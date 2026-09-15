# Case 65 deepening — Toshiba / Toshiba Memory age-aware NAND read tracking and reference-time metadata (2014–2018)

## Status

**`bounded deepening complete`** — closes part of Case 65's manufacturer-design-witness debt at the **patent / disclosed-controller-design** level. It does **not** establish that a named retail SSD shipped this exact policy, that Toshiba's design is ReMAR, or that the disclosed reference-time bookkeeping is crash-atomic under arbitrary power loss.

This record adds a manufacturer-primary design witness for a controller that makes elapsed-time information part of NAND read-voltage tracking and, importantly for this repository, exposes two different persistence horizons for the control metadata: reference-time records can reside in nonvolatile memory while the controller loads working copies into volatile memory after power-on.

The narrow result is:

```text
nonvolatile reference-time / management record
    -> power-on load into controller working memory
    -> elapsed-time reconstruction
    -> word-line / time / count-conditioned tracking choice
    -> read-voltage search / tracking
```

That is evidence for **age-aware interpretation state**. It is not evidence for physical refresh.

---

## Research question

Case 65 already grounds Luo et al.'s 2018 **Retention Model Aware Reading (ReMAR)** research proposal, where retained program-time information helps select a more appropriate read reference for an aged 3D NAND embodiment.

The remaining question for this slice is narrower:

> Can manufacturer-primary material show a real NAND-controller design in which elapsed-time metadata is retained and then used to constrain read-voltage tracking, without silently upgrading a patent disclosure into shipped-product evidence or collapsing it into ReMAR?

The Toshiba / Toshiba Memory patent record provides such a bounded witness.

---

## Source roles

### P1 — Toshiba Corp, US9251892B1, 2016

**Shohei Asami, Toshikatsu Hida, Tokumasa Hara, Riki Suzuki, _Memory system and method of controlling nonvolatile memory_, US9251892B1.**

- priority: **2014-09-11**;
- filed: **2015-03-03**;
- published / granted: **2016-02-02**;
- original assignee: **Toshiba Corp**;
- current assignee shown by Google Patents: Kioxia Corp.

Primary public record: <https://patents.google.com/patent/US9251892B1/en>.

Evidence role: **manufacturer-primary adaptive-read-tracking precursor**. It shows that Toshiba publicly disclosed controller-side read-voltage tracking before the 2018 ReMAR paper. It is not used as an age-aware-retention design unless the source itself supplies elapsed-time semantics.

### P2 — Toshiba Memory Corp, US20180277227A1 / US10586601B2

**_Semiconductor memory device and read control method thereof_.**

- claims priority from Japanese Patent Application **2017-058897**, filed **2017-03-24**;
- US application record: filed **2018-03-01**;
- US publication **US20180277227A1**: **2018-09-27**;
- later US grant **US10586601B2**: **2020-03-10**;
- assignee in the later US record: **Toshiba Memory Corporation**.

Public application record: <https://patents.justia.com/patent/20180277227>.

Evidence role: **manufacturer-primary age-aware read-control design witness**. The claims directly make elapsed time and word-line identity inputs to a read-voltage tracking process. The detailed embodiment further describes reference-time records, access counters, power-on loading of management state, and tracking after ECC/error evidence.

### S1 — Luo et al., 2018

Yixin Luo, Saugata Ghose, Yu Cai, Erich F. Haratsch, Onur Mutlu, **“Improving 3D NAND Flash Memory Lifetime by Tolerating Early Retention Loss and Process Variation,”** *Proceedings of the ACM on Measurement and Analysis of Computing Systems* 2(3), Article 37, 2018, DOI `10.1145/3224432`.

Author-accessible text: <https://arxiv.org/abs/1807.05140>.

Evidence role: **scholarly experimental + controller-policy comparison** already grounded in Case 65. ReMAR is not treated as derived from Toshiba, nor Toshiba's design as derived from ReMAR.

---

## Chronology and anti-priority boundary

The dates have to be separated carefully:

```text
2014-09-11
    Toshiba adaptive-read-tracking priority date

2016-02-02
    US9251892B1 becomes public / granted

2017-03-24
    Japanese priority filing for Toshiba Memory age-aware design
    (not yet a public US disclosure)

2018-06 / 2018-07
    Luo et al. ReMAR work publicly presented / posted

2018-09-27
    US20180277227A1 public application
```

This produces two different chronology statements:

> **public adaptive read-voltage tracking precedent existed before ReMAR.**

But:

> **earlier priority filing != earlier public disclosure of the age-aware Toshiba design.**

The inspected record therefore does not justify an invention-priority claim, nor a genealogy claim from Toshiba to ReMAR or vice versa.

---

## Historical record

### H/P — Toshiba publicly disclosed adaptive read-voltage tracking by 2016

US9251892B1 describes a controller that determines an appropriate read voltage using observed threshold-voltage behavior rather than assuming one immutable read point. Its public record has a 2014 priority date and a 2016 publication/grant date.

For Case 65 the safe historical use is modest:

```text
fixed read voltage
    !=
all manufacturer read-control practice before 2018
```

It shows an earlier Toshiba design lineage for adaptive read tracking. The inspected material does not make retention age the decisive variable for this 2016 patent, so it is not relabeled as ReMAR or as an early-retention algorithm.

### H/P — the 2018 Toshiba Memory application explicitly conditions tracking on elapsed time

US20180277227A1's abstract and claims define a controller that determines a read voltage for a target cell by selecting a **tracking parameter** based on both:

- the word line connected to the target cell; and
- an **elapsed time from a previous access** to a group of cells including the target cell.

The tracking parameter can include:

- a starting read voltage;
- a number of read voltages used by the tracking process; and
- a gap between those read voltages.

The patent also allows tables or a formula to combine word-line identity and elapsed time, and further embodiments select among tables based on an access count.

This is manufacturer-primary evidence for a controller design where time is not merely a passive aging description. It becomes an input to the later interpretation procedure.

### H/P — the detailed embodiment retains reference-time and count state

The disclosed controller maintains management information including a **write reference time** for a block or page and can also manage read and write counts. In the described flow, elapsed time is calculated from retained reference-time information to the current access, after which the controller selects an adjustment / tracking pattern.

The bounded control relation is therefore broader than a single age scalar:

```text
word-line position
    + elapsed time from reference event
    + access-count / write-count state in disclosed variants
        -> tracking-parameter selection
        -> read-voltage search behavior
```

That matters for Case 65 because it warns against translating every age-aware controller into a one-variable `time -> Vref` model.

### H/P — reference-time data can survive at rest yet be loaded into volatile working state

The detailed Toshiba Memory embodiment describes management data stored in the nonvolatile memory and, after power-on, read into controller memory together with firmware/control and mapping-related state. Among the management items are **reference time data** and adjustment-pattern data.

The historical fact is a two-level state arrangement:

```text
nonvolatile management record
    -> after power-on
volatile controller working copy
```

The nonvolatile record and the live in-memory representation are not the same physical state, even though they participate in one control relation.

This is especially useful for the repository's retention question: a NAND device can require **persistent metadata about how to read persistent NAND**, while still rebuilding the immediately usable controller state after restart.

### H/P — tracking is tied to error evidence, not only to the passage of time

The disclosed flows use tracking when the ordinary read path cannot satisfy its error-correction condition; the patent also describes variants that can begin tracking when an error count is high even if ECC still corrects the data.

So the design does not support the simplification:

```text
time passes
    -> unconditional tracking every time
```

A safer reconstruction is:

```text
read / error evidence
    + retained context (word line, reference time, counts)
        -> choose bounded tracking search
```

### H/P — the design can participate in background / patrol reading

The detailed disclosure also permits the read-voltage determination behavior to be used during background or patrol-style reads, rather than only on a foreground host read that has already failed.

That provides a bounded bridge to maintenance policy:

> **interpretation maintenance can be invoked proactively without itself being physical refresh.**

The source does not establish a universal patrol interval, a specific production firmware schedule, or that every patrol read rewrites data.

### H/P — the patent contemplates 3D NAND but is not a measured 3D-NAND product study

The patent describes embodiments applicable to NAND organizations including three-dimensional structures. That makes it relevant to Case 65's 3D NAND interpretation problem, but its evidence role remains a **design disclosure**.

It does not supply the kind of measured, vendor-identified retention curve that would close the case's separate debt for named later 3D NAND generation measurements.

---

## Retained/control-state decomposition

This deepening requires the following states to remain separate.

### 1. NAND payload / threshold-voltage state

The physical cell distribution being interpreted.

### 2. Logical payload

The value the controller is trying to recover under ECC and read-control rules.

### 3. Reference-time record

A stored time marker associated with a block/page or access/write reference event in the disclosed design.

This is **control metadata**, not user payload.

### 4. Current-time relation

A meaningful current time or elapsed-time computation is required before the reference record can become an age estimate.

### 5. Word-line identity

The design conditions tracking on the target word line, making spatial/process context distinct from age.

### 6. Read/write count state

Some disclosed variants further select tracking behavior using access/write counters.

### 7. Adjustment-pattern / tracking-policy state

Tables or formulas map the retained context to tracking parameters such as start voltage, number of attempts, and spacing.

### 8. Volatile controller working copy

After power-on, management information can be loaded from nonvolatile storage into controller memory for active use.

### 9. ECC / error evidence

The read path's current failure or high-error condition can decide whether the tracking path is entered.

The important retention chain is therefore not one item called “the read voltage.” It is a relation among physical state, persistent control metadata, reconstructed working state, current error evidence, and a policy that selects an interpretation operation.

---

## Engineering reconstruction

### E — control metadata can have more than one persistence horizon

The Toshiba Memory design exposes a useful boundary:

```text
reference-time metadata retained in nonvolatile memory
    !=
working copy currently resident in controller memory
```

A controller restart can therefore destroy the active working representation without necessarily destroying the retained relation from which that working representation can be rebuilt.

This gives Case 65 a more concrete implementation-level form of its earlier `clock continuity can become retention infrastructure` result:

> **persistent read-interpretation metadata != continuously resident read-interpretation state.**

### E — boot reconstruction is not evidence of crash-atomic metadata updates

The patent's power-on load path proves that a restart boundary exists between durable management records and active working state. It does **not** prove:

- that every reference-time update reaches NAND atomically;
- that a torn metadata update is impossible;
- that the time record and logical-to-physical mapping are transactionally committed together;
- that the most recent record always survives sudden power failure;
- or that recovery from an inconsistent record has a particular policy.

Thus:

> **metadata is intended to persist across power cycles != arbitrary-crash consistency is proven.**

### E — age-aware interpretation can be multi-dimensional

The patent combines elapsed time with word-line position and, in variants, access/write counts.

So:

> **retention age != complete controller interpretation context.**

A real controller may use time as one dimension among process-location and use-history variables. This is consistent with Case 65's broader lesson that the future legibility of a cell is relational, but the exact relations here are those disclosed by Toshiba, not an extrapolated universal model.

### E — error evidence and context have different roles

ECC failure / high error count answers a question such as “is the ordinary read path insufficient or near its limit?” The retained reference-time and word-line/count context answer “where should a more expensive tracking search begin and how broad should it be?”

Therefore:

```text
trigger evidence
    != tracking context
    != tracking result
    != payload recovery verdict
```

### E — better interpretation is not physical renewal

Nothing in the bounded age-aware tracking relation requires restoring leaked charge. The controller can vary the read search around an existing physical embodiment.

Therefore:

> **age-aware read tracking != physical refresh / rewrite.**

If a later maintenance path rewrites data after reading it, that is another operation and requires its own source.

---

## Functional comparison with ReMAR — bounded

### Shared functional problem

Both the Toshiba Memory design and ReMAR make **time since a reference event** useful to later read interpretation.

A safe functional comparison is:

```text
retained time reference
    + current time
        -> elapsed-time estimate
        -> better-bounded read-reference selection/search
```

### Mechanism and evidence differences

ReMAR is a scholarly technique motivated by measured 3D-NAND early-retention behavior and explicitly models retention-age-dependent optimal read reference.

The Toshiba Memory patent is a manufacturer design disclosure in which elapsed time, word-line identity, and other state can choose a tracking search pattern.

Therefore:

> **same broad function != same algorithm.**

And:

> **same broad function != historical genealogy.**

The patent record inspected here does not show that Toshiba implemented ReMAR, that the ReMAR authors used Toshiba's design, or that either party copied the other.

### Priority date versus public disclosure

The Toshiba age-aware application claims a March 2017 Japanese priority date, but the US application became public in September 2018. Luo et al.'s ReMAR work was publicly presented / posted earlier in 2018.

Therefore:

> **filing priority chronology != public-knowledge chronology.**

This is why the evidence is useful as a parallel manufacturer design witness but unsuitable for an invention-priority claim.

---

## Cross-case boundaries

### Versus Case 36 — Flash Correct-and-Refresh

Case 36 concerns physical renewal / remapping policies that restore margin by rewriting corrected data.

This Case 65 deepening concerns a read path that uses retained context to choose a better interpretation/search of an existing embodiment.

```text
read-control adaptation
    !=
physical renewal
```

### Versus Case 52 — read disturb

Toshiba's disclosed variants can use read-count state, but the existence of a read-count input does not make all of the patent's elapsed-time behavior a read-disturb mechanism.

```text
elapsed-time context
    != read-count context
```

They may coexist as inputs to one controller policy.

### Versus Case 59 — program interference / NAC

The present witness does not require reading a neighboring cell as side information. It therefore does not close Case 65's separate ReNAC / real-neighbor-trace debt.

### Versus Case 04 — mapping/currentness

Both mapping metadata and read-interpretation metadata are controller state required to make persistent NAND useful, but they answer different questions:

- mapping/currentness: **which physical embodiment currently counts?**
- read-control context: **how should that embodiment be interpreted now?**

Losing one is not evidence of losing the other.

---

## Prior-art boundary

This deepening changes the prior-art picture in a bounded way.

1. Toshiba's 2016 public patent is an earlier manufacturer-primary witness for adaptive NAND read-voltage tracking.
2. Toshiba Memory's 2018 public application is a manufacturer-primary witness for **elapsed-time-conditioned** tracking with retained reference-time/control state.
3. Its 2017 Japanese priority filing predates Luo et al.'s 2018 public ReMAR record, but a priority filing is not the same thing as public disclosure.
4. The sources do not establish invention priority for `age-aware NAND reading` as a broad category.
5. The sources do not establish a direct technology-transfer or citation genealogy between Toshiba and ReMAR.

This repository therefore treats the record as **parallel / overlapping design evidence**, not a winner's timeline.

---

## Explicit non-claims

This evidence does **not** claim that:

1. US9251892B1 is an early-retention algorithm merely because it adapts read voltage.
2. The March 2017 Japanese priority filing was publicly readable on that date.
3. Toshiba Memory publicly disclosed its age-aware design before Luo et al. publicly presented ReMAR.
4. Toshiba invented age-aware NAND read-reference adaptation.
5. ReMAR derives from Toshiba's patent work.
6. Toshiba's design derives from ReMAR.
7. US20180277227A1 proves a named retail SSD/controller shipped the mechanism.
8. A patent embodiment proves production firmware behavior.
9. The reference-time field is user payload.
10. A block/page reference time is a perfect measurement of every cell's physical age.
11. A persistent reference-time record proves its latest update is crash-atomic.
12. Loading metadata at boot proves all metadata dependencies are mutually consistent.
13. Elapsed time is the only tracking input; the patent also exposes word-line and count dimensions.
14. ECC success means tracking is unnecessary in every embodiment; high-error-count variants can trigger additional work.
15. Read-voltage tracking physically restores leaked charge.
16. A background/patrol read necessarily rewrites the page.
17. Toshiba's tracking and ReMAR use identical equations, table layouts, voltage-search ranges, or metadata sizes.
18. The patent's 3D-NAND applicability is an independent measurement of a named 3D NAND product's early-retention curve.
19. Read-count-conditioned behavior and retention-age-conditioned behavior are the same physical failure mechanism.
20. Persistence of interpretation metadata is equivalent to persistence of the FTL mapping/currentness relation.

---

## Claim ledger

| Claim | Layer | Evidence strength | Boundary |
| --- | --- | --- | --- |
| Toshiba publicly disclosed adaptive NAND read-voltage tracking by 2016 | `H/P` | strong manufacturer-primary patent record | not yet an age-aware claim |
| Toshiba Memory's 2018 application selects tracking parameters using word line + elapsed time | `H/P` | strong manufacturer-primary application claims | patent design, not shipped product |
| tracking parameters can include start voltage, number of read voltages, and voltage spacing | `H/P` | strong application claims | does not expose every implementation heuristic |
| disclosed variants also use access/read/write count state | `H/P` | strong detailed-design evidence | count semantics vary by embodiment |
| reference-time / adjustment / management state can be stored nonvolatile and loaded after power-on | `H/P` | strong detailed-design evidence | does not prove atomic update behavior |
| ECC failure or high error evidence can trigger tracking | `H/P` | strong detailed-design evidence | not a universal trigger for all controllers |
| background/patrol paths can invoke the behavior | `H/P` | strong detailed-design evidence | not evidence of rewriting |
| persistent control record and volatile working copy have different persistence horizons | `E` | direct engineering reconstruction from power-on load path | project terminology |
| elapsed time is one dimension of interpretation state rather than the whole state | `E` | direct reconstruction from multi-input selection | bounded to disclosed design |
| age-aware tracking is physical refresh | `X` | contradicted by operation type | read interpretation != rewrite |
| Toshiba design is ReMAR | `X/A` | only functional comparison is supported | no algorithm/genealogy identity |
| March 2017 priority date proves earlier public disclosure than ReMAR | `X` | documentary-status error | filing date != public publication date |
| the disclosed design shipped in a named product | `X` | not established by inspected sources | product evidence remains open |
| age-aware control metadata can itself be part of a retention system | `I` | bounded conceptual pressure | not source vocabulary |

---

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `early retention` did not locate a dedicated reusable case. The broader Toshiba/Kioxia controller lineage, BiCS/V-NAND process genealogy, and patent-family history should live there if developed.

This repository keeps only the retention-specific relation among:

- persistent reference-time/control metadata;
- power-cycle reconstruction into volatile controller state;
- elapsed-time/context-conditioned read tracking;
- ECC/error evidence;
- and the boundary against physical renewal.

Case 65's existing ReMAR and ReNAC evidence remains the home for the academic 3D-NAND measurements and neighbor-conditioned recovery proposal.

---

## What this closes, and what remains open

### Boundedly closed

- a **manufacturer-primary design witness** that elapsed time can directly condition NAND read-voltage tracking;
- a manufacturer-primary example where reference-time/control metadata has a nonvolatile-at-rest representation and a volatile runtime representation;
- an earlier public Toshiba adaptive-read-tracking precursor against which the 2018 age-aware material can be compared without claiming algorithm identity.

### Still open

- evidence that a **named shipped SSD/controller** implemented this exact Toshiba/Toshiba Memory mechanism;
- direct vendor-identified 3D NAND retention measurements tied to that controller;
- sudden-power-loss tests of reference-time / tracking-metadata update consistency;
- exact coupling between reference-time state and FTL remap / garbage-collection relocation;
- production command/firmware traces showing the tracking path in operation;
- named shipped evidence for ReMAR-like block-program timestamps specifically;
- named shipped evidence for ReNAC-like neighbor-state reads;
- later TLC/QLC measurements and modern LDPC / soft-decoding interactions.

The correct status is therefore **manufacturer design disclosed; deployment and fault semantics unresolved**.

---

## Sources

1. Toshiba Corp, Shohei Asami, Toshikatsu Hida, Tokumasa Hara, Riki Suzuki, **_Memory system and method of controlling nonvolatile memory_**, US9251892B1, priority 11 September 2014, published/granted 2 February 2016. <https://patents.google.com/patent/US9251892B1/en>
2. Toshiba Memory Corporation, **_Semiconductor memory device and read control method thereof_**, US20180277227A1, claiming priority to JP2017-058897 (24 March 2017), US publication 27 September 2018; later US10586601B2, granted 10 March 2020. <https://patents.justia.com/patent/20180277227>
3. Yixin Luo, Saugata Ghose, Yu Cai, Erich F. Haratsch, Onur Mutlu, **“Improving 3D NAND Flash Memory Lifetime by Tolerating Early Retention Loss and Process Variation,”** *Proceedings of the ACM on Measurement and Analysis of Computing Systems* 2(3), Article 37, 2018, DOI `10.1145/3224432`. <https://arxiv.org/abs/1807.05140>

## Evidence-strength summary

- **Strong:** manufacturer-primary claim language that elapsed time + word-line identity select tracking parameters for read-voltage determination.
- **Strong:** manufacturer-primary design disclosure of retained reference-time / count / policy state and power-on loading into controller working memory.
- **Moderate-to-strong:** chronological comparison with ReMAR, provided priority filing and public publication are kept separate.
- **Not established:** shipped-product deployment, arbitrary-power-loss consistency, exact ReMAR genealogy, exact controller firmware implementation, or universal 3D NAND behavior.
