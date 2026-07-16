# Analysis

## Sources and Scope

The task brief is the source of acceptance criteria. The relevant behavioral
chain is reservation service -> page snapshot -> item page -> comparison view
-> checkout action.

## Changed-Risk Zones

| Risk | Why it matters | Required treatment |
| --- | --- | --- |
| State mapping | A technical state can show the wrong customer label. | Check every supported state and its label. |
| Secondary action | A desktop fix can leave mobile or compare actionable. | Inspect each independently implemented action. |
| Propagation delay | Service and page snapshot can disagree temporarily. | Check final state and stale-page interval. |
| Baseline regression | Disabling all actions breaks available inventory. | Prove normal available flow remains active. |

## Scope Decision

Desktop, mobile, comparison, available, reserved, unavailable, and the
propagation interval are in scope. Visual accessibility and real interaction
remain manual because a service assertion cannot prove them.

## Constraints and Open Questions

- The approved test environment must provide each reservation state or a safe
  way to create it.
- The final user-facing label is a product decision and must be confirmed from
  the current requirement, not inferred from the technical state name.
- The propagation interval requires timestamped evidence from both the checkout
  boundary and the page state; the final page alone is insufficient.
