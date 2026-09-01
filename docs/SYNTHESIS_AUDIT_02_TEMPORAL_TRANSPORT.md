# Synthesis Audit 02 — Temporal Transport, Recoverability, and Mechanism

> **Question:** does the provisional thesis `storage is temporal transport` add explanatory power, or does it merely redescribe the fact that retained state is available later?

**Status:** bounded pre-synthesis audit.

This document tests one project thesis against the five grounded retention regimes. It does not promote a universal ontology of storage and does not treat a media-theoretical proposition as historical vocabulary used by the actors in the cases.

Grounded cases used here:

- [`00 — Abacus / reckoning retained position`](../cases/00-abacus-retained-position.md), with [`evidence/00-abacus-rod-line-reckoning-grounding.md`](../evidence/00-abacus-rod-line-reckoning-grounding.md);
- [`02 — Magnetic core destructive read`](../cases/02-magnetic-core-destructive-read.md), with [`evidence/02-magnetic-core-1951-1954-grounding.md`](../evidence/02-magnetic-core-1951-1954-grounding.md);
- [`03 — DRAM scheduled restoration`](../cases/03-dram-refresh-as-scheduled-restoration.md), with [`evidence/03-dram-1967-1982-grounding.md`](../evidence/03-dram-1967-1982-grounding.md);
- [`04 — Mapped Flash logical identity`](../cases/04-flash-virtual-mapping-logical-identity.md), with [`evidence/04-flash-1992-1998-grounding.md`](../evidence/04-flash-1992-1998-grounding.md);
- [`05 — RADOS replica agreement and repair`](../cases/05-rados-replicated-object-repair.md), with [`evidence/05-rados-2006-2007-grounding.md`](../evidence/05-rados-2006-2007-grounding.md).

The mercury delay-line case remains `first-pass` and is deliberately excluded from the formal verdict even though it is an intuitively strong example of a storage/transfer collapse. The audit should not win by choosing the case that already looks most like transmission.

---

## 1. Prior-art anchor: Ernst's proposition is real and stronger than a loose paraphrase

Wolfgang Ernst states the proposition directly in `Archives in Transition: Dynamic Media Memories`, collected in *Digital Memory and the Archive*. On printed p. **100**, after discussing minimal-delay memories and buffers, he argues that storage is a limiting case of transfer and writes that **“storage is a transfer across a temporal distance.”**

Source:

- Wolfgang Ernst, `Archives in Transition: Dynamic Media Memories`, in *Digital Memory and the Archive*, ed. Jussi Parikka, University of Minnesota Press, 2012/2013, p. 100. Publisher record: <https://www.upress.umn.edu/9780816677672/digital-memory-and-the-archive/>.
- Ernst's Humboldt technical-storage notes present the same storage/transfer argument under `Channel time and time channel: Transmission replacing storage?`: <https://www.musikundmedien.hu-berlin.de/de/medienwissenschaft/medientheorien/ernst-in-english/NOTES/PDF/storage-notes.pdf/@@download/file/STORAGE-NOTES.pdf>.

This is **philosophical / media-theoretical prior art** for the repository's thesis. It is not evidence that Cheng Dawei, Forrester, Dennard, Ban, or the Ceph authors understood their systems through this proposition.

The exact claim is also stronger than the harmless observation `stored data are available later`. Ernst is trying to weaken the conceptual opposition between transmission media and storage media. The audit therefore has to test whether that collapse remains informative across mechanisms that do not literally circulate or move during the retention interval.

---

## 2. Verdict

The thesis **survives as a controlled analytical model, but not as a literal mechanism claim or a sufficient definition of storage**.

The strongest defensible form is:

> **Retention can be modeled as a transfer relation across time: a state established at `t0` remains or is reconstructed so that an agreed equivalent is recoverable at `t1`.**

That model is useful because it forces five questions into view:

1. what is established or encoded at `t0`;
2. what interval must be crossed;
3. what disturbances, transformations, maintenance, or replacement are allowed during that interval;
4. what operation recovers the state at `t1`;
5. what criterion makes the recovered state count as the same retained value, object, or current state.

But three stronger readings fail:

```text
storage = literal physical motion through time      → rejected
storage = any causal persistence from t0 to t1      → too broad
storage = fully explained once t0 and t1 are named → rejected
```

The grounded cases show that `temporal transport` does not tell us whether the interval is crossed by quiescence, repeated reconstruction, remapping, replication, protocol agreement, or human interpretation. Those mechanism differences remain exactly what this repository is supposed to preserve.

---

## 3. Three meanings of `transport` must be separated

### 3.1 Physical transport

A physical token or signal moves from one location to another.

This is **not** a universal description of storage. A bead can remain still; a ferrite core can remain in one remanent state; an unchanged Flash cell can retain a state without the represented information physically travelling anywhere during the idle interval.

### 3.2 Material causal continuity

A later physical condition depends causally on an earlier condition.

This is true of retained states, but it is too weak to define storage. Many ordinary physical systems have state and causal continuity. A cooling object, a dent, a weather pattern, or a displaced stone can carry traces of earlier conditions without becoming a storage system in the repository's useful sense.

### 3.3 Recoverability relation across time

A state made actionable at `t0` is still actionable, or can be reconstructed as an agreed equivalent, at `t1`.

This is the useful version for the project. It is relational rather than kinematic:

```text
state / identity at t0
        ↓
retention interval
        ↓
allowed persistence, disturbance, reconstruction, relocation, repair
        ↓
selection / recovery at t1
        ↓
criterion of sameness or currentness
```

`Temporal transport` should therefore be treated as an **engineering/philosophical abstraction over a recoverability relation**, not as a claim that every stored thing literally moves.

---

## 4. Cross-case test

### 4.1 Passive position: temporal transport without physical travel

The grounded abacus / line-reckoning case is the cleanest counterexample to a literal transport reading.

Cheng's instruction to leave the completed numerical configuration unmoved gives the minimal pattern:

```text
t0: operator produces a meaningful positional configuration
interval: the configuration stays in place
 t1: operator reads or continues from that configuration
```

Nothing needs to circulate through the substrate during the interval. What crosses the temporal gap is not a travelling bead but the **availability of an interpreted relation** among counter, position, convention, and procedural role.

The temporal-transfer model adds one useful point: it makes the `t0 → t1` relation explicit and therefore asks what must survive besides the material counter position. The answer includes convention and procedural context.

But it does not explain the mechanism by itself. `Passive positional stability + interpretation` remains the actual retention regime.

**Result:** temporal transport is useful only in the relational sense; literal transport is false here.

### 4.2 Magnetic core: continuity can be quiescent and then reconstructive

Core memory makes the model more interesting because two interval structures coexist.

During quiescence, remanent magnetization can carry the logical distinction from `t0` toward a later access without periodic reconstruction. At the access boundary, however, a classic destructive read may force the core into a known state; the previously represented value remains logically retained only if sensing and rewrite reconstruct it.

Thus the temporal relation can contain a discontinuity in physical embodiment:

```text
remanent state at t0
        ↓
quiescent interval
        ↓
destructive read
        ↓
sensed logical value
        ↓
restored magnetic state
```

If `transport` means one physical token travelling intact, the description fails. If it means preservation of a recoverable logical equivalence relation across time, it works.

**Result:** the model is strongest when it explicitly allows reconstruction and states the sameness criterion.

### 4.3 DRAM: repeated reconstruction is close to relay through time

Grounded DRAM is the strongest support for the metaphor.

The physical charge has a bounded unaided lifetime. Longer logical retention depends on scheduled sense/amplify/restore operations. Over a sufficiently long interval, there need not be one uninterrupted physical charge packet corresponding to the original write.

The state is better pictured as repeatedly re-established:

```text
logical value at t0
    → decaying physical embodiment
    → sense / amplify / restore
    → new physical embodiment
    → ...
    → recovery at t1
```

Here `temporal transport` does explanatory work because it blocks the intuitive mistake that storage requires one untouched physical token. The logical value is carried across the interval by a chain of reconstruction events.

But the phrase still does not tell us **why** reconstruction is scheduled, how often it must occur, how rows are selected, or what failure looks like. Those remain mechanism-specific questions.

**Result:** strongly illuminating, but still not a substitute for refresh mechanics.

### 4.4 Mapped Flash: data, identity, and location can follow different temporal paths

Mapped Flash complicates the model because several things can be `transported` differently.

An unchanged programmed physical state may remain quiescently. Under update or reclamation, however:

- the logical identity remains stable;
- the current physical embodiment can move;
- old embodiments can survive physically after they stop counting logically;
- mapping/allocation metadata determines which embodiment is current.

There is therefore no single temporal trajectory called `the block` unless the layer is named.

A temporal-transfer analysis becomes useful only after separating:

```text
physical cell state
logical value
logical unit identity
mapping relation
currentness
future serviceability
```

The logical object can cross time while its physical location changes, but that statement depends on the mapping relation being retained too.

**Result:** `transport across time` helps expose invariants only if the retained target is specified; otherwise it hides the very identity problem that makes the case valuable.

### 4.5 RADOS: there may be no single path through time at all

RADOS is the strongest challenge to a simple sender → channel → receiver picture.

A replicated object can exist in several physical embodiments. Membership changes, replicas become stale or missing, primary authority moves, peering compares versions/logs, and re-replication creates new embodiments. The 2006 design also separates in-memory replicated acknowledgement from later durable commit.

The retained object therefore need not have one privileged material trajectory from `t0` to `t1`.

What crosses the interval is a **protocol-defined current state** sustained by some changing set of replicas plus metadata and authority rules.

A temporal-transfer model can still be drawn, but it has to look like a relation over a changing distributed state rather than a parcel moving along one channel:

```text
accepted state at t0
        ↓
replication / versioning / map epochs / failures / repair
        ↓
protocol-authorized current state at t1
```

**Result:** the abstraction survives, but only after abandoning the assumption of one carrier, one path, or one continuously privileged copy.

---

## 5. Counterexample ledger

| Candidate claim | Result | Why |
| --- | --- | --- |
| Stored information literally moves through the substrate during the whole retention interval. | **rejected** | passive position, quiescent core remanence, and idle Flash are counterexamples |
| The same physical carrier must survive from `t0` to `t1`. | **rejected** | core restore, DRAM regeneration, Flash relocation, and RADOS repair preserve higher-layer continuity through changed embodiment |
| Any physical causal continuity across time is storage. | **rejected as too broad** | it would turn ordinary stateful physical traces into storage without an operational recoverability criterion |
| Retention can be represented as an input-at-`t0` / recoverable-output-at-`t1` relation. | **supported** | all five grounded cases permit such a relation once the retained target and recovery criterion are specified |
| Storage and transmission are absolutely distinct operation classes. | **qualified / rejected as an absolute** | DRAM reconstruction, remapping, repair, and buffers show that stored state can be sustained through transfer-like operations; however the distinction remains useful at specific mechanism/interface layers |
| Duration alone distinguishes storage from transfer or buffer. | **rejected as sufficient criterion** | the cases add role, addressability, identity, update semantics, recovery threshold, and protocol authority; time interval alone does not classify them |
| Temporal transport explains the mechanism of retention. | **rejected** | it leaves open whether retention is quiescent, deadline-driven, access-triggered, remapped, replicated, or human-interpreted |
| The temporal-transfer model can expose where sameness criteria live. | **supported** | DRAM, Flash, and RADOS especially require logical equivalence/currentness criteria across changed embodiments |

---

## 6. What explanatory work the model actually performs

The phrase is worth keeping only if it changes the questions we ask.

### 6.1 It makes the interval an object of analysis

Instead of asking only `where is the state?`, the model asks:

- what can happen between write and later recovery;
- what disturbances are tolerated;
- what maintenance deadlines exist;
- what transformations preserve identity;
- what events cause the relation to fail.

This is genuinely useful across quiescent and reconstructive systems.

### 6.2 It makes encoding and recovery symmetric enough to compare

A storage case can be written as:

```text
formation / write
        ↓
retention interval
        ↓
selection / read / reconstruction
```

That structure exposes differences that a static noun like `memory` can hide. A core's destructive read, DRAM's scheduled restoration, Flash's map-mediated recovery, and RADOS's currentness checks all sit at different places in the relation.

### 6.3 It permits identity without physical-token continuity

The model can compare systems where the later state is materially different from the earlier one as long as the repository names the equivalence rule.

This is its strongest contribution to the current project.

### 6.4 It invites, but does not automatically justify, a channel/noise formalization

For some future cases, especially ECC, bit rot, archival migration, and probabilistic durability, the interval can be modeled as a noisy channel through time. That can make error rates, redundancy, and reconstruction mathematically comparable.

But the present audit does **not** claim that all five grounded cases have already been formalized in Shannon-theoretic terms, or that information theory supplies their historical actors' own concepts.

---

## 7. Limits: where `temporal transport` becomes too general

### 7.1 It does not distinguish retention mechanisms

Every successful case can be drawn as `t0 → t1`. That is exactly why the abstraction risks becoming vacuous.

The repository should never replace:

- remanence;
- refresh;
- destructive-read restore;
- remapping;
- reclamation;
- replication;
- peering;
- human positional interpretation;

with the single phrase `temporal transport`.

### 7.2 It can hide addressability

A state may survive the interval and still be practically useless if it cannot be selected at `t1`. The next synthesis audit should therefore test addressability separately rather than smuggling retrieval into the word `transport`.

### 7.3 It can hide multiple success thresholds

RADOS demonstrates that `acknowledged`, `replicated`, `current`, and `durably committed` are not one temporal endpoint. A single `t1` may therefore be an oversimplification; systems can expose several retention thresholds.

### 7.4 It can hide interpretation

In the passive-position case, the substrate can survive while convention or procedural meaning is lost. A later physical configuration is not enough. Recovery must be recovery **as a meaningful state**.

### 7.5 It is not historical vocabulary for most cases

`Temporal transport` is a modern engineering/philosophical reconstruction. The project must not retroactively attribute it to historical actors merely because their mechanisms can be modeled this way.

---

## 8. Revised thesis

The original README thesis is too categorical:

> `Storage is temporal transport.`

The grounded evidence supports a more precise formulation:

> **Storage and retention can be analyzed as transfer relations across temporal distance: a state established at `t0` remains or is reconstructed as an agreed recoverable equivalent at `t1`. This does not imply literal physical motion, one persistent carrier, or active maintenance, and it does not by itself distinguish storage mechanisms. The model earns its keep only when it specifies the retained target, interval, admissible transformations, recovery operation, and criterion of sameness/currentness.**

This keeps the Ernstian challenge to a rigid storage/transmission opposition while preventing the proposition from swallowing all mechanism differences.

---

## 9. Consequence for the next synthesis pass

Thesis 2 can now be treated as **audited and revised**, not promoted to a final conclusion.

The next bounded synthesis question should be README thesis 3:

> `Addressability changes what retention can do.`

That audit should compare at least:

- human spatial selection in the grounded abacus/reckoning case;
- coordinate selection in grounded magnetic core;
- row/column and shared sense/restore organization in grounded DRAM;
- logical-to-physical mapping in grounded Flash;
- object → PG → current placement / authority in grounded RADOS.

The central question should be whether `retained` and `retrievable by a chosen operation` are separate properties, and how much of modern storage's apparent power comes from selection machinery rather than from durability alone.
