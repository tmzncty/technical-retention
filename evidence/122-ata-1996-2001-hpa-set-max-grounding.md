# Evidence 122 — ATA Host Protected Area / SET MAX Grounding (1996–2001)

## Research question

Can a disk retain a larger native logical-sector population while a smaller current maximum deliberately removes part of that population from ordinary host reads/writes, and can the addressability policy itself have a lifetime different from the payload?

This record grounds only that bounded relation. It does not attempt a general HPA/DCO/BIOS-recovery history.

---

## Source hierarchy and identity

### P1 — T13 document archive: D96137r0

**Institution:** Technical Committee T13 AT Attachment  
**Document:** `d96137r0 — ATA protected area proposal`  
**Author listed:** Colegrove  
**Submission date:** **24 April 1996**  
**URL:** <https://t13.org/Documents/>

The T13 archive metadata establishes a public standards-development record for an `ATA protected area proposal` by this date.

**What it proves:** proposal title, author metadata, and submission date.  
**What it does not prove:** the exact proposal mechanism without inspecting the proposal facsimile; invention priority; private design chronology.

### P2 — T13 document archive: D97106r0 / D97106r1

**Institution:** Technical Committee T13 AT Attachment  
**Documents:** `SET MAX ADDRESS addition`  
**Author listed:** McLean  
**Submission dates:** **2 December 1996** (r0), **28 January 1997** (r1)  
**URL:** <https://t13.org/Documents/>

**What it proves:** a separately tracked SET MAX proposal trail later than D96137r0.  
**What it does not prove:** that SET MAX was the first protected-area idea or that the proposal date is an invention date.

### P3 — T13/1153D Revision 18, ATA/ATAPI-4 working draft

**Document:** *Information Technology — AT Attachment with Packet Interface Extension (ATA/ATAPI-4)*  
**Identifier:** T13/1153D Revision 18  
**Date:** **19 August 1998**  
**Inspected facsimile:** USPTO PTAB exhibit copy of the T13 draft.

#### Document-status boundary

The cover explicitly says the document is an **internal working document**, `not a completed standard`, and not approved. This record therefore calls it a working draft throughout. It is not silently relabeled as the final ANSI publication.

#### Revision-history locations

The revision history records:

- **Revision 5 — 28 June 1996:** added `D96137R0 Protected area proposal`;
- **Revision 9 — 10 February 1997:** added `SET MAX ADDRESS addition (D97106R1)`;
- **Revision 14 — 26 June 1997:** added a new SET MAX / NATIVE MAX description per `D97119R3`;
- **Revision 18 — 19 August 1998:** later editorial stage inspected here.

This provides the bridge from T13 proposal metadata to a surviving integrated draft.

#### §8.26 — READ NATIVE MAX ADDRESS

Revision 18 §8.26 assigns `READ NATIVE MAX ADDRESS` to the Host Protected Area feature set and defines the native maximum as:

- the highest address accepted by the device in the factory-default condition;
- the maximum address valid for `SET MAX ADDRESS`.

The command can report that native maximum in LBA or CHS form according to the addressing selection.

**Retention relevance:** a native ceiling remains separately knowable even when the current ordinary-access ceiling has been lowered.

#### §8.38 — SET MAX ADDRESS

Revision 18 §8.38 says the command redefines the maximum address of the **user-accessible address space** in either LBA translation or the current CHS translation.

After a successful change:

- relevant `IDENTIFY DEVICE` capacity information reflects the new maximum;
- read/write attempts above the selected maximum are rejected with `ID Not Found`;
- failed SET MAX commands do not change the IDENTIFY contents.

The clause does not say that lowering the maximum rewrites, relocates, erases, encrypts, or sanitizes sectors above the frontier.

#### Maximum-address persistence semantics

The Sector Count input includes a bit controlling whether the maximum-address setting is preserved across power-up / hardware reset or whether the device reverts to the most recent non-volatile maximum-address setting.

The wording is important because it makes the **reachability configuration itself retained state with an explicit lifetime**.

**Engineering consequence:** `addressability-policy lifetime` can differ from `payload lifetime`.

### P4 — Maxtor 541DX Product Manual

**Vendor:** Maxtor Corporation  
**Document:** *Maxtor 541DX Product Manual*  
**Models:** 2B020H1, 2B015H1, 2B010H1  
**P/N:** 1546/A  
**Date floor:** copyright **2001**  
**Vendor-hosted archival URL:** <https://www.seagate.com/staticfiles/maxtor/en_us/documentation/manuals/fireball_541dx_manual.pdf>

The manual is now hosted in Seagate's Maxtor archive and is a named shipping-product witness.

#### Product identity / interface context

The manual describes the 541DX family as Ultra ATA hard drives and lists `Read Native Max Address` / `Set Max Mode` in the interface command summary.

#### Read Native Max Address

The manual says the native maximum is the highest address accepted in the drive's factory-default condition and the maximum valid for SET MAX.

#### Set Max

The manual states that after successful SET MAX completion:

- reads/writes above the selected maximum are rejected with `IDNF`;
- IDENTIFY response fields reflect the maximum set.

It also documents SET MAX password, lock, unlock, and freeze-lock subcommands.

#### Separate lifetime/control state

The manual says the SET MAX password is retained until the next power cycle and describes lock/freeze behavior that restricts later SET MAX commands. These are control/authority states with lifetimes distinct from sector payload and distinct from the maximum-address value itself.

**What P4 proves:** at least one named 2001 Maxtor family implemented the bounded command/control model.  
**What it does not prove:** first implementation, universal ATA behavior, cryptographic protection, or sector-health guarantees above the current maximum.

---

## Evidence chain

```text
24 Apr 1996
T13 D96137r0
"ATA protected area proposal"
        |
28 Jun 1996
ATA/ATAPI-4 rev.5 records integration of D96137R0
        |
2 Dec 1996 / 28 Jan 1997
D97106r0/r1
"SET MAX ADDRESS addition"
        |
10 Feb 1997
ATA/ATAPI-4 rev.9 records integration of D97106R1
        |
26 Jun 1997
rev.14 records revised SET MAX / NATIVE MAX description
        |
19 Aug 1998
rev.18 working draft exposes mature
READ NATIVE MAX + SET MAX semantics
        |
2001
Maxtor 541DX named-product manual implements
READ NATIVE MAX + SET MAX + control subcommands
```

This is a standards-development and implementation floor. It is not an invention genealogy beyond the documented sequence.

---

## Grounded claims

### H/P — proposal chronology is layered

The protected-area proposal is visible in April 1996. SET MAX is separately tracked later in December 1996 / January 1997. The integrated draft records both steps.

> **protected-area concept record ≠ SET MAX proposal record**

### H/P — native maximum and current user maximum are distinct interface state

`READ NATIVE MAX ADDRESS` returns a native/factory-default maximum while `SET MAX ADDRESS` can establish a smaller user-accessible maximum.

> **native address ceiling ≠ current ordinary-service ceiling**

### H/P — lowered reachability is enforced through command admissibility and capacity reporting

Above the selected current maximum, ordinary reads/writes are rejected; IDENTIFY capacity-related state reflects the selected maximum.

> **current reported capacity ≠ native addressable population**

### H/P + X — no erase follows from lowering the frontier

Neither §8.26 nor §8.38 establishes a media erase or payload rewrite when SET MAX lowers the frontier.

> **ordinary inaccessibility ≠ demonstrated payload destruction**

### H/P + E — reachability policy has its own persistence class

The maximum-address setting can be selected to persist across power/reset or to revert to a retained non-volatile setting.

> **payload persistence ≠ reachability-policy persistence**

### H/P — authority/control state is another distinct lifetime

The 2001 Maxtor manual's password/lock/freeze behavior introduces state governing whether later SET MAX changes are admitted. Some such state terminates at power-cycle boundaries.

> **authority to change addressability ≠ addressability frontier ≠ hidden payload**

---

## Engineering reconstruction

### E1 — retained payload can outlive ordinary addressability

Assumptions:

1. payload in a sector above a later-lowered current maximum was intact before the change;
2. SET MAX performs only the documented address-range/configuration operation;
3. no independent media failure occurs.

Then the sector's payload may remain retained while ordinary I/O is rejected because of policy state.

This is weaker and more precise than saying `HPA preserves data`.

### E2 — loss/reversion of metadata can increase reach

A volatile lower maximum may revert after a power/reset boundary while payload remains on the disk. In that path, losing/reverting access-limiting state can make a larger range ordinary-addressable again.

This is a useful counterexample to the intuition that losing retained metadata always reduces access.

### E3 — one device can truthfully support multiple capacity observations

`IDENTIFY DEVICE` after SET MAX and `READ NATIVE MAX ADDRESS` answer different interface questions. A smaller current-capacity observation and a larger native-capacity observation are not necessarily contradictory.

> **capacity observation must be qualified by command and policy state**

### E4 — hidden-sector survival is not guaranteed by address metadata alone

Restoring a larger maximum proves only that addresses become admissible again. It does not prove the corresponding sector payload survived magnetic defects or other failures.

> **address restored ≠ payload validated**

---

## Cross-case boundaries

### Case 89 — ATA CHS/LBA translation

Case 89: representation changes while LBA designation can remain invariant.  
Case 122: admitted address range changes while a larger native population remains separately represented.

`representation change ≠ reachability-frontier change`.

### Case 113 — ATA 48-bit LBA

Case 113: older command syntax lacks bits to encode high LBAs.  
Case 122: a current maximum intentionally excludes addresses even though the device retains a larger native maximum.

`encoding ceiling ≠ policy/configuration ceiling`.

### Case 44 — NVMe deallocation / sanitize

Case 44: logical-currentness reduction and stronger subsystem forgetting operations.  
Case 122: ordinary access can be withheld without evidence that prior payload was forgotten.

`ordinary inaccessibility ≠ logical deallocation ≠ sanitization`.

### Case 14 — defect reassignment

Case 14 changes which physical embodiment serves a logical block. SET MAX does not establish any embodiment replacement.

`reachability change ≠ remapping`.

---

## Rejected claims

- **`D96137r0 = invention date of hidden disk regions`** — unsupported.
- **`D97106r0 = invention date of HPA`** — unsupported and chronologically too coarse; an earlier protected-area proposal is already recorded.
- **`ATA/ATAPI-4 Revision 18 = final approved ANSI standard`** — false document identity; the facsimile says otherwise.
- **`SET MAX hides data by erasing it`** — unsupported.
- **`READ NATIVE MAX proves every high sector is healthy`** — unsupported.
- **`HPA password = payload encryption`** — unsupported.
- **`current IDENTIFY capacity = physical platter capacity`** — unsupported.
- **`HPA = DCO`** — false mechanism collapse; DCO remains separate future work.
- **`HPA = partition hiding`** — false interface collapse.
- **`HPA is an ancestor of NVMe deallocation/sanitize`** — no genealogy established; only bounded functional comparison.

---

## Related-repository check

Searches in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Host Protected Area`, `HPA`, and `SET MAX ADDRESS` returned no dedicated case during this slice.

Therefore this evidence record contains the minimum ATA chronology needed to support the retention-specific relation. A broader history of:

- ATA protected-area proposals;
- BIOS/PARTIES use;
- DCO;
- OEM recovery environments;
- forensic tooling;
- later SATA command evolution

should be developed in the companion repository rather than duplicated here.

---

## Remaining evidence debt

1. Inspect the original D96137r0 protected-area proposal facsimile.
2. Inspect D97106r0/r1 and D97119R3 facsimiles rather than relying on T13 metadata + integrated revision history for their exact wording.
3. Obtain the final approved ATA/ATAPI-4 publication or standards-body archival facsimile and compare exact HPA clauses against Revision 18.
4. Separate HPA from DCO with primary ATA/ATAPI-6 proposal/standard evidence before drawing a general hidden-capacity taxonomy.
5. Add named hardware/fault traces only if they can distinguish current maximum, native maximum, payload integrity, lock state, and power/reset behavior.
