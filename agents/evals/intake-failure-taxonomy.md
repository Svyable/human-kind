# Agent Intake Failure Taxonomy

This taxonomy defines what the first Human Kind agent harness is trying to detect. It is intentionally narrower than “agent quality.” A green benchmark means the contribution contracts still enforce known invariants; it does **not** prove that an agent is truthful, wise, safe, or useful in open-ended research.

## Failure classes

| ID | Class | Example invariant |
| --- | --- | --- |
| F1 | Contract completeness | Required headings cannot disappear silently. |
| F2 | Controlled vocabulary | Domains, roles, status recommendations, intervention types, time horizons, and reversibility must use known values. |
| F3 | Provenance and authority | Required attestations and `decision_authority: none` must survive materialization. |
| F4 | Identity and target integrity | Idea IDs must not collide; reviews must bind to an existing unique dossier. |
| F5 | Untrusted text boundary | Issue text is data, never shell or Python code to execute. |
| F6 | Retry and idempotency | Re-running a review updates the same artifact; workflow retries reuse an existing PR when present. |
| F7 | Output integrity | Dossier metadata/index entries and paired review YAML/Markdown artifacts are produced consistently. |
| F8 | Evidence and uncertainty fields | Reviews cannot omit findings, sources, counterevidence/uncertainty, or risk analysis. |
| F9 | Sensitive-data minimization | Fixtures must not contain credentials, private data, or unnecessarily operational harmful detail. |
| F10 | Benchmark generalization | Passing visible fixtures must not be treated as evidence that novel failures are covered. Holdouts and seeded mutations should be added as the harness matures. |

## Benchmark outcomes

Track at least three outcomes when the suite grows beyond contract regression testing:

1. **Meaningful-defect detection rate** — fraction of intentionally seeded, decision-relevant defects that fail the harness.
2. **Known-good false-positive rate** — fraction of reviewed good fixtures incorrectly rejected.
3. **Seeded-regression detection** — whether a deliberate weakening of a parser or schema is caught before merge.

The initial suite includes a seeded-regression guard for arbitrary agent roles: programmatic submissions must not bypass the Issue Form vocabulary by declaring an invented authority-bearing role.

## Fixture policy

Prefer a small number of canonical positive fixtures plus deterministic mutations over dozens of copied Issue bodies. Every new production failure should be reduced to the smallest non-sensitive fixture that reproduces it.

Do not turn real private incidents, credentials, personal data, or harmful operational details into fixtures. Preserve only the minimum structure necessary to test the failure class.

## What this benchmark cannot establish

This suite does not measure source truth, claim/source alignment, domain expertise, stakeholder legitimacy, novel-risk discovery, or real-world impact. Those require separate research and human review. Benchmark pass rate must never become a substitute for substantive dossier evaluation.
