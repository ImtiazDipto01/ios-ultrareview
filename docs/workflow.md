# Review workflow

## Phase 1: Provide the target and intent

Supply a PR URL or repository plus exact base/head refs. Describe the user-visible outcome and compatibility requirements. Existing PR prose can establish intent; a separate ticket is not mandatory.

The agent pins immutable target identity and obtains the complete change plus necessary consumers. A tiny eligible change needs only a short intent statement. A large change needs full coverage across chunks; sampling cannot justify whole-PR approval.

## Phase 2: Inspect the affected behavior

The agent traces root causes using only relevant platform guidance. A scene change may need state ownership and restoration checks. A persistence change may need migration, failure recovery, and conflict handling. A release configuration change may need effective build settings even when existing tests are green.

The finding must explain a concrete consequence. Architecture preferences, unrelated debt, optional modernization, and technologies the product does not use do not become blockers.

## Phase 3: Establish evidence

Checks execute only after inspecting repository trust and execution requirements. Read-only inspection can use pinned Git objects. Execution may need an isolated environment and additional permissions from the host.

Supply CI or local evidence when available:

```text
Target: full immutable head SHA (or qualifying current merge-result SHA)
Command/job: xcodebuild test ... / linked CI job
Environment: Xcode version, scheme/configuration, destination
Outcome: PASS; tests actually executed
Artifacts: logs or result bundle; source/target identity verifiable
```

This is an evidence template, not a completed check. A green iPhone simulator run does not establish physical-device behavior, all supported OS versions, or native iPad compatibility. Evidence qualifies only for the mechanism it actually exercises.

## Phase 4: Read the result

Expect an intent summary, exact target, findings, validation status, score/decision, and finite required conditions. Findings with `B` IDs block readiness. Optional `E` items at 4.5 do not block approval.

A validation-only 4.0 names the missing command/job/event and says no source change is requested. A partial review identifies coverage omissions and withholds a whole-PR score.

The [canonical report guidance](../skills/ios-ultrareview/references/github-review-format.md) contains the full output contract.

## Phase 5: Re-review after repairs

Provide the previous review, repaired target, and new evidence:

```text
Use ios-ultrareview to re-review this PR at NEW_HEAD_SHA.
Previous review: [attach or link the full review].
B1 and B2 are repaired. Here are the exact-target regression and app-test logs.
Verify the published pass conditions, preserve IDs, and update confidence.
```

The agent verifies the delta and marks items `Done`, `N/A`, or `Withdrawn` when justified. New blockers require a demonstrated new material defect; the agent does not rescan unchanged code to invent new requirements. When 5.0 evidence is already complete, it awards 5.0 without manufacturing an intermediate task.

## Phase 6: Submit when authorized

Draft review is the default. If you want a GitHub submission, explicitly authorize it. The host still needs authenticated provider tools and actor capability. Comment-only authorization allows `COMMENT`; approval or request-changes authority is separate. The agent refreshes target identity before writing.
