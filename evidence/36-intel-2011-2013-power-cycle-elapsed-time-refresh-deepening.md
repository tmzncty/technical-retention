# Case 36 Deepening — Intel 2011-filed / 2013-public power-cycle elapsed-time refresh state

## Status

**`bounded deepening complete`** — this addendum narrows one specific control-state and chronology boundary around Case 36. It directly inspects the public Intel-origin patent record later published as **US20130007344A1 / US8650353B2**, which describes nonvolatile-memory refresh driven by per-data/per-location elapsed-time state that can be stored in nonvolatile memory at power-down, reloaded after power-up, compared with a refresh threshold, and reset when the data is relocated to a fresh physical location.

The result is deliberately narrower than a general Flash-refresh history:

1. the application was **filed 1 July 2011** but the U.S. application was not publicly published until **3 January 2013**;
2. the disclosed maintenance clock can survive a power cycle as stored control metadata;
3. the patent's worked timing definition counts cumulative **powered-on intervals**, not automatically all wall-clock time while the medium is unpowered;
4. when a threshold is crossed, the disclosed refresh can relocate data independently of a host request and restart the elapsed-time relation for the new physical embodiment.

This evidence therefore deepens Case 36's retained-maintenance-state model while preserving the repository's anti-anachronism rule:

> **2011 filing chronology != 2011 public disclosure.**

It is not added to the existing set of **pre-2012 public** Flash-refresh records.

Canonical case: [`../cases/36-nand-flash-correct-and-refresh-maintenance.md`](../cases/36-nand-flash-correct-and-refresh-maintenance.md).

Related prior-art deepening: [`36-flash-refresh-1997-2009-prior-art-deepening.md`](36-flash-refresh-1997-2009-prior-art-deepening.md).

Related age-aware reading case: [`../cases/65-3d-nand-early-retention-loss-age-aware-reading.md`](../cases/65-3d-nand-early-retention-loss-age-aware-reading.md).

---

## Why this slice exists

Case 36 already has strong public evidence before the 2012 FCR paper for:

- periodic and idle-time nonvolatile-memory refresh;
- retained last-refresh time;
- power-up refresh;
- error/ECC-assisted maintenance;
- data-age/timestamp-triggered refresh;
- relocation plus logical-to-physical remapping;
- erase-free rewrite refresh.

The remaining question addressed here is different:

> What does an almost contemporary controller design say about the **persistence horizon of maintenance timing state itself**, especially across power-down and power-up?

That question matters because a controller can depend on history that is neither user payload nor a complete event log. A compact elapsed-time record may influence whether a still-readable physical embodiment is considered due for renewal.

The Intel-origin record is unusually useful because it describes both sides of that boundary:

- a retained representation in nonvolatile memory; and
- a runtime representation loaded into a register after power-up.

It also supplies a useful counterexample against treating every quantity called `elapsed time` or `retention age` as the same clock.

---

## Evidence classification

This addendum uses the repository's standard separation:

- **H/P — Historical / primary technical record:** dated patent filing/publication metadata, claims, figures, and descriptive text.
- **E — Engineering reconstruction:** state decomposition and failure/persistence relations inferred directly from the disclosed mechanism.
- **A — Functional analogy:** bounded comparison with FCR, Case 65, and other maintenance regimes without asserting genealogy.
- **P — Philosophical interpretation:** a narrow statement about compressed technical history and continuation state; never attributed to the inventors.
- **X — Explicitly rejected inference:** stronger claims that the inspected record does not support.

Patent disclosure is treated as **design evidence**, not proof of commercial deployment.

---

## Source identity and chronology

### Public record

The inspected record is:

- Hanmant P. Belgal, Xin Guo, Sai Krishna Mylavarapu, and Neal R. Mielke, **“Apparatus, system, and method for refreshing non-volatile memory.”**
- U.S. application `13/174,926`.
- Original assignee in the public record: **Intel Corporation**.
- Filing / priority date: **1 July 2011**.
- Application publication: **US20130007344A1, 3 January 2013**.
- Grant publication: **US8650353B2, 11 February 2014**.
- Public text: <https://patents.google.com/patent/US8650353B2/en>.

The date distinction is essential. The public patent record shows a 2011 filing event and a 2013 application-publication event. Those are different historical facts.

### Relative chronology with FCR

Case 36's bounded FCR object was publicly presented at ICCD in September 2012. The resulting chronology is:

```text
2011-07-01  Intel-origin application filed
2012-09     Cai et al. FCR public conference record
2013-01-03  Intel-origin U.S. application becomes public
2014-02-11  US8650353B2 grant publication
```

Therefore:

> **filing precedence != public-disclosure precedence.**

And specifically:

> **this source cannot be counted as an inspected pre-FCR public disclosure merely because its filing date is earlier.**

Nothing in this addendum decides patent-law priority, validity, conception date, private knowledge, or whether the FCR authors knew of the filing before publication.

---

## Historical / implementation record

### The controller tracks elapsed time per data or data location

The patent defines a controller mechanism that partitions nonvolatile memory and keeps elapsed-time information associated with data and/or data locations. A dedicated partition can retain those elapsed-time records.

The disclosed memory scope is broad. Embodiments include:

- SSD-attached nonvolatile memory;
- NAND Flash;
- NOR Flash;
- other nonvolatile technologies.

For Case 36, only the NAND/SSD-compatible retention-maintenance relation is carried forward. The broader patent scope is not used to claim one physical refresh mechanism across all listed media.

### Stored timing state can cross power-down and power-up

The patent describes storing elapsed-time or timestamp information in nonvolatile memory and then loading the timing state after power-up into controller working state.

Its claims make the boundary explicit:

- a timestamp corresponding to data in a data location can be stored to nonvolatile memory when the memory is powered down;
- the timestamp is loaded after powering up;
- elapsed time is determined from the loaded timestamp;
- data are refreshed when elapsed time exceeds a refresh time.

The descriptive embodiment likewise places stored elapsed times in a memory partition and reloads them at power-up.

This is direct evidence for two different persistence horizons:

```text
nonvolatile elapsed-time / timestamp record
    !=
volatile controller register / runtime working state
```

A power cycle can destroy the runtime copy while leaving a stored representation from which the controller reconstructs the maintenance relation.

### Refresh is autonomous with respect to the host request path

The patent describes automatic refresh before the associated retention-time limit and expressly allows refresh to occur independently of a host request. One embodiment gives refresh lower priority than host traffic and permits it during idle periods.

Therefore the historical record supports:

> **host inactivity != absence of internal retention work.**

But it does not establish any particular shipping SSD scheduler, QoS policy, firmware queue, or service-time guarantee.

### Refresh can relocate the logical payload and reset the maintenance clock

In the disclosed refresh path, data can be moved from the old physical data location to a new free location. The old location can then be erased/reclaimed, and the elapsed-time relation for the newly written location is reset and tracked again.

This produces a clean state transition:

```text
old physical embodiment
    + accumulated elapsed-time record
    -> refresh threshold crossed
    -> payload relocated to new free location
    -> old location retired / erased
    -> elapsed-time state for new embodiment reset
    -> new maintenance epoch begins
```

The logical payload can therefore continue while both physical location and maintenance-age state change.

### The refresh threshold can itself change with device condition

The claims and description allow the `retention time limit` to be determined from conditions such as operating voltage, temperature, and process technology. The record further describes reducing the retention-time limit over time and modifying the refresh time in response; the description associates this with device aging / increasing program-erase history in some embodiments.

Thus:

> **refresh deadline != necessarily one immutable device-lifetime constant.**

This is functionally adjacent to FCR's wear-adaptive maintenance rate, but the two documents do not thereby become the same algorithm or one genealogy.

---

## The critical clock-semantics boundary

### The patent's disclosed `elapsed time` is cumulative powered-on time

The patent defines `elapsed time` in a particularly important way. In the worked timing description, the quantity accumulates from power-up to power-down and then resumes across later powered intervals. Its example expresses the resulting quantity as the sum of powered intervals such as `t1 + t2`.

The record also describes periodically storing elapsed-time values and storing the determined elapsed times to nonvolatile memory at power-down so that they can be loaded again after the next power-up.

Therefore the direct historical record supports:

```text
power-on interval t1
    -> persist elapsed-time state at power-down
    -> power-off interval
    -> reload stored state at next power-up
    -> accumulate power-on interval t2

tracked elapsed time = t1 + t2 + ...
```

### Cross-reboot clock continuity is not automatically wall-clock retention age

The engineering consequence is easy to overstate. A counter that survives reboot can still represent only a selected notion of time.

For the disclosed worked embodiment:

> **cross-reboot maintenance-clock continuity != complete wall-clock retention age.**

And:

> **persistent timestamp state != proof that powered-off duration is included in the represented quantity.**

This does **not** mean the patent claims Flash stops aging while unpowered. It means only that the inspected timing definition does not allow us to equate its stored `elapsed time` with a universal physical-retention-age clock that necessarily includes every powered-off interval.

That distinction matters because charge-loss physics and controller scheduling clocks are different objects.

### A durable history summary can be intentionally lossy

The stored timing record is a compact control summary. It need not preserve:

- every read;
- every program operation;
- every power transition as a separate event record;
- a complete wall-clock chronology;
- raw threshold-voltage history;
- complete ECC-error history.

It preserves enough state for the disclosed controller rule to continue its maintenance decision after a power cycle.

Therefore:

> **retained maintenance history != retained event history.**

This is an engineering relation, not a claim about the inventors' philosophical intent.

---

## Retained-state decomposition

The mechanism exposes several separable kinds of state:

1. **payload charge / cell state** — the physical nonvolatile embodiment whose retention may degrade;
2. **logical payload identity** — the host-level data relation intended to continue across relocation;
3. **physical-location / mapping relation** — which location currently embodies the payload;
4. **stored elapsed-time or timestamp record** — nonvolatile control state used to continue the maintenance clock;
5. **runtime timing register / working copy** — volatile state reconstructed after power-up;
6. **time-source relation** — the current powered interval against which additional elapsed time is accumulated;
7. **refresh threshold / retention-time-limit policy** — the rule deciding when maintenance becomes due;
8. **device-condition inputs** — voltage, temperature, process, age/P-E-related context used by disclosed threshold adaptation;
9. **maintenance execution state** — whether relocation/erase/reset has actually completed.

Hence:

```text
payload state
    != mapping/currentness state
    != maintenance-age summary
    != runtime clock state
    != refresh policy
    != maintenance-completion state
```

A device can preserve one of these while losing another.

---

## Engineering reconstruction

### Due state is not completed maintenance

Crossing the elapsed-time threshold means the controller has a reason to refresh. It does not itself mean that data have already been relocated, the old location erased, or the new elapsed-time state committed.

Therefore:

```text
refresh due
    != refresh admitted / scheduled
    != payload relocated
    != old embodiment retired
    != new maintenance epoch established
```

The inspected patent describes the functional path but does not supply a crash-atomic transaction protocol for all of these substeps.

### Timer reset follows embodiment renewal, not logical forgetting

When refreshed data are relocated, the disclosed mechanism resets elapsed time for the new location. The user-visible payload can remain logically the same even though the maintenance clock restarts.

Thus:

> **maintenance-age reset != logical-object creation from nothing.**

And:

> **logical identity continuity != physical-age continuity.**

This is the same high-level identity/location distinction used elsewhere in the repository, but the trigger here is retention maintenance rather than ordinary garbage collection.

### Durable scheduling state can matter even when payload remains readable

A payload can remain physically present and ECC-readable while the controller loses or misinterprets the control state that says when it should next be renewed.

Accordingly:

> **payload survival != maintenance-policy continuity.**

The patent gives direct design evidence that a controller may deliberately make future retention work depend on stored timing state. It does not establish how a shipping product protects that metadata against torn updates or sudden-power loss.

### Powered maintenance and unpowered retention are different horizons

The disclosed automatic refresh requires the controller and memory system to be operating. The Flash medium, by contrast, is nonvolatile and can retain state without operating power.

Therefore:

> **medium can remain physically nonvolatile while maintenance execution is power-dependent.**

The patent's powered-on elapsed-time example makes this especially visible. The controller's maintenance clock and the substrate's physical aging need not have identical temporal coverage.

---

## Functional comparison with 2012 FCR

There are real similarities between the Intel-origin design record and Cai et al.'s FCR proposal:

- both treat Flash/nonvolatile retention as potentially requiring active maintenance;
- both allow maintenance to occur without a host payload update;
- both can renew data by writing a new physical embodiment;
- both treat maintenance timing as adaptable rather than necessarily fixed forever;
- both expose a trade between retention risk and program/erase/endurance cost.

But the comparison stops there.

FCR's bounded contribution is a peer-reviewed 2012 measured/evaluated policy family coupling 3x-nm MLC retention-error characterization, ECC capability, P/E wear, remapping, in-place reprogramming, hybrid fallback, and workload simulation.

The Intel-origin document is a patent/design disclosure whose public application appeared in 2013 and whose claims focus on elapsed-time tracking, refresh-time/retention-limit policy, power-cycle state transfer, and autonomous refresh.

Therefore:

> **functional overlap != direct design genealogy.**

And:

> **2011 filing date != evidence that FCR copied or even knew the design.**

No citation/influence chain is established in this slice.

---

## Functional comparison with Case 65 age-aware reading

Case 65 provides a useful counterexample to collapsing all retained time metadata into one function.

In Case 65, retention-age information can help select a better **read interpretation** for an existing 3D-NAND embodiment. The Toshiba/Toshiba Memory design witness there also distinguishes nonvolatile reference-time/control records from volatile working copies.

The Intel-origin Case 36 record instead uses elapsed-time state to decide when to **refresh/relocate** data.

Thus:

```text
age-aware read interpretation
    !=
time-triggered physical renewal
```

The semantics of the time variable also differ. The present Intel patent's worked elapsed-time definition accumulates powered-on intervals. Case 65's retention-age discussion must not be silently rewritten to inherit that definition.

Therefore:

> **same word `time` / `age` != same clock, persistence horizon, or maintenance action.**

This is a functional comparison only. No Toshiba ↔ Intel ↔ ReMAR/FCR genealogy is asserted.

---

## Historical vocabulary vs project vocabulary

### Historical/source vocabulary retained from the patent

- `elapsed time`;
- `time stamp`;
- `refresh time`;
- `retention time limit`;
- `refresh`;
- `relocating`;
- `new (free) data location`;
- `power-up` / `power-down`;
- `non-volatile memory`;
- `solid state drive (SSD)`;
- `NAND flash memory`;
- `program erase cycles`.

### Project analytical vocabulary

The following are reconstruction terms used by this repository, not terms attributed to the inventors:

- `maintenance-clock continuity`;
- `persistence horizon`;
- `maintenance-age summary`;
- `runtime working copy`;
- `maintenance epoch`;
- `physical-age continuity`;
- `control-state reconstruction`;
- `wall-clock retention age`;
- `history compression`.

Keeping these vocabularies separate prevents later abstractions from being projected backward into the source.

---

## Failure and forgetting boundaries

The disclosed design suggests several distinct failure surfaces without proving that any shipping device actually exhibits all of them:

- payload charge can decay while the controller still retains its timing metadata;
- timing metadata can be lost or stale while payload data remain physically present;
- runtime timing state disappears on power loss and must be reconstructed from a stored representation;
- a stored value can survive while the time-source interpretation needed to extend it becomes wrong;
- a refresh can become due before it is actually executed;
- relocation can create a new physical embodiment while the logical payload continues;
- a reset elapsed-time relation can be correct for the new embodiment even though it does not preserve the old embodiment's age;
- a powered-on-only maintenance clock can differ from total wall-clock time since programming.

The source does not give enough information to claim:

- crash-atomic timestamp updates;
- transactional coupling between timestamp reset and FTL remapping;
- a journal/checkpoint format;
- recovery rules for torn timing metadata;
- exact refresh-threshold values in a named product;
- exact treatment of long unpowered intervals in any commercial implementation.

Those remain evidence debt.

---

## Philosophical interpretation — tightly bounded

The mechanism provides one modest conceptual lesson for the repository:

> A system can retain not only an object but a **compressed relation to its technical past**, and that retained relation can decide what maintenance the object receives next.

The elapsed-time record is not the payload and not a complete history. It is a purpose-built summary of selected past duration.

A second limit follows immediately:

> A retained history summary is only as broad as the events and clock semantics that the system chose to encode.

This is the repository's interpretation. The patent does not make a philosophical claim about memory, identity, or historical time.

---

## Explicit non-claims

This addendum does **not** claim that:

1. the 2011 Intel-origin filing was publicly available in 2011;
2. US20130007344A1 is pre-2012 public prior art for the FCR paper;
3. the Intel inventors were the first to propose Flash/nonvolatile refresh or retained refresh timing state;
4. Cai et al. knew of, copied, licensed, or were influenced by this filing;
5. a named Intel SSD shipped the exact disclosed design;
6. the patent proves a commercial controller used exactly the illustrated partitions/registers;
7. the disclosed `elapsed time` equals complete wall-clock time since programming;
8. the patent proves that physical retention aging stops while the device is powered off;
9. every possible embodiment ignores powered-off duration;
10. timestamp storage and mapping updates are crash-atomic;
11. the timing state is user payload;
12. reset of the maintenance clock erases the logical identity of the payload;
13. the mechanism is identical to FCR, ReMAR, Toshiba age-aware tracking, DRAM refresh, or SSD sanitization;
14. one patent disclosure establishes broad industry deployment;
15. the described retention-time-limit adaptation is a universal NAND law;
16. a surviving timestamp guarantees a correct current maintenance decision under every reboot, temperature, and device-age history.

---

## Claim ledger

| Claim | Type | Strength | Evidence / limit |
| --- | --- | --- | --- |
| Intel-origin application `13/174,926` was filed 1-Jul-2011 | H/P | strong | public patent metadata |
| US20130007344A1 became public 3-Jan-2013 | H/P | strong | public patent timeline/publication record |
| US8650353B2 was granted/published 11-Feb-2014 | H/P | strong | public patent timeline |
| The original assignee in the record is Intel Corporation | H/P | strong | public patent metadata |
| The design stores elapsed-time/timestamp state associated with data or data locations in nonvolatile memory | H/P | strong | description + claims |
| Timing state can be loaded after power-up into controller working state | H/P | strong | description + claims 13–15 / SSD system claim |
| Data can be refreshed when elapsed time crosses a refresh threshold | H/P | strong | abstract + claims |
| Refresh can relocate data to a new free physical location and reset the elapsed-time relation | H/P | strong | definitions + detailed description |
| Refresh may occur independently of a host request and at lower priority/idle time in an embodiment | H/P | strong bounded | description/claims; not a universal scheduler claim |
| The disclosed worked `elapsed time` accumulates powered-on intervals across power cycles | H/P | strong | timing definition and `t1 + t2` example |
| Cross-reboot maintenance-clock continuity is the same as complete wall-clock retention age | X | rejected | powered-on-interval definition prevents this equivalence |
| The source proves Flash does not age while unpowered | X | rejected | controller-clock semantics != physical charge-loss law |
| Retention-time limit / refresh time can be adjusted as device condition changes | H/P | strong bounded | claims + description |
| The 2011 filing should be counted as pre-FCR public prior art | X | rejected | public application date is 3-Jan-2013 |
| The record proves direct Intel → FCR influence | X | rejected | no citation/influence chain established |
| The record proves named-product deployment | X | rejected | patent/design disclosure only |
| Stored timing state is control/context state rather than user payload | E | strong reconstruction | function is maintenance scheduling |
| Relocation can preserve logical payload while starting a new physical maintenance epoch | E | strong reconstruction | disclosed move + elapsed-time reset |
| A durable timing summary can omit parts of total real-world chronology | E | strong reconstruction | bounded by disclosed powered-on-time semantics |

---

## Related-repository audit

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for the exact patent numbers (`8650353`, `20130007344`) and broad nonvolatile-memory-refresh wording found no dedicated packet to reuse.

Therefore this addendum keeps only the retention-specific material required here:

- filing/publication chronology;
- elapsed-time control state;
- power-cycle persistence horizon;
- refresh-threshold decision;
- relocation/reset semantics;
- anti-genealogy boundary.

A fuller history of Intel SSD/controller architecture, patent prosecution/continuation history, product deployment, and vendor-to-vendor refresh design belongs primarily in `computing-archaeology` if developed later.

---

## Remaining evidence debt

1. Inspect prosecution history and any continuation/family records closely enough to determine whether another public family member exposed the same text before 3-Jan-2013.
2. Trace citations between this patent family, Cai et al. FCR, earlier refresh patents, and later controller patents without treating citation as influence by default.
3. Find a named shipping product or firmware/manual source, if any, that exposes comparable power-cycle timing-state behavior.
4. Find implementation evidence for atomicity/checkpointing of the timing metadata and its coupling to relocation/mapping state.
5. Determine how real controllers, if documented, account for **powered-off** retention duration when scheduling refresh after long shutdowns.
6. Find power-cut/fault-injection evidence for timestamp persistence and refresh-epoch reset.
7. Compare the timing model against Case 111's extended-shutdown maintenance only after a source exposes a directly comparable commercial policy.
8. Preserve the distinction between a maintenance scheduler's selected clock and physical retention-aging time in any later cross-case synthesis.

---

## Sources

1. Hanmant P. Belgal, Xin Guo, Sai Krishna Mylavarapu, Neal R. Mielke, **“Apparatus, system, and method for refreshing non-volatile memory,”** U.S. application `13/174,926`; US20130007344A1, published 3 January 2013; US8650353B2, granted/published 11 February 2014; filed 1 July 2011; original assignee Intel Corporation. Public record: <https://patents.google.com/patent/US8650353B2/en>.
2. Yu Cai, Gulay Yalcin, Onur Mutlu, Erich F. Haratsch, Adrian Cristal, Osman S. Unsal, Ken Mai, **“Flash Correct-and-Refresh: Retention-Aware Error Management for Increased Flash Memory Lifetime,”** ICCD 2012, DOI `10.1109/ICCD.2012.6378623`. Author-hosted paper: <https://users.ece.cmu.edu/~omutlu/pub/flash-correct-and-refresh_iccd12.pdf>.
3. Existing Case 36 public-prior-art ledger: [`36-flash-refresh-1997-2009-prior-art-deepening.md`](36-flash-refresh-1997-2009-prior-art-deepening.md).
4. Existing Case 65 age-aware read/control-state comparison: [`../cases/65-3d-nand-early-retention-loss-age-aware-reading.md`](../cases/65-3d-nand-early-retention-loss-age-aware-reading.md).
