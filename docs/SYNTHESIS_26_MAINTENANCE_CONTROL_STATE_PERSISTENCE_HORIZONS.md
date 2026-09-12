# Synthesis 26 — Maintenance-Control State: Persistence Horizon, Reconstitution, and Authority

> **Question:** when one retained relation depends on auxiliary state that schedules, qualifies, resumes, authorizes, or audits maintenance, how long must that auxiliary state itself survive?

**Status:** bounded cross-case synthesis over already-grounded evidence. It introduces one project analytical term, `maintenance-control state`, and compares persistence horizons across existing cases. It does **not** claim one historical lineage or one universal metadata architecture across DRAM, NAND, SSD firmware, HDFS, or other distributed systems.

Grounded witnesses used here:

- [`Case 09 — DRAM CBR refresh-address internalization`](../cases/09-dram-cbr-refresh-address-internalization.md), especially [`evidence/09-dram-refresh-counter-initialization-test-deepening.md`](../evidence/09-dram-refresh-counter-initialization-test-deepening.md): a cyclic refresh-counter phase can be stateful and testable yet deliberately reinitialized at power-on;
- [`Case 78 — NAND bad-block management`](../cases/78-micron-nand-bad-block-marker-management.md), especially [`evidence/78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md`](../evidence/78-linux-mtd-2004-mirrored-versioned-bbt-deepening.md): a Flash-resident bad-block table can require restart persistence, mirroring, version currentness, and protected placement;
- [`Case 83 — HDFS BlockScanner`](../cases/83-apache-hdfs-block-scanner-checksum-verification.md), especially [`evidence/83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md`](../evidence/83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md): a resumable maintenance cursor can persist across restart, while loss falls back to replay and a clock-domain bug shows configured checkpoint policy need not equal effective checkpointing;
- [`Case 116 — HDFS DataNode maintenance state`](../cases/116-apache-hdfs-datanode-maintenance-state.md), especially [`evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md`](../evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md): retained administrative intent can survive restart through configuration while runtime replica-location evidence is re-observed;
- [`Case 15 — Intel SSD 320 power-loss durability`](../cases/15-intel-ssd320-power-loss-durability.md), especially [`evidence/15-intel320-2011-unsafe-shutdown-telemetry-deepening.md`](../evidence/15-intel320-2011-unsafe-shutdown-telemetry-deepening.md): a cumulative unsafe-shutdown count can retain event evidence without becoming a payload-durability verdict.

- [`Case 45 — DDR5 on-die ECC / ECS`](../cases/45-micron-ddr5-on-die-ecc-ecs.md), especially [`evidence/45-micron-ddr5-2022-2026-ecs-telemetry-validity-deepening.md`](../evidence/45-micron-ddr5-2022-2026-ecs-telemetry-validity-deepening.md): a latest scrub diagnostic summary can be mode-relative, threshold-filtered, explicitly resettable, and interpretable only within a reporting/configuration epoch.

The historical claims remain in those case/evidence records. The categories below are **engineering reconstruction**, not source vocabulary unless a source independently uses the same words.

---

## 1. Verdict

The repository should use `maintenance-control state` as a bounded umbrella for non-payload state whose role is to **schedule, qualify, resume, authorize, or audit work that preserves another retained relation**.

The term is useful only if it does not imply one persistence contract. The six witnesses immediately reject that shortcut:

```text
DRAM refresh counter
    -> regime-local cyclic phase
    -> reinitialize at power-on

HDFS scanner cursor
    -> restart-progress checkpoint
    -> resume if readable, replay if lost

Flash BBT
    -> restart-persistent qualification/currentness state
    -> mirror + version + protected placement

HDFS maintenance configuration
    -> retained policy/expiry
    -> reload policy, re-observe runtime embodiment evidence

SSD unsafe-shutdown counter
    -> cumulative event-history summary
    -> persists as telemetry, not as a durability verdict

DDR5 ECS report state
    -> mode-relative + threshold-filtered latest maintenance summary
    -> explicitly resettable; not a lifetime event ledger
```

Therefore the main rule is:

> **maintenance-control state must be classified by role, authority, failure consequence, and required persistence horizon; `metadata` or `checkpoint` alone is too coarse.**

This synthesis does not create an exhaustive taxonomy. It establishes a comparison discipline that survives the current counterexamples.

---

## 2. Claim discipline

Following [`METHOD.md`](METHOD.md) and [`../AGENTS.md`](../AGENTS.md):

- **H/P — historical / primary:** product, patent, project-source, and release-specific facts remain grounded in the individual cases;
- **E — engineering reconstruction:** `maintenance-control state`, persistence-horizon comparison, and the role matrix are project analytical tools;
- **A — functional analogy:** similarity of role does not establish shared mechanism or genealogy;
- **I — philosophical interpretation:** interpretation is limited to differentiated support conditions for technical persistence.

The synthesis specifically rejects the phrase `memory of memory` as a substitute for mechanism. Auxiliary state can be initialized, replayed, mirrored, reloaded, re-observed, or accumulated under sharply different contracts.

---

## 3. Why this is not Synthesis 24 again

[`SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md`](SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md) asks **what condition makes preservation work due**: access, elapsed time, capacity pressure, wear, failure, and so on.

This synthesis asks a different question:

> **What state does the preservation machinery itself need in order to know what to do, where to continue, what to trust, or what happened — and across which interruption must that state survive?**

Trigger regime and control-state horizon are therefore orthogonal. A deadline-driven DRAM regime can use volatile cyclic phase; a proactive scanner can use a restart checkpoint; a failure-management path can depend on a durable exclusion map.

> **same maintenance trigger ≠ same maintenance-control-state persistence horizon**

and

> **same persistence horizon ≠ same control authority**.

---

## 4. Comparison axes

For any proposed maintenance-control state, audit at least these axes:

| Axis | Question |
| --- | --- |
| **role** | Does the state carry phase, progress, qualification/currentness, policy/authority, event history, or runtime observation? |
| **target relation** | What retained payload or service relation does it help preserve? |
| **minimum horizon** | Must it survive only the active regime, process restart, device power cycle, media replacement, or the device/system lifetime? |
| **reconstitution path** | Initialize, replay, reload configuration, compare copies, reconstruct from payload, or re-observe participants? |
| **authority** | Advisory only, scheduling input, allocation gate, service-admission gate, or direct currentness selector? |
| **failure consequence** | Repeated work, delayed evidence, unsafe reuse/admission, loss of optimization, loss of diagnosis, or direct loss of recoverability? |
| **history semantics** | Current phase/currentness scalar, compact summary, or event-by-event history? |
| **durability evidence** | Interface/source contract only, or independently tested fault/power-loss behavior? |

A strong case should avoid filling unknown cells by analogy.

---

## 5. Regime-local phase — Case 09

The TI DRAM evidence shows a refresh counter with stateful sequential phase that is forced to zero at power-on and then increments across CAS-before-RAS refresh cycles. Motorola product documentation separately makes counter progression testable.

The key relation is:

```text
powered retention regime active
    -> counter phase matters for next-row coverage

power removed / new regime begins
    -> disclosed counter phase is reinitialized
```

The counter is constitutive maintenance state while refresh is active, yet cross-power durability is not part of the disclosed contract.

Therefore:

> **constitutive maintenance state ≠ durable checkpoint**

and

> **maintenance phase ≠ maintenance history**.

The counter's role is to distribute future work, not to preserve a complete record of prior refreshes.

---

## 6. Restart-progress checkpoint — Case 83

The HDFS scanner cursor has a different contract. It retains traversal position so a restarted scanner can continue rather than repeat the whole scan. If the cursor is absent or unreadable, the implementation creates a fresh iterator.

Thus cursor loss is not payload rollback. It changes the amount and ordering of future maintenance work:

```text
cursor survives
    -> resume later in traversal

cursor lost
    -> replay from fresh iterator
    -> earlier work repeated
    -> later blocks may wait longer for renewed verification evidence
```

This fixes two boundaries:

> **maintenance-progress loss ≠ payload loss**

but also

> **reconstructable/replayable control state ≠ consequence-free control state**.

The clock-domain defect in the intended periodic-save branch adds a second lesson: a documented/configured persistence policy can fail at implementation level.

> **retention policy intent ≠ effective retention behavior**.

---

## 7. Qualification/currentness map — Case 78

The Linux MTD Flash BBT carries a stronger form of authority. It records which blocks are excluded or reserved from ordinary use. The 2004 implementation can retain primary/mirror copies with version numbers, choose the higher readable version, and rewrite a missing or stale peer.

Here loss or stale selection can affect **admission of physical media**, not merely maintenance efficiency. That is why restart continuity and currentness discrimination matter.

But the stronger persistence requirement must not be overread:

> **mirrored/versioned control state ≠ transactional or power-fail-atomic update proof**.

And the version field is a currentness discriminator rather than an event log:

> **qualification currentness ≠ failure history**.

The BBT therefore differs from both the DRAM counter and HDFS cursor even though all three are non-payload state used by maintenance infrastructure.

---

## 8. Retained policy versus re-observed runtime evidence — Case 116

Hadoop 3.0.1 maintenance mode supplies a split persistence contract. Administrative state and expiry can be reloaded from the combined-host configuration after NameNode restart, while knowledge that a currently absent maintenance DataNode actually embodies a replica may require later DataNode return/re-registration.

So one maintenance relation can combine:

```text
retained policy source
    +
reconstituted in-memory policy object
    +
re-observed runtime embodiment evidence
```

This gives a strong boundary:

> **policy persistence ≠ persistence of every runtime fact used under that policy**.

It also blocks a common distributed-systems shortcut:

> **physical embodiment may survive ≠ coordinator presently knows or credits that embodiment**.

Re-observation is therefore a legitimate continuity mechanism alongside storage and replay.

---

## 9. Cumulative event-history summary — Case 15

Intel SSD 320 SMART C0h has yet another role. It is a lifetime cumulative count of unsafe/unclean shutdown events under the documented product semantics. It does not schedule the next NAND address or restore a scan cursor. It records a compact summary of past exposure.

The retained scalar lacks per-event timestamps, affected LBAs, outstanding-command state, PLP completion, and post-restart outcome.

Therefore:

> **cumulative event count ≠ per-event audit history**

and

> **event evidence ≠ preservation outcome**.

This matters because control/telemetry state can survive longer than the event it describes while remaining advisory rather than directly authoritative over payload currentness.

The product documentation also leaves the exact counter-update persistence mechanism open, so:

> **documented cumulative semantics ≠ demonstrated power-fail-atomic telemetry update**.

---


## 9A. Resettable, threshold-filtered diagnostic summary — Case 45

DDR5 ECS adds a persistence horizon not represented by the first five witnesses. Micron's 2022 product-core record exposes a correction summary whose interpretation depends on count mode and threshold, whose maximum-row component compresses many visited rows into one retained diagnostic relation, and whose counters/report registers can be explicitly reset.

The later Linux CXL ECS control surface independently exposes row/code-word count mode, reporting threshold, and counter reset as host-visible policy where supported.

This means that the retained state is neither a lifetime event count nor an append-only event log:

```text
ECS corrective work
    -> may repair array state

reporting mode + threshold
    -> define what later count means / what becomes visible

latest report registers
    -> retain bounded diagnostic summary

reset / later reporting boundary
    -> retire or replace that summary
```

Therefore:

> **summary persistence != repair persistence**

> **latest diagnostic state != complete maintenance history**

> **telemetry reset != rollback of earlier corrective work**.

This also sharpens the comparison with Case 15. A cumulative lifetime unsafe-shutdown count and a resettable ECS summary can both be long enough-lived to inform later diagnosis while having different history semantics. `counter` is therefore not a sufficient persistence-horizon category.

The project term `reporting/configuration epoch` is used only to describe the validity interval over which a count mode/threshold and its accumulated summary can be interpreted together. It is not Micron or JEDEC historical vocabulary, and this synthesis does not claim the reporting registers survive power removal.

The Case 45 self-refresh/PASR deepening now adds a transition-relative refinement. Micron states that ordinary self-refresh entry/exit does not reset ECS transparency counters/registers, while the same transition resets the Same Bank Refresh internal bank counter; ECS interval timing may restart after exit. Under PASR, the counters can remain while the full-array evidential interpretation becomes invalid enough that known-data initialization plus counter reset is required before a later accurate full-array scrub.

Therefore the synthesis must add two rules:

> **same transition != same persistence horizon for every maintenance-control state**

and:

> **retained control state != retained validity of the proposition that state once supported**.

This is still not a cross-power claim. It makes the comparison more precise by classifying the transition boundary and the evidence-validity domain alongside the state itself.

---

## 10. Persistence horizon ≠ authority

The six cases show that persistence duration and decision authority are independent axes.

- A short-lived DRAM counter phase can be essential to full-array coverage.
- A restart-persistent HDFS cursor can be lost with replay rather than unsafe payload admission.
- A Flash BBT can gate whether a block is eligible for ordinary use.
- An HDFS maintenance config can retain policy while runtime replica evidence is deliberately rebuilt conservatively.
- A lifetime SMART count can persist for diagnosis without selecting payload currentness.
- A resettable ECS summary can persist beyond one corrective operation while remaining filtered, mode-relative diagnostic evidence rather than a complete repair history.

Therefore neither of these shortcuts is safe:

> **long-lived metadata = more authoritative metadata**

> **short-lived/reconstructable metadata = less important metadata**.

Authority must be reconstructed from the bounded mechanism.

---

## 11. Reconstitution is part of retention architecture

A maintenance-control relation need not survive by preserving one unchanged representation. Across the witnesses, continuity can be produced by:

- deterministic initialization;
- replay of maintenance work;
- mirror/version comparison and repair;
- configuration reload;
- participant re-observation;
- cumulative update of compact telemetry.

This gives a useful cross-case rule:

> **persistence can be provided by retained representation, by controlled reconstitution, or by a composition of both.**

That is compatible with [`SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md`](SYNTHESIS_25_RECURRENCE_REFRESH_TERMINOLOGY.md): reconstitution can preserve an operational relation without implying that one physical token or one exact in-memory object survives.

The rule is analytical. It is not a claim that the historical systems shared vocabulary or design lineage.

---

## 12. Checkpoint ≠ certificate

The cases also expose why `checkpoint` is dangerous as a generic word.

- The HDFS scanner cursor says where traversal had reached, not that every earlier block verified successfully.
- The DRAM counter test can expose bounded enumerator progression, not certify all future refresh deadlines.
- The BBT version says which readable table is newer under the implementation rule, not why each block was retired or that the whole update was crash-atomic.

Therefore:

> **retained progress/currentness evidence ≠ complete correctness certificate**.

A maintenance-control record should be read according to the exact proposition it supports.

---

## 13. Failure consequences differ by role

Losing maintenance-control state can have qualitatively different consequences:

| State role | Bounded loss/staleness consequence |
| --- | --- |
| cyclic phase | coverage sequence restarts / must be re-established within the active regime |
| traversal checkpoint | maintenance replay and delayed later coverage |
| qualification/currentness map | risk of using or trusting an inadmissible physical resource if no safe reconstruction path exists |
| retained policy | desired administrative relation may be lost unless reloadable; runtime reliance may still require fresh observation |
| event-history summary | diagnostic/audit information can be incomplete without directly proving payload loss |

This is why `control metadata corrupted` is not a sufficient failure description.

---

## 14. Functional analogies and stop conditions

The cross-case comparison is functional only.

- DRAM counter state is not a filesystem checkpoint.
- A Flash BBT mirror is not consensus replication.
- HDFS configuration reload is not a device firmware journal.
- SMART event telemetry is not repair-history currentness.
- Re-observed replica location is not proof that the bytes became physically rewritten.

No genealogy among these mechanisms is asserted.

A fresh search of `tmzncty/computing-archaeology` for the combined refresh-counter / BBT / scanner-cursor / unsafe-shutdown relation found no dedicated cross-technology study to reuse. Broad histories of DRAM control logic, NAND BBTs, SMART telemetry, or HDFS maintenance mechanisms remain companion-repository work. This document keeps only the retention-specific comparison.

---

## 15. Philosophical interpretation — bounded

The exact technical fact is that preservation can depend on auxiliary state whose required lifetime differs from both the payload and from other control state in the same system.

The narrow conceptual payoff is:

> **technical persistence is often supported by a stratified set of states, some retained, some replayed, some reinitialized, and some re-observed. Continuity of the higher-level relation does not require every supporting representation to persist in the same way.**

This blocks both extremes: persistence is not merely untouched material survival, but neither does every support relation need infinite recursive preservation.

The interpretation stops there. The evidence does not justify `machines remember how to remember`, a universal theory of metadata, or a claim that every maintenance process needs its own durable history.

---

## 16. Rejected strong claims

- **`maintenance-control state is always durable metadata` — rejected.** Case 09 directly supplies a regime-local, power-on-initialized counter phase.
- **`reconstructable state is unimportant` — rejected.** Replay can consume maintenance budget; re-observation can change what embodiments may be credited.
- **`persisted state is automatically authoritative` — rejected.** SMART event history can be persistent yet advisory; HDFS policy can persist while runtime replica evidence is rebuilt.
- **`version/currentness state is history` — rejected.** The BBT version selects the newer representation without preserving a bad-block event ledger.
- **`checkpoint means verified correctness` — rejected.** The HDFS cursor and DRAM counter-test boundaries contradict this.
- **`duplicate control state implies consensus or crash atomicity` — rejected.** The BBT mirror is a local reconciliation mechanism with explicit fault limits.
- **`control-state loss implies payload loss` — rejected as a universal rule.** Cursor loss can cause replay; telemetry loss can lose diagnosis; other control-state failures can be much more severe.
- **`payload survival implies control-state survival` — rejected.** A physical replica can survive while a restarted NameNode has not yet re-observed it.
- **`one transition gives every maintenance-control state the same lifetime` — rejected.** DDR5 self-refresh entry/exit preserves ECS transparency state while resetting REFsb bank phase, and PASR can preserve bits while invalidating their prior full-array evidential scope.

---

## 17. Research consequences

Future cases that introduce auxiliary preservation state should explicitly answer:

1. What proposition does the state encode?
2. What decision consumes it?
3. What is its minimum required persistence horizon?
4. Can it be reconstructed, replayed, or re-observed?
5. What happens while it is missing or stale?
6. Does it encode phase/currentness, a compact summary, or actual history?
7. What evidence establishes its own durability under the relevant failure model?
8. Does a duplicate copy add redundancy, currentness discrimination, atomicity, or only risk reduction?

This gives future Flash/SSD and distributed-storage cases a common checklist without forcing them into one mechanism.

---

## Sources and evidence custody

This synthesis introduces no new historical floor. Historical claims are inherited from the grounded evidence records listed at the top:

- TI US4653030A and Motorola 1989 *Memory Data* through Case 09 evidence;
- Linux MTD 2004 documentation/CVS source through Case 78 evidence;
- Apache HDFS-7430, HDFS-12209, and Hadoop 2.7.3 source through Case 83 evidence;
- Apache Hadoop 3.0.1 documentation/source/tests through Case 116 evidence;
- Intel SSD 320 September/March 2011 manufacturer documents through Case 15 evidence.
- Micron DDR5 SDRAM Product Core Data Sheet Rev. D 10/2022 plus official Linux EDAC/CXL ECS documentation through the Case 45 deepening evidence.

For exact URLs, page anchors, version tags, and evidence grades, use the linked case/evidence records rather than treating this synthesis as a substitute source.
