# Synthetic Final QA Report: Allocation State Propagation

> This is a fictional completed-report example. All system names, timestamps,
> candidates, artifacts, and results are invented. It demonstrates report
> structure and evidence discipline; it is not a release approval.

## Change Description and Tested Scope

The item detail page now consumes the published `allocation_state` field. A
held item renders **On hold**; an unavailable item renders **Currently
unavailable**. In both states, detail-page and comparison request actions must
be inert. An active item must retain its existing allocation path.

The test scope included:

- state contract and payload-to-label mapping;
- detail page on desktop and mobile profiles;
- independently rendered comparison actions;
- active baseline behavior;
- the interval between allocation-service closure and catalog-snapshot refresh;
- delivery and publication evidence needed to classify a failed result.

Excluded from this fictional example: search result ranking, pricing, and the
deleted-item not-found flow. They were not changed by the task and were not
needed to prove the allocation-state behavior.

## Manual Work Performed

| ID | Human check | Profile | Factual synthetic result |
| --- | --- | --- | --- |
| MANUAL-01 | Reviewed held and unavailable labels in title area. | Desktop | Both labels were legible and aligned with the fictional design specification. |
| MANUAL-02 | Used pointer and keyboard on inactive actions. | Desktop and mobile | No disabled control navigated or retained an actionable focus path. |
| MANUAL-03 | Followed active-item allocation journey through its first valid step. | Desktop | Active action opened the expected allocation step. |
| MANUAL-04 | Observed allocation transition after approved state change. | Desktop | The action became inert before a customer could enter a closed allocation route. |

Manual evidence complements, but does not replace, the browser and data-layer
evidence recorded below.

## Execution Run

### 1. Delivery and Contract Preflight

**Expected:** The test environment serves the target change and the public
state contract accepts `active`, `held`, and `unavailable`.

**Actual:** Synthetic build `sample-build-42` contained the target change.
Contract checks confirmed all three values and explicit customer label mapping.
The preflight passed.

### 2. Candidate Validation

**Expected:** Each candidate has a reachable page, matching published snapshot,
and expected allocation-service availability before browser assertions start.

**Actual:** Three fictional candidates were validated at `2030-04-18T10:00Z`:
one active, one held, and one unavailable. No stale candidate was used.

### 3. Held State on Desktop

**Expected:** Held detail page remains reachable, shows **On hold**, and has no
actionable desktop request control.

**Actual:** The page rendered normally. The scoped title evidence showed **On
hold**. The request element was a disabled button without an allocation
destination. The check passed.

### 4. Held State on Mobile

**Expected:** Mobile sticky request action is inert for held state.

**Actual:** The mobile sticky action exposed disabled semantics and no route.
Touch and keyboard-equivalent interaction did not navigate. The check passed.

### 5. Unavailable State on Desktop

**Expected:** Unavailable detail page remains reachable, shows **Currently
unavailable**, and has no actionable desktop request control.

**Actual:** The published payload contained `allocation_state=unavailable`.
The title label matched the product wording and the action had no destination.
The check passed.

### 6. Unavailable State on Mobile

**Expected:** Mobile sticky request action is inert for unavailable state.

**Actual:** The control was disabled, had no allocation route, and did not
navigate when activated through the supported mobile interaction path. The
check passed.

### 7. Comparison Surface

**Expected:** Every visible request action for held and unavailable items is
inert, including card and summary locations.

**Actual:** The desktop card action, desktop summary action, and mobile compare
action were inspected for both non-active candidates. All were inert and had no
allocation destination. The regression check passed.

### 8. Active Baseline

**Expected:** Active item has no non-active label and retains the allocation
entry path.

**Actual:** The active candidate rendered no state label. Its request action
was enabled and opened the first valid allocation step. The baseline passed.

### 9. Controlled Allocation Transition

**Expected:** An authorized person creates exactly one allocation transition;
the agent remains read-only and records a timestamped baseline.

**Actual:** The synthetic operator created one approved held state at
`2030-04-18T10:18:24Z`. The agent had captured the active page, active action,
service response, and snapshot version before the handoff. The handoff was
recorded as complete.

### 10. Service and Publication Timeline

**Expected:** Service closure, publication event, snapshot update, page label,
and action state can be ordered in time.

**Actual:** The synthetic evidence showed service closure at `T+08s`, a
publication event at `T+19s`, snapshot state at `T+34s`, and final visible
label/action update at `T+39s`. The timeline was complete.

### 11. Transition-Window Safety

**Expected:** After service closure, the customer cannot enter a rejected
allocation route from an apparently active detail-page action.

**Actual:** Between `T+08s` and `T+39s`, the page snapshot still represented
the former active state, but the request control became inert at `T+10s` and
had no destination. No navigation to the closed route was possible. The
transition was classified as safe.

### 12. Final Consistency Retest

**Expected:** Final snapshot, visible label, action state, and service response
agree after publication.

**Actual:** The final held page showed **On hold** with inert desktop and mobile
actions. The active control case remained enabled on the independent baseline
candidate. The final consistency retest passed.

## Agent Actions and What They Proved

| Action | What it proved | DoD/requirement covered |
| --- | --- | --- |
| Read task sources, implementation mapping, contract tests, and delivery metadata. | Scope and state contract were established before execution. | R1-R6 |
| Reused allocation lifecycle and browser-action routes from private route memory. | Existing proven paths were used instead of speculative route discovery. | Process quality; R1-R6 |
| Validated fresh candidates before browser checks. | Each UI result started from matching data, snapshot, and service facts. | R1-R5 |
| Ran focused browser scenarios for detail, mobile, and comparison actions. | Non-active controls were inert across independent surfaces. | R1-R5 |
| Recorded service, publication, snapshot, and UI timestamps during transition. | The final result distinguished safe interim behavior from delayed publication. | R6 |
| Performed final route-memory comparison. | The verified cross-layer path was suitable for a private route-atlas update. | Reuse quality |

## Evidence Package

| Artifact | Purpose | Source |
| --- | --- | --- |
| `01-task-brief.md` | Product requirement and acceptance criteria. | Synthetic task source. |
| `02-analysis.md` | Scope, dependencies, risk zones, and automation boundary. | Synthetic analysis based on the task source. |
| `03-algorithm.md` | Reusable route, roles, stop conditions, and coverage plan. | Approved synthetic analysis and route-memory protocol. |
| `04-automated-checks.md` | Automation design, scenario matrix, and synthetic execution evidence. | Project-native test-layer model. |
| `05-manual-test-cases.md` | Human scenarios and expected observations. | Approved synthetic algorithm. |
| `06-report.md` | Traceability and factual conclusion. | Synthetic execution and manual records. |
| `evidence/` | Scoped screenshots, interaction video, DOM facts, and timeline record in a real case. | Not included here because this example is fictional. |

## Requirement and DoD Traceability

| Item | Automated evidence | Manual evidence | Status |
| --- | --- | --- | --- |
| R1: held page is reachable, clear, and inert | AUTO-01, AUTO-03, AUTO-04 | MANUAL-01, MANUAL-02 | Passed in synthetic example |
| R2: unavailable page is reachable, clear, and inert | AUTO-02, AUTO-05, AUTO-06 | MANUAL-01, MANUAL-02 | Passed in synthetic example |
| R3: inactive actions cannot navigate | AUTO-03 through AUTO-06 | MANUAL-02 | Passed in synthetic example |
| R4: active path remains available | AUTO-07 | MANUAL-03 | Passed in synthetic example |
| R5: comparison surface follows rule | AUTO-08 | MANUAL-02 | Passed in synthetic example |
| R6: transition window is safe | AUTO-09, AUTO-10 | MANUAL-04 | Passed in synthetic example |

## Findings, Blockers, and Remaining Risk

No blocker occurred in this fictional run. The result still has boundaries:

1. It does not prove every localization or browser profile.
2. It does not replace accessibility review with assistive technology.
3. It does not prove behavior under every publication outage.
4. A real project must retain private artifacts, exact data, and environment
   links outside this public playbook.

## Conclusion and Decision Owner

The synthetic evidence demonstrates a complete artifact chain for a complex
state-propagation change. It demonstrates how an agent should reason and
record facts; it does not represent a real product result. In a real task, the
QA owner and product/release owner review the actual evidence and decide whether
remaining risk is acceptable.
