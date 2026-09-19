# Dell PERC Foreign Configuration: Retained Array Topology Across Controller Replacement

**Status:** `grounded`

## Scope

- **Object / system:** Dell PowerEdge RAID Controller (PERC), bounded historically by PERC 6/i firmware released **20 November 2007**, the Dell-authored PERC 6/i / PERC 6/E / CERC 6/i User's Guide working copy dated **24 June 2009**, the PERC H700/H800 documentation set revised **March 2011**, PERC 6/E firmware released **6 December 2011**, and the Dell-hosted H310/H710/H710P/H810 User's Guide Rev. A02 (**March 2013**) for later operation-semantics continuity.
- **Retention question:** what array-defining state can remain on the member disks when the controller's current configuration disappears or no longer admits those disks; under what bounded hardware design can pending controller-cache state itself survive a controller-card failure and move to a replacement controller; and what exactly is retired when an operator clears rather than imports a foreign configuration?
- **Roadmap role:** advances `controller failure` at the RAID configuration / admissibility layer.
- **Related-repository boundary:** a fresh search of `tmzncty/computing-archaeology` found no dedicated PERC foreign-configuration / controller-replacement case to reuse. Broad RAID-controller history, MegaRAID genealogy, NVRAM-controller architecture, earlier foreign-metadata prior art, and vendor-family archaeology belong there if developed.

This case does **not** claim that Dell invented disk-resident RAID metadata, controller migration, foreign-configuration import, battery-backed RAID cache, or secure erase. The earliest directly inspected Dell record here is a **documentation floor**, not an invention date.

The project terms `array-topology witness`, `controller admissibility`, `configuration re-admission`, `configuration retirement`, `controller-local pending payload`, and `recovery relation` below are **engineering reconstructions**, not Dell historical vocabulary.

---

## Historical vocabulary

The inspected Dell sources directly use:

- `virtual disk`;
- `physical disk`;
- `foreign`;
- `foreign configuration`;
- `foreign metadata`;
- `import`;
- `clear`;
- `Ready`;
- `Rebuild`;
- `Consistency Check`;
- `Format`;
- `Initialization`;
- `pinned cache`;
- `discard`;
- `Instant Secure Erase`;
- `virtual disk migration`;
- `write-back cache`;
- `preserve the virtual disk's write cache`;
- `flush the preserved cache`;
- `RAID Level Migration`;
- `Capacity Expansion`;
- `Degraded`, `Failed`, and `Offline` in later operational documentation.

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

### H/P* — the June-2009 PERC 6 manual names `foreign metadata` and separates preview from admission

The Dell-authored PERC 6/i, PERC 6/E and CERC 6/i User's Guide working copy `Dell_PERC6.2_UG.book`, whose inspected page footers are dated **24 June 2009**, explains the POST message `Foreign configuration(s) found on adapter` by saying that controller firmware detects a physical disk with existing **foreign metadata**, marks the disk `foreign`, and raises an alert.

The same manual's `Foreign Configuration View` lets the operator inspect disk groups, virtual disks, physical disks, space allocation, and hot spares before deciding whether to import or clear.

That creates a direct historical separation:

```text
foreign metadata survives
    -> controller detects foreign state
    -> operator can preview
    != configuration already imported
```

The exact binary on-disk format remains out of scope. `Foreign metadata` is Dell's direct vocabulary here; `array-topology witness` remains this project's analytical term.

### H/P* — PERC 6 `Clear` deletes the foreign relation; it is not the manual's `Format` or `Initialization`

Across the PERC 6 foreign-configuration procedures, Dell repeatedly contrasts:

- `Import` — import/merge the foreign configuration into the controller's configuration;
- `Clear` — delete the foreign configuration from the reinserted disks.

The troubleshooting table gives a concrete postcondition: clearing the foreign configuration puts the physical disk into `Ready` state and may lead to data loss.

The same manual separately defines:

- `Format` as writing a specific value to **all data fields on a physical disk**;
- `Initialization` as writing zeros to virtual-disk data fields and generating parity, explicitly erasing previous data.

Therefore the manual itself supports:

```text
Clear Foreign Configuration
    != Format
    != virtual-disk Initialization
```

and, more carefully:

> **configuration retirement can destroy ordinary controller recoverability without itself proving whole-medium overwrite.**

This is not a forensic-recovery claim. The manual does not prove that payload sectors are untouched after every clear; it proves that `Clear`, `Format`, and `Initialization` are separately named and separately described operations.

### H/P* — import, rebuild, and consistency verification are different phases

The 2009 manual describes foreign-import cases in which reinserted drives are imported and then automatically rebuilt. It then recommends starting a consistency check after rebuild completion to ensure virtual-disk data integrity.

Thus:

```text
Import
    -> possible Rebuild
    -> Consistency Check
```

> **configuration import ≠ RAID rebuild ≠ consistency verification.**

The manual also warns that drive state can change between the foreign scan and actual import, and it excludes failed/offline drives from the documented import path. A visible foreign configuration is therefore not a guarantee that the configuration remains importable.

### H/P* — foreign-config clear and pinned-cache discard retire different retained objects

Immediately after the foreign-configuration procedures, the same PERC 6 guide describes `pinned cache`: dirty cache retained when a virtual disk becomes offline or is deleted because physical disks are missing.

Dell says this cache remains until the virtual disk is imported or the cache is discarded, and warns the operator to import the foreign configuration before discarding preserved cache because data belonging to that foreign configuration may otherwise be lost.

This directly separates:

```text
disk side
    foreign metadata / foreign configuration
        -> Import or Clear

controller side
    preserved dirty / pinned cache
        -> later flush or Discard
```

> **foreign-configuration Clear ≠ preserved-cache Discard.**

Configuration retirement and pending-payload retirement are separate forgetting operations even when they participate in one recovery episode.

### H/P — March 2011 PERC H800 makes a transportable failed-controller cache path explicit

Dell's _PERC H700 and H800 Technical Guide_, Revision 3 (**March 2011**), distinguishes the H800 from the H700 at the cache-carrier layer. The H800 cache options include a **512 MB transportable battery backup unit (TBBU)** and transportable 512 MB / 1 GB nonvolatile-cache options. Section 4.5.7.1 defines the TBBU as a cache-memory module with an integrated battery pack that can be transported into a new controller. Section 4.5.1 separately states that the nonvolatile-cache option uses battery energy to transfer cache contents to flash during a power cycle, with the guide specifying retention for up to ten years.

The Dell-authored _PERC H700 and H800 User's Guide_, March 2011 Rev. A02, makes the controller-failure use case explicit. Its `Cache Data Recovery` section says that after a **PERC H800 card failure** the complete TBBU/TNVC module can be moved to a new PERC H800 without putting preserved cache data at risk. Its transfer procedure further constrains the path: the replacement is another PERC H800 with no prior configuration, the original storage enclosures are reconnected, and the replacement controller then flushes the retained cache to the virtual disks.

The current Dell H800 support page still indexes this Dell User's Guide; the exact March-2011 page text used here survives on third-party mirrors because Dell's present support front end did not yield a stable directly fetchable copy during this research round. The controller-family design claim does **not** depend solely on that mirror: Dell's own still-hosted March-2011 Technical Guide independently establishes the transportable H800 cache module and the cache-to-flash power-loss path.

This changes the earlier open boundary in one important but narrow way:

> **controller card failure ≠ mandatory loss of controller-local dirty state, if the retained cache carrier itself survives and the documented H800 transplant conditions are met.**

It also requires a finer location distinction:

> **controller-local state ≠ state physically inseparable from the controller card.**

For the H800 TBBU/TNVC path, pending writes are controller-local in the protocol/ownership sense but can inhabit a removable state carrier that outlives the failed controller card.

The evidence does **not** license a universal PERC claim. It does not show that every H700/H800 cache option is transportable, that a destroyed/corrupt TBBU/TNVC can be recovered, that arbitrary later PERC generations accept the module, or that cache already committed to member disks is still only cache-resident.

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

### H/P — the March-2013 secured-foreign path makes physical-erasure semantics context-dependent

Dell's directly hosted _PowerEdge RAID Controller H310, H710, H710P, and H810 User's Guide_, Rev. A02 (**March 2013**), independently preserves the `Foreign View -> Import/Clear -> possible Rebuild -> Consistency Check` separation.

More importantly, the secured-foreign section supplies an explicit exception to any universal statement that `Clear` is "only metadata":

- `Import` and `Clear` remain the high-level actions;
- to **Clear** a foreign configuration secured with a different security key, Dell says **Instant Secure Erase** is required;
- Dell defines Instant Secure Erase as permanently erasing all data on an encryption-capable physical disk and resetting security attributes;
- a secured foreign disk with an unavailable passphrase remains inaccessible until the appropriate passphrase is supplied or the disk is instant-secure-erased.

The correct boundary is therefore contextual:

```text
ordinary foreign-config Clear semantics
    -> delete foreign configuration relation
    != by itself evidence of whole-medium erase

secured foreign config + different/unavailable key
    -> Clear path requires Instant Secure Erase
    -> permanent data erase + security-attribute reset
```

> **the label `Clear` alone does not determine physical-erasure semantics; security context and the concrete execution path matter.**

This blocks both overclaims: `Clear = sanitization` and `Clear never erases payload`.

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

Case 131 requires at least eight different state classes.

### 1. User payload embodiments

The member disks contain the data/parity blocks from which the virtual disk's payload is served or reconstructed.

### 2. Disk-resident array configuration

Dell's foreign-configuration terminology describes retained configuration on physical disks. The 2009 guide directly calls the detected object `foreign metadata`. This state helps describe virtual disks / hot-spare assignments after movement or controller reconfiguration.

### 3. Controller-current admitted configuration

The controller maintains a current configuration against which attached disks are interpreted. A disk can be physically present yet appear `foreign` because its retained configuration is not synchronized with that current controller state.

### 4. Virtual-disk health / member sufficiency

Even when configuration is recognized, the surviving member set can be `Ready`, `Degraded`, `Failed`, or otherwise not importable. Topology knowledge does not manufacture missing data.

### 5. Controller-local uncommitted write cache

The 2011 PERC 6/E record explicitly preserves pending write-back data in the controller when disks disappear. The 2009 manual names the related retained object `pinned cache`. This is current payload state that may not yet have reached the member disks.

### 6. Transition state

RAID-level migration and capacity expansion create in-progress relations that Dell warns must not be interrupted if importability and data availability are to be preserved.

### 7. Operator / management decision state

`preview`, `import`, `clear`, cache `discard`, and recovery choices determine which retained configuration/pending-payload relation becomes authoritative or is retired. The management act is not the same as physical survival of the disks.

### 8. Key / security authority

For secured foreign configurations, the controller may additionally require the appropriate security key/passphrase before import. In the documented March-2013 different-key clear path, Instant Secure Erase becomes an additional erasure gate.

Thus:

> **configuration authority ≠ key authority ≠ payload-erasure authority.**

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

### Configuration-retirement path

The 2009 PERC 6 manual adds the inverse transition:

```text
foreign metadata detected
    ↓
operator chooses Clear
    ↓
foreign configuration deleted from reinserted disk(s)
    ↓
physical disk can enter Ready state
    ↓
new configuration / allocation path becomes possible
```

This supports:

> **old relation retired ≠ old payload proven physically erased.**

But the later secured-foreign path adds:

```text
foreign configuration protected by different/unavailable key
    ↓ operator chooses Clear
Instant Secure Erase required
    ↓
permanent data erase + security-attribute reset
```

So the physical consequence of a high-level `Clear` request is context-dependent.

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

The 2009 manual's separate `Discard` action also establishes:

> **foreign-config Clear ≠ pinned-cache Discard.**

---

## Controller failure boundary

This case advances the roadmap item `controller failure`, but only at one layer.

A controller can fail or be replaced while disk-resident array configuration survives. A compatible replacement controller may be able to import that configuration and restore access.

However:

> **controller failure ≠ automatic payload loss.**

does **not** imply:

> **controller replacement ≡ transparent continuation.**

A replacement path still depends on compatible interpretation, sufficient member disks, acceptable array state, and — for encrypted configurations — any required key authority.

The PERC 6/E preserved-cache evidence still belongs to the **same controller retaining cache across missing-disk episodes** and, by itself, does not prove failed-card cache transfer. The March-2011 H800 material supplies a separate bounded counterexample: if the TBBU/TNVC survives, Dell documents moving that cache carrier to a replacement H800 and then flushing the retained cache to the virtual disks.

Therefore the stronger boundary is now:

> **foreign-configuration recovery after controller replacement ≠ failed-controller dirty-cache recovery by itself.**

but also:

> **failed controller card ≠ failed retained-cache carrier.**

The H800 path composes two independently retained state transports: member disks can carry array configuration/payload embodiments, while TBBU/TNVC can carry pending write state. Recovery completeness can depend on both. Failed or corrupt cache modules, nontransportable controller designs, cross-generation compatibility, controller-NVRAM corruption, independent fault injection, and encrypted-key loss remain open.

---

## Import, reconstruction, and integrity are separate

A foreign-configuration import tells the controller to re-admit an array relation. It does not by itself prove every payload block is intact.

Cases 17, 88, 95, and 102 already show different RAID obligations: parity reconstructability, partial-parity logging, write-hole avoidance, and patrol/consistency checking. Case 131 must not collapse those into import.

The 2009 and 2013 PERC manuals make this separation especially concrete:

```text
Import
    -> possible Rebuild
    -> Consistency Check
```

> **configuration import ≠ RAID rebuild.**

> **configuration import ≠ consistency check.**

> **successful import ≠ end-to-end payload-integrity verification.**

The current Dell guidance itself warns that an import chosen at the wrong time can cause corruption, which is enough to reject "import succeeded, therefore the newest correct state was proven" as a general rule.

---

## Clear, reuse, and sanitization are separate

The PERC documentation now supports a more precise forgetting boundary than the earlier case text.

For the ordinary PERC 6 foreign-clear path:

```text
Clear foreign configuration
    -> delete old configuration relation
    -> disk can become Ready
    != Format
    != Initialization
    != evidence that every payload field was overwritten
```

For the later secured-foreign path:

```text
different / unavailable security key
    + Clear request
    -> Instant Secure Erase required
    -> permanent erase
```

Therefore neither of these universal claims is valid:

```text
Clear == secure sanitization
Clear == never erases payload
```

The correct rule is:

> **configuration retirement does not by itself prove physical erasure; the concrete security state and execution path determine whether an explicit erase primitive is required.**

This is a terminology/operation boundary, not recovery advice and not a forensic claim about residual sectors after an actual PERC operation.

---

## Cross-case comparison

### Case 102 — PERC Patrol Read / Consistency Check

Case 102 owns maintenance on an already admitted PERC array: media verification and RAID consistency checking.

Case 131 begins earlier in the recovery path: **which disk-carried configuration is admitted as the virtual disk at all?**

The 2009/2013 foreign-import procedures now directly expose the phase ordering:

```text
admission
    -> possible repair
    -> integrity verification
```

> **array admission ≠ array integrity maintenance.**

### Case 128 — ZFS vdev labels and uberblocks

Case 128 and Case 131 share a useful functional pattern: retained member-media metadata can outlive volatile/controller-local control state and later help reconstruct a service relation.

But their mechanisms differ sharply:

- ZFS software interprets vdev labels and qualifies an uberblock/root;
- PERC firmware/management logic detects and imports controller-specific foreign configurations.

No PERC ↔ ZFS genealogy is asserted.

> **functional restart-metadata analogy ≠ common mechanism.**

The new clear deepening also does not assert that PERC `Clear` is equivalent to any ZFS label-retirement command.

### Case 87 — SCSI write-back cache

Case 87 distinguishes volatile/nonvolatile cache residence from physical-medium commitment. Case 131 adds a RAID-controller example in which Dell explicitly preserves uncommitted write cache while a virtual disk is unavailable.

The comparison is functional:

> **controller-local cached currentness ≠ disk-resident configuration currentness.**

It does not establish a direct SCSI-standard lineage for PERC's implementation.

### Case 17 — parity reconstruction

Case 17 owns the algebraic/repair question. Foreign-configuration metadata can describe an array that is too incomplete to reconstruct or serve.

> **topology knowledge ≠ reconstructability.**

### Case 44 — key destruction / cryptographic erasure

The March-2013 secured-foreign path adds a useful but narrow comparison to Case 44.

A secured foreign configuration can remain inaccessible because key/passphrase authority is missing. Dell's documented alternatives are then qualitatively different:

```text
recover the appropriate key/passphrase
    -> import may remain possible

or

Instant Secure Erase
    -> permanently erase all data
    -> reset security attributes
```

This supports:

> **configuration authority ≠ key authority ≠ payload-erasure authority.**

It does **not** establish NIST sanitization compliance, forensic resistance, or a universal PERC cryptographic-erasure design.

### Case 145 — reuse admission

Case 145 separates JFFS2 erase completion / retained witness qualification from free-list admission. Case 131 supplies a different functional example in which retiring an old configuration relation can move a disk into a `Ready` / future allocation path.

The commonality is only:

> **reuse authority is mediated by retained state.**

No filesystem/RAID implementation lineage is asserted.

---

## Prior-art / genealogy boundary

This case makes no invention-priority claim for:

- RAID metadata on member disks;
- controller-replacement recovery;
- battery-backed RAID write cache;
- MegaRAID foreign configuration;
- disk migration;
- secure erase;
- encrypted RAID import.

The earliest directly inspected Dell source in this case remains the **20 November 2007** PERC 6/i firmware record. It is a directly evidenced Dell floor, not a global historical origin.

The 24 June 2009 PERC 6 manual deepening strengthens **terminology and operation semantics**, not priority. Its value is that one product manual directly co-locates `foreign metadata`, `Import`, `Clear`, `Ready`, `Format`, `Initialization`, `Rebuild`, `Consistency Check`, `pinned cache`, and `Discard`.

The March-2013 Dell-hosted manual supplies a later direct-vendor continuity witness and a bounded secured-foreign / Instant-Secure-Erase exception.

A companion-repository search found no existing `computing-archaeology` PERC foreign-configuration case. A future genealogy should examine earlier PERC / MegaRAID generations, other hardware RAID metadata formats, controller NVRAM designs, security-key evolution, and cross-controller migration using primary manuals rather than retroactively assigning PERC 6 vocabulary to older systems.

---

## Engineering reconstruction

The bounded evidence supports the following project-level relations:

```text
physical disk survival
    != virtual-disk service availability

disk-resident array configuration
    != controller-current admitted configuration

foreign metadata detected
    != configuration previewed
    != configuration imported

foreign configuration detected
    != foreign configuration importable

configuration import
    != RAID rebuild
    != consistency verification

foreign-config Clear
    != pinned-cache Discard

ordinary foreign-config Clear
    != evidence of Format / Initialization / whole-medium erase

secured foreign config + different/unavailable key
    -> Clear may require Instant Secure Erase

configuration authority
    != key authority
    != payload-erasure authority

disk-resident configuration
    != controller-local uncommitted write cache

controller replacement recovery
    != failed-controller dirty-cache recovery

controller failure
    != automatic physical erasure
```

These are analytical separations supported by the Dell records. They are not Dell's own philosophical claims.

---

## Philosophical interpretation

**I — optional interpretation.**

Case 131 is a useful example of retention as **continued admissible relation**, not merely continued bits. A disk can retain payload and configuration while ceasing to be an admitted member of the controller's current virtual disk. Recovery then consists partly of re-establishing an interpretive/authority relation between surviving media and a controller.

The clear deepening adds the inverse: a system can retire the relation that makes surviving bits interpretable as the former array before it has established that every payload field was physically overwritten. In a secured path, however, the security policy can explicitly couple relation retirement to an erase primitive.

That interpretation must remain secondary. The historical evidence establishes foreign configuration, import/clear behavior, rebuild/check ordering, preserved cache, and one secured-erase gate; it does not state a theory of memory or identity.

---

## Failure / forgetting modes

Distinct failure modes include:

1. physical member loss or unreadability;
2. insufficient surviving members for import/reconstruction;
3. configuration recognized as foreign but not imported;
4. wrong import decision against a still-active array;
5. foreign configuration cleared instead of imported;
6. assuming a `Ready` disk is blank or sanitized when only configuration retirement has been established;
7. assuming `Clear` can avoid erase in a secured/different-key path where Dell requires Instant Secure Erase;
8. controller replacement with incompatible firmware/controller semantics;
9. interrupted RAID-level migration or capacity expansion;
10. loss or discard of controller-local uncommitted write cache before it reaches member media;
11. conflating foreign-config Clear with pinned-cache Discard;
12. recovery of topology without proof of payload consistency;
13. encrypted configuration whose key authority is unavailable;
14. failed/corrupt/nontransportable retained-cache carrier;
15. controller-NVRAM corruption or other current-configuration loss not reproduced in the inspected documents.

These modes occur at different layers and should not be reported as one generic `RAID metadata loss`.

---

## Evidence debt after this deepening

The bounded `Clear` semantics / whole-medium-overwrite ambiguity is now substantially closed at the vendor-terminology level, but Case 131 still lacks:

- exact PERC 6 on-disk metadata layout;
- update/checksum/sequence and clear atomicity;
- crash/fault behavior during `Clear` itself;
- controller-NVRAM corruption experiments;
- cross-generation/vendor metadata compatibility;
- failed/corrupt/nontransportable cache-module evidence;
- encrypted-key-loss recovery beyond the documented 2013 control path;
- independent laboratory fault injection;
- sector-level before/after forensic measurement of `Clear`;
- earlier RAID-controller prior art.

None should be inferred from the present manuals.

---

## Sources

### Primary / contemporary Dell records

1. Dell, **PERC 6/i Integrated Firmware v6.0.1-0080, A01**, released 20 Nov 2007. `Important Information` documents remove/reinsert → `foreign` → import/clear, migration shutdown, and RLM/capacity-expansion restrictions.  
   https://www.dell.com/support/home/en-us/drivers/DriversDetails?driverId=D0CFD

2. Dell, **PERC 6/i, PERC 6/E and CERC 6/i User's Guide**, `Dell_PERC6.2_UG.book`, inspected page footers dated 24 Jun 2009. Surviving Dell-authored searchable copy; used with mirror-provenance caveat. Key locations: pp. 89–93, 116, 142–143.  
   https://manualzilla.com/doc/7425219/dell-poweredge-expandable-raid-controller-3-user-s-guide

3. Dell, **Dell PERC H700 and H800 Technical Guide**, Revision 3, March 2011. Dell-hosted primary source. H800 overview lists transportable TBBU/TNVC cache options; §4.5.1 distinguishes battery-held cache from NV-cache transfer to flash; §4.5.7.1 defines the TBBU as a cache module that can move with its battery to a new controller.  
   https://i.dell.com/sites/csdocuments/shared-content_data-sheets_documents/en/perc-technical-guidebook.pdf

4. Dell, **PowerEdge RAID Controller H700 and H800 User's Guide**, March 2011 Rev. A02, especially `Cache Data Recovery` (p. 37) and `Transferring a TBBU or TNVC Between PERC H800 Cards` (p. 63). Dell's current H800 support page continues to index the User's Guide; exact page text was checked against a surviving Dell-authored mirror.  
   https://www.dell.com/support/product-details/en-us/product/poweredge-rc-h800/resources/manuals

5. Dell, **PERC 6/E Adapter Firmware v6.1.1-0047, A08**, released 06 Dec 2011. `Fixes & Enhancements` and `Important Information` document preserved uncommitted write cache and its flush after disk return plus foreign import.  
   https://www.dell.com/support/home/en-us/drivers/driversdetails?driverid=tp43x

6. Dell, **PowerEdge RAID Controller (PERC) H310, H710, H710P, and H810 User's Guide**, Rev. A02, March 2013. Dell-hosted primary. Key inspected locations: pp. 44–46 for foreign import/clear, rebuild, consistency check, preserved cache; pp. 68–69 for secured foreign configuration and Instant Secure Erase; p. 14 for initialization semantics.  
   https://dl.dell.com/manuals/common/poweredge-rc-h710_user%27s%20guide_en-us.pdf

### Later Dell operational / continuity witnesses

7. Dell OpenManage Server Administrator Storage Management, **Foreign Configuration Operations** — defines foreign configuration as data residing on physical disks moved between controllers.  
   https://www.dell.com/support/manuals/en-in/openmanage-server-administrator-v10.2.0.0/omss_10.2_ug_olh/foreign-configuration-operations?guid=guid-2082f2d8-2cd4-4878-a385-a389d4971061&lang=en-us

8. Dell, **PowerEdge: How to Import a Foreign Configuration in the RAID Controller Using the System Setup Menu** — current operational recovery guidance, including PERC replacement and warnings about unsafe import.  
   https://www.dell.com/support/kbdoc/en-us/000122457/how-to-import-a-foreign-configuration-in-the-raid-controller-using-the-system-setup-menu

9. Dell iDRAC10 User's Guide, **Importing or auto importing foreign configuration** — current member-sufficiency/import rules and `Ready` / `Degraded` / `Failed` examples.  
   https://www.dell.com/support/manuals/en-us/poweredge-xe9785l/idrac10_1.30.xx_ug/importing-or-auto-importing-foreign-configuration?guid=guid-9ecc96b6-8169-468a-ab6d-04e80169ab85&lang=en-us

## Evidence records

- [Evidence 131A — Dell PERC 2007–2011 foreign-configuration and preserved-cache grounding](../evidence/131-dell-perc-2007-2011-foreign-configuration-grounding.md)
- [Evidence 131B — Dell PERC 6 (2009) foreign-clear / secure-erase boundary deepening](../evidence/131-dell-perc6-2009-2013-foreign-clear-secure-erase-boundary-deepening.md)
