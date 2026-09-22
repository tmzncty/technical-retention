# Case 76 — SSD Endurance / Retention Evidence Index

## Status

**`grounded`**

This file is the local evidence/navigation index for [`Case 76 — JEDEC JESD218 SSD Endurance Qualification`](../cases/76-jedec-ssd-endurance-retention-qualification.md).

The case is intentionally kept at `grounded`. The evidence now spans standards-level qualification relations, earlier device-level endurance/retention qualification, manufacturer explanations of physical acceleration, qualified-by-similarity coverage, named commercial product contracts, and later datacenter/NVMe requirement profiles. That breadth does **not** eliminate the remaining gaps around normative revision archaeology, mechanism-specific validation, qualification telemetry, and field-condition mapping.

The central boundary remains:

```text
host-visible endurance rating
    != raw NAND P/E count
    != one universal media-wear coordinate

power-off retention interval
    != universal shelf life
    != mechanism-independent physical age
```

---

## 1. Base case

### [`../cases/76-jedec-ssd-endurance-retention-qualification.md`](../cases/76-jedec-ssd-endurance-retention-qualification.md)

Primary question:

> At a workload-qualified SSD endurance rating, what exactly is being promised about later power-off retention, and how is that promise related to host writes, internal media wear, workload, error criteria, and product class?

The base case directly separates:

```text
Endurance
    != Data Retention

Host writes / TBW
    != internal NVM writes / P-E cycles

application-class service condition
    != universal physical constant

active-use phase
    != retention-use / power-off phase
```

Status: **grounded**.

---

## 2. Evidence chains

### 2.1 Device-level prior art and SSD-level qualification grounding

[`76-jedec-2000-2015-ssd-endurance-retention-grounding.md`](76-jedec-2000-2015-ssd-endurance-retention-grounding.md)

Role:

- anchors the earlier JESD22-A117 device-level program/erase-endurance-and-retention test family;
- separates that device-level test lineage from JESD218's later whole-SSD, host-TBW qualification relation;
- keeps workload, controller behavior, UBER/FFR and post-endurance power-off retention distinct from raw-cell cycling.

Boundary:

```text
earlier NVM endurance/retention qualification
    != JESD218 SSD-level service contract
```

### 2.2 Qualified-by-similarity coverage

[`76-lattice-2014-qualified-by-similarity-retention-deepening.md`](76-lattice-2014-qualified-by-similarity-retention-deepening.md)

Role:

- shows that a manufacturer qualification program may directly stress one vehicle while extending coverage to another family through an explicit similarity relation;
- keeps sample evidence, coverage rules and field-failure probability separate.

Boundary:

```text
directly stressed qualification vehicle
    != every covered product directly stressed

qualified by similarity
    != identical whole-device failure envelope
```

### 2.3 Datacenter/NVMe requirement and product-profile continuation

[`76-ocp-2021-2026-datacenter-nvme-retention-profile-deepening.md`](76-ocp-2021-2026-datacenter-nvme-retention-profile-deepening.md)

Role:

- follows later datacenter/NVMe retention requirement profiles and named product contract surfaces;
- tests how a recognizable service interval can recur across later TLC/QLC and vendor contexts without becoming a raw-cell physics law.

Boundary:

```text
recurring service requirement
    != identical media physics
    != identical controller margin
    != independently audited compliance result
```

### 2.4 Mechanism-specific accelerated-retention boundary

[`76-intel-2012-arrhenius-retention-acceleration-mechanism-boundary-deepening.md`](76-intel-2012-arrhenius-retention-acceleration-mechanism-boundary-deepening.md)

Role:

- uses Intel's June 2012 retention application note to distinguish ICL from SILC;
- grounds Intel's 40 °C / 2,190 h to 66 °C / 96 h worked Arrhenius mapping under a 1.1 eV high-activation-energy model;
- records Intel's warning that SILC has much lower temperature dependence and may anneal under temperatures used to accelerate ICL;
- prevents accelerated dwell from being rewritten as one universal physical-age clock.

Boundary:

```text
qualification-equivalent dwell under model M
    != universal physical age

Ea(ICL model)
    != Ea(SILC)

high-temperature acceleration of ICL
    != guaranteed acceleration of every retention-loss mechanism
```

---

## 3. Cross-chain state model

The evidence now supports the following layered representation:

```text
application / workload history
        ↓
host writes (TBW)
        ↓
controller write amplification + wear leveling
        ↓
internal NVM P/E history
        ↓
physical wear / trap population
        ↓
retention-use power state
        ↓
storage temperature + dwell
        ↓
mechanism-specific charge-loss / recovery processes
        ↓
read-margin / ECC state
        ↓
UBER + functional qualification criterion
        ↓
qualification verdict / product service contract
```

None of the arrows should be collapsed into identity.

In particular:

```text
same TBW
    != same physical wear state

same wear state
    != same retention trajectory under every temperature history

same elapsed retention time
    != same mechanism-specific exposure

same service interval
    != same implementation or physical margin
```

---

## 4. Historical record vs engineering reconstruction

### Historical record

Historical claims in this case family should remain source-bounded:

- JEDEC documents define named qualification objects, classes, workloads, temperatures, durations and acceptance criteria;
- Intel's 2012 manufacturer note describes ICL/SILC behavior and its use of Arrhenius acceleration in retention qualification;
- named manufacturers publish bounded product retention/endurance contracts;
- qualification programs may explicitly use similarity rules rather than directly stressing every covered SKU.

These records do not automatically establish invention priority or implementation genealogy.

### Engineering reconstruction

The project may reconstruct relationships such as:

```text
qualification point
    = wear boundary
    + workload history
    + storage temperature
    + storage duration
    + mechanism/model assumptions
    + acceptance criterion
```

or:

```text
service-level retention contract
    != mechanism-level lifetime constant
```

Such formulas are project models. They must not be attributed to historical actors unless a source actually uses them.

---

## 5. Functional analogies

Functional analogy is allowed only with explicit non-genealogy labels.

### Case 111 — Enterprise SSD Extended Shutdown

[`../cases/111-enterprise-ssd-extended-shutdown-maintenance.md`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md)

Case 111 concerns powered maintenance opportunity, recommissioning and background refresh after or around extended shutdown.

Useful contrast:

```text
Case 76
accelerated passive retention qualification

Case 111
powered device/controller maintenance
```

The fact that both involve hours/days/months does not make the mechanisms equivalent.

### Case 85 — NAND Read Retry

[`../cases/85-nand-read-retry.md`](../cases/85-nand-read-retry.md)

Case 85 separates media state from read-interpretation configuration. This complements Case 76:

```text
physical retention margin
    != reader configuration used to recover a marginal state
```

A drive can therefore have a physical retention trajectory and a controller/read-path mitigation trajectory at the same time.

### Case 36 / Case 37

The base case already routes to the preceding NAND/SSD wear and retention cases. Their role should remain physical/engineering context rather than being silently rewritten as the origin of JESD218's service contract.

---

## 6. Philosophical boundary

The narrow project-level interpretation is:

> retention duration is relational rather than context-free.

An engineering claim such as “three months” is meaningful only with its state and condition qualifiers. It does not denote a universal scalar property detached from wear, temperature, power state, workload history, error margin and qualification criterion.

This is a project interpretation, not historical JEDEC or Intel terminology.

---

## 7. Claim matrix

| Claim | Current support | Status |
| --- | --- | --- |
| JESD218 composes endurance and subsequent power-off retention | direct standard/base-case evidence | grounded |
| TBW is host-visible and not identical to raw NAND cycling | direct standard/base-case evidence | grounded |
| Client/enterprise retention conditions are class-qualified, not universal constants | direct standard/base-case evidence | grounded |
| device-level post-cycling retention qualification predates JESD218 | prior-art evidence | grounded |
| qualification coverage can be extended through explicit similarity criteria | manufacturer qualification evidence | grounded |
| later products can repeat similar retention service intervals across different media/product envelopes | named product evidence | grounded, non-genealogical |
| Intel uses a 1.1 eV Arrhenius model for a 40 °C → 66 °C retention acceleration example | Intel 2012 primary manufacturer source | grounded |
| ICL and SILC cannot be treated as one identical temperature-acceleration process | Intel 2012 primary manufacturer source | grounded |
| 96 h at 66 °C is one universal equivalent-age statement for all SSD physics | contradicted by mechanism boundary | rejected |
| a qualification interval alone predicts exact field lifetime | not supported | rejected |
| recurring service interval proves identical NAND/controller implementation | not supported | rejected |

---

## 8. Remaining research debt

The highest-value open work is now specific rather than generic:

- direct facsimile comparison of JESD218/JESD218A/JESD218B/C revision wording where legally/publicly available;
- public experimental data separating ICL and SILC contributions after controlled P/E histories over multiple storage temperatures;
- later TLC/QLC qualification evidence showing whether and how high-Ea and low-Ea mechanisms are partitioned;
- actual qualification telemetry: raw-error evolution, ECC/UBER behavior and failure criteria during/after accelerated retention;
- field-temperature and field-write distributions versus the standardized qualification assumptions;
- product/controller evidence separating media deterioration from read-retry, ECC, refresh/scrub and remapping mitigations;
- NAND-component qualification versus controller-inclusive SSD qualification;
- explicit evidence for what state is or is not preserved when an accelerated test is interrupted and resumed.

None of these gaps requires changing the present maturity label.

---

## 9. Maturity decision

**Case 76 remains `grounded`.**

Rationale:

- the historical qualification relation is well established;
- multiple evidence layers now support the boundary between service contract, wear state and physical mechanism;
- the new Intel packet strengthens the mechanism-specific acceleration model substantially;
- but normative revision archaeology, later-generation mechanism validation and qualification-to-field transfer remain incomplete.

No promotion is made in this round.