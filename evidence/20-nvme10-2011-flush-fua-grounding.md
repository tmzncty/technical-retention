# Grounding Record — NVM Express 1.0 Flush, FUA, Ordering, and Power-Fail Atomicity

## Purpose

This record grounds [`../cases/20-nvme10-fua-flush-persistence-ordering.md`](../cases/20-nvme10-fua-flush-persistence-ordering.md).

**Promotion decision:** `grounded` for the bounded 2011 NVMe 1.0 host/controller persistence-semantics question.

The case is not a product implementation study. Its primary artifact is the official NVM Express Revision 1.0 Gold specification, so the strongest claims are about what the interface required, exposed, or explicitly refused to imply.

---

## Primary artifact

NVMHCI Workgroup / NVM Express, **_NVM Express Revision 1.0_**, official Gold PDF, ratified **1 March 2011**:

<https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0-Gold.pdf>

The PDF was directly opened and its text layer and relevant facsimile pages were inspected during this slice.

### Directly checked locators

| Printed page | Section / field | Grounded fact |
| --- | --- | --- |
| 2 | front matter | `NVM Express revision 1.0`; ratified 1 March 2011 |
| 8–9 | §§1.1–1.3 | host/NVM-subsystem interface scope; interface above wear-leveling/NVM-management details; caching algorithm not specified |
| 70 | Identify Controller | `Volatile Write Cache (VWC)` presence; `Atomic Write Unit Normal (AWUN)`; `Atomic Write Unit Power Fail (AWUPF)` |
| 79 | §5.12.1.6 | VWC feature; cache guaranteed to drain to nonvolatile media on power loss is considered nonvolatile for this feature |
| 88 | §6.3 | independent-command ordering is not generally supplied by controller; host/application enforces required ordering; normal atomic write unit may differ from power-fail unit |
| 93 | §6.7 | Flush asks that data in volatile storage be flushed to nonvolatile memory |
| 97 | Figure 128, Write CDW12 | Write FUA requires data on nonvolatile media before command completion; explicitly no implied ordering with other commands |
| ~100 | controller command-processing discussion | command processing / media commitment is not required to follow one simple receive order |

Direct screenshot inspection succeeded for the ratification page, Identify Controller VWC/AWUN/AWUPF page, VWC feature note, Flush page, and Write FUA page. The §6.3 ordering text was also directly read from the official PDF text layer; one attempted screenshot fetch for that page returned a transient cache miss, so no visual-layout claim depends on it.

---

## Claim-by-claim grounding

### 1. Revision/date

**Claim:** Revision 1.0 was ratified on 1 March 2011.

**Evidence class:** `H/P`.

**Anchor:** printed p. 2.

**Boundary:** the front matter also preserves then-current Intel/NVMHCI hosting language. This case does not infer present institutional ownership from that historical download instruction; the artifact is currently hosted by NVM Express.

### 2. VWC is an explicit interface capability

**Claim:** Identify Controller reports whether a volatile write cache is present; if present, the host may use Flush and the Volatile Write Cache feature.

**Evidence class:** `H/P`.

**Anchor:** printed p. 70, field 525.

**Boundary:** this says nothing about the physical memory technology used for a named controller's cache.

### 3. Power-loss guarantee changes the VWC classification

**Claim:** if the controller guarantees that write-cache data reach nonvolatile media on loss of power, that cache is considered nonvolatile for the VWC feature.

**Evidence class:** `H/P`.

**Anchor:** §5.12.1.6, printed p. 79.

**Mechanism-level consequence (`E`):** interface volatility classification is not reducible to a physical-material label. A recovery guarantee can change how a cache is classified at this contract boundary.

**Rejected overclaim:** physically volatile cells become intrinsically nonvolatile. The source says no such thing.

### 4. Flush is a distinct volatile → nonvolatile operation

**Claim:** the host uses Flush to indicate that data in volatile storage should be flushed to nonvolatile memory.

**Evidence class:** `H/P`.

**Anchor:** §6.7, printed p. 93.

**Boundary:** Revision 1.0's short wording is retained as-is. Later-revision semantics about exact prior-command scope or persistence domains are not imported backward.

### 5. FUA binds nonvolatile-media residence to one Write's completion

**Claim:** Write FUA requires the data to be written to nonvolatile media before command completion.

**Evidence class:** `H/P`.

**Anchor:** Figure 128, printed p. 97.

This supports the project distinction:

`generic completion ≠ explicit media-before-completion guarantee`.

The case deliberately phrases this conservatively: the generic completion definition alone is not silently upgraded into a media-persistence guarantee for every ordinary write.

### 6. FUA does not supply cross-command ordering

**Claim:** the same FUA definition states that there is no implied ordering with other commands.

**Evidence class:** `H/P`.

**Anchor:** Figure 128, printed p. 97.

This is the strongest direct source for the engineering finding:

`per-command persistence ≠ cross-command ordering`.

### 7. Ordering above the controller remains a host/application responsibility

**Claim:** when independent commands require ordering, host software or the associated application must enforce it above the controller.

**Evidence class:** `H/P`.

**Anchor:** §6.3, printed p. 88.

**Boundary:** fused operations are an explicit exception class and are outside this case's main persistence comparison.

### 8. Normal and power-fail atomicity are distinct reported capabilities

**Claim:** AWUN and AWUPF separately report atomic write units for normal operation and a power-fail condition; §6.3 says they may differ.

**Evidence class:** `H/P`.

**Anchors:** Identify Controller p. 70; §6.3 p. 88.

This directly grounds:

`normal-operation atomicity ≠ power-fail atomicity`.

The case does not infer which physical failure mechanism determines a product's AWUPF.

### 9. Read-visible currentness and persistence order remain separable

**Claim:** after a write completes, later-completing reads of that location return that write's data rather than an older value, while the controller does not generally supply application ordering among independent commands.

**Evidence class:** `H/P` for the two source clauses; `E` for their comparison.

**Anchor:** §6.3, printed p. 88.

This supports `post-write currentness ≠ persistence order/history` without claiming that the standard retains an operation log.

---

## Prior-art boundary

This case makes **no claim that NVMe invented Flush, FUA, volatile write caching, or durable-write interfaces**.

The repository already grounds an earlier ATA line in Case 15: T13/1699-D Revision 4a (21 May 2007) defines `FLUSH CACHE` against a `volatile write cache` / `non-volatile media` distinction. That is sufficient to block a false `NVMe invented flush` narrative inside this repository.

A complete SCSI/ATA/FUA genealogy is outside this bounded slice. It should be researched separately before any priority claim is attempted.

---

## Related-repository duplication check

Searched [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for:

- `NVM Express` / `NVMe`;
- `volatile write cache`;
- `FUA`;
- `Flush`.

No dedicated existing NVMe persistence-semantics treatment was found in the checked repository state. Therefore this case does not duplicate an existing technical-history chapter. If later work grows into a general NVMe interface chronology or controller-engineering history, that broader material should move to `computing-archaeology` and be linked from here.

---

## Evidence-layer controls

### Historical record (`H/P`)

Period vocabulary, fields, commands, dates, and normative statements are taken from the official Revision 1.0 specification.

### Engineering reconstruction (`E`)

The project terms `durability boundary`, `per-command persistence`, `persistence ordering`, and `interface recovery guarantee` summarize relations among those sourced fields. They are not represented as 2011 terminology.

### Functional analogy (`A`)

Comparisons to Case 15 (Intel SSD 320), Case 16 (BSD FFS soft updates), and Case 04 (mapped Flash) are explicitly cross-layer analogies. NVMe Revision 1.0 is not evidence that those earlier systems implemented NVMe semantics.

### Philosophical interpretation (`I`)

The limited interpretive result is that `nonvolatile storage` at a host interface can depend on operational guarantees in addition to medium labels. This does not replace the physical mechanism or turn persistence into a merely linguistic property.

---

## Rejected claims / unsupported extrapolations

- **X:** Revision 1.0 defines the later generic concept `persistence domain` for this case.
- **X:** every NVMe 1.0 controller has a physically volatile DRAM write cache.
- **X:** every NVMe 1.0 controller uses capacitor-backed power-loss protection.
- **X:** generic command completion means every ordinary Write is already on nonvolatile media.
- **X:** Write FUA orders all earlier/later commands; the specification explicitly denies implied ordering.
- **X:** AWUN and AWUPF are necessarily equal.
- **X:** an interface guarantee proves empirical fault compliance for every implementation.
- **X:** NVMe invented Flush/FUA.

---

## Remaining open work

Not required for this bounded case's `grounded` status:

- later NVMe persistence-domain terminology and exact revision history;
- NVMe 1.1+ changes to Flush/FUA/VWC wording;
- named-controller implementation and fault-injection evidence;
- controller metadata/journal recovery across power loss;
- filesystem/database composition with barriers, FUA, Flush, and `fsync`;
- NVMe over Fabrics persistence and transport-failure semantics;
- full historical FUA genealogy across SCSI/ATA before 2011.

These are separate regimes rather than hidden blockers for the 2011 interface question.

---

## Promotion decision

**`grounded`**.

Reason: the central case rests on an official period primary specification directly inspected at exact locators; historical vocabulary and normative boundaries are recoverable; the mechanism-level reconstruction is explicitly separated from historical language; prior-art overclaim is blocked by earlier ATA evidence already in the repository; relevant related-repository duplication was checked; and the case records both negative clauses and unsupported extrapolations rather than treating `NVMe` or `nonvolatile` as self-explanatory categories.