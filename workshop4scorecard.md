# Workshop 3 baseline scorecard

Fill after an agent run. Use an independent instructor review for quality, not
the agent's self-assessment. Do not put an answer key in the agent input folder.

| Field | Observation |
|---|---|
| Date / pair / run identifier | 2026-11-21; presenter rehearsal; W3-TEST-20261121. Solver session ea3871b5-4376-4433-9b82-1a7aa6556604. |
| Client and version | Copilot CLI 1.0.114; fresh isolated solver and reviewer workspaces. |
| Model selected | Auto, administrator-managed; solver usage export reported gpt-6.1-terra. No fixed-model override. |
| Input folder and unchanged policy | sample1; input SHA256 checks passed; 5 people, 11 messages, 4 receipts; unchanged fixed USD policy rate. |
| Confirmed-only transfers exactly correct | PASS - reviewagent's independent reference and submission recomputation match all paise balances, totals and four minimum transfers; report agrees. See workshop4context.md, Reviewer quality checks; T009-T012. |
| Duplicates merged; distinct same-price rides retained | PASS - four source merges verified; M001 and M006 remain distinct dated routes. See Reviewer quality checks; T003, T005-T009, T012. |
| Boat attendance and exact fuel cost questioned, not guessed | PASS - M007-M009 excluded with source-linked boarding and exact-fuel questions. See Reviewer quality checks; T003, T009, T012. |
| Every ledger row and unresolved item cites evidence | PASS - cited IDs exist and jointly support each payer, amount and consumer set. See Reviewer quality checks; T003, T005-T009, T012. |
| Dinner category split and USD conversion correct | PASS - itemized consumers and policy conversion verified by the independent reference and calculator; no combined dinner charge. See Reviewer quality checks; T002-T003, T007-T012. |
| Calculator called successfully; no invented arithmetic | PASS - T010 exited successfully; T011 matches saved calculation and recomputation; reported money matches tool output. See Reviewer quality checks; T009-T012. |
| Expense coverage complete | PASS - independent full inventory covers M001-M010 and R001-R004; M011 is chatter. See Reviewer quality checks; T003-T008, T012. |
| Quality pass (all checks above pass) | PASS - fresh adversarial reviewagent run, followed by comparison of its reference/recomputed artifacts. Boat/fuel still require human answers; no payment authorization. |
| End-to-end elapsed time | 61.149 seconds, recorded prompt to final response; no approvals or interruptions. Startup/export and reviewer excluded. See workshop4context.md, Recorded measurements; P001 and F001 timestamps. |
| Model requests / tool calls (observed) | 9 model requests from solver usage.json; 14 distinct executed solver calls, including 1 contract setup and 13 workflow calls. T001-T014 preserved in workshop4context.md; reviewer excluded. |
| Tokens / Copilot usage or credits (if shown) | Solver: 110208 input, 4394 output, 91220 cache-read, 18961 cache-write, 539 reasoning tokens as reported; 3.52 displayed AI credits. Source: solver usage export and console, summarized in workshop4context.md; categories are not added again. |
| Human corrections / notes | None. Rehearsal evidence and review findings retained in workshop4context.md; temporary run artifacts removed. No optimized comparison or reliable per-tool latency shown. First experiment: assess final artifact readbacks T013/T014 without removing quality checks. |

No speed result counts unless quality passes. Mark unavailable metrics `not
shown`, not zero. Keep the same prompt, policy, and data for baseline comparisons.
