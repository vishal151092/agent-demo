# Workshop narrative: "The Goa trip is over. Who owes whom?"

**Build an agent that turns a messy group-trip chat and receipts into a fair, explainable settlement, then make it faster and more economical without reducing accuracy.**

The story: five friends just returned from a weekend trip. Expenses are spread across a WhatsApp export, a few receipt notes, and half-remembered messages: "I paid for the cab, add it," "Priya only had drinks," and "Wait, did anyone log the dinner?" Someone always ends up spending an evening sorting it out. Everyone has been that person, or has owed money to that person.

**Platform:** VS Code with GitHub Copilot. Participants build a custom agent (`.github\agents\settle.agent.md`) with instructions and a small set of selected tools. Copilot runs the agent loop.

## The specific task

The agent gets three inputs: a chat export, a folder of receipt text files, and a short "house rules" policy. It has to produce a **settlement report** that includes:

- A ledger of expenses showing who paid, the amount, who shares the cost, and the source message or receipt.
- Flags for duplicates and ambiguous items, with the evidence for each.
- Clarification questions for the group where the inputs can't settle an item.
- Final balances and the minimum set of transfers, such as "Arjun pays Meera ₹1,240."

Seed the data with judgment calls like these:

| Chat or receipt | What participants should notice |
|---|---|
| "Paid 3,200 for dinner" plus a receipt for ₹3,200 | Two sources describe one expense. Count it once. |
| "Priya only had drinks" | The split isn't equal. The agent should apply the policy rather than guess. |
| "Rahul skipped the boat ride" (said by someone else) | This is reported, not confirmed. Flag it and ask. |
| "Fuel ~2k" | The amount is approximate. Ask for the exact figure instead of making one up. |
| A receipt in USD for a hostel booking | A currency rule is needed. The rate belongs in the policy. |

**Why use an agent instead of a script?** Interpreting the chat, matching messages to receipts, and deciding when to ask are all judgment calls. The arithmetic isn't. Give the agent a tiny `settle.py` tool that computes balances and transfers from a ledger, and require the agent to use it. **Key lesson: the model reasons, tools calculate.** An LLM doing mental arithmetic on money is a bug.

---

## Workshop 3: Build an agent you can trust (45 minutes)

**Learning outcome:** participants can explain the agent loop and build an agent that completes a bounded task from evidence, with tools handling the deterministic work.

| Time | Activity | Concept |
|---|---|---|
| 0–5 min | Tell the trip story. Pairs settle 6 messages by hand and compare answers. They'll disagree. | The task involves real judgment. |
| 5–10 min | Paste the chat into plain chat and ask "who owes whom?" Check the math and the duplicates. | A fluent answer isn't a correct one. Hallucinated arithmetic. |
| 10–18 min | Fill in the agent scaffold: goal, house rules, ledger format, allowed tools (read files, run `settle.py`, write report), and stop conditions. | Instructions, context, tools, and boundaries. |
| 18–28 min | Run the agent and watch it read the chat, open receipts, build the ledger, call the tool, and write the report. | The loop: **observe → decide → act → check → repeat or stop.** |
| 28–36 min | Add the tricky cases: the hearsay exclusion and the approximate fuel cost. Pairs fix one instruction and rerun. | Uncertainty, asking for clarification, and keeping a human in the loop. |
| 36–42 min | Run it on a second trip dataset and score the result against a rubric. Record the baseline. | Evaluation and observability. |
| 42–45 min | Compare results across pairs and set up the next challenge. | Correct is necessary but not sufficient. |

### The agent contract

> Build an expense ledger from the chat and receipts using the house rules. Cite the source for every entry. Merge duplicates only when amount, payer, and context match, and explain why. Don't guess amounts or participants. List those as questions instead. Compute balances only by running `settle.py`. Write the report, check that every expense is either in the ledger or listed as a question, and stop. Don't modify the source files or message anyone.

**Make the roles explicit:** the model interprets, tools compute and write, the harness runs the loop, and the group (the human) answers questions and approves the settlement.

**Deliverable:** a working agent, a settlement report, and a baseline scorecard.

### The segue

> "That worked for a weekend with 5 people. Now it's a 10-day trip with 12 people and 300 messages, or a flat-share running all semester. Do you need a bigger model, a smaller one, or just less wasted work? Measure first."

---

## Workshop 4: Make the same agent efficient (45 minutes)

**Learning outcome:** participants run controlled experiments to cut latency and model usage while holding a quality threshold.

| Time | Activity | Concept |
|---|---|---|
| 0–6 min | Run the baseline on the large trip and inspect the trace in Agent Debug Logs. Look for re-reading the whole chat, opening every receipt, verbose reasoning, and repeated tool calls. | Diagnose before optimizing. |
| 6–16 min | **Experiment 1: less context.** Add a pre-step that greps the chat for messages containing amounts and currency, so the agent reads only candidate lines plus their neighbours. Keep the same model. | Targeted retrieval and context efficiency. |
| 16–25 min | **Experiment 2: less work.** Read the rules once, use a compact ledger format, call `settle.py` once at the end, and add a clear done check. | Tool-call overhead, output length, and stopping conditions. |
| 25–35 min | **Experiment 3: change the model.** Compare two models on the optimized setup in fresh sessions, keeping prompts, data, and tools identical. Optionally route only flagged items to the stronger model. | Model capability vs. latency and usage, and when escalation makes sense. |
| 35–41 min | Run the chosen configuration on an unseen trip. | Holdout evaluation: don't overfit to the examples. |
| 41–45 min | Each pair presents its configuration and one tradeoff it accepted. | Optimize the whole system, not just the model choice. |

### Scorecard used in both workshops

| Quality | Efficiency |
|---|---|
| Final transfers correct (vs. answer key) | End-to-end time |
| Duplicates handled correctly | Model requests and tool calls |
| Ambiguous items flagged, not guessed | Tokens, where shown |
| Every ledger entry cites a source | Copilot usage or credits reported |

**Acceptance rule:** transfers must still be exactly correct, with no invented amounts. Speed gains count only if quality holds. Pool timings across pairs, since single runs are noisy.

**Deliverable:** an optimized agent and a before/after scorecard explaining the tradeoff.

---

## Prep

Starter repo contents:

- 3 synthetic trips: small (Workshop 3), large (Workshop 4), and unseen (holdout).
- Receipt text files and a house-rules file.
- `settle.py` with tests.
- The agent scaffold and the scorecard.
- Answer keys, kept outside the agent's workspace.

Use fictional names and amounts. Ask participants to install VS Code, sign in to Copilot, and open the repo beforehand. Keep checkpoint branches so stragglers can catch up.

**Out of scope:** real payment apps, live WhatsApp integration, MCP setup, multi-agent systems, and UI.

**Backup task with the same structure:** "Tailor my job applications." The agent matches a resume to 10 postings, flags requirements the participant doesn't meet instead of faking them, and drafts tailored bullet points.

## References

- [VS Code: Custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- [VS Code: Choose a model](https://code.visualstudio.com/docs/agents/guides/choose-a-model)
- [VS Code: Agent debug view](https://code.visualstudio.com/docs/agents/agent-troubleshooting/chat-debug-view)
