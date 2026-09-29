# Evaluation and provenance

## What has actually been measured

The [public development summary](../evals/results/development-summary.json) derives from the private frozen 1.0.0 report. It preserves target/runtime hashes and reported outcomes while omitting private machine paths and source logs. It is a publication summary, not the original evidence archive or a independently reproducible accuracy benchmark.

| Track | Recorded outcome | Limit |
| --- | --- | --- |
| Scene ownership | Defective 3.0; clean 5.0 | Used RC1, before final density edits. |
| Backward-compatible API/cache decoding | Defective 3.0; clean 5.0 | Final 1.0.0 runtime; complete component fixture. |
| Xcode release configuration | Defective 3.0; clean 5.0 | Final runtime; current-iPhone hosted checks plus effective settings. |
| Sequential onboarding re-review | 3.0 → validation-only 4.0 → 5.0 | One reviewer session; stable required items; optional A4 was unnecessary. |
| Author execution checks | Ten green visible suites, four hidden portable pairs, app checks and guard checks | Author-known checks, not independent model discovery. |

Historical aided runs used reviewer-visible failing tests and multiple cases per reviewer context. Their provenance appears in the recovery addendum; they are not counted as fresh-context independent discovery.

## Recovered model identity and usage

Original frozen reports did not capture model/settings/tokens. The [post-hoc recovery](../evals/results/provenance-recovery.json) identifies nine reviewer sessions from retained Codex Desktop host metadata: **configured model `gpt-6-sol`, reasoning effort `ultra`**. Recovery occurred after the original measurements. Original records were not rewritten or backdated.

The public addendum contains selected metadata and digests, not private conversation logs. A host-configured identifier is not an independently server-attested backend snapshot. Other unavailable settings remain unknown. Client token counters cover whole reviewer sessions, including retries and artifact writing; multi-case sessions have no per-case attribution. Parent orchestration and fixture authoring are outside those session totals. Cached input is part of input; reasoning output is part of output. These counters are not final billing or evidence of token savings.

There is no real-PR accuracy corpus, cross-model comparison, demonstrated efficiency improvement, or physical-device reliability measurement. A skill-quality assessment from another reviewer is distinct from the PR merge-confidence scale. The public release makes no unattributed “4/5 benchmark” claim.

## Run a new evaluation

1. Freeze the skill version and tool configuration. Generate scratch fixtures from [discovery](../evals/discovery-fixtures/README.md), [stateful/Xcode](../evals/stateful-fixtures/README.md), or [expertise](../evals/expertise-fixtures/README.md) resources.
2. Give each discovery reviewer a fresh context, one neutral input, its complete repository, the assigned skill, and named evidence. Keep hidden evaluator resources out of scope.
3. Capture the actual model/settings, commands, access, and review. Freeze the prediction **before** revealing hidden checks.
4. Execute/adjudicate hidden outcomes. Grade root-cause discovery, false blockers, severity, score rules, evidence honesty, and cleanup separately.
5. Report the case set and exclusions. Compare revisions only after matched inputs/tools/settings have actually run.

The fixture runners do not call a model or automatically grade prose. Their task access boundaries do not provide filesystem isolation. A reviewer that reads hidden resources before freezing has a contaminated run and must be excluded.

## Public-benchmark freeze guard

Normal historical freezing permits explicit unknown metadata. New public benchmark records can use `--public-benchmark` to require a known model, at least one recorded setting, and a hash-bound named host/provider source. The guard checks consistency and source bytes; it cannot authenticate caller statements.

Create `settings.json`, `tools.json`, and a **sanitized recorded metadata source**. Create a provenance envelope with this shape (replace example identifiers and the digest with actual recorded values):

```json
{
  "model": "ACTUAL_MODEL_ID",
  "settings": {"reasoning_effort": "ACTUAL_RECORDED_VALUE"},
  "source": {
    "kind": "host-recorded",
    "label": "Selected host turn metadata; configured model only",
    "artifact": "host-metadata.json",
    "sha256": "ACTUAL_64_CHARACTER_SHA256"
  }
}
```

The source artifact is resolved relative to the envelope. Use `provider-recorded` only for a provider record. Settings must equal `settings.json`; unknown extra settings may remain null and must be disclosed. If you pass `--tokens`, include `usage` with a matching integer `total_tokens` and a nonempty `scope` in the envelope. Leave tokens absent when unavailable. Do not construct evidence by copying your desired values into a purported host record.

```sh
python3 evals/freeze-review.py \
  --input /scratch/input.md --review /scratch/review.md \
  --skill skills/ios-ultrareview --base ACTUAL_BASE_SHA --head ACTUAL_HEAD_SHA \
  --model ACTUAL_MODEL_ID --settings-json /scratch/settings.json \
  --tools-json /scratch/tools.json --public-benchmark \
  --provenance-json /scratch/provenance.json \
  --fresh-context --no-hidden-access --output /scratch/frozen
```

The guard rejects unknown model, missing/all-unknown settings, inconsistent metadata, missing/tampered source, unscoped token claims, and invalid counters before creating frozen output. Copies and hashes preserve input/review/settings/tools and selected provenance. Refusal to overwrite an existing output and structured target SHA checks remain intact.

Check frozen records and logs for private content before publication. This mode is a maintainer publication check; it does not add a requirement to ordinary PR scoring. A stronger public study should supply independently inspectable sanitized traces and matched cases across models.
