# Case 141 — PostgreSQL Replication Slots: WAL Retention Frontier and Continuation Admission

**Status:** grounded  
**Claim layer:** historical record + engineering reconstruction + bounded functional analogy + bounded philosophical interpretation  
**Primary regime:** PostgreSQL 9.4 replication-slot introduction/release (2014), PostgreSQL 13 resource-bound evolution (2020), and PostgreSQL 17 logical failover-slot synchronization (2024)
**Evidence records:**

- [`../evidence/141-postgresql-2014-2020-replication-slot-wal-retention-grounding.md`](../evidence/141-postgresql-2014-2020-replication-slot-wal-retention-grounding.md)
- [`../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md`](../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md)

## Summary

This case asks a narrow distributed-log retention question:

> **Can history that is no longer needed for the primary's immediate current state remain non-reclaimable because a lagging or disconnected future consumer still needs it, and what happens when the primary later gains authority to sacrifice that continuation relation to bound local storage use?**

PostgreSQL 9.4 supplies a clean mechanism. A **replication slot** is persistent control state. Its `restart_lsn` records the oldest WAL position that might still be required by the slot's consumer. PostgreSQL aggregates slot requirements into the WAL-removal horizon, so old WAL remains available even while the consumer is not currently connected.

The relevant retained objects are therefore not one thing:

```text
primary current database state
        != replication-slot control state
        != consumer-need frontier (`restart_lsn`)
        != retained WAL history governed by that frontier
        != current connection/activity state
```

The released 9.4 documentation also exposes a cost: replication slots retain only history known to be needed, but the original design had no built-in way to bound the disk space that slot-retained `pg_xlog` could consume.

PostgreSQL 13 makes that conflict explicit. `max_slot_wal_keep_size` can cap how much WAL a slot is allowed to protect. The later `wal_status` state machine distinguishes `reserved`, `extended`, `unreserved`, and `lost`. In particular, `unreserved` means required WAL is no longer protected although it may still physically exist until checkpoint removal; `lost` means required WAL has actually disappeared and the slot is no longer usable.

That gives the case's central decomposition:

```text
history still needed by consumer
    != history currently protected from reclamation
    != history physically present right now
    != history sufficient for future continuation
```

The 2020 policy is later history and must not be projected back into 2014 vocabulary or semantics.

## Research questions

1. What exactly is retained by a PostgreSQL replication slot?
2. How does a small `restart_lsn` frontier govern the lifetime of a much larger WAL corpus?
3. Does a disconnected consumer stop constraining retention? No — under the 9.4 slot relation, disconnection and retention obligation are separate.
4. Does crash-safe slot state imply all required WAL necessarily survives forever? No — PostgreSQL 13 provides a direct counterexample.
5. What is the difference among `reserved`, `unreserved`, physically present, and `lost` WAL?
6. Is slot invalidation technical erasure? No — it changes continuation/reclamation authority, not media sanitization.
7. How does this differ from Raft snapshot transfer, Bigtable redo-point recovery, and LevelDB file liveness?
8. What belongs here versus broader PostgreSQL/WAL history in `computing-archaeology`?

## Source ladder

| Evidence | Date | Strength | Use here |
|---|---:|---|---|
| PostgreSQL `858ec118...`, “Introduce replication slots” | 2014-02-01 | `H/P` | crash-safe slot purpose and initial WAL-retention relation |
| PostgreSQL 9.4 release notes | 2014-12-18 | `H/P` | released-feature chronology |
| PostgreSQL 9.4 `REL9_4_0` `slot.c` / `slot.h` | 2014 | `H/P` | persistent slot fields, save/checkpoint/startup reconstitution, minimum required LSN |
| PostgreSQL 9.4 official replication-slot docs | 9.4 release series | `H/P` | `restart_lsn`, disconnected standby, old-WAL retention, no slot-space bound |
| PostgreSQL `c6550776...` | 2020-04-07 | `H/P` | `max_slot_wal_keep_size`, checkpoint invalidation, disk-exhaustion motivation |
| PostgreSQL `b8fd4e02...` | 2020-06-24 | `H/P` | `reserved` / `extended` / `unreserved` / `lost` state refinement |
| PostgreSQL 13 release/docs | 2020-09-24 release | `H/P` | released resource-bound contract |

The complete source ledger and claim ledger are in the evidence file.

## Historical record

### 1. Replication slots enter PostgreSQL as crash-safe continuation state

PostgreSQL commit `858ec11858a914d4c380971985709b6d6b7dd6fc`, committed on **1 February 2014**, explicitly introduces replication slots as a **crash-safe data structure** that can prevent premature removal of WAL needed by a standby. The patch's wording is historical evidence, not a modern reconstruction.

The final PostgreSQL 9.4 release followed on **18 December 2014**. The distinction matters:

`mainline implementation date != release date != first proposal/invention date`

This case claims the first two only. It does not establish the complete pre-commit proposal genealogy.

### 2. Slot state is not the WAL corpus

In PostgreSQL 9.4 source, a slot has persistent state on disk under `pg_replslot` and an in-memory cache while the server is running. `ReplicationSlotPersistentData` includes `restart_lsn`, described as the oldest LSN that might still be required by the slot.

The slot therefore does not preserve downstream continuity by storing another copy of all WAL inside the slot object. It preserves a **control relation** that tells WAL reclamation how far back history may still be needed.

`slot metadata != protected WAL history`

### 3. One retained frontier can extend the lifetime of many WAL segments

The 9.4 `pg_replication_slots` documentation describes `restart_lsn` as the oldest WAL position that might still be required by the consumer and therefore will not be automatically removed during checkpoints.

The 9.4 implementation computes the oldest valid `restart_lsn` across slots and publishes that requirement to the WAL subsystem. A single sufficiently lagging slot can therefore hold the effective retention floor farther in the past than newer slots.

This is not a claim that `restart_lsn` contains the log. It is a compact retained relation whose value governs the liveness of many separate WAL files.

### 4. Current inactivity does not erase a future continuation claim

PostgreSQL 9.4 documentation explicitly motivates slots as retaining required WAL even when a standby is disconnected. The user-visible slot view separately reports whether a slot is currently `active`.

Therefore:

`active connection lifetime != slot lifetime != retained-history obligation lifetime`

A disconnected standby can be absent from current service while still shaping what the primary is allowed to reclaim.

### 5. The slot's own retention relation has a crash boundary

The 9.4 implementation distinguishes in-memory dirty state from saved state. `ReplicationSlotSave()` serializes slot state to disk; checkpoints save slots; startup restores on-disk slots and recomputes retention constraints. Slot creation uses a temporary path plus synchronization and rename steps.

This provides direct implementation evidence that the project treated the **retention policy state itself** as something that must survive crash/restart.

It also supplies a lower-layer stop condition:

`PostgreSQL performs persistence operations != every filesystem/controller/device empirically satisfies them under every fault`

No lower-device conformance claim is made here.

### 6. The original precise retention relation could grow without a built-in slot-space bound

The PostgreSQL 9.4 warm-standby documentation contrasts replication slots with fixed WAL-keeping and archive strategies. Slots can retain only what is known to be needed, but the same text says that the alternatives can bound `pg_xlog` space while replication slots at that time could not.

This is an important counterexample to a common optimization intuition:

`retention precision != retention cheapness`

The mechanism can be very precise about **why** old history is still live and still allow the required history to grow until local storage itself becomes the problem.

### 7. PostgreSQL 13 makes resource survival capable of defeating continuation preservation

On **7 April 2020**, commit `c6550776394e25c1620bc8258427c8f1d448080d` added `max_slot_wal_keep_size`. Its commit message states the operational motive plainly: experience showed that excessive slot-retained WAL could make the primary fail by exhausting space. Over-limit slots can be invalidated at checkpoint, allowing old WAL storage to be released.

PostgreSQL 13, released **24 September 2020**, includes this behavior.

This changes the retention authority relation:

```text
consumer says: this history is still needed for continuation
primary policy says: only up to this resource budget remains protected
```

Neither claim makes the other conceptually disappear. The system resolves the conflict by allowing protection to end and downstream continuation to fail.

### 8. `unreserved` proves physical presence and retention authority can diverge

Before PostgreSQL 13 released, commit `b8fd4e02c6d01183bf6def5897ad6cf7766bfff4` refined WAL availability into four user-visible states:

- `reserved`;
- `extended`;
- `unreserved`;
- `lost`.

For this case, `unreserved` is the crucial state. Required WAL is no longer protected under the configured retention rules, yet the segments may not have been removed by the next checkpoint and the consumer can still sometimes catch up. `lost` is stronger: required WAL has been removed and the slot can no longer resume replication.

So the system itself exposes this sequence:

```text
needed + protected
    -> needed + no longer protected + still physically present
    -> needed + removed
    -> old slot continuation inadmissible
```

The intermediate state blocks two collapses at once:

`physical survival != current retention protection`

and

`protection withdrawal != completed physical disappearance`

## 2024 deepening — failover-slot synchronization makes the retention frontier itself cross-node state

PostgreSQL 17, released **26 September 2024**, adds an explicit logical-slot failover regime. The implementation history usefully separates several steps that the final feature can otherwise make look like one operation.

On **25 January 2024**, commit `c393308b69d229b664391ac583b9e07418d411b6` added the logical-slot `failover` property. Its own commit message explicitly says that this property indicates a slot is intended to be synchronized to standbys while the commit **does not yet contain the synchronization capability**. Commit `93db6cbda037f1be9544932bd9a785dabf3ff712` on **22 February 2024** then added the periodic slot sync worker and `sync_replication_slots` on the standby. A separate **8 March 2024** commit, `bf279ddd1c28ce0251446ee90043a4cb96e5db0f`, added the wait relation that keeps logical subscribers from outrunning selected physical failover candidates; its development name `standby_slot_names` was renamed `synchronized_standby_slots` on **1 July 2024** by `0f934b0739ad28e8e20d8ad22ca80538544ce28a`.

The released documentation then adds the admission boundary. A standby can persist a synchronized logical slot only if the WAL and system-catalog rows required by the primary slot are still available on that standby; otherwise synchronization is refused because persisting the slot could admit a continuation state with missing history. At failover time, resumability depends on a **persistent** synchronized slot whose `pg_replication_slots.synced` value reached true before promotion.

That yields a new decomposition for this case:

```text
slot exists on primary
    != `failover = true`
    != standby copy/update mechanism enabled
    != synchronized slot admitted/persisted on standby
    != required WAL/catalog substrate available there
    != subscriber state/currentness
    != successful post-promotion continuation
```

### Engineering reconstruction — the claimant on history becomes history-bearing distributed control state

The original 9.4 case showed a compact retained claimant (`restart_lsn` and related slot state) constraining reclamation of a much larger WAL corpus. PostgreSQL 17 adds a second-order retention requirement: if another node may inherit publisher authority, the **claimant itself must survive and remain admissibly current on that future primary**.

So:

> **replicated retention frontier != replicated replay substrate**

and:

> **`failover = true` != `synced = true` != guaranteed subscriber currentness**.

The second distinction is directly bounded by PostgreSQL's own documentation: a logical slot knows nothing about receiver state. Slot synchronization preserves/qualifies the server-side continuation relation; it is not a complete subscriber-application checkpoint.

### Future failover readiness can constrain present progress

When `synchronized_standby_slots` is configured, logical WAL senders wait until the named physical standby slots confirm receipt/flush before exposing corresponding changes. The possible **future** role of a standby therefore creates a **present** scheduling constraint on logical replication.

This is a configured relation, not an assertion that all PostgreSQL logical replication is synchronous or that it shares the same semantics as synchronous transaction commit.

### Earlier ecosystem prior-art boundary

EDB's open-source `pg_failover_slots` extension was publicly announced on **18 April 2023** and already described copying logical slots to standbys, periodically synchronizing positions, and preventing logical consumers from advancing beyond selected failover standbys. This is earlier PostgreSQL-ecosystem **functional prior art** for the bounded failover-continuation problem.

No direct extension→core code ancestry or invention claim is made. Establishing such genealogy would require separate patch/mailing-list/source-history evidence.

### Philosophical interpretation — bounded

Project interpretation only: sometimes retaining old history is not enough; the system must also retain and transfer the **claim that says which old history remains live**, then revalidate that claim against the substrate available at a new authority node. Once that claim can move, it acquires its own persistence/currentness problem.

This is not PostgreSQL historical vocabulary and does not equate replication slots with human memory, archival promises, or tertiary retention.

### Forgetting stop condition

Failure to synchronize a slot, refusal to persist it, slot invalidation, slot drop, or WAL reclamation changes replay/continuation authority. None of these protocol events proves secure erasure of all old filesystem, device, backup, or forensic embodiments.

`continuation no longer admissible != media sanitization`

The source-controlled evidence and claim ledger are in [`../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md`](../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md).

## Retained state and mechanism

The bounded regime contains at least six distinct relations:

1. **primary current database state** — what the primary currently serves;
2. **WAL history** — older change records that can support downstream continuation;
3. **slot identity and persistent control state** — the retained replication-stream object;
4. **consumer-need frontier** — especially `restart_lsn`, delimiting oldest possibly needed WAL;
5. **current activity state** — whether a consumer is presently using the slot;
6. **WAL retention/admissibility state** — whether required history is protected, merely still present, or already lost under the later bounded policy.

The central lifecycle is:

```text
consumer falls behind or disconnects
    -> persistent slot remains
    -> restart_lsn stays behind primary progress
    -> older WAL remains protected
    -> retained-history volume grows

PostgreSQL 13, if a finite cap is configured:
    -> retention budget can be exceeded
    -> WAL may become unreserved
    -> consumer can still catch up while bytes remain
    -> checkpoint can remove required WAL
    -> slot becomes lost / unusable for continuation
```

## Engineering reconstruction

### A. Current-state sufficiency and continuation-history sufficiency are different

The primary may have everything required to serve its own current database state while an older WAL segment is still indispensable to a lagging downstream consumer.

Therefore:

`primary can continue serving != old WAL is reclaimable`

The reclaimability question depends on other retained relations, not only local currentness.

### B. A frontier can retain history without being history

A `restart_lsn` is a compact piece of second-order state. It says something about which earlier history remains possibly necessary. Its semantic weight is larger than its storage size because it governs reclamation of a potentially large log prefix.

`small metadata footprint != small retention consequence`

### C. Downstream absence can remain operationally present as an obligation

The disconnected consumer is not currently executing on the primary, yet the slot makes its future need operationally effective in the present by withholding WAL reclamation.

This is an engineering description of control flow, not a claim that the consumer is “virtually present” in any metaphysical sense.

### D. Retention obligation and retention capacity can conflict

PostgreSQL 9.4 privileges the continuation relation strongly enough that slot-held WAL lacks a built-in space cap. PostgreSQL 13 adds a policy that can withdraw protection rather than let that relation consume unlimited primary storage.

So:

`history still useful != infrastructure will preserve it without limit`

### E. Slot persistence does not imply continuation persistence

The 2020 bounded regime provides a direct counterexample to treating retained metadata as sufficient recovery evidence. The slot can still exist while its required WAL is `lost` and the slot is unusable.

`slot presence != replay-substrate presence != continuation admissibility`

### F. `unreserved` separates eligibility for reclamation from completed reclamation

When WAL becomes `unreserved`, it has crossed a policy boundary before it has necessarily crossed a physical removal boundary.

This mirrors a recurring repository distinction:

`retirement authority != completed retirement`

But the comparison remains functional; PostgreSQL WAL removal is not Flash block erase, filesystem secure deletion, or distributed tombstone garbage collection.

## Cross-case comparison

### Case 58 — Raft snapshotting

Raft's bounded 2014 snapshot mechanism permits committed log history to become dispensable after equivalent stable state plus boundary/membership metadata exists. A follower that needs compacted history can receive `InstallSnapshot`.

PostgreSQL 9.4 replication slots instead preserve the needed WAL history for the lagging consumer. PostgreSQL 13 can later allow that guarantee to fail under a configured space budget.

Functional contrast:

```text
Raft:
retire old command history -> preserve state equivalent -> transfer snapshot if follower is too far behind

PostgreSQL slot:
retain old WAL because consumer still needs replay -> optionally cap retention -> continuation can become impossible
```

This is not a genealogy and does not imply the protocols solve the same consistency problem.

### Case 57 — Bigtable redo/materialization

Case 57's redo points delimit history needed to reconstruct a tablet's own volatile/current materialization after failure. PostgreSQL `restart_lsn` can delimit history needed by another replication consumer.

`local recovery frontier != remote-consumer continuation frontier`

### Case 137 — LevelDB obsolete-file liveness

LevelDB can keep a superseded SSTable because a still-live `Version`/iterator references it. PostgreSQL can keep otherwise old WAL because a persistent replication slot still claims a downstream need.

The useful analogy is only:

`locally superseded/old != reclaimable while another live relation still depends on it`

LevelDB reader liveness and PostgreSQL replication continuation are different mechanisms and histories.

### Case 41 / distributed deletion cases

Cassandra tombstones and similar negative evidence can remain because a disconnected/stale replica may later reappear. PostgreSQL slots likewise show future distributed reconciliation/continuation needs extending the life of otherwise old state.

The analogy stops at **future participant need constraining reclamation**. A WAL replay frontier is not a tombstone grace period, and the failure of either mechanism has different consequences.

## Terminology and anti-anachronism

### PostgreSQL 9.4 vocabulary

The bounded historical terms include:

- `replication slot`;
- `physical` / `logical` slot;
- `restart_lsn`;
- `active`;
- `pg_replslot`;
- WAL segments;
- checkpoints.

### PostgreSQL 13 additions

The bounded later terms include:

- `max_slot_wal_keep_size`;
- `wal_status`;
- `reserved`;
- `extended`;
- `unreserved`;
- `lost`.

Do not rewrite the 2014 design as though it already had the 2020 cap or the later four-state availability model.

Likewise, project terms such as `continuation admission`, `retention frontier`, `history liveness claimant`, and `retirement authority` are **engineering reconstruction vocabulary**, not PostgreSQL historical vocabulary.

## Philosophical interpretation — bounded

The case contributes one modest temporal observation.

A WAL segment's technical future can depend on a participant that is currently absent. The past segment remains because another process may need to resume from it later. The slot makes that **future-oriented claim on the past** durable across disconnection and restart.

PostgreSQL 13 then supplies the counterweight: the claim is institutionally/technically bounded by the primary's configured resource policy. A future continuation can remain meaningful and nevertheless lose preservation priority.

That is enough for the conceptual comparison. It does not justify equating a replication slot with human memory, archival obligation, promise, debt, or Stieglerian retention.

## Failure and forgetting

- **Consumer lag grows:** more historical WAL can remain live because the frontier stays old.
- **Consumer disconnects:** the slot can continue retaining history; connection loss is not automatically continuation loss.
- **Primary crashes/restarts:** persistent slot state is restored so the retention relation can survive process lifetime.
- **Slot persistence write is not yet saved:** in-memory changed control state and crash-surviving control state are distinct in the implementation.
- **9.4 slot retained indefinitely:** local WAL space can become the failure resource because there is no built-in slot-space cap.
- **v13 configured cap exceeded:** protection can be withdrawn to protect primary capacity.
- **`unreserved`:** required WAL may still exist but is no longer protected from checkpoint removal.
- **`lost`:** required WAL is gone and old slot continuation is no longer usable.
- **Slot dropped/invalidated:** this changes retention/replay authority; it does not prove underlying media erasure.
- **Underlying storage violates persistence assumptions:** slot crash safety is then outside the contract directly established by PostgreSQL source alone.

## Counterexamples and stop conditions

- **Replication slot != replica.** The slot is control state about a replication stream, not another full database copy.
- **Replication slot != WAL corpus.** It governs retention of WAL stored elsewhere.
- **`restart_lsn` != full replay history.** It is a frontier, not the retained records themselves.
- **Current primary state != sufficient downstream replay history.** A remote consumer can still need old WAL.
- **Inactive != no retention obligation.** Disconnected consumers are a core use case.
- **Crash-safe slot != immortal slot.** Administrative drop and later resource-bounded invalidation remain possible.
- **Precise retention != bounded storage cost.** PostgreSQL 9.4 explicitly demonstrates the contrary.
- **WAL present != WAL protected.** PostgreSQL 13 `unreserved` is a direct counterexample.
- **WAL unprotected != WAL already removed.** The consumer may still catch up before removal.
- **Slot exists != slot usable.** A `lost` slot can remain observable while required replay history is gone.
- **WAL removal != secure deletion.** No media sanitization claim follows.
- **PostgreSQL replication retention != Raft snapshotting.** Retaining replay history and substituting materialized state are different future-repair strategies.
- **2020 resource-bound semantics != 2014 design vocabulary.** Later evolution remains later.

## Prior art and novelty boundary

This case does not claim PostgreSQL invented log retention, replication progress, replay positions, or keeping history for lagging replicas. Consensus systems, database logs, replication protocols, and archival logs provide extensive earlier history.

The contribution is narrower and source-controlled:

> **PostgreSQL 9.4 gives a particularly explicit crash-safe implementation in which a retained consumer-need frontier directly constrains WAL reclamation even across disconnection; PostgreSQL 13 then gives an equally explicit later counterexample in which primary resource protection can withdraw that history-retention guarantee, and the software distinguishes “no longer protected but still present” from “actually lost and no longer usable.”**

A complete genealogy belongs in `tmzncty/computing-archaeology`, not here. A fresh companion-repository search during this slice found no dedicated PostgreSQL replication-slot study to reuse.

## Uncertainty and next evidence

The bounded case is grounded, while these remain open:

1. exact pre-2014 proposal/review lineage and precursor implementations;
2. physical-slot versus logical-slot advancement semantics in release-by-release detail;
3. the interaction with WAL archiving, base backup, and reinitialization when required slot WAL is lost;
4. post-17 failover-slot fixes, multi-standby/cascading evolution, promotion fault injection, and production failover traces;
5. named production incidents or measurements of WAL accumulation and primary disk-pressure failure;
6. controlled checkpoint/slot-loss fault injection;
7. lower-layer filesystem and device persistence testing for the slot save/rename/fsync protocol;
8. full replication/log-retention genealogy, which should be coordinated with `computing-archaeology`.

## Related repository boundary

`tmzncty/computing-archaeology` was searched for `PostgreSQL replication slot`, `restart_lsn`, and related WAL-retention terms during this pass; no dedicated overlapping study was found.

If the broad history of PostgreSQL WAL, streaming replication, logical decoding, replication slots, failover slots, or related protocols is developed there later, this case should link to it rather than reproduce the history.

`technical-retention` keeps the narrower question:

> **Which retained relation makes otherwise old history continue to count as live, what event or policy ends that protection, and does loss of replay authority coincide with physical disappearance?**

## Evidence links

- [Evidence 141 — PostgreSQL 2014–2020 replication-slot WAL-retention grounding](../evidence/141-postgresql-2014-2020-replication-slot-wal-retention-grounding.md)
- [Evidence 141 deepening — PostgreSQL 17 failover-slot synchronization](../evidence/141-postgresql-2024-failover-slot-synchronization-deepening.md)
- [Case 58 — Raft snapshot/log compaction](58-raft-snapshot-log-compaction.md)
- [Case 57 — Bigtable tablet log/memtable recovery](57-google-bigtable-tablet-log-memtable-recovery.md)
- [Case 137 — LevelDB MANIFEST/CURRENT](137-leveldb-v17-manifest-current-recovery.md)
- [PostgreSQL commit `858ec118...`](https://github.com/postgres/postgres/commit/858ec11858a914d4c380971985709b6d6b7dd6fc)
- [PostgreSQL 9.4 replication-slot docs](https://www.postgresql.org/docs/9.4/warm-standby.html#STREAMING-REPLICATION-SLOTS)
- [PostgreSQL commit `c6550776...`](https://github.com/postgres/postgres/commit/c6550776394e25c1620bc8258427c8f1d448080d)
- [PostgreSQL commit `b8fd4e02...`](https://github.com/postgres/postgres/commit/b8fd4e02c6d01183bf6def5897ad6cf7766bfff4)
- [PostgreSQL 13 replication-slot view](https://www.postgresql.org/docs/13/view-pg-replication-slots.html)
