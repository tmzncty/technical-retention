# Case 02 — Magnetic-Core Retention Evidence Navigation

**Canonical case:** [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md)

**Current maturity:** `grounded` in the canonical case and ROADMAP. **No maturity promotion is made by this navigation file.**

> Repository-state note: `CASE_INDEX.md` does not currently return usable content through the connector's large-file read path. This index therefore does not invent or silently reconstruct a ledger entry; it preserves the `grounded` status already present in the canonical Case 02 and ROADMAP.

This is a **focused navigation index**, not a claim that every Case-02-adjacent file is listed. Its purpose is to keep the main retention boundaries legible as the evidence chain grows.

---

## Evidence map

| Slice | Evidence | What it establishes | Boundary |
| --- | --- | --- | --- |
| **1951–1954 core grounding** | [`02-magnetic-core-1951-1954-grounding.md`](02-magnetic-core-1951-1954-grounding.md) | remanent binary state, coincident-current selection, destructive read and restore in the bounded classic scheme, implemented MIT read–rewrite cycle, contemporary nondestructive-read counterexamples | quiescent nonvolatility != read invariance; classic destructive read != essence of all magnetic-core memory |
| **RCA 1952 `static` / no-holding-power deepening** | [`02-rca-1952-static-memory-no-holding-power-read-restore-deepening.md`](02-rca-1952-static-memory-no-holding-power-read-restore-deepening.md) | period `Static Magnetic Matrix Memory` vocabulary, no-holding-power quiescent retention, operating 256-bit experimental model, and read-triggered conditional restoration in one source | `static` != physically untouched during access; no holding power != no operating energy / support apparatus; experimental model != shipping product |
| **RCA/Rajchman 1952–1959 filing / publication provenance** | [`02-rca-1952-1959-magnetic-memory-patent-publication-provenance-deepening.md`](02-rca-1952-1959-magnetic-memory-patent-publication-provenance-deepening.md) | later primary patents attest an 8-Mar-1952 application filing and a 25-Nov-1952 parent filing while preserving June-1952 public-paper and 1956–1959 patent-publication dates as different event types | application filing != public technical disclosure != patent publication / issue != product embodiment != invention-priority adjudication |
| **IBM 705 1954–1955 retention vocabulary** | [`02-ibm-705-1954-1955-indefinite-retention-vocabulary-deepening.md`](02-ibm-705-1954-1955-indefinite-retention-vocabulary-deepening.md) | bounded product-facing use of apparently horizonless `indefinitely` language | period adjective != quantified retention specification / warranty / infinite lifetime |
| **IBM 7090 1960–1962 startup policy** | [`02-ibm-7090-1960-1962-power-on-clear-retention-policy-deepening.md`](02-ibm-7090-1960-1962-power-on-clear-retention-policy-deepening.md) | Reset can preserve core while ordinary power-on path includes clear/zeroing policy | material nonvolatility != restart preservation policy |
| **TCM-32 1964 clear/write scope** | [`02-1964-tcm32-clear-write-memory-clear-deepening.md`](02-1964-tcm32-clear-write-memory-clear-deepening.md) | selected-address clear/write versus whole-stack memory clear in a later production system | rewrite / clear scope != Flash-style erase != secure sanitization |
| **IBM 1401 / DEC PDP-7 1965–1966 power transition** | [`02-1965-1966-core-power-transition-retention-deepening.md`](02-1965-1966-core-power-transition-retention-deepening.md) | controlled power sequencing can preserve core while control state is separately reset | unpowered retention != transition immunity != whole-machine restart continuity |
| **DEC PDP-8 1966–1969 power-cycle diagnostic** | [`02-dec-1966-1969-pdp8-memory-power-cycle-diagnostic-deepening.md`](02-dec-1966-1969-pdp8-memory-power-cycle-diagnostic-deepening.md) | explicit machine test for bit dropout/pickup after simulated power failure plus bounded later restoration observations | diagnostic requirement/pass != universal substrate lifetime; observed wrong bit != proven ferrite-remanence decay |
| **DEC PDP-8/E 1973 current-cycle power-fail closure** | [`02-dec-pdp8e-1973-power-fail-current-cycle-closure-deepening.md`](02-dec-pdp8e-1973-power-fail-current-cycle-closure-deepening.md) | production maintenance manual explicitly states that POWER OK loss stops normal timing while the current memory cycle completes, with X/Y current-source shutdown delayed sufficiently to finish WRITE | stopping new/normal timing != truncating already-admitted destructive-read work; quiescent nonvolatility != in-flight closure; documented cycle completion != universal brownout survival distribution |
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

The RCA 1952 mechanism slice sharpens the first four relations because one period source itself combines:

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

The RCA/Rajchman provenance slice adds an orthogonal source-control decomposition:

```text
application filing event
    !=
public technical disclosure
    !=
patent publication / issue
    !=
named-product embodiment
    !=
invention-priority adjudication
```

A later patent's recital of an earlier filing can improve chronology without silently moving the public-document floor backward.

The PDP-8/E power-fail slice now adds a named implementation answer for the access/power boundary:

```text
power-fail detection
    -> stop normal timing progression
    != immediate withdrawal of core-drive capability

current cycle already admitted
    -> retain X/Y drive long enough for WRITE closure
    -> then remove the current source
```

This closes the qualitative current-cycle question without turning one manual into a measured worst-case brownout distribution.

---

## Historical / engineering / analogy / interpretation boundary

### Historical record

Use period papers, patents, manuals, maintenance documents, and artifacts to state what a particular system called its operations and what behavior it actually documented.

For the 1952 RCA mechanism slice, historically attested terms include:

- `Static Magnetic Matrix Memory`;
- stable physical states;
- remanent magnetization;
- no holding power;
- an operating 256-bit experimental model;
- a read / restoration sequence.

For the provenance slice, keep the event types attached to their records: an 8-March-1952 application filing is retrospectively attested by later patent text; the June-1952 RCA Review paper is a public technical disclosure; later issued patents have their own 1956–1959 publication dates.

For the 1973 PDP-8/E slice, the historical implementation vocabulary is DEC's own `POWER OK`, memory-cycle `READ` / `WRITE`, timing chain, X/Y current source, Memory Register, and the documented fast-on/slow-off power-fail circuit.

Do not silently replace those terms with later `SRAM`, standardized `NVM`, persistence-domain, transaction-drain, or crash-consistency vocabulary, and do not turn filing order into invention order.

### Engineering reconstruction

Project terms such as:

- `quiescent-retention contract`;
- `access-retention contract`;
- `logical nondestructiveness as a restored service property`;
- `power-transition boundary`;
- `drain-before-withdraw`;
- `filing floor` versus `public-document floor`;

are modern mechanism or evidence-control descriptions. They are useful only when attached to explicit period behavior or explicit document metadata.

### Functional analogy

Comparisons to DRAM restore, later nonvolatile memory, Flash retention, restart-preservation mechanisms, distributed repair, or modern in-flight drain protocols are allowed only at named relations such as:

```text
access creates a restore obligation
```

or:

```text
failure detection can change admission before completion capability is withdrawn
```

or:

```text
quiescent substrate retention does not determine restart policy
```

or, for provenance:

```text
current visible record can preserve evidence about an earlier event
```

They are not mechanism or invention genealogies.

### Philosophical interpretation

Case 02 supports the bounded interpretation that technical `stillness` is relation-specific: a state may need no continuous holding power yet still depend on active reconstruction when accessed.

The PDP-8/E deepening adds a second bounded observation: continuity across a boundary event can require preserving not only state but also enough **completion capability** to finish a reconstruction already in progress.

The provenance deepening adds a separate methodological observation: an event can precede the surviving public record that later makes the event visible. That is a statement about evidence custody, not a claim that patent archives and magnetic memory are the same technical mechanism.

These are project-level conceptual results. They are not historical claims that Rajchman, Papian, Forrester, IBM, DEC, or patent examiners formulated a philosophy of retention.

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

## Filing / publication provenance boundary

The RCA/Rajchman slice is deliberately not a legal priority study. Its purpose is to keep historical document events typed correctly.

The bounded chronology is:

```text
8-Mar-1952
    later-attested application filing

June-1952
    directly inspected public RCA Review paper

25-Nov-1952
    parent application expressly identified by a later continuation

1956–1959
    public patent issue / publication records inspected here
```

Therefore:

```text
earlier application filing
    !=
earlier proven public disclosure

continuation relation
    !=
proof that every later technical sentence existed unchanged in the parent

citation as prior literature
    !=
direct implementation genealogy
```

The exact original contents of Serial No. 275,622 and the complete public mapping/disposition of every related serial-number application remain separate archival questions.

---

## Related-repository routing

The broad engineering history remains in:

- [`tmzncty/computing-archaeology/docs/memory/why-core-memory-was-worth-weaving.md`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md).

That repository already covers core-memory selection, Whirlwind, destructive readout, system tradeoffs, and manufacturing. Keep `technical-retention` focused on the retained state, maintenance/restore obligations, transition boundaries, policy semantics, evidence lifetime, source provenance, and controlled cross-mechanism comparison.

Fresh repository searches found no dedicated PDP-8/E memory-cycle power-fail packet to reuse in this round. A broader PDP-8/E power-supply, maintenance, product-family, and field-service history should continue to route primarily to `computing-archaeology` rather than being recreated here.

---

## Maturity / status

Case 02 remains **`grounded`**.

The PDP-8/E maintenance-manual slice materially improves one previously open boundary: a named production implementation now explicitly documents completion of the current core-memory cycle after power-fail detection, with X/Y current-source shutdown delayed until the write portion can complete.

This closes the **qualitative P1 current-cycle policy** that remained open after the Victor slice. It does not yet supply a numeric slow-off delay, worst-case aged-component timing margin, external restore-complete indication, or phase-by-phase destructive power-cut experiment.

The case therefore has stronger implementation grounding without a maturity promotion. The next highest-value work is phase-specific validation and quantitative threshold/hold-up evidence, plus a counterexample controller that handles the same boundary differently.
