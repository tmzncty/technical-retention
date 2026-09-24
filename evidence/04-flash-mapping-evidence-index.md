# Case 04 — Flash mapping / relocation evidence index

## Status

**Case maturity: `grounded`**.

This index is navigation and evidence-layer control for [`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md). It does not promote the case beyond the maturity stated by the parent case / authoritative ledger.

Case 04 asks how logical identity survives physical relocation, how one embodiment becomes current while another is retired, and what evidence is required before old physical space can safely return to reuse.

The current anti-collapse rule is:

```text
physical nonvolatility
    != logical currentness
    != relocation completion
    != integrity qualification
    != crash-recoverable mapping authority
    != reclaim eligibility
    != erase completion
    != erase success
    != future reuse admission
```

---

## Evidence chain 1 — NAND device geometry before FTL semantics

**Packet:** [`04-1987-1989-nand-device-geometry-before-ftl-deepening.md`](04-1987-1989-nand-device-geometry-before-ftl-deepening.md)

Late-1980s Toshiba / NAND-structure literature establishes a device-level floor for NAND strings, pages, block erase, random read, and dense nonvolatile-array geometry.

It does **not** establish FTL mapping, logical-to-physical remapping, garbage-collection policy, or crash-recoverable mapping authority.

```text
NAND page/block geometry
    != FTL semantics
```

---

## Evidence chain 2 — 1993–1995 virtual mapping and logical identity

**Parent case:** [`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md)

The Amir Ban / M-Systems `Flash file system` patent directly grounds virtual versus physical address space, a retained virtual map, out-of-place replacement, logical-unit continuity across physical movement, logical invalidation before later physical erase, and relocation of still-current data before reclaim.

Core relation:

```text
same logical object
    != same physical location

payload survives somewhere
    != which payload instance currently counts is self-evident
```

This source does not define every later FTL or a universal power-failure protocol.

---

## Evidence chain 3 — Ban issued-patent facsimile / ordering boundary

**Packet:** [`04-ban-1993-1995-patent-facsimile-ordering-boundary-deepening.md`](04-ban-1993-1995-patent-facsimile-ordering-boundary-deepening.md)

Direct inspection of U.S. Patent 5,404,485 adds page/figure/claim anchors but also exposes an important internal ordering limit. One high-level write paragraph can be read as allocation/currentness changes before replacement-data write, while the FIG. 6 explanation and claim 1 put replacement-data write before allocation/map changes.

Therefore:

```text
all transition steps appear in the patent
    != one unambiguous durable update order is specified
    != crash-atomic publication is proven
```

The facsimile remains useful for transfer-unit rules, stable logical identity, Flash-resident primary map, map-block update, and startup reconstruction of volatile mapping state.

---

## Evidence chain 4 — FTL terminology / standardization chronology

**Packet:** [`04-ftl-1995-1996-terminology-standardization-addendum.md`](04-ftl-1995-1996-terminology-standardization-addendum.md)

This packet separates:

```text
public FTL term use by February 1995
    != reported PCMCIA approval by August 1995
    != later-reported specification release in May 1996
```

It provides a terminology floor without claiming first coinage or silently replacing earlier actor vocabulary with later FTL terminology.

---

## Evidence chain 5 — 2008–2014 FTL crash recovery / reconstructed authority

**Packet:** [`04-2008-2014-ftl-power-off-crash-recovery-deepening.md`](04-2008-2014-ftl-power-off-crash-recovery-deepening.md)

Especially through directly inspected DCR 2014, this chain separates the latest volatile working map, the last durable checkpoint/recovery base, newer on-Flash evidence, and the reconstructed post-crash authoritative map.

```text
latest volatile mapping state
    != latest durable recovery base
    != final reconstructed mapping after restart
```

A logical identity can survive loss of the exact runtime map when enough persistent evidence remains to construct a successor authoritative map. DCR is a specific FTL design, not a universal commercial-SSD model.

---

## Evidence chain 6 — Samsung raw-NAND Copy-Back integrity boundary

**Packet:** [`04-samsung-2004-2010-nand-copyback-integrity-boundary-deepening.md`](04-samsung-2004-2010-nand-copyback-integrity-boundary-deepening.md)

Samsung manufacturer documentation separates physical Copy-Back relocation from payload qualification. Earlier parts warn that source-page charge-loss errors can be propagated/accumulated by repeated Copy-Back; later parts expose source-read, controller-visible bit-error checking, optional correction/reload, and destination programming.

```text
Copy-Back program completion
    != source payload revalidated

new physical embodiment exists
    != intended logical payload has been qualified
```

The device datasheets do not establish FTL publication order, old-page retirement order, or higher-level crash atomicity.

---

## Evidence chain 7 — 2001–2003 interrupted erase / completion-state recovery

**Packet:** [`04-m-systems-2001-2003-interrupted-erase-recovery-deepening.md`](04-m-systems-2001-2003-interrupted-erase-recovery-deepening.md)

M-Systems evidence adds a distinct erase-interruption seam. A power failure during destructive maintenance cannot be treated as though erase completion were self-evident; persistent pending/completed state participates in restart recovery.

The key boundary is:

```text
erase was initiated
    != erase completion was established

controller restarted
    != interrupted destructive maintenance can be forgotten
```

This chain concerns **absence of a trustworthy completion verdict after interruption**. It must remain distinct from Evidence chain 10 below, where an operation reaches the status-verdict point and explicitly reports failure.

---

## Evidence chain 8 — 2003–2004 TrueFFS mapping reconstruction after power failure

**Packet:** [`04-trueffs-2003-2004-mapping-power-failure-reconstruction-deepening.md`](04-trueffs-2003-2004-mapping-power-failure-reconstruction-deepening.md)

TrueFFS material deepens the restart side of mapped Flash: current logical-to-physical authority need not survive as one intact volatile object if enough on-media metadata remains to rebuild it after power failure.

```text
runtime mapping object survives
    != mapping authority survives

persistent evidence + reconstruction
    can produce successor authority
```

This is mapping-recovery evidence, not proof of a universal SSD FTL or a universal atomic-write contract.

---

## Evidence chain 9 — 2007–2010 T13 TRIM / logical invalidation / read-semantics boundary

**Packet:** [`04-t13-2007-2010-trim-logical-invalidation-read-semantics-deepening.md`](04-t13-2007-2010-trim-logical-invalidation-read-semantics-deepening.md)

This chain keeps host-visible deallocation separate from physical erasure. TRIM/DATA SET MANAGEMENT can communicate that logical ranges are no longer needed, while subsequent read behavior and actual physical reclamation remain separately specified/implemented.

```text
host deallocation intent
    != controller logical invalidation
    != physical erase
    != sanitization
```

It should not be used to back-project modern TRIM semantics onto the 1993 mapping patent.

---

## Evidence chain 10 — 2011–2014 Micron raw-NAND erase status / reuse qualification

**Packet:** [`04-micron-2011-2014-raw-nand-erase-status-reuse-authority-deepening.md`](04-micron-2011-2014-raw-nand-erase-status-reuse-authority-deepening.md)

Micron first-party raw-NAND documentation and bad-block-management guidance add a lower-level qualification step after an erase command has stopped being busy.

The named device contract separates:

```text
ERASE accepted
    -> BUSY
    -> READY
    -> FAIL status checked
        -> success
        or
        -> erase failure / retirement path
```

Micron's datasheet distinguishes `RDY` from `FAIL`: readiness answers whether the target/operation remains busy, while the status verdict answers whether PROGRAM/ERASE/READ succeeded. Bad-block guidance separately treats runtime PROGRAM/ERASE errors as evidence for developed bad blocks, and current Micron support guidance explicitly sends an ERASE-failed block to retirement.

The resulting **engineering reconstruction** is:

```text
logical reclaim eligibility
    != erase command admission
    != temporal completion / ready
    != erase success
    != allocator reuse admission
```

`reuse authority`, `reuse eligibility`, `completion authority`, and `media-admissibility evidence` are repository terms, not Micron historical vocabulary.

### Boundary

This packet does **not** establish that:

- successful raw-NAND erase automatically inserts a block into an FTL free pool;
- the documented raw-NAND family is the medium inside any named Crucial/Micron SSD;
- erase success equals sanitization or secure deletion;
- factory bad blocks and developed bad blocks have the same cause;
- a current Micron FAQ can be backdated unchanged to 2011;
- raw-NAND status semantics are a host-visible managed-SSD contract.

---

## Unified evidence model

The ten chains now support a more complete transition model without pretending every historical implementation contained every layer:

```text
logical address / object
    ↓
current mapping / currentness authority
    ↓
source physical embodiment
    ↓
replacement / relocation primitive
    ↓
integrity qualification of the replacement
    ↓
destination physical embodiment
    ↓
durable publication of current mapping
    ↓
old embodiment logically retired
    ↓
old block becomes reclaim-eligible
    ↓
erase attempt
    ├─ interrupted -> completion not established -> recovery/recheck path
    └─ reaches status verdict
          ├─ PASS -> medium-level reuse candidate
          └─ FAIL -> bad-block retirement / replacement-capacity path
    ↓
implementation-specific allocator admission
```

Two different negative erase outcomes must remain separate:

```text
power failed before a trustworthy completion verdict existed
    !=
operation completed far enough to return FAIL
```

They may both prevent ordinary reuse, but they arise from different evidence and can demand different recovery state.

---

## Retained-state classes now visible in Case 04

Case 04 is no longer only a mapping story. The evidence now exposes at least these distinct retained/control-state classes:

1. **payload state** — the user data representation;
2. **identity/currentness state** — which physical embodiment counts for a logical object;
3. **integrity state** — whether a moved/read representation is accepted under ECC/correctness rules;
4. **recovery-base state** — checkpoints/log evidence sufficient to reconstruct current mapping after restart;
5. **reclaim state** — whether an old embodiment is logically eligible for destructive maintenance;
6. **erase-operation state** — whether destructive maintenance is pending/in progress/completed;
7. **media-admissibility state** — whether the physical block is still considered usable or has been retired;
8. **capacity-management state** — free/reserve space needed to continue relocation and absorb failures.

These classes can interact, but they are not synonyms.

---

## Historical record vs engineering reconstruction vs functional analogy vs interpretation

### Historical / source record

Directly sourced records include:

- late-1980s NAND geometry;
- Ban/M-Systems virtual/physical mapping and transfer procedures;
- the issued Ban patent's internally non-uniform write-order descriptions;
- 1995–1996 FTL terminology milestones;
- M-Systems interrupted-erase recovery state;
- TrueFFS mapping reconstruction after power failure;
- Samsung Copy-Back integrity constraints;
- T13 host deallocation/read-semantics contracts;
- DCR checkpoint/recovery reconstruction;
- Micron `RDY`/`FAIL`, ERASE BLOCK qualification, error management, and bad-block handling.

### Engineering reconstruction

Repository-level relations include:

```text
physical survival
    != logical currentness

replacement existence
    != authoritative publication

functional step order
    != durable/crash-atomic order

relocation completion
    != integrity qualification

logical invalidation
    != physical erase

reclaim eligibility
    != erase success

erase ready
    != erase pass

erase pass
    != allocator free-pool insertion
```

These relations are analytical reconstructions grounded in source mechanisms, not quotations attributed to all vendors or eras.

### Functional analogy

Comparisons to copy-on-write, WAL/journaling, distributed repair, redundancy-mode conversion, SSD garbage collection, or storage-retirement authority are structural only unless an explicit historical lineage is separately sourced.

### Philosophical interpretation

Any language about identity, forgetting, publication, authority, or continuity remains downstream of the engineering record. NAND vendors, standards bodies, and FTL authors are not retroactively credited with those philosophical claims.

---

## Cross-case comparisons — functional, not genealogical

### Case 03 — DRAM refresh

DRAM commonly regenerates state while retaining the same addressable identity; Case 04 allows identity to persist through deliberate physical relocation.

```text
regeneration in place
    != identity continuity through remapping
```

### Case 24 — Azure LRC source-replica retirement

Case 24 distinguishes representation publication/retirement from deletion/reclamation. Case 04 exposes an analogous local-media sequence:

```text
old embodiment no longer needed
    != erase completed successfully
    != physical block admitted for future use
```

No Azure genealogy from NAND is asserted.

### Case 150 — managed-SSD garbage collection

Case 150 separates background erase opportunity/execution/completion at a managed-device layer. Case 04 chain 10 contributes a lower raw-NAND distinction:

```text
not busy
    != passed
```

This does not prove that a named SSD firmware exposes or preserves the same state machine.

### Case 134 — interrupted Copyback quarantine

The shared functional shape is:

```text
physical operation attempted
    != resulting state qualified for admission
```

The command family, fault model, and historical evidence remain different.

---

## Open evidence debt

Case 04 remains `grounded`. The highest-value remaining work is now narrower than `find more Flash history`:

1. **Named FTL free-pool transition** — source-level firmware/patent/implementation evidence that a block joins a reusable/free pool only after successful erase qualification.
2. **Erase-failure fault trace** — a named raw-NAND/controller experiment that captures `BUSY -> READY -> FAIL -> bad-block retirement/remap` end to end.
3. **Interrupted/no-verdict vs completed/FAIL** — a named controller showing how restart logic distinguishes `no trustworthy verdict because power died` from `operation returned failure`.
4. **Bad-block retirement durability** — determine exactly when a newly developed bad-block record itself becomes crash-durable and how torn retirement metadata is recovered.
5. **Relocation publication ordering** — named implementation/fault-injection evidence ordering destination validation, durable mapping publication, source retirement, and later erase.
6. **Copy-Back interruption** — source/fault evidence for reset or power loss during source-read, internal-buffer, and destination-program phases.
7. **Original PORCE full text** — upgrade remaining later-reported PORCE details to directly inspected primary evidence.
8. **Named shipping SSD/controller mapping format** — persistent map/checkpoint/rebuild behavior in an identified product.
9. **On-die ECC relocation** — establish how later NAND internal ECC changes controller-visible relocation qualification.
10. **Wear-leveling boundary** — add bounded early evidence rather than equating reclamation, reserve replacement, and wear leveling.
11. **Host deallocation / sanitization boundary** — continue to keep TRIM, controller invalidation, physical erase, secure erase, and crypto-erase distinct.
12. **Reserve exhaustion** — connect accumulated media retirement to a documented capacity/end-of-life threshold without overgeneralizing one vendor.

---

## Navigation / coverage note

This index previously lagged behind the repository and omitted three already-landed Case-04 deepening packets (`interrupted erase`, `TrueFFS power-failure reconstruction`, and `T13 TRIM`) even though those files were already part of the evidence tree. This revision routes those packets together with the new Micron raw-NAND erase-status packet so the case's navigation reflects the actual evidence set.

No maturity promotion follows merely from repairing navigation.

---

## Related repository routing

### `tmzncty/computing-archaeology`

Broader NAND/SSD technical genealogy belongs there: device generations, vendor chronology, command-family history, controller architecture, ONFI/status evolution, product lineage, and cross-vendor bad-block-management history.

A fresh search in this pass for `NAND bad block erase failure` and `MT29F` found no dedicated packet that could be directly reused. Accordingly, this repository keeps the new work narrowly on the retention/control seam:

```text
operation readiness
    != operation success
    != future media admissibility
```

This is a result of the current search, not a claim that `computing-archaeology` contains no NAND material anywhere.

### `tmzncty/problem-history`

Continue to use that repository's anti-anachronism discipline when asking when terms such as `Flash Translation Layer`, `garbage collection`, `copy-on-write`, `publication`, `currentness`, or `retirement` entered particular actor vocabularies. Case 04 may use them analytically only when they are labeled as reconstruction rather than historical quotation.
