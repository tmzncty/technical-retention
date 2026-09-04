# Data General Dynamic-RAM “Sniffing”: Refresh-Coupled ECC Scrub and Corrective Writeback

## Status

**`grounded`** — bounded to Data General's 1980-filed dynamic-RAM refresh/error-correction design in US4380812A, with IBM's 1971-filed US3735105A used as earlier manufacturer-primary prior art for systematic cycle-stealing memory correction and IBM Research's mid-1980s `soft error scrubbing` record used only as a later terminology/reliability boundary.

Grounding record: [`../evidence/77-ibm-data-general-1971-1988-ecc-scrub-grounding.md`](../evidence/77-ibm-data-general-1971-1988-ecc-scrub-grounding.md).

## Scope

This case asks one narrow question left open by the DRAM-refresh cases and by Case 45's later DDR5 ECS case:

> What changes when a dynamic-RAM system uses the recurring refresh schedule as an opportunity to inspect ECC-protected words, repair correctable stored errors, and write the corrected word back — while ordinary charge refresh and codeword-integrity maintenance remain technically distinct operations?

The bounded design is Data General's US4380812A, filed **25 April 1980** and published **19 April 1983**. Its historical vocabulary includes:

- `dynamic RAM`;
- `refresh`;
- `error correction`;
- `sniff` / `sniffing` for the periodic word-level error-check operation;
- `refresh interval timer`;
- `refresh address counter`;
- `bank controller`;
- `write back`.

The patent's illustrative organization uses 32 data bits plus 7 check bits per word and describes a system in which a row-refresh opportunity also advances a fuller address used to inspect one word for an ECC-correctable error. If the word is erroneous, the corrected value is written back into the same memory location.

This case is **not**:

- a claim that Data General invented memory scrubbing;
- a claim that US4380812A was implemented unchanged in a named shipping Data General computer;
- a claim that every 1980-era DRAM system combined ECC checking with refresh;
- a claim that `sniffing` was already the generic historical term `memory scrubbing`;
- a claim that charge refresh and ECC scrub are the same physical operation merely because this design schedules them together;
- a complete history of SEC-DED memory, semiconductor soft errors, alpha-particle failures, patrol scrub, Chipkill, DRAM RAS, or DDR5 ECS.

The contribution is a retention-specific separation of **charge restoration, error detection, logical correction, stored-codeword repair, scan coverage, and maintenance scheduling** inside one period design that deliberately composes them.

## Relation to earlier cases

### Cases 03, 21, 33, 34, 35, and 69 — DRAM refresh

Those cases establish several variants of the ordinary DRAM retention obligation: decaying charge must be periodically restored, while command responsibility, address generation, temperature policy, bank geometry, and timing elasticity can move independently.

Case 77 adds a second maintenance target:

```text
cell charge near a valid logical level
        !=
ECC-protected word free of an already-manifested correctable error
```

Data General's design intentionally schedules error checking alongside refresh opportunities, but its own address geometry and timescales show that the two duties are not identical.

### Case 45 — DDR5 ODECC / ECS

Case 45 gives a later commercial DDR5 composition in which ordinary read-path ODECC and Error Check and Scrub are distinct from ordinary refresh. Case 77 is a useful earlier counterpoint because it puts the integrity scan at the **system/bank-controller** level and deliberately piggybacks it on refresh timing.

The shared functional relation is:

```text
recover a correct value now
        !=
repair the stored embodiment for later
```

The mechanisms, integration locus, interface, vocabulary, and historical period are different. No direct Data-General-to-DDR5 genealogy is claimed.

### Case 43 — AVATAR

AVATAR uses runtime ECC evidence to change **future refresh classification**. Data General's bounded design instead uses an ECC event to correct and rewrite the word; the inspected patent does not establish a row-retention classifier that changes future charge-refresh cadence.

Therefore:

> **ECC corrective writeback ≠ retention-aware refresh reclassification**.

## Historical record

### 1. Data General explicitly combines dynamic-RAM refresh with periodic word checking

US4380812A identifies its field as error correction for a dynamic-RAM array in which error detection occurs as part of a refresh operation. The patent separately explains ordinary dynamic-RAM refresh in charge terms: a capacitive cell loses charge with time, so each row must be periodically read/restored before the represented `one` or `zero` becomes unreliable.

The same design then adds a periodic full-word check, which it calls a `sniff` or `sniffing` operation. A refresh event supplies the recurring maintenance opportunity, but a complete word address is used so that one ECC-protected word can be read and evaluated while the relevant rows are refreshed.

Source: Data General, US4380812A, filed 1980-04-25, published 1983-04-19: <https://patents.google.com/patent/US4380812A/en>

### 2. One refresh opportunity does not mean one complete integrity sweep

The illustrative DRAM has 128 rows and a refresh pulse approximately every 15 microseconds so each row is refreshed about every 2 milliseconds. Yet only one word is selected for the added error-check operation at each such opportunity, and the fuller refresh/sniff address advances through row, column, and module position.

The patent gives an illustrative interval of about **two seconds** between checks of the same word.

The exact numbers belong to that disclosed embodiment, not to DRAM in general. Their methodological value is the ratio:

```text
charge-restoration coverage
        much faster than
full word-integrity scan coverage
```

This directly blocks the shortcut `if ECC checking is scheduled during refresh, then ECC scrub simply is refresh`.

### 3. Demand-path correction and stored-array repair are deliberately separated

The patent describes two error encounters:

- if a requester reads a word and an error is found, corrected data can be supplied to the requester;
- the erroneous stored word is not necessarily rewritten on that demand path;
- the later periodic sniff encounters the word, corrects it, and performs the writeback into memory.

Thus a logical read can succeed while the stored embodiment still contains the correctable defect.

### 4. Maintenance must respect concurrent currentness

The patent also handles a requester arriving around a sniff/writeback. Foreground access can take priority; the maintenance operation is then retried. In the pipelined discussion, the word may be read again before corrective writeback because its contents could have changed after the first error observation.

This is an important retention boundary:

> a previously computed corrected image can itself become stale before it is written back.

Corrective maintenance therefore depends on currentness/ordering, not only on ECC algebra.

### 5. Earlier IBM evidence blocks a Data-General-first claim

IBM's Gerald A. Maley filed US3735105A on **11 June 1971**, years before Data General's filing. IBM's design systematically and sequentially addresses monolithic memory when the memory is otherwise idle, detects/corrects errors, and rewrites corrected data so random errors do not accumulate beyond the redundancy code's correcting capability.

IBM calls this a `memory correcting system` operating on a `cycle stealing` basis. The inspected text does **not** establish that 1971 IBM used the later generic word `scrubbing`, nor is it restricted to the same dynamic-RAM refresh-coupled mechanism as Data General.

Source: IBM, US3735105A, filed 1971-06-11, published 1973-05-22: <https://patents.google.com/patent/US3735105A/en>

Therefore the safe historical claim is not `Data General invented memory scrub`. It is:

> by 1980, Data General had disclosed a dynamic-RAM design that deliberately coupled periodic ECC word inspection and conditional corrective writeback to recurring refresh opportunities, while keeping full-word scan addressing and ordinary row refresh technically distinct.

### 6. `soft error scrubbing` is a later verified term in the source set

An IBM Research publication record for Blaum, Goodman, and McEliece explicitly uses the title **“Effect of Soft Error Scrubbing on Single-Error Protected RAM Systems”** and treats scrub interval `T` as a reliability parameter for coded memory.

The IBM catalog has a bibliographic wrinkle: the page labels the publication `ISIT 1985` while its displayed date is December 1986. This case therefore uses it only as a **mid-1980s terminology and reliability-model witness**, not as proof of a first use or an exact 1985/1986 priority claim.

Source: IBM Research: <https://research.ibm.com/publications/effect-of-soft-error-scrubbing-on-single-error-protected-ram-systems>

## Mechanism

### 1. Refresh and integrity scrub preserve different margins

Ordinary DRAM refresh renews the analog charge representation before leakage crosses a data-loss threshold. ECC checking asks another question: does the recovered codeword already contain a correctable error?

A word can therefore be:

```text
sufficiently refreshed as charge
        +
still contain one ECC-correctable wrong bit
```

Conversely, correcting an ECC error does not remove the recurring charge-refresh obligation.

Therefore:

> **charge refresh ≠ codeword integrity scrub**.

Data General's design is valuable precisely because it composes both without making them conceptually identical.

### 2. Shared scheduling opportunity ≠ shared maintenance predicate

A refresh interval timer creates a recurring time slot. The row address is sufficient to restore cell charge across the selected row geometry. The added sniff operation needs a fuller address so that one particular word can be checked through the ECC path.

The same timer event can therefore trigger two operations whose target granularity and success condition differ.

This yields:

> **shared maintenance trigger ≠ identical maintenance purpose**.

### 3. Row-refresh coverage ≠ word-scrub coverage

The patent's illustrative timing makes this especially clear. Every row receives refresh on the millisecond scale, whereas a particular full word can wait much longer before its turn in the rotating integrity scan.

The system therefore retains at least two notions of `coverage`:

- every charge-bearing row has been refreshed within its deadline;
- every ECC-protected word has been inspected within the intended scrub interval.

Meeting one does not logically prove the other.

### 4. Correction at read time ≠ renewal of stored state

The error corrector can reconstruct a correct logical value for the requester. If that corrected value is only returned outward, the latent stored defect remains.

Corrective writeback changes the future risk relation: it restores the codeword to a state that again has its full single-error margin against an additional independent error, within the assumptions of the bounded code.

Hence:

> **successful corrected read ≠ restored redundancy margin**.

This is the same functional relation later seen in Case 45, but Data General's implementation and historical vocabulary are different.

### 5. Scrub interval is a retention-control parameter

The IBM Research record later makes the point mathematically explicit by parameterizing reliability with scrub interval `T`. Data General's design already embodies the engineering intuition: inspect words often enough that a correctable error is unlikely to be joined by another error in the same codeword before repair.

The scan schedule is therefore not application history. It is **second-order retention-control state**: enough address/progress relation must exist for the system to continue coverage.

The patent's refresh/sniff counter is a concrete embodiment of that requirement in the disclosed design.

### 6. Foreground priority does not erase maintenance debt

The design permits ordinary requester traffic to preempt or delay a sniff. But the sniff address is retained/reused and the maintenance operation is retried rather than silently forgotten.

This gives a relation familiar from Case 69's refresh scheduling but with a different trigger and purpose:

> **maintenance deferral ≠ maintenance cancellation**.

Here the deferred work is an integrity inspection/corrective opportunity, not a JEDEC REF command.

### 7. Corrective writeback must be current

If a requester can modify the word between detection and maintenance writeback, replaying a stale corrected image could overwrite newer valid data. The patent therefore describes re-accessing/re-reading before the corrective writeback in the pipelined path.

This makes integrity maintenance relational:

```text
error evidence
    + current word version
    + correction
    + writeback ordering
        -> safe stored-state repair
```

ECC alone is not enough to authorize a later write.

## Retained state

The bounded design involves several state classes:

1. **application payload bits** — the logical user/program word;
2. **check bits** — redundancy used to detect/correct the bounded error class;
3. **dynamic-cell charge** — the volatile physical representation periodically refreshed;
4. **refresh schedule/address state** — enough state to ensure all rows receive charge restoration;
5. **sniff scan position** — enough full-address progress to eventually inspect all protected words;
6. **error evidence / diagnosis state** — the disclosed controller can record errored words/addresses and distinguish continuing fault behavior from one corrected event;
7. **request/maintenance ordering state** — enough control relation to delay and retry maintenance without overwriting a newer foreground value.

These must not be collapsed into `the memory contents`.

## Failure and forgetting boundaries

The case exposes several distinct failure modes:

- **charge-decay failure** — refresh misses the physical retention deadline;
- **correctable codeword error** — charge/state has deviated but the code still reconstructs the intended word;
- **error accumulation** — another error appears before the first defect is repaired, exhausting the bounded correction relation;
- **coverage failure** — some word is not revisited by the systematic scan within the assumed reliability interval;
- **stale-maintenance writeback** — a corrected image computed from an old observation overwrites a newer foreground value;
- **hard/recurrent fault** — repeated correction cannot substitute for repairing a permanently faulty component;
- **diagnostic-state loss** — payload may remain usable while the system forgets evidence useful for locating a recurring fault.

Likewise, successful corrective writeback is not `forgetting` in a sanitization sense. It intentionally removes an error from the **current codeword state**, but supplies no claim that every prior electrical state is forensically erased.

## Maintenance, bandwidth, and labor

Data General explicitly uses already recurring refresh opportunities to reduce incremental machine-time cost for error detection. That does not make maintenance free:

- counters/address generation must advance;
- ECC/check-bit logic must evaluate the selected word;
- an error can cause an extra read/modify/write sequence;
- foreground traffic can force retry and therefore retain pending maintenance position;
- permanent faults can create recurring correction/diagnosis work;
- system designers must choose a scan interval consistent with the error model and capacity.

The useful project formulation is:

> **piggybacked maintenance ≠ zero-cost maintenance**.

## Prior art and anti-anachronism

### Historical record

- **1971 IBM:** `memory correcting system`, systematic sequential addressing, cycle stealing, correction and reinsertion/rewriting of corrected data.
- **1980 Data General:** dynamic-RAM refresh plus `sniff` / `sniffing`, full-word error checking, conditional corrective writeback, and a separate illustrative scrub/scan cadence.
- **mid-1980s IBM Research record:** explicit `soft error scrubbing` terminology and a reliability model parameterized by scrub interval.

### Engineering reconstruction

This repository uses `integrity scrub`, `patrol-like scan`, `redundancy-margin renewal`, and `second-order retention-control state` as modern engineering descriptors where useful.

They are **not** silently projected into the 1971 IBM or 1980 Data General documents as the actors' own words.

### Rejected claims

- `Data General invented memory scrubbing` — **rejected** by the earlier IBM manufacturer-primary design.
- `IBM 1971 is already the same dynamic-RAM refresh-coupled mechanism` — **rejected**; the IBM scope is broader monolithic memory and cycle stealing, while Data General's bounded mechanism explicitly composes dynamic-RAM refresh with word checking.
- `Data General sniffing = DDR5 ECS` — **rejected**; only the read/correct/writeback relation is functionally comparable.
- `refresh = scrub` — **rejected** by the distinct address coverage, timescales, predicates, and writeback conditions inside the Data General design itself.
- `patent disclosure = proven production deployment` — **rejected**; no named shipping system implementation is claimed here.

## Functional analogy and philosophical limit

A bounded functional analogy describes the integrity scan as preventive maintenance: a recoverable defect is removed before a second defect consumes the remaining correction margin.

The analogy is useful only at that operational level. The system does not `remember its mistakes` in a psychological sense, and a check-bit syndrome or scan counter is not an archive simply because it is retained state about other retained state.

The narrower conceptual result is:

> apparent continuity can depend on maintaining not only the payload, but also the **remaining margin by which future errors are still recoverable**.

That margin is neither identical to the payload nor reducible to the DRAM cell's raw charge-retention deadline.

## Related repositories

A repository search found no dedicated ECC/memory-scrubbing case in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for this slice. A future full genealogy of Hamming/SEC-DED memory, semiconductor soft errors, IBM/Data General implementations, patrol scrub, Chipkill, and DDR-era RAS belongs primarily there.

`technical-retention` should keep only the cross-mechanism distinction developed here: **charge refresh, codeword correction, stored repair, scan coverage, and remaining correction margin are separate retention relations even when one controller schedules them together**.

## Sources

### Manufacturer-primary / patent evidence

1. Gerald A. Maley / IBM, **US3735105A, “Error correcting system and method for monolithic memories”**, filed 11 June 1971, published 22 May 1973. <https://patents.google.com/patent/US3735105A/en>
2. Michael L. Ziegler II, Michael B. Druke, John R. Van Roekel, Ward Baxter II / Data General, **US4380812A, “Refresh and error detection and correction technique for a data processing system”**, filed 25 April 1980, published 19 April 1983. <https://patents.google.com/patent/US4380812A/en>

### Institutional / scholarly terminology and reliability boundary

3. M. Blaum, Rodney M. Goodman, Robert J. McEliece, **“Effect of Soft Error Scrubbing on Single-Error Protected RAM Systems”**, IBM Research publication record; catalog labels `ISIT 1985` and displays a December 1986 date. <https://research.ibm.com/publications/effect-of-soft-error-scrubbing-on-single-error-protected-ram-systems>
4. Mario Blaum, Rodney Goodman, Robert McEliece, **“The Reliability of Single-Error Protected Computer Memories,”** *IEEE Transactions on Computers* 37(1), 1988, pp. 114–119; IBM Research record. <https://research.ibm.com/publications/the-reliability-of-single-error-protected-computer-memories>

## Open questions

- Which named Data General machines, if any, implemented the exact refresh-coupled sniff mechanism disclosed in US4380812A?
- What period service/engineering manuals expose the scan interval, counters, or ECC fault reports in deployed systems?
- When did `scrub`, `scrubbing`, and later `patrol scrub` become stable vendor/architecture vocabulary rather than one paper's terminology?
- How did system-level memory scrub move between processor, memory controller, chipset, DIMM, and eventually device-internal DDR5 ECS loci?
- Which commercial systems coupled scrub to refresh versus running an independent scan engine?
- How should hard-error sparing/offlining be layered over correction/writeback without treating repeated rewrite as repair of failed hardware?
