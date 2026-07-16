# Staged Session Prompts

Use one prompt per session or terminal turn. Replace `<task-id>` and project
paths with local values. The purpose is deliberate human review between stages,
not a longer automated chain.

## 1. Analysis

```text
Use the local AGENTS.md and the ai-assisted-qa skill for task <task-id>.
Perform Stage 1: analysis only. Read the task, acceptance criteria or DoD,
relevant code, existing tests, related artifacts, and route memory. Produce the
complete analysis in chat first. Do not start the algorithm, automated checks,
manual test case, or report.
```

## 2. Algorithm

```text
Use the local AGENTS.md and the ai-assisted-qa skill for task <task-id>.
Perform Stage 2: verification algorithm only. Use the approved analysis as a
source of truth. Check route memory and similar proven routes before new route
discovery. Define tools, evidence, stop conditions, and user versus agent
actions. Produce the complete algorithm in chat first. Do not start automated
checks, the manual test case, or the report.
```

## 3. Automated Evidence

```text
Use the local AGENTS.md and the ai-assisted-qa skill for task <task-id>.
Perform Stage 3: automated evidence only. Use the approved analysis and
algorithm. Reuse project-native tests and approved routes. State what each
check proves, run only authorized non-destructive checks, and record factual
results or exact blockers. Do not start the manual test case or final report.
```

## 4. Manual Test Case

```text
Use the local AGENTS.md and the ai-assisted-qa skill for task <task-id>.
Perform Stage 4: manual test case only. Use the approved analysis, algorithm,
and automated evidence. Cover requirements and remaining changed-risk scope.
Write concrete preconditions, actions, expected results, and evidence needs.
Do not invent execution results or final-report conclusions.
```

## Final Reporting

Request reporting separately after actual automated and manual results exist.
The report must map each requirement or DoD item to evidence, blockers, and
remaining risk.
