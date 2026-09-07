# Evidence 123 — ATA Device Configuration Overlay Grounding (2000–2007)

## Research question

Can an ATA device retain a configuration that reduces the commands, modes, features, and capacity presented through ordinary host interfaces, while preserving a distinct selectable capability baseline — and can that retained configuration have a lifetime different from both payload and the authority state used to lock further changes?

This record grounds only that bounded DCO relation. It does not attempt a complete ATA/HPA/DCO/BIOS history.

---

## Source hierarchy and identity

### P1 — T13 document archive: e00140r0 / r1 / r2

**Institution:** Technical Committee T13 AT Attachment  
**Documents:** `Device configuration overlay proposal`  
**Author listed:** McLean  
**Submission dates:**

- `e00140r0` — **18 July 2000**;
- `e00140r1` — **31 August 2000**;
- `e00140r2` — **23 October 2000**.

**Archive URLs:**

- <https://t13.org/documents>
- <https://t13.org/docsearch>

The T13 archive metadata establishes a public standards-development trail for a named `Device configuration overlay proposal` in 2000.

**What it proves:** proposal title, document numbers, listed author, and submission dates.  
**What it does not prove:** exact proposal wording without the proposal facsimile; first private conception; absolute invention priority; later normative semantics.

### P2 — T13 expired-standards record: ATA/ATAPI-6

**Institution:** Technical Committee T13 AT Attachment  
**Record:** `INCITS 361-2002 (1410D): AT Attachment - 6 with Packet Interface (ATA/ATAPI - 6)`  
**T13 date shown:** **25 February 2002**  
**URL:** <https://www.t13.org/standards-expired>

T13's institutional record places ATA/ATAPI-6 in the 2002 standards generation after the 2000 DCO proposal trail.

**What it proves:** the named published-standard/project record and date shown by T13.  
**What it does not prove:** the exact wording of the final approved DCO clauses without directly inspecting the normative facsimile.

### P3 — Maxtor DiamondMax Plus9 Product Manual

**Vendor:** Maxtor Corporation  
**Document:** *DiamondMax Plus9 60/80/120/160/200GB AT Product Manual*  
**Part number:** 1877  
**Date:** **30 October 2003**  
**Archival host:** Seagate's Maxtor documentation archive  
**URL:** <https://www.seagate.com/staticfiles/maxtor/en_us/documentation/manuals/diamondmax_plus_9_manual.pdf>

The title page identifies the product family and date. Chapter 5 describes the ATA interface and says the drive follows ATA/ATAPI-6 for the command set.

#### Supported-command table

Table 5-1 lists:

- `DEVICE CONFIGURATION FREEZE LOCK` — command `B1h`, feature `C1h`;
- `DEVICE CONFIGURATION IDENTIFY` — `B1h/C2h`;
- `DEVICE CONFIGURATION RESTORE` — `B1h/C0h`;
- `DEVICE CONFIGURATION SET` — `B1h/C3h`.

It also lists `READ NATIVE MAX ADDRESS` and the SET MAX command family, which is useful because the named product exposes both DCO and HPA-related command surfaces in one shipping family.

#### IDENTIFY capability witness

Table 5-2 identifies:

- Device Configuration Overlay feature-set support;
- 48-bit Address feature-set support;
- SET MAX security-extension support;
- HPA feature-set enablement in the relevant IDENTIFY words.

**What P3 proves:** a named 2003 Maxtor family implemented and reported the DCO command family in the ATA/ATAPI-6 era.  
**What it does not prove:** first implementation, universal conformance, exact DCO persistent-state internals, or the physical condition of any capacity hidden through DCO.

### P4 — T13/1699-D Revision 4a, ATA8-ACS working draft

**Document:** *Information technology — AT Attachment 8 - ATA/ATAPI Command Set (ATA8-ACS)*  
**Identifier:** T13/1699-D Revision 4a  
**Date:** **21 May 2007**  
**Inspected facsimile:** <https://tc.gts3.org/cs3210/2016/spring/r/hardware/ATA8-ACS.pdf>

#### Document-status boundary

The cover explicitly identifies this as a **Working Draft** and says it is **not a completed standard**. The record therefore uses it as later primary standards-continuity evidence, not as a substitute for the final approved ATA/ATAPI-6 normative text.

#### §4.8 — Device Configuration Overlay feature set

Printed pp. 17–20 state that the optional DCO feature set lets a utility modify optional commands, modes, feature sets, and reported capacity. The DCO command family contains:

- `DEVICE CONFIGURATION FREEZE LOCK`;
- `DEVICE CONFIGURATION IDENTIFY`;
- `DEVICE CONFIGURATION RESTORE`;
- `DEVICE CONFIGURATION SET`.

When DCO SET clears support for a command/mode/capacity/feature, the device shall not provide the feature represented as unsupported.

**Retention relevance:** a persistent control relation can change the host-visible operational contract without changing the semantic identity of the device or demonstrating payload rewrite.

#### Capacity reduction and READ NATIVE MAX

Printed p. 18 states that maximum capacity may be reduced. If DCO SET modifies maximum capacity, the address returned by `READ NATIVE MAX ADDRESS` / `READ NATIVE MAX ADDRESS EXT` is also modified.

This directly establishes:

> **HPA-native observation ≠ factory/selectable DCO baseline**

once DCO state is considered.

It also blocks a too-strong forensic or engineering assumption that `READ NATIVE MAX` always reveals an observer-independent factory maximum.

#### DCO IDENTIFY versus ordinary IDENTIFY

Printed p. 18 says DCO IDENTIFY specifies selectable commands, modes, capacity, and feature sets. After DCO SET, this information is no longer available from ordinary IDENTIFY, while DCO IDENTIFY data is not changed by DCO SET or DCO RESTORE.

Therefore:

> **current ordinary capability report ≠ selectable capability baseline**

The distinction is interface-level. It does not establish physical hidden hardware geometry.

#### Persistent reduced configuration

Printed p. 18 says that during power-on reset or hardware reset a device shall not change settings made by DCO SET. The same page says a device that successfully completed DCO SET returns to `DCO Reduced_config` after power-on reset.

Printed pp. 19–20 show the `Factory_config`, `DCO_locked`, and `DCO_reduced_config` state model.

**Retention relevance:** the reduced configuration itself is retained across the documented reset/power boundary.

#### FREEZE LOCK lifetime

Printed p. 18 says that after a successful DCO FREEZE LOCK, DCO SET/IDENTIFY/RESTORE are aborted until the subsequent power-on reset. Hardware or software reset does not clear the DCO locked state.

This creates a different lifetime from DCO SET configuration:

> **configuration persistence ≠ modification-authority lock lifetime**

#### HPA/DCO interaction

Printed p. 18 says DCO SET capacity reduction is aborted if an HPA has been established because an HPA may be lost if capacity is reduced. DCO RESTORE is also aborted when the ordinary current maximum is below the native maximum because an HPA exists.

Printed p. 19 additionally rejects eliminating HPA support when an HPA is established.

This proves the two mechanisms interact through validity conditions; they are not independent address-range knobs.

#### §7.10.5 — DEVICE CONFIGURATION SET

Printed p. 97 states that DCO SET permits a device manufacturer or personal-computer system manufacturer to reduce optional commands, modes, or feature sets supported by the device. It also says changing maximum LBA changes the address returned by READ NATIVE MAX / EXT.

The formulation is important because the historical actors' own standardization vocabulary is about **configuration/capability reduction**, not the project's later philosophical language of concealment or availability.

---

## Evidence chain

```text
18 Jul 2000
T13 e00140r0
"Device configuration overlay proposal"
        |
31 Aug / 23 Oct 2000
r1 / r2 proposal revisions
        |
25 Feb 2002
T13 record for INCITS 361-2002
ATA/ATAPI-6
        |
30 Oct 2003
Maxtor DiamondMax Plus9 product manual
DCO command-family implementation witness
        |
21 May 2007
ATA8-ACS Rev 4a working draft
later continuity exposes exact
DCO capability/capacity/reset semantics
```

This is a public standards-development and implementation/continuity floor. It is not an invention genealogy beyond the documented sequence.

---

## Grounded claims

### H/P — DCO proposal chronology is publicly visible by July 2000

T13 records three revisions of the named DCO proposal between July and October 2000.

> **proposal record ≠ invention date**

### H/P — ATA/ATAPI-6 is the relevant 2002 standards generation

T13 lists INCITS 361-2002 / ATA/ATAPI-6 after the DCO proposal series.

The evidence record does not pretend that archive metadata replaces inspection of the final normative clauses.

### H/P — DCO reached a named shipping product by 2003

The Maxtor DiamondMax Plus9 manual exposes all four DCO commands and reports DCO support through IDENTIFY fields.

> **standard-generation feature ≠ paper-only mechanism**

within this bounded product witness.

### H/P — DCO can reduce more than capacity

Later primary standards continuity says DCO may reduce optional commands, modes, feature sets, and capacity.

> **current service contract ≠ payload state alone**

### H/P — DCO changes the native-max observation used by HPA

A DCO maximum-capacity change modifies READ NATIVE MAX / EXT.

> **READ NATIVE MAX under DCO ≠ factory/selectable maximum**

### H/P — DCO retains a selectable baseline distinct from ordinary reporting

DCO IDENTIFY reports the selectable capability/capacity baseline even after ordinary IDENTIFY is reduced.

> **ordinary advertised support ≠ selectable support baseline**

### H/P + E — DCO SET state is retained across documented reset/power boundaries

The later DCO contract says power-on or hardware reset shall not alter DCO SET settings and returns a configured device to Reduced_config after power-on.

> **configuration state has a retention lifetime independent of one I/O session**

### H/P + E — FREEZE LOCK is a distinct, shorter-lived authority state

The freeze blocks DCO management through hardware/software reset but ends at the subsequent power-on reset, while the reduced configuration can remain.

> **configuration lifetime ≠ lock lifetime**

### H/P — HPA and DCO interact through validity restrictions

DCO capacity changes/restores may be rejected while an HPA is established.

> **coexisting control regimes ≠ independent composition**

---

## Engineering reconstruction

### E1 — retained capability state can outlive the operation that installed it

Assumptions:

1. the DCO SET command succeeds;
2. no later valid RESTORE/reconfiguration changes it;
3. the device follows the bounded later reset contract.

Then the reduced capability/capacity surface remains after a later power-on/hardware-reset transition.

This is a retention relation over **service configuration**, not over user bytes.

### E2 — an observer can mistake a configured surface for a physical limit

Ordinary IDENTIFY can truthfully say a capability is unsupported after DCO reduction even though DCO IDENTIFY retains it in the selectable baseline.

The defensible conclusion is:

> **current interface absence ≠ proof of physical impossibility**

not the stronger claim that every suppressed path remains physically active.

### E3 — a “deeper” address query can itself be policy-conditioned

Case 122's READ NATIVE MAX relation is bounded by Case 123 because DCO can modify the value it returns.

A layered audit therefore needs to name the command/configuration regime rather than treating one number as the drive's metaphysical `true size`.

### E4 — authority state can expire while configuration persists

After power-on reset, DCO FREEZE LOCK's prohibition ends, but DCO SET's reduced configuration is retained.

Thus `who may change the state now` and `what state currently survives` have separate temporal contracts.

### E5 — capability restoration is not integrity verification

A successful DCO RESTORE changes the interface contract. It does not establish that newly addressable sectors are readable/correct, nor that old data has survived.

> **address/capability restored ≠ payload validated**

---

## Cross-case boundaries

### Case 122 — HPA / SET MAX

Case 122: ordinary current maximum can be lowered while READ NATIVE MAX retains a higher HPA-native ceiling.  
Case 123: DCO can lower the maximum that READ NATIVE MAX itself returns and can suppress non-capacity capabilities.

`HPA frontier ≠ DCO capability baseline`.

This is a functional/interface comparison, not a claim that HPA and DCO form one implementation stack.

### Case 113 — ATA 48-bit LBA

Case 113: command encoding determines which LBAs a command family can represent.  
Case 123: current configuration can suppress a feature/capability that exists in the selectable baseline.

`representational capability ≠ configuration-authorized capability`.

### Case 89 — CHS/LBA translation

Case 89 changes the representation relation used to designate sectors. DCO changes the currently exposed capability/capacity contract.

`address representation ≠ capability overlay`.

### Case 44 — forgetting/sanitize

DCO can hide/withdraw ordinary capacity without a media-erasure operation.

`inaccessibility ≠ deallocation ≠ sanitization`.

---

## Claim failures explicitly rejected

- `DCO was invented on 18 July 2000` — unsupported; that is a public proposal date.
- `ATA8-ACS Rev 4a is the final ATA/ATAPI-6 standard` — false; it is a later working draft.
- `READ NATIVE MAX always reports the factory physical capacity` — too strong once DCO is considered.
- `ordinary IDENTIFY reports every capability the device could ever expose` — contradicted by DCO IDENTIFY semantics.
- `DCO SET erases the capacity it hides` — unsupported.
- `DCO RESTORE validates or reconstructs payload` — unsupported.
- `DCO FREEZE LOCK is encryption` — unsupported.
- `DCO and HPA are independent knobs` — contradicted by command validity restrictions.
- `similarity to HPA proves one genealogy` — unsupported.

---

## Related-repository boundary

A current default-branch search of `tmzncty/computing-archaeology` for `Device Configuration Overlay`, `DCO`, and the DCO command names returned no dedicated technical-history case to reuse.

If a broad ATA configuration/HPA/DCO/BIOS genealogy is built, it should primarily live there. This evidence record retains only the capability/configuration lifetime relation needed by `technical-retention`.

---

## Remaining evidence debt

- directly renderable `e00140r0/r1/r2` proposal facsimiles;
- final approved ATA/ATAPI-6 normative DCO text and page anchors;
- proposal-to-final wording change archaeology;
- ATA/ATAPI-7 / ACS DCO revision history;
- earlier capability-overlay / OEM-capacity-config prior art;
- named BIOS/OEM DCO deployment documentation;
- independent hardware traces across IDENTIFY, DCO IDENTIFY, READ NATIVE MAX, SET MAX, RESTORE, and power cycles;
- forensic evidence for physical payload survival behind DCO-reduced capacity;
- interaction with later security/sanitize mechanisms;
- broader genealogy in `computing-archaeology`.
