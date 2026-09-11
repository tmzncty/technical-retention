# Case 151 — DDR5 Same Bank Refresh: Partitioned Refresh Scope, Concurrent Service, and Retention Scheduling

Status: grounded

## 0. Research Status Snapshot

- **Historical record:** grounded at a conservative public boundary. JEDEC announced publication of JESD79-5 DDR5 on 2020-07-14; current Micron DDR5 documentation describes SAME BANK REFRESH (`REFsb`). A Micron-origin 2014 LPDDR2 product manual preserved on a third-party mirror provides an earlier, product-specific per-bank-refresh prior-art floor.
- **Engineering reconstruction:** grounded only at the public command/interface level. `REFsb` partitions a refresh episode to the same bank number across bank groups while non-targeted banks remain eligible for other commands subject to DDR5 timing rules. No hidden controller scheduler, cell circuit, or product firmware is inferred.
- **Functional analogy:** bounded. Cases 03, 09, and 10 study other dimensions of DRAM refresh; LPDDR2 `REFpb` provides earlier bank-scoped refresh chronology. Similarity does not establish an identical state machine or direct genealogy.
- **Philosophical interpretation:** interpretation only. A persistence obligation may be spatially scoped: some state can be under compulsory maintenance while other state remains available for foreground use.

## 1. Problem Statement

DRAM refresh is compulsory restorative maintenance, but the existence of a refresh obligation does not by itself determine how much of a memory device must become unavailable during each maintenance episode.

DDR5 `REFsb` is a useful retention case because it makes that distinction explicit. Micron describes the command as refreshing a bank in each bank group while keeping the other banks available for access. The preservation obligation therefore remains device-wide over time, but a particular refresh operation can have a narrower spatial scope.

The bounded question is:

> What must remain true for DDR5 data retention when the maintenance that restores charge is partitioned across banks rather than expressed only as whole-array blocking work?

## 2. Boundary and Stop Conditions

### In scope

- the public DDR5 `REFsb` command relation;
- bank-group/bank maintenance scope and foreground-access consequences;
- a conservative 2020 public DDR5-standard boundary;
- Micron LPDDR2 `REFpb` as an earlier bank-scoped-refresh prior-art floor;
- comparison with Cases 03, 09, 10, and 150;
- retention-specific interpretation of spatially partitioned maintenance.

### Out of scope

- exact JEDEC timing tables not reproduced in the public sources used here;
- hidden memory-controller scheduling algorithms;
- DRAM cell-circuit implementation of refresh;
- RowHammer/TRR policy;
- per-row individualized retention profiling;
- claims that DDR5 invented bank-scoped refresh;
- claims of direct LPDDR2-to-DDR5 genealogy;
- ECC scrub, data-integrity proof, or media sanitization.

## 3. Evidence Matrix

| ID | Evidence | Type | Supports | Does not support |
|---|---|---|---|---|
| E151.1 | JEDEC publication announcement mirrored by Design-Reuse, 2020-07-14 | institutional historical record, mirrored | public publication boundary for JESD79-5 DDR5 | invention date; exact normative `REFsb` wording |
| E151.2 | Micron DDR5 SDRAM product documentation | first-party technical | DDR5 exposes all-bank and same-bank refresh; `REFsb` refreshes a bank in each bank group | controller microarchitecture; implementation genealogy |
| E151.3 | Micron DDR5 feature explanation | first-party technical | targeted banks must be idle; untargeted banks can remain available subject to timing restrictions | universal performance gain; no stalls of any kind |
| E151.4 | Micron-origin 2014 LPDDR2 manual mirrored by Doczz | historical vendor manual mirror (`H/P*`) | `REFpb` existed on a named LPDDR2 product family; target bank inaccessible while other banks can be read/written | origin-hosted archival provenance; DDR5 equivalence or lineage |
| E151.5 | Micron current legacy-part catalog for EDB4432BBPA | first-party product identity | the mirrored manual corresponds to a real Micron/Elpida LPDDR2 part family | the detailed refresh text by itself |

## 4. Historical Record

### 4.1 DDR5 public boundary: 2020, not an invention claim

JEDEC's publication announcement for JESD79-5 is dated **2020-07-14**. This is used only as a conservative public standard boundary. It is not treated as the date on which bank-scoped refresh was invented, nor as proof that every DDR5 implementation immediately shipped with the same controller policy.

Micron's current DDR5 product material contrasts earlier DDR refresh support with DDR5's addition of `REFsb`: the command refreshes a bank in each bank group rather than requiring an all-bank refresh episode.

### 4.2 What `REFsb` changes

Micron's DDR5 feature explanation is more precise than the label “same bank” alone. The command targets **the same bank number across bank groups**. On the cited 16Gb x4/x8 organization, only one bank in each bank group needs to be idle for the command; the remaining banks need not all be idle and remain available subject to the specified timing restrictions.

Therefore:

- `same-bank wording != exactly one physical bank total`;
- `some bank scope under refresh != all banks unavailable`;
- `foreground service continuity != absence of retention maintenance`.

The data in the targeted banks still depends on periodic restorative work. What changes is the service-blocking scope of a particular maintenance episode.

### 4.3 Earlier bank-scoped prior art: LPDDR2 in 2014

A Micron-origin LPDDR2 product manual, Rev. A 07/14, preserved by a third-party documentation mirror, describes a per-bank refresh command (`REFpb`). It states that the target bank is inaccessible during its per-bank refresh cycle while other banks remain accessible and may receive reads or writes. Micron's current legacy catalog independently identifies the `EDB4432BBPA` family as LPDDR2.

This establishes a bounded prior-art floor: **bank-scoped DRAM refresh was publicly documented on a named Micron/Elpida LPDDR2 product family by 2014**, before JESD79-5 DDR5 was published in 2020.

It does **not** establish that LPDDR2 `REFpb` and DDR5 `REFsb` are the same state machine. In the LPDDR2 document, a device-internal bank counter schedules the target bank in a round-robin sequence; Micron's DDR5 description instead says `REFsb` targets the same bank number across bank groups. Earlier chronology therefore blocks a novelty overclaim but does not prove direct genealogy.

## 5. Engineering Reconstruction

At the public-interface level, a bounded reconstruction is:

1. DRAM cells remain subject to a periodic refresh obligation.
2. The controller reaches a point at which a bank-scoped refresh episode is due and legal under the command/timing contract.
3. A DDR5 `REFsb` command selects a bank number across the bank groups.
4. The targeted banks are unavailable for the refresh interval.
5. Non-targeted banks remain eligible for foreground commands, subject to the command/timing restrictions that still apply.
6. After the refresh interval, the targeted banks return to ordinary access eligibility.
7. Repeating such scoped episodes over time satisfies the broader retention schedule.

This is an **interface-level reconstruction**, not a claim about silicon micro-operations or a particular memory-controller scheduler.

The relevant retained state categories are also distinct:

- **payload state:** charge patterns representing user/system data in DRAM cells;
- **maintenance obligation:** the requirement that restorative refresh continue within timing limits;
- **maintenance scope/control state:** which bank set a given refresh episode targets and which commands are legal while it is in progress.

The refresh-control relation is not another payload replica and not a full history of prior refresh events.

## 6. What This Case Does Not Mean

### 6.1 Bank-scoped refresh is not individualized retention profiling

`REFsb` exposes a spatial command granularity. It does not, from the evidence used here, say that each row has its own measured leakage rate or individualized retention deadline. Case 10 addresses adaptive cadence/leakage ideas; Case 151 addresses spatial maintenance scope.

### 6.2 Interface capability is not deployed scheduling policy

The existence of `REFsb` does not prove how often a real CPU memory controller uses it, how it trades it against all-bank refresh, or how workloads affect its policy. Those claims require controller-specific documentation or traces.

### 6.3 Refresh is not ECC scrub or sanitization

Refresh restores volatile charge so valid data remains readable. It is not, by itself, an error-correction scrub that proves integrity, and it is not a deletion/sanitization procedure intended to make prior data irrecoverable.

## 7. Cross-Case Comparison

| Case | Maintenance / retained relation | Main variable | Key distinction from Case 151 |
|---|---|---|---|
| Case 03 — DRAM scheduled restoration | periodic charge restoration | cadence | Case 151 asks how one mandatory refresh episode is spatially partitioned |
| Case 09 — CBR refresh address internalization | device-managed refresh sequencing | address/control ownership | internalizing refresh address generation is different from limiting service-blocking scope |
| Case 10 — leakage-tracked self-refresh | adaptive maintenance cadence | time / sensed retention need | Case 151 does not infer per-row leakage profiling |
| Case 150 — managed-SSD garbage collection | background relocation + erase | reclamation scope/opportunity | only a functional analogy: foreground service can coexist with maintenance; medium, mechanism, and persistence problem differ |

## 8. Related Repository Boundary

`tmzncty/computing-archaeology` was searched for a dedicated `per-bank refresh` / `REFsb` topic before this case was opened; no dedicated treatment was found.

The broad historical genealogy of LPDDR/DDR refresh commands, memory-controller policy evolution, DRAM-bank organizations, and platform adoption belongs primarily in `computing-archaeology`. This case keeps only the bounded retention relation: **mandatory restorative maintenance can be spatially partitioned without turning the rest of the memory device into “not under retention.”**

## 9. Philosophical Interpretation

**Interpretation only:** persistence is not equivalent to global quiescence. A technical system can preserve a whole by rotating a maintenance relation across parts, temporarily withdrawing one scope from foreground use while leaving other scopes current and serviceable.

This is a useful abstraction for `technical-retention`, but it must not be mistaken for historical actor language or proof that unrelated maintenance systems share a common implementation lineage.

## 10. Open Questions

- obtain an archival/origin-hosted copy of the 2014 Micron LPDDR2 manual rather than relying on the preserved vendor-document mirror;
- recover and quote the exact normative JESD79-5 `REFsb` wording from a lawfully accessible standards copy;
- identify a named shipped DDR5 memory controller and document when/how it selects `REFsb` versus all-bank refresh;
- quantify workload-visible effects with product/platform measurements without confusing performance results with retention semantics;
- trace LPDDR2 `REFpb`, later LPDDR generations, and DDR5 `REFsb` historically in `computing-archaeology` before asserting genealogy.

## Sources

1. Micron Technology, **DDR5 DRAM** product page, current first-party comparison table: https://www.micron.com/products/memory/dram-components/ddr5-sdram
2. Micron Technology, **Micron DDR5 SDRAM: New Features**, current first-party technical material: https://assets.micron.com/adobe/assets/urn%3Aaaid%3Aaem%3A5ea148c8-e3fe-489e-8489-99b1b9cdcd3c/renditions/original/as/ddr5-new-features-white-paper.pdf
3. JEDEC press-release text mirrored by Design-Reuse, **JEDEC Publishes New DDR5 Standard for Advancing Next-Generation High Performance Computing Systems**, 2020-07-14: https://www.design-reuse.com/news/8558-jedec-publishes-new-ddr5-standard-for-advancing-next-generation-high-performance-computing-systems/
4. Micron Technology, current legacy LPDDR catalog entry for `EDB4432BBPA-1D-F`: https://www.micron.com/products/memory/dram-components/lpddr-components/part-catalog/part-detail/edb4432bbpa-1d-f
5. Micron-origin **168-Ball, Single-channel Mobile LPDDR2 SDRAM**, Rev. A 07/14, preserved vendor-document mirror: https://doczz.net/doc/8137024/168-ball--single-channel-mobile-lpddr2-sdram
