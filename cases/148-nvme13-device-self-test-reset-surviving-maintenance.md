# NVM Express 1.3 Device Self-test: Reset-Surviving Diagnostic Work, Resume State, and Bounded Result History

## Status

**`grounded`** — bounded to NVM Express Revision 1.3, ratified 26-Apr-2017 and dated 1-May-2017, with the NVM Express revision-changes page used to establish that Device Self-Test was a new optional NVMe 1.3 feature. A 2005 T10 SAT proposal is used only as earlier ATA/SCSI self-test prior-art evidence; NVMe is not treated as the inventor of storage-device self-test. Later NVMe 1.4 changes are used only as anti-anachronism and bounded evolution evidence.

Evidence navigation:

- grounding: [`../evidence/148-nvme13-2017-device-self-test-reset-resume-grounding.md`](../evidence/148-nvme13-2017-device-self-test-reset-resume-grounding.md)
- subsystem/sanitize/product deepening: [`../evidence/148-2017-2021-dst-subsystem-sanitize-product-deepening.md`](../evidence/148-2017-2021-dst-subsystem-sanitize-product-deepening.md)

## Scope

- **Object / system:** NVMe 1.3 Device Self-test command, Device Self-test Log, and short/extended self-test operation semantics.
- **Date anchor:** NVMe 1.3 ratified 26-Apr-2017; specification dated 1-May-2017.
- **Retention question:** what non-payload state must remain authoritative when an extended diagnostic operation crosses controller reset or power restoration, and how is that current work distinguished from the bounded history of completed/aborted tests?

The bounded mechanism is:

```text
Device Self-test command accepted
    -> current self-test operation becomes active
    -> command itself completes
    -> background diagnostic work continues
       -> may suspend/resume around foreground commands
       -> short test: reset aborts
       -> extended test: reset/power restoration resumes work
    -> completion or abort creates a result record
    -> current-operation field then returns to no-operation
    -> up to 20 newest results remain addressable in the log
```

The later deepening adds a second axis that was already present in NVMe 1.3 and a conflict boundary made explicit in NVMe 1.4:

```text
current self-test relation
    + DSTO[0]
        -> exclusion domain may be controller-local or subsystem-wide

extended self-test survives reset/power restoration
    != survives every later administrative transition

NVMe 1.4 sanitize start
    -> abort in-progress DST across the NVM subsystem
    -> retain bounded abort evidence with result code 9h
```

This is **not**:

- a general history of SMART, SCSI SEND DIAGNOSTIC, ATA self-test, or storage diagnostics;
- a claim that NVMe invented short/extended drive self-tests or self-test result logs;
- proof that every NVMe 1.3 device implements Device Self-test, which is optional;
- proof that a resumed extended test preserves an exact internal program counter, NAND address, analog state, or block-by-block checkpoint;
- proof that the last-20 result history has the same cross-power persistence contract as the in-progress extended operation;
- proof that subsystem-wide self-test exclusion implies a consensus protocol or one physical storage location for the current-operation state;
- proof that successful self-test establishes complete media integrity, archival fitness, or secure erasure;
- evidence that diagnostic-operation continuity is equivalent to host-write power-loss protection.

---

## Historical vocabulary and chronology

NVM Express Revision 1.3 is dated **1 May 2017** and states that Revision 1.3 was ratified on **26 April 2017**. The NVM Express revision-changes page lists **Device Self-Test (optional)** under the new features in Revision 1.3, describing one self-test command for short and long operations and pointing to Technical Proposal `001a`.

That is an NVMe-family chronology, not a global invention claim.

Earlier self-test traditions are directly visible in T10 document `05-245r1`, dated **7 November 2005**. That SCSI/ATA Translation proposal maps SCSI background short/extended self-test functions to ATA `SMART EXECUTE OFF-LINE IMMEDIATE` short and extended self-test routines and discusses a Self-Test Results log page. Therefore:

> **new to NVMe 1.3 != first storage-device self-test mechanism**.

The exact genealogy from ATA/SCSI traditions to NVMe Technical Proposal 001a remains open; functional similarity and earlier chronology do not establish direct lineage.

A later, separately bounded change matters for anti-anachronism. NVM Express's official Revision 1.4 changes page classifies **Sanitize during Device Self-Test** as a mandatory/incompatible change and attributes it to Technical Proposal `4022`. That later rule cannot be projected backward into the original 2017 abort list.

---

## Historical record

### The command starts background work and then completes

NVMe 1.3 §5.8 defines short, extended, vendor-specific, and abort Device Self-test command actions. Figure 68 specifies the start path in a revealing order: validate command parameters, set the current self-test status, start the self-test operation, and then complete the command successfully.

Therefore:

> **Device Self-test command completion != device self-test operation completion**.

The command creates/changes control state and launches longer-lived work; its completion entry does not mean the diagnostic has finished.

### Self-test is explicitly background maintenance that may be suspended and resumed

Section 8.11 says a device self-test runs in the background. Some commands may execute concurrently; other commands require the controller to suspend the self-test, process and complete the foreground command, and then resume the self-test. Which commands fall into each category is vendor specific.

Thus:

> **temporary suspension != abort**

and

> **foreground command completion can coexist with an unfinished diagnostic obligation**.

The operation can be temporally interrupted while remaining the current self-test.

### Short and extended tests have deliberately different reset horizons

Section 8.11.1 says a short self-test **shall be aborted by any Controller Level Reset**.

Section 8.11.2 gives the extended operation a stronger continuity contract: it **shall persist across any Controller Level Reset** and resume after completion of the reset or after restoration of power, if power was lost.

This creates one of the cleanest maintenance-state contrasts in the repository:

> **same command family != same interruption-survival horizon**.

A reset is an abort cause for short work and a continuation boundary for extended work.

### Resume continuity is not exact microstate preservation

NVMe 1.3 does not require an exact restart instruction/address. Section 8.11.2 says the segment at which an extended self-test resumes is **vendor specific**, while recommending that an implementation should only need to redo tests within the last segment that had been under test before reset.

Therefore:

> **operation identity/obligation survives != every internal execution detail survives unchanged**.

The standard requires continuity of the extended self-test relation while leaving checkpoint granularity and restart implementation partly open.

The Current Percentage Complete field likewise reports progress but does not normatively expose an exact durable physical restart position.

> **reported percentage != demonstrated byte/block-exact durable checkpoint**.

### Current self-test authority may be controller-local or subsystem-wide

NVMe 1.3 already includes the Identify Controller **Device Self-test Options (`DSTO`)** field. Bit 0 distinguishes two concurrency domains:

- cleared to `0`: the NVM subsystem supports one Device Self-test operation **per controller** at a time;
- set to `1`: the NVM subsystem supports **only one Device Self-test operation in progress for the NVM subsystem**.

Figure 68 uses the same distinction when interpreting whether a new Device Self-test command encounters a test already in progress.

Therefore:

> **current maintenance operation != scope in which that operation excludes another maintenance operation**.

The externally visible authority/concurrency relation may span the subsystem even though the specification does not disclose one mandatory physical embodiment for that state.

### Current operation and retained outcomes are different state classes

The Device Self-test Log (Log Identifier `06h`) contains:

- current self-test operation;
- current percentage complete; and
- results of the **last 20** completed or aborted self-test operations.

The newest result structure is the most recently completed/aborted operation, followed by older results.

This yields:

> **current maintenance execution state != retained maintenance-result history**.

and

> **last-20 result history != complete device diagnostic history**.

The log is explicitly bounded by count.

### Result evidence is created before current status is cleared

Figure 98 requires that if a current short/extended self-test completes or is aborted, the controller creates a new Self-test Result Data Structure **before** setting Current Device Self-test Operation to `0h`. Figure 68 gives the same order for an explicit abort: abort the operation, create the newest result entry, set current status to zero, then complete the abort command.

So the transition is not simply `running -> absent`:

```text
current work
    -> completion/abort outcome
    -> result evidence created
    -> current-work status cleared
```

Therefore:

> **operation retirement != outcome evidence discarded at the same transition**.

This does not prove indefinite or cross-power retention of the entire 20-entry history; it establishes the ordering and bounded history relation exposed by the 1.3 interface.

### Abort and failure are not synonyms

Figure 99 distinguishes outcomes including:

- completed without error;
- aborted by a Device Self-test command;
- aborted by Controller Level Reset;
- aborted due to namespace removal;
- aborted due to Format NVM;
- fatal/unknown test error before completion;
- completed with failed segment(s);
- aborted for unknown reason.

Thus:

> **aborted != diagnostic failure**

and

> **diagnostic failure != operation failed to complete**.

The result history preserves why a test ceased or what it found, rather than collapsing every non-success path into one bit.

### NVMe 1.4 adds subsystem-wide sanitize-driven retirement

The original NVMe 1.3 Sanitize operation is already subsystem-wide, but the inspected 2017 Device Self-test abort rules do not yet say that sanitize start must abort the self-test, and result code `9h` is reserved.

NVM Express explicitly identifies this as a later mandatory change in Revision 1.4. Revision 1.4c requires that when a sanitize operation starts on any controller, all controllers in the NVM subsystem abort Device Self-test operations in progress. Its Device Self-test result table adds:

```text
9h = Operation was aborted due to a sanitize operation
```

For an extended self-test this creates a precise hierarchy:

```text
Controller Level Reset / power restoration
    -> preserve and resume current extended-test obligation

Sanitize start
    -> terminate that obligation across the subsystem
    -> retain bounded historical evidence of sanitize-driven abort
```

Therefore:

> **reset-surviving maintenance state != maintenance state immune to stronger conflicting subsystem transitions**.

This is later evolution evidence, not a retroactive description of every NVMe 1.3 implementation.

### Result records are compressed diagnostic evidence, not payload copies

A result structure can carry Power On Hours at completion/abort and, when valid, a failing namespace/LBA plus status information. If multiple logical blocks fail, the Failing LBA field reports only one of them.

Therefore:

> **self-test result record != complete media-error history**.

and

> **self-test result record != user payload replica**.

A result preserves selected evidence about maintenance and faults, not the data being tested.

### Named commercial witness: Intel SSD D7-P5510

Intel's December-2020 D7-P5510 product brief identifies the drive as PCIe 4.0 x4, **NVMe 1.3c**, and explicitly advertises **Device self-test**. It says the host can request tests including SMART check, volatile-memory backup, NVM integrity, and drive-life checks.

This establishes a narrow product-level fact:

> **Device Self-test existed in a named commercial NVMe 1.3c enterprise SSD family, not only in the paper standard**.

It does **not** establish how a particular D7-P5510 firmware revision persisted extended-test resume state across reset/power loss, nor does the product brief constitute fault-injection testing. The listed diagnostic examples must not be rewritten as proof that firmware executes the informative standard example exactly.

---

## Retained state

The bounded case contains at least seven state classes:

1. **user payload / NVM state** — data whose integrity may be sampled or checked, but not copied into the control state simply by running self-test;
2. **current operation identity/status** — none, short, extended, or vendor-specific;
3. **progress/resume state** — enough state for an extended operation to remain the same outstanding diagnostic across reset/power restoration, with vendor-specific resume segment;
4. **maintenance authority / exclusion domain** — whether an in-progress self-test excludes another test only on the receiving controller or across the NVM subsystem (`DSTO[0]`);
5. **result history** — the newest 20 completed/aborted result structures;
6. **termination-cause evidence** — the result code distinguishing reset, Format, explicit abort, later sanitize-driven abort, and other outcomes;
7. **diagnostic detail validity** — per-result validity bits for namespace, failing LBA, and status fields.

These lifetimes and authorities are not interchangeable.

In particular:

> **cross-power operation continuity != proof of cross-power persistence for every diagnostic field or every internal test variable**.

And:

> **subsystem-wide authority relation != proof of one shared physical state object**.

---

## Physical / logical substrate

The specification defines an interface contract, not a required physical representation for self-test resume state. The device may embody that control state in controller nonvolatile storage, flash metadata, another persistent structure, or some implementation-specific reconstruction sufficient to meet the required behavior.

The same caution applies to the subsystem-wide `DSTO` case: the standard constrains externally visible concurrency behavior without requiring this repository to invent a controller-to-controller state-sharing mechanism.

Accordingly, this case grounds **contractual persistence and authority of the extended operation relation**, not a specific transistor/register layout.

This is an important stop condition:

> **required behavior != disclosed embodiment**.

---

## Addressing and access geometry

The Device Self-test command can target:

- controller-only testing (`NSID=0h`);
- one active namespace;
- or all active namespaces accessible through the controller (`FFFFFFFFh`).

The result format can conditionally name a failing namespace/LBA. That makes diagnostic scope and failure location explicit without turning the log into a map of every physical block tested.

This target scope must not be conflated with `DSTO` concurrency scope:

> **what the test covers != where another simultaneous test is excluded**.

The informative example in §8.11 includes RAM, SMART, volatile-memory backup, metadata, NVM integrity, data-integrity housekeeping, media check, and drive-life segments. Because that figure is informative, these examples must not be rewritten as a mandatory universal implementation sequence. The D7-P5510 product brief naming several similar diagnostic functions is a product-feature witness, not proof of exact segment implementation or ordering.

---

## Time

Several time relations coexist:

- short self-test should complete in two minutes or less;
- extended self-test should complete within the time reported by the controller;
- current percentage complete tracks the active operation;
- foreground commands may temporarily suspend background self-test;
- short work ends at Controller Level Reset;
- extended work crosses Controller Level Reset and power restoration;
- later NVMe 1.4 sanitize start deliberately terminates in-progress self-test work rather than preserving it;
- completed/aborted results enter a bounded newest-20 history;
- result Power On Hours records the device's power-on-hour count at the termination event.

These are different clocks/horizons. A lifetime of one field cannot be inferred from another merely because they share one log page.

---

## Maintenance and invisible work

Device Self-test makes maintenance itself a retained technical relation. The controller or subsystem must potentially:

- schedule diagnostic segments around ordinary commands;
- suspend and resume work;
- preserve or reconstruct enough extended-test state across reset/power restoration;
- track current progress;
- enforce controller-local or subsystem-wide self-test exclusion according to `DSTO`;
- distinguish abort causes from failure findings;
- create a result record before clearing current operation state;
- maintain bounded newest-result ordering;
- and, in the later NVMe 1.4 rule set, retire current self-test work when subsystem sanitize takes authority.

The user-visible payload may remain unchanged while substantial controller work and non-payload state are required to make the diagnostic appear continuous or to retire it correctly.

---

## Failure / forgetting boundaries

Keep these separate:

- **short-test reset abort** — operation ends because reset is a specified abort boundary;
- **extended-test reset/power interruption** — operation remains outstanding and later resumes;
- **explicit abort command** — requested termination with a result entry;
- **Format NVM / namespace-change termination** — operation can end because the tested scope changed;
- **sanitize-driven termination (NVMe 1.4+)** — a subsystem-wide conflicting maintenance operation retires in-progress DST and creates corresponding abort evidence;
- **segment diagnostic failure** — the test completes but records one or more failed segments;
- **fatal/unknown test error** — operation does not complete normally;
- **history rollover after >20 results** — older result detail falls outside this bounded log history;
- **user-data loss / sanitize success** — not established merely by a self-test abort transition.

Especially:

> **diagnostic continuity across power restoration != host-write power-loss protection**.

The self-test operation can survive/restart while this source set says nothing by itself about durability of host writes outstanding at power loss.

And:

> **self-test completion without error != secure erase, archival guarantee, or future-readable-forever certificate**.

And for the later sanitize interaction:

> **self-test result 9h != proof that the sanitize operation itself completed successfully**.

---

## Engineering reconstruction

A compact model is:

```text
maintenance request accepted
    !=
maintenance work finished

current work relation
    !=
progress report
    !=
resume checkpoint granularity
    !=
maintenance authority / exclusion domain
    !=
result record
    !=
last-20 history
    !=
user payload
```

A second compact model captures the event-relative persistence horizon:

```text
same extended self-test relation
    + reset / power restoration
        -> preserve obligation and resume

same extended self-test relation
    + NVMe 1.4 sanitize start
        -> retire obligation
        -> preserve bounded reason-for-retirement evidence
```

The strongest project conclusion is:

> **Technical retention can preserve an unfinished maintenance obligation across a selected failure boundary even when exact execution microstate is not standardized, while a stronger conflicting subsystem transition may intentionally retire that obligation and convert it into bounded historical evidence.**

`unfinished maintenance obligation`, `resume-state horizon`, `maintenance-authority domain`, and `result-history conversion` are project engineering language, not NVM Express historical vocabulary.

---

## Functional comparisons

### Case 146 — Flash erase suspend/resume

Case 146 shows a pending erase can remain current while execution is suspended, but its inspected 1990s sources do **not** prove that suspended erase control state survives reset or power loss. NVMe 1.3 extended Device Self-test explicitly requires continuation across Controller Level Reset and restoration of power.

> **powered suspend/resume continuity != reset/power-surviving maintenance continuity**.

This is a functional comparison only; it establishes no genealogy.

### Case 101 — SCSI Background Medium Scan

Both cases expose background media-related maintenance, progress/state, and diagnostic evidence. Case 101's 2024 WD product witness proves BMS can resume after `EN_BMS` disable/re-enable but deliberately stops short of claiming a power-loss-persistent scan checkpoint. NVMe 1.3 extended self-test has an explicit reset/power-restoration continuation requirement.

> **BMS control disable/re-enable continuation != NVMe extended-self-test reset/power continuity**.

The two interfaces also differ in repair policy and result structures; shared scanning/diagnostic shape is not one state machine.

### Case 18 — OpenZFS scrub progress/completion durability

Case 18 exposes implementation-level checkpoint machinery for long-running maintenance and distinguishes work actually performed from work durably checkpointed. Case 148 instead gives an interface contract that extended Device Self-test survives reset/power restoration while resume segment details remain vendor specific.

> **standardized continuation contract != disclosed checkpoint embodiment**.

This is a functional comparison only.

### Case 66 — NVMe 1.4 Persistent Event Log

Case 66 concerns a subsystem-global persistent event history added in NVMe 1.4. Case 148 concerns a self-test log with one current operation plus the newest 20 test outcomes.

> **bounded self-test result history != Persistent Event Log**.

The later sanitize abort result `9h` remains a Device Self-test result-state transition; it does not transform this log into PEL.

### Synthesis 26 — maintenance-control persistence horizons

Case 148 adds a useful horizon not explicit in the original witness set: one maintenance relation is normatively required to cross controller reset and power restoration, while a sibling short operation in the same interface is required to terminate at reset. The later sanitize interaction adds another distinction: a relation may survive a failure boundary but be intentionally retired by a stronger conflicting operation.

This supports Synthesis 26's rule that maintenance-control state must be classified by role and required persistence horizon rather than called generically `metadata` or `checkpoint`.

---

## Prior art and anti-anachronism

The safe historical claims are narrow:

- NVMe 1.3 was ratified 26-Apr-2017 and is dated 1-May-2017;
- NVM Express identifies Device Self-Test as a new optional **NVMe 1.3** feature and attributes it to Technical Proposal 001a;
- T10 material from 2005 already discusses SCSI background short/extended tests, ATA SMART short/extended self-tests, abort, and Self-Test Results logging;
- therefore no global invention claim is made for NVMe;
- the exact TP001a development history and direct lineage remain open;
- NVMe 1.3 already contained `DSTO` controller-vs-subsystem concurrency semantics;
- NVMe 1.3 Sanitize was already subsystem-wide, but the inspected 2017 self-test abort list and result table do not yet contain the later sanitize-driven DST retirement rule / result `9h`;
- NVM Express's Revision 1.4 changes page labels sanitize-driven self-test abort as a mandatory/incompatible change and attributes it to TP4022;
- the TP4022 body itself has not been directly inspected in this slice.

> **later NVMe 1.4 mandatory change != evidence that identical behavior was already normative in NVMe 1.3**.

And:

> **official TP attribution != direct inspection of proposal drafting history**.

---

## Philosophical / media-theoretical interpretation

A narrow interpretive pressure follows from the mechanism: persistence need not mean keeping an unchanged finished object. A system may preserve the **obligation and identity of unfinished technical work** across interruption, later turn that work into an outcome record, and retain only a bounded history of those outcomes.

The sanitize deepening adds one more bounded point: persistence is conditional on the authority relations that keep the unfinished work meaningful. A reset may preserve the extended-test obligation; a later subsystem-wide sanitize operation may deliberately terminate it and preserve only selected evidence of that retirement.

The interpretation stops there. This is not human memory, not a universal theory of “unfinishedness,” not distributed consensus, and not evidence that every maintenance process has durable selfhood. The relevant facts are concrete interface rules for current operation, authority scope, reset/power behavior, result creation, and bounded history.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| NVMe 1.3 was ratified 26-Apr-2017 and document dated 1-May-2017 | H/P | NVM Express Revision 1.3 |
| Device Self-Test was a new optional NVMe 1.3 feature | H/P | official NVM Express revision-changes page |
| ATA/SCSI short/extended self-test and result-log concepts predate NVMe 1.3 | H/P | T10/05-245r1 (2005) |
| Starting a self-test completes the command after the background operation starts | H/P | NVMe 1.3 Figure 68 |
| Short self-test is aborted by Controller Level Reset | H/P | NVMe 1.3 §8.11.1 |
| Extended self-test persists across Controller Level Reset and resumes after reset/power restoration | H/P | NVMe 1.3 §8.11.2 |
| Exact resume segment is vendor specific | H/P | NVMe 1.3 §8.11.2 |
| `DSTO[0]` distinguishes one DST per controller from one DST per subsystem | H/P | NVMe 1.3 Identify Controller + Figure 68 |
| Device Self-test Log exposes current operation/progress plus last 20 results | H/P | NVMe 1.3 §5.14.1.6 |
| Result is created before current operation is cleared | H/P | NVMe 1.3 Figure 98 / Figure 68 |
| NVMe 1.4 mandates subsystem-wide abort of in-progress DST when sanitize starts | H/P | official 1.4 changes page + NVMe 1.4c §5.24 / §8.11 |
| NVMe 1.4c result code `9h` records abort due to sanitize | H/P | NVMe 1.4c Device Self-test Result table |
| Intel D7-P5510 publicly advertises Device Self-test on an NVMe 1.3c product | H/P | Intel/Solidigm D7-P5510 product brief |
| Bounded result history is a complete lifetime diagnostic archive | X | contradicted by last-20 structure |
| Extended-test continuation proves exact internal microstate persistence | X | resume segment is vendor specific; embodiment undisclosed |
| Subsystem-wide DST exclusion proves a consensus protocol or one shared physical state object | X | not specified |
| D7-P5510 feature advertisement proves reset/power-resume fault behavior | X | product brief contains no such test |
| Self-test result `9h` proves sanitize completed successfully | X | result only records DST abort cause |
| Device self-test continuity proves host-write PLP or secure sanitization | X | not established |
| NVMe invented device self-test | X | earlier T10/ATA/SCSI evidence; no genealogy claim |

---

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `NVMe Device Self-test`, `sanitize`, and `DSTO` found no dedicated study to reuse. A broad genealogy of ATA SMART, SCSI SEND DIAGNOSTIC, NVMe TP001a/TP4022, vendor implementation, and diagnostic tooling belongs primarily there if developed comprehensively.

This repository keeps the narrower retention relation: **background maintenance operation identity, interruption survival, authority/exclusion scope, result-state conversion, and bounded diagnostic history**.

Related internal cases/syntheses:

- [`Case 18 — ZFS scrub latent-error detection`](18-zfs-scrub-latent-error-detection.md)
- [`Case 66 — NVM Express 1.4 Persistent Event Log`](66-nvme14-persistent-event-log-history.md)
- [`Case 101 — SCSI Background Medium Scan`](101-scsi-background-medium-scan-proactive-defect-discovery.md)
- [`Case 146 — Flash erase suspend/resume`](146-flash-erase-suspend-pending-operation-state.md)
- [`Synthesis 26 — Maintenance-Control State: Persistence Horizon, Reconstitution, and Authority`](../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md)

---

## Open questions

- Can public archival material establish the exact TP001a drafting/approval chronology without relying on member-only Kavi access?
- Can the ratified TP4022 proposal body be directly inspected to recover the drafting rationale behind sanitize-driven DST retirement, beyond the official changes-page attribution and final normative text?
- On a named Device Self-test-capable drive such as D7-P5510, what do controller-reset and full-power fault tests show for extended-test resume behavior on a specific firmware revision?
- On a real multi-controller subsystem, how does `DSTO` scope affect cross-controller start/abort visibility?
- What implementation mechanism stores/reconstructs extended-self-test resume state across power restoration on shipped devices?
- Does a named product persist the last-20 result population across all resets/power cycles, firmware update, format, and sanitize boundaries, and where do those lifetimes differ?
- How did later NVMe revisions evolve self-test scope, sanitize interaction, virtualization, Host-Initiated Refresh, and result semantics?
- How do ATA SMART and SCSI self-test persistence/abort contracts compare historically without flattening distinct command families?

---

## Sources

1. NVM Express, **NVM Express Revision 1.3**, ratified 26-Apr-2017, document dated 1-May-2017, especially §5.8 pp.87–88, §5.14.1.6 pp.104–107, Identify Controller `DSTO`, and §8.11 pp.258–260: <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>.
2. NVM Express, **Changes in NVMe Revision 1.3**, Device Self-Test new-feature entry and TP001a reference: <https://nvmexpress.org/changes-in-nvme-revision-1-3/>.
3. T10 Technical Committee, Wayne Bellamy / Hewlett-Packard, **T10/05-245r1 — SAT - SEND DIAGNOSTIC command and Self-Test Results**, 7-Nov-2005: <https://www.t10.org/ftp/t10/document.05/05-245r1.pdf>.
4. NVM Express, **Changes in NVMe Revision 1.4**, especially mandatory “Sanitize during Device Self-Test” change and TP4022 attribution: <https://nvmexpress.org/changes-in-nvme-revision-1-4/>.
5. NVM Express, **NVM Express Base Specification Revision 1.4c**, 9-Mar-2021, especially §5.14.1.6, §5.24, and §8.11: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4c-2021.06.28-Ratified.pdf>.
6. Intel / Solidigm, **Intel SSD D7-P5510 Product Brief**, document 345311-001, `1220`: <https://www.solidigm.com/content/dam/solidigm/en/site/products/data-center/d7/p5510/documents/d7-p5510-series-product-brief.pdf>.
