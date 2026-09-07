# Raft Snapshotting: Committed State Beyond the Replicated-Log Prefix

## Status

**`grounded`** — bounded to the snapshot/log-compaction mechanism described by Diego Ongaro and John Ousterhout in the May 20, 2014 extended Raft paper.

Grounding record: [`../evidence/58-raft-2014-snapshot-log-compaction-grounding.md`](../evidence/58-raft-2014-snapshot-log-compaction-grounding.md).

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

The retention-specific claim is narrower:

> **In the 2014 Raft design, a committed decision need not remain forever as its original replicated log entry. Once a server has materialized the committed state into a stable snapshot and retained the protocol boundary needed to reconnect that state to the remaining log, the covered prefix becomes dispensable. If a follower later needs history the leader has compacted away, repair changes from entry replay to snapshot state transfer.**

`history-retention obligation`, `state-equivalence handoff`, and `recovery-representation substitution` below are project engineering terms, not period Raft vocabulary.

## Historical vocabulary

The paper directly uses `replicated log`, `committed`, `state machine`, `stable storage`, `snapshot`, `snapshotting`, `log compaction`, `last included index`, `last included term`, `configuration`, `InstallSnapshot RPC`, `AppendEntries`, `log cleaning`, and `log-structured merge trees`.

Do not silently normalize these into unrelated monotonically changing metadata such as HDFS generation stamps, QJM epochs, Kafka high watermarks, database LSNs, or generic `checkpoint IDs`.

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

## Retained state and mechanism

The bounded system retains several different state classes:

1. **state-machine state** — the applied current result of committed commands;
2. **remaining replicated-log suffix** — commands after the snapshot boundary;
3. **snapshot boundary metadata** — last included index and term;
4. **effective cluster configuration** — membership needed after the historical entry that established it may disappear;
5. **per-replica progress** — leader knowledge that determines whether ordinary replay or snapshot transfer remains possible;
6. **term/vote/log persistence outside the snapshot relation** — ordinary Raft consensus state not to be collapsed into application payload.

The representation change is:

```text
committed command prefix + current state
    -> stable snapshot(current state, boundary, configuration)
    -> retire covered log prefix
    -> retain later log suffix
```

A lagging-replica repair becomes:

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

## Functional analogies and boundaries

### A — Raft snapshotting and GFS checkpointing

Case 46's GFS master also recovers from a materialized checkpoint plus later log history. The functional analogy is `materialized state can replace some replay history`.

It stops there. GFS's operation log is master metadata history with a different durability/authority contract; Raft's snapshot carries log index/term and membership context for consensus continuation.

### A — Raft snapshotting and Bigtable compaction

Case 57 shows Bigtable minor compaction reducing future dependence on commit-log redo by materializing state into SSTables. Raft likewise reduces detailed-history dependence through materialization.

But Bigtable redo points, memtables, and SSTables are not a consensus log and do not inherit Raft's term/log-matching semantics.

### A — Raft prefix retirement and Kafka failover truncation

Case 56 can truncate a nonauthoritative divergent Kafka suffix after failover. Case 58 normally retires an **authoritative committed prefix** after its result has been materialized. Both deliberately forget log records, but for opposite currentness reasons.

## Failure and forgetting

- **Snapshot creation fails before completion:** the paper's deletion permission is after completion; the old prefix remains the safe source representation.
- **Boundary metadata is lost/wrong:** plausible application bytes alone do not establish a valid continuation point.
- **Follower crosses the compaction frontier:** ordinary replay becomes unavailable, but snapshot transfer can preserve recoverability.
- **Follower retains conflicting uncommitted suffix:** physical survival does not grant authority; the installed snapshot may supersede it.
- **Snapshot too frequent:** extra materialization work consumes bandwidth/energy.
- **Snapshot too infrequent:** log space and replay time grow.
- **Lower-layer failure:** `stable storage` is an assumption of the bounded algorithm description, not proof of filesystem, controller, SSD, or power-loss behavior.

Raft log deletion is therefore **logical/protocol forgetting**, not raw-media sanitization or forensic erasure.

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
```

The arrows above mean **chronological/mechanism comparison only**. They do not assert source-code descent, exclusive influence, invention priority, or an uninterrupted Birrell → Chubby → Raft implementation lineage.

The defensible project contribution is therefore:

> **Raft 2014 supplies a particularly explicit primary-source case in which consensus-ordered committed history is replaceable by stable current state plus boundary/membership metadata, and in which that representation change alters the repair path for lagging replicas. Earlier checkpoint/log-replay and Chubby WAL/snapshot evidence constrain novelty claims without erasing Raft's distinct protocol contract.**

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

A search of `tmzncty/computing-archaeology` for Raft/snapshot/InstallSnapshot and, in this deepening pass, Birrell/Chubby checkpoint terms found no dedicated case to reuse. Broader consensus/checkpoint genealogy should still be routed there if later needed; this repository keeps only the retention-specific mechanism and novelty boundary.

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| persistent term/vote/log state is distinct from volatile commit/application progress | H/P | Fig. 2 | supported |
| servers snapshot only committed entries | H/P | §7 | supported |
| snapshot carries current state plus last included index/term and configuration | H/P | §7 | supported |
| complete snapshot permits covered-prefix deletion | H/P | §7 | supported |
| follower behind retained history is repaired with InstallSnapshot | H/P | §7, Fig. 13 | supported |
| installed snapshot can supersede follower-local log history | H/P | §7, Fig. 13 | supported |
| committed state need not retain original command bytes forever | E | §§5.3–5.4 + §7 | supported |
| snapshot metadata is retention infrastructure rather than payload | E | §7 | supported |
| Raft snapshotting is identical to GFS checkpointing or Bigtable compaction | X | comparison above | rejected |
| Raft invented snapshotting/log compaction | X | §7 prior-art discussion | rejected |
| deleting a Raft prefix proves secure media erasure | X | no lower-layer evidence | rejected |

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

## Next evidence

Future work should remain separate rather than silently expanding this bounded case: implementation crash windows and atomic snapshot installation; named production Raft snapshot formats; later membership variants; independent fault injection; application-level snapshot consistency; and composition with filesystem/device persistence semantics.
