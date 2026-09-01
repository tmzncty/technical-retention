# Philosophical Spine

This file is a map of questions, not a doctrine the technical cases are expected to illustrate.

## 1. Retention before `storage`

The repository begins with a deliberately simple question:

> How does a state outlive the moment that produced it?

This avoids assuming that every useful case belongs to the modern computer category `storage`.

A position, mark, magnetization, charge, pulse train, mapping entry, log record, or replicated value may all let a past operation remain effective later, but not in the same way.

The philosophical task is to identify the differences rather than erase them under the word `memory`.

---

## 2. Stiegler: technical exteriorization and tertiary retention

Bernard Stiegler is a central starting point because technics is not treated as a neutral container placed around an already complete human subject. Technical supports participate in the constitution and transmission of memory and temporality.

Questions for this repository:

- Which technical traces can properly illuminate `tertiary retention`?
- What changes when retained traces become machine-addressable and machine-operational rather than only human-readable?
- What changes when retrieval is automatic, indexed, probabilistic, or algorithmic?
- What changes when retention is transient but continuously renewed?
- Can a buffer, cache, or register be philosophically relevant even though it is not a cultural archive?
- How do different retention timescales interact with attention, anticipation, and inherited knowledge?

### Guardrail

`Tertiary retention` must not become a label pasted onto every memory cell.

The project should distinguish at least:

- biological remembering;
- durable external inscription;
- operational machine state;
- transient intermediary storage;
- archival preservation;
- executable / algorithmically active records.

The bounded [`PHILOSOPHICAL_TEST_02_STIEGLER_TERTIARY_RETENTION.md`](PHILOSOPHICAL_TEST_02_STIEGLER_TERTIARY_RETENTION.md) now makes the boundary explicit: `technical retention` is intentionally broader than `tertiary retention`. Substrate class, volatility, machine readability, and replication do not by themselves decide whether a retained state participates in Stiegler's thicker relation of technical exteriorization, repetition, learning, or transmission.

---

## 3. Heidegger: ordering and availability

Heidegger's `Bestand` / standing-reserve can help ask how modern technical systems render entities available for ordering and further ordering.

Technical retention introduces concrete operations that may sharpen this problem:

- indexing;
- addressing;
- inventory;
- random access;
- caching;
- prefetch;
- replication;
- tiering;
- lifecycle policy;
- deletion;
- transformation into queryable records.

But these engineering operations do not prove that `Bestand = storage`.

The research question is instead:

> Does a particular technical regime of retention participate in a broader mode of making things continuously available, substitutable, callable, and orderable? If so, through which exact operations?

The bounded [`PHILOSOPHICAL_TEST_03_HEIDEGGER_ORDERABILITY.md`](PHILOSOPHICAL_TEST_03_HEIDEGGER_ORDERABILITY.md) now tightens this boundary with primary-text anchors and grounded mechanism comparisons. Heidegger's 1977 Lovitt translation places `storing` inside a larger chain of transformation, distribution, switching, regulation, and securing, while `Bestand` names a mode of standing ready for further ordering and is explicitly more than mere stock.

The useful technical bridge is therefore narrower than a noun-to-noun analogy. The addressability audit's path

```text
designation → selection/resolution → currentness/admissibility → recovery
```

can make the engineering conditions of `being on call` precise. Mapped Flash and RADOS further show that logical callability can survive replacement of physical embodiments only because mapping, placement, version, authority, and repair relations remain effective.

The guardrail remains:

> **Technical availability can discipline a Heideggerian interpretation of orderability; it does not define `Bestand`, and a stored datum is not classified as standing-reserve merely because it can be retrieved.**

This must be argued case by case.

---

## 4. Ernst: technical memory has its own operations and times

Wolfgang Ernst is crucial because he refuses to let cultural memory discourse substitute for analysis of technical mechanisms and their timing.

For this repository, the strongest Ernstian challenge remains:

> Stop saying `memory` until you can say what the machine or technical procedure is doing.

That means examining:

- storage elements;
- registers;
- accumulators;
- buffers;
- access organization;
- read/write cycles;
- refresh;
- latency;
- circulation;
- signal timing;
- mapping and reclamation;
- protocol ordering and repair;
- operational feedback.

Ernst's 2013 `Zeitkritik` work emphasizes machine-specific temporality / `Eigenzeit`, and his statements on time-critical media make operation and timing central to the being of technical media. That emphasis is a major methodological prior art for this repository.

However, the bounded test in [`PHILOSOPHICAL_TEST_01_ERNST_OPERATIONALITY.md`](PHILOSOPHICAL_TEST_01_ERNST_OPERATIONALITY.md) shows that it should not be universalized into `retained state = continuous operation` or `technically decisive time = microtime only`.

The grounded cases force a decomposition among:

- quiescent retention;
- continuous circulation/regeneration;
- access-triggered restoration;
- deadline-driven refresh;
- workload/capacity-triggered reclamation;
- wear/lifetime-triggered placement;
- failure/membership-triggered repair;
- interpretive/procedural continuity.

A particularly productive proposition associated with Ernst's storage work is that storage and transfer are not absolute opposites: storage can be analyzed as transfer across temporal distance. The bounded [`temporal-transport audit`](SYNTHESIS_AUDIT_02_TEMPORAL_TRANSPORT.md) retains this only as a recoverability relation, not as literal motion or a sufficient mechanism theory.

The current working lesson is therefore:

> **Use operational analysis to discover the relevant timescale; do not assume in advance that every retention mechanism is continuously active or microtemporal.**

---

## 5. Kirschenbaum: forensic materiality beyond the interface and beyond disk

Matthew Kirschenbaum's forensic approach is important because the apparently immaterial digital object must be read through actual inscriptions, storage substrates, and material histories rather than only through its screen-level manifestation.

The bounded [`PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md`](PHILOSOPHICAL_TEST_04_KIRSCHENBAUM_FORENSIC_MATERIALITY.md) now tests that approach against grounded mapped Flash and RADOS, with Wei et al. FAST 2011 used as a deliberately later SSD sanitization boundary rather than projected backward into the 1993 Flash case.

The test retains Kirschenbaum's distinction between **forensic materiality** — physical particularity and individualized material history — and **formal materiality** — relational computational states. It also preserves his warning that these categories cannot simply be mapped onto `hardware` and `software`.

But the hard-drive-centered mechanism cannot be universalized into a law that every obsolete digital state leaves indefinitely recoverable residue. Managed Flash and distributed storage require stronger distinctions:

```text
interface disappearance
        !=
logical invalidation
        !=
physical destruction
        !=
forensic recoverability
        !=
authoritative currentness
```

Mapped Flash can leave an obsolete embodiment physically present after the map has moved current identity elsewhere; later SSD experiments show that controller indirection can leave raw-Flash remnants invisible through the normal host interface, while reclamation, sanitization, or key destruction can later change recoverability. RADOS adds a distributed version of the problem: several physical replicas may survive as material witnesses while version, epoch, peering, and authority determine which one counts as current.

The project therefore adds two controlled comparison rules:

> **forensic witness ≠ authoritative current state**

and

> **logical-object survivability ≠ current-embodiment survivability ≠ forensic-trace survivability**

These are project terms, not Kirschenbaum's historical vocabulary.

The guardrail is now:

> **Forensic materiality travels beyond magnetic disk as a methodological demand to investigate embodiment and trace history. Hard-drive-specific assumptions about overwrite, remanence, and recovery must be re-grounded for Flash, SSD controllers, encryption, and distributed systems rather than carried over by analogy.**

---

## 6. Persistence as an achieved relation

The first bounded synthesis audit rejected the universal equation `persistence = continuous activity`.

The surviving project hypothesis is narrower:

> **Persistence is often an achieved relation, but the work required to sustain it depends on the retained layer and the trigger that creates a maintenance obligation.**

Cases already distinguish:

- passive positional stability;
- quiescent magnetic remanence;
- destructive-read restore;
- deadline-driven DRAM refresh;
- Flash remapping and reclamation;
- distributed peering and repair.

The philosophical question is no longer simply why users experience an active process as a static thing. It is:

> **Which work, if any, is required merely for a state to remain; which work is required only on access, workload, wear, failure, or interpretation; and which of those obligations are visible at which interface?**

See [`SYNTHESIS_AUDIT_01_MAINTAINED_PERSISTENCE.md`](SYNTHESIS_AUDIT_01_MAINTAINED_PERSISTENCE.md) and [`SYNTHESIS_AUDIT_06_MAINTENANCE_VISIBILITY.md`](SYNTHESIS_AUDIT_06_MAINTENANCE_VISIBILITY.md).

---

## 7. Identity without location

Modern storage increasingly separates logical identity from physical location.

A file block, virtual page, SSD LBA, object-store key, database row, or replicated log entry may retain its identity while the physical bits move, are rewritten, or are reconstructed elsewhere.

Questions:

- What must remain invariant for the retained thing to count as `the same`?
- Is identity carried by address, content, metadata, causal history, naming, protocol, or institutional convention?
- At what layer does identity reside?
- Can a retained object's substrate be completely replaced without loss of identity?

This is a technical problem before it is a metaphysical metaphor.

---

## 8. Technical forgetting

Forgetting is not one operation.

Candidate distinctions:

- passive decay;
- volatile loss after power removal;
- refresh failure;
- destructive read without rewrite;
- overwrite;
- block erase;
- logical deletion;
- unlinking / loss of reference;
- garbage collection;
- loss of index;
- loss of mapping metadata;
- key destruction;
- media damage;
- format obsolescence;
- protocol or software obsolescence;
- institutional abandonment;
- deliberate archival destruction.

A philosophy of technical memory that cannot distinguish these mechanisms is too coarse for this project.

---

## 9. A long-term synthesis question

Only after the case studies accumulate should the project attempt to answer:

> Is `retention` one philosophical operation instantiated by many technologies, or only a family resemblance we impose across fundamentally different mechanisms?

Either answer is acceptable if the evidence supports it.
