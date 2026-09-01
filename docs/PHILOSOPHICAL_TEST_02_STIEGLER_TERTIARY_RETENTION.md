# Philosophical Test 02 — Bernard Stiegler: Tertiary Retention and the Boundary of Machine State

> **Bounded question:** when does a technically retained state illuminate Bernard Stiegler's `tertiary retention`, and where does treating every retained bit, bead, map entry, or replica state as tertiary retention collapse distinctions that the concept is meant to make?

**Status:** bounded philosophical/prior-art test against four `grounded` retention regimes: passive positional working state, DRAM, mapped Flash, and RADOS.

This document does **not** add a historical case and does not attribute Stiegler's vocabulary to Cheng Dawei, Dennard, Ban/M-Systems, or Ceph/RADOS engineers. The technical facts come from the already grounded case files. The new work here is a source-controlled philosophical boundary test.

---

## 1. Why this test is necessary

`technical-retention` deliberately uses a broader research category than ordinary `memory` or `storage`: any actionable state that outlives the operation which produced it may be worth comparing, provided the mechanism and claim layer are explicit.

That breadth creates a predictable danger when the repository meets Stiegler.

Two shortcuts are tempting:

1. **too narrow:** tertiary retention means only durable, human-readable archives such as books, photographs, or records;
2. **too broad:** every non-biological state retained by a technical device is therefore a tertiary retention.

The primary Stiegler sources reject the first shortcut, while the grounded engineering cases show why the second is analytically destructive.

The test therefore asks a narrower question:

> **What additional relation must be specified before a case of technical retention can be used as a case of tertiary retention?**

---

## 2. Claim-layer boundary

This test keeps four layers separate.

1. **Historical record (`H/P`)** — the case studies establish the period mechanisms and vocabularies: positional calculation, capacitor regeneration, Flash mapping, and RADOS placement/version/repair.
2. **Engineering reconstruction (`E`)** — the repository compares what state is retained, how it is selected, how identity survives reconstruction or relocation, and what maintenance is required.
3. **Stieglerian prior art (`I/P`)** — Stiegler develops tertiary retention through exteriorization, mnemotechnics, technical supports, grammatization, intergenerational memory, and the relation between technical traces and psychic/collective individuation.
4. **Project interpretation (`I`)** — this document tests how far that conceptual apparatus can travel across machine-operational states without becoming a synonym for `technical state that lasts for a while`.

No philosophical fit changes a case's evidence maturity.

---

## 3. Primary Stiegler anchors used here

### 3.1 Tertiary retention is not merely a durable container

In *For a New Critique of Political Economy* (2010), translated by Daniel Ross, Stiegler defines tertiary retention through the **mnemotechnical exteriorization** of secondary retention and then immediately broadens the frame: technical objects function as intergenerational supports of memory and material culture, conditioning learning and mnemonic activity.

The relevant passage is in the Introduction, printed pp. **8–10**. Stiegler also treats writing, numeration, and later the reproducibility of gesture as transformations of the mnemotechnical retentional layer.

Primary source:

- Bernard Stiegler, *For a New Critique of Political Economy*, trans. Daniel Ross, Polity, 2010, Introduction, printed pp. 8–10. Publicly accessible scan used for page verification: <https://www.radicalimagination.institute/wp-content/uploads/2023/10/Bernard-Stiegler-For-a-New-Critique-of-Political-Economy-Polity-2010.pdf>.

This matters because `tertiary retention = permanent document` is already too narrow. Stiegler's argument includes technical objects, learned gestures, numeration, and technical materialization more broadly.

### 3.2 A silicon memory chip can be a support, but the support is not the whole concept

In **"Die Aufklärung in the Age of Philosophical Engineering"** (2012), Stiegler describes grammatization as technical processes that discretize and reproduce behavioural flows through which human experience is expressed or imprinted. When discussing the spatialization/materialization of temporal flows, he explicitly lists a **silicon memory chip** among possible supports.

He then says that a retention emerging from a temporal flow can become tertiary through technical materialization onto a support that is neither cerebral nor psychical.

Primary source:

- Bernard Stiegler, **"Die Aufklärung in the Age of Philosophical Engineering,"** *Computational Culture* 2, 28 September 2012: <https://computationalculture.net/die-aufklarung-in-the-age-of-philosophical-engineering/>.

This is important for the repository in two directions:

- volatile or electronically mediated storage is not excluded simply because it lacks the durability of paper;
- nevertheless, the philosophical description concerns a materialized **retentional/behavioural flow**, not the semiconductor mechanism in abstraction from what relation it is serving.

### 3.3 Direct human legibility is not a necessary test

The same 2012 text treats databases and metadata among the changing technical supports of archived traces and digital tertiary retention. Therefore a criterion such as `an unaided human must be able to read the substrate directly` would be too restrictive.

Machine mediation, indexing, encoding, software interpretation, and automatic operations can all belong to a tertiary-retentional system.

But that still does not imply:

> `machine-readable = tertiary retention`.

A controller-internal table and a database of cultural records can both be machine-readable while playing very different roles in exteriorization and transmission.

### 3.4 Dormancy and efficacy must be separated

Stiegler's 2012 text later gives a particularly useful limit: tertiary retention can remain **"dead"** when it does not transform the secondary retentions of a psychical individual affected by it. The surrounding argument is about projection, re-interiorization, education, and the constitution of psychic/social circuits.

This does **not** mean a dormant inscription ceases physically to exist or ceases to be a technical support. It means that its retentional efficacy cannot be reduced to the fact that a substrate continues to hold a distinction.

That distinction maps well onto the repository's mechanism-first method:

```text
physical survival of a state
        !=
its role in a circuit of memory, learning, repetition, or transmission
```

### 3.5 A useful scholarly boundary reading

A later scholarly discussion of Stiegler's general organology emphasizes that technical memory is inscribed in artefacts and that tools can retain know-how, but also stresses the importance of practice, apprenticeship, ritual, and pedagogy in activating such supports.

Secondary source:

- Marco Pavanini, **"Multistability and Derrida's Différance: Investigating the Relations Between Postphenomenology and Stiegler's General Organology,"** *Philosophy & Technology* 35, article 1 (2022), published 24 January 2022: <https://link.springer.com/article/10.1007/s13347-022-00501-x>.

This source is used as **scholarly interpretation**, not as a substitute for Stiegler's own wording.

---

## 4. The proposition to test

A defensible Stieglerian proposition is:

> **Technical exteriorization can retain and transform experience, memory, know-how, and behavioural forms beyond the nervous system, thereby conditioning later perception, learning, repetition, and collective transmission.**

The overextended version would be:

> **Any state physically retained by a technical system is a tertiary retention merely because it persists outside a brain.**

The second proposition is too coarse for this repository.

The distinction is not between `old cultural media` and `new computer memory`. It is between:

- a **retention mechanism**;
- a **technical support**;
- a **retained token/state**;
- and a **retentional function or relation** in which that state participates.

Those can coincide, but they need not.

---

## 5. Cross-case test

| Case | What the grounded technical case establishes | Strong Stieglerian relevance | Boundary / counterexample |
| --- | --- | --- | --- |
| Abacus / line reckoning | an actionable numerical state can remain materially exteriorized in bead/counter position + convention + procedural role; Cheng 1592 explicitly instructs leaving a completed result unmoved | the device and learned positional practice are strong examples of technics carrying operational know-how across people and generations; calculation/numeration also fits Stiegler's discussion of mnemotechnical transformation | one transient bead configuration during one calculation is **technical working retention**, but calling every intermediate position a cultural tertiary retention without specifying the level of exteriorization/transmission would erase the difference between session state and inherited practice |
| DRAM | a logical bit remains available through bounded charge survival plus scheduled regeneration; physical charge is repeatedly reconstructed under a stable selection relation | Stiegler explicitly allows silicon memory as a support; a digital text, image, recording, or database temporarily embodied in DRAM can participate in tertiary retention despite the substrate's volatility | the capacitor's current charge, a refresh operation, parity state, or arbitrary machine intermediate is not automatically a tertiary retention merely because it is non-biological and retained; **substrate class does not decide philosophical class** |
| Mapped Flash | a stable logical identity can survive deliberate relocation; data + mapping/allocation state are jointly required for the storage service | durable digital traces, databases, recordings, and other exteriorized records stored in Flash are clear candidates for digital tertiary-retentional systems | FTL-style virtual maps and block-allocation state can be constitutive **infrastructure for** the continuity of such a trace without therefore being the same retentional object; Stiegler's use of `metadata` does not license equating every controller-internal mapping entry with culturally operative metadata |
| RADOS | an object can remain current despite replica loss/replacement through placement, version, temporary authority, peering, and repair | a shared document, recording, dataset, or other transmissible trace can remain tertiary-retentional while its material replicas and privileged physical locations change | replica count, CRUSH placement, PG currentness, and repair logs explain **how** a digital object remains available; they do not by themselves tell us **what** is being exteriorized or how it enters psychic/collective memory. Distributedness is not a criterion of tertiary retention |

The philosophical verdict rests on these four grounded cases. Mercury delay-line memory is intentionally not needed for the verdict and remains `first-pass`.

---

## 6. Result 1 — `technical retention` is intentionally broader than `tertiary retention`

The repository's category answers:

> **What state remains available, by what mechanism, across what temporal gap?**

Stiegler's concept asks a thicker question about technical exteriorization and its relation to psychic, behavioural, collective, and intergenerational memory.

Therefore:

```text
tertiary retention
    is a possible philosophical interpretation of some technical-retention relations

technical retention
    is not a renamed Stieglerian category
```

This asymmetry is useful rather than embarrassing. It lets the repository examine the engineering infrastructure on which a tertiary-retentional system may depend without forcing every internal support state into the same philosophical class.

---

## 7. Result 2 — substrate does not decide tertiary-retentional status

The DRAM case is the cleanest counterexample to substrate essentialism.

The same physical mechanism can successively hold:

- a piece of encoded prose;
- a decoded audio buffer;
- a database page;
- a temporary arithmetic intermediate;
- a free-list bit;
- an ECC/parity fragment;
- an internal pointer.

At the mechanism level all are retained electrical states.

It would be analytically empty to declare them philosophically identical solely because the same capacitor/sense infrastructure held them.

Conversely, volatility does not disqualify a tertiary-retentional relation. A digital cultural trace can be transiently embodied in DRAM while being reproduced from Flash, disk, network, or another replica. The relevant continuity may reside at a higher technical layer than one physical cell.

Thus the repository rejects both:

> `nonvolatile = tertiary retention`

and

> `volatile = not tertiary retention`.

---

## 8. Result 3 — content alone is not enough either

Avoiding substrate essentialism does not mean retreating to an immaterial `content` theory.

Mapped Flash and RADOS show why.

A digital trace may remain the `same` logical object only because mappings, placement rules, version state, currentness rules, and repair procedures continue to identify an admissible embodiment.

So a tertiary-retentional object can depend on machine states that are not themselves straightforward instances of the same philosophical relation.

This produces a useful three-layer distinction:

```text
A. retentional object / trace
   what is exteriorized, repeated, transmitted, or adopted

B. constitutive identity/currentness relations
   mapping, naming, versioning, admissibility

C. retention infrastructure
   refresh, relocation, replication, repair, ECC, allocation, power, operators
```

The layers can overlap in a real system, but they should not be silently collapsed.

A controller mapping table can be indispensable to a book stored on Flash without being `the book`. A PG log can be indispensable to reconstructing a shared object without being identical to the cultural or epistemic trace carried by that object.

---

## 9. Result 4 — direct human readability is not required, but relation to practice matters

A crude boundary would say:

> only inscriptions that humans can directly read count as tertiary retention.

Stiegler's treatment of technical objects, gesture, silicon supports, databases, metadata, and digital systems makes that untenable.

The better question is functional and organological:

> **What form of experience, know-how, gesture, record, or behavioural/mental flow is technically exteriorized, and through what practices or technical operations can it be reactivated, repeated, learned, transmitted, or used to reorganize later activity?**

This allows machine mediation without treating every machine state as philosophically equivalent.

For the abacus, trained practice supplies the interpretation. For a digital database, software and schemas may mediate access. For a replicated object store, naming and protocol machinery may preserve the object across changing embodiments.

The degree of autonomous machine processing changes the circuit; it does not automatically create or abolish tertiary retention.

---

## 10. Result 5 — `intergenerational support` must not be converted into a durability threshold

Stiegler's intergenerational emphasis could be misread as a minimum retention-time specification: a state would qualify only if it survives for years or generations.

The sources do not justify that engineering rule.

What is intergenerational is the technical-cultural system and its capacity to exteriorize and transmit, not necessarily one uninterrupted physical token.

Mapped Flash and RADOS are particularly useful here:

- a physical Flash block can be erased while the logical trace persists elsewhere;
- a replica can fail while the logical object is reconstructed on another device;
- DRAM can temporarily embody a digital trace whose longer continuity exists across a storage/network system.

Therefore:

> **intergenerational transmission does not require intergenerational survival of one physical embodiment.**

This is an engineering/philosophical comparison, not a claim that Stiegler described FTL or RADOS.

---

## 11. Counterexamples that must remain visible

### Counterexample A — arbitrary machine working state

A short-lived pointer, refresh-state bit, allocator flag, or intermediate numerical value is certainly a technically retained state. Nothing in the mechanism alone proves that it exteriorizes psychic memory, experience, know-how, or a transmissible retentional flow in the Stieglerian sense.

So the repository rejects:

> `outside the brain + retained = tertiary retention`.

### Counterexample B — durable but semantically orphaned state

A nonvolatile bit pattern can persist while its format, key, schema, convention, or practice is lost. Physical durability therefore does not guarantee active retentional efficacy.

This aligns with the project's existing finding that physical survival does not imply retained current/usable meaning.

### Counterexample C — machine-readable but not equivalent roles

A user document, an FTL mapping table, and a RADOS PG log may all be machine-readable retained states. Their being machine-readable does not make their roles interchangeable.

### Counterexample D — transient embodiment of a durable relation

A tertiary-retentional object need not be tied to a nonvolatile physical token at every instant. DRAM buffering, Flash relocation, and distributed reconstruction show how higher-level continuity can traverse volatile or replaceable embodiments.

### Counterexample E — technical object versus instantaneous state

Stiegler's broad claim about technical objects as intergenerational supports should not be atomized into the claim that **every instantaneous microstate inside every technical object** is independently a tertiary retention.

The scale of analysis matters.

---

## 12. What Stiegler adds to this repository

After the boundary correction, Stiegler remains highly productive.

### A. Exteriorization is not neutral storage

A technical support can reorganize what can be repeated, compared, learned, anticipated, and transmitted. The support's affordances and operations matter.

### B. Technical memory precedes individual use

A user encounters inherited technical organs, not a blank world to which memory is later added. This is especially useful for the abacus/practice case and for modern software/storage systems whose naming, indexing, and interface conventions precede an individual session.

### C. Reproduction changes what is reproducible

Writing, numeration, recorded gesture, digital traces, databases, and metadata do not merely preserve a pre-existing object unchanged; their technical discretization and manipulation create new forms of repetition and analysis.

### D. Retentional efficacy is relational

The 2012 discussion of tertiary retention being `dead` without a reverse effect on psychic retention prevents the project from confusing bare physical survival with living circuits of adoption, learning, interpretation, and collective memory.

---

## 13. What `technical-retention` adds beyond a generic Stieglerian reading

The contribution is not the discovery that technics exteriorizes memory. Stiegler already makes that central.

The repository can add mechanism control at layers often blurred by philosophical vocabulary:

- a bead configuration can be current working state without being an archive;
- DRAM can preserve a logical trace through scheduled physical reconstruction;
- Flash can preserve one logical identity through physical relocation and retained maps;
- a distributed store can preserve a logical object through replacement of replicas and protocol-defined currentness;
- the machine states that sustain those relations need not all have the same philosophical role as the object they sustain.

This yields a narrower novelty claim:

> **A Stieglerian account of digital tertiary retention benefits from distinguishing the exteriorized trace from the retention mechanisms, identity/currentness metadata, and maintenance infrastructure that make the trace recoverable as the same trace.**

That distinction is a project interpretation, not a correction attributed to Stiegler himself.

---

## 14. Controlled vocabulary after the test

The following terms should remain distinct.

### `technical retention`

Repository-level comparative category for a materially/operationally retained state that remains actionable across a temporal gap.

### `tertiary retention`

Stieglerian philosophical concept concerning technical exteriorization/materialization and its role in psychic, behavioural, collective, and intergenerational retention.

### `retentional object / trace`

A **project term for this test only**, not Stiegler's historical terminology: the object or trace whose exteriorization/repetition/transmission is under philosophical analysis.

### `retention infrastructure`

An engineering/project term for mechanisms such as refresh, mapping, ECC, repair, allocation, placement, power, and operational maintenance that keep a higher-level state recoverable or serviceable.

These last two should not be promoted into the global glossary until further tests show that they remain useful across Heidegger/Kirschenbaum and additional technical bridges.

---

## 15. Related-repository boundary

A repository search found no existing `tertiary retention` / Stiegler treatment in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). That repository remains the source for detailed engineering histories; this document does not duplicate its memory-device chronology.

The grounded mechanism descriptions are reused from `technical-retention` cases whose wider technical context already routes outward where appropriate:

- [`cases/00-abacus-retained-position.md`](../cases/00-abacus-retained-position.md)
- [`cases/03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md)
- [`cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md)
- [`cases/05-rados-replicated-object-repair.md`](../cases/05-rados-replicated-object-repair.md)

Anti-anachronism remains governed by [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history): neither Cheng's arithmetic vocabulary nor twentieth-/twenty-first-century engineering sources are evidence that their actors formulated a Stieglerian concept.

---

## 16. Verdict

### Retained with scope

Stiegler's tertiary retention is a strong framework for asking how technical exteriorization changes memory, learning, repetition, transmission, and collective temporality. It plainly extends beyond paper archives and can include digital/silicon supports, databases, metadata, and technically reproduced behaviours.

### Rejected as a universalization

The repository rejects the equation:

> `technical retained state = tertiary retention`.

A retained machine state can be operationally indispensable without itself being the exteriorized retentional object under analysis.

### Working formulation after the test

> **Treat tertiary retention as a relation of technical exteriorization and retentional efficacy, not as a hardware class. First establish the retained mechanism; then ask what experience, know-how, trace, or behavioural/mental flow is exteriorized, how it can be repeated or transmitted, and which machine states merely sustain that continuity.**

This formulation remains a project interpretation and should stay counterexample-sensitive.

---

## 17. Evidence and maturity note

The philosophical boundary rests on four cases already marked `grounded`; no case is promoted by philosophical fit. The Stiegler anchors are primary author texts with exact printed-page verification for the 2010 book passage and a dated author text in *Computational Culture* for the digital/silicon/grammatization boundary.

Open questions deliberately left for later work:

- whether `retentional object / trace` survives comparison with Kirschenbaum's forensic materiality;
- whether Stiegler's later organology requires a stronger distinction between technical support and technical organ than this bounded test develops;
- how encrypted or permanently machine-inaccessible surviving data should be classified;
- whether executable models and learned procedures require a separate subtype from records/inscriptions;
- how `tertiary retention` should interact with a later archive/preservation case where institutional continuity, migration, and format obsolescence become central.

Those questions do not block the current verdict.