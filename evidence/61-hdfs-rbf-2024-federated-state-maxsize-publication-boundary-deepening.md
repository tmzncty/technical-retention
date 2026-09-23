# Case 61 deepening — HDFS RBF federated-state max-size publication boundary (2024)

## Status

**bounded deepening complete**

This evidence slice deepens [`Case 61 — Apache HDFS Observer NameNode`](../cases/61-apache-hdfs-observer-stateid-read-freshness.md) at one narrow boundary left open by the earlier RBF work:

> When a Router retains freshness frontiers for several HDFS nameservices, what exactly does the configured federated-state `maxsize` bound, and what happens when the retained Router map and the client-visible map have different cardinalities?

The answer matters for technical retention because RBF retains more currentness evidence than it necessarily publishes on every response. Apache's 2024 HDFS-17558 report and merged PR #6902 expose a concrete bug where the implementation confused the cardinality of **retained Router state** with the cardinality of **publishable response state**.

The bounded engineering relation is:

```text
retained currentness state
    != client-visible currentness state

raw Router map cardinality
    != serialized frontier cardinality

publication budget
    != truncation policy
```

`publication budget`, `publishable frontier set`, and `retained-vs-published cardinality` below are project reconstruction terms. They are not Apache historical vocabulary.

---

## Why this is a separate slice

The existing RBF deepening already grounds three obligations:

1. state IDs must retain **nameservice scope**;
2. response currentness metadata must be processed **before dependent caller progress**;
3. cached state IDs must sometimes be **invalidated** when their producing regime disappears.

Those results are documented in:

- [`61-hdfs-rbf-2022-2024-federated-stateid-publication-invalidation-deepening.md`](61-hdfs-rbf-2022-2024-federated-stateid-publication-invalidation-deepening.md).

This slice does not repeat them. It isolates a fourth obligation:

> **The set of retained frontiers and the set eligible to cross an RPC boundary are different objects, so a size limit has to be applied to the latter if it is intended to bound publication.**

That distinction became explicit in HDFS-17558 and PR #6902.

---

## Source and evidence classification

### P1 — Apache JIRA HDFS-17558

**HDFS-17558 — “RBF: Make maxSizeOfFederatedStateToPropagate work on setResponseHeaderState.”**

- created: 26 June 2024;
- updated: 17 July 2024;
- component: `rbf`;
- priority: Major;
- current JIRA state at the time of this research: **Open / Unresolved**;
- linked to GitHub PR #6902.

The issue states that when `namespaceIdMap` grows beyond `DFS_ROUTER_OBSERVER_FEDERATED_STATE_PROPAGATION_MAXSIZE`, federated state does not propagate, and calls that behavior inconsistent with the configuration description.

Source:
<https://issues.apache.org/jira/browse/HDFS-17558>

The current issue status is kept separate from the code-history fact that its associated PR was merged. A merged patch must not be rewritten as a resolved JIRA when the issue record itself still says Open/Unresolved.

### P2 — Apache Hadoop PR #6902

PR #6902 carries the same HDFS-17558 title and was merged into Apache Hadoop `trunk` on **17 July 2024**.

- PR: <https://github.com/apache/hadoop/pull/6902>
- merge commit: `ebbe9628d34476939343a94484528d3754e92eb9`
- implementation commit in the PR: `22acb36e926766215d38096ca90d1277deb200e3`
- test commit in the PR: `a78b2493f081be7dd7f7a4efd07216ef96dd2528`

The patch changes only a small amount of `RouterStateIdContext` code, but it changes what the configured threshold is measuring.

### P3 — Hadoop 3.4.0 release source

`RouterStateIdContext.java` in `rel/release-3.4.0` is the pre-fix implementation used as the bounded release witness here:

<https://github.com/apache/hadoop/blob/rel/release-3.4.0/hadoop-hdfs-project/hadoop-hdfs-rbf/src/main/java/org/apache/hadoop/hdfs/server/federation/router/RouterStateIdContext.java>

It keeps:

```text
ConcurrentHashMap<String, LongAccumulator> namespaceIdMap
```

and obtains `maxSizeOfFederatedStateToPropagate` from the RBF configuration.

### P4 — RBF configuration source

The configuration key is:

```text
dfs.federation.router.observer.federated.state.propagation.maxsize
```

with a default value of **5** in the bounded RBF source.

The configuration text describes it as the maximum size of federated state sent in the RPC header and explains the tradeoff: propagating federated state can avoid repeated `msync`, at the cost of a larger RPC header.

Release-source path:
<https://github.com/apache/hadoop/blob/rel/release-3.4.0/hadoop-hdfs-project/hadoop-hdfs-rbf/src/main/resources/hdfs-rbf-default.xml>

### P5 — Hadoop 3.4.0 client source

`ClientGSIContext.java` in `rel/release-3.4.0` is used to bound the client-side consequence of an omitted federated-state field:

<https://github.com/apache/hadoop/blob/rel/release-3.4.0/hadoop-hdfs-project/hadoop-hdfs-client/src/main/java/org/apache/hadoop/hdfs/ClientGSIContext.java>

It merges a newly received `RouterFederatedStateProto` into the previously retained client map only when the response header actually contains that field. If the field is absent, the existing `routerFederatedState` object is not explicitly cleared by that method.

### P6 — exact release-source checks after the merged patch

The same `RouterStateIdContext.java` path was checked in:

- `rel/release-3.4.1`;
- `rel/release-3.4.2`;
- `rel/release-3.4.3`;
- `rel/release-3.5.0`.

The three checked 3.4.x maintenance releases still use the pre-fix raw-map gate. `rel/release-3.5.0` uses the post-build count gate. The 3.5.0 source also contains an observer-read-eligibility filter that is later than the minimal HDFS-17558 patch and is **not attributed to HDFS-17558 here**.

Sources:

- <https://github.com/apache/hadoop/blob/rel/release-3.4.1/hadoop-hdfs-project/hadoop-hdfs-rbf/src/main/java/org/apache/hadoop/hdfs/server/federation/router/RouterStateIdContext.java>
- <https://github.com/apache/hadoop/blob/rel/release-3.4.2/hadoop-hdfs-project/hadoop-hdfs-rbf/src/main/java/org/apache/hadoop/hdfs/server/federation/router/RouterStateIdContext.java>
- <https://github.com/apache/hadoop/blob/rel/release-3.4.3/hadoop-hdfs-project/hadoop-hdfs-rbf/src/main/java/org/apache/hadoop/hdfs/server/federation/router/RouterStateIdContext.java>
- <https://github.com/apache/hadoop/blob/rel/release-3.5.0/hadoop-hdfs-project/hadoop-hdfs-rbf/src/main/java/org/apache/hadoop/hdfs/server/federation/router/RouterStateIdContext.java>

### Related-repository check

A repository search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for HDFS Observer, `RouterFederatedState`, and HDFS-17558 found no dedicated technical-history packet to reuse. This slice therefore remains retention-specific and does not attempt a parallel general history of HDFS RBF.

---

## Historical record 1 — Hadoop 3.4.0 gated on the raw retained map

In Hadoop 3.4.0, `updateResponseState()` performs the threshold check before building the outbound protobuf:

```text
if namespaceIdMap.size() <= maxSize
    -> setResponseHeaderState(...)
else
    -> do not attach RouterFederatedState
```

Inside `setResponseHeaderState()`, however, not every retained map entry is actually serialized. The code iterates the map and only inserts an entry into `RouterFederatedStateProto` when:

```text
value != Long.MIN_VALUE
```

That creates two cardinalities:

```text
R = all keys retained in namespaceIdMap
P = keys whose value is publishable into the response protobuf
```

where, in the bounded 3.4.0 source:

```text
P = { ns in R | stateId(ns) != Long.MIN_VALUE }
```

The pre-fix gate tested:

```text
|R| <= M
```

while the object sent to the client contained only:

```text
P
```

This is not merely a naming issue. It means a retained placeholder/unset nameservice can count against the publication threshold even though that entry would not consume a state-ID slot in the serialized federated map.

### Safe historical claim

> **In the checked Hadoop 3.4.x implementation, the configured federated-state threshold was applied to the raw `namespaceIdMap` before unset entries were filtered out of the response protobuf.**

This is source-level implementation evidence, not an inference from documentation alone.

---

## Historical record 2 — HDFS-17558 identified the retained/published mismatch

HDFS-17558 describes the externally relevant symptom:

```text
namespaceIdMap grows beyond configured max
    -> federated state does not propagate
```

The issue says this conflicts with the intended configuration behavior of limiting the size of the federated state propagated to the client.

The important point for this repository is narrower than “there was a bug”:

> **The object whose cardinality was being bounded was not necessarily the object being published.**

The Router may know about several namespaces while only a subset currently has a meaningful frontier eligible for serialization.

This supports:

```text
retained namespace membership
    != publishable currentness evidence
```

and:

```text
state container size
    != response evidence size
```

---

## Historical record 3 — the 2024 patch moves the threshold after filtering

PR #6902 changes the code in two coordinated steps.

### Before

Conceptually:

```text
updateResponseState:
    if raw namespaceIdMap.size <= M:
        build federated response
        filter Long.MIN_VALUE while building
        publish response
```

### After

Conceptually:

```text
updateResponseState:
    build federated response
    filter non-publishable entries while building
    if built response entry count <= M:
        publish response
```

The exact implementation changes the threshold expression from raw `namespaceIdMap.size()` to:

```text
builder.getNamespaceStateIdsCount()
```

inside `setResponseHeaderState()`.

Thus the patch changes the bounded predicate from:

```text
|R| <= M
```

to:

```text
|P| <= M
```

for the entries actually assembled for propagation.

### Important terminology boundary

Although the property is named `maxsize` and the configuration description speaks of state size in the RPC header, the checked implementation compares an **entry count**, not a serialized byte length.

Therefore this slice uses:

```text
publication-entry budget
```

as an engineering description of what the source actually enforces.

It does **not** claim that HDFS-17558 implemented a byte-size budget.

---

## Historical record 4 — the regression test proves complete-or-omit behavior, not truncation

The test added in PR #6902 is particularly valuable because it establishes two sides of the boundary with concrete map contents.

The test configures:

```text
maxSize = 1
```

and first constructs a Router map containing:

```text
ns0 -> 10
ns1 -> Long.MIN_VALUE
```

The raw map therefore contains two keys, but only one meaningful frontier is serializable.

The expected response contains **one** federated-state entry.

This is the direct regression case:

```text
|R| = 2
|P| = 1
M   = 1

pre-fix raw-map gate:
    2 > 1 -> suppress publication

post-fix built-map gate:
    1 <= 1 -> publish ns0
```

The test then adds:

```text
ns2 -> 20
```

Now there are two meaningful frontiers while `M` remains one. The expected response contains **zero** federated-state entries.

That gives a second and equally important rule:

```text
|P| > M
    -> publish no RouterFederatedState map
```

not:

```text
|P| > M
    -> choose any M entries and publish a truncated map
```

So the observed policy is **complete-or-omit**, not truncation.

### Why this matters

A simple phrase such as “the Router limits the federated state to five namespaces” would be misleading. In the checked implementation lineage, exceeding the limit does not mean the client receives an arbitrary or priority-selected subset of at most five nameservices. It can mean the sideband federated-state map is omitted altogether.

---

## Historical record 5 — client retention means omission is not global revocation

Hadoop 3.4.0 `ClientGSIContext.receiveResponseState()` distinguishes responses that contain `routerFederatedState` from those that do not.

When the field exists, the client merges the returned per-namespace map into its retained map using per-namespace maxima.

When the field is absent, that method does **not** clear the previously retained `routerFederatedState`; instead it follows the scalar `stateId` branch.

Therefore the max-size suppression boundary must not be described as:

```text
Router omits federated state
    -> every client forgets all previously learned namespace frontiers
```

A more precise relation is:

```text
Router omits this response's federated map
    != previously retained client map is necessarily erased
```

and:

```text
new client with no prior federated map
    != old client carrying prior federated map
```

This resembles the old/new-client distinction already exposed by HDFS-17514, but the trigger is different:

- HDFS-17514 concerns **validity-regime invalidation**;
- HDFS-17558 concerns **publication-budget gating**.

The mechanisms must not be collapsed.

---

## Historical record 6 — checked release boundary

The exact release files checked here give a useful bounded chronology.

| Release source | Threshold placement | Bounded observation |
| --- | --- | --- |
| Hadoop 3.4.0 | before response construction | raw `namespaceIdMap.size()` gate |
| Hadoop 3.4.1 | before response construction | same pre-fix gate |
| Hadoop 3.4.2 | before response construction | same pre-fix gate |
| Hadoop 3.4.3 | before response construction | same pre-fix gate |
| Hadoop 3.5.0 | after response construction/filtering | built map count gate |

PR #6902 was merged to `trunk` on 17 July 2024. The checked 3.4.1–3.4.3 release tags still contain the earlier implementation, while the checked 3.5.0 release tag contains the post-build count behavior.

This supports only the bounded release statement:

> **The HDFS-17558-style gating change is absent from the checked Hadoop 3.4.0–3.4.3 release sources and present in the checked Hadoop 3.5.0 release source.**

It does not establish every downstream vendor backport, branch state, or unpublished build.

The 3.5.0 source additionally filters on whether a namespace is Observer-read eligible before counting the built map. That later eligibility predicate is noted only as part of the 3.5.0 release witness; it is not attributed to the minimal HDFS-17558 patch without separate genealogy evidence.

---

## Engineering reconstruction — retention and publication are two state planes

The combined source evidence supports a useful decomposition:

```text
NameNode progress
    ↓
Router retains nameservice-scoped frontier
    ↓
Router decides which retained entries are publishable
    ↓
Router applies publication-entry budget
    ↓
response either carries the complete built map or omits it
    ↓
client may merge newly published state with previously retained state
```

At least four predicates are distinct:

1. **retained** — does the Router have a map entry for this nameservice?
2. **meaningful/eligible** — should that entry be included in the response map?
3. **budget-admissible** — is the complete built map at or below the configured count?
4. **client-retained** — has a particular client already learned a frontier from an earlier response?

Therefore:

```text
Router knows frontier F(ns)
    != current response publishes F(ns)

current response omits F(ns)
    != client has never retained F(ns)

client retained F(ns)
    != Router must publish F(ns) again on every response
```

This is a control-state retention problem rather than namespace-payload durability.

---

## Engineering reconstruction — per-entry monotonicity does not imply publication monotonicity

Inside a valid state-ID regime, the Router and client use maxima so a namespace frontier normally advances monotonically.

But the **availability of the federated map on a response** is governed by a separate predicate:

```text
publishable entry count <= M
```

That means the following sequence is possible at the relation level:

```text
time t:
    P has M entries
    -> federated map may be published

time t+1:
    P has M+1 entries
    -> federated map omitted
```

No individual namespace frontier had to move backward for the sideband map to disappear from the next response.

So:

```text
monotonic frontier values
    != monotonic publication availability
```

This is not a claim that the client then necessarily becomes stale; existing client-side retained state and other synchronization paths remain relevant. It is only the narrower claim that **control evidence can be monotonic in value while its transport availability is non-monotonic under a publication budget**.

---

## Engineering reconstruction — a budget policy is part of currentness semantics

The max-size configuration might look like a performance knob because it trades response-header growth against repeated synchronization work. The test shows why it also has a semantic boundary worth recording.

A budget policy must answer at least:

```text
what is counted?
when is it counted?
which entries are eligible?
what happens when the limit is exceeded?
what previously retained client state survives omission?
```

HDFS-17558 exists because the first two questions were initially answered by different stages of the implementation.

The corrected source aligns them:

```text
build the state actually eligible for publication
    -> count that built state
    -> decide whether to publish it
```

This is an example of a broader retention rule:

> **When retained state is transformed before publication, admission limits should be reasoned about at the same representation boundary as the object the limit is supposed to govern.**

That sentence is an engineering reconstruction, not Apache historical wording.

---

## Failure / transition matrix

| Condition | Router-retained state | Response federated state | What must not be inferred |
| --- | --- | --- | --- |
| map empty | none | absent | namespace payload absent |
| raw map contains unset placeholders; built map within limit | more raw keys than meaningful frontiers | post-fix: complete meaningful map may be sent | raw key count equals outbound count |
| built map exactly at limit | retained frontiers present | complete built map may be sent | only one selected subset is guaranteed |
| built map exceeds limit | retained frontiers may still exist | federated map omitted | Router forgot those frontiers |
| response omits map after client learned earlier map | Router may still retain frontiers | no new map in this response | client necessarily cleared earlier map |
| state-ID producer becomes invalid/disabled | separate validity-regime problem | may require reset/invalidation logic | size-limit omission is equivalent to HDFS-17514 invalidation |

---

## Historical record versus engineering reconstruction

### Historical record

Directly supported by Apache records and source:

- HDFS-17558 reports that raw `namespaceIdMap` size could suppress federated-state propagation;
- Hadoop 3.4.0 applies the threshold before filtering out `Long.MIN_VALUE` entries;
- PR #6902 moves the threshold to the built protobuf's namespace-entry count;
- the added test demonstrates `2 raw / 1 meaningful / max 1 -> 1 published`;
- the same test demonstrates `2 meaningful / max 1 -> 0 published`;
- `ClientGSIContext` retains/merges previously received federated state rather than clearing it merely because a later response lacks that field;
- checked 3.4.1, 3.4.2, and 3.4.3 release source still has the old gate;
- checked 3.5.0 release source has the post-build gate;
- the JIRA remains Open/Unresolved even though PR #6902 was merged.

### Engineering reconstruction

Project abstractions derived from those records:

- `retained-vs-published cardinality`;
- `publishable frontier set`;
- `publication-entry budget`;
- `monotonic value ≠ monotonic publication availability`;
- `budget admission should be evaluated at the representation boundary it governs`.

These are not attributed to Apache developers as historical terminology.

---

## Functional analogy

A bounded functional analogy can be made to other systems that retain a large control-state set but publish only a representation that passes a transport or protocol budget.

Examples include:

- bounded dependency/context propagation;
- compacted synchronization metadata;
- metadata sidecars constrained by protocol envelopes;
- cache-validation or replica-progress summaries.

The analogy stops at the relation:

```text
internal control state
    -> filtered/encoded outward evidence
    -> transport/admission budget
```

This evidence does **not** establish genealogy from vector clocks, cache validators, databases, or other metadata-compression schemes to HDFS RBF.

It also does not show that HDFS uses a generic metadata truncation framework: the tested policy is specifically complete-or-omit at this boundary.

---

## Philosophical interpretation

No philosophical claim is necessary to establish the case.

A later synthesis may observe that a system can retain a fact internally without making that fact available to another participant, and that “having evidence” is therefore actor- and interface-relative. That is downstream interpretation only.

The historical claim remains concrete:

> RBF can retain nameservice state IDs that are not attached to a particular client response because publication is governed by filtering and a configured entry-count threshold.

---

## Explicit non-claims

This slice does **not** claim that:

1. HDFS invented bounded freshness-context propagation;
2. `maxsize` is a serialized byte-length limit — the checked code compares namespace-entry counts;
3. exceeding the threshold truncates the map to the first or most important `M` namespaces;
4. map omission means Router state has been deleted;
5. map omission means every client forgets previously learned federated state;
6. map omission by itself proves a stale read occurred;
7. the max-size mechanism replaces Observer catch-up, `msync`, Active fallback, or other consistency paths;
8. HDFS-17558 is resolved in JIRA — the current issue record remains Open/Unresolved;
9. the change was backported to checked Hadoop 3.4.1–3.4.3 releases;
10. the 3.5.0 Observer-eligibility filter was introduced by HDFS-17558;
11. every downstream Hadoop distribution follows the same release/backport history;
12. a large Router state map implies a large namespace payload or namespace-data durability problem.

---

## Chronology

| Date / release | Evidence | Retention-specific significance |
| --- | --- | --- |
| 2022 RBF Observer work | federated nameservice-state map introduced | currentness evidence becomes nameservice-scoped |
| Hadoop 3.4.0 | raw map size checked before serialization filtering | retained-map count governs publication |
| 26 Jun 2024 | HDFS-17558 created; implementation commit authored | retained/published cardinality mismatch explicitly reported and patched |
| 17 Jul 2024 | regression test added; PR #6902 merged to trunk | complete-or-omit behavior and post-filter count boundary are tested |
| checked 3.4.1–3.4.3 release source | old gate still present | no release-source evidence of the patch in these checked maintenance tags |
| Hadoop 3.5.0 release source | built-map count gate present | post-filter publication predicate appears in checked release source |

---

## Retention decomposition added by this slice

The Case 61 retained-state stack can now be expanded to:

```text
namespace payload / edit state
    != NameNode transaction progress
    != Router nameservice -> frontier map
    != publishable subset of Router frontier entries
    != publication-entry budget decision
    != serialized federated response state
    != client-retained federated map
    != validity of the state-ID-producing regime
```

The small size of the metadata does not make these relations interchangeable.

The strongest bounded conclusion is:

> **RBF's client-visible freshness evidence is not simply “whatever the Router retains.” It is a filtered representation whose publication is separately admitted by an entry-count budget; a 2024 bug arose because the pre-fix code applied that budget to the raw retained map instead of the representation actually eligible for publication.**

---

## Open work after this slice

The max-size implementation boundary is now grounded, but several narrower questions remain useful future slices:

- end-to-end fault injection with new versus already-stateful clients when the map crosses the threshold during a session;
- exact interaction between map omission and `msync`/Active fallback under RBF in a running cluster;
- telemetry/metrics, if any, that make suppression due to the threshold operationally visible;
- mixed-version Router/client behavior around the 3.4.x → 3.5.0 release boundary;
- downstream-vendor backports;
- byte-level RPC overhead as nameservice count grows;
- separate genealogy of the later `isNamespaceObserverReadEligible()` filter.

These are follow-on questions, not blockers for the bounded retained-vs-published cardinality relation established here.

---

## Status judgment

This slice supports **no maturity promotion** for Case 61. The canonical case remains **grounded**.

The contribution is narrower: one explicit open debt — RBF federated-state size-limit behavior — is now converted from a general TODO into a source-grounded implementation boundary with an exact regression test and a checked release horizon.