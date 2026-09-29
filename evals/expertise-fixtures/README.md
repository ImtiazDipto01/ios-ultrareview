# Aided detection and workflow fixtures

Defective heads include visible focused tests that fail, so this suite measures responses to available failure evidence and workflow handling, **not independent defect discovery**. Use [the discovery track](../discovery-fixtures/README.md) for green-suite cases with hidden evaluator outcome tests. These locally authored snapshot repositories complement `../scenarios.md`. They test independent window selection, foreground recovery when background work is not delivered, durable Watch Connectivity dispatch, locked-device Keychain policy, staged API/cache compatibility, and an unchanged portable private-symbol rename. They are controlled component fixtures, not production apps or proof of general model competence.

Create a fresh suite in a writable scratch directory:

```sh
python3 build.py /absolute/path/to/new-fixture-output
```

The builder refuses a non-empty destination and creates six Git repositories with exact base/head SHAs, neutral `inputs/input-*.md`, and a separate `evaluator/` oracle and input map. It does not use network access, credentials, remote repositories or personal Git identities/configuration. Never provide the builder, manifest or evaluator files to blind reviewers. Give each reviewer only its assigned skill plus one neutral input; reset context between cases and preserve model/tool settings for comparisons.

Generate actual exact-head build and focused test evidence for the portable rename case:

```sh
python3 validate-bounded.py /absolute/path/to/fixture-output
```

This runs real host SwiftPM commands from an owned archived exact-head snapshot, writes logs and provenance to `evidence/bounded-rename`, and removes only its own temporary source/build/cache directory. It preserves the ordinary checkout. It uses the native SwiftPM build system to avoid host Finder-metadata signing problems; that switch is deprecated in newer toolchains, so adapt to the default build system when needed and retain the actual command/output. There are no synthetic CI claims. Give input11's reviewer the evidence record and its logs explicitly, or let the reviewer execute qualifying checks itself. The five paired platform cases contain focused executable domain tests, but portable host execution does not validate their Apple adapters, app scheme, device lifecycle, lock state or paired delivery.

Measure aided seeded-root-cause detection, false blockers on clean controls, score/cap and decision correctness, evidence truthfulness and review cost. A failed seeded domain test confirms fixture behavior, not reviewer competence. Clean domain cases with only host logic proof retain material app/device evidence limits when the changed obligation depends on that platform; ask for the smallest relevant platform validation rather than prescribing universal hardware checks. The bounded rename can reach 5.0 when its real exact-head build/tests pass because no Apple-specific behavior is changed.

Do not install generated `.git`, `.build`, caches, worktrees, logs or evidence with the skill. Only these authored generator resources belong in the skill directory.
