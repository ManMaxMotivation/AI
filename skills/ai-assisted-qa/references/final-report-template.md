# Final QA Report Template

Use this form after execution. Adapt Markdown to the project tracker only if
the project has a mandatory format. Do not change the section order, collapse
manual steps, or substitute planned results for actual observations.

```markdown
# QA Report: <task-id> - <short title>

## Outcome

Status: PASS / FAIL / BLOCKED / PARTIAL
Tested revision or delivery identifier: <confirmed value or "not available">
Target contour: <confirmed environment>

## Change Description

1. <What changed, based on the approved analysis.>
2. <Second changed behavior or scope item.>

## What Was Checked Manually

1. <Exact user-visible state, contour, locale/device/browser when material.>
2. <Another independently checked profile.>

## Execution Run

1. <Exact action copied from approved manual test case step 1.>
   **Expected result:** <Exact expected result copied from that step.>
   **Actual result:** <Factual observed result, evidence reference, or BLOCKED/NOT RUN.>

2. <Exact action copied from approved manual test case step 2.>
   **Expected result:** <Exact expected result copied from that step.>
   **Actual result:** <Factual observed result, evidence reference, or BLOCKED/NOT RUN.>

## Agent Actions

Automated checks: total <N>; passed <N>; failed <N>; blocked/not run <N>.

1. <Behavior-proving automated check or blocker investigation.>
   **Expected result:** <What this check was expected to prove.>
   **Actual result:** <Factual result and evidence reference.>

2. <Next behavior-proving automated check.>
   **Expected result:** <Expected proof.>
   **Actual result:** <Factual result and evidence reference.>

## Verification Artifacts

1. `analysis.md` - <origin and purpose.>
2. `algorithm.md` - <origin and purpose.>
3. `automated-checks-report.md` - <origin and purpose.>
4. `autotest.<ext>` or `autotests.zip` - <origin and rerun purpose, if present.>
5. `evidence-*.zip` - <factual contents, if present.>
6. `manual-test-cases.md` - <approved source of manual execution.>
7. <manual media/log/other factual evidence, if present.>

## DoD

1. [PASS / FAIL / BLOCKED / PARTIAL] <Original DoD item, unchanged.>
   Evidence or limitation: <factual reference.>
2. [PASS / FAIL / BLOCKED / PARTIAL] <Original DoD item, unchanged.>
   Evidence or limitation: <factual reference.>

## Findings, Blockers, and Remaining Risk

1. <Finding or "None found in the executed scope".>
2. <Blocker and the exact coverage it prevents, if any.>
3. <Remaining risk that the executed evidence does not close.>

## Conclusion and Decision Owner

<A factual conclusion stating what was evidenced, what remains unknown, and
who may accept any limitation or approve release.>
```

## Mandatory Preflight

Before the report is shown, saved, or published:

1. Reopen the approved manual test case and compare its steps with `Execution
   Run` mechanically: count, order, action, expected result, and literal
   technical fragments must agree.
2. Verify that every actual result is backed by a real execution record or is
   explicitly marked `BLOCKED` or `NOT RUN`.
3. Confirm that all current relevant artifacts are listed and each list entry
   says where it came from.
4. Keep original DoD wording. Add a limitation beside it instead of rewriting
   it as a smaller requirement.
5. Confirm that a report publication command applies to this exact approved
   report version and this exact artifact set. Publishing is transport only; it
   must not mutate the report.
