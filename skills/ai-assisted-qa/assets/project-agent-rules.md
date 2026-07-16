# AI-Assisted QA Rule

For every non-trivial QA task, use the `ai-assisted-qa` workflow before giving a
final verdict. Save `analysis.md`, `algorithm.md`, `automated-checks.md`,
`manual-test-cases.md`, and `report.md` under `qa/<task-id>/`.

Read the task, acceptance criteria, relevant code, existing tests, and related
artifacts before selecting coverage. Preserve the full changed-risk scope or
state a factual reason for each exclusion. Keep automated and manual evidence
separate. Record blocked and not-run work explicitly; never infer a pass from
an unavailable environment or partial check.

Use repository-native test tooling and approved environments. Do not run
destructive production operations. Do not place credentials, private URLs,
personal data, internal IDs, or proprietary artifacts in public outputs.
