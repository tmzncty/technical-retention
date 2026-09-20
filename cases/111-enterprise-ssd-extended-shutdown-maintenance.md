# Enterprise SSD Extended Shutdown: Qualification Window, Powered Maintenance, and Operator Scheduling

## Status

**`grounded`** for the bounded vendor operational-guidance relation described below.

Grounding record: [`../evidence/111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md`](../evidence/111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md).

NetApp rated-life/offline-retention telemetry deepening: [`../evidence/111-netapp-rated-life-offline-retention-telemetry-deepening.md`](../evidence/111-netapp-rated-life-offline-retention-telemetry-deepening.md).

IBM ESS post-offline scrub-completion deepening: [`../evidence/111-ibm-ess-post-offline-scrub-completion-deepening.md`](../evidence/111-ibm-ess-post-offline-scrub-completion-deepening.md).

IBM / Lenovo shutdown-cadence and documentation-lineage deepening: [`../evidence/111-ibm-lenovo-2020-2022-shutdown-cadence-lineage-deepening.md`](../evidence/111-ibm-lenovo-2020-2022-shutdown-cadence-lineage-deepening.md).

Seagate Pulsar.2 2012 powered retention-refresh prior-art deepening: [`../evidence/111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md`](../evidence/111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md).

Seagate Pulsar XT.2 2011 powered-retention prior-art / revision-history deepening: [`../evidence/111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md`](../evidence/111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md).

Seagate first-generation Pulsar 2010 powered-retention prior-art deepening: [`../evidence/111-seagate-pulsar-2010-powered-retention-refresh-prior-art-deepening.md`](../evidence/111-seagate-pulsar-2010-powered-retention-refresh-prior-art-deepening.md).

## Scope

- **Object / system:** enterprise SSD/NVMe storage kept powered off for extended periods, as addressed by IBM storage-system support guidance and Dell PowerEdge support guidance.
- **Earlier product-level prior-art witness:** Seagate's first-generation Pulsar SATA Product Manual, Rev. A, dated **5 April 2010**, directly documents powered firmware/hardware cell monitoring / refresh while separately specifying typical one-year power-off retention at 25 °C and saying preventive maintenance is not required. A September-2009 shipment date from Seagate is commercialization chronology only and is not used to back-project the April-2010 maintenance wording.
- **Later, more explicit product-level witness:** Seagate's Pulsar XT.2 SAS Product Manual, Rev. B, June 2011, directly documents powered cell monitoring / refresh and conditional rewrite. Its revision table supports a weaker continuity inference to the March-2011 Rev. A lineage; direct Rev. A text remains uninspected.
- **Historical anchor for the operator-runbook layer:** an IBM support-content mirror records the extended-shutdown guidance as created on **16 December 2020**; the current IBM support page is marked modified **28 March 2023**.
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

> **A power-off retention qualification interval can be operationalized as a maintenance schedule without becoming the same thing as that schedule. A directly inspected Seagate enterprise-SSD product manual documented powered firmware/hardware monitoring / refresh by 5 April 2010 while separately specifying unpowered retention and requiring no routine preventive maintenance from the operator. Later Seagate manuals expose a more explicit conditional-rewrite relation, while IBM and Dell later turn extended shutdown into operator-facing powered-run policies. The surviving record therefore separates passive offline survival, autonomous device maintenance, maintenance opportunity, maintenance completion, operator policy, standards qualification, and the source-critical difference among commercialization date, documentation date, revision-history inference, and implementation/invention date.**

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

## IBM ESS follow-up — post-offline scrub and operator-visible completion

A bounded ESS-specific follow-up is now grounded in [`evidence/111-ibm-ess-post-offline-scrub-completion-deepening.md`](../evidence/111-ibm-ess-post-offline-scrub-completion-deepening.md).

IBM's _Spectrum Scale RAID Frequently Asked Questions and Answers_ goes beyond the generic instruction to restore power after an extended SSD shutdown. For an SSD-based ESS system powered off for two months, it tells the operator to power the system on **to allow the disk scrubbing process to complete a run**, and gives an `mmfs` completion message — `End scrubbing tracks of ...` — to be observed for each vdisk in each declustered array. The same FAQ separately gives a time-based recommendation of at least two weeks powered after two months off.

This sharpens the case's maintenance state machine:

```text
calendar intervention point
    != powered maintenance opportunity
    != named scrub execution
    != observed per-vdisk scrub completion
```

The evidence remains system-layer evidence. A Spectrum Scale RAID scrub completion message does **not** prove that every NAND cell was read or rewritten, does not expose drive-firmware refresh thresholds, and does not establish that every hidden device-local retention task is complete. The same IBM passage separately prescribes **Sanitize with Block Erase** when drives are to be cleared for later reuse, so `scrub complete != sanitize complete` is directly preserved in the vendor record.

## IBM / Lenovo follow-up — cadence variance, automatic scrub admission, and documentation lineage

A second bounded follow-up is now grounded in [`evidence/111-ibm-lenovo-2020-2022-shutdown-cadence-lineage-deepening.md`](../evidence/111-ibm-lenovo-2020-2022-shutdown-cadence-lineage-deepening.md).

The December 2020–May 2022 first-party record shows that even **inside IBM** the same three-month / 40 °C background did not yield one operator cadence. The generic IBM flash says two months off followed by at least two weeks powered; the TS7770 notice says two months off followed by at least one week powered; the December 2020 ESS 5000 Redbook says at least one week powered every six weeks off. A later ESS alert returns to the two-month / two-week guidance but also says that, after more than seven days powered off following installation, ESS automatically starts a background scrub that reads data and rewrites only when it finds a problem.

Thus the maintenance clocks themselves must be kept distinct:

```text
standards qualification horizon
    != product/system intervention schedule
    != automatic scrub-admission threshold
    != scrub completion
```

The same deepening also cautions against treating Lenovo's January 2021 HT511702 page as an automatically independent third-vendor engineering witness. It closely tracks the IBM generic flash in title, wording, `chdrive` command vocabulary, and cadence, and it covers a Storwize-for-Lenovo product family for which Lenovo's own product documentation explicitly uses the name **IBM Storwize V7000 for Lenovo**. The bounded historical conclusion is documentation / platform-lineage continuity, not proof of independent engineering discovery or one shared firmware implementation.

## Seagate Pulsar.2 follow-up — powered autonomous retention work predates the operator-runbook layer

A third bounded follow-up is now grounded in [`evidence/111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md`](../evidence/111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md).

Seagate's **Pulsar.2 SAS Product Manual, Rev. B, April 2012** gives a typical powered-off retention value of three months at 40 °C and says the SSD contains firmware / hardware features that can monitor and refresh memory cells while power is applied. Its `6.2.5 Data Retention` section is more specific: while powered, SSD-cell retention is monitored and cells are rewritten if levels decay to an unexpected level.

The same manual says `Preventive maintenance: None required` and later `No routine scheduled preventive maintenance is required`.

That combination establishes a responsibility boundary that the later operator runbooks make visible from the other side:

```text
no routine operator-scheduled preventive maintenance
    !=
no controller-local retention maintenance

power applied
    -> autonomous monitor / conditional rewrite capability available
    !=
maintenance completion proved
```

A Seagate 1200.2 SAS SSD manual from October 2016 repeats the same broad powered monitoring / rewrite relation and the no-routine-scheduled-maintenance statement. It is a documentation-continuity witness only; it does not establish identical firmware, thresholds, NAND, or scheduler.

The April-2012 Pulsar.2 witness remains useful as later MLC documentation continuity. It no longer sets Case 111's earliest directly inspected product-level floor.

## Seagate Pulsar XT.2 follow-up — direct 2011 floor and revision-history boundary

A fourth bounded follow-up is now grounded in [`evidence/111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md`](../evidence/111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md).

Seagate's **Pulsar XT.2 SAS Product Manual, Rev. B, June 2011** identifies the product's media as SLC NAND Flash. The same first-party manual gives a typical powered-off retention figure of three months at 40 °C, says that powered firmware / hardware can monitor and refresh cells, and states in its dedicated `Data Retention` subsection that powered cells are monitored and conditionally rewritten when their levels decay unexpectedly. It also says no routine scheduled preventive maintenance is required.

This moved the directly inspected named-product powered-retention-maintenance floor in Case 111 from April 2012 to June 2011 before the first-generation Pulsar source below moved it earlier again.

The XT.2 revision table adds a deliberately different evidence category. It records Rev. A on **16 March 2011** as the initial release and says the **1 June 2011** Rev. B changed only sheet 34 for a 7 mm weight correction. The retention passages inspected in Rev. B are on printed pp. 14 and 16. This supports a **revision-history continuity inference** to the March-2011 lineage, but a direct Rev. A facsimile was not inspected, so March 2011 is not treated as direct wording evidence or as an invention date.

The later Pulsar.2 revision table supplies the useful counterexample: Pulsar.2 Rev. A is dated 11 August 2011, but Rev. B's April-2012 change list explicitly includes p. 14, where the later `Data Retention` section resides. The inspected 2012/2013 wording therefore cannot be silently back-projected into Pulsar.2 Rev. A. This sharpens the repository's source rule:

```text
directly inspected wording
    !=
revision-history-supported continuity
    !=
feature invention / implementation priority
```

The product comparison is also bounded. XT.2 documents SLC NAND; Pulsar.2 documents MLC NAND. Similar broad powered-monitor / conditional-rewrite language across both products supports documentation-level continuity, not proof of one controller, firmware, sensing metric, threshold, scheduler, rewrite geometry, or genealogy.

Neither Seagate manual establishes an IBM/Dell-style operator cadence. The earlier product-level maintenance witness therefore does **not** move the explicit operator-runbook floor back to 2011.

## Seagate first-generation Pulsar follow-up — direct April-2010 floor

A fifth bounded follow-up is grounded in [`evidence/111-seagate-pulsar-2010-powered-retention-refresh-prior-art-deepening.md`](../evidence/111-seagate-pulsar-2010-powered-retention-refresh-prior-art-deepening.md).

Seagate's first-generation **Pulsar Product Manual**, publication `100596473`, Rev. A, is dated April 2010 and its revision history records **5 April 2010** as the initial release. It identifies SLC NAND Flash and gives a typical powered-off retention value of **one year at 25 °C**. The same reliability material says retention degrades with NAND use and temperature, but that when power is applied the SSD contains firmware and hardware features able to **monitor and refresh memory cells**. In the same table, `Preventive maintenance` is `None required`.

This moves Case 111's directly inspected named-enterprise-SSD documentation floor from June 2011 to **5 April 2010**:

```text
offline retention specification
    + powered firmware/hardware monitor-refresh capability
    + no operator preventive-maintenance requirement
```

A Seagate corporate announcement from 7 December 2009 says Pulsar revenue shipments to selected OEMs began in **September 2009**. That date is retained only as commercialization chronology. The April-2010 maintenance wording is not back-projected into 2009:

```text
commercialization date
    != documentation date
    != implementation / invention date
```

The 2010 wording is also less specific than XT.2/Pulsar.2. It does **not** directly establish the later explicit conditional rewrite when cell levels decay unexpectedly, nor a page/block relocation primitive, host-read trigger, whole-device sweep, cadence, or completion signal. The later manuals remain stronger witnesses for those narrower claims.

Finally, the product numbers cannot be compared naively: the first-generation Pulsar's `1 year @ 25 °C` and XT.2/Pulsar.2's `3 months @ 40 °C` are specified under different temperatures and product/media contexts. They do not support a claim that the earlier product intrinsically retained data longer.

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

The IBM / Lenovo cadence deepening makes the same distinction stronger: even one vendor's surviving 2020 documentation maps the same standards-level background onto different schedules for different system contexts. `operator cadence` is therefore a system-policy relation, not a universal NAND physical constant.

The Seagate follow-ups add a separate product layer: by April 2010 a named SSD manual already exposed powered autonomous monitoring / refresh without exposing any operator cadence at all. Thus `device-local maintenance capability != field runbook`.

### E — passive offline survival and active powered maintenance must be separated

The bounded vendor documentation supports at least three states:

1. **powered off:** NAND must retain enough recoverable state without controller background work;
2. **powered but maintenance incomplete:** the controller has an opportunity to perform work, but Dell's minimum powered-duration language warns against treating power presence as completion evidence;
3. **powered with a prescribed maintenance opportunity:** sufficient run time or a vendor-prescribed read sweep is supplied so retention tasks can execute under the documented policy.

Therefore:

> **unpowered nonvolatility ≠ unpowered maintenance availability**;

and:

> **powered state ≠ proved maintenance completion**.

The Seagate 2010–2012 records give direct named-product support for the first distinction: cell monitoring / refresh is explicitly conditioned on power being applied. The second remains newly sharp at the operator-policy level because Dell assigns a minimum powered duration and IBM exposes a separate system-level scrub completion witness.

### E — a read sweep can be maintenance-triggering without becoming universal “refresh” semantics

Dell's statement that reading all used NAND cells triggers retention tasks means that, in that bounded support regime:

> **read sweep ≠ verification-only operation**.

But the evidence does not justify the stronger statement:

> `every read refreshes every NAND cell`.

The host action and the hidden device action are different layers. A host issues reads over a logical used-data set; firmware may use the resulting error/age/read evidence to schedule hidden work. The source does not disclose exact physical rewrite geometry, thresholds, or completion telemetry.

Seagate's earlier manuals do not say their retention monitoring is triggered by a host read sweep, so the mechanisms must not be merged from functional similarity alone.

### E — maintenance time becomes capacity-sensitive operational infrastructure

Dell says larger-capacity drives require longer powered-on duration for the background tasks. That directly makes **elapsed maintenance opportunity** an operational resource.

The source does not provide a formula, so the defensible result is only:

> **larger capacity can lengthen the prescribed maintenance window**,

not a linear scaling law and not a universal per-terabyte constant.

This is a retention issue that has migrated above the NAND cell: rack power, operator scheduling, system availability, backup state, and time reserved for maintenance can all become part of whether the retained state remains safely serviceable.

### E — “three months” is a risk/qualification boundary, not a deterministic failure clock

Neither the standard-level relation grounded in Case 76 nor the vendor support wording proves that one particular drive becomes unreadable exactly when a clock reaches three months. IBM says there is **potential** for data loss/failure after extended shutdown; Dell says systems powered off for more than three months **may** exhibit errors or faults. The later Seagate Pulsar XT.2 and Pulsar.2 manuals likewise present three months at 40 °C as a typical product retention specification, not a deterministic individual-unit failure timestamp.

The first-generation Pulsar's one-year-at-25 °C figure is a different bounded product condition, not evidence against the later three-month-at-40 °C relation and not a universal shelf-life guarantee.

Therefore:

> **retention interval ≠ deterministic individual-drive failure time**.

The practical policy is conservative precisely because actual wear, active-use temperature, power-off temperature, controller state, NAND variation, and maintenance history can differ.

The ESS `>7 days off -> automatic scrub` rule sharpens this further: a maintenance-admission threshold is not a failure threshold. It can cause proactive re-observation and selective repair well before the longer offline-risk window.

## Cross-case comparison

### Case 55 — NVMe SMART / Health endurance telemetry

Case 55 already grounds model-derived endurance state such as NVMe `Percentage Used` and the rule that 100% estimated endurance consumed need not mean immediate failure. NetApp supplies a storage-system operational continuation: model-derived wear evidence can change warning severity and replacement policy because future long-offline retention is no longer treated as unqualified.

The relation is functional/interface-level only. The evidence does not establish that every NetApp `Rated Life Used` value is literally the NVMe field, nor one ATA/NVMe→ONTAP implementation genealogy.

### Case 76 — JESD218 endurance/retention qualification

Case 76 answers:

> what must remain true at a rated endurance boundary under a specified SSD qualification relation?

Case 111 asks instead:

> how do named products and system vendors turn retention into powered device work and, later, an operator runbook before or around that boundary?

Thus:

```text
standards qualification
    !=
named-product autonomous maintenance
    !=
field maintenance policy
```

The field policy can cite the standard while adding earlier intervention, backup, environment, powered-run duration, and recommissioning rules. The IBM-internal cadence variance shows that one standards background can support multiple product/system runbooks without implying multiple underlying retention standards; the Seagate witnesses show that a product can also perform powered retention work without exposing such a runbook.

### Case 37 — Samsung 840 EVO periodic refresh

Case 37 gives a named commercial product episode in which Samsung described a powered periodic refresh feature for **old-data read performance** and explicitly said it did not operate while power was off.

The Seagate Pulsar / XT.2 / Pulsar.2 witnesses are earlier and enterprise-oriented, but they are not evidence that these Seagate products and 840 EVO use the same mechanism. The shared functional statement is only that powered controller work can renew or protect NAND-resident state. The product class, NAND class, symptom framing, thresholds, schedule, and genealogy differ or remain undisclosed.

Case 111 then moves the comparison one level outward: IBM and Dell document **operator-facing shutdown schedules** for enterprise SSD/NVMe systems. Powered device maintenance and human scheduling can therefore occupy different responsibility layers.

### Case 36 — Flash Correct-and-Refresh

Case 36 is a research algorithm/evaluation for maintaining NAND recoverability within ECC margin. Neither the Seagate Pulsar-family manuals nor the IBM/Dell field guidance establishes that those products implement that algorithm. `monitor and refresh memory cells`, `background retention task`, `read-triggered task`, `background scrub`, and academic `FCR` are not synonyms and no genealogy is asserted.

### Case 67 — OCP Refresh Counts terminology boundary

Case 67 grounds OCP `Refresh Counts` as an integrity-maintenance block-reallocation accounting category. The first-generation Pulsar manual's `refresh memory cells` wording is a product-level retention-maintenance description, not a telemetry definition.

Therefore:

```text
same label “refresh”
    != same unit of work
    != same controller primitive
    != same telemetry semantics
```

No genealogy is asserted between the 2010 product wording and later OCP accounting vocabulary.

## Prior art and anti-anachronism

No invention-priority claim is made for any of these product or support documents. The standards relation predates the later operator runbooks, and the Seagate record now supplies a **directly inspected named enterprise-SSD product-level powered-maintenance witness by 5 April 2010**. Seagate's 7-December-2009 product announcement separately says revenue shipments began in September 2009, but that commercialization chronology does not make the April-2010 maintenance wording a 2009 direct-documentation fact. The XT.2 record remains useful because it supplies stronger conditional-rewrite wording and a separate revision-history lesson. Case 37 separately grounds a 2014–2015 commercial client-SSD maintenance episode in which powered time mattered. The 2020–2026 sources remain valuable for a different historical object: **operator-facing policy** that tells administrators how to manage an extended shutdown once nonvolatile media cannot simply be treated as indefinitely passive shelf storage.

The Seagate chronology does not prove direct ancestry to Samsung, IBM, Dell, NetApp, or OCP. It also illustrates why document dates must be handled case by case: shipment date, public announcement, surviving manual date, revision-history inference, and invention/implementation date are separate categories. The Lenovo deepening adds a parallel source-critical caution: a second corporate masthead is not automatically a second independent technical witness. Lenovo HT511702 closely follows the IBM generic support wording and sits inside an explicit IBM Storwize-for-Lenovo product/document lineage. It is useful historical evidence of policy propagation, but should not be double-counted as independent validation unless a separate engineering basis is recovered.

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Pulsar`, publication `100596473`, `Pulsar XT.2`, and the existing extended-shutdown terms found no dedicated packet to reuse. A generic history of Seagate enterprise SSDs, SSD retention-management firmware, SLC/MLC product evolution, or the IBM Storwize / ESS / TS7700 platform genealogy belongs there; this case keeps only the retention-specific distinctions among qualification, offline survival, powered controller maintenance, maintenance opportunity, maintenance admission, operator scheduling, recommissioning, and source-chronology evidence strength.

## Failure and forgetting boundaries

For this bounded case, distinguish:

- **extended power-off:** controller background work is unavailable;
- **powered autonomous-maintenance capability:** in the Seagate product witnesses, controller monitoring / refresh becomes available without a routine operator maintenance schedule;
- **short offline-history trigger:** in the named ESS alert, more than seven days off after installation admits an automatic background scrub on return;
- **approaching a vendor risk window:** policy calls for backup/environment checks and a powered maintenance interval;
- **power restored:** maintenance becomes possible but is not thereby proved complete;
- **sufficient powered interval or read sweep:** a vendor-prescribed opportunity/trigger is supplied for hidden retention tasks;
- **named scrub completion:** in the separate ESS FAQ evidence, per-vdisk completion can be observed at the system layer;
- **post-maintenance service:** ordinary operation resumes, without the support article proving a new universal shelf-life guarantee;
- **drive at end of life:** IBM warns against extended power-off, further separating endurance state from calendar time alone.

None of these states proves physical sanitization, permanent archival safety, or future correctness without qualification.

## Functional analogy and philosophical limit

A limited functional analogy is useful: a supposedly “passive” nonvolatile storage system can contain **autonomous powered maintenance** below the user-visible interface and, under long shutdown conditions, can later impose **periodic human scheduling work** because that maintenance machinery cannot operate while unpowered. Retention work can therefore cross an organizational boundary: from cell physics and controller firmware into power planning, backup policy, rack/system availability, and operator time.

The Seagate witnesses make the interface boundary especially visible: `Preventive maintenance: None required` or `No routine scheduled preventive maintenance` can coexist with explicit powered monitoring / refresh inside the device. The 2010 source now shows this relation directly before the later manuals' more explicit conditional-rewrite wording. The later cadence evidence then shows that institutions can place several clocks around one material risk: qualification horizon, scrub-admission threshold, operator intervention point, powered dwell, and completion evidence. The source chronology adds another historiographical clock: commercialization, surviving text, inferred prior revision, and invention/implementation dates are not interchangeable. This is a project interpretation, not Seagate, IBM, Lenovo, Dell, NetApp, or OCP's philosophical vocabulary. It must not be generalized into the claim that every act of powering a system is “memory maintenance,” or that operational runbooks are the same mechanism as NAND refresh.

## Claim ledger

| Claim | Type | Evidence strength | Boundary |
| --- | --- | --- | --- |
| Seagate first-generation Pulsar Rev. A is directly dated April 2010 and records 5 April 2010 as initial release | H/P | strong | first-party Seagate manual; documentation date only |
| First-generation Pulsar uses SLC NAND Flash | H/P | strong | named 2010 product family only |
| 2010 Pulsar specifies typical one-year power-off retention at 25 °C | H/P | strong | bounded product condition; not directly comparable with later 3mo@40°C figures |
| 2010 Pulsar says powered firmware/hardware can monitor and refresh memory cells | H/P | strong | exact trigger, geometry, scheduler and primitive undisclosed |
| 2010 Pulsar says preventive maintenance is not required | H/P | strong | operator-facing requirement; does not negate controller-local maintenance |
| Seagate says Pulsar revenue shipments to selected OEMs began in September 2009 | H/P | strong | commercialization chronology only |
| September-2009 shipment date proves April-2010 maintenance wording already existed | X | rejected | no inspected 2009 source establishes the wording |
| Seagate Pulsar XT.2 Rev. B is a June 2011 named enterprise-SSD product witness | H/P | strong | directly inspected first-party document; later, more explicit wording |
| Pulsar XT.2 uses SLC NAND Flash | H/P | strong | named product only |
| XT.2 says powered firmware / hardware can monitor and refresh memory cells and §6.2.5 describes conditional rewrite | H/P | strong | exact sensing metric, threshold, cadence, and geometry undisclosed |
| XT.2 says no routine scheduled preventive maintenance is required | H/P | strong | operator requirement; does not negate controller-local maintenance |
| XT.2 Rev. A is recorded as 16 March 2011 and Rev. B says only sheet 34 changed | H/P | strong | revision-history fact |
| XT.2 retention wording therefore likely continues from Rev. A | H/E | medium-strong | revision-history inference; direct Rev. A text not inspected |
| `March 2011 revision-lineage inference = direct wording / invention date` | X | rejected | evidential categories remain separate |
| Pulsar.2 Rev. B changed p. 14, where the later Data Retention section resides | H/P | strong | blocks automatic unchanged-wording back-projection to Rev. A |
| Pulsar.2 Rev. A therefore lacked powered retention maintenance | X | rejected | change list establishes page change, not feature absence |
| Seagate Pulsar.2 Rev. B is an April 2012 named enterprise-SSD product witness | H/P | strong | later MLC documentation continuity, not earliest direct floor |
| Pulsar.2 says powered firmware / hardware can monitor and refresh memory cells | H/P | strong | exact metric, threshold and scheduler undisclosed |
| Pulsar.2 says powered cell state is monitored and rewritten when levels decay unexpectedly | H/P | strong | conditional behavior, not continuous whole-device rewrite |
| Pulsar.2 says no routine scheduled preventive maintenance is required | H/P | strong | operator requirement; does not negate controller-local maintenance |
| `same broad SLC/MLC wording = same controller algorithm` | X | rejected | documentation similarity does not establish implementation identity or genealogy |
| `no scheduled preventive maintenance = no internal maintenance` | X | rejected | contradicted by the Seagate manuals |
| `power applied = retention maintenance complete` | X | rejected | no completion telemetry / dwell contract in inspected Seagate sources |
| IBM support guidance recommends at least two weeks powered after two months off | H/P | strong | IBM affected-system operational guidance, not universal SSD law |
| IBM TS7770 notice recommends at least one week powered after two months off | H/P | strong | TS7770 / FC 8081 context |
| IBM ESS 5000 Redbook recommends at least one week powered every six weeks off | H/P | strong | December 2020 ESS 5000 first-edition guidance |
| IBM ESS alert automatically starts a background scrub after >7 days off after installation | H/P | strong | named ESS behavior; trigger threshold != failure threshold |
| IBM ESS alert says the scrub reads data and rewrites only if it finds a problem | H/P | strong | system-layer statement, not proof of NAND-page geometry |
| Lenovo HT511702 recommends at least two weeks powered after two months off | H/P | strong | Lenovo V-series / Storwize-for-Lenovo support context |
| Lenovo HT511702 is automatically an independent third-vendor engineering validation | X | rejected | wording, command, date, and Storwize-for-Lenovo lineage argue against automatic double-counting |
| Dell current guidance recommends every 2.5 months, minimum three weeks powered | H/P | strong | Dell PowerEdge affected-product context; version 3, 14 May 2026 |
| Dell says powered SSD/NVMe performs retention background tasks while extended power-off prevents them | H/P | strong | vendor support description; firmware internals not disclosed |
| Dell says a read over all used NAND cells triggers retention tasks | H/P | strong | bounded Dell claim; does not prove universal read-refresh semantics |
| qualification interval ≠ autonomous device maintenance ≠ operator maintenance schedule | E | strong | cross-source decomposition, not source vocabulary |
| same standards background ≠ one IBM field cadence | H/E | strong | 2020 IBM generic, TS7770, and ESS 5000 schedules differ |
| automatic maintenance trigger ≠ operator intervention schedule ≠ completion | E | strong | coexisting ESS rules plus separate completion evidence |
| power restored ≠ maintenance completion | E | strong | Seagate capability wording, Dell minimum-duration wording and IBM scrub-completion evidence support the distinction |
| powered maintenance opportunity can become fleet-level retention infrastructure | E/A | medium | useful cross-layer interpretation, not vendor terminology |
| NetApp warns at 90/95% rated life and requires replacement above 100% | H/P | strong | wear-state operator policy; not a deterministic failure threshold |
| NetApp `Rated Life Used >99` means endurance estimate consumed but not necessarily device failure | H/P | strong | directly documented CLI semantic boundary |
| readable now ≠ qualified for long powered-off retention | E | strong | current service and future-offline admission are distinct |
| Seagate / IBM / Dell guidance demonstrates FCR or Samsung's exact refresh algorithm | X | rejected | no genealogy or implementation identity established |
| `refresh memory cells` in 2010 Pulsar == OCP `Refresh Counts` telemetry semantics | X | rejected | product maintenance wording and telemetry accounting are different evidence objects |
| three months is a deterministic failure instant for every drive | X | rejected | product/vendor wording is qualification/risk-bounded |

## Open questions

- What was the first publication date of Dell article 000198930 before the surviving version-3 modification date?
- Which named SSD controller/firmware families under Dell's affected systems implement the described read-triggered retention behavior, and how?
- What telemetry, if any, proves that the prescribed background work has completed outside the now-grounded ESS system-level scrub witness?
- How does required powered duration scale with capacity and amount of used NAND in the vendor implementation?
- Can independent fault/retention testing validate the IBM/Dell operational windows after rated endurance?
- What engineering rationale produced the one-week / two-week / six-week cadence differences across the 2020 IBM documents?
- Was Lenovo HT511702 mechanically syndicated, contractually inherited, or separately reissued from a shared Storwize support corpus?
- Can a direct Pulsar XT.2 Rev. A (16 March 2011) facsimile verify the retention-bearing pp. 14/16 wording that Rev. B's sheet-34-only change record implies was already present?
- What exactly changed on Pulsar.2's retention-bearing p. 14 between the uninspected August-2011 Rev. A and April-2012 Rev. B?
- Which **pre-5-April-2010** named enterprise-SSD manuals, if any, publish comparable powered retention-monitoring / refresh behavior?
- Can September–December 2009 Pulsar engineering or product documentation directly establish the powered maintenance wording without back-projecting the 2010 manual?
- What exact monitoring signal, trigger, coverage policy, and rewrite primitive sat behind first-generation Pulsar's `monitor and refresh memory cells` statement?
- Beyond the now-grounded Seagate product-level powered-refresh capability and NetApp wear-state relation, which vendors publish explicit long-offline operator cadences or completion telemetry?
- How do these runbooks change across later NAND generations and controller ECC/refresh policies?

## Sources

- Seagate Technology LLC, **_Pulsar Product Manual_**, publication 100596473, Rev. A, April 2010: <https://www.seagate.com/content/dam/seagate/migrated-assets/staticfiles/support/disc/manuals/ssd/100596473a.pdf>.
- Seagate, **“Seagate introduces its First Solid State Drive: Pulsar,”** 7 December 2009: <https://investors.seagate.com/news/news-details/2009/Seagate-introduces-its-First-Solid-State-Drive-Pulsar/default.aspx>.
- Seagate Technology, **_Pulsar XT.2 SAS Product Manual_**, publication 100647497, Rev. B, June 2011: <https://www.seagate.com/staticfiles/support/docs/manual/sas/100647497b.pdf>.
- Seagate Technology, **_Pulsar.2 SAS Product Manual_**, publication 100666271, Rev. B, April 2012: <https://www.seagate.com/files/www-content/product-content/pulsar-fam/pulsar/pulsar-2/en-us/docs/100666271b.pdf>.
- Seagate Technology, **_Pulsar.2 SAS Product Manual_**, publication 100666271, Rev. C, March 2013 (revision-history comparator): <https://www.seagate.com/files/www-content/product-content/pulsar-fam/pulsar/pulsar-2/en-us/docs/100666271c.pdf>.
- Seagate Technology, **_1200.2 SAS SSD Product Manual_**, Rev. D, October 2016: <https://www.seagate.com/content/dam/seagate/migrated-assets/www-content/product-content/ssd-fam/1200-ssd/en-us/docs/1200-2-sas-ssd-product-manual-100773817d.pdf>.
- IBM Support, **“Potential for SSD data loss after extended shutdown,”** current page modified 28 March 2023: <https://www.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>.
- IBM support-content mirror of the same guidance, showing creation on 16 December 2020: <https://supportcontent.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>.
- IBM Support, **“TS7770 with FC 8081 may experience issues when being powered off for more than three months,”** first published 17 December 2020: <https://www.ibm.com/support/pages/node/6382550>.
- IBM Redbooks, **_Implementation Guide for IBM Elastic Storage System 5000_**, SG24-8498-00, First Edition, December 2020: <https://www.redbooks.ibm.com/redbooks/pdfs/sg248498.pdf>.
- Lenovo Support, **HT511702 — “Potential for SSD data loss after extended shutdown,”** original publication 24 January 2021: <https://support.lenovo.com/za/en/solutions/ht511702>.
- Lenovo Press, **TIPS1302 — “IBM Storwize V7000 for Lenovo”**: <https://lenovopress.lenovo.com/tips1302-ibm-storwize-v7000-for-lenovo>.
- IBM Support, **“IBM ESS Alert : Potential for SSD data loss after extended shutdown,”** modified 23 May 2022: <https://www.ibm.com/support/pages/ibm-ess-alert-potential-ssd-data-loss-after-extended-shutdown>.
- Dell Technologies Support, **“PowerEdge: Data Retention Occur with SSD or Nvme Drives Due to Prolonged Power off,”** article 000198930, version 3, last modified 14 May 2026: <https://www.dell.com/support/kbdoc/en-us/000198930/ssd-data-retention-considerations-when-powering-off-systems-for-a-prolonged-duration>.
- NetApp, **ONTAP 9.9.1 EMS Event Catalog**, May 2021, doc `215-15259_A0`: <https://docs.netapp.com/p/ontap/9x/9.9.1/EMS-Event-Catalog.pdf>.
- NetApp, **`shm.threshold events`**: <https://docs.netapp.com/us-en/ontap-ems/shm-threshold-events.html>.
- NetApp, **`storage disk show`** (`-ssd-wear`): <https://docs.netapp.com/us-en/ontap-cli/storage-disk-show.html>.
- Internal standards context: [`Case 76 — JEDEC JESD218 SSD Endurance Qualification`](76-jedec-ssd-endurance-retention-qualification.md).
- Internal commercial-refresh comparison: [`Case 37 — Samsung 840 EVO Old-Data Performance Restoration`](37-samsung-840-evo-old-data-performance-refresh.md).
