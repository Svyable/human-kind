#!/usr/bin/env python3
"""Validate Human Kind dossier metadata and repository-local Markdown links."""

from __future__ import annotations

import datetime as dt
import json
import pathlib
import re
import sys
from collections import defaultdict

import jsonschema
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
IDEAS = ROOT / "ideas"
SCHEMA = json.loads((ROOT / "agents/schemas/idea.schema.json").read_text())
TEMPLATE = (IDEAS / "_template").resolve()
STALE_DAYS = 180


def warning(message: str) -> None:
    print(f"::warning::{message}")


def error(message: str) -> None:
    print(f"::error::{message}")


def validate_dossiers() -> int:
    failures = 0
    titles: dict[str, list[pathlib.Path]] = defaultdict(list)
    ids: dict[str, list[pathlib.Path]] = defaultdict(list)
    today = dt.date.today()

    for path in sorted(IDEAS.rglob("idea.yaml")):
        if TEMPLATE in path.resolve().parents:
            continue
        try:
            data = yaml.safe_load(path.read_text())
            jsonschema.Draft202012Validator(SCHEMA, format_checker=jsonschema.FormatChecker()).validate(data)
        except Exception as exc:
            error(f"{path.relative_to(ROOT)}: schema validation failed: {exc}")
            failures += 1
            continue

        title = str(data["title"]).strip().casefold()
        titles[title].append(path)
        ids[str(data["id"]).strip().casefold()].append(path)

        reviewed = dt.date.fromisoformat(str(data["last_reviewed"]))
        age = (today - reviewed).days
        if age > STALE_DAYS:
            warning(f"{path.relative_to(ROOT)}: last_reviewed is {age} days old (>{STALE_DAYS})")

        folder = path.parent
        for required in ("proposal.md", "evidence.md", "risks.md", "updates.md"):
            if not (folder / required).exists():
                error(f"{folder.relative_to(ROOT)}: missing {required}")
                failures += 1

    for normalized, paths in titles.items():
        if len(paths) > 1:
            error("Duplicate dossier title: " + ", ".join(str(p.relative_to(ROOT)) for p in paths))
            failures += 1
    for normalized, paths in ids.items():
        if len(paths) > 1:
            error("Duplicate dossier id: " + ", ".join(str(p.relative_to(ROOT)) for p in paths))
            failures += 1

    return failures


LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def validate_local_links() -> int:
    failures = 0
    for md in ROOT.rglob("*.md"):
        if ".git" in md.parts:
            continue
        text = md.read_text(errors="replace")
        for target in LINK.findall(text):
            target = target.strip().split()[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            raw = target.split("#", 1)[0]
            if not raw:
                continue
            candidate = (md.parent / raw).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                error(f"{md.relative_to(ROOT)}: local link escapes repository: {target}")
                failures += 1
                continue
            if not candidate.exists():
                error(f"{md.relative_to(ROOT)}: broken local link: {target}")
                failures += 1
    return failures


def main() -> int:
    failures = validate_dossiers() + validate_local_links()
    if failures:
        print(f"Validation failed with {failures} error(s).")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
