# Case Index

This index tracks case maturity and evidence type. A checked box in the roadmap is not enough: each case should show **what kind of claim has actually been established**.

## Status levels

### `scouted`

A potentially useful case has been identified, but its historical vocabulary and mechanism have not yet been verified.

### `first-pass`

The case has:

- a bounded research question;
- at least one credible historical or technical source;
- a mechanism-level description;
- explicit separation of historical record from modern analogy;
- known evidence gaps.

It is usable for comparison but should not be treated as settled.

### `grounded`

The case has:

- strong primary evidence where available;
- precise source locations;
- historical vocabulary;
- mechanism and failure modes;
- counterexamples / limits;
- related-repository duplication checked.

### `mature`

The case is strong enough to support synthesis across cases. It has survived source deepening and conceptual comparison, and its central claims no longer depend on a single source or fragile analogy.

---

## Evidence labels

Use these labels in case claim ledgers where useful:

| Label | Meaning |
| --- | --- |
| `H` | historical record |
| `P` | primary / contemporary evidence |
| `S` | scholarly or institutional secondary evidence |
| `E` | engineering / operational reconstruction |
| `A` | functional analogy |
| `I` | philosophical / media-theoretical interpretation |
| `X` | rejected or explicitly unsupported claim |

A claim may have more than one label, for example `H/P` or `E/A`.

---

## Cases

| Case | Status | Retention regime | Main methodological use | Next work |
| --- | --- | --- | --- | --- |
| [Abacus as Retained Position](cases/00-abacus-retained-position.md) | **first-pass** | passive mechanical position + human interpretation | test `register-like` analogy; separate working state from archive; recover period vocabulary | facsimile folio locations; older counting-rod vocabulary; non-Chinese comparison |
| [Mercury Delay-Line Memory: Retention as Circulation](cases/01-mercury-delay-line-circulation.md) | **first-pass** | recirculation + regeneration | persistence as continuous activity; time as access geometry; identity through re-creation | exact patent/page anchors; direct 1949 IRE inspection; temperature-control primary source |
| Magnetic core memory | scouted | remanence + destructive read/rewrite | nonvolatility, destructive read, maintenance labor | primary manuals/patents and core-weaving sources |
| DRAM | scouted | decaying charge + refresh | persistence as scheduled restoration | coordinate technical history with `computing-archaeology` |
| Flash / SSD | scouted | trapped charge + controller remapping | identity without location; deletion vs erasure; endurance | FTL/controller primary technical sources |
| Replicated object storage | scouted | redundancy + protocol + repair | logical durability without privileged physical copy | choose bounded implementation / system before writing |

---

## Comparison matrix — provisional

This matrix should become more precise as cases mature.

| Case | State substrate | Active retention work | Read | Addressing | Location stability | History retained by default? |
| --- | --- | --- | --- | --- | --- | --- |
| Abacus | bead position | mostly human protection / interpretation | nondestructive visual/manual | spatial column selected by user | high during one configuration | no |
| Delay line | propagating pulse pattern | continuous circulation / regeneration / retiming | electronically sensed; state continues by recirculation | temporal slot + index | not meaningfully static | no |
| Magnetic core | magnetization | little while idle; restore after destructive read | destructive in classic core | matrix selection | high at core location | no |
| DRAM | capacitor charge | periodic refresh | sense + restore | row/column | high at logical cell while powered | no |
| SSD | Flash cell states behind FTL | ECC, remapping, GC, wear leveling | controller-mediated | logical block/page | deliberately unstable physically | usually no |
| Replicated object storage | multiple copies / coded fragments + metadata | repair, replication, consistency machinery | protocol-mediated | logical key | no privileged copy required | implementation-dependent |

---

## Cross-case findings already supported

After only two first-pass cases, three distinctions are already useful enough to carry forward:

1. **state retention ≠ history retention** — both the abacus and delay line preserve current working state without automatically preserving the sequence that produced it;
2. **retention mechanism ≠ apparent persistence** — one state sits still; the other survives by continual circulation and re-creation;
3. **identity of logical state ≠ identity of physical token** — especially in the delay line, logical sameness survives repeated regeneration of the physical signal.

These are provisional cross-case findings, not final philosophical conclusions.

---

## Current synthesis gate

Do **not** write a grand `What Is Technical Retention?` synthesis yet.

The current gate remains:

- at least four contrasting cases at `grounded` or better;
- at least one case of passive position;
- at least one case of active refresh / circulation;
- at least one case of nonvolatile physical remanence or trapped state;
- at least one case where logical identity survives physical relocation;
- philosophical comparison must be performed after, not instead of, mechanism reconstruction.
