# Agent Idea Intake Workflow

This workflow turns a trusted agent-authored GitHub Issue into a versioned **intake dossier pull request**. It does not accept, prioritize, validate, or merge the idea.

## Flow

`Agent Issue → Contract validation → Dossier generation → Repository validation → Intake PR → Human review`

1. A trusted agent opens an Issue whose title begins with `[Agent Idea]` and whose body follows the **Agent idea submission** Issue Form headings.
2. `.github/workflows/agent-idea-intake.yml` runs only for Issue authors whose GitHub `author_association` is `OWNER`, `MEMBER`, or `COLLABORATOR`.
3. `scripts/agent_issue_to_dossier.py` treats all Issue content as untrusted text, validates enum values and required fields, and creates a dossier under `ideas/<domain>/HK-<issue-number>-<slug>/`.
4. The generator creates `idea.yaml`, `README.md`, `proposal.md`, `evidence.md`, `risks.md`, and `updates.md`, and adds the dossier to `data/idea-index.yaml`.
5. The normal repository validator runs before any branch is pushed.
6. A new `agent-intake/issue-<number>` branch and PR are created. The PR explicitly records that human review is required and decision authority is none.
7. Merging the PR closes the source Issue. Lifecycle promotion beyond `intake` is a separate human-reviewed change.

## Trust boundary

Public Issues are intentionally **not** a write primitive. An untrusted account may open an Issue with the title prefix, but the workflow will only leave an explanatory comment. To auto-materialize ideas, an agent account must be a repository collaborator (or act through a trusted maintainer-controlled integration).

This protects the repository from arbitrary public users creating branches and PRs through a workflow with `contents: write` permission.

## Agent contract

Agents must provide:

- a stable agent identifier and declared constrained role;
- primary domain, geography, time horizon, beneficiaries, intervention type, and reversibility;
- a bounded problem statement, intervention, and causal mechanism;
- prior work/sources and an explicit falsification condition;
- risks, equity/legitimacy analysis, required participants/reviewers, success metrics, and the smallest responsible next step;
- all three attestations in the Issue Form.

The generated metadata records:

```yaml
generated_by: agent
human_reviewer: required
claims_requiring_verification: true
source_links_required: true
decision_authority: none
source_issue: <issue URL>
source_agent: <stable agent identifier>
```

## Programmatic submission

Agents do not have to use the GitHub web form, but programmatic Issue bodies must render the same `###` headings, in the same names, as `.github/ISSUE_TEMPLATE/agent-idea.yml`. The parser intentionally refuses loosely structured prose so automation cannot silently guess missing safety or evidence fields.

Use a title of the form:

```text
[Agent Idea] Short, testable proposal title
```

Never include credentials, private keys, personal secrets, or sensitive source material in an Issue. GitHub Issues and generated PRs are public in this repository.

## Failure behavior

If contract parsing or repository validation fails, no branch is pushed. The workflow comments on the source Issue with a link to the failed Actions run. A corrected submission should be opened as a new Issue; the initial version intentionally does not rewrite already-created intake branches from edited Issues.
