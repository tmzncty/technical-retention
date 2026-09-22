# Case 04 — Flash mapping / relocation evidence index

## Status

**Case maturity: `grounded`**.

This index is navigation and evidence-layer control for [`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md). It does not promote the case beyond the maturity stated by the parent case.

Case 04 asks how logical identity can remain stable while the physical embodiment of data changes, and what additional retained state is required to keep the new embodiment current, recoverable, and acceptable.

The central anti-collapse rule is now:

```text
physical nonvolatility
    !=
logical currentness
    !=
relocation completion
    !=
integrity qualification
    !=
crash-recoverable mapping authority
```

---

## Evidence chain 1 — NAND device geometry before FTL semantics

**Packet:** [`04-1987-1989-nand-device-geometry-before-ftl-deepening.md`](04-1987-1989-nand-device-geometry-before-ftl-deepening.md)

### What it establishes

Late-1980s Toshiba / NAND-structure device literature provides a historical device-level floor for:

- NAND string organization;
- page / successive programming behavior;
- block erasing;
- random reading;
- dense nonvolatile array geometry.

### What it does not establish

```text
NAND string / page / block operation geometry
    !=
FTL mapping
    !=
logical-to-physical remapping
    !=
crash-recoverable mapping authority
```

The packet prevents later FTL vocabulary from being projected backward onto device papers that did not describe it.

---

## Evidence chain 2 — 1993–1995 virtual mapping and logical identity

**Parent case:** [`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md)

### What it establishes

The 1993-filed Amir Ban / M-Systems `Flash file system` patent directly grounds:

- virtual versus physical address space;
- a retained virtual map;
- out-of-place replacement of an already-written logical location;
- logical unit identity remaining stable while physical location changes;
- logical deletion / invalidation preceding later physical erase;
- relocation of still-current blocks before reclaim erase;
- mapping/allocation metadata as retained or reconstructible state.

The core result is:

```text
same logical object
    !=
same physical location
```

and:

```text
payload bits survive
    !=
which payload instance currently counts is self-evident
```

### Boundary

This patent does not define every later FTL, every modern garbage collector, every NAND command primitive, or a universal power-fail protocol.

---

## Evidence chain 3 — FTL terminology / standardization chronology

**Packet:** [`04-ftl-1995-1996-terminology-standardization-addendum.md`](04-ftl-1995-1996-terminology-standardization-addendum.md)

### What it establishes

The packet separates three milestones that are easy to collapse:

```text
public term use by February 1995
    !=
reported PCMCIA approval by August 1995
    !=
later-reported specification release in May 1996
```

It provides a terminology floor without turning the earliest inspected use into a claim of first coinage or invention.

### Boundary

Historical vocabulary remains source-sensitive. `FTL`, `garbage collection`, and `copy-on-write` must not silently replace the actor vocabulary of earlier sources.

---

## Evidence chain 4 — FTL power-off recovery and reconstructed authority

**Packet:** [`04-2008-2014-ftl-power-off-crash-recovery-deepening.md`](04-2008-2014-ftl-power-off-crash-recovery-deepening.md)

### What it establishes

2008–2014 FTL recovery evidence, especially directly inspected DCR 2014, separates:

- latest volatile working-map state;
- last durable checkpoint / recovery base;
- newer on-flash evidence;
- reconstructed post-crash mapping authority.

The strong bounded relation is:

```text
latest volatile mapping state
    !=
latest durable recovery base
    !=
final reconstructed mapping after restart
```

Thus logical identity can survive loss of the exact runtime map when enough persistent evidence remains to construct a successor authoritative map.

### Boundary

The DCR implementation is a specific FTL design, not a universal commercial-SSD recovery model.

---

## Evidence chain 5 — raw-NAND Copy-Back integrity boundary

**Packet:** [`04-samsung-2004-2010-nand-copyback-integrity-boundary-deepening.md`](04-samsung-2004-2010-nand-copyback-integrity-boundary-deepening.md)

### What it establishes

Samsung manufacturer NAND documentation from the 2004–2010 line directly separates physical relocation from payload revalidation.

The earlier K9F1208U0B-family documentation warns that source-page charge-loss errors can be propagated and accumulated by repeated Copy-Back and recommends ECC. The 2010 K9GAG08U0E-family documentation exposes a source-read / controller-visible bit-error check / optional correction or reload / destination-program workflow.

The bounded result is:

```text
Copy-Back program completion
    !=
source payload revalidated

new physical embodiment exists
    !=
new physical embodiment is qualified as the intended logical payload
```

### Boundary

Copy-Back is a raw NAND primitive. The Samsung device datasheets do not establish FTL mapping-publication order, old-page retirement order, or crash atomicity around that higher-level transition.

---

## Unified evidence model

The five chains now support the following layered model without pretending every historical system implemented every layer in the same way:

```text
logical address / logical object
    ↓
current mapping / currentness authority
    ↓
source physical embodiment
    ↓
relocation / rewrite primitive
    ↓
integrity observation and correction
    ↓
destination physical embodiment
    ↓
higher-layer publication / retirement policy
    ↓
crash-recoverable evidence for the current mapping relation
```

The most important result is not that Flash is “nonvolatile.” It is that a rewritable mapped-storage service has several independent retention obligations:

1. **material persistence** — cells retain a representation;
2. **identity persistence** — mapping says which representation belongs to the logical object;
3. **integrity persistence** — the representation remains acceptable under ECC / correctness rules;
4. **authority persistence** — enough control evidence survives to decide which mapping counts after restart;
5. **maintenance capacity** — free / transfer space and reclaim work remain available so the service can continue changing state.

---

## Cross-case comparisons — functional, not genealogical

### Case 03 — DRAM refresh

DRAM primarily preserves a logical value by regenerating state in a maintenance regime tied to the same addressable storage site. Case 04 adds a different pattern: the logical identity can deliberately migrate between physical sites.

```text
regeneration in place
    !=
identity continuity through remapping
```

### Case 81 / distributed storage

Distributed repair, configuration authority, and Flash mapping share a structural question: after a transition, which embodiment is allowed to count as current?

The analogy is useful at the relation level only. It does not establish common lineage or identical commit protocols.

### Case 85 — NAND read retry

Case 85 separates media truth, reader configuration, and retry state. The Copy-Back packet adds a neighboring separation:

```text
physical operation succeeds
    !=
payload acceptability is established
```

Again, this is a functional comparison, not genealogy.

---

## Historical record vs reconstruction vs interpretation

### Historical record

Directly sourced statements include:

- NAND device operation geometry in late-1980s papers;
- Ban's virtual/physical mapping and transfer-unit procedures;
- contemporary / near-contemporary FTL terminology milestones;
- DCR's volatile-map / durable-checkpoint recovery structure;
- Samsung Copy-Back mechanics, error-propagation warning, and later check/correct procedure.

### Engineering reconstruction

Project-level engineering conclusions include:

```text
physical survival
    !=
logical currentness

relocation completion
    !=
integrity qualification

recovery starting authority
    !=
final reconstructed authority

logical invalidation
    !=
physical erase
```

These are reconstructed relations grounded in the cited mechanisms, not quotations from every source.

### Functional analogy

Comparisons to copy-on-write, journals/WALs, distributed repair, or redundancy-mode conversion are structural only unless a separate historical lineage is sourced.

### Philosophical interpretation

Claims about identity, forgetting, or continuity are downstream interpretations. They must remain visibly downstream of the engineering record and are not attributed to NAND vendors, FTL authors, or standards bodies.

---

## Open evidence debt

Case 04 remains `grounded`. The highest-value remaining work is now more specific than “find more Flash history”:

1. **Power-fail ordering around relocation** — a named controller / firmware / patent source that orders destination validation, mapping publication, old-page invalidation, and later erase.
2. **Copy-Back interruption** — named-device or fault-injection evidence for reset / power loss during source read, internal-buffer residency, or destination programming.
3. **Original PORCE full text** — upgrade remaining later-reported PORCE details to directly inspected page-anchored primary evidence.
4. **Named shipping SSD / controller mapping format** — show persistent map/checkpoint/rebuild behavior in an identified product.
5. **On-die ECC relocation** — establish how later NAND internal ECC changes controller-visible integrity qualification around relocation.
6. **Wear leveling** — add a bounded early source rather than equating reclamation with wear leveling.
7. **Host deallocation / secure erase** — keep TRIM, DEALLOCATE, controller invalidation, physical erase, and crypto-erase as a separate later slice.
8. **Torn-program / atomicity boundary** — do not let DCR or Copy-Back evidence stand in for a universal host-FLUSH / PLP / torn-NAND contract.

---

## Related repository routing

### `tmzncty/computing-archaeology`

Broader NAND / SSD technical genealogy belongs there: device generations, vendor chronology, command-family history, controller architecture, and exact Copy-Back lineage.

A fresh repository search for `copyback` / `copy-back` found no dedicated companion packet to reuse in this pass, so this index links only retention-specific work in `technical-retention`.

### `tmzncty/problem-history`

Use that repository's anti-anachronism discipline when asking when terms such as `Flash Translation Layer`, `garbage collection`, `copy-on-write`, or `currentness` entered particular actor vocabularies. Case 04 may use those concepts analytically, but must continue to preserve source-era language.
