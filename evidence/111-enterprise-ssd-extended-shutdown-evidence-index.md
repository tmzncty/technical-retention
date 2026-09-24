# Case 111 Evidence Index — Enterprise SSD Extended Shutdown Maintenance

Canonical case: [`../cases/111-enterprise-ssd-extended-shutdown-maintenance.md`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md)

**Current maturity:** `grounded`

This is a navigation and evidence-boundary aid. `CASE_INDEX.md` remains the repository-wide maturity ledger.

The current Case-111 package deliberately separates:

```text
standards retention qualification
    != named-product powered retention machinery
    != operator shutdown cadence
    != maintenance opportunity
    != maintenance obligation / urgency
    != maintenance activity / progress
    != bounded-run completion
    != power-removal authority
    != retention-specific completion authority
    != future offline-retention guarantee
```

---

## 1. IBM / Dell extended-shutdown operator policy

[`111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md`](111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md)

**Role:** canonical operator-policy grounding.

Establishes that enterprise-SSD power-off retention guidance can become an operational schedule involving backup, temperature/environment, conservative off-time, powered dwell after extended shutdown, and Dell's alternate full-read trigger path.

Core boundary:

```text
JEDEC qualification interval
    != vendor operator schedule

power restored
    != maintenance proven complete
```

---

## 2. NetApp wear-state gate — current serviceability versus future offline retention

[`111-netapp-rated-life-offline-retention-telemetry-deepening.md`](111-netapp-rated-life-offline-retention-telemetry-deepening.md)

**Role:** operator-facing wear-state / retention-admission boundary.

```text
SSD readable / serviceable now
    != SSD trusted for long future powered-off retention

rated-life estimate
    != immediate failure verdict
```

This is a replacement/admission policy, not another periodic refresh cadence.

---

## 3. IBM ESS — system-level scrub completion witness

[`111-ibm-ess-post-offline-scrub-completion-deepening.md`](111-ibm-ess-post-offline-scrub-completion-deepening.md)

**Role:** strongest currently grounded Case-111 system-level completion signal.

```text
calendar intervention point
    != powered maintenance opportunity
    != named scrub execution
    != observed per-vdisk scrub completion
```

The ESS completion message is authority for the named scrub run only. It does not prove every hidden SSD-internal retention task or every physical NAND cell was refreshed.

---

## 4. IBM / Lenovo — cadence variance and documentation lineage

[`111-ibm-lenovo-2020-2022-shutdown-cadence-lineage-deepening.md`](111-ibm-lenovo-2020-2022-shutdown-cadence-lineage-deepening.md)

**Role:** vendor/system policy variation and source-lineage guardrail.

```text
standards qualification horizon
    != system intervention schedule
    != automatic scrub admission threshold
    != scrub completion
```

It also prevents closely related IBM/Lenovo documentation from being double-counted as automatically independent engineering witnesses.

---

## 5. Seagate Pulsar.2 — 2012 MLC powered retention maintenance

[`111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md`](111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md)

**Role:** named-product first-party powered-maintenance witness and later documentation continuity.

```text
power applied
    -> retention monitoring available
    -> conditional cell rewrite / refresh
```

while the same product family says no routine scheduled preventive maintenance is required.

```text
no operator-scheduled preventive maintenance
    != no internal maintenance
```

The source does not recover controller thresholds, scan cursor, exact rewrite geometry, or retention-completion telemetry.

---

## 6. Seagate Pulsar XT.2 — 2011 SLC powered-retention witness and revision-history boundary

[`111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md`](111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md)

**Role:** directly inspected June-2011 named-product floor for the more explicit conditional-rewrite wording, plus revision-history discipline.

```text
direct Rev. B text — June 2011
    != revision-history continuity inference — March 2011
    != invention / implementation date
```

XT.2 is SLC; later Pulsar.2 is MLC. Similar wording does not prove identical firmware or maintenance mechanism.

---

## 7. First-generation Seagate Pulsar — 2010 named-product floor

[`111-seagate-pulsar-2010-powered-retention-refresh-prior-art-deepening.md`](111-seagate-pulsar-2010-powered-retention-refresh-prior-art-deepening.md)

**Role:** earliest directly inspected named enterprise-SSD product documentation currently used by Case 111 for powered retention monitoring/refresh.

Direct documentation floor: **5 April 2010**.

```text
shipment date
    != surviving documentation date
    != implementation date
    != invention date
```

The September-2009 shipment date is commercialization chronology only.

---

## 8. Pulsar XT.2 maintenance observability — BMS/DST versus retention completion

[`111-seagate-xt2-maintenance-observability-boundary-deepening.md`](111-seagate-xt2-maintenance-observability-boundary-deepening.md)

**Role:** device-level observability deepening.

The same June-2011 SSD that documents powered retention monitoring/rewrite also exposes explicit host-visible state for other subsystems:

```text
Background Media Scan
    -> status
    -> progress
    -> scan counts
    -> results / errors

Drive Self Test
    -> persistent result entry
    -> terminal pass / fail / abort semantics

Data Retention monitoring/rewrite
    -> powered monitoring + conditional rewrite documented
    -> no analogous public retention-specific completion surface identified
```

Bounded result:

```text
maintenance telemetry exists
    != retention-maintenance completion authority
```

This packet reuses Case 67's OCP result rather than duplicating it: counted integrity-maintenance activity does not prove whole-device refresh coverage completion.

---

## 9. eMMC 4.41→5.1 — BKOPS maintenance debt, periodic wake-up, and completion scope

[`111-emmc-441-51-bkops-periodic-wakeup-maintenance-cadence-deepening.md`](111-emmc-441-51-bkops-periodic-wakeup-maintenance-cadence-deepening.md)

**Role:** standards/prior-art control-surface deepening; not an enterprise-SSD implementation claim.

JEDEC's revision history places Background Operations and HPI in the 4.41 change set. The 5.1 standard then exposes a much richer generic maintenance relation:

```text
BKOPS support
    != current BKOPS debt / urgency
    != BKOPS run admitted
    != BKOPS run completed
```

The interface provides:

- `BKOPS_STATUS` levels from no operation required through critical outstanding maintenance;
- host-triggered `BKOPS_START`;
- HPI preemption of an unfinished background operation;
- autonomous background-operation control in the 5.1 interface;
- `PERIODIC_WAKEUP`, which can require the host to wake the device at a configured cadence and let at least one BKOPS run finish **without interruption** before powering down again;
- a separate Power Off Notification completion relation.

The key Case-111 boundary is:

```text
maintenance cadence can be interface-defined
    != cadence proves work ran
    != generic BKOPS completion proves retention-refresh completion
```

and:

```text
BKOPS run complete
    != power-off preparation complete
    != future offline-retention guarantee
```

This evidence therefore sharpens, rather than closes, the open retention-specific completion target.

---

## Evidence-chain summary

### Chain A — standards / product / operator layers

```text
SSD retention qualification relation
    -> named product has powered internal retention maintenance
    -> long shutdown removes maintenance opportunity
    -> vendor/system publishes conservative operator cadence
```

This is a cross-layer operationalization chain, not a genealogy claim.

### Chain B — opportunity, obligation, execution, completion

```text
power available
    != maintenance debt absent
    != maintenance admitted
    != maintenance running
    != maintenance complete
```

The eMMC BKOPS evidence adds an explicit interface-level obligation/urgency and bounded-run completion relation; IBM ESS supplies a system-level named scrub completion witness.

Neither proves retention-specific whole-device refresh completion for a named enterprise SSD.

### Chain C — observability is subsystem-specific

```text
same SSD may expose
    BMS progress/result
    + DST terminal result
    + autonomous retention monitoring/rewrite

therefore:
maintenance observability is not all-or-nothing
```

The eMMC comparison adds a second version of the same lesson at interface level:

```text
generic background-maintenance completion observable
    != hidden maintenance class individually identified
```

### Chain D — current health versus future offline admission

```text
current readable payload
    != remaining endurance estimate
    != future long-offline retention qualification
```

NetApp supplies the strongest operator-facing wear-state gate in the current Case-111 evidence set.

### Chain E — maintenance cadence versus maintenance meaning

```text
configured wake cadence
    -> obligation to provide a maintenance opportunity
    -> required bounded run may have completion evidence

but:
completion of generic maintenance class
    != completion of retention-specific maintenance class
```

This is the main addition from the eMMC standards slice.

---

## Cross-case links

### Case 76 — JESD218 endurance / retention qualification

Case 111 operationalizes a standards-level retention relation. It does not replace or rederive Case 76.

```text
qualification relation
    != maintenance mechanism
    != field runbook
```

### Case 37 — Samsung 840 EVO powered old-data maintenance

Functional comparison only: powered controller work can renew NAND-resident state. No controller, NAND, cadence, trigger, or genealogy identity is asserted.

### Case 36 — Flash Correct-and-Refresh

Case 36 provides a research mechanism/evaluation. Seagate `monitor / refresh / rewrite` wording and generic eMMC BKOPS do not establish that exact algorithm.

### Case 67 — read reclaim / OCP `Refresh Counts`

Reuse: [`67-2020-2025-ocp-refresh-count-semantics-deepening.md`](67-2020-2025-ocp-refresh-count-semantics-deepening.md).

```text
OCP SMART-10
    = integrity-maintenance block-reallocation accounting

OCP background refresh
    = whole-device powered-on coverage obligation

counter increment
    != whole-device coverage completion
```

### Case 135 — automotive eMMC self-refresh

Useful counterexample to generic-BKOPS overreach:

```text
generic background-maintenance completion
    != retention-specific self-refresh completion
```

unless a named product source explicitly binds the two.

### Case 150 — managed-SSD garbage collection

Case 150 studies reclaim/erase scheduling and power-loss boundaries. eMMC BKOPS is useful only as functional prior art for host-visible managed-Flash maintenance scheduling.

```text
eMMC BKOPS completion
    != M550 GC completion
    != M550 map publication
    != M550 erase completion
```

No eMMC→M550 genealogy is claimed.

### Case 20 — storage-interface shutdown state machines

Power Off Notification is functionally comparable to other host/device shutdown handshakes because it separates host intent from device-side completion/readiness. No protocol genealogy is asserted here.

---

## Historical / engineering / analogy / interpretation separation

### Historical / source record

Safe source-level claims include:

- named vendor manuals/support documents publish the listed operator/product behaviors;
- Seagate Pulsar-family manuals document powered retention monitoring/refresh;
- XT.2 supports BMS status/results and DST result reporting;
- IBM/Dell publish extended-shutdown procedures;
- IBM ESS exposes a named scrub-completion message;
- NetApp exposes rated-life/offline-retention policy;
- JEDEC eMMC exposes BKOPS obligation/urgency, execution control, periodic wake-up, and separate power-off coordination.

### Engineering reconstruction

Project terms include:

- `maintenance opportunity`;
- `maintenance debt`;
- `maintenance urgency`;
- `maintenance admission`;
- `maintenance activity/progress evidence`;
- `maintenance completion evidence`;
- `operator completion authority`;
- `power-removal authority`;
- `offline-retention admission`.

These organize source relations; they are not retroactively attributed to Seagate, IBM, Dell, Lenovo, NetApp, JEDEC, OCP, or Linux developers.

### Functional analogy

Useful analogies compare where work is admitted, observed, preempted, scheduled, and declared complete. They do not establish shared implementation or ancestry.

### Philosophical interpretation

A narrow permissible interpretation is that long-term availability can depend on maintenance obligations whose visibility and authority change across device, interface, system, and operator layers.

Do not turn that into a claim that every powered interval is maintenance, every counter is proof, or every hidden background task is equivalent.

---

## Explicit anti-collapse rules

```text
three-month qualification
    != three-month deterministic failure instant

power-on
    != retention refresh complete

read sweep
    != every cell rewritten

BMS complete
    != retention maintenance complete

DST passed
    != future offline retention guaranteed

Refresh Counts increased
    != whole-device refresh coverage proved

BKOPS_STATUS = 0
    != every retention-sensitive cell freshly rewritten

BKOPS run complete
    != retention-refresh completion proved

PERIODIC_WAKEUP configured
    != required work already executed

Power Off Notification complete
    != retention refresh complete

scrub completion message
    != all SSD firmware-local maintenance complete

rated life consumed
    != immediate device failure

no scheduled preventive maintenance
    != no internal maintenance

same vendor/product family
    != same firmware mechanism
```

---

## Open debt priority

### P1 — retention-specific device completion authority

Find a first-party **named SSD/NVMe/SAS device** interface where a host-visible field is explicitly tied to completion or whole-device coverage of **retention refresh / data-retention maintenance itself**.

The eMMC slice makes the evidentiary bar clearer:

```text
generic background-work completion
    != retention-specific completion
```

A source must bind the visible completion evidence to the retention-maintenance obligation being claimed.

### P2 — Dell affected-drive implementation mapping

Identify controller/firmware families under Dell article 000198930 and determine whether Dell's read-all-used-NAND procedure maps to a vendor-defined telemetry/result surface.

### P3 — powered-duration scaling

Find first-party engineering evidence explaining how maintenance time scales with capacity, used NAND, wear state, temperature history, and controller/background scheduling.

Dell says larger capacities can require longer powered time; the implementation relation remains unresolved.

### P4 — earliest Dell publication floor

Recover the first publication date/revision lineage of Dell article 000198930 before the surviving version-3 modification date.

This is source chronology, not mechanism evidence.

### P5 — controlled device-level experiment

Where hardware is available, correlate power-on dwell, full-read sweep, maintenance counters/logs, and subsequent offline-retention behavior under an exact product/firmware/environment boundary.

### P6 — named commercial eMMC maintenance-class binding

Find a first-party product manual in which a specific `BKOPS_STATUS` / completed BKOPS run is explicitly tied to a named hidden maintenance class such as retention refresh, reclamation, wear leveling, or bad-block management.

This is a product-interface question, not permission to infer every BKOPS implementation from JEDEC's generic maintenance contract.

---

## Reuse boundary

Fresh repository searches found no dedicated `BKOPS` packet in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) during this pass.

Broader histories of SCSI Background Media Scan, SAS SSD diagnostics, eMMC/MMC standards evolution, JEDEC proposal/ballot history, Linux MMC host-stack evolution, mobile-storage product adoption, and eMMC→UFS maintenance interfaces belong primarily in `computing-archaeology` if pursued.

Case 111 should remain focused on retention qualification, powered maintenance, operator policy, observability, completion scope, and future-offline admission.

---

## Current status

**Case 111 remains `grounded`.**

The new eMMC standards slice adds a strong generic maintenance-cadence/completion counterexample but does **not** satisfy the retention-specific device-completion requirement and therefore does not justify maturity promotion.

The most valuable next evidence remains:

> **a named first-party SSD/NVMe/SAS interface that explicitly tells the host when retention-specific maintenance or its whole-device coverage obligation is complete.**
