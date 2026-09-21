# Case 02 — Magnetic-Core Retention Evidence Navigation

**Canonical case:** [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md)

**Current maturity:** `grounded` in the canonical case and ROADMAP. **No maturity promotion is made by this navigation file.**

> Repository-state note: `CASE_INDEX.md` is currently an empty file on `main`, although `ROADMAP.md` describes it as the authoritative maturity ledger. This index therefore does not invent or silently reconstruct a missing ledger entry; it records the status already present in the canonical Case 02 and ROADMAP until the repository-wide ledger inconsistency is repaired in a separate bounded slice.

This is a **focused navigation index**, not a claim that every Case-02-adjacent file is listed. Its purpose is to keep the main retention boundaries legible as the evidence chain grows.

---

## Evidence map

| Slice | Evidence | What it establishes | Boundary |
| --- | --- | --- | --- |
| **1951–1954 core grounding** | [`02-magnetic-core-1951-1954-grounding.md`](02-magnetic-core-1951-1954-grounding.md) | remanent binary state, coincident-current selection, destructive read and restore in the bounded classic scheme, implemented MIT read–rewrite cycle, contemporary nondestructive-read counterexamples | quiescent nonvolatility != read invariance; classic destructive read != essence of all magnetic-core memory |
| **RCA 1952 `static` / no-holding-power deepening** | [`02-rca-1952-static-memory-no-holding-power-read-restore-deepening.md`](02-rca-1952-static-memory-no-holding-power-read-restore-deepening.md) | period `Static Magnetic Matrix Memory` vocabulary, no-holding-power quiescent retention, operating 256-bit experimental model, and read-triggered conditional restoration in one source | `static` != physically untouched during access; no holding power != no operating energy / support apparatus; experimental model != shipping product |
| **IBM 705 1954–1955 retention vocabulary** | [`02-ibm-705-1954-1955-indefinite-retention-vocabulary-deepening.md`](02-ibm-705-1954-1955-indefinite-retention-vocabulary-deepening.md) | bounded product-facing use of apparently horizonless `indefinitely` language | period adjective != quantified retention specification / warranty / infinite lifetime |
| **IBM 7090 1960–1962 startup policy** | [`02-ibm-7090-1960-1962-power-on-clear-retention-policy-deepening.md`](02-ibm-7090-1960-1962-power-on-clear-retention-policy-deepening.md) | Reset can preserve core while ordinary power-on path includes clear/zeroing policy | material nonvolatility != restart preservation policy |
| **TCM-32 1964 clear/write scope** | [`02-1964-tcm32-clear-write-memory-clear-deepening.md`](02-1964-tcm32-clear-write-memory-clear-deepening.md) | selected-address clear/write versus whole-stack memory clear in a later production system | rewrite / clear scope != Flash-style erase != secure sanitization |
| **IBM 1401 / DEC PDP-7 1965–1966 power transition** | [`02-1965-1966-core-power-transition-retention-deepening.md`](02-1965-1966-core-power-transition-retention-deepening.md) | controlled power sequencing can preserve core while control state is separately reset | unpowered retention != transition immunity != whole-machine restart continuity |
| **DEC PDP-8 1966–1969 power-cycle diagnostic** | [`02-dec-1966-1969-pdp8-memory-power-cycle-diagnostic-deepening.md`](02-dec-1966-1969-pdp8-memory-power-cycle-diagnostic-deepening.md) | explicit machine test for bit dropout/pickup after simulated power failure plus bounded later restoration observations | diagnostic requirement/pass != universal substrate lifetime; observed wrong bit != proven ferrite-remanence decay |
| **1963–1972 thermal-control / access-throttling prior art** | [`02-1963-1972-core-thermal-control-prior-art-access-throttling-deepening.md`](02-1963-1972-core-thermal-control-prior-art-access-throttling-deepening.md) | later operating-control strategies around temperature / service conditions | quiescent remanence != unconstrained powered operating service |
| **1970–1973 temperature compensation / margin control** | [`02-1970-1973-core-temperature-compensation-operating-margin-deepening.md`](02-1970-1973-core-temperature-compensation-operating-margin-deepening.md) | temperature-dependent drive/inhibit control as one later design strategy | retained payload != temperature-independent operating margin; one strategy != universal architecture |
| **1991 clearing / purging / degaussing vocabulary** | [`02-1991-ncsc-core-clearing-purging-degaussing-deepening.md`](02-1991-ncsc-core-clearing-purging-degaussing-deepening.md) | later security-assurance vocabulary around removal of recoverable information | overwrite / clearing != purging != generic `forgetting`; later security terms must not be projected backward |
| **Papian 1952 page-level disturbance evidence (Case 70)** | [`70-papian-1952-half-select-disturbance-facsimile-deepening.md`](70-papian-1952-half-select-disturbance-facsimile-deepening.md) | direct facsimile inspection of repeated half-select disturbance geometry and discrimination | laboratory disturbance test != named-machine field distribution; linked rather than duplicated in Case 02 |

---

## Retention decomposition now supported

The evidence chain should not be compressed into one `magnetic core is nonvolatile` sentence.

```text
remanent physical state while quiescent
    !=
resistance to half-select / neighboring disturbance
    !=
read invariance
    !=
logical equality after a read/restore cycle
    !=
powered operating margin
    !=
power-transition immunity
    !=
startup preservation policy
    !=
post-restart control state
    !=
secure erasure / sanitization state
```

The new RCA 1952 slice sharpens the first four relations because one period source itself combines:

```text
`static` memory vocabulary
+
no holding power between operations
+
interrogation that may disturb the selected core
+
conditional restoration to preserve the logical value
```

That directly blocks the shortcut:

```text
static
    -> nothing physical changes
```

The historically safer relation is:

```text
static with respect to quiescent holding-energy demand
    !=
static with respect to access trajectory
```

---

## Historical / engineering / analogy / interpretation boundary

### Historical record

Use period papers, patents, manuals, maintenance documents, and artifacts to state what a particular system called its operations and what behavior it actually documented.

For the new 1952 slice, historically attested terms include:

- `Static Magnetic Matrix Memory`;
- stable physical states;
- remanent magnetization;
- no holding power;
- an operating 256-bit experimental model;
- a read / restoration sequence.

Do not silently replace those terms with later `SRAM`, standardized `NVM`, persistence-domain, or crash-consistency vocabulary.

### Engineering reconstruction

Project terms such as:

- `quiescent-retention contract`;
- `access-retention contract`;
- `logical nondestructiveness as a restored service property`;
- `power-transition boundary`;

are modern mechanism descriptions. They are useful only when attached to explicit period behavior.

### Functional analogy

Comparisons to DRAM restore, later nonvolatile memory, Flash retention, or restart-preservation mechanisms are allowed only at named functions such as:

```text
access creates a restore obligation
```

or:

```text
quiescent substrate retention does not determine restart policy
```

They are not mechanism or invention genealogies.

### Philosophical interpretation

Case 02 supports the bounded interpretation that technical `stillness` is relation-specific: a state may need no continuous holding power yet still depend on active reconstruction when accessed.

That is a project-level conceptual result. It is not a historical claim that Rajchman, Papian, Forrester, IBM, or DEC formulated a philosophy of retention.

---

## Cross-vendor vocabulary boundary

The RCA 1952 and IBM 705 1955 evidence should be read together but not merged:

```text
RCA 1952 technical paper
    -> `static`
    -> no-holding-power remanent storage
    -> explicit operating / restore mechanism
    -> experimental hardware

IBM 705 1955 promotional literature
    -> `indefinitely`
    -> product-facing retention rhetoric
    -> no numerical retention qualification envelope on the cited brochure page
```

The comparison demonstrates that apparently horizonless magnetic-memory language appears in more than one 1950s vendor context.

It does **not** demonstrate:

- one common circuit;
- one common test method;
- one common reliability contract;
- one shared authorial lineage;
- first coinage of any term.

Source genre and mechanism remain part of the evidence.

---

## Related-repository routing

The broad engineering history remains in:

- [`tmzncty/computing-archaeology/docs/memory/why-core-memory-was-worth-weaving.md`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md).

That repository already covers core-memory selection, Whirlwind, destructive readout, system tradeoffs, and manufacturing. Keep `technical-retention` focused on the retained state, maintenance/restore obligations, transition boundaries, policy semantics, evidence lifetime, and controlled cross-mechanism comparison.

A fresh repository search for a dedicated Rajchman-1952 retention packet found no narrower `computing-archaeology` artifact to reuse in this round.

---

## Maturity / status

Case 02 remains **`grounded`**.

The RCA 1952 deepening improves:

- period terminology;
- cross-vendor prior-art control;
- direct evidence for `quiescent no-holding-power != access-triggered restore`;
- the chronology of public no-holding-power / apparently horizonless retention language.

It does **not** justify a promotion because substantial open work remains around material distributions, early production correspondence, exact power-transition behavior in the earliest experimental systems, cross-machine reliability distributions, and broader genealogy.

---

## Remaining bounded debt

High-value follow-ons include:

- earlier RCA internal / patent / conference wording before June 1952;
- exact patent chronology around Rajchman/Rosenberg without treating filing order as invention priority;
- direct power-off / power-on evidence for the 1952 RCA 256-bit experimental unit;
- quantitative dormant-remanence evidence under specified material / temperature conditions;
- cross-vendor terminology at Burroughs, Remington Rand/UNIVAC, DEC, and other early systems;
- cross-machine operating-margin distributions and earlier production correspondence;
- repository-wide repair of the currently empty `CASE_INDEX.md` maturity ledger in a dedicated scaffold-maintenance slice, rather than silently reconstructing it inside one case.

Broader institutional and device genealogy should continue to route primarily to `computing-archaeology`.
