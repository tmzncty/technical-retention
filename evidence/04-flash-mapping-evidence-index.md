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
    != erase request acceptance
    != erase completion
    != erase success
    != post-erase format preparation
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

```text
erase was initiated
    != erase completion was established

controller restarted
    != interrupted destructive maintenance can be forgotten
```

This chain concerns **absence of a trustworthy completion verdict after interruption**. It remains distinct from chain 10, where the operation reaches a status-verdict point, and chain 11, where a named FTL consumes erase-completion evidence and still requires a later preparation/admission step.

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

This chain keeps host-visible deallocation separate from physical erasure. TRIM / DATA SET MANAGEMENT can communicate that logical ranges are no longer needed, while subsequent read behavior and actual physical reclamation remain separately specified/implemented.

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

```text
ERASE accepted
    -> BUSY
    -> READY
    -> FAIL status checked
        -> success
        or
        -> erase failure / retirement path
```

Micron's datasheet distinguishes `RDY` from `FAIL`: readiness answers whether the target/operation remains busy, while the status verdict answers whether PROGRAM/ERASE/READ succeeded. Bad-block guidance separately treats runtime PROGRAM/ERASE errors as evidence for developed bad blocks.

The resulting engineering reconstruction remains:

```text
logical reclaim eligibility
    != erase command admission
    != temporal completion / ready
    != erase success
```

This packet alone does not establish higher-level allocator admission.

---

## Evidence chain 11 — Linux v2.6.12 FTL erase completion -> preparation -> transfer-unit admission

**Packet:** [`04-linux-ftl-2005-transfer-unit-reuse-admission-deepening.md`](04-linux-ftl-2005-transfer-unit-reuse-admission-deepening.md)

Released Linux v2.6.12 source provides the named implementation bridge that chain 10 intentionally left open.

The driver explicitly distinguishes:

```text
XFER_UNKNOWN
XFER_ERASING
XFER_ERASED
XFER_PREPARED
XFER_FAILED
```

`erase_xfer()` submits an asynchronous erase and leaves completion to `ftl_erase_callback()`. Only `MTD_ERASE_DONE` changes the unit to `XFER_ERASED`; another callback outcome sends it to `XFER_FAILED`.

`XFER_ERASED` is still not an allocator/reclaimer admission state. `prepare_xfer()` writes the FTL header and BAM stub and sets `XFER_PREPARED` only after those writes succeed. `reclaim_block()` chooses candidates only in the `XFER_PREPARED` branch.

The bounded historical implementation therefore supports:

```text
erase request accepted
    != erase completed successfully
    != FTL metadata preparation succeeded
    != transfer unit admitted as relocation destination
```

It also exposes a persistence-horizon boundary: startup `build_maps()` can reconstruct a transfer unit as `XFER_PREPARED` from a valid FTL header with `LogicalEUN == 0xffff`, so the volatile enum instance is not the only evidence of preparedness.

### Boundary

This is a PCMCIA-style Linux software FTL over MTD Flash, not evidence for a modern NAND SSD firmware state machine. Its `prepared transfer unit` is also not identical to an ordinary free 512-byte data block; the same source separately tracks `EUNInfo[].Free`, `FreeTotal`, and BAM `BLOCK_FREE` entries.

The packet therefore closes the previous highest-priority **named FTL reusable-capacity admission** debt only in this bounded implementation form.

---

## Unified evidence model

The eleven chains now support a more complete transition model without pretending every historical implementation contained every layer:

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
durable publication / reconstructable currentness evidence
    ↓
old embodiment logically retired
    ↓
old capacity becomes reclaim-eligible
    ↓
erase lifecycle
    ├─ interrupted -> completion not established -> recovery/recheck path
    └─ reaches result
          ├─ failure -> retirement/failure path
          └─ success -> post-erase control preparation may still be required
                           ↓
                    implementation-specific reuse admission
```

For Linux v2.6.12 FTL specifically:

```text
XFER_UNKNOWN
    -> erase request
    -> XFER_ERASING
    -> MTD_ERASE_DONE
    -> XFER_ERASED
    -> FTL header/BAM preparation
    -> XFER_PREPARED
    -> eligible relocation destination
```

Two different negative erase outcomes remain separate:

```text
power failed before a trustworthy completion verdict existed
    !=
operation reached a failure verdict
```

And the new source-level evidence adds a third boundary:

```text
erase completed successfully
    != higher-level reuse metadata is prepared
```

---

## Retained/control-state classes now visible in Case 04

Case 04 now exposes at least these distinct classes:

1. **payload state** — user data representation;
2. **identity/currentness state** — which embodiment counts for a logical object;
3. **integrity state** — whether a moved/read representation is accepted;
4. **recovery-base state** — checkpoints/log/on-media evidence sufficient to reconstruct current mapping;
5. **reclaim state** — whether an old embodiment is eligible for destructive maintenance;
6. **erase-operation state** — pending/in-progress/done/failed destructive maintenance;
7. **media-admissibility state** — whether physical media remains acceptable or is retired;
8. **post-erase format/preparation state** — whether control metadata required for safe higher-level use has been established;
9. **capacity-management state** — free/reserve/prepared capacity available to continue relocation and absorb failures.

These classes interact but are not synonyms.

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
- Micron `RDY` / `FAIL`, ERASE qualification, error management, and bad-block handling;
- Linux v2.6.12 FTL transfer-unit states, MTD erase callback qualification, post-erase preparation, and prepared-only relocation selection.

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
    != erase request acceptance
    != erase success
    != post-erase preparation
    != reuse admission
```

`reuse authority`, `reuse admission`, `qualification`, and `control-state persistence horizon` are analytical terms, not words attributed to all vendors/implementations.

### Functional analogy

Comparisons to copy-on-write, WAL/journaling, distributed repair, SSD garbage collection, bad-block retirement, or storage-retirement authority are structural only unless an explicit historical lineage is separately sourced.

### Philosophical interpretation

Any language about identity, forgetting, publication, authority, continuity, or `trusted empty space` remains downstream of the engineering record. Flash vendors, Linux MTD developers, standards bodies, and FTL authors are not retroactively credited with those philosophical claims.

---

## Cross-case comparisons — functional, not genealogical

### Case 03 — DRAM refresh

```text
regeneration in place
    != identity continuity through remapping
```

DRAM commonly reconstructs state while keeping a stable addressable location relation; Case 04 allows identity to persist through deliberate physical relocation.

### Case 24 — Azure LRC source-replica retirement

```text
old embodiment no longer needed
    != cleanup completed
    != resource admitted for future reuse
```

This is a structural comparison only; no Azure-from-Flash genealogy is asserted.

### Case 78 — NAND bad-block knowledge

```text
physical/media exclusion evidence
    != FTL transfer-unit preparation
```

Both can constrain reuse, but they are different retained relations with different persistence/recovery paths.

### Case 150 — managed-SSD garbage collection

Case 150 separates maintenance opportunity, execution, and completion at a managed-device layer. Chains 10–11 now add lower/raw and software-FTL distinctions:

```text
not busy
    != erase passed
    != higher-level preparation complete
    != reusable-capacity admission
```

No claim is made that a named SSD firmware exposes the Linux FTL state machine.

### Case 134 — interrupted Copyback quarantine

```text
physical operation attempted
    != resulting state qualified for admission
```

The command family, fault model, and historical evidence remain different.

---

## Open evidence debt

Case 04 remains `grounded`. The previous highest-priority debt — a named FTL in which successful erase qualification precedes a separate reusable-capacity admission state — is now closed by chain 11 in the bounded Linux v2.6.12 implementation.

Highest-value remaining work is now:

1. **Linux FTL cut-point fault trace** — interrupt around asynchronous erase completion, FTL-header write, BAM-stub write, and the next reclaim cycle; observe restart classification and whether `build_maps()` ever admits an incompletely prepared transfer unit.
2. **Erase-failure fault trace** — capture `BUSY/ERASING -> failure -> retirement/non-admission` end to end on a named raw-Flash/controller path.
3. **Interrupted/no-verdict vs completed/FAIL** — show how one named controller distinguishes power-loss ambiguity from an explicit negative completion verdict.
4. **Bad-block retirement durability** — determine when a newly developed bad-block record becomes crash-durable and how torn retirement metadata is recovered.
5. **Relocation publication ordering** — named implementation/fault injection ordering destination validation, durable mapping publication, source retirement, and later erase.
6. **Copy-Back interruption** — reset/power-loss evidence for source-read, internal-buffer, and destination-program phases.
7. **Original PORCE full text** — upgrade later-reported PORCE details to directly inspected primary evidence.
8. **Named shipping SSD/controller mapping format** — persistent map/checkpoint/rebuild behavior in an identified product.
9. **Modern NAND/SSD free/reserve-pool transition** — find an open firmware/controller implementation connecting NAND erase qualification to block-pool admission without assuming Linux PCMCIA FTL semantics.
10. **On-die ECC relocation** — establish how later NAND internal ECC changes controller-visible relocation qualification.
11. **Wear-leveling boundary** — add bounded early evidence rather than equating reclamation, reserve replacement, and wear leveling.
12. **Host deallocation / sanitization boundary** — continue to keep TRIM, controller invalidation, physical erase, secure erase, and crypto-erase distinct.
13. **Reserve exhaustion** — connect accumulated media retirement to a documented capacity/end-of-life threshold without overgeneralizing one vendor.

---

## Navigation / coverage note

This index now routes eleven Case-04 evidence chains. The latest addition is the released Linux v2.6.12 FTL source-level path:

```text
MTD erase completion
    -> XFER_ERASED
    -> FTL metadata preparation
    -> XFER_PREPARED
    -> relocation admission
```

It replaces the earlier generic `erase pass != allocator free-pool insertion` debt with a narrower set of fault-injection and modern-controller questions.

No maturity promotion follows from this navigation update.

---

## Related repository routing

### `tmzncty/computing-archaeology`

Broader NAND/SSD/Flash-card technical genealogy belongs there: device generations, PCMCIA FTL standardization, Linux MTD/Card Services history, M-Systems licensing/patent lineage, controller architecture, ONFI/status evolution, product lineage, and later SSD free-pool/over-provisioning implementations.

A fresh search in this pass for `ftl.c`, `Flash Translation Layer David Hinds`, and the Linux FTL driver found no dedicated packet that could be reused. Accordingly, this repository keeps the new work narrowly on the retention/control seam:

```text
erase completion evidence
    != post-erase preparation
    != reuse admission
```

This is a result of the current search, not a claim that `computing-archaeology` contains no Flash material anywhere.

### `tmzncty/problem-history`

Continue to use that repository's anti-anachronism discipline when asking when terms such as `Flash Translation Layer`, `garbage collection`, `free pool`, `copy-on-write`, `publication`, `currentness`, `retirement`, or `reuse authority` entered particular actor vocabularies. Case 04 may use modern analytical terms only when they are labeled as reconstruction rather than historical quotation.