# Case 111 Evidence Index — Enterprise SSD Extended Shutdown Maintenance

Canonical case: [`../cases/111-enterprise-ssd-extended-shutdown-maintenance.md`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md)

**Current maturity:** `grounded`

This index is a navigation and evidence-boundary aid. It does not replace `CASE_INDEX.md` as the repository-wide maturity ledger, and it does not promote Case 111 beyond the canonical `grounded` status.

The evidence chain is intentionally split because several superficially similar claims belong to different technical layers:

```text
standards retention qualification
    != named-product powered retention machinery
    != operator shutdown cadence
    != powered maintenance opportunity
    != maintenance activity telemetry
    != maintenance progress
    != bounded-run completion evidence
    != future offline-retention guarantee
```

---

## 1. Grounding — IBM / Dell extended-shutdown operator policy

[`111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md`](111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md)

**Role:** canonical operator-policy grounding.

Establishes that enterprise-SSD power-off retention guidance can become an operational schedule involving:

- backup;
- temperature/environment;
- maximum or conservative off-time;
- powered dwell after extended shutdown;
- Dell's alternate full-read trigger path.

Core boundary:

```text
JEDEC qualification interval
    != vendor operator schedule
```

and:

```text
power restored
    != maintenance proven complete
```

---

## 2. NetApp wear-state gate — current serviceability versus future offline retention

[`111-netapp-rated-life-offline-retention-telemetry-deepening.md`](111-netapp-rated-life-offline-retention-telemetry-deepening.md)

**Role:** operator-facing wear-state / retention-admission boundary.

NetApp's rated-life telemetry adds a distinct relation:

```text
SSD readable / serviceable now
    !=
SSD trusted for long future powered-off retention
```

The evidence is a wear-state replacement/admission policy, not another periodic refresh cadence.

---

## 3. IBM ESS — system-level scrub completion witness

[`111-ibm-ess-post-offline-scrub-completion-deepening.md`](111-ibm-ess-post-offline-scrub-completion-deepening.md)

**Role:** strongest currently grounded operator-visible completion signal in Case 111.

IBM ESS guidance distinguishes:

```text
calendar intervention point
    != powered maintenance opportunity
    != named scrub execution
    != observed per-vdisk scrub completion
```

The completion message is authority for the named ESS scrub run only. It does not prove that every hidden SSD-internal retention task or every physical NAND cell was refreshed.

---

## 4. IBM / Lenovo — cadence variance and documentation lineage

[`111-ibm-lenovo-2020-2022-shutdown-cadence-lineage-deepening.md`](111-ibm-lenovo-2020-2022-shutdown-cadence-lineage-deepening.md)

**Role:** vendor/system policy variation and source-lineage guardrail.

The record shows multiple operator clocks around the same broad three-month/40 °C retention background:

```text
standards qualification horizon
    != system intervention schedule
    != automatic scrub admission threshold
    != scrub completion
```

It also prevents double-counting closely related IBM/Lenovo documentation as automatically independent engineering witnesses.

---

## 5. Seagate Pulsar.2 — 2012 MLC powered retention maintenance

[`111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md`](111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md)

**Role:** named-product first-party powered-maintenance witness and later documentation continuity.

The surviving manual documents:

```text
power applied
    -> retention monitoring available
    -> conditional cell rewrite / refresh
```

while also saying no routine scheduled preventive maintenance is required.

This supports:

```text
no operator-scheduled preventive maintenance
    != no internal maintenance
```

It does not recover controller thresholds, scan cursor, exact rewrite geometry, or completion telemetry.

---

## 6. Seagate Pulsar XT.2 — 2011 SLC powered-retention witness and revision-history boundary

[`111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md`](111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md)

**Role:** directly inspected June-2011 named-product floor for the more explicit conditional-rewrite wording, plus source-critical revision reasoning.

The packet separates:

```text
direct Rev. B text — June 2011
    != revision-history continuity inference — March 2011
    != invention / implementation date
```

Pulsar XT.2 is SLC; later Pulsar.2 is MLC. Similar broad product wording does not prove identical controller firmware or maintenance mechanism.

---

## 7. First-generation Seagate Pulsar — 2010 named-product floor

[`111-seagate-pulsar-2010-powered-retention-refresh-prior-art-deepening.md`](111-seagate-pulsar-2010-powered-retention-refresh-prior-art-deepening.md)

**Role:** earliest directly inspected named enterprise-SSD product documentation currently used by Case 111 for powered retention monitoring/refresh.

The direct documentation floor is **5 April 2010**.

A September-2009 shipment date is commercialization chronology only and is not used to back-project the April-2010 maintenance wording.

Core source-critical boundary:

```text
shipment date
    != surviving documentation date
    != implementation date
    != invention date
```

---

## 8. Pulsar XT.2 maintenance observability — BMS/DST versus retention completion

[`111-seagate-xt2-maintenance-observability-boundary-deepening.md`](111-seagate-xt2-maintenance-observability-boundary-deepening.md)

**Role:** device-level observability deepening; narrows the open completion-telemetry question.

The same June-2011 named SSD that documents powered retention monitoring/rewrite also exposes explicit host-visible state for other subsystems:

```text
Background Media Scan
    -> current status
    -> progress
    -> scan counts
    -> error/result entries

Drive Self Test
    -> nonvolatile result record
    -> explicit terminal pass/fail/abort semantics

Data Retention monitoring/rewrite
    -> powered monitoring + conditional rewrite documented
    -> no analogous public retention-specific completion surface identified
```

This closes only a narrow question:

```text
Does XT.2 expose maintenance telemetry at all?
    -> yes

Does that make retention-refresh completion observable?
    -> not from the inspected public interface material
```

Key engineering boundary:

```text
maintenance telemetry exists
    != retention-maintenance completion authority
```

The packet also reuses Case 67's OCP result rather than duplicating it: a cumulative integrity-maintenance counter can prove counted activity without proving whole-device refresh coverage completion.

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

### Chain B — maintenance opportunity versus completion

```text
power available
    -> controller maintenance can run
    != maintenance has run
    != maintenance has covered all required state
    != bounded maintenance run is complete
```

IBM ESS currently provides the clearest Case-111 system-level completion witness for its named scrub.

### Chain C — observability is subsystem-specific

```text
same SSD
    + BMS status/progress/counts
    + DST persistent terminal result
    + autonomous retention monitoring/rewrite

therefore:
maintenance observability is not all-or-nothing
```

The public interface can make one maintenance process legible while leaving another without a documented completion token.

### Chain D — current health versus future offline admission

```text
current readable payload
    != remaining endurance estimate
    != future long-offline retention qualification
```

NetApp supplies the strongest operator-facing wear-state gate in the current Case-111 evidence set.

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

Useful only as a functional comparison that powered controller work can renew NAND-resident state. No controller, NAND, cadence, trigger, or genealogy identity is asserted.

### Case 36 — Flash Correct-and-Refresh

Case 36 provides a research mechanism/evaluation. Seagate `monitor / refresh / rewrite` wording does not establish that exact algorithm.

### Case 67 — read reclaim / OCP `Refresh Counts`

Reuse: [`67-2020-2025-ocp-refresh-count-semantics-deepening.md`](67-2020-2025-ocp-refresh-count-semantics-deepening.md).

Case 67 establishes:

```text
OCP SMART-10
    = integrity-maintenance block-reallocation accounting

OCP background refresh
    = whole-device powered-on coverage obligation
```

but:

```text
counter increment
    != whole-device coverage completion
```

This is directly useful to Case 111's observability question without duplicating the OCP technical-history packet.

### Case 150 — managed-SSD garbage collection

Case 150 studies reclaim/erase scheduling and power-loss boundaries. Functional similarity is limited to hidden controller work and maintenance opportunity. GC completion, erase completion, and retention-refresh completion are distinct authorities.

---

## Historical / engineering / analogy / interpretation separation

### Historical / source record

Safe historical claims include:

- named vendor manuals and support documents publish the listed operator/product behaviors;
- Seagate Pulsar-family manuals document powered retention monitoring/refresh;
- XT.2 supports BMS status/results and DST result reporting;
- IBM/Dell publish extended-shutdown procedures;
- IBM ESS exposes a named scrub-completion message;
- NetApp exposes rated-life/offline-retention policy.

### Engineering reconstruction

Project terms include:

- `maintenance opportunity`;
- `maintenance activity evidence`;
- `maintenance progress evidence`;
- `maintenance completion evidence`;
- `operator completion authority`;
- `offline-retention admission`.

These terms organize source relations; they are not retroactively attributed to Seagate, IBM, Dell, Lenovo, NetApp, JEDEC, or OCP.

### Functional analogy

Useful analogies compare where work is admitted, observed, and declared complete. They do not establish shared implementation or ancestry.

### Philosophical interpretation

A narrow permissible interpretation is that long-term retention can depend on maintenance whose visibility changes across device, system, and operator layers.

Do not turn that into a claim that every powered interval is maintenance, every counter is proof, or every hidden background task is equivalent.

---

## Explicit anti-collapse rules

Keep these inequalities visible:

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

Find a first-party named SSD/NVMe/SAS interface where a host-visible field is explicitly tied to completion or whole-device coverage of **retention refresh/data-retention maintenance** itself.

This is now more precise than the former generic `find telemetry` question.

### P2 — Dell affected-drive implementation mapping

Identify controller/firmware families under Dell article 000198930 and determine whether Dell's read-all-used-NAND procedure maps to a vendor-defined telemetry/result surface.

### P3 — powered-duration scaling

Find first-party engineering evidence explaining how maintenance time scales with:

- capacity;
- used NAND;
- wear state;
- temperature history;
- controller bandwidth/background scheduling.

Dell says larger capacities can require longer powered time; the implementation relation remains unresolved.

### P4 — earliest Dell publication floor

Recover the first publication date/revision lineage of Dell article 000198930 before the surviving version-3 modification date.

This is source chronology, not mechanism evidence.

### P5 — controlled device-level experiment

Where hardware is available, correlate:

- power-on dwell;
- full-read sweep;
- BMS/patrol/reclaim/refresh counters;
- vendor logs;
- subsequent offline-retention behavior.

A controlled result would still need an exact product/firmware/environment boundary.

---

## Reuse boundary

A current repository search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Background Media Scan` and `Pulsar XT.2` found no dedicated technical-history packet to reuse in this pass.

If future work expands into the history of:

- SCSI Background Media Scan;
- LOG SENSE maintenance telemetry;
- SAS SSD command evolution;
- Seagate enterprise-SSD product genealogy;

that broader history should live in `computing-archaeology` and be linked back here. Case 111 should remain focused on retention qualification, powered maintenance, operator policy, observability, and completion authority.

---

## Current status

**Case 111 remains `grounded`.**

This index adds navigation and narrows an open telemetry question; it does not justify maturity promotion.

The most valuable next evidence is no longer generic proof that enterprise SSDs have background maintenance or telemetry. The sharper target is:

> **a named first-party device interface that explicitly tells the host when retention-specific maintenance or its whole-device coverage obligation is complete.**