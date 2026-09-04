# Grounding Record — 3-D NAND Read-Disturb Reclaim and Adaptive Thresholding (2009–2019)

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
