# GitHub review format

## Acquisition failure or patch-only input

When [target-acquisition.md](target-acquisition.md) classifies the target as inaccessible, do not use the scored review template. Return:

```markdown
## iOS UltraReview — not started: target inaccessible

**Review type: AI-assisted.**

### Access blocker

State which exact target facts or repository content could not be obtained and which routes were tried.

### Required next step

Name the smallest access action that would make the target reviewable.

### Outcome

No score or provider decision — the PR target was not acquired.
```

For user-requested patch-only inspection, use `## Limited patch inspection — no merge-confidence score`, state the inspected scope and missing context/evidence, and report only directly demonstrated preliminary issues. Do not emit a decision or `B`/`E` path. Never submit either output as a live provider review.

Place `**Review type: AI-assisted.**` directly below every public review or patch-inspection title. This preserves reviewer disclosure while keeping the product name in the title.

## Summary template

This file owns the public presentation. Use [scoring-and-severity.md](scoring-and-severity.md) for scoring, caps, statuses, and decisions, and [five-point-evidence.md](five-point-evidence.md) for the `E` path. Do not restate those rules in every review.

Choose the compact presentation below for a tiny bounded change; use the standard template for broader reviews. Aim for about **200–300 words for a clean tiny review**, or **600 words for a standard summary**, plus necessary inline findings and threshold rows. These are advisory editing targets: do not omit findings, provenance, material limitations, or locked items to meet a word budget. Re-review can be shorter when unchanged facts are linked and current disposition is explicit.

```markdown
## iOS UltraReview — confidence X.X/5

**Review type: AI-assisted.**

Target: repository/PR or snapshot; base `<SHA>`, merge base `<SHA>`, head `<SHA>`, current merge result `<SHA>` when applicable.

### Summary

What the PR changes, the overall result, and the reason for the score.

### Previous findings

Re-review only: Fixed / Still open / No longer applies / Withdrawn / New.

### What's good

- Specific verified strengths.

### Blocking themes

- Independent P0–P2 root causes and consequences without duplicating inline text.

Use `### No blocking findings` when appropriate.

### Validation performed

- `PASS` / `FAIL` / `NOT RUN` — command or job, scope/destination, tested SHA, and result or reason.

### Path to 4.5/5

Stable `B` items when below 4.5.

### Proposed decision — not submitted

**REQUEST CHANGES**, **COMMENT**, or **APPROVE**.
```

Replace the last heading with `### Decision` only after successful provider submission. When exact-target validation is the sole baseline gap, use `## iOS UltraReview — confidence 4.0/5 (validation-limited)` and state that no source change is requested.

Use exactly one threshold section:

- below 4.5: `Path to 4.5/5`, rendering the canonical `B` schema and statuses from [scoring-and-severity.md](scoring-and-severity.md);
- at 4.5: `Path to 5.0/5 — optional, non-blocking`, rendering only the locked `E` items from [five-point-evidence.md](five-point-evidence.md); or
- at 5.0: `5.0 evidence — complete`, briefly naming covered and justified `N/A` gates.

At 4.5, say plainly that the PR is approved and the `E` items are optional. Do not reproduce the lock rules in the review.

For snapshot mode, place this visible line directly below the AI-assistance disclosure, substituting the exact reason when useful:

```markdown
**Review mode: Snapshot — exact refs were reviewed, but live currentness could not be refreshed; not submitted.**
```

Then name the exact base, merge base, head, and merge result when applicable and append:

```markdown
### Draft inline findings

1. **[P1][B1] Short title** — `Feature/File.swift:42 (RIGHT)`
   Trigger, consequence, invariant, smallest fix direction, and focused regression evidence.
```

Do not imply draft findings were posted. Use [worked-example.md](worked-example.md) only for calibration.

## Compact presentation for a small PR

Keep the standard title, disclosure, applicable snapshot label and exact identity.
Combine summary, verified strengths, blocking consequences and material limits into
one paragraph. Combine validation rows into a short list or paragraph; preserve
command/job, tested SHA, scope/destination and result, distinguishing supplied
execution from checks you ran. Then use the canonical threshold section and decision.

```markdown
## iOS UltraReview — confidence X.X/5

**Review type: AI-assisted.**
<Snapshot disclosure when applicable>

Target: <exact identity as defined in the standard template>

Summary: <change, assessment, verified strength, blockers/limits>
Validation: <PASS/FAIL/NOT RUN and qualifying provenance>

### <Exactly one applicable threshold section>
<Canonical B/E rows, or covered/N/A reasons at 5.0>

### Proposed decision — not submitted
**APPROVE / COMMENT / REQUEST CHANGES**
```

On re-review preserve previous findings and every B/E ID and disposition. Append
draft inline findings when present. Use the standard form when blockers need it.

## Inline findings

Each actionable inline finding contains:

1. an imperative title with severity and stable ID, such as `[P1][B1]`;
2. the concrete trigger or reproduction path;
3. the observable consequence;
4. the violated requirement or invariant when non-obvious;
5. the smallest credible fix direction; and
6. focused regression evidence when the repository can reasonably provide it.

Aim for roughly **80 words per finding** when the trigger, consequence, invariant, and remedy fit. Longer causal or provenance detail is appropriate when needed to make the finding independently verifiable; never truncate a necessary explanation to fit the target.

Example:

```markdown
[P1][B1] Preserve the manual route after location cancellation

If the user leaves while location is pending, the late response still overwrites the manually selected route. Cancel or identify the request so stale success and failure cannot mutate the destination, and add a regression test that completes the response after manual navigation.
```

Anchor to the smallest relevant changed-line range on the reviewed commit. Use `RIGHT` for added/modified code and `LEFT` for deleted behavior. Keep one root cause per comment. Missing files/scope, cross-cutting gaps, positives, questions, and validation limits belong in the summary. If no accurate changed-line anchor exists, keep the finding in the summary with path and symbol.

## Non-blocking boundary

Keep these outside findings, blocking themes, score reductions, and `B`/`E` paths unless a concrete changed trigger produces a P0–P2 consequence:

- formatting, naming, imports, and personal architecture preferences;
- newest-API adoption or broad rewrites without a correctness need;
- speculative performance, coverage percentages, and unrelated legacy debt;
- unresolved product questions without authoritative answers; and
- new testing/tooling frameworks, screenshots, recordings, unsupported languages, exhaustive audits, or optional polish pursued only for a higher score.

When the user explicitly requests optional feedback, add **Non-blocking notes** with at most three useful, concrete suggestions. Each should name its benefit and remain outside finding IDs, blocking themes, score, decision, and `B`/`E` obligations. Omit this section otherwise. An unmet optional 5.0 gate belongs in the canonical `E` path rather than being duplicated as a note.

## Posting behavior

Use [github-api.md](github-api.md) for authorized batching, actor capability,
identity/anchor refresh, ambiguous writes and post-write verification. Keep the
proposed label until submission is verified. Apply the canonical decision mapping
within actual user authority; comment-only/self-review authority remains COMMENT.
Optional E work stays non-blocking. Never imply a review merged the PR.
