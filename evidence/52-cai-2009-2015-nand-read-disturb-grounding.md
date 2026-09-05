# Case 52 Grounding Record — NAND Read Disturb, 2002–2015

## Purpose

This record grounds [`../cases/52-nand-flash-read-disturb-access-induced-decay.md`](../cases/52-nand-flash-read-disturb-access-induced-decay.md).

The bounded question is:

> Can an ordinary NAND read leave the requested value recoverable now while cumulatively degrading other retained cells in the same physical block, and what evidence existed from 2002 through 2015 for mechanism recognition, qualification, controller mitigation, and recovery?

The answer is **yes for the bounded source set**, with an important evidence split:

- the **read-disturb phenomenon and earlier read-count/migration management** are historical/primary prior art before 2015;
- the **2015 commercial-chip measurements** directly characterize the physical/error behavior of 2Y-nm MLC NAND;
- **Vpass Tuning** and **Read Disturb Recovery (RDR)** are proposed/evaluated techniques in that paper, not demonstrated deployment in a named shipped SSD controller.

## Consolidation note

The grounding-record filename is retained for stable links, but the evidence window is now **2002–2015**. The former Case 97 duplicated Case 52's central mechanism. Its unique evidence has been absorbed here: Fujitsu's 2002-priority manufacturer filing and NASA/JPL's 2008 qualification/test report, including the explicit no-disturb-failure result. Git history retains the former files for provenance. Case 67 remains a separate later 3-D NAND controller-policy case.

## Evidence classes

| Source | Date / object | Evidence role | What it can establish | What it cannot establish |
| --- | --- | --- | --- | --- |
| Fujitsu, US20030137873A1 / US6707714B2 | priority 2002-01-22; publication 2003-07-24 | manufacturer primary patent | early explicit NAND `read disturb` vocabulary; non-selected-word-line read voltage; light-programming / threshold-shift mechanism; voltage tradeoff | first discovery/invention priority; universal later-controller implementation |
| Sheldon & Freie, NASA/JPL Publication 08-7 | March 2008 | institutional qualification/test report | disturb as a reliability concern; migration+erase guidance; 50k/100k/500k/1M read protocol; explicit no-disturb-failure result | universal read-count threshold; evidence that the tested devices failed from read disturb |
| Frost et al., US7818525B1 | priority 2009-08-12; publication 2010-10-19 | manufacturer/controller primary patent | period `Read Disturb` vocabulary; elevated unread-cell gate stress; repeated weak programming; ECC; per-block read counting; threshold-triggered relocation and mapping update | universal implementation across NAND products; exact invention priority for read disturb itself |
| Ha, Jeong, Kim, APSys | 2013 | peer-reviewed scholarly prior art | read-disturb management as an existing high-density NAND/FTL problem; neighboring-page reads; proactive relocation/load balancing | direct characterization of the same 2Y-nm chips used in 2015; commercial deployment |
| Cai et al., DSN | June 2015 conference; pp. 438–449 | peer-reviewed primary experimental paper | commercial 2Y-nm MLC characterization; Vpass/read-count/P-E-wear relations; proposed Vpass Tuning and RDR; experimental RDR behavior | named-product controller deployment; universal thresholds for later 3D NAND |
| CMU/Intel Science & Technology Center abstract page | 2015 | institutional bibliographic/abstract record | author/title/event confirmation and bounded summary of the paper | substitute for figure- or section-level evidence where the paper itself is available |

## Earlier manufacturer-primary evidence — Fujitsu 2002/2003

Fujitsu Limited, **“Read disturb alleviated flash memory,”** US20030137873A1 / US6707714B2:

- priority: 22 January 2002;
- U.S. filing: 22 October 2002;
- U.S. application publication: 24 July 2003;
- original assignee: Fujitsu Ltd.

Source: <https://patents.google.com/patent/US20030137873A1/en>.

The patent directly supports the date and historical vocabulary, NAND non-selected-word-line read-voltage stress, a light-programming / threshold-rise mechanism, and a disturb-versus-read-margin voltage tradeoff. It does **not** establish first discovery or universal later-controller implementation.

## Independent institutional qualification evidence — NASA/JPL 2008

Douglas Sheldon and Michael Freie, **_Disturb Testing in Flash Memories_**, JPL Publication 08-7, March 2008, NASA Electronic Parts and Packaging (NEPP) Program.

Source: <https://nepp.nasa.gov/files/13582/07-100%20Sheldon_JPL%20Distrub%20Testing%20in%20Flash%20Mem.pdf>.

The executive summary defines disturb testing around nearby programming/reading changing an expected state, states that manufacturers acknowledged disturb failures, and says no specific disturb failures were noted in the report's testing. The report gives contemporary SLC/MLC read-count guidance plus migration+erase mitigation; Program 8 performs 50k, 100k, 500k, and 1M page reads on one page; the conclusions report no program-disturb or read-disturb failures in the tested devices.

Evidence strength: **H/S — strong institutional qualification/test witness and especially strong as a negative-result boundary.** The numerical guidance is retained as 2008 guidance, not a universal NAND law.

> **recognized failure mechanism + conservative guidance ≠ a fixed failure threshold reproduced by every tested device**.

## Primary paper inspected

Yu Cai, Yixin Luo, Saugata Ghose, Erich F. Haratsch, Ken Mai, Onur Mutlu, **“Read Disturb Errors in MLC NAND Flash Memory: Characterization, Mitigation, and Recovery,”** *45th Annual IEEE/IFIP International Conference on Dependable Systems and Networks (DSN)*, 2015, pp. 438–449, DOI `10.1109/DSN.2015.49`.

Author/institution-hosted PDF:
<https://istc-cc.cmu.edu/publications/papers/2015/flash-read-disturb-errors_dsn15.pdf>

Institutional abstract:
<https://istc-cc.cmu.edu/publications/papers/2015/flash-read-disturb-errors_dsn15_abs.shtml>

### Directly inspected anchors

#### Introduction / mechanism, printed p. 438 / PDF p. 1

The paper distinguishes read-disturb noise from P/E cycling, cell-to-cell program interference, and retention noise. Its circuit explanation states that:

- data is represented through cell threshold voltage;
- reading one cell in a NAND string requires unselected cells to be held on with a pass-through voltage;
- the pass-through voltage is above stored threshold voltages so unselected transistors conduct;
- those unread cells can experience tunneling and upward threshold-voltage shifts;
- repeated neighboring-page reads can eventually move an unread cell across a logical-state boundary.

This directly grounds the key historical/technical relation:

> **a successful selected-page read can impose cumulative material stress on unread neighboring cells**.

It does not by itself prove every physical cell changes after every single read; the paper's mechanism and measurements are cumulative/probabilistic.

#### Circuit-level read disturb / related work, printed p. 440 / PDF p. 3

Section 2.3 describes Fowler–Nordheim tunneling under pass-through voltage. It explicitly contrasts a single read-disturb event with programming: the read-disturb tunneling current is much smaller, so one event shifts threshold voltage more slowly, but repeated reads to the block accumulate.

The same section states that one read can disturb other pages in the same block.

Section 2.4 records earlier mitigation proposals:

- caching recently read data to avoid physical reads;
- maintaining cumulative per-block read counters and rewriting a block at a threshold;
- a Read Disturb-Aware FTL moving high-read pages;
- then-planned YAFFS mechanisms using fixed read-count rewrite or periodic check reads.

This is why the repository does not attribute generic read-count-triggered refresh/migration to the 2015 paper.

#### Commercial-chip characterization / read count and wear, printed pp. 441–442 / PDF pp. 4–5

The authors use commercially available 2Y-nm MLC NAND chips and an FPGA-based test platform.

For the tested devices, the paper reports:

- threshold-voltage shift magnitude grows with accumulated read-disturb operations;
- lower-threshold-voltage states are more susceptible;
- RBER rises roughly linearly with read-disturb count for a fixed P/E-wear level;
- the effect of read disturb becomes stronger as P/E cycles accumulate.

These are **bounded empirical properties of the tested technology**, not constants to project onto every later NAND generation.

The paper separately notes that Flash correct-and-refresh can periodically relocate block contents and reset accumulated effects from retention loss and read disturb, but such refresh adds erase/program wear. This supports the comparison to Case 36 while preserving the distinct triggers/error sources.

#### Vpass tradeoff and ECC margin, Sections 3.4–4

The authors find that reducing pass-through voltage decreases read-disturb impact, but an excessively low value can make unread cells fail to pass the selected value and therefore create additional read errors.

Their proposed **Vpass Tuning** chooses a lower per-block `Vpass` while preserving correctness within ECC margin. The paper evaluates the proposal with empirical error characterization and real workload traces and reports an average modeled endurance improvement of 21% across the examined traces.

Evidence boundary:

> **evaluation of a proposed tuning policy ≠ measured field deployment in a named SSD**.

The conclusion explicitly expresses hope that NAND manufacturers will expose pass-through-voltage controls to future controller designers, reinforcing that this paper should not be cited as proof that the proposed control was already a standard shipped interface.

#### RDR, Section 5 / printed pp. 447–449 / PDF pp. 10–12

The proposed **Read Disturb Recovery (RDR)** starts from an ECC-uncorrectable page. Its mechanism:

1. preserves readable valid data from the block;
2. scans threshold voltages of the failed page;
3. intentionally induces additional read disturbs by repeatedly reading another page in the same block;
4. scans threshold voltages again;
5. uses the magnitude of threshold-voltage change to classify susceptible cells as relatively disturb-prone or disturb-resistant;
6. probabilistically predicts likely earlier cell states and then retries ECC.

This directly grounds a counterintuitive relation:

> **additional controlled disturbance can be used as diagnostic evidence for logical recovery**.

The mechanism does not physically restore the old threshold distribution. It infers likely prior logical state from how cells respond to further disturbance.

The paper reports experimental RBER reduction reaching 36% at one million read-disturb operations for its evaluated 8,000-P/E-cycle block. That number is retained only as an experiment-specific result.

## Earlier primary prior art inspected

### US7818525B1 — `Efficient reduction of read disturb errors in NAND FLASH memory`

Inventors: Holloway H. Frost, Charles J. Camp, Timothy J. Fisher, James A. Fuxa, Lance W. Shelton.

- priority: 12 August 2009;
- filing: 24 September 2009;
- publication/grant: 19 October 2010;
- original assignee: Texas Memory Systems, Inc.

Source:
<https://patents.google.com/patent/US7818525B1/en>

Directly inspected portions establish:

- `Read Disturb` as explicit vocabulary;
- elevated gate voltage on unread cells during a NAND read;
- repeated stress allowing charge accumulation/weak programming in cells not selected for the read;
- ECC as a mitigation layer;
- an already-known approach using a block read count followed by data movement/erase at a threshold;
- the patent's own more incremental scheme: after a block read-count threshold, move subsequently requested pages to a different block, optionally ECC-check them, mark the old page dirty, and update logical-to-physical translation.

This is strong prior-art evidence against any statement that read-count maintenance or relocation begins with Cai et al. 2015.

It is **not** used to establish first invention of read disturb. The patent itself describes the condition and conventional mitigation as recognized/used, so a broader priority claim would require earlier device manuals/patents and is unnecessary for this case.

## 2013 scholarly prior-art check

Keonsoo Ha, Jaeyong Jeong, Jihong Kim, **“A read-disturb management technique for high-density NAND flash memory,”** *4th Asia-Pacific Workshop on Systems (APSys 2013)*, Article 13, DOI `10.1145/2500727.2500743`.

Seoul National University publication record:
<https://snu.elsevierpure.com/en/publications/a-read-disturb-management-technique-for-high-density-nand-flash-m/>

The institutional record preserves the peer-reviewed paper's abstract. It states that many reads to neighboring pages in the same block can produce read-disturb errors and proposes changing data-block locations to spread highly skewed reads, reducing migration time relative to an existing FTL approach.

Use here: **chronology and prior-art boundary only**. The 2015 DSN paper remains the source for the detailed 2Y-nm device characterization and RDR mechanism.

## Cross-case distinctions supported

### Versus Case 02 — magnetic core destructive read

Supported functional analogy:

> access itself can create a retention obligation.

Required stop condition:

- classic core destructive read changes the selected magnetic element during sensing and requires restore;
- NAND read disturb primarily exposes unselected cells to cumulative pass-through stress while the selected read can succeed;
- core restore is immediate/constitutive in the bounded scheme;
- NAND mitigation may depend on cumulative read count, ECC margin, voltage policy, or later relocation/recovery.

Therefore `NAND read disturb = destructive read` is rejected as a historical or physical equation.

### Versus Case 36 — Flash Correct-and-Refresh

Case 36 centers **retention-age/wear-driven raw error accumulation** and proactive renewal before ECC margin expires.

Case 52 adds **access-count-driven disturbance**. The 2015 paper itself treats retention error and read disturb as separate error classes even though block rewriting can reset accumulated effects from both.

Therefore:

> **maintenance outcome similarity ≠ failure-trigger identity**.

### Versus Case 04 — mapped Flash

Read-disturb management can relocate a current page/block and update logical-to-physical mapping. Case 04 already grounds logical identity across physical relocation; Case 52 supplies a distinct reason for making that relocation: cumulative read stress rather than ordinary erase/rewrite/reclamation alone.

## Evidence limits / rejected upgrades

Do **not** upgrade this record into any of the following:

- `all NAND reads destructively alter their requested data`;
- `read disturb and retention loss are one phenomenon`;
- `20,000`, `100,000`, or `1,000,000` reads is a universal NAND threshold;
- `Vpass Tuning` was deployed in a named commercial SSD by 2015;
- `RDR` was a production recovery feature;
- `RDR` restores original physical threshold voltages;
- Cai et al. invented read disturb or generic read-count relocation;
- a broader 3D-NAND read-reclaim history is completed by this case.

## Related-repository check

A current repository search for `read disturb NAND flash` in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) returned no dedicated case. There is therefore no existing technical-history slice to copy. If a broader NAND scaling/controller-history account is later built there, this case should link to it and retain only the access-versus-retention comparison here.

## Grounding decision

**`grounded`** is justified because the bounded central claims no longer depend on a single evidence type:

- the 2002-priority Fujitsu filing directly establishes earlier manufacturer-primary NAND `read disturb` vocabulary, mechanism class, and a read-voltage tradeoff without proving invention priority;
- the 2008 NASA/JPL qualification report independently establishes contemporary reliability guidance while its explicit no-disturb-failure result blocks universal read-count thresholds;
- the 2009-priority controller patent directly establishes pre-2015 terminology and read-count/migration prior art;
- the 2013 peer-reviewed record independently establishes read-disturb management as an existing FTL/reliability problem;
- the 2015 peer-reviewed paper directly measures commercial 2Y-nm MLC chips and exposes the physical/error relations used in the case;
- proposal/evaluation claims remain explicitly separated from commercial deployment.

This status does not close modern read-disturb history, 3D-NAND behavior, or named-controller implementation/compliance.
