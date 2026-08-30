#!/usr/bin/env python3
"""Validate conflict-resistant idea-index fragments against landed dossiers."""

from __future__ import annotations

import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
AGGREGATE = ROOT / "data" / "idea-index.yaml"
FRAGMENTS = ROOT / "data" / "idea-index.d"
REQUIRED = {
    "id",
    "title",
    "status",
    "domains",
    "evidence_level",
    "last_reviewed",
    "path",
    "source_issue",
}


def error(message: str) -> None:
    print(f"::error::{message}")


def main() -> int:
    failures = 0
    aggregate = yaml.safe_load(AGGREGATE.read_text()) or {}
    aggregate_ids = {
        str(item.get("id", "")).strip()
        for item in aggregate.get("ideas", [])
        if isinstance(item, dict) and str(item.get("id", "")).strip()
    }
    fragment_ids: set[str] = set()

    for path in sorted(FRAGMENTS.glob("*.yaml")):
        relative = path.relative_to(ROOT)
        try:
            item = yaml.safe_load(path.read_text())
        except Exception as exc:
            error(f"{relative}: invalid YAML: {exc}")
            failures += 1
            continue

        if not isinstance(item, dict):
            error(f"{relative}: fragment must contain one mapping")
            failures += 1
            continue

        missing = sorted(REQUIRED - set(item))
        if missing:
            error(f"{relative}: missing fields: {', '.join(missing)}")
            failures += 1
            continue

        idea_id = str(item["id"]).strip()
        if path.stem != idea_id:
            error(f"{relative}: filename must match id {idea_id}")
            failures += 1
        if idea_id in aggregate_ids:
            error(f"{relative}: {idea_id} already exists in legacy aggregate")
            failures += 1
        if idea_id in fragment_ids:
            error(f"{relative}: duplicate fragment id {idea_id}")
            failures += 1
        fragment_ids.add(idea_id)

        dossier = ROOT / str(item["path"])
        metadata_path = dossier / "idea.yaml"
        if not metadata_path.is_file():
            error(f"{relative}: dossier path has no idea.yaml: {item['path']}")
            failures += 1
            continue

        metadata = yaml.safe_load(metadata_path.read_text()) or {}
        for field in ("id", "title", "status", "domains", "evidence_level", "last_reviewed"):
            if metadata.get(field) != item.get(field):
                error(f"{relative}: {field} does not match {metadata_path.relative_to(ROOT)}")
                failures += 1
        if metadata.get("source_issue") != item.get("source_issue"):
            error(f"{relative}: source_issue does not match dossier metadata")
            failures += 1

    if failures:
        print(f"Idea-index fragment validation failed with {failures} error(s).")
        return 1

    print(f"Idea-index fragment validation passed for {len(fragment_ids)} fragment(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
