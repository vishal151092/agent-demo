import copy
import itertools
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from settle import calculate, minimum_transfers


class SettlementTests(unittest.TestCase):
    def setUp(self):
        self.rules = {
            "participants": ["A", "B", "C"],
            "base_currency": "INR",
            "inr_per_unit": {"INR": "1", "USD": "83.00"},
        }
        self.row = {
            "id": "E1",
            "description": "Shared fare",
            "paid_by": "A",
            "amount": "1.00",
            "currency": "INR",
            "shares": {"C": 1, "B": 1, "A": 1},
            "sources": ["chat.txt:M1"],
        }

    def test_equal_split_remainder_uses_policy_order_not_object_order(self):
        result = calculate(self.rules, {"expenses": [self.row]})
        self.assertEqual(result["expenses"][0]["shares_paise"], {"C": 33, "B": 33, "A": 34})
        self.assertEqual(result["balances_paise"], {"A": 66, "B": -33, "C": -33})
        self.assertEqual(result["minimum_transfer_count"], 2)
        self.assertEqual(result["net_total_paise"], 0)

    def test_weighted_split_and_foreign_currency_half_up(self):
        self.row.update(amount="0.015", currency="USD", shares={"A": 1, "B": 2})
        result = calculate(self.rules, {"expenses": [self.row]})
        self.assertEqual(result["total_paise"], 125)
        self.assertEqual(result["expenses"][0]["shares_paise"], {"A": 42, "B": 83})
        self.assertEqual(result["transfers"], [
            {"from": "B", "to": "A", "amount_paise": 83, "amount_inr": "0.83"}
        ])

    def test_itemized_meal_excludes_drinks_only_diner_from_food(self):
        food = {**self.row, "amount": "12.00", "shares": {"A": 1, "B": 1}}
        drinks = {**self.row, "id": "E2", "amount": "3.00"}
        result = calculate(self.rules, {"expenses": [food, drinks]})
        self.assertEqual(result["balances_paise"], {"A": 800, "B": -700, "C": -100})

    def test_invalid_evidence_rows_are_rejected(self):
        changes = [
            {"amount": "~2k"}, {"amount": 2.0}, {"amount": "NaN"},
            {"amount": "-1"}, {"amount": "0"}, {"amount": "0.00001"},
            {"currency": "EUR"}, {"paid_by": "Unknown"},
            {"shares": {}}, {"shares": {"B": True}}, {"shares": {"B": 1.5}},
            {"shares": {"B": 0}}, {"shares": {"Unknown": 1}},
            {"sources": []}, {"sources": [""]}, {"description": ""},
        ]
        for change in changes:
            with self.subTest(change=change), self.assertRaises(ValueError):
                calculate(self.rules, {"expenses": [{**self.row, **change}]})
        with self.assertRaises(ValueError):
            calculate(self.rules, {"expenses": [self.row, self.row]})

    def test_empty_ledger_and_already_balanced(self):
        self.assertEqual(calculate(self.rules, {"expenses": []})["transfers"], [])
        other = {**self.row, "id": "E2", "paid_by": "B"}
        self.row.update(shares={"A": 1, "B": 1})
        other.update(shares={"A": 1, "B": 1})
        self.assertEqual(calculate(self.rules, {"expenses": [self.row, other]})["transfers"], [])

    def test_exact_minimum_beats_naive_greedy(self):
        balances = {"A": -800, "B": -700, "C": -500, "D": 1000, "E": 800, "F": 200}
        transfers = minimum_transfers(balances, list(balances))
        self.assertEqual(len(transfers), 4)
        remaining = balances.copy()
        for transfer in transfers:
            remaining[transfer["from"]] += transfer["amount_paise"]
            remaining[transfer["to"]] -= transfer["amount_paise"]
        self.assertTrue(all(value == 0 for value in remaining.values()))

    def test_minimum_count_against_independent_small_state_search(self):
        def oracle(values):
            values = tuple(value for value in values if value)
            if not values:
                return 0
            best = len(values)
            for index in range(1, len(values)):
                if values[0] * values[index] < 0:
                    next_values = list(values[1:])
                    next_values[index - 1] += values[0]
                    best = min(best, 1 + oracle(next_values))
            return best

        for prefix in itertools.product((-2, -1, 0, 1, 2), repeat=4):
            values = (*prefix, -sum(prefix))
            balances = dict(zip("ABCDE", values))
            with self.subTest(values=values):
                self.assertEqual(len(minimum_transfers(balances, list(balances))), oracle(values))

    def test_participant_limit_and_base_currency(self):
        for change in [
            {"participants": ["A", "A"]},
            {"participants": list("ABCDEFGHIJKLM")},
            {"participants": []},
            {"base_currency": "USD"},
            {"inr_per_unit": {"INR": "2"}},
        ]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                calculate({**self.rules, **change}, {"expenses": []})

    def test_cli_writes_result_and_preserves_inputs_on_error(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            rules_path, ledger_path, output_path = [root / name for name in ("rules.json", "ledger.json", "output.json")]
            rules_path.write_text(json.dumps(self.rules), encoding="utf-8")
            ledger_path.write_text(json.dumps({"expenses": [self.row]}), encoding="utf-8")
            command = [
                sys.executable, str(Path(__file__).resolve().parents[1] / "settle.py"),
                "--rules", str(rules_path), "--ledger", str(ledger_path),
                "--output", str(output_path),
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(output_path.read_text())["total_paise"], 100)
            original = ledger_path.read_bytes()
            result = subprocess.run(command[:-1] + [str(ledger_path)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(ledger_path.read_bytes(), original)
            invalid = copy.deepcopy(self.row)
            invalid["sources"] = []
            ledger_path.write_text(json.dumps({"expenses": [invalid]}), encoding="utf-8")
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source citation", result.stderr)


if __name__ == "__main__":
    unittest.main()
