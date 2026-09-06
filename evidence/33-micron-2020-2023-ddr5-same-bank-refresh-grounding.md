# Grounding Record — Case 33: Micron DDR5 Same-Bank Refresh

## Decision

**Case status: `grounded`.**

The bounded claim is not a complete DDR5 refresh specification. It is narrower:

> Micron manufacturer documentation from a **November 2019 Rev. A pre-final DDR5 white paper** through 2020–2023 public enablement material consistently identifies `Same Bank Refresh` / `REFsb` as a bank-correlated refresh mode, and the 2019 source additionally records target-idle rules, conditional non-target availability, `tREFSBRD`, FGR cadence, `tRFCsb`, and same-bank ordering for its bounded DDR5 example.

That is enough to ground the retention-specific comparison **refresh obligation ≠ target geometry ≠ service-blocking scope ≠ conditional non-target service ≠ schedule authority**, while leaving final `JESD79-5` revision archaeology, controller compliance, LPDDR/per-bank genealogy, temperature-compensated refresh, and retention-aware policies open.

## Evidence boundary

This record uses public Micron manufacturer sources as the primary evidence layer. The source set now includes Micron's **Rev. A 11/19** white paper **“Micron® DDR5 SDRAM: New Features”** by Randall Rooney and Neal Koyle. The current Micron asset endpoint exposes matching indexed text but rejects direct binary rendering in this research interface; a preserved full-document mirror was therefore inspected for the contiguous refresh section and the revision footer. The official Micron asset URL is retained as the provenance anchor, and the mirror is explicitly identified as a mirror rather than silently treated as Micron hosting.

The 2019 white paper predates the July 2020 final-standard announcement. Its exact `tREFI` / `tRFCsb` / `tREFSBRD` / FGR statements are therefore used only as **manufacturer design/enablement evidence for the bounded 16Gb-era relation**, not as a substitute for a directly inspected final `JESD79-5` revision.

No claim here should be read as a complete normative statement of final DDR5 command legality, all density/revision timing values, or controller compliance.

## Source ledger

### A. Micron DDR5 Technology Enablement Program article

Micron Technology, Inc., **“Micron's DDR5 Technology Enablement Program empowers an ecosystem”**

<https://www.micron.com/about/blog/memory/dram/microns-ddr5-technology-enablement-program-empowers-ecosystem>

Current page inspection on 2026-09-03 establishes:

- Micron states that JEDEC announced the DDR5 standard in **July 2020**;
- in its DDR5 feature list, Micron says DDR5 includes improved refresh schemes (`Same Bank Refresh`) that improve performance by **targeting one bank per bank group**;
- Micron identifies itself as a lead developer of DDR5 specifications, which is relevant to source provenance but is **not** used as an invention-priority claim.

The page itself does not expose a stable publication date in the currently rendered HTML. Source B below bounds its existence by 1 June 2021.

### B. Micron 1 June 2021 press release

Micron Technology, Inc., **“Micron Accelerates Breakthrough Platform Innovation With Advancements Across Industry’s First 176-Layer NAND and 1-Alpha DRAM”**, 1 June 2021.

<https://investors.micron.com/news/press-release/2021/Micron-Accelerates-Breakthrough-Platform-Innovation-With-Advancements-Across-Industrys-First-176-Layer-NAND-and-1-Alpha-DRAM-06-01-2021/default.aspx>

Current page inspection establishes:

- the release is dated **1 June 2021**;
- its DDR5 TEP section describes the program as launched in 2020;
- its resource list directly links **“Micron’s DDR5 Technology Enablement Program Empowers an Ecosystem.”**

Therefore the feature article in Source A demonstrably existed no later than 1 June 2021 even if the current blog template does not expose its original publication date.

### C. Micron DDR5 product page

Micron Technology, Inc., **DDR5 DRAM** product page.

<https://www.micron.com/products/memory/dram-components/ddr5-sdram>

Current page inspection on 2026-09-03 establishes the manufacturer comparison table:

- DDR4 bank organization is shown separately from DDR5 bank-group/bank organization;
- under `PRECHARGE commands`, DDR5 includes `same bank` in addition to all-bank/per-bank forms;
- under `REFRESH commands`, DDR4 is listed as `All bank` while DDR5 is listed as `All bank and same bank`;
- the explanation states: **`REFsb enables refreshing a bank in each BG`**.

This is the strongest currently inspectable public Micron source for the exact bounded wording that `same bank` does not mean one globally singular bank.

Because this is a current product page rather than a frozen 2020 datasheet, it is used as manufacturer institutional confirmation of the feature semantics, not as sole evidence for the feature's original date.

### D. Micron 2023 Intel Xeon / DDR5 article

Micron Technology, Inc., **“Redefining performance With DDR5 and 4th Gen Intel Xeon scalable processors.”**

<https://www.micron.com/about/blog/company/partners/redefining-performance-with-ddr5-and-4th-gen-intel-xeon-scalable>

The page ties its platform context to Intel's **10 January 2023** 4th Gen Xeon Scalable launch and carries ©2023 Micron.

Its RAS section names `Same bank refresh` and explains the practical availability distinction:

- DDR4 is described as locking/refreshing all banks together;
- DDR5 provides greater access through more granular refresh;
- same-bank refresh keeps the other bank groups available so the processor can continue accessing data.

The article also uses the simplifying phrase `refreshing a single bank at a time`. This record does **not** use that phrase to override Sources A/C, whose more precise topology is `one bank per bank group` / `a bank in each BG`.

### E. Micron July 2020 DDR5 TEP release

Micron Technology, Inc., **“Micron Accelerates DDR5 Adoption With Technology Enablement Program,”** 14 July 2020.

Institutional archive entry inspected through Micron Investor Relations:

<https://investors.micron.com/node/41136>

The release states that the DDR5 TEP announcement accompanied JEDEC approval of the DDR5 standard. It is used only to anchor standardization context and Micron participation, not Same Bank Refresh mechanism details.

### F. Micron Rev. A 11/19 DDR5 new-features white paper

Randall Rooney and Neal Koyle, Micron Technology, Inc., **“Micron® DDR5 SDRAM: New Features,”** Rev. A 11/19, document code `CCM004-676576390-11390`.

Official Micron asset:

<https://assets.micron.com/adobe/assets/urn%3Aaaid%3Aaem%3A5ea148c8-e3fe-489e-8489-99b1b9cdcd3c/original/as/ddr5-new-features-white-paper.pdf>

Preserved full-document mirror used for contiguous text/revision inspection:

<https://device.report/m/3d08f1032327cf5fbb74a044017258d62a01653aef88d208c3eef3c4f40754a2>

Inspected refresh-section evidence:

- the document names `ALL-BANK REFRESH (REFab)` and `SAME-BANK REFRESH (REFsb)`;
- `REFsb` targets the same bank in **all bank groups**, selected by bank bits on the command/address interface;
- targeted banks must be idle/precharged before the refresh and cannot resume ordinary reads/writes for the refresh duration;
- in the comparison, `REFab` requires all banks idle, while `REFsb` requires only one bank per bank group idle;
- for the described 16Gb x4/x8 organization, the remaining twelve banks need not be idle, but their access remains subject to `tREFSBRD`;
- `REFsb` is described as FGR-only, with each bank receiving refresh every 1.95 µs on average in that mode;
- the bounded 16Gb example gives `tRFCsb = 130 ns`, compared with 295 ns for the discussed all-bank refresh;
- every same-bank position must receive one `REFsb` before the same position receives a second, while the visit order among bank positions may vary;
- the footer records **©2019 Micron Technology, Inc.** and **Rev. A 11/19**, and warns that products/programs/specifications are subject to change without notice.

Evidence classification: **H/P**, with a hosting/provenance caveat. The content is manufacturer-authored and is independently indexed at the official Micron asset; the inspectable full-document copy is a third-party preservation mirror. This is adequate for the bounded manufacturer design relation, not for final-standard priority or normative-compliance claims.

## Claim-by-claim grounding

### Claim 1 — `Same Bank Refresh` is public DDR5 manufacturer vocabulary no later than 2021

**Status: grounded (`H/P`).**

Source A uses the exact phrase `Same Bank Refresh`; Source B links Source A in a dated 1 June 2021 resource list.

This establishes bounded public manufacturer usage no later than that date.

It does not establish first use of the term.

### Claim 2 — DDR5 Same Bank Refresh targets a bank position across bank groups

**Status: grounded (`H/P`).**

Two Micron formulations converge:

- Source A: `targeting one bank per bank group`;
- Source C: `REFsb enables refreshing a bank in each BG`.

This blocks the misleading simplification `one globally singular bank`.

The case therefore uses **bank-correlated target set across bank groups** as an engineering description while preserving `Same Bank Refresh` / `REFsb` as the historical/manufacturer vocabulary.

### Claim 3 — Same Bank Refresh changes service availability during maintenance

**Status: grounded (`H/P` + `E`).**

Source D states that DDR5's granular same-bank refresh keeps other bank groups available for processor access while refresh occurs.

Source C independently distinguishes all-bank refresh from same-bank refresh.

Engineering reconstruction:

> The retention obligation can remain while the ordinary-service blocking scope is narrowed.

That formulation is project vocabulary, not a quotation or historical term.

### Claim 4 — `refresh obligation ≠ service-blocking scope`

**Status: grounded (`E`).**

Cases 03 and 21 already ground the continuing physical/command-level need for DRAM refresh. Case 33 adds manufacturer evidence that DDR5 can change which bank resources remain accessible during refresh.

The result is relational, not genealogical:

```text
required maintenance exists
    !=
all banked service resources must be unavailable together
```

### Claim 5 — `refresh target geometry ≠ refresh schedule authority`

**Status: grounded as bounded cross-case reconstruction (`E`).**

Case 21 provides a directly sourced distinction between externally repeated `AUTO REFRESH` and internally recurring `SELF REFRESH` in a 1999 Micron SDRAM family.

Case 33's sources describe which banks `REFsb` targets and which remain accessible. They do not document a transfer of recurring-command responsibility equivalent to Case 21 self refresh.

Therefore the two dimensions must remain independent unless another source explicitly ties them together.

### Claim 6 — DDR5 `Same Bank Refresh` is historically identical to every `per-bank refresh` regime

**Status: rejected (`X`).**

Source C itself gives a useful terminology warning: in its feature table, `PRECHARGE` distinguishes `per bank` and `same bank`, while `REFRESH` is presented as `all bank` versus `same bank` for DDR5.

The roadmap's older phrase `per-bank refresh` was a broad research bucket, not a license to normalize DDR5 terminology.

LPDDR and other standards/products using `per-bank refresh` require separate primary evidence.

### Claim 7 — Micron invented Same Bank Refresh

**Status: rejected / unstudied (`X`).**

Sources A/E place Micron inside JEDEC DDR5 specification work and standardization, but do not establish invention priority.

The case uses Micron as a strong first-party witness to a standardized feature, not as a priority claim.

### Claim 8 — 2019 manufacturer `REFsb` timing and sequencing relation

**Status: grounded for the bounded Rev. A 11/19 manufacturer design witness (`H/P`).**

Source F now supports the specific relation that `REFsb` is FGR-only in the described regime, leaves non-target banks available subject to `tREFSBRD`, gives a 1.95 µs average per-bank refresh cadence, gives a 130 ns `tRFCsb` for its 16Gb example, and requires every same-bank position to be serviced before any same-bank position is repeated.

The timing numbers are **not** generalized to every DDR5 density/product/revision.

### Claim 9 — final normative DDR5 `REFsb` contract and controller compliance

**Status: deliberately open.**

The Rev. A 11/19 white paper predates the July 2020 final-standard announcement and explicitly says specifications are subject to change. A future slice must directly inspect relevant final/later `JESD79-5` revisions and, separately, named-controller behavior before making normative or compliance claims. The present deepening therefore closes the bank-structured relation decomposition without converting a manufacturer white paper into the standard itself.

## Terminology control

### Historical / manufacturer vocabulary

- `Same Bank Refresh`;
- `REFsb`;
- `bank group` / `BG`;
- `all bank` refresh;
- DDR4 / DDR5.

### Engineering reconstruction vocabulary

- `refresh target geometry`;
- `maintenance-interference geometry`;
- `service-blocking scope`;
- `maintenance localization`;
- `bank-correlated target set`.

These project terms must not be attributed to Micron or JEDEC actors unless separately sourced.

### Functional analogy only

The observation that localized refresh resembles other technologies that reduce maintenance interference is a **functional analogy** only. It does not establish lineage or technical identity with:

- locality-aware erasure-code repair;
- RAID rebuild throttling;
- SSD garbage collection;
- distributed scrub;
- cache coherence.

## Related-repository check

On 2026-09-06, GitHub code searches in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `DDR5`, `refresh`, `Same Bank Refresh`, and `REFsb` returned no dedicated case to reuse.

Therefore the bounded retention-specific analysis belongs here. A broader DDR4→DDR5/JEDEC/controller history should still be routed to `computing-archaeology` rather than expanded inside Case 33.

## Cross-case consequence

Before Case 33, the DRAM sequence already supported:

```text
retention deadline
    != row restoration
    != refresh-row enumeration
    != recurring event generation
    != normal/self-refresh authority
    != retention-mode service availability
```

Case 33 adds:

```text
refresh target geometry
    != service-blocking geometry
    != availability of non-target bank resources
```

This is a real addition to the project's retention model because it shows that maintenance and availability need not be globally inverse at the device/rank level: part of a banked dynamic-memory organization can remain callable while another bank-correlated subset is undergoing retention work.

## Residual uncertainties / next work

The case should remain bounded. Future work may separately address:

1. directly inspected final/later `JESD79-5` revision chronology and exact normative `REFsb` semantics;
2. density/product/revision-specific evolution of `tRFCsb`, `tREFSBRD`, FGR, and command legality beyond the bounded 2019 example;
3. LPDDR/per-bank refresh genealogy and terminology;
4. temperature-controlled / temperature-compensated refresh;
5. retention-aware scheduling based on measured cell retention time;
6. named-controller implementation, failure behavior, and empirical compliance;
7. interactions with self refresh and low-power modes in a specific DDR5 product.

None of those gaps invalidates the present finding; they define the point at which this case stops.