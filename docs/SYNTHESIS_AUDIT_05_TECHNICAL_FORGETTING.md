# Synthesis Audit 05 — Technical Forgetting

> **Question:** does README thesis 4, `Forgetting has mechanisms`, survive contact with the five grounded retention regimes, and if so what has to be distinguished before the word `forgetting` is analytically useful?

**Status:** bounded synthesis audit. This is not a philosophy of forgetting and not a complete failure taxonomy.

The formal evidence base is limited to the five `grounded` cases in [`CASE_INDEX.md`](../CASE_INDEX.md):

- passive positional reckoning;
- classic magnetic core in the bounded destructive-read scheme;
- bounded 1T1C / commercial DRAM;
- mapped Flash, 1992–1998;
- RADOS, 2006–2007.

The mercury delay-line case remains `first-pass` and is not silently promoted here.

This audit reuses already inspected primary evidence and their exact anchors in the case grounding records. It adds a cross-case engineering vocabulary; it does **not** claim that historical actors used the modern category `technical forgetting`.

---

## 1. Verdict

The weak proposition survives:

> **Technical forgetting has mechanisms.**

But the proposition is too weak unless the object and layer of forgetting are named. The stronger useful formulation is:

> **A retained state can cease to remain usable because its physical distinction is destroyed, a required maintenance obligation is missed, its logical/current identity is invalidated, or a relation required to select, interpret, authorize, or reconstruct it is lost. These are different mechanisms, and none is equivalent to mere unavailability. Lower-layer destruction can also be masked by relocation, reconstruction, or redundancy, so physical loss does not automatically imply higher-layer forgetting.**

This audit therefore classifies thesis 4 as **retained with scope + decomposed**.

The decomposition matters more than the slogan. Across the grounded cases, at least five distinct events are easy to collapse into the single word `forgetting`:

1. destruction or disturbance of a physical distinction;
2. failure to perform required restoration before a deadline or after a destructive operation;
3. logical invalidation of an embodiment that physically survives;
4. loss of a relation that identifies, interprets, or authorizes the current state;
5. loss of service/recoverability despite some lower-layer trace still surviving.

The converse also matters: physical destruction can occur without logical forgetting if the system has already preserved an equivalent current state elsewhere.

---

## 2. The target of forgetting must be named

Earlier audits already showed that `the data persist` is incomplete. The same problem applies to `the data are forgotten`.

A forgetting claim should identify which target has ceased to be retained:

- **physical distinction** — a bead configuration, remanent magnetic state, capacitor-charge difference, programmed Flash state, or one replica embodiment;
- **logical value** — the value the system still treats as recoverable;
- **logical identity** — which value belongs to a named block/object/position;
- **currentness / authority** — which surviving embodiment is admitted as the current state;
- **relation / metadata** — mapping, placement, version, convention, or procedure needed to recover or interpret the state;
- **serviceability** — whether future reads/writes/recovery can still be performed;
- **durable threshold** — whether a value survived only in volatile acknowledgement state or reached a stronger commit condition.

The phrase `forgotten state` is therefore under-specified until the target layer is stated.

---

## 3. Case audit

## 3.1 Passive positional reckoning — forgetting can be disturbance or loss of interpretation

The Cheng Dawei grounding record supplies direct primary evidence for a completed abacus result being left unmoved (`待數莫動`) in a procedure with designated positions. The Ries comparison likewise depends on a positional counter field. See [`evidence/00-abacus-rod-line-reckoning-grounding.md`](../evidence/00-abacus-rod-line-reckoning-grounding.md).

Two forgetting mechanisms follow from the grounded case.

### A. Physical / configurational disturbance

If beads or counters are moved, cleared, or reset without another record, the prior working configuration normally ceases to exist. This is a straightforward destruction of the current working state.

### B. Interpretive / procedural loss

The physical arrangement alone is not the whole retained numerical state. The grounding record already shows that actionable state depends on position + convention + procedure. A configuration can therefore physically survive while its operational meaning becomes unavailable because the convention or procedural context is lost.

This is not evidence that Ming users called such an event `forgetting`. It is a modern engineering comparison constrained by the historical evidence.

### Counterexample supplied by the case

**Physical survival is not sufficient for operational retention.** A bead configuration can remain exactly where it was and still cease to function as retained numerical state for an observer who lacks the relevant positional/procedural relation.

At the same time, **mere temporary inability to inspect the board is not necessarily forgetting**. If the configuration and interpretive relation remain intact, later access can restore availability.

---

## 3.2 Magnetic core — destructive access can create a forgetting event if restore is omitted

The grounded magnetic-core evidence separates quiescent remanence from destructive read. Forrester's patent, Papian's 1953 M.I.T. machine paper, and Widrow's 1954 discussion all support the bounded classic sequence in which read drives the selected core toward a reference state and the prior logical value must be rewritten if it is to remain retained. See [`evidence/02-magnetic-core-1951-1954-grounding.md`](../evidence/02-magnetic-core-1951-1954-grounding.md).

### A. No periodic forgetting merely from idleness in the bounded claim

The core can remain in one of two stable remanent states without periodic refresh merely to keep the element's bit present. The case is therefore a counterexample to any universal equation:

```text
elapsed time without maintenance -> forgetting
```

### B. Access-triggered physical destruction

In the bounded destructive-read scheme, the read itself changes the physical state. If the prior value is not restored, the previously retained value has been physically replaced by the forced read-reference state.

This is a clean mechanism of technical forgetting:

```text
retained remanent state
    -> destructive read
    -> logical value is learned
    -> physical embodiment is reset
    -> restore omitted
    -> prior value no longer retained in that core
```

### Counterexample supplied by the case

**Access is not always epistemically neutral.** A system can forget because it read.

But the contemporary nondestructive-read sources also prevent universalizing this mechanism: `core read = forgetting risk` is a property of the bounded destructive-read regime, not an essence of magnetic cores.

---

## 3.3 DRAM — forgetting can be a missed maintenance deadline

The DRAM grounding record establishes charge leakage, periodic regeneration, commercial row-level refresh, and sense/amplify/return-to-cell practice. See [`evidence/03-dram-1967-1982-grounding.md`](../evidence/03-dram-1967-1982-grounding.md).

### A. Leakage is a physical process; forgetting occurs when recoverability is lost

Charge begins leaking before the stored value is necessarily unreadable. The useful boundary is therefore not `any physical drift = forgetting`.

The relevant retention failure occurs when the physical distinction has degraded far enough that the system can no longer reliably sense/reconstruct the intended value before refresh restores it.

### B. Missed refresh is deadline failure

DRAM adds a mechanism absent from passive position and quiescent core: a retained state can be lost because the maintenance operation does not occur within the required interval.

The grounded AMD Am9050 documentation makes the logic explicit: leakage eventually destroys the information unless cells are refreshed within the specified period. Intel AP-133 then shows refresh as sense → amplify → return-to-cell reconstruction.

The forgetting mechanism is therefore not simply `volatile device loses power`. It is more general:

```text
bounded physical distinction
    + required refresh deadline
    + deadline missed
    -> recoverability can collapse
```

### C. Normal refresh is not forgetting

Refresh deliberately replaces the immediate electrical state with a reconstructed one while preserving the higher-level logical value. Physical-token discontinuity is therefore not by itself a forgetting event.

### Counterexample supplied by the case

**Microscopic physical change can be constitutive of remembering rather than evidence of forgetting.** The system repeatedly replaces charge state in order to preserve the logical value.

---

## 3.4 Mapped Flash — logical invalidation, physical erasure, relation loss, and relocation must be separated

The 1992–1998 Flash evidence is especially useful because it forces several distinct events apart. Ban's 1993-filed patent, Wells's 1992-lineage wear-leveling work, Intel AP-619, and the later bounded Toshiba NAND evidence are summarized in [`evidence/04-flash-1992-1998-grounding.md`](../evidence/04-flash-1992-1998-grounding.md).

### A. Logical invalidation can precede physical erasure

In Ban's architecture, a rewritten virtual/logical block can be redirected to a new physical location while the old physical embodiment is marked `deleted and not writable`. Wells similarly describes replaced sectors becoming `dirty` before later clean-up.

The old physical state can therefore survive while it has already ceased to count as the current logical state.

This is a direct counterexample to:

```text
logical forgetting = physical erasure
```

### B. Physical erasure can occur without logical forgetting

During reclamation, still-current data are copied elsewhere before the old erase unit is erased. If mapping is updated correctly, physical destruction of the old embodiment is part of continued logical retention.

This reverses the naive equation:

```text
physical destruction -> forgetting
```

At the logical-object layer, the erase can be maintenance rather than forgetting.

### C. Mapping/allocation relation can be the thing that is lost

The grounding record shows that mapping/allocation metadata is required to identify which physical embodiment currently belongs to a virtual/logical identity. Some of that state is retained in Flash and some can be reconstructed from retained media metadata in the bounded sources.

If the relation cannot be recovered, payload bits may physically survive while the system can no longer determine which embodiment is current for the requested logical identity.

This is **relation loss**, not necessarily payload destruction.

### D. Bad-block replacement further separates local loss from logical loss

The bounded 1998 Toshiba evidence explicitly describes replacing a failed block with another block and preventing later access to the failed one. A local physical embodiment can be abandoned while the retained logical state is recreated elsewhere.

### Counterexample supplied by the case

Flash provides both directions of the distinction:

- a physical trace may survive after it has been logically invalidated;
- a physical embodiment may be erased or abandoned while the logical identity survives elsewhere.

Technical forgetting is therefore layer-relative.

---

## 3.5 RADOS — replica loss, stale state, currentness loss, and durable loss are different failures

The RADOS grounding record provides exact anchors for placement, versioning, peering, stale-read exclusion, `down`/`out`, re-replication, PG logs, and the distinction between replicated volatile `ack` and later on-disk `commit`. See [`evidence/05-rados-2006-2007-grounding.md`](../evidence/05-rados-2006-2007-grounding.md).

### A. Replica destruction need not be object forgetting

An OSD can fail or be marked out; RADOS can reconstruct the current object onto another member. Loss of one embodiment becomes a **repair trigger**, not necessarily loss of the logical object.

This is the distributed analogue of the Flash relocation counterexample:

> local physical loss can be absorbed by higher-layer redundancy and reconstruction.

### B. Stale does not mean erased

A replica can remain physically readable yet be stale or not currently authorized to answer. The 2007 design explicitly uses map epochs, peer communication, and heartbeat/currentness rules to exclude stale read authority.

The stale copy therefore survives as bytes while ceasing to count as current service state.

### C. Currentness / recovery relation can be a retention target

Peering uses versions, PG logs, intervening map epochs, and membership information to determine what the PG should contain. The 2007 paper explicitly protects PG log/currentness metadata even while some object replicas remain missing.

Consequently, loss of the relation that establishes `what is current` is analytically distinct from destruction of every payload copy.

### D. `ack` loss and committed-state loss are different thresholds

In the bounded 2006/2007 design, replicated in-memory acknowledgement occurs before final persistent-media commit. Clients retain writes until commit so they can participate in recovery after simultaneous loss of volatile OSD state.

A power event can therefore destroy an acknowledged physical/volatile embodiment without necessarily destroying the logical operation if replay/recovery still succeeds. Conversely, losing all recoverable participants before durable commit represents a different retention failure from losing one replica after commit.

### Counterexample supplied by the case

**Copy count is not a forgetting criterion.** One copy can disappear with no object loss, several copies can survive while disagreement/currentness prevents safe service, and surviving stale bytes are not equivalent to retained current state.

---

## 4. A bounded mechanism taxonomy

The grounded cases support the following provisional families. They are overlapping mechanisms, not a universal ontology.

| Mechanism family | What fails | Grounded examples | Important non-equivalence |
| --- | --- | --- | --- |
| **physical disturbance / destruction** | the physical distinction itself | moved/cleared counters; destructive core read without rewrite; Flash erase of one embodiment | physical loss may be masked by another current embodiment |
| **deadline / obligation failure** | required restoration does not occur in time or after a triggering operation | core read without restore; DRAM missed refresh | ordinary reconstruction is not itself forgetting |
| **logical invalidation / deauthorization** | a surviving embodiment ceases to count as current | Flash `deleted`/`dirty`; stale or unauthorized RADOS replica | invalidation/currentness loss is not physical erasure |
| **relation / metadata loss** | the relation needed to identify, interpret, map, or authorize state is lost | positional convention/procedure; Flash mapping/allocation; RADOS map/version/PG-log/currentness state | payload survival alone does not restore operational identity |
| **service / recoverability loss** | a state cannot be made usable although some trace may remain | missing interpretation, unrecoverable mapping/currentness, failed reconstruction | unavailability can be temporary; do not equate every outage with forgetting |

A sixth category, **history loss**, remains separate. All grounded cases can preserve current state without automatically preserving every prior state. Forgetting a previous version/history is not the same event as losing the current state.

---

## 5. Counterexamples that constrain the thesis

A useful technical-forgetting thesis must preserve all of the following negative results.

### 5.1 Physical loss ≠ logical forgetting

- DRAM refresh replaces the immediate electrical state while retaining the value.
- Flash reclamation can erase an obsolete physical embodiment after preserving current data elsewhere.
- RADOS can lose and replace one replica without losing the object.

### 5.2 Physical survival ≠ retained logical/current state

- an abacus/reckoning configuration can survive while interpretation/procedure is lost;
- stale Flash embodiments can survive after logical invalidation;
- RADOS replicas can remain readable while stale or unauthorized.

### 5.3 Logical invalidation ≠ physical erasure

Mapped Flash supplies direct primary evidence for this distinction. It must remain explicit anywhere deletion/forgetting is discussed.

### 5.4 Unavailability ≠ forgetting

A retained state can be temporarily unreachable, unselectable, or not yet safely admissible and later become available again. `Unavailable now` is therefore not a sufficient forgetting criterion.

### 5.5 Maintenance is not one temporal pattern

Forgetting from omitted maintenance can be:

- access-triggered — classic destructive core read without rewrite;
- deadline-triggered — DRAM refresh missed;
- failure/repair-triggered — distributed redundancy degrades and later recovery can fail;
- procedural — a human-maintained representational relation disappears.

The mechanism and trigger must be named.

### 5.6 Stale / obsolete state is not automatically `forgotten history`

An old physical embodiment may remain as residue even after it ceases to count as current. Conversely, retaining old embodiments does not imply a coherent version history. `state retention` and `history retention` remain separate.

---

## 6. What this audit changes in the project's vocabulary

The glossary's existing `technical forgetting` entry is directionally correct but its candidate list is too flat. After this audit, use the term only when the analysis identifies at least:

1. **target layer** — physical distinction, logical value/identity, relation/currentness, serviceability, or history;
2. **mechanism** — disturbance/destruction, missed maintenance, invalidation/deauthorization, relation/metadata loss, or failed reconstruction;
3. **masking / redundancy condition** — whether another embodiment or reconstruction path preserves the higher-level state;
4. **reversibility / recoverability boundary** — whether the event is temporary unavailability, a stale-but-surviving state, logical deletion, or actual loss of recoverable current state.

This does not make the taxonomy complete. Encryption-key destruction, media/format obsolescence, archival institutional abandonment, controller-wide failures, and long-term bit rot remain outside the five grounded cases and must not be treated as already audited merely because they appear in the roadmap.

---

## 7. Historical, engineering, analogy, and philosophical boundaries

### Historical record

The historical claims remain those established in the source records: Cheng's positional instruction, documented destructive-read/restore core cycles, manufacturer DRAM refresh requirements, Flash invalidation/remapping/reclamation vocabulary, and RADOS version/peering/repair/currentness semantics.

### Engineering reconstruction

The cross-case taxonomy in this document is a modern analytical reconstruction. Terms such as `relation loss` or `technical forgetting mechanism family` are not projected backward as historical actors' categories.

### Functional analogy

Comparing a lost positional convention with lost Flash mapping or RADOS currentness metadata is useful only at the limited level that **a surviving physical payload can fail to remain operationally identifiable/current without a retained relation**. It establishes no genealogy or architectural identity.

### Philosophical interpretation

No Stieglerian, Heideggerian, Ernstian, or Kirschenbaum conclusion is drawn here. The audit is intended to give later philosophical work a mechanism-sensitive object rather than a metaphorically unified `forgetting`.

---

## 8. Revised thesis 4

Recommended README formulation:

> **Technical forgetting is layer- and mechanism-specific.** A retained state can cease to remain usable through physical destruction, missed restoration/refresh, logical invalidation, loss of mapping/interpretive/currentness relations, or failed reconstruction. These events are not equivalent to one another or to temporary unavailability, and lower-layer loss can be masked by relocation, reconstruction, or redundancy.

This formulation survives all five grounded cases while remaining vulnerable to later cases.

---

## 9. Result for the cross-audit ledger

**Thesis 4 result:** `retained with scope + decomposed`.

Rejected strong claims to add to the ledger:

- `physical destruction = logical forgetting`;
- `logical deletion/invalidation = physical erasure`;
- `physical survival = retained current state`;
- `unavailable now = forgotten`;
- `loss of one replica = loss of the object`;
- `all maintenance failures are periodic/deadline failures`.

Required decomposition:

```text
technical forgetting
    -> target layer
    -> failure / invalidation mechanism
    -> retained relation or currentness state
    -> redundancy / reconstruction path
    -> recoverability boundary
```

---

## 10. Next bounded synthesis unit

README thesis 6 remains the only unaudited project-level thesis:

> **More reliable retention can hide more of its maintenance from experience.**

The next audit should not assume a historical law. It should test at least:

- visible human protection/interpretation in positional calculation;
- read–rewrite hidden inside a core memory cycle;
- row-level DRAM sense/restore and refresh infrastructure;
- Flash controller remapping/reclamation/bad-block management;
- RADOS peering/repair/currentness machinery;
- whether `hidden from the user`, `automated`, `reliable`, `labor-saving`, and `infrastructural` are actually the same relation.

Only after thesis 6 is audited should the project decide whether the first bounded thesis-audit sequence is complete enough to begin the named Stiegler / Heidegger / Ernst / Kirschenbaum tests.
