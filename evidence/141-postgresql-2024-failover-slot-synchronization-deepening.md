# Evidence: PostgreSQL 17 logical failover-slot synchronization — replicated retention frontier and failover currentness

**Status:** `grounded`

**Case:** [Case 141 — PostgreSQL Replication Slots: WAL Retention Frontier and Continuation Admission](../cases/141-postgresql-replication-slot-wal-retention-frontier.md)

**Scope:** PostgreSQL 17 core failover-slot semantics and one bounded earlier PostgreSQL-ecosystem functional-prior-art witness. This record distinguishes failover intent, slot-control-state synchronization, replay-substrate availability, standby readiness, subscriber state, and media erasure. It does **not** claim PostgreSQL invented failover-capable logical replication, that the 2023 extension is direct code ancestry of PostgreSQL 17, or that synchronized slot metadata proves every lower layer has durably preserved all required bytes under arbitrary faults.

## Research question

PostgreSQL 9.4 made a replication slot a crash-surviving claimant on old WAL: a compact frontier such as `restart_lsn` could keep much larger history live on one primary. What additional retention obligation appears when the machine that may become the future primary is itself allowed to change?

PostgreSQL 17 supplies a bounded answer: **the continuation claimant must itself become replicated state, and its standby copy is useful only when the history and catalog state it refers to are also available and the copy has reached an admitted synchronized state before failover.**

That gives a sharper decomposition:

```text
logical slot exists on primary
    != slot marked for failover
    != slot-control state copied to standby
    != synchronized slot admitted as persistent (`synced = true`)
    != required WAL/catalog replay substrate available on standby
    != subscriber has applied/confirmed the same state
    != successful post-promotion continuation
```

## Source ledger

### Primary A — PostgreSQL core commit `c393308b...` (2024-01-25)

**Commit:** `c393308b69d229b664391ac583b9e07418d411b6`, “Allow to enable failover property for replication slots via SQL API.”  
**Source:** <https://github.com/postgres/postgres/commit/c393308b69d229b664391ac583b9e07418d411b6>

The commit adds the slot `failover` property and an optional fifth `failover` argument to `pg_create_logical_replication_slot()`. Its own commit message is unusually explicit about the boundary: the property indicates that a slot is intended to be synchronized to standbys, but **this commit does not yet implement slot synchronization**; later commits will do that.

This is direct historical evidence for:

> `failover intent/property != synchronization mechanism`

It also prevents a common retrospective collapse in which the final PostgreSQL 17 feature is read backward as one indivisible change.

### Primary B — PostgreSQL core commit `93db6cbd...` (2024-02-22)

**Commit:** `93db6cbda037f1be9544932bd9a785dabf3ff712`, “Add a new slot sync worker to synchronize logical slots.”  
**Source:** <https://github.com/postgres/postgres/commit/93db6cbda037f1be9544932bd9a785dabf3ff712>

This commit adds the slot synchronization worker and `sync_replication_slots`. When enabled on a physical standby, failover logical slots from the primary can be created/updated on that standby and synchronized periodically. Slots that cease to require synchronization can be dropped by the worker. The commit separately notes that making logical WAL senders wait for physical standbys would be added later.

So a second boundary is explicit in the implementation chronology:

> `copy/update failover-slot control state != gating subscriber-visible progress on standby WAL receipt`

### Primary C — PostgreSQL core commit `bf279ddd...` (2024-03-08) and final-name commit `0f934b07...` (2024-07-01)

**Initial commit:** `bf279ddd1c28ce0251446ee90043a4cb96e5db0f`, “Introduce a new GUC 'standby_slot_names'.”  
<https://github.com/postgres/postgres/commit/bf279ddd1c28ce0251446ee90043a4cb96e5db0f>

**Rename:** `0f934b0739ad28e8e20d8ad22ca80538544ce28a`, “Rename standby_slot_names to synchronized_standby_slots.”  
<https://github.com/postgres/postgres/commit/0f934b0739ad28e8e20d8ad22ca80538544ce28a>

The March commit adds a wait relation: logical WAL sender processes associated with failover slots wait until named physical standby slots have confirmed receipt/flush of the corresponding WAL before changes are exposed downstream. The stated purpose is to keep potential failover candidates from lagging behind logical subscribers. The July rename is important vocabulary hygiene: the released PostgreSQL 17 term is `synchronized_standby_slots`, not the earlier development name `standby_slot_names`.

This creates a present-time cost for future failover readiness:

> **a future-primary retention/readiness requirement can delay current logical decoding progress.**

That statement is engineering reconstruction of the documented wait relation, not PostgreSQL historical vocabulary.

### Primary D — PostgreSQL 17 release record (2024-09-26)

**Release notes:** <https://www.postgresql.org/docs/17/release-17.html>  
**Release announcement:** <https://www.postgresql.org/about/news/postgresql-17-released-2936/>

PostgreSQL 17 was released on **2024-09-26**. The release notes list logical-slot failover and `sync_replication_slots` among the logical-replication changes. This anchors the released-feature boundary; it is not an invention date for slot synchronization or replication failover as a broader idea.

### Primary E — PostgreSQL 17 logical-decoding documentation, §47.2.3

**Documentation:** <https://www.postgresql.org/docs/17/logicaldecoding-explanation.html#LOGICALDECODING-REPLICATION-SLOTS-SYNCHRONIZATION>

The released documentation adds several crucial admission conditions.

1. A logical slot on the primary must be created/configured as a failover slot, and `sync_replication_slots` must be enabled on the standby for automatic periodic synchronization.
2. Automatic synchronization is recommended over one-shot manual `pg_sync_replication_slots()` because it continuously retries and updates; the manual function is primarily for testing/debugging and is more vulnerable to initial-sync failure when required WAL or catalog rows are already disappearing.
3. The standby persists a synchronized slot only when the primary slot's required WAL and system-catalog rows are still available on the standby. If not, PostgreSQL refuses to persist the synchronized slot because doing so could lead to data loss.
4. Post-failover resumability depends on the standby slot having reached `pg_replication_slots.synced = true` before failover. Only **persistent** synchronized slots in that state can be used for logical replication after promotion; temporary synchronized slots do not qualify.

The same chapter also says a logical replication slot knows nothing about the receiver's state. That prevents `synced = true` from being read as proof that the subscriber itself has applied every corresponding change.

### Primary F — PostgreSQL 17 replication configuration and slot-state views

**Replication configuration:** <https://www.postgresql.org/docs/17/runtime-config-replication.html>  
**`pg_replication_slots`:** <https://www.postgresql.org/docs/17/view-pg-replication-slots.html>

The released `synchronized_standby_slots` setting makes logical WAL senders wait until named physical slots confirm WAL receipt/flush. The `pg_replication_slots` view separately exposes:

- `failover`: whether a logical slot is enabled to be synchronized to standbys;
- `synced`: whether the logical slot was synchronized from a primary;
- `restart_lsn` and `catalog_xmin`: retained-history/catalog frontiers;
- `confirmed_flush_lsn`: what the logical consumer has confirmed receiving.

These are distinct fields because they answer different questions. The interface itself therefore resists a single boolean notion of “safe for failover.”

## Earlier PostgreSQL-ecosystem functional prior-art witness — `pg_failover_slots` (2023)

**Announcement:** EDB, “PG Failover Slots (pg_failover_slots),” 2023-04-18, hosted in the PostgreSQL.org community news feed: <https://www.postgresql.org/about/news/pg-failover-slots-pg_failover_slots-2623/>

The extension announcement describes the pre-core problem in almost the same operational shape: logical slots existed only on the primary; after promotion, losing the consumer-confirmed position and the information about which log still had to be retained could create an unknown gap. The extension advertised copying missing slots to the standby, periodically synchronizing their positions, and ensuring selected standbys received data before logical-slot WAL senders sent data to consumers.

This is useful **functional prior art inside the PostgreSQL ecosystem**. It is not evidence that PostgreSQL 17 copied this code, that the extension originated the idea, or that there is a proven direct implementation genealogy. Establishing proposal/code lineage would require a separate mailing-list and patch-series study.

## Historical record — bounded conclusions

### H1. PostgreSQL 17 decomposes failover support into several separately introduced controls

The development record does not support the shortcut `failover=true means the slot is synchronized`. The January commit explicitly says the opposite: it introduces the property before the synchronization capability exists. February adds periodic standby synchronization. March adds a separate wait relation so logical consumers cannot outrun selected physical failover candidates. July fixes the released configuration name. September releases the combined feature.

### H2. Slot synchronization has an admission test based on the referred-to substrate

PostgreSQL does not simply copy slot metadata and declare success. The released documentation refuses to persist the synchronized slot when the WAL or catalog rows the remote slot needs are already unavailable on the standby.

So the software itself establishes:

> `replicated slot-control metadata != sufficient replay substrate`

### H3. `synced` is a readiness predicate with a promotion-time consequence

The released documentation makes post-failover continuation depend on `synced = true` before failover and on slot persistence. This is stronger than “a slot-shaped object exists on the standby.”

`standby slot exists != standby slot admitted for post-failover logical decoding`

### H4. Subscriber state remains a separate relation

The same logical-decoding documentation says a logical slot does not know receiver state. A synchronized slot can therefore be a valid retained continuation object without being a full record of subscriber application state.

`slot failover readiness != subscriber currentness`

## Engineering reconstruction

### E1. The retention frontier becomes retained replicated state

Case 141's original PostgreSQL 9.4 regime already showed that a small `restart_lsn`-bearing control object can keep a large WAL suffix live. PostgreSQL 17 adds a second-order requirement: if another machine may inherit the publisher role, the **claim that keeps history live must itself survive across machines**.

```text
WAL history
    <- governed by slot/frontier state on primary
    <- failover requires a qualified copy of that state on standby
    <- the copy is only useful while its referenced WAL/catalog substrate remains available
```

This is an engineering reconstruction of the documented relations, not a term used by PostgreSQL developers.

### E2. Failover intent, propagation, currentness, and usability are different axes

A compact model is:

```text
`failover = true`
    -> eligible/intended for synchronization

`sync_replication_slots = true`
    -> standby periodically propagates eligible slot state

required WAL + catalog rows available
    -> synchronized state can be persisted safely

`synced = true` + persistent slot before failover
    -> slot is admitted for post-promotion logical replication
```

None of those arrows is an identity.

### E3. Replicating a pointer/frontier does not replicate what it points to

The refusal to persist an unsafe synchronized slot is a direct counterexample to the idea that replication metadata alone carries continuation. `restart_lsn`, `catalog_xmin`, and related slot state are meaningful only with the WAL/catalog history they qualify.

`retained reference/control state != retained referent substrate`

### E4. Future failover readiness can gate present progress

With `synchronized_standby_slots`, a logical WAL sender waits for selected physical standby slots to confirm receipt/flush before exposing corresponding decoded changes. A requirement about a **possible future primary** can therefore become a present scheduling constraint.

This is not ordinary synchronous-commit equivalence and not a claim that all PostgreSQL 17 logical replication automatically blocks this way; it applies when the relevant failover configuration is enabled.

### E5. Periodic synchronization creates a currentness problem for the claimant itself

The slot sync worker is periodic. The project therefore distinguishes:

`a retained standby copy exists != the copy has reached the released readiness condition at the instant of failover`.

The released contract resolves that operational question with `synced` plus the substrate checks rather than by treating any old copied slot as adequate.

### E6. Crash-safe does not mean exact-most-recent progress

PostgreSQL's logical-decoding documentation separately notes that a slot's current position is persisted at checkpoints, so after a crash it can rewind and resend recent changes. That is a useful adjacent boundary:

`crash-surviving continuation != exact latest progress retained`

Clients must tolerate/reconcile duplicates. This observation is not used here to claim that failover-slot synchronization and local crash recovery are the same mechanism.

## Functional analogy — bounded

The useful cross-case analogy is to other cases where **control metadata that governs retention or eligibility has its own currentness problem**. For example, Cassandra retained maintenance metadata and repair metadata can remain operationally significant after the data operation that motivated them. PostgreSQL 17 adds a distributed version of that problem: a copied continuation claimant is useful only while it is sufficiently current and its referred-to history remains available.

The analogy stops at that function. Replication-slot synchronization is not Cassandra hinted handoff, repair metadata, consensus membership, or a distributed tombstone protocol.

Within PostgreSQL itself, the historical evolution is stronger than analogy:

```text
9.4: keep a crash-surviving local claimant so one primary retains needed history
17:  copy/qualify that claimant on a potential future primary and coordinate WAL receipt
```

This is same-project evolution, not a claim that the 2024 design was conceptually implicit in 2014.

## Philosophical interpretation — bounded

**Project interpretation only:** the case shows that retaining a past is sometimes insufficient unless the system also retains, transfers, and revalidates the **claim about which past remains live**. Once authority may move to another node, that claim becomes a technical object with its own persistence and currentness obligations.

This does not make a replication slot a human memory, promise, archive, debt, or Stieglerian tertiary retention. The mechanism remains a database replication protocol with explicit WAL/catalog and promotion constraints.

## Forgetting and sanitization stop condition

Dropping a slot, failing to synchronize it, refusing to persist it, letting required WAL become reclaimable, or losing post-failover continuation authority changes protocol-level retention and replay relations. None of those events by itself proves that every old WAL byte, filesystem block, device remap, backup copy, or forensic embodiment has been securely erased.

`continuation no longer admissible != physical sanitization`

## Claim ledger

| Claim | Layer | Strength | Boundary |
|---|---|---|---|
| PostgreSQL 17 released logical-slot failover controls | historical record | `H/P` | release boundary, not invention date |
| `c393308b...` adds failover property before sync capability | historical record | `H/P` | commit says subsequent commits add sync |
| `93db6cbd...` adds periodic slot sync worker and `sync_replication_slots` | historical record | `H/P` | standby synchronization mechanism |
| `bf279ddd...` adds wait-on-physical-standby relation | historical record | `H/P` | development name later renamed |
| `synced = true` + persistence conditions matter at failover | historical record | `H/P` | released PostgreSQL 17 docs |
| missing WAL/catalog rows block safe synchronized-slot persistence | historical record | `H/P` | released admission condition |
| failover intent != synchronized/readiness state | engineering reconstruction | `E` | reconstructed from separately exposed controls |
| copied control state != replay substrate | engineering reconstruction | `E` | direct substrate-check counterexample |
| future failover readiness may gate current logical progress | engineering reconstruction | `E` | only under configured synchronized standbys |
| slot readiness != subscriber currentness | engineering reconstruction | `E` | slot explicitly knows nothing of receiver state |
| 2023 `pg_failover_slots` is earlier ecosystem functional prior art | historical/prior-art record | `H/P/A` | no direct ancestry or invention claim |
| retained continuation claim becomes cross-node retention object | philosophical interpretation | `P/I` | project language only |
| loss of continuation != media sanitization | stop condition | `X` | no physical-erasure inference |

## Counterclaims and limits

- `failover = true` does **not** mean the slot is already synchronized.
- A synchronized slot object does **not** prove required WAL/catalog history exists; PostgreSQL checks that separately.
- `synced = true` is not a statement about subscriber-applied state; the slot does not know receiver state.
- Automatic periodic sync is not literal instantaneous identity at every wall-clock instant.
- `synchronized_standby_slots` is a configured wait relation, not evidence that all logical replication in PostgreSQL 17 is synchronous in the same sense.
- The 2023 extension is earlier functional prior art, not proven source-code ancestry of the PostgreSQL 17 core feature.
- This slice does not establish first invention of logical-slot failover, replication-position transfer, or log-retention frontiers.
- No claim is made about filesystem, controller, SSD, or cloud-volume durability beyond PostgreSQL's own documented contract.
- No protocol-level slot loss or WAL recycling event is treated as sanitization.

## Related-repository boundary

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for PostgreSQL replication-slot failover / `sync_replication_slots` found no dedicated study to reuse.

Accordingly this record keeps only the retention/currentness slice. A broader genealogy of PostgreSQL WAL, physical/logical replication, pre-17 failover approaches, patch-series evolution, and database-log failover belongs primarily in `computing-archaeology` if developed later.

## Open evidence debt

1. Trace the full PostgreSQL mailing-list and patch-series genealogy before `c393308b...`, including rejected/earlier designs.
2. Compare `pg_failover_slots` implementation history with core PostgreSQL 17 only if source-level lineage can be demonstrated rather than inferred from functional similarity.
3. Capture controlled promotion tests at different synchronization phases (`failover=true` only, temporary sync, persistent `synced=true`, missing WAL/catalog substrate).
4. Measure the latency/backpressure effects of `synchronized_standby_slots` under a lagging physical standby.
5. Trace post-17 fixes and later-version semantic changes without back-projecting them into PostgreSQL 17.
6. Keep lower-layer persistence and secure-erasure testing separate from PostgreSQL protocol semantics.
