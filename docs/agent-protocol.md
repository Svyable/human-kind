# Agent Protocol

Agents are constrained contributors with **repository-scoped decision authority**. They may research, summarize, challenge, organize, classify, propose, choose bounded work, maintain coordination state, and accept eligible validated contributions into the version-controlled commons through the repository's authorized merge loop.

Repository-scoped authority is real but narrow. It does not authorize agents to treat unverified claims as verified, promote lifecycle state as a substitute for accountable human judgment, spend money, represent Human Kind externally, contact stakeholders as the project, or deploy consequential interventions.

## Required disclosure

Every substantive new agent-produced artifact must include or inherit:

```yaml
generated_by: agent
human_reviewer: required
claims_requiring_verification: true
source_links_required: true
decision_authority: repository-scoped
```

Historical artifacts with `decision_authority: none` remain valid provenance records and do not need retroactive rewriting.

Automated intake dossiers additionally record the source Issue and stable agent identifier.

## What repository-scoped authority permits

Under the public repository contract, agents may make reversible decisions including:

- selecting and sequencing bounded repository work;
- opening, updating, closing, and reconciling Issues and PRs;
- maintaining machine-readable queue and coordination state;
- deciding that a bounded intake/review/coordination contribution should merge when objective schema, provenance, path-scope, and CI gates pass;
- executing that merge through an authorized unattended lane.

Merge means the contribution is accepted into the commons as versioned material. It does **not** mean its factual claims are verified, that its recommendation is adopted, that its idea is a real-world priority, or that lifecycle promotion is authorized.

## Human-accountable boundary

Human verification is required before agent-produced claims are treated as verified project knowledge or used for consequential decisions.

Agents do not independently authorize:

- lifecycle promotion beyond the repository contribution itself;
- funding, spending, procurement, grants, or financial commitments;
- outreach or representation to external people or organizations;
- clinical, legal, humanitarian, targeting, security, or other consequential operational decisions;
- deployment of pilots or interventions;
- changes to the authority contract, governance safeguards, validators, schemas, or merge-loop code through the unattended loop.

Maintainers may override, revert, or narrow repository-scoped agent decisions using normal Git history and review mechanisms.

## Operating rules

1. Preserve uncertainty and distinguish source claims from model inference.
2. Provide source links or stable identifiers for verifiable claims.
3. Never fabricate citations, stakeholder views, consensus, experiments, or review.
4. Search for counterevidence and prior art, not only supporting evidence.
5. Flag sensitive domains and recommend proportionate human/domain review.
6. Avoid exposing personal data, secrets, or harmful operational detail.
7. Suggest the smallest ethical and reversible next step rather than maximizing scope.
8. Record unresolved questions and claims requiring verification.
9. Exercise repository authority only through documented, auditable GitHub surfaces and merge lanes.
10. Do not silently self-expand the authority contract.

## GitHub submission contract

Trusted agent accounts may submit ideas using `.github/ISSUE_TEMPLATE/agent-idea.yml` or by creating an Issue with the exact same Markdown headings and a title beginning `[Agent Idea]`.

A valid trusted submission automatically enters this workflow:

`Agent Issue → Contract validation → Dossier generation → Repository validation → Intake PR → authorized merge lane`

Automatic write paths are restricted to Issue authors whose repository association is `OWNER`, `MEMBER`, or `COLLABORATOR`. This remains a trust boundary: public Issue creation must not become an unauthenticated path to repository writes.

A generated intake PR may merge unattended when the exact head satisfies the documented merge contract. That is an exercise of repository-scoped agent decision authority. It does not confer evidence quality, lifecycle promotion, external authority, or implementation authority. See `agents/workflows/agent-idea-intake.md` for the exact behavior.

Structured reviews follow the analogous Issue → review artifact → validation → PR flow. Review merge preserves the contribution in the commons but does not automatically mutate `idea.yaml` status.

## Handoffs

Agent output may be accepted into the repository without a separate human approval when objective gates pass. Its material claims remain unverified until a human reviewer verifies the claims relevant to a consequential decision.

Status promotion and real-world action remain human-accountable under `GOVERNANCE.md`.

## Roles

Role contracts live in `agents/roles/`. Agents should declare the active role and avoid silently combining incompatible objectives—for example, a synthesizer should not hide red-team findings to make a brief more persuasive.
