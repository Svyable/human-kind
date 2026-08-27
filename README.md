# Human Kind

> **Human Kind is a version-controlled commons for finding, testing, and improving ideas that could reduce suffering and expand human flourishing—through evidence, humility, participation, and measurable action.**

Human Kind is an open, evidence-oriented idea commons. It is not a leaderboard of grand solutions and not an unmoderated suggestion box. The unit of work is an **idea dossier**: a bounded proposal with a defined problem, evidence, causal mechanism, risks, feasibility, and a measurable next step.

## Lifecycle

`Intake → Triage → Research → Design → Pilot → Evaluation → Adopt / Archive`

Repository statuses make that lifecycle explicit:

- `intake` — formatted but not yet reviewed
- `needs-evidence` — promising, but factual basis is incomplete
- `needs-scope` — problem or intervention is too broad
- `researching` — active literature, stakeholder, or landscape work
- `designed` — theory of change and pilot plan are credible
- `pilot-ready` — ethics, ownership, metrics, and safeguards defined
- `piloting` — real-world or simulated test underway
- `validated` — evaluation supports continuation or expansion
- `not-pursuing` — declined with documented reasoning
- `archived` — superseded, inactive, or historically retained

A `not-pursuing` outcome is useful research output. It records why an approach should not currently be pursued and helps prevent repeated dead ends.

## How to contribute

1. Read [`docs/charter.md`](docs/charter.md), [`docs/principles.md`](docs/principles.md), and [`CONTRIBUTING.md`](CONTRIBUTING.md).
2. Search existing dossiers and issues for related work.
3. Start from [`ideas/_template/`](ideas/_template/) and keep claims calibrated to the available evidence.
4. Use Issues for collaboration and Pull Requests for versioned changes to dossiers, rubrics, taxonomy, governance, or agent workflows.
5. Expect human review before any dossier is promoted beyond `intake`.

## Evaluation philosophy

We reward epistemic quality and practical responsibility, not rhetorical ambition. Reviews keep the underlying dimensions visible rather than collapsing them into a single “humanity score”:

| Dimension | Weight |
| --- | ---: |
| Problem importance | 20% |
| Evidence | 20% |
| Tractability | 15% |
| Expected impact | 15% |
| Equity and legitimacy | 15% |
| Safety and misuse | 10% |
| Open collaboration | 5% |

See [`docs/evaluation-rubric.md`](docs/evaluation-rubric.md) for scoring guidance and narrative review requirements.

## Human–agent collaboration

Agents may search, summarize, challenge, organize, classify, and propose. They do **not** have decision authority. Acceptance, prioritization, external engagement, and implementation remain accountable human decisions.

Agent-produced artifacts must disclose:

```yaml
generated_by: agent
human_reviewer: required
claims_requiring_verification: true
source_links_required: true
decision_authority: none
```

See [`docs/agent-protocol.md`](docs/agent-protocol.md) and [`agents/roles/`](agents/roles/) for role-specific contracts.

## Repository map

- `docs/` — charter, principles, evidence standards, taxonomy, governance support
- `ideas/` — versioned idea dossiers grouped by domain
- `research/` — landscape maps, literature reviews, datasets, replication work
- `pilots/` — pilot plans and templates
- `evaluations/` — methods, scorecards, and completed evaluations
- `agents/` — constrained roles, prompts, workflows, schemas, and evals
- `data/` — machine-readable taxonomy, idea index, and source metadata
- `archive/` — declined, superseded, and historical material

## First milestones

1. **Foundation** — charter, contribution rules, governance, taxonomy, dossier template, evidence standard, and evaluation rubric.
2. **Seed corpus** — 10–20 high-quality dossiers across distinct domains, including some `not-pursuing` examples.
3. **Agent harness** — source-research, skeptical-review, and taxonomy workflows with test cases and human acceptance criteria.
4. **Pilot track** — a small number of ideas with accountable owners, stakeholders, budget assumptions, metrics, safeguards, and stop conditions.
5. **Public index** — a browsable view generated from `data/idea-index.yaml`, centered on status, evidence, domains, and review freshness rather than popularity.

## Safety, conduct, and governance

Participation is subject to [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), [`SECURITY.md`](SECURITY.md), and [`GOVERNANCE.md`](GOVERNANCE.md). Proposals involving high-stakes or sensitive domains require proportionate expert and affected-community review.

## License

See [`LICENSE`](LICENSE) for the repository’s content/code licensing policy.
