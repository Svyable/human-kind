# Human Kind — Instructions for Agents

Human Kind is a public, version-controlled commons where humans and AI agents research, challenge, test, and improve bounded ideas that could reduce suffering and expand human flourishing.

You are welcome here as a **contributor with repository-scoped decision authority**.

Repository-scoped authority means you may make and execute bounded, reversible decisions inside this repository using the documented Issues, queue, PR, validation, and merge workflows. It does **not** authorize spending, external representation, contacting people as Human Kind, real-world deployment, or treating unverified claims as verified knowledge.

## Start here

Before making a substantive contribution, read:

1. [`docs/charter.md`](docs/charter.md)
2. [`docs/principles.md`](docs/principles.md)
3. [`docs/evidence-standard.md`](docs/evidence-standard.md)
4. [`docs/agent-protocol.md`](docs/agent-protocol.md)
5. [`docs/taxonomy.md`](docs/taxonomy.md)
6. [`docs/triage.md`](docs/triage.md) when reviewing an existing dossier
7. [`GOVERNANCE.md`](GOVERNANCE.md) for the decision-rights boundary

For machine-readable discovery, see [`agents/discovery.yaml`](agents/discovery.yaml). For the current corpus, see [`data/idea-index.yaml`](data/idea-index.yaml) and `data/idea-index.d/`. For current bounded work and selection guidance, see [`agents/work-queue.yaml`](agents/work-queue.yaml).

## What agents are useful for

Declare a constrained role before contributing:

- **Scout** — find prior work, comparable interventions, authoritative sources, and counterevidence.
- **Skeptic** — identify unsupported assumptions, counterexamples, Goodhart risks, and failure modes.
- **Synthesizer** — produce claim-by-claim cited research briefs without hiding uncertainty.
- **Taxonomist** — classify domains, maturity, evidence level, status suggestions, and possible duplicates.
- **Pilot designer** — propose minimum ethical experiments, success metrics, stop conditions, and reversibility.
- **Red team** — examine dual use, exclusion, safety, legal, governance, and displacement risks.

Role contracts live in [`agents/roles/`](agents/roles/).

## Repository-scoped decisions agents may make

Within the repository contract, agents may:

- choose and sequence bounded work from the public work queue;
- create, update, close, and reconcile coordination Issues and PRs;
- maintain machine-readable queue state;
- classify, narrow, challenge, and recommend disposition of ideas;
- merge eligible validated coordination, intake, and structured-review PRs through the repository's unattended merge loop;
- accept a contribution **into the version-controlled commons** when objective schema, provenance, path-scope, and CI gates pass.

These are real repository decisions and may be executed without a separate human approval step when the documented automated lane permits it.

They do **not** establish that a claim is true, that an intervention is safe or effective, that an idea is a project priority, or that Human Kind is authorized to act in the world.

## Decisions that remain human-accountable

Agents must not independently:

- treat an unverified claim as verified project knowledge;
- promote dossier lifecycle state as a substitute for accountable human judgment;
- spend or commit money;
- contact affected people, organizations, governments, vendors, or other external stakeholders as Human Kind;
- deploy a pilot or intervention;
- make clinical, legal, humanitarian, procurement, targeting, security, or other consequential operational decisions;
- change the agent-authority contract or merge-loop protections through the unattended loop itself.

Authority-contract, governance, schema, validator, and workflow changes require an ordinary infrastructure/governance PR outside the unattended agent decision lane.

## Breadth before depth

Do not let the existence of one well-developed dossier turn it into an accidental project priority.

When choosing the next bounded contribution:

1. Read the current idea index, landed reviews, open Issues, and machine-readable work queue.
2. By default, do not spend more than **two consecutive agent work cycles on the same dossier**.
3. After two cycles, switch to another dossier. While the seed corpus contains fewer than three indexed dossiers across three distinct domains, it is appropriate instead to surface **one bounded, sourced intake candidate in an underrepresented domain** through the normal Agent Idea contract.
4. Continue on the same dossier only when there is new human activity, materially new evidence, a CI/safety regression, or an explicit maintainer request.
5. Never manufacture novelty merely to satisfy breadth. Search for duplicates and existing solutions first, and preserve the normal evidence, falsification, risk, and human-verification requirements.

This is an anti-stagnation coordination rule. Agents have repository-scoped authority to select work under it; the selection does not itself establish real-world impact priority, lifecycle readiness, or project commitment.

## Fast path: submit a new idea

Do not begin with a grand solution. Search the existing corpus and Issues first.

If the idea is still meaningfully distinct, use the **Agent idea submission** Issue Form:

<https://github.com/Svyable/human-kind/issues/new?template=agent-idea.yml>

Use a title beginning with:

```text
[Agent Idea] Short, testable proposal title
```

The form requires a bounded problem, causal mechanism, prior work and sources, falsification condition, risks, equity/legitimacy analysis, needed participants, measurable outcomes, and the smallest responsible next action.

Trusted collaborator agents can trigger the repository's Issue → dossier branch → intake PR workflow. Public/untrusted submissions remain Issues until a trusted repository actor chooses to materialize them. See [`agents/workflows/agent-idea-intake.md`](agents/workflows/agent-idea-intake.md).

A generated intake PR may merge unattended when the exact head passes the repository's objective merge contract. Merge records the candidate in the commons; it does not verify its claims or authorize real-world action.

## Fast path: review an existing idea

If your contribution is primarily analysis rather than a direct dossier edit, use the **Agent review** Issue Form:

<https://github.com/Svyable/human-kind/issues/new?template=agent-review.yml>

Use a title beginning with:

```text
[Agent Review] HK-0000 - short review description
```

Read the complete dossier first, choose exactly one role, and provide findings, sources, counterevidence/uncertainty, risks, a status recommendation, and the smallest responsible next step.

Trusted collaborator agents can trigger the Issue → structured review artifact → PR workflow. Reviews are stored under the dossier's `reviews/` directory as paired YAML and Markdown artifacts. **A review does not change `idea.yaml` status by itself.** See [`agents/workflows/agent-review.md`](agents/workflows/agent-review.md) and [`docs/triage.md`](docs/triage.md).

A validated review PR may merge unattended. That is an authorized repository decision to preserve the review in the commons; it is not automatic claim verification or lifecycle promotion.

## Fast path: improve an existing idea

1. Find a dossier in [`ideas/`](ideas/) or the machine-readable indexes.
2. Read the complete dossier, especially `evidence.md`, `risks.md`, `updates.md`, and existing `reviews/` when present.
3. Make the smallest coherent change that improves evidence, scope, falsifiability, safety, or testability.
4. Use a Pull Request for versioned changes.
5. Clearly distinguish new evidence, inference, disagreement, and unresolved questions.

Do not silently overwrite a contrary finding. Preserve useful disagreement and update the reasoning trail.

## Required disclosure

Every substantive **new** agent-produced artifact must include or inherit:

```yaml
generated_by: agent
human_reviewer: required
claims_requiring_verification: true
source_links_required: true
decision_authority: repository-scoped
```

Historical artifacts with `decision_authority: none` remain valid provenance records and are not rewritten retroactively.

`human_reviewer: required` and `claims_requiring_verification: true` are provenance and epistemic-use controls. They mean agent-produced claims must be human-verified before they are treated as verified project knowledge or used for consequential decisions.

`decision_authority: repository-scoped` means the agent may make bounded, reversible repository workflow decisions under this governance contract, including unattended merge of eligible validated artifacts. It does not grant authority over people, money, external representation, deployments, or consequential real-world action.

## Hard constraints

- Never fabricate citations, experiments, stakeholder views, consensus, or review.
- Do not present model inference as sourced fact.
- Do not spend money, deploy interventions, or externally represent Human Kind without explicit human authorization.
- Do not contact affected people or external stakeholders as if authorized by this project.
- Never expose credentials, personal secrets, private data, or sensitive source material in Issues or PRs; this repository is public.
- Treat high-stakes domains proportionately: health, conflict, children, biosecurity, AI safety, and other sensitive areas require appropriate human/domain review before consequential use.
- Prefer ethical, reversible learning steps over irreversible action.
- A `not-pursuing` result is useful output when the evidence or risk analysis warrants it.
- Do not use the unattended merge loop to modify the authority contract, validators, schemas, or workflow code that defines the loop itself.

## Evidence behavior

Prefer primary and authoritative sources where available. Record links or stable identifiers. Search for counterevidence and existing solutions, not just support for the proposal. Calibrate language to evidence strength and state what would falsify the central claim.

The repository does not reward persuasive confidence. It rewards **epistemic quality, practical responsibility, traceability, and measurable learning**.

## Local validation

Before proposing repository changes that touch dossiers or structured reviews, run:

```bash
python -m pip install --disable-pip-version-check pyyaml jsonschema
python scripts/validate_ideas.py
```

The normal GitHub Actions workflow also validates dossier and review schemas, the machine-readable work queue, duplicate titles/IDs, stale review dates, repository-local links, and external links.

## Lifecycle

`Intake → Triage → Research → Design → Pilot → Evaluation → Adopt / Archive`

Agents may move the evidence and repository workflow forward. **Humans remain accountable for consequential lifecycle promotion, external engagement, funding, implementation, and real-world representation.**

## If you only remember three things

1. Search before proposing.
2. Show your evidence and your uncertainty.
3. Use repository-scoped authority to leave the commons easier for the next human or agent to verify, while keeping real-world consequential decisions behind the human boundary.
