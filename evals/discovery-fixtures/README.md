# Independent discovery track

Generate five paired complete component snapshots in fresh scratch storage:

```sh
python3 build.py /absolute/path/to/discovery-suite
python3 validate.py /absolute/path/to/discovery-suite --input-number 1 --public
```

All reviewer-visible existing tests must actually pass on both defective and safe heads. These tests cover legitimate established paths, not empty assertions. The four portable hidden suites exercise independent product invariants: scene ownership after select/restore, recovery after omitted scheduling delivery and fetch failure, eventual phone receipt without another watch activation, and compatibility with previously persisted JSON. The Keychain case has a separately labeled static platform-contract oracle; a host assertion about the accessibility enum would merely mirror implementation, so this case does not pretend to supply a device-lock test.

Give a reviewer only one neutral `inputs/input-NN.md`, its named repository, the assigned skill and explicitly supplied evidence. Use a **fresh context per case**, identical model/settings and access for comparisons, and no evaluator/generator/manifest access. This is an access boundary in the evaluator task, not a filesystem security boundary. An agent with unrestricted filesystem access could still read hidden resources; such a run is contaminated and must be excluded.

Freeze the completed review before hidden tests are disclosed or run:

```sh
python3 ../freeze-review.py --input /suite/inputs/input-01.md \
  --review /run/review.md --skill /skill/ios-ultrareview \
  --base ACTUAL_BASE_SHA --head ACTUAL_HEAD_SHA --model ACTUAL_MODEL_ID \
  --settings-json /run/settings.json --tools-json /run/tools.json \
  --command-log /run/commands.log --fresh-context --no-hidden-access --output /suite/evaluator/frozen/input-01
python3 validate.py /absolute/path/to/discovery-suite --input-number 1 --hidden \
  --freeze /suite/evaluator/frozen/input-01/record.json
```

Settings/tool JSON must describe actual settings, evidence access and tool versions. Optional elapsed/token fields stay unknown when not captured; never estimate them as measured. The freezer saves immutable-by-hash copies and the skill tree hash; the evaluator verifies input, target and frozen artifact hashes before execution. It adds hidden tests to a disposable archived copy, leaving the reviewed Git object unchanged. Freeze all relevant reviews before exposure. A later repair/review is a separate outcome, never retroactive independent discovery.

Grade the frozen finding against `evaluator/oracle.json`: independent seeded-root-cause discovery, false clean blockers, severity/causality and diff anchors. Grade score/cap, baseline versus optional evidence gaps, truthfulness and cleanup separately. A green visible suite is not proof of absence; a red hidden test does not establish the reviewer found its cause. Record both outcomes. Hidden Watch Connectivity tests model a queue and consumer receipt; they do not validate real system delivery, activation, suspension or batteries. Keychain runtime claims still require suitable device evidence.

No runner calls a model or grades prose automatically. Evaluator judgment must consider equivalent correct findings/tests and actual scoped evidence. Generated repositories, results and hidden resources stay outside the installed skill. Compare before/after only after the same cases have actually run with the original and revised skill; a generated suite alone establishes no recall, cost or cross-model improvement.
