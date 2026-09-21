# Case 79 Evidence Index — HDFS Startup SafeMode, Re-observation, and Destructive Authority

## Canonical case

- [`../cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md`](../cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md) — **canonical Case 79**, status **`grounded`**.
- [`../cases/117-apache-hdfs-startup-safemode-reobservation.md`](../cases/117-apache-hdfs-startup-safemode-reobservation.md) — later duplicate/consolidation pointer; do not treat as an independent mechanism or maturity track.

Repository-wide maturity remains governed by the canonical case / roadmap / repository ledger rather than this case-local navigation file. This index only records the bounded Case-79 evidence chain and does not alter repository-wide maturity policy.

---

## Evidence chain

### 1. Canonical grounding — namespace persistence vs report-rebuilt location knowledge

The canonical case establishes the core startup split:

```text
durable NameNode namespace
    !=
durable replica-location inventory

surviving DataNode replica
    !=
restarted NameNode has already re-observed that replica
```

Bounded evidence includes released Hadoop 0.18.0 source, the 2010 HDFS architecture paper, Apache HDFS user/architecture documentation, and later released source continuity through 2.7.3/2.8.0.

### 2. Manual SafeMode lifetime deepening

- [`79-hadoop-2008-2016-manual-safemode-restart-lifetime-deepening.md`](79-hadoop-2008-2016-manual-safemode-restart-lifetime-deepening.md)

This slice separates three lifetimes:

```text
durable namespace state
    !=
prior-process manual SafeMode state
    !=
fresh startup SafeMode state after restart
```

It also prevents a false inference from `logSyncAll()`: syncing namespace edits at manual SafeMode entry does not by itself prove that manual SafeMode intent is journaled as namespace state.

### 3. 2006–2008 destructive-command guard deepening

- [`79-hadoop-2006-2008-safemode-destructive-command-guard-deepening.md`](79-hadoop-2006-2008-safemode-destructive-command-guard-deepening.md)

This slice adds the early SafeMode admission/destructive-authority chronology:

```text
2006 HADOOP-306
    -> SafeMode forbids filesystem modification
       and inhibits block replication

2006 HADOOP-594
    -> threshold 0.95 -> 0.999
       so nearly all blocks report before modification

2008 HADOOP-3002
    -> observed block removal while SafeMode active
    -> heartbeat path already guarded
    -> block-report path could also return block commands
    -> removal must be withheld there too

2008 Hadoop 0.17.2
    -> release changelog carries the blocker fix
       "Hold off block removal while in safe mode"
```

The bounded engineering result is:

```text
positive inventory evidence received
    !=
destructive removal authority established
```

and:

```text
SafeMode policy exists
    !=
every command-emission path already enforces it
```

HADOOP-4810 is included only as a separate late-2008 corroborating startup data-loss/deletion hazard. It is **not** merged with HADOOP-3002's root cause.

### 4. HADOOP-3002 exact patch-site genealogy and released-source boundary

- [`79-hadoop-2008-hadoop3002-patch-site-genealogy-deepening.md`](79-hadoop-2008-hadoop3002-patch-site-genealogy-deepening.md)

This slice closes the exact source/branch genealogy left open by the previous evidence:

```text
2008-07-07
9fc0ca9d... initial branch-0.18 merge
    -> broader heartbeat/SafeMode rewrite
    -> lock-order / potential-deadlock concern
    -> 6afd12e3... explicit revert

2008-07-08
trunk SVN r675012 final source revision
    -> branch-0.18 5b3f8571... / SVN r675015
    -> branch-0.17 c32d1180... / SVN r675055
```

The release-bearing source change is concrete:

```text
Hadoop 0.17.1
processReport(...) -> Block[]
    -> block-report processing may return obsolete blocks
    -> NameNode.blockReport may immediately emit DNA_INVALIDATE

HADOOP-3002 / Hadoop 0.17.2
processReport(...) -> void
reportDiff(...) -> explicit toInvalidate result
    -> addToInvalidates(...)
    -> no direct block-report deletion response
    -> ordinary invalidation scheduling emits work later
```

The final patch also moves the SafeMode check upward from replication-only `computeReplicationWork(...)` to `computeDatanodeWork(...)`, so the guard dominates both replication and invalidation work scheduling.

The retention-specific result is:

```text
recognize a deletion obligation
    !=
emit a deletion command now
```

and:

```text
pending invalidation obligation
    !=
current destructive-execution authority
```

The final implementation therefore permits a running NameNode to **retain pending invalidation work while withholding destructive execution during SafeMode**. This is not a claim that `recentInvalidateSets` is crash-persistent; restart rediscovery/reconstruction remains a separate question.

The first-attempt -> revert -> final-patch sequence also supplies a second bounded result:

```text
correct safety policy
    !=
concurrency-safe first implementation
```

The historical record supports a lock-order / potential-deadlock concern and an actual revert; it does not establish that a production deadlock definitely occurred.

---

## Cross-case controls

Use these only as controlled functional comparisons:

- **Case 46 — GFS master recovery:** both systems can re-derive storage-location knowledge after master restart; no historical genealogy is claimed.
- **Case 51 — HDFS DataNode command fencing:** asks *which NameNode* may issue block-changing commands; Case 79 asks whether startup inventory/admission state permits ordinary command work.
- **Case 61 — HDFS Observer freshness:** client-qualified namespace-read freshness is distinct from startup replica re-observation.
- **Case 80 — HDFS rack/failure-domain placement:** safe-block admission does not establish rack-placement satisfaction.
- **Case 83 — HDFS scanner verification history:** maintenance-history control state is not the same as current startup inventory evidence.
- **Case 116 — per-DataNode maintenance expiry:** local maintenance mode is not NameNode-wide startup SafeMode.
- **Case 153 — Ceph snap-trim:** functionally, `cleanup debt exists != actor currently authorized to execute cleanup`; no HDFS/Ceph genealogy is claimed.

Do not collapse these into a single “HDFS safety” or generic distributed-cleanup mechanism.

---

## Vocabulary discipline

### Historical / source vocabulary

- `SafeMode` / `safe mode`;
- `Blockreport` / `block report`;
- `Heartbeat`;
- filesystem modification;
- block replication;
- block removal;
- safe blocks / safely replicated blocks;
- threshold / extension;
- invalidation / excess / under-replication;
- `toInvalidate`, `addToInvalidates`, `recentInvalidateSets` in the relevant source family.

### Engineering reconstruction vocabulary

The repository may use, when explicitly marked:

- `re-observation`;
- `inventory-confidence state`;
- `delayed repair authority`;
- `destructive-command guard`;
- `action-relative evidence sufficiency`;
- `destructive authority`;
- `deletion obligation`;
- `execution authority`.

### Philosophical interpretation only

Terms such as `negative knowledge`, `epistemic closure`, or “absence becomes knowledge” are **not Apache terminology**. They may be used only as bounded interpretation and must not be projected back into historical actors' language.

---

## Status

**Case 79 remains `grounded`.**

The four evidence lines now establish both the early SafeMode/destructive-authority history and the exact HADOOP-3002 patch genealogy through release-bearing 0.17 source. That materially strengthens source custody, but still does not provide the period-correct fault injection, restart reconstruction of invalidation obligations, or complete startup-deletion analysis needed for a maturity promotion.

### Closed across the current evidence chain

- early release-history floor for SafeMode's mutation/replication restriction;
- early threshold-change rationale tied to report progress before modification;
- named 2008 blocker showing block-report command emission could bypass the intended SafeMode removal prohibition;
- release-bearing evidence that Hadoop 0.17.2 carried the block-removal guard fix;
- exact final HADOOP-3002 source revision identity: trunk SVN r675012;
- exact branch-0.18 and branch-0.17 merge commits;
- released 0.17.1 -> 0.17.2 block-report / invalidation patch site;
- first-attempt -> revert -> revised-final chronology and the bounded lock-order concern.

### Still open

1. optionally locate a canonical Git object for historical trunk SVN r675012 if a faithful pre-split mirror exposes one; this is a provenance refinement, not required to establish the final branch diff;
2. period-correct fault injection with delayed/partial reports plus invalidate-command tracing;
3. separate reconstruction of HADOOP-4810 corrupt/excess replica classification and deletion ordering;
4. determine how invalidation obligations are rediscovered or reconstructed across NameNode restart rather than assuming the exact in-memory queue survives.
