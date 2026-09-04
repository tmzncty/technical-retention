# NAND Flash Program Interference: Write-Induced Neighbor Drift, Program Order, and Read-Reference Recovery

## Status

**`grounded`** — bounded to floating-gate MLC NAND cell-to-cell **program interference** as documented from 2002 through the 2013 commercial-2Y-nm characterization, with a 2007 manufacturer-linked architecture paper constraining prior art and a 2014 neighbor-assisted correction paper used only as a bounded recovery extension.

Grounding record: [`../evidence/59-nand-2002-2014-program-interference-grounding.md`](../evidence/59-nand-2002-2014-program-interference-grounding.md).

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

### `floating-gate interference` by 2002

Jae-Duk Lee, Sung-Hoi Hur, and Jung-Dal Choi, **“Effects of Floating-Gate Interference on NAND Flash Memory Cell Operation,”** *IEEE Electron Device Letters* 23(5), May 2002, pp. 264–266, DOI `10.1109/55.998871`, explicitly describes a victim-cell threshold-voltage shift proportional to adjacent-cell threshold changes and attributes it to parasitic capacitive coupling around neighboring floating gates.

The paper's abstract uses the phrase **`floating-gate interference`**. Its own priority language is retained narrowly: the authors say they introduce that concept for Flash cells. This repository does not expand that sentence into a universal claim that no earlier EEPROM/NAND coupling phenomenon or related disturbance mechanism existed.

The important chronological result is simpler:

> **cell-to-cell capacitive interference in NAND is documented well before the 2013 commercial-chip characterization.**

### Architecture/program-order mitigation by 2007–2008

Ki Tae Park and colleagues' Samsung-linked VLSI/JSSC work treats **cell-to-cell interference** as a scaling barrier and proposes a temporary-LSB / parallel-MSB programming architecture intended to reduce coupling. The 2008 journal abstract explicitly says the scheme reduces the number of neighboring cells programmed after a selected cell and the amount of their threshold-voltage shift, and ties part of the interference to **the order in which cells are programmed**.

This is strong prior art against any claim that programming-order-aware mitigation began with Cai et al. in 2013.

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
5. **program-order state** — which LSB/MSB pages have already been programmed and which neighboring programs remain possible;
6. **neighbor data values** — the magnitude of aggressor threshold change depends on the value being programmed, affecting victim shift;
7. **read-reference policy** — the voltage boundary used later to interpret the shifted physical distribution;
8. **ECC margin** — the remaining error-correction envelope above raw physical errors;
9. **optional neighbor-assisted decoding information** — in the 2014 NAC proposal, the value of an immediate neighbor can select a more appropriate conditional read-reference set.

`program-order state` is a project analytical description. Period sources use concrete page-programming-order language; no claim is made that contemporary engineers called it a `retention clock` or `history state`.

## Engineering reconstruction

### Programming one state can alter another already-retained state

The central retention relation is not ordinary overwrite. The victim cell is not selected as the new program target. Nevertheless, the aggressor's threshold-voltage increase couples capacitively into the victim floating gate and shifts the victim's threshold voltage.

Therefore:

> **successful aggressor programming ≠ unchanged neighboring retained state**.

And:

> **write target ≠ complete physical effect scope**.

This sharpens Case 13's erase-granularity result in the opposite direction. Coarse erase deliberately changes a larger explicit operation scope; program interference is an **unintended physical side effect** whose scope is set by coupling geometry rather than by the logical write designation.

### Logical write isolation can be weaker than physical-cell isolation

At the interface or FTL level, two logical pages can appear independently writable. At the array level, however, the electric state produced by programming one cell depends on nearby cell geometry and can change an already-programmed neighbor.

Therefore:

> **logical page independence ≠ physical retention independence**.

This does not mean every neighboring cell changes enough to alter its decoded value. It means the physical distributions are coupled and the future error margin of a victim can be consumed by a different program operation.

### Program order can be a retention constraint

The 2013 commercial-chip characterization finds a large difference between in-page-order and tested out-of-page-order programming. Under the recommended sequential page-number order, a victim is exposed to a more constrained sequence of later neighbor programming. In the authors' tested out-of-order example, a victim can receive interference from both LSB and MSB programming of neighboring wordlines; their worst-case measured mean shift is about **4.4×** the in-order comparison in that setup.

The authors also state that Flash manufacturers generally recommend programming pages in a block sequentially in page-number order.

Therefore:

> **programming sequence can be part of the physical conditions under which previously written data remains reliably distinguishable**.

And:

> **same final set of programmed pages ≠ same interference history**.

That last relation must be bounded. The 2013 paper characterizes particular two-bit MLC page-order regimes; it does not prove that every reordering in every NAND generation produces a distinct final distribution.

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

## Distinguishing program interference from adjacent NAND failure modes

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

### Versus generic `program disturb`

NAND literature also uses `program disturb` for unintended programming/error mechanisms involving cells that are meant to remain inhibited/unselected during a program operation. That family overlaps the broader fact that programming can disturb non-target cells, but the bounded sources here specifically model **cell-to-cell capacitive program interference** as victim threshold shift caused by neighboring aggressor programming.

Accordingly:

> **`program disturb` terminology ≠ automatically the same mechanism as the bounded cell-to-cell program-interference model**.

A source must establish the mechanism before the terms are merged.

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

The relevant `before/after` relation is the **sequence of neighboring program events**, not merely the number of seconds since the victim was written.

This gives the project another bounded maintenance category:

> **operation-sequence-conditioned retention**.

It should not be promoted to a universal controlled term until more cases require it.

Maintenance can occur at several different loci:

- NAND/device design can reduce coupling;
- page architecture/program sequencing can reduce later aggressor exposure;
- controller modeling can predict shifted distributions;
- read retry/reference adaptation can compensate at read time;
- ECC can mask residual raw errors;
- rewrite/remapping can renew physical margin through mechanisms covered in other cases.

These are not one operation called `refresh`.

## Failure and forgetting boundaries

Distinct failure paths in this bounded case include:

- parasitic coupling shifts a victim distribution after neighbor programming;
- a particular program order exposes the victim to more/larger later aggressor transitions;
- particular aggressor/victim data combinations produce more harmful shifts;
- process variation broadens the distribution of victim responses;
- a fixed read-reference voltage becomes mismatched to a shifted distribution;
- raw errors exceed ECC/retry/recovery capability;
- controller inference/model error can choose a suboptimal reference boundary.

Forgetting here is not `a write happened`. It is the eventual inability to recover the intended victim value from a physical state whose separation margin has been consumed by neighboring program operations and other noise sources.

## Historical record / engineering reconstruction / interpretation ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| floating-gate interference is documented in NAND by 2002 | `H/P` | Lee et al. bibliographic/abstract record and DOI |
| Samsung-linked work treated cell-to-cell interference and programming order as an engineering problem by 2007–2008 | `H/P` | period VLSI/JSSC publication record |
| 2013 commercial 2Y-nm tests measured location-, order-, and data-dependent program interference | `H/P` | directly inspected ICCD paper |
| a successful aggressor write can reduce a neighbor's future retention margin | `E` | reconstruction from measured victim-threshold shifts |
| program order can become part of reliable-retention conditions | `E` | bounded to measured/recommended page-order regime |
| adaptive read reference can recover logical interpretation without restoring the old physical voltage | `E` | mechanism follows directly from read-boundary adaptation; deployment not claimed |
| NAC uses neighbor state as decoding side information | `H/P` for proposal and evaluation; `E` for retention comparison | 2014 experimental/research paper; no product deployment claimed |
| this is analogous to Case 52 because one target operation affects another retained state | `A` | functional analogy only; physical mechanisms differ |
| write and retention are not always separable operations | `I` | bounded philosophical pressure from mechanism; not historical actor vocabulary |

## Philosophical / media-theoretical interpretation — bounded

The case supplies one narrow conceptual correction:

> **retention is not always an interval in which nothing relevant happens to the retained thing. The creation of a new nearby state can revise the physical conditions under which an older state remains recoverable.**

That does not make every write an act of forgetting, and it does not imply that the 2002–2014 authors were offering a theory of memory. It simply prevents the repository from treating `write` as affecting only the newly written object and `retention` as an isolated property of each cell.

The bounded physical lesson is relational: in dense NAND, the reliability of one retained value can depend on **what is later written nearby, in what order, to what threshold state, and how the later reader interprets the resulting distribution**.

## Functional analogies and stop conditions

### Case 52 — read disturb

Safe analogy:

> a successful operation aimed at one logical target can create a preservation cost for another retained state.

Stop condition:

- Case 52 uses repeated-read pass-through stress;
- Case 59 uses programming-induced capacitive coupling;
- read count and program sequence are different histories;
- Vpass tuning/read-count relocation and program-order/read-reference mitigation are different control problems.

### Case 53 — RowHammer

A second bounded analogy is possible: both RowHammer and NAND program interference expose **physical-neighbor coupling that breaks a purely logical account of operation scope**.

Stop condition:

- RowHammer is repeated DRAM activation causing disturbance/charge-loss risk in physical victim rows;
- NAND program interference is threshold shift caused by neighboring floating-gate programming;
- refresh-targeting and NAND read-reference/program-order policy are not historically or physically the same.

## Cross-case result

Case 59 adds the following relations:

```text
logical program target
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

The strongest new findings are:

- **successful aggressor programming ≠ unchanged neighboring retained state**;
- **logical page independence ≠ physical retention independence**;
- **same final programmed population ≠ necessarily the same interference history**;
- **program order can be a retention constraint**;
- **victim logical identity ≠ physically self-contained victim state**;
- **read-reference recovery ≠ physical-state restoration**;
- **neighbor state can become decoding side information**;
- **program interference ≠ retention-age leakage ≠ read disturb**.

## Related repositories

A current code search in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for NAND `program interference` returned no dedicated case. This file therefore keeps the retention-specific mechanism comparison here rather than duplicating an existing historical engineering account.

If `computing-archaeology` later develops a broader NAND scaling/cell-coupling history, this case should link to it and retain only the relational retention argument.

## Sources

1. Jae-Duk Lee, Sung-Hoi Hur, Jung-Dal Choi, **“Effects of Floating-Gate Interference on NAND Flash Memory Cell Operation,”** *IEEE Electron Device Letters* 23(5), May 2002, pp. 264–266, DOI `10.1109/55.998871`. Bibliographic record: <https://cir.nii.ac.jp/crid/1362544419688184448>.
2. Ki Tae Park, Myounggon Kang, Doogon Kim, Soonwook Hwang, Yeong Taek Lee, Changhyun Kim, Kinam Kim, **“A zeroing cell-to-cell interference page architecture with temporary LSB storing program scheme for sub-40nm MLC NAND flash memories and beyond,”** *2007 Symposium on VLSI Circuits*, pp. 188–189, DOI `10.1109/VLSIC.2007.4342709`. Institutional record: <https://pure.uos.ac.kr/en/publications/a-zeroing-cell-to-cell-interference-page-architecture-with-tempor-2/>.
3. Ki Tae Park et al., **“A zeroing cell-to-cell interference page architecture with temporary LSB storing and parallel MSB program scheme for MLC NAND flash memories,”** *IEEE Journal of Solid-State Circuits* 43(4), 2008, pp. 919–927, DOI `10.1109/JSSC.2008.917558`. Institutional record: <https://pure.uos.ac.kr/en/publications/a-zeroing-cell-to-cell-interference-page-architecture-with-tempor/>.
4. Yu Cai, Onur Mutlu, Erich F. Haratsch, Ken Mai, **“Program Interference in MLC NAND Flash Memory: Characterization, Modeling, and Mitigation,”** *31st IEEE International Conference on Computer Design (ICCD)*, October 2013, pp. 123–130, DOI `10.1109/ICCD.2013.6657034`. Author/institution PDF: <https://istc-cc.cmu.edu/publications/papers/2013/flash-programming-interference_iccd13.pdf>; abstract: <https://istc-cc.cmu.edu/publications/papers/2013/flash-programming-interference_iccd13_abs.shtml>.
5. Yu Cai, Gulay Yalcin, Onur Mutlu, Erich F. Haratsch, Osman Unsal, Adrian Cristal, Ken Mai, **“Neighbor-Cell Assisted Error Correction for MLC NAND Flash Memories,”** *ACM SIGMETRICS*, June 2014, pp. 491–504. Author PDF: <https://users.ece.cmu.edu/~omutlu/pub/neighbor-assisted-error-correction-in-flash_sigmetrics14.pdf>; institutional abstract: <https://istc-cc.cmu.edu/publications/papers/2014/neighbor-assisted-error-correction-in-flash_sigmetrics14_abs.shtml>.

## Remaining work

The bounded case is grounded, but several distinct regimes remain open:

- direct full-text inspection of the 2002 IEEE paper if an accessible archival copy becomes available;
- exact vendor datasheet/page-program-order constraints for named planar-NAND parts;
- modern charge-trap / 3D-NAND program-interference geometry;
- named-controller deployment of interference-aware reference-voltage or neighbor-assisted recovery;
- independent product fault validation;
- a stricter genealogy of `program disturb` versus `program interference` terminology.
