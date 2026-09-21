# Case 79 Evidence Index — HDFS Startup SafeMode, Re-observation, and Destructive Authority

## Canonical case

- [`../cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md`](../cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md) — **canonical Case 79**, status **`grounded`**.
- [`../cases/117-apache-hdfs-startup-safemode-reobservation.md`](../cases/117-apache-hdfs-startup-safemode-reobservation.md) — later duplicate/consolidation pointer; do not treat as an independent mechanism or maturity track.

`CASE_INDEX.md` is currently empty even though `ROADMAP.md` still describes it as an authoritative maturity ledger. This local index therefore records the bounded Case-79 status conservatively from the canonical case and its evidence chain; it does **not** reconstruct the repository-wide ledger.

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

---

## Cross-case controls

Use these only as controlled functional comparisons:

- **Case 46 — GFS master recovery:** both systems can re-derive storage-location knowledge after master restart; no historical genealogy is claimed.
- **Case 51 — HDFS DataNode command fencing:** asks *which NameNode* may issue block-changing commands; Case 79 asks whether startup inventory/admission state permits ordinary command work.
- **Case 61 — HDFS Observer freshness:** client-qualified namespace-read freshness is distinct from startup replica re-observation.
- **Case 80 — HDFS rack/failure-domain placement:** safe-block admission does not establish rack-placement satisfaction.
- **Case 83 — HDFS scanner verification history:** maintenance-history control state is not the same as current startup inventory evidence.
- **Case 116 — per-DataNode maintenance expiry:** local maintenance mode is not NameNode-wide startup SafeMode.

Do not collapse these into a single “HDFS safety” mechanism.

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
- invalidation / excess / under-replication in the relevant source families.

### Engineering reconstruction vocabulary

The repository may use, when explicitly marked:

- `re-observation`;
- `inventory-confidence state`;
- `delayed repair authority`;
- `destructive-command guard`;
- `action-relative evidence sufficiency`;
- `destructive authority`.

### Philosophical interpretation only

Terms such as `negative knowledge`, `epistemic closure`, or “absence becomes knowledge” are **not Apache terminology**. They may be used only as bounded interpretation and must not be projected back into historical actors' language.

---

## Status

**Case 79 remains `grounded`.**

The new 2006–2008 evidence materially deepens one seam—SafeMode as an admission regime whose destructive block-removal prohibition had to cover all command-emission paths—but does not supply enough fault-injection, complete source-diff genealogy, or cross-release exhaustiveness for promotion.

### Closed in this slice

- early release-history floor for SafeMode's mutation/replication restriction;
- early threshold-change rationale tied to report progress before modification;
- named 2008 blocker showing block-report command emission could bypass the intended SafeMode removal prohibition;
- release-bearing evidence that Hadoop 0.17.2 carried the block-removal guard fix.

### Still open

- exact final HADOOP-3002 SVN/Git commit and parent diff;
- exact branch-0.17 / branch-0.18 patch-site comparison;
- period-correct fault injection with delayed/partial reports plus invalidate-command tracing;
- separate reconstruction of HADOOP-4810 corrupt/excess replica classification;
- repository-wide `CASE_INDEX.md` repair, which should remain a dedicated navigation task rather than being folded into Case 79.
