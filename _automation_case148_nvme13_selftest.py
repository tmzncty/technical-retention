from pathlib import Path

CASE_PATH = Path('cases/148-nvme13-device-self-test-reset-surviving-maintenance.md')
EVIDENCE_PATH = Path('evidence/148-nvme13-2017-device-self-test-reset-resume-grounding.md')
INDEX_PATH = Path('CASE_INDEX.md')
ROADMAP_PATH = Path('ROADMAP.md')

for p in (INDEX_PATH, ROADMAP_PATH):
    if not p.exists():
        raise SystemExit(f'missing required file: {p}')
for p in (CASE_PATH, EVIDENCE_PATH):
    if p.exists():
        raise SystemExit(f'{p} already exists; refusing duplicate/concurrent integration')

CASE = r'''# NVM Express 1.3 Device Self-test: Reset-Surviving Diagnostic Work, Resume State, and Bounded Result History

## Status

**`grounded`** — bounded to NVM Express Revision 1.3, ratified 26-Apr-2017 and dated 1-May-2017, with the NVM Express revision-changes page used to establish that Device Self-Test was a new optional NVMe 1.3 feature. A 2005 T10 SAT proposal is used only as earlier ATA/SCSI self-test prior-art evidence; NVMe is not treated as the inventor of storage-device self-test. Later NVMe 1.4 changes are used only as anti-anachronism evidence.

Grounding record: [`../evidence/148-nvme13-2017-device-self-test-reset-resume-grounding.md`](../evidence/148-nvme13-2017-device-self-test-reset-resume-grounding.md).

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

This is **not**:

- a general history of SMART, SCSI SEND DIAGNOSTIC, ATA self-test, or storage diagnostics;
- a claim that NVMe invented short/extended drive self-tests or self-test result logs;
- proof that every NVMe 1.3 device implements Device Self-test, which is optional;
- proof that a resumed extended test preserves an exact internal program counter, NAND address, analog state, or block-by-block checkpoint;
- proof that the last-20 result history has the same cross-power persistence contract as the in-progress extended operation;
- proof that successful self-test establishes complete media integrity, archival fitness, or secure erasure;
- evidence that diagnostic-operation continuity is equivalent to host-write power-loss protection.

---

## Historical vocabulary and chronology

NVM Express Revision 1.3 is dated **1 May 2017** and states that Revision 1.3 was ratified on **26 April 2017**. The NVM Express revision-changes page lists **Device Self-Test (optional)** under the new features in Revision 1.3, describing one self-test command for short and long operations and pointing to Technical Proposal `001a`.

That is an NVMe-family chronology, not a global invention claim.

Earlier self-test traditions are directly visible in T10 document `05-245r1`, dated **7 November 2005**. That SCSI/ATA Translation proposal maps SCSI background short/extended self-test functions to ATA `SMART EXECUTE OFF-LINE IMMEDIATE` short and extended self-test routines and discusses a Self-Test Results log page. Therefore:

> **new to NVMe 1.3 != first storage-device self-test mechanism**.

The exact genealogy from ATA/SCSI traditions to NVMe Technical Proposal 001a remains open; functional similarity and earlier chronology do not establish direct lineage.

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

### Result records are compressed diagnostic evidence, not payload copies

A result structure can carry Power On Hours at completion/abort and, when valid, a failing namespace/LBA plus status information. If multiple logical blocks fail, the Failing LBA field reports only one of them.

Therefore:

> **self-test result record != complete media-error history**.

and

> **self-test result record != user payload replica**.

A result preserves selected evidence about maintenance and faults, not the data being tested.

---

## Retained state

The bounded case contains at least five state classes:

1. **user payload / NVM state** — data whose integrity may be sampled or checked, but not copied into the control state simply by running self-test;
2. **current operation identity/status** — none, short, extended, or vendor-specific;
3. **progress/resume state** — enough state for an extended operation to remain the same outstanding diagnostic across reset/power restoration, with vendor-specific resume segment;
4. **result history** — the newest 20 completed/aborted result structures;
5. **diagnostic detail validity** — per-result validity bits for namespace, failing LBA, and status fields.

These lifetimes and authorities are not interchangeable.

In particular:

> **cross-power operation continuity != proof of cross-power persistence for every diagnostic field or every internal test variable**.

---

## Physical / logical substrate

The specification defines an interface contract, not a required physical representation for self-test resume state. The device may embody that control state in controller nonvolatile storage, flash metadata, another persistent structure, or some implementation-specific reconstruction sufficient to meet the required behavior.

Accordingly, this case grounds **contractual persistence of the extended operation relation**, not a specific transistor/register layout.

This is an important stop condition:

> **required behavior != disclosed embodiment**.

---

## Addressing and access geometry

The Device Self-test command can target:

- controller-only testing (`NSID=0h`);
- one active namespace;
- or all active namespaces accessible through the controller (`FFFFFFFFh`).

The result format can conditionally name a failing namespace/LBA. That makes diagnostic scope and failure location explicit without turning the log into a map of every physical block tested.

The informative example in §8.11 includes RAM, SMART, volatile-memory backup, metadata, NVM integrity, data-integrity housekeeping, media check, and drive-life segments. Because that figure is informative, these examples must not be rewritten as a mandatory universal implementation sequence.

---

## Time

Several time relations coexist:

- short self-test should complete in two minutes or less;
- extended self-test should complete within the time reported by the controller;
- current percentage complete tracks the active operation;
- foreground commands may temporarily suspend background self-test;
- short work ends at Controller Level Reset;
- extended work crosses Controller Level Reset and power restoration;
- completed/aborted results enter a bounded newest-20 history;
- result Power On Hours records the device's power-on-hour count at the termination event.

These are different clocks/horizons. A lifetime of one field cannot be inferred from another merely because they share one log page.

---

## Maintenance and invisible work

Device Self-test makes maintenance itself a retained technical relation. The controller must potentially:

- schedule diagnostic segments around ordinary commands;
- suspend and resume work;
- preserve or reconstruct enough extended-test state across reset/power restoration;
- track current progress;
- distinguish abort causes from failure findings;
- create a result record before clearing current operation state;
- maintain bounded newest-result ordering.

The user-visible payload may remain unchanged while substantial controller work and non-payload state are required to make the diagnostic appear continuous.

---

## Failure / forgetting boundaries

Keep these separate:

- **short-test reset abort** — operation ends because reset is a specified abort boundary;
- **extended-test reset/power interruption** — operation remains outstanding and later resumes;
- **explicit abort command** — requested termination with a result entry;
- **Format NVM / namespace-change termination** — operation can end because the tested scope changed;
- **segment diagnostic failure** — the test completes but records one or more failed segments;
- **fatal/unknown test error** — operation does not complete normally;
- **history rollover after >20 results** — older result detail falls outside this bounded log history;
- **user-data loss / media sanitization** — not established by these diagnostic-state transitions.

Especially:

> **diagnostic continuity across power restoration != host-write power-loss protection**.

The self-test operation can survive/restart while this source set says nothing by itself about durability of host writes outstanding at power loss.

And:

> **self-test completion without error != secure erase, archival guarantee, or future-readable-forever certificate**.

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
result record
    !=
last-20 history
    !=
user payload
```

The strongest project conclusion is:

> **Technical retention can preserve an unfinished maintenance obligation across a failure boundary even when exact execution microstate is not standardized, then convert that current obligation into bounded historical evidence before declaring the work no longer current.**

`unfinished maintenance obligation`, `resume-state horizon`, and `result-history conversion` are project engineering language, not NVM Express historical vocabulary.

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

### Case 66 — NVMe 1.4 Persistent Event Log

Case 66 concerns a subsystem-global persistent event history added in NVMe 1.4. Case 148 concerns a 1.3 self-test log with one current operation plus the newest 20 test outcomes.

> **bounded self-test result history != Persistent Event Log**.

PEL has its own persistence, event selection, capacity, suppression/deletion, sanitize, and reporting-context rules. A later standard may record diagnostic events without making the earlier self-test log itself a PEL.

### Synthesis 26 — maintenance-control persistence horizons

Case 148 adds a useful horizon not explicit in the original witness set: one maintenance relation is normatively required to cross controller reset and power restoration, while a sibling short operation in the same interface is required to terminate at reset.

This supports Synthesis 26's rule that maintenance-control state must be classified by role and required persistence horizon rather than called generically `metadata` or `checkpoint`.

---

## Prior art and anti-anachronism

The safe historical claims are narrow:

- NVMe 1.3 was ratified 26-Apr-2017 and is dated 1-May-2017;
- NVM Express identifies Device Self-Test as a new optional **NVMe 1.3** feature and attributes it to Technical Proposal 001a;
- T10 material from 2005 already discusses SCSI background short/extended tests, ATA SMART short/extended self-tests, abort, and Self-Test Results logging;
- therefore no global invention claim is made for NVMe;
- the exact TP001a development history and direct lineage remain open.

NVM Express's Revision 1.4 changes page later records added/clarified rules, including sanitize-driven self-test abort and clarified Format NVM termination. Those later requirements must not be silently projected backward into every detail of the 2017 Revision 1.3 contract.

> **later NVMe 1.4 clarification/change != evidence that identical wording/behavior was already normative in NVMe 1.3**.

---

## Philosophical / media-theoretical interpretation

A narrow interpretive pressure follows from the mechanism: persistence need not mean keeping an unchanged finished object. A system may preserve the **obligation and identity of unfinished technical work** across interruption, later turn that work into an outcome record, and retain only a bounded history of those outcomes.

The interpretation stops there. This is not human memory, not a universal theory of “unfinishedness,” and not evidence that every maintenance process has durable selfhood. The relevant facts are concrete interface rules for current operation, reset/power behavior, result creation, and bounded history.

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
| Device Self-test Log exposes current operation/progress plus last 20 results | H/P | NVMe 1.3 §5.14.1.6 |
| Result is created before current operation is cleared | H/P | NVMe 1.3 Figure 98 / Figure 68 |
| Bounded result history is a complete lifetime diagnostic archive | X | contradicted by last-20 structure |
| Extended-test continuation proves exact internal microstate persistence | X | resume segment is vendor specific; embodiment undisclosed |
| Device self-test continuity proves host-write PLP or secure sanitization | X | not established |
| NVMe invented device self-test | X | earlier T10/ATA/SCSI evidence; no genealogy claim |

---

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `NVMe Device Self-test` and `self-test` found no dedicated study to reuse. A broad genealogy of ATA SMART, SCSI SEND DIAGNOSTIC, NVMe TP001a, vendor implementation, and diagnostic tooling belongs primarily there if developed comprehensively.

This repository keeps the narrower retention relation: **background maintenance operation identity, interruption survival, result-state conversion, and bounded diagnostic history**.

Related internal cases/syntheses:

- [`Case 66 — NVM Express 1.4 Persistent Event Log`](66-nvme14-persistent-event-log-history.md)
- [`Case 101 — SCSI Background Medium Scan`](101-scsi-background-medium-scan-proactive-defect-discovery.md)
- [`Case 146 — Flash erase suspend/resume`](146-flash-erase-suspend-pending-operation-state.md)
- [`Synthesis 26 — Maintenance-Control State: Persistence Horizon, Reconstitution, and Authority`](../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md)

---

## Open questions

- Can public archival material establish the exact TP001a drafting/approval chronology without relying on member-only Kavi access?
- Which named NVMe 1.3 commercial controllers/drives implemented Device Self-test, and what did reset/power fault testing show?
- What implementation mechanism stores/reconstructs extended-self-test resume state across power restoration on shipped devices?
- Does a named product persist the last-20 result population across all resets/power cycles, firmware update, format, and sanitize boundaries, and where do those lifetimes differ?
- How did later NVMe revisions evolve self-test scope, sanitize interaction, virtualization, and result semantics?
- How do ATA SMART and SCSI self-test persistence/abort contracts compare historically without flattening distinct command families?

---

## Sources

1. NVM Express, **NVM Express Revision 1.3**, ratified 26-Apr-2017, document dated 1-May-2017, especially §5.8 pp.87–88, §5.14.1.6 pp.104–107, and §8.11 pp.258–260: <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>.
2. NVM Express, **Changes in NVMe Revision 1.3**, Device Self-Test new-feature entry and TP001a reference: <https://nvmexpress.org/changes-in-nvme-revision-1-3/>.
3. T10 Technical Committee, Wayne Bellamy / Hewlett-Packard, **T10/05-245r1 — SAT - SEND DIAGNOSTIC command and Self-Test Results**, 7-Nov-2005: <https://www.t10.org/ftp/t10/document.05/05-245r1.pdf>.
4. NVM Express, **Changes in NVMe Revision 1.4**, later sanitize/self-test and Format NVM clarifications used only as anti-anachronism evidence: <https://nvmexpress.org/changes-in-nvme-revision-1-4/>.
'''

EVIDENCE = r'''# Evidence 148 — NVMe 1.3 Device Self-test reset/resume grounding

## Purpose

Ground Case 148 at the interface/specification layer and prevent four common overclaims:

1. treating completion of the Device Self-test command as completion of the self-test operation;
2. treating every self-test as having the same reset/power persistence horizon;
3. treating required extended-test continuation as proof of an exact internal checkpoint representation;
4. treating a 20-entry result log as complete or equivalent to NVMe 1.4 Persistent Event Log history.

This record separates historical primary claims (`H/P`), engineering reconstruction (`E`), functional analogy (`A`), and stop conditions/counterclaims (`X`).

---

## Source ledger

### S1 — NVM Express Revision 1.3 (`H/P`)

- Organization: NVM Express, Inc.
- Revision: 1.3.
- Ratification stated in document: **26-Apr-2017**.
- Document date: **1-May-2017**.
- URL: <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>
- Relevant locations:
  - §5.8, pp.87–88 — Device Self-test command and command processing;
  - §5.14.1.6, pp.104–107 — Device Self-test Log and Self-test Result Data Structure;
  - §8.11, pp.258–260 — background operation, suspension/resume, short/extended reset behavior.

### S2 — NVM Express “Changes in NVMe Revision 1.3” (`H/P`)

- Organization: NVM Express, Inc.
- URL: <https://nvmexpress.org/changes-in-nvme-revision-1-3/>
- Use: identifies Device Self-Test as a **new optional feature** in NVMe Revision 1.3 and references Technical Proposal `001a`.
- Stop condition: “new feature in NVMe 1.3” is an intra-NVMe statement, not a global invention claim.

### S3 — T10/05-245r1 SAT - SEND DIAGNOSTIC command and Self-Test Results (`H/P`)

- Committee: T10 Technical Committee.
- Author: Wayne Bellamy, Hewlett-Packard.
- Date: **7-Nov-2005** (revision 1; revision history notes first revision 8-Sep-2005).
- URL: <https://www.t10.org/ftp/t10/document.05/05-245r1.pdf>
- Relevant locations: pp.1–4.
- Use: establishes that a decade earlier SCSI/ATA translation work already referenced background short/extended self-tests, ATA SMART short/extended self-test routines, abort, and a Self-Test Results log page.
- Stop condition: this proves earlier prior art/functionality, not a direct genealogy into NVMe TP001a.

### S4 — NVM Express “Changes in NVMe Revision 1.4” (`H/P`, later witness)

- Organization: NVM Express, Inc.
- URL: <https://nvmexpress.org/changes-in-nvme-revision-1-4/>
- Use: later change record says Revision 1.4 added a requirement for sanitize to abort self-tests and clarified Format NVM termination behavior.
- Stop condition: this is **later** evidence and must not be back-projected into 2017 as if all wording/behavior were already identical.

---

## Claim-by-claim grounding

### C1 — Chronology

**Claim (`H/P`):** Revision 1.3 is dated 1-May-2017 and states that the revision was ratified on 26-Apr-2017.

**Evidence:** S1 cover/legal front matter.

**Boundary:** ratification date and document date are distinct; neither alone is an invention date for device diagnostics.

### C2 — New to NVMe 1.3, not invented in 2017

**Claim (`H/P`):** NVM Express lists Device Self-Test among the new optional capabilities in Revision 1.3 and references TP001a.

**Evidence:** S2.

**Counterevidence (`H/P`):** S3 (2005) already describes SCSI background short/extended self-test and maps them to ATA SMART short/extended routines, including abort/result logging.

**Conclusion (`E`):** `new NVMe feature != new storage-diagnostic concept`.

### C3 — Command completion precedes operation completion

**Claim (`H/P`):** Figure 68 starts a short/extended self-test and then completes the Device Self-test command successfully.

**Evidence:** S1 §5.8 Figure 68, p.88.

**Conclusion (`E`):** `command completion != maintenance completion`.

### C4 — Background work can suspend/resume around foreground commands

**Claim (`H/P`):** §8.11 says self-test is background work; commands may either run concurrently or require self-test suspension, after which the self-test resumes.

**Evidence:** S1 §8.11, p.258.

**Conclusion (`E`):** `temporary suspension != abort`; current maintenance can remain current while not actively executing.

### C5 — Short reset horizon

**Claim (`H/P`):** short Device Self-test shall be aborted by any Controller Level Reset.

**Evidence:** S1 §8.11.1, p.259.

**Conclusion (`E`):** short current-work state is not required to survive that reset as ongoing work.

### C6 — Extended reset/power-restoration horizon

**Claim (`H/P`):** extended Device Self-test shall persist across any Controller Level Reset and resume after completion of the reset or any restoration of power, if any.

**Evidence:** S1 §8.11.2, p.260.

**Conclusion (`E`):** the extended maintenance obligation/identity has a cross-reset and cross-power-restoration contract.

**Stop condition (`X`):** this requirement does not disclose where/how resume state is physically stored.

### C7 — Resume is not exact microstate preservation

**Claim (`H/P`):** the segment at which extended self-test resumes is vendor specific; implementations should only need to repeat tests within the last segment under test before reset.

**Evidence:** S1 §8.11.2, p.260.

**Conclusion (`E`):** `resume continuity != exact instruction/block-level checkpoint preservation`.

The standard allows replay within a coarser segment, so operation identity can survive without standardizing exact internal microstate.

### C8 — Current state and bounded history are separate

**Claim (`H/P`):** the Device Self-test Log reports current operation, current percentage complete, and results of the last 20 operations.

**Evidence:** S1 §5.14.1.6, pp.104–105.

**Conclusions (`E`):**

- `current execution state != result history`;
- `newest-20 results != complete device history`.

### C9 — Result-before-clear transition ordering

**Claim (`H/P`):** when current self-test completes or aborts, a Self-test Result Data Structure is created before Current Device Self-test Operation is set to `0h`; explicit abort processing uses the same ordering.

**Evidence:** S1 Figure 98, p.105; Figure 68, p.88.

**Conclusion (`E`):** retirement of current-operation authority is preceded by creation of outcome evidence.

**Stop condition (`X`):** the source set does not separately state that all 20 historical result entries survive every power/reset/firmware/sanitize boundary.

### C10 — Abort reason and diagnostic failure are distinct

**Claim (`H/P`):** Figure 99 has distinct codes for explicit abort, Controller Level Reset abort, namespace-removal abort, Format NVM abort, fatal/unknown error, and completed tests with failed segments.

**Evidence:** S1 Figure 99, p.106.

**Conclusion (`E`):** `aborted != failed`; termination cause and diagnostic outcome are different retained facts.

### C11 — Result record is compressed evidence

**Claim (`H/P`):** result structures may carry Power On Hours, namespace/LBA and status information; if multiple logical blocks fail, only one failing LBA is reported.

**Evidence:** S1 Figure 99, pp.106–107.

**Conclusion (`E`):** result structures retain selected diagnostic evidence, not a full test trace or media history.

### C12 — Later Revision 1.4 behavior cannot be back-projected

**Claim (`H/P`):** S4 identifies later mandatory changes/clarifications around sanitize and Format NVM interaction with Device Self-test.

**Conclusion (`E/X`):** use S1 for 2017 normative behavior; later revision-change pages are temporal guardrails, not evidence that later wording was already in 1.3.

---

## Cross-case controls

### Case 146 — Flash erase suspend/resume (`A`)

Both mechanisms retain an unfinished-work relation while execution can be paused. But Case 146's inspected 1990s product/patent sources do not establish resume after power loss/reset. NVMe 1.3 extended self-test explicitly requires persistence across Controller Level Reset and resumption after restoration of power.

Safe comparison:

> `powered pending-operation state != failure-boundary-persistent pending-operation state`.

No lineage is claimed.

### Case 101 — SCSI Background Medium Scan (`A`)

Both are background diagnostic/maintenance processes. The WD 2024 Case-101 witness supports disable/re-enable continuation of BMS but deliberately leaves power-cycle persistence open. NVMe 1.3 extended self-test instead contains an explicit reset/power-restoration requirement.

Safe comparison:

> `maintenance progress continuity under control toggling != specified crash/power interruption continuity`.

### Case 66 — NVMe 1.4 Persistent Event Log (`A`)

Self-test result history is count-bounded at 20 and tied to self-test outcomes. PEL is a later, subsystem-global event-history mechanism with its own persistence and deletion rules.

Safe comparison:

> `self-test history != persistent event history`.

### Synthesis 26 (`E/A`)

Case 148 strengthens the persistence-horizon matrix: even within one standardized maintenance feature, sibling operations can intentionally have different reset horizons. It also shows that required continuation does not force one standardized reconstitution mechanism.

---

## Counterclaim ledger

| Shortcut | Status | Reason |
| --- | --- | --- |
| “The start command completed, so the test completed” | rejected | Figure 68 completes command after starting background operation |
| “All self-tests survive reset” | rejected | short test shall abort on Controller Level Reset |
| “No self-test survives power loss” | rejected | extended test shall resume after restoration of power |
| “Resume means exact internal checkpoint” | rejected | resume segment is vendor specific; rework inside last segment is permitted/recommended |
| “Current percentage is an exact durable LBA/block cursor” | rejected | percentage is progress reporting; no exact durable physical cursor is specified |
| “Last 20 results are complete lifetime history” | rejected | explicit newest-20 bound |
| “Aborted means failed media” | rejected | abort reasons and segment failures have distinct result codes |
| “Self-test result is user payload” | rejected | result stores diagnostic metadata/selected failure evidence |
| “Self-test passing proves future retention forever” | rejected | no such guarantee in S1 |
| “Self-test continuation proves host-write PLP” | rejected | different retained relation; not established |
| “NVMe invented device self-test” | rejected | 2005 T10/ATA/SCSI evidence predates NVMe 1.3 |
| “NVMe 1.4 behavior can be read back into 1.3” | rejected | official revision-changes page identifies later changes/clarifications |

---

## Related-repository boundary

Fresh searches of `tmzncty/computing-archaeology` for `NVMe Device Self-test` and `self-test` returned no dedicated study. This evidence record therefore keeps only the retention-specific contract needed for Case 148.

A wider history of:

- ATA SMART self-test;
- SCSI SEND DIAGNOSTIC;
- SAT translation;
- NVM Express TP001a drafting;
- vendor firmware implementations;
- diagnostic tooling and operational practice;

belongs primarily in `computing-archaeology` rather than being duplicated here.

---

## Open debt

- obtain public TP001a text/approval chronology if an authoritative public copy exists;
- identify a named NVMe 1.3 product implementing Device Self-test;
- perform or cite reset/power-fault experiments that observe extended-test resume behavior on hardware;
- determine product-specific persistence/reset rules for the last-20 result history;
- compare later NVMe self-test revisions without rewriting later semantics into the 2017 case.
'''

CASE_ROW = r'''| [NVM Express 1.3 Device Self-test: Reset-Surviving Diagnostic Work, Resume State, and Bounded Result History](cases/148-nvme13-device-self-test-reset-surviving-maintenance.md) | **grounded** | optional NVMe background diagnostic operation + reset/power-surviving extended-work relation + current progress + newest-20 result history | distinguish command completion from maintenance completion; short-reset abort from extended reset/power resume; operation identity from exact checkpoint microstate; current work from bounded result evidence | [2017 NVMe 1.3 grounding + 2005 prior-art guardrail](evidence/148-nvme13-2017-device-self-test-reset-resume-grounding.md); TP001a public chronology, named-product embodiment, result-log persistence boundaries, and hardware fault validation remain open |'''

FINDINGS = r'''
## Case 148 — NVMe 1.3 Device Self-test findings

Grounding record: [`evidence/148-nvme13-2017-device-self-test-reset-resume-grounding.md`](evidence/148-nvme13-2017-device-self-test-reset-resume-grounding.md).

- **3196 — 26-Apr-2017 ratification != 1-May-2017 document date:** NVMe 1.3 states both dates; keep ratification and published-document chronology distinct. (`H/P`)
- **3197 — new optional NVMe 1.3 feature != global invention:** NVM Express lists Device Self-Test as a new optional Revision-1.3 capability tied to TP001a, but this is an intra-NVMe chronology claim. (`H/P`, `X`)
- **3198 — 2005 ATA/SCSI self-test prior art != proven direct genealogy:** T10/05-245r1 already maps SCSI short/extended tests to ATA SMART routines and a results log, so NVMe invention priority is rejected without inferring direct lineage. (`H/P`, `A`, `X`)
- **3199 — command completion != self-test completion:** NVMe 1.3 Figure 68 starts short/extended background work and then completes the Device Self-test command. (`H/P`, `E`)
- **3200 — current maintenance execution != retained result history:** Log 06h separately exposes current operation/progress and newest completed/aborted result structures. (`H/P`, `E`)
- **3201 — short-test reset boundary != extended-test reset boundary:** short self-test shall abort on any Controller Level Reset; extended self-test shall persist across reset. (`H/P`, `E`)
- **3202 — extended maintenance obligation crosses power restoration:** NVMe 1.3 requires extended self-test to resume after reset or restoration of power, establishing a failure-boundary persistence contract for unfinished diagnostic work. (`H/P`, `E`)
- **3203 — resume continuity != exact microstate preservation:** resume segment is vendor specific and tests within the last segment may be repeated; operation identity can survive without a standardized exact internal checkpoint. (`H/P`, `E`, `X`)
- **3204 — percentage complete != byte/block-exact durable cursor:** the log reports percentage progress but the specification does not equate that value with a precise persistent physical restart position. (`H/P`, `E`, `X`)
- **3205 — background suspension != abort:** §8.11 requires suspend/process/resume around commands that cannot run concurrently, so temporarily inactive execution can remain current maintenance work. (`H/P`, `E`)
- **3206 — current-operation retirement != immediate loss of outcome evidence:** completion/abort creates a Self-test Result Data Structure before current operation is set to no-operation. (`H/P`, `E`)
- **3207 — aborted != failed:** result codes distinguish explicit/reset/namespace/format aborts from fatal test errors and completed tests with failed segments. (`H/P`, `E`)
- **3208 — newest-20 result history != complete device history:** Log 06h retains a bounded 20-result window rather than an unlimited diagnostic archive. (`H/P`, `E`)
- **3209 — self-test result != payload replica or complete media-error trace:** result structures store selected diagnostic metadata and at most one failing LBA when multiple blocks fail. (`H/P`, `E`)
- **3210 — Case146 powered suspend continuity != NVMe reset/power continuity:** Flash erase-suspend sources did not prove power-loss survival; NVMe extended self-test explicitly crosses reset/power restoration. Functional comparison only. (`A`, `X`)
- **3211 — Case101 BMS disable/re-enable continuation != reset/power-persistent diagnostic work:** the WD BMS witness resumes after control toggling but leaves power-cycle persistence open; NVMe 1.3 states a stronger extended-test boundary. (`A`, `X`)
- **3212 — self-test result log != NVMe 1.4 Persistent Event Log:** Case66 PEL has separate subsystem-global persistence/deletion/sanitize/reporting-context semantics; the 1.3 self-test log is a current-operation + newest-20 outcome interface. (`A`, `X`)
- **3213 — later NVMe 1.4 self-test changes != original 1.3 wording:** sanitize-driven abort and Format NVM clarifications are later revision evidence and must not be back-projected. (`H/P`, `E`, `X`)
- **3214 — extended diagnostic continuity != host-write power-loss protection or sanitize proof:** survival of maintenance-operation identity says nothing by itself about outstanding host-write durability or forensic erasure. (`E`, `X`)
- **3215 — related-repository boundary:** fresh `tmzncty/computing-archaeology` searches found no dedicated NVMe Device Self-test study; broad ATA/SCSI/NVMe diagnostic genealogy belongs there while Case148 retains the persistence-horizon relation. (`H/P` project-state record)
'''

ROADMAP_ENTRY = r'''
- [x] **Case 148 NVMe 1.3 Device Self-test reset/power-surviving maintenance slice** — [`cases/148-nvme13-device-self-test-reset-surviving-maintenance.md`](cases/148-nvme13-device-self-test-reset-surviving-maintenance.md), grounded by [`evidence/148-nvme13-2017-device-self-test-reset-resume-grounding.md`](evidence/148-nvme13-2017-device-self-test-reset-resume-grounding.md): Revision 1.3 (ratified 26-Apr-2017, dated 1-May-2017) separates command completion from background test completion, makes short self-test abort on Controller Level Reset while extended self-test persists across reset and resumes after power restoration, allows vendor-specific/coarse resume within the last segment, and converts completion/abort into a result record before clearing current status. Log 06h retains current progress plus only the newest 20 outcomes, so `current work != bounded history != exact checkpoint != payload`. T10 2005 provides an earlier ATA/SCSI self-test prior-art guardrail without a genealogy claim. TP001a public chronology, named-product implementation, exact result-log persistence, and hardware fault testing remain open; fresh `computing-archaeology` searches found no dedicated study to reuse.
'''

# Concurrency / numbering guards.
index = INDEX_PATH.read_text(encoding='utf-8')
roadmap = ROADMAP_PATH.read_text(encoding='utf-8')
if 'cases/148-nvme13-device-self-test-reset-surviving-maintenance.md' in index or 'Case 148 — NVMe 1.3 Device Self-test findings' in index:
    raise SystemExit('Case148 already present in CASE_INDEX; refusing duplicate')
if '3196 —' in index:
    raise SystemExit('finding 3196 already occupied; concurrent index advance requires renumbering')
if '3195 — related-repository boundary' not in index:
    raise SystemExit('expected Case147 terminal finding 3195 not found; concurrent state changed')
if 'cases/147-s3-multipart-upload-preobject-retention.md' not in index:
    raise SystemExit('expected Case147 index row missing')
if 'Case 148 NVMe 1.3 Device Self-test reset/power-surviving maintenance slice' in roadmap:
    raise SystemExit('Case148 already present in ROADMAP; refusing duplicate')
if 'Case 147 S3 Multipart Upload pre-object retention / completion / abort slice' not in roadmap:
    raise SystemExit('expected Case147 roadmap state missing')

CASE_PATH.write_text(CASE.rstrip() + '\n', encoding='utf-8')
EVIDENCE_PATH.write_text(EVIDENCE.rstrip() + '\n', encoding='utf-8')

marker = '\n## Comparison matrix — provisional'
if marker not in index:
    raise SystemExit('CASE_INDEX case-table marker not found')
index = index.replace(marker, '\n' + CASE_ROW + marker, 1)
index = index.rstrip() + '\n' + FINDINGS.strip() + '\n'
INDEX_PATH.write_text(index, encoding='utf-8')

roadmap = roadmap.rstrip() + '\n' + ROADMAP_ENTRY.strip() + '\n'
ROADMAP_PATH.write_text(roadmap, encoding='utf-8')
