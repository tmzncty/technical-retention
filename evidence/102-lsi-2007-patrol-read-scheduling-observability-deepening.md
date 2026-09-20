# Evidence 102A — LSI MegaRAID 2007 Patrol Read Scheduling, Coverage, and Observability Boundary

## Status

**`bounded deepening complete`** for the June-2007 MegaRAID Version 2.0 maintenance-control slice described here.

This packet deepens [`../cases/102-perc-megaraid-patrol-read-consistency-boundary.md`](../cases/102-perc-megaraid-patrol-read-consistency-boundary.md). It does **not** replace the 2005 Dell PERC grounding and does not claim a complete PERC→MegaRAID hardware or firmware genealogy.

## Research question

Case 102 already established the important task boundary:

```text
Patrol Read
    !=
Consistency Check
```

The remaining version-specific question was narrower:

> By June 2007, what did LSI MegaRAID Version 2.0 directly expose about Patrol Read scheduling, scope, execution admission, progress/status observability, and its difference from Consistency Check?

The result adds a second boundary that should not be hidden inside the word `scan`:

```text
maintenance configuration
    !=
maintenance execution
    !=
progress / status evidence
    !=
coverage completion
    !=
repair success
```

## Source custody

### Directly inspected manual

- **LSI Corporation, _MegaRAID SAS Software User’s Guide_, Document 80-00156-01 Rev. B, Version 2.0, June 2007.**
- Surviving facsimile mirror inspected at:
  - <https://techpubs.jurassic.nl/library/manuals/0000/860-0488-001/pdf/860-0488-001.pdf>
- The PDF itself identifies LSI Corporation, document number, revision, version, and June-2007 date.
- Relevant printed/PDF locations inspected through the surviving text layer:
  - revision history: PDF p. 5;
  - §1.4.5 `Consistency Check`: PDF p. 25;
  - §1.4.7 `Patrol Read`: PDF p. 26;
  - §3.5 Patrol Read adapter properties: PDF pp. 121–122;
  - §7.5 `Running a Patrol Read`: PDF pp. 210–212;
  - §8.2 `Running a Consistency Check`: later maintenance chapter;
  - Appendix A event table: patrol-read progress/error event vocabulary.

The hosting domain is not LSI/Broadcom. The evidential object is therefore **an LSI-authored period manual preserved on a third-party technical-publication mirror**, not a claim that the mirror is an official LSI publication server.

A screenshot request against the PDF mirror was attempted during this research pass but the web cache returned a cache-miss error. Claims below therefore rely on the successfully retrieved PDF text layer and visible LSI document metadata, not on a claimed fresh image-level facsimile inspection of every cited page.

### Corroborating converted copies

Converted copies of the same Version 2.0 text were also found at StudyLib / Doczz. They are useful for phrase location and searchability but do not increase the historical claim merely by duplicating the same authored manual.

## Historical record

### H/P — the surviving June-2007 document is Version 2.0, Rev. B

The manual title page identifies:

- document `80-00156-01`;
- Rev. B;
- Version 2.0;
- June 2007;
- LSI Corporation authorship/copyright.

Its revision history records:

```text
DB15-000339-00        December 2005   Version 1.0   Initial release
80-00156-01 Rev. A    August 2006     Version 1.1   RAID 10/50 procedure correction
80-00156-01 Rev. B    June 2007       Version 2.0   WebBIOS/MSM/MegaCLI updates + RAID intro
```

This directly anchors the **document family chronology**.

It does **not** prove that every Version-2.0 Patrol Read sentence was present unchanged in Version 1.0 or 1.1. The packet therefore attributes exact scheduling and observability wording only to the inspected June-2007 Version 2.0 text.

### H/P — Version 2.0 directly distinguishes Patrol Read from Consistency Check

Section 1.4.5 defines Consistency Check around redundant virtual disks. It says the operation verifies correctness of data in RAID 1, 5, 10, 50, and 60; in a parity example it computes data and compares the result with parity. The same passage recommends running a consistency check at least monthly.

Section 1.4.7 separately describes Patrol Read as review for possible **physical disk errors** that could lead to drive failure, followed by corrective action depending on array configuration and error type.

Therefore the June-2007 manual itself preserves two distinct maintenance objects:

```text
Patrol Read
    -> physical-disk error discovery / corrective path

Consistency Check
    -> redundant virtual-disk correctness relation
```

This is direct Version-2.0 evidence and no longer needs to be inferred only from the later Rev. F manual.

### H/P — Patrol Read has explicit admission conditions that are not identical to its run duration

Section 1.4.7 says Patrol Read starts only when the controller has been idle for a defined period and no other background tasks are active, while also saying that once started it can continue during heavy I/O.

That gives a useful historical boundary:

```text
idle / no-background-task start admission
    !=
idle-only execution
```

A scan can therefore be admitted under one resource condition and continue under a different foreground-I/O condition.

This matters for retention analysis because `automatic` does not mean `unconditional at an exact wall-clock instant`.

### H/P — Version 2.0 exposes automatic, manual, disabled, and continuous scheduling modes

Section 7.5 says Patrol Read can be configured as:

- `Auto` — runs automatically at the configured interval;
- `Manual` — runs only when manually started;
- `Disabled` — does not run.

The same section gives a default periodic frequency of **7 days / 168 hours** and offers `Continuous Patrolling`, under which the periodic interval field is disabled.

The command-tool section separately exposes:

- `-Dsbl`;
- `-EnblAuto`;
- `-EnblMan`;
- `-Start`;
- `-Stop`;
- `-Info`;
- an interval/delay setting in hours, where zero means immediate restart.

These controls are historical interface facts. They do not establish a seven-day physical defect-formation law.

### H/P — task rate is an explicit resource-allocation control

Version 2.0 exposes a Patrol Read task rate. The manual explains that the rate controls how much system resource is dedicated to Patrol Read while it is running and warns that raising it can slow foreground tasks, while lowering background-task rates can make background work take much longer.

Thus the period interface already separates:

```text
whether maintenance is enabled
    !=
when it is admitted
    !=
how aggressively resources are allocated to it
```

This is controller scheduling state, not payload state and not a media-health verdict.

### H/P — the documented physical-drive scope is broader than redundant virtual drives

Section 7.5 says Patrol Read periodically verifies all sectors of physical disks connected to a controller, including the system-reserved area on RAID-configured drives. It says Patrol Read can be used for all RAID levels and all hot-spare drives.

Consistency Check, by contrast, is meaningful on redundant virtual disks. Version 2.0 lists RAID 1/5/10/50/60 in its definition and explicitly notes that RAID 0 provides no data redundancy.

The resulting scope distinction is direct:

```text
controller physical-drive patrol scope
    !=
redundant virtual-disk consistency scope
```

### H/P — the UI exposes an observability asymmetry

The Version-2.0 Patrol Read instructions say that Patrol Read does not report its progress through the running operation UI and that its status is reported in the event log.

The appendix event vocabulary includes a separate Patrol Read progress event and separate events for:

- corrected medium error;
- progress;
- uncorrectable medium error;
- bad-block puncturing.

The command interface also exposes `-Info`, which returns operation mode, execution-delay value, and Patrol Read status.

Consistency Check has a different interface path: its maintenance section says its progress can be monitored, and command/UI facilities expose consistency-check progress.

The safe reconstruction is therefore not `Patrol Read has no progress state`. It is:

```text
internal / logged progress state may exist
    !=
progress is exposed through the same interactive UI path
```

and:

```text
maintenance observability channel
    is itself part of the controller interface contract
```

### H/P — event evidence distinguishes progress from correction and failure

The event table does not collapse Patrol Read into one binary state. It distinguishes at least:

```text
progress
corrected medium error
uncorrectable medium error
bad-block puncture
```

Consequently:

```text
scan in progress
    !=
medium defect found
    !=
defect corrected
    !=
unrecoverable defect
    !=
puncture action
```

An administrator seeing one event class has not thereby obtained all the others.

## Engineering reconstruction

The following are project-level engineering reconstructions from the historical interface, not LSI's ontology.

### E — configuration state is not execution state

A controller can retain:

- Auto/Manual/Disabled mode;
- delay/frequency;
- Continuous Patrolling choice;
- task rate;
- include/exclude scope.

Those are instructions and policy parameters.

They do not prove that a current pass:

- has started;
- has reached a specific disk or sector;
- has completed;
- found no defect;
- successfully repaired every defect it found.

Therefore:

```text
maintenance configured
    !=
maintenance performed
```

### E — default cadence is policy, not a hazard clock

The seven-day default is a controller/software operating policy documented for Version 2.0.

It is not evidence that:

- sectors become unsafe on day eight;
- no defect can appear inside seven days;
- every pass finishes before the next nominal interval;
- seven days is universal across later MegaRAID firmware.

Thus:

```text
configured cadence
    !=
physical defect-arrival process
```

### E — admission condition is not execution exclusivity

The manual says idle/no-background-task conditions gate start but that heavy I/O need not terminate an already-running patrol.

So:

```text
start precondition
    !=
whole-run invariant
```

This is a useful generic retention-control distinction: a maintenance obligation can wait for an admissible start window even though its execution later overlaps foreground use.

### E — progress evidence is not a coverage certificate

A progress/status event can tell an operator that work is underway or how the controller reports its state. It does not by itself prove complete medium coverage.

Likewise, completion of a pass would only certify bounded observations during that pass; it would not prove timeless future readability.

Therefore:

```text
status/progress evidence
    !=
coverage completion
    !=
future media-health guarantee
```

### E — corrective-action vocabulary does not prove payload restoration

A `corrected medium error` event is stronger than a progress event but still must not be inflated into a universal statement that logical payload, redundancy relation, and all media-health state have been fully restored.

A `puncturing bad block` event is explicitly different again.

The safe relation remains:

```text
error discovered
    !=
error corrected
    !=
payload reconstructed
    !=
redundancy re-qualified
```

## Controlled functional comparison

### Case 101 — SCSI Background Medium Scan

Both device-side BMS and controller-side Patrol Read schedule proactive medium checking. This packet adds only a controller-interface comparison:

- MegaRAID exposes controller-level Auto/Manual/Disabled, delay, rate, scope, and event-log status;
- T10 BMS belongs inside the SCSI device-server maintenance model.

Functional similarity does not establish code or design genealogy.

### Case 17 — RAID parity reconstruction

Consistency Check can evaluate a redundancy relation; Patrol Read can expose medium defects. Neither interface fact alone proves that parity reconstruction is available for every discovered error.

### Case 18 / ZFS scrub

MegaRAID's event/status model can be compared with ZFS scrub only at the level of `maintenance work produces operator-visible evidence`. ZFS checksum authority and end-to-end block identity are different mechanisms.

## Philosophical interpretation — bounded downstream layer

This slice makes one narrow conceptual point useful to the project:

> A maintenance policy can persist as configuration even while evidence that the policy has actually been fulfilled must be produced again by execution.

That is a project interpretation. LSI's 2007 manual documents controls, scopes, and observable events; it does not present a philosophy of memory.

A second bounded interpretation is that **maintenance has an epistemic interface**: controllers retain not only payload and redundancy state but also status/event records that let operators know something about ongoing or failed maintenance. Such records are evidence about maintenance, not the maintained object itself.

## Explicit non-claims

This packet does **not** claim that:

1. LSI invented Patrol Read.
2. Version 2.0 first introduced Patrol Read.
3. Every Version-2.0 sentence was already present in Version 1.0.
4. Rev. B's revision note proves unchanged Patrol Read wording in Rev. A.
5. Dell PERC 2005 and LSI MegaRAID 2007 share one firmware implementation.
6. PERC is simply an OEM rename of the exact controller documented here.
7. seven days is a physical-media retention constant.
8. seven days is a universal recommended interval for all MegaRAID generations.
9. Auto mode guarantees an exact start time.
10. Auto mode guarantees a pass finishes before the next nominal interval.
11. Continuous Patrolling means every sector is under continuous observation.
12. an idle start condition means the whole pass runs only while idle.
13. Patrol Read and Consistency Check have disjoint physical I/O.
14. Patrol Read validates parity.
15. Consistency Check covers all controller-attached physical sectors.
16. Patrol Read completion proves parity consistency.
17. Consistency Check completion proves controller-wide media readability.
18. a progress event proves pass completion.
19. a status value proves repair success.
20. a corrected-medium-error event proves every logical/redundancy layer is restored.
21. bad-block puncturing is equivalent to successful remapping.
22. event-log presence equals persistent power-loss-safe logging semantics.
23. `-Info` reveals exact sector-level coverage.
24. the manual specifies checkpoint/restart semantics for an interrupted patrol.
25. controller reboot semantics for an in-progress patrol are established here.
26. firmware upgrade preserves in-progress patrol state.
27. manual mode is safer or less safe than Auto mode.
28. a monthly Consistency Check recommendation is a universal RAID rule.
29. RAID 0 Patrol Read supplies redundancy that RAID 0 lacks.
30. this packet is a history of RAID scrubbing in general.

## Claim ledger

| Claim | Type | Strength | Boundary |
| --- | --- | --- | --- |
| LSI Version 2.0 / Rev. B is dated June 2007 | H/P | strong | directly visible document metadata |
| Revision table records initial Version 1.0 in Dec. 2005 and Version 1.1 in Aug. 2006 | H/P | strong | document-family chronology only |
| Version 2.0 directly defines Consistency Check for redundant virtual disks | H/P | strong | exact June-2007 wording |
| Version 2.0 directly describes Patrol Read around physical-disk errors | H/P | strong | exact June-2007 wording |
| Patrol Read starts under idle/no-other-background-task admission but may continue during heavy I/O | H/P | strong | Version-2.0 controller behavior |
| Auto/Manual/Disabled are explicit modes | H/P | strong | Version-2.0 interface |
| default periodic frequency is seven days / 168 h | H/P | strong | software default, not physical hazard law |
| Continuous Patrolling removes the periodic interval field | H/P | strong | does not imply instantaneous/full-time sector coverage |
| Patrol Read task rate allocates controller resources | H/P | strong | not payload state |
| Patrol Read covers physical disks, system-reserved areas, all RAID levels and hot spares | H/P | strong | bounded to inspected manual |
| Consistency Check and Patrol Read have different scopes | H/E | strong | direct definitions + controlled decomposition |
| Patrol Read UI progress/status path differs from Consistency Check monitoring | H/E | strong | interface/observability boundary |
| event vocabulary distinguishes progress, correction, unrecoverable error and puncture | H/P | strong | event evidence, not repair guarantee |
| maintenance configuration ≠ execution ≠ observation ≠ completion | E | strong | project decomposition supported by interfaces |
| same document family chronology = identical earlier wording | X | rejected | exact earlier texts not inspected |
| seven-day default = seven-day defect clock | X | rejected | category error |

## Remaining evidence debt

This packet closes only the **June-2007 Version-2.0 direct-text gap**. Still open:

- direct Version 1.0 (December 2005) and Version 1.1 (August 2006) facsimile comparison;
- Version 2.1 / Rev. C exact diff;
- controller reboot / power-loss behavior while Patrol Read is in progress;
- whether patrol coverage position is checkpointed, restarted, or discarded across reset;
- persistence semantics of Patrol Read event/status records;
- exact firmware/controller product matrix for this manual;
- Dell PERC↔LSI MegaRAID OEM/silicon/firmware genealogy;
- empirical tests showing how Auto/Continuous modes behave under sustained foreground/background load;
- relation between physical-drive exclusions and actual sector coverage in each firmware family.

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `MegaRAID Patrol Read` returned no dedicated packet.

Broader work on:

- LSI controller model chronology;
- Dell OEM relationships;
- exact Version 1.0→2.x document/software genealogy;
- RAID controller product history;
- origin/first-use history of `Patrol Read`;

belongs in `computing-archaeology` unless it is needed to establish a retention-specific boundary here.

## Result

The June-2007 Version-2.0 manual directly closes an evidential gap left by Case 102's reliance on a later Rev. F continuity witness. By 2007 LSI explicitly exposed Patrol Read as a separately scheduled physical-drive maintenance operation with Auto/Manual/Disabled modes, a seven-day default cadence, optional continuous patrolling, task-rate controls, idle admission, broad physical-drive scope, and event/status observability. The same manual separately defines Consistency Check at the redundant virtual-disk layer.

The strongest retention result is not another generic statement that `scrubbing is good`; it is the control-state decomposition:

```text
policy / schedule retained by controller
    !=
maintenance admitted
    !=
maintenance executing
    !=
progress/status observed
    !=
coverage complete
    !=
repair / redundancy re-qualified
```

That distinction is directly useful across later storage-maintenance cases without turning MegaRAID's specific historical vocabulary into a universal storage ontology.
