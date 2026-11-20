# Workshop 3: run the trip-settlement agent

This implements the **first session**, Workshop 3 in `workshop-plan.md`, not the
Workshop 4 optimization exercise. All trip data is fictional.

## Files and prerequisites

`sample1` contains a chat export, four receipt notes, the authoritative
`house-rules.json`, and a blank baseline scorecard. The first six message IDs are
the opening hand-settlement exercise; M007-M010 introduce uncertainty and repeats.
There are no resolved answers hidden in this input folder.

`workshop3finalagent.md` is the commented agent contract. The small
`.github\agents\workshop3finalagent.agent.md` profile makes it selectable.
`settle.py` is a standard-library-only Python 3 calculator with focused tests.
Have Python 3.10+ available as `python` (or substitute `py -3` in all commands).
Have VS Code with GitHub Copilot signed in, or GitHub Copilot CLI with an active
Copilot plan and PowerShell 6+ on Windows.

Open a PowerShell terminal at this repository's root (not inside `sample1`):

```powershell
python --version
python -m unittest discover -s tests -v
```

## VS Code

1. Open the repository folder in VS Code and open Copilot Chat.
2. Select **workshop3finalagent** in the agents dropdown. The discovery profile
   must be under `.github\agents` and end in `.agent.md`; the root `.md` file alone
   is not the selectable profile.
3. Verify the tools include file read/search, edit, and shell execution; then
   paste the prompt below. Review tool calls as the agent reads inputs, writes
   its ledger, runs Python, checks the result, and writes its report.

```text
Settle the trip in sample1 using the workshop3finalagent contract.
Read the house rules, full chat and all receipt notes. Write the confirmed-only
ledger, run settle.py, and write a source-linked provisional settlement report
under sample1\output. Include duplicate evidence, unresolved questions and
expense coverage. Do not modify inputs or guess missing information.
```

If it does not appear, confirm the opened folder is the repository root and
reload the VS Code window. Inspect the profile's tool configuration if required
tools are unavailable; do not let the model substitute mental arithmetic.

## GitHub CLI (`gh`) or standalone Copilot CLI

With a current GitHub CLI that supports `gh copilot`, start interactively from
the repository root. `--` passes the following flags to Copilot rather than `gh`:

```powershell
gh copilot -- --agent workshop3finalagent
```

Trust the repository when prompted, sign in with `/login` if needed, and paste
the same prompt. Approve the needed ledger/report writes and Python calculation.
If your installed `gh` does not have this subcommand, use standalone Copilot CLI:

```powershell
copilot --agent workshop3finalagent
```

Alternatively start `copilot`, enter `/agent`, select `workshop3finalagent`, and
paste the prompt. If standalone Copilot is missing, install it on Windows with
`winget install GitHub.Copilot`, then reopen the terminal.
These workflows use the custom-agent CLI, not legacy `gh copilot suggest` or
`gh copilot explain` command suggestion workflows.

## Outputs and human review

The agent creates (rather than reading a supplied solution):

```text
sample1\output\ledger.json
sample1\output\calculation.json
sample1\output\settlement-report.md
```

Reproduce its calculation without a model:

```powershell
python .\settle.py --rules .\sample1\house-rules.json --ledger .\sample1\output\ledger.json --output .\sample1\output\calculation.json
```

The ledger uses decimal-string amounts and integer sharing weights. The tool
converts currencies, rounds to paise, allocates shares, and finds the exact
minimum number of transfers for up to twelve participants. It does not decide
whether evidence is true or a duplicate; that is the agent's job.

Check that dinner's food and drinks are separate, repeated dinner/cab/hostel/
breakfast sources are not double charged, the return cab remains a distinct
expense, USD uses the policy rate, and uncertain boat attendance and approximate
fuel are excluded with questions. A report is **provisional**, not permission
to pay. Supply real clarifications in a later chat turn and rerun before approval.

Record the baseline in `sample1\scorecard.md`: actual runtime, observed requests
and calls, usage where available, and independently reviewed quality. Keep any
instructor answer key outside the workspace. Use a fresh session for comparison
runs; this sample does not supply Workshop 4's large or unseen trips.

## Documentation

Run syntax and agent configuration checked against official documentation:

- [VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- [Custom agent configuration and tool aliases](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Using Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/overview)
- [GitHub CLI Copilot launcher](https://cli.github.com/manual/gh_copilot)
- [Installing Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli)
