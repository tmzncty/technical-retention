# Synthesis 09 — Distributed Coded Storage: Read Recovery, Durable Repair, Placement Restoration, and Representation Handoff

## Scope

This is a **bounded cross-case synthesis**, not a new historical case and not a genealogy of erasure coding, Facebook storage, Windows Azure Storage, or OpenStack Swift.

It closes two closely coupled relation-decomposition questions already present in the roadmap:

> In distributed coded storage, how should `coded recoverability`, `read availability`, `full-fragment repair`, and `restored failure-domain placement` be separated?

> In locality-aware coded storage, how should `recoverability`, `reconstruction read-set/cost`, `on-demand read recovery`, `durable fragment repair`, and `redundancy-regime handoff completion` be separated?

The positive comparison is built from two already-grounded production cases:

- [Case 19 — Facebook f4 erasure-coded warm storage](../cases/19-facebook-f4-erasure-coded-failure-domains.md);
- [Case 24 — Windows Azure Storage LRC](../cases/24-windows-azure-lrc-repair-locality-handoff.md).

A third grounded case is used as a **negative/currentness control**, not as evidence that all coded object stores share the same pipeline:

- [Case 25 — OpenStack Swift EC overwrite/currentness](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md).

Historical facts remain owned by those case/evidence records. This document adds a typed **engineering reconstruction (`E`)** and **functional comparison (`A`)** across them. No direct implementation lineage among f4, WAS, and Swift is claimed.

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `erasure coding`, f4, LRC, and related reconstruction terms found no dedicated overlapping case in the current repository search surface. A fuller history of Reed–Solomon deployment, locally repairable codes, declustered placement, cloud-object repair, or Azure/Facebook/OpenStack engineering genealogy should therefore be developed there rather than recreated here if that history becomes a project priority.

---

## Primary-source anchors

The bounded historical records used here are already grounded in the individual evidence files. The principal primary sources are:

- Subramanian Muralidhar et al., **“f4: Facebook’s Warm BLOB Storage System,”** OSDI 2014, USENIX Association: <https://www.usenix.org/conference/osdi14/technical-sessions/presentation/muralidhar>.
- Cheng Huang et al., **“Erasure Coding in Windows Azure Storage,”** USENIX ATC 2012: <https://www.usenix.org/conference/atc12/technical-sessions/presentation/huang>.
- OpenStack Swift 2.10.1, **“Erasure Code Support”** documentation: <https://files.openstack.org/docs/swift/2.10.1/overview_erasure_code.html>.

These sources do not license a shared vocabulary stronger than their actual system descriptions. In particular, f4 explicitly treats erasure codes as tools rather than claiming coding-theory priority; the WAS paper situates LRC against earlier coding work; Swift documents its own mutable-object commit/currentness protocol rather than a universal EC rule.

---

## Historical records kept separate

### Facebook f4, 2014 — request-scoped reconstruction, full-block rebuild, and placement balancing are three different operations

The f4 paper describes immutable warm BLOBs stored in erasure-coded cells. A normal read reaches the target data block directly. When that block is unavailable, a backoff node can obtain the corresponding ranges from companion/parity blocks and reconstruct **only the requested BLOB range**. That foreground path is deliberately narrower than full repair.

A rebuilder node handles the later heavyweight operation: reconstructing an entire missing block and writing a replacement. The coordinator separately runs a placement balancer because failure, reconstruction, and replacement can leave multiple blocks from one stripe in the same failure domain even after the missing content has been recreated.

The historical sequence therefore permits at least three distinct completion conditions:

```text
request can be answered by decoding
    ≠
missing full block has been durably rebuilt
    ≠
stripe placement again satisfies the intended failure-domain geometry
```

The last relation matters because the same set of surviving/rebuilt coded fragments can expose different correlated-failure risk depending on where those fragments reside.

### Windows Azure Storage, 2012 — a smaller reconstruction dependency set is not a complete repair state

The WAS paper defines `reconstruction cost` in terms of how many fragments must be read to recover an unavailable fragment. Production `LRC (12, 2, 2)` lowers the source read set for a common single-fragment reconstruction relative to the compared Reed–Solomon design while retaining similar normalized storage overhead.

The paper then separates two uses of essentially the same decoding capability. For an unavailable or hot fragment, another Extent Node can reconstruct the requested fragment, cache it, and return data to the client. If the original fragment remains unavailable for an extended period, the Stream Manager initiates reconstruction on another Extent Node and the result is **written to disk**.

Thus the production source itself blocks the shortcut:

```text
successful on-demand reconstruction
    ≠
durable fragment replacement
```

Those are different service and maintenance milestones.

### WAS, 2012 — code locality and physical/administrative topology are different relations

WAS also separates code dependency from placement. The paper distinguishes hardware-correlated **fault domains** from planned **upgrade domains** and uses placement policy to spread fragments accordingly. `Local` in LRC therefore names a smaller coding dependency/read set; it does not mean that the needed fragments are physically co-located or that network topology disappears.

This gives a second non-equivalence:

```text
small reconstruction dependency set
    ≠
physical locality
    ≠
independent failure-domain placement
```

### WAS, 2012 — changing redundancy regimes requires retained transition state and a completion gate

Sealed WAS extents begin with three full replicas and are erasure-coded asynchronously. The encoding coordinator persists conversion progress so another node can resume after interruption. The new coded state is checked through decoding/CRC validation, fragment boundaries and completion flags are recorded, and only after the documented handoff sequence are the old full replicas scheduled for deletion. If validation fails, the conversion is aborted and the full copies remain.

This is a representation-handoff problem, not merely a code-selection problem:

```text
old replicated representation
    -> target coded fragments partly produced
    -> retained conversion progress
    -> validation
    -> completion/admissibility metadata
    -> old full replicas become retirement candidates
```

The project term `redundancy-regime handoff` is an engineering reconstruction. It is not historical WAS vocabulary.

### Swift, 2015–2016 — mathematical sufficiency can still fail the currentness/admissibility test

Swift is included mainly to stop the f4/WAS comparison from becoming a universal model for mutable coded objects. In Swift 2.10.1, a successful GET requires enough **distinct fragment indexes at the same timestamp** plus a matching durability indication. Newer fragment bytes may physically exist before the corresponding object version has crossed the documented commit boundary, while an older timestamp can remain protected from deletion.

Therefore even before asking about foreground recovery versus durable repair, a mutable EC system may need another qualification layer:

> `enough mathematically complementary fragments exist` ≠ `this is the current committed coded version the service is allowed to return or repair`.

This is why the separate roadmap question for mutable erasure-coded currentness remains open rather than being marked complete by this synthesis.

---

## Engineering reconstruction: eight typed relations

The terms below are project engineering vocabulary. They are not attributed as shared terminology to the historical systems.

### 1. Coded-state admissibility / currentness

Which fragment set is allowed to count as one current retained object?

For immutable f4/WAS slices this qualification is comparatively simple once the intended representation is established. Swift shows why mutable coded storage can require version/timestamp and commit evidence before decoding inputs become service-admissible.

### 2. Algebraic recoverability

Does a sufficient compatible subset of coded contributions exist to reconstruct the missing data under the code?

This is a mathematical relation among fragments. It does not specify whether the needed fragments are cheap to read, where they are placed, whether the current request is already served, or whether a replacement embodiment has been written.

### 3. Reconstruction dependency / read-set geometry

How many and which source fragments must be read to exercise recoverability?

WAS LRC makes this a first-class production design concern. Two codes can have similar storage overhead and both be recoverable while imposing different I/O/network work for the common repair path.

### 4. Foreground request recovery

Can the system satisfy the current read without first restoring the missing durable embodiment?

f4 reconstructs the requested BLOB subrange; WAS can reconstruct/cache an unavailable fragment for the client path. This is a **service** relation with a request-scoped completion condition.

### 5. Durable fragment/block repair

Has the missing coded contribution been re-materialized as durable managed storage?

f4 background rebuild reconstructs the full missing block. WAS long-unavailability reconstruction writes a replacement fragment to disk. This is stronger than one successful reconstructed read.

### 6. Failure-domain placement restoration

After durable content repair, are the rebuilt fragments again distributed according to the intended correlated-failure geometry?

f4 supplies a direct counterexample: reconstruction/replacement can leave a placement violation, and the coordinator's placement balancer performs another maintenance action. Durably reconstructed bytes are therefore not automatically restored topology.

### 7. Representation-handoff completion

When a system changes redundancy regimes, has the target representation crossed the implementation's validation/currentness gate so that the old representation can be retired?

WAS makes this explicit with persisted encoding progress, CRC/decoding validation, metadata/completion flags, and later source-replica deletion. Handoff state is constitutive retention infrastructure even though it is not client payload.

### 8. Source-representation retirement / convergence

Have old replicas, stale locations, temporary caches, or transitional embodiments actually been retired after the new relation becomes admissible?

Authorization to delete and completed cleanup are separate events. This synthesis treats retirement as a convergence question rather than assuming it occurs at the exact instant of validation or repair.

---

## Compact relation map

```text
candidate coded fragments
        ↓
currentness / representation admissibility
        ↓
algebraic reconstructability
        ↓
reconstruction dependency/read-set geometry
        ↓
┌─────────────────────────────┬───────────────────────────────┐
│ foreground request recovery │ durable fragment/block repair │
└─────────────────────────────┴───────────────────────────────┘
                                  ↓
                      failure-domain placement restored
                                  ↓
                    ordinary redundancy geometry recovered
```

A representation transition adds a different axis:

```text
old representation still retained
        ↓
target representation production
        ↓
retained transition progress
        ↓
validation / completion evidence
        ↓
target representation becomes admissible
        ↓
old representation becomes retireable
        ↓
retirement / cleanup convergence
```

These are diagnostic decompositions, not one universal implementation pipeline. Systems can combine, omit, reorder, or add relations.

---

## Cross-case matrix

| Relation | Facebook f4, 2014 | Windows Azure Storage LRC, 2012 | Swift EC, 2015–2016 boundary |
| --- | --- | --- | --- |
| object mutation regime in bounded case | immutable warm BLOB | sealed immutable extent during coding | mutable PUT/overwrite |
| algebraic recovery relation | RS within cell; geo XOR at another layer | LRC data/local/global parity | EC fragments, but only compatible version/index cohorts count |
| repair-read geometry | request subrange can be decoded from companion/parity ranges | LRC reduces common reconstruction source set | decode threshold is subordinate to same-timestamp/distinct-index/currentness rules |
| foreground recovery | backoff reconstructs requested BLOB range | EN reconstructs/caches requested fragment for client | proxy reconstructs an admissible timestamp cohort |
| durable repair | rebuilder reconstructs full block | Stream Manager reconstruction writes fragment to disk | reconstructor repairs missing fragment archives |
| placement relation | rack/node placement; later placement balancer | fault-domain and upgrade-domain placement are distinct from LRC locality | ring primaries/handoffs; not used here to close a placement-history claim |
| representation handoff | not the canonical mechanism of this slice | three replicas → async LRC production → validation/completion → replica retirement | new timestamp fragments → commit/durable state before old timestamp retirement |
| strongest methodological use here | content repair ≠ topology restoration | repair cost ≠ service recovery ≠ durable repair; transition gate | algebraic sufficiency ≠ current committed version |

The table is an `A/E` comparison. Similar rows do not establish direct technological descent.

---

## Cross-case findings

### E — coded recoverability ≠ request-time read availability

A code can in principle reconstruct missing data while the service still needs mapping, source selection, network reads, decoding capacity, and a live foreground recovery path. Conversely, one successful request says only that this path succeeded for that demand.

### E — request-time reconstruction ≠ durable fragment repair

f4 and WAS independently expose this boundary in production descriptions. A reconstructed response/cache can satisfy the current request while the intended durable coded contribution is still absent.

### E — durable fragment repair ≠ restored failure-domain placement

f4 provides the decisive counterexample: a reconstructed/replaced block can exist while stripe members remain badly concentrated in one failure domain. Placement balancing is a later obligation.

### E — reconstruction read-set/cost ≠ code strength

LRC changes how much distributed state must commonly be read to reconstruct a missing fragment. This is not the same property as the full set of failure patterns the code can tolerate; the WAS paper explicitly notes its LRC is not MDS.

### E — coding locality ≠ physical locality

A small dependency group is a relation in the code. Physical rack/fault/upgrade placement remains a separate system-design relation and can deliberately spread those contributors apart.

### E — similar storage overhead ≠ similar repair work

The production WAS comparison demonstrates that storage overhead can remain similar while reconstruction I/O/network dependency changes materially. Capacity efficiency therefore does not determine maintenance cost by itself.

### E — transition progress state ≠ target payload fragments

During WAS asynchronous conversion, progress state lets work resume after interruption. It is neither the old full-replica payload nor simply another final LRC fragment; it is retention infrastructure for completing the representation change.

### E — target fragments present ≠ representation handoff complete

Partially produced coded bytes do not authorize retirement of the old full replicas. Validation and completion metadata gate the handoff. The same general warning is strengthened, under different protocol semantics, by Swift's newer-fragment-without-durability counterexample.

### E — handoff completion ≠ physical cleanup completion

A system can reach the point at which old replicas are *eligible* to be deleted before every obsolete embodiment has actually been reclaimed. Authority to retire and completed retirement are different milestones.

### E — service recovery ≠ topology convergence

A system may already answer reads and may even have re-materialized a missing fragment while still owing placement balancing, handoff reversion, or other convergence work that restores the intended correlated-failure margin.

### E — mutable coded currentness is an additional axis, not an automatic extension of immutable repair

Swift shows that fragment presence plus coding algebra can be insufficient when multiple timestamps coexist. This synthesis therefore does not close the separate mutable-EC roadmap question.

---

## Relationship to Syntheses 07 and 08

[Synthesis 07](SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md) establishes the broader recovery pipeline from failure/currentness evidence through mathematical reconstructability, repair scope, reconstruction geometry, restored redundancy, and later verification.

This document cuts **sideways through distributed production semantics** that Synthesis 07 deliberately left abstract:

- one-request reconstruction versus durable full-fragment repair;
- repair dependency/read-set cost versus code strength;
- durable content repair versus failure-domain placement restoration;
- target representation production versus validated redundancy-regime handoff.

[Synthesis 08](SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md) asks how a physically present embodiment becomes disqualified through integrity verification. Synthesis 09 instead assumes that a missing/unavailable/transitioning coded relation is already known and asks which service, repair, placement, and handoff milestones follow.

The seams are intentional; they prevent `recovered`, `repaired`, and `durable` from becoming all-purpose status words.

---

## Prior-art and genealogy boundary

Nothing here establishes that:

- f4 invented Reed–Solomon or distributed erasure coding;
- WAS invented the general idea that coding can trade storage overhead for repair/access work;
- LRC `locality` implies physical co-location;
- Facebook f4, WAS LRC, and Swift EC form one direct implementation lineage;
- request-scoped decoding historically evolved into full repair in one necessary sequence;
- all coded storage systems require a separate placement-balancer stage;
- all systems transitioning from replication to EC use WAS-style completion flags;
- mutable object-store currentness can be inferred from immutable f4/WAS semantics.

The repository uses these cases only because their differences make the retention relations easier to separate.

---

## Why this matters for technical retention

Erasure coding can tempt a description in which the retained object is reduced to an algebraic fact: if enough fragments survive, the object survives. The production cases show why that is incomplete.

A usable retained object can additionally depend on:

- which coded version is current;
- how much source state must be touched to exercise recovery;
- whether current demand can be served before durable repair;
- whether a new fragment has actually been written;
- whether repaired fragments again occupy independent failure domains;
- whether a new redundancy representation has crossed its validation gate;
- whether the old representation has actually been retired.

Thus `the object survives` can name several different future possibilities. Technical retention becomes more precise when those possibilities are kept as separate relations rather than collapsed into one durability bit.

---

## Philosophical boundary

A philosophical interpretation may note that logical continuity survives replacement, that availability can precede restoration, or that a small amount of mapping/control state governs the status of much larger payloads. None of those observations turns coding equations, placement maps, completion flags, or `.durable` markers into a philosophical category by themselves.

This synthesis therefore makes no new Stiegler, Heidegger, Ernst, or Kirschenbaum claim. Its contribution is engineering discipline that later philosophical interpretation must respect.

---

## What remains open

This bounded closure does **not** finish distributed coded-storage history. High-value next slices include:

- the separate mutable-EC question: fragment presence, version/timestamp coherence, coded reconstructability, commit/durability evidence, old-version retirement, and repair convergence;
- integrity-qualified coded repair where checksum metadata itself may be suspect;
- exact production measurements of repair bandwidth, tail latency, throttling, and concurrent-failure exposure;
- placement under correlated rack/zone/datacenter failures beyond the three bounded systems here;
- modern locality/regenerating-code genealogy and its production adoption;
- controller/network fault injection showing how partial handoff and repair states fail in practice;
- broader erasure-coding history in `computing-archaeology` rather than duplicated here.

Those are additional research slices, not blockers for the two bounded relation-decomposition questions closed here.
