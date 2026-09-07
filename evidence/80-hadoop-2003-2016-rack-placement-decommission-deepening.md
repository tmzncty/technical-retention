# Case 80 deepening — HDFS rack-aware placement, decommission sufficiency, and failure-domain topology

## Purpose

Deepen the already-grounded Case 80 without creating a second HDFS decommission case. The narrow question is:

> when a live DataNode is being withdrawn, why is a surviving replica count not by itself the same thing as a satisfactory retained placement relation?

The evidence chain is bounded to:

- Google File System rack-aware replica placement in 2003 as an earlier distributed-filesystem prior-art floor;
- Hadoop 0.18 HDFS architecture documentation for an early HDFS rack-aware placement policy and its explicit reliability/performance tradeoff;
- exact Hadoop 2.7.3 `BlockPlacementPolicyDefault` and `DecommissionManager` source for placement verification and decommission sufficiency.

This record separates historical record, engineering reconstruction, functional comparison, and prior-art restraint. It does **not** attempt a full GFS→HDFS design genealogy or a general data-center failure-domain history.

---

## Source A — Ghemawat, Gobioff, and Leung, _The Google File System_ (SOSP 2003)

**Type:** original systems paper; primary/contemporary technical source.

**Artifact:** Sanjay Ghemawat, Howard Gobioff, Shun-Tak Leung, _The Google File System_, SOSP 2003, §4.2 `Replica Placement`.

**URL:** <https://static.googleusercontent.com/media/research.google.com/en/us/archive/gfs-sosp2003.pdf>

### Directly inspected evidence

The paper describes chunkservers distributed across many racks and says that merely spreading replicas across machines is not enough for its reliability/availability objective. Chunk replicas are also spread across racks so replicas can survive an entire rack becoming damaged or offline, including shared-resource failures such as a network switch or power circuit. The paper simultaneously records the cost: writes must send data to multiple racks.

This supplies an earlier distributed-file-system witness for the relation:

> **replica multiplicity ≠ failure-domain diversity.**

The PDF text at printed/page index 7 was directly inspected. No figure-level claim depends on this source.

### Supports

- explicit rack-level failure-domain placement in a large distributed filesystem by 2003;
- a historical engineering tradeoff between cross-rack survival/bandwidth and cross-rack write traffic;
- an earlier mechanism floor that blocks any HDFS-first claim for the general idea of spreading replicated file data across racks.

### Does not support

- direct implementation descent from GFS to HDFS;
- identity of GFS placement policy and any particular HDFS release;
- decommission semantics in HDFS;
- a claim that rack labels perfectly model every correlated physical failure.

---

## Source B — Hadoop release-0.18.0 HDFS architecture documentation

**Type:** Apache release documentation; primary institutional source.

**Artifact:** `docs/hdfs_design.html`, section `Replica Placement: The First Baby Steps`, ref `release-0.18.0`.

**URL:** <https://github.com/apache/hadoop/blob/release-0.18.0/docs/hdfs_design.html>

### Directly inspected evidence

The document says replica placement is critical to HDFS reliability and performance and describes the purpose of a rack-aware policy as improving reliability, availability, and network bandwidth utilization.

It first gives a `simple but non-optimal` policy of placing replicas on unique racks. The benefit is survival of a whole-rack failure and use of bandwidth from multiple racks; the cost is increased write traffic across racks.

For the common replication-factor-three case, the same 0.18 document instead describes:

```text
replica 1 -> one node in the local rack
replica 2 -> another node in the local rack
replica 3 -> a node in a different rack
```

It explicitly notes that this uses only two unique racks rather than three.

### Supports

- HDFS itself distinguished replica count from rack distribution by the 0.18 release documentation;
- maximal rack spread was already treated as a policy option with a write-cost tradeoff, not as a synonym for replication factor;
- three replicas could intentionally occupy two racks in the bounded 0.18 policy.

### Boundary

This is a release-bounded policy description. It must not be silently substituted for the exact 2.7.3 target ordering below.

---

## Source C — Hadoop 2.7.3 `BlockPlacementPolicyDefault.java`

**Type:** exact release source; primary implementation evidence.

**Path:** `hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/BlockPlacementPolicyDefault.java`

**URL:** <https://github.com/apache/hadoop/blob/branch-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/BlockPlacementPolicyDefault.java>

### Directly inspected evidence — target selection

The class comment describes a factor-three path that is not the same ordering as the 0.18 documentation:

```text
replica 1 -> local writer machine when possible
replica 2 -> a different rack
replica 3 -> a different node on replica 2's rack
```

The implementation also computes `maxNodesPerRack` and states that, once the cluster has more than one rack and more than one replica, the adjustment is intended to avoid placing all replicas on the same rack.

This gives a useful release-evolution guardrail:

> **same two-rack diversity objective ≠ same per-replica target order across HDFS releases.**

The 0.18 architecture text and 2.7.3 implementation should therefore remain separately dated historical records.

### Directly inspected evidence — placement verification

`verifyBlockPlacement` counts distinct rack network locations. In a cluster that has been multi-rack it sets:

```text
minRacks = min(2, numberOfReplicas)
```

and compares the actual distinct-rack count against that minimum through `BlockPlacementStatusDefault`.

For the bounded default policy, this directly establishes:

> **replication factor 3 ≠ requirement for three unique racks.**

and:

> **placement-policy satisfaction ≠ maximal rack spread.**

### Directly inspected evidence — target and excess-replica selection use topology

`isGoodTarget` rejects a target when its rack already contains more chosen nodes than `maxTargetPerRack` permits.

The excess-replica path constructs rack-aware candidate classes, including replicas on racks containing more than one copy versus racks containing exactly one copy, before choosing deletions. This is enough for the bounded conclusion that excess-copy cleanup is topology-aware; this record does not claim a universal optimal deletion policy or reconstruct uninspected helper semantics beyond the displayed source path.

### Supports

- rack location is retained/derived control state used both to admit a placement and to constrain later excess-replica cleanup;
- copy count and copy topology are separate predicates;
- losing one physical replica can have different topology consequences depending on what racks the remaining replicas occupy.

---

## Source D — Hadoop 2.7.3 `DecommissionManager.java`

**Type:** exact release source; primary implementation evidence.

**Path:** `hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DecommissionManager.java`

**URL:** <https://github.com/apache/hadoop/blob/branch-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DecommissionManager.java>

### Directly inspected evidence

`isSufficientlyReplicated` first tests the conjunction:

```text
numLive >= numExpected
AND
blockManager.isPlacementPolicySatisfied(block)
```

before taking the ordinary full-strength success path.

The method then contains the already-recorded release-specific exceptions for under-construction and non-under-construction blocks. Those exceptions remain important: the new rack-placement evidence does not erase the existing finding that `sufficiently replicated` is not one timeless equation in HDFS 2.7.3.

### Supports

For the ordinary full-strength branch:

> **live-replica count ≠ placement-policy satisfaction.**

and therefore:

> **decommission safety/admissibility ≠ bare replica-count threshold.**

The block can have enough live replicas numerically and still fail the placement-policy part of the ordinary success predicate.

### Boundary

This statement is about the displayed 2.7.3 control path. It is not generalized to every exception, every HDFS release, erasure-coded HDFS, or later maintenance-state machinery.

---

## Historical record versus engineering reconstruction

### Historical record

The directly supported historical statements are:

1. GFS 2003 explicitly spread replicas across racks because machine-level replication alone did not cover entire-rack failure, while acknowledging extra cross-rack write cost.
2. Hadoop 0.18 documentation explicitly described rack-aware HDFS placement and distinguished all-unique-rack placement from its factor-three two-rack policy.
3. Hadoop 0.18's factor-three description and Hadoop 2.7.3's exact target ordering differ, even though both intentionally use more than one rack.
4. Hadoop 2.7.3 `verifyBlockPlacement` separately evaluates distinct rack count and, in its default multi-rack path, requires at least two racks for replication factors of two or more.
5. Hadoop 2.7.3 `DecommissionManager.isSufficientlyReplicated` uses both live-replica count and placement-policy satisfaction in its ordinary full-strength success branch.
6. Hadoop 2.7.3 target admission and excess-replica cleanup consult rack topology.

### Engineering reconstruction

The repository may therefore use these bounded engineering distinctions:

- **replica multiplicity ≠ failure-domain diversity**;
- **live-replica count ≠ placement-policy satisfaction**;
- **rack-diversity requirement ≠ one unique rack per replica**;
- **placement sufficiency ≠ maximal rack spread**;
- **decommission completion ≠ bare copy-count threshold**;
- **over-replica deletion ≠ arbitrary copy deletion**;
- **rack topology state ≠ payload**;
- **same two-rack objective ≠ unchanged placement algorithm across releases**.

These are project formulations, not quotations from Apache or Google.

---

## Functional comparisons — not genealogy

### Case 05 — RADOS / CRUSH

Both cases make retained service depend on where copies are placed, not merely how many copies exist. RADOS PG/OSD placement and HDFS rack-aware replication remain different mechanisms and histories.

### Cases 19 and 24 — f4 / Windows Azure LRC

Those coded-storage cases already separate coding algebra from failure-domain placement. Case 80 now supplies a replicated-storage counterpart:

> **copy count ≠ failure-domain placement**, just as **fragment count/reconstructability ≠ failure-domain placement**.

This is a functional relation comparison only.

### Case 83 — HDFS block scanner

Rack diversity says where acceptable replica embodiments are distributed. It does not prove those replicas have recently passed checksum verification:

> **placement qualification ≠ integrity qualification.**

### Cases 49–51 — HDFS recovery/authority

Rack placement does not by itself decide generation-stamp currentness, writer recovery authority, or which NameNode may issue block-changing commands. Topological diversity is one retention relation among several.

---

## Prior-art boundary

GFS 2003 is an earlier public distributed-filesystem witness for cross-rack replica placement than the bounded HDFS 0.18 record. That blocks an HDFS-first claim for the general mechanism.

It does **not** establish a demonstrated implementation genealogy:

> **GFS 2003 rack-spread prior art ≠ proven GFS→HDFS placement-code descent.**

A genuine genealogy would require direct design records, citations, code history, or author evidence tracing the HDFS implementation. That broader history belongs in `tmzncty/computing-archaeology` if pursued.

Searches of `tmzncty/computing-archaeology` for `HDFS rack replica placement` and `rack awareness` found no dedicated treatment to reuse in this round.

---

## Rejected or unsupported claims

| Claim | Status | Reason |
| --- | --- | --- |
| HDFS invented rack-aware replicated storage | rejected | GFS 2003 already supplies an earlier distributed-filesystem witness; no broader priority study |
| three replicas means three independent racks | rejected | bounded HDFS policies intentionally use two racks for the factor-three case |
| enough live replicas automatically means HDFS placement policy is satisfied | rejected | 2.7.3 ordinary full-strength decommission test evaluates both predicates |
| maximum rack spread is always the HDFS optimum | rejected | 0.18 explicitly describes all-unique-rack placement as simple but non-optimal because of write cost |
| HDFS 0.18 and 2.7.3 use the same factor-three target ordering | rejected | their inspected descriptions differ |
| rack-aware placement proves replica contents are checksum-valid/current | rejected | integrity/currentness are separate relations handled by other HDFS mechanisms/cases |
| decommission completion securely erases the retiring node | rejected | Case 80 remains an administrative/retention handoff case, not sanitization |
| GFS rack placement proves direct HDFS implementation genealogy | rejected | chronology/function alone are insufficient for descent |
| rack label proves every physical failure is independent across racks | unsupported | the bounded sources use rack topology as an operational failure-domain model, not a universal physical independence proof |

---

## Evidence status

**`grounded` deepening for Case 80.**

The new evidence closes a bounded relation left implicit in the original case: in ordinary full-strength Hadoop 2.7.3 decommission logic, preservation elsewhere is not measured only by how many live replicas remain; it is also qualified by the placement policy. The 0.18/2.7.3 comparison additionally prevents release mechanics from being silently merged, while GFS 2003 supplies an earlier prior-art floor without being converted into an unproven genealogy.
