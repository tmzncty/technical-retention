# DRAM power-off remanence 1979–2008 grounding record

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
