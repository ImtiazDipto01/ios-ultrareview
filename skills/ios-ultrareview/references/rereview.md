# Re-review protocol

A re-review verifies resolution and moves the PR toward a stable decision. It does not restart a
greenfield review of unchanged code.

## Recover continuity

Collect the previous review and target tuple, score/decision, acceptance basis, P0–P2 findings,
stable `B` and `E` items, validation gaps, substantive author replies, unresolved threads, and
current target. Compare the code and evidence delta between the two targets.

If prior artifacts are unavailable, disclose the continuity limit and reconstruct only from
accessible evidence. If target, authority, and evidence are unchanged, perform a continuity check
and stop after reporting no state change. An explicitly requested independent review may reason
afresh, while still deduplicating prior threads.

## Resolve earlier topics

For each prior finding or path item, use one public resolution:

- **Fixed:** the behavior is corrected and its required evidence passes.
- **Still open:** the original failing path remains, the repair is partial, or required evidence is
  externally blocked. Preserve the original supported severity and explain exactly what remains.
- **No longer applies:** verified implementation context or an authorized scope decision removes the
  governing condition.
- **Withdrawn:** evidence shows the reviewer's factual, causal, severity, or authority premise was
  wrong.

Map these to path statuses: `Fixed` → `Done`, `Still open` → `Open`, `No longer applies` → `N/A`,
and `Withdrawn` → `Withdrawn`. Never renumber or reuse a `B` or `E` ID.

When inspection shows code is repaired but verification is missing, the remaining issue is evidence,
not an unresolved code defect. Keep the relevant path item open with the exact evidence needed and
apply the evidence cap.

## Adjudicate author replies

Treat a reply as evidence to verify rather than automatic authority:

- withdraw or reclassify when it disproves the trigger, causal path, consequence, requirement, or
  severity;
- mark no longer applicable when an authorized owner changes scope;
- mark fixed only after tracing current behavior and relevant evidence;
- convert genuine intent uncertainty into a question or validation limit with the needed authority
  named; or
- retain a demonstrated defect with its controlling evidence.

Reference the existing thread instead of re-arguing or reposting the same issue. Author agreement is
not required to correct a mistaken review, and assertion alone does not refute a demonstrated path.

## Inspect the repair delta

Focus on code changed to address prior items, affected callers/state/persistence/lifecycle/tests,
changed requirements or base context, and regressions introduced or exposed by the repair. Confirm
the complete current target remains merge-ready, but preserve prior classifications for unchanged
topics.

A topic may change classification only when there is a specific material basis: changed code or
integration context alters its trigger/consequence/invariant; new authoritative scope applies; new
test/runtime/static causal evidence appears; or a named earlier factual/rubric error is corrected. A
new SHA, fresh preference, or stronger wording alone is insufficient.

## Admit a genuinely new P0–P2

A new blocking finding is allowed only when every condition holds:

1. it has a distinct root cause rather than reframing a ledgered topic;
2. it names a concrete trigger or required precondition in the current target;
3. it traces the current path or missing branch to an observable user, data, security, or
   engineering consequence;
4. it identifies the governing requirement or invariant when non-obvious;
5. the consequence independently meets P0–P2; and
6. it states the novelty basis: introduced/exposed by the repair, supported by new
   authority/evidence, or genuinely missed earlier.

A concrete static causal trace can demonstrate a consequence; runtime reproduction is not mandatory.
A possibility without the trigger-to-consequence chain is a question, evidence gap, or non-blocking
note.

If the defect existed on the prior reviewed target, label it a newly recognized reviewer oversight.
Assign the next unused `B` ID and do not imply the developer introduced it. This safety exception
remains available at any round, but cannot be used for stricter interpretations, style, optional
cleanup, or a previously dismissed topic without new material basis.

## Preserve locked paths and stop on state

- Maintain `B` items under [scoring-and-severity.md](scoring-and-severity.md). New safety findings
  may append an ID only through the admission rule above.
- Maintain `E` items under [five-point-evidence.md](five-point-evidence.md). Unchanged scope cannot
  add or tighten the 5.0 path.
- Avoid duplicate inline threads; link a moved prior thread when a new anchor is essential.
- If validation is the only new input, verify SHA, provenance, command/job,
  configuration/destination, tests, and result. Update evidence, score, and decision without another
  code sweep.
- When exact-target evidence is the sole remaining baseline gate, use the validation-limited header,
  request no source change, and name the qualifying event.
- Review count is never a reason to approve, suppress a verified defect, or invent a new one.
  Material state change is the tripwire.

Recalculate the score from the complete current target rather than adding points per fix. A score
can remain flat after real progress when another independent item still sets the ceiling; explain
that plainly.

## Re-review output

Under `Previous findings`, group items as:

- `Fixed`
- `Still open`
- `No longer applies` when present
- `Withdrawn` when present
- `New` for findings that passed the admission rule; otherwise `None`

Then use the standard output. Report stable path IDs and only the exact open work. At 4.5, open `E`
items stay optional and the recommendation is `APPROVE`. At 5.0, state that the 4.5 baseline and all
applicable evidence items are complete.
