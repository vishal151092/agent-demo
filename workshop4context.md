# Between Workshop 3 and Workshop 4: prove where optimization is needed

> **Presenter guide.** Use after Workshop 3's trustworthy agent and before
> Workshop 4's efficiency experiments in `workshop-plan.md`. This guide explains
> evidence collection and preserves one measured rehearsal below; it does not
> establish an optimized speedup. Keep presenter notes and review answers out of the solver's
> clean input workspace, as in `context.md` and `stage1context.md`.

**Outcome:** an adversarially reviewed baseline in the existing
`sample1\scorecard.md`, preserved solver traces, and findings that identify the
first optimization to test. Do not add scorecard dimensions: its quality,
elapsed time, requests/calls, usage and corrections already support the decision.

**SAY:**
> "Workshop 3 gave us an answer we can inspect. Now we need to know whether it
> is doing unnecessary work. The solver cannot grade itself. A second agent
> will try to prove it wrong, and our logs will show what the work cost."

## Rehearsal evidence: November 21, 2026

Run **W3-TEST-20261121** used the actual `workshop3finalagent` on an unchanged
clean copy of `sample1`, followed by `reviewagent` in a separate fresh workspace.
No presenter answers, old reports or baseline scorecard were available to the
solver. SHA256 checks confirmed the input files were unchanged. The existing
`sample1\scorecard.md` is the completed rehearsal scorecard, not a blank template.

### Recorded measurements

| Existing scorecard dimension | Observed solver result | Measurement source |
|---|---|---|
| Client / model selected | Copilot CLI 1.0.114; administrator-selected Auto; usage export reported `gpt-6.1-terra` | Current run's session metadata, console and `usage.json:currentModel` |
| Input / policy | 5 people, 11 messages, 4 receipts; fixed USD rate 83.00 | Unchanged `sample1` source files and snapshotted policy |
| End-to-end elapsed time | **61.149 seconds**, recorded user prompt to final assistant response | P001 `2026-11-21T06:14:30.503Z` to F001 `2026-11-21T06:15:31.652Z` |
| Model requests / tool calls | **9 model requests; 14 executed tool calls**, including 1 contract read and 13 workflow calls | `usage.json:modelMetrics.gpt-6.1-terra.requests.count`; distinct successful T001-T014 events |
| Tokens / usage | **110,208 input; 4,394 output; 91,220 cache read; 18,961 cache write; 539 reasoning tokens as reported; 3.52 displayed AI credits** | Model usage fields and solver console's final AI Credits summary |
| Human corrections | None; no interactive approvals or interruptions | Presenter observation and trace |

Do not add cache or reasoning categories to totals again. The one submitted
user prompt and reported premium-request cost of 1 are **not** the 9 model
requests. Reviewer calls, time and usage are excluded.

Separately measured process-launch-to-exit time was **70.909 seconds**,
including CLI startup and local export; API duration was **58.452 seconds**.
Neither substitutes for the prompt-to-final scorecard metric. Individual tool
events were projected together at the final commit, so their timestamps do
**not** provide trustworthy per-call latencies. Event order and payloads still
identify what happened; no per-tool latency savings are claimed.

### Rehearsal trace excerpts

These are actual executed events, indexed T001-T014 from this rehearsal's
local trace. Paths below are relative to its clean workspace. Exact start-event
IDs are preserved so cleanup does not turn the presenter notes into dead links.
Every event had a successful matching completion.

| Trace | Tool and exact target/action | Start-event ID |
|---|---|---|
| T001 | `view workshop3finalagent.md` (contract setup) | `128d50a8-af3d-4530-8528-164bb66b5afb` |
| T002 | `view sample1\house-rules.json` | `3e6541db-3bdb-4c8d-82a2-758583a2684d` |
| T003 | `view sample1\chat.txt` (full chat) | `2f6c1fee-36bc-4c96-8a6a-9b4c8207701e` |
| T004 | `view sample1\receipts` (directory inventory) | `65158851-6f10-412f-ad7e-52f56b59b52e` |
| T005 | `view sample1\receipts\airport-cab.txt` | `1b8f49ad-5199-4614-86de-eb00aa27f47d` |
| T006 | `view sample1\receipts\breakfast.txt` | `db3c2576-eff0-4978-9ccb-3ff24f70aa44` |
| T007 | `view sample1\receipts\dinner.txt` | `e6e53c86-f15d-47c0-a3f3-3ce4104805f6` |
| T008 | `view sample1\receipts\hostel.txt` | `fcaafe11-5378-468b-9140-9c145f8e70c0` |
| T009 | `apply_patch` creates `sample1\output\ledger.json` (58 lines) | `c7a4c417-3e55-429a-b359-3cfbb535ba09` |
| T010 | `powershell` runs the calculator command below once | `8c2838ab-d772-4dcb-a47d-7c0559236087` |
| T011 | `view sample1\output\calculation.json` | `31fbaade-260b-4324-bda1-1155f010ede2` |
| T012 | `apply_patch` creates `sample1\output\settlement-report.md` (105 lines) | `e0995e2c-d380-4c49-9acd-1aee7cfd9661` |
| T013 | `view sample1\output\settlement-report.md` after T012 | `b0d35618-9343-427d-b8c2-dca48a1604b1` |
| T014 | `view sample1\output\ledger.json` after T009/T012 | `78f5f5aa-2bb5-4938-8cbd-f0dcddf0c271` |

T010's actual command:

```powershell
python .\settle.py --rules .\sample1\house-rules.json --ledger .\sample1\output\ledger.json --output .\sample1\output\calculation.json
```

It exited successfully and reported `4 transfers (provisional)`.
The final response F001, event `793564b0-3670-4e4b-8013-e5c4b9143d29`,
said: "Created the confirmed-only provisional settlement. Boat attendance and
the exact fuel cost remain unresolved; no payments were made."
P001's prompt event was `da4f6140-2980-4be3-9478-1056dd8448fb`.

### Reviewer quality checks

The actual fresh **reviewagent** run returned **PASS on all seven checks**.
It built REF001-REF006 from the full source snapshot before reading E001-E006,
ran `settle.py` for its independent reference, then ran it again on the unchanged
submitted ledger. Reference and submitted rows matched by expense meaning,
payer, amount, currency, consumers and calculated share allocations; different
reference IDs were not treated as errors.

The saved solver calculation and submission recomputation matched line-for-line.
Both calculated total **1,550,000 paise**, `net_total_paise: 0`, and minimum
transfer count **4**. Tool-produced balances were Arjun **-22,000**, Meera
**-2,000**, Prem **-162,000**, Rahul **-322,000**, Dev **+508,000** paise.
Transfers to Dev were respectively **22,000**, **2,000**, **162,000** and
**322,000** paise. The report matched these calculator outputs.

| Existing quality dimension | Review result and retained evidence |
|---|---|
| Transfers exactly correct | PASS: independent reference, saved output, recomputation and report agree; T009-T012. |
| Duplicates / distinct rides | PASS: M001/R001, M002/M010/R002, M004/R003 and M005/R004 merge; M006 stays separate by date and reverse route; T003, T005-T009, T012. |
| Uncertainty not guessed | PASS: boat M007/M008 and approximate fuel M009 remain excluded with neutral, source-linked questions; T003, T009, T012. |
| Source citations | PASS: each ledger row and unresolved question resolves to supporting chat/receipt IDs; dinner consumers come from M003; T003, T005-T009, T012. |
| Meal categories / USD policy | PASS: food is split among Arjun, Meera, Rahul and Dev; drinks among all five. USD 100 converts to INR 8300 at policy rate; no additional combined dinner row; T002-T003, T007-T012. |
| Calculator / no invented arithmetic | PASS: T010 succeeds, T011 equals the saved output and independent recomputation, and report money matches; T009-T012. |
| Expense coverage | PASS: full-source inventory covers M001-M010 and R001-R004; M011 is chatter. Provisional status and both outstanding questions remain explicit; T003-T008, T012. |

The reviewer also compared the actual T009/T012 write payloads with the
T014/T013 returned content and preserved submitted files. They matched after
newline normalization, establishing that the final readbacks had no intervening
changes. It did **not** call those quality checks inherently wasted work.
Its three ranked hypotheses were a more targeted done/readback plan, a compact
report, and a later model comparison **if administrator policy allows one**.
It did not recommend candidate-only retrieval under this rehearsal's explicit
full-chat prompt.

The isolated solver/reviewer workspaces, raw exports, logs and generated
calculation/reference artifacts were removed after comparison. This section and
the completed scorecard retain the measured values, verdict and trace excerpts;
T001-T014 identify the historical observed events, not files to open after cleanup.
To reproduce the audit, run the capture/review workflow below with a new run ID.

### What this baseline actually suggests testing

**First test Experiment 2's done check:** T013/T014 read back the just-written,
unchanged report and ledger, 163 lines combined, with no subsequent edits,
new evidence or calculator rerun. They may be useful verification; test moving
those checks before the final write rather than simply deleting checks.
The local target is two fewer workflow tool calls (14 to 12 total including
setup), **not** a measured speedup or a promise of two fewer model requests.
Hold all quality checks fixed and remeasure time, requests and usage.

**Then test compact output:** T009/T012 wrote a 58-line ledger and 105-line
report. Preserve citations, duplicate explanations and unresolved questions
while reducing repeated coverage/prose. The 4,394 output tokens are whole-run
usage, not a token count attributable only to those files; savings are unmeasured.

**Batch input retrieval as a separate experiment:** T002-T008 are seven input
tool calls. Rules/chat/directory inventory were already requested together, and
the four receipts were in a parallel batch. A bounded command may reduce call
count, but this trace does not show four sequential receipt requests or prove a
latency gain. The full chat, policy and receipts were each read once; the
calculator ran once. Do not claim repeated input reads or repeated arithmetic.
The measured prompt explicitly required full-chat reading; batching full inputs
is compatible with it, but candidate-only filtering is not. Use the neutral
prompt and a new baseline below before isolating targeted retrieval.

**SAY:**
> "The baseline gave us a concrete place to start: two final artifact reads,
> and a fairly long report. We have not shown that retrieval helps eleven
> messages, or that a smaller model is sufficient. Those are experiments,
> not conclusions from this one scorecard."

## Presenter run sheet

Prepare and review a rehearsal baseline before the session. Use the saved
scorecard and trace in the 0-6 minute diagnostic segment of Workshop 4; collecting
and reviewing a fresh run may take longer than that segment.

| Step | DO | SAY / ASK |
|---|---|---|
| Capture | Run the unchanged Workshop 3 agent in a fresh session; record its trace and elapsed time. | "These are observations, not the agent's estimates." |
| Challenge | In a separate fresh session, run `reviewagent` on the frozen evidence. | "Try to disprove the ledger, not just check that balances add to zero." |
| Inspect | Open the completed scorecard and `review\findings.md`; jump to each cited solver event. | "Which field tells us this matters, and which event explains it?" |
| Decide | Choose one of the plan's three experiments from a supported finding. | "Change one thing; keep the correctness threshold." |

## 1. Add and select the independent reviewer

`reviewagent.md` is the full instruction contract.
`.github\agents\reviewagent.agent.md` is its discovery profile, matching the
existing Workshop 3/4 arrangement. Keep both files at these locations. The
root `.md` alone does not make the agent selectable.

In VS Code, open the repository root, start a **new** Copilot Chat session and
select **reviewagent** from the agent picker. If absent, check the profile's
`.agent.md` suffix and reload the window. Confirm read/search, edit and execution
tools are available. It needs the existing Python calculator, not new packages.

For standalone Copilot CLI, start from the repository root:

```powershell
copilot --agent reviewagent
```

Use the review prompt in section 4. Do not ask the settlement agent to become
its own reviewer in the existing conversation. The reviewer gets raw sources
and the actual solver contract, but not `context.md`, `stage1context.md` or an
instructor answer key. Its findings remain subject to instructor review.

## 2. Capture a baseline without optimizing it first

To reproduce this rehearsal, use `workshop3finalagent` and the prompt from
`instructions.md`, unchanged.
Record the exact prompt as `prompt.txt`; keep the model, policy, tools and client
fixed for context/work comparisons. Do not compare an Auto baseline with a
fixed-model run and attribute the difference solely to retrieval.

For a controlled targeted-retrieval experiment, instead establish a **new**
Workshop 3 baseline with this common task prompt, then keep it identical for
the staged variants selected through the agent picker:

```text
Settle the trip in sample1 according to the selected agent's contract.
Use the authoritative policy and source evidence; do not guess missing amounts
or participants. Write the confirmed-only ledger, use settle.py for arithmetic,
and write a source-linked provisional report with duplicates, unresolved
questions and expense coverage under sample1\output. Do not modify inputs.
```

The original rehearsal prompt names Workshop 3 and requires full-chat reads.
Do not reuse that wording with candidate-only retrieval or compare a
changed-prompt run against the recorded 61.149-second baseline as though only
retrieval changed.

`sample1` is sufficient to rehearse capture and review. Only that small trip
currently exists. For the plan's scale challenge, the presenter must separately
prepare the fictional large trip (12 people, roughly 300 messages) and unseen
holdout with the same input contract. Preserve judgment cases, including
no-amount attendance/consumption messages and distant clarification messages.
Do not multiply bills by copying IDs or accidentally create duplicate charges.
Run baseline and optimized configurations on the **same** large trip. Do not
compare small-trip baseline time with large-trip optimized time.

### VS Code trace capture

Before running, enable the logging setting appropriate to the harness:
`chat.agentHost.agentDebugLog.enabled` for Agent Host sessions, or
`github.copilot.chat.agentDebugLog.fileLogging.enabled` for Local harness
sessions. Capture is not retroactive; record unavailable features as `not shown`.

Open **Show Agent Debug Logs** from the Chat overflow menu, or
**Developer: Open Agent Debug Panel** from the Command Palette. Verify the
session breadcrumb identifies the **solver**, not the reviewer.

- **Summary:** capture reported model turns, tool calls, tokens and errors.
- **Logs:** filter tool calls and LLM requests. Expand relevant events to
  preserve exact inputs and returned outputs, not just the collapsed label.
- **Chat Debug view:** inspect the affected request's Context and prompt/tool
  payload when diagnosing oversized context. Use only fields actually shown.

Copy/export the solver conversation and relevant expanded debug events. Save
the text as `trace.md` in the run directory below; keep raw exports alongside it.
VS Code's **Copy All** preserves conversation/tool text; **Chat: Export Chat...**
saves JSON. Neither substitutes for unshown timing/token metadata: copy the
Summary and relevant debug details too.

Give each actual event a stable heading such as `## T001` when the export lacks
IDs. Preserve event order, tool name, exact file/range/command, output and shown
timestamp/duration. These headings are references to observed events, **not**
scripted events that the solver is expected to produce.

Start a stopwatch when submitting the solver prompt and stop at its final
response. Include approval/wait time consistently and note it. Review and
snapshot time are outside the solver measurement.

### Optional CLI capture

In an interactive solver session, `/session info` identifies the session,
`Ctrl+O` expands timeline tool details, and `/share file session <path>` exports
the session. Save to a local file; do not publish the evidence.
When starting a run, `--usage-output-file <path>` can record final usage JSON
when that solver session ends. Keep this file with the run and label its units.
Do not substitute `/context` occupancy for cumulative run tokens or treat
premium/billing requests as the number of actual LLM calls.

## 3. Freeze the solver inputs and outputs

Immediately after the run, before another solver invocation overwrites outputs,
create a uniquely named archive. From the repository root:

```powershell
$trip = '.\sample1'
$run = "$trip\output\runs\W3-B01"
if (Test-Path $run) { throw 'Choose a new run ID; do not overwrite evidence.' }
New-Item -ItemType Directory -Path "$run\inputs\receipts","$run\submission" | Out-Null
Copy-Item "$trip\chat.txt","$trip\house-rules.json" "$run\inputs"
Copy-Item "$trip\receipts\*.txt" "$run\inputs\receipts"
Copy-Item "$trip\output\ledger.json","$trip\output\calculation.json","$trip\output\settlement-report.md" "$run\submission"
Copy-Item '.\workshop3finalagent.md' "$run\solver-contract.md"
Copy-Item '.\.github\agents\workshop3finalagent.agent.md' "$run\solver-profile.agent.md"
```

Save the exact prompt, trace and observations to that run directory:

```text
sample1\output\runs\W3-B01\
  inputs\                 chat.txt, house-rules.json, receipts\*.txt
  submission\             ledger.json, calculation.json, settlement-report.md
  solver-contract.md      exact contract used for this run
  solver-profile.agent.md exact discovery profile used
  prompt.txt              exact solver prompt
  trace.md                event IDs/headings and expanded event details
  observations.md         measured values plus their sources
  ...                     any raw chat/debug/usage exports
  review\                 created by reviewagent, never by the solver
```

In `observations.md`, record date/pair/run ID, solver session identity,
client/version, selected model (Auto if applicable), input/policy identity,
start/end or elapsed time, inclusion of waits, and any shown requests/calls,
tokens/credits. For every value name its source: Summary screenshot, raw usage
field, trace event or presenter stopwatch. Use `not shown` for missing metrics;
record interruptions and human corrections. Never type illustrative numbers
into a real baseline.

For optimized runs, use a fresh run ID such as `W4-E1-01` and snapshot the actual
experimental contract/profile, not Workshop 3's files. Keep completed run archives
and reviewer answers outside the next solver's clean workspace. The archive's
input snapshot lets the reviewer resolve original `sample1\...:M001` citations
without relying on later modifications.

## 4. Ask the adversarial agent to create the scorecard

In the fresh **reviewagent** session, paste:

```text
Adversarially review the solver run W3-B01 for trip sample1.
The preserved run is sample1\output\runs\W3-B01.
Follow reviewagent.md. Establish a reference from the snapshotted rules, full
chat and all receipts before inspecting the submitted answer. Try to falsify
each existing quality check; use settle.py for reference and recomputation.
Fill the existing sample1\scorecard.md dimensions using only this solver run's
observed evidence. Mark missing metrics not shown and unverified checks
NOT REVIEWED. Exclude all reviewer calls, time and usage.
Write the archived scorecard and findings under this run's review folder.
For each proposed optimization, cite exact trace event IDs/headings and name
the scorecard field to remeasure. Do not repair the submitted artifacts.
```

The reviewer writes `review\reference-ledger.json`,
`review\reference-calculation.json`, `review\recomputed-submission.json`,
`review\findings.md` and `review\scorecard.md`. It updates the existing
`sample1\scorecard.md` Observation cells for that run without changing dimensions.
The archived scorecard remains the baseline when the next review updates the
live scorecard.

**DO:** Have the instructor inspect failed/unverified checks and source-linked
counterexamples. A calculator success or zero net balance cannot validate a
guessed ledger. If reviewer and presenter disagree, adjudicate against raw
evidence and record the correction before accepting quality.

## 5. Use the scorecard to select exact traces, not a fashionable optimization

These are lookup targets, **not claims that a particular baseline contains
them**. The reviewer must replace them with actual event references.

| Existing scorecard dimension | Exact events/payloads to inspect | Supported experiment |
|---|---|---|
| Requests / tool calls; elapsed time | First full read of `chat.txt` and any later overlapping read of unchanged lines; adjacent LLM requests; shown durations. Cite both reads. | Experiment 1: candidate lines plus neighbours instead of repeated full context. |
| Requests / tool calls; elapsed time | Separate reads of `house-rules.json` and each `receipts\*.txt`; any repeated policy/receipt read. Distinguish required initial reads from redundant reads and batching opportunities. | Experiments 1/2: one bounded read-only retrieval command, rules read once. |
| Tokens / usage; elapsed time | Ledger/report write events and final reply; actual output-token fields where shown. Identify echoed JSON/report text or excessive narrative, not hidden reasoning. | Experiment 2: compact ledger/report and terse final reply without losing sources. |
| Requests / tool calls; human corrections | Every `settle.py` command, its exit/result and intervening ledger edits. Separate necessary validation repair from repeated successful calculations of an unchanged ledger. | Experiment 2: one valid final calculation and an explicit done check. |
| Elapsed time; requests / calls | Successful calculation/report write followed by further reads, rewrites or requests without new evidence. Cite the completed artifact and subsequent events. | Experiment 2: stop after coverage and success checks, not open-ended rechecking. |
| Model selected; usage; elapsed time | Actual model identity and LLM request timing/token fields on otherwise identical optimized runs. Record unavailable model details. | Experiment 3: compare models only after context/work changes are controlled. |
| All quality dimensions | Source IDs beside ledger/calculation/report mismatches and the solver's relevant selection/write event. Especially inspect `M003`, `M007`/`M008`, `M009`, `M006` and dinner receipt `R002` in `sample1`. | Reject an apparent speedup caused by dropping judgment evidence or guessing. |

**SAY:**
> "The scorecard tells us whether the run is correct and what it cost. The trace
> tells us what to change. A necessary read is not a defect, and a shorter run
> with the wrong ledger is not an optimization."

If no redundant work is demonstrated, say so. `sample1` is small enough that
retrieval may retain almost everything; do not manufacture a need for it.
A complete full-source reviewer audit must catch omissions that the optimized
agent's candidate-only coverage check cannot see.

## 6. Hand off to the plan's controlled experiments

Use the common task prompt above for a new controlled baseline, then keep that
prompt, input/policy, model and tools fixed. The recorded rehearsal remains a
demonstration, not the comparator for a different prompt. For Experiment
1, change only retrieval; for Experiment 2, hold that retrieval fixed and change
the work/output/done plan; for Experiment 3, change only the model. The supplied
`workshop4finalagent.md` combines Experiments 1 and 2: comparing that final agent
directly to Workshop 3 measures their **combined** effect, not either separately.
Use staged participant copies when isolating changes.

After each solver run, repeat capture, snapshot and fresh adversarial review
with the same `reviewagent` contract. Compare the archived scorecards side by
side. Speed gains count only if every quality check remains `PASS`, transfers
are exactly correct and no amount is invented. Do not rank uncertified runs or
missing usage measurements as cheap. Pool repeat timings across pairs rather
than claiming significance from one noisy run.

Finally review the chosen configuration on the unseen trip, without exposing
prior reference ledgers or instructor answers. Present one before/after field,
the exact solver events that explain it, and the quality checks that held.

## Sources for the workflow

- Repository: `workshop-plan.md` (experiments, acceptance rule),
  `workshop3finalagent.md` (accuracy contract), `workshop4finalagent.md`
  (retrieval/work changes), `sample1\scorecard.md` (existing dimensions),
  `instructions.md` (solver invocation), and `stage1context.md` (presenter format).
- VS Code diagnostic views and capture:
  [Debug chat interactions](https://code.visualstudio.com/docs/agents/agent-troubleshooting/chat-debug-view),
  [Debugging agent work](https://code.visualstudio.com/learn/foundations/debugging-and-whats-happening-behind-the-scenes),
  [Export or copy a conversation](https://code.visualstudio.com/docs/agents/run/sessions/session-history).
- CLI export/usage instructions checked against this build's documentation for
  `/share`, `/session`, timeline expansion, `/context` and `--usage-output-file`.
