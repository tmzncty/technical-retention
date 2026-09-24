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

## Evidence chain

### 1. IBM / Dell extended-shutdown operator policy

[`111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md`](111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md)

**Role:** canonical operator-policy grounding.

Establishes that enterprise-SSD power-off retention guidance can become an operational schedule involving backup, temperature/environment, conservative off-time, powered dwell after extended shutdown, and Dell's alternate full-read trigger path.

```text
JEDEC qualification interval
    != vendor operator schedule

power restored
    != maintenance proven complete
```

### 2. NetApp wear-state gate — current serviceability versus future offline retention

[`111-netapp-rated-life-offline-retention-telemetry-deepening.md`](111-netapp-rated-life-offline-retention-telemetry-deepening.md)

**Role:** operator-facing wear-state / retention-admission boundary.

```text
SSD readable / serviceable now
    != SSD trusted for long future powered-off retention

rated-life estimate
    != immediate failure verdict
```

### 3. IBM ESS — system-level scrub completion witness

[`111-ibm-ess-post-offline-scrub-completion-deepening.md`](111-ibm-ess-post-offline-scrub-completion-deepening.md)

**Role:** strongest currently grounded Case-111 system-level completion signal.

```text
calendar intervention point
    != powered maintenance opportunity
    != named scrub execution
    != observed per-vdisk scrub completion
```

The ESS completion message is authority for the named scrub run only. It does not prove every hidden SSD-internal retention task or every physical NAND cell was refreshed.

### 4. IBM / Lenovo — cadence variance and documentation lineage

[`111-ibm-lenovo-2020-2022-shutdown-cadence-lineage-deepening.md`](111-ibm-lenovo-2020-2022-shutdown-cadence-lineage-deepening.md)

**Role:** vendor/system policy variation and source-lineage guardrail.

```text
standards qualification horizon
    != system intervention schedule
    != automatic scrub admission threshold
    != scrub completion
```

### 5. Seagate Pulsar.2 — 2012 MLC powered retention maintenance

[`111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md`](111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md)

**Role:** named-product first-party powered-maintenance witness and later documentation continuity.

```text
power applied
    -> retention monitoring available
    -> conditional cell rewrite / refresh

no operator-scheduled preventive maintenance
    != no internal maintenance
```

The source does not recover controller thresholds, scan cursor, exact rewrite geometry, or retention-completion telemetry.

### 6. Seagate Pulsar XT.2 — 2011 SLC powered-retention witness

[`111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md`](111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md)

**Role:** directly inspected June-2011 named-product floor for the more explicit conditional-rewrite wording, plus revision-history discipline.

```text
direct Rev. B text — June 2011
    != revision-history continuity inference — March 2011
    != invention / implementation date
```

XT.2 is SLC; later Pulsar.2 is MLC. Similar wording does not prove identical firmware or maintenance mechanism.

### 7. First-generation Seagate Pulsar — 2010 named-product floor

[`111-seagate-pulsar-2010-powered-retention-refresh-prior-art-deepening.md`](111-seagate-pulsar-2010-powered-retention-refresh-prior-art-deepening.md)

**Role:** earliest directly inspected named enterprise-SSD product documentation currently used by Case 111 for powered retention monitoring/refresh.

Direct documentation floor: **5 April 2010**.

```text
shipment date
    != surviving documentation date
    != implementation date
    != invention date
```

### 8. Pulsar XT.2 maintenance observability — BMS/DST versus retention completion

[`111-seagate-xt2-maintenance-observability-boundary-deepening.md`](111-seagate-xt2-maintenance-observability-boundary-deepening.md)

**Role:** device-level observability deepening.

```text
Background Media Scan
    -> status / progress / counts / results

Drive Self Test
    -> persistent result entry
    -> terminal pass / fail / abort semantics

Data Retention monitoring/rewrite
    -> powered monitoring + conditional rewrite documented
    -> no analogous public retention-specific completion surface identified
```

```text
maintenance telemetry exists
    != retention-maintenance completion authority
```

### 9. eMMC 4.41→5.1 — BKOPS maintenance debt, periodic wake-up, and completion scope

[`111-emmc-441-51-bkops-periodic-wakeup-maintenance-cadence-deepening.md`](111-emmc-441-51-bkops-periodic-wakeup-maintenance-cadence-deepening.md)

**Role:** standards/prior-art control-surface deepening; not an enterprise-SSD implementation claim.

JEDEC e.MMC exposes:

- `BKOPS_STATUS` maintenance-debt / urgency levels;
- host-triggered `BKOPS_START`;
- HPI preemption;
- autonomous background-operation control;
- `PERIODIC_WAKEUP` cadence;
- a separate Power Off Notification relation.

```text
BKOPS support
    != current BKOPS debt / urgency
    != BKOPS run admitted
    != BKOPS run completed

BKOPS run complete
    != retention-refresh completion proved
    != power-off preparation complete
    != future offline-retention guarantee
```

### 10. Micron industrial e.MMC — named refresh versus generic BKOPS

[`111-micron-2023-2025-industrial-emmc-refresh-vs-bkops-boundary-deepening.md`](111-micron-2023-2025-industrial-emmc-refresh-vs-bkops-boundary-deepening.md)

**Role:** named commercial product boundary for P6; strengthens rather than closes the retention-specific completion target.

Micron's 32/64/128/256GB industrial e.MMC Rev. F (10/2023) and Rev. I (01/2025) publicly list all of the following on the same product family:

```text
BKOPS control
Auto initiated refresh
Host initiated refresh
```

Rev. I's public ECSD table separately exposes the standard generic background-operation fields:

```text
BKOPS_SUPPORT   [502]
BKOPS_STATUS    [246]
BKOPS_START     [164]
BKOPS_EN        [163]
PERIODIC_WAKEUP [131]
```

but the inspected public datasheet does not identify a refresh-specific progress/completion field and does not state that `BKOPS_STATUS` certifies Micron refresh completion.

Therefore:

```text
same product has BKOPS
    + same product has named refresh
    != BKOPS completion is a refresh-completion certificate

host can initiate refresh
    != public whole-device refresh coverage authority
```

Rev. F also placed explicit retention values on the feature page (1 year at 55°C at maximum PE; 2 years at 55°C at 10% of maximum PE). Rev. I says those retention values were removed from Features while keeping refresh features documented. Treat that as documentation lineage, not a physical-behavior transition.

---

## Unified evidence model

### A. Standards / product / operator layers

```text
retention qualification relation
    -> named product has powered maintenance / refresh
    -> long shutdown removes maintenance opportunity
    -> vendor/system publishes conservative operator cadence
```

This is a cross-layer operationalization chain, not a genealogy claim.

### B. Opportunity, obligation, execution, completion

```text
power available
    != maintenance debt absent
    != maintenance admitted
    != maintenance running
    != generic maintenance complete
    != retention-specific refresh complete
```

IBM ESS supplies a system-level named scrub-completion witness. eMMC supplies a generic maintenance-run completion relation. The new Micron product witness shows that a product can name refresh separately while still leaving the public BKOPS→refresh completion binding unestablished.

### C. Observability is subsystem- and maintenance-class-specific

```text
maintenance telemetry exists
    != every maintenance class is separately observable

named refresh capability exists
    != refresh progress / coverage / terminal result is publicly exposed
```

### D. Current health versus future offline admission

```text
current readable payload
    != remaining endurance estimate
    != future long-offline retention qualification
```

### E. Maintenance cadence versus maintenance meaning

```text
configured wake cadence
    -> obligation to provide a maintenance opportunity
    -> generic bounded run may have completion evidence

but:
generic run completion
    != source-identified retention-refresh completion
```

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

Case 36 provides a research mechanism/evaluation. Seagate or Micron refresh wording does not establish that exact algorithm.

### Case 67 — read reclaim / OCP `Refresh Counts`

Reuse: [`67-2020-2025-ocp-refresh-count-semantics-deepening.md`](67-2020-2025-ocp-refresh-count-semantics-deepening.md).

```text
counter increment
    != whole-device coverage completion
```

### Case 135 — automotive eMMC self-refresh

Useful counterexample to generic-BKOPS overreach:

```text
generic background-maintenance completion
    != retention-specific self-refresh completion
```

The Micron evidence now provides an independent named-product reason to keep those classes separate unless a source explicitly binds them.

### Case 150 — managed-SSD garbage collection

Functional comparison only:

```text
eMMC BKOPS completion
    != M550 GC completion
    != M550 map publication
    != M550 erase completion
```

### Case 20 — storage-interface shutdown state machines

Power Off Notification is functionally comparable to other host/device shutdown handshakes because it separates host intent from device-side completion/readiness. No protocol genealogy is asserted.

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
- JEDEC e.MMC exposes BKOPS obligation/urgency, execution control, periodic wake-up, and separate power-off coordination;
- Micron industrial e.MMC Rev. F / Rev. I name `BKOPS control`, `Auto initiated refresh`, and `Host initiated refresh` separately;
- Micron's public ECSD table exposes generic BKOPS fields but does not publicly label one as refresh-specific completion authority.

### Engineering reconstruction

Project terms include:

- `maintenance opportunity`;
- `maintenance debt`;
- `maintenance urgency`;
- `maintenance admission`;
- `maintenance activity/progress evidence`;
- `maintenance completion evidence`;
- `maintenance-class attribution`;
- `retention-specific completion authority`;
- `operator completion authority`;
- `power-removal authority`;
- `offline-retention admission`.

These organize source relations; they are not retroactively attributed to the vendors, JEDEC, OCP, or Linux developers.

### Functional analogy

Useful analogies compare where work is admitted, observed, preempted, scheduled, and declared complete. They do not establish shared implementation or ancestry.

### Philosophical interpretation

A narrow permissible interpretation is that maintenance can be technically real, invocable, and still only partially observable at the public interface. Do not turn that into a universal claim that all firmware-local work is unknowable.

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

same product supports BKOPS + refresh
    != BKOPS completion identifies refresh completion

host-initiated refresh
    != public whole-device coverage certificate

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

Find a first-party **named SSD/NVMe/SAS/eMMC device** interface where a host-visible field is explicitly tied to completion or whole-device coverage of **retention refresh / data-retention maintenance itself**.

The evidentiary bar is now stronger:

```text
generic background-work completion
    != retention-specific completion

and

same product naming BKOPS + refresh
    != source-level binding between them
```

A source must bind visible completion evidence to the retention-maintenance obligation being claimed.

### P2 — Dell affected-drive implementation mapping

Identify controller/firmware families under Dell article 000198930 and determine whether Dell's read-all-used-NAND procedure maps to a vendor-defined telemetry/result surface.

### P3 — powered-duration scaling

Find first-party engineering evidence explaining how maintenance time scales with capacity, used NAND, wear state, temperature history, and controller/background scheduling.

### P4 — earliest Dell publication floor

Recover the first publication date/revision lineage of Dell article 000198930 before the surviving version-3 modification date.

### P5 — controlled device-level experiment

Where hardware is available, correlate power-on dwell, full-read sweep, maintenance counters/logs, and subsequent offline-retention behavior under an exact product/firmware/environment boundary.

### P6 — named commercial eMMC maintenance-class binding

**Partially sharpened, not closed.** The Micron industrial e.MMC family now proves that a named commercial product can publicly expose generic BKOPS and separately name host/auto refresh, while the public datasheet still does not bind `BKOPS_STATUS` or completed BKOPS to refresh completion.

The remaining target is therefore narrower:

> Find a first-party product manual, vendor command specification, or host-visible status/result definition that explicitly says a particular BKOPS terminal state, vendor status bit, progress field, or completion code corresponds to retention-refresh / data-refresh completion or coverage.

---

## Reuse boundary

Fresh companion searches found no dedicated Micron e.MMC refresh packet in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) during this pass.

Broader histories of Micron embedded-flash generations, eMMC/MMC standards evolution, JEDEC proposal/ballot history, Linux MMC host-stack evolution, product adoption, vendor-specific commands, and eMMC→UFS maintenance interfaces belong primarily in `computing-archaeology` if pursued.

Case 111 should remain focused on retention qualification, powered maintenance, operator policy, observability, completion scope, and future-offline admission.

---

## Current status

**Case 111 remains `grounded`.**

The Micron product slice materially improves the product-level prior-art boundary: the same named product family publicly exposes both generic BKOPS and separately named refresh features, but the inspected public interface still does not establish retention-specific completion authority.

No maturity promotion is justified. The highest-value next evidence remains a named first-party host-visible terminal state or coverage indicator explicitly bound to retention refresh itself.
