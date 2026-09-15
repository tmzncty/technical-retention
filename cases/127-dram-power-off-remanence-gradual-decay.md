# DRAM Power-Off Remanence: Gradual Decay, Cooling, and Residual Recoverability

## Scope

- **Object / system:** commodity SDRAM, DDR, and DDR2 modules characterized by Halderman et al. in 2008, with a 2005 reboot-survival observation and a cautiously bounded 1979 low-temperature prior-art floor.
- **Date range:** 1979–2008 for the central power-off evidence chain, with a bounded 1984–1991 cryogenic-operation deepening used to distinguish refresh suppression from power-off remanence.
- **Why this case matters for technical retention:** it tests what `volatile` means at the instant ordinary refresh and power support stop. The physical information-bearing state does not necessarily disappear at the same moment that the system ceases to guarantee ordinary DRAM service.

This is **not** a general history of cold-boot attacks, memory forensics, DRAM security, cryogenic electronics, or semiconductor remanence. Case 03 remains the canonical case for ordinary powered DRAM refresh. Case 127 is narrower:

> What survives after the maintenance regime that normally makes DRAM reliable has stopped, and how should residual physical recoverability be distinguished from ordinary volatile-memory service?

Cryogenic refresh-suppression boundary deepening: [`../evidence/127-1984-1991-cryogenic-dram-refresh-suppression-boundary-deepening.md`](../evidence/127-1984-1991-cryogenic-dram-refresh-suppression-boundary-deepening.md).

---

## Historical vocabulary and prior-art boundary

Halderman et al. use the terms **`memory remanence`**, **`decay`**, **`ground state`**, and **`refresh`**. Their paper explicitly says that the DRAM effect they study is caused by cell capacitance and is different from the longer-term semiconductor `burn-in` effects discussed by Peter Gutmann.

The word `remanence` therefore cannot be treated as one physical mechanism merely because several security papers use it.

The 2008 paper also blocks an origin myth. Its authors describe their work as the first comprehensive security study of the consequences, not the discovery of DRAM remanence itself. They cite earlier knowledge extending into the 1970s, including Link and May's 1979 paper reporting low-temperature behavior. The 1979 article has **not** been directly facsimile-inspected in this slice, so its one-week liquid-nitrogen result is retained only as a later scholarly report, not as a directly verified primary quotation.

The new 1984–1991 deepening does not erase that source debt. It instead supplies independent period-adjacent evidence that low-temperature MOS/DRAM charge retention was an established engineering topic: a Hitachi patent with 1984 priority explicitly cites Link/May and describes a low-temperature RAM embodiment in which special refresh becomes unnecessary, while IBM's 1989 and 1991 cryogenic-DRAM records report greatly increased cell-retention intervals. Those are **powered cryogenic operating regimes**, not evidence that power-off remanence and refresh-free operation are the same thing.

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

### H/P — 1984–1991 cryogenic-operation evidence separates refresh suppression from power-off remanence

The dedicated deepening adds three independent engineering witnesses without pretending they are cold-boot experiments.

Hitachi's U.S. Patent 4,710,648, from a family with **9 May 1984** priority and issued **1 December 1987**, describes MOS operation below about 200 K as strongly reducing junction leakage. Its one-bit RAM embodiment states that at sufficiently low temperature the charge-storage interval becomes long enough that a special refresh operation is unnecessary. The patent background explicitly cites Link/May 1979 as earlier low-temperature MOS-memory literature.

IBM's 1989 `Experimental low temperature DRAM` publication record reports greatly enhanced retention in a functioning 512-Kbit cryogenic CMOS DRAM. IBM's 1991 `A 4-Mb Low-Temperature DRAM` record reports an LT-optimized trench-capacitor DRAM whose cell retention time exceeded **eight hours at 85 K**.

These records establish a different support relation from cold boot:

```text
cryogenic powered operation
    + greatly reduced leakage
    -> refresh can become extremely infrequent or unnecessary

power-off cold-boot regime
    + refresh absent
    + ordinary service support withdrawn
    -> residual state decays and may remain temporarily recoverable
```

Therefore:

> **refresh absent != power absent**

and:

> **refresh-free under one cryogenic operating condition != nonvolatile-storage contract**.

The direct Link/May 1979 facsimile remains open; this deepening narrows the historical gap rather than falsely closing it.

Detailed ledger: [`../evidence/127-1984-1991-cryogenic-dram-refresh-suppression-boundary-deepening.md`](../evidence/127-1984-1991-cryogenic-dram-refresh-suppression-boundary-deepening.md).

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

The cryogenic-operation deepening adds another boundary: maintenance cadence can change because the **loss rate** changes. Deliberate cooling can reduce leakage enough that explicit refresh becomes extremely infrequent or unnecessary in a bounded powered regime. Cooling is not a refresh command, and a powered cryogenic memory is not the same system state as an unpowered module retaining residual charge.

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

The cryogenic-operation records make the same point from the opposite side of the support boundary: a colder device can need far less temporal refresh work while it remains powered. Thus `retention obligation`, `physical loss rate`, and `maintenance cadence` must remain separate. A thermal-support regime can reduce temporal maintenance without becoming the same mechanism as refresh.
---

## Functional analogies and limits

### A — Case 03 ordinary DRAM refresh

Case 03 asks how a decaying capacitor supports reliable powered service through scheduled restoration. Case 127 starts precisely when that maintenance loop stops.

The useful relation is:

```text
Case 03: deadline-driven preservation before loss
Case 127: residual decay after preservation work stops
```

The cryogenic deepening adds a third bounded state: an intentionally colder **powered** DRAM can move the maintenance deadline far outward because leakage has changed. That is still not the same thing as power-off residual survival.

This is one mechanism family viewed under different support conditions, not unrelated definitions of DRAM.

### A — nonvolatile Flash / SSD

Flash and SSD cases retain state across power loss as part of their intended service contract, though controllers and mappings add their own recovery obligations. Case 127 instead concerns an **unmanaged residual window** after ordinary volatile-memory support has ended.

Therefore:

```text
DRAM remanence after power loss
    ≠
nonvolatile-media durability guarantee
```

Likewise, a refresh-free cryogenic operating point does not by itself turn DRAM into a nonvolatile medium.

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

The cryogenic-operation boundary adds another conditionality: the refresh-maintenance clock itself changes when the operating environment changes. That strengthens the repository's rule that a retention interval must be tied to its support conditions rather than treated as a property detached from temperature, voltage, device, and operating regime.

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
| low-temperature DRAM retention was known by 1979 | H/S | later peer-reviewed report plus independent period patent citation; direct 1979 facsimile still not inspected |
| Hitachi disclosed a sub-200 K RAM embodiment in which special refresh could become unnecessary | H/P | primary patent design disclosure; not shipped-product proof |
| IBM's 1991 LT-optimized DRAM record reports cell retention exceeding 8 h at 85 K | H/P | first-party institutional record of peer-reviewed paper; not interpreted as power-off shelf retention |
| refresh absent necessarily means power absent | X | rejected by cryogenic powered-operation evidence |
| refresh-free under one cryogenic condition makes DRAM nonvolatile storage | X | unsupported category collapse |
| Halderman 2008 invented DRAM remanence | X | explicitly rejected by authors' own prior-work section |
| cold-boot capacitance remanence is identical to Gutmann's semiconductor burn-in | X | explicitly rejected by Halderman et al. |
| commodity DRAM should be classified as nonvolatile storage | X | unsupported; residual remanence ≠ service contract |

---

## Related repositories

### `tmzncty/computing-archaeology`

A fresh repository search found no dedicated cold-boot / DRAM-remanence or cryogenic-DRAM case to reuse. Broad DRAM device genealogy, low-temperature semiconductor engineering, the Link/May 1979 facsimile reconstruction, IBM's low-temperature VLSI program, platform boot-memory behavior, and security-attack history belong there if later developed. Case 127 retains only the retention-specific relation among maintenance withdrawal, residual charge, decay, temperature, reboot overwrite, recoverability, and refresh suppression under changed operating conditions.

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
4. Hitachi, Ltd., **U.S. Patent 4,710,648, “Semiconductor including signal processor and transient detector for low temperature operation.”** Priority family 9 May 1984; U.S. issue 1 December 1987. <https://patents.justia.com/patent/4710648>.
   - used for the period industrial disclosure that low-temperature MOS leakage can become small enough for a RAM embodiment to dispense with special refresh, and for its explicit citation of Link/May 1979.
5. W. H. Henkels et al., **“Experimental low temperature DRAM,”** Symposium on VLSI Circuits 1989. IBM Research record: <https://research.ibm.com/publications/experimental-low-temperature-dram>. DOI `10.1109/VLSIC.1989.1037471`.
6. W. H. Henkels et al., **“A 4-Mb Low-Temperature DRAM,”** *IEEE Journal of Solid-State Circuits* 26(11), 1991, 1519–1529. IBM Research record: <https://research.ibm.com/publications/a-4-mb-low-temperature-dram>. DOI `10.1109/4.98967`.

### Earlier prior-art lead, not directly inspected here

7. W. Link and H. May, **“Eigenschaften von MOS-Ein-Transistorspeicherzellen bei tiefen Temperaturen,”** *Archiv für Elektronik und Übertragungstechnik* 33 (June 1979), 229–235.
   - bibliographic identity and the earlier low-temperature-retention result are taken from Halderman et al. 2008 §2/reference [29], with independent period citation in the Hitachi patent; direct facsimile inspection remains open.
8. P. Wyns and R. L. Anderson, **“Low-Temperature Operation of Silicon Dynamic Random-Access Memories,”** *IEEE Transactions on Electron Devices* 36(8), 1989, 1423–1428, DOI `10.1109/16.30954`.
   - used only at abstract/index strength in the deepening; direct facsimile inspection remains open for exact quantitative conditions.
