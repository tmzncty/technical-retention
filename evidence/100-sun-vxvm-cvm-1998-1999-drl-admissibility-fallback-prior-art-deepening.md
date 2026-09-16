# Evidence 100 — Sun/Veritas DRL Prior Art: Spatial Repair Witness, Cluster Aggregation, and Conservative Fallback (1998–1999)

**Status:** `bounded deepening complete`

**Canonical case:** [Case 100 — ZFS Dirty Time Log: Retained Failure Intervals and Selective Resilver](../cases/100-zfs-dirty-time-log-selective-resilver.md)

## Scope

This packet deepens one narrow prior-art boundary around Case 100:

> Before ZFS Dirty Time Logging, what did Sun/Veritas documentation already say about retaining bounded mirror-recovery scope, making that scope usable after failure, and falling back when the repair-scope witness was no longer admissible?

The answer is bounded to two manufacturer manuals:

1. **Sun StorEdge Volume Manager 2.6 System Administrator's Guide**, Part No. 805-5706-10, Revision A, **July 1998**;
2. **Sun Cluster 2.2 Cluster Volume Manager Guide**, Part No. 806-2329, **July 14 1999**.

The 1998 manual directly documents ordinary Dirty Region Logging (DRL) as a persistent spatial bitmap used to avoid full mirror recovery after a crash. It also uses the term `resilvering` for mirror/database resynchronization. The 1999 cluster manual adds a more revealing lifecycle: one recovery map plus per-node active maps, merge-before-rejoin rules, compatibility/size checks, and conservative full-volume recovery when the DRL is invalid or structurally inadequate.

This packet is **not**:

- a general history of Veritas Volume Manager, Sun StorEdge Volume Manager, SSVM, or CVM;
- proof that DRL was invented in 1998;
- proof that `resilvering` was coined by Sun or Veritas in 1998;
- a genealogy claim from VxVM/CVM DRL to ZFS DTL;
- a claim that spatial DRL and temporal/birth-time DTL are the same mechanism;
- a claim that invalid DRL metadata proves payload corruption;
- a claim that every later volume manager uses the same fallback policy.

A repository search of `tmzncty/computing-archaeology` for `DTL`, `resilver`, `VxVM`, and `Dirty Region Logging` found no dedicated technical-history slice to reuse. Broader VxVM/CVM genealogy belongs there if developed later; this packet keeps only the retention-specific repair-witness boundary.

## Source classification and inspection status

### 1998 Sun StorEdge Volume Manager 2.6 System Administrator's Guide

Primary manufacturer manual:

<https://imap.filibeto.org/sun/lib/nonsun/veritas/vxvm/sevm-2.6/805-5706-10.pdf>

Directly inspected facsimile pages:

- printed p. **1-29** / PDF page 41 — §1.1.8 `Dirty Region Logging`;
- printed p. **1-30** / PDF page 42 — §1.1.9 `VxSmartSync Recovery Accelerator`.

The cover identifies:

- title: *Sun StorEdge Volume Manager 2.6 System Administrator's Guide*;
- Part No. 805-5706-10;
- Revision A;
- July 1998.

This is a strong primary documentation witness for the documented product/interface behavior. It is not proof of first shipment, first implementation, or invention priority.

### 1999 Sun Cluster 2.2 Cluster Volume Manager Guide

Primary manufacturer manual:

<https://docs.oracle.com/cd/E19957-01/806-2329/806-2329.pdf>

HTML transcription of the same section:

<https://docs.oracle.com/cd/E19957-01/806-2329/ch2admin-39382/index.html>

Directly inspected facsimile pages:

- printed p. **2-9** / PDF page 33 — DRL log format, compatibility, and invalid-log fallback;
- printed p. **2-10** / PDF page 34 — cluster recovery, active-map incorporation, rejoin gate, and volatile coordination.

The manual footer identifies **July 14 1999**.

This is a strong primary documentation witness for the Sun Cluster 2.2 CVM behavior described there. It is not evidence that every VxVM/CVM version has identical map formats or cluster admission rules.

---

## Historical record

### H/P — by July 1998 DRL explicitly retained a spatial recovery witness

The July 1998 Sun StorEdge Volume Manager 2.6 manual describes DRL as an optional property for speeding recovery of mirrored volumes after system failure.

Its mechanism is explicit:

- the mirrored volume is divided into consecutive logical regions;
- a dirty region log contains a status bit for each region;
- before data is written to a region, that region is marked dirty in the log;
- when a region transitions from clean to dirty, the log is synchronously written to disk before the data write can proceed;
- after restart, only regions marked dirty need mirror recovery.

The manual also states the negative case: if DRL is not used and a system failure occurs, the mirrors are restored to consistency by copying the full contents of the volume between mirrors, including areas that may already be consistent.

So the documented relation is already:

```text
write exposure
    -> durable spatial dirty witness
    -> crash
    -> selective recovery of marked regions

no usable DRL witness
    -> broader/full mirror recovery
```

This is strong pre-ZFS evidence that **repair scope itself can be retained state**.

### H/P — DRL ordering makes the recovery witness precede the potentially exposed data write

The same 1998 manual does not describe the dirty bitmap as a post-failure reconstruction guessed from payload contents. A clean-to-dirty transition is synchronously recorded before the corresponding data write is allowed to occur.

That ordering matters:

```text
mark region dirty durably
    before
allowing the data write
```

The DRL is therefore part of the crash-recovery protocol, not merely an after-the-fact performance hint.

This packet does not infer a modern WAL identity from that fact. `write-ahead` is a useful engineering description of ordering; the historical source's own term is Dirty Region Logging.

### H/P — the 1998 manual already uses `resilvering` outside ZFS

The immediately following VxSmartSync section describes the mirror `resynchronization process` as **also known as `resilvering`** for volumes used with Oracle databases.

The same section explains that database-maintained logs can tell the system which portions require recovery and can therefore remove the need for VxVM DRL on database data volumes. Recovery scope may thus be supplied by a different retained history source.

This establishes a conservative vocabulary floor:

> `resilvering` was public Sun/Veritas product documentation vocabulary by July 1998.

It does **not** establish:

- first coinage;
- a stable meaning across every product lineage;
- direct vocabulary transmission into ZFS;
- identity between VxSmartSync mirror/database recovery and later ZFS resilver algorithms.

Therefore:

```text
same historical word
    !=
same retained-state geometry
    !=
same implementation
    !=
proved genealogy
```

### H/P — ordinary DRL can retain a coarser summary than the underlying write history

The 1998 manual states that dirty bits are not necessarily cleared immediately after a write. A region can remain marked dirty until it becomes least recently used; another write to a region already marked dirty need not synchronously rewrite the log before that write.

Thus the DRL is not a complete mutation log. It retains a conservative recovery classification:

```text
region marked dirty
    = may require recovery after crash

not
    = exact ordered list of writes to that region
```

This is an important prior-art boundary for Case 100 because later ZFS DTL is likewise repair-oriented summary state rather than complete application history, although the two summaries have different geometry and update semantics.

### H/P — by July 1999 CVM split DRL state into a recovery map and per-node active maps

The Sun Cluster 2.2 CVM guide distinguishes the single-system and cluster formats:

- SSVM DRL: one recovery map + one active map;
- CVM DRL: one recovery map + multiple active maps, one per cluster node.

The log must be large enough for all per-node active maps plus the recovery map.

This gives a historically documented decomposition:

```text
per-node active recovery-scope state
    !=
consolidated recovery map
```

The maps are not user payload. They are control metadata that records enough spatial exposure state for later mirror recovery.

### H/P — cluster startup incorporates active maps into the recovery map

The 1999 guide states that on initial cluster startup all active maps are incorporated into the recovery map during volume start.

A crashed node is not allowed to rejoin until its DRL active maps have been incorporated into the recovery maps of all affected volumes. Recovery utilities compare the crashed node's active maps with the recovery map and update it before the node resumes I/O, because renewed I/O will overwrite the active map.

Meanwhile other nodes can continue I/O.

The important retention relation is:

```text
node crashes
    -> its active map still matters
    -> active-map information is merged into the recovery map
    -> only then may that node resume I/O that can overwrite its active map
```

The crash event itself is over, but the repair-relevant state produced before/during that event cannot yet be discarded.

### H/P — CVM retains durable recovery maps while also using volatile coordination state

The same 1999 section says the CVM kernel tracks crashed nodes and recovery-state changes to prevent I/O collisions. The master performs **volatile tracking** of DRL recovery-map updates and prevents multiple recovery utilities from changing a recovery map simultaneously.

Therefore the documented system contains at least two persistence horizons:

```text
DRL maps on log subdisk
    !=
volatile master coordination for map updates
```

The existence of persistent repair-scope metadata does not imply that every control variable participating in recovery is itself persistent.

### H/P — invalid or undersized DRL metadata triggers conservative full-volume recovery

The 1999 CVM guide is unusually explicit about the failure boundary.

It states that when disk groups move between SSVM and CVM, imported dirty region logs can be considered invalid. In one direction, SSVM treats CVM logs as invalid and conducts a **full volume recovery**. It also states that when an SSVM DRL is too small for the number of CVM nodes, CVM marks the log invalid and performs full recovery. Moving a DRL volume from a two-node cluster to a four-node cluster can similarly make the log too small, again causing full-volume recovery until an adequately sized log is allocated.

Thus in this documented lineage:

```text
payload/mirrors may still exist
    +
repair-scope witness is invalid or structurally inadequate
    ->
do not trust the selective scope
    ->
widen recovery to the full volume
```

That is stronger than saying DRL merely improves performance. The validity of the repair witness controls whether selective recovery is admissible.

---

## Engineering reconstruction

### E — selective repair needs an admissible repair-scope witness, not merely surviving payload

The 1998–1999 documentation supports a simple reconstruction:

```text
surviving mirrored payload
    !=
knowledge of which regions may have diverged
```

When a valid DRL exists, the system can use a bounded dirty-region set. When that witness is unavailable, invalid, or too small for the current cluster geometry, the documented safe response is to expand repair scope.

This yields:

> **payload survival ≠ selective-repair authority.**

### E — losing selectivity can be safer than pretending the scope is still known

The CVM compatibility rules show a conservative design choice:

```text
valid scope witness
    -> selective recovery allowed

invalid scope witness
    -> selective claim withdrawn
    -> full recovery
```

The system does not reinterpret invalid metadata as evidence that nothing needs repair.

Thus:

> **repair-scope witness invalid ≠ repair debt absent.**

and:

> **unknown repair scope can widen work without proving payload corruption.**

### E — repair-witness failure policy is implementation-specific

This packet produces a useful bounded contrast inside Case 100.

For Sun Cluster 2.2 CVM in 1999:

```text
invalid / undersized DRL
    -> conservative full-volume recovery
```

For the separately grounded OpenZFS 2.1.11 source path:

```text
leaf DTL load failure during vdev_load()
    -> VDEV_STATE_CANT_OPEN
    + VDEV_AUX_CORRUPT_DATA
```

The common high-level problem is loss of a repair-control witness, but the system response is not universal.

Therefore:

> **repair-control metadata is important ≠ every implementation degrades the same way when it is unavailable.**

One implementation can broaden repair scope; another can reject normal admission in the inspected path.

This is a functional comparison, not genealogy and not an equivalence between DRL and DTL.

### E — active-map incorporation is a control-state handoff before overwrite/reuse

The CVM rejoin rule can be reconstructed as a handoff problem:

```text
per-node active map
    -> contains still-relevant recovery exposure
    -> merge into recovery map
    -> recovery map becomes the continuing witness
    -> active map may then be overwritten by resumed I/O
```

That gives another bounded project distinction:

> **old representation may be reusable only after its repair-relevant relation has migrated to another representation.**

This should not be paraphrased as payload migration; only repair-control state is being discussed.

### E — spatial and temporal repair witnesses are different geometries

DRL asks roughly:

```text
which logical regions were exposed to writes around the failure interval?
```

The later ZFS DTL family asks roughly:

```text
which transaction-group intervals were under-replicated,
and which current blocks have birth times intersecting those intervals?
```

Both can reduce later repair, but their retained evidence is different:

```text
DRL
    spatial region -> conservative dirty/clean recovery status

DTL
    failure txg/time interval + block birth -> repair membership test
```

This packet therefore strengthens the prior-art floor while simultaneously sharpening the novelty boundary of the ZFS DTL mechanism.

---

## Retained-state decomposition

For the 1998–1999 DRL slice, do not collapse:

```text
user/database payload
    !=
mirror/plex membership and current data copies
    !=
per-region dirty status
    !=
dirty region log on log subdisk
    !=
per-node active map
    !=
consolidated recovery map
    !=
cluster/node dirty-membership state
    !=
volatile master coordination of recovery-map updates
    !=
actual mirror resynchronization I/O
    !=
post-recovery clean/admissible state
```

The retention object studied here is mainly **repair-scope control metadata**.

---

## Failure and admissibility boundaries

### Invalid DRL does not prove data corruption

The 1999 manual says invalid/inadequate logs can cause full recovery. That is an operational consequence of not trusting the bounded recovery witness.

It does not establish:

```text
DRL invalid
    -> payload definitely corrupt
```

The safe reading is:

```text
DRL invalid
    -> selective scope no longer trusted
    -> broader recovery required
```

### Full recovery does not mean the system has forgotten the volume

The volume identity, mirror relation, and payload embodiments can remain available even when the fine-grained repair-scope witness is unusable.

So:

> **loss of repair precision ≠ loss of logical object identity.**

### Per-node active map must not be overwritten before incorporation

The rejoin rule demonstrates an explicit overwrite hazard for maintenance metadata. Resumed I/O can overwrite the active map, so the relevant information must first be incorporated into the continuing recovery map.

Thus:

> **metadata embodiment reuse ≠ debt retirement.**

The representation can be reused only after the information that still constrains recovery has been handed forward.

### Volatile coordination loss is not identical to durable DRL loss

The manual explicitly calls the master's tracking of concurrent recovery-map updates volatile. This should not be silently upgraded into persistent history or treated as the same retained object as the on-disk DRL maps.

---

## Functional comparisons

### Case 100 later ZFS DTL

Shared high-level function:

- retain exceptional under-replication/write-exposure evidence;
- use that evidence to avoid unnecessary later repair;
- do not require a complete mutation history.

Different mechanism:

- DRL: spatial dirty-region bitmap and cluster active/recovery maps;
- DTL: txg/time intervals combined with block birth information.

Different inspected failure policy:

- Sun Cluster 2.2 CVM: invalid/undersized DRL can force full-volume recovery;
- OpenZFS 2.1.11: failure to load required leaf DTL metadata can make the vdev `CANT_OPEN` on the inspected path.

No direct genealogy is asserted.

### Case 48 Cassandra incremental repair state

A bounded functional resemblance exists: both systems retain a control classification whose validity determines how narrowly later repair can proceed.

But Cassandra's repaired/unrepaired SSTable/session relations and VxVM's dirty-region bitmap are different representations, time scales, and repair semantics.

`shared maintenance-control role != shared implementation or history`.

---

## Philosophical / media-theoretical interpretation

`I` — These manuals provide a particularly concrete form of selective technical memory. The system does not need to retain every write that occurred before a crash; it retains a conservative witness sufficient to constrain future repair.

`I` — They also show a disciplined form of forgetting. Fine-grained selectivity is usable only while the witness that justifies it remains admissible. When the witness becomes invalid, the system does not pretend to remember more precisely than it can justify; it broadens recovery.

`I` — The cluster active-map handoff adds another point: a past node's activity can remain operationally binding after that node has crashed. The representation carrying that obligation may change before the obligation itself is discharged.

These are project interpretations. They are not claims that Sun or Veritas engineers formulated a philosophy of memory, forgetting, or debt.

---

## Explicit non-claims

This packet does **not** establish:

1. that Dirty Region Logging was invented by Sun or Veritas in 1998;
2. that July 1998 is the first public description of DRL;
3. that July 1998 is the first product shipment using DRL;
4. that the word `resilvering` first appeared in July 1998;
5. that ZFS borrowed the word `resilvering` directly from this manual;
6. that VxVM/CVM DRL and ZFS DTL are the same mechanism;
7. that spatial DRL is an earlier implementation of birth-time/txg DTL;
8. that chronology proves a direct engineering lineage from VxVM/CVM into ZFS;
9. that every dirty-region bit corresponds to one application write;
10. that DRL is a complete write history;
11. that a dirty bit proves the region is corrupt;
12. that a clean bit proves absence of every latent media defect;
13. that an invalid DRL proves user payload corruption;
14. that an invalid DRL means repair can be skipped;
15. that full-volume recovery necessarily rewrites every byte under every release and configuration beyond what the cited manuals describe;
16. that CVM per-node active maps are user payload or database logs;
17. that the volatile master coordination state is persisted in the DRL;
18. that successful active-map incorporation means mirror resynchronization itself is complete;
19. that the 1999 CVM map layout is universal across all VxVM/CVM versions;
20. that OpenZFS 2.1.11 must use the same fallback policy as 1999 CVM;
21. that a shared functional pattern establishes shared source code, organization, or genealogy;
22. that invalidation or replacement of repair-control metadata securely erases historical traces or payload.

---

## Claim ledger

| Claim | Label | Evidence | Limit |
| --- | --- | --- | --- |
| July 1998 Sun StorEdge Volume Manager 2.6 documents DRL as a per-region dirty bitmap used after restart to limit mirror recovery | `H/P` | 1998 manual §1.1.8, printed p. 1-29 | documentation floor, not invention/ship-date claim |
| a clean-to-dirty DRL transition is synchronously logged before the corresponding data write | `H/P` | 1998 manual §1.1.8 | bounded to documented behavior |
| without DRL after system failure, the manual describes full-content mirror recovery | `H/P` | 1998 manual §1.1.8 | product/manual semantics, not universal volume-manager rule |
| July 1998 documentation calls resynchronization `also known as resilvering` | `H/P` | 1998 manual §1.1.9, printed p. 1-30 | vocabulary floor, not first coinage or ZFS genealogy |
| database-maintained logs can supply recovery-scope knowledge instead of VxVM DRL for VxSmartSync data volumes | `H/P` | 1998 manual §1.1.9.1 | bounded to described database integration |
| 1999 CVM DRL has one recovery map plus one active map per node | `H/P` | Sun Cluster 2.2 CVM Guide §2.1.4.1, printed p. 2-9 | version/product-specific layout |
| imported/inadequately sized DRLs can be marked invalid and trigger full-volume recovery | `H/P` | 1999 guide §2.1.4.2, pp. 2-9–2-10 | does not prove payload corruption |
| active maps are incorporated into recovery maps at startup, and a crashed node must complete this incorporation before rejoin/resumed I/O | `H/P` | 1999 guide §2.1.4.3, p. 2-10 | cluster recovery-control rule |
| master tracks concurrent recovery-map updates volatilely | `H/P` | 1999 guide §2.1.4.3 | volatile coordination is not the on-disk DRL itself |
| surviving payload is insufficient by itself to justify selective recovery | `E` | valid-vs-invalid DRL behavior | engineering reconstruction |
| invalid repair-scope metadata may conservatively widen repair work without proving payload corruption | `E` | CVM fallback behavior | bounded to this policy pattern |
| CVM invalid-DRL full recovery and OpenZFS 2.1.11 DTL-load admission failure are the same implementation | `X` | cross-version/source comparison | rejected |
| identical use of `resilvering` proves direct historical continuity into ZFS | `X` | chronology alone | rejected |

---

## Source ledger

### Sun Microsystems, *Sun StorEdge Volume Manager 2.6 System Administrator's Guide*

Part No. 805-5706-10, Revision A, July 1998.

Facsimile:

<https://imap.filibeto.org/sun/lib/nonsun/veritas/vxvm/sevm-2.6/805-5706-10.pdf>

Relevant anchors:

- cover — title, part number, revision, July 1998;
- §1.1.8 `Dirty Region Logging`, printed p. 1-29 — spatial dirty bitmap, synchronous dirty transition before data write, restart recovery scope, full-recovery counterfactual;
- §1.1.9 `VxSmartSync Recovery Accelerator`, printed p. 1-30 — `resynchronization process (also known as resilvering)`;
- §1.1.9.1 — database-maintained logs as an alternative recovery-scope source for data volumes.

### Sun Microsystems, *Sun Cluster 2.2 Cluster Volume Manager Guide*

Part No. 806-2329, July 14 1999.

Facsimile:

<https://docs.oracle.com/cd/E19957-01/806-2329/806-2329.pdf>

HTML section:

<https://docs.oracle.com/cd/E19957-01/806-2329/ch2admin-39382/index.html>

Relevant anchors:

- §2.1.4 `Dirty Region Logging and CVM`;
- §2.1.4.1 `Log Format and Size`, printed p. 2-9 — recovery map + per-node active maps;
- §2.1.4.2 `Compatibility`, pp. 2-9–2-10 — invalid/undersized log -> full recovery;
- §2.1.4.3 `Recovery With DRL`, printed p. 2-10 — active-map incorporation, rejoin gate, continued I/O on other nodes, volatile master tracking.

### Repository-local comparison witnesses

- [Case 100 canonical](../cases/100-zfs-dirty-time-log-selective-resilver.md);
- [OpenZFS 2.1.11 DTL persistence/reload deepening](100-openzfs-211-dtl-persistence-reload-deepening.md);
- [OpenZFS 2.1.11 DTL retirement/excision deepening](100-openzfs-211-dtl-retirement-excision-deepening.md).

---

## What this changes in Case 100

Before this packet, Case 100 already used Sun Cluster 2.2 DRL as an earlier functional prior-art floor for selective mirror recovery. This deepening makes that floor much more precise:

1. **July 1998 primary documentation** directly grounds the spatial dirty-region bitmap and write-before-data ordering;
2. the same manual shows `resilvering` was already public storage-recovery vocabulary before ZFS;
3. **July 1999 cluster documentation** separates per-node active maps from the consolidated recovery map;
4. cluster recovery demonstrates a handoff in which active-map information must be incorporated before the old representation can be overwritten by resumed I/O;
5. invalid or undersized DRL metadata does not authorize narrow recovery — it causes conservative full-volume recovery;
6. this creates a strong bounded counterexample to any universal claim that loss of repair-control metadata must always make a storage object unopenable: OpenZFS 2.1.11's inspected DTL-load path and 1999 CVM choose different failure policies.

The resulting project relations are:

```text
repair-scope witness
    != payload

repair-scope witness valid
    != repair complete

repair-scope witness invalid
    != repair debt absent
    != payload proved corrupt

same word `resilvering`
    != same mechanism
    != proved genealogy

repair-control metadata unavailable
    != one universal fallback policy
```

---

## Remaining evidence debt

This packet closes the bounded **1998–1999 product-document behavior and terminology** slice. It leaves distinct questions open:

- earlier Veritas Volume Manager releases/manuals that may push the DRL documentation floor before July 1998;
- the earliest surviving technical use and provenance of the word `resilvering`;
- source-code or engineering-design evidence for the exact SSVM/CVM DRL on-disk representation;
- whether and when later VxVM/CVM releases changed invalid-log fallback or active/recovery-map semantics;
- controlled reconstruction of a DRL failure/invalidation and recovery trace;
- organizational/personnel/documentary evidence, if any, that could establish or reject a direct genealogy between earlier VxVM/CVM recovery vocabulary/mechanisms and later ZFS DTL/resilver work.

Those belong to future bounded slices. Chronology and functional resemblance alone are not sufficient to answer them.