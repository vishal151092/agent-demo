---
name: workshop4finalagent
description: Settle a fictional trip with the Workshop 3 accuracy contract, using less context, fewer calls and shorter output; settle.py does all arithmetic.
tools: ['read', 'search', 'edit', 'execute']
---

<!-- The .agent.md suffix enables discovery in VS Code and Copilot CLI.
     Keep the complete commented contract in the requested root-level file.
     No model is pinned: model choice is the Workshop 4 experiment variable. -->
Before acting, read `workshop4finalagent.md` at the repository root and follow its
entire contract, including the tool-call budget. Use the trip folder named in the
prompt (default `sample1`). Write only that trip's `output` folder. Do not modify
inputs or calculate monetary results yourself.
