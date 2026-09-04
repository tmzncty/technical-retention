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

### §7 — prior art

The paper states that snapshotting is used in Chubby and ZooKeeper and names log cleaning and log-structured merge trees as incremental alternatives.

**Rejected claim:** `Raft 2014 invented snapshotting/log compaction`.

## Source 2 — official Raft publication index

**The Raft Consensus Algorithm**: <https://raft.github.io/>.

Used only to verify the canonical author-maintained publication path and relationship of the 2014 paper to the broader Raft work. Mechanism claims remain anchored to the paper.

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
