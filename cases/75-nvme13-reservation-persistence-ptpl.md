# NVM Express 1.3d Reservations: Retained Access Authority, PTPL, and Preemption

## Scope

- **Object / system:** the reservation facility of NVM Express Revision 1.3d, bounded to namespace registration/reservation state, reset and power-loss persistence, reporting, release, and preemption;
- **Date range:** principally the ratified 20 March 2019 Revision 1.3d semantics, with NVM Express Revision 1.4 change notes used only to mark a later clarification boundary and SCSI persistent-reservation material from 1998–2002 used as prior art;
- **Research question:** what must remain available so that a shared namespace continues to know **who is registered, who holds exclusion authority, and whether that authority survives resets or power loss**, independently of the user payload stored in the namespace?

This is not a general history of NVMe, multipath storage, cluster fencing, or SCSI reservations. Cases 20, 30, 44, 55, and 66 already cover other NVMe retention relations. The present case isolates a different one:

> **a storage system may need to retain access authority independently of the data whose access that authority controls.**

The primary source does not specify the physical medium in which reservation state is embodied. It specifies externally observable retention and forgetting semantics.

---

## Historical vocabulary and source boundary

The principal period vocabulary is supplied directly by NVM Express Revision 1.3d:

- `reservation`;
- `registrant`;
- `reservation holder`;
- `reservation key`;
- `Reservation Register`;
- `Reservation Acquire`;
- `Reservation Release`;
- `Reservation Report`;
- `Persist Through Power Loss (PTPL)`;
- `Change Persist Through Power Loss State (CPTPL)`;
- `Persist Through Power Loss State (PTPLS)`;
- `Preempt` and `Preempt and Abort`;
- `Reservation Conflict`;
- `Generation (GEN)`.

The phrases **retained access authority**, **authority-retention state**, **authority forgetting**, and **current exclusion relation** below are engineering reconstructions for this repository. They are not NVMe historical vocabulary.

The case also preserves one anti-anachronism boundary: NVM Express did not invent persistent reservations or power-loss-persistent reservation state. T10 SCSI work used `persistent reservation`, `reservation key`, preemption, and an `Activate Persist Through Power Loss (APTPL)` capability years earlier.[^spc2][^spc3]

---

## Retained state: not payload, but a permission relation

An NVMe namespace may contain user payload blocks, but reservation operation introduces another state class whose job is not to encode those blocks.

At minimum, the bounded reservation regime needs to represent relations including:

```text
host / Host Identifier
        ↓
registered reservation key
        ↓
registrant status
        ↓
reservation-holder status + reservation type
        ↓
which commands from which host classes are allowed or conflict
```

Revision 1.3d defines six reservation types: Write Exclusive, Exclusive Access, Write Exclusive – Registrants Only, Exclusive Access – Registrants Only, Write Exclusive – All Registrants, and Exclusive Access – All Registrants.[^nvme-res]

The command-behavior table then makes these states operational. Depending on reservation type and whether a host is a holder, registrant, or non-registrant, reads or writes that would otherwise address perfectly intact data may instead complete with `Reservation Conflict`.[^nvme-res]

Thus:

> **payload presence ≠ access permission**

and:

> **data durability ≠ authority durability**.

A byte can survive while a host loses the right to modify it. Conversely, an access-control relation can be cleared by power-loss policy while the namespace payload remains intact.

---

## Reset survival and power-loss survival are different regimes

Revision 1.3d makes a precise distinction that is easy to lose in generic statements such as “reservations are persistent.”

It states that registrations and reservations persist across **Controller Level Resets** and **NVM Subsystem Resets**, except reset due to power loss. Retention across power-loss reset is separately controlled by the namespace's PTPL state.[^nvme-res]

This creates at least three distinct questions:

```text
1. does the payload survive?
2. do reservation registrations / holder state survive an ordinary controller/subsystem reset?
3. do they survive loss of power?
```

The standard answers questions 2 and 3 separately.

Therefore:

> **controller reset ≠ power loss**

and:

> **reset-persistent authority ≠ power-loss-persistent authority**.

The distinction is not merely terminological. It changes who can resume access after a failure boundary.

---

## PTPL is retained policy about retained authority

Revision 1.3d gives each namespace that supports reservations a `Persist Through Power Loss (PTPL)` state. The state may be changed with Set Features or as a side effect of Reservation Register.[^nvme-ptpl]

Its semantics are explicit:

```text
PTPL = 1
    → reservations and registrants persist across power loss

PTPL = 0
    → reservations are released and registrants are cleared on power on
```

The controller also exposes `CPTPL` in the Reservation Register command so a registration operation can leave PTPL unchanged, set it to zero, or set it to one.[^nvme-register]

This gives a nested retention relation:

- the **reservation / registrant state** controls future access;
- the **PTPL state** controls whether that reservation / registrant state itself crosses a power-loss boundary.

In project terms:

> **retention policy can itself be retained control state.**

This does not imply that PTPL is stored in the same physical medium as user data or reservation keys. Revision 1.3d specifies behavior, not implementation substrate.

---

## Capability, current state, and physical implementation must remain separate

Several statements that sound similar are technically different:

1. a controller supports the NVMe reservation commands;
2. a namespace supports reservations;
3. a namespace has a PTPL state;
4. PTPL is currently set to `1`;
5. the implementation has some physical nonvolatile mechanism sufficient to honor that state.

Revision 1.3d makes reservation support optional, but if reservations are supported it requires the associated commands/features and requires a namespace supporting reservations to support PTPL state.[^nvme-support]

That does not mean PTPL must always be enabled.

So:

> **PTPL support ≠ PTPL enabled**

and:

> **specified persistence semantics ≠ specified physical persistence implementation**.

The standard intentionally leaves the latter below the interface.

---

## Registration and reservation are not the same retained relation

A host first becomes a **registrant** by registering a reservation key. A registrant may then acquire a reservation. Replacing a reservation key does not by itself alter an existing reservation.[^nvme-register][^nvme-res]

Likewise, unregistering can have different consequences depending on the reservation type and whether the unregistering host is the only or last holder.[^nvme-res]

This forces a separation between:

```text
registered identity/key state
and
current reservation-holder state
and
reservation type
```

A repository that collapsed all three into `lock state` would lose behavior that the interface itself exposes.

---

## Preemption: retained authority can be transferred without erasing payload

`Reservation Acquire` supports `Acquire`, `Preempt`, and `Preempt and Abort`.[^nvme-acquire]

For the bounded preemption paths, Revision 1.3d can atomically:

- unregister registrants whose keys match the preempt target;
- release an existing reservation;
- create a new reservation for the issuing host.

For `Preempt and Abort`, controllers associated with preempted hosts are also requested to abort commands being processed against the namespace. The standard explicitly qualifies that abort as **best effort**; completion waits until the requested commands are either aborted or otherwise completed.[^nvme-preempt]

This matters because:

> **authority transfer ≠ payload relocation**

and:

> **authority transition ≠ guaranteed instantaneous cancellation of every in-flight operation**.

The namespace bytes need not move for the recognized writer/holder relation to change.

---

## Release, clear, and power-loss forgetting are different operations

Revision 1.3d distinguishes an orderly `Release` from `Clear`, and also from power-loss behavior controlled by PTPL.[^nvme-release]

These should not be merged as one generic `unlock`:

- **Release** concerns a currently held reservation and is performed by a reservation holder under the defined key/type rules;
- **Clear** removes reservation state through the Reservation Release command's separate action;
- **PTPL = 0 followed by power loss/power on** causes reservations to be released and registrants cleared by failure-boundary policy rather than by an ordinary host release command.

Hence:

> **explicit release ≠ administrative clear ≠ power-loss-triggered authority forgetting**.

None of these operations is a media sanitization claim. They change access-control state, not necessarily user payload or stale physical traces.

---

## Reservation Report: current summary is not a complete history

`Reservation Report` returns current registration/reservation status and includes a 32-bit wrapping `Generation (GEN)` counter.[^nvme-report]

The counter is incremented for defined successful state-changing operations including Reservation Register, Clear, Preempt, and Preempt and Abort. It is useful evidence that reservation state changed, but it is not an append-only history of exactly what happened.

Because it wraps and because the status data structure reports current state rather than every prior transition:

> **reservation generation ≠ complete authority history**.

This is especially important beside Case 66. A Persistent Event Log is a retained event-history regime; Reservation Report is primarily a current authority-state report with a change counter. Similar words such as `generation` or `log` should not collapse those roles.

---

## Failure and forgetting modes

### Payload survives, authority is intentionally forgotten

If PTPL is zero, a power loss can clear registrations and release reservations even if the nonvolatile namespace payload survives.

### Authority survives ordinary reset but not power loss

The standard explicitly makes Controller Level Reset / NVM Subsystem Reset persistence stronger than the default power-loss case.

### Stale cluster assumption after authority loss

A higher-level cluster that assumes an old registration/reservation survived when PTPL policy caused it to disappear may no longer have the exclusion relation it expected. This is an engineering consequence, not a claim about a particular cluster product.

### Stale holder replaced by preemption

A registered host can use the prescribed key relation to preempt another registration/reservation. The old payload need not be deleted; what changes is which host relation the subsystem recognizes.

### In-flight command survives an abort request far enough to complete

`Preempt and Abort` is not proof that every in-flight command is stopped at the same instant. The standard calls the abort side effect best effort.[^nvme-preempt]

### Current-state report loses detailed history

GEN can show that defined changes occurred modulo wrapping, while the current report omits the full transition sequence.

---

## Historical record

### Primary / normative evidence

1. **NVM Express, NVM Express Revision 1.3d, ratified 20 March 2019.** Sections 5.21.1.21, 6.10–6.13, and 8.8 define reservation persistence, register/acquire/release/report commands, reservation types, reset behavior, preemption, and PTPL semantics.[^nvme]

2. **NVM Express, “Changes in NVMe Revision 1.4.”** The change record notes a clarification to the interaction between Reservation Register `CPTPL` and a saveable Reservation Persistence Feature. This is used only to prevent silent projection of later clarified wording backward into the 1.3d text.[^nvme14]

3. **T10 SPC-2 / SPC-3 persistent-reservation material, 1998–2002.** T10 documents already describe reservation keys, preemption, and an Activate Persist Through Power Loss capability that can preserve registrations and reservations across power cycles.[^spc2][^spc3]

### Related-repository check

A repository search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for NVMe reservations / PTPL / persistent reservations found no dedicated history to reuse. A future broader SCSI→NVMe reservation genealogy belongs there rather than being reconstructed inside this bounded case.

---

## Engineering reconstruction

### Finding 1 — retention can preserve authority rather than content

The reservation facility retains relations that determine **who may perform which operations** against already-addressable content.

This is technically consequential state even though it is not user payload.

### Finding 2 — durability has more than one object

A namespace can preserve its data while losing its reservation registration state, or preserve both.

The phrase `the storage survived power loss` is therefore underspecified unless it says **which state class** survived.

### Finding 3 — failure boundaries partition retention guarantees

Ordinary controller/subsystem reset and power loss are separate retention boundaries in the normative model.

A control relation may cross one and not the other.

### Finding 4 — authority-retention policy is second-order state

PTPL does not itself identify the reservation holder. It determines whether registrant/holder relations cross power loss.

The system therefore retains state **about how another state should be retained**.

### Finding 5 — compressed change evidence is not history

GEN gives a wrapping monotonic-like change indication over selected reservation operations. It does not preserve the sequence, actors, or payload of every prior authority transition.

---

## Functional analogies — bounded

### HDFS fencing — Cases 50 and 51

Both regimes show that data may remain physically present while retained protocol/control state determines whose commands remain admissible.

The analogy stops there. HDFS epochs and DataNode command fencing belong to a distributed filesystem control plane; NVMe reservations are namespace-level storage-interface semantics with reservation keys and defined command-conflict rules.

### Dynamo membership — Case 68

Both maintain non-payload state that affects future routing/access behavior. But membership/placement is not reservation ownership, and transient reachability suspicion has no direct NVMe PTPL equivalent.

### Store-in cache authority — Case 72

Both demonstrate that metadata can determine which surviving embodiment or actor currently counts. Cache currentness and writeback obligation are not access-exclusion reservations.

### NVMe Persistent Event Log — Case 66

PEL is retained device history. Reservation state is current access authority plus limited change evidence. `history retention` and `authority retention` should remain separate.

---

## Philosophical / media-theoretical interpretation — bounded

This case supports one narrow interpretation:

> **technical retention can preserve a normative relation — who is entitled to act — rather than only a representation of what happened or a payload to be read later.**

The stored bytes and the permission to alter them are different state classes with different failure boundaries. PTPL makes that distinction unusually explicit because the interface lets the system decide whether the authority relation itself crosses power loss.

This is not a historical claim that NVMe authors were formulating a philosophy of memory or normativity. It is a later conceptual use of the technical separation established by the standard.

---

## Counterexamples and limits

### `Persistent reservation` does not mean unconditional power-loss persistence

Revision 1.3d explicitly separates ordinary reset persistence from power-loss persistence through PTPL.

### PTPL does not prove one physical implementation

The standard specifies externally observable persistence semantics, not whether a controller uses NAND, NVRAM, capacitor-backed SRAM, replicated metadata, or another mechanism for reservation state.

### Reservation state is not user-data durability

A reservation can survive while payload correctness fails for unrelated reasons, and payload can survive while reservation state is cleared.

### Reservation Report is not an audit log

GEN is a wrapping counter over selected operations and the report gives current status. It does not preserve a complete event chronology.

### Preempt and Abort is not instantaneous global cancellation

The abort side effect is explicitly best effort; completion semantics do not justify a stronger claim.

### This case does not establish NVMe invention priority

SCSI persistent-reservation and persist-through-power-loss work clearly predates the NVMe 1.3d semantics used here.

---

## Compact comparison

| Relation | Revision 1.3d behavior | Must not be collapsed into |
| --- | --- | --- |
| Namespace payload | nonvolatile user data under the namespace | reservation/registrant state |
| Registration | host/key relation making a host a registrant | reservation holder status |
| Reservation | current access-exclusion relation + type | payload ownership or physical location |
| Controller/subsystem reset | registrations/reservations persist, except reset due to power loss | power-loss boundary |
| PTPL = 1 | reservations and registrants persist across power loss | proof of a specified physical metadata medium |
| PTPL = 0 | reservations released and registrants cleared on power on after loss | media erase or sanitization |
| Preempt | changes recognized registration/holder authority | payload migration |
| Preempt and Abort | authority transition plus best-effort abort requests | guaranteed instantaneous cancellation |
| GEN | wrapping change counter for defined reservation operations | complete historical log |

---

## Sources

[^nvme]: NVM Express, **NVM Express Revision 1.3d**, ratified 20 March 2019, <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_3d-2019.03.20-Ratified.pdf>.

[^nvme-ptpl]: Ibid., §5.21.1.21, “Reservation Persistence,” especially Figure 167: PTPL `1` preserves reservations and registrants across power loss; PTPL `0` releases/clears them on power on.

[^nvme-register]: Ibid., §6.11, especially Figure 221 (`CPTPL`) and Figure 222 (`CRKEY` / `NRKEY`).

[^nvme-acquire]: Ibid., §6.10, especially Figures 217–219 (`Acquire`, `Preempt`, `Preempt and Abort`, reservation types).

[^nvme-release]: Ibid., §6.12 and §8.8.6–8.8.8, distinguishing `Release`, `Clear`, preemption, and clearing.

[^nvme-report]: Ibid., §6.13, especially Figure 229 (`GEN`, `RTYPE`, `REGCTL`, `PTPLS`).

[^nvme-support]: Ibid., §8.8 opening requirements: reservation support is optional; controllers/namespaces that support it must expose the defined reservation and persistence facilities.

[^nvme-res]: Ibid., §8.8.2–8.8.6, especially Figures 266–267 and the reset/PTPL statement immediately following Figure 266.

[^nvme-preempt]: Ibid., §8.8.7, including the atomic registration/reservation changes and the best-effort abort qualification for `Preempt and Abort`.

[^nvme14]: NVM Express, **Changes in NVMe Revision 1.4**, reservation-register interaction clarification, <https://nvmexpress.org/changes-in-nvme-revision-1-4/>.

[^spc2]: T10/1236-D Revision 20, **SCSI Primary Commands - 2 (SPC-2)**, 18 July 2001; a publicly mirrored draft records persistent-reservation power-loss behavior and APTPL semantics: <https://13thmonkey.org/documentation/SCSI/spc2r20.pdf>. This is used only to establish pre-NVMe prior art, not as the principal normative source for this case.

[^spc3]: Rob Elliott / T10, **T10/01-099r5, SPC-3 Letting persistent reservations ignore target ports**, 3 January 2002, especially §§5.5.3.1–5.5.3.2 on reservation keys, preemption, and preserving persistent reservations with APTPL: <https://www.t10.org/ftp/t10/document.01/01-099r5.pdf>.

---

## Status

**`grounded`** — normative NVMe evidence directly establishes the retained reservation/registration relations, reset-versus-power-loss boundary, PTPL control, reporting, release, and preemption; T10 material blocks an NVMe-first prior-art claim. Physical implementation of reservation state, named-controller conformance under fault injection, and a full SCSI→NVMe genealogy remain separate future work.
