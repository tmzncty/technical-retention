# Dell PERC Foreign Configuration: Retained Array Topology Across Controller Replacement

**Status:** `grounded`

## Scope

- **Object / system:** Dell PowerEdge RAID Controller (PERC), bounded historically by PERC 6/i firmware released **20 November 2007** and PERC 6/E firmware released **6 December 2011**, with later Dell management documentation used only as continuity / operational witnesses.
- **Retention question:** what array-defining state can remain on the member disks when the controller's current configuration disappears or no longer admits those disks, and what separate controller-local state can still prevent transparent recovery?
- **Roadmap role:** advances `controller failure` at the RAID configuration / admissibility layer.
- **Related-repository boundary:** a fresh search of `tmzncty/computing-archaeology` found no dedicated PERC foreign-configuration / controller-replacement case to reuse. Broad RAID-controller history, MegaRAID genealogy, NVRAM-controller architecture, and vendor-family archaeology belong there if developed.

This case does **not** claim that Dell invented disk-resident RAID metadata, controller migration, foreign-configuration import, or battery-backed RAID cache. The earliest directly inspected Dell record here is a **documentation floor**, not an invention date.

The project terms `array-topology witness`, `controller admissibility`, `configuration re-admission`, `controller-local pending payload`, and `recovery relation` below are **engineering reconstructions**, not Dell historical vocabulary.

---

## Historical vocabulary

The inspected Dell sources directly use:

- `virtual disk`;
- `physical disk`;
- `foreign`;
- `foreign configuration`;
- `import`;
- `clear`;
- `virtual disk migration`;
- `write-back cache`;
- `preserve the virtual disk's write cache`;
- `flush the preserved cache`;
- `RAID Level Migration`;
- `Capacity Expansion`;
- `Ready`, `Degraded`, `Failed`, and `Offline` in later operational documentation.

Do not silently normalize these into ZFS `vdev labels`, filesystem superblocks, generic `metadata`, or a universal cluster-membership protocol. Functional comparisons are useful; historical identity is not established.

---

## Historical record

### H/P — PERC 6/i firmware documentation shows disk-carried foreign configuration by 20 November 2007

Dell's PERC 6/i Integrated firmware release `6.0.1-0080, A01`, dated **20 November 2007**, says that if all physical disks making up a virtual disk are removed, the RAID controller deletes the virtual disk from its current configuration. If those disks are later reinserted, they are marked `foreign` and can be imported with a management application.

The same record says disks containing a foreign configuration cannot immediately be reused as hot spares or members of a new virtual disk; the foreign configuration must first be **imported or cleared**.

This establishes a bounded historical fact:

> By November 2007, Dell documented a PERC regime in which array-defining configuration could remain associated with the physical disks after the controller had removed the virtual disk from its current admitted configuration.

It does **not** establish the first use of such a design in RAID history.

**Primary anchor:** Dell, _PERC 6/i Integrated Firmware v6.0.1-0080, A01_, release date 20 Nov 2007, `Important Information`.

### H/P — migration already required a controlled source-side shutdown

The same 2007 release note warns that, before virtual-disk migration, the source system must be powered off before removing the physical disks **to preserve the correct virtual disk state**. It also warns not to interrupt RAID-level migration or capacity expansion because doing so can prevent import and make data unavailable.

This blocks a simplistic model in which "the disks carry the config" means "disk movement is always self-describing and transaction-free."

> **disk-resident configuration survival ≠ arbitrary hot-migration safety.**

There are still transition states whose interruption can make the retained configuration inadmissible or unusable.

### H/P — the 2011 PERC 6/E release separates foreign configuration from preserved dirty write cache

Dell's PERC 6/E firmware `6.1.1-0047, A08`, released **6 December 2011**, adds a much sharper retention boundary.

Its fixes say the controller preserves **uncommitted write cache** for virtual disks that become offline or deleted because physical disks are missing. The `Important Information` section then states that, when write-back cache is enabled and disks are removed, the controller preserves the virtual disk's write cache and flushes that preserved cache when the disks return and the foreign configuration is imported. Firmware update is blocked while such cache is preserved.

Thus the source itself exposes two retained state classes:

```text
physical disks
    -> foreign array configuration / payload embodiments

controller
    -> preserved uncommitted write cache
```

They participate in one recovery episode but are not the same thing.

> **disk-resident foreign configuration ≠ controller-local uncommitted write cache.**

### H/P — 2011 still treats import and clear as distinct state transitions

The 2011 release repeats that a physical disk carrying a foreign configuration is unavailable for immediate new allocation until the foreign configuration is either imported or cleared. It also repeats the source-shutdown requirement for virtual-disk migration and the restrictions around RAID-level migration / capacity expansion.

So `foreign` is not merely an informational label. It changes what operations the controller admits.

> **configuration detection ≠ configuration admission.**

and:

> **import ≠ clear.**

The first tries to re-establish the old virtual-disk relation. The second removes that foreign relation so the disks can be used under a different configuration path.

### H/S — later Dell management documentation explicitly locates foreign configuration on physical disks

Current Dell OpenManage Storage Management documentation defines a foreign configuration as **data residing on physical disks that have been moved from one controller to another** and describes the virtual disks on those moved physical disks as foreign configurations.

This later documentation is a continuity witness for the disk-resident location of the configuration relation. It is not projected backward as proof of every PERC 6 on-disk field or encoding.

### H/S — later import rules make admissibility conditional on a sufficiently complete disk set

Current Dell iDRAC documentation says a foreign configuration can be imported only under particular virtual-disk states and gives concrete examples: one side of a RAID 1 mirror may be importable in `Degraded` state, while one disk from an original three-disk RAID 5 is `Failed` and cannot be imported.

That is important because it separates:

```text
foreign metadata detected
    !=
enough member state survives for an admissible virtual disk
```

The controller can know what the disks claim to be while still refusing to reconstruct a usable array.

### H/S — current Dell recovery guidance explicitly includes controller replacement

Dell's current PowerEdge foreign-configuration recovery article says to use the procedure after **installing or replacing a new PERC** when the original RAID configuration is expected to be intact and should be recovered. The same article warns that importing at the wrong time may result in data loss and distinguishes a whole offline/failed foreign array from a single foreign disk in an otherwise active RAID.

This is operational continuity, not evidence that modern PERC firmware is identical to PERC 6.

It does establish the retention pattern that motivates this case:

> a failed/replaced controller need not imply that the array topology has vanished, because a later compatible controller may rediscover and import disk-resident configuration.

But the recovery is conditional and requires operator judgment.

---

## Retained state classes

Case 131 requires at least seven different state classes.

### 1. User payload embodiments

The member disks contain the data/parity blocks from which the virtual disk's payload is served or reconstructed.

### 2. Disk-resident array configuration

Dell's foreign-configuration terminology describes retained configuration on physical disks. This is the relation by which the disks can be recognized as belonging to virtual disks / hot-spare assignments after movement or controller reconfiguration.

### 3. Controller-current admitted configuration

The controller maintains a current configuration against which attached disks are interpreted. A disk can be physically present yet appear `foreign` because its retained configuration is not synchronized with that current controller state.

### 4. Virtual-disk health / member sufficiency

Even when configuration is recognized, the surviving member set can be `Ready`, `Degraded`, `Failed`, or otherwise not importable. Topology knowledge does not manufacture missing data.

### 5. Controller-local uncommitted write cache

The 2011 PERC 6/E record explicitly preserves pending write-back data in the controller when disks disappear. This is current payload state that may not yet have reached the member disks.

### 6. Transition state

RAID-level migration and capacity expansion create in-progress relations that Dell warns must not be interrupted if importability and data availability are to be preserved.

### 7. Operator / management decision state

`preview`, `import`, `clear`, and recovery choices determine which retained configuration relation becomes authoritative. The management act is not the same as the physical survival of the disks.

---

## Retention and recovery transitions

### Foreign-configuration path

```text
admitted virtual disk
    ↓ remove / move member disks
controller current config no longer admits the VD
    ↓
disk-resident configuration still survives
    ↓ controller detects it as foreign
foreign configuration detected
    ↓ preview / qualification
importable?  ── no ──> unavailable / degraded recovery work
    │
   yes
    ↓
configuration re-admitted
    ↓
virtual disk service can resume subject to member/data health
```

Engineering reconstruction:

> **payload/media survival ≠ array-configuration admissibility.**

All member media may still exist while the current controller refuses ordinary virtual-disk service until the retained configuration is qualified and imported.

### Preserved-cache path

The 2011 PERC 6/E record adds another relation:

```text
write accepted into controller write-back cache
    ↓
member disks disappear / VD becomes offline
    ↓
controller preserves uncommitted cache
    ↓
member disks return + foreign config imported
    ↓
preserved cache is flushed
```

This is not merely foreign-configuration recovery. It is a pending-payload durability problem coupled to configuration recovery.

> **configuration re-admission ≠ pending-write commitment.**

---

## Controller failure boundary

This case advances the roadmap item `controller failure`, but only at one layer.

A controller can fail or be replaced while disk-resident array configuration survives. A compatible replacement controller may be able to import that configuration and restore access.

However:

> **controller failure ≠ automatic payload loss.**

does **not** imply:

> **controller replacement ≡ transparent continuation.**

A replacement path still depends on compatible interpretation, sufficient member disks, acceptable array state, and — for encrypted configurations — any required key authority.

Most importantly, the 2011 preserved-cache evidence belongs to the **same controller retaining cache across missing-disk episodes**. The inspected sources do not prove that dirty cache trapped on a failed old controller is magically transferred into a replacement controller.

Therefore:

> **foreign-configuration recovery after controller replacement ≠ recovery of dirty cache from the failed controller.**

That failed-controller dirty-cache question remains open.

---

## Import, reconstruction, and integrity are separate

A foreign-configuration import tells the controller to re-admit an array relation. It does not by itself prove every payload block is intact.

Cases 17, 88, 95, and 102 already show different RAID obligations: parity reconstructability, partial-parity logging, write-hole avoidance, and patrol/consistency checking. Case 131 must not collapse those into import.

> **configuration import ≠ RAID rebuild.**

> **configuration import ≠ consistency check.**

> **successful import ≠ end-to-end payload-integrity verification.**

The current Dell guidance itself warns that an import chosen at the wrong time can cause corruption, which is enough to reject "import succeeded, therefore the newest correct state was proven" as a general rule.

---

## Cross-case comparison

### Case 102 — PERC Patrol Read / Consistency Check

Case 102 owns maintenance on an already admitted PERC array: media verification and RAID consistency checking.

Case 131 begins earlier in the recovery path: **which disk-carried configuration is admitted as the virtual disk at all?**

> **array admission ≠ array integrity maintenance.**

A controller can recognize/import a configuration and still require later consistency or media verification.

### Case 128 — ZFS vdev labels and uberblocks

Case 128 and Case 131 share a useful functional pattern: retained member-media metadata can outlive volatile/controller-local control state and later help reconstruct a service relation.

But their mechanisms differ sharply:

- ZFS software interprets vdev labels and qualifies an uberblock/root;
- PERC firmware/management logic detects and imports controller-specific foreign configurations.

No PERC ↔ ZFS genealogy is asserted.

> **functional restart-metadata analogy ≠ common mechanism.**

### Case 87 — SCSI write-back cache

Case 87 distinguishes volatile/nonvolatile cache residence from physical-medium commitment. Case 131 adds a RAID-controller example in which Dell explicitly preserves uncommitted write cache while a virtual disk is unavailable.

The comparison is functional:

> **controller-local cached currentness ≠ disk-resident configuration currentness.**

It does not establish a direct SCSI-standard lineage for PERC's implementation.

### Case 17 — parity reconstruction

Case 17 owns the algebraic/repair question. Foreign-configuration metadata can describe an array that is too incomplete to reconstruct or serve.

> **topology knowledge ≠ reconstructability.**

---

## Prior-art / genealogy boundary

This case makes no invention-priority claim for:

- RAID metadata on member disks;
- controller-replacement recovery;
- battery-backed RAID write cache;
- MegaRAID foreign configuration;
- disk migration.

The earliest directly inspected Dell source in this case is the 20 November 2007 PERC 6/i firmware record. It is a **directly evidenced Dell floor**, not a global historical origin.

A companion-repository search found no existing `computing-archaeology` PERC foreign-configuration case. A future genealogy should examine earlier PERC / MegaRAID generations, other hardware RAID metadata formats, controller NVRAM designs, and cross-controller migration using primary manuals rather than retroactively assigning PERC 6 vocabulary to older systems.

---

## Engineering reconstruction

The bounded evidence supports the following project-level relations:

```text
physical disk survival
    != virtual-disk service availability

disk-resident array configuration
    != controller-current admitted configuration

foreign configuration detected
    != foreign configuration importable

configuration import
    != RAID rebuild
    != consistency verification

disk-resident configuration
    != controller-local uncommitted write cache

controller replacement recovery
    != failed-controller dirty-cache recovery

import
    != clear

controller failure
    != automatic physical erasure
```

These are analytical separations supported by the Dell records. They are not Dell's own philosophical claims.

---

## Philosophical interpretation

**I — optional interpretation.**

Case 131 is a useful example of retention as **continued admissible relation**, not merely continued bits. A disk can retain payload and configuration while ceasing to be an admitted member of the controller's current virtual disk. Recovery then consists partly of re-establishing an interpretive/authority relation between surviving media and a controller.

That interpretation must remain secondary. The historical evidence establishes foreign configuration, import/clear behavior, migration constraints, and preserved cache; it does not state a theory of memory or identity.

---

## Failure / forgetting modes

Distinct failure modes include:

1. physical member loss or unreadability;
2. insufficient surviving members for import/reconstruction;
3. configuration recognized as foreign but not imported;
4. wrong import decision against a still-active array;
5. foreign configuration cleared instead of imported;
6. controller replacement with incompatible firmware/controller semantics;
7. interrupted RAID-level migration or capacity expansion;
8. loss of controller-local uncommitted write cache before it reaches member media;
9. recovery of topology without proof of payload consistency;
10. encrypted configuration whose key authority is unavailable.

These modes occur at different layers and should not be reported as one generic `RAID metadata loss`.

---

## Sources

### Primary / contemporary Dell records

1. Dell, **PERC 6/i Integrated Firmware v6.0.1-0080, A01**, released 20 Nov 2007. `Important Information` documents remove/reinsert → `foreign` → import/clear, migration shutdown, and RLM/capacity-expansion restrictions.  
   https://www.dell.com/support/home/en-us/drivers/DriversDetails?driverId=D0CFD

2. Dell, **PERC 6/E Adapter Firmware v6.1.1-0047, A08**, released 06 Dec 2011. `Fixes & Enhancements` and `Important Information` document preserved uncommitted write cache and its flush after disk return plus foreign import.  
   https://www.dell.com/support/home/en-us/drivers/driversdetails?driverid=tp43x

### Later Dell operational / continuity witnesses

3. Dell OpenManage Server Administrator Storage Management, **Foreign Configuration Operations** — defines foreign configuration as data residing on physical disks moved between controllers.  
   https://www.dell.com/support/manuals/en-in/openmanage-server-administrator-v10.2.0.0/omss_10.2_ug_olh/foreign-configuration-operations?guid=guid-2082f2d8-2cd4-4878-a385-a389d4971061&lang=en-us

4. Dell, **PowerEdge: How to Import a Foreign Configuration in the RAID Controller Using the System Setup Menu** — current operational recovery guidance, including PERC replacement and warnings about unsafe import.  
   https://www.dell.com/support/kbdoc/en-us/000122457/how-to-import-a-foreign-configuration-in-the-raid-controller-using-the-system-setup-menu

5. Dell iDRAC10 User's Guide, **Importing or auto importing foreign configuration** — current member-sufficiency/import rules and `Ready` / `Degraded` / `Failed` examples.  
   https://www.dell.com/support/manuals/en-us/poweredge-xe9785l/idrac10_1.30.xx_ug/importing-or-auto-importing-foreign-configuration?guid=guid-9ecc96b6-8169-468a-ab6d-04e80169ab85&lang=en-us

## Evidence record

See [Evidence 131 — Dell PERC 2007–2011 foreign-configuration and preserved-cache grounding](../evidence/131-dell-perc-2007-2011-foreign-configuration-grounding.md).
