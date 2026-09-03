# Apache HDFS DataNode Command Fencing: Heartbeat Authority, Transaction-ID Recency, and Stale Replica Inventories

## Scope

- **Bounded system:** Apache HDFS high-availability DataNode/NameNode interaction, from the 2011 HA-branch fencing work in HDFS-1972/HDFS-2627 through the released Hadoop **2.7.3** implementation.
- **Bounded mechanism:** DataNodes maintaining connections to both HA NameNodes; HA state and namespace transaction ID carried in heartbeat responses; DataNode-side `bpServiceToActive` / `lastActiveClaimTxId`; command dispatch that accepts destructive/replicative/recovery commands only from the selected Active; and the distinct post-failover `blockContentsStale` inventory state that delays some invalidations until fresh heartbeat/block-report evidence arrives.
- **Primary source base:** HDFS-1972 and its December 2011 patch; HDFS-2627; Hadoop 2.7.3 `FSNamesystem.java`, `BPServiceActor.java`, `BPOfferService.java`, and `DatanodeStorageInfo.java`.
- **Research question:** when both old and new NameNodes may remain reachable during failover, what retained control state lets a DataNode decide whose block-management commands count, and why is that authority decision still insufficient to make every post-failover deletion safe?

This is **not** a general HDFS HA history. Case 49 covers block generation stamps and lease recovery. Case 50 covers QJM edit-log writer epochs and JournalNode promises. This case isolates **DataNode command-source admissibility and post-failover replica-inventory freshness**.

The bounded retention claim is:

> **An HDFS DataNode can remain connected to more than one NameNode while retaining a runtime distinction about which NameNode currently has block-command authority. In the bounded 2.7.3 implementation, heartbeat responses carry HA state and namespace transaction ID; the DataNode remembers the highest accepted Active claim, applies that claim before processing commands from the same heartbeat, and ignores destructive/replicative/recovery command classes from non-selected Standby actors. Separately, after NameNode failover, block inventories can remain marked stale until fresh heartbeat and block-report evidence arrives, so a newly authoritative NameNode can still postpone irreversible invalidation. Command authority and inventory freshness are therefore distinct non-payload retention relations.**

`command-source admissibility`, `authority watermark`, and `inventory freshness` below are project terms. Historical Apache vocabulary includes `ACTIVE`, `STANDBY`, `transaction ID`, `heartbeat`, `bpServiceToActive`, `lastActiveClaimTxId`, `split-brain`, `blockContentsStale`, `heartbeatedSinceFailover`, `block report`, `invalidation`, and `postponedMisreplicatedBlocks`.

---

## Historical vocabulary and prior-art boundary

### Direct Apache vocabulary

HDFS-1972 is itself titled **“HA: Datanode fencing mechanism.”** Its description states the problem in concrete actor terms: an active and standby NameNode may both send commands to a DataNode; the DataNode must honor commands only from the active NameNode and reject standby commands during failover and split-brain conditions.

HDFS-2627 then narrows one part of the design: on startup DataNodes should initially treat neither NameNode as active; heartbeat responses should carry each NameNode's HA state; and the DataNode should believe the NameNode that claims Active with the **higher transaction ID**.

The later 2.7.3 source preserves vocabulary such as:

- `BPServiceActor`;
- `bpServiceToActive`;
- `lastActiveClaimTxId`;
- `NNHAStatusHeartbeat`;
- `HAServiceState.ACTIVE`;
- `HAServiceState.STANDBY`;
- `blockContentsStale`;
- `heartbeatedSinceFailover`;
- `DNA_TRANSFER`;
- `DNA_INVALIDATE`;
- `DNA_RECOVERBLOCK`.

### Prior-art boundary

This case does **not** claim that HDFS invented:

- active/standby failover;
- fencing;
- split-brain detection;
- monotonically ordered transaction identifiers;
- heartbeat-based role observation;
- refusing stale control-plane commands.

The historically defensible claim is narrower: the 2011 HDFS HA work explicitly designed a DataNode-side fencing relation around heartbeat-advertised HA state plus transaction-ID recency, and the released 2.7.3 code implements that relation alongside a separate post-failover replica-inventory freshness gate.

Do not normalize the transaction ID into a generic consensus `term`, Paxos ballot, QJM epoch, or HDFS block generation stamp. The source gives it a different role.

---

## Historical record

### H/P — Apache framed dual NameNode command sources as a corruption risk

HDFS-1972, created in May 2011 and resolved in December 2011, states that an HA configuration can have active and standby NameNodes both sending commands to the DataNode. It requires the DataNode to honor commands only from the active NameNode and reject standby commands, including during failover and split-brain states.

That wording matters. The problem is not merely “which server is reachable?” Both can be reachable. The problem is which reachable control source is **admissible for state-changing DataNode work**.

**Primary anchor:** <https://issues.apache.org/jira/browse/HDFS-1972>

### H/P — HDFS-2627 selected the Active claim by heartbeat HA state plus transaction-ID recency

HDFS-2627, created and resolved in December 2011, says DataNodes should not assume either NameNode is Active at startup. Instead, NameNodes include HA state in heartbeat responses and the DataNode “will believe whichever NN claims to be active at a higher transaction ID.”

This is direct historical evidence for a retained recency relation at the DataNode rather than a static configuration label.

**Primary anchor:** <https://issues.apache.org/jira/browse/HDFS-2627>

### H/P — the NameNode heartbeat exports both role and namespace progress

In Hadoop 2.7.3 `FSNamesystem.handleHeartbeat()`, the NameNode creates an `NNHAStatusHeartbeat` containing:

- `haContext.getState().getServiceState()`;
- `getFSImage().getLastAppliedOrWrittenTxId()`.

Thus the DataNode does not derive Active authority solely from TCP connection identity or a configured endpoint. The heartbeat carries both **role assertion** and **transaction-history position**.

**Primary source:** <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java>

### H/P — the DataNode remembers the most recent accepted Active claim

Hadoop 2.7.3 `BPOfferService` has one actor per NameNode for the block pool and retains:

- `bpServiceToActive`, the actor the DataNode currently treats as Active;
- `lastActiveClaimTxId`, initialized to `-1`.

The source comment on `lastActiveClaimTxId` is unusually explicit: each time a NameNode claims Active, the DataNode records its most recent transaction ID, and this lets it detect a split-brain case where an earlier NameNode still asserts Active with a transaction ID lower than an already observed claim.

`updateActorStatesFromHeartbeat()` then implements the rule:

```text
heartbeat says ACTIVE
        |
        v
compare heartbeat txid with lastActiveClaimTxId
        |
        +---- lower / not more recent -> reject the competing Active claim
        |
        +---- higher -> select that BPServiceActor as Active
```

If the selected actor later reports non-Active state, the DataNode can clear the selected Active reference.

**Primary source:** <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/BPOfferService.java>

### H/P — authority state is updated before commands from the same heartbeat are interpreted

`BPServiceActor.offerService()` receives a heartbeat response, then calls:

```text
bpos.updateActorStatesFromHeartbeat(...)
```

**before** processing the response's DataNode commands.

The source comment explains why: the first heartbeat from a newly Active NameNode may already contain commands that should be processed. The order therefore prevents the command list from being interpreted against the previous heartbeat's authority view.

This supports:

```text
heartbeat reception
    != command admissibility

current role/txid interpretation
    -> command admissibility for that response
```

**Primary source:** <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/BPServiceActor.java>

### H/P — state-changing block commands are routed through the selected Active actor

`BPOfferService.processCommandFromActor()` checks whether the actor that supplied the command is `bpServiceToActive`.

For the selected Active, the bounded 2.7.3 source handles command classes including:

- `DNA_TRANSFER`;
- `DNA_INVALIDATE`;
- `DNA_CACHE` / `DNA_UNCACHE`;
- `DNA_FINALIZE`;
- `DNA_RECOVERBLOCK`;
- `DNA_BALANCERBANDWIDTHUPDATE`;
- `DNA_ACCESSKEYUPDATE`.

The `DNA_INVALIDATE` branch explicitly treats blocks as obsolete and calls the local dataset invalidation path; `DNA_TRANSFER` creates another block copy; `DNA_RECOVERBLOCK` invokes block recovery.

For a Standby actor, however, the source explicitly ignores `DNA_TRANSFER`, `DNA_INVALIDATE`, `DNA_RECOVERBLOCK`, `DNA_FINALIZE`, cache/un-cache, shutdown, and bandwidth-update command classes.

Therefore:

```text
NameNode can communicate with DataNode
    != NameNode may issue every DataNode mutation command
```

**Primary source:** <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/BPOfferService.java>

### H/P — command authority is not one all-or-nothing binary

The same Standby path still accepts `DNA_ACCESSKEYUPDATE`.

This is important negative evidence. The implementation does **not** define Standby as “all messages ignored.” It distinguishes command classes.

So:

```text
standby
    != disconnected
    != universally ignored
```

and:

```text
block-mutation authority
    != every control-plane authority
```

This prevents an overly simple claim that one Boolean role bit governs every possible interaction.

### H/P — failover separately makes replica inventory epistemically stale

HDFS-1972's final December 2011 patch added another part of the fencing design for over-replicated blocks. It explains that after failover the new Active may not yet know about block deletions that were pending under the previous NameNode. The patch therefore marks block contents stale and postpones some over-replication processing until fresh block reports arrive.

Hadoop 2.7.3 `DatanodeStorageInfo` preserves this relation at storage granularity. Its source comment says that at startup or failover there may be pending block deletions from a prior NameNode incarnation. Until a block report arrives, storage block contents are considered stale; if a block has a stale replica, invalidations for that block are withheld.

`markStaleAfterFailover()` sets:

```text
heartbeatedSinceFailover = false
blockContentsStale = true
```

A later heartbeat marks the storage as heartbeated. A block report clears `blockContentsStale` only after that heartbeat condition has been satisfied.

**Primary sources:**

- <https://issues.apache.org/jira/secure/attachment/12508141/hdfs-1972.txt>
- <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DatanodeStorageInfo.java>

### H/P — stale inventory postpones irreversible deletion rather than declaring payload corrupt

The HDFS-1972 patch adds `postponedMisreplicatedBlocks`. Its comments explain the reason: an apparently over-replicated block may include a replica that the previous NameNode had already told a DataNode to delete. Acting immediately on the new Active's stale map could therefore delete one more copy under a false count.

The patch explicitly postpones invalidation when replicas reside on nodes with potentially out-of-date block reports, and revisits those blocks after fresh reports arrive.

This is not a checksum or byte-corruption diagnosis. It is a **knowledge/currentness qualification on the NameNode's replica inventory**.

### H/P — prior queued maintenance decisions are not blindly carried through role transition

The same HDFS-1972 patch added queue clearing during failover, with a comment describing the target as queues that hold decisions previously made by the NameNode. Replication, invalidation, recovery, and related queued work were part of the fencing review.

This supports a bounded historical observation:

```text
a previously computed maintenance decision
    != automatically admissible after authority transition
```

The exact later queue structures evolved; this case uses the 2011 patch for the historical design point rather than projecting every patch field unchanged into all later HDFS versions.

---

## Retained state

The bounded mechanism contains several distinct state classes.

### 1. DataNode-selected Active actor

`bpServiceToActive` identifies which `BPServiceActor` currently supplies Active-authorized commands for the block pool.

### 2. DataNode `lastActiveClaimTxId`

An in-memory monotonic watermark of the most recent Active claim accepted by the DataNode.

This is **not** user payload and **not** a JournalNode `lastPromisedEpoch`.

### 3. Heartbeat-advertised HA state and transaction ID

Each heartbeat supplies the observation used to update the DataNode's local authority view.

### 4. Post-failover storage freshness state

`heartbeatedSinceFailover` and `blockContentsStale` qualify whether the new Active's block inventory is fresh enough for certain destructive decisions.

### 5. Block reports

Reports do not merely enumerate bytes. In this failover path they provide re-observation evidence that can retire the stale-inventory condition.

### 6. Queued maintenance decisions

Replication/invalidation/recovery work may embody conclusions drawn under an earlier control state. The 2011 fencing patch treats some such decisions as unsafe to carry blindly across failover.

These are all **second-order operational states** about payload and authority rather than application file contents themselves.

---

## Retention mechanism

The bounded command-source sequence is:

```text
DataNode keeps BPServiceActor for each NameNode
        |
        v
heartbeat response arrives from one actor
        |
        +---- HA service state
        +---- last applied/written namespace txid
        |
        v
DataNode compares ACTIVE claim with lastActiveClaimTxId
        |
        +---- older competing claim -> do not replace selected Active
        +---- newer claim -> select actor; advance watermark
        |
        v
process commands from that same heartbeat
        |
        +---- selected Active -> permit documented command classes
        +---- Standby/non-selected -> ignore destructive/replicative/recovery classes
```

The bounded post-failover inventory sequence is different:

```text
NameNode authority transition
        |
        v
storage inventory marked stale
        |
        v
post-failover heartbeat observed
        |
        v
fresh block report observed
        |
        v
storage inventory may become non-stale
        |
        v
previously postponed over-replication / invalidation decisions may be reconsidered
```

These sequences solve different questions:

```text
Who may command a mutation?
    !=
Do we know enough about replica state to perform this mutation safely?
```

---

## Read / write / erase semantics

### Read / observation

The DataNode maintains heartbeat sessions with multiple NameNodes. Observation of a Standby remains useful; connection itself does not grant block-mutation authority.

A block report is also an observation operation with retention consequences: it can retire uncertainty represented by `blockContentsStale`.

### Write / mutation

`DNA_TRANSFER`, `DNA_RECOVERBLOCK`, cache state changes, and similar commands cause or coordinate state change. Their admissibility depends on which actor the DataNode currently treats as Active.

### Erase / invalidation

`DNA_INVALIDATE` is especially revealing because the DataNode may physically remove a local block replica. The implementation therefore composes two gates:

1. command source must be authorized as Active at the DataNode;
2. the NameNode's replica inventory must be fresh enough for the deletion decision in the failover/over-replication path.

The first gate is **authority currentness**. The second is **inventory currentness**.

Neither should be confused with secure media erasure.

---

## Maintenance and labor

Making one HDFS namespace survive failover requires more than storing file bytes:

- each DataNode maintains actor connections to the HA NameNodes;
- NameNodes generate heartbeat responses carrying HA role and transaction progress;
- DataNodes compare competing Active claims;
- command dispatch differentiates Active and Standby sources;
- failover marks storage inventory stale;
- DataNodes send heartbeats and block reports so the new Active can rebuild confidence in current replica inventory;
- postponed mis-replication work is later reconsidered;
- broader QJM/ZKFC/process fencing remains separate infrastructure outside this bounded mechanism.

Automation relocates the labor into continuous protocol observation and bookkeeping; it does not remove the need to maintain authority and freshness relations.

---

## Failure and forgetting

### Failure mode 1 — old Active remains reachable and still claims Active

A lower-transaction-ID claim does not replace a more recent Active claim already accepted by the DataNode.

Physical liveness therefore does not automatically restore command authority.

### Failure mode 2 — DataNode sees the new Active but still has stale replica knowledge

Authority can transition before every storage has produced fresh post-failover inventory evidence. Destructive invalidation may still need to wait.

### Failure mode 3 — stale inventory makes an over-replicated block look safer to delete than it is

A replica in the NameNode map may already have been deleted under a previous command. HDFS postpones the irreversible action until the stale condition is cleared.

### Failure mode 4 — DataNode restarts

`lastActiveClaimTxId` is an ordinary in-memory field initialized to `-1` in the bounded release source. This case therefore does **not** claim that DataNode command fencing is a crash-persistent promise comparable to QJM's `lastPromisedEpoch`.

After a DataNode restart, the authority view must be re-established through current protocol interaction. The larger HA system supplies additional fencing layers.

### Failure mode 5 — Standby sends a command class that is not block-destructive

The source permits `DNA_ACCESSKEYUPDATE` from Standby, so “ignore Standby” cannot be generalized into one universal command prohibition.

### What is *not* established

This case does not claim:

- transaction ID is a synonym for QJM epoch, Raft term, Paxos ballot, or block generation stamp;
- `lastActiveClaimTxId` is persisted across DataNode restart;
- the DataNode mechanism alone solves every HDFS split-brain path;
- QJM writer fencing makes DataNode command fencing redundant;
- external process fencing becomes unnecessary;
- every command from Standby is ignored;
- `blockContentsStale` means the underlying block bytes are corrupt;
- a stale replica inventory proves a replica exists or does not exist;
- postponed invalidation is secure deletion;
- the 2011 patch structure is identical in every later Hadoop release.

---

## Historical record vs engineering reconstruction

### Historical record

Apache primary sources establish:

- HDFS explicitly identified simultaneous Active/Standby commands to DataNodes as a corruption risk;
- HDFS-2627 chose heartbeat HA state plus higher transaction ID as the DataNode Active-selection rule;
- Hadoop 2.7.3 NameNode heartbeat responses carry service state plus last applied/written transaction ID;
- Hadoop 2.7.3 DataNodes retain an Active actor reference and `lastActiveClaimTxId`;
- competing lower-txid Active claims are rejected at the DataNode;
- heartbeat role state is updated before commands from the same response are processed;
- destructive/replicative/recovery command classes are ignored from Standby actors;
- `DNA_ACCESSKEYUPDATE` is an explicit command-class exception;
- post-failover storage inventory can be marked stale until heartbeat plus block-report evidence arrives;
- HDFS-1972 postponed some invalidation work under stale inventory and cleared prior queued decisions during failover.

### Engineering reconstruction

From those documented relations it follows that:

- **connected NameNode ≠ command-authoritative NameNode**;
- **one logical Active ≠ one fencing locus**;
- **runtime command-source authority ≠ crash-persistent fencing promise**;
- **authority currentness ≠ replica-inventory currentness**;
- **over-replication count under stale inventory ≠ safe deletion basis**;
- **uncertainty can be retained as control state to prevent premature forgetting**;
- **previously computed maintenance work can become inadmissible when the authority/freshness context changes**.

These are project reconstructions. Apache did not use this exact comparative vocabulary.

---

## Functional comparisons

### Case 50 — QJM epoch fencing

**Functional bridge:** both mechanisms prevent an older still-existing actor from continuing to define current state after failover.

**Boundary:** QJM puts a **durable promise on JournalNodes** (`lastPromisedEpoch`) and uses quorum overlap to fence edit-log writers. DataNode command fencing uses a **runtime local observation** (`lastActiveClaimTxId` plus selected actor) driven by heartbeat role/txid and is not shown here as crash-persistent.

Therefore:

```text
DataNode lastActiveClaimTxId
    != JournalNode lastPromisedEpoch
```

### Case 49 — generation-stamp lease recovery

**Functional bridge:** monotonic control state helps stale embodiments or attempts remain physically present without remaining admissible.

**Boundary:** generation stamps qualify block/recovery generations; DataNode Active-claim transaction IDs qualify a command source. `block generation stamp != Active-claim txid`.

### Case 28 / 41 — Swift and Cassandra deletion evidence

**Functional bridge:** retained negative/currentness state can prevent an older state from being acted upon as if it were current.

**Boundary:** tombstones qualify application-data currentness across replicas; HDFS stale-inventory state withholds destructive maintenance because the control plane does not yet know enough about replica reality.

### Case 46 — GFS re-observation

**Functional bridge:** some operational state is safer to reconstruct by asking surviving participants what they currently hold rather than trusting an old central record.

**Boundary:** GFS deliberately re-derives chunk locations after master restart; HDFS Case 51 marks replica inventory stale after failover and waits for fresh heartbeat/block-report evidence before certain deletions.

These are functional comparisons, not claims of direct genealogy.

---

## Philosophical interpretation — bounded

The technical fact that creates the conceptual problem is narrow: **authority and knowledge can lag one another**.

A new NameNode can become the accepted control authority while still refusing an irreversible deletion because its replica inventory is not yet fresh. Conversely, an older NameNode can remain alive and communicative while its commands cease to count at the DataNode.

This supports a limited interpretation:

> technical retention may include preserving not only a value, but a distinction about **who may alter it** and an explicit state of **not yet knowing enough to erase it safely**.

The useful point is not that HDFS “remembers” like a human. It is that continued availability of payload depends on second-order states that preserve authority boundaries and uncertainty long enough for re-observation.

The interpretation stops there. `lastActiveClaimTxId` is not an archive, `blockContentsStale` is not phenomenological memory, and neither field establishes a general philosophy of authority.

---

## Claim ledger

| Claim | Label | Evidence | Strength / boundary |
| --- | --- | --- | --- |
| HDFS HA identified dual NameNode commands to one DataNode as a corruption risk | `H/P` | HDFS-1972 | strong historical problem statement |
| DataNode should choose the Active claim with the higher transaction ID | `H/P` | HDFS-2627 | strong direct design statement |
| 2.7.3 heartbeat response carries HA service state plus last applied/written txid | `H/P` | `FSNamesystem.java` | strong release-source evidence |
| DataNode retains selected Active actor plus `lastActiveClaimTxId` | `H/P` | `BPOfferService.java` | strong |
| lower competing Active claim does not replace a more recent accepted claim | `H/P` | `updateActorStatesFromHeartbeat()` | strong |
| HA state is updated before commands from the same heartbeat are processed | `H/P` | `BPServiceActor.offerService()` | strong and ordering-specific |
| destructive/replicative/recovery commands are ignored from Standby actor | `H/P` | `processCommandFromStandby()` | strong, bounded to listed command classes |
| `DNA_ACCESSKEYUPDATE` is permitted from Standby | `H/P` | same source | strong negative boundary |
| post-failover storage inventory can remain stale until heartbeat + block report | `H/P` | `DatanodeStorageInfo.java`; HDFS-1972 patch | strong |
| stale inventory can postpone block invalidation | `H/P` | HDFS-1972 patch | strong historical implementation evidence |
| command authority and inventory freshness are distinct retention relations | `E` | combined source behavior | strong project reconstruction |
| `lastActiveClaimTxId` is crash-persistent like QJM `lastPromisedEpoch` | `X` | source shows ordinary in-memory field initialized to `-1` | rejected |
| Standby means all control messages are ignored | `X` | `DNA_ACCESSKEYUPDATE` exception | rejected |
| `blockContentsStale` means block payload is corrupt | `X` | source defines it as potentially out-of-date inventory after failover | rejected |
| HDFS invented active/standby fencing or monotonic control sequencing | `X` | no priority evidence; scope is mechanism instantiation | rejected |

---

## Related repositories

### `tmzncty/computing-archaeology`

Searched for a dedicated HDFS DataNode-fencing / heartbeat-transaction-ID / failover-inventory case before writing. None was found.

Therefore this case keeps the bounded retention-specific relation here. A broader historical account of HDFS HA architecture, Hadoop release evolution, or distributed-systems fencing genealogy should live in `computing-archaeology` and be linked rather than duplicated.

### `tmzncty/problem-history`

The anti-anachronism rule is useful here: Apache's own 2011 problem was concrete—dual NameNode commands, failover, split brain, and stale block reports. The project-level language of “authority retention” and “inventory freshness” is a later reconstruction and is labeled as such.

---

## Sources

### Apache primary design / issue records

- Apache HDFS-1972, **HA: Datanode fencing mechanism**: <https://issues.apache.org/jira/browse/HDFS-1972>
- HDFS-1972 final December 2011 patch: <https://issues.apache.org/jira/secure/attachment/12508141/hdfs-1972.txt>
- Apache HDFS-2627, **HA: determine DN's view of which NN is active based on heartbeat responses**: <https://issues.apache.org/jira/browse/HDFS-2627>

### Hadoop 2.7.3 release source

- `FSNamesystem.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSNamesystem.java>
- `BPServiceActor.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/BPServiceActor.java>
- `BPOfferService.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/BPOfferService.java>
- `DatanodeStorageInfo.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DatanodeStorageInfo.java>

### Neighboring HA boundary

- Hadoop 2.7.3, **HDFS High Availability Using the Quorum Journal Manager**: <https://hadoop.apache.org/docs/r2.7.3/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithQJM.html>

---

## Maturity

**Status: `grounded`.**

The bounded case is grounded because Apache's 2011 issue/design record states the corruption problem and higher-transaction-ID heartbeat rule directly, while exact Hadoop 2.7.3 release source independently exposes the runtime Active watermark, same-heartbeat update ordering, command-class filtering, and post-failover stale-inventory mechanism.

Remaining work is deliberately separate:

- post-2.7 DataNode command-fencing evolution;
- DataNode restart/split-brain fault injection;
- modern HDFS erasure-coded block-command behavior;
- Observer/read-freshness semantics;
- wider fencing/leader-authority genealogy.
