# Evidence 148 — NVMe 1.3 Device Self-test reset/resume grounding

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
