# Agent task coordination

Use this lightweight protocol when working from `agents/work-queue.yaml` or one of its linked Issues. The goal is to reduce duplicate effort without creating ownership, authority, or artificial scarcity around open research questions.

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
decision_authority: none
```

A claim is a coordination signal only. It does not reserve a topic, confer priority, imply endorsement, or authorize lifecycle changes.

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
decision_authority: none
```

If you stop working before submitting, release it explicitly:

```text
CLAIM RELEASED
reason: <brief reason>
decision_authority: none
```

Expired claims are treated as inactive. Another contributor may proceed, while preserving and crediting any useful partial work already posted.

## Parallel work is sometimes useful

Independent parallel analysis is appropriate when it tests robustness, explores a genuinely different evidence base, or intentionally reproduces a result. Say so explicitly in the claim scope. Avoid redundant parallel work that adds volume without new evidence or disagreement.

## Authority boundary

All claims and resulting agent-produced artifacts require human verification. Agents have `decision_authority: none`; claims cannot accept, prioritize, classify, promote, fund, deploy, or otherwise decide the fate of a dossier.
