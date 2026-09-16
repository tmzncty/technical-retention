# ZFS Dirty Time Log: Retained Failure Intervals and Selective Resilver

**Status:** `grounded`

## Scope

This case asks one bounded retention question:

> How can a storage system retain enough evidence about *when* one redundant device failed to receive state so that later repair can select only blocks exposed during that interval, rather than treating the whole device as equally suspect?

The historical core is bounded to the Sun ZFS dirty-time-log / resilver patent family with a **2005-11-04 priority floor** and **2007-05-10 publication witnesses**. Oracle Solaris operational documentation is used as a product-level witness that ZFS can resilver only the minimum necessary data after a short outage. OpenZFS 2.1.11 source is used only as a later implementation-continuity witness for DTL classes and persistence/derivation boundaries.

This case is not:

- a generic ZFS history;
- a second scrub case (Case 18 already covers proactive verification and checksum-qualified healing);
- a second RAID-Z write-hole case (Case 95);
- a second dRAID sequential-rebuild case (Case 96);
- proof that Sun/ZFS invented dirty logging or selective mirror recovery;
- proof that every ZFS release implements every patent-family embodiment exactly as written;
- a claim that a DTL proves stored payload is corrupt.

A repository search found no dedicated DTL/resilver case in `tmzncty/computing-archaeology`; broader dirty-log, mirror-recovery, and ZFS implementation genealogy belongs there rather than being duplicated here.

### Evidence deepening

- [`evidence/100-openzfs-211-dtl-persistence-reload-deepening.md`](../evidence/100-openzfs-211-dtl-persistence-reload-deepening.md) — source-level OpenZFS 2.1.11 deepening of the leaf `DTL_MISSING` persistence cycle: space-map serialization, config object reference, load-time reconstruction, derived aggregate DTL state, and the `CANT_OPEN` boundary when DTL metadata cannot be loaded.
- [`evidence/100-openzfs-211-dtl-retirement-excision-deepening.md`](../evidence/100-openzfs-211-dtl-retirement-excision-deepening.md) — source-level OpenZFS 2.1.11 deepening of DTL retirement: completion vs cancellation, per-leaf excision eligibility, txg-frontier-bounded removal, `DTL_SCRUB` exception preservation, and delayed reset of attach/rebuild markers until missing/outage debt is empty.
- [`evidence/100-sun-vxvm-cvm-1998-1999-drl-admissibility-fallback-prior-art-deepening.md`](../evidence/100-sun-vxvm-cvm-1998-1999-drl-admissibility-fallback-prior-art-deepening.md) — primary-manual deepening of the pre-ZFS DRL floor: July 1998 spatial dirty-region write-before-data logging and `resilvering` vocabulary, plus July 1999 CVM recovery/active-map handoff, invalid-log fallback to full recovery, and the boundary `same recovery word != same repair geometry or genealogy`.

## Historical vocabulary

Historical / source vocabulary retained here:

- `dirty region logging` / `DRL`;
- `dirty time log` / `DTL`;
- `birth time`;
- `transaction group`;
- `resilver` / `resilvering`;
- `pruned resilvering`;
- `minimum amount of necessary data`.

Project engineering vocabulary:

- **failure-exposure history** — retained evidence of intervals during which a redundant target had less than the required replication relation;
- **repair-scope witness** — metadata sufficient to decide that a block or subtree can be excluded from a later catch-up pass;
- **repair debt** — a still-retained obligation to restore redundancy after the device becomes available again.

The project terms are analytical reconstructions, not Sun/Oracle historical terminology.

## Historical record

### H/P — dirty-region logging already provided selective recovery before ZFS DTL

The earlier prior-art floor is now bounded more tightly by direct primary documentation. The **July 1998 Sun StorEdge Volume Manager 2.6 System Administrator's Guide** describes `Dirty Region Logging (DRL)` as dividing a mirrored volume into consecutive regions, retaining a status bit per region, synchronously writing a clean-to-dirty transition before the associated data write, and after restart recovering only regions marked dirty. The same manual states that without DRL after a system failure the mirrors may require full-content recovery.

The **July 14 1999 Sun Cluster 2.2 Cluster Volume Manager Guide** then adds cluster-specific retained state: one recovery map plus one active map per node. On startup active maps are incorporated into the recovery map; a crashed node is not allowed to rejoin until its active maps have been incorporated into all affected recovery maps. If imported DRL metadata is considered invalid or is too small for the cluster geometry, the documented fallback is full-volume recovery rather than trusting a selective scope.

That is an explicit pre-ZFS functional prior-art floor for **bounded recovery instead of full-copy recovery**, while also showing that selective recovery depends on an admissible repair-scope witness.

It does not make DRL and ZFS DTL identical. DRL is region-oriented and incurs logging work when regions transition dirty. The later ZFS DTL family instead exploits block birth time / transaction-group relations to record intervals of unsuccessful storage and decide whether specific blocks need resilvering.

The July 1998 manual also calls the mirror/database `resynchronization process` **"also known as resilvering"**. That establishes a pre-ZFS public documentation floor for the word, not first coinage and not a genealogy claim into ZFS. `Same word resilvering != same mechanism != proved historical descent`.

### H/P — the ZFS patent family has a 2005-11-04 priority floor

Sun's later patent-family records claim benefit of provisional application 60/734,023, filed **2005-11-04**, titled `Dirty Time Logging and Resilvering`, naming William H. Moore and Jeffrey S. Bonwick. Related applications published on **2007-05-10** include:

- `Method and system for dirty time logging` (`US20070106869A1`, later `US7925827B2`);
- `Method and system for dirty time log directed resilvering` (`US20070106867A1`, later `US7930495B2`);
- `Method and system for pruned resilvering using a dirty time log` (`US20070106677A1`, later `US8635190B2`);
- `Method and system for metadata-based resilvering` (`US20070106866A1`, later `US8938594B2`).

This is a date-bounded documentary floor, not an invention-priority claim and not by itself proof of the first shipping implementation.

### H/P — DTL records failed-replication time / transaction-group state

The patent-family description associates a DTL with storage devices and says it tracks times during which I/O requests were not successfully completed on a device. It explicitly allows transaction-group numbers to stand for those times, and explains `birth time` as either time or transaction-group number in the described embodiments.

The important historical relation is therefore not simply `block is dirty` but:

```text
block birth txg
    compared with
interval(s) in which one target did not receive required writes
```

### H/P — birth time plus DTL can bound block-level repair

The dirty-time-logging application describes updating the DTL with a block's birth time when a storage attempt is unsuccessful. The directed/pruned resilver family then uses those birth times to decide which blocks require resilvering.

The pruned-resilver application states that a child block is resilvered when its birth time is in the DTL and that a branch need not be traversed when parent/descendant birth-time ordering makes intersection with the DTL impossible. Its worked example uses DTL birth times / transaction groups 32–37 for an offline disk and treats blocks outside that interval as not requiring resilvering under the described conditions.

Thus retained time/txg metadata can reduce future traversal as well as future write work.

### H/P — product documentation exposes the selective-repair outcome

Oracle's Solaris ZFS administration documentation states that ZFS resilvers only the minimum amount of necessary data. It contrasts a short outage, where catch-up can finish quickly, with full device replacement, where work is proportional to used data.

This operational documentation is useful because the patent family alone would only establish a described design. It still does not prove a universal performance ratio, exact internal algorithm for every release, or that every short outage produces little work.

### H/P — later OpenZFS source retains DTL as replication-history state

OpenZFS 2.1.11 `module/zfs/vdev.c` describes a vdev DTL as the set of transaction groups for which the vdev has `less than perfect replication`. It distinguishes `DTL_MISSING`, `DTL_PARTIAL`, `DTL_SCRUB`, and on-demand `DTL_OUTAGE`.

The same source says that leaf `DTL_MISSING` maps are sufficient to derive the aggregate DTL/outage state and therefore are what the implementation keeps on disk; other DTL forms are regenerated after pool load/configuration changes.

The implementation path is now grounded more narrowly in the linked evidence packet: `vdev_dtl_sync()` writes the leaf missing ranges into a DTL space map, vdev configuration carries the space-map object id as `ZPOOL_CONFIG_DTL`, load-time construction restores that id as `vdev_dtl_object`, and `vdev_dtl_load()` rebuilds the runtime leaf range tree from the retained object.

A second source-level deepening now grounds the opposite end of that lifecycle. OpenZFS 2.1.11 does not retire `DTL_MISSING` merely because a maintenance activity ended: `vdev_dtl_reassess()` first qualifies completion/error state and leaf coverage, subtracts only the eligible prefix below the maintenance txg frontier, overlays `DTL_SCRUB` exceptions back into the resulting missing map, and resets attach/rebuild markers only after missing/outage debt becomes empty.

This is **later source-level continuity only**. It must not be projected backward as proof that every 2005–2007 Solaris/ZFS implementation had precisely these four classes, the same object format, or identical persistence and retirement rules.

## Retained state

In the bounded DTL-directed repair model, later selective catch-up requires at least:

1. payload / metadata blocks that remain valid on surviving redundant members;
2. block pointers carrying birth-time / transaction-group information in the described ZFS tree;
3. retained DTL interval information identifying when a target did not receive required state;
4. current vdev/topology information identifying which redundancy relation must be restored;
5. traversal/recovery logic that compares block birth state with the retained DTL;
6. enough surviving redundancy to source the missing contribution.

For the OpenZFS 2.1.11 persistence/retirement slices, one more decomposition matters:

```text
leaf in-memory DTL_MISSING
    != DTL space-map object
    != vdev configuration reference to that object
    != reconstructed runtime DTL_MISSING
    != DTL_SCRUB unrepaired-scan exception state
    != derived parent / aggregate DTL views
    != scan / rebuild completion and txg frontier
    != actual resilver I/O
    != attach/rebuild marker state
```

The DTL is not user payload. It is also not a complete write history. It is a compressed witness to a **repair-relevant interval**.

The earlier DRL packet adds a separate pre-ZFS decomposition that must not be back-projected into DTL: mirrored payload/plex state, per-region dirty bits, per-node active maps, a consolidated recovery map, cluster membership/crash state, volatile coordination of recovery-map updates, and actual resynchronization I/O are distinct states with different persistence horizons.

## Retention mechanism

### A failure event can end while its repair obligation remains

A device may return online, but blocks born while it was unavailable can still be missing there. If the system forgot the relevant exposure interval immediately when the device returned, it would lose information useful for bounded repair.

Engineering reconstruction:

```text
device unavailable during txg interval
    ->
retain interval / missing-replication evidence
    ->
device returns
    ->
compare block birth txgs with retained interval
    ->
repair only potentially affected blocks
    ->
retire repair evidence when the required relation is restored
```

Therefore:

> **failure over ≠ repair debt over.**

The 1999 CVM DRL documentation supplies an earlier functional counterexample to any assumption that a node's failure event and the repair-scope state created by that event end together: a crashed node's active map must be incorporated into the continuing recovery map before the node may rejoin and resume I/O that can overwrite the active map.

### DTL is failure-exposure history, not mutation history

A DTL does not need to enumerate every application write, file operation, or historical block value. It preserves the subset of temporal information needed to decide whether a block could have missed required replication on a particular target.

Thus:

> **repair-scope history ≠ complete mutation history.**

The same broad distinction already appears in the earlier DRL manuals: a dirty bit conservatively identifies a region that may require recovery; it is not an ordered record of every write performed in that region.

### Time/txg selection is different from a dirty-region bitmap

DRL marks spatial regions that need recovery. The described DTL method can instead log transaction-group/birth-time intervals and ask each block whether its birth belongs to those intervals.

Both can reduce full-copy work, but their retained evidence has different geometry:

```text
DRL: spatial region -> dirty/clean recovery status
DTL: transaction-time interval + block birth -> possible repair membership
```

No direct genealogy beyond documented chronology/function is asserted.

## Addressing and access geometry

DTL-directed resilver combines two coordinate systems:

- **tree/location reachability** — block pointers identify and reach current blocks;
- **transaction-time membership** — birth time / txg is compared with DTL intervals.

Pruned resilver can avoid descending a subtree when its birth-time relation shows that no descendant could fall into the relevant dirty interval under the described tree ordering.

So future repair work is shaped not only by where blocks are but by **when their current embodiments entered the tree**.

## Read and verification semantics

A DTL entry does not say that a surviving source block has failed a checksum. It says that the required replication relation was incomplete during specified transaction groups / conditions.

Case 18 remains the checksum/scrub comparison. In modern OpenZFS source, `DTL_SCRUB` also shows that scrub outcome and replication-missing state can interact, but this does not collapse them into one state.

Therefore:

> **repair membership ≠ corruption diagnosis.**

The earlier DRL fallback reinforces this separation from another direction: a DRL can be considered invalid or structurally inadequate and cause full-volume recovery without the manual thereby asserting that every payload region is corrupt.

## Repair semantics

### Short-outage catch-up is not full-device replacement

Oracle documentation distinguishes short-outage resilvering from replacement. A returned device may need only the state it missed; a replacement has no trusted prior contents and therefore presents a much larger repair scope, bounded by allocated/used state and implementation details.

### DTL-directed resilver is not dRAID sequential reconstruction

Case 96's dRAID reconstruction uses fixed-width redundancy geometry and device/space-map order to restore redundancy quickly across distributed spare capacity. Case 100 instead focuses on **temporal pruning of repair scope** using DTL/birth relations.

One can optimize *which blocks need repair* and *how repair I/O is laid out* independently.

### DTL-directed resilver is not RAID-Z write-hole avoidance

Case 95 addresses how a new coded block is committed without leaving a fixed partial-stripe update as the standing authoritative state. Case 100 starts after a redundancy gap exists and asks how much state must later be repaired.

## Persistence and derivation boundary

The OpenZFS 2.1.11 source gives a useful later counterexample to the assumption that every useful maintenance classification must itself be independently durable. Leaf `DTL_MISSING` state is retained on disk, while aggregate/other DTL state can be derived after load or topology change.

The exact source-level persistence cycle is:

```text
leaf DTL_MISSING range tree
    -> vdev_dtl_sync()
DTL space-map object
    -> vdev_config_generate()
ZPOOL_CONFIG_DTL object reference
    -> load-time vdev construction
vdev_dtl_object
    -> vdev_dtl_load()
reconstructed leaf DTL_MISSING
    -> DTL derivation
parent / aggregate DTL and outage views
```

Engineering reconstruction:

> **retention infrastructure can preserve a minimal sufficient basis and regenerate higher-level maintenance state.**

and:

> **repair-debt persistence ≠ repair execution persistence.**

The first relation is implementation-specific. The second prevents a category error: reloading a non-empty DTL means the system has recovered evidence that repair is still owed; it does not mean the resilver itself survived as completed work.

### Qualified retirement is the inverse lifecycle, not an unconditional clear

The linked retirement deepening shows that OpenZFS 2.1.11 also distinguishes maintenance completion from authority to forget repair history. A canceled/restarting scan does not pass the same retirement frontier as a completed scan. For eligible leaves, `vdev_dtl_should_excise()` relates the leaf's missing history to the relevant resilver/rebuild txg coverage; deferred or insufficiently covered leaves are not treated as though the pass discharged their debt.

When excision is allowed, `vdev_dtl_reassess()` subtracts only the prefix `[0, scrub_txg)` and folds `DTL_SCRUB` exceptions into the new `DTL_MISSING` map. After this reassessment, transient `DTL_SCRUB` state can be cleared because still-unrepaired intervals remain represented by `DTL_MISSING`. Attach/rebuild markers are reset only when both missing and outage maps are empty, and the configuration is dirtied to persist that reset.

Engineering reconstruction:

```text
maintenance completed
    != repair debt retired

covered + qualified old debt
    -> may be excised

scan-discovered unrepaired exception
    -> remains represented

missing/outage debt empty
    -> attach/rebuild marker may be retired
```

This is **qualified repair-debt retirement**, a project term rather than OpenZFS historical vocabulary.

## Failure boundaries

### Losing DTL / repair-scope evidence

If repair-relevant interval state is unavailable or invalid, selective catch-up may no longer be justified even if payload remains on surviving members. OpenZFS 2.1.11 provides a sharper source-level boundary than a generic “fallback to more work” story: when a leaf `vdev_dtl_load()` fails during `vdev_load()`, the implementation marks the vdev `VDEV_STATE_CANT_OPEN` with `VDEV_AUX_CORRUPT_DATA` and returns the error.

That establishes an admission dependency for this implementation:

```text
payload may remain physically present
    !=
required DTL metadata is readable and admissible
```

It does **not** establish that DTL metadata failure proves user payload corruption, nor that every other ZFS version has the same failure policy.

> **payload survival ≠ preservation of the evidence needed for efficient and admissible repair.**

### Earlier DRL shows that repair-witness failure policy is not universal

The 1999 Sun Cluster 2.2 CVM manual documents a different response to unusable repair-scope metadata. Imported DRLs that are considered invalid, or logs that are too small for the current cluster node geometry, can cause **full-volume recovery**. In that lineage, loss of trusted selectivity broadens work rather than proving the payload corrupt or necessarily blocking the volume outright.

The bounded contrast is:

```text
Sun Cluster 2.2 CVM, 1999:
invalid / undersized DRL
    -> full-volume recovery

OpenZFS 2.1.11 inspected load path:
required leaf DTL load failure
    -> CANT_OPEN + CORRUPT_DATA auxiliary state
```

This is a functional comparison only. It establishes `repair-control metadata unavailable != one universal fallback policy`; it does not identify DRL and DTL or assert a direct implementation lineage.

### DTL presence mistaken for corruption

A transaction group can be in a missing/partial replication interval without proving that every corresponding source block is corrupt. The DTL bounds where a replica may be incomplete; checksum/integrity evidence answers another question.

### DTL absence mistaken for universal integrity

Conversely, absence from this repair log is not a proof against latent media corruption, controller bugs, or every other failure class. Scrub/checksum verification remains a separate relation.

### Completion mistaken for retirement authority

A maintenance activity reaching a completion path is not by itself authority to erase all DTL evidence. OpenZFS 2.1.11 separately checks leaf eligibility/coverage and preserves `DTL_SCRUB` exceptions when reconstructing `DTL_MISSING`.

Thus:

> **scan/rebuild completion ≠ unconditional repair-debt clearance.**

### Patent embodiment mistaken for release guarantee

The patent family establishes described methods and chronology. Oracle operational docs establish user-visible selective-resilver behavior. Neither source alone licenses projection of every algorithmic detail onto every Solaris/OpenZFS release.

## Prior art and genealogy boundary

### Dirty-region logging is an explicit earlier functional floor

The July 1998 Sun StorEdge Volume Manager 2.6 manual directly documents spatial DRL, synchronous recording of a newly dirty region before the corresponding data write, restart recovery limited to dirty regions, and the full-recovery counterfactual when DRL is absent. The July 1999 Sun Cluster 2.2 guide adds recovery/active-map structure and invalid-log conservative fallback. The 2007 DTL patent description itself also discusses conventional DRL as an existing recovery scheme.

Therefore this case explicitly rejects:

> `ZFS DTL invented selective mirror resynchronization`.

The 1998 manual also establishes that `resilvering` was already public mirror/database recovery vocabulary before the ZFS patent/publication window. That rejects using the mere presence of the word as evidence that the mechanism originated with ZFS.

### Difference retained instead of erased

The prior art matters precisely because the mechanisms are not identical. DRL pays for a spatial dirty map around writes; the ZFS DTL family exploits temporal/transaction-group exposure plus block birth metadata already carried in the tree.

Chronology, shared vocabulary, and functional resemblance do not establish direct descent, and this case makes no universal `first` claim for either technique or term.

## Cross-case comparison

### Case 18 — ZFS scrub

- Case 18: proactively read/verify current storage and use checksum-qualified redundancy for healing.
- Case 100: retain exposure history so a later resilver can avoid treating unaffected state as repair work, while the later source deepening shows that scrub-discovered unrepaired intervals can remain as DTL debt even after the traversal itself completes.

`verification scope ≠ catch-up scope`, and `scan completion ≠ repaired-everything evidence`.

### Case 48 — Cassandra incremental repair state

Both cases retain maintenance history that can reduce future repair work. Cassandra retains repaired/unrepaired classification over SSTable populations; ZFS DTL retains txg exposure intervals for a redundancy target. The later Case 100 deepening adds a sharper functional boundary shared at a high level with Cassandra session cleanup: **workflow completion/age is not by itself control-state retirement authority**. Cassandra checks whether SSTables still reference a session; OpenZFS checks repair coverage/status and preserves DTL exceptions. This is a functional comparison only, not genealogy.

### Case 85 — NAND read-retry parameter state

Case 85 shows that payload and recovery-control metadata can be distinct retention objects. Case 100 shows the same broad functional separation at a distributed-storage layer: payload blocks can survive while separate repair-scope metadata is needed to reconstruct the system's maintenance obligation. `shared separation ≠ shared representation or genealogy`.

### Case 95 — RAID-Z write-hole avoidance

Write-hole avoidance governs admissible update construction. DTL governs later repair after incomplete replication. `update consistency ≠ recovery-scope selection`.

### Case 96 — dRAID

DTL/pruned resilver reduces the **set** of blocks that require catch-up. dRAID sequential reconstruction changes **reconstruction geometry/bandwidth** and restores coded redundancy before later checksum scrub. The 2.1.11 retirement deepening also prevents `sequential rebuild complete = checksum-qualified integrity`: `vdev_rebuild.c` explicitly treats the checksum-verification scrub as a later phase. `less work selected ≠ same work scheduled faster`, and `redundancy restored ≠ later verification complete`.

### Case 116 — HDFS maintenance state

Case 116 separates persistence of administrative maintenance intent from correctness of the runtime sufficiency predicate. Case 100 adds a different persistence boundary: a repair obligation can survive restart even though the actual repair action has not completed. This is a functional comparison only.

## Functional analogy

A bounded analogy is a maintenance exception journal: instead of remembering all successful events, the system retains only intervals where a required relation was not satisfied and later uses that summary to focus repair.

The retirement deepening extends the analogy cautiously: an exception record may be forgotten only after the system has evidence that its represented obligation has been discharged, while surviving exceptions are carried forward into the next authoritative repair-debt representation.

The earlier DRL packet adds a negative control to that analogy: if the exception summary is no longer admissible, a system may have to abandon selectivity and perform broader recovery rather than infer that no exception exists.

The analogy is functional. It must not replace the historical terms `DRL`, `DTL`, `birth time`, `transaction group`, and `resilver`.

## Philosophical / media-theoretical interpretation

`I` — Case 100 shows that technical retention can preserve not only a payload or an old version but a **debt toward a relation**: the system remembers that one embodiment missed part of the current state and therefore still requires repair.

`I` — It also shows a form of selective forgetting. Complete write history can disappear while a small temporal summary survives because that summary is sufficient for a future maintenance decision.

`I` — The pre-ZFS DRL evidence sharpens the inverse case: when a repair-scope witness loses admissibility, the system can deliberately give up fine-grained selectivity and widen recovery rather than pretend to remember a precision it can no longer justify.

`I` — The OpenZFS persistence slice adds a second selective layer: even some higher-level maintenance views may disappear as volatile state while a smaller durable basis survives and later regenerates them.

`I` — The retirement slice makes forgetting conditional in the opposite direction: a covered portion of repair history can be excised once it no longer constrains future repair, while scan-discovered unrepaired exceptions survive because they still have operational force.

`I` — The past matters operationally only to the degree that it can still constrain present repair. Once redundancy is restored and the relevant evidence can safely be retired, the system need not become a permanent archive of the outage.

These are project interpretations, not claims that Sun/Veritas/Oracle/OpenZFS authors formulated a philosophy of memory.

## Counterexamples and limits

This case does not establish:

- that DTL is the first dirty-log technique;
- that DRL and DTL are the same mechanism;
- that July 1998 is the invention or first-deployment date for DRL;
- that July 1998 is the first use or coinage of `resilvering`;
- that the shared word `resilvering` proves a direct VxVM/CVM → ZFS genealogy;
- that invalid DRL metadata proves mirrored payload corruption;
- that every system reacts to invalid repair-scope metadata by full recovery;
- that the 2005 provisional date equals first deployment;
- that every patent claim shipped unchanged;
- that DTL membership proves checksum failure or user-visible corruption;
- that selective resilver is always fast;
- that every short outage has a small repair set;
- that pruned tree traversal and modern dRAID sequential rebuild are interchangeable;
- that modern OpenZFS DTL class/persistence/retirement semantics can be backdated unchanged to 2005;
- that every aggregate/runtime DTL view is independently stored on disk;
- that a successfully reloaded DTL means repair execution completed across the restart;
- that DTL-load corruption proves payload corruption;
- that a completed scan or rebuild automatically clears every DTL interval;
- that an empty DTL proves absence of latent corruption;
- that resetting an attach/rebuild marker securely erases payload or every historical trace;
- that OpenZFS 2.1.11's DTL error and retirement paths are universal across all ZFS versions;
- that clearing repair-state metadata securely erases payload.

## Related repositories

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — searches for `DTL`, `resilver`, `VxVM`, and `Dirty Region Logging` found no dedicated case in this slice. Broad dirty-log, mirror-recovery, VxVM/CVM/ZFS source-history, and controller genealogy should live there if developed.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — useful for a future question about when `dirty`, `resync`, `resilver`, and transaction-time repair became actors' own problem vocabulary.

## Claim ledger

| Claim | Label | Evidence | Limit |
| --- | --- | --- | --- |
| July 1998 Sun StorEdge Volume Manager 2.6 documents DRL as a per-region dirty bitmap used after restart to limit mirror recovery | `H/P` | Sun StorEdge Volume Manager 2.6 System Administrator's Guide §1.1.8 | documentation floor; not invention/first deployment |
| a clean-to-dirty DRL transition is synchronously recorded before the associated data write | `H/P` | July 1998 manual §1.1.8 | bounded product documentation |
| July 1998 documentation calls mirror/database resynchronization `also known as resilvering` | `H/P` | July 1998 manual §1.1.9 | vocabulary floor; not first coinage or ZFS genealogy |
| Sun Cluster 2.2 CVM has one recovery map plus per-node active maps, merges crashed-node state before rejoin, and can use full recovery when DRL metadata is invalid/undersized | `H/P` | Sun Cluster 2.2 Cluster Volume Manager Guide §§2.1.4.1–2.1.4.3 | 1999 product/version-specific semantics |
| Sun DTL/resilver family claims 2005-11-04 provisional priority | `H/P` | US patent family | documentary chronology, not first deployment |
| DTL can store failed-write/offline time as transaction-group / birth-time evidence | `H/P` | US7925827 / related family description | bounded to described embodiments |
| pruned resilver can use parent/child birth-time relations to skip unaffected tree branches | `H/P` | US8635190 / US20070106677 | patent/design witness; not universal release guarantee |
| ZFS product docs say short-outage repair can resilver only minimum necessary data | `H/P` | Oracle Solaris ZFS Administration Guide | qualitative product behavior; no universal performance factor |
| later OpenZFS source defines DTL as txgs with less-than-perfect replication | `H/P` | OpenZFS 2.1.11 `vdev.c` | later continuity only |
| later OpenZFS persists leaf `DTL_MISSING` in a DTL space map and carries its object id in vdev configuration | `P` | OpenZFS 2.1.11 `vdev.c`, `vdev_label.c`; Evidence 100 persistence deepening | implementation/version-specific |
| later OpenZFS reloads leaf `DTL_MISSING` and derives other DTL state from that sufficient basis | `P/E` | OpenZFS 2.1.11 `vdev.c`; Evidence 100 persistence deepening | implementation/version-specific |
| OpenZFS 2.1.11 DTL-load failure can make a leaf vdev `CANT_OPEN` with `VDEV_AUX_CORRUPT_DATA` | `P` | OpenZFS 2.1.11 `vdev.c`; Evidence 100 persistence deepening | does not prove payload corruption or universal policy |
| OpenZFS 2.1.11 distinguishes completed vs incomplete scan input to DTL reassessment | `P` | `dsl_scan.c`; Evidence 100 retirement deepening | implementation/version-specific |
| DTL excision is qualified by per-leaf state/coverage rather than generic completion alone | `P` | `vdev_dtl_should_excise()`, `vdev_dtl_reassess()` | exact predicates are version-specific |
| eligible retirement subtracts only the covered prefix and preserves `DTL_SCRUB` exceptions in the regenerated missing map | `P` | OpenZFS 2.1.11 `vdev.c`; Evidence 100 retirement deepening | does not prove all errors are detected |
| attach/rebuild marker reset waits for empty missing/outage debt and dirties config | `P` | OpenZFS 2.1.11 `vdev.c` | not equivalent to erasing all history |
| invalid repair-scope metadata proves payload corruption | `X` | 1999 CVM invalid-log fallback | rejected |
| all systems react to repair-scope metadata loss with the same admission/fallback policy | `X` | CVM vs OpenZFS 2.1.11 comparison | rejected |
| DTL is a complete write-history archive | `X` | mechanism/source comparison | rejected |
| DTL membership proves payload corruption | `X` | mechanism/source comparison | rejected |
| surviving DTL repair debt proves repair execution survived/completed | `X` | persistence lifecycle | rejected |
| maintenance completion automatically authorizes forgetting all repair debt | `X` | excision predicates + `DTL_SCRUB` overlay | rejected |
| ZFS invented selective mirror recovery | `X` | earlier DRL + patent's own prior-art discussion | rejected |
| DRL chronology or shared `resilvering` vocabulary proves direct genealogy into DTL | `X` | none | unsupported |

## Sources

- Sun StorEdge Volume Manager 2.6 System Administrator's Guide, Revision A, July 1998: <https://imap.filibeto.org/sun/lib/nonsun/veritas/vxvm/sevm-2.6/805-5706-10.pdf>
- Sun Cluster 2.2, `Dirty Region Logging and CVM`: <https://docs.oracle.com/cd/E19957-01/806-2329/ch2admin-39382/index.html>
- Sun Cluster 2.2 Cluster Volume Manager Guide facsimile, July 14 1999: <https://docs.oracle.com/cd/E19957-01/806-2329/806-2329.pdf>
- Sun/Oracle patent family overview, `Method and system for metadata-based resilvering`: <https://patents.google.com/patent/US8938594B2/en>
- `Method and system for dirty time logging`: <https://patents.google.com/patent/US7925827B2/en>
- `Method and system for dirty time log directed resilvering`: <https://patents.google.com/patent/US7930495B2/en>
- `Method and system for pruned resilvering using a dirty time log`: <https://patents.google.com/patent/US8635190B2/en>
- Oracle Solaris ZFS resilvering status: <https://docs.oracle.com/cd/E26505_01/html/E37384/gbbba.html>
- OpenZFS 2.1.11 `module/zfs/vdev.c`: <https://github.com/openzfs/zfs/blob/zfs-2.1.11/module/zfs/vdev.c>
- OpenZFS 2.1.11 `module/zfs/vdev_label.c`: <https://github.com/openzfs/zfs/blob/zfs-2.1.11/module/zfs/vdev_label.c>
- OpenZFS 2.1.11 `module/zfs/dsl_scan.c`: <https://github.com/openzfs/zfs/blob/zfs-2.1.11/module/zfs/dsl_scan.c>
- OpenZFS 2.1.11 `module/zfs/vdev_rebuild.c`: <https://github.com/openzfs/zfs/blob/zfs-2.1.11/module/zfs/vdev_rebuild.c>
- OpenZFS 2.1.11 source as packaged by Debian, `module/zfs/vdev.c`: <https://sources.debian.org/src/zfs-linux/2.1.11-1%2Bdeb12u1/module/zfs/vdev.c>
- Repository DRL prior-art deepening: [`evidence/100-sun-vxvm-cvm-1998-1999-drl-admissibility-fallback-prior-art-deepening.md`](../evidence/100-sun-vxvm-cvm-1998-1999-drl-admissibility-fallback-prior-art-deepening.md)
- Repository persistence deepening: [`evidence/100-openzfs-211-dtl-persistence-reload-deepening.md`](../evidence/100-openzfs-211-dtl-persistence-reload-deepening.md)
- Repository retirement deepening: [`evidence/100-openzfs-211-dtl-retirement-excision-deepening.md`](../evidence/100-openzfs-211-dtl-retirement-excision-deepening.md)

## Remaining work

The 1998–1999 DRL product-document prior-art slice, the OpenZFS 2.1.11 persistence cycle, and the OpenZFS 2.1.11 retirement predicate are now bounded. Remaining evidence debt is narrower:

- trace earlier Veritas/Sun Volume Manager documentation if a future slice needs the DRL or `resilvering` vocabulary floor before July 1998; do not infer first coinage from the current floor;
- identify the exact historical commit/release where the current-style DTL space-map persistence/load path entered the ZFS lineage;
- identify the commit/release where the current-style excision predicates and `DTL_SCRUB` overlay entered the lineage, and compare Solaris/illumos/OpenZFS revisions without projecting current semantics backward;
- add a controlled export/import or reboot trace with a non-empty leaf DTL before and after reload;
- add a fault-injection trace for an unreadable/corrupt DTL object and record actual import/open behavior;
- run interrupted/erroring resilver experiments to verify that uncovered or unrepaired ranges remain represented across restart;
- trace sequential rebuild → later checksum scrub on a real pool and keep redundancy restoration distinct from integrity revalidation.