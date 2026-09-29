# Attainable 5.0 confidence

`5.0/5` means the defined PR scope has unusually complete, direct evidence. It does not claim that
bugs are impossible. First require the `4.5` baseline: no P0–P2 findings, material acceptance
criteria met, and relevant build/tests passing for the exact target.

Classify each triggered gate below as `Covered`, `Gap`, or `N/A`, with one concrete reason. Award
`5.0` whenever every applicable gate is covered and any locked `E` path is complete. If this is
already true on the first review, award `5.0` immediately.

## Proportional gates

1. **Product proof.** Every material acceptance row marked met has row-specific evidence on the
   reviewed target. Behavior requires an executed focused test, qualifying CI check, or observed
   runtime/simulator/device result that exercises it. A static criterion may use a compiler, build,
   schema, configuration, or artifact check. Inspection alone does not prove behavior.
2. **Regression protection.** Every material changed behavior or repaired defect that the
   repository's existing test harness can reasonably exercise has a focused automated test of the
   authoritative outcome passing on the exact reviewed target. Existing tests count. A generic green
   suite, coverage percentage, or manual check does not replace focused protection. Mark `N/A` when
   no candidate is test-eligible; a new UI/snapshot/accessibility framework is not required merely
   to create eligibility.
3. **Failure and recovery.** When the changed feature has a credible fallible path, cover the
   relevant denial, error, cancellation, retry, offline, invalid-data, or recovery behavior. Cover
   the actual changed risks, not every theoretical combination.
4. **Lifecycle and concurrency.** When async work, mutable shared state, navigation/lifecycle
   ownership, or ordering changes, cover relevant interruption, cancellation, repeated action, stale
   result, background/foreground, restoration, or race behavior. Synchronous/stateless changes are
   `N/A`.
5. **Critical persistence and integration.** When persisted data, migrations, API contracts,
   dependency wiring, shared state, or critical consumers change, prove only the high-impact
   invariants: no credible data loss/corruption, required compatibility, correct core contract, and
   correct critical consumer behavior.
6. **Triggered platform quality.** Evaluate only subchecks activated by the diff and repository
   requirements:
   - material UI: verify the core affected flow on a representative supported configuration;
   - localization: check only supported project localizations, with RTL only when supported or
     required;
   - changed interactive UI: check relevant accessibility semantics, labels, focus, scaling, or
     contrast proportionally;
   - changed credentials, permissions, sensitive data, telemetry, or trust boundaries: verify secure
     storage/handling and project-approved consent, disclosure, minimization, and redaction;
   - a credible changed hot path: verify responsiveness, memory, or repeated-I/O risk
     proportionally.

Project-standard tests or a focused runtime check may cover UI behavior; screenshots, recordings, UI
tests, snapshots, accessibility automation, Instruments, and unsupported languages are not universal
requirements. Approved analytics/crash telemetry is acceptable when it follows project policy and
excludes secrets or prohibited sensitive values.

Specialist lenses refine which existing gates apply; they do not add gates or score caps. Evidence
must exercise the claimed mechanism: a fake can prove application recovery logic while paired
transfer or device-lock behavior may need suitable device evidence. Mark unrelated
platforms/capabilities `N/A`; never add work merely to demonstrate the full senior-engineer
competency inventory. A bounded PR with complete applicable evidence can receive 5.0 on its first
review.

## Locked path to 5.0

When the score first reaches `4.5` with one or more gaps, publish `Path to 5.0/5 — optional,
non-blocking` as the complete list for the current authorized scope. Use the smallest finite list;
there is no fixed maximum or minimum.

| ID | Gate and current gap | Minimum sufficient evidence | Objective pass condition | Status |
|---|---|---|---|---|
| `E1` | named triggered risk and what is missing | outcome-based action; equivalent evidence allowed | binary observable condition | `Open` |

Assign stable `E1`, `E2`, and so on. Use only `Open`, `Done`, `N/A`, or `Withdrawn`. Keep an
external block `Open` and name the unavailable evidence event, service, credential, hardware, or
decision.

Combine gates in one item when the same action and objective pass condition close the same
underlying gap; do not split work merely to create one item per gate.

Once published, the list is locked for unchanged scope:

- preserve IDs and written pass conditions;
- accept equivalent evidence that exercises the same risk;
- do not add, split, replace, or tighten items after fresh sampling;
- reopen the same ID only when later code touches its basis or concrete evidence disproves its pass
  condition; and
- when an authorized material scope change creates a new applicable gap, append the next unused `E`
  ID and state one sentence identifying the scope-change basis.

A new SHA, base update, reviewer preference, or stricter interpretation is not a scope-change basis.
A genuine P0–P2 belongs in the `B` baseline path, temporarily lowers the score, and freezes `E`
evaluation until 4.5 is restored; the late-finding admission rule still applies.

Award `5.0` when the 4.5 baseline holds and every published `E` item is `Done`, justified `N/A`, or
`Withdrawn`. If no `E` item is needed because all gates are covered, remaining at `4.5` is
inconsistent—award `5.0`.
