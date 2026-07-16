# QA Artifact Contract

Create one directory per task. Keep the chain concise enough to review, but do
not omit a source, risk, blocker, or requirement merely to make it shorter.

## analysis.md

Use these sections:

1. Change in plain language
2. Sources reviewed and their authority
3. Acceptance criteria or DoD
4. Changed surface and dependencies
5. Risks and regression zones
6. Constraints, assumptions, and open questions
7. Scope decision

For every risk, state why the change can affect it. Separate confirmed facts
from inferences.

## algorithm.md

Use these sections:

1. Case signature and preconditions
2. Coverage route in execution order
3. Requirement-to-step mapping
4. Tools, entry points, and expected evidence
5. Reuse of existing tests or known routes
6. Stop conditions and human handoffs

Each step must be observable. Do not write vague steps such as "test the
feature" or "check for regressions".

## automated-checks.md

For each check record:

- ID and requirement/risk covered
- test layer and reason for selecting it
- procedure or repository-native command
- expected observable result
- actual result, evidence, and status
- limitation or blocker, if present

Do not mark a check as passed because the command started, a page opened, or a
different layer was green.

## manual-test-cases.md

For each scenario record:

- ID and requirement/risk covered
- preconditions and entry point
- user actions
- expected result
- actual result, evidence, and status when executed

Use manual testing for evidence that needs a person, not as a place to defer
reproducible automation without reason.

## report.md

Use these sections:

1. Change and scope tested
2. Requirement/DoD traceability table
3. Automated evidence summary
4. Manual evidence summary
5. Findings, blockers, and remaining risk
6. Factual conclusion and decision owner

The conclusion must say what was evidenced, what was not, and who may decide
whether an accepted limitation is sufficient.
