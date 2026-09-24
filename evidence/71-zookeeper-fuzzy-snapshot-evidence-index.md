# Case 71 Evidence Index — ZooKeeper Fuzzy Snapshot / Replay / Recovery-Set Retention

Canonical case: [`../cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md`](../cases/71-apache-zookeeper-fuzzy-snapshot-replay-recovery.md)

Current maturity: **`grounded`**

This index routes the bounded Case 71 evidence without turning the case into a general history of ZooKeeper, Zab, write-ahead logging, snapshotting, or distributed coordination.

---

## Evidence chain

### 1. Historical and mechanism grounding

[`71-zookeeper-2006-2019-fuzzy-snapshot-grounding.md`](71-zookeeper-2006-2019-fuzzy-snapshot-grounding.md)

Establishes the bounded ZooKeeper recovery relation from project documentation, the 2010 USENIX ATC paper, and release-era administrator material:

```text
committed update history
    -> nonvolatile transaction log
    -> live in-memory tree

periodic fuzzy snapshot
    -> may correspond to no actual single historical tree state

restart
    -> load a complete/admissible snapshot
    -> replay ordered idempotent transactions
    -> reconstruct end-of-log state
```

Also grounds the administrative requirement to retain enough transaction-log coverage around the selected snapshot and the existence of purge policy for retiring older recovery artifacts.

### 2. Exact 3.4.14 snapshot materialization and restart admission

[`71-zookeeper-3414-snapshot-admission-replay-source-deepening.md`](71-zookeeper-3414-snapshot-admission-replay-source-deepening.md)

Exact release anchor: Apache ZooKeeper `release-3.4.14`, commit `4c25d480e66aadd371de8bd2fd8da255ac140bcf`.

Closes the source-level path:

```text
final snapshot.<zxid> pathname chosen
    -> direct serialization to final name
    -> trailing completion marker
    -> lightweight structural filtering
    -> full deserialize/header/checksum admission
    -> fallback from newer rejected candidate to older candidate
    -> replay from selected snapshot boundary + 1
```

Key separations:

```text
snapshot pathname exists
    != serialization reached end marker
    != full snapshot admission
    != snapshot selected for restart
    != replay reached current end state
```

This packet also records that the inspected snapshot path has no explicit `FileChannel.force()` while the transaction-log commit path does when `forceSync` is enabled; that is a source-path difference, not a complete power-failure proof.

### 3. Exact 3.4.14 purge frontier and recovery-set retirement

[`71-zookeeper-3414-purge-recovery-set-retirement-deepening.md`](71-zookeeper-3414-purge-recovery-set-retirement-deepening.md)

Closes the adjacent retirement path:

```text
autopurge policy
    -> PurgeTxnLog
    -> choose N recent snapshot-looking names
    -> oldest chosen name defines purge zxid frontier
    -> preserve newest transaction log whose start <= frontier
    -> preserve all later transaction logs
    -> delete older snapshot/log names outside the retained closure
```

The exact source additionally proves that purge selection and restart admission use different relations:

```text
purge:
    parseable snapshot filename + recency

restart:
    structural validity
    + deserialize/header success
    + checksum success
```

Therefore:

```text
configured snapshot-retention count
    != source-level guarantee of the same number
       of independently restart-admissible snapshot bases
```

The packet deliberately stops short of claiming a production data-loss bug. It records a source-level control asymmetry and leaves destructive fault validation to a later experiment.

---

## Unified retained-state / control chain

The three packets together support this bounded reconstruction:

```text
committed transaction history
    |
    +-> transaction-log embodiment
    |
    +-> live in-memory data tree
            |
            v
       fuzzy snapshot starts at S
            |
            v
       snapshot payload may include
       a temporally mixed subset of later effects
            |
            v
       completion / checksum evidence
            |
            v
       restart-admissible snapshot candidate
            |
            +-> selected boundary S'
            |
            v
       ordered log replay from S' + 1
            |
            v
       reconstructed current state

separate maintenance path:

configured purge policy
    -> recent snapshot-name set
    -> oldest-name purge frontier P
    -> predecessor-log + later-log retained closure
    -> older artifact retirement
```

The important anti-collapse is:

```text
snapshot representation
    != snapshot admission evidence
    != selected replay boundary
    != log-coverage sufficiency
    != purge-policy frontier
    != physical artifact deletion completion
```

---

## Claim-layer discipline

### Historical record

Use ZooKeeper's own vocabulary and exact source behavior:

- `fuzzy snapshot`;
- `transaction log` / replay log;
- `zxid`;
- `snapshot.<zxid>`;
- `lastProcessedZxid`;
- `PurgeTxnLog`;
- `autopurge.snapRetainCount`;
- `autopurge.purgeInterval`;
- `findNRecentSnapshots`;
- `isValidSnapshot`;
- checksum verification;
- preceding transaction-log preservation.

### Engineering reconstruction

Project terms include:

- `recovery-set retention`;
- `snapshot admission`;
- `recovery-set retirement authority`;
- `purge frontier` versus `restart frontier`;
- `representation closure`;
- `historical-instant fidelity`.

These are analytical terms, not claims about ZooKeeper developers' period vocabulary.

### Functional analogy

Allowed comparisons include:

- Raft snapshot/prefix retirement (Case 58);
- Ceph PG-log retirement authority (Case 05);
- Kafka cleaner/checkpoint state (Case 42).

They are mechanism comparisons only. No shared genealogy is implied.

### Philosophical interpretation

A restrained interpretation may say that technical forgetting can require evidence that another surviving representation plus continuation history remains sufficient. It must not turn ZooKeeper's cleanup implementation into a theory of human memory, archives, or forgetting.

---

## Current strongest conclusions

1. A ZooKeeper fuzzy snapshot can be recovery-equivalent without reproducing one actual historical instantaneous tree state.
2. Snapshot filename existence is weaker than restart admission.
3. Restart can fall back from a newer unusable candidate to an older retained snapshot.
4. Snapshot zxid is a conservative replay boundary, not a statement that no later effect appears in the fuzzy payload.
5. Transaction-log file start identifiers do not fully describe the history ranges carried by those files.
6. A log starting before the oldest retained snapshot can still be required for recovery and is therefore preserved by the 3.4.14 purge path.
7. The purge policy counts recent snapshot names, while restart separately validates/adopts snapshot candidates.
8. Current-state recoverability depends on a relation among representation, admission evidence, replay boundary, log coverage, ordered replay semantics, and retained cleanup policy.
9. Older recovery history can be retired once the selected retained closure is sufficient; this is bounded history retention, not indefinite archival retention.
10. Case 71 remains **`grounded`**. The new purge deepening does not justify a maturity promotion.

---

## Open debts

Highest priority:

- exact 3.4.14 file-set fault matrix with recent incomplete/checksum-invalid snapshots followed by autopurge and restart;
- interruption between individual purge `File.delete()` operations;
- observation of the actually admitted restart snapshot and first opened replay log;
- distinguish restart success from reaching the latest zxid and from retaining fallback redundancy.

Secondary:

- exact release-to-release archaeology of when predecessor-log retention entered the purge implementation;
- whether later ZooKeeper releases changed recent-snapshot selection to use stronger validity/admission semantics;
- filesystem/device durability of snapshot publication and deletion;
- broad WAL/snapshot/checkpoint genealogy, which belongs primarily in `tmzncty/computing-archaeology`.

---

## Related-repository routing

A fresh companion search found no dedicated `PurgeTxnLog` / ZooKeeper purge packet in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology).

Keep broad implementation/release history there if it is later developed. Keep this repository focused on the retention-specific relations among:

```text
representation
    -> admission
    -> replay closure
    -> policy frontier
    -> retirement authority
```
