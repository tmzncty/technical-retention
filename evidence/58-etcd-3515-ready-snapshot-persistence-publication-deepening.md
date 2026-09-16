# Case 58 deepening — etcd v3.5.15 snapshot persistence, publication, and release ordering

## Status

**`bounded deepening complete`**

This file is a **later implementation witness** for Case 58. It does not rewrite the historical 2014 Raft claim. It asks a narrower engineering question:

> In one named production Raft implementation, what distinct representations and publication steps sit between a snapshot appearing in Raft `Ready` and older local recovery material being released?

The bounded target is **etcd v3.5.15**, whose annotated tag resolves to commit `9a5533382d84999e4e79642e1ec0f8bfa9b70ba8`.

## Evidence class

- **H/P — implementation record:** exact released etcd v3.5.15 source.
- **E — engineering reconstruction:** distinctions inferred from explicit call ordering and API contracts.
- **A — functional analogy:** limited comparison with Case 71 ZooKeeper snapshot/replay recovery.
- **P — bounded interpretation:** retention/publication language used by this repository, not terminology claimed from etcd authors.

This is not evidence for every Raft implementation and not a source for the historical origin of snapshotting.

## Exact implementation anchors

### etcd release and Raft library version

The v3.5.15 server module declares `go.etcd.io/etcd/raft/v3 v3.5.15`. The release tag is therefore a useful exact implementation anchor rather than a floating `main` snapshot.

Primary source:

- etcd v3.5.15 `server/go.mod`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/go.mod>

### Raft `Ready` is a staged handoff, not one durable object

In `raft/node.go`, `Ready` separately carries:

- `HardState`, which is to be saved to stable storage before messages are sent;
- `Entries`, likewise to be saved before messages are sent;
- `Snapshot`, which is to be saved to stable storage;
- `CommittedEntries`, which are to be applied to the store/state machine;
- outbound `Messages`;
- `MustSync` for the hard-state/entry write path.

The same API says the application must call `Advance` after retrieving a `Ready`, and describes `Advance` as notification that the application has saved progress up to that `Ready`.

Primary source:

- etcd Raft v3.5.15 `raft/node.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/raft/node.go>

The retention-relevant point is not that `Ready` itself is durable. It is precisely a boundary at which several classes of work still have to happen.

## Historical / implementation record

### H/P — etcd orders stable HardState/Entries before its snapshot path

In `server/etcdserver/raft.go`, the v3.5.15 Ready loop first calls:

```go
r.storage.Save(rd.HardState, rd.Entries)
```

If `rd.Snapshot` is non-empty, it then calls, in order:

```go
r.storage.SaveSnap(rd.Snapshot)
r.raftStorage.ApplySnapshot(rd.Snapshot)
r.publishSnapshot(rd.Snapshot)
```

After the snapshot block it calls:

```go
r.storage.Release(rd.Snapshot)
r.transport.Send(r.processMessages(rd.Messages))
```

and later acknowledges progress through the node's advance path.

Primary source:

- etcd v3.5.15 `server/etcdserver/raft.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/raft.go>

This supplies a named implementation witness for a staged relation:

```text
snapshot appears in Ready
    != stable snapshot path completed
    != in-memory Raft storage advanced to snapshot
    != etcd application/server snapshot publication completed
    != old local recovery resources released
    != outbound messages sent
    != Ready progress acknowledged
```

The arrows are implementation ordering, not a claim that these calls form one transaction.

### H/P — etcd deliberately writes the snapshot file before the WAL snapshot marker

The v3.5.15 `Storage.SaveSnap` implementation constructs a `walpb.Snapshot` carrying snapshot index, term, and configuration state. Its source comment then states the intended ordering directly:

> save the snapshot file before writing the snapshot to the wal

The adjacent comment explains why: this ordering can leave an **orphaned snapshot file**, but is chosen to prevent a **WAL snapshot entry with no corresponding snapshot file**.

The code is:

```go
err := st.Snapshotter.SaveSnap(snap)
if err != nil {
    return err
}
return st.WAL.SaveSnapshot(walsnap)
```

Primary source:

- etcd v3.5.15 `server/etcdserver/storage.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/storage.go>

This is unusually strong evidence because the implementation itself names the asymmetric crash consequence it prefers.

The bounded state relation is:

```text
snapshot file persisted
    -> WAL snapshot marker may be appended

power loss between those steps
    -> orphan snapshot file is an admitted outcome

WAL snapshot marker without corresponding snapshot file
    -> ordering is specifically designed to avoid this outcome
```

The source does **not** describe those two representations as an atomic commit.

### H/P — the snapshot file is checksummed and file-synced before `SaveSnap` returns

`Snapshotter.save` serializes the Raft snapshot, wraps it with a Castagnoli CRC32, and writes the resulting file using `pioutil.WriteAndSyncFile`.

`WriteAndSyncFile` writes the bytes, calls `fileutil.Fsync(f)`, closes the file, and returns the resulting error. Its own contract says it calls Sync before close and guarantees the data is synced if no error is returned.

Primary sources:

- etcd v3.5.15 `server/etcdserver/api/snap/snapshotter.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/api/snap/snapshotter.go>
- etcd v3.5.15 `pkg/ioutil/util.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/pkg/ioutil/util.go>

Therefore, for this exact code path, it is too weak to say merely “a file was written.” The implementation explicitly performs a file sync before successful return.

But this still does not license a universal physical-media claim:

```text
successful file fsync in this implementation
    != proof against every filesystem/controller/drive/power-loss failure mode
```

The exact directory-entry durability and lower storage-stack contract are outside the checked source slice.

### H/P — snapshot admission on restart is stronger than “newest .snap file exists”

The v3.5.15 snapshotter stores a CRC and, when loading, rejects empty data, protobuf decode failure, and CRC mismatch. `LoadNewestAvailable` accepts the newest snapshot only when its `(term,index)` matches one of the WAL snapshot records supplied to it.

Primary source:

- etcd v3.5.15 `server/etcdserver/api/snap/snapshotter.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/api/snap/snapshotter.go>

This is the other half of the file-before-WAL-marker choice. An orphaned snapshot file need not become authoritative merely because it has a newer-looking filename.

The useful distinction is:

```text
snapshot pathname exists
    != snapshot decodes and passes CRC
    != snapshot has a matching WAL snapshot record
    != snapshot is admissible as the restart boundary
```

This is implementation-level admission logic, not a generic Raft rule.

### H/P — release happens after stable save, in-memory ApplySnapshot, and publication

`Storage.Release` is documented as releasing resources older than a snapshot that are no longer needed. In v3.5.15 it:

1. calls `WAL.ReleaseLockTo(snapshot index)`; then
2. calls `Snapshotter.ReleaseSnapDBs`, which removes older `.snap.db` files.

Primary source:

- etcd v3.5.15 `server/etcdserver/storage.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/storage.go>

The Ready loop invokes this only after `SaveSnap`, `raftStorage.ApplySnapshot`, and `publishSnapshot` for a non-empty snapshot.

The retention interpretation is therefore:

```text
replacement representation saved
    -> Raft in-memory snapshot boundary advanced
    -> server/application snapshot publication performed
    -> older local recovery resources become release-eligible
```

Release eligibility is not the same thing as immediate erasure of every old byte, and `ReleaseLockTo` is not a secure-delete primitive.

## Retained-state decomposition

The implementation exposes several state classes that should not be collapsed:

1. **Raft Ready snapshot object** — work handed from the Raft library to the embedding application;
2. **snapshot file** — serialized, checksummed snapshot representation;
3. **WAL snapshot record** — durable relation that identifies a snapshot boundary in WAL history;
4. **HardState and post-boundary WAL entries** — ordinary persistent Raft state/history outside the snapshot file;
5. **in-memory `raft.MemoryStorage` snapshot boundary** — local live Raft-library view after `ApplySnapshot`;
6. **server/application snapshot publication state** — the etcd-side publication step after in-memory Raft apply;
7. **older WAL-file lock / snapshot-DB retention state** — resources whose release is delayed until the newer boundary has crossed earlier steps;
8. **CRC/admission evidence** — evidence used to reject damaged or unmatched snapshot files on load.

A compact project model is:

```text
current committed state
    -> Ready snapshot candidate
    -> synced snapshot file
    -> matching WAL snapshot record
    -> in-memory Raft snapshot apply
    -> etcd-side publication
    -> old recovery-material release eligibility
```

Each arrow is an ordered dependency observed in this implementation. It is not a claim of one indivisible transaction.

## Engineering reconstruction

### E — snapshot file existence ≠ restart authority

A file can survive as an orphan if the process fails before its WAL snapshot record is written. The restart-side matching rule is evidence that physical survival alone is insufficient to make it the selected recovery boundary.

### E — currentness is relational across representations

For this implementation, a useful restart snapshot is not just payload bytes. Its term/index relation must also be represented in the WAL-side snapshot history. This is an implementation-specific example of `payload embodiment != continuation authority`.

### E — durability publication is deliberately asymmetric

The code prefers:

```text
possible orphan snapshot
```

over:

```text
WAL marker referring to absent snapshot
```

That is a failure-policy choice. It preserves a conservative direction of disagreement rather than pretending the two writes are atomic.

### E — in-memory `ApplySnapshot` ≠ disk persistence

`raftStorage.ApplySnapshot` occurs only after `storage.SaveSnap` succeeds in the Ready loop. It changes the live Raft storage view; it is not the operation that makes the snapshot file durable.

### E — stable save ≠ application publication

`publishSnapshot` is a separate later call. Therefore it is unsafe to use “snapshot saved,” “snapshot applied to Raft memory storage,” and “snapshot published to etcd application/server state” as synonyms.

### E — release ≠ original commitment

The release of older WAL locks and `.snap.db` material happens long after the commands were originally committed. It is retention maintenance: retiring recovery representations after a replacement boundary becomes usable.

### E — ordered operations ≠ crash atomicity

The implementation has explicit ordering and an explicit admitted orphan state. That is almost the opposite of evidence for a single atomic snapshot transaction.

## Crash-window boundary

The source supports a bounded crash matrix:

```text
before snapshot-file save succeeds
    -> no new completed snapshot file is established by this path

snapshot file synced, before WAL snapshot record succeeds
    -> orphan snapshot file is explicitly admitted

WAL snapshot record succeeds, before in-memory ApplySnapshot
    -> stable representations may be ahead of current process-memory view

in-memory ApplySnapshot succeeds, before publishSnapshot
    -> Raft library view may be ahead of etcd-side publication

publication succeeds, before Release
    -> replacement is published while older local recovery resources remain retained
```

What happens under every kernel/filesystem/controller/power-loss interleaving is **not** proven by this source slice. In particular, this pass does not claim directory-entry fsync semantics for the snapshot pathname or full sudden-power-loss correctness of the storage stack.

## Functional comparison

### A — etcd/Raft Case 58 and ZooKeeper Case 71

Case 71's ZooKeeper 3.4.14 deepening also separates snapshot admission from transaction-log replay and shows that “newest snapshot pathname” need not equal “newest admissible recovery snapshot.”

The functional analogy is:

```text
materialized snapshot artifact
    + separate continuation/admission evidence
    + later history
    -> recoverable current state
```

The mechanisms are different:

- ZooKeeper 3.4.14 uses its own snapshot serialization/completion/checksum and transaction-log replay rules.
- etcd v3.5.15 uses Raft snapshot metadata, a checksummed synced snapshot file, a WAL snapshot record, and Raft-specific application/continuation machinery.

No shared implementation lineage is claimed.

## Bounded philosophical interpretation

The narrow interpretive point is that “the snapshot” is not one ontologically simple thing in this implementation. The same logical checkpoint crosses several embodiments and authority relations before older history becomes releasable.

That supports a project-level distinction:

```text
representation exists
    != representation is admitted
    != representation is current
    != replacement handoff is complete
    != older representation is safe to retire
```

This is an engineering reading of observed implementation boundaries, not a claim that etcd or Raft authors used this vocabulary.

## Explicit non-claims

This deepening does **not** claim that:

1. etcd v3.5.15 defines universal Raft snapshot semantics;
2. the 2014 Raft paper prescribed etcd's exact local storage ordering;
3. `InstallSnapshot` network transfer is identical to `Storage.SaveSnap` local publication;
4. `Ready.Snapshot` is itself durable;
5. ordered `SaveSnap -> ApplySnapshot -> publishSnapshot -> Release` is one atomic transaction;
6. successful `fsync` proves survival against every lower-layer power-loss failure;
7. the checked code proves snapshot-directory metadata is durably fsynced for every platform/filesystem;
8. every orphan snapshot is harmless under every possible operator/tool workflow;
9. `raftStorage.ApplySnapshot` is the same operation as applying application payload to the full etcd state machine;
10. `publishSnapshot` is a generic Raft concept;
11. `ReleaseLockTo` physically erases old WAL bytes;
12. release of old snapshot DB files is secure deletion;
13. the implementation has no other relevant recovery state outside this bounded source slice;
14. CRC proves semantic correctness of snapshot contents;
15. matching `(term,index)` proves the snapshot represents a healthy application state independently of the surrounding protocol;
16. etcd invented file-before-marker publication, checkpoint/WAL pairing, or snapshot admission;
17. this source establishes direct lineage from Birrell, Chubby, ZooKeeper, or other systems;
18. a later etcd version necessarily preserves this exact ordering.

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| etcd v3.5.15 uses Raft v3.5.15 | H/P | `server/go.mod` | supported |
| Raft `Ready` separates stable state, snapshot, committed entries, and outbound messages | H/P | `raft/node.go` | supported |
| etcd Ready loop saves HardState/Entries before snapshot handling | H/P | `server/etcdserver/raft.go` | supported |
| etcd orders `SaveSnap -> ApplySnapshot -> publishSnapshot -> Release` | H/P | `server/etcdserver/raft.go` | supported |
| `Storage.SaveSnap` writes snapshot file before WAL snapshot record | H/P | `server/etcdserver/storage.go` | supported |
| this ordering explicitly admits orphan snapshot files | H/P | `server/etcdserver/storage.go` comment | supported |
| snapshot file is CRC-wrapped and written through `WriteAndSyncFile` | H/P | `snapshotter.go` | supported |
| `WriteAndSyncFile` calls file fsync before close | H/P | `pkg/ioutil/util.go` | supported |
| loading can require snapshot `(term,index)` to match WAL snapshot records | H/P | `Snapshotter.LoadNewestAvailable` | supported |
| newer pathname alone is insufficient restart authority | E | SaveSnap ordering + matching load rule | supported |
| old recovery resources are released after newer snapshot save/apply/publication in this loop | E/H | Ready loop + `Storage.Release` | supported |
| file/WAL ordering is an atomic transaction | X | explicit orphan allowance | rejected |
| successful file fsync proves arbitrary physical-media power-loss durability | X | lower layers not established | rejected |
| local etcd snapshot publication is identical to Raft `InstallSnapshot` | X | different code/roles | rejected |

## Source ledger

1. etcd v3.5.15 tag / commit anchor: <https://github.com/etcd-io/etcd/tree/v3.5.15> — annotated release tag resolving to commit `9a5533382d84999e4e79642e1ec0f8bfa9b70ba8`.
2. etcd v3.5.15 `server/go.mod`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/go.mod> — exact Raft module version.
3. etcd v3.5.15 `raft/node.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/raft/node.go> — `Ready` fields and `Advance` contract.
4. etcd v3.5.15 `server/etcdserver/raft.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/raft.go> — production Ready-loop ordering.
5. etcd v3.5.15 `server/etcdserver/storage.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/storage.go> — snapshot-file-before-WAL-marker ordering and release path.
6. etcd v3.5.15 `server/etcdserver/api/snap/snapshotter.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/api/snap/snapshotter.go> — CRC, synced snapshot-file path, matching-load admission, and older snap-DB release.
7. etcd v3.5.15 `pkg/ioutil/util.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/pkg/ioutil/util.go> — write + file fsync + close helper.
8. Case 58 grounding: [`58-raft-2014-snapshot-log-compaction-grounding.md`](58-raft-2014-snapshot-log-compaction-grounding.md) — 2014 protocol-level historical record kept separate from this later implementation witness.
9. Case 71 canonical/evidence — ZooKeeper comparison is functional only, not a genealogy claim.

A search of `tmzncty/computing-archaeology` for Raft, `InstallSnapshot`, snapshot compaction, and etcd found no dedicated reusable technical-history module. This file therefore keeps only the retention-specific implementation boundary; a broad etcd/Raft implementation genealogy belongs in the companion repository if later needed.

## Remaining evidence debt

The next useful work is no longer another prose explanation of Raft snapshotting. It is direct fault injection at the identified seams:

- kill/power-fail after snapshot-file sync but before WAL snapshot marker;
- fail after WAL snapshot marker but before `raftStorage.ApplySnapshot`;
- fail after in-memory apply but before `publishSnapshot`;
- fail after publication but before `Release`;
- separately inspect snapshot-directory durability and WAL `SaveSnapshot` fsync semantics on the exact platform under test;
- verify restart selection and orphan cleanup empirically;
- compare exact ordering across later etcd versions only if version drift becomes relevant.

Those experiments would turn the current source-level crash-window reconstruction into fault-injection evidence without conflating Raft protocol rules with filesystem/device behavior.

## 2026 follow-up navigation

A later bounded packet now closes the **received `.snap.db` directory-entry durability sub-question for current upstream in source-level form**: [`58-etcd-2026-received-snapshot-db-directory-fsync-deepening.md`](58-etcd-2026-received-snapshot-db-directory-fsync-deepening.md).

That follow-up compares v3.5.15's `file fsync -> rename -> success` path with upstream commit `cf31e1f6033f0752f0c55d2456a0771be0c5ba80` / PR #22314, which adds a containing-directory fsync after rename and on the existing-file retry path before `SaveDBFrom` may report success and before the snapshot receiver proceeds to Raft message processing. It also preserves the upstream test boundary that SIGKILL/fault-injection control flow is **not** direct proof of unsynced-directory-entry loss.

This does not change the v3.5.15 historical record above, does not establish a released/backported version for the 2026 fix, and does not close the separate WAL `SaveSnapshot` sync-semantics debt.