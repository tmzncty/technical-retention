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
| Mercury delay-line memory | scouted | recirculation | persistence as continuous motion; time as address geometry | reuse `computing-archaeology` evidence + primary technical papers/manuals |
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
| Delay line | propagating pulse pattern | continuous circulation / regeneration | temporally gated | temporal slot | not meaningfully static | no |
| Magnetic core | magnetization | little while idle; restore after destructive read | destructive in classic core | matrix selection | high at core location | no |
| DRAM | capacitor charge | periodic refresh | sense + restore | row/column | high at logical cell while powered | no |
| SSD | Flash cell states behind FTL | ECC, remapping, GC, wear leveling | controller-mediated | logical block/page | deliberately unstable physically | usually no |
| Replicated object storage | multiple copies / coded fragments + metadata | repair, replication, consistency machinery | protocol-mediated | logical key | no privileged copy required | implementation-dependent |

Do not treat blank or simplified cells as conclusions. The matrix is a question generator, not a benchmark table.

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
