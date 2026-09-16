# Deepening Record — 1963–1972 Magnetic-Memory Thermal Control: Kuhlmann Prior Art and Access-Rate Throttling

## Target case

[`cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md)

Follow-on to [`02-1970-1973-core-temperature-compensation-operating-margin-deepening.md`](02-1970-1973-core-temperature-compensation-operating-margin-deepening.md).

Related named-machine operating-margin work remains in [`70-dec-pdp8e-1973-operating-margin-deepening.md`](70-dec-pdp8e-1973-operating-margin-deepening.md).

## Status

**`bounded deepening complete`**

This record closes the **bibliographic/chronological part** of the earlier record's Kuhlmann debt and adds one distinct contemporary thermal-control architecture. It does **not** claim to have recovered a complete facsimile-level reading of Kuhlmann's 1963-priority patent family, nor does it claim commercial deployment of the patent mechanisms.

The narrow question is:

> Before the 1970–1973 Call / Hewlett-Packard / Ampex slice, what public prior art already tied magnetic-memory operation to temperature-dependent current control, and could thermal operating margin also be protected by controlling *when accesses are admitted* rather than only by changing current?

The bounded answer is:

```text
remanent payload survives
    !=
access electronics are indefinitely admissible at any workload

thermal-control strategy
    !=
one universal mechanism

current compensation
    !=
access-rate throttling

recent-access control state
    !=
user payload
```

---

## Why this slice is separate from general core-memory history

Case 02 is grounded in 1950–1954 MIT evidence for remanence, selection, destructive read, and restoration. Case 70 owns the narrower half-select / operating-margin story in named machines. The existing 1970–1973 temperature-compensation record already shows later proposed ways of adapting inhibit or drive current and supplies an Ampex negative control.

This follow-on does only two things:

1. pushes the inspected **temperature-control prior-art chronology** backward to the Kuhlmann / Olympia patent family;
2. records a Siemens design in which recent access history is represented as an analog thermal-control state and used to **limit access rate**.

The latter is deliberately not projected onto Whirlwind, DEC, IBM, or the Kuhlmann mechanism.

---

## Historical record

### H/P* — Kuhlmann / Olympia public prior-art floor precedes the 1970–1971 filings

Later patent records consistently identify U.S. Patent **3,354,443**, Kuhlmann, **“Device for temperature compensation of magnetic storage cores in data processing installations,”** published / issued on **1967-11-21**.

The German family metadata preserved in the later Hewlett-Packard family record points further back to:

- **DE1216364B**;
- priority date **1963-04-18**;
- publication date **1966-05-12**;
- assignee **Olympia Werke AG**;
- translated title **“Arrangement for the temperature-dependent regulation of the magnetic reversal currents for magnetic storage cores.”**

This gives a conservative inspected public-document floor earlier than the 1970 Call filing and the 1971 Hewlett-Packard filing.

The evidence strength is intentionally marked `H/P*`, not full `H/P`, because this run recovered the family/bibliographic record and later primary citations but did **not** recover and inspect the complete Kuhlmann specification and claims themselves.

Therefore the repository may safely say:

```text
by 1966 public patent-family record:
    temperature-dependent regulation of magnetic-core reversal current
    is already explicit vocabulary
```

It may **not** yet say exactly which sensor topology, transfer function, current path, or production machine implemented Kuhlmann's design.

### H/P — Kuhlmann was treated as relevant prior art by multiple later magnetic-memory patents

The Kuhlmann U.S. patent is cited in at least three later records inspected in this slice:

1. Henry M. Call, U.S. Patent 3,626,393, **“Temperature Compensation Circuit for Magnetic Core Memories,”** filed 1970-02-13 and issued 1971-12-07;
2. Siemens AG, U.S. Patent 3,707,704, **“Selective Circuit for a Data Storer with Optional Access,”** filed 1970-09-09 and issued 1972-12-26;
3. Robert J. Frankenberg / Hewlett-Packard, U.S. Patent 3,750,119, **“Computer Memory Temperature Compensation,”** filed 1971-10-20 and issued 1973-07-31.

That repeated citation is evidence that the Kuhlmann record remained visible as relevant prior art in the early-1970s patent literature.

It is **not** evidence that Call, Siemens, or Hewlett-Packard copied Kuhlmann's circuit, nor that all four records form one direct engineering lineage.

Patent citation relation is weaker than implementation genealogy:

```text
later patent cites earlier patent
    !=
direct design transfer
    !=
commercial deployment lineage
```

### H/P — Call characterizes the preexisting design problem as temperature-sensitive drive/inhibit control

Call's 1970-filed patent states that magnetic-core characteristics change with ambient temperature and that an inhibit path must prevent unwanted switching without becoming so strong that it defeats intended setting current.

It says prior-art compensation devices changed the voltage supplying inhibit drivers, while Call proposes exploiting temperature-dependent resistance in the inhibit winding/current-limiting path itself.

Kuhlmann is the core-memory patent explicitly listed in Call's patent references.

Because the Call text discusses `prior art` in the plural and does not assign every sentence to a single cited patent, this record does **not** attribute every described prior-art voltage-control detail specifically to Kuhlmann.

The safe relation is:

```text
Kuhlmann is cited as relevant earlier core-memory temperature prior art
+
Call describes voltage/current compensation as an existing approach

but

Call's generic prior-art description
    !=
page-level reconstruction of Kuhlmann's exact circuit
```

### H/P — Hewlett-Packard confirms temperature-dependent drive current and distinguishes ambient from activity heating

Hewlett-Packard's 1971-filed patent also cites Kuhlmann 3,354,443.

Its own description says magnetic-core stacks require temperature-dependent drive current and identifies two contributors to memory temperature:

- heat from the surrounding computer;
- heat generated within memory by current passing through it.

It further distinguishes two earlier compensation patterns: sensing individual core stacks and averaging them, or sensing ambient temperature while assuming a nominal constant stack temperature rise. The latter can be inaccurate after a memory has cooled during a long period without use.

This does not identify either generic earlier method uniquely with Kuhlmann. It does, however, strengthen the historical record that by the early 1970s `temperature compensation` was not one circuit but a design family with different sensed variables and approximations.

### H/P — Siemens 1970: protect selection electronics by retaining a model of recent access activity

Siemens AG filed U.S. Patent 3,707,704 on **1970-09-09**; it was issued on **1972-12-26**.

The patent addresses a different thermal problem from payload remanence. It says selective circuits had traditionally been dimensioned so that random access could be tolerated at any time, which could prevent faster and less expensive designs. Under normal random-access operation, addresses change; a pathological or test case may repeatedly call the same address and therefore repeatedly operate the same selection circuit.

The proposed control architecture:

- models / imitates the thermal behavior of a selection circuit;
- uses a timing network including resistors and a capacitor;
- describes the capacitor as an **analog store** for the succession of calls to a storage address;
- evaluates a thermal threshold;
- limits the succession of storage operations for addresses whose repeated use would otherwise overload the selection circuitry.

The patent explicitly explains that if several addresses alternate, a given selection circuit receives recovery periods during which its temperature can fall, allowing a different admissible service rate.

This is direct primary evidence for an **activity-history-dependent access-admission controller**.

### H/P — Siemens is a related magnetic-memory control record, not evidence about ferrite payload decay

The Siemens patent says the technique is useful for random-access stores and specifically discusses word-organized **magnetic-wire storage** as an advantageous application.

Accordingly, this record does not relabel it as a ferrite-core implementation.

Its relevance to Case 02 is narrower:

```text
magnetic-memory access path
    may have a thermal operating history
    that constrains whether another access is admissible
```

That is a control-architecture comparison around retained-state usability, not a claim that magnetic-wire payload and ferrite-core remanence are the same substrate mechanism.

### H/P — Siemens also cites Kuhlmann, but citation does not collapse the mechanisms

The Siemens patent's U.S. references include Kuhlmann 3,354,443.

Yet Siemens' disclosed intervention is not simply `adjust magnetic-core reversal current`. It prevents selection-circuit overload by simulating recent thermal load and limiting call succession.

Therefore the citation establishes relevance of prior temperature-control work, not mechanism identity:

```text
shared prior-art citation
    !=
same control variable
    !=
same protected component
    !=
same memory substrate
```

---

## Engineering reconstruction

### E — retained payload and access admissibility are different state variables

Case 02's payload-bearing state is remanent magnetization. The later control records show that another question exists around it:

```text
is the payload still physically present?

vs

is the access apparatus currently inside a safe operating region?
```

A `yes` to the first does not force a `yes` to the second.

Thus:

> **payload persistence ≠ immediate service admissibility**.

This does not mean the payload has been forgotten. It means normal access may be delayed or require parameter adaptation.

### E — temperature control can target different variables

Across the bounded records, designers intervene at different points:

```text
Kuhlmann family title / chronology
    -> temperature-dependent regulation of reversal current

Call
    -> exploit inhibit-path resistance to adapt inhibit current

Hewlett-Packard
    -> estimate ambient + activity heating and regulate drive supply

Siemens
    -> estimate selection-circuit thermal history and limit access rate

Ampex negative control from the companion record
    -> spend margin in material / pulse design to avoid active compensation
```

The synthesis is:

> **same broad thermal constraint ≠ one required control architecture**.

### E — recent access history can itself become operational retained state

The Siemens capacitor does not store user words. It stores a decaying analog representation related to the succession of recent address calls.

That state affects future behavior:

```text
recent accesses
    -> analog thermal-model state
    -> threshold evaluation
    -> access admitted or delayed
```

Therefore:

> **operationally consequential retained state ≠ payload state**.

This is exactly the kind of distinction the repository needs: a machine can retain temporary control history whose purpose is to keep access machinery inside an operating envelope.

### E — modeled thermal state is not measured payload temperature

Siemens describes an imitation of thermal behavior rather than a direct measurement of a stored bit's temperature.

Therefore:

```text
control-state estimate of thermal load
    !=
direct physical measurement of core temperature
    !=
payload value
```

The system can make a real scheduling decision from a model state that is neither user data nor an archival log.

### E — throttling is not refresh

Siemens' intervention may reduce or delay storage operations. It does not periodically reconstruct decaying user payload in the DRAM sense.

So:

```text
access throttling
    !=
payload refresh
    !=
destructive-read restore
```

All three can affect whether data remains usable, but they operate on different failure surfaces.

### E — inactivity can improve access margin without changing payload identity

In the Siemens model, a recovery interval lets selection circuitry cool. The payload need not be rewritten for this to happen.

This gives a useful inverse of maintenance-by-activity:

```text
waiting
    -> control apparatus recovers thermal margin

without implying

waiting
    -> payload rewritten
```

That distinction prevents `maintenance` from becoming so broad that every beneficial idle period is mislabeled as state restoration.

---

## Functional comparisons

### A — Case 70 half-select disturbance

Case 70 shows that an access can physically burden non-target magnetic elements and shared sensing paths. The Siemens record instead concerns thermal loading of **selection circuitry** under an unfavorable access pattern.

The bounded commonality is only:

> ordinary memory traffic can create an operating-margin obligation outside the selected payload bit itself.

The mechanisms must remain distinct:

```text
half-select magnetic disturbance
    !=
selection-circuit thermal overload
```

### A — Case 03 DRAM refresh

DRAM refresh restores decaying cell charge. The thermal-control records adapt drive conditions or service rate around a remanent / magnetic store.

The safe analogy is:

```text
continued usability can depend on support machinery
```

The analogy stops there.

### A — modern thermal / activity throttling

A high-level functional analogy exists to later systems that admit work according to a thermal or recent-activity budget.

This record does **not** claim a genealogy from Siemens 1970 to later CPU, DRAM, SSD, or RowHammer throttling. The similarity is one abstract control relation:

```text
recent activity
    -> estimated operating stress
    -> future work admission
```

No direct historical continuity is asserted.

---

## Philosophical boundary

One narrow interpretation is justified:

> A retained object can continue to exist while the system temporarily withholds the operation that would normally expose or modify it.

That is a statement about **conditional availability**, not about the payload becoming absent.

The Siemens analog history also shows that `retention` inside a machine can be deliberately short-lived and operational: its value lies precisely in decaying as the modeled thermal burden recovers.

This is an engineering/philosophical interpretation. Neither Siemens, Kuhlmann, Call, nor Hewlett-Packard is presented as making a general theory of memory or persistence.

---

## Explicit non-claims

This record does **not** claim that:

1. Kuhlmann invented magnetic-core temperature compensation;
2. the 1963 priority date is the date of public disclosure;
3. the exact Kuhlmann circuit has been facsimile-inspected in this run;
4. the complete Kuhlmann claims or implementation details are reconstructed here;
5. Olympia commercially shipped a machine using the Kuhlmann patent exactly as filed;
6. a later patent citation proves direct technical influence;
7. Call's generic `prior art` description can be assigned word-for-word to Kuhlmann;
8. Hewlett-Packard's two generic prior-art methods can be assigned specifically to Kuhlmann;
9. Siemens' thermal throttling is a ferrite-core payload mechanism;
10. magnetic-wire storage and ferrite-core memory are physically identical;
11. Siemens throttling refreshes magnetic payload;
12. the analog capacitor state is user payload or archival history;
13. simulated thermal state equals directly measured component temperature;
14. delayed access means data has been forgotten;
15. a temperature-control patent proves field deployment or failure frequency;
16. shared citation of Kuhlmann makes the later designs one engineering lineage;
17. this slice establishes a universal thermal limit or duty cycle for magnetic memory;
18. this slice replaces the stronger named-machine DEC/IBM service evidence in Case 70.

---

## Claim ledger

| Claim | Label | Evidence | Strength / boundary |
| --- | --- | --- | --- |
| The Kuhlmann / Olympia family has 1963-04-18 priority and DE1216364B publication on 1966-05-12 | `H/P*` | patent-family metadata preserved in HP family record | strong bibliographic chronology; Kuhlmann body not directly inspected |
| US3354443 is titled `Device for temperature compensation of magnetic storage cores in data processing installations` and was published/issued 1967-11-21 | `H/P*` | repeated later patent citation records | bibliographic / citation evidence |
| The German family title explicitly concerns temperature-dependent regulation of magnetic reversal currents for magnetic storage cores | `H/P*` | DE1216364B family metadata | title-level mechanism boundary only |
| Call 1970, Siemens 1970, and HP 1971 records cite Kuhlmann 3354443 | `H/P` | three inspected later patent records | proves citation relation, not design genealogy |
| Call describes temperature-sensitive inhibit/current margin and proposes resistance-based compensation | `H/P` | US3626393A | strong primary proposed mechanism |
| HP describes ambient plus memory-activity heating as contributors to required drive current | `H/P` | US3750119A | strong primary proposed mechanism |
| Siemens models selection-circuit thermal history and limits repeated-address call succession | `H/P` | US3707704 | strong primary proposed mechanism |
| Siemens describes a capacitor as an analog store for recent address-call succession | `H/P` | US3707704 | strong primary terminology / mechanism |
| The Siemens record proves ferrite-core payload decay under repeated address calls | `X` | source concerns selection-circuit overload and includes magnetic-wire application | rejected overreach |
| Access throttling is a form of DRAM-like refresh | `X` | different controlled quantity and operation | rejected collapse |
| Later citation proves Kuhlmann was commercially deployed | `X` | no deployment evidence in this slice | rejected inference |
| Payload persistence and safe immediate access are identical properties | `X` | contradicted by bounded control architectures | rejected collapse |

---

## Source hierarchy

### Earlier patent-family / citation record

1. **DE1216364B**, Olympia Werke AG, priority `1963-04-18`, publication `1966-05-12`, translated title **“Arrangement for the temperature-dependent regulation of the magnetic reversal currents for magnetic storage cores.”** Bibliographic family metadata visible in the German family record of Hewlett-Packard's later patent: <https://patents.google.com/patent/DE2247994A1/en>.
2. Kuhlmann, **U.S. Patent 3,354,443**, **“Device for temperature compensation of magnetic storage cores in data processing installations,”** issued `1967-11-21`. The title/date are preserved in the inspected later U.S. patent references below.

Because the Kuhlmann specification body was not directly recovered, sources 1–2 are used conservatively for chronology, title-level vocabulary, and citation lineage only.

### Primary later technical sources

3. Henry M. Call, **“Temperature Compensation Circuit for Magnetic Core Memories,”** U.S. Patent 3,626,393, filed `1970-02-13`, issued `1971-12-07`: <https://patents.google.com/patent/US3626393A/en>.
4. **“Selective Circuit for a Data Storer with Optional Access,”** U.S. Patent 3,707,704, filed `1970-09-09`, issued `1972-12-26`, Siemens AG; preserved full-text mirror: <https://www.freepatentsonline.com/3707704.html>.
5. Robert J. Frankenberg, **“Computer Memory Temperature Compensation,”** U.S. Patent 3,750,119, filed `1971-10-20`, issued `1973-07-31`, Hewlett-Packard Company: <https://patents.google.com/patent/US3750119A/en>.

### Repository evidence reused rather than duplicated

6. [`02-1970-1973-core-temperature-compensation-operating-margin-deepening.md`](02-1970-1973-core-temperature-compensation-operating-margin-deepening.md) — Call / HP / Ampex control-architecture comparison.
7. [`70-dec-pdp8e-1973-operating-margin-deepening.md`](70-dec-pdp8e-1973-operating-margin-deepening.md) — named-machine DEC/IBM operating-margin evidence.
8. [`02-magnetic-core-1951-1954-grounding.md`](02-magnetic-core-1951-1954-grounding.md) — Case 02 historical grounding.

---

## Related repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Kuhlmann`, `US3354443`, and the exact temperature-compensation terms did not surface a dedicated history to reuse.

Accordingly this file keeps only the retention-specific boundary:

- payload remanence versus access admissibility;
- temperature-dependent current control versus access-rate control;
- recent-activity-derived control state versus payload state.

A full Olympia / Kuhlmann patent-family genealogy, magnetic-wire-store history, vendor implementation history, or thermal-design history belongs in `computing-archaeology` if pursued.

---

## Remaining evidence debt

This round closes the earlier record's **Kuhlmann chronology/citation** debt but not every implementation question. Remaining useful work is:

1. recover a directly inspectable full Kuhlmann / Olympia specification or national-family facsimile and compare its claims to the title-level family metadata;
2. determine whether a named Olympia computer or memory product can be tied to the Kuhlmann mechanism without inferring deployment from assignment alone;
3. inspect period core-manufacturer material data with quantitative switching-current / temperature curves;
4. keep Siemens magnetic-wire selection-circuit throttling separate from ferrite-core payload retention unless a stronger source bridges them;
5. do not infer shelf-retention lifetime from thermal access-control evidence.

The new retained-state decomposition is therefore:

```text
remanent payload
    !=
thermal operating condition
    !=
current / inhibit calibration relation
    !=
recent-access thermal-model state
    !=
access-admission decision
    !=
proof of successful read or write
```
