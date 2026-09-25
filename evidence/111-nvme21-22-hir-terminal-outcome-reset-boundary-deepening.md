# Case 111 — NVMe 2.1/2.2 HIR terminal-outcome and reset boundary

**Status:** Case 111 remains `grounded`.

## Scope

The previous Host-Initiated Refresh (HIR) slice established a standards-level refresh-specific interface: recommended interval (`RHIRI`), nominal duration (`HIRT`), all-media operation scope, and current percentage complete.

This slice asks a narrower question:

> When a HIR episode ends, what public evidence distinguishes command acceptance, work in progress, successful/aborted termination, and restartable maintenance state?

The answer matters because a background refresh command may complete at the command-queue level before the refresh operation itself has ended.

## Historical / source record

### NVM Express 2.1 — command completion is not HIR completion

NVM Express Base Specification Revision 2.1, ratified 5 August 2024, added HIR through TP4058 / Environmental Extremes Management.

Its Device Self-test command-processing table assigns `STC=3h` to Host-Initiated Refresh. For that command, the controller validates parameters, marks the current Device Self-test state as HIR, starts the HIR operation, and then completes the command successfully.

This ordering is important:

```text
Device Self-test command accepted
    -> HIR current-operation state established
    -> HIR background operation started
    -> command completion posted
```

The completion queue entry therefore reports completion of the command submission path, not completion of the background HIR episode.

Revision 2.1's Device Self-test log distinguishes current-operation/progress state from a rolling history of completed or aborted Device Self-test results. HIR is identified by Self-test Code `3h` in the result structure.

### NVM Express 2.2 / UNH-IOL 2025 — terminalization is separately observable

NVM Express Base Specification Revision 2.2, ratified 11 March 2025, retains the Device Self-test result model. Its result-status vocabulary distinguishes successful completion from several abort/error outcomes.

UNH-IOL's **NVM Command Set Conformance Test Suite v24.0**, last updated 1 August 2025 and targeting Base Specification 2.2, gives a concrete HIR conformance procedure.

For `STC=3h` it explicitly warns that command completion may arrive before the background HIR operation finishes. The host repeatedly reads Device Self-test Log page `06h` until the log says the operation is no longer in progress. While HIR is running, the current Device Self-test status is `3h`; after the episode ends, the current-operation field returns to `0h`.

The same HIR test checks several terminal-abort paths:

```text
Controller Level Reset
    -> HIR result: aborted by Controller Level Reset (2h)
    -> newest Self-test Result entry added
    -> current operation becomes 0h

Sanitize
    -> HIR result: aborted due to Sanitize (9h)

Format NVM
    -> HIR result: aborted by Format NVM (4h)

Device Self-test abort command (STC=Fh)
    -> HIR result: aborted by Device Self-test command (1h)
```

For the Controller Level Reset case, UNH-IOL explicitly compares the log before and after reset and requires a **new Newest Self-test Result Data Structure** after the aborted HIR episode.

## Engineering reconstruction

The source relations support the following project-level decomposition:

```text
command acceptance
    != maintenance operation completion

current-operation state
    != terminal outcome record

percentage complete
    != terminal success

terminal outcome record
    != restartable work checkpoint

aborted episode recorded
    != refresh coverage complete
```

These labels are engineering reconstruction, not NVM Express historical vocabulary.

### Maintenance-episode terminalization

A useful project term for this relation is **maintenance-episode terminalization**:

```text
background maintenance episode
    -> reaches success / abort / error end
    -> terminal result record becomes newest history entry
    -> current-operation state becomes idle
```

The public interface preserves an outcome of the episode without exposing or preserving every internal step that produced that outcome.

### Reset is a termination boundary, not a demonstrated resume boundary

The Controller Level Reset conformance case is especially important for Case 111.

The observable contract is:

```text
HIR in progress
    -> Controller Level Reset
    -> HIR terminal result = aborted
    -> new result entry
    -> no HIR currently in progress
```

Therefore:

```text
pre-reset percentage / internal scan position
    != demonstrated restart checkpoint
```

Nothing in this source establishes that a later HIR resumes from the exact internal position reached before reset.

This closes a bounded part of the previous debt: **current HIR progress must not be treated as restart-persistent maintenance-control state merely because the device exposes a percentage.**

### Rolling history is not permanent provenance

The Device Self-test log retains a bounded rolling set of recent results (20 entries in Revision 2.1), with the newest completed or aborted operation at the head.

Thus:

```text
terminal result retained in log
    != indefinite maintenance provenance

result history
    != exact internal refresh trajectory

newest terminal result
    != future offline-retention guarantee
```

The result record is evidence about the defined maintenance episode. It is not a certificate that every NAND page was rewritten, that the media will meet an arbitrary future shelf-life requirement, or that all internal maintenance classes are complete.

## What this changes in Case 111

The standards-level HIR evidence can now be split more precisely:

```text
RHIRI
    -> recommended scheduling horizon

HIRT
    -> nominal operation duration

Current Percentage Complete
    -> live progress evidence while HIR is active

Device Self-test Result
    -> terminal outcome evidence for a completed/aborted episode

rolling 20-result log
    -> bounded episode history
```

This makes HIR a stronger public completion surface than the generic-BKOPS product evidence currently available in Case 111.

It still does **not** close the highest-value product-level debt. A standardized capability and conformance procedure are not evidence that a particular shipping SSD implements HIR.

## Functional comparison

### eMMC BKOPS

Functional comparison only:

```text
generic eMMC BKOPS status / completion
    != HIR refresh-specific progress and result semantics
```

The comparison is about observability structure. It does not imply JEDEC-to-NVMe genealogy, common firmware, or identical maintenance algorithms.

### IBM ESS scrub completion

The IBM ESS case and NVMe HIR both expose named maintenance completion at a public boundary, but at different layers:

```text
system-level vdisk scrub completion
    != device-level HIR terminal result
```

Neither should be used as proof that every lower-layer or higher-layer maintenance obligation has completed.

## Philosophical interpretation

A narrow interpretation survives the mechanism:

> Technical completion is relative to an interface-defined episode.

The system can retain a public statement that a maintenance episode ended successfully or was aborted while leaving the controller's internal refresh trajectory opaque. What survives is not necessarily the whole history of the work, but a bounded relation between an operation identity and an outcome.

This is a project interpretation, not NVM Express or UNH-IOL terminology.

## Anti-collapse rules

```text
Device Self-test command Successful Completion
    != HIR operation completed

HIR progress percentage
    != HIR terminal success

current-operation = 0h
    != previous HIR necessarily succeeded

abort result
    != refresh coverage completion

Controller Level Reset
    -> HIR abort in the tested contract
    != exact-progress resume

newest result record
    != permanent maintenance history

successful HIR episode
    != future offline-retention guarantee

standards-defined HIR
    != named-product adoption
```

## Related-repository boundary

Fresh searches of `tmzncty/computing-archaeology` for `Host-Initiated Refresh`, `TP4058`, and `Device Self-test refresh` found no dedicated packet to reuse.

Broad NVMe Device Self-test genealogy, TP proposal history, controller implementation history, and product-adoption archaeology belong there if pursued. Case 111 keeps the retention-specific distinction among scheduling, progress, terminal outcome, restart behavior, and future-offline admission.

## Remaining debt

1. Find a first-party **named shipping SSD/NVMe product** that advertises HIR support and exposes `RHIRI`, `HIRT`, progress, or terminal results.
2. On such a named product, capture a real HIR trace through success and at least one interruption/reset path.
3. Determine whether any vendor exposes finer-grained refresh coverage or resume state beyond the standardized Device Self-test result surface.
4. Keep HIR episode completion separate from future offline-retention qualification.

## Primary / institutional sources

- NVM Express, *NVM Express Base Specification, Revision 2.1*, ratified 5 August 2024: https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.1-2024.08.05-Ratified.pdf
- NVM Express, *NVM Express Base Specification, Revision 2.2*, ratified 11 March 2025: https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.2-2025.03.11-Ratified-1.pdf
- University of New Hampshire InterOperability Laboratory, *NVM Command Set Conformance Test Suite*, Version 24.0, last updated 1 August 2025, Test 1.26 — Device Self-test Host-Initiated Refresh Operation: https://www.iol.unh.edu/sites/default/files/testsuites/nvme/v24/UNH-IOL_NVM_Command_Set_Conformance_v24.0_2025.08.01.pdf
