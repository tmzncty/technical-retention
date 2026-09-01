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
| [Magnetic Core Memory: Retention at Rest, Destruction in Reading](cases/02-magnetic-core-destructive-read.md) | **grounded** | remanence + destructive read / restore in the bounded classic scheme | separate idle nonvolatility from read invariance; show access itself can create a retention obligation; bound destructive read with contemporary nondestructive alternatives | [1951–1954 grounding record](evidence/02-magnetic-core-1951-1954-grounding.md); future work should be narrow archival/semantic archaeology rather than generic core-memory expansion |
| [DRAM Refresh as Scheduled Restoration](cases/03-dram-refresh-as-scheduled-restoration.md) | **grounded** | decaying charge + periodic regeneration; destructive-read restore in bounded 1T1C embodiment | separate time-triggered maintenance from access-triggered restore; stable logical address over repeatedly restored physical charge | [1967–1982 grounding record](evidence/03-dram-1967-1982-grounding.md); future work should be narrow failure/semantic archaeology rather than generic DRAM expansion |
| [Flash Virtual Mapping: Logical Identity Without Physical Location](cases/04-flash-virtual-mapping-logical-identity.md) | **first-pass** | nonvolatile Flash + virtual/logical/physical mapping + deferred reclamation | identity persistence without location persistence; logical invalidation vs physical erase; mapping metadata as retained state | patent PDF anchors; full Masuoka 1987 paper; early Flash/NAND datasheet; first explicit FTL terminology; wear-leveling source |
| [RADOS Replicated Objects: Retention by Replica Agreement and Repair](cases/05-rados-replicated-object-repair.md) | **grounded** | n-way replication + versioned primary authority + failure-triggered repair | currentness beyond copy multiplicity; no permanently privileged physical home; repair-triggered retention; ack vs durable commit | [2006–2007 grounding record](evidence/05-rados-2006-2007-grounding.md); future work should be narrow semantic/version archaeology rather than generic Ceph expansion |

---

## Comparison matrix — provisional

This matrix should become more precise as cases mature.

| Case | State substrate | Active retention work | Read | Addressing | Location stability | History retained by default? |
| --- | --- | --- | --- | --- | --- | --- |
| Abacus | bead position | mostly human protection / interpretation | nondestructive visual/manual | spatial column selected by user | high during one configuration | no |
| Delay line | propagating pulse pattern | continuous circulation / regeneration / retiming | electronically sensed; state continues by recirculation | temporal slot + index | not meaningfully static | no |
| Magnetic core | remanent magnetization | little merely to remain at rest; active restore after classic destructive read | destructive in the bounded classic case, followed by rewrite when logical value must persist; contemporary nondestructive schemes also existed | coincident coordinate selection | high at the selected core | no |
| DRAM | capacitor / storage-node charge | periodic regeneration because of leakage; shared row-level sense/restore infrastructure; restore after destructive read in the bounded Dennard 1T1C embodiment | destructive in the bounded Dennard embodiment; commercial dynamic memories can have nondestructive reads | word/bit-line or row/column selection | logical cell stable while physical charge is repeatedly renewed | no |
| Mapped Flash | nonvolatile cell state + allocation/mapping metadata | out-of-place update, map maintenance, transfer/reclamation; later NAND adds ECC/wear/GC layers | map-mediated read of current physical embodiment | virtual/logical address translated to physical location | deliberately unstable under rewrite/reclaim | usually no; stale physical embodiments may cease to count before erase |
| RADOS | multiple object replicas + cluster map + PG/version/recovery state | replication, failure detection, peering, re-replication, migration/recovery | protocol-authorized current replica; exact read role depends on replication scheme | object → PG → CRUSH + current cluster map → ordered OSD set | no permanently privileged physical home | no by default; PG logs retain bounded recovery history and can be guarded separately from every replica |

---

## Cross-case findings already supported

After six bounded cases, several distinctions are useful enough to carry forward. **Magnetic core, DRAM, and RADOS are now `grounded`; the other three cases remain `first-pass`**, so cross-case synthesis must still remain provisional.

1. **state retention ≠ history retention** — all six cases preserve current working state without automatically preserving the complete sequence that produced it;
2. **retention mechanism ≠ apparent persistence** — an abacus configuration can sit still, a delay-line pattern survives by continual circulation, a core can remain magnetized at rest, a DRAM cell survives for a bounded interval before scheduled regeneration, mapped Flash can preserve a logical object while relocating its physical embodiment, and RADOS can preserve an object while replica membership changes;
3. **identity of logical state ≠ identity of physical token** — delay-line regeneration, destructive-read core restore, DRAM regeneration, mapped Flash, and RADOS recovery all preserve logical sameness through changed physical state;
4. **idle nonvolatility ≠ read invariance** — the grounded magnetic-core evidence shows that an element can retain remanent state without maintenance energy yet the bounded classic read operation can destroy that state and require rewrite;
5. **access can itself create a retention obligation** — classic destructive-read core and Dennard's bounded 1T1C embodiment may require immediate rewrite after read;
6. **destructive read is a regime, not an essence of magnetic core** — contemporary 1953–1954 nondestructive sensing/readout work bounds the classic destructive-read case and rejects `all core reads are destructive`;
7. **time can itself create a retention obligation** — DRAM adds a distinct deadline: charge leakage requires scheduled regeneration even without useful access;
8. **dynamic retention ≠ destructive read** — Dennard disclosed nondestructive alternatives; Intel 1103 manufacturer documentation combines dynamic storage and periodic refresh with nondestructive read; AMD's 1976 Am9050 directly combines a one-transistor/capacitor cell, nondestructive read, and mandatory refresh;
9. **identity persistence ≠ location persistence** — Ban's Flash mapping explicitly keeps logical unit identity stable while the physical location changes; RADOS extends this across independently failing devices;
10. **logical invalidation ≠ physical erasure** — a block can be marked deleted / not current before the containing Flash erase unit is physically erased;
11. **metadata can be constitutive of retention** — in mapped Flash, maps/allocation state identify the current embodiment; in RADOS, cluster-map, placement, version, and recovery state help establish which replicas currently count;
12. **maintenance can be space/reclaim-triggered** — a nonvolatile medium may still require deferred copying and erasure so repeated logical rewrites can continue;
13. **replica multiplicity ≠ retained currentness** — several physical copies may exist while only a version-consistent subset represents the current ordered state;
14. **maintenance can be failure/repair-triggered** — distributed redundancy can degrade after failure or membership change and be restored by reconstructing current state onto replacement members;
15. **logical success ≠ durable commit** — the bounded 2006 RADOS design distinguishes replicated in-memory acknowledgement from later persistent-media commit, and the contemporaneous 2007 dissertation preserves this distinction across the expanded replication discussion;
16. **retention of currentness metadata can be guarded separately from every material replica** — the 2007 RADOS paper explicitly protects PG logs describing what a PG should contain even while object replicas may remain missing during background recovery;
17. **readability ≠ authorized currentness** — the 2007 RADOS design makes map-epoch and heartbeat state part of deciding whether an otherwise reachable replica may safely answer a read;
18. **refresh can be shared reconstruction, not merely a timer event** — commercial DRAM documentation makes row selection, sense amplification, restoration, and return-to-cell part of maintaining a large array of minimal storage cells.

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
- at least one case where logical identity survives loss/replacement of a replica member;
- philosophical comparison must be performed after, not instead of, mechanism reconstruction.

Current evidence-maturity count: **3 / 4 required grounded cases**. Magnetic core grounds quiescent remanence plus access-triggered restoration and a contemporary nondestructive boundary; DRAM grounds deadline-driven restoration and shared sense/restore infrastructure; RADOS grounds distributed currentness and repair. One more case still needs source deepening before synthesis is allowed, and the variety conditions remain relevant even after the numeric threshold is reached.
