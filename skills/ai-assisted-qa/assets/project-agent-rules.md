# Local Agent Rules for Artifact-Led QA

Copy this file into the target project's local `AGENTS.md` or merge it with
existing local rules. Set the project-specific paths, tracker, permitted
contours, and validators locally; do not commit credentials or internal URLs.

## Scope and Sources of Truth

1. For every non-trivial QA task, use the `ai-assisted-qa` skill and the
   controlled session templates before giving a final verdict.
2. The local `AGENTS.md`, approved task requirements/DoD, confirmed delivery,
   local implementation, and approved artifacts are sources of truth, in that
   order when local policy defines a conflict.
3. Before conclusions, inspect all available task fields, notes, attachments,
   linked work, merged changes, local code, existing tests, and relevant prior
   artifacts. State missing sources and never replace them with guesses.
4. Do not narrow a changed-risk scope to a current environment, a happy path,
   or a representative state unless the analysis states the factual reason that
   it still covers the requirement.

## Task Directory and Artifact Names

1. Configure a local artifact root as `<case-root>`. For every task, first
   ensure `<case-root>/<task-id>/` exists. Do not alter an existing case
   structure without instruction.
2. Create only the artifact for the explicitly requested stage:
   - `analysis.md`;
   - `algorithm.md`;
   - `automated-checks-report.md`, executable `autotest.<ext>` or
     `autotests.zip`, and factual evidence archive when they exist;
   - `manual-test-cases.md`;
   - `report.md`.
3. An automated report, an executable test, and a final task report are
   different artifacts. Do not substitute one for another.
4. Preserve run output outside temporary directories. Package multiple
   evidence files only when an archive improves repeatable inspection.

## Human-Gated Stages

1. Execute only the explicitly requested stage:
   analysis -> algorithm -> automated checks -> manual test case -> report.
2. Show the complete current-stage artifact in chat. Do not start the next
   stage without a new request.
3. Saving, sending, and publishing are transport operations. They must not
   rephrase, shorten, normalize, reorder, add, or remove the approved text.
4. Before saving an approved test case or report, compare it mechanically with
   the approved chat text. If different, stop and correct the saved copy.
5. Before test-case or report work, state the local rules reread, source of
   truth, validators, and the stop condition for save/publish.

## Analysis and Algorithm

1. Analysis must establish code delivery status, implementation facts, prior
   behavior, intended behavior, requirement/DoD matrix, full changed surface,
   risks, regression zones, constraints, and automation/manual boundary.
2. Before new discovery, search the private route atlas and similar approved
   algorithms. Reuse a proven matching route before discovering one again.
3. At the algorithm stage preflight required entry points read-only. Record
   infrastructure blockers early and do not perform unrelated checks after a
   required proof has become impossible.
4. An algorithm must separate user actions from agent actions and give each
   step a requirement/risk, entry point, proof, expected factual outcome, and
   stop condition.
5. After the algorithm, synchronize route memory as
   `compare -> reuse/update/add`. Add or update only proven reusable routes;
   keep recurring barriers separate and one-off diagnosis task-local.

## Automated Checks

1. Choose test layers by changed risk, not by task label or habit. Prefer the
   repository-native runner.
2. Before writing a new test, select a compatible format and preflight only
   the tools it needs. An executable check must run end-to-end and be repeatable
   before it is presented as reusable or CI-ready.
3. Record the exact scenario, requirement/risk, environment, procedure,
   expected proof, actual result, status, and evidence location.
4. Keep failed, blocked, and not-run scenarios visible. A command starting, a
   page opening, or a different green layer is not proof of the changed
   behavior.
5. For browser-visible behavior, use human-readable visual proof appropriate
   to the change. Logs, traces, and network data supplement the proof but do
   not replace it.
6. Do not perform destructive production actions, publish data, or change
   infrastructure merely to obtain coverage unless expressly authorized.

## Manual Test Cases

1. One manual test case covers the complete DoD unless an explicit split is
   approved.
2. Use this fixed form: title/identifier, description, concise task analysis,
   preconditions, and independently numbered steps.
3. Every step has one concrete action and one observable expected result.
   Preconditions and every external step must identify a confirmed entry point;
   do not require the tester to infer it from another item.
4. Use confirmed data only. Do not put placeholder IDs, endpoint parameters,
   request bodies, access values, or guessed routes into an executable step.
5. Keep automated coverage out of the manual case unless an independent human
   check is actually needed. Include all user-visible states and relevant
   negative states that the task requires.
6. Show the complete draft and wait for approval before saving it 1:1.

## Final Reports

1. Write reports only after factual evidence exists and the user requests one.
2. The report must reproduce approved manual-test-case steps in the same count,
   order, action, expected result, and exact technical literals where used. Do
   not compress several steps into a summary.
3. Preserve original DoD wording. If a contour cannot prove it, mark the item
   blocked or partial and state the limitation beside it.
4. The report must list the full current relevant artifact set and its source.
   Agent actions may contain only behavior, regression, scope-boundary, or
   blocker proof; internal document checks remain outside the report.
5. Before save or publication, validate the exact report version against the
   approved test case and factual artifacts. If any check fails, stop.
6. Publication requires a current explicit instruction for this exact report
   version and artifact set. A publication never mutates the report.

## Safety

1. Keep route atlases, barriers, detailed cases, evidence, logs, screenshots,
   internal links, identifiers, and access details private unless a separate
   publication review approves an independently rewritten public artifact.
2. Never place credentials, tokens, private URLs, personal data, customer
   data, internal IDs, or proprietary code in public output.
3. Before any public commit, run the repository's safety checks and inspect the
   staged diff. Automated secret scanning is a backstop, not a substitute for
   the review.
