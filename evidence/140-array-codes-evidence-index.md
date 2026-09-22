# Case 140 Evidence Index — double-disk-failure array codes

**Case:** [`../cases/140-ibm-double-disk-failure-array-codes.md`](../cases/140-ibm-double-disk-failure-array-codes.md)  
**Current local status:** `grounded`  
**Scope:** early IBM double-disk-failure coding, error/erasure recovery budget, and the operational boundary between reconstructability, rebuild, distributed sparing, and later failure margin.

This index is the local navigation surface for Case 140. It does not reconstruct the repository-wide `CASE_INDEX.md`, which is currently empty.

---

## 1. Canonical case

- [`../cases/140-ibm-double-disk-failure-array-codes.md`](../cases/140-ibm-double-disk-failure-array-codes.md)

The canonical case establishes the bounded thesis:

```text
future failure margin can be retained as a coding relation
rather than as an extra complete copy
```

but keeps that statement separate from rebuild policy, production deployment, RAID-6 naming, and arbitrary silent-corruption correction.

---

## 2. Evidence chain A — 1991–1994 IBM double-disk-failure grounding

- [`140-ibm-1991-1994-double-disk-array-codes-grounding.md`](140-ibm-1991-1994-double-disk-array-codes-grounding.md)

### Historical record established

- 1991 patent-family priority floor for IBM array coding/rebuild work;
- 1992 public patent/conference disclosure floor;
- explicit protection against up to two unavailable disks/DASDs;
- two redundant disks in the cited ICC/EVENODD line;
- row/diagonal or related array-code relations rather than two complete replicas;
- 1994 EVENODD as a named XOR-based double-disk-failure RAID scheme;
- later RAID-6 terminology kept as a later functional comparison, not back-projected source terminology.

### Boundary retained

```text
two unavailable members recoverable
    !=
two replicas
    !=
all silent corruption correctable
    !=
production controller deployment
```

### Main remaining debt from this chain

- complete genealogy among Reed–Solomon, IBM diagonal-array codes, EVENODD, RDP, and later RAID-6 families;
- named production implementation;
- exact RAID-6 term/standards chronology.

---

## 3. Evidence chain B — error versus erasure budget

- [`140-ibm-1991-1995-erasure-error-budget-deepening.md`](140-ibm-1991-1995-erasure-error-budget-deepening.md)

### Historical record established

IBM patent material explicitly distinguishes:

```text
erasure / unavailable DASD
    -> failed location is already known

DASD in error
    -> errant source must be identified and corrected
```

and assigns those cases different usable parity budgets.

For the cited construction:

```text
P parity DASDs
    -> up to P known unavailable DASDs

one DASD in error
    -> consumes redundancy equivalent to two parity DASDs
```

The 1995 EVENODD journal abstract independently advertises a decoder for one column/track in error, but the evidence packet intentionally does not infer full mixed-fault semantics from the abstract alone.

### Boundary retained

```text
same physical parity bytes
    !=
same usable fault budget under different fault-location knowledge
```

and:

```text
P = 2
    supports the cited two-erasure relation
    !=
proof of one unknown error + one additional erasure
```

### Main remaining debt from this chain

- full 1995 journal paper inspection;
- exact mixed error/erasure bounds for EVENODD itself;
- sector-level detection/location semantics and interaction with device ECC/CRC.

---

## 4. Evidence chain C — distributed sparing / successive-failure boundary

- [`140-ibm-1992-1994-distributed-sparing-successive-failure-boundary-deepening.md`](140-ibm-1992-1994-distributed-sparing-successive-failure-boundary-deepening.md)

### Historical record established

The inspected IBM Research records show that:

- reconstruction was treated as work with duration, not an instantaneous consequence of mathematical reconstructability;
- distributed sparing spreads spare capacity through the array;
- after rebuild, a distributed-sparing array may be **logically different from the original array**;
- Ng and Mattson aimed to maintain uniform parity-group distribution across **successive failures**;
- contemporaneous IBM RAID5 work explicitly distinguished normal mode, degraded mode before rebuild, and rebuild mode while reconstruction had started but not finished.

### Boundary retained

The strongest source-supported transition is:

```text
valid layout L0
    -> failure F1
    -> rebuild
    -> valid reconfigured layout L1
    -> later failure F2
```

with:

```text
L1 != L0
```

in the source's own post-rebuild `logically different` sense.

The inspected public records do **not** yet prove:

```text
F1
    -> partial rebuild
    -> F2
    -> guaranteed recovery under every overlap point
```

### Main remaining debt from this chain

- full-paper inspection of the successive-failure algorithm;
- exact partial-rebuild mapping/currentness semantics;
- restart-surviving rebuild progress;
- foreground writes during reconstruction;
- named controller behavior under a second failure during rebuild.

---

## 5. Cross-chain state model

The three evidence chains should be read together, but not collapsed.

```text
                    fault-location knowledge
                             │
                             ▼
current coded fragments -> decoding relation -> reconstructability
          │                                      │
          │                                      ▼
          │                              residual coding margin
          │                                      │
          ▼                                      ▼
  currentness / validity                  failed-member state
                                                 │
                                                 ▼
                                          spare destination
                                                 │
                                                 ▼
                                          rebuild progress
                                                 │
                                                 ▼
                                  post-rebuild placement / mapping
                                                 │
                                                 ▼
                                      restored future margin
```

The key separations are:

```text
coding margin
    != spare capacity
    != rebuild admission
    != rebuild progress
    != post-rebuild placement
    != proof of currentness
```

and:

```text
recoverable now
    != fully rebuilt
    != full designed failure margin restored
```

---

## 6. Historical / engineering / analogy / philosophy separation

### Historical record

Safe historical claims include:

- the dated IBM paper/patent records and their explicit fault models;
- the source-era distinction between unavailable DASDs and DASDs in error;
- distributed sparing and the source's statement that the rebuilt array can be logically different;
- source-era normal/degraded/rebuild terminology where directly stated.

### Engineering reconstruction

Repository reconstructions include:

- fault-location knowledge is part of the effective recovery state;
- spares do not themselves add parity equations;
- partially rebuilt state can differ from both the old intact layout and the completed new layout;
- a current reconstructed representation requires more than mere physical presence of parity/rebuilt bytes.

### Functional analogy

Allowed comparisons include:

- Case 17 single-parity reconstruction;
- Case 136 rebuild scheduling/policy;
- Synthesis 09 representation handoff;
- later erasure-coded systems where missing fragments are reconstructed into new placements.

These comparisons do not imply common implementation genealogy.

### Philosophical interpretation

A bounded interpretive statement is:

> continuity can survive reconfiguration even when physical or placement identity does not.

This is repository interpretation, not source-era vocabulary.

---

## 7. Cross-case links

### Case 17 — single-parity RAID reconstruction

Case 17 supplies the one-erasure baseline. Case 140 changes the coding budget and residual margin; it does not erase rebuild-state concerns.

### Case 136 — rebuild-rate / scheduling state

Case 136 asks how repair resources are allocated and whether policy survives restart/configuration boundaries. Case 140 asks whether the coded relation can still solve the missing members and, in this new deepening, where reconstructability ends and rebuild-state/currentness questions begin.

### Synthesis 09 — coded representation handoff

The relation:

```text
old valid representation
    -> conversion / reconstruction
    -> new valid representation
```

is a useful functional comparison. Do not import modern transaction/epoch vocabulary into the 1990s papers without source evidence.

### `tmzncty/computing-archaeology`

A fresh search in this run found no dedicated `Uniform Parity Group Distribution` or `distributed sparing` packet to reuse. Broader IBM disk-array history, product genealogy, declustering families, and terminology history should go there if developed.

---

## 8. Source ladder

| Evidence | Source class | Strongest supported use | Important stop condition |
|---|---|---|---|
| 1991/1992 IBM patent-family and ICC material | primary patent + IBM institutional publication record | two-unavailable-member coding/rebuild floor | priority date is not public-disclosure date |
| ISCA 1994 EVENODD | IBM institutional publication record | named XOR-based two-disk-failure RAID code | implementability is not shipment/deployment |
| US5351246A | primary patent text | explicit error/erasure budget distinction | adjacent IBM code work is not automatically EVENODD |
| IEEE TC 1995 EVENODD abstract | IBM/Caltech institutional record | one-column-in-error decoder advertised | abstract does not establish every mixed-fault bound |
| Ng & Mattson IEEE TC 1994 distributed sparing | IBM institutional record | post-rebuild logical reconfiguration; successive-failure maintenance target | abstract does not prove second failure during incomplete rebuild |
| Ng & Mattson HPDC 1992 | IBM institutional record | reconstruction is distributable work with duration | performance/rebuild organization is not double-failure proof |
| Ng DPD 1994 sparing | IBM institutional record | spares accelerate exit from degraded state | spare count is not coding margin |
| Menon DPD 1994 RAID5 performance | IBM institutional record | source-era degraded vs rebuild-in-progress terminology | RAID5 model is not evidence for Case 140 dual-failure behavior |

---

## 9. Explicit anti-overclaim checklist

Before promoting a new Case 140 claim, check all of the following:

- Is a patent priority date being mistaken for public disclosure?
- Is `two redundant disks` being mistaken for two replicas?
- Is a known-erasure result being expanded to unknown silent corruption?
- Is spare capacity being mistaken for an independent parity equation?
- Is `successive failures` being silently rewritten as overlapping failures during partial rebuild?
- Is mathematical reconstructability being mistaken for completed physical rebuild?
- Is physical presence of parity/rebuilt bytes being mistaken for currentness?
- Is post-rebuild validity being assumed to require restoration of the original placement?
- Is a paper's algorithm being treated as named production deployment?
- Is later RAID-6 terminology being projected backward into sources that did not use it?
- Is a functional analogy being presented as historical genealogy?
- Is an abstract-level statement being used to support details only a full paper could establish?

---

## 10. Priority research queue

The highest-value next slices are now narrower than the original canonical debt list:

1. **Second failure during incomplete rebuild** — inspect a source that explicitly specifies or tests this overlap state.
2. **Rebuild currentness** — identify how partially rebuilt stripes/regions are marked, validated, or made authoritative.
3. **Restart persistence** — establish whether rebuild progress survives controller/process/power restart and at what granularity.
4. **Write/rebuild concurrency** — establish parity/currentness ordering while foreground writes overlap reconstruction.
5. **Production witness** — find a named controller/product/manual implementing a two-failure code with documented rebuild fault behavior.
6. **Mixed faults** — inspect the full 1995 EVENODD journal paper and later sector-error/URE work without conflating located erasures with silent corruption.
7. **Terminology/genealogy** — move broad RAID-6 naming and code-family history into `computing-archaeology` if it grows beyond retention-specific evidence.

---

## 11. Status rule

Case 140 remains **`grounded`**.

The new distributed-sparing evidence deepens the operational model and closes an ambiguity around the word `successive`, but it does not justify maturity promotion because the strongest practical seam remains open:

```text
second failure
    during
incomplete rebuild
```

with currentness, restart, and foreground-write semantics still ungrounded at implementation level.

A future maturity review should require at least one direct source covering that overlap state or an equivalent production/fault-injection witness rather than promoting the case from additional coding-theory material alone.
