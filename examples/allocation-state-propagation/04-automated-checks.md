# Automated Evidence Artifact: Allocation State Propagation

> Synthetic example. The execution record below is fictional and exists to
> demonstrate the level of detail an AI-generated automation artifact must
> preserve. It is not a runnable test against a real system.

## 1. Automation Objective

Prove deterministic behavior that is unsuitable for a purely manual check:

1. payload state maps to the correct visible state;
2. inactive request controls have no actionable destination;
3. active controls preserve the existing route;
4. independently rendered comparison controls follow the same rule;
5. the transition window is measured across service, snapshot, and UI layers.

The artifact does not claim to prove visual quality, accessibility judgment, or
the complete real customer allocation flow. Those remain manual evidence.

## 2. Why These Test Layers Were Selected

| Layer | Purpose | Why this layer is needed | Why it is not enough alone |
| --- | --- | --- | --- |
| Contract test | Validate legal state values and label mapping. | Catches bad state transformation early. | Cannot prove page wiring or interaction. |
| Component test | Validate state utility and action semantics. | Catches a link retained behind disabled styling. | Cannot prove routing or independent page surfaces. |
| Browser test | Validate real rendered detail and comparison actions. | Proves DOM, destination, and visible state together. | Cannot reliably create or judge every production-like transition. |
| Read-only telemetry check | Correlate service closure, publication, and snapshot timing. | Proves the source of a transition delay. | Cannot prove visual quality by itself. |
| Manual test | Inspect visual, keyboard, and human-driven allocation path. | Covers human and environment-dependent behavior. | Must not replace reproducible assertions. |

## 3. Preconditions

Before implementing or executing an automated scenario, the agent must record:

| Item | Required fact |
| --- | --- |
| Target revision | The browser environment serves the change being tested. |
| Browser profile | Desktop and mobile profiles match project-approved configuration. |
| Candidate catalog | Fresh active, held, and unavailable candidates satisfy the algorithm criteria. |
| State source | Candidate state is confirmed from the published payload, not from label text alone. |
| Route source | Detail, comparison, and allocation routes come from route memory or current project configuration. |
| Evidence path | Screenshots, video where interaction matters, DOM facts, and network facts have a task-local destination. |

If one precondition is false, the script must fail or skip with an explicit
reason. It must not substitute a stale ID, random catalog item, or synthetic
browser storage state as the primary proof.

## 4. Test Architecture

The generated test should be split by behavioral purpose, not written as one
long loop through every scenario.

```text
tests/allocation-state/
  fixtures/
    candidate-discovery.ts       Fresh validated candidates and timestamps
    evidence.ts                  Scoped visual and DOM evidence helpers
  allocation-contract.spec.ts    State mapping contract
  detail-state.spec.ts           Desktop and mobile detail page behavior
  comparison-state.spec.ts       Independently rendered compare actions
  transition-window.spec.ts      Timed service/snapshot/UI observation
```

This structure lets a later rerun target one failed layer without replaying a
long state-changing journey. It also prevents a successful active baseline from
masking a failed unavailable-state scenario.

## 5. Candidate Contract

The discovery fixture returns only candidates that satisfy this shape:

```ts
type Candidate = {
  publicId: string;
  detailRoute: string;
  comparisonRoute?: string;
  snapshotVersion: string;
  allocationState: "active" | "held" | "unavailable";
  serviceAvailability: "allocatable" | "closed";
  observedAt: string;
};
```

The fixture rejects a candidate if the public page, snapshot, or service layer
disagrees before the scenario starts. That protects tests from falsely blaming
the UI for invalid input data.

## 6. Scenario Matrix

| ID | Scenario | Layer | Requirement | Required assertions |
| --- | --- | --- | --- | --- |
| AUTO-01 | State contract maps `held` to `On hold`. | Contract/component | R1 | Public payload and label mapping agree. |
| AUTO-02 | State contract maps `unavailable` to `Currently unavailable`. | Contract/component | R2 | Public payload and label mapping agree. |
| AUTO-03 | Held detail page desktop action is inert. | Browser | R1, R3 | Page is reachable; label visible; control disabled; no destination. |
| AUTO-04 | Held mobile sticky action is inert. | Browser | R1, R3 | Same facts in mobile surface. |
| AUTO-05 | Unavailable detail page desktop action is inert. | Browser | R2, R3 | Correct label; disabled semantic control; no destination. |
| AUTO-06 | Unavailable mobile sticky action is inert. | Browser | R2, R3 | Same facts in mobile surface. |
| AUTO-07 | Active detail page preserves request route. | Browser | R4 | No label; enabled action; valid first allocation step. |
| AUTO-08 | Held and unavailable comparison actions are inert. | Browser | R5 | Each visible compare action has no active allocation route. |
| AUTO-09 | Service closure is correlated with snapshot refresh. | Integration/read-only | R6 | Ordered timestamps for service, worker, snapshot, page, control. |
| AUTO-10 | Stale active control after service closure is detected. | Browser/integration | R6 | Scenario fails with evidence if a user can enter rejected route. |

## 7. Assertion Rules for Browser Tests

For every inactive action, assert all applicable facts. Do not replace these
with a color assertion:

```text
visible label matches approved wording
page document is reachable
control exposes disabled semantics
control has no allocation href or route handler
keyboard activation does not navigate
pointer interaction does not navigate
network log contains no allocation-route navigation from the control
```

For an active action, assert the inverse only where it is part of the product
contract:

```text
no inactive-state label is rendered
control is enabled
destination is present and points to the approved allocation entry point
first allocation step renders a valid application state
```

## 8. Transition-Window Observation

The transition scenario is not a sleep-based test. It captures facts at each
boundary:

| Timestamp | Observation | Evidence |
| --- | --- | --- |
| T0 | Active detail page and working allocation route. | Snapshot payload, DOM, route response. |
| T1 | Allocation service closes the item. | Read-only service response or allocation record. |
| T2 | Publication worker accepts or processes the change. | Read-only job status and event time. |
| T3 | Published snapshot receives non-active state. | Versioned payload and timestamp. |
| T4 | Detail page renders label and disables every action. | Scoped UI artifact and DOM facts. |

The test classifies outcomes:

- `safe`: action is inert by T1, even if snapshot label arrives later;
- `publication-delay`: snapshot stays old because the worker is delayed or
  failed; this is not automatically a page-component defect;
- `unsafe-transition`: service is closed but an active page action can reach a
  rejection route; fail AUTO-10 with complete timing evidence;
- `final-state-defect`: snapshot is new but page label or action is wrong.

## 9. Example Test Intent

The agent may generate project-native code from this specification. Its intent
must remain equivalent to this outline:

```ts
test("unavailable detail action cannot start allocation", async ({ page, candidate }) => {
  await page.goto(candidate.detailRoute);
  await expect(page.getByTestId("allocation-state")).toHaveText("Currently unavailable");
  const action = page.getByTestId("request-allocation");
  await expect(action).toBeDisabled();
  await expect(action).not.toHaveAttribute("href", /allocate/);
  await action.focus();
  await page.keyboard.press("Enter");
  await expect(page).toHaveURL(candidate.detailRoute);
});
```

The selector names are illustrative. A real agent must use stable selectors or
the project's approved locator strategy, not invent production selectors.

## 10. Synthetic Execution Record

The following record demonstrates how a completed automation artifact reports
facts. It is fictional and must never be copied as a result for a real task.

| Scenario | Profile | Result | Factual evidence |
| --- | --- | --- | --- |
| AUTO-01 | contract | passed | `held` payload mapped to `On hold`. |
| AUTO-02 | contract | passed | `unavailable` payload mapped to `Currently unavailable`. |
| AUTO-03 | desktop | passed | Held page reachable; disabled button; no destination. |
| AUTO-04 | mobile | passed | Held sticky action disabled; no navigation. |
| AUTO-05 | desktop | passed | Unavailable label and inert action matched contract. |
| AUTO-06 | mobile | passed | Unavailable sticky action had no allocation destination. |
| AUTO-07 | desktop | passed | Active candidate had no label and reached valid allocation step. |
| AUTO-08 | desktop and mobile | passed | All observed comparison actions were inert for non-active candidates. |
| AUTO-09 | read-only timeline | passed | Service closure, snapshot refresh, and page update were timestamped. |
| AUTO-10 | transition | passed | No active request action remained after service closure in the observed run. |

## 11. Required Evidence Package

For an actual task, preserve:

1. runner summary with scenario IDs and exact status;
2. candidate discovery record with sanitized identifiers or private storage
   reference;
3. scoped screenshots for static state and video for interaction flows where the
   action itself must be visible;
4. DOM/semantic facts for disabled controls and destination absence;
5. timestamped service, publication, and snapshot observations for transition
   scenarios;
6. a short report explaining failures, skips, and limits.

## 12. Automation Limits

This artifact does not authorize a release. It does not prove that labels are
visually acceptable, that every assistive technology communicates state well,
or that a human-controlled allocation flow is complete. Those claims require
the separate manual test artifact and final report.
