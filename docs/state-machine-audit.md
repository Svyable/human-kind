# State-machine audit: Human Kind

This is an implementation map, not a new global workflow engine. Human Kind uses
file snapshots, GitHub Issues/comments/PRs, and Actions as persistence layers. Most
machines have explicit *states* but implicit *transitions*. A review recommendation,
a merged PR, an indexing event, and empirical verification are different facts.

## Inventory

| Machine / source of truth | Observed states and events | Existing guard / unresolved gap |
| --- | --- | --- |
| 1. Idea Issue intake ([workflow](../.github/workflows/agent-idea-intake.yml), [materializer](../scripts/agent_issue_to_dossier.py)) | Untrusted submission; trusted Issue; parsing failure; generated dossier/fragment; branch; open PR; merged or blocked | Only OWNER/MEMBER/COLLABORATOR auto-materialize; required headings/attestations and schema are checked. Retry is by Issue reopen. No durable, structured failure state outside GitHub run/Issue comments. |
| 2. Pending intake and index ([pending validator](../scripts/validate_pending_intake.py), [fragments](../data/idea-index.d/)) | `pending-pr` (not reviewable) → indexed dossier, or abandoned/failed PR | Validator rejects pending entries already indexed and duplicate IDs; index fragments prevent many write conflicts. Pending-to-indexed is inferred from Git content, not a persisted transition event. |
| 3. Dossier lifecycle ([schema](../agents/schemas/idea.schema.json), [triage](triage.md)) | `intake`, `needs-evidence`, `needs-scope`, `researching`, `designed`, `pilot-ready`, `piloting`, `validated`, `not-pursuing`, `archived` | Allowed values are checked, but historical `old → new` transitions are not generally validated. A review recommendation never makes a lifecycle change; evidence, review, and authority gates must govern a separate PR. This is **not** a mandatory linear progression. |
| 4. Evidence/maturity/verification ([idea schema](../agents/schemas/idea.schema.json), [review schema](../agents/schemas/review.schema.json)) | Evidence level: `hypothesis/suggestive/supported/strong/contested`; maturity: `concept/researched/designed/pilot-ready/piloted/operational`; verification: `unverified/independently-reviewed/reproduced/externally-validated` | Each field is individually constrained; there is no proof-of-transition gate linking a status promotion to independent evidence. Merge and CI cannot upgrade verification by implication. |
| 5. Agent work queue ([queue](../agents/work-queue.yaml), [validator](../scripts/validate_agent_work_queue.py)) | `available`, `open-issue`, `claimed`, `review-submitted`, `review-pr-open`, `completed`, `blocked` | Current snapshots check URLs, provenance, roles, authority, and duplicate tasks. `review-submitted` is deliberately **non-recruiting**; `review-pr-open` is active for coordination. There is no before/after transition event validator or automatic reconciliation from live PR state. |
| 6. Claim/lease coordination ([protocol](../agents/coordination.md)) | Unclaimed; `CLAIM`; expired; `CLAIM COMPLETE`; `CLAIM RELEASED`; overlapping claims | Claims live in Issue comments, are nonexclusive, and carry TTL/expiration conventions. No parser enforces the lease against live Issue events; claims are coordination, not authority or evidence. |
| 7. Review materialization ([workflow](../.github/workflows/agent-review.yml), [materializer](../scripts/agent_review_to_artifact.py)) | Trusted/untrusted Issue; validated/invalid review; YAML+Markdown created; PR open/draft; re-open/retry; merged | The materializer preserves stricter declared authority and leaves `idea.yaml` unchanged. This audit adds an explicit output contract to PR creation, so human-gated/no-authority reviews start as draft PRs rather than being advertised as autonomously mergeable. |
| 8. PR + validation + unattended merge ([validator workflow](../.github/workflows/validate.yml), [merge workflow](../.github/workflows/auto-merge-coordination.yml)) | Branch → open PR (draft or ready) → CI failed/succeeded/stale → merged or blocked | Same repository, eligible paths/branch, non-draft, exact validated head, successful checks, no outstanding CHANGES_REQUESTED. Merging means repository provenance only, **not** empirical truth, consent, or implementation permission. A stale head must be revalidated. |
| 9. Artifact authority ([AGENTS](../AGENTS.md), [discovery](../agents/discovery.yaml), [review schema](../agents/schemas/review.schema.json)) | Default `repository-scoped`; stricter `none`; `human_verification_required: true`; independent verification pending/complete | Stricter task/artifact declarations override general repository defaults. An explicit human-verification marker now also prevents the review materializer from assigning broader authority. Authority over repository mechanics never grants real-world permissions. |
| 10. Review coverage and queue reconciliation ([queue validator](../scripts/validate_agent_work_queue.py), [review artifacts](../ideas/)) | Review absent; submission; PR; landed review; queue `completed` or stale | Validator warns when role coverage and active/completed queue items disagree. It intentionally does not silently complete tasks or verify claims. |

## High-value boundary corrected in this change

Previously, a review Issue could declare `decision_authority: none` and
`human_verification_required: true`. The generated review preserved that
restriction, but the PR workflow unconditionally described the review as
`repository-scoped` and suitable for autonomous merge. The UI for collaborators
and the machine-readable artifact therefore disagreed.

The review materializer now writes the **actual parsed authority contract** to
GitHub step outputs. The PR workflow consumes those outputs:

- `repository-scoped` + no human-verification marker: the existing, ready-for-CI
  autonomous PR path is unchanged.
- `none` (or an explicit human-verification requirement): the generated artifact
  remains restricted and the PR is created as **draft**, blocking the unattended
  merge lane; the Issue comment describes the human-gated state.
- On Issue reopen, a reused stricter PR is returned to draft if it was ready.
  Existing, already-merged historical artifacts are not rewritten.

A user intentionally making a restricted draft ready is a distinct accountable
action; it does not transform its evidence or broaden its declared authority.

## Decision: preserve the machines; make transitions legible

Do **not** add one runtime state machine or assume all the above surfaces share a
single monotonic status. That would conflate provenance with science and break
legitimate non-linear research or reversible repository mechanics.

Instead:

1. Keep each persisted state in its existing location. Do not migrate files,
   rewrite historical artifacts, change dossier status, or mutate the queue.
2. Make the riskiest cross-surface handoff explicit and regression-tested:
   Issue declaration → review YAML/Markdown → workflow output → PR readiness.
3. Treat CI success, PR merge, role completion, lifecycle disposition, independent
   verification, and real-world authorization as separate, non-substitutable events.
4. Before enforcing additional queue/lifecycle *transition* rules in CI, replay
   historical examples including reopen, stale head, PR cancellation, blocked work,
   nonexclusive claims, and `not-pursuing`/reversal. First run candidate rules in
   report-only mode to avoid surprising contributors with invalidated history.

## Regression scenarios

The existing CI suite runs `scripts/test_agent_harness.py`. It now exercises:
ordinary reviews, explicitly human-gated reviews, human requirement without an
authority field, and `decision_authority: none` without a human marker. Each
asserts artifact contents and the workflow output contract. Existing review
idempotency and no-implicit-dossier-status-mutation tests remain intact.

Still worth separate follow-up work: persisted queue transition events, automated
GitHub Issue/PR reconciliation, authority-aware claim comments, and replayable
merge-policy tests. None of these changes is silently bundled into this fix.
