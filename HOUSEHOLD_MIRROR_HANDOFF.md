# HouseHold Mirror Handoff

## Status

HouseHold is the real-world proving ground for the Household Escalation Engine (HEE). This record preserves decisions, completed work, blockers, ownership, validation requirements, and the exact continuation scope.

Current continuation state:

```text
incident documentation
→ facts/findings separation
→ evidence organization
→ custody/provenance separation
→ escalation packet structure
→ repository guidance
→ synthetic fixture
→ read-only validator and dry-run planner
→ manual read-only CI workflow committed
→ CI run and artifact observation pending
→ StegDB protocol registration
```

## Decisions Preserved

1. StegDB is the canonical protocol and schema authority.
2. HouseHold contains real incident state and implementation evidence.
3. HEE connects canonical rules to HouseHold workflows without replacing professional or human judgment.
4. Protocols live once in StegDB; incidents reference rather than redefine them.
5. Facts belong in `timeline/`; interpretation, constraints, impacts, risks, and remedies belong in `findings/`.
6. Evidence, provenance, custody, confidence, and review state are distinct concepts.
7. Confidence metadata is decision support, not proof, authentication, or a legal conclusion.
8. Custody events are append-only and do not independently establish truth, ownership, authority, or liability.
9. Originals must not be silently overwritten; hashes, transformations, and references must remain traceable.
10. Generated material remains draft until human review.
11. Automation must fail clearly and must not send letters, notifications, or evidence merely because validation succeeds.
12. Public fixtures and CI data must be synthetic or safely redacted.
13. Canonical synchronization must be overlay-only and non-destructive.

## Durable Records

### HouseHold

- `HOUSEHOLD_MIRROR_HANDOFF.md`
- `README.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `_new-incident-template/README.md`
- `HEE/README.md`
- `HEE/household-escalation-engine.md`
- `HEE/engine/packet-spec.md`
- `HEE/intake/intake_questionnaire.md`
- `HEE/fixtures/minimal-incident/`
- `HEE/tools/validate_incident.py`
- `HEE/tests/test_validate_incident.py`
- `.github/workflows/hee-validate.yml`

### StegDB

- Active canonical task: `StegVerse-Labs/StegDB#9`
- Scope: artifact records, confidence factors and limitations, custody transitions, notifications, packet review state, and overlay-only canonical consumption.

## Completed Work

- Established StegDB/HEE/HouseHold authority boundaries.
- Established facts-versus-analysis and evidence/provenance/custody distinctions.
- Committed contribution, privacy, incident-template, and HEE guidance.
- Added a synthetic fixture containing no real personal or incident data.
- Added a standard-library-only validator that checks required fields, safe relative paths, referenced files, review state, and unresolved uncertainty.
- Added a dry-run packet planner that always sets `send_authorized` to `false`.
- Added four unit tests covering success, missing evidence, send prohibition, and output isolation.
- Added a `workflow_dispatch`-only GitHub Actions workflow with `contents: read` permission.
- The workflow runs tests, validates only the synthetic fixture, verifies expected outputs, and uploads the outputs without committing them.

## Commit Record

- Initial handoff: `66deb63631ed1d1213c82504e3cc13810baae1ad`
- Guidance:
  - `CONTRIBUTING.md`: `cc31bbb944df872c5192aa566017712d5fdd0cc3`
  - `SECURITY.md`: `505f55ea7f968940b1e856c841aaad417c9b3976`
  - `_new-incident-template/README.md`: `2cbc7387e589609be968fb0dc402d75581a2d4c5`
  - `HEE/README.md`: `f25e2225e262746023069974c88c3c113a305341`
- Validator: `3eea79ece5887d8ca6dd64bdbfac05e27fbbc0b0`
- Fixture:
  - manifest: `bdffcfdef566d4bb7a853aa2a43e3ab9da84d477`
  - evidence: `94c9b7fd51cd66b5dfb789d0b12b4fc47d3abd2a`
  - timeline: `6c6b615011477860dc610319340a116c665b0b12`
  - findings: `6002bef02e8e37ef4c17e74c7a42be9fdcee974a`
- Tests: `59ad28f083a1e364a95cea9eaded3617b6acc16a`
- Read-only validation workflow: `09109c2ecccd0ee63f565648b59abe031112ba74`

## Local Validation Evidence

```text
python -m unittest discover -s HEE/tests -p 'test_*.py'
Ran 4 tests
OK

python HEE/tools/validate_incident.py HEE/fixtures/minimal-incident --output-root out/hee
status: PASS
errors: 0
warnings: 1 (unresolved uncertainty present)
evidence files validated: 1
supporting files validated: 2
send_authorized: false
```

Observed deterministic fixture hashes:

- manifest: `f16410ece35f6a0bc625d38d6f7e129c1281d1f850dd416cb412c0f44f20b292`
- evidence: `c842bbcbdf35a8429e2dfb500c5dcf6a4a8b304ba6ddea2199ceab18ff71395e`
- timeline: `2517e22897b792d8d3a39d57c454171a33c87d227a9b720935fd9bfefb3fa053`
- findings: `bb092a49c29bcbdb04b9e4ead21dab00dc9553982f16871074235e13ca347aea`

Generated outputs:

```text
out/hee/minimal-incident/validation.json
out/hee/minimal-incident/validation.md
out/hee/minimal-incident/packet-plan.json
```

Outputs are written outside the fixture and do not modify source evidence.

## Non-Authoritative Drafts

These paths remain non-authoritative unless independently found and validated on the default branch:

- `docs/STRUCTURE.md`
- `.github/CODEOWNERS`
- `.github/pull_request_template.md`
- `.github/ISSUE_TEMPLATE/*`
- `HEE/escalation-level-spec.md`
- `HEE/letter-template.md`
- `HEE/attachments-template.md`
- `HEE/tools/hee.py`
- `HEE/engine/hee_engine.py`
- `HEE/engine/__init__.py`
- `.github/workflows/hee-generate.yml`

Do not copy old drafts blindly.

## Known Blockers and Risks

- The committed validation workflow has not yet been dispatched and observed.
- Artifact identity and contents have not yet been verified from a real Actions run.
- Confidence scoring semantics require canonical StegDB review before ecosystem use.
- Filesystem modification time and EXIF presence are not reliable truth indicators.
- Generated letters and packets require human review before delivery.
- Existing incidents may require additive, non-destructive migration.
- Real incident evidence must not enter fixtures, logs, or workflow artifacts without explicit privacy review.

## Exact Next Authorized Task

```text
Dispatch `.github/workflows/hee-validate.yml`, observe the run, verify the uploaded artifact, and record the run evidence here.
```

Done when:

- one real workflow run is complete;
- the four tests pass;
- synthetic fixture validation reports `PASS`;
- artifact `hee-minimal-incident-validation` contains `validation.json`, `validation.md`, and `packet-plan.json`;
- `packet-plan.json` records `send_authorized: false`;
- run ID, workflow commit SHA, artifact ID/name, result, and verified hashes are added to this handoff.

No evidence ingestion, confidence scoring, letter generation, repository mutation, or external delivery is authorized in this step.

## Ownership and Permitted Continuation Scope

- HouseHold owner: next authorized HouseHold/HEE build session or StegVerse entity assigned to `StegVerse-Labs/HouseHold`.
- StegDB owner: next authorized session or entity assigned to `StegVerse-Labs/StegDB#9`.
- Permitted HouseHold scope: dispatch and observe the read-only synthetic workflow, verify artifacts, record evidence, and make additive exact-file corrections if validation fails.
- No authority is granted to publish private evidence, send communications, notify counterparties, claim legal validity, or replace directories.

## Pending Validation

- Observe the real GitHub Actions run.
- Verify artifact contents and hashes.
- Verify canonical references before claiming StegDB integration.
- Preserve the distinction between structural validation and truth/authenticity claims.

## Archive Readiness

All session-specific decisions, completed work, blockers, remaining tasks, active ownership, validation requirements, and continuation boundaries are preserved here and in `StegVerse-Labs/StegDB#9`.
