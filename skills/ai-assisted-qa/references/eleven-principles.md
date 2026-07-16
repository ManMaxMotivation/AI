# Eleven Principles of AI-Assisted QA

1. **Gate each artifact.** Analyze, algorithmize, automate, write manual cases,
   and report in separate user-controlled sessions.
2. **Start from sources of truth.** Requirements, DoD, code, approved tests,
   and confirmed artifacts outrank assumptions.
3. **Map full changed risk.** Do not reduce scope to a happy path without an
   explicit risk-based reason.
4. **Reuse proven routes first.** Search route memory and similar algorithms
   before exploring a familiar system from scratch.
5. **Keep route memory healthy.** At algorithm completion use
   `compare -> reuse/update/add`; add only proven reusable routes.
6. **Separate knowledge types.** Reusable routes, process barriers, and
   task-specific root cause belong in different records.
7. **Choose the smallest proving layer.** Use the narrowest native test layer
   that establishes the behavior; do not run a matrix by habit.
8. **Keep automation and manual work distinct.** A green API or unit result
   does not prove visual, accessibility, timing, or user-flow behavior.
9. **Stop on facts.** Record exact blockers and request a handoff instead of
   retrying guesses or presenting a partial result as a pass.
10. **Preserve literal traceability.** Every report conclusion must point to a
    requirement, evidence source, factual status, and the approved manual step
    it represents; do not compress the manual run into a summary.
11. **Protect private context.** Treat work artifacts as private, publish only
    synthetic reconstructions, and review both secrets and business-sensitive
    details before release.
