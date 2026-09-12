# Evidence 146C — Intel 28F008SA Erase-Suspend / Abort and Power-Control Boundary

## Scope

This note deepens Case 146 with a named Intel product witness rather than another patent-level description. Intel's November-1995 `28F008SA` datasheet and January-1996 application note AP-364 document a concrete FlashFile device whose internal Write State Machine (WSM) can suspend an in-progress block erase, admit reads from other blocks, and later resume that erase. The same product documentation distinguishes that powered suspend path from reset/power-control conditions that abort erase or return the device to Read Array mode.

The narrow question is:

> What survives a powered Erase Suspend on the Intel 28F008SA, and how is that different from an erase interrupted by reset/power-control conditions?

The bounded answer is that the **pending erase relation and WSM suspend mode remain live enough for an Erase Resume command**, while the target block is not promised to contain authoritative old data. Reset/power-control interruption does not expose the same Resume contract: Intel tells software to issue a fresh block-erase command sequence after system integrity is restored.

This is product evidence, not proof that the 28F008SA implements the exact circuitry or claim language of Intel's 1991-priority / 1994-published erase-suspend patent.

---

## Source identity and provenance

### P1 — Intel 28F008SA datasheet, Order Number 290429-005 — `H/P*`

- **Document:** *28F008SA — 8-MBIT (1-MBIT x 8) FlashFile Memory*
- **Manufacturer:** Intel Corporation
- **Document date:** November 1995
- **Order number:** `290429-005`
- **Product identity:** `28F008SA`; the document lists Erase Suspend Capability, sixteen 64-Kbyte blocks, an integrated Command User Interface / state machine, and TSOP / PSOP package offerings.
- **Accessible archival copies:** [AllDatasheet page-level mirror](https://www.alldatasheet.com/html-pdf/66035/INTEL/PA28F008SA-85/132/1/PA28F008SA-85.html); [Silicon-Ark archived Intel PDF](https://www.silicon-ark.co.uk/datasheets/28f008sa-datasheet-intel.pdf).
- **Evidence class:** `H/P*` — Intel-authored product documentation preserved by third-party archives.

The datasheet gives a named commercial-product contract before AMD's November-1996 Am29F040 witness already used in Case 146. It is not used here to establish first invention or first shipment.

### P2 — Intel AP-364, Order Number 292099-003 — `H/P*`

- **Document:** *28F008SA Automation and Algorithms*
- **Author:** Brian Dipert, MCD Marketing Applications, Intel
- **Date:** January 1996; copyright notice 1995
- **Order number:** `292099-003`
- **Accessible archival copy:** [Intel-vintage developer archive PDF](https://intel-vintage-developer.eu5.org/DESIGN/FLCOMP/APPLNOTS/29209903.PDF)
- **Evidence class:** `H/P*` — Intel-authored application note preserved on an archival mirror.

AP-364 is especially useful because it describes the 28F008SA WSM as a concrete device state machine and gives separate flows for block erase, erase suspend/resume, current/next WSM states, and background erase.

---

## Historical record

### H/P* — a named Intel 28F008SA product exposes erase suspend by late 1995 / early 1996

The November-1995 datasheet advertises `Erase Suspend Capability` for the 28F008SA and describes a 16-block, 8-Mbit FlashFile product with an integrated Command User Interface and state machine. AP-364 then gives the device-level command/state-machine behavior in January 1996.

This is a stronger product anchor than patent ownership alone:

```text
Intel patent line exists
    !=
therefore every named Intel product implements that patent

named Intel product documentation explicitly exposes erase suspend
    =
product-level evidence for the capability
```

The chronology is also bounded:

```text
1991 patent priority
< 1994 patent publication/grant
< November 1995 28F008SA datasheet
< January 1996 AP-364
< November 1996 AMD Am29F040 witness
```

Only the latter two Intel dates are used as product-document evidence here. The sequence does not by itself prove implementation descent from the patent.

### H/P* — suspend preserves a live WSM operation relation and changes admission

AP-364 says that while the WSM is executing block erase, writing `B0H` requests Erase Suspend. Once the WSM has suspended erase:

- `SR.7` (WSM status) and `SR.6` (erase-suspend status) are set;
- `RY/BY#` returns high;
- software may switch to Read Array mode and read a block other than the one being erased;
- `D0H` Erase Resume transitions the WSM out of suspend and back to Erase.

This grounds a concrete control relation:

```text
active block erase
  -- B0H / suspend transition -->
suspended pending erase + other-block read admission
  -- D0H -->
erase execution resumes
```

The command relation is observable through both the status register and `RY/BY#`; it is not merely a conceptual reconstruction imposed after the fact.

### H/P* — the target block is not restored by suspension

AP-364 explicitly warns that although any block is physically addressable, the block being erased when suspension occurs contains **unknown data**. The flowchart directs ordinary reads to a block other than the one being erased.

Therefore:

```text
pending erase remains resumable
    !=
pre-erase payload remains authoritative
```

Suspend preserves unfinished-work identity, not a rollback image of the target block.

### H/P* — continuation depends on a live power/control condition

Intel requires `VPP` to remain at the erase programming level throughout the suspend interval. AP-364 says that a transition to low `VPP` during suspension is detected and reported as a VPP error when Erase Resume is issued.

The same note separately states that block-erase abort occurs if:

- `RP#` (Reset/Powerdown) goes low and deep powerdown is entered; or
- `VPP` falls to the low level.

After such an abort, the documented recovery is to issue a **repeat block-erase sequence** after system integrity is restored.

That is a different interface contract from `D0H` Resume:

```text
powered suspend -> D0H resumes the pending WSM erase
abort/power-control interruption -> fresh erase setup/confirm sequence is required
```

The application note also says the 28F008SA defaults to Read Array mode at power-up and on return from Deep Powerdown. This is direct product evidence that the suspended WSM mode is not specified as a power-cycle-persistent checkpoint.

### H/P* — abort does not imply a known physical rollback point

AP-364's instruction to repeat block erase after an abort is a **control/API recovery rule**. It does not say that every erase pulse already applied has been undone, that the cell distribution returns to the pre-erase state, or that a restarted erase begins from physically pristine conditions.

The strongest supported statement is:

```text
immediate resume relation lost at the interface
    !=
physical erase progress proven reset to zero
```

---

## Engineering reconstruction

### Suspend, abort, and completion are three different states

For the bounded 28F008SA contract, a useful decomposition is:

```text
S = (T, M, A, P)

T = target block / pending erase relation
M = WSM mode and status
A = operations currently admitted to the host
P = physical cell / erase-progress state
```

A powered Erase Suspend visibly retains enough `T + M` to make `D0H` meaningful later and alters `A` so other-block reads become legal. The sources do not expose a complete representation of `P`.

On reset/power-control abort, software no longer receives the same suspended-operation continuation contract. It must establish a new erase command sequence. That supports:

```text
operation-control continuity != physical-state identity
```

and:

```text
payload nonvolatility != pending-maintenance-control nonvolatility
```

### `Resume` is not the same verb as `retry/reissue`

The product documentation itself separates two host actions:

- `Erase Resume (D0H)` while a valid powered suspend relation exists;
- repeat `Erase Setup / Erase Confirm` after an aborted operation.

This matters because both may ultimately pursue the same target postcondition — an erased block — but they rely on different retained control state.

A useful project formulation is:

```text
same desired postcondition
    !=
same continuation authority
```

### VPP is part of the continuation contract, not just background electricity

Because Intel explicitly requires `VPPH` through the suspend interval and diagnoses a low-VPP transition on Resume, the continuation relation is conditioned by an external electrical state as well as by logical commands/status.

This is not a claim that one voltage rail stores the operation identity by itself. It means the product-level retention contract is **conditional on maintained operating conditions**.

---

## Functional comparison — explicitly non-genealogical

### Texas Instruments TMS29F040 (Case 146B)

Both named products expose a powered erase-suspend / erase-resume relation and a separate reset/power boundary. The TI document additionally says its internal pulse counter is reset during suspend/resume; the Intel AP-364 material inspected here does **not** make that same statement.

Therefore the safe comparison is:

```text
shared functional boundary
    = powered suspend/resume is not the same as power/reset interruption

not established
    = identical progress variables, counters, checkpoints, or circuitry
```

The TI result must not be back-projected into the Intel WSM.

### Case 15 — SSD power-loss protection

Case 15 concerns explicit failure-triggered energy and durability mechanisms. The 28F008SA instead documents a pending operation whose live continuation contract depends on power/control conditions and falls back to reissuing erase after abort. The comparison is only the bounded distinction between nonvolatile payload substrate and volatile maintenance/control state.

---

## Rejected upgrades / limits

### X — no patent-to-product implementation descent claim

Intel's 1991-priority / 1994-published patent and Intel's 1995/1996 28F008SA product documents coexist in the same corporate lineage, but that alone does not prove that the exact patented circuitry, checkpoint structure, or claims were implemented in this silicon revision.

The named-product gap is narrowed; the **direct patent-to-product genealogy remains open**.

### X — no exact hidden progress-state claim

The WSM, CUI, status bits, commands, and external power conditions are documented. A complete internal register-transfer design, pulse counter set, analog threshold history, and charge-state trajectory are not.

### X — no rollback claim

Unknown target-block data during suspend and a requirement to repeat erase after abort do not imply restoration of the old payload or return to a known pre-erase physical state.

### X — no sanitization claim

Suspend, abort, retry, successful block erase, or power cycling do not by themselves establish secure sanitization or forensic non-recoverability.

### X — no universal NOR rule

This note is bounded to Intel 28F008SA documentation. It does not establish identical behavior for AMD Am29F040, TI TMS29F040, Macronix devices, later Intel FlashFile families, NAND, or managed SSDs.

---

## What this closes and what remains open

This deepening closes the bounded **named Intel product-behavior** gap in Case 146:

1. a November-1995 Intel 28F008SA datasheet explicitly advertises Erase Suspend Capability;
2. January-1996 AP-364 gives the actual `B0H` suspend / `D0H` resume state-machine path and target-block `unknown data` boundary;
3. the same product documentation distinguishes live powered Resume from reset/power-control abort followed by a fresh erase command sequence.

Still open:

- direct documentary linkage from the 1991-priority patent's claimed implementation to a particular 28F008SA silicon revision;
- exact first Intel shipping date and pre-November-1995 product genealogy;
- exact physical cell-state distribution after reset/power interruption at different erase phases;
- independent hardware brownout/reset tests;
- cross-vendor comparison of hidden progress state beyond what each manufacturer actually documents;
- later NOR/NAND suspend/abort genealogy.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for a dedicated `28F008SA erase suspend` study returned no reusable module. Broader NOR command-set, silicon-generation, and patent/product genealogy should be developed there rather than duplicated here.
