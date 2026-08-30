#!/usr/bin/env python3
"""Validate the agent work queue against the aggregate + fragment idea namespace.

This compatibility wrapper keeps the existing queue validator authoritative while
supplying it a temporary merged view of the legacy aggregate index and the newer
conflict-resistant per-dossier fragments. It rejects ambiguous duplicate IDs before
running the existing validator.
"""

from __future__ import annotations

import pathlib
import tempfile

import yaml

from scripts import validate_agent_work_queue as queue_validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data/idea-index.yaml"
FRAGMENTS_DIR = ROOT / "data/idea-index.d"


def load_yaml(path: pathlib.Path):
    try:
        return yaml.safe_load(path.read_text())
    except Exception as exc:
        raise RuntimeError(f"{path.relative_to(ROOT)} could not be parsed: {exc}") from exc


def merged_index(index_path: pathlib.Path = INDEX_PATH, fragments_dir: pathlib.Path = FRAGMENTS_DIR) -> dict:
    aggregate = load_yaml(index_path)
    if not isinstance(aggregate, dict) or not isinstance(aggregate.get("ideas"), list):
        raise RuntimeError("data/idea-index.yaml must contain an ideas list")

    ideas: list[dict] = []
    seen: set[str] = set()

    for item in aggregate["ideas"]:
        if not isinstance(item, dict) or not str(item.get("id", "")).strip():
            raise RuntimeError("data/idea-index.yaml contains an invalid idea entry")
        idea_id = str(item["id"]).strip()
        if idea_id in seen:
            raise RuntimeError(f"duplicate idea id in aggregate index: {idea_id}")
        seen.add(idea_id)
        ideas.append(item)

    if fragments_dir.exists():
        for path in sorted(fragments_dir.glob("*.yaml")):
            item = load_yaml(path)
            if not isinstance(item, dict) or not str(item.get("id", "")).strip():
                raise RuntimeError(f"{path.relative_to(ROOT)} must contain one idea mapping with an id")
            idea_id = str(item["id"]).strip()
            if idea_id in seen:
                raise RuntimeError(f"duplicate idea id across aggregate/fragments: {idea_id}")
            seen.add(idea_id)
            ideas.append(item)

    return {
        "version": aggregate.get("version", 1),
        "last_generated": aggregate.get("last_generated"),
        "ideas": ideas,
    }


def main() -> int:
    try:
        index = merged_index()
    except RuntimeError as exc:
        print(f"::error::{exc}")
        return 1

    temp_path: pathlib.Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".yaml",
            prefix="idea-index-merged-",
            dir=ROOT / "data",
            delete=False,
        ) as handle:
            yaml.safe_dump(index, handle, sort_keys=False)
            temp_path = pathlib.Path(handle.name)

        queue_validator.INDEX_PATH = temp_path
        return queue_validator.main()
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
