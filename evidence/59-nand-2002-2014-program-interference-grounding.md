# Case 59 Grounding Record — NAND Program Interference, 2002–2014

## Purpose

This record grounds [`../cases/59-nand-program-interference-write-induced-neighbor-drift.md`](../cases/59-nand-program-interference-write-induced-neighbor-drift.md).

The bounded question is:

> Can programming one planar floating-gate MLC NAND cell/page materially shift the already-retained threshold-voltage state of neighboring cells, and what evidence establishes the roles of coupling geometry, program order, data values, and later read-reference adaptation?

For the bounded sources, the answer is **yes**, with four evidence layers kept separate:

- **2002** establishes prior `floating-gate interference` vocabulary and capacitive neighbor coupling;
- **2007–2008** establishes manufacturer-linked architectural/program-order mitigation before 2013;
- **2013** directly characterizes modern commercial 2Y-nm MLC NAND and provides the primary experimental basis for this case;
- **2014** extends the recovery relation by using immediate-neighbor values as conditional decoding information in a research proposal/evaluation, not as evidence of named-product deployment.

## Evidence classes

| Source | Date / object | Evidence role | What it can establish | What it cannot establish |
| --- | --- | --- | --- | --- |
| Lee, Hur, Choi, IEEE EDL | May 2002, 0.12-µm NAND | period scholarly/device prior art | `floating-gate interference` vocabulary; adjacent-cell threshold changes coupling into victim threshold; parasitic-capacitance mechanism; pre-2013 chronology | exact behavior of 2Y-nm commercial devices; universal first invention of every related disturb mechanism |
| Park et al., VLSI / JSSC | 2007–2008, Samsung-linked sub-40/60-nm MLC work | manufacturer-linked period engineering prior art | cell-to-cell interference as a scaling problem; temporary-LSB / parallel-MSB programming; program order and neighbor-after-victim exposure as mitigation variables | direct evidence for the 2Y-nm chips in Cai et al.; universal vendor policy |
| Cai et al., ICCD | October 2013, commercial 2Y-nm two-bit MLC NAND | peer-reviewed primary experimental paper | victim/aggressor mechanism; location/order/data dependencies; measured in-order vs out-of-order effects; model; dynamic read-reference proposal/evaluation | commercial deployment of the proposal; later 3D-NAND constants |
| Cai et al., SIGMETRICS | June 2014, experimental MLC NAND + simulations | peer-reviewed research extension | neighbor-conditioned voltage distributions; NAC proposal; using neighbor values to select reread references after ECC failure | named-controller deployment; physical restoration of victim threshold voltage |

## 2002 prior-art record

Jae-Duk Lee, Sung-Hoi Hur, and Jung-Dal Choi, **“Effects of Floating-Gate Interference on NAND Flash Memory Cell Operation,”** *IEEE Electron Device Letters* 23(5), May 2002, pp. 264–266, DOI `10.1109/55.998871`.

Stable bibliographic record:
<https://cir.nii.ac.jp/crid/1362544419688184448>

The indexed abstract states that:

- `floating-gate interference` causes a cell threshold-voltage shift proportional to threshold-voltage changes in adjacent cells;
- the effect results from parasitic capacitive coupling around floating gates;
- a 0.12-µm NAND MLC design shows a bounded reported interference shift around 0.2 V;
- adjacent-wordline voltage also affects programming speed through parasitic capacitance.

The authors' abstract uses first-introduction language for the **concept of floating-gate interference in Flash cells**. This repository does not widen that sentence into `first program-disturb phenomenon in all nonvolatile memory`; related inhibit/boosting/program-disturb mechanisms require their own genealogy.

The only chronology claim needed here is:

> **neighbor-capacitance-induced threshold shift was already an explicit NAND engineering problem by 2002.**

Because a conveniently accessible full facsimile was not directly inspected in this run, detailed equation/figure claims are not assigned to the 2002 paper beyond the indexed abstract/bibliographic evidence.

## 2007–2008 architecture/program-order prior art

Ki Tae Park and colleagues, including Samsung affiliation, published **“A zeroing cell-to-cell interference page architecture with temporary LSB storing program scheme for sub-40nm MLC NAND flash memories and beyond”** at the 2007 Symposium on VLSI Circuits, DOI `10.1109/VLSIC.2007.4342709`.

Institutional record:
<https://pure.uos.ac.kr/en/publications/a-zeroing-cell-to-cell-interference-page-architecture-with-tempor-2/>

Its abstract treats cell-to-cell coupling interference as a major scaling barrier and reports the proposed temporary-LSB page architecture as eliminating the bounded design's bitline coupling and reducing wordline coupling.

The expanded 2008 JSSC version, DOI `10.1109/JSSC.2008.917558`, is indexed at:
<https://pure.uos.ac.kr/en/publications/a-zeroing-cell-to-cell-interference-page-architecture-with-tempor/>

The abstract directly connects the architecture to:

- reducing the number of neighbor cells that are programmed **after** a selected cell;
- reducing the threshold-voltage shift induced during those later neighbor programs;
- reducing interference caused by **the order in which cells are programmed**.

Use in this case: **prior-art and mechanism-boundary control**. It prevents the false claim that program-order-aware interference mitigation began with the 2013 ICCD paper.

## 2013 primary experimental paper inspected

Yu Cai, Onur Mutlu, Erich F. Haratsch, Ken Mai, **“Program Interference in MLC NAND Flash Memory: Characterization, Modeling, and Mitigation,”** *31st IEEE International Conference on Computer Design (ICCD)*, October 2013, pp. 123–130, DOI `10.1109/ICCD.2013.6657034`.

Institutional abstract:
<https://istc-cc.cmu.edu/publications/papers/2013/flash-programming-interference_iccd13_abs.shtml>

Author/institution-hosted PDF:
<https://istc-cc.cmu.edu/publications/papers/2013/flash-programming-interference_iccd13.pdf>

The PDF was directly inspected, including rendered page images for the opening/mechanism discussion and the out-of-order-programming figures.

### Abstract and Introduction — printed p. 123 / PDF p. 1

The paper defines program interference as a programming operation changing not only the selected cell's threshold voltage but also surrounding cells' threshold voltages. The authors state that a sufficiently shifted surrounding cell can cross into a different logical threshold range and later read incorrectly.

They characterize **commercial 2Y-nm (20–24 nm) MLC NAND** using read-retry to measure threshold distributions.

The abstract and contribution list identify three measured dependencies:

1. location of aggressor relative to victim;
2. order in which cells/pages are programmed;
3. data values in the programmed and surrounding cells.

The paper's novelty claim is explicitly bounded to detailed experimental characterization/modeling in **modern** MLC devices. The same introduction cites earlier program-interference work and says previous models had been tested at older nodes.

### Distinguishing retention and program interference — printed p. 123

The Introduction separately lists `erase`, `program interference`, `retention`, and `read` error classes. It describes retention errors as gradual charge loss over time and program interference as unintended victim changes while a neighboring page is programmed.

This directly supports:

> **program interference ≠ retention-age leakage**.

The two error classes can coexist in one raw-error/ECC budget without sharing one trigger.

### Victim/aggressor mechanism — printed pp. 123–124

The paper names the unintentionally shifted cell the **victim** and the programmed neighbor the **aggressor**. It attributes the relation to parasitic capacitance coupling between neighboring floating gates.

MLC logical value is represented by the threshold-voltage range in which a cell falls. A victim crossing a range boundary can therefore become a logical error at later read time.

The paper also states that cells are programmed via incremental step pulse programming (`ISPP`) and that the victim's programmed threshold voltage can change when neighbor cells are programmed later.

This directly grounds the retention-specific relation:

> **the creation of a new neighboring physical state can alter a previously programmed retained state without selecting that older state as the write target.**

### Page programming order — printed pp. 124–126

The tested two-bit MLC all-bit-line device programs LSB and MSB pages at different times. The paper states that manufacturers generally recommend pages in a block be programmed sequentially in page-number order.

It distinguishes:

- **in-page-order programming**;
- **out-of-page-order programming**.

The measured behavior matters because a victim wordline under out-of-order programming can be exposed to more later LSB/MSB programs on neighboring wordlines.

In the reported worst-case comparison, the mean shift after four interference events is approximately **4.4×** the in-order/direct-neighbor comparison. The paper uses this result to explain why in-order programming maintains better signal quality in the tested devices.

Evidence boundary:

> **4.4× is a test-specific result, not a universal NAND constant.**

The general conclusion retained in the case is only that **program order materially changes interference exposure in this measured planar two-bit MLC regime**.

### Physical location and coupling geometry — printed pp. 124–126

The paper distinguishes bitline-to-bitline and wordline-to-wordline interference. In its all-bit-line test architecture, measured same-wordline bitline interference is small/negligible relative to wordline interference because same-wordline cells are programmed together. Direct-neighbor wordlines dominate far-neighbor wordlines; the authors report a direct-neighbor mean shift about 4.2× a far-neighbor comparison in one measured relation.

This grounds:

> **logical neighborhood ≠ sufficient description of physical interference geometry**.

Again, no numerical ratio is projected beyond the tested architecture.

### Data-value dependence — printed pp. 126–127

The paper finds that interference depends on both victim and aggressor logical/threshold states. Because NAND programming moves threshold voltage upward, a larger aggressor threshold change can induce a larger victim shift through coupling.

This is the basis for the case's narrower reconstruction:

> **the reliability margin of one intended value can depend on what value is later written to a physical neighbor**.

It does not mean the neighbor becomes part of the victim's application-level logical identity.

### Wear boundary — printed pp. 128–129

For the tested devices, the authors report that the amount of program interference is **not significantly dependent on P/E-cycle count** over their experiment, in contrast to several other NAND error mechanisms whose susceptibility changes strongly with wear.

That negative result is important: the repository should not automatically make all NAND reliability phenomena `wear clocks` merely because they consume a common ECC budget.

### Predictive model and dynamic read reference — printed pp. 128–130

The paper models the victim shift from neighboring threshold changes without requiring the controller to know exact parasitic coupling capacitances. It proposes learning/predicting shifted threshold-voltage distributions and adjusting the **read reference voltage** accordingly.

The authors' evaluation reports:

- **64% raw BER reduction**;
- **30% P/E-cycle lifetime improvement** relative to their stated ECC baseline.

These are paper-specific evaluation results.

The mechanism supports a key retention distinction:

> **better logical recovery can come from changing the interpretation boundary after the physical state has shifted, rather than physically restoring the victim to its old threshold voltage.**

Evidence boundary:

> **research proposal/evaluation ≠ named commercial-controller deployment**.

## 2014 neighbor-assisted correction extension

Yu Cai, Gulay Yalcin, Onur Mutlu, Erich F. Haratsch, Osman Unsal, Adrian Cristal, Ken Mai, **“Neighbor-Cell Assisted Error Correction for MLC NAND Flash Memories,”** *ACM SIGMETRICS*, June 2014, pp. 491–504.

Institutional abstract:
<https://istc-cc.cmu.edu/publications/papers/2014/neighbor-assisted-error-correction-in-flash_sigmetrics14_abs.shtml>

Author PDF:
<https://users.ece.cmu.edu/~omutlu/pub/neighbor-assisted-error-correction-in-flash_sigmetrics14.pdf>

The paper's abstract states that identifying the value stored in an immediate neighbor makes the victim's data value easier to determine. It characterizes threshold-voltage distributions **conditional on neighbor value** and proposes **Neighbor-Cell Assisted Correction (NAC)**:

1. an ordinary page read fails ECC;
2. the controller rereads with read-reference values corresponding to conditional distributions for possible neighbor values;
3. reread results are used to correct victim cells whose neighbors have the corresponding values.

The reported lifetime improvement is simulation/evaluation evidence, not product deployment.

This record uses the paper only to ground:

> **neighbor retained state can serve as decoding side information after program interference**.

It does not imply that the neighbor is logically part of the victim payload or that reading the neighbor physically repairs the victim.

## Cross-case distinctions

### Versus Case 36 — Flash Correct-and-Refresh

Case 36 centers **retention-age/wear-dependent error accumulation** and proactive rewrite/remapping before ECC margin expires.

Case 59 centers **a later neighboring program operation** that shifts the victim through parasitic coupling.

Supported relation:

> **same ECC budget / possible rewrite remedy ≠ same failure trigger**.

### Versus Case 52 — read disturb

Case 52 centers repeated reads applying pass-through voltage to unselected cells, so cumulative read count becomes a stress history.

Case 59 centers aggressor programming transitions and page/program order.

Supported analogy:

> an operation on one logical target can degrade another retained state.

Required stop condition:

> **read-induced pass-voltage stress ≠ program-induced capacitive coupling**.

### Versus Case 13 — coarse erase

Case 13 shows an explicitly coarse **erase operation** whose sanctioned operation scope can include many cells even while read/program addressing is finer.

Case 59 instead exposes an unintended neighbor side effect of an addressed program operation.

Therefore:

> **coarse commanded state-change geometry ≠ parasitic physical effect geometry**.

### Versus Case 53 — RowHammer

Both cases make physical neighborhood relevant to retention and can cause one access/update stream to harm another state.

But:

- RowHammer involves repeated DRAM activations and disturbance-related charge loss in victim rows;
- Case 59 involves NAND program-time capacitive threshold shift;
- DRAM targeted refresh and NAND program sequencing/read-reference adaptation are not one mechanism or one historical genealogy.

## Terminology boundary: `program disturb`

NAND sources also use `program disturb` for unintended programming of cells/wordlines that should remain inhibited during a program operation, often discussed with boosting/pass voltages. The broader English words overlap, but this case is specifically about **cell-to-cell program interference caused by neighboring threshold transitions and parasitic coupling**.

Do not silently rewrite every `program disturb` source as evidence for this exact mechanism. A source must identify coupling/neighbor-threshold behavior before it is folded into this lineage.

This distinction is especially important because Case 52 already demonstrates how apparently similar `disturb` vocabulary can hide different voltage paths and maintenance clocks.

## Claim ledger

| Claim | Label | Source basis |
| --- | --- | --- |
| floating-gate interference is explicit NAND vocabulary by 2002 | `H/P` | Lee et al. indexed paper/DOI |
| program-order/cell-to-cell mitigation predates 2013 | `H/P` | Park et al. 2007–2008 institutional publication records |
| programming a neighbor can shift a victim threshold distribution | `H/P` | directly inspected Cai et al. 2013 paper |
| location, programming order, and data value affect measured interference | `H/P` | Cai et al. 2013 commercial-chip experiments |
| successful target programming can consume another cell's retention margin | `E` | reconstruction from measured victim shifts |
| read-reference adaptation changes recovery criterion rather than undoing victim physical shift | `E` | Cai 2013 model/mitigation mechanism |
| neighbor value can serve as conditional decoding information | `H/P` for proposal; `E` for retention comparison | Cai et al. 2014 |
| Case 59 and read disturb share cross-target preservation cost | `A` | bounded functional analogy only |
| dense-state creation can modify the conditions of older-state retention | `I` | philosophical interpretation, not actor vocabulary |

## Evidence limits / rejected upgrades

Do **not** upgrade this record into any of the following:

- `Cai et al. 2013 invented program interference`;
- `the 2002 paper proves first discovery of every NAND program-disturb mechanism`;
- `program interference = retention loss`;
- `program interference = read disturb`;
- `program interference = RowHammer`;
- `all-bit-line NAND always has negligible bitline interference`;
- `out-of-order programming is always 4.4× worse`;
- `P/E wear never affects program interference in any NAND generation`;
- `the 2013 read-reference technique shipped in commercial controllers`;
- `NAC shipped in commercial SSDs`;
- `a shifted victim threshold has been physically restored when a reread returns the correct bits`;
- `planar floating-gate measurements directly describe modern 3D charge-trap NAND`.

## Related-repository check

A current GitHub code search for `NAND program interference` in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) returned no dedicated case. There is therefore no existing historical engineering slice to duplicate.

If a broader NAND process/scaling/interference history is later added there, this record should point to that history and keep only the retention-specific evidence chain here.

## Grounding decision

**`grounded`** is justified for this bounded slice because:

- chronology is not anchored on the 2013 experiment alone: 2002 and 2007–2008 prior art constrain novelty claims;
- the central physical relations come from a directly inspected peer-reviewed paper measuring real commercial 2Y-nm MLC NAND chips;
- proposal/evaluation results are not silently upgraded to commercial deployment;
- program interference is explicitly separated from retention-age loss, read disturb, generic program-disturb vocabulary, and RowHammer;
- the cross-case interpretation is limited to the retention relation exposed by the measured mechanism.

Grounded status does **not** close modern 3D-NAND interference, exact vendor program-order contracts, named-controller deployment, or independent product fault validation.
