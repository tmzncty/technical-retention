from pathlib import Path

CASE_PATH = Path('cases/146-flash-erase-suspend-pending-operation-state.md')
EVIDENCE_PATH = Path('evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md')
INDEX_PATH = Path('CASE_INDEX.md')
ROADMAP_PATH = Path('ROADMAP.md')

for p in (INDEX_PATH, ROADMAP_PATH):
    if not p.exists():
        raise SystemExit(f'missing required file: {p}')
for p in (CASE_PATH, EVIDENCE_PATH):
    if p.exists():
        raise SystemExit(f'{p} already exists; refusing duplicate/concurrent integration')

CASE = r'''# Flash Erase Suspend/Resume: Pending Erasure, Read Availability, and Operation-State Retention

## Status

**`grounded`** — bounded to the public 1991-priority/1994-published Intel erase-suspend patent line, AMD's November-1996 Am29F040 product contract, and later 1996-priority/1998-public refinements used only to expose checkpoint and capability boundaries.

Grounding record: [`../evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md`](../evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md).

## Scope

- **Object / system:** sector/block erase suspend and resume in 1990s parallel Flash memory.
- **Historical anchors:** Intel `US5355464A`, priority 11 February 1991 and publication 11 October 1994; AMD Am29F040, Publication 17113 Rev. E, November 1996; later Am29F040B and Macronix multiple-checkpoint material as bounded refinements.
- **Retention question:** when a long erase operation is temporarily suspended so other data can be serviced, what must remain true for the device to resume the *same pending erase obligation*, and why does suspension neither complete nor undo the target-sector state transition?

This is not a general history of NOR Flash, Flash command sets, real-time embedded execution, background operations, or SSD firmware. Case 13 already grounds early coarse-erase geometry; Case 145 separately grounds raw-Flash filesystem reclamation. Case 146 isolates the **operation-state** relation layered above erase physics.

The central bounded distinction is:

```text
erase requested / underway
        ↓
suspend request
        ↓
suspended erase remains pending
        +
other-sector access becomes available
        ↓
resume command
        ↓
pending erase continues toward completion
```

The retained relation is not a second copy of the target payload. It is the control/admission state by which the device continues to treat one erase as pending while temporarily exposing other operations.

---

## Historical vocabulary

Period and near-period sources use terms including:

- `erase suspend` / `Erase Suspend`;
- `erase resume` / `Erase Resume`;
- `sector erase` and `chip erase`;
- `Embedded Erase Algorithm`;
- `erase-suspend-read mode`;
- `state machine` / automated erase sequence;
- `Data Polling` and `Toggle Bit` status;
- `checkpoint` in the later Macronix refinement;
- `pre-program`, `erase pulse`, and `erase verify`.

Project terms used below — **pending-operation identity**, **operation-state retention**, **target-sector read authority**, and **temporary serviceability** — are engineering reconstructions, not claims about the vocabulary of Intel or AMD engineers.

---

## Retained state

The case contains at least three different state classes:

1. **array payload / cell state** — the floating-gate states being erased or left untouched;
2. **operation-control state** — whether sector erase is active, suspended, resumable, or complete, plus enough command/state-machine context to interpret a later Resume command;
3. **host-visible status/admission state** — status bits/mode behavior that distinguish ordinary array reads from erase progress/suspension and determine which accesses are accepted.

These should not be collapsed.

A suspended erase does not imply that the target sector's old payload remains an authoritative readable object. Conversely, the ability to read another sector during suspension does not imply that the target erase completed.

---

## Physical / logical substrate

The target payload is embodied in floating-gate Flash cells. Erase is a high-voltage, internally controlled physical process applied at sector/block scale in the bounded devices.

The suspend/resume relation is embodied in control logic/state-machine state and exposed through command decoding and status behavior. The inspected product documentation does not establish the exact transistor/register implementation of every retained control bit, and this case therefore stays at the command/state-machine contract level where the sources are strongest.

The relevant distinction is:

> **nonvolatile payload substrate != necessarily nonvolatile operation-control substrate**.

Nothing inspected here proves that an in-progress/suspended erase can survive loss of power and later resume. A Flash array can be nonvolatile while the control state of a pending operation is not.

---

## Historical record

### Intel public patent floor: suspend an automated erase so another read can be serviced

Intel's `US5355464A`, **“Circuitry and method for suspending the automated erasure of a non-volatile semiconductor memory,”** carries an 11-February-1991 priority date and was published/granted on 11-October-1994.

For chronology, those dates must remain separate:

> `1991 priority != 1991 public disclosure`.

The safe public-document floor used here is 1994 unless an earlier public source is independently established.

The patent title and later patent-family references establish a specific 1990s design problem: an automated erase sequence could occupy the nonvolatile memory long enough that a system needed a way to suspend erase, service another access, and later resume the erase sequence.

This case does **not** claim Intel invented every form of interruptible nonvolatile-memory operation. Earlier EEPROM/write-interruption material exists, and program/write interruption is not identical to sector erase suspend.

### AMD Am29F040: a named product contract by November 1996

AMD's Am29F040 datasheet, Publication 17113 Rev. E, Issue Date November 1996, documents a 4-Mbit, 5-V sector-erase Flash memory with eight uniform 64-Kbyte sectors.

Its feature list explicitly advertises:

- `Erase suspend/resume`;
- reading data from a sector **not** being erased;
- internal `Embedded Erase Algorithms`;
- Data Polling / Toggle Bit completion status.

The detailed command description says Erase Suspend is valid while sector erase is executing, is ignored during chip erase or the Embedded Program Algorithm, and causes the device to enter an erase-suspend-read mode. A Resume command (`30H`) resumes sector erase.

The product therefore supplies a concrete contract in which:

```text
sector erase is not complete
    +
sector erase is temporarily not executing normally
    +
unaffected-sector reads are admitted
    +
a later command resumes the pending erase
```

The document used here survives through datasheet archives rather than AMD's present website. It is treated as a manufacturer-primary document via an archival mirror (`H/P*`), not as an origin-hosted current AMD page.

### Suspension is not instantaneous in the named product

The November-1996 Am29F040 documentation gives a maximum delay of 15 µs from an Erase Suspend command during sector erase to the erase-suspended state. DQ7/DQ6 status behavior is then used to determine whether suspension has occurred.

Therefore:

> `suspend request != suspended state at the same instant`.

This is a small but important retention boundary. The host's request and the device's admitted operation state are distinct events.

### Am29F040B later broadens what can happen during suspension

AMD's Am29F040B preliminary documentation, Publication 21445 Rev. B Amendment/+2, Issue Date April 1998, describes Erase Suspend as permitting the host to read **or program** sectors not selected for erasure and gives a maximum 20-µs suspend latency in the documented path.

That later capability must not be silently projected backward into the November-1996 Am29F040, whose advertised suspend service is reading from non-erasing sectors.

Thus:

> `1996 Am29F040 suspend/read contract != 1998 Am29F040B suspend/read+program contract`.

Shared family naming does not make every revision's state machine identical.

### Later Macronix evidence exposes checkpoint semantics

Macronix `US5805501A`, priority 22-May-1996 and publication 8-September-1998, describes a **multiple checkpoint erase suspend algorithm**. Its related-art discussion identifies earlier erase-suspend work, while its own contribution is to increase the number of points at which an erase flow can safely stop: during preconditioning, erase-pulse application, erase verification, and boundaries between phases.

The exact implementation is later and vendor-specific, but it demonstrates why `Suspend` should not be modeled as magic instantaneous freezing of arbitrary analog activity. A controller/state machine can need a safe transition point before exposing the device as suspended.

The patent also says the suspend flow returns to the block-erase procedure to complete the erase. That supports the interface-level distinction:

> **suspend != abort**.

It does not prove that every physical pulse counter, address counter, or analog condition is preserved literally unchanged across every suspend implementation.

---

## Retention mechanism

### Pending-operation identity

A Resume command is meaningful only if the device still distinguishes a suspended erase from an idle/completed state.

At the interface level, the device therefore retains enough relation to answer:

- an erase remains pending;
- which sector(s) are implicated;
- ordinary access rules differ for those sectors;
- Resume should continue the erase workflow rather than begin an unrelated operation.

That relation may be very small compared with the sector payload, but it changes how the whole device is interpreted and what future commands are admissible.

### What is *not* established

The sources do not establish one universal internal representation such as a durable program counter or exact analog-progress checkpoint. They also do not prove persistence across:

- power failure;
- reset;
- device removal;
- brownout;
- controller replacement.

So the case grounds **powered operation-state retention**, not a crash-persistent transaction checkpoint.

---

## Addressing and access geometry

The AMD product contract makes access conditional on both address and operation state.

While an erase is suspended:

- normal array reads are admitted from sectors not selected for erase;
- the erasing/suspended sector is not thereby restored to ordinary read service;
- status information is used to determine erase/suspend state.

In the later Am29F040B documentation, reads at addresses inside erase-suspended sectors produce status data rather than normal array payload. This makes the admission relation especially explicit:

> **physical addressability != payload-read authority**.

The same numeric address can resolve to operation status rather than ordinary stored data depending on the device's retained mode/state.

---

## Read semantics

Reads of unaffected sectors are nondestructive ordinary reads in the bounded product contract.

The significant point is scheduling rather than read physics: suspend creates a temporal window in which other-sector data becomes accessible before the target erase finishes.

Therefore:

> `temporary read availability elsewhere != target erase completion`.

And, for the target sector:

> `target cells physically exist != old target payload is currently authoritative/readable through the ordinary array interface`.

The case does not claim that target cells have one simple, stable mid-erase value.

---

## Write and erasure semantics

### Erase

Sector erase is an internally managed sequence involving preparation/erase/verification work rather than one instantaneous logical bit flip.

### Suspend

Suspend requests a transition from active erase execution into a state in which the erase remains pending while certain other accesses become legal.

### Resume

Resume exits the suspended mode and continues the sector-erase operation toward its normal completion condition.

### Abort / rollback

Neither AMD nor the bounded patents establish Erase Suspend as rollback to the pre-erase payload. It is therefore incorrect to describe suspension as restoring the old sector.

Likewise, no source inspected here establishes that Resume means every implementation restarts at the exact transistor-level instant where high-voltage activity stopped. The strong claim is interface/state-machine continuation, not exact analog-progress identity.

---

## Time

Several timescales coexist:

- ordinary read access latency;
- sector-erase duration;
- host-to-device suspend-request latency;
- time spent in suspended mode;
- resume-to-eventual-completion time.

AMD's 1996 device documents a bounded suspend-entry latency, while the later Am29F040B changes both capability and the published latency figure. The Macronix checkpoint design makes the latency/state-machine relation explicit.

The key temporal lesson is:

> **a maintenance/state-transition interval can be interrupted without being retired**.

Pendingness can outlive one continuous execution interval.

---

## Maintenance and invisible work

Erase Suspend exists because erase is not free background nothingness. The memory performs hidden control work: command decode, preconditioning where required, high-voltage erase pulses, verification, status reporting, and state-machine transitions.

Suspend/resume adds more invisible work:

- detect a suspend request;
- reach or create a safe interruption point;
- preserve enough operation relation to remain resumable;
- expose alternate access without misreporting the erasing sector as normal data;
- re-enter the erase flow later.

Thus `background erase` is not absence of maintenance. It is scheduling and mediation of maintenance relative to foreground service.

---

## Failure / forgetting modes

Keep these distinct:

- **erase completes** — target sector reaches the device's erase completion criterion;
- **erase is suspended** — erase remains pending but execution/service rules change;
- **erase fails** — verification/retry policy cannot establish successful completion;
- **power/reset interrupts operation** — behavior is not established here as resumable;
- **logical deletion** — a higher-layer naming/currentness relation may be retired without invoking this exact device command;
- **reclamation erase** — a filesystem/FTL may request erase for reuse;
- **secure sanitization** — requires a separate contract and is not proved by erase-suspend semantics.

Suspending an erase is therefore neither forgetting nor preservation of the old payload. It is preservation of a **pending transformation relation** while the transformation is temporarily not being driven to completion.

---

## Engineering reconstruction

The bounded sources support the following decomposition:

```text
payload state
    != erase-operation state
    != command/admission state
    != host-visible status
```

A long erase can be pending while foreground access elsewhere proceeds. This shows that a storage device may have to retain not just values, mappings, and error history, but also **unfinished work identity**.

However, the reconstruction must remain interface-level. `Resume` proves a continuation relation; it does not prove bit-for-bit preservation of an undocumented internal microstate.

A useful invariant is:

> **unfinished technical work can remain current even while it is not actively executing.**

That is narrower than saying a machine “remembers what it was doing.”

---

## Functional analogies

### Case 13 — coarse Flash erase

Case 13 establishes coarse erase domains and asymmetric read/program/erase geometry. Case 146 adds a later operation-scheduling layer: long/coarse erase can be made preemptible enough to expose unaffected data before completion.

This is a functional/chronological comparison, not proof that Case 13's specific devices directly evolved into AMD's state machine.

### Case 145 — JFFS2 reclamation

JFFS2 may request erase to reclaim a raw-Flash block and separately retain evidence that erase completed before admitting reuse. Case 146 studies the lower device-level possibility that erase execution itself can be suspended and resumed. Filesystem reclamation state and chip-internal suspend state are not one mechanism.

### Case 15 — SSD power-loss protection

Both cases distinguish payload nonvolatility from volatile control/maintenance state, but Case 15 has explicit failure-triggered energy/durability concerns. Case 146 has **no evidence** that suspended erase state survives power loss. Suspend must therefore not be analogized to durable SSD transaction recovery.

---

## Counterexamples and limits

This case does **not** establish that:

- Intel invented all interruptible nonvolatile-memory operations;
- 11-February-1991 priority is a public disclosure date;
- AMD's 1996 product implements Intel's patented state machine;
- every Flash part supports erase suspend;
- chip erase is suspendable because sector erase is;
- a suspend request takes effect instantaneously;
- target-sector old data remains valid during suspension;
- Resume preserves exact analog progress or every internal counter;
- suspended state survives power loss/reset;
- an erase operation is secure sanitization;
- later Am29F040B read+program capability existed in the 1996 Am29F040 contract.

These limits are central to the case rather than cleanup trivia.

---

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated `Erase Suspend` study to reuse.

If future work becomes a broad genealogy of Intel/AMD/Macronix command sets, NOR architectural evolution, XIP/real-time Flash, or exact silicon state-machine implementation, it belongs primarily in `computing-archaeology`. `technical-retention` should keep the narrower comparison among pending-operation state, temporary availability, and physical erase progress.

---

## Philosophical / media-theoretical interpretation — bounded

Case 146 supports one modest claim: **technical retention can concern unfinished obligation as well as finished content**.

During suspend, the erase is neither simply present as completed history nor absent as cancelled work. A future Resume command remains qualified by a retained operation relation. Meanwhile other data can be made available without resolving the target transformation.

This can sharpen discussions of technical temporality because `current` need not mean `currently executing`: a suspended operation can remain current as unfinished work.

The mechanism does not justify calling the chip intentional, mnemonic in a psychological sense, or an archive of its own activity. Nor does a volatile state-machine relation automatically qualify as Stieglerian tertiary retention.

---

## Source ledger

### P1 — Intel `US5355464A` — `H/P`

Intel Corporation, **“Circuitry and method for suspending the automated erasure of a non-volatile semiconductor memory,”** priority 11-February-1991, publication/grant 11-October-1994:
<https://patents.google.com/patent/US5355464A/en>

Used for the public patent chronology and the bounded erase-suspend design line. Priority and public disclosure are kept distinct.

### P2 — AMD Am29F040, Publication 17113 Rev. E, November 1996 — `H/P*`

Manufacturer datasheet preserved through archival mirrors. Stable searchable copy:
<https://www.alldatasheet.com/datasheet-pdf/pdf/55458/AMD/AM29F040.html>

Used for named-product sector geometry, Embedded Erase Algorithm, Erase Suspend/Resume, non-erasing-sector read availability, suspend latency/status, and sector-erase versus chip-erase scope. Archival hosting is marked with `*`.

### P3 — AMD Am29F040B, Publication 21445 Rev. B Amendment/+2, April 1998 — `H/P*`

Manufacturer preliminary datasheet preserved through archival mirrors:
<https://www.datasheetbank.com/en/datasheet-html/276259/AMD/1page/AM29F040B.html>

Used only as a later refinement witness for read+program during suspend, target-sector status reads, and the changed suspend contract. It is not back-projected into 1996.

### P4 — Macronix `US5805501A` — `H/P`

Macronix International Co., Ltd., **“Flash memory device with multiple checkpoint erase suspend logic,”** priority 22-May-1996, publication 8-September-1998:
<https://patents.google.com/patent/US5805501A/en>

Used to ground the later explicit checkpoint/state-machine boundary and to show that suspend latency can depend on safe interruption points.

### P5 — AMD 1994 Flash Memory Products Data Book — `H/P*` corroboration

Archived AMD data book:
<https://bitsavers.org/components/amd/_dataBooks/1994_AMD_Flash_Memory_Products_Data_Book.pdf>

Searchable archival copies list Am29F040 `Suspend Erase/Resume` as allowing reads in another sector. Because exact page/facsimile inspection was not completed in this slice, it is corroborative rather than the sole anchor for a page-specific claim.

---

## Next work

- obtain a directly inspectable full facsimile/text rendering of `US5355464A` if an exact figure/claim-level implementation argument becomes necessary;
- identify a named Intel shipping part/manual tied directly to the 1991-priority patent line without inferring product implementation from patent ownership;
- test reset/power-fail behavior on a period-compatible part or emulator before making any persistence-across-reset claim;
- trace erase-suspend evolution into later simultaneous-read/write NOR and modern NAND only if the broader engineering history is developed in `computing-archaeology`;
- keep secure erase/sanitization and higher-layer reclamation as separate cases.
'''

EVIDENCE = r'''# Case 146 grounding — Intel/AMD Flash erase suspend and pending-operation state, 1991–1998

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
'''

CASE_ROW = '| [Flash Erase Suspend/Resume: Pending Erasure, Read Availability, and Operation-State Retention](cases/146-flash-erase-suspend-pending-operation-state.md) | **grounded** | sector/block erase + suspend/resume control state + status/admission mode + temporary non-target access | separate pending transformation from completion/abort; distinguish host suspend request from admitted suspended state; other-sector serviceability from target-sector payload authority; operation identity from exact microstate persistence | [1991–1998 grounding](evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md); exact Intel product tie, full early genealogy, reset/power-loss behavior, simultaneous-read/write evolution, silicon validation, and later NAND policy remain open |'

FINDINGS = r'''## Case 146 — Flash erase-suspend / pending-operation-state findings

Grounding record: [`evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md`](evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md).

- **3159 — 1991 priority != 1991 public disclosure:** Intel `US5355464A` claims 11-Feb-1991 priority but was published/granted 11-Oct-1994; the earlier date must not be presented as the public evidence date without another source. (`H/P`, `X`)
- **3160 — named-product erase-suspend contract by November 1996:** AMD Publication 17113 Rev. E specifies Am29F040 Erase Suspend/Resume and ordinary reads from sectors not being erased. (`H/P*`)
- **3161 — suspend request != suspended state:** the Am29F040 documents up to 15 µs to enter erase-suspended state after a suspend command during sector erase, so command issuance and admitted state transition are distinct events. (`H/P*`, `E`)
- **3162 — erase suspended != erase completed:** suspend changes execution/access mode while a later Resume command is still required to continue the sector erase toward completion. (`H/P*`, `E`)
- **3163 — erase suspended != erase aborted/rolled back:** Resume continues the pending erase; the bounded sources do not say suspension restores the target sector's pre-erase payload. (`H/P`, `H/P*`, `E`, `X`)
- **3164 — pending maintenance can outlive one continuous execution interval:** a sector erase can remain current as unfinished work while normal erase execution is temporarily paused and other service is admitted. (`E`)
- **3165 — unaffected-sector availability != target-sector payload authority:** during suspend, ordinary reads are admitted elsewhere while the erasing/suspended sector is not returned to ordinary payload-read service. (`H/P*`, `E`)
- **3166 — addressability != ordinary payload-read authority:** later Am29F040B documentation explicitly returns status data for addresses inside erase-suspended sectors, showing that retained operation mode mediates what an address yields. (`H/P*`, `E`)
- **3167 — operation-control/status state != payload replica:** suspend/resume state and DQ status qualify pending work/access; they are not another copy of the sector's user data. (`E`, `X`)
- **3168 — Resume continuity != exact microstate preservation:** an interface promise to continue erase does not prove every pulse counter, address counter, analog condition, or implementation state is preserved unchanged. (`E`, `X`)
- **3169 — array nonvolatility != power-loss-persistent suspend checkpoint:** the inspected sources do not establish resumption after reset/power removal, so Flash nonvolatility cannot be transferred to pending-operation control state. (`H/P*`, `E`, `X`)
- **3170 — Sector Erase suspend != universal operation preemption:** Am29F040 ignores Erase Suspend during Chip Erase or Embedded Program, making suspendability operation-scoped rather than a generic device scheduler. (`H/P*`, `E`, `X`)
- **3171 — 1996 Am29F040 contract != 1998 Am29F040B contract:** the later B revision allows read or program of non-erasing sectors during suspend; that widened capability must not be back-projected into the earlier read-oriented Am29F040 contract. (`H/P*`, `X`)
- **3172 — safe checkpoint semantics can bound suspend latency:** Macronix's 1996-priority/1998-public multiple-checkpoint design makes precondition, erase-pulse, and verify interruption points explicit; suspend need not mean instantaneous freezing of arbitrary internal activity. (`H/P`, `E`)
- **3173 — similar earlier write-interruption prior art != erase-suspend mechanism identity:** adjacent EEPROM/nonvolatile-write preemption can establish a broader functional prior-art floor without proving the same erase geometry, command semantics, or genealogy. (`H/P`, `A`, `X`)
- **3174 — related-repository / sanitization boundary:** fresh repository searches found no dedicated erase-suspend study in `technical-retention` or `computing-archaeology`; broad command-set/product genealogy belongs primarily in the companion repo, while Case 146 remains retention-specific and does not treat ordinary erase/suspend as secure sanitization. (`H/P` project-state record, `A`, `X`)'''

ROADMAP_ITEM = r'''- [x] Case 146 Flash erase-suspend / pending-operation-state slice — [`cases/146-flash-erase-suspend-pending-operation-state.md`](cases/146-flash-erase-suspend-pending-operation-state.md) + [`evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md`](evidence/146-intel-amd-1991-1998-flash-erase-suspend-grounding.md): Intel's 1991-priority/1994-public erase-suspend patent line and AMD's November-1996 Am29F040 product contract ground a state in which sector erase remains unfinished while unaffected-sector reads become available and a later Resume continues the pending erase. Later Am29F040B and Macronix checkpoint evidence are used only to expose revision/safe-transition boundaries. This closes the bounded `suspend != complete/abort`, `request != admitted suspended state`, `other-sector availability != target payload authority`, and `operation continuation != exact microstate/power-loss persistence` seams. Exact Intel shipping-product tie, early command-set genealogy, reset/power-loss behavior, simultaneous-read/write evolution, later NAND policy, and hardware validation remain open; broad Flash architecture history belongs primarily in `computing-archaeology`.'''

CASE_PATH.write_text(CASE.rstrip() + '\n', encoding='utf-8')
EVIDENCE_PATH.write_text(EVIDENCE.rstrip() + '\n', encoding='utf-8')

index = INDEX_PATH.read_text(encoding='utf-8')
if 'cases/146-flash-erase-suspend-pending-operation-state.md' in index or '3159 — 1991 priority != 1991 public disclosure' in index:
    raise SystemExit('Case146/index integration already present; refusing duplicate')

lines = index.splitlines()
row_pos = None
for i, line in enumerate(lines):
    if 'cases/145-jffs2-garbage-collection-negative-state-evidence.md' in line and line.startswith('| '):
        row_pos = i + 1
if row_pos is None:
    raise SystemExit('could not find Case145 table-row anchor in CASE_INDEX.md')
lines.insert(row_pos, CASE_ROW)
index = '\n'.join(lines).rstrip() + '\n\n' + FINDINGS.strip() + '\n'
INDEX_PATH.write_text(index, encoding='utf-8')

roadmap = ROADMAP_PATH.read_text(encoding='utf-8')
if 'Case 146 Flash erase-suspend / pending-operation-state slice' in roadmap:
    raise SystemExit('Case146 roadmap item already present; refusing duplicate')
phase_anchor = '## Phase 2 — Build missing technical bridges\n\n'
if phase_anchor not in roadmap:
    raise SystemExit('Phase 2 anchor missing from ROADMAP.md')
roadmap = roadmap.replace(phase_anchor, phase_anchor + ROADMAP_ITEM + '\n', 1)
ROADMAP_PATH.write_text(roadmap.rstrip() + '\n', encoding='utf-8')

print('integrated Case 146 canonical research files')
