# Enterprise SSD Extended Shutdown: Qualification Window, Powered Maintenance, and Operator Scheduling

## Status

**`grounded`** for the bounded vendor operational-guidance relation described below.

Grounding record: [`../evidence/111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md`](../evidence/111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md).

NetApp rated-life/offline-retention telemetry deepening: [`../evidence/111-netapp-rated-life-offline-retention-telemetry-deepening.md`](../evidence/111-netapp-rated-life-offline-retention-telemetry-deepening.md).

## Scope

- **Object / system:** enterprise SSD/NVMe storage kept powered off for extended periods, as addressed by IBM storage-system support guidance and Dell PowerEdge support guidance.
- **Historical anchor:** an IBM support-content mirror records the extended-shutdown guidance as created on **16 December 2020**; the current IBM support page is marked modified **28 March 2023**.
- **Later continuity / cross-vendor witness:** Dell support article **000198930**, version 3, marked last modified **14 May 2026**.
- **Research question:** what changes when a standards-level power-off retention interval becomes an operator scheduling problem involving backup, environment, powered maintenance opportunity, recommissioning time, and sometimes an explicit read sweep?

This case is a bounded continuation of Case 76's JESD218 SSD endurance/retention qualification relation and Case 37's product-specific powered periodic refresh. It is **not**:

- a new derivation of the JESD218 qualification tables;
- a claim that every enterprise SSD fails exactly at three months;
- a claim that every SSD implements Dell's described background tasks in the same way;
- a claim that merely applying power always completes retention maintenance;
- a claim that a full-device read universally rewrites NAND;
- a controlled endurance/retention experiment;
- a firmware-internals study;
- an archival-storage recommendation for all SSD classes;
- an invention-priority claim for Flash refresh, scrubbing, or powered maintenance.

The bounded retention claim is:

> **A power-off retention qualification interval can be operationalized as a maintenance schedule without becoming the same thing as that schedule. IBM and Dell both warn about extended enterprise-SSD shutdown around the three-month / 40 °C regime, yet prescribe different powered-run intervals. Dell additionally documents powered background retention work and a full-used-NAND read as a trigger for retention tasks. The surviving vendor record therefore separates passive offline survival, maintenance opportunity, maintenance completion, operator policy, and standards qualification.**

`maintenance opportunity`, `operator scheduling`, `offline survival`, and `recommissioning window` are project engineering terms unless explicitly attributed to a source.

## Historical vocabulary

The vendor sources use terms including:

- `extended shutdown` / `prolonged power off`;
- `data retention`;
- `power off` / `powered-up`;
- `end of life`;
- `background tasks`;
- `data retention tasks`;
- `wear-leveling`;
- `read operation`;
- `used NAND cells`;
- `backup`;
- `decommissioned`.

The following are project terms rather than historical vendor vocabulary:

- `qualification window`;
- `maintenance opportunity`;
- `maintenance-completion evidence`;
- `operator retention policy`;
- `fleet-level retention infrastructure`.

## Historical record

### H/P — IBM operationalizes the three-month retention boundary as an earlier power-on schedule

IBM's support article **“Potential for SSD data loss after extended shutdown”** states that the JEDEC enterprise-SSD requirement is a minimum of three months at 40 °C and warns that after prolonged shutdown there is potential for data loss or drive failure. Its operational recommendation is deliberately earlier than that boundary: a system and its enclosed drives should be **powered up for at least two weeks after two months of system power off**. IBM separately recommends recent backups before extended shutdown, maintaining the powered-off environment below 40 °C, and avoiding extended power-off for a drive already reporting end-of-life status.

A surviving IBM support-content mirror records the article as created **16 December 2020**; the current IBM support page records a modified date of **28 March 2023**. The creation timestamp is used only as a publication floor for this support guidance, not as an invention date for the underlying retention concern.

The important historical relation is therefore:

```text
three-month / 40 °C standards background
    !=
IBM operator schedule of two months off + at least two weeks powered
```

IBM presents the latter as conservative operational guidance, not as a redefinition of the JEDEC requirement.

### H/P — Dell explicitly distinguishes powered background retention work from the unpowered interval

Dell's current PowerEdge support article **000198930**, version 3, last modified **14 May 2026**, states that enterprise SSD/NVMe devices perform data-retention tasks while powered and that extended power-off removes the opportunity for those tasks. It additionally says wear-leveling occurs while the drives are powered, whether idle or handling host I/O.

Dell then recommends, for its affected PowerEdge context and “based on current technology,” that SSD/NVMe drives containing user data be **powered up once every 2.5 months for a minimum duration of three weeks** to allow background tasks to complete. Dell adds that larger capacities can require longer powered-on duration.

This is unusually useful because it blocks a common shortcut:

```text
power restored
    !=
retention maintenance demonstrated complete
```

The documented operator action includes **time under power**, not merely a transition from off to on.

### H/P — Dell gives a second maintenance path: read all used NAND cells

The same Dell support article says that, alternatively, **a read operation on all used NAND cells triggers the data-retention tasks**, and recommends that approach for larger-capacity drives.

Within this source's bounded product-support claim, a full read is therefore not described only as passive verification. It can be an **event that triggers device retention work**.

That does not establish that:

- every physical page is rewritten;
- every controller uses the same read-reclaim algorithm;
- every vendor has the same trigger;
- a successful read proves future retention for a specific interval.

The internal implementation remains undisclosed in the inspected Dell source.

### H/P — the two vendors do not publish one universal operator cadence

IBM's surviving guidance says two months off followed by at least two weeks powered. Dell's current guidance says 2.5 months off followed by at least three weeks powered, with longer powered time as capacities increase, or a read sweep over used NAND.

The historical record therefore gives a useful negative result:

> **shared reference to a three-month enterprise retention regime ≠ one standardized operator maintenance schedule**.

The support policies are vendor/system guidance layered above the standards-level qualification relation.


### H/P — NetApp adds a wear-state gate for future long-offline retention

NetApp's May 2021 _ONTAP 9.9.1 EMS Event Catalog_ documents `shm.threshold.ratedLife`, `ratedLife2`, and `ratedLifeMax` events at >90%, >95%, and >100% rated life used. The event descriptions say that at 100% rated life an SSD **might not be able to retain data while powered off for long periods of time**. At 90/95% ONTAP tells the operator to plan replacement as the estimate approaches 100%; above 100% it tells the operator to replace the SSD.

Current `storage disk show -ssd-wear` documentation independently states that `Rated Life Used` is an estimate based on actual usage plus the manufacturer's prediction of device life and that a value greater than 99 means estimated endurance has been used but **does not necessarily indicate device failure**. It exposes spare-block-consumption fields separately.

This creates a third operator-facing relation alongside IBM and Dell:

```text
current payload still serviceable
    !=
future long-power-off retention still trusted
```

and:

```text
rated-life estimate
    !=
immediate failure verdict
```

NetApp does **not** provide the IBM/Dell periodic power-up cadence in the inspected evidence. The bounded addition is a wear-state **admission/replacement policy**, not another documented refresh schedule.

## Engineering reconstruction

### E — qualification interval and maintenance schedule are different relations

Case 76 grounds JESD218's bounded SSD qualification relation at a specified endurance/workload/temperature/use condition. Case 111 adds a different relation: what an operator is told to do when a deployed storage system will remain off long enough to approach that risk window.

```text
qualification condition
    -> states what a rated device must satisfy under a test/use model

operator maintenance schedule
    -> states when to intervene conservatively in a deployed system
```

The schedule can be earlier than the qualification boundary without contradicting it. A maintenance recommendation includes safety margin, fleet uncertainty, environmental uncertainty, time needed for background work, and backup/recommissioning concerns not encoded by one headline retention interval.

### E — passive offline survival and active powered maintenance must be separated

The bounded vendor documentation supports at least three states:

1. **powered off:** NAND must retain enough recoverable state without controller background work;
2. **powered but maintenance incomplete:** the controller has an opportunity to perform work, but Dell's minimum powered-duration language warns against treating power presence as completion evidence;
3. **powered with a prescribed maintenance opportunity:** sufficient run time or a vendor-prescribed read sweep is supplied so retention tasks can execute under the documented policy.

Therefore:

> **unpowered nonvolatility ≠ unpowered maintenance availability**;

and:

> **powered state ≠ proved maintenance completion**.

The first relation is consistent with Case 37's Samsung statement that its product-specific periodic refresh did not run while the drive was powered off. The second is newly sharp at the operator-policy level because Dell assigns a minimum powered duration.

### E — a read sweep can be maintenance-triggering without becoming universal “refresh” semantics

Dell's statement that reading all used NAND cells triggers retention tasks means that, in that bounded support regime:

> **read sweep ≠ verification-only operation**.

But the evidence does not justify the stronger statement:

> `every read refreshes every NAND cell`.

The host action and the hidden device action are different layers. A host issues reads over a logical used-data set; firmware may use the resulting error/age/read evidence to schedule hidden work. The source does not disclose exact physical rewrite geometry, thresholds, or completion telemetry.

### E — maintenance time becomes capacity-sensitive operational infrastructure

Dell says larger-capacity drives require longer powered-on duration for the background tasks. That directly makes **elapsed maintenance opportunity** an operational resource.

The source does not provide a formula, so the defensible result is only:

> **larger capacity can lengthen the prescribed maintenance window**,

not a linear scaling law and not a universal per-terabyte constant.

This is a retention issue that has migrated above the NAND cell: rack power, operator scheduling, system availability, backup state, and time reserved for maintenance can all become part of whether the retained state remains safely serviceable.

### E — “three months” is a risk/qualification boundary, not a deterministic failure clock

Neither the standard-level relation grounded in Case 76 nor the vendor support wording proves that one particular drive becomes unreadable exactly when a clock reaches three months. IBM says there is **potential** for data loss/failure after extended shutdown; Dell says systems powered off for more than three months **may** exhibit errors or faults.

Therefore:

> **retention interval ≠ deterministic individual-drive failure time**.

The practical policy is conservative precisely because actual wear, active-use temperature, power-off temperature, controller state, NAND variation, and maintenance history can differ.

## Cross-case comparison


### Case 55 — NVMe SMART / Health endurance telemetry

Case 55 already grounds model-derived endurance state such as NVMe `Percentage Used` and the rule that 100% estimated endurance consumed need not mean immediate failure. NetApp supplies a storage-system operational continuation: model-derived wear evidence can change warning severity and replacement policy because future long-offline retention is no longer treated as unqualified.

The relation is functional/interface-level only. The evidence does not establish that every NetApp `Rated Life Used` value is literally the NVMe field, nor one ATA/NVMe→ONTAP implementation genealogy.

### Case 76 — JESD218 endurance/retention qualification

Case 76 answers:

> what must remain true at a rated endurance boundary under a specified SSD qualification relation?

Case 111 asks instead:

> how do system vendors turn an extended power-off risk into an operator runbook before or around that boundary?

Thus:

```text
standards qualification
    !=
field maintenance policy
```

The field policy can cite the standard while adding earlier intervention, backup, environment, powered-run duration, and recommissioning rules.

### Case 37 — Samsung 840 EVO periodic refresh

Case 37 gives a named commercial product episode in which Samsung described a powered periodic refresh feature for **old-data read performance** and explicitly said it did not operate while power was off.

Case 111 is not another 840 EVO refresh case. It moves the comparison one level outward: IBM and Dell document **operator-facing shutdown schedules** for enterprise SSD/NVMe systems. The similarity is functional — powered time can be retention infrastructure — while the product, target property, mechanism, and evidence class differ.

### Case 36 — Flash Correct-and-Refresh

Case 36 is a research algorithm/evaluation for maintaining NAND recoverability within ECC margin. Case 111 contains no evidence that IBM or Dell implemented that algorithm. `background retention task`, `read-triggered task`, and academic `FCR` are not synonyms and no genealogy is asserted.

## Prior art and anti-anachronism

No invention-priority claim is made for either support article. The standards relation predates them, and Case 37 already grounds a 2014–2015 commercial SSD maintenance episode in which powered time mattered. The 2020–2026 sources are valuable because they expose **operator-facing policy**: how a storage vendor tells administrators to manage an extended shutdown once nonvolatile media cannot simply be treated as indefinitely passive shelf storage.

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated enterprise-SSD extended-shutdown / powered-maintenance case to reuse. A generic history of SSD retention-management firmware belongs there; this case keeps only the retention-specific distinction among qualification, offline survival, powered maintenance opportunity, operator scheduling, and recommissioning.

## Failure and forgetting boundaries

For this bounded case, distinguish:

- **extended power-off:** controller background work is unavailable;
- **approaching a vendor risk window:** policy calls for backup/environment checks and a powered maintenance interval;
- **power restored:** maintenance becomes possible but is not thereby proved complete;
- **sufficient powered interval or read sweep:** a vendor-prescribed opportunity/trigger is supplied for hidden retention tasks;
- **post-maintenance service:** ordinary operation resumes, without the support article proving a new universal shelf-life guarantee;
- **drive at end of life:** IBM warns against extended power-off, further separating endurance state from calendar time alone.

None of these states proves physical sanitization, permanent archival safety, or future correctness without qualification.

## Functional analogy and philosophical limit

A limited functional analogy is useful: a supposedly “passive” nonvolatile storage system can impose **periodic human scheduling work** because the device's own maintenance machinery cannot operate while unpowered. Retention work can therefore cross an organizational boundary: from cell physics and controller firmware into power planning, backup policy, rack/system availability, and operator time.

This is a project interpretation, not IBM or Dell's historical vocabulary. It must not be generalized into the claim that every act of powering a system is “memory maintenance,” or that operational runbooks are the same mechanism as NAND refresh.

## Claim ledger

| Claim | Type | Evidence strength | Boundary |
| --- | --- | --- | --- |
| IBM support guidance recommends at least two weeks powered after two months off | H/P | strong | IBM affected-system operational guidance, not universal SSD law |
| Dell current guidance recommends every 2.5 months, minimum three weeks powered | H/P | strong | Dell PowerEdge affected-product context; version 3, 14 May 2026 |
| Dell says powered SSD/NVMe performs retention background tasks while extended power-off prevents them | H/P | strong | vendor support description; firmware internals not disclosed |
| Dell says a read over all used NAND cells triggers retention tasks | H/P | strong | bounded Dell claim; does not prove universal read-refresh semantics |
| qualification interval ≠ operator maintenance schedule | E | strong | cross-source decomposition, not source vocabulary |
| power restored ≠ maintenance completion | E | strong | Dell minimum-duration wording supports the distinction |
| same standards background ≠ same vendor cadence | H/E | strong | IBM and Dell prescriptions differ |
| powered maintenance opportunity can become fleet-level retention infrastructure | E/A | medium | useful cross-layer interpretation, not vendor terminology |
| NetApp warns at 90/95% rated life and requires replacement above 100% | H/P | strong | wear-state operator policy; not a deterministic failure threshold |
| NetApp `Rated Life Used >99` means endurance estimate consumed but not necessarily device failure | H/P | strong | directly documented CLI semantic boundary |
| readable now ≠ qualified for long powered-off retention | E | strong | current service and future-offline admission are distinct |
| IBM/Dell guidance demonstrates FCR or Samsung's exact refresh algorithm | X | rejected | no genealogy or implementation identity established |
| three months is a deterministic failure instant for every drive | X | rejected | vendor wording is probabilistic/risk-based and Case 76 is qualification-bounded |

## Open questions

- What was the first publication date of Dell article 000198930 before the surviving version-3 modification date?
- Which named SSD controller/firmware families under Dell's affected systems implement the described read-triggered retention behavior, and how?
- What telemetry, if any, proves that the prescribed background work has completed?
- How does required powered duration scale with capacity and amount of used NAND in the vendor implementation?
- Can independent fault/retention testing validate the IBM/Dell operational windows after rated endurance?
- How do other enterprise vendors beyond the now-grounded NetApp wear-state relation operationalize long powered-off intervals?
- How do these runbooks change across later NAND generations and controller ECC/refresh policies?

## Sources

- IBM Support, **“Potential for SSD data loss after extended shutdown,”** current page modified 28 March 2023: <https://www.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>.
- IBM support-content mirror of the same guidance, showing creation on 16 December 2020: <https://supportcontent.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>.
- Dell Technologies Support, **“PowerEdge: Data Retention Occur with SSD or Nvme Drives Due to Prolonged Power off,”** article 000198930, version 3, last modified 14 May 2026: <https://www.dell.com/support/kbdoc/en-us/000198930/ssd-data-retention-considerations-when-powering-off-systems-for-a-prolonged-duration>.
- NetApp, **ONTAP 9.9.1 EMS Event Catalog**, May 2021, doc `215-15259_A0`: <https://docs.netapp.com/p/ontap/9x/9.9.1/EMS-Event-Catalog.pdf>.
- NetApp, **`shm.threshold events`**: <https://docs.netapp.com/us-en/ontap-ems/shm-threshold-events.html>.
- NetApp, **`storage disk show`** (`-ssd-wear`): <https://docs.netapp.com/us-en/ontap-cli/storage-disk-show.html>.
- Internal standards context: [`Case 76 — JEDEC JESD218 SSD Endurance Qualification`](76-jedec-ssd-endurance-retention-qualification.md).
- Internal commercial-refresh comparison: [`Case 37 — Samsung 840 EVO Old-Data Performance Restoration`](37-samsung-840-evo-old-data-performance-refresh.md).
