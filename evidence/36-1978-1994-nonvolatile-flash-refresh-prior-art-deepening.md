# Case 36 Earlier Prior-Art Deepening — 1978–1994 nonvolatile-memory and Flash refresh

## Purpose

This addendum deepens the earlier-public-record boundary for [`../cases/36-nand-flash-correct-and-refresh-maintenance.md`](../cases/36-nand-flash-correct-and-refresh-maintenance.md).

The existing Case-36 prior-art addendum begins with a 1997 filing / 1999 public patent record. Its own evidence debt therefore asks for **pre-1997 nonvolatile-memory refresh prior art**. This slice closes that bounded gap with three primary patent records:

1. a **1978-filed / 1980-public Matsushita** nonvolatile-memory refresh circuit whose specific embodiment is MNOS and whose trigger is natural time-dependent drift;
2. a **1990-filed / 1993-public Intel** block-erase Flash EPROM refresh design whose trigger is accumulated gate/drain disturbance from ordinary high-voltage operations;
3. an independent **1992-filed / 1994-public Texas Instruments** Flash EEPROM refresh design using margin-sensitive reads, restorative program pulses, optional sector erase/rewrite, and erase-cycle/time triggers.

The result is not an invention-priority claim. It establishes only a conservative **publicly inspectable floor** for several refresh relations that predate the 2012 Flash Correct-and-Refresh (FCR) paper.

The most important correction is chronological and mechanistic:

> **generic nonvolatile-memory refresh is publicly documented by 1980, and explicit Flash refresh is publicly documented by 1993; neither statement implies that those records implement Cai et al.'s 2012 retention-aware FCR design.**

The sources also show why `refresh` cannot be treated as one timeless physical operation. Across these records it can mean erase-and-rewrite after a decay warning, same-location reprogram after disturb detection, or a sector reconstruction path after temporarily retaining the intended contents.

## Evidence classification

- **H/P** — patent records and technical descriptions available in the cited public documents.
- **E** — engineering reconstruction constrained by those mechanisms.
- **A** — bounded functional comparison with later Case-36 FCR and other grounded cases.
- **I** — narrow philosophical interpretation explicitly separated from the historical record.
- **X** — rejected or unsupported stronger inference.

Patent filing/priority dates and public publication/grant dates are kept separate. A patent disclosure is not evidence that the disclosed mechanism shipped in a commercial product, and similarity does not establish an influence chain.

---

## Source A — Matsushita, 1978 filing / 1980 publication: natural-decay warning and automatic reprogramming

### Identity

- Yukio Furuta and Tomisaburo Okumura, **“Non-volatile memory refresh control circuit,”** US 4,218,764 A.
- Original assignee: Matsushita Electric Industrial Co., Ltd.
- Filed / priority: **1978-10-03**.
- Published / granted: **1980-08-19**.
- Public record: <https://patents.google.com/patent/US4218764A/en>.

These dates establish a public record by 1980. They do not establish first invention of nonvolatile-memory refresh.

### Historical record

The patent explicitly begins from a nonvolatile-memory retention problem rather than from DRAM-style volatility. It describes nonvolatile devices as retaining contents `semipermanently` while stating that memory states nevertheless change gradually with elapsed time. It models two logical memory levels whose separation decreases until ordinary interrogation can no longer distinguish them reliably.

The proposed control relation introduces an earlier warning threshold. A second nonvolatile-memory part, carrying a predetermined pattern and interrogated at a stricter reference level, can produce an alarm **before** the primary memory reaches the final readability threshold. The reprogram control then:

1. reads/transfers the primary memory contents into a temporary memory circuit;
2. erases the relevant nonvolatile memory;
3. writes the retained contents back;
4. resets the alarm/control sequence.

The patent describes repeated reprogramming before the level separation reaches the terminal threshold, and its diagrams explicitly present recurring renewal at successive intervals as a way to keep valid states readable.

The specific circuit embodiment is **MNOS (metal-silicon nitride-silicon dioxide-semiconductor)** memory. That fact matters: this is strong prior art for a **nonvolatile-memory refresh relation**, not evidence that Flash already existed in this 1978 embodiment or that MNOS refresh and later floating-gate Flash refresh are one device genealogy.

The record also describes variants in which reprogramming is initiated when power is turned on, and a delayed power-off arrangement that allows reprogramming before supply removal. Those are execution-window variants around the same retention problem; they are not evidence of unpowered refresh.

### Engineering reconstruction

The bounded relation can be written as:

```text
slowly drifting nonvolatile state
        -> stricter proxy / early-warning threshold
        -> alarm
        -> temporary capture of intended payload
        -> erase + rewrite
        -> renewed read margin
```

Several separations follow:

> **nonvolatile != drift-free**

> **early-warning proxy != payload**

> **maintenance trigger != already-failed ordinary read**

> **refresh execution window != physical retention lifetime**

The second/sentinel memory is especially useful for this repository. It is not the user payload, but its deliberately earlier loss of margin can authorize work that preserves the payload. That is an early example of retention-policy evidence as a separate state relation.

### Limits

Do not infer from this source that:

- the 1978 embodiment is Flash, NAND, NOR, SSD, or FTL-based;
- its MNOS physical mechanism is identical to floating-gate retention loss;
- its warning circuit shipped in a named product;
- its public record establishes first invention or direct influence on later Flash designs.

---

## Source B — Intel, 1990 filing / 1993 publication: explicit Flash EPROM block refresh after disturb exposure

### Identity

- Albert Fazio, Gregory E. Atwood, and Neal R. Mielke, **“Floating gate non-volatile memory with blocks and memory refresh,”** US 5,239,505 A.
- Assignee: Intel Corporation.
- Filed / priority: **1990-12-28**.
- Published / granted: **1993-08-24**.
- Public record: <https://patents.google.com/patent/US5239505A/en>.

This is the first source in this addendum that is explicitly a **Flash EPROM** record.

### Historical record

Intel describes a blocked Flash EPROM in which high-voltage program/erase operations can electrically disturb cells outside the intended operation target. The patent distinguishes **gate disturbance** and **drain disturbance** and explains that repeated high-field operations can slowly program or erase unselected cells. The problem is therefore cumulative operational interference, not merely the passive passage of time.

The disclosed refresh path is tied to the block-erase operation. After an erase command completes on the selected block, refresh control scans the other memory addresses. A sense amplifier uses ordinary and elevated reference potentials to identify a programmed cell whose margin has weakened. If refresh is required, the control circuitry issues a program command and writes the data **back into the same addressed memory location**. The erased block is skipped; other locations are checked in sequence.

The refresh controller may be implemented as an internal state machine/on-chip controller or externally by a microprocessor. The patent therefore gives both the operation and possible control locus without proving which variant shipped.

### Engineering reconstruction

The bounded relation is:

```text
program/erase activity in blocked Flash
        -> cumulative gate/drain disturb exposure in other cells
        -> post-erase scan
        -> margin-sensitive read qualification
        -> same-location reprogram where needed
        -> renewed programming margin
```

This changes the Case-36 prior-art boundary in three important ways.

First:

> **explicit Flash refresh is publicly documented by 1993, earlier than the existing 1997/1999 floor.**

Second:

> **Flash refresh trigger != necessarily retention age.**

Here the trigger is coupled to high-voltage device activity and interference exposure. It is therefore an operation/disturb-maintenance regime, not the same trigger relation as Cai et al.'s retention-time/P-E-wear/ECC policy.

Third:

> **Flash refresh != necessarily relocation.**

The inspected Intel path reprograms weak data into the same addressed location. Later remapping-based refresh is one possible refresh geometry, not part of the definition of refresh itself.

### Limits

The source does not establish:

- NAND-specific read-disturb behavior;
- FTL mapping or SSD-level relocation;
- ECC-assisted reconstruction;
- passive long-term retention-age scheduling;
- named commercial deployment;
- influence on the 2012 FCR design.

Its `gate disturbance` / `drain disturbance` vocabulary and block-erase context must therefore remain historical to this source rather than being normalized into later NAND-controller terms.

---

## Source C — Texas Instruments, 1992 filing / 1994 publication: independent Flash refresh, margin restoration, and maintenance counters

### Identity

- John F. Schreck, **“Method and circuitry for refreshing a flash electrically erasable, programmable read only memory,”** US 5,365,486 A.
- Assignee: Texas Instruments Incorporated.
- Filed / priority: **1992-12-16**.
- Published / granted: **1994-11-15**.
- Public record: <https://patents.google.com/patent/US5365486A/en>.

This provides an independent same-era Flash-specific witness outside Intel.

### Historical record

TI explicitly describes a method and apparatus for **flash EEPROM refresh**. Its background again centers on disturb caused by high-voltage operations in electrically coupled wordlines/bitlines and sectors.

For a programmed cell, the refresh method can read at two control-gate voltages to distinguish a still-programmed but weakened/disturbed state. A disturbed programmed bit can then receive an additional, shorter program/restoration pulse that restores programming margin.

The same patent also treats the complementary case in which sector-level erase geometry matters. It can preserve a **memory record** of the intended cell states in RAM or another EEPROM sector, erase the affected sector, and reprogram it from that retained record. Thus even inside one patent, `refresh` does not name only one physical transition.

A particular embodiment includes an **erase-cycle counter** for electrically associated sectors and can enable refresh after a predetermined count. The patent also states that proactive sector state capture/reprogramming can be initiated after a predetermined number of erase cycles **or a predetermined amount of time**. It permits sector, partial-chip, or whole-chip refresh scopes.

The memory record/controller can be on-chip or off-chip; the patent explicitly notes that an on-chip embodiment can make refresh invisible to the outside system.

### Engineering reconstruction

The TI record separates at least four things that are often collapsed:

1. **disturb exposure** — the physical stress accumulated from neighboring/high-voltage operations;
2. **diagnostic margin evidence** — the two-reference read that distinguishes a weakened state before ordinary logical interpretation necessarily fails;
3. **maintenance-control state** — e.g. an erase-cycle count or time condition deciding when to run proactive work;
4. **renewal mechanism** — a restorative program pulse or, for a sector path, retained-state capture followed by erase/reprogram.

Therefore:

> **maintenance counter != payload age**

and:

> **same historical word `refresh` != one required rewrite geometry**.

The on-chip option also sharpens another repository distinction:

> **host/interface invisibility != absence of maintenance work**.

### Limits

The erase-cycle counter is a disclosed embodiment, not proof of a universal Flash controller state. The patent does not prove commercial deployment, FTL behavior, NAND-specific page/block organization, or the exact policy used by later SSDs. The optional time trigger does not by itself establish modern retention-age characterization or an empirical retention model.

---

## What this changes about the existing 1997–2009 prior-art map

The earlier addendum remains useful because it grounds later and more SSD-like relations: ECC-assisted refresh, idle/power-up scheduling, retained last-refresh time, relocation/remapping, explicit age/timestamp control, and erase-free rewrite refresh. This new addendum changes only its **starting floor**.

The old statement should now be read as:

> the 1997/1999 record was the earliest source in the previously inspected set, **not** the earliest publicly documented nonvolatile-memory or Flash refresh relation.

The newly inspected chronology is conservatively:

```text
1978 filed / 1980 public — Matsushita: nonvolatile-memory natural-decay warning -> capture -> erase/rewrite
1990 filed / 1993 public — Intel: explicit blocked Flash EPROM disturb scan -> same-location reprogram
1992 filed / 1994 public — TI: explicit flash EEPROM margin test -> restorative pulse or sector reconstruction
1997 filed / 1999 public — So/Wong: multilevel NVM refresh with ECC/error participation and richer scheduling
2000 filed / 2002 public — dynamic Flash refresh with relocation/mapping change
2004 priority / 2005 public — age/timestamp-triggered in-place or out-of-place Flash refresh
2007 filed / 2009 public — erase-free rewrite refresh triggered by time/drift/read errors
2012 — Cai et al.: measured 3x-nm MLC FCR design/evaluation with storage-time, wear, ECC, hybrid and adaptive policy
```

This is a **selected evidence sequence**, not a complete genealogy.

## Claims that must now be rejected or narrowed

The new primary record set rejects these shortcuts:

- `nonvolatile-memory refresh begins with Flash` — contradicted by the 1980-public Matsushita MNOS-bounded record;
- `explicit Flash refresh begins in the late 1990s` — contradicted by the 1993-public Intel record and independently corroborated by TI in 1994;
- `Flash refresh is inherently retention-age-driven` — Intel/TI prominently address operation-induced disturb;
- `Flash refresh necessarily relocates data` — Intel's inspected path performs same-location reprogramming;
- `refresh names one physical maintenance operation` — the three records include capture/erase/rewrite, same-location program restoration, and sector reconstruction;
- `refresh scheduling always requires a wall-clock history` — erase-command and erase-cycle-count triggers are direct counterexamples;
- `hidden/on-chip refresh is maintenance-free` — internalization changes interface visibility/control locus, not the existence of reads, tests, programming, or rewrite work.

## What remains distinctive in the bounded 2012 FCR case

Nothing in this slice removes the narrower Case-36 distinction already established for Cai et al. 2012. The FCR paper still provides an evaluated combination of:

- measured 3x-nm MLC NAND retention-error behavior;
- explicit storage-time / P-E-wear / fixed-ECC trade-offs;
- remapping-based and in-place paths in one named FCR design family;
- hybrid fallback keyed to the opposite/right-shift error population;
- per-block P/E-cycle information used to adapt refresh rate over device life;
- SSD/workload simulation quantifying reliability/endurance consequences, including conditions where more refresh can reduce lifetime.

The correct novelty posture is therefore:

> **earlier records establish many component refresh relations; FCR remains a distinct 2012 measured/evaluated policy combination, not the origin of generic Flash refresh.**

This is still not a patent-validity or invention-priority judgment.

---

## Cross-case controls

### Case 13 — early Flash erase geometry

Case 13 already establishes that coarse electrical erase creates preservation work for unaffected logical state. The Intel/TI patents add a different but related consequence of shared high-voltage geometry: operations aimed at one region can impose **disturbance debt** on other still-current cells/regions.

**Boundary:** erase-geometry coupling and disturb-triggered refresh are functionally connected but are not identical operations; this addendum does not rewrite Case 13's Toshiba/Intel genealogy.

### Case 52 — NAND read disturb

Case 52 shows a later NAND regime where repeated reads can disturb neighboring cells and trigger mitigation/relocation policies.

**Functional analogy only:** both regimes make ordinary activity create future retention work outside the immediate logical target. Intel/TI's early-1990s Flash EPROM/EEPROM high-voltage program/erase disturb is not NAND read disturb, and no direct genealogy is established.

### Case 36 — FCR

The older records establish refresh as a broad historical vocabulary/mechanism family before FCR. Case 36 remains distinct because its bounded trigger/evaluation center is **retention error accumulation under storage time + P/E wear + ECC capability**.

### Case 82 / Case 134 — relocation and integrity

Those cases show that copying/moving Flash data does not automatically imply ECC requalification or correction. The Intel 1993 path is useful as the opposite geometry counterexample: a refresh can renew a margin without relocating the logical data at all.

### Syntheses 24, 26, and 27

- **Synthesis 24:** Matsushita supplies condition/time-dependent renewal; Intel supplies operation-triggered refresh after erase; TI supplies disturb-count/time-triggered variants. `refresh` therefore crosses several trigger regimes even inside nonvolatile semiconductor memory.
- **Synthesis 26:** TI's erase-cycle counter and Matsushita's warning-state relation are examples of non-payload maintenance-control state with different persistence/authority questions.
- **Synthesis 27:** Matsushita's stricter-reference sentinel and Intel/TI's margin-sensitive reads show that preservation decisions can depend on proxy/threshold evidence before ordinary payload service fails.

These are **project-level functional comparisons**, not historical vocabulary imported into the patents.

---

## Philosophical limit

The bounded conceptual pressure is modest:

> A state can be materially classified as nonvolatile while its **continued admissibility as a reliably recoverable state** is maintained by periodic, condition-triggered, or activity-triggered renewal.

The early records also show that maintenance can be triggered by a relation to another state — a sentinel threshold, an operation count, a high-field event — rather than by the payload simply crossing from `present` to `absent`.

That does **not** justify saying that the patents theorized memory philosophically, that all nonvolatile storage is secretly volatile, or that every refresh mechanism is one form of recurrence. Those would collapse historical record into later interpretation.

---

## Related-repository audit

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `US5239505` and `flash refresh` found no dedicated overlapping case in this round.

Therefore:

- this addendum keeps only the retention-specific prior-art boundary needed by Case 36;
- a complete MNOS/Flash disturb genealogy, assignee/prosecution lineage, device-family deployment history, and semiconductor process evolution belong primarily in `computing-archaeology` if developed;
- no Matsushita -> Intel/TI -> FCR influence chain is asserted.

---

## Claim ledger

| Claim | Type | Strength | Evidence / limit |
| --- | --- | --- | --- |
| A 1978-filed / 1980-public Matsushita patent explicitly describes reprogramming nonvolatile memory before natural decay makes states indistinguishable | H/P | strong bounded prior art | US4218764A abstract + description; specific circuit embodiment is MNOS |
| Matsushita uses a stricter-reference nonvolatile monitor/sentinel to warn before the primary payload reaches its terminal read threshold | H/P | strong | US4218764A description |
| Matsushita can temporarily capture intended state, erase, and rewrite the nonvolatile memory after the warning | H/P | strong | US4218764A description |
| The 1980-public record proves Flash refresh | X | rejected | specific embodiment is MNOS; Flash identity is not established by this source |
| A 1990-filed / 1993-public Intel patent explicitly describes blocked Flash EPROM refresh | H/P | strong bounded Flash prior art | US5239505A field/background/refresh sequence |
| Intel's inspected refresh is tied to gate/drain disturbance from high-voltage operations and is invoked after block erase | H/P | strong | US5239505A description |
| Intel's inspected refresh can reprogram weak data back into the same addressed location | H/P | strong | US5239505A refresh sequence |
| All Flash refresh is retention-age driven or relocation-based | X | rejected | contradicted by Intel's disturb-triggered same-location path |
| A 1992-filed / 1994-public TI patent independently describes flash EEPROM refresh | H/P | strong bounded corroboration | US5365486A technical field + description |
| TI can detect weakened programmed state with two read levels and restore margin with an extra program pulse | H/P | strong | US5365486A Fig. 3 description |
| TI also discloses state capture plus sector erase/reprogram and permits erase-cycle/time triggers | H/P | strong | US5365486A Fig. 4–6 discussion |
| TI's erase-cycle count is complete payload-age history | X | rejected | it is a maintenance trigger/proxy for a bounded embodiment, not a chronology of each cell's state |
| On-chip refresh means no maintenance work occurs | X | rejected | TI makes interface invisibility a placement/control property while read/test/program work remains |
| These patents prove commercial deployment or direct influence on FCR | X | rejected | patent disclosure/similarity is insufficient for either claim |
| Generic nonvolatile refresh predates 2012 FCR by decades in the inspected public record | H/P/E | strong bounded chronology | 1980-public Matsushita + 1993/1994-public Flash-specific records |
| FCR remains distinct as a 2012 measured/evaluated NAND retention-aware policy combination | H/P/E | strong bounded distinction | Cai et al. 2012 + component-prior-art exclusions |

---

## Sources

1. Yukio Furuta and Tomisaburo Okumura, **“Non-volatile memory refresh control circuit,”** US 4,218,764 A, filed 3 October 1978, published/granted 19 August 1980, Matsushita Electric Industrial Co., Ltd.: <https://patents.google.com/patent/US4218764A/en>.
2. Albert Fazio, Gregory E. Atwood, and Neal R. Mielke, **“Floating gate non-volatile memory with blocks and memory refresh,”** US 5,239,505 A, filed 28 December 1990, published/granted 24 August 1993, Intel Corporation: <https://patents.google.com/patent/US5239505A/en>.
3. John F. Schreck, **“Method and circuitry for refreshing a flash electrically erasable, programmable read only memory,”** US 5,365,486 A, filed 16 December 1992, published/granted 15 November 1994, Texas Instruments Incorporated: <https://patents.google.com/patent/US5365486A/en>.
4. Yu Cai et al., **“Flash Correct-and-Refresh: Retention-Aware Error Management for Increased Flash Memory Lifetime,”** ICCD 2012, pp. 94–101, DOI `10.1109/ICCD.2012.6378623`; used only to preserve the later Case-36 comparison boundary.

## Evidence debt after this slice

1. pre-1978 nonvolatile-memory renewal/refresh genealogy;
2. non-patent academic/manufacturer records between the 1970s and the late 1990s;
3. exact family/prosecution histories and any Japanese/other-language priority records needed for invention-history work;
4. named commercial implementations of the 1980, 1993, or 1994 disclosed mechanisms;
5. direct citation/influence relations, if any, between these patent families and the later FCR literature;
6. device-level fault experiments separating passive retention loss, program/erase disturb, and read disturb across specific Flash generations;
7. broader semiconductor-memory/controller history, which belongs primarily in `computing-archaeology`.
