# Manual Test Case: Allocation State Propagation

> Synthetic test case. It is a complete human-readable scenario structure, not
> an execution record. A real tester fills actual result and evidence only after
> the step is performed in an approved environment.

## Description

Verify that allocation state is communicated consistently on a fictional
equipment item detail page and related comparison surface. The scenario covers
held, unavailable, and active items, then observes the transition after a real
allocation action. It specifically protects against a stale page that lets a
customer open an allocation route after the service has already closed the
item.

## Analysis for This Test Case

**Previous behavior:** every published item rendered a normal request link. A
customer could see an active detail-page action even after the allocation
service had rejected the item.

**Changed behavior:** the page reads `allocation_state`, renders **On hold** or
**Currently unavailable**, and removes the request destination for non-active
items. Desktop, mobile, and comparison actions are separate risk surfaces.

**Problem solved:** a customer should understand why an item cannot be
requested and should not be routed into an avoidable unavailable or not-found
experience.

**Regression zones:** published snapshot mapping, title label, desktop action,
mobile sticky action, comparison actions, active baseline, allocation route,
and the service-to-snapshot propagation interval.

## Preconditions

1. The target build revision is confirmed in the approved test environment.
2. The current design source confirms the approved title-area labels:
   **On hold** and **Currently unavailable**.
3. A fresh held candidate is available: reachable detail page, snapshot state
   `held`, and a closed allocation service response.
4. A fresh unavailable candidate is available: reachable detail page, snapshot
   state `unavailable`, and a closed allocation service response.
5. A fresh active candidate is available: reachable detail page, active or
   absent state field, and a valid allocation route.
6. The comparison surface can load each selected candidate.
7. The tester has the approved browser profiles and any required test account.
8. A user-approved method exists for creating one real allocation transition;
   the agent does not create or alter state without this handoff.

## Test Steps

### 1. Held Detail Page on Desktop

Open the held candidate in the approved desktop browser profile.

**Expected result:** The detail page is reachable and does not show the generic
deleted-item experience. **On hold** is visible in the approved title area. The
desktop request control is visibly disabled, exposes disabled semantics, and
does not navigate to an allocation route.

### 2. Held Detail Page on Mobile

Open the same held candidate in the approved mobile profile and scroll to the
sticky request area.

**Expected result:** The item remains reachable and shows **On hold**. The
mobile sticky request control is disabled, has no allocation destination, and
cannot be activated by touch or keyboard-equivalent interaction.

### 3. Held Comparison Surface

Open the comparison surface containing the held candidate. Inspect every
request control that belongs to that item, including any card and summary
actions.

**Expected result:** The candidate can be displayed for comparison if that is
allowed by product rules, but no request control for it can navigate to an
allocation route. An active compare action is a defect even if the detail page
is correct.

### 4. Unavailable Detail Page on Desktop

Open the unavailable candidate in the approved desktop browser profile.

**Expected result:** The detail page remains reachable. The title area shows
**Currently unavailable**, not the raw technical state. The desktop request
control is disabled and has no actionable destination.

### 5. Unavailable Detail Page on Mobile

Open the unavailable candidate in the approved mobile profile and inspect the
sticky request area.

**Expected result:** The label is visible and understandable in the mobile
layout. The sticky action is disabled and cannot open allocation.

### 6. Unavailable Comparison Surface

Open the comparison surface for the unavailable candidate in desktop and the
separately implemented mobile profile, when present.

**Expected result:** Every visible request control is disabled or absent as
defined by the product. No control exposes an allocation link or starts a
navigation that the service will reject.

### 7. Active Baseline on Detail Page

Open the fresh active candidate in the desktop profile.

**Expected result:** No held or unavailable label is present. The request
control is enabled and opens the valid first allocation step. The state feature
has not disabled the existing active-item journey.

### 8. Active Baseline on Mobile

Open the active candidate in the mobile profile if the mobile action is a
separate implementation.

**Expected result:** The sticky action remains enabled and its behavior matches
the approved active desktop journey.

### 9. Prepare Transition Observation

Before changing state, record the active candidate's page, action state,
snapshot version, service availability, and current time. Confirm with the user
that the approved allocation action may now be performed.

**Expected result:** The baseline is unambiguous: the page is active, the
action is actionable, the service accepts allocation, and the evidence has a
timestamp that can be compared with later observations.

### 10. Perform Approved Allocation Handoff

The authorized person performs the real allocation action or approved state
change for the selected active candidate, then reports completion time to the
agent.

**Expected result:** The action creates the intended allocation lifecycle event
for exactly one candidate. The tester does not change multiple candidates or
assume the state changed without a factual confirmation.

### 11. Inspect the Propagation Interval

Immediately after the handoff, reopen the item page while the agent observes
service closure, published snapshot state, and the request control. Repeat only
according to the approved algorithm until final consistency or a stop condition.

**Expected result:** If the service is already closed, the page must not expose
an action that can send the customer to a known rejected route. If the snapshot
is delayed, record the exact state of the label and control as a transition
finding rather than silently waiting for the final state.

### 12. Verify Final Held or Unavailable State

After publication completes, reopen the same candidate in desktop and mobile
profiles. Inspect comparison again if it is in scope.

**Expected result:** Published payload, visible label, request control, and
service state agree. The final page is reachable, non-active actions are inert,
and the active baseline remains unaffected for a separate current candidate.

## Exploratory Checks

Run these only when they are relevant to the changed risk or requested scope:

| Area | Exploration | Expected learning |
| --- | --- | --- |
| Browser history | Back, forward, refresh, and direct route entry after state change. | UI does not restore an actionable stale action. |
| Accessibility | Keyboard focus order, disabled semantics, label announcement. | State is understandable without visual color alone. |
| Layout | Long translated label, narrow mobile viewport, title wrapping. | Label remains legible and does not obscure controls. |
| Data edge | Missing, null, or unsupported state field in an approved non-production fixture. | Fallback is explicit and never makes an unsafe action active. |
| Timing | Slow publication or temporary worker failure. | Report distinguishes delivery blocker from UI defect. |

## Actual Result Record

For a real run, add the following directly under each executed step:

```text
Actual result: <factual observation only>
Evidence: <private artifact name or approved source>
Environment/profile: <approved contour and device profile>
Status: passed | failed | blocked | not run
```

Do not fill these fields from expected results, an automated green run, or a
previous task. The final report consumes only factual records.
