# Synthesis Index

This file is a compact navigation layer for cross-case synthesis in `technical-retention`. It does **not** replace [`CASE_INDEX.md`](../CASE_INDEX.md), which remains authoritative for case maturity, or [`ROADMAP.md`](../ROADMAP.md), which remains authoritative for staged research priorities.

Synthesis documents compare relations already grounded in individual cases. They do not silently upgrade functional analogy into historical continuity or invention genealogy.

## Current bounded syntheses

| Synthesis | Status | Main question |
| --- | --- | --- |
| [`06 — Flash Read Path vs Renewal`](SYNTHESIS_06_FLASH_READ_PATH_VS_RENEWAL.md) | bounded | How do reader-side adaptation, ECC/retry, logical recoverability, powered maintenance, and physical renewal differ? |
| [`07 — Coded Recoverability / Repair Margin`](SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md) | bounded | How do algebraic reconstructability, degraded service, repair scope, and restored redundancy margin differ? |
| [`08 — Proactive Integrity / Repair Margin`](SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md) | bounded | How do presence, integrity evidence, verification coverage, discovery, repair-source qualification, and restored redundancy differ? |
| [`09 — Distributed Coded Service / Repair / Placement`](SYNTHESIS_09_DISTRIBUTED_CODED_SERVICE_REPAIR_PLACEMENT.md) | bounded | How do coded availability, request-time reconstruction, durable repair, placement restoration, and representation handoff differ? |
| [`10 — Mutable EC Currentness / Retirement / Repair`](SYNTHESIS_10_MUTABLE_EC_CURRENTNESS_RETIREMENT_REPAIR.md) | bounded | How do fragment presence, version coherence, durability, service admissibility, old-version retirement, and repair convergence differ? |
| [`11 — Access Disturbance / Maintenance`](SYNTHESIS_11_ACCESS_DISTURBANCE_MAINTENANCE.md) | bounded | How can a successful access create immediate restore work or consume future retention margin elsewhere? |
| [`12 — Integrity-Qualified Coded Recovery`](SYNTHESIS_12_INTEGRITY_QUALIFIED_CODED_RECOVERY.md) | bounded | How do coded sufficiency, integrity qualification, fault localization, repair-source admissibility, and later revalidation interact? |
| [`13 — Durability Handoff / Persistence Domain`](SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md) | bounded | How do completion, intermediate residence, ordering, persistence-boundary arrival, power-fail protection, and recoverability differ? |
| [`14 — Distributed Ack / Visibility / Durability`](SYNTHESIS_14_DISTRIBUTED_ACK_VISIBILITY_DURABILITY.md) | bounded | How do replica progress, protocol completion, client acknowledgement, reader visibility, and durability differ? |
| [`15 — Logical Identity / Embodiment Replacement`](SYNTHESIS_15_LOGICAL_IDENTITY_EMBODIMENT_REPLACEMENT.md) | bounded | What must remain invariant when the physical embodiment serving a stable logical identity changes? |
| [`16 — Replica Currentness as a Retained Relation`](SYNTHESIS_16_REPLICA_CURRENTNESS_RETAINED_RELATION.md) | bounded | Why does surviving replica state not by itself establish currentness or authority? |
| [`17 — Replicated-Log Suffix / Currentness / Visibility`](SYNTHESIS_17_REPLICATED_LOG_SUFFIX_CURRENTNESS_VISIBILITY.md) | bounded | How do surviving suffixes, qualified replicas, committed prefixes, visibility, truncation authority, and convergence differ? |
| [`18 — Consensus Snapshot Continuation`](SYNTHESIS_18_CONSENSUS_SNAPSHOT_CONTINUATION.md) | bounded | What continuation state must survive when committed log history is compacted into a snapshot? |
| [`19 — Log-Structured Tablet Recovery`](SYNTHESIS_19_LOG_STRUCTURED_TABLET_RECOVERY.md) | bounded | How do redo history, volatile materialization, immutable files, live membership, replay boundaries, and reclamation differ? |
| [`20 — Filesystem Crash-Retention Layers`](SYNTHESIS_20_FILESYSTEM_CRASH_RETENTION_LAYERS.md) | bounded | How do live visibility, crash-admissible state, explicit durability, replay authority, cleanup obligations, and reclamation differ? |
| [`21 — Lagging Read-Replica Freshness Authority`](SYNTHESIS_21_LAGGING_READ_REPLICA_FRESHNESS_AUTHORITY.md) | bounded | How is a minimum acceptable read frontier transported and enforced when a read replica can lag? |
| [`22 — Erase / Invalidation / Sanitization / Verification`](SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md) | bounded | How do logical invalidation, physical erase, reuse, sanitization objective, completion, and independent verification differ? |
| [`23 — Retention Interpreter / Access Apparatus`](SYNTHESIS_23_RETENTION_INTERPRETER_ACCESS_APPARATUS.md) | bounded | Why do material survival, restart legibility, format interpretation, reader capability, and service admission remain separate? |
| [`24 — Retention Maintenance Trigger Regimes`](SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md) | bounded | What makes preservation work due, and how do trigger, opportunity, progress, execution, and completion differ? |
| [`25 — Recurrence / Refresh Terminology`](SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md) | bounded | How can identity-through-re-instantiation be compared without collapsing period terms such as recirculation, regeneration, rewrite, and refresh? |
| [`26 — Maintenance-Control-State Persistence Horizons`](SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md) | bounded | How long must auxiliary maintenance state survive, and when is reset, replay, rebind, or reconstruction safer than persistence? |
| [`27 — Retention-Policy Evidence Validity`](SYNTHESIS_27_RETENTION_POLICY_EVIDENCE_VALIDITY.md) | bounded | When is a sensor, proxy, retained profile, status field, or error observation sufficiently representative and current to drive maintenance policy? |
| [`28 — Reclamation Authority After Retirement`](SYNTHESIS_28_RECLAMATION_AUTHORITY_AFTER_RETIREMENT.md) | bounded | What authority, cleanup obligations, preservation work, and closure evidence sit between logical retirement and reuse? |
| [`29 — Maintenance Observability: Schedule, Admission, Coverage, Accounting, and Closure`](SYNTHESIS_29_MAINTENANCE_OBSERVABILITY_COVERAGE_ACCOUNTING.md) | **bounded / current** | What is an observer actually entitled to infer from maintenance configuration, progress, counters, events, and completion surfaces? |
| [`29 — Semantic Persistence and Restart Continuation`](SYNTHESIS_29_SEMANTIC_PERSISTENCE_AND_RESTART_CONTINUATION.md) | bounded | When a usable relation survives interruption, what survives: representation, meaning, progress, relation, or restart authority? |
| [`30 — Maintenance Coverage: Local Work, Domain Completion, and Completion Evidence`](SYNTHESIS_30_MAINTENANCE_COVERAGE_COMPLETION_EVIDENCE.md) | bounded | What connects local maintenance actions to protected-domain coverage, completion evidence, and renewed future obligation? |

### Numbering note

The repository currently contains **two files titled `Synthesis 29`**. This index preserves their existing filenames and titles rather than silently renumbering one and risking broken cross-references. A future repository-wide renumbering should be treated as a separate navigation cleanup with link auditing, not folded into an unrelated research slice.

## Focused synthesis deepenings

- [`Synthesis 09 deepening — HACFS 2015 adaptive code conversion and the crash-safety evidence boundary`](../evidence/synthesis09-hacfs-2015-adaptive-code-conversion-evidence-boundary-deepening.md) — FAST ’15 provides an independent adaptive-EC transition witness with explicit per-file `coding state`, background `upcode`/`downcode`, and parity-only representation change, but the inspected publication does not establish transaction ordering, conversion-progress persistence, restart/resume semantics, target-code validation, or old-parity retirement gates. The bounded result is `dynamic code conversion documented != crash-safe representation handoff documented`; this advances but deliberately does not close the roadmap’s failed/asynchronous redundancy-mode-conversion debt.
- [`Synthesis 29 deepening — maintenance-history loss, future control, and distinguishability`](../evidence/synthesis29-maintenance-history-loss-control-state-deepening.md) — grounded Cases 38 and 83 now distinguish **representational collapse** (S3700 AFh saturation / event-class omission) from **premature deletion of decision-bearing completion history** (HDFS verification-log rollover). The bounded result is `maintenance history retained != exact history retained`, and, separately, `historical record != retrospective-only state`: recent completion evidence can be consumed by future maintenance eligibility. This closes only the saturation / premature-rollover portion of Synthesis 29's telemetry-loss debt; reset and wrap counterexamples remain open.

## Synthesis audits

The earlier audit series stress-tests broad provisional theses and records negative results rather than merely accumulating supporting examples:

- [`Audit 01 — Maintained Persistence`](SYNTHESIS_AUDIT_01_MAINTAINED_PERSISTENCE.md)
- [`Audit 02 — Temporal Transport`](SYNTHESIS_AUDIT_02_TEMPORAL_TRANSPORT.md)
- [`Audit 03 — Addressability`](SYNTHESIS_AUDIT_03_ADDRESSABILITY.md)
- [`Audit 04 — Privileged Location`](SYNTHESIS_AUDIT_04_PRIVILEGED_LOCATION.md)
- [`Audit 05 — Technical Forgetting`](SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md)
- [`Audit 06 — Maintenance Visibility`](SYNTHESIS_AUDIT_06_MAINTENANCE_VISIBILITY.md)
- [`Counterexample Ledger`](SYNTHESIS_COUNTEREXAMPLE_LEDGER.md)

## Methodological boundary

Use this index to find comparisons, then return to the individual cases/evidence packets for historical claims. In particular:

```text
cross-case category
    != historical actor vocabulary
    != shared physical mechanism
    != demonstrated genealogy
```

For broader technical genealogy, follow [`../RELATED_REPOS.md`](../RELATED_REPOS.md) and reuse `tmzncty/computing-archaeology` where an engineering-history treatment already exists.
