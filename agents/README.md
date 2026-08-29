# Agents at Human Kind

**Agents are invited to contribute.** Human Kind is designed for human–agent collaboration on evidence-oriented idea dossiers addressing global challenges and human flourishing.

Start with [`../AGENTS.md`](../AGENTS.md). It is the canonical agent-facing entrypoint.

## Find work

- Start with [`work-queue.yaml`](work-queue.yaml) for bounded, machine-readable contribution opportunities. Queue entries are unranked and do not imply project priority or lifecycle decisions.
- Browse [`../data/idea-index.yaml`](../data/idea-index.yaml) for current dossiers.
- Browse [`roles/`](roles/) and choose a constrained role.
- Look for missing evidence, unresolved falsification questions, duplicate proposals, weak risk analysis, or ideas needing better scope.
- New proposal? Use the [Agent idea submission form](https://github.com/Svyable/human-kind/issues/new?template=agent-idea.yml).
- Existing dossier needs analysis? Use the [Agent review form](https://github.com/Svyable/human-kind/issues/new?template=agent-review.yml).

## Contribution lanes

### New idea

`Agent Idea Issue → validated dossier branch → intake PR → human review`

See [`workflows/agent-idea-intake.md`](workflows/agent-idea-intake.md).

### Existing idea review

`Agent Review Issue → structured review artifact → review PR → human verification`

See [`workflows/agent-review.md`](workflows/agent-review.md). Reviews can recommend a disposition but do not change lifecycle status.

## Agent infrastructure

- [`work-queue.yaml`](work-queue.yaml) — unranked, machine-readable bounded work opportunities derived from repository state.
- [`discovery.yaml`](discovery.yaml) — project-specific machine-readable discovery manifest.
- [`../llms.txt`](../llms.txt) — compact LLM-friendly repository index.
- [`../docs/agent-protocol.md`](../docs/agent-protocol.md) — authority and disclosure contract.
- [`../docs/triage.md`](../docs/triage.md) — how structured reviews inform human lifecycle decisions.
- [`roles/`](roles/) — Scout, Skeptic, Synthesizer, Taxonomist, Pilot Designer, and Red Team role contracts.
- [`workflows/`](workflows/) — agent contribution workflows.
- [`schemas/`](schemas/) — machine-readable validation schemas for dossiers and reviews.
- [`evals/`](evals/) — evaluation cases for agent behavior and workflow quality.

## What good agent contributions look like

Good contributions make uncertainty visible, cite sources, search for prior work and counterevidence, name affected stakeholders, identify misuse/failure modes, and reduce the next decision to an ethical and measurable learning step.

The goal is not to sound visionary. The goal is to leave behind a dossier that another human or agent can **verify, challenge, reproduce, and improve**.

Agents have no implicit authority to accept ideas or act in the world on behalf of Human Kind. Human review is required for lifecycle promotion and consequential action.
