# Micron LPDDR2 Per-Bank REFRESH: Maintenance Granularity, Full-Array Obligation, and Service Concurrency

## Status

**`grounded`** — bounded to Micron Mobile LPDDR2 manufacturer documentation from 2014–2015, now independently cross-checked against a June-2012 SK hynix LPDDR2-S4B product specification and a 2009 Hynix manufacturer-primary per-bank-refresh design disclosure, with no invention-priority or complete JEDEC-genealogy claim.

Grounding record: [`../evidence/105-micron-2014-2015-lpddr2-per-bank-refresh-grounding.md`](../evidence/105-micron-2014-2015-lpddr2-per-bank-refresh-grounding.md).

Cross-vendor / prior-art deepening: [`../evidence/105-hynix-2009-2012-per-bank-refresh-prior-art-product-deepening.md`](../evidence/105-hynix-2009-2012-per-bank-refresh-prior-art-product-deepening.md).

## Scope

Cases 03, 09, 10, 21, 69, and 104 already separate the DRAM refresh deadline, refresh-row enumeration, autonomous scheduling, maintenance-authority handoff, bounded timing elasticity, and self-refresh rate/coverage policy. Case 104 leaves one specific normal-operation question open:

> What changes when one refresh transaction can target **one bank** while the device still owes a recurring refresh obligation across the full bank set?

The bounded object here is the LPDDR2 `REFpb` / `REFab` relation. The original primary witness is Micron's _168-Ball, Single-channel Mobile LPDDR2 SDRAM_, Rev. A (July 2014), supplemented by a December 2014 automotive LPDDR2 document as a same-manufacturer continuity check. A June-2012 SK hynix H9TCNNNBLDMMPR specification now supplies an earlier independent product witness for the same bounded interface relation. Hynix US20090116326A1 supplies an earlier manufacturer-primary design-publication floor for per-bank address/control machinery, but is not identified with the later product implementation.

This case is not a general LPDDR2 or JEDEC history. It does not establish who invented per-bank refresh, when the feature first entered a normative standard, how every controller scheduled it, or whether the Hynix patent was implemented in the inspected SK hynix product.

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

## Cross-vendor and earlier-prior-art deepening — Hynix 2009 / SK hynix 2012

Detailed record: [`../evidence/105-hynix-2009-2012-per-bank-refresh-prior-art-product-deepening.md`](../evidence/105-hynix-2009-2012-per-bank-refresh-prior-art-product-deepening.md).

### H/P — Hynix exposed per-bank address/control machinery publicly by May 2009

Hynix Semiconductor's US20090116326A1, published 7 May 2009 from a 2 November 2007 priority filing, describes a semiconductor-memory address counter intended to support per-bank refresh as well as all-bank refresh and self refresh. Its description explicitly separates bank-address and row-address counting/control, says a specific bank may be refreshed while ordinary read/write operations proceed in other banks, and says bank targeting should advance internally in round-robin order.

This is a **manufacturer-primary design disclosure**, not a shipping-product witness. It gives the case an earlier public prior-art floor for the bounded control problem while leaving invention priority and implementation lineage open.

### H/P — a June-2012 SK hynix LPDDR2 product independently exposes the Case-105 relation

SK hynix's _16Gb LPDDR2-S4B (x32, 2CS) H9TCNNNBLDMMPR_, Rev. 1.1 (June 2012), distinguishes REFpb and REFab and specifies the same broad control relation later visible in the Micron product evidence:

- REFpb follows a fixed bank sequence `0-1-2-3-4-5-6-7-...`;
- RESET and every self-refresh exit synchronize the bank count to zero;
- the controller is responsible for tracking which bank is being refreshed;
- the target bank is inaccessible during `tRFCpb` while other banks can remain accessible and receive ordinary operations;
- one REFab may be replaced, for the documented refresh accounting, by one **full cycle of eight REFpb** commands.

The SK hynix product document survives through a third-party PDF mirror. It is therefore treated as manufacturer-authored product documentation with mirror provenance, not as a currently origin-hosted archive.

This moves the bounded cross-vendor product-document floor for Case 105 earlier than the original July-2014 Micron witness. It does not establish the first commercial LPDDR2 per-bank-refresh product.

### H/P — self-refresh exit and PASR sharpen the scope boundary in the same product

The same 2012 SK hynix specification says that self-refresh exit can miss an internally timed refresh event and requires at least one explicit refresh before a subsequent self-refresh entry, glossed as `8 per-bank or 1 all-bank`.

It separately defines PASR bank masking and states that when a bank is masked, refresh to that bank is blocked and data retention by that bank is not guaranteed in self refresh.

The same product therefore supplies a direct internal counterexample to collapsing two kinds of `partial` maintenance:

```text
REFpb
    one transaction targets one bank
    repeated transactions still compose into bank-complete refresh accounting

PASR
    a bank can be excluded from self-refresh maintenance
    retention for that bank is not guaranteed
```

This independently supports the canonical boundary:

> **maintenance transaction scope != retained-set scope**.

## Retained state and control state

At least four state classes must remain distinct:

1. **payload state** — charge-encoded user data in the DRAM arrays;
2. **maintenance-coverage obligation** — the requirement that sufficient refresh work occur across the rolling refresh window;
3. **bank-target tracking state** — the controller/device relation identifying which bank the next REFpb affects;
4. **service/admission state** — whether the target and non-target banks can accept ordinary accesses during the maintenance interval.

Only the first class is user payload. The other relations help determine whether and when that payload remains maintainable and serviceable.

The Hynix/SK hynix deepening adds a useful persistence-horizon boundary: the bank-target relation can be deliberately re-synchronized at RESET or self-refresh exit. It is retention infrastructure for the current maintenance regime, not evidence of durable application history.

## Engineering reconstruction

### E — Maintenance transaction scope is not the same thing as retained-set scope

Case 104's PASR can deliberately shrink the subset promised retention in self refresh. REFpb does something different: it shrinks the **scope of one refresh transaction** while the rolling-window requirement still composes those transactions into full-bank maintenance coverage.

> **maintenance transaction scope ≠ retained set**

and, more specifically:

> **REFpb ≠ PASR**.

The SK hynix 2012 product strengthens this distinction because its REFpb full-cycle accounting and its PASR no-retention guarantee appear in the same manufacturer document.

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

The earlier Hynix patent and the later SK hynix/Micron product documents all support this broad functional partition, but they are not assumed to share an identical circuit implementation.

### E — One refresh event does not discharge the whole refresh obligation

A single REFpb is a completed maintenance transaction for one target bank, but the documented refresh contract is expressed over a rolling window and, for the eight-bank substitution, a complete bank cycle.

> **one completed REFpb ≠ full-array refresh obligation satisfied**.

The cross-vendor deepening sharpens the decomposition:

```text
one REFpb completed
    !=
full eight-bank REFpb cycle completed
    !=
rolling refresh-window obligation satisfied
```

This matters for retention analysis because `maintenance completed` requires a typed scope and accounting horizon.

### E — Scheduling state can be retention infrastructure

The controller's obligation to track the per-bank sequence is not user data, yet loss or desynchronization of that relation would undermine correct future maintenance scheduling. REFab/RESET/self-refresh-exit synchronization therefore concerns a small control relation whose correctness helps preserve a much larger volatile payload.

The 2012 SK hynix reset/self-refresh-exit rule supports a bounded additional relation:

```text
maintenance-control coherence within a regime
    !=
cross-reset durable checkpointing
```

This does not establish how the bank counter is physically implemented or retained inside every controller/device.

### E — Regime transitions can expose follow-up maintenance debt

SK hynix's requirement to issue `8 per-bank or 1 all-bank` refresh before a subsequent self-refresh entry shows that leaving one internally maintained regime can create a bounded handoff obligation before the next regime is admitted.

`maintenance handoff debt` is project vocabulary, not manufacturer terminology.

The source supports only the bounded sequence:

```text
self-refresh exit
    -> possible missed internally timed refresh
    -> explicit follow-up refresh requirement
    -> subsequent self-refresh entry
```

It does not prove a persistent exact refresh-progress checkpoint across power failure.

### E — Scheduling flexibility does not abolish deadlines

Micron permits distributed/burst refresh patterns under explicit rolling-window conditions. SK hynix likewise expresses the obligation over a rolling refresh window while allowing per-bank scheduling and other-bank service. Per-bank granularity creates additional scheduling freedom and concurrency, but the minimum refresh requirement remains.

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

The 2012 SK hynix product document now provides direct same-product evidence for both sides of this contrast: REFpb full-cycle accounting and PASR bank masking with no retention guarantee for the masked bank.

Thus `partial-array retention` and `per-bank maintenance transaction` must not be collapsed into a single idea of partial refresh.

## Prior-art boundary

The prior-art/product chronology is now deliberately split by evidence type:

- **7 May 2009 — manufacturer-primary design-publication floor:** Hynix US20090116326A1 publicly discloses per-bank refresh address/control machinery, one-bank maintenance with other-bank service, and internal bank sequencing. This is not a named-product witness and does not establish invention priority.
- **June 2012 — cross-vendor named-product-document floor:** SK hynix H9TCNNNBLDMMPR Rev. 1.1 documents REFpb/REFab, fixed round-robin target tracking, other-bank service during `tRFCpb`, full-cycle eight-REFpb substitution for one REFab, self-refresh-exit follow-up refresh, and PASR retention withdrawal.
- **July 2014 onward — original Micron grounding:** Micron independently documents the bounded LPDDR2 REFpb/REFab relation and remains the original canonical product witness.

This chronology does **not** prove Hynix -> SK hynix product descent, Hynix -> Micron influence, exact circuit identity, first shipment, first invention, or exact JEDEC clause ancestry.

A complete standards history still requires revision-by-revision JEDEC evidence. Broader circuit/product genealogy belongs primarily in `computing-archaeology` if pursued.

## Functional analogy and philosophical limit

A functional analogy to rotating maintenance windows is useful: maintenance can be localized so that other regions remain available. The analogy stops at the engineering relation. A DRAM bank is not an archival collection, REFpb does not perform cultural selection, and bank scheduling supplies no evidence for a philosophical theory of memory or forgetting by itself.

The bounded conceptual result is narrower:

> apparent continuous availability can depend on maintenance whose **transaction scope is local** while whose **retention obligation is global over time**.

The Hynix/SK hynix evidence adds that a small target-sequence relation can coordinate those local acts without becoming durable application history.

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
Case 106  a later same-bank target set can span corresponding banks across bank groups
```

The 2009–2012 Hynix/SK hynix deepening is a chronological and cross-vendor constraint inside Case 105, not a claim that this list is a direct technology genealogy.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| the bounded Micron LPDDR2 family exposes separate REFpb and REFab operations | H/P | Micron Rev. A 07/14, REFRESH-command section |
| REFpb targets one bank selected by a fixed round-robin bank counter | H/P | Micron printed p. 81 |
| the controller must track the bank being refreshed | H/P | Micron printed p. 81; automotive Rev. B 12/14 continuity |
| the REFpb target bank is inaccessible during `tRFCpb` while other banks may be read/written | H/P | Micron printed p. 82 |
| one REFab can be replaced by a full cycle of eight REFpb commands for the documented refresh requirement | H/P | Micron printed p. 83 |
| Hynix publicly disclosed per-bank refresh address/control circuitry by 7 May 2009 | H/P | US20090116326A1 publication and description |
| the 2009 Hynix disclosure permits ordinary access to other banks while one bank is refreshed and internally sequences bank addresses | H/P | US20090116326A1 description |
| SK hynix H9TCNNNBLDMMPR Rev. 1.1 documents LPDDR2 REFpb/REFab semantics in June 2012 | H/P | SK hynix manufacturer-authored product specification, mirror provenance |
| the 2012 SK hynix product requires controller bank tracking and resets bank count on RESET/self-refresh exit | H/P | SK hynix refresh-command section |
| the 2012 SK hynix product allows one full cycle of eight REFpb to substitute for one REFab in refresh accounting | H/P | SK hynix refresh-requirements section |
| the 2012 SK hynix product requires `8 per-bank or 1 all-bank` refresh before a subsequent self-refresh entry after exit | H/P | SK hynix self-refresh section |
| a PASR-masked bank in the 2012 SK hynix product has no data-retention guarantee in self refresh | H/P | SK hynix PASR bank-masking section |
| the 2009 patent is proven to be the implementation used by the 2012 product | X | not established |
| per-bank transaction scope is equivalent to PASR retention-scope reduction | X | contradicted by full-cycle accounting and explicit PASR retention semantics |
| one completed REFpb proves the whole array is freshly maintained | X | outside command scope; rolling/full-cycle requirement remains |
| Micron invented per-bank refresh in 2014 | X | contradicted as a safe novelty claim by earlier Hynix design/public-product evidence; invention priority still not established |
| identical broad Hynix/SK hynix/Micron semantics prove identical silicon or direct genealogy | X | not established |

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated LPDDR2 REFpb / Hynix per-bank-refresh / DDR5 REFsb study to reuse. [`Case 106`](106-ddr5-same-bank-refresh-parallel-target-set.md) handles the bounded later DDR5 same-bank target-set / coverage-accounting relation while preserving Case 105's one-bank LPDDR2 boundary.

Keep the retention-specific target-scope / coverage-scope distinction, maintenance-control persistence horizon, and PASR counterexample here. Full JEDEC genealogy, pre-2009 circuit history, product/shipment chronology, controller scheduling history, patent-family lineage, and broader cross-vendor implementation history should primarily be developed in `computing-archaeology` if pursued.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the anti-anachronism guard: `maintenance transaction scope`, `refresh debt`, `maintenance handoff debt`, and `retained set` are present analytical terms, not vocabulary attributed to Hynix, SK hynix, Micron, or JEDEC engineers.

## Sources

1. Micron Technology, Inc., _168-Ball, Single-channel Mobile LPDDR2 SDRAM_, `168b_12x12_4-16gb_2e0e_lpddr2.pdf`, Rev. A, July 2014, especially printed pp. 1 and 81–83. Manufacturer PDF preserved by Mouser: <https://www.mouser.com/datasheet/2/671/168b_12x12_4%2016gb_2e0e_mobile%20lpddr2-1283387.pdf>.
2. Micron Technology, Inc., _1Gb: x16, x32 Automotive Mobile LPDDR2 SDRAM_, `1gb_mobile_lpddr2_u88m_ait_aat.pdf`, Rev. B, December 2014, especially printed pp. 55–56 and refresh-requirement tables. Manufacturer text preserved by DTSheet: <https://dtsheet.com/doc/1384685/1gb--x16--x32-automotive-lpddr2-sdram>.
3. Sang Kwon Lee / Hynix Semiconductor Inc., US20090116326A1, _Semiconductor memory device capable of performing per-bank refresh_, published 7 May 2009; priority 2 November 2007; filed 27 June 2008. Google Patents: <https://patents.google.com/patent/US20090116326A1/en>.
4. SK hynix, _16Gb LPDDR2-S4B (x32, 2CS) H9TCNNNBLDMMPR_, MCP Specification, Rev. 1.1, June 2012. Manufacturer-authored PDF surviving through a third-party mirror: <https://14469692.s21i.faiusr.com/61/ABUIABA9GAAgpfTMqgYoysi4pgQ.pdf>. Relevant sections: revision history, `Refresh Command`, `LPDDR2 SDRAM Refresh Requirements`, `Self refresh operation`, and `Partial Array Self Refresh: Bank Masking`.
