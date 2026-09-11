from pathlib import Path

CASE_PATH = Path('cases/150-crucial-m550-active-garbage-collection.md')
EVIDENCE_PATH = Path('evidence/150-crucial-2014-2024-active-garbage-collection-grounding.md')
INDEX_PATH = Path('CASE_INDEX.md')
ROADMAP_PATH = Path('ROADMAP.md')

CASE_TEXT = r'''# Crucial M550 Active Garbage Collection: Idle-Time Reclamation, Live-Data Relocation, and Free-Space Authority

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
'''

EVIDENCE_TEXT = r'''# Evidence 150 — Crucial M550 / Active Garbage Collection grounding, 2014–2024

## Status

**Grounding record for Case 150.**

Target case: [`../cases/150-crucial-m550-active-garbage-collection.md`](../cases/150-crucial-m550-active-garbage-collection.md)

## Research question

Can a named managed SSD ground the relation

`logical retirement / deallocation -> controller-local selective relocation -> erase-block reclamation`

without inventing undocumented firmware details or conflating garbage collection with TRIM or sanitization?

## Result

Yes, with a deliberately layered evidence chain:

1. a first-party 2014 M550 product flyer establishes **Active Garbage Collection** and **TRIM support** as separate named features;
2. a first-party Micron release anchors M550 availability to **18 March 2014**;
3. maintained Crucial support explains current/family-level Active Garbage Collection as controller-local background maintenance needing powered idle opportunity and free space;
4. SNIA provides vendor-neutral period terminology for TRIM versus internal GC and a generic valid-data-relocation-before-erase mechanism;
5. older academic flash-management literature blocks any invention-priority claim for the 2014 product.

The evidence is sufficient to ground the retention relation, but not to reconstruct M550 firmware internals.

---

## Claim table

| Claim | Evidence | Classification | Strength / limit |
|---|---|---|---|
| M550 product flyer revision is 29-Jan-2014 | Crucial M550 flyer | historical record / primary | strong |
| M550 flyer lists both Active Garbage Collection and TRIM support | Crucial M550 flyer | historical record / primary | strong |
| M550 was publicly available under Crucial/Micron brands on 18-Mar-2014 | Micron release | historical record / primary | strong |
| Current Crucial support describes Active GC as controller-local background cleanup | Crucial support | current vendor contract | strong for maintained family description, not 2014 exact internals |
| Current Crucial support says powered idle periods and free space are needed for effective Active GC | Crucial support | current vendor contract | strong current statement; anti-anachronism guard required |
| TRIM indication and internal GC are distinct mechanisms | M550 flyer + SNIA 2011 | historical record + engineering reconstruction | strong distinction; exact firmware coupling unknown |
| Generic SSD GC relocates valid data before erasing source blocks containing invalid data | SNIA 2016 | high-quality industry mechanism source | strong generic mechanism, not M550-specific |
| Flash erase-unit / out-of-place update management predates M550 | Gal & Toledo 2005 | academic prior-art guardrail | strong against invention claim, no direct genealogy |
| Exact M550 victim selection / mapping commit / crash recovery is known | none | blocked | **not established** |
| Active GC proves secure deletion / sanitization | none | blocked | **false / unsupported** |

---

## Source-by-source notes

### 1. Crucial M550 product flyer — revision 01/29/2014

URL:
<https://content.crucial.com/content/dam/crucial/ssd-products/m550/flyer/crucial-m550-ssd-product-flyer-en.pdf>

Observed primary facts:

- document identifies `Crucial M550 Solid State Drive`;
- revision line: `01/29/2014`;
- NAND: `20nm Micron MLC NAND`;
- firmware: `User upgradeable firmware`;
- Advanced Features include `Active Garbage Collection`;
- the next feature line separately lists `TRIM support`;
- power-loss protection, SMART, ECC, and device sleep are also listed.

Interpretive limit:

The flyer proves named-product feature exposure. It does not reveal a block-victim policy, valid-page copy algorithm, GC urgency threshold, mapping metadata transaction, or power-fail state machine. Feature co-presence cannot be turned into undocumented coupling.

### 2. Micron M550 launch / availability record — 18-Mar-2014

URL:
<https://investors.micron.com/static-files/6f3e5f2f-7a82-41b0-b3a0-56c8b4b4c1a1>

Observed primary facts:

- dated `March 18, 2014`;
- identifies M550 as a new personal-storage-class SSD;
- says it is available that day to consumers, businesses and system builders under Crucial and to OEM customers under Micron;
- says M550 tightly integrates Micron NAND and firmware.

Interpretive limit:

The release dates public availability; it does not independently document Active GC internals. Pairing it with the dated product flyer establishes a conservative named-product floor, not an invention date.

### 3. Crucial maintained support — Active Garbage Collection

Origin-hosted localized copies:
<https://www.crucial.jp/support/articles-faq-ssd/ssd-used-to-be-faster-but-has-slowed-down>
<https://www.crucial.es/support/articles-faq-ssd/ssd-used-to-be-faster-but-has-slowed-down>

The maintained article is dated 15-Nov-2024 on surfaced copies.

Observed vendor statements:

- Crucial SSDs have Active Garbage Collection built into the SSD controller;
- it performs background cleanup when the SSD is powered but not actively reading/writing;
- idle periods are needed for it to operate;
- available free space is needed because cleanup involves moving data;
- the feature is presented as useful where TRIM cannot operate normally.

Anti-anachronism rule:

Use this as a **maintained family-level behavior description**, not as proof that M550 firmware in 2014 had the same trigger intervals, threshold values, or scheduling policy. The historical M550 document proves the feature name; the current support page explains the maintained vendor concept.

### 4. SNIA, Trim: The Basics — 29-Jun-2011

URL:
<https://www.snia.org/blog/2011/trim-basics>

Observed institutional statements:

- TRIM is described as a method for the host OS to inform a NAND-flash device which blocks are no longer in use and can be erased;
- drive-internal Garbage Collection is described as performing a similar cleanup task by erasing blocks marked for deletion;
- TRIM requires both OS and SSD support.

Use:

This is a useful pre-2014 terminology/prior-art floor showing that host-provided deallocation knowledge and device-internal garbage collection were already separately discussed. It does not document M550.

### 5. SNIA, Increasing SSD Performance and Lifetime with Multi-stream Technology — 15-Jun-2016

URL:
<https://www.snia.org/educational-library/increasing-ssd-performance-and-lifetime-multi-stream-technology-2016>

The SNIA abstract states that, as SSD writes continue, valid data can fragment across NAND blocks containing invalid/obsolete data; GC relocates valid data to other blocks and then completely erases the original blocks. It also links GC with write amplification and performance cost.

Use:

This is the generic mechanism witness used for engineering reconstruction:

`mixed valid+invalid block -> preserve/relocate valid pages -> erase old block -> recover free space`.

It is explicitly **not** used as evidence that M550 uses the same scheduler, data structures, or internal copy primitive.

### 6. Gal & Toledo, Algorithms and Data Structures for Flash Memories — ACM CSUR 37(2), 2005

Institutional record:
<https://cris.tau.ac.il/en/publications/algorithms-and-data-structures-for-flash-memories/>

The survey records two relevant physical constraints: bits are cleared by erasing a larger block, and erase endurance is limited. It surveys not-in-place update, erase reduction, and wear-leveling algorithms used to make flash practical.

Use:

Only as a broad prior-art guardrail: the erase-management / out-of-place-update problem family was mature before the M550. No direct genealogy to Micron/Crucial firmware is asserted.

---

## Engineering reconstruction

The sources jointly support the following bounded state decomposition:

```text
logical/current host data
        |
        | overwrite/delete/deallocation knowledge
        v
some old physical pages cease to be required as current payload
        |
        | but erase operates at a larger block granularity
        v
mixed block: stale pages + still-live pages
        |
        | GC preserves/relocates live pages
        v
old block loses current-data obligations
        |
        | erase
        v
reusable physical capacity
```

Key distinctions:

- **logical currentness:** which host-visible content is authoritative;
- **reclaim eligibility:** which physical embodiments no longer need to remain current;
- **relocation obligation:** which still-live content must survive before erasing a mixed block;
- **reclaim completion:** the old erase block actually becomes reusable;
- **sanitization:** a separate security property not established by ordinary GC.

This decomposition explains why `delete`, `TRIM`, `GC`, and `sanitize` cannot be used as synonyms.

---

## Stop conditions

The following claims are intentionally blocked:

1. **Exact M550 algorithm.** No inspected first-party source exposes victim selection, wear-leveling coupling, valid-page-copy primitive, or mapping commit order.
2. **Idle-only GC.** Current Crucial support explains idle-time Active GC; it does not prove M550 never performed urgent/foreground reclamation.
3. **Exact free-space threshold.** The current support recommendation is operational guidance, not a 2014 firmware constant.
4. **Power-fail atomicity.** M550 lists power-loss protection, but no source ties that feature to a specific GC transaction protocol.
5. **Sanitization.** Ordinary GC is not documented as device-wide secure purge, cryptographic erase, or verified forensic irrecoverability.
6. **Invention priority.** 2011 SNIA and earlier flash-management literature predate the named M550 witness; no first-inventor claim is made.
7. **Genealogy.** Chronology does not establish design descent from Gal/Toledo, SNIA, another SSD vendor, or a specific controller architecture.

---

## Cross-case evidence notes

- **Case 04:** use for logical-to-physical remapping/currentness; Case150 adds selective reclamation of mixed erase blocks.
- **Case 39:** use for an explicit FTL crash-recovery implementation; do not fill M550's crash-protocol gap by analogy.
- **Case 145:** raw-Flash JFFS2 exposes obsolete-node and erase/reuse evidence in open source; managed SSD GC hides corresponding details behind firmware.
- **Case 84:** ZNS shifts parts of placement/reclamation responsibility across the host/device boundary; functional comparison only.
- **Cases 44/47:** retain sanitize/remanence authority; do not promote GC erase to secure erase.

---

## Related-repository check

A fresh code search in `tmzncty/computing-archaeology` for `SSD garbage collection FTL` returned no dedicated study. Therefore this bounded retention case does not duplicate a known companion-repository package.

If expanded later, broad FTL history, early commercial SSD garbage collection, controller lineages, and product scheduler evolution should move to `computing-archaeology`; `technical-retention` should retain only the state/reclamation relation and cross-case comparison.
'''

INDEX_ROW = r'''| [Crucial M550 Active Garbage Collection: Idle-Time Reclamation, Live-Data Relocation, and Free-Space Authority](cases/150-crucial-m550-active-garbage-collection.md) | **grounded** | managed NAND SSD + named Active Garbage Collection + separate TRIM signal + live-data relocation before erase-block reclamation | distinguish logical retirement from physical reclaim; TRIM knowledge from GC execution; idle host from controller inactivity; live relocation from logical mutation; reclamation from sanitization | [2014 M550 product grounding + 2011/2016 SNIA + maintained Crucial support](evidence/150-crucial-2014-2024-active-garbage-collection-grounding.md); exact firmware GC algorithm, crash protocol, historical support-page recovery, and device tracing remain open |'''

FINDINGS = r'''## Case 150 — Crucial M550 Active Garbage Collection findings

Grounding record: [`evidence/150-crucial-2014-2024-active-garbage-collection-grounding.md`](evidence/150-crucial-2014-2024-active-garbage-collection-grounding.md).

- **3234 — 2014 named-product floor != invention date:** Crucial's 29-Jan-2014 M550 flyer lists Active Garbage Collection and TRIM support, while Micron anchors product availability to 18-Mar-2014; earlier records prevent an invention-priority reading. (`H/P`, `X`)
- **3235 — feature listing != exact firmware algorithm:** M550 documentation establishes the feature but not victim selection, copy primitive, mapping transaction, threshold, or scheduler. (`H/P`, `E`, `X`)
- **3236 — Active Garbage Collection != TRIM:** the M550 flyer lists them separately, and SNIA's period vocabulary distinguishes host deallocation knowledge from device-internal cleanup. (`H/P`, `E`)
- **3237 — host deletion/deallocation != physical erase:** retiring logical data can make old embodiments unnecessary without proving the containing NAND block has been erased. (`E`)
- **3238 — reclaim eligibility != reclaim completion:** knowing that pages are stale supplies permission/opportunity for reclamation but is not evidence that free erased capacity already exists. (`E`)
- **3239 — stale page != whole mixed block disposable:** generic SSD GC must preserve valid pages sharing a victim erase block before that block can be erased. (`E`)
- **3240 — live-data relocation != host-visible logical mutation:** GC can move still-current payload to a new physical embodiment while preserving logical currentness. (`E`, `A`)
- **3241 — forgetting stale embodiments can require preserving live state first:** selective erase-block reclamation is retention-preserving and forgetting-producing in the same transition. (`E`, `Φ`)
- **3242 — logical free capacity != immediately programmable physical free pages:** managed SSD namespace availability and the controller's erased/free-block pool are distinct state layers. (`E`)
- **3243 — host idle != controller inactive:** maintained Crucial support explicitly treats powered idle time as an opportunity for controller-local Active Garbage Collection. (`H/P`, `E`)
- **3244 — powered idle != powered off:** Crucial's support guidance requires power while avoiding active I/O, making energy availability part of the maintenance opportunity. (`H/P`, `E`)
- **3245 — maintenance opportunity != maintenance completion:** an idle interval enables GC but does not by itself prove which blocks were reclaimed or that all maintenance debt is gone. (`E`, `X`)
- **3246 — lack of idle opportunity != immediate data invalidity:** garbage-collection pressure can manifest as performance/reclamation debt without implying current logical payload has already become incorrect. (`E`, `X`)
- **3247 — free-space recommendation != fixed historical firmware threshold:** maintained Crucial guidance about free space must not be back-projected as an M550 2014 constant. (`H/P`, `E`, `X`)
- **3248 — current Crucial family description != exact 2014 M550 scheduler:** the 2024 support page explains maintained behavior but cannot supply undocumented 2014 trigger timing or foreground/urgent-GC rules. (`H/P`, `X`)
- **3249 — M550 power-loss protection feature != documented GC crash protocol:** co-presence of PLP and GC does not reveal commit ordering or interrupted-relocation recovery. (`H/P`, `X`)
- **3250 — ordinary GC erase != sanitization:** capacity reclamation is not documented as device-wide purge, cryptographic erase, or verified forensic irrecoverability. (`E`, `X`)
- **3251 — Case145 JFFS2 GC != managed-SSD hidden GC:** both relocate live data before erase, but JFFS2 exposes filesystem node/version/reuse evidence while a managed SSD hides mapping/reclaim state behind firmware. (`A`, `X`)
- **3252 — Case84 ZNS authority shift != proof that all GC disappears:** ZNS changes the host/device placement-reclamation boundary and can reduce hidden GC pressure, but it is not the same state machine as M550 Active GC. (`A`, `X`)
- **3253 — related-repository boundary:** fresh `tmzncty/computing-archaeology` search found no dedicated SSD-GC study; broad FTL/commercial-GC genealogy belongs there while Case150 retains the bounded reclamation relation. (`H/P` project-state record)
'''

ROADMAP_ENTRY = r'''- [x] **Case 150 Crucial M550 Active Garbage Collection / managed-SSD reclaim slice** — [`cases/150-crucial-m550-active-garbage-collection.md`](cases/150-crucial-m550-active-garbage-collection.md), grounded by [`evidence/150-crucial-2014-2024-active-garbage-collection-grounding.md`](evidence/150-crucial-2014-2024-active-garbage-collection-grounding.md): Crucial's revision-dated 29-Jan-2014 M550 flyer lists Active Garbage Collection and TRIM support as separate features and Micron anchors M550 availability to 18-Mar-2014. Maintained Crucial support supplies the current family-level `powered idle -> background cleanup` and free-space relation, while SNIA supplies the generic `preserve/relocate live pages -> erase mixed old block -> recover free capacity` mechanism. The slice fixes `logical retirement != physical reclamation`, `TRIM knowledge != GC execution`, `host idle != controller inactivity`, `live relocation != logical mutation`, and `ordinary GC != sanitize`. Exact M550 victim policy, GC crash protocol, a period 2010–2014 support-page copy, and named-device traces remain open; fresh `computing-archaeology` search found no dedicated SSD-GC study to reuse.'''

# Concurrency / duplicate guards.
index = INDEX_PATH.read_text(encoding='utf-8')
roadmap = ROADMAP_PATH.read_text(encoding='utf-8')
if CASE_PATH.exists() or EVIDENCE_PATH.exists():
    raise SystemExit('Case150 target already exists; refusing duplicate')
if '3234 —' in index:
    raise SystemExit('finding 3234 already occupied; concurrent index advance requires renumbering')
if '3233 — related-repository boundary' not in index:
    raise SystemExit('expected Case149 terminal finding 3233 not found; concurrent state changed')
if 'cases/149-micron-nand-otp-data-protect-irreversible-authority.md' not in index:
    raise SystemExit('expected Case149 index row missing')
if 'Case 150 Crucial M550 Active Garbage Collection / managed-SSD reclaim slice' in roadmap:
    raise SystemExit('Case150 already present in ROADMAP; refusing duplicate')
if 'Case 149 Micron NAND OTP Data Protect irreversible-authority slice' not in roadmap:
    raise SystemExit('expected Case149 roadmap state missing')

CASE_PATH.parent.mkdir(parents=True, exist_ok=True)
EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
CASE_PATH.write_text(CASE_TEXT.rstrip() + '\n', encoding='utf-8')
EVIDENCE_PATH.write_text(EVIDENCE_TEXT.rstrip() + '\n', encoding='utf-8')

# Insert the case row immediately before the comparison matrix, preserving case-table locality.
marker = '## Comparison matrix — provisional'
if marker not in index:
    raise SystemExit('CASE_INDEX comparison-matrix marker missing')
index = index.replace(marker, INDEX_ROW + '\n' + marker, 1)
index = index.rstrip() + '\n' + FINDINGS.rstrip() + '\n'
INDEX_PATH.write_text(index, encoding='utf-8')

ROADMAP_PATH.write_text(roadmap.rstrip() + '\n' + ROADMAP_ENTRY.rstrip() + '\n', encoding='utf-8')
