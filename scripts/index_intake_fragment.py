#!/usr/bin/env python3
"""Write one conflict-resistant idea-index fragment from a materialized intake.

The intake materializer still updates data/idea-index.yaml in its local working tree for
backward-compatible harness behavior, but workflow commits should stage only the dossier
and this per-idea fragment. This keeps concurrent intake PRs off the shared aggregate.
"""

from __future__ import annotations

import os
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "idea-index.yaml"
FRAGMENTS = ROOT / "data" / "idea-index.d"


def die(message: str) -> "None":
    print(f"::error::{message}")
    raise SystemExit(2)


def main() -> int:
    issue_number = os.environ.get("ISSUE_NUMBER", "").strip()
    if not issue_number.isdigit():
        die("ISSUE_NUMBER must be numeric")

    idea_id = f"HK-{int(issue_number):04d}"
    index = yaml.safe_load(INDEX.read_text()) or {}
    ideas = index.get("ideas")
    if not isinstance(ideas, list):
        die("data/idea-index.yaml must contain an ideas list")

    matches = [entry for entry in ideas if isinstance(entry, dict) and entry.get("id") == idea_id]
    if len(matches) != 1:
        die(f"expected exactly one materialized index entry for {idea_id}; found {len(matches)}")

    FRAGMENTS.mkdir(parents=True, exist_ok=True)
    path = FRAGMENTS / f"{idea_id}.yaml"
    path.write_text(yaml.safe_dump(matches[0], sort_keys=False, allow_unicode=True))
    print(f"Wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
