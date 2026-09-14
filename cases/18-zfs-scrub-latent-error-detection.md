# ZFS Data Scrubbing: Proactive Integrity Verification Before Demand

## Status

**`grounded`** for the bounded mechanism.

Historical grounding: [`../evidence/18-zfs-scrub-2004-2010-grounding.md`](../evidence/18-zfs-scrub-2004-2010-grounding.md).

Later implementation deepening: [`../evidence/18-openzfs-2017-2026-scrub-progress-completion-durability-deepening.md`](../evidence/18-openzfs-2017-2026-scrub-progress-completion-durability-deepening.md) — persistent pause/progress state, restart from the last on-disk checkpoint, and the 2026 `zpool wait` fix separating `DSS_FINISHED` from final-txg sync.

## Scope

- **Bounded mechanism:** pool-wide integrity scrubbing in ZFS, with checksums and redundant-copy repair, contrasted with device-replacement resilvering.
- **Bounded period:** 2004–2010. The 2004 MASCOTS paper supplies a pre-ZFS-invention-priority boundary for `disk scrubbing`; the Sun/OpenSolaris-era ZFS administration semantics are taken from the Solaris ZFS Administration Guide as archived by Oracle.
- **Primary/system witness:** _Solaris ZFS Administration Guide_, especially `Checksums and Self-Healing Data`, `Controlling ZFS Data Scrubbing`, and `Viewing Resilvering Status`.
- **Prior-art witness:** Thomas Schwarz, Qin Xin, Ethan L. Miller, Darrell D. E. Long, Andy Hospodor, and Spencer Ng, **“Disk Scrubbing in Large Archival Storage Systems,”** MASCOTS 2004, pp. 409–418.
- **Independent empirical context:** Lakshmi N. Bairavasundaram, Garth R. Goodson, Shankar Pasupathy, and Jiri Schindler, **“An Analysis of Latent Sector Errors in Disk Drives,”** SIGMETRICS 2007.
- **Later implementation witness:** OpenZFS 2017 pause/resume, OpenZFS 2.1-era checkpoint/resume semantics, and the 2026 scan-completion wait fix. These are explicitly later deepening evidence and are not back-projected into the 2004–2010 record.
- **Research question:** what changes when a retained block can remain physically present yet defective or unverified until it is read, and how does proactive scrubbing differ from failure-triggered reconstruction/rebuild?

This is **not** a general history of ZFS, checksums, RAID-Z, end-to-end data integrity, latent-sector-error statistics, or OpenZFS scan architecture. It also does not claim that ZFS invented disk scrubbing.

The bounded comparison is narrower:

> **Retention can fail first as an undetected integrity defect. A scrub advances the moment of verification before ordinary demand, and—when a trustworthy redundant copy exists—can couple detection to repair before a later failure consumes the remaining repair path. Later OpenZFS evidence additionally shows that the progress and completion of this maintenance operation have their own retained-state boundary.**

---

## Historical vocabulary

### Schwarz et al., 2004

The paper explicitly uses:

- `disk scrubbing`;
- `periodically accessed`;
- `detect drive failure`;
- `block failures`;
- `rebuilding the affected blocks`;
- `opportunistic scrubbing`.

### Solaris ZFS Administration Guide

The ZFS documentation explicitly uses:

- `scrubbing`;
- `zpool scrub`;
- `checksummed`;
- `self-healing data`;
- `bad data block`;
- `redundant copy`;
- `repairs the bad data`;
- `resilvering`;
- `DEGRADED`;
- `checksum` / `CKSUM` errors in status output.

### Later OpenZFS implementation vocabulary

The bounded deepening uses OpenZFS's own later terms including `paused`, `checkpointed to disk`, `persistent on-disk scrub state`, `DSS_SCANNING`, `DSS_FINISHED`, `dsl_scan_phys_t`, `DMU_POOL_SCAN`, `txg`, `spa_sync()`, and `zpool wait`.

The following are **project engineering terms**, not historical ZFS vocabulary claims:

- `verification latency`;
- `verification age`;
- `latent-integrity window`;
- `repair-opportunity margin`;
- `proactive verification work`;
- `durable maintenance frontier`;
- `completion-durability boundary`.

---

## Historical record

### H/P — disk scrubbing is prior art before the bounded ZFS documentation

Schwarz et al. published `Disk Scrubbing in Large Archival Storage Systems` in October 2004. Their abstract defines a process in which drives are periodically accessed to detect failures; scrubbing all stored data can reveal block failures and allow affected blocks to be rebuilt from redundancy. They also distinguish scheduled scrubbing from `opportunistic` scrubbing performed while disks are already powered for other reasons.

This establishes a strict historical boundary:

> ZFS is a useful system-specific case for scrub semantics, checksum verification, and self-healing, but it is **not** evidence that Sun invented the general idea of periodically scanning storage to expose latent failures.

**Anchor:** Storage Systems Research Center publication record and abstract for Schwarz et al., MASCOTS 2004.

### H/P — ZFS treats checksums and repair as filesystem-layer integrity relations

The Solaris ZFS Administration Guide states that **all data and metadata is checksummed**. It further states that ZFS stores checksums in a manner intended to detect failure modes such as a complete block being written to the wrong location, and that checksum verification/data recovery are performed at the filesystem layer.

The same section defines `self-healing data`: when ZFS detects a bad block and redundancy is available, it obtains correct data from another redundant copy and repairs the damaged block.

The retained object is therefore not adequately described as `some bytes still exist on disk`. ZFS's own service semantics require a relation among:

- block contents;
- checksum evidence;
- the expected block identity/location relation;
- and, for transparent repair, another trustworthy redundant embodiment.

**Primary anchor:** _Solaris ZFS Administration Guide_, `Checksums and Self-Healing Data`.

### H/P — scrub moves integrity checking before ordinary demand

The ZFS guide states that errors may be encountered either **through scrubbing** or **when accessing a file on demand**. Explicit `zpool scrub` traverses all data in the pool once and verifies that all blocks can be read. It runs below ordinary I/O priority so the pool remains usable while the scan proceeds.

The crucial distinction is temporal:

```text
on-demand discovery:
    ordinary request reaches a damaged block
        -> defect becomes visible

scrub discovery:
    maintenance scan reaches the block first
        -> defect can become visible before an application needs it
```

The source does not claim that every possible silent corruption is detectable by every scrub. The bounded historical claim is that ZFS deliberately provides a whole-pool verification operation whose trigger is **not an application read of each object**.

**Primary anchor:** _Solaris ZFS Administration Guide_, `Controlling ZFS Data Scrubbing`.

### H/P — scrub is maintenance work with an explicit performance/energy cost

The same guide says scrub proceeds as fast as devices allow but at lower priority than normal I/O, may negatively affect performance, and in most cases should continue to completion. It also notes that routine scrubbing keeps disks doing I/O and can prevent power management from placing otherwise idle drives into low-power mode.

So proactive integrity work is not free background magic. It consumes:

- read bandwidth;
- device activity time;
- power;
- scheduling priority;
- operator/automation policy for when to run it.

This is a direct system-level retention cost.

### H/P — resilvering is related to scrubbing but has a different trigger and completion condition

The guide defines `resilvering` as the process of moving data from good copies to a replacement device. It emphasizes that ZFS can copy only the necessary used data, that the process is interruptible/resumable, and that a pool can remain `ONLINE` or `DEGRADED` while resilvering proceeds because the desired redundancy level has not yet been restored.

The scrubbing section says only one scrub/resilver class operation can run in a pool at a time; a device replacement can suspend an in-progress scrub until resilvering completes.

This is enough to keep two maintenance relations separate:

- **scrub:** proactively traverse current data to expose integrity/readability problems;
- **resilver:** reconstruct/copy required current data onto a device whose contents are known to need restoration because of replacement/out-of-date state.

Modern OpenZFS documentation states this contrast even more explicitly, but this case does not need later vocabulary to establish the bounded historical distinction.

### H/S — latent sector errors supply an independent empirical reason detection time matters

Bairavasundaram et al. (SIGMETRICS 2007) define latent sector errors as sector faults that go undetected until the corresponding sectors are accessed. Their study analyzes production storage data at large scale and treats these faults as a reliability problem distinct from complete disk failure.

This source is used only as **independent empirical context**. It does not establish ZFS implementation details, and its measured rates are not silently assigned to ZFS pools.

The retention consequence is nevertheless important:

> A redundant system can possess enough information to repair a block while still failing to benefit from that redundancy if the defect remains undiscovered until another failure removes the needed repair source.

That last sentence is engineering reconstruction from the relation among latent error, redundancy, and later repair—not a quotation from the paper.

### H/P — later OpenZFS makes maintenance progress itself persistent

The 2017 OpenZFS pause/resume commit says the feature is implemented by maintaining **persistent on-disk scrub state**. OpenZFS 2.1 documentation further says paused state and progress are periodically synced to disk and that restart/export-import resumes from the last on-disk checkpoint.

OpenZFS 2.1.11 source makes the distinction concrete: `dsl_scan_init()` reloads `DMU_POOL_SCAN` and scan-queue state after reboot, while `dsl_scan_sync_state()` only writes the normal persistent scan record when its sorting queues are in a consistency-safe state.

This later implementation evidence is developed in the dedicated deepening note and is **not** a claim about the exact Sun-era implementation.

### H/P — 2026 OpenZFS separates runtime `DSS_FINISHED` from safe wait completion

OpenZFS commit `92a3904afc93c3a70584f13db8f26816dc79328d`, merged 2026-09-09, fixes a race in `zpool wait -t scrub/resilver`. The old predicate could observe the scan as no longer `DSS_SCANNING` while the txg containing final DTL/config/label work was still syncing.

The fix records the finishing txg and keeps the activity reported as in progress until `spa_last_synced_txg()` reaches that txg. The bounded relation is therefore:

```text
runtime DSS_FINISHED
    != final scan txg synced
    != safe completion observation by a waiter
```

This is an implementation record, not a philosophical reinterpretation of `finished`.

---

## Retained state

This case now requires at least eight distinct targets.

### 1. User payload and filesystem metadata

The ordinary data/metadata the pool is expected to return.

### 2. Integrity evidence

The checksums against which read results are validated. Integrity evidence is not the same thing as another copy of the payload.

### 3. Redundant repair source

A mirror/RAID-Z or other redundant embodiment from which a correct copy can be obtained after corruption is detected.

### 4. Pool/device health and error state

The system records encountered errors and exposes pool/device status. These operational states help determine whether a physical survivor remains acceptable and whether repair is needed.

### 5. Repair opportunity

This is not a payload object. It is the still-existing relation `bad block + trustworthy alternate copy + functioning repair path`. Scrubbing can consume I/O in order to discover defects while that relation still exists.

`repair opportunity` is a project term, not period vocabulary.

### 6. Live maintenance progress / policy

Later OpenZFS must distinguish whether a scan is active/paused and how far the running traversal has advanced.

### 7. Durable scan checkpoint

Later OpenZFS persists scan-control state from which a paused/interrupted operation can be reconstructed. This checkpoint can lag the live execution frontier.

### 8. Completion transaction and wait predicate

The 2026 fix shows that terminal scan state and the txg carrying final configuration/label updates are separate moments. A caller's safe completion predicate can therefore depend on the latter being synced.

The decomposition is:

```text
payload state
    != integrity evidence
    != redundant repair source
    != live scan progress
    != durable scan checkpoint
    != final completion txg
    != API-visible completion predicate
```

---

## Retention mechanism

### Quiescent media retention

Individual disk sectors or other pool devices retain bytes through their underlying media mechanisms. This case does not duplicate disk/Flash physics already handled elsewhere.

### End-to-end-ish checksum verification within the filesystem layer

ZFS does not accept mere successful device I/O as sufficient evidence that the returned block is the intended current block. The filesystem-layer checksum relation participates in deciding whether the retrieved block is acceptable.

The case uses `end-to-end-ish` only as engineering shorthand; the historical wording retained in claims is the guide's own filesystem-layer checksumming/recovery description.

### Demand-triggered checking

Ordinary access can reveal a damaged block.

### Proactive full-pool checking

`zpool scrub` deliberately traverses all pool data even when applications have not requested every block.

### Conditional self-healing

When a bad block is detected and another trustworthy redundant copy exists, ZFS can replace the bad embodiment with correct data.

### Device-replacement reconstruction

Resilvering transfers required current state to a replacement/out-of-date device and restores the desired redundancy condition only when the process completes.

### Checkpointed maintenance execution — later OpenZFS deepening

The later implementation periodically materializes a safe scan-control frontier to pool metadata. Reboot/import can reconstruct the operation from that retained frontier rather than treating every process restart as a new scan from zero.

This mechanism retains **control state about verification work**, not another copy of the user payload.

---

## Read semantics

A ZFS read is not only `device returned bytes`.

For the bounded integrity path:

```text
read candidate
    -> checksum / identity validation
    -> acceptable current block

or

read candidate
    -> integrity failure
    -> obtain trustworthy redundant copy if available
    -> return/repair from that copy
```

Scrubbing deliberately exercises this broad verification path across the pool before ordinary application demand necessarily reaches each block.

Reading during a scrub is normally nondestructive at the logical interface, but a discovered integrity failure may trigger repair writes. Therefore:

> `scrub read` ≠ `purely observational read with no possible state transition`.

---

## Write / repair semantics

Ordinary application writes are outside this bounded case except insofar as checksums must continue to correspond to the current data.

Repair differs from ordinary update:

- the logical value is intended to remain the same;
- one physical embodiment is judged bad;
- another redundant embodiment supplies the current value;
- the bad copy is replaced or corrected.

This is **maintenance of an existing logical state**, not creation of a newer application value.

Later OpenZFS adds another write class to keep separate: writing/checkpointing **scan-control metadata**. Persisting progress or terminal maintenance state does not by itself rewrite the payload under verification.

---

## Time

This case introduces several distinct timescales:

- normal application read latency;
- time since a block was last read/verified;
- scrub traversal duration;
- interval between scrub passes;
- delay between defect creation and defect discovery;
- time between first latent defect and loss of another repair source;
- repair-write latency after detection;
- resilver duration after device replacement;
- time spent `DEGRADED` before desired redundancy is restored;
- later OpenZFS's interval between live progress and the last durable scan checkpoint;
- the final interval between setting terminal scan state and syncing the txg that carries final completion-side metadata.

The strongest bounded temporal point remains:

> **A physical defect may already exist while the logical system still appears healthy because the relevant block has not yet been checked.**

The later deepening adds a second timing boundary:

> **Verification work may already have been performed while the restart-safe checkpoint still trails it, and terminal state may already have been set while final completion-side metadata is still syncing.**

`verification age` is a useful engineering comparison term for the elapsed interval since a block or region was last successfully checked, but this case does **not** claim that the bounded ZFS version stores a per-block `verification age` variable.

---

## Failure and forgetting modes

Distinct failures include:

- a block becoming unreadable between successful accesses;
- a block remaining readable at the device level but failing higher-level checksum/identity validation;
- a latent fault remaining undiscovered until ordinary demand;
- the alternate redundant copy failing before the latent fault is discovered;
- checksum/integrity evidence itself being unavailable or corrupted;
- insufficient redundancy to self-heal a detected block;
- scrub not being run, being cancelled, or being delayed long enough for repair opportunity to shrink;
- scrub discovering damage but the repair write failing;
- device replacement/resilvering remaining incomplete while another failure occurs;
- pool degradation reducing redundancy even though current application reads still succeed;
- interruption after live scrub progress has advanced beyond the most recent safe persisted checkpoint, causing bounded verification rework after restart;
- an API/wait predicate declaring the maintenance activity over before its final transaction group has finished syncing, as in the pre-2026 OpenZFS race.

Do not collapse these into `bit rot`. Detection, diagnosis, reconstruction, restoration of redundancy, execution progress, and completion durability are different retention events.

---

## Engineering reconstruction

### E — physical presence/readability ≠ verified current integrity

A block may physically exist and even be returned by a device, while checksum/identity verification rejects it. Retention at the medium layer and admissibility at the filesystem layer are separate relations.

### E — redundancy availability ≠ defect discovery

A good alternate copy can coexist with an undetected damaged copy. Until the damaged region is accessed or scrubbed, the system may not know that repair is needed.

### E — detection work ≠ repair work

Scrubbing performs proactive traversal/verification. Repair is conditional on discovering a problem and having a trustworthy source. A system can complete a scrub with no repair, detect an unrepairable problem, or detect and repair damage.

### E — scrub ≠ rebuild/resilver

Scrub searches broadly for unknown integrity problems among current data. Resilvering reconstructs state known to need restoration onto a replacement/out-of-date device. The operations may share read/verification machinery, but their triggers and completion conditions differ.

### E — verification timing can change effective fault tolerance

If one copy is already latently bad, the nominal redundancy level may overstate the repair margin available against a later member failure. Earlier verification can expose and repair the first defect while another good copy still exists.

This is a system-reliability inference supported by the scrub/latent-error relation, not a claim that ZFS advertises a numeric `effective redundancy` variable.

### E — proactive retention maintenance can be epistemic before it is restorative

DRAM refresh must actively recreate charge because the substrate predictably leaks. ZFS scrub can instead spend work primarily to **find out whether** retained blocks are still trustworthy; physical rewriting happens only when verification exposes damage and redundancy permits repair.

That difference matters for the repository's maintenance taxonomy.

### E — work performed ≠ work durably checkpointed

Later OpenZFS's documented resume point is the last checkpoint synced to disk. Therefore some already-performed verification may legitimately be repeated after interruption.

```text
live progress
    -> safe checkpoint sometime later

restart between them
    -> resume from checkpoint
    -> repeat bounded work
```

Repeated work is not evidence that payload retention failed.

### E — terminal state ≠ durable maintenance completion

The 2026 OpenZFS fix is a concrete implementation counterexample to equating `DSS_FINISHED` with a safe completion observation. The terminal enum can be set in syncing context before the same txg's final config/label work reaches disk.

The new wait predicate deliberately spans that `finishing` interval.

### E — txg sync boundary ≠ universal physical-media proof

The fix strengthens the OpenZFS software/API completion contract. It does not prove that every possible drive/controller stack provides unlimited power-loss guarantees beyond the lower-layer contracts ZFS relies upon.

---

## Functional analogies

### A — scrub is refresh-like only in the weakest maintenance sense

Both DRAM refresh and ZFS scrub are maintenance work performed so future access remains reliable. But the mechanisms differ sharply:

- DRAM refresh is deadline-driven restoration required even for healthy cells;
- scrub is periodic/proactive verification, with repair conditional on detected failure.

Therefore do **not** call scrubbing `storage refresh` as a historical or mechanism-equivalent statement.

### A — scrub and RAID rebuild both consume redundancy but at different moments

Case 17 reconstructs after a member is already known failed/degraded. Case 18 can expose a latent block defect **before** a full member failure and repair it while ordinary redundancy remains available.

This is a functional comparison, not a claim that ZFS scrub descends historically from Berkeley RAID rebuild semantics.

### A — self-healing resembles RADOS repair only at the repair-function layer

Both can replace a bad embodiment from another authoritative current embodiment. RADOS uses replica/version/placement protocol state; ZFS scrub uses filesystem checksum verification plus pool redundancy. Their currentness and failure models are not interchangeable.

### A — Case 100 DTL state and Case 18 scan-progress state are different maintenance records

Case 100's DTL records **what redundancy debt still exists**. The later Case 18 deepening records **how far a verification/reconstruction activity has safely progressed and when its completion is safe to expose**.

```text
DTL maintenance debt
    != scrub traversal checkpoint
    != scrub/resilver finishing txg
```

The functional comparison is useful because all are non-payload state required for storage maintenance; it is not a claim of identical representation.

### A — Case 101 Patrol Read shows a different interruption policy

Dell PERC Patrol Read can preserve maintenance scheduling/summary state while an automatic scan may restart from the beginning after reboot. Later OpenZFS instead documents resume from an on-disk scrub checkpoint.

The comparison shows that `maintenance state persists` can mean several different things:

```text
remember maintenance policy
    != retain reusable progress frontier
    != retain every transient execution detail
```

No historical lineage is claimed.

---

## Philosophical boundary

The technical fact that matters is not merely that `data persists`. It is that **the truth of continued availability can itself require scheduled verification work**, and later implementation evidence shows that this verification process can itself leave control state that must be retained.

A cautious philosophical question follows:

> What does it mean for a technical trace to be “still there” when its defect may already exist but remains operationally unknown until the system tests it?

This case does not answer that question by equating verification with memory, archive, or Heideggerian availability. It only supplies mechanism-level distinctions between:

- material survival;
- verified admissibility;
- repairability;
- restored redundancy;
- maintenance work performed;
- maintenance work durably checkpointed;
- and maintenance completion safely exposed.

---

## Counterexamples and limits

- A scrub cannot reconstruct data if no trustworthy redundant source exists.
- A successful scrub does not guarantee permanent future integrity; damage can occur immediately afterward.
- Checksums can detect many corruption classes but are not proof against every possible correlated failure or implementation bug.
- `all data and metadata is checksummed` is a ZFS system claim; it is not a universal property of RAID or filesystems.
- The 2004 Schwarz et al. paper establishes prior art for the general scrubbing concept, not ZFS implementation details.
- The 2007 latent-sector-error study supplies independent empirical context, not ZFS-specific error rates.
- The 2017–2026 OpenZFS control-state evidence is a **later deepening** and must not be back-projected into the Sun-era historical record.
- Persistent scrub progress does not imply per-block durable verification timestamps.
- Resume from a checkpoint does not imply zero repeated work after interruption.
- The 2026 `zpool wait` race does not by itself prove user-payload corruption or data loss.
- Waiting through the final txg's `spa_sync()` is a software completion contract, not a claim of magical immunity to every lower-layer hardware failure.
- This case does not cover automatic scrub scheduling policy, RAID-Z mathematics, deduplication, snapshots, or modern distributed scrub protocols.

---

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `OpenZFS scrub`, `zpool wait`, and `dsl_scan` found no dedicated case to reuse. Therefore this case retains the retention-specific mechanism rather than duplicating an existing technical history.

If a broader history of storage integrity checking, SCSI VERIFY, ZFS txg internals, scan sorting, Illumos/OpenZFS portability, disk ECC, or RAID-Z is added there later, this case should link to it and retain only the verification/repair/progress/completion timing comparison.

---

## Sources

### Primary / institutional — historical grounding

- Oracle archive of the Sun/OpenSolaris-era _Solaris ZFS Administration Guide_, **“Checksums and Self-Healing Data”**: <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gaypb/index.html>
- _Solaris ZFS Administration Guide_, **“Controlling ZFS Data Scrubbing”**: <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gbbxi/index.html>
- _Solaris ZFS Administration Guide_, **“Viewing Resilvering Status”**: <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gbcus/index.html>

### Project-primary — later implementation deepening

- OpenZFS, **“Implemented zpool scrub pause/resume”**, commit `0ea05c64f8d08c20439dd2a06e949a2aa4115101`, 2017-07-07: <https://github.com/openzfs/zfs/commit/0ea05c64f8d08c20439dd2a06e949a2aa4115101>
- OpenZFS 2.1, `zpool-scrub(8)`: <https://openzfs.github.io/openzfs-docs/man/v2.1/8/zpool-scrub.8.html>
- OpenZFS 2.1.11, `module/zfs/dsl_scan.c`: <https://github.com/openzfs/zfs/blob/zfs-2.1.11/module/zfs/dsl_scan.c>
- OpenZFS, **“Wait for the txg that finished a scan to sync”**, commit `92a3904afc93c3a70584f13db8f26816dc79328d`, merged 2026-09-09: <https://github.com/openzfs/zfs/commit/92a3904afc93c3a70584f13db8f26816dc79328d>
- OpenZFS PR #19066, **“Wait for the txg that finished a scan to sync”**: <https://github.com/openzfs/zfs/pull/19066>

### Prior art / scholarly context

- Thomas Schwarz, Qin Xin, Ethan L. Miller, Darrell D. E. Long, Andy Hospodor, Spencer Ng, **“Disk Scrubbing in Large Archival Storage Systems,”** MASCOTS 2004, pp. 409–418; SSRC publication record and abstract: <https://www.ssrc.us/pub/schwarz-mascots04.html>
- Lakshmi N. Bairavasundaram, Garth R. Goodson, Shankar Pasupathy, Jiri Schindler, **“An Analysis of Latent Sector Errors in Disk Drives,”** SIGMETRICS 2007, pp. 289–300, DOI 10.1145/1254882.1254917: <https://dl.acm.org/doi/10.1145/1254882.1254917>

---

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| disk scrubbing predates the bounded ZFS documentation | H/P | Schwarz et al. 2004 | supported |
| ZFS scrub proactively verifies pool data before application demand necessarily reaches it | H/P | Solaris ZFS guide | supported |
| ZFS can repair detected bad data from trustworthy redundancy | H/P | Solaris ZFS guide | supported |
| scrub and resilver have distinct triggers/roles | H/P | Solaris ZFS guide | supported |
| 2017 OpenZFS pause/resume uses persistent on-disk scrub state | H/P | commit `0ea05c64` | supported |
| OpenZFS 2.1 documents paused-state/progress sync and restart from the last on-disk checkpoint | H/P | `zpool-scrub(8)` | supported |
| OpenZFS 2.1.11 reconstructs scan execution from persistent `DMU_POOL_SCAN`/queue state | H/P | `dsl_scan.c` | supported |
| persistent scan-state writes are gated by a safe queue condition | H/P | `dsl_scan_sync_state()` | supported |
| before the 2026 fix, `zpool wait` could return after in-core terminal state but before final txg sync | H/P | PR #19066 / commit `92a3904` | supported |
| the 2026 fix extends completion observation through the finishing txg's sync | H/P | `dsl_scan_done()` / `spa_activity_in_progress()` | supported |
| work performed is distinct from work durably checkpointed | E | restart-from-checkpoint semantics | supported reconstruction |
| terminal scan state is distinct from durable maintenance completion | E | 2026 bug/fix | strongly supported reconstruction |
| final txg sync is universal proof of physical-media permanence | E | none | **not claimed** |

---

## Remaining evidence debt

The central Case 18 mechanism and the later maintenance-control distinction are grounded. Useful future deepening remains:

1. trace the earliest Illumos/OpenZFS revision in which scan progress became restartable independently of the 2017 explicit pause UI;
2. reproduce paused-scrub export/import or reboot and measure bounded rework between live and persisted frontiers;
3. reproduce the pre-`92a3904` wait race against the historical parent commit with controlled write delay;
4. identify the exact label/config/MOS objects participating in scrub versus resilver completion rather than inferring them from broad names;
5. keep controller/cache/media flush semantics as a separate lower-layer durability case.

No evidence here requires changing the canonical maturity from `grounded`.