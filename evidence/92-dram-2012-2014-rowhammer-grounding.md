# Grounding record — DRAM RowHammer, 2012–2014

## Purpose

This record grounds [`../cases/92-dram-rowhammer-access-induced-retention-failure.md`](../cases/92-dram-rowhammer-access-induced-retention-failure.md).

The bounded question is not `what is the full history of RowHammer?` It is:

> **Can ordinary DRAM refresh remain on schedule while access activity in one physical row accelerates charge loss in another row enough to create a new retention obligation, and what primary evidence existed by 2012–2014 for activity-conditioned / targeted refresh?**

The source set deliberately combines:

1. a peer-reviewed experimental paper on real commodity modules;
2. an earlier-filed industry patent describing row-hammer detection and targeted victim-row refresh;
3. the paper authors' released experimental/software artifact as a reproducibility pointer, not as independent evidence.

The broader disturbance-error genealogy, later security exploits, TRR, DDR4/DDR5/RFM, and vendor implementation history are outside this record.

---

## Source A — Kim et al., ISCA 2014

**Yoongu Kim, Ross Daly, Jeremie Kim, Chris Fallin, Ji Hye Lee, Donghyuk Lee, Chris Wilkerson, Konrad Lai, Onur Mutlu, “Flipping Bits in Memory Without Accessing Them: An Experimental Study of DRAM Disturbance Errors,” Proceedings of the 41st International Symposium on Computer Architecture (ISCA), June 2014, pp. 361–372. DOI: `10.1109/ISCA.2014.6853210`.**

Institutional landing page:

- <https://istc-cc.cmu.edu/publications/papers/2014/kim-isca14_abs.shtml>

Full paper:

- <https://istc-cc.cmu.edu/publications/papers/2014/kim-isca14.pdf>

### Evidence role

`P/S` — original peer-reviewed experimental research and the main empirical source for this case.

### Exact anchors used

#### Abstract and introduction — measured prevalence and access-induced corruption

- printed p. 1 / PDF p. 1, Abstract: repeated access/activation to one row can corrupt data in nearby rows; 110 of 129 tested modules exhibited disturbance errors; as few as 139K accesses induced an error in the measured sample;
- printed p. 1, Introduction: repeated wordline toggling is associated with disturbance effects and accelerated charge leakage in nearby rows;
- footnote 1: the authors state that industry was aware of the RowHammer problem by at least 2012 and cite Intel patent applications; they also distinguish their paper's review/publication chronology from those applications.

Use this to support:

- `repeated row activation can disturb non-target rows`;
- `the 2014 result is sample-bounded, not a universal DRAM claim`;
- `the paper is not the origin of all DRAM disturbance engineering`.

Do **not** use it to claim a fully proven microscopic coupling mechanism for every device. The paper characterizes and reasons about coupling pathways, but several fine-grained physical explanations remain hypotheses/observations rather than transistor-level proof.

#### §2.2–§2.4 — ordinary access and refresh baseline

- printed pp. 2–3: DRAM cell charge is sensed through the row buffer and restored after row activation;
- §2.4, printed p. 3: cell charge is nonpersistent because of leakage; it must be restored before retention time expires;
- §2.4: the DDR3 baseline discussed by the paper uses a 64 ms retention / refresh window and enough refresh operations to cover all rows in that window;
- §2.4: opening a row and refreshing it are circuit-level restoration operations for the row's cells.

Use this to support:

- `ordinary refresh = deadline-driven restoration`;
- repeated aggressor activation can repeatedly restore the aggressor itself;
- RowHammer is not simply a case where the normal refresh schedule stopped running.

#### §3 and §6 — disturbance can outrun ordinary refresh

- printed p. 3 onward: repeated wordline activation accelerates leakage in nearby victim cells;
- §6.2, Fig. 6 / surrounding text: disturbance errors depend jointly on refresh interval and activation interval; the paper defines a threshold activation count `Nth` within a 64 ms refresh interval for its tested modules;
- reported `Nth` values include 139K, 155K, and 284K in the three modules highlighted there.

Use this to support:

- `ordinary refresh compliance ≠ disturbance immunity`;
- `safe retention interval can become workload-conditioned`;
- `activity threshold is bounded state sufficient for some mitigation designs`.

#### §6.3 — aggressor/victim and ECC boundary

- printed p. 8: the paper names repeatedly opened rows `aggressor rows` and the disturbed cells `victim cells`;
- Table 5 / surrounding text: some 64-bit words contain multiple victims;
- SECDED cannot correct measured double-bit cases and is not failsafe against the multi-bit disturbance patterns discussed.

Use this to support:

- `ECC presence ≠ unconditional recoverability`;
- `one access target can create nonlocal retention consequences`.

Do **not** generalize this to every ECC scheme or every later DDR generation.

#### §7 — victim cells are not merely ordinary weak cells

- printed p. 10, `Victim Cells ≠ Weak Cells`: the authors identify ordinary weak cells with a long no-access/no-refresh test and find only a small overlap with disturbance victim cells in the three characterized modules;
- they conclude that the coupling pathway responsible for disturbance errors may be independent of the process variation responsible for weak cells.

Use this to block:

- `RowHammer victim = shortest ordinary retention-time cell`;
- `RowHammer is merely ordinary passive leakage sped up uniformly`.

The conclusion is sample-bounded and phrased cautiously because the paper says the pathways *may* be independent.

#### §8.1 — global refresh, counters, and cost

- printed pp. 10–11: sufficiently short refresh intervals can eliminate disturbance errors under the tested conditions, but global frequent refresh increases performance/energy cost;
- the paper gives an 8.2 ms example with estimated refresh-time overhead of 11.0–35.0%, compared with the cited baseline 1.4–4.5%;
- `Identify “hot” rows and refresh neighbors` discusses per-row counters / approximate structures and the storage/search cost of retaining hot-row activity state.

Use this to support:

- `global faster refresh ≠ targeted refresh`;
- tracked mitigation can retain bounded access-frequency state rather than complete access history.

#### §8.2 — PARA and physical adjacency

- printed p. 11: PARA (`probabilistic adjacent row activation`) probabilistically opens/refreshes an adjacent row whenever a row is closed;
- the paper explicitly calls PARA `stateless` because it does not require per-row activation counters or stored aggressor/victim address tables;
- the same section states that selective refresh requires physical-adjacency knowledge and that logical-to-physical mapping / remapping complicates the relation.

Use this to support:

- `activity-conditioned maintenance need not imply retained per-row counters`;
- `stateless PARA ≠ no maintenance policy`;
- `logical row adjacency ≠ guaranteed physical adjacency`;
- topology/mapping knowledge can participate in retention maintenance.

Do **not** claim PARA was a JEDEC feature or a deployed industry mechanism in 2014 merely because the paper proposed it.

---

## Source B — Intel `Row hammer refresh command` patent family

**Kuljit S. Bains, John B. Halbert, Christopher P. Mozak, Theodore Z. Schoenborn, Zvika Greenfield, “Row hammer refresh command,” U.S. application 13/539,415, filed 30 June 2012; application publication US20140006703A1, 2 January 2014; later patent US9236110B2. Original assignee: Intel Corporation.**

Stable public record:

- <https://patents.google.com/patent/US9236110B2/en>

### Evidence role

`H/P` — contemporary industry patent witness. It establishes that `row hammer event/condition`, thresholded repeated access, victim rows, physical adjacency, and targeted refresh were part of an Intel engineering design filed in 2012.

A patent documents a proposed/claimed design. It does **not** prove that every embodiment was built, standardized, shipped, or historically first.

### Exact anchors used

#### Priority / filing chronology

The public patent record gives:

- U.S. application / priority date: `2012-06-30`;
- application publication `US20140006703A1`: `2014-01-02`;
- later granted patent `US9236110B2`: `2016-01-12`.

Use this only for the bounded statement:

> by 2012, Intel engineers were filing row-hammer-specific targeted-refresh designs.

Do not infer origin priority beyond that.

#### Detailed description — thresholded access and victim refresh

The detailed description says, in substance:

- repeated access to a specific row within a time window is a `row hammer event` / `row hammer condition`;
- a physically adjacent row can be a `victim row` and can experience data corruption;
- a monitor/controller can identify when the specific row exceeds a threshold number of accesses;
- the controller can cause targeted refresh of victim row(s).

Use this to support:

- `maintenance can be triggered by retained/derived activity state, not elapsed time alone`;
- `a victim row can require an additional refresh despite the ordinary refresh regime`.

#### Logical / physical topology boundary

The patent notes that physically adjacent rows may be logically labeled differently across manufacturers, that the DRAM device knows its internal mapping, and that a controller need not itself know the exact victim-row address if it can identify the hammered row to the device.

Use this to support:

- `logical address relation ≠ physical interference topology`;
- topology resolution can be delegated across the controller/device boundary.

#### Fig. 6 description — threshold state and refresh-period relation

The described flow receives a row-hammer indication from a monitor that tracks whether a row has exceeded a threshold number of accesses within a time period. The text relates that period to the interval between refreshes and then performs targeted refresh of the victim row/region.

Use this as a clean period witness for:

```text
access activity
    -> bounded detection/threshold state
    -> targeted maintenance action
```

Do **not** treat the patent's phrase that refreshing the victim `cures` the row-hammer condition as evidence that a refresh reconstructs user data after an already-completed bit flip. In context, the mechanism is a preventative/alleviating refresh response to the detected condition.

---

## Source C — CMU-SAFARI RowHammer repository

Repository:

- <https://github.com/CMU-SAFARI/rowhammer>

### Evidence role

`P` as a released research artifact / navigation source, **not an independent replication** of Source A.

The repository provides the RowHammer test/software context and points back to the 2014 paper. It is useful for reproducibility archaeology if a later experiment slice is created, but the central historical/mechanism claims in Case 92 rest on Sources A and B rather than counting the paper's own code as a second independent confirmation.

---

## Claim ledger

| Claim | Label | Source basis | Boundary |
| --- | --- | --- | --- |
| DRAM cell charge requires recurring restoration before ordinary retention expires | `H/P` | Kim et al. §2.4 | baseline as described for DDR3-era systems in the paper; deeper history remains Case 03 |
| repeated row activation can corrupt nearby rows in the tested commodity modules | `H/P` | Kim et al. Abstract, §§3–7 | sample-bounded; not every DRAM generation/device |
| repeated wordline toggling is associated with accelerated nearby-cell charge leakage | `H/P` | Kim et al. Abstract / mechanism discussion | do not overclaim a fully resolved microscopic pathway for all devices |
| ordinary refresh compliance can coexist with disturbance failure | `E` | combination of §2.4 ordinary schedule and disturbance measurements within the refresh interval | project reconstruction, not period terminology |
| aggressor activation can restore aggressor charge while threatening victims | `E` | row-open restore semantics + aggressor/victim measurements | relation-level reconstruction |
| victim cells are not simply the shortest-retention weak cells | `H/P` | Kim et al. §7 | explicitly bounded to the characterized modules |
| SECDED is not failsafe against the measured multi-bit disturbance patterns | `H/P` | Kim et al. §6.3 | do not generalize to stronger ECC schemes |
| globally shorter refresh can suppress disturbance but with substantial overhead | `H/P` | Kim et al. §8.1 | exact overheads are paper/model/sample-specific |
| hot-row tracking can retain counters/approximate activity state | `H/P/E` | Kim et al. §8.1; Intel patent | not proof every implementation uses counters |
| PARA couples neighbor refresh to row-close events without per-row history tables | `H/P` | Kim et al. §8.2 | proposal/evaluation, not standard/deployment proof |
| targeted refresh can depend on physical adjacency mapping hidden by logical row numbering | `H/P/E` | Kim et al. §8.2; Intel patent | topology relation, not a claim all mappings are secret/opaque |
| Intel filed a row-hammer targeted-refresh patent family in 2012 | `H/P` | US13/539,415 public record | prior-art witness only; no invention-priority claim |
| retention interval can be workload/topology-conditioned under interference | `E` | synthesis of ordinary refresh + measured disturbance | project term |
| refresh of a still-correct victim ≠ recovery of a value after corruption | `E/X` | mechanism boundary | source does not establish refresh-alone post-flip correction |
| RowHammer ≠ magnetic-core half-select or NAND read disturb | `A/X` | cross-case comparison | functional analogy only; no genealogy |

---

## Rejected / unsupported claims

### X — `the 2014 ISCA paper discovered DRAM disturbance errors`

Rejected. The paper itself discusses older DRAM disturbance awareness and specifically states that industry was aware of the RowHammer problem by at least 2012.

### X — `Intel invented RowHammer in 2012`

Rejected. The patent is a dated industry witness for a row-hammer-specific mitigation design, not proof of first discovery or first invention of the broader phenomenon.

### X — `every modern DRAM device is vulnerable at 139K activations`

Rejected. `139K` is the low end observed in the 2014 characterization; thresholds vary by module/process and later devices/mitigations are outside this case.

### X — `RowHammer victims are just ordinary weak retention cells`

Rejected by the paper's bounded victim/weak-cell comparison.

### X — `ordinary 64 ms refresh guarantees integrity under arbitrary access patterns`

Rejected as an end-to-end inference. The paper demonstrates disturbance errors within the ordinary refresh regime and studies shorter intervals as a mitigation.

### X — `logical row N±1 necessarily means physical victim row`

Rejected. Both the paper and patent treat logical/physical mapping as a problem for targeted refresh.

### X — `PARA stores aggressor counters`

Rejected. The paper's central claimed advantage is precisely that PARA avoids the per-row counter/address structures discussed for hot-row detection.

### X — `PARA provides an absolute guarantee`

Rejected. The paper explicitly treats it as probabilistic and analyzes an extremely low rather than mathematically zero failure probability.

### X — `targeted refresh after corruption reconstructs the original payload`

Unsupported. The sources ground targeted refresh as prevention/alleviation of a disturbance condition; post-corruption value reconstruction is a separate ECC/redundancy problem.

### X — `RowHammer mitigation proves secure memory isolation`

Rejected. This case establishes one physical-disturbance relation and selected mitigations, not a complete security proof against all disturbance patterns or later bypasses.

---

## Prior-art / novelty boundary

The evidence changes the repository's novelty boundary in a useful way:

- Case 03 already grounds DRAM as **deadline-driven restoration** under ordinary leakage;
- Case 92 shows that by 2012–2014 DRAM engineers/researchers were also dealing with **activity-conditioned disturbance**, where another row's access history changes the urgency of victim restoration;
- Intel's 2012 filing blocks any claim that the 2014 paper invented the row-hammer engineering problem;
- Kim et al. themselves block an even broader origin claim by discussing earlier disturbance-error history.

What `technical-retention` can contribute is therefore not `RowHammer exists`. The retention-specific contribution is the comparison:

> **retention deadlines are not always functions of the bearer and elapsed time alone; under physical coupling, another component's workload can modify the maintenance deadline, and preserving logical isolation can require topology-aware restoration policy.**

That sentence is an **engineering synthesis**, not historical vocabulary.

---

## Cross-case boundary notes

### Case 03 — DRAM scheduled restoration

Reuse Case 03 for the substrate/ordinary-refresh history. Case 92 should not duplicate Dennard, commercial DRAM chronology, or generic refresh explanation beyond what is necessary to expose the disturbance counterexample.

### Case 70 — magnetic-core half-select disturbance

Functional analogy only: logical nonselection can coexist with physical partial stress. Core coercivity/selection currents and DRAM wordline/cell coupling are different mechanisms and histories.

### NAND read disturb cases

Functional analogy only: repeated read/access operations can impose non-target stress. Do not infer a shared genealogy or shared physical model from the similar relational shape.

### Case 83 — HDFS scanner

Contrast only: scanner work detects latent integrity problems in persistent blocks, whereas RowHammer targeted refresh is restoration intended to prevent volatile charge from crossing a corruption threshold. Verification ≠ restoration.

---

## Related-repository check

Searched `tmzncty/computing-archaeology` for `RowHammer` and `DRAM disturbance` before writing this slice; no dedicated existing case was found. The division of labor is therefore:

- **here:** retention-specific relation among ordinary refresh, access-induced leakage, physical adjacency, bounded activity state, and targeted restoration;
- **future `computing-archaeology`:** full disturbance-error engineering history, process/device evolution, JEDEC/vendor mitigation genealogy, and named-platform implementation archaeology.

If the latter appears, this record should link/reuse it rather than duplicate it.

---

## Evidence-status conclusion

**Status: grounded.**

The central case no longer depends on a single type of evidence:

- the 2014 paper supplies direct experimental characterization on real commodity modules plus mechanism/mitigation analysis;
- the 2012-filed Intel patent supplies an earlier industry-primary witness for row-hammer threshold detection, physical victim rows, and targeted refresh;
- both independently make logical-vs-physical adjacency relevant to the maintenance problem.

The case remains deliberately narrow. Later TRR/RFM implementations, exploit history, and a complete pre-2012 disturbance genealogy are not promotion blockers because they answer different historical questions.
