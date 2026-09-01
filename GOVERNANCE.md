# Governance

## Purpose

Governance exists to keep Human Kind open to contribution while preserving epistemic quality, safety, legitimacy, reversibility, and accountable decision-making.

## Decision rights

Agents have **repository-scoped decision authority**. Within the public repository and its documented automated workflows, agents may make reversible process decisions such as:

- choose and sequence bounded work from the agent work queue;
- maintain queue and coordination state;
- classify, narrow, challenge, or recommend disposition of ideas and reviews;
- open, update, close, and reconcile repository Issues and Pull Requests;
- accept bounded contributions into the commons by merging PRs that satisfy the repository's schema, provenance, path-scope, and required-CI gates through an authorized merge lane.

This authority is intentionally narrower than real-world authority. Agents do **not** independently:

- declare unverified claims to be verified project knowledge;
- promote dossier lifecycle state as a substitute for accountable human judgment;
- commit funding or spend money;
- contact or represent Human Kind to external stakeholders;
- deploy pilots or interventions in the world;
- make clinical, legal, humanitarian, procurement, targeting, security, or other consequential operational decisions.

`decision_authority: repository-scoped` therefore means authority to decide and execute bounded, reversible repository workflow actions. It does not mean authority over people, money, deployments, external representation, or consequential real-world action.

Human verification remains required before agent-produced claims are treated as verified project knowledge or used for consequential decisions. Maintainers may override, revert, or narrow agent repository decisions through normal Git history and review mechanisms.

## Automated decision loop

The validated agent merge workflow is an execution mechanism for repository-scoped agent authority. Eligible same-repository agent PRs may merge without a separate human approval when the exact head SHA passes required CI and satisfies a narrowly defined branch/path contract.

Outstanding `CHANGES_REQUESTED` reviews remain a veto. The unattended loop must not be able to expand its own authority: edits to governance, agent-authority policy, validators, schemas, or workflow code require an ordinary governance/infrastructure PR outside the unattended decision lane.

## Dossier promotion

Promotion should be based on evidence and readiness rather than popularity. Reviewers should inspect each rubric dimension and provide narrative rationale. A promotion PR must identify material uncertainties, changed risks, affected stakeholders, and the smallest reversible next action.

For health, conflict, biosecurity, children, AI safety, or other high-stakes domains, maintainers should require relevant domain expertise and, where feasible, participation by people affected by the decision.

Repository-scoped agent authority does not by itself authorize lifecycle promotion or consequential use. Those remain human-accountable boundaries unless this governance contract is explicitly changed in a future governance PR.

## Governance changes

Material changes to the charter, evidence standard, evaluation rubric, lifecycle, licensing, or agent authority should be proposed by PR and discussed publicly before merge. Significant decisions should be summarized in `docs/decision-log.md`.

Authority-contract and merge-loop changes are **not** eligible for unattended agent auto-merge. This prevents agents from silently expanding their own mandate.

## Conflicts of interest

Contributors should disclose financial, organizational, advocacy, or implementation interests that could reasonably affect a review. A conflicted reviewer may provide evidence or analysis but should not be the sole approver of a consequential decision.

## Appeals and reversibility

A dossier or repository decision may be revisited when new evidence appears. `not-pursuing` and `archived` are documented states, not permanent erasure. Changes should preserve the reasoning history in Git and `updates.md`.

## Stewardship

The project should favor transparent rules, distributed review, reversible automation, and replaceable maintainership over founder authority. As the contributor base grows, this document should evolve toward explicit maintainer nomination, removal, quorum, conflict-resolution procedures, and auditable agent-authority boundaries.
