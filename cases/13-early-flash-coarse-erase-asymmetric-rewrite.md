# Early Flash EEPROM: Coarse Erase, One-Transistor Density, and Asymmetric Rewrite

## Status

**`grounded`** — bounded to a 1980–1988 transition documented by Toshiba/Masuoka primary patent evidence, the indexed abstract of the 1984 IEDM `Flash E²PROM` paper, an Intel 1988-filed Flash patent, and the indexed abstract of Intel's 1988 JSSC in-system Flash paper.

Grounding record: [`../evidence/13-early-flash-coarse-erase-1980-1988-grounding.md`](../evidence/13-early-flash-coarse-erase-1980-1988-grounding.md).

## Scope

This case is not a general history of Flash memory, NOR, NAND, EEPROM, or SSDs.

It asks one bounded retention question:

> What changes when an electrically erasable nonvolatile memory deliberately shares erase infrastructure across many cells, preserving fine-grained read/program selection while making deliberate forgetting much coarser?

Case 12 established that electrical erasure does **not** itself determine erase granularity: Intel's 2816 supports selected byte erase and whole-chip erase.

Case 13 studies a different design regime. In the early Flash sources used here, a one-transistor/high-density cell is paired with erase control shared across many cells, culminating in period designs where the array is electrically erased together while programming remains address-selected.

The retention-specific transition is therefore not merely:

```text
EEPROM
    ->
Flash
```

It is:

```text
fine-grained electrical alteration
    ->
shared / coarse erase authority
    +
fine-grained read/program selection
    +
higher-density one-transistor cell objective
```

That asymmetry later becomes one of the physical conditions to which mapping/copy/reclaim systems such as Case 04 respond. It does **not** mean an early Flash chip already contains an FTL.

## Primary evidence boundary

The central sources are:

1. Fujio Masuoka and Hisakazu Iizuka / Toshiba, US4531203A, **_Semiconductor memory device and method for manufacturing the same_**, Japanese priority 20 December 1980, U.S. filing 13 November 1981;
2. F. Masuoka et al., **“A new flash E²PROM cell using triple polysilicon technology,”** IEDM 1984, pp. 464–467, DOI `10.1109/IEDM.1984.190752`;
3. Jerry A. Kreifels et al. / Intel, US5053990A, **_Program/erase selection for flash memory_**, filed 17 February 1988;
4. V. N. Kynett et al., **“An In-System Reprogrammable 32 K × 8 CMOS Flash Memory,”** _IEEE Journal of Solid-State Circuits_ 23(5), 1988, pp. 1157–1163, DOI `10.1109/4.5938`.

The Toshiba and Intel patents were directly inspected as full text. The 1984 IEDM and 1988 JSSC bibliographic records and abstracts were checked through scholarly indexes, but directly renderable full-paper facsimiles were not obtained in this slice. Figure-specific or exact-page claims from those papers therefore remain archival cleanup.

A 2023 retrospective by Stefan K. Lai is used only as **H/S** corroboration for Intel's later description of the cost/function tradeoff. It is not substituted for period evidence.

## Historical vocabulary

Period source vocabulary includes:

- `E²P-ROM` / electrically erasable and programmable read-only memory;
- `floating gate`;
- `erase gate`;
- `erase line`;
- `one transistor` / `single transistor per bit`;
- `Flash Electrically Erasable-PROM`;
- `flash EPROM`;
- `entire array` / simultaneous electrical erase;
- `command port`;
- `program verify`;
- `erase verify`;
- `in-system reprogrammable`.

Project comparison terms include:

- `erase domain`;
- `coarse erase`;
- `asymmetric rewrite granularity`;
- `retention dependency among neighbors`;
- `bulk forgetting`;
- `collateral state preservation`.

Those project terms are **E/A**, not historical quotations.

## Historical record

### H/P — density pressure existed before the named Flash paper

Masuoka and Iizuka's Toshiba patent begins from a concrete design comparison.

Its background describes a then-conventional electrically erasable cell using two transistors and states that this produces a density disadvantage relative to one-transistor UV EPROM. The disclosed design instead makes one electrically erasable memory bit from one MOS transistor containing floating, control, and erase gates.

The patent therefore does more than say `electrical erase is possible`.

It explicitly links:

```text
cell selection / erase structure
    ->
transistor count
    ->
packaging density
```

The patent also cites earlier single-transistor E²PROM work. It is therefore **not** evidence that this design was the universal first one-transistor electrically erasable memory.

### H/P — erase authority can be physically shared across cells

In the directly inspected Toshiba embodiment, one control gate is shared by two bits and one erase gate by four bits; later text says the erase-gate grouping may also be one or two cells.

The same patent describes:

- digit lines;
- select/control lines;
- erase lines;
- hot-carrier injection for writing;
- lower-voltage sensing for reading;
- high-field removal of charge toward the erase gate for erasing.

This matters because erase granularity is already visible as a **layout/control relation**, not merely a later software property.

The patent's own range of embodiments is a warning against overgeneralization:

> shared electrical erase does not automatically mean one universal erase unit.

### H/P — the 1984 IEDM source explicitly names the Flash regime and whole-array erase

The indexed abstract of Masuoka et al.'s 1984 IEDM paper describes a `Flash Electrically Erasable-PROM` cell with one transistor per bit.

It distinguishes:

- program by channel hot-carrier injection, similar to EPROM;
- simultaneous erasure of all memory-cell contents through field emission from floating gate to erase gate.

This supplies the missing period vocabulary and the explicit whole-array forgetting relation.

The source is used only at the abstract level until a directly inspectable facsimile of pp. 464–467 is obtained.

### H/P — Intel's 1988-filed Flash design preserves whole-array erase while programming by address

US5053990A uses the period term `flash EPROM` and explicitly describes Flash memories in which the entire array is simultaneously erased electrically while the cells use a single device per cell.

Its preferred embodiment is a 32,768 × 8, 256-Kbit array built from one-transistor Flash cells.

The physical operations remain asymmetric:

```text
erase
    high erase condition applied to the whole array

program
    address + data latched
    programming condition applied through selected X/Y path

read
    normal addressed sensing path
```

The patent's preferred cell uses hot-electron programming and Fowler–Nordheim tunneling erase. The exact device is sufficient for the bounded mechanism claim without assigning it to an unsupported catalog part number.

### H/P — coarse erase does not mean coarse control state

Intel's patent adds a layer absent from a simple `all bits erase together` description.

A command-port controller retains and decodes erase/program/read/verify commands, drives voltage generators, and performs a staged erase algorithm.

The erase sequence includes:

1. command setup and confirmation;
2. application of a whole-array erase condition;
3. erase verification by walking addresses;
4. another erase pulse if verification fails;
5. an error condition if the bounded retry/pulse limit is reached.

Thus the physical state change is coarse, but the control and diagnostic work is not.

> **coarse erase domain ≠ coarse verification granularity.**

### H/P — the 1988 Intel engineering paper exposes the time/granularity asymmetry

The indexed abstract of Kynett et al. reports a 32K × 8 CMOS Flash memory with a one-transistor cell and in-system reprogramming.

At the abstract level it reports:

- all cells in the array matrix electrically erased in about 200 ms;
- programming at about 100 µs per byte typical;
- a command-port interface for microprocessor-controlled reprogramming;
- more than 10,000 erase/program cycles demonstrated.

These values are **device-specific period evidence**, not universal Flash constants.

They show why the adjective `flash` must be handled carefully:

> a fast collective erase operation is not the same property as a fast arbitrary-byte rewrite operation.

### H/S — later Intel retrospective explicitly describes the cost/function compromise

Stefan K. Lai's 2023 account of ETOX NOR Flash describes the Intel development goal as combining EEPROM-like in-system alterability with a product cost approaching EPROM. It characterizes the resulting compromise as large-block rather than EEPROM-style single-byte alterability.

This later expert retrospective is useful because it makes the economic/architectural tradeoff explicit.

It is not used to establish what Toshiba engineers in 1980–1984 said, nor as proof of invention priority.

## Retained state and substrate

The retained state remains a nonvolatile floating-gate charge/threshold condition.

At idle:

```text
floating-gate charge condition
    ->
threshold / conduction distinction
    ->
recoverable bit without periodic refresh
```

Case 13 changes not the basic fact of nonvolatility but the **geometry of deliberate state change**.

A collection of otherwise independently readable/programmed bit states can share one erase authority.

Therefore the technically relevant retained object at update time is no longer only one cell:

```text
one target value to be changed
    exists inside
an erase domain containing other still-current values
```

Those neighboring values become operationally relevant because an erase event can destroy them too.

## Read / program / erase semantics

### Read

Read remains fine-grained through ordinary array addressing and sensing.

The bounded sources do not require bulk read merely because erase is bulk.

### Program

The Intel preferred embodiment latches address and data and applies program stress to the selected path. The Kynett abstract reports byte-rate programming.

Program granularity is therefore finer than erase granularity in this bounded regime.

### Erase

The 1984 Masuoka abstract and 1988 Intel patent both supply whole-array simultaneous electrical erase evidence for their bounded Flash designs.

The operation is neither `passive decay` nor `ordinary overwrite`. It is a privileged high-field intervention controlled by erase lines/voltage-generation and, in the Intel design, command/verify machinery.

## Why coarse erase changes retention

### E — one bit's revisability can depend on preserving neighboring state

Suppose one logical byte must change while the physical erase operation resets the whole array.

If the other bytes remain logically current, they must exist somewhere outside the erase event's destructive scope before the erase occurs and must later be restored.

In engineering terms:

```text
preserve still-current neighbors
    ->
bulk erase
    ->
reprogram intended current contents
```

The bounded early Flash device does not itself guarantee how a system performs that preservation. It may be host-managed or application-specific.

This is exactly where Case 13 must stop and Case 04 begins.

### E — bulk forgetting can be fast while selective rewriting remains expensive

Simultaneous erase amortizes one erase intervention over many cells.

But if only one logical value needed alteration, the system-level cost can include preservation and reconstruction of other data in the erase domain.

Therefore:

```text
fast physical bulk erase
    !=
cheap logical single-value update
```

This is an engineering consequence of the sourced geometry, not a claim that period authors used the term `amortization` in this sense.

### E — erase control is another retained/control state

Intel's command port, state registers, timers/counters, voltage-control paths, and verification loop show that `nonvolatile medium` does not mean `no operational state is needed to modify it safely`.

Modification depends on transient control state that orchestrates the destruction and reconstruction of persistent state.

That is different from DRAM refresh: the control work is not needed merely for a quiescent bit to survive. It is needed when intentional forgetting/reprogramming occurs.

### E — coarse state change can require fine-grained proof of success

Intel's whole-array erase is followed by address-walking verification.

So:

```text
state-change granularity
    !=
observation / verification granularity
```

A maintenance operation may be collective at the physical layer and selective at the diagnostic layer.

## From Case 12 to Case 13

Case 12 showed:

```text
electrical erasure
    can be byte-selectable
    and can coexist with chip erase
```

Case 13 adds:

```text
electrical erasure
    can deliberately become coarse
    while program/read remain fine-grained
```

The key transition is therefore not `optical -> electrical`; Case 12 already completed that transition.

The new axis is:

> **how much otherwise-current state shares one erase event?**

That is the device-level bridge needed before mapped Flash.

## From Case 13 to Case 04

Case 04 begins in the 1990s from a block-erase-before-write Flash substrate and asks how stable logical identity survives physical relocation, invalidation, transfer, and reclamation.

Case 13 supplies the prior device-level condition without projecting the later solution backward:

```text
Case 13
coarse erase domain
    +
finer program/read selection

        does not itself imply
        an FTL or mapping layer

Case 04
mapping + out-of-place update + transfer/reclaim
    make a constrained medium
    present a stable logical address space
```

Thus:

> **erase asymmetry is a precondition for the later retention problem; mapping is one historically later answer to it, not part of the early device definition.**

## Failure and forgetting

Relevant bounded failure classes include:

- **retention loss** — floating-gate state no longer supports the intended threshold distinction;
- **under-erase** — one or more cells remain insufficiently erased after the bulk operation;
- **over-erase / leakage vulnerability** — erase moves cells beyond a desired operating margin;
- **program failure** — the selected cell/byte does not reach the required programmed state;
- **verification failure** — state-changing work occurs but the system cannot establish that the array satisfies the required margin;
- **command/control error** — a destructive erase mode is invoked at the wrong time;
- **collateral loss** — still-current neighboring values are not preserved across a coarse erase event;
- **cycling wear** — repeated program/erase operations consume a finite endurance budget.

These are not one generic `data loss` category.

## Addressability, authority, and geometry

This case requires three different questions:

1. **Which state can be read?** — selected through ordinary address decoding;
2. **Which state can be programmed?** — selected through address/data and program paths;
3. **Which state must be erased together?** — determined by shared erase infrastructure and the device's erase mode.

For the bounded whole-array designs:

```text
read/program addressability
    is finer than
erase authority
```

Therefore `addressable` is not one scalar property of a memory device. Different state-changing operations can have different geometries on the same substrate.

## Maintenance and labor

No periodic refresh is required merely to keep the bounded floating-gate state.

But intentional modification requires substantial maintenance infrastructure:

- elevated-voltage generation/control;
- command sequencing;
- program/erase timing;
- verify operations;
- retry/error limits;
- preservation/reconstruction of unaffected logical data when the erase scope is broader than the intended logical edit.

The last item can lie outside the chip. The repository does not invent an internal controller where the source only establishes a media constraint.

## Functional analogy and anti-anachronism

Useful later comparisons:

- `erase domain`;
- `coarse-grained forgetting`;
- `collateral state preservation`;
- `asymmetric rewrite granularity`.

Do not project backward:

- `FTL`;
- `garbage collection`;
- `TRIM`;
- SSD `write amplification` as a named historical property;
- NAND page/block terminology where the bounded source is a whole-array Flash design;
- modern NOR sector architecture where the cited design erases the entire array.

The early sources establish a physical/control asymmetry. Later storage systems build additional abstractions over it.

## Philosophical limit

Case 13 supports one bounded interpretive question:

> What does it mean for a technical system to make forgetting collective even when use is selective?

A single retained value can be individually readable and programmable yet belong to a larger physical group that must be forgotten together.

This means technical individuality is operation-dependent: the unit that can be addressed is not necessarily the unit that can be erased.

That interpretation is grounded by the mechanism. It is not evidence that Toshiba or Intel engineers formulated a philosophy of collective forgetting.

## Cross-case results

Case 13 adds the following controls:

```text
program addressability
    !=
erase addressability
```

```text
electrical erasability
    !=
fine-grained erasability
```

```text
fast bulk erase
    !=
fast arbitrary rewrite
```

```text
coarse physical state change
    !=
coarse verification granularity
```

```text
early Flash erase geometry
    can create the retention problem later solved by
copy / reclaim / remapping

but
coarse erase
    !=
FTL
```

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Toshiba's 1980-priority patent explicitly treats the two-transistor E²PROM density penalty and discloses a one-transistor electrically erasable cell | H/P | directly inspected US4531203A |
| the Toshiba disclosure physically shares erase/control infrastructure across multiple cells in bounded embodiments | H/P | directly inspected US4531203A |
| Masuoka et al. 1984 use `Flash Electrically Erasable-PROM` and describe simultaneous erasure of all cell contents | H/P | indexed primary abstract; full facsimile pending |
| Intel's 1988-filed Flash patent defines a one-transistor 32K × 8 preferred embodiment with entire-array simultaneous electrical erase | H/P | directly inspected US5053990A |
| Intel's preferred embodiment programs through selected address/data paths while erase acts on the full array | H/P | directly inspected US5053990A |
| Intel's erase algorithm performs bulk erase pulses but verifies erased state address by address and retries when necessary | H/P | directly inspected US5053990A |
| Kynett et al. report whole-array erase in about 200 ms and typical programming around 100 µs/byte | H/P | indexed 1988 JSSC abstract; full facsimile pending |
| one-transistor/high-density Flash can historically be coupled to coarser/shared erase infrastructure | E grounded in H/P | Toshiba + Intel primary design evidence |
| every one-transistor EEPROM must erase an entire array | X | contradicted by prior/sibling architectures and by the Toshiba patent's own variable erase-gate sharing |
| `Flash` means NAND page/block erase in all periods | X | anachronistic / overbroad |
| whole-array erase proves that an early Flash device contained an FTL | X | no mapping-layer evidence; Case 04 is historically separate |
| Intel's 1988 patent is a proven exact catalog-part schematic | X | product identity not established in this case |
| Masuoka/Toshiba alone can be credited here with a universal invention claim for all electrically erasable one-transistor memory | X | source itself cites prior single-transistor E²PROM work; priority claim is broader than the bounded evidence |

## Related repositories

Searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Masuoka flash EEPROM` and `flash memory EEPROM NAND` returned no dedicated matching case during this slice.

This case therefore keeps only the retention-specific transition. A fuller fabrication/process history should be added there rather than duplicated here.

## Sources

### Primary / contemporary

1. Fujio Masuoka and Hisakazu Iizuka, **_Semiconductor memory device and method for manufacturing the same_**, US4531203A, priority 20 December 1980, filed 13 November 1981: <https://patents.google.com/patent/US4531203A/en>.
2. F. Masuoka et al., **“A new flash E²PROM cell using triple polysilicon technology,”** _1984 International Electron Devices Meeting_, pp. 464–467, DOI: <https://doi.org/10.1109/IEDM.1984.190752>. Abstract/bibliographic record checked; full facsimile remains archival cleanup.
3. Jerry A. Kreifels, Alan Baker, George Hoekstra, Virgil N. Kynett, Steven Wells, Mark Winston / Intel, **_Program/erase selection for flash memory_**, US5053990A, filed 17 February 1988: <https://patents.google.com/patent/US5053990A/en>.
4. V. N. Kynett et al., **“An In-System Reprogrammable 32 K × 8 CMOS Flash Memory,”** _IEEE Journal of Solid-State Circuits_ 23(5), 1988, pp. 1157–1163, DOI: <https://doi.org/10.1109/4.5938>. Abstract/bibliographic record checked; full facsimile remains archival cleanup.

### Secondary / retrospective

5. Stefan K. Lai, **“Development of ETOX NOR Flash Memory,”** in _75th Anniversary of the Transistor_, 2023, DOI: <https://doi.org/10.1002/9781394202478.ch16>. Used only for the later explicit cost/function framing.

### Internal comparison

6. [`12-intel-2816-eeprom-electrical-erasure.md`](12-intel-2816-eeprom-electrical-erasure.md) — byte/chip electrical erase and endurance-bounded forgetting.
7. [`04-flash-virtual-mapping-logical-identity.md`](04-flash-virtual-mapping-logical-identity.md) — later mapping/copy/reclaim layer built over block-erase-before-write Flash semantics.
