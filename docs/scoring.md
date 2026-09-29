# Scoring and readiness

The score measures merge confidence in an acquired, completely reviewed target. It is not a competence grade, code-style score, or arithmetic defect count.

| Severity | Consequence |
| --- | --- |
| P0 | Catastrophic failure requiring immediate correction. |
| P1 | Serious failure of a supported central behavior. |
| P2 | Material but more bounded correctness or product failure. |
| P3 | Nonblocking improvement. |

Apply the exact definitions and all score anchors in the [canonical scoring reference](../skills/ios-ultrareview/references/scoring-and-severity.md). The table here is an orientation, not a substitute rubric.

## Required path: B items

Below 4.5, each independent defect, scope blocker, or necessary evidence gate has a stable `B` item with an observable pass condition. Fixing a defect does not automatically satisfy an independent whole-target validation gate.

When evidence is the only remaining gate, the score is exactly **4.0** and the report requests no source change. When no P0–P2 remains, material acceptance criteria hold, and relevant exact-target baseline checks pass, **4.5** is merge-ready.

## Optional path: E items

At 4.5, the [5.0 evidence reference](../skills/ios-ultrareview/references/five-point-evidence.md) selects proportional gates for the actual change. An optional `E` item has a finite pass condition and remains stable for unchanged scope. Optional cleanup never becomes a required repair.

**5.0 is attainable.** Award it immediately when all applicable evidence is complete. A clean, well-validated small change can receive 5.0 without a long platform checklist.

## Examples

| Situation | Result |
| --- | --- |
| A bounded confirmed P1 breaks profile persistence. | At most 3.0; repair its behavior and establish regression evidence. |
| No code defect remains, but no qualifying app-target build/test evidence is available. | Exactly 4.0, validation-limited; request evidence. |
| Baseline holds; a relevant, optional excellence condition remains. | 4.5 and approval recommendation. |
| Baseline and all applicable proportional gates hold. | 5.0 and approval recommendation. |
| Only part of a large PR was available. | No whole-PR score or decision. |

These are synthetic illustrations. Use the canonical references for actual consequence assessment and caps.
