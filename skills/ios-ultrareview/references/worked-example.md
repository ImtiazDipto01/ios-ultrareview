# Worked review example

Use this synthetic example only to calibrate structure, severity, stable IDs, and convergence. Repository facts in a real review control the outcome.

## Scenario and working matrix

The PR description is the complete stated intent; there is no external ticket:

- persist the profile before marking setup complete;
- on save failure, remain in setup and allow retry; and
- after location denial, keep manual city entry usable.

The exact head has no Xcode build/test evidence.

| Requirement | Evidence | Status |
|---|---|---|
| Persist before completion | Static trace shows completion and dismissal occur before the awaited save | Missing |
| Save failure remains recoverable | Static trace shows setup has already dismissed | Missing |
| Denial restores manual entry | Denial branch leaves `isLocating` true while the form is disabled | Missing |

## Complete draft review

```markdown
## iOS UltraReview — confidence 3.0/5

**Review type: AI-assisted.**
**Review mode: Snapshot — exact refs were reviewed, but live currentness could not be refreshed; not submitted.**

Target: base `main@abc123`, merge base `abc123`, head `def456`; no merge-result SHA available.

### Summary

This snapshot does not yet preserve the profile-setup contract. A failed save can leave setup marked complete without a stored profile, and location denial leaves manual entry disabled. The PR description is specific enough to establish stated intent; the lack of a separate ticket does not lower confidence by itself.

### What's good

- Profile persistence is isolated behind the repository abstraction.
- Location authorization is injected, so denial can be tested deterministically.

### Blocking themes

- Setup completion currently occurs before required persistence succeeds.
- Permission denial leaves the only manual recovery path disabled.

### Validation performed

- `PASS` — complete PR diff and affected setup flow inspected at head `def456`.
- `NOT RUN` — no trusted Xcode build or test result exists for head `def456`.

### Path to 4.5/5

| ID | Source | Required outcome | Objective pass condition | Status |
|---|---|---|---|---|
| B1 | P1 inline finding | Commit completion only after persistence | A failing save keeps the completion marker false and setup visible; focused regression evidence passes | Open |
| B2 | P2 inline finding | Restore manual entry after denial | Denial clears locating state and leaves manual entry usable; focused regression evidence passes | Open |
| B3 | validation gap | Validate the exact target | The documented app-scheme build and relevant tests pass on this head or its qualifying current merge result | Open |

### Proposed decision — not submitted

**REQUEST CHANGES**

### Draft inline findings

1. **[P1][B1] Commit completion only after the profile save succeeds** — `Features/ProfileSetup/ProfileSetupModel.swift:88 (RIGHT)`

   If persistence fails or the process ends first, this path has already stored the completion marker and dismissed setup. On relaunch, the user bypasses setup without the required profile. Await the save and commit completion/navigation only on success; retain the draft and expose retry on failure. Add a failing-repository test that keeps the marker false and setup visible.

2. **[P2][B2] Restore manual entry when location permission is denied** — `Features/ProfileSetup/ProfileSetupModel.swift:141 (RIGHT)`

   The denial branch never clears `isLocating`, while that state disables the form. A user who denies permission cannot continue manually without relaunching. End locating state on every terminal path and add a denial-path test proving manual entry remains usable.
```

## Expected convergence

1. After both repairs and focused tests, mark `B1` and `B2` `Done`. If the full exact-target build/tests are still missing, keep only `B3` `Open`, use `4.0/5 (validation-limited)`, request no source change, and recommend `COMMENT`.
2. When qualifying exact-target build/tests arrive, mark `B3` `Done`. The baseline becomes `4.5/5` and the recommendation becomes `APPROVE`.
3. If lifecycle/concurrency evidence is the only genuine 5.0 gap, publish one optional item such as `E1`: prove a cancelled pending save cannot later commit completion.
4. When that exact pass condition succeeds on the current target, mark `E1` `Done`, add no replacement items for unchanged scope, and award `5.0/5` with `APPROVE`.

The initial 3.0 illustrates a localized P1 with a narrower recovery defect in an otherwise sound feature. It is not a formula that every P1-plus-P2 receives 3.0. Wider consequences and repair burden can justify a lower score within the same caps; use the boundary examples in [scoring-and-severity.md](scoring-and-severity.md).

## Clean tiny review with qualifying CI — synthetic

**This is a presentation example, not an executed evaluation.** Assume a complete exact-target snapshot of a private, synchronous helper rename in an existing iOS app. The signature, consumers, control flow, data, and platform behavior are unchanged. Assume the reviewer verified trusted CI's underlying successful commands, immutable head SHA, configuration/destination, focused public-outcome tests, and archived result. The invented identifiers and `PASS` rows below demonstrate how to report that evidence; they do not claim a real repository, device, CI run, or local execution.

```markdown
## iOS UltraReview — confidence 5.0/5

**Review type: AI-assisted.**
**Review mode: Snapshot — exact refs were reviewed, but live currentness could not be refreshed; not submitted.**

Target: synthetic CoreApp snapshot; base and merge base `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`, head `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb`; no provider merge result supplied.

Summary: The PR renames a private normalization helper and updates its two callers without changing the signature, control flow, or observable output. All changed paths and their callers were inspected. The existing public-outcome tests cover normalization, empty input, and repeated calls. No blocking findings remain, and the applicable evidence gates are complete. The score applies to this bounded snapshot; live currentness is unavailable.

Validation: `PASS` — trusted supplied CI, not local execution, at head `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb`: CoreApp Debug build and CoreTests/NormalizationTests via xcodebuild; iPhone 15 simulator, iOS 17.5; underlying commands exited 0 and all three focused tests passed. Assumed CI record and archived result identify the same SHA, scheme, configuration, destination, and tests. Inspection separately confirmed no exported API, persistence, dependency wiring, or executable infrastructure changed.

### 5.0 evidence — complete

Product proof and regression protection are covered by the exact-target build and focused outcome tests. Failure/recovery, lifecycle/concurrency, critical persistence/integration, and platform-quality changes are N/A: this private synchronous rename alters none of those behaviors. No optional E items are needed.

### Proposed decision — not submitted

**APPROVE**
```

If that qualifying CI evidence were absent and no source defect remained, the same snapshot would be **4.0 validation-limited**, with the exact build/test event as an open `B` item and a **COMMENT** recommendation. If 4.5 held but a triggered proportional gate lacked evidence, publish its finite optional `E` item. Do not keep a fully evidenced bounded change at 4.5 merely because it is small or uses CI rather than a local Mac.

## Score boundary examples — synthetic

These examples assume complete target acquisition; they illustrate selection within the unchanged caps, not automatic scores for matching keywords.

| Pattern | Illustrative score and reason |
|---|---|
| A newly added secondary export format fails on one malformed record; the error is recoverable and primary export is intact. | **4.0:** a localized P2 with a narrow repair. |
| A broad UI change has independent bounded regressions in search recovery, settings accessibility, and secondary export; no common/core flow is defeated. | **3.5:** P2 impact reaches several independent requirements across the changed scope. The breadth, not the number, distinguishes it from 4.0. |
| A profile save can mark setup complete before persistence succeeds; other flows and architecture work and the repair is localized. | **3.0:** an isolated P1 defeats the central save contract. A small additional recoverable defect does not automatically force 2.5. |
| That core save failure also accompanies consequential independent recovery and integration gaps across the feature. | **2.5:** substantial correct structure exists, but the repair burden reaches beyond the isolated P1. |
| Independent central sync and migration failures need substantial redesign; other feature boundaries remain usable. | **2.0:** reconstruction is required in central flows with useful structure left intact. |
| Shared lifecycle/storage ownership makes most central flows unsafe or nonfunctional without any confirmed P0. | **1.5:** the foundation is broadly unsound, rather than a contained repair in otherwise usable boundaries. |

An uncertainty about an authoritative core requirement can invoke the existing criteria cap; it is not a code defect without a demonstrated violated requirement. The complete worked example and clean-case presentation live in [worked-example.md](worked-example.md).

