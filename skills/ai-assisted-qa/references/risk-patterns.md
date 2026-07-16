# Risk Patterns

Use these patterns to direct analysis. They are prompts for investigation, not
prewritten test cases.

## UI State and Navigation

Trace state before and after navigation, refresh, browser history, direct URL
entry, and a neighboring flow with independent state. Check the visible control,
serialized route state, and the actual result together. A valid destination does
not prove that every selected value survived.

## API or Contract Change

Check new, unchanged, absent, malformed, and legacy-compatible fields. Trace
the field from producer through transformation, storage or cache, consumer, and
visible behavior. Separate schema validity from business semantics.

## Data Migration or ETL

Identify the source record, transformation rule, idempotency key, output,
error path, and rollback or recovery expectation. Include null, historical,
duplicate, and partially migrated records. A successful batch alone does not
prove that records were transformed correctly.

## Asynchronous Propagation

Map the time boundary between each system. Test both the final consistent state
and the interval in which one system has changed while another is stale. Define
what the user is allowed to do during that interval and which safe behavior is
expected.

## Cross-Surface Behavior

When a rule appears in more than one UI or API surface, list every surface
reached by the changed state. Check a primary path and each independently
implemented action. Do not assume that a shared label or a successful desktop
test proves mobile, comparison, export, or secondary flows.
