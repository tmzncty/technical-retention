# Case 52 Deepening — SanDisk 2012–2013 Targeted Read Scrub: Counter-Free Sampling, Retained Policy, and Queue-Lifetime Choice

## Status

**`bounded deepening complete`** for the SanDisk targeted-read-scrub control-state slice described here.

Canonical case: [`../cases/52-nand-flash-read-disturb-access-induced-decay.md`](../cases/52-nand-flash-read-disturb-access-induced-decay.md).

Related Case 52 records:

- [`52-cai-2009-2015-nand-read-disturb-grounding.md`](52-cai-2009-2015-nand-read-disturb-grounding.md)
- [`52-micron-2006-read-disturb-temporary-failure-maintenance-deepening.md`](52-micron-2006-read-disturb-temporary-failure-maintenance-deepening.md)
- [`52-denali-2008-2009-persistent-read-count-checkpoint-deepening.md`](52-denali-2008-2009-persistent-read-count-checkpoint-deepening.md)
- [`52-sandisk-2004-2007-read-disturb-exposure-avoidance-prior-art-deepening.md`](52-sandisk-2004-2007-read-disturb-exposure-avoidance-prior-art-deepening.md)

## Why this slice exists

Case 52 already has a particularly useful early controller-state witness in Denali's 2008-filed / July-2009-public design: a block table can retain read-count data in non-volatile memory, load it into working memory at power-up, update the live copy during service, and checkpoint it periodically / at shutdown. That record makes accumulated access history into an explicit maintenance clock.

A later SanDisk filing exposes a complementary design choice that should not be collapsed into the Denali topology. Steven T. Sprouse et al., **_Flash memory with targeted read scrub algorithm_**, filed 21 June 2012 and publicly published as **US20130346805A1 on 26 December 2013**, describes a targeted read-scrub design that can decide whether to inspect for read disturb **without storing per-block or per-word-line read counters**. Instead, one embodiment probabilistically admits a scan in response to host reads, uses retained manufacturer-derived policy parameters to choose a disturb-susceptible word line and safety threshold, and creates a separate refresh queue only after measured error evidence crosses that threshold.

The same source then explicitly says the refresh queue **may be stored in controller RAM or in non-volatile memory**.

That combination gives Case 52 a precise second-order retention boundary:

```text
exact accumulated READ count
    is one possible maintenance-control state
but not the only one

counter-free scan-admission policy
    + retained characterization parameters
    + sampled ECC/error evidence
    + pending refresh queue
can form a different controller state machine
```

and:

```text
maintenance policy persistence
    !=
maintenance-obligation persistence
```

The source does **not** disclose the crash/restart semantics needed to make a RAM-resident queue equivalent to a non-volatile queue. That difference is preserved as an open engineering boundary rather than silently filled in.

## Source chronology and public-date discipline

Primary family text:

- Steven T. Sprouse, Alexandra Bauche, Yichao Huang, Jian Chen, Jianmin Huang, Dana Lee, **_Flash memory with targeted read scrub algorithm_**;
- U.S. application `13/529,522`;
- filing / priority date: **21 June 2012**;
- public application: **US20130346805A1, 26 December 2013**;
- later grant: **US9053808B2, 9 June 2015**;
- Google Patents records SanDisk Technologies as the original/current assignee line for the inspected family.

Primary-family text and metadata:

- <https://patents.google.com/patent/US20130346805A1/en>
- <https://patents.google.com/patent/US9053808B2/en>

The filing date is useful as **design chronology**. The conservative public-document floor for this record is **26 December 2013**. This packet therefore does not use the June-2012 filing date to manufacture a pre-publication prior-art claim against the September-2012 FCR conference record in Case 36.

The source is a patent disclosure, not proof that a named shipping SanDisk SSD, card, USB drive, or controller used the exact embodiment, parameters, or queue-lifetime choice.

## Historical record

### H/P — the source itself contrasts per-block read counters with a counter-free scan-admission design

The background says some existing read-scrub processes copy a block after a fixed number of reads and require the Flash device to track/store multiple per-block counters. It identifies processing/storage overhead and unnecessary copying as drawbacks.

The disclosed targeted scheme can instead decide whether a read-scrub scan should occur after each host read without using stored read-counter information. One worked embodiment generates a random number and applies a frequency criterion; the example uses a one-in-1000 scan opportunity, but the source explicitly treats that number as one configurable example rather than a universal law.

Thus the period record itself supports:

```text
read-disturb maintenance
    !=
necessarily exact per-block READ-count accumulation
```

and:

```text
host READ event
    can create a probabilistic inspection opportunity
without becoming
one durable history increment
```

This does not mean the controller retains no state at all. It means one specific historical summary — an exact or deterministic read counter — can be omitted in that embodiment.

### H/P — policy parameters can be retained even when exact access history is not

The source describes manufacturer characterization of read-disturb susceptibility and then storing policy inputs in non-volatile memory, including:

- one or more word-line offsets judged especially susceptible to disturb;
- the selected read-scrub scan frequency;
- an error threshold / safety relation chosen below the ECC uncorrectable limit.

The word-line offset can be based on modeled or actual testing of a particular design or manufacturing run. The source also allows scan frequency to vary with factors such as P/E-cycle count or device fullness.

Therefore the historical mechanism does **not** have the shape:

```text
no read counter
    ->
no retained maintenance state
```

Instead it can have the shape:

```text
manufacturer characterization
    -> retained offset / frequency / threshold policy
    -> probabilistic scan admission
```

The retained policy is a model of **where and how often to look**, not an event log of every read that happened.

### H/P — one sampled region can qualify maintenance for a larger block

When a scan is admitted, the controller identifies a word line using the stored offset and can scan only one page — in the described MLC example, an upper page — rather than scanning the entire block.

The source emphasizes that designs/manufacturing runs can differ in which neighboring word line is most susceptible. The sampled page's ECC/error evidence is compared with a predetermined threshold.

If the sampled error count stays below the threshold, the source permits the controller to return to normal host-read processing without further action. If the error count crosses the threshold, the **whole physical block** can be placed in a refresh queue.

This directly establishes:

```text
sampled local error evidence
    !=
full-block error census
```

while also establishing a policy relation in which:

```text
sampled local error evidence
    can authorize
block-level maintenance obligation
```

The source does not claim the sampled page is a complete record of all disturb damage in the block.

### H/P — the error threshold is an ECC-safety / maintenance-cost policy boundary

The source explains that the threshold should be selected with a margin below the ECC uncorrectable-error limit while avoiding excessive refresh operations that would hurt performance and device life.

Its example figure uses a UECC value of 36 and a refresh threshold of 25 errors. Those figures are explicitly tied to an illustrative device-characterization example.

Therefore:

```text
error threshold
    !=
universal NAND failure constant
```

and:

```text
threshold crossing
    !=
already-uncorrectable data
```

The policy is intentionally early enough that ECC can still correct errors during later copying.

### H/P — detection and renewal are deliberately separated in time

A block whose sampled page exceeds the threshold is not necessarily copied immediately. It is placed in a refresh queue. The source says queued blocks can later be refreshed during housekeeping such as garbage collection or another background operation chosen so as not to interfere with responding to host commands.

During refresh, the data from the selected block are copied to a new block, with the device's ECC used to correct errors while copying.

Thus the source separates:

```text
hazard observed
    !=
maintenance obligation recorded
    !=
background service opportunity
    !=
renewal executed
```

This is especially important for `technical-retention`: knowing that a block should be renewed is itself a state that may need to outlive the observation that created it.

### H/P — the refresh queue may be volatile or non-volatile

The source states explicitly that the refresh queue may be stored **in controller RAM or in non-volatile memory**. It also permits FIFO handling or another selection order.

This is the narrowest and most important historical witness in this packet:

```text
same logical maintenance obligation
    can be embodied in
volatile controller RAM
or
non-volatile memory
```

The source does not specify:

- whether a RAM-resident queue is reconstructed after unexpected power loss;
- whether a queued obligation lost from RAM is rediscovered by later scans;
- whether the non-volatile form is synchronously updated;
- whether queue writes are atomic;
- what happens if power fails while queue metadata are being changed;
- whether a completed refresh and queue removal are transactionally ordered;
- whether one product implementation uses RAM, NVM, or a hybrid.

Those are intentionally left open.

### H/P — current workload can suppress a scan that would be redundant

The patent also describes an optimization in which a qualifying read-scrub scan may be skipped for sequential-read patterns when the would-be sampled neighbor has already been read and ECC-checked as part of ordinary command service.

This supplies another historical boundary:

```text
scan-frequency criterion met
    !=
scan must execute unconditionally
```

Maintenance admission can depend on evidence already obtained through ordinary service.

### H/P — wear can widen or accelerate the inspection policy

The source permits increasing scan frequency as P/E cycles increase, scanning more targeted word lines, or adding random-word-line sampling as wear grows.

This is not a proof of one shipped adaptive algorithm, but it is a period disclosure that separates:

```text
fixed physical read-disturb mechanism
    from
adaptive controller inspection policy
```

The controller's model of enough evidence can change with device condition.

## Engineering reconstruction

### E — maintenance may depend on retained policy rather than retained exact causal history

Denali's earlier inspected design gives Case 52 a direct chain:

```text
past READ events
    -> retained read count
    -> threshold
    -> relocation
```

The SanDisk targeted-scrub disclosure permits a different chain:

```text
host READ opportunity
    -> probabilistic scan decision
    -> retained susceptibility model / policy
    -> sampled ECC-error evidence
    -> queued obligation
    -> later relocation
```

The functional goal overlaps, but the retained control state is different.

Therefore:

> **future maintenance can depend on a retained model of risk without retaining an exact summary of every risk-producing event.**

This is an engineering reconstruction of the disclosed composition, not vocabulary attributed to SanDisk.

### E — forgetting access history can be intentional rather than a failure

A controller that deliberately uses counter-free probabilistic scan admission is not necessarily suffering metadata loss. The omission of per-block read counters can be an architectural choice trading exact historical accounting for sampled observation plus policy parameters.

Thus:

```text
not retaining exact READ history
    !=
necessarily losing maintenance capability
```

This conclusion is bounded to a design that still retains enough policy and obtains fresh error evidence before the ECC margin is exhausted.

It does not justify discarding arbitrary controller state.

### E — policy-state persistence and pending-work persistence have different horizons

The source describes policy parameters such as offset/frequency in non-volatile memory, while the refresh queue may instead be in RAM or NVM.

That allows a strict decomposition:

```text
risk-model / inspection-policy state
    may survive power loss

pending refresh obligation
    may or may not survive directly
    depending on queue embodiment
```

Therefore:

> **maintenance-policy persistence != pending-maintenance persistence.**

A device can reboot remembering how to detect risk while no longer directly remembering every obligation discovered before the reboot — if the queue was volatile.

Whether that is safe depends on restart/re-detection behavior that the inspected patent does not establish.

### E — discovery is not completion evidence

Once a block enters the queue, a later background copy remains to be performed. Queue membership therefore means something closer to **pending maintenance** than **completed renewal**.

```text
error threshold crossed
    -> block queued
    !=
block refreshed
```

After copying, another state transition must establish that the new block is the valid embodiment and that the pending queue item can be retired. The patent text used here does not disclose a crash-consistency protocol for that handoff.

### E — probabilistic inspection changes the meaning of “coverage”

With a deterministic read counter, one can at least describe a direct relation between counted operations and a threshold. With probabilistic scan admission, there is no guarantee that every fixed-size sequence of host reads contains exactly one scan merely because the expected frequency is one in X.

The source describes a probability-based mechanism; it does not provide a worst-case deterministic scan-gap guarantee for the random embodiment.

Therefore:

```text
expected scan frequency
    !=
deterministic maximum time/read gap between scans
```

This is a mathematical/engineering consequence of the disclosed probabilistic topology. The patent itself should not be rewritten as promising a hard deterministic coverage bound unless another source supplies one.

### E — sampled observation and repair scope need not have the same granularity

The scheme can inspect one upper page of one targeted word line and then queue the entire physical block for relocation. This means evidence granularity and action granularity differ:

```text
observation granularity
    !=
maintenance-action granularity
```

That relation is useful across the repository because many maintenance systems sample or summarize more narrowly than they act.

### E — a maintenance queue is second-order retained state

The user payload is what must remain logically recoverable. The refresh queue is instead retained information **about what must happen to the payload later**.

It is neither payload nor merely diagnostic telemetry:

```text
payload state
    !=
pending-maintenance obligation state
    !=
maintenance-completion evidence
```

Queue loss can matter even if every queued payload block is still presently ECC-correctable, because the queue encodes future work admitted before the current margin is exhausted.

Again, the patent does not show that losing a RAM queue necessarily causes data loss; re-observation may exist. The point is the state-class distinction.

## Controlled functional comparisons

### Versus the Denali 2008–2009 read-count checkpoint design

The two designs should not be merged into one genealogy.

Denali supplies an explicit persisted event-summary path:

```text
READs
    -> per-block read-count state
    -> live RAM table
    -> periodic / shutdown checkpoint
    -> power-up reload
    -> thresholded relocation
```

The SanDisk targeted-scrub disclosure supplies a counterexample:

```text
READ opportunity
    -> probability test
    -> selected targeted scan
    -> sampled bit-error threshold
    -> refresh queue
    -> later background relocation
```

The comparison supports only:

> different controllers can preserve different summaries of the past while pursuing the same broad retention objective.

It does not establish influence, descent, or product implementation.

### Versus the SanDisk 2004–2007 exposure-avoidance deepening

The earlier SanDisk-associated evidence supplies preventive topologies: withhold useful payload from repeatedly stressed neighbor geometry, deny access through mapping/policy, or change the electrical read sequence to reduce one disturb mechanism.

The 2012–2013 targeted-scrub design instead allows ordinary access-induced risk and selectively observes/repairs it later.

```text
prevent hazardous exposure
    !=
observe accumulated effect and renew
```

The shared company context is not enough to assert one product genealogy.

### Versus Case 67 — SK hynix adaptive read-reclaim

Case 67's bounded SK hynix design uses compressed read-count proxy state and measured error evidence, and can reset one proxy at power-off while compensating through conservative later checking.

The SanDisk targeted-scrub disclosure contributes a different control-state option: **avoid retaining read counters in the first place** for scan admission, while retaining susceptibility/frequency policy and optionally retaining the pending-work queue.

The controlled comparison is:

```text
resettable compressed history proxy
    !=
counter-free probabilistic inspection policy
```

Both show that maintenance can be safe only if enough later observation/control survives, but their algorithms and historical lineages are not equated.

### Versus Case 36 — Flash Correct-and-Refresh

Both can move corrected data before ECC margin is exhausted. Case 36 is primarily retention-age / wear-driven FCR; this packet is read-disturb-oriented sampled inspection.

The 21 June 2012 filing date is **not** used to claim public priority over Cai et al.'s September-2012 paper because the application was not publicly published until 26 December 2013.

### Versus distributed scrub / patrol cases

A targeted NAND read-scrub scan and a filesystem/object-store scrub can both be described functionally as maintenance observation followed by possible repair, but that analogy stops quickly.

The address geometry, evidence, failure modes, authority, redundancy source, repair operation, restart behavior, and historical genealogy differ. This packet does not use distributed-storage vocabulary to describe SanDisk's controller internals.

## Historical record / engineering reconstruction / interpretation ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| US13/529,522 was filed 21-Jun-2012 and US20130346805A1 was published 26-Dec-2013 | `H/P` | patent-family metadata |
| SanDisk is the assignee line in the inspected family record | `H/P` | patent-family metadata; not shipment evidence |
| source contrasts stored per-block read counters with a scan-admission embodiment that does not use read-counter information | `H/P` | background + description + claim 13 |
| counter-free embodiment can use probability/random-number frequency criterion per host read | `H/P` | FIG. 9 / description |
| susceptibility offset and scan frequency can be stored in non-volatile memory | `H/P` | description / claims |
| scan frequency may vary with P/E count, fullness, or other conditions | `H/P` | description |
| one targeted page/word line can supply error evidence used to queue a whole block | `H/P` | FIG. 8 / description |
| block is queued when measured errors exceed a threshold selected below UECC in the worked policy example | `H/P` | description |
| queued block can be copied to a new block later during background/housekeeping work with ECC correction | `H/P` | description |
| refresh queue may reside in controller RAM or non-volatile memory | `H/P` | FIG. 12 / description |
| RAM queue is definitely reconstructed after crash | `X` | restart semantics not disclosed |
| non-volatile queue update is synchronous/atomic after every admission | `X` | update protocol not disclosed |
| publication proves named commercial deployment | `X` | patent design != shipped product |
| one-in-1000 and example error values are universal NAND constants | `X` | worked characterization examples only |
| counter-free means no retained maintenance state | `X` | NVM policy parameters explicitly disclosed |
| one sampled page is a complete block-damage census | `X` | source explicitly performs targeted sampling |
| queue membership proves refresh completion | `X` | queue precedes later copy |
| filing date is the public-document date | `X` | application publication occurred Dec-2013 |
| exact causal history is always required for future retention work | `X/E` | counter-free sampled-control counterexample |
| maintenance-policy persistence and pending-work persistence are distinct | `E` | NVM policy parameters + RAM/NVM queue choice |
| expected probabilistic frequency is a deterministic maximum scan gap | `X/E` | no hard gap bound established in source |
| local observation granularity can differ from maintenance-action granularity | `E` | targeted page scan -> whole-block queue/copy |
| these mechanisms are equivalent to human remembering/forgetting | `X/I` | unsupported anthropomorphism |

## Philosophical interpretation — bounded

This slice supports one narrow project-level statement:

> **A technical system can preserve the ability to care for a retained object without preserving an exact history of every event that endangered it. What must survive is not “the past” in general, but enough policy, observation, and pending-work state for later operations to re-establish a safe margin.**

The RAM-versus-NVM queue choice adds a second pressure:

> **Knowing how to detect future risk and remembering already-discovered work are different retention problems.**

Those are project interpretations. The SanDisk inventors do not present the design as a theory of memory, history, or forgetting.

## Explicit non-claims

This packet does **not** claim that:

1. SanDisk invented NAND read disturb;
2. SanDisk invented read scrub;
3. US20130346805A1 is public 2012 prior art merely because it was filed in 2012;
4. the patent was implemented in a named commercial product;
5. one-in-1000 is a production parameter;
6. 25 errors or UECC 36 is a universal ECC policy;
7. every SanDisk controller omitted read counters;
8. probabilistic sampling is always safer than deterministic counting;
9. probabilistic sampling provides a hard deterministic coverage bound;
10. a targeted word line is always physically adjacent by exactly one row in every NAND design;
11. one sampled page exactly represents every error in its block;
12. queue insertion means refresh already completed;
13. background refresh is identical to garbage collection merely because it can use a housekeeping opportunity;
14. a copied block is securely erased from its old physical embodiment;
15. RAM queue loss necessarily causes data loss;
16. RAM queue contents are definitely reconstructed after reset;
17. non-volatile queue contents are necessarily crash-consistent;
18. queue insertion/removal and FTL mapping updates are one atomic transaction;
19. stored offsets/frequency constitute a complete physical-device model;
20. manufacturer's characterization parameters never change after deployment;
21. omitted read counters imply zero retained control state;
22. retained policy state is user payload;
23. pending maintenance is diagnostic-only telemetry;
24. the SanDisk design is genealogically derived from Denali;
25. the SK hynix Case 67 design descends from this patent;
26. Case 36 FCR descends from this patent;
27. NAND targeted read scrub is the same mechanism as HDFS/ZFS/Ceph scrub;
28. a probabilistic decision erases the physical effects of reads that were not sampled;
29. power loss resets read-disturb damage;
30. maintenance state has one universal persistence horizon.

## Evidence debt left open

This bounded deepening deliberately leaves the following for later work:

- exact queue-lifetime choice in a named SanDisk/Western Digital product;
- restart/recovery behavior for a RAM-resident refresh queue;
- crash consistency of a non-volatile refresh queue;
- queue-admission versus mapping-update ordering during interrupted copy/refresh;
- whether completed queue items leave management telemetry;
- exact random generator / probability implementation in shipped firmware;
- measured worst-case scan-gap behavior under probability-based admission;
- exact product-specific susceptibility offsets and thresholds;
- later SanDisk/Western Digital `Low Impact Read Disturb Handling`, background-media-scan, and patrol-read lineage;
- independent hardware validation tying read workload to queue/reclaim behavior;
- broader SanDisk controller/product genealogy, which belongs primarily in `computing-archaeology`.

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `US9053808` found no dedicated reusable packet. Keep this retention-specific distinction among counter-free scan admission, retained risk-model parameters, sampled error evidence, pending-work queue lifetime, and later re-embodiment here.

A broader history of SanDisk controller generations, patent-family relationships, SSD/card product deployment, read-scrub terminology, and the later Western Digital maintenance line belongs in `computing-archaeology` rather than being duplicated here.

## Sources

1. Steven T. Sprouse, Alexandra Bauche, Yichao Huang, Jian Chen, Jianmin Huang, Dana Lee, **_Flash memory with targeted read scrub algorithm_**, US application `13/529,522`, filed/priority 21 June 2012; US20130346805A1 published 26 December 2013; later US9053808B2 granted/published 9 June 2015; SanDisk Technologies assignee line: <https://patents.google.com/patent/US20130346805A1/en> and <https://patents.google.com/patent/US9053808B2/en>.
2. Case 52 Denali control-state comparison: [`52-denali-2008-2009-persistent-read-count-checkpoint-deepening.md`](52-denali-2008-2009-persistent-read-count-checkpoint-deepening.md).
3. Case 52 earlier SanDisk prevention comparison: [`52-sandisk-2004-2007-read-disturb-exposure-avoidance-prior-art-deepening.md`](52-sandisk-2004-2007-read-disturb-exposure-avoidance-prior-art-deepening.md).
4. Case 67 comparison: [`../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md`](../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md).
5. Case 36 comparison: [`../cases/36-nand-flash-correct-and-refresh-maintenance.md`](../cases/36-nand-flash-correct-and-refresh-maintenance.md).
