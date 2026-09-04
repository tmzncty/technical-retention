# Grounding Record 75 — NVMe Reservation Persistence, PTPL, and Preemption (2001–2019)

## Purpose

This record grounds [`cases/75-nvme13-reservation-persistence-ptpl.md`](../cases/75-nvme13-reservation-persistence-ptpl.md).

The bounded question is not “how do storage reservations work in general?” It is narrower:

> **Which non-payload relations does NVM Express Revision 1.3d require a reservation-capable namespace to preserve across resets, which of them may cross power loss, and how can those relations be deliberately replaced or forgotten?**

The main source is the ratified NVM Express Revision 1.3d specification. T10 SCSI persistent-reservation material is used to establish prior art and prevent an NVMe-first claim. NVM Express Revision 1.4 change notes are used only to mark a later clarification boundary.

---

## Source A — NVM Express Revision 1.3d

**NVM Express, _NVM Express Revision 1.3d_, ratified 20 March 2019.**

Official PDF:
<https://nvmexpress.org/wp-content/uploads/NVM-Express-1_3d-2019.03.20-Ratified.pdf>

### A1. Reservation support is optional; PTPL state belongs to the reservation-capable namespace

**Location:** §8.8, printed pp. 254–255 in the PDF.

The specification states that reservation support by a namespace/controller is optional, identifies support through `RESCAP` / `ONCS`, and requires the associated Reservation Report, Register, Acquire, Release, notification, Host Identifier, and Reservation Persistence facilities when reservations are supported.

It further requires a namespace supporting reservations to support **Persist Through Power Loss (PTPL) state**.

### Supports

- `reservation support ≠ universal NVMe requirement`;
- `reservation support ≠ PTPL currently enabled`;
- PTPL is namespace-associated control state, not a global statement that “the SSD is persistent.”

### Does not support

- a claim that all NVMe namespaces implement reservations;
- a claim that all reservation-capable namespaces always retain reservations through power loss;
- any physical implementation claim for reservation metadata.

---

## Source B — Reservation Persistence Feature

**Same specification, §5.21.1.21, printed p. 172 / PDF page carrying Figure 167.**

The standard says each namespace supporting reservations has a **Persist Through Power Loss (PTPL)** state. It may be changed with Set Features or Reservation Register.

Figure 167 gives the decisive behavior:

- PTPL set to `1`: reservations and registrants persist across power loss;
- PTPL cleared to `0`: reservations are released and registrants are cleared on power on.

The 1.3d text also says the Reservation Persistence feature **should not** support a saveable value, while acknowledging the possibility that a saveable value is supported.

### Supports

- `PTPL state ≠ reservation/registrant state`;
- `retention policy can itself be retained control state` as an engineering reconstruction;
- power loss can intentionally forget authority relations while user payload remains a separate state class;
- `PTPL = 0` is an access-authority forgetting rule, not a media-erasure rule.

### Does not support

- one physical medium for PTPL or reservation keys;
- secure erasure of any reservation metadata embodiment;
- user-payload loss when PTPL is zero.

---

## Source C — Reservation Register and CPTPL

**Same specification, §6.11, printed pp. 200–201, especially Figures 221–222.**

Reservation Register registers, unregisters, or replaces a reservation key. `CPTPL` permits the command to:

- leave PTPL unchanged;
- set PTPL to zero;
- set PTPL to one.

The command carries current/new reservation keys (`CRKEY`, `NRKEY`) for the defined actions.

### Supports

- registration identity/key state is separate from reservation-holder state;
- a host operation can change both registration state and the policy governing power-loss retention;
- `CPTPL` is an operation on the PTPL policy, not itself a reservation type.

### Version boundary

NVM Express's **Changes in NVMe Revision 1.4** page records a later clarification of how CPTPL interacts with a saveable Reservation Persistence Feature. That clarification should not be silently rewritten into the historical 1.3d wording.

Source:
<https://nvmexpress.org/changes-in-nvme-revision-1-4/>

---

## Source D — Reservation types and reset/power-loss boundary

**Revision 1.3d, §8.8.3 and surrounding text, printed pp. 256–257, especially Figures 266–267.**

The standard defines six reservation types and maps holder/registrant/non-registrant status to allowed or conflicting read/write/administrative command groups.

Immediately after the reservation-type description it states:

- registrations and reservations persist across Controller Level Resets and NVM Subsystem Resets;
- the exception is reset due to power loss;
- retention across a reset due to power loss may be configured using PTPLS.

### Supports

- `payload presence ≠ access permission`;
- `controller/subsystem reset ≠ power loss`;
- `reset-persistent authority ≠ power-loss-persistent authority`;
- reservation state is operational because it changes whether otherwise-valid commands are accepted or rejected.

### Does not support

- a claim that a reservation survives every conceivable failure;
- a claim that reservation metadata has the same durability envelope as namespace payload;
- a claim that Host Identifier, registration key, reservation type, and holder status are one indivisible datum.

---

## Source E — Acquire, Release, Clear, and Preempt

### Reservation Acquire

**Revision 1.3d, §6.10 and §8.8.5/§8.8.7.**

`Reservation Acquire` supports:

- Acquire;
- Preempt;
- Preempt and Abort.

The command carries a current reservation key and, for preemption, a preempt reservation key.

### Reservation Release

**Revision 1.3d, §6.12 and §8.8.6/§8.8.8.**

`Reservation Release` distinguishes:

- Release;
- Clear.

Only a reservation holder can perform an orderly release under the defined key/type rules. Clear is a separate action.

### Preempt

**Revision 1.3d, §8.8.7, printed pp. 258–260.**

For defined cases, preemption atomically changes registration/reservation relations: matching registrants can be unregistered, an existing reservation released, and a new reservation created for the issuing host.

For **Preempt and Abort**, controllers associated with preempted hosts are requested to abort commands being processed for the namespace. The standard explicitly says the abort side effect is **best effort** and that requested commands may already be too far along to abort; command completion waits until they are aborted or otherwise completed.

### Supports

- `authority transfer ≠ payload relocation`;
- `explicit release ≠ clear ≠ PTPL-triggered power-loss forgetting`;
- `preempt ≠ physical erase`;
- `Preempt and Abort ≠ guaranteed instantaneous cancellation of all in-flight work`.

---

## Source F — Reservation Report and GEN

**Revision 1.3d, §6.13, printed pp. 202–204, especially Figure 229.**

Reservation Report returns current reservation/registration status. The structure contains:

- `GEN`, a 32-bit wrapping counter;
- reservation type;
- number of registered controllers;
- PTPLS;
- registered-controller structures.

GEN increments for specified successful reservation operations, including Reservation Register, Clear, Preempt, and Preempt and Abort.

### Supports

- current reservation status includes both authority state and a compressed change indicator;
- `GEN ≠ complete authority history`;
- `current-state report ≠ append-only event log`.

### Cross-case boundary

This is intentionally distinct from Case 66's NVMe Persistent Event Log. PEL is an event-history mechanism with its own retention and retrieval rules; Reservation Report primarily presents current authority state plus a wrapping change counter.

---

## Source G — SCSI prior art: SPC-2 / SPC-3 persistent reservations

### G1. SPC-2 Revision 20, 18 July 2001

Public draft mirror:
<https://13thmonkey.org/documentation/SCSI/spc2r20.pdf>

The draft already describes persistent reservations and explicitly states that a persistent reservation may be released by loss of power when persist-through-power-loss capability is not enabled. The `APTPL` mechanism determines whether reservation keys/reservations survive power loss.

This source is used conservatively because the accessible copy is a public mirror rather than the principal official source for the NVMe case.

### G2. T10/01-099r5, 3 January 2002

Rob Elliott, Compaq Computer Corporation, **“SPC-3 Letting persistent reservations ignore target ports.”**

Official T10 PDF:
<https://www.t10.org/ftp/t10/document.01/01-099r5.pdf>

The proposal's suggested SPC-3 text states that:

- persistent reservations support dynamic contention resolution in multi-initiator systems;
- initiators register reservation keys;
- reservation keys support identification and preemption;
- `APTPL` can preserve registration keys and persistent reservations across power cycles;
- reset and power-cycle retention are explicitly distinguished.

### Prior-art conclusion

By 2001–2002, SCSI persistent-reservation work clearly already combined:

```text
registration keys
+ reservation ownership/type
+ preemption
+ optional persist-through-power-loss behavior
```

Therefore Case 75 must **not** claim that NVMe invented persistent reservations, reservation keys, preemption, or persist-through-power-loss reservation state.

The defensible historical claim is narrower:

> NVM Express Revision 1.3d provides a clear, normative NVMe instance in which namespace access authority is retained across ordinary reset and is separately configurable across power loss through PTPL.

---

## Repository reuse / duplication check

### `technical-retention`

Existing nearby cases are not substitutes:

- **Case 20** — NVMe VWC/FUA/Flush: payload/media persistence and ordering;
- **Case 30** — NVMe PMR: host-memory access and persistence barriers;
- **Case 44** — Deallocate/Sanitize: logical deallocation versus media forgetting;
- **Case 55** — SMART/Health: health/endurance telemetry;
- **Case 66** — Persistent Event Log: retained device-event history;
- **Cases 50/51** — HDFS fencing: distributed authority/fencing analogies;
- **Case 68** — Dynamo membership/failure boundary;
- **Case 72** — store-in cache currentness/castout authority.

Case 75 is the first bounded case centered on **storage-interface access-authority retention across reset/power-loss boundaries**.

### `computing-archaeology`

Searches for `NVMe reservation`, `PTPL`, and `persistent reservation` found no dedicated history. No technical-history passage was copied.

A broad SCSI RESERVE/RELEASE → persistent reservation → NVMe reservation genealogy would primarily be a `computing-archaeology` task if pursued later.

---

## Claim-strength ledger

| Claim | Evidence | Strength |
| --- | --- | --- |
| NVMe reservation support is optional | Rev. 1.3d §8.8 | strong / normative |
| A reservation-capable namespace supports PTPL state | Rev. 1.3d §8.8 | strong / normative |
| Reservations/registrations persist across controller/subsystem reset except power-loss reset | Rev. 1.3d §8.8.3 surrounding text | strong / normative |
| PTPL=1 preserves reservations/registrants across power loss | Rev. 1.3d §5.21.1.21 | strong / normative |
| PTPL=0 releases reservations and clears registrants on power on | Rev. 1.3d §5.21.1.21 | strong / normative |
| CPTPL can change PTPL as a Reservation Register side effect | Rev. 1.3d §6.11 | strong / normative |
| Registration/key state is distinct from reservation-holder/type state | Rev. 1.3d §§6.10–6.13, 8.8 | strong / normative |
| Preemption can atomically change authority relations | Rev. 1.3d §8.8.7 | strong / normative |
| Preempt-and-abort cancellation is best effort | Rev. 1.3d §8.8.7 | strong / normative |
| Reservation Report GEN is not complete history | Figure 229 + wrapping/selected-operation semantics | strong engineering reconstruction |
| Physical medium implementing reservation persistence is specified | no such evidence in inspected sections | rejected |
| NVMe invented persistent reservations / PTPL | contradicted by 2001–2002 SCSI evidence | rejected |
| Reservation clearing implies payload sanitization | no; different state class/commands | rejected |

---

## Historical record / engineering reconstruction / analogy boundary

### Historical record

Safe statements include:

- Revision 1.3d defines reservation registration, acquire/release/report, reservation types, PTPL, reset behavior, preemption, and current status reporting;
- T10 SCSI materials used persistent reservations and persist-through-power-loss semantics earlier.

### Engineering reconstruction

The following are project-level reconstructions rather than NVMe quotations:

- `retained access authority`;
- `authority durability`;
- `authority forgetting`;
- `retention policy can itself be retained state`;
- `payload durability ≠ authority durability`;
- `GEN ≠ complete authority history`.

### Functional analogy

Comparisons to HDFS fencing, Dynamo membership, store-in-cache currentness, or replicated leader epochs are functional only. They do not establish common implementation mechanisms or genealogy.

### Philosophical interpretation

The claim that retention may preserve a normative relation — “who may act” — is a later interpretation disciplined by the interface semantics. It is not attributed to NVMe or T10 authors.

---

## Open questions kept outside Case 75

1. Which named NVMe SSD/controller products preserve reservation state in which physical medium?
2. What do independent power-cut experiments show about PTPL conformance?
3. When exactly did reservations first enter the NVMe specification revision sequence?
4. How did SCSI SPC-2/SPC-3 persistent reservation semantics map into NVMe design decisions beyond the compatibility notes visible in 1.3d/1.4?
5. How do Linux DM multipath, clustered filesystems, Windows clustering, VMware, or other initiators actually use NVMe reservations in deployed fencing paths?
6. How do NVMe-oF discovery/controller failures interact with reservation state in concrete implementations?

These are valid later slices, but none is required to ground the bounded 1.3d semantics established here.

---

## Result

Case 75 can be marked **`grounded`**.

The decisive result is not merely that NVMe has reservations. It is the stronger decomposition:

```text
payload retention
≠
registration retention
≠
reservation-holder/type retention
≠
PTPL policy retention
≠
complete authority-transition history
```

and the failure-boundary correction:

```text
Controller Level Reset / NVM Subsystem Reset
≠
power-loss reset
```

NVM Express Revision 1.3d gives normative evidence for these distinctions, while earlier SCSI work prevents an invention-priority overclaim.
