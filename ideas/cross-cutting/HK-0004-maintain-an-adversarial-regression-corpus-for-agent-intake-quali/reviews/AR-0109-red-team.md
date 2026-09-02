# AR-0109 — Red Team review

**Idea:** HK-0004 — Maintain an adversarial regression corpus for agent intake quality  
**Agent:** `chatgpt-gpt-5.6-sol`  
**Source Issue:** https://github.com/Svyable/human-kind/issues/15  
**Created:** 2026-09-02  
**Decision authority:** none

> Agent-produced review. Human verification is required before this review influences lifecycle promotion or consequential action.

## Review summary

HK-0004 is most vulnerable not to a single catastrophic failure but to gradual benchmark capture: visible fixtures can become targets, stale cases can stop representing live intake failures, and a green regression suite can be misread as evidence of broader epistemic or safety quality. These risks do not falsify the proposal, but they narrow the responsible use of the corpus to recurrence prevention unless it is paired with holdouts or mutation checks, explicit coverage accounting, false-positive measurement, and pruning or refresh rules. Human verification is required before these findings are treated as verified project knowledge.

## Findings

- **REPOSITORY-SOURCED** — The dossier and AR-0008 already identify overfitting, false confidence, benchmark gaming, and narrow maintainer-defined criteria as material risks; the failure mode is therefore not hypothetical in the repository's own theory of change.
- **INFERENCE** — A public corpus can create evaluator leakage: once agents, prompts, or maintainers repeatedly see the same adversarial fixtures, changes may optimize specifically for those examples while leaving nearby unseen failures undetected.
- **INFERENCE** — Corpus staleness can create a false-negative blind spot if workflow code, schemas, agent behavior, or intake patterns evolve faster than fixtures are refreshed. A suite that never gains new representative cases can become easier to pass while becoming less informative.
- **INFERENCE** — Coverage metrics can themselves become Goodhart targets. Counting fixtures or defect classes may reward nominal breadth without testing whether high-impact or socially consequential failure mechanisms are represented.
- **INFERENCE** — Failure examples drawn mainly from maintainer-observed incidents can encode a narrow error model. This can systematically underrepresent failures visible only to domain reviewers or affected communities while still producing an apparently objective benchmark.
- **INFERENCE** — Sensitive-domain fixtures can leak or preserve harmful details if regression cases are copied too literally from real incidents. The safer pattern is aggressive minimization, synthetic or abstracted cases where possible, and explicit review before adding any fixture containing private, security-sensitive, or operational detail.
- **INFERENCE** — The bounded mitigation is a layered harness: stable public fixtures for known regressions; a small held-out or periodically refreshed set for generalization; seeded mutations for sensitivity; false-positive tracking on known-good submissions; and explicit corpus refresh or retirement criteria. None of these checks establishes downstream human judgment quality.

## Sources and evidence

- `ideas/cross-cutting/HK-0004-maintain-an-adversarial-regression-corpus-for-agent-intake-quali/proposal.md`
- `ideas/cross-cutting/HK-0004-maintain-an-adversarial-regression-corpus-for-agent-intake-quali/evidence.md`
- `ideas/cross-cutting/HK-0004-maintain-an-adversarial-regression-corpus-for-agent-intake-quali/risks.md`
- `ideas/cross-cutting/HK-0004-maintain-an-adversarial-regression-corpus-for-agent-intake-quali/reviews/AR-0008-skeptic.md`
- `agents/evals/README.md`

## Counterevidence and uncertainty

- The repository has not yet measured how often visible fixtures actually cause benchmark-specific optimization, so evaluator leakage is a plausible mechanism rather than an observed project fact.
- No landed evidence establishes the right refresh cadence, holdout size, mutation strategy, or retirement rule for this repository.
- Stable fixtures may still have substantial value for preventing recurrence even when they are poor proxies for generalization; the risk case supports layered evaluation rather than removal.
- Some socially consequential failures may not be safely or objectively reducible to automated regression fixtures at all and may require human domain review instead.

## Risks and safety

- Green CI may be interpreted as broader epistemic or safety assurance than the harness supports.
- Visible cases may incentivize benchmark-specific optimization and evaluator leakage.
- Stale fixtures may miss new failure classes while preserving a false sense of coverage.
- Coverage counts may reward nominal breadth rather than meaningful failure detection.
- Maintainer-derived cases may underrepresent domain-specific or affected-community failure modes.
- Sensitive examples may preserve private, harmful, or operational details if not minimized.
- Corpus growth without pruning can increase maintenance cost and make failures harder to interpret.

## Recommended status

`needs-evidence`

This is a recommendation only. It does not change `idea.yaml`.

## Smallest responsible next step

Add one repository-only red-team evaluation before expanding the corpus: choose one existing visible fixture family, create a small held-out variant and one seeded mutation that preserves the same underlying failure mechanism without copying the fixture surface form, then verify whether the current harness detects both while continuing to accept known-good intake examples. Record false positives and any miss explicitly. Do not change dossier lifecycle status or infer broader safety quality from the result.
