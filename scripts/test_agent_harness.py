#!/usr/bin/env python3
"""Regression tests for Human Kind's agent intake and review materializers."""

from __future__ import annotations

import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "agents" / "evals" / "fixtures"
IDEA_SCRIPT = ROOT / "scripts" / "agent_issue_to_dossier.py"
REVIEW_SCRIPT = ROOT / "scripts" / "agent_review_to_artifact.py"


def _section_pattern(heading: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^###[ \t]+{re.escape(heading)}[ \t]*\n.*?(?=^###[ \t]+|\Z)"
    )


def replace_section(body: str, heading: str, value: str) -> str:
    replacement = f"### {heading}\n\n{value.strip()}\n\n"
    updated, count = _section_pattern(heading).subn(replacement, body, count=1)
    if count != 1:
        raise AssertionError(f"Could not replace section: {heading}")
    return updated.rstrip() + "\n"


def remove_section(body: str, heading: str) -> str:
    updated, count = _section_pattern(heading).subn("", body, count=1)
    if count != 1:
        raise AssertionError(f"Could not remove section: {heading}")
    return updated.rstrip() + "\n"


class AgentHarnessTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        (self.root / "scripts").mkdir()
        (self.root / "ideas").mkdir()
        (self.root / "data").mkdir()
        shutil.copy2(IDEA_SCRIPT, self.root / "scripts" / IDEA_SCRIPT.name)
        shutil.copy2(REVIEW_SCRIPT, self.root / "scripts" / REVIEW_SCRIPT.name)
        (self.root / "data" / "idea-index.yaml").write_text(
            "version: 1\nlast_generated: null\nideas: []\n"
        )
        self.idea_body = (FIXTURES / "agent-idea-valid.md").read_text()
        self.review_body = (FIXTURES / "agent-review-valid.md").read_text()
        self.seed_dossier()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def seed_dossier(self) -> pathlib.Path:
        dossier = self.root / "ideas" / "cross-cutting" / "HK-0004-harness-test"
        dossier.mkdir(parents=True)
        (dossier / "idea.yaml").write_text(
            yaml.safe_dump(
                {
                    "id": "HK-0004",
                    "title": "Harness seed dossier for review tests",
                    "status": "intake",
                },
                sort_keys=False,
            )
        )
        return dossier

    def run_script(
        self,
        script_name: str,
        *,
        issue_number: int,
        body: str,
        title: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env.update(
            {
                "ISSUE_NUMBER": str(issue_number),
                "ISSUE_BODY": body,
                "ISSUE_URL": (
                    f"https://github.com/Svyable/human-kind/issues/{issue_number}"
                ),
                "ISSUE_UPDATED_AT": "2026-08-27T12:00:00Z",
            }
        )
        if title is not None:
            env["ISSUE_TITLE"] = title
            env["ISSUE_ACTOR"] = "harness"
        return subprocess.run(
            [sys.executable, str(self.root / "scripts" / script_name)],
            env=env,
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )

    def run_idea(
        self,
        body: str | None = None,
        *,
        number: int = 9001,
        title: str = "[Agent Idea] Test bounded intervention quality",
    ) -> subprocess.CompletedProcess[str]:
        return self.run_script(
            IDEA_SCRIPT.name,
            issue_number=number,
            body=body if body is not None else self.idea_body,
            title=title,
        )

    def run_review(
        self,
        body: str | None = None,
        *,
        number: int = 9101,
    ) -> subprocess.CompletedProcess[str]:
        return self.run_script(
            REVIEW_SCRIPT.name,
            issue_number=number,
            body=body if body is not None else self.review_body,
        )

    def assert_failed(
        self, result: subprocess.CompletedProcess[str], contains: str | None = None
    ) -> None:
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        if contains:
            self.assertIn(contains, result.stdout + result.stderr)

    # Positive controls

    def test_valid_idea_materializes_disclosure_and_index(self) -> None:
        result = self.run_idea()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        paths = list(self.root.glob("ideas/climate/HK-9001-*/idea.yaml"))
        self.assertEqual(len(paths), 1)
        data = yaml.safe_load(paths[0].read_text())
        self.assertEqual(data["status"], "intake")
        self.assertEqual(data["generated_by"], "agent")
        self.assertEqual(data["review_requirement"], "independent")
        self.assertEqual(data["verification_status"], "unverified")
        self.assertNotIn("human_reviewer", data)
        self.assertIs(data["claims_requiring_verification"], True)
        self.assertEqual(data["decision_authority"], "repository-scoped")
        self.assertEqual(data["geography"], ["global", "Canada"])
        index = yaml.safe_load((self.root / "data" / "idea-index.yaml").read_text())
        self.assertEqual(index["ideas"][0]["id"], "HK-9001")

    def test_issue_text_is_literal_not_shell_code(self) -> None:
        marker = self.root / "SHOULD_NOT_EXIST"
        payload = f"Record the literal string $(touch {marker}) without executing it."
        body = replace_section(self.idea_body, "Proposed intervention", payload)
        result = self.run_idea(body, number=9002)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(marker.exists())
        proposal = next(self.root.glob("ideas/climate/HK-9002-*/proposal.md"))
        self.assertIn("$(touch", proposal.read_text())

    def test_other_constrained_contributor_role_is_accepted(self) -> None:
        body = replace_section(
            self.idea_body, "Agent role", "Other constrained contributor"
        )
        result = self.run_idea(body, number=9003)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_new_science_domains_are_accepted(self) -> None:
        for number, domain in ((9004, "basic-science"), (9005, "engineering-and-energy")):
            body = replace_section(self.idea_body, "Primary domain", domain)
            result = self.run_idea(body, number=number)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(len(list(self.root.glob(f"ideas/{domain}/HK-{number}-*/idea.yaml"))), 1)

    def test_valid_review_creates_twins_without_status_mutation(self) -> None:
        dossier = self.root / "ideas" / "cross-cutting" / "HK-0004-harness-test"
        before = yaml.safe_load((dossier / "idea.yaml").read_text())
        result = self.run_review(number=9101)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        review_yaml = dossier / "reviews" / "AR-9101-skeptic.yaml"
        review_md = dossier / "reviews" / "AR-9101-skeptic.md"
        self.assertTrue(review_yaml.exists())
        self.assertTrue(review_md.exists())
        review = yaml.safe_load(review_yaml.read_text())
        self.assertEqual(review["recommended_status"], "needs-evidence")
        self.assertEqual(review["review_requirement"], "independent")
        self.assertEqual(review["verification_status"], "unverified")
        self.assertNotIn("human_reviewer", review)
        self.assertEqual(review["decision_authority"], "repository-scoped")
        after = yaml.safe_load((dossier / "idea.yaml").read_text())
        self.assertEqual(after, before)

    def test_review_retry_is_idempotent(self) -> None:
        first = self.run_review(number=9102)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        second = self.run_review(number=9102)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        dossier = self.root / "ideas" / "cross-cutting" / "HK-0004-harness-test"
        self.assertEqual(len(list((dossier / "reviews").glob("AR-9102-*"))), 2)

    def test_red_team_role_maps_to_machine_slug(self) -> None:
        body = replace_section(self.review_body, "Agent role", "Red team")
        result = self.run_review(body, number=9103)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        dossier = self.root / "ideas" / "cross-cutting" / "HK-0004-harness-test"
        review = yaml.safe_load(
            (dossier / "reviews" / "AR-9103-red-team.yaml").read_text()
        )
        self.assertEqual(review["role"], "red-team")

    # Adversarial controls

    def test_duplicate_idea_id_is_rejected(self) -> None:
        first = self.run_idea(number=9200)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        second = self.run_idea(number=9200)
        self.assert_failed(second, "ID collision")

    def test_idea_missing_heading_rejected(self) -> None:
        self.assert_failed(
            self.run_idea(
                remove_section(self.idea_body, "Theory of change"), number=9201
            ),
            "missing headings",
        )

    def test_idea_unchecked_attestation_rejected(self) -> None:
        body = replace_section(
            self.idea_body,
            "Agent attestation",
            "- [ ] one\n- [ ] two\n- [ ] three",
        )
        self.assert_failed(self.run_idea(body, number=9202), "attestation")

    def test_idea_invalid_domain_rejected(self) -> None:
        body = replace_section(self.idea_body, "Primary domain", "astrology")
        self.assert_failed(
            self.run_idea(body, number=9203), "Unsupported primary domain"
        )

    def test_idea_invalid_time_horizon_rejected(self) -> None:
        body = replace_section(self.idea_body, "Time horizon", "immediate")
        self.assert_failed(
            self.run_idea(body, number=9204), "Unsupported time horizon"
        )

    def test_idea_invalid_intervention_type_rejected(self) -> None:
        body = replace_section(self.idea_body, "Intervention type", "magic")
        self.assert_failed(
            self.run_idea(body, number=9205), "Unsupported intervention type"
        )

    def test_idea_invalid_reversibility_rejected(self) -> None:
        body = replace_section(self.idea_body, "Reversibility", "absolute")
        self.assert_failed(self.run_idea(body, number=9206), "Unsupported reversibility")

    def test_idea_unsupported_role_rejected(self) -> None:
        body = replace_section(self.idea_body, "Agent role", "Supreme decider")
        self.assert_failed(
            self.run_idea(body, number=9207), "Unsupported agent role"
        )

    def test_review_unknown_idea_rejected(self) -> None:
        body = replace_section(self.review_body, "Idea ID", "HK-9999")
        self.assert_failed(self.run_review(body, number=9301), "No dossier found")

    def test_review_unsupported_role_rejected(self) -> None:
        body = replace_section(self.review_body, "Agent role", "Supreme decider")
        self.assert_failed(
            self.run_review(body, number=9302), "Unsupported agent role"
        )

    def test_review_unchecked_attestation_rejected(self) -> None:
        body = replace_section(
            self.review_body,
            "Agent attestation",
            "- [x] one\n- [ ] two\n- [ ] three",
        )
        self.assert_failed(self.run_review(body, number=9303), "attestation")

    def test_review_invalid_status_rejected(self) -> None:
        body = replace_section(self.review_body, "Recommended status", "approved")
        self.assert_failed(
            self.run_review(body, number=9304), "Unsupported recommended status"
        )

    def test_review_empty_sources_rejected(self) -> None:
        body = replace_section(self.review_body, "Sources and evidence", "")
        self.assert_failed(
            self.run_review(body, number=9305), "Missing required section"
        )

    def test_review_empty_findings_rejected(self) -> None:
        body = replace_section(self.review_body, "Findings", "")
        self.assert_failed(
            self.run_review(body, number=9306), "Missing required section"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
