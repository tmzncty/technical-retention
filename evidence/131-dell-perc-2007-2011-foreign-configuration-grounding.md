# Evidence 131 — Dell PERC 2007–2011 Foreign-Configuration and Preserved-Cache Grounding

## Purpose

This evidence note grounds Case 131's bounded claims about Dell PERC foreign configuration, controller re-admission, disk migration, and controller-local preserved write cache.

It deliberately distinguishes:

- **historical record** — what Dell's dated firmware documentation actually says;
- **later operational continuity** — what current/later Dell manuals say about the same family of concepts;
- **engineering reconstruction** — retention relations inferred from those behaviors;
- **unsupported history** — invention/origin claims not established by the inspected corpus.

No community post is required for the central claims.

---

## Source A — Dell PERC 6/i Integrated firmware 6.0.1-0080, A01

**Type:** `H/P` — vendor primary, dated product firmware release record.  
**Release date:** **20 November 2007**.  
**Dell Driver ID:** `D0CFD`.

**URL:**  
https://www.dell.com/support/home/en-us/drivers/DriversDetails?driverId=D0CFD

### Directly grounded statements

Dell's `Important Information` states that:

1. if all physical disks making up a virtual disk are removed, the RAID controller deletes the virtual disk;
2. if those disks are later reinserted, they are marked `foreign` and can be imported using a management application;
3. a physical disk carrying a foreign configuration cannot be immediately reused as a hot spare or member of a new virtual disk;
4. the foreign configuration must first be imported or cleared;
5. before virtual-disk migration, the source system must be powered off before disk removal to preserve the correct virtual-disk state;
6. import is restricted during RAID Level Migration / Capacity Expansion, and interruption can make data unavailable.

### Claim limits

This source proves:

> Dell documented foreign-configuration recovery behavior for PERC 6/i by 20 Nov 2007.

It does **not** prove:

- Dell invented foreign configuration in 2007;
- the exact on-disk metadata format;
- that every older PERC behaved identically;
- that any arbitrary disk set can be imported;
- that an imported array is payload-consistent.

---

## Source B — Dell PERC 6/E Adapter firmware 6.1.1-0047, A08

**Type:** `H/P` — vendor primary, dated product firmware release record.  
**Release date:** **6 December 2011**.  
**Dell Driver ID:** `TP43X`.

**URL:**  
https://www.dell.com/support/home/en-us/drivers/driversdetails?driverid=tp43x

### Directly grounded statements

The `Fixes & Enhancements` section says:

- the controller will preserve **uncommitted write cache** for virtual disks that become offline or are deleted because physical disks are missing;
- storage-management applications can provide detailed information on foreign configurations.

The `Important Information` section states:

1. removing all physical disks causes the controller to delete the virtual disk; reinserting them marks them foreign and permits import;
2. with write-back cache enabled, if some or all physical disks are removed, the controller preserves the virtual disk's write cache;
3. the controller flushes the preserved cache after physical disks are replaced and the foreign configuration is imported;
4. firmware update is blocked while cache is preserved;
5. foreign disks cannot be allocated to a new role until import or clear;
6. source-side power-off is required before virtual-disk migration;
7. RAID Level Migration / Capacity Expansion create import restrictions.

### Evidence consequence

Source B directly separates two state locations:

```text
member disks
    -> foreign configuration and persistent payload/parity embodiments

PERC controller
    -> uncommitted write-back cache that may be preserved while the disks are absent
```

This is enough to ground:

> `disk-resident foreign configuration ≠ controller-local uncommitted write cache`.

### Claim limits

The source describes cache preservation **on the controller that experienced the missing-disk episode**. It does not state that dirty cache trapped on a dead controller is transferred into a replacement controller.

Therefore the following remains unsupported and is explicitly rejected:

> `foreign import after controller replacement automatically recovers failed-controller dirty cache`.

---

## Source C — Dell OpenManage foreign-configuration operations

**Type:** `H/S` — later vendor operational documentation / continuity witness.

**URL:**  
https://www.dell.com/support/manuals/en-in/openmanage-server-administrator-v10.2.0.0/omss_10.2_ug_olh/foreign-configuration-operations?guid=guid-2082f2d8-2cd4-4878-a385-a389d4971061&lang=en-us

### Directly grounded statements

The documentation defines a foreign configuration as **data residing on physical disks that have been moved from one controller to another**. Virtual disks on those moved physical disks are treated as foreign configurations.

The operation provides a preview before import.

### Methodological use

This source gives later Dell vocabulary for the physical locus of the configuration relation. It supports the engineering phrase `disk-resident array configuration`.

It is **not** used to claim that every field documented in later OpenManage existed unchanged in the 2007 firmware.

---

## Source D — Dell current PERC replacement / foreign import guidance

**Type:** `H/S` — current vendor operational guidance.

**URL:**  
https://www.dell.com/support/kbdoc/en-us/000122457/how-to-import-a-foreign-configuration-in-the-raid-controller-using-the-system-setup-menu

### Directly grounded statements

Dell states that foreign configuration is detected when RAID metadata is not synchronized with the controller's current configuration. Examples include disks/virtual disks moved between systems or an array that went offline and returned.

The article says to use the import procedure when:

- a new PERC has been installed or replaced; and
- the original RAID configuration is expected to be intact and should be recovered.

It warns that importing at the wrong time can cause data loss and specifically says not to import a single foreign disk into an otherwise Online/Degraded active array; in that scenario, Dell directs the operator toward clearing that disk's foreign state and rebuilding.

### Evidence consequence

This grounds the present-day operational relation:

> controller replacement can leave enough disk-resident RAID metadata for a replacement PERC to detect and import the original configuration.

It does not prove transparent recovery, automatic currentness selection, or payload integrity.

---

## Source E — Dell iDRAC foreign-import member-sufficiency rules

**Type:** `H/S` — current vendor manual / continuity witness.

**URL:**  
https://www.dell.com/support/manuals/en-us/poweredge-xe9785l/idrac10_1.30.xx_ug/importing-or-auto-importing-foreign-configuration?guid=guid-9ecc96b6-8169-468a-ab6d-04e80169ab85&lang=en-us

### Directly grounded statements

Dell's manual says:

- a foreign configuration is data residing on physical disks moved from one controller to another;
- foreign configurations may be imported so virtual disks are not lost after physical-disk movement;
- import is allowed only for qualifying `Ready` / `Degraded` states or associated hot-spare cases;
- one side of a RAID 1 can be importable as `Degraded`;
- one member of an original three-disk RAID 5 is `Failed` and cannot be imported;
- the controller can detect a physical disk as `Foreign` because it contains all or some portion of a virtual disk or a hot-spare assignment.

### Evidence consequence

This grounds:

> `foreign configuration detected ≠ sufficient member state for import`.

and:

> `configuration knowledge ≠ data reconstructability`.

---

## Claim ledger

| ID | Claim | Label | Evidence | Strength / limit |
| --- | --- | --- | --- | --- |
| G-131.1 | PERC 6/i documentation dated 20-Nov-2007 records remove-all-disks → delete VD → reinsert → foreign → import. | `H/P` | A | strong direct product record |
| G-131.2 | Foreign disks require import or clear before ordinary reuse as new VD/hot-spare members. | `H/P` | A, B | direct, repeated |
| G-131.3 | Source-side power-off is required for documented virtual-disk migration to preserve correct VD state. | `H/P` | A, B | direct; bounded to documented path |
| G-131.4 | RLM/capacity-expansion interruption can block import and make data unavailable. | `H/P` | A, B | direct |
| G-131.5 | PERC 6/E A08 dated 06-Dec-2011 preserves uncommitted write cache when missing disks make a VD offline/deleted. | `H/P` | B | strong direct product record |
| G-131.6 | That preserved cache is flushed when disks return and the foreign configuration is imported. | `H/P` | B | direct |
| G-131.7 | Later Dell docs explicitly describe foreign configuration as data residing on physical disks moved between controllers. | `H/S` | C, E | later continuity; not 2007 field-layout proof |
| G-131.8 | Current Dell guidance explicitly includes new/replacement PERC recovery as a foreign-import use case. | `H/S` | D | current operational continuity |
| G-131.9 | Foreign metadata detection does not ensure an importable member set. | `H/S`, `E` | E | direct examples + reconstruction |
| G-131.10 | Disk-resident array configuration is distinct from the controller's current admitted configuration. | `E` | A, C, D | reconstruction from foreign/admission behavior |
| G-131.11 | Disk-resident configuration is distinct from controller-local uncommitted write cache. | `E` | B | unusually strong because source names both |
| G-131.12 | Successful configuration import is not itself RAID rebuild or integrity verification. | `E` | D, E + Cases 17/102 | bounded cross-case reconstruction |
| G-131.13 | Controller replacement recovery does not prove recovery of dirty cache from the failed controller. | `X`, `E` | B, D | explicit anti-overclaim |
| G-131.14 | 20-Nov-2007 is a direct Dell documentation floor, not invention priority. | `X` | A | chronology guardrail |
| G-131.15 | PERC foreign-config import and ZFS vdev-label/uberblock import are functional analogies only. | `A` | Case 128 | no genealogy claim |
| G-131.16 | PERC foreign-config recovery and PERC Patrol Read/Consistency Check operate at different phases: admission vs maintenance. | `A`, `E` | Case 102 | cross-case separation |

---

## March 2011 H800 transportable-cache deepening

### Source F — Dell PERC H700 and H800 Technical Guide, Revision 3

**Type:** `H/P` — Dell-hosted vendor primary.
**Revision:** **March 2011**.
**URL:** https://i.dell.com/sites/csdocuments/shared-content_data-sheets_documents/en/perc-technical-guidebook.pdf

Directly inspected points:

- the H800 overview lists a standard 512 MB **transportable battery backup unit (TBBU)** and transportable 512 MB / 1 GB nonvolatile-cache options;
- §4.5.1 distinguishes battery-held cache from the NV-cache path in which battery energy transfers cache contents to flash on a power cycle, with retention stated as up to ten years;
- §4.5.7.1 defines the TBBU as a cache-memory module with an integrated battery pack that enables moving the cache module with its battery into a new controller;
- the same section describes H700 BBU separately, blocking an automatic projection of H800 transportability onto every PERC cache design.

### Source G — Dell PERC H700 and H800 User's Guide, March 2011 Rev. A02

**Type:** `H/P*` — Dell-authored primary manual, with a preservation/provenance caveat.
**Revision:** **March 2011, Rev. A02**.
**Dell support index:** https://www.dell.com/support/product-details/en-us/product/poweredge-rc-h800/resources/manuals
**Surviving page-text mirrors checked:**
- https://www.manualshelf.com/manual/dell/poweredge-raid-controller-h700/instruction-manual-english.html
- https://dell.manymanuals.com/computer-hardware/poweredge-raid-controller-h800/user-manual-11966/37
- https://dell.manymanuals.com/computer-hardware/poweredge-raid-controller-h800/user-manual-11966/63

The current Dell support page still indexes the User's Guide but did not expose a stable directly fetchable copy in this research round. The surviving Dell-authored manual text records:

- `Cache Data Recovery` (p. 37): after a PERC H800 card failure, the complete TBBU/TNVC can be transferred to a new PERC H800 without putting preserved cache data at risk;
- p. 63: if the controller fails after a power failure, the TBBU/TNVC can be moved to a replacement controller; the replacement should have no prior configuration; after original storage enclosures are reconnected, the replacement controller flushes the retained cache to the virtual disks.

This is stronger than merely inferring portability from the module name. It directly documents a failed-controller recovery procedure, but only for the bounded H800 path.

### Claim-ledger additions

| ID | Claim | Label | Evidence | Strength / limit |
| --- | --- | --- | --- | --- |
| G-131.17 | By March 2011 Dell documented PERC H800 TBBU/TNVC cache options as transportable state carriers. | `H/P` | F | strong Dell-hosted product record |
| G-131.18 | H800 TBBU transportability means controller-local cache state need not be physically inseparable from the controller card. | `E` | F | bounded reconstruction |
| G-131.19 | The H800 nonvolatile-cache path can transfer cached data to flash during a power cycle rather than merely holding DRAM alive continuously. | `H/P` | F | direct Dell-hosted mechanism statement |
| G-131.20 | The March-2011 H800 User's Guide explicitly documents moving a surviving TBBU/TNVC to a replacement H800 after controller-card failure. | `H/P*` | G | Dell-authored manual; mirrored page text |
| G-131.21 | The documented replacement path requires another PERC H800 with no prior configuration and reconnecting the original storage enclosures before cache flush. | `H/P*` | G | bounded procedure, not universal migration |
| G-131.22 | Controller-card failure need not imply dirty-cache loss when the separate retained-cache carrier survives and the documented transplant path remains admissible. | `E` | F, G | bounded to H800 TBBU/TNVC |
| G-131.23 | Transportable cache survival is not the same event as commitment of those pending writes to member disks; the replacement controller still has to flush them. | `H/P*`, `E` | G | direct sequence + reconstruction |
| G-131.24 | Foreign-configuration import and cache-module transfer are separate recovery relations even when one recovery episode may require both disk-resident configuration and pending cache state. | `E` | A-E, F-G | cross-source decomposition |
| G-131.25 | H800 transportability does not establish a universal PERC, cross-generation, or cross-vendor cache-transplant contract. | `X` | F, G | anti-overclaim |
| G-131.26 | March 2011 is a directly inspected Dell product-documentation floor for this H800 portability path, not an invention-priority claim for transportable RAID cache. | `X` | F, G | chronology guardrail |

## Rejected / unsupported claims

Do **not** write any of the following from this evidence set:

- "Dell invented disk-resident RAID metadata in 2007."
- "Foreign configuration is the same thing as user data."
- "If foreign metadata survives, the array is necessarily importable."
- "Import reconstructs missing payload."
- "Import verifies parity consistency."
- "Every PERC controller replacement preserves every dirty write that was on the failed controller."
- "The H800 TBBU/TNVC recovery path works after destruction, loss, or corruption of the cache module itself."
- "A PERC H800 TBBU/TNVC can be transplanted into arbitrary later PERC generations or third-party controllers."
- "Clear Foreign Configuration is equivalent to secure sanitization."
- "PERC foreign metadata and ZFS labels are the same mechanism."
- "Later OpenManage field semantics can be projected unchanged into PERC 6/i A01."

---

## Related cases

- [Case 17 — RAID parity reconstruction](../cases/17-raid-parity-reconstruction-degraded-repair.md): reconstructability after member failure.
- [Case 87 — SCSI write-back cache / FUA / SYNCHRONIZE CACHE](../cases/87-scsi2-writeback-cache-fua-synchronize-cache.md): cached currentness vs media commitment.
- [Case 88 — Linux MD RAID5 Partial Parity Log](../cases/88-linux-md-raid5-partial-parity-log.md): retained parity-update intent, not controller migration metadata.
- [Case 95 — ZFS RAID-Z dynamic-stripe write-hole](../cases/95-zfs-raidz-dynamic-stripe-write-hole.md): write-hole avoidance, not controller config import.
- [Case 102 — PERC / MegaRAID Patrol Read and Consistency Check](../cases/102-perc-megaraid-patrol-read-consistency-boundary.md): maintenance after array admission.
- [Case 128 — ZFS vdev labels and uberblocks](../cases/128-zfs-vdev-label-uberblock-import-root-recovery.md): functional restart-metadata analogy only.

## Related-repository check

A fresh search of `tmzncty/computing-archaeology` for PERC foreign configuration, controller replacement, and RAID metadata found no dedicated case to reuse. Broad hardware-RAID metadata genealogy and controller architecture remain better suited to that repository if developed.
