# Evidence 126 — NVMe Reservations / PTPL, 1998–2012

## Purpose

Ground the bounded Case 126 claim that **multi-host access authority can have a lifetime distinct from both namespace payload lifetime and controller lifetime**, and that NVM Express 1.1 gives reservation/registration state a separate power-loss persistence policy (`PTPL`).

The evidence record also establishes a conservative prior-art floor: a 1998 T10 Persistent Reservations proposal already describes reset-surviving reservations plus optional `APTPL` preservation across power cycles.

This record does not establish invention priority, direct SCSI→NVMe implementation genealogy, named-device conformance, or the physical nonvolatile representation used by NVMe controllers.

---

## P1 — NVM Express Revision 1.1, 11 October 2012

**Source:** NVM Express, *NVM Express Revision 1.1*, dated 11 October 2012.  
<https://www.nvmexpress.org/wp-content/uploads/NVM-Express-1_1.pdf>

### Exact anchors

#### Cover / date

- cover: `Revision 1.1`;
- date: `October 11, 2012`.

#### §1.4.1 — Multi-Path I/O and Namespace Sharing, pp. 10–12

The specification distinguishes multi-path I/O from namespace sharing. Namespace sharing means two or more hosts access a common shared namespace through different NVMe controllers. It says concurrent shared-namespace access requires coordination between hosts, while the procedure used for that coordination is outside the specification.

The dual-port example says a reset of one port affects its associated controller but not the other controller, the shared namespace, or the other controller's operations on that namespace.

**Claim supported:** controller/path lifetime can differ from shared-namespace lifetime.

#### §5.12.1.16 — Reservation Persistence, p. 104

The Reservation Persistence Feature (`83h`) assigns each namespace that supports reservations a namespace-specific **Persist Through Power Loss (`PTPL`) state**.

The defined behavior is:

- `PTPL = 1`: reservations and registrants persist across power loss;
- `PTPL = 0`: reservations are released and registrants are cleared on power loss.

The feature may be modified using Set Features or Reservation Register.

**Claim supported:** power-loss survival is controlled by a separate retained policy state.

#### Reservation Register — CPTPL, pp. 120–121

The `Change Persist Through Power Loss State (CPTPL)` field permits Reservation Register to alter PTPL as a side effect:

- `00b`: no change;
- `10b`: set PTPL to 0;
- `11b`: set PTPL to 1.

**Claim supported:** registration mutation and future power-loss-lifetime policy can be coupled in one command while remaining distinct semantic fields.

#### Reservation Report — PTPLS, p. 124

Reservation Report exposes `Persist Through Power Loss State (PTPLS)` together with registered-controller information.

**Claim supported:** PTPL is observable current state, not merely an undocumented implementation choice.

#### §8.7 — Reservations, pp. 155–158

The specification says reservations may be used by multiple hosts to coordinate access to a shared namespace and warns that incorrect application may corrupt data or impair system operation.

It requires reservation-supporting namespaces to expose reservation capabilities and support PTPL state.

Crucially, it states:

- reservations and registrations persist across all Controller Level Resets;
- they persist across all NVM Subsystem Resets;
- the exception is reset due to power loss;
- power-loss survival may be configured through namespace PTPLS.

**Claim supported:** `reset-surviving ≠ power-loss-surviving`.

### Limits

P1 does not reveal the controller's physical storage implementation for PTPL state, prove product conformance, or prove that a retained reservation makes application recovery correct.

---

## P2 — NVM Express 1.1 release announcement, 8 November 2012

**Source:** NVM Express Work Group, *NVM Express Work Group Releases 1.1 Specification*, 8 November 2012.  
<https://www.nvmexpress.org/wp-content/uploads/docs/NVMe_Press_Release_1-1_20121108.pdf>

The release announcement says NVMe 1.1 adds multi-port / multi-host support including Multi-Path I/O and namespace sharing, enhanced reset capabilities, and a simplified reservations mechanism compatible with SCSI reservations.

**Claim supported:** reservations were publicly presented by NVM Express as part of the 1.1 enterprise feature set.

**Limit:** a release announcement is not invention evidence and does not define the detailed PTPL contract by itself; P1 supplies the normative technical semantics.

---

## P3 — NVM Express SCSI Translation Reference, 24 June 2015

**Source:** NVM Express, *NVM Express: SCSI Translation Reference*, 24 June 2015.  
<https://nvmexpress.org/wp-content/uploads/NVM_Express_-_SCSI_Translation_Reference-1_5_20150624_Gold.pdf>

The reservation translation section states directly that **NVMe Reservation support was added in NVM Express 1.1**, then maps SCSI reservation types and commands to NVMe reservation operations.

**Claim supported:** the consortium's own later compatibility document confirms the 1.1 chronology.

**Limit:** translation compatibility is not proof of direct historical or implementation descent.

---

## P4 — T10/98-203 revision 3, 24 July 1998

**Source:** George Penokie (IBM), *Persistent Reservations*, T10/98-203 revision 3, 24 July 1998.  
<https://www.t10.org/ftp/t10/document.98/98-203r3.pdf>

### Exact anchors

#### §0.0.1 — Persistent Reservations management method, p. 1

The proposal describes a multi-initiator reservation mechanism intended to survive initiator failures and recovery actions. It states that persistent reservations are not reset by target reset/global actions and may be used to enforce device sharing among multiple initiators.

It also says reservation/registration service actions may require access to nonvolatile memory in the logical unit.

#### §0.0.1.1 — Preserving persistent reservations across power cycles, pp. 1–2

The proposal defines `Activate Persist Through Power Loss (APTPL)`.

When APTPL is enabled, the device server preserves registrations and persistent reservations across power cycles until disabled. The proposal enumerates the minimum retained information, including initiator identification, reservation key, scope, and type, and explicitly says the preservation capability requires nonvolatile memory within the logical unit.

**Claim supported:** by July 1998 a public T10 standards-development artifact already exposed the bounded relation:

```text
reset-surviving multi-initiator reservation
        +
optional power-cycle persistence
        +
retained identity/key/type information
```

### Limits

This is a standards-development proposal, not proof that July 1998 is the invention date, not a shipping-product witness, and not evidence that NVMe copied a particular SCSI implementation.

---

## Chronology and novelty boundary

| Date | Artifact | What may safely be claimed |
| --- | --- | --- |
| 24 Jul 1998 | T10/98-203r3 | public SCSI standards-development record for Persistent Reservations + APTPL semantics |
| 11 Oct 2012 | NVM Express 1.1 | ratified NVMe reservation/PTPL contract |
| 8 Nov 2012 | NVM Express 1.1 release announcement | consortium publicly positions reservations among 1.1 multi-host enterprise additions |
| 24 Jun 2015 | NVM Express SCSI Translation Reference | later official statement that Reservation support was added in 1.1; SCSI↔NVMe translation mapping |

Chronology is not genealogy.

The evidence supports an earlier SCSI-family prior-art floor and a later NVMe contract. It does not support an invention claim for either artifact or a direct line of implementation descent.

---

## Claim ledger

| ID | Type | Claim | Evidence | Strength / limit |
| --- | --- | --- | --- | --- |
| C126-01 | H/P | NVMe 1.1 is dated 11 Oct 2012 | P1 | strong |
| C126-02 | H/P | reservations are an NVMe 1.1 addition | P2, P3 | strong institutional chronology |
| C126-03 | H/P | shared namespace may outlive one controller/port reset | P1 §1.4.1 | strong bounded example |
| C126-04 | H/P | reservations coordinate access to a shared namespace | P1 §8.7 | strong |
| C126-05 | H/P | registrations/reservations survive non-power-loss controller/subsystem resets | P1 §8.7 | strong |
| C126-06 | H/P | PTPL controls power-loss survival of reservations/registrants | P1 §5.12.1.16, §8.7 | strong |
| C126-07 | H/P | PTPL is namespace-specific and can be modified/reported | P1 | strong |
| C126-08 | E | payload persistence ≠ access-authority persistence | P1 + mechanism decomposition | strong bounded reconstruction |
| C126-09 | E | registration key ≠ active reservation authority | P1 reservation command structure | strong |
| C126-10 | E | PTPL policy state ≠ reservation state | P1 feature/command separation | strong |
| C126-11 | H/P | 1998 T10 proposal already exposes APTPL and reset-surviving persistent reservations | P4 | strong prior-art floor |
| C126-12 | X | NVMe invented persistent reservations | contradicted by P4 chronology | reject |
| C126-13 | X | SCSI translation proves direct genealogy | unsupported | reject |
| C126-14 | X | PTPL proves payload durability | category error | reject |
| C126-15 | X | reservation clear/preempt implies payload erase | unsupported/category error | reject |

---

## Related-repository check

Fresh code searches in `tmzncty/computing-archaeology` for `persistent reservation`, `APTPL`, `PTPL`, and reservation fencing returned no dedicated case to reuse.

If the broader history is developed later, it belongs there: SCSI/SPC proposal genealogy, cluster-fencing software, multi-port storage architectures, and NVMe enterprise adoption. Case 126 stays bounded to the retention relation.
