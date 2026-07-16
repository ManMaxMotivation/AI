# Four-Stage QA Methodology

## Purpose

This repository demonstrates a repeatable way to make complex QA work easier
to review, reproduce, and extend. It is inspired by real delivery practice,
but all included data, scenarios, names, and artifacts are synthetic.

The method is designed for changes where a narrow requirement can affect
multiple layers, such as data compatibility, routing, state persistence, API
contracts, or user-visible behavior.

## The Four Stages

### 1. Analysis

Start with a concise, sanitized brief: the change, acceptance criteria, known
risks, and constraints. Identify the behavioral surface and regression zones.
Then assign stable requirement IDs in `verification.yaml`. The output is not a
claim that every risk is covered; it is a reviewable list of what must be
considered.

### 2. Algorithm

Convert the analysis into a sequence of observable verification steps. State
which facts should be compared and which evidence makes the result repeatable.
For example, a state-persistence change needs the source state, destination
state, URL representation, and an independent control flow.

### 3. Automated Checks

Automate deterministic, high-signal assertions where they are appropriate. A
team exports relevant facts from its approved unit, contract, API, integration,
browser, or data tooling as local JSON. `qa-case-pipeline verify` evaluates
declarative JSON-Pointer assertions against those files and writes a report
mapped to requirement IDs. Automation produces evidence; it is not a blanket
release approval.

### 4. Manual Exploratory Checks

Use human investigation for scenarios that need product context, visual
inspection, accessibility judgment, unexpected paths, imperfect data, and
cross-system behavior. Manual work begins from the automated evidence and
deliberately looks beyond it.

## How This Changes the Workflow

Without a shared structure, a complex change can require repeated discussion,
separate test notes, one-off checks, and later reconstruction of why a result
was trusted. The four-stage package puts the reasoning and evidence next to
each other, which makes review and follow-up more efficient.

It does not remove the need for requirements, environments, observability, or
manual QA. It makes assumptions, remaining risk, and the automation boundary
visible instead of leaving them implicit.

## AI Boundary

Codex may help draft a plan from a sanitized brief, but its response is
constrained by a JSON schema and must be reviewed. The integration:

- uses a temporary working directory and read-only sandbox;
- does not pass a target repository to Codex;
- does not run a target project's commands;
- keeps the final decision with the engineer or QA specialist.

Never supply secrets, private URLs, personal data, customer data, proprietary
code, or internal trackers in a public brief or generated artifact.

## Current Demonstrations

`reservation-state-propagation` is the complete primary template. It checks a
state contract across a page, desktop/mobile actions, a comparison surface, and
a transition window where two systems are temporarily inconsistent.
`ui-state-persistence` and `schema-legacy-compat` remain small synthetic
reference fixtures for focused checks. All examples are deliberately local and
synthetic.
