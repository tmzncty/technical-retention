from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"anchor missing in {path}: {old[:120]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_once(path: str, marker: str, addition: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if addition.strip() in text:
        raise SystemExit(f"addition already present in {path}")
    if marker not in text:
        raise SystemExit(f"required marker missing in {path}: {marker!r}")
    p.write_text(text.rstrip() + "\n\n" + addition.strip() + "\n", encoding="utf-8")


# Guard against replaying on a tree that already contains this research slice.
evidence_path = Path("evidence/146-intel-28f008sa-suspend-abort-power-boundary-deepening.md")
if evidence_path.exists():
    raise SystemExit("Intel 28F008SA evidence already exists")

case_path = Path("cases/146-flash-erase-suspend-pending-operation-state.md")
roadmap_path = Path("ROADMAP.md")
index_path = Path("CASE_INDEX.md")

case_text = case_path.read_text(encoding="utf-8")
if "### Findings 3780–3795" in index_path.read_text(encoding="utf-8"):
    raise SystemExit("CASE_INDEX findings already present")
if "Case 146 Intel 28F008SA named-product suspend / abort boundary deepening" in roadmap_path.read_text(encoding="utf-8"):
    raise SystemExit("ROADMAP item already present")

# A compact named-product evidence record. URLs are archival mirrors of Intel-authored documents;
# the claims are bounded to the visible product contract and do not assert patent-to-product descent.
evidence_path.write_text(r'''# Evidence 146C — Intel 28F008SA Erase-Suspend / Abort and Power-Control Boundary

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
''', encoding="utf-8")

# Case 146: add the new evidence to the status/navigation line.
old_status = "**`grounded`** — bounded to the public 1991-priority/1994-published Intel erase-suspend patent line, AMD's November-1996 Am29F040 product contract, Texas Instruments' 1998 TMS29F040 named-product microstate/power-transition contract, and later 1996-priority/1998-public refinements used only to expose checkpoint and capability boundaries.\n\nGrounding records: [`../evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md`](../evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md) + [`../evidence/146-ti-tms29f040-erase-suspend-microstate-power-deepening.md`](../evidence/146-ti-tms29f040-erase-suspend-microstate-power-deepening.md)."
new_status = "**`grounded`** — bounded to the public 1991-priority/1994-published Intel erase-suspend patent line, Intel's November-1995 / January-1996 28F008SA named-product contract, AMD's November-1996 Am29F040 product contract, Texas Instruments' 1998 TMS29F040 named-product microstate/power-transition contract, and later 1996-priority/1998-public refinements used only to expose checkpoint and capability boundaries.\n\nGrounding records: [`../evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md`](../evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md) + [`../evidence/146-ti-tms29f040-erase-suspend-microstate-power-deepening.md`](../evidence/146-ti-tms29f040-erase-suspend-microstate-power-deepening.md) + [`../evidence/146-intel-28f008sa-suspend-abort-power-boundary-deepening.md`](../evidence/146-intel-28f008sa-suspend-abort-power-boundary-deepening.md)."
replace_once(str(case_path), old_status, new_status)

# Case 146: add a bounded named-product historical section after the patent-line discussion.
case_anchor = "This case does **not** claim Intel invented every form of interruptible nonvolatile-memory operation. Earlier EEPROM/write-interruption material exists, and program/write interruption is not identical to sector erase suspend.\n\n### AMD Am29F040: a named product contract by November 1996"
case_insert = """This case does **not** claim Intel invented every form of interruptible nonvolatile-memory operation. Earlier EEPROM/write-interruption material exists, and program/write interruption is not identical to sector erase suspend.

### Intel 28F008SA: named product suspend/resume and abort boundary by 1995–1996

Intel's November-1995 28F008SA datasheet (Order Number `290429-005`) advertises `Erase Suspend Capability` for a named 8-Mbit FlashFile product with sixteen 64-Kbyte blocks, an integrated Command User Interface / state machine, and production package offerings. January-1996 application note AP-364 then exposes the product's WSM behavior in more detail.

During block erase, `B0H` requests suspend. Once the WSM reaches the suspended state, status distinguishes the mode, reads can be directed to blocks other than the target, and `D0H` transitions the WSM back to Erase. AP-364 explicitly says that the target block contains unknown data while suspended and that `VPP` must remain high through the suspend interval.

The same note distinguishes suspend from abort. `RP#` low / Deep Powerdown or low `VPP` aborts block erase, after which Intel tells software to repeat the block-erase sequence once system integrity is restored. Power-up and return from Deep Powerdown default the device to Read Array mode. Thus the product supplies a concrete named-device boundary:

```text
powered suspend + valid continuation conditions
    -> D0H resumes pending erase

reset/power-control abort
    -> fresh erase setup/confirm required
```

This closes the **named Intel product-behavior** gap but not the stronger genealogy claim. The shared Intel corporate lineage and compatible chronology do not prove that a particular 28F008SA silicon revision implements the exact circuitry or claims of `US5355464A`.

Detailed source treatment: [`../evidence/146-intel-28f008sa-suspend-abort-power-boundary-deepening.md`](../evidence/146-intel-28f008sa-suspend-abort-power-boundary-deepening.md).

### AMD Am29F040: a named product contract by November 1996"""
replace_once(str(case_path), case_anchor, case_insert)

# Strengthen the control-state/power paragraph without changing the physical-state boundary.
old_not_established = "The same TI product also resets command/control state to read mode below its low-VCC lockout threshold and on power-up. That is affirmative named-product evidence against treating its suspended erase as a crash-persistent transaction checkpoint. The exact cell-level condition of a power-interrupted target sector remains unspecified here, and the TI rule must not be projected onto every Intel/AMD/Macronix/later-NAND implementation.\n\nSo the case grounds **powered operation-state retention with transition-specific state projection**, not universal preservation of controller microstate and not crash-persistent transaction recovery."
new_not_established = "The TI product resets command/control state to read mode below its low-VCC lockout threshold and on power-up. Intel's 28F008SA independently supplies a related but separately documented product boundary: AP-364 requires maintained `VPP` through suspend, treats `RP#` low / low `VPP` as erase-abort conditions, requires a fresh block-erase sequence after abort, and defaults to Read Array on power-up / return from Deep Powerdown. These are product-specific control contracts; neither establishes the exact cell-level condition of a power-interrupted target sector, and neither rule may be projected onto AMD/Macronix/later-NAND implementations.\n\nSo the case grounds **powered operation-state retention with transition-specific state projection**, not universal preservation of controller microstate and not crash-persistent transaction recovery."
replace_once(str(case_path), old_not_established, new_not_established)

# Add the Intel application note to the source ledger before Next work.
source_anchor = "Used only as a later refinement witness for read+program during suspend, target-sector status reads, and the changed suspend contract. It is not back-projected into 1996.\n\n### P4 — Macronix `US5805501A` — `H/P`"
source_repl = """Used only as a later refinement witness for read+program during suspend, target-sector status reads, and the changed suspend contract. It is not back-projected into 1996.

### P6 — Intel 28F008SA datasheet (November 1995) + AP-364 (January 1996) — `H/P*`

Intel-authored product documentation preserved through archival mirrors:
<https://www.alldatasheet.com/html-pdf/66035/INTEL/PA28F008SA-85/132/1/PA28F008SA-85.html>
<https://intel-vintage-developer.eu5.org/DESIGN/FLCOMP/APPLNOTS/29209903.PDF>

Used for the named Intel product witness, `B0H` suspend / `D0H` resume WSM path, target-block `unknown data` boundary, maintained-`VPP` condition, reset/power-control abort distinction, and Read Array default after power-up / Deep Powerdown. Archival hosting is marked with `*`; no patent-to-product descent is inferred.

### P4 — Macronix `US5805501A` — `H/P`"""
replace_once(str(case_path), source_anchor, source_repl)

# Narrow the Next work item: the named product exists now; exact patent/product genealogy is what remains.
old_next = "- identify a named Intel shipping part/manual tied directly to the 1991-priority patent line without inferring product implementation from patent ownership;"
new_next = "- the 28F008SA now supplies a named Intel product/manual witness; still require direct documentary evidence before tying a particular 28F008SA silicon revision to the exact 1991-priority patent implementation, and keep exact first-shipment genealogy separate;"
replace_once(str(case_path), old_next, new_next)

# ROADMAP: add a completed bounded slice at the top of Phase 2.
roadmap_anchor = "## Phase 2 — Build missing technical bridges\n\n"
roadmap_item = """- [x] **Case 146 Intel 28F008SA named-product suspend / abort boundary deepening:** [`cases/146-flash-erase-suspend-pending-operation-state.md`](cases/146-flash-erase-suspend-pending-operation-state.md) + [`evidence/146-intel-28f008sa-suspend-abort-power-boundary-deepening.md`](evidence/146-intel-28f008sa-suspend-abort-power-boundary-deepening.md) add Intel's November-1995 28F008SA datasheet and January-1996 AP-364 as a named-product witness. The WSM keeps a powered suspended erase resumable with `D0H`, exposes other-block reads while target-block data is unknown, and requires maintained `VPP`; by contrast, reset/power-control abort is recovered by a fresh erase command sequence and the device defaults to Read Array after power-up / Deep Powerdown. This closes the bounded named-Intel-product behavior gap and fixes `suspend != abort/restart`, `resumable operation != valid target payload`, and `array nonvolatility != pending-control nonvolatility`. Direct 1991-patent-to-28F008SA implementation descent, exact first shipment, cell-state outcome after interruption, and hardware brownout testing remain open; broad NOR command-set and silicon genealogy belongs primarily in `computing-archaeology`.\n\n"""
replace_once(str(roadmap_path), roadmap_anchor, roadmap_anchor + roadmap_item)

# CASE_INDEX: continue from the verified previous tail (3779).
findings = r'''### Findings 3780–3795 — Case 146 Intel 28F008SA named-product suspend / abort boundary

- **3780 — H/P*** — Intel's November-1995 `28F008SA` datasheet (Order Number `290429-005`) advertises `Erase Suspend Capability` for the named 8-Mbit FlashFile product and documents an integrated Command User Interface / state machine.
- **3781 — H/P*** — Intel AP-364 (`292099-003`, January 1996) documents the 28F008SA WSM and gives separate block-erase, erase-suspend/resume, current/next-state, and background-erase flows.
- **3782 — H/P*** — During an active block erase, `B0H` requests suspend; after the WSM reaches suspend, `SR.7` and `SR.6` indicate the state and `RY/BY#` returns high.
- **3783 — H/P*** — In the suspended state, AP-364 permits reading blocks other than the one being erased and explicitly says the target block contains unknown data.
- **3784 — H/P*** — `D0H` Erase Resume transitions the WSM out of suspend and back to Erase; Intel requires `VPP` to remain at the high erase level throughout the suspend interval.
- **3785 — H/P*** — AP-364 says block-erase abort occurs when `RP#` goes low / Deep Powerdown is entered or `VPP` falls low, and directs software to repeat the block-erase sequence after system integrity is restored.
- **3786 — H/P*** — The 28F008SA defaults to Read Array mode at power-up and on return from Deep Powerdown, so the product documentation does not specify suspended WSM mode as a power-cycle-persistent checkpoint.
- **3787 — E** — `powered suspend != abort/restart`: Resume is a continuation command only while the suspended operation relation remains live; abort recovery requires a fresh erase setup/confirm sequence.
- **3788 — E** — `resumable erase obligation != authoritative target payload`: the pending erase can remain resumable while the target block's data is explicitly unknown.
- **3789 — E** — `nonvolatile Flash array != nonvolatile pending-operation control state`; product-level power/reset behavior separates payload substrate from the WSM continuation relation.
- **3790 — E** — Maintained `VPP` is part of the documented continuation conditions, so retention of the suspend/resume relation is conditional on external operating state as well as logical command state.
- **3791 — E** — Requiring a fresh erase command sequence after abort establishes loss of the immediate interface-level Resume relation, but does not establish that prior physical erase progress has been reset to zero.
- **3792 — A/E** — Intel 28F008SA and TI TMS29F040 both separate powered suspend/resume from reset/power interruption, but TI's documented pulse-counter reset must not be projected into Intel's undocumented internal progress state.
- **3793 — H/P*** — The named Intel product witness is dated November 1995 / January 1996, after the 1991-priority/1994-public patent line and before the November-1996 AMD Am29F040 witness; this is chronology, not proof of implementation descent.
- **3794 — X** — Shared Intel ownership, compatible dates, and similar vocabulary do not prove that a particular 28F008SA silicon revision implements the exact circuitry or claims of `US5355464A`; direct patent-to-product genealogy remains open.
- **3795 — X** — Erase Suspend, abort, repeat erase, target-block unknown data, and eventual successful block erase do not by themselves establish rollback, a known interrupted cell distribution, secure sanitization, or forensic non-recoverability.'''
append_once(str(index_path), "**3779 — X**", findings)

# Basic invariants before the workflow commits.
for p in [case_path, evidence_path, roadmap_path, index_path]:
    text = p.read_text(encoding="utf-8")
    if text.endswith(" \n"):
        raise SystemExit(f"trailing whitespace sentinel in {p}")

print("Case 146 Intel 28F008SA deepening patch applied")
