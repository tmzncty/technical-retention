# Case 04 Deepening — Micron 2011–2014 Raw-NAND Erase Status and Reuse Authority

**Status:** `bounded deepening complete`

**Supports:** [`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md)

**Adjacent evidence:**

- [`04-m-systems-2001-2003-interrupted-erase-recovery-deepening.md`](04-m-systems-2001-2003-interrupted-erase-recovery-deepening.md)
- [`04-trueffs-2003-2004-mapping-power-failure-reconstruction-deepening.md`](04-trueffs-2003-2004-mapping-power-failure-reconstruction-deepening.md)
- [`04-samsung-2004-2010-nand-copyback-integrity-boundary-deepening.md`](04-samsung-2004-2010-nand-copyback-integrity-boundary-deepening.md)

## Purpose

Case 04 already establishes that logical invalidation, relocation, mapping publication, and later physical erase are distinct events. Evidence 04D further establishes a power-loss seam in which an interrupted erase must not be mistaken for a completed erase.

This packet asks a lower-level and deliberately narrower question:

> on a named raw-NAND family, what evidence distinguishes `the erase command is no longer busy` from `the erase succeeded`, and what does first-party bad-block guidance require when erase success is not established?

The bounded answer is unusually clear in Micron's documentation:

```text
erase command accepted
    -> die/LUN busy
    -> die/LUN ready
    -> host checks FAIL status
        -> success
        or
        -> erase error / block retirement path
```

This adds a source-controlled boundary that should not be silently collapsed into the higher-level word `reclaimed`.

The repository-level conclusion is:

```text
logical reclaim eligibility
    !=
erase command admission
    !=
operation no longer busy
    !=
erase success
    !=
allocator reuse of the block
```

`reuse authority`, `reuse eligibility`, and `completion authority` are **engineering-reconstruction terms used by this repository**. They are not Micron historical vocabulary.

---

## Evidence classes

- **H/P — Historical record / primary:** Micron device datasheet and Micron technical note / support guidance.
- **E — Engineering reconstruction:** relations inferred from the documented state transitions.
- **A — Functional analogy:** bounded comparison to other technical-retention cases.
- **I — Philosophical interpretation:** downstream conceptual consequence only.
- **X — Non-claim / stop condition:** claims that the inspected sources do not support.

---

## Source ledger

### S1 — Micron, 4Gb / 8Gb / 16Gb x8/x16 NAND Flash Memory, Rev. Q, April 2014 (`H/P`)

**Document family / root parts shown in the inspected PDF:**

- `MT29F4G08ABADAH4`
- `MT29F4G08ABADAWP`
- `MT29F4G08ABBDAH4`
- `MT29F4G08ABBDAHC`
- `MT29F4G16ABADAH4`
- `MT29F4G16ABADAWP`
- `MT29F4G16ABBDAH4`
- `MT29F4G16ABBDAHC`
- `MT29F8G08ADADAH4`
- `MT29F8G08ADBDAH4`
- `MT29F8G16ADADAH4`
- `MT29F8G16ADBDAH4`
- `MT29F16G08AJADAWP`

**Document identifier:** `m60a_4gb_8gb_16gb_ecc_nand.pdf`, Rev. Q 04/14 EN.

**Public copy inspected:** Texas Instruments E2E mirror of the Micron PDF:

<https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/791/1031.M60A_5F00_4GB_5F00_8GB_5F00_16GB_5F00_ECC_5F00_NAND_5F00_16BIT.PDF>

The document itself is Micron-authored first-party technical documentation. The current public copy inspected in this pass is a TI-hosted mirror rather than a current `micron.com` PDF URL.

Relevant printed-page anchors:

- printed p. 1: feature summary distinguishes the operation-status byte from `R/B#`;
- printed p. 25: Ready/Busy# semantics;
- printed pp. 54–55: status register / READ STATUS semantics;
- printed p. 77: ERASE BLOCK operation;
- printed p. 107: Error Management.

### S2 — Micron, TN-29-59, *Bad Block Management in NAND Flash Memory*, Rev. H, April 2011 (`H/P`)

**Document identifier:** `tn2959_bbm_in_nand_flash.fm`, Rev. H 4/11 EN.

**Public copy inspected:** Texas Instruments E2E mirror:

<https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/791/tn2959_5F00_bbm_5F00_in_5F00_nand_5F00_flash.pdf>

The note states that it covers Micron NAND Flash memory devices generally and separates:

- factory-generated bad blocks;
- bad blocks that develop during device lifetime;
- block replacement / remapping behavior.

The printed p. 3 `Block Replacement` page was directly inspected as a page image in this research pass.

### S3 — Micron NAND FAQ (`H/P`, current first-party support guidance)

Micron support FAQ:

<https://www.micron.com/sales-support/sales/faqs>

A regional Micron mirror may resolve the same content at `sg.micron.com`.

The NAND FAQ says to issue `READ STATUS` after PROGRAM or ERASE and says that an ERASE failure reported by status means the block should be retired.

S3 is used as current first-party corroboration, not as a 2011/2014 historical timestamp.

---

## Historical / technical record

### H1 — the datasheet distinguishes operation completion from pass/fail at the feature-summary level

The Rev. Q datasheet's first-page feature summary assigns two different observability roles:

- the **operation status byte** provides a software method for detecting operation completion, pass/fail condition, and write-protect status;
- **Ready/Busy# (`R/B#`)** provides a hardware method for detecting operation completion.

That wording already blocks a common collapse:

```text
R/B# says the target is no longer busy
    !=
R/B# alone says the erase passed
```

The device exposes a separate pass/fail result through status.

### H2 — Ready/Busy# is a readiness relation, not a success verdict

In the asynchronous-interface section, Micron defines a target as busy when one or more die/LUNs are busy and ready when all die/LUNs are ready.

The status-register table separately defines:

```text
RDY = 0 -> Busy
RDY = 1 -> Ready

FAIL = 0 -> successful PROGRAM / ERASE / READ
FAIL = 1 -> error in PROGRAM / ERASE / READ
```

The two fields therefore answer different questions:

```text
RDY: is the operation / target still occupied?
FAIL: did the relevant operation succeed?
```

This distinction is explicit device-interface semantics, not a repository analogy.

### H3 — ERASE BLOCK has an admission phase, a busy phase, and a post-ready qualification phase

For `ERASE BLOCK (60h-D0h)`, Micron documents the sequence:

1. the command is accepted when the die/LUN is ready;
2. the host writes `60h`;
3. it supplies the row-address cycles;
4. it concludes with `D0h`;
5. the selected die/LUN becomes busy for `tBERS` while the block is erased;
6. progress can be observed through `R/B#` or status operations;
7. once the die/LUN is ready, the host **should check the FAIL bit**.

The datasheet says this check verifies that the operation completed successfully.

The bounded relation is therefore:

```text
accepted erase command
    !=
completed erase interval
    !=
successful erase verdict
```

### H4 — the command's purpose is to prepare the block for later programming, but readiness still does not itself establish that purpose was achieved

Micron introduces the erase section by saying erase operations clear block contents to prepare pages for program operations.

That goal matters for retention semantics: physical erasure is not merely the disappearance of old logical meaning. It is also the medium-conditioning step that makes the block suitable for a later programming cycle.

However, the same section still requires a FAIL-bit check after readiness.

Thus the source does not support the shortcut:

```text
R/B# high
    -> block is automatically qualified for reuse
```

### H5 — the Error Management section requires status checking because media can fail to program or erase over time

The Rev. Q datasheet's Error Management section states that some memory locations may fail to program or erase properly over time and requires, among other precautions:

- always check status after PROGRAM or ERASE;
- use bad-block management;
- use wear-leveling algorithms.

This is first-party evidence that pass/fail qualification is not decorative interface metadata. It participates in continued safe use of the medium.

### H6 — Micron distinguishes factory bad blocks from developed / grown bad blocks

TN-29-59 says bad blocks can be present when a device ships or can develop during device lifetime.

It further states that additional bad blocks are identified when PROGRAM or ERASE attempts produce errors in the status register.

So this packet keeps two classes separate:

```text
factory-marked bad block
    !=
runtime-developed bad block
```

They may enter the same bad-block-management structure, but their evidence and chronology differ.

### H7 — factory bad-block markers themselves create a separate erase hazard

TN-29-59 says factory bad-block information must be read before erase because the marker is erasable and cannot be recovered after it is erased.

This creates a different relation from a runtime erase failure:

```text
factory bad-block evidence
    can itself be destroyed by erase
```

Therefore a controller cannot infer:

```text
no surviving factory marker after an erase
    -> block was originally good
```

The bad-block table is part of the retained interpretation needed to avoid using invalid blocks.

### H8 — TN-29-59 makes bad-block state operational by redirecting logical use away from the failed block

TN-29-59 says the bad-block table is saved in a good block and loaded into RAM at reboot; blocks in that table are not addressable, and bad-block-management software redirects FTL references to good blocks.

For developed bad blocks, the note describes skip-block and reserve-block methods.

In the reserve-block method:

- a user-addressable area and a reserved block area are maintained;
- bad blocks can be replaced by redirecting the FTL to a known free good block;
- the bad-block table tracks remapped developed bad blocks.

This is first-party evidence that a failure classification changes later admission / addressing behavior.

### H9 — current Micron support guidance makes ERASE failure → retirement explicit

Micron's current NAND FAQ says status should be checked after PROGRAM or ERASE.

It then gives an explicit control consequence:

```text
READ STATUS reports PROGRAM failure
    -> place the data elsewhere
    -> retire the programmed block

READ STATUS reports ERASE failure
    -> retire that block
```

The FAQ does not use the repository phrase `reuse authority`, but the operational consequence is strong: an erase-failed block does not continue as a normal block for future use.

---

## Engineering reconstruction

### E1 — `ready` is temporal completion, not success authority

The interface distinguishes:

```text
busy / ready
```

from:

```text
pass / fail
```

Therefore, at this raw-NAND boundary:

```text
operation stopped consuming the current execution interval
    !=
operation achieved its intended media transition
```

This is the central result of this slice.

### E2 — physical-space reclamation has a qualification phase below the FTL

A higher layer may already have decided that a physical erase block is a reclaim candidate because its old logical contents are obsolete or have been relocated.

But raw NAND adds another gate:

```text
logical reclaim candidate
    -> issue erase
    -> wait until ready
    -> inspect pass/fail
```

Only the successful branch can even become a candidate for ordinary free-block use.

Repository reconstruction:

```text
reclaim eligibility
    !=
reuse eligibility
```

The first can arise from mapping/currentness policy. The second additionally depends on successful medium preparation.

### E3 — successful erase and allocator admission are still not the same event

The Micron sources show erase success and bad-block retirement rules. They do **not** expose one universal FTL allocator implementation that says exactly when a successfully erased block is inserted into a free-block queue.

Therefore this packet deliberately stops at:

```text
successful erase
    -> medium-level prerequisite for later ordinary reuse
```

and does not claim:

```text
successful erase status
    ==
allocator free-pool insertion
```

That higher-level transition remains implementation-specific.

### E4 — failed destructive maintenance can reduce usable capacity rather than produce reusable space

The intended reclamation path is:

```text
old block no longer needed
    -> erase
    -> reusable space
```

But the failure path can be:

```text
old block no longer needed
    -> erase attempt
    -> FAIL
    -> retire block
    -> consume reserve / replacement capacity
```

So maintenance is not only a process that restores free capacity. It can also reveal media failure and permanently reduce the set of usable physical locations.

### E5 — bad-block state is retained control state

TN-29-59's bad-block table is saved in NAND and reloaded into RAM at reboot.

That table is not user payload, but it directly affects whether a physical block is admissible for later use.

For Case 04 this adds another retained-state class:

```text
user payload
    !=
logical-to-physical currentness map
    !=
allocation / reclaim state
    !=
bad-block / retirement state
```

A block can physically persist while control metadata says it is no longer a valid substrate for future logical state.

### E6 — the negative verdict can outlive the failed operation

An erase failure is transient as an event but can produce persistent policy state:

```text
erase attempt at t0
    -> FAIL
    -> block retirement recorded
    -> future operations avoid that block
```

The event disappears; the exclusion relation remains.

This is a particularly clear instance of the repository's central question: a later controller action is governed by state produced by an earlier failure moment.

### E7 — this is distinct from interrupted-erase uncertainty in Evidence 04D

Evidence 04D asks:

```text
power failed during erase;
was completion ever proven?
```

This packet asks:

```text
erase reached a status-verdict point;
did the device report success or failure?
```

The two negative paths must not be collapsed:

```text
completion not proven because execution was interrupted
    !=
completion reached but operation reported failure
```

Both can block ordinary reuse, but they arise from different evidence.

### E8 — retained bad-block metadata and retained erase-completion metadata solve different problems

Evidence 04D's pending/completed erase markers answer whether an interrupted operation earned completion status.

TN-29-59's bad-block table answers whether a physical block remains admissible after factory classification or later failure.

Thus:

```text
operation-history evidence
    !=
media-admissibility evidence
```

A robust mapped-Flash system may need both.

---

## Functional comparisons — not genealogy

### A1 — Case 24, Azure LRC source-replica retirement

Case 24 distinguishes:

```text
source replica scheduled for deletion
    !=
physical deletion
    !=
capacity reclamation
```

Case 04 adds a lower-level local-medium analogue:

```text
old Flash embodiment reclaimable
    !=
erase completed successfully
    !=
block available for future use
```

This is a comparison of control boundaries only. No Microsoft/Azure lineage from NAND bad-block management is asserted.

### A2 — Case 150, Micron background erase / planned power-down

Case 150 separates erase pending, executing, and completed at a managed-device control level.

This Case-04 packet adds the raw-NAND device-side distinction:

```text
not busy
    !=
passed
```

Again, this is functional comparison, not proof that the M550 firmware directly used the exact raw-NAND family documented here.

### A3 — Case 134, interrupted Copyback quarantine

Case 134 asks whether an interrupted physical relocation is qualified for later use.

The shared abstract relation is:

```text
physical operation attempted
    !=
new state qualified for admission
```

The command, failure mode, and historical source families remain different.

---

## Prior-art / terminology boundary

The Micron sources use historical/device vocabulary such as:

- `Ready/Busy#`;
- `RDY`;
- `FAIL`;
- `PROGRAM`;
- `ERASE`;
- `bad block`;
- `bad block table`;
- `skip block`;
- `reserve block`;
- `retired` in current Micron FAQ wording.

This repository uses the following only as analytical reconstruction:

- `reuse authority`;
- `reuse eligibility`;
- `completion authority`;
- `media-admissibility evidence`;
- `qualification phase`.

Do not quote those project terms back into 2011/2014 Micron documentation.

---

## Philosophical interpretation

### I1 — successful destruction can itself require evidence

Case 04 already shows that logical forgetting can precede physical erasure.

This packet adds a further complication: the destructive operation itself can finish in the temporal sense while still failing in the normative/engineering sense required for future use.

The exact technical fact is:

```text
ready
    !=
pass
```

The conceptual consequence is narrow:

> a state transition may require not only an operation but a retained judgment about whether that operation succeeded strongly enough to authorize the next state.

This is not a claim that NAND vendors were making a philosophical argument about authority.

### I2 — forgetting and future availability can diverge

A logical object can already have been retired while the physical region intended to replace that obsolete embodiment with fresh capacity fails its erase.

Thus one can lose the old logical obligation without gaining new physical availability.

The point is not metaphoric `memory loss`; it is an engineering asymmetry between:

- no longer needing the old payload;
- successfully producing a trustworthy medium state for future payloads.

---

## Explicit non-claims

This packet does **not** establish that:

1. every NAND vendor uses exactly the same status-bit layout;
2. every NAND generation uses the same bad-block-marker locations;
3. `R/B# = HIGH` means an erase failed or passed by itself;
4. every erase failure is caused by wear rather than another device/system condition;
5. every erase failure destroys all data in the block;
6. a failed block is physically removed from the chip;
7. a retired block can never be inspected by vendor diagnostics;
8. one failed erase always consumes one host-visible unit of capacity immediately;
9. successful raw-NAND erase automatically means an FTL allocator has inserted the block into its free pool;
10. a successful erase is equivalent to sanitization or secure deletion;
11. erase success proves indefinite future data retention;
12. Micron's 2011 TN-29-59 describes the firmware of every managed Micron SSD;
13. the 2014 raw-NAND family is the NAND media inside Crucial M550;
14. the current Micron FAQ wording can be backdated unchanged to 2011;
15. factory bad blocks and developed bad blocks have the same physical cause;
16. bad-block retirement and wear leveling are the same mechanism;
17. garbage collection and bad-block management are the same mechanism;
18. a bad-block table is identical to a logical-to-physical sector map;
19. the TI-hosted PDF mirror establishes independent archival custody equivalent to Micron's own current site;
20. the functional comparisons above establish historical influence or genealogy.

---

## Open evidence debt

The next useful work is now narrower than `find more NAND erase documentation`:

1. **Named FTL free-pool transition:** find a source-level or firmware/patent implementation that explicitly places a block into a free/reuse pool only after successful erase status.
2. **Erase-failure fault trace:** capture or locate a named raw-NAND/controller experiment showing `busy -> ready -> FAIL -> bad-block retirement/remap` end to end.
3. **Power-fail + FAIL interaction:** determine how a controller distinguishes `no trustworthy verdict because power died` from `completed command returned FAIL`.
4. **Retirement durability:** find a named implementation showing exactly when a newly developed bad-block record itself becomes crash-durable.
5. **Reserve exhaustion:** connect accumulated bad-block retirement to a documented capacity/end-of-life admission threshold without generalizing from one vendor.
6. **Managed-SSD boundary:** retain the distinction between raw-NAND status semantics and host-visible SSD behavior.

---

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `NAND bad block erase failure` and `MT29F` found no dedicated packet to reuse in this pass.

Accordingly, this file keeps only the retention-specific seam:

```text
operation readiness
    !=
operation success
    !=
future media admissibility
```

Broader Micron NAND product genealogy, NAND bad-block physics, ONFI status-command evolution, vendor comparisons, controller-driver history, and bad-block-management implementation history remain better candidates for `computing-archaeology`.

---

## Bounded conclusion

Micron's named raw-NAND documentation and bad-block guidance establish a control boundary that higher-level Flash accounts can easily hide.

An erase does not pass through one binary state called `done`.

At minimum the inspected device contract separates:

```text
ERASE accepted
    -> BUSY
    -> READY
    -> FAIL status checked
        -> success branch
        or
        -> failure / retirement branch
```

For Case 04, this means physical-space reclamation has a lower-level qualification step of its own. A block may be logically obsolete and may have finished an erase attempt in the temporal sense without thereby becoming a valid substrate for future writes.

The resulting engineering reconstruction is:

```text
logical invalidation
    !=
physical erase attempt
    !=
erase success
    !=
future reuse authority
```

That relation strengthens Case 04 without turning raw NAND into a generic SSD model and without projecting later controller vocabulary backward into Micron's device documentation.
