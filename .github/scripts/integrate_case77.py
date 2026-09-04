from pathlib import Path
import re

CASE_PATH = Path('cases/77-data-general-dram-sniff-refresh-ecc-scrub.md')
EVIDENCE_PATH = Path('evidence/77-ibm-data-general-1971-1988-ecc-scrub-grounding.md')

case_text = r'''# Data General Dynamic-RAM “Sniffing”: Refresh-Coupled ECC Scrub and Corrective Writeback

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
'''

evidence_text = r'''# Case 77 grounding record — IBM/Data General memory correction, refresh-coupled sniffing, and later scrub terminology (1971–1988)

## Purpose

This record grounds [`../cases/77-data-general-dram-sniff-refresh-ecc-scrub.md`](../cases/77-data-general-dram-sniff-refresh-ecc-scrub.md).

The bounded question is not `when was memory scrubbing invented?` It is:

> Can period-primary evidence show a dynamic-RAM design in which ordinary charge refresh supplies recurring scheduling opportunities for a distinct full-word ECC inspection and corrective-writeback path, while earlier evidence prevents a false invention claim and later institutional evidence controls the modern word `scrubbing`?

Answer: **yes**, within the limits below.

## Evidence layers

### A. Historical record

Directly supportable claims about the cited designs, dates, terminology, and disclosed control paths.

### B. Engineering reconstruction

Modern terms such as `integrity scrub`, `redundancy-margin renewal`, `patrol-like scan`, and `second-order retention-control state` are used only to compare mechanisms.

### C. Functional analogy

Comparisons to DDR5 ECS, AVATAR, filesystem/disk scrub, and other maintenance systems are relation-level only.

### D. Philosophical interpretation

The case may pressure concepts of maintenance and continuity, but no engineering term is silently elevated into a theory of memory.

No experiment was performed in this slice.

---

## Source 1 — IBM US3735105A (primary prior-art boundary)

**Artifact:** Gerald A. Maley, assigned to International Business Machines Corporation, US3735105A, *Error correcting system and method for monolithic memories*.

**Dates:**

- filing / priority: **1971-06-11**;
- publication / grant: **1973-05-22**.

**URL:** <https://patents.google.com/patent/US3735105A/en>

### Directly supports

- IBM discloses a `memory correcting system` for monolithic memory.
- It operates on a **cycle-stealing** basis when memory is otherwise not busy.
- A counter/system can systematically and sequentially address memory locations rather than waiting for the running program to touch them.
- The purpose includes preventing random errors from accumulating beyond the correction capability of the redundancy code.
- When a correctable error is detected, corrected information can be reinserted / rewritten rather than leaving the erroneous stored word unchanged.
- The disclosure distinguishes normal-program error detection from systematic background interrogation.
- The patent states that some monolithic-memory types can be regenerated by reading, but its scope is not one precise DRAM refresh-coupled implementation.

### Does **not** support

- that IBM used the later generic term `memory scrubbing` in 1971;
- that this was the first ever systematic memory-correction design;
- a named commercial computer implementing the exact disclosed embodiment;
- the Data General 1980 refresh/sniff address composition;
- a universal claim about all semiconductor memories.

### Why it matters for Case 77

It blocks the attractive but unsupported narrative that Data General's later `sniff` mechanism invented the general idea of systematically revisiting ECC-protected memory to remove errors before they accumulate.

The safe relation is:

```text
IBM 1971 cycle-stealing systematic correction
        -> earlier prior art for the general maintenance pattern

Data General 1980 dynamic-RAM refresh-coupled sniff
        -> later, more specific composition
```

No direct genealogy is claimed from that date ordering alone.

---

## Source 2 — Data General US4380812A (central primary evidence)

**Artifact:** Michael L. Ziegler II, Michael B. Druke, John R. Van Roekel, Ward Baxter II, originally assigned to Data General Corporation, US4380812A, *Refresh and error detection and correction technique for a data processing system*.

**Dates:**

- filing / priority: **1980-04-25**;
- publication / grant: **1983-04-19**.

**URL:** <https://patents.google.com/patent/US4380812A/en>

### Historical vocabulary directly visible

- `dynamic random access memory (RAM)`;
- `refresh operation`;
- `sniff` / `sniffing operation`;
- `refresh interval timer`;
- `refresh address counter`;
- `bank controller`;
- `error correction`;
- `write back` / writeback control.

### Directly supports — ordinary refresh

The disclosure explains dynamic-RAM retention through charge stored on a capacitive element and the need for periodic read/restoration of each row before that charge decays beyond the intended logical state.

In the illustrative configuration:

- DRAM chips have 128 rows;
- an example refresh event recurs about every 15 microseconds;
- therefore each row is refreshed about every 1920 microseconds, approximately 2 milliseconds.

These are embodiment values, not universal DRAM constants.

### Directly supports — ECC organization

The illustrative memory plane uses:

- **32 data bits**;
- **7 check bits**;
- **39 chip-bit contributions** to the protected word.

The disclosed correction logic can identify/correct a bounded single-bit error class before supplying corrected data.

This record does not generalize that exact organization to every Data General memory.

### Directly supports — `sniff` operation

The patent explicitly describes periodic reading/error checking of a selected word as `sniff` / `sniffing`.

The important geometry is:

- row refresh acts across the addressed row of the DRAM chips/modules;
- only one selected word is read through the full ECC path at a given sniff opportunity;
- the refresh/sniff counter therefore carries row plus additional column/module address information for the integrity scan.

The patent gives an illustrative **two-second** interval between sniffing the same word.

This establishes:

> refresh-row coverage and full-word ECC-scan coverage can have different granularity and cadence inside one design.

### Directly supports — demand correction versus stored repair

When an ordinary requester encounters an erroneous word:

- the ECC path can correct the value before it is delivered outward;
- the patent says the stored word is not necessarily corrected at that moment;
- the periodic sniff later detects the stored error and triggers corrected writeback.

This directly grounds:

> **logical service correction ≠ stored-array repair**.

### Directly supports — corrective writeback

During a sniff, if an error is detected:

- the corrected data is written back into the same memory location;
- the control path retains/selects the same full address for the correction;
- in the pipelined embodiment, the word is re-read before the corrective write because its contents might have been modified in the meantime.

This directly grounds:

> **old error evidence ≠ unconditional authority to write an old corrected image later**.

### Directly supports — foreground priority and retry

If an external requester needs the memory around a scheduled sniff:

- request service can take precedence;
- the maintenance operation is delayed/repeated;
- the scan address is not simply discarded as completed.

Thus maintenance can be deferred without being canceled.

### Directly supports — fixed-frequency handling of recurring/hard faults

The patent discusses limiting the time spent on error correction when a hard single-bit error is present. Repeated correction is therefore not equivalent to repairing defective hardware.

### Does **not** support

- a named shipping product or machine containing the exact disclosed circuit;
- independent field reliability measurements;
- a claim that all Data General systems used this scheme;
- the first historical use of `scrub`;
- DDR5 on-die ECC/ECS semantics;
- a complete SEC-DED code genealogy;
- a claim that refresh and sniff are one physical predicate rather than deliberately coupled maintenance operations.

---

## Source 3 — IBM Research `soft error scrubbing` record (institutional terminology boundary)

**Artifact:** M. Blaum, Rodney M. Goodman, Robert J. McEliece, *Effect of Soft Error Scrubbing on Single-Error Protected RAM Systems*.

**URL:** <https://research.ibm.com/publications/effect-of-soft-error-scrubbing-on-single-error-protected-ram-systems>

### Catalog metadata caution

The IBM Research page:

- labels the publication **`ISIT 1985`**;
- displays a publication-date field of **01 Dec 1986**.

The record is therefore used here only as a **mid-1980s terminology/reliability witness**. It is not used to decide exact first-use chronology between 1985 and 1986.

### Directly supports

- the explicit phrase `soft error scrubbing` was in use in this mid-1980s IBM-associated research record;
- the protected RAM model uses single-error correction / double-error detection;
- the paper studies how scrubbing changes reliability;
- the scrub interval `T` is an explicit reliability parameter;
- scrubbing benefit depends on the underlying mix of failure modes rather than being universally beneficial under every error model.

### Does **not** support

- that these authors coined `scrubbing`;
- that Data General called its 1980 mechanism `soft error scrubbing`;
- a production implementation;
- a universal optimum interval.

---

## Source 4 — IBM Research 1988 reliability context

**Artifact:** Mario Blaum, Rodney Goodman, Robert McEliece, *The Reliability of Single-Error Protected Computer Memories*, *IEEE Transactions on Computers* 37(1), 1988, pp. 114–119.

**IBM Research record:** <https://research.ibm.com/publications/the-reliability-of-single-error-protected-computer-memories>

### Directly supports

- SEC-DED protected RAM reliability was an explicit late-1980s scholarly reliability problem;
- reliability analysis distinguishes failure modes and uses a system-level model rather than treating `ECC present` as a binary guarantee.

### Role in Case 77

This source is contextual, not needed for the central mechanism. It reinforces the evidence boundary that correction capability, error rates, and maintenance interval are reliability relations rather than simple Boolean device properties.

---

## Claim ledger

| Claim | Type | Evidence | Confidence |
| --- | --- | --- | --- |
| IBM disclosed systematic cycle-stealing correction of monolithic memory by 1971 filing date | H/P | US3735105A | high |
| IBM 1971 used the later generic term `scrubbing` | X | not established | rejected |
| Data General filed a dynamic-RAM refresh/error-correction design in 1980 | H/P | US4380812A | high |
| Data General calls the periodic integrity check `sniff` / `sniffing` | H/P | US4380812A | high |
| ordinary row refresh and full-word error scan have different address/coverage relations | H/P/E | US4380812A | high |
| the illustrative row-refresh timescale is about 2 ms while the same-word sniff interval is about 2 s | H/P | US4380812A bounded embodiment | high |
| demand read correction can succeed without immediate stored-word repair | H/P/E | US4380812A | high |
| a sniff-detected correctable error can trigger writeback of corrected data | H/P | US4380812A | high |
| a delayed corrective write may require re-reading because foreground data could have changed | H/P/E | US4380812A pipelined embodiment | high |
| maintenance may defer to requester traffic and later retry | H/P/E | US4380812A | high |
| `soft error scrubbing` appears as explicit IBM-associated research vocabulary by the mid-1980s | H/S | IBM Research record | high, exact 1985/1986 catalog chronology intentionally unresolved |
| scrub interval is a reliability parameter rather than mere implementation trivia | S/E | IBM Research record | high |
| Data General invented memory scrubbing | X | contradicted by earlier IBM systematic-correction evidence and unproven priority | rejected |
| Data General's patent proves named-product deployment | X | no deployment evidence in inspected sources | rejected |
| Data General sniffing and DDR5 ECS are the same mechanism | X/A | only bounded functional analogy | rejected |
| refresh and integrity scrub are synonymous | X | distinct cadence/address/purpose in central source | rejected |

---

## Cross-case boundaries

### Against Case 03 / DRAM refresh

Case 03 retains charge through periodic restoration. Case 77 adds an ECC-protected integrity relation whose scan can be much less frequent than row refresh.

> `charge restored` does not entail `every protected word recently verified/repaired`.

### Against Case 45 / DDR5 ECS

Both can be described functionally as read/check/correct/writeback maintenance. But:

- Data General 1980 places control at the system/bank-controller level and couples the opportunity to refresh;
- Case 45's Micron DDR5 evidence places ODECC/ECS inside the DRAM device and lists ordinary refresh separately;
- the historical vocabulary and interface are different.

This is a comparison, not genealogy.

### Against Case 43 / AVATAR

AVATAR changes later row-refresh classification based on error evidence. Data General writes corrected data back but does not establish a fast/slow row policy.

> `correct stored word` ≠ `change future refresh class`.

### Against disk/filesystem scrub cases

ZFS and storage scrubs traverse checksummed/redundant storage with different substrates, fault domains, and repair authority. The shared relation is only proactive integrity verification before user demand exposes an unrecoverable combination.

---

## Related-repository check

Searched [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `scrub` and `ECC` during this slice; no dedicated source file was returned by repository search.

Therefore this case retains a bounded retention analysis rather than copying a companion technical history. If a full ECC/scrub genealogy is later built, it should primarily live in `computing-archaeology`, with this case linking to it.

---

## Evidence gaps / future work

1. **Named deployment:** locate Data General product/service manuals establishing whether and where the US4380812A design shipped.
2. **Terminology chronology:** trace `scrub`, `scrubbing`, `memory scrubbing`, `patrol scrub`, and vendor equivalents with dated primary sources.
3. **ECC genealogy:** connect Hamming-derived codes, SEC-DED memory organization, semiconductor soft-error discovery, scrubbing, sparing, Chipkill, and DDR-era RAS without flattening them.
4. **Controller placement:** document movement of scan/correction authority from CPU/system controller to chipset/memory controller and later on-die ECS.
5. **Fault validation:** find field/fault-injection evidence that distinguishes correctable-event rate, recurring hard faults, scrub interval, and uncorrectable accumulation in named systems.
6. **Concurrency:** deepen the read-modify-write/currentness hazards of corrective scrub in multiprocessor or DMA-heavy systems.

None of these gaps blocks the bounded Case-77 claim.
'''

readme_entry = '- [`Case 77 — Data General Dynamic-RAM “Sniffing”: Refresh-Coupled ECC Scrub and Corrective Writeback`](cases/77-data-general-dram-sniff-refresh-ecc-scrub.md) — `grounded`; Data General\'s 1980-filed design uses dynamic-RAM refresh opportunities to advance a distinct full-word `sniff`/ECC check and conditionally rewrite corrected state. Earlier IBM 1971 cycle-stealing systematic correction blocks a first-invention claim, while the design itself separates charge-refresh coverage, integrity-scan coverage, demand correction, stored repair, and maintenance retry/currentness. Grounding: [`evidence/77-ibm-data-general-1971-1988-ecc-scrub-grounding.md`](evidence/77-ibm-data-general-1971-1988-ecc-scrub-grounding.md).'

case_index_row = '| [Data General Dynamic-RAM “Sniffing”: Refresh-Coupled ECC Scrub and Corrective Writeback](cases/77-data-general-dram-sniff-refresh-ecc-scrub.md) | **grounded** | dynamic-RAM charge + row refresh + ECC/check bits + full-word sniff address/coverage + conditional corrected writeback + foreground-aware retry | separate charge restoration from codeword-integrity renewal even when one schedule composes them; demand correction from stored repair; row-refresh coverage from word-scrub coverage; and correction algebra from writeback currentness | [1971–1988 IBM/Data General grounding](evidence/77-ibm-data-general-1971-1988-ecc-scrub-grounding.md); named Data General deployment, full scrub-terminology genealogy, controller-placement history, hard-error sparing, and independent fault validation remain separate work |'

matrix_row = '| Data General DRAM sniffing / 1980–1983 bounded design | dynamic-cell charge + ECC-protected word/check bits + row-refresh schedule + full-word sniff position + correction/writeback control | ordinary row refresh remains millisecond-scale in the illustrative design; one full word is additionally sniffed per refresh opportunity; correctable errors can trigger re-read/correct/writeback and foreground traffic can force retry | a demand read may return corrected data without immediately repairing the stored word; the later sniff path repairs the embodiment | refresh needs row coverage while sniffing advances a fuller row/column/module address relation | no payload relocation is required; the same logical location is renewed in place, but a stale maintenance image must not overwrite a newer foreground value | no application history by default; bounded scan-position/error/diagnostic state supports coverage and repair rather than a complete access history |'

findings = r'''## Case 77 — Data General refresh-coupled ECC-sniff findings

909. **charge refresh ≠ ECC integrity scrub even when scheduled together** — Data General uses refresh opportunities for both, but charge restoration and codeword-error removal have different success predicates;
910. **row-refresh coverage ≠ full-word scrub coverage** — the bounded design refreshes rows on the millisecond scale while a particular ECC-protected word can be revisited on a much longer scan interval;
911. **shared maintenance trigger ≠ identical maintenance purpose** — one timer/opportunity can coordinate two retention duties without making their mechanisms or failure margins synonymous;
912. **refresh address ≠ complete scrub address** — row restoration can proceed from a row address while the integrity scan needs additional column/module position to select one full protected word;
913. **demand-path correction ≠ stored-array repair** — an erroneous word can be corrected for the requester while the stored defect remains until the later sniff/writeback path;
914. **successful corrected read ≠ restored redundancy margin** — logical service can succeed while one correctable stored error still consumes part of the codeword's future failure margin;
915. **corrective writeback can renew failure margin without changing logical payload** — repair removes the already-observed error so an additional independent error is less likely to exceed the bounded code;
916. **error detection ≠ unconditional later write authority** — a corrected image derived from an earlier read can become stale if a foreground writer changes the word before maintenance completes;
917. **re-read before corrective writeback can be a currentness safeguard** — the bounded pipelined design re-accesses the word because its contents may have changed since the first error observation;
918. **foreground priority ≠ maintenance abandonment** — requester traffic can delay the sniff, while the controller retains/retries the maintenance position instead of marking unperformed work complete;
919. **maintenance deferral ≠ maintenance cancellation** — Case 77's integrity-scan debt is functionally comparable to Case 69's deferred refresh work only at the scheduling-relation level, not in mechanism;
920. **scan-position state ≠ application payload** — counters/full-address progress can be required for complete preventive coverage without being part of the user's stored word;
921. **correctable-event repair ≠ repair of permanently faulty hardware** — repeated writeback can remove transient word errors while a recurring hard fault still requires diagnosis, sparing, replacement, or other action;
922. **Data General `sniff` ≠ automatically historical `scrub` vocabulary** — `sniff/sniffing` is directly sourced in the 1980 filing, while `soft error scrubbing` is independently verified in the later IBM Research record;
923. **Data General system-level sniffing ≠ DDR5 on-die ECS** — both expose a read/check/correct/writeback relation, but controller locus, interface, ordinary-refresh composition, device generation, and historical terminology differ;
924. **Data General 1980 refresh-coupled correction ≠ invention of systematic memory correction** — IBM's 1971-filed cycle-stealing memory-correcting design already systematically revisits and rewrites corrected monolithic-memory state, so the bounded novelty claim is the Data General dynamic-RAM refresh/sniff composition rather than first invention.'''

# Guard against accidental replay.
if CASE_PATH.exists() or EVIDENCE_PATH.exists():
    raise SystemExit('Case 77 already exists; refusing to duplicate')

CASE_PATH.write_text(case_text.rstrip() + '\n', encoding='utf-8')
EVIDENCE_PATH.write_text(evidence_text.rstrip() + '\n', encoding='utf-8')

# README: insert after the first Case-76 case-ledger line, not the later evidence list.
readme_path = Path('README.md')
readme_lines = readme_path.read_text(encoding='utf-8').splitlines()
needle = 'cases/76-jedec-ssd-endurance-retention-qualification.md'
idx = next(i for i, line in enumerate(readme_lines) if line.startswith('- ') and needle in line)
readme_lines.insert(idx + 1, readme_entry)
readme_path.write_text('\n'.join(readme_lines) + '\n', encoding='utf-8')

# ROADMAP: this is the thirteenth bounded DRAM sub-slice. Insert before the existing broad-open-boundary sentence.
roadmap_path = Path('ROADMAP.md')
roadmap = roadmap_path.read_text(encoding='utf-8')
old_count = '**partially advanced by twelve grounded bounded sub-slices**'
new_count = '**partially advanced by thirteen grounded bounded sub-slices**'
if old_count not in roadmap:
    raise SystemExit('DRAM sub-slice count anchor missing')
roadmap = roadmap.replace(old_count, new_count, 1)
open_anchor = 'The broad item stays unchecked because a true JEDEC standards chronology'
insert_sentence = '[`cases/77-data-general-dram-sniff-refresh-ecc-scrub.md`](cases/77-data-general-dram-sniff-refresh-ecc-scrub.md), grounded by [`evidence/77-ibm-data-general-1971-1988-ecc-scrub-grounding.md`](evidence/77-ibm-data-general-1971-1988-ecc-scrub-grounding.md), adds an early system-level integrity-maintenance composition: Data General\'s 1980-filed dynamic-RAM design uses recurring refresh opportunities to advance a distinct full-word `sniff`/ECC scan and conditional corrective writeback, while IBM\'s 1971-filed cycle-stealing memory-correction design blocks a false first-invention claim. The case separates charge refresh from codeword repair, row-refresh coverage from word-scan coverage, demand correction from stored repair, and correction from writeback currentness. '
if open_anchor not in roadmap:
    raise SystemExit('DRAM open-boundary anchor missing')
roadmap = roadmap.replace(open_anchor, insert_sentence + open_anchor, 1)
roadmap_path.write_text(roadmap, encoding='utf-8')

# CASE_INDEX case ledger row.
index_path = Path('CASE_INDEX.md')
index_lines = index_path.read_text(encoding='utf-8').splitlines()
case76_needle = 'cases/76-jedec-ssd-endurance-retention-qualification.md'
case_idx = next(i for i, line in enumerate(index_lines) if line.startswith('| [') and case76_needle in line)
index_lines.insert(case_idx + 1, case_index_row)

# Comparison matrix row, after Case 76.
matrix_needle = '| JESD218 SSD endurance qualification / 2010–2015 bounded regime |'
matrix_idx = next(i for i, line in enumerate(index_lines) if line.startswith(matrix_needle))
index_lines.insert(matrix_idx + 1, matrix_row)

index = '\n'.join(index_lines) + '\n'
old_summary = 'After seventy-seven bounded cases, **all seventy-seven cases are now `grounded`.**'
new_summary = 'After seventy-eight bounded cases, **all seventy-eight cases are now `grounded`.**'
if old_summary not in index:
    raise SystemExit('aggregate status anchor missing')
index = index.replace(old_summary, new_summary, 1)

# Findings are currently the file tail; append the next bounded block.
if not index.rstrip().endswith('the Data General dynamic-RAM refresh/sniff composition rather than first invention.'):
    # Normal path before findings append should end at Case 76 finding 908.
    expected_tail = 'the bounded claim is the SSD-level application-class/TBW/retention composition.'
    if not index.rstrip().endswith(expected_tail):
        raise SystemExit('CASE_INDEX findings tail drifted; refusing unsafe append')
    index = index.rstrip() + '\n\n' + findings.rstrip() + '\n'
index_path.write_text(index, encoding='utf-8')

# Validation.
for p in [CASE_PATH, EVIDENCE_PATH, readme_path, roadmap_path, index_path]:
    text = p.read_text(encoding='utf-8')
    if '\x00' in text:
        raise SystemExit(f'NUL byte in {p}')

assert 'Case 77' in readme_path.read_text(encoding='utf-8')
roadmap_now = roadmap_path.read_text(encoding='utf-8')
assert 'thirteen grounded bounded sub-slices' in roadmap_now
assert '77-data-general-dram-sniff-refresh-ecc-scrub.md' in roadmap_now
index_now = index_path.read_text(encoding='utf-8')
assert 'seventy-eight bounded cases' in index_now
assert '909. **charge refresh ≠ ECC integrity scrub even when scheduled together**' in index_now
assert '924. **Data General 1980 refresh-coupled correction ≠ invention of systematic memory correction**' in index_now
assert matrix_row in index_now

nums = sorted(int(p.name.split('-', 1)[0]) for p in Path('cases').glob('[0-9][0-9]-*.md'))
assert nums == list(range(78)), nums

print('Case 77 integration prepared and validated')
