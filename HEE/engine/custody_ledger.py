#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "custody-transition-v1"
BOUNDARY_VALUE = "NONE_BY_RECORD_ALONE"
ALLOWED_STATES = {"PROPOSED", "ACKNOWLEDGED", "CONTESTED", "CONFIRMED", "EXPIRED", "REVOKED"}


@dataclass(frozen=True)
class LedgerResult:
    state: str
    transition: dict[str, Any] | None
    errors: list[dict[str, str]]
    next_executable_task: str


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _is_datetime(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def _transition_digest(transition: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(transition, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate_transition(transition: dict[str, Any], previous: dict[str, Any] | None) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    required = (
        "schema_version", "transition_id", "item_id", "sequence", "state", "initiated_by",
        "current_custodian", "proposed_custodian", "recorded_at", "authority_effect",
        "truth_effect", "ownership_effect",
    )
    for field in required:
        if field not in transition:
            errors.append({"code": "missing_required_field", "detail": field})

    if transition.get("schema_version") != SCHEMA_VERSION:
        errors.append({"code": "wrong_schema_version", "detail": str(transition.get("schema_version"))})
    if transition.get("state") not in ALLOWED_STATES:
        errors.append({"code": "invalid_state", "detail": str(transition.get("state"))})
    if not isinstance(transition.get("sequence"), int) or transition.get("sequence", 0) < 1:
        errors.append({"code": "invalid_sequence", "detail": str(transition.get("sequence"))})
    if not _is_datetime(transition.get("recorded_at")):
        errors.append({"code": "invalid_recorded_at", "detail": str(transition.get("recorded_at"))})
    for field in ("authority_effect", "truth_effect", "ownership_effect"):
        if transition.get(field) != BOUNDARY_VALUE:
            errors.append({"code": "boundary_violation", "detail": field})

    if previous is None:
        if transition.get("sequence") != 1:
            errors.append({"code": "first_sequence_must_be_one", "detail": str(transition.get("sequence"))})
        if transition.get("previous_transition_id") not in (None, ""):
            errors.append({"code": "first_transition_has_previous", "detail": str(transition.get("previous_transition_id"))})
    else:
        if transition.get("item_id") != previous.get("item_id"):
            errors.append({"code": "item_id_changed", "detail": str(transition.get("item_id"))})
        if transition.get("sequence") != previous.get("sequence", 0) + 1:
            errors.append({"code": "non_monotonic_sequence", "detail": str(transition.get("sequence"))})
        if transition.get("previous_transition_id") != previous.get("transition_id"):
            errors.append({"code": "previous_transition_mismatch", "detail": str(transition.get("previous_transition_id"))})

    return errors


def append_transition(ledger_path: Path, transition: dict[str, Any], receipt_path: Path | None = None) -> LedgerResult:
    ledger: list[dict[str, Any]]
    if ledger_path.exists():
        loaded = _load_json(ledger_path)
        if not isinstance(loaded, list):
            raise ValueError("custody ledger must contain a JSON array")
        ledger = loaded
    else:
        ledger = []

    previous = ledger[-1] if ledger else None
    errors = validate_transition(transition, previous)

    if any(item.get("transition_id") == transition.get("transition_id") for item in ledger):
        errors.append({"code": "duplicate_transition_id", "detail": str(transition.get("transition_id"))})

    if errors:
        result = LedgerResult(
            state="FAILED",
            transition=None,
            errors=errors,
            next_executable_task="Correct the first custody transition validation error and retry.",
        )
    else:
        ledger.append(transition)
        _write_json(ledger_path, ledger)
        result = LedgerResult(
            state="COMPLETE",
            transition=transition,
            errors=[],
            next_executable_task="Validate notification references and continue to packet review when required.",
        )

    if receipt_path is not None:
        receipt = {
            "schema_version": "hee-custody-append-receipt-v1",
            "state": result.state,
            "ledger_path": str(ledger_path),
            "transition_id": transition.get("transition_id"),
            "transition_sha256": _transition_digest(transition),
            "errors": result.errors,
            "next_executable_task": result.next_executable_task,
            "boundaries": {
                "establishes_truth": False,
                "establishes_ownership": False,
                "establishes_authority": False,
                "external_delivery_authorized": False,
            },
        }
        _write_json(receipt_path, receipt)

    return result
