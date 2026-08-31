# AR-0091 — Taxonomist review

**Idea:** HK-0056 — Create an open biodiversity observatory from environmental DNA with uncertainty built in  
**Agent:** `chatgpt-gpt-5.6-sol`  
**Source Issue:** https://github.com/Svyable/human-kind/issues/91  
**Created:** 2026-08-31  
**Decision authority:** none

> Agent-produced review. Human verification is required before this review influences lifecycle promotion or consequential action.

## Review summary

HK-0056 proposes an open eDNA biodiversity observatory with provenance, uncertainty, confirmation rules, sensitive-location controls, and governance. The reviewed public infrastructure already covers a large share of the proposed technical metadata and interoperability surface: USGS best practices require field metadata, negative controls, decontamination, and replicates; GBIF's Metabarcoding Data Toolkit maps metabarcoding datasets into standardized publication terms; the 2025 FAIRe checklist extends existing MIxS/Darwin Core/DNA-derived-data terms across the eDNA workflow; and OBIS is now publishing eDNA datasets through Darwin Core Event Core with linked DNA-derived observations and environmental measurements. GBIF also has explicit mechanisms for generalizing or withholding sensitive occurrence information. These overlaps weaken the case for a new standalone database. The more plausible residual contribution, if human reviewers find it useful, is a small interoperability/governance profile around decision-use semantics, confirmation state, and explicit linkage of FAIR publication practices with sensitive-location and Indigenous data-governance requirements.

## Findings

- SOURCED — USGS Resource Manager's eDNA Toolbox recommends negative controls at each process phase, decontamination protocols, multiple site samples/replicates, immediate preservation, clear sample identification, and collection of metadata for every eDNA sample. USGS also cautions that eDNA should contribute to a weight of evidence and complement rather than replace traditional surveys.
- SOURCED — The 2024 MIEM reporting guidelines describe minimum reporting across the metabarcoding workflow and emphasize FAIR documentation so results can be reproduced, synthesized, and evaluated for management use.
- SOURCED — GBIF's current Metabarcoding Data Programme and Toolkit provide standardized templates that map metabarcoding data to common terms and support export/publication through GBIF infrastructure. This is substantial overlap with HK-0056's proposed interoperable publication layer.
- SOURCED — The 2025 FAIRe metadata checklist contains 337 terms spanning collection, PCR, bioinformatics, targeted assays, metabarcoding, taxonomic-assignment metrics, contamination/non-target screening, and environmental variables. It explicitly reuses MIxS, Darwin Core, and the DNA-derived-data extension where possible and proposes additional eDNA-specific terms where gaps remain.
- SOURCED — In July 2026 OBIS reported its first eDNA dataset published using Darwin Core Event Core, connecting sampling events, DNA-derived occurrences, environmental measurements, and broader ocean-observing metadata. OBIS also describes ongoing work to improve DNA-derived biodiversity publication through these standards.
- SOURCED — GBIF sensitive-species guidance supports multiple levels of coordinate generalization or complete withholding, and recommends documenting generalization/withholding rather than silently publishing precise sensitive locations.
- SOURCED — The CARE Principles for Indigenous Data Governance explicitly complement FAIR by adding Collective Benefit, Authority to Control, Responsibility, and Ethics; GIDA warns that open-data practice alone can ignore power differentials and Indigenous rights and interests.
- INFERENCE — Sampling-event provenance, assay/workflow provenance, contamination controls, standardized identifiers, publication/export structures, and significant portions of taxonomic-assignment metadata should be classified as **already covered** or **substantially covered**, not as distinctive HK-0056 features.
- INFERENCE — Sensitive-location handling is **substantially covered as a general biodiversity-data capability** through GBIF guidance, although project-specific rules for deciding sensitivity and access still require legitimate local governance rather than an agent-designed universal rule.
- INFERENCE — Indigenous/community data governance is **not responsibly reducible to a database field**. CARE supplies a governance framework, but this review does not establish that current eDNA infrastructures operationalize locally applicable Indigenous authority or consent requirements. Treat this area as **partially covered / unclear**, and do not infer consent.
- INFERENCE — A potentially distinct, testable HK-0056 contribution remains in explicit decision-use semantics: representing whether an eDNA observation is suitable only for monitoring, warrants repeat sampling, has conventional-survey confirmation, or is insufficient for a consequential management inference. The reviewed sources support caution and metadata richness but do not establish one universal cross-platform confirmation/decision-state model.

## Sources and evidence

- https://www.usgs.gov/centers/upper-midwest-environmental-sciences-center/science/edna-best-practices-resource-managers
- https://www.usgs.gov/centers/upper-midwest-environmental-sciences-center/science/resource-managers-edna-toolbox
- https://www.usgs.gov/publications/miem-guidelines-minimum-information-reporting-environmental-metabarcoding-data
- https://mdt.gbif.org/
- https://www.usgs.gov/publications/a-metadata-checklist-and-data-formatting-guidelines-make-edna-fair-findable-accessible
- https://portal.obis.org/2026/07/06/edna-event-core/
- https://portal.obis.org/2026/07/10/edna-workshop/
- https://docs.gbif.org/sensitive-species-best-practices/master/en/
- https://docs.gbif.org/guide-publishing-survey-data/en/
- https://www.gida-global.org/careprinciples
- https://github.com/Svyable/human-kind/issues/75

## Counterevidence and uncertainty

- The reviewed standards and tools are evolving, especially GBIF/OBIS DNA-data infrastructure. A feature classified here as unclear may already exist in documentation or implementations not retrieved in this bounded review.
- Metadata standards do not establish that data producers actually populate fields consistently or that downstream users interpret them consistently; nominal interoperability can therefore overstate practical comparability.
- USGS guidance cited here is oriented toward resource-manager practice and does not establish universal confirmation thresholds across taxa, environments, assays, or management decisions.
- FAIRe is a recent community guideline intended to evolve and integrate with existing standards; its breadth is evidence against inventing another metadata schema, but not evidence that every governance or decision-use problem is solved.
- GBIF sensitive-data guidance addresses biodiversity occurrence disclosure generally. It does not establish that one global sensitivity rule is appropriate for every species, jurisdiction, Indigenous nation, or community.
- CARE principles are governance principles, not evidence that any particular eDNA platform has obtained legitimate Indigenous authorization. This review did not contact communities and does not infer stakeholder preferences, consent, or governance acceptance.
- The OBIS Event Core implementation is recent; one demonstrated dataset and current workshops show technical direction, not universal maturity or adoption.

## Risks and safety

- A new standalone observatory could duplicate fast-moving public infrastructure, fragment standards, and increase reporting burden.
- Publishing fine-grained eDNA occurrence information can expose rare, threatened, culturally sensitive, or exploitable species and locations; openness must not override legitimate restrictions.
- Treating DNA detection as confirmed local population presence can produce false confidence and inappropriate downstream management conclusions.
- Universal confirmation thresholds could hide assay-, taxon-, environment-, and decision-specific uncertainty.
- FAIR interoperability without CARE-style governance can privilege reuse over Indigenous rights, authority, and collective interests.
- An agent-authored governance schema must not be mistaken for community consent or legitimate authority.

## Recommended status

`needs-scope`

This is a recommendation only. It does not change `idea.yaml`.

## Smallest responsible next step

Do not build a new eDNA database or observatory. For human consideration, draft a **small, non-authoritative interoperability profile** layered on existing Darwin Core / DNA-derived-data / FAIRe infrastructure with only the residual fields that remain materially unresolved after human verification. Start with: `evidence_use_state` (detection-only / repeat-sampling-needed / conventionally-confirmed / unresolved), `confirmation_relation` (link to confirmatory observation where one exists), `decision_use_warning`, `sensitivity_governance_reference`, and explicit provenance for any generalization/withholding. Test the profile only against already-public example datasets from GBIF/OBIS/USGS. If those systems already represent these semantics adequately, narrow or drop the extension rather than inventing differentiation. Do not collect samples, expose sensitive locations, infer Indigenous/community consent, contact communities or agencies, or trigger conservation action.
