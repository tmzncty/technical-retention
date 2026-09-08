# NVMe 1.1 Reservations: Retained Access Authority Across Reset and Power Loss

## Status

**`grounded`** — bounded to NVM Express 1.1 (11 October 2012), its shared-namespace reservation model and per-namespace Persist Through Power Loss (`PTPL`) state, with a 1998 T10 Persistent Reservations proposal as an earlier public prior-art floor.

Grounding record: [`../evidence/126-nvme-1998-2012-reservation-ptpl-grounding.md`](../evidence/126-nvme-1998-2012-reservation-ptpl-grounding.md).

## Scope

This case asks a narrow retention question:

> **When several hosts can reach the same namespace, what access-control relation must survive a controller reset or a power cycle if the system is to preserve who is registered, who holds a reservation, and who may displace that holder?**

The bounded relation is:

```text
shared namespace persists
        ↓
hosts/controllers may change or reset
        ↓
registrant keys + reservation state qualify access
        ↓
ordinary controller/subsystem reset
        ↓
reservation/registration state survives
        ↓
power-loss reset
        ↓
PTPL decides whether that authority relation also survives
```

This is not a general history of SCSI reservations, clustering, multipathing, storage fencing, NVMe-oF, persistent-memory durability, or high-availability software. It is also not a payload-durability case. Cases 15, 20, 87, and Synthesis 13 already treat cache/flush/persistence handoff; Case 114 treats NVMe namespace write protection as a different mutation-authority regime.

`access-authority retention`, `coordination state`, `authority lifetime`, and `authority forgetting` below are project engineering terms, not historical NVMe vocabulary.

---

## Historical vocabulary

The inspected sources directly use `shared namespace`, `reservation`, `registrant`, `reservation key`, `Reservation Register`, `Reservation Acquire`, `Reservation Release`, `Reservation Report`, `Reservation Persistence`, `Persist Through Power Loss` / `PTPL`, `PTPLS`, `preempt`, `clear`, `Persistent Reservations`, and `Activate Persist Through Power Loss` / `APTPL`.

The case preserves those terms rather than retroactively calling every relation a lock, lease, epoch, or fence.

---

## Historical record

### H/P — NVMe 1.1 is a dated public specification floor, not an invention date

The original NVM Express Revision 1.1 is dated **11 October 2012**. NVM Express's 8 November 2012 release announcement says that 1.1 added multi-port / multi-host capabilities, namespace sharing, enhanced reset capabilities, and a reservations mechanism compatible with SCSI reservations. NVM Express's later SCSI Translation Reference states directly that NVMe Reservation support was added in NVM Express 1.1.

This establishes a public NVMe specification floor. It does not establish that NVMe invented persistent reservations, multi-host fencing, or power-loss-persistent reservation state.

### H/P — shared namespace persistence creates a coordination problem distinct from payload retention

NVM Express 1.1 §1.4.1 defines namespace sharing as two or more hosts accessing one shared namespace through different NVMe controllers. It explicitly says that concurrent access requires coordination between hosts, while the procedure used for that coordination is outside the specification.

The same section makes controller lifetime and namespace lifetime separable. In its dual-port example, a reset of one port affects only the associated controller and has no impact on the other controller, the shared namespace, or operations performed by the other controller on that namespace.

Therefore:

```text
one controller resets
        ≠
shared namespace disappears
```

### H/P — reservations retain a relative access relation, not a copy of namespace payload

NVM Express 1.1 §8.7 says reservations may be used by two or more hosts to coordinate access to a shared namespace. A reservation restricts which hosts may perform particular classes of operations. Reservation types differ in whether writes or all accesses are excluded and in the rights of registrants versus the reservation holder.

The reservation machinery therefore retains **who is registered and which access relation is currently in force**. It does not duplicate the logical blocks whose access it governs.

### H/P — registration and reservation are distinct retained states

Reservation Register registers, unregisters, or replaces a reservation key. Reservation Acquire and Reservation Release separately establish, preempt, release, or clear reservation state.

A host may therefore remain a **registrant** without necessarily being the current reservation holder. The key is an identity/qualification token inside the protocol; it is not itself the reservation.

### H/P — ordinary reset survival is stronger than power-loss survival by default

NVM Express 1.1 §8.7 states that reservations and registrations persist across **all Controller Level Resets and all NVM Subsystem Resets except a reset due to power loss**.

Power loss is therefore a separate lifetime boundary. Ordinary reset survival does not imply power-loss survival.

### H/P — PTPL is a namespace-specific retained policy state

NVM Express 1.1 §5.12.1.16 defines the Reservation Persistence Feature (Feature Identifier `83h`). Each namespace supporting reservations has a namespace-specific **Persist Through Power Loss (`PTPL`) state**, modifiable through Set Features or Reservation Register.

The defined behavior is explicit:

- `PTPL = 1`: reservations and registrants persist across power loss;
- `PTPL = 0`: reservations are released and registrants are cleared on power loss.

Reservation Register can also change the same state through `CPTPL`, and Reservation Report exposes the current `PTPLS` value. This gives the authority relation its own retained lifetime policy.

### H/P — capability, policy, registration population, and active reservation are different states

Section 8.7 requires a namespace that supports reservations to expose reservation capabilities and support PTPL state. This does not mean every namespace has an active reservation, that any controller currently holds one, or that PTPL is configured to preserve it across power loss.

### H/P — preempt and clear alter authority, not payload

Reservation Acquire can preempt a holder under the protocol's key rules. Reservation Release with the clear action can release reservation state and unregister registrants. Those commands alter **access qualification and authority**. They do not constitute secure erase, media overwrite, namespace format, or proof that user payload changed.

---

## Prior-art floor: T10 Persistent Reservations, 1998

### H/P — T10 98-203r3 already separates reset persistence from optional power-cycle persistence

T10 document **98-203 revision 3**, dated **24 July 1998** and authored by George Penokie (IBM), describes Persistent Reservations among multiple initiators. It states that persistent reservations survive recovery actions and are not reset by target reset/global actions, while retention across target power loss is optional.

Its `Activate Persist Through Power Loss` (`APTPL`) mechanism lets an application client request preservation of registration and reservation information across power cycles. The proposal explicitly says this preservation capability requires nonvolatile memory in the logical unit and enumerates retained information such as initiator identification, reservation key, scope, and type.

This predates NVMe 1.1 by fourteen years as a public standards-development artifact with the same broad function:

```text
multi-initiator access relation
        +
reset-surviving reservation state
        +
optional power-loss persistence
```

That chronology is a prior-art boundary, not proof of direct SCSI → NVMe implementation descent. NVM Express later described its reservation mechanism as compatible with SCSI and published a SCSI translation reference, but compatibility and translation do not establish invention genealogy.

---

## Retained-state decomposition

At least six distinct state classes participate:

1. **Namespace payload** — logical blocks and metadata served by the namespace. Reservation persistence does not itself preserve or rewrite these bytes.
2. **Namespace identity and sharing relation** — the namespace can remain the same shared object across multiple controllers; its lifetime is not reducible to one path or controller.
3. **Registrant population** — hosts/controllers that have registered keys.
4. **Active reservation relation** — current reservation type and holder/all-registrants relation determine which accesses are permitted.
5. **PTPL policy state** — namespace-specific policy determining whether registration/reservation state survives a power-loss reset.
6. **Live controller/host execution state** — queues, processes, paths, and sessions can disappear or reset even while the retained reservation relation survives.

These classes should not be collapsed into one generic `persistent state`.

---

## Retention mechanism and lifetime

For the bounded NVMe 1.1 case:

```text
explicit register/acquire
        ↓
registrant + reservation relation exists
        ↓
controller-level reset / subsystem reset
        ↓
relation survives
        ↓
power-loss reset
        ↓
if PTPL=1: relation survives
if PTPL=0: registration/reservation is cleared
```

The power-loss branch is a protocol-defined authority-lifetime decision. The specification does not require us to infer the physical nonvolatile representation used inside a controller.

T10's 1998 proposal explicitly mentions nonvolatile memory as necessary for its APTPL preservation capability, but that statement must not be silently projected into a specific NVMe controller implementation.

---

## Engineering reconstruction

### E — namespace payload persistence ≠ access-authority persistence

A namespace can retain every user block while a power loss clears registrants and reservations when `PTPL=0`. Conversely, `PTPL=1` can preserve the reservation relation while saying nothing by itself about whether the newest writes crossed their required durability boundary.

### E — controller reset survival ≠ power-loss survival

NVMe 1.1 makes this distinction explicit. A state can be persistent across ordinary controller/subsystem reset yet still be intentionally forgotten on power loss. `persistent` therefore requires a named failure boundary.

### E — registration key ≠ reservation authority

A key can remain registered when its registrant is not the current holder. Registration is a qualification relation; reservation is an active access relation.

### E — PTPL state ≠ reservation state

PTPL determines the **future lifetime rule** applied at power loss. It is not itself the current reservation, holder, or registrant set. It is second-order retained state: a retained rule about whether another retained relation should survive a later event.

### E — shared-namespace identity ≠ one controller's lifetime

The multipath examples permit one controller/port to reset without removing the shared namespace or disturbing another controller's operations. The logical object and one access path have different lifetimes.

### E — authority survival ≠ actor survival

A host process, controller queue, or path can disappear while a reservation/registration relation survives the reset. The system may therefore retain an authority relation longer than the execution context that established it. Recovery may then require explicit preempt, release, or clear work.

### E — more persistent authority ≠ monotonically safer retention

PTPL can prevent a power cycle from accidentally reopening a shared namespace to unqualified hosts. It can also preserve obsolete authority after the actor that created it is gone. Persistence has a coordination cost as well as a protective function.

### E — preempt/clear ≠ data forgetting

Removing reservation authority changes who may access the namespace. It does not erase or invalidate user data. Authority forgetting and payload forgetting are different operations.

---

## Failure and forgetting modes

Within this bounded case, distinguish:

- controller/path reset while reservation state survives;
- power loss with `PTPL=0`, intentionally forgetting registration/reservation state;
- power loss with `PTPL=1`, retaining authority while the original host execution context is gone;
- incorrect or stale key ownership interpretation;
- failure to preempt a dead holder during recovery;
- accidental clear/release of valid coordination state;
- namespace payload surviving while access authority is lost;
- authority surviving while newest payload writes were not independently durable;
- reservation protocol misuse causing corruption despite mechanically correct persistence.

The last boundary is explicit in NVMe 1.1: incorrect application of reservations may corrupt data or impair system operation. Retention of the mechanism does not prove correct use.

---

## Cross-case functional comparisons

### A — Case 114: NVMe Namespace Write Protection

Case 114 retains a namespace-scoped **mutation-authority policy** such as temporary-until-power-cycle or permanent write protection. Case 126 retains a **relative multi-host access relation** involving registrants, keys, reservation types, and holders.

```text
write-protection state
        ≠
reservation state
```

Overlapping write-admission effects do not make the mechanisms identical.

### A — Case 50: HDFS QJM epoch fencing

Case 50 also shows authority surviving actor/process turnover: JournalNodes retain `lastPromisedEpoch` so an old writer can remain alive yet lose successful mutation authority. The functional analogy is retained protocol state qualifying a stale actor's future authority. QJM uses quorum overlap and epoch promises in a distributed journal; NVMe uses namespace/controller reservation state. Similar fencing function is not historical or technical identity.

### A — Synthesis 13: durability handoff

Synthesis 13 separates completion, volatile residence, persistence-domain arrival, ordering, and failure model. Case 126 adds a different question above that stack: **who remains authorized to access a shared namespace after reset?** A retained reservation cannot substitute for Flush/FUA/persistence semantics, and a durable write cannot substitute for reservation/fencing state.

---

## Philosophical interpretation

### I — technical retention can preserve a relation of permission after the acting moment ends

The retained object here is not primarily a stored payload but a **relation among actors and a shared object**: registered participant, holder, reservation type, and the policy governing whether that relation survives power loss.

This supplies a bounded example in which technical retention preserves not only a value but a rule of future admissibility. It does not imply that political, legal, or social authority is technically equivalent to a storage reservation.

---

## Prior-art / novelty boundary

Do not claim:

- NVMe invented persistent reservations or power-loss-persistent fencing;
- T10 98-203r3 proves the first invention of Persistent Reservations;
- SCSI/NVMe compatibility proves direct implementation genealogy;
- PTPL makes namespace payload durable;
- a reservation key is the same thing as a reservation;
- a reservation-capable namespace necessarily has an active reservation;
- reset-surviving state necessarily survives power loss;
- PTPL reveals the controller's physical nonvolatile implementation;
- preempting or clearing a reservation erases user data;
- a persistent reservation proves cluster/application correctness.

The safe claim is narrower:

> **NVM Express 1.1 (11 October 2012) specifies reservation and registration state that survives controller/subsystem resets and gives each reservation-capable namespace a separate PTPL state controlling survival across power loss. A 1998 T10 Persistent Reservations proposal already documents reset-surviving multi-initiator reservation state plus optional APTPL preservation, providing a clear earlier prior-art floor without proving direct genealogy.**

---

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for Persistent Reservation, `APTPL`, `PTPL`, reservation fencing, and related terms found no dedicated case to reuse.

The division of labor remains:

- `technical-retention`: reservation/registration/PTPL lifetime, authority retention, and comparison with other retained authority relations;
- `computing-archaeology`: if developed later, broad SCSI/SPC persistent-reservation genealogy, cluster-fencing history, multipath hardware/software history, and NVMe enterprise-feature adoption.

---

## Primary sources

1. NVM Express, **NVM Express Revision 1.1**, 11 October 2012, especially §1.4.1, §5.12.1.16, Reservation Register/Report, and §8.7: <https://www.nvmexpress.org/wp-content/uploads/NVM-Express-1_1.pdf>
2. NVM Express Work Group, **NVM Express Work Group Releases 1.1 Specification**, 8 November 2012: <https://www.nvmexpress.org/wp-content/uploads/docs/NVMe_Press_Release_1-1_20121108.pdf>
3. NVM Express, **NVM Express: SCSI Translation Reference**, 24 June 2015: <https://nvmexpress.org/wp-content/uploads/NVM_Express_-_SCSI_Translation_Reference-1_5_20150624_Gold.pdf>
4. T10, George Penokie (IBM), **T10/98-203 revision 3 — Persistent Reservations**, 24 July 1998: <https://www.t10.org/ftp/t10/document.98/98-203r3.pdf>

---

## Evidence status

| Claim | Status |
| --- | --- |
| NVMe Reservation support is a 1.1 addition | **primary/institutional grounded** |
| shared namespace can outlive one controller/path reset in the bounded examples | **primary grounded** |
| registrations/reservations survive non-power-loss controller/subsystem resets | **primary grounded** |
| PTPL separately controls reservation/registrant survival across power loss | **primary grounded** |
| PTPL is namespace-specific and reportable/modifiable | **primary grounded** |
| 1998 T10 proposal already exposes APTPL/nonvolatile-preservation semantics | **primary standards-development grounded** |
| SCSI → NVMe direct genealogy | **not established** |
| physical NVMe implementation of PTPL state | **not established** |
| named-controller power-cycle conformance | **open** |
| application/cluster correctness under failure | **open** |
