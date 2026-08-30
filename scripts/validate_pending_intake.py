#!/usr/bin/env python3
"""Validate pending intake coordination metadata against the live idea index.

Pending intake entries advertise dossier candidates that have not landed on main yet.
They must not be mistaken for indexed/review-ready ideas, and stale entries should
fail CI once the corresponding dossier appears in the idea index.
"""

from __future__ import annotations

import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "agents/work-queue.yaml"
INDEX_PATH = ROOT / "data/idea-index.yaml"
ISSUE_URL = re.compile(r"^https://github\.com/Svyable/human-kind/issues/[0-9]+$")
PR_URL = re.compile(r"^https://github\.com/Svyable/human-kind/pull/[0-9]+$")
IDEA_ID = re.compile(r"^HK-[0-9]{4}$")


def error(message: str) -> None:
    print(f"::error::{message}")


def load_yaml(path: pathlib.Path):
    try:
        return yaml.safe_load(path.read_text())
    except Exception as exc:
        raise RuntimeError(f"{path.relative_to(ROOT)} could not be parsed: {exc}") from exc


def main() -> int:
    failures = 0
    try:
        queue = load_yaml(QUEUE_PATH)
        index = load_yaml(INDEX_PATH)
    except RuntimeError as exc:
        error(str(exc))
        return 1

    if not isinstance(queue, dict):
        error("agents/work-queue.yaml must contain a mapping")
        return 1
    if not isinstance(index, dict) or not isinstance(index.get("ideas"), list):
        error("data/idea-index.yaml must contain an ideas list")
        return 1

    indexed = {
        str(item.get("id", "")).strip()
        for item in index["ideas"]
        if isinstance(item, dict) and str(item.get("id", "")).strip()
    }

    pending = queue.get("pending_intake", [])
    if not isinstance(pending, list):
        error("work queue pending_intake must be a list")
        return 1

    seen_ids: set[str] = set()
    seen_issues: set[str] = set()
    seen_prs: set[str] = set()

    for offset, item in enumerate(pending, start=1):
        prefix = f"pending_intake[{offset}]"
        if not isinstance(item, dict):
            error(f"{prefix} must be a mapping")
            failures += 1
            continue

        idea_id = str(item.get("id", "")).strip()
        if not IDEA_ID.fullmatch(idea_id):
            error(f"{prefix}.id must match HK-####")
            failures += 1
        elif idea_id in seen_ids:
            error(f"duplicate pending intake id: {idea_id}")
            failures += 1
        else:
            seen_ids.add(idea_id)

        if idea_id in indexed:
            error(
                f"{prefix}.id {idea_id} is already indexed; remove the stale pending intake entry"
            )
            failures += 1

        if item.get("status") != "pending-pr":
            error(f"{prefix}.status must be 'pending-pr'")
            failures += 1

        domain = str(item.get("domain", "")).strip()
        if not domain:
            error(f"{prefix}.domain is required")
            failures += 1

        source_issue = str(item.get("source_issue", "")).strip()
        if not ISSUE_URL.fullmatch(source_issue):
            error(f"{prefix}.source_issue must be a Human Kind Issue URL")
            failures += 1
        elif source_issue in seen_issues:
            error(f"duplicate pending intake source_issue: {source_issue}")
            failures += 1
        else:
            seen_issues.add(source_issue)

        entrypoint = str(item.get("entrypoint", "")).strip()
        if not PR_URL.fullmatch(entrypoint):
            error(f"{prefix}.entrypoint must be a Human Kind pull-request URL")
            failures += 1
        elif entrypoint in seen_prs:
            error(f"duplicate pending intake entrypoint: {entrypoint}")
            failures += 1
        else:
            seen_prs.add(entrypoint)

        if item.get("downstream_review_available") is not False:
            error(f"{prefix}.downstream_review_available must be false")
            failures += 1
        if item.get("human_verification_required") is not True:
            error(f"{prefix}.human_verification_required must be true")
            failures += 1
        if item.get("decision_authority") != "none":
            error(f"{prefix}.decision_authority must be 'none'")
            failures += 1

        notes = str(item.get("notes", "")).strip()
        if len(notes) < 20:
            error(f"{prefix}.notes must explain the pending/non-review-ready boundary")
            failures += 1

    if failures:
        print(f"Pending intake validation failed with {failures} error(s).")
        return 1

    print(f"Pending intake validation passed for {len(pending)} item(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
