# AR-0166 — Skeptic review

**Idea:** HK-0074 — Make essential-medicine stockout risk visible before patients lose access  
**Agent:** `chatgpt-gpt-5.6-sol`  
**Source Issue:** https://github.com/Svyable/human-kind/issues/166  
**Created:** 2026-09-07  
**Decision authority:** none  
**Human verification required:** true  
**Verification status:** unverified

> Agent-produced review requiring human verification. Decision authority is none. Its claims remain unverified until independently checked; repository merge does not establish empirical truth, change dossier lifecycle status, or authorize real-world action.

## Review summary

HK-0074 proposes making essential-medicine stockout risk visible before patients lose access. The strongest residual case is not that public shortage systems are absent—they are substantial—but that their heterogeneous states, uncertainty, missingness, and resolution histories might be represented more consistently and retrospectively validated.

The Skeptic conclusion is that current public regulatory shortage signals do **not** by themselves justify inference that a particular facility will stock out, a particular patient will lose access, or an `anticipated shortage` label is a calibrated probability. FDA explicitly distinguishes nationwide shortage determinations from usually temporary localized supply issues; Health Canada states that not all reported shortages affect patients; TGA defines shortage against projected Australian demand over a six-month horizon; and EMA notification guidance allows early reporting with limited information that may later be supplemented. A portable semantics layer may still be useful for provenance and retrospective comparison, but predictive or patient-access value remains unverified.

`human_verification_required: true`
`decision_authority: none`
`verification_status: unverified`

## Findings

- SOURCED — FDA defines drug shortage at the nationwide U.S. market level and explicitly says local pharmacy/hospital supply issues are usually temporary distribution issues; FDA checks manufacturer supply against national demand before treating a local report as evidence of national shortage risk.
- SOURCED — FDA requires manufacturers to notify interruptions likely to cause a meaningful disruption, ideally six months in advance; this is an early-warning obligation, not a published calibrated probability of a later shortage.
- SOURCED — Health Canada distinguishes anticipated shortages (manufacturer believes a shortage is likely to occur) from actual shortages and requires broad reporting; it also states that in some cases shortages are resolved without patients experiencing difficulty obtaining their drugs.
- SOURCED — Health Canada further notes that not all shortages listed on Drug Shortages Canada end up affecting patients, so report presence cannot be equated with patient-access loss.
- SOURCED — TGA defines an Australian medicine shortage using national normal/projected consumer demand over the next six months and requires reporting for specified reportable medicines. This horizon and coverage differ from FDA and Health Canada definitions.
- SOURCED — EMA guidance asks authorization holders to notify authorities as early as possible once an impending/anticipated shortage is confirmed, even when information is limited and will be supplemented later. EMA's public catalogue historically covers shortages affecting more than one Member State that have been assessed by the Agency.
- INFERENCE — Because these systems use different market scopes, product/reportability rules, reporting triggers, timelines, and resolution criteria, a shared label such as `anticipated_shortage` is not automatically comparable across jurisdictions without preserving source-native definitions.
- INFERENCE — Public report feeds alone do not expose the full denominators and independent outcome labels needed to estimate forecast precision, recall, calibration, or patient-access sensitivity/specificity. Counting reports, resolved reports, or durations is therefore not equivalent to validating warning performance.
- INFERENCE — The most defensible residual value is a provenance-preserving interoperability/validation layer that keeps source-native semantics, timestamps, missingness, and resolution history explicit. Predictive claims should remain out of scope until tested against independent outcomes.

## Sources and evidence

- FDA — Frequently Asked Questions about Drug Shortages, including nationwide-vs-localized shortage handling and advance notification requirements: https://www.fda.gov/drugs/drug-shortages/frequently-asked-questions-about-drug-shortages
- FDA — Drug Shortages, including public shortage and supply reporting context: https://www.fda.gov/drugs/drug-safety-and-availability/drug-shortages
- Health Canada — Drug shortages regulations and guidance: https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-shortages/regulations-guidance.html
- Health Canada — Drug shortages in Canada, including statement that not all listed shortages affect patients: https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-shortages.html
- TGA — Medicine shortages information for sponsors, including six-month national-demand definition: https://www.tga.gov.au/safety/shortages-and-supply-disruptions/medicine-shortages/medicine-shortages-information-sponsors
- EMA — Guidance for MAHs on detection and notification of shortages: https://www.ema.europa.eu/en/documents/regulatory-procedural-guideline/guidance-detection-and-notification-shortages-medicinal-products-marketing-authorisation-holders-mahs-union-eea_en.pdf
- EMA — Public catalogue scope description: https://www.ema.europa.eu/en/news/european-medicines-agency-launches-public-catalogue-medicine-shortages-assessed-agency
- Repository provenance — HK-0074 task Issue #161 and landed Taxonomist review AR-0095: https://github.com/Svyable/human-kind/issues/161 and https://github.com/Svyable/human-kind/pull/96

## Counterevidence and uncertainty

- Existing regulators explicitly value early reporting because it can create time to prevent or mitigate shortages. That supports the general value of early signals even though it does not establish a cross-system warning layer's incremental value.
- A national shortage can contribute to patient access problems, and Health Canada notes that shortages may cause back-orders, stock-outs, or delayed availability. The critique is against automatic inference, not against any causal connection.
- Public documentation reviewed here does not provide a complete cross-jurisdiction audit of every field, reporting exception, or historical revision, so semantic incompatibility should be tested field-by-field rather than assumed globally.
- Facility stockout and patient-access outcomes may exist in local procurement, wholesaler, pharmacy, hospital, payer, or survey data not represented in public regulator feeds. This review did not access private or sensitive inventory data.
- An `anticipated shortage` may prove empirically predictive. The unsupported step is treating the categorical label as a calibrated probability before a timestamped outcome study is performed.
- The incremental value of portable fields such as uncertainty, response state, time-to-stockout, or retrospective miss/false-alarm history is unresolved; some may improve analysis, while others may simply duplicate source-native metadata.

## Risks and safety

- INFERENCE — False-positive warnings could encourage unnecessary attention shifts, stockpiling, emergency purchasing, or clinically consequential substitution if downstream actors treat an uncalibrated signal as certain. This review does not recommend any such action.
- INFERENCE — False negatives or missing reports could create false reassurance, especially where manufacturer reporting, regulatory coverage, distribution visibility, or local inventory data are weak.
- Cross-jurisdiction normalization could erase material differences in market scope, product definitions, reportability, and resolution criteria, creating false comparability.
- A public layer must not expose confidential supplier/facility inventory, patient-level data, sensitive logistics, or inferred operational vulnerabilities.
- No procurement, substitution, supplier/facility outreach, patient targeting, or live deployment is authorized by this review.

## Recommended status

`needs-evidence`

This is a review recommendation. The review materializer does not change `idea.yaml`; a separate evidence-gated repository change may do so.

## Smallest responsible next step

Define a retrospective, repository-only validation protocol before adding predictive claims. Freeze timestamped public shortage/anticipated-shortage events with source-native semantics, then identify an independently sourced, non-sensitive outcome dataset capable of distinguishing at least national shortage realization from facility stockout or patient-access outcomes. Predeclare comparators and metrics before inspecting outcomes.

Concrete falsifier/stop conditions: if no lawful non-sensitive independent outcome source can support the claimed level of inference; if portable fields cannot be mapped without erasing source-native definitions; or if a predeclared retrospective benchmark shows no incremental discrimination, calibration, useful lead time, or decision-relevant information over existing source-native signals, narrow the proposal to provenance/interoperability or stop the warning-layer claim.
