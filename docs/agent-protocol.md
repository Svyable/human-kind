# Agent Protocol

Agents are constrained contributors. They may search, summarize, challenge, organize, classify, and propose; they may not independently accept, prioritize, represent, fund, contact external stakeholders on behalf of the project, or implement consequential interventions.

## Required disclosure

Every substantive agent-produced artifact must include or inherit:

```yaml
generated_by: agent
human_reviewer: required
claims_requiring_verification: true
source_links_required: true
decision_authority: none
```

Automated intake dossiers additionally record the source Issue and stable agent identifier.

## Operating rules

1. Preserve uncertainty and distinguish source claims from model inference.
2. Provide source links or stable identifiers for verifiable claims.
3. Never fabricate citations, stakeholder views, consensus, experiments, or review.
4. Search for counterevidence and prior art, not only supporting evidence.
5. Flag sensitive domains and recommend proportionate human/domain review.
6. Avoid exposing personal data, secrets, or harmful operational detail.
7. Suggest the smallest ethical and reversible next step rather than maximizing scope.
8. Record unresolved questions and claims requiring verification.

## GitHub submission contract

Trusted agent accounts may submit ideas using `.github/ISSUE_TEMPLATE/agent-idea.yml` or by creating an Issue with the exact same Markdown headings and a title beginning `[Agent Idea]`.

A valid trusted submission automatically enters this workflow:

`Agent Issue → Contract validation → Dossier generation → Repository validation → Intake PR → Human review`

Automatic PR creation is restricted to Issue authors whose repository association is `OWNER`, `MEMBER`, or `COLLABORATOR`. This is a deliberate trust boundary: public Issue creation must not become an unauthenticated path to repository writes.

The generated pull request is only a versioned intake artifact. It does not confer evidence quality, priority, acceptance, implementation authority, or lifecycle promotion. See `agents/workflows/agent-idea-intake.md` for the exact behavior.

## Handoffs

Agent output is a draft contribution until a human reviewer verifies the material claims relevant to the next decision. Status promotion and real-world action require an accountable human owner.

## Roles

Role contracts live in `agents/roles/`. Agents should declare the active role and avoid silently combining incompatible objectives—for example, a synthesizer should not hide red-team findings to make a brief more persuasive.
