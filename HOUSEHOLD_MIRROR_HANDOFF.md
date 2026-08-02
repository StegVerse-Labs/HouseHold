# HouseHold Mirror Handoff

## Active Goal

Goal ID: `HOUSEHOLD-HEE-ACTIVATION-001`

Activate a governed Household Escalation Engine path that validates incident structure, preserves evidence boundaries, produces machine-owned continuation receipts, and cannot silently authorize repository mutation or external delivery.

Repository: `StegVerse-Labs/HouseHold`
Branch: `main`

## Authoritative Records

- `HOUSEHOLD_MIRROR_HANDOFF.md`
- `README.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `_new-incident-template/README.md`
- `HEE/README.md`
- `HEE/engine/packet-spec.md`
- `HEE/fixtures/minimal-incident/`
- `HEE/tools/validate_incident.py`
- `HEE/tests/test_validate_incident.py`
- `.github/workflows/hee-validate.yml`
- Cross-repository canonical task: `StegVerse-Labs/StegDB#9`

## Decisions Preserved

1. StegDB is the canonical protocol and schema authority.
2. HouseHold contains real incident state and implementation evidence.
3. HEE connects canonical rules to HouseHold workflows without replacing professional or human judgment.
4. Facts, findings, evidence, provenance, custody, confidence, review state, and delivery state remain distinct.
5. Confidence metadata is decision support, not proof, authentication, admissibility, or a legal conclusion.
6. Original evidence must not be silently overwritten.
7. Generated packet material remains draft until human review.
8. Automation must fail closed and must never infer permission to send, publish, notify, or mutate.
9. Public fixtures and CI data must remain synthetic or safely redacted.
10. Canonical synchronization must be overlay-only and non-destructive.

## Execution Inventory

### Complete and committed

- Repository guidance and security boundary.
- Synthetic incident fixture.
- Read-only structure and reference validator.
- Dry-run packet planner.
- Unit tests for valid fixture, missing evidence, output isolation, and delivery prohibition.
- Machine-owned execution receipt generation.
- Explicit machine-state vocabulary: `COMPLETE`, `BLOCKED`, `RETRY`, `REVIEW_REQUIRED`, `FAILED`.
- Duplicate execution key derived from incident ID and source-manifest SHA-256.
- Automated push-path, weekly scheduled, and manually dispatched CI validation.
- Read-only workflow permissions and non-mutating artifact upload.

### Implemented but awaiting hosted validation

- Updated validator commit: `340d3755dc261c63dc976f105e20b8e419c8da09`.
- Updated five-test suite commit: `a8c80fdc2edfbeeacced54c42c81b3c8e9857aec`.
- Automated validation workflow commit: `b554d65af2203bdc772f17be87d9b82d233e0c4d`.

The workflow should trigger automatically on these paths:

```text
HEE/tools/validate_incident.py
HEE/tests/**
HEE/fixtures/minimal-incident/**
.github/workflows/hee-validate.yml
```

It also runs weekly at `17 9 * * 1` and remains manually dispatchable.

### Missing or blocked

- Directly observed workflow run, jobs, logs, and artifact for commit `b554d65af2203bdc772f17be87d9b82d233e0c4d`.
- Canonical StegDB HEE schemas and protocol versioning under `StegVerse-Labs/StegDB#9`.
- Import/source-lock receipt proving which StegDB protocol revision HouseHold consumes.
- Production evidence ingestion and append-only custody implementation.
- Confidence-factor implementation approved by StegDB.
- Reviewed packet generation.
- External delivery remains intentionally unimplemented and unauthorized.

## Current Machine-Owned Continuation

Owner repository: `StegVerse-Labs/HouseHold`
Owner workflow: `.github/workflows/hee-validate.yml`

Triggers:

- push to `main` affecting validator, tests, fixture, or workflow;
- weekly schedule;
- manual dispatch.

Deterministic inputs:

- `HEE/fixtures/minimal-incident/incident.json`;
- referenced synthetic evidence, timeline, and findings;
- validator revision on the checked-out commit.

Persisted outputs:

```text
out/hee/minimal-incident/validation.json
out/hee/minimal-incident/validation.md
out/hee/minimal-incident/packet-plan.json
out/hee/minimal-incident/execution-receipt.json
```

Artifact name:

```text
hee-minimal-incident-validation-<github.run_id>
```

Fail-closed assertions:

- `send_authorized == false`;
- `repository_mutation_authorized == false`;
- `external_delivery_authorized == false`;
- fixture machine state is expected to be `REVIEW_REQUIRED` because unresolved uncertainty and human review remain.

## Validation Commands

```text
python -m unittest discover -s HEE/tests -p 'test_*.py'
python HEE/tools/validate_incident.py HEE/fixtures/minimal-incident --output-root out/hee
```

Hosted validation is complete only after direct inspection of the workflow run, job steps/logs, and uploaded artifact.

## Blockers and Machine-Observable Release Conditions

### Hosted CI observation

State: `RETRY`
Owner: `.github/workflows/hee-validate.yml`
Release condition: a completed Actions run exists for commit `b554d65af2203bdc772f17be87d9b82d233e0c4d`, all tests and validation steps pass, and the uploaded artifact contains all four expected files.

### Canonical protocol integration

State: `BLOCKED`
Owner: `StegVerse-Labs/StegDB#9`
Release condition: versioned artifact, confidence, custody, notification, packet-review, and source-lock contracts are committed and validated in StegDB.

### Human packet review

State: `REVIEW_REQUIRED`
Owner: named human authority for the specific incident.
Release condition: facts, recipient, remedy, attachments, uncertainty, and delivery method are reviewed and recorded. This does not automatically authorize delivery.

## Exact Next Tasks

1. `StegVerse-Labs/HouseHold/.github/workflows/hee-validate.yml`
   - observe the automatically triggered run;
   - inspect job steps and logs;
   - verify artifact identity and contents;
   - record run ID, artifact ID, hashes, and result in this handoff.

2. `StegVerse-Labs/StegDB#9`
   - install the canonical HEE artifact and packet contracts;
   - install evidence-confidence limitations and override receipt contract;
   - install custody-transition and notification contracts;
   - install a HouseHold source-lock/import receipt contract.

3. `StegVerse-Labs/HouseHold/HEE/`
   - consume the validated StegDB contracts through an overlay-only, version-locked import after task 2 completes.

## Archive Conditions

This work is not closed while hosted validation evidence and canonical StegDB integration remain incomplete. The conversation is not required for continuity because this handoff and `StegVerse-Labs/StegDB#9` preserve the execution state, but active work remains.

## Percentages

Required deliverables denominator: 16.

Completed and committed: 10.
Implemented but hosted-unvalidated: 3.
Missing or dependency-blocked: 3.

Developed files denominator: 12 required production or validation files for the current HouseHold slice.
Developed: 9.
Scaffolding/stubs: 0.
Missing required files: 3, consisting of the StegDB source-lock consumer, custody implementation, and reviewed packet generator.

Goal activation remains below completion because hosted CI evidence and canonical protocol integration are not yet verified.
