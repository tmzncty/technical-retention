# Static MOS RAM: Powered Quiescence in a Semiconductor Array

## Scope

- **Status:** `grounded`.
- **Object / system:** a bounded 1968–1975 static-MOS semiconductor-memory bridge, with a 1976 publication of an Intel design filed in 1975. Intel 1101/1101A, 2102, and 5101/5101L documentation supplies product/array behavior; Vadasz–Chua–Grove (1971) supplies period Intel vocabulary; NASA-CR-108672 (1970) and Fairchild US3530443A (filed 1968, published 1970) supply independent period cell-level witnesses; Intel/Pashley US3946369A, filed in 1975, now supplies manufacturer-primary Intel static-RAM cell and array design evidence without being silently identified as a particular commercial part.
- **Date range:** 1968–1975 for the bounded design/filing window; the Pashley filing was published in 1976.
- **Primary question:** what changes, and what does not, when regenerative bistable retention moves from the grounded thermionic flip-flop case into monolithic semiconductor memory arrays?
- **Why this case matters:** Case 06 established powered bistable working retention without scheduled refresh. Static semiconductor memory tests whether that distinction survives integration, array addressing, package-level read/write semantics, finite electrical margins, low-power standby/data-retention modes, and a manufacturer-primary Intel cell/selection/sensing design.

This is **not** a general history of SRAM, bipolar scratchpad memory, cache, register files, CMOS scaling, or the modern six-transistor CMOS SRAM cell. Cache policy and hierarchy semantics remain intentionally excluded. A modern `6T SRAM` description must not be projected onto every 1968–1975 static MOS device merely because one period depletion-load cell also contains six MOS devices.

Source-deepening / grounding records:

- [`../evidence/07-fairchild-static-mos-regime-deepening.md`](../evidence/07-fairchild-static-mos-regime-deepening.md);
- [`../evidence/07-intel-1101-period-cell-witness.md`](../evidence/07-intel-1101-period-cell-witness.md);
- [`../evidence/07-5101-battery-backed-retention-transition.md`](../evidence/07-5101-battery-backed-retention-transition.md);
- [`../evidence/07-intel-pashley-1975-static-ram-grounding.md`](../evidence/07-intel-pashley-1975-static-ram-grounding.md) — promotion record.

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

**Source-status boundary:** the p. 43 / p. 47 locations and text are strongly identified, but this repository has still not obtained a reliably renderable facsimile of those exact pages for direct visual inspection. That archival task remains open. It is no longer a promotion blocker because the central mechanism is independently grounded by other primary sources.

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

### 1975 filing / 1976 publication — Intel `static RAM`, `bistable circuits`, depletion loads

Richard D. Pashley's Intel-assigned US3946369A, filed 21 April 1975 and published 23 March 1976, calls its object an **MOS static random-access memory** and describes static memories as employing **bistable circuits for memory cells**.

Its preferred embodiment is an n-channel MOS `1,024 × 1` memory organized as a `32 × 32` array, operated from +5 V, with depletion-load devices and polycrystalline-silicon gates. The Figure 1 description explicitly places a bistable cell between VCC/VSS and a complementary pair of column lines and describes feedback between the two cell branches.

This is the first Case-07 source that closes the broad **manufacturer-primary Intel cell-mechanism** gap. It still does not name the commercial part represented by the disclosed embodiment.

**Primary anchor:** Richard D. Pashley, “High speed MOS RAM employing depletion loads,” US Patent 3,946,369, assigned to Intel Corporation, filed 21 April 1975, published 23 March 1976: <https://www.freepatentsonline.com/3946369.html>.

---

## Historical record

### H/P — period engineers explicitly described static MOS storage in flip-flop terms

The Fairchild 1968-filed patent describes MOS flip-flop storage and cross-coupled stability. Vadasz, Chua, and Grove likewise use MOS flip-flop language for storage by 1971. Pashley's Intel filing then describes an Intel static RAM in terms of bistable memory cells and explicit inter-branch feedback.

The strongest historically safe claim is therefore:

> by 1968–1975, period semiconductor-memory engineering sources — including an Intel manufacturer-primary design — explicitly described static MOS memory cells through flip-flop / bistable / cross-coupled relations.

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

### H/P — Intel US3946369A exposes one manufacturer-primary static cell and access path

Pashley's 1975-filed Intel patent describes the preferred cell as a bistable circuit with two load/drive branches, feedback between the two branches, and two access transistors connecting the internal storage nodes to complementary column lines under X-line control. The array has 32 rows and 32 columns, X/Y decoding, paired column lines, column sense amplifiers, a read bus, output sensing/buffering, and write-bus connections.

The patent's invention focuses heavily on the **access path** rather than on periodically restoring the cell. It limits column-line voltage swing, decouples unselected column capacitance from the read bus, senses small changes rapidly, and uses a cross-coupled address buffer so true/complement address signals switch together and do not create unintended multiple selection.

This is central to the case because it directly separates two things that generic descriptions of `SRAM` often blur:

> a bit may be held by a bistable cell while reliable selection and recovery still depend on distinct decoder, line-capacitance, sensing, and address-transition constraints.

### H/P — nearby Intel patent evidence can still belong to the dynamic branch

Intel patent US3706079A, Vadasz and Karp, filed 16 September 1971, explicitly describes a **three-line dynamic storage cell**. It stores charge on parasitic capacitance and states that the charge is transient and must be refreshed periodically.

**Primary anchor:** Leslie L. Vadasz, Joel A. Karp, “Three-line cell for random-access integrated circuit memory,” US Patent 3,706,079: <https://patents.google.com/patent/US3706079A/en>.

This patent is included as a negative control. Being an early Intel MOS-memory patent by Vadasz does not make it evidence for the 1101/2102 static bit-cell topology.

---

## Retained state and substrate

### H/P

The period sources establish a static-MOS regime in which binary state can be held by DC-stable / cross-coupled flip-flop- or bistable-type circuitry rather than by scheduled reconstruction of a transient storage charge.

Fairchild and NASA give independent period witnesses for cross-coupled static-MOS cell design; Vadasz et al. supply period flip-flop vocabulary; Intel product documentation supplies bounded package-level static behavior; and Pashley's 1975 filing supplies an Intel manufacturer-primary `1024 × 1` static-RAM cell/array design with explicit bistability and feedback.

### E — claim-specific reconstruction

For the bounded comparison, the retained target is a **which-stable-logical-condition** relation inside a powered semiconductor cell, organized into an array whose surrounding selection and I/O circuits determine which cell can be read or changed.

The repository now has a directly interpretable transistor-level **Intel static-RAM design source**, but it does **not** have an explicit primary statement identifying Pashley's preferred embodiment as the commercial 1101, 1101A, 2102, or 2102A. Therefore exact product-topology claims remain open even though the broader Intel manufacturer-primary mechanism gap is closed.

---

## Retention mechanism: powered quiescence survives the substrate transition

### E

For the bounded Intel static products, the package-level mechanism relation is:

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

Pashley's Intel filing supplies a manufacturer-primary Intel implementation relation:

```text
+5 V powered n-channel depletion-load cell
        +
feedback between two bistable branches
        ↓
retained static condition
        ↓
X-line access to complementary column pair
        ↓
Y selection + sense amplifier / read bus or write path
```

This resembles grounded Case 06 in one controlled respect: **holding can be regenerative/static under suitable powered conditions rather than deadline-driven refresh**.

It differs in equally important ways:

- semiconductor rather than thermionic implementation;
- dense integration into arrays;
- word/bit or row/column selection mediating access;
- package-level read/write timing;
- sense-amplifier and line-capacitance constraints;
- address-transition integrity constraints;
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
- Pashley's preferred Intel static-RAM embodiment explicitly uses a +5 V VCC condition.

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

Pashley's preferred embodiment is specifically an **n-channel depletion-load** static RAM cell. The presence of two loads, two drive/storage devices, and two access devices does not make it the same circuit technology as a later complementary-CMOS six-transistor cell.

### E

This blocks two shortcuts:

> **cross-coupled morphology alone does not settle the whole retention regime; biasing, array conditions, and maintenance protocol also matter.**

and

> **same device count ≠ same historical SRAM topology.**

For Intel 1101A/2102, the manufacturer documentation remains the authority for the package claim `fully DC stable` / no refresh. Pashley's patent grounds an Intel static-cell design class but is not silently relabeled as either product.

---

## Read, write, timing, and recovery semantics

### H/P — read can be nondestructive

Intel specifies nondestructive read for the 2102 and 5101 family.

This is another direct counterexample to any equation of electronic volatility with destructive read.

### H/P — static retention still has access timing

The 1101A sheet specifies read-cycle/access and write-cycle/write-pulse/setup/hold/chip-select intervals. The 5101 similarly specifies read/write cycles, write setup/hold/recovery, and recovery from its low-voltage retention condition.

Fairchild's patent independently separates standby, address, read, and write bias conditions even within a static-storage regime.

Pashley's Intel patent adds a different timing/reliability problem: high-capacitance column lines slow sensing, and mismatched switching of an address signal and its complement can create unintended multiple selection. The disclosed sense path and cross-coupled address buffer are designed to prevent these failures.

### E

Thus:

> **no periodic refresh ≠ no temporal constraints**.

And:

> **retention stability ≠ access-path reliability**.

A state can be quiescent between useful operations while selection, sensing, output, writing, deselection, address transitions, and re-entry from a retention-only condition remain explicitly timed or conditioned operations.

This extends Case 06's distinction between **state-holding stability** and **transition/recovery dynamics** into semiconductor arrays.

---

## Bistability is margin-bounded

### H/P

The Fairchild patent compares operating arrangements in terms of threshold sensitivity, current transients, write speed, power dissipation, and noise immunity. It identifies one half-select arrangement as particularly sensitive to threshold variation and therefore problematic for yield, and compares alternative modes/circuits with different noise margins and power/write tradeoffs.

Pashley's Intel patent does not publish a static-noise-margin number for a named commercial part, but it does make two additional finite-margin problems explicit at the array interface: small column-line signals must be sensed reliably despite capacitance, and address-transition skew must not produce multiple selection.

These are source-specific engineering statements. They should not be converted into an unsourced hold/noise-margin number for the 1101A or 2102.

### E

The bounded cross-case lesson is:

> **bistability ≠ unlimited state-holding margin**.

and, separately:

> **a valid held state does not by itself guarantee valid selection or sensing.**

A cell can have two intended logical conditions while retention and successful access remain dependent on finite electrical/process margins and on the bias and timing conditions of the surrounding array.

This deepens, rather than replaces, the existing distinction `cell bistability ≠ array-memory semantics`.

---

## Cell retention is not array organization

### H/P

Vadasz et al. distinguish MOS storage arrays from drive, sense, and decode circuitry. Their p. 47 Intel-1101 example uses parallel address connections and chip-select inputs to choose memory units. Intel's 2102 block diagram likewise separates cell array, row selector, column selection, input control, and external I/O/control.

Fairchild US3530443A also places a storage cell within word/bit-line array conditions rather than treating the state-holding pair as a complete memory service in isolation.

Pashley's Intel filing makes this separation even more explicit within one manufacturer-primary design: bistable cells, X/Y decoding, paired column lines, column sense amplifiers, a common read bus, output buffering, write paths, and address buffers are separate circuit roles.

### E

The retained state of one cell is only one analytical layer:

```text
cell-level stable state
    ≠ electrical hold margin
    ≠ array grouping
    ≠ row/column or word/bit selection
    ≠ sensing margin
    ≠ address-transition integrity
    ≠ package selection
    ≠ architectural role
    ≠ cache policy
```

A static semiconductor cell does not become a `cache` merely because later caches are commonly built from SRAM. Cache requires placement, lookup/tag, replacement, visibility, hierarchy, and often coherence/consistency semantics that are outside this case.

---

## Failure and technical forgetting

### H/P

The grounded case now has several different bounded failure / validity boundaries:

- **Intel retention-condition boundary:** 5101L retention is guaranteed only down to its specified 2.0 V floor; Intel explicitly invokes battery backup when non-volatility is desired.
- **Fairchild electrical-margin boundary:** the 1968-filed patent discusses threshold sensitivity, current transients, noise immunity, and power/write tradeoffs across disclosed operating arrangements.
- **Intel access/sensing boundary:** Pashley's filing treats column-line capacitance and small-signal sensing as access constraints and explicitly prevents transient multiple selection by making address/complement transitions coincident.

Intentional write is also an explicit state replacement operation in these static-memory families.

### E

For this case, forgetting/unavailability can therefore occur through at least:

1. **supply-condition loss** — the electrical condition required for retained state is no longer guaranteed;
2. **insufficient electrical hold margin / disturbance** — a retained distinction can fail to remain if the actual cell leaves its valid stability regime;
3. **intentional rewrite** — a later write establishes another stable logical condition;
4. **selection failure** — an intact cell state can be addressed incorrectly or multiply selected because the decoder/address-transition relation fails;
5. **sensing / I/O failure** — an intact selected state can fail to be recovered correctly through the column/sense/output path.

The last two are especially important because they show that **technical unavailability does not imply physical loss of the held bit**.

The 5101L provides a device-specific retention-supply boundary; Fairchild supplies explicit generic period hold/noise-margin discussion; Pashley supplies Intel manufacturer-primary selection/sensing constraints. Exact 1101A/2102 static-noise-margin values remain a product-specific archival question, not a prerequisite for the bounded regime claim.

---

## Comparison with grounded Case 06 and DRAM

| Dimension | Case 06: thermionic flip-flop | Case 07: grounded static MOS RAM | Grounded DRAM case |
| --- | --- | --- | --- |
| state holding | regenerative bistability | DC-stable / cross-coupled bistable semiconductor state; Intel/Pashley directly grounds one manufacturer-primary static cell design | decaying storage-node charge in bounded 1T1C regime |
| power | powered operating condition | powered; 5101L additionally separates low-V retention from ordinary operation | powered system plus scheduled regeneration |
| periodic refresh merely to remain | not established | explicitly unnecessary in cited Intel static devices; Fairchild also distinguishes static from a separate dynamic mode | required in bounded dynamic regime |
| read | state can condition later gates nondestructively | Intel 2102 / 5101 nondestructive read; Pashley separately exposes sense-path constraints | device/regime dependent; bounded Dennard 1T1C destructive, later commercial examples can be nondestructive |
| access organization | often directly wired into counters/controls; higher organization external | array + X/Y decode + access devices + complementary column lines + sensing + chip/interface control | decoded array + sense/restore infrastructure |
| holding constraints | circuit operating condition + stability | supply + finite electrical/process margin; exact values claim/device specific | leakage deadline + sense/restore margins |
| timing problem | set / trigger / recovery margins | access/write/select timing + address-transition integrity + sensing + retention-to-operation recovery | access timing + refresh deadline + restore |

The result is not that SRAM is merely a smaller flip-flop or a faster DRAM. The cases expose different combinations of **state-holding relation, electrical support, array organization, maintenance trigger, access semantics, and engineering margin**.

---

## Functional analogies and prohibited collapses

### A — useful bounded analogy

A static MOS memory cell is **flip-flop-like in a historically supported sense**: period sources explicitly use flip-flop / bistable / cross-coupled language for MOS storage, and bounded static devices maintain state without scheduled refresh.

### X — do not infer

- `static = nonvolatile without power`;
- `static = no timing constraints`;
- `cross-coupled = automatically static under every bias/array regime`;
- `static cell = register`;
- `static RAM = cache`;
- `all early static RAM = modern six-transistor CMOS SRAM`;
- `six MOS devices = canonical CMOS 6T SRAM`;
- `NASA 1970 generic cell = Intel 1101/2102 transistor-level schematic`;
- `Fairchild US3530443A = Intel 1101/2102 transistor-level schematic`;
- `Intel US3946369A = Intel 2102/2102A`;
- `Intel US3706079A = static-cell evidence`;
- `no refresh = maintenance-free system`;
- `cell retains state = decoder/sense/interface must return it correctly`.

---

## Philosophical / conceptual interpretation

### I — quiescence can be conditional rather than autonomous

The case sharpens `quiescent retention`. A state may require **no recurring state-restoration event** while still depending on a continuously satisfied electrical condition and finite operating margins. `Nothing has to be rewritten yet` and `nothing has to be supplied or constrained` are different propositions.

### I — retention can have a lower-power mode than availability

The 5101L adds a useful complication to the project's availability/addressability work without collapsing into philosophical vocabulary: a state can continue to count as retained under a lower-voltage condition while ordinary active service is not yet restored. Retention and full callability are therefore not identical operational states.

### I — a retained state and its recoverability path can fail separately

Pashley's cell/sense/decode separation makes another conceptual boundary concrete. A bit can remain in a valid bistable condition while the system's ability to designate, select, sense, or return it is compromised. This is a technical instance of the repository's broader distinction between **state survival** and **recoverability/serviceability**; it is not a claim that Intel used that philosophical vocabulary.

---

## Evidence status and remaining cleanup

This case is now **`grounded`** for the bounded static-MOS retention comparison.

The promotion does **not** mean that every product-specific topology question is solved. It means the central regime no longer depends on a neighboring vendor's cell or on package-level behavior alone: Intel/Pashley US3946369A supplies manufacturer-primary cell/array mechanism evidence, while Intel catalog documentation supplies product-level static/no-refresh/nondestructive-read and 5101L retention-mode behavior.

### Strongly supported now

- period MOS flip-flop / bistable / cross-coupled storage vocabulary;
- a 1968-filed primary Fairchild cell design with explicit static-storage operation;
- separation of standby/address/read/write conditions within a period static-MOS array discussion;
- period evidence that `static` and `dynamic` can be operating regimes requiring source-controlled bias/maintenance analysis rather than merely modern topology labels;
- Intel static-versus-dynamic product classification;
- no clock/refresh requirement for the cited Intel static devices;
- nondestructive read for the cited Intel devices;
- decoded array / chip-selection organization;
- explicit low-voltage data-retention mode and operation recovery in the 5101L family;
- generic period evidence that threshold/noise/power margins constrain usable cell operation;
- Intel manufacturer-primary `1024 × 1`, `32 × 32`, +5 V static-RAM cell/array design with explicit bistability and inter-branch feedback;
- manufacturer-primary separation between held cell state, selection, sensing, address-transition integrity, and output path.

### Archival / product-specific cleanup still open

1. directly inspect a full, reliably renderable facsimile of Vadasz–Chua–Grove 1971 pp. 43 and 47 rather than treating indexed page text as visual inspection;
2. if an exact commercial-topology claim is later needed, obtain an explicit manufacturer-primary link from a transistor-level cell to the 1101/1101A/2102/2102A rather than identifying Pashley's design by resemblance;
3. recover an Intel-product-specific static hold/noise-margin account beyond the already grounded 5101L retention-supply boundary and Pashley's access/sensing constraints;
4. keep bipolar static memories and later canonical CMOS six-transistor SRAM separate unless they change the retention comparison;
5. interpret the Smithsonian 1101 mask only if layer documentation makes that interpretation defensible.

These tasks can deepen product genealogy and margins, but they no longer block the central static-MOS retention regime.

Cache remains separate. It should be opened as the next bounded bridge only at the **policy / hierarchy / identity / replacement** layer, not as another cell-topology survey.

---

## Sources

### Primary / contemporary

1. Harold S. Crafts, Wendell B. Sander, James B. Angell, “MOS gated resistor memory cell,” US Patent 3,530,443, filed 27 November 1968, published 22 September 1970. <https://patents.google.com/patent/US3530443A/en>
2. L. L. Vadasz, H. T. Chua, A. S. Grove, “Semiconductor random-access memories,” *IEEE Spectrum* 8(5), May 1971, pp. 40–48. Relevant indexed locations: p. 43 (MOS flip-flops / static MOS cell), p. 47 (fully decoded static MOS / Intel 1101 system example). Exact facsimile inspection remains open. <https://www.worldradiohistory.com/Archive-IEEE/1971/IEEE-Spectrum-1971-05.pdf>
3. J. P. Green, A. L. Kosmala, F. H. Martin, *Engineering Study for a Mass Memory System for Advanced Spacecrafts*, NASA-CR-108672, 1 August 1970, Fig. 2.6.10 `Static MOS Memory Cell`. <https://ntrs.nasa.gov/citations/19710005248>
4. Intel Corporation, *Intel Data Catalog*, 1975. RAM selection guide p. 2-2; Intel 1101A pp. 2-3–2-5; Intel 2102 p. 2-33; Intel 5101 / 5101L pp. 2-115–2-116. <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/1975_Intel_Data_Catalog.pdf>
5. Richard D. Pashley, “High speed MOS RAM employing depletion loads,” US Patent 3,946,369, assigned to Intel Corporation, filed 21 April 1975, published 23 March 1976. Figure 1 and its detailed description are the central manufacturer-primary cell/array anchors. <https://www.freepatentsonline.com/3946369.html>
6. Leslie L. Vadasz, Joel A. Karp, “Three-line cell for random-access integrated circuit memory,” US Patent 3,706,079, filed 16 September 1971, published 12 December 1972. Used here as an explicit dynamic-cell negative control, not as evidence for Intel static topology. <https://patents.google.com/patent/US3706079A/en>

### Secondary / institutional context

7. Computer History Museum, *The Storage Engine*, “1970: Semiconductors compete with magnetic cores.” Chronology only; central mechanism claims above do not depend on it. <https://www.computerhistory.org/storageengine/semiconductors-compete-with-magnetic-cores/>

---

## Grounded conclusion

The static-semiconductor bridge survives source deepening and can now be treated as grounded for its bounded retention question.

What carries over from the grounded thermionic flip-flop case is **powered quiescent state holding without scheduled refresh**. The Fairchild 1968-filed disclosure makes one early MOS implementation family concrete; Intel's product documentation shows how static state holding is exposed as a decoded commercial memory service and, in the 5101L, how retention can have a lower supply condition than ordinary operation. Pashley's 1975 Intel filing then closes the remaining manufacturer-primary mechanism gap by placing an explicitly bistable, feedback-coupled static cell inside a 1024 × 1 decoded/sensed array.

Three corrections matter most:

> **static retention is neither unpowered retention nor an ideal Boolean state outside electrical margins.**

> **cell retention, selection integrity, and sensing/recovery are distinct mechanism layers.**

> **manufacturer-primary static-cell evidence does not license an unsourced commercial-model identity or a universal modern CMOS 6T topology.**

Case 07 is therefore closed as a bounded static-MOS substrate/array bridge. Exact 1101/2102 product genealogy and Vadasz facsimile inspection remain archival cleanup; the next new technical question should move upward to cache semantics rather than continuing to accumulate generic SRAM history.