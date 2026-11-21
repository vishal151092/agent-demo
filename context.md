# Setting the stage: "The Goa trip is over. Who owes whom?"

> **Presenter-only document.** Run this opening **before** stage 1 of the hands-on
> workshop that builds up to `workshop3agent`. It contains the answer key.
> Do not leave this file open on a shared screen, and do not keep it in the
> workspace participants hand to an agent. The agent's tools can find and read it.

**Duration:** about 20 minutes, in three parts:

| Part | Time | What the audience does | What they should take away |
|---|---|---|---|
| 1. Story and sample | 0–4 min | Listen and open `sample1` | Messy evidence and a precise policy |
| 2. Build the ledger by hand | 4–14 min | Validate one receipt at a time against the chat | Most of the work is **judgment**, not arithmetic |
| 3. Compute balances | 14–20 min | Watch one worked example, then do the rest | Arithmetic is mechanical, so a **tool** should do it |

**Have ready:** `sample1\chat.txt`, `sample1\receipts\*.txt`, `sample1\house-rules.json`
open in tabs. Use a whiteboard or slide with an empty ledger table (columns below).
Do **not** show `settle.py` or any agent file yet.

Conventions below: **SAY** = speaking notes (paraphrase freely), **DO** = action,
**ASK** = question to the room, **⚖ JUDGMENT** = where a human had to decide.

## Quick run sheet (present from this; expand a part only if you need the detail)

| Time | Do | Key line |
|---|---|---|
| 0–4 | Show `sample1`. Read the four house rules aloud and point out the fixed USD rate of 83.00. Have pairs guess the total, but don't reveal it. | "Without rules, two careful people settle this trip differently." |
| 4–14 | Fill the ledger: **R001 + M001** merge ⚖ · **M006** separate ride ⚖ · **R002** food 2,400 split 4 ways, drinks 800 split 5 ways; Priya had drinks only ⚖⚖⚖ · **R003** USD 100 × 83 = 8,300 ⚖ · **R004** merge · **boat, fuel** become questions ⚖⚖ | "Seven ⚖ marks, and none of them is arithmetic." |
| 14–20 | Work Priya live: paid 1,000, share 2,620, **owes 1,620**. Pairs do the rest. Check that balances add to 0 and shares add to 15,500. | "Paid minus share. That part is mechanical." |
| +0.5 | Bridge to stage 1. | "The model reasons, a tool calculates." |

Confirmed total **₹15,500**. The answer key is in Part 3.

---

## Part 1 — Share the story and the sample (0–4 min)

<details>
<summary>Full notes for Part 1</summary>

**SAY:**
> "Five friends, Arjun, Meera, Priya, Rahul and Dev, just got back from a weekend in
> Goa, 14–15 November. Nobody used a split app. All we have is the group chat,
> four receipt notes that someone saved, and a short list of house rules they
> agreed on. Someone has to work out who owes whom. Everyone in this room has
> been that person, or owed money to that person."

**DO:** Show the sample folder.

```text
sample1\
  chat.txt             11 messages, M001–M011
  house-rules.json     participants, base currency, USD rate, policy
  receipts\
    airport-cab.txt    R001
    dinner.txt         R002
    hostel.txt         R003
    breakfast.txt      R004
```

**DO:** Scroll through `chat.txt` once without stopping. Then open `house-rules.json`
and read these four rules aloud, because they decide almost every item:

1. *"Merge sources only when payer, amount, currency, date and expense context
   identify the same expense. Equal amounts alone do not imply duplicates."*
2. *"For itemized meals, split each category among its confirmed consumers.
   Drinks-only diners do not share food."*
3. *"Uncertain third-party attendance reports require confirmation; paying alone
   does not prove attendance."*
4. *"Exclude any expense whose exact amount, payer or participant set remains
   unresolved. Ask a source-linked question; never estimate."*

Also point out `"inr_per_unit": {"USD": "83.00"}`: a fixed rate, not a live one.

**SAY:**
> "This is all fictional. The rules are what make the job fair. Without them,
> two careful people will settle this trip differently. Let's prove that."

**ASK (optional, 60 seconds):** "In pairs, glance at the chat and guess the total
confirmed spend." Collect two or three answers. They will differ (common wrong
answers: ₹19,900 if they include the boat and "~2k" fuel, ₹18,700 if they add
the dinner twice; the confirmed total is ₹15,500).
Do not reveal the right answer yet.

</details>

---

## Part 2 — Fill the ledger one receipt at a time (4–14 min)

<details>
<summary>Full notes for Part 2</summary>

**SAY:**
> "The method: take one receipt, find every chat message about the same expense,
> check them against each other, then apply the rules. Write a ledger row only
> when the payer, the amount and the people sharing it are all confirmed.
> Anything else becomes a question. Every row must cite its sources."

**DO:** Draw the empty ledger:

| ID | Expense | Paid by | Amount | INR | Shared by | Sources | Notes |
|---|---|---|---|---|---|---|---|

Fill it in live, in this order.

### Receipt R001: airport cab

- **Receipt:** Arjun, INR 1500.00, 2026-11-14, airport to hostel, all five passengers.
- **Chat:** M001 says the same: Arjun, INR 1500, airport-to-hostel cab, all five.
- **Decision:** R001 and M001 are the **same expense**. Payer, amount, currency,
  date and route all match. Merge them into one row.

| E1 | Airport-to-hostel cab | Arjun | INR 1500.00 | 1500.00 | All 5 | M001, R001 | merged duplicate |

**⚖ JUDGMENT:** Deciding that two sources describe one expense. **SAY:** "No
formula told us these match. We compared five attributes and decided."

### Hold on: M006, the return cab (no receipt)

**DO:** Before moving on, point to M006: Arjun, INR 1500, hostel-to-airport, all
five, **on 15 Nov**, *"a different ride from yesterday's cab."*

**ASK:** "Same payer, same amount, same people. Is this a duplicate of E1?"
Let the room argue for 30 seconds.

- **Decision:** **No.** The date and route differ, and the payer says it was a
  separate ride. Rule 1: *equal amounts alone do not imply duplicates.* It gets
  its own row, cited only to the chat.

| E6 | Hostel-to-airport cab | Arjun | INR 1500.00 | 1500.00 | All 5 | M006 | distinct ride, no receipt |

**⚖ JUDGMENT:** Deciding **not** to merge. **SAY:** "This is the mirror image of
R001. An over-eager deduplicator silently loses ₹1,500 here."

### Receipt R002: dinner at Sunset Table

- **Receipt:** Meera, total INR 3200.00 = **food 2400.00 + drinks 800.00**, 14 Nov.
  The receipt does not list diners.
- **Chat:** M002 (Meera paid 3200 for dinner), M003 (Priya: *"I only had drinks.
  Arjun, Meera, Rahul and Dev had the food. All five shared the drinks."*), M010
  (Meera: the receipt is *"the same dinner… not a second charge"*).
- **Decisions:**
  1. M002, M010 and R002 are **one** dinner. Count ₹3,200 once, not two or three times.
  2. The receipt is itemized, so split it into **two rows** by category (rule 2).
  3. Who shared what comes from M003. It is a first-hand account from Priya
     about her own consumption, and it names everyone. That is enough to confirm it.

| E2 | Dinner – food | Meera | INR 2400.00 | 2400.00 | Arjun, Meera, Rahul, Dev | M002, M003, M010, R002 | Priya excluded (drinks only) |
| E3 | Dinner – drinks | Meera | INR 800.00 | 800.00 | All 5 | M002, M003, M010, R002 | |

**⚖ JUDGMENT (three times):** (a) three sources, one expense; (b) splitting one
bill into two rows; (c) trusting M003 as first-hand evidence. **SAY:** "An equal
five-way split of ₹3,200 is the most common mistake here. It overcharges Priya ₹480."

### Receipt R003: hostel (USD)

- **Receipt:** Dev, **USD 100.00**, two nights, all five guests, no extra fees.
- **Chat:** M004 matches: Dev, USD 100.00, hostel, both nights, all five.
- **Decision:** Merge them into one row. Convert at the **policy** rate of 83.00, so
  USD 100.00 → **INR 8,300.00**. Do not look up today's exchange rate.

| E4 | Hostel, 2 nights | Dev | USD 100.00 | 8300.00 | All 5 | M004, R003 | policy rate 83.00 |

**⚖ JUDGMENT:** Small but real: which exchange rate counts. **SAY:** "If two of you
use different live rates, you get different answers. The rate belongs in the rules."

### Receipt R004: breakfast

- **Receipt:** Priya, INR 1000.00, 15 Nov, all five diners.
- **Chat:** M005 matches it exactly and says "split equally."
- **Decision:** Merge into one row. Nothing unusual. **SAY:** "Not every item is a trap.
  Recognizing the easy ones quickly also matters."

| E5 | Breakfast | Priya | INR 1000.00 | 1000.00 | All 5 | M005, R004 | merged duplicate |

### Chat-only claims with no receipt: these become questions, not rows

**Boat ride (M007, M008):**
- Rahul paid INR 2400 (first-hand, so payer and amount are confirmed).
- **Who went** is unconfirmed. Meera *"thinks"* Rahul skipped, which is
  uncertain third-party hearsay. Rahul himself says *"paying doesn't tell you who
  actually boarded."*
- **Decision:** **Exclude** it and ask: *"Who boarded the boat ride Rahul paid
  INR 2400 for (M007, M008)? Rahul, did you go?"*

**⚖ JUDGMENT:** Refusing to guess. **ASK:** "Who assumed all five went? Who assumed
four?" Either way, you made up the participant set.

**Fuel (M009):**
- Dev paid, and all five were in the car, but the amount is *"~2k"*, and Dev says
  he'll find the exact figure later.
- **Decision:** **Exclude** it and ask: *"Dev, what was the exact fuel amount (M009)?"*

**⚖ JUDGMENT:** Do not write down ₹2,000. **SAY:** "Writing ₹2,000 feels helpful,
but it puts a made-up number into someone else's debt."

**Non-expenses:** M011 is chatter and needs no row. **SAY:** "Still, check every
message so you can say coverage is complete."

### The finished ledger (confirmed only)

| ID | Expense | Paid by | INR | Shared by |
|---|---|---|---:|---|
| E1 | Airport cab | Arjun | 1,500 | All 5 |
| E2 | Dinner – food | Meera | 2,400 | Arjun, Meera, Rahul, Dev |
| E3 | Dinner – drinks | Meera | 800 | All 5 |
| E4 | Hostel (USD 100 × 83) | Dev | 8,300 | All 5 |
| E5 | Breakfast | Priya | 1,000 | All 5 |
| E6 | Return cab | Arjun | 1,500 | All 5 |
| | **Total confirmed** | | **15,500** | |

**Open questions:** boat ride participants (M007/M008); exact fuel amount (M009).

**SAY (recap of judgment calls):**
> "Count the ⚖ marks: merging duplicates, refusing to merge the return cab,
> splitting an itemized bill, trusting a first-hand statement, choosing the exchange
> rate, and twice refusing to guess. None of that is arithmetic. That is the part
> an agent can help with, as long as it shows its evidence and asks when unsure."

</details>

---

## Part 3 — Compute each person's balance (14–20 min)

<details>
<summary>Full notes for Part 3</summary>

**SAY:**
> "Now the mechanical part. For each person: **balance = what they paid − their
> share of what they consumed.** Positive means they receive money; negative means
> they owe."

### Worked example: Priya

**DO:** Work this out live on the board. Priya is a good example because the
dinner split affects her.

**Step 1: what Priya paid.**

| Row | Paid |
|---|---:|
| E5 Breakfast | 1,000 |
| **Total paid** | **1,000** |

**Step 2: Priya's share of each row she consumed** (amount ÷ number of sharers).

| Row | Calculation | Priya's share |
|---|---|---:|
| E1 Airport cab | 1,500 ÷ 5 | 300 |
| E2 Dinner – food | not a sharer | 0 |
| E3 Dinner – drinks | 800 ÷ 5 | 160 |
| E4 Hostel | 8,300 ÷ 5 | 1,660 |
| E5 Breakfast | 1,000 ÷ 5 | 200 |
| E6 Return cab | 1,500 ÷ 5 | 300 |
| **Total share** | | **2,620** |

**Step 3: balance.** 1,000 − 2,620 = **−1,620**, so **Priya owes ₹1,620.**

**SAY:**
> "With a naive five-way dinner split, Priya's share would be ₹3,100 instead of
> ₹2,620, and she'd owe ₹2,100. That's ₹480 wrong because of one judgment call,
> even with perfect arithmetic."

### Exercise for the audience (3 minutes, in pairs)

**SAY:** "Do the same three steps for Arjun, Meera, Rahul and Dev. Two checks:
the balances must add to **zero**, and the shares must add to ₹15,500. Then work
out the fewest payments that settle everything."

**DO:** Leave the finished ledger table on screen. Walk around and listen for
mistakes: dividing food by five, adding the dinner twice, dropping the return
cab, or including the fuel or boat ride.

<details>
<summary><strong>Presenter answer key (do not show until pairs finish)</strong></summary>

| Person | Paid | Share | Balance | Meaning |
|---|---:|---:|---:|---|
| Arjun | 3,000 (E1 + E6) | 3,220 | **−220** | owes |
| Meera | 3,200 (E2 + E3) | 3,220 | **−20** | owes |
| Priya | 1,000 (E5) | 2,620 | **−1,620** | owes |
| Rahul | 0 | 3,220 | **−3,220** | owes |
| Dev | 8,300 (E4) | 3,220 | **+5,080** | receives |
| **Check** | **15,500** | **15,500** | **0** | |

Each food eater's share: 300 + 600 + 160 + 1,660 + 200 + 300 = 3,220.

**Minimum transfers (4):** Arjun → Dev ₹220 · Meera → Dev ₹20 ·
Priya → Dev ₹1,620 · Rahul → Dev ₹3,220.

These figures were checked with `settle.py` on the confirmed ledger above. The
result is **provisional**. The boat ride (₹2,400, Rahul paid) and the fuel (Dev paid)
will change it once the group answers.
</details>

**ASK:** "Who got exactly these numbers?" Usually not everyone. **ASK:** "Was
the disagreement about the arithmetic, or the ledger?" It's almost always the ledger.

</details>

---

## Closing: bridge to stage 1 (30 seconds)

**SAY:**
> "That took us about fifteen minutes for eleven messages and four receipts. Two
> lessons will shape everything we build next:
> 1. **The model should do the reasoning**: matching sources, applying the rules,
>    knowing when to ask, and citing evidence.
> 2. **A tool should do the calculating**: the step we just did by hand is exactly
>    what `settle.py` does, and a model doing mental arithmetic on money is a bug.
>
> Over the next three stages we'll build an agent that does Part 2 with evidence,
> hands Part 3 to a tool, and stops to ask a human about the boat and the fuel."

**DO:** Close this file. Move to stage 1.
