# Packet Eligibility Rules (v1)

This document defines what content can appear in escalation packets.

## Assertions vs Context

- Asserted Evidence: evidence that meets confidence threshold and is
  used to support factual statements in the letter.
- Context Evidence: evidence that exists but is below threshold. Context
  evidence is not included by default.

## Default Settings

- Only asserted evidence is included in packets.
- Context evidence is excluded unless explicitly enabled AND clearly
  labeled as non-asserted.

## Level thresholds

- Level 1: >= 0.40
- Level 2: >= 0.60
- Level 3: >= 0.75
- Level 4: >= 0.85

## Provenance Requirements

An artifact must have:
- artifact_id
- hash
- ingestion timestamp
- source type
- transformation log (even if empty)

If any are missing, the artifact must be treated as weak until corrected.
