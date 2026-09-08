from pathlib import Path

CASE_PATH = Path("cases/127-dram-power-off-remanence-gradual-decay.md")
EVIDENCE_PATH = Path("evidence/127-dram-1979-2008-remanence-grounding.md")
ROADMAP_PATH = Path("ROADMAP.md")
INDEX_PATH = Path("CASE_INDEX.md")

CASE_MARKER = "# DRAM Power-Off Remanence: Gradual Decay, Cooling, and Residual Recoverability"
EVIDENCE_MARKER = "# DRAM power-off remanence 1979–2008 grounding record"
FINDINGS_MARKER = "## Case 127 — DRAM power-off remanence findings"

CASE_TEXT = r'''# DRAM Power-Off Remanence: Gradual Decay, Cooling, and Residual Recoverability

## Scope

- **Object / system:** commodity SDRAM, DDR, and DDR2 modules characterized by Halderman et al. in 2008, with a 2005 reboot-survival observation and a cautiously bounded 1979 low-temperature prior-art floor.
- **Date range:** 1979–2008 for the evidence chain; the central experimentally grounded mechanism is the 2008 study.
- **Why this case matters for technical retention:** it tests what `volatile` means at the instant ordinary refresh and power support stop. The physical information-bearing state does not necessarily disappear at the same moment that the system ceases to guarantee ordinary DRAM service.

This is **not** a general history of cold-boot attacks, memory forensics, DRAM security, cryogenic electronics, or semiconductor remanence. Case 03 remains the canonical case for ordinary powered DRAM refresh. Case 127 is narrower:

> What survives after the maintenance regime that normally makes DRAM reliable has stopped, and how should residual physical recoverability be distinguished from ordinary volatile-memory service?

---

## Historical vocabulary and prior-art boundary

Halderman et al. use the terms **`memory remanence`**, **`decay`**, **`ground state`**, and **`refresh`**. Their paper explicitly says that the DRAM effect they study is caused by cell capacitance and is different from the longer-term semiconductor `burn-in` effects discussed by Peter Gutmann.

The word `remanence` therefore cannot be treated as one physical mechanism merely because several security papers use it.

The 2008 paper also blocks an origin myth. Its authors describe their work as the first comprehensive security study of the consequences, not the discovery of DRAM remanence itself. They cite earlier knowledge extending into the 1970s, including Link and May's 1979 paper reporting low-temperature behavior. The 1979 article has **not** been directly facsimile-inspected in this slice, so its one-week liquid-nitrogen result is retained only as a later scholarly report, not as a directly verified primary quotation.

---

## Historical record

### H/P — ordinary-temperature power-off decay is gradual, not instantaneous

J. Alex Halderman and colleagues published **“Lest We Remember: Cold Boot Attacks on Encryption Keys”** at the 17th USENIX Security Symposium in July 2008. Their experimental systems used SDRAM, DDR, and DDR2 modules from several manufacturers in machines dated 1999–2007.

For ordinary-temperature tests, the measured module temperatures ranged from **25.5 °C to 44.1 °C**. Across the tested machines, the fastest sample reached complete data loss in approximately **2.5 seconds**, while the slowest took an average of about **35 seconds**. The curves differed substantially by machine but shared a broad shape: slow initial decay, a faster middle interval, then slower final decay.

This establishes a bounded historical result:

> removing power from the tested DRAM systems ended guaranteed normal service before it necessarily ended all physically recoverable state.

It does **not** establish a universal seconds-long retention specification for every DRAM device, temperature, data pattern, generation, or platform.

Primary anchor: Halderman et al. 2008, §3.1, especially the discussion corresponding to lines 65–71 in the USENIX HTML edition.

### H/P — the ordinary refresh deadline is a reliability requirement, not a measured instant of physical oblivion

The same paper describes a DRAM cell as capacitor-based and explains that charge leaks toward a cell-dependent ground state. It also distinguishes the standard refresh interval from the instant at which a particular unrefreshed cell actually loses its contents: the refresh specification is chosen for extremely high reliability during ordinary operation, while missing one individual refresh deadline does not imply immediate destruction of that cell's information.

That distinction is central to this repository. A maintenance deadline answers:

```text
when must the system act to preserve the service guarantee?
```

It does not necessarily answer:

```text
at what exact instant does every physical trace become unrecoverable?
```

Primary anchor: Halderman et al. 2008, §3, especially the cell/refresh discussion immediately before §3.1.

### H/P — cooling changes the residual-retention window dramatically

Halderman et al. cooled four tested systems to approximately **−50 °C**, removed power, and maintained the lower temperature until power was restored. In their samples, a 60-second interruption still allowed at least **99.9% of bits** to be recovered correctly.

As an extreme experiment, they kept one removed module in liquid nitrogen for **60 minutes**. In a 1 MB test region they measured roughly **14,000 bit errors**, reported as **0.17% decay**.

The safe claim is empirical and bounded: lowering temperature greatly extended residual recoverability in the tested modules. The paper's suggestion that sufficient cooling may extend recoverability for much longer is an extrapolation and should not be silently promoted into a universal retention rating.

Primary anchor: Halderman et al. 2008, §3.2, Table 2 and the liquid-nitrogen experiment.

### H/P — decay is structured and can be predictable

The 2008 tests found highly nonuniform but often predictable decay patterns. Most cells tended toward a wiring-dependent **ground state**, and many cells switched after relatively repeatable no-power intervals. Figure 4 shows a test image that was still visually indistinguishable from the original after five seconds and then progressively degraded over longer power-off intervals.

This means that residual memory need not behave like a uniformly randomized buffer once refresh stops. In the bounded experiments, physical forgetting proceeded through structured cell-specific decay.

Primary anchor: Halderman et al. 2008, §3.3 and Figure 4.

### H/P — reboot and refresh resumption create a second transition

Halderman et al. separately document what happens when a platform starts again. BIOS/POST activity may overwrite some memory, and some ECC-capable systems may clear memory. On machines that do not wipe it first, once the memory controller resumes refreshing, the residual bit values that are then sensed and rewritten become stabilized enough for ordinary reads and imaging.

This is a crucial retention boundary:

> **refresh resumption arrests further decay of the surviving image; it does not prove that the image still equals the pre-power-loss state.**

Primary anchor: Halderman et al. 2008, §3.4 and §4, especially the discussion of BIOS overwriting and restart-time refresh.

### H/P — a 2005 reboot-survival observation predates the comprehensive 2008 study

Jim Chow, Ben Pfaff, Tal Garfinkel, and Mendel Rosenblum reported in USENIX Security 2005 that rebooting did not necessarily clear physical memory on their test machines. They found that soft reboot preserved most RAM, while hard reboot results varied; on an IBM ThinkPad T30, many test stamps remained after **30 seconds without power**.

Their paper's main subject is secure deallocation and software data lifetime, not a systematic characterization of powered-off DRAM decay. It should therefore be used as an earlier reboot-survival witness, not as a substitute for the 2008 physical-decay experiments.

Primary anchor: Chow et al. 2005, §3, `Effect of Rebooting`.

### H/S — the low-temperature phenomenon predates the security framing

Halderman et al. state that DRAM remanence and temperature dependence had been known since the 1970s and cite:

- W. Link and H. May, **“Eigenschaften von MOS-Ein-Transistorspeicherzellen bei tiefen Temperaturen,”** *Archiv für Elektronik und Übertragungstechnik* 33 (June 1979), 229–235.

The 2008 paper reports that a 1978 experiment associated with this source found no data loss for a week without refresh under liquid-nitrogen cooling. Because this slice did not inspect the 1979 article itself, that exact result remains **secondary-source prior-art evidence** here.

This is enough to block a claim that the physical low-temperature retention effect originated with the 2008 cold-boot security work, but not enough to settle detailed 1970s device behavior or priority.

---

## Retained state and substrate

The retained object is not `the RAM module` in the abstract. In the bounded physical mechanism, each logical bit depends on an analog electrical condition of a DRAM storage cell that remains sufficiently distinguishable for later sensing.

After ordinary power and refresh stop:

```text
pre-loss logical value
    -> residual cell charge / electrical state
    -> temperature- and cell-dependent leakage
    -> possibly still distinguishable value
    -> eventual ground-state decay
```

The logical state can therefore outlive the **guaranteed service regime** for a time without becoming nonvolatile in the ordinary engineering sense.

---

## Retention interval and failure boundary

Case 03 describes **bounded physical survival + scheduled restoration** during normal powered operation. Case 127 looks at what happens when scheduled restoration ceases.

The transition is not well described as one Boolean edge:

```text
powered + refreshed
    -> power/refresh removed
    -> residual recoverability window
    -> accumulating bit errors
    -> practical reconstruction may become harder or impossible
    -> eventual physical decay toward ground states
```

Different observers can cross different boundaries at different times:

- normal processor service may be gone immediately with platform power;
- many physical bit values may still survive;
- a degraded image may remain recoverable;
- exact byte-for-byte equality may already be lost;
- enough structured redundancy may still permit reconstruction of some higher-level objects.

The 2008 paper's cryptographic reconstruction work demonstrates the last point, but this case does not reproduce attack procedures. For this repository the methodological lesson is simply that **logical recoverability can persist through partial physical corruption when the retained object has reconstructible structure**.

---

## Read / write / erase semantics

### Read after restart

Once a suitable controller restarts refresh, surviving values can be read through ordinary memory accesses. The act of bringing the platform back into service may itself modify memory through BIOS/firmware activity before later software observes it.

### Ordinary overwrite

A write replaces the currently represented DRAM value. This is distinct from passive leakage.

### Explicit wiping

A BIOS memory clear or software zeroing operation actively replaces residual values. Such wiping is an erasure operation at the logical cell-value level; it should not be confused with merely waiting for unpowered decay.

### Power removal

Power removal is **not itself a deterministic erase command** in the bounded commodity DRAM evidence. It withdraws the infrastructure that guarantees refresh and service, after which the physical state decays on device- and temperature-dependent timescales.

---

## Maintenance and invisible work

DRAM's ordinary `volatile` behavior depends on infrastructure that is usually invisible to software:

- continuous electrical support for the memory subsystem;
- refresh scheduling;
- row selection and sense/restore cycles;
- timing margins chosen for reliable service.

Case 127 reveals that when this infrastructure stops, the underlying physical state does not necessarily disappear on the same clock edge. `Volatile` is therefore best treated here as an **operational contract and maintenance dependency**, not as a claim of instantaneous material annihilation.

That formulation is an engineering reconstruction. It is not a replacement for the historical vocabulary of the cited papers.

---

## Failure / forgetting modes

The case adds several failure distinctions:

- **maintenance withdrawal** — refresh and ordinary power support stop;
- **gradual leakage** — cell states move toward their ground states;
- **partial corruption** — some bits have decayed while others remain;
- **platform overwrite** — BIOS/POST or later software replaces residual state;
- **recovery freeze-in** — restarted refresh stabilizes whatever values survive at that moment;
- **logical reconstruction failure** — a higher-level object becomes unrecoverable before or after total physical decay depending on redundancy and error pattern.

These are not one generic event called `RAM cleared`.

---

## Engineering reconstruction

### E — volatility ≠ instantaneous erasure

The tested systems give a direct counterexample to the shortcut:

```text
power removed
    => every DRAM bit immediately becomes physically unrecoverable
```

The stronger defensible relation is:

```text
power/refresh removed
    => ordinary retention guarantee ends
    => residual state decays with time and environment
```

### E — refresh deadline ≠ physical decay timestamp

A refresh interval is chosen to make ordinary memory service highly reliable. It is not evidence that every cell crosses its sensing boundary at the same moment when that interval is exceeded.

### E — service availability ≠ residual recoverability

A powered-off computer cannot ordinarily service loads from its DRAM, yet a later process may still recover some of the physical state. Availability and residual recoverability are therefore distinct retention relations.

### E — surviving residual image ≠ exact historical image

Partial decay, BIOS overwrite, and restart-time activity can all change the recovered bytes. A surviving image is evidence of earlier state, but it need not be a perfect snapshot of the pre-loss memory contents.

### E — resumed refresh ≠ repair of the original state

When refresh resumes, it can stabilize the values then present. It does not infer which bits have already decayed and restore the pre-loss logical value unless some additional redundancy/reconstruction mechanism does that work.

### E — cooling extends a window; it does not change the service contract into nonvolatility

Cooling alters leakage rate and therefore residual-retention time in the tested devices. It does not turn commodity DRAM into a specified archival or power-independent memory regime.

---

## Functional analogies and limits

### A — Case 03 ordinary DRAM refresh

Case 03 asks how a decaying capacitor supports reliable powered service through scheduled restoration. Case 127 starts precisely when that maintenance loop stops.

The useful relation is:

```text
Case 03: deadline-driven preservation before loss
Case 127: residual decay after preservation work stops
```

This is one mechanism viewed on opposite sides of the maintenance boundary, not two unrelated definitions of DRAM.

### A — nonvolatile Flash / SSD

Flash and SSD cases retain state across power loss as part of their intended service contract, though controllers and mappings add their own recovery obligations. Case 127 instead concerns an **unmanaged residual window** after ordinary volatile-memory support has ended.

Therefore:

```text
DRAM remanence after power loss
    ≠
nonvolatile-media durability guarantee
```

### A — magnetic core

Magnetic core's remanent state is designed to persist at rest without periodic refresh in the bounded classic regime. DRAM residual charge can linger after power loss, but it is leaking toward a ground state. Both can be called `remanent` in loose English only at the cost of hiding the very different physical and operational contracts.

### Limit — not every platform preserves boot-time RAM

Halderman et al. explicitly observed BIOS overwrite and mandatory clearing on some systems. The remanence mechanism does not imply that every reboot exposes the same residual bytes through the same platform path.

### Limit — not a universal quantitative DRAM law

The measured modules span several commodity technologies and vendors, but the seconds/minutes figures are experiment-specific. Later DRAM generations, temperatures, packages, controllers, ECC initialization, and platform firmware can behave differently.

---

## Philosophical / media-theoretical interpretation

### I — operational categories need not coincide with instantaneous material boundaries

`Volatile memory` is indispensable engineering vocabulary, but this case shows why a media-theoretical reading should not convert it into a metaphysical claim that the trace vanishes at the exact moment power is removed.

The technical record instead exposes several times:

- service time;
- refresh-maintenance time;
- residual physical decay time;
- reconstruction time;
- deliberate wipe/overwrite time.

This plural-timescale result fits the repository's existing Ernst guardrail: operational analysis should identify **which operation and which timescale** are at issue rather than universalize one microtemporal boundary.

This does not make DRAM remanence identical to human memory, Stieglerian tertiary retention, or an archive.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Halderman et al. systematically measured ordinary-temperature DRAM decay in SDRAM/DDR/DDR2 test systems | H/P | strong primary peer-reviewed evidence |
| tested modules lost data gradually rather than at the instant power/refresh stopped | H/P | strong primary experimental evidence |
| normal-temperature complete-decay times varied roughly 2.5 s to 35 s across the bounded tested machines | H/P | exact §3.1 result; not universalized |
| cooling to about −50 °C greatly reduced errors after power removal in the tested modules | H/P | §3.2 + Table 2 |
| one liquid-nitrogen test measured 0.17% decay in 1 MB after 60 minutes | H/P | exact bounded experiment |
| decay often proceeded predictably toward cell-dependent ground states | H/P | §3.3 |
| BIOS/reboot activity can overwrite or clear residual memory before later software reads it | H/P | §3.4 |
| restart-time refresh stabilizes residual values but does not prove they equal the original pre-loss state | H/P + E | §4 plus bounded reconstruction |
| Chow et al. observed hard-reboot survival on at least one 2005 test machine | H/P | §3 `Effect of Rebooting` |
| low-temperature DRAM retention was known by 1979 | H/S | later peer-reviewed report; direct 1979 facsimile not inspected |
| Halderman 2008 invented DRAM remanence | X | explicitly rejected by authors' own prior-work section |
| cold-boot capacitance remanence is identical to Gutmann's semiconductor burn-in | X | explicitly rejected by Halderman et al. |
| commodity DRAM should be classified as nonvolatile storage | X | unsupported; residual remanence ≠ service contract |

---

## Related repositories

### `tmzncty/computing-archaeology`

A fresh repository search found no dedicated cold-boot / DRAM-remanence case to reuse. Broad DRAM device genealogy, low-temperature semiconductor engineering, platform boot-memory behavior, and security-attack history belong there if later developed. Case 127 retains only the retention-specific relation among maintenance withdrawal, residual charge, decay, temperature, reboot overwrite, and recoverability.

### `tmzncty/problem-history`

Use the anti-anachronism rule. `Volatile` is a useful technical classification, but the historical sources themselves must decide what was measured and claimed. The 2008 authors explicitly distinguish their capacitance-based phenomenon from earlier `burn-in`; a shared word such as `remanence` does not prove one mechanism or one historical problem.

---

## Sources

### Primary / contemporary

1. J. Alex Halderman, Seth D. Schoen, Nadia Heninger, William Clarkson, William Paul, Joseph A. Calandrino, Ariel J. Feldman, Jacob Appelbaum, and Edward W. Felten, **“Lest We Remember: Cold Boot Attacks on Encryption Keys,”** 17th USENIX Security Symposium, 30 July 2008, pp. 45–60. <https://www.usenix.org/legacy/event/sec08/tech/full_papers/halderman/halderman_html/>
   - §2: prior-work/origin boundary and distinction from `burn-in`;
   - §3: DRAM cell/refresh model;
   - §3.1: ordinary-temperature decay measurements;
   - §3.2: reduced-temperature and liquid-nitrogen experiments;
   - §3.3: ground-state/predictability observations;
   - §3.4 and §4: BIOS overwrite, restart-time refresh, and residual-memory imaging boundary.
2. Jim Chow, Ben Pfaff, Tal Garfinkel, and Mendel Rosenblum, **“Shredding Your Garbage: Reducing Data Lifetime Through Secure Deallocation,”** 14th USENIX Security Symposium, 2005, pp. 331–346. <https://www.usenix.org/legacy/event/sec05/tech/full_papers/chow/chow_html/>
   - §3 `Effect of Rebooting`: soft- versus hard-reboot observations, including an IBM ThinkPad T30 retaining many test stamps after 30 seconds without power.
3. Peter Gutmann, **“Data Remanence in Semiconductor Devices,”** 10th USENIX Security Symposium, 15 August 2001, pp. 39–54. <https://www.usenix.org/legacy/publications/library/proceedings/sec01/full_papers/gutmann/gutmann_html/index.html>
   - used only as terminology/prior-art context; Halderman et al. explicitly distinguish the 2008 capacitance effect from Gutmann-style `burn-in`.

### Earlier prior-art lead, not directly inspected here

4. W. Link and H. May, **“Eigenschaften von MOS-Ein-Transistorspeicherzellen bei tiefen Temperaturen,”** *Archiv für Elektronik und Übertragungstechnik* 33 (June 1979), 229–235.
   - bibliographic identity and the earlier low-temperature-retention result are taken from Halderman et al. 2008 §2/reference [29]; direct facsimile inspection remains open.
'''

EVIDENCE_TEXT = r'''# DRAM power-off remanence 1979–2008 grounding record

This evidence record grounds [`cases/127-dram-power-off-remanence-gradual-decay.md`](../cases/127-dram-power-off-remanence-gradual-decay.md).

**Canonical maturity status is tracked in [`CASE_INDEX.md`](../CASE_INDEX.md).** The record is deliberately bounded. It is not a cold-boot attack manual and does not replace the broad DRAM history that belongs in `tmzncty/computing-archaeology`.

## Grounding question

Case 03 establishes ordinary DRAM retention as bounded physical charge survival plus scheduled restoration. Case 127 asks a different failure-boundary question:

> When power and refresh stop, does the physical state disappear at the same instant as the ordinary service guarantee, or can a degraded but still recoverable residue persist?

Four claims need separate evidence:

1. power-off DRAM decay can be gradual at ordinary temperatures;
2. temperature materially changes the residual-retention window;
3. reboot/restart activity can preserve, overwrite, or stabilize different parts of the residual image;
4. the 2008 security study did not originate the underlying remanence phenomenon.

---

## Source A — Halderman et al., USENIX Security 2008: systematic commodity-DRAM remanence characterization

**Document:** J. Alex Halderman et al., “Lest We Remember: Cold Boot Attacks on Encryption Keys,” 17th USENIX Security Symposium, 30 July 2008, pp. 45–60.

**Primary access:** <https://www.usenix.org/legacy/event/sec08/tech/full_papers/halderman/halderman_html/>

**Evidence class:** `H/P` — peer-reviewed contemporary experimental paper.

### A1. Test population and scope

**Table 1 / introductory experiment description.**

The authors tested machines using SDRAM, DDR, and DDR2 modules from Infineon, Samsung, Micron, and Elpida, with system dates from 1999 through 2007. This is a heterogeneous commodity sample, not a universal DRAM specification.

### A2. Ordinary-temperature decay is gradual and device-dependent

**§3.1.**

Operating temperatures in the bounded tests ranged from 25.5 °C to 44.1 °C. The fastest machine reached complete data loss in roughly 2.5 seconds; the slowest averaged about 35 seconds. Curves differed in scale but showed slow initial decay, a faster middle interval, and slower final decay.

**Grounded boundary:** `power removed ≠ immediate physical erasure` for the tested systems. The numerical range must not be generalized to all DRAM.

### A3. Refresh interval is a service-reliability bound, not a physical oblivion timestamp

**§3, immediately before §3.1.**

The paper explains capacitor leakage toward a cell-dependent ground state and notes that the standard refresh interval is chosen to make ordinary operation highly reliable. Failure to refresh one cell within that interval does not imply that its contents are instantaneously destroyed.

**Grounded boundary:** `refresh deadline ≠ exact decay instant`.

### A4. Lower temperature extends residual recoverability

**§3.2 / Table 2.**

With modules cooled to approximately −50 °C before power removal, all tested samples retained at least 99.9% correct bits after 60 seconds without power. One additional experiment kept a removed module in liquid nitrogen for 60 minutes and measured about 14,000 errors in a 1 MB test region, reported as 0.17% decay.

**Grounded boundary:** temperature is a major parameter of residual-retention time. This does not establish an archival-storage guarantee.

### A5. Decay can be directional and predictable

**§3.3 / Figure 4.**

The paper reports highly nonuniform but commonly predictable decay. Cells tend toward wiring-dependent ground states, and many cells switch after repeatable no-power intervals. A loaded test image remained visually indistinguishable after five seconds in one example and then degraded progressively.

**Grounded boundary:** `unrefreshed decay ≠ uniform randomization`.

### A6. Boot-time overwrite and refresh resumption are separate transitions

**§3.4 and §4.**

The authors observed BIOS overwriting of some ranges and mandatory memory clearing on some ECC-capable systems. Where residual values survive boot, the restarted memory controller begins refreshing and rewriting them, halting further decay enough for ordinary readout.

**Engineering consequence:** resuming refresh stabilizes the residual state then present; it is not evidence that previously decayed bits have been restored to their historical values.

---

## Source B — Chow et al., USENIX Security 2005: earlier reboot-survival observation

**Document:** Jim Chow, Ben Pfaff, Tal Garfinkel, Mendel Rosenblum, “Shredding Your Garbage: Reducing Data Lifetime Through Secure Deallocation,” 14th USENIX Security Symposium, 2005, pp. 331–346.

**Primary access:** <https://www.usenix.org/legacy/event/sec05/tech/full_papers/chow/chow_html/>

**Evidence class:** `H/P` — peer-reviewed contemporary experimental paper.

### B1. Software data lifetime and physical reboot survival must be separated

The paper's central experiments show that logically dead data can remain in allocated/unused memory for days or weeks because software has not overwritten it. That is **not** a claim that one unpowered DRAM cell physically retains charge for weeks.

### B2. `Effect of Rebooting` supplies the relevant physical boundary

In §3 the authors report that soft reboot preserved most RAM on tested systems and that hard-reboot behavior varied. They specifically report an IBM ThinkPad T30 retaining many test stamps after 30 seconds without power.

This is the appropriate pre-2008 physical-remanence witness from the paper.

**Grounded boundary:** `logical non-overwrite lifetime ≠ power-off physical remanence lifetime`, even though both can expose old data.

---

## Source C — Gutmann, USENIX Security 2001: terminology and mechanism boundary

**Document:** Peter Gutmann, “Data Remanence in Semiconductor Devices,” 10th USENIX Security Symposium, 15 August 2001, pp. 39–54.

**Primary access:** <https://www.usenix.org/legacy/publications/library/proceedings/sec01/full_papers/gutmann/gutmann_html/index.html>

**Evidence class:** `H/P` for Gutmann's own semiconductor-remanence discussion; `H/P + X` for the boundary because Halderman et al. explicitly distinguish their phenomenon from it.

Gutmann discusses several semiconductor-remanence mechanisms, including longer-term physical changes associated with repeatedly storing a value. Halderman et al. 2008 §2 explicitly say that their modern-DRAM effect is different: it can occur even for momentarily stored data and follows from DRAM cell capacitance.

**Grounded boundary:** `same remanence vocabulary ≠ same physical mechanism`.

---

## Source D — Link & May 1979: earlier low-temperature prior-art floor via later scholarly report

**Bibliographic record:** W. Link and H. May, “Eigenschaften von MOS-Ein-Transistorspeicherzellen bei tiefen Temperaturen,” *Archiv für Elektronik und Übertragungstechnik* 33 (June 1979), 229–235.

**Current access status:** direct facsimile not inspected in this slice.

**Evidence class:** `H/S` here — Halderman et al. 2008 §2 and reference [29] identify the paper and report that a 1978 experiment showed no data loss for a week without refresh under liquid-nitrogen cooling.

This establishes a conservative **prior-art floor** for the phenomenon through a later peer-reviewed source. It does not authorize exact quotation, device-level detail, or invention priority from the 1979 paper until that primary text is directly inspected.

---

## Evidence ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| modern commodity DRAM can retain substantial state briefly after power/refresh stop | `H/P` | Halderman 2008 abstract + §3.1 | strong bounded experiment |
| ordinary-temperature decay was gradual in the tested systems | `H/P` | Halderman §3.1 | strong |
| 2.5 s to ~35 s complete-decay results are sample-specific, not a universal specification | `H/P + X` | Halderman §3.1 + Table 1 scope | strong boundary |
| standard refresh deadline is not identical to each cell's physical decay instant | `H/P + E` | Halderman §3 preface to experiments | strong bounded reconstruction |
| cooling substantially extends residual retention | `H/P` | Halderman §3.2 / Table 2 | strong |
| one 60-minute liquid-nitrogen experiment measured 0.17% decay in a 1 MB region | `H/P` | Halderman §3.2 | strong exact experiment |
| decay often tended toward predictable, cell-dependent ground states | `H/P` | Halderman §3.3 | strong |
| boot firmware can overwrite/clear residual state | `H/P` | Halderman §3.4 | strong |
| resumed controller refresh stabilizes surviving values | `H/P` | Halderman §4 | strong |
| resumed refresh restores the exact historical state | `X` | not supported; partial decay may already have occurred | explicitly rejected |
| Chow et al. observed hard-reboot state survival in 2005 | `H/P` | Chow §3 `Effect of Rebooting` | strong earlier witness |
| Chow's days/weeks software-data lifetime equals physical no-power DRAM retention | `X` | different mechanism/experiment | explicitly rejected |
| low-temperature DRAM remanence predates 2008 | `H/S` | Halderman §2 citing Link & May 1979 | strong prior-art boundary, primary inspection still open |
| Halderman 2008 discovered the physical phenomenon | `X` | authors explicitly cite earlier work | rejected |
| Gutmann-style burn-in and cold-boot capacitance remanence are identical | `X` | Halderman §2 explicitly distinguishes them | rejected |

---

## What this changes in the project

### 1. `Volatile` is not an erasure timestamp

The case adds a failure-state interval between supported service and complete physical decay. Ordinary volatility specifies dependence on power/maintenance for reliable operation; it does not prove instantaneous material disappearance at power removal.

### 2. A maintenance deadline and a forgetting boundary answer different questions

Case 03 grounds the need to refresh before a deadline. Case 127 shows why that deadline should not be reinterpreted as the exact moment after which every physical trace is gone.

### 3. Recovery can stabilize a degraded residue

Restarted refresh can freeze in surviving bit values while BIOS activity may independently overwrite others. Recovery therefore has both preservation and disturbance components.

### 4. Environmental state belongs in the retention relation

Temperature materially changes leakage and residual-retention time. The retained state's future availability is partly conditioned by an environmental variable even after active refresh has ceased.

---

## Historical cautions

### Do not make 2008 an invention date

Halderman et al. explicitly cite older knowledge and describe their novelty as a comprehensive security study and exploitation of the consequences.

### Do not convert the 1979 secondary report into direct inspection

The Link/May bibliographic record and low-temperature result are grounded here through Halderman et al. Direct quotation and device-detail claims require the original article.

### Do not turn residual remanence into a nonvolatile guarantee

A recoverable residue after power loss is not the same thing as a specified, maintenance-independent service contract.

### Do not conflate software lifetime with physical remanence

Chow et al.'s long-lived stamps under ordinary operation show allocator/non-overwrite lifetime. Only their reboot subsection supplies the physical power-cycle witness used here.

---

## Related-repository boundary

A fresh `tmzncty/computing-archaeology` search for `cold boot DRAM remanence` returned no dedicated case. If a full history of low-temperature DRAM physics, platform reboot behavior, memory-forensics techniques, or semiconductor-remanence terminology is later built there, Case 127 should cite that work rather than duplicate it.

The bounded contribution retained here is:

> **ordinary DRAM service can end before all physical state becomes unrecoverable; after maintenance withdrawal, residual charge decays on temperature- and cell-dependent timescales, and restart can either overwrite or stabilize portions of the surviving image.**

---

## Readiness assessment

Case 127 satisfies the repository's `grounded` criteria for this bounded question:

- peer-reviewed primary experiments;
- exact section/table anchors;
- mechanism-level charge/leakage/refresh account;
- a pre-2008 primary reboot-survival witness;
- a conservative 1979 prior-art floor without pretending direct facsimile inspection;
- explicit separation of historical record, engineering reconstruction, analogy, and interpretation;
- cross-case boundaries against ordinary refresh, nonvolatile media, and burn-in;
- related-repository duplication check.

Future work should be narrow: direct Link/May 1979 facsimile inspection, later DDR-generation replication, named-platform ECC/firmware behavior, or controlled fault experiments—not a generic cold-boot history.
'''

ROADMAP_PHASE2 = r'''- [x] DRAM power-off remanence / gradual-decay boundary — [`cases/127-dram-power-off-remanence-gradual-decay.md`](cases/127-dram-power-off-remanence-gradual-decay.md), grounded by [`evidence/127-dram-1979-2008-remanence-grounding.md`](evidence/127-dram-1979-2008-remanence-grounding.md): Halderman et al. 2008 systematically separate normal DRAM refresh-service deadlines from the later physical-decay window, measuring gradual ordinary-temperature loss across SDRAM/DDR/DDR2 samples, strong temperature dependence, structured ground-state decay, BIOS overwrite, and restart-time stabilization of residual values; Chow et al. 2005 supplies an earlier hard-reboot survival witness, while Link/May 1979 is retained only as a later-reported prior-art floor pending direct facsimile inspection. This closes the bounded `volatile service guarantee vs residual physical recoverability vs environmental decay vs restart stabilization` relation; later DDR generations, exact low-temperature genealogy, named-platform ECC/firmware behavior, direct 1979 inspection, fault injection, and security-attack history remain open.
'''

ROADMAP_DECAY = "- [ ] decay and leakage — **substantially advanced at the DRAM physical-state layer by grounded Cases 03 and 127**: Case 03 grounds leakage as the reason ordinary powered DRAM requires periodic restoration before a service deadline; Case 127 crosses the maintenance boundary and shows that after refresh/power withdrawal the tested SDRAM/DDR/DDR2 modules decayed gradually rather than instantaneously, with strong temperature dependence and structured cell-specific ground states. This grounds `refresh deadline ≠ physical decay timestamp`, `volatile service loss ≠ immediate physical erasure`, and `residual recoverability ≠ exact historical image`. Direct Link/May 1979 facsimile inspection, later DDR generations, Flash/EEPROM charge-loss regimes beyond already bounded cases, environmental acceleration across other media, and controlled fault injection remain open;"

ROADMAP_POWER = "- [ ] power loss — **substantially advanced at the DRAM physical-state, SSD-device, and access-authority layers by grounded Cases 127, 15, and 126**: Case 127 shows that removing power/refresh can end ordinary DRAM service before all physical bit state becomes unrecoverable, and that restart may overwrite or stabilize a degraded residue; Case 15 separates volatile staging, explicit flush, orderly shutdown, capacitor-backed unsafe-power-loss transfer, and a named Intel SSD 320 recovery defect/fix; Case 126 separately shows reservation/registration coordination state whose power-loss survival is controlled by namespace-specific `PTPL`. Together these ground `power loss ≠ one universal forgetting boundary`, `volatile service loss ≠ instantaneous physical erasure`, `documented protection architecture ≠ bug-free recovery`, and `payload durability ≠ access-authority durability`. Independent named-device post-fix SSD fault injection, later-DRAM platform validation, exact BAD_CTX internal cause, physical-cell loss across other media, controller families, and broader power-failure genealogies remain open;"

INDEX_ROW = "| [DRAM Power-Off Remanence: Gradual Decay, Cooling, and Residual Recoverability](cases/127-dram-power-off-remanence-gradual-decay.md) | **grounded** | residual capacitor state after power/refresh withdrawal + temperature-dependent gradual decay + structured ground-state convergence + boot-time overwrite or refresh stabilization | separate volatile service lifetime from physical residual recoverability; distinguish refresh deadline from decay timestamp, residual image from exact snapshot, and restart stabilization from restoration of the original state | [1979–2008 grounding record](evidence/127-dram-1979-2008-remanence-grounding.md); direct Link/May 1979 facsimile, later DDR generations, named-platform ECC/firmware behavior, fault injection, and broad cold-boot/security genealogy remain separate work |"

FINDINGS = r'''## Case 127 — DRAM power-off remanence findings

- **2207 — volatile-memory classification ≠ instantaneous physical erasure:** the 2008 commodity-DRAM experiments retain measurable state for seconds after power/refresh withdrawal, so `volatile` cannot be used as an exact material-erasure timestamp. (`H/P`, `E`)
- **2208 — refresh deadline ≠ physical decay timestamp:** the ordinary refresh interval is a high-reliability service bound; exceeding one refresh interval does not imply that every cell has already lost its information. (`H/P`, `E`)
- **2209 — power removal ≠ immediate absence of all retained state:** normal processor service can disappear while residual capacitor states remain physically distinguishable. (`H/P`, `E`)
- **2210 — service unavailability ≠ residual recoverability:** an unpowered DIMM is not serving ordinary loads, yet later restart/transfer can recover part of its prior state. (`H/P`, `E`)
- **2211 — surviving residual image ≠ exact historical snapshot:** cell decay, BIOS overwrite, initialization, and later writes can make a recovered image only a degraded witness of the pre-loss state. (`H/P`, `E`)
- **2212 — cooling-extended remanence ≠ nonvolatile service contract:** lower temperature lengthens the measured residual window without turning commodity DRAM into specified archival storage. (`H/P`, `E`, `X`)
- **2213 — refresh resumption ≠ restoration of the original state:** restarted refresh can stabilize values then present but does not by itself infer and repair bits that already decayed. (`H/P`, `E`)
- **2214 — BIOS/POST overwrite ≠ spontaneous cell decay:** platform startup can actively replace residual state, so post-reboot disappearance has both device-physics and firmware-action causes. (`H/P`, `E`)
- **2215 — DRAM decay ≠ uniform randomization:** the tested modules commonly decayed toward wiring-dependent ground states in repeatable, nonuniform patterns. (`H/P`)
- **2216 — predictable decay order ≠ indefinite stability:** repeatable cell-specific decay timing can aid reconstruction while the underlying state is still moving toward loss. (`H/P`, `E`)
- **2217 — Halderman 2008 comprehensive security study ≠ invention of DRAM remanence:** the paper explicitly cites earlier 1970s knowledge and pre-2008 reboot-survival observations. (`H/P`, `X`)
- **2218 — Link/May 1979 prior-art floor ≠ direct primary inspection:** the article and low-temperature result are grounded here through Halderman et al.'s peer-reviewed account; exact 1979 device details remain unclaimed until the original is inspected. (`H/S`, `X`)
- **2219 — Chow 2005 software data lifetime ≠ no-power DRAM retention lifetime:** days/weeks of logically dead bytes under ordinary operation arise from non-overwrite/allocator behavior; only the paper's reboot experiment is evidence for physical power-cycle remanence. (`H/P`, `E`, `X`)
- **2220 — shared `remanence` vocabulary ≠ one physical mechanism:** Halderman et al. explicitly separate capacitance-based cold-boot persistence from Gutmann-style longer-term semiconductor `burn-in`. (`H/P`, `X`)
- **2221 — Case 03 normal refresh ≠ Case 127 post-maintenance decay:** Case 03 grounds scheduled restoration required for reliable powered service; Case 127 begins after that maintenance loop stops and tracks residual physical recoverability. (`A`, `E`)
- **2222 — related-repository boundary:** a fresh `tmzncty/computing-archaeology` search found no dedicated cold-boot/DRAM-remanence case to reuse; broad low-temperature DRAM, platform reboot, and memory-forensics genealogy belongs there if developed, while Case 127 retains the bounded maintenance-withdrawal/decay/recovery relation. (`H/P` project-state record)
'''


def ensure_new_files():
    if CASE_PATH.exists() and CASE_MARKER not in CASE_PATH.read_text(encoding="utf-8"):
        raise RuntimeError("Case 127 path exists with unexpected content")
    if EVIDENCE_PATH.exists() and EVIDENCE_MARKER not in EVIDENCE_PATH.read_text(encoding="utf-8"):
        raise RuntimeError("Evidence 127 path exists with unexpected content")
    CASE_PATH.write_text(CASE_TEXT.rstrip() + "\n", encoding="utf-8")
    EVIDENCE_PATH.write_text(EVIDENCE_TEXT.rstrip() + "\n", encoding="utf-8")


def update_roadmap():
    text = ROADMAP_PATH.read_text(encoding="utf-8")
    if "cases/127-dram-power-off-remanence-gradual-decay.md" not in text:
        anchor = "## Phase 2 — Build missing technical bridges\n\n"
        if anchor not in text:
            raise RuntimeError("Phase 2 anchor missing")
        text = text.replace(anchor, anchor + ROADMAP_PHASE2 + "\n", 1)

    lines = text.splitlines()
    found_decay = False
    found_power = False
    for i, line in enumerate(lines):
        if line.startswith("- [ ] decay and leakage"):
            lines[i] = ROADMAP_DECAY
            found_decay = True
        elif line.startswith("- [ ] power loss"):
            lines[i] = ROADMAP_POWER
            found_power = True
    if not found_decay:
        raise RuntimeError("decay and leakage roadmap item missing")
    if not found_power:
        raise RuntimeError("power loss roadmap item missing")
    ROADMAP_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def update_index():
    text = INDEX_PATH.read_text(encoding="utf-8")
    if "cases/127-dram-power-off-remanence-gradual-decay.md" not in text:
        lines = text.splitlines()
        insert_at = None
        for i, line in enumerate(lines):
            if "cases/126-nvme11-reservation-ptpl-authority-retention.md" in line:
                insert_at = i + 1
                break
        if insert_at is None:
            raise RuntimeError("Case 126 index row anchor missing")
        lines.insert(insert_at, INDEX_ROW)
        text = "\n".join(lines).rstrip() + "\n"

    if FINDINGS_MARKER not in text:
        text = text.rstrip() + "\n\n" + FINDINGS.rstrip() + "\n"
    INDEX_PATH.write_text(text, encoding="utf-8")


def normalize():
    for path in (CASE_PATH, EVIDENCE_PATH, ROADMAP_PATH, INDEX_PATH):
        text = path.read_text(encoding="utf-8")
        clean = "\n".join(line.rstrip() for line in text.splitlines()).rstrip() + "\n"
        path.write_text(clean, encoding="utf-8")


ensure_new_files()
update_roadmap()
update_index()
normalize()
