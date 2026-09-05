# Evidence 97 — NAND Flash Read Disturb, 2002–2015

**Supports:** [`cases/97-nand-flash-read-disturb-access-conditioned-retention.md`](../cases/97-nand-flash-read-disturb-access-conditioned-retention.md)

**Status:** `grounded`

## Research question

What direct evidence supports the bounded claim that NAND reads can cumulatively disturb unread neighboring cell state, making reliable retention depend partly on access workload and mitigation rather than wall-clock age alone?

This record deliberately separates:

1. an early manufacturer-primary recognition of the mechanism;
2. an independent institutional qualification/test witness, including its negative result;
3. a later open experimental characterization;
4. project engineering reconstruction from historical terminology;
5. prior-art and invention-priority limits.

## A. Fujitsu manufacturer-primary witness — 2002 priority / 2003 publication

### Source

Fujitsu Limited, **“Read disturb alleviated flash memory,”** US20030137873A1 / US6707714B2.

- Priority: **2002-01-22**.
- U.S. filing: **2002-10-22**.
- U.S. application publication: **2003-07-24**.
- Original assignee: Fujitsu Ltd.

Source: <https://patents.google.com/patent/US20030137873A1/en>.

### Directly supported historical claims

The patent uses `read disturb` in the title and description and explicitly concerns NAND-type Flash.

Its background explains that NAND read applies a sufficiently high voltage to non-selected word lines so that non-selected cells conduct. It then describes a `light programming operation state` on those non-selected cells: floating-gate charge can increase, threshold voltage can rise, and an erased state can eventually be changed toward a programmed state.

The disclosed design varies the voltage applied to non-selected word lines according to write-frequency classes. The stated tradeoff is that reducing the non-selected-word-line voltage suppresses read disturb but too low a voltage can make over-programmed cells fail to conduct correctly during a read.

### Evidence strength

`H/P — strong for date, historical vocabulary, mechanism class, and the existence of an engineering tradeoff.`

### What it does not establish

- first discovery of read disturb;
- first NAND mitigation of any kind;
- universal voltage values or read-count limits;
- that the disclosed patent architecture maps directly to a later SSD controller;
- that read disturb affects every NAND generation identically.

The case therefore says **recognized/documented by this date**, not `invented here`.

---

## B. NASA/JPL institutional witness — March 2008

### Source

Douglas Sheldon and Michael Freie, **_Disturb Testing in Flash Memories_**, Jet Propulsion Laboratory, California Institute of Technology, JPL Publication 08-7, March 2008, NASA Electronic Parts and Packaging (NEPP) Program.

- NASA NTRS: <https://ntrs.nasa.gov/citations/20210001742>
- NASA NEPP PDF: <https://nepp.nasa.gov/files/13582/07-100%20Sheldon_JPL%20Distrub%20Testing%20in%20Flash%20Mem.pdf>

### B.1 Executive-summary boundary

The report says 2Gb NAND devices were tested for both program and read disturb. It defines disturb testing as asking whether programming or reading nearby cells changes the expected state of another Flash cell. It also states that manufacturers acknowledge disturb failures and provide guidance for handling them.

Crucially, the executive summary says:

> No specific disturb failures were noted on the testing done for this report.

The case retains this negative finding rather than converting the existence of the mechanism into a universal device-failure claim.

### B.2 Mechanism and mitigation boundary

In the `Disturb Errors` section, the report describes read disturb in terms of electron injection through tunnel oxide and notes that program/read operations can cause electrons to move to or from other cells within the block.

The same section gives a **rule of thumb** of no more than roughly one million READ cycles per block for SLC and 100,000 for MLC. If the application must exceed that guidance, it recommends moving the data to another block and erasing the original block; the erase restarts the block's read-disturb exposure cycle.

These counts are recorded as the report's 2008 guidance, not as a universal NAND law.

### B.3 Test protocol and negative result

The report's Program 8 performs, on a single page:

- 50k page reads;
- 100k page reads;
- 500k page reads;
- 1M page reads;

and then identifies any error locations.

The conclusions repeat that no program-disturb or read-disturb failures were detected in this experiment.

### Evidence strength

`H/S — strong institutional test/qualification witness; strong negative-result boundary; moderate for generic mechanism explanation because it summarizes device physics and manufacturer guidance rather than establishing invention priority.`

### Retention-specific use

The JPL report supplies three unusually useful relations:

1. high read activity can be treated as a storage-reliability stress even without new application payload;
2. migration + erase can be maintenance intended to renew reliability margin rather than change logical value;
3. a read-count threshold is device/regime-specific, because this particular test did not reproduce a failure even at the tested upper count.

---

## C. Cai et al. experimental witness — 2015

### Source

Yu Cai, Yixin Luo, Saugata Ghose, Erich F. Haratsch, Ken Mai, Onur Mutlu, **“Read Disturb Errors in MLC NAND Flash Memory: Characterization, Mitigation, and Recovery,”** SAFARI Technical Report No. 2015-007, Carnegie Mellon University / Seagate Technology, May 2015.

- Technical report PDF: <https://research.ece.cmu.edu/safari/tr/tr-2015-007.pdf>
- Conference version: IEEE/IFIP DSN 2015, DOI `10.1109/DSN.2015.49`.

### C.1 Direct experimental claim

The abstract states that reading one row can affect threshold voltages of **unread Flash cells in different rows of the same block**, potentially moving them into a different logical state. The experiments use commercial 2Y-nm (20–24 nm) MLC NAND chips.

The paper reports that read-disturb-induced threshold-voltage shift / raw-error behavior correlates with:

- number of reads to neighboring pages;
- program/erase-cycle wear;
- pass-through-voltage magnitude;
- retention age / available error margin.

The case does not generalize these measurements outside the tested MLC regime.

### C.2 Physical read-path mechanism

The paper explains that cells in one NAND bitline/string are connected in series. To read one selected cell, the other cells in the string must be switched on so that the selected value reaches the sense amplifier. This is accomplished using a pass-through voltage `Vpass` high enough to exceed stored cell threshold voltages.

The paper then states that applying `Vpass` to unread cells induces tunneling and can shift their threshold voltages upward. Section 2.2 describes the per-read effect as a small `weak programming` effect that accumulates over repeated reads.

This is the central mechanism anchor for:

> logical read target ≠ physical stress target.

### C.3 Read count is a workload variable, not a complete history requirement

The paper notes earlier mitigation work based on a cumulative per-block read counter followed by block rewrite when a threshold is exceeded. It also discusses page migration in a read-disturb-aware FTL.

The case therefore treats a read counter as a possible **summary of exposure**, not evidence that a controller must retain every individual read event.

### C.4 Vpass / ECC tradeoff

The experiments show that reducing `Vpass` decreases read-disturb threshold shift but can create ordinary read errors if non-selected cells no longer pass the selected signal reliably. The proposed `Vpass Tuning` mechanism uses unused ECC correction margin to tolerate some of those added read errors while reducing disturbance.

This directly blocks two shortcuts:

- `lower Vpass = free reliability improvement`;
- `ECC-correct output = physically unchanged NAND state`.

### C.5 Proposed maintenance metadata

The paper's implementation-cost section says the proposed per-block tuning scheme requires:

- one byte per block for an 8-bit tuned `Vpass` setting;
- one byte per block for the predicted worst-case page.

For its assumed 512GB / 65,536-block SSD configuration, that is 128KB total metadata.

This is an evaluated research design, not a commercial-controller artifact. It is used only as a bounded witness that **small retained control state can govern a much larger payload's future read safety**.

### C.6 Scope of quantitative results

The paper reports an average endurance improvement of 21% for `Vpass Tuning` over the workload traces and model used in its evaluation, and a 36% raw-bit-error-rate reduction for its Read Disturb Recovery technique.

The case does not convert these into generic NAND/SSD performance ratios.

### Evidence strength

`H/P/S — strong peer-reviewed/open technical characterization for the tested 2Y-nm MLC chips; strong mechanism evidence; proposed mitigation remains a research design rather than production-deployment evidence.`

---

## D. Cross-case boundaries

### D.1 Read disturb vs retention loss — Case 36

Case 36's Flash Correct-and-Refresh is driven by retention-error accumulation over age and ECC margin. Case 97's central trigger is read activity in a physical neighborhood.

`A/E`: both can culminate in ECC-qualified rewrite or relocation, but the physical trigger is different.

**retention loss ≠ read disturb**.

### D.2 Read disturb vs RowHammer — Case 53

`A`: both are access-induced neighboring-state disturbances. The comparison stops there.

- DRAM RowHammer: repeated row activation, DRAM charge/coupling/leakage regime.
- NAND read disturb: pass-through bias / weak programming / threshold-voltage shift in Flash strings.

No historical or technical lineage is inferred from the analogy.

### D.3 Read disturb vs mapped-Flash relocation — Case 04

Case 04 explains how logical identity can survive physical relocation and how mapping metadata chooses the current embodiment. Case 97 supplies one possible maintenance reason for relocation: renewing reliability margin after heavy read exposure.

This is functional composition, not evidence that the 1993 mapped-Flash case was already implementing the later read-disturb mitigation.

### D.4 Read disturb vs magnetic-core half-select — Case 70

`A`: in both cases the physically affected set is wider than the logical target set. The substrate physics, timescale, threshold behavior, and historical lineage are unrelated.

---

## E. Claims now safe to write

1. By a 2002-priority Fujitsu filing, `read disturb` was an explicit NAND engineering problem tied to read voltage applied to non-selected word lines.
2. NASA/JPL's 2008 report treated read disturb as a qualification/reliability concern, discussed migration+erase mitigation, and explicitly reported **no observed disturb failure** in its tested devices.
3. Cai et al. 2015 experimentally measured cumulative read-induced threshold-voltage shifts in unread cells of commercial 2Y-nm MLC NAND and tied susceptibility to read count, wear, voltage, and retention age.
4. A logically successful read can impose physical stress on state not named by the logical request.
5. Read-disturb mitigation can depend on bounded maintenance metadata and can exchange disturbance margin against ECC margin, write/erase endurance, or background bandwidth.
6. `NAND nonvolatile` does not imply `all reads are physically neutral` or `reliable retention is independent of workload`.

## F. Claims still unsafe

- `Fujitsu invented read disturb`;
- `2002 was the first observation of read disturb`;
- `all NAND fails after 100k or 1M reads`;
- `JPL observed a read-disturb failure in the 2008 devices`;
- `Cai et al. invented read-disturb mitigation`;
- `all commercial SSDs store exactly two bytes of read-disturb metadata per block`;
- `read disturb is RowHammer in Flash`;
- `ECC erases the underlying physical disturbance`;
- `migration after reads is free of wear`;
- `selected-page read is itself a destructive read in the magnetic-core sense`.

## G. Related-repository check

Before writing the case, `tmzncty/computing-archaeology` was searched for `NAND read disturb` and `Flash retention disturbance NAND`; no existing dedicated case was found. The broad NAND/Flash device and controller genealogy remains better suited to that repository.

`tmzncty/problem-history` remains the methodological guardrail: `access-conditioned retention` and `disturbance budget` are project engineering vocabulary, not claims about the exact concepts historical actors believed themselves to be formulating.

## Promotion judgment

`grounded`.

The central mechanism has:

- manufacturer-primary evidence from 2002/2003;
- independent NASA/JPL institutional/test evidence from 2008, including an explicit negative result;
- strong experimental scholarly evidence from 2015;
- bounded cross-case comparisons;
- explicit invention-priority and generalization limits.

No further source is required to use the case for cross-mechanism comparison. Future work should be a separate later-NAND / commercial-controller / 3D-NAND implementation case rather than silently widening this one.
