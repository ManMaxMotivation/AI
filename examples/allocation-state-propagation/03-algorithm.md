# Verification Algorithm: Allocation State Propagation

> Synthetic worked example. This algorithm is intentionally detailed to show
> how analysis becomes an executable QA route. Replace fictional names, tools,
> and entry points with approved project-specific ones.

## 1. Case Signature

| Field | Value |
| --- | --- |
| Change class | Cross-layer state propagation and action-state UI behavior |
| Primary risk | The allocation service rejects an item while a stale page still offers an active request action. |
| Data direction | Allocation record -> publication worker -> catalog snapshot -> item detail and comparison UI |
| Required states | `active`, `held`, `unavailable` |
| User-facing surfaces | Detail page desktop, detail page mobile sticky action, comparison page, allocation route |
| Evidence classes | Contract payload, browser DOM, route response, publication timing, manual visual evidence |
| Mutation policy | Read-only by default; a person performs any state-creating action after approval. |

## 2. Sources Used for This Algorithm

1. The approved analysis artifact for this task.
2. The task brief and acceptance criteria.
3. The project's private route atlas and barrier registry.
4. Existing allocation contract tests and browser-suite conventions.
5. The merged implementation and delivery metadata.

No old candidate URL, item ID, or test record is assumed permanent. A prior case
can supply a route pattern but not fresh test data or proof for the current
task.

## 3. Preconditions and Read-Only Preflight

Before a browser run or a state-changing handoff, the agent confirms:

| Check | Evidence | Stop if |
| --- | --- | --- |
| Code delivery | Target revision is present in test-environment build metadata. | Build is older or cannot be identified. |
| Route atlas | Matching allocation and browser routes are current enough to reuse. | Route conflicts with current code or requirement. |
| Test runner | Project-native browser/API runner is available and its health check passes. | Runner or approved environment is unavailable. |
| Candidate source | Current catalog can provide active, held, and unavailable candidates. | A state cannot be observed or safely created. |
| Publication evidence | Worker/job logs or equivalent read-only telemetry can be inspected. | Snapshot timing is required but telemetry is unavailable. |
| Design source | Current approved labels and placement are available. | Visual requirement is ambiguous. |

The agent records an exact blocker at this stage. It does not compensate by
inventing a route, using stale test data repeatedly, or declaring the feature
passed from source code alone.

## 4. Route Memory Decision

### Reused Routes

| Route family | Reused portion | Why it is safe to reuse |
| --- | --- | --- |
| Allocation lifecycle | Candidate discovery, service-closure observation, state timestamp capture | The service lifecycle is unchanged by the page component. |
| Published snapshot | Locate snapshot version and compare payload before/after allocation | The page still consumes the standard published snapshot. |
| Browser action evidence | Inspect visible control, semantic role, destination, keyboard behavior | The project has an approved evidence convention for interactive controls. |

### Task-Specific Additions

The current task adds label semantics and a shared disable rule across detail,
mobile, and comparison surfaces. Those assertions are new and belong in the
task artifact. After verification, update the route atlas only if the complete
state-propagation path is proven reusable for another task class.

### Atlas Synchronization Decision

At the end of this phase, compare the discovered route with the existing atlas:

- **Reuse** if the existing route already describes the verified path.
- **Update** if the route remains valid but needs a new evidence or stop rule.
- **Add** only if this task proves a new repeatable path.

Do not add exact item identifiers, temporary data, personal handoffs, or a
one-off defect cause to route memory.

## 5. Coverage Route

### Step 1: Confirm Delivery and State Contract

**Risk covered:** browser tests target an old build or an unsupported state.

1. Confirm the environment build contains the target change.
2. Read the state contract or contract tests for `active`, `held`, and
   `unavailable`.
3. Confirm the item loader reads the published field and that the state utility
   has an explicit non-active branch.
4. Record the approved visible label for each non-active state.

**Evidence:** build revision, contract output or test result, implementation
mapping, design wording.

**Pass condition:** delivery and state contract are independently confirmed.

### Step 2: Select and Validate Candidates

**Risk covered:** a stale or invalid candidate invalidates later conclusions.

For each required state, collect a fresh candidate record:

| Field | Active | Held | Unavailable |
| --- | --- | --- | --- |
| Public item identifier | required | required | required |
| Detail page entry point | required | required | required |
| Published snapshot version | required | required | required |
| `allocation_state` | `active` or absent | `held` | `unavailable` |
| Service allocation response | allocatable | rejected or held | rejected |
| Comparison entry point | required when in scope | required when in scope | required when in scope |
| Timestamp captured | required | required | required |

Validate every candidate before it becomes test data. A page that is already
deleted, a snapshot that does not contain the item, or a service response that
does not match the expected state is not a valid candidate.

### Step 3: Verify Final Held State

**Risk covered:** held item is hidden, mislabeled, or still actionable.

1. Open the held item detail page in the desktop profile.
2. Confirm a reachable page and the `held` value in the published snapshot.
3. Confirm **On hold** is visible in the title area.
4. Inspect every desktop request control: it is disabled, has no allocation
   destination, and cannot be activated by pointer or keyboard.
5. Repeat for the mobile sticky action in a dedicated mobile profile.

**Evidence:** snapshot excerpt, scoped desktop and mobile visual artifact, DOM
semantics, action destination state.

### Step 4: Verify Final Unavailable State

**Risk covered:** permanent state maps to the wrong label or leaves a bypass.

Repeat Step 3 for an `unavailable` candidate. Confirm **Currently unavailable**
instead of the raw technical value. Inspect desktop, mobile, and every visible
request action separately.

### Step 5: Verify the Active Baseline

**Risk covered:** a shared disable rule breaks normal allocation.

1. Open a current active candidate.
2. Confirm no allocation-state label is shown.
3. Confirm the desktop action is enabled and has the expected destination.
4. Confirm the route reaches the first valid allocation step without a generic
   unavailable failure.
5. Repeat the mobile action only if it is separately implemented or changed.

The active path is not a secondary nice-to-have. It is the control condition
for the state utility.

### Step 6: Verify Independent Comparison Actions

**Risk covered:** detail-page coverage hides a second implementation defect.

For held and unavailable candidates, inspect each comparison action location:

1. card-level action;
2. summary or footer action;
3. mobile action, if the comparison surface has one.

For each location, record role, enabled state, destination, and actual result.
If the comparison product scope is later excluded, preserve that decision and
its owner in the report; do not silently drop the risk.

### Step 7: Observe the Propagation Window

**Risk covered:** customer enters a service-rejected route while page snapshot
is stale.

This step needs a controlled state transition. The agent remains read-only until
the user confirms that the approved environment and candidate may be changed.

1. Establish `T0`: active page, active action, working allocation route, and
   baseline snapshot.
2. The user completes the approved allocation action or creates the approved
   test state.
3. The agent records, without mutation:
   - first service rejection time;
   - first publication-worker event;
   - first updated snapshot time;
   - first page render with label;
   - first disabled action time.
4. If an action remains active after service rejection, demonstrate the user
   outcome only when safe and authorized. Record it as a transition defect.
5. Continue until the final snapshot and visible action agree, or stop on a
   publication blocker.

**Required conclusion:** distinguish a page-component defect, publication delay,
and safe interim behavior. Do not collapse them into one result.

### Step 8: Classify and Preserve Evidence

Classify each failed observation before proposing a fix:

| Observation | Likely owning layer | Required next evidence |
| --- | --- | --- |
| Snapshot has state, label absent | Page state mapping or label component | DOM and implementation trace. |
| Label exists, action still navigates | Action component or state propagation | DOM semantics and action wiring. |
| Desktop safe, mobile active | Mobile-specific component | Mobile DOM and component input trace. |
| Page snapshot stale after service closure | Publication or interim-product behavior | Worker timeline and timestamp comparison. |
| Snapshot never changes | Upstream publication/data layer | First failing worker task and input state. |
| Active item disabled | Shared state utility or fallback | Active payload and computed view-state trace. |

Preserve artifacts under the task directory with sources and timestamps. Update
route memory only after a route is confirmed, not merely attempted.

## 6. Minimal Fast Path

Use the full route above for release evidence. A focused diagnostic rerun may
use this short path only when the relevant candidates and routes are already
proven:

1. Confirm the environment revision.
2. Open one exact candidate and inspect the changed control.
3. Capture the expected payload and DOM facts.
4. Stop after the first factual blocker or result.

Do not use this fast path to replace state matrix, active baseline, comparison,
or propagation coverage for the original task.

## 7. User and Agent Responsibilities

### User

1. Approves the candidate and any state-changing action.
2. Performs any real allocation, administrative state change, or human
   confirmation that the agent is not authorized to perform.
3. Reports the completion time of the action when possible.
4. Reviews each staged artifact before authorizing the next phase.

### Agent

1. Works read-only until explicit authorization.
2. Validates candidates and delivery before building browser evidence.
3. Reuses approved routes before discovery.
4. Records payload, UI, service, and publication observations separately.
5. Stops on the documented conditions instead of guessing through an unstable
   environment.
6. Never reports visual or transition success from backend evidence alone.

## 8. Stop Conditions

Stop and report the exact condition when:

1. the target revision is absent from the tested build;
2. a required candidate state cannot be observed or safely created;
3. the approved browser or data contour fails preflight;
4. the published snapshot cannot be inspected when it is needed for the claim;
5. a required human action has not been authorized;
6. the publication worker fails before the page can receive new state;
7. a product requirement leaves the transition fallback ambiguous.

## 9. Expected Factual Result

The completed case is valid only when the evidence can show all of the
following, or clearly identify a blocker:

- active item: no label, actionable request route;
- held item: reachable page, **On hold**, no actionable desktop or mobile
  request route;
- unavailable item: reachable page, **Currently unavailable**, no actionable
  desktop, mobile, or comparison request route;
- transition: a timed explanation of service closure, snapshot change, and
  visible action behavior;
- manual review: visual and interaction results recorded separately from
  automation.
