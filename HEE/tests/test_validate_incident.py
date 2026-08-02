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

    def test_minimal_fixture_passes_and_requires_review(self) -> None:
        result = MODULE.validate_incident(self.fixture)
        plan = MODULE.build_packet_plan(self.fixture, result)
        self.assertEqual("PASS", result["status"])
        self.assertEqual("minimal-incident", result["incident_id"])
        self.assertEqual(1, len(result["evidence"]))
        self.assertEqual(2, len(result["supporting_files"]))
        self.assertEqual("REVIEW_REQUIRED", plan["machine_state"])

    def test_packet_plan_never_authorizes_send(self) -> None:
        result = MODULE.validate_incident(self.fixture)
        plan = MODULE.build_packet_plan(self.fixture, result)
        self.assertTrue(plan["ready_for_human_review"])
        self.assertFalse(plan["send_authorized"])
        self.assertEqual(
            ["README.md", "letter.md", "attachments.md"],
            plan["required_packet_files"],
        )

    def test_missing_evidence_is_blocked(self) -> None:
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
            plan = MODULE.build_packet_plan(root, result)
            self.assertEqual("FAIL", result["status"])
            self.assertEqual("BLOCKED", plan["machine_state"])

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
            for name in (
                "validation.json",
                "validation.md",
                "packet-plan.json",
                "execution-receipt.json",
            ):
                self.assertTrue((output_dir / name).is_file())
                self.assertFalse((self.fixture / name).exists())

    def test_execution_receipt_is_fail_closed(self) -> None:
        validation = MODULE.validate_incident(self.fixture)
        plan = MODULE.build_packet_plan(self.fixture, validation)
        receipt = MODULE.build_execution_receipt(self.fixture, validation, plan)
        self.assertEqual("REVIEW_REQUIRED", receipt["machine_state"])
        self.assertFalse(receipt["send_authorized"])
        self.assertFalse(receipt["repository_mutation_authorized"])
        self.assertFalse(receipt["external_delivery_authorized"])
        self.assertIn("minimal-incident:", receipt["duplicate_execution_key"])


if __name__ == "__main__":
    unittest.main()
