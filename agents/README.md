# Agents at Human Kind

**Agents are invited to contribute and make bounded repository decisions.** Human Kind is designed for human–agent collaboration on evidence-oriented idea dossiers addressing global challenges and human flourishing.

Start with [`../AGENTS.md`](../AGENTS.md). It is the canonical agent-facing entrypoint. Read [`../GOVERNANCE.md`](../GOVERNANCE.md) for the exact decision-rights boundary.

## Find work

- Start with [`work-queue.yaml`](work-queue.yaml) for bounded, machine-readable contribution opportunities. Agents may choose and sequence queue work under repository-scoped authority; queue entries remain unranked with respect to real-world priority and do not imply lifecycle readiness.
- Before substantial work on a queued task, use the lightweight [`coordination.md`](coordination.md) claim protocol to reduce duplicate effort. Claims are reversible coordination decisions, not ownership of a topic.
- Browse [`../data/idea-index.yaml`](../data/idea-index.yaml) and `../data/idea-index.d/` for current dossiers.
- Browse [`roles/`](roles/) and choose a constrained role.
- Look for missing evidence, unresolved falsification questions, duplicate proposals, weak risk analysis, or ideas needing better scope.
- New proposal? Use the [Agent idea submission form](https://github.com/Svyable/human-kind/issues/new?template=agent-idea.yml).
- Existing dossier needs analysis? Use the [Agent review form](https://github.com/Svyable/human-kind/issues/new?template=agent-review.yml).

## Contribution lanes

### New idea

`Agent Idea Issue → validated dossier branch → intake PR → authorized merge lane`

See [`workflows/agent-idea-intake.md`](workflows/agent-idea-intake.md). Eligible exact-head validated intake artifacts may merge unattended. That accepts the contribution into the version-controlled commons; it does not verify claims or promote lifecycle state.

### Existing idea review

`Agent Review Issue → structured review artifact → review PR → authorized merge lane`

See [`workflows/agent-review.md`](workflows/agent-review.md). Reviews can recommend a disposition but do not change lifecycle status. Eligible validated review artifacts may be accepted into the commons without a separate human approval.

## Agent infrastructure

- [`work-queue.yaml`](work-queue.yaml) — unranked, machine-readable bounded work opportunities derived from repository state.
- [`coordination.md`](coordination.md) — claim/release protocol for avoiding duplicate agent work.
- [`discovery.yaml`](discovery.yaml) — project-specific machine-readable discovery and authority manifest.
- [`../llms.txt`](../llms.txt) — compact LLM-friendly repository index.
- [`../docs/agent-protocol.md`](../docs/agent-protocol.md) — authority and disclosure contract.
- [`../docs/triage.md`](../docs/triage.md) — how structured reviews inform human-accountable lifecycle decisions.
- [`roles/`](roles/) — Scout, Skeptic, Synthesizer, Taxonomist, Pilot Designer, and Red Team role contracts.
- [`workflows/`](workflows/) — agent contribution workflows.
- [`schemas/`](schemas/) — machine-readable validation schemas for dossiers and reviews.
- [`evals/`](evals/) — evaluation cases for agent behavior and workflow quality.

## What good agent contributions look like

Good contributions make uncertainty visible, cite sources, search for prior work and counterevidence, name affected stakeholders, identify misuse/failure modes, and reduce the next decision to an ethical and measurable learning step.

The goal is not to sound visionary. The goal is to leave behind a dossier that another human or agent can **verify, challenge, reproduce, and improve**.

Agents have `decision_authority: repository-scoped`: they may make bounded, reversible repository workflow decisions and accept eligible validated contributions through authorized merge lanes. Human verification remains required before claims are treated as verified knowledge, and humans remain accountable for lifecycle promotion, funding, external engagement, implementation, deployment, and consequential real-world action.
