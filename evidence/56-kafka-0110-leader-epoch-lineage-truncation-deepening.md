# Evidence 56B — Kafka 0.11 Leader-Epoch Lineage and Truncation Authority

## Target case

[`cases/56-apache-kafka-replicated-log-high-watermark.md`](../cases/56-apache-kafka-replicated-log-high-watermark.md)

Parent grounding record: [`56-kafka-082-replication-high-watermark-grounding.md`](56-kafka-082-replication-high-watermark-grounding.md).

## Status

**`bounded deepening complete`.**

This slice closes one explicit follow-up left by the Kafka 0.8.2 grounding record:

> What changed when Kafka 0.11 stopped using the follower's recorded high watermark as the normal startup truncation reference and introduced retained leader-epoch lineage for divergence detection and truncation?

The bounded answer is:

> **Kafka 0.11.0.0 separates two relations that the earlier recovery path could conflate: the high watermark remains a committed/visibility frontier, while a per-replica leader-epoch history supplies lineage evidence for deciding where a returning follower may safely truncate. A follower can therefore retain bytes above its recorded high watermark when the current leader's epoch history shows those bytes belong to the same lineage, while a divergent suffix can be removed at the end of the last epoch the leader recognizes.**

This is a source-history and recovery-semantics deepening. It is **not** a claim that KIP-101 solved every Kafka divergence case, that leader epochs are unique to Kafka, or that the checkpoint file itself is an infallible correctness certificate.

---

## Bounded artifacts and dates

- **KIP-101 — “Alter Replication Protocol to use Leader Epoch rather than High Watermark for Truncation”**: accepted Apache design proposal associated with KAFKA-1211.
- **Apache Kafka 0.11.0.0**: released **28 June 2017**.
- **Exact implementation slice**: Apache Kafka source tag `0.11.0.0`, especially `ReplicaFetcherThread.scala`, `LeaderEpochFileCache.scala`, and `LeaderEpochCheckpointFile.scala`.
- **Later corrective boundary**: KIP-279, which documents remaining fast-failover divergence scenarios and changes the epoch comparison protocol. KIP-279 is used as counterevidence against overclaiming KIP-101, not as evidence for 0.11.0.0 behavior.

---

## Historical record

### H — KIP-101 identifies high-watermark truncation itself as a data-loss hazard in one recovery sequence

KIP-101 describes a two-round replication timing relation. A follower may already have fetched a message while its local high watermark still lags because the leader's later acknowledgement/progress information has not yet returned. If that follower restarts, truncates immediately to its recorded high watermark, and is then elected leader before refetching the already-replicated message, the truncation can destroy a message that the old leader had already treated as committed.

The important historical point is narrower than “high watermarks are unsafe.” Kafka continued to use the high watermark after this change. The problem was **using a lagging follower-local high watermark as the normal authority for startup log truncation**.

Primary source:

- Apache Kafka, KIP-101, `Motivation` / `Scenario 1`: <https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=177052956>.

### H — KIP-101 adds lineage state: leader epoch plus the first offset belonging to that epoch

KIP-101 defines a `Leader Epoch` as a monotonically increasing 32-bit identifier for a continuous period of partition leadership. It defines a `Leader Epoch Start Offset` and a `Leader Epoch Sequence File` mapping each epoch to its starting offset.

The proposal's key recovery move is:

```text
follower's latest leader epoch
        +
leader's epoch history
        -> end offset for that epoch on the leader
        -> truncation decision
```

The leader epoch is stamped into replicated message sets, while each replica retains the epoch/start-offset sequence separately.

Primary source:

- Apache Kafka, KIP-101, `Definition of Terms`, `Leader Epoch`, `Add Leader Epoch Sequence File per Partition`: <https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=177052956>.

### H — epoch lineage does not replace the high watermark as the commitment/visibility frontier

KIP-101's title can be misread. It says leader epoch replaces the high watermark **for truncation**, not that the high watermark ceases to exist or ceases to express the replicated committed prefix.

The 0.11.0.0 `ReplicaFetcherThread.processPartitionData` still sets the follower high watermark to:

```text
min(follower log end offset, leader-reported high watermark)
```

The new epoch path is used when a follower is deciding where its local history must converge before ordinary replication resumes.

Primary source:

- Apache Kafka source tag `0.11.0.0`, `core/src/main/scala/kafka/server/ReplicaFetcherThread.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/ReplicaFetcherThread.scala>.

### H — exact 0.11.0.0 code asks the leader about the follower's latest retained epoch

In `ReplicaFetcherThread.scala`, epoch-driven truncation is enabled when the inter-broker protocol supports the relevant 0.11 protocol level. `buildLeaderEpochRequest` reads the follower's latest epoch from its local epoch cache and constructs an `OffsetsForLeaderEpochRequest`.

When the leader returns an epoch end offset, `maybeTruncate` uses three bounded outcomes:

1. if the leader reports an undefined epoch offset, the follower falls back to its high watermark;
2. if the leader's returned epoch end is at or beyond the follower's current log end, no truncation is required;
3. otherwise the follower truncates to the leader-returned epoch end offset.

The exact source therefore supports a stronger distinction than the 0.8.2 case:

```text
follower has a longer suffix
    != suffix is automatically divergent
    != suffix is automatically safe

lineage comparison decides whether and where truncation is required
```

Primary source:

- Apache Kafka source tag `0.11.0.0`, `ReplicaFetcherThread.scala`, `maybeTruncate`, `buildLeaderEpochRequest`, `fetchEpochsFromLeader`.

### H — the retained implementation object is a per-replica `(LeaderEpoch => StartOffset)` cache backed by `leader-epoch-checkpoint`

The exact 0.11.0.0 implementation calls the persistent file `leader-epoch-checkpoint`, even though KIP-101's proposal vocabulary says `Leader Epoch Sequence File` / `leader-epoch-sequence-file`.

`LeaderEpochFileCache`:

- initializes its in-memory epoch list from `checkpoint.read()`;
- accepts monotonically advancing epoch/start-offset assignments;
- flushes the checkpoint when a new valid epoch assignment is appended;
- can remove entries at or beyond a truncation point with `clearAndFlushLatest`;
- can prune older entries when earlier log history is removed with `clearAndFlushEarliest`;
- answers an epoch request with the first later epoch's start offset, or the current log end when the requested epoch is the latest known epoch.

This is not a complete replica-event history. It is a compact retained **lineage-to-offset relation** sufficient for the bounded recovery decision.

Primary sources:

- Apache Kafka source tag `0.11.0.0`, `core/src/main/scala/kafka/server/epoch/LeaderEpochFileCache.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/epoch/LeaderEpochFileCache.scala>.
- Apache Kafka source tag `0.11.0.0`, `core/src/main/scala/kafka/server/checkpoints/LeaderEpochCheckpointFile.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/checkpoints/LeaderEpochCheckpointFile.scala>.

### H — the checkpoint is actively maintained as retained control state, not merely regenerated on every recovery

The generic 0.11.0.0 `CheckpointFile` implementation writes a temporary file, flushes the writer, calls `FileDescriptor.sync()`, and then replaces the old path through `atomicMoveWithFallback`.

That implementation detail is relevant because it shows Apache treating the epoch relation as state worth persistently maintaining across broker-process loss. It does **not** prove filesystem-independent atomicity, power-loss immunity, or identical behavior on every storage stack.

Primary source:

- Apache Kafka source tag `0.11.0.0`, `core/src/main/scala/kafka/server/checkpoints/CheckpointFile.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/checkpoints/CheckpointFile.scala>.

### H — Apache's 0.11 acceptance tests explicitly target the failures described by KIP-101

`EpochDrivenReplicationProtocolAcceptanceTest` says the tests were written to assert that adding leader epochs fixes the KIP-101 problems and includes a toggle that can demonstrate failure under the pre-KIP-101 behavior.

The test suite includes:

- a basic workflow checking that epoch/start-offset entries propagate across leader changes;
- `shouldNotAllowDivergentLogs`, which deliberately damages one broker's local log, creates a new history on that broker, restarts the other broker, and waits for logs to converge;
- `offsetsShouldNotGoBackwards`, which is explicitly documented as reproducible under the pre-KIP-101 protocol setting and checks monotonic offsets after recovery;
- `shouldSurviveFastLeaderChange`, while explicitly noting that the test author could not make the pre-KIP-101 fast-leader-change bug deterministic in that test.

This is valuable implementation-era evidence, but tests are not a proof that all possible failure interleavings are covered.

Primary source:

- Apache Kafka source tag `0.11.0.0`, `core/src/test/scala/unit/kafka/server/epoch/EpochDrivenReplicationProtocolAcceptanceTest.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/test/scala/unit/kafka/server/epoch/EpochDrivenReplicationProtocolAcceptanceTest.scala>.

### H — mixed-version compatibility intentionally retains the older high-watermark truncation path

KIP-101 says the LeaderEpoch request is sent only when all brokers support it; otherwise the existing high-watermark truncation logic remains in use. The exact 0.11.0.0 source similarly gates the request on the inter-broker protocol version and can synthesize an undefined epoch result that leads to the high-watermark fallback.

Thus capability deployment is itself part of the recovery contract:

```text
software binaries contain leader-epoch code
    != cluster is already using leader-epoch truncation
```

Primary sources:

- Apache Kafka, KIP-101, `Compatibility, Deprecation, and Migration Plan`.
- Apache Kafka 0.11.0.0 `ReplicaFetcherThread.scala`.

### H — KIP-101 itself explicitly leaves an unclean-election divergence boundary open

KIP-101 states that the proposal does not protect against all log divergence when `unclean.leader.election.enable=true`; its appendix constructs a history in which alternating isolated leaders can produce divergent epochs below the point visible to the simple one-request comparison.

That boundary is essential. The correct historical claim is **not** “leader epochs solve Kafka divergence.” It is that KIP-101 introduced a stronger lineage-aware truncation relation for the documented 0.11 regime while leaving a known class of histories outside its guarantee.

Primary source:

- Apache Kafka, KIP-101, appendix `Possibility for Divergent Logs with Leader Epochs & Unclean Leader Election`.

### H — KIP-279 later proves that KIP-101 was not the final lineage-comparison design

KIP-279 documents another fast-leader-failover divergence scenario and proposes returning both the largest epoch less than or equal to the requested epoch and that epoch's end offset, potentially repeating the exchange until leader and follower converge on the largest common epoch.

KIP-279 therefore serves as direct later counterevidence to any claim that the 0.11 KIP-101 algorithm exhausted the divergence problem. It also makes explicit a deeper requirement: in some recovery histories, deciding where two logs diverged requires comparing more of the retained epoch lineage rather than merely one current epoch lookup.

Later source:

- Apache Kafka, KIP-279, `Fix log divergence between leader and follower after fast leader fail over`: <https://cwiki.apache.org/confluence/display/KAFKA/KIP-279%3A%2BFix%2Blog%2Bdivergence%2Bbetween%2Bleader%2Band%2Bfollower%2Bafter%2Bfast%2Bleader%2Bfail%2Bover>.

---

## Engineering reconstruction

The following are project-level reconstructions, not Apache's historical vocabulary.

### E — committed-prefix evidence and lineage evidence are different retained relations

The high watermark answers a question like:

> How far has the currently qualified replicated prefix advanced?

The epoch history answers a different recovery question:

> Which leadership lineage produced the surviving suffix, and where does that lineage cease to match the current leader?

Therefore:

```text
committed-prefix frontier != lineage map
```

A single scalar prefix boundary is not sufficient to reconstruct every safe truncation decision after leadership changes.

### E — a recovery boundary can be stronger when it preserves causal/protocol provenance, not merely position

An offset alone identifies a place in a log. `(leader epoch, start offset)` adds information about **under which leadership period that region entered the log**.

This does not turn Kafka into a provenance database. The relation is narrow and protocol-specific. But for recovery it can distinguish two byte sequences whose numerical offsets overlap while their leadership histories differ.

### E — retained control metadata can prevent destructive recovery

The 0.8.2 case already showed that retained control state can authorize truncation. KIP-101 supplies the converse: better-retained lineage state can prevent an otherwise-valid recovery procedure from truncating a suffix too aggressively.

Thus:

```text
recovery action != inherently retention-preserving
```

A recovery rule can itself destroy retained state if the evidence used to choose its boundary is too weak or stale for the transition being performed.

### E — “no truncation needed” does not mean “everything above HW is committed”

If a leader-epoch lookup says the follower does not need to truncate, that conclusion only says the follower's surviving suffix is not rejected by this lineage check. Ordinary consumer visibility and replication commitment remain governed by the high-watermark relation.

So:

```text
lineage-admissible suffix != committed-visible suffix
```

### E — checkpointed lineage is a compressed relation, not complete history

`leader-epoch-checkpoint` does not retain every produce request, fetch acknowledgement, election event, controller transition, or physical write. It retains enough epoch/start-offset structure to answer the bounded lookup.

Therefore:

```text
retained recovery relation != retained event history
```

### E — compatibility fallback changes the evidence available to the recovery decision

Under an older inter-broker protocol, the same 0.11 binaries can fall back to high-watermark truncation. The storage payload may be identical, yet the **available retained/control relation** used to adjudicate recovery is weaker.

This makes protocol-version state part of the practical retention regime without making the protocol version itself the retained payload.

### E — integrity of retention metadata is itself a retention problem

KIP-101 discusses the epoch file getting ahead of an asynchronously flushed log after unclean shutdown and requiring entries beyond the recovered LEO to be removed. The 0.11 implementation also prunes epoch state when the log is truncated or earlier history is discarded.

The epoch relation must therefore remain coherent with the payload history it qualifies. A stale or impossible lineage record is not merely “extra metadata”; it can misdescribe which history survives.

---

## Functional analogies — bounded

### A — Case 58 Raft snapshot continuation metadata

Raft snapshot `last included index` / `term` and Kafka leader-epoch history both show that a retained payload/state representation may need compact boundary or lineage metadata to support later continuation. They are not the same protocol: Raft's term/index participates in a consensus log and snapshot/install rules; Kafka 0.11's epoch file is a replica-local history used in follower divergence/truncation.

### A — Case 49 HDFS generation stamp and lease recovery

HDFS generation/recovery stamps and Kafka leader epochs both demonstrate that surviving bytes can require version/authority evidence before they are accepted as the current continuation. This is a functional analogy only. Their writer authority, data layout, quorum rules, and recovery operations are different.

### A — Case 05 RADOS peering/currentness

Both systems reject the idea that the physically fullest surviving copy automatically determines the future. RADOS uses PG/version/peering evidence; Kafka uses partition leadership, ISR/progress, high watermark, and—by 0.11—retained epoch lineage. No common implementation genealogy is inferred.

### A — within Kafka, Case 56's 0.8.2 and 0.11 slices should remain layered

The 0.11 slice does not invalidate the 0.8.2 high-watermark case. It sharpens it:

- high watermark remains essential for committed-prefix/visibility semantics;
- leader-epoch lineage becomes a separate truncation/recovery relation;
- later KIP-279 further strengthens the lineage comparison.

This is an example of one system family splitting one overloaded recovery signal into more specialized retained state.

---

## Philosophical interpretation — bounded

The technical fact that motivates interpretation is precise: a future broker can possess the payload bytes and their numeric offsets yet still need retained information about **which leadership history produced them** before it can decide what counts as the continuing log.

A narrow project interpretation is therefore:

> **Persistence can depend on retention of a relation of admissible continuity, not only on survival of the states to be continued.**

The leader-epoch checkpoint is not “memory of the past” in a broad cultural sense. It is a compact operational trace that makes one future act—truncate here, or do not truncate—better informed.

The boundary is equally important: this does not imply that every technical system needs historical provenance, that Kafka retains complete causal history, or that protocol lineage is philosophically identical to personal or archival memory.

---

## Explicit non-claims

This evidence does **not** establish that:

1. Kafka invented epochs, terms, primary/backup lineage, or replicated-log recovery.
2. KIP-101 introduced every use of `LeaderEpoch` in Kafka; the KIP itself says a leader-epoch concept already existed and changes how it is propagated/retained/used.
3. `leader-epoch-checkpoint` is the same object as `replication-offset-checkpoint`.
4. leader epoch is the same as producer epoch, transactional producer epoch, controller epoch, or a Raft term.
5. a suffix accepted by the epoch truncation check is necessarily committed or `READ_COMMITTED` visible.
6. high watermark became obsolete in Kafka 0.11.
7. KIP-101 protects against all divergence with unclean leader election enabled; it explicitly says it does not.
8. KIP-101 was the final leader-epoch recovery design; KIP-279 is direct counterevidence.
9. the text-file checkpoint preserves a complete leadership history forever; pruning, deletion/compaction interactions, rebuild, and later protocol changes matter.
10. `FileDescriptor.sync()` plus an atomic-move attempt proves universal power-fail atomicity on every filesystem/storage stack.
11. Apache's acceptance tests exhaustively prove all crash interleavings.
12. the KIP proposal name `leader-epoch-sequence-file` and the shipping 0.11 implementation name `leader-epoch-checkpoint` are interchangeable historical labels without qualification.
13. mixed-version clusters automatically receive the same recovery guarantee as a cluster running the leader-epoch inter-broker protocol.
14. similarity to Raft/HDFS/RADOS proves genealogy or borrowing.

---

## Claim ledger

| Claim | Type | Status |
| --- | --- | --- |
| Kafka 0.11.0.0 was released 28 June 2017 | historical record | established |
| KIP-101 identifies follower-HW truncation as able to destroy a message in a fast recovery/election sequence | historical record | established |
| KIP-101 retains `(LeaderEpoch => StartOffset)` history per replica | historical record | established |
| exact 0.11 implementation persists that relation in `leader-epoch-checkpoint` | historical record | established in source |
| exact 0.11 follower asks the leader about its latest local epoch before normal epoch-driven truncation | historical record | established in source |
| leader epoch is a truncation-lineage relation, not a replacement for high-watermark commitment | historical/engineering | established |
| follower suffix can survive despite being above follower's recorded HW when lineage check does not require truncation | historical/engineering | supported by KIP-101 scenario and implementation |
| divergent suffix can be truncated at leader-returned epoch end | historical record | established |
| mixed-version fallback can retain high-watermark truncation | historical record | established |
| retained lineage can prevent destructive recovery based on weaker stale boundary evidence | engineering reconstruction | supported |
| checkpointed lineage is complete event history | rejected | explicit non-claim |
| KIP-101 solved all divergence | rejected | contradicted by KIP-101 boundary and KIP-279 |
| leader-epoch similarity to Raft/HDFS proves common genealogy | rejected | functional analogy only |

---

## Source list

### Primary Apache design / release records

1. Apache Kafka, **KIP-101 — Alter Replication Protocol to use Leader Epoch rather than High Watermark for Truncation**: <https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=177052956>.
2. Apache Kafka, **Downloads**, Kafka 0.11.0.0 released 28 June 2017: <https://kafka.apache.org/community/downloads/>.
3. Apache Kafka, **0.11.0.0 release notes**: <https://archive.apache.org/dist/kafka/0.11.0.0/RELEASE_NOTES.html>.

### Exact 0.11.0.0 implementation

4. `ReplicaFetcherThread.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/ReplicaFetcherThread.scala>.
5. `LeaderEpochFileCache.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/epoch/LeaderEpochFileCache.scala>.
6. `LeaderEpochCheckpointFile.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/checkpoints/LeaderEpochCheckpointFile.scala>.
7. `CheckpointFile.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/main/scala/kafka/server/checkpoints/CheckpointFile.scala>.
8. `EpochDrivenReplicationProtocolAcceptanceTest.scala`: <https://github.com/apache/kafka/blob/0.11.0.0/core/src/test/scala/unit/kafka/server/epoch/EpochDrivenReplicationProtocolAcceptanceTest.scala>.

### Later qualification / counterevidence

9. Apache Kafka, **KIP-279 — Fix log divergence between leader and follower after fast leader fail over**: <https://cwiki.apache.org/confluence/display/KAFKA/KIP-279%3A%2BFix%2Blog%2Bdivergence%2Bbetween%2Bleader%2Band%2Bfollower%2Bafter%2Bfast%2Bleader%2Bfail%2Bover>.

---

## Related-repository check

A fresh repository search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Kafka` returned no dedicated Kafka replication / leader-epoch history. This slice therefore keeps only the retention-specific recovery relation here rather than creating a generic Kafka architecture history. If the companion repository later grows that history, this evidence should link to it and trim duplicated mechanism chronology.

---

## Remaining evidence debt

This bounded 0.11 slice is complete, but the following are deliberately left open:

- KIP-279's shipping implementation/release chronology and exact multi-round largest-common-epoch behavior;
- later leader-epoch checkpoint evolution, including modern corruption/rebuild handling;
- KRaft metadata epochs versus partition leader epochs;
- independent crash/failover fault injection against named Kafka releases;
- exact storage-stack durability beneath epoch-checkpoint and log-file updates;
- mixed-version upgrade tests that directly compare the high-watermark fallback and epoch-driven path;
- compaction/deletion cases in which epoch lineage must be retained or rebuilt after old payload ranges disappear.

None of these blocks the narrow conclusion of this evidence file.