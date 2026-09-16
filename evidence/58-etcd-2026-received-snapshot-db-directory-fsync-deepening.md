# Case 58 deepening — etcd received snapshot DB: file fsync, rename, directory fsync, and Raft-message publication

## Status

**`bounded deepening complete`**

This is a later implementation follow-up for [`../cases/58-raft-snapshot-log-compaction.md`](../cases/58-raft-snapshot-log-compaction.md). It closes one storage-layer question left explicit by [`58-etcd-3515-ready-snapshot-persistence-publication-deepening.md`](58-etcd-3515-ready-snapshot-persistence-publication-deepening.md):

> When etcd receives a database snapshot from a peer, is syncing the snapshot file and renaming it into place enough to establish the pathname as a crash-durable recovery representation, or does the containing directory need a separate persistence step before the Raft message is processed?

The bounded comparison is between:

- exact released etcd **v3.5.15** source, used as the earlier implementation witness; and
- upstream etcd commit `cf31e1f6033f0752f0c55d2456a0771be0c5ba80`, merged through PR #22314 on **2026-09-03**, used only as a later main-branch correction witness.

This packet does **not** establish that the 2026 change has shipped in a particular released etcd version or been backported to every supported branch. It also does not rewrite the 2014 Raft paper.

## Evidence classes

- **H/P — implementation record:** exact etcd v3.5.15 source and the later upstream commit/PR.
- **E — engineering reconstruction:** distinctions among data-file sync, namespace mutation, directory-entry durability, receiver success, and later Raft/WAL processing.
- **A — functional analogy:** bounded comparison with other completion/publication barriers in this repository.
- **P — philosophical interpretation:** a narrow claim about recoverability depending on retained relations, not only retained payload bytes.

## Why this slice matters

The prior Case 58 implementation packet already established that one etcd snapshot path is not a single atomic object: snapshot bytes, a WAL-side snapshot record, in-memory Raft state, server publication, and older-resource release are separate stages. It deliberately left a lower-layer caveat:

```text
successful file fsync
    != proven directory-entry durability
    != proof against every sudden-power-loss outcome
```

The 2026 upstream fix is unusually useful because etcd's own developers later identified exactly that missing namespace-persistence seam for the **received database snapshot** path.

The core result is:

```text
file contents synced
    -> rename performed
    != containing directory synced
    != renamed pathname proven durable across the covered crash model

2026 upstream main:
file contents synced
    -> rename performed
    -> containing directory fsynced
    -> only then may SaveDBFrom report success
    -> only then may snapshot receiver process the Raft message
```

This is not a claim that `rename()` lacks atomic namespace semantics. The issue is **persistence of the renamed directory entry**, not whether another process can observe a half-renamed pathname.

## Historical / implementation record

### H/P — etcd v3.5.15 `SaveDBFrom` synced the temporary file before rename

In `server/etcdserver/api/snap/db.go` at tag `v3.5.15`, `Snapshotter.SaveDBFrom` creates a temporary file in the snapshot directory, streams the received database snapshot into it, calls `fileutil.Fsync(f)`, closes the file, and then renames the temporary file to `<index>.snap.db`.

The relevant bounded sequence is:

```text
CreateTemp(snapshot directory)
    -> copy received DB snapshot bytes
    -> fsync(temp file)
    -> close(temp file)
    -> rename(temp, final .snap.db)
    -> return success
```

If the final pathname already exists, v3.5.15 removes the new temporary file and returns success without any directory sync.

Primary source:

- etcd v3.5.15 `server/etcdserver/api/snap/db.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/api/snap/db.go>

The old source comment said the routine “guarantees the save operation is atomic.” That wording is evidence of the implementation's own API description, but it must not be inflated into a proof that the final directory entry had crossed every crash-durability boundary. The later fix is direct evidence that those were distinct concerns.

### H/P — the v3.5.15 snapshot receiver called `SaveDBFrom` before processing the Raft message

In the v3.5.15 snapshot HTTP handler, the receiver first executes:

```go
n, err := h.snapshotter.SaveDBFrom(r.Body, m.Snapshot.Metadata.Index)
```

and returns HTTP 500 on failure. Only after successful return does it call:

```go
h.r.Process(context.TODO(), m)
```

The handler sends the final `204 No Content` only after the Raft message has been processed.

Primary source:

- etcd v3.5.15 `server/etcdserver/api/rafthttp/http.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/api/rafthttp/http.go>

Therefore the code already encoded an ordering intention:

```text
received snapshot DB save succeeds
    -> process associated Raft message
    -> report successful receive
```

The later bug fix changes what “save succeeds” must include before that publication boundary is crossed.

### H/P — Linux documents file fsync and directory-entry persistence as distinct obligations

The Linux `fsync(2)` manual states that calling `fsync()` on a file does not necessarily ensure that the directory entry containing the file has reached disk; an explicit `fsync()` on a file descriptor for the directory is also needed for that purpose.

Primary technical reference:

- Linux man-pages, `fsync(2)`: <https://man7.org/linux/man-pages/man2/fsync.2.html>

This source supplies the operating-system contract cited by the etcd fix. It does not establish identical semantics for every filesystem or operating system.

### H/P — August/September 2026 upstream etcd explicitly identified the missing directory fsync

Commit `cf31e1f6033f0752f0c55d2456a0771be0c5ba80`, later merged by PR #22314 on 2026-09-03, states the issue directly:

- `SaveDBFrom` synced a received snapshot database before renaming it into place;
- it did **not** sync the containing directory;
- syncing a file alone does not necessarily persist its directory entry under the Linux contract;
- the snapshot receiver calls `SaveDBFrom` before processing the Raft message, which can later advance/sync WAL-side snapshot state;
- therefore the directory should be synced before receiver processing continues.

Primary sources:

- commit: <https://github.com/etcd-io/etcd/commit/cf31e1f6033f0752f0c55d2456a0771be0c5ba80>
- merged PR #22314: <https://github.com/etcd-io/etcd/pull/22314>

This is a current implementation correction, not a historical-origin source for Raft snapshotting.

### H/P — the 2026 fix syncs the containing snapshot directory after rename

Current upstream `server/etcdserver/api/snap/db.go` now performs:

```text
write temp file
    -> fsync file
    -> close file
    -> rename temp to final .snap.db
    -> open snapshot directory
    -> fsync directory
    -> return success
```

The helper `fsyncSnapDir` opens the directory and calls `fileutil.Fsync(d)`. The source comment explicitly says the purpose is to make the renamed snapshot database durable, on storage that honors `fsync`, before the snapshot receiver processes the Raft message.

Primary source:

- current upstream `server/etcdserver/api/snap/db.go`: <https://github.com/etcd-io/etcd/blob/main/server/etcdserver/api/snap/db.go>

The bounded claim is about this implementation ordering. It is not a bottom-of-stack guarantee for arbitrary drives/controllers/power failures.

### H/P — a directory-fsync failure now prevents the receiver from publishing success into Raft processing

The 2026 change propagates `fsyncSnapDir` failures from `SaveDBFrom`. The receiver's existing ordering then means a directory-sync failure causes `SaveDBFrom` to fail and the HTTP handler to return before calling `h.r.Process(...)`.

Current upstream receiver source:

- <https://github.com/etcd-io/etcd/blob/main/server/etcdserver/api/rafthttp/http.go>

Thus the later implementation relation is:

```text
snapshot DB bytes copied
    -> file fsynced
    -> final pathname installed by rename
    -> directory fsynced
    -> SaveDBFrom success
    -> Raft message processing may proceed
```

The code does not claim those steps are one transaction.

### H/P — the existing-file retry path also performs directory fsync

The fix does something less obvious than merely adding a sync after a fresh rename. If the destination `.snap.db` already exists, current code removes the newly created temporary file **and still syncs the containing directory before returning success**.

The source explains why: a previous `SaveDBFrom` may have renamed the destination and then crashed before syncing the directory. A retry that merely observes the pathname should not assume the missing persistence action has already happened.

This is direct implementation evidence for a retained obligation that can outlive the call which created the visible pathname:

```text
pathname presently exists
    != proof that the earlier rename crossed the intended persistence boundary

retry observes pathname
    -> re-perform directory sync
    -> only then report success
```

That is a very narrow claim about this recovery/retry path, not a general rule that every existing file requires repeated directory sync.

### H/P — upstream tests intentionally stop short of claiming physical directory-entry loss was simulated

The added unit test injects directory-sync failure and verifies that both the fresh-rename path and existing-file path call the sync hook and propagate errors.

The added E2E source is explicitly conservative. Its comments say the tests cover receiver error/recovery and crash-before-return control flow, but **do not simulate loss of an unsynced directory entry**; the source also states that `SIGKILL` does not test directory-entry durability.

Primary source:

- PR/commit diff: <https://github.com/etcd-io/etcd/pull/22314>

That negative statement is important evidence discipline:

```text
fault-injection/control-flow coverage
    != direct experiment proving a particular filesystem lost the rename
```

## Retained-state decomposition

For this slice, several different things that casual language might call “the snapshot on disk” must remain separate:

1. **received database bytes** — the application/KV database image streamed from the peer;
2. **temporary file contents** — a file embodiment before final naming;
3. **file-content persistence state** — whether the temp file's contents have crossed the file `fsync` boundary;
4. **final pathname / directory entry** — the namespace relation introduced by rename;
5. **directory persistence state** — whether the containing directory has crossed the intended `fsync` boundary after rename;
6. **Raft snapshot message** — protocol metadata/message processed only after `SaveDBFrom` succeeds in the receiver path;
7. **later WAL-side snapshot state** — a separate representation whose exact sync semantics are outside this slice;
8. **HTTP receive completion** — reported only after the Raft message processing path returns successfully.

The key decomposition is:

```text
snapshot payload bytes
    != file object
    != final pathname
    != persisted pathname relation
    != Raft message publication
    != WAL-side continuation evidence
```

The pathname relation is not user payload, but it can still be retention infrastructure because restart/recovery code must be able to find the saved database snapshot by name.

## Engineering reconstruction

### E — file-data durability ≠ namespace durability

A successful `fsync` on the temporary snapshot file addresses the file's data/metadata persistence contract. The later rename changes a directory entry. Under the Linux contract cited by the fix, the containing directory has a separate persistence obligation.

Therefore:

```text
file fsync succeeded
    != renamed directory entry is proven durable
```

This is the central engineering boundary closed by the 2026 follow-up.

### E — rename atomicity ≠ rename crash persistence

The old code comment's `atomic` wording and the later directory-fsync correction are not logically contradictory once two properties are separated:

- **atomic namespace replacement/visibility** — observers do not have to see a half-renamed name;
- **durability across the relevant crash model** — the directory mutation has reached the intended persistence boundary.

Therefore:

```text
atomic rename
    != durable rename after crash/power loss
```

This project uses that as an engineering reconstruction. It does not redefine POSIX or claim one universal filesystem behavior.

### E — visible pathname ≠ discharged persistence obligation

The existing-file retry path is especially valuable because it blocks a tempting inference:

```text
I can see the final .snap.db name
    therefore
its earlier namespace update must already be durably published
```

Current etcd refuses that inference in this specific path: it re-syncs the directory before returning success.

### E — receiver completion is a publication boundary layered above filesystem persistence

The HTTP receiver's sequencing means the application-level/protocol step is intentionally gated on storage completion:

```text
storage relation established
    -> Raft message processed
    -> receive success returned
```

The 2026 change strengthens the left-hand predicate from “file synced and renamed” to “file synced, renamed, and containing directory synced.”

That makes `SaveDBFrom` success a **publication gate**, not merely a byte-copy completion marker.

### E — `.snap.db` and `.snap` are different representations and code paths

The previous Case 58 deepening analyzed local Raft `.snap` files plus WAL snapshot records. This slice analyzes the **received KV database snapshot** `.snap.db` path.

They interact in recovery, but they must not be merged:

```text
received database .snap.db
    != local Raft .snap metadata/state snapshot
    != WAL snapshot record
```

The 2026 directory-fsync fix for `.snap.db` does not by itself close every persistence question in the local `.snap`/WAL path.

### E — the remaining debt is now narrower

The earlier evidence asked for a storage-layer pass on both:

1. exact directory-entry durability; and
2. WAL `SaveSnapshot` sync semantics.

This follow-up closes the first question **for current upstream's received `.snap.db` path in bounded form**: the implementation now explicitly performs directory fsync, and its commit explains the intended contract.

It does **not** yet close the second question. Exact WAL snapshot-record write/sync ordering, failure windows, version chronology, and release/backport uptake remain separate research slices.

## Functional analogies and boundaries

### A — bounded comparison with Case 100's completion-publication barrier

Case 100's 2026 OpenZFS deepening showed that an in-memory scan could be logically finished while `zpool wait` still needed to wait for the finishing transaction group to sync.

This etcd slice has a narrower filesystem/protocol form:

```text
rename visible / file bytes synced
    != receiver may safely cross its intended persistence gate
```

The functional commonality is only:

> **a higher-level completion/publication signal can be held back until a lower persistence relation crosses its required frontier.**

No genealogy is claimed. An OpenZFS txg, a POSIX/Linux directory `fsync`, and Raft message processing are technically different mechanisms.

### A — bounded comparison with Case 58's existing file/WAL admission relation

The earlier etcd deepening already showed:

```text
snapshot file exists
    != snapshot is WAL-matched restart authority
```

The present slice adds a lower namespace layer:

```text
snapshot file contents synced
    != final pathname relation durably published
```

Together they produce a layered access/recovery model without claiming one universal transaction:

```text
bytes
    -> file embodiment
    -> namespace relation
    -> continuation/admission relation
    -> protocol publication
```

## Philosophical interpretation

### P — operational persistence includes relations needed to find a surviving embodiment

This case gives a narrow technical reason not to identify retention with substrate survival alone. Even if the received database bytes have been written and the file itself has been synced, a future recovery operation still depends on a retained namespace relation that makes the final snapshot path available after restart.

The bounded interpretation is:

> **A technically retained object may depend on retained relations of designation and access in addition to retained payload.**

This is consistent with the repository's wider separation of physical presence, designation, currentness, and recoverability. It is not a claim that a directory entry is philosophically identical to user data, nor that every naming relation is equally constitutive in every storage system.

## Failure / crash boundaries

A bounded matrix for the old and new paths is:

```text
failure before temp-file fsync succeeds
    -> received file contents have not crossed this path's file-sync boundary

file fsync succeeds, failure before rename
    -> durable temp-file contents may exist without final .snap.db name

v3.5.15: rename succeeds, crash before any containing-directory sync
    -> old code returned success without explicitly establishing directory-entry persistence
    -> exact post-crash pathname outcome depends on lower-layer contract/behavior

2026 upstream: rename succeeds, directory fsync fails
    -> SaveDBFrom returns error
    -> receiver returns before h.r.Process(...)

2026 upstream: rename succeeds, directory fsync succeeds
    -> SaveDBFrom may return success
    -> receiver may proceed to Raft message processing

retry sees existing final pathname
    -> current upstream still fsyncs directory before success
```

The matrix intentionally does not claim a measured probability of name loss, an exact hardware persistence domain, or a universal filesystem outcome.

## Explicit non-claims

This deepening does **not** claim that:

1. etcd v3.5.15 necessarily lost snapshot DB files in real deployments;
2. every crash between rename and directory fsync loses the directory entry;
3. `rename()` is non-atomic;
4. atomic rename implies crash durability;
5. file `fsync` is useless or insufficient for file contents;
6. every operating system/filesystem has exactly the Linux contract cited here;
7. every storage device correctly honors every `fsync` promise;
8. the 2026 upstream commit has shipped in a named etcd release;
9. the fix is backported to all release branches;
10. the 2026 behavior can be projected backward into etcd v3.5.15;
11. either implementation defines the 2014 Raft protocol;
12. `.snap.db`, `.snap`, and WAL snapshot records are the same artifact;
13. directory fsync alone makes the complete snapshot/recovery transaction atomic;
14. directory fsync proves the snapshot payload is semantically correct;
15. directory fsync proves the matching Raft/WAL state has already been persisted;
16. a visible existing pathname proves its previous rename was already durably published;
17. the E2E SIGKILL test directly simulates loss of an unsynced directory entry;
18. the upstream tests prove a real filesystem's power-loss behavior;
19. this slice closes WAL `SaveSnapshot` sync semantics;
20. this slice establishes complete end-to-end sudden-power-loss correctness for etcd snapshots;
21. this slice establishes direct influence from another system or a historical genealogy;
22. the functional comparison to OpenZFS equates txg sync with directory `fsync`.

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| v3.5.15 `SaveDBFrom` fsyncs the received temp file before rename | H/P | v3.5.15 `snap/db.go` | supported |
| v3.5.15 `SaveDBFrom` lacks a containing-directory fsync after rename | H/P | v3.5.15 `snap/db.go` | supported |
| v3.5.15 receiver processes the Raft message only after `SaveDBFrom` succeeds | H/P | v3.5.15 `rafthttp/http.go` | supported |
| Linux documents file fsync and directory-entry persistence as distinct obligations | H/P | Linux `fsync(2)` | supported within Linux contract |
| 2026 upstream commit identifies missing directory fsync as the bug boundary | H/P | `cf31e1f...`, PR #22314 | supported |
| current upstream fsyncs the snapshot directory after rename | H/P | current `snap/db.go` | supported |
| current upstream fsyncs the directory on the existing-file retry path | H/P | current `snap/db.go` | supported |
| a directory-sync error prevents receiver progression to Raft processing | H/P/E | current `db.go` + receiver ordering | supported |
| file fsync proves renamed pathname durability | X | Linux contract + 2026 fix | rejected |
| rename atomicity proves crash persistence | X | persistence distinction | rejected |
| pathname existence proves prior directory-sync obligation was discharged | X | existing-file retry path | rejected |
| SIGKILL E2E test proves unsynced directory-entry loss | X | test source explicitly denies this | rejected |
| 2026 main-branch fix is known to ship in a particular release | X | release/backport check not performed | not established |
| directory fsync closes WAL snapshot-record durability | X | separate representation/path | rejected |

## Source ledger

1. etcd v3.5.15, `server/etcdserver/api/snap/db.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/api/snap/db.go>
   - temp-file write, file fsync, rename, old existing-file behavior, and absence of directory fsync.
2. etcd v3.5.15, `server/etcdserver/api/rafthttp/http.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/api/rafthttp/http.go>
   - `SaveDBFrom` before `h.r.Process` and final HTTP success.
3. Linux man-pages, `fsync(2)`: <https://man7.org/linux/man-pages/man2/fsync.2.html>
   - file sync does not necessarily persist the containing directory entry; explicit directory sync is needed for that contract.
4. etcd commit `cf31e1f6033f0752f0c55d2456a0771be0c5ba80`, **“fix: fsync snap directory when saving a received snapshot db”**: <https://github.com/etcd-io/etcd/commit/cf31e1f6033f0752f0c55d2456a0771be0c5ba80>
   - developer-authored rationale, implementation diff, unit/E2E test boundaries.
5. etcd PR #22314, merged 2026-09-03: <https://github.com/etcd-io/etcd/pull/22314>
   - merged upstream review/provenance for the fix.
6. current upstream etcd `server/etcdserver/api/snap/db.go`: <https://github.com/etcd-io/etcd/blob/main/server/etcdserver/api/snap/db.go>
   - post-rename and existing-file-path directory fsync behavior.
7. current upstream etcd `server/etcdserver/api/rafthttp/http.go`: <https://github.com/etcd-io/etcd/blob/main/server/etcdserver/api/rafthttp/http.go>
   - continued storage-before-Raft-message ordering.
8. Earlier Case 58 implementation packet: [`58-etcd-3515-ready-snapshot-persistence-publication-deepening.md`](58-etcd-3515-ready-snapshot-persistence-publication-deepening.md)
   - local `.snap` / WAL / publication decomposition and the directory-entry caveat this packet narrows.

## Related-repository boundary

A fresh search of `tmzncty/computing-archaeology` for Raft/snapshot material found no dedicated packet to reuse. This file therefore keeps only the retention-specific persistence/publication seam. A broader history of etcd snapshot transport, Linux filesystem crash semantics, or consensus implementation genealogy belongs elsewhere if developed later.

## Result

The useful bounded conclusion is:

```text
retained snapshot bytes
    != durably retained final pathname
    != protocol publication

v3.5.15 received DB path:
file fsync -> rename -> success

2026 upstream received DB path:
file fsync -> rename -> directory fsync -> success -> Raft processing
```

The 2026 correction therefore closes a concrete retention seam that the earlier Case 58 packet had left open: **the namespace relation by which a received snapshot DB is found after restart has its own persistence boundary.** It also narrows the next debt rather than erasing it: WAL `SaveSnapshot` sync semantics, exact crash/fault-injection behavior across the remaining publication stages, and release/backport chronology remain open.