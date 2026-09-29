# Executable convergence, acquisition and Xcode cases

These authored local projects implement scenarios A, C and D from [scenarios.md](../scenarios.md). Generate them in fresh scratch storage:

```sh
python3 build.py /absolute/path/to/stateful-suite
```

No generator output is executed CI, build, test or device evidence. Repository prompts contain real local Git SHAs and neutral stated intent, without expected scores or oracle labels. Give each blind case a fresh reviewer context and the assigned skill, one neutral input, its repository and only explicitly named evidence. Keep `manifest.json`, generators and evaluator oracles out of reviewer scope. See [freezing instructions](../discovery-fixtures/README.md) for recording actual model/settings/tool metadata, review artifacts and skill hashes. Evaluation task bounds are required; these resources are not protected from unrestricted filesystem access.

## A1 → A2 → A3 → A4

The onboarding snapshots contain a real dependency-free Swift module and the same source compiled in a minimal SwiftUI iOS app with a shared Xcode scheme and hosted XCTest target. The app adapter/view stay unchanged; focused tests assert completion/dismissal state, retained draft/retry and manual entry after denial. A1 introduces persistence-ordering, permission-denial and cancelled-save completion violations while established happy-path coverage remains green. A2 repairs all three obligations and adds focused success/failure/denial tests; interruption evidence remains a separately testable gap. The re-review receives only the immediately preceding frozen review to retain B/E IDs.

```sh
python3 validate.py /suite focused
python3 validate.py /suite app-baseline \
  --destination 'platform=iOS Simulator,id=ACTUAL_INSTALLED_SIMULATOR_UUID'
```

`focused` produces actual host build/test logs, usable for A2's focused regression checks. `app-baseline` executes `xcodebuild build-for-testing` then `test-without-building` on the exact repaired application source. It creates `inputs/A3.md` only if both commands succeed and hosted tests execute. Inspect the records/logs and compare SHA/destination to the review target; the evidence is local simulator evidence, never CI or physical-device proof. An inaccessible simulator leaves A3 unavailable rather than fabricated.

At A3, a reviewer may publish a finite optional cancellation item. Freeze that review before supplemental evaluator access, then execute the exact requested condition:

```sh
python3 validate.py /suite optional --freeze /run/frozen-A3/record.json --optional-item E1 \
  --pass-condition "EXACT CANCELLATION CONDITION FROM FROZEN REVIEW" \
  --adjudicated-cancellation-item
```

The validator checks frozen hashes/target and successful A3 provenance, runs additive deterministic interruption tests in an archived temporary copy, and creates `inputs/A4.md` only after success. The test pauses persistence, cancels the parent task, releases persistence and asserts completion/dismissal cannot commit afterward. No reviewed source changes between A2/A3/A4. An equivalent reviewer-executed cancellation check at A3 can correctly yield immediate 5.0; do not artificially withhold a score to force the sequence. The caller must adjudicate that the selected stable item and quoted frozen pass condition describe this cancellation outcome; the validator records that attestation, checks exact text/whole-token ID and rejects mismatches. It does not automatically grade semantic equivalence. A missing/changed E item is not silently invented. Review convergence separately from test correctness; automated scripts do not grade review prose.

## Real Xcode release-configuration pair

`inputs/X1.md` and `X2.md` review materially similar xcconfig consolidations in a real app/test project. Existing app tests stay unchanged. The product requires retaining iOS 17 and iPad support; a current iPhone simulator green suite cannot independently prove those static release constraints.

```sh
python3 validate.py /suite xcode-clean --destination 'platform=iOS Simulator,id=UUID'
python3 validate.py /suite xcode-defect --destination 'platform=iOS Simulator,id=UUID'
```

Successful runs append reviewer-visible real build/test provenance, with no expected labels, to the relevant neutral inputs. After reviews are frozen, adjudicate the effective configuration using actual Xcode settings:

```sh
python3 validate.py /suite xcode-adjudicate --input X1 --freeze /run/frozen-X1/record.json
python3 validate.py /suite xcode-adjudicate --input X2 --freeze /run/frozen-X2/record.json
```

This hidden audit checks effective app deployment/family settings rather than grepping a project line. It is a static product-contract check, not execution on iOS 17 or iPad. Fixture failures from malformed projects or unavailable tools are infrastructure failures, not successful seeded outcomes.

## C/D local acquisition and state events

The generator makes an accessible local bare provider with immutable objects, a metadata pointer, ordinary clean/dirty checkouts, a dedicated reused exact-head worktree, and two recorded review-created cleanup paths. Neutral prompts cover inaccessible access, explicitly authorized partial-patch inspection, ownership and stale-head behavior. The C1 local Git transport is a substitute for network acquisition; it does not exercise a hosted provider API or credentials.

```sh
python3 validate.py /suite inspect-acquisition
# Run after D4 reviewer pins/validates the first head and pauses:
python3 validate.py /suite advance-head
```

`advance-head` moves only this suite's known provider ref and metadata to another prebuilt commit. Supply the resumed reviewer the explicit event. Check that prior evidence and anchors are not transplanted to the new target. D3 cleanup should remove only the recorded clean owned path without force and retain the dirty/reused paths. Capture before/after Git status and ownership; never clean all suite worktrees merely for convenience.

D5 includes an inspected wrapper that changes a tracked README, generates declared disposable output and creates an undeclared file. The reviewer can correctly decline execution based on those effects. To separately test post-run state handling, the evaluator may inject that same documented local event:

```sh
python3 validate.py /suite inject-mutation
```

Injection writes only exact manifest-identified fixture paths after checking untouched head/state. It claims **no build run**. Restart/resume the reviewer with an explicit state-event message; require integrity revalidation and retention of unexplained content. The validator does not reset, clean, stash, force-remove or normalize dirty repositories. All execution build caches are isolated in owned temporary directories; records and logs remain for inspection. Dispose of only suite-owned resources after all artifact/cleanup grading is frozen.
