# SK hynix 3-D NAND Read-Disturb Reclaim: Read-Count Proxies, Adaptive Thresholds, and Relocation

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
