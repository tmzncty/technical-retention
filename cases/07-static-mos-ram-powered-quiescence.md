# Static MOS RAM: Powered Quiescence in a Semiconductor Array

## Scope

- **Status:** `first-pass`.
- **Object / system:** a bounded 1969–1975 static-MOS semiconductor-memory bridge, using period Intel engineering sources plus a 1970 NASA contractor study. Intel 1101/1101A and 2102-class documentation establishes period `static` / random-access vocabulary and package/array behavior; Intel 5101/5101L is used as a bounded later comparison because it explicitly separates ordinary operation from a low-voltage data-retention condition.
- **Date range:** 1969–1975 for the bounded historical bridge.
- **Primary question:** what changes, and what does not, when regenerative bistable retention moves from the grounded thermionic flip-flop case into monolithic semiconductor memory arrays?
- **Why this case matters:** Case 06 established that a powered bistable state can remain quiescently available without scheduled refresh. Static semiconductor memory tests whether that distinction survives integration, array addressing, package-level read/write semantics, and low-power standby/data-retention modes.

This is **not** a general history of SRAM, bipolar scratchpad memory, cache, register files, CMOS scaling, or the modern six-transistor SRAM cell. Cache policy and hierarchy semantics are intentionally excluded. A modern `6T SRAM` description must not be projected onto every 1969–1975 static MOS device without a cell-specific primary source.

---

## Related-repository check

Fresh code searches in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `SRAM`, `static random access memory`, and `Intel 1101` found no dedicated static-semiconductor-memory treatment to reuse. That repository already identifies semiconductor memory as a historical gap and remains the preferred home for a broad engineering history.

The contribution here is therefore narrow: establish a retention-specific bridge from regenerative state holding to a decoded semiconductor-memory array, then stop before cache or general semiconductor-memory history.

---

## Historical vocabulary

### 1971 — `static MOS memory`, `MOS flip-flops for storage`, Intel 1101

L. L. Vadasz, H. T. Chua, and A. S. Grove of Intel, writing in the May 1971 issue of *IEEE Spectrum*, describe a semiconductor-memory approach that used **MOS flip-flops for storage**. On p. 43 they compare a `static MOS memory cell` that had become commercially available in 1969 with bipolar cells, and discuss MOS memory arrays as storage arrays of MOS flip-flops. On p. 47 they describe fully decoded static MOS memories and use the Intel `1101` as their 256-by-1 example.

This source is important because the bridge from the flip-flop case to static semiconductor memory is not only a modern functional analogy: period engineers themselves used `flip-flop` language for the MOS storage element. That still does **not** make every package, register, or cache historically synonymous with a flip-flop.

**Primary anchor:** L. L. Vadasz, H. T. Chua, A. S. Grove, “Semiconductor random-access memories,” *IEEE Spectrum* 8(5), May 1971, pp. 40–48, especially pp. 43 and 47: <https://www.worldradiohistory.com/Archive-IEEE/1971/IEEE-Spectrum-1971-05.pdf>.

### 1975 — `static`, `fully DC stable`, and `no clocks or refreshing`

Intel's 1975 *Data Catalog* classifies its RAM products explicitly as `Static` or `Dynamic`. The 1101A is described as a 256-word by one-bit random-access memory using P-channel MOS devices and **fully dc stable (static) circuitry**, requiring no clocks to operate. The 2102 is described as a `1024 BIT FULLY DECODED STATIC MOS RANDOM ACCESS MEMORY` using fully DC-stable circuitry and requiring **no clocks or refreshing**; its data is read nondestructively.

The historically safe vocabulary in this bounded source set is therefore `static MOS memory`, `static random access memory`, `fully DC stable`, `no clocks or refreshing`, `read nondestructively`, `chip select`, and `fully decoded`.

This case does **not** claim that the acronym `SRAM`, or one modern canonical transistor topology, was the only or universal period vocabulary.

**Primary anchor:** Intel Corporation, *Intel Data Catalog*, 1975, RAM selection guide p. 2-2; 1101A pp. 2-3–2-5; 2102 p. 2-33: <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/1975_Intel_Data_Catalog.pdf>.

### 1975 — `data retention` as a specified low-power mode

The same Intel catalog describes the CMOS 5101 family as static RAMs with a low-power deselected condition. It says the devices are suitable where `battery operation or battery backup for non-volatility` is required. The 5101L / 5101L-3 variants add **guaranteed data retention at a supply voltage as low as 2.0 V**. The following page separately lists normal operation at 5 V ±5%, a 2.0 V minimum `VCC for Data Retention`, a `Data Retention Current`, `Chip Deselect to Data Retention Time`, and an `Operation Recovery Time`.

That vocabulary matters because it makes a distinction between **retaining the stored state** and **being in the ordinary active operating condition** directly visible in a period vendor specification.

**Primary anchor:** Intel, *Data Catalog* (1975), 5101/5101L pp. 2-115–2-116.

---

## Historical record

### H/P — period engineers explicitly described static MOS storage as flip-flop storage

Vadasz, Chua, and Grove state that one semiconductor-memory approach used MOS flip-flops for storage and discuss a static MOS memory cell commercially available in 1969. Their p. 43 discussion places storage cells, sensing, decoding, and drive circuitry in different roles rather than treating the entire memory system as one undifferentiated cell.

The strongest historically safe claim is:

> by 1971, Intel engineers were explicitly describing static MOS semiconductor storage in flip-flop terms while also distinguishing the storage array from the support circuitry around it.

This supports a historical vocabulary link to Case 06, not a claim that the ENIAC circuit and a MOS memory cell are electrically identical.

### H/P — a contemporary NASA study depicts a cross-coupled static MOS memory cell

NASA contractor report NASA-CR-108672, published 1 August 1970, includes **Fig. 2.6.10, `Static MOS Memory Cell`**. The figure depicts a four-device cell with two internal cross-coupled devices, two access devices, a `SELECT` control, and two `DATA` connections.

This figure gives a period engineering witness that a static MOS storage cell could be organized around cross-coupled state holding plus separately controlled data access.

It is used only as a **generic 1970 static-MOS cell witness**. It is not evidence that Intel's 1101 or 2102 used this exact four-device topology.

**Primary / institutional anchor:** J. P. Green, A. L. Kosmala, F. H. Martin, *Engineering Study for a Mass Memory System for Advanced Spacecrafts*, NASA-CR-108672, 1 August 1970, Fig. 2.6.10: <https://ntrs.nasa.gov/citations/19710005248>; scan: <https://ntrs.nasa.gov/api/citations/19710005248/downloads/19710005248.pdf>.

### H/P — Intel 1101A turns `static` into a package-level operating claim

Intel's 1975 1101A data sheet says the device is a 256-word by one-bit random-access memory element using normally-off P-channel MOS devices in a monolithic array. It uses **fully dc stable (static) circuitry** and therefore requires **no clocks to operate**. The same sheet supplies address inputs, read/write, chip select, data input/output, power-supply conditions, and explicit read/write timing.

The important boundary is that `static` does not mean `outside time`. The stored condition does not require a periodic refresh clock, but accessing and changing it still has specified read-cycle, access, write-pulse, setup, hold, and chip-select timing.

### H/P — Intel 2102 combines static retention with a decoded array and nondestructive read

Intel's 2102 data sheet calls the device a 1024-word by one-bit `STATIC MOS RANDOM ACCESS MEMORY`, states that it uses fully DC-stable circuitry and needs **no clocks or refreshing to operate**, and states that data is read **nondestructively**. Its block diagram separates:

- a 32-row by 32-column cell array;
- row selection;
- column selection / I/O circuitry;
- input-data control;
- address inputs;
- read/write control;
- chip enable;
- data output.

This is a period primary example in which a quiescent cell-retention regime is embedded in an addressing and I/O organization substantially richer than one directly wired flip-flop.

**Primary anchor:** Intel, *Data Catalog* (1975), 2102 p. 2-33.

### H/P — Intel 5101L separates retention supply from normal operating supply

Intel specifies normal 5101-family operation at 5 V ±5%. For the 5101L variants it separately guarantees data retention with `VCC for Data Retention` down to **2.0 V**, specifies data-retention current at 2.0 V, and defines an `Operation Recovery Time` after the retention condition. The preceding page explicitly frames battery backup as a route to `non-volatility` for applications that require it.

This establishes a particularly useful bounded fact:

> the supply condition required to preserve a static state need not be identical to the supply condition under which the package performs its ordinary read/write service.

It also blocks the shortcut `static = unpowered`.

---

## Retained state and substrate

### H/P

The period sources establish a static-MOS memory regime in which a binary state is held by DC-stable / flip-flop-type circuitry rather than by a periodically refreshed charge-storage cycle. The NASA figure directly shows a generic cross-coupled static-MOS cell; Vadasz et al. explicitly call MOS storage elements flip-flops.

### E — claim-specific reconstruction

For the bounded comparison, the retained target is a **which-stable-logical-condition** relation inside a powered semiconductor cell, organized into an array whose surrounding decode and I/O circuits select which cell's state is read or changed.

The repository does **not** yet have a directly inspected transistor-level primary schematic for the specific Intel 1101/1101A or 2102 bit cell. Therefore this first pass does not assign either product a specific four-, six-, or other transistor topology merely because later SRAM textbooks make one arrangement familiar.

---

## Retention mechanism: powered quiescence survives the substrate transition

### E

The bounded mechanism can be reconstructed as:

```text
write / state-setting action
        ↓
bistable DC-stable cell condition
        ↓
continued suitable supply condition
        ↓
no periodic refresh merely because time passes
        ↓
later address/select + read or write operation
```

This resembles the grounded Case-06 thermionic flip-flop in one controlled respect: **state holding is regenerative/static under suitable operating conditions rather than deadline-driven refresh**.

It differs in equally important ways:

- the retention element is semiconductor rather than thermionic;
- many cells are integrated into an array;
- row/column decoding and chip selection mediate access;
- package-level read/write interfaces and timing become part of the usable-retention relation;
- low-power standby / retention-only supply conditions become explicit in the 5101L documentation.

The comparison is functional and mechanism-level; it is not a claim that one exact circuit topology simply persisted unchanged from Eccles–Jordan or ENIAC into Intel RAM.

---

## `Static` does not mean `no power`

The Intel sources support a stronger distinction than `static versus dynamic` alone.

### H/P

- 1101A operation is specified under powered supply conditions.
- 2102 is a single-+5-V static MOS RAM; `no clocks or refreshing required` is a statement about recurring clock/refresh work, not a statement that VCC is unnecessary.
- 5101/5101-3 are explicitly discussed as candidates for **battery operation or battery backup for non-volatility**.
- 5101L variants guarantee a low-voltage data-retention condition down to 2.0 V, not to zero volts.

### E

Therefore:

> **refresh-free retention ≠ energy-free retention**.

And, more subtly:

> **retention-supporting power ≠ full-operation power**.

The 5101L case makes the latter distinction concrete. A memory can remain in a state-preserving electrical regime while not yet being in its ordinary active read/write operating condition.

This suggests that future cross-case work should treat `power dependence` as more than one Boolean property. At minimum, the relevant questions are whether power is required to preserve state, what supply range is guaranteed for retention, what power is required for active access, and what transition/recovery is required between those modes.

---

## Read, write, and timing semantics

### H/P — read can be nondestructive

Intel states that 2102 data is read nondestructively. The 5101 family is also described as nondestructive-read static circuitry.

This supplies another direct counterexample to any equation of electronic volatility with destructive read.

### H/P — static retention still has access timing

The 1101A sheet specifies read-cycle/access times and write-cycle, write-pulse, setup, hold, chip-select, and deselect intervals. The 5101 sheet similarly specifies a 650 ns read cycle, a 650 ns write cycle, write setup/hold/recovery constraints, and an operation-recovery time for the low-VCC retention condition.

### E

Thus:

> **no periodic refresh ≠ no temporal constraints**.

A state can be quiescent between useful operations while selection, sensing/output, writing, deselection, and re-entry from a retention-only power condition remain explicitly timed operations.

This extends Case 06's distinction between **state-holding stability** and **transition/recovery dynamics** into a semiconductor-memory package.

---

## Cell retention is not array organization

### H/P

Vadasz et al. separate MOS storage arrays from drive, sense, and decode circuitry. Their p. 47 Intel-1101 system example connects address inputs in parallel and uses chip-select inputs to choose memory units. Intel's 2102 block diagram separates cell array, row selector, column-selection circuits, input control, and external I/O/control pins.

### E

The retained state of one cell is only one layer in an addressable RAM service:

```text
cell-level stable state
    ≠ array grouping
    ≠ row/column decoding
    ≠ package selection
    ≠ architectural role
    ≠ cache policy
```

This is the semiconductor continuation of Case 06 finding 89: **state element, organization, architectural role, and interface semantics must remain separate comparison axes**.

A static semiconductor cell does not become a `cache` merely because later caches are commonly built from SRAM. Cache requires additional placement, lookup/tag, replacement, coherence/consistency, visibility, and hierarchy semantics that are outside this case.

---

## Failure and technical forgetting

This first pass supports only bounded failure claims.

### H/P

- Intel's static devices are specified under explicit supply ranges.
- 5101L low-voltage state retention is guaranteed only down to a specified 2.0 V floor in the cited catalog.
- Intel explicitly invokes battery backup when `non-volatility` is desired.
- write operations deliberately replace the retained logical state.

### E

For this case, forgetting can therefore occur at least through:

1. **supply-condition loss** — the continued state is no longer guaranteed when the retention-supporting electrical condition is lost;
2. **intentional rewrite** — a later write establishes another stable state;
3. **access-organization failure** — an intact cell state may become unusable if selection/I/O circuitry cannot recover it, although this case does not yet ground specific package failure modes in detail.

Do not generalize the 5101L's 2.0 V guarantee to all static RAM, and do not infer a precise Intel-2102 data-loss voltage from a different product's specification.

---

## Comparison with grounded Case 06 and DRAM

| Dimension | Case 06: thermionic flip-flop | Case 07: bounded static MOS RAM | Grounded DRAM case |
| --- | --- | --- | --- |
| state holding | regenerative bistability | DC-stable / flip-flop-type semiconductor state | decaying storage-node charge in bounded 1T1C regime |
| power | powered operating condition | powered; 5101L additionally separates low-V retention from ordinary operation | powered system plus scheduled regeneration |
| periodic refresh merely to remain | not established | explicitly unnecessary in Intel static devices | required in the bounded dynamic regime |
| read | state can condition later gates nondestructively | Intel 2102 / 5101 nondestructive read | device/regime dependent; bounded Dennard 1T1C destructive, later commercial examples can be nondestructive |
| access organization | often directly wired into counters/controls; higher organization external | decoded array + row/column selection + chip enable + I/O | decoded array + sense/restore infrastructure |
| timing problem | set / trigger / recovery margins | read/write/select timing + retention-to-operation recovery | access timing + refresh deadline + restore |

The important result is not that SRAM is simply a smaller flip-flop or a faster DRAM. The three cases expose **different combinations of state-holding mechanism, continuing supply, access organization, and maintenance timing**.

---

## Functional analogies and prohibited collapses

### A — useful bounded analogy

A static MOS memory cell is **flip-flop-like in the historically supported sense that period engineers explicitly called MOS storage elements flip-flops** and used DC-stable state holding rather than periodic refresh.

### X — do not infer

- `static = nonvolatile without power`;
- `static = no timing constraints`;
- `static cell = register`;
- `static RAM = cache`;
- `all early static RAM = modern six-transistor CMOS SRAM`;
- `the generic NASA 1970 static-MOS figure = Intel 1101/2102 transistor-level schematic`;
- `no refresh = maintenance-free system`.

---

## Philosophical / conceptual interpretation

### I — quiescence can be conditional rather than autonomous

The case sharpens the repository's use of `quiescent retention`. A state may require **no recurring state-restoration event** while still depending on a continuously satisfied electrical condition. `Nothing has to be rewritten yet` and `nothing has to be supplied` are different propositions.

### I — retention can have a lower-power mode than availability

The 5101L adds a useful complication to the Heidegger/availability and general addressability discussions without collapsing into them: a state can continue to count as retained under a low-voltage condition while ordinary active service is not yet restored. Retention and full callability are therefore not identical operational states.

This is a project interpretation, not Intel's philosophical vocabulary.

---

## Evidence status and remaining gaps

This case remains **`first-pass`** despite having strong period primary documentation.

The central package-level claims are well supported:

- period static-MOS / flip-flop vocabulary;
- Intel static-versus-dynamic classification;
- no clock/refresh requirement for the cited static devices;
- nondestructive read for the cited Intel devices;
- decoded array / chip-selection organization;
- explicit low-voltage data-retention mode and operation recovery in the 5101L family.

Promotion to `grounded` should still close these gaps:

1. directly inspect a full, reliably renderable copy of Vadasz–Chua–Grove 1971 pp. 43 and 47 rather than relying on indexed period-page text for the relevant passages;
2. obtain a **cell-specific primary schematic or design paper for an Intel 1101/1101A or 2102-class static bit cell**, so the product-level state-holding mechanism does not depend on combining Intel package documentation with a generic NASA static-MOS figure;
3. add a source-controlled failure/noise-margin or hold-supply account for a specific static device rather than generalizing from the 5101L's bounded low-VCC guarantee;
4. keep bipolar static memories and later canonical CMOS six-transistor SRAM as separate source work unless they change the retention comparison.

Cache should remain deferred until the cell/array bridge is grounded enough that later cache policy semantics cannot be mistaken for substrate properties.

---

## Sources

### Primary / contemporary

1. L. L. Vadasz, H. T. Chua, A. S. Grove, “Semiconductor random-access memories,” *IEEE Spectrum* 8(5), May 1971, pp. 40–48. Relevant bounded passages: p. 43 (`MOS flip-flops for storage`, static MOS cell) and p. 47 (fully decoded static MOS / Intel 1101 system example). <https://www.worldradiohistory.com/Archive-IEEE/1971/IEEE-Spectrum-1971-05.pdf>
2. J. P. Green, A. L. Kosmala, F. H. Martin, *Engineering Study for a Mass Memory System for Advanced Spacecrafts*, NASA-CR-108672, 1 August 1970, Fig. 2.6.10 `Static MOS Memory Cell`. <https://ntrs.nasa.gov/citations/19710005248>
3. Intel Corporation, *Intel Data Catalog*, 1975. RAM selection guide p. 2-2; Intel 1101A pp. 2-3–2-5; Intel 2102 p. 2-33; Intel 5101 / 5101L pp. 2-115–2-116. <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/1975_Intel_Data_Catalog.pdf>

### Secondary / institutional context

4. Computer History Museum, *The Storage Engine*, “1970: Semiconductors compete with magnetic cores.” Useful for broader chronology only; central mechanism claims above do not depend on it. <https://www.computerhistory.org/storageengine/semiconductors-compete-with-magnetic-cores/>

---

## First-pass conclusion

The static-semiconductor bridge survives the first test but changes the comparison in a useful way.

What carries over from the grounded thermionic flip-flop case is **powered quiescent state holding without scheduled refresh**. What changes is the organization around that state: dense arrays, row/column decoding, chip selection, package-level nondestructive read/write semantics, and explicitly specified standby/data-retention modes.

The 5101L is the strongest new counterexample to a one-bit `power dependence` category. A state can require continued electrical support while needing **less** supply for retention than for ordinary operation. The next source-deepening pass should therefore ask not merely whether SRAM `needs power`, but which powered condition is sufficient to keep the state, which is required to access it, and how the system moves between those conditions.
