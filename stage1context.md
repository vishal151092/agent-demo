# Stage 1: the first-pass agent, and why it isn't enough (about 15 minutes)

> **Presenter-only. Contains answers.** Stage 1 of 3 toward `workshop3agent`. Uses the
> same `sample1` as the opening, unchanged. Run demos in a clean copy of the repo that
> contains only `.github\agents\stage1agent.agent.md`, `settle.py` and `sample1`.
> Otherwise the agent can find `context.md` or this file.

Conventions: **SAY** = speaking notes, **DO** = action, **ASK** = question to the room.

## Run sheet

| Time | Do | Key line |
|---|---|---|
| 0–3 | Walk through `stage1agent`: what it gets right and what it says | "This is the agent most of us write first." |
| 3–6 | Run it on `sample1` | "Watch the loop: read, write, calculate, report." |
| 6–10 | Compare its answer with the hand-built ledger. It guessed the boat and fuel. | Reason for **stage 2** |
| 10–14 | Ask the report to justify itself. It can't. | Reason for **stage 3** |
| 14–15 | Bridge | "Right tools, wrong instructions." |

---

## 0–3 min: walk through the agent

**DO:** Open `.github\agents\stage1agent.agent.md`. **SAY:** "This is the draft most
people write first. It looks reasonable. Two concepts are applied well."

| Concept | Where | SAY |
|---|---|---|
| The model reasons, tools calculate | Section 2: ledger format plus the `settle.py` command | "No mental arithmetic. A tool does every rupee." |
| Boundaries | Section 3 and the `tools:` line | "It can't change the evidence, pay anyone or message anyone." |

**DO:** Without commenting, highlight these three lines. You will come back to them:

1. *"The group wants a **complete, final settlement** so everyone can pay up today."*
2. *"`house-rules.json`: the participant names and currency exchange rates."*
3. *"Make sure **every expense the group mentions ends up in the ledger** so nothing is forgotten."*

**ASK:** "Anything here you wouldn't have written yourself?" Most rooms say no.

## 3–6 min: run it

**DO:** In a clean copy, select **stage1agent** in Copilot Chat and send
`Settle the trip in sample1.` As it runs, name each step of the loop: it **reads** the chat,
receipts and rules, **writes** `ledger.json`, **runs** `settle.py` and **writes** the report.
It takes about 50 seconds and 5–8 tool calls.

## 6–10 min: compare with the hand-built ledger (the case for stage 2)

**DO:** Open `sample1\output\calculation.json` beside the opening's finished ledger.

**Expect it to guess.** In 4 of 5 rehearsal runs it added two rows the group never confirmed:

| | Hand-built (opening) | Stage 1 agent (4 of 5 runs) |
|---|---|---|
| E1–E6: cabs, dinner food and drinks split, hostel at 83.00, breakfast | ✔ | ✔ identical |
| Boat ride, M007/M008 | Excluded; ask who boarded | **₹2,400 split across all five** |
| Fuel, M009 "~2k" | Excluded; ask the exact amount | **Entered as ₹2,000.00** |
| Total | ₹15,500 | **₹19,900** |
| Prem pays Dev | ₹1,620 | **₹2,500** |
| Rahul pays Dev | ₹3,220 | **₹1,700** |

**SAY:** "Every transfer is wrong. The arithmetic is perfect, because `settle.py` did it.
The *ledger* is wrong."

**DO:** Read out what the agent wrote, word for word (rehearsal run 1):

> *"The ledger uses INR 2,000.00 for the approximate fuel amount in M009 and splits the
> boat ride across all five participants although attendance is uncertain (M007-M008)."*

**ASK:** "Did it notice the problem?" Yes. "Did it read the house rules?" Yes. In every
run, it opened `house-rules.json`, which says *"never estimate or silently assume."*
"So why did it guess?"

**DO:** Go back to the three highlighted lines and connect each one to the failure:

| Line in the agent | What it caused | Concept applied wrongly |
|---|---|---|
| "complete, **final** settlement… pay up **today**" | Pressure to fill every gap instead of stopping | Goal: no point where it stops and asks a human |
| `house-rules.json` = "names and exchange rates" | The policy was read but not treated as binding | Context: the rules are not named as the authority |
| "**every expense**… so nothing is forgotten" | ~2k became 2,000.00; "booked for the group" became all five | Goal: completeness beat correctness |

**SAY:**
> "We never told it to guess. We told it to be complete and final, and we never said
> what to do when evidence is unclear. When instructions conflict, the agent follows
> the one we emphasized. Stage 2 fixes this: uncertain items are excluded and turned
> into specific questions for the group, and the house rules become the authority."

## 10–14 min: ask the report to justify itself (the case for stage 3)

**SAY:** "Suppose the numbers had been right. Rahul still asks, *'Why do I owe this?'*"

**DO:** Open `sample1\output\settlement-report.md` and **ASK** the room to find each item:

| Can the report show… | Rehearsal result (5 runs) |
|---|---|
| Which messages and receipts each row came from? | 2 of 5 reports showed sources. All 5 ledgers had them, only because `settle.py` refuses rows without one. |
| Why R001 and M001 were merged, and the dinner counted once? | 0 of 5 explained a merge |
| Why M006 is a *separate* ₹1,500 cab, not a duplicate? | 0 of 5 |
| That every message and receipt was accounted for? | 0 of 5 had a coverage check |
| Questions for the group? | 1 of 5 |
| The same layout run to run? | No. Reports ranged from 23 to 38 lines. |

**SAY:**
> "Even when it's right, we can't tell a reliable answer from a lucky one. Stage 3
> requires evidence for every row and merge, a coverage check, and a clear finish line."

**Point out one thing that worked:** every report was labelled *provisional*, even though
the agent asked for a *final* settlement. That label came from `settle.py`'s
output status, not the model. **SAY:** "That's the tool acting as a guardrail. Tools can enforce
what instructions only ask for."

## 14–15 min: bridge

**SAY:**
> "Stage 1 got the tools and boundaries right. It got the *instructions* wrong in two ways:
> - **Stage 2:** say what to do with uncertainty: exclude it, ask, and let the human decide.
> - **Stage 3:** say what proof to show, and when the job is done."

**DO:** Type into the empty comments in the agent, live:
`Stage 2: house rules are the authority; uncertain items become questions, not guesses.` and
`Stage 3: every row shows its evidence; check coverage; then stop.`

---

## If the live run differs from rehearsal

- **It excludes the boat and fuel and asks questions** (rehearsal run 2, 1 of 5): **SAY:** "It
  got lucky. It read the policy and followed it this time, but our goal pushed the other way."
  Rerun it in a new chat. In rehearsal it guessed 4 times out of 5. Then show the table above
  and continue with the stage 3 audit, which applies either way.
- **It guesses only one item:** use that one. The point is the same.

## Rehearsal evidence

Recorded 2026-11-21 with Copilot CLI 1.0.114 in Auto model mode. Each run used a fresh
session in a clean copy containing only the agent, `settle.py` and `sample1` (without `scorecard.md`).

| Run | Boat | Fuel | Total | Transfers correct? | Report |
|---|---|---|---:|---|---|
| 1 | All five | ₹2,000 | ₹19,900 | No | Notes both guesses, no questions |
| 2 | Excluded | Excluded | ₹15,500 | Yes | Asks two specific questions |
| 3 | All five | ₹2,000 | ₹19,900 | No | Notes both guesses, no sources |
| 4 | All five | ₹2,000 | ₹19,900 | No | Notes both guesses, no sources |
| 5 | All five | ₹2,000 | ₹19,900 | No | Mentions neither |

Each run cost 0.27–0.37 AI credits and took 35–54 seconds. Results vary by model and run.
To rehearse from a clean copy:

```powershell
copilot --agent stage1agent -p "Settle the trip in sample1." --allow-all-tools --trust-folder
```
