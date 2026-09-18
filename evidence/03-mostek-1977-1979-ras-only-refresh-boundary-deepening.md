# Case 03 evidence deepening — Mostek MK4116 RAS-only refresh, 1977–1979

**Status:** `bounded deepening complete`

## Research question

Case 03 already grounds DRAM as deadline-driven restoration and, with Intel's 1982 2164A / 1984 8203 evidence, separates payload state from refresh timing, traversal, and arbitration state.

This bounded slice asks an earlier and narrower question:

> By the late 1970s, how did a commercial 16K DRAM document the relation among ordinary memory cycles, RAS-only refresh, full-row coverage, low-power standby, and external refresh-support logic?

The aim is not a general Mostek history and not an invention-priority claim. It is to tighten a terminology and trigger boundary that matters across Case 03 and Synthesis 25:

> **an ordinary access may earn refresh credit for one row without making the retention regime access-triggered.**

The slice also fixes two additional boundaries:

> **RAS-only refresh != autonomous/self refresh**

and

> **low-power standby retention != maintenance-free retention**.

---

## Source custody and dating

### Primary vendor anchor — 1979 Mostek data book

Mostek's *1979 Memory Data Book and Designers Guide* contains an MK4116 entry listing:

- `Read-Modify-Write, RAS-only refresh, and Page-mode capability`;
- `128 refresh cycles (2 msec refresh interval)`.

Archival scan:

- MOSTEK, *1979 Memory Data Book and Designers Guide*, Bitsavers: <https://www.bitsavers.org/components/mostek/_dataBooks/1979_Mostek_Memory_Data_Book_and_Designers_Guide_Mar79.pdf>

A second Bitsavers scan of the same year's book exposes the same feature wording:

- <https://www.bitsavers.org/components/mostek/_dataBooks/1979_Mostek_Memory_Data_Book_and_Designers_Guide.pdf>

This vendor book establishes the historical floor used in this note: by 1979, Mostek itself publicly documented `RAS-only refresh`, 128-cycle coverage, and a 2 ms interval for the MK4116 family.

### Primary vendor mechanism scan — later Mostek-branded MK4116 datasheet copy

A surviving standalone MK4116-2/-3 datasheet scan carries `UNITED TECHNOLOGIES MOSTEK` branding. Because that corporate header is later than the 1979 data-book anchor, this note does **not** use the standalone scan to date the mechanism to 1979 by itself.

It is used instead to inspect detailed vendor wording that is consistent with the product-family feature already present in the 1979 Mostek book:

- Mostek, `MK4116(J/N/E)-2/3`, surviving datasheet scan: <https://www.minuszerodegrees.net/memory/4116/datasheet_MK4116-2_and_MK4116-3.pdf>

The scan states that refresh of the dynamic-cell matrix is accomplished by performing a memory cycle at **each of the 128 row addresses within each 2 ms interval**. It separately states that **any normal memory cycle** performs the refresh operation for the selected row, while `RAS-only` cycles are the easiest way to carry out the full refresh function and substantially reduce operating power.

The same scan describes refresh current as `RAS cycling, CAS = VIHC`, and in its battery-standby discussion says VCC may be removed without affecting refresh/data retention while system logic other than the **RAS timing circuitry and refresh address logic** may be turned off.

### Period secondary witness — 1977 system design literature

A contemporary *Electronic Design* article dated 5 July 1977 discusses interfacing Z80 systems to 16-pin dynamic RAM and explicitly names the Mostek MK4116. It states that the MK4116 requires **128 refresh cycles every 2 ms** and that memory is refreshed by a read/write cycle or a **RAS-only refresh cycle**.

Source:

- *Electronic Design*, vol. 25 no. 14, 5 July 1977, p. 68, World Radio History scan: <https://www.worldradiohistory.com/Archive-Electronic-Design/1977/Electronic-Design-V25-N14-1977-0705.pdf>

This is useful as a period system-design witness that RAS-only refresh and the 128-cycle / 2 ms relation were already being discussed around the MK4116 in 1977. It is **not** substituted for the vendor source and does not establish invention priority or exact product-introduction date.

---

## Historical record

### H/P — the 1979 Mostek product contract exposes both coverage count and deadline

The 1979 Mostek data book lists two facts together:

```text
128 refresh cycles
    +
2 ms refresh interval
```

The detailed product-family datasheet makes the relation explicit: each of the 128 row addresses must receive a qualifying memory cycle during each 2 ms interval.

This is stronger than the statement `the chip needs refresh`. It exposes two separate obligations:

1. **deadline** — the relevant coverage must occur inside the bounded interval;
2. **coverage** — the work must reach the full row-address set rather than merely occur 128 times without regard to address.

The vendor record therefore supports:

> **refresh activity exists != refresh obligation satisfied**.

### H/P — ordinary reads/writes can refresh, but are not guaranteed to close the coverage obligation

The MK4116 documentation states that any normal memory cycle performs the refresh operation for the row addressed by that cycle.

That creates an important historical interface relation:

```text
foreground read/write cycle to row R
    -> useful memory operation
    + refresh credit for row R
```

But the same document still requires all 128 row addresses to be serviced within 2 ms.

Nothing in the inspected source says an arbitrary user workload is guaranteed to visit every row before the deadline. Therefore normal accesses can contribute maintenance work without converting the underlying retention obligation into `access-triggered restoration`.

### H/P — RAS-only refresh removes the column/data phase, not the row-maintenance obligation

The MK4116 identifies `RAS-only refresh` as a supported operating mode. Its electrical table describes refresh current with RAS cycling while CAS remains high. The addressing section says the externally applied RAS latches the row address; CAS subsequently latches the column address for ordinary access.

The refresh section then says RAS-only cycles are the easiest way to perform refresh and reduce operating power.

Historically, the operation therefore permits the system to perform row restoration without carrying out the full column/data-access path of a normal memory cycle.

The source does **not** say that row addresses, timing, or refresh scheduling disappear.

### H/P — battery standby preserves less logic than normal operation, but not zero refresh infrastructure

The standalone Mostek-family datasheet says VCC can be removed in battery standby without affecting refresh operation/data retention and that system logic may be turned off **except** for RAS timing circuitry and refresh address logic.

This is an unusually direct product-level boundary:

```text
normal useful memory service stopped
    !=
retention work stopped
```

and:

```text
reduced-power standby
    !=
passive nonvolatile persistence
```

The retained payload remains dependent on recurring row refresh plus the external/support logic needed to generate it.

### H/S — 1977 period design literature treats ordinary cycles and RAS-only cycles as alternate ways to satisfy row refresh work

The July 1977 *Electronic Design* article says the MK4116 requires 128 refresh cycles per 2 ms and that a read/write cycle or RAS-only cycle can refresh the memory. Its system discussion also treats timing/address generation as a board/system design problem rather than an invisible autonomous action inside the DRAM.

This contemporaneous evidence supports the bounded historical interpretation that system designers were already reasoning about refresh as a scheduling/coverage obligation that could be serviced by useful accesses or explicit maintenance cycles.

It does not prove every 1977 MK4116 system used the same controller or schedule.

---

## Engineering reconstruction

### E — refresh credit and refresh trigger are different relations

The strongest result of this slice is:

```text
operation that earns maintenance credit
    !=
condition that makes maintenance due
```

For the MK4116, a normal read/write cycle can refresh the selected row. Nevertheless, elapsed time plus complete row coverage remain the retention obligation.

Therefore:

> **opportunistic refresh by access != access-triggered retention regime**.

A row may be refreshed because an ordinary access happens to service it, while another untouched row still becomes due solely because the global 2 ms coverage window is advancing.

This prevents a taxonomy error in Synthesis 24: the response may be piggybacked on access even when the trigger remains deadline-driven.

### E — activity count and set coverage are separable

A naive controller could perform many cycles yet repeatedly revisit the same rows. The documented contract is not merely `do 128 things`; it is `perform a qualifying cycle at each of 128 row addresses within the interval`.

Thus:

```text
number of refresh-capable cycles
    !=
proof of row-set coverage
```

and:

```text
refresh cadence
    !=
refresh traversal state
```

The later Intel 8203 evidence in Case 03 makes the corresponding control-state decomposition explicit with separate timer and row counter. The MK4116 product contract shows why such separation is logically necessary even before that later named controller is considered.

### E — RAS-only is an operation-form optimization, not autonomy

In the bounded MK4116 interface:

- RAS selects/latches a row;
- CAS selects/latches the column phase for normal access;
- refresh can be carried out with RAS cycling while CAS remains inactive/high.

The maintenance operation is therefore cheaper/simpler than a full useful access, but it still requires the system to provide the row-selection sequence and timing.

Hence:

> **RAS-only refresh != self-refresh**.

And, compared with Intel 2164A terminology:

> **RAS-only refresh != Hidden Refresh**.

The names answer different interface questions. `RAS-only` describes a refresh cycle that omits the column phase. Intel's later `Hidden Refresh` describes a mode in which useful output can remain visible while refresh occurs. Neither term should be silently used as a synonym for autonomous refresh.

### E — standby shifts the retention boundary rather than abolishing it

The battery-standby passage allows much of the surrounding system to power down while retaining the RAS timing and refresh-address path.

So the system crosses from:

```text
full useful-service apparatus
```

into:

```text
minimum-enough retention apparatus
```

This makes `standby` analytically valuable. It reveals which infrastructure is constitutive of retaining the state and which infrastructure is only required for normal service.

The evidence does not establish one universal minimum-retention circuit for all DRAM systems. It establishes this product-family boundary.

### E — maintenance can be hidden in useful work without becoming free

If an ordinary read/write visit refreshes a row, some retention work is supplied as a side effect of foreground work. That does not make the maintenance cost disappear:

- unvisited rows still need explicit servicing;
- row coverage still has to be coordinated;
- the 2 ms deadline still applies;
- standby still retains refresh timing/address infrastructure.

Thus:

> **maintenance piggybacked on useful work != maintenance obligation eliminated**.

---

## Functional comparisons — not genealogy

### A — Case 09, Intel 1103 external scheduling

Case 09's 1103 evidence exposes a bounded product contract of 32 refresh cycles / 2 ms and a separate controller implementation that derives cadence, traversal, and arbitration.

The MK4116 comparison sharpens the same abstract distinction at a denser 128-row geometry and adds an explicit statement that ordinary accesses may count toward refresh.

Functional comparison:

```text
device-level deadline/coverage contract
    !=
controller implementation used to satisfy it
```

No Mostek -> Intel or Intel -> Mostek genealogy is asserted.

### A — Intel 2164A / 8203 in Case 03

The later Intel evidence gives explicit historical names for `Hidden Refresh`, a refresh timer, refresh counter, and arbitration.

The MK4116 evidence supplies an earlier product-interface contrast:

```text
RAS-only refresh
    -> omit column/data phase

Hidden Refresh
    -> bounded output/interface visibility behavior

external timer/counter
    -> schedule + traversal control state
```

These mechanisms are functionally comparable but not interchangeable vocabulary.

### A — Case 105, LPDDR2 per-bank refresh

Case 105 later shows controller/device coordination in a bank-local refresh regime, including bank-target tracking and whole-device accounting.

The functional commonality is only this:

> one maintenance action can have a local target while the retention obligation is defined over a larger set and interval.

The standards, interfaces, device organizations, and historical lineages are different.

---

## Philosophical interpretation — bounded

### I — inactivity at the useful interface can coexist with active retention labor

The MK4116 standby boundary is a compact counterexample to an intuitive equation between `idle` and `nothing happening`.

At the useful-service layer, the memory system can enter a reduced-power standby state. At the retention layer, RAS timing and row-address progression still have work to do.

The restrained interpretive point is:

> **technical quiescence is layer-relative: useful service may pause while constitutive maintenance continues.**

This does not imply that every technical persistence is operationally active, and it does not override the repository's quiescent-retention counterexamples such as magnetic remanence.

### I — maintenance can disappear from observation without disappearing from ontology

When an ordinary memory access also refreshes a selected row, the foreground operation and preservation operation coincide physically for part of the system's obligation.

That coincidence can make maintenance less visible to an observer who sees only successful reads/writes. The remaining rows and the deadline show why the maintenance relation is still analytically real.

This is a philosophical reading downstream of the engineering contract, not historical Mostek vocabulary.

---

## Explicit non-claims

This evidence does **not** claim that:

1. Mostek invented DRAM refresh;
2. Mostek invented RAS-only refresh;
3. 1977 is the exact MK4116 introduction date;
4. the 1977 *Electronic Design* article is a Mostek-authored source;
5. the later `UNITED TECHNOLOGIES MOSTEK` standalone datasheet scan itself proves a 1979 publication date;
6. every MK4116 revision had byte-for-byte identical documentation or timings;
7. every normal access pattern automatically refreshes all rows in time;
8. a high number of refresh-capable cycles proves complete row coverage;
9. RAS-only refresh is self-refresh;
10. RAS-only refresh is identical to Intel 2164A Hidden Refresh;
11. the DRAM internally owns the full refresh-address counter merely because a RAS-only cycle refreshes a row;
12. battery standby makes the MK4116 nonvolatile;
13. VCC removal means all power rails may be removed;
14. standby retention proves that no external timer/address logic is needed;
15. CAS remaining high means row selection no longer matters;
16. one product-family 2 ms interval is a timeless universal DRAM constant;
17. 128 refresh cycles means `any 128 row cycles` independent of address;
18. a normal read/write's refresh side effect turns the system into an access-triggered retention regime;
19. access-piggybacked maintenance is costless;
20. later self-refresh DRAM descends directly from this specific MK4116 mode;
21. the 1977 design article's example controller is the only or canonical MK4116 refresh implementation;
22. the Mostek product evidence establishes invention priority over Intel, TI, NEC, Motorola, or other DRAM vendors;
23. low-power standby and modern DRAM self-refresh are historically or electrically identical;
24. the source establishes exact refresh-cursor persistence across reset or power loss;
25. this bounded slice is a substitute for a broader Mostek / 16K-DRAM technical history.

---

## Claim ledger

| Claim | Type | Status |
| --- | --- | --- |
| Mostek's 1979 data book lists MK4116 RAS-only refresh | H/P | grounded by vendor data book |
| Mostek's 1979 data book lists 128 refresh cycles / 2 ms | H/P | grounded by vendor data book |
| detailed MK4116-family docs require a cycle at each of 128 row addresses within 2 ms | H/P | grounded by vendor-family datasheet scan |
| any normal cycle can refresh its selected row | H/P | grounded by vendor-family datasheet scan |
| RAS-only refresh is identified as a lower-power/easier explicit refresh path | H/P | grounded by vendor-family datasheet scan |
| refresh current is specified with RAS cycling and CAS inactive/high | H/P | grounded by vendor-family datasheet scan |
| battery standby can remove VCC while retaining RAS timing + refresh-address logic | H/P | grounded by vendor-family datasheet scan |
| 1977 period design literature discusses MK4116 128-cycle / 2 ms and RAS-only refresh | H/S | grounded by contemporaneous trade press |
| access can earn refresh credit while trigger remains deadline-driven | E | bounded reconstruction |
| cycle count does not by itself prove full row-set coverage | E | bounded reconstruction from vendor contract |
| RAS-only refresh does not establish autonomous/self refresh | E | bounded reconstruction |
| low-power standby retention still depends on retained maintenance apparatus | E | bounded reconstruction |
| RAS-only, Hidden Refresh, and self-refresh should remain distinct terms | A/E | bounded cross-case terminology rule |
| useful-interface inactivity can coexist with active retention maintenance | I | bounded interpretation |

---

## Prior-art boundary

The defensible chronology from this slice is deliberately narrow:

- by **5 July 1977**, period system-design literature discussing the MK4116 described 128 refresh cycles per 2 ms and RAS-only refresh;
- by **1979**, Mostek's own memory data book explicitly listed `RAS-only refresh` and `128 refresh cycles (2 msec refresh interval)` for the MK4116;
- the inspected detailed Mostek-family datasheet makes explicit that normal memory cycles may perform row refresh while the full 128-row / 2 ms obligation remains, and that battery standby still retains RAS timing and refresh-address logic.

This is a historical floor for the inspected public record. It is not a first-use, first-invention, or direct-genealogy claim for `refresh`, RAS-only refresh, external refresh counters, or low-power DRAM standby.

The repository's existing 1947–1976 terminology evidence remains the appropriate earlier anchor for `recirculation`, `regeneration`, and early semiconductor `refresh` vocabulary. This slice adds a late-1970s commercial-product interface boundary rather than replacing that chronology.

---

## Related-repository boundary

A fresh search of `tmzncty/computing-archaeology` for `MK4116` found no dedicated packet to reuse.

`technical-retention` should therefore retain only the bounded seam developed here:

```text
row-level refresh credit from normal or RAS-only cycle
    -> complete 128-row coverage obligation
    -> 2 ms deadline
    -> external/support timing + address logic
    -> standby retention with reduced useful-service apparatus
```

A broader history of Mostek, 16K DRAM competition, MK4116 process/design revisions, Apple/Commodore/early-microcomputer adoption, controller boards, vendor cross-licensing, and later self-refresh genealogy belongs primarily in `computing-archaeology` rather than being recreated here.

---

## Remaining evidence debt

This bounded slice closes the trigger/credit/standby terminology question but leaves several narrower historical tasks open:

- obtain and directly inspect a dated 1977–1978 Mostek MK4116 vendor datasheet or data-book facsimile to tighten the vendor chronology before the 1979 book;
- trace the earliest Mostek use of the exact phrase `RAS-only refresh` without turning that into invention priority;
- compare period controller application notes to determine how often designers actually relied on foreground-access refresh credit versus dedicated refresh cycles;
- trace when `self-refresh` became a distinct vendor/standards term and keep it separate from earlier RAS-only modes;
- investigate whether any period MK4116 standby implementation retained refresh traversal state across particular reset/power-fail regimes.

None of those debts blocks the bounded conclusion established here.