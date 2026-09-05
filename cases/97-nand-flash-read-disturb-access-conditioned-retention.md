# NAND Flash Read Disturb: Access-Conditioned Retention and Neighbor-State Maintenance

**Status:** `grounded`

## Scope

This case asks one bounded question:

> What changes when an operation presented as a logical NAND Flash **read** can cumulatively alter the physical state of *other, unread cells* in the same block, so that preservation depends on access history as well as elapsed time?

The evidence window is deliberately narrow:

- a Fujitsu NAND read-disturb patent with a 22 January 2002 priority date and 24 July 2003 U.S. publication;
- NASA/JPL NAND disturb testing published in March 2008;
- Cai et al.'s 2015 CMU/Seagate experimental characterization of read disturb in 2Y-nm MLC NAND Flash.

This is **not** a general NAND history, an SSD-controller history, a complete Flash-reliability taxonomy, or a claim about every SLC/MLC/TLC/QLC/3D-NAND generation. Case 04 already handles logical/physical mapping and reclamation; Case 36 handles retention-loss correct-and-refresh; Case 47 handles sanitization/hidden remnants. Broader Flash engineering history belongs in `tmzncty/computing-archaeology`; a search there found no existing NAND read-disturb case to reuse.

## Evidence labels and vocabulary

Historical/source vocabulary used here:

- `read disturb`;
- `pass-through voltage` / `Vpass`;
- `threshold voltage` / `Vth`;
- `weak programming` effect;
- `read disturb errors`;
- `ECC` / error-correction capability;
- `read count` / per-block read counter;
- rewriting / moving data to another block.

Project engineering vocabulary used here:

- **access-conditioned retention** — recoverability depends not only on wall-clock age but also on how much potentially disturbing access occurred in the relevant physical neighborhood;
- **disturbance budget** — the bounded amount of read-induced physical shift that can accumulate before ECC/read margin or logical-state boundaries are exceeded;
- **maintenance-state summary** — retained controller state such as a block read counter, tuned voltage, or worst-case-page estimate that supports future mitigation without preserving the complete read history.

These project terms are `E`; they are not attributed to historical actors as period vocabulary.

## Historical record

### H/P — Fujitsu documented NAND read disturb no later than a 2002-priority filing

Fujitsu's U.S. application **US20030137873A1, “Read disturb alleviated flash memory”** has a 22 January 2002 priority date, was filed on 22 October 2002, and was published on 24 July 2003.

Its description states that during NAND read, a high voltage is applied to non-selected word lines so that non-selected cells conduct. The same passage warns that this can place those cells in a light-programming condition: charge on a floating gate can increase, threshold voltage can rise, and an erased state can eventually be mistaken for a programmed state. The disclosed mitigation varies the voltage applied to non-selected word lines according to write-frequency classes, balancing read margin against read-disturb suppression.

This is a manufacturer-primary witness that the phenomenon and the term `read disturb` were already part of NAND engineering by this date. It is **not** used as proof that Fujitsu discovered or invented the phenomenon first.

### H/S — NASA/JPL treated disturb as a reliability qualification problem in 2008

Douglas Sheldon and Michael Freie's **JPL Publication 08-7, _Disturb Testing in Flash Memories_** (March 2008), produced under NASA's NEPP program, defines a disturb failure as a nearby programming or reading operation changing an initially expected stored state. The report says manufacturers acknowledge disturb failures and discusses system mitigation and qualification.

Its mechanism review describes read-disturb electron injection through tunnel oxide and notes that program/read operations can cause electrons to move in other cells within a block. It presents a rule-of-thumb limit of about one million reads per block for SLC and 100,000 for MLC, then says that if this threshold must be exceeded, data can be moved to another block and the original block erased, restarting the read-disturb exposure cycle.

These values are preserved only as **2008 report guidance**, not universal NAND limits.

### H/S — the same JPL study is an important negative result

The JPL experiment performed 50k, 100k, 500k, and 1M page reads on a single page during its read-disturb test, but the report states that **no read-disturb or program-disturb failures were detected** in the tested 2Gb devices.

This negative result is methodologically important. `Read disturb exists as a mechanism` does not imply `every tested device must fail after a fixed read count`. Device generation, process, wear, temperature, data pattern, voltage, and test conditions matter.

### H/P/S — 2015 open-literature experiments directly measured cumulative disturb in MLC NAND

Cai, Luo, Ghose, Haratsch, Mai, and Mutlu's 2015 SAFARI technical report / DSN paper, **“Read Disturb Errors in MLC NAND Flash Memory: Characterization, Mitigation, and Recovery,”** experimentally characterizes commercial 2Y-nm (20–24 nm) MLC NAND chips.

The paper reports that:

- a read to one row shifts threshold-voltage distributions of **unread cells in other rows of the same block**;
- the shift increases with the number of reads to neighboring pages;
- greater P/E-cycle wear increases susceptibility;
- pass-through voltage is a central mechanism variable;
- lowering `Vpass` reduces per-read disturbance, but reducing it too far introduces a different read-correctness problem.

The paper's physical explanation is especially useful for this repository. Cells in a NAND string are series-connected. To read one selected cell, the other cells in that string must be turned on with a pass-through voltage high enough to exceed their stored threshold voltages. Applying that voltage can induce tunneling and raise the threshold voltage of cells that were **not** logically selected for reading. Individual shifts are small, but repeated reads can accumulate them until a state boundary is crossed.

Thus a host-visible or page-level `read` can be logically nondestructive with respect to the returned value while still being physically non-neutral to neighboring retained state.

## Retained state

The payload state is encoded by NAND-cell threshold-voltage ranges. In the bounded 2015 MLC case, a cell's logical value depends on which threshold-voltage region the cell occupies.

But reliable future recovery can also depend on non-payload state:

1. block wear / P/E history;
2. cumulative read exposure or a conservative summary of it;
3. ECC margin / observed raw-error state;
4. controller-selected `Vpass` settings if adaptive mitigation is used;
5. mapping state if data are migrated to another block for refresh/rewrite;
6. policy thresholds that decide when further reads are no longer acceptable without maintenance.

The user payload can remain bit-for-bit logically unchanged while these surrounding relations become less favorable.

## Physical / logical substrate

The bounded physical substrate is a NAND block composed of word lines and series-connected strings/bit lines. One word line is selected for the requested page read; other cells in the same string must nevertheless be electrically biased so the selected cell's state can propagate to the sense amplifier.

This is the key geometry:

> **logical target scope ≠ physical stress scope**.

The logical interface names one page/cell state to read. The physical read path involves other cells whose values are not being requested.

## Retention mechanism

### Quiescent nonvolatility remains real

Nothing in this case says NAND requires DRAM-style periodic refresh merely to hold every bit. Charge/threshold state is nonvolatile over ordinary power-off intervals subject to the device's retention behavior.

### Read activity adds another loss mechanism

Time-dependent retention loss and read disturb are distinct error sources in the 2015 paper. A cell may lose margin because charge drifts with age, while another component of margin can be consumed because neighboring pages are repeatedly read.

Therefore:

**time-conditioned retention ≠ access-conditioned retention.**

### One read can protect the requested value while burdening another value

The selected page can be read successfully. Meanwhile, the pass-through operation on unselected cells can make a small threshold shift in those cells. Enough repetitions can move an unread cell toward or across a logical-state boundary.

Therefore:

**successful read return ≠ zero preservation cost elsewhere in the block.**

### ECC can absorb disturbance without making the disturbance absent

If accumulated raw bit errors remain within ECC capability, the controller can still return correct data. This creates a second boundary:

**correct logical output ≠ unchanged physical state.**

ECC postpones logical failure by supplying correction margin; it does not prove that read-induced threshold shifts did not occur.

## Addressing and access geometry

NAND exposes page/block organization, while an SSD may add an FTL above it. This case remains below host LBA semantics.

A page read electrically affects a wider NAND-string/block neighborhood than the page designated by the request. The critical retention relation is therefore not only `which address was read?` but also `which physical block/string shared the pass-through operation, how often, and under what voltage/wear/age conditions?`

This is a functional comparison with Case 70 magnetic-core half-select disturbance: both show that logical nonselection does not imply zero physical excitation. The mechanisms and genealogies are entirely different.

## Read semantics

`Nondestructive read` is too coarse if it is taken to mean that no stored state anywhere is affected.

For this bounded NAND regime:

- the requested page may remain logically unchanged;
- the read is not the deliberate program operation used to write the neighboring pages;
- nevertheless, unselected cells can receive a weak-programming effect from pass-through voltage;
- repeated operations can accumulate until later reads of those cells become erroneous.

A more precise statement is:

> **payload-nondestructive at the selected logical target ≠ physically non-disturbing for neighboring retained state.**

## Write / erase / migration semantics

Mitigation can eventually require an actual rewrite/migration. The 2008 JPL report recommends moving data to another block and erasing the original if read-count guidance must be exceeded. The 2015 paper's related-work discussion likewise records approaches based on per-block read counts and rewriting or relocating block/page contents.

Such maintenance is not the same as the host issuing a new application write. It is controller/filesystem work undertaken to renew physical margin while preserving the same higher-level logical value.

If relocation is used, Case 04's mapping relation becomes relevant: logical identity can remain stable while the physical embodiment changes.

## Time and workload

Read disturb creates a non-wall-clock timescale:

```text
retention exposure
    = elapsed physical aging
    + wear-dependent susceptibility
    + access-conditioned disturbance
    + voltage / operating-condition effects
```

This expression is an engineering heuristic, not a literal additive device model.

A cold block and a hot-read block of the same chronological age can therefore face different disturbance exposure. Conversely, JPL's negative result shows that a large read count does not map to one universal failure time across devices.

## Maintenance and labor

Read-disturb tolerance can require:

- controller accounting for per-block reads or a more compact exposure proxy;
- ECC measurement/correction;
- voltage calibration;
- background rewriting or migration;
- erase/reprogram cycles that consume endurance;
- block allocation and FTL remapping;
- validation/qualification under realistic workloads and wear states.

Thus nonvolatile storage can require maintenance because it is **used**, not only because it sits for a long time.

## A bounded controller-metadata example: Vpass Tuning

Cai et al. propose per-block dynamic `Vpass` tuning. Their design uses ECC margin to tolerate some additional read errors introduced by reducing `Vpass`, while reducing read-disturb stress. The paper states that its assumed implementation stores one byte for each block's tuned `Vpass` setting and one byte for the predicted worst-case page; for the paper's assumed 512GB SSD / 65,536 blocks, this is 128KB.

This is a research proposal/evaluation, not evidence that commercial SSDs universally used exactly this metadata design.

For retention analysis it supplies a useful principle:

> **maintenance metadata can be tiny relative to payload yet still govern whether future reads remain safe.**

The metadata need not be a complete read log. A controller can retain a bounded summary—counter, tuned setting, error margin, worst-case page—and still make future preservation decisions.

## Failure / forgetting modes

### Disturbance accumulates below the logical interface

A workload can repeatedly read one hot page while changing the physical margin of other pages that the host did not access.

### ECC margin is exhausted

Correctable raw errors can become uncorrectable if disturbance and other noise sources together outrun the ECC budget.

### Mitigation itself has a tradeoff

Lower `Vpass` reduces disturbance but can make unread cells fail to pass the selected value correctly; the 2015 work explicitly treats this as a balance rather than a free improvement.

### Refresh/rewrite consumes another finite resource

Moving/reprogramming data renews disturbance margin but consumes program/erase endurance and background bandwidth. Preservation work can therefore exchange one reliability budget for another.

### Lost maintenance metadata can remove protection before payload disappears

If a controller policy depends on per-block exposure, ECC state, tuned voltage, or mapping state, loss/corruption of that control relation can make future reads less safely managed even though NAND payload cells still physically contain charge.

This last point is an engineering reconstruction; the bounded sources do not establish one universal commercial metadata format.

## Engineering reconstruction

The bounded mechanism can be summarized as:

1. a logical read selects one NAND row/page;
2. series-connected unselected cells must be biased with `Vpass` so the selected state can reach the sense amplifier;
3. that bias can produce a small weak-programming / tunneling effect in unselected cells;
4. repeated reads accumulate threshold-voltage shift;
5. wear, retention age, and voltage conditions change how much margin remains;
6. ECC can hide some physical disturbance from the logical interface;
7. the controller may reduce `Vpass`, count reads, rewrite/migrate data, or otherwise renew margin before errors become uncorrectable.

The retained object therefore depends on a relation among **stored charge, neighborhood geometry, access history, error margin, and maintenance policy**.

## Functional analogies

### Case 36 — NAND correct-and-refresh

`A/E`: Case 36 treats time/retention-error accumulation and ECC-triggered refresh. Case 97 treats read-induced disturbance accumulation. Both can end in rewrite/remap, but the trigger regimes differ.

**retention refresh ≠ read-disturb refresh.**

### Case 04 — mapped Flash

`A/E`: when read-disturb mitigation moves valid data to a fresh block, the logical object can retain identity while the serving physical block changes. Case 04 supplies the mapping/currentness relation; Case 97 supplies one reason that relocation may become maintenance rather than host-requested mutation.

### Case 53 — DRAM RowHammer

`A`: both cases show access to one logical location disturbing neighboring physical state, and both make workload part of retention. They are not the same mechanism: RowHammer involves repeated DRAM row activations and charge leakage/coupling; NAND read disturb involves read/pass-through bias and threshold-voltage shift in Flash cells.

**shared functional pattern ≠ shared device physics or historical lineage.**

### Case 70 — magnetic-core half-select

`A`: both expose a target-scope / physical-effect-scope mismatch. Core half-select is subthreshold magnetic excitation in coincident-current selection; NAND read disturb is an electrical stress of series-connected unselected Flash cells. No genealogy is claimed.

## Prior art and genealogy boundary

The 2002-priority Fujitsu patent demonstrates that read disturb was an explicit NAND engineering problem by that date. It does not prove first observation or first invention.

The 2015 paper itself describes read disturb as already well known, while claiming the first detailed open-literature experimental characterization on the tested state-of-the-art MLC chips. This repository therefore preserves the narrower claim:

> Fujitsu provides an early manufacturer-primary witness; JPL provides an independent 2008 qualification/test witness including a negative result; Cai et al. provide a 2015 open experimental characterization and proposed mitigation/recovery techniques.

The repository does **not** claim that 2015 discovered read disturb, that Fujitsu invented all mitigation, or that later SSD read-reclaim policies descend directly from this one patent.

## Philosophical / media-theoretical interpretation

`I` — This case weakens an intuitive opposition between `reading` and `writing`. At the logical interface they remain distinct operations, but the physical read path can still spend a small portion of another cell's future stability margin.

`I` — It also makes retention workload-relational. A state does not merely wait through homogeneous chronological time; its future recoverability can depend on what neighboring addresses were asked to do while it remained logically untouched.

These are project interpretations. They are not historical claims that NAND engineers used philosophical `retention` vocabulary.

## Counterexamples and limits

This case does **not** establish:

- that every NAND device fails after a fixed number of reads;
- that the 2008 JPL rule-of-thumb read counts are universal limits;
- that JPL observed read-disturb failures in its tested 2Gb devices—it explicitly did not;
- that a selected-page NAND read normally destroys the selected payload;
- that read disturb and ordinary retention loss are the same error source;
- that read disturb and RowHammer are the same mechanism;
- that ECC prevents physical threshold-voltage movement;
- that rewrite/migration is free of endurance or bandwidth cost;
- that Cai et al.'s `Vpass` metadata layout describes a commercial SSD controller;
- that Fujitsu 2002 establishes invention priority for read disturb;
- that a NAND block's complete read history must be retained forever.

## Sources

### Primary / period manufacturer evidence

- Fujitsu Limited, **“Read disturb alleviated flash memory,”** US20030137873A1 / US6707714B2, priority 22 January 2002, filed 22 October 2002, application published 24 July 2003: <https://patents.google.com/patent/US20030137873A1/en>.

### Institutional test evidence

- Douglas Sheldon and Michael Freie, **_Disturb Testing in Flash Memories_**, Jet Propulsion Laboratory, California Institute of Technology, JPL Publication 08-7, March 2008; NASA NTRS record: <https://ntrs.nasa.gov/citations/20210001742>; NEPP PDF: <https://nepp.nasa.gov/files/13582/07-100%20Sheldon_JPL%20Distrub%20Testing%20in%20Flash%20Mem.pdf>.

### Experimental scholarly evidence

- Yu Cai, Yixin Luo, Saugata Ghose, Erich F. Haratsch, Ken Mai, Onur Mutlu, **“Read Disturb Errors in MLC NAND Flash Memory: Characterization, Mitigation, and Recovery,”** SAFARI Technical Report No. 2015-007, May 2015: <https://research.ece.cmu.edu/safari/tr/tr-2015-007.pdf>.
- Conference version, 45th Annual IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 2015, DOI `10.1109/DSN.2015.49`.

## Related repositories

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — broader NAND/Flash process, controller, interface, reliability, and technology-history work belongs there. A pre-write search found no existing NAND read-disturb case to reuse.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — useful for keeping `access-conditioned retention` as project reconstruction rather than projecting that phrase onto 2002/2008/2015 actors.

## Status

`grounded` — the central mechanism has manufacturer-primary, independent institutional, and experimental scholarly support; the negative JPL result is retained as a deliberate counterexample; invention priority and universal device thresholds remain explicitly unclaimed.
