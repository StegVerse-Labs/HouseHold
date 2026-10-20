# HEE Evidence Confidence v1

Status: canonical protocol candidate for `StegVerse-Labs/StegDB#9`.

## Purpose

This protocol defines transparent confidence metadata for evidence use decisions. It does not authenticate evidence, establish truth, determine admissibility, or provide a legal conclusion.

## Required distinctions

A conforming implementation must keep separate:

- the artifact and its bytes;
- provenance assertions;
- custody events;
- confidence assessment;
- packet review state;
- delivery authority.

No value in one category automatically proves another.

## Assessment states

- `UNASSESSED` — no score or band has been assigned.
- `REVIEW_REQUIRED` — factors exist but a score or use decision requires review.
- `ASSESSED` — a versioned process produced a score, band, factors, and limitations.

## Bands

When a numeric score is used, it is constrained to `[0, 1]`.

- `weak`: `0.00 <= score < 0.30`
- `moderate`: `0.30 <= score < 0.60`
- `strong`: `0.60 <= score < 0.80`
- `very-strong`: `0.80 <= score <= 1.00`

Bands are descriptive labels. They are not proof thresholds and do not create legal status.

## Factors and limitations

Every assessed record must include:

- a unique assessment identifier;
- algorithm or policy version;
- computation timestamp;
- observable factors;
- explicit limitations;
- prior assessment preservation when reassessed.

Permitted factors may include source acknowledgement, byte continuity, transformation disclosure, independent corroboration, or metadata availability. Implementations must not treat EXIF presence, filesystem modification time, a hash, or ingestion proximity as authentication by itself.

## Overrides

Manual or policy overrides require a separate immutable override receipt conforming to `evidence-confidence-override-receipt-v1.schema.json`.

An override must preserve:

- the prior assessment;
- the replacement assessment or use decision;
- the actor and authority basis;
- a rationale;
- the affected artifact;
- a timestamp;
- an explicit statement that the override does not authenticate evidence.

## Packet use

Packet inclusion rules must be declared by the consumer. StegDB does not define a universal legal or court threshold.

A packet generator must:

- expose included and excluded artifact references;
- expose unresolved uncertainty;
- preserve the confidence assessment version;
- require human review before delivery;
- keep `delivery_authorized` false in canonical packet manifests.

## Compatibility

Version `v1` is additive. Legacy `protocols/hee/evidence-confidence-policy.md` remains historical and is superseded for new integrations where it conflicts with this protocol, especially any implication that confidence alone establishes proof or court readiness.
