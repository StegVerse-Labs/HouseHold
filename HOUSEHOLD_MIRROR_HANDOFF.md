# HouseHold Mirror Handoff

## Active Goal

Goal ID: `HOUSEHOLD-HEE-ACTIVATION-001`

Activate a governed Household Escalation Engine path that validates incident structure, preserves evidence boundaries, consumes commit-pinned StegDB protocols, produces machine-owned receipts, and cannot silently authorize repository mutation or external delivery.

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
- `HEE/canonical/stegdb-hee-v1-import.json`
- `HEE/tools/verify_stegdb_hee_import.py`
- `.github/workflows/hee-validate.yml`
- StegDB source handoff: `StegVerse-Labs/StegDB/STEGDB_MIRROR_HANDOFF.md`
- StegDB tasks: issues `#9` and `#10`

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
10. Canonical synchronization is commit-pinned, hash-bound, overlay-only, and non-destructive.

## Execution Inventory

### Complete and committed

- Repository guidance and privacy boundary.
- Synthetic incident fixture.
- Read-only incident validator.
- Dry-run packet planner.
- Machine execution receipt and duplicate-execution key.
- Five unit tests.
- Push, schedule, and manual CI triggers.
- Read-only workflow permissions and artifact upload.
- Commit-pinned StegDB HEE import configuration.
- Remote exact-byte import validator.
- Generated HouseHold canonical import validation receipt.
- Generated HouseHold source-lock receipt.
- CI assertions that imported source is overlay-only and does not modify incident data.

### Commit record

- Incident validator: `340d3755dc261c63dc976f105e20b8e419c8da09`
- Five-test suite: `a8c80fdc2edfbeeacced54c42c81b3c8e9857aec`
- Automated fixture workflow: `b554d65af2203bdc772f17be87d9b82d233e0c4d`
- StegDB import config: `45d342c12b1ead5dc0908a5139275896d6561e32`
- StegDB import validator: `6ccf6f2d3813f624c520139591b65697865da24c`
- Integrated fixture + canonical workflow: `3c2b967c22e9abc91b525bf53ab16270b2b15a00`

### Canonical source pin

```text
source repository: StegVerse-Labs/StegDB
source commit: eb488813c4cf8b6baa76609f2aab90d7e6126fcd
package manifest: protocols/hee/hee-v1-package.json
required canonical files: 7
```

The import validator:

- fetches exact bytes from the pinned commit;
- validates the package file list and fail-closed boundary flags;
- validates JSON documents parse;
- calculates SHA-256 for every imported protocol;
- emits a duplicate execution key;
- emits `COMPLETE`, `BLOCKED`, `RETRY`, `REVIEW_REQUIRED`, or `FAILED`;
- emits the next executable task;
- keeps repository mutation, incident mutation, and external delivery unauthorized.

### Implemented but hosted-unvalidated

- The current workflow revision has not yet produced a directly inspected Actions run, job log, or artifact through the available status surface.
- Combined-status lookup for commit `3c2b967c22e9abc91b525bf53ab16270b2b15a00` returned no status entries.

### Missing or blocked

- Hosted StegDB canonical-package validation receipt inspection.
- Hosted HouseHold exact-byte import and source-lock receipt inspection.
- Production append-only custody-event implementation.
- Reviewed packet generation.
- External delivery remains intentionally unimplemented and unauthorized.

## Machine-Owned Continuation

Owner repository: `StegVerse-Labs/HouseHold`
Owner workflow: `.github/workflows/hee-validate.yml`

Triggers:

- push to `main` affecting the incident validator, import validator, source config, tests, synthetic fixture, or workflow;
- weekly schedule at `17 9 * * 1`;
- manual dispatch.

Deterministic inputs:

- synthetic HouseHold fixture;
- commit-pinned StegDB import configuration;
- exact remote bytes from the pinned StegDB commit.

Persisted outputs:

```text
out/hee/minimal-incident/validation.json
out/hee/minimal-incident/validation.md
out/hee/minimal-incident/packet-plan.json
out/hee/minimal-incident/execution-receipt.json
out/hee/canonical/import-validation.json
out/hee/canonical/household-source-lock.json
```

Artifact:

```text
hee-validation-<github.run_id>
```

Fail-closed assertions:

- incident `send_authorized == false`;
- incident `repository_mutation_authorized == false`;
- incident `external_delivery_authorized == false`;
- canonical import `repository_mutation_authorized == false`;
- canonical import `external_delivery_authorized == false`;
- canonical import `incident_data_modified == false`;
- source lock `overlay_only == true`;
- source lock contains exactly seven canonical protocol hashes.

## Validation Commands

```text
python -m unittest discover -s HEE/tests -p 'test_*.py'
python HEE/tools/validate_incident.py HEE/fixtures/minimal-incident --output-root out/hee
python HEE/tools/verify_stegdb_hee_import.py --config HEE/canonical/stegdb-hee-v1-import.json --output-dir out/hee/canonical
```

Hosted validation is complete only after direct inspection of the run, job steps/logs, and uploaded artifact.

## Blockers and Machine-Observable Release Conditions

### StegDB package validation

State: `RETRY`
Owner: `StegVerse-Labs/StegDB/.github/workflows/stegdb-central.yml`
Release condition: the HEE validation job reports `COMPLETE` and its artifact contains a valid `meta/hee_v1_protocol_validation.json` for the pinned package.

### HouseHold import validation

State: `RETRY`
Owner: `.github/workflows/hee-validate.yml`
Release condition: a completed run fetches all seven pinned files, records their SHA-256 values, reports `COMPLETE`, and uploads both import receipts.

### Human packet review

State: `REVIEW_REQUIRED`
Owner: named human authority for the specific incident.
Release condition: facts, recipient, remedy, attachments, uncertainty, and delivery method are reviewed and recorded. This does not automatically authorize delivery.

## Exact Next Tasks

1. `StegVerse-Labs/StegDB/.github/workflows/stegdb-central.yml`
   - observe the HEE package validation job and artifact.

2. `StegVerse-Labs/HouseHold/.github/workflows/hee-validate.yml`
   - observe exact-byte import, fixture validation, source-lock generation, and combined artifact.

3. `StegVerse-Labs/HouseHold/HEE/`
   - after hosted source-lock validation, implement append-only custody events against the canonical custody schema.

4. `StegVerse-Labs/HouseHold/HEE/`
   - implement reviewed packet generation only after custody state and source lock are valid.

## Archive Conditions

Active work remains until hosted StegDB validation, hosted HouseHold import validation, artifact inspection, append-only custody implementation, and reviewed packet generation are completed or formally superseded.

## Percentages

Task denominator: 20 deliverables.

- complete and committed: 15;
- implemented but hosted-unvalidated: 2;
- missing or blocked: 3.

Developed-file denominator: 14 required HouseHold files for the current activation slice.

- developed: 12;
- scaffolding/stubs: 0;
- missing: 2, consisting of append-only custody implementation and reviewed packet generation.

Goal activation remains incomplete because hosted evidence and the final two production capabilities are not yet verified.
