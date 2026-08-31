# DRAM Refresh as Scheduled Restoration

## Scope

- **Object / system:** Robert H. Dennard's one-transistor / one-capacitor field-effect-transistor memory, with the Intel 1103 used only as a bounded commercial comparison.
- **Date range:** 1967–1975 for the central evidence used here.
- **Why this case matters for technical retention:** it separates two obligations that magnetic core had partially joined: **restoration caused by access** and **restoration caused merely by the passage of time**.

This case does **not** attempt a general history of DRAM, SDRAM, DDR, sense amplifiers, row-buffer organization, or modern refresh policy. Those belong primarily in `computing-archaeology` when that repository fills its identified semiconductor-memory gap.

The question here is narrower:

> What kind of persistence is it when the retained state is expected to decay even if nobody reads it, and the system must schedule work simply to keep the present state present?

---

## Historical vocabulary

The 1968 patent is titled **"Field-effect transistor memory"**, not "DRAM". It speaks of:

- `random access memory`;
- `memory cell`;
- `storage node`;
- `read-write cycle`;
- `destructive memory`;
- information being `retained in storage`;
- periodic `regeneration`.

Modern terminology such as **1T1C DRAM**, **refresh**, and **dynamic memory** is useful for classification, but it should not replace the patent's own vocabulary when describing what Dennard actually claimed.

A later Intel data catalog explicitly calls the 1103 a **1024-bit dynamic memory** and specifies a **refresh period**.

---

## Historical record

### H/P — Dennard's patent makes leakage constitutive, not exceptional

Robert H. Dennard filed U.S. Patent 3,387,286 on 14 July 1967; it was granted on 4 June 1968.

The abstract describes an embodiment in which each cell uses **one field-effect transistor and one capacitor**. Information is represented by whether the capacitor is charged. The same transistor connects the storage capacitor to the bit line for writing and reading.

Most importantly for this project, the patent states in its opening disclosure that the capacitor charge leaks away and therefore the stored information must be **periodically regenerated**.

The summary sharpens the point: capacitor storage is said not to be `remanent` in the same sense as a latch or magnetic core because charge tends to leak away with time. Dennard nevertheless argues that the charge remains usable for long enough relative to the read-write cycle that regeneration can consume only a fraction of the memory's operating time.

**Primary anchor:** U.S. Patent 3,387,286, printed pp. 1–2, especially the abstract and `Summary of the invention`; PDF pages 4/9 in the scanned file.

### H/P — In the 1T1C embodiment, reading creates a second restoration obligation

The patent's detailed description of the FIG. 1 array states that its one-transistor / one-capacitor storage is a **destructive memory**: reading discharges the capacitor, so information that must continue to exist has to be rewritten.

The same passage then separately states that capacitor charge storage is not permanent and therefore requires periodic regeneration. Suggested regeneration methods include dedicating recurring memory cycles to regeneration or sequentially reading and rewriting word positions.

This distinction matters. The patent itself gives us two different reasons to rewrite a logical value:

1. **access-triggered restore** — a read has destroyed the physical state;
2. **time-triggered regeneration** — leakage will eventually destroy the physical distinction even if no useful read occurs.

The required regeneration frequency depends substantially on capacitor size and leakage paths. Dennard also notes that leakage is temperature-sensitive.

**Primary anchor:** U.S. Patent 3,387,286, printed pp. 5–6, description of the FIG. 1 array and regeneration; PDF page 6/9 in the scanned file.

### H/P — Dynamic retention does not logically require destructive read

The same patent also discloses other cells in which charge is stored in the gate-to-substrate capacitance of a second field-effect transistor and readout can be nondestructive.

A useful commercial boundary appears in Intel's later 1103 documentation. Intel's 1975 data catalog describes the 1103 as a **1024 word by 1-bit dynamic memory**, says that stored information is **non-destructively read**, and nevertheless requires all 1024 bits to be refreshed every **two milliseconds**, accomplished in 32 read cycles.

Therefore:

> destructive read is one possible source of restoration work, but it is not what makes a memory `dynamic` in the relevant retention sense.

The deeper feature is that the information-bearing electrical state is not assumed to remain indefinitely without periodic system action.

The Computer History Museum's semiconductor-memory history identifies the Intel 1103 as using a three-transistor dynamic cell derived from work by Honeywell's William Regitz; it should therefore not be silently treated as an implementation of Dennard's one-transistor cell.

---

## Retained state

In the bounded one-transistor / one-capacitor case, a binary value is represented by the electrical condition of the storage node and capacitor:

```text
logical distinction
    -> charged / uncharged capacitor state
    -> storage-node voltage
```

The exact voltage is not the logical object of interest. The memory system needs the physical state to remain far enough from the decision boundary that sensing and restoration can recover the intended bit.

This is already a useful distinction between:

- **physical state** — an analog electrical quantity that drifts;
- **logical state** — the binary value the system repeatedly reconstructs from it.

---

## Physical substrate

The primary FIG. 1 embodiment uses:

- a field-effect transistor as the access device;
- a capacitor as the storage element;
- word and bit lines;
- word-line drivers;
- bit-line drivers and sense amplifiers.

The storage element is therefore small only because selection, sensing, rewriting, and scheduling are displaced into circuitry shared across many cells.

This is a recurring retention pattern:

> density at the retained-state site can increase by moving maintenance work into shared infrastructure.

---

## Retention mechanism

The capacitor does not retain information because it reaches a permanently stable state. It retains information because:

1. the access transistor is normally off and presents a high-impedance path;
2. leakage is slow relative to a memory cycle;
3. before leakage destroys the usable distinction, the system regenerates the information.

So the relevant persistence is neither the passive positional stability of the abacus nor the remanent stability of magnetic core.

It is better described as:

> **bounded physical survival + scheduled restoration.**

A DRAM cell can be left electrically undisturbed for a while, but not indefinitely.

---

## Addressing and access geometry

Dennard's patent describes an array selected through **word lines and bit lines**. A selected word line connects the cells of that word to bit lines and sense circuitry.

Compared with the mercury delay line, the key change is that the requested state does not have to circulate to a unique access point. Selection is spatial/electrical rather than primarily phase-of-circulation.

But random access does not abolish time. It creates a new temporal obligation underneath the stable address:

```text
logical address remains stable
while
stored charge decays
and
periodic regeneration revisits the array
```

The address looks timeless only because the maintenance schedule is hidden below it.

---

## Read semantics

### Dennard FIG. 1 1T1C embodiment

Readout discharges the storage capacitor and is explicitly described as destructive. If the logical state must persist, it must be written back.

### Boundary: dynamic but nondestructively read storage

Dennard's patent includes nondestructive-read alternatives, and Intel's 1103 data-sheet description likewise combines nondestructive reads with mandatory periodic refresh.

Therefore this case must not collapse:

```text
dynamic retention
```

into:

```text
destructive read
```

They are separable mechanisms.

---

## Write and erasure semantics

In the FIG. 1 embodiment, writing establishes a charged or uncharged condition on the capacitor through the selected transistor.

There is no separate archival concept of `delete`. A new write replaces the currently represented bit value. Loss can also occur unintentionally if the state decays below recoverability or restoration fails.

This is **state retention**, not history retention. The cell does not preserve previous values merely because a new value is written.

---

## Time

DRAM forces several timescales into one object:

### Read-write cycle

The useful computation/access timescale.

### Charge-retention interval

The interval over which leakage has not yet destroyed the recoverable distinction.

### Regeneration / refresh interval

The system-maintenance schedule chosen to revisit state before the retention interval is exceeded.

### Temperature-dependent leakage timescale

The patent explicitly connects leakage, and thus usable storage time, to junction temperature.

This makes DRAM a particularly clean example of a claim central to this repository:

> a logical state can appear continuously present even though its physical embodiment has a deadline.

---

## Maintenance and labor

At the cell level, the retained state seems minimal: one transistor and one capacitor in the key embodiment.

At system level, that simplicity requires surrounding work:

- selection;
- sensing;
- rewrite after destructive read where applicable;
- periodic regeneration / refresh scheduling;
- timing;
- temperature-aware design margins;
- power and control circuitry.

The historical move is therefore not simply from `complicated memory` to `simple memory`.

It is also a redistribution of complexity:

> **fewer devices per stored bit, more coordinated maintenance around the array.**

---

## Failure / forgetting modes

This case adds several distinct forms of technical forgetting:

- leakage until the charge difference is no longer recoverable;
- missed or late refresh;
- failed restore after destructive read;
- sense error followed by rewriting the wrong logical value;
- temperature increase shortening the safe retention interval;
- failure of shared refresh / sense / timing infrastructure affecting many cells.

These should not all be called merely `volatile memory loss`.

---

## Engineering reconstruction

### E — DRAM adds a deadline to quiescent retention

Magnetic core can retain a remanent state while idle without scheduled rewriting. Dennard's capacitor state cannot be treated that way: even an untouched bit has a finite maintenance deadline.

Thus **quiescent** does not mean **maintenance-free**.

### E — Refresh is temporal multiplexing of maintenance

Dennard's examples allocate recurring memory cycles to regeneration. In functional terms, array bandwidth is periodically borrowed from ordinary work so that the current state remains available for future work.

Persistence consumes time.

### E — The logical bit survives repeated analog replacement

After regeneration, the charge configuration is newly established. The system treats that restored physical state as the continuation of the same logical bit.

This strengthens a cross-case finding already exposed by delay-line regeneration and destructive-read core:

> logical identity does not require identity of one uninterrupted physical token.

---

## Philosophical / media-theoretical interpretation

### I — Persistence as scheduled return

The delay line retains by continuous recurrence; DRAM introduces a different temporal regime. The state can remain locally quiescent for an interval, but the system must **return to it before a deadline**.

This suggests a useful distinction for later comparison:

```text
continuous maintenance
    delay-line circulation

access-triggered maintenance
    classic destructive-read core

periodic deadline-driven maintenance
    DRAM refresh
```

These are engineering categories first. They should not yet be promoted into a universal philosophy of memory.

### I — Availability rests on invisible temporal discipline

To software, a memory location appears simply available at its address. Physically, the cell's state is decaying and must be restored on schedule.

The philosophical value of the case is therefore not that DRAM is a metaphor for human memory. It is that it demonstrates mechanically how **stable availability can be an effect produced by hidden temporal organization**.

That observation can later be tested against Ernst's operational / microtemporal account. It should not yet be equated with Stiegler's tertiary retention or Heidegger's `Bestand`.

---

## Functional analogy and limits

### A — Similarity to magnetic core

Both classic destructive-read core and the Dennard FIG. 1 cell may require rewrite after read.

But the mechanisms are different:

- core: remanent magnetic state can remain at rest; access may destroy it;
- capacitor cell: access may destroy it **and** time-dependent leakage creates a restoration obligation even without useful access.

### A — Similarity to delay line

Both can preserve a logical pattern through repeated recreation.

But:

- delay line requires continuous circulation as the retention mechanism;
- DRAM gives each cell an interval of local persistence before scheduled regeneration.

### Limit — not every DRAM read is destructive

The Intel 1103 boundary case and nondestructive embodiments in Dennard's own patent show that `dynamic` cannot be defined merely by destructive readout.

### Limit — not a complete modern DRAM account

Modern DRAM adds much richer sensing, row-buffer, refresh, error, packaging, power, and controller behavior. This case deliberately does not project later architecture backward into the 1967 patent.

---

## Cross-case result

Cases 00–03 now expose four distinct retention regimes:

```text
abacus
    retained position

mercury delay line
    continuous circulation / regeneration

magnetic core
    remanence at rest + access-triggered restore

Dennard 1T1C memory
    decaying state + periodic regeneration
    (+ destructive-read restore in the bounded embodiment)
```

The important new distinction is:

> **maintenance can be triggered by time even when no useful access occurs.**

This will matter later for Flash retention/read-disturb management, SSD background work, scrubbing, replica repair, lease renewal, and long-term archival migration — but those comparisons must be established case by case rather than assumed now.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Dennard filed the `Field-effect transistor memory` patent in 1967 and it issued in 1968 | H/P | exact patent metadata |
| One disclosed embodiment uses one FET and one capacitor | H/P | patent abstract + FIG. 1 description |
| Capacitor leakage requires periodic regeneration | H/P | patent abstract, summary, and detailed description |
| The FIG. 1 one-capacitor embodiment has destructive readout and requires rewrite if information is to remain | H/P | patent pp. 5–6 |
| Regeneration can be scheduled independently of ordinary accesses | H/P/E | patent's recurring-cycle and sequential regeneration examples |
| Intel 1103 documentation combines dynamic storage, nondestructive read, and a 2 ms refresh requirement | H/P | Intel 1975 Data Catalog, p. 2-7 |
| Dynamic retention is therefore not identical to destructive read | E | bounded inference from the patent + Intel commercial comparison |
| DRAM exposes periodic deadline-driven maintenance as distinct from continuous circulation and access-triggered restore | E/I | cross-case reconstruction |
| DRAM is identical to tertiary retention or `Bestand` | X | explicitly unsupported |

---

## Related repositories

### `tmzncty/computing-archaeology`

That repository currently identifies SRAM / DRAM / ROM / EEPROM / Flash / cache / ECC as a missing historical middle. A future full technical history of semiconductor memory should be developed there. This case should remain focused on the retention problem and link outward rather than pre-empting that work.

Current relevant memory track:

<https://github.com/tmzncty/computing-archaeology/tree/main/docs/memory>

### `tmzncty/problem-history`

Use its anti-anachronism rule here: `DRAM`, `refresh`, and `1T1C` are useful modern organizing terms, but the 1968 patent's own wording is `Field-effect transistor memory`, `regeneration`, `destructive memory`, and `retained in storage`.

---

## Sources

### Primary

1. Robert H. Dennard, **"Field-effect transistor memory,"** U.S. Patent 3,387,286, filed 14 July 1967, issued 4 June 1968. Google Patents transcription: <https://patents.google.com/patent/US3387286A/en>. Public-domain scan: <https://commons.wikimedia.org/wiki/File:MOS_DRAM_patent.pdf>.
   - printed pp. 1–2: abstract, prior art, and summary;
   - FIG. 1 / FIGS. 4A–4B: one-transistor / one-capacitor array and read-write timing;
   - printed pp. 5–6: destructive read, rewrite obligation, regeneration schemes, leakage and temperature dependence.
2. Intel Corporation, **1975 Intel Data Catalog**, `1103 — Fully Decoded Random Access 1024 Bit Dynamic Memory`, p. 2-7. Bitsavers scan: <https://www.bitsavers.org/components/intel/_dataBooks/1975_Intel_Data_Catalog.pdf>.
   - states dynamic operation;
   - nondestructive read;
   - refresh of all 1024 bits in 32 read cycles;
   - required refresh period of 2 ms for 0–70 °C ambient.

### Institutional secondary / artifact context

3. Computer History Museum, **"1970: Semiconductors Compete with Magnetic Cores,"** *The Storage Engine*: <https://www.computerhistory.org/storageengine/semiconductors-compete-with-magnetic-cores/>.
   - useful for placing Intel 1103's three-transistor dynamic cell in the early semiconductor-memory transition;
   - not used as the primary source for Dennard's 1T1C mechanism.
4. Computer History Museum, **Intel 1103 1024-bit (1K) DRAM** object record: <https://www.computerhistory.org/revolution/memory-storage/8/368/1017>.

## Source notes

The patent is the authoritative source for what Dennard disclosed and for the distinction between destructive read and periodic regeneration. The 1975 Intel catalog is later than the 1103's 1970 introduction, so it should be treated as primary manufacturer documentation of the product family rather than as evidence for the exact first-shipment specification. The 1103 comparison is intentionally used to bound the concept of dynamic retention, not to claim that the 1103 implements Dennard's exact one-transistor cell.