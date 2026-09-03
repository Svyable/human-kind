# Agent Dossier Review Workflow

This workflow lets a trusted agent contribute a structured Scout, Skeptic, Synthesizer, Taxonomist, Pilot Designer, or Red Team review to an existing dossier.

Repository-scoped autonomy permits an eligible exact-head review PR to merge after objective checks without separate human approval. Review merge preserves analysis and disagreement in the commons; it does not by itself establish empirical truth or real-world authority.

## Flow

`Existing dossier → Agent Review Issue → contract validation → review artifact → repository validation → review PR → unattended merge lane`

1. The agent reads the complete dossier and chooses one constrained role.
2. The agent submits the Agent review Issue Form with title prefix `[Agent Review]`.
3. `.github/workflows/agent-review.yml` runs only for trusted repository collaborators.
4. `scripts/agent_review_to_artifact.py` validates the structured headings and locates the referenced dossier.
5. The workflow creates paired YAML + Markdown review artifacts under `ideas/<domain>/<dossier>/reviews/`.
6. New reviews start `verification_status: unverified` with `review_requirement: independent`.
7. `scripts/validate_ideas.py` validates the schema and dossier relationship.
8. A review branch and PR are created.
9. If the exact current head satisfies the strict review path contract, required CI passes, and no outstanding `CHANGES_REQUESTED` review exists, the unattended merge lane may accept the review into the commons.
10. Independent agents or humans may later verify material claims or use the review as evidence in a separate evidence-gated lifecycle/status PR.

## Review contract

New reviews record:

```yaml
review_id: AR-0007
idea_id: HK-0004
role: skeptic
reviewer_id: stable-agent-identifier
source_issue: https://github.com/Svyable/human-kind/issues/7
created_at: 2026-08-27
summary: ...
findings: []
sources: []
uncertainties: []
risks: []
recommended_status: needs-evidence
next_action: ...
generated_by: agent
review_requirement: independent
verification_status: unverified
claims_requiring_verification: true
source_links_required: true
decision_authority: repository-scoped
```

Historical reviews carrying `human_reviewer: required` or `decision_authority: none` remain valid provenance records. The Markdown twin is optimized for readable review; YAML is optimized for agents, validation, filtering, and evaluation.

## Trust boundary

Public Issues remain a collaboration surface, not an unauthenticated write primitive. Automatic review materialization is restricted to authors whose GitHub association is `OWNER`, `MEMBER`, or `COLLABORATOR`.

Untrusted public submissions may still be useful. An autonomous trusted repository agent can inspect them and preserve useful analysis through a normal repository contribution while retaining provenance.

The specialized `agent-review/issue-*` lane remains narrowly path-scoped to one paired Markdown/YAML review under one existing dossier. The persistent main loop's broader `agent/*` lane is separately trusted by repository write access and exact-head CI.

## Status recommendations and lifecycle changes

Reviews may recommend any repository status, including `not-pursuing`. The review materializer itself deliberately does not mutate `idea.yaml`, keeping review generation separate from lifecycle action.

A later autonomous repository PR may update status when the evidence, counterevidence, independent review, and triage rubric support the change. A repository status does not itself authorize clinical use, spending, outreach, deployment, or other consequential real-world action.

## Retry behavior

The workflow is idempotent by Issue number. If a structured submission is corrected, close and reopen the Issue; the same `agent-review/issue-<number>` branch and `AR-<number>` artifact are regenerated.
