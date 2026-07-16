# Synthetic Task Brief

An online catalog lets a customer reserve an item. Reservation state may change
in a service before the page snapshot refreshes. The item page must show a
clear state, disable the reservation action when appropriate, and preserve the
normal flow for an available item.

## Acceptance Criteria

1. Reserved and unavailable items remain viewable with a clear label.
2. Disabled actions do not navigate to checkout on desktop, mobile, or compare
   views.
3. Available items retain the existing checkout flow.
4. During propagation delay, a stale page does not expose an actionable path
   that leads to a known unavailable checkout.

All names, states, and values in this example are fictional.
