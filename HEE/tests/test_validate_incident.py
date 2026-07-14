from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "HEE" / "tools" / "validate_incident.py"
SPEC = importlib.util.spec_from_file_location("validate_incident", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ValidateIncidentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = ROOT / "HEE" / "fixtures" / "minimal-incident"

    def test_minimal_fixture_passes(self) -> None:
        result = MODULE.validate_incident(self.fixture)
        self.assertEqual("PASS", result["status"])
        self.assertEqual("minimal-incident", result["incident_id"])
        self.assertEqual(1, len(result["evidence"]))
        self.assertEqual(2, len(result["supporting_files"]))
        self.assertTrue(
            any(
                item["code"] == "unresolved_uncertainty_present"
                for item in result["warnings"]
            )
        )

    def test_packet_plan_never_authorizes_send(self) -> None:
        result = MODULE.validate_incident(self.fixture)
        plan = MODULE.build_packet_plan(self.fixture, result)
        self.assertTrue(plan["ready_for_human_review"])
        self.assertFalse(plan["send_authorized"])
        self.assertEqual(
            ["README.md", "letter.md", "attachments.md"],
            plan["required_packet_files"],
        )

    def test_missing_evidence_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "incident.json").write_text(
                json.dumps(
                    {
                        "incident_id": "broken",
                        "escalation_level": 1,
                        "counterparty": "Example",
                        "objectives": ["Request response"],
                        "evidence_paths": ["evidence/missing.txt"],
                        "supporting_paths": [],
                        "review_state": "draft",
                        "unresolved_uncertainty": [],
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.validate_incident(root)
            self.assertEqual("FAIL", result["status"])
            self.assertTrue(
                any(item["code"] == "missing_evidence" for item in result["errors"])
            )

    def test_output_is_written_outside_fixture(self) -> None:
        validation = MODULE.validate_incident(self.fixture)
        plan = MODULE.build_packet_plan(self.fixture, validation)
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = MODULE.write_outputs(
                self.fixture,
                Path(temp_dir),
                validation,
                plan,
            )
            self.assertTrue((output_dir / "validation.json").is_file())
            self.assertTrue((output_dir / "validation.md").is_file())
            self.assertTrue((output_dir / "packet-plan.json").is_file())
            self.assertFalse((self.fixture / "validation.json").exists())


if __name__ == "__main__":
    unittest.main()
