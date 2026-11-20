"""Calculate an evidence-approved ledger; never infer expenses from chat."""

import argparse
import json
import re
from decimal import Decimal, ROUND_HALF_UP, localcontext
from functools import lru_cache
from pathlib import Path


def decimal_value(value, label):
    if not isinstance(value, str) or not re.fullmatch(r"\d{1,12}(?:\.\d{1,8})?", value):
        raise ValueError(f"{label} must be a positive decimal string (up to 8 decimals)")
    number = Decimal(value)
    if number <= 0:
        raise ValueError(f"{label} must be positive")
    return number


def money(paise):
    sign = "-" if paise < 0 else ""
    rupees, remainder = divmod(abs(paise), 100)
    return f"{sign}{rupees}.{remainder:02d}"


def split_paise(total, weights, participants):
    denominator = sum(weights.values())
    shares = {name: total * weights[name] // denominator for name in weights}
    order = {name: index for index, name in enumerate(participants)}
    ranked = sorted(
        weights,
        key=lambda name: (-(total * weights[name] % denominator), order[name]),
    )
    for name in ranked[: total - sum(shares.values())]:
        shares[name] += 1
    return shares


def minimum_transfers(balances, participants):
    # Maximum disjoint zero-sum groups imply minimum transfers: n - groups.
    active = [name for name in participants if balances[name]]
    values = [balances[name] for name in active]
    sums = [0] * (1 << len(active))
    for mask in range(1, len(sums)):
        bit = mask & -mask
        sums[mask] = sums[mask ^ bit] + values[bit.bit_length() - 1]

    @lru_cache(maxsize=None)
    def partition(mask):
        if not mask:
            return ()
        first = mask & -mask
        best = (mask,)
        subset = (mask - 1) & mask
        while subset:
            if subset & first and sums[subset] == 0:
                candidate = (subset,) + partition(mask ^ subset)
                if len(candidate) > len(best):
                    best = candidate
                    if len(best) == mask.bit_count() // 2:
                        break
            subset = (subset - 1) & mask
        return best

    transfers = []
    for group in partition(len(sums) - 1):
        debtors = [
            [name, -balances[name]]
            for index, name in enumerate(active)
            if group & (1 << index) and balances[name] < 0
        ]
        creditors = [
            [name, balances[name]]
            for index, name in enumerate(active)
            if group & (1 << index) and balances[name] > 0
        ]
        debtor_index = creditor_index = 0
        while debtor_index < len(debtors) and creditor_index < len(creditors):
            debtor, owed = debtors[debtor_index]
            creditor, due = creditors[creditor_index]
            amount = min(owed, due)
            transfers.append(
                {"from": debtor, "to": creditor, "amount_paise": amount, "amount_inr": money(amount)}
            )
            debtors[debtor_index][1] -= amount
            creditors[creditor_index][1] -= amount
            if debtors[debtor_index][1] == 0:
                debtor_index += 1
            if creditors[creditor_index][1] == 0:
                creditor_index += 1
    return transfers


def calculate(rules, ledger):
    if not isinstance(rules, dict) or not isinstance(ledger, dict):
        raise ValueError("Rules and ledger must be JSON objects")
    participants = rules.get("participants")
    if (
        not isinstance(participants, list)
        or not 1 <= len(participants) <= 12
        or any(not isinstance(name, str) or not name.strip() for name in participants)
        or len(set(participants)) != len(participants)
    ):
        raise ValueError("Provide 1-12 unique, nonempty participant names")
    if rules.get("base_currency") != "INR":
        raise ValueError("This calculator requires INR as base currency")
    rates = rules.get("inr_per_unit")
    if not isinstance(rates, dict) or not rates:
        raise ValueError("Provide inr_per_unit currency rates")
    parsed_rates = {key: decimal_value(value, f"Rate for {key}") for key, value in rates.items()}
    if parsed_rates.get("INR") != Decimal("1"):
        raise ValueError("INR rate must be 1")
    expenses = ledger.get("expenses")
    if not isinstance(expenses, list):
        raise ValueError("Ledger must contain an expenses array")

    balances = dict.fromkeys(participants, 0)
    seen = set()
    computed = []
    total = 0
    for row in expenses:
        if not isinstance(row, dict):
            raise ValueError("Every expense must be an object")
        identifier = row.get("id")
        if not isinstance(identifier, str) or not identifier.strip() or identifier in seen:
            raise ValueError("Expense IDs must be nonempty and unique")
        seen.add(identifier)
        if not isinstance(row.get("description"), str) or not row["description"].strip():
            raise ValueError(f"{identifier}: description is required")
        payer = row.get("paid_by")
        if not isinstance(payer, str) or payer not in balances:
            raise ValueError(f"{identifier}: unknown payer")
        currency = row.get("currency")
        if not isinstance(currency, str) or currency not in parsed_rates:
            raise ValueError(f"{identifier}: unsupported currency")
        amount = decimal_value(row.get("amount"), f"{identifier} amount")
        weights = row.get("shares")
        if (
            not isinstance(weights, dict)
            or not weights
            or any(
                name not in balances or type(weight) is not int or weight <= 0
                for name, weight in weights.items()
            )
        ):
            raise ValueError(f"{identifier}: shares require known names and positive integer weights")
        sources = row.get("sources")
        if (
            not isinstance(sources, list)
            or not sources
            or any(not isinstance(source, str) or not source.strip() for source in sources)
        ):
            raise ValueError(f"{identifier}: at least one source citation is required")
        with localcontext() as context:
            context.prec = 50
            paise = int((amount * parsed_rates[currency] * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        if paise <= 0:
            raise ValueError(f"{identifier}: converted amount rounds to zero")
        allocated = split_paise(paise, weights, participants)
        balances[payer] += paise
        for name, share in allocated.items():
            balances[name] -= share
        total += paise
        computed.append(
            {
                **row,
                "amount_paise": paise,
                "amount_inr": money(paise),
                "shares_paise": allocated,
                "shares_inr": {name: money(share) for name, share in allocated.items()},
            }
        )

    if sum(balances.values()) != 0:
        raise ValueError("Internal error: balances do not sum to zero")
    transfers = minimum_transfers(balances, participants)
    remaining = balances.copy()
    for transfer in transfers:
        remaining[transfer["from"]] += transfer["amount_paise"]
        remaining[transfer["to"]] -= transfer["amount_paise"]
    if any(remaining.values()):
        raise ValueError("Internal error: transfers do not settle balances")
    return {
        "currency": "INR",
        "status": "provisional_confirmed_ledger_only",
        "balance_sign": "positive receives; negative owes",
        "total_paise": total,
        "total_inr": money(total),
        "expenses": computed,
        "balances_paise": balances,
        "balances_inr": {name: money(value) for name, value in balances.items()},
        "net_total_paise": sum(balances.values()),
        "minimum_transfer_count": len(transfers),
        "transfers": transfers,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rules", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve() in {args.rules.resolve(), args.ledger.resolve()}:
        parser.error("Output must not overwrite rules or ledger")
    try:
        rules = json.loads(args.rules.read_text(encoding="utf-8-sig"))
        ledger = json.loads(args.ledger.read_text(encoding="utf-8-sig"))
        result = calculate(rules, ledger)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Settlement failed: {error}\n")
    print(f"Wrote {args.output}: {result['minimum_transfer_count']} transfers (provisional)")


if __name__ == "__main__":
    main()
