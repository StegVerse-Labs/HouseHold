from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "HEE" / "engine" / "custody_ledger.py"
SPEC = importlib.util.spec_from_file_location("custody_ledger", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def transition(sequence: int, transition_id: str, previous: str | None) -> dict:
    return {
        "schema_version": "custody-transition-v1",
        "transition_id": transition_id,
        "item_id": "synthetic-item",
        "sequence": sequence,
        "previous_transition_id": previous,
        "state": "PROPOSED" if sequence == 1 else "ACKNOWLEDGED",
        "initiated_by": "synthetic-actor",
        "current_custodian": "custodian-a",
        "proposed_custodian": "custodian-b",
        "recorded_at": "2026-08-02T08:15:00Z",
        "authority_effect": "NONE_BY_RECORD_ALONE",
        "truth_effect": "NONE_BY_RECORD_ALONE",
        "ownership_effect": "NONE_BY_RECORD_ALONE",
        "evidence_refs": [],
        "notification_refs": [],
    }


class CustodyLedgerTests(unittest.TestCase):
    def test_appends_valid_chain_and_writes_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            ledger = root / "ledger.json"
            receipt = root / "receipt.json"
            first = MODULE.append_transition(ledger, transition(1, "tr-1", None), receipt)
            second = MODULE.append_transition(ledger, transition(2, "tr-2", "tr-1"), receipt)
            self.assertEqual("COMPLETE", first.state)
            self.assertEqual("COMPLETE", second.state)
            rows = json.loads(ledger.read_text())
            self.assertEqual(["tr-1", "tr-2"], [row["transition_id"] for row in rows])
            proof = json.loads(receipt.read_text())
            self.assertFalse(proof["boundaries"]["establishes_truth"])
            self.assertFalse(proof["boundaries"]["external_delivery_authorized"])

    def test_rejects_non_monotonic_sequence_without_mutating(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            ledger = Path(temp_dir) / "ledger.json"
            MODULE.append_transition(ledger, transition(1, "tr-1", None))
            before = ledger.read_bytes()
            result = MODULE.append_transition(ledger, transition(3, "tr-3", "tr-1"))
            self.assertEqual("FAILED", result.state)
            self.assertEqual(before, ledger.read_bytes())
            self.assertTrue(any(error["code"] == "non_monotonic_sequence" for error in result.errors))

    def test_rejects_boundary_violation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            ledger = Path(temp_dir) / "ledger.json"
            item = transition(1, "tr-1", None)
            item["ownership_effect"] = "ESTABLISHES_OWNERSHIP"
            result = MODULE.append_transition(ledger, item)
            self.assertEqual("FAILED", result.state)
            self.assertFalse(ledger.exists())

    def test_rejects_duplicate_transition_id(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            ledger = Path(temp_dir) / "ledger.json"
            MODULE.append_transition(ledger, transition(1, "tr-1", None))
            result = MODULE.append_transition(ledger, transition(2, "tr-1", "tr-1"))
            self.assertEqual("FAILED", result.state)
            self.assertTrue(any(error["code"] == "duplicate_transition_id" for error in result.errors))


if __name__ == "__main__":
    unittest.main()
