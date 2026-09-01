# DRAM 1967–1982 grounding record

This companion evidence record deepens [`cases/03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md). It is deliberately narrow: it verifies the case's central retention claims against exact primary-source locations, adds a commercial one-transistor/capacitor device, and grounds row-level sense/restore as actual manufacturer-documented practice rather than only an engineering reconstruction.

**Canonical maturity status is tracked in [`CASE_INDEX.md`](../CASE_INDEX.md).** This record does not turn the case into a general history of DRAM. A full semiconductor-memory lineage still belongs primarily in `tmzncty/computing-archaeology`.

## Grounding question

The case argues that DRAM makes persistence depend on a deadline: an information-bearing electrical state may remain locally quiescent for a while, but leakage means the system must revisit and restore it before the distinction becomes unrecoverable.

To promote the case beyond `first-pass`, four things need to be established independently:

1. the original 1967–1968 invention disclosure really does separate leakage-driven regeneration from access-triggered restore;
2. a commercial manufacturer actually sold a one-transistor/capacitor dynamic memory with mandatory refresh;
3. dynamic retention does not require destructive read;
4. commercial DRAM documentation makes sensing, amplification, return-to-cell, and row refresh explicit enough to ground the mechanism below the word `refresh`.

---

## Source A — Dennard US 3,387,286: invention-level mechanism

Robert H. Dennard, **“Field-effect transistor memory,”** U.S. Patent 3,387,286, filed 14 July 1967, issued 4 June 1968.

Google Patents transcription:
https://patents.google.com/patent/US3387286A/en

Public-domain scan:
https://commons.wikimedia.org/wiki/File:MOS_DRAM_patent.pdf

### A1. One field-effect transistor and one capacitor can retain one binary state

**Printed pp. 1–2; abstract and summary; FIG. 1.**

The patent describes an embodiment in which a binary value is represented by charge on a capacitor and the minimum cell uses one field-effect transistor to connect that storage element to the bit line.

This establishes the bounded physical substrate used by Case 03 without relying on later textbook terminology such as `1T1C`.

### A2. Leakage creates a maintenance obligation even without useful access

**Printed pp. 1–2 and pp. 5–6.**

Dennard explicitly contrasts capacitor storage with remanent storage: charge leaks with time, so information must be periodically `regenerated`. The detailed description gives recurring-cycle and sequential read/rewrite schemes for regeneration and notes that the required interval depends on capacitance, leakage paths, and temperature.

This grounds the case's central distinction:

> **time-triggered regeneration is not the same thing as access-triggered restore.**

### A3. The FIG. 1 embodiment has destructive read, but dynamic retention need not

**Printed pp. 5–6; FIG. 1 embodiment and later alternative cells.**

The one-transistor/capacitor embodiment is described as destructive: reading discharges the storage capacitor, so information that must remain has to be rewritten. The patent also discloses nondestructive-read alternatives using additional transistor structure.

Therefore the historical patent itself already warns against defining `dynamic` as `destructive read`.

---

## Source B — AMD Am9050, 1976: commercial one-transistor/capacitor dynamic memory

Advanced Micro Devices, **1976 AMD MOS/LSI Data Book**, `Am9050 — 4096-Bit Dynamic R/W Random Access Memory`.

Primary manufacturer PDF:
https://www.bitsavers.org/components/amd/_dataBooks/1976_AMD_MOS_LSI_Data_Book.pdf

### B1. Commercial manufacturer vocabulary: one transistor + small internal capacitor

**Printed p. 3-9, Functional Description.**

AMD describes the Am9050 as a 4096 × 1 dynamic random-access memory and states that its basic memory element is a **one-transistor cell that stores charge on a small internal capacitor**.

This is important for the project's anti-anachronism rule. The document itself gives the mechanism; the modern shorthand `1T1C` is useful for classification but need not be projected into the 1976 wording.

### B2. Mandatory refresh coexists with nondestructive read

**Printed p. 3-9.**

The same manufacturer description says the dynamic storage mechanism requires periodic refresh to maintain data integrity while also stating that readout is **nondestructive**, so rewriting after every ordinary read is not necessary.

This gives a strong commercial boundary for:

> **dynamic retention ≠ destructive read.**

The earlier Intel 1103 evidence in Case 03 already supported that distinction, but the Am9050 is stronger for this bounded question because the same source explicitly combines a one-transistor/capacitor cell with nondestructive read and periodic refresh.

### B3. Leakage and row-level refresh are described as ordinary operating semantics

**Printed p. 3-13, `REFRESH`.**

AMD explains that information is represented by presence or absence of charge in the memory cell; leakage currents eventually drain the charge and destroy the information unless it is restored. Each cell must be refreshed at least once every **2 ms**.

The array is described as 64 rows × 64 columns. Cycling any location in a row refreshes the 64 cells in that row, so all 64 row addresses must be accessed within the refresh interval.

This grounds three retention facts at once:

- the physical state has a bounded lifetime;
- refresh is organized above the individual cell;
- maintenance is temporally multiplexed across a row-oriented array.

---

## Source C — AMD Am9016, 1979: sense/restore circuitry is explicit infrastructure

Advanced Micro Devices, **1979 AMD The Designer's Guide**, `Am9016 — 16,384 × 1 Dynamic R/W Random Access Memory`.

Primary manufacturer PDF:
https://www.bitsavers.org/components/amd/_dataBooks/1979_AMD_The_Designers_Guide.pdf

### C1. Single-transistor charge storage remains the documented cell model

**Printed p. 3-63.**

AMD again describes the basic memory element as a single transistor storing charge on a small capacitor and specifies periodic refresh requirements for the device family.

This is not used to claim an invention priority. It is commercial implementation evidence for the mechanism family.

### C2. The block diagram exposes shared restoration machinery

**Printed p. 3-63, block diagram.**

The manufacturer block diagram explicitly includes:

- **128 sense-restore amplifiers**;
- sense and restore clocks;
- row and column decoders;
- the memory array around them.

This supports a central engineering claim already made in Case 03:

> increasing density at the retained-state site can move selection, sensing, and restoration complexity into shared array infrastructure.

Because the source is a later commercial device, it should not be read as a literal schematic of Dennard's 1967 FIG. 1 array.

---

## Source D — Intel AP-133, April 1982: sense, amplify, return, refresh

Intel Corporation, **Application Note AP-133, “Designing Memory Systems For Microprocessors Using the Intel 2164A and 2118 Dynamic RAMs,”** April 1982, Order Number 210431-001.

Contained in Intel memory-component handbooks; an accessible scan is available via Bitsavers:
https://bitsavers.informatik.uni-stuttgart.de/components/intel/_dataBooks/1984_Intel_Memory_Components_Handbook.pdf

### D1. Refresh is explicitly described below the interface metaphor

**Printed pp. 3-70 to 3-72; mechanism discussion on p. 3-72.**

AP-133 describes a DRAM storage cell as a transistor plus capacitor and explains that capacitor leakage eventually destroys the represented state. Refresh must therefore occur before the information degrades.

### D2. Commercial row refresh is sense → amplify → return to cell

**Printed p. 3-72.**

The application note explains that selecting a row transfers stored charge onto bit lines, where separate sense amplifiers detect and amplify the small signal; the restored value is then **returned to the cell**. A row-address operation therefore refreshes the row, and cycling all rows within the required interval maintains the array.

This is the primary manufacturer evidence needed to sharpen the word `refresh` into an actual retention operation:

```text
weak / decaying cell state
    -> row selection
    -> bit-line signal
    -> sense and amplification
    -> restored value returned to cell
```

This later source is used to ground commercial sense/restore practice, not to claim that every 1967–1982 DRAM implements an identical circuit.

---

## Evidence ledger: what is now grounded

| Claim | Type | Exact primary evidence | Status |
| --- | --- | --- | --- |
| Dennard disclosed one-transistor/capacitor storage | `H/P` | US 3,387,286, printed pp. 1–2, FIG. 1 | strong |
| capacitor leakage requires periodic regeneration independent of useful access | `H/P` | US 3,387,286, printed pp. 1–2 and 5–6 | strong |
| Dennard's FIG. 1 read is destructive and requires rewrite if state must remain | `H/P` | US 3,387,286, printed pp. 5–6 | strong |
| dynamic retention does not logically require destructive read | `H/P + E` | Dennard nondestructive alternatives; AMD Am9050 p. 3-9; existing Intel 1103 boundary | strong |
| a commercial one-transistor/capacitor DRAM required periodic refresh | `H/P` | AMD Am9050 p. 3-9 | strong |
| commercial refresh was specified as leakage-driven row maintenance on a 2 ms deadline | `H/P` | AMD Am9050 p. 3-13 | strong |
| sense/restore amplifiers and restore clocks were explicit commercial DRAM infrastructure | `H/P` | AMD Am9016 p. 3-63 | strong |
| row refresh can be implemented by sensing, amplifying, and returning state to cells | `H/P` | Intel AP-133 p. 3-72 | strong |
| stable logical address can conceal repeated physical restoration | `E` | cross-reading of the sources above | strong bounded reconstruction |
| DRAM is identical to Stieglerian tertiary retention or Heideggerian `Bestand` | `X` | not established by technical evidence | explicitly rejected |

---

## What the evidence changes conceptually

### 1. `Refresh` is not merely a timer event

The first-pass case correctly identified a deadline, but the commercial sources let us say more precisely what happens when the deadline is serviced. At least in the bounded commercial examples here, refresh is an **array operation that reconstructs a usable cell state through shared sensing/restoration circuitry**.

### 2. The retained object is not an uninterrupted packet of charge

The logical value survives even though the physical electrical quantity leaks and is periodically driven back into a recoverable state. The relevant continuity is therefore not identity of one unmodified physical token.

### 3. Shared maintenance is part of the density bargain

A tiny storage cell is not a complete self-sufficient memory. Row decoders, bit lines, sense/restore amplifiers, clocks, and refresh scheduling collectively make the minimal cell usable as retained state.

### 4. Dynamic retention names a deadline, not a read semantic

The Am9050 is especially useful because it explicitly combines:

- one-transistor/capacitor storage;
- nondestructive ordinary read;
- mandatory periodic refresh.

That is a direct commercial counterexample to any attempt to identify dynamic retention with destructive readout.

---

## Historical cautions

### Do not claim a commercial `first`

This record does not claim that the Am9050 was the first commercial 1T1C DRAM. Establishing commercial priority would require a separate product-history investigation across Mostek, TI, Intel, AMD, and other manufacturers.

### Do not equate product lineage with Dennard's exact embodiment

The evidence demonstrates a mechanism family and commercial practice. It does not prove that every later product directly implements the exact topology, timing, or circuitry shown in Dennard's FIG. 1.

### Do not back-project 1982 circuitry into 1967

Intel AP-133 is excellent primary manufacturer evidence for the sense/amplify/return operation in later commercial DRAM. It is not evidence that Dennard's original patent used the same sense-amplifier implementation.

### Do not expand this file into a general DRAM history

SDRAM/DDR timing, distributed refresh policies, row buffers, modern retention failures, ECC, RowHammer, package power, and controller policy remain outside this bounded grounding task.

---

## Related-repository boundary

`tmzncty/computing-archaeology` currently identifies SRAM / DRAM / ROM / EEPROM / Flash / cache / ECC as a missing historical middle. A full technical lineage should be built there.

This repository now has enough primary evidence for the narrower retention claim:

> **a logical DRAM state persists through bounded physical charge survival plus scheduled, shared reconstruction before a leakage deadline.**

That claim can be reused later without duplicating the full semiconductor-memory history.

---

## Readiness assessment

Case 03 now satisfies the repository's `grounded` criteria:

- strong primary invention evidence;
- exact page/figure anchors for central claims;
- period manufacturer vocabulary;
- commercial one-transistor/capacitor evidence;
- explicit sensing/restoration mechanism;
- maintenance and failure modes;
- a direct counterexample to `dynamic = destructive read`;
- anti-anachronism limits;
- related-repository duplication check.

Future DRAM work in `technical-retention` should therefore be narrow semantic or failure archaeology rather than adding generic device history.