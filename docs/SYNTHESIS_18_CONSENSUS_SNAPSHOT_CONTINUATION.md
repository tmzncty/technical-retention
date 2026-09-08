# Synthesis 18 — Consensus Snapshotting: History Replacement, Continuation Metadata, and State-Transfer Repair

## Status and scope

**Bounded engineering synthesis over already-grounded recovery cases.** This document closes one explicit ROADMAP question:

> In consensus snapshotting, how should committed command history, applied state, stable snapshot payload, log-position/term boundary metadata, cluster configuration, remaining log suffix, follower progress, and state-transfer repair be separated?

The bounded answer is:

> **A committed replicated-log prefix does not have to survive forever as the same command bytes once its effects have been materialized in an admissible stable snapshot and enough continuation state survives to reconnect that snapshot to the remaining protocol history. Snapshot completion can authorize retirement of covered history, but it does not imply that every follower has converged. Once a follower falls behind the retained-history frontier, recovery can change from command replay to state transfer.**

The synthesis is centered on:

- [Case 58 — Raft snapshot/log compaction](../cases/58-raft-snapshot-log-compaction.md), the canonical consensus case;
- [Case 46 — GFS master log/checkpoint recovery](../cases/46-google-gfs-master-log-checkpoint-recovery.md), a checkpoint/replay and re-observation counterexample;
- [Case 71 — ZooKeeper fuzzy snapshot/replay recovery](../cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md), a counterexample to `snapshot = exact historical instant`;
- [Case 57 — Bigtable tablet log/memtable/SSTable recovery](../cases/57-google-bigtable-tablet-log-memtable-recovery.md), a non-consensus materialization analogy.

Historical facts remain in those canonical case and evidence records. The decomposition below is **engineering reconstruction**. Cross-system comparisons are **functional analogies** unless explicitly marked as historical record. This document does not claim that Raft, GFS, ZooKeeper, or Bigtable invented checkpointing, logging, snapshotting, state transfer, or history compaction, and it does not construct a Birrell → Chubby → ZooKeeper/GFS/Bigtable → Raft genealogy.

---

## 1. The mistaken model: one retained log is the state

A simple but misleading model is:

```text
committed commands
    -> retained forever in the replicated log
    -> replay is always possible
    -> followers recover by receiving missing commands
```

The grounded cases break this chain.

Raft 2014 explicitly permits a server to snapshot committed applied state and, after the snapshot is complete, delete the covered log prefix. A follower that later needs entries the leader no longer retains cannot be repaired by ordinary entry replay and instead receives an `InstallSnapshot` state transfer.

GFS 2003 likewise bounds master restart by a latest complete checkpoint plus later operation-log files, while deliberately recovering chunk locations by fresh participant reports rather than from a persistent historical table.

ZooKeeper shows that a snapshot can remain recovery-valid even when it does not correspond to any one historical state, provided ordered idempotent replay and sufficient log coverage close the recovery relation.

Bigtable shows a non-consensus version of the same broad functional pressure: materializing recent committed state into immutable SSTables can reduce how much redo history must be replayed after failure.

Thus the useful question is not simply `is the log retained?` It is:

> **Which representation now carries the authoritative state, what metadata connects it to later history, and which recovery operations remain possible after older history is retired?**

---

## 2. Eight relations that must remain distinct

### 2.1 Committed command history

Question:

> Which ordered commands have crossed the consensus commitment rule?

In the bounded Raft case, only committed entries may be snapshotted. Commitment is therefore a qualification on the history that may be materialized; snapshotting is not the operation that originally makes a speculative entry committed.

Therefore:

```text
entry present in a local log
    != committed entry

entry committed
    != entry must remain forever as original log bytes
```

### 2.2 Applied state

Question:

> Which committed commands have already been incorporated into the state machine's current state?

Raft snapshots the state produced by committed applied history. `commitIndex` and `lastApplied` are distinct from the persistent term/vote/log state in the 2014 paper's Figure 2. The current in-memory state-machine embodiment is also not automatically the same object as a completed stable snapshot.

Therefore:

```text
committed history
    != applied state

applied state in memory
    != completed stable snapshot
```

### 2.3 Stable snapshot payload

Question:

> Which materialized current state has been written into a recovery representation that may substitute for detailed prefix replay?

The snapshot payload carries the state-machine result of the covered committed prefix. It is a replacement recovery representation, not another copy of every command that produced it.

Therefore:

```text
snapshot payload
    != original command sequence
```

And because lower storage is outside the bounded Raft algorithm:

```text
called stable storage by protocol paper
    != independently proven filesystem/device power-fail behavior
```

### 2.4 Continuation / boundary metadata

Question:

> Where does the materialized state reconnect to the surviving ordered history?

Raft retains `last included index` and `last included term`. These summarize the boundary necessary for later `AppendEntries` consistency and `InstallSnapshot` handling.

They are not a compressed copy of all deleted commands. They answer a different question: how the retained materialized state joins the remaining log lineage.

Therefore:

```text
boundary metadata
    != replaced history

snapshot payload alone
    != complete Raft continuation state
```

### 2.5 Effective cluster configuration

Question:

> Which membership state must remain valid after the log entry that established it may itself be compacted away?

The 2014 Raft snapshot carries the latest cluster configuration at the snapshot boundary. This is a direct example of a protocol relation whose current effect must survive even when the historical command that produced it no longer does.

Therefore:

```text
configuration-entry bytes retired
    != effective membership forgotten
```

### 2.6 Remaining log suffix

Question:

> Which commands after the snapshot boundary still remain in detailed ordered form?

A snapshot does not normally mean `no log exists`. The covered prefix may be retired while later entries remain and continue the replicated history.

Thus:

```text
history compacted
    != all history discarded

snapshot current state
    + continuation metadata
    + later log suffix
    -> one recovery composition
```

### 2.7 Follower progress relative to the retained-history frontier

Question:

> Does a follower still need only entries that the leader retains, or has compaction overtaken it?

Follower lag is relational. A follower may be behind yet still repairable by ordinary `AppendEntries` as long as the needed prefix remains. The same numerical lag can become a different recovery problem once the leader has compacted past the follower's next required entry.

Therefore:

```text
follower lag
    != data loss

follower lag
    + needed entries compacted
    -> replay path unavailable
```

### 2.8 Repair mode and post-repair convergence

Question:

> Does recovery transmit missing history, or a replacement materialized state, and has the recipient actually converged afterward?

Raft changes repair mode when replay history is no longer available:

```text
needed entry retained
    -> AppendEntries replay

needed entry compacted
    -> InstallSnapshot state transfer
    -> reconcile/discard local history as required
    -> resume replication after boundary
```

The decision that a snapshot should supersede local history precedes completion of the physical transfer and subsequent catch-up.

Therefore:

```text
snapshot is authoritative recovery source
    != follower already converged
```

---

## 3. History can be retired only after a representation handoff

### Historical record inherited from Case 58

Raft Section 7 says each server independently snapshots only committed entries. After a snapshot has been completely written, the server may delete log entries through the last included index and may delete the previous snapshot.

### Engineering reconstruction

The bounded handoff is:

```text
committed prefix
    -> applied state
    -> complete stable snapshot
       + lastIncludedIndex
       + lastIncludedTerm
       + effective configuration
    -> covered prefix becomes dispensable
```

The important relation is not `snapshot = backup`. It is **replacement of one recovery representation by another under an admissibility condition**.

The ordering matters:

```text
retire sole source first
    -> unsafe handoff

complete replacement first
    -> covered source may become dispensable
```

This pattern is functionally comparable to Bigtable compaction and GFS checkpointing, but those systems do not inherit Raft's consensus term/membership continuation rules.

---

## 4. Compaction changes the future repair protocol

The most retention-specific consequence of consensus snapshotting is not merely reduced disk usage. It changes what future recovery is able to transmit.

Before the compaction frontier overtakes a follower:

```text
leader retains missing entry sequence
    -> follower can learn history by replay
```

Afterward:

```text
leader no longer retains missing prefix
    -> exact command replay from leader is impossible
    -> follower receives state materialization instead
```

The system has not simply forgotten `irrelevant bytes`. It has deliberately changed the **geometry of future repair**.

This yields a reusable guardrail:

> **A history-retirement decision can preserve current-state recoverability while simultaneously removing one future reconstruction path.**

Retention is therefore not monotonic in the sense `more detailed history is always necessary`, nor in the sense `once a snapshot exists, history no longer matters`.

---

## 5. State transfer can supersede physically surviving local history

Raft's `InstallSnapshot` receiver rules are a second counterexample to material maximalism.

If the follower has a log entry matching the snapshot's last included index and term, it may retain later compatible entries. Otherwise the installed snapshot can supersede the follower's whole local log, including physically surviving entries that are not part of the current authoritative lineage.

Therefore:

```text
longer surviving local log
    != stronger authority

surviving local history
    != history that must be preserved during recovery
```

This agrees functionally with Synthesis 17's Kafka result that a longer suffix may be less authoritative, but the protocols are not historically or mechanically identical. Raft snapshot installation is a consensus state-transfer contract; Kafka leader-epoch truncation is a different replicated-log recovery mechanism.

---

## 6. Counterexample: ZooKeeper fuzzy snapshots

Case 71 prevents this synthesis from silently turning `snapshot` into one universal semantics.

ZooKeeper's bounded fuzzy snapshot can contain a subset of updates that occurred after snapshotting began and may correspond to **no actual point-in-time tree state**. The snapshot-start zxid is a conservative replay boundary rather than a claim that no later effects are embodied in the file. Ordered idempotent replay supplies the temporal closure that makes the fuzzy image recovery-valid.

Therefore:

```text
snapshot
    != necessarily exact historical instant

snapshot boundary
    != necessarily maximum update already embodied in payload
```

Raft's bounded argument is different: it snapshots committed applied state and retains consensus continuation metadata. ZooKeeper's fuzzy image relies on its own replay semantics.

The shared functional question is only:

> What additional retained relation makes this materialized image a valid recovery base?

The answers differ.

---

## 7. Counterexample: GFS checkpoint plus re-observation

Case 46 prevents another overgeneralization: `checkpoint + later log = all recovered control state`.

GFS persists namespace and file-to-chunk mutation history through the operation log and checkpoints, but it deliberately does **not** persist chunk replica locations as authoritative master metadata. After restart those locations are re-observed from surviving chunkservers.

GFS also distinguishes a complete checkpoint from an incomplete physically present one; recovery skips incomplete checkpoints.

Therefore:

```text
checkpoint file exists
    != recovery-admissible checkpoint

important metadata
    != necessarily replayed/persisted metadata

replay recovery
    != re-observation recovery
```

The consensus-snapshot synthesis should therefore not become a universal theory that every current relation must survive in snapshot bytes.

---

## 8. Functional analogy: Bigtable materialization without consensus snapshot semantics

Case 57 offers a useful non-consensus comparison.

Bigtable first commits mutations to a GFS-backed commit log, then inserts them into a volatile memtable. Minor compaction materializes frozen memtable state into an immutable SSTable and reduces the amount of commit-log history that future recovery must replay. `METADATA` retains the live SSTable set and redo points needed to compose recovery.

The functional analogy is:

```text
recent committed history
    -> materialized current-state representation
    -> future replay horizon can move forward
```

But Bigtable's redo points and SSTable membership are not Raft's `lastIncludedIndex` / `lastIncludedTerm`, and tablet recovery is not a consensus `InstallSnapshot` exchange.

Therefore:

> **history-to-state materialization is older and broader than one consensus protocol, while the exact continuation metadata and repair authority remain system-specific.**

This is a novelty boundary, not a genealogy claim.

---

## 9. Failure and forgetting taxonomy

The synthesis exposes several distinct failures.

### 9.1 Committed history survives but materialized state does not

Recovery can still be possible by replay if enough authoritative log history remains. Snapshot loss is not automatically committed-state loss.

### 9.2 Snapshot payload survives but continuation metadata is lost or wrong

The application bytes may look plausible while the protocol no longer has a valid boundary connecting them to the remaining log. Therefore:

```text
payload-readable snapshot
    != continuation-valid snapshot
```

### 9.3 Effective configuration is omitted while the establishing history is retired

Current state may survive while the protocol forgets which participants constitute the cluster. This is a control-state retention failure, not a user-payload failure.

### 9.4 Follower loses replay access but snapshot transfer remains available

The follower is beyond one repair path, not beyond all repairability.

### 9.5 Snapshot is authoritative but transfer or later catch-up is incomplete

Recovery authority has been decided, but convergence work remains unfinished.

### 9.6 Incomplete checkpoint/snapshot is mistaken for complete

GFS supplies the direct counterexample: physical file presence is not enough for recovery admissibility.

### 9.7 Old history is retained indefinitely

This may preserve more forensic/audit material but defeats the bounded storage/replay-work goal that motivates compaction. More history is not automatically a better current-recovery design.

### 9.8 Covered history is retired before replacement closure

This destroys the handoff relation itself. Logical state may then be unrecoverable even though scattered payload fragments or partial snapshot bytes survive.

History retirement here is **protocol/recovery forgetting**, not proof of secure erase, overwrite, cryptographic erasure, or raw-media sanitization.

---

## 10. Historical record, reconstruction, analogy, interpretation

### Historical record

The canonical case files retain the sourced facts:

- Raft 2014 snapshots committed entries, stores last included index/term and current configuration, deletes covered history only after snapshot completion, and uses `InstallSnapshot` when log replay is unavailable;
- GFS 2003 recovers master state from a latest complete checkpoint plus later operation log while re-observing chunk locations;
- ZooKeeper 2009–2019 can use fuzzy snapshots plus ordered idempotent replay and a bounded retained recovery-file set;
- Bigtable 2006 uses commit log, memtable, immutable SSTables, live-file membership, redo points, and compaction to move the recovery frontier.

### Engineering reconstruction

Terms such as `representation handoff`, `continuation state`, `history-retirement frontier`, `repair-mode change`, and `recovery closure` are project terms used to compare the mechanisms.

### Functional analogy

The systems are compared only where they share a bounded function: replacing some detailed history with a current-state materialization while retaining enough relation state for future recovery.

### Philosophical interpretation

No new philosophical thesis is required to close this roadmap question. A later interpretation may ask what it means for a technical system to preserve `the same state` while deleting the sequence of events that produced it, but that question must remain downstream of the engineering distinctions above.

---

## 11. Prior art and novelty boundary

Case 58 already grounds an earlier floor: Birrell, Jones, and Wobber's 1987 small-database design used an on-disk log, occasional whole-database checkpoints, and checkpoint-plus-log crash recovery; Chubby 2006 combined WAL/snapshotting with a consensus-distributed database log. Raft's own paper names snapshotting in Chubby and ZooKeeper.

Therefore this synthesis makes **no invention claim** for:

- checkpointing;
- log replay;
- materializing current state;
- discarding older history;
- sending state to repair another replica.

The project contribution is narrower:

> **Across grounded cases, the retained object after history compaction is not just `the snapshot`. Recoverability can depend separately on snapshot admissibility, continuation metadata, effective authority/configuration, remaining history, participant progress, and a repair path that may change from replay to state transfer.**

A search of `tmzncty/computing-archaeology` for Raft/snapshot/checkpoint/consensus terms found no dedicated case to reuse during this pass. Broader checkpoint, consensus, state-machine-replication, Chubby/Zab/Raft, and database-recovery genealogy belongs there if developed; this repository keeps only the retention-specific relation decomposition.

---

## 12. Primary-source anchors inherited from canonical cases

1. Diego Ongaro and John Ousterhout, **“In Search of an Understandable Consensus Algorithm (Extended Version)”**, 20 May 2014, official Raft project PDF: <https://raft.github.io/raft.pdf>. Section 7 and Figures 12–13 are the bounded Raft snapshot/`InstallSnapshot` anchors.
2. Sanjay Ghemawat, Howard Gobioff, and Shun-Tak Leung, **“The Google File System,”** SOSP 2003, official Google Research archive: <https://research.google/pubs/the-google-file-system/>. Sections 2.6.2–2.6.3 and 5.1.3 ground checkpoint/log recovery and chunk-location re-observation.
3. Patrick Hunt, Mahadev Konar, Flavio P. Junqueira, and Benjamin Reed, **“ZooKeeper: Wait-free coordination for Internet-scale systems,”** USENIX ATC 2010: <https://www.usenix.org/legacy/events/atc10/tech/full_papers/Hunt.pdf>. Sections 4.1–4.3 ground idempotent replay and fuzzy snapshots.
4. Fay Chang et al., **“Bigtable: A Distributed Storage System for Structured Data,”** OSDI 2006, USENIX: <https://www.usenix.org/legacy/events/osdi06/tech/chang.html>. Sections 5.3–5.4 and 6 ground commit-log/memtable/SSTable recovery and compaction.
5. Andrew D. Birrell, Michael B. Jones, and Edward P. Wobber, **“A Simple and Efficient Implementation for Small Databases,”** SOSP 1987 / DEC SRC Research Report 24: <https://birrell.org/andrew/papers/024-DatabasesPaper.pdf>. Earlier checkpoint-plus-log-replay floor retained through Case 58.
6. Mike Burrows, **“The Chubby lock service for loosely-coupled distributed systems,”** OSDI 2006: <https://www.usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows_html/>. Earlier distributed-service WAL/snapshot floor retained through Case 58.

---

## 13. Compact review checklist

When evaluating a future snapshot/checkpoint case, ask separately:

1. What history has become authoritative before materialization begins?
2. What portion of that history has already been applied to current state?
3. What exactly is written into the snapshot/checkpoint payload?
4. What proves the materialization is complete/admissible?
5. What boundary metadata reconnects it to later history?
6. Which authority or membership state must survive even if the establishing history is removed?
7. Which later history suffix still has to remain?
8. Which replicas/participants are behind that retained-history frontier?
9. Can lagging participants still replay commands, or must they receive state transfer?
10. What work remains after the authoritative recovery boundary is decided?
11. Which metadata is re-observed rather than persisted?
12. Does deleting old history mean logical retirement only, or is any physical sanitization actually established?

If these questions cannot be answered separately, `snapshot`, `checkpoint`, `compaction`, or `recovery` is probably hiding more than one retention relation.

---

## Bounded conclusion

The consensus-snapshotting problem is not adequately described as `save state and truncate the log`.

A more precise retention decomposition is:

```text
committed command history
    -> applied state
    -> admissible stable materialization
       + continuation boundary
       + effective configuration/authority state
    -> covered history may be retired
    -> later suffix remains
    -> follower progress is evaluated against retained-history frontier
       -> replay if history remains
       -> state transfer if history has been compacted
    -> convergence continues after the recovery decision
```

The central result is therefore:

> **Current state can outlive the detailed history that produced it, but only because another retained representation plus continuation relations takes over the work that the retired history used to perform. History retirement preserves one kind of continuity by changing the evidence and repair machinery through which that continuity can later be reconstructed.**
