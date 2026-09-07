# Case 58 Grounding — Raft 2014 Snapshotting, Log Compaction, and InstallSnapshot

## Purpose

This record grounds [`../cases/58-raft-snapshot-log-compaction.md`](../cases/58-raft-snapshot-log-compaction.md) in the official Ongaro/Ousterhout Raft paper and fixes the novelty boundary before cross-case comparison.

## Bounded claim

The evidence supports this narrow claim:

> In the 2014 Raft design, a server may replace a committed/applied log prefix with a stable snapshot containing current state plus the log-position/term and cluster-configuration metadata needed for continuation. Once snapshot creation completes, the covered prefix can be discarded. A follower that later needs compacted history can recover through `InstallSnapshot`, so history retention and replica repair are coupled but not identical.

It does **not** establish that Raft invented snapshotting, that every production Raft implementation has identical crash semantics, or that logical log deletion sanitizes lower-layer media.

## Source 1 — official extended Raft paper

Diego Ongaro and John Ousterhout, **“In Search of an Understandable Consensus Algorithm (Extended Version)”**, published May 20, 2014. Official PDF: <https://raft.github.io/raft.pdf>.

### Figure 2 — persistent versus volatile state

Figure 2 identifies `currentTerm`, `votedFor`, and `log[]` as persistent state and says they are updated on stable storage before responding to RPCs. It lists `commitIndex` and `lastApplied` as volatile state.

**Grounded boundary:** `commit progress ≠ complete durable representation of committed history`.

### §§5.3–5.4 — commitment and application precede snapshot compaction

Raft's normal replication path establishes commitment and applies committed entries to the state machine. Section 7 then restricts snapshots to committed entries.

**Grounded boundary:** `snapshot creation ≠ original consensus commitment`.

### §7 / Figure 12 — snapshot as history-to-state materialization

Section 7 motivates log compaction because an unbounded log consumes storage and makes replay increasingly expensive. The simplest mechanism described is to write the entire current system state to a stable snapshot and discard the log up through the snapshot point.

Figure 12 depicts the committed prefix replaced by a snapshot while later log entries remain.

**Grounded relation:** `committed state ≠ indefinitely retained command-history bytes`.

### §7 — snapshot boundary metadata

The snapshot retains:

- `last included index`;
- `last included term`;
- the latest cluster configuration as of that boundary.

The paper explains that index/term allow the later log suffix to continue satisfying the `AppendEntries` consistency check.

**Grounded relation:** `snapshot payload ≠ sufficient consensus-continuation state`.

### §7 — deletion follows completed replacement materialization

Once a server completes writing the snapshot it may delete log entries through `last included index` and may delete the previous snapshot.

**Grounded relation:** `completed replacement representation -> covered-prefix dispensability`.

### §7 / Figure 13 — InstallSnapshot when replay history is gone

The paper describes a follower that is so far behind that the leader has already discarded the next entry it needs. The leader sends `InstallSnapshot` instead of replaying nonexistent log history. The RPC carries snapshot bytes plus the last-included index/term.

On receipt, a follower may keep a compatible post-snapshot suffix if it has an entry with the same boundary index/term. Otherwise it discards its existing log because the snapshot supersedes it and the old log may contain conflicting uncommitted entries.

**Grounded relations:** `compacted replay prefix ≠ unrecoverable follower`; `physically surviving local log ≠ consensus authority`; `history compaction can change repair protocol`.

### §7 — cadence and maintenance cost

The authors warn that taking snapshots too often wastes disk bandwidth and energy, whereas taking them too rarely risks storage exhaustion and longer replay. They propose a fixed log-size threshold as a simple trigger and note copy-on-write support as one way to reduce foreground disruption.

**Grounded relation:** `history-retention cost and materialization cost trade against each other`.

### §7 — Raft's own prior-art statement

The paper states that snapshotting is used in Chubby and ZooKeeper and names log cleaning and log-structured merge trees as incremental alternatives.

**Rejected claim:** `Raft 2014 invented snapshotting/log compaction`.

### Earlier mechanism floor — Birrell, Jones, and Wobber 1987

The 1987 paper's publication record and report describe a small database that records updates incrementally on disk in a log, occasionally makes a checkpoint of the entire database, and recovers by restoring an older checkpoint and replaying the later log.

**Grounded boundary:** `checkpoint + suffix replay predates Raft`; `generic database checkpoint/replay ≠ Raft consensus snapshot semantics`.

### Earlier distributed-service floor — Chubby 2006

Chubby §2.10 states that its rewritten database uses write-ahead logging and snapshotting similar to Birrell et al., while its database log is distributed among replicas using a distributed consensus protocol. §2.11 separately describes periodic GFS backup snapshots for disaster recovery and replacement-replica initialization.

**Grounded boundaries:** `pre-Raft consensus-distributed log + snapshotting exists`; `Chubby WAL/snapshot design ≠ demonstrated Raft InstallSnapshot contract`; `database snapshotting ≠ off-cell backup role`.

### Novelty/genealogy guardrail

The direct evidence supports chronological and functional prior-art floors. It does **not** by itself prove source-code descent, exclusive intellectual influence, or an uninterrupted Birrell → Chubby → Raft implementation genealogy.

**Grounded boundary:** `earlier analogous mechanism ≠ proven direct genealogy`.

## Source 2 — official Raft publication index

**The Raft Consensus Algorithm**: <https://raft.github.io/>.

Used only to verify the canonical author-maintained publication path and relationship of the 2014 paper to the broader Raft work. Mechanism claims remain anchored to the paper.

## Source 3 — Birrell/Jones/Wobber 1987 checkpoint + log replay

Andrew D. Birrell, Michael B. Jones, and Edward P. Wobber, **“A Simple and Efficient Implementation for Small Databases”**, SOSP 1987 / DEC SRC Research Report 24. Author-hosted report: <https://birrell.org/andrew/papers/024-DatabasesPaper.pdf>. Institutional publication record: <https://www.microsoft.com/en-us/research/publication/a-simple-and-efficient-implementation-for-small-databases/>.

Used only for the earlier mechanism floor: incremental disk log, occasional whole-database checkpoint, and crash recovery by restoring a checkpoint then replaying the log. No Raft-style consensus metadata is inferred.

## Source 4 — Chubby 2006 WAL/snapshot + consensus-distributed log

Mike Burrows, **“The Chubby lock service for loosely-coupled distributed systems”**, OSDI 2006, USENIX HTML: <https://static.usenix.org/events/osdi06/tech/full_papers/burrows/burrows_html/>.

- §2.10 grounds the rewritten Chubby database's write-ahead logging and snapshotting, its explicit similarity to Birrell et al., and consensus distribution of the database log.
- §2.11 grounds the separate GFS backup-snapshot role.

Used as a pre-Raft distributed-service floor, not as evidence that Chubby implemented Raft's later boundary metadata or `InstallSnapshot` receiver rules.

## Related-repository duplication check

Before drafting, `tmzncty/computing-archaeology` was searched for Raft, `InstallSnapshot`, snapshot, and consensus-log-specific terms. No dedicated Raft snapshot/log-compaction case was found. Broader consensus history should still be routed there if later needed; this repository keeps only the retention-specific mechanism comparison.

## Claim discipline

### Historical record (`H/P`)

Safe claims are limited to what the 2014 paper states: snapshotting only committed entries, stable snapshot state, last-included index/term, effective configuration, deletion after completion, lagging-follower InstallSnapshot recovery, receiver-side supersession rules, and cadence tradeoffs.

### Engineering reconstruction (`E`)

The project may infer that detailed committed history can cease to be constitutive of current recoverability after a valid state-equivalence handoff, and that compaction changes the future repair representation. These are project formulations, not quoted Raft vocabulary.

### Functional analogy (`A`)

Comparison to GFS checkpoints, Bigtable compaction, Kafka failover truncation, or database checkpoints is allowed only at the relational level. Their authority and identity semantics remain different.

### Philosophical interpretation (`I`)

No philosophical claim is needed for grounding this case. Later synthesis may use the case to test whether persistence can include deliberate destruction of authoritative history, but that interpretation must not be back-projected onto the Raft authors.

## Remaining gaps

Not blockers for the bounded grounded status:

- crash-window/atomic-install details of specific implementations;
- named production Raft snapshot formats;
- later membership/configuration variants;
- independent fault-injection validation;
- lower-layer persistence of snapshot files;
- secure deletion/forensic behavior after log compaction.
