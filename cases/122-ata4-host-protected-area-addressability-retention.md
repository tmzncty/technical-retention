# Case 122 — ATA/ATAPI-4 Host Protected Area: Retained Payload Beyond the Current User-Addressable Frontier

## Status

**`grounded`** — bounded to the 1996–2001 ATA Host Protected Area / `READ NATIVE MAX ADDRESS` / `SET MAX ADDRESS` development path, with T13 proposal and draft-history records plus a named Maxtor shipping-product manual. The case establishes an addressability-retention relation: sectors can remain part of a device's native addressable population while a smaller current maximum makes them unavailable to ordinary reads and writes; the maximum-address policy itself can have either volatile or power-cycle-persistent lifetime.

Grounding record: [`../evidence/122-ata-1996-2001-hpa-set-max-grounding.md`](../evidence/122-ata-1996-2001-hpa-set-max-grounding.md).

## Scope

Case 89 establishes that one logical sector can keep its LBA while the host-visible CHS representation changes. Case 113 establishes that sectors can exist in a larger 48-bit LBA population while an older 28-bit command family cannot reach them. Case 122 asks a different question:

> What if the interface deliberately lowers the **current** user-addressable maximum even though the device retains a larger **native** maximum and the payload above the lowered frontier is intended to remain there?

This case is **not**:

- a complete history of HPA, PARTIES, BIOS recovery partitions, or OEM service environments;
- a Device Configuration Overlay (`DCO`) case; that follow-on is now grounded separately as [Case 123](123-ata6-device-configuration-overlay-capability-retention.md);
- a secure-erasure or sanitization case;
- a claim that sectors above the current maximum are physically contiguous in a simple platter geometry;
- a claim that ATA/ATAPI-4 invented hidden/reserved disk regions;
- a claim that the 24 April 1996 T13 proposal was the first private conception of a protected area;
- a claim that the inspected ATA/ATAPI-4 Revision 18 working draft is itself the final approved ANSI text;
- a claim that lowering the maximum address moves, overwrites, encrypts, or erases the hidden payload.

The broader ATA/HPA/DCO/BIOS history belongs primarily in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). A current repository search there for `Host Protected Area`, `HPA`, and `SET MAX ADDRESS` found no dedicated case to reuse.

---

## Historical vocabulary

The inspected primary sources use:

- `ATA protected area proposal`;
- `Host Protected Area feature set`;
- `READ NATIVE MAX ADDRESS`;
- `SET MAX ADDRESS`;
- `native maximum address`;
- `user-accessible address space`;
- `maximum LBA address`;
- `current CHS translation`;
- `volatile` / preservation across power-up or hardware reset;
- `SET MAX SET PASSWORD`, `SET MAX LOCK`, `SET MAX UNLOCK`, and `SET MAX FREEZE LOCK` in the later product witness.

The following are **project engineering terms**, not period ATA vocabulary:

- `addressability-retention relation`;
- `current addressability frontier`;
- `reachability policy state`;
- `payload survival beyond ordinary reach`;
- `addressability lifetime`.

---

## Historical record

### H/P — protected-area work is visible in the T13 record before the later SET MAX proposal

T13's surviving document index lists **D96137r0, `ATA protected area proposal`, submitted 24 April 1996** by Colegrove.

The ATA/ATAPI-4 1153D Revision 18 draft's own revision history says Revision 5, dated **28 June 1996**, added `D96137R0 Protected area proposal`.

This matters because the historical chain should not be compressed into `SET MAX ADDRESS appeared, therefore HPA began there`.

> **protected-area proposal chronology ≠ SET MAX command chronology**

### H/P — SET MAX ADDRESS appears as a later, separately tracked proposal

T13 lists **D97106r0, `SET MAX ADDRESS addition`, submitted 2 December 1996**, followed by D97106r1 on **28 January 1997**.

The 1153D revision history says Revision 9, dated **10 February 1997**, added `SET MAX ADDRESS addition (D97106R1)`. Revision 14, dated **26 June 1997**, then added a new SET MAX / NATIVE MAX description under D97119R3.

This supplies an unusually good proposal-to-draft chronology floor without proving invention priority.

### H/P — the inspected 1998 document is a working draft, not silently the final standard

The facsimile inspected here is **T13/1153D Revision 18, 19 August 1998**. Its cover explicitly calls it an `internal working document`, says it is `not a completed standard`, and says it had not been approved.

The case therefore uses Revision 18 as primary standards-development evidence. It does not relabel the inspected document as the final ANSI publication.

### H/P — READ NATIVE MAX exposes a device-native maximum distinct from the current user maximum

Revision 18 §8.26 defines `READ NATIVE MAX ADDRESS` as part of the Host Protected Area feature set. Its description says the command returns the **native maximum address**, defined as the highest address accepted by the device in the factory-default condition and as the maximum valid value for `SET MAX ADDRESS`.

This creates an interface-visible distinction between:

```text
native maximum address
        !=
current maximum exposed for ordinary user access
```

### H/P — SET MAX changes ordinary read/write reach, not the demonstrated existence of the higher native range

Revision 18 §8.38 says `SET MAX ADDRESS` lets the host redefine the maximum address of the **user-accessible address space**, in either LBA translation or current CHS translation.

After successful completion:

- `IDENTIFY DEVICE` capacity-related fields reflect the newly set maximum;
- read/write attempts above that maximum are rejected with `ID Not Found`;
- the device still has a separately queryable native maximum through `READ NATIVE MAX ADDRESS`.

The draft does not say that lowering the maximum erases or relocates sectors above it.

Therefore the direct historical mechanism supports:

> **ordinary read/write inaccessibility ≠ demonstrated payload destruction**

and:

> **current reported user capacity ≠ native addressable population**

### H/P — the maximum-address policy itself has a retention lifetime

Revision 18's `SET MAX ADDRESS` input defines a selection whose setting may either be preserved across power-up/hardware reset or revert to the most recent non-volatile maximum-address setting.

Thus the case contains two different kinds of retained state:

1. payload held by the disk medium/controller system;
2. a maximum-address configuration that controls which part of that payload ordinary commands may reach.

The second state can be deliberately shorter-lived than the first.

> **payload persistence ≠ reachability-policy persistence**

### H/P — a 2001 Maxtor shipping-product manual implements the command family

Maxtor's **541DX Product Manual**, copyright 2001, for models 2B020H1 / 2B015H1 / 2B010H1, documents `READ NATIVE MAX ADDRESS` and `SET MAX` in the drive command set.

The manual says:

- `READ NATIVE MAX ADDRESS` returns the highest address accepted in the factory-default condition;
- after `SET MAX`, ordinary reads and writes above the selected maximum are rejected with `IDNF`;
- `IDENTIFY DEVICE` fields reflect the set maximum;
- the product also implements `SET MAX SET PASSWORD`, `LOCK`, `UNLOCK`, and `FREEZE LOCK`.

The password and lock states have their own power-cycle behavior, which must not be confused with payload or maximum-address state.

This is a named product witness for implementation continuity, not proof of first commercial implementation.

---

## Retained state

The bounded case separates at least six state classes.

### 1. User payload

The sector contents remain the state whose later accessibility matters.

### 2. Native maximum address

The device retains a factory-default/native address ceiling that `READ NATIVE MAX ADDRESS` can report even when ordinary access is constrained by a lower current maximum.

### 3. Current user maximum

This is the current frontier used to accept or reject ordinary reads/writes and to shape capacity reporting.

### 4. Persistence class of the current maximum

The selected maximum can be configured to survive or not survive a power-up/hardware-reset boundary.

### 5. HPA security/control state

The later bounded product exposes password, lock, unlock, freeze, and retry-related control state. These govern authority to change the maximum; they are not themselves the payload.

### 6. Hidden physical placement

Nothing in the evidence establishes that `native LBA N` reveals the platter coordinate of its embodiment. Case 89 and Case 108 already block that shortcut.

---

## Retention mechanism

HPA is not a magnetic-retention mechanism. It does not make a domain more remanent, add ECC, or replicate sectors.

The retention-specific mechanism is **selective service reach over an already retained logical-sector population**:

```text
native logical-sector population
        |
        +--> 0 ... current_max
        |       ordinary read/write admitted
        |
        +--> current_max+1 ... native_max
                ordinary read/write rejected
                native extent still separately reportable
                payload not shown to have been erased merely by hiding
```

The case therefore makes `having data` a relational statement. A sector can be retained by the device while being outside the current ordinary-service frontier.

---

## Addressing and access

### Ordinary path

After a lowered maximum is active, ordinary reads and writes above it are rejected. Capacity fields presented through `IDENTIFY DEVICE` are correspondingly reduced.

### Native-maximum path

`READ NATIVE MAX ADDRESS` exposes the higher native ceiling. This is not an ordinary payload read; it is an interface operation that reveals the existence of a larger address range.

### Reconfiguration path

A permitted `SET MAX ADDRESS` can change the current frontier. Whether the setting survives power-up/hardware reset depends on the configured persistence semantics.

### Security/control path

The later product witness exposes additional SET MAX password/lock/freeze operations. Their purpose is to regulate who/when can change the frontier, not to prove that hidden payload is cryptographically protected or erased.

---

## Read / write / hide semantics

### Lowering the maximum

The demonstrated operation changes admissible address range and reported capacity.

It does **not** demonstrate:

- sector rewrite;
- physical relocation;
- media erase;
- cryptographic transformation;
- loss of the higher native-maximum relation.

### Restoring a larger maximum

The standards chain is designed around a separate native maximum and a host-set current maximum. Restoring a larger permitted maximum changes reachability. It should not be described as `recovering erased data`, because no erasure was established by the hide operation.

### Power/reset transition

A volatile maximum can disappear while payload remains physically retained. A non-volatile maximum can continue to constrain ordinary reach across the same transition.

This is the central temporal result:

> **the lifetime of an access boundary can differ from the lifetime of the bytes it bounds**.

---

## Failure and forgetting

Keep separate:

- **magnetic/payload loss** — sector value cannot be recovered;
- **current-frontier exclusion** — sector is above the current ordinary-access maximum;
- **loss/reversion of volatile maximum state** — the access policy changes after reset/power transition;
- **loss of authority credentials/control state** — a host may be unable to change a locked maximum even if data remains;
- **address-mode mismatch** — CHS and LBA reach are not identical, as Case 89 already shows;
- **legacy address-width limitation** — Case 113's 28-bit/48-bit distinction;
- **defect reassignment** — Case 14's embodiment replacement;
- **secure forgetting** — Case 44's erase/sanitize problem.

A lowered maximum is therefore a poor proxy for forgetting:

> **hidden from ordinary reads ≠ erased ≠ sanitized ≠ physically absent**.

---

## Engineering reconstruction

### E — reachability is retained state, not merely an instantaneous property of payload

Because the same native population can be paired with different current maxima, ordinary addressability depends on a retained configuration relation.

> **payload state + address policy -> current service reachability**

### E — losing a policy state can reveal rather than lose payload

If a volatile lower maximum reverts after a power/reset boundary while the sectors remain intact, the change is not `data recovery` at the substrate level. It is a change in which retained sectors are admitted to ordinary service.

This is a useful counterexample to any universal equation:

```text
less metadata retained -> less payload accessible
```

Here, loss/reversion of one access-limiting state can increase ordinary reach.

### E — capacity reporting is observer/interface qualified

`IDENTIFY DEVICE` can report the reduced current capacity while `READ NATIVE MAX ADDRESS` reports the larger native ceiling.

Therefore:

> **reported capacity ≠ one observer-independent description unless the command regime is specified**.

### E — policy persistence can be shorter than payload persistence

A volatile maximum is explicitly allowed to expire across power/reset while disk payload survives that boundary. Conversely, a persistent lower maximum can outlive many ordinary I/O sessions without changing the hidden bytes.

> **addressability lifetime ≠ payload lifetime**

---

## Functional comparisons

### A — Case 89: CHS/LBA translation

Case 89 changes the **representation** used to designate logical sectors; Case 122 changes the **currently admitted range** of those designations.

> **representation re-parameterization ≠ reachability frontier change**

Revision 18 itself allows SET MAX in either LBA or current CHS translation, so these axes can interact without becoming the same mechanism.

### A — Case 113: 28-bit / 48-bit LBA reach

Case 113's high sectors are unreachable because an older command family lacks enough address bits. Case 122's hidden sectors can be within the command's numerical capability yet deliberately excluded by current policy state.

> **encoding ceiling ≠ administrative/current maximum**

### A — Case 44: deallocation and sanitize

Case 44 asks when old data ceases to be logically current or is actively sanitized. Case 122 shows an earlier disk-interface counterexample in which ordinary inaccessibility is deliberately produced **without evidence of forgetting**.

> **inaccessibility ≠ deallocation ≠ sanitization**

### A — Case 14: defect reassignment

Case 14 preserves an LBA across physical replacement. Case 122 preserves the larger native logical population while changing which addresses ordinary service will accept. No physical replacement follows from SET MAX itself.

---

## Philosophical interpretation

The case is useful for theories of availability only after the engineering decomposition is fixed.

A retained object is not simply `present` or `absent`. Here, at least four relations can diverge:

- physical/payload survival;
- logical designation within the native population;
- current ordinary-service addressability;
- authority to change the addressability frontier.

This can discipline philosophical claims about technical availability, concealment, or orderability. It does **not** make HPA a philosophical concept, and it does not prove that hidden sectors are `forgotten` in any strong sense.

---

## Counterexamples and limits

- A sector above a lowered SET MAX frontier may still be lost physically; HPA does not guarantee payload integrity.
- A native-maximum report proves an address-range relation, not that every sector's payload is healthy.
- Password/lock support does not prove cryptographic confidentiality of hidden bytes.
- Lowering a maximum does not prove secure deletion.
- Restoring reach does not prove that payload survived; it only makes the address eligible again.
- The inspected 1998 document is a working draft, not the final approved standard.
- The 2001 Maxtor manual proves one named product family implemented the bounded commands, not universal drive behavior.
- DCO can also alter visible capacity and even the `READ NATIVE MAX` observation in later ATA generations; that separate capability/configuration layer is now grounded in [Case 123](123-ata6-device-configuration-overlay-capability-retention.md).

---

## Claim ledger

| Claim | Type | Strength / limit |
| --- | --- | --- |
| T13 lists D96137r0 `ATA protected area proposal` on 24 Apr 1996 | H/P | strong institutional chronology |
| ATA/ATAPI-4 rev. 5 records integration of D96137R0 | H/P | strong draft-history anchor |
| T13 lists D97106r0/r1 `SET MAX ADDRESS addition` in Dec 1996 / Jan 1997 | H/P | strong proposal chronology |
| ATA/ATAPI-4 rev. 9 records integration of D97106R1 | H/P | strong draft-history anchor |
| rev. 18 is an internal working draft, not the approved final standard | H/P/X | explicit document-status boundary |
| READ NATIVE MAX reports the factory-default/native maximum | H/P | strong |
| SET MAX can reduce ordinary user-addressable range | H/P | strong |
| ordinary reads/writes above the set maximum are rejected | H/P | strong |
| maximum-address policy can have volatile or power/reset-persistent lifetime | H/P | strong |
| lowering current maximum erases hidden sectors | X | rejected |
| current reported capacity equals native addressable population | X | rejected |
| HPA password/lock state proves payload encryption | X | rejected |
| 2001 Maxtor 541DX implements READ NATIVE MAX / SET MAX / lock subcommands | H/P | named manufacturer-primary product witness |
| addressability lifetime can differ from payload lifetime | E | strong reconstruction from persistence semantics |
| HPA is historically identical to later DCO, partition hiding, or NVMe deallocation | X/A | rejected; only bounded comparisons allowed |

---

## Sources

### Primary / contemporary

- T13 document archive, `d96137r0 — ATA protected area proposal`, Colegrove, submitted 24 April 1996: <https://t13.org/Documents/>
- T13 document archive, `d97106r0/r1 — SET MAX ADDRESS addition`, McLean, submitted 2 December 1996 / 28 January 1997: <https://t13.org/Documents/>
- T13/1153D Revision 18, *AT Attachment with Packet Interface Extension (ATA/ATAPI-4)*, 19 August 1998, especially revision history, §8.26 `READ NATIVE MAX ADDRESS`, and §8.38 `SET MAX ADDRESS`. The inspected facsimile explicitly identifies itself as an internal working draft.
- Maxtor, *541DX Product Manual*, P/N 1546/A, copyright 2001, especially §7 `Read Native Max Address`, `Set Max`, and SET MAX security/control subcommands: <https://www.seagate.com/staticfiles/maxtor/en_us/documentation/manuals/fireball_541dx_manual.pdf>

### Related repository

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — broad ATA/HPA/DCO/BIOS technical history belongs there if developed. This case retains only the addressability/retention decomposition.

---

## Open evidence debt

- Obtain and inspect the D96137r0 and D97106r0/r1 proposal facsimiles themselves, not only T13 metadata plus later draft integration records.
- Obtain the final approved ATA/ATAPI-4 text or a standards-body archival facsimile and compare it clause-by-clause with Revision 18.
- Ground PARTIES / BIOS runtime access only if a later slice needs host-software re-entry into HPA.
- Treat `DCO` as a separate case before making any broad taxonomy of hidden-capacity mechanisms.
- Add a named-platform trace or fault experiment only if it can distinguish payload survival, current maximum state, power/reset behavior, and lock state without conflating them.
