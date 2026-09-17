# Case 58 deepening — etcd v3.5.15 WAL snapshot marker sync and restart-admission boundary

## Status

**`bounded deepening complete`**

This file closes one narrow storage-layer debt left by the existing etcd v3.5.15 Case 58 deepening:

> After the snapshot file has been written, what exactly happens to the separate WAL-side snapshot record, when does that record cross etcd's explicit sync boundary, and how does restart use that WAL evidence when deciding whether a snapshot file is admissible?

The target is the released **etcd v3.5.15** source. GitHub records the v3.5.15 release as published on **2024-07-19**.

This is a later implementation witness for Case 58, not evidence that the 2014 Raft paper prescribed etcd's exact local file/WAL ordering.

## Navigation

- canonical Case 58: [`../cases/58-raft-snapshot-log-compaction.md`](../cases/58-raft-snapshot-log-compaction.md)
- parent v3.5.15 implementation deepening: [`58-etcd-3515-ready-snapshot-persistence-publication-deepening.md`](58-etcd-3515-ready-snapshot-persistence-publication-deepening.md)
- received-snapshot pathname durability follow-up: [`58-etcd-2026-received-snapshot-db-directory-fsync-deepening.md`](58-etcd-2026-received-snapshot-db-directory-fsync-deepening.md)

The 2026 received-snapshot follow-up concerns `.snap.db` pathname durability after rename. This file addresses a different representation: the v3.5.15 **WAL snapshot record** written by local snapshot publication.

## Evidence classes

- **H/P — implementation record:** exact etcd v3.5.15 source and release metadata.
- **E — engineering reconstruction:** retained-state and crash-window distinctions inferred from explicit ordering and restart matching.
- **A — functional analogy:** narrow comparison to checkpoint-manifest/commit-marker patterns and to Case 100 publication barriers.
- **P — bounded interpretation:** project vocabulary about continuation authority and recognition; not terminology attributed to etcd authors.

## Exact source anchors

Primary sources used in this slice:

1. etcd v3.5.15 release metadata: <https://github.com/etcd-io/etcd/releases/tag/v3.5.15>
2. v3.5.15 storage wrapper: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/storage.go>
3. v3.5.15 snapshotter: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/api/snap/snapshotter.go>
4. v3.5.15 WAL implementation: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/wal/wal.go>
5. v3.5.15 WAL snapshot validation helper: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/wal/walpb/record.go>
6. v3.5.15 server restart path: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/server.go>

## Historical / implementation record

### H/P — v3.5.15 deliberately saves the snapshot file before the WAL snapshot record

`server/etcdserver/storage.go` defines `storage.SaveSnap` by first constructing a `walpb.Snapshot` containing:

- snapshot `Index`;
- snapshot `Term`;
- `ConfState`.

It then calls:

```go
err := st.Snapshotter.SaveSnap(snap)
if err != nil {
    return err
}
return st.WAL.SaveSnapshot(walsnap)
```

The source comment states the failure-policy intent directly: save the snapshot file before writing the snapshot to the WAL. That ordering can leave an **orphaned snapshot file**, but prevents a **WAL snapshot entry with no corresponding snapshot file**.

This direct source comment matters because the asymmetric intermediate state is not merely inferred after the fact; it is an explicitly documented implementation choice.

Therefore:

```text
snapshot-file save
    -> WAL snapshot-record save

possible failure window
    -> file exists without matching WAL snapshot record

inverse partial state
    -> WAL snapshot record without corresponding snapshot file
    -> ordering is specifically designed to avoid it
```

### H/P — the snapshot file and WAL record contain different representations

`Snapshotter.save` serializes the full `raftpb.Snapshot`, wraps it with a CRC, and writes it to a `.snap` file.

By contrast, the `walpb.Snapshot` created in `storage.SaveSnap` carries boundary/control metadata: index, term, and configuration state. It is serialized as a WAL record of `snapshotType`.

The useful distinction is therefore not merely “two copies of the same file”:

```text
snapshot file
    = materialized Raft snapshot representation

WAL snapshot record
    = WAL-side boundary / restart-matching representation
```

The exact fields and roles are implementation facts; the phrase **restart anchor** below is an engineering label used by this repository.

### H/P — `WAL.SaveSnapshot` does not merely append; it calls the WAL sync path before returning

In v3.5.15, `WAL.SaveSnapshot`:

1. validates the snapshot for writing;
2. marshals the `walpb.Snapshot`;
3. takes the WAL mutex;
4. encodes a record of `snapshotType`;
5. updates the WAL's last-entry index if the snapshot index is ahead;
6. returns `w.sync()`.

The relevant source shape is:

```go
rec := &walpb.Record{Type: snapshotType, Data: b}
if err := w.encoder.encode(rec); err != nil {
    return err
}
if w.enti < e.Index {
    w.enti = e.Index
}
return w.sync()
```

This closes the previously open question of whether v3.5.15 `SaveSnapshot` simply buffered/encoded the marker or crossed an explicit sync boundary before successful return.

For this exact source, successful `WAL.SaveSnapshot` includes a call to the WAL sync path.

### H/P — the WAL sync path flushes the encoder and calls `fdatasync` unless unsafe no-sync mode is set

`WAL.sync()` first flushes the encoder. In the normal path, it then calls:

```go
fileutil.Fdatasync(w.tail().File)
```

There is an explicit `unsafeNoSync` mode under which this storage guarantee is deliberately bypassed. The normal production claim must therefore be phrased as:

```text
normal v3.5.15 WAL SaveSnapshot success
    -> encoded snapshot record passed through WAL sync
    -> encoder flush + fdatasync requested
```

not:

```text
all imaginable etcd configurations
    -> identical durability behavior
```

The source itself names the bypass `unsafeNoSync`; this packet does not silently treat that mode as equivalent to normal stable-storage behavior.

### H/P — `SaveSnap` returns only after the WAL snapshot record's sync call succeeds

`storage.SaveSnap` returns the result of `WAL.SaveSnapshot`. Since `WAL.SaveSnapshot` returns the result of `w.sync()`, the normal successful local `SaveSnap` chain is:

```text
serialize/checksum snapshot file
    -> write + file sync snapshot file
    -> construct WAL snapshot metadata
    -> encode snapshotType WAL record
    -> flush WAL encoder
    -> fdatasync current WAL file
    -> storage.SaveSnap may return success
```

This is stronger than the earlier bounded statement “snapshot file precedes WAL record.” It identifies the WAL record's explicit source-level synchronization boundary.

It is still not evidence that the two files form one atomic storage transaction.

### H/P — restart enumerates WAL snapshot records before selecting a snapshot file

The v3.5.15 restart path first calls:

```go
wal.ValidSnapshotEntries(cfg.Logger, cfg.WALDir())
```

It then calls:

```go
ss.LoadNewestAvailable(walSnaps)
```

The adjacent server comment states that snapshot files can be orphaned if etcd crashes after writing them but before writing the corresponding WAL log entries.

This directly joins the write-side asymmetric ordering to the restart-side admission rule.

### H/P — restart selection does not accept the newest snapshot pathname merely because it exists

`Snapshotter.LoadNewestAvailable` considers snapshot files from newest to oldest, but accepts one only if its `(term,index)` matches one of the supplied WAL snapshot records.

Therefore:

```text
newer snapshot file physically present
    != matching WAL snapshot evidence present
    != snapshot selected for restart
```

An orphan file is an anticipated intermediate/storage residue, not automatic continuation authority.

### H/P — WAL snapshot entries themselves are filtered against committed HardState

`WAL.ValidSnapshotEntries` reads WAL `snapshotType` records and the latest hard state. Its source comment defines a valid snapshot entry as one whose index is less than or equal to the most recent committed HardState, and the function filters entries accordingly:

```text
wal snapshot record observed
    + snapshot index <= latest HardState.Commit
    -> returned as a valid WAL snapshot entry
```

Thus restart admission has at least two relations in this implementation:

```text
WAL-side snapshot record must be valid relative to committed HardState
    +
file snapshot (term,index) must match a returned WAL snapshot entry
```

This is more specific than saying merely “the snapshot file has a CRC.”

### H/P — WAL open/read also treats the selected snapshot as a required historical marker

The v3.5.15 WAL API documents that a snapshot supplied to `Open` should previously have been saved to the WAL. `ReadAll` checks snapshot records while decoding and returns `ErrSnapshotNotFound` if the requested snapshot boundary is not found.

That is consistent with the restart-selection logic above: the WAL-side snapshot record is part of the local continuation contract, not decorative duplicate metadata.

## Retained-state decomposition

This slice sharpens the Case 58 implementation model into the following representations:

1. **full snapshot artifact** — the checksummed serialized `raftpb.Snapshot` in the snapshot directory;
2. **WAL snapshot record** — `snapshotType` record carrying index/term/configuration metadata;
3. **WAL committed HardState** — separate persistent state used to bound which WAL snapshot entries count as valid;
4. **snapshot-file admission evidence** — successful decode/CRC plus `(term,index)` match against valid WAL snapshot entries;
5. **live Ready / MemoryStorage state** — process-memory progress that comes after local stable save in the Ready pipeline;
6. **application/server publication state** — later publication boundary already documented by the parent deepening;
7. **older recovery-resource retention state** — material not yet released after the replacement boundary.

A compact v3.5.15 restart relation is:

```text
snapshot artifact
    + matching WAL snapshot record
    + WAL record valid relative to committed HardState
    -> admissible local restart snapshot
```

That is an implementation reconstruction over directly inspected source; it is not asserted as universal Raft protocol law.

## Engineering reconstruction

### E — durable snapshot embodiment ≠ durable restart anchor

The file-first ordering means the full snapshot artifact can cross its own file-sync boundary while the corresponding WAL record has not yet crossed the WAL sync boundary.

Therefore:

```text
snapshot bytes persisted by the snapshotter path
    != WAL-side restart marker persisted
```

The implementation explicitly tolerates the first state as an orphan-file outcome.

### E — successful local snapshot publication has a two-representation persistence frontier

For this exact `SaveSnap` path, success is not reached at the snapshot file's file sync. It includes a later WAL record encode and WAL `fdatasync` request.

A useful project model is:

```text
payload/materialized-state persistence frontier
    -> WAL restart-anchor persistence frontier
    -> later live/application publication frontiers
```

These frontiers are ordered here but not atomic.

### E — the chosen asymmetry is conservative with respect to restart authority

The source chooses to tolerate:

```text
extra materialized artifact
    without authority marker
```

rather than:

```text
authority marker
    without corresponding materialized artifact
```

Combined with restart matching, this means the admitted partial state tends toward **under-recognition of a newer artifact** rather than **recognition of an absent artifact**.

This is a local failure-policy observation, not a proof about every possible corruption scenario.

### E — file visibility ≠ recognition as a continuation point

The restart code makes “current enough to recover from” a relation among multiple persisted structures. A file's continued physical existence is insufficient if the WAL-side evidence needed to recognize its boundary is absent.

This is a particularly clean technical-retention example of:

```text
embodiment survival
    != recognized continuity
```

### E — WAL snapshot marker ≠ snapshot payload

The marker records boundary/configuration metadata and participates in restart matching. It is not the full state-machine image.

Therefore:

```text
control evidence retained
    != payload retained

payload retained
    != control evidence retained
```

Both representations matter, but for different reasons.

### E — WAL marker sync ≠ universal physical power-loss proof

`fdatasync` is an operating-system/storage-stack contract boundary invoked by etcd. The source does not prove behavior of every filesystem, controller cache, SSD firmware, device power-loss-protection design, or faulty hardware path.

The supported claim is source-level ordering and requested synchronization, not metaphysical certainty that electrons have reached a particular physical medium under every failure mode.

## Crash-window matrix

The directly inspected ordering supports this bounded matrix:

| Failure point | Snapshot file | matching WAL record | restart implication supported by source |
| --- | --- | --- | --- |
| before snapshot-file save succeeds | not established by this path | not written by this call | new snapshot not established |
| after snapshot-file sync, before WAL record is encoded/synced | may exist | may be absent | orphan snapshot is explicitly anticipated |
| after WAL record encode but before WAL sync returns | file exists | record may be only partially/not durably represented | do not treat successful `SaveSnap` as established |
| after normal `WAL.SaveSnapshot` success | file save succeeded | WAL record passed through encoder flush + `fdatasync` | local stable-save stage may return success |
| restart with file but no valid matching WAL entry | file exists | no admissible matching entry | `LoadNewestAvailable` does not select it |
| restart with matching WAL entry newer than committed HardState | file may exist | filtered out by `ValidSnapshotEntries` | not a valid restart marker under this function |

The table does **not** claim exhaustive crash correctness for all lower-layer storage behaviors.

## Functional analogies and boundaries

### A — checkpoint artifact + commit/manifest record

Many storage systems separate a bulk checkpoint artifact from a smaller record that establishes which artifact is current or admissible. etcd v3.5.15 is functionally comparable at that abstract level.

But this packet does not claim direct genealogy from database manifests, ARIES, LSM manifests, filesystem superblocks, or any other named system.

### A — Case 100 completion-publication barrier

Case 100's later OpenZFS witness separates internal “finished” state from the txg boundary that must be crossed before completion is safely reported. Case 58 here separates a snapshot file's own persistence point from the later WAL-side restart-anchor sync.

The bounded analogy is:

```text
one representation/stage complete
    != whole publication contract complete
```

The mechanisms remain different:

- etcd uses a snapshot artifact plus WAL record and restart matching;
- OpenZFS uses txg synchronization and scan-completion reporting.

No common lineage is claimed.

## Bounded philosophical interpretation

The narrow interpretive point is that preservation is relational. A materialized state artifact can physically survive while the system intentionally refuses to treat it as the current recovery point because a separate recognition relation did not survive or was never completed.

For this implementation:

```text
something survived
    != the system knows it may continue from that thing
```

That is a philosophy-of-technical-objects reading of concrete source behavior, not vocabulary attributed to etcd developers.

## Explicit non-claims

This deepening does **not** claim that:

1. etcd v3.5.15 defines universal Raft snapshot storage semantics;
2. the 2014 Raft paper prescribed this file-before-WAL-marker sequence;
3. a `walpb.Snapshot` contains the full snapshot payload;
4. the `.snap` file and WAL snapshot record are interchangeable copies;
5. two ordered sync operations form one atomic transaction;
6. an orphan snapshot file is impossible;
7. an orphan snapshot file is automatically selected on restart;
8. the newest snapshot filename is automatically authoritative;
9. CRC alone establishes continuation authority;
10. matching `(term,index)` alone proves application-level semantic health;
11. every WAL snapshot record is valid regardless of HardState commit position;
12. `fdatasync` proves survival through every hardware/controller/filesystem failure;
13. `unsafeNoSync` provides the same durability contract as the normal path;
14. source-level ordering proves actual crash outcomes without fault injection;
15. the 2026 received-snapshot directory-fsync fix is the same issue as this v3.5.15 local WAL marker sync;
16. WAL snapshot-record persistence closes every directory-entry durability question for the snapshot file;
17. successful local `SaveSnap` is identical to application publication, Ready advancement, or network `InstallSnapshot`;
18. a later etcd release necessarily preserves this exact code organization;
19. etcd invented checkpoint markers, manifest records, or two-artifact recovery protocols;
20. functional similarity establishes direct technical genealogy.

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| etcd v3.5.15 was released 2024-07-19 | H/P | GitHub release metadata | supported |
| `storage.SaveSnap` saves snapshot file before WAL snapshot record | H/P | `storage.go` | supported |
| source explicitly allows an orphan snapshot file in that ordering | H/P | `storage.go` comment | supported |
| `walpb.Snapshot` used here carries index/term/ConfState | H/P | `storage.go`, `record.go` | supported |
| `WAL.SaveSnapshot` encodes a `snapshotType` record and calls `w.sync()` | H/P | `wal.go` | supported |
| normal `w.sync()` flushes encoder and calls `fdatasync` | H/P | `wal.go` | supported |
| unsafe no-sync mode can bypass the `fdatasync` call | H/P | `wal.go` | supported |
| restart obtains WAL snapshot entries before `LoadNewestAvailable` | H/P | `server.go` | supported |
| restart source explicitly acknowledges orphan snapshot files | H/P | `server.go` comment | supported |
| `LoadNewestAvailable` requires file `(term,index)` to match WAL snapshot evidence | H/P | `snapshotter.go` | supported |
| `ValidSnapshotEntries` filters snapshot markers newer than committed HardState | H/P | `wal.go` | supported |
| durable snapshot artifact and durable restart marker are distinct persistence frontiers | E | ordered file/WAL save + sync + restart matching | supported |
| source-level ordered persistence is one atomic transaction | X | explicit orphan state | rejected |
| successful `fdatasync` proves arbitrary physical power-loss survival | X | lower-layer evidence absent | rejected |
| file existence alone establishes restart authority | X | restart matching rule | rejected |

## Related-repository boundary

A search of `tmzncty/computing-archaeology` for `etcd snapshot Raft WAL` returned no dedicated technical-history packet to reuse in this pass.

Accordingly this file keeps only the retention-specific implementation boundary. A broad history of etcd's WAL package, Raft implementation lineage, Linux `fsync`/`fdatasync` history, storage-filesystem semantics, or checkpoint-manifest design belongs in the companion history repository if developed later.

## Remaining evidence debt

This slice closes the previously explicit question **“does v3.5.15 `WAL.SaveSnapshot` cross a sync boundary, and what ordering does it establish?”**

Useful next work is narrower:

- fault-inject immediately before and after `WAL.SaveSnapshot` sync and confirm restart selection behavior;
- inspect actual filesystem behavior in a controlled sudden-power-loss setup rather than inferring hardware survival from the source-level `fdatasync` call;
- follow later etcd releases to determine whether this exact storage organization changed;
- separately track release/backport status of the 2026 received-snapshot directory-fsync correction;
- keep network `InstallSnapshot`, local Ready publication, and local restart selection as separate evidence slices.

No maturity increase is warranted from this implementation deepening alone; **Case 58 remains `grounded`**.