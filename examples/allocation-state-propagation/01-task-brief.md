# Synthetic Task Brief: Allocation State on an Item Detail Page

> This is a fictional reconstruction for learning. It is not copied from a
> customer task, application, test environment, or source repository.

## Product Context

Example Equipment Marketplace is a fictional marketplace for reservable
equipment. A customer opens an item detail page and can select **Request
allocation**. A successful request temporarily holds the item; a completed
transaction makes it unavailable. The catalog page is rendered from a published
snapshot, while the allocation service makes the item unavailable immediately.

## Requested Change

Add an allocation-state component to the item detail page.

The published item payload has the field `allocation_state`:

| Technical value | Customer-facing meaning | Expected page behavior |
| --- | --- | --- |
| absent or `active` | Item can be requested | No status label; request action is enabled. |
| `held` | A temporary allocation exists | Show `On hold`; disable every request action. |
| `unavailable` | Item can no longer be allocated | Show `Currently unavailable`; disable every request action. |

The page must remain reachable for `held` and `unavailable` items. Those states
are not equivalent to a deleted item.

## Acceptance Criteria

1. The detail page stays available for all three supported states.
2. `held` displays **On hold** and `unavailable` displays **Currently
   unavailable** in the title area.
3. Desktop and mobile request actions are disabled and have no allocation URL
   when the item is not active.
4. The existing active-item allocation path continues to work.
5. Related comparison surfaces do not expose an active allocation action for a
   held or unavailable item.
6. During propagation from the allocation service to the published snapshot, a
   customer must not be sent from an apparently active action to a known
   unavailable allocation route.

## Explicit Non-Goals

- Redesigning the allocation flow.
- Hiding held or unavailable items from search.
- Changing the business rule that decides whether an item can be allocated.
- Replacing the standard not-found page for genuinely deleted items.

## Known Delivery Constraint

The service decision and the page snapshot can update at different times. A
valid final-state check alone cannot prove safe behavior during this interval.
