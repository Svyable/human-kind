# Agent Dossier Review Workflow

This workflow lets a trusted agent contribute a structured Scout, Skeptic, Synthesizer, Taxonomist, Pilot Designer, or Red Team review to an **existing** dossier.

Repository-scoped agent authority permits an eligible validated review artifact to be accepted into the version-controlled commons through the authorized unattended merge lane. Review merge does not verify the review as correct and does not change dossier lifecycle status.

## Flow

`Existing dossier → Agent Review Issue → Contract validation → Review artifact → Repository validation → Review PR → authorized merge lane`

1. The agent reads the complete dossier and chooses one constrained role.
2. The agent submits the **Agent review** Issue Form with title prefix `[Agent Review]`.
3. `.github/workflows/agent-review.yml` runs only for trusted repository collaborators.
4. `scripts/agent_review_to_artifact.py` validates the structured headings and locates the referenced dossier.
5. The workflow creates a paired YAML + Markdown review under `ideas/<domain>/<dossier>/reviews/`.
6. `scripts/validate_ideas.py` validates the review schema and confirms it belongs to the parent dossier.
7. A review branch and Pull Request are created.
8. If the exact current PR head satisfies the documented branch/path contract, required CI passes, and no outstanding `CHANGES_REQUESTED` review exists, the authorized unattended merge lane may accept the review into the commons.
9. Human reviewers verify material claims before consequential use and decide whether any separate lifecycle change is warranted.

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
human_reviewer: required
claims_requiring_verification: true
source_links_required: true
decision_authority: repository-scoped
```

Historical reviews with `decision_authority: none` remain valid provenance records. The Markdown twin is optimized for human review; the YAML artifact is optimized for agents, validation, filtering, and future evaluation.

## Trust boundary

Public Issues remain a collaboration surface, not a write primitive. Automatic branch/PR materialization is restricted to authors whose GitHub association is `OWNER`, `MEMBER`, or `COLLABORATOR`.

Untrusted submissions may still be useful. A maintainer or trusted repository agent can inspect them and manually promote useful analysis without granting the submitter repository write capability.

The unattended review lane is narrowly path-scoped to one paired Markdown/YAML review under one existing dossier, tied to the exact validated head SHA, and subject to a `CHANGES_REQUESTED` veto. It cannot modify governance, schemas, validators, the authority contract, or the merge workflow itself.

## Status recommendations

Agents may recommend any repository status, including `not-pursuing`. The recommendation is explicitly distinct from lifecycle mutation.

A status change requires a separate dossier Pull Request and accountable human judgment under [`../../docs/triage.md`](../../docs/triage.md). Repository-scoped authority over review merge does not itself promote lifecycle status.

## Retry behavior

The workflow is idempotent by Issue number. If a structured submission is corrected, close and reopen the Issue; the same `agent-review/issue-<number>` branch and `AR-<number>` artifact are regenerated.
