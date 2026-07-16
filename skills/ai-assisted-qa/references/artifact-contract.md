# QA Artifact Contract

This contract preserves an audit trail across a complex QA task. A project may
rename files and use its own tracker markup, but it must preserve the chain and
the required information. Do not create every file automatically: create the
artifact for the stage that was explicitly requested.

```text
<case-root>/<task-id>/
  analysis.md
  algorithm.md
  automated-checks-report.md
  autotest.<ext> or autotests.zip             # only if a rerunnable test exists
  evidence-automated.zip or evidence-ui.zip   # only if multiple evidence files exist
  manual-test-cases.md
  report.md
```

## 1. Analysis

`analysis.md` is the scope contract. It must be detailed enough for another
tester to understand what has changed and why the later coverage is justified.

Required sections:

1. Change in plain language.
2. Sources reviewed and their authority: task tracker, acceptance criteria or
   DoD, notes, attachments, linked work, delivery revision, local code, tests,
   and prior artifacts.
3. Requirement and DoD matrix.
4. Delivery status: present, absent, or partial, with factual implementation
   references.
5. Previous behavior.
6. Intended new behavior and the problem it solves.
7. Changed surface and dependencies: code modules, API/data contracts, state
   transitions, jobs, integrations, routes, UI states, roles, and consumers as
   applicable.
8. Risks and regression zones, each with a concrete cause.
9. Existing route or prior-artifact reuse decision.
10. Automation/manual boundary.
11. Constraints, unknowns, access limits, and blockers.
12. Scope conclusion: what must be proven before the task may be closed.

Facts, inferences, and open questions must be distinguishable. Reading only a
ticket or only a diff is insufficient for a full analysis when other sources
exist.

## 2. Algorithm

`algorithm.md` converts the approved analysis into a repeatable route before
any conclusion about task quality is made.

Required sections:

1. Case signature and covered DoD/risk scope.
2. Sources and approved prior artifacts used.
3. Preconditions, contours, permissions, and read-only entry-point preflight.
4. Route-memory and process-barrier decision.
5. Ordered coverage route. For every step state:
   - requirement/risk;
   - user action and agent action;
   - system layer and exact entry point;
   - expected observable evidence;
   - expected factual result;
   - stop condition, escalation, or next branch.
6. Minimal fast path, if the complete route has an expensive branch.
7. Automation/manual boundary.
8. Intended route-memory synchronization: `compare -> reuse/update/add`.
9. Expected factual end state.

A route is not reusable merely because it was written. Only a route that has
been proven by real work may be added to a private route atlas.

## 3. Automated Checks

The automated stage has three distinct things when they exist: executable
checks, an outcome report, and factual evidence. A test script does not replace
the report, and a report does not replace a rerunnable test.

`automated-checks-report.md` must include:

1. Automation objective and changed-risk classification.
2. Selected test layers and why each is sufficient.
3. Tool and dependency preflight.
4. Data/state and environment preconditions.
5. Scenario matrix: scenario ID, DoD/risk, procedure, expected proof, actual
   result, status, and evidence location.
6. Assertions and what they do and do not prove.
7. Actual execution record, including failed, blocked, and not-run scenarios.
8. Rerun/CI instructions for executable checks, when one exists.
9. Evidence package inventory.
10. Automation limits that remain for manual verification.

Requirements for executable checks:

- prefer the repository-native runner;
- select the implementation format deliberately and preflight its actual
  dependencies;
- run the exact artifact end-to-end before calling it reusable;
- preserve outputs outside temporary directories;
- do not silently exclude failed scenario evidence;
- keep the artifact safe to rerun and compatible with the project CI route.

## 4. Manual Test Case

`manual-test-cases.md` is a human execution document, not a prose copy of the
automation stage.

Required sections and rules:

1. Task title and identifier.
2. Description.
3. Analysis for the test case: previous behavior, change, problem solved, and
   regression zones only.
4. Preconditions: only required conditions and explicit entry points. A tester
   must not have to infer a URL, screen, API method, target entity, or target
   contour from another step.
5. Steps: independent numbering, one action and one observable expected result
   per step. Keep the action and its expected result together.

Additional requirements:

- one test case covers the full DoD unless the reviewer explicitly asks for a
  split;
- do not use placeholders for runtime IDs, endpoints, request bodies, or
  access data in an executable technical step;
- use only confirmed test data and entry points;
- include all required user-visible states, including relevant negative states;
- include design comparison for UI/layout work when a design source exists;
- include only human work that automation cannot faithfully prove or that must
  be independently confirmed;
- show the full draft for approval, then save it 1:1 without reformatting.

## 5. Final Report

`report.md` is written after factual execution. It must be traceable back to
the approved manual test case and automation evidence.

Required sections, in order:

1. Outcome header and tested revision or delivery identifier, if known.
2. Change description.
3. What was checked manually, including factual contour/profile where relevant.
4. Execution run: every approved manual test-case step in the same order, each
   with action, expected result, and factual actual result.
5. Agent actions: only checks that prove behavior, regression, scope boundary,
   or blocker, plus a passed/failed/not-run count.
6. Artifact inventory and provenance.
7. Original DoD items with their factual status. Do not rewrite them narrower.
8. Findings, blockers, and remaining risk.
9. Factual conclusion and decision owner.

Run a literal traceability check before saving: manual step count, action text,
expected result, exact technical fragments where needed, artifact list, and
DoD wording. The report must show an unverified requirement as unverified; it
must never turn an inaccessible environment or planned test into a pass.

Use `references/final-report-template.md` as the copyable form.
