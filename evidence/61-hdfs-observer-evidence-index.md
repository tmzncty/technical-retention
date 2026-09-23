# Case 61 — HDFS Observer / RBF freshness evidence index

## Status

**Case status: grounded**

This file is the compact evidence navigation for [`Case 61 — Apache HDFS Observer NameNode`](../cases/61-apache-hdfs-observer-stateid-read-freshness.md).

It does not replace the canonical case. Its purpose is to keep the expanding evidence chain navigable while preserving the distinctions between:

- payload / edit-log state;
- NameNode transaction progress;
- client freshness lower bounds;
- Router nameservice-scoped state;
- publication ordering;
- state-ID validity regime;
- publication-budget admission.

No maturity promotion is made by this index.

---

## Canonical case

- [`../cases/61-apache-hdfs-observer-stateid-read-freshness.md`](../cases/61-apache-hdfs-observer-stateid-read-freshness.md)

Canonical bounded question:

> Once mutation authority and replica survival are already handled, what additional retained state is required to decide whether a lagging HDFS replica is fresh enough to serve a particular read?

The canonical case establishes the single-nameservice Observer mechanism around HDFS-12943 / Hadoop 3.3.0:

```text
client accepts response carrying state ID S
    ↓
client retains max frontier S
    ↓
future coordinated read carries S
    ↓
Observer must catch up to at least S
    ↓
read may be admitted
```

Key boundary:

```text
read-capable replica
    != sufficiently fresh replica for this client
```

---

## Evidence chain 1 — canonical Observer state-ID mechanism

### Scope

2017–2020 design and implementation, bounded by the Hadoop 3.3.0 release source and Apache JIRA/documentation.

### Primary anchors

- HDFS-12943 — Consistent Reads from Standby Node;
- HDFS-13688 — `msync()`;
- HDFS-14272 — startup/cross-client state synchronization;
- Hadoop 3.3.0:
  - `ObserverReadProxyProvider`;
  - `ClientGSIContext`;
  - `GlobalStateIdContext`;
  - `ReadOnly`.

### Established relation

```text
namespace replica exists
    != replica is fresh enough for a client

client program order
    != protocol-retained causal lower bound

writer authority
    != read freshness
```

### Status

**grounded in canonical case**

---

## Evidence chain 2 — RBF scope, publication ordering, and validity-regime invalidation

- [`61-hdfs-rbf-2022-2024-federated-stateid-publication-invalidation-deepening.md`](61-hdfs-rbf-2022-2024-federated-stateid-publication-invalidation-deepening.md)

### Scope

2022–2024 Router-Based Federation extension of Observer freshness state.

### Primary anchors

- HADOOP-18345;
- HDFS-13522;
- HDFS-16767;
- Hadoop 3.4.0 `RouterStateIdContext` / `ClientGSIContext`;
- HDFS-17156 and commit `42b4525f75b828bf58170187f030b08622e238ab`;
- HDFS-17514 and commit `6a4f0be854b36b0dd985aba8d3110b0f2928c2fc`.

### Established relations

```text
stateId value
    != complete freshness relation

stateId + nameservice identity
    -> bounded federated freshness relation
```

```text
RPC result visible to caller
    != response currentness metadata already published
```

```text
monotonic inside one valid state-ID regime
    != monotonic across regime invalidation
```

This evidence chain establishes that currentness evidence has **scope**, **publication order**, and **validity state** of its own.

### Status

**bounded deepening complete**

---

## Evidence chain 3 — RBF federated-state publication budget / max-size boundary

- [`61-hdfs-rbf-2024-federated-state-maxsize-publication-boundary-deepening.md`](61-hdfs-rbf-2024-federated-state-maxsize-publication-boundary-deepening.md)

### Scope

Hadoop 3.4.x pre-fix source, HDFS-17558, merged Apache Hadoop PR #6902, and checked 3.5.0 release source.

### Primary anchors

- HDFS-17558 — `maxSizeOfFederatedStateToPropagate` bug report;
- Apache Hadoop PR #6902;
- implementation commit `22acb36e926766215d38096ca90d1277deb200e3`;
- regression-test commit `a78b2493f081be7dd7f7a4efd07216ef96dd2528`;
- merge commit `ebbe9628d34476939343a94484528d3754e92eb9`;
- `RouterStateIdContext.java` from checked Hadoop 3.4.0, 3.4.1, 3.4.2, 3.4.3, and 3.5.0 release tags;
- Hadoop 3.4.0 `ClientGSIContext.java`.

### Historical result

Pre-fix code measured:

```text
raw namespaceIdMap cardinality
```

before response construction, even though unset `Long.MIN_VALUE` entries were filtered out before serialization.

PR #6902 changes the gate to measure:

```text
built RouterFederatedStateProto namespace-entry count
```

after filtering.

Its regression test establishes:

```text
raw map = {ns0 -> 10, ns1 -> MIN_VALUE}
max = 1

publishable count = 1
    -> publish ns0
```

and then:

```text
add ns2 -> 20
max = 1

publishable count = 2
    -> publish no federated-state map
```

Therefore:

```text
retained Router state
    != client-visible propagated state

raw retained cardinality
    != publishable cardinality

max-size policy
    != truncation to M entries
```

The bounded policy is **complete-or-omit**, not arbitrary truncation.

### Release boundary

Checked release source shows:

- 3.4.0 — pre-fix raw-map gate;
- 3.4.1 — pre-fix raw-map gate;
- 3.4.2 — pre-fix raw-map gate;
- 3.4.3 — pre-fix raw-map gate;
- 3.5.0 — post-build count gate present.

No claim is made about every downstream vendor branch or unexamined release.

### Status

**bounded deepening complete**

---

## Consolidated retained-state decomposition

Case 61 now distinguishes at least the following state classes:

| State / relation | Retained or reconstructed where | What it is for | What it is not |
| --- | --- | --- | --- |
| namespace payload / edit state | NameNode / journal machinery | authoritative namespace evolution | proof every Observer is caught up |
| NameNode transaction progress | NameNode | basis for state-ID progress | writer epoch by itself |
| client scalar `lastSeenStateId` | client alignment context | single-nameservice freshness floor | complete namespace history |
| Router namespace frontier map | Router | nameservice-scoped trusted progress | client-visible map by definition |
| pool-local frontier | Router connection-pool context | carry client/namespace lower bound downstream | shared authoritative Router maximum |
| federated response map | RPC response header | publish scoped frontiers to client | all state retained by Router |
| client federated map | client alignment context | retain/merge per-namespace lower bounds | global ordering across nameservices |
| publication-order state | RPC processing path | ensure frontier installed before dependent caller progress | namespace payload itself |
| validity-regime state | NameNode/Router path | decide whether a retained frontier still has a meaningful producer | numeric magnitude of the frontier |
| publication-entry budget | Router response construction | admit or omit complete federated response state | byte-length bound or truncation guarantee |

Compactly:

```text
payload
    != progress number
    != evidence scope
    != retained Router map
    != publishable map
    != publication admission
    != client-retained frontier
    != continuing validity of the frontier-producing regime
```

---

## Cross-evidence boundaries

### Writer authority versus read currentness

Case 61 must remain distinct from adjacent HDFS fencing cases:

```text
QJM epoch fencing
    -> who may extend shared edit history?

DataNode command fencing
    -> whose block-management commands are current?

Observer state IDs
    -> how far must a read replica have caught up for this client?
```

### Currentness value versus currentness publication

The RBF evidence now adds:

```text
frontier F retained
    != F attached to this response
```

and:

```text
frontier values monotonic
    != federated-map publication available on every response
```

A threshold crossing can suppress the map without any namespace frontier moving numerically backward.

### Publication omission versus invalidation

HDFS-17558 and HDFS-17514 are not the same failure:

```text
HDFS-17558
    -> currentness evidence may remain valid internally
    -> publication is gated by response-entry budget

HDFS-17514
    -> producing regime becomes invalid/disabled
    -> stale cached frontier may need reset
```

Thus:

```text
not published now
    != no longer valid
    != globally revoked
```

---

## Historical record / reconstruction discipline

### Historical record

Actor/source-level facts include:

- Apache's Observer and state-ID protocol;
- per-client maximum state retention;
- nameservice-scoped RBF map;
- publication-before-caller-notification fix;
- stale-state invalidation when state context is disabled;
- HDFS-17558 raw-map versus built-map max-size bug;
- PR #6902's post-filter count fix and regression test;
- checked release-source boundary through 3.5.0.

### Engineering reconstruction

Project abstractions include:

- `client freshness frontier`;
- `read-admissibility lower bound`;
- `freshness-scope state`;
- `validity-regime boundary`;
- `retained-vs-published cardinality`;
- `publishable frontier set`;
- `publication-entry budget`.

### Functional analogy

Comparisons with vector-clock/context propagation, replica-progress summaries, cache validators, Kafka high-watermark state, or other bounded metadata envelopes are permitted only at the relation level. They do not establish shared genealogy or identical guarantees.

### Philosophy

No philosophical premise is needed for any Case 61 historical claim. Statements about actor-relative evidence, “the already-seen past,” or knowledge being retained but not exposed are downstream interpretation only.

---

## Current open work

With RBF max-size behavior now grounded, useful remaining slices include:

- exact HDFS-12943 design-PDF and proposal-version archaeology;
- broader post-3.3 Observer consistency regressions beyond the already grounded fixes;
- exact release/backport history for HDFS-17514;
- **mixed old/new-client invalidation and max-threshold fault injection** in a running cluster;
- exact `msync` / Active-fallback behavior when federated-state publication is omitted by the threshold;
- metrics/telemetry for max-size suppression;
- mixed-version 3.4.x / 3.5.0 Router-client behavior;
- WebHDFS and delegation-token-specific behavior;
- end-to-end file-data visibility versus namespace-metadata freshness;
- snapshots, encryption zones, access-time-dependent operation classes;
- independent fault injection measuring stale-read/fallback behavior;
- broader comparison with follower reads in ZooKeeper, Raft-based databases, Spanner-like systems, and object stores.

The former general TODO **“RBF federated-state size-limit behavior”** is no longer open as a mechanism question; it is now replaced by the narrower runtime/fault-injection and interoperability questions above.

---

## Maturity judgment

**grounded — unchanged**

The new max-size evidence closes a specific implementation debt but does not justify promotion beyond the canonical case's current maturity.

Why no promotion:

- implementation and regression-test evidence are strong;
- the checked release horizon is useful but still bounded;
- end-to-end fault injection for threshold crossing remains absent;
- downstream backports and mixed-version behavior remain open;
- client behavior under omission is source-grounded but not yet exercised here as a complete runtime trace.

The correct update is therefore **deeper grounding and better navigation, not a maturity-level increase**.