# AR-0138 — Pilot Designer review

**Idea:** HK-0055 — Pre-commit disaster cash before forecasts cross the danger threshold  
**Agent:** `chatgpt-gpt-5.6-sol`  
**Source Issue:** https://github.com/Svyable/human-kind/issues/138  
**Created:** 2026-09-04  
**Decision authority:** none  
**Human verification required:** true  
**Verification status:** unverified

> Agent-produced review requiring human verification. Decision authority is none. Its claims remain unverified until independently checked; repository merge does not establish empirical truth, change dossier lifecycle status, or authorize real-world action.

## Review summary

A public-code retrospective audit is feasible for HK-0055 in Nepal, but its evidentiary scope is narrower than “validate anticipatory cash.” OCHA’s public Nepal analysis reconstructs historical flood events and GloFAS forecasts, computes readiness/action activations, and defines TP/FP/FN across lead times and probability thresholds. That can test hydrologic trigger skill and lead-time tradeoffs. It cannot from the same public inputs establish humanitarian welfare value, distributional reach, targeting fairness, market functioning, or the comparative value of cash versus rapid post-shock support. OCHA separately documents important historical impact-data and forecast-archive gaps.

## Findings

- SOURCED — OCHA’s Nepal framework uses separate readiness and action triggers: readiness uses a 7-day GloFAS 70% exceedance probability for a 1-in-2-year discharge threshold; action combines a DHM alert with a 3-day GloFAS threshold or observed government danger level.
- SOURCED — OCHA reports a lead-time/reliability tradeoff: about 70% of relevant exceedance events at Chatara were expected to be forecast at 4–7 days, while historical Chisapani forecasts had never reached the corresponding threshold at those long lead times.
- SOURCED — The public `pa-anticipatory-action` Nepal analysis evaluates return periods 1.5/2/5 years, forecast cells corresponding to 50%/70% exceedance probability, lead times 1–7 days, and separate readiness (4–7) and action (1–3) windows; it computes TP, FP and FN against observed hazard definitions.
- INFERENCE — This is sufficient for a bounded reproducibility audit if every predeclared threshold/lead-time cell is reported rather than selecting only the best result.
- SOURCED — OCHA documents that Nepal historical water levels could identify flood events but impact severity such as people affected or houses destroyed was difficult to estimate; national historical flood forecasts were also not retained.
- INFERENCE — A hydrologic true positive is therefore a forecast/event match under a hazard definition, not evidence that cash reached the right households or improved welfare.
- INFERENCE — `trigger_skill` and `intervention_value` should be separate evidence objects. Welfare, reach, payment access, markets, acting-in-vain costs, miss harms and a rapid-post-shock comparator remain untested unless separate evidence is available.
- INFERENCE — Readiness and action stages should be scored separately because a system can have poor long-lead readiness recall but materially different short-lead action performance.

## Sources and evidence

- https://centre.humdata.org/triggering-anticipatory-action-for-floods-in-nepal/
- https://github.com/OCHA-DAP/pa-anticipatory-action/tree/develop/analyses/npl
- https://github.com/OCHA-DAP/pa-anticipatory-action/blob/develop/analyses/npl/12_historical_event_timeline.md
- https://github.com/OCHA-DAP/pa-anticipatory-action/blob/develop/analyses/npl/02_glofas_skill.md
- https://centre.humdata.org/data-requirements-for-anticipatory-action/
- https://github.com/Svyable/human-kind/blob/main/ideas/disaster-resilience/HK-0055-pre-commit-disaster-cash-before-forecasts-cross-the-danger-thres/reviews/AR-0101-skeptic.md

## Counterevidence and uncertainty

- Hazard-trigger skill is still decision-relevant even though it is not end-to-end welfare validation.
- Reproducing OCHA’s public repository may not reproduce every operational judgment or local/national input used in the live framework.
- Archived GloFAS reforecasts cannot reconstruct national forecasts that were never retained.
- River-discharge return-period and station danger-level exceedance are hazard proxies, not interchangeable humanitarian-impact measures.
- False-alarm and miss costs are asymmetric and context-dependent; no loss function is assigned here without sourced evidence.

## Risks and safety

- Post-hoc threshold or event-definition selection can manufacture apparently strong historical performance.
- Calling hazard detection “impact prediction” can hide the absence of data on who was harmed and by how much.
- Optimizing lead time, recall, or precision alone can create harmful tradeoffs.
- Beneficiary inclusion, payment access, market functioning and other distributional outcomes are outside the public hazard-replay data and remain explicitly unvalidated.
- No live threshold, fund movement, recipient list, targeting, outreach or deployment is authorized.

## Recommended status

`needs-evidence`

This is a review recommendation. The review materializer does not change `idea.yaml`; a separate evidence-gated repository change may do so.

## Smallest responsible next step

Create a repository-only reproducibility artifact pinned to a specific public OCHA commit. Predeclare the 1-in-2-year primary event threshold, existing 50%/70% forecast-probability cells, and readiness/action lead-time windows already present in source code; retain alternative hazard definitions as sensitivity analyses. Reproduce TP/FP/FN and, where definable, TN counts separately by station and trigger stage, reporting every tested cell and source/version gap. Add a `not_tested` table for welfare, targeting, payment access, markets, acting-in-vain cost, miss harm and rapid-post-shock comparator outcomes. Do not recommend an operational threshold.
