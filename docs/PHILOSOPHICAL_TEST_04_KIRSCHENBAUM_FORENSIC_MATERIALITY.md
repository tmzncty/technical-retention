# Philosophical Test 04 — Matthew G. Kirschenbaum: Forensic Materiality Beyond the Hard Drive

> **Bounded question:** which parts of Kirschenbaum's forensic/formal materiality distinction survive contact with mapped Flash, SSD controller indirection, and replicated object storage, and which hard-drive-specific intuitions about erasure, residue, repeatability, and survivability must be narrowed?

**Status:** bounded philosophical/prior-art test against the already `grounded` mapped-Flash and RADOS cases, with one deliberately later technical boundary source: Wei et al., FAST 2011, on SSD sanitization and raw-Flash remnants. This document does **not** promote the 1993 Flash case into a general SSD history, and it does not attribute Kirschenbaum's vocabulary to Ban/M-Systems, Ceph/RADOS engineers, or SSD designers.

The technical result is narrower than `digital data always leaves recoverable traces` and stronger than `digital media are material`:

> **Interface disappearance, logical invalidation, physical survival, forensic recoverability, and authoritative currentness are distinct relations. Kirschenbaum's forensic/formal distinction remains useful beyond magnetic disk precisely when those relations are kept separate rather than collapsed into one story about hidden residue.**

---

## 1. Why this test is necessary

[`PRIOR_ART.md`](PRIOR_ART.md) correctly treats *Mechanisms* as major prior art for this repository. Kirschenbaum does not discuss electronic textuality only at the screen or software level; he insists that storage devices, inscription mechanisms, versions, traces, and forensic recovery matter to the ontology and interpretation of digital objects.

That creates an obvious affinity with several results already grounded here:

- mapped Flash can invalidate a logical embodiment before the containing erase unit is physically erased;
- Flash mapping can preserve logical identity while physical location changes;
- RADOS can preserve one logical object while physical replicas are lost, replaced, or moved;
- a stale RADOS replica can physically survive while no longer counting as current;
- physical survival and logical/current availability have already been shown to be different properties.

But the affinity also creates a risk. *Mechanisms* makes the magnetic hard drive its central storage mechanism. A careless extension could turn hard-drive-specific forensic expectations into a universal ontology of digital persistence:

```text
deleted -> hidden physical residue -> recoverable by sufficiently deep forensics
```

Mapped Flash and distributed storage do not permit that shortcut. Controller-mediated relocation can create **more** hidden embodiments than a host interface exposes, but background reclamation can later destroy them. Cryptographic sanitization can make surviving physical data practically unreadable by removing a key. Distributed systems can leave multiple physical witnesses while protocol state decides which witness is current. Conversely, a logical object can survive even after every earlier physical embodiment relevant to one moment has been replaced.

The test therefore asks whether Kirschenbaum's distinction is best understood as a **method for refusing screen-level immateriality**, not as a guarantee that every obsolete digital state remains forensically recoverable.

---

## 2. Claim-layer boundary

This document keeps five layers distinct.

1. **Kirschenbaum primary text (`I/P`)** — *Mechanisms* defines forensic and formal materiality, foregrounds storage and inscription, and treats the hard drive as its central storage mechanism.
2. **Historical/technical record (`H/P`)** — Ban's 1993-filed Flash file-system patent documents logical/physical mapping, out-of-place update, logical invalidation before physical erase, transfer/reclamation, and retained mapping metadata.
3. **Later technical research (`S/E`)** — Wei et al. (FAST 2011) experimentally show that SSD FTL indirection can leave raw-Flash remnants invisible through the normal host interface and distinguish logical, digital, analog, and cryptographic sanitization.
4. **Grounded distributed mechanism (`H/P` + `E`)** — the 2006–2007 RADOS case distinguishes replica existence, placement, version/currentness, temporary authority, and repair.
5. **Project interpretation (`I/A`)** — this document tests how Kirschenbaum's materiality distinction behaves when embodiment is remapped, multiplied, invalidated, reconstructed, or made unreadable by a retained relation such as a key or currentness map.

No conceptual fit upgrades case maturity. The 2011 SSD evidence is a bounded later comparison, not permission to project modern SSD semantics backward into Ban's 1993 system.

---

## 3. Primary Kirschenbaum anchors

### 3.1 Storage is intentionally brought back below the visible digital object

In the Introduction to *Mechanisms*, Kirschenbaum uses Kenneth Thibodeau's physical/logical/conceptual decomposition of digital objects and argues that new-media criticism had concentrated too heavily on the conceptual, screen-level manifestation while treating the uses of electronic data as independent of the mode of physical record.

The Introduction explicitly notes that a conceptually homogeneous database may be compound at the logical and physical levels, with components distributed across multiple file systems, servers, or source media. That observation is important for the RADOS comparison below because it shows that the move from one visible object to multiple physical components is not foreign to Kirschenbaum's own starting point.

**Primary-text anchor:** Matthew G. Kirschenbaum, *Mechanisms: New Media and the Forensic Imagination* (MIT Press, 2008), Introduction, printed pp. 3–4. Page-preserving excerpt: <https://raley.english.ucsb.edu/wp-content/Engl800/Kirschenbaum-intro.pdf>.

Bibliographic/catalog anchor: MIT Press, *Mechanisms*: <https://mitpress.mit.edu/9780262113113/mechanisms/>.

### 3.2 Forensic materiality is based on individualization, not merely on `data remains after delete`

Kirschenbaum defines **forensic materiality** through the principle of individualization: physical things have particular histories and are not exactly interchangeable when inspected at sufficient resolution. He connects this to micron-scale traces of digital inscription, storage substrates, engineering practices, ergonomics, labor, and the broader material circumstances of computation.

This matters because the concept is already broader than one deletion/recovery trick. It concerns the particular material history of an embodiment and the instruments/practices that make that history legible.

**Primary-text anchor:** *Mechanisms*, Introduction, printed pp. 9–10, especially the definition beginning on p. 9 and continuing through p. 10: <https://raley.english.ucsb.edu/wp-content/Engl800/Kirschenbaum-intro.pdf>.

### 3.3 Formal materiality concerns relational computational states

Kirschenbaum contrasts forensic materiality with **formal materiality**, which he defines as the imposition of multiple relational computational states on a data set or digital object. His example emphasizes that the same data may present different layers or properties when different software/formal regimes are invoked.

He also explicitly warns against simply mapping `forensic = hardware` and `formal = software`; firmware and programmable hardware make that division unstable.

For this repository, that is the crucial bridge to mapping and distributed currentness. A stable logical object can depend on relations that are neither reducible to one physical token nor safely dismissed as immaterial abstraction.

**Primary-text anchor:** *Mechanisms*, Introduction, printed pp. 11–13: <https://raley.english.ucsb.edu/wp-content/Engl800/Kirschenbaum-intro.pdf>.

### 3.4 The book's central storage mechanism is nevertheless the hard drive

Kirschenbaum describes chapter 2, `Extreme Inscription`, as an in-depth examination of the magnetic hard disk and calls the hard drive the book's central example of storage as a writing machine. The book's institutional description likewise emphasizes storage, **particularly the hard drive**.

This source boundary matters. Kirschenbaum briefly names EEPROM/Flash while discussing the search for media that are both stable and erasable, but *Mechanisms* is not an SSD FTL monograph and does not supply the later controller semantics tested below.

Therefore:

> **Kirschenbaum's method can travel beyond disk; hard-drive-specific mechanism claims cannot travel without new technical evidence.**

**Primary-text anchor:** *Mechanisms*, Introduction, printed pp. 19–20; flash/EEPROM boundary note at printed p. 13: <https://raley.english.ucsb.edu/wp-content/Engl800/Kirschenbaum-intro.pdf>.

**Publisher anchor:** <https://mitpress.mit.edu/9780262113113/mechanisms/>.

---

## 4. Technical evidence reused and added

### 4.1 Grounded mapped Flash: obsolete logical state can survive before physical erase

The bounded Ban/M-Systems case already establishes:

- virtual/logical identity is mapped to physical Flash locations;
- rewriting can place new data in an unwritten physical block and update the map;
- the old block can become `deleted and not writable` before later unit-level physical erasure;
- reclamation copies still-current blocks before erasing the old unit;
- mapping/allocation metadata is itself retained state needed to recover which embodiment currently counts.

See [`cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md) and [`evidence/04-flash-1992-1998-grounding.md`](../evidence/04-flash-1992-1998-grounding.md).

That case supports the architectural distinction:

```text
no longer logically current
        !=
physically erased now
```

It does **not** by itself prove a universal forensic recovery window for stale Flash contents.

### 4.2 FAST 2011: SSD FTL indirection can create raw-Flash remnants invisible to the normal interface

Wei, Grupp, Spada, and Swanson experimentally tested SSD sanitization by writing identifiable patterns, applying sanitization techniques, dismantling drives, and reading raw Flash chips through custom hardware.

Their paper gives a much stronger later SSD boundary than analogy alone:

- SSDs maintain logical-to-physical indirection;
- out-of-place updates can leave old versions in raw Flash after the host-visible mapping has moved;
- the authors call these old physical copies `digital remnants`;
- in their tested devices, FTL activity could produce multiple stale copies;
- overwriting through the normal logical interface can therefore achieve **logical** sanitization without necessarily achieving **digital** sanitization;
- hard-drive-oriented single-file sanitization methods failed in their tests.

The important result for this project is not `SSDs always preserve deleted data`. It is the demonstrated separation of layers.

**Technical source:** Michael Wei, Laura M. Grupp, Frederick E. Spada, Steven Swanson, **“Reliably Erasing Data From Flash-Based Solid State Drives,”** FAST '11, USENIX Association, February 2011: <https://www.usenix.org/conference/fast11/reliably-erasing-data-flash-based-solid-state-drives>.

Open-access paper: <https://www.usenix.org/events/fast11/tech/full_papers/Wei.pdf>.

### 4.3 FAST 2011 also shows why `physical survival = forensic accessibility` is too strong

Wei et al. explicitly distinguish multiple sanitization levels:

- **logical sanitization** — data cannot be recovered through the standard device interface;
- **digital sanitization** — data cannot be recovered through digital means even by bypassing ordinary controller interfaces;
- **analog sanitization** — the underlying analog signal is degraded beyond practical reconstruction;
- **cryptographic sanitization** — encrypted data may remain while the storage holding the decryption key is sanitized.

This vocabulary is technical-security terminology from 2011, not Kirschenbaum's philosophical vocabulary and not Ban's 1993 terminology.

Its value here is methodological: `gone` must name an adversary/interface and a retained layer.

### 4.4 Grounded RADOS: physical witness and authoritative state can diverge

The RADOS case already establishes that:

- one logical object can have several replicas;
- object → PG → OSD placement can change with the cluster map;
- versioning and peering determine currentness;
- a stale physical replica can remain readable yet not be authorized as the current object;
- failed replicas can be replaced through reconstruction;
- logical identity can survive the permanent loss of an earlier physical copy.

See [`cases/05-rados-replicated-object-repair.md`](../cases/05-rados-replicated-object-repair.md) and [`evidence/05-rados-2006-2007-grounding.md`](../evidence/05-rados-2006-2007-grounding.md).

This makes distributed storage a useful limit case for forensic materiality: there may be **several individualized material witnesses** to an object's history, while protocol state separately decides which witness is current enough to serve the object now.

---

## 5. Cross-case test

| Question | Kirschenbaum / hard-drive-centered prior art | Mapped Flash / SSD boundary | RADOS boundary | Result |
| --- | --- | --- | --- | --- |
| Does interface disappearance imply physical disappearance? | forensic reading warns against screen-level ephemerality | **no**: invalidation/remapping can leave stale physical embodiments; FAST 2011 directly recovers raw-Flash remnants after host-level operations | **no**: a deauthorized/stale replica may remain physically present | strong cross-mechanism support for separating interface state from physical state |
| Does physical survival imply the old state is still the current object? | forensic trace gives evidentiary history | **no**: old block can survive after the map has moved current identity elsewhere | **no**: stale replica may survive but fail currentness/authority tests | `forensic witness ≠ authoritative current state` |
| Does overwrite mean modification of the same physical site? | magnetic-disk reasoning often makes overwrite spatially intuitive | **not generally** on managed Flash: out-of-place update and later reclaim break the assumption | distributed writes update/replace multiple embodiments under protocol ordering | overwrite semantics are medium/system-specific |
| Does a logical object's survival require survival of one earlier embodiment? | not required by Kirschenbaum's formal-materiality concept, but the central mechanism study is a physical disk | **no**: logical address can survive remapping | **no**: object can survive replica replacement | logical survivability can coexist with destruction/replacement of forensic embodiments |
| Does `deleted` mean one thing? | *Mechanisms* foregrounds traces and recovery against simple ephemerality | **no**: logical invalidation, digital recoverability, analog residue, erase, and cryptographic unreadability can diverge | **no**: deletion/currentness/service policy must be separated from existence of old replicas or logs | deletion requires layer + mechanism + authority specification |
| Is repeatability physical identity? | forensic materiality rejects exact material interchangeability; formal materiality explains repeatable computational state | repeated reads of one logical identity may traverse different physical embodiments | repeated reads of one object identity may be served after membership/replica changes | logical repeatability can be achieved through non-identical material histories |

---

## 6. Result 1 — forensic materiality survives beyond disk as a discipline of embodiment, not as a universal remanence law

The strongest portable part of Kirschenbaum's forensic materiality is the refusal to treat a digital object as if its screen-level or logical appearance exhausted its existence.

Mapped Flash strengthens that lesson. The host sees a stable logical block service, while the controller may have moved the current contents and left an obsolete embodiment behind. FAST 2011 demonstrates that such hidden raw-Flash copies were not only an architectural possibility: on the tested devices they could be physically extracted after controller-level indirection had made them invisible to the normal host interface.

But the same mechanisms that create remnants can later eliminate them. Reclamation erases blocks. A correctly implemented sanitize operation can remove recoverable data. Cryptographic sanitization can attack recoverability by destroying a key relation rather than every ciphertext embodiment.

Therefore the project should reject:

```text
forensic materiality
    =
all obsolete digital states remain physically recoverable indefinitely
```

The narrower surviving formulation is:

> **A digital object's material embodiments have particular histories that may diverge from its current interface representation. Whether an obsolete state remains recoverable is a separate empirical question about mechanism, elapsed operations, instrumentation, keys, and adversary model.**

---

## 7. Result 2 — `forensic trace` and `current state` are orthogonal categories

Kirschenbaum's forensic imagination values residual traces because they can reveal histories that a normal interface or final textual state no longer exposes.

The grounded cases add a strict systems distinction:

```text
physically surviving evidence of an earlier state
        can coexist with
an unambiguous current logical state elsewhere
```

Mapped Flash gives the local case. An invalidated block may remain physically present while the map points to the replacement block.

RADOS gives the distributed case. A stale replica may contain an intelligible previous value while peering/version state identifies another replica set/version as current.

This means a forensic investigator and a live storage service can legitimately ask different questions of the same surviving bytes:

```text
forensic question:
    what happened here, and what traces remain?

service question:
    which embodiment is admissible as the current value now?
```

Neither question reduces to the other.

The repository should therefore retain:

> **forensic witness ≠ authoritative current state**.

That distinction extends the earlier findings `physical survival ≠ retained current state` and `readability ≠ authorized currentness`.

---

## 8. Result 3 — SSDs turn erasure into a layered relation among interface, mapping, raw media, and adversary

The Flash/SSD comparison changes the prior-art boundary most sharply.

A hard-drive-centered account can easily encourage the intuition that overwrite addresses the same physical region and that increasingly deep forensic inspection asks whether a residual analog trace remains there.

Managed Flash inserts an indirection layer before that question. Wei et al. show why they must define several different sanitization levels: a normal host interface can cease to return a value while raw chips still contain a digital copy; a digital copy can be eliminated while a still deeper analog-remanence question remains; cryptographic erasure can instead remove the relation that makes surviving ciphertext intelligible.

For `technical-retention`, this yields a controlled erasure path:

```text
logical invalidation / deallocation
        ↓ may or may not coincide with
loss through standard interface
        ↓ may or may not coincide with
digital destruction of raw recoverable copies
        ↓ may or may not coincide with
analog destruction of residual physical signal

and separately:
cryptographic key destruction
        can make surviving ciphertext practically unrecoverable
        without physically erasing every data-bearing cell
```

The arrows are **not** a guaranteed chronological sequence. They are distinct predicates that particular systems and operations may satisfy together or separately.

This is a direct mechanism-level reason not to use `delete`, `erase`, `gone`, `unrecoverable`, and `destroyed` as synonyms.

---

## 9. Result 4 — survivability must be split into object, embodiment, and trace survivability

Kirschenbaum uses survivability to ask how digital objects endure through media, transmission, versions, and archival circumstances.

Mapped and distributed systems require at least three technical survivability questions.

### 9.1 Logical-object survivability

Does the named/addressed object remain recoverable as the same logical object?

Flash remapping and RADOS replica replacement can preserve this even while physical embodiments change.

### 9.2 Current-embodiment survivability

Does the particular physical embodiment that currently answers survive?

This can fail while logical-object survivability remains intact because a new embodiment is selected or reconstructed.

### 9.3 Forensic-trace survivability

Do older physical embodiments, stale replicas, logs, metadata, or remnant signals remain available to reconstruct history?

This can fail even while the logical object remains healthy. Garbage collection may erase obsolete Flash. RADOS may repair and later discard obsolete copies. Conversely, forensic traces may survive after the logical object or current service has disappeared.

Therefore:

> **logical survivability ≠ embodiment survivability ≠ trace survivability**.

This decomposition is a project result, not Kirschenbaum's terminology.

---

## 10. Result 5 — repeatability is often produced through controlled nonidentity

Kirschenbaum's pairing of forensic and formal materiality already resists the idea that digital repeatability proves material identity. Forensic materiality stresses physical particularity, while formal systems can repeatedly present what counts as the same digital object.

Mapped Flash and RADOS make this mechanism visible:

```text
same logical designation
        !=
same physical location

same returned object identity
        !=
same replica member

same recoverable value
        !=
same microscopic charge / magnetic / device history
```

A storage stack can therefore produce strong logical repeatability precisely by **tolerating and managing material nonidentity**.

The important technical invariant is not necessarily one token. It may be a relation among:

- designation;
- mapping or placement;
- currentness/version;
- error-corrected or reconstructed content;
- protocol-defined admissibility.

This is close to Kirschenbaum's formal-materiality concern with relational computational states, but the particular invariants are engineering reconstructions established by the cases, not terms imported from *Mechanisms*.

---

## 11. Result 6 — distributed storage multiplies forensic witnesses without abolishing authority

RADOS creates a useful extension beyond the single-device imagination.

At one moment, several replicas may each possess individualized material histories:

- different device serial histories;
- different local write timings;
- different sector/block allocation histories;
- different failure and recovery histories;
- potentially different stale/current versions after disruption.

A forensic approach can treat each surviving replica as a material witness.

But the live storage system has an additional problem Kirschenbaum's trace vocabulary alone does not solve:

> **Which witness is authorized to answer as current?**

RADOS uses version, epoch, peering, placement, and temporary primary authority to solve that service problem.

This yields a new boundary:

```text
more material copies
        does not entail
more ambiguity about the current logical object

and

one authoritative logical object
        does not entail
one physically privileged historical witness
```

The philosophical usefulness of forensic materiality therefore increases when distributed systems are treated as **multi-witness material histories** rather than as a placeless `cloud`.

But `forensic materiality` does not replace distributed-consistency/currentness semantics. It asks a different question.

---

## 12. Encryption/key-mediated disappearance — useful, but bounded

The roadmap explicitly warns that encryption/key-mediated disappearance should enter only when separately sourced.

Wei et al. provide that separate source boundary. They define cryptographic sanitization as a regime where the device encrypts stored data and sanitization targets the key-storage relation. They also warn that its effectiveness depends on the encryption design and the ability to prevent recovery/bypass of the key.

This supports a narrow technical claim:

> **A physical data-bearing embodiment can survive while the relation needed to interpret it is deliberately destroyed.**

That is highly relevant to the repository's earlier finding that relation loss can matter as much as payload loss.

It does **not** support the stronger claims that:

- deleting one key always proves all plaintext is unrecoverable;
- every encrypted SSD implements cryptographic erase correctly;
- physical ciphertext has been erased when the key is destroyed;
- RADOS in the bounded 2006–2007 case used such a mechanism.

Those stronger claims remain outside this slice.

---

## 13. Counterexamples and rejected shortcuts

This test rejects:

```text
forensic materiality = hard-drive remanence                         -> rejected
forensic materiality = every deleted state remains recoverable     -> rejected
logical deletion = physical erasure                                -> already rejected and reinforced
host-interface invisibility = raw-media absence                     -> rejected by mapped Flash / FAST 2011
physical survival = current logical state                           -> rejected by Flash and RADOS
physical survival = forensic accessibility                          -> rejected; access depends on mechanism, instrumentation, key, and adversary
one digital object = one physical witness                           -> rejected by RADOS and Kirschenbaum's own compound-object starting point
logical survivability = survival of one embodiment                  -> rejected by remapping and replica replacement
logical repeatability = material identity                           -> rejected
key destruction = physical data erasure                             -> rejected
```

It retains only the narrower propositions:

> **Kirschenbaum's forensic/formal materiality distinction remains a strong prior-art discipline for refusing screen-level immateriality and for tracking the interaction of physical inscription with relational computational state. Beyond magnetic disk, however, forensic claims must be re-grounded against controller indirection, reclamation, encryption, replication, and authority rather than inherited from HDD overwrite/remanence assumptions.**

and:

> **A state may survive as a forensic trace without remaining current, may remain current while all earlier embodiments are replaced, or may physically survive while a lost key/mapping/currentness relation makes it unusable.**

---

## 14. Historical, engineering, and philosophical claims kept separate

### Kirschenbaum primary/prior-art claims (`I/P`)

- *Mechanisms* deliberately brings storage and physical record into new-media analysis.
- forensic materiality is grounded in individualization and material particularity;
- formal materiality concerns multiple relational computational states imposed on a data set/digital object;
- the book explicitly warns against a simple forensic=hardware / formal=software split;
- the hard drive is the book's central storage mechanism;
- the Introduction already recognizes compound digital objects whose physical components can be distributed across servers/media.

### Historical/technical claims reused (`H/P`)

- Ban's 1993-filed Flash design separates virtual/logical identity from physical location;
- it permits logical invalidation before later erase-unit destruction;
- retained map/allocation state determines which embodiment currently counts;
- 2006–2007 RADOS separates replica existence from version/currentness and temporary protocol authority.

### Later scholarly technical boundary (`S/E`)

- FAST 2011 experimentally found raw-Flash remnants behind SSD FTL indirection on tested devices;
- it distinguishes logical, digital, analog, and cryptographic sanitization;
- it shows that HDD-oriented individual-file overwrite/sanitization assumptions did not transfer cleanly to the tested SSDs.

### Project interpretation (`I/A`)

- `forensic witness` and `authoritative current state` should be separate controlled ideas;
- `survivability` should be decomposed into logical-object, current-embodiment, and forensic-trace survivability;
- repeatable logical identity can be achieved through changing individualized physical embodiments;
- distributed storage can be read as a multi-witness material history without reducing currentness/authority to material presence;
- forensic materiality travels beyond disk as a methodological demand, not as a universal promise of recoverable remnants.

---

## 15. Relationship to existing repository results

This test does not replace the earlier audits. It sharpens them.

### Technical forgetting

[`SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md`](SYNTHESIS_AUDIT_05_TECHNICAL_FORGETTING.md) established:

- physical destruction ≠ logical forgetting;
- physical survival ≠ retained current state;
- relation loss can matter as much as payload loss;
- unavailability, staleness, invalidation, and physical erasure are distinct.

The Kirschenbaum test adds a forensic axis:

> **trace survivability is another layer that can diverge from both current logical state and service availability.**

### Addressability/currentness

[`SYNTHESIS_AUDIT_03_ADDRESSABILITY.md`](SYNTHESIS_AUDIT_03_ADDRESSABILITY.md) separates designation, resolution, candidate embodiment, currentness/admissibility, and recovery.

The forensic test adds:

```text
historical/forensic witness
        is not another word for
current/admissible embodiment
```

### Privileged location

[`SYNTHESIS_AUDIT_04_PRIVILEGED_LOCATION.md`](SYNTHESIS_AUDIT_04_PRIVILEGED_LOCATION.md) showed that logical identity can survive physical relocation without becoming placeless.

The present test adds the inverse question:

> **What histories remain at discarded places after logical identity has moved on?**

The answer is mechanism-dependent, not universally `nothing` or universally `recoverable residue`.

---

## 16. Related-repository check

A direct GitHub search of `tmzncty/computing-archaeology` for Kirschenbaum / forensic materiality and for an existing SSD-forensics treatment returned no relevant reusable research package during this slice.

Accordingly:

- no generic Flash/SSD history is duplicated here;
- the grounded Flash mechanism remains sourced from this repository's Ban/1990s case;
- the new technical addition is limited to the FAST 2011 erasure/remnant boundary needed for the philosophical test;
- any future full SSD-controller/forensics history should still be coordinated with `computing-archaeology` rather than expanded inside this document.

---

## 17. Sources

### Kirschenbaum / media theory

- Matthew G. Kirschenbaum, *Mechanisms: New Media and the Forensic Imagination*, MIT Press, 2008. Publisher record: <https://mitpress.mit.edu/9780262113113/mechanisms/>.
- Kirschenbaum, *Mechanisms*, Introduction, `Awareness of the Mechanism`, page-preserving excerpt used for the definitions and scope checks in this test: <https://raley.english.ucsb.edu/wp-content/Engl800/Kirschenbaum-intro.pdf>.
- Digital Humanities Quarterly review of *Mechanisms* (secondary check on the forensic/formal distinction): <https://www.digitalhumanities.org/dhq/vol/3/2/000048/000048.html>.

### Flash / SSD

- Amir Ban, U.S. Patent 5,404,485, **“Flash file system,”** filed 8 March 1993, issued 4 April 1995. Grounded in [`evidence/04-flash-1992-1998-grounding.md`](../evidence/04-flash-1992-1998-grounding.md).
- Michael Wei, Laura M. Grupp, Frederick E. Spada, Steven Swanson, **“Reliably Erasing Data From Flash-Based Solid State Drives,”** 9th USENIX Conference on File and Storage Technologies (FAST '11), February 2011: <https://www.usenix.org/conference/fast11/reliably-erasing-data-flash-based-solid-state-drives>; paper: <https://www.usenix.org/events/fast11/tech/full_papers/Wei.pdf>.

### Distributed storage

- Sage Weil et al., 2006–2007 Ceph/RADOS primary sources and contemporaneous implementation evidence, grounded in [`evidence/05-rados-2006-2007-grounding.md`](../evidence/05-rados-2006-2007-grounding.md).

---

## 18. Bounded verdict

The test supports a qualified extension of Kirschenbaum rather than either rejection or uncritical generalization.

### Retained

- digital objects must be studied through material embodiments as well as screen/interface appearance;
- storage mechanisms matter to textual/digital interpretation;
- forensic materiality and formal materiality provide a useful paired vocabulary for physical particularity and relational computational state;
- residual traces can expose histories hidden by a current interface.

### Narrowed

- forensic residue is **mechanism- and time-dependent**, not guaranteed merely because a digital state once existed;
- hard-drive overwrite/remanence intuitions cannot be transferred to SSDs without FTL/erase/reclamation evidence;
- physical survival does not determine currentness, readability, or forensic accessibility;
- distributed copies multiply material witnesses but do not eliminate protocol-defined currentness and authority.

### New project decomposition

```text
logical-object survivability
        !=
current-embodiment survivability
        !=
forensic-trace survivability
```

and:

```text
forensic witness
        !=
authoritative current state
```

These are **project comparison terms**, not Kirschenbaum's historical vocabulary.

The next synthesis step can now return to the roadmap's remaining high-level question — whether `technical retention` names one coherent operation or a family of mechanisms — with four named prior-art tests completed and with `trace survivability` added as a distinct layer rather than silently folded into persistence itself.
