# Workshop 4 final agent scorecard

Fill after an agent run. Use an independent instructor review for quality, not
the agent's self-assessment. Do not put an answer key in the agent input folder.

| Field | Observation |
|---|---|
| Date / pair / run identifier | 2026-11-21; pair not shown; presenter rehearsal; W4-FINAL-20261121. |
| Client and version | GitHub Copilot CLI 1.0.114. |
| Model selected | Auto, administrator-managed; usage export reported gpt-6-luna. |
| Input folder and unchanged policy | sample1; T002 policy matches the snapshot; source/snapshot SHA-256 equality verified, digest not shown. Prior-run equality not shown. |
| Confirmed-only transfers exactly correct | PASS - reference and recomputation agree on total, all balances and minimum count; report transfers match. See reviewer evidence below. |
| Duplicates merged; distinct same-price rides retained | PASS - M002/M010/R002 is one dinner; M001/R001 and M006 are distinct dated routes. T002, T003, T006. |
| Boat attendance and exact fuel cost questioned, not guessed | PASS - M007-M009 stay excluded and have specific questions and confirmers. T002, T003, T006. |
| Every ledger row and unresolved item cites evidence | PASS - E001-E006 and both questions cite snapshot IDs supporting their claims. T002, T003, T006. |
| Dinner category split and USD conversion correct | PASS - M003/R002 support separate consumers; M004/R003 and policy support the USD conversion. T002-T005. |
| Calculator called successfully; no invented arithmetic | PASS - solver's T004 call exited 0; saved calculation and report agree with recomputation. |
| Expense coverage complete | PASS - full M001-M011 and R001-R004 inventory accounted for; noncandidate context caveat below. |
| Quality pass (all checks above pass) | PASS - all seven checks reviewed and passed by reviewagent; subject to instructor approval. |
| End-to-end elapsed time | 41.832 seconds, P001 to F001; includes ordinary waiting, no interactive approvals or interruptions; excludes snapshotting and review. |
| Model requests / tool calls (observed) | 7 model requests from solver usage export; 6 distinct executed calls, T001-T006, including one setup call; reviewer calls excluded. |
| Tokens / Copilot usage or credits (if shown) | gpt-6-luna: 89810 input, 4754 output, 72045 cache-read, 17744 cache-write, 2388 reasoning tokens; `tokenDetails.input` 21 (reported categories overlap). 0.37 AI Credits displayed; raw `totalNanoAiu` 372228500. |
| Human corrections / notes | None for this run. No controlled comparison shown. The report's one noncandidate was actually returned as context; see coverage caveat below. |

No speed result counts unless quality passes. Mark unavailable metrics `not
shown`, not zero. Keep the same prompt, policy, and data for baseline comparisons.

## Preserved reviewer evidence

The fresh adversarial reviewer built a reference from the complete snapshotted
policy, chat and receipts **before** reading the submitted settlement. It then
recomputed the submitted ledger with `settle.py`. The saved calculator output
matched the recomputation in all JSON fields; the independently reconstructed
rows matched the submission's amounts, payers, currencies and share allocations.
The separate reviewer session displayed **24.94 AI credits**, excluded from the
solver's 0.37-credit measurement.

The reviewer accounted for M001-M010 and R001-R004, with M011 as non-expense
chatter. It verified that M001/R001 merge, M006 is a separate return cab,
M002/M010/R002 describe one itemized dinner, M004/R003 and M005/R004 merge,
and the boat (M007/M008) and approximate fuel (M009) remain excluded with
questions. Its reference and submission both calculated **1,550,000 paise**
confirmed spend, balances Arjun -22,000, Meera -2,000, Prem -162,000, Rahul
-322,000, Dev +508,000 paise, and four minimum transfers to Dev. The report
matched those values and states that the settlement is provisional.

**Coverage caveat:** the filter returned all 13 nonblank chat lines. Twelve
were candidates (M001-M011 and the dated synthetic header); the other fictional
data header was returned as neighboring context. The report's "1 line skipped"
means noncandidate, not withheld from the tool result. The reviewer found no
omitted expense and passed coverage, subject to instructor adjudication.

## Preserved solver trace

The following are actual events from the isolated solver session
`81e478cb-9d18-4fb2-9b16-7a7a1d887946`. All six tool calls completed
successfully. The temporary raw trace and generated run files were removed
after review; event IDs and findings are retained here.

| Event | Observed action | Start-event ID |
|---|---|---|
| T001 | Read `workshop4finalagent.md` (setup). | `71462e9a-efb5-4ef6-9fc9-2f36c9aeb45b` |
| T002 | One PowerShell prefilter read the policy, candidate chat lines with neighbors, and all four receipts. | `f73e4590-8b2b-439d-a54b-8a979ac8bd33` |
| T003 | Wrote `sample1\output\ledger.json` (8 lines). | `dd43dcf2-9a3c-4330-94d6-f861dda26325` |
| T004 | Ran `python .\settle.py --rules .\sample1\house-rules.json --ledger .\sample1\output\ledger.json --output .\sample1\output\calculation.json`; exit 0. | `79c7f89e-6d87-46fb-8a7b-b1890a40d638` |
| T005 | Read `sample1\output\calculation.json` (253 lines). | `432d9636-aac7-486b-9d76-a2857bd88f8d` |
| T006 | Wrote `sample1\output\settlement-report.md` (61 lines). | `bac8c2a7-91e7-4a05-864a-4248cb0c1f8a` |

Prompt event P001 `6107e2f3-4d37-4b93-931b-79970d249e22` was recorded at
`2026-11-21T06:39:25.504Z`; final response F001
`0e81fc94-9cb7-4fea-a72c-904a8250a46d` at `2026-11-21T06:40:07.336Z`.
Process launch-to-exit was 51.668 seconds including startup and export, not the
41.832-second prompt-to-final measurement. Tool timestamps were projected
together; individual call durations are not available.

The earlier `workshop4scorecard.md` rehearsal used a different prompt and Auto
resolved a different model. These two single runs are not a controlled comparison;
their differences do not establish an optimization's causal speed or cost savings.
