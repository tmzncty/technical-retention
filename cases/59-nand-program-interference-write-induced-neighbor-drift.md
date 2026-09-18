# NAND Flash Program Interference: Write-Induced Neighbor Drift, Program Order, and Read-Reference Recovery

## Status

**`grounded`** — bounded to floating-gate MLC NAND cell-to-cell **program interference** as documented from 2002 through the 2013 commercial-2Y-nm characterization, with a 2007 manufacturer-linked architecture paper constraining prior art and a 2014 neighbor-assisted correction paper used only as a bounded recovery extension. A separate 1997–1999 terminology/prior-art addendum now grounds three distinct pre-2002 boundaries: Samsung NAND program-inhibit risk, Invox analog/multilevel `program disturb` with history-sensitive word-line bias, and AMD NAND self-boosting `program disturb` / `pass disturb`. These earlier mechanisms are kept separate from the later cell-to-cell genealogy. A 2006–2007 product-document deepening anchors named Samsung MLC and Micron SLC page-program-order contracts while explicitly separating **product usage rules** from claims about their underlying physical cause.

Grounding record: [`../evidence/59-nand-2002-2014-program-interference-grounding.md`](../evidence/59-nand-2002-2014-program-interference-grounding.md).

Terminology/prior-art addendum: [`../evidence/59-program-disturb-1997-1999-terminology-mechanism-boundary.md`](../evidence/59-program-disturb-1997-1999-terminology-mechanism-boundary.md).

Named-product program-order deepening: [`../evidence/59-samsung-micron-2006-2007-product-program-order-deepening.md`](../evidence/59-samsung-micron-2006-2007-product-program-order-deepening.md).

## Scope

This case asks one narrow retention question left open by Cases 04, 36, and 52:

> **What changes when programming one NAND cell/page can shift the already-retained threshold-voltage state of neighboring cells, so the creation of one new state consumes reliability margin in other retained states?**

The bounded mechanism is **program interference** / **floating-gate cell-to-cell interference** in planar floating-gate MLC NAND. Parasitic capacitive coupling lets a threshold-voltage change in a newly programmed `aggressor` cell shift the threshold voltage of a nearby already-programmed `victim` cell. If the victim crosses a read-decision boundary, the later logical value can be misread even though the victim was not the target of the new program operation.

This is **not**:

- a general NAND reliability history;
- the same phenomenon as retention-age charge leakage in Case 36;
- the same phenomenon as read disturb in Case 52;
- a claim that every NAND generation has the same coupling geometry, direction, or magnitude;
- a claim that `program disturb` is always synonymous with cell-to-cell program interference;
- proof that the 2013 dynamic read-reference mechanism or 2014 Neighbor-Cell Assisted Correction (`NAC`) shipped in a named commercial SSD controller;
- a complete account of charge-trap / 3D NAND interference, read retry, LDPC, write amplification, or controller firmware.

The case is deliberately historical and mechanism-specific. The 2013 paper's tested devices are commercial **2Y-nm (20–24 nm), two-bit MLC, all-bit-line planar NAND**. Its measurements do not authorize numerical projection onto later 3D NAND.

## Historical vocabulary and prior-art boundary

### Pre-2002 `program disturb`: one phrase, several bounded mechanisms

The prior-art addendum prevents this case from treating 2002 `floating-gate interference` as the beginning of every programming-induced non-target error.

Samsung US5677873A (published **14 October 1997**) already documents a NAND inhibit problem in which nondesignated cells can be inadvertently programmed during adjacent programming unless channel/source/bitline potentials are biased or boosted appropriately. The inspected patent does not establish the later cell-to-cell interference model and is retained in its own historical vocabulary.

Invox US5818757A (published **6 October 1998**), **“Analog and multi-level memory with reduced program disturb,”** is now more than a title-level witness. Its public patent abstract says that biasing unselected word-lines reduces `program disturb` of the threshold voltages of unselected cells during another write. It explicitly distinguishes rows/cells that have **already been written** from erased or `virgin` ones and discloses sequential row fill plus bias-flag circuitry used to choose the corresponding word-line treatment. This grounds an early write-history-sensitive preservation problem in analog/multilevel nonvolatile memory, but the inspected abstract does **not** establish NAND-string geometry or the 2002 neighboring-floating-gate capacitive-coupling model.

A later same-inventor/SanDisk record, US6285593B1 (2001), discusses `program disturb (or drain disturb)` of previously programmed unselected floating-gate cells and explicitly cites US5818757. It is used only as a continuity/cross-check witness; its later voltage values, decoder embodiments, and control-state implementation are not projected backward into the 1998 patent.

AMD US5991202A (published **23 November 1999**) then explicitly defines NAND **`program disturb`** as unintended programming of an unselected cell on a selected word line and separately names **`pass disturb`** for another unselected-cell path in the self-boosting/pass-voltage regime.

The chronology therefore supports a stronger but still bounded rule:

```text
1997 Samsung NAND:
    failed inhibit / inadvertent programming risk

1998 Invox analog/multilevel NVM:
    already-written unselected threshold state can be disturbed
    + prior row state changes protective bias policy

1999 AMD NAND:
    self-boosting `program disturb` and `pass disturb` explicitly distinguished

2002+ Case 59 lineage:
    neighboring aggressor threshold transition
    -> parasitic floating-gate coupling
    -> victim threshold shift
```

Therefore:

> **pre-2002 program-disturb / program-inhibit evidence ≠ proof of the 2002+ cell-to-cell capacitive program-interference mechanism.**

And conversely:

> **2002 `floating-gate interference` vocabulary ≠ origin of every non-target threshold-state preservation problem caused by programming.**

The Invox evidence adds a specific anti-anachronism rule:

> **same phrase `program disturb` ≠ same array topology, electrical cause, or mitigation genealogy.**

See the dedicated [`program-disturb terminology/mechanism addendum`](../evidence/59-program-disturb-1997-1999-terminology-mechanism-boundary.md) for source custody, the later continuity witness, and rejected origin upgrades.

### `floating-gate interference` by 2002

Jae-Duk Lee, Sung-Hoi Hur, and Jung-Dal Choi, **“Effects of Floating-Gate Interference on NAND Flash Memory Cell Operation,”** *IEEE Electron Device Letters* 23(5), May 2002, pp. 264–266, DOI `10.1109/55.998871`, explicitly describes a victim-cell threshold-voltage shift proportional to adjacent-cell threshold changes and attributes it to parasitic capacitive coupling around neighboring floating gates.

The paper's abstract uses the phrase **`floating-gate interference`**. Its own priority language is retained narrowly: the authors say they introduce that concept for Flash cells. This repository does not expand that sentence into a universal claim that no earlier EEPROM/NAND coupling phenomenon or related disturbance mechanism existed.

The important chronological result is simpler:

> **cell-to-cell capacitive interference in NAND is documented well before the 2013 commercial-chip characterization.**

### Named product program-order contracts by 2006–2007

Samsung's manufacturer-authored **K9GAG08U0M / K9GAG08B0M** datasheet identifies the family as a **two-bit-per-cell** 16-Gbit NAND product. Its revision history runs from an initial issue dated **12 April 2006** through Rev. 0.6 dated **12 February 2007**. The technical notes state that pages within a block must be programmed consecutively from the LSB page toward the MSB page and that **random page-address programming is prohibited**. The same document limits consecutive partial-page programming without intervening erase to one cycle for the page.

That directly closes the previous lack of a named MLC product contract, but it does **not** identify cell-to-cell interference as the sole physical reason for the rule.

A same-period Micron SLC counterexample makes that boundary stronger. Micron's named `MT29F4G08AAA / MT29F8G08BAA / MT29F8G08DAA / MT29F16G08FAA` family is explicitly **SLC**; its Rev. A initial release is August 2006 and Rev. B is February 2007. Yet it likewise requires pages to be programmed consecutively from least- to most-significant page address and prohibits random page-address programming, while allowing up to four partial-page program operations under its stated rule.

Therefore:

> **named-product sequential-programming rule ≠ sufficient evidence for MLC cell-to-cell program interference.**

The product rules establish legal programming histories at the interface. The physical cause must be grounded separately.

See [`59-samsung-micron-2006-2007-product-program-order-deepening.md`](../evidence/59-samsung-micron-2006-2007-product-program-order-deepening.md) for the full source and non-claim ledger.

### Architecture/program-order mitigation by 2007–2008

Ki Tae Park and colleagues' Samsung-linked VLSI/JSSC work treats **cell-to-cell interference** as a scaling barrier and proposes a temporary-LSB / parallel-MSB programming architecture intended to reduce coupling. The 2008 journal abstract explicitly says the scheme reduces the number of neighboring cells programmed after a selected cell and the amount of their threshold-voltage shift, and ties part of the interference to **the order in which cells are programmed**.

This is strong prior art against any claim that programming-order-aware mitigation began with Cai et al. in 2013.

The named Samsung product contract and the Samsung-linked research are contemporaneous, but this case does not infer a direct implementation genealogy between the K9GAG08X0M product and the Park et al. architecture without a source that makes that link.

### `program interference`, `victim`, and `aggressor` in 2013

Yu Cai, Onur Mutlu, Erich F. Haratsch, and Ken Mai, **“Program Interference in MLC NAND Flash Memory: Characterization, Modeling, and Mitigation,”** ICCD 2013, pp. 123–130, uses:

- `program interference` / `program interference errors`;
- `victim cell`;
- `aggressor cell`;
- `wordline to wordline interference`;
- `bitline to bitline interference`;
- `in-page-order programming` and `out-of-page-order programming`;
- `threshold voltage (Vth)` and `threshold voltage distribution`;
- `read reference voltage`;
- `read-retry`;
- `raw bit error rate (BER)`.

The authors claim the first **detailed experimental characterization and realistic model in modern 2Y-nm commercial MLC NAND**, not invention of the phenomenon. Their Related Work explicitly cites earlier 120-nm and 60-nm interference models and other simulation-based work.

## Retained state and constitutive relations

The bounded regime contains several separable states and relations:

1. **victim-cell physical state** — floating-gate charge expressed as a threshold-voltage position/distribution;
2. **victim logical value** — the MLC state inferred from the voltage range in which the victim is read;
3. **aggressor program transition** — a neighboring cell's intended movement to a new threshold-voltage state;
4. **coupling geometry** — wordline/bitline/diagonal physical relation and parasitic capacitance between cells;
5. **program-order state** — which pages have already been programmed, which next page choices remain legal under a product contract, and—within the bounded MLC mechanism—which LSB/MSB and neighboring program events remain possible;
6. **per-page partial-program budget** — a separate product-contract history dimension; the inspected Samsung MLC part permits one cycle while the inspected Micron SLC family permits up to four under their respective rules;
7. **neighbor data values** — the magnitude of aggressor threshold change depends on the value being programmed, affecting victim shift;
8. **read-reference policy** — the voltage boundary used later to interpret the shifted physical distribution;
9. **ECC margin** — the remaining error-correction envelope above raw physical errors;
10. **optional neighbor-assisted decoding information** — in the 2014 NAC proposal, the value of an immediate neighbor can select a more appropriate conditional read-reference set;
11. **prior-art row-history / bias-selection knowledge** — in the 1998 Invox abstract, whether an unselected row already contains programmed data changes the protective word-line bias used during a later write.

`program-order state`, `partial-program budget`, and `row-history / bias-selection knowledge` are project analytical descriptions. Period sources use concrete page-order, cycle-limit, row-filled, and bias-selection language. No claim is made that contemporary engineers called these a `retention clock`, a modern FTL frontier, or a crash-persistent metadata record.

## Engineering reconstruction

### Programming one state can alter another already-retained state

The central Case 59 relation is not ordinary overwrite. The victim cell is not selected as the new program target. Nevertheless, the aggressor's threshold-voltage increase couples capacitively into the victim floating gate and shifts the victim's threshold voltage.

Therefore:

> **successful aggressor programming ≠ unchanged neighboring retained state**.

And:

> **write target ≠ complete physical effect scope**.

This sharpens Case 13's erase-granularity result in the opposite direction. Coarse erase deliberately changes a larger explicit operation scope; program interference is an **unintended physical side effect** whose scope is set by coupling geometry rather than by the logical write designation.

The pre-2002 records show that the high-level lesson predates this particular mechanism: writes could already impose non-target preservation obligations under different inhibit/bias regimes. That functional overlap does not erase the mechanism distinction.

### Safe write policy can depend on prior non-target state

The 1998 Invox abstract adds a bounded relation that is adjacent to, but not identical with, Case 59's later page-order history. The same current write can require different unselected-row bias depending on whether a row has already been written or remains erased/virgin.

Therefore:

> **same current write target ≠ same safe electrical policy under different prior row histories**.

And:

> **payload state ≠ the control knowledge needed to preserve that payload during a later write**.

This does not prove that the disclosed bias flags survive power loss or reset. It only establishes that prior programming state is used by the disclosed protection logic.

### Logical write isolation can be weaker than physical-cell isolation

At the interface or FTL level, two logical pages can appear independently writable. At the array level, however, the electric state produced by programming one cell depends on nearby cell geometry and can change an already-programmed neighbor.

Therefore:

> **logical page independence ≠ physical retention independence**.

This does not mean every neighboring cell changes enough to alter its decoded value. It means the physical distributions are coupled and the future error margin of a victim can be consumed by a different program operation.

### Program order can be a retention constraint

The 2013 commercial-chip characterization finds a large difference between in-page-order and tested out-of-page-order programming. Under the recommended sequential page-number order, a victim is exposed to a more constrained sequence of later neighbor programming. In the authors' tested out-of-order example, a victim can receive interference from both LSB and MSB programming of neighboring wordlines; their worst-case measured mean shift is about **4.4×** the in-order comparison in that setup.

The authors also state that Flash manufacturers generally recommend programming pages in a block sequentially in page-number order. The 2006–2007 Samsung/Micron datasheet deepening adds direct named-product evidence that sequential in-block programming was an explicit controller-facing contract in same-period planar NAND.

But both the Micron SLC comparison and the earlier Invox sequential-row example prevent causal overreach:

> **sequential-programming/recording structure ≠ proof of one particular physical mechanism.**

Therefore:

> **programming sequence can be part of the physical and interface conditions under which previously written data remains reliably usable**.

And:

> **same final set of programmed pages ≠ same legal or physical program history**.

That relation must remain bounded. The 2013 paper characterizes particular two-bit MLC page-order regimes; the 2007 datasheets define product usage constraints; the 1998 Invox abstract describes a different analog/multilevel row-history/bias arrangement. None proves that every reordering in every nonvolatile-memory generation produces the same failure mode.

### Command success does not certify the whole programming history

The named product documents expose per-operation status while separately constraining the sequence in which pages may be programmed. Consequently:

> **one page-program command reporting success ≠ proof that the complete block history satisfies every product programming constraint**.

This does not assert that prohibited histories are accepted or that they necessarily cause silent corruption. It only separates transaction outcome from history-level admissibility.

### Retention can depend on a neighboring value that is not part of the victim's logical identity

The amount of interference depends not only on physical position and order but also on the threshold-voltage change of the aggressor, which depends on the aggressor's programmed data value. The victim's resulting voltage distribution therefore carries a conditional dependence on **neighbor data**.

Thus:

> **victim logical identity ≠ physically self-contained victim state**.

A cell can retain the same intended logical bits while its physical margin depends on what was later written nearby.

This is not a claim that the neighbor becomes part of the logical payload. It is a claim that physical recoverability can be relational.

### Read-reference adaptation can recover interpretation without undoing the physical shift

Cai et al. model the shifted distributions and propose adjusting the read reference voltage so the later read boundary better matches the predicted post-interference distribution. Their evaluation reports a **64% reduction in raw BER** and a **30% modeled P/E-cycle lifetime improvement** relative to their baseline.

The important retention distinction is:

> **recovered logical interpretation ≠ restoration of the pre-interference physical threshold voltage**.

Changing the read boundary does not rewind the victim floating gate. It changes how a physically shifted state is interpreted.

Therefore:

> **retention can sometimes be extended by adapting the recovery criterion rather than renewing the stored embodiment**.

This is a proposed/evaluated controller mechanism in the paper, not evidence of named-product deployment.

### Neighbor state can become recovery side information

The 2014 **Neighbor-Cell Assisted Error Correction (NAC)** work makes the relational recovery point even sharper. It experimentally finds that conditioning a victim's threshold-voltage distribution on the value of its immediate neighbor can produce better read-reference choices. NAC proposes rereading an ECC-failing page using reference voltages selected for particular neighbor values and using those rereads to correct cells whose neighbors have those values.

Therefore:

> **a neighboring retained value can become decoding side information for another retained value**.

And again:

> **neighbor-assisted logical recovery ≠ physical restoration of the victim cell**.

The paper reports a simulated lifetime improvement, not a shipped-controller field result.

## Distinguishing program interference from adjacent failure modes

### Versus Case 36 — retention-age error

Case 36 centers charge loss/drift with **elapsed retention age** and wear as major inputs to proactive correction/refresh. Program interference instead occurs when a **neighbor is programmed**.

Therefore:

> **write-induced neighbor drift ≠ elapsed-time retention leakage**.

Both can consume the same ECC budget and both can be mitigated by later reread/rewrite/controller work, but common recovery resources do not make their physical causes identical.

### Versus Case 52 — read disturb

Case 52 centers repeated reads whose pass-through voltage cumulatively stresses unselected cells. Case 59 centers programming-induced capacitive coupling from an aggressor threshold transition.

Therefore:

> **program interference ≠ read disturb**.

The shared functional result is only that **an operation on one logical target can degrade a different retained state**. Their voltages, triggers, histories, and mitigation opportunities are different.

### Versus pre-2002 `program disturb`

The earlier records establish that programming-induced non-target state change was already an engineering problem, but they do not define one universal mechanism.

The Invox record is especially useful as a counterexample to terminology-based genealogy: it uses `program disturb` in an analog/multilevel nonvolatile-memory design where prior programmed/erased row state changes the word-line protection policy. AMD then uses the same phrase in a NAND self-boosting context. Case 59 later uses `program interference` for experimentally characterized neighboring floating-gate coupling.

Accordingly:

> **`program disturb` terminology ≠ automatically the same mechanism as bounded cell-to-cell program interference**.

A source must establish the mechanism before terms are merged.

## Time and maintenance

Program interference introduces a temporal relation unlike ordinary wall-clock retention:

```text
victim programmed
    -> victim currently readable
    -> later neighboring page/cell program
    -> victim threshold distribution shifts
    -> raw-error margin changes
    -> later read may require different reference voltage / ECC
```

The product-contract deepening adds a second, related but non-identical history:

```text
block erased
    -> pages programmed along a legal frontier
    -> partial-program budget consumed per page
    -> future legal program choices narrow
```

The Invox prior-art deepening adds a third, older but mechanism-distinct control history:

```text
row erased / virgin
    -> row becomes programmed
    -> protection state for later writes changes
    -> future unselected-wordline bias policy changes
```

These are not one history. The first is physical cell-to-cell interference, the second is a NAND product-admissibility history, and the third is an analog/multilevel bias-selection history. Their common analytical point is only that **later safe operation can depend on earlier state transitions**.

The relevant `before/after` relation is therefore not merely the number of seconds since the victim was written. It can include **the sequence of neighboring program events, the legal program history of the block, or prior programmed/erased state used by protection logic**.

This gives the project another bounded maintenance category:

> **operation-sequence-conditioned retention**.

It should not be promoted to a universal controlled term until more cases require it.

Maintenance can occur at several different loci:

- memory-array bias/inhibit design can protect non-target state;
- NAND/device design can reduce coupling;
- page architecture/program sequencing can reduce later aggressor exposure;
- controller allocation can keep future program commands inside a product's legal history;
- controller modeling can predict shifted distributions;
- read retry/reference adaptation can compensate at read time;
- ECC can mask residual raw errors;
- rewrite/remapping can renew physical margin through mechanisms covered in other cases.

These are not one operation called `refresh`.

## Failure and forgetting boundaries

Distinct failure paths in this bounded case include:

- insufficient inhibit/bias margin can alter a non-target cell during programming;
- prior written/erased state can make one protective bias policy safe and another unsafe in the Invox design context;
- parasitic coupling shifts a victim distribution after neighbor programming;
- a particular program order exposes the victim to more/larger later aggressor transitions;
- a controller attempts a program history outside a named product's documented contract;
- a page's documented partial-program budget is exhausted;
- particular aggressor/victim data combinations produce more harmful shifts;
- process variation broadens the distribution of victim responses;
- a fixed read-reference voltage becomes mismatched to a shifted distribution;
- raw errors exceed ECC/retry/recovery capability;
- controller inference/model error can choose a suboptimal reference boundary.

Forgetting here is not `a write happened`, and a datasheet prohibition is not itself proof of corruption. Within the grounded interference mechanism, forgetting is the eventual inability to recover the intended victim value from a physical state whose separation margin has been consumed by neighboring program operations and other noise sources.

The pre-2002 prior art adds only this bounded historical correction: engineers already had to protect meaningful non-target state from later programming operations before the specific Case 59 coupling model was published.

## Historical record / engineering reconstruction / interpretation ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| NAND inadvertent-programming/inhibit risk is public by 1997 | `H/P` | Samsung US5677873A; no `program disturb` coinage claim |
| Invox uses `program disturb` publicly by Oct 1998 and its abstract describes threshold disturbance of unselected cells during another write | `H/P` | US5818757A public patent abstract |
| Invox distinguishes already-written from erased/virgin rows for protective bias and discloses row-filled bias flags | `H/P` | US5818757A abstract; persistence horizon of flags not established |
| later So/Wong/SanDisk work discusses program/drain disturb of previously programmed unselected cells and cites US5818757 | `H/P` continuity witness | US6285593B1; later embodiments are not back-projected |
| AMD explicitly distinguishes NAND `program disturb` and `pass disturb` by 1999 | `H/P` | US5991202A |
| floating-gate interference is documented in NAND by 2002 | `H/P` | Lee et al. bibliographic/abstract record and DOI |
| Samsung K9GAG08X0M public datasheet history begins in 2006 and Rev. 0.6 is dated 12 Feb 2007 | `H/P` | manufacturer datasheet revision history |
| Samsung's named two-bit MLC product requires sequential LSB→MSB page programming and prohibits random page programming | `H/P` | manufacturer technical note / PAGE PROGRAM section |
| Samsung limits partial-page programming to one cycle for the page in the inspected revision | `H/P` | manufacturer AC table + PAGE PROGRAM prose |
| Micron's named Feb-2007 SLC family also requires consecutive page programming while allowing up to four partial-page operations | `H/P` | manufacturer datasheet |
| similar sequencing language across different devices does not by itself identify the same physical cause | `E/A` | cross-source counterexample; no common mechanism inferred |
| Samsung-linked work treated cell-to-cell interference and programming order as an engineering problem by 2007–2008 | `H/P` | period VLSI/JSSC publication record |
| 2013 commercial 2Y-nm tests measured location-, order-, and data-dependent program interference | `H/P` | directly inspected ICCD paper |
| a successful aggressor write can reduce a neighbor's future retention margin | `E` | reconstruction from measured victim-threshold shifts |
| safe write policy can depend on prior non-target programmed/erased state | `E` | bounded reconstruction from Invox abstract |
| program order can become part of reliable-retention conditions | `E` | bounded to measured/recommended page-order regime and named product contracts |
| adaptive read reference can recover logical interpretation without restoring the old physical voltage | `E` | mechanism follows directly from read-boundary adaptation; deployment not claimed |
| NAC uses neighbor state as decoding side information | `H/P` for proposal and evaluation; `E` for retention comparison | 2014 experimental/research paper; no product deployment claimed |
| this is analogous to Case 52 because one target operation affects another retained state | `A` | functional analogy only; physical mechanisms differ |
| write and retention are not always separable operations | `I` | bounded philosophical pressure from mechanism; not historical actor vocabulary |

## Philosophical / media-theoretical interpretation — bounded

The case supplies one narrow conceptual correction:

> **retention is not always an interval in which nothing relevant happens to the retained thing. The creation of a new nearby state can revise the physical conditions under which an older state remains recoverable.**

The prior-art deepening adds a complementary point: preserving older state during a new write can require **knowledge that the older state already exists**, because the safe electrical treatment of non-target cells may depend on whether they are programmed or still erased.

The named-product deepening adds a third bounded point: a medium can expose a **history of admissible future operations** alongside its currently retained payload. The current bits do not necessarily tell the whole system which program operation is legal next.

These do not make every write an act of forgetting, and they do not imply that the 1997–2014 sources were offering a theory of memory. They simply prevent the repository from treating `write` as affecting only the newly written object, `retention` as an isolated property of each cell, or the present payload as a complete description of future-valid operation.

The bounded physical lesson is relational: in dense NAND, the reliability of one retained value can depend on **what is later written nearby, in what order, to what threshold state, and how the later reader interprets the resulting distribution**. The bounded prior-art lesson is that even before this specific coupling model, safe later writes could depend on the prior state of unselected memory. The bounded product-contract lesson is separate: correct future programming can also depend on **which physical pages and partial-program opportunities have already been consumed**.

## Functional analogies and stop conditions

### Case 52 — read disturb

Safe analogy:

> a successful operation aimed at one logical target can create a preservation cost for another retained state.

Stop condition:

- Case 52 uses repeated-read pass-through stress;
- 1997/1999 NAND program disturb uses inhibit/self-boosting bias;
- 1998 Invox uses history-sensitive protection against program/disturb of unselected analog/multilevel cells;
- Case 59 uses programming-induced capacitive coupling;
- read count, row-history bias, NAND self-boosting, and program sequence are different histories/control problems.

### Case 53 — RowHammer

A second bounded analogy is possible: both RowHammer and NAND program interference expose **physical-neighbor coupling that breaks a purely logical account of operation scope**.

Stop condition:

- RowHammer is repeated DRAM activation causing disturbance/charge-loss risk in physical victim rows;
- NAND program interference is threshold shift caused by neighboring floating-gate programming;
- refresh-targeting and NAND read-reference/program-order policy are not historically or physically the same.

### Cases 43 / 93 — control knowledge protects payload

A very narrow functional analogy is permitted: AVATAR's refresh classification and Invox's row-filled/bias-selection relation both make payload preservation depend on non-payload control knowledge about current state.

Stop condition:

- AVATAR is a DRAM refresh-policy/revalidation problem;
- Invox is a write-time nonvolatile-memory bias-selection problem;
- no genealogy, shared metadata format, or shared persistence horizon is claimed.

## Cross-case result

Case 59 adds the following relations:

```text
logical program target
    !=
prior programmed/erased state used by protection logic
    !=
product-legal next program operation
    !=
partial-program budget
    !=
physical electrical effect scope
    !=
neighbor coupling geometry
    !=
program-order history
    !=
neighbor data-dependent threshold shift
    !=
current raw-error population
    !=
ECC-corrected logical recoverability
    !=
read-reference interpretation policy
```

The strongest findings are:

- **pre-2002 programming-induced non-target preservation problems ≠ the later cell-to-cell interference mechanism**;
- **same phrase `program disturb` ≠ mechanism identity**;
- **same current write target ≠ same safe bias policy under different prior row histories**;
- **successful aggressor programming ≠ unchanged neighboring retained state**;
- **logical page independence ≠ physical retention independence**;
- **same final programmed population ≠ necessarily the same interference history**;
- **named-product sequencing rule ≠ identified physical mechanism**;
- **same broad sequencing rule across MLC and SLC ≠ same silicon cause**;
- **program order can be a retention and product-admissibility constraint**;
- **victim logical identity ≠ physically self-contained victim state**;
- **read-reference recovery ≠ physical-state restoration**;
- **neighbor state can become decoding side information**;
- **program interference ≠ retention-age leakage ≠ read disturb**.

## Related repositories

A fresh code search in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Invox program disturb`, NAND `program interference`, and related vocabulary returned no dedicated case. This file therefore keeps the retention-specific mechanism and product-contract comparison here rather than duplicating an existing historical engineering account.

If `computing-archaeology` later develops a broader NAND/nonvolatile-memory programming history, the Invox/SanDisk analog-memory genealogy, self-boosting/local-boost evolution, page-programming history, and vendor architecture chronology should primarily live there. This case should retain the relational retention argument and the boundary between **historical term, physical mechanism, product rule, and controller/control-state history**.

## Sources

1. Jae-Duk Lee, Sung-Hoi Hur, Jung-Dal Choi, **“Effects of Floating-Gate Interference on NAND Flash Memory Cell Operation,”** *IEEE Electron Device Letters* 23(5), May 2002, pp. 264–266, DOI `10.1109/55.998871`. Bibliographic record: <https://cir.nii.ac.jp/crid/1362544419688184448>.
2. Ki Tae Park, Myounggon Kang, Doogon Kim, Soonwook Hwang, Yeong Taek Lee, Changhyun Kim, Kinam Kim, **“A zeroing cell-to-cell interference page architecture with temporary LSB storing program scheme for sub-40nm MLC NAND flash memories and beyond,”** *2007 Symposium on VLSI Circuits*, pp. 188–189, DOI `10.1109/VLSIC.2007.4342709`. Institutional record: <https://pure.uos.ac.kr/en/publications/a-zeroing-cell-to-cell-interference-page-architecture-with-tempor-2/>.
3. Ki Tae Park et al., **“A zeroing cell-to-cell interference page architecture with temporary LSB storing and parallel MSB program scheme for MLC NAND flash memories,”** *IEEE Journal of Solid-State Circuits* 43(4), 2008, pp. 919–927, DOI `10.1109/JSSC.2008.917558`. Institutional record: <https://pure.uos.ac.kr/en/publications/a-zeroing-cell-to-cell-interference-page-architecture-with-tempor/>.
4. Yu Cai, Onur Mutlu, Erich F. Haratsch, Ken Mai, **“Program Interference in MLC NAND Flash Memory: Characterization, Modeling, and Mitigation,”** *31st IEEE International Conference on Computer Design (ICCD)*, October 2013, pp. 123–130, DOI `10.1109/ICCD.2013.6657034`. Author/institution PDF: <https://istc-cc.cmu.edu/publications/papers/2013/flash-programming-interference_iccd13.pdf>; abstract: <https://istc-cc.cmu.edu/publications/papers/2013/flash-programming-interference_iccd13_abs.shtml>.
5. Yu Cai, Gulay Yalcin, Onur Mutlu, Erich F. Haratsch, Osman Unsal, Adrian Cristal, Ken Mai, **“Neighbor-Cell Assisted Error Correction for MLC NAND Flash Memories,”** *ACM SIGMETRICS*, June 2014, pp. 491–504. Author PDF: <https://users.ece.cmu.edu/~omutlu/pub/neighbor-assisted-error-correction-in-flash_sigmetrics14.pdf>; institutional abstract: <https://istc-cc.cmu.edu/publications/papers/2014/neighbor-assisted-error-correction-in-flash_sigmetrics14_abs.shtml>.
6. Samsung Electronics, **K9GAG08U0M / K9GAG08B0M / K9LBG08U1M, 2G × 8 Bit NAND Flash Memory**, preliminary Rev. 0.6, 12 February 2007. Public mirror: <https://opendevices.ru/wp-content/uploads/2011/11/K9GAG08U0M.pdf>; distributor mirror: <https://docs.rs-online.com/b7c3/0900766b80defffe.pdf>.
7. Micron Technology, **4Gb, 8Gb, and 16Gb x8 NAND Flash Memory**, MT29F4G08AAA / MT29F8G08BAA / MT29F8G08DAA / MT29F16G08FAA, Rev. B, February 2007; Rev. A initial release August 2006. Public text mirror: <https://studylib.net/doc/8343321/mt29fxg08xaa---digi-key>; USPTO PTAB-hosted copy: <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1544922/download-documents?artifactId=Gaz2p22wnz7JIP8TNNKPNQt6NuP5glGQRpo_XvDZShTeDlySjz8oH14>.
8. Hock C. So, Sau C. Wong, Invox Technology, **US5818757A, “Analog and multi-level memory with reduced program disturb,”** published 6 October 1998. Stable patent record: <https://patents.google.com/patent/US5818757A/en>. The present case uses the public indexed abstract for mechanism-level claims and does not claim full-specification inspection.
9. Sau C. Wong et al., SanDisk, **US6285593B1, “Word-line decoder for multi-bit-per-cell and analog/multi-level memories with improved resolution and signal-to-noise ratio,”** issued 4 September 2001. Public full-text mirror: <https://patents.justia.com/patent/6285593>. Used as later same-inventor continuity/cross-check evidence, not as a substitute for the 1998 full specification.

## Remaining work

The bounded case is grounded, but several distinct regimes remain open:

- direct full-text inspection of the 2002 IEEE paper if an accessible archival copy becomes available;
- direct page-by-page inspection of the complete 1998 US5818757 facsimile/specification beyond the now-inspected mechanism-bearing public abstract;
- pre-1998 `program disturb` vocabulary in directly inspected full-text nonvolatile-memory sources;
- vendor evidence explicitly tying a named product's page-order constraint to cell-to-cell program interference, rather than merely stating the usage rule;
- later planar MLC/TLC and modern charge-trap / 3D-NAND program-order/interference geometry;
- named-controller deployment of interference-aware reference-voltage or neighbor-assisted recovery;
- a shipped-controller/FTL trace showing how program-order frontier state is retained or reconstructed across sudden power loss;
- independent product fault validation, including bounded tests of documented sequence violations;
- exact persistence/reconstruction horizon of any controller state that records prior programming history;
- direct genealogy, if any, among analog/multilevel Invox disturb mitigation, NAND self-boosting disturb mitigation, and later cell-to-cell-interference work.
