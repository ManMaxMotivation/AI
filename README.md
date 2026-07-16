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
| [`SKILL.md`](skills/ai-assisted-qa/SKILL.md) | The agent workflow: analysis, verification algorithm, automated evidence, and manual exploration. |
| [Artifact contract](skills/ai-assisted-qa/references/artifact-contract.md) | Required structure and quality criteria for each QA artifact. |
| [Risk patterns](skills/ai-assisted-qa/references/risk-patterns.md) | Reusable reasoning for UI state, API contracts, data migrations, and asynchronous propagation. |
| [Staged session prompts](skills/ai-assisted-qa/references/staged-session-prompts.md) | Four separate terminal prompts that keep the engineer in control between QA stages. |
| [Route memory protocol](skills/ai-assisted-qa/references/route-memory.md) | A `compare -> reuse/update/add` method for reusing proven QA routes. |
| [Eleven principles](skills/ai-assisted-qa/references/eleven-principles.md) | The non-negotiable operating rules distilled from a mature QA workflow. |
| [Project rule snippet](skills/ai-assisted-qa/assets/project-agent-rules.md) | A short rule block to add to a project's local agent instructions. |
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

Copy the contents of
[`project-agent-rules.md`](skills/ai-assisted-qa/assets/project-agent-rules.md)
into your project's local agent instruction file. This tells the agent where to
save artifacts and prevents it from treating a partial check as complete.

### 3. Run the Task in Controlled Stages

Do not ask the agent to analyze, test, and report everything in one turn. Use
the four [staged session prompts](skills/ai-assisted-qa/references/staged-session-prompts.md)
as separate Codex terminal messages:

```text
1. Analysis -> inspect the agent's understanding and scope.
2. Algorithm -> inspect the route, evidence, and stop conditions.
3. Automated evidence -> authorize only the checks you accept.
4. Manual test case -> review human scenarios before execution.
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
  automated-checks.md     Reusable checks and actual execution evidence
  manual-test-cases.md    Exploratory and human-only scenarios
  report.md               Requirement/DoD traceability and factual outcome
```

## The Four-Stage Method

1. **Analysis**: establish the source of truth, full scope, changed behavior,
   dependencies, regression zones, and unresolved questions.
2. **Algorithm**: turn the analysis into an ordered, evidence-backed path. It
   states which layer is checked, by which tool, and when to stop.
3. **Automated evidence**: reuse existing unit, contract, API, data, or browser
   checks where they fit. Run only approved, relevant checks and preserve the
   factual result.
4. **Manual exploration**: investigate what automation cannot establish:
   usability, visual quality, unusual paths, timing, external dependencies, and
   product judgment.

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

See the [synthetic example](examples/allocation-state-propagation/) for the
expected depth and artifact flow. It intentionally demonstrates a detailed
cross-layer case, not a short generic checklist.

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
