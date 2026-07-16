# Verification Algorithm

1. Confirm the contract values for available, reserved, and unavailable state.
2. Inspect the final reserved page: page remains reachable, label is correct,
   desktop and mobile actions are disabled.
3. Inspect the final unavailable page with the same criteria.
4. Inspect the related comparison action independently.
5. Inspect an available item to prove the normal checkout action remains active.
6. Reproduce or observe the interval in which checkout rejects the item while
   the page snapshot is still stale; the page must not offer an active action.
7. Perform manual visual, keyboard, mobile, and end-to-end checks.

## Stop Conditions

- Stop and report a blocker if the approved environment or required state is
  unavailable.
- Do not claim the propagation interval is covered from the final state alone.
- Do not close visual or keyboard behavior from API evidence.

## Requirement-to-Step Mapping

| Requirement | Steps |
| --- | --- |
| State is visible and clear | 1, 2, 3, 7 |
| Disabled actions cannot navigate | 2, 3, 4, 7 |
| Available flow remains active | 5, 7 |
| Stale page is safe | 6, 7 |
