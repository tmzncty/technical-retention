# Case 76 deepening — OCP Datacenter NVMe SSD powered-retention and profile boundary, 2021–2026

## Status

**`bounded deepening complete`** for the narrow standards-level relation documented below.

This note deepens [`../cases/76-jedec-ssd-endurance-retention-qualification.md`](../cases/76-jedec-ssd-endurance-retention-qualification.md). It does **not** change Case 76's `grounded` maturity.

## Research question

Case 76 already grounds the September-2010 JESD218 relation in which a host-visible SSD endurance rating is composed with workload, error/failure criteria, and a subsequent power-off retention interval. It also carries later named-product witnesses whose published retention contracts often use the familiar enterprise figure of three months at 40 °C.

This slice asks a narrower later question:

> By the Open Compute Project's public Datacenter NVMe SSD specifications, is `datacenter SSD retention` still representable as one universal three-month power-off number, or does the interface contract separate powered-off retention, powered-on retention maintenance, and customer/profile-selected retention requirements?

The answer from the inspected primary standards record is the latter.

The bounded relation is:

```text
powered-off EOL retention requirement
    != powered-on retention requirement
    != powered background-refresh obligation
    != selected device-profile retention value
    != warranty duration
```

## Scope and source custody

### Primary source A — OCP Datacenter NVMe SSD Specification v2.0

- Open Compute Project, **_Datacenter NVMe® SSD Specification_**, Version **2.0**, cover date **07/30/2021**.
- Authors named on the cover: Ross Stenfort and Ta-Yu Wu / Facebook; Lee Prewitt / Microsoft; Paul Kaler and David Derosa / HPE; William Lynn and Austin Bolen / Dell EMC.
- Official OCP PDF:
  <https://www.opencompute.org/documents/datacenter-nvme-ssd-specification-v2-0r21-pdf>
- Directly inspected sections:
  - §6.6 `Background Data Refresh`;
  - §7.2 `Retention Conditions`;
  - §7.4 `End-of-Life (EOL)` as context;
  - §12 `Device Profiles`.

### Primary source B — OCP Datacenter NVMe SSD Specification v2.7

- Open Compute Project, **_Datacenter NVMe® SSD Specification_**, Version **2.7**, cover date **01/08/2026**.
- Authors named on the cover: Ross Stenfort / Meta; Lee Prewitt and Tim Sharp / Microsoft; Paul Kaler / HPE; David Black and Colm Murphy / Dell Technologies; Chris Sabol and Charles Kunzman / Google.
- Official OCP PDF:
  <https://www.opencompute.org/documents/datacenter-nvme-ssd-specification-v2-7-final-pdf-1>
- Directly inspected sections:
  - §7.6 `Background Data Refresh`;
  - §8.2 `Retention Conditions`;
  - §8.4 `End-of-Life (EOL)` as context;
  - §13 `Device Profiles`.

The 2021 and 2026 documents are used to establish a public standards/profile contract and its continuity. They are **not** used to establish invention priority for SSD refresh, NAND data retention, wear leveling, or the one-/three-month values.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for the OCP Datacenter NVMe SSD retention/profile slice found no dedicated packet to reuse. Broad OCP/NVMe procurement genealogy, vendor adoption, firmware algorithms, and platform qualification history therefore remain companion-repository work rather than being reconstructed here.

---

## Historical record

### H1 — OCP v2.0 already separates non-operational and operating retention

The July-2021 v2.0 specification does not publish one undifferentiated `retention` number.

Its `RETC-1` requires **Non-Operational (Powered-off)** device data retention at end of life to be **at least one month at 40 °C**, while explicitly directing the reader to device profiles for profile-specific values and allowing longer requirements.

Its immediately adjacent `RETC-2` separately requires **Operating (Powered-on)** data retention of **at least seven years**, under the stated assumption that the device's TBW capability is consumed linearly over its lifetime. The requirement explicitly says that this does **not** imply a particular warranty period.

So the historical source itself requires at least this distinction:

```text
RETC-1
powered-off / end-of-life retention
    minimum 1 month @ 40 °C

RETC-2
powered-on retention
    at least 7 years
    under stated linear-TBW-use assumption
    not a warranty statement
```

The seven-year requirement is therefore not evidence that an unpowered end-of-life device must retain for seven years.

Likewise, the one-month minimum is not the v2.0 document's only possible power-off retention value because the same document delegates a longer selectable value to the Device Profiles table.

### H2 — v2.0 requires powered background data refresh as an explicit retention mechanism

Section 6.6 of v2.0 gives a separate mechanism-level contract.

`BKGND-1` requires support for **background data refresh while the device is powered on** so that power-on retention issues do not cause data loss.

`BKGND-2` separately requires the device to be designed and tested for normal NAND operating temperature.

`BKGND-3` then requires background data refresh to:

- cover the **entire device**; and
- be designed to **continuously run in the background**, not only during idle periods.

That historical wording matters because it blocks two simplifications:

```text
powered-on retention
    != passive NAND charge survival alone
```

and

```text
background retention maintenance
    != idle-only maintenance opportunity
```

The source specifies a device-level behavior and coverage obligation. It does not disclose the controller's page-selection algorithm, ECC thresholds, rewrite geometry, scan cursor, physical cadence, or completion telemetry.

### H3 — v2.0 device profiles make the power-off retention value selectable

Section 12 of v2.0 describes Device Profiles as firmware-based configuration settings applied by device vendors during manufacturing; customers provide an A/B preference for each configuration setting.

For `DP-CFG-3`, defined as `Retention Time based on RETC-1`, the table gives:

- **Configuration A: 1 Month**;
- **Configuration B: 3 Months**.

This is unusually important for the retention argument because both values occur **inside the same datacenter SSD specification and the same profile mechanism**.

The source therefore does not permit the shortcut:

> `datacenter SSD` = `three-month power-off retention by definition`.

The standard's own profile table admits a one-month and a three-month configuration.

This is a contract/profile distinction, not a claim about the raw NAND physics of Configuration A versus B.

### H4 — OCP v2.7 retains the same core split in January 2026

The January-2026 v2.7 specification preserves the same retention architecture.

Its `RETC-1` still requires at least **one month at 40 °C** for non-operational, powered-off, end-of-life data retention and still points to Device Profiles for longer requirements.

Its `RETC-2` still separately requires at least **seven years** of powered-on data retention under the stated linear-TBW-consumption assumption.

Its §7.6 still requires powered background data refresh, entire-device coverage, and continuous background operation rather than idle-only execution.

Its §13 Device Profiles still gives `DP-CFG-3` as:

- A = **1 Month**;
- B = **3 Months**.

The bounded historical result is therefore continuity from the inspected **v2.0 (30 July 2021)** publication to the inspected **v2.7 (8 January 2026)** publication.

This does **not** establish that every intermediate revision used byte-for-byte identical wording. It establishes that the core relation is directly visible at both endpoints.

### H5 — OCP defines a datacenter requirement layer, not merely an NVMe command list

The v2.7 Overview says the document defines requirements for a Datacenter NVMe SSD, that these requirements are **in addition to** underlying standards, and that they may override some underlying requirements. It also says customers may impose additional requirements.

That statement is useful for scope discipline. The OCP retention/profile rules are a datacenter SSD requirement layer with customer/profile choices; they should not be silently treated as identical to:

- the NVM Express base command-set standard;
- JEDEC's JESD218 application-class qualification relation;
- one vendor's product warranty;
- one operator's field maintenance runbook.

---

## Engineering reconstruction

### E1 — `retention time` is power-regime-qualified in the OCP contract

The same device family is governed by different retention obligations depending on whether it is powered.

A useful reconstruction is:

```text
power-off regime
    controller background work unavailable
    -> RETC-1 minimum/profile interval

power-on regime
    controller operational
    + required background data refresh
    -> RETC-2 multi-year operating-retention contract
```

This is not a claim that `RETC-2 = BKGND alone`. The source gives both requirements, but it does not publish a complete causal proof allocating the seven-year result among media physics, ECC, read-retry, wear leveling, refresh, over-provisioning, and other controller mechanisms.

The defensible statement is narrower:

> OCP's powered-on retention contract explicitly coexists with a required powered background-refresh mechanism; its powered-off contract cannot rely on that mechanism executing during the off interval.

### E2 — one SSD has more than one retention horizon

The case already uses `retention horizon` as a project descriptor. The OCP evidence makes the plurality unusually concrete:

```text
H_off(EOL, 40 °C, selected profile)
    = at least 1 month or 3 months by DP-CFG-3

H_on(stated TBW-life assumption)
    = at least 7 years
```

These are not competing measurements of one timeless substrate constant. They are separate service relations under different power and profile conditions.

### E3 — profile selection is retained policy/configuration, not payload embodiment

`DP-CFG-3` is a manufacturing/customer-selected device-profile requirement. Conceptually it belongs to a different layer than the user data whose retention is being protected.

The engineering decomposition is:

```text
payload state
    != retention-policy/profile state
    != maintenance mechanism
    != demonstrated maintenance progress
```

The inspected OCP clauses do not say how `DP-CFG-3` is encoded internally, whether a host can later change it, which firmware tables enforce it, or whether different settings imply different over-provisioning, NAND selection, refresh policy, qualification bins, or some combination.

Therefore the profile value should be treated as a **contractual/configuration requirement**, not reverse-engineered into an undocumented physical implementation.

### E4 — entire-device refresh coverage does not prove one particular physical rewrite pass

`BKGND-3` requires background data refresh to cover the entire device. That is stronger than an idle-only or hot-data-only statement, but it still does not expose exact embodiment.

The following stronger claims are not warranted:

```text
entire-device coverage
    = every physical NAND page rewritten on one periodic sweep
```

or

```text
continuous background refresh
    = one fixed scan cursor with one fixed revisit period
```

A controller may make implementation-specific decisions below the standard's observable requirement. The OCP source is intentionally used here for the **service/maintenance obligation**, not firmware archaeology.

### E5 — OCP's one-month profile prevents `three months` from becoming a universal enterprise/datacenter constant

Case 76 already warns that JESD218's application-class table is a qualified service model rather than a raw-media constant. The OCP record supplies a later counterexample at the standards/profile layer.

JESD218's 2010 enterprise row uses a three-month / 40 °C power-off retention condition at its stated qualification boundary. OCP v2.0/v2.7, by contrast, makes **one month** the base `RETC-1` minimum and makes **one month versus three months** a Device Profile setting.

The safe comparison is:

```text
same broad domain: enterprise/datacenter SSDs
    != same retention contract

same numerical 3-month option
    != same standards semantics
```

A three-month OCP profile and the JESD218 enterprise row may share a number and temperature, but the inspected OCP sources do not say that `DP-CFG-3 B` is definitionally or procedurally identical to a JESD218 qualification verdict.

### E6 — `powered on` is necessary for the specified refresh opportunity but not itself completion evidence

OCP says the refresh mechanism runs while powered and is designed to run continuously. It does not publish an operator-visible `refresh complete` bit for this requirement in the inspected sections.

Therefore:

```text
power applied
    -> maintenance opportunity / execution regime available

but

power applied
    != proof that every retention-risk item has already been renewed
```

This connects functionally to Case 111, where IBM/Dell operator guidance separately turns extended shutdown into powered maintenance windows and, in some system contexts, scrub-completion evidence.

The relation is a functional comparison only. This note does not establish that the OCP BKGND implementation is the same algorithm as the IBM/Dell devices behind Case 111.

### E7 — powered retention requirement is not a warranty promise

OCP v2.0 explicitly says the seven-year powered-on retention requirement does not imply a specific warranty period.

Thus:

```text
retention service requirement
    != commercial warranty duration
```

This matters methodologically because service-contract time, qualification time, expected media survival, maintenance cadence, and commercial support/warranty are often reported in the same product literature but are not interchangeable predicates.

---

## Cross-case comparison

### Case 76 — JESD218 qualification

The canonical Case 76 relation remains:

```text
host TBW / application-class endurance stress
    -> qualified SSD state
    -> specified power-off retention interval
```

The OCP deepening adds:

```text
datacenter device requirement
    -> power-state split
    -> powered background refresh obligation
    -> profile-selected power-off interval
```

The OCP material is a later standards/profile counterexample to universalizing one `enterprise SSD retention` number. It is not evidence that OCP replaced JESD218 or that one standard was derived from the other.

### Case 37 — Samsung 840 EVO periodic refresh

Case 37 is a named-product episode involving old-data read-performance degradation and a powered periodic refresh feature.

The OCP record is broader but less implementation-specific: it requires background data refresh for datacenter SSDs under its scope, entire-device coverage, and continuous background execution. It does not disclose the same product symptom, algorithm, threshold, or release history.

Functional analogy:

> powered controller activity can participate in keeping older stored data serviceable.

Historical continuity claim:

> **not established here**.

### Case 111 — enterprise SSD extended-shutdown maintenance

Case 111 moves outward from device requirements into operator schedules: how long a system may remain off, how long it should be powered, whether a read sweep or system scrub is requested, and what completion evidence an operator may observe.

The OCP deepening sits one layer below that runbook problem:

```text
OCP device-level powered-refresh obligation
    != IBM/Dell field maintenance schedule
    != ESS scrub-completion message
```

The useful comparison is that `power state` can change the available retention machinery without itself proving completion.

### Cases 36 and 55 — refresh/correction and endurance telemetry

Case 36 separates powered Flash correction/renewal from passive power-off survival. Case 55 separates lifetime/health telemetry from immediate payload failure.

OCP adds another orthogonal relation: a profile-selected power-off interval and a distinct multi-year powered-retention requirement.

None of these should be collapsed into one scalar `SSD health` variable.

---

## Functional analogy

A useful functional analogy is to **two maintenance regimes sharing one payload**:

- while unpowered, survival depends on the state already embodied in nonvolatile media and whatever correction margin will remain when power returns;
- while powered, the device may actively spend controller work, bandwidth, spare media, and write endurance to renew risky data.

The analogy is functional. The OCP specification does not use the repository's `maintenance-regime` taxonomy and does not claim philosophical continuity with DRAM refresh, magnetic-core rewrite, RAID scrubbing, or distributed replica repair.

---

## Philosophical interpretation

The technical fact creating the conceptual problem is precise:

> the same logical payload is assigned different retention promises depending on whether the device remains powered, and the powered regime includes required background renewal work.

A narrow project interpretation follows:

> `retention duration` is not always a property that can be assigned to a stored thing independently of its operational regime. The future availability of the payload can depend on whether the apparatus remains able to perform hidden maintenance.

The interpretation stops before claiming that OCP engineers were theorizing `technical memory`, `tertiary retention`, `Bestand`, or any philosophical category. Their vocabulary is an engineering requirements vocabulary: powered-on/off retention, background data refresh, endurance, device profiles, and EOL.

---

## Explicit non-claims

This deepening does **not** claim any of the following:

1. OCP invented SSD background data refresh.
2. OCP invented the one-month or three-month retention intervals.
3. OCP v2.0 is the first historical datacenter SSD document to mention powered refresh.
4. OCP's `RETC-1` is identical to JESD218's enterprise retention test.
5. OCP Device Profile B is proof of JESD218 compliance.
6. OCP Device Profile A is proof of non-compliance with any particular JEDEC revision.
7. A one-month profile is physically incapable of retaining data for longer than one month.
8. A three-month profile will fail immediately after three months.
9. Seven-year powered retention is seven-year powered-off retention.
10. Seven-year powered retention is a seven-year warranty.
11. Power-on by itself proves refresh completion.
12. `BKGND-3` proves that every physical page is rewritten once per fixed sweep.
13. `continuous` proves a fixed-period scan clock.
14. `entire device` means every raw NAND cell is user-data-bearing and rewritten.
15. Background refresh is the only mechanism supporting OCP powered retention.
16. ECC, read retry, wear leveling, over-provisioning, media selection, and refresh are interchangeable.
17. The one-/three-month profile distinction is caused by NAND cell density alone.
18. OCP v2.7 uses byte-for-byte identical retention text to every intermediate revision.
19. A standards/profile requirement proves one named vendor firmware implements it correctly.
20. A standards requirement is an independent conformance result.
21. A customer profile preference is the same thing as a host runtime command.
22. A retention profile is the same thing as user payload state.
23. OCP background refresh is historically descended from Samsung 840 EVO periodic refresh.
24. OCP background refresh is the same mechanism as DRAM refresh or RAID scrub.
25. `datacenter SSD` and `JESD218 Enterprise class` are synonyms.
26. The recurrence of `3 months @ 40 °C` across documents proves one universal NAND constant.
27. Powered background refresh implies zero additional media wear.
28. The OCP requirement exposes the refresh cursor, metadata representation, thresholds, or persistence horizon.
29. End-of-life retention is the same question as sudden-power-loss durability.
30. End-of-life retention is the same question as secure erase or sanitization.

---

## Claim ledger

| ID | Claim | Layer | Evidence strength |
| --- | --- | --- | --- |
| OCP76-1 | v2.0 RETC-1 requires at least one month powered-off EOL retention at 40 °C, with longer profile requirements possible | Historical record | Direct OCP v2.0 normative text |
| OCP76-2 | v2.0 RETC-2 separately requires at least seven years powered-on retention under a linear-TBW-use assumption and says this is not a warranty | Historical record | Direct OCP v2.0 normative text |
| OCP76-3 | v2.0 BKGND-1/3 require powered background refresh, whole-device coverage, and continuous background operation rather than idle-only operation | Historical record | Direct OCP v2.0 normative text |
| OCP76-4 | v2.0 DP-CFG-3 exposes one-month and three-month retention configurations | Historical record | Direct OCP v2.0 Device Profile table |
| OCP76-5 | v2.7 retains the same core RETC/BKGND/profile split in January 2026 | Historical record | Direct OCP v2.7 normative text |
| OCP76-6 | Powered-on and powered-off retention are distinct service relations | Engineering reconstruction | Directly constrained by RETC-1 vs RETC-2 |
| OCP76-7 | The powered-on relation includes a mandatory maintenance opportunity/mechanism unavailable while fully unpowered | Engineering reconstruction | Constrained by BKGND-1/3 + power-state wording |
| OCP76-8 | One datacenter SSD specification can admit more than one power-off retention profile | Engineering reconstruction | Directly constrained by DP-CFG-3 |
| OCP76-9 | `three months` cannot be treated as a universal datacenter SSD constant | Engineering reconstruction / counterexample | OCP one-month minimum/profile A vs profile B |
| OCP76-10 | OCP/JESD218 comparison is functional/contractual, not proven genealogy | Functional analogy boundary | Separate standards records; no influence evidence claimed |
| OCP76-11 | Operational regime can be part of what makes a retention duration meaningful | Philosophical interpretation | Bounded interpretation of power-state split + BKGND requirements |

---

## Remaining evidence debt

This slice intentionally leaves the following work open:

- inspect the full OCP v1.x / Cloud SSD predecessor record to establish when `RETC-*`, `BKGND-*`, and `DP-CFG-3` first entered the specification family;
- revision-by-revision diff from v2.0 through v2.7 rather than endpoint comparison only;
- recover public issue/change-request history explaining why Profile A uses one month and Profile B uses three months;
- determine whether OCP supplier compliance reports expose test methods or pass/fail evidence for RETC/BKGND requirements;
- obtain named-drive conformance evidence that is independent of manufacturer self-description;
- recover controller/firmware evidence for refresh eligibility, cursor/progress state, rewrite geometry, thresholds, and restart behavior;
- quantify write amplification/endurance cost attributable specifically to background retention refresh;
- distinguish how SLC/MLC/TLC/QLC generations meet the same OCP service requirement without treating media label as a causal explanation by itself;
- compare OCP profile retention with the exact later JESD218 revision text rather than assuming the September-2010 wording remained unchanged;
- investigate whether powered background refresh progress/state survives reset or power loss and in what representation;
- map operator guidance in Case 111 onto specifically OCP-qualified products without assuming the same hidden firmware behavior;
- leave broad OCP/NVMe product genealogy, adoption history, controller design, and datacenter procurement evolution to `computing-archaeology` unless they change the retention comparison.

## Bounded result

The narrow result is now defensible:

> **By OCP Datacenter NVMe SSD Specification v2.0 (30 July 2021), the public datacenter-SSD contract already distinguished at least one month of powered-off EOL retention at 40 °C from at least seven years of powered-on retention, separately required whole-device background data refresh while powered, and made the powered-off requirement profile-selectable between one and three months. OCP v2.7 (8 January 2026) retains this architecture. Therefore `SSD retention time` cannot be treated here as one substrate-only constant or one universal enterprise/datacenter number: power regime, maintenance availability, endurance context, and selected service profile are separate parts of the retained-state relation.**

That is a standards/engineering conclusion. It is not an invention claim, a firmware reconstruction, a compliance result for a named device, or a universal NAND-physics law.

## Sources

1. Open Compute Project, **_Datacenter NVMe® SSD Specification_**, Version 2.0, 30 July 2021. Official PDF: <https://www.opencompute.org/documents/datacenter-nvme-ssd-specification-v2-0r21-pdf>. Relevant sections: §6.6 Background Data Refresh; §7.2 Retention Conditions; §7.4 End-of-Life; §12 Device Profiles.
2. Open Compute Project, **_Datacenter NVMe® SSD Specification_**, Version 2.7, 8 January 2026. Official PDF: <https://www.opencompute.org/documents/datacenter-nvme-ssd-specification-v2-7-final-pdf-1>. Relevant sections: §7.6 Background Data Refresh; §8.2 Retention Conditions; §8.4 End-of-Life; §13 Device Profiles.
3. Canonical Case 76 grounding and source ledger: [`76-jedec-2000-2015-ssd-endurance-retention-grounding.md`](76-jedec-2000-2015-ssd-endurance-retention-grounding.md).
4. Operational continuation: [`../cases/111-enterprise-ssd-extended-shutdown-maintenance.md`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md).
