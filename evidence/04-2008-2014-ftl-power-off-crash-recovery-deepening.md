# Evidence 04C — FTL Power-Off Recovery: Mapping Persistence, Checkpoints, and Reconstructed Authority (2008–2014)

## Status

**`bounded deepening complete`** for the 2008–2014 FTL power-off/crash-recovery slice described here.

This packet deepens [`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md). It does not replace the case's 1993–1995 mapping evidence and does not claim a universal SSD power-loss algorithm.

## Research question

Case 04 already established that a stable logical identity can survive physical relocation only because mapping/allocation state tells the system which physical embodiment currently counts.

The remaining crash-boundary question was narrower:

> What happens when user pages have been written to NAND, but newer FTL mapping/control state exists only in volatile RAM when power is lost?

The bounded result is:

```text
physical payload survival
    !=
volatile mapping-cache survival
    !=
persistent recovery evidence
    !=
post-restart reconstructed mapping authority
```

A system can therefore lose the **current in-memory description of logical identity** without necessarily losing every physical page that participated in the pre-crash history.

## Why this slice is separate from ordinary NAND retention

This packet is about metadata currentness across an execution boundary, not about charge leakage over months or years.

It must not collapse these two questions:

```text
Will programmed cell state remain readable after power removal?

versus

After an interrupted sequence of writes / remaps / reclamation,
which surviving physical pages should the FTL expose as current?
```

The first belongs primarily to media-retention physics. The second is a crash-consistency / recovery-authority problem in the mapping layer.

---

## Source custody and quality

### 1. PORCE — 2008 peer-reviewed journal article

Tae-Sun Chung, Myungho Lee, Yeonseung Ryu, and Kangsun Lee, **“PORCE: An efficient power off recovery scheme for flash memory,”** *Journal of Systems Architecture* 54(10), 2008, pp. 935–943, DOI `10.1016/j.sysarc.2008.03.007`.

Inspected public evidence:

- bibliographic record in DBLP;
- public abstract/metadata preserved by ResearchGate;
- later peer-reviewed summaries used only where the original full article was not publicly inspectable in this pass.

The inspected original abstract states that many FTL algorithms lacked a power-off recovery module, proposes PORCE, says it is tightly coupled to FTL operations, and says it minimizes normal-operation degradation by storing as little recovery information as possible.

A 2021 peer-reviewed paper by Park et al. summarizes the PORCE reclamation path more specifically: a reclamation-start log is written before reclamation and a reclamation-commit log after it in a transaction-log area in flash. Because that exact protocol detail was not inspected in the original 2008 full text during this pass, this packet labels the detail **H/S**, not H/P.

### 2. DCR — 2014 DAC paper, directly inspected full text

Chi Zhang, Yi Wang, Tianzheng Wang, Renhai Chen, Duo Liu, and Zili Shao, **“Deterministic Crash Recovery for NAND Flash Based Storage Systems,”** DAC 2014, pp. 148:1–148:6, DOI `10.1145/2593069.2593124`.

Inspected public full-text mirror:

- <https://picture.iczhiku.com/resource/ieee/wYiSoORpWfslrvmm.pdf>

The retrieved PDF text carries the authors, ACM DAC 2014 copyright notice, conference dates, and six-page paper text. The web screenshot service returned a cache-miss while this packet was prepared, so claims below rely on the successfully retrieved text layer rather than a claim of fresh image-level facsimile inspection.

Authoritative metadata was corroborated through IEEE Xplore and the Hong Kong Polytechnic University Scholars Hub.

Relevant directly inspected locations:

- p. 1: abstract and introduction;
- p. 2: FTL architecture and mapping-strategy discussion;
- pp. 2–3: motivational checkpoint/crash example and beginning of DCR recovery procedure.

### 3. Later comparison source — 2021 FAST hybrid-mapping recovery paper

Jong-Hyeok Park, Dong-Joo Park, Tae-Sun Chung, and Sang-Won Lee, **“A Crash Recovery Scheme for a Hybrid Mapping FTL in NAND Flash Storage Devices,”** *Electronics* 10(3), 2021, article 327, DOI `10.3390/electronics10030327`.

This open-access peer-reviewed paper is used only to clarify the historical literature boundary around PORCE and to show that crash recovery remains mapping-architecture-specific. It is not projected backward into the 2008 implementation.

---

## Historical record

### H/P — by 2008 power-off recovery was an explicit FTL research problem

The PORCE article's abstract describes an FTL power-off recovery module as an important issue for portable flash devices and proposes a recovery scheme tightly coupled to FTL operations.

This is enough to establish a dated historical fact:

```text
FTL mapping / reclamation machinery
    had acquired an explicit
power-off recovery problem
    by 2008
```

It is **not** enough to claim that PORCE was the first such scheme, that all shipping products lacked recovery before 2008, or that the paper's implementation represented commercial SSD firmware.

### H/P — DCR 2014 explicitly makes mapping metadata a crash-recovery object

The DCR paper states that an FTL manages flash using metadata such as address-mapping tables and that correct storage/access depends on this metadata.

It therefore defines its recovery target as **FTL metadata consistency**, not merely readability of NAND cells.

The paper is unusually useful for Case 04 because it writes the dependency in operational terms:

```text
correct flash pages
    are not enough by themselves;

upper layers rely on
correct FTL metadata
    to find the correct data.
```

This is direct historical/engineering evidence for the distinction Case 04 previously inferred from mapping architecture.

### H/P — DCR distinguishes volatile current metadata from durable checkpoint state

In DCR's motivational example, FTL metadata including block mapping and related state is cached in RAM during normal operation and periodically flushed to a reserved area in flash.

At the crash point, the up-to-date in-RAM mapping may be newer than the last durable checkpoint. After power failure the volatile version is gone, and restart begins from the durable checkpoint.

The paper's Figure 2 discussion explicitly says the updated FTL metadata in RAM is lost with power failure and that the system restarts from the last checkpoint.

That produces a clean retention boundary:

```text
latest volatile mapping state
    !=
latest durable mapping checkpoint
```

and, more importantly:

```text
loss of latest volatile map
    !=
loss of all on-flash evidence needed for recovery
```

### H/P — recovery can re-establish mapping currentness by inspecting surviving on-flash evidence

DCR reconstructs the post-crash state from the last checkpoint plus a bounded inspection of blocks that could have changed after that checkpoint.

For its block-level FTL, the paper exploits deterministic allocation behavior. Rather than scanning every block, it starts from the location implied by the last checkpoint/allocation strategy and inspects a limited region.

The recovery logic reads page spare areas, obtains logical page numbers, derives logical block numbers, and updates metadata accordingly.

The paper separately handles:

- regular writes;
- a special garbage-collection case;
- wear-leveling-related recovery.

That is direct evidence that **recovery authority is reconstructed from multiple retained traces**, not merely copied back from one perfect pre-crash RAM table.

### H/P — DCR's evaluated result is recovery of FTL metadata consistency, not a media-retention experiment

The DAC paper reports an ARM11-based evaluation and compares DCR with a version-based recovery scheme. The abstract says the system can recover FTL metadata consistently; the paper reports reduced recovery time, including one 128-GB Postmark example in which DCR recovers metadata faster than the comparison scheme.

The result should be read narrowly:

- it is evidence about a particular research FTL/recovery design;
- it is not evidence that every host write was durable at an arbitrary crash instruction;
- it is not evidence about long-term NAND charge retention;
- it is not a universal SSD recovery-time bound.

### H/S — PORCE's reclamation protocol treats maintenance interruption as a metadata-ordering problem

Park et al. (2021), while reviewing prior work, describes PORCE as dividing FTL writes into cases with and without reclamation and says its reclamation path writes a reclamation-start log before the operation and a reclamation-commit log afterward in a flash transaction-log area.

Because this pass did not inspect the complete 2008 article, the safe use of this detail is:

> later peer-reviewed literature reports that PORCE persisted explicit recovery markers around reclamation.

It is not promoted here to direct 2008 full-text evidence.

Still, the architectural boundary is useful:

```text
reclamation operation
    !=
proof that reclamation completed
```

A retained marker can participate in deciding whether an interrupted maintenance transition should be replayed, completed, rolled back, or otherwise repaired.

---

## Engineering reconstruction

### E — mapping persistence has at least four layers

The DCR evidence supports a finer decomposition than Case 04 previously used:

```text
1. user-data pages / blocks in NAND

2. volatile in-RAM mapping/control state

3. durable recovery evidence
   checkpoint + on-flash metadata / page spare information

4. reconstructed post-restart mapping state
```

These layers can have different lifetimes and different authority.

The key point is not that layer 3 always has one universal format. It is that a practical FTL crash-recovery design needs **some retained evidence strong enough to decide what the new authoritative mapping should be** after layer 2 disappears.

### E — exact runtime-state continuity is not required for logical-identity continuity

DCR does not require the old RAM mapping object itself to survive power failure.

Instead:

```text
old runtime map disappears
    +
durable checkpoint survives
    +
post-checkpoint physical traces survive
    +
recovery procedure re-observes/replays them
        ->
new runtime map
```

Therefore:

> **logical-address continuity can survive loss of the exact volatile data structure that previously implemented it.**

This is a stronger and more precise statement than saying merely that “the map is persistent.”

### E — a checkpoint is recovery evidence, not automatically the latest truth

The last checkpoint can intentionally lag the crash point.

Thus:

```text
last durable checkpoint
    !=
complete current mapping at the instant before crash
```

Its authority is conditional: it is a known-good prefix/base from which newer surviving effects must be discovered or replayed.

That distinction matters for retention vocabulary. A persistent object can be authoritative for **where recovery starts** without being authoritative for **the final recovered state**.

### E — physical persistence can preserve conflicting-looking historical embodiments

Out-of-place update means a crash may leave multiple physically readable pages or blocks associated with the history of one logical object.

The recovery problem is not just “find a readable copy.” It is:

- identify which writes completed far enough to count;
- identify which mappings/allocation transitions are current;
- reject stale or intermediate embodiments;
- rebuild a consistent logical-to-physical relation.

So:

```text
more surviving physical traces
    !=
more immediately usable logical state
```

Without ordering/currentness evidence, additional persistent pages can increase ambiguity rather than resolve it.

### E — recovery work is not the same thing as retained state

DCR's scan/replay procedure is active work performed after restart.

It should not be described as though the NAND “remembered the mapping by itself.”

A more exact relation is:

```text
retained checkpoint + metadata traces
    --interpreted by recovery algorithm-->
reconstructed mapping state
```

The retained evidence constrains the answer; software labor turns that evidence back into an operational map.

### E — crash consistency and cell retention are orthogonal enough to fail separately

Two distinct failures are possible in principle:

```text
A. cells lose readability
   while mapping metadata is internally consistent

B. cells/pages remain readable
   while mapping/currentness metadata is inconsistent
```

Case 04 is about B in this packet.

Cases on read disturb, early retention loss, ECC, and refresh address A or related media-integrity problems. Neither problem subsumes the other.

---

## Controlled functional comparisons

### A — checkpoint/replay resemblance to journals or logs

DCR's checkpoint plus reconstruction pattern has a functional resemblance to other crash-recovery systems that keep a durable base and reconstruct later state from surviving evidence.

That resemblance is limited to this shape:

```text
stable recovery base
    +
newer durable evidence
    +
restart-time reconstruction
```

It does **not** establish genealogy or identical transaction semantics between an FTL, a filesystem journal, or a database WAL.

### A — reconstructible runtime state in distributed/storage cases

Other cases in this repository show volatile maintenance or control state being recreated from stronger persistent evidence after restart.

Case 04 now joins that cross-case family in a specific way:

```text
volatile L2P / block-map state
    can disappear
while
persistent mapping evidence + physical state
    can be sufficient to reconstruct a new map
```

The comparison should remain functional. No common historical lineage is claimed.

### Limit — DCR is not a universal FTL model

The 2014 implementation is block-level and deliberately exploits deterministic allocation behavior.

Modern page-level, hybrid, log-structured, zoned, open-channel, controller-specific, or encrypted SSD architectures may retain different metadata and use different recovery strategies.

The general lesson is therefore not:

> all FTLs recover exactly like DCR.

It is:

> an FTL's logical identity can depend on crash-recoverable metadata whose volatile working representation and durable recovery representation are different objects.

---

## Philosophical / media-theoretical interpretation

### I — persistence of inscription is not persistence of addressability

The project-level interpretive consequence is constrained by the engineering record:

- pages may still physically exist;
- the volatile map that made them immediately addressable may not;
- retained checkpoint/metadata traces can allow addressability to be reconstructed.

So:

```text
persistence of physical inscription
    !=
persistence of immediately usable logical identity
```

This is a downstream interpretation, not wording attributed to Chung, Zhang, or the historical actors.

### I — continuity can depend on recoverable evidence rather than uninterrupted state

A stronger bounded interpretation is:

> continuity need not mean one control representation remains present without interruption; it can mean enough evidence survives for a successor representation to be reconstructed under the system's rules.

This should not be universalized into a metaphysics of identity. It is one technical pattern demonstrated by a mapped nonvolatile-storage system.

---

## Explicit non-claims

This packet does **not** claim that:

1. PORCE was the first FTL power-loss recovery scheme.
2. DCR was the first crash-recovery idea in flash storage merely because its authors describe a deterministic approach as first.
3. every commercial SSD in 2008 or 2014 used PORCE or DCR.
4. every FTL keeps the full mapping table in DRAM.
5. every FTL periodically flushes metadata in the same format or cadence as DCR.
6. every mapping update is atomically durable after the data page program finishes.
7. physical survival of a newly written page means the host write is committed.
8. physical survival of an old page means that page is still logically current.
9. the last checkpoint is necessarily the final recovered mapping.
10. checkpoints alone are sufficient without any newer recovery evidence.
11. page spare/OOB metadata has the same schema on all NAND devices.
12. DCR's deterministic allocation assumption applies to every later SSD firmware.
13. scanning a bounded number of blocks is always faster on every capacity/workload.
14. the reported 128-GB recovery time is a modern SSD guarantee.
15. FTL crash recovery proves long-term NAND retention.
16. NAND retention specifications prove crash-consistent mapping updates.
17. a clean filesystem journal can repair inconsistent lower-layer FTL metadata.
18. FTL crash recovery and filesystem crash recovery are the same layer.
19. PORCE's later-described start/commit markers have been directly re-inspected in the original 2008 full text in this pass.
20. a transaction-log analogy proves database-style ACID semantics.
21. stale physical pages are necessarily forensically recoverable.
22. mapping reconstruction implies secure deletion failure.
23. reconstruction always restores the exact old RAM bit pattern.
24. recovery is passive; it is active controller/software work.
25. `nonvolatile` means `self-describing`.
26. `persistent metadata` means every intermediate metadata write is crash-atomic.
27. remapping, garbage collection, wear leveling, and crash recovery are interchangeable terms.
28. the block-level DCR design is genealogically descended from Ban's 1993 patent merely because both use mappings.
29. this packet establishes a complete FTL history.
30. this packet establishes vendor firmware behavior for a named shipping SSD.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| PORCE is a 2008 Journal of Systems Architecture article proposing an FTL power-off recovery scheme | H/P | article metadata + inspected abstract |
| PORCE's abstract says the scheme is tightly coupled to FTL operations and stores limited recovery information | H/P | inspected abstract |
| Later literature reports reclamation-start and reclamation-commit logs for PORCE | H/S | Park et al. 2021 review of prior work; original 2008 full text not inspected here |
| DCR 2014 treats address mappings and related FTL metadata as direct crash-recovery objects | H/P | directly inspected DAC paper |
| DCR caches FTL metadata in RAM and periodically flushes it to a reserved flash area | H/P | DAC paper §2.3 |
| The updated in-RAM metadata can be lost at power failure while the last durable checkpoint remains | H/P | DAC Figure 2 discussion |
| DCR reconstructs post-checkpoint mapping state from the checkpoint plus bounded inspection of surviving blocks/page metadata | H/P | DAC §2.3 and §3.1 |
| DCR handles regular operations, a special garbage-collection case, and wear-leveling recovery separately | H/P | DAC §3.1 |
| Exact volatile mapping-state persistence is unnecessary if sufficient durable reconstruction evidence survives | E | reconstruction from DCR mechanism |
| A durable checkpoint is automatically identical to the final recovered map | X | contradicted by DCR's post-checkpoint reconstruction |
| Physical payload survival automatically proves logical currentness | X | contradicted by mapping/recovery dependency |
| FTL crash recovery is the same phenomenon as NAND charge retention | X | category error; explicitly separated |

---

## What this closes in Case 04

The previous canonical case deliberately left this debt open:

> add power-failure / atomicity evidence before making claims about mapping-update crash consistency.

This packet closes the **minimum direct-evidence gap** for saying:

```text
volatile current mapping can be lost at power failure;
checkpoint / on-flash metadata can survive;
recovery can reconstruct a new authoritative mapping.
```

It does **not** close all atomicity questions. In particular, it does not establish a universal ordering contract for:

- user-data program completion;
- mapping-page program completion;
- cache flush completion;
- garbage-collection victim erase;
- controller capacitor/PLP behavior;
- host FLUSH/FUA semantics;
- torn-program behavior at arbitrary NAND program boundaries.

Those remain separate, more hardware/controller-specific slices.

---

## Remaining evidence debt

High-value next steps are now narrower:

1. inspect the original PORCE 2008 full text and replace the H/S reclamation-log statement with page-anchored H/P evidence if available;
2. add a named shipping controller/SSD document describing mapping-table persistence or rebuild after unsafe power loss;
3. add standards-level host durability semantics (for example, SATA/NVMe flush/power-state guarantees) as a **separate layer**, not as FTL-internal proof;
4. add a controlled fault-injection paper that distinguishes lost host data from surviving-but-unmapped physical pages;
5. compare a page-mapped and block-mapped FTL recovery design without generalizing one metadata layout to the other;
6. keep media-retention/read-disturb/refresh evidence in their own cases rather than importing them into crash consistency.

---

## Related-repository routing

A search of `tmzncty/computing-archaeology` for `flash translation layer` and `NAND FTL power recovery` found no dedicated packet to reuse in this pass.

The division of labor remains:

- `technical-retention`: mapping-currentness, crash-recovery evidence, retained/reconstructed authority;
- `computing-archaeology`: broader NAND/FTL/controller chronology, vendor genealogy, standards adoption, and product history.

No broad FTL genealogy is duplicated here.

---

## References

### Primary / direct research sources

1. Tae-Sun Chung, Myungho Lee, Yeonseung Ryu, Kangsun Lee, **“PORCE: An efficient power off recovery scheme for flash memory,”** *Journal of Systems Architecture* 54(10), 2008, pp. 935–943. DOI: <https://doi.org/10.1016/j.sysarc.2008.03.007>. Bibliographic record: <https://dblp.org/rec/journals/jsa/ChungLRL08>.
2. Chi Zhang, Yi Wang, Tianzheng Wang, Renhai Chen, Duo Liu, Zili Shao, **“Deterministic Crash Recovery for NAND Flash Based Storage Systems,”** DAC 2014, pp. 148:1–148:6. DOI: <https://doi.org/10.1145/2593069.2593124>. Institutional metadata: <https://research.polyu.edu.hk/en/publications/deterministic-crash-recovery-for-nand-flash-based-storage-systems/>. Public full-text mirror inspected: <https://picture.iczhiku.com/resource/ieee/wYiSoORpWfslrvmm.pdf>.

### Secondary / later boundary source

3. Jong-Hyeok Park, Dong-Joo Park, Tae-Sun Chung, Sang-Won Lee, **“A Crash Recovery Scheme for a Hybrid Mapping FTL in NAND Flash Storage Devices,”** *Electronics* 10(3), 2021, 327. DOI: <https://doi.org/10.3390/electronics10030327>.

## Final bounded result

The new retention distinction is:

```text
retained payload
    !=
retained mapping working state
    !=
retained recovery evidence
    !=
reconstructed post-crash authority
```

Mapped flash can preserve logical identity across power loss even when the exact volatile map disappears—but only if enough stronger evidence survives for a recovery procedure to decide again which physical embodiment counts.