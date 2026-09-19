# Case 141 Evidence Deepening: PostgreSQL 2011–2020 WAL Archive as an Alternate Continuation Carrier

## Status

**`bounded deepening complete`** for the interaction among physical streaming replication, primary-local WAL retention, an externally accessible WAL archive, base-backup bootstrap, and reinitialization when the replay gap is no longer available.

This slice is deliberately narrow. It does **not** claim that an archived WAL segment keeps a replication slot usable, that a `lost` slot can be resurrected by copying archived WAL back, that logical-decoding slots have the same recovery path as physical standbys, or that WAL archival proves permanent or forensic preservation.

## Research question

Case 141 already establishes that a replication slot is persistent control state whose `restart_lsn` can keep a much larger local WAL corpus live, and that PostgreSQL 13 can later withdraw that protection until the slot reaches `lost`.

The remaining question is:

> **When WAL needed by a physical standby is no longer available through the primary's ordinary streaming-retention path, is the history necessarily gone, or can another retained carrier still bridge the continuation gap? If every usable replay path is gone, what substitutes for that missing history?**

The answer in PostgreSQL's own documentation is a three-way separation:

```text
primary-local WAL protection
    != WAL archive retention
    != standby continuation / bootstrap state
```

An accessible archive can preserve enough replay history for a physical standby even when the primary would otherwise recycle it. If the standby falls behind beyond all retained replay history, PostgreSQL documents reinitialization from a new base backup rather than continuation from the missing log range.

---

## Sources inspected

Primary PostgreSQL project sources:

1. PostgreSQL 9.1 documentation, **25.2 Log-Shipping Standby Servers**: <https://www.postgresql.org/docs/9.1/warm-standby.html>.
2. PostgreSQL 9.1 release notes, release date **12 September 2011**: <https://www.postgresql.org/docs/9.1/release-9-1.html>.
3. PostgreSQL 9.4 documentation, **25.2 Log-Shipping Standby Servers**: <https://www.postgresql.org/docs/9.4/warm-standby.html>.
4. PostgreSQL 9.4 release notes, release date **18 December 2014**: <https://www.postgresql.org/docs/9.4/release-9-4.html>.
5. PostgreSQL 13 documentation, **26.2 Log-Shipping Standby Servers**: <https://www.postgresql.org/docs/13/warm-standby.html>.
6. PostgreSQL 13 documentation, **51.80 `pg_replication_slots`**: <https://www.postgresql.org/docs/13/view-pg-replication-slots.html>.
7. PostgreSQL 13 documentation, **29.4 WAL Configuration**: <https://www.postgresql.org/docs/13/wal-configuration.html>.
8. PostgreSQL 13 release notes, release date **24 September 2020**: <https://www.postgresql.org/docs/13/release-13.html>.

A fresh search of `tmzncty/computing-archaeology` for `PostgreSQL replication slot`, `restart_lsn`, `WAL archive`, and `restore_command` found no dedicated PostgreSQL replication/archival packet to reuse. Broader WAL/log-shipping history therefore remains companion-repository territory.

---

## Historical record

### H/P — PostgreSQL 9.1 already documented archive-backed catch-up before replication slots existed

PostgreSQL 9.1 was released on **12 September 2011**. Its warm-standby documentation describes a standby as able to obtain WAL from three locations in an ordered retry loop:

1. a configured WAL archive through `restore_command`;
2. WAL already present in the standby's local `pg_xlog`;
3. streaming replication from the primary.

The same documentation says that when streaming replication is used **without file-based continuous archiving**, `wal_keep_segments` has to be large enough to stop the primary recycling WAL that the standby might still need. If the standby falls too far behind, it must be reinitialized from a new base backup.

Crucially, the same paragraph says that if an accessible WAL archive exists, `wal_keep_segments` is not required because the standby can use the archive to catch up.

This predates replication slots. Therefore:

```text
archive-backed physical-standby continuation
    predates
replication-slot WAL-retention control
```

This is a chronology statement about PostgreSQL's released documentation, not a claim that PostgreSQL invented log shipping or archive-based recovery in 2011.

### H/P — the archive is expected to be reachable independently of primary availability

PostgreSQL 9.1 tells operators to place continuous-archive storage somewhere accessible to the standby even when the primary is down, such as the standby itself or another trusted server rather than the primary.

The archive is therefore documented as a distinct operational carrier, not merely a second pathname into the same live primary `pg_xlog` directory.

### H/P — a base backup is the materialized starting point for a standby

The same 9.1 documentation requires taking a base backup to bootstrap the standby and restoring that backup when setting the standby up.

The relevant decomposition is already visible before slots:

```text
materialized database state at a base-backup point
    + subsequent WAL history
    -> standby catch-up
```

If the necessary intervening WAL is not retained, a new base backup replaces the unusable old bootstrap/replay path.

### H/P — PostgreSQL 9.4 adds replication slots without removing the archive alternative

PostgreSQL 9.4, released **18 December 2014**, documents the new replication-slot option in the physical streaming-replication setup.

Its streaming-replication section states:

- without continuous archiving, the primary may recycle old WAL before a standby receives it;
- if that happens, the standby must be reinitialized from a new base backup;
- `wal_keep_segments` or a replication slot can stop WAL from being recycled too early;
- if an accessible WAL archive retains enough segments, **those local retention solutions are not required for the standby to catch up**.

Thus replication slots entered an ecosystem that already had another retained-history route.

### H/P — archive cleanup has its own retention authority

PostgreSQL 9.1 and 9.4 both document `archive_cleanup_command` / `pg_archivecleanup` as ways to remove archived files no longer required by a standby.

The docs also give a separate warning: if the archive serves backup recovery as well as standby catch-up, files needed to recover from at least the latest base backup must still be retained even when the standby no longer needs them.

So the archive has a retirement policy that is distinct from the primary's slot frontier:

```text
slot says what primary-local WAL must remain
    !=
archive cleanup says which archived WAL copies may be retired
```

### H/P — PostgreSQL 13 retains the same alternate-carrier relation while adding bounded slot retention

PostgreSQL 13, released **24 September 2020**, preserves the same physical-standby guidance using the renamed `wal_keep_size` setting:

- absent file-based continuous archiving, a lagging standby can lose required WAL and need a new base backup;
- `wal_keep_size` or a replication slot can protect enough local WAL;
- an accessible archive can instead let the standby catch up, provided that archive retains enough segments.

This continuity matters because PostgreSQL 13 simultaneously introduces the bounded slot-retention states already grounded in Case 141.

### H/P — `lost` is slot-scoped, not a proof that every copy of the WAL vanished

PostgreSQL 13 defines `wal_status = lost` as meaning that some WAL files required by the slot have been removed and the slot is no longer usable.

That statement is strong about the **slot's continuation contract**. It is not a global inventory of every WAL embodiment. The separate warm-standby documentation explicitly permits an archive to retain WAL independently of the primary's ordinary local-retention mechanisms.

Therefore the historical record supports:

```text
slot is `lost`
    -> that slot is no longer usable

but not:

slot is `lost`
    -> no matching WAL segment can exist anywhere else
```

### H/P — WAL archiving itself can delay local recycling

PostgreSQL 13 WAL-configuration documentation states that when WAL archiving is enabled, log segments must be archived before they can be recycled or removed.

That is a separate local deletion gate from slot retention:

```text
checkpoint says older WAL is no longer needed for crash REDO
    + archival obligation satisfied
    + other retention constraints permit removal
    -> segment may be recycled / removed
```

This evidence does not imply that every archive implementation durably stores every accepted file forever. It shows that PostgreSQL's local WAL lifecycle recognizes successful archival as an independent prerequisite when archiving is configured.

---

## Engineering reconstruction

### E — one replay need can be served by multiple carriers

For a physical standby, the needed WAL interval is a logical dependency. It is not intrinsically tied to one storage location.

A bounded reconstruction from the documentation is:

```text
standby needs WAL range R
        |
        +-- primary still streams R
        |
        +-- standby-local pg_wal/pg_xlog contains R
        |
        +-- accessible archive contains R
        |
        `-- none of the above contains a sufficient gap-free path
                -> old continuation path fails
                -> bootstrap again from a new base backup
```

The important word is **sufficient**. One surviving segment does not repair a missing interval.

### E — local protection and global history existence are different predicates

A replication slot controls whether some WAL on the primary is protected from normal recycling/removal. A WAL archive is a separate carrier with its own placement and cleanup policy.

Therefore:

```text
primary no longer protects WAL X
    != WAL X no longer exists anywhere
```

and:

```text
WAL X exists in an archive
    != replication slot S is usable
```

The first prevents overclaiming erasure. The second prevents overclaiming slot resurrection.

### E — `lost` is a continuation-admission failure for the slot, not a sanitization witness

Once PostgreSQL reports a slot as `lost`, the slot cannot be used for its intended replication continuation. That is an application/protocol fact.

It proves none of the following:

- the corresponding bytes were overwritten on the primary medium;
- an archive copy does not exist;
- a backup does not contain equivalent history;
- lower-layer remnants are unrecoverable.

`lost continuation authority != secure erasure`

### E — archive retention is not slot retention moved to another directory

The two relations differ in carrier and retirement authority.

A slot is persistent server-side control state that constrains primary WAL reclamation. An archive is a copied WAL corpus governed by archive success and archive cleanup/retention policy. A standby can consume the archive through `restore_command` without the archive becoming part of the slot object.

Therefore:

```text
slot metadata
    != primary-local WAL files
    != archived WAL copies
```

### E — archive cleanup can end one rescue path while another may remain

`archive_cleanup_command` can retire archive files after they are no longer needed by a standby. If the same archive is also used for backups, the documented retention condition is different: files needed to recover from the latest base backup must remain.

So archive retention is role-dependent:

```text
not needed by standby A
    != not needed by backup recovery
    != safe to delete for every consumer
```

This is another example of one physical object having multiple liveness claimants.

### E — a new base backup substitutes materialized state for unavailable replay history

When the replay gap is gone, PostgreSQL does not claim that the missing WAL can be reconstructed from the slot metadata. The documented recovery is to reinitialize the standby from a **new base backup**.

The resulting transformation is:

```text
old base image + missing WAL interval
    -> continuation impossible along that path

newer base image
    -> new materialized starting point
    -> only later WAL must be replayed
```

This is a change of recovery starting point, not recovery of the old missing history.

### E — `new base backup` is not `repair the old slot`

A fresh base backup can restore a physical standby to a usable replication topology, but this does not mean the old slot's lost continuation relation has been repaired or that a logical slot's decoding state has been recreated.

The bounded claim is only:

> for the physical warm-standby path described by these PostgreSQL documents, reinitialization from a new base backup is the documented remedy when the required WAL interval is unavailable.

### E — archive success creates another retention obligation but not archival immortality

PostgreSQL's WAL configuration blocks recycling/removal until a segment has been archived when archiving is enabled. After a successful archival handoff, the destination's retention policy becomes decisive for how long that alternate copy remains available.

Thus:

```text
archive handoff completed
    != archive copy retained indefinitely
```

and:

```text
archive copy retained
    != every future consumer is entitled / configured to use it
```

---

## Functional comparison

### A — Case 58 Raft snapshotting: replay-history substitution by newer materialized state

A narrow functional analogy exists with Case 58. In Raft, when compacted log entries are no longer available, a lagging follower can receive a snapshot representing later materialized state plus protocol metadata. In this PostgreSQL physical-standby path, if required WAL has disappeared, the standby can be reinitialized from a newer base backup.

The shared abstract shape is:

```text
required incremental history unavailable
    -> transfer/install newer materialized state
    -> resume from a later boundary
```

The mechanisms, consistency protocols, metadata, and histories are different. No genealogy or equivalence is asserted.

### A — Case 57 Bigtable: materialization point plus later history

Case 57 likewise distinguishes a materialized state point from subsequent redo history. PostgreSQL's base-backup-plus-WAL relation is functionally comparable at that level only.

`similar recovery decomposition != same storage engine semantics`

### A — Case 130 LTO: surviving object versus usable access path

Case 130 shows that surviving media does not guarantee a usable end-to-end reader path. This PostgreSQL slice supplies a distributed analogue: surviving WAL somewhere does not guarantee that the current standby/slot configuration can actually consume it.

`carrier survival != configured continuation path`

Again, this is functional comparison only.

---

## Philosophical interpretation — bounded

Project interpretation only:

A retained past can be **plural**. The same logical history may have a primary-local embodiment, an archive copy, a standby-local copy, and later materialized state that reduces how much of the old replay history must still be traversed.

That means “forgotten here” and “forgotten everywhere” are different technical propositions.

Likewise, a system can abandon one continuity relation and establish another by choosing a newer materialized starting point. That is not equivalent to reconstructing the missing past.

These are repository-level interpretations, not PostgreSQL historical vocabulary and not claims about human memory or archival philosophy.

---

## Explicit non-claims / stop conditions

1. **X — `wal_status = lost` means no copy of the required WAL exists anywhere.** Rejected; the field describes slot availability, while archives are separate carriers.
2. **X — an archive copy makes a `lost` replication slot usable again.** Not established by the inspected sources.
3. **X — copying archived WAL back resurrects the exact old slot state.** Not established.
4. **X — physical-standby archive catch-up applies unchanged to logical-decoding slots.** Rejected as an unsupported generalization.
5. **X — a WAL archive is part of the replication-slot object.** Rejected; slot control state and archived WAL corpus are separate.
6. **X — replication slots invented PostgreSQL history retention.** Rejected; archive-based catch-up is documented in PostgreSQL 9.1 before slots.
7. **X — PostgreSQL 9.1 invented log shipping or WAL archiving.** Not claimed.
8. **X — `wal_keep_segments`/`wal_keep_size`, slots, and archives are implementation-identical.** Rejected; they are alternative/overlapping retention mechanisms.
9. **X — an accessible archive always contains every needed segment.** Rejected; catch-up depends on retaining a sufficient interval.
10. **X — archive success means the copy is retained forever.** Rejected; archive cleanup is explicitly documented.
11. **X — archive cleanup safe for one standby is automatically safe for backup recovery.** Rejected by PostgreSQL's own warning.
12. **X — reinitializing from a new base backup reconstructs the missing WAL bytes.** Rejected; it changes the materialized starting point.
13. **X — a new base backup preserves the identity/history of the old standby continuation path in every relevant sense.** Not established.
14. **X — local WAL removal is secure deletion.** Rejected; no sanitization evidence is present.
15. **X — archived WAL is immune to storage failure, corruption, operator deletion, or lifecycle policy.** Not established.
16. **X — successful `archive_command` proves downstream archival media semantics beyond PostgreSQL's handoff contract.** Not established.
17. **X — every archived segment is independently sufficient for catch-up.** Rejected; a usable replay interval must be available.
18. **X — a standby that can obtain old WAL from an archive necessarily uses a replication slot.** Rejected; 9.1 is a pre-slot counterexample.
19. **X — base backup and WAL archive are interchangeable objects.** Rejected; one is materialized database state, the other incremental history.
20. **X — similarity to Raft snapshots, Bigtable redo, or LTO access-path survival establishes genealogy.** Rejected; comparisons are functional only.

---

## Claim ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| PostgreSQL 9.1 documents archive-backed standby catch-up before replication slots | `H/P` | official 9.1 warm-standby docs |
| 9.1 streaming without archive can require `wal_keep_segments`, otherwise excessive lag can force a new base backup | `H/P` | official 9.1 streaming-replication section |
| an accessible archive can substitute for primary-side retained WAL for physical standby catch-up if enough segments remain | `H/P` | official 9.1, 9.4, and 13 warm-standby docs |
| 9.4 adds replication slots as another way to prevent premature WAL recycling | `H/P` | official 9.4 warm-standby docs |
| archive cleanup has its own retention condition, including a separate backup-recovery requirement | `H/P` | official 9.1/9.4/13 docs |
| PostgreSQL 13 `lost` means required WAL was removed and the slot is unusable | `H/P` | official 13 `pg_replication_slots` docs |
| PostgreSQL 13 requires WAL to be archived before local recycling/removal when archiving is enabled | `H/P` | official 13 WAL-configuration docs |
| slot-local WAL protection is not the same predicate as global WAL existence | `E` | derived from slot status + independent archive path |
| archive WAL presence is not proof that a lost slot is usable | `E` | bounded negative inference from separate contracts |
| a new base backup changes the materialized recovery starting point rather than recovering missing WAL | `E` | derived from documented reinitialization flow |
| one history dependency may be satisfiable by multiple carriers | `E` | archive/local/streaming fallback structure |
| archive cleanup and slot retention are separate retirement authorities | `E` | separate documented mechanisms |
| base-backup substitution is functionally comparable to snapshot-based catch-up | `A` | bounded cross-case reconstruction only |
| any of the above proves secure erasure | `X` | no sanitization evidence |

---

## Prior-art / chronology boundary

The most important chronology result is negative rather than novelty-seeking:

```text
PostgreSQL 9.1 (2011):
archive-backed physical standby catch-up + base-backup reinitialization

PostgreSQL 9.4 (2014):
replication slots join the local WAL-retention choices

PostgreSQL 13 (2020):
slot retention becomes explicitly budget-bounded with `unreserved` / `lost`
```

Therefore replication slots should not be narrated as the origin of PostgreSQL's general problem of retaining replay history for lagging standbys. Their distinctive contribution in this case is the **persistent, precise consumer-need frontier that constrains primary-local reclamation**, later made resource-bounded.

This is not an invention-priority claim for WAL archives, log shipping, base backups, or replication slots outside the bounded PostgreSQL chronology inspected here.

---

## What this slice closes

This substantially closes the Case 141 debt item previously phrased as:

> interaction with WAL archiving, base backup, and reinitialization when required slot WAL is lost.

The debt is now narrower:

- exact implementation behavior if a physical slot reaches `lost` while an independently retained archive still contains the nominally required WAL range;
- whether any supported operational sequence can reuse such archive history without discarding/recreating the slot;
- logical-slot-specific archive/rebootstrap semantics, which must not be inferred from physical warm-standby documentation;
- fault-injection traces covering archive gaps, checkpoint removal, standby catch-up, and reinitialization;
- archive-system durability and lower-layer persistence validation;
- broader PostgreSQL WAL/archive genealogy in `computing-archaeology`.

## Related repository routing

A fresh search of `tmzncty/computing-archaeology` found no dedicated PostgreSQL replication-slot/WAL-archive packet. This evidence therefore keeps only the retention-specific seam:

```text
consumer needs history
    -> one or more carriers may keep it available
    -> each carrier has a distinct retirement authority
    -> loss of one carrier is not global erasure
    -> loss of every usable replay path forces a newer materialized bootstrap
```

The broader history of PostgreSQL WAL archiving, streaming replication, backup tooling, archive implementations, and operator practice belongs in `computing-archaeology` if developed later.