# ZFS Data Scrubbing: Proactive Integrity Verification Before Demand

## Scope

- **Bounded mechanism:** pool-wide integrity scrubbing in ZFS, with checksums and redundant-copy repair, contrasted with device-replacement resilvering.
- **Bounded period:** 2004–2010. The 2004 MASCOTS paper supplies a pre-ZFS-invention-priority boundary for `disk scrubbing`; the Sun/OpenSolaris-era ZFS administration semantics are taken from the Solaris ZFS Administration Guide as archived by Oracle.
- **Primary/system witness:** _Solaris ZFS Administration Guide_, especially `Checksums and Self-Healing Data`, `Controlling ZFS Data Scrubbing`, and `Viewing Resilvering Status`.
- **Prior-art witness:** Thomas Schwarz, Qin Xin, Ethan L. Miller, Darrell D. E. Long, Andy Hospodor, and Spencer Ng, **“Disk Scrubbing in Large Archival Storage Systems,”** MASCOTS 2004, pp. 409–418.
- **Independent empirical context:** Lakshmi N. Bairavasundaram, Garth R. Goodson, Shankar Pasupathy, and Jiri Schindler, **“An Analysis of Latent Sector Errors in Disk Drives,”** SIGMETRICS 2007.
- **Research question:** what changes when a retained block can remain physically present yet defective or unverified until it is read, and how does proactive scrubbing differ from failure-triggered reconstruction/rebuild?

This is **not** a general history of ZFS, checksums, RAID-Z, end-to-end data integrity, latent-sector-error statistics, or modern OpenZFS scan policy. It also does not claim that ZFS invented disk scrubbing.

The bounded comparison is narrower:

> **Retention can fail first as an undetected integrity defect. A scrub advances the moment of verification before ordinary demand, and—when a trustworthy redundant copy exists—can couple detection to repair before a later failure consumes the remaining repair path.**

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

The following are **project engineering terms**, not historical ZFS vocabulary claims:

- `verification latency`;
- `verification age`;
- `latent-integrity window`;
- `repair-opportunity margin`;
- `proactive verification work`.

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

---

## Retained state

This case requires at least five distinct targets.

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
- time spent `DEGRADED` before desired redundancy is restored.

The strongest bounded temporal point is:

> **A physical defect may already exist while the logical system still appears healthy because the relevant block has not yet been checked.**

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
- pool degradation reducing redundancy even though current application reads still succeed.

Do not collapse these into `bit rot`. Detection, diagnosis, reconstruction, and restoration of redundancy are different retention events.

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

---

## Philosophical boundary

The technical fact that matters is not merely that `data persists`. It is that **the truth of continued availability can itself require scheduled verification work**.

A cautious philosophical question follows:

> What does it mean for a technical trace to be “still there” when its defect may already exist but remains operationally unknown until the system tests it?

This case does not answer that question by equating verification with memory, archive, or Heideggerian availability. It only supplies a mechanism-level distinction between:

- material survival;
- verified admissibility;
- repairability;
- and restored redundancy.

---

## Counterexamples and limits

- A scrub cannot reconstruct data if no trustworthy redundant source exists.
- A successful scrub does not guarantee permanent future integrity; damage can occur immediately afterward.
- Checksums can detect many corruption classes but are not proof against every possible correlated failure or implementation bug.
- `all data and metadata is checksummed` is a ZFS system claim; it is not a universal property of RAID or filesystems.
- The 2004 Schwarz et al. paper establishes prior art for the general scrubbing concept, not ZFS implementation details.
- The 2007 latent-sector-error study supplies independent empirical context, not ZFS-specific error rates.
- Current OpenZFS scan implementation and policy have evolved beyond the bounded period and are not silently back-projected.
- This case does not cover automatic scrub scheduling policy, RAID-Z mathematics, deduplication, snapshots, or modern distributed scrub protocols.

---

## Related repositories

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `scrub`, `scrubbing`, `latent sector`, and `ZFS` found no dedicated case at the time of this slice. Therefore this file adds a retention-specific argument rather than duplicating an existing engineering history.

If a broader history of storage integrity checking, SCSI VERIFY, disk ECC, ZFS architecture, or RAID-Z is added there later, this case should link to it and retain only the verification/repair-timing comparison.

---

## Sources

### Primary / institutional

- Oracle archive of the Sun/OpenSolaris-era _Solaris ZFS Administration Guide_, **“Checksums and Self-Healing Data”**: <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gaypb/index.html>
- _Solaris ZFS Administration Guide_, **“Controlling ZFS Data Scrubbing”**: <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gbbxi/index.html>
- _Solaris ZFS Administration Guide_, **“Viewing Resilvering Status”**: <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gbcus/index.html>

### Prior art / scholarly context

- Thomas Schwarz, Qin Xin, Ethan L. Miller, Darrell D. E. Long, Andy Hospodor, Spencer Ng, **“Disk Scrubbing in Large Archival Storage Systems,”** MASCOTS 2004, pp. 409–418; SSRC publication record and abstract: <https://www.ssrc.us/pub/schwarz-mascots04.html>
- Lakshmi N. Bairavasundaram, Garth R. Goodson, Shankar Pasupathy, Jiri Schindler, **“An Analysis of Latent Sector Errors in Disk Drives,”** SIGMETRICS 2007, pp. 289–300, DOI 10.1145/1254882.1254917: <https://dl.acm.org/doi/10.1145/1254882.1254917>

---

## Status

**`grounded` for the bounded mechanism.**

The central claims are supported by system-primary/institutional documentation plus pre-existing scholarly prior art and independent empirical context. No claim that ZFS invented scrubbing, no ZFS-specific assignment of SIGMETRICS field rates, and no modern OpenZFS implementation detail is required for the case.
