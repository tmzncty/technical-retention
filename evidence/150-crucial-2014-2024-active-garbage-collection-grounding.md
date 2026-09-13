# Evidence 150 — Crucial M550 / Active Garbage Collection grounding, 2014–2024

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

### Follow-up deepening — Micron TN-29-60 (2011)

A bounded prior-art/mechanism follow-up is now recorded in [`150-micron-2011-ftl-garbage-collection-prior-art-deepening.md`](150-micron-2011-ftl-garbage-collection-prior-art-deepening.md).

That note adds a Micron-authored April 2011 FTL witness for:

- out-of-place update followed by invalidation of the old physical page;
- explicit garbage-collection sequencing: select candidate block(s), copy still-valid pages, then erase;
- free-page / full-virtual-block pressure as a trigger condition;
- optional background garbage collection during system idle time;
- a documented power-consumption trade-off for that idle-time feature.

This moves the public Micron functional-prior-art floor for the general idle/background FTL-GC pattern to **no later than April 2011**. It does **not** establish Micron invention priority, direct M550 firmware descent, identical algorithms, or a shipping-controller implementation history.

The bounded engineering relation is now strengthened to:

`logical supersession != invalidity != reclamation opportunity != copy/erase execution != reclamation completion`.

### Follow-up deepening — powered-idle maintenance opportunity and host power policy

A second bounded follow-up is recorded in [`150-crucial-powered-idle-maintenance-opportunity-deepening.md`](150-crucial-powered-idle-maintenance-opportunity-deepening.md).

That note re-inspects Crucial's first-party maintained support procedure and records the operational details that the earlier grounding deliberately left qualitative:

- Active Garbage Collection is described as controller-local cleanup while the SSD is **powered** but not actively reading/writing;
- Crucial recommends at least **10% free capacity** for best results;
- a performance-recovery procedure reserves **6–8 hours** of powered idle time, for example in BIOS/UEFI or macOS Startup Manager;
- Crucial explicitly recommends host power settings that keep SATA/NVMe SSDs powered/available during otherwise idle periods.

The bounded engineering result is:

`host inactivity != guaranteed device maintenance opportunity != maintenance completion`.

The `6–8 h` interval is treated as a vendor runbook window, **not** a firmware completion SLA; the `10%` figure is treated as an operational recommendation, **not** a published GC trigger threshold. The current family-level procedure is not back-projected as exact 2014 M550 firmware behavior.

---

## Claim table

| Claim | Evidence | Classification | Strength / limit |
|---|---|---|---|
| M550 product flyer revision is 29-Jan-2014 | Crucial M550 flyer | historical record / primary | strong |
| M550 flyer lists both Active Garbage Collection and TRIM support | Crucial M550 flyer | historical record / primary | strong |
| M550 was publicly available under Crucial/Micron brands on 18-Mar-2014 | Micron release | historical record / primary | strong |
| Current Crucial support describes Active GC as controller-local background cleanup | Crucial support | current vendor contract | strong for maintained family description, not 2014 exact internals |
| Current Crucial support says powered idle periods and free space are needed for effective Active GC | Crucial support | current vendor contract | strong current statement; anti-anachronism guard required |
| Current Crucial support recommends a 6–8 h powered-idle recovery window | Crucial support | current vendor runbook | strong for the procedure; **not** a GC completion-time guarantee |
| Current Crucial support recommends keeping at least 10% free for best results | Crucial support | current vendor runbook | strong recommendation; **not** an exact firmware threshold |
| Host power-management settings can be changed to preserve the vendor-recommended powered-idle opportunity | Crucial support | current vendor runbook + engineering reconstruction | strong for the operational procedure; exact SATA/NVMe controller-state semantics unknown |
| TRIM indication and internal GC are distinct mechanisms | M550 flyer + SNIA 2011 | historical record + engineering reconstruction | strong distinction; exact firmware coupling unknown |
| Generic SSD GC relocates valid data before erasing source blocks containing invalid data | SNIA 2016 | high-quality industry mechanism source | strong generic mechanism, not M550-specific |
| Micron publicly documented an FTL select/copy/erase GC sequence and optional idle-time background feature by Apr-2011 | Micron TN-29-60 | historical record / vendor technical note | strong for generic SLC FTL guidance; not M550 firmware genealogy |
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

Origin-hosted localized copy:
<https://www.crucial.es/support/articles-faq-ssd/ssd-used-to-be-faster-but-has-slowed-down>

The maintained article is dated 15-Nov-2024 on surfaced copies.

Observed vendor statements:

- Crucial SSDs have Active Garbage Collection built into the SSD controller;
- it performs background cleanup when the SSD is powered but not actively reading/writing;
- idle periods are needed for it to operate;
- available free space is needed because cleanup involves moving data;
- the feature is presented as useful where TRIM cannot operate normally;
- at least **10% free capacity** is recommended for best results;
- a degraded-performance recovery procedure leaves the SSD powered and idle for **6–8 hours**;
- the same procedure recommends host power settings that prevent the SSD from being powered down during the intended maintenance window.

Anti-anachronism rule:

Use this as a **maintained family-level behavior description and runbook**, not as proof that M550 firmware in 2014 had the same trigger intervals, free-space threshold, scheduler, SATA/NVMe power-state handling, or 6–8-hour completion behavior. The historical M550 document proves the feature name; the current support page explains the maintained vendor concept and operator procedure.

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

### 6. Gal & Toledo, Algorithms and Data Structures for Flash Memories — ACM CSUR 37(2), June 2005

Institutional record:
<https://cris.tau.ac.il/en/publications/algorithms-and-data-structures-for-flash-memories/>

The survey records two relevant physical constraints: bits are cleared by erasing a larger block, and erase endurance is limited. It surveys not-in-place update, erase reduction, and wear-leveling algorithms used to make flash practical.

Use:

Only as a broad prior-art guardrail: the erase-management / out-of-place-update problem family was mature before the M550. No direct genealogy to Micron/Crucial firmware is asserted.

### 7. Micron TN-29-60, Garbage Collection in SLC NAND Flash Memory — Rev. G 4/11 — `H/P`

Historical Micron URL:
<https://www.micron.com/~/media/documents/products/technical-note/nand-flash/tn2960-garbage-collection-slc-nand.pdf>

Accessible preserved text copy inspected:
<https://studylib.net/doc/18193030/garbage-collection-in-slc-nand-flash-memory>

The Micron-authored note explicitly describes an FTL garbage-collection algorithm in which out-of-place writes leave old physical pages invalid, garbage collection selects candidate blocks, copies still-valid pages to free space, then erases the selected physical block(s). It also describes an optional background feature that activates garbage collection during system idle time, while noting a power-consumption trade-off.

Use:

This is a pre-M550 vendor-authored functional-prior-art and mechanism witness. It does **not** prove that M550 firmware is an implementation of the note, or that Micron first invented any of these mechanisms in 2011. See the dedicated deepening evidence linked above for claim typing and stop conditions.

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

TN-29-60 further lets the project separate **maintenance demand** from **maintenance opportunity**: a free-page threshold can create reclamation pressure, while an idle interval can provide an opportunity to perform the work earlier. Therefore `GC due/pressured != idle opportunity != GC execution != completion`.

The maintained Crucial runbook sharpens `idle opportunity` into a cross-layer condition. In the vendor's procedure, application/user inactivity is insufficient by itself: the SSD must remain powered, and Crucial explicitly changes host power settings to preserve that device-level condition. Therefore the project can now use the more precise bounded relation:

`host inactivity != powered-device maintenance opportunity != GC completion`.

The recommended **6–8 h** interval is evidence for reserving a maintenance window, not for a controller completion deadline. Likewise, the **10%** free-space recommendation is an operator guideline, not a demonstrated firmware threshold.

---

## Stop conditions

The following claims are intentionally blocked:

1. **Exact M550 algorithm.** No inspected first-party source exposes victim selection, wear-leveling coupling, valid-page-copy primitive, or mapping commit order.
2. **Idle-only GC.** Current Crucial support explains idle-time Active GC; it does not prove M550 never performed urgent/foreground reclamation.
3. **Exact free-space threshold.** The current support `10%` recommendation is operational guidance, not a 2014 firmware constant or universal trigger.
4. **Six-to-eight-hour completion SLA.** The interval is a vendor runbook opportunity window; no inspected source makes it a guaranteed GC deadline.
5. **Specific low-power-state semantics.** Host power-setting guidance does not expose SATA DEVSLP/HIPM/DIPM, NVMe APST, or controller-state internals.
6. **Power-fail atomicity.** M550 lists power-loss protection, but no source ties that feature to a specific GC transaction protocol.
7. **Sanitization.** Ordinary GC is not documented as device-wide secure purge, cryptographic erase, or verified forensic irrecoverability.
8. **Invention priority.** Micron TN-29-60 (2011), SNIA 2011, and earlier flash-management literature predate the named M550 witness; no first-inventor claim is made.
9. **Genealogy.** Chronology does not establish M550 design descent from TN-29-60, Gal/Toledo, SNIA, another SSD vendor, or a specific controller architecture.

---

## Cross-case evidence notes

- **Case 04:** use for logical-to-physical remapping/currentness; Case150 adds selective reclamation of mixed erase blocks.
- **Case 39:** use for an explicit FTL crash-recovery implementation; do not fill M550's crash-protocol gap by analogy.
- **Case 135:** both cases expose controller-owned maintenance that depends on a host-created service opportunity. Case135 uses a reset/time command window, bus-idle gating and ECC-threshold selection; Case150C uses a powered-idle operator runbook. Functional comparison only; no shared algorithm or genealogy is claimed.
- **Case 145:** raw-Flash JFFS2 exposes obsolete-node and erase/reuse evidence in open source; managed SSD GC hides corresponding details behind firmware.
- **Case 84:** ZNS shifts parts of placement/reclamation responsibility across the host/device boundary; functional comparison only.
- **Cases 44/47:** retain sanitize/remanence authority; do not promote GC erase to secure erase.

---

## Related-repository check

A fresh code search in `tmzncty/computing-archaeology` for `active garbage collection` returned no dedicated study. Therefore this bounded retention case does not duplicate a known companion-repository package.

If expanded later, broad FTL history, early commercial SSD garbage collection, controller lineages, SATA/NVMe power-state genealogy, and product scheduler evolution should move to `computing-archaeology`; `technical-retention` should retain only the state/reclamation/maintenance-opportunity relation and cross-case comparison.
