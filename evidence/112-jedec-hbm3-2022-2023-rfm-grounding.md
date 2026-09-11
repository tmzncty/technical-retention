# Evidence 112 — JEDEC HBM3 Refresh Management, 2022–2023

## Scope

This record grounds one narrow relation:

> HBM3 separates ordinary periodic refresh coverage from activity-triggered Refresh Management, and single-bank `RFMpb` is explicitly exempt from the rolling-all-bank rule that applies to periodic `REFpb`.

It does not reconstruct hidden in-DRAM mitigation, establish commercial-controller behavior, or claim invention priority.

ARFM chronology/policy deepening: [`112-jedec-hbm3-2022-2023-arfm-deepening.md`](112-jedec-hbm3-2022-2023-arfm-deepening.md). Direct reinspection shows that ARFM is already part of JESD238 (January 2022), so it is no longer left as a generic later-HBM evidence item.

## Source 1 — JESD238, January 2022

**Document:** JEDEC, _High Bandwidth Memory DRAM (HBM3)_, JESD238, January 2022.  
**Public text mirror inspected:** <https://studylib.net/doc/28350036/jesd238-hbm3>

**Provenance:** public mirror of a JEDEC copyrighted standard, not the canonical JEDEC distribution endpoint. That mirror status is preserved rather than silently upgraded to official-host provenance.

### §6.3.2.6 — periodic per-bank refresh

The inspected `REFpb` clause establishes:

- row selection comes from internal refresh counters;
- rules apply within each SID;
- one of the 16 banks per SID may be selected in any order;
- a bank may not receive another `REFpb` until all banks in that SID have received one;
- the controller must track which bank is being refreshed;
- the example advances ordinary refresh progress after a complete 16-bank set.

Grounded relation:

```text
single REFpb target
    !=
complete periodic-refresh coverage
```

Order is flexible; coverage is not optional.

### §6.3.2.7 — Refresh Management

The RFM clause establishes:

- high DRAM activity may require extra management to protect stored data;
- the device exposes whether additional RFM beyond ordinary refresh is required;
- a suggested controller implementation uses per-bank Rolling Accumulated ACTIVATE (`RAA`);
- ACTIVATE increments the selected bank's RAA;
- `RAAIMT` is a vendor-provided initial management threshold;
- `RFMab` grants all-bank management time;
- `RFMpb` grants single-bank management time.

Most importantly, the standard gives RFM and REF similar command-duration classes but states that the rolling-all-bank requirement for `REFpb` **does not apply to `RFMpb`**.

Grounded relation:

> **same per-bank command geometry/duration class ≠ same coverage obligation**

### RAA maximum and service admission

The standard permits RFM to be postponed only while RAA remains below vendor-provided `RAAMMT`. At `RAAMMT`, further ACTIVATE commands to the bank are disallowed until REF/RFM reduces RAA.

This is a protocol limit, not a statement that corruption occurs exactly at that threshold:

> **management/admission threshold ≠ observed bit-flip threshold**

### Periodic REF remains independent

The standard explicitly says RFM:

- does not replace periodic REF;
- does not affect the ordinary internal refresh counters;
- supplies extra/bonus time for internal management.

It also allows ordinary REF to decrement RAA for affected banks.

Therefore:

```text
periodic refresh-progress state
    !=
activity-pressure state
```

while one REF event can influence both.

### Self-refresh

The standard allows per-bank RAA values to reset after self-refresh lasting at least `tRAASRF`, while shorter self-refresh entry/exit does not decrement RAA.

This supports only a bounded engineering reconstruction: a history-dependent activity budget can be discarded after a qualifying maintenance regime. It does not identify the hidden work performed during that interval.

---

## Source 2 — JESD238A, January 2023

**Document:** JEDEC, _High Bandwidth Memory DRAM (HBM3)_, JESD238A, January 2023.  
**Public text mirror inspected:** <https://studylib.net/doc/27298996/jesd238a>

The title page identifies JESD238A as a revision of **JESD238, January 2022**. The inspected 2023 clauses preserve the bounded Case-112 relations:

- periodic `REFpb` complete-bank coverage;
- `RFMpb` exemption from the rolling rule;
- one-bank `RFMpb` targeting;
- `RAAMMT` ACTIVATE admission limit;
- RFM independence from periodic REF/internal refresh counters;
- sustained-self-refresh RAA reset.

This is revision continuity across the two inspected editions, not a universal statement about every later HBM standard or every product.

---

## Source 3 — Kim et al., ISCA 2014

**Institutional page:** <https://istc-cc.cmu.edu/publications/papers/2014/kim-isca14_abs.shtml>

The CMU publication record reports that repeated activation of the same DRAM row can corrupt nearby rows; the study induced errors in 110 of 129 modules from three manufacturers and related repeated wordline toggling to accelerated leakage in nearby rows.

It is included only as an earlier open anchor for **activation-conditioned DRAM integrity risk**.

It does not establish that:

- JESD238 RFM derives from this paper;
- HBM3 implements PARA;
- RAA thresholds map to the paper's observed activation counts;
- HBM3 internal mitigation uses the same victim logic.

> **earlier disturbance evidence ≠ demonstrated RFM genealogy**

---

## Cross-case boundary

**Case 54:** owns the broad DDR5 `device requirement + controller RAA + opaque in-DRAM work` decomposition. Case 112 adds only HBM3-specific target/coverage geometry.

**Case 105:** establishes per-bank transaction granularity while preserving full periodic-retention coverage.

**Case 106:** establishes a DDR5 same-bank-index parallel target set under periodic coverage accounting.

The bounded HBM3 contrast is:

```text
REFpb:
    one bank per transaction
    + rolling all-bank periodic coverage

RFMpb:
    one selected bank
    + no rolling-all-bank requirement
    + activity-pressure accounting
```

These are functional comparisons, not genealogy claims.

## computing-archaeology reuse check

Searches in `tmzncty/computing-archaeology` for `HBM`, `HBM3`, and `HBM3 RFM` found no dedicated case to reuse. General HBM standards/packaging/product history remains out of scope here.

## Claim ledger

| Claim | Type | Strength |
| --- | --- | --- |
| JESD238 is dated Jan. 2022 | H/P | strong |
| JESD238A is dated Jan. 2023 and revises Jan. 2022 JESD238 | H/P | strong |
| periodic `REFpb` must cover all banks before repeat | H/P | strong |
| `RFMpb` is exempt from that rolling requirement | H/P | strong |
| `RFMpb` targets one selected bank | H/P | strong |
| RFM does not replace REF or advance internal refresh counters | H/P | strong |
| REF may decrement RAA | H/P | strong |
| `RAAMMT` blocks more ACTIVATE until maintenance | H/P | strong |
| long-enough self-refresh may reset RAA | H/P | strong |
| RAA is maintenance state rather than payload | E | strong |
| RAA is wall-clock retention age | X | rejected |
| RAA threshold is a measured corruption threshold | X | rejected |
| RFM completion identifies a victim row | X | rejected |
| HBM3 `RFMpb` equals DDR5 `RFMsb` target geometry | X | rejected |
| Kim 2014 proves direct HBM3 genealogy | X | rejected |
| Jan. 2022 is RFM invention priority | X | rejected |

## Open evidence

Pre-2022 committee drafts/patents; named HBM3 RFM parameter values; controller bookkeeping/scheduling; independent command traces; hidden internal mitigation; commercial ARFM policy and later HBM revisions beyond the inspected 2022–2023 contract; threshold and missed-RFM fault injection.
