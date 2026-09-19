# Case 115 evidence deepening — Hadoop 2.4.1 snapshot HA failover and retry-cache continuity

**Status:** bounded deepening complete

**Case:** [`cases/115-apache-hdfs-snapshot-shared-block-replication.md`](../cases/115-apache-hdfs-snapshot-shared-block-replication.md)

**Bounded question:** In Hadoop 2.4.1 HA, if a snapshot create/delete/rename request has already taken effect on the active NameNode but the client loses the reply and retries after failover, what retained evidence prevents the new active NameNode from treating the retry as a fresh independent mutation?

This note closes one narrow part of Case 115's open HA-failover debt. It does **not** establish arbitrary torn/corrupt shared-edit recovery, every failover interleaving, lower-device durability, or behavior in later Hadoop releases.

---

## 1. Why this slice matters

Case 115 already separates:

```text
snapshot namespace/diff state
    != shared DataNode payload blocks
    != block-replication obligation
    != later block retirement / invalidation
```

The normal-restart deepening added another distinction:

```text
NameNode process-memory loss
    != snapshot namespace-relation loss
```

because snapshot-specific edit operations can be replayed.

HA failover adds a different ambiguity. A client can observe:

```text
request sent
    -> active NN mutates namespace
    -> reply is lost
    -> active changes
    -> client retries same RPC
```

At that point it is not enough for the new active to know only that the namespace mutation exists. It also needs enough retained **operation identity / completion knowledge** to recognize that the retried RPC is the same already-completed request and, where needed, return the prior result.

The bounded retention question is therefore:

> **Can completion identity survive active-NameNode replacement independently of the client receiving the original reply?**

For snapshot create/delete/rename in the inspected Hadoop 2.4.1 HA test path, the answer is yes.

---

## 2. Source custody and fixed baseline

This note is pinned to Apache Hadoop tag:

- tag: `release-2.4.1`
- annotated tag object: `a5ffd153f61c68ae6f62a2f30fac59687c9b0dbd`
- commit: `1b5c6b3a3b90c6e396e00e991b49d170eb2dac55`
- tagger date: **2014-06-30**

Tag object:

<https://github.com/apache/hadoop/tree/release-2.4.1>

Primary source files used here:

1. `hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop/hdfs/server/namenode/ha/TestRetryCacheWithHA.java`
   - <https://github.com/apache/hadoop/blob/release-2.4.1/hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop/hdfs/server/namenode/ha/TestRetryCacheWithHA.java>
2. `hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSEditLog.java`
   - <https://github.com/apache/hadoop/blob/release-2.4.1/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSEditLog.java>
3. `hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSEditLogLoader.java`
   - <https://github.com/apache/hadoop/blob/release-2.4.1/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/namenode/FSEditLogLoader.java>
4. `hadoop-common-project/hadoop-common/src/main/java/org/apache/hadoop/ipc/RetryCache.java`
   - <https://github.com/apache/hadoop/blob/release-2.4.1/hadoop-common-project/hadoop-common/src/main/java/org/apache/hadoop/ipc/RetryCache.java>

A fresh companion search found no dedicated `HDFS snapshot retry cache` packet in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). Broader Hadoop HA / retry-cache / edit-log genealogy should remain there if later developed.

---

## 3. Historical record — snapshot edit records can carry RPC identity

In `FSEditLog.java`, the `release-2.4.1` snapshot log methods are explicit:

```text
logCreateSnapshot(..., boolean toLogRpcIds)
logDeleteSnapshot(..., boolean toLogRpcIds)
logRenameSnapshot(..., boolean toLogRpcIds)
```

Each method constructs its corresponding snapshot edit operation, calls:

```text
logRpcIds(op, toLogRpcIds)
```

and then logs the edit.

`logRpcIds(...)` records the RPC server's current:

```text
clientId
callId
```

onto the edit operation when requested.

### Historical claim H-115.41

**In Hadoop 2.4.1, snapshot create/delete/rename edit operations can retain the originating RPC's client ID and call ID as part of the edit-log record.**

This is not merely snapshot namespace state. It is operation-identity state attached to the logged mutation.

---

## 4. Historical record — edit replay can rebuild retry-cache completion state

`FSEditLogLoader.java` treats snapshot operations specially during replay.

For `OP_CREATE_SNAPSHOT`, the loader:

1. applies the snapshot creation through `SnapshotManager`;
2. obtains the resulting snapshot path;
3. when `toAddRetryCache` is true, calls:

```text
fsNamesys.addCacheEntryWithPayload(
    createSnapshotOp.rpcClientId,
    createSnapshotOp.rpcCallId,
    path)
```

For `OP_DELETE_SNAPSHOT` and `OP_RENAME_SNAPSHOT`, after applying the mutation it calls:

```text
fsNamesys.addCacheEntry(
    rpcClientId,
    rpcCallId)
```

when retry-cache reconstruction is enabled.

The asymmetry matters:

```text
createSnapshot
    -> retry identity + prior result payload (snapshot path)

deleteSnapshot / renameSnapshot
    -> retry identity + successful-completion entry
```

### Historical claim H-115.42

**Snapshot edit replay can reconstruct not only snapshot namespace state but also retry-cache entries keyed by the original RPC identity; create additionally reconstructs the prior result payload used by a retried request.**

Therefore:

```text
namespace replay
    != retry-completion replay
```

although both can be derived from the same edit-log operation.

---

## 5. Historical record — RetryCache exists specifically to recognize successful non-idempotent retries

`RetryCache.java` states its purpose directly: it maintains a cache of non-idempotent requests successfully processed by the RPC server so retries can be recognized. A request is identified by:

```text
unique client ID + call ID
```

When a retry finds a successful existing entry, the previous response can be returned rather than independently re-executing the operation.

`CacheEntryWithPayload` exists for operations whose previous response, or part of it, must be retained to generate the retried response.

The same class provides `addCacheEntry(...)` and `addCacheEntryWithPayload(...)` specifically for entries loaded from edit-log state; the source comments say that an entry loaded from the edit log can be assumed to have succeeded.

### Historical claim H-115.43

**The retry cache is an explicit operation-completion relation, distinct from the snapshot object itself: `(clientId, callId) -> successful prior processing`, optionally with response payload.**

The in-memory cache is not itself claimed to be the durable embodiment. The edit record carries enough information for the relevant entries to be reconstructed.

---

## 6. Historical record — released HA tests exercise lost-reply failover for snapshot operations

`TestRetryCacheWithHA.java` in `release-2.4.1` defines explicit `AtMostOnceOp` implementations for:

- `CreateSnapshotOp`;
- `DeleteSnapshotOp`;
- `RenameSnapshotOp`.

Each has a dedicated test:

```text
testCreateSnapshot()
testDeleteSnapshot()
testRenameSnapshot()
```

and each is run through the same `testClientRetryWithFailover(...)` harness.

The harness deliberately creates the ambiguous-completion condition:

1. prepare the operation;
2. configure a dummy retry invocation handler to throw a fake network exception **after** the RPC invocation has returned from the server path;
3. invoke the operation on the active NameNode;
4. wait until the test confirms that the mutation has actually taken effect on the active NameNode;
5. force NameNode 0 to standby and NameNode 1 to active;
6. stop injecting the fake exception so the client can retry through the failover proxy;
7. wait for the client operation to obtain a result;
8. assert that a retry-cache hit occurred;
9. assert that the new NameNode's retry-cache `updated` metric is positive, with the test comment explicitly attributing that update to NN1 applying the edit log.

### Historical claim H-115.44

**The released Hadoop 2.4.1 HA test suite deliberately exercises snapshot create/delete/rename across the interval “operation took effect, client did not receive the response, active NameNode changed, client retried,” and requires retry-cache participation after failover.**

This is stronger than a generic ordinary-restart test because the ambiguity is at the client-visible RPC completion boundary.

---

## 7. Historical record — the same HA test suite separately demonstrates retry-cache transfer through edit application

`testRetryCacheOnStandbyNN()` runs a set of operations on NN0, captures its retry-cache entries, explicitly rolls the edit log, explicitly tails edits on NN1, shuts down NN0, transitions NN1 to active, and then checks that NN1's retry cache contains the same entries.

This is not snapshot-specific by itself, but it directly demonstrates the release's intended HA path:

```text
retry-relevant operation state
    -> edit log
    -> standby tails/applies edits
    -> standby retry cache populated
    -> standby becomes active
```

Together with the snapshot-specific `testCreateSnapshot`, `testDeleteSnapshot`, and `testRenameSnapshot` cases, it supplies the missing bridge between snapshot operation records and post-failover duplicate suppression.

### Historical claim H-115.45

**In the inspected release tests, retry-cache continuity across NameNode replacement is reconstructed from edit-log application rather than by preserving the previous active NameNode process's heap.**

---

## 8. Engineering reconstruction — three different things can survive one lost reply

The source supports a three-way separation:

```text
A. snapshot namespace result
   e.g. snapshot exists / was deleted / was renamed

B. operation identity
   clientId + callId

C. response/completion knowledge
   successful prior processing
   + optional prior response payload
```

A failover-safe retry path needs more than A.

If only the namespace result survived, a new active might be able to observe the resulting state but still lack a protocol-level proof that a retried RPC is the same completed invocation.

The edit-log RPC IDs and reconstructed retry-cache entry supply B and C.

### Engineering claim E-115.46

> **retained mutation result != retained operation identity != retained response/completion knowledge**

These states can be represented together in one edit record, but they answer different questions.

---

## 9. Engineering reconstruction — client-visible uncertainty can coexist with server-side durable progress

The HA test intentionally creates this state:

```text
server mutation has taken effect
    +
client has not received the successful reply
```

The client's uncertainty therefore does not imply that the system has no evidence of completion.

After failover, the retained/replayed operation identity can let the new active respond to the retry without treating it as a new mutation.

### Engineering claim E-115.47

> **client uncertainty about completion != server loss of completion evidence**

and:

> **lost reply != permission to execute a non-idempotent mutation again as a new operation**

This is a retention relation about protocol history, not payload copying.

---

## 10. Engineering reconstruction — the old runtime cache is disposable if stronger evidence can rebuild it

The old active NameNode's in-memory `RetryCache` does not need to survive as one continuing Java object.

For the bounded path:

```text
old active runtime RetryCache
    -> process/role transition can disappear

edit-log operation carrying RPC identity/result information
    -> standby applies edit
    -> new runtime RetryCache entry
    -> retried RPC recognized
```

This yields:

> **runtime-cache continuity != operation-history continuity**

and:

> **reconstructed control state can preserve a protocol obligation even when its previous in-memory embodiment is gone.**

That is the same broad retention family seen elsewhere in the repository, but the mechanism here is explicitly HDFS edit replay plus retry-cache reconstruction.

---

## 11. Engineering reconstruction — at-most-once response continuity is separate from snapshot payload retention

The retry-cache evidence contains no duplicate copy of the snapshot's DataNode blocks.

A compact decomposition is:

```text
shared DataNode block payload
    != snapshot namespace/diff authority
    != edit-log mutation record
    != RPC identity
    != retry-cache completion/response state
```

Therefore:

> **snapshot payload survives failover** is not the same claim as
> **a retried snapshot mutation is recognized as already completed**.

Both matter to a coherent HA service, but they are different retention problems.

---

## 12. Functional comparison — Case 80 HDFS decommission restart reconstruction

Case 80 shows that a retained higher-level decommission intent can recreate volatile maintenance progress after NameNode restart.

The bounded functional resemblance is:

```text
Case 80
retained exclusion policy
    -> new runtime decommission obligation/progress

Case 115
retained edit operation + RPC identity
    -> new runtime retry-cache completion entry
```

The analogy stops there. Decommission policy/progress and RPC duplicate suppression are different state machines and authorities.

No shared historical origin is claimed beyond both being HDFS mechanisms in their respective version-bounded records.

---

## 13. Functional comparison — ordinary edit replay versus HA ambiguous-completion replay

The earlier Case-115 normal-restart evidence established:

```text
snapshot-specific edit
    -> replay
    -> snapshot namespace relation reconstructed
```

This HA slice adds:

```text
snapshot-specific edit
    + retained RPC identity
    -> standby replay
    -> namespace result reconstructed
    + retry-completion relation reconstructed
    -> same client call can be recognized after failover
```

Thus:

> **namespace replay != duplicate-suppression replay**

Even when one logged operation supplies evidence for both.

---

## 14. Philosophical interpretation — bounded and downstream

`I` — A system may need to retain not only **what state exists now**, but also **which action already happened** and **which answer is owed when that action is asked about again**.

`I` — In that limited sense, operational continuity can depend on retaining an event relation across replacement of the process that originally witnessed the event.

`I` — The same logical completion can survive a change of active machine because the relevant evidence is not identical with one runtime cache object.

These are project interpretations. Hadoop engineers are not being assigned a philosophy of memory, identity, or testimony.

---

## 15. Explicit non-claims

This evidence does **not** establish any of the following:

1. that Hadoop invented at-most-once RPC semantics;
2. that Hadoop invented retry caches;
3. that HDFS snapshots invented HA-safe duplicate suppression;
4. that every HDFS RPC persists retry-cache identity;
5. that every snapshot RPC in every Hadoop release uses identical retry-cache behavior;
6. that `clientId + callId` is globally permanent history;
7. that retry-cache entries are retained forever;
8. that the in-memory `RetryCache` itself is a durable file format;
9. that snapshot payload blocks are duplicated into the edit log;
10. that the edit-log RPC IDs by themselves prove DataNode block health;
11. that replayed retry-cache state proves rack-placement correctness;
12. that replayed retry-cache state proves lower-media durability of NameNode storage under arbitrary power loss;
13. that the test injects torn/corrupt edit-log records;
14. that the test proves every crash instruction boundary;
15. that the test proves every JournalNode quorum-loss interleaving;
16. that the test proves split-brain is impossible under every external failure;
17. that successful duplicate suppression means the original client observed the first reply;
18. that the same response is reconstructed for every HDFS operation; createSnapshot specifically uses a payload-bearing entry here;
19. that delete/rename payload-free cache entries contain no relevant historical information; they still retain successful completion identity;
20. that snapshot namespace state and retry-completion state are the same state;
21. that ordinary NameNode restart and HA active/standby failover are identical recovery paths;
22. that the exact `release-2.4.1` code remains unchanged today;
23. that edit-log replay is equivalent to a database transaction protocol in implementation or genealogy;
24. that a retry-cache hit proves secure deletion, reclamation, or sanitization of any block;
25. that this evidence closes the broader Hadoop HA / shared-edits history.

---

## 16. Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| Hadoop 2.4.1 snapshot create/delete/rename edit methods can record RPC clientId/callId | H/P | direct `FSEditLog.java` |
| `logRpcIds` copies server client ID + call ID into eligible edit operations | H/P | direct `FSEditLog.java` |
| replay of createSnapshot can rebuild a retry-cache entry with the returned snapshot path payload | H/P | direct `FSEditLogLoader.java` |
| replay of deleteSnapshot/renameSnapshot can rebuild successful retry-cache entries keyed by RPC identity | H/P | direct `FSEditLogLoader.java` |
| RetryCache defines successful non-idempotent request identity by client ID + call ID | H/P | direct `RetryCache.java` |
| RetryCache can retain previous response payload needed to answer a retry | H/P | direct `CacheEntryWithPayload` |
| released HA tests exist for createSnapshot/deleteSnapshot/renameSnapshot through one failover retry harness | H/P | direct `TestRetryCacheWithHA.java` |
| the harness waits until the old active has applied the mutation before forcing failover | H/P | direct test code |
| the harness intentionally withholds the first usable client response by injecting a post-invocation network exception | H/P | direct dummy handler + harness |
| the harness requires a retry-cache hit after failover and observes NN1 cache update from edit application | H/P | direct assertions/comments in test |
| runtime RetryCache continuity is unnecessary if edit-log evidence reconstructs the relevant entry | E | bounded reconstruction from loader/test path |
| mutation result, operation identity, and response/completion knowledge are distinct retention relations | E | bounded relation decomposition |
| client uncertainty about receipt of completion does not imply absence of server-side completion evidence | E | bounded reconstruction from test geometry |
| snapshot payload retention is equivalent to retry-cache retention | X | explicitly rejected |
| the test proves arbitrary torn shared-edit recovery | X | explicitly rejected |
| this release behavior proves all modern HDFS behavior | X | explicitly rejected |

---

## 17. Remaining evidence debt

This slice closes only the **released HA ambiguous-completion / retry-cache reconstruction** part of the prior Case-115 HA debt.

Still open:

1. fault injection at the exact edit append / sync / JournalNode quorum boundaries for snapshot operations;
2. torn/corrupt shared-edit segments and recovery policy;
3. explicit JournalNode quorum-loss and restoration cases;
4. exact active/standby fencing and split-brain failure boundaries for the same snapshot operations;
5. persistence/expiry policy of retry-cache reconstruction across longer checkpoint/history horizons;
6. later-release evolution of snapshot retry-cache handling;
7. composition with lower filesystem/device durability;
8. post-delete DataNode invalidation/restart races already identified by the canonical case.

The safe closed statement is narrower:

> **For the inspected Hadoop 2.4.1 HA regression path, a snapshot mutation can take effect on one active NameNode, lose its first client-visible response, cross active-NameNode failover, and have the retried call recognized from edit-reconstructed retry state rather than treated as an unrelated fresh mutation.**
