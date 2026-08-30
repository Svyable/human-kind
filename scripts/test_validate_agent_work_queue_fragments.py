#!/usr/bin/env python3
"""Focused regression tests for fragment-aware work-queue validation."""

from __future__ import annotations

import pathlib
import tempfile

import yaml

import validate_agent_work_queue as queue_validator
import validate_agent_work_queue_fragments as compat


def write_yaml(path: pathlib.Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False))


def test_fragment_only_idea_is_visible() -> None:
    with tempfile.TemporaryDirectory(dir=compat.ROOT) as raw:
        root = pathlib.Path(raw)
        aggregate = root / "idea-index.yaml"
        fragments = root / "idea-index.d"
        write_yaml(
            aggregate,
            {"version": 1, "ideas": [{"id": "HK-0001", "path": "ideas/a"}]},
        )
        write_yaml(
            fragments / "HK-0056.yaml",
            {"id": "HK-0056", "path": "ideas/biodiversity/HK-0056"},
        )
        merged = compat.merged_index(aggregate, fragments)
        by_id = {item["id"]: item for item in merged["ideas"]}
        assert by_id["HK-0056"]["path"] == "ideas/biodiversity/HK-0056"
        assert "HK-9999" not in by_id


def test_aggregate_fragment_duplicate_is_rejected() -> None:
    with tempfile.TemporaryDirectory(dir=compat.ROOT) as raw:
        root = pathlib.Path(raw)
        aggregate = root / "idea-index.yaml"
        fragments = root / "idea-index.d"
        write_yaml(
            aggregate,
            {"version": 1, "ideas": [{"id": "HK-0056", "path": "ideas/a"}]},
        )
        write_yaml(
            fragments / "HK-0056.yaml",
            {"id": "HK-0056", "path": "ideas/b"},
        )
        try:
            compat.merged_index(aggregate, fragments)
        except RuntimeError as exc:
            assert "duplicate idea id across aggregate/fragments" in str(exc)
        else:
            raise AssertionError("aggregate/fragment duplicate should fail")


def test_combined_role_slug_remains_unsupported() -> None:
    assert "taxonomist" in queue_validator.ROLES
    assert "synthesizer" in queue_validator.ROLES
    assert "taxonomist-synthesizer" not in queue_validator.ROLES


def main() -> int:
    test_fragment_only_idea_is_visible()
    test_aggregate_fragment_duplicate_is_rejected()
    test_combined_role_slug_remains_unsupported()
    print("Fragment-aware agent work queue regression tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
