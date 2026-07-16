# Methodology

## The Problem

Complex changes rarely fail in one isolated function. A requirement can cross a
data contract, a transformation, a cache, several UI surfaces, an asynchronous
job, and a user journey. A short test checklist often records the final action
but loses the reasoning that connects these layers.

The result is familiar: a green narrow check, a missing regression path, and no
clear explanation of what was not verified.

## The Method

The playbook makes four stages explicit.

1. **Analysis** establishes the actual scope before testing. It starts from
   requirements and code, identifies sources of truth and changed-risk zones,
   and records uncertainty instead of hiding it.
2. **Algorithm** defines the test route before execution. It makes each step,
   evidence source, tool, and stop condition reviewable.
3. **Automated evidence** proves deterministic behavior at the appropriate
   layer. It is not expanded into a broad matrix without a changed-risk reason.
4. **Manual exploration** investigates the gaps automation cannot honestly
   close: visual quality, accessibility, timing, user understanding, and
   external or human handoffs.

The report connects each requirement or DoD point to these stages. It is a
decision record, not a substitute for product or release ownership.

## Why AI Helps

An AI agent is useful when it follows a fixed reasoning discipline: reading
sources before proposing coverage, locating dependencies, separating fact from
assumption, and maintaining traceability. It is not useful when it invents a
generic test plan or announces success without evidence.

The skill in this repository provides the discipline. The engineer retains
control of the environment, the final test scope, and the conclusion.

## Practical Boundaries

- Reuse project-native tests and approved routes before creating new machinery.
- Test the whole changed behavioral scope, not an arbitrary smoke subset.
- Do not turn an unavailable environment, missing access, or unexecuted manual
  scenario into a pass.
- Do not put private work artifacts into public examples.
