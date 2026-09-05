# SCSI-2 Write-Back Cache, FUA, and SYNCHRONIZE CACHE: Completion Before Medium and Typed Durability

## Scope

- **Object / interface:** direct-access SCSI block-device cache semantics.
- **Bounded period:** 1994–2004, with a 2001 Seagate product implementation witness.
- **Primary question:** when a write may complete while its newest logical-block value still resides in controller/device cache, what additional interface state and commands distinguish `current`, `completed`, `written to the physical medium`, and `survives a power cycle`?

This is not a general history of SCSI, disk caches, RAID controllers, battery-backed write cache, operating-system buffer caches, filesystems, or storage barriers. It is a retention-specific predecessor comparison for Case 20's 2011 NVMe `VWC` / `Flush` / `FUA` boundary.

The bounded result is:

> **SCSI-2 already made ordinary write completion weaker than physical-medium commitment when write-back caching was enabled, while `FUA` and `SYNCHRONIZE CACHE` supplied stronger, separately scoped media-access relations. By 2004, SBC-2 work made another distinction explicit: a non-volatile cache can survive power cycles yet still be weaker than the medium for removal, controller replacement, or long shutdown.**

That result does not prove a direct SCSI → NVMe genealogy. It establishes earlier interface prior art for separating completion, cache residence, media commitment, failure survival, and portability.

---

## Historical vocabulary

The inspected sources use:

- `cache memory` / `cache`;
- `write-back caching`;
- `write-through caching`;
- `force unit access (FUA)`;
- `SYNCHRONIZE CACHE`;
- `physical medium` / `medium`;
- `GOOD status`;
- `deferred error`;
- `volatile cache`;
- `non-volatile cache`;
- `FUA_NV` and `SYNC_NV` in the later SBC-2 work.

The following are **project engineering terms**, not claims about SCSI historical vocabulary:

- `completion boundary`;
- `media-commit boundary`;
- `typed durability`;
- `controller-coupled survivability`;
- `portability-qualified retention`;
- `retention handoff`.

Do not silently rename 1994 SCSI-2 semantics using later NVMe phrases such as `Volatile Write Cache`, `Flush command`, or `persistence domain`.

---

## Historical record

### H/P — SCSI-2 explicitly separated cache from the stored blocks

ANSI X3.131-1994 §9.1.6 describes cache memory as temporary storage inside the direct-access device, separate from the stored blocks and normally not directly accessible by the initiator. During write operations, data may be placed in cache and written to the medium later; the standard names this **write-back caching**.

Most importantly, it states that under write-back caching the command may complete **before** the blocks are written to the medium. It also names the resulting power/hardware-loss interval and allows a later media-write failure to appear as a **deferred error** on another command.

**Primary anchor:** ANSI X3.131-1994, §9.1.6 `Data cache`, printed p. 152.

### H/P — SCSI-2 FUA strengthened one command from cache acceptance to physical-medium access

The same §9.1.6 says the `force unit access (FUA)` bit tells the direct-access device to access the physical medium. For a write, `FUA=1` requires the device to complete the data write to the physical medium **before completing the command**. For a read, it requires retrieval from the physical medium rather than satisfying the read from cache.

This is a bounded command-level relation. It does not mean that every other cached write has been drained.

**Primary anchor:** ANSI X3.131-1994, §9.1.6, printed p. 152.

### H/P — SCSI-2 SYNCHRONIZE CACHE was a separate cache-to-medium control

SCSI-2 says `SYNCHRONIZE CACHE` forces pending write data in the requested set of logical blocks to be stored in the physical medium and can be used to ensure that data were written and detected errors reported.

The command therefore differs from an ordinary write and from per-command FUA in control shape: it acts on pending cached state for a requested logical-block range.

**Primary anchor:** ANSI X3.131-1994, §9.1.6 with cross-reference to §9.2.18, printed p. 152.

### H/P — a period product implemented the same GOOD-status / medium-write split

Seagate's **Cheetah 73LP Product Manual, Rev. C** says that with write caching enabled (`WCE=1`) the drive may return `GOOD` status after data enter cache but before they are written to the medium. A later media-write failure after `GOOD` becomes a deferred error. The same manual states that `Synchronize Cache` forces cached write data to the medium and that when the command completes, data from previous writes have been written to the medium.

This is useful implementation evidence that the standard's distinction was not merely abstract vocabulary.

**Primary anchor:** Seagate, _Cheetah 73LP Product Manual, Rev. C_, 2001, §4.5.1 `Cache operation`, printed p. 12.

### H/P — 2004 T10 work made volatile cache, non-volatile cache, and medium three different retention classes

T10 proposal **03-388r2**, dated 10 March 2004, begins from an explicit limitation: existing SBC-2 cache controls understood cache but did not adequately distinguish **non-volatile cache**. It gives battery-backed RAID-controller cache as the motivating example and says such cache may preserve data for hours or days.

The proposal distinguishes several use cases:

- short power loss or reboot may be satisfied by retaining data in non-volatile cache;
- moving disks to another controller requires a coherent set on the medium rather than leaving some current data in controller cache;
- extended shutdown and removable media similarly create reasons to force the medium.

It therefore proposes `FUA_NV` and `SYNC_NV` so software can request a non-volatile-cache boundary separately from the physical-medium boundary.

**Primary anchor:** T10/03-388r2, pp. 1–2, `Overview` and `Proposal`.

### H/P — SBC-2 revision 16 incorporated the non-volatile-cache distinction

T10's current standards/version list identifies **SBC-2 T10/1417-D revision 16** as the final-draft version associated with later INCITS 405-2005. The 13 November 2004 revision-16 text distinguishes volatile and non-volatile caches, states that non-volatile cache may have a finite retention time without power, and preserves the write-back rule that a command can complete before medium write.

It also defines:

- `FUA=1`: write reaches the medium before command completion;
- `FUA_NV=1` with `FUA=0`: write may complete after reaching non-volatile cache rather than medium;
- `SYNC_NV=0`: synchronization to the medium;
- `SYNC_NV=1`: where supported, synchronization may stop at non-volatile cache or medium.

This is later than SCSI-2 and must not be projected backward into the 1994 vocabulary.

**Primary / standards-history anchors:** T10/1417-D Revision 16, 13 November 2004, §4.10 and SYNCHRONIZE CACHE sections; T10 standards version-descriptor list.

---

## Retained state

This case requires at least five state classes to remain distinct.

### 1. Host-visible current logical-block value

After a write has been accepted into write-back cache, the device can hold the newest value for an LBA even while the physical medium still contains an older value.

### 2. Volatile cached write data

This is current enough to satisfy the caching policy but is explicitly exposed to loss across the relevant power/hardware failure interval.

### 3. Non-volatile cached write data

In the 2004 SBC-2 regime, cache can retain data through power cycles. The source explicitly warns that this retention may still have a time limit.

### 4. Physical-medium representation

FUA and ordinary `SYNCHRONIZE CACHE` can require the newest logical-block value to reach the physical medium before the relevant completion boundary.

### 5. Deferred-error state / obligation

When a cached write has already returned `GOOD` and the later medium write fails, the original command cannot simply be retroactively un-completed. The device may instead retain/report the failure as a deferred error on a subsequent command.

This is control/error state, not the user payload itself.

---

## Retention mechanism and transitions

### Ordinary write-back path

```text
initiator WRITE
    ↓
device/cache receives newest logical-block value
    ↓
GOOD / command completion may occur
    ↓
physical-medium write happens later
```

The interval between cache acceptance and media write is a real retention regime, not merely an implementation detail that can be collapsed into `the disk has the data`.

### FUA path

```text
WRITE with FUA=1
    ↓
physical-medium access/write
    ↓
command completion / GOOD
```

FUA strengthens the completion condition of that access. It does not by itself mean `flush every unrelated cached block`.

### SYNCHRONIZE CACHE path

```text
pending newer cached blocks in requested range
    ↓
explicit synchronization request
    ↓
newest values recorded on physical medium
    ↓
completion relation
```

SCSI-2 describes this as an explicit way to make pending cached writes reach the physical medium and expose detected errors.

### Later non-volatile-cache path

```text
volatile cache
    ↓
SYNC_NV / FUA_NV-qualified transition (where supported)
    ↓
non-volatile cache
    ↓  optional/required stronger transition
physical medium
```

The 2004 distinction makes clear that `survives a power cycle` and `is on the medium` can be two different storage-interface predicates.

---

## Addressing and scope

The initiator addresses logical blocks, not cache SRAM cells or physical sectors directly.

Three scopes should not be merged:

- an ordinary WRITE addresses its logical-block range;
- `FUA` changes the access/completion condition for the addressed command;
- `SYNCHRONIZE CACHE` targets pending cached state over an explicit range, with zero-valued range conventions able to cover a broader remainder/device scope in the command family.

The interface therefore exposes not just **where** data are logically named but **how far down the retention path** an operation must carry their newest value.

---

## Read / write / synchronization semantics

### Ordinary cached write

`GOOD` can mean that the command completed successfully under the enabled cache policy even though the physical medium has not yet received the newest value.

### FUA write

`FUA=1` raises the required destination for that write to the physical medium before completion.

### Synchronization

`SYNCHRONIZE CACHE` is a later explicit operation over already-pending cache state. It is not another user-data write and does not imply that synchronized blocks must be evicted from cache. The 2004 T10 text explicitly permits logical blocks to remain cached after synchronization.

### Deferred errors

Write-back caching permits a medium-write error to occur after the command that supplied the data has already completed. The reporting relation can therefore become temporally detached from the operation that caused it.

---

## Time

At least these times are distinct:

- host transfers data to the device;
- cache receives the newest version;
- ordinary WRITE returns `GOOD`;
- a later physical-medium write begins;
- that write succeeds or fails;
- a deferred error may be reported on a later command;
- an explicit synchronization begins and completes;
- power is lost and restored;
- non-volatile-cache retention time elapses;
- a disk/removable medium is detached from the controller that held cached state.

A major result of the 2004 source is that the relevant survival interval depends on the anticipated transition. `Power cycle`, `extended shutdown`, and `controller/media separation` are not one failure model.

---

## Maintenance, energy, and labor

Write-back caching moves retention responsibility rather than removing it:

- device firmware/controller logic tracks dirty/current cached blocks;
- media-write scheduling eventually propagates current values downward;
- the initiator/OS chooses whether ordinary completion is sufficient or FUA/synchronization is required;
- error machinery retains and later reports deferred failures;
- battery-backed/non-volatile controller cache depends on whatever power/storage infrastructure actually supplies the advertised retention interval;
- administrators must use a stronger medium boundary before physically moving media away from the controller when controller-local cache may contain current data.

The SCSI interface does not identify the exact battery chemistry, capacitor, SRAM design, RAID firmware, or cache journal used by every implementation. Those mechanisms require named-device evidence.

---

## Failure / forgetting modes

Distinct bounded failures include:

- power loss while the only newest copy is in volatile cache;
- hardware failure during the write-back interval;
- a later medium-write error after the original command already returned `GOOD`;
- software treating ordinary completion as proof of physical-medium write;
- software treating non-volatile controller cache as equivalent to a medium that can be removed and read under another controller;
- extended unpowered time exceeding a non-volatile cache's finite retention capability;
- failure of the controller/cache infrastructure that is still required to recover controller-resident state;
- later medium failure after successful synchronization, which is a different failure regime.

Do not collapse these into one generic `write lost` category.

---

## Engineering reconstruction

### E — GOOD status / command completion ≠ physical-medium residency

SCSI-2's write-back rule is a direct counterexample to an end-to-end interpretation of `completed`: the newest logical value can be accepted and the command can finish while the medium remains older.

### E — current logical value can temporarily live above the medium

During write-back, cache is not merely a duplicate acceleration copy. It can be the location of the newest version that must still be propagated to the medium.

### E — FUA is a per-access completion strengthening, not a generic cache purge

The historical definition ties the addressed operation's completion to physical-medium access. `FUA` and `SYNCHRONIZE CACHE` therefore solve related but non-identical retention problems.

### E — synchronization completion ≠ cache eviction

The later T10 text allows synchronized blocks to remain in cache. The retention transition is about currentness of the lower layer, not compulsory disappearance of the upper-layer copy.

### E — deferred error preserves failure information after success was already reported

Write-back caching separates the chronology of request completion from the chronology of media failure. A later error-reporting relation is required because the causing command has already crossed its ordinary completion boundary.

### E — power-cycle survival ≠ physical-medium independence

A non-volatile controller cache can make a current value survive short power loss while still leaving that value dependent on the same controller/cache infrastructure. If the disks move elsewhere, the medium itself must already contain the coherent current state.

### E — non-volatile cache ≠ indefinite retention

SBC-2 revision 16 explicitly allows a limit on how long non-volatile cache retains data without power. `Non-volatile` is therefore not an evidence-free synonym for timeless persistence.

---

## Functional analogies

### A — Case 20, NVMe 1.0 VWC / Flush / FUA

SCSI-2 and NVMe 1.0 both expose a host/controller boundary where ordinary completion, cached state, explicit synchronization, and per-command forced media access must remain separate.

The comparison is useful because SCSI-2 is earlier. It does **not** establish that NVMe copied one exact SCSI mechanism or that similarly named `FUA` fields have identical scope in every revision.

### A — Case 15, Intel SSD 320 power-loss protection

Case 15 supplies a named physical/controller implementation in which stored energy moves volatile state toward NAND after power loss. Case 87 stays at the SCSI interface and later non-volatile-cache contract. A battery-backed RAID cache is a motivating example in T10, not evidence that every SCSI cache uses Intel-style SSD PLP.

### A — Cases 31–32, persistence domains / ADR-eADR

All three cases show that a state may be failure-protected before it reaches the final medium if a stronger transition guarantee exists. The historical mechanisms and vocabulary differ: SCSI cache/media controls are not SNIA persistence-domain terminology and are not Intel ADR/eADR.

---

## Philosophical interpretation

### I — `retained` depends on the transition one intends to survive

This case makes a useful limit on substrate-centered language. One current logical value can be:

- sufficient for ordinary running service because it is in write-back cache;
- insufficient for a sudden power failure if that cache is volatile;
- sufficient for a short power cycle if held in qualified non-volatile cache;
- still insufficient for detaching the medium from that controller;
- sufficient for that detachment only after the medium itself has the coherent current state.

The philosophical lesson is not that persistence is “merely relative” or contractual. Each layer still depends on concrete hardware and successful transitions. The narrower result is that **availability across time is typed by the interruption, duration, and infrastructure boundary being crossed**.

That interpretation is the repository's reconstruction, not SCSI actors' own philosophical vocabulary.

---

## Counterexamples and limits

This case does **not** establish:

- that all SCSI devices implemented write-back caching;
- that `GOOD` always preceded media write;
- that all non-volatile caches used batteries;
- that SCSI-2 contained `FUA_NV` or `SYNC_NV` in 1994;
- that the 2004 proposal alone proves every later product implemented those bits;
- that non-volatile cache is equivalent to secure or indefinite storage;
- that FUA creates a global order among unrelated commands;
- that successful synchronization protects against later media failure;
- that SCSI invented write-back caching, forced access, cache flushing, or stable storage;
- a direct SCSI → NVMe genealogy.

---

## Related repositories

[`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) currently treats post-RAMAC disk geometry, controller intelligence, and the ST-506 / SCSI / IDE-ATA / SATA transitions as a still-missing historical bridge. A complete SCSI bus/command-set/controller genealogy belongs there. This case therefore keeps only the cache/currentness/durability semantics needed by `technical-retention`.

See that repository's [`AUDIT.md`](https://github.com/tmzncty/computing-archaeology/blob/main/AUDIT.md), especially `P1-C — Disk and removable-media geometry after RAMAC`.

---

## Sources

### Primary / standards sources

1. ANSI X3.131-1994, _Small Computer System Interface-2 (SCSI-2)_, especially §9.1.6 `Data cache`, printed p. 152. Preserved scan: <https://www.bitsavers.org/components/ncr_symbios/scsi/SCSI-2_Standard_1994.pdf>.
2. Seagate Technology, _Cheetah 73LP Product Manual_, Rev. C, 2001, especially §4.5.1 `Cache operation`, printed p. 12: <https://www.seagate.com/support/disc/manuals/scsi/100109943c.pdf>.
3. Rob Elliott (HP), T10/03-388r2, _SPC-3 SBC-2 Nonvolatile caches_, 10 March 2004: <https://www.t10.org/ftp/t10/document.03/03-388r2.pdf>.
4. T10/1417-D Revision 16, _SCSI Block Commands - 2 (SBC-2)_, 13 November 2004; preserved draft copy: <https://citeseerx.ist.psu.edu/document?doi=ee9633c63189099a796a09ae69824ca39b0f4fc3&repid=rep1&type=pdf>.
5. T10, `SCSI Standards Version Descriptors`, documenting SBC-2 Revision 16 and INCITS 405-2005: <https://www.t10.org/lists/stds-alph.htm>.

### Repository evidence record

- [`../evidence/87-scsi-1994-2004-cache-durability-grounding.md`](../evidence/87-scsi-1994-2004-cache-durability-grounding.md)

---

## Status

**grounded**

The central retention boundary is supported by the 1994 SCSI-2 standard, a named Seagate implementation, and 2004 T10/SBC-2 standards work. Remaining work is deliberately separate: exact pre-SCSI-2 cache-control genealogy, controller-specific non-volatile-cache implementation/fault validation, later SBC-3 removal/obsolescence of `SYNC_NV`, cross-protocol ordering semantics, and a full SCSI→SAS/NVMe lineage.