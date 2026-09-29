# Contributing

Start with a concrete review failure or a reproducible platform case. Explain the expected behavior, observed finding/score, agent/model when known, exact target, and available evidence. Remove credentials, proprietary code, and personal data from examples.

Keep shared rules in `SKILL.md` and domain detail in the relevant reference. Preserve half-point scoring, validation-only 4.0, complete-target prerequisites, stable B/E paths, attainable 5.0, and external-write authority. Avoid expanding a single failure into a universal checklist.

## Local checks

```sh
python3 scripts/check.py
python3 -m unittest discover -s tests -v
python3 scripts/install-smoke.py
```

The first two checks use Python 3.10+ and its standard library. The installer smoke test also needs Git, Node.js 22.20.0+, npm, and network access. It uses an isolated temporary project, pins `skills@1.7.0`, disables installer telemetry, and verifies installed contents for Codex, Claude Code, and Cursor. It does not change your global skills.

Maintainer fixtures require Swift for component execution; Xcode/macOS and an installed simulator are needed for app checks. Read [the evaluation guide](docs/evaluation.md) before evaluating. Do not expose hidden oracles to a reviewer before freezing its predictions. New fixtures should include a defective case, a clean control, neutral input, and a consequential product invariant.

A scenario definition is not an executed measurement. Document failed infrastructure, excluded/contaminated runs, settings, evidence access, and cost scope. Do not claim model-wide accuracy from a small fixture suite.

Contributions are provided under this repository's MIT license. Retain third-party notices and cite new adapted source material.
