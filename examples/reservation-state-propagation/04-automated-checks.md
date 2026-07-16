# Automated Evidence Plan

| ID | Risk covered | Suitable layer | Expected evidence |
| --- | --- | --- | --- |
| AUTO-01 | State mapping | Contract/API | Each technical state maps to the expected page payload and label. |
| AUTO-02 | Disabled primary action | Browser or component | Reserved and unavailable action is disabled and has no checkout target. |
| AUTO-03 | Secondary action regression | Browser | Comparison action follows the same disabled rule. |
| AUTO-04 | Available baseline | Browser/API | Available item retains an enabled checkout action. |
| AUTO-05 | Propagation delay | Integration/browser | When checkout rejects the item, stale page action is not actionable. |

No execution result is included because this is an example of the plan, not a
record of a real run.
