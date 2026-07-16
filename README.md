# AI

An open research project by `ManMaxMotivation` for building AI tools and
experiments.

The product direction and architecture will be defined through validated
research and useful implementation work. Significant changes are agreed,
tested, committed, and published to GitHub.

## Local Configuration

Create `.env` from `.env.example` when the project needs environment
variables. `.env` is not tracked by Git and must never contain information
intended for publication.

GitHub access is provided by the GitHub CLI (`gh`). Tokens are not stored in
this repository.

## Git Workflow

The default branch is `main`. Before starting an agreed task, update the local
branch with `git fetch origin` and, when the working tree is clean,
`git pull --ff-only`. After implementation and relevant checks, publish the
completed change to `origin/main` and verify the remote state.

Detailed automation and repository rules are maintained in `AGENTS.md`.
