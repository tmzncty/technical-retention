# Evidence 151 — DDR5 Same-Bank Refresh and Earlier Bank-Scoped DRAM Refresh (2014–2020)

Status: grounded evidence record

## Research Question

What public evidence is sufficient to establish that DDR5 exposes a bank-partitioned refresh mechanism that can preserve foreground access to untargeted banks, while also preventing the overclaim that DDR5 invented bank-scoped DRAM refresh?

## Evidence Classification

### E151.1 — JESD79-5 public publication boundary

- **Source:** JEDEC press-release text mirrored by Design-Reuse, 2020-07-14.
- **Class:** institutional historical record, preserved mirror (`I/H*`).
- **Claim supported:** JEDEC publicly announced publication of JESD79-5 DDR5 SDRAM on 2020-07-14.
- **Strength:** strong for public chronology.
- **Stop condition:** does not establish invention date, implementation date for every product, or exact normative `REFsb` language.

### E151.2 — Micron DDR5 command comparison

- **Source:** Micron first-party DDR5 SDRAM product documentation.
- **Class:** primary technical (`P`).
- **Claim supported:** DDR5 supports all-bank and same-bank refresh; Micron describes `REFsb` as refreshing a bank in each bank group.
- **Strength:** strong for public product/interface semantics.
- **Stop condition:** no inference about hidden controller scheduling or direct genealogy.

### E151.3 — Micron `REFsb` access-scope explanation

- **Source:** Micron first-party **DDR5 SDRAM: New Features** technical material.
- **Class:** primary technical (`P`).
- **Claim supported:** `REFsb` targets the same bank number across bank groups; targeted banks must be idle before refresh; non-targeted banks need not all be idle and remain available subject to refresh timing restrictions.
- **Strength:** strong for command-scope engineering reconstruction.
- **Stop condition:** does not mean every bank is always accessible or that `REFsb` creates zero workload stalls.

### E151.4 — 2014 Micron-origin LPDDR2 `REFpb` manual

- **Source:** **168-Ball, Single-channel Mobile LPDDR2 SDRAM**, Rev. A 07/14, Micron Technology copyright 2014, preserved by Doczz.
- **Class:** historical vendor-document mirror (`H/P*`).
- **Claim supported:** a named Micron/Elpida LPDDR2 family documented per-bank refresh (`REFpb`) by 2014; target bank is inaccessible during `tRFCpb`, while other banks remain accessible and may receive READ/WRITE commands; target bank selection follows a device bank counter.
- **Strength:** good prior-art floor, downgraded for non-origin hosting.
- **Stop condition:** do not call it an origin-hosted primary copy; do not infer that DDR5 `REFsb` is the same state machine.

### E151.5 — Current Micron legacy-part identity

- **Source:** Micron current catalog for `EDB4432BBPA-1D-F` / obsolete LPDDR family.
- **Class:** primary product identity (`P`).
- **Claim supported:** the part family represented in the preserved 2014 manual is a real Micron/Elpida LPDDR2 product family.
- **Strength:** corroborates provenance/product identity, not detailed command semantics.

## Claim Matrix

| Claim | Classification | Evidence | Confidence |
|---|---|---|---|
| JESD79-5 was publicly announced as published on 2020-07-14 | historical record | E151.1 | high |
| DDR5 `REFsb` refreshes a bank in each bank group | historical/technical record | E151.2–E151.3 | high |
| Untargeted banks can remain available while the selected same-bank set is refreshing, subject to timing rules | technical record | E151.3 | high |
| `same bank` does not mean exactly one physical bank in the entire device | engineering interpretation of public command scope | E151.3 | high |
| LPDDR2 `REFpb` already provided product-documented bank-scoped refresh by 2014 | prior-art historical record | E151.4–E151.5 | medium-high |
| DDR5 invented bank-scoped refresh | rejected claim | E151.4 | high confidence rejection |
| LPDDR2 `REFpb` directly caused or evolved into DDR5 `REFsb` | genealogy claim | not established | unsupported |
| `REFsb` implies per-row individualized retention profiling | implementation claim | not established | unsupported |
| a real DDR5 controller necessarily uses `REFsb` whenever possible | product policy claim | not established | unsupported |

## Engineering Reconstruction Boundary

The strongest safe reconstruction is interface-level:

`periodic refresh obligation -> legal REFsb opportunity -> selected bank number across bank groups enters refresh interval -> untargeted banks remain command-eligible subject to timing -> selected banks return to ordinary access -> repeated scoped episodes satisfy broader refresh schedule`

This reconstruction does **not** specify:

- how a CPU memory controller chooses between `REFab` and `REFsb`;
- exact silicon refresh micro-operations;
- row-remap/ECC/TRR interaction;
- workload-dependent scheduling heuristics;
- any undisclosed queue, timer, or persistent controller state.

## Prior-Art and Anti-Anachronism Notes

1. **2020 is a public DDR5 standard boundary, not an invention date.**
2. **2014 LPDDR2 is an earlier named-product bank-scoped-refresh floor, not proof of the first such implementation.**
3. `LPDDR2 REFpb != DDR5 REFsb`: the public targeting contracts differ.
4. Earlier chronology does not establish genealogy.
5. Current Micron DDR5 explanations are used to describe the public feature; they are not silently projected backward into the 2014 LPDDR2 state machine.
6. The 2014 manual is a vendor-origin document on a third-party mirror and is therefore explicitly downgraded to `H/P*` pending a better archival/origin copy.

## Cross-Case Limits

- **Case 03:** periodic restorative maintenance; Case 151 adds spatial partitioning of a refresh episode.
- **Case 09:** CBR/internal refresh address ownership; Case 151 is about service/maintenance scope rather than who advances the refresh address.
- **Case 10:** adaptive self-refresh cadence; Case 151 does not imply individualized leakage sensing.
- **Case 150:** managed-SSD GC can coexist with foreground service, but this is only a functional analogy. SSD reclamation, DRAM charge restoration, and their persistence states are unrelated mechanisms.

## Related-Repository Check

A repository search of `tmzncty/computing-archaeology` for `per-bank refresh` / `REFsb` found no dedicated case before this slice was opened. Broader DDR/LPDDR command genealogy, controller adoption, and DRAM organization history should be developed there rather than duplicated here.

## Sources

- Micron DDR5 SDRAM: https://www.micron.com/products/memory/dram-components/ddr5-sdram
- Micron DDR5 feature material: https://assets.micron.com/adobe/assets/urn%3Aaaid%3Aaem%3A5ea148c8-e3fe-489e-8489-99b1b9cdcd3c/renditions/original/as/ddr5-new-features-white-paper.pdf
- JEDEC publication announcement mirror, 2020-07-14: https://www.design-reuse.com/news/8558-jedec-publishes-new-ddr5-standard-for-advancing-next-generation-high-performance-computing-systems/
- Micron legacy LPDDR part identity: https://www.micron.com/products/memory/dram-components/lpddr-components/part-catalog/part-detail/edb4432bbpa-1d-f
- Micron-origin 2014 LPDDR2 manual mirror: https://doczz.net/doc/8137024/168-ball--single-channel-mobile-lpddr2-sdram
