# AI-Assisted QA Playbook

This repository is a reusable QA workflow for people who use an AI agent while
testing complex product changes. It is not a test runner and it does not impose
a framework, language, or CI stack.

The practical value is a portable **skill**: install it in an agent-enabled
project and the agent follows a disciplined sequence instead of jumping from a
ticket straight to a few happy-path checks.

## Who This Is For

- QA engineers and SDETs who want repeatable analysis and reporting.
- Developers who need to test a change across code, API, data, and UI layers.
- QA leads who want an AI agent to produce consistent, reviewable artifacts.

## What You Can Take Into Your Project

| Resource | What it gives you |
| --- | --- |
| [`SKILL.md`](skills/ai-assisted-qa/SKILL.md) | The full agent contract: analysis, algorithm, executable automated evidence, approved manual test case, and final report. |
| [Artifact contract](skills/ai-assisted-qa/references/artifact-contract.md) | Detailed required structure, naming, traceability, and quality criteria for every artifact. |
| [Risk patterns](skills/ai-assisted-qa/references/risk-patterns.md) | Reusable reasoning for UI state, API contracts, data migrations, and asynchronous propagation. |
| [Controlled session templates](skills/ai-assisted-qa/references/staged-session-prompts.md) | Five complete terminal messages: analysis, algorithm, automated checks, manual test case, and report. |
| [Final report template](skills/ai-assisted-qa/references/final-report-template.md) | Step-for-step report form with preflight rules that prevent compressed or invented outcomes. |
| [Route memory protocol](skills/ai-assisted-qa/references/route-memory.md) | A `compare -> reuse/update/add` method for reusing proven QA routes. |
| [Eleven principles](skills/ai-assisted-qa/references/eleven-principles.md) | The non-negotiable operating rules distilled from a mature QA workflow. |
| [Project `AGENTS.md` rule set](skills/ai-assisted-qa/assets/project-agent-rules.md) | A complete local rule set to merge into a project's agent instructions. |
| [Complete synthetic example](examples/allocation-state-propagation/) | Six detailed artifacts, from task brief to final report, with no real system data. |

## Adopt the Workflow

### 1. Install the Skill for Codex

Clone this repository and copy the skill into your local Codex skills folder:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/ai-assisted-qa "${CODEX_HOME:-$HOME/.codex}/skills/"
```

For another AI agent, provide `SKILL.md` and its `references/` directory as the
agent's operating instructions. The workflow is tool-agnostic.

### 2. Add the Project Rule

Merge the contents of
[`project-agent-rules.md`](skills/ai-assisted-qa/assets/project-agent-rules.md)
into your project's local `AGENTS.md`, then configure only the local artifact
root, permitted contours, and validators. This installs the full artifact and
reporting contract, not a generic reminder.

### 3. Run the Task in Controlled Stages

Do not ask the agent to analyze, test, and report everything in one turn. Use
the five [controlled session templates](skills/ai-assisted-qa/references/staged-session-prompts.md)
as separate Codex terminal messages:

```text
1. Analysis -> inspect the complete task understanding and changed-risk scope.
2. Algorithm -> inspect reproducible routes, evidence, stop conditions, and handoffs.
3. Automated checks -> inspect executable checks, factual results, and evidence.
4. Manual test case -> approve complete human steps before they are saved.
5. Final report -> verify that actual evidence and approved steps are represented 1:1.
```

Each phase uses the approved artifact from the prior phase as its source of
truth. The agent must not move ahead on its own.

### 4. Give the Agent a Real Task

Use a direct request such as:

```text
Use $ai-assisted-qa for this task. Read the requirements, relevant code and
existing tests. Create the full QA artifact chain under qa/<task-id>/.
Do not run production mutations or claim a result that is not evidenced.
```

The agent should create this chain:

```text
qa/<task-id>/
  analysis.md             Scope, requirements, dependencies, risks, blockers
  algorithm.md            Verification sequence, evidence, stop conditions
  automated-checks-report.md  Automated scope, actual results, and evidence
  autotest.<ext>              Rerunnable check, only when one exists
  evidence-*.zip              Factual output package, only when needed
  manual-test-cases.md        Approved human scenarios
  report.md                   Step-by-step factual outcome and DoD traceability
```

## The Five-Artifact Method

1. **Analysis**: establish sources of truth, delivery status, full changed
   behavior, dependencies, risks, regression zones, and unresolved questions.
2. **Algorithm**: turn the analysis into an ordered, reproducible route with
   read-only preflight, entry points, evidence, responsibilities, and stops.
3. **Automated checks**: create and run risk-justified, repeatable tests and
   preserve their factual report and evidence. A test file is not the report.
4. **Manual test case**: prepare one complete DoD-covering human scenario with
   explicit entry points, actions, and observable expected results.
5. **Final report**: copy the approved manual steps into the factual execution
   record, add automated proof, artifacts, immutable DoD, and remaining risk.

The final report does not replace a release decision. It makes the evidence,
remaining uncertainty, and manual judgment visible to the person making one.

## Route Memory: Faster Without Losing Coverage

Mature QA teams do not rediscover every browser path, data chain, or diagnostic
sequence from scratch. Keep a private route atlas inside the target project.
Before building a new algorithm, the agent searches for a matching proven route
and reuses it when it remains valid. At the end of the algorithm phase it
synchronizes the atlas with `compare -> reuse/update/add`.

This preserves verified knowledge across related tasks while keeping one-off
incidents and process barriers out of the route map. The full protocol and a
generic record format are in
[route-memory.md](skills/ai-assisted-qa/references/route-memory.md).

## The Eleven Principles

The playbook's core discipline is summarized in
[Eleven Principles of AI-Assisted QA](skills/ai-assisted-qa/references/eleven-principles.md).
They cover phased control, source authority, risk-based coverage, route reuse,
evidence integrity, stopping rules, and publication safety.

## Why This Is Different From a Generic Test Checklist

A checklist often loses the link between a requirement, the changed code or
data, the automated result, and the manual observation. This workflow requires
that link. It also prevents two common failures:

- reducing a complex task to a happy-path smoke check without a risk-based
  reason;
- claiming that an automated green run covers UI, data propagation, or user
  behavior that it did not observe.

See the [synthetic example](examples/allocation-state-propagation/) and the
[complete session templates](skills/ai-assisted-qa/references/staged-session-prompts.md)
for the expected depth and artifact flow. The templates are intentionally
operational: another project can take them, set local paths and tools, and use
the same staged control without inheriting private project data.

## Safety and Publication

This repository deliberately contains no copied work artifacts. Before using a
case as a public example, follow the
[publication-safety checklist](docs/publication-safety.md). It covers tokens,
credentials, private URLs, customer and test data, internal identifiers,
screenshots, logs, and proprietary implementation details.

Automated secret scanning runs for pushes and pull requests. It is a safety net,
not a replacement for human review.

## Scope

The playbook supplies a method and agent instructions. It does not promise that
an LLM can independently test every system, infer missing requirements, access
private environments, or replace a QA engineer. The work remains evidence-led,
risk-based, and reviewable.

Read [docs/adoption.md](docs/adoption.md) for a step-by-step adoption guide and
[docs/methodology.md](docs/methodology.md) for the rationale behind the method.
