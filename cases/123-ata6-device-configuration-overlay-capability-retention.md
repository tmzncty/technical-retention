# Case 123 — ATA/ATAPI-6 Device Configuration Overlay: Persistent Capability Reduction Beneath the HPA Frontier

## Status

**`grounded`** — bounded to the 2000–2007 ATA Device Configuration Overlay (`DCO`) standards-development and interface path, with T13 proposal/public-standard metadata, a named 2003 Maxtor shipping-product witness, and later ATA8-ACS working-draft continuity used to recover exact command and reset semantics.

Grounding record: [`../evidence/123-ata-2000-2007-dco-grounding.md`](../evidence/123-ata-2000-2007-dco-grounding.md).

## Scope

Case 122 established the ATA Host Protected Area (`HPA`) relation in which a host-set current maximum can be lower than the separately queryable native maximum. Case 123 asks a narrower follow-on question:

> What if retained device configuration can reduce not only ordinary capacity, but the command/mode/feature contract itself — and can even change what `READ NATIVE MAX ADDRESS` reports?

This case is **not**:

- a complete history of ATA/ATAPI-6;
- a complete DCO/HPA/PARTIES/BIOS genealogy;
- a forensic claim that every drive actually contains recoverable hidden sectors;
- a claim that the inspected 2007 ATA8-ACS document is a final approved standard;
- a claim that `DCO` is encryption, secure erase, or sanitization;
- a claim that the T13 proposal date is an invention date;
- a claim that DCO necessarily reveals physical platter geometry;
- a claim that the interface-level ordering described below is a literal firmware-stack implementation.

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Device Configuration Overlay`, `DCO`, and the ATA command names found no dedicated case to reuse. Broader ATA capability/configuration history belongs there if developed; this case keeps only the retention-specific state/lifetime relation.

---

## Historical vocabulary

Primary sources use:

- `Device configuration overlay proposal`;
- `Device Configuration Overlay feature set`;
- `DEVICE CONFIGURATION IDENTIFY`;
- `DEVICE CONFIGURATION SET`;
- `DEVICE CONFIGURATION RESTORE`;
- `DEVICE CONFIGURATION FREEZE LOCK`;
- `Factory_config`;
- `Reduced_config`;
- `DCO_locked`;
- `selectable commands, modes, capacity, and feature sets`.

The following are **project engineering terms**, not period ATA vocabulary:

- `capability-retention relation`;
- `factory/selectable capability baseline`;
- `current advertised capability surface`;
- `configuration-authorized reach`;
- `observer-qualified capacity`.

---

## Historical record

### H/P — DCO has a public T13 proposal trail in 2000

The T13 document archive lists:

- `e00140r0 — Device configuration overlay proposal`, submitted **18 July 2000**;
- `e00140r1`, submitted **31 August 2000**;
- `e00140r2`, submitted **23 October 2000**.

These dates establish a public standards-development floor. They do **not** prove first private conception or absolute invention priority.

### H/P — T13 separately lists ATA/ATAPI-6 as INCITS 361-2002

T13's expired-standards record lists **INCITS 361-2002 (1410D), AT Attachment - 6 with Packet Interface (ATA/ATAPI-6)** with a **25 February 2002** submission/publication record.

This supports a standards-generation anchor for DCO without requiring the inaccessible proposal PDF to carry every mechanism claim.

### H/P — a named 2003 Maxtor product implements the DCO command family

Maxtor's *DiamondMax Plus9 60/80/120/160/200GB AT Product Manual*, dated **30 October 2003**, is preserved in Seagate's Maxtor archive.

Its supported-command table includes:

- `DEVICE CONFIGURATION FREEZE LOCK` (`B1h/C1h`);
- `DEVICE CONFIGURATION IDENTIFY` (`B1h/C2h`);
- `DEVICE CONFIGURATION RESTORE` (`B1h/C0h`);
- `DEVICE CONFIGURATION SET` (`B1h/C3h`).

The same manual's IDENTIFY table reports the Device Configuration Overlay feature set and 48-bit Address feature set as separately reportable capabilities. This is a named shipping-product witness, not a claim of first implementation or universal behavior.

### H/P — later ATA8-ACS continuity exposes the exact DCO state/lifetime contract

The inspected **T13/1699-D Revision 4a, 21 May 2007** ATA8-ACS document explicitly identifies itself as a **Working Draft** and says it is not a completed standard. It is therefore used only as later standards-continuity evidence for a mechanism already publicly tracked in the ATA/ATAPI-6 era.

Its DCO feature-set clause states that DCO can modify optional commands, modes, feature sets, and reported capacity. `DEVICE CONFIGURATION SET` may clear support/enabled indications; when a capability is configured as unsupported, the device is required not to provide it.

> **physical/device capability population ≠ current interface-advertised capability surface**

### H/P — DCO capacity reduction changes READ NATIVE MAX itself

The later working draft says that when `DEVICE CONFIGURATION SET` reduces maximum capacity, the value returned by `READ NATIVE MAX ADDRESS` / `READ NATIVE MAX ADDRESS EXT` is also modified.

This is the decisive difference from the bounded HPA relation in Case 122:

- HPA: current ordinary maximum may be lower while `READ NATIVE MAX` exposes the higher HPA-native ceiling;
- DCO: a lower DCO maximum changes the maximum that `READ NATIVE MAX` itself reports.

Therefore:

> **HPA-native maximum ≠ DCO factory/selectable maximum**

and:

> **`READ NATIVE MAX` ≠ universal factory-capacity oracle once DCO is in scope**

This is an interface-semantic comparison, not a claim about literal firmware layering.

### H/P — DCO retains a second capability view through DEVICE CONFIGURATION IDENTIFY

The DCO clause says `DEVICE CONFIGURATION IDENTIFY` specifies the selectable commands, modes, capacity, and feature sets the device is capable of supporting. After DCO SET, that information is no longer available from ordinary `IDENTIFY DEVICE`, while the DCO IDENTIFY data is not changed by DCO SET or DCO RESTORE.

Thus one device can expose at least two legitimate capability descriptions:

```text
selectable / DCO-identify baseline
            !=
current ordinary IDENTIFY surface
```

> **current advertised support ≠ selectable support baseline**

### H/P — reduced DCO configuration survives power-on and hardware reset

The later working draft states that during power-on reset or hardware reset the device **shall not change the settings made by a DEVICE CONFIGURATION SET command**. Its state description also enters `Reduced_config` after power-up when a reduced configuration has been set.

This makes DCO configuration itself retained state with a lifetime spanning resets/power cycles in the documented contract.

> **payload persistence ≠ capability-configuration persistence**, even when both cross the same power boundary.

### H/P — DCO FREEZE LOCK has a different lifetime from DCO SET state

After successful `DEVICE CONFIGURATION FREEZE LOCK`, DCO SET / IDENTIFY / RESTORE are rejected until the next power-on reset. Hardware or software reset does not clear the locked state, but the next power-on reset does.

Therefore:

> **persistent reduced configuration ≠ temporary authority lock**

A device may retain the reduced configuration across power-up while the authority-freeze state used during the preceding power cycle has expired.

### H/P — DCO and HPA interact rather than behaving as independent knobs

The later working draft says DCO capacity reduction is command-aborted when an HPA is already established because reducing capacity may lose that HPA relation; DCO RESTORE is likewise rejected when the current IDENTIFY capacity is below the native maximum because an HPA exists.

The state spaces therefore interact operationally.

> **two addressability-control mechanisms ≠ two freely composable independent settings**

---

## Retained state

The bounded case separates at least seven state classes.

### 1. User payload

Sector contents whose later accessibility may be affected but which DCO does not itself demonstrate rewriting or erasing.

### 2. DCO selectable/factory capability baseline

The set of commands, modes, feature sets, and capacity that `DEVICE CONFIGURATION IDENTIFY` says the device can support.

### 3. Current reduced configuration

The capability/capacity subset currently enforced after a successful `DEVICE CONFIGURATION SET`.

### 4. Ordinary IDENTIFY presentation

The host-visible capability report shaped by the reduced configuration.

### 5. DCO-modified maximum capacity

A maximum that can constrain both ordinary capacity reporting and the value returned by `READ NATIVE MAX`.

### 6. DCO lock state

A temporary authority state preventing DCO reconfiguration commands until the next power-on reset.

### 7. HPA state

A separate, interacting current-maximum/control regime retained by Case 122. It must not be folded into DCO merely because both can affect visible capacity.

---

## Retention mechanism

DCO is not a magnetic-retention mechanism. It is retained **configuration authority over what the device agrees to expose and provide**.

A useful bounded reconstruction is:

```text
selectable capability/capacity baseline
        |
        | DEVICE CONFIGURATION SET
        v
persistent Reduced_config
        |
        +--> ordinary IDENTIFY reports reduced surface
        +--> disabled feature is not provided
        +--> lower DCO maximum changes READ NATIVE MAX
        |
        | DEVICE CONFIGURATION RESTORE
        v
Factory_config
```

A separate `FREEZE LOCK` controls whether the configuration can be inspected/changed during the current power-cycle authority window.

The important retained object is therefore not just bytes or an address frontier. It can be a **contract about which operations and capacities count as available**.

---

## Addressing and access

### Ordinary capability observation

`IDENTIFY DEVICE` reflects the current reduced surface after DCO SET.

### DCO capability observation

`DEVICE CONFIGURATION IDENTIFY` reports the selectable baseline and is explicitly kept distinct from ordinary IDENTIFY after reduction.

### HPA-native observation

`READ NATIVE MAX` is not independent of DCO. A DCO maximum-capacity change modifies its result.

### Reconfiguration path

`DEVICE CONFIGURATION SET` establishes the reduced surface. `RESTORE` can return to the selectable baseline subject to state restrictions, including HPA interaction.

### Authority-freeze path

`DEVICE CONFIGURATION FREEZE LOCK` blocks DCO SET/IDENTIFY/RESTORE for the bounded power-cycle interval without becoming the reduced configuration itself.

---

## Read / write / restore / forgetting semantics

### DCO SET

The demonstrated operation changes capability reporting and required device behavior. Capacity can be reduced.

It does **not** demonstrate:

- media overwrite;
- sector relocation;
- cryptographic transformation;
- physical erasure;
- payload validation.

### DCO RESTORE

Restore re-enables capabilities disabled through DCO and returns ordinary IDENTIFY toward the DCO-identify baseline when allowed.

It should not be described as `restoring deleted data`.

> **capability restoration ≠ payload restoration**

### Hidden capacity and forgetting

Because DCO can make a region inaccessible through a reduced capacity surface without specifying media erase:

> **DCO inaccessibility ≠ deallocation ≠ sanitization**

This is the same general negative boundary as HPA, but reached through a different configuration layer.

---

## Engineering reconstruction

### E — one device can retain multiple observer-qualified truths about its capabilities

Ordinary IDENTIFY and DCO IDENTIFY answer different questions. A reduced capability can be truthfully `unsupported` to the ordinary interface while still appearing in the selectable DCO baseline.

> **reported unsupported ≠ physically impossible**

The conclusion is interface-qualified; it does not prove unused hardware blocks, firmware paths, or media geometry.

### E — configuration can hide the probe used by another configuration layer

Case 122 uses `READ NATIVE MAX` to distinguish current HPA reach from a higher native maximum. Case 123 shows that DCO can change what `READ NATIVE MAX` returns.

Therefore a capacity audit that asks only `IDENTIFY DEVICE` and `READ NATIVE MAX` can still be conditioned by retained DCO state.

> **one deeper-looking diagnostic view ≠ observer-independent ground truth**

### E — configuration persistence and modification authority have different clocks

DCO SET survives power-on/hardware reset, while DCO FREEZE LOCK expires at the next power-on reset.

The system therefore contains at least two lifetimes:

1. retained reduced configuration;
2. temporary authority to prevent reconfiguration.

> **configuration lifetime ≠ lock lifetime**

### E — restoring an interface contract does not certify the media behind it

DCO RESTORE can re-enable capacity/features, but a newly reachable sector can still be damaged.

> **capability/addressability restored ≠ payload validated**

---

## Functional comparisons

### A — Case 122: HPA / SET MAX

HPA changes the current ordinary-address frontier while retaining a separately queryable native maximum. DCO can change the maximum returned by that native-max query itself and can additionally suppress commands/modes/features.

> **HPA current frontier ≠ DCO selectable-capability baseline**

The comparison is functional/interface-semantic only. It does not assert an implementation stack or invention genealogy.

### A — Case 113: 28-bit / 48-bit LBA

Case 113 distinguishes what an address format can encode. DCO can suppress current support/reporting for a feature such as 48-bit addressing even when the selectable baseline says it is available.

> **encoding capability ≠ configuration-authorized capability**

### A — Case 89: CHS/LBA translation

Case 89 changes address representation. DCO changes the currently exposed command/capability contract and possibly maximum capacity.

> **representation parameter ≠ capability policy**

### A — Case 44: erase / sanitize

DCO can make capacity or commands unavailable without demonstrating forgetting.

> **interface withdrawal ≠ secure media forgetting**

---

## Philosophical interpretation

This case sharpens technical `availability` before any philosophical use of that word.

A device may physically retain payload and even retain a selectable capability baseline while the current service contract says that some capacity or operation is unavailable. Conversely, restoring the contract can make an operation/address admissible again without proving the associated payload survived intact.

The engineering lesson is that availability is relational among:

- retained payload;
- retained configuration;
- command/view used by the observer;
- authority to modify configuration;
- interacting control regimes such as HPA.

This can discipline philosophical discussion of orderability or concealment. It does **not** make DCO itself an instance of `Bestand`, `tertiary retention`, or a theory of forgetting.

---

## Counterexamples and limits

- DCO reduced capacity does not prove every hidden sector contains valid payload.
- DCO IDENTIFY's selectable baseline does not disclose physical platter coordinates.
- `reported unsupported` does not prove the implementation remains electrically active behind the interface; only the selectable capability relation is established.
- DCO RESTORE does not verify sector integrity.
- DCO FREEZE LOCK is not payload encryption.
- ATA8-ACS Revision 4a is later working-draft continuity, not the inspected final ATA/ATAPI-6 normative text.
- T13 proposal dates are standards-development chronology, not absolute invention priority.
- The 2003 Maxtor manual proves one named product family implemented the DCO command family; it does not prove universal conformance.
- No physical-drive fault experiment was performed in this slice.

---

## Claim ledger

| Claim | Type | Strength / limit |
| --- | --- | --- |
| T13 lists e00140r0/r1/r2 DCO proposals in Jul–Oct 2000 | H/P | strong institutional chronology |
| T13 lists INCITS 361-2002 / ATA/ATAPI-6 | H/P | strong standards-generation anchor |
| Maxtor DiamondMax Plus9 manual exposes DCO command support in 2003 | H/P | strong named-product witness |
| later ATA8-ACS working draft says DCO can reduce commands/modes/features/capacity | H/P | strong later continuity, not ATA/ATAPI-6 final-text substitute |
| DCO capacity reduction modifies READ NATIVE MAX result | H/P | strong |
| DCO IDENTIFY baseline differs from ordinary IDENTIFY after reduction | H/P | strong |
| DCO SET state survives power-on/hardware reset | H/P | strong in bounded later contract |
| DCO FREEZE LOCK expires at next power-on reset but survives hardware/software reset | H/P | strong |
| DCO and HPA are freely independent | X | rejected |
| DCO capacity reduction erases hidden payload | X | rejected |
| DCO RESTORE validates restored-address payload | X | rejected |
| 2000 proposal date proves invention | X | rejected |
| DCO/HPA similarity proves one genealogy | A/X | rejected |

---

## Evidence debt

- direct inspectable facsimile of `e00140r0/r1/r2` proposal text rather than archive metadata only;
- final approved ATA/ATAPI-6 normative facsimile and exact DCO clause comparison;
- ATA/ATAPI-7/ACS revision-by-revision changes to DCO fields and restrictions;
- earlier reserved-capacity / capability-overlay prior art beyond HPA;
- named BIOS/OEM deployment records showing why/how system manufacturers used DCO;
- independent drive traces comparing IDENTIFY, READ NATIVE MAX, DCO IDENTIFY, HPA, and restore behavior;
- fault/power-cycle validation of persistent DCO state;
- forensic media validation distinguishing hidden addressability from actual payload survival;
- broader technical genealogy in `computing-archaeology` rather than duplicating it here.
