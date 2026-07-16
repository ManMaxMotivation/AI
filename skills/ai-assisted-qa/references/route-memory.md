# Route Memory

Route memory prevents an agent from rediscovering the same approved path for
every related task. Keep it in the target project's private QA area, for example
`qa/route-atlas.md`. Do not publish environment-specific routes, credentials,
or private entry points in this playbook.

## Mandatory Cycle

1. Classify the task and search the route atlas first.
2. Compare any matching route with the current requirement, code, and known
   constraints.
3. Reuse the route when it still proves the needed behavior.
4. Consult the project's barrier registry and similar approved algorithms if the
   route is incomplete or stale.
5. Build a task-specific route only after those sources are exhausted.
6. At the end of the algorithm phase, synchronize the atlas:
   `compare -> reuse/update/add`.

Only confirmed, repeatable routes belong in the atlas. Do not add speculative
paths, one-off root causes, credentials, exact volatile test data, or shell
workarounds. Keep process barriers in a separate barrier registry and preserve
task-specific diagnosis in the task's own algorithm artifact.

## Generic Record

```markdown
### Route: <short capability name>
- When to use: <symptom or task class>
- Canonical path:
  1. <approved entry point>
  2. <verification step>
  3. <expected evidence>
- Avoid: <known stale or misleading path>
- Proof source: <private task artifact or approved runbook>
- Last verified: <date>
```

Treat a route as stale when current code, requirements, or evidence disproves
it. Replace it only with a newly proven path, not an assumption.
