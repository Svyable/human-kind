# Agent evaluations

Evaluate agents on **verifiability and decision support**, not fluency.

The first executable harness protects the repository's two agent contribution contracts:

- Agent Idea Issue → intake dossier materializer
- Agent Review Issue → structured review materializer

Run it locally with:

```bash
python -m pip install --disable-pip-version-check pyyaml jsonschema
python scripts/test_agent_harness.py
```

CI runs the same suite on every pull request and push to `main`.

## Current strategy

The suite uses two canonical known-good Issue bodies in [`fixtures/`](fixtures/) and mutates them to exercise positive and adversarial cases. This keeps the corpus reviewable while still covering missing fields, invalid enums, provenance/attestation failures, duplicate IDs, unknown review targets, literal treatment of untrusted text, retry behavior, role mapping, and status non-mutation.

See [`intake-failure-taxonomy.md`](intake-failure-taxonomy.md) for failure classes and measurement limits.

## Adding a regression case

When a real workflow defect appears:

1. Reduce it to the smallest non-sensitive input that reproduces the problem.
2. Add a test that fails on the buggy implementation.
3. Fix the parser, schema, or workflow.
4. Keep the regression test permanently unless the contract itself is intentionally changed.

Do not copy secrets, personal data, private incidents, or harmful operational details into fixtures.

## Beyond contract tests

Future evaluation should separately measure citation validity, claim/source alignment, uncertainty calibration, counterevidence retrieval, taxonomy accuracy, duplicate detection, sensitive-domain escalation, refusal to claim decision authority, preservation of negative evidence, and generalization to holdout cases.

A passing regression corpus is evidence that known repository invariants still hold. It is **not** a score for intelligence, truthfulness, safety, or human benefit.
