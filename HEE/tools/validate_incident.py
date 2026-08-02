#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "hee-validation-v1"
RECEIPT_VERSION = "hee-execution-receipt-v1"
ALLOWED_REVIEW_STATES = {"draft", "reviewed", "sent"}
MACHINE_STATES = {"COMPLETE", "BLOCKED", "RETRY", "REVIEW_REQUIRED", "FAILED"}
REQUIRED_FIELDS = (
    "incident_id",
    "escalation_level",
    "counterparty",
    "objectives",
    "evidence_paths",
    "review_state",
    "unresolved_uncertainty",
)
BLOCKING_ERROR_CODES = {
    "missing_required_field",
    "missing_evidence",
    "missing_supporting_file",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative_path(value: str) -> bool:
    path = Path(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts


def _load_manifest(incident_dir: Path) -> tuple[Path, dict[str, Any]]:
    manifest_path = incident_dir / "incident.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"missing manifest: {manifest_path}")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {manifest_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("incident.json must contain a JSON object")
    return manifest_path, data


def validate_incident(incident_dir: Path) -> dict[str, Any]:
    incident_dir = incident_dir.resolve()
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    manifest_path, manifest = _load_manifest(incident_dir)

    for field in REQUIRED_FIELDS:
        if field not in manifest:
            errors.append({"code": "missing_required_field", "field": field})

    incident_id = manifest.get("incident_id")
    if not isinstance(incident_id, str) or not incident_id.strip():
        errors.append({"code": "invalid_incident_id", "field": "incident_id"})

    level = manifest.get("escalation_level")
    if not isinstance(level, int) or level < 1:
        errors.append({"code": "invalid_escalation_level", "field": "escalation_level"})

    counterparty = manifest.get("counterparty")
    if not isinstance(counterparty, str) or not counterparty.strip():
        errors.append({"code": "invalid_counterparty", "field": "counterparty"})

    objectives = manifest.get("objectives")
    if not isinstance(objectives, list) or not objectives or not all(
        isinstance(item, str) and item.strip() for item in objectives
    ):
        errors.append({"code": "invalid_objectives", "field": "objectives"})

    review_state = manifest.get("review_state")
    if review_state not in ALLOWED_REVIEW_STATES:
        errors.append({"code": "invalid_review_state", "field": "review_state"})
    elif review_state == "sent":
        warnings.append(
            {
                "code": "sent_state_not_delivery_proof",
                "message": "review_state=sent is an assertion and is not independent delivery proof.",
            }
        )

    uncertainty = manifest.get("unresolved_uncertainty")
    if not isinstance(uncertainty, list) or not all(
        isinstance(item, str) and item.strip() for item in uncertainty
    ):
        errors.append(
            {
                "code": "invalid_unresolved_uncertainty",
                "field": "unresolved_uncertainty",
            }
        )
    elif uncertainty:
        warnings.append(
            {
                "code": "unresolved_uncertainty_present",
                "message": f"{len(uncertainty)} unresolved uncertainty item(s) remain.",
            }
        )

    evidence = manifest.get("evidence_paths")
    evidence_results: list[dict[str, Any]] = []
    if not isinstance(evidence, list) or not evidence:
        errors.append({"code": "invalid_evidence_paths", "field": "evidence_paths"})
        evidence = []
    for value in evidence:
        if not isinstance(value, str) or not _safe_relative_path(value):
            errors.append({"code": "unsafe_evidence_path", "path": str(value)})
            continue
        path = incident_dir / value
        if not path.is_file():
            errors.append({"code": "missing_evidence", "path": value})
            continue
        evidence_results.append(
            {
                "path": value,
                "sha256": _sha256(path),
                "size_bytes": path.stat().st_size,
            }
        )

    supporting_paths = manifest.get("supporting_paths", [])
    if not isinstance(supporting_paths, list):
        errors.append({"code": "invalid_supporting_paths", "field": "supporting_paths"})
        supporting_paths = []
    supporting_results: list[dict[str, Any]] = []
    for value in supporting_paths:
        if not isinstance(value, str) or not _safe_relative_path(value):
            errors.append({"code": "unsafe_supporting_path", "path": str(value)})
            continue
        path = incident_dir / value
        if not path.is_file():
            errors.append({"code": "missing_supporting_file", "path": value})
            continue
        supporting_results.append(
            {
                "path": value,
                "sha256": _sha256(path),
                "size_bytes": path.stat().st_size,
            }
        )

    if review_state == "reviewed" and errors:
        warnings.append(
            {
                "code": "reviewed_manifest_has_errors",
                "message": "The manifest claims reviewed state but validation errors remain.",
            }
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PASS" if not errors else "FAIL",
        "incident_id": incident_id if isinstance(incident_id, str) else None,
        "source_manifest": {
            "path": "incident.json",
            "sha256": _sha256(manifest_path),
        },
        "review_state": review_state,
        "errors": errors,
        "warnings": warnings,
        "unresolved_uncertainty": uncertainty if isinstance(uncertainty, list) else [],
        "evidence": evidence_results,
        "supporting_files": supporting_results,
    }


def classify_machine_state(validation: dict[str, Any]) -> tuple[str, str]:
    errors = validation.get("errors", [])
    error_codes = {item.get("code") for item in errors}
    if errors:
        if error_codes & BLOCKING_ERROR_CODES:
            return "BLOCKED", "Resolve missing required fields or referenced files, then rerun validation."
        return "FAILED", "Correct invalid incident structure or values, then rerun validation."
    if validation.get("review_state") != "reviewed":
        return "REVIEW_REQUIRED", "A human authority must review the packet inputs and set review_state=reviewed."
    if validation.get("unresolved_uncertainty") or validation.get("warnings"):
        return "REVIEW_REQUIRED", "Resolve or explicitly accept recorded uncertainty and warnings."
    return "COMPLETE", "No additional structural validation task is required for this incident revision."


def build_packet_plan(incident_dir: Path, validation: dict[str, Any]) -> dict[str, Any]:
    _, manifest = _load_manifest(incident_dir.resolve())
    machine_state, next_task = classify_machine_state(validation)
    return {
        "schema_version": "hee-packet-plan-v1",
        "incident_id": manifest.get("incident_id"),
        "escalation_level": manifest.get("escalation_level"),
        "counterparty": manifest.get("counterparty"),
        "objectives": manifest.get("objectives", []),
        "review_state": manifest.get("review_state"),
        "machine_state": machine_state,
        "next_executable_task": next_task,
        "ready_for_human_review": validation["status"] == "PASS",
        "send_authorized": False,
        "evidence": validation["evidence"],
        "supporting_files": validation["supporting_files"],
        "unresolved_uncertainty": validation["unresolved_uncertainty"],
        "required_packet_files": ["README.md", "letter.md", "attachments.md"],
        "notes": [
            "This is a dry-run plan and does not generate or send an external letter.",
            "A human reviewer must confirm facts, recipient, remedy, attachments, and delivery method.",
        ],
    }


def build_execution_receipt(
    incident_dir: Path,
    validation: dict[str, Any],
    packet_plan: dict[str, Any],
) -> dict[str, Any]:
    machine_state = packet_plan["machine_state"]
    if machine_state not in MACHINE_STATES:
        raise ValueError(f"unsupported machine state: {machine_state}")
    return {
        "schema_version": RECEIPT_VERSION,
        "generated_at": _utc_now(),
        "owner_repository": "StegVerse-Labs/HouseHold",
        "owner_component": "HEE synthetic-fixture validator",
        "trigger_contract": ["workflow_dispatch", "push:path-filter", "schedule:weekly"],
        "incident_id": validation.get("incident_id") or incident_dir.name,
        "source_manifest_sha256": validation["source_manifest"]["sha256"],
        "validation_status": validation["status"],
        "machine_state": machine_state,
        "next_executable_task": packet_plan["next_executable_task"],
        "duplicate_execution_key": (
            f"{validation.get('incident_id') or incident_dir.name}:"
            f"{validation['source_manifest']['sha256']}"
        ),
        "outputs": ["validation.json", "validation.md", "packet-plan.json", "execution-receipt.json"],
        "send_authorized": False,
        "repository_mutation_authorized": False,
        "external_delivery_authorized": False,
    }


def _markdown_report(validation: dict[str, Any], packet_plan: dict[str, Any]) -> str:
    lines = [
        f"# HEE Validation — {validation.get('incident_id') or 'unknown'}",
        "",
        f"- **Validation status:** {validation['status']}",
        f"- **Machine state:** {packet_plan['machine_state']}",
        f"- **Review state:** {validation.get('review_state')}",
        f"- **Evidence files validated:** {len(validation['evidence'])}",
        f"- **Supporting files validated:** {len(validation['supporting_files'])}",
        f"- **Errors:** {len(validation['errors'])}",
        f"- **Warnings:** {len(validation['warnings'])}",
        f"- **Next task:** {packet_plan['next_executable_task']}",
        "",
        "## Errors",
    ]
    lines.extend(
        [
            f"- `{item.get('code')}` — {json.dumps(item, sort_keys=True)}"
            for item in validation["errors"]
        ]
        or ["- None"]
    )
    lines += ["", "## Warnings"]
    lines.extend(
        [
            f"- `{item.get('code')}` — {item.get('message', json.dumps(item, sort_keys=True))}"
            for item in validation["warnings"]
        ]
        or ["- None"]
    )
    lines += ["", "## Unresolved uncertainty"]
    lines.extend(
        [f"- {item}" for item in validation["unresolved_uncertainty"]] or ["- None"]
    )
    lines += [
        "",
        "## Boundary",
        "",
        "This report validates structure and references only. It does not authenticate evidence, decide truth, establish custody authority, provide legal advice, mutate the repository, or authorize delivery.",
        "",
    ]
    return "\n".join(lines)


def write_outputs(
    incident_dir: Path,
    output_root: Path,
    validation: dict[str, Any],
    packet_plan: dict[str, Any],
) -> Path:
    incident_id = validation.get("incident_id") or incident_dir.name
    output_dir = output_root / str(incident_id)
    output_dir.mkdir(parents=True, exist_ok=True)
    receipt = build_execution_receipt(incident_dir, validation, packet_plan)
    (output_dir / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "validation.md").write_text(
        _markdown_report(validation, packet_plan),
        encoding="utf-8",
    )
    (output_dir / "packet-plan.json").write_text(
        json.dumps(packet_plan, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "execution-receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a HouseHold incident and create a dry-run HEE packet plan."
    )
    parser.add_argument("incident_dir", type=Path)
    parser.add_argument("--output-root", type=Path, default=Path("out/hee"))
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate without writing output files.",
    )
    args = parser.parse_args()

    try:
        validation = validate_incident(args.incident_dir)
        packet_plan = build_packet_plan(args.incident_dir, validation)
        if args.check_only:
            print(json.dumps({"validation": validation, "packet_plan": packet_plan}, indent=2, sort_keys=True))
        else:
            print(
                write_outputs(
                    args.incident_dir,
                    args.output_root,
                    validation,
                    packet_plan,
                )
            )
        return 0 if validation["status"] == "PASS" else 1
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
