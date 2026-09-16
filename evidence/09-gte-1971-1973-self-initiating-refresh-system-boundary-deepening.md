# Evidence 09 — GTE 1971–1973 self-initiating refresh system-boundary deepening

**Status:** `bounded deepening complete`

**Parent case:** [`../cases/09-dram-cbr-refresh-address-internalization.md`](../cases/09-dram-cbr-refresh-address-internalization.md)

**Earlier adjacent record:** [`09-1973-1982-early-self-refresh-control-partitions-prior-art-deepening.md`](09-1973-1982-early-self-refresh-control-partitions-prior-art-deepening.md)

**Bounded question:** what does GTE's US3729722A actually mean by `self-initiating refresh`, and does its April-1973 publication establish device-local/on-chip autonomous refresh earlier than the already-grounded 1973–1982 Case-09 prior art?

This record closes one explicit debt from the earlier prior-art slice by directly inspecting the primary patent text. The result is a useful correction rather than a simple earlier-date claim: **the GTE patent is an early public witness for automatically recurring refresh at the memory-system level, but its preferred embodiment keeps the refresh clock, pulse generator, row counter, gating, and busy/service logic outside the commercial DRAM chips it refreshes.**

Accordingly, the title phrase `self-initiating refresh` must not be silently read as `on-chip self-refresh`.

---

## Result in one sentence

GTE's US3729722A, filed **17 September 1971** and published/granted **24 April 1973**, describes a free-running system-level refresh controller around commercial Intel 1103 dynamic-memory chips: an external clock triggers a refresh pulse generator, a separate row-address counter advances across rows, gating substitutes the refresh address for the ordinary address, and a `memory busy` relation defers external accesses during refresh.

The bounded chronology therefore becomes:

```text
1973-04-24 GTE public patent
    self-initiating recurring refresh at memory-system level
    + external/system refresh clock
    + external/system row counter
    + address-path gating
    + explicit busy/defer service boundary
    != on-chip refresh control

1973-06-05 MOS Technology public patent
    self-refreshing memory
    + row-specific refresh-age/deadline evidence
    + mandatory/opportunistic refresh

1980 TI public patent
    refresh-row counter/address mux moved onto DRAM chip
    + recurring refresh request still external

1982 TI public patent
    internal recurring timing
    + internal row enumeration
    + access/refresh arbitration
```

This is a control-partition chronology, not a proof of invention priority or direct implementation lineage.

---

## Primary sources and provenance

### 1. GTE Automatic Electric Laboratories, US3729722A

- Title: `Dynamic mode integrated circuit memory with self-initiating refresh means`.
- Inventor: Joseph Patrick Shuba.
- Original assignee: GTE Automatic Electric Laboratories Incorporated.
- Filed / priority: **17 September 1971**.
- Public patent date: **24 April 1973**.
- Application: `US00181443A` / No. `181,443`.
- Direct text inspected: <https://patents.google.com/patent/US3729722A/en>

The public transcript contains the abstract, description, preferred embodiment, and eight claims. The patent's own summary says a dynamic integrated-circuit memory is supplied with a clock-controlled refresh pulse generator, address counter, and gating arrangement so that each memory cell is periodically refreshed.

The critical implementation detail is not merely the title. The preferred embodiment explicitly uses **commercial Intel 1103 MOS memory chips** and then describes separate refresh components around them:

- a free-running clock / crystal-controlled oscillator;
- a refresh pulse generator, for which an SN74121 monostable multivibrator is given as an example;
- a row-address counter, for which SN74163 binary counters are given as examples;
- gating between the ordinary row-address register and the refresh-counter path;
- a `memory busy` signal while refresh owns the array interface.

The claims are framed as a refresh apparatus **in combination with** an integrated-circuit dynamic-memory system. They do not require the clock, refresh pulse generator, or row counter to be fabricated in the same semiconductor body as the dynamic cells.

Therefore this is direct primary evidence for system-level automatic refresh control, not evidence that the 1103 chip itself contained the refresh controller.

### 2. Texas Instruments, US4207618A

- Title: `On-chip refresh for dynamic memory`.
- Inventors: Lionel S. White, Jr.; G. R. Mohan Rao.
- Filed / priority: **26 June 1978**.
- Public patent date: **10 June 1980**.
- Direct text inspected: <https://patents.google.com/patent/US4207618A/en>

TI's background section is valuable as a later manufacturer-authored contrast. It describes conventional dynamic RAM systems as requiring external refresh systems containing a refresh-address counter, a system interrupt mechanism, and a timer. It then states the invention's different boundary: the refresh-address counter and address multiplexing are incorporated on the dynamic-RAM chip, leaving an external refresh command to initiate each event.

The Google Patents family/citation record for US4207618A lists US3729722A among its cited prior-art families. That formal citation relation is useful provenance, but it is not treated here as proof that GTE directly caused TI's design.

---

## Historical record

### H/P — `self-initiating` is already public vocabulary in April 1973

US3729722A was published on 24 April 1973, several weeks before the 5 June 1973 publication of MOS Technology's US3737879.

The narrow vocabulary conclusion is therefore:

```text
by 1973-04-24
    public patent vocabulary includes
    `self-initiating refresh`
```

This does **not** establish that GTE coined the phrase, invented automatic refresh, or was the first actor to build such a controller. It establishes only a checked public-document floor for this wording in the current source set.

### H/P — the GTE preferred embodiment is a memory-system controller around commercial DRAM chips

The patent describes its refresh arrangement with reference to commercially available Intel 1103 chips. In that illustrative system, the memory chips provide the dynamic array and normal memory circuitry, while the patent's refresh clock, pulse generator, row-address counter, gating, and busy relation are described as surrounding system circuitry.

The bounded relation is:

```text
self-initiating refresh system
    != self-refreshing DRAM chip
```

This directly blocks a title-only reading of the patent.

### H/P — a free-running clock supplies recurring cadence

The GTE embodiment uses a free-running clock operating whenever power is applied to the memory system. That clock triggers the refresh pulse generator at a rate chosen so every row is serviced within the device's refresh interval.

For the patent's Intel-1103 example, the document uses:

- 32 rows;
- a stated requirement that all bits be refreshed within 2 ms;
- a 16 kHz refresh clock;
- one refresh pulse every 62.5 microseconds.

Those values are the patent's worked example, **not universal DRAM constants**.

The historical control partition is:

```text
external requester / CPU
    does not issue each refresh event

memory-system refresh controller
    generates recurring refresh cadence automatically
```

### H/P — row enumeration is also system-level in the preferred embodiment

Each refresh pulse steps a binary row-address counter. The counter advances sequentially and its address is selected through gating during a refresh period.

During ordinary service, the external row-address register supplies the address. During refresh, the counter's row address takes authority over the row-address drivers.

Thus the preferred embodiment already separates:

```text
service address source
    != maintenance address source
```

but the maintenance address source is still **outside the commercial DRAM chips** used in the example.

### H/P — refresh can block service even when initiation is automatic

The GTE patent maintains a `memory busy` signal during refresh and states that the memory will not respond to external addressing during that interval. If external circuits attempt a memory access during a refresh cycle, that access is deferred until refresh completes.

The document characterizes the maximum deferral as one refresh period / one ordinary memory cycle in the described arrangement.

Therefore:

```text
refresh automatically initiated
    != refresh invisible to service timing
    != simultaneous ordinary access guaranteed
```

Automation removes the need for an external requester to schedule each event; it does not remove array occupancy.

### H/P — simultaneous same-row refresh across multiple chips is a system-level optimization

The refresh pulse generator is described as activating the memory circuitry so that the selected row is refreshed across all memory chips at once. The patent presents this as faster than refreshing chips one at a time.

This matters because `which row is maintained` and `which chip is maintained` are separate geometry choices. In this design a shared system-level row address can service the same row position across a bank of chips simultaneously.

---

## Retained-state and control-state decomposition

The GTE patent adds a useful early control partition to Case 09.

### 1. Payload state

The Intel-1103-class dynamic cells retain electrical charge only for a bounded interval and require periodic reconstruction.

### 2. Recurrence / cadence state

A free-running oscillator and pulse generator determine when the next maintenance event occurs.

This is not application payload.

### 3. Coverage / traversal state

The row-address counter records which refresh row comes next in the sequential traversal.

Again, this is maintenance-control state rather than user data.

### 4. Address-source authority

The gating network decides whether ordinary external row-address state or the refresh-counter state currently reaches the row-address drivers.

### 5. Service-admission state

The `memory busy` relation signals that ordinary external addressing must wait while refresh occupies the memory cycle.

These states/relations jointly produce retention service without being stored inside the DRAM cell array itself.

---

## Engineering reconstruction

### E — `automatic` and `on-chip` are independent axes

The direct inspection exposes a two-axis distinction that title-level chronology can hide:

```text
axis 1: who supplies recurring refresh cadence?
    requester/controller manually or explicitly
    vs dedicated automatic timing logic

axis 2: where is that logic located?
    board / memory system
    vs memory device / semiconductor body
```

GTE 1973 occupies:

```text
automatic recurring cadence
    + system-level row enumeration
    + system-level address gating
```

TI 1980 occupies:

```text
external recurring command
    + on-chip row enumeration
```

TI 1982 supplies a later patent witness for:

```text
on-chip recurring cadence
    + on-chip row enumeration
```

Therefore:

> **refresh autonomy != refresh-control integration.**

A maintenance obligation can be automated before its machinery is moved into the component being maintained.

### E — `self-initiating` is observer-relative

The GTE controller is `self-initiating` relative to the processor or external requester because a free-running refresh clock creates events without one refresh command per cycle.

It is not `self-initiating` in the stronger later sense of a DRAM chip internally generating both refresh timing and maintenance addresses.

A defensible reconstruction is:

```text
self-initiating at memory-system boundary
    != self-initiating at DRAM-package boundary
```

This is exactly why period vocabulary must be attached to a control boundary rather than mapped directly to a timeless category.

### E — hidden maintenance can move outward as well as inward

Case 09 often asks what happens when refresh work moves into the chip. The GTE case supplies the complementary architecture: a dedicated memory-system controller can hide recurring refresh work from the CPU even though that work remains physically outside the memory chips.

So `hidden from CPU` does not specify `inside DRAM`.

### E — automatic cadence still depends on powered infrastructure

The free-running oscillator operates while power is applied to the memory system. If the refresh controller loses the power/clock conditions required for recurrence, the dynamic payload does not become nonvolatile merely because normal request logic is absent.

Thus:

```text
processor-independent recurrence
    != infrastructure-independent retention
    != unpowered retention
```

### E — service deferral is part of the retention contract

The `memory busy` behavior shows that maintenance can be autonomous yet still expose a scheduling cost at the service boundary.

A useful decomposition is:

```text
refresh initiation hidden from requester
    != refresh occupancy hidden from requester
```

The requester may not schedule maintenance, but it can still experience the consequence that an access waits.

---

## Functional comparisons

The following are **functional analogies only** unless a primary-source citation relation is explicitly stated.

### A — GTE 1973 vs TI 1980

The two patents isolate opposite halves of the later automation story:

```text
GTE 1973 preferred embodiment
    internal-to-memory-system cadence
    external-to-DRAM enumeration

TI 1980
    external cadence / refresh command
    internal-to-DRAM enumeration
```

This is a particularly useful counterexample to a one-dimensional `more automatic = more integrated` narrative.

The TI patent corpus formally cites the GTE patent as prior art. That establishes a document-level relation, not an implementation genealogy.

### A — GTE 1973 vs MOS Technology 1973

Both patents use language that can look `self-refresh`-like to a modern reader, but they solve the control problem differently.

GTE's preferred embodiment uses a global free-running cadence plus cyclic row counter. MOS Technology's US3737879, as grounded in the adjacent evidence record, uses row-specific refresh-age/deadline state, mandatory refresh, and optional opportunistic refresh.

Therefore:

```text
similar early-1970s autonomy vocabulary
    != identical maintenance evidence
    != identical scheduler geometry
    != proven shared implementation lineage
```

### A — GTE `memory busy` vs TI 1982 `invisible to CPU`

Both systems can relieve the CPU from generating every refresh event, yet their interface handling differs. GTE explicitly exposes a busy/defer relation during refresh; TI's later internally clocked patent frames refresh as invisible to CPU while still allowing an access arriving after refresh begins to wait until maintenance completes.

The bounded comparison is:

```text
control-message invisibility
    != latency invisibility
```

No direct descent is asserted.

---

## Philosophical interpretation

### I — automation can relocate obligation without relocating machinery into the maintained object

The exact technical fact is that GTE's controller can initiate refresh independently of ordinary request traffic while remaining external to the DRAM chips it maintains.

A bounded interpretation is:

> an operation may become `automatic` because responsibility has moved from a requester to dedicated infrastructure, not because the retained object has become self-sufficient.

The interpretive limit is important. This does not imply that all persistence is active maintenance, that every hidden controller is philosophically a subject, or that technical autonomy is equivalent to agency.

### I — the boundary of the object changes the description of autonomy

At the CPU boundary, the GTE memory subsystem can appear to maintain itself. At the DRAM-chip boundary, the same arrangement is externally refreshed.

Thus the technical description `self-initiating` is partly boundary-relative. That observation disciplines later philosophical language about autonomy: the first question must be **which system boundary is being used?**

---

## Chronology discipline

The dates in this record are separated by evidentiary role:

```text
GTE US3729722A
    filed / priority 1971-09-17
    public patent 1973-04-24

MOS Technology US3737879
    filed 1972-01-05
    public patent 1973-06-05

TI US4207618A
    filed / priority 1978-06-26
    public patent 1980-06-10
```

The GTE filing date is historically relevant to the patent record, but this repository still uses **24 April 1973** as the checked public-document date for its mechanism claims.

The earlier filing date does not establish first invention in the broader technical field, because this slice does not audit confidential work, foreign filings, all related patent families, conference disclosures, products, or laboratory prototypes.

---

## Terminology consequence

Direct inspection changes the earlier evidence debt in a nontrivial way.

Before inspection, the title `Dynamic mode integrated circuit memory with self-initiating refresh means` could be misread as evidence for an earlier chip-local self-refresh architecture.

After inspection, the safer vocabulary map is:

```text
`self-initiating refresh` (GTE 1973)
    = automatic recurring refresh at the disclosed memory-system boundary
    != proof of on-chip refresh control

`on-chip refresh` (TI 1980)
    = refresh-address counter/address mux placed in semiconductor memory device
    while recurring refresh command remains external

`invisible to CPU` (TI 1982)
    = internally recurring refresh in the disclosed device
    with service collision handled by delay/latching

later `SELF REFRESH`
    = must be read from its own device/interface contract
```

Therefore:

> **historical autonomy vocabulary does not by itself identify the physical location of maintenance control.**

---

## Explicit non-claims

This record does **not** claim that:

1. GTE invented dynamic-memory refresh;
2. GTE invented automatic refresh;
3. `self-initiating refresh` first appeared in April 1973;
4. the 17 September 1971 filing date is a public-disclosure date;
5. the Intel 1103 itself contained GTE's refresh clock or row counter;
6. GTE's preferred embodiment is an on-chip self-refresh DRAM;
7. every implementation covered by the patent claims had to use the exact SN74121/SN74163 examples;
8. 16 kHz, 62.5 microseconds, or 2 ms are universal DRAM refresh constants;
9. automatically initiated refresh is transparent to all observers;
10. a `memory busy` indication is equivalent to later SDRAM command semantics;
11. the GTE row counter is equivalent to MOS Technology's per-row refresh-age counters;
12. the TI 1980 patent's citation of GTE proves direct engineering influence;
13. GTE 1973 → TI 1980 → TI 1982 is a demonstrated genealogy;
14. the GTE patent establishes a shipped GTE DRAM product;
15. CPU-visible autonomy implies unpowered retention;
16. a memory subsystem and an individual DRAM chip have the same autonomy boundary.

---

## Source-strength ledger

| Claim | Source | Strength | Boundary |
|---|---|---|---|
| GTE filing/publication dates, title, inventor, assignee | US3729722A direct patent transcript | H/P* | public patent metadata/transcript |
| preferred embodiment uses commercial Intel 1103 chips | US3729722A description | H/P* | patent embodiment, not proof of GTE product shipment |
| free-running clock triggers periodic refresh pulses | US3729722A description/claims | H/P* | system-level disclosed apparatus |
| SN74121 pulse generator and SN74163 counter examples | US3729722A preferred embodiment | H/P* | examples, not universal claim limits |
| refresh counter supplies sequential maintenance row | US3729722A description/claims | H/P* | preferred architecture/claims |
| `memory busy` defers external accesses during refresh | US3729722A description | H/P* | disclosed service contract |
| GTE controller is not evidence of on-chip self-refresh | direct component-placement comparison | E | engineering reconstruction from patent architecture |
| TI contrasts external refresh overhead with on-chip counter/mux | US4207618A background/summary/claims | H/P* | TI patent disclosure |
| US4207618A cites US3729722A | patent-corpus citation record | H/P | document relation only |
| `automatic` and `on-chip` are independent axes | GTE/TI cross-source comparison | E/A | mechanism comparison, not genealogy |

`H/P*` marks directly inspected primary patent text through a reliable public HTML transcript rather than an origin-hosted, page-stable USPTO facsimile in this slice.

---

## Related-repository check

`tmzncty/computing-archaeology` was checked before expanding this slice. Its semiconductor-memory overview, [`docs/memory/why-semiconductor-ram-became-a-hierarchy.md`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-semiconductor-ram-became-a-hierarchy.md), already supplies the broad constraint-first account: dynamic cells trade local circuitry for density and therefore require controller work for sensing/restoration/refresh.

That companion file does **not** currently provide a dedicated GTE-US3729722 control-boundary history. This record therefore keeps only the retention-specific distinction needed by Case 09:

```text
automatic recurrence
    != device-local recurrence
```

A broader history of early-1970s refresh-controller boards, Intel 1103 system design, vendor competition, component costs, or influence genealogy belongs primarily in `computing-archaeology` if developed later.

---

## Navigation / status update

This slice closes the first remaining-evidence item in [`09-1973-1982-early-self-refresh-control-partitions-prior-art-deepening.md`](09-1973-1982-early-self-refresh-control-partitions-prior-art-deepening.md): the GTE patent has now been directly inspected.

The result is **not** `earlier on-chip self-refresh found`. The closed debt should instead be summarized as:

> US3729722A is an April-1973 public witness for self-initiating, free-running **memory-system-level** refresh around commercial dynamic-memory chips; it is a terminology/control-partition prior-art witness and a negative control against equating `self-initiating` with `on-chip`.

Case 09 remains **`grounded`**. This evidence changes the chronology and vocabulary boundary but does not by itself justify a maturity promotion.

---

## Remaining evidence debt

The most useful next work is narrower than before:

1. directly inspect contemporaneous Intel 1103 manufacturer documentation if a future claim needs to separate the patent's worked 2 ms / 32-row assumptions from the exact revision-specific Intel product contract;
2. audit whether any pre-24-April-1973 public source uses comparable `self-refresh` / `self-initiating` vocabulary before making a first-use claim;
3. identify named commercial products, if any, implementing GTE's disclosed external automatic-refresh controller rather than inferring shipment from a patent;
4. keep the GTE→TI formal citation relation separate from any stronger influence genealogy;
5. preserve the separate MOS-Technology row-age/deadline architecture rather than collapsing all 1973 autonomy evidence into one scheduler family.

None of these debts blocks the bounded conclusion of this record.