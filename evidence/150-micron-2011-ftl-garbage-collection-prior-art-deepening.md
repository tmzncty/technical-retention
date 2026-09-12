# Evidence 150B — Micron TN-29-60 (2011): FTL Garbage-Collection Prior Art

## Status

**`grounded`**

Target case: [`../cases/150-crucial-m550-active-garbage-collection.md`](../cases/150-crucial-m550-active-garbage-collection.md)

Companion grounding: [`150-crucial-2014-2024-active-garbage-collection-grounding.md`](150-crucial-2014-2024-active-garbage-collection-grounding.md)

## Scope

This evidence note deepens Case 150 on one bounded question:

> **How far back can a Micron-authored technical record directly document the general flash-translation-layer garbage-collection pattern that later Crucial material calls background / Active Garbage Collection, without turning chronology into an unsupported M550 firmware genealogy?**

Claim classes used here:

- **A — historical record:** what Micron TN-29-60 actually says;
- **B — engineering reconstruction:** state distinctions implied by the documented mechanism;
- **D — functional analogy / prior-art comparison:** the bounded relation between the 2011 FTL note and the 2014 Crucial M550 product/support record.

No direct code lineage, controller lineage, or invention-priority claim is made.

---

## Source and provenance

### P1 — Micron Technology, TN-29-60, Rev. G 4/11 — `H/P`

Micron Technology, Inc., **“Garbage Collection in SLC NAND Flash Memory,”** Technical Note TN-29-60, Revision G, April 2011.

Historical Micron URL recorded for the note:

<https://www.micron.com/~/media/documents/products/technical-note/nand-flash/tn2960-garbage-collection-slc-nand.pdf>

Publicly accessible preserved text copy inspected for this research:

<https://studylib.net/doc/18193030/garbage-collection-in-slc-nand-flash-memory>

The preserved copy identifies itself as Micron TN-2960 / TN-29-60, carries `Rev. G 4/11 EN`, and includes Micron's 2011 copyright line. The original Micron URL is retained as provenance but was not directly retrievable during this research pass. The mirror is therefore used as a preservation witness for a Micron-authored technical note, not as an independent publisher.

The note explicitly describes a **recommended garbage-collection algorithm to be implemented in FTL software for NAND Flash memory devices**. It is a generic SLC NAND / FTL engineering note, not an M550 firmware manual.

---

## Historical record — FTL mapping and out-of-place invalidation

**Classification: A — historical record.**

TN-29-60 describes the Flash Translation Layer as a software layer between the file system and NAND. It says the FTL translates virtual addresses to physical addresses and includes wear-leveling and garbage-collection software modules.

It then explains the erase-before-rewrite problem in explicitly out-of-place terms. Rather than erasing a block immediately for an overwrite, the FTL can write the new data to another physical page and mark the previous physical page's data **invalid**.

This gives a period Micron-authored witness for the distinction:

```text
new logical version becomes current
        ↓
new physical page receives that version
        ↓
old physical page becomes invalid
        ↓
old physical capacity is not yet necessarily reusable
```

Historical wording such as `virtual`, `physical`, `invalid`, `garbage collection`, and `FTL` belongs to the source. The repository terms **currentness**, **reclaim eligibility**, and **reclamation debt** are later engineering reconstructions.

---

## Historical record — garbage collection is a select/copy/erase transition

**Classification: A — historical record.**

TN-29-60 gives an explicit three-step basic garbage-collection sequence:

1. virtual blocks meeting the garbage-collection condition are selected for erasure;
2. still-valid physical pages are copied to a free area;
3. the selected physical blocks are erased.

The note also states that garbage collection is used to free space occupied by invalid data so further PROGRAM operations can proceed.

This directly supports a mechanism boundary that Case 150 previously had to ground with more generic later material:

```text
invalid pages exist
        ≠
whole physical block immediately disposable

selected mixed block
        ↓
copy still-valid pages elsewhere
        ↓
erase selected physical block(s)
        ↓
recover reusable space
```

The source therefore documents selective preservation as part of reclamation: live payload is moved before the erase unit containing stale payload is retired.

---

## Historical record — trigger pressure and background opportunity are distinct

**Classification: A — historical record.**

TN-29-60 gives two trigger-style conditions for garbage collection:

- when a virtual block is full; or
- when the number of free pages in the device falls below a specified threshold.

Separately, its **Background Feature** section says an FTL can activate garbage collection during system idle time. The purpose is to make long NAND erase latency transparent by freeing space automatically during idle intervals rather than waiting until incoming writes exhaust the remaining free-page pool.

The same section also records an operational cost: if background garbage collection runs while the FTL is otherwise not reading or writing NAND, power consumption will not fall as it otherwise might, so Micron does not recommend the background feature where low power consumption is required.

Thus the 2011 source itself separates:

- **maintenance pressure / trigger:** free-page shortage or a full virtual block;
- **maintenance opportunity / scheduling:** idle time in which work may be brought forward;
- **execution cost:** copying/erasing work consumes NAND operations and energy.

It does not describe these categories with the repository's vocabulary, but the underlying facts are source-grounded.

---

## Engineering reconstruction — invalidity, reclaimability, and erasure are different states

**Classification: B — engineering reconstruction.**

The source supports the following decomposition:

```text
logical overwrite
        ↓
old physical page marked invalid
        ↓
invalid space contributes to reclamation pressure
        ↓
victim / candidate selected
        ↓
valid co-residents copied elsewhere
        ↓
physical erase
        ↓
capacity becomes reusable
```

Therefore:

- `logical supersession != physical erase`;
- `invalid page != erased page`;
- `invalid page exists != containing block can be erased without preservation work`;
- `reclaim eligibility != reclaim execution`;
- `reclaim execution != reclaim completion`;
- `free-page pressure != idle opportunity`.

The last distinction matters for Case 150. A controller may owe reclamation work because internal free space is scarce even when it has not yet received a convenient idle interval. Conversely, an idle interval is only an opportunity; the source does not establish that every idle interval necessarily starts or completes garbage collection.

---

## Engineering reconstruction — forgetting stale embodiments can require carrying live state forward

**Classification: B — engineering reconstruction.**

The three-step Micron sequence provides a compact physical example of selective forgetting:

```text
mixed physical block
  ├─ invalid / stale pages
  └─ still-valid pages
          ↓
retain continuity of still-valid payload by copying it
          ↓
remove currentness obligations from the old block
          ↓
erase the old block
```

This justifies the bounded Case-150 proposition that **reclamation can depend on preservation**. The controller cannot safely reclaim a mixed erase unit merely because some contained pages are stale.

The proposition is mechanism-level only. It is not a claim about human memory, archives, or philosophical forgetting.

---

## Functional prior-art comparison to Crucial M550 / Active Garbage Collection

**Classification: D — functional analogy / prior-art guardrail.**

Case 150's named-product anchor is the Crucial/Micron M550 in 2014. TN-29-60 establishes that **by April 2011 Micron was already publishing a general FTL design in which garbage collection can run as a background feature during system idle time and performs valid-page copy before block erase**.

That chronology is enough to reject any reading in which the 2014 M550 marketing/support record is treated as the origin of idle/background flash garbage collection.

The safe claim is:

> **Micron-authored public technical material documents the general FTL background-GC pattern no later than April 2011; the 2014 M550 record is a later named managed-SSD embodiment witness.**

The following stronger claims are **not** supported:

- the M550 firmware directly implements the exact TN-29-60 reference algorithm;
- M550's controller code descends from this technical note;
- the M550 uses identical victim-selection thresholds, virtual-block structures, SLC assumptions, or copy policies;
- Micron invented flash garbage collection in 2011;
- April 2011 is the earliest industry implementation or publication of background garbage collection.

The note concerns generic SLC NAND FTL software. M550 is a later managed MLC SSD product. Similar functional structure does not collapse those implementation domains.

---

## TRIM / deallocation boundary

TN-29-60's basic mechanism does not need host TRIM semantics to establish invalid-page reclamation. It describes FTL-local invalidation after out-of-place updates and subsequent reclamation.

Case 150's later M550 record separately exposes both `TRIM support` and `Active Garbage Collection`.

The combined bounded interpretation is:

- host-provided deallocation information may increase the set of physical embodiments that no longer need to remain current;
- FTL-local overwrite invalidation can also create reclaimable stale pages;
- neither fact is itself the physical block erase;
- garbage collection remains a separate select/copy/erase transition.

Therefore:

`TRIM/deallocation knowledge != invalid-page reclamation != physical erase completion`.

This is a state distinction, not a claim that all SSDs couple TRIM and garbage collection identically.

---

## Sanitization boundary

Nothing in TN-29-60 upgrades normal garbage collection into a security sanitization contract.

The note optimizes reusable space and sustainable throughput. Its erase operations target blocks selected by the FTL's capacity-management algorithm. It does not state that ordinary garbage collection:

- discovers every historical embodiment of a host object;
- purges remapped/spare/cache copies;
- implements a sanitize standard;
- supplies externally verifiable forensic irrecoverability.

Thus:

`block erased for GC != device-wide sanitize completion`.

Case 44 / Case 47 remain the stronger repository locations for sanitize/remanence authority.

---

## Power / idle boundary

TN-29-60 explicitly records a performance-versus-power trade-off for idle background garbage collection. It does **not** document crash consistency for an interrupted GC cycle.

Do not infer from this note:

- durable mapping-journal format;
- atomic victim-block commit sequence;
- power-loss recovery algorithm;
- capacitor-backed completion;
- whether a particular shipping SSD resumes, rolls back, scans, or reconstructs an interrupted move.

So:

`powered idle opportunity != documented durable GC transaction protocol`.

That gap remains open for a shipping controller / firmware implementation witness.

---

## Cross-case comparison

### Case 04 — FTL logical/physical identity

Case 04 supplies the broader logical-to-physical remapping relation. TN-29-60 adds a concrete reason for relocation: live pages can be moved specifically so a mixed erase unit may be reclaimed.

### Case 39 — explicit FTL crash recovery

Case 39 remains the appropriate place for a documented FTL recovery state machine. TN-29-60 does not fill Case 150's crash-consistency evidence debt.

### Case 44 / Case 47 — deallocation and sanitization

The 2011 Micron note reinforces the distinction between logical invalidity and later physical reclamation. It does not convert ordinary reclamation into a purge guarantee.

### Case 145 — JFFS2 garbage collection

Both cases can use the functional pattern `preserve live state -> reclaim an erase unit`, but JFFS2 exposes its metadata and state machine in open source while managed-SSD FTL policy remains controller-local. Shared vocabulary is not mechanism identity.

---

## Related-repository check

A fresh search of `tmzncty/computing-archaeology` for `TN-29-60`, `garbage collection NAND`, and `FTL NAND` found no dedicated technical-history package to reuse.

Accordingly, this note keeps only the retention / reclamation mechanism and bounded prior-art result. A broader genealogy of FTL algorithms, early NAND management software, commercial SSD controller families, or first-introduction claims belongs in `computing-archaeology` if pursued later.

---

## Stop conditions / rejected claims

The following statements are deliberately blocked:

1. **“Micron invented flash garbage collection in 2011.”** Not established.
2. **“TN-29-60 is the M550 firmware design document.”** False / unsupported.
3. **“The M550 implements the exact TN-29-60 algorithm.”** Not established.
4. **“Background means idle-only.”** The note documents an optional idle-time feature, not a universal scheduler law for shipping SSDs.
5. **“Invalid means physically erased.”** Contradicted by the select/copy/erase sequence.
6. **“Garbage collection means sanitize.”** Unsupported.
7. **“The preserved mirror alone proves byte-identical archival provenance.”** Not established; the original Micron URL remains the provenance anchor, while the mirror is the accessible preservation witness inspected in this pass.
8. **“The 2011 note proves a direct genealogy to Crucial's 2014 product.”** Chronology and functional similarity are insufficient.

---

## Remaining evidence debt

1. Recover an archived first-party copy of the original Micron TN-29-60 PDF and record a stable hash/facsimile provenance chain.
2. Find a shipping managed-SSD controller / firmware document that exposes its actual GC trigger, victim-selection, relocation-commit, and recovery state machine.
3. Find M550-specific telemetry or traces showing background maintenance before/after powered-idle treatment.
4. Quantify product-specific idle timing, urgency transition, and interruption behavior without back-projecting current Crucial support guidance.
5. Route broader pre-2011 FTL / background-GC genealogy to `computing-archaeology` rather than turning this bounded retention case into a flash-history survey.
