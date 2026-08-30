#!/usr/bin/env python3
"""Regression tests for conflict-resistant intake index fragments."""

from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "index_intake_fragment.py"


class IndexFragmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        (self.root / "scripts").mkdir()
        (self.root / "data").mkdir()
        shutil.copy2(SCRIPT, self.root / "scripts" / SCRIPT.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_helper(self, issue_number: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["ISSUE_NUMBER"] = issue_number
        return subprocess.run(
            [sys.executable, str(self.root / "scripts" / SCRIPT.name)],
            cwd=self.root,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )

    def test_writes_exact_materialized_entry_to_independent_fragment(self) -> None:
        entry = {
            "id": "HK-0042",
            "title": "Test independent intake indexing",
            "status": "intake",
            "domains": ["cross-cutting"],
            "evidence_level": "hypothesis",
            "last_reviewed": "2026-08-30",
            "path": "ideas/cross-cutting/HK-0042-test-independent-intake-indexing",
            "source_issue": "https://github.com/Svyable/human-kind/issues/42",
        }
        (self.root / "data" / "idea-index.yaml").write_text(
            yaml.safe_dump({"version": 1, "ideas": [entry]}, sort_keys=False)
        )

        result = self.run_helper("42")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        fragment = self.root / "data" / "idea-index.d" / "HK-0042.yaml"
        self.assertEqual(yaml.safe_load(fragment.read_text()), entry)

    def test_rejects_missing_materialized_entry(self) -> None:
        (self.root / "data" / "idea-index.yaml").write_text("version: 1\nideas: []\n")
        result = self.run_helper("42")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exactly one materialized index entry", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
