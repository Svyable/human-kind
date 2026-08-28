# AR-0008 — Skeptic review

**Idea:** HK-0004 — Maintain an adversarial regression corpus for agent intake quality  
**Agent:** `chatgpt-gpt-5.6-sol`  
**Source Issue:** https://github.com/Svyable/human-kind/issues/8  
**Created:** 2026-08-28  
**Decision authority:** none

> Agent-produced review. Human verification is required before this review influences lifecycle promotion or consequential action.

## Review summary

The proposal is coherent and reversible: a regression corpus could help catch known intake failures before workflow changes reach production. The current dossier, however, mainly cites GitHub Actions, JSON Schema, and an internal eval directory. Those sources support implementation mechanics, not the central causal claim that a curated regression corpus will materially improve epistemic, provenance, and safety quality. I therefore recommend `needs-evidence`, not rejection: the next experiment should first define defect classes, baseline failure rates, and acceptance criteria so the benchmark can be evaluated rather than merely accumulated.

## Findings

- The existing sources document CI and schema infrastructure but do not establish that regression fixtures detect meaningful epistemic or safety regressions.
- The proposed five positive and ten adversarial fixtures are a reasonable reversible starting point, but the sample size and case mix are currently arbitrary rather than derived from a failure taxonomy.
- Several success metrics are process metrics, such as deterministic rejection or easy fixture addition, rather than outcome metrics showing that important defects are caught with an acceptable false-positive rate.
- The dossier correctly names overfitting and false confidence as risks, but it does not yet specify holdout cases, rotating cases, mutation testing, or another mechanism that tests generalization beyond memorized fixtures.
- The central falsifier is directionally good but still needs measurable thresholds for "meaningful defects," "brittle false alarms," and disproportionate maintenance cost.

## Sources and evidence

- ideas/cross-cutting/HK-0004-maintain-an-adversarial-regression-corpus-for-agent-intake-quali/proposal.md
- ideas/cross-cutting/HK-0004-maintain-an-adversarial-regression-corpus-for-agent-intake-quali/evidence.md
- ideas/cross-cutting/HK-0004-maintain-an-adversarial-regression-corpus-for-agent-intake-quali/risks.md
- agents/evals/README.md
- https://docs.github.com/en/actions
- https://json-schema.org/

## Counterevidence and uncertainty

- A static fixture corpus may mostly catch already-known failures while missing novel failures, so passing it could create false confidence.
- Property-based tests, schema mutation tests, shadow evaluation, or periodically refreshed holdout cases may outperform or complement a fixed benchmark; the dossier has not compared these alternatives yet.
- There is no measured baseline defect rate for the current agent intake path, so expected benefit and test sensitivity cannot yet be estimated.
- The proposal may still be worthwhile even with weak external evidence because the next experiment is low-cost and reversible; the evidence gap argues for measurement, not abandonment.

## Risks and safety

- Benchmark gaming could optimize agents and prompts toward visible fixtures instead of general epistemic quality.
- A benchmark that overrepresents maintainer-defined failures could encode narrow value judgments while appearing objective.
- Sensitive-domain adversarial examples could preserve harmful or private detail if fixtures are not aggressively minimized and sanitized.
- Maintenance burden could grow faster than value if every observed failure becomes a permanent fixture without pruning criteria.
- Goodhart pressure could shift attention toward benchmark pass rates instead of real review quality.

## Recommended status

`needs-evidence`

This is a recommendation only. It does not change `idea.yaml`.

## Smallest responsible next step

Define a compact intake-failure taxonomy and three measurable benchmark outcomes: meaningful-defect detection rate, false-positive rate on known-good submissions, and detection of deliberately introduced parser/prompt regressions. Then create a minimal fixture set spanning those categories plus a small holdout set, run it against the current system and at least one seeded regression, and record whether the benchmark detects the change before expanding to a larger corpus.
