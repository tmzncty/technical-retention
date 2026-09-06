# NVM Express SMART / Health Endurance Telemetry: Retained Device History Without Payload History

## Status

**`grounded`** — bounded to the NVMe 1.0/1.0e/1.3 SMART / Health Information interface and a 2014 Intel DC P3700 product witness. The spare-exhaustion deepening uses the original 2011 Gold specification to separate spare-threshold warning, reserve exhaustion, and actual command failure without inferring a hidden SSD remapping algorithm. A prior-art pass adds a bounded 1995–1997 ATA SMART floor for retained drive-health state, while explicitly refusing to equate ATA vendor-specific attributes with the later NVMe SMART / Health schema or to claim a direct ATA→NVMe genealogy. A further ATA/ATAPI-5 pass adds a bounded 1999 diagnostic-history relation: off-line data collection, short/extended self-test, off-line versus captive execution, current progress/status, and a finite circular self-test log are kept distinct. The case establishes that an SSD can retain cumulative health/endurance evidence across power cycles and expose it to host software without that evidence being the user payload or a complete physical wear history.

Grounding record: [`../evidence/55-nvme10-13-smart-health-endurance-grounding.md`](../evidence/55-nvme10-13-smart-health-endurance-grounding.md).

## Scope

This case asks a narrow retention question:

> What changes when the storage device retains facts about **its own past use and degradation** in order to qualify future service?

The object is the NVMe `SMART / Health Information` log, especially:

- `Percentage Used`;
- `Available Spare` and `Available Spare Threshold`;
- `Data Units Written`;
- `Power Cycles`, `Power On Hours`, and `Unsafe Shutdowns`;
- `Media and Data Integrity Errors` / `Media Errors`;
- the distinction between cumulative/lifetime information and the current `Critical Warning` state.

This is not a general history of SMART, NAND endurance, wear leveling, SSD failure prediction, or enterprise fleet management. It also does not claim that the standardized host-visible counters expose the controller's complete internal P/E-cycle distribution, write amplification, bad-block map, ECC history, or physical degradation model.

## Historical record

### 1995–1997 ATA SMART supplies an older drive-health-state floor without supplying the NVMe schema

The NVMe interface is not the beginning of drive-health state retention. An official **July 1995 X3T10 SFF Liaison Report (`95-292r0`)** states that a copy of `SMART (Self Monitoring Analysis and Reporting Technology)` submitted by Quantum had been approved for publication as **SFF-8035i**. The document is useful as a standards-history floor, but it does **not** prove that Quantum invented SMART or that the inspected copy contains every semantic detail later carried into ATA.

The later **ATA-3 Working Draft X3T13/2008D Revision 7b, 27 January 1997** provides the needed interface semantics. Its revision history records that Revision 3, dated **26 July 1995**, `Added SFF8035i S.M.A.R.T. into the standard`. Clause 6.6 then describes SMART as monitoring and **storing** performance/calibration parameters to predict near-term degradation or fault conditions. The draft is explicit that the set and identity of attributes are selected by the device manufacturer and are vendor-specific/proprietary, while thresholds are manufacturer-determined from design/reliability testing.

That distinction matters for this case. ATA-3 does not present one fixed cross-vendor health schema equivalent to the later NVMe log. It presents a host interface around a manufacturer-selected attribute/threshold model.

The same draft also gives direct retention semantics for the monitoring machinery itself:

- `SMART DISABLE OPERATIONS` says the enabled/disabled SMART state is preserved across power cycles;
- `SMART ENABLE/DISABLE ATTRIBUTE AUTOSAVE` allows updated attribute values to be saved to **nonvolatile memory** after vendor-specified events, and preserves the autosave enabled/disabled state across power cycles;
- `SMART READ ATTRIBUTE VALUES` saves updated values to nonvolatile memory before returning the attribute-value structure;
- `SMART RETURN STATUS` saves updated values to nonvolatile memory before comparing them with the thresholds;
- `SMART SAVE ATTRIBUTE VALUES` explicitly forces updated values into nonvolatile memory regardless of the autosave timer.

The bounded historical result is therefore stronger than the generic statement `SMART existed before NVMe`:

```text
manufacturer-selected monitored attribute
        -> retained/updated attribute value
        -> manufacturer-set threshold
        -> threshold comparison / reliability status
        -> host-visible warning relation
```

with a separate policy/control path:

```text
SMART enabled state
attribute-autosave enabled state
        -> preserved across power cycles
```

and a separate materialization step:

```text
updated attribute value
        -> optional/event- or command-triggered save to nonvolatile memory
```

These arrows are an **engineering reconstruction of the documented interface relations**, not period terminology and not a claim that every ATA device implemented the same internal sensors, media, firmware, or persistence mechanism.

The source boundary is also explicit. The ATA-3 text inspected here is a period **working draft** preserved through a third-party transcription/mirror. Its document identity, revision/date, clause structure, and wording are strong enough for this bounded standards-history comparison, but the project does not silently upgrade the mirror into a directly inspected original SFF-8035i facsimile or use it to settle SMART invention priority.

### 1999 ATA/ATAPI-5 separates off-line data collection, self-test execution mode, and retained diagnostic history

The **ATA/ATAPI-5 Working Draft T13/1321D Revision 2, 13 December 1999** supplies a later but still pre-NVMe diagnostic-history boundary. This source is a period draft transcription/mirror rather than a directly rendered T13 facsimile; T13's official expired-standards ledger independently identifies project `1321D` as **AT Attachment - 5 with Packet Interface (ATA/ATAPI-5)** and gives its standards-submission date as **28 February 2000**. The December text is therefore used as a period working-draft witness, not silently promoted to the final published standard.

Its revision history is also useful but must not be mistaken for invention history. Revision `0c`, dated **5 March 1999**, records incorporation of `D99105R0 Self-test log modification` and `D99108R0 Optional pointer on self-test log`. T13's official 1999 document index independently lists those proposals as submitted on **10 February 1999** and **22 February 1999** respectively. This establishes an active 1999 standards-editing episode around self-test logging; it does **not** prove that SMART self-test or diagnostic logging originated in those proposals.

The substantive interface boundary appears in §8.41.4. `SMART EXECUTE OFF-LINE IMMEDIATE` can either collect SMART data in **off-line mode** and save it to device nonvolatile memory, or execute a **self-diagnostic test routine**. Table 34 gives separate subcommands for the SMART off-line routine, Short self-test, Extended self-test, abort, and captive-mode Short/Extended self-tests. The draft therefore does not support treating `off-line data collection` and `self-test` as synonyms.

The execution mode is a second independent axis. In **off-line mode**, command completion occurs **before** the subcommand routine runs; BSY remains clear/DRDY remains set, and an interrupting host command may suspend or abort the routine while still being serviced within two seconds. By contrast, in **captive mode** the device holds BSY while the self-test executes and completes the command only after recording the result. Short and Extended self-tests may use either mode.

This yields a historical interface decomposition:

```text
diagnostic/data-collection request
        -> selected routine
        -> execution mode (off-line or captive)
        -> current execution/progress state
        -> completion/result classification
        -> optional failure localization
        -> bounded retained self-test-log entry
```

The arrows are an **engineering reconstruction of documented relations**, not period terminology for one universal pipeline.

The retained-history boundary is especially explicit in §8.41.6.8.3. The SMART self-test log has **21 descriptor entries** and is a circular buffer: the twenty-second entry replaces the first. A descriptor retains the self-test subcommand, execution status, a `Life timestamp` measured as **device power-on lifetime in hours when that self-test completed**, a failure checkpoint, and a failing LBA when the failure was caused by an uncorrectable sector. If the test passed, or failed for another reason, the failing-LBA field is undefined.

Thus ATA/ATAPI-5 can retain evidence of the device's own diagnostic work, but the interface itself blocks several stronger readings: the log is bounded rather than exhaustive, its timebase is power-on lifetime rather than wall-clock chronology, and not every failed self-test has a meaningful media LBA.

### NVMe 1.0 already separates spare threshold, spare exhaustion, and command failure

The original **NVM Express Revision 1.0 Gold**, ratified **1 March 2011**, already contains the spare-capacity and failure boundary needed for this case; 1.0e is therefore not treated as the first appearance of the mechanism.

In §5.10.1.2 and Figure 59, Revision 1.0 says SMART / Health information is provided over the life of the controller and retained across power cycles. `Available Spare` is a normalized 0–100% measure of remaining spare capacity, while `Available Spare Threshold` may generate an asynchronous event once that reserve falls below the configured threshold. The asynchronous-event table separately names `Spare Below Threshold`.

A different table, the generic command-status definitions, gives `Write Fault` a stronger service consequence: the write data could not be committed to the media, and the specification says this **may** be due to lack of available spare locations. The immediately following `Unrecovered Read Error` is defined separately as read data that could not be recovered from the media.

The historical interface therefore does **not** expose one binary `healthy/dead` transition. It exposes at least three different relations:

```text
remaining spare capacity
        -> threshold crossing / warning
        -> possible exhaustion-related write failure
```

The arrows are an engineering ordering of interface relations, not a claim that every device must traverse a deterministic state machine. In particular, the specification says spare exhaustion **may** cause a Write Fault; it does not say every Write Fault proves spare exhaustion, nor that crossing the warning threshold means the reserve is already exhausted.

This direct 2011 evidence sharpens the ROADMAP failure slice while keeping the implementation boundary intact: NVMe exposes reserve and failure semantics to the host, but does not thereby specify a particular controller's bad-block table, FTL, replacement-pool allocator, NAND defect-growth process, or automatic reassignment algorithm.

### NVMe 1.0e already defines retained health history

The official NVM Express 1.0e specification states in §5.10.1.2 that the SMART / Health Information log provides information `over the life of the controller` and that the information is `retained across power cycles`.

Figure 60 then defines, among other fields:

- `Available Spare` as a normalized percentage of remaining spare capacity;
- `Available Spare Threshold`, whose crossing may cause an asynchronous event;
- `Percentage Used` as a **vendor-specific estimate** of device life used, based on actual usage and the manufacturer's prediction of device life;
- a value of `100` as estimated endurance consumed, explicitly **not necessarily device failure**;
- `Data Units Written` as the amount of host data written to the controller, excluding metadata;
- power-cycle, power-on-hour, unsafe-shutdown, media-error, and lifetime error-log-entry counters.

The specification says `Percentage Used` is updated once per power-on hour while the controller is not asleep. It points to JEDEC JESD218 for SSD life/endurance measurement techniques.

The NVM Express specification archive records the 1.0 family, and the 1.0e front matter says NVMe 1.0 was ratified on 1 March 2011. Therefore this case must not attribute the basic SMART/endurance fields to NVMe 1.3.

### NVMe 1.3 clarifies a mixed temporal regime inside one log page

NVMe 1.3 §5.14.1.2 preserves the same broad SMART/Health model but makes an especially useful distinction explicit: the `Critical Warning` bits represent the **current associated state and are not persistent**.

The same log page still includes cumulative/lifetime quantities such as host data written, power cycles, unsafe shutdowns, media/data-integrity errors, and lifetime error-information entries, while `Percentage Used` remains a vendor-specific life estimate and may exceed 100.

Thus `SMART / Health` is not one uniform kind of memory. It mixes at least:

```text
current condition / warning state
        !=
retained cumulative usage/error history
        !=
model-derived endurance estimate
```

### Intel DC P3700: a named 2014 product witness

Intel's July 2014 `Intel Solid-State Drive DC P3700 Series Product Specification`, order number 330566-002US, states that the P3700 supports the mandatory SMART / Health Information log defined by NVMe 1.0. Its table exposes `Available Spare`, a 10% spare threshold, `Percentage Used Estimate`, and the host data-unit counters. The product document repeats the important boundary that `100` means estimated endurance consumed but may not mean device failure.

The same P3700 product specification also says that a small portion of physical capacity is used for NAND media management and maintenance while the user-addressable LBA count remains stable for the life of the drive. That is product-level evidence that visible logical capacity and hidden maintenance capacity are not the same relation.

The surviving copy used here is an Intel-authored document preserved through manual/document mirrors rather than a current Intel-hosted PDF. The document identity, order number, July 2014 revision, and page transcript are preserved in the grounding record; this provenance is not silently upgraded to a current-vendor URL.

## Retained states and their different meanings

### 1. User payload

Application data addressed through namespaces/LBAs.

### 2. Cumulative host-usage counters

`Data Units Written`, command counts, power cycles, power-on hours, unsafe shutdowns, and related quantities retain summaries of past interaction with the controller.

They are **history-bearing state**, but not a complete event log.

### 3. Error-history counters

The media/data-integrity error count records controller-detected **unrecovered** integrity errors. The lifetime count of Error Information log entries is another retained historical quantity.

Neither is a complete record of every raw cell error or every successful ECC correction.

### 4. Endurance estimate

`Percentage Used` is not defined as a direct physical sensor reading. The standard calls it vendor specific and bases it on actual usage plus the manufacturer's prediction of life.

It is therefore retained/derived **model state about future margin**.

### 5. Spare-capacity state

`Available Spare` represents remaining spare capacity and can be compared with a threshold that can trigger host notification.

This is reserve/maintenance state, not filesystem free space and not application payload.

### 6. Current warning state

By NVMe 1.3, `Critical Warning` is explicitly current and nonpersistent. A device can therefore expose a present warning that differs categorically from its cumulative counters and endurance estimate even though they share one log page.

## Engineering reconstruction

### Same `SMART` label does not imply the same retained schema

ATA-3 and NVMe both expose device-health state to a host, but the inspected contracts are not interchangeable. ATA-3 says the active attribute set and attribute identities are manufacturer-selected and proprietary; NVMe instead standardizes named fields such as `Available Spare`, `Percentage Used`, `Data Units Written`, power-cycle counts, and media/data-integrity error counts.

Therefore:

> **ATA SMART attribute state ≠ NVMe SMART / Health field schema**.

and:

> **shared `SMART` terminology ≠ unchanged semantics or proven implementation genealogy**.

The earlier ATA source is prior art for **retained drive-health state and host-visible reliability qualification**, not evidence that NVMe copied a particular ATA attribute representation or that the two interfaces share one internal health model.

### Monitoring policy state, observed health state, and nonvolatile save are separate relations

ATA-3 preserves SMART enable/disable state and autosave policy across power cycles, while separately describing when updated attribute values are monitored and when they are saved to nonvolatile memory. An enabled autosave policy is therefore not itself a stored attribute value, and enabling SMART is not equivalent to saying that every possible health observation has already been materialized persistently.

Therefore:

> **SMART enabled state ≠ attribute value**,

> **attribute-autosave policy ≠ autosave event ≠ nonvolatile attribute embodiment**.

The command descriptions add a useful counterexample to a passive-observation model: `READ ATTRIBUTE VALUES` and `RETURN STATUS` can cause updated health values to be saved before the host receives data/status. In this bounded ATA contract, observation/reporting can be coupled to **maintenance of the telemetry state itself**.

This still does not mean the attribute records are a complete event history. They compress device-specific conditions into normalized values/status, just as later NVMe counters/estimates compress other aspects of use and degradation.

### Diagnostic trigger, execution mode, completion, verdict, and retained history are separate relations

ATA/ATAPI-5 adds a different kind of non-payload retained state to the earlier ATA-3 attribute/threshold model. The host can initiate a diagnostic routine, but what the command means cannot be reduced to a single `test happened` bit.

First, the draft separates the SMART off-line data-collection routine from Short/Extended self-tests. Second, it separates the **routine** from the **execution mode**: Short/Extended self-tests can run off-line or captive. Third, off-line command completion precedes diagnostic completion, while captive completion follows the test. Therefore:

> **SMART off-line data collection ≠ SMART self-test**,

> **self-test routine ≠ self-test execution mode**,

> **off-line command completion ≠ diagnostic completion**.

`Off-line` also does not mean that the device has become unavailable to the host. The documented off-line protocol keeps the command interface ready and requires many interrupting host commands to be serviced promptly, with the diagnostic work suspended, aborted, or later resumed depending on capability/policy. Therefore:

> **off-line diagnostic execution ≠ host-visible device offline/unavailable**.

The SMART READ DATA structure then keeps capability, progress, and outcome distinct. Separate bits report support for EXECUTE OFF-LINE IMMEDIATE, off-line read scanning, and Short/Extended self-test; the self-test execution byte separately reports approximate percent remaining and classifications such as completed, host-aborted, reset-interrupted, electrical failure, servo/seek failure, read failure, or in-progress. The recommended polling time is only a minimum recommendation before the host should first poll; the draft says actual test time may be several times that value.

Therefore:

> **off-line-data-collection capability ≠ off-line read-scan capability ≠ self-test capability**,

> **self-test progress/status ≠ final pass/fail verdict**,

> **host abort/reset interruption ≠ device-detected diagnostic failure**,

> **recommended polling time ≠ test-completion deadline**.

Finally, the 21-entry circular self-test log retains only a bounded diagnostic trace. It is not a complete event archive, and its `Life timestamp` is a power-on-hour coordinate rather than a civil-time timestamp. A failing LBA is meaningful only for the first uncorrectable sector that caused that particular test to fail; other failure classes need not yield such an address.

Therefore:

> **self-test log entry ≠ complete device event history**,

> **power-on-life timestamp ≠ wall-clock chronology**,

> **self-test failure ≠ universally localized failing LBA**.

This also provides a bounded functional comparison with Cases 101 and 103. ATA off-line self-test, SCSI Background Medium Scan, and host-issued SCSI VERIFY all qualify media/device condition while separating foreground service from maintenance in different ways. Their maintenance loci, triggering rules, scope, result records, and historical vocabularies differ, so the comparison does **not** establish an ATA↔SCSI genealogy.

### The device can retain evidence about its own retention margin

An SSD does not only retain user data. It may also preserve across power cycles enough controller state to report how much work it has seen, how many unsafe power losses occurred, how many unrecovered media/data-integrity errors were detected, how much spare capacity remains, and an estimated fraction of endurance consumed.

Therefore:

> **retained device-health state ≠ retained user payload**.

Yet the distinction does not make health state unimportant. A future administrator, controller, or monitoring system can use it to decide whether a device should remain in service, be replaced, or be investigated.

### `Percentage Used` is an estimate, not a countdown to a deterministic death instant

The specification itself blocks a tempting shortcut: `100` means estimated endurance consumed but may not indicate failure, and the value may exceed 100.

Therefore:

> **100% Percentage Used ≠ device failure**.

and:

> **vendor-specific endurance estimate ≠ direct measurement of every cell's remaining life**.

The field compresses device history and a manufacturer model into an operationally useful scalar. That compression is precisely why it is useful, and precisely why it must not be treated as a complete physical history.

### Host writes are not the physical NAND write history

`Data Units Written` is defined at the host/controller interface: data the host wrote to the controller, excluding metadata. The field is not specified as a count of NAND page programs, block erases, garbage-collection copies, mapping writes, ECC metadata writes, or other internal controller traffic.

Therefore:

> **host Data Units Written ≠ physical NAND program/erase work**.

This matters when comparing the host-visible usage history with the wear mechanisms in Cases 36 and 52. A host counter can be a useful workload witness without being the substrate's complete stress ledger.

### Spare threshold, reserve exhaustion, and service failure are different states

The 2011 command-status wording makes the spare-reserve distinction operational rather than merely descriptive. A controller can report remaining spare capacity; the remaining capacity can fall below a warning threshold; and lack of spare locations can become severe enough that a write cannot be committed. These are different claims.

Therefore:

> **spare below threshold ≠ spare exhausted**.

and:

> **spare exhaustion as a possible Write Fault cause ≠ proof that every Write Fault is a spare-exhaustion event**.

and:

> **Write Fault ≠ Unrecovered Read Error**.

The retention consequence is that **present payload correctness and future repair/continuation margin can diverge**. A device may still serve current data while its hidden reserve for replacing or bypassing future failed locations is shrinking. Conversely, a low-spare warning is not itself evidence that current user payload has already been lost.

This is where Cases 14 and 78 become useful functional comparisons. SCSI grown-defect reassignment and Micron NAND bad-block management directly ground finite replacement pools at lower layers; NVMe 1.0 shows a later host-visible interface that reports remaining spare capacity and can surface a write failure when spare locations are unavailable. The comparison is **not** genealogy, and the NVMe source cannot be used to infer that an SSD implements either earlier mechanism internally.

### Spare capacity is maintenance reserve, not ordinary free user space

The NVMe `Available Spare` field refers to remaining spare capacity. Intel's P3700 separately documents physical capacity reserved for NAND management/maintenance while keeping the logical LBA count stable.

The bounded reconstruction is:

> **spare/maintenance reserve ≠ user-addressable free capacity**.

The P3700 document does not establish that every hidden management byte is counted directly by NVMe `Available Spare`; this case deliberately keeps those quantities distinct.

### Warning state and history state can share an interface without sharing persistence semantics

NVMe 1.3 explicitly says `Critical Warning` bits are current and nonpersistent while the SMART/Health interface also exposes lifetime/cumulative state.

Therefore:

> **current warning state ≠ retained cumulative health history**.

This is a useful counterexample to any assumption that one log page has one temporal ontology.

### A retained counter does not imply a complete archive

`Data Units Written`, unsafe-shutdown count, power-on hours, and error counts summarize categories. They do not preserve order, timing of every event, causal links among events, per-LBA history, or raw internal-media observations.

Therefore:

> **retained lifetime counter ≠ complete device history**.

This is a controller-scale version of the repository's broader `state retention ≠ history retention` distinction, with an important twist: here some **history is intentionally retained**, but only in lossy aggregate form.

### Telemetry cadence and maintenance cadence are separate

NVMe specifies that `Percentage Used` is updated once per power-on hour under the stated condition. That does not mean NAND refresh, garbage collection, wear leveling, bad-block replacement, scrub, read reclaim, or host replacement decisions all run hourly.

Therefore:

> **telemetry update cadence ≠ media-maintenance cadence**.

The field records/updates a model output; it does not itself perform the physical retention work.

## Relation to existing cases

### Case 36 — NAND correct-and-refresh

Case 36 concerns physical error accumulation, ECC margin, and rewrite/refresh policy. Case 55 concerns host-visible retained evidence about overall device use/health. A health estimate may influence operational policy, but it is not the same thing as restoring charge distributions or correction margin.

### Case 38 — Intel PLI self-test validation

Case 38 studies a product-specific capacitor-readiness/self-test path and SMART/event state for power-loss protection. Case 55 is broader and more standardized: generic NVMe health/endurance history. Therefore:

> **generic NVMe SMART/Health telemetry ≠ product-specific PLI readiness validation**.

### Case 52 — NAND read disturb

Case 52 shows that reads can consume physical margin. Case 55's `Data Units Written` field cannot be used as a universal physical-wear ledger, and a write counter in particular does not encode read-hotness/read-disturb history.

### Cases 44 and 47 — sanitization

A drive can report health telemetry while separate erase/sanitize semantics determine whether prior user data remains recoverable. Good health does not prove sanitization; sanitization does not reset the conceptual distinction between payload and health history.

### Cases 48 and 54 — second-order maintenance state

Cassandra `repairedAt` and DDR5 RAA-like state already show non-payload state governing future maintenance. NVMe health telemetry adds a different regime: cumulative/estimated **device aging evidence** that can qualify future service without itself being the payload being preserved.

These are functional comparisons only, not shared genealogy or protocol semantics.

## Failure and forgetting boundaries

Several forms of failure remain distinct:

- user data may be fully readable while `Percentage Used` reaches or exceeds 100;
- spare reserve may fall below threshold before immediate payload loss;
- media/data-integrity errors count only unrecovered events defined by the interface, not every corrected raw error;
- a current `Critical Warning` may clear while cumulative lifetime counters remain;
- a controller can retain aggregated history while forgetting the sequence of events that produced the aggregate;
- the health log itself can be unavailable if the controller cannot operate, even though some NAND embodiments physically survive;
- a healthy-looking interface report does not independently verify hidden physical wear distribution or future failure time.

The repository should therefore reject `SMART says healthy` as a synonym for `all retained payload is safe indefinitely`.

## Prior art and anti-anachronism

NVMe 1.0 was ratified in 2011, and the official 1.0e specification already contains the SMART/Health fields central to this case. Intel's 2014 P3700 product specification explicitly implements the NVMe 1.0 mandatory SMART/Health log.

Accordingly:

> **NVMe 1.3 clarification ≠ invention of NVMe endurance telemetry**.

The bounded value of comparing 1.0e and 1.3 is semantic, not priority-seeking: 1.3 makes the persistence boundary of `Critical Warning` explicit while preserving cumulative and estimated health fields.

The prior-art boundary is now narrower. Official July 1995 T10/SFF evidence establishes publication approval for SFF-8035i, and the January 1997 ATA-3 Revision 7b working draft records the July 1995 incorporation of SFF8035i SMART and directly grounds manufacturer-selected attributes, thresholds, nonvolatile attribute saves, and power-cycle-persistent SMART/autosave policy state. This is enough to reject any NVMe-origin reading of drive-health retention.

It is **not** a full ATA SMART genealogy. The original SFF-8035i facsimile/revision chain, pre-SFF vendor implementations, ATA-4 evolution, proposal-level facsimile archaeology for the 1999 self-test-log changes, later selective/conveyance self-test evolution, named-product diagnostic behavior, and any direct ATA→NVMe design genealogy remain separate work. The December 1999 ATA/ATAPI-5 Revision 2 text closes only a bounded diagnostic-history/interface relation; `proposal submission`, `working-draft incorporation`, `standards publication`, `first implementation`, and `invention` are not treated as synonyms.

## Philosophical interpretation — bounded

This case permits one narrow formulation:

> A technical object can preserve not only a payload but also a compressed account of the conditions under which that payload-bearing object has been used up.

The interesting point is not anthropomorphic `the SSD remembers its age`. Technically, the device retains counters, reserve state, and a model-derived estimate that make past use relevant to future decisions. Some of this history is durable across power cycles; some nearby warning state is explicitly current and nonpersistent.

The case therefore sharpens a distinction between **retaining the thing** and **retaining evidence about the remaining conditions of retention**.

That is a project-level interpretation. It is not terminology attributed to NVM Express or Intel.

## Claim ledger

| Claim | Label | Status |
| --- | --- | --- |
| ATA/ATAPI-5 Revision 2 separates SMART off-line data collection from Short/Extended self-test and permits self-test in off-line or captive mode | `H/P` | strong period working-draft semantics; mirror provenance retained |
| Off-line mode completes the host command before the routine and can service interrupting host commands while the routine is suspended/aborted/resumed | `H/P` | strong period working-draft execution semantics |
| ATA/ATAPI-5 exposes separate current self-test progress/status and distinct capability bits for off-line immediate, off-line read scan, and self-test | `H/P` | strong period working-draft semantics |
| ATA/ATAPI-5 self-test history uses a 21-entry circular log with power-on-life completion timestamp and conditional failing-LBA field | `H/P` | strong period working-draft log semantics |
| 1999 T13 proposal/index and draft-revision evidence proves the invention of SMART self-test or direct ATA→NVMe genealogy | `X` | rejected; revision history is a standards-editing floor only |
| July 1995 X3T10/SFF liaison evidence says a Quantum-submitted SMART copy was approved for publication as SFF-8035i | `H/P` | strong official committee liaison witness; publication floor, not invention proof |
| ATA-3 Revision 7b records that its 26 July 1995 Revision 3 added SFF8035i SMART | `H/P` | strong period working-draft revision history, mirror provenance retained |
| ATA-3 SMART attributes/identities are manufacturer-selected and proprietary, while thresholds are manufacturer-set | `H/P` | strong period working-draft semantics |
| ATA-3 preserves SMART enable state and attribute-autosave policy across power cycles and can save updated attribute values to nonvolatile memory | `H/P` | strong period working-draft command semantics |
| ATA SMART attribute state is historically/technically identical to the later fixed NVMe SMART / Health field schema | `X` | rejected; shared label does not erase interface/schema differences |
| SFF-8035i publication approval or ATA-3 incorporation proves invention priority or direct ATA→NVMe genealogy | `X` | rejected; standards-history floor only |
| NVMe 1.0 Gold already exposes Available Spare, a spare threshold, and a Spare Below Threshold asynchronous-event condition | `H/P` | strong, official 2011 specification |
| NVMe 1.0 `Write Fault` says data could not be committed and lack of spare locations is one possible cause | `H/P` | strong, official 2011 specification |
| `Spare Below Threshold` is not equivalent to reserve exhaustion, and `Write Fault` is not equivalent to `Unrecovered Read Error` | `H/P/E` | strong bounded reconstruction from distinct normative fields/status codes |
| NVMe 1.0e SMART/Health information is described as lifetime information retained across power cycles | `H/P` | strong, official specification |
| NVMe 1.0e defines Available Spare, Percentage Used, host data-unit counters, power/unsafe-shutdown counters, and media-error history | `H/P` | strong, official specification |
| `Percentage Used = 100` may occur without device failure | `H/P` | explicit normative wording |
| `Data Units Written` is host/controller-interface traffic rather than a normative count of internal NAND programs/erases | `H/P/E` | strong bounded reconstruction from field definition |
| NVMe 1.3 explicitly marks Critical Warning bits as current and nonpersistent | `H/P` | strong, official specification |
| Intel DC P3700 2014 implements the mandatory NVMe 1.0 SMART/Health log and exposes the relevant endurance fields | `H/P` | named product document, mirror provenance retained |
| health/endurance state can be retention infrastructure without being payload | `E` | bounded case reconstruction |
| a SMART percentage proves exact remaining lifetime for every physical NAND cell | `X` | rejected by vendor-specific-estimate wording |
| NVMe 1.3 invented SSD health/endurance telemetry | `X` | contradicted by NVMe 1.0e and 2014 P3700 evidence |
| NVMe health telemetry is historically/technically identical to Cassandra repair state or DDR5 RAA | `X` | rejected; functional analogy only |

## Sources

1. NVM Express, **NVM Express Revision 1.0 Gold**, ratified 1 March 2011, especially the generic command-status definitions, asynchronous-event status table, §5.10.1.2, and Figure 59: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0-Gold.pdf>
2. NVM Express, **NVM Express 1.0e**, official specification PDF, especially §5.10.1.2 and Figure 60, printed pp. 67–69: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0e.pdf>
3. NVM Express, **NVM Express Revision 1.3**, official specification PDF, especially §5.14.1.2 and Figure 93, printed pp. 98–100: <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>
4. NVM Express, **Specification Archives**, historical revision index: <https://nvmexpress.org/nvm-express-specification-archives/>
5. Intel, **Intel Solid-State Drive DC P3700 Series Product Specification**, Order Number 330566-002US, July 2014; surviving transcript/mirror used for product-specific tables: <https://manualzilla.com/doc/7195133/intel-dcp3700-1.6tb>
6. NVM Express, **Features for Error Reporting, SMART, Log Pages, Failures and management capabilities in NVMe Architectures**, later institutional explanation used only as operational corroboration, not historical priority evidence: <https://nvmexpress.org/resource/features-for-error-reporting-smart-log-pages-failures-and-management-capabilities-in-nvme-architectures/>

7. X3T10, **Liaison Report from SFF**, `X3T10/95-292r0`, July 1995; official T10 archive, directly inspected facsimile p. 1: <https://www.t10.org/ftp/t10/document.95/95-292r0.pdf>
8. X3T13, **AT Attachment-3 Interface (ATA-3), Working Draft X3T13/2008D Revision 7b**, 27 January 1997; period draft text/transcription used for §6.6 and §7.31 semantics and revision history: <https://paperzz.com/doc/7545036/at-attachment-3-interface--ata-3--working-draft>
9. Technical Committee T13, **1999 document index**, official metadata for `d99105r0` (10 February 1999) and `d99108r0` (22 February 1999), plus the **Expired Standards** ledger identifying project 1321D / ATA/ATAPI-5 and its 28 February 2000 submission date: <https://t13.org/documents?created%5Bmax%5D=1999-12-31&created%5Bmin%5D=1999-01-01&order=field_document_number&page=1&sort=desc> and <https://www.t13.org/standards-expired>
10. T13, **AT Attachment with Packet Interface - 5 (ATA/ATAPI-5), Working Draft T13/1321D Revision 2**, 13 December 1999; period draft transcription/mirror used for revision history and §§8.41.4–8.41.6: <https://studylib.net/doc/25730948/ata-atapi-5>

## Related repositories

A fresh repository search found no dedicated NVMe SMART/endurance or ATA SMART/SFF-8035i/ATA5 self-test case in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). Broader SMART/ATA/NVMe health-monitoring genealogy and disk/SSD engineering chronology should remain there if developed; this case keeps only the retention-specific state/history, diagnostic-history, and interface-boundary distinctions.
