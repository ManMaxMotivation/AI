# Synthetic Final QA Report: Allocation State Propagation

> This is a fictional completed-report example. All system names, timestamps,
> candidates, artifacts, and results are invented. It demonstrates how a final
> report must preserve approved manual steps and factual evidence; it is not a
> release approval for a real product.

## Outcome

Status: PASS in this synthetic run.

Tested revision or delivery identifier: `sample-build-42` (fictional).

Target contour: fictional approved test environment; desktop and mobile
browser profiles.

## Change Description

1. The item detail page consumes published `allocation_state`.
2. A held item shows **On hold** and an unavailable item shows **Currently
   unavailable**.
3. In both non-active states, detail-page and comparison request actions are
   inert and have no allocation destination.
4. An active item retains its existing allocation path.
5. The changed-risk scope includes the interval between allocation-service
   closure and the published catalog snapshot reaching the visible page.

## What Was Checked Manually

1. Held and unavailable detail-page labels in the approved desktop and mobile
   title areas.
2. Desktop, mobile, card, and comparison request controls for non-active
   candidates.
3. The active-item allocation entry path on desktop and separate mobile action
   where it exists.
4. A controlled, user-authorized transition from active to held state.
5. The final state after publication, including comparison surface when in
   scope.

## Execution Run

1. Open the held candidate in the approved desktop browser profile.
   **Expected result:** The detail page is reachable and does not show the
   generic deleted-item experience. **On hold** is visible in the approved
   title area. The desktop request control is visibly disabled, exposes
   disabled semantics, and does not navigate to an allocation route.
   **Actual result:** The fictional held page was reachable. Scoped title
   evidence showed **On hold**. The request element was disabled, had no
   allocation destination, and did not navigate. Status: passed.

2. Open the same held candidate in the approved mobile profile and scroll to
   the sticky request area.
   **Expected result:** The item remains reachable and shows **On hold**. The
   mobile sticky request control is disabled, has no allocation destination,
   and cannot be activated by touch or keyboard-equivalent interaction.
   **Actual result:** The fictional mobile page showed **On hold**. The sticky
   action exposed disabled semantics, had no route, and did not navigate by the
   supported touch or keyboard-equivalent interaction. Status: passed.

3. Open the comparison surface containing the held candidate. Inspect every
   request control that belongs to that item, including any card and summary
   actions.
   **Expected result:** The candidate can be displayed for comparison if that
   is allowed by product rules, but no request control for it can navigate to
   an allocation route. An active compare action is a defect even if the detail
   page is correct.
   **Actual result:** The fictional desktop card action, desktop summary
   action, and mobile comparison action for the held candidate had no active
   allocation destination. Status: passed.

4. Open the unavailable candidate in the approved desktop browser profile.
   **Expected result:** The detail page remains reachable. The title area shows
   **Currently unavailable**, not the raw technical state. The desktop request
   control is disabled and has no actionable destination.
   **Actual result:** The fictional published payload contained
   `allocation_state=unavailable`; the page showed **Currently unavailable**.
   The request control was disabled and had no destination. Status: passed.

5. Open the unavailable candidate in the approved mobile profile and inspect
   the sticky request area.
   **Expected result:** The label is visible and understandable in the mobile
   layout. The sticky action is disabled and cannot open allocation.
   **Actual result:** The fictional mobile title label was visible and the
   sticky action was disabled. No supported interaction opened allocation.
   Status: passed.

6. Open the comparison surface for the unavailable candidate in desktop and
   the separately implemented mobile profile, when present.
   **Expected result:** Every visible request control is disabled or absent as
   defined by the product. No control exposes an allocation link or starts a
   navigation that the service will reject.
   **Actual result:** Each observed fictional comparison control was inert or
   absent according to the state rule. No control exposed a link or navigation
   into the closed allocation route. Status: passed.

7. Open the fresh active candidate in the desktop profile.
   **Expected result:** No held or unavailable label is present. The request
   control is enabled and opens the valid first allocation step. The state
   feature has not disabled the existing active-item journey.
   **Actual result:** The fictional active candidate rendered no non-active
   label. Its request control was enabled and opened the expected first
   allocation step. Status: passed.

8. Open the active candidate in the mobile profile if the mobile action is a
   separate implementation.
   **Expected result:** The sticky action remains enabled and its behavior
   matches the approved active desktop journey.
   **Actual result:** The separate fictional mobile action was enabled and
   followed the same valid allocation entry behavior. Status: passed.

9. Before changing state, record the active candidate's page, action state,
   snapshot version, service availability, and current time. Confirm with the
   user that the approved allocation action may now be performed.
   **Expected result:** The baseline is unambiguous: the page is active, the
   action is actionable, the service accepts allocation, and the evidence has a
   timestamp that can be compared with later observations.
   **Actual result:** Before the fictional handoff, the agent recorded an
   active page, enabled action, service availability, and snapshot version at
   `2030-04-18T10:18:16Z`. The approved operator handoff was confirmed.
   Status: passed.

10. The authorized person performs the real allocation action or approved state
    change for the selected active candidate, then reports completion time to
    the agent.
    **Expected result:** The action creates the intended allocation lifecycle
    event for exactly one candidate. The tester does not change multiple
    candidates or assume the state changed without a factual confirmation.
    **Actual result:** The fictional authorized operator created one held-state
    transition and reported completion at `2030-04-18T10:18:24Z`. The agent did
    not mutate any state. Status: passed.

11. Immediately after the handoff, reopen the item page while the agent
    observes service closure, published snapshot state, and the request
    control. Repeat only according to the approved algorithm until final
    consistency or a stop condition.
    **Expected result:** If the service is already closed, the page must not
    expose an action that can send the customer to a known rejected route. If
    the snapshot is delayed, record the exact state of the label and control as
    a transition finding rather than silently waiting for the final state.
    **Actual result:** Fictional evidence showed service closure at `T+08s`,
    while the page snapshot still showed the former active state. The request
    control became inert at `T+10s` and had no destination; publication reached
    the snapshot at `T+34s` and the visible label at `T+39s`. The interval was
    classified as safe, not hidden by waiting for final consistency. Status:
    passed.

12. After publication completes, reopen the same candidate in desktop and
    mobile profiles. Inspect comparison again if it is in scope.
    **Expected result:** Published payload, visible label, request control, and
    service state agree. The final page is reachable, non-active actions are
    inert, and the active baseline remains unaffected for a separate current
    candidate.
    **Actual result:** The fictional final held page showed **On hold** with
    inert desktop and mobile actions. Comparison remained inert. The separate
    active baseline remained enabled. Status: passed.

## Agent Actions

Automated checks: total `10`; passed `10`; failed `0`; blocked/not run `0`.

1. Read the synthetic task source, implementation mapping, contract tests, and
   delivery metadata before execution.
   **Expected result:** The state contract and delivery scope are established
   before any test selects candidates or a browser route.
   **Actual result:** The fictional analysis confirmed `active`, `held`, and
   `unavailable` state mapping, independent detail/comparison surfaces, and
   the transition-window risk. Status: passed.

2. Reuse the approved synthetic allocation-lifecycle and browser-action routes
   after comparing them with the task's state contract.
   **Expected result:** The agent uses a matching proven route rather than
   guessing a new cross-layer route.
   **Actual result:** The fictional route supplied candidate validation,
   service/snapshot observations, and browser evidence points. Status: passed.

3. Run AUTO-01 through AUTO-08: contract and focused browser checks for held,
   unavailable, active, and comparison behavior.
   **Expected result:** Non-active controls have no viable allocation route;
   active behavior remains available.
   **Actual result:** All eight fictional scenarios passed with state mapping,
   disabled semantics, destination, and browser assertions recorded in
   `04-automated-checks.md`. Status: passed.

4. Run AUTO-09 and AUTO-10: read-only transition timing and stale-active-action
   detection.
   **Expected result:** The evidence orders service, publication, snapshot, and
   UI events and fails if service closure leaves an actionable route.
   **Actual result:** The fictional timeline showed an inert action before the
   final label, and no rejected allocation route was reachable. Status: passed.

## Verification Artifacts

1. `01-task-brief.md` - fictional requirement and acceptance criteria source.
2. `02-analysis.md` - synthetic scope, dependencies, risk zones, and
   automation/manual boundary.
3. `03-algorithm.md` - approved synthetic verification route, roles, and stop
   conditions.
4. `04-automated-checks.md` - automation architecture, scenario matrix, and
   synthetic execution record.
5. `05-manual-test-cases.md` - approved human execution source reproduced
   above.
6. `06-report.md` - this fictional factual-report structure.
7. `evidence/` - in a real task, a private package of focused screenshots,
   interaction video, DOM facts, and timeline records. It is intentionally not
   included in this public fictional example.

## DoD

1. [PASS] R1: held page is reachable, clear, and inert.
   Evidence or limitation: AUTO-01, AUTO-03, AUTO-04 and execution steps 1-3.
2. [PASS] R2: unavailable page is reachable, clear, and inert.
   Evidence or limitation: AUTO-02, AUTO-05, AUTO-06 and execution steps 4-6.
3. [PASS] R3: inactive actions cannot navigate.
   Evidence or limitation: AUTO-03 through AUTO-06 and execution steps 1-6.
4. [PASS] R4: active path remains available.
   Evidence or limitation: AUTO-07 and execution steps 7-8.
5. [PASS] R5: comparison surface follows rule.
   Evidence or limitation: AUTO-08 and execution steps 3 and 6.
6. [PASS] R6: transition window is safe.
   Evidence or limitation: AUTO-09, AUTO-10 and execution steps 9-12.

## Findings, Blockers, and Remaining Risk

1. No product finding occurred in this fictional run.
2. No fictional execution blocker occurred.
3. This example does not prove every localization or browser profile, assistive
   technology behavior, or every publication outage. A real task must list its
   actual private evidence, data, environments, and unresolved risk.

## Conclusion and Decision Owner

The synthetic evidence demonstrates a complete artifact chain for a complex
state-propagation change: analysis drives the algorithm, the algorithm drives
repeatable automated proof, the approved manual test case is reproduced in the
execution run, and the report makes remaining uncertainty explicit. In a real
task, the QA owner and product/release owner decide whether the actual evidence
and remaining risk are sufficient.
