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


def test_review_submitted_is_non_recruiting_and_preserves_stricter_bounds() -> None:
    assert "review-submitted" in queue_validator.STATUSES
    assert "review-submitted" not in queue_validator.ACTIVE_STATUSES

    valid = {
        "entrypoint": "https://github.com/Svyable/human-kind/issues/123",
        "task_issue": "https://github.com/Svyable/human-kind/issues/120",
        "review_submission": "https://github.com/Svyable/human-kind/issues/123",
        "human_verification_required": True,
        "decision_authority": "none",
    }
    assert queue_validator.review_submitted_violations(valid) == []

    widened = dict(valid, decision_authority="repository-scoped")
    violations = queue_validator.review_submitted_violations(widened)
    assert any("decision_authority must be 'none'" in item for item in violations)

    missing_submission = dict(valid)
    missing_submission.pop("review_submission")
    violations = queue_validator.review_submitted_violations(missing_submission)
    assert any("review_submission" in item for item in violations)


def test_open_issue_supports_normal_and_stricter_authority_lanes() -> None:
    normal = {
        "entrypoint": "https://github.com/Svyable/human-kind/issues/137",
        "task_issue": "https://github.com/Svyable/human-kind/issues/137",
        "independent_verification_required": True,
        "decision_authority": "repository-scoped",
    }
    assert queue_validator.open_issue_violations(normal) == []

    stricter = dict(
        normal,
        human_verification_required=True,
        decision_authority="none",
    )
    assert queue_validator.open_issue_violations(stricter) == []

    widened = dict(stricter, decision_authority="repository-scoped")
    violations = queue_validator.open_issue_violations(widened)
    assert any("decision_authority must be 'none'" in item for item in violations)

    missing_task = dict(stricter)
    missing_task.pop("task_issue")
    violations = queue_validator.open_issue_violations(missing_task)
    assert any("task_issue" in item for item in violations)

    invalid_entrypoint = dict(stricter, entrypoint="https://example.com/issues/137")
    violations = queue_validator.open_issue_violations(invalid_entrypoint)
    assert any("entrypoint" in item for item in violations)


def test_review_pr_open_supports_normal_and_stricter_authority_lanes() -> None:
    normal = {
        "entrypoint": "https://github.com/Svyable/human-kind/pull/128",
        "task_issue": "https://github.com/Svyable/human-kind/issues/120",
        "review_submission": "https://github.com/Svyable/human-kind/issues/123",
        "independent_verification_required": True,
        "decision_authority": "repository-scoped",
    }
    assert queue_validator.review_pr_open_violations(normal) == []

    stricter = dict(
        normal,
        human_verification_required=True,
        decision_authority="none",
    )
    assert queue_validator.review_pr_open_violations(stricter) == []

    widened = dict(stricter, decision_authority="repository-scoped")
    violations = queue_validator.review_pr_open_violations(widened)
    assert any("decision_authority must be 'none'" in item for item in violations)

    missing_verification = dict(stricter, independent_verification_required=False)
    violations = queue_validator.review_pr_open_violations(missing_verification)
    assert any("independent_verification_required" in item for item in violations)


def main() -> int:
    test_fragment_only_idea_is_visible()
    test_aggregate_fragment_duplicate_is_rejected()
    test_combined_role_slug_remains_unsupported()
    test_review_submitted_is_non_recruiting_and_preserves_stricter_bounds()
    test_open_issue_supports_normal_and_stricter_authority_lanes()
    test_review_pr_open_supports_normal_and_stricter_authority_lanes()
    print("Fragment-aware agent work queue regression tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
