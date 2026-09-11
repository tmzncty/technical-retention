# Case 146 grounding — Intel/AMD Flash erase suspend and pending-operation state, 1991–1998

## Status and purpose

**Grounding record for Case 146.**

This note supports one bounded claim:

> **By the mid-1990s, public Flash documentation exposed erase suspend/resume as a state-machine/service relation in which sector erase could remain unfinished while reads from unaffected sectors were admitted, after which a Resume command continued the pending erase.**

The evidence is deliberately split by source role:

- Intel `US5355464A` establishes a 1991-priority / 1994-public erase-suspend patent line;
- AMD's November-1996 Am29F040 datasheet supplies a named shipping-product interface contract;
- AMD's April-1998 Am29F040B documentation shows a later capability change rather than being silently backdated;
- Macronix's 1996-priority / 1998-public patent makes safe-checkpoint/state-machine latency explicit.

None of these sources is used to claim one cross-vendor implementation genealogy.

---

## 1. Source ladder

### 1.1 Intel `US5355464A` — 1991 priority, 1994 publication

**Type:** `H/P`, manufacturer patent.

Record:

- Assignee: Intel Corporation;
- title: **“Circuitry and method for suspending the automated erasure of a non-volatile semiconductor memory”**;
- priority date: **11 February 1991**;
- publication/grant date: **11 October 1994**.

Stable record:
<https://patents.google.com/patent/US5355464A/en>

The chronology must be stated as two dates. A patent priority date records a claimed priority relationship; it is not automatically evidence that the public could inspect the disclosure that day.

Accordingly:

> `1991 priority != 1991 public disclosure`.

The 1994 publication is the conservative public floor used for this patent family in Case 146.

### 1.2 AMD Am29F040 — November 1996

**Type:** `H/P*`, manufacturer-primary datasheet preserved through third-party archives.

Document identity:

- AMD Am29F040;
- `4 Megabit (524,288 x 8-Bit) CMOS 5.0 Volt-only, Sector Erase Flash Memory`;
- Publication **17113**;
- Revision **E**, Amendment/0;
- Issue Date **November 1996**.

Searchable archival copy:
<https://www.alldatasheet.com/datasheet-pdf/pdf/55458/AMD/AM29F040.html>

The first-page feature summary establishes:

- eight uniform 64-Kbyte sectors / sector erase architecture;
- Embedded Erase Algorithms;
- Data Polling / Toggle Bit status;
- `Erase suspend/resume`;
- support for reading data from a sector not being erased.

The command description further states that:

- Erase Suspend is valid during Sector Erase;
- the command is ignored during Chip Erase or the Embedded Program Algorithm;
- when suspend is requested during Sector Erase, the device can require up to **15 µs** to enter the suspended state;
- DQ7 and DQ6 status behavior indicates the state transition;
- the device defaults to `erase-suspend-read mode` after suspension;
- data reads in that mode must come from sectors not erase-suspended;
- `Erase Resume (30H)` resumes the erase operation.

These points establish a concrete named-product state machine at the interface level without requiring reverse engineering of its internal registers.

### 1.3 AMD Am29F040B — April 1998

**Type:** `H/P*`, manufacturer-primary preliminary datasheet preserved through third-party archives.

Document identity:

- AMD Am29F040B;
- Publication **21445**;
- Rev. **B**, Amendment/+2;
- Issue Date **April 1998**;
- marked `PRELIMINARY`.

Archival HTML rendering:
<https://www.datasheetbank.com/en/datasheet-html/276259/AMD/1page/AM29F040B.html>

The later document changes the advertised suspend service: while sector erase is suspended, the host may read **or program** a sector not selected for erasure. It also states that reading an address within erase-suspended sectors produces status data, and it gives a maximum **20 µs** suspend-entry delay for the documented path.

This source is useful precisely because it blocks a false continuity claim:

> `same product-family vocabulary != identical revision contract`.

Case 146 does not project the 1998 read+program feature back into the 1996 Am29F040.

### 1.4 Macronix `US5805501A` — 1996 priority, 1998 publication

**Type:** `H/P`, manufacturer patent.

Record:

- Assignee: Macronix International Co., Ltd.;
- title: **“Flash memory device with multiple checkpoint erase suspend logic”**;
- priority/filing date: **22 May 1996**;
- publication date: **8 September 1998**.

Stable record:
<https://patents.google.com/patent/US5805501A/en>

The patent's explicit contribution is a **multiple checkpoint** suspend algorithm. The erase flow contains precondition/pre-program work, erase-pulse work, and erase verification. Suspend checks can occur at several points so the controller need not wait for only one coarse boundary.

This is strong evidence for two limits on simplified reconstructions:

1. a host can issue a Suspend command before the device is actually in its suspended state;
2. the safe place at which high-voltage/state-machine work stops can matter to suspend latency.

The patent says the suspend procedure returns to the block-erase procedure to complete the erase. This supports `suspend != abort`, but it does not prove that every undocumented analog/internal progress variable is preserved literally across every implementation.

### 1.5 AMD 1994 Flash Memory Products Data Book — corroborative archival witness

**Type:** `H/P*`, manufacturer data book via Bitsavers.

Archive:
<https://bitsavers.org/components/amd/_dataBooks/1994_AMD_Flash_Memory_Products_Data_Book.pdf>

Search indexing for the archived book exposes Am29F040 material using `Suspend Erase/Resume` and describing suspension so data can be read in another sector of the same device. This is consistent with the later 1996 final datasheet.

Because this slice did not obtain a conveniently renderable page-level facsimile from the large archival PDF, the 1994 book is not used as the sole support for exact command timing or detailed state semantics. It is retained as corroboration and an earlier product-document lead for future archival cleanup.

---

## 2. Historical findings

### H1 — erase suspend was a public technical mechanism by 1994

The Intel patent provides a public 1994 floor for a Flash/nonvolatile-memory erase-suspend design, with a 1991 priority claim kept separately.

This does not establish first invention. Patent families and later references show adjacent earlier work on interruptible EEPROM/write operations, and those mechanisms are not silently relabeled as Flash sector erase suspend.

### H2 — by November 1996 AMD specified erase suspend/resume on a named Flash part

The Am29F040 is not merely a patent proposal. Its datasheet makes Erase Suspend/Resume part of the product contract and defines where ordinary reads are available while erase remains pending.

The safe historical statement is therefore stronger than `someone patented the idea` but narrower than `all 1990s Flash implemented it`.

### H3 — suspend scope is operation-specific

On Am29F040, Erase Suspend is for Sector Erase and is ignored during Chip Erase or the Embedded Program Algorithm.

Therefore:

> `one suspendable maintenance operation != universal device preemption`.

This also blocks a misleading analogy to a general CPU task scheduler.

### H4 — host request and device state are separate events

The documented maximum 15-µs delay means `B0 written` and `erase-suspended state reached` are not the same event.

Later checkpoint-oriented designs make the reason intelligible at a mechanism level: the device may need to leave high-voltage work at an admissible point before normal alternate service can be exposed.

### H5 — later revisions can widen the suspend-mode contract

The 1998 Am29F040B permits programming as well as reading non-erasing sectors during suspend. That feature is a later product-revision witness, not evidence that every earlier Am29F040 offered the same operation set.

---

## 3. Engineering reconstruction

### E1 — suspend retains a pending-operation relation

If a later Resume command is to continue an erase rather than start a new unrelated command, the device must preserve enough state to distinguish:

```text
idle / ordinary mode
    from
sector erase active
    from
sector erase suspended and still pending
    from
erase completed / failed
```

The evidence strongly supports this **interface-level state relation**. It does not justify inventing a universal internal register layout.

### E2 — pendingness is not payload

The suspended-state relation says what work remains admissible/required. It is not a replica of the target-sector payload and does not restore the old target contents.

Thus:

> `pending erase state != retained old payload`.

### E3 — suspend is neither completion nor abort

The strongest safe model is:

```text
active erase
    -> suspended pending erase
    -> resumed erase
    -> completion/failure
```

Suspension changes execution and access rules without retiring the transformation.

### E4 — exact physical progress is a separate claim

An interface may guarantee that erase resumes while the implementation repeats a pulse, re-enters verification, restores an address counter, or otherwise reconstructs execution state. The inspected sources do not prove one universal microarchitectural choice.

Therefore:

> `operation identity retained != every microstate/progress variable retained unchanged`.

### E5 — addressable does not mean ordinary payload-readable

During Am29F040-family suspend operation, the erasing sector participates in status determination while unaffected sectors may return ordinary data. The later B documentation is explicit that addresses within suspended sectors return status data.

Therefore:

> `physical/logical address supplied != ordinary payload-read authority`.

Operation state mediates what an address means at that moment.

### E6 — target-sector survival is not target-sector currentness

Mid-erase cells physically exist, but the interface does not promise that the old sector payload is a stable, authoritative value while erase is suspended.

Thus:

> `physical embodiment still present != old payload admitted as current`.

### E7 — control-state retention can be much smaller than the transformation it governs

A small amount of state-machine/status information can keep an erase of an entire sector logically pending. The size of retained control evidence need not scale with the payload whose future transformation it governs.

### E8 — nonvolatile array does not imply nonvolatile operation state

Nothing in the inspected suspend/resume contract says a suspended erase survives power removal. The product's low-VCC protection and array nonvolatility should not be converted into a power-fail-resumable-operation claim.

Therefore:

> `nonvolatile payload medium != power-loss-persistent pending-operation state`.

---

## 4. Functional comparisons and stop conditions

### Versus Case 13 — early Flash coarse erase

Case 13 grounds erase granularity and erase-before-rewrite asymmetry. Case 146 adds temporal/preemption semantics around later erase execution.

Functional relation:

```text
coarse / long erase work
    can motivate
foreground-service scheduling around erase
```

But the current evidence does not prove a direct product genealogy from Case 13's particular devices to Am29F040.

### Versus Case 145 — JFFS2

JFFS2 may retain logical/reclamation evidence around an erase block; Case 146 shows a chip-level erase operation itself can be pending/suspended. A filesystem's GC state is not the Flash chip's erase-suspend state.

### Versus Case 15 — SSD power-loss protection

Case 15 explicitly studies failure-triggered work needed to move volatile state into durable media. Case 146 has no equivalent evidence for preserving suspend state through power loss.

Do not write:

> `erase suspend = durable checkpoint`.

### Sanitization stop condition

Sector erase is a physical state-changing operation, but these sources define product programming/erase behavior, not a security sanitize guarantee. Suspend/resume says even less about forensic irrecoverability.

Do not write:

> `erase completed = secure sanitization`

without a separate security/interface source and implementation evidence.

---

## 5. Prior-art / genealogy boundary

The case uses chronology conservatively:

```text
Intel erase-suspend patent
  priority: 1991-02-11
  public patent: 1994-10-11

AMD Am29F040 final datasheet
  issue: 1996-11

Macronix multi-checkpoint patent
  priority: 1996-05-22
  publication: 1998-09-08

AMD Am29F040B preliminary datasheet
  issue: 1998-04
```

This permits statements about public evidence floors and later refinement. It does **not** establish:

- invention priority across the industry;
- private-development chronology;
- Intel → AMD copying;
- AMD → Macronix copying;
- one shared internal state machine.

Earlier NEC material on interrupting EEPROM/write work by a subsequent read request is relevant as a warning: **similar preemption function can predate the bounded erase-suspend line while operating on a different write/program mechanism**. A complete genealogy belongs in `computing-archaeology`.

---

## 6. Philosophical interpretation boundary

The engineering mechanism supports one narrow observation: technical systems can retain an unfinished relation whose meaning is prospective.

The suspended state is meaningful because a future command can still validly continue the transformation. That differs from a retained event log describing a completed past action.

However:

- this is not evidence of intention;
- it is not a psychological memory trace;
- it is not automatically archival history;
- it is not automatically durable across power loss;
- it is not automatically tertiary retention.

The philosophical gain comes from keeping the operation relation precise.

---

## 7. Related-repository check

Fresh searches of both `tmzncty/technical-retention` and `tmzncty/computing-archaeology` for the exact phrase `Erase Suspend` returned no existing dedicated case/study before this integration.

A future broad study of parallel-NOR command sets, Intel/AMD/Macronix product genealogy, execute-in-place constraints, simultaneous-read/write Flash, and later NAND suspend policy should be developed primarily in `computing-archaeology`; Case 146 should remain bounded to the retention semantics of pending operation state.

---

## 8. Findings contributed by this grounding

1. Intel's 1991 priority and 1994 public patent dates must not be collapsed.
2. AMD documented Erase Suspend/Resume on a named Am29F040 product by November 1996.
3. Sector Erase suspension does not imply Chip Erase or Program suspension.
4. A Suspend command and the device reaching a suspended state are separate events.
5. Resume establishes pending-operation continuation, not rollback of target payload.
6. A suspended operation remains unfinished even while other data becomes serviceable.
7. Other-sector availability does not restore target-sector ordinary read authority.
8. Operation/status state is control metadata, not a second payload copy.
9. Exact microarchitectural progress preservation is not established by interface-level Resume semantics.
10. Array nonvolatility does not prove suspended-control-state persistence across power loss/reset.
11. Am29F040B's 1998 read+program behavior must not be backdated into Am29F040's 1996 read-only suspend contract.
12. Macronix's checkpoint design shows suspend latency can be constrained by safe state-machine interruption points.
13. Similar earlier nonvolatile-write interruption is prior art for the broad function, not proof of erase-suspend mechanism identity.
14. Erase suspend is not secure sanitization and not a durable transaction checkpoint.

---

## 9. Sources

1. Intel Corporation, `US5355464A`, **Circuitry and method for suspending the automated erasure of a non-volatile semiconductor memory**, priority 11-Feb-1991, publication 11-Oct-1994: <https://patents.google.com/patent/US5355464A/en>
2. Advanced Micro Devices, **Am29F040 — 4 Megabit (524,288 x 8-Bit) CMOS 5.0 Volt-only, Sector Erase Flash Memory**, Publication 17113 Rev. E Amendment/0, November 1996, archival copy: <https://www.alldatasheet.com/datasheet-pdf/pdf/55458/AMD/AM29F040.html>
3. Advanced Micro Devices, **Am29F040B — 4 Megabit (512 K x 8-Bit) CMOS 5.0 Volt-only, Uniform Sector Flash Memory**, Publication 21445 Rev. B Amendment/+2, April 1998 preliminary, archival rendering: <https://www.datasheetbank.com/en/datasheet-html/276259/AMD/1page/AM29F040B.html>
4. Macronix International Co., Ltd., `US5805501A`, **Flash memory device with multiple checkpoint erase suspend logic**, priority 22-May-1996, publication 8-Sep-1998: <https://patents.google.com/patent/US5805501A/en>
5. Advanced Micro Devices, **1994 Flash Memory Products Data Book**, archival scan, Bitsavers: <https://bitsavers.org/components/amd/_dataBooks/1994_AMD_Flash_Memory_Products_Data_Book.pdf>
