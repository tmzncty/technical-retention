# Case 51 grounding — HDFS DataNode command fencing, heartbeat authority, and post-failover inventory freshness

## Promotion target

Ground [`cases/51-apache-hdfs-datanode-command-fencing.md`](../cases/51-apache-hdfs-datanode-command-fencing.md) as a bounded distributed-retention case without collapsing HDFS QJM writer fencing, block generation stamps, DataNode command authority, and replica-inventory freshness into one generic “epoch” mechanism.

**Result:** `grounded`.

The central relation is directly supported by Apache primary sources:

> in HDFS HA, a DataNode can keep connections to multiple NameNodes while retaining a runtime view of which actor currently has block-command authority; heartbeat HA state plus transaction-ID recency update that view before same-response commands are interpreted, while post-failover stale-inventory state separately postpones some irreversible block invalidations until fresh reports arrive.

---

## Bounded evidence set

### A. Apache HDFS-1972 — DataNode fencing problem and failover inventory safety

- **Issue:** `HA: Datanode fencing mechanism`.
- **Created:** 20 May 2011.
- **Resolved:** 21 December 2011.
- **Direct problem statement:** active and standby NameNodes can both send commands to a DataNode; the DataNode must honor commands only from Active and reject Standby commands to prevent corruption, including during failover and split brain.
- **Final patch:** December 2011 `hdfs-1972.txt`.
- **Direct patch evidence:** after failover, apparently over-replicated blocks may not be processed until replicas have block-reported to the new Active, because old pending deletions may not yet be reflected in its inventory.
- **Direct patch evidence:** invalidation is postponed when replicas are on stale nodes; blocks are rescanned after fresh reports.
- **Direct patch evidence:** failover cleanup clears queued replication/invalidation/recovery decisions that were made under a prior control state.
- **Use here:** grounds both the historical command-fencing problem and the distinct post-failover inventory-freshness problem.
- **Issue URL:** <https://issues.apache.org/jira/browse/HDFS-1972>
- **Patch URL:** <https://issues.apache.org/jira/secure/attachment/12508141/hdfs-1972.txt>

### B. Apache HDFS-2627 — higher-transaction-ID Active claim

- **Issue:** `HA: determine DN's view of which NN is active based on heartbeat responses`.
- **Created:** 3 December 2011.
- **Resolved:** 8 December 2011.
- **Direct design evidence:** on startup the DataNode should initially treat neither NameNode as Active.
- **Direct design evidence:** NameNodes include HA state in heartbeat responses.
- **Direct design evidence:** the DataNode believes the NameNode claiming Active at the higher transaction ID.
- **Use here:** anchors the historical selection rule without importing later consensus terminology.
- **URL:** <https://issues.apache.org/jira/browse/HDFS-2627>

### C. Hadoop 2.7.3 `FSNamesystem.java` — heartbeat role + transaction progress

- **Version:** `rel/release-2.7.3`.
- **Direct source evidence:** `handleHeartbeat()` creates `NNHAStatusHeartbeat` from the current HA service state plus `getFSImage().getLastAppliedOrWrittenTxId()`.
- **Use here:** establishes what the DataNode is actually told by the NameNode in the bounded release.
- **URL:** <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java>

### D. Hadoop 2.7.3 `BPOfferService.java` — retained Active actor and transaction-ID watermark

- **Version:** `rel/release-2.7.3`.
- **Direct source evidence:** one `BPOfferService` manages one `BPServiceActor` per NameNode and retains `bpServiceToActive`.
- **Direct source evidence:** source comment says `lastActiveClaimTxId` records the most recent transaction ID from an accepted Active claim to detect split-brain where an earlier NameNode still asserts Active with too-low txid.
- **Direct source evidence:** `lastActiveClaimTxId` is an ordinary in-memory `long` initialized to `-1`; this source does not make it a crash-persistent promise.
- **Direct source evidence:** `updateActorStatesFromHeartbeat()` accepts a competing Active only when its txid is more recent than the retained watermark.
- **Direct source evidence:** `processCommandFromActor()` dispatches by whether the command's actor is the selected `bpServiceToActive`.
- **Direct source evidence:** Active handles transfer/invalidate/cache/finalize/recover/bandwidth/access-key commands; Standby ignores the destructive/replicative/recovery classes but still accepts `DNA_ACCESSKEYUPDATE`.
- **Use here:** grounds both command-source admissibility and the command-class-specific boundary.
- **URL:** <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/BPOfferService.java>

### E. Hadoop 2.7.3 `BPServiceActor.java` — update authority before processing same-heartbeat commands

- **Version:** `rel/release-2.7.3`.
- **Direct source evidence:** after heartbeat response, `offerService()` first calls `bpos.updateActorStatesFromHeartbeat(...)`.
- **Direct source evidence:** the source comment says this ordering is important because the first heartbeat from a new Active may contain commands that should be processed.
- **Direct source evidence:** command processing follows the authority-state update.
- **Use here:** grounds the ordering relation `fresh authority interpretation -> command interpretation`.
- **URL:** <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/BPServiceActor.java>

### F. Hadoop 2.7.3 `DatanodeStorageInfo.java` — post-failover stale inventory

- **Version:** `rel/release-2.7.3`.
- **Direct source evidence:** source comment says startup/failover may leave pending block deletions from a previous NameNode incarnation, so block contents are considered stale until a block report is received.
- **Direct source evidence:** if any block has a stale replica, invalidations for that block are withheld.
- **Direct source evidence:** `markStaleAfterFailover()` resets heartbeat freshness and sets `blockContentsStale=true`.
- **Direct source evidence:** a heartbeat sets `heartbeatedSinceFailover=true`; a later block report can clear `blockContentsStale`.
- **Use here:** grounds inventory freshness as a different retained control relation from command-source authority.
- **URL:** <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DatanodeStorageInfo.java>

### G. Hadoop 2.7.3 HA/QJM guide — neighboring fencing boundary

- **Direct system evidence:** HDFS HA uses Active/Standby NameNodes; QJM and external/process fencing solve neighboring but different authority/liveness surfaces.
- **Use here:** prevents DataNode command fencing from being presented as the only HDFS fencing layer.
- **URL:** <https://hadoop.apache.org/docs/r2.7.3/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithQJM.html>

---

## Source cross-check

The 2011 design and 2.7.3 release source agree on the command-authority chain:

```text
NameNode heartbeat
        |
        +---- HA state
        +---- namespace txid
        |
        v
DataNode Active-claim comparison
        |
        +---- older competing ACTIVE -> reject takeover
        +---- newer ACTIVE -> select actor / advance watermark
        |
        v
same-response commands interpreted
        |
        +---- selected Active -> process documented command classes
        +---- Standby -> ignore destructive/replicative/recovery classes
```

The same historical fencing work also establishes a separate inventory chain:

```text
failover
  -> mark block inventory stale
  -> post-failover heartbeat
  -> block report
  -> stale state may clear
  -> postponed invalidation can be reconsidered
```

The second chain is not evidence that the first failed. It answers a different question: whether the newly authoritative NameNode knows enough about replica reality to make a destructive decision.

---

## Claim ledger

| Claim | Label | Evidence | Strength / boundary |
| --- | --- | --- | --- |
| HDFS identified simultaneous Active/Standby DataNode commands as a corruption risk | `H/P` | HDFS-1972 | strong direct historical statement |
| DataNode should prefer the higher-txid Active claim | `H/P` | HDFS-2627 | strong direct design statement |
| 2.7.3 heartbeat exports HA service state and last applied/written txid | `H/P` | `FSNamesystem.java` | strong release-source evidence |
| DataNode retains one selected Active actor plus `lastActiveClaimTxId` | `H/P` | `BPOfferService.java` | strong |
| lower competing Active claim is not allowed to replace the more recent one | `H/P` | `updateActorStatesFromHeartbeat()` | strong |
| authority state is updated before commands from the same heartbeat | `H/P` | `BPServiceActor.offerService()` | strong ordering evidence |
| block-transfer/invalidation/recovery command classes are ignored from Standby | `H/P` | `processCommandFromStandby()` | strong, command-list bounded |
| some control work remains allowed from Standby (`DNA_ACCESSKEYUPDATE`) | `H/P` | same source | strong negative boundary |
| post-failover replica inventory is retained as stale until fresh observation | `H/P` | HDFS-1972 patch; `DatanodeStorageInfo.java` | strong |
| stale inventory can postpone invalidation | `H/P` | HDFS-1972 patch and release-source comment | strong |
| command authority and inventory freshness are distinct second-order state | `E` | combined mechanism | strong project reconstruction |
| `lastActiveClaimTxId` is a durable JournalNode-like fencing promise | `X` | plain in-memory field initialized `-1` | rejected |
| all Standby messages are ignored | `X` | access-key update exception | rejected |
| stale inventory means payload corruption | `X` | source defines stale report/deletion knowledge | rejected |
| one fencing mechanism covers edit log, DataNode commands, process liveness, and stale reads | `X` | Cases 50–51 + HA guide | rejected |

---

## Counterexample value

### `reachable controller = authoritative controller`

Rejected. A lower-txid NameNode may remain reachable and continue claiming Active while the DataNode retains a newer Active claim and declines to transfer command authority back.

### `new Active = all destructive decisions immediately safe`

Rejected. The new Active can still have stale replica inventory after failover and postpone invalidation until fresh reports arrive.

### `fencing state must be durable to matter`

Rejected as a universal statement. QJM Case 50 does require a durable JournalNode promise for its crash model; DataNode Case 51 uses runtime remembered authority state and re-observation. The right durability boundary depends on which component can restart and which surrounding protocol layers exist.

### `Standby = no useful control relation`

Rejected. Standby communication remains active and at least access-key update is accepted, while block mutation classes are filtered.

### `stale = corrupt`

Rejected. `blockContentsStale` expresses uncertainty about whether the central inventory has incorporated prior deletion effects, not a checksum failure of the local block bytes.

---

## Cross-case controls

### Case 50 / HDFS QJM epoch fencing

Functional bridge: both qualify an old still-running NameNode as no longer authoritative.

Boundary:

```text
JournalNode lastPromisedEpoch
    = persistent acceptor-side write-fencing promise

DataNode lastActiveClaimTxId
    = runtime observed Active-claim watermark
```

Do not merge them into a generic “HDFS term.”

### Case 49 / generation-stamp lease recovery

Generation stamps qualify block/recovery generations. Case 51 transaction IDs qualify which NameNode claim the DataNode treats as current for command dispatch.

`block generation stamp != namespace transaction ID`.

### Case 46 / GFS master recovery

Both show that fresh observation of participants can be a retention mechanism when central knowledge may be stale.

Boundary: GFS re-derives chunk locations after master restart; HDFS withholds some destructive decisions after failover until post-failover heartbeat/block-report evidence refreshes replica inventory.

### Cases 28 / 41 / negative state

Tombstones retain evidence that an older data value must not become current again. HDFS `blockContentsStale` instead retains **uncertainty** that blocks a deletion decision. Both can inhibit forgetting, but for different reasons.

---

## `computing-archaeology` reuse check

Searched `tmzncty/computing-archaeology` for HDFS, DataNode fencing, heartbeat transaction IDs, Active/Standby command filtering, and post-failover stale block inventory. No dedicated case was found.

Therefore this slice does not duplicate an existing companion-repository mechanism history. A future broad HDFS HA chronology should live there and be linked here.

---

## Maturity decision

**Promote to `grounded`.**

Why:

- Apache's 2011 issues state both the DataNode fencing problem and the higher-transaction-ID heartbeat selection rule directly;
- the final HDFS-1972 patch exposes the reason for stale post-failover replica inventory and postponed invalidation;
- Hadoop 2.7.3 release source independently implements the Active watermark, same-heartbeat ordering, command-class filtering, and storage freshness state;
- the crash-persistence boundary is explicit rather than assumed;
- QJM epoch fencing, generation stamps, external process fencing, and inventory freshness remain separated;
- companion-repository duplication was checked.

Remaining work is deliberately separate: post-2.7 DataNode fencing evolution, restart/split-brain fault injection, modern HDFS erasure-coded command behavior, Observer/read-freshness semantics, and broader fencing genealogy.
