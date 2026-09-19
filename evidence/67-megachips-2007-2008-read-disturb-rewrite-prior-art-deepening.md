# Evidence Deepening — MegaChips 2007–2008 Read-Disturb Repair by Thresholded Rewrite

## Status

**`bounded deepening complete`** — manufacturer-primary patent-family evidence inspected for a pre-2009 controller design that uses read-activity / error evidence as a repair condition and can rewrite or relocate data before NAND read-disturb damage exceeds usable ECC margin.

This packet deepens [`../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md`](../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md). It is a **prior-art and terminology** slice, not a claim that the inspected design shipped in a named MegaChips product or that it is genealogically ancestral to later Samsung or SK hynix implementations.

## Research question

Case 67 already had 2009-priority Samsung evidence for an explicit `read reclaim` signal and 2013-priority Samsung evidence for BER-qualified block copying. The narrower question here is:

> Before that inspected `read reclaim` terminology, was there manufacturer-primary evidence for the same broad retention relation — repeated reads / correctable error evidence -> thresholded maintenance decision -> corrected rewrite or relocation — and, if so, what controller state and scheduling choices were already explicit?

The answer is yes, with an important vocabulary warning: the 2007-priority MegaChips family calls the work **bit-error prevention / repair / recovery / rewriting**, not `read reclaim`.

## Source hierarchy

### A — primary patent family

MegaChips, **JP2008192267A / US20080189588A1**, “Bit error prevention method and information processing apparatus.”

Inspected family records:

- Japanese filing / priority: **2007-02-07**;
- US filing: **2008-01-03**;
- US application publication **US20080189588A1**: **2008-08-07**;
- Japanese application publication **JP2008192267A**: **2008-08-21**;
- US grant **US8214720B2**: **2012-07-03**;
- the US family record names MegaChips Corporation as original/current assignee; the Japanese record identifies the predecessor MegaChips LSI Solutions entity in its assignment history.

Primary text used here comes from the English US family page and the English/translated Japanese family pages. The relevant mechanism is already present in the application-publication family; later grant language is used only where noted to clarify claim boundaries.

Sources:

- <https://patents.google.com/patent/US20080189588A1/en>
- <https://patents.google.com/patent/US8214720B2/en>
- <https://patents.google.com/patent/JP2008192267A/en>
- <https://patents.google.com/patent/JP5283845B2/en>

## Historical record

### 1. The family explicitly frames repeated reads as a NAND reliability problem

The disclosure describes NAND use in SD-card-like storage and game-machine / ROM-like workloads where application data can be read repeatedly without intervening write or erase activity. It names the resulting phenomenon `read disturb` and explains the risk that repeated selection can shift the state of unselected cells until errors exceed installed ECC capability.

The historically safe claim is therefore:

> **By the 2007-02-07 priority date, a MegaChips controller/system design explicitly treated repeated NAND reads as a maintenance problem that could require proactive rewriting.**

This is not evidence that MegaChips discovered the physical read-disturb mechanism. The disclosure itself cites earlier work, including the 2005 publication `US20050210184A1`, for avoiding read disturb at the memory-operation level.

### 2. A repair condition can be based on read count, current bit-error count, or accumulated error occurrence

The family does not expose only one trigger. It states that a threshold / repair condition can use, among other quantities:

- the **number of readouts** of stored data;
- the **number of bit errors** in data that has been read;
- the **accumulated number of occurrences of bit errors**.

For read disturb, the description specifically calls read count a suitable threshold because repeated reads create the risk condition. It also gives an ECC-margin example: if ECC can correct four bits, a threshold such as three error bits can trigger repair before the current embodiment exceeds correction capability.

This yields three distinct maintenance-evidence classes:

```text
workload evidence        = how much relevant reading has occurred
current condition evidence = how many errors are observed now
historical condition evidence = how often errors have accumulated/occurred
```

They may feed the same repair action, but they are not the same state.

### 3. Threshold crossing can trigger repair before an uncorrectable read

The disclosure explicitly describes the threshold as a trigger for rewriting temporarily held data. With a read-count threshold, rewriting can occur before any bit error has yet appeared. With an error-count threshold tied below ECC capacity, data can be corrected and rewritten while it remains recoverable.

Safe boundary:

> **maintenance threshold crossing != uncorrectable payload**.

And, in the ECC-qualified variant:

> **correctable read != sufficient reason to leave the old physical embodiment unchanged indefinitely**.

The design therefore predates the inspected 2009 Samsung `read reclaim` publication in the broader functional relation of **proactive repair while the payload remains recoverable**.

### 4. ECC correction and medium repair are separate operations

The description explicitly criticizes the ordinary situation in which ECC corrects data for output but does not repair the nonvolatile medium itself. Its repair flow can check/correct the temporary data and then write the corrected value back to nonvolatile storage.

This supplies a pre-2009 direct boundary for Case 67:

```text
successful ECC output
    !=
medium repaired for future reads
```

The later term `read reclaim` is not necessary for that engineering distinction to exist.

### 5. `Rewrite` is broader than `relocation`

The family uses broad rewrite/recovery language. The description includes a concrete block-level path in which replacement block data is written into an unused area and storage-management information is changed to point reads at the new pages. It also includes a page-level path in which the affected page is written to an unused page and the management information is changed from the old page to the new page. Another embodiment permits rewriting into another flash memory.

The later US claims also include a same-location rewrite alternative.

Therefore:

> **rewrite / repair != necessarily relocation**.

But the source also directly supports:

> **one disclosed repair path = corrected value -> unused physical area -> mapping/storage-information update -> new current embodiment**.

This is why the source belongs in Case 67's prior-art boundary even though it does not use the later `read reclaim` term.

### 6. Repair-policy metadata can itself be retained in Flash

The preferred embodiment places the threshold in the Flash **redundant area** and reads it before the protected data, for example at power-on. Thresholds can be set per page or block, and the disclosure also permits dividing memory into element areas with different thresholds according to physical characteristics or application access characteristics.

That establishes:

```text
payload data
    !=
repair-policy metadata
```

and:

```text
one global maintenance threshold
    !=
per-area maintenance policy
```

The threshold is not a physical damage measurement. It is retained policy metadata controlling when observed or accumulated evidence becomes actionable.

### 7. Retained threshold policy does not prove retained read-history state

The source is clear that the **threshold value** may be stored in the redundant area and read at power-on. It is not comparably clear, in the inspected passages, that every comparison value — especially a running read-count history — survives power removal in a particular persistent counter format.

So the evidence supports:

> **persistent repair threshold != proven persistent read-count history**.

This is a useful contrast with the later SK hynix 2017-priority design, which explicitly discusses clearing its read-count proxy at power-off and compensating by conservative requalification. MegaChips 2007–2008 instead gives direct evidence for retained threshold policy and multiple scheduling modes, but this packet does **not** infer an undocumented power-fail lifetime for the accumulated count itself.

### 8. Maintenance can be admitted inline or by scheduled scanning

The disclosure gives two broad admission modes.

First, repair can be integrated into an ordinary host-read path: data is read into temporary storage, checked/corrected, compared with the repair condition, and rewritten if necessary.

Second, the system can proactively read all or part of the storage area at a predetermined time and perform rewrite work. Named opportunities include:

- power-on;
- power-off;
- idle / low-access-load periods;
- sleep;
- charging;
- periodic execution;
- externally instructed execution.

This yields another boundary:

```text
repair trigger condition
    !=
repair scheduling opportunity
```

A condition may define **which data needs repair** while a scheduling policy defines **when the system is willing to pay the work**.

### 9. Coverage state can be retained separately from the payload

For partial rather than whole-memory maintenance passes, the source says information about the area already/next subject to read access can itself be stored in memory area, redundant area, controller nonvolatile memory, host state, or other Flash. It also describes dividing the full area and covering the pieces across multiple maintenance occasions.

Thus a maintenance pass may require a distinct traversal relation:

```text
payload currentness
    !=
repair-policy threshold
    !=
maintenance coverage / traversal state
```

The source does not define one universal checkpoint format for that coverage state; it merely establishes that the design recognizes coverage metadata as a separable concern.

## Engineering reconstruction

### A. `Read reclaim` is one later vocabulary for a broader older maintenance relation

The 2007-priority MegaChips family supports this functional chain:

```text
repeated reads and/or observed correctable errors
    -> compare against repair condition
    -> optionally ECC-correct current value
    -> rewrite value
    -> optionally update mapping to a new physical embodiment
```

Samsung's 2009-priority family later exposes a `read reclaim` signal and block reassignment before ECC failure. SK hynix's 2017-priority family later composes read-count proxies, test reads, adaptive thresholds, 3-D sampling, and conditional reclaim.

The safe historical conclusion is **not** that these later designs descend from MegaChips. It is:

> the broad function `read-disturb evidence -> proactive corrected rewrite / re-embodiment` is directly documented before the inspected 2009 `read reclaim` terminology.

### B. Policy, evidence, scheduling, and repair carrier are four separate states

The MegaChips source makes it unusually easy to keep four layers apart:

1. **policy** — the threshold / repair condition;
2. **evidence** — read count, bit-error count, accumulated error occurrence;
3. **schedule / coverage** — inline host-read admission, power-on/off scan, idle work, partial-area traversal;
4. **repair carrier** — corrected temporary data and the destination / mapping update used to establish the renewed embodiment.

Conflating these produces bad claims such as “the threshold is the read history” or “a background scan is the repair condition.” Neither is source-supported.

### C. A successful logical read can simultaneously be evidence for future physical work

In the ordinary host-read path, the same read operation can both satisfy the immediate request and generate/combine evidence that causes maintenance. This yields:

> **foreground success != no background/maintenance consequence**.

Case 67's later SK hynix design expresses the same broad retention pressure with different controller machinery and a more explicit two-stage `count -> test -> reclaim` composition.

### D. Repair can be proactive without being instantaneous

The source permits maintenance at power-on/off, idle, sleep, charge, or other low-load times. Therefore a thresholded need for repair does not imply that every implementation must synchronously relocate data before returning the triggering host read.

Safe relation:

```text
maintenance need recognized
    !=
maintenance work necessarily completed at the same instant
```

The exact crash-consistency semantics of a delayed or interrupted rewrite are outside this source slice.

## Functional comparison

### Versus Case 67's SK hynix 2017-priority design

MegaChips 2007–2008:

```text
repair threshold
    <- read count OR bit-error count OR accumulated error occurrence
    -> rewrite / optional relocation
```

SK hynix 2017–2019:

```text
compressed read-count proxy
    -> scheduled test read
    -> measured ECC/bit-error evidence
    -> adaptive future threshold
    -> conditional reclaim
```

The later composition separates proxy-triggered **qualification** from reclaim more explicitly and adds 3-D neighborhood sampling and an explicit power-off-reset policy for the proxy. The earlier MegaChips design already demonstrates thresholded proactive rewrite and per-area policy, but it does not establish those later details.

### Versus Samsung 2009-priority read-reclaim signal

Samsung's inspected family gives a named `read reclaim` indicator tied to an error threshold below maximum ECC capability and subsequent block reassignment. MegaChips's earlier family uses `repair`, `recovery`, and `rewrite` language.

Therefore:

> **terminology floor != functional-mechanism floor**.

The repository should not date the broad maintenance relation merely by the first inspected occurrence of the phrase `read reclaim`.

### Versus Case 36 — Correct-and-Refresh

Both cases can express `correct -> rewrite`, but their bounded triggers differ. Case 36 centers retention/wear maintenance; this packet centers read-disturb / read-workload and error evidence. Similarity of repair action does not collapse the failure clocks.

### Versus Case 52 — physical read disturb

Case 52 supplies physical/read-disturb evidence and characterization. This packet is controller/system prior art for deciding when to rewrite. It does not replace physical characterization, nor does a patent threshold establish a universal NAND disturb limit.

### Versus Case 04 — logical identity across relocation

The block/page rewrite variants that update storage-management information provide another concrete example of logical identity surviving a change in physical carrier. That is a functional bridge only; Case 04 remains the generic mapping case.

### Versus Case 150 — SSD garbage collection

Both can move valid data into other physical space, but the admission evidence differs:

```text
read-disturb repair: reliability evidence authorizes re-embodiment
capacity GC: reclamation / free-space pressure authorizes movement
```

Shared copy/erase machinery does not make the triggers synonymous.

## Philosophical interpretation — bounded

This slice supports only a narrow systems claim:

> **Retention policy can itself be a retained object.** A system may preserve not just user data, but thresholds and coverage information that determine when future evidence is strong enough to justify rewriting that data.

That does not make policy metadata equivalent to the payload, and it does not imply that every causal history must be preserved. In fact, the source leaves the exact persistence of the running read-history comparison value under-specified while explicitly retaining threshold policy.

## Explicit non-claims

This packet does **not** establish any of the following:

1. MegaChips invented NAND read disturb.
2. MegaChips invented all forms of refresh, scrubbing, reclaim, ECC repair, or Flash relocation.
3. `JP2008192267A` is the first historical system ever to rewrite NAND because of read disturb.
4. The 2007 priority date means the public could read the patent text in 2007; the US and JP application publications inspected here are from August 2008.
5. A patent filing proves a named shipping MegaChips controller or game cartridge implemented the mechanism.
6. Every repair threshold is a read-count threshold; the disclosure gives several evidence types.
7. A threshold value is a direct measurement of cell charge or threshold-voltage distribution.
8. The threshold stored in the redundant area proves that the running read-count comparison value is also persistent across power loss.
9. Every rewrite is a physical relocation; same-location rewrite is also contemplated.
10. Every relocation immediately erases or sanitizes the old physical data.
11. Power-on/off scanning proves one exact boot/shutdown implementation in a shipping product.
12. A power-off maintenance opportunity implies that work always finishes before loss of power.
13. ECC correction by itself repairs NAND cell state.
14. Correctable data necessarily has adequate future retention margin without rewrite.
15. The per-area threshold is a universal physical endurance constant.
16. The cited ECC example (`4` correctable, threshold `3`) is a universal production setting.
17. MegaChips 2007–2008 is genealogically ancestral to Samsung 2009, SK hynix 2017, or Samsung PM963 firmware.
18. Similarity to Case 36 proves the same failure mechanism.
19. Similarity to garbage collection proves capacity reclamation and reliability repair are the same operation.
20. This source establishes crash atomicity of mapping handoff during an interrupted rewrite.

## Claim ledger

| ID | Claim | Layer | Evidence strength |
| --- | --- | --- | --- |
| G-67.31 | MegaChips family priority is 2007-02-07; US application publication is 2008-08-07 and JP publication is 2008-08-21 | `H` | high — family bibliographic records |
| G-67.32 | The disclosure explicitly frames repeated NAND reads as capable of producing read-disturb errors | `H/P` | high — background description |
| G-67.33 | Repair conditions can use read count, bit-error count, or accumulated bit-error occurrence | `H/P` | high — abstract, description, claims |
| G-67.34 | Correctable/error-free data can be rewritten proactively before an uncorrectable condition | `H/P` | high — description |
| G-67.35 | The described flow can ECC-correct temporary data before rewriting it | `H/P` | high — description/claims |
| G-67.36 | A disclosed block/page repair path writes into unused physical space and updates storage-management information | `H/P` | high — description |
| G-67.37 | Rewrite is not synonymous with relocation because same-location rewrite is also contemplated | `H/P` | high — US claims |
| G-67.38 | A preferred embodiment stores repair threshold policy in Flash redundant area and can read it at power-on | `H/P` | high — description |
| G-67.39 | Threshold policy may vary by page/block/element area | `H/P` | high — description and granted claim boundary |
| G-67.40 | Maintenance may run inline with host reads or at power-on/off, idle, sleep, charging, periodic, or external-command opportunities | `H/P` | high — description/claims |
| G-67.41 | The source recognizes separately stored coverage/area information for partial maintenance passes | `H/P` | high — description |
| G-67.42 | Retained threshold metadata proves retained running read-count history across power loss | `X` | not established |
| G-67.43 | The broad functional relation `read-disturb evidence -> proactive rewrite / relocation` is documented before the inspected 2009 Samsung `read reclaim` terminology | `E/H` | high for chronology + functional comparison; no genealogy claimed |
| G-67.44 | MegaChips 2007 is the historical origin of read reclaim | `X` | unsupported |
| G-67.45 | Patent disclosure proves named-product deployment | `X` | unsupported |

## Prior-art and terminology boundary

The inspected chronology should now be expressed as:

```text
2007-02-07  MegaChips priority:
            read-disturb / bit-error repair condition;
            read-count or error-based thresholds;
            corrected rewrite / optional relocation

2008-08     MegaChips US and JP application publications

2009-03-12  Samsung priority:
            explicit read-reclaim indication below ECC limit;
            affected-block reassignment

2013-02-19  Samsung priority:
            BER/read-voltage-qualified read reclaim;
            copying to another block; endurance cost

2017-08-31  SK hynix priority:
            compressed read-count proxy;
            adaptive test cadence;
            3-D neighborhood sampling;
            conditional read reclaim
```

Two timing rules matter:

```text
priority / filing date
    !=
public publication date
```

and:

```text
first inspected use of a term
    !=
first inspected instance of the broader function
```

This packet therefore lowers Case 67's **inspected functional prior-art floor** for thresholded read-disturb repair/re-embodiment from the previous 2009-priority Samsung family to the 2007-priority / 2008-public MegaChips family. It does not establish absolute invention priority.

## Related-repository boundary

A current repository search found no `JP2008192267`, `US8214720`, or `MegaChips read disturb` packet in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology).

The retention-specific seam stays here:

```text
read-workload / error evidence
    -> repair policy threshold
    -> maintenance scheduling / coverage
    -> corrected rewrite
    -> optional physical re-embodiment
```

A broader history of MegaChips controller products, game-cartridge deployments, SD-controller generations, patent genealogy, and vendor adoption belongs in `computing-archaeology` if pursued.

## Remaining evidence debt

This slice does **not** close the following Case 67 gaps:

- named shipping product evidence for a disclosed trigger algorithm;
- exact production thresholds and counter persistence;
- independent power-cycle / fault-injection validation;
- crash consistency of mapping/currentness handoff during reliability relocation;
- cross-vendor product-level comparison of how read-reclaim counters are exposed;
- pre-2007 direct evidence for the narrower combination of **read-disturb evidence plus corrected rewrite/relocation**;
- a demonstrated genealogy connecting MegaChips 2007, Samsung 2009/2013, and SK hynix 2017.

## Sources

1. MegaChips Corporation, **US20080189588A1, “Bit error prevention method and information processing apparatus,”** priority 7 February 2007, filed 3 January 2008, published 7 August 2008; later granted as US8214720B2 on 3 July 2012: <https://patents.google.com/patent/US20080189588A1/en>
2. MegaChips Corporation, **US8214720B2, “Bit error prevention method and information processing apparatus,”** family/grant text used for claim-boundary checking: <https://patents.google.com/patent/US8214720B2/en>
3. MegaChips LSI Solutions / MegaChips family, **JP2008192267A, “Method of preventing bit error, and information processing device,”** filed/priority 7 February 2007, published 21 August 2008: <https://patents.google.com/patent/JP2008192267A/en>
4. Same Japanese family, **JP5283845B2**, later grant used to cross-check the threshold / ECC-margin / scheduling passages: <https://patents.google.com/patent/JP5283845B2/en>
