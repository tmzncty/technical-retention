# Case 112 — HBM3 Refresh Management: Activity-Triggered Bonus Maintenance vs Periodic Refresh

## Status

**`grounded`** — bounded to the public HBM3 `JESD238` / `JESD238A` Refresh Management (`RFM`) contract, especially the separation between periodic `REF` coverage and activity-triggered `RFM`, the HBM3-specific difference between rolling `REFpb` coverage and targeted `RFMpb`, and the optional Adaptive Refresh Management (`ARFM`) policy-level contract already present in the January-2022 standard.

Grounding record: [`../evidence/112-jedec-hbm3-2022-2023-rfm-grounding.md`](../evidence/112-jedec-hbm3-2022-2023-rfm-grounding.md).

ARFM chronology/policy deepening: [`../evidence/112-jedec-hbm3-2022-2023-arfm-deepening.md`](../evidence/112-jedec-hbm3-2022-2023-arfm-deepening.md).

Named commercial controller-support deepening: [`../evidence/112-rambus-2021-2026-hbm3-controller-rfm-commercial-support-deepening.md`](../evidence/112-rambus-2021-2026-hbm3-controller-rfm-commercial-support-deepening.md).

## Scope

Case 54 already grounds the broad DDR5 split-authority pattern: a DRAM may advertise an RFM requirement/thresholds while the controller retains activation-pressure state and schedules time for opaque in-DRAM work. Case 112 asks a narrower HBM3 question:

> What changes when a **per-bank RFM command need not roll across all banks**, although ordinary per-bank refresh still must cover all banks?

This case is not a general HBM history, a complete RowHammer history, a claim that HBM3 invented activation-aware maintenance, or a reverse engineering of hidden victim-row logic. Broader HBM architecture/history remains for [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology); current repository search found no dedicated HBM3-RFM case there to reuse.

## Historical anchor

`JESD238` (January 2022), §6.3.2.7, defines HBM3 Refresh Management. The inspected standard exposes:

- an `RFM` field saying whether additional management beyond ordinary refresh is required;
- suggested per-bank Rolling Accumulated ACTIVATE (`RAA`) accounting;
- vendor-provided `RAAIMT` and `RAAMMT` thresholds;
- all-bank `RFMab`;
- single-bank `RFMpb`.

`JESD238A` (January 2023), explicitly a revision of the January 2022 edition, preserves the bounded relations used here. This is a public-standards floor, not an invention-priority claim.

## 1. Periodic REF ≠ RFM

The decisive standard boundary is explicit: an RFM command does **not** replace periodic REF and does **not** affect the ordinary internal refresh counters. The standard characterizes RFM as extra/“bonus” time for internal refresh management.

Engineering reconstruction:

```text
baseline time/retention obligation
    -> periodic REF / REFpb
    -> ordinary refresh progress

activation-pressure obligation
    -> RAA reaches management threshold
    -> RFMab / RFMpb
    -> extra internal-management opportunity
    -> no ordinary refresh-counter progress
```

Ordinary REF can also reduce RAA pressure, but one event affecting two accounting relations does not make those relations identical.

> **periodic REF obligation ≠ RFM obligation**

## 2. `REFpb` and `RFMpb` have different coverage rules

HBM3 periodic `REFpb` may select banks in any order, but a bank cannot receive another `REFpb` until all banks in that SID have been covered. The controller must track that periodic bank cycle.

HBM3 then states that the rolling-all-bank rule **does not apply to `RFMpb`**. `RFMpb` targets one selected bank and can therefore follow activity pressure rather than periodic coverage order.

This yields the central result:

> **per-bank maintenance target ≠ periodic retained-set coverage**

and:

> **one `RFMpb` completion ≠ progress through the ordinary `REFpb` all-bank cycle**

A hot bank may need repeated activity-conditioned maintenance while every other bank remains part of the baseline periodic-retention obligation.

## 3. RAA is maintenance state, not payload or retention age

The suggested controller scheme increments a bank's RAA when that bank receives ACTIVATE and reduces it through qualifying REF/RFM work.

RAA is therefore constitutive second-order retention state: it retains enough past activity to decide future maintenance/admission while intentionally forgetting detailed event history. It is not:

- application payload;
- wall-clock retention age;
- a complete activation trace;
- the DRAM's ordinary refresh counter;
- a physical adjacency/victim map.

> **RAA count ≠ payload**  
> **RAA count ≠ retention age**  
> **RAA count ≠ complete access history**

## 4. Management threshold ≠ corruption threshold

At vendor-provided `RAAIMT`, additional management is needed. If RAA reaches `RAAMMT`, no more ACTIVATE commands are allowed to that bank until REF/RFM reduces the count.

The inspected clauses do not say that a bit flips exactly at either threshold.

> **`RAAIMT` / `RAAMMT` ≠ demonstrated bit-flip threshold**

Likewise, a bank can become temporarily unable to accept another ACTIVATE while its payload is still retained:

> **ACTIVATE blocked at `RAAMMT` ≠ payload loss**

The blocked state is an admission-control consequence intended to protect integrity.

## 5. RFM completion ≠ disclosed internal algorithm

The standard gives the HBM3 device time to manage refresh internally. It does not expose physical victim-row selection, row adjacency, hidden counters, or the exact restore sequence.

> **RFM completion ≠ proof of a specific victim-row rewrite**

and:

> **host-visible RAA accounting ≠ in-DRAM victim knowledge**

Precise selection of a bank is still much coarser than proof about which physical rows are restored inside that bank.

## 6. Ordinary REF can reduce RAA without changing identity

HBM3 permits ordinary REF to decrement RAA for affected banks. Therefore a single maintenance event can simultaneously satisfy baseline charge-restoration work and reduce an activation-pressure budget.

> **REF reducing RAA ≠ REF becoming disturbance-only maintenance**

This is a useful general rule for the repository: one event can participate in multiple retention relations without those relations becoming semantically identical.

## 7. Self-refresh RAA reset ≠ RFM replacing REF

HBM3 permits per-bank RAA values to reset after sufficiently long self-refresh (`tRAASRF`), while shorter self-refresh does not earn that decrement.

That is an accounting reset under a maintenance-qualified regime, not evidence that RFM and periodic refresh counters are one state machine.

> **RAA reset after sustained self-refresh ≠ periodic-REF obligation erased**


## 8. Adaptive RFM adds policy-level state above per-bank RAA

The original Case-112 pass left `ARFM/later HBM evolution` in open work. Direct reinspection of the same January-2022 JESD238 source shows that this wording was too loose: **Adaptive Refresh Management is already specified in HBM3 §6.3.2.8.** The correction is chronological and semantic; it is not a new invention-priority claim.

### H/P — capability, default requirement, and selected level are distinct

HBM3 exposes separate `ARFM` and `RFM` bits in the IEEE1500 `DEVICE_ID` WDR. `ARFM` says whether adaptive-level selection is supported; the default `RFM` bit says whether refresh management is required at the default level. The same device record supplies read-only default and A/B/C `RAAIMT`, `RAAMMT`, and `RAADEC` profiles, while `MR8 OP[5:4]` selects the active RFM level.

Therefore:

```text
ARFM capability
    != default RFM requirement
    != selected RFM level
    != per-bank RAA value
```

The device publishes an allowed policy menu; the controller selects among those vendor-defined profiles. This is a more precise split-authority relation than treating “the threshold” as one immutable constant.

### H/P — a level transition must retire outstanding accounted pressure first

JESD238 requires the host to decrement RAA to **0** using RFM or pending REF commands before changing the ARFM level, and requires the same RFM level on all channels of the HBM3 DRAM.

Engineering reconstruction:

```text
old policy level
    + outstanding bank-local RAA pressure
    -> maintenance / REF until accounted RAA = 0
    -> level transition
    -> new vendor-defined threshold/decrement profile
```

So:

> **policy change != arbitrary reinterpretation of an outstanding RAA balance under new thresholds**.

The standard gives a transition rule for the accounted state. It does **not** say that RAA=0 erases physical disturbance history or reveals the hidden mitigation state.

### H/P — default “RFM not required” is not an immutable lifetime property

ARFM can also make RFM operative on an ARFM-capable HBM3 DRAM whose default `RFM` bit says `RFM not required`: selecting a non-default level makes the device treat RFM commands as RFM rather than RNOP.

Thus:

> **default RFM requirement != immutable lifetime RFM requirement**.

Conversely, a device without ARFM support cannot treat the non-default level field as a generic tuning knob; those combinations are illegal/RFU.

### E — “adaptive” does not prove autonomous DRAM policy selection

The public contract gives the **controller** flexibility to choose Levels A/B/C. The inspected standard does not demonstrate that the DRAM autonomously chooses a level from workload, temperature, or observed faults.

> **ARFM != demonstrated autonomous self-tuning of the selected level**.

This distinction matters because Case 112 already separates public controller-side RAA bookkeeping from opaque in-DRAM management. ARFM adds a policy-selection layer; it does not disclose the hidden victim-selection algorithm.

Full source mapping and limits are recorded in [`../evidence/112-jedec-hbm3-2022-2023-arfm-deepening.md`](../evidence/112-jedec-hbm3-2022-2023-arfm-deepening.md).

## 9. Named commercial controller witness: Rambus HBM3E/HBM3 Controller IP

A new bounded product-level witness closes the shallowest form of the earlier `named controller implementation` debt without pretending that public marketing material exposes internal scheduling logic.

### H/P — HBM3-ready controller engineering predates the final public HBM3 standard

Rambus announced an **HBM3-ready memory interface subsystem** on **16 August 2021**, consisting of a digital controller plus PHY. The release advertised HBM3 RAS support and a built-in hardware-level performance activity monitor.

That dated record is useful as a pre-JESD238 controller-engineering floor, but it does **not** explicitly mention RFM, RAA, or ARFM.

> **2021 HBM3-ready + RAS/activity monitor != proved 2021 RFM support claim**.

The current RFM wording must not be back-projected into that announcement.

### H/P — the controller became a named licensable product

On **25 October 2023**, Rambus announced HBM3 Memory Controller IP supporting up to 9.6 Gbps, described it as modular/configurable, said it could be integrated with a customer's choice of third-party HBM3 PHY, and stated that the controller was available for licensing.

That establishes a commercial controller-product boundary rather than a standards-only example. The dated release itself still does not enumerate RFM.

### H/P — the current controller feature list explicitly includes RFM

The current Rambus HBM3E/HBM3 Controller IP page, inspected **14 September 2026**, explicitly lists:

- `Refresh Management (RFM) support`;
- self-refresh and power-down low-power modes;
- HBM3 RAS features;
- a built-in hardware-level performance Activity Monitor;
- DFI compatibility and AXI/native user interfaces.

Therefore the bounded public-product claim is now grounded:

> **at least one named commercial HBM3 controller-IP product explicitly advertises RFM support**.

The exact first date on which Rambus publicly used that RFM wording remains unknown because the current product page is undated.

### E — feature support does not reveal the bookkeeping implementation

The tempting shortcut is rejected. Rambus calls the other block a **performance Activity Monitor**; the public page does not say it stores per-bank RAA, applies `RAAIMT`/`RAAMMT`/`RAADEC`, or drives RFM scheduling.

```text
RFM support
    + Activity Monitor
    !=
proved JEDEC RAA implementation
```

Likewise:

```text
controller feature support
    != runtime RFM enabled in every system
    != ARFM capability
    != ARFM level selected
    != particular RFM command currently due
```

The standard contract and the commercial feature claim are complementary evidence layers, not interchangeable ones.

### E — controller, PHY, and DRAM are separate maintenance boundaries

Rambus describes the controller as combinable with a customer-selected PHY. For retention analysis this supports a bounded decomposition:

```text
controller command / scheduling logic
    != PHY electrical transport
    != opaque in-DRAM maintenance
```

It does not prove the location of every counter in every customer integration.

Detailed source mapping and explicit non-claims are in [`../evidence/112-rambus-2021-2026-hbm3-controller-rfm-commercial-support-deepening.md`](../evidence/112-rambus-2021-2026-hbm3-controller-rfm-commercial-support-deepening.md).

## Cross-case comparison

### Case 54 — DDR5 RFM

Case 54 owns the broad `device requirement + controller activity accounting + hidden DRAM management` decomposition. Case 112 adds HBM3-specific target/coverage geometry.

> **HBM3 `RFMpb` ≠ DDR5 `RFMsb` target geometry**

The bounded HBM3 command selects one bank; Case 54's DDR5 same-bank form belongs to a different geometry. Shared RFM/RAA vocabulary supports functional comparison, not implementation identity or genealogy.

### Case 105 — LPDDR2 REFpb

Case 105 shows per-bank periodic transactions whose sequence still covers the full retained bank set. HBM3 periodic `REFpb` preserves the same high-level distinction; HBM3 `RFMpb` supplies the counterexample that activity-conditioned per-bank work need not roll across all banks.

> **same transaction granularity ≠ same coverage obligation**

### Case 106 — DDR5 REFsb

Case 106 separates a parallel same-bank-index target set from full periodic coverage. Case 112 separates a single activity-conditioned target from ordinary periodic progress.

Together:

```text
maintenance name
    != target geometry
    != trigger
    != coverage obligation
    != accounting effect
```

This is functional comparison only.

### Case 53 — RowHammer prior art

Kim et al.'s 2014 open experimental study demonstrated that repeated activation can corrupt nearby DRAM rows and related the disturbance to accelerated charge leakage. That is an earlier open mechanism floor for activation-conditioned integrity risk.

It does **not** prove that HBM3 RFM derives from that paper, implements PARA, or uses the same thresholds/algorithm.

> **RowHammer 2014 evidence ≠ demonstrated HBM3-RFM genealogy**

## Historical-priority boundary

`JESD238` is dated January 2022; `JESD238A` is dated January 2023. Those dates establish a public standard interface by then, not the origin of refresh management. Earlier patents, vendor-private mechanisms, committee drafts, or DDR5/HBM development may predate publication.

Rambus's August-2021 HBM3-ready controller/subsystem announcement now supplies a pre-final-standard commercial engineering floor, but because that release does not explicitly name RFM it does not establish a pre-2022 RFM-publication floor.

> **January 2022 HBM3 publication ≠ RFM invention date**

and:

> **pre-standard HBM3-ready controller engineering ≠ pre-standard public RFM claim**.

## Claim ledger

| Claim | Type | Strength |
| --- | --- | --- |
| JESD238 Jan. 2022 exposes HBM3 RFM/RAA/RFMpb/RFMab | H/P | strong for inspected standard mirror |
| JESD238A Jan. 2023 preserves the bounded relation | H/P | strong |
| periodic `REFpb` must roll through all banks within an SID | H/P | strong |
| `RFMpb` is explicitly exempt from that rolling rule | H/P | strong |
| RFM does not replace REF or advance internal refresh counters | H/P | strong |
| ordinary REF can reduce RAA | H/P | strong |
| `RAAMMT` can block further ACTIVATE until maintenance | H/P | strong |
| sufficiently long self-refresh may reset RAA | H/P | strong |
| RFM target scope differs from retained-set coverage | E | strong |
| Rambus publicly announced an HBM3-ready controller+PHY subsystem in Aug. 2021 | H/P | strong |
| the inspected Aug. 2021 release explicitly names RFM | X | rejected |
| Rambus HBM3 Memory Controller IP was available for licensing in Oct. 2023 | H/P | strong |
| current Rambus HBM3E/HBM3 controller page explicitly lists RFM support | H/P | strong for current product contract |
| Rambus performance Activity Monitor is proven to be JEDEC RAA bookkeeping | X | rejected |
| controller/PHY/DRAM are separable maintenance-responsibility boundaries | E | strong as bounded reconstruction |
| RAA threshold equals physical corruption threshold | X | rejected |
| RFM completion proves a particular victim-row rewrite | X | rejected |
| HBM3 `RFMpb` equals DDR5 `RFMsb` geometry | X | rejected |
| 2014 RowHammer paper proves direct HBM3 genealogy | X | rejected |
| January 2022 is invention priority | X | rejected |

## Open work

Pre-2022 committee/patent genealogy remains open. The **named commercial controller public-support witness is now closed at feature-list level**, but detailed controller behavior remains open: archived/datable first RFM-support wording, actual RAA bookkeeping/scheduling, commercial ARFM level-selection policy, and independent HBM3 command traces. Named HBM3 stack/device parameter values, hidden victim selection, threshold/fault injection, customer deployment evidence, and performance/energy validation also remain open. Later HBM evolution beyond the inspected 2022–2023 standards contract remains a separate revision-specific question.

## Sources

1. JEDEC, **JESD238 — High Bandwidth Memory DRAM (HBM3)**, January 2022, especially §6.3.2.6–§6.3.2.7 and `DEVICE_ID` RAA/RFM fields. Public text mirror: <https://studylib.net/doc/28350036/jesd238-hbm3>.
2. JEDEC, **JESD238A — High Bandwidth Memory DRAM (HBM3)**, January 2023, revision of JESD238 January 2022. Public text mirror: <https://studylib.net/doc/27298996/jesd238a>.
3. Yoongu Kim et al., **“Flipping Bits in Memory Without Accessing Them: An Experimental Study of DRAM Disturbance Errors,”** ISCA 2014. CMU institutional page: <https://istc-cc.cmu.edu/publications/papers/2014/kim-isca14_abs.shtml>.
4. Rambus Inc., **“Rambus Advances AI/ML Performance with 8.4 Gbps HBM3-Ready Memory Subsystem,”** 16 August 2021: <https://investor.rambus.com/press-releases/press-release-details/2021/Rambus-Advances-AIML-Performance-with-8.4-Gbps-HBM3-Ready-Memory-Subsystem/default.aspx>.
5. Rambus Inc., **“Rambus Boosts AI Performance with 9.6 Gbps HBM3 Memory Controller IP,”** 25 October 2023: <https://investor.rambus.com/press-releases/press-release-details/2023/Rambus-Boosts-AI-Performance-with-9.6-Gbps-HBM3-Memory-Controller-IP/default.aspx>.
6. Rambus, **“HBM3E / HBM3 Controller IP,”** official current product page, inspected 14 September 2026: <https://www.rambus.com/interface-ip/hbm/hbm3-controller/>.
