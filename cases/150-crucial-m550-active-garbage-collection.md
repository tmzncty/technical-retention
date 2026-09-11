# Crucial M550 Active Garbage Collection: Idle-Time Reclamation, Live-Data Relocation, and Free-Space Authority

## Status

**`grounded`**

## Scope

- **System:** managed NAND SSDs, anchored to the Crucial/Micron M550 product family and Crucial's maintained description of controller-local Active Garbage Collection.
- **Historical anchor:** Crucial M550 product flyer revision 29 January 2014 plus Micron's 18 March 2014 M550 availability announcement.
- **Retention question:** after host-visible data has been superseded or deallocated, what further controller-local work is required before physical erase blocks become useful free space, and why can reclamation require preserving and relocating still-live data while retiring stale embodiments?

This is not a reconstruction of the proprietary M550 firmware, Marvell 88SS9189 microcode, victim-selection policy, exact over-provisioning layout, NAND metadata format, or power-loss recovery state machine. It does not claim that Crucial or Micron invented SSD garbage collection.

The bounded question is narrower:

> **How does a managed SSD provide a concrete case where logical retirement can precede physical reclamation, while the act of forgetting stale physical embodiments itself depends on retaining and relocating still-current data?**

The case is useful because the same product family exposes `Active Garbage Collection` and `TRIM support` as distinct features, while maintained Crucial documentation describes controller-local cleanup as work that needs powered idle opportunity and free space. A vendor-neutral SNIA account supplies the generic erase-block mechanism without turning that generic mechanism into an undocumented M550 implementation claim.

---

## Historical vocabulary

The 2014 Crucial product flyer uses period terms including:

- `Active Garbage Collection`;
- `TRIM support`;
- `NAND Flash`;
- `firmware`;
- `Power Loss Protection`;
- `Device Sleep`.

Crucial's maintained support material uses:

- `Active Garbage Collection`;
- `controller`;
- `background cleanup`;
- `idle time`;
- `Trim`;
- `free space`.

The project phrases **reclaim eligibility**, **free-space authority**, **reclamation debt**, **live-data preservation before erase**, and **background-maintenance opportunity** are engineering reconstructions. They are not claimed as Crucial's 2014 vocabulary.

---

## Historical record: a named managed SSD with Active Garbage Collection

Crucial's M550 product flyer is revision-dated **29 January 2014**. Its advanced-feature list includes both **Active Garbage Collection** and **TRIM support**. The same flyer identifies the device as a SATA SSD using 20 nm Micron MLC NAND and user-upgradeable firmware.

Micron's **18 March 2014** M550 launch announcement states that the M550 was available that day under the Crucial brand for consumers/business/system builders and under the Micron brand for OEM customers.

These two first-party records support a conservative productization statement:

> **By March 2014, a named Crucial/Micron managed SSD product publicly listed Active Garbage Collection as a drive feature distinct from TRIM support.**

They do **not** establish invention priority for garbage collection, the date the mechanism was first implemented inside Micron/Crucial firmware, or the exact internal algorithm used by M550 firmware.

Earlier industry and academic records already make a first-invention reading untenable. SNIA discussed TRIM and drive-internal garbage collection in 2011, and earlier flash-management literature had long treated erase-before-rewrite, out-of-place updates, and erase-unit reclamation as established design problems.

---

## Maintained vendor description: powered idle time can be productive maintenance time

Crucial's maintained support article says Crucial SSDs contain a controller-local maintenance feature called **Active Garbage Collection**. It describes the feature as background cleanup that runs when the SSD has power but is not actively reading or writing data, and says the drive needs idle periods for the feature to operate. The same support material says available free space matters because TRIM and Active Garbage Collection rely on moving data as part of cleanup.

That maintained support page is a useful current/family-level contract, but it is **not** back-projected as proof that every M550 firmware revision used precisely the same trigger thresholds, idle timers, amount-of-free-space heuristic, or power-state transitions.

The bounded engineering consequence is nonetheless clear:

- `host not issuing foreground I/O != controller doing nothing`;
- `powered idle != powered off`;
- `maintenance opportunity != maintenance completion`.

An idle interval can therefore be operationally productive even when the host sees no application I/O. Conversely, lack of idle opportunity can accumulate background maintenance pressure without implying that currently readable logical data are already incorrect.

---

## TRIM and garbage collection are different relations

The M550 flyer lists **TRIM support** and **Active Garbage Collection** separately. SNIA's 2011 explanation of TRIM likewise distinguishes a host-to-device indication that logical blocks are no longer in use from a drive's internal garbage collection work.

The important retention split is:

```text
host / filesystem decides some logical data are no longer needed
        ↓
TRIM/deallocation may communicate that fact to the device
        ↓
device gains stronger knowledge that some physical embodiments need not remain current
        ↓
controller still has to reorganize / reclaim erase-block space
```

Therefore:

- `host deletion != device physical erase`;
- `TRIM/deallocation indication != garbage-collection execution`;
- `reclaim eligibility != reclaim completion`;
- `logical free space != immediately erased NAND capacity`.

Crucial's maintained material also presents Active Garbage Collection as useful where TRIM is unavailable. That means controller-local reclamation cannot be reduced to merely “executing a TRIM command.” The two mechanisms can cooperate, but they are not one state transition.

---

## Generic NAND GC mechanism: forgetting stale state requires retaining live state

For the mechanism-level reconstruction, this case uses SNIA's vendor-neutral 2016 SSD garbage-collection explanation rather than pretending that Crucial publicly documented M550 firmware internals.

SNIA describes the generic managed-SSD problem this way: as writes continue, valid data can become fragmented across NAND blocks containing invalid/obsolete data. To reclaim a block, garbage collection first relocates valid data to other blocks and then erases the original block. That work contributes to write amplification and can interfere with foreground performance.

The retention relation is unusually clear:

```text
mixed erase block
  ├─ stale / invalid physical embodiments
  └─ still-live physical embodiments
            ↓
preserve / relocate still-live data
            ↓
retire old physical embodiments
            ↓
erase old block
            ↓
block becomes reusable capacity
```

So the act of forgetting is selective. A whole erase block cannot safely be treated as disposable merely because it contains some stale pages. Still-current data must remain authoritative across relocation before the block can be erased for reuse.

This yields:

- `stale page exists != containing erase block reclaimable now`;
- `physical relocation of live data != host-visible logical mutation`;
- `old physical embodiment retired != logical payload forgotten`;
- `erase-block reclamation requires preservation of live state`.

This is the core reason to include managed SSD garbage collection in a repository about technical retention: **reclamation is not simply deletion; it is a state transition whose correctness depends on distinguishing what may be forgotten from what must survive the transition.**

---

## Free space is an operational resource, not only a namespace count

Crucial's maintained support material recommends retaining free capacity so that data movement and cleanup can proceed effectively. Storage Executive documentation likewise describes over-provisioning as additional space available to the controller so functions such as wear leveling and garbage collection can operate more smoothly.

This should not be over-read into a specific M550 over-provisioning ratio or firmware threshold. The general relation is narrower:

> **host-visible unused capacity and controller-available relocation/reclamation workspace are related but not identical concepts.**

A block-interface SSD may expose a stable logical namespace even while its controller is continuously transforming the physical placement and free-block pool underneath that namespace.

Thus:

- `logical capacity != current pool of immediately programmable physical pages`;
- `free namespace address != erased physical page ready for programming`;
- `additional spare area can change maintenance opportunity without changing user payload semantics`.

---

## Foreground latency and background maintenance

SNIA and systems research describe garbage collection as a source of write amplification and performance interference. That is important here only as an operational witness: background maintenance competes for NAND/channel/controller resources and therefore has a scheduling relation to foreground I/O.

The repository should not infer from the word `background` that garbage collection has no observable effect. Nor should it infer from Crucial's idle-time support advice that every garbage-collection action occurs only during total host idleness. Product firmware may perform foreground/urgent reclamation under pressure; the sources inspected here do not disclose the exact M550 scheduler.

So:

- `background != performance-invisible`;
- `idle-preferred maintenance != proof of idle-only maintenance`;
- `garbage-collection pressure != data-loss event`.

---

## Power and crash boundary

The maintained Crucial support instructions require the SSD to remain **powered** while idle to give Active Garbage Collection an opportunity to run. This makes energy availability part of the maintenance opportunity.

But the inspected sources do not reveal:

- whether a particular GC move is transactionally checkpointed;
- exactly when old/new mapping metadata become authoritative;
- what survives sudden power loss during an M550 GC cycle;
- whether an interrupted victim block is retried from a durable journal, reconstructed by scan, or handled another way.

M550 documentation separately advertises power-loss protection, but feature co-presence is not enough to reconstruct the GC crash protocol.

Therefore:

> **powered-idle requirement != evidence for a specific durable GC checkpoint format**.

Case 39 remains the stronger repository example for explicitly studied FTL power-failure metadata recovery.

---

## Forgetting and sanitization boundary

Garbage collection erases blocks as a capacity-management operation, but this case does not promote ordinary GC into a security sanitization guarantee.

Keep separate:

- host-level delete or overwrite;
- TRIM/deallocation knowledge;
- internal invalid/stale-page status;
- garbage-collection relocation of still-live data;
- erase-block reclamation for future writes;
- device sanitize/security erase commands;
- forensic irrecoverability across all spare, remapped, cached, or redundant embodiments.

A block erased during garbage collection may indeed lose its former cell contents, but the vendor materials inspected here do not establish that ordinary Active Garbage Collection is intended to find and purge every embodiment of a deleted logical object, satisfy a sanitization standard, or provide externally verifiable purge completion.

Thus:

> **garbage collection != sanitize**.

Cases 44 and 47 remain the stronger sanitize/remanence boundary.

---

## Cross-case comparison

### Case 04 — mapped Flash / FTL identity

Case 04 shows that logical designation can survive physical relocation. Case 150 adds the reclamation motive: live data may be relocated specifically so that a mixed old erase block can be erased and returned to the free pool. Same broad abstraction layer, different bounded question.

### Case 145 — JFFS2 raw-Flash garbage collection

Both cases relocate live data and reclaim erase-block space, but the authority boundary differs sharply. JFFS2 exposes filesystem nodes, versions, obsolete-node state, and `CLEANMARKER` logic in open source. A managed SSD hides the corresponding mapping/victim-selection/recovery machinery behind a block interface. Shared `garbage collection` vocabulary does not make their state machines identical.

### Case 84 — NVMe Zoned Namespace reset

ZNS deliberately changes the host/device division of flash-management responsibility and can reduce hidden device garbage-collection pressure by exposing write-ordering and zone constraints. That is a functional contrast, not a claim that ZNS “eliminates all garbage collection” or descends from Crucial's firmware design.

### Case 39 — GeckoFTL crash recovery

Case 39 explicitly studies metadata needed to recover FTL state after power failure. Case 150 has no source basis for reconstructing the M550 GC crash protocol, so it stops at the observed maintenance/reclamation boundary.

### Cases 44 / 47 — sanitization

Ordinary garbage collection reclaims capacity while preserving all data that remains current. Sanitization aims to retire recoverability itself. Similar erase primitives can participate in both, but their authority, completeness, and verification contracts differ.

---

## Prior-art and genealogy boundary

This case does **not** claim that the 2014 M550 introduced SSD garbage collection.

Guardrails:

- SNIA publicly discussed drive-internal garbage collection and TRIM by 2011;
- 2005 flash-management literature already surveyed out-of-place updates, large erase units, reclaim/erase-management problems, and wear management;
- the M550 evidence therefore serves as a **named-product embodiment floor**, not an invention date;
- chronology does not prove a Micron/Crucial genealogy from any particular earlier paper, patent, controller family, or SSD vendor.

A fresh search of `tmzncty/computing-archaeology` found no dedicated SSD garbage-collection study to reuse. Broader FTL genealogy, early commercial SSD GC, controller architecture, and product-by-product scheduler history belong primarily there if pursued; Case 150 keeps only the retention/reclamation relation.

---

## Philosophical interpretation — bounded

The engineering evidence supports one restrained observation: **technical forgetting may require active preservation.**

A mixed erase block cannot be forgotten wholesale. The controller must discriminate current from stale embodiments, carry current data forward, and only then erase the old container. “Garbage collection” is therefore not pure destruction; it is a selective transition that preserves one continuity while ending another.

A second observation is that **inactivity at one layer can be maintenance activity at another**. Host idleness can provide the interval in which a controller reorganizes physical state while leaving the logical namespace apparently unchanged.

These are mechanism-level observations. They do not make SSD garbage collection a theory of human forgetting, archival memory, or ontology.

---

## Source ledger

### P1 — Crucial M550 product flyer, revision 29 January 2014 — `H/P`

Crucial / Micron, **“Crucial M550 Solid State Drive”**, revision `01/29/2014`:
<https://content.crucial.com/content/dam/crucial/ssd-products/m550/flyer/crucial-m550-ssd-product-flyer-en.pdf>

Directly supports:

- M550 product identity and 20 nm Micron MLC NAND;
- firmware as user-upgradeable;
- `Active Garbage Collection` and `TRIM support` listed as separate advanced features;
- co-presence of power-loss protection, SMART, ECC, and device sleep.

It does **not** disclose the garbage collector's victim-selection algorithm, mapping transaction protocol, idle threshold, crash recovery, or erase scheduling.

### P2 — Micron M550 availability announcement, 18 March 2014 — `H/P`

Micron Technology investor-relations press release / static release PDF:
<https://investors.micron.com/static-files/6f3e5f2f-7a82-41b0-b3a0-56c8b4b4c1a1>

Directly supports the 18 March 2014 availability/public-product anchor for M550 under Crucial and Micron brands. It is not used to infer GC internals.

### P3 — Crucial maintained Active Garbage Collection support article, 15 November 2024 — `H/P` for current vendor contract; anti-anachronism guard required

Crucial Support, localized origin-hosted copies including:
<https://www.crucial.jp/support/articles-faq-ssd/ssd-used-to-be-faster-but-has-slowed-down>
<https://www.crucial.es/support/articles-faq-ssd/ssd-used-to-be-faster-but-has-slowed-down>

Directly supports Crucial's maintained family-level statements that Active Garbage Collection is controller-local background maintenance, benefits from powered idle time, and needs available space for cleanup/data movement.

This source is **not** used to assert that every 2014 M550 firmware revision had identical timing thresholds or scheduling behavior.

### P4 — SNIA, “Trim: The Basics,” 29 June 2011 — `H/P` for SNIA's period terminology; generic only

SNIA Solid State Storage Initiative:
<https://www.snia.org/blog/2011/trim-basics>

Supports the period distinction between host TRIM knowledge and drive-internal garbage collection. It is not a Micron/Crucial implementation source.

### P5 — SNIA, “Increasing SSD Performance and Lifetime with Multi-stream Technology,” 15 June 2016 — high-quality industry mechanism source

SNIA educational library, presenter Changho Choi:
<https://www.snia.org/educational-library/increasing-ssd-performance-and-lifetime-multi-stream-technology-2016>

Its abstract describes the generic managed-SSD GC sequence: valid data fragmented across blocks with invalid data are relocated before the original blocks are erased; GC contributes to write amplification and performance cost.

Used for generic engineering reconstruction only, not as proof of exact M550 firmware behavior.

### P6 — Gal & Toledo, ACM Computing Surveys 37(2), June 2005 — high-quality academic prior-art guardrail

Tel Aviv University record:
<https://cris.tau.ac.il/en/publications/algorithms-and-data-structures-for-flash-memories/>

The peer-reviewed survey records flash's erase-unit constraint and established not-in-place update / erase-management / wear-management techniques well before M550. It is used to reject a 2014 invention-priority reading, not to claim direct genealogy.

---

## Evidence-strength summary

- **Strong:** named M550 product documentation explicitly lists Active Garbage Collection and TRIM as separate features; Micron gives a dated 2014 availability anchor.
- **Strong for current vendor behavior:** Crucial's maintained support material explicitly describes controller-local Active Garbage Collection, powered idle opportunity, and free-space dependence.
- **Strong generic mechanism:** SNIA describes relocation of valid data before erase-block reclamation and its write-amplification/performance cost.
- **Moderate historical guardrail:** 2011 SNIA and 2005 academic flash-management literature establish that the relevant problem family predates M550.
- **Not established:** exact M550 GC algorithm, victim policy, internal metadata, free-space threshold, power-fail transaction, firmware-version differences, or complete physical sanitization effect.

---

## Open debt

1. Recover an origin-hosted or archived 2010–2014 Crucial support page that dates Active Garbage Collection's idle-time description closer to M550 rather than relying on maintained 2024 support text.
2. Find a first-party controller/firmware document exposing an actual managed-SSD GC state machine, victim selection, or crash protocol.
3. Add named-device traces that correlate TRIM, idle time, internal writes, and reclaimed space without mistaking performance recovery for direct block-level proof.
4. Trace early commercial SSD GC / FTL genealogy in `computing-archaeology` rather than expanding this case into a general SSD history.
5. Keep ordinary reclamation erase separate from sanitize/remanence testing unless lower-layer evidence is obtained.
