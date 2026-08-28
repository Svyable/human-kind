# Agent Dossier Review Workflow

This workflow lets a trusted agent contribute a structured Scout, Skeptic, Synthesizer, Taxonomist, Pilot Designer, or Red Team review to an **existing** dossier.

It does not change the dossier, accept the review as correct, or promote lifecycle status.

## Flow

`Existing dossier → Agent Review Issue → Contract validation → Review artifact → Repository validation → Review PR → Human verification`

1. The agent reads the complete dossier and chooses one constrained role.
2. The agent submits the **Agent review** Issue Form with title prefix `[Agent Review]`.
3. `.github/workflows/agent-review.yml` runs only for trusted repository collaborators.
4. `scripts/agent_review_to_artifact.py` validates the structured headings and locates the referenced dossier.
5. The workflow creates a paired YAML + Markdown review under `ideas/<domain>/<dossier>/reviews/`.
6. `scripts/validate_ideas.py` validates the review schema and confirms it belongs to the parent dossier.
7. A review branch and Pull Request are created.
8. Human reviewers verify material claims and decide whether any separate dossier change is warranted.

## Review contract

Every review records:

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
human_reviewer: required
claims_requiring_verification: true
source_links_required: true
decision_authority: none
```

The Markdown twin is optimized for human review; the YAML artifact is optimized for agents, validation, filtering, and future evaluation.

## Trust boundary

Public Issues remain a collaboration surface, not a write primitive. Automatic branch/PR materialization is restricted to authors whose GitHub association is `OWNER`, `MEMBER`, or `COLLABORATOR`.

Untrusted submissions may still be useful. A maintainer can inspect them and manually promote the useful analysis without granting the submitter repository write capability.

## Status recommendations

Agents may recommend any repository status, including `not-pursuing`. The recommendation is explicitly non-authoritative.

A status change requires a separate dossier Pull Request and human review under [`../../docs/triage.md`](../../docs/triage.md).

## Retry behavior

The workflow is idempotent by Issue number. If a structured submission is corrected, close and reopen the Issue; the same `agent-review/issue-<number>` branch and `AR-<number>` artifact are regenerated.
