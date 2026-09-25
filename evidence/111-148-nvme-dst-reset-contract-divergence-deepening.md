# Case 111 / Case 148 — NVMe Device Self-test reset-contract divergence

**Status:** bounded cross-case deepening complete. Case 111 and Case 148 remain `grounded`.

**Primary anchor:** Case 111 Host-Initiated Refresh (HIR).  
**Comparator:** Case 148 NVMe Device Self-test reset-surviving maintenance.

## Bounded question

NVMe uses one Device Self-test command family and one Device Self-test log surface for several long-running operations. Does that shared framework imply one shared persistence horizon across Controller Level Reset or power interruption?

The checked specifications say **no**.

This slice compares only the public interruption contracts. It does not reconstruct controller firmware, checkpoint layout, or NAND-refresh implementation, and it does not claim that later HIR was historically derived from the earlier extended-test resume rule.

## Historical / normative record

### NVMe 1.3 short Device Self-test — reset aborts the operation

NVM Express Revision 1.3, ratified 26-Apr-2017, §8.11.1 says a short Device Self-test reports percentage complete through the Device Self-test Log and **shall be aborted by any Controller Level Reset**.

```text
short Device Self-test in progress
    -> Controller Level Reset
    -> operation aborted
```

Source: NVM Express, *NVM Express Revision 1.3*:  
https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf

### NVMe 1.3 extended Device Self-test — reset/power restoration preserve operation continuity

The adjacent §8.11.2 gives a deliberately different contract. The extended Device Self-test also exposes percentage complete, but it **shall persist across any Controller Level Reset** and **shall resume after completion of the reset or any restoration of power**. The exact segment at which it resumes is vendor specific; the specification says implementations should only have to repeat tests within the last segment that was active before reset.

```text
extended Device Self-test in progress
    -> Controller Level Reset / restoration of power
    -> operation persists
    -> resumes
```

This is an operation-level continuation requirement. It does not disclose whether a controller stores an exact byte/LBA cursor, a coarser segment checkpoint, or reconstructs sufficient state in another way.

### NVMe 2.1 HIR — reset affecting the performing controller is an abort boundary

NVM Express Base Specification Revision 2.1, ratified 5-Aug-2024, adds Host-Initiated Refresh through Device Self-test (`STC=3h`). HIR is an implementation-specific media-refresh operation; it exposes current percentage complete in the Device Self-test log and applies to all media in the NVM subsystem.

Its reset contract differs from extended Device Self-test:

- HIR shall be aborted if a Controller Level Reset affects the controller on which HIR is being performed;
- a Controller Level Reset on a controller that is not performing HIR shall not impact that HIR operation.

```text
HIR in progress on controller C
    -> Controller Level Reset affecting C
    -> HIR aborted

HIR in progress on controller C
    -> Controller Level Reset affecting another controller
    -> HIR not impacted by that reset
```

Source: NVM Express, *NVM Express Base Specification, Revision 2.1*:  
https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.1-2024.08.05-Ratified.pdf

### UNH-IOL 2025 makes the HIR abort/result transition observable

UNH-IOL's *NVM Command Set Conformance Test Suite v24.0* (1-Aug-2025, Base Specification 2.2) tests the HIR reset rule directly. The procedure starts HIR with `STC=3h`, performs a Controller Level Reset, polls the Device Self-test Log until the operation is no longer running, then requires:

- result status `2h`, aborted by Controller Level Reset;
- a new Newest Self-test Result Data Structure;
- current Device Self-test status `0h`.

```text
live HIR progress
    -> reset affecting performing controller
    -> terminal abort result
    -> newest result entry
    -> idle
```

That is a terminalization trace at the public interface, not a resume trace.

Source: UNH-IOL, *NVM Command Set Conformance Test Suite v24.0*:  
https://www.iol.unh.edu/sites/default/files/testsuites/nvme/v24/UNH-IOL_NVM_Command_Set_Conformance_v24.0_2025.08.01.pdf

## Engineering reconstruction

### Same command family can carry several persistence contracts

The source record supports this project-level decomposition:

```text
Device Self-test command family
    |
    +-- short DST
    |      reset -> abort
    |
    +-- extended DST
    |      reset/power restoration -> persist and resume
    |
    +-- HIR
           performing-controller reset -> abort + terminal result
```

Therefore:

```text
same command family
    != same interruption contract
```

A useful project term is **operation-coded persistence contract**: the required persistence horizon belongs to the specific operation semantics, not merely to the enclosing command opcode or log page. This is repository vocabulary, not NVM Express historical terminology.

### Same progress surface does not imply the same progress persistence horizon

Extended Device Self-test and HIR both expose percentage-complete information through the Device Self-test log.

But:

```text
extended DST percentage
    + reset
    -> operation-level continuation required

HIR percentage
    + reset affecting performing controller
    -> episode terminalized as aborted
```

Thus:

```text
same style of live progress field
    != same restartability
    != same checkpoint contract
```

A progress percentage is evidence about work reported during the current operation. It is not by itself a promise that the progress coordinate survives reset as restart authority.

### Interruption semantics depend on operation identity and controller affinity

HIR also blocks a generic equation `reset anywhere = maintenance abort`. The public rule distinguishes a reset affecting the controller that performs HIR from a reset on another controller.

Project-level relation:

```text
interruption event
    + operation identity
    + affected-controller relation
    -> continuation / abort semantics
```

Controller affinity is therefore part of the public HIR persistence contract.

### Terminal outcome retention is not continuation-state retention

HIR's reset path produces a terminal result record. Extended Device Self-test's reset path requires continued operation.

```text
retain enough state to continue unfinished work
    !=
retain an outcome record that unfinished work was aborted
```

The first preserves an unfinished obligation across interruption. The second preserves evidence about the termination of that obligation.

### Extended-test power continuity cannot be projected onto HIR

Case 148's extended-test contract explicitly includes restoration of power. The checked HIR material instead establishes reset-triggered abort semantics for the performing controller.

Therefore:

```text
extended DST survives reset/power restoration
    != HIR survives reset/power restoration
```

Do not import the extended-test persistence contract into HIR merely because both use Device Self-test.

## Historical chronology and anti-anachronism

```text
2017 NVMe 1.3
    short DST: reset-abort
    extended DST: reset/power-restoration resume

2024 NVMe 2.1
    HIR added as another Device Self-test operation
    HIR: performing-controller reset-abort
```

Safe historical statement:

> NVMe's Device Self-test framework contains operation-specific interruption semantics, and later HIR was standardized with a reset-abort contract rather than inheriting the extended-test resume contract.

Unsafe claim:

> HIR designers intentionally rejected the earlier extended-DST checkpoint mechanism for a known architectural or philosophical reason.

The inspected specifications establish behavior, not committee motivation or internal implementation genealogy.

## Functional comparison

### Case 148 — extended Device Self-test

Case 148 remains the repository's strong NVMe example of a long-running maintenance/diagnostic obligation normatively required to survive Controller Level Reset and restoration of power. Its named Lexar/ULINK witness strengthens conformance evidence for reset scenarios but does not expose the hidden checkpoint embodiment.

### Case 111 — Host-Initiated Refresh

HIR is the complementary counterexample inside the same broad protocol framework:

```text
same command/log family
    + another long-running media operation
    + live percentage complete
    -> reset terminalization instead of resume
```

This is a functional comparison, not a claim of identical firmware machinery or direct implementation reuse.

### Synthesis 26 — maintenance-control persistence horizons

This pair sharpens the existing rule:

```text
same transition
    != same persistence horizon for every maintenance-control state
```

with a protocol-local version:

```text
same command family
    != same persistence horizon for every operation
```

No universal taxonomy is inferred from one protocol family.

## Philosophical interpretation — bounded

The exact technical fact is that the public identity of "the operation" does not survive interruption uniformly. The protocol specifies which relation must continue:

- extended DST preserves **unfinished-task continuity**;
- HIR reset handling preserves **termination evidence** instead.

A narrow interpretation follows:

> Continuity is defined by the proposition the interface chooses to preserve, not merely by the persistence of one internal representation.

This does not imply that all technical identity is contractual or that physical continuity is irrelevant. It is only a bounded reading of these two NVMe operation contracts.

## Anti-collapse rules

```text
Device Self-test support
    != one reset-survival rule

Current Percentage Complete
    != restartable progress checkpoint

long-running operation
    != reset-surviving operation

same Device Self-test log
    != same persistence horizon

extended DST reset resume
    != HIR reset resume

HIR abort result retained
    != HIR work state retained

operation-level continuation
    != exact internal cursor preservation

Controller Level Reset
    != one global semantic effect across all Device Self-test modes

reset on non-performing controller
    != reset affecting the controller performing HIR
```

## What this changes

This closes one bounded cross-case question:

> Can a shared NVMe maintenance/diagnostic command-and-log framework be treated as evidence of one shared restart-persistence model?

**No.** The standards themselves supply a counterexample.

It does not close Case-111 P1: a named shipping HIR implementation and real HIR success/reset trace remain open. It also does not close Case-148's implementation question: the hidden embodiment or reconstitution method for extended-DST resume state remains undisclosed.

## Related-repository boundary

Fresh searches of `tmzncty/computing-archaeology` for `Device Self-test reset Host-Initiated Refresh`, `NVMe extended self-test reset`, and `Host-Initiated Refresh TP4058` found no dedicated reusable packet.

Broad Device Self-test command genealogy, TP001a/TP4058 committee history, firmware checkpoint design, and vendor implementation archaeology remain companion-repository work. This repository keeps only the retention-specific interruption-contract comparison.

## Sources

1. NVM Express, *NVM Express Revision 1.3*, ratified 26-Apr-2017, §§8.11.1–8.11.2: https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf
2. NVM Express, *NVM Express Base Specification, Revision 2.1*, ratified 5-Aug-2024, Host-Initiated Refresh operation: https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.1-2024.08.05-Ratified.pdf
3. University of New Hampshire InterOperability Laboratory, *NVM Command Set Conformance Test Suite v24.0*, 1-Aug-2025, Test 1.26: https://www.iol.unh.edu/sites/default/files/testsuites/nvme/v24/UNH-IOL_NVM_Command_Set_Conformance_v24.0_2025.08.01.pdf
4. Repository comparator: [Case 148 ULINK / Lexar Device Self-test controller-reset conformance](148-ulink-2026-lexar-dst-controller-reset-conformance-deepening.md).
