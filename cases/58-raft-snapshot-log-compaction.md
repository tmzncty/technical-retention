# Raft Snapshotting: Committed State Beyond the Replicated-Log Prefix

## Status

**`grounded`** — historically bounded to the snapshot/log-compaction mechanism described by Diego Ongaro and John Ousterhout in the May 20, 2014 extended Raft paper, with later exact-version implementation deepenings for etcd v3.5.15.

Evidence navigation:

- grounding: [`../evidence/58-raft-2014-snapshot-log-compaction-grounding.md`](../evidence/58-raft-2014-snapshot-log-compaction-grounding.md)
- later implementation deepening: [`../evidence/58-etcd-3515-ready-snapshot-persistence-publication-deepening.md`](../evidence/58-etcd-3515-ready-snapshot-persistence-publication-deepening.md)
- WAL snapshot-marker sync / restart-admission deepening: [`../evidence/58-etcd-3515-wal-snapshot-marker-sync-boundary-deepening.md`](../evidence/58-etcd-3515-wal-snapshot-marker-sync-boundary-deepening.md)

The etcd material does **not** replace the 2014 historical record or raise the case maturity beyond `grounded`; it is a bounded witness for local persistence/publication ordering that the Raft paper intentionally leaves below the protocol level.

## Scope

This case asks one narrow distributed-retention question:

> **When a replicated state machine has already incorporated a committed log prefix, what must remain after that prefix is deliberately discarded, and how can a lagging follower recover once the leader no longer retains the missing entries?**

The bounded mechanism is:

```text
replicated log entry
    -> commitment
    -> application to state machine
    -> independent snapshot of committed state
    -> stable snapshot retains current state
       + last included index
       + last included term
       + effective cluster configuration
    -> covered log prefix may be discarded

follower later falls behind retained history
    -> ordinary AppendEntries replay cannot supply missing prefix
    -> leader sends InstallSnapshot
    -> follower installs materialized state
    -> incompatible/superseded local history can be discarded
    -> replication continues from the snapshot boundary
```

This is not a general history of consensus, Paxos, ZooKeeper, Chubby, etcd, Consul, databases, or checkpointing. It does not claim that Raft invented snapshots, log compaction, state-machine replication, or state transfer. The paper itself names Chubby and ZooKeeper as systems using snapshotting and discusses log cleaning and log-structured merge trees as alternatives.

The retention-specific historical claim is narrower:

> **In the 2014 Raft design, a committed decision need not remain forever as its original replicated log entry. Once a server has materialized the committed state into a stable snapshot and retained the protocol boundary needed to reconnect that state to the remaining log, the covered prefix becomes dispensable. If a follower later needs history the leader has compacted away, repair changes from entry replay to snapshot state transfer.**

The later etcd v3.5.15 deepenings ask separate questions: how one production implementation stages stable snapshot bytes, a WAL-side snapshot record, in-memory Raft storage, application/server publication, and release of older recovery resources; and, more narrowly, where the WAL snapshot record crosses its explicit sync boundary and how restart admission joins snapshot files to WAL evidence. These are not projected backward into 2014.

`history-retention obligation`, `state-equivalence handoff`, `recovery-representation substitution`, `publication seam`, and `restart anchor` below are project engineering terms, not period Raft vocabulary.

## Historical vocabulary

The paper directly uses `replicated log`, `committed`, `state machine`, `stable storage`, `snapshot`, `snapshotting`, `log compaction`, `last included index`, `last included term`, `configuration`, `InstallSnapshot RPC`, `AppendEntries`, `log cleaning`, and `log-structured merge trees`.

The later etcd source directly uses `Ready`, `HardState`, `Entries`, `Snapshot`, `SaveSnap`, `SaveSnapshot`, `ApplySnapshot`, `publishSnapshot`, `Release`, `WAL`, `Snapshotter`, `ValidSnapshotEntries`, `LoadNewestAvailable`, and `Advance`.

Do not silently normalize either vocabulary into unrelated monotonically changing metadata such as HDFS generation stamps, QJM epochs, Kafka high watermarks, database LSNs, or generic `checkpoint IDs`.

## Historical record

### H/P — persistent consensus state is distinct from volatile progress state

Figure 2 lists `currentTerm`, `votedFor`, and `log[]` as persistent state on all servers, updated on stable storage before responding to RPCs. `commitIndex` and `lastApplied` are listed separately as volatile state.

This already prevents a shortcut in which `commitIndex` itself is treated as the enduring representation of every committed decision.

**Primary anchor:** Ongaro and Ousterhout 2014, Figure 2.

### H/P — snapshotting comes after commitment and application

A leader advances commitment under Raft's replication/safety rules; servers apply committed entries to their state machines in log order. Section 7 then says each server snapshots independently and snapshots **only committed entries**.

The bounded ordering is therefore:

```text
entry committed
    -> entry applied
    -> current state materialized in snapshot
    -> covered command history may later be retired
```

A speculative local suffix does not become authoritative merely because it physically survives long enough to be snapshotted.

**Primary anchors:** §§5.3–5.4 and §7.

### H/P — snapshotting is introduced to bound log space and replay time

Section 7 says the log cannot grow without bound because it occupies space and takes longer to replay during restart. The simplest compaction approach in the paper is to write the entire current system state to a snapshot on stable storage and then discard the log up to that point. Figure 12 depicts committed log entries replaced by a state snapshot while later entries remain.

**Primary anchor:** §7 and Figure 12.

### H/P — snapshot payload is not enough by itself

Raft retains with the snapshot:

- `last included index`, the final log entry represented by the snapshot and the last applied entry;
- `last included term`, the term of that entry;
- the latest cluster configuration as of the snapshot boundary.

The index and term are needed because the first surviving log entry still participates in the `AppendEntries` consistency relation. Membership state must likewise survive even if the log entry that established it is compacted away.

**Primary anchor:** §7.

### H/P — completed snapshot precedes covered-prefix deletion

The paper says that once a server completes writing a snapshot it may delete all log entries through the last included index and may delete the previous snapshot. The sequence is therefore a replacement handoff, not blind deletion of the only known representation.

**Primary anchor:** §7.

### H/P — compaction can make ordinary replay unavailable to a lagging follower

A follower may fall so far behind that the leader has discarded the next log entry the follower needs. At that point ordinary `AppendEntries` catch-up cannot reproduce the missing history entry by entry from the leader's retained log.

**Primary anchor:** §7.

### H/P — InstallSnapshot substitutes state transfer for missing history replay

Figure 13 and §7 define `InstallSnapshot`. The leader sends snapshot chunks together with `lastIncludedIndex` and `lastIncludedTerm`. A follower installs the newer snapshot and resets its state machine to the received state.

If the follower has an entry matching the snapshot's last included index and term, later entries can remain. Otherwise its existing log is superseded and may contain conflicting uncommitted entries, so the follower discards the whole log.

This gives a direct primary-source counterexample to the idea that a physically longer surviving local log must be more authoritative.

**Primary anchor:** Figure 13 and §7.

### H/P — snapshot cadence is a retention-maintenance tradeoff

The paper says snapshotting too often wastes disk bandwidth and energy, while snapshotting too infrequently risks storage exhaustion and increases replay work. A fixed log-size threshold is presented as a simple practical trigger, and copy-on-write support is suggested to reduce disruption while the state machine writes the snapshot.

**Primary anchor:** §7.

## Later implementation witness — etcd v3.5.15

This section is **not** historical evidence for the 2014 paper. It is an exact-version production implementation witness showing how one Raft system decomposes the local handoff that the paper calls “stable storage.”

### H/P — `Ready` separates work that has not yet crossed the same boundary

etcd v3.5.15 uses `go.etcd.io/etcd/raft/v3 v3.5.15`. In that library, `Ready` separately carries `HardState`, `Entries`, `Snapshot`, `CommittedEntries`, and outbound `Messages`; `Advance` later tells the node that application progress has been saved/processed.

So:

```text
snapshot appears in Ready
    != stable local snapshot path completed
    != application publication completed
    != Ready acknowledged
```

### H/P — the production Ready loop has an explicit publication order

For a non-empty snapshot, `server/etcdserver/raft.go` orders:

```text
Save HardState + Entries
    -> SaveSnap
    -> raftStorage.ApplySnapshot
    -> publishSnapshot
    -> Release older recovery resources
    -> send outbound messages
    -> later advance Ready progress
```

The ordering is directly visible in source. It is not evidence that the sequence is one atomic transaction.

### H/P — snapshot file precedes WAL snapshot record by design

`server/etcdserver/storage.go` deliberately calls `Snapshotter.SaveSnap` before `WAL.SaveSnapshot`. Its source comment states the intended failure asymmetry: this may leave an **orphaned snapshot file**, but avoids a **WAL snapshot entry with no corresponding snapshot file**.

That gives a direct implementation-level distinction:

```text
ordered publication
    != atomic publication

orphan snapshot file can exist
    != orphan file is automatically restart authority
```

### H/P — snapshot bytes are checksummed and file-synced in this path

`Snapshotter.save` wraps serialized snapshot data with a Castagnoli CRC32 and writes it through `WriteAndSyncFile`; that helper writes, calls `fileutil.Fsync`, then closes the file.

This supports the narrow claim that the exact code path performs a file sync before successful return. It does **not** prove every filesystem, directory-entry, controller, drive-cache, or sudden-power-loss behavior.

### H/P — restart admission can require file/WAL agreement

`Snapshotter.LoadNewestAvailable` accepts a snapshot only when its metadata `(term,index)` matches one of the supplied WAL snapshot records. The loader also checks non-empty data, decoding, and CRC.

Thus in this implementation:

```text
newest-looking snapshot pathname
    != decodable/checksummed snapshot
    != WAL-matched snapshot
    != admissible restart boundary
```

This makes the admitted orphan-file state meaningful: physical survival of a file is not by itself sufficient currentness evidence.

### H/P — WAL snapshot record crosses an explicit sync boundary before local `SaveSnap` succeeds

The narrower v3.5.15 follow-up inspects `server/wal/wal.go`. `WAL.SaveSnapshot` validates and encodes a `snapshotType` record and then returns `w.sync()`. In the normal path, `w.sync()` flushes the encoder and calls `fileutil.Fdatasync` on the current WAL file. The separate `unsafeNoSync` mode deliberately bypasses that call.

The server restart path first calls `WAL.ValidSnapshotEntries`, which filters snapshot records relative to the most recent committed HardState, and only then asks `Snapshotter.LoadNewestAvailable` for a file whose `(term,index)` matches the resulting WAL evidence.

Therefore the exact v3.5.15 implementation supports:

```text
snapshot file synced
    != WAL restart marker synced

WAL record observed
    != WAL record valid relative to committed HardState

file physically present
    != admissible restart snapshot
```

**Deepening record:** [`../evidence/58-etcd-3515-wal-snapshot-marker-sync-boundary-deepening.md`](../evidence/58-etcd-3515-wal-snapshot-marker-sync-boundary-deepening.md).

### H/P — old recovery material is released only after the newer boundary crosses earlier steps

`Storage.Release` releases older WAL locks and removes older `.snap.db` files. The Ready loop invokes it after `SaveSnap`, `raftStorage.ApplySnapshot`, and `publishSnapshot`.

This is a local implementation example of replacement-before-retirement. It is not secure erasure, and it is not a universal Raft protocol ordering.

**Deepening record:** [`../evidence/58-etcd-3515-ready-snapshot-persistence-publication-deepening.md`](../evidence/58-etcd-3515-ready-snapshot-persistence-publication-deepening.md).

## Retained state and mechanism

The historical Raft mechanism retains several different state classes:

1. **state-machine state** — the applied current result of committed commands;
2. **remaining replicated-log suffix** — commands after the snapshot boundary;
3. **snapshot boundary metadata** — last included index and term;
4. **effective cluster configuration** — membership needed after the historical entry that established it may disappear;
5. **per-replica progress** — leader knowledge that determines whether ordinary replay or snapshot transfer remains possible;
6. **term/vote/log persistence outside the snapshot relation** — ordinary Raft consensus state not to be collapsed into application payload.

The etcd v3.5.15 implementation deepenings add local representation classes that are **not** claimed as universal Raft state:

7. **Ready snapshot candidate** — work handed from the Raft library to the embedding application;
8. **checksummed snapshot file** — a stable-file embodiment written and synced by the snapshotter path;
9. **synced WAL snapshot record** — a separate boundary/configuration representation written as `snapshotType` and passed through the normal WAL flush + `fdatasync` path before `SaveSnapshot` returns;
10. **WAL committed HardState relation** — restart-side evidence used to filter which WAL snapshot records count as valid;
11. **in-memory Raft snapshot boundary** — live `MemoryStorage` state after `ApplySnapshot`;
12. **server/application publication state** — the later `publishSnapshot` boundary;
13. **old-recovery-resource retention state** — WAL locks and older snapshot DB material not yet released;
14. **snapshot admission evidence** — decoding/CRC plus valid-WAL `(term,index)` matching used when selecting a usable snapshot.

The historical representation change is:

```text
committed command prefix + current state
    -> stable snapshot(current state, boundary, configuration)
    -> retire covered log prefix
    -> retain later log suffix
```

The named etcd implementation exposes a finer local sequence:

```text
Ready snapshot candidate
    -> synced snapshot file
    -> encoded + synced WAL snapshot record
    -> in-memory Raft ApplySnapshot
    -> server/application publication
    -> older recovery resources become releasable
```

A lagging-replica repair remains a different protocol relation:

```text
needed next entry still retained
    -> AppendEntries replay

needed next entry already compacted
    -> InstallSnapshot
    -> install materialized state
    -> preserve compatible later suffix if one exists
    -> otherwise discard superseded local history
    -> resume AppendEntries after boundary
```

Local etcd `SaveSnap` publication and network `InstallSnapshot` must not be merged merely because both involve snapshots.

## Engineering reconstruction

### E — committed state ≠ indefinitely retained command history

Consensus establishes that a command belongs to the committed history, but the exact bytes of that command need not remain forever once their effect has been safely materialized in a snapshot and the continuation boundary survives.

### E — snapshot payload ≠ complete continuation state

A serialized application image without the last included index/term and effective configuration is not equivalent to the Raft snapshot described by the paper. Retention includes protocol metadata that is not user payload.

### E — snapshot boundary ≠ replaced history

`lastIncludedIndex` and `lastIncludedTerm` summarize where the retained state connects to the remaining log. They do not preserve the deleted command sequence itself.

### E — history compaction changes future repair protocol

Before compaction overtakes a follower, missing state can be transmitted as missing commands. Afterward, a materialized state must cross the network instead. The system's decision to forget history therefore changes what future repair must do.

### E — follower lag ≠ data loss

Lag becomes dangerous only relative to the leader's retained-history frontier and availability of a valid snapshot. A follower can be too far behind for command replay yet still recover by state transfer.

### E — physically surviving local history ≠ consensus authority

The receiver rules explicitly permit a newer snapshot to supersede an entire local log. Survival of bytes is not sufficient evidence that those bytes still define current replicated state.

### E — configuration history can be forgotten only if effective membership survives

Compacting the log entry that established a configuration cannot mean forgetting which servers constitute the cluster. The snapshot therefore carries the latest configuration through the boundary.

### E — snapshotting is maintenance of recoverability, not original durability

Snapshot construction consumes bandwidth/energy and bounds later replay/storage cost, but it occurs after commands have already crossed the consensus commitment relation. It should not be retroactively called the original commit event.

### E — file existence ≠ local restart authority

The etcd v3.5.15 file-before-WAL ordering explicitly admits an orphan snapshot file. Its matching-load rule then demonstrates that a physically present file need not be accepted as the restart boundary unless the separate WAL-side relation also exists.

### E — durable snapshot file ≠ durable WAL restart marker

The snapshotter's successful file-sync point occurs before the separate `WAL.SaveSnapshot` call. The latter encodes its own record and crosses the normal WAL flush + `fdatasync` path before local `SaveSnap` returns. The two representations therefore have distinct persistence frontiers.

### E — stable file save ≠ in-memory apply ≠ server publication

The v3.5.15 Ready loop makes these separate calls in order. Treating `SaveSnap`, `raftStorage.ApplySnapshot`, and `publishSnapshot` as synonyms would erase real crash seams.

### E — ordered publication ≠ atomic transaction

The source explicitly prefers one possible partial state—an orphan snapshot file—over the inverse partial state of a WAL marker without its corresponding file. That is a failure-policy choice, not evidence of transaction atomicity.

### E — replacement handoff ≠ physical deletion

`Release` makes older local recovery resources releasable/removable only after the newer snapshot has crossed earlier steps. Releasing locks or deleting older files is not proof of secure media sanitization.

## Functional analogies and boundaries

### A — Raft snapshotting and GFS checkpointing

Case 46's GFS master also recovers from a materialized checkpoint plus later log history. The functional analogy is `materialized state can replace some replay history`.

It stops there. GFS's operation log is master metadata history with a different durability/authority contract; Raft's snapshot carries log index/term and membership context for consensus continuation.

### A — Raft snapshotting and Bigtable compaction

Case 57 shows Bigtable minor compaction reducing future dependence on commit-log redo by materializing state into SSTables. Raft likewise reduces detailed-history dependence through materialization.

But Bigtable redo points, memtables, and SSTables are not a consensus log and do not inherit Raft's term/log-matching semantics.

### A — Raft prefix retirement and Kafka failover truncation

Case 56 can truncate a nonauthoritative divergent Kafka suffix after failover. Case 58 normally retires an **authoritative committed prefix** after its result has been materialized. Both deliberately forget log records, but for opposite currentness reasons.

### A — etcd v3.5.15 snapshot admission and ZooKeeper Case 71

Case 71's ZooKeeper deepening likewise shows that snapshot artifact existence does not alone establish recovery authority. Both systems combine a materialized snapshot with separate continuation/admission evidence and later history.

The mechanisms differ: ZooKeeper 3.4.14 uses its own completion/checksum and transaction-log replay rules; etcd v3.5.15 uses a checksummed synced snapshot file, a synced WAL snapshot record, and Raft-specific metadata/Ready handling. This is a functional comparison only, not a shared implementation or genealogy claim.

## Failure and forgetting

- **Snapshot creation fails before completion:** the paper's deletion permission is after completion; the old prefix remains the safe source representation.
- **Boundary metadata is lost/wrong:** plausible application bytes alone do not establish a valid continuation point.
- **Follower crosses the compaction frontier:** ordinary replay becomes unavailable, but snapshot transfer can preserve recoverability.
- **Follower retains conflicting uncommitted suffix:** physical survival does not grant authority; the installed snapshot may supersede it.
- **Snapshot too frequent:** extra materialization work consumes bandwidth/energy.
- **Snapshot too infrequent:** log space and replay time grow.
- **etcd v3.5.15 fails after synced snapshot file but before WAL snapshot record:** an orphan snapshot file is an explicitly admitted representation state.
- **etcd v3.5.15 fails after WAL record encode but before normal WAL sync returns:** the file and in-process encoded marker can be ahead of the persistence frontier required for successful `SaveSnapshot`; source ordering alone does not license treating the call as completed.
- **etcd v3.5.15 restart sees a file without a valid matching WAL record:** file existence alone does not make it an admissible restart snapshot.
- **etcd v3.5.15 stable representations advance before live process-memory/publication state:** the Ready-loop ordering exposes separate seams rather than one atomic transition.
- **Older recovery resources survive after newer publication:** this is expected until `Release`; coexistence does not mean equal currentness.
- **Lower-layer failure:** `stable storage` in the Raft paper and successful file/WAL sync requests in etcd are not proofs of every filesystem, directory-entry, controller, SSD, or power-loss behavior.

Raft log deletion and etcd local file release are therefore **logical/protocol/storage-lifecycle forgetting**, not raw-media sanitization or forensic erasure.

## Prior art and novelty boundary

### H/P — 1987 checkpoint + log replay is an earlier mechanism floor

Birrell, Jones, and Wobber's 1987 small-database design records updates incrementally in an on-disk log, occasionally checkpoints the entire database, and recovers after a crash by restoring an older checkpoint and replaying the later log. This predates Raft by decades and is direct evidence that `materialized checkpoint + retained suffix replay` is not a Raft invention.

This floor is intentionally narrow. The 1987 paper is a small-database recovery design, not a replicated-consensus snapshot protocol. It does not establish Raft-style `lastIncludedIndex` / `lastIncludedTerm`, membership continuation metadata, or leader-to-follower `InstallSnapshot` semantics.

### H/P — Chubby 2006 combines WAL/snapshotting with a consensus-distributed database log

Burrows's 2006 Chubby paper states that Chubby rewrote its database using write-ahead logging and snapshotting similar to Birrell et al., while the database log was distributed among replicas using a distributed consensus protocol. It separately describes periodic backup snapshots written to GFS for disaster recovery and initialization of replacement replicas.

This is a stronger pre-Raft distributed-system floor than a generic local checkpoint, but the evidence still does not license semantic collapse. The paper does not specify that Chubby's ordinary database snapshot carries Raft's later index/term boundary contract or that lagging replicas use an `InstallSnapshot`-equivalent RPC under identical rules. Chubby's off-cell backup snapshots are also a distinct operational role from the database's snapshot/log mechanism and must not be silently merged with it.

### H/P — Raft itself acknowledges snapshotting prior art

Section 7 of the 2014 Raft paper explicitly says snapshotting is used in Chubby and ZooKeeper and names log cleaning and log-structured merge trees as other compaction approaches. Raft therefore does not present the generic idea of snapshotting/log compaction as its invention.

### E/A — earlier mechanism floor ≠ proven direct implementation genealogy

The historically safe relation is:

```text
1987 Birrell et al.
    checkpoint whole database + replay later log
        -> earlier checkpoint/replay mechanism floor

2006 Chubby
    WAL + snapshotting similar to Birrell
    + database log distributed by consensus
        -> earlier distributed-service floor

2014 Raft
    snapshot committed/applied state
    + lastIncludedIndex / lastIncludedTerm / configuration
    + explicit InstallSnapshot recovery path
        -> a later, explicitly specified consensus-continuation contract

2024 release line witness: etcd v3.5.15
    exact local snapshot-file/WAL/publication/release ordering
    + WAL snapshot-record sync and restart-admission filtering
        -> later implementation deepening, not historical origin evidence
```

The arrows above mean **chronological/mechanism comparison only**. They do not assert source-code descent, exclusive influence, invention priority, or an uninterrupted Birrell → Chubby → Raft → etcd implementation lineage.

The defensible project contribution is therefore:

> **Raft 2014 supplies a particularly explicit primary-source case in which consensus-ordered committed history is replaceable by stable current state plus boundary/membership metadata, and in which that representation change alters the repair path for lagging replicas. Earlier checkpoint/log-replay and Chubby WAL/snapshot evidence constrain novelty claims without erasing Raft's distinct protocol contract; etcd v3.5.15 later shows that an actual local implementation can further decompose “stable snapshot” into multiple ordered, non-atomic embodiments, synced control records, restart-admission relations, and publication stages.**

## Source ledger

1. Diego Ongaro and John Ousterhout, **“In Search of an Understandable Consensus Algorithm (Extended Version)”**, published May 20, 2014, official author/project PDF: <https://raft.github.io/raft.pdf>.
   - Figure 2: persistent versus volatile Raft state.
   - §§5.3–5.4: commitment/application context.
   - §7 and Figures 12–13: snapshotting, retained metadata, covered-prefix deletion, `InstallSnapshot`, receiver behavior, cadence tradeoffs, and Raft's own prior-art boundary.
2. **The Raft Consensus Algorithm**, official author/project publication index: <https://raft.github.io/>. Used for provenance/publication navigation, not as a substitute for the paper's mechanism details.
3. Andrew D. Birrell, Michael B. Jones, and Edward P. Wobber, **“A Simple and Efficient Implementation for Small Databases”**, SOSP 1987 / DEC SRC Research Report 24. Author-hosted report: <https://birrell.org/andrew/papers/024-DatabasesPaper.pdf>; institutional publication record: <https://www.microsoft.com/en-us/research/publication/a-simple-and-efficient-implementation-for-small-databases/>.
   - Direct prior-art floor for incremental on-disk logging, occasional whole-database checkpointing, and crash recovery by checkpoint restore plus log replay.
   - Not evidence for Raft consensus metadata or `InstallSnapshot` semantics.
4. Mike Burrows, **“The Chubby lock service for loosely-coupled distributed systems”**, OSDI 2006, USENIX: <https://static.usenix.org/events/osdi06/tech/full_papers/burrows/burrows_html/>.
   - §2.10: Chubby database rewrite using write-ahead logging and snapshotting similar to Birrell et al.; database log distributed among replicas using consensus.
   - §2.11: periodic backup snapshots to GFS for disaster recovery/replacement-replica initialization, kept separate here from the ordinary database snapshot/log mechanism.
5. etcd v3.5.15 exact release source, `server/go.mod`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/go.mod>.
   - Pins `go.etcd.io/etcd/raft/v3 v3.5.15`.
6. etcd v3.5.15 Raft `Ready` contract, `raft/node.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/raft/node.go>.
7. etcd v3.5.15 production Ready loop, `server/etcdserver/raft.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/raft.go>.
8. etcd v3.5.15 storage wrapper, `server/etcdserver/storage.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/storage.go>.
   - Directly documents snapshot-file-before-WAL-marker ordering and admitted orphan snapshot files.
9. etcd v3.5.15 snapshotter, `server/etcdserver/api/snap/snapshotter.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/api/snap/snapshotter.go>.
   - CRC, synced file write path, WAL-matched loading, and old `.snap.db` release.
10. etcd v3.5.15 file helper, `pkg/ioutil/util.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/pkg/ioutil/util.go>.
   - Write + file fsync + close behavior.
11. etcd v3.5.15 WAL implementation, `server/wal/wal.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/wal/wal.go>.
   - `SaveSnapshot` record encoding, normal flush + `fdatasync` path, `ValidSnapshotEntries`, and restart-boundary validation behavior.
12. etcd v3.5.15 server restart path, `server/etcdserver/server.go`: <https://github.com/etcd-io/etcd/blob/v3.5.15/server/etcdserver/server.go>.
   - obtains valid WAL snapshot entries before `LoadNewestAvailable` and explicitly documents orphan snapshot files.

A search of `tmzncty/computing-archaeology` for Raft/snapshot/WAL and etcd found no dedicated case to reuse. Broader consensus/checkpoint or etcd implementation genealogy should still be routed there if later needed; this repository keeps only the retention-specific mechanism, implementation boundary, and novelty constraint.

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| persistent term/vote/log state is distinct from volatile commit/application progress | H/P | Raft Fig. 2 | supported |
| servers snapshot only committed entries | H/P | Raft §7 | supported |
| snapshot carries current state plus last included index/term and configuration | H/P | Raft §7 | supported |
| complete snapshot permits covered-prefix deletion | H/P | Raft §7 | supported |
| follower behind retained history is repaired with InstallSnapshot | H/P | Raft §7, Fig. 13 | supported |
| installed snapshot can supersede follower-local log history | H/P | Raft §7, Fig. 13 | supported |
| committed state need not retain original command bytes forever | E | Raft §§5.3–5.4 + §7 | supported |
| snapshot metadata is retention infrastructure rather than payload | E | Raft §7 | supported |
| etcd v3.5.15 orders snapshot file before WAL snapshot record | H/P | `storage.go` | supported |
| that ordering explicitly permits orphan snapshot files | H/P | `storage.go` comment | supported |
| v3.5.15 snapshot file path uses CRC + file fsync | H/P | `snapshotter.go`, `util.go` | supported |
| `WAL.SaveSnapshot` encodes a snapshot record and calls the normal WAL sync path before success | H/P | `wal.go` | supported |
| normal WAL sync flushes the encoder and requests `fdatasync` | H/P | `wal.go` | supported |
| valid WAL snapshot records are filtered relative to committed HardState | H/P | `wal.go` | supported |
| a snapshot can be admitted only when `(term,index)` matches valid WAL snapshot history in `LoadNewestAvailable` | H/P | `server.go`, `snapshotter.go` | supported |
| Ready-loop stable save, in-memory apply, publication, and release are distinct stages | H/P/E | `raft.go`, `storage.go` | supported |
| durable snapshot file and durable WAL restart marker are distinct persistence frontiers | E | `storage.go`, `wal.go`, restart path | supported |
| ordered file/WAL writes are an atomic transaction | X | explicit orphan allowance | rejected |
| successful file/WAL sync calls prove every physical power-loss outcome | X | lower-layer evidence absent | rejected |
| local etcd `SaveSnap` is identical to network `InstallSnapshot` | X | distinct code/roles | rejected |
| Raft snapshotting is identical to GFS checkpointing or Bigtable compaction | X | comparison above | rejected |
| Raft invented snapshotting/log compaction | X | §7 prior-art discussion | rejected |
| deleting a Raft prefix or old etcd file proves secure media erasure | X | no lower-layer sanitization evidence | rejected |

## Case findings

1. **Committed state ≠ indefinitely retained command history.**
2. **Snapshot current-state payload ≠ complete protocol-continuation state.**
3. **Snapshot boundary ≠ history it replaces.**
4. **Completed replacement snapshot precedes covered-prefix retirement.**
5. **Log compaction ≠ original commitment.**
6. **Compacted replay prefix ≠ unrecoverable follower.**
7. **History compaction can change future repair protocol.**
8. **Follower lag ≠ data loss.**
9. **Physically surviving follower log ≠ consensus authority.**
10. **Compatible post-snapshot suffix ≠ superseded prefix.**
11. **Configuration history can disappear while effective membership state survives.**
12. **Snapshot cadence trades retained-history/replay cost against materialization work.**
13. **Authoritative committed-prefix forgetting ≠ divergent-suffix truncation.**
14. **Raft snapshotting ≠ GFS checkpointing ≠ Bigtable compaction.**
15. **Raft log-prefix deletion ≠ secure erase.**
16. **Raft 2014 snapshotting ≠ invention of snapshotting/log compaction.**
17. **1987 checkpoint + log replay ≠ replicated-consensus snapshot protocol.**
18. **Checkpoint/replay materialization predates Raft 2014.**
19. **Chubby 2006 WAL + snapshotting + consensus-distributed log ≠ Raft `InstallSnapshot` contract.**
20. **Chubby database snapshotting ≠ Chubby off-cell backup snapshot role.**
21. **Earlier mechanism floor ≠ proven direct Birrell → Chubby → Raft implementation genealogy.**
22. **Raft `Ready` snapshot candidate ≠ completed stable local snapshot publication.**
23. **etcd snapshot file existence ≠ restart authority.**
24. **synced snapshot file ≠ synced matching WAL snapshot record.**
25. **WAL snapshot record observed ≠ valid restart marker relative to committed HardState.**
26. **stable snapshot save ≠ in-memory Raft apply ≠ server/application publication.**
27. **ordered publication ≠ atomic snapshot transaction.**
28. **orphan snapshot file ≠ automatically selected recovery boundary.**
29. **replacement publication ≠ immediate release of older recovery material.**
30. **release of old WAL/snapshot resources ≠ physical secure erasure.**
31. **local etcd snapshot publication ≠ Raft `InstallSnapshot` network state transfer.**
32. **source-level `fdatasync` boundary ≠ universal lower-layer power-loss proof.**

## Next evidence

The broad protocol mechanism is already grounded, and the exact v3.5.15 WAL `SaveSnapshot` sync ordering is now source-grounded. The next useful work should be implementation fault injection rather than another generic Raft summary: inject failure after snapshot-file sync, immediately before/after WAL snapshot-record sync, after in-memory `ApplySnapshot`, after `publishSnapshot`, and before/after `Release`; then observe restart snapshot admission and old-resource retention. A separate storage-layer pass can test actual filesystem/controller sudden-power-loss behavior rather than inferring it from `fsync`/`fdatasync` source calls. Later membership variants, named snapshot formats, cross-version etcd changes, and the release/backport chronology of the 2026 received-snapshot directory-fsync fix should remain separate slices rather than being silently folded into the 2014 historical case.