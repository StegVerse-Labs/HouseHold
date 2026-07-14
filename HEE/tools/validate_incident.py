#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "hee-validation-v1"
ALLOWED_REVIEW_STATES = {"draft", "reviewed", "sent"}
REQUIRED_FIELDS = (
    "incident_id",
    "escalation_level",
    "counterparty",
    "objectives",
    "evidence_paths",
    "review_state",
    "unresolved_uncertainty",
)


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


def build_packet_plan(incident_dir: Path, validation: dict[str, Any]) -> dict[str, Any]:
    _, manifest = _load_manifest(incident_dir.resolve())
    return {
        "schema_version": "hee-packet-plan-v1",
        "incident_id": manifest.get("incident_id"),
        "escalation_level": manifest.get("escalation_level"),
        "counterparty": manifest.get("counterparty"),
        "objectives": manifest.get("objectives", []),
        "review_state": manifest.get("review_state"),
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


def _markdown_report(validation: dict[str, Any]) -> str:
    lines = [
        f"# HEE Validation — {validation.get('incident_id') or 'unknown'}",
        "",
        f"- **Status:** {validation['status']}",
        f"- **Review state:** {validation.get('review_state')}",
        f"- **Evidence files validated:** {len(validation['evidence'])}",
        f"- **Supporting files validated:** {len(validation['supporting_files'])}",
        f"- **Errors:** {len(validation['errors'])}",
        f"- **Warnings:** {len(validation['warnings'])}",
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
        "This report validates structure and references only. It does not authenticate evidence, decide truth, establish custody authority, provide legal advice, or authorize delivery.",
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
    (output_dir / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "validation.md").write_text(
        _markdown_report(validation),
        encoding="utf-8",
    )
    (output_dir / "packet-plan.json").write_text(
        json.dumps(packet_plan, indent=2, sort_keys=True) + "\n",
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
            print(json.dumps(validation, indent=2, sort_keys=True))
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
