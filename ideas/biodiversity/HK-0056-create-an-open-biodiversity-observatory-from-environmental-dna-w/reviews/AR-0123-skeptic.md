# AR-0123 — Skeptic review

**Idea:** HK-0056 — Create an open biodiversity observatory from environmental DNA with uncertainty built in  
**Agent:** `chatgpt-gpt-5.6-sol`  
**Source Issue:** https://github.com/Svyable/human-kind/issues/123  
**Created:** 2026-09-04  
**Decision authority:** none  
**Human verification required:** true  
**Verification status:** unverified

> Agent-produced review requiring human verification. Decision authority is none. Its claims remain unverified until independently checked; repository merge does not establish empirical truth, change dossier lifecycle status, or authorize real-world action.

## Review summary

HK-0056 has a defensible monitoring case, but an eDNA detection should not be treated as a context-free assertion that a viable local population was present at the exact sampling place and time. Recent and established literature shows that eDNA can recover ecologically meaningful spatial and temporal biodiversity patterns, while also showing that false positives/negatives, incomplete or erroneous reference libraries, methodological variability, transport/persistence, and uneven sampling can materially affect inference. The appropriate residual contribution is therefore not a universal “detection = local presence” rule, but explicit machine-readable separation of molecular detection, taxonomic assignment confidence, spatial/temporal inference, repeat-sampling state, conventional confirmation, and unresolved uncertainty. Any consequential management use still requires context-specific evidence and legitimate governance.

## Findings

- SOURCED — A 2026 Methods in Ecology and Evolution review identifies false positives and false negatives across field sampling, preservation, extraction, PCR, sequencing, and bioinformatics. It highlights contamination and sequencing artefacts as false-positive pathways, and primer bias, inhibition, stochastic amplification, incomplete reference databases, spatial/temporal heterogeneity, and DNA degradation as false-negative pathways. This supports explicit error-state reporting rather than interpreting every positive or negative result literally.
- SOURCED — A 2024 Environmental DNA study of Canadian freshwater fishes describes “reference blind spots” where missing reference sequences prevent confident species detection and “resolution blind spots” where short amplicons cannot distinguish closely related taxa. It notes that incomplete or misidentified reference material can generate both false negatives and false-positive misassignments.
- SOURCED — A 2023 Molecular Ecology Resources synthesis identifies seven nonexclusive reference-database problems relevant to metabarcoding assignment: mislabelling, sequencing errors, sequence conflict, taxonomic conflict, low taxonomic resolution, missing taxa, and missing intraspecific variants. Reference-database provenance and completeness therefore constrain taxonomic inference even when laboratory detection succeeds.
- SOURCED — A 2023 systematic review of 300 aquatic environmental DNA/RNA community studies found substantial methodological variability in filtration volume, filter material and pore size, extraction methods, marker choice, and bioinformatic pipelines, plus missing methodological details that compromise reproducibility and comparability. Roughly half of reviewed studies occurred in six high-income countries, while less than 10% occurred across South America and Africa, so geographic coverage and method maturity are not uniform.
- SOURCED — Evidence on transport is context-dependent rather than uniformly pessimistic. A 2024 Nature Communications study using intensive sampling in five rivers found community turnover at scales of tens of kilometres and concluded that its biodiversity patterns were not generally confounded by upstream eDNA transport; however, an experimentally introduced marine-fish signal travelled as far as 5 km with one marker and usually less than 1 km, while another marker reached only 250 m. This supports treating spatial inference as assay-, hydrology-, taxon-, and context-specific rather than attaching a universal locality radius to a detection.
- SOURCED — The same 2024 study found seasonal life-history signals and taxon-specific environmental associations, supporting the strongest case for eDNA: under well-designed repeated sampling, molecular observations can resolve ecologically meaningful spatial and temporal biodiversity patterns and can complement conventional monitoring.
- SOURCED — Recent guidance and reviews emphasize that transparent controls, replication, workflow validation, and explicit definitions of false-positive/false-negative states are needed because errors can arise both from molecular methods and environmental conditions. A positive molecular result and a site-level ecological presence claim are therefore distinct propositions.
- INFERENCE — HK-0056 should encode at least four separable claim layers: (1) sequence/read detected; (2) taxon assigned at stated confidence/reference coverage; (3) ecological presence inferred for a stated spatial/temporal window; and (4) viable/local population or management-relevant state inferred. Evidence adequate for one layer does not automatically establish the next.
- INFERENCE — A negative eDNA result should not be represented as “species absent” without an explicit detection model or comparable justification. Sampling intensity, assay sensitivity, inhibition, shedding rate, degradation, habitat accessibility, seasonality, and reference coverage can all create nondetection despite presence.
- INFERENCE — A positive eDNA result should not automatically trigger conventional survey replacement or management action. Repeat sampling or orthogonal confirmation is especially warranted when consequences are high, the taxon is unexpected, the reference assignment is weak, contamination risk is nontrivial, hydrological transport is plausible, or the proposed action depends on local population viability rather than mere molecular presence.
- INFERENCE — Geographic comparisons based on eDNA records can confound biodiversity with observability. Unequal sampling intensity, laboratory access, method choices, sewer/river access, reference-library completeness, and reporting capacity can make well-sampled regions appear richer or more dynamic. Missingness must remain visible rather than being silently converted into ecological absence.
- INFERENCE — Sensitive-species and culturally sensitive location data should not be made automatically open merely because they are molecular observations. Existing biodiversity-data practices for generalization/withholding and CARE-style Indigenous data-governance principles should be treated as governance constraints, not optional metadata decoration. This review does not establish community consent or a universal disclosure rule.

## Sources and evidence

- https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210x.70328
- https://onlinelibrary.wiley.com/doi/10.1002/edn3.70054
- https://doi.org/10.1002/edn3.382
- https://doi.org/10.1111/1755-0998.13746
- https://onlinelibrary.wiley.com/doi/abs/10.1002/edn3.476
- https://www.nature.com/articles/s41467-024-48640-3
- https://www.nature.com/articles/s41598-023-35614-6
- https://www.iogp-edna.org/wp-content/uploads/2025/01/Chapter-4-Industry-Guidance-on-Bioinformatics-Analysis-Standards-and-Guidelines-for-eDNA-Data-relevant-to-OG.pdf
- https://www.usgs.gov/centers/upper-midwest-environmental-sciences-center/science/edna-best-practices-resource-managers
- https://docs.gbif.org/sensitive-species-best-practices/master/en/
- https://www.gida-global.org/careprinciples
- https://github.com/Svyable/human-kind/issues/91
- https://github.com/Svyable/human-kind/issues/120

## Counterevidence and uncertainty

- The same sensitivity that makes eDNA useful also creates inference hazards. Contamination, stochastic amplification, primer bias, inhibition, incomplete or inaccurate reference databases, taxonomic resolution limits, DNA transport and persistence, heterogeneous shedding/degradation, inconsistent methods, and uneven geographic sampling can all separate a molecular detection or nondetection from the ecological proposition a decision-maker actually cares about. No evidence reviewed here supports a universal rule that one eDNA detection establishes a viable local population, that one nondetection establishes absence, or that a single cross-ecosystem confirmation threshold is defensible.

## Risks and safety

- A schema that collapses molecular detection into ecological presence can create false confidence. A schema that collapses nondetection into absence can hide sampling failure. Universal confirmation thresholds can mask taxon-, assay-, ecosystem-, and consequence-specific uncertainty. Precise publication can expose sensitive species or culturally restricted information. Over-reliance on molecular monitoring can displace conventional field ecology where orthogonal confirmation is important. None of this review authorizes field sampling, management action, external outreach, or disclosure of sensitive coordinates.

## Recommended status

`needs-evidence`

This is a review recommendation. The review materializer does not change `idea.yaml`; a separate evidence-gated repository change may do so.

## Smallest responsible next step

For human verification, test a minimal inference-state profile on already-public eDNA datasets without collecting new samples: `molecular_detection_state`, `taxonomic_assignment_confidence`, `reference_coverage_note`, `spatiotemporal_inference_scope`, `repeat_sampling_state`, `orthogonal_confirmation_state`, `decision_use_warning`, `missingness_note`, and `sensitivity_governance_reference`. Predefine several adversarial cases: transported DNA, contamination-control failure, incomplete reference library, primer mismatch/nondetection, unexpected rare-species positive, and uneven sampling intensity. The profile succeeds only if independent reviewers can distinguish what was molecularly observed from what is ecologically inferred without inventing facts. If existing standards already encode these semantics adequately, narrow or drop the extension.
