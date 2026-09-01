# AR-0095 — Taxonomist review

**Idea:** HK-0074 — Make essential-medicine stockout risk visible before patients lose access  
**Agent:** `chatgpt-gpt-5.6-sol`  
**Source Issue:** https://github.com/Svyable/human-kind/issues/95  
**Created:** 2026-09-01  
**Decision authority:** none

> Agent-produced review. Human verification is required before this review influences lifecycle promotion or consequential action.

## Review summary

HK-0074 proposes making essential-medicine stockout risk visible before patients lose access. This bounded crosswalk finds substantial prior art in public regulatory shortage systems, especially for distinguishing anticipated versus actual shortages, tracking current/resolved states, reasons and mitigation information, and—in the EU—machine-to-machine shortage-reporting interoperability. That overlap weakens any case for a new standalone shortage dashboard or reporting platform. The residual question is narrower: whether existing public systems expose a portable, non-sensitive semantic layer for uncertainty/data-missingness, expected time-to-stockout, response-state history, and retrospective false-alarm/miss validation. The reviewed public documentation does not establish that those residual semantics are consistently available across systems. Recommendation is therefore `needs-scope` for human consideration only, not a lifecycle change.

## Findings

- SOURCED — WHO's 2017 technical consultation treats shortage/stockout notification as an established systems problem across supply- and demand-side causes, with patient harm possible from higher costs, poorer outcomes, inappropriate substitution, and falsified-product risk. This is strong prior art against treating shortage notification itself as novel.
- SOURCED — FDA maintains a public Drug Shortages Database covering current and resolved shortages and discontinuations; FDA states the list is updated daily with new/resolved shortages and additional supplier-capacity information. Resolved shortages remain visible for six months and discontinued shortages for one year.
- SOURCED — EMA's public shortage catalogue reports shortage reason, current status (ongoing/resolved), extent, and information for patients and healthcare professionals. The European Shortages Monitoring Platform (ESMP) additionally collects supply, demand, and availability data and supports machine-to-machine interoperability with national-authority and industry systems.
- SOURCED — Health Canada requires reporting of both anticipated and actual prescription-drug shortages. Its public system can be searched for actual and anticipated shortages and discontinuations. Canada defines an actual shortage as current supply unable to meet demand and an anticipated shortage as future supply that may not meet projected demand; manufacturers should not wait for complete stock-out before reporting.
- SOURCED — Australia's TGA Medicine Shortages Reports Database publicly distinguishes current, anticipated, resolved shortages and discontinuations, includes management-action information, and offers a downloadable extract.
- INFERENCE — `anticipated shortage`, `actual/current shortage`, `resolved`, `discontinued`, reason/cause, and basic mitigation/management state should be classified as **already covered or substantially covered** by mature public systems, not distinctive HK-0074 features.
- INFERENCE — Interoperable reporting is **already covered in a meaningful regional implementation** by EMA ESMP's machine-to-machine interface. A new platform would need to demonstrate a material cross-system interoperability gap rather than merely restating this capability.
- INFERENCE — Publicly documented support for `expected_time_to_stockout`, explicit confidence/uncertainty grades, low-data/missingness state, false-alarm/miss semantics, and retrospective validation appears **partial, unclear, or meaningfully absent** in this bounded review. This is a candidate residual gap, not an established one.
- INFERENCE — Facility-level stock-on-hand, supplier-confidential quantities, and fine-grained vulnerability data should not be presumed appropriate for a public commons even if useful operationally; the safest candidate contribution is a public semantic crosswalk/profile, not collection of sensitive inventory data.

## Sources and evidence

- https://www.who.int/publications/i/item/WHO-EMP-IAU-2017.15
- https://www.fda.gov/drugs/drug-shortage-staff
- https://www.fda.gov/drugs/drug-safety-and-availability
- https://esmp.ema.europa.eu/
- https://open.canada.ca/data/en/dataset/f6198ae6-ed66-4de5-b03f-7c347d8e850e
- https://open.canada.ca/data/en/dataset/653f1530-b182-42e5-9953-5061ea521cf0
- https://open.canada.ca/data/en/dataset/cad7007c-6352-480c-a3c5-8a176fe773b5
- https://apps.tga.gov.au/shortages/search/Index
- https://github.com/Svyable/human-kind/issues/83

## Counterevidence and uncertainty

- This is a documentation crosswalk, not an exhaustive audit of every field, API schema, national implementation, wholesaler system, hospital inventory platform, or procurement dataset. A semantic marked unclear may exist in technical documentation not retrieved here.
- Regulatory shortage systems operate at different scopes and granularity. A national drug-shortage report is not equivalent to facility-level stock-on-hand or patient access, so overlap at the reporting layer does not prove equivalent operational capability.
- EMA ESMP has richer regulator/industry reporting than what is necessarily public in the shortage catalogue; this review does not infer that every ESMP field is publicly accessible.
- Anticipated-shortage states encode some uncertainty but do not by themselves establish calibrated probability, confidence, or forecast-error semantics.
- TGA management actions and EMA patient/professional information demonstrate mitigation-state coverage, but this review does not establish a common interoperable response-state vocabulary across jurisdictions.
- A cross-system schema could create false comparability if definitions of shortage, market scope, product identifiers, reporting obligations, and resolution differ materially across jurisdictions.
- No claim here establishes that a public warning layer improves patient outcomes, predicts facility stockouts, or outperforms existing local supply-chain practice.

## Risks and safety

- Publishing granular facility, supplier, stock-on-hand, lead-time, or vulnerability information could expose commercially sensitive or security-sensitive supply conditions and should not be treated as a default openness goal.
- A cross-jurisdiction warning score could imply precision that the underlying definitions and reporting obligations do not support.
- False alarms can induce hoarding or inefficient procurement; misses can create false reassurance. This review does not recommend operational thresholds.
- Public mitigation information must not be converted by an agent into clinically consequential substitution advice.
- A new dashboard could duplicate regulator infrastructure, fragment identifiers, and create stale or conflicting shortage signals.

## Recommended status

`needs-scope`

This is a recommendation only. It does not change `idea.yaml`.

## Smallest responsible next step

For human consideration, do not build a new shortage-reporting platform. Draft a small, non-authoritative **cross-system interoperability profile** using only public or synthetic data and only the residual semantics that remain unresolved after human verification: `signal_state` (anticipated / actual / resolved / discontinued), `evidence_timestamp`, `data_missingness_state`, `time_to_stockout_semantics` (reported / inferred / absent), `response_state`, `resolution_timestamp`, and optional retrospective `false_alarm` / `miss` / `latency` annotations. Map those fields to FDA, EMA/ESMP, Health Canada, and TGA public semantics. Drop any field already adequately represented. Do not collect facility inventories, supplier-confidential data, patient data, recommend substitutions or purchases, contact external organizations, or deploy a warning system.
