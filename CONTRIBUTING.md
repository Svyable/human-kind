# Contributing to Human Kind

Human Kind is an evidence-oriented idea commons. Contributions should make the corpus more testable, legible, safe, or useful—not merely more ambitious.

## Before contributing

Read `docs/charter.md`, `docs/principles.md`, `docs/evidence-standard.md`, `docs/agent-protocol.md`, and `GOVERNANCE.md`. Search existing dossiers and issues for duplicates or prior art.

## Units of work

Use **Issues** for idea intake, research questions, source requests, pilot coordination, and governance discussion. Use **Pull Requests** for versioned changes to dossiers, rubrics, taxonomy, governance, data, or agent workflows.

Substantive proposals belong in `ideas/<domain>/<slug>/`, not only in an Issue. Start by copying `ideas/_template/`.

## Dossier requirements

Every dossier must include a valid `idea.yaml` and should maintain:

- `proposal.md` — problem, prior work, novelty, mechanism, falsifiers, and smallest ethical next step
- `evidence.md` — claim-by-claim sources and uncertainty
- `risks.md` — failure modes, misuse, displacement of harm, equity, reversibility
- `updates.md` — dated changes, decisions, and evaluation history

Use primary sources and systematic evidence when available. Clearly separate observed facts, expert judgment, model outputs, assumptions, and hypotheses.

## Pull requests

A PR should explain:

1. what claims changed;
2. what sources were added or removed;
3. how the risk analysis changed;
4. whether status, maturity, evidence level, or next action changed;
5. which claims still require human verification.

Eligible bounded coordination, intake, and structured-review PRs may merge through the authorized exact-head validated agent lane without a separate human approval. That merge accepts versioned material into the commons; it does not verify claims or promote lifecycle status.

At least one accountable human review is required before promoting a dossier beyond `intake`. High-stakes domains require proportionate domain expertise and affected-community input before external action.

## Agents

Agent contributions must disclose their role and preserve the required metadata contract. New agent artifacts use `decision_authority: repository-scoped`.

Repository-scoped authority permits agents to choose bounded work, maintain coordination state, and accept eligible validated contributions through authorized merge lanes. It does not permit agents to treat unverified claims as settled facts, promote lifecycle status as a substitute for accountable human judgment, spend money, contact or represent Human Kind externally, deploy interventions, or make consequential operational decisions.

Historical artifacts with `decision_authority: none` remain valid provenance records.

## Quality bar

Prefer a smaller, falsifiable proposal over a sweeping manifesto. Prefer a documented `not-pursuing` recommendation over leaving a weak idea indefinitely open. Review the dimensions in `docs/evaluation-rubric.md` individually; do not substitute a single aggregate score for reasoning.

## Conduct and security

Follow `CODE_OF_CONDUCT.md` and `SECURITY.md`. Do not publish private personal data, confidential material, exploit details that create avoidable harm, or instructions whose primary value is enabling abuse.
