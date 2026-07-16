# Adoption Guide

## Start With One Real Task

Do not introduce the workflow across an entire backlog. Select one task with a
clear risk: a state transition, API contract, data migration, UI flow, or
cross-service change. Keep the task's artifacts in its own directory.

```text
qa/<task-id>/
```

Install the skill, add the project rule, and use the staged-session prompts.
Run analysis first; inspect it before asking for the algorithm. Run automated
checks, the manual test case, and the final report only in later, explicit
sessions.

## Keep Human Gates Between Stages

The engineer controls the sequence:

1. Ask only for analysis and review what the agent understood.
2. Ask only for the algorithm and review tools, routes, and stop conditions.
3. Authorize automated checks only after the route is accepted.
4. Ask for the manual test case after automated scope and factual evidence are known.
5. Request a final report only after actual execution, then verify that it
   reproduces approved manual steps and lists every relevant artifact.

This prevents an early misunderstanding from being copied into every later
artifact. Use the copyable prompts in
[`staged-session-prompts.md`](../skills/ai-assisted-qa/references/staged-session-prompts.md).

## Create Private Route Memory

Add a private `qa/route-atlas.md` to the target project. Before the algorithm
phase, the agent searches it and related approved algorithms. When it proves a
new reusable route, it synchronizes the atlas as `compare -> reuse/update/add`.
Do not store volatile data, credentials, private URLs, or one-off root causes in
the atlas. See the [route-memory protocol](../skills/ai-assisted-qa/references/route-memory.md).

## Review the Analysis Before Execution

The highest-value review point is before the first test run. Check that:

- requirements and DoD are complete;
- the agent read the changed code and existing tests;
- every additional scenario has a stated risk reason;
- important missing information is a blocker or question, not an assumption.

Correct the algorithm at this point. It is cheaper than discovering a missing
surface after a report is written.

## Let Existing Tooling Do the Execution

The skill does not replace your unit runner, API client, browser suite, data
validator, or CI. It tells the agent how to choose and document the right one.
Use the repository-native command or approved environment. Store factual output
and human-readable evidence according to your project's policy.

## Keep Manual Work Explicit

Manual scenarios should answer questions that are not covered by the available
automation. Keep preconditions, entry points, one action, and one observable
expected result explicit. Record the environment, actual result, evidence, and
blocker only after execution. This prevents a report from implying that browser,
visual, or timing behavior was checked when only a service-level assertion ran.

## Treat the Report as a Traceability Check

The final report is not a short release note. It copies approved manual
test-case actions and expected results in the same order, adds factual actual
results, records behavior-proving automated checks, lists the full artifact
set, and preserves the original DoD wording. Before saving or publishing, run a
mechanical comparison with the approved test case. A missing or blocked result
stays missing or blocked in the report.

## Improve From Real Friction

After the task, review the five artifacts with the tester or reviewer. Add a
new risk pattern or template only when it solves a repeated problem. Keep
project-specific routes, credentials, URLs, and operational instructions in
that project's private local rules, never in this public playbook.
