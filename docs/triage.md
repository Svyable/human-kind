# Triage

Triage is the first substantive review phase after an idea dossier enters `intake`. It is a **decision-support process**, not a separate value in `idea.yaml`.

The purpose of triage is to decide what kind of work, if any, should happen next while preserving uncertainty and avoiding premature promotion.

## Inputs

A triage decision should consider:

- the complete dossier;
- existing solutions and likely duplicates;
- the quality and relevance of cited evidence;
- the causal mechanism and falsification condition;
- material safety, misuse, equity, and legitimacy concerns;
- at least one review that meaningfully challenges the proposal when feasible;
- whether an accountable human owner or appropriate reviewer exists for the next stage.

Agent reviews may inform triage, but they do not constitute a triage decision.

## Questions

1. Is the problem bounded enough to investigate?
2. Is the proposal meaningfully distinct from existing work?
3. Are the central factual claims supported enough to justify more effort?
4. Is the mechanism coherent and falsifiable?
5. Are there blocking safety, legal, legitimacy, or dual-use concerns?
6. Who is missing from the review process?
7. What is the smallest responsible next learning action?
8. What evidence would change the disposition?

## Typical dispositions

Triage usually results in one of these status recommendations:

- `needs-scope` — the problem, population, mechanism, or intervention is too broad.
- `needs-evidence` — important claims are insufficiently supported or prior work is missing.
- `researching` — the dossier is scoped enough for active literature, landscape, or stakeholder research.
- `not-pursuing` — current evidence, duplication, risk, legitimacy, or tractability does not justify further work.
- `intake` — retain at intake when the review itself is incomplete or contradictory.

Moving directly from `intake` to a later design or pilot status should be exceptional and supported by unusually mature pre-existing evidence plus appropriate human/domain review.

## Reviews versus decisions

Structured reviews live under:

```text
ideas/<domain>/<dossier>/reviews/
```

A review may recommend a status and next action. It must preserve its provenance and uncertainty. **A review never changes lifecycle status by itself.**

A status change requires a Pull Request that updates `idea.yaml`, explains the evidence and review basis, and receives accountable human review. Sensitive domains require proportionate expert or affected-community input.

## Minimum triage record

When changing status after triage, the Pull Request should state:

- prior status;
- new status;
- reviews considered;
- evidence added or rejected;
- unresolved disagreements;
- blocking concerns;
- smallest responsible next action;
- accountable human reviewer.

The reasoning should also be summarized in the dossier's `updates.md` so future contributors can reconstruct why the status changed.
