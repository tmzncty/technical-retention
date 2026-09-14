# Evidence 103 — SCSI VERIFY vs Reassignment Authority, 2001–2022

## Status

**`bounded deepening complete`**

## Scope

This record deepens Case 103 along one narrow boundary left open in the canonical case:

> **When a SCSI device is asked to verify a logical block, does that verification operation itself carry the authority to reassign the block, and how should verification evidence be separated from later remediation?**

The central product witness is Seagate's **_Serial Attached SCSI (SAS) SCSI Commands Reference Manual_, Publication 100293068, Rev. M, June 2022**. It is especially useful because one first-party manual documents, side by side:

- `VERIFY` and the `Verify Error Recovery` mode page;
- read-path `ARRE` automatic reallocation;
- explicit `REASSIGN BLOCKS` remediation.

T10 records from 2001 and 2005 provide a standards-development boundary around `REASSIGN BLOCKS` payload handling and Background Medium Scan result states. They are used as period engineering records, not as proof that every shipping implementation behaved identically.

This file does **not** attempt a complete history of SCSI error recovery, bad-sector remapping, VERIFY standardization, or RAID patrol read. Case 14 remains canonical for logical-block identity across physical replacement; Case 101 remains canonical for Background Medium Scan; Case 103 remains canonical for host-issued VERIFY.

---

## Sources inspected

### Primary / first-party sources

1. T10, George Penokie (Tivoli), **01-210r0, _Reassign Blocks 2 TBytes Support_**, 11 July 2001.  
   <https://www.t10.org/ftp/t10/document.01/01-210r0.pdf>

2. T10, **05-344r0, _Working Draft SCSI Block Commands - 3 (SBC-3), Revision 0_**, 9 September 2005.  
   <https://t10.org/ftp/t10/document.05/05-344r0.pdf>

3. T10, **05-340r2, _SBC-3 SPC-4 Background scan additions_**, 11 November 2005.  
   <https://www.t10.org/ftp/t10/document.05/05-340r2.pdf>

4. Seagate Technology LLC, **_Serial Attached SCSI (SAS) SCSI Commands Reference Manual_**, Publication 100293068, Rev. M, June 2022.  
   <https://www.seagate.com/content/dam/seagate/migrated-assets/staticfiles/support/docs/manual/Interface%20manuals/100293068m.pdf>

### Repository context

- [`../cases/103-scsi-verify-host-driven-medium-qualification.md`](../cases/103-scsi-verify-host-driven-medium-qualification.md)
- [`../cases/14-scsi-disk-defect-reassignment-logical-identity.md`](../cases/14-scsi-disk-defect-reassignment-logical-identity.md)
- [`../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md`](../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md)

A fresh search of `tmzncty/computing-archaeology` for `SCSI VERIFY`, `REASSIGN BLOCKS`, `Background Medium Scan`, `bad sector`, and SCSI remapping combinations found no dedicated overlapping history. Broad SCSI command genealogy therefore remains a companion-repository task rather than being recreated here.

---

## Historical record

### H/P — the 2001 T10 REASSIGN proposal does not promise preservation of payload in the reassigned blocks

T10 `01-210r0`, dated 11 July 2001, proposes updated `REASSIGN BLOCKS` parameter handling for larger LBAs. Its command description says that the device server reassigns the physical medium used for each listed logical block address. For the blocks actually named in the defect list, the proposal says their data **may be altered**; only data in all other logical blocks is required to be preserved.

The same proposal notes that one LBA can be reassigned multiple times over the life of the medium until spare locations are exhausted.

This is useful here for a narrow reason: in this 2001 standards-development text, **preserving the logical designation after reassignment is not the same contract as preserving the old payload of that defective block**.

It does not prove that every drive implementing `REASSIGN BLOCKS` in 2001 destroyed or replaced recoverable data. It is an interface-text boundary, not a universal firmware trace.

### H/P — by the September 2005 SBC-3 working draft, REASSIGN explicitly carries recoverable data forward

The 9 September 2005 SBC-3 Revision 0 working draft describes a stronger `REASSIGN BLOCKS` data-handling rule. If the device can recover user data and protection information from the original logical block, it shall write that recovered information to the reassigned logical block. If recovery is not possible, vendor-specific user data is written instead, with a defined default for enabled protection information. Other logical blocks remain preserved.

This establishes a bounded semantic contrast:

```text
2001 proposal:
    data in listed defective blocks may be altered

September 2005 SBC-3 draft:
    if original data is recoverable, carry it to the reassigned block
```

The inspected records do **not** establish the exact accepted proposal, ballot, or revision in which this wording first changed. Therefore this file uses only the defensible bracket:

> **the 2001 proposal and the September 2005 SBC-3 draft do not express the same payload-preservation contract for `REASSIGN BLOCKS`.**

The command name alone is not sufficient evidence for invariant semantics across revisions.

### H/P — the November 2005 Background Scan proposal separates discovery state from several remediation outcomes

T10 `05-340r2`, dated 11 November 2005, revises Background Medium Scan result reporting. Its `REASSIGN STATUS` proposal distinguishes, among other states:

- a failed logical block for which reassignment is still pending host action;
- successful device-side reassignment;
- successful device-side rewrite in place;
- successful application-client reassignment through `REASSIGN BLOCKS`;
- successful application-client action through a write operation;
- failed reassignment paths.

The same proposal contains an editor's note recording that disk-drive vendors in the November CAP working group said they might rewrite rather than always reallocate.

This is **standards-development evidence**, not a claim that every one of these proposed states entered the final standard unchanged or that every product supported every path.

Its value for this case is narrower:

> **the standards work treated error discovery, pending remediation, reassignment, rewrite-in-place, and failed remediation as distinguishable states.**

That directly resists a `verification/discovery = repair` collapse.

### H/P — Seagate 2022 explicitly says verify-medium operations do not trigger automatic read reassignment

Seagate's June 2022 Rev. M manual defines the `Verify Error Recovery` mode page as the error-recovery parameter set used during verify-medium operations, including `VERIFY` and the verify portion of `WRITE AND VERIFY`.

It then states explicitly that **verify-medium operations do not trigger automatic read reassignment**.

This is the strongest negative control in the present slice because the same manual separately documents automatic read reassignment for ordinary read operations.

### H/P — the same Seagate manual gives read operations a separate ARRE-controlled reallocation path

In the `Read-Write Error Recovery` mode page, Seagate documents `ARRE` (`Automatic Read Reallocation Enabled`). When `ARRE=1`, automatic reallocation of defective logical blocks during read operations is enabled. The manual says this automatic reallocation occurs only after successful recovery of the data, and the recovered data is placed in the reallocated logical block.

So within one vendor manual:

```text
read operation + ARRE authority
    may perform automatic reallocation after successful recovery

verify-medium operation
    does not trigger automatic read reassignment
```

This is not merely a difference in scheduling. It is a difference in **remediation authority attached to two access paths**.

### H/P — explicit REASSIGN BLOCKS remains a separate remediation command in the same 2022 manual

The June 2022 manual's `REASSIGN BLOCKS` section requests reassignment of defective logical blocks to another reserved area. It says GLIST should be updated when supported, PLIST is not altered, and—if user data and protection information can be recovered from the original logical block—the recovered information is written to the reassigned logical block. If recovery fails, vendor-specific user data is written instead.

The manual also retains the rule that one LBA may be reassigned more than once over the medium's lifetime until spare locations are exhausted.

Thus the same current first-party command reference exposes three different roles:

```text
VERIFY
    -> qualify / report according to verify criteria

READ with ARRE enabled
    -> ordinary read path may gain automatic-reallocation authority

REASSIGN BLOCKS
    -> explicit defect-remediation command
```

These roles can interact, but the interface does not collapse them into one operation.

---

## Engineering reconstruction

The following are project analytical statements, not T10 or Seagate historical vocabulary.

### E — verification evidence and remediation authority are different relations

A request may exercise a block, perform retries/correction according to verify policy, and produce success or error evidence without itself being authorized to relocate the block.

For the bounded 2022 Seagate interface:

```text
verify-medium error recovery
    !=
automatic read reassignment
```

This gives stronger support to the canonical Case 103 rule:

```text
verification result
    !=
repair completion
```

### E — operation type can change what repair authority is available over the same logical block

The same LBA may be touched through different command paths. In the inspected 2022 manual, ordinary reads can be subject to `ARRE`; verify-medium operations explicitly do not trigger automatic read reassignment.

Therefore:

```text
same logical block
    + different operation class
    -> different remediation authority
```

The retained payload and physical medium have not changed merely because the caller selected a different command, but the permitted maintenance transition has.

### E — successful error recovery during verification is not evidence of relocation

The Verify Error Recovery page provides retry/recovery controls. Because the manual separately states that verify-medium operations do not trigger automatic read reassignment, a successful verify after retries or correction must not be upgraded into evidence that the LBA was physically remapped.

```text
recoverable during VERIFY
    !=
reassigned during VERIFY
```

A physical-location claim requires separate evidence.

### E — a defect can have evidence before it has a completed repair transition

The 2005 BMS proposal makes this explicit in status form: an LBA can be known as failed while remediation is pending. The later repair may be a reassign, a write-driven path, a rewrite in place, or may fail.

So a useful retention decomposition is:

```text
observation / qualification
    -> defect evidence
    -> repair decision / authority
    -> remediation attempt
    -> post-remediation state
```

This is **not** claimed as one mandatory universal pipeline. It is a decomposition of separable roles exposed by the inspected interfaces.

### E — logical-address continuity and payload continuity remain separate even when remediation improves

The 2001 and 2005 texts show why Case 14's distinction must remain explicit. Reassignment can preserve the LBA-to-service relation while the contract for what happens to the old payload differs across revisions.

Therefore:

```text
same LBA after remediation
    !=
proof that the old payload was recoverable
```

and:

```text
same command name across revisions
    !=
identical payload-preservation guarantee
```

---

## Cross-case comparison

### Case 103 — host-driven VERIFY

Case 103 owns the host-driven qualification primitive: the initiator selects a logical-block range and asks the device to verify it. This deepening adds a stronger 2022 negative control around what that primitive does **not** authorize.

> **VERIFY can renew evidence about a medium embodiment without automatically becoming a block-relocation operation.**

### Case 14 — SCSI defect reassignment

Case 14 owns the physical-replacement / logical-identity relation. The present record adds a later semantic bracket: the payload-handling contract attached to `REASSIGN BLOCKS` was not textually invariant between the 2001 T10 proposal and the September 2005 SBC-3 draft.

The cross-case boundary is:

```text
qualification of an embodiment
    !=
replacement of an embodiment
    !=
preservation of the old value across replacement
```

### Case 101 — Background Medium Scan

Case 101 owns proactive device-side discovery and retained scan-result evidence. The November 2005 proposal shows why its `REASSIGN STATUS` is not just another name for `VERIFY`: BMS reporting can describe pending or completed remediation states in addition to discovery.

The useful functional relation is:

```text
VERIFY: initiator asks for bounded qualification
BMS: device-side background discovery/reporting regime
REASSIGN / rewrite: remediation paths
```

No genealogy among these mechanisms is asserted.

---

## Functional analogy — bounded

The general pattern resembles other repository cases where an integrity check is deliberately kept separate from repair authority: ZFS scrub, distributed-replica checking, NAND bad-block classification, and filesystem/device maintenance all contain examples where evidence can exist before repair.

That similarity is only functional. It does not establish historical descent from SCSI command semantics, identical failure models, or identical authority structures.

---

## Philosophical interpretation — bounded

A retained object can be **tested** without being **reconstituted**. The SCSI command boundary makes that distinction unusually concrete: one operation can ask whether a medium embodiment remains acceptable under verification criteria, while another relation controls whether the embodiment may be replaced.

The defensible interpretation is therefore limited:

> **evidence that something still counts as serviceable and authority to change what physically embodies it are separable technical relations.**

This does not imply that observation is metaphysically independent of intervention in every storage technology. It is a claim about the bounded command and error-recovery contracts inspected here.

---

## Explicit non-claims

This record does **not** claim that:

1. `01-210r0` is the final 2001 SBC-2 standard text;
2. every 2001 drive altered payload during `REASSIGN BLOCKS`;
3. the exact committee revision that introduced recover-if-possible semantics has been identified;
4. the November 2005 `05-340r2` proposal entered the final standard unchanged;
5. every drive implements Background Medium Scan;
6. every Seagate product implements every command or option in the June 2022 reference manual;
7. `VERIFY` performs no retries or error correction—its dedicated error-recovery page explicitly provides such controls;
8. a successful VERIFY proves that no latent failure can occur later;
9. a VERIFY error automatically inserts an LBA into a grown-defect list;
10. a VERIFY error automatically invokes `REASSIGN BLOCKS`;
11. automatic read reassignment is the same thing as host-issued `REASSIGN BLOCKS` in all implementations;
12. `ARRE=1` guarantees successful reallocation—the documented path depends on successful data recovery and can itself fail;
13. logical-block reassignment exposes the physical replacement address to the application client;
14. rewrite-in-place and physical reassignment are the same operation;
15. the 2005 BMS proposal's rewrite-in-place alternative proves the final standard or every drive used that path;
16. SCSI VERIFY, BMS, RAID patrol read, filesystem scrub, and distributed checksum scans are one historical lineage;
17. preserving an LBA proves preservation of its prior user data;
18. the present evidence closes the full chronology of SCSI defect management or VERIFY standardization.

---

## Claim ledger

| Claim | Type | Evidence | Strength |
| --- | --- | --- | --- |
| 2001 T10 proposal allows data in reassigned listed blocks to be altered | H/P | T10 01-210r0 | direct |
| September 2005 SBC-3 draft requires recovered data to be written to the reassigned block when recovery succeeds | H/P | T10 05-344r0 | direct |
| exact revision that changed the REASSIGN payload contract is identified | X | not established | rejected |
| November 2005 BMS proposal distinguishes pending, reassigned, rewritten, and failed remediation states | H/P | T10 05-340r2 | direct, proposal-bounded |
| 2022 Seagate verify-medium operations do not trigger automatic read reassignment | H/P | Seagate 100293068 Rev. M | direct |
| 2022 Seagate ordinary read operations may automatically reallocate under ARRE after successful recovery | H/P | Seagate 100293068 Rev. M | direct |
| 2022 Seagate keeps explicit REASSIGN BLOCKS separate from VERIFY | H/P | Seagate 100293068 Rev. M | direct |
| verification evidence and remediation authority are separable | E | cross-read of above interfaces | strong |
| successful verify error recovery proves physical relocation | X | contradicted by 2022 verify/reassignment boundary | rejected |
| same command name guarantees identical semantics across revisions | X | 2001/2005 contrast | rejected |

---

## Remaining evidence debt

This bounded slice closes the canonical Case 103 debt **at the interface-contract level** for VERIFY versus reassignment. It does not close several deeper questions:

- locate the exact T10 proposal / accepted revision that changed `REASSIGN BLOCKS` from the older `data may be altered` wording to the recover-if-possible rule;
- obtain a named-drive execution trace showing a VERIFY medium error followed by host-selected remediation;
- test how a specific product reports a recoverable VERIFY result versus a later ordinary READ with `ARRE` enabled;
- identify cross-vendor product manuals that explicitly state whether verify-medium operations may or may not trigger relocation;
- distinguish command-level remediation authority from undocumented firmware maintenance that may happen outside the command contract;
- continue the wider HDD defect-management / CHS→LBA chronology in `computing-archaeology` rather than rebuilding it here.

---

## Result

**Bounded deepening complete.**

The main result is not that VERIFY is a passive operation. It can perform genuine medium work, retries, correction, and qualification. The stronger and better-supported boundary is:

```text
verification work
    !=
automatic reassignment authority
```

In the June 2022 Seagate command reference, verify-medium operations explicitly do not trigger automatic read reassignment, while ordinary reads can receive that authority through `ARRE` and `REASSIGN BLOCKS` remains an explicit defect-remediation command. T10 records from 2001–2005 further show that even the remediation command's payload-preservation contract must be dated rather than assumed from its name.