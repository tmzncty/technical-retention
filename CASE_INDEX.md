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
| [Powered Flip-Flop Working Retention: Eccles–Jordan to ENIAC](cases/06-flip-flop-powered-working-retention.md) | **first-pass** | powered regenerative/bistable working state + explicit set/reset/clear; no periodic refresh established in the bounded thermionic case | stress-test the category at very short intervals; separate continuous power from periodic maintenance; allow later state-sensitive use without a discrete retrieval transaction | directly inspect the 1919 Eccles–Jordan trigger-relay paper/reprint, inspect ENIAC Part II/circuit drawings, and add a period primary `register` boundary before promotion |

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
| Powered flip-flop / ENIAC | regenerative vacuum-tube circuit condition used as normal/abnormal machine state | operating power and stable circuit conditions; explicit set/reset/clear; no scheduled state refresh established in the bounded evidence | bounded ENIAC output/gate use is nondestructive; reset is separate | a flip-flop can be directly wired into later logic; counters/accumulators provide higher-level organization rather than retention requiring an address | fixed circuit element while powered | no; working condition is current state only |

---

## Cross-case findings already supported

After seven bounded cases, **abacus/passive position, magnetic core, DRAM, mapped Flash, and RADOS are `grounded`; delay line and powered flip-flop remain `first-pass`.** The repository satisfies both the numeric and mechanism-variety gates for bounded synthesis. This does **not** make the provisional theses conclusions: new technical bridges must remain free to break or revise the current relational criterion.

1. **state retention ≠ history retention** — all cases preserve current working state without automatically preserving the complete sequence that produced it;
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
38. **the location-detachment sequence is functional, not teleological** — fixed cells, stable addresses, remapped blocks, and distributed replicas can coexist in one modern stack; the audit's stages do not establish one inevitable historical ascent toward placeless storage;
39. **technical forgetting is layer-relative** — a forgetting claim must name whether the lost target is a physical distinction, logical value/identity, mapping/currentness relation, serviceability, history, or durability threshold;
40. **physical loss ≠ higher-level forgetting** — ordinary DRAM reconstruction replaces charge, Flash reclamation can erase an obsolete embodiment, and RADOS can replace a failed replica while preserving the logical state;
41. **physical survival ≠ retained current state** — an uninterpretable positional configuration, an invalidated Flash block, or a stale/deauthorized RADOS replica can remain materially present after it has ceased to function as the intended current state;
42. **missed maintenance can be a forgetting mechanism, but maintenance triggers differ** — destructive core read creates an access-triggered restore obligation, DRAM creates a deadline-triggered refresh obligation, and distributed systems create failure/repair-triggered obligations;
43. **relation loss can matter as much as payload loss** — positional convention/procedure, Flash mapping/allocation, and RADOS version/PG-log/currentness state can be required to recover which surviving state is meaningful or current;
44. **unavailability, staleness, logical deletion, and physical erasure are not synonyms** — each can occur without some of the others, and temporary loss of service should not be counted as technical forgetting merely because the state cannot be used at one moment;
45. **maintenance visibility is observer-relative** — a DRAM refresh can be absent from an application's semantic model while remaining a first-class timing/design obligation; RADOS repair can be transparent to an object client while highly visible to operators;
46. **automation ≠ invisibility** — a system can automate restore, refresh, remapping, or repair while exposing timing, degraded state, capacity consumption, diagnostics, or implementation constraints to another layer;
47. **interface invisibility ≠ labor disappearance** — core manufacturing/support work and distributed replacement/infrastructure remain material and institutional even when a logical memory/object interface hides lower-layer operations;
48. **nonvolatility can reduce one maintenance obligation while leaving others intact** — core remanence and Flash quiescence remove periodic refresh merely to keep an idle physical state present, but access, mapping, reclaim, wear, failure, and system-support obligations remain;
49. **reliability is not one cross-period scalar** — positional disturbance, half-select/sense error, missed refresh, Flash wear/block failure, and replica/currentness failure are different failure models and cannot be ranked by one unsupported `more reliable` scale;
50. **self-healing ≠ maintenance-free** — automated distributed repair still depends on surviving current state, functioning control machinery, spare capacity, replacement members, and physical failure-domain assumptions;
51. **stable interfaces can relocate retention work** — classic core hides read–rewrite in the memory cycle, DRAM hides scheduled reconstruction below ordinary software, mapped Flash hides physical relocation behind logical designation, and RADOS hides replica replacement behind the object service;
52. **work displacement is functional, not teleological** — visible human procedure, device/controller work, protocol repair, manufacturing, and operations coexist in modern stacks; the evidence does not establish a historical law that later systems necessarily hide more maintenance or use less human labor;
53. **operational analysis ≠ continuous-retention ontology** — Ernst's demand to inspect what a technical medium does is methodologically strong, but quiescent positional, core, and Flash states reject the inference that a retained state must be continuously acted upon merely to remain;
54. **retention-time operation ≠ access-time operation** — a core can retain remanence without power yet require a timed sense/rewrite sequence on access; a passive positional state can remain while selection and interpretation occur only when a human returns to it;
55. **microtemporality is mechanism-dependent rather than universal** — pulse phase, sense timing, and DRAM refresh deadlines make short timescales causally decisive in some mechanisms, while Flash reclamation and RADOS repair may be deferred or event-triggered on longer operational horizons;
56. **quiescence is itself a temporal regime** — `nothing must happen yet` is an engineering fact when a mechanism lacks a recurring reconstruction deadline under specified conditions; quiescent retention is not absence of temporality;
57. **technical retention has plural operational timescales** — continuous circulation, access-triggered restore, deadline-driven refresh, workload/capacity/wear triggers, failure/membership repair, and human procedural continuity should not be collapsed into one generic `time-critical` rhythm;
58. **philosophical fit cannot promote evidence maturity** — the first-pass delay-line case is especially congruent with Ernstian microtemporality, but that conceptual fit does not substitute for its still-open source-grounding tasks;
59. **technical retention is broader than Stieglerian tertiary retention** — a retained machine state can be technically real and analytically important without thereby participating in the thicker relation of exteriorization, repetition, learning, or transmission that the bounded Stiegler test tracks;
60. **substrate class does not decide philosophical class** — volatile DRAM, nonvolatile Flash, and replicated objects can all support tertiary-retentional traces, while arbitrary internal states on the same substrates need not play the same retentional role;
61. **retentional object ≠ all constitutive retention infrastructure** — mappings, currentness/version state, refresh, placement, and repair can be required to sustain an exteriorized trace without being philosophically identical to that trace;
62. **Bestand ≠ storage** — Heidegger's primary text places storing within a larger chain of transformation/distribution/switching and treats standing-reserve as a mode of orderability rather than a noun for stored items;
63. **technical availability ≠ Heideggerian orderability** — designation, resolution, currentness/admissibility, and recovery can explain whether a system can service a request, but that engineering relation does not by itself establish Heidegger's mode of revealing;
64. **mere later usability is not enough for standing-reserve** — the grounded abacus case is a negative control: an intentionally retained state can be selected for a later operation without licensing the claim that any usable retained state is Heideggerian `Bestand`;
65. **replaceable embodiment can increase flexible callability without producing immateriality** — mapped Flash and RADOS preserve logical service through changing embodiments, but that service remains dependent on physical media/topology and retained mapping, placement, authority, and repair relations;
66. **physical presence ≠ orderable currentness** — an invalidated Flash embodiment or stale/deauthorized RADOS replica can survive materially and even be readable while no longer counting as the state that the current interface may order or return;
67. **forensic materiality ≠ a universal remanence law** — Kirschenbaum's materiality discipline remains useful beyond disk, but no mechanism-level evidence supports the claim that every obsolete digital state remains indefinitely recoverable merely because it once had a physical embodiment;
68. **interface disappearance ≠ raw-media absence** — grounded Flash already separates logical invalidation from later physical erase, and the bounded FAST 2011 SSD comparison experimentally shows that FTL indirection can leave raw-Flash remnants invisible through the normal host interface;
69. **forensic witness ≠ authoritative current state** — an obsolete Flash embodiment or stale RADOS replica can preserve evidence of an earlier state without being the embodiment that mapping/version/currentness rules authorize as current;
70. **logical-object survivability ≠ current-embodiment survivability ≠ forensic-trace survivability** — remapping and replica replacement can preserve the logical object while earlier embodiments disappear, while stale traces can also survive after they cease to participate in current service;
71. **logical repeatability can be achieved through material nonidentity** — stable Flash designations and RADOS object identities can return what counts as the same logical state across changed physical locations or replica membership, so repeatability does not imply continuity of one material token;
72. **physical survival ≠ forensic accessibility** — recoverability of a surviving embodiment depends on the medium, controller state, reclamation history, instrumentation, encryption/key relations, and the relevant adversary/interface rather than on material persistence alone;
73. **distributed replication can multiply material witnesses without multiplying current authority** — RADOS replicas may have different individualized material histories while protocol version/epoch/peering rules still establish one admissible current state for service;
74. **technical retention ≠ one physical or engineering mechanism** — the grounded cases share no common remanence, refresh, mapping, replication, address, or maintenance operation; any mechanism-specific definition already has direct counterexamples;
75. **technical retention ≠ generic physical persistence or causal residue** — material survival alone is insufficient because positional meaning can be lost while configuration survives, and Flash/RADOS embodiments can survive after losing current logical status or authority;
76. **the current minimal cross-case invariant is target-relative admissible continuation across time** — analysis must name a retention target, temporal separation, continuity mechanism, later recovery/interpretation/admissibility operation, and a sameness/currentness rule explaining why the later state counts as the target;
77. **recoverability is target-relative** — a stale Flash page or old RADOS replica may be recoverable as a forensic/historical trace while not being recoverable as the current operational object, so `can be recovered` is incomplete without `recovered as what`;
78. **technical retention has no currently justified minimum duration** — working positional state and volatile DRAM block an arbitrary durability threshold; the next latch/register bridge must test whether the category becomes trivial at very short intervals;
79. **one controlled relation does not imply one natural technology kind** — the grounded mechanisms are better compared through cross-cutting axes such as continuity target, maintenance trigger, embodiment replacement, recovery performer, and currentness/interpretation rule than forced into mutually exclusive `passive/active/distributed` subfamilies;
80. **category coherence is provisional and evidence-gated** — the current result is supported only by the five grounded regimes; the first-pass delay-line case and future latch/cache/SSD/filesystem/RAID cases must be allowed to break or revise the relational criterion rather than being forced into it;
81. **short duration ≠ trivial retention** — ENIAC's decade flip-flop can preserve a pending carry condition across intervening pulse activity until a later reset/carry phase; the operational difference between `state remained` and `state failed to remain` is real even when the interval is tiny compared with archival storage;
82. **continuous power ≠ periodic state maintenance** — the bounded thermionic flip-flop requires operating power for its regenerative state to exist, but the primary evidence does not establish a DRAM-like deadline-driven rewrite or a delay-line-like circulation operation merely to hold either state;
83. **volatility ≠ dynamic refresh** — ENIAC power-up can yield accidental flip-flop states and requires initialization, yet the bounded evidence does not show periodic refresh of a correctly powered flip-flop; loss on power interruption and deadline-driven reconstruction are different properties;
84. **later retention can be demonstrated by state-sensitive use rather than discrete retrieval** — ENIAC's static outputs and gate-control uses show that retained state may remain continuously exposed to downstream circuitry and matter when a later operation acts on it, so the cross-case criterion should not require a separate storage-style read transaction;
85. **flip-flop mechanism ≠ register architecture** — Eccles–Jordan's primary vocabulary is relay/amplification/retroaction, while ENIAC distinguishes flip-flops, ring counters, and accumulators; later `register` terminology must be sourced rather than used as a synonym for any bistable element;
86. **initialization is part of usable working retention** — ENIAC's random power-up states show that possessing a bistable physical state is not sufficient for computation; clearing establishes a system-admissible starting state before later continuity can be interpreted as retained working state.

These are provisional cross-case findings, not final philosophical conclusions. Audits 01–06 test all six project-level theses explicitly; the cross-audit ledger records both the revised survivors and the negative results. The named philosophical/prior-art sequence includes [`docs/PHILOSOPHICAL_TEST_01_ERNST_OPERATIONALITY.md`](docs/PHILOSOPHICAL_TEST_01_ERNST_OPERATIONALITY.md), [`docs/PHILOSOPHICAL_TEST_02_STIEGLER_TERTIARY_RETENTION.md`](docs/PHILOSOPHICAL_TEST_02_STIEGLER_TERTIARY_RETENTION.md), [`docs/PHILOSOPHICAL_TEST_03_HEIDEGGER_ORDERABILITY.md`](docs/PHILOSOPHICAL_TEST_03_HEIDEGGER_ORDERABILITY.md), and [`docs/PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md`](docs/PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md). The first category-coherence result is recorded in [`docs/SYNTHESIS_AUDIT_07_TECHNICAL_RETENTION_COHERENCE.md`](docs/SYNTHESIS_AUDIT_07_TECHNICAL_RETENTION_COHERENCE.md). Case 06 is the first post-audit adversarial bridge and already requires `later state-sensitive use` to be accepted alongside explicit recovery.

---

## Current synthesis gate

The **mechanism gate is now closed**. A synthesis pass may begin, but it must be bounded and evidence-led rather than a declaration of one universal ontology of storage.

- [x] at least four contrasting cases at `grounded` or better — currently five;
- [x] at least one **passive-position** case at `grounded` or better — grounded Case 00;
- [x] at least one case of active refresh / circulation at `grounded` or better — grounded DRAM satisfies the refresh side of this condition;
- [x] at least one case of nonvolatile physical remanence or trapped state at `grounded` or better — grounded magnetic core and mapped Flash satisfy this from different mechanisms;
- [x] at least one case where logical identity survives physical relocation — grounded mapped Flash;
- [x] at least one case where logical identity survives loss/replacement of a replica member — grounded RADOS;
- [x] all six README project-level theses have received bounded synthesis audits; none is promoted to a final conclusion;
- [x] named prior-art tests completed for Ernst operationality/microtemporality, Stiegler tertiary-retention boundary, Heidegger orderability/standing-reserve, and Kirschenbaum forensic/formal materiality beyond disk;
- [x] first category-coherence audit completed in [`docs/SYNTHESIS_AUDIT_07_TECHNICAL_RETENTION_COHERENCE.md`](docs/SYNTHESIS_AUDIT_07_TECHNICAL_RETENTION_COHERENCE.md): no single physical mechanism survives, but a target-relative relation of technically organized continuation and later admissibility currently survives across the five grounded regimes.

**Current adversarial bridge:** [`cases/06-flip-flop-powered-working-retention.md`](cases/06-flip-flop-powered-working-retention.md) is `first-pass`. It supports short-lived working retention and forces a wording refinement: later continuity may be shown through **state-sensitive use**, not only through explicit recovery/retrieval. It also separates continuous power from periodic state reconstruction and keeps `flip-flop ≠ register` as an anti-anachronism boundary.

**Next highest-value unit:** source-deepen Case 06 before opening the next semiconductor bridge. Inspect the original 1919 Eccles–Jordan trigger-relay paper or page-preserving reprint, the relevant ENIAC circuit drawings / Part II circuit description, and a period primary source for `register` as an architectural grouping/role. Promote only if those sources confirm the current mechanism boundaries.
