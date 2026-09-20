# Case 14 deepening — Seagate AWRE/ARRE automatic-reallocation policy, saved mode state, and repair closure (1991–1996)

## Status

**Bounded deepening complete.**

This packet deepens [`../cases/14-scsi-disk-defect-reassignment-logical-identity.md`](../cases/14-scsi-disk-defect-reassignment-logical-identity.md) without changing its maturity from `grounded`.

The existing case already established that:

- a host-visible LBA can survive replacement of the physical sector that embodies it;
- `REASSIGN BLOCKS` changes the physical medium behind an LBA but does not itself guarantee survival of the old payload;
- finite spare locations and defect-list update failure are explicit failure boundaries.

The remaining roadmap seam addressed here is narrower:

> when a period drive can reallocate a defective sector automatically during ordinary reads or writes, what retained control state admits that repair, what must still succeed before the repair closes, and what survives a reset?

The source set gives a bounded answer for named Seagate products rather than a generic claim about all SCSI disks.

---

## Why this slice is separate from the original Case 14 grounding

The original grounding used the 1994 ST43401N/ND / ST43402ND manual chiefly as a product witness that `auto reallocation` success/failure, defect-list failures, and spare exhaustion were concrete device conditions. It did not reconstruct the control plane that determines whether automatic reassignment is attempted.

This deepening adds that control plane from two Seagate-authored product manuals:

1. the **ST3283N SCSI Interface Drive Product Manual, Rev. A, 9 November 1991**;
2. the **Hawk 4 Family (Wide) SCSI-2 Product Manual, Rev. E, March 1996**, for ST15230W/WD/WC/DC.

The 1991 ST3283N manual directly documents:

- `AWRE` — Automatic Write Reallocation Enabled;
- `ARRE` — Automatic Read Reallocation Enabled;
- a savable Error Recovery mode page;
- current, saved, default, and changeable parameter views;
- reset-time reconstruction of current parameters from saved or default state;
- an appendix that distinguishes automatic repair of recovered/recoverable errors from explicit host `REASSIGN BLOCKS` work.

The 1996 Hawk 4 manual independently makes the physical embodiment of the four mode-parameter classes unusually explicit:

- Default values in firmware stored in flash E-PROM on the PCB;
- Saved values stored on disk media;
- Current values as volatile control state;
- Changeable masks retained in nonvolatile memory.

This lets the case separate **repair capability**, **repair-admission policy**, **current execution state**, **repair material**, and **repair closure**.

---

## Source set and custody

### Primary source A — Seagate ST3283N, 1991

Seagate Technology, **_ST3283N SCSI Interface Drive Product Manual, Rev. A_**, Publication 36184-001, 9 November 1991.

First-party Seagate PDF:

<https://www.seagate.com/support/disc/manuals/scsi/3293npm.pdf>

Primary anchors used here:

- p. 131 / §6.1.10 `Mode Select Command (15H)` — saving mode parameters;
- p. 140 / Mode Sense page-control description — current/default/changeable/saved semantics and reset behavior;
- pp. 172–175 / §7.1 `Error Recovery Page` — `AWRE`, `ARRE`, defaults, changeability, and page savability;
- pp. 197–198 / Appendix A error-recovery notes — automatic read/write reallocation versus explicit `REASSIGN BLOCKS`.

The inspected public artifact is Seagate-authored and currently hosted by Seagate. Page-preserving text extraction was directly inspected. Screenshot rendering of the relevant large-PDF pages was attempted but the remote renderer did not return usable page images in this pass, so no layout-sensitive claim is made.

### Primary source B — Seagate ST43401N/ND and ST43402ND, 1994

Seagate Technology, **_ST43401N/ND and ST43402ND Reference Manual, Rev. C_**, Publication 83327730, December 1994.

First-party Seagate PDF:

<https://www.seagate.com/support/disc/manuals/scsi/27730c.pdf>

Primary anchors used here:

- manual p. 34 / PDF p. 41 — `Write error recovered with auto reallocation`, `Write error—auto reallocation failed`, and `Unrecovered read error—auto reallocate failed`;
- manual p. 35 / PDF p. 42 — recovered-data codes that explicitly say the data were auto-reallocated;
- manual p. 36 / PDF p. 43 — `No defect spare location available` and `Defect list update failure`.

The relevant sense-code pages were directly text-inspected, and one of the adjacent pages was also visually rendered in this pass.

### Primary source C — Seagate Hawk 4 family, 1996

Seagate Technology, **_Product Manual — Hawk 4 Family (Wide) SCSI-2 (Volume 1), Rev. E_**, Publication 77767479, March 1996, for ST15230W/WD/WC/DC.

First-party Seagate PDF:

<https://www.seagate.com/support/disc/manuals/scsi/67479_e.pdf>

Primary anchors used here:

- p. 5 — the family includes an `Integrated SCSI Controller`;
- pp. 42–43 / §11.3.2 — Default, Saved, Current, and Changeable mode-parameter classes;
- p. 44 / Table 11.3.2-2 — SCSI-2 Error Recovery Page defaults and change masks for ST15230W/WD/WC/DC.

The inspected artifact is Seagate-authored and currently hosted by Seagate. Page-preserving extracted text was directly inspected. Screenshot retrieval for the relevant mode-page tables returned a cache error, so no claim here depends on typography or visual table geometry beyond the extracted byte sequence.

---

# Historical record

## H/P — automatic reallocation is a configurable policy, not an inevitable consequence of having spare sectors

The ST3283N Error Recovery Page exposes two distinct control bits:

- `AWRE` for automatic write reallocation;
- `ARRE` for automatic read reallocation.

The manual gives both bits a default value of `0` and marks them changeable by the initiator. The page itself is marked parameter-savable.

Therefore, for this named 1991 drive:

```text
hardware/firmware supports automatic reallocation
        !=
automatic reallocation currently admitted by policy
```

A drive can possess defect-management machinery and spare capacity while the corresponding automatic action is disabled.

This is a historical interface fact for the named product, not a claim that every SCSI implementation shipped with the same defaults.

## H/P — the same drive distinguishes current control state from saved and default control state

The ST3283N `MODE SENSE` semantics distinguish four parameter views.

The relevant retained-state relations are:

- **Current values** — values presently used by the drive to control operation;
- **Saved values** — values retained in nonvolatile memory;
- **Default values** — fallback values used after reset if valid Saved values cannot be retrieved;
- **Changeable values** — a mask describing what an initiator is permitted to modify.

After a power-on reset, hard reset, or Bus Device Reset, Current values are reconstructed from Saved values when they are retrievable, otherwise from Default values.

This establishes a direct product-level counterexample to the shortcut:

```text
reset clears current runtime state
        -> therefore repair policy is forgotten
```

For this drive, current policy can be volatile as an execution embodiment while its configured value is recoverable from retained Saved state.

## H/P — a successful `MODE SELECT` with `SP=1` creates a separate save-completion boundary

The 1991 manual says that with Save Mode Parameters (`SP`) set, the drive updates the current mode values, saves the current values of savable parameters, and returns Good status only after that save operation completes. If the command detects an error, the saved values are not changed.

This produces a useful historical transaction boundary:

```text
request new repair policy
        -> update Current value
        -> save savable parameter state
        -> Good status after save completes
```

The documentation does **not** justify treating that command as an arbitrary power-fail-atomic transaction across every internal medium/controller state. It does show that the interface distinguishes runtime update from saved-policy materialization and makes completion conditional on the save path succeeding.

## H/P — the ST3283N's default policy is not evidence that the feature is absent

The Error Recovery Page lists:

```text
AWRE default = 0
ARRE default = 0
```

while marking the Error Recovery bits changeable and the page savable.

Therefore:

```text
default off
    != unsupported
```

and

```text
supported
    != enabled
```

This distinction matters for historical reconstruction because a later field observation of a disabled feature does not by itself establish that the hardware or firmware lacked the capability.

## H/P — `AWRE=1` and `ARRE=1` admit automatic replacement during ordinary I/O

For the ST3283N:

- `AWRE=1` causes the drive to automatically reallocate bad blocks detected during writes;
- `AWRE=0` suppresses automatic reallocation and returns Check Condition / Medium Error instead;
- `ARRE=1` enables automatic reallocation of bad blocks detected during reads;
- `ARRE=0` suppresses that automatic path and returns Check Condition / Medium Error.

The product appendix adds an implementation-level threshold for the read path: with ARRE enabled, read errors requiring more than three retries or ECC correction to recover are automatically reallocated. Unrecoverable sectors remain a separate case for which the initiator should use `REASSIGN BLOCKS`.

For writes, the same appendix says that when AWRE is enabled, a sector whose header cannot be recovered is automatically reallocated and the data field rewritten; when disabled, the initiator is expected to perform explicit reassignment and rewrite work.

Thus the product supports at least two repair loci:

```text
ordinary I/O + automatic policy
        -> device-local reassignment path

ordinary I/O + automatic policy disabled
        -> error surfaced to initiator
        -> host may invoke explicit REASSIGN BLOCKS
```

These are historically documented alternatives, not two names for one operation.

## H/P — automatic read reallocation still depends on successful data recovery

The ST3283N appendix distinguishes recovered read errors from unrecoverable sectors. The former may be automatically reallocated under ARRE; the latter still require explicit handling and do not become magically recoverable because a spare exists.

The 1994 ST43401N/ND / ST43402ND sense-code table independently exposes the same separation at the outcome level:

- recovered data with automatic reallocation;
- unrecovered read error with auto-reallocate failure.

Therefore the period product evidence supports:

```text
automatic-reallocation policy enabled
        !=
source payload recoverable
```

A replacement location cannot restore a value that the drive can no longer recover merely by virtue of being empty and spare.

## H/P — automatic write reallocation can preserve new write data even when the old sector embodiment is unusable

The ST3283N appendix documents an AWRE-enabled path in which a sector is automatically reallocated and the data field is rewritten after a header-recovery failure.

That path differs from an old-payload recovery problem. For a write, the command may already supply the value intended to become current. The drive can therefore redirect that value to a replacement embodiment if its documented recovery/reallocation conditions are satisfied.

This gives an important semantic distinction:

```text
read-side reallocation
    often depends on recovering the value already stored

write-side reallocation
    may have the intended new value available from the write operation
```

The exact internal buffering and crash windows are not reconstructed here.

## H/P — the Hawk 4 family makes the physical placement of policy state unusually explicit

The March 1996 ST15230W/WD/WC/DC manual states that the drive maintains four mode-parameter classes and identifies their embodiments:

```text
Default values   -> firmware in flash E-PROM on the PCB
Saved values     -> disk media
Current values   -> volatile memory, used to control operation
Changeable mask  -> nonvolatile memory
```

At power-up, Saved values are taken from media into Current volatile storage. Standard OEM drives have Saved values initialized from Default values before shipment.

This lets the case distinguish:

```text
repair-policy meaning
        !=
current volatile embodiment of that policy
        !=
nonvolatile source used to reconstruct it
```

The policy can therefore survive loss of one runtime embodiment without requiring the current RAM bits themselves to persist.

## H/P — the Hawk 4 SCSI-2 table independently shows error-recovery policy as both defaulted and changeable

For the ST15230W/WD/WC/DC SCSI-2 implementation, Table 11.3.2-2 lists Error Recovery Page `01h` with a default byte 2 of `00h` and a change mask byte 2 of `EFh`.

Under the documented Error Recovery Page layout, that means the automatic reallocation bits are initially clear while the corresponding policy bits are among the initiator-changeable controls.

This is useful corroboration because it is a later named product family with an explicitly stated `Integrated SCSI Controller`, yet the same broad distinction remains visible:

```text
controller-integrated capability
        !=
current repair-admission setting
```

The evidence does not establish that ST3283N and Hawk 4 share one controller silicon design or one firmware lineage.

## H/P — successful automatic repair is still bounded by finite spares and defect-list update success

The December 1994 ST43401N/ND / ST43402ND manual exposes separate outcomes for:

- successful write recovery with automatic reallocation;
- automatic write-reallocation failure;
- unrecovered read error with automatic-reallocation failure;
- recovered data that were auto-reallocated;
- no defect spare location available;
- defect-list update failure.

These outcome categories prevent a one-bit model in which `AWRE=1` or `ARRE=1` means “repair guaranteed.”

The more faithful relation is:

```text
automatic repair admitted
        + sufficient/recoverable value state
        + replacement location available
        + replacement / defect metadata update succeeds
        -> repair may close successfully
```

Each term is separately defeasible in the source set.

---

# Retained-state decomposition

This deepening adds a fifth state class to the original Case 14 decomposition.

## 1. Payload state

The value currently intended for an LBA.

On a read-side repair, this may need to be recovered from a marginal or defective old sector before relocation can preserve it.

On a write-side repair, the command path may already possess the new intended value.

## 2. Logical designation

The host-visible LBA remains the service designation even when its physical embodiment changes.

## 3. Defect / replacement metadata

The drive must retain which locations are defective and which replacement locations serve affected logical blocks.

## 4. Spare capacity

Unused replacement locations provide finite future repair capability.

## 5. Repair-policy state

`AWRE`, `ARRE`, and related error-recovery controls determine whether ordinary I/O is allowed to invoke an automatic reassignment path.

For the named products here, this policy itself has multiple embodiments:

```text
Default policy
Saved policy
Current policy
Changeability / authority mask
```

The product may therefore retain not only user data and defect mappings, but also **rules controlling whether future retention work is automatically attempted**.

That last sentence is engineering reconstruction, not period terminology.

---

# Engineering reconstruction

## E — capability, admission, execution, and closure are different relations

The source set supports the following decomposition:

```text
automatic-reallocation capability
    !=
configured admission policy (AWRE / ARRE)
    !=
triggering read/write error
    !=
automatic repair actually attempted
    !=
source value available / recoverable
    !=
spare embodiment available
    !=
defect-map update successful
    !=
repair closed successfully
```

A report that a drive “supports auto reallocation” establishes only the first relation unless more evidence is supplied.

## E — present payload correctness does not prove future repair policy is usable

A disk can still read all currently requested data while its repair policy is disabled or incorrectly configured.

Conversely, an enabled policy can exist while no current defect requires action.

Therefore:

```text
payload presently readable
    !=
future repair admission configured
```

This is the same general methodological distinction that appears in maintenance-control cases elsewhere in the repository, but the mechanism here is failure-triggered disk replacement rather than periodic refresh or scrub.

## E — reset can destroy the runtime embodiment without destroying the configured relation

The ST3283N and Hawk 4 mode-parameter semantics show a recoverable relation:

```text
Saved nonvolatile policy
        -> reset / power-up
        -> reconstructed Current volatile policy
```

Thus:

```text
current volatile control bits lost
    !=
repair policy forgotten
```

provided that the retained Saved/default source remains valid and retrievable.

The evidence does not establish the exact crash-consistency protocol by which those saved parameters are internally updated.

## E — `spare exists` and `repair may run` are independent dimensions

Finite spare capacity is one prerequisite for reassignment. AWRE/ARRE are a separate admission relation.

So:

```text
spare capacity > 0
    !=
automatic repair enabled
```

and

```text
automatic repair enabled
    !=
spare capacity > 0
```

This becomes important near exhaustion: an enabled policy can still fail because replacement material is gone.

## E — repair location and value continuity remain separate

The original Case 14 already established that explicit `REASSIGN BLOCKS` does not itself preserve the old payload.

The automatic path sharpens rather than removes that distinction. A read-side automatic relocation can preserve the value only when the drive recovers it sufficiently to place it in the replacement block. A failed recovery cannot be repaired merely by changing physical location.

Thus:

```text
replacement embodiment acquired
    !=
old payload recovered
```

## E — saved repair policy is itself retention infrastructure

For the Hawk 4 family, the product can reconstruct current error-recovery behavior from nonvolatile Saved/default state after reset.

The retained policy is not user payload, yet it can affect whether later media defects are absorbed locally or surfaced to the host.

That makes it a form of **retention-control state** in the project's vocabulary.

This is an engineering classification, not a Seagate historical term.

---

# Controlled functional comparisons

## A — Case 55 NVMe health telemetry

Case 55's `Available Spare` and spare-threshold warning are **health/resource observations**. AWRE/ARRE are **repair-admission controls**.

The useful comparison is:

```text
reserve health / warning
    !=
repair policy
```

Both can refer to a system whose future service depends on spare capacity, but the interfaces answer different questions.

No ATA/SCSI→NVMe genealogy is inferred from that functional comparison.

## A — Case 78 NAND bad-block replacement

Both cases expose finite hidden replacement capacity used to sustain a stable higher-level address service after physical defects.

But:

- the present case concerns magnetic-disk SCSI defect management and mode-page policy;
- Case 78 concerns NAND bad-block handling and reserved replacement blocks.

The shared function `replace failed embodiment while preserving higher-level service` does not make the media physics, metadata, command protocols, or historical lineages identical.

## A — Case 04 mapped Flash

Both can preserve a logical designation while changing physical location.

The difference remains decisive:

- mapped Flash commonly relocates state because ordinary update and erase geometry require out-of-place management;
- this disk slice is bounded to failure/error-triggered replacement and policy-controlled automatic repair.

The term `FTL` must not be back-projected onto the disk mechanism.

---

# Philosophical interpretation

## I — a system may retain rules for how it will try to retain later

The source set permits a narrow interpretive statement:

> a technical system can retain not only a current value and the mapping that makes that value addressable, but also a nonvolatile policy that governs whether later degradation will trigger local repair.

This should not be inflated into the slogan that a disk “remembers how to heal itself.” The policy is a documented mode parameter embedded in a concrete command/firmware architecture. It has finite authority, finite spare material, and failure modes.

The stronger technical lesson is simpler:

```text
retention of payload
    !=
retention of repair relation
    !=
retention of repair-admission policy
```

Those relations can support one another without becoming conceptually identical.

---

# Failure matrix

| Situation | Payload/value state | AWRE/ARRE policy | Spare / metadata state | Bounded consequence supported by sources |
| --- | --- | --- | --- | --- |
| marginal read, value recoverable, ARRE enabled | recovered | admitted | sufficient | drive may automatically reallocate recovered data |
| marginal read, value recoverable, ARRE disabled | recovered | not admitted | irrelevant to automatic path | error surfaced; initiator may use explicit reassignment |
| read unrecoverable | unavailable | even if admitted | spare may exist | automatic relocation cannot manufacture the lost value; explicit handling remains |
| write-site failure, intended write data available, AWRE enabled | new value available | admitted | sufficient | drive may redirect/rewrite through automatic reassignment |
| write-site failure, AWRE disabled | new value may be available | not admitted | spare may exist | automatic path suppressed; error/host repair path remains |
| automatic repair admitted but no spare location remains | value may be available | admitted | exhausted | repair can fail with no-spare condition |
| spare exists but defect metadata update fails | value may be available | admitted | update failed | replacement service may not close successfully |
| reset loses Current parameter embodiment | payload independent | Current volatile state lost | Saved/default retained | Current repair policy can be reconstructed from retained parameter state |

The table is an engineering reconstruction of documented relations. It is not a period state-machine diagram.

---

# Explicit non-claims

1. This packet does **not** claim that Seagate invented automatic bad-sector reassignment.
2. It does **not** claim that AWRE or ARRE first appeared in 1991.
3. It does **not** establish the first SCSI standard revision containing those bits.
4. It does **not** establish one direct design genealogy from ST3283N to Hawk 4.
5. It does **not** claim that the two products share the same controller silicon.
6. It does **not** infer undocumented internal firmware data structures from mode-page behavior.
7. It does **not** treat `default 0` as evidence that automatic reallocation was unsupported.
8. It does **not** treat `supported` as evidence that a customer actually enabled the feature.
9. It does **not** treat `AWRE=1` or `ARRE=1` as a guarantee that every defect will be repaired.
10. It does **not** treat spare capacity as evidence that the automatic policy is enabled.
11. It does **not** treat an enabled policy as evidence that spare capacity remains.
12. It does **not** treat successful reassignment as proof that the old payload had been recoverable before repair.
13. It does **not** claim that explicit `REASSIGN BLOCKS` and automatic reallocation preserve payload by the same path.
14. It does **not** claim that read-side and write-side automatic reallocation have identical value-availability preconditions.
15. It does **not** generalize the ST3283N retry threshold to all Seagate drives.
16. It does **not** generalize the Hawk 4 default/change mask to all SCSI products.
17. It does **not** equate a saved mode parameter with the currently executing volatile parameter embodiment.
18. It does **not** claim that every reset preserves every drive mode parameter.
19. It does **not** infer arbitrary sudden-power-loss atomicity for Mode Select saving from ordinary command-completion semantics.
20. It does **not** claim that Hawk 4 Saved values and user payload share identical media layout or protection.
21. It does **not** treat `No defect spare location available` as proof that every physical spare sector in the device is literally consumed; it is used only as the documented service-level failure condition.
22. It does **not** treat a defect-list update failure as equivalent to payload corruption.
23. It does **not** equate SCSI automatic reallocation with a Flash Translation Layer.
24. It does **not** equate AWRE/ARRE policy with NVMe SMART / Health telemetry.
25. It does **not** close empirical spare-exhaustion progression or fault-injection work.
26. It does **not** close broader HDD CHS→LBA, defect-management, or controller genealogy.
27. It does **not** claim that an automatic repair event is invisible to every host or diagnostic interface.
28. It does **not** infer fleet-wide reliability effects or failure probabilities from product-manual semantics.

---

# Claim ledger

| Claim | Type | Evidence strength |
| --- | --- | --- |
| ST3283N exposes AWRE and ARRE in Error Recovery Page 01h | H/P | strong: 1991 Seagate product manual |
| ST3283N ships with AWRE=0 and ARRE=0 in the documented default page | H/P | strong for named product |
| those controls are changeable by the initiator | H/P | strong for named product |
| Error Recovery Page is savable | H/P | strong for named product |
| Mode Select `SP=1` separates Current update from Saved-parameter materialization and returns Good after save completion | H/P | strong for named product |
| after reset Current mode state is reconstructed from Saved values when retrievable, otherwise Default | H/P | strong for named product |
| ARRE-enabled ST3283N automatically relocates certain recovered read errors | H/P | strong: product appendix |
| unrecoverable read sectors remain a distinct host-repair problem | H/P | strong: product appendix |
| AWRE-enabled ST3283N can automatically relocate and rewrite on the documented write/header failure path | H/P | strong: product appendix |
| 1994 named Seagate products distinguish successful auto reallocation, auto-reallocation failure, no-spare failure, and defect-list update failure | H/P | strong: product sense-code table |
| Hawk 4 has an integrated SCSI controller | H/P | strong: 1996 product manual |
| Hawk 4 Default values reside in flash E-PROM, Saved values on disk media, and Current values in volatile memory | H/P | strong: 1996 product manual |
| Hawk 4 Error Recovery Page default byte 2 is 00h and change mask is EFh | H/P | strong: Table 11.3.2-2 |
| repair capability != repair-admission policy | E | directly supported by default/changeable policy semantics |
| current volatile repair policy != retained saved/default source | E | directly supported by reset reconstruction semantics |
| automatic repair enabled != successful repair closure | E | directly supported by failure codes / spare boundaries |
| a technical system can retain policy state governing later retention work | I/E | bounded project interpretation |
| Seagate invented AWRE/ARRE or automatic reassignment | X | unsupported / rejected |
| all SCSI drives shared these defaults and internal implementations | X | unsupported / rejected |

---

# Related-repository routing

Before writing this packet, `tmzncty/computing-archaeology` was searched for combinations including:

- `ST15230 AWRE ARRE automatic reallocation`;
- `SCSI bad sector remap defect reallocation`.

No dedicated overlapping packet was returned.

That is only a routing check. The broad history of SCSI defect-management standardization, HDD controller silicon, CHS/LBA evolution, format-time slipping, grown-defect-list implementation, and vendor competition still belongs primarily in `computing-archaeology` if pursued.

`technical-retention` keeps the narrower relation:

```text
retained repair policy
    + recoverable/current value
    + spare embodiment
    + current defect metadata
    -> possible continuation of the same logical-block service
```

---

# Bounded conclusion

The new evidence closes one previously weak part of the roadmap without pretending to close the whole defect-management history.

By 1991, one named Seagate SCSI drive documented **automatic read/write reallocation as a configurable, savable error-recovery policy** rather than as an inevitable side effect of having spare sectors. Its current control values were reconstructable after reset from retained Saved/default state. The 1994 named-product sense codes independently expose successful and failed auto-reallocation outcomes, spare exhaustion, and defect-list update failure. The 1996 Hawk 4 family then makes the policy-storage split explicit across firmware flash, disk-resident Saved values, volatile Current values, and nonvolatile change masks.

The strongest bounded reconstruction is therefore:

```text
repair capability
    != repair-admission policy
    != current volatile policy embodiment
    != source-value recoverability
    != replacement capacity
    != metadata-update success
    != repair closure
```

This packet does **not** supply empirical spare-exhaustion curves, controller-silicon archaeology, sudden-power-loss fault injection, or a full HDD→NAND→SSD defect-management genealogy. Those remain separate work.