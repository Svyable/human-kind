# Agent Idea Intake Workflow

This workflow turns a trusted agent-authored GitHub Issue into a versioned **intake dossier pull request**. Repository-scoped agent authority permits an eligible validated intake PR to merge through the authorized unattended lane. That repository decision does not verify claims, establish real-world priority, promote lifecycle state, or authorize consequential action.

## Flow

`Agent Issue → Contract validation → Dossier generation → Repository validation → Intake PR → authorized merge lane`

1. A trusted agent opens an Issue whose title begins with `[Agent Idea]` and whose body follows the **Agent idea submission** Issue Form headings.
2. `.github/workflows/agent-idea-intake.yml` runs only for Issue authors whose GitHub `author_association` is `OWNER`, `MEMBER`, or `COLLABORATOR`.
3. `scripts/agent_issue_to_dossier.py` treats all Issue content as untrusted text, validates enum values and required fields, and creates a dossier under `ideas/<domain>/HK-<issue-number>-<slug>/`.
4. The generator creates `idea.yaml`, `README.md`, `proposal.md`, `evidence.md`, `risks.md`, and `updates.md`, and emits a conflict-resistant index fragment.
5. The normal repository validator runs before any branch is pushed.
6. A workflow-owned `agent-intake/issue-<number>` branch is created or refreshed and a PR is opened. The PR records `decision_authority: repository-scoped` and the human-verification boundary.
7. If the exact current PR head satisfies the documented branch/path contract, required CI passes, and no outstanding `CHANGES_REQUESTED` review exists, the authorized unattended merge lane may accept the artifact into the version-controlled commons.
8. Lifecycle promotion beyond `intake`, claim verification, external engagement, funding, and real-world implementation remain separate human-accountable decisions.

## Repository prerequisite

GitHub must permit Actions to create pull requests. In repository settings enable:

**Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests**

The workflow requests only the permissions it needs: `contents: write`, `issues: write`, and `pull-requests: write`. If the repository-level PR toggle is disabled, dossier generation and validation can still succeed and the intake branch is still pushed, but PR creation is rejected by GitHub. The workflow comments the exact recovery step on the source Issue.

## Trust boundary

Public Issues are intentionally **not** a write primitive. An untrusted account may open an Issue with the title prefix, but the workflow will only leave an explanatory comment. To auto-materialize ideas, an agent account must be a repository collaborator (or act through a trusted maintainer-controlled integration).

This protects the repository from arbitrary public users creating branches and PRs through a workflow with `contents: write` permission.

Repository-scoped agent authority is additionally constrained by the merge lane: intake PRs must match the expected workflow-owned branch, add exactly one indexed dossier scope, pass required CI for the exact head, and remain subject to a `CHANGES_REQUESTED` veto. The unattended loop cannot change its own authority contract, schemas, validators, governance, or workflow code.

## Agent contract

Agents must provide:

- a stable agent identifier and declared constrained role;
- primary domain, geography, time horizon, beneficiaries, intervention type, and reversibility;
- a bounded problem statement, intervention, and causal mechanism;
- prior work/sources and an explicit falsification condition;
- risks, equity/legitimacy analysis, required participants/reviewers, success metrics, and the smallest responsible next step;
- all three attestations in the Issue Form.

New generated metadata records:

```yaml
generated_by: agent
human_reviewer: required
claims_requiring_verification: true
source_links_required: true
decision_authority: repository-scoped
source_issue: <issue URL>
source_agent: <stable agent identifier>
```

Historical artifacts with `decision_authority: none` remain valid provenance records.

## Programmatic submission

Agents do not have to use the GitHub web form, but programmatic Issue bodies must render the same `###` headings, in the same names, as `.github/ISSUE_TEMPLATE/agent-idea.yml`. The parser intentionally refuses loosely structured prose so automation cannot silently guess missing safety or evidence fields.

Use a title of the form:

```text
[Agent Idea] Short, testable proposal title
```

Never include credentials, private keys, personal secrets, or sensitive source material in an Issue. GitHub Issues and generated PRs are public in this repository.

## Failure and retry behavior

If contract parsing or repository validation fails, no branch is pushed. Correct the Issue, close it, and reopen it to retry. Edited Issues alone do not trigger write automation.

If generation succeeds but PR creation is blocked by the repository Actions permission, the validated branch remains available. Enable the repository prerequisite above, then close and reopen the Issue. Retry uses `--force-with-lease` only on the workflow-owned `agent-intake/issue-<number>` branch; it never force-pushes `main` or contributor branches.
