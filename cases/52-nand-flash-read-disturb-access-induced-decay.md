# NAND Flash Read Disturb: Access-Induced Decay, Vpass Mitigation, and Recovery

## Status

**`grounded`** — bounded to NAND read disturb from a Fujitsu 2002-priority manufacturer filing through Yu Cai et al.'s 2015 DSN experimental characterization. NASA/JPL's March 2008 qualification study is retained as an independent institutional witness, including its explicit negative result; a 2009-priority Texas Memory Systems patent and a 2013 APSys paper constrain controller/FTL prior-art claims. The case separates measured device behavior, engineering reconstruction, and proposed mitigation/recovery, and does not claim commercial deployment of the 2015 mechanisms.

Grounding record: [`../evidence/52-cai-2009-2015-nand-read-disturb-grounding.md`](../evidence/52-cai-2009-2015-nand-read-disturb-grounding.md).

## Scope

This case asks a narrow question left open by Cases 02, 04, and 36:

> What changes when an operation intended to *read* one NAND page can cumulatively alter the threshold-voltage state of other, unread cells in the same physical block, so access itself becomes a source of future retention error?

The bounded mechanism is **read disturb** in NAND Flash. In the cited sources, reading a selected page requires a sufficiently high pass-through voltage (`Vpass`) on unselected cells in the NAND string so that the selected cell's conduction state can reach the sense path. Repeated exposure can weakly program those unselected cells, shifting their threshold voltages until some cross a logical-state boundary.

This is **not**:

- a general history of NAND reliability;
- a claim that every NAND generation has the same read-disturb threshold or direction of error;
- evidence that ordinary reads immediately destroy the selected page;
- evidence that the 2015 `Vpass Tuning` or `Read Disturb Recovery (RDR)` proposals were shipped in a named commercial controller;
- evidence that read disturb and retention loss are the same physical mechanism;
- evidence that NAND read disturb is historically or physically identical to magnetic-core destructive read;
- a complete history of modern 3D-NAND read reclaim, read retry, LDPC, or controller firmware.

## Historical vocabulary and record

### Earlier manufacturer-primary witness — Fujitsu, 2002 priority / 2003 publication

Fujitsu's **US20030137873A1, “Read disturb alleviated flash memory,”** has a 22 January 2002 priority date and a 24 July 2003 U.S. publication date. The original assignee is Fujitsu Ltd. The application explicitly concerns NAND-type Flash and uses `read disturb` as period vocabulary. Its background explains that a high voltage is applied to non-selected word lines during read so those cells conduct; this can put non-selected cells into a light-programming condition, add floating-gate charge, raise threshold voltage, and eventually compromise the erased/programmed distinction. The disclosed design varies the non-selected-word-line voltage and makes a tradeoff explicit: lowering it can suppress disturb, while lowering it too far can make some cells fail to conduct correctly during read.

Primary source: <https://patents.google.com/patent/US20030137873A1/en>.

This is an earlier manufacturer-primary witness than the 2009-priority controller patent already used in this case. It is **not** evidence that Fujitsu first discovered read disturb or invented every later mitigation technique.

### Independent qualification witness — NASA/JPL, March 2008

Douglas Sheldon and Michael Freie's NASA/JPL **_Disturb Testing in Flash Memories_**, JPL Publication 08-7, treats read disturb as a NAND reliability and qualification problem. The report says manufacturers acknowledged disturb failures and supplied guidance, describes read disturb as a neighboring-cell/state problem within a block, and records a contemporary rule of thumb of roughly one million READ cycles per block for SLC and 100,000 for MLC. If that guidance had to be exceeded, it recommends moving data to another block and erasing the original block, restarting that block's read-disturb exposure cycle.

Institutional source: <https://nepp.nasa.gov/files/13582/07-100%20Sheldon_JPL%20Distrub%20Testing%20in%20Flash%20Mem.pdf>.

The same report supplies a valuable **negative result**. Program 8 performed 50k, 100k, 500k, and 1M page-read operations on a single page, yet the report states that no program-disturb or read-disturb failures were detected in the tested devices. Therefore the report's read-count figures are historical guidance, not universal physical thresholds.

### Recognized `Read Disturb` before 2015

US7818525B1, filed by Texas Memory Systems in 2009 and published in 2010, explicitly uses the term **`Read Disturb` errors**. It describes NAND reads as applying an elevated voltage to unread cells, repeated exposure as allowing charge to accumulate, and sufficiently shifted cells as becoming weakly programmed. The patent also describes then-existing mitigation by maintaining a block read count and moving data after a threshold, while proposing a more incremental page-migration strategy once the threshold is reached.

This is important for chronology: Cai et al. 2015 did **not** originate either the phenomenon or the generic idea of read-count-triggered relocation.

A 2013 APSys paper by Keonsoo Ha, Jaeyong Jeong, and Jihong Kim likewise treats read-disturb management as an existing FTL problem. Its abstract describes errors in a page after many reads to neighboring pages in the same block and proposes redistributing hot read traffic to reduce migration overhead.

### 2015 commercial-chip characterization

Yu Cai, Yixin Luo, Saugata Ghose, Erich F. Haratsch, Ken Mai, and Onur Mutlu, **“Read Disturb Errors in MLC NAND Flash Memory: Characterization, Mitigation, and Recovery,”** DSN 2015, experimentally characterizes read disturb on commercially available 2Y-nm (20–24 nm) MLC NAND chips.

The paper's historical/technical vocabulary includes:

- `read disturb` / `read disturb errors`;
- `read disturb count`;
- `pass-through voltage (Vpass)`;
- `threshold voltage (Vth)`;
- `raw bit error rate (RBER)`;
- `program/erase (P/E) cycles`;
- `retention age`;
- `error correction capability` / ECC margin;
- `Vpass Tuning`;
- `Read Disturb Recovery (RDR)`;
- `disturb-prone` and `disturb-resistant` cells.

The paper reports that read-disturb-induced threshold shifts and RBER increase with cumulative reads to neighboring pages, and that susceptibility grows with P/E wear. It also treats retention errors as a separate error source that can coexist with read disturb.

## Retained state and constitutive control state

The bounded regime contains several separable states:

1. **physical cell state** — stored charge / threshold-voltage distributions encoding MLC values;
2. **selected-page logical payload** — the value requested by the current read;
3. **unselected-neighbor physical state** — cells in other pages that must be electrically passed through during that read;
4. **raw error population** — errors visible before ECC reconstruction;
5. **ECC correction margin** — remaining ability to mask/correct raw errors before a page becomes uncorrectable;
6. **access-stress history** — cumulative reads to a physical block, represented in some prior mitigation schemes by a per-block read counter;
7. **wear state** — P/E-cycle history that changes susceptibility to later disturb;
8. **mapping/currentness state** — logical-to-physical relations when mitigation relocates current data;
9. **read-voltage policy state** — the selected `Vpass` / error-margin relation in the 2015 tuning proposal.

`access-stress history` and `read-voltage policy state` are project analytical descriptions. The cited sources use more concrete terms such as block read count and `Vpass`.

## Engineering reconstruction

### A successful read can spend future retention margin elsewhere

The central counterexample is that a NAND read is not materially confined to the bits whose logical value is returned. To read one cell in a series NAND string, unselected cells must be driven so they remain conductive. The elevated pass-through voltage can induce tunneling into those unread cells. One exposure is weak relative to programming, but repeated reads accumulate.

Therefore:

> **successful selected-page read ≠ zero material change to neighboring retained state**.

And more narrowly:

> **logical nondestructiveness of the requested read ≠ zero future-retention cost to the surrounding physical block**.

This does not mean every read immediately changes a decoded neighbor value. The point is cumulative margin consumption: the current request can succeed while making a future request more error-prone.

### Recognized mechanism ≠ universal read-count failure threshold

The NASA/JPL 2008 result prevents an easy but incorrect upgrade from `read disturb exists` to `a fixed read count predicts failure`. The report used large read-count sequences and contemporary migration/erase guidance, yet its own tested devices did not reproduce a disturb failure.

Therefore:

> **read-disturb mechanism ≠ universal fixed read-count failure threshold**.

A practical threshold is qualified by device generation, process, wear, data pattern, temperature, voltage, ECC margin, and test/workload conditions.

### Read count can become a maintenance clock

Case 36 uses elapsed retention time and wear as inputs to proactive Flash Correct-and-Refresh. Read disturb exposes a different trigger class. A physically hot block can accumulate disturbance because of **how often it is read**, even if user data is not being rewritten and little wall-clock time has passed.

The 2009-priority patent explicitly maintains a per-block read count since erase and uses threshold crossing to trigger migration behavior. Cai et al. likewise analyze cumulative read-disturb count and note earlier controller proposals that rewrite or move blocks/pages after read-count thresholds.

Therefore:

> **access count can be a retention-maintenance clock**.

And:

> **read hotness ≠ write wear, while read hotness can consume future error margin**.

P/E wear remains a separate axis: the 2015 measurements show more-worn blocks become more susceptible to each read disturb.

### Read disturb is not retention-age leakage

Cai et al. separate `read disturb` from `retention` as distinct error sources. Read disturb generally shifts susceptible cell threshold voltages upward through repeated pass-through stress; retention processes can produce different threshold-voltage drift. The same page's total raw errors may include both.

Therefore:

> **read-disturb accumulation ≠ retention-age leakage**.

The two mechanisms can interact in one ECC budget without becoming the same failure process.

This boundary matters directly to Case 36: FCR can renew a block and thereby reset accumulated effects from more than one error source, but the fact that the same rewrite helps both does not collapse their causes or triggers.

### ECC can preserve the answer while the physical margin is deteriorating

As with Case 36, raw errors can remain below the ECC correction capability. A host-visible read may still return the intended value even though physical errors have accumulated.

Therefore:

> **ECC-correctable successful read ≠ undisturbed physical state**.

and:

> **current payload recoverability ≠ unchanged future correction margin**.

The maintenance problem begins before interface-visible data loss.

### Lower pass-through voltage trades one error mechanism against another

Cai et al. show that reducing `Vpass` can reduce read-disturb-induced threshold shifts. But `Vpass` exists because unselected cells must conduct strongly enough to pass the selected cell's value through the NAND string. Lowering it too far can create additional read errors.

Their proposed `Vpass Tuning` therefore searches for a lower per-block value while remaining inside an ECC-qualified correctness condition.

Thus:

> **lower electrical stress ≠ free reliability improvement**.

and:

> **read-disturb mitigation ≠ elimination of read-path margin requirements**.

The reported 21% average endurance improvement is an evaluation result from empirical characterization plus workload-trace simulation, not a measured field-lifetime result from a shipped SSD.

### Compact maintenance summaries can govern much larger payloads

Cai et al.'s proposed `Vpass Tuning` implementation gives one bounded research example: one byte per block for the tuned `Vpass` setting and one byte for the predicted worst-case page. For the paper's assumed 512GB / 65,536-block configuration, that is 128KB total metadata.

This is a proposal/evaluation cost estimate, not a universal commercial SSD format. Its narrower methodological result is:

> **small maintenance metadata ≠ small retention significance**.

A controller can retain a counter, tuned setting, error-margin estimate, or worst-case-page summary without retaining a complete read history, yet that small control state can still govern when future reads remain safe.

### Recovery can use additional disturbance as diagnostic evidence

The 2015 RDR proposal deliberately reverses the ordinary instinct to stop disturbing a failed block. After an ECC-uncorrectable read, RDR records susceptible cells' threshold voltages, intentionally induces additional read disturbs, measures how strongly those cells shift, classifies them as disturb-prone or disturb-resistant, probabilistically estimates their earlier logical state, and then retries ECC.

Therefore:

> **additional controlled disturbance can become recovery evidence**.

This is a particularly strong distinction between **state preservation** and **state inference**. RDR does not physically rewind threshold voltages to their earlier positions. It uses the response of the already-degraded medium to infer which logical values are more likely to have preceded the observed disturbance.

Hence:

> **inferred logical recovery ≠ restoration of the prior physical threshold distribution**.

The paper's RDR result is experimental/proposed recovery, not commercial deployment.

### Mitigation can preserve logical identity by replacing embodiment

Read-count-triggered rewrite/migration and read-disturb-aware FTL techniques can move valid payload to another physical block and update logical-to-physical mapping.

That extends Case 04 with another relocation trigger:

> **retention maintenance under access stress ≠ physical-location stability**.

The historical mechanisms remain distinct. Case 04's bounded mapped-Flash lineage centers erase/rewrite/reclamation and logical mapping; Case 52 adds read activity itself as a reason to retire or relocate an embodiment before its error budget becomes unsafe.

### Boundary with Case 67 — later 3-D NAND adaptive read reclaim

Case 52 remains the canonical physical/access-induced read-disturb case and now carries the 2002–2015 historical bridge. Case 67 remains a distinct later controller-policy slice: a 2017-priority / 2019 SK hynix disclosure uses compressed read-count proxies, thresholded ECC qualification, adaptive checking, 3-D neighborhood sampling, and conditional reclaim. The shared trigger family does not make the controller policies historically or technically identical.

> **generic read-disturb mechanism/history ≠ one later 3-D NAND controller policy**.

## Read semantics compared with magnetic core

A bounded functional analogy to Case 02 is useful because both cases make **access itself** part of the retention problem.

But the mechanisms oppose each other in important ways:

- in the classic destructive-read core case, reading the selected core directly destroys/changes the selected magnetic state and creates an immediate rewrite obligation;
- in NAND read disturb, the selected page can be read correctly while elevated pass voltage cumulatively perturbs **unselected neighboring cells**;
- core restore is constitutive of each destructive access in the bounded scheme;
- NAND disturb mitigation may be threshold-triggered, delayed, voltage-adaptive, ECC-masked, or relocation-based.

Therefore the only safe functional analogy is:

> **access can create a preservation obligation**.

It is not a historical genealogy and does not make NAND read disturb another form of magnetic-core destructive read.

## Failure and forgetting boundaries

Within this bounded regime, later loss can arise through distinct paths:

- cumulative pass-through stress shifts unread-cell threshold voltages;
- P/E wear increases susceptibility to a given amount of read disturb;
- retention-age error and other error sources consume the same finite ECC budget without sharing one cause;
- the present read can succeed while future margin deteriorates;
- a too-low `Vpass` can reduce disturb yet introduce pass-through/read errors;
- a read-count threshold can be set too aggressively or too conservatively, changing relocation overhead versus risk;
- relocation/rewrite can restore margin but consumes controller work, free space, program/erase operations, and mapping updates;
- RDR can improve probabilistic reconstruction without guaranteeing every failed cell is correctly inferred.

Forgetting here is not simply “the cell was read.” It is the eventual loss of a sufficiently distinguishable/recoverable logical state after cumulative physical disturbance and finite correction/recovery resources.

## Prior art and anti-anachronism

The 2015 DSN paper claims the first detailed/open experimental characterization of read disturb in contemporary 2Y-nm MLC NAND. This repository keeps that claim narrow.

It does **not** promote the paper into:

- invention of read disturb;
- invention of read-count monitoring;
- invention of read-triggered relocation;
- invention of all read-voltage adaptation or recovery.

US7818525B1 has a 2009 priority date and already describes recognized NAND `Read Disturb` errors, per-block read counting, threshold-triggered movement, ECC, and logical-to-physical remapping. The 2013 APSys paper independently places read-disturb management and FTL relocation before the 2015 characterization.

Accordingly:

> **2015 commercial-chip characterization ≠ invention of read-disturb mitigation**.

Historical vocabulary belongs to its source. Project phrases such as `access-stress clock`, `future-retention cost`, and `recovery evidence` are engineering reconstructions, not claims about how the engineers historically conceptualized memory or temporality.

## Philosophical interpretation — bounded

The case adds one narrow conceptual pressure to the repository:

> retrieval is not always external to retention. An operation that successfully makes a state available now can materially reduce the future recoverability of other retained states.

This helps resist a simple opposition in which `storage` passively preserves while `access` merely observes. It does **not** imply that every act of reading consumes its medium, nor that the 2015 authors were making a philosophical argument.

## Cross-case result

Case 52 adds a new maintenance trigger and a new read/retention relation:

```text
logical READ request
    !=
selected-page sensing
    !=
Vpass stress on unselected cells
    !=
cumulative neighbor threshold shift
    !=
raw error population
    !=
ECC-correctable current payload
    !=
remaining future correction margin
    !=
read-count / Vpass / relocation policy
    !=
optional probabilistic RDR recovery
```

Compared with Case 36:

```text
elapsed retention age / wear
    -> proactive renewal before ECC margin expires

cumulative read activity / wear
    -> access-induced error growth, mitigation, relocation, or recovery
```

The common higher-level relation is maintenance before recoverability margin is exhausted. The trigger and physical mechanism are different.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| NAND `Read Disturb` vocabulary and read-count-based mitigation predate 2015 | H/P | 2009-priority US7818525B1 + 2013 APSys record |
| A read to one NAND row can shift threshold voltages of unread cells in other rows of the same block | H/P | DSN 2015 §§1–2 + experimental characterization |
| The selected page may be read while neighboring unread cells receive cumulative pass-through-voltage stress | H/P/E | DSN 2015 circuit account + characterization |
| Read-disturb effect/RBER increases with cumulative reads and P/E wear in the tested 2Y-nm MLC chips | H/P | DSN 2015 §§3.2–3.3 |
| Read disturb and retention-age errors are distinct error sources that can coexist | H/P | DSN 2015 error taxonomy/evaluation |
| Per-block read count can act as a maintenance trigger | H/P/E | US7818525B1 + DSN 2015 prior-work section |
| Lowering Vpass can reduce disturb but can also create other read errors | H/P | DSN 2015 §§3.4–3.7 |
| Vpass Tuning is proven as a deployed commercial SSD feature | X | DSN 2015 proposes/evaluates the mechanism; it does not identify a shipped controller implementation |
| RDR intentionally adds controlled read disturbance to infer susceptible cells after an uncorrectable read | H/P | DSN 2015 §5 |
| RDR physically restores cells to their pre-disturb threshold voltages | X | RDR estimates logical state and retries ECC; physical rewind is not the demonstrated mechanism |
| NAND read disturb is the same mechanism as magnetic-core destructive read | X/A | only the bounded function `access can create preservation work` is comparable |
| Every modern NAND generation has the same read-count threshold | X | process, wear, voltage, architecture, and generation dependence are explicit limits |

## Related repositories

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated NAND read-disturb case. A broader history of NAND scaling, cell architecture, controllers, and manufacturer reliability techniques belongs there; this repository keeps the retention-specific relation among access, neighboring physical disturbance, ECC margin, read-count policy, relocation, and recovery.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the anti-anachronism discipline. `Read Disturb`, `Vpass Tuning`, and `Read Disturb Recovery` are source vocabulary where cited; `access-stress clock` and `future-retention cost` are modern analytical terms.

## Sources

1. Yu Cai, Yixin Luo, Saugata Ghose, Erich F. Haratsch, Ken Mai, Onur Mutlu, **“Read Disturb Errors in MLC NAND Flash Memory: Characterization, Mitigation, and Recovery,”** *45th Annual IEEE/IFIP International Conference on Dependable Systems and Networks (DSN)*, Rio de Janeiro, 2015, pp. 438–449, DOI `10.1109/DSN.2015.49`. Author/institution-hosted full paper: <https://istc-cc.cmu.edu/publications/papers/2015/flash-read-disturb-errors_dsn15.pdf>. Institutional abstract: <https://istc-cc.cmu.edu/publications/papers/2015/flash-read-disturb-errors_dsn15_abs.shtml>.
2. Holloway H. Frost, Charles J. Camp, Timothy J. Fisher, James A. Fuxa, Lance W. Shelton, **“Efficient reduction of read disturb errors in NAND FLASH memory,”** US7818525B1, priority 12 August 2009, filed 24 September 2009, published 19 October 2010, original assignee Texas Memory Systems, Inc.: <https://patents.google.com/patent/US7818525B1/en>.
3. Keonsoo Ha, Jaeyong Jeong, Jihong Kim, **“A read-disturb management technique for high-density NAND flash memory,”** *4th Asia-Pacific Workshop on Systems (APSys 2013)*, Article 13, DOI `10.1145/2500727.2500743`. Seoul National University publication record: <https://snu.elsevierpure.com/en/publications/a-read-disturb-management-technique-for-high-density-nand-flash-m/>.
