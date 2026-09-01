# Static MOS RAM: Powered Quiescence in a Semiconductor Array

## Scope

- **Status:** `first-pass`.
- **Object / system:** a bounded 1968–1975 static-MOS semiconductor-memory bridge. Intel 1101/1101A, 2102, and 5101/5101L documentation supplies product/array behavior; Vadasz–Chua–Grove (1971) supplies period Intel vocabulary; NASA-CR-108672 (1970) and Fairchild US3530443A (filed 1968, published 1970) supply period cell-level witnesses without being silently relabeled as Intel product schematics.
- **Date range:** 1968–1975 for this bounded bridge.
- **Primary question:** what changes, and what does not, when regenerative bistable retention moves from the grounded thermionic flip-flop case into monolithic semiconductor memory arrays?
- **Why this case matters:** Case 06 established powered bistable working retention without scheduled refresh. Static semiconductor memory tests whether that distinction survives integration, array addressing, package-level read/write semantics, finite electrical margins, and low-power standby/data-retention modes.

This is **not** a general history of SRAM, bipolar scratchpad memory, cache, register files, CMOS scaling, or the modern six-transistor SRAM cell. Cache policy and hierarchy semantics remain intentionally excluded. A modern `6T SRAM` description must not be projected onto every 1968–1975 static MOS device without a cell-specific primary source.

Source-deepening record: [`../evidence/07-fairchild-static-mos-regime-deepening.md`](../evidence/07-fairchild-static-mos-regime-deepening.md).

---

## Related-repository check

Fresh code searches in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `SRAM`, `static random access memory`, `static RAM`, and `Intel 1101` still find no dedicated static-semiconductor-memory case to reuse. That repository already identifies semiconductor memory as a historical gap and remains the preferred home for any broad engineering history.

The contribution here is narrower: establish a retention-specific bridge from regenerative state holding to a decoded semiconductor-memory array, then stop before cache or generic semiconductor-memory history.

---

## Historical vocabulary

### 1968–1970 — `flip-flop`, cross-coupling, and `static storage`

Fairchild patent US3530443A, filed 27 November 1968 and published 22 September 1970, describes the then-typical semiconductor memory cell as a flip-flop plus gating elements. For its MOS discussion it describes two MOS transistors with cross-coupled gate/drain relations as the stability-producing storage portion and develops a four-active-device cell in which two additional MOS devices also serve load/gating functions.

The patent is particularly useful because it does not treat `static` as a timeless name for a transistor count. The disclosed cell family is discussed under several operating regimes, including `static storage` and `dynamic storage`, and under separate standby, address, read, and write conditions.

**Primary anchor:** Harold S. Crafts, Wendell B. Sander, James B. Angell, “MOS gated resistor memory cell,” US Patent 3,530,443, filed 27 November 1968, published 22 September 1970: <https://patents.google.com/patent/US3530443A/en>.

### 1971 — `static MOS memory`, `MOS flip-flops for storage`, Intel 1101

L. L. Vadasz, H. T. Chua, and A. S. Grove of Intel, writing in the May 1971 issue of *IEEE Spectrum*, describe a semiconductor-memory approach using MOS flip-flops for storage. Indexed period-page text locates their discussion of a commercially available `static MOS memory cell` on p. 43 and their fully decoded static-MOS / Intel `1101` system-expansion example on p. 47.

This source matters because the bridge from Case 06 to static semiconductor memory is not only a modern functional analogy: period engineers themselves used `flip-flop` vocabulary for MOS storage elements while separately discussing storage arrays, drive, sensing, decoding, and chip selection.

**Source-status boundary:** the p. 43 / p. 47 locations and text are strongly identified, but this repository has still not obtained a reliably renderable facsimile of those exact pages for direct visual inspection. That archival task remains open.

**Primary anchor:** L. L. Vadasz, H. T. Chua, A. S. Grove, “Semiconductor random-access memories,” *IEEE Spectrum* 8(5), May 1971, pp. 40–48: <https://www.worldradiohistory.com/Archive-IEEE/1971/IEEE-Spectrum-1971-05.pdf>.

### 1975 — `static`, `fully DC stable`, and `no clocks or refreshing`

Intel's 1975 *Data Catalog* classifies RAM products explicitly as `Static` or `Dynamic`.

- The 1101A is a 256-word by one-bit P-channel MOS random-access memory using **fully dc stable (static) circuitry**, with no clock required to operate.
- The 2102 is a `1024 BIT FULLY DECODED STATIC MOS RANDOM ACCESS MEMORY`, uses fully DC-stable circuitry, requires **no clocks or refreshing**, and is specified for nondestructive read.

The historically safe vocabulary in this bounded source set is therefore `static MOS memory`, `static random access memory`, `fully DC stable`, `no clocks or refreshing`, `read nondestructively`, `chip select`, and `fully decoded`.

This case does **not** claim that `SRAM`, or one modern canonical transistor topology, was the only or universal period vocabulary.

**Primary anchor:** Intel Corporation, *Intel Data Catalog*, 1975, RAM selection guide p. 2-2; 1101A pp. 2-3–2-5; 2102 p. 2-33: <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/1975_Intel_Data_Catalog.pdf>.

### 1975 — `data retention` as a specified low-power mode

The same Intel catalog describes the CMOS 5101 family as static RAMs with a low-power deselected condition. It identifies battery operation or battery backup as useful where application-level non-volatility is required. The 5101L / 5101L-3 variants add **guaranteed data retention at a supply voltage as low as 2.0 V**. The following page separately specifies normal operation at 5 V ±5%, minimum `VCC for Data Retention`, `Data Retention Current`, `Chip Deselect to Data Retention Time`, and `Operation Recovery Time`.

That vocabulary makes a distinction between **retaining the stored state** and **being in the ordinary active operating condition** directly visible in a period vendor specification.

**Primary anchor:** Intel, *Data Catalog* (1975), 5101/5101L pp. 2-115–2-116.

---

## Historical record

### H/P — period engineers explicitly described static MOS storage in flip-flop terms

The Fairchild 1968-filed patent describes MOS flip-flop storage and cross-coupled stability. Vadasz, Chua, and Grove likewise use MOS flip-flop language for storage by 1971.

The strongest historically safe claim is therefore:

> by 1968–1971, period semiconductor-memory engineering sources explicitly described MOS memory cells through flip-flop / cross-coupled storage relations.

This supports a historical vocabulary link to Case 06. It does **not** establish electrical identity between Eccles–Jordan/ENIAC circuits and any later MOS cell.

### H/P — a contemporary NASA study depicts a generic cross-coupled static MOS cell

NASA contractor report NASA-CR-108672, published 1 August 1970, includes Fig. 2.6.10, `Static MOS Memory Cell`, depicting a four-device cell with two internal cross-coupled devices, two access devices, `SELECT`, and two `DATA` connections.

This is a period engineering witness that static MOS storage could combine cross-coupled state holding with separately controlled access.

It remains a **generic 1970 static-MOS cell witness**. It is not evidence that Intel's 1101, 1101A, or 2102 used that exact topology.

**Primary / institutional anchor:** J. P. Green, A. L. Kosmala, F. H. Martin, *Engineering Study for a Mass Memory System for Advanced Spacecrafts*, NASA-CR-108672, 1 August 1970, Fig. 2.6.10: <https://ntrs.nasa.gov/citations/19710005248>.

### H/P — Fairchild US3530443A makes the state-holding relation and array conditions explicit

The Fairchild disclosure describes a complete MOS memory cell in which two devices are cross-coupled and store the logic condition while two other devices also act as load/gating elements. It then places the cell in an array with word and bit lines and separates standby, address, read, and write conditions.

In the disclosed static-storage mode, state holding therefore cannot be reduced to the word `bistable`: the retained relation exists under a stated powered standby bias and becomes usable through separate address/read/write bias changes.

The patent also discusses threshold sensitivity, current transients, power, write speed, and noise margin when comparing alternative operating arrangements. Those values and tradeoffs are specific to the disclosed Fairchild circuits and must not be transferred to Intel products.

### H/P — Intel 1101A turns `static` into a package-level operating claim

Intel's 1975 1101A sheet says the device is a 256-word by one-bit random-access memory element using normally-off P-channel MOS devices in a monolithic array. It uses **fully dc stable (static) circuitry** and requires no clock to operate. The same sheet supplies address inputs, read/write, chip select, data input/output, power-supply conditions, and explicit read/write timing.

The important boundary is that `static` does not mean `outside time`. The stored condition does not require a periodic refresh clock, but accessing and changing it still has specified read-cycle, access, write-pulse, setup, hold, and chip-select timing.

### H/P — Intel 2102 combines static retention with a decoded array and nondestructive read

Intel's 2102 sheet calls the device a 1024-word by one-bit static MOS RAM, states that it uses fully DC-stable circuitry and needs **no clocks or refreshing**, and states that data is read **nondestructively**. Its block diagram separates:

- a 32-row by 32-column cell array;
- row selection;
- column selection / I/O circuitry;
- input-data control;
- address inputs;
- read/write control;
- chip enable;
- data output.

This is a period primary example in which quiescent cell retention is embedded in an addressing and I/O organization substantially richer than one directly wired flip-flop.

### H/P — Intel 5101L separates retention supply from normal operating supply

Intel specifies normal 5101-family operation at 5 V ±5%. For 5101L variants it separately guarantees retention down to 2.0 V, specifies data-retention current at 2.0 V, and defines an `Operation Recovery Time` after the retention condition. The preceding page frames battery backup as a way to obtain application-level non-volatility.

This establishes a bounded fact:

> the supply condition sufficient to preserve a static state need not be identical to the supply condition under which the package performs its ordinary read/write service.

It blocks the shortcut `static = unpowered`.

### H/P — nearby Intel patent evidence can still belong to the dynamic branch

Intel patent US3706079A, Vadasz and Karp, filed 16 September 1971, explicitly describes a **three-line dynamic storage cell**. It stores charge on parasitic capacitance and states that the charge is transient and must be refreshed periodically.

**Primary anchor:** Leslie L. Vadasz, Joel A. Karp, “Three-line cell for random-access integrated circuit memory,” US Patent 3,706,079: <https://patents.google.com/patent/US3706079A/en>.

This patent is included as a negative control. Being an early Intel MOS-memory patent by Vadasz does not make it evidence for the 1101/2102 static bit-cell topology.

---

## Retained state and substrate

### H/P

The period sources establish a static-MOS regime in which binary state can be held by DC-stable / cross-coupled flip-flop-type circuitry rather than by scheduled reconstruction of a transient storage charge.

The Fairchild patent and NASA report give independent period witnesses for cross-coupled static-MOS cell design; Vadasz et al. supply period flip-flop vocabulary; Intel product documentation supplies bounded package-level static behavior.

### E — claim-specific reconstruction

For the bounded comparison, the retained target is a **which-stable-logical-condition** relation inside a powered semiconductor cell, organized into an array whose surrounding selection and I/O circuits determine which cell can be read or changed.

The repository still lacks a directly inspected transistor-level primary schematic/design source for the specific Intel 1101/1101A or 2102 bit cell. Therefore it does not assign those products a four-, six-, or other transistor topology merely because a nearby Fairchild patent, a generic NASA figure, or a later SRAM textbook shows one.

---

## Retention mechanism: powered quiescence survives the substrate transition

### E

For the bounded Intel static products, the mechanism-level relation is:

```text
write / state-setting action
        ↓
DC-stable logical cell condition
        ↓
continued suitable supply condition
        ↓
no scheduled refresh merely because time passes
        ↓
later address/select + read or write operation
```

The Fairchild period witness adds a lower-level model for one contemporary implementation family:

```text
cross-coupled MOS storage relation
        +
powered standby bias
        ↓
stable logical condition
        ↓
array address
        ↓
differential read or state-switching write
```

This resembles grounded Case 06 in one controlled respect: **holding can be regenerative/static under suitable powered conditions rather than deadline-driven refresh**.

It differs in equally important ways:

- semiconductor rather than thermionic implementation;
- dense integration into arrays;
- word/bit or row/column selection mediating access;
- package-level read/write timing;
- explicitly engineered standby and retention-only supply conditions;
- finite threshold/noise/process margins that constrain usable holding and access.

The comparison is functional and mechanism-level. It is not a genealogy of one unchanged flip-flop circuit.

---

## `Static` does not mean `no power`

### H/P

- 1101A operation is specified under powered supply conditions.
- 2102 is a +5 V static MOS RAM; `no clocks or refreshing required` concerns recurring state-restoration work, not the absence of VCC.
- 5101/5101-3 are explicitly discussed for battery operation or battery backup where non-volatility is required.
- 5101L variants guarantee a low-voltage retention condition down to 2.0 V, not zero volts.
- Fairchild's static-storage mode is likewise a powered bias regime, not an unpowered state.

### E

Therefore:

> **refresh-free retention ≠ energy-free retention**.

And:

> **retention-supporting power ≠ full-operation power**.

The 5101L makes the second distinction concrete. A device can remain in a state-preserving electrical condition while not yet being in its normal read/write service condition.

Future cross-case work should therefore ask at least four separate power questions:

1. is power needed merely to preserve state?
2. what supply range is guaranteed for retention?
3. what supply/condition is required for active access?
4. what transition or recovery is required between retention and operation?

---

## `Static` is not a sufficient topology label

### H/P

Fairchild US3530443A is unusually useful because the disclosed basic cell family is discussed under several operating modes, including static storage and dynamic storage. In the dynamic mode, the patent states that all word lines must be periodically addressed and that restoring pulses are required before the natural storage interval is exceeded.

### E

This blocks another shortcut:

> **cross-coupled morphology alone does not settle the whole retention regime; biasing, array conditions, and maintenance protocol also matter.**

For Intel 1101A/2102, the manufacturer documentation remains the authority for the package claim `fully DC stable` / no refresh. The Fairchild patent is not a substitute for an Intel cell disclosure; it is a period control showing why `static` and `dynamic` must be grounded in actual operation rather than inferred from a modern schematic stereotype.

---

## Read, write, and timing semantics

### H/P — read can be nondestructive

Intel specifies nondestructive read for the 2102 and 5101 family.

This is another direct counterexample to any equation of electronic volatility with destructive read.

### H/P — static retention still has access timing

The 1101A sheet specifies read-cycle/access and write-cycle/write-pulse/setup/hold/chip-select intervals. The 5101 similarly specifies read/write cycles, write setup/hold/recovery, and recovery from its low-voltage retention condition.

Fairchild's patent independently separates standby, address, read, and write bias conditions even within a static-storage regime.

### E

Thus:

> **no periodic refresh ≠ no temporal constraints**.

A state can be quiescent between useful operations while selection, sensing, output, writing, deselection, and re-entry from a retention-only condition remain explicitly timed or conditioned operations.

This extends Case 06's distinction between **state-holding stability** and **transition/recovery dynamics** into semiconductor arrays.

---

## Bistability is margin-bounded

### H/P

The Fairchild patent compares operating arrangements in terms of threshold sensitivity, current transients, write speed, power dissipation, and noise immunity. It identifies one half-select arrangement as particularly sensitive to threshold variation and therefore problematic for yield, and compares alternative modes/circuits with different noise margins and power/write tradeoffs.

These are **Fairchild-circuit-specific** engineering statements. They do not establish Intel 1101A/2102 noise margins.

### E

The bounded cross-case lesson is:

> **bistability ≠ unlimited state-holding margin**.

A cell can have two intended logical conditions while retention and successful access remain dependent on finite electrical/process margins and on the bias conditions of the surrounding array.

This deepens, rather than replaces, the existing distinction `cell bistability ≠ array-memory semantics`.

---

## Cell retention is not array organization

### H/P

Vadasz et al. distinguish MOS storage arrays from drive, sense, and decode circuitry. Their p. 47 Intel-1101 example uses parallel address connections and chip-select inputs to choose memory units. Intel's 2102 block diagram likewise separates cell array, row selector, column selection, input control, and external I/O/control.

Fairchild US3530443A also places a storage cell within word/bit-line array conditions rather than treating the state-holding pair as a complete memory service in isolation.

### E

The retained state of one cell is only one analytical layer:

```text
cell-level stable state
    ≠ electrical margin / bias regime
    ≠ array grouping
    ≠ row/column or word/bit selection
    ≠ package selection
    ≠ architectural role
    ≠ cache policy
```

A static semiconductor cell does not become a `cache` merely because later caches are commonly built from SRAM. Cache requires placement, lookup/tag, replacement, visibility, hierarchy, and often coherence/consistency semantics that are outside this case.

---

## Failure and technical forgetting

### H/P

The first pass now has two different kinds of bounded failure evidence:

- **Intel retention-condition boundary:** 5101L retention is guaranteed only down to its specified 2.0 V floor; Intel explicitly invokes battery backup when non-volatility is desired.
- **Fairchild electrical-margin boundary:** the 1968-filed patent discusses threshold sensitivity, current transients, noise immunity, and power/write tradeoffs across disclosed operating arrangements.

Intentional write is also an explicit state replacement operation in both families.

### E

For this case, forgetting/unavailability can therefore occur through at least:

1. **supply-condition loss** — the electrical condition required for retained state is no longer guaranteed;
2. **insufficient electrical margin / disturbance** — a retained distinction can fail to remain or be recovered correctly if the actual circuit leaves its valid stability/read/write margins;
3. **intentional rewrite** — a later write establishes another stable logical condition;
4. **access-organization failure** — an intact cell state may become unusable if selection/I/O machinery cannot recover it.

The Fairchild patent closes a **generic period margin-mechanism** gap, not the roadmap's device-specific Intel hold/failure gap. Do not transfer Fairchild thresholds/noise values to Intel devices, and do not infer an Intel-2102 data-loss voltage from the 5101L specification.

---

## Comparison with grounded Case 06 and DRAM

| Dimension | Case 06: thermionic flip-flop | Case 07: bounded static MOS RAM | Grounded DRAM case |
| --- | --- | --- | --- |
| state holding | regenerative bistability | DC-stable / cross-coupled flip-flop-type semiconductor state in period witnesses | decaying storage-node charge in bounded 1T1C regime |
| power | powered operating condition | powered; 5101L additionally separates low-V retention from ordinary operation | powered system plus scheduled regeneration |
| periodic refresh merely to remain | not established | explicitly unnecessary in cited Intel static devices; Fairchild also distinguishes static from a separate dynamic mode | required in bounded dynamic regime |
| read | state can condition later gates nondestructively | Intel 2102 / 5101 nondestructive read | device/regime dependent; bounded Dennard 1T1C destructive, later commercial examples can be nondestructive |
| access organization | often directly wired into counters/controls; higher organization external | array + selection + chip enable + I/O; period Fairchild source also separates standby/address/read/write | decoded array + sense/restore infrastructure |
| holding constraints | circuit operating condition + stability | supply + finite threshold/noise/process margin; exact values device-specific | leakage deadline + sense/restore margins |
| timing problem | set / trigger / recovery margins | access/write/select timing + retention-to-operation recovery | access timing + refresh deadline + restore |

The result is not that SRAM is merely a smaller flip-flop or a faster DRAM. The cases expose different combinations of **state-holding relation, electrical support, array organization, maintenance trigger, access semantics, and engineering margin**.

---

## Functional analogies and prohibited collapses

### A — useful bounded analogy

A static MOS memory cell is **flip-flop-like in a historically supported sense**: period sources explicitly use flip-flop / cross-coupled language for MOS storage, and bounded static devices maintain state without scheduled refresh.

### X — do not infer

- `static = nonvolatile without power`;
- `static = no timing constraints`;
- `cross-coupled = automatically static under every bias/array regime`;
- `static cell = register`;
- `static RAM = cache`;
- `all early static RAM = modern six-transistor CMOS SRAM`;
- `NASA 1970 generic cell = Intel 1101/2102 transistor-level schematic`;
- `Fairchild US3530443A = Intel 1101/2102 transistor-level schematic`;
- `Intel US3706079A = static-cell evidence`;
- `no refresh = maintenance-free system`.

---

## Philosophical / conceptual interpretation

### I — quiescence can be conditional rather than autonomous

The case sharpens `quiescent retention`. A state may require **no recurring state-restoration event** while still depending on a continuously satisfied electrical condition and finite operating margins. `Nothing has to be rewritten yet` and `nothing has to be supplied or constrained` are different propositions.

### I — retention can have a lower-power mode than availability

The 5101L adds a useful complication to the project's availability/addressability work without collapsing into philosophical vocabulary: a state can continue to count as retained under a lower-voltage condition while ordinary active service is not yet restored. Retention and full callability are therefore not identical operational states.

This is a project interpretation, not Intel's philosophical vocabulary.

---

## Evidence status and remaining gaps

This case remains **`first-pass`**. The new Fairchild source materially deepens the mechanism, but it would be a category error to promote the Intel-bounded case by substituting a neighboring vendor's cell for the missing Intel-specific one.

### Strongly supported now

- period MOS flip-flop / cross-coupled storage vocabulary;
- a 1968-filed primary cell design with explicit static-storage operation;
- separation of standby/address/read/write conditions within a period static-MOS array discussion;
- period evidence that `static` and `dynamic` can be operating regimes requiring source-controlled bias/maintenance analysis rather than merely modern topology labels;
- Intel static-versus-dynamic product classification;
- no clock/refresh requirement for the cited Intel static devices;
- nondestructive read for the cited Intel devices;
- decoded array / chip-selection organization;
- explicit low-voltage data-retention mode and operation recovery in the 5101L family;
- generic period evidence that threshold/noise/power margins constrain usable cell operation.

### Promotion gaps still open

1. directly inspect a full, reliably renderable facsimile of Vadasz–Chua–Grove 1971 pp. 43 and 47 rather than treating indexed page text as visual inspection;
2. obtain a **cell-specific primary schematic or design paper for an Intel 1101/1101A or 2102-class static bit cell**;
3. add a source-controlled **Intel-device-specific** hold/failure/noise-margin account, rather than transferring the Fairchild circuit's margins or the 5101L low-V guarantee to another device;
4. keep bipolar static memories and later canonical CMOS six-transistor SRAM separate unless they change the retention comparison.

Cache remains deferred until the cell/array bridge is grounded enough that policy/hierarchy semantics cannot be mistaken for substrate properties.

---

## Sources

### Primary / contemporary

1. Harold S. Crafts, Wendell B. Sander, James B. Angell, “MOS gated resistor memory cell,” US Patent 3,530,443, filed 27 November 1968, published 22 September 1970. <https://patents.google.com/patent/US3530443A/en>
2. L. L. Vadasz, H. T. Chua, A. S. Grove, “Semiconductor random-access memories,” *IEEE Spectrum* 8(5), May 1971, pp. 40–48. Relevant indexed locations: p. 43 (MOS flip-flops / static MOS cell), p. 47 (fully decoded static MOS / Intel 1101 system example). Exact facsimile inspection remains open. <https://www.worldradiohistory.com/Archive-IEEE/1971/IEEE-Spectrum-1971-05.pdf>
3. J. P. Green, A. L. Kosmala, F. H. Martin, *Engineering Study for a Mass Memory System for Advanced Spacecrafts*, NASA-CR-108672, 1 August 1970, Fig. 2.6.10 `Static MOS Memory Cell`. <https://ntrs.nasa.gov/citations/19710005248>
4. Intel Corporation, *Intel Data Catalog*, 1975. RAM selection guide p. 2-2; Intel 1101A pp. 2-3–2-5; Intel 2102 p. 2-33; Intel 5101 / 5101L pp. 2-115–2-116. <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/1975_Intel_Data_Catalog.pdf>
5. Leslie L. Vadasz, Joel A. Karp, “Three-line cell for random-access integrated circuit memory,” US Patent 3,706,079, filed 16 September 1971, published 12 December 1972. Used here as an explicit dynamic-cell negative control, not as evidence for Intel static topology. <https://patents.google.com/patent/US3706079A/en>

### Secondary / institutional context

6. Computer History Museum, *The Storage Engine*, “1970: Semiconductors compete with magnetic cores.” Chronology only; central mechanism claims above do not depend on it. <https://www.computerhistory.org/storageengine/semiconductors-compete-with-magnetic-cores/>

---

## First-pass conclusion

The static-semiconductor bridge survives a second, deeper test.

What carries over from the grounded thermionic flip-flop case is **powered quiescent state holding without scheduled refresh**. The Fairchild 1968-filed disclosure now makes one period MOS implementation family more concrete: cross-coupled storage, powered standby, explicit address/read/write conditions, and finite electrical margins. Intel's product documentation then shows how static state holding is exposed as a decoded commercial memory service and, in the 5101L, how retention can have a lower supply condition than ordinary operation.

Two corrections matter most:

> **static retention is neither unpowered retention nor an ideal Boolean state outside electrical margins.**

and

> **a period MOS circuit's vendor/date proximity is not enough to identify an Intel static bit-cell topology.**

The next promotion work therefore remains deliberately narrow: inspect Vadasz pp. 43/47 directly, locate a genuine Intel 1101/1101A/2102 static-cell design source, and ground an Intel-device-specific hold/failure margin before cache is opened.