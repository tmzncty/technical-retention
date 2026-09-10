# Case 36 Prior-Art Deepening — 1997–2009 nonvolatile-Flash refresh

## Purpose

This addendum deepens the novelty boundary for [`../cases/36-nand-flash-correct-and-refresh-maintenance.md`](../cases/36-nand-flash-correct-and-refresh-maintenance.md).

Case 36 remains a bounded study of Yu Cai et al.'s 2012 **Flash Correct-and-Refresh (FCR)** proposal/evaluation. The question here is narrower:

> Which parts of the 2012 FCR mechanism already had explicit technical prior art in earlier nonvolatile-memory records, and which parts remain distinctive to the 2012 paper's measured/evaluated combination?

The answer is materially stronger than the earlier generic caution against invention-priority claims. Public patent records before 2012 already describe:

- nonvolatile multilevel-memory refresh in response to threshold-voltage drift;
- ECC/error-detection-assisted correction and refresh;
- deferred, periodic, idle-time, and power-up refresh scheduling;
- refresh state such as last-refresh time;
- erase/rewrite sector refresh;
- refresh that moves data and changes logical-to-physical address mappings;
- age/timestamp-triggered in-place or out-of-place refresh;
- erase-free reprogram refresh triggered by time, charge/voltage drift, or read-error evidence.

Therefore the repository must **not** use FCR as the origin of generic Flash refresh, periodic nonvolatile-memory maintenance, refresh-by-relocation/remapping, or erase-free reprogram refresh.

This addendum does **not** decide patent validity, priority disputes, commercial deployment, or a direct design genealogy from any patent family to Cai et al. 2012.

## Evidence classification

- **H/P** — dated patent applications/publications and their technical descriptions/claims.
- **E** — engineering reconstruction constrained by those records.
- **A** — bounded functional comparison with the 2012 FCR mechanism and other repository cases.
- **X** — explicitly rejected stronger inference.

---

## Source A — 1997 filing / 1999 public patent: multibit nonvolatile refresh with error detection

### Identity

- Hock C. So and Sau C. Wong, **“Multibit-per-cell non-volatile memory with error detection and correction,”** US 5,909,449 A.
- U.S. application `08/924,909` filed **1997-09-08**.
- Patent publication/grant **1999-06-01**.
- Public patent record: <https://patents.google.com/patent/US5909449A/en>.

The later continuation family includes patents titled **“Multi-bit-per-cell flash EEPROM memory with refresh”**, but this addendum uses the 1999 public record as the conservative public-disclosure floor rather than silently treating the 1997 filing date as a publication date.

### Directly relevant mechanism

The patent describes a multilevel nonvolatile memory whose allowed threshold-voltage states are separated by forbidden zones. Drift into a forbidden zone can be detected as an error. The record describes several refresh paths and triggers:

- a refresh cycle reads cells and reprograms threshold voltages into an allowed state;
- a detected sector error may be marked for later refresh rather than repaired immediately;
- ECC can identify/correct data needed during reading or refreshing;
- an erasable Flash sector may be read into a buffer, erased, and rewritten;
- a timer may schedule systematic refresh;
- refresh may be delayed until inactivity;
- the last refresh date/time may be retained and checked while powered;
- full or partial refresh may be performed during power-up.

The patent even discusses periodic refresh intervals bounded by expected threshold drift, while making clear that the exact interval is technology-dependent.

### Retention consequence

This is a strong pre-2012 record for the generic relation:

> **nonvolatile state + drift/error evidence + correction/rewrite + retained schedule state can form a maintenance-dependent retention regime.**

It also means that the following are **not** safe FCR invention claims:

- `nonvolatile Flash can be refreshed`;
- `refresh can be periodic`;
- `refresh can be deferred to idle time`;
- `power-up can trigger refresh`;
- `ECC/error evidence can participate in refresh`;
- `refresh scheduling can depend on retained maintenance time state`.

### Limits

The inspected 1999 record is not a modern SSD/FTL paper, does not establish the 2012 FCR wear/error characterization, and does not prove that a commercial controller implemented every disclosed embodiment.

---

## Source B — 2000 filing / 2002 patent: dynamic refresh that changes physical location

### Identity

- **“Flash memory with dynamic refresh,”** US 6,396,744 B1.
- U.S. application `09/558,477` filed **2000-04-25**.
- Patent publication/grant **2002-05-28**.
- Public patent record: <https://patents.google.com/patent/US6396744B1/en>.

The same priority family later produced records titled **“Dynamic refresh that changes the physical storage locations of data in flash memory”** and **“Non-volatile memory operations that change a mapping between physical and logical addresses when restoring data.”** The family relation is directly visible in the patent record; this addendum does not infer a later SSD FTL genealogy from the titles alone.

### Directly relevant mechanism

The patent record describes:

- a refresh timer;
- a memory-management unit that reads and rewrites data for refresh without treating the operation as an ordinary host output;
- refresh that writes data into a second set of memory cells rather than requiring the same physical cells;
- an address-mapping circuit that maps a logical/virtual address to one physical address before refresh and another afterward;
- nonvolatile storage of one or more time counts indicating the last refresh of a memory, bank, array, or sector.

Later members of the same family explicitly describe periodic refresh whose timing can be related to tolerable threshold-voltage drift and expected drift rate, and data movement between physical locations with mapping changes.

### Retention consequence

This pushes an especially important Case-36 boundary backward:

> **refresh-mediated logical identity continuity across physical relocation predates the 2012 FCR paper.**

Therefore:

> **FCR remapping-based refresh != invention of refresh relocation or refresh-time address remapping.**

The 2012 FCR contribution must be described more narrowly: it uses measured retention-error behavior, ECC bounds, wear state, and SSD/FTL policy to decide when and how to renew error margin, rather than introducing the bare idea that refresh may move data behind a stable logical designation.

### Limits

A patent family describing internal mapping does not prove:

- commercial SSD deployment;
- identity with the later standard `FTL` abstraction;
- direct influence on Cai et al.;
- the exact same error trigger, endurance model, or controller architecture.

---

## Source C — 2004 priority / 2005 publication: data-age and timestamp-triggered refresh

### Identity

- **“Refreshing data stored in a flash memory,”** US 2005/0243626 A1 / US 7,325,090 B2.
- Priority **2004-04-29**; U.S. application filed **2004-10-27**.
- Application publication **2005-11-03**.
- Public patent record: <https://patents.google.com/patent/US7325090B2/en>.

### Directly relevant mechanism

The record describes refreshing nonvolatile-memory data according to a predetermined condition and explicitly allows:

- **in-place or out-of-place** refresh;
- a data-age condition;
- timestamps stored with data to record the storage/refresh date;
- periodic refresh;
- refresh at boot or dismount;
- refresh according to data type.

### Retention consequence

By 2005 there is therefore a public technical record in which **retention age itself is explicit control metadata** for deciding future maintenance.

This narrows another possible FCR novelty shortcut:

> **retention-age-aware refresh scheduling != an idea that first appears in 2012 FCR.**

FCR's adaptive-rate mechanism remains different because the 2012 paper couples measured retention-error behavior to P/E-cycle wear state and ECC-correctability/lifetime trade-offs rather than merely attaching an age timestamp to stored data.

### Limits

`age-aware` is a bounded functional comparison. The 2005 record and 2012 FCR do not thereby become one implementation lineage.

---

## Source D — 2007 filing / 2009 publication: erase-free rewrite refresh

### Identity

- Darlene G. Hamilton, Mark W. Randolph, Don Carlos Darling, and Ron Kornitz, **“Extending flash memory data retension [sic] via rewrite refresh,”** US 2009/0161466 A1.
- Filed / priority **2007-12-20**.
- Published **2009-06-25**.
- Original assignee in the public record: Spansion LLC.
- Public patent record: <https://patents.google.com/patent/US20090161466A1/en>.

### Directly relevant mechanism

The record describes reprogramming a Flash program state without first performing the full erase/rewrite cycle. It gives several possible triggers:

- elapsed time since programming or prior refresh;
- measured charge/voltage drift;
- read-error count/frequency crossing a threshold.

It explicitly presents the erase-free path as a way to renew stored state while reducing the endurance cost associated with repeated erase cycles, and describes applicability across several Flash technologies including SLC/MLC and NAND/NOR examples.

### Retention consequence

This is direct pre-2012 prior art against another overbroad novelty claim:

> **erase-free reprogram refresh != uniquely introduced by FCR.**

The safer FCR distinction is the paper's specific hybrid logic and evaluated reliability trade-off: in-place reprogramming is used for one bounded error direction, right-shift/program-interference evidence can force remapping, and refresh cadence is tied to P/E wear and ECC margin.

### Limits

A patent disclosure is not evidence that the mechanism was shipped in a named product. Nor does similarity of reprogramming goals establish that FCR copied, inherited, or even consulted this record.

---

## What this changes about Case 36

### Claims that must now be rejected as FCR novelty claims

The following relations have explicit pre-2012 technical prior art in the inspected record set:

1. nonvolatile Flash/nonvolatile multilevel memory can use refresh;
2. refresh may be periodic or deferred to idle time;
3. refresh may run at power-up;
4. refresh can use error-detection/ECC evidence;
5. refresh scheduling can depend on retained timing/age metadata;
6. refresh may erase/rewrite a sector;
7. refresh may relocate payload and change logical-to-physical mapping;
8. refresh may be performed in place or out of place;
9. refresh may reprogram a cell without a full erase cycle;
10. read-error or drift evidence may trigger refresh.

### What remains distinctive in the bounded 2012 FCR case

The surviving repository-level novelty is narrower and better grounded:

- the named **FCR** proposal and its 2012 paper identity;
- measured 3x-nm MLC retention-error characterization used as the policy basis;
- explicit comparison of required storage interval, P/E wear, and fixed ECC capability;
- remapping-based, in-place, hybrid, and adaptive-rate FCR as one evaluated design family;
- the hybrid threshold separating in-place repair from remap fallback when the opposite/right-shift error population becomes too large;
- per-block P/E-cycle information used to adapt refresh rate over device life;
- quantified SSD simulation driven by measured Flash characterization and workload traces;
- the explicit demonstration that refresh itself can spend endurance and become counterproductive beyond an operating point.

These points should be treated as a **combination/evaluation boundary**, not an invention-priority judgment.

---

## Historical record, engineering reconstruction, analogy, and philosophy

### Historical record

The dated patent records establish that specific refresh mechanisms and vocabulary existed before 2012. Patent filing/priority and public publication dates are recorded separately.

### Engineering reconstruction

The mechanism-level continuity is:

```text
physical threshold drift / error evidence
    -> maintenance trigger or schedule
    -> read / correction / rewrite or reprogram
    -> possibly new physical location / mapping
    -> renewed future read margin
```

But the controlling variables differ across records. `same functional chain` does not imply `same algorithm`.

### Functional analogy

The patents and FCR can be compared as nonvolatile-memory maintenance regimes. The comparison is functional, not genealogical.

Likewise, DRAM refresh remains only a bounded analogy: scheduled restoration is shared at a high level, while cell physics, rewrite geometry, endurance, control locus, and ordinary read semantics differ.

### Philosophical limit

The earlier prior art strengthens rather than weakens the project's mechanism-first rule: `nonvolatile` has never guaranteed that every useful reliability target is maintenance-free. It does not justify treating all technically maintained state as one philosophical kind of retention.

---

## Cross-case controls

### Case 04 — Flash virtual mapping

Case 04 grounds logical identity without location stability in an earlier Flash management context. The 2000 dynamic-refresh patent family adds a different trigger for relocation: restoration/refresh itself can change the physical embodiment.

**Boundary:** mapping continuity is older than FCR and does not establish an FTL genealogy into the 2012 design.

### Case 37 — Samsung 840 EVO old-data maintenance

Case 37 provides a later named commercial-product record in which powered maintenance/rewrite is used to address old-data behavior.

**Boundary:** earlier patents + 2012 research proposal do not prove the exact mechanism Samsung later shipped.

### Case 82 — NAND COPYBACK

Case 82 shows that relocation can propagate existing error debt when correction is bypassed. Case 36's bounded FCR path deliberately includes correction/error qualification before renewal.

**Boundary:** `move-and-remap` alone is not enough to establish `correct-and-refresh` semantics.

---

## Related-repository audit

`tmzncty/computing-archaeology` was searched in this round for `Flash memory with dynamic refresh` and broader nonvolatile-refresh wording. No dedicated Flash-refresh patent/history case was found.

Therefore:

- this addendum keeps only the retention-specific novelty boundary needed by Case 36;
- a full genealogy of nonvolatile-memory refresh patents, assignees, controller architectures, NAND generations, and commercial implementations belongs in `computing-archaeology` if developed;
- no direct patent-to-FCR genealogy is asserted here.

---

## Claim ledger

| Claim | Type | Strength | Evidence / limit |
| --- | --- | --- | --- |
| A 1997-filed, 1999-public U.S. patent describes multilevel nonvolatile-memory refresh triggered by drift/error evidence | H/P | strong bounded prior art | US5909449A; filing date separated from public grant date |
| The 1999 record includes deferred/periodic/idle-time/power-up refresh and retained last-refresh time | H/P | strong | US5909449A description |
| The 1999 record includes ECC/error-correction participation in read/refresh | H/P | strong | US5909449A description |
| A 2000-filed / 2002-public Flash patent describes refresh that can move data and change logical-to-physical mapping | H/P | strong | US6396744B1 and family record |
| A 2005-public record describes data-age/timestamp-triggered in-place or out-of-place Flash refresh | H/P | strong | US20050243626A1 / US7325090B2 |
| A 2009-public record describes erase-free reprogram refresh triggered by time, drift, or read-error evidence | H/P | strong | US20090161466A1 |
| Generic periodic Flash refresh is an invention of FCR | X | rejected | contradicted by pre-2012 records |
| Refresh-time relocation/remapping is an invention of FCR | X | rejected | contradicted by 2000/2002 dynamic-refresh family |
| Erase-free reprogram refresh is an invention of FCR | X | rejected | contradicted by 2007/2009 record |
| The patent records prove commercial deployment | X | rejected | patent disclosure != shipped implementation |
| Similar mechanisms prove a direct patent -> FCR design genealogy | X | rejected | no influence/citation chain established in this slice |
| FCR remains a distinct 2012 measured/evaluated retention-aware policy combination | H/P/E | strong bounded distinction | Cai et al. 2012 + prior-art exclusions above |

---

## Evidence debt

Still open after this slice:

1. pre-1978 nonvolatile-memory refresh genealogy and non-patent pre-1997 records; the bounded 1978–1994 public-patent floor is now handled in [`36-1978-1994-nonvolatile-flash-refresh-prior-art-deepening.md`](36-1978-1994-nonvolatile-flash-refresh-prior-art-deepening.md);
2. exact prosecution/continuation genealogy and ownership history for the 1997 and 2000 patent families;
3. non-patent academic/manufacturer records between 1997 and 2012;
4. named commercial implementations of any inspected patent mechanism;
5. whether and how these patent families were known to or cited by the FCR authors;
6. later 3D-NAND/controller refresh mechanisms and vendor-specific implementation evidence;
7. independent device-level experiments comparing refresh policy, endurance cost, and unpowered retention;
8. full controller-reliability history, which belongs primarily in `computing-archaeology`.
