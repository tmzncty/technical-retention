# SCSI Disk Defect Reassignment: Logical Block Identity Across Physical Replacement

## Scope

- **Bounded period:** 1990–1997.
- **Primary mechanism witness:** Litko Chan / NeXT, U.S. Patent 5,271,018, **“Method and apparatus for media defect management and media addressing,”** filed 27 April 1990 and issued 14 December 1993.
- **Primary interface witness:** Seagate, **_Disc Drive SCSI-2/SCSI-3 Interface Product Manual (Vol. 2; Ver. 2), Rev. H_**, August 1997, especially §5.2.1.3 `Reassign Blocks Command (07h)`.
- **Named-product corroboration:** Seagate **ST43401N/ND and ST43402ND Reference Manual, Rev. C**, December 1994.
- **Automatic-reallocation policy deepening:** [`../evidence/14-seagate-1991-1996-awre-arre-saved-policy-deepening.md`](../evidence/14-seagate-1991-1996-awre-arre-saved-policy-deepening.md), using the 1991 ST3283N and 1996 Hawk 4 ST15230W/WD/WC/DC manuals to separate repair capability, savable `AWRE`/`ARRE` admission policy, volatile Current state, retained Saved/default state, value recoverability, spare capacity, and repair closure.
- **Research question:** what remains the “same” when a host-visible logical block address stays usable while the physical disk sector carrying that logical block is replaced after a media defect?

This is **not** a general history of hard disks, SCSI, Winchester technology, zone-bit recording, CHS-to-LBA interfaces, SMART, or every vendor's bad-sector policy. The broad ROADMAP item `HDD geometry, bad-sector remapping, CHS → LBA` therefore remains open.

The narrower retention problem is:

> A logical block can keep the same host-visible designation while the controller changes which physical sector embodies it. But that reassignment operation does not necessarily preserve the block's payload by itself.

The automatic-reallocation deepening adds a second boundary:

> The ability to substitute a spare sector is not the same thing as the retained policy that admits automatic substitution, and neither is the same thing as successful recovery of the value that must populate the replacement.

That combination makes this case a useful counterweight to mapped Flash: **designation continuity, physical-location continuity, payload continuity, repair policy, and repair capacity are different relations.**

---

## Historical vocabulary

The period sources themselves use terms including:

- `logical block address` / `LBA`;
- `physical target address`;
- `primary defect list` / `PDL`;
- `secondary defect list` / `SDL`;
- `manufacturer's defect`;
- `grown defect`;
- `sector slipping`;
- `linear displacement` / replacement;
- `spare sector` / `spare location`;
- `Reassign Blocks`;
- `Defect Logical Block Address`;
- `automatic reallocation`;
- `Automatic Write Reallocation Enabled` / `AWRE`;
- `Automatic Read Reallocation Enabled` / `ARRE`;
- `Current`, `Saved`, `Default`, and `Changeable` mode parameters;
- `Save Mode Parameters` / `SP`;
- `NO DEFECT SPARE LOCATION AVAILABLE`.

The following are **project engineering terms**, not claims about actors' vocabulary:

- `logical identity`;
- `designation continuity`;
- `repair slack`;
- `repair-admission policy`;
- `retention-control state`;
- `mapping-mediated retention`.

Likewise, comparing this mechanism to a later Flash Translation Layer is a **functional analogy**, not a claim that 1990s disk defect management was historically called an FTL or directly descended from one.

---

## Historical record

### H/P — the host-visible LBA and the physical target address are explicitly different addresses

Chan's 1990-filed patent describes each disk sector as having both a `logical block address` and a `physical target address`.

The patent defines the LBA as the address used by the host to read and write, while the physical target address is the actual location on the disk surface, typically expressed by track and sector. A controller translator converts between the two.

This is direct period evidence for an address abstraction in which the address used by the host does not have to be identical to one immutable physical sector location.

The patent presents this material partly as **prior art**. It therefore cannot support a claim that NeXT or Chan invented logical block addressing, defect remapping, sector slipping, or linear displacement.

**Primary anchor:** US5271018A, background discussion surrounding FIGS. 1A–1C and FIG. 2.

### H/P — manufacturer defects and grown defects impose different replacement work in the bounded account

For manufacturer defects, the patent describes `sector slipping`: a defective physical sector is skipped during formatting and the next usable sector receives the next LBA. The host still sees a contiguous sequence of logical blocks while spare capacity is consumed underneath it.

For a defect that appears after user data have been placed — a `grown defect` — the patent explains why simply slipping every later block is no longer acceptable. Subsequent blocks have already been identified by their current LBAs; changing those addresses would produce lost data or misreads. The defective LBA is instead associated with a spare physical sector, and the `secondary defect list` records the relationship between defective and replacement locations.

This gives the case a retention-specific historical boundary:

> preserving the host's existing logical designation can itself constrain how repair is performed.

### H/P — a normal access can traverse retained defect metadata before reaching the current physical sector

In the patent's prior-art flow, a host LBA is translated to an initial physical target address. The controller then consults the PDL for slip adjustments and the SDL for grown-defect replacements. If the translated target corresponds to a grown defect, the SDL supplies the replacement physical target.

The PDL and SDL are stored on the disk and read into controller RAM at power-up.

Thus the disk's usable logical-block service is not supplied by magnetic payload bits alone. It also depends on retained and recoverable **defect/replacement metadata** that tells the controller which physical sector currently counts for a logical designation.

### H/P — Seagate's 1991 ST3283N makes automatic reassignment a configurable and savable error-recovery policy

The ST3283N SCSI Interface Drive Product Manual, Rev. A, dated 9 November 1991, exposes `AWRE` and `ARRE` in Error Recovery Page `01h`.

For this named product:

- both `AWRE` and `ARRE` have documented default value `0`;
- the bits are marked changeable by the initiator;
- the Error Recovery Page is parameter-savable;
- `AWRE=1` admits automatic reallocation of bad blocks detected during writes;
- `ARRE=1` admits automatic reallocation of bad blocks detected during reads;
- with the corresponding bit clear, the automatic path is suppressed and a Medium Error / host-visible handling path remains.

The same manual's Appendix A states that, with ARRE enabled, certain read errors that are successfully recovered only after additional retries or ECC correction are automatically reallocated, while unrecoverable sectors remain for explicit `REASSIGN BLOCKS` handling. With AWRE enabled, a documented write/header failure can cause automatic sector replacement and rewriting of the data field.

This establishes:

```text
automatic-reallocation capability
        !=
automatic-reallocation admission policy
```

and, on the read side:

```text
automatic repair enabled
        !=
old value successfully recovered
```

The product semantics are deepened in [`../evidence/14-seagate-1991-1996-awre-arre-saved-policy-deepening.md`](../evidence/14-seagate-1991-1996-awre-arre-saved-policy-deepening.md).

### H/P — current repair policy can be volatile while the configured policy survives reset

The ST3283N manual separates Mode Sense values into Current, Changeable, Default, and Saved views. Current values are the values actually controlling operation. After power-on reset, hard reset, or Bus Device Reset, Current values are reconstructed from Saved values when they can be retrieved, otherwise from Default values.

Its Mode Select semantics also distinguish setting Current parameters from saving savable parameters. With `SP=1`, the drive saves the savable parameter state and does not return Good status until that save operation completes; an error leaves Saved parameters unchanged.

Therefore:

```text
Current volatile policy embodiment lost at reset
        !=
configured repair policy forgotten
```

provided that the retained Saved/default source remains available.

This is an interface/recovery relation, not a claim that every internal parameter-write path is arbitrarily power-fail atomic.

### H/P — Hawk 4 makes the physical embodiment of Default, Saved, Current, and Changeable policy state explicit

Seagate's March 1996 Hawk 4 Family (Wide) SCSI-2 manual for ST15230W/WD/WC/DC lists an `Integrated SCSI Controller` and explicitly states that the drive maintains four sets of mode parameters:

```text
Default values   -> firmware in flash E-PROM on the PCB
Saved values     -> disk media
Current values   -> volatile memory used to control operation
Changeable mask  -> nonvolatile memory
```

At power-up, Saved values from the media are loaded into Current volatile storage. The SCSI-2 mode table gives Error Recovery Page `01h` a default byte 2 of `00h` and a change mask of `EFh`, independently corroborating that supported error-recovery controls can ship disabled by default while remaining initiator-changeable.

This named-family product evidence blocks another shortcut:

```text
default off
        !=
feature absent
```

It does **not** establish that ST3283N and Hawk 4 use the same controller silicon or one direct design lineage.

### H/P — SCSI `REASSIGN BLOCKS` explicitly changes the physical medium behind the same LBA

Seagate's August 1997 interface manual defines `Reassign Blocks Command (07h)` as a request to reassign defective logical blocks to an area reserved for that purpose. The initiator sends a defect list containing the logical block addresses to be reassigned, and the drive changes the **physical medium used for each logical block address**.

The same manual says that, after the command completes, recovered data may be written back to the **same Logical Block Addresses**.

It also states that a logical block which has already been reassigned can be reassigned again. Over the life of the medium, the same logical block can therefore be assigned to multiple physical addresses until spare locations are exhausted.

**Primary anchor:** Seagate, _Disc Drive SCSI-2/SCSI-3 Interface Product Manual_, Rev. H, August 1997, §5.2.1.3, manual pp. 137–138.

### H/P — physical replacement does not automatically preserve the defective block's data

The same Seagate command description contains a crucial limit: data in the logical blocks named for reassignment **is not preserved** by the command. Other logical blocks remain preserved, and the manual recommends that the initiator recover the affected data before issuing reassignment, then write the recovered data back to the same LBA afterward.

Therefore:

```text
same host-visible LBA after reassignment
        ≠
automatic survival of the old payload
```

A stable logical designation can survive a change of physical embodiment even when payload recovery is a separate operation that may fail.

This prevents an overly strong reading of “logical identity survives relocation.” What survives unconditionally in the command semantics is the **address relation / service slot**; the old data value survives only if it can be recovered or reconstructed and rewritten.

### H/P — the repair reserve is finite, and automatic repair has distinct closure failures

Seagate's 1997 manual specifies failure when the logical unit has insufficient spare capacity: `NO DEFECT SPARE LOCATION AVAILABLE`. It also returns the first LBA that could not be reassigned when available.

The December 1994 ST43401N/ND and ST43402ND reference manual independently exposes sense codes for:

- write error recovered with auto reallocation;
- write error with auto-reallocation failure;
- unrecovered read error with auto-reallocate failure;
- recovered data with auto reallocation;
- defect-list errors;
- missing primary or grown defect lists;
- `No defect spare location available`;
- `Defect list update failure`.

This turns spare space, defect metadata, and automatic-repair outcome into explicit parts of the failure model rather than invisible controller conveniences.

It also means:

```text
AWRE/ARRE enabled
        !=
repair succeeded
```

because source-value recovery, replacement capacity, and metadata-update success remain separate prerequisites.

### H/P — host-visible LBA abstraction does not make physical geometry disappear

The same 1997 Seagate interface manual supports defect descriptors in physical-sector format containing cylinder number, head number, and defect sector number, while `REASSIGN BLOCKS` itself accepts four-byte defect LBAs.

Chan's patent likewise distinguishes host LBA from a physical target expressed through track/sector coordinates.

The bounded historical conclusion is therefore not that LBA “abolished geometry.” It is that a controller can expose a logical-block interface while physical geometry remains operative inside media management and defect description.

---

## Retained state

This case has several distinct retained states or resources.

### 1. Magnetic payload state

The current data value is physically encoded on magnetic media at whichever sector is presently assigned to the logical block.

### 2. Host-visible logical designation

The host continues to address a block by LBA even when the physical sector serving that LBA changes.

### 3. Defect / replacement metadata

PDL, SDL, grown-defect state, or equivalent drive-maintained structures determine which physical sectors must be skipped or replaced.

### 4. Spare capacity

Unused replacement locations are not themselves payload, but they are a finite resource that makes later defect repair possible.

This suggests a useful distinction:

> **retention capacity is not only occupied data capacity; reserved repair capacity can be part of what makes future retention possible.**

That sentence is an engineering reconstruction, not period vocabulary.

### 5. Repair-policy state

The ST3283N and Hawk 4 evidence adds another layer: mode parameters can decide whether an ordinary read/write error is eligible for device-local automatic reallocation.

For the bounded product evidence, that policy itself can be decomposed into:

```text
Default policy
Saved nonvolatile policy
Current volatile policy
Changeability / authority mask
```

This means that the retention system may need not only payload, mappings, and spare material, but also retained control state governing whether later repair work is automatically admitted.

`retention-control state` is project vocabulary, not a historical Seagate term.

---

## Substrate and retention mechanism

The bounded system is layered:

```text
magnetic sector state
        +
physical disk geometry
        +
controller address translation
        +
defect/replacement metadata
        +
reserved spare sectors
        +
error-recovery / automatic-reallocation policy
```

At rest, the magnetic state is nonvolatile in the ordinary disk sense. The distinctive retention work in this case appears when media defects threaten an existing logical block.

A grown defect can trigger an **exceptional repair path**:

1. identify or report the affected logical block;
2. determine whether automatic repair is admitted by the current error-recovery policy or must be host initiated;
3. recover or otherwise obtain the value that should remain current, where possible;
4. assign another physical location to the same LBA;
5. update defect/replacement metadata;
6. rewrite the recovered or newly supplied value to that same logical designation.

The repair is therefore **failure-triggered**, not ordinary rewrite relocation by default in the evidence used here.

The 1991 product evidence adds a control distinction:

```text
repair needed
    !=
automatic repair admitted
```

---

## Addressing and access geometry

The host operates with an LBA-oriented interface.

Inside the bounded Chan account, normal read/write resolution can be reconstructed as:

```text
host LBA
    ↓
initial physical-target translation
    ↓
PDL slip adjustment
    ↓
SDL grown-defect replacement lookup
    ↓
current physical target
```

The physical layer can still be expressed through track/sector or cylinder/head/sector-like coordinates.

This matters because **address abstraction does not imply substrate abstraction has ceased to matter**. It means the service has inserted retained relations between the designation used above and the current physical location below.

---

## Read, write, and repair semantics

### Ordinary read

The SCSI interface describes reads in logical-block terms; the host asks for an LBA, not for a particular spare sector.

With `ARRE` admitted in the bounded ST3283N implementation, some successfully recovered read errors can additionally trigger device-local automatic relocation before the service continues.

### Ordinary write

Writes likewise target logical blocks. The internal physical target can be changed by defect-management state.

With `AWRE` enabled in the ST3283N evidence, a documented write/header failure can trigger automatic sector replacement and rewriting of the write data.

### Reassignment

`REASSIGN BLOCKS` is not just another normal write. It changes which physical medium serves one or more logical block addresses.

It also remains distinct from automatic reallocation during ordinary I/O: the latter is conditioned by saved/current error-recovery policy, while the explicit command is initiated as a separate host repair operation.

### Recovery before reassignment

Because reassignment itself does not preserve the affected block's data, recovery and rewrite are separate obligations.

This gives a three-layer state transition:

```text
preserve designation
        ≠
choose replacement embodiment
        ≠
preserve/reconstruct payload
```

The automatic-reallocation deepening adds a fourth distinction:

```text
repair capability
        ≠
repair-admission policy
```

---

## Failure and forgetting

Retention can fail here through several independent paths:

- the magnetic payload becomes unreadable before it can be recovered;
- a sector becomes a grown defect;
- ECC/retries cannot recover the old payload;
- automatic reallocation is supported but disabled by current policy;
- current policy cannot be reconstructed because its Saved/default source is unavailable or invalid;
- reassignment cannot find spare capacity;
- automatic reallocation is attempted but fails;
- defect-list metadata is absent, corrupt, or cannot be updated;
- the mapping from logical designation to physical replacement is lost or misapplied;
- controller/interface state cannot reconstruct the current physical target.

The source set does **not** justify a universal claim about how every 1990s or modern HDD handles each failure internally.

---

## Engineering reconstruction

### E — logical-block retention can be relational rather than locational

The host-visible LBA can remain invariant while a physical sector changes. The retained service therefore includes a relation:

```text
logical designation → current usable embodiment
```

### E — address continuity and value continuity must be audited separately

The Seagate command semantics are a direct counterexample to treating those as one property. The address can be reassigned successfully while the old value has already been lost.

### E — maintenance metadata is part of the retention system

A physical copy of user data is not sufficient to reproduce the logical service if the controller cannot determine which physical sector serves the logical address. Defect lists and replacement state therefore belong in the retention analysis.

### E — spare capacity is latent repair capability

A spare sector is “unused” from the host's payload perspective but can be necessary for retaining the service after a later defect. `NO DEFECT SPARE LOCATION AVAILABLE` makes this finite dependency visible.

### E — repair policy is distinct retained control state

The 1991 and 1996 Seagate evidence establishes that automatic reallocation can be controlled by mode parameters whose current runtime embodiment is distinct from saved/default state used after reset.

This gives:

```text
automatic-reallocation capability
    !=
configured admission policy
    !=
current volatile policy embodiment
    !=
automatic repair actually attempted
```

A present payload can remain correct even while future local repair admission is misconfigured, and an enabled repair policy can exist even when there is no current defect.

### E — reset of Current state need not mean loss of the repair relation

For the named products, Current mode parameters can be reconstructed from Saved/default state after reset.

Therefore:

```text
volatile control embodiment lost
    !=
configured repair relation lost
```

provided the retained source remains retrievable.

### E — successful repair requires more than admission

The combined source set supports a stronger closure boundary:

```text
repair admitted
    + value available / recoverable
    + spare embodiment available
    + defect metadata update succeeds
    -> repair may close
```

This prevents `AWRE=1` or `ARRE=1` from being misread as “data is safe.”

---

## Functional analogy

### A — comparison with mapped Flash, Case 04

The useful analogy is narrow:

- **HDD defect reassignment:** one LBA can survive failure-triggered replacement of its physical sector;
- **mapped Flash:** one logical/virtual designation can survive routine out-of-place update, copy, reclamation, and erase-driven relocation.

Both cases demonstrate:

> logical designation need not be identical with one permanent physical location.

But the mechanisms are historically and operationally different. This case does **not** establish an FTL, erase-before-write garbage collection, wear leveling, or a direct genealogy from disk remapping to Flash mapping.

### A — comparison with NAND bad-block replacement, Case 78

Both cases use hidden replacement capacity to continue a higher-level address service after physical defects.

But the present case uses magnetic-disk defect management, SCSI error-recovery controls, and grown-defect/reassignment semantics; Case 78 concerns NAND factory/lifetime bad blocks and reserved replacement blocks. The comparison is functional only and establishes no shared implementation or genealogy.

### A — comparison with NVMe SMART / Health, Case 55

Case 55's `Available Spare` and threshold warning are observations about remaining reserve/health. `AWRE` and `ARRE` are controls governing whether an automatic repair path may run.

Thus:

```text
reserve telemetry
    !=
repair-admission policy
```

The two cases can be compared because both expose dependencies on hidden repair capacity, not because ATA/SCSI SMART, NVMe SMART, and SCSI error-recovery pages are historically one interface.

### A — comparison with RADOS, Case 05

Both cases can preserve a logical service despite replacement of a physical embodiment. RADOS, however, adds replica multiplicity, protocol currentness, temporary authority, membership, and repair among multiple OSDs. A disk spare-sector substitution is not a distributed-replication protocol.

---

## Philosophical interpretation

### I — identity need not mean material sameness

This case supplies a very narrow technical test for claims about identity through persistence. The thing the host continues to call `LBA n` can remain a valid designation after its physical sector changes.

Yet the Seagate data-loss boundary prevents an easy metaphysical slogan. A preserved name/service slot is not enough to prove that the same informational content survived.

A cautious formulation is:

> **technical identity can be maintained by rules of designation and replacement, but those rules do not by themselves guarantee continuity of the value designated.**

The automatic-reallocation evidence adds a second narrow interpretive point:

> **a system may retain rules governing whether it will attempt future repair, without those rules being identical to either the payload being protected or the repair resources themselves.**

This is not a claim that a disk “remembers how to heal itself.” It is a controlled interpretation of documented nonvolatile repair-policy state.

The engineering case disciplines philosophical discussion; it does not prove a general metaphysics of identity or technical self-maintenance.

---

## Rejected / unsupported claims

### X — “NeXT or Chan invented LBA or bad-sector remapping”

Rejected. US5271018A explicitly presents the relevant sector-slipping and linear-displacement mechanisms as prior art.

### X — “LBA made disk geometry disappear”

Rejected. The same period sources continue to describe physical target addresses and physical-sector defect geometry underneath the logical interface.

### X — “REASSIGN BLOCKS automatically preserves data”

Rejected. Seagate explicitly says the data in blocks selected for reassignment is not preserved by the command.

### X — “support for AWRE/ARRE means automatic reallocation is enabled”

Rejected. The ST3283N documents both bits as supported/changeable while their default values are zero.

### X — “AWRE/ARRE enabled means reassignment must succeed”

Rejected. The named-product evidence separately exposes auto-reallocation failure, unrecoverable read errors, no-spare failure, and defect-list update failure.

### X — “a reset that discards Current values necessarily forgets the repair policy”

Rejected for the bounded products. Current values are rebuilt from retained Saved/default state when retrievable.

### X — “Saved policy and Current policy are one state”

Rejected. The manuals explicitly distinguish retained Saved/default values from volatile Current operating values.

### X — “HDD bad-sector remapping is a Flash Translation Layer”

Rejected. Similarity in logical/physical indirection is a functional analogy only.

### X — “this case closes the history of CHS → LBA”

Rejected. The broad interface chronology remains a separate ROADMAP task.

### X — “every HDD uses this exact PDL/SDL, AWRE/ARRE default, or spare-sector implementation”

Rejected. The case is bounded to the documented mechanisms and interface semantics in the cited period sources.

### X — “the source set proves arbitrary power-fail atomicity of saved mode-parameter updates”

Rejected. Ordinary command/save completion semantics do not by themselves establish sudden-power-loss behavior at every internal persistence boundary.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| period sources distinguish LBA from physical target address | H/P | strong: US5271018A |
| grown-defect replacement can preserve an existing LBA while changing physical target | H/P | strong: US5271018A + Seagate Reassign Blocks |
| PDL/SDL or equivalent defect metadata participates in address resolution | H/P | strong for bounded Chan account |
| ST3283N exposes changeable, savable AWRE/ARRE automatic-reallocation policy | H/P | strong: 1991 Seagate product manual |
| ST3283N documents AWRE=0 / ARRE=0 defaults while still supporting those controls | H/P | strong for named product |
| after reset ST3283N Current mode values are reconstructed from Saved/default state | H/P | strong for named product |
| Hawk 4 explicitly separates firmware Default, disk-resident Saved, volatile Current, and nonvolatile Changeable state | H/P | strong: 1996 Seagate product manual |
| automatic read reallocation remains distinct from successful recovery of an old value | H/P + E | strong: ST3283N appendix + 1994 product failure codes |
| reassignment itself need not preserve the affected payload | H/P | strong: Seagate 1997 §5.2.1.3 |
| one LBA may be reassigned to multiple physical addresses over medium life | H/P | strong: Seagate 1997 §5.2.1.3 |
| finite spare exhaustion is a retention/repair failure mode | H/P + E | strong: Seagate 1997 + 1994 product manual |
| repair capability, repair admission, spare capacity, and repair closure are distinct relations | E | strongly supported by combined product/interface evidence |
| logical identity can be maintained relationally rather than by fixed physical location | E | strongly supported by bounded mechanisms |
| HDD remapping and Flash FTL are historically the same mechanism | X | explicitly rejected |
| stable logical designation guarantees payload continuity | X | directly contradicted by Seagate command semantics |
| support for automatic reallocation guarantees it is enabled or will succeed | X | directly contradicted by named-product policy/failure semantics |
| this case establishes the whole CHS→LBA transition | X | explicitly rejected |

---

## Source and inspection notes

### Primary sources

1. Litko Chan, **US5271018A, _Method and apparatus for media defect management and media addressing_**, filed 27 April 1990, issued 14 December 1993, original assignee NeXT, Inc.  
   <https://patents.google.com/patent/US5271018A>

2. Seagate Technology, **_ST3283N SCSI Interface Drive Product Manual, Rev. A_**, Publication 36184-001, 9 November 1991, especially §6.1.10, Mode Sense page-control semantics, §7.1, and Appendix A.  
   <https://www.seagate.com/support/disc/manuals/scsi/3293npm.pdf>

3. Seagate Technology, **_ST43401N/ND and ST43402ND Reference Manual, Rev. C_**, Publication 83327730, December 1994.  
   <https://www.seagate.com/support/disc/manuals/scsi/27730c.pdf>

4. Seagate Technology, **_Product Manual — Hawk 4 Family (Wide) SCSI-2 (Volume 1), Rev. E_**, Publication 77767479, March 1996, especially §11.3.2 and Table 11.3.2-2.  
   <https://www.seagate.com/support/disc/manuals/scsi/67479_e.pdf>

5. Seagate Technology, **_Disc Drive SCSI-2/SCSI-3 Interface Product Manual (Vol. 2; Ver. 2), Rev. H_**, Publication 77738479, August 1997, especially §5.2.1.3 `Reassign Blocks Command (07h)`, manual pp. 137–138.  
   <https://bitsavers.trailing-edge.com/pdf/seagate/scsi/77738479H_SCSI-2_SCSI-3_Interface_Product_Manual_Volume_2_Version_2.pdf_199708.pdf>

### Inspection boundary

- US5271018A was directly inspected as full primary text in the original grounding pass.
- The 1991 ST3283N manual and 1996 Hawk 4 manual are Seagate-authored PDFs currently hosted by Seagate. Their relevant pages were directly inspected through page-preserving extracted text. Screenshot rendering was attempted for the large relevant pages but the remote renderer did not return usable page images in this pass, so no layout-sensitive claim depends on them.
- The smaller December 1994 Seagate product manual was directly text-inspected and an adjacent relevant sense-code page was visually rendered.
- The August 1997 Seagate manual was directly inspected through page-preserving PDF text extraction in the original grounding; fresh screenshot rendering of the large mirror's Reassign Blocks pages timed out in that research pass, so no figure/layout claim depends on visual inspection.
- An earlier HP 97540 SCSI-2 manual and the SCSI-2 standard were found during discovery, but direct retrieval was unreliable in the original grounding. They are not needed for the central claims and are not used to manufacture an unsupported priority claim.

---

## Related repositories

`tmzncty/computing-archaeology` was searched again before this deepening for combinations including `ST15230 AWRE ARRE automatic reallocation` and `SCSI bad sector remap defect reallocation`. No directly overlapping dedicated packet was returned.

That negative search is a routing check, not proof that the companion repository contains no disk-related material. A future broad history of SCSI defect-management standardization, disk geometry, zone recording, CHS/LBA interfaces, controller silicon, and vendor implementation genealogy should still belong primarily there; this file keeps only the retention-specific logical-identity / repair-policy argument.

---

## Status

**grounded**

The case has period primary mechanism evidence, manufacturer interface semantics, named-product corroboration, explicit failure modes, historical vocabulary, and bounded counterclaims. The 1991–1996 automatic-reallocation deepening now adds a named-product control boundary: **repair capability != repair-admission policy != current volatile policy embodiment != value recoverability != spare capacity != metadata-update success != repair closure**.

Remaining work is narrower and should not block the current maturity: empirical spare-exhaustion progression, sudden-power-loss testing of saved mode-parameter updates, controller-silicon internals, broader SCSI/ATA defect-management genealogy, and the larger HDD/CHS→LBA chronology remain open.