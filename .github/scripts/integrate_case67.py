from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = "cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md"
EVIDENCE_PATH = "evidence/67-sk-hynix-2009-2019-read-reclaim-grounding.md"

case = r'''# SK hynix 3-D NAND Read-Disturb Reclaim: Read-Count Proxies, Adaptive Thresholds, and Relocation

## Status

**`grounded`** — bounded to the manufacturer-primary controller design documented in SK hynix / SK hynix Memory Solutions America patent publication **US20190066809A1**, with priority dated 31 August 2017 and publication dated 28 February 2019. Earlier Samsung patent publications from 2009- and 2013-priority families are used to block false invention claims for ECC-margin-triggered read reclaim and relocation.

Grounding record: [`../evidence/67-sk-hynix-2009-2019-read-reclaim-grounding.md`](../evidence/67-sk-hynix-2009-2019-read-reclaim-grounding.md).

## Scope

This case asks a narrow question left open by Cases 52 and 65:

> What changes when a 3-D NAND controller treats **read activity and measured error margin as maintenance evidence**, adapts how often it tests potentially disturbed regions, and can preserve the logical payload by copying valid values into a new physical population before the old embodiment becomes uncorrectable?

The bounded object is the read-disturb detection/recovery composition in US20190066809A1:

- a read-count proxy associated with a block/group of blocks;
- a read threshold that determines when to perform read-disturb checking;
- test reads of an associated or expanded region;
- ECC-derived bit-error evidence;
- adaptive read thresholds / error thresholds;
- a read-reclaim operation that copies valid values to other memory cells;
- clearing/resetting the read-count proxy after reclaim and, in the disclosed design, after power-off;
- 3-D neighborhood sampling that can include wordlines above and below the original read location.

This is **not**:

- proof that a named commercial SK hynix SSD shipped this exact algorithm, threshold table, counter width, or persistence behavior;
- a generic history of NAND read disturb;
- a claim that SK hynix invented read reclaim, ECC-margin-triggered relocation, garbage collection, wear leveling, ECC, or 3-D NAND;
- evidence that the controller counter is a direct physical measurement of trapped charge or threshold-voltage shift;
- a claim that power-off physically resets read-disturb damage;
- a claim that read reclaim securely erases the superseded physical cells;
- a substitute for Case 52's physical read-disturb characterization or Case 65's retention-age-aware read-reference adaptation.

## Historical record

### A repeated read can create a future retention obligation outside the logical read target

US20190066809A1 describes the familiar NAND read-disturb mechanism: pass bias applied while reading can unintentionally change charge/threshold state in nonselected cells. It then frames a controller workload in which repeated reads of a single page can cause read disturb across a larger block.

The source therefore supports a bounded historical/engineering distinction:

> **successful logical read ≠ absence of future retention debt**.

A read can return correct data now while contributing to a physical condition that makes later reads less reliable.

It also supports:

> **logical read target ≠ complete physically stressed neighborhood**.

The operation named by the host/controller and the set of cells whose reliability margin is affected need not have the same geometry.

### The design retains a read-count proxy rather than one counter for every physical victim

The patent explains that an idealized implementation could maintain a read counter for every page, but that counter storage is expensive, particularly under mobile-product memory constraints. The disclosed approach groups blocks/counters and chooses counter length and check frequency together.

The controller therefore retains a compressed workload-history state:

> **read-count proxy ≠ physical read-disturb state**.

The count records selected read activity under one policy. It is not the victim cells' threshold-voltage distribution and is not a complete history of every electrically relevant event.

### Threshold crossing triggers qualification, not necessarily immediate relocation

The disclosed flow increments the relevant read count. When a threshold or a multiple of the threshold is reached, the controller performs a read-disturb test. The test obtains bit-error evidence from associated blocks/pages and compares it with an error threshold. The error threshold may be expressed as a percentage of the system's ECC capability.

This yields two distinct boundaries:

> **read-count threshold crossing ≠ uncorrectable payload**.

and:

> **read-count threshold crossing ≠ automatic proof that relocation is required**.

The count schedules/qualifies further checking; measured error state can decide whether reclaim should occur.

### Error evidence can change the future maintenance cadence

The patent describes an adaptive target read threshold selected according to bit errors, including a lookup-table form in which higher bit-error counts can correspond to lower subsequent read thresholds. It also describes more aggressive checking after conditions such as counter refresh/power-off when conservative treatment is warranted.

Thus:

> **adaptive read threshold ≠ fixed physical failure limit**.

The threshold is retained/derived **policy state**: a controller decision about when to inspect again, informed by observed error evidence and expected workload risk.

### Read reclaim re-embodies valid values

The claims explicitly define a read-reclaim operation that can copy valid values from one plurality of memory cells to another. Other passages describe triggering garbage-collection/reclaim work when the test indicates sufficient error pressure.

Therefore:

> **ECC-correctable logical data ≠ data that must remain in the same cells**.

and:

> **read reclaim relocation ≠ logical payload change**.

The same logical value can be preserved precisely by ending its dependence on the more-disturbed physical embodiment.

### The disclosed counter can be cleared at power-off

One of the most useful details for retention comparison is explicit: the first read count can be set to zero after a power-off as well as after read reclaim. The description argues that shorter counters and sufficiently conservative checking can avoid having to store the counters in NAND across sudden power loss.

This establishes a strong counterexample:

> **controller counter continuity ≠ medium damage continuity**.

and, more specifically:

> **power-off-cleared maintenance proxy ≠ power-off-cleared read disturb**.

The controller is allowed to forget one compressed history variable while the physical cells do not thereby return to their earlier threshold-voltage state. The design must compensate through conservative post-reset checking policy rather than by pretending the physical history disappeared.

### 3-D geometry changes what should be sampled

For a 3-D NAND embodiment, the patent's expanded-block test can include pages associated with wordlines at higher and lower levels than the first block/read location. The description also discusses sampling top/bottom and neighboring wordline positions.

This does not establish one universal 3-D NAND disturb geometry. It does establish that the controller design treats physical vertical adjacency as relevant maintenance information beyond the logical page originally requested.

## Retained states and control state

The bounded regime contains at least seven separable states:

1. **logical payload** — the value the host expects to remain recoverable;
2. **physical cell state** — threshold/charge distributions whose margin can be altered by read disturb;
3. **logical-to-physical mapping** — needed if reclaim relocates the current payload;
4. **read-count proxy** — compressed workload-history state used to schedule checks;
5. **last-read / grouping information** — controller state used by some disclosed counter/sampling variants;
6. **bit-error / ECC evidence** — a measured qualification of current recoverability margin;
7. **adaptive policy state** — target read threshold, error threshold, sampling factor, or lookup-table relation that determines future maintenance.

These states do not share one lifetime. In the disclosed design, the medium condition survives power-off while the read-count proxy may not.

## Engineering reconstruction

### A maintenance proxy may intentionally be less durable than the condition it protects against

Most retention discussions assume that if a controller remembers a risk history, longer persistence of that history is automatically better. Case 67 provides a counterexample. The patent explicitly trades counter-storage persistence against check frequency and conservative threshold selection.

So:

> **maintenance-proxy lifetime can be shorter than physical-condition lifetime**.

This is not permission to discard arbitrary metadata. It is a design-specific statement that a lossy proxy can still be safe if its reset boundary is composed with a conservative requalification policy.

### ECC correction and physical renewal are separate acts

ECC can make a current read logically successful even while bit-error count indicates shrinking margin. Read reclaim then copies valid values to other cells.

Therefore:

> **current ECC correction ≠ future margin restoration**.

and:

> **read reclaim ≠ ECC correction**.

One recovers/qualifies a value from the current embodiment; the other changes the embodiment carrying the value into the future.

### Read retry / read-reference adaptation and reclaim are different recovery loci

Case 65 shows that a controller can adapt read interpretation according to retention age, and Case 59 shows read-reference adaptation after interference. Earlier Samsung read-reclaim prior art also explicitly distinguishes changing read voltage from copying data to another block.

Thus:

> **read-reference adaptation ≠ read-reclaim relocation**.

A successful retry can recover the current logical value without moving it. Reclaim uses a recovered/valid value to create a new physical copy and then changes which embodiment should carry currentness.

### Reliability-triggered reclaim and capacity-triggered garbage collection should not be collapsed

The SK hynix design may invoke garbage-collection-like movement when read-disturb evidence warrants relocation. That does not make its trigger identical to ordinary space reclamation.

> **reliability-triggered reclaim ≠ capacity-triggered garbage collection**.

The physical copy/erase machinery may overlap while the reason for selecting a block and the retained evidence that authorizes the work differ.

### Relocation is not sanitization

Copying valid values elsewhere and retiring the old location preserves logical continuity. Nothing in the bounded source proves immediate physical removal of all superseded charge states or forensic remnants.

Therefore:

> **read-reclaim relocation ≠ secure erase / sanitization**.

Cases 44 and 47 remain the relevant forgetting/sanitization boundary.

## Cross-case boundaries

### Versus Case 52 — NAND read disturb

Case 52 establishes the physical/access-induced regime: repeated reads can apply pass-voltage stress to unread same-block cells; cumulative reads become a maintenance clock; mitigation may include voltage tuning, relocation, or probabilistic recovery.

Case 67 adds a **manufacturer-primary controller-policy slice**:

```text
read activity
    -> compressed read-count proxy
    -> thresholded test-read schedule
    -> ECC/bit-error qualification
    -> adaptive future threshold
    -> conditional reclaim / relocation
```

The two are complementary. Case 67 does not replace Case 52's characterization evidence, and the patent does not prove a shipped commercial implementation.

### Versus Case 65 — 3-D NAND early retention loss

Case 65 is principally elapsed-time / retention-age driven:

```text
program age + P/E state
    -> age-aware read reference
    -> improved interpretation of the same physical embodiment
```

Case 67 is principally read-workload / disturb driven:

```text
read-count proxy + measured bit errors
    -> inspection urgency
    -> conditional physical relocation
```

Elapsed-time retention loss and access-induced read disturb can coexist, but they are different maintenance clocks and failure mechanisms.

### Versus Case 36 — Flash Correct-and-Refresh

Case 36 studies retention-error correction and refresh/reprogram policy using retention/wear information. Case 67 studies read-disturb pressure caused by access history and a distinct trigger path into reclaim. Both can end in re-embodiment; the trigger and diagnostic relation are not the same.

### Versus Case 04 — mapped Flash

Case 04 establishes that logical identity can survive physical relocation under an FTL-style mapping relation. Case 67 supplies a later **reason** for relocation: not only erase/reclaim geometry, but proactive reliability maintenance after access-induced stress.

### Versus Case 59 — program interference

Program interference is write-induced neighbor coupling. Read disturb is read-induced pass-voltage stress. The shared relation is only functional:

> an operation that succeeds for its logical target can alter the future reliability margin of another retained state.

The physical mechanisms and histories remain distinct.

## Failure and forgetting boundaries

Distinct failure or policy-failure modes include:

- the read-count proxy underestimates relevant stress;
- grouping/sampling misses the most disturbed victim region;
- a threshold is too lax for the actual error-growth regime;
- power-off resets volatile counter state and requalification policy is not conservative enough;
- ECC margin falls faster than scheduled checking anticipates;
- valid data cannot be recovered well enough to seed relocation;
- relocation/GC is interrupted or mapping/currentness handoff fails;
- reclaim consumes additional program/erase endurance;
- a controller confuses a successful retry with sufficient future retention margin;
- a physical old embodiment survives after logical relocation, creating no implication of secure erasure.

These are not one generic `bit rot` mechanism. Some concern the medium, others the adequacy and lifetime of controller-side maintenance evidence.

## Historical record / engineering reconstruction / interpretation ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| US20190066809A1 has 2017-08-31 priority, 2019-02-28 publication, and SK hynix assignees | `H/P` | patent bibliographic record |
| repeated single-page reads are treated as capable of disturbing a larger block | `H/P` | patent background/description |
| controller increments read-count state and schedules test reads at threshold/multiple conditions | `H/P` | patent abstract, description, and claims |
| bit-error evidence can select an adaptive target read threshold and error threshold | `H/P` | patent description/claims |
| read reclaim can copy valid values into another plurality of cells | `H/P` | explicit claims |
| the disclosed read count may be reset at power-off without storing it in NAND | `H/P` | explicit description/claims |
| physical read-disturb state therefore resets at power-off | `X` | contradicted by the distinction between a controller proxy and cell condition |
| SK hynix invented read reclaim or ECC-margin-triggered relocation in 2017 | `X` | earlier Samsung 2009/2013 patent evidence |
| this patent proves a named commercial SK hynix SSD shipped the exact algorithm | `X` | patent/design evidence is not product deployment evidence |
| logical payload can survive a controller-authorized change of physical embodiment | `E` | follows from valid-value copy + mapping/currentness handoff |
| a volatile/lossy maintenance proxy may still support retention if reset is paired with conservative requalification | `E` | bounded reconstruction of the disclosed power-off/counter/check-frequency composition |
| this is equivalent to human memory, forgetting, or recollection | `X/I` | unsupported philosophical anthropomorphism |

## Philosophical interpretation — bounded

This case adds one narrow pressure to the repository's vocabulary of technical retention:

> **A system does not need to retain every causal trace in order to retain a usable object. It may preserve a deliberately compressed, even resettable maintenance proxy, provided that later requalification and repair work re-establish enough confidence before the physical margin is exhausted.**

That is an engineering relation, not a claim about human memory. It is useful because it separates **retaining the payload**, **retaining the physical condition**, and **retaining evidence about what maintenance the payload may soon need**.

## Cross-case result

Case 67 adds this chain:

```text
correct read now
    !=
no read-induced physical stress
    !=
read-count proxy
    !=
measured bit-error condition
    !=
adaptive maintenance threshold
    !=
reclaim decision
    !=
new physical embodiment
    !=
secure erasure of the old embodiment
```

Its strongest new result is that **controller-maintained risk history can be intentionally less durable than the medium state it approximates**, while still participating in a safe retention regime through conservative re-testing and relocation.

## Prior art and anti-anachronism

The 2017-priority SK hynix design is not the origin of read reclaim.

Samsung's US20100235713A1, with 2009 priority and 2010 publication, already describes an ECC circuit counting read-data error bits, a minimum threshold below the maximum correctable-error count, a read-reclaim indication, and reassignment/change of the affected block before the data exceeds ECC capability.

Samsung's US20140237165A1, with 2013 priority and 2014 publication, separately describes controller read reclaim as copying data to another block, compares bit-error rate with a threshold, uses read voltage/retry state in the reclaim decision, and explicitly notes that reclaim adds erase/write work and can shorten device lifetime.

Therefore the defensible claim is narrower:

> **By the 2017-priority SK hynix design, 3-D NAND read-disturb maintenance was being formulated as a composition of compressed read-count tracking, adaptive test thresholds based on error evidence, 3-D neighborhood sampling, and conditional relocation/reclaim.**

That is enough to deepen the retention comparison without an invention-priority or shipped-product claim.

## Sources

1. SK hynix Inc. / SK hynix Memory Solutions America Inc., **US20190066809A1, “Read disturb detection and recovery with adaptive thresholding for 3-d nand storage,”** priority 31 August 2017, filed 7 December 2017, published 28 February 2019; granted as US10714195B2, 14 July 2020: <https://patents.google.com/patent/US20190066809A1/en>
2. Samsung Electronics Co., Ltd., **US20100235713A1, “Non-volatile memory generating read reclaim signal and memory system,”** priority 12 March 2009, published 16 September 2010: <https://patents.google.com/patent/US20100235713A1/en>
3. Samsung Electronics Co., Ltd., **US20140237165A1, “Memory controller, method of operating the same and memory system including the same,”** priority 19 February 2013, published 21 August 2014: <https://patents.google.com/patent/US20140237165A1/en>

## Related repositories

A repository search found no dedicated 3-D NAND read-reclaim / read-disturb controller case in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). A broader history of commercial controller families, product deployment, and 3-D NAND generations belongs there if pursued; this case keeps the retention-specific relation between workload evidence, adaptive maintenance policy, and re-embodiment here.
'''

evidence = r'''# Grounding Record — 3-D NAND Read-Disturb Reclaim and Adaptive Thresholding (2009–2019)

## Purpose

This record grounds [`../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md`](../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md).

The bounded claim is **not** that SK hynix invented NAND read disturb or read reclaim. It is that manufacturer-primary patent evidence supports a specific 2017-priority 3-D NAND controller composition in which a compressed read-count proxy schedules testing, measured bit-error evidence adapts future thresholds, a 3-D expanded neighborhood can be checked, and valid values can be relocated through read reclaim. Earlier Samsung patent publications establish that ECC-margin-triggered read reclaim and block relocation already predate this filing.

## Source hierarchy

### A — primary manufacturer design source

SK hynix Inc. / SK hynix Memory Solutions America Inc., **US20190066809A1**, “Read disturb detection and recovery with adaptive thresholding for 3-d nand storage”:

<https://patents.google.com/patent/US20190066809A1/en>

Bibliographic record:

- priority: **2017-08-31**;
- filing: **2017-12-07**;
- publication: **2019-02-28**;
- granted as **US10714195B2** on **2020-07-14**;
- original assignees include SK hynix Inc. and SK hynix Memory Solutions America Inc.

Directly inspected source anchors include:

- background/summary passages describing pass-bias read disturb and repeated single-page reads affecting a larger block;
- summary/claims for read count, read threshold, test-read scheduling, bit-error-based adaptive target threshold, and ECC-percentage error thresholds;
- claims defining read reclaim as copying valid values to another plurality of memory cells;
- description/claims allowing the read count to reset after read reclaim or power-off;
- description explaining the counter-storage tradeoff and why counters need not be persisted in NAND across sudden power-off in this design;
- 3-D expanded-block sampling including pages on higher/lower wordlines and other selected positions.

### B — earlier manufacturer prior art: ECC margin and reclaim indication

Samsung Electronics Co., Ltd., **US20100235713A1**, “Non-volatile memory generating read reclaim signal and memory system”:

<https://patents.google.com/patent/US20100235713A1/en>

Bibliographic record:

- priority: **2009-03-12**;
- publication: **2010-09-16**.

Directly inspected source anchors:

- ECC detects/corrects up to a maximum number of errors;
- a counter detects when read-data error count exceeds a lower `error-possible` threshold;
- a read-reclaim indicator can identify a block before the error count exceeds ECC capability;
- logical addresses / block placement can be changed before the condition becomes uncorrectable.

This blocks any claim that the 2017 SK hynix filing invented ECC-margin-triggered read reclaim or proactive block reassignment.

### C — earlier manufacturer prior art: reclaim versus retry and endurance

Samsung Electronics Co., Ltd., **US20140237165A1**, “Memory controller, method of operating the same and memory system including the same”:

<https://patents.google.com/patent/US20140237165A1/en>

Bibliographic record:

- priority: **2013-02-19**;
- publication: **2014-08-21**.

Directly inspected source anchors:

- controller calculates bit-error rate and compares it with a threshold;
- read retry changes read voltage and can reduce current BER;
- read reclaim is separately described as copying data from one block to another;
- reclaim decision can depend on BER and read-voltage state;
- read reclaim adds erase/write work and therefore can reduce device lifetime;
- read reclaim is included among controller background operations.

This supplies a useful pre-2017 boundary between **interpretive recovery** (retry/read-voltage adjustment) and **physical re-embodiment** (reclaim/copy).

## Verified facts from US20190066809A1

### 1. Read activity is tracked as controller state

The design associates a read count and read threshold with a block/group. Reads increment the count; threshold/multiple conditions trigger test-read work.

Safe claim:

> read activity becomes retained controller-side maintenance evidence.

Unsafe claim:

> the counter is a direct physical measure of read-disturb damage.

The patent treats it as a proxy/scheduling state and then measures bit errors separately.

### 2. A successful read can stress a wider physical region

The description states that repeated single-page reads can cause read disturb across the block and discusses pass-bias-induced charge/threshold effects.

Safe claim:

> logical read target and physical stress scope can differ.

This is compatible with, but does not replace, the independent/read-disturb characterization evidence already used in Case 52.

### 3. Test reads qualify the proxy with measured error evidence

At check points, the controller can read associated/expanded pages, perform ECC decoding, determine error counts, and compare them with an error threshold. The threshold can be expressed as a percentage of ECC capability.

Safe claims:

- threshold crossing schedules qualification rather than proving immediate data loss;
- ECC margin is a separate retained/observed relation from the read-count proxy.

### 4. Future check cadence can be adaptive

The patent describes selecting a second/target read threshold according to observed bit errors, including lookup-table behavior with lower thresholds for higher error counts.

Safe claim:

> policy state can adapt to measured medium condition.

Unsafe claim:

> one named commercial SSD used a particular table or threshold value.

No product deployment evidence is supplied.

### 5. Read reclaim changes physical embodiment

Claims define read reclaim as copying valid values from one plurality of cells to another.

Safe claims:

- reclaim can preserve logical payload while replacing physical embodiment;
- current ECC success and future physical renewal are separate events.

Unsafe claim:

> reclaim securely erases all superseded physical remnants.

The source does not establish sanitization.

### 6. Read-count lifetime can be shorter than physical-condition lifetime

The patent says the read count can be reset to zero after power-off and describes avoiding NAND persistence of those counters across sudden power loss, paired with check-frequency/threshold design intended to detect risky blocks early enough.

Safe reconstruction:

> controller counter continuity ≠ medium damage continuity.

This is one of the central reasons the case belongs in `technical-retention`: a maintenance proxy may be deliberately volatile even though the condition it approximates is nonvolatile.

Unsafe claim:

> power-off repairs or resets read disturb.

Nothing in the source supports that.

### 7. 3-D sampling expands beyond the original read location

The patent's expanded-region examples include wordlines above/below the read location and other sampled pages.

Safe claim:

> the design treats physical 3-D neighborhood information as relevant to maintenance qualification.

Unsafe claim:

> this exact geometry is universal to all 3-D NAND products or generations.

## Prior-art / novelty boundary

Do **not** claim:

- SK hynix invented read reclaim;
- SK hynix invented proactive relocation before ECC failure;
- SK hynix invented read retry or adaptive read voltage;
- SK hynix invented read-disturb counters;
- US20190066809A1 proves first commercial deployment;
- the 2017 filing is the first 3-D NAND reliability-management algorithm.

The source-supported contribution is narrower:

> by the 2017-priority SK hynix filing, a manufacturer design for 3-D NAND explicitly composed compressed read-count tracking, adaptive error-informed test cadence, expanded 3-D neighborhood checking, and conditional valid-data relocation.

Samsung's 2009-priority patent already establishes a lower-than-ECC-limit error threshold feeding a read-reclaim indication, and Samsung's 2013-priority patent already establishes BER/read-voltage-qualified block copying plus the endurance cost of reclaim. These sources make invention-priority claims unnecessary and unsafe.

## In-repository boundaries

### Case 52 — physical read-disturb regime

[`../cases/52-nand-flash-read-disturb-access-induced-decay.md`](../cases/52-nand-flash-read-disturb-access-induced-decay.md) grounds access-induced NAND disturbance, `Vpass` stress, cumulative-read pressure, and characterization/mitigation concepts. Case 67 adds a later manufacturer-controller design with explicit maintenance proxy lifetime and relocation policy. It should not be used to rewrite Case 52's physical history.

### Case 65 — early retention loss / age-aware reading

[`../cases/65-3d-nand-early-retention-loss-age-aware-reading.md`](../cases/65-3d-nand-early-retention-loss-age-aware-reading.md) uses elapsed retention age as read-interpretation state. Case 67 uses read workload and measured bit errors to decide inspection and re-embodiment. Time-driven retention and access-driven disturb remain distinct.

### Case 36 — Flash Correct-and-Refresh

[`../cases/36-nand-flash-correct-and-refresh-maintenance.md`](../cases/36-nand-flash-correct-and-refresh-maintenance.md) concerns retention-error correction/refresh and wear-informed policy. Similarity at the `repair can rewrite/move data` level is functional only.

### Case 04 — mapped Flash

[`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md) supplies the generic logical-identity-across-relocation relation. Case 67 supplies one later reliability trigger for such relocation.

### Cases 44 / 47 — sanitization

Read reclaim preserving logical currentness is the opposite objective from secure forgetting. Do not infer physical erase/remanence semantics from relocation.

## Related-repository duplication check

A current search of `tmzncty/computing-archaeology` for `read reclaim 3D NAND` returned no dedicated case. General controller/product genealogy should go there if developed later. This record therefore keeps only the retention-specific workload-evidence → qualification → relocation relation in `technical-retention`.

## What the evidence does not establish

The sources do not establish:

- a named shipping SK hynix SSD/controller using exactly US20190066809A1;
- exact production firmware thresholds, table values, counter widths, or sampling factors;
- how the read-count state is coordinated with every real FTL mapping/checkpoint path;
- crash consistency of a reclaim relocation in a named product;
- independent fault-injection validation;
- one universal 3-D NAND disturb topology;
- secure erasure of source cells after relocation;
- invention priority for read reclaim or read-disturb management.

These remain separate slices.

## Sources

1. SK hynix Inc. / SK hynix Memory Solutions America Inc., **US20190066809A1**, “Read disturb detection and recovery with adaptive thresholding for 3-d nand storage,” priority 31 August 2017, published 28 February 2019: <https://patents.google.com/patent/US20190066809A1/en>
2. Samsung Electronics Co., Ltd., **US20100235713A1**, “Non-volatile memory generating read reclaim signal and memory system,” priority 12 March 2009, published 16 September 2010: <https://patents.google.com/patent/US20100235713A1/en>
3. Samsung Electronics Co., Ltd., **US20140237165A1**, “Memory controller, method of operating the same and memory system including the same,” priority 19 February 2013, published 21 August 2014: <https://patents.google.com/patent/US20140237165A1/en>
'''

readme_case_line = "- [`cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md`](cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md) — grounded manufacturer-primary 3-D NAND read-disturb controller bridge: a compressed read-count proxy schedules test reads, ECC/bit-error evidence adapts future thresholds, and conditional read reclaim copies valid values to a new physical population; the disclosed counter can reset at power-off, sharply separating maintenance-proxy continuity from medium-condition continuity."
readme_evidence_line = "- [`evidence/67-sk-hynix-2009-2019-read-reclaim-grounding.md`](evidence/67-sk-hynix-2009-2019-read-reclaim-grounding.md) — Case-67 grounding record: SK hynix's 2017-priority 3-D NAND design is bounded against Samsung 2009/2013 read-reclaim prior art, while named-product deployment, exact production thresholds/counter persistence, and independent fault validation remain open."

case_index_row = "| [SK hynix 3-D NAND Read-Disturb Reclaim: Read-Count Proxies, Adaptive Thresholds, and Relocation](cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md) | **grounded** | access-induced NAND stress + compressed read-count maintenance proxy + ECC/bit-error qualification + adaptive thresholds + conditional physical relocation | separate successful current read from future retention debt; controller proxy lifetime from medium-condition lifetime; retry/interpretation from reclaim/re-embodiment; reliability-triggered reclaim from capacity GC and sanitization | [2009–2019 read-reclaim grounding](evidence/67-sk-hynix-2009-2019-read-reclaim-grounding.md); named shipping product, exact firmware thresholds/counter persistence, crash-safe relocation implementation, and independent validation remain separate work |"

matrix_row = "| SK hynix 3-D NAND adaptive read-disturb reclaim / 2017–2019 | logical payload + physical threshold state + read-count proxy + ECC/error evidence + adaptive maintenance thresholds + mapping/currentness | read activity increments a compressed proxy; thresholded test reads qualify physical margin; error evidence can tighten future cadence; reclaim copies valid values elsewhere | ordinary read can succeed while adding disturb pressure; test reads/ECC qualify risk; reclaim performs physical re-embodiment rather than merely reinterpretation | logical mapping + grouped read-count state + sampled 3-D neighborhood + target/error thresholds; counter may reset at power-off | physical disturb can outlive volatile proxy state; insufficient post-reset conservatism, missed victims, or failed relocation can exhaust margin | preserves current logical payload while retaining only compressed/resettable workload evidence rather than complete access history |"

findings = r'''## Case 67 — SK hynix 3-D NAND adaptive read-reclaim findings

749. **successful logical read ≠ absence of future retention debt** — a read can return correct data while pass-bias stress contributes to later read-disturb risk;
750. **read-count proxy ≠ physical read-disturb state** — controller history schedules inspection but is not the threshold-voltage/charge condition itself;
751. **controller count continuity ≠ medium damage continuity** — the disclosed count may be cleared or lost across a boundary that does not restore the cells;
752. **power-off-cleared counter ≠ power-off-cleared disturb** — a power transition can reset bookkeeping while physical read-disturb history remains embodied in the medium;
753. **read-count threshold crossing ≠ uncorrectable payload** — threshold crossing can trigger a test-read/qualification step before ECC capability is exhausted;
754. **measured bit-error margin can qualify maintenance urgency** — ECC-derived error evidence can determine whether reclaim occurs and how soon future checks should recur;
755. **adaptive read threshold ≠ fixed physical failure limit** — the target threshold is policy/control state selected from measured conditions rather than a universal cell constant;
756. **ECC-correctable data ≠ data safe to leave indefinitely in the same cells** — current successful correction can coexist with a proactive decision to renew the embodiment;
757. **read retry / read-reference adaptation ≠ read-reclaim relocation** — reinterpretation can recover a current value without moving it, whereas reclaim copies valid data into another physical population;
758. **read-reclaim relocation ≠ logical payload change** — logical continuity can be preserved through a change of physical carrier;
759. **logical payload continuity ≠ physical embodiment continuity** — the same current object can survive deliberate replacement of disturbed cells;
760. **reliability-triggered reclaim ≠ capacity-triggered garbage collection** — copy/GC machinery may overlap while trigger evidence and retention purpose differ;
761. **read-reclaim relocation ≠ secure erase / sanitization** — moving current data supplies no proof that superseded physical remnants are immediately or forensically removed;
762. **logical read target ≠ complete physically stressed 3-D neighborhood** — the disclosed check can sample higher/lower wordlines and associated blocks outside the originally addressed page;
763. **maintenance-proxy lifetime can be shorter than physical-condition lifetime** — the 2017 design explicitly trades durable counter storage against conservative test frequency/threshold policy;
764. **2017 SK hynix adaptive 3-D reclaim composition ≠ invention of read reclaim or ECC-margin-triggered maintenance** — Samsung 2009/2013 patent evidence already documents proactive error-threshold indication, block relocation, retry/reclaim separation, and reclaim endurance cost.
'''


def insert_after_line_with(text, needle, new_line):
    if new_line in text:
        return text
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if needle in line]
    if not matches:
        raise RuntimeError(f"anchor not found: {needle}")
    lines.insert(matches[-1] + 1, new_line)
    return "\n".join(lines).rstrip() + "\n"


def patch_readme(text):
    text = insert_after_line_with(text, "cases/66-nvme14-persistent-event-log-history.md", readme_case_line)
    text = insert_after_line_with(text, "evidence/66-nvme14-2019-persistent-event-log-grounding.md", readme_evidence_line)
    return text


def patch_roadmap(text):
    if CASE_PATH in text:
        return text
    lines = text.splitlines()
    idx = next((i for i, line in enumerate(lines) if "SSD FTL/controller-mediated persistence" in line), None)
    if idx is None:
        raise RuntimeError("SSD roadmap anchor not found")
    line = lines[idx]
    line2, n = re.subn(r"55, 59, 65, and 66\*\*", "55, 59, 65, 66, and 67**", line, count=1)
    if n == 0:
        line2, n = re.subn(r"65, and 66\*\*", "65, 66, and 67**", line, count=1)
    if n == 0:
        raise RuntimeError("could not update SSD case list")
    desc = " [`cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md`](cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md), grounded by [`evidence/67-sk-hynix-2009-2019-read-reclaim-grounding.md`](evidence/67-sk-hynix-2009-2019-read-reclaim-grounding.md), advances the manufacturer-primary 3-D-NAND read-reclaim design layer left open by Cases 52 and 65: a compressed read-count proxy schedules read-disturb tests, ECC/bit-error evidence adapts future thresholds, 3-D neighborhood sampling qualifies risk, and conditional reclaim copies valid values into a new physical population. The patent also allows the count to reset at power-off, making controller-proxy continuity explicitly shorter than medium-condition continuity. Earlier Samsung 2009/2013 read-reclaim patents block an invention claim, and the patent itself does not prove a named shipping product."
    marker = " The broad item stays unchecked because"
    if marker not in line2:
        raise RuntimeError("SSD broad-item marker not found")
    line2 = line2.replace(marker, desc + marker, 1)
    line2 = line2.replace("modern 3D-NAND read-reclaim/device-specific read-disturb management", "named-commercial 3D-NAND read-reclaim/device-specific implementation and independent validation")
    lines[idx] = line2
    return "\n".join(lines).rstrip() + "\n"


def patch_case_index(text):
    if CASE_PATH not in text:
        text = insert_after_line_with(text, "cases/66-nvme14-persistent-event-log-history.md", case_index_row)
    if matrix_row not in text:
        lines = text.splitlines()
        h = next((i for i, line in enumerate(lines) if line.strip() == "## Comparison matrix — provisional"), None)
        if h is None:
            raise RuntimeError("comparison matrix heading not found")
        start = next((i for i in range(h + 1, len(lines)) if lines[i].startswith("| Case |")), None)
        if start is None:
            raise RuntimeError("comparison matrix table not found")
        end = start + 2
        while end < len(lines) and lines[end].startswith("|"):
            end += 1
        lines.insert(end, matrix_row)
        text = "\n".join(lines).rstrip() + "\n"
    if "## Case 67 — SK hynix 3-D NAND adaptive read-reclaim findings" not in text:
        text = text.rstrip() + "\n\n" + findings.rstrip() + "\n"
    return text


def run(*args):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True)


def main():
    subprocess.run(["git", "pull", "--ff-only", "origin", "main"], cwd=ROOT, check=True)

    (ROOT / CASE_PATH).write_text(case.rstrip() + "\n", encoding="utf-8")
    (ROOT / EVIDENCE_PATH).write_text(evidence.rstrip() + "\n", encoding="utf-8")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    index = (ROOT / "CASE_INDEX.md").read_text(encoding="utf-8")

    (ROOT / "README.md").write_text(patch_readme(readme), encoding="utf-8")
    (ROOT / "ROADMAP.md").write_text(patch_roadmap(roadmap), encoding="utf-8")
    (ROOT / "CASE_INDEX.md").write_text(patch_case_index(index), encoding="utf-8")

    nums = sorted(int(p.name[:2]) for p in (ROOT / "cases").glob("[0-9][0-9]-*.md"))
    if nums != list(range(68)):
        raise RuntimeError(f"case-number ledger mismatch: {nums[:3]} ... {nums[-5:]}")
    for p in [CASE_PATH, EVIDENCE_PATH]:
        if not (ROOT / p).exists():
            raise RuntimeError(f"missing {p}")
    for nav in ["README.md", "ROADMAP.md", "CASE_INDEX.md"]:
        t = (ROOT / nav).read_text(encoding="utf-8")
        if CASE_PATH not in t:
            raise RuntimeError(f"{nav} missing case 67 path")
    idx_text = (ROOT / "CASE_INDEX.md").read_text(encoding="utf-8")
    if "749. **successful logical read" not in idx_text or "764. **2017 SK hynix" not in idx_text:
        raise RuntimeError("case 67 findings missing")
    if idx_text.count(CASE_PATH) < 1:
        raise RuntimeError("case 67 index row missing")
    run("git", "diff", "--check")

    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], cwd=ROOT, check=True)
    subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], cwd=ROOT, check=True)
    subprocess.run(["git", "add", "README.md", "ROADMAP.md", "CASE_INDEX.md", CASE_PATH, EVIDENCE_PATH], cwd=ROOT, check=True)
    subprocess.run(["git", "rm", "-f", ".github/scripts/integrate_case67.py", ".github/workflows/integrate-case67.yml"], cwd=ROOT, check=True)
    subprocess.run(["git", "commit", "-m", "case67: ground 3D NAND adaptive read-reclaim policy"], cwd=ROOT, check=True)
    subprocess.run(["git", "push", "origin", "HEAD:main"], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
