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
| [Abacus as Retained Position](cases/00-abacus-retained-position.md) | **grounded** | passive mechanical position + human interpretation | establish passive positional working retention without importing `register`; distinguish state constraint, interpretation, and genealogy | [1592 / counting-rod / 1525 line-reckoning grounding record](evidence/00-abacus-rod-line-reckoning-grounding.md); future work is edition/comparative cleanup |
| [Mercury Delay-Line Memory: Retention as Circulation](cases/01-mercury-delay-line-circulation.md) | **first-pass** | recirculation + regeneration | persistence as continuous activity; time as access geometry; identity through re-creation | exact patent/page anchors; direct 1949 IRE inspection; temperature-control primary source |
| [Magnetic Core Memory: Retention at Rest, Destruction in Reading](cases/02-magnetic-core-destructive-read.md) | **grounded** | remanence + destructive read / restore in the bounded classic scheme | separate idle nonvolatility from read invariance; show access itself can create a retention obligation; bound destructive read with contemporary nondestructive alternatives | [1951–1954 grounding record](evidence/02-magnetic-core-1951-1954-grounding.md); future work should be narrow archival/semantic archaeology rather than generic core-memory expansion |
| [DRAM Refresh as Scheduled Restoration](cases/03-dram-refresh-as-scheduled-restoration.md) | **grounded** | decaying charge + periodic regeneration; destructive-read restore in bounded 1T1C embodiment | separate time-triggered maintenance from access-triggered restore; stable logical address over repeatedly restored physical charge | [1967–1982 grounding record](evidence/03-dram-1967-1982-grounding.md); future work should be narrow failure/semantic archaeology rather than generic DRAM expansion |
| [Flash Virtual Mapping: Logical Identity Without Physical Location](cases/04-flash-virtual-mapping-logical-identity.md) | **grounded** | nonvolatile Flash + virtual/logical/physical mapping + deferred reclamation + bounded wear/failure management | identity persistence without location persistence; logical invalidation vs physical erase; mapping metadata as retained state; reclamation vs wear leveling | [1992–1998 grounding record](evidence/04-flash-1992-1998-grounding.md); full Masuoka 1987 paper remains archival cleanup; TRIM/secure erase remain separate later cases |
| [RADOS Replicated Objects: Retention by Replica Agreement and Repair](cases/05-rados-replicated-object-repair.md) | **grounded** | n-way replication + versioned primary authority + failure-triggered repair | currentness beyond copy multiplicity; no permanently privileged physical home; repair-triggered retention; ack vs durable commit | [2006–2007 grounding record](evidence/05-rados-2006-2007-grounding.md); future work should be narrow semantic/version archaeology rather than generic Ceph expansion |

---

## Comparison matrix — provisional

This matrix should become more precise as cases mature.

| Case | State substrate | Active retention work | Read | Addressing | Location stability | History retained by default? |
| --- | --- | --- | --- | --- | --- | --- |
| Abacus / reckoning surface | bead/counter position + positional convention + procedural context | mostly human protection / interpretation / selection; no machine refresh merely to remain | nondestructive visual/manual | human-mediated spatial selection through positional convention | high during one configuration | no |
| Delay line | propagating pulse pattern | continuous circulation / regeneration / retiming | electronically sensed; state continues by recirculation | temporal slot + index | not meaningfully static | no |
| Magnetic core | remanent magnetization | little merely to remain at rest; active restore after classic destructive read | destructive in the bounded classic case, followed by rewrite when logical value must persist; contemporary nondestructive schemes also existed | coincident coordinate selection; nonselected cores must tolerate half-select disturbance | high at the selected core | no |
| DRAM | capacitor / storage-node charge | periodic regeneration because of leakage; shared row-level sense/restore infrastructure; restore after destructive read in the bounded Dennard 1T1C embodiment | destructive in the bounded Dennard embodiment; commercial dynamic memories can have nondestructive reads | stable row/column selection through decoders and shared sense/restore infrastructure | logical cell stable while physical charge is repeatedly renewed | no |
| Mapped Flash | nonvolatile cell state + allocation/mapping metadata | out-of-place update, map maintenance, reclamation; wear equalization is a distinct optional objective; bad-block/ECC replacement appears in later bounded NAND evidence | map-mediated read of current physical embodiment | stable virtual/logical designation translated through retained mapping state | deliberately unstable under rewrite/reclaim | usually no; stale physical embodiments may cease to count before erase |
| RADOS | multiple object replicas + cluster map + PG/version/recovery state | replication, failure detection, peering, re-replication, migration/recovery | protocol-authorized current replica; exact read role depends on replication scheme | object → PG → CRUSH/current map → candidate OSD set, then currentness/authority checks | no permanently privileged physical home | no by default; PG logs retain bounded recovery history and can be guarded separately from every replica |

---

## Cross-case findings already supported

After six bounded cases, **abacus/passive position, magnetic core, DRAM, mapped Flash, and RADOS are `grounded`; delay line remains `first-pass`.** The repository now satisfies both the numeric and mechanism-variety gates for beginning a bounded synthesis pass. This does **not** make the provisional theses conclusions: philosophical comparison must still be performed against the grounded mechanisms rather than substituted for them.

1. **state retention ≠ history retention** — all six cases preserve current working state without automatically preserving the complete sequence that produced it;
2. **retention mechanism ≠ apparent persistence** — an abacus configuration can sit still, a delay-line pattern survives by continual circulation, a core can remain magnetized at rest, a DRAM cell survives for a bounded interval before scheduled regeneration, mapped Flash can preserve a logical object while relocating its physical embodiment, and RADOS can preserve an object while replica membership changes;
3. **passive positional retention can be operational without autonomous machine readout** — Cheng's 1592 procedure directly couples designated abacus positions with an instruction to leave the completed numerical configuration unmoved, while Ries's 1525 line reckoning independently shows a positional counter field used as part of arithmetic;
4. **the retained state may be a relation rather than an isolated token** — in positional calculation, counter + position + convention + procedure constitute the actionable state; later mapped/distributed systems automate increasingly large parts of comparable identity relations;
5. **the degree to which a medium constrains legal states matters** — a bead frame constrains movement/position more strongly than an open line-reckoning surface even though both can support passive positional working retention;
6. **historical material operation and modern reconstruction must remain layered** — early Chinese procedural texts establish placement/position language, while exact counting-rod manipulation sometimes remains a specialist reconstruction rather than a directly described artifact operation;
7. **cross-cultural functional similarity ≠ genealogy** — Cheng 1592 and Ries 1525 can support a shared mechanism comparison without proving transmission, common origin, or modern-register ancestry;
8. **identity of logical state ≠ identity of physical token** — delay-line regeneration, destructive-read core restore, DRAM regeneration, mapped Flash, and RADOS recovery all preserve logical sameness through changed physical state;
9. **idle nonvolatility ≠ read invariance** — the grounded magnetic-core evidence shows that an element can retain remanent state without maintenance energy yet the bounded classic read operation can destroy that state and require rewrite;
10. **access can itself create a retention obligation** — classic destructive-read core and Dennard's bounded 1T1C embodiment may require immediate rewrite after read;
11. **destructive read is a regime, not an essence of magnetic core** — contemporary 1953–1954 nondestructive sensing/readout work bounds the classic destructive-read case and rejects `all core reads are destructive`;
12. **time can itself create a retention obligation** — DRAM adds a distinct deadline: charge leakage requires scheduled regeneration even without useful access;
13. **dynamic retention ≠ destructive read** — Dennard disclosed nondestructive alternatives; Intel 1103 manufacturer documentation combines dynamic storage and periodic refresh with nondestructive read; AMD's 1976 Am9050 directly combines a one-transistor/capacitor cell, nondestructive read, and mandatory refresh;
14. **identity persistence ≠ location persistence** — Ban's Flash mapping explicitly keeps logical unit identity stable while the physical location changes; Intel's 1995 FTL description independently presents logical-to-physical remapping as the mechanism by which a virtual block service survives Flash erase geometry; RADOS extends this across independently failing devices;
15. **logical invalidation ≠ physical erasure** — a block can cease to count as current (`deleted`, `dirty`, or invalidated) before the containing Flash erase unit is physically erased;
16. **metadata can be constitutive of retention** — in mapped Flash, maps/allocation state identify the current embodiment; in RADOS, cluster-map, placement, version, and recovery state help establish which replicas currently count;
17. **maintenance can be space/reclaim-triggered** — a nonvolatile medium may still require deferred copying and erasure so repeated logical rewrites can continue;
18. **reclamation ≠ wear leveling** — reclamation recovers writable capacity while preserving current data; Wells's 1992-lineage wear-leveling patent adds the distinct objective of distributing switching/erase burden to extend usable medium life;
19. **historical terminology must follow the source** — Ban's 1993-filed system uses `virtual map` / logical-unit vocabulary; Intel AP-619 documents `Flash Translation Layer (FTL)` as a PCMCIA-approved format by August 1995. Earlier mechanisms should not be retroactively renamed without evidence;
20. **replica multiplicity ≠ retained currentness** — several physical copies may exist while only a version-consistent subset represents the current ordered state;
21. **maintenance can be failure/repair-triggered** — distributed redundancy can degrade after failure or membership change and be restored by reconstructing current state onto replacement members; bounded 1998 NAND evidence also shows block replacement as a local device-management response to program/erase failure;
22. **logical success ≠ durable commit** — the bounded 2006 RADOS design distinguishes replicated in-memory acknowledgement from later persistent-media commit, and the contemporaneous 2007 dissertation preserves this distinction across the expanded replication discussion;
23. **retention of currentness metadata can be guarded separately from every material replica** — the 2007 RADOS paper explicitly protects PG logs describing what a PG should contain even while object replicas may remain missing during background recovery;
24. **readability ≠ authorized currentness** — the 2007 RADOS design makes map-epoch and heartbeat state part of deciding whether an otherwise reachable replica may safely answer a read;
25. **refresh can be shared reconstruction, not merely a timer event** — commercial DRAM documentation makes row selection, sense amplification, restoration, and return-to-cell part of maintaining a large array of minimal storage cells;
26. **retention ≠ addressability** — a state can remain physically present while the selector, map, convention, or index needed to choose it is absent; passive positional retention can also be operationally selected by a human without autonomous machine addressing;
27. **address stability ≠ location stability** — DRAM preserves a stable cell-selection relation across repeated reconstruction, while mapped Flash and RADOS preserve higher-level designations across deliberate physical relocation or replica replacement;
28. **address resolution ≠ currentness authorization** — mapped Flash can leave an old embodiment physically present after logical invalidation, and RADOS can resolve a reachable replica that is stale or not currently authorized to answer;
29. **selection machinery can be retention machinery** — magnetic-core half-select margins/destructive read and DRAM sense/restore show that the way a state is selected can create disturbance or reconstruction obligations rather than merely revealing an independent stored value;
30. **addressability is not one historical scalar** — human spatial selection, coordinate decoding, logical translation, and distributed placement are different operational relations with different costs; the repository should not narrate them as a simple monotonic ascent from `less` to `more` addressable;
31. **physical-token continuity ≠ physical-home continuity** — classic core restore and bounded DRAM regeneration can replace the immediate magnetic/electrical state while continuing to use the same selected physical location;
32. **location can be constitutive of a retained identity** — positional calculation is a counterexample to any universal `logical state is location-independent` thesis because position participates directly in the operative numerical meaning;
33. **relocation ≠ immateriality** — mapped Flash and RADOS let a logical identity survive replacement of physical embodiments, but every current embodiment remains material and subject to device/topology constraints;
34. **removing one permanent home can increase dependence on retained relations** — Flash mapping/allocation state and RADOS placement/version/currentness state become constitutive precisely because physical embodiments are replaceable;
35. **physical topology remains relevant after location abstraction** — RADOS uses failure-domain topology in placement, so absence of one permanent home does not make `where replicas are` irrelevant to durability;
36. **permanent physical home ≠ temporary protocol authority** — RADOS can move replicas and primary/read roles while still requiring protocol-defined authority over which state may order or answer as current;
37. **mobility can create maintenance rather than eliminate it** — Flash relocation creates map/reclamation obligations and distributed replica replacement creates peering/repair obligations;
38. **the location-detachment sequence is functional, not teleological** — fixed cells, stable addresses, remapped blocks, and distributed replicas can coexist in one modern stack; the audit's stages do not establish one inevitable historical ascent toward placeless storage.

These are provisional cross-case findings, not final philosophical conclusions. Audits 01–04 now test maintenance, temporal-transfer, addressability, and privileged-location claims explicitly. The next bounded synthesis task is one cross-audit counterexample ledger before any provisional thesis is promoted to a conclusion.

---

## Current synthesis gate

The **mechanism gate is now closed**. A synthesis pass may begin, but it must be bounded and evidence-led rather than a declaration of one universal ontology of storage.

- [x] at least four contrasting cases at `grounded` or better — currently five;
- [x] at least one **passive-position** case at `grounded` or better — grounded Case 00;
- [x] at least one case of active refresh / circulation at `grounded` or better — grounded DRAM satisfies the refresh side of this condition;
- [x] at least one case of nonvolatile physical remanence or trapped state at `grounded` or better — grounded magnetic core and mapped Flash satisfy this from different mechanisms;
- [x] at least one case where logical identity survives physical relocation — grounded mapped Flash;
- [x] at least one case where logical identity survives loss/replacement of a replica member — grounded RADOS;
- [x] bounded philosophical/engineering comparison has begun **after** mechanism reconstruction through synthesis audits 01–04; provisional theses remain revisable and are not final conclusions.

**Next highest-value unit:** build a cross-audit counterexample ledger that records which provisional theses have been rejected, narrowed, split, retained with scope conditions, or left untested. Do this before promoting any thesis to a conclusion or opening a grand synthesis chapter.
