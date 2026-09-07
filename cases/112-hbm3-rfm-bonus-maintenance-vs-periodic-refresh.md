# Case 112 — HBM3 Refresh Management: Activity-Triggered Bonus Maintenance vs Periodic Refresh

## Status

**`grounded`** — bounded to the public HBM3 `JESD238` / `JESD238A` Refresh Management (`RFM`) contract, especially the separation between periodic `REF` coverage and activity-triggered `RFM`, and the HBM3-specific difference between rolling `REFpb` coverage and targeted `RFMpb`.

Grounding record: [`../evidence/112-jedec-hbm3-2022-2023-rfm-grounding.md`](../evidence/112-jedec-hbm3-2022-2023-rfm-grounding.md).

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

> **January 2022 HBM3 publication ≠ RFM invention date**

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
| RAA threshold equals physical corruption threshold | X | rejected |
| RFM completion proves a particular victim-row rewrite | X | rejected |
| HBM3 `RFMpb` equals DDR5 `RFMsb` geometry | X | rejected |
| 2014 RowHammer paper proves direct HBM3 genealogy | X | rejected |
| January 2022 is invention priority | X | rejected |

## Open work

Pre-2022 committee/patent genealogy; named HBM3 stack and controller behavior; independent HBM3 command traces; hidden victim selection; ARFM and later HBM evolution; threshold/fault injection; performance/energy validation.

## Sources

1. JEDEC, **JESD238 — High Bandwidth Memory DRAM (HBM3)**, January 2022, especially §6.3.2.6–§6.3.2.7 and `DEVICE_ID` RAA/RFM fields. Public text mirror: <https://studylib.net/doc/28350036/jesd238-hbm3>.
2. JEDEC, **JESD238A — High Bandwidth Memory DRAM (HBM3)**, January 2023, revision of JESD238 January 2022. Public text mirror: <https://studylib.net/doc/27298996/jesd238a>.
3. Yoongu Kim et al., **“Flipping Bits in Memory Without Accessing Them: An Experimental Study of DRAM Disturbance Errors,”** ISCA 2014. CMU institutional page: <https://istc-cc.cmu.edu/publications/papers/2014/kim-isca14_abs.shtml>.
