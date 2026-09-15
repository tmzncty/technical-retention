# Evidence 09 — 1981–1983 autonomous DRAM self-refresh prior-art deepening

**Status:** `bounded deepening complete`

**Parent case:** [`../cases/09-dram-cbr-refresh-address-internalization.md`](../cases/09-dram-cbr-refresh-address-internalization.md)

**Bounded question:** did early-1980s DRAM work already place both refresh-row enumeration and recurring refresh timing on-chip, and if so, how should that evidence change the Case-09 comparison between CAS-before-RAS refresh and later SDRAM SELF REFRESH?

This record is intentionally narrow. It does **not** attempt to establish invention priority for self-refresh, a complete DRAM standardization genealogy, a product-shipment chronology, or a direct line of descent from one 1981/1983 design to later SDRAM.

---

## Why this slice matters

Case 09 already established an important architectural distinction from Texas Instruments' 1984-filed CAS-before-RAS work:

```text
internal refresh-row enumeration
    != internal recurring refresh cadence
```

That result remains correct. TI's disclosed CBR counter supplies the next refresh address while an external processor or controller still determines how often the CBR request occurs.

The existing canonical case then used a 1999 Micron SDRAM product as a later comparison in which SELF REFRESH additionally internalizes recurring refresh clocking after explicit mode entry.

The risk is a misleading chronological impression:

```text
1980s
    internal address counter only
        ->
1990s SDRAM
    autonomous self-refresh
```

The early-1980s literature does not support that simple progression. A 1981 IEEE JSSC paper by Reese and colleagues already describes self-refresh implemented with an on-chip timer, arbiter, and refresh counter. A 1983 Mitsubishi/IECE paper explicitly concerns a 64-Kbit MOS DRAM with `auto/self refresh` functions, and later Mitsubishi patents cite that paper while reconstructing an architecture with an internal timer, refresh-address counter, control logic, and address multiplexer.

The correction is therefore not that Case 09's control decomposition was wrong. The correction is historical:

> **internal row enumeration and internal cadence were separable properties, but implementations combining them under a self-refresh regime were already part of early-1980s DRAM practice rather than a late-SDRAM invention.**

---

## Source and evidence boundary

### 1. Reese et al., IEEE JSSC, 1981

A bibliographic record for E. A. Reese, D. W. Spaderna, S. T. Flannagan, and F. Tsang appears in *IEEE Journal of Solid-State Circuits*, vol. 16, no. 5, 1981, pp. 479–487, DOI `10.1109/JSSC.1981.1051626`.

Multiple later patent references cite the work as `A 4K x 8 Dynamic RAM with Self Refresh`. Some modern indexing pages render the capacity in the title inconsistently, so this record does not use that discrepancy to make a capacity claim. The DOI, volume/issue, page range, authors, year, and self-refresh subject are the relevant anchors here.

The abstract as preserved by modern scholarly indexes states that self-refresh is implemented with:

- an on-chip timer;
- an arbiter;
- a refresh counter;
- a high-speed arbiter that resolves conflicts between refresh cycles and memory accesses;
- a `ready` output to the processor.

The full IEEE article was not directly inspected in this slice. Therefore detailed circuit claims beyond the abstract-level description are not promoted to page-level historical evidence.

### 2. Yamada et al., IECE / English translation, 1983

Michihiro Yamada and colleagues published `Auto/Self Refresh機能内蔵64Kbit MOSダイナミックRAM` in January 1983 in the Institute of Electronics and Communication Engineers of Japan. An English translation is indexed as `A 64Kbit MOS dynamic RAM with auto/self refresh functions`, *Electronics and Communications in Japan*, vol. 66, no. 1, pp. 103–110, DOI `10.1002/ECJA.4400660114`.

Modern bibliographic records summarize the article as discussing circuit provisions for automatic and self-refresh modes, with particular attention to an on-chip refresh-address counter and the timer used during self-refresh.

The original/translation full text was not directly rendered in this slice. The article's existence, date, title, DOI, and broad abstract-level scope are treated as period publication evidence; detailed mechanism reconstruction below is additionally checked against later Mitsubishi patents that explicitly identify the 1983 article as the source of the illustrated conventional refresh circuit.

### 3. Later Mitsubishi patent reconstruction of the 1983 circuit

US 5,251,176, filed in 1991 and assigned to Mitsubishi Electric, explicitly says that its Figure 3 refresh circuit is disclosed in Yamada et al.'s 1983 article.

The patent describes the cited circuit as containing:

- a refresh control circuit;
- a timer producing a refresh-request signal after a set interval;
- a refresh-address counter;
- a multiplexer choosing between external addresses and refresh-counter output.

It further describes a self-refresh episode in which, after the first refresh, the timer is activated; if the refresh instruction remains asserted beyond the timer's set interval, another refresh request is generated and the refresh address is advanced.

This is **later manufacturer-authored prior-art reconstruction**, not a substitute for direct page-level inspection of the 1983 paper. It is useful because the assignee and inventors are working in the same Mitsubishi DRAM lineage and explicitly attribute the depicted conventional circuit to the 1983 publication.

### 4. Mitsubishi 1990 patent statement about self-refresh autonomy

US 4,943,960 states that self-refresh had been `proposed and put into actual use` and identifies the 1983 Yamada article as an example. It describes the self-refresh cycle as one in which a timer and address counter built into the DRAM perform refresh automatically without externally supplied clock signals.

Again, this is a later retrospective manufacturer statement. It strengthens the functional interpretation of the earlier publication but does not by itself establish the first commercial product, first shipment date, or invention priority.

### 5. VLSI Technology's 1990-filed hidden-refresh patent as a later prior-art witness

US 5,193,072 distinguishes three earlier classes in its background:

1. externally managed DRAM refresh;
2. DRAMs with an internal refresh counter that still respond to an external refresh request, citing a 1981 Eaton et al. 64K DRAM;
3. DRAMs with a `self-refresh` mode that refresh without direction from external circuitry, citing the 1981 Reese et al. work.

The same patent says the cited self-refresh mode locks out memory accesses while the internal refresh operation proceeds.

This source is valuable as a later engineering taxonomy of prior art. It is **not** used to claim that the 1990 patent authors invented the categories or that every 1981 implementation behaved identically.

---

## Historical record

### H/P — an IEEE JSSC self-refresh implementation existed by 1981

The 1981 Reese et al. JSSC article provides a period publication anchor for a DRAM design whose self-refresh circuitry includes an on-chip timer, arbiter, and refresh counter.

The minimum defensible historical statement is therefore:

```text
by 1981
    DRAM self-refresh literature included
        internal refresh timing
        + internal refresh-row enumeration
        + arbitration with ordinary access
```

This does not establish the first self-refreshing DRAM. Earlier self-refreshing-memory patents and quasi-static RAM work existed, and a priority claim would require a separate genealogy.

### H/P — early self-refresh was not necessarily an access-transparent background operation

The later VLSI prior-art account describes the Reese-style self-refresh mode as refreshing without external direction while locking out ordinary memory access.

That evidence matters because `autonomous refresh` and `concurrent service` are different properties:

```text
internal cadence authority
    != refresh invisibility to access
    != simultaneous normal service
```

The 1981 JSSC abstract's explicit arbiter/`ready` interface also shows that conflict management between refresh and access was part of the design problem, even though this slice does not reconstruct the exact arbitration policy from the full paper.

### H/P — the 1983 Mitsubishi publication explicitly joined AUTO and SELF refresh in one DRAM discussion

The 1983 Yamada et al. title itself places `auto/self refresh` together. Later Mitsubishi descriptions of the cited circuit distinguish an externally initiated refresh path from a self-refresh path whose timer keeps producing requests while the self-refresh condition remains active.

The important period boundary is therefore not simply:

```text
external refresh
    vs internal refresh
```

but at least:

```text
external timing + external or internal row enumeration

external refresh-mode entry/request
    + internal recurring timing
    + internal row enumeration
```

### H/P — timer state and refresh-counter state are distinct control functions

US 5,251,176's explicit reconstruction of the Yamada circuit separates:

- the timer, which determines when another refresh request becomes due;
- the refresh-address counter, which determines which row is selected next;
- the multiplexer, which chooses the maintenance-address path instead of the normal external-address path;
- the refresh-control circuit, which coordinates the mode and sequence.

This later manufacturer reconstruction makes the Case-09 analytical decomposition historically concrete:

```text
when to refresh
    != which row to refresh
    != which address source currently has authority
```

### H/P — self-refresh remained a powered retention regime

The Mitsubishi later patent literature discusses self-refresh in low-power and battery-backed contexts. That framing does not turn DRAM into a nonvolatile medium.

The bounded relation is:

```text
main system can relinquish ordinary refresh clock/control
    while
DRAM remains supplied sufficiently for internal refresh
```

not:

```text
DRAM retains payload with no electrical power
```

The payload remains dynamic charge state whose survival still depends on repeated restoration.

---

## Retained-state / control-state decomposition

This slice exposes at least six distinct state or control relations.

### 1. Payload charge state

The logical data remains embodied in dynamic cell state and still has a finite retention interval.

### 2. Self-refresh mode condition

Some external event or sustained control condition places the device into the regime in which internal recurrence is allowed to continue.

This is control state, not user payload.

### 3. Timer / oscillator state

The internal timing circuit establishes when a subsequent refresh request should occur.

Its exact physical phase need not be externally observable for it to be constitutive of the maintenance episode.

### 4. Refresh-address-counter phase

The counter determines which row is next in the coverage sequence.

This is a different state from the timer phase.

### 5. Address-source selection

The device must select the internal refresh address rather than the external service address during the refresh operation.

### 6. Arbitration / service availability state

If normal access can conflict with maintenance, the device or interface needs some rule for deciding whether refresh proceeds, access proceeds, or the requester waits.

The 1981 abstract's arbiter and `ready` output make this boundary visible.

The resulting decomposition is:

```text
payload state
    != self-refresh mode state
    != refresh-timer state
    != refresh-coverage position
    != address-source authority
    != access/maintenance arbitration state
```

These states can have different persistence horizons and different visibility at the package boundary.

---

## Engineering reconstruction

### E — Case 09's architectural distinction survives, but its historical ordering must be corrected

The TI CBR evidence still proves:

```text
internal refresh address counter
    != internal refresh scheduler
```

The new early-self-refresh evidence adds:

```text
1981–1983 implementations could also combine
    internal timer
    + internal refresh counter
    + internal control/arbitration
```

Therefore the correct history is not a single ladder in which one function moved on-chip only after another had done so.

A safer representation is a design-space view:

```text
external cadence + external row enumeration

external cadence + internal row enumeration

internal cadence during self-refresh + internal row enumeration
```

At least the latter two control partitions were present in early-1980s technical literature.

### E — `self-refresh` names a regime, not a claim of total system autonomy

Even in an internally timed self-refresh design, several dependencies remain:

- sufficient electrical power;
- a valid mode-entry/control condition;
- functioning internal timer and row-coverage machinery;
- device timing/electrical margins;
- a defined handoff back to normal service.

So:

```text
self-refresh
    != self-powered
    != nonvolatile
    != independent of mode control
    != maintenance-free
```

### E — internalizing cadence relocates the maintenance deadline, not the physical need for maintenance

The physical reason for periodic restoration remains cell leakage. What changes is who owns the recurring trigger.

In an externally timed regime, system/controller logic must repeatedly make refresh happen before the deadline. In self-refresh, the device's timer takes over that obligation for the duration of the mode.

Thus:

> **retention obligation can remain physically unchanged while the authority for discharging it moves across the device boundary.**

### E — battery backup is infrastructure substitution, not quiescent retention

If ordinary system power/control is withdrawn while backup power keeps the DRAM and self-refresh circuitry operating, the maintenance infrastructure has changed without the payload becoming passive.

The useful distinction is:

```text
source of power changed
    != need for power disappeared

source of refresh cadence changed
    != need for refresh disappeared
```

This is particularly important because `system powered down` in a datasheet or product discussion can otherwise be mistaken for `memory array unpowered`.

### E — arbitration and refresh autonomy are orthogonal

An internal timer can decide that refresh is due, but a separate policy is still required if an external access arrives at the same time.

The 1981 paper's abstract-level timer/arbiter/counter decomposition therefore supports:

```text
maintenance trigger authority
    != conflict-resolution policy
```

A design may be autonomous about when refresh is due while still exposing wait/ready behavior to the host.

---

## Functional comparison to the existing Case-09 evidence

### A — 1981 self-refresh vs TI 1984-filed CBR counter

The comparison is functional, not genealogical.

```text
Reese et al. 1981 self-refresh
    on-chip timer
    on-chip refresh counter
    arbiter / ready relation

TI 1984-filed CBR-counter design
    on-chip refresh counter
    external processor/controller controls CBR frequency
```

The useful result is a counterexample to any story that equates `early-1980s DRAM` with one unique control partition.

### A — 1983 auto/self-refresh vs Micron 1999 SDRAM AUTO/SELF REFRESH

Both source sets distinguish an externally controlled refresh regime from a self-refresh regime with internal recurrence.

That supports a bounded functional comparison:

```text
auto refresh
    external recurrence authority

self refresh
    internal recurrence authority after entry
```

But the interfaces differ substantially. The 1983 circuit is described through a dedicated refresh instruction/control scheme; the 1999 SDRAM uses synchronous command semantics and CKE/tXSR rules.

Therefore:

```text
similar control partition
    != identical signaling
    != identical state machine
    != direct standardization lineage
```

### A — relation to Case 03

Case 03 explains why DRAM requires deadline-driven restoration. This slice shows one way the scheduling responsibility can be internalized.

Case 03 remains the physical-retention grounding; Case 09 remains the control-locus case.

---

## Philosophical / media-theoretical boundary

### I — apparent autonomy can be produced by hidden infrastructure

The technical fact is narrow: an internal timer and refresh counter can continue maintenance after the host relinquishes recurring control.

That makes the memory appear more self-sustaining at the system interface, but the appearance is produced by additional internal machinery and continuing power.

A defensible conceptual formulation is:

> **maintenance can become less visible to one observer by being relocated into the retained object's supporting apparatus.**

This does not establish a general philosophical concept of autonomy, agency, or self-maintenance. It only disciplines such language with the actual control and power dependencies.

### I — `rest` is observer-relative

A host may be idle or powered down while the DRAM continues cyclic internal work. Conversely, a payload can appear unchanged while timer, counter, and refresh circuits repeatedly act on it.

The case therefore reinforces the repository's warning:

```text
interface quiescence
    != physical quiescence
```

without implying that every retained state is continuously active.

---

## Explicit non-claims

This evidence record does **not** claim that:

1. Reese et al. invented DRAM self-refresh;
2. 1981 is the first use of the phrase `self-refresh`;
3. the exact title/capacity discrepancy in modern indexes for the Reese paper has been definitively resolved here;
4. the full 1981 JSSC paper was directly page-inspected in this slice;
5. the full 1983 Japanese or English article was directly page-inspected in this slice;
6. Mitsubishi's 1991-filed patent reproduces every circuit detail of the 1983 publication without modification;
7. a later patent's prior-art summary is equivalent to a contemporary 1983 product manual;
8. the 1983 paper establishes a first commercial shipment;
9. `put into actual use` establishes which exact product first shipped with self-refresh;
10. self-refresh makes DRAM nonvolatile;
11. `system powered down` means the DRAM receives zero power;
12. internal refresh timing eliminates the retention deadline;
13. internal refresh timing eliminates the need for refresh-address coverage;
14. internal refresh timing implies transparent simultaneous access;
15. an on-chip timer proves one particular oscillator topology;
16. Reese 1981, Yamada 1983, TI's 1984-filed CBR patent, and Micron 1999 SDRAM form a demonstrated direct genealogy;
17. the same term `self-refresh` implies identical command semantics across these designs;
18. a functional similarity between early self-refresh and later SDRAM SELF REFRESH proves standards continuity;
19. all early-1980s DRAMs provided self-refresh;
20. all self-refresh designs used the same timer period, power source, arbitration policy, or counter initialization rule.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| A Reese et al. self-refresh DRAM paper appeared in IEEE JSSC in 1981, vol. 16 no. 5, pp. 479–487, DOI `10.1109/JSSC.1981.1051626` | H/P | strong bibliographic record; full text not directly inspected in this slice |
| The indexed abstract describes self-refresh using an on-chip timer, arbiter, and refresh counter | H/P | abstract-level publication metadata; no page-level circuit reconstruction claimed |
| A Yamada et al. `64Kbit MOS dynamic RAM with auto/self refresh functions` paper appeared in January 1983 and has English DOI `10.1002/ECJA.4400660114` | H/P | strong bibliographic record; full text not directly inspected here |
| Later Mitsubishi patents explicitly attribute a timer + refresh-counter + multiplexer refresh circuit to the 1983 Yamada paper | H/P | strong later manufacturer prior-art reconstruction |
| In the cited conventional self-refresh architecture, the timer determines recurrence while the counter supplies successive refresh addresses | H/P/E | explicit in later Mitsubishi reconstruction; used conservatively for the attributed architecture |
| Mitsubishi later described self-refresh as operating without externally supplied refresh clocks | H/P | manufacturer patent retrospective; not a first-invention claim |
| VLSI Technology's 1990-filed patent distinguishes external refresh, internal-counter/external-request refresh, and self-refresh as earlier design classes | H/P | later patent prior-art taxonomy |
| Internal refresh addressing and internal refresh cadence are separable properties | E | supported by contrast among TI CBR and early self-refresh evidence |
| Autonomous self-refresh existed in early-1980s DRAM technical literature before the 1999 SDRAM witness | H/P | strong at publication level; no direct lineage asserted |
| Early self-refresh proves DRAM became nonvolatile | X | rejected: dynamic payload still depends on powered periodic restoration |
| Main-system power-off language proves zero power at the DRAM | X | rejected: backup/self-refresh regimes preserve power to the retention apparatus |
| Similar AUTO/SELF control partitions prove the 1983 and 1999 interfaces are identical | X | rejected: only a functional comparison is made |
| Historical coexistence of CBR and self-refresh proves one descended from the other | X | unsupported genealogy |
| Internal timer state, counter phase, mode state, and payload are one retained state | X/E | rejected by control-state decomposition |

---

## What this changes in Case 09

The canonical case should retain its central control decomposition but revise the chronology around the 1999 successor comparison.

Before this deepening, the narrative could be read as:

```text
1980s CBR
    internal row counter, external cadence
        ->
1999 SDRAM SELF REFRESH
    internal cadence too
```

After this deepening, the defensible map is:

```text
early 1980s design space already includes at least:

    external recurrence + internal refresh address

    internal recurrence in self-refresh + internal refresh address

later SDRAM
    standard/product command semantics reorganize those authority relations
    within a synchronous interface
```

The novelty of the 1999 Case-09 comparison is therefore **not** `first autonomous self-refresh`. Its value is the clean, directly documented product-level contrast between SDRAM AUTO REFRESH and SELF REFRESH under one command architecture, including mode entry/exit and shared row-counter semantics.

---

## Remaining evidence debt

1. Directly inspect the full IEEE JSSC PDF for DOI `10.1109/JSSC.1981.1051626`, including the exact published title/capacity and timer/arbiter/counter figures.
2. Directly inspect the 1983 Japanese paper and/or the English translation DOI `10.1002/ECJA.4400660114` at page level.
3. Establish whether a named commercial DRAM corresponding to the 1981 or 1983 papers can be documented through a contemporary datasheet rather than later patent recollection.
4. Separate publication, prototype, production, and shipment chronology before making any commercial-first claim.
5. Trace earlier self-refreshing-memory patents and the 1979 quasi-static-RAM literature only if a first-introduction genealogy becomes important; that broader history belongs primarily in `computing-archaeology`.
6. If standards history becomes necessary, trace JEDEC self-refresh command semantics independently rather than inferring them from vendor papers.

---

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `CAS-before-RAS` found no dedicated case to reuse.

The broader history of quasi-static RAM, early self-refresh prototypes/products, ISSCC/JSSC publication genealogy, DRAM controller integration, and later JEDEC standardization belongs primarily there.

This repository keeps the retention-specific result:

> **refresh deadline, cadence authority, row-coverage state, address-source authority, and access arbitration are distinct relations, and early DRAM designs distributed them across the chip boundary in more than one way.**

---

## Sources

1. E. A. Reese, D. W. Spaderna, S. T. Flannagan, F. Tsang, self-refresh DRAM paper, *IEEE Journal of Solid-State Circuits* 16(5), 1981, pp. 479–487, DOI `10.1109/JSSC.1981.1051626`: <https://doi.org/10.1109/JSSC.1981.1051626>.
2. Bibliographic record preserving the `A 4Kx8 dynamic RAM with self-refresh` title, authors, volume/issue/pages and DOI: <https://eurekamag.com/research/080/945/080945698.php>.
3. Michihiro Yamada et al., `A 64Kbit MOS dynamic RAM with auto/self refresh functions`, *Electronics and Communications in Japan*, vol. 66, no. 1, January 1983, DOI `10.1002/ECJA.4400660114`: <https://doi.org/10.1002/ECJA.4400660114>.
4. Takahiro Komatsu, `Dynamic type semiconductor memory device with a refresh function and method for refreshing the same`, US 5,251,176, Mitsubishi Electric, filed 27 August 1991; Figure-3 prior-art discussion explicitly attributes timer/counter/multiplexer architecture to Yamada et al. 1983: <https://patents.google.com/patent/US5251176A/en>.
5. Masaki Kumanoya et al., `Self-refreshing of dynamic random access memory device and operating method therefor`, US 4,943,960, Mitsubishi Electric, granted 24 July 1990; background describes timer + address counter self-refresh without external refresh clocks and cites Yamada et al. 1983: <https://patents.google.com/patent/US4943960A/en>.
6. Gerald Lee Frenkil and Steven E. Golson, `Hidden refresh of a dynamic random access memory`, US 5,193,072, VLSI Technology, filed 21 December 1990; background distinguishes external refresh, internal-counter refresh, 1981 Reese self-refresh, and quasi-static RAM: <https://patents.google.com/patent/US5193072A/en>.
7. European Patent Office, EP0509811B1 prior-art page preserving bibliographic entries for the 1982 Kung self-refresh paper and 1983 Yamada auto/self-refresh paper: <https://data.epo.org/publication-server/rest/v1.2/publication-dates/19981202/patents/EP0509811NWB1/document.pdf>.
