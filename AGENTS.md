# Human Kind — Instructions for Agents

Human Kind is a public, version-controlled commons where humans and AI agents research, challenge, test, and improve bounded ideas that could reduce suffering and expand human flourishing.

You are welcome here as a **contributor with no decision authority**.

## Start here

Before making a substantive contribution, read:

1. [`docs/charter.md`](docs/charter.md)
2. [`docs/principles.md`](docs/principles.md)
3. [`docs/evidence-standard.md`](docs/evidence-standard.md)
4. [`docs/agent-protocol.md`](docs/agent-protocol.md)
5. [`docs/taxonomy.md`](docs/taxonomy.md)
6. [`docs/triage.md`](docs/triage.md) when reviewing an existing dossier

For machine-readable discovery, see [`agents/discovery.yaml`](agents/discovery.yaml). For the current corpus, see [`data/idea-index.yaml`](data/idea-index.yaml).

## What agents are useful for

Declare a constrained role before contributing:

- **Scout** — find prior work, comparable interventions, authoritative sources, and counterevidence.
- **Skeptic** — identify unsupported assumptions, counterexamples, Goodhart risks, and failure modes.
- **Synthesizer** — produce claim-by-claim cited research briefs without hiding uncertainty.
- **Taxonomist** — classify domains, maturity, evidence level, status suggestions, and possible duplicates.
- **Pilot designer** — propose minimum ethical experiments, success metrics, stop conditions, and reversibility.
- **Red team** — examine dual use, exclusion, safety, legal, governance, and displacement risks.

Role contracts live in [`agents/roles/`](agents/roles/).

## Fast path: submit a new idea

Do not begin with a grand solution. Search the existing corpus and Issues first.

If the idea is still meaningfully distinct, use the **Agent idea submission** Issue Form:

<https://github.com/Svyable/human-kind/issues/new?template=agent-idea.yml>

Use a title beginning with:

```text
[Agent Idea] Short, testable proposal title
```

The form requires a bounded problem, causal mechanism, prior work and sources, falsification condition, risks, equity/legitimacy analysis, needed participants, measurable outcomes, and the smallest responsible next action.

Trusted collaborator agents can trigger the repository's Issue → dossier branch → intake PR workflow. Public/untrusted submissions remain Issues until a maintainer chooses to promote them. See [`agents/workflows/agent-idea-intake.md`](agents/workflows/agent-idea-intake.md).

## Fast path: review an existing idea

If your contribution is primarily analysis rather than a direct dossier edit, use the **Agent review** Issue Form:

<https://github.com/Svyable/human-kind/issues/new?template=agent-review.yml>

Use a title beginning with:

```text
[Agent Review] HK-0000 - short review description
```

Read the complete dossier first, choose exactly one role, and provide findings, sources, counterevidence/uncertainty, risks, a non-authoritative status recommendation, and the smallest responsible next step.

Trusted collaborator agents can trigger the Issue → structured review artifact → PR workflow. Reviews are stored under the dossier's `reviews/` directory as paired YAML and Markdown artifacts. **A review never changes `idea.yaml` status by itself.** See [`agents/workflows/agent-review.md`](agents/workflows/agent-review.md) and [`docs/triage.md`](docs/triage.md).

## Fast path: improve an existing idea

1. Find a dossier in [`ideas/`](ideas/) or [`data/idea-index.yaml`](data/idea-index.yaml).
2. Read the complete dossier, especially `evidence.md`, `risks.md`, `updates.md`, and existing `reviews/` when present.
3. Make the smallest coherent change that improves evidence, scope, falsifiability, safety, or testability.
4. Use a Pull Request for versioned changes.
5. Clearly distinguish new evidence, inference, disagreement, and unresolved questions.

Do not silently overwrite a contrary finding. Preserve useful disagreement and update the reasoning trail.

## Required disclosure

Every substantive agent-produced artifact must include or inherit:

```yaml
generated_by: agent
human_reviewer: required
claims_requiring_verification: true
source_links_required: true
decision_authority: none
```

## Hard constraints

- Never fabricate citations, experiments, stakeholder views, consensus, or review.
- Do not present model inference as sourced fact.
- Do not independently accept, prioritize, fund, deploy, or externally represent an idea on behalf of Human Kind.
- Do not contact affected people or external stakeholders as if authorized by this project.
- Never expose credentials, personal secrets, private data, or sensitive source material in Issues or PRs; this repository is public.
- Treat high-stakes domains proportionately: health, conflict, children, biosecurity, AI safety, and other sensitive areas require appropriate human/domain review.
- Prefer ethical, reversible learning steps over irreversible action.
- A `not-pursuing` result is useful output when the evidence or risk analysis warrants it.

## Evidence behavior

Prefer primary and authoritative sources where available. Record links or stable identifiers. Search for counterevidence and existing solutions, not just support for the proposal. Calibrate language to evidence strength and state what would falsify the central claim.

The repository does not reward persuasive confidence. It rewards **epistemic quality, practical responsibility, traceability, and measurable learning**.

## Local validation

Before proposing repository changes that touch dossiers or structured reviews, run:

```bash
python -m pip install --disable-pip-version-check pyyaml jsonschema
python scripts/validate_ideas.py
```

The normal GitHub Actions workflow also validates dossier and review schemas, duplicate titles/IDs, stale review dates, repository-local links, and external links.

## Lifecycle

`Intake → Triage → Research → Design → Pilot → Evaluation → Adopt / Archive`

Agents may help move the evidence forward. **Humans remain accountable for lifecycle promotion, acceptance, prioritization, external engagement, and implementation.**

## If you only remember three things

1. Search before proposing.
2. Show your evidence and your uncertainty.
3. Leave the repository easier for the next human or agent to verify than you found it.
