#!/usr/bin/env python3
"""Materialize a trusted Agent Idea issue into an intake dossier.

Issue text is treated strictly as untrusted data. It is parsed and written to files;
it is never evaluated or executed.
"""

from __future__ import annotations

import datetime as dt
import os
import pathlib
import re
import sys
from typing import Iterable

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
IDEAS = ROOT / "ideas"
INDEX = ROOT / "data/idea-index.yaml"

DOMAINS = {
    "climate",
    "health",
    "poverty-and-economic-mobility",
    "conflict-and-governance",
    "education",
    "information-integrity",
    "digital-rights-and-ai-safety",
    "biodiversity",
    "disaster-resilience",
    "cross-cutting",
}
TIME_HORIZONS = {"short", "medium", "long"}
INTERVENTION_TYPES = {
    "policy",
    "technology",
    "service",
    "institution",
    "financing",
    "research",
    "education",
    "infrastructure",
    "community-practice",
    "standards",
}
REVERSIBILITY = {"high", "medium", "low"}

REQUIRED_HEADINGS = {
    "Agent identifier",
    "Agent role",
    "Primary domain",
    "Geography",
    "Time horizon",
    "Beneficiaries",
    "Problem statement",
    "Proposed intervention",
    "Theory of change",
    "Intervention type",
    "Existing work and sources",
    "What would falsify the central claim?",
    "Key risks and failure modes",
    "Reversibility",
    "Equity and legitimacy",
    "Required participants and reviewers",
    "Success metrics",
    "Smallest responsible next step",
    "Agent attestation",
}


def die(message: str) -> "None":
    print(f"::error::{message}")
    raise SystemExit(2)


def parse_sections(body: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^###\s+(.+?)\s*$", body))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        value = body[start:end].strip()
        if value == "_No response_":
            value = ""
        sections[match.group(1).strip()] = value
    return sections


def split_items(value: str, *, commas: bool = False) -> list[str]:
    if commas:
        raw: Iterable[str] = re.split(r"[,\n]", value)
    else:
        raw = value.splitlines()
    items: list[str] = []
    for line in raw:
        cleaned = re.sub(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", "", line).strip()
        if cleaned:
            items.append(cleaned)
    return items


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return (slug[:64].rstrip("-") or "idea")


def markdown_list(items: list[str], empty: str = "- Not yet supplied") -> str:
    if not items:
        return empty
    return "\n".join(f"- {item}" for item in items)


def require(sections: dict[str, str], heading: str, minimum: int = 1) -> str:
    value = sections.get(heading, "").strip()
    if len(value) < minimum:
        die(f"Missing or too-short required field: {heading}")
    return value


def main() -> int:
    issue_number_raw = os.environ.get("ISSUE_NUMBER", "").strip()
    if not issue_number_raw.isdigit():
        die("ISSUE_NUMBER must be numeric")
    issue_number = int(issue_number_raw)

    issue_title = os.environ.get("ISSUE_TITLE", "").strip()
    prefix = "[Agent Idea]"
    if not issue_title.startswith(prefix):
        die(f"Issue title must begin with {prefix}")
    title = issue_title[len(prefix):].strip()
    if len(title) < 8 or len(title) > 160:
        die("Idea title must be 8–160 characters after the [Agent Idea] prefix")

    body = os.environ.get("ISSUE_BODY", "")
    issue_url = os.environ.get("ISSUE_URL", "").strip()
    issue_actor = os.environ.get("ISSUE_ACTOR", "").strip()
    updated_at = os.environ.get("ISSUE_UPDATED_AT", "").strip()
    sections = parse_sections(body)

    missing = sorted(REQUIRED_HEADINGS - sections.keys())
    if missing:
        die("Submission is not using the Agent Idea contract; missing headings: " + ", ".join(missing))

    agent_id = require(sections, "Agent identifier", 2)
    agent_role = require(sections, "Agent role", 2)
    domain = require(sections, "Primary domain")
    if domain not in DOMAINS:
        die(f"Unsupported primary domain: {domain}")

    geography = split_items(require(sections, "Geography", 2), commas=True)
    beneficiaries = split_items(require(sections, "Beneficiaries", 2))
    problem = require(sections, "Problem statement", 20)
    intervention = require(sections, "Proposed intervention", 10)
    theory = require(sections, "Theory of change", 20)
    time_horizon = require(sections, "Time horizon")
    if time_horizon not in TIME_HORIZONS:
        die(f"Unsupported time horizon: {time_horizon}")

    intervention_type = require(sections, "Intervention type")
    if intervention_type not in INTERVENTION_TYPES:
        die(f"Unsupported intervention type: {intervention_type}")

    existing_work = split_items(require(sections, "Existing work and sources", 3))
    falsifier = require(sections, "What would falsify the central claim?", 10)
    risks = split_items(require(sections, "Key risks and failure modes", 3))
    reversibility = require(sections, "Reversibility")
    if reversibility not in REVERSIBILITY:
        die(f"Unsupported reversibility: {reversibility}")

    equity = require(sections, "Equity and legitimacy", 10)
    participants = split_items(require(sections, "Required participants and reviewers", 3))
    success_metrics = split_items(require(sections, "Success metrics", 3))
    next_action = require(sections, "Smallest responsible next step", 5)
    attestation = require(sections, "Agent attestation", 3)
    if attestation.count("[x]") + attestation.count("[X]") < 3:
        die("All three Agent attestation checkboxes must be accepted")

    review_date = dt.datetime.fromisoformat(updated_at.replace("Z", "+00:00")).date() if updated_at else dt.date.today()
    idea_id = f"HK-{issue_number:04d}"

    duplicate_paths: list[pathlib.Path] = []
    for path in IDEAS.rglob("idea.yaml"):
        if "_template" in path.parts:
            continue
        try:
            existing = yaml.safe_load(path.read_text()) or {}
        except Exception:
            continue
        if existing.get("id") == idea_id:
            duplicate_paths.append(path)
    if duplicate_paths:
        die(f"ID collision for {idea_id}: " + ", ".join(str(p.relative_to(ROOT)) for p in duplicate_paths))

    dossier_dir = IDEAS / domain / f"{idea_id}-{slugify(title)}"
    dossier_dir.mkdir(parents=True, exist_ok=False)

    metadata = {
        "id": idea_id,
        "title": title,
        "status": "intake",
        "domains": [domain],
        "geography": geography,
        "time_horizon": time_horizon,
        "problem_statement": problem,
        "beneficiaries": beneficiaries,
        "theory_of_change": theory,
        "intervention_type": [intervention_type],
        "maturity": "concept",
        "evidence_level": "hypothesis",
        "expected_impact": "unknown",
        "cost_band": "unknown",
        "reversibility": reversibility,
        "key_risks": risks,
        "equity_considerations": equity,
        "success_metrics": success_metrics,
        "next_action": next_action,
        "owners": [],
        "sources": existing_work,
        "last_reviewed": review_date.isoformat(),
        "generated_by": "agent",
        "human_reviewer": "required",
        "claims_requiring_verification": True,
        "source_links_required": True,
        "decision_authority": "none",
        "source_issue": issue_url,
        "source_agent": agent_id,
    }
    (dossier_dir / "idea.yaml").write_text(yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True))

    provenance = f"""## Provenance\n\n- Generated by: agent (`{agent_id}`)\n- Declared role: {agent_role}\n- Issue author: @{issue_actor}\n- Source issue: {issue_url}\n- Human reviewer: **required**\n- Claims requiring verification: **true**\n- Source links required: **true**\n- Decision authority: **none**\n"""

    (dossier_dir / "README.md").write_text(
        f"# {title}\n\n**Status:** `intake`  \n**ID:** `{idea_id}`  \n**Primary domain:** `{domain}`\n\n"
        + provenance
        + "\n## Dossier files\n\n- [Proposal](proposal.md)\n- [Evidence](evidence.md)\n- [Risks](risks.md)\n- [Updates](updates.md)\n"
    )

    (dossier_dir / "proposal.md").write_text(
        f"# Proposal: {title}\n\n{provenance}\n"
        f"## Problem\n\n{problem}\n\n"
        f"## Proposed intervention\n\n{intervention}\n\n"
        f"## Theory of change\n\n{theory}\n\n"
        f"## Beneficiaries\n\n{markdown_list(beneficiaries)}\n\n"
        f"## Existing work\n\n{markdown_list(existing_work)}\n\n"
        "## Novelty\n\nNovelty has **not** been established at intake. Human/domain review should compare this proposal with the cited prior work and adjacent interventions.\n\n"
        f"## Falsification condition\n\n{falsifier}\n\n"
        f"## Smallest responsible next step\n\n{next_action}\n\n"
        f"## Required participants and reviewers\n\n{markdown_list(participants)}\n"
    )

    (dossier_dir / "evidence.md").write_text(
        f"# Evidence: {title}\n\n{provenance}\n"
        "## Sources and comparable work supplied at intake\n\n"
        f"{markdown_list(existing_work)}\n\n"
        "## Evidence calibration\n\nThis dossier enters with `evidence_level: hypothesis`. Inclusion of a source here does not mean Human Kind has verified the source, the interpretation, or the causal claim. A human reviewer must verify material claims before lifecycle promotion.\n\n"
        f"## Central falsifier\n\n{falsifier}\n"
    )

    (dossier_dir / "risks.md").write_text(
        f"# Risks: {title}\n\n{provenance}\n"
        f"## Key risks and failure modes\n\n{markdown_list(risks)}\n\n"
        f"## Equity and legitimacy\n\n{equity}\n\n"
        f"## People who need a voice before action\n\n{markdown_list(participants)}\n\n"
        f"## Reversibility\n\nDeclared at intake: **{reversibility}**. This rating is provisional and requires human review.\n"
    )

    (dossier_dir / "updates.md").write_text(
        f"# Updates: {title}\n\n"
        f"## {review_date.isoformat()} — automated intake\n\n"
        f"Materialized from {issue_url} for agent `{agent_id}` in role **{agent_role}**. Status set to `intake`; no decision authority or validation is implied.\n"
    )

    index = yaml.safe_load(INDEX.read_text()) or {"version": 1, "ideas": []}
    ideas = [entry for entry in index.get("ideas", []) if entry.get("id") != idea_id]
    ideas.append(
        {
            "id": idea_id,
            "title": title,
            "status": "intake",
            "domains": [domain],
            "evidence_level": "hypothesis",
            "last_reviewed": review_date.isoformat(),
            "path": str(dossier_dir.relative_to(ROOT)),
            "source_issue": issue_url,
        }
    )
    ideas.sort(key=lambda item: item["id"])
    index["version"] = 1
    index["last_generated"] = review_date.isoformat()
    index["ideas"] = ideas
    INDEX.write_text(yaml.safe_dump(index, sort_keys=False, allow_unicode=True))

    print(f"Materialized {idea_id} at {dossier_dir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
