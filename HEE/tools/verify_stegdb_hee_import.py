#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_VALUES = {"COMPLETE", "BLOCKED", "RETRY", "REVIEW_REQUIRED", "FAILED"}
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "HEE" / "canonical" / "stegdb-hee-v1-import.json"
DEFAULT_OUTPUT = ROOT / "out" / "hee" / "canonical"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json_bytes(data: bytes, label: str) -> dict[str, Any]:
    try:
        parsed = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid JSON for {label}: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError(f"{label} must contain a JSON object")
    return parsed


def fetch_bytes(repository: str, commit: str, path: str, timeout: int = 20) -> bytes:
    owner, name = repository.split("/", 1)
    url = f"https://raw.githubusercontent.com/{owner}/{name}/{commit}/{path}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github.raw",
            "User-Agent": "HouseHold-HEE-Canonical-Import/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def validate_config(config: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    required = (
        "schema_version",
        "source_repository",
        "source_commit_sha",
        "consumer_repository",
        "package_manifest_path",
        "required_paths",
        "overlay_only",
        "incident_data_modified",
    )
    for field in required:
        if field not in config:
            errors.append({"code": "missing_config_field", "detail": field})
    if config.get("schema_version") != "household-hee-import-config-v1":
        errors.append({"code": "wrong_config_version", "detail": str(config.get("schema_version"))})
    if config.get("source_repository") != "StegVerse-Labs/StegDB":
        errors.append({"code": "wrong_source_repository", "detail": str(config.get("source_repository"))})
    commit = config.get("source_commit_sha")
    if not isinstance(commit, str) or len(commit) != 40 or any(ch not in "0123456789abcdef" for ch in commit):
        errors.append({"code": "invalid_source_commit", "detail": str(commit)})
    if config.get("consumer_repository") != "StegVerse-Labs/HouseHold":
        errors.append({"code": "wrong_consumer_repository", "detail": str(config.get("consumer_repository"))})
    if config.get("overlay_only") is not True:
        errors.append({"code": "overlay_not_enforced", "detail": "overlay_only must be true"})
    if config.get("incident_data_modified") is not False:
        errors.append({"code": "incident_mutation_not_forbidden", "detail": "incident_data_modified must be false"})
    paths = config.get("required_paths")
    if not isinstance(paths, list) or not paths or not all(isinstance(item, str) and item for item in paths):
        errors.append({"code": "invalid_required_paths", "detail": "required_paths must be a non-empty string array"})
    elif len(paths) != len(set(paths)):
        errors.append({"code": "duplicate_required_path", "detail": "required_paths contains duplicates"})
    return errors


def run_import(config_path: Path, output_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("import config must contain a JSON object")

    errors = validate_config(config)
    fetched: list[dict[str, Any]] = []
    package: dict[str, Any] | None = None
    state = "FAILED" if errors else "REVIEW_REQUIRED"

    if not errors:
        repository = config["source_repository"]
        commit = config["source_commit_sha"]
        package_path = config["package_manifest_path"]
        try:
            package_bytes = fetch_bytes(repository, commit, package_path)
            package = load_json_bytes(package_bytes, package_path)
            package_files = package.get("files", [])
            if package.get("schema_version") != "hee-v1-package-manifest-v1":
                errors.append({"code": "wrong_package_version", "detail": str(package.get("schema_version"))})
            if package.get("owner_repository") != repository:
                errors.append({"code": "package_owner_mismatch", "detail": str(package.get("owner_repository"))})
            if package.get("consumer_repository") != config["consumer_repository"]:
                errors.append({"code": "package_consumer_mismatch", "detail": str(package.get("consumer_repository"))})
            if package_files != config["required_paths"]:
                errors.append({"code": "required_path_set_mismatch", "detail": "package file list does not exactly match HouseHold import config"})
            boundaries = package.get("boundaries", {})
            for key in (
                "authenticates_evidence",
                "establishes_truth",
                "establishes_ownership",
                "authorizes_delivery",
                "modifies_incident_data",
            ):
                if boundaries.get(key) is not False:
                    errors.append({"code": "package_boundary_not_fail_closed", "detail": key})

            for path in config["required_paths"]:
                data = fetch_bytes(repository, commit, path)
                if path.endswith(".json"):
                    load_json_bytes(data, path)
                fetched.append(
                    {
                        "path": path,
                        "sha256": sha256_bytes(data),
                        "size_bytes": len(data),
                    }
                )
        except urllib.error.HTTPError as exc:
            errors.append({"code": "source_http_error", "detail": f"{exc.code}: {exc.reason}"})
            state = "BLOCKED" if exc.code in {401, 403, 404} else "RETRY"
        except (urllib.error.URLError, TimeoutError) as exc:
            errors.append({"code": "source_unavailable", "detail": str(exc)})
            state = "RETRY"
        except (OSError, ValueError, KeyError) as exc:
            errors.append({"code": "source_validation_error", "detail": str(exc)})
            state = "FAILED"

    if errors and state == "REVIEW_REQUIRED":
        state = "FAILED"
    elif not errors:
        state = "COMPLETE"

    duplicate_payload = {
        "source_repository": config.get("source_repository"),
        "source_commit_sha": config.get("source_commit_sha"),
        "required_paths": config.get("required_paths"),
        "fetched": fetched,
    }
    duplicate_execution_key = hashlib.sha256(
        json.dumps(duplicate_payload, sort_keys=True).encode("utf-8")
    ).hexdigest()

    next_task = {
        "COMPLETE": "Use this source-lock receipt as the canonical input to HouseHold HEE validation.",
        "BLOCKED": "Restore read access to the pinned StegDB commit or replace it with an authorized accessible commit.",
        "RETRY": "Retry the import after source connectivity recovers.",
        "REVIEW_REQUIRED": "Review the imported protocol boundaries before use.",
        "FAILED": "Correct the first validation error and rerun the import validator.",
    }[state]

    generated_at = datetime.now(timezone.utc).isoformat()
    validation = {
        "schema_version": "household-hee-import-validation-v1",
        "owner_repository": "StegVerse-Labs/HouseHold",
        "source_repository": config.get("source_repository"),
        "source_commit_sha": config.get("source_commit_sha"),
        "generated_at": generated_at,
        "state": state,
        "errors": errors,
        "fetched_protocols": fetched,
        "duplicate_execution_key": duplicate_execution_key,
        "next_executable_task": next_task,
        "repository_mutation_authorized": False,
        "external_delivery_authorized": False,
        "incident_data_modified": False,
    }

    lock = {
        "schema_version": "household-source-lock-v1",
        "lock_id": f"HOUSEHOLD-HEE-V1-{config.get('source_commit_sha', 'unknown')[:12]}",
        "source_repository": config.get("source_repository"),
        "source_commit_sha": config.get("source_commit_sha"),
        "consumer_repository": config.get("consumer_repository"),
        "protocols": [
            {
                "path": item["path"],
                "sha256": item["sha256"],
                "schema_or_protocol_version": Path(item["path"]).name,
            }
            for item in fetched
        ],
        "imported_at": generated_at,
        "validation_state": state,
        "validation_receipt_ref": "out/hee/canonical/import-validation.json",
        "overlay_only": True,
        "incident_data_modified": False,
        "next_executable_task": next_task,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "import-validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "household-source-lock.json").write_text(
        json.dumps(lock, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return validation, lock


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify and lock the commit-pinned StegDB HEE v1 package.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    try:
        validation, _ = run_import(args.config, args.output_dir)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(validation, indent=2, sort_keys=True))
    return 0 if validation["state"] == "COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
