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

## Evidence navigation

- [Powered idle, sleep states, and maintenance opportunity deepening](../evidence/150-crucial-powered-idle-sleep-maintenance-opportunity-deepening.md) — separates host-visible idleness, device/interface sleep, controller maintenance eligibility, and actual GC execution; also records the M550's co-listed Device Sleep support and a firmware-version boundary around power-state transitions.
- [2013–2015 AGC provenance and m4 experiment deepening](../evidence/150-crucial-2013-2015-agc-provenance-experiment-deepening.md) — narrows the public-circulation floor of Crucial's `6–8 hours` powered-idle support wording to contemporaneous 2013–2014 preservation witnesses and uses a peer-reviewed named Crucial m4 experiment to separate GC presence, deallocation/reclaim eligibility, execution, physical erase, and observed stale-data recoverability.
- [2013 support-page version provenance deepening](../evidence/150-crucial-2013-support-page-version-provenance-deepening.md) — moves the independently witnessed named-resource existence floor to 12 June 2013, records later-preserved page metadata reporting 17 January 2013 creation and 23 October 2013 edit timestamps, and separates page identity from content-version identity rather than back-dating the later `6–8 hours` body wholesale.
- [IBM 2009–2012 SSD GC validity/map/erase prior-art deepening](../evidence/150-ibm-2009-2012-ssd-gc-validity-map-erase-prior-art-deepening.md) — adds a manufacturer-authored controller design that separates PI invalidity evidence, victim selection, live-data recovery/re-storage, address-map update, erase eligibility, and actual old-block erase. It is used as prior-art/control-architecture evidence, **not** as M550 implementation evidence or genealogy.
- [T13 2007–2010 TRIM logical-invalidation/read-semantics deepening](../evidence/04-t13-2007-2010-trim-logical-invalidation-read-semantics-deepening.md) — shared standards evidence already developed for Case 04 and intentionally **reused rather than duplicated** here; separates host discardability notification, post-TRIM read semantics (including DRAT/read-zero proposals), later physical reclamation, and sanitization.
- [2009–2012 over-provisioning / reserved-capacity deepening](../evidence/150-2009-2012-overprovisioning-reserved-capacity-deepening.md) — uses a 2009-priority adaptive-over-provisioning patent family, OCZ's 2012 User Pool / OP Pool disclosure, and Intel SSD 710 product literature to separate host-visible logical capacity, controller-reserved maintenance headroom, OP-pool role, erased-block readiness, garbage-collection completion, and endurance/write-amplification effects without projecting those mechanisms into M550 firmware.

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

Earlier industry and academic records already make a first-invention reading untenable. SNIA discussed TRIM and drive-internal garbage collection in 2011, earlier flash-management literature had long treated erase-before-rewrite, out-of-place updates, and erase-unit reclamation as established design problems, and the new IBM 2009-priority control-architecture witness already exposes a detailed managed-SSD GC sequence before the M550 product anchor.

---

## Maintained vendor description: powered idle time can be productive maintenance time

Crucial's maintained support article says Crucial SSDs contain a controller-local maintenance feature called **Active Garbage Collection**. It describes the feature as background cleanup that runs when the SSD has power but is not actively reading or writing data, and says the drive needs idle periods for the feature to operate. The same support material says available free space matters because TRIM and Active Garbage Collection rely on moving data as part of cleanup.

That maintained support page is a useful current/family-level contract, but it is **not** back-projected as proof that every M550 firmware revision used precisely the same trigger thresholds, idle timers, amount-of-free-space heuristic, or power-state transitions.

The bounded engineering consequence is nonetheless clear:

- `host not issuing foreground I/O != controller doing nothing`;
- `powered idle != powered off`;
- `maintenance opportunity != maintenance completion`.

An idle interval can therefore be operationally productive even when the host sees no application I/O. Conversely, lack of idle opportunity can accumulate background maintenance pressure without implying that currently readable logical data are already incorrect.

The follow-on power-state deepening adds an important qualification. Crucial's maintained troubleshooting procedure deliberately keeps an SSD powered and idle for **6–8 hours**, including by using BIOS/UEFI or Startup Manager, and recommends changing sleep-related power settings so the device remains powered long enough for background cleanup. Meanwhile the 2014 M550 flyer separately lists `Device Sleep support`. These records justify treating **host idle**, **interface/device sleep**, **maintenance eligibility**, and **actual maintenance execution** as distinct analytical states. They do **not** prove whether M550 garbage collection can or cannot run in SATA DevSleep, Partial, or Slumber.

### Period-provenance and named-device follow-on

The [2013–2015 provenance/experiment deepening](../evidence/150-crucial-2013-2015-agc-provenance-experiment-deepening.md) narrows two remaining seams.

A public **18 August 2013** reproduction of a Crucial-support email concerning a V4 SSD contains the `Active Garbage Collection` + `6–8 hours` powered-idle procedure, and a **22 March 2014** forum post reproduces a passage attributed to Crucial's website under the heading `Crucial SSDs and TRIM/Garbage Collection`. These are contemporaneous preservation witnesses, not authenticated Crucial-origin archives.

The [2013 support-page version-provenance deepening](../evidence/150-crucial-2013-support-page-version-provenance-deepening.md) now moves a different chronology floor earlier. Mac Geek Gab's **12 June 2013** complete show notes already list the distinctive resource title `My SSD used to be so much faster… What happened?`, while a September 2014 forum quotation preserves reported Crucial page metadata of **17 January 2013** creation and **23 October 2013** edit timestamps. The January date remains a later-preserved metadata claim rather than an authenticated origin capture, and the quoted 2014 body cannot be assigned wholesale to the January version because the same preserved header reports an intervening edit. The safer floor for the detailed `6–8 hours` wording therefore remains the August 2013 support-correspondence reproduction.

This yields a documentation boundary that matters to the historical method:

```text
same support-page identity
    != same content version
    != authenticated origin capture
```

Second, Shah, Mahmood, and Slay's SecureComm 2014 experiment names a **Crucial m4 CT064M4SSD2 64 GB** and reports sharply different stale-data recovery outcomes across USB/secondary-SATA and primary-SATA-with-Windows-7/TRIM setups. The paper itself infers from the survivor cases that the m4 lacked background garbage collection. This repository records that inference but does not adopt it as established device fact: recoverability can show that physical embodiments survived the tested path, but cannot by itself distinguish `GC engine absent` from `pages not made discard-eligible`, `GC not scheduled`, or `erase not completed`.

The added boundary is therefore:

```text
maintenance mechanism present
    != pages authorized for reclamation
    != maintenance execution on those pages
    != physical erase before observation
    != stale-data recoverability outcome
```

The m4 experiment is an adjacent named-device witness, not evidence that the later M550 uses the same controller, scheduler, or reclaim policy.

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

The m4 experiment adds a useful observability guardrail: when a tested host path did not produce the authors' expected TRIM effect, stale payload remained recoverable. That result does not establish that no garbage collector existed; a controller that still regards pages as live may have to preserve/relocate them rather than discard them. Thus `TRIM absent != GC absent`, just as `TRIM delivered != physical erase necessarily synchronous with the command`.

### Reused T13 interface evidence: read semantics can change before reclamation is proved complete

The repository already has a detailed standards-history packet for Case 04, [`04-t13-2007-2010-trim-logical-invalidation-read-semantics-deepening.md`](../evidence/04-t13-2007-2010-trim-logical-invalidation-read-semantics-deepening.md). Case 150 deliberately reuses that packet instead of creating a second TRIM history.

The T13 proposal sequence adds an interface-level layer between deallocation knowledge and physical reclamation. In `e07154r6`, trimmed logical-block data become indeterminate until rewritten. The later `e08137` DRAT proposal distinguishes deterministic from non-deterministic reads after TRIM, and the `e09117` / `e09158` read-zero/clarification work further distinguishes an advertised all-zero post-TRIM read result.

For this case, the bounded consequence is:

```text
TRIM/deallocation delivered
    != old payload remains host-visible/current at that LBA
    != old NAND embodiment proved physically erased
    != garbage-collection completion
    != sanitize completion
```

In particular, a host-visible zero after a read-zero-after-TRIM contract is a **block-interface read result**, not by itself evidence that the old physical cells have already been erased. Conversely, indeterminate post-TRIM reads are an interface freedom, not proof that stale cells necessarily remain recoverable.

This sharpens Case 150's existing state chain:

```text
host retirement decision
    -> TRIM/deallocation knowledge
    -> post-TRIM read/currentness contract
    -> controller stale/invalid authority
    -> later live-data relocation as required
    -> erase-block reclamation
```

The source evidence does not require every controller to expose these as separately timed internal events, but it blocks the stronger and unsupported equation `TRIM completion = physical reclaim completion`.

The T13 material is standards/interface prior art only. No inspected source establishes that the M550 advertised DRAT or RZAT, or that its firmware implemented any particular post-TRIM return mechanism.

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

### Manufacturer-controller prior art: IBM 2009-priority validity → map → erase sequence

The [IBM prior-art/control-architecture deepening](../evidence/150-ibm-2009-2012-ssd-gc-validity-map-erase-prior-art-deepening.md) adds a manufacturer-primary implementation design without turning it into an M550 claim. IBM's `US20120266050A1 / US8904261B2`, priority **17 December 2009**, describes an SSD controller that maintains an `LBA/PBA address map`, sets per-page `PI` invalidity flags for overwritten/deleted pages, and maintains aggregate PI counts used in internal management.

Its Figure 6 GC path makes the sequencing unusually explicit:

```text
invalidity evidence / PI counts
    -> select recycle target
    -> recover still-valid data
    -> re-store valid data in new physical locations
    -> update LBA/PBA address map
    -> old blocks become erasable
    -> erase now or at a later time
```

This sharpens the case in three ways.

First, **invalidity is controller authority, not physical destruction**: setting a PI flag changes whether an old page counts as valid; it does not itself erase the cell state.

Second, **new embodiment creation and currentness publication are distinct**: valid data are re-stored before the address map is updated to the new locations.

Third, **map/currentness transition and capacity reclamation are distinct**: after the map update the old blocks can be erased, but the patent expressly permits that erase to occur immediately **or later**. Therefore a controller can have remaining physical reclamation work after the logical resolution relation has already moved.

This is strong prior-art/control-architecture evidence for:

```text
invalid page known
    != victim selected
    != live data copied
    != mapping updated
    != old block erased
    != capacity reusable
```

It is **not** evidence that M550 firmware used IBM's PI flags, stride/C2 design, victim heuristic, map-publication order, or crash protocol. Chronology is not genealogy.

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

### 2009–2012 prior art: reserved capacity is maintenance headroom, not an erased-block certificate

The [over-provisioning / reserved-capacity deepening](../evidence/150-2009-2012-overprovisioning-reserved-capacity-deepening.md) now makes this boundary historical rather than merely generic.

A 2009-priority Shalvi/Sommer/Kasorla disclosure defines over-provisioning against physical capacity larger than host-visible logical capacity, allows the over-provisioning overhead to change while the host-visible user capacity remains fixed, and links larger OP to lower compaction cost, less wear, and greater throughput in its described designs. OCZ's 2012 publication goes further by defining `User Pool` and `OP Pool` as transitionable controller roles and allowing programmed / partially written blocks to belong to the OP pool before consolidation returns an erased block to that pool. Intel's 2011 SSD 710 literature then supplies a named-product witness: `20 percent over-provisioning` is tied to higher endurance/performance ratings, while a separate HET brief says `extra spare area` lowers write amplification alongside — not instead of — background refresh, wear leveling, and disturb-management mechanisms.

The bounded result is:

```text
physical NAND capacity
    != host-visible logical capacity

host-visible free LBA space
    != controller-reserved over-provisioning capacity

over-provisioning-pool membership
    != erased / empty NAND state

reserved maintenance headroom
    != reclamation already completed
```

For Case 150, over-provisioning is therefore best treated as **capacity that can make future relocation/reclamation transitions cheaper or feasible**, not as evidence that those transitions have already run. The patent/product evidence is prior art and a named-product control; it does not disclose the M550's exact OP ratio, pool implementation, or crash protocol.

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

The power-state deepening further separates:

- absence of foreground I/O;
- SATA/interface low-power state;
- system sleep policy;
- controller-local maintenance eligibility;
- actual completion of reclamation work.

The M550's co-listed Device Sleep support therefore cannot be used as shorthand for either “GC runs during sleep” or “GC cannot run during sleep.” Product-specific evidence for that arbitration remains missing. Crucial's M550 MU02 release notes also later mention improved behavior during power-state transitions, which is enough to make firmware-version sensitivity explicit but not enough to infer a GC scheduler change.

The IBM prior-art/control-architecture witness adds one adjacent historical fact but does **not** close the M550 crash seam. Its specific embodiment says that after a controller detects a power-supply interruption, transient parity together with controller metadata including the current address map can be copied to Flash before shutdown. That demonstrates that **preserving controller metadata across a detected shutdown** was already an explicit manufacturer design concern by the 2009-priority family.

But the inspected sources still do not reveal for the M550:

- whether a particular GC move is transactionally checkpointed;
- exactly when old/new mapping metadata become authoritative;
- what survives sudden power loss during an M550 GC cycle;
- whether an interrupted victim block is retried from a durable journal, reconstructed by scan, or handled another way.

Nor does IBM's bounded pre-shutdown copy prove arbitrary-power-cut GC atomicity, PI-state durability, torn-map handling, or an M550 implementation. M550 documentation separately advertises power-loss protection, but feature co-presence is not enough to reconstruct the GC crash protocol.

Therefore:

> **powered-idle requirement != evidence for a specific durable GC checkpoint format**;

and:

> **pre-shutdown metadata preservation path != arbitrary-power-cut GC transaction proof**.

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

Case 04's later T13 deepening is now explicitly shared with this case. There it answers how host-side discardability knowledge crosses the interface and how read-after-TRIM semantics can change without proving immediate physical reclamation. Here the same evidence is used only to refine the **TRIM → GC** boundary; the standards chronology remains authoritative in the Case-04 evidence file rather than being copied into a second packet.

The IBM prior-art/control-architecture witness gives that relation a later manufacturer-defined state sequence: physical re-storage, address-map update, and old-block erase are distinct transitions. It is a functional/historical control witness, not a claim that the early Case-04 systems or M550 implemented the IBM stride/C2 architecture.

The m4 experiment deepening adds the reverse-side control question: if device-level retirement/deallocation evidence is absent or not acted on, upper-layer deletion need not make a physical embodiment reclaimable. That is a functional reconstruction, not a claim that the m4 implements Case 04's historical patent structures.

### Case 145 — JFFS2 raw-Flash garbage collection

Both cases relocate live data and reclaim erase-block space, but the authority boundary differs sharply. JFFS2 exposes filesystem nodes, versions, obsolete-node state, and `CLEANMARKER` logic in open source. A managed SSD hides the corresponding mapping/victim-selection/recovery machinery behind a block interface. Shared `garbage collection` vocabulary does not make their state machines identical.

### Case 84 — NVMe Zoned Namespace reset

ZNS deliberately changes the host/device division of flash-management responsibility and can reduce hidden device garbage-collection pressure by exposing write-ordering and zone constraints. That is a functional contrast, not a claim that ZNS “eliminates all garbage collection” or descends from Crucial's firmware design.

### Case 39 — GeckoFTL crash recovery

Case 39 explicitly studies metadata needed to recover FTL state after power failure. Case 150 has no source basis for reconstructing the M550 GC crash protocol, so it stops at the observed maintenance/reclamation boundary. IBM's detected-interruption metadata-copy path is an adjacent prior-art witness, not a substitute for Case 39's explicit restart/reconstitution problem.

### Case 111 — long-offline SSD operational retention

Case 111 also demonstrates that future powered opportunity can matter, but for a different obligation: long-offline NAND retention and field policy rather than ordinary erase-block reclamation. The comparison is functional only. Case 111's weeks/months cadence must not be imported into Case 150, and Case 150's 6–8-hour troubleshooting window must not be treated as a NAND retention qualification interval.

### Cases 44 / 47 — sanitization

Ordinary garbage collection reclaims capacity while preserving all data that remains current. Sanitization aims to retire recoverability itself. Similar erase primitives can participate in both, but their authority, completeness, and verification contracts differ.

The SecureComm m4 tests use quick format and forensic recovery, not a security sanitize command. Their path-dependent survivor result therefore strengthens `logical retirement != physical trace retirement` while remaining outside sanitize-conformance claims.

---

## Prior-art and genealogy boundary

This case does **not** claim that the 2014 M550 introduced SSD garbage collection.

Guardrails:

- Gal and Toledo's 2005 flash-management survey already records erase-unit constraints, not-in-place update, reclamation/erase management, and wear-management problem families;
- the T13 2007–2010 Data Set Management / TRIM / DRAT / read-zero proposal chain predates M550 and already separates host discardability notification from later read behavior; it is interface prior art, not M550 implementation evidence;
- IBM's manufacturer-authored `US20120266050A1 / US8904261B2`, with **2009-12-17 priority**, exposes a concrete managed-SSD controller sequence separating invalidity state, victim selection, live-data re-storage, map update, and later block erase;
- the 2009-priority Shalvi/Sommer/Kasorla family, OCZ's 2012 publication, and Intel's 2011 SSD 710 literature independently establish that over-provisioning / spare-area capacity was already an explicit controller/product design variable tied to compaction, write amplification, wear, endurance, or performance before M550;
- SNIA publicly discussed drive-internal garbage collection and TRIM by 2011;
- the M550 evidence therefore serves as a **named-product embodiment floor**, not an invention date;
- the IBM and over-provisioning witnesses are prior-art/control-architecture evidence, not proof that Crucial/Micron implemented those designs;
- chronology does not prove a Micron/Crucial genealogy from any particular earlier paper, patent, controller family, or SSD vendor.

A fresh search of `tmzncty/computing-archaeology` for combinations of `garbage collection`, `SSD`, `FTL`, `IBM`, and `Cideciyan` found no dedicated matching study to reuse. A new search for `Crucial Active Garbage Collection powered idle` likewise found no dedicated support-page/product-history module to reuse. The current pass also searched `DRAT RZAT TRIM ATA`, `e07154`, and `over-provisioning SSD 710` and found no dedicated companion packet. Broad FTL genealogy, early commercial SSD GC, over-provisioning terminology/product history, controller architecture, T13/T10/SATA low-power/TRIM transport genealogy, Windows adoption, support-site migration, and product-by-product scheduler history belong primarily there if pursued; Case 150 keeps only the retention/reclamation relation and reuses the existing Case-04 T13 packet for interface semantics.

---

## Philosophical interpretation — bounded

The engineering evidence supports one restrained observation: **technical forgetting may require active preservation.**

A mixed erase block cannot be forgotten wholesale. The controller must discriminate current from stale embodiments, carry current data forward, and only then erase the old container. “Garbage collection” is therefore not pure destruction; it is a selective transition that preserves one continuity while ending another.

The IBM deepening sharpens this without changing the philosophical boundary: negative validity evidence, positive mapping/currentness state, and later physical erase can be different retained relations. Forgetting at one layer can therefore depend on preserving enough state to know what must **not** be forgotten during the same transition.

The reused T13 interface evidence adds a narrower observation: an old payload can cease to be the host-visible/current value at an LBA before lower-layer physical erasure is proved complete. That is an interface/currentness statement, not a claim that the old NAND pattern necessarily survives.

The over-provisioning deepening adds another bounded condition: **absence of current payload can itself be maintained as transformation capacity**. Controller-reserved headroom can make it possible to carry current embodiments forward while stale embodiments are retired. This does not mean empty space “stores” the payload, nor does it make over-provisioning a philosophical synonym for reserve; it is an engineering precondition for some future state transitions.

A second observation is that **inactivity at one layer can be maintenance activity at another**. Host idleness can provide the interval in which a controller reorganizes physical state while leaving the logical namespace apparently unchanged.

The power-state deepening adds a further limit to that observation: apparent inactivity does not itself guarantee that lower-layer maintenance machinery remains eligible. Energy-saving policy can consume the same idle interval in a different way.

The m4 experiment deepening adds one more bounded condition: forgetting safely can require retained authority that an old embodiment is no longer current. A forensic trace can survive after upper-layer retirement without thereby remaining authoritative current state.

The new support-page provenance slice adds a methodological analogue: a **named page identity can persist while its body version changes**. This is useful only as a state-separation warning for historical evidence; it does not identify documentation revision with NAND remapping or claim any technical genealogy between them.

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

It does **not** disclose the garbage collector's victim-selection algorithm, mapping transaction protocol, idle threshold, crash recovery, erase scheduling, or GC eligibility in Device Sleep.

### P2 — Micron M550 availability announcement, 18 March 2014 — `H/P`

Micron Technology investor-relations press release / static release PDF:
<https://investors.micron.com/static-files/6f3e5f2f-7a82-41b0-b3a0-56c8b4b4c1a1>

Directly supports the 18 March 2014 availability/public-product anchor for M550 under Crucial and Micron brands. It is not used to infer GC internals.

### P3 — Crucial maintained Active Garbage Collection support article, 15 November 2024 — `H/P` for current vendor contract; anti-anachronism guard required

Crucial Support, localized origin-hosted copies including:
<https://www.crucial.jp/support/articles-faq-ssd/ssd-used-to-be-faster-but-has-slowed-down>
<https://www.crucial.es/support/articles-faq-ssd/ssd-used-to-be-faster-but-has-slowed-down>

Directly supports Crucial's maintained family-level statements that Active Garbage Collection is controller-local background maintenance, benefits from powered idle time, needs available space for cleanup/data movement, and can be given a longer maintenance window by keeping the device powered rather than allowing ordinary sleep policy to remove that opportunity.

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

### P7 — SATA-IO TPR 038 `DEVSLP` and interoperability material — `H/P`, protocol boundary only

SATA-IO, **“SATA3.1 TPR C108 – Device Sleep,” Version 1.0a**:
<https://sata-io.org/sites/default/files/TP_038_SATA31_TPR_C108_DEVSLP_V1.0a.pdf>

SATA-IO Unified Test Document Device Sleep tests:
<https://sata-io.org/sites/default/files/documents/UTD_1_6_Rev1_1%20Released.pdf>

These sources distinguish DevSleep from PHYRDY/Partial/Slumber and document Device Sleep interface behavior. They are used to prevent vocabulary collapse, not to infer M550 GC behavior.

### P8 — Crucial M550 MU02 firmware support record, released 8 January 2018 — `H/P`, revision-sensitivity guardrail

Crucial Support, **M550 SSD firmware and support**:
<https://stage.crucial.com/content/crucial/en-us/home/support/ssd-support/m550-support.html>

The published release note includes improved stability/efficiency/performance during power-state transitions and corrected NCQ TRIM error handling. It does not say that garbage-collection scheduling changed.

### P9 — IBM 2009-priority SSD data-management patent — `H/P`, prior-art/control-architecture witness

Roy D. Cideciyan, Evangelos S. Eleftheriou, Robert Haas, Xiao-Yu Hu, Ilias Iliadis, **“Data management in solid state storage devices,”** US20120266050A1 / US8904261B2, IBM; priority 17 December 2009; U.S. application publication 18 October 2012:
<https://patents.google.com/patent/US8904261B2/en>

Directly supports for its described embodiment:

- LBA/PBA mapping metadata;
- PI invalidity flags and aggregate PI counts;
- victim selection informed by invalid-page counts;
- recovery and re-storage of still-valid data;
- address-map update after new data placement;
- old-block erase after the map update, with erase allowed immediately or later;
- a bounded detected-power-interruption path that copies transient parity and current-map metadata to Flash before shutdown.

It is **not** used as evidence of M550 firmware internals, commercial deployment, invention priority, or arbitrary-power-cut transaction atomicity.

### F1 — powered-idle follow-on bounded deepening

[Evidence 150 — Crucial SSD Active Garbage Collection: Powered Idle, Sleep States, and Maintenance Opportunity](../evidence/150-crucial-powered-idle-sleep-maintenance-opportunity-deepening.md)

This follow-on is the authoritative location for the power-state/maintenance-opportunity decomposition and its explicit non-claims.

### F2 — period-provenance / named-device experiment follow-on

[Evidence 150 — Crucial 2013–2015 AGC Provenance and m4 Experiment Boundary](../evidence/150-crucial-2013-2015-agc-provenance-experiment-deepening.md)

### F3 — over-provisioning / reserved-capacity follow-on

[Evidence 150 — 2009–2012 Over-Provisioning as Controller Maintenance Reserve](../evidence/150-2009-2012-overprovisioning-reserved-capacity-deepening.md)

This follow-on is the authoritative location for the bounded distinction among host-visible capacity, controller-reserved over-provisioning capacity, OP-pool membership, erased-block readiness, write amplification, and maintenance completion.