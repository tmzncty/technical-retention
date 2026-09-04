from pathlib import Path

CASE_PATH = "cases/58-raft-snapshot-log-compaction.md"
EVIDENCE_PATH = "evidence/58-raft-2014-snapshot-log-compaction-grounding.md"

CASE_TEXT = r'''# Raft Snapshotting: Committed State Beyond the Replicated-Log Prefix

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

The paper does not claim snapshotting as a Raft invention. Section 7 names **Chubby** and **ZooKeeper** as snapshot users and discusses **log cleaning** and **log-structured merge trees** as alternative compaction techniques. The broader paper also situates Raft among prior consensus/replicated-state-machine work.

The defensible project contribution is therefore:

> **Raft 2014 supplies a particularly explicit primary-source case in which consensus-ordered committed history is replaceable by stable current state plus boundary/membership metadata, and in which that representation change alters the repair path for lagging replicas.**

## Source ledger

1. Diego Ongaro and John Ousterhout, **“In Search of an Understandable Consensus Algorithm (Extended Version)”**, published May 20, 2014, official author/project PDF: <https://raft.github.io/raft.pdf>.
   - Figure 2: persistent versus volatile Raft state.
   - §§5.3–5.4: commitment/application context.
   - §7 and Figures 12–13: snapshotting, retained metadata, covered-prefix deletion, `InstallSnapshot`, receiver behavior, cadence tradeoffs, and prior-art boundary.
2. **The Raft Consensus Algorithm**, official author/project publication index: <https://raft.github.io/>. Used for provenance/publication navigation, not as a substitute for the paper's mechanism details.

A search of `tmzncty/computing-archaeology` for Raft/snapshot/InstallSnapshot/consensus-log terms found no dedicated Raft snapshot case before drafting. This case therefore fills a retention-specific distributed-state gap rather than duplicating an existing engineering history.

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

## Next evidence

Future work should remain separate rather than silently expanding this bounded case: implementation crash windows and atomic snapshot installation; named production Raft snapshot formats; later membership variants; independent fault injection; application-level snapshot consistency; and composition with filesystem/device persistence semantics.
'''

EVIDENCE_TEXT = r'''# Case 58 Grounding — Raft 2014 Snapshotting, Log Compaction, and InstallSnapshot

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
'''

Path(CASE_PATH).parent.mkdir(parents=True, exist_ok=True)
Path(EVIDENCE_PATH).parent.mkdir(parents=True, exist_ok=True)
Path(CASE_PATH).write_text(CASE_TEXT)
Path(EVIDENCE_PATH).write_text(EVIDENCE_TEXT)

# README navigation
p = Path("README.md")
s = p.read_text()
case_link = "- [`cases/58-raft-snapshot-log-compaction.md`](cases/58-raft-snapshot-log-compaction.md) — grounded Raft 2014 snapshot/log-compaction bridge: only committed entries are snapshotted; current state plus `last included index`/`term` and cluster configuration can replace a committed log prefix; lagging followers cross from AppendEntries replay to InstallSnapshot once required history has been compacted away."
ev_link = "- [`evidence/58-raft-2014-snapshot-log-compaction-grounding.md`](evidence/58-raft-2014-snapshot-log-compaction-grounding.md) — Case-58 grounding record: official Ongaro/Ousterhout 2014 Raft paper anchors stable snapshotting, boundary metadata, prefix retirement, InstallSnapshot recovery, cadence costs, and an explicit prior-art boundary against claiming Raft invented snapshotting/log compaction."
lines = s.splitlines()
if CASE_PATH not in s:
    i = next(i for i,l in enumerate(lines) if "cases/57-google-bigtable-tablet-log-memtable-recovery.md" in l)
    lines.insert(i + 1, case_link)
    s = "\n".join(lines) + "\n"
if EVIDENCE_PATH not in s:
    lines = s.splitlines()
    try:
        j = next(i for i,l in enumerate(lines) if "evidence/57-bigtable-2006-log-memtable-sstable-grounding.md" in l)
        lines.insert(j + 1, ev_link)
    except StopIteration:
        j = next(i for i,l in enumerate(lines) if "cases/58-raft-snapshot-log-compaction.md" in l)
        lines.insert(j + 1, ev_link)
    s = "\n".join(lines) + "\n"
p.write_text(s)

# ROADMAP
p = Path("ROADMAP.md")
s = p.read_text()
lines = s.splitlines()
idx = next(i for i,l in enumerate(lines) if l.startswith("- [ ] distributed replication and erasure coding beyond RADOS"))
line = lines[idx]
line = line.replace("Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, 51, 56, and 57", "Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, 51, 56, 57, and 58")
if CASE_PATH not in line:
    sentence = " [`cases/58-raft-snapshot-log-compaction.md`](cases/58-raft-snapshot-log-compaction.md), grounded by [`evidence/58-raft-2014-snapshot-log-compaction-grounding.md`](evidence/58-raft-2014-snapshot-log-compaction-grounding.md), adds a consensus-history materialization regime: only committed Raft entries are snapshotted; current state plus `last included index`/`term` and cluster configuration can replace a stable log prefix; and a follower that falls behind the retained prefix is repaired by `InstallSnapshot` rather than by replaying history the leader no longer keeps. This separates commitment, applied state, retained command history, snapshot boundary metadata, follower progress, and recovery representation."
    line = line.replace(" The broad item stays unchecked", sentence + " The broad item stays unchecked", 1)
lines[idx] = line

idx2 = next(i for i,l in enumerate(lines) if l.startswith("- [ ] append-log / changelog compaction and current-state reconstruction"))
line2 = lines[idx2]
line2 = line2.replace("partially advanced by grounded Cases 42 and 57", "partially advanced by grounded Cases 42, 57, and 58")
if CASE_PATH not in line2:
    sentence2 = " [`cases/58-raft-snapshot-log-compaction.md`](cases/58-raft-snapshot-log-compaction.md), grounded by [`evidence/58-raft-2014-snapshot-log-compaction-grounding.md`](evidence/58-raft-2014-snapshot-log-compaction-grounding.md), adds a consensus-specific history-to-state transition: an authoritative committed prefix can become dispensable after its state-machine result and boundary/membership metadata are captured in a stable snapshot, while a lagging replica may thereafter require state transfer instead of entry-by-entry replay. This is distinct from Kafka's keyed log compaction and Bigtable's memtable/SSTable compaction."
    line2 = line2.replace(" The broad item stays unchecked", sentence2 + " The broad item stays unchecked", 1)
lines[idx2] = line2
s = "\n".join(lines) + "\n"

q = "- [ ] In consensus snapshotting, how should committed command history, applied state, stable snapshot payload, log-position/term boundary metadata, cluster configuration, remaining log suffix, follower progress, and state-transfer repair be separated?"
if q not in s:
    anchor = "- [ ] In log-structured tablet recovery, how should committed redo history, volatile memtable state, immutable materialized files, live-file membership, redo points, replay cost, and deletion-marker retirement be separated?"
    if anchor in s:
        s = s.replace(anchor, anchor + "\n" + q, 1)
maint = "- consensus snapshot/materialization, committed-log-prefix retirement, and lagging-replica state-transfer recovery;"
if maint not in s:
    anchor = "- commit-log replay, memtable materialization, SSTable compaction, live-file membership, and obsolete-file garbage collection;"
    if anchor in s:
        s = s.replace(anchor, anchor + "\n" + maint, 1)
p.write_text(s)

# CASE_INDEX
p = Path("CASE_INDEX.md")
s = p.read_text()
row = "| [Raft Snapshotting: Committed State Beyond the Replicated-Log Prefix](cases/58-raft-snapshot-log-compaction.md) | **grounded** | replicated consensus log + committed/applied state machine + stable snapshot + last-included index/term + cluster configuration + remaining suffix + InstallSnapshot repair | separate committed current state from indefinitely retained command history; snapshot payload from protocol-boundary metadata; physical local-log survival from authority; ordinary replay from snapshot state transfer | [2014 Raft snapshot/log-compaction grounding](evidence/58-raft-2014-snapshot-log-compaction-grounding.md); implementation crash windows, product-specific snapshot formats, later membership variants, and independent fault injection remain separate work |"
if CASE_PATH not in s:
    lines = s.splitlines()
    i = next(i for i,l in enumerate(lines) if l.startswith("| [") and "cases/57-google-bigtable-tablet-log-memtable-recovery.md" in l)
    lines.insert(i + 1, row)
    s = "\n".join(lines) + "\n"
for old,new in [("58 bounded cases","59 bounded cases"),("all 58 cases","all 59 cases"),("fifty-eight bounded cases","fifty-nine bounded cases"),("fifty-eight cases","fifty-nine cases")]:
    s = s.replace(old,new)

matrix_raft = "| Raft replicated-state-machine snapshotting / 2014 bounded regime | committed state-machine state + stable snapshot + `lastIncludedIndex`/`lastIncludedTerm` + cluster configuration + remaining log suffix | local snapshotting of committed entries; stable materialization; covered-prefix deletion; `InstallSnapshot` for followers behind retained history | current service from applied state; lagging replica may recover from state transfer when entry replay is no longer available | log index + term + effective cluster configuration + continuing suffix | committed prefix can be deliberately discarded after snapshot completion; follower local log can be discarded when superseded | snapshot retains current state and continuation boundary rather than the full command history it replaces |"
marker = "\n\n---\n\n## Cross-case findings already supported"
if matrix_raft not in s and marker in s:
    s = s.replace(marker, "\n" + matrix_raft + marker, 1)

findings = r'''
## Case 58 — Raft snapshot/log-compaction findings

605. **Committed state ≠ indefinitely retained command history.** Raft can preserve the result of a committed prefix in a stable state-machine snapshot and later delete the original covered entries.
606. **Snapshot current-state payload ≠ complete protocol-continuation state.** `last included index`, `last included term`, and the effective cluster configuration must accompany the materialized state so replication/membership semantics can continue after the source entries disappear.
607. **Snapshot boundary ≠ history it replaces.** The index/term locate and qualify a compacted prefix; they do not preserve the detailed command sequence of that prefix.
608. **Completed replacement snapshot precedes covered-prefix retirement.** The bounded paper authorizes deletion once snapshot writing completes, making deletion a representation handoff rather than blind history loss.
609. **Log compaction ≠ original commitment.** Consensus commitment and application happen before the later maintenance operation that materializes and retires old history.
610. **Compacted replay prefix ≠ unrecoverable follower.** A follower can remain recoverable after needed log entries disappear if an authoritative snapshot is available for transfer.
611. **History compaction can change the future repair protocol.** A lagging follower ordinarily receives `AppendEntries`; once it falls behind compacted history, repair changes to `InstallSnapshot` state transfer.
612. **Follower lag ≠ data loss.** Lag becomes a recovery-path problem only in relation to the leader's retained-history frontier and available snapshot representation.
613. **Physically surviving follower log ≠ consensus authority.** Installing a newer snapshot can require discarding an entire existing local log when it is superseded or may contain conflicting uncommitted entries.
614. **Compatible post-snapshot suffix ≠ superseded prefix.** If the follower has an entry matching the snapshot's last included index and term, later entries may remain valid even while covered entries are deleted.
615. **Configuration history entry can disappear while effective membership state must survive.** Raft carries the latest configuration as of the snapshot boundary into the snapshot itself.
616. **Snapshot cadence trades retained-history/replay cost against present materialization work.** Too-frequent snapshots waste bandwidth/energy; too-infrequent snapshots grow storage and restart replay cost.
617. **Authoritative committed-prefix forgetting ≠ divergent-suffix truncation.** Raft Case 58 retires already-committed history after state-equivalence handoff; Kafka Case 56 can truncate a nonauthoritative divergent suffix after failover.
618. **Raft snapshotting ≠ GFS checkpointing ≠ Bigtable compaction.** All can substitute materialized state for replay history at a functional level, but their logs, authority rules, metadata, and recovery protocols differ.
619. **Raft log-prefix deletion ≠ secure erase.** Removal from Raft's live recovery representation does not prove lower-layer media sanitization or forensic absence.
620. **Raft 2014 snapshotting ≠ invention of snapshotting/log compaction.** The paper itself names Chubby and ZooKeeper as snapshot users and discusses log cleaning/LSM alternatives; the grounded claim is the Raft-specific consensus/snapshot retention composition.
'''
if "## Case 58 — Raft snapshot/log-compaction findings" not in s:
    s = s.rstrip() + "\n\n" + findings.strip() + "\n"
p.write_text(s)

# Validation
assert Path(CASE_PATH).exists() and Path(EVIDENCE_PATH).exists()
assert CASE_PATH in Path("README.md").read_text()
road = Path("ROADMAP.md").read_text()
assert CASE_PATH in road
assert "Cases 42, 57, and 58" in road
ci = Path("CASE_INDEX.md").read_text()
assert ci.count(CASE_PATH) >= 1
assert "59 bounded cases" in ci
assert "620." in ci
assert matrix_raft in ci
