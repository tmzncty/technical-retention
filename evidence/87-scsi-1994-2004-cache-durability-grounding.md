# Case 87 grounding — SCSI cache completion, forced media access, and non-volatile-cache boundaries (1994–2004)

## Purpose

Ground the bounded Case 87 claim that direct-access SCSI already separated:

```text
ordinary command completion / GOOD
    ≠
newest value written to physical medium
    ≠
explicit cache synchronization
    ≠
qualified survival in non-volatile controller cache
    ≠
media-independent / removable-state completeness
```

This record does not attempt a complete SCSI command-set, disk-cache, RAID-controller, or NVMe genealogy.

---

## Source 1 — ANSI X3.131-1994, SCSI-2

**Type:** period standard / primary technical source.

**Document:** _Small Computer System Interface-2 (SCSI-2)_, ANSI X3.131-1994.

**Preserved scan:** <https://www.bitsavers.org/components/ncr_symbios/scsi/SCSI-2_Standard_1994.pdf>

### Direct anchor

§9.1.6 `Data cache`, printed p. 152.

### Claims grounded

The standard states that:

- cache memory is temporary storage separate from stored blocks and normally not directly accessible by the initiator;
- during write operations the device can hold data in cache and write it to the medium later;
- this is called a `write-back caching algorithm`;
- under write-back caching, a command may complete before blocks are written to the medium;
- this creates an interval in which power/hardware failure can lose data;
- an error during the later medium write may be reported as a `deferred error` on a later command;
- `FUA=1` on a write requires the physical-medium write before command completion;
- `FUA=1` on a read requires retrieval from the physical medium;
- `SYNCHRONIZE CACHE` forces pending write data in the requested logical-block set to be stored in the physical medium and can be used to ensure writing and detected-error reporting.

### Why this is decisive

This single period-standard section directly blocks several later shortcuts:

```text
command completed
    ≠ automatically
physical medium is current

write-back cache contains newest value
    ≠ automatically
power-fail-safe value

FUA
    ≠ merely a performance hint
```

It also establishes that the `FUA` and `SYNCHRONIZE CACHE` vocabulary is historical SCSI-2 vocabulary no later than the 1994 standard.

### Evidence limit

The standard defines an interface. It does not tell us the SRAM technology, battery, capacitor, cache journal, spindle firmware, or internal scheduling algorithm of a particular target.

The source also does **not** contain the later `FUA_NV` / `SYNC_NV` distinction used in the 2004 SBC-2 chain. Those terms must not be projected backward.

---

## Source 2 — Seagate Cheetah 73LP Product Manual, Rev. C (2001)

**Type:** manufacturer-primary implementation witness.

**Document:** Seagate Technology, _Cheetah 73LP Product Manual_, Rev. C.

**URL:** <https://www.seagate.com/support/disc/manuals/scsi/100109943c.pdf>

### Direct anchor

§4.5.1 `Cache operation`, printed p. 12.

### Claims grounded

Seagate states that when write caching is enabled (`WCE=1`):

- a write may return `GOOD` after data transfer into cache but before medium write;
- a later error writing that data to the medium after `GOOD` produces a deferred error;
- `Synchronize Cache` can force all cached write data to the medium;
- when that synchronization completes, data received from previous writes have been written to the medium.

### Why this source matters

The SCSI-2 distinction was implemented in a named commercial disk family. The case therefore does not depend solely on an abstract standards possibility.

### Evidence limit

This manual grounds this drive family's documented behavior. It does not establish the default/cache semantics of every SCSI disk, nor does it prove fault-path compliance under every power-loss timing window.

---

## Source 3 — T10/03-388r2, _SPC-3 SBC-2 Nonvolatile caches_ (10 March 2004)

**Type:** official T10 technical proposal / primary standards-process evidence.

**URL:** <https://www.t10.org/ftp/t10/document.03/03-388r2.pdf>

### Direct anchors

- p. 1, `Overview` and `Proposal`;
- pp. 2–4, proposed definitions/cache model;
- p. 6 onward, proposed `FUA_NV` / `SYNC_NV` command changes.

### Claims grounded

The proposal says that existing SBC-2 had cache-aware tools including FUA and SYNCHRONIZE CACHE but did not adequately comprehend non-volatile cache as a separate destination class.

It gives battery-backed RAID-controller cache as an explicit motivating example and distinguishes operational goals:

- for temporary power loss or reboot, retaining current data in non-volatile cache can be sufficient;
- for moving disks to another controller, leaving some coherent current state only in controller cache is insufficient;
- extended shutdown and removable media similarly motivate forcing current state to the medium.

It describes then-current behavior as:

- `SYNCHRONIZE CACHE` → medium;
- `FUA=1` → medium;

and proposes:

- `SYNC_NV` → allow a synchronization boundary at non-volatile cache;
- `FUA_NV` → allow an access/completion boundary at non-volatile cache.

The proposed cache model further says:

- volatile cache does not retain through power cycles;
- non-volatile cache does retain through power cycles;
- there may be a limit on how long non-volatile cache retains data;
- write-back may complete before medium write;
- later medium-write errors can be deferred;
- `FUA=1` requires physical-medium access before `GOOD`;
- synchronization to medium need not remove the block from cache.

### Why this source changes the comparison

It creates an especially clean three-way retention distinction:

```text
volatile cache
    ≠
non-volatile cache that survives a bounded interruption
    ≠
physical medium that can remain coherent when separated from the controller
```

This is stronger than the generic statement `battery-backed cache is durable`. The T10 problem statement itself explains why different future transitions demand different retention destinations.

### Evidence limit

This document is a proposal, not by itself proof that every proposed bit entered a final standard or was implemented in deployed products. Final-draft adoption is checked separately below.

Its motivating statement that RAID controllers `often employ battery-backed caches` is sufficient as a period standards-process witness, not as a quantitative deployment survey.

---

## Source 4 — T10/1417-D Revision 16, _SCSI Block Commands - 2_ (13 November 2004)

**Type:** final working draft / primary standards text.

**Preserved copy:** <https://citeseerx.ist.psu.edu/document?doi=ee9633c63189099a796a09ae69824ca39b0f4fc3&repid=rep1&type=pdf>

### Direct anchors

- §4.10 `Caches`;
- `WRITE` / FUA and FUA_NV definitions;
- `SYNCHRONIZE CACHE (10)/(16)` and SYNC_NV definitions.

### Claims grounded

Revision 16 states that:

- cache is separate from the medium;
- cache may be volatile or non-volatile;
- non-volatile cache retains through power cycles but may have a finite no-power retention time;
- write-back caching allows command completion before logical blocks reach the medium;
- power loss with volatile cache and hardware failure remain loss windows;
- later medium-write failure can be a deferred error;
- `FUA=1` makes a write reach the medium before command completion;
- `FUA_NV=1` with `FUA=0` may allow the write to complete after reaching non-volatile cache instead of medium;
- `SYNC_NV=0` synchronizes volatile and non-volatile cached logical blocks to the medium;
- `SYNC_NV=1`, where supported, allows volatile-cache state to synchronize to non-volatile cache or medium without requiring non-volatile-cache contents themselves to be pushed farther;
- synchronization need not imply cache eviction.

### Why this is decisive

The final-draft text shows that the 2004 distinction was not merely left at the proposal stage. It entered the SBC-2 revision-16 standards text as a typed choice between medium and non-volatile-cache completion/synchronization boundaries.

### Evidence limit

A final draft is not a named-controller implementation test. The case therefore does not claim `FUA_NV` / `SYNC_NV` deployment prevalence or correct behavior in any specific RAID controller.

---

## Source 5 — T10 standards/version-descriptor list

**Type:** official institutional standards-history metadata.

**URL:** <https://www.t10.org/lists/stds-alph.htm>

### Claim grounded

The current T10 list records:

- `SBC-2 T10/1417-D revision 16`;
- `SBC-2 INCITS 405-2005`.

This provides a controlled chronology anchor linking the inspected revision-16 draft to the SBC-2 standards line.

### Evidence limit

The list establishes identity/version chronology, not command semantics. Command claims remain grounded in the draft text itself.

---

## Related-repository check

[`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) was checked before creating this slice.

Its current [`INDEX.md`](https://github.com/tmzncty/computing-archaeology/blob/main/INDEX.md) describes storage coverage through RAMAC/direct-access disk, while [`AUDIT.md`](https://github.com/tmzncty/computing-archaeology/blob/main/AUDIT.md) lists **P1-C — Disk and removable-media geometry after RAMAC** as still missing, including:

- controller intelligence;
- ST-506 / SCSI / IDE-ATA / SATA transitions;
- later geometry hiding through FTLs.

No dedicated SCSI FUA / SYNCHRONIZE CACHE history was found in the repository search. Therefore Case 87 does not duplicate an established companion-repository history. The complete SCSI bus/command/controller lineage should still be routed there rather than expanded here.

---

## Claim classification

### Historical record

Supported directly:

- SCSI-2 cache/write-back/FUA/SYNCHRONIZE CACHE vocabulary and semantics;
- a 2001 Seagate implementation of GOOD-before-medium with deferred-error and synchronization behavior;
- 2004 T10 motivation for a distinct non-volatile-cache boundary;
- SBC-2 revision-16 volatile/non-volatile cache, FUA_NV and SYNC_NV semantics.

### Engineering reconstruction

Project terms derived from the mechanisms:

- `completion boundary`;
- `media-commit boundary`;
- `controller-coupled survivability`;
- `portability-qualified retention`;
- `typed durability`.

These terms are not attributed to ANSI, T10, or Seagate.

### Functional analogy

Bounded comparisons only:

- Case 20 NVMe 1.0 `VWC` / `Flush` / `FUA`;
- Case 15 Intel SSD 320 PLP;
- Cases 31–32 persistence-domain / ADR-eADR paths.

The sources do not establish direct genealogy among those mechanisms.

### Philosophical interpretation

The claim that retention is qualified by which transition the state must survive is a repository interpretation disciplined by the SCSI mechanism. It is not period SCSI philosophy.

---

## Explicit refusals

This evidence record does **not** support:

- `SCSI invented write-back caching`;
- `SCSI invented stable storage`;
- `GOOD always means cache-only completion`;
- `all SCSI devices enable write-back cache`;
- `SCSI-2 already had FUA_NV/SYNC_NV in 1994`;
- `all non-volatile SCSI cache is battery-backed`;
- `non-volatile cache = physical medium`;
- `non-volatile cache = unlimited shelf retention`;
- `FUA = global cache flush`;
- `SYNCHRONIZE CACHE = cache eviction`;
- `successful synchronization = protection from every later failure`;
- `SCSI FUA and NVMe FUA are historically identical`;
- `SCSI directly caused NVMe's later interface design`.

---

## Evidence status

**grounded**

The bounded historical core is independently supported by a period standard, manufacturer documentation, an official T10 proposal explaining the engineering problem, the subsequent SBC-2 final-draft text, and T10 version metadata.

Open work remains separate: pre-1994 forced-write/cache-flush genealogy; exact SBC-3 obsolescence/removal history for `SYNC_NV`; controller-specific non-volatile-cache hardware and fault testing; multi-initiator/order semantics; and full SCSI→SAS/NVMe interface genealogy.