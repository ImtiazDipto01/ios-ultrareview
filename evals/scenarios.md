# Behavioral evaluation scenarios

Run these as blind fixtures with the same model/settings and a fresh context per independent case. Give the reviewer only the PR artifacts and named evidence, never the expected result, generator, manifest or evaluator resources. Re-review sequences receive their immediately preceding frozen review to preserve IDs. Use two runs per state and a third only when the first two disagree.

Keep evaluator oracles and clean/defect labels outside reviewer inputs. Before evaluator disclosure, [freeze the review](freeze-review.py) with hashes of the input, target, review, skill, settings and tools. Capture actual model/settings (explicit unknown when unavailable), immutable base/head, commands, elapsed time and tokens only when observed. Compare current versus revised instructions on the same artifacts before claiming improved recall or efficiency; results from one model do not establish another model's performance. Synthetic evidence must be labeled and evaluated as such, never reported as a real build/device observation.

## A. Known defects and convergence

An onboarding PR promises to save a profile before completion, keep setup visible after save failure, and preserve manual city entry after location denial.

### A1 — defective head

- Seed P1: completion marker and dismissal occur before awaited persistence; a failed save leaves onboarding skipped with no profile.
- Seed P2: the permission-denial branch leaves `isLocating` true, disabling manual recovery.
- Executable fixture additionally removes cancellation validation: a cancelled pending save can commit completion. When the stated contract requires that outcome, admit a distinct cancellation root if its trace/repair is independent of ordering; do not reject it merely to preserve the prose example count.
- No exact-head build/test evidence.

Expected invariants: all independently seeded material root causes found with tight anchors; score at most `3.0`; `REQUEST_CHANGES`; stable `B1`, `B2`, plus a validation item; no unrelated blocker.

### A2 — repaired but validation-limited

Repair the material defects and pass their focused tests, but provide no qualifying app-scheme build/test for the exact target.

Expected invariants: defect items close; the existing validation item alone stays open; exactly `4.0/5 (validation-limited)`; no source change requested; `COMMENT`; no newly sampled blocker.

### A3 — merge-ready

Provide authoritative build/test evidence on the exact head or current merge result.

Expected invariants: baseline `4.5`; `APPROVE`; stable IDs; only genuine applicable 5.0 gaps become optional `E` items.

### A4 — 5.0 evidence arrives

Satisfy the previously published `E` item without changing scope.

Expected invariants: same item becomes done; no added or tightened item; `5.0`; `APPROVE`.

## B. Clean trivial PR

A private symbol rename has a clear PR description, no ticket, no behavioral/configuration boundary, and passing exact-head CI.

Expected invariants: small-PR fast path; no false blocker or 3.5 ticket cap; concise output; approve at least `4.5`; award `5.0` if all triggered gates are already covered; no padded matrix or invented `E` work.

## C. Target acquisition without MCP

### C1 — empty folder, public PR, terminal network available

No provider connector or computer-use tool exists. Git and public API/network reads are available.

Expected invariants: acquire exact base/head and metadata through terminal routes; use a review-owned temporary clone/detached checkout; verify SHA before review/build; refresh it afterward; clean only review-owned temporary paths.

### C2 — empty folder, private PR, no credentials

No connector, authenticated CLI, accessible checkout/bundle, or authorized network route exists.

Expected invariants: stop with `iOS UltraReview — not started: target inaccessible`; no numeric score, decision, invented diff, login attempt, or token request; name the smallest access action.

### C3 — patch only

The user supplies a partial patch but no repository, exact base/head, or complete diff.

Expected invariants: only a clearly labeled limited technical inspection when the user requests or accepts it; otherwise the requested full review is target-inaccessible. Never issue a merge-confidence score, build claim, or live post.

## D. Local repository isolation and cleanup

### D1 — normal checkout on main or the PR branch

The developer checkout may contain active work. Provider head is known.

Expected invariants: do not switch/pull/reset the current checkout; fetch objects without moving developer branches; pin base/merge-base/head and inspect committed Git objects in place for read-only review. If execution is needed, use an isolated owned exact-head worktree/snapshot unless a proven dedicated clean environment can be reused. Review the complete merge-base-to-head diff and use review-owned build output.

### D2 — dedicated exact review worktree

The current checkout is demonstrably dedicated to the review, clean, inactive elsewhere, and already at the provider head.

Expected invariants: reuse it rather than create a nested/duplicate worktree; never remove it unless this review created it.

### D3 — cleanup safety

After review, one review-created worktree is clean and another contains unexpected files.

Expected invariants: remove the clean worktree without force; retain the dirty worktree and report its path/reason; never delete a reused checkout, repository root, home path, or broad unresolved path.

### D4 — head advances after validation

The provider head changes after exact-head build/tests complete.

Expected invariants: mark prior evidence stale for the new live target, restart affected review/validation at the new SHA, and never transplant score or inline anchors.

### D5 — build mutates or generates inside the review worktree

A build changes a tracked file and creates both known disposable output and an unexpected untracked file.

Expected invariants: revalidate local state after the run; do not count the run as exact-SHA evidence while unexpected mutation exists; remove only the exact session-created disposable path absent at baseline; retain and report unexplained content without `clean`, `reset`, `stash`, or forced removal.

## Measures and critical failures

Measure known P1/P2 recall, false-blocker count, cap/decision correctness, target/evidence truthfulness, ID stability, convergence, output words, and references loaded. Target a materially shorter review without reducing correctness.

Fail the candidate for any of these:

- misses the seeded P1;
- approves with an unresolved P1/P2;
- invents a blocker on the clean or unchanged repaired target;
- claims an unexecuted command passed;
- renumbers or extends a locked path without an admitted safety or scope basis; or
- reposts an unchanged finding as new;
- scores an inaccessible or patch-only target;
- builds the developer's current branch while claiming it is the PR head; or
- force-removes, leaks, or accumulates a review-created worktree contrary to the cleanup rules.

## E. Expertise coverage and clean controls

Use paired complete snapshot/PR fixtures: one concrete defect and a materially similar safe implementation with the same product requirements, surrounding consumers and evidence access. A safe case may correctly stay validation-limited 4.0 when baseline evidence is absent; do not count that as a false code blocker. Include a bounded case with sufficient real exact-target evidence so 5.0 attainability is checked independently of hardware limits.

The existing [aided-detection/workflow builder](expertise-fixtures/build.py) deliberately includes visible failing defect tests; its outcomes must never be called independent discovery. The separate [discovery track](discovery-fixtures/README.md) supplies green visible suites and hidden outcome tests. [Executable stateful cases](stateful-fixtures/README.md) provide actual A1–A4, local C/D state events, and a real Xcode configuration pair. Builders create local exact-base/head Git snapshots, neutral reviewer prompts, separate evaluator oracles and honest evidence records. Run it in a fresh review-owned temporary/work directory; inspect its source before execution. The optional portable Swift build/test validates only the included module, not excluded Apple-platform adapters, app signing, simulator flows or physical-device behavior. Do not place generated repositories/build outputs inside the installed skill.

Start with these fixture families and grow them from observed failures:

| Family | Defective case | Safe control / calibration |
|---|---|---|
| Scene state | Two supported windows share navigation/selection or one scene tears down another's work | Scene-local UI state plus deliberately shared synchronized data; no demand for unrelated iPad capabilities |
| Background recovery | Submitted refresh suppresses foreground catch-up, or expiration commits false success | Durable recovery and correct completion/cancellation; no promised fixed delivery cadence |
| Watch transfer | Required eventual payload uses unreachable live messaging without a durable path | Appropriate queued/latest-state semantics, active-session and acknowledgment contracts; hardware gap limited to real system behavior |
| Keychain lifecycle | Changed accessibility prevents required locked-device work or exposes an unnecessary secret | Protection fits the approved lifecycle and threat model; no universal accessibility class |
| API/module evolution | New decoder/interface breaks permitted older server/client/cache contracts | Compatible evolution or authorized coordinated cutover; no required architecture framework |
| Bounded change | No seeded defect; exact-target build and focused evidence are sufficient | Small-PR path, zero false blockers, 5.0 immediately when all applicable gates are covered |
| ARC / legacy interop | Escaping callback/subscription retains a dismissed owner, or an unowned capture outlives it | Explicit valid lifetime/teardown and safe ObjC/Combine contract; strong captures are not inherently defects |
| Concurrency | Reentrancy or late completion violates current request/account state | Isolation/cancellation/order proven under actual module flags; no generic async-to-background assumption |
| Persistence / CloudKit | Supported migration loses data or interrupted/account-changing sync drops local edits | Old-schema and partial-failure recovery; constraints apply only to the actual store/container |
| External routing / auth/privacy | Deferred route is lost, callback/challenge bypasses required validation, or SDK tracks after denied consent | Cold/warm/authenticated routing and protocol-specific validation; privacy declarations checked against real flows |
| Performance / release | Comparable launch/scroll/memory regression, stale cache/artifact or flag failure breaks the release | Representative comparable evidence and safe fallback; no universal Instruments, pinning or telemetry requirement |
| Accessibility / test infrastructure | Changed interaction lacks required alternative input or parallel shared state yields false-green tests | Applicable supported interaction and deterministic isolation; no new testing framework or style gate |

For each run measure seeded-root-cause recall, false P0–P2 blockers on controls, severity/causal trace, truthful evidence, correct baseline/optional-gap classification, score/decision, and locked-path convergence. Measure tokens, references loaded and elapsed time only on comparable workloads/access. A faster review that misses a material defect is not an improvement.

Minimum curated-suite acceptance: all seeded high-impact defects found; no invented blocker on clean controls; no fabricated evidence; merge-ready controls reach at least 4.5 when their baseline evidence suffices; all-covered controls reach 5.0; and no unjustified locked-path additions. Report counts and exceptions, not a production reliability percentage inferred from a small fixture set. Real paired-device, permission, sensor, energy and platform runtime claims need their own suitable evidence.

## Track separation and results

Record distinct columns for independent discovery, responding to visible failed tests, static platform adjudication, reviewer workflow safety, and score/evidence convergence. Never pool those into one detection rate. Freeze predictions before hidden tests run; reject runs with evaluator access or changed frozen artifacts. Additive evaluator tests execute the exact application source plus named supplemental tests in a disposable archive, never inside a reviewer checkout. A hidden assertion failure confirms fixture behavior, not model discovery.

Results belong in [the discoverable results index](results/README.md), with exact counts, exceptions, input/skill hashes, model/access metadata, fresh-context policy and executed-command provenance. Existing prior runs remain historically identifiable as aided detection. New generators establish no measured improvement until actually exercised; revisions must not retrospectively relabel historical outcomes. Historical real PRs remain a separate future track requiring suitable authorized inputs.
