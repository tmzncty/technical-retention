# Cross-Audit Counterexample Ledger

> **Purpose:** record what the bounded synthesis audits have actually rejected, narrowed, decomposed, or retained before any provisional thesis is promoted to a conclusion.

**Status:** bounded synthesis control document.

This ledger does not add a new historical case. It consolidates the results of:

- [`SYNTHESIS_AUDIT_01_MAINTAINED_PERSISTENCE.md`](SYNTHESIS_AUDIT_01_MAINTAINED_PERSISTENCE.md);
- [`SYNTHESIS_AUDIT_02_TEMPORAL_TRANSPORT.md`](SYNTHESIS_AUDIT_02_TEMPORAL_TRANSPORT.md);
- [`SYNTHESIS_AUDIT_03_ADDRESSABILITY.md`](SYNTHESIS_AUDIT_03_ADDRESSABILITY.md);
- [`SYNTHESIS_AUDIT_04_PRIVILEGED_LOCATION.md`](SYNTHESIS_AUDIT_04_PRIVILEGED_LOCATION.md);
- [`SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md`](SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md).

The formal evidence base remains the five `grounded` cases in [`CASE_INDEX.md`](../CASE_INDEX.md): passive positional reckoning, magnetic core, DRAM, mapped Flash, and 2006–2007 RADOS. The mercury delay-line case remains `first-pass` and is not silently promoted here.

This document is therefore a **cross-case engineering / methodological synthesis**. It does not turn the repository's analytical vocabulary into historical actors' vocabulary, and it does not yet constitute a philosophical conclusion.

---

## 1. Status vocabulary

The ledger uses the following result labels.

| Result | Meaning |
| --- | --- |
| **rejected** | a stronger claim has direct counterexamples in the grounded cases |
| **narrowed** | the original intuition survives only with explicit scope conditions |
| **decomposed** | one apparent property has to be split into several relations or stages |
| **retained with scope** | useful as a bounded analytical model, but not a universal definition or historical law |
| **untested** | not yet subjected to a dedicated bounded audit |

`Audited` does **not** mean `final`. A claim can survive an audit and still fail against later cases, better sources, or philosophical prior art.

---

## 2. README thesis ledger

| README thesis | Audit state | Result | What survives | What must not be claimed |
| --- | --- | --- | --- | --- |
| **1. Persistence is often an achieved relation, not a maintenance-free property.** | audited in 01 | **narrowed + decomposed** | useful persistence may depend on quiescent stability, scheduled reconstruction, access-triggered restore, remapping/reclamation, repair, or human/procedural maintenance; the maintenance target and trigger must be named | `persistence = continuous activity`; `nonvolatile = maintenance-free`; one active/passive label classifies a whole technology |
| **2. Storage can be analyzed as transfer across temporal distance, but only as a recoverability model.** | audited in 02 | **retained with scope** | a state established at `t0` can remain or be reconstructed as an agreed recoverable equivalent at `t1`; the model is useful when it names the retained target, interval, allowed transformations, recovery operation, and sameness/currentness rule | literal physical motion is universal; one carrier must persist; any causal continuity is storage; `temporal transport` explains the mechanism by itself |
| **3. Addressability is a separate operational relation layered onto retention.** | audited in 03 | **retained with scope + decomposed** | designation, selection/resolution, currentness/admissibility, and read/recovery can be distinct stages; stable designation can survive physical relocation | retention requires a machine-readable address; address equals location; resolution proves currentness; addressability equals availability; addressability is one historical scalar |
| **4. Technical forgetting is layer- and mechanism-specific.** | audited in 05 | **retained with scope + decomposed** | forgetting claims must name a target layer and distinguish physical destruction, missed maintenance, logical invalidation/deauthorization, relation/currentness loss, and service/recoverability loss; redundancy or reconstruction can mask lower-layer destruction | physical destruction always means logical forgetting; logical invalidation means physical erasure; physical survival proves current logical retention; temporary unavailability means forgotten; one replica loss means object loss |
| **5. Logical persistence can become detached from any one permanent physical home without becoming placeless.** | audited in 04 | **narrowed + decomposed** | some layers allow identity to survive replacement of microscopic state, then replacement of a physical home, then replacement of replica membership; retained mapping/placement/currentness relations become constitutive | logical persistence is always location-independent; reconstruction at one cell is relocation; mapping makes state immaterial; replication eliminates authority; history is a monotonic ascent toward placelessness |
| **6. More reliable retention can hide more of its maintenance from experience.** | not yet audited | **untested** | audits 01, 04, and 05 supply candidate mechanisms for hidden work, but no dedicated evidence-led test has yet separated reliability, interface invisibility, automation, labor, and infrastructure | do not treat `more reliable -> more hidden labor` as an established historical law |

The immediate discipline is simple:

> **No README thesis is a final conclusion yet. Five have survived only in revised form; thesis 6 remains unaudited.**

---

## 3. Rejected strong claims across the audits

The same overgeneralizations recur under different language. Keeping them in one place should prevent later synthesis from reintroducing claims that individual audits already rejected.

| Rejected strong claim | Counterexample / reason | Origin |
| --- | --- | --- |
| every persistent state requires continuous active maintenance | passive positional state, quiescent core remanence, and idle Flash remain without periodic regeneration merely to stay present | Audit 01 |
| nonvolatile means maintenance-free | core access can create restore work; mapped Flash serviceability depends on mapping/reclamation and later wear/failure handling | Audit 01 |
| maintenance must be periodic to be constitutive | core restore is access-triggered; Flash maintenance can be workload/capacity/wear-triggered; RADOS repair is failure/membership-triggered | Audit 01 |
| hidden retention work is necessarily automated | positional calculation depends on human protection, selection, interpretation, and procedural continuity | Audit 01 |
| stored information literally moves during the whole retention interval | bead position, quiescent core, and idle Flash are direct counterexamples | Audit 02 |
| the same physical carrier must persist from `t0` to `t1` | core restore, DRAM regeneration, Flash relocation, and RADOS repair preserve higher-layer continuity through changed embodiments | Audit 02 |
| any causal physical persistence is storage | this would make ordinary traces and stateful objects storage without an operational recoverability criterion | Audit 02 |
| temporal transport explains the retention mechanism | the model leaves open quiescence, refresh, destructive-read restore, remapping, replication, repair, and interpretation | Audit 02 |
| a retained state must have a machine-readable address | grounded positional working state can be selected by a trained human without an address bus or decoder | Audit 03 |
| address is simply physical location | mapped Flash and RADOS resolve stable logical identities through retained mapping/placement relations | Audit 03 |
| resolving a reachable embodiment proves it is current | stale Flash embodiments and RADOS stale/unauthorized replicas can remain physically readable | Audit 03 |
| addressability and availability are the same property | designation can succeed while mapping/currentness, interpretation, interface, key, or readable embodiment is missing | Audit 03 |
| logical persistence is always independent of location | positional reckoning makes location constitutive; bounded core and DRAM keep stable selected physical homes | Audit 04 |
| physical-state reconstruction already means the logical object moved | core rewrite and DRAM restoration recreate state at the same selected home | Audit 04 |
| remapping or replication makes retained state immaterial | every current embodiment remains material; mapping/placement state only changes which embodiment counts | Audit 04 |
| distributed replication eliminates privileged authority | RADOS removes a permanent physical home while retaining temporary protocol authority and currentness rules | Audit 04 |
| later systems are monotonically more placeless | fixed cells, stable addresses, remapped blocks, and distributed replicas coexist in modern stacks | Audit 04 |
| physical destruction always means logical forgetting | DRAM reconstruction, Flash reclamation/relocation, and RADOS replica replacement can destroy or abandon one embodiment while preserving the higher-level state | Audit 05 |
| physical survival proves retained current state | positional state can lose interpretation; Flash and RADOS can preserve stale/invalid physical embodiments that no longer count as current | Audit 05 |
| logical deletion or invalidation is physical erasure | mapped Flash explicitly separates `deleted`/`dirty` status from later erase-unit clean-up | Audit 05 |
| temporary unavailability is forgetting | a surviving state can be unreachable, unselectable, or not yet admissible and later return to service | Audit 05 |
| one replica loss means object loss | RADOS can turn member loss into peering/re-replication while the object remains retained | Audit 05 |
| all maintenance failures have one temporal form | classic core restore is access-triggered, DRAM refresh deadline-triggered, RADOS repair failure-triggered, and positional interpretation/protection procedural | Audit 05 |

These are not minor wording preferences. They are **negative results** that later writing must preserve.

---

## 4. Decompositions that now constrain the vocabulary

The audits repeatedly show that one noun often hides several technically distinct relations.

### 4.1 `Persistence`

At minimum, distinguish:

- survival of a physical distinction;
- logical value across physical reconstruction;
- logical identity across relocation;
- currentness / authority among multiple embodiments;
- serviceability under future writes;
- interpretability / procedural availability;
- durable commit threshold.

A statement such as `the data persist` is incomplete until the layer is named.

### 4.2 `Maintenance`

Current grounded cases support different trigger structures:

- quiescent interval with no recurring restore merely to remain;
- deadline-driven regeneration;
- access-triggered restoration;
- workload / capacity-triggered reclamation;
- wear / lifetime-triggered placement;
- failure / membership-triggered repair;
- interpretive / procedural maintenance.

These are overlapping obligations, not a mutually exclusive technology taxonomy.

### 4.3 `Temporal transport`

Separate:

- literal physical transport;
- generic causal continuity;
- recoverability relation across time.

Only the third is currently retained as a useful project-level model, and even it does not replace mechanism reconstruction.

### 4.4 `Addressability`

Separate:

1. designation / identity;
2. selection or resolution;
3. candidate embodiment(s);
4. currentness / admissibility where required;
5. read / reconstruction / interpretation.

A stable logical designation may coexist with changing physical location and changing temporary authority.

### 4.5 `Location continuity`

Separate:

- continuity of one microscopic physical token;
- continuity of one selected physical home;
- continuity of a logical designation;
- continuity of mapping / placement relation;
- continuity of currentness / protocol authority.

DRAM is the crucial middle counterexample: microscopic electrical state is repeatedly rebuilt while the selected physical home remains stable.

### 4.6 `Technical forgetting`

A forgetting statement should identify:

1. **target layer** — physical distinction, logical value/identity, relation/currentness, serviceability, history, or durable threshold;
2. **mechanism** — disturbance/destruction, missed maintenance, logical invalidation/deauthorization, relation/metadata loss, or failed reconstruction;
3. **masking condition** — whether another current embodiment or reconstruction path preserves the higher-level state;
4. **recoverability boundary** — temporary unavailability, stale/obsolete residue, logical deletion, or actual loss of recoverable current state.

This is intentionally narrower than a complete taxonomy of archival or institutional forgetting.

---

## 5. Cross-audit patterns that are useful but are **not conclusions yet**

The following patterns recur in more than one audit. They should guide the next research slices, but this ledger deliberately stops short of elevating them into final theses.

### Pattern A — the retained object can expand beyond the visible value

A usable retained state may include more than the apparent payload:

```text
positional state
    = physical configuration + convention + procedure

mapped state
    = value + logical identity + mapping/allocation relation

distributed state
    = value + object identity + placement + version/currentness relation
```

This is a **functional comparison**, not a genealogy from abacus to object storage.

### Pattern B — stable interfaces can hide discontinuity below them

Logical continuity may survive:

- destructive read and rewrite;
- scheduled regeneration;
- block relocation;
- replica loss and replacement.

But the kind of discontinuity matters. Recreating charge in the same DRAM cell is not the same operation as remapping a Flash logical unit to another block or replacing a RADOS replica.

### Pattern C — abstraction can create new retention dependencies

When a higher-level identity stops depending on one permanent physical home, it becomes more dependent on retained or reconstructible relations that identify which embodiment is current.

This does **not** imply that later systems are less physical. It changes where the invariants live.

### Pattern D — operational availability is a path, not a synonym for survival

A useful state may require successful passage through:

```text
physical / logical survival
        +
designation
        +
selection / resolution
        +
currentness / admissibility
        +
read / reconstruction / interpretation
```

Failure at any stage can make a surviving trace operationally unavailable.

### Pattern E — state retention and history retention remain distinct

None of the grounded cases automatically preserves a complete history of the operations that produced the current state. PG logs, stale Flash embodiments, forensic residue, or procedural traces may preserve some history, but current-state retention does not by itself entail historical record retention.

### Pattern F — destruction and forgetting can move in opposite directions across layers

A lower-level embodiment can be destroyed while the logical state is preserved by reconstruction, relocation, or redundancy. Conversely, a physical trace can survive after it has lost logical identity, currentness, or interpretation.

This is the strongest cross-audit reason not to define technical forgetting at only one physical or semantic layer.

---

## 6. What remains deliberately unresolved

This ledger does not answer:

- whether `technical retention` is one coherent operation or a family resemblance;
- whether Stieglerian tertiary retention properly covers transient machine-operational state;
- whether Heideggerian availability is materially clarified by the addressability/currentness decomposition;
- how Ernst's microtemporality should be balanced against long quiescent intervals and preservation regimes;
- how Kirschenbaum's forensic materiality changes when old physical embodiments remain after logical invalidation or when replicas and mappings move;
- whether reliable retention systematically makes maintenance less visible;
- how key destruction, media/format obsolescence, institutional abandonment, bit rot, and several controller-level failure modes should extend the bounded forgetting taxonomy.

Those remain later tests, not omissions to fill with assertion.

---

## 7. Next bounded synthesis unit

With technical forgetting audited, README thesis 6 is the only project-level thesis without a dedicated bounded test:

> **More reliable retention can hide more of its maintenance from experience.**

The five grounded cases already supply a useful contrast, but the audit must separate several relations that are easy to collapse:

- visible human protection, interpretation, and reset in positional calculation;
- read–rewrite hidden inside a core memory cycle;
- row-level DRAM sense/restore and refresh infrastructure;
- Flash controller remapping, reclamation, wear management, and bad-block replacement;
- RADOS peering, currentness, repair, and commit machinery;
- `hidden from the user` versus `automated` versus `reliable` versus `labor-saving` versus `infrastructural`.

The goal should be to test whether there is a bounded relation between interface-level apparent stability and displaced maintenance work, **not** to announce a historical law that later storage is automatically more reliable because its labor is more hidden.

Only after that test should the project decide whether the first bounded thesis-audit sequence is complete enough to begin the named Stiegler / Heidegger / Ernst / Kirschenbaum tests.
