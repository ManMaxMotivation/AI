---
name: ai-assisted-qa
description: "Run a controlled, artifact-led QA workflow for a complex product task: full analysis, a reproducible verification algorithm, executable automated checks with evidence, an approved manual test case, and a traceable final report. Use for QA analysis, code or pull-request review, test design, automated verification, manual test cases, and QA reports."
---

# AI-Assisted QA

This skill is an operating contract for QA work. It is designed to prevent an
agent from guessing requirements, shrinking changed-risk scope, or treating a
planned or partial check as a result.

## Non-Negotiable Session Contract

Run only the stage explicitly requested by the user. The normal sequence is:

1. Full analysis.
2. Verification algorithm.
3. Automated checks, executable test artifacts, and factual evidence.
4. Manual test case.
5. Final QA report.

These are separate human-gated messages. Do not proceed merely because the
previous artifact appears complete. Present the complete artifact for review;
when a stage permits saving, persist the same reviewed text without silent
compression, rewording, reordering, or format normalization. A report is not a
stage-three byproduct: write it only when actual execution evidence exists and
the user asks for it.

Use the complete prompts in `references/staged-session-prompts.md`. They are
the public, portable form of the workflow. Do not replace them with a shorter
generic checklist.

## Required Sources and Preflight

Before selecting coverage, obtain every available source of truth:

- task description, status, acceptance criteria, DoD, and custom fields;
- notes, attachments, screenshots, linked/parent/sibling work;
- merged revisions, pull requests, delivery information, and existing tests;
- actual local implementation and its dependencies;
- approved prior artifacts, route memory, and process barriers.

Identify missing sources. Do not invent task intent, entry points, data,
environment state, execution results, access, or a passing outcome.

Apply `references/publication-safety.md` before reading material for public
reuse and before publishing an artifact. A public example must be independently
written and anonymized; do not copy proprietary case text, screenshots, URLs,
identifiers, logs, or test data.

## Route Memory and Barriers

Before new route discovery, search the project's private route atlas and
similar approved algorithms. Reuse a matching proven route first. At the end
of the algorithm stage, synchronize it as `compare -> reuse/update/add`.

Only confirmed, reusable routes belong in the atlas. Keep a recurring process
barrier in its barrier record. Keep one-off root cause, incident details, and
task-specific diagnosis in the task algorithm. Read
`references/route-memory.md` for the full protocol.

## Stage Requirements

### 1. Analysis

Create the full scope contract before execution. It must establish delivery
status, implementation facts, prior and intended behavior, requirement/DoD
coverage, changed surface, dependencies, state transitions, risks, regression
zones, constraints, and the automation/manual boundary. For UI work, decide
whether browser automation is both possible and needed, what it can prove, and
what remains manual.

### 2. Verification Algorithm

Create a repeatable route from preconditions to observable proof. First make a
read-only preflight of every needed contour and entry point. If a required
proof is blocked, record the exact impact and stop that branch. For every route
step, name the requirement/risk, user action, agent action, layer/entry point,
evidence, expected factual outcome, and stop condition. Keep the route focused
but do not omit a changed-risk branch merely to make it shorter.

### 3. Automated Checks and Evidence

Choose the smallest layer that actually proves each risk. Prefer existing
project-native runners. Select shell, Python, browser automation, or a native
runner deliberately and preflight the dependencies used. Run an executable
artifact end-to-end before presenting it as rerunnable or suitable for CI.

Keep three things distinct: executable checks, their factual outcome report,
and their evidence. Preserve failed and blocked scenarios. For browser-visible
behavior, leave human-readable proof: action/transition video or focused static
screenshot as appropriate. Raw logs and responses supplement, not replace,
visual evidence.

### 4. Manual Test Case

Create one complete human test case from approved evidence. It must cover the
original DoD and the human-only or independently required risk. Use explicit,
confirmed entry points and test data. A step has one concrete action and one
observable expected result. Do not duplicate automation, use placeholders in
executable technical steps, or turn internal code names into user-visible
expected results. The draft is approved before saving and then saved 1:1.

### 5. Final Report

Write only from actual execution records. The manual execution section must
repeat the approved test-case steps in the same order and detail, including
action, expected result, and actual result. Do not collapse steps. Preserve
the original DoD wording. List all relevant artifacts and their provenance.
The report may say `PASS`, `FAIL`, `BLOCKED`, `PARTIAL`, or `NOT RUN`; it may
not infer a pass from intent, a green unrelated test, or an unavailable
environment. Use `references/final-report-template.md`.

## Quality Gates

Before completing a stage, confirm that:

- all available authoritative sources were reconciled or explicitly missing;
- each selected check has a risk-based reason;
- every requirement has a proof path or an explicit blocker;
- automation and manual work are separate and neither overclaims coverage;
- actual evidence, not prose, supports every reported result;
- route-memory updates contain only proven reusable knowledge;
- the artifact has no credentials, private endpoints, personal data, internal
  identifiers, customer data, proprietary code, or copied private text;
- the final report mechanically traces to the approved test case and factual
  automated evidence.

Use `references/artifact-contract.md` as the mandatory detailed contract and
copy `assets/AGENTS.md` into a target project's local instructions when the
project needs this workflow.
