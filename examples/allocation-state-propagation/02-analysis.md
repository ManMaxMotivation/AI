# Analysis: Allocation State Propagation

> Synthetic worked example. Facts, system names, paths, identifiers, and
> outcomes are fictional. The structure demonstrates the expected depth of an
> analysis artifact.

## 1. Change in Plain Language

The item detail page previously treated every published item as allocatable. It
rendered **Request allocation** as a normal link based only on the public item
identifier. The new behavior introduces a state component that explains why an
item is temporarily or permanently unavailable and prevents the customer from
starting an allocation route that the service will reject.

This is not only a visual change. The label, the enabled state of the action,
the destination URL, the published payload, and the allocation service must
agree. The highest-risk moment is the period after the allocation service has
closed the item but before the catalog snapshot has refreshed.

## 2. Sources Reviewed and Their Authority

| Source | Authority | What it establishes |
| --- | --- | --- |
| Task brief and acceptance criteria | Product scope | Required states, labels, and user-visible behavior. |
| Parent capability note | Cross-feature boundary | Detail page must stay reachable; deleted items remain a separate not-found case. |
| Design specification | Visual source | Label placement, wording, and disabled-action presentation. |
| Merged change set | Implementation source | State mapping, component wiring, desktop/mobile actions, and comparison surface. |
| Existing allocation contract tests | Data-contract source | Legal values and transition rules for `allocation_state`. |
| Existing route atlas entries | Reuse source | Known allocation, browser, and snapshot-refresh paths. |
| Published build metadata and test environment | Delivery source | Whether the changed code is actually present in the environment. |

The task brief is authoritative for acceptance criteria. The design
specification is authoritative for visible labels. The merged change and its
tests are authoritative for current implementation behavior. A prior backend
test may supply a route or candidate state, but it does not prove this
page-level change.

## 3. Requirement and DoD Matrix

| ID | Requirement | Evidence needed | Not sufficient on its own |
| --- | --- | --- | --- |
| R1 | Held page remains reachable and labelled. | Published payload, rendered title area, disabled desktop/mobile action. | A service-level state value alone. |
| R2 | Unavailable page remains reachable and labelled. | Same three layers as R1. | A screenshot without payload or action state. |
| R3 | Inactive actions cannot navigate. | DOM semantics, absence of destination, pointer/keyboard behavior. | A visually grey control. |
| R4 | Active path remains usable. | Active payload, enabled action, allocation route reaches its expected first step. | A disabled-state test only. |
| R5 | Comparison surface follows the rule. | Every independently rendered compare action. | Detail-page result. |
| R6 | Transition window is safe. | Timed service result, snapshot result, visible action state. | Final snapshot after propagation. |

## 4. State Contract and Terminology

The technical state and customer wording deliberately differ for one branch.
The test must verify both layers instead of assuming that a visible phrase is
the raw API value.

| Allocation record | Published payload | Label | Request action |
| --- | --- | --- | --- |
| no current allocation | absent or `active` | no label | enabled with allocation destination |
| temporary hold | `held` | On hold | disabled; no destination |
| completed allocation or removal from stock | `unavailable` | Currently unavailable | disabled; no destination |

An unsupported value is not accepted by the contract. If it appears in a
published payload, it is a data-contract defect and not a reason to silently
fall back to an active request action.

## 5. Changed Surface and Dependencies

The fictional implementation has these responsibilities:

| Layer | Responsibility | Regression risk |
| --- | --- | --- |
| Allocation domain | Converts allocation lifecycle to public state. | A transition maps to the wrong public value. |
| Publication worker | Copies the state into a versioned catalog snapshot. | Snapshot is stale, incomplete, or delayed. |
| Item page loader | Reads the snapshot and computes page state. | Missing field becomes an unsafe default. |
| State label component | Renders label and accessible text. | Wrong label, missing state, or inaccessible announcement. |
| Desktop action component | Removes allocation navigation when inactive. | Looks disabled but retains a link. |
| Mobile sticky action | Receives the same state independently. | Desktop is fixed while mobile remains active. |
| Comparison component | Renders a separate request action. | Secondary flow bypasses the rule. |
| Allocation route | Rejects a non-active item. | Correct rejection can still become a poor user journey. |

The state is asynchronous. The normal timeline is:

```text
customer request -> allocation service closes item -> publication worker ->
catalog snapshot -> item page reload -> visible label and disabled action
```

The allocation service may close the item before the snapshot changes. The
detail page therefore needs a safe interim behavior, not merely a correct final
render.

## 6. Delivery Status

The synthetic change set is assumed merged into the target branch. The delivery
preflight must still prove that the test environment serves a build containing
the change. A green source pipeline does not prove that the browser environment
has the same revision.

Required delivery facts:

1. identify the target change and its parent revision;
2. verify the deployment or publishing job completed;
3. verify the visible build metadata contains the target revision;
4. distinguish deployment evidence from visual verification.

## 7. How the Feature Worked Before

Before the change, the detail page built its request action from the item ID.
It did not read `allocation_state`, did not show a status label, and did not
change behavior for a held item. If the allocation service had already rejected
the item, a customer could still click the page action and reach a generic
failure route.

The prior behavior was especially misleading during publication delay: the
customer saw an apparently available item even though the service had already
made the allocation impossible.

## 8. How the Feature Should Work Now

The page computes a single view state from the published payload and passes it
to each relevant surface. A non-active state must:

1. retain a reachable item page;
2. render the product-approved label;
3. disable desktop and mobile actions;
4. remove the allocation destination rather than relying only on styling;
5. apply the same rule to independently implemented comparison controls.

The active state remains a control branch. It proves that the feature has not
turned the page into a permanently disabled experience.

## 9. Route Reuse Decision

The route atlas contains two relevant generic entries:

- **Allocation lifecycle and published snapshot**: use it to identify a
  candidate item, observe service closure, and follow publication evidence.
- **Browser action-state evidence**: use it to verify a visible control,
  destination semantics, and a neighboring UI surface.

These routes provide verified entry points and evidence expectations. They do
not close R1-R6 by themselves because this task introduces new labels and a new
cross-surface state rule. The task algorithm must extend, not duplicate, them.

## 10. Risks and Regression Zones

| Risk | Why it is plausible | Required coverage |
| --- | --- | --- |
| Wrong label for unavailable | Product wording and technical value differ. | Payload-to-label assertion and manual design review. |
| Link remains actionable | A component can use disabled styling around an anchor. | DOM, keyboard, pointer, and destination checks. |
| Mobile omission | Sticky mobile action is a separate component. | Dedicated mobile scenario. |
| Compare omission | Compare owns a separate action implementation. | Each compare action location. |
| Active regression | Shared state utility can disable the normal path. | Active page and allocation route. |
| Snapshot lag | Service and page read different sources. | Timestamped transition observation. |
| Delivery confusion | Environment can serve an older build. | Build metadata before browser conclusion. |
| Deleted-item confusion | Not-found behavior must remain distinct. | Negative scope confirmation; no substitute state label. |

## 11. Automation and Manual Boundary

Automation is appropriate for payload contracts, DOM state, destination
semantics, route response, and repeatable transition observations. A browser
test can assert that a control is a disabled button without a destination.

Manual testing is still required for label legibility, visual placement,
keyboard experience, the complete allocation journey where human confirmation
is needed, and any transition that requires approved state creation. A passing
browser script is not a visual or product-judgment verdict.

## 12. Constraints and Open Questions

1. Candidate items are volatile. The algorithm must discover current candidates
   from approved sources instead of embedding old permanent links.
2. Creating a true `held` or `unavailable` state may be a user-controlled or
   environment-controlled action. The agent remains read-only until explicitly
   authorized.
3. If the publication worker is unavailable, the page result cannot be
   classified as a front-end regression without first recording the delivery
   blocker.
4. The product owner must confirm whether the comparison surface is in scope if
   the written task names only the detail page. The risk is documented because
   it exposes the same allocation action.
5. The desired fallback during snapshot lag must be explicit. If the page lacks
   a live availability check, the team may need a separate requirement rather
   than silently accepting a service rejection.

## 13. Analysis Conclusion

The task is a cross-layer state-propagation change, not a label-only UI task.
Coverage must prove the state contract, final page behavior, independent action
surfaces, active baseline, and the time boundary between service closure and
published snapshot. The next artifact defines a staged, read-only-first route
and separates user actions from agent actions.
