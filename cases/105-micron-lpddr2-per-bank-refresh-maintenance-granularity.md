# Micron LPDDR2 Per-Bank REFRESH: Maintenance Granularity, Full-Array Obligation, and Service Concurrency

## Status

**`grounded`** — bounded to Micron Mobile LPDDR2 manufacturer documentation from 2014–2015, especially the 168-ball single-channel family, with no invention-priority or complete JEDEC-genealogy claim.

Grounding record: [`../evidence/105-micron-2014-2015-lpddr2-per-bank-refresh-grounding.md`](../evidence/105-micron-2014-2015-lpddr2-per-bank-refresh-grounding.md).

## Scope

Cases 03, 09, 10, 21, 69, and 104 already separate the DRAM refresh deadline, refresh-row enumeration, autonomous scheduling, maintenance-authority handoff, bounded timing elasticity, and self-refresh rate/coverage policy. Case 104 leaves one specific normal-operation question open:

> What changes when one refresh transaction can target **one bank** while the device still owes a recurring refresh obligation across the full bank set?

The bounded object here is Micron's Mobile LPDDR2 `REFpb` / `REFab` contract. The main primary witness is Micron's _168-Ball, Single-channel Mobile LPDDR2 SDRAM_, Rev. A (July 2014), supplemented by a December 2014 automotive LPDDR2 document as a same-manufacturer continuity check.

This case is not a general LPDDR2 or JEDEC history. It does not establish who invented per-bank refresh, when the feature first entered a normative standard, or how every controller scheduled it.

## Historical record

### H/P — Micron names per-bank refresh as a concurrency feature

The July 2014 Micron datasheet lists `8 internal banks for concurrent operation` and `Per-bank refresh for concurrent operation` among the product features. In the REFRESH-command section, Micron distinguishes:

- `REFpb` — a per-bank refresh operation;
- `REFab` — an all-bank refresh operation.

For the documented eight-bank devices, the per-bank sequence is a fixed round-robin over banks 0 through 7. The controller must track which bank is being refreshed, and the bank count can be synchronized to zero by RESET or on exit from self refresh.

This is manufacturer interface vocabulary. `maintenance granularity`, `refresh debt`, and `retained set` below are project-level engineering terms.

### H/P — One target bank is unavailable while other banks may remain in service

Micron states that the target bank is inaccessible for the per-bank refresh cycle time `tRFCpb`. Other banks, however, remain addressable during that interval and may stay active or receive READ/WRITE commands.

When the REFpb cycle completes, the affected bank returns to the idle state. A target bank must have been idle before the REFpb operation begins.

Thus the documented maintenance event can temporarily withdraw service from one bank without imposing a whole-device service blackout.

### H/P — Per-bank transaction scope does not remove the full refresh obligation

The same datasheet defines a minimum number `R` of refresh commands inside each rolling refresh window `tREFW`. For devices supporting per-bank refresh, Micron states that one REFab can be replaced by **a full cycle of eight REFpb commands**.

This is the decisive retention boundary. A single-bank maintenance transaction is not permission to preserve only one bank. The smaller transaction scope is nested inside a continuing coverage obligation over the bank set and rolling refresh window.

### H/P — All-bank refresh and per-bank refresh are not command-identical

REFab requires all banks to be idle and refreshes all banks together. It also synchronizes the controller/device bank count to zero. REFpb instead targets the bank selected by the device's fixed bank counter and permits activity in the non-target banks.

The fact that eight REFpb commands can replace one REFab for the documented refresh-accounting requirement therefore does not make the two command forms operationally identical.

## Retained state and control state

At least four state classes must remain distinct:

1. **payload state** — charge-encoded user data in the DRAM arrays;
2. **maintenance-coverage obligation** — the requirement that sufficient refresh work occur across the rolling refresh window;
3. **bank-target tracking state** — the controller/device relation identifying which bank the next REFpb affects;
4. **service/admission state** — whether the target and non-target banks can accept ordinary accesses during the maintenance interval.

Only the first class is user payload. The other relations help determine whether and when that payload remains maintainable and serviceable.

## Engineering reconstruction

### E — Maintenance transaction scope is not the same thing as retained-set scope

Case 104's PASR can deliberately shrink the subset promised retention in self refresh. REFpb does something different: it shrinks the **scope of one refresh transaction** while the rolling-window requirement still composes those transactions into full-bank maintenance coverage.

> **maintenance transaction scope ≠ retained set**

and, more specifically:

> **REFpb ≠ PASR**.

### E — Localized maintenance can coexist with service concurrency

During `tRFCpb`, the target bank is unavailable while other banks remain usable. The system therefore exposes a three-way distinction:

```text
payload retained in a bank
    !=
bank currently undergoing maintenance
    !=
bank currently admissible for ordinary service
```

Temporary service withdrawal for one bank is not evidence that its data have been forgotten, and concurrent service from another bank is not evidence that the target bank has completed its refresh work.

### E — One refresh event does not discharge the whole refresh obligation

A single REFpb is a completed maintenance transaction for one target bank, but the documented refresh contract is expressed over a rolling window and, for the eight-bank substitution, a complete bank cycle.

> **one completed REFpb ≠ full-array refresh obligation satisfied**.

This matters for retention analysis because `maintenance completed` requires a typed scope and accounting horizon.

### E — Scheduling state can be retention infrastructure

The controller's obligation to track the per-bank sequence is not user data, yet loss or desynchronization of that relation would undermine correct future maintenance scheduling. REFab/RESET/self-refresh-exit synchronization therefore concerns a small control relation whose correctness helps preserve a much larger volatile payload.

This does not establish how the bank counter is physically implemented or retained inside every controller/device.

### E — Scheduling flexibility does not abolish deadlines

Micron permits distributed/burst refresh patterns under explicit rolling-window conditions. Per-bank granularity creates additional scheduling freedom and concurrency, but the minimum refresh requirement remains.

> **more scheduling freedom ≠ maintenance optionality**.

## Contrast with Case 104

Cases 104 and 105 are intentionally adjacent because they expose two superficially similar but technically different meanings of `partial` maintenance:

```text
Case 104 — PASR
    changes which regions are promised maintenance in self refresh
    excluded regions may lose data

Case 105 — REFpb
    changes which bank one normal-operation refresh transaction services
    repeated transactions still satisfy a full-bank rolling-window obligation
```

Thus `partial-array retention` and `per-bank maintenance transaction` must not be collapsed into a single idea of partial refresh.

## Prior-art boundary

This case establishes a dated **Micron product-document floor no later than July 2014** for the bounded LPDDR2 REFpb semantics described above. It makes no claim that Micron originated the mechanism or term.

A complete history would require revision-by-revision JEDEC evidence, earlier vendor/product documents, controller implementations, and cross-vendor comparison. That broader engineering genealogy belongs primarily in `computing-archaeology` if pursued.

## Functional analogy and philosophical limit

A functional analogy to rotating maintenance windows is useful: maintenance can be localized so that other regions remain available. The analogy stops at the engineering relation. A DRAM bank is not an archival collection, REFpb does not perform cultural selection, and bank scheduling supplies no evidence for a philosophical theory of memory or forgetting by itself.

The bounded conceptual result is narrower:

> apparent continuous availability can depend on maintenance whose **transaction scope is local** while whose **retention obligation is global over time**.

## Cross-case result

The DRAM refresh decomposition can now be extended without turning it into a historical ladder:

```text
Case 03   leakage creates a refresh deadline
Case 09   refresh-row enumeration can move on-chip
Case 10   refresh scheduling can become autonomous and condition-derived
Case 21   recurring refresh responsibility can hand off between controller and SDRAM
Case 69   external refresh issue time can have bounded scheduling elasticity
Case 104  self-refresh cadence and retained coverage can vary independently
Case 105  one refresh transaction can be bank-local while the rolling retention obligation remains bank-complete
```

This is a functional decomposition, not a proof of direct genealogy.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| the bounded Micron LPDDR2 family exposes separate REFpb and REFab operations | H/P | Micron Rev. A 07/14, REFRESH-command section |
| REFpb targets one bank selected by a fixed round-robin bank counter | H/P | Micron printed p. 81 |
| the controller must track the bank being refreshed | H/P | Micron printed p. 81; automotive Rev. B 12/14 continuity |
| the REFpb target bank is inaccessible during `tRFCpb` while other banks may be read/written | H/P | Micron printed p. 82 |
| one REFab can be replaced by a full cycle of eight REFpb commands for the documented refresh requirement | H/P | Micron printed p. 83 |
| per-bank transaction scope is equivalent to PASR retention-scope reduction | X | contradicted by the documented full-cycle refresh accounting and Case 104 PASR semantics |
| one completed REFpb proves the whole array is freshly maintained | X | outside command scope; rolling/full-cycle requirement remains |
| Micron invented per-bank refresh in 2014 | X | not established; this is only a dated manufacturer-product witness |

## Related repositories

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated LPDDR2 REFpb or DDR5 REFsb case. [`Case 106`](106-ddr5-same-bank-refresh-parallel-target-set.md) now handles the bounded later DDR5 same-bank target-set / coverage-accounting relation while preserving Case 105's one-bank LPDDR2 boundary. Full JEDEC genealogy beyond these bounded source floors, earlier prior art, controller scheduling history, and cross-vendor implementation should be developed there if pursued broadly.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the anti-anachronism guard: `maintenance transaction scope`, `refresh debt`, and `retained set` are present analytical terms, not vocabulary attributed to Micron engineers.

## Sources

1. Micron Technology, Inc., _168-Ball, Single-channel Mobile LPDDR2 SDRAM_, `168b_12x12_4-16gb_2e0e_lpddr2.pdf`, Rev. A, July 2014, especially printed pp. 1 and 81–83. Manufacturer PDF preserved by Mouser: <https://www.mouser.com/datasheet/2/671/168b_12x12_4%2016gb_2e0e_mobile%20lpddr2-1283387.pdf>.
2. Micron Technology, Inc., _1Gb: x16, x32 Automotive Mobile LPDDR2 SDRAM_, `1gb_mobile_lpddr2_u88m_ait_aat.pdf`, Rev. B, December 2014, especially printed pp. 55–56 and refresh-requirement tables. Manufacturer text preserved by DTSheet: <https://dtsheet.com/doc/1384685/1gb--x16--x32-automotive-lpddr2-sdram>.
