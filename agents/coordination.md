# Agent task coordination

Use this lightweight protocol when working from `agents/work-queue.yaml` or one of its linked Issues. The goal is to reduce duplicate effort while keeping repository coordination reversible and auditable.

Agents have **repository-scoped decision authority** over bounded coordination actions such as claiming, releasing, reconciling, or closing repository work. A claim still does not create exclusive ownership, real-world priority, lifecycle authority, or permission to act outside the repository.

## Before starting

1. Read the linked task Issue, dossier, existing reviews, and relevant role contract.
2. Check the Issue conversation for an active claim using the format below.
3. If another contributor is already working, prefer complementing their scope, reviewing their output, or choosing another queue item rather than duplicating the same work.

## Claim format

Post one concise Issue comment before beginning substantial work:

```text
CLAIM
agent: <stable identifier or GitHub handle>
role: <scout|skeptic|synthesizer|taxonomist|pilot-designer|red-team>
scope: <one sentence describing the bounded contribution>
expected_output: <issue comment|agent review issue|pull request>
expires: <YYYY-MM-DD, no more than 7 days from claim>
decision_authority: repository-scoped
```

A claim is a repository coordination decision. It may influence which agent works on which bounded task, but it does not reserve a topic, establish real-world priority, verify evidence, imply endorsement, or authorize lifecycle changes.

## While working

- Keep scope bounded to the task and declared role.
- Cite sources for substantive factual claims and preserve counterevidence.
- If your scope changes materially, update the claim in a new comment rather than silently expanding it.
- Do not contact external stakeholders, spend funds, run real-world interventions, or represent Human Kind externally.

## Completing or releasing a claim

When the contribution is submitted, add a short comment linking the output and mark the claim complete:

```text
CLAIM COMPLETE
output: <URL>
human_verification: required
decision_authority: repository-scoped
```

If you stop working before submitting, release it explicitly:

```text
CLAIM RELEASED
reason: <brief reason>
decision_authority: repository-scoped
```

Expired claims are treated as inactive. Another contributor may proceed, while preserving and crediting any useful partial work already posted.

## Parallel work is sometimes useful

Independent parallel analysis is appropriate when it tests robustness, explores a genuinely different evidence base, or intentionally reproduces a result. Say so explicitly in the claim scope. Avoid redundant parallel work that adds volume without new evidence or disagreement.

## Authority boundary

Claims and resulting new agent-produced artifacts use `decision_authority: repository-scoped`. Agents may make bounded, reversible repository coordination and merge decisions through documented lanes. Human verification is still required before claims are treated as verified project knowledge, and agents may not independently promote lifecycle state, fund or spend, deploy, contact or represent Human Kind externally, or make other consequential real-world decisions.
