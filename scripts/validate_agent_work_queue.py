#!/usr/bin/env python3
"""Validate the machine-readable agent work queue against repository state.

The queue is repository coordination and task-selection metadata, not a real-world
priority ranking. Agents have repository-scoped authority over bounded queue,
coordination, and evidence-gated repository lifecycle decisions. Structural violations
fail CI. Historical completed/blocked records may retain older human-verification or
no-authority disclosures as provenance.
"""

from __future__ import annotations

import datetime as dt
import pathlib
import re
import sys
from collections import defaultdict

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "agents/work-queue.yaml"
INDEX_PATH = ROOT / "data/idea-index.yaml"
IDEAS = ROOT / "ideas"

ROLES = {"scout", "skeptic", "synthesizer", "taxonomist", "pilot-designer", "red-team"}
STATUSES = {
    "available",
    "open-issue",
    "claimed",
    "review-submitted",
    "review-pr-open",
    "completed",
    "blocked",
}
ACTIVE_STATUSES = {"available", "open-issue", "claimed", "review-pr-open"}
ISSUE_URL = re.compile(r"^https://github\.com/Svyable/human-kind/issues/[0-9]+$")
PR_URL = re.compile(r"^https://github\.com/Svyable/human-kind/pull/[0-9]+$")
SELECTION_EXCEPTIONS = {
    "new-repository-activity",
    "materially-new-evidence",
    "ci-or-safety-regression",
    "explicit-task-dependency",
}
REPOSITORY_AUTHORITY = "repository-scoped"


def error(message: str) -> None:
    print(f"::error::{message}")


def warning(message: str) -> None:
    print(f"::warning::{message}")


def load_yaml(path: pathlib.Path):
    try:
        return yaml.safe_load(path.read_text())
    except Exception as exc:
        raise RuntimeError(f"{path.relative_to(ROOT)} could not be parsed: {exc}") from exc


def review_roles_present_in_checkout() -> dict[str, set[str]]:
    roles: dict[str, set[str]] = defaultdict(set)
    for path in IDEAS.glob("*/*/reviews/*.yaml"):
        try:
            data = load_yaml(path)
        except RuntimeError as exc:
            warning(str(exc))
            continue
        if isinstance(data, dict):
            idea_id = str(data.get("idea_id", "")).strip()
            role = str(data.get("role", "")).strip()
            if idea_id and role:
                roles[idea_id].add(role)
    return roles


def review_submitted_violations(item: dict) -> list[str]:
    """Return structural violations for a submitted/materialized review with no PR yet."""
    violations: list[str] = []
    if not ISSUE_URL.fullmatch(str(item.get("entrypoint", "")).strip()):
        violations.append("entrypoint must be a Human Kind Issue URL when status=review-submitted")
    if not ISSUE_URL.fullmatch(str(item.get("task_issue", "")).strip()):
        violations.append("task_issue must be a Human Kind Issue URL when status=review-submitted")
    if not ISSUE_URL.fullmatch(str(item.get("review_submission", "")).strip()):
        violations.append("review_submission must be a Human Kind Issue URL when status=review-submitted")

    authority = item.get("decision_authority")
    if authority not in (None, "none", REPOSITORY_AUTHORITY):
        violations.append(
            "decision_authority must be omitted, 'none', or 'repository-scoped' when status=review-submitted"
        )
    if item.get("human_verification_required") is True and authority != "none":
        violations.append(
            "decision_authority must be 'none' when status=review-submitted and human_verification_required=true"
        )
    return violations


def review_pr_open_violations(item: dict) -> list[str]:
    """Return structural violations for an open review PR, preserving stricter provenance."""
    violations: list[str] = []
    if not PR_URL.fullmatch(str(item.get("entrypoint", "")).strip()):
        violations.append("entrypoint must be a Human Kind PR URL when status=review-pr-open")
    if not ISSUE_URL.fullmatch(str(item.get("task_issue", "")).strip()):
        violations.append("task_issue must be a Human Kind Issue URL when status=review-pr-open")
    if not ISSUE_URL.fullmatch(str(item.get("review_submission", "")).strip()):
        violations.append("review_submission must be a Human Kind Issue URL when status=review-pr-open")
    if item.get("independent_verification_required") is not True:
        violations.append("independent_verification_required must be true when status=review-pr-open")

    authority = item.get("decision_authority")
    if item.get("human_verification_required") is True:
        if authority != "none":
            violations.append(
                "decision_authority must be 'none' when status=review-pr-open and human_verification_required=true"
            )
    elif authority != REPOSITORY_AUTHORITY:
        violations.append(
            f"decision_authority must be {REPOSITORY_AUTHORITY!r} when status=review-pr-open"
        )
    return violations


def main() -> int:
    failures = 0

    if not QUEUE_PATH.exists():
        error("agents/work-queue.yaml is missing")
        return 1

    try:
        queue = load_yaml(QUEUE_PATH)
        index = load_yaml(INDEX_PATH)
    except RuntimeError as exc:
        error(str(exc))
        return 1

    if not isinstance(queue, dict):
        error("agents/work-queue.yaml must contain a mapping")
        return 1

    if queue.get("schema_version") != 2:
        error("work queue schema_version must be 2")
        failures += 1
    if queue.get("kind") != "human-kind-agent-work-queue":
        error("work queue kind must be human-kind-agent-work-queue")
        failures += 1

    updated = str(queue.get("updated", "")).strip()
    try:
        dt.date.fromisoformat(updated)
    except ValueError:
        error("work queue updated must be an ISO date")
        failures += 1

    policy = queue.get("policy")
    expected_policy = {
        "ordering": "unranked",
        "lifecycle_mutation": "evidence-gated",
        "decision_authority": REPOSITORY_AUTHORITY,
        "independent_verification_required": True,
    }
    if not isinstance(policy, dict):
        error("work queue policy must be a mapping")
        failures += 1
        policy = {}
    for key, expected in expected_policy.items():
        if policy.get(key) != expected:
            error(f"work queue policy.{key} must be {expected!r}")
            failures += 1

    selection = queue.get("selection")
    if not isinstance(selection, dict):
        error("work queue selection must be a mapping")
        failures += 1
        selection = {}
    if selection.get("strategy") != "breadth-before-depth":
        error("work queue selection.strategy must be 'breadth-before-depth'")
        failures += 1
    max_cycles = selection.get("default_max_consecutive_cycles_per_dossier")
    if not isinstance(max_cycles, int) or not 1 <= max_cycles <= 4:
        error("work queue selection.default_max_consecutive_cycles_per_dossier must be an integer from 1 to 4")
        failures += 1
    exceptions = selection.get("exceptions")
    if not isinstance(exceptions, list) or set(exceptions) != SELECTION_EXCEPTIONS:
        error("work queue selection.exceptions must contain the four documented override conditions")
        failures += 1
    if selection.get("decision_authority") != REPOSITORY_AUTHORITY:
        error(f"work queue selection.decision_authority must be {REPOSITORY_AUTHORITY!r}")
        failures += 1
    if selection.get("independent_verification_required") is not True:
        error("work queue selection.independent_verification_required must be true")
        failures += 1

    coordination = queue.get("coordination")
    if not isinstance(coordination, dict):
        error("work queue coordination must be a mapping")
        failures += 1
        coordination = {}
    if coordination.get("decision_authority") != REPOSITORY_AUTHORITY:
        error(f"work queue coordination.decision_authority must be {REPOSITORY_AUTHORITY!r}")
        failures += 1
    if coordination.get("independent_verification_required") is not True:
        error("work queue coordination.independent_verification_required must be true")
        failures += 1

    seed_corpus = selection.get("seed_corpus")
    if not isinstance(seed_corpus, dict):
        error("work queue selection.seed_corpus must be a mapping")
        failures += 1
        seed_corpus = {}
    min_dossiers = seed_corpus.get("minimum_indexed_dossiers")
    min_domains = seed_corpus.get("minimum_distinct_domains")
    if not isinstance(min_dossiers, int) or min_dossiers < 2:
        error("work queue selection.seed_corpus.minimum_indexed_dossiers must be at least 2")
        failures += 1
    if not isinstance(min_domains, int) or min_domains < 2:
        error("work queue selection.seed_corpus.minimum_distinct_domains must be at least 2")
        failures += 1
    if seed_corpus.get("when_below_floor") != "surface-bounded-intake-candidate":
        error("work queue selection.seed_corpus.when_below_floor must be 'surface-bounded-intake-candidate'")
        failures += 1

    indexed: dict[str, dict] = {}
    if not isinstance(index, dict) or not isinstance(index.get("ideas"), list):
        error("data/idea-index.yaml must contain an ideas list")
        return failures + 1
    for item in index["ideas"]:
        if isinstance(item, dict) and item.get("id"):
            indexed[str(item["id"])] = item

    work = queue.get("work")
    if not isinstance(work, list):
        error("work queue work must be a list")
        return failures + 1

    seen_ids: set[str] = set()
    seen_role_targets: set[tuple[str, str]] = set()
    reviews_present = review_roles_present_in_checkout()
    active_targets: set[str] = set()

    for offset, item in enumerate(work, start=1):
        prefix = f"work[{offset}]"
        if not isinstance(item, dict):
            error(f"{prefix} must be a mapping")
            failures += 1
            continue

        work_id = str(item.get("id", "")).strip()
        if not work_id:
            error(f"{prefix}.id is required")
            failures += 1
        elif work_id in seen_ids:
            error(f"duplicate work queue id: {work_id}")
            failures += 1
        else:
            seen_ids.add(work_id)

        role = str(item.get("role", "")).strip()
        if role not in ROLES:
            error(f"{prefix}.role has unsupported value {role!r}")
            failures += 1

        status = str(item.get("status", "")).strip()
        if status not in STATUSES:
            error(f"{prefix}.status has unsupported value {status!r}")
            failures += 1

        idea_id = str(item.get("target_idea", "")).strip()
        index_item = indexed.get(idea_id)
        if index_item is None:
            error(f"{prefix}.target_idea {idea_id!r} is not in data/idea-index.yaml")
            failures += 1
        else:
            expected_path = str(index_item.get("path", "")).strip()
            actual_path = str(item.get("target_path", "")).strip()
            if actual_path != expected_path:
                error(
                    f"{prefix}.target_path must match idea-index path for {idea_id}: {expected_path!r}"
                )
                failures += 1
            dossier = ROOT / actual_path
            if not dossier.is_dir() or not (dossier / "idea.yaml").exists():
                error(f"{prefix}.target_path does not resolve to a dossier: {actual_path}")
                failures += 1

        role_target = (idea_id, role)
        if idea_id and role:
            if role_target in seen_role_targets:
                error(f"duplicate queue role for target: {idea_id} / {role}")
                failures += 1
            else:
                seen_role_targets.add(role_target)

        if item.get("contribution_type") != "structured-review":
            error(f"{prefix}.contribution_type must be 'structured-review'")
            failures += 1

        objective = str(item.get("objective", "")).strip()
        if len(objective) < 20:
            error(f"{prefix}.objective must be at least 20 characters")
            failures += 1

        signals = item.get("completion_signals")
        if not isinstance(signals, list) or len(signals) < 2 or any(
            not isinstance(signal, str) or len(signal.strip()) < 5 for signal in signals or []
        ):
            error(f"{prefix}.completion_signals must contain at least two substantive strings")
            failures += 1

        entrypoint = str(item.get("entrypoint", "")).strip()
        if not entrypoint.startswith("https://"):
            error(f"{prefix}.entrypoint must be an https URL")
            failures += 1
        if status == "open-issue" and not ISSUE_URL.fullmatch(entrypoint):
            error(f"{prefix}.entrypoint must be a Human Kind Issue URL when status=open-issue")
            failures += 1
        if status == "review-submitted":
            for violation in review_submitted_violations(item):
                error(f"{prefix}.{violation}")
                failures += 1
        if status == "review-pr-open":
            for violation in review_pr_open_violations(item):
                error(f"{prefix}.{violation}")
                failures += 1

        strict_human_review_pr = (
            status == "review-pr-open"
            and item.get("human_verification_required") is True
            and item.get("decision_authority") == "none"
        )
        if (
            status in ACTIVE_STATUSES
            and not strict_human_review_pr
            and item.get("decision_authority") not in (None, REPOSITORY_AUTHORITY)
        ):
            error(
                f"{prefix}.decision_authority must be omitted or {REPOSITORY_AUTHORITY!r} for active work"
            )
            failures += 1
        if (
            status in ACTIVE_STATUSES
            and not strict_human_review_pr
            and item.get("human_verification_required") is True
        ):
            error(
                f"{prefix}.human_verification_required is a legacy field and must not be used for active autonomous work"
            )
            failures += 1
        if status in ACTIVE_STATUSES and item.get("independent_verification_required") is not True:
            error(f"{prefix}.independent_verification_required must be true for active work")
            failures += 1

        if status in ACTIVE_STATUSES and idea_id:
            active_targets.add(idea_id)

        if status in ACTIVE_STATUSES and role in reviews_present.get(idea_id, set()):
            warning(
                f"{prefix} is still {status!r}, but a {role} review is present in the current checkout for {idea_id}; reconcile the queue if that review is already merged"
            )

        if status == "completed" and role not in reviews_present.get(idea_id, set()):
            warning(
                f"{prefix} is marked completed, but no {role} review was found in the current checkout for {idea_id}"
            )

    indexed_domains = {
        domain
        for item in indexed.values()
        for domain in item.get("domains", [])
        if isinstance(domain, str) and domain.strip()
    }
    if isinstance(min_dossiers, int) and isinstance(min_domains, int):
        if len(indexed) < min_dossiers or len(indexed_domains) < min_domains:
            warning(
                "Seed corpus is below the breadth floor "
                f"({len(indexed)}/{min_dossiers} dossiers, {len(indexed_domains)}/{min_domains} domains). "
                "Prefer a bounded, sourced intake candidate over another unprompted deepening cycle unless a documented selection exception applies."
            )
        elif len(active_targets) == 1 and len(indexed) > 1:
            warning(
                "All active work-queue items target one dossier despite a broader indexed corpus; check the breadth-before-depth selection policy."
            )

    if failures:
        print(f"Agent work queue validation failed with {failures} error(s).")
        return 1

    print(f"Agent work queue validation passed for {len(work)} item(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
