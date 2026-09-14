# Evidence 100 — OpenZFS 2.1.11 DTL Persistence, Reload, and Admission Boundary

**Status:** `bounded deepening complete`

**Canonical case:** [Case 100 — ZFS Dirty Time Log: Retained Failure Intervals and Selective Resilver](../cases/100-zfs-dirty-time-log-selective-resilver.md)

## Scope

This evidence packet asks one narrow implementation question:

> In OpenZFS 2.1.11, what exactly survives a pool/process restart so that dirty-time-log repair debt can be reconstructed, and what happens if that retained DTL state cannot be loaded?

The answer is source-level and version-bounded. In OpenZFS 2.1.11:

1. a leaf vdev's `DTL_MISSING` range tree is serialized into a DTL space-map object;
2. the DTL space-map object identifier is included in generated vdev configuration;
3. load-time vdev construction reads `ZPOOL_CONFIG_DTL` into `vdev_dtl_object`;
4. `vdev_dtl_load()` opens that object and reconstructs the in-memory leaf `DTL_MISSING` range tree;
5. the implementation explicitly says the leaf `DTL_MISSING` maps are the sufficient on-disk basis from which the other DTLs and outage maps are regenerated;
6. if the leaf DTL cannot be loaded during `vdev_load()`, the vdev is set to `VDEV_STATE_CANT_OPEN` with `VDEV_AUX_CORRUPT_DATA`.

This packet does **not** attempt to establish the earliest historical introduction of this exact object format or load path. The canonical case already carries the 2005–2007 Sun DTL/resilver documentary floor. Here, OpenZFS 2.1.11 is an implementation witness for a later, inspectable persistence lifecycle.

## Source classification

Primary implementation witnesses:

- **[implementation-primary]** OpenZFS 2.1.11 `module/zfs/vdev.c`;
- **[implementation-primary]** OpenZFS 2.1.11 `module/zfs/vdev_label.c`.

These are source-code records of one released implementation lineage. They are not proof that every Solaris or OpenZFS release used the same persistence layout.

A repository search of `tmzncty/computing-archaeology` for `DTL`, `resilver`, and related terms found no dedicated existing DTL/resilver history packet to reuse. Broader ZFS source genealogy still belongs there if developed later.

## Implementation record

### P — the implementation says only the leaf `DTL_MISSING` basis needs to be kept on disk

OpenZFS 2.1.11 explains the DTL relation in `module/zfs/vdev.c`. After deriving parent DTL/outage state from child state, its source comment states that knowing the leaf vdevs' `DTL_MISSING` maps is sufficient to compute the DTLs and outage maps for all vdevs. It then states that this leaf basis is what is kept on disk, while the other DTLs are regenerated when loading the pool or after a configuration change.

The bounded relation is therefore:

```text
leaf DTL_MISSING maps
    = durable sufficient basis in this implementation

other / aggregate DTL and outage views
    = regenerated state
```

This is stronger and more precise than saying generically that “the DTL is persisted.” Not every useful maintenance view is independently serialized.

### P — `vdev_dtl_sync()` serializes leaf missing-range state into a space map

`vdev_dtl_sync(vdev_t *vd, uint64_t txg)` is leaf-specific. It takes the leaf `vd->vdev_dtl[DTL_MISSING]` range tree and writes a synchronized copy through the DTL space map.

The function:

- allocates a DTL space-map object when one does not yet exist;
- opens that space map;
- snapshots the in-memory `DTL_MISSING` range tree into a temporary range tree;
- truncates the space map for rewrite;
- calls `space_map_write(..., SM_ALLOC, ...)` with the retained missing ranges;
- dirties the top-level vdev configuration when the DTL space-map object identity changes.

Thus the implementation does not merely preserve a boolean “needs resilver” flag. It persists a range representation of missing transaction-group state.

### P — the vdev configuration carries the DTL space-map object identity

In OpenZFS 2.1.11 `module/zfs/vdev_label.c`, `vdev_config_generate()` includes:

```text
ZPOOL_CONFIG_DTL -> space_map_object(vd->vdev_dtl_sm)
```

when the DTL space map exists.

On the load path in `module/zfs/vdev.c`, vdev allocation for `VDEV_ALLOC_LOAD` reads `ZPOOL_CONFIG_DTL` into `vd->vdev_dtl_object`.

The important persistence relation is therefore not only:

```text
DTL ranges -> space-map object
```

but also:

```text
vdev configuration -> identifier of the DTL space-map object
```

The two layers play different roles. The space map carries the missing-range representation; the configuration carries the reference by which the load path can locate it.

### P — `vdev_dtl_load()` reconstructs runtime `DTL_MISSING` from the retained object

For a leaf vdev whose `vdev_dtl_object` is nonzero, `vdev_dtl_load()`:

1. opens the referenced space map in the pool meta-object set;
2. creates a temporary range tree;
3. loads the space map with `space_map_load(..., SM_ALLOC)`;
4. walks the loaded tree into `vd->vdev_dtl[DTL_MISSING]` under the DTL lock.

This gives an explicit restart/reload boundary:

```text
on-disk DTL space-map object
    -> load
runtime leaf DTL_MISSING range tree
```

The runtime maintenance state is reconstructed from durable repair metadata rather than assumed to survive in memory.

### P — inability to load the DTL is an admission failure, not merely a lost optimization

`vdev_load()` explicitly invokes `vdev_dtl_load()` for leaf vdevs. If that call returns an error, the implementation sets the vdev state to:

```text
VDEV_STATE_CANT_OPEN
VDEV_AUX_CORRUPT_DATA
```

and returns the error.

This is a significant negative control. In this implementation, the DTL persistence structure is not treated as a disposable performance hint whose loss simply forces an automatic full scan. A DTL-load failure participates in whether the vdev can be admitted on the normal load path.

That does **not** prove that user payload on the vdev is corrupt. It proves that corruption/failure in this required metadata path is itself enough for the implementation to reject normal opening of that vdev.

## Engineering reconstruction

The source supports the following bounded lifecycle reconstruction:

```text
replication gap / missed txgs
    ->
leaf DTL_MISSING range tree records repair debt
    ->
vdev_dtl_sync()
    ->
DTL ranges serialized into a space-map object
    ->
vdev configuration retains the DTL object identity
    ->
process/pool unload and later load
    ->
ZPOOL_CONFIG_DTL becomes vdev_dtl_object
    ->
vdev_dtl_load()
    ->
runtime leaf DTL_MISSING reconstructed
    ->
aggregate / other DTL views regenerated from leaf basis
    ->
selective resilver logic can again consult retained repair debt
```

This yields two distinctions useful to the project:

> **repair-debt persistence ≠ repair execution persistence.**

and:

> **durable maintenance basis ≠ durable maintenance view.**

The first says that surviving knowledge that work is owed does not mean the repair itself continued or completed across the restart. The second says that the system can durably preserve a sufficient lower-level basis while reconstructing higher-level maintenance classifications on demand.

## Retained-state decomposition

For this OpenZFS 2.1.11 slice, the following objects should not be collapsed:

```text
user / filesystem payload
    !=
block birth / txg information used by repair selection
    !=
leaf in-memory DTL_MISSING range tree
    !=
DTL space-map object
    !=
vdev configuration reference to that object
    !=
reconstructed runtime leaf DTL_MISSING
    !=
derived parent / aggregate DTLs and outage maps
    !=
actual resilver I/O
    !=
post-repair state in which the repair debt may be retired
```

The central retention object in this deepening is **repair-control metadata**, not application payload.

## Failure boundary

### Payload survival does not imply repair-metadata continuity

The source-level error path demonstrates that a system may still have storage media containing payload while failing to reconstruct a maintenance relation needed by the implementation.

The safe statement is:

```text
payload may remain physically present
    !=
DTL metadata is readable and admissible
```

No claim is made here about what percentage of payload remains valid in any such real-world failure.

### DTL metadata corruption does not prove payload corruption

`VDEV_AUX_CORRUPT_DATA` is the implementation's auxiliary state on the DTL-load error path. It must not be paraphrased as evidence that every user block is corrupt.

The code establishes an **admission dependency**:

```text
required repair metadata cannot be loaded
    ->
normal vdev load can fail
```

It does not establish:

```text
required repair metadata cannot be loaded
    ->
all payload is damaged
```

### Missing runtime aggregate state is not necessarily lost history

Because the implementation explicitly regenerates other DTLs from leaf `DTL_MISSING`, absence of a separately persisted parent/aggregate DTL is not itself a retention failure.

This is a useful counterexample to a simplistic rule that every runtime maintenance structure must have its own durable copy.

## Functional comparison

### Case 85 — NAND read-retry parameter state

Case 85 shows that user payload and the control/calibration state needed to recover that payload can be distinct retention objects. Case 100 shows a different layer of the same broad functional pattern: payload blocks and the maintenance metadata needed to bound future redundancy repair can also be distinct.

The analogy is functional only. NAND retry calibration and ZFS DTL space maps share neither representation nor genealogy.

### Case 116 — HDFS maintenance state

Case 116 separates persistence of maintenance intent from correctness of the predicate used to act on it. Case 100 adds another distinction:

```text
maintenance obligation survives restart
    !=
maintenance action has completed
```

Again, this is not a shared implementation claim.

## Philosophical / media-theoretical limit

`I` — This implementation makes “unfinished repair” into a retainable technical object. What survives is not the failed event itself and not a complete history of writes, but enough structured evidence for the system to reconstitute an obligation after volatile execution state disappears.

`I` — It also demonstrates selective durability: a lower-level basis can be persisted while derived classifications are allowed to vanish and be recomputed. Technical memory therefore need not preserve every representation through which a system temporarily understands the same obligation.

These are project interpretations. OpenZFS source authors are not being attributed a philosophy of memory.

## Explicit non-claims

This evidence packet does **not** establish:

1. that OpenZFS 2.1.11 is the first ZFS release to persist DTL state this way;
2. that the exact 2.1.11 DTL space-map representation existed unchanged in 2005 or 2007;
3. that every Solaris, illumos, or OpenZFS release has identical DTL load/sync semantics;
4. that a DTL space-map object is a complete write-ahead log;
5. that a DTL records every affected block individually;
6. that `ZPOOL_CONFIG_DTL` by itself contains the DTL ranges;
7. that all parent/aggregate DTL views are independently durable;
8. that successful DTL reload means resilver work has already occurred;
9. that a DTL-load error proves user payload corruption;
10. that loss of DTL metadata is automatically and safely recoverable by a full resilver in this exact error path;
11. that every in-memory DTL field survives a process restart;
12. that DTL persistence proves the underlying media will retain the object indefinitely;
13. that an object identifier is meaningful without the referenced MOS object and surrounding pool metadata;
14. that this source inspection proves production prevalence or field reliability;
15. that source chronology alone establishes invention priority.

## Claim ledger

| Claim | Label | Evidence | Limit |
| --- | --- | --- | --- |
| leaf `DTL_MISSING` is the sufficient on-disk basis from which other DTLs/outage maps are generated | `P` | OpenZFS 2.1.11 `vdev.c` source comment | version-specific implementation statement |
| `vdev_dtl_sync()` writes leaf `DTL_MISSING` ranges to a DTL space-map object | `P` | OpenZFS 2.1.11 `vdev.c` | implementation witness, not earliest provenance |
| generated vdev config carries the DTL space-map object id | `P` | OpenZFS 2.1.11 `vdev_label.c` | object reference, not the range contents themselves |
| load-time vdev construction reads `ZPOOL_CONFIG_DTL` into `vdev_dtl_object` | `P` | OpenZFS 2.1.11 `vdev.c` | bounded to load path |
| `vdev_dtl_load()` reconstructs runtime `DTL_MISSING` from the space map | `P` | OpenZFS 2.1.11 `vdev.c` | leaf/nonzero-object path |
| DTL-load failure can set the vdev `CANT_OPEN` with `VDEV_AUX_CORRUPT_DATA` | `P` | OpenZFS 2.1.11 `vdev.c` | does not prove payload corruption |
| durable repair basis can be smaller than the set of runtime maintenance views | `E` | persistence + derivation source relation | engineering reconstruction |
| surviving repair debt means repair execution survived/completed | `X` | source lifecycle distinction | rejected |
| DTL corruption proves all user blocks corrupt | `X` | source semantics | rejected |

## Source ledger

### OpenZFS 2.1.11 `module/zfs/vdev.c`

Stable source:

<https://github.com/openzfs/zfs/blob/zfs-2.1.11/module/zfs/vdev.c>

Relevant source regions/functions:

- DTL explanatory comment immediately before the DTL manipulation routines — states that leaf `DTL_MISSING` is sufficient and is what is kept on disk;
- load-time vdev allocation — reads `ZPOOL_CONFIG_DTL` into `vdev_dtl_object` for `VDEV_ALLOC_LOAD`;
- `vdev_dtl_load()` — opens/loads the DTL space map and rebuilds runtime `DTL_MISSING`;
- `vdev_dtl_sync()` — allocates/updates the DTL space-map object and writes the leaf missing ranges;
- `vdev_load()` — turns `vdev_dtl_load()` failure into `VDEV_STATE_CANT_OPEN` / `VDEV_AUX_CORRUPT_DATA`.

### OpenZFS 2.1.11 `module/zfs/vdev_label.c`

Stable source:

<https://github.com/openzfs/zfs/blob/zfs-2.1.11/module/zfs/vdev_label.c>

Relevant function:

- `vdev_config_generate()` — emits `ZPOOL_CONFIG_DTL` with the DTL space-map object id when the DTL space map exists.

## Remaining evidence debt

This packet closes the narrow source-level question of **how a leaf DTL repair basis survives load/reload in OpenZFS 2.1.11**. It leaves several distinct questions open:

- the exact historical commit/release where this space-map persistence form first entered the ZFS lineage;
- illumos/Solaris/OpenZFS cross-version genealogy of DTL object format and load semantics;
- a controlled fault-injection test that corrupts or withholds the DTL object and records real import/open behavior;
- a restart trace showing a non-empty DTL before export/reboot and the reconstructed DTL/resilver scope after import;
- the precise conditions under which DTL state is retired after successful repair across versions;
- whether later source revisions add recovery/fallback paths that alter the 2.1.11 admission boundary.

Those are appropriate follow-on slices; they are not inferred here.