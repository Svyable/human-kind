#!/usr/bin/env python3
"""Materialize a structured trusted-agent review Issue into a dossier review artifact."""

from __future__ import annotations

import datetime as dt
import os
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
IDEAS = ROOT / "ideas"

ROLE_MAP = {
    "Scout": "scout",
    "Skeptic": "skeptic",
    "Synthesizer": "synthesizer",
    "Taxonomist": "taxonomist",
    "Pilot designer": "pilot-designer",
    "Red team": "red-team",
}
STATUSES = {
    "intake", "needs-evidence", "needs-scope", "researching", "designed",
    "pilot-ready", "piloting", "validated", "not-pursuing", "archived",
}
REQUIRED = [
    "Idea ID", "Agent identifier", "Agent role", "Review summary", "Findings",
    "Sources and evidence", "Counterevidence and uncertainty", "Risks and safety",
    "Recommended status", "Smallest responsible next step", "Agent attestation",
]


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def parse_sections(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in body.splitlines():
        match = re.match(r"^###\s+(.+?)\s*$", line)
        if match:
            current = match.group(1)
            sections.setdefault(current, [])
        elif current is not None:
            sections[current].append(line)
    return {key: "\n".join(lines).strip() for key, lines in sections.items()}


def list_items(text: str) -> list[str]:
    items: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        line = re.sub(r"^[-*]\s+", "", line)
        line = re.sub(r"^\d+[.)]\s+", "", line)
        if line:
            items.append(line)
    return items


def find_dossier(idea_id: str) -> tuple[pathlib.Path, dict]:
    matches: list[tuple[pathlib.Path, dict]] = []
    for path in IDEAS.glob("*/*/idea.yaml"):
        data = yaml.safe_load(path.read_text())
        if isinstance(data, dict) and str(data.get("id", "")).strip() == idea_id:
            matches.append((path.parent, data))
    if not matches:
        fail(f"No dossier found for {idea_id}.")
    if len(matches) > 1:
        fail(f"Multiple dossiers found for {idea_id}; repository invariants are broken.")
    return matches[0]


def submission_bounds(body: str) -> tuple[str, bool]:
    """Preserve explicit stricter authority/verification declarations from the source Issue."""
    authority = "repository-scoped"
    if re.search(r"(?i)`?decision_authority`?\s*:\s*`?none`?", body):
        authority = "none"
    human_verification_required = bool(
        re.search(r"(?i)`?human_verification_required`?\s*:\s*`?true`?", body)
    )
    return authority, human_verification_required


def main() -> int:
    issue_number = os.environ.get("ISSUE_NUMBER", "").strip()
    issue_body = os.environ.get("ISSUE_BODY", "")
    issue_url = os.environ.get("ISSUE_URL", "").strip()
    issue_updated_at = os.environ.get("ISSUE_UPDATED_AT", "").strip()

    if not issue_number.isdigit():
        fail("ISSUE_NUMBER must be numeric.")
    if not issue_url.startswith("https://github.com/"):
        fail("ISSUE_URL must be a GitHub URL.")

    sections = parse_sections(issue_body)
    missing = [heading for heading in REQUIRED if not sections.get(heading)]
    if missing:
        fail("Missing required section(s): " + ", ".join(missing))

    idea_id = sections["Idea ID"].strip().upper()
    if not re.fullmatch(r"HK-\d{4,}", idea_id):
        fail("Idea ID must match HK-0000 or a longer numeric identifier.")

    role_label = sections["Agent role"].strip()
    role = ROLE_MAP.get(role_label)
    if role is None:
        fail(f"Unsupported agent role: {role_label!r}")

    reviewer_id = sections["Agent identifier"].strip()
    if len(reviewer_id) < 2:
        fail("Agent identifier is too short.")

    recommended_status = sections["Recommended status"].strip()
    if recommended_status not in STATUSES:
        fail(f"Unsupported recommended status: {recommended_status!r}")

    findings = list_items(sections["Findings"])
    sources = list_items(sections["Sources and evidence"])
    uncertainties = list_items(sections["Counterevidence and uncertainty"])
    risks = list_items(sections["Risks and safety"])
    if not all((findings, sources, uncertainties, risks)):
        fail("Findings, sources, uncertainties, and risks must each contain at least one item.")

    attestation = sections["Agent attestation"]
    if len(re.findall(r"(?im)^\s*-\s*\[[xX]\]", attestation)) < 3:
        fail("All three agent attestation checkboxes must be checked.")

    dossier_dir, idea = find_dossier(idea_id)
    review_id = f"AR-{int(issue_number):04d}"
    date_text = issue_updated_at[:10] if re.match(r"^\d{4}-\d{2}-\d{2}", issue_updated_at) else dt.date.today().isoformat()
    dt.date.fromisoformat(date_text)
    decision_authority, human_verification_required = submission_bounds(issue_body)

    review = {
        "review_id": review_id,
        "idea_id": idea_id,
        "role": role,
        "reviewer_id": reviewer_id,
        "source_issue": issue_url,
        "created_at": date_text,
        "summary": sections["Review summary"].strip(),
        "findings": findings,
        "sources": sources,
        "uncertainties": uncertainties,
        "risks": risks,
        "recommended_status": recommended_status,
        "next_action": sections["Smallest responsible next step"].strip(),
        "generated_by": "agent",
        "review_requirement": "independent",
        "verification_status": "unverified",
        "claims_requiring_verification": True,
        "source_links_required": True,
        "decision_authority": decision_authority,
    }
    if human_verification_required:
        review["human_verification_required"] = True

    reviews_dir = dossier_dir / "reviews"
    reviews_dir.mkdir(exist_ok=True)
    yaml_path = reviews_dir / f"{review_id}-{role}.yaml"
    md_path = reviews_dir / f"{review_id}-{role}.md"
    yaml_path.write_text(yaml.safe_dump(review, sort_keys=False, allow_unicode=True))

    def bullets(values: list[str]) -> str:
        return "\n".join(f"- {item}" for item in values)

    if decision_authority == "none":
        authority_note = (
            "> Agent-produced review requiring human verification. Decision authority is none. "
            "Its claims remain unverified until independently checked; repository merge does not "
            "establish empirical truth, change dossier lifecycle status, or authorize real-world action."
        )
    else:
        authority_note = (
            "> Agent-produced review. Repository-scoped authority permits autonomous bounded repository "
            "decisions and eligible exact-head merge. Its claims remain unverified until independently "
            "checked; repository merge does not authorize consequential real-world action."
        )
    human_line = "**Human verification required:** true  \n" if human_verification_required else ""

    md = f"""# {review_id} — {role.replace('-', ' ').title()} review

**Idea:** {idea_id} — {idea.get('title', '')}  
**Agent:** `{reviewer_id}`  
**Source Issue:** {issue_url}  
**Created:** {date_text}  
**Decision authority:** {decision_authority}  
{human_line}**Verification status:** unverified

{authority_note}

## Review summary

{review['summary']}

## Findings

{bullets(findings)}

## Sources and evidence

{bullets(sources)}

## Counterevidence and uncertainty

{bullets(uncertainties)}

## Risks and safety

{bullets(risks)}

## Recommended status

`{recommended_status}`

This is a review recommendation. The review materializer does not change `idea.yaml`; a separate evidence-gated repository change may do so.

## Smallest responsible next step

{review['next_action']}
"""
    md_path.write_text(md)
    print(f"Materialized {review_id} for {idea_id} at {yaml_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
