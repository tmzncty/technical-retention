# Flash Erase Suspend/Resume: Pending Erasure, Read Availability, and Operation-State Retention

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
