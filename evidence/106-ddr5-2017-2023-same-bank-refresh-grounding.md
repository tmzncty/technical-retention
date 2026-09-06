# DDR5 2017–2023 Same Bank Refresh grounding record

This record grounds [`../cases/106-ddr5-same-bank-refresh-parallel-target-set.md`](../cases/106-ddr5-same-bank-refresh-parallel-target-set.md).

The bounded question is whether DDR5 Same Bank Refresh can localize one maintenance transaction to corresponding bank positions across multiple bank groups while retaining a broader coverage obligation, and how that differs from the one-bank LPDDR2 REFpb regime in Case 105.

## Source A — proposed DDR5 Full Spec Rev0.1, 5 December 2017

Publicly mirrored PDF:
<https://www.pedestrian.com.cn/_downloads/4928176668e6494cc99abfb887fdf326/DDR5_JESD79-5.pdf>

The PDF text was inspected directly. The page image for printed p. 176 / PDF page 184 containing §4.10.3 was also visually inspected. The remote screenshot cache did not return the revision-history page image during this run, so the 12/5/17 revision line is grounded in direct PDF text extraction rather than a claimed visual facsimile check.

### A1. Document status and date boundary

The front matter labels the file `DDR5 Full Spec Draft Rev0.1`, identifies committee JC42.3, and marks it as committee letter-ballot/proposed material. The revision history gives:

- `Rev0.1`;
- author `C.Cox`;
- date `12/5/17`;
- description `Initial Format Rev0.1 - Includes all ballots through Q3'17`.

This means the repository can establish a **December 2017 proposed-draft floor**. It must not describe this public mirror as the final published JESD79-5 standard.

### A2. REFsb target geometry — printed p. 176, §4.10.3

The section says Same Bank Refresh (`REFsb`) applies refresh to a specific bank **in each bank group**, in contrast to All Bank Refresh (`REFab`) over all banks in every bank group. In this draft REFsb is valid only in FGR mode.

The visual page inspection confirms the same wording and the section title `4.10.3 Same Bank Refresh`.

This grounds:

- `same bank` ≠ one unique physical bank in the whole device;
- one REFsb target set = corresponding target bank in multiple bank groups;
- REFsb ≠ REFab.

### A3. Synchronization / coverage accounting — printed p. 176

The draft says each REFsb increments an internal bank counter. A REFsb can be issued in any bank order, but every bank must receive one before the same bank can receive a subsequent REFsb; repeating early is illegal.

The first command is described as the `Synchronization` REFsb. The internal count resets after every bank has received one REFsb, RESET, entering/exiting self refresh, or REFab. The global refresh counter increments on REFab or after all banks have received one REFsb and the synchronization count resets. A REFab in the middle of a same-bank sequence does not increment the global counter for that incomplete sequence.

The exact implementation of these counters is not exposed. The primary evidence establishes interface/accounting semantics, not a transistor-level controller design.

### A4. Target-bank unavailability and non-target service — printed p. 176

The draft explicitly says the target banks — `one in each Bank Group` — are inaccessible during `tRFCsb`, while other banks in each bank group are accessible/addressable. On completion, the refreshed banks are idle.

This directly supports:

- target-set maintenance ≠ whole-device blackout;
- non-target availability ≠ target-bank availability;
- command completion for one target set ≠ coverage completion across all bank indices.

### A5. Scheduling flexibility is bounded

The same section allows bank indices in any order but forbids early repetition, and states that a single REFab can be replaced by 2 or 4 REFsb commands **for scheduling in terms of postponing and pulling in refresh commands**.

That wording is kept narrow. It is not rewritten here as a claim that 2/4 REFsb are universally semantically identical to one REFab for every retention, accounting, timing, or service property.

## Source B — Micron DDR5 ecosystem page, final-standard/product-era continuity

Micron manufacturer page:
<https://www.micron.com/about/blog/memory/dram/microns-ddr5-technology-enablement-program-empowers-ecosystem>

The page states that JEDEC announced the DDR5 standard in **July 2020** and lists Same Bank Refresh among DDR5 improvements, describing it as targeting one bank per bank group.

Use here: later manufacturer continuity and a publication-era anchor.

Do not use it for: invention priority, exact final normative wording, or proof that every DDR5 part exposes identical optional behavior.

## Source C — Micron 2023 platform-era explanation

Micron manufacturer page:
<https://www.micron.com/about/blog/company/partners/redefining-performance-with-ddr5-and-4th-gen-intel-xeon-scalable>

The article is situated around Intel's 10 January 2023 launch of 4th Gen Xeon Scalable systems. It lists Same Bank Refresh among DDR5 RAS/availability features and explains its practical purpose as granular refresh that keeps non-target banks available for access.

This source is useful as a product/platform-era service interpretation. It is not stronger than Source A for exact 2017 command/accounting semantics.

## Cross-case evidence boundary

### Case 105 — LPDDR2 REFpb

Case 105's Micron LPDDR2 documents ground a one-bank REFpb target, a fixed round-robin sequence, non-target-bank service, and full-cycle rolling refresh accounting.

### Case 106 — proposed DDR5 REFsb

Source A instead grounds a parallel target set: one corresponding bank in each bank group, with coverage/synchronization across all bank indices.

Therefore the defensible comparison is:

> both localize recurring refresh work relative to whole-device maintenance, but their transaction target geometry and accounting semantics are not command-identical.

Nothing in the present source set proves a direct LPDDR2 REFpb → DDR5 REFsb implementation genealogy.

## Evidence ledger

| Claim | Label | Location | Strength |
| --- | --- | --- | --- |
| Rev0.1 dated 12/5/17 includes ballots through Q3'17 | H/P | Source A revision history | strong proposed-standards primary text |
| REFsb targets one specific bank in each bank group | H/P | Source A §4.10.3, printed p. 176 | strong proposed-standards primary text + page-image inspection |
| REFsb is restricted to FGR mode in this draft | H/P | Source A §4.10.3, printed p. 176 | strong proposed-standards primary text |
| target banks are unavailable during `tRFCsb`; others remain accessible | H/P | Source A §4.10.3, printed p. 176 | strong proposed-standards primary text + page-image inspection |
| every bank index must be serviced before one repeats | H/P | Source A §4.10.3, printed p. 176 | strong proposed-standards primary text |
| synchronization/global counter state records maintenance coverage rather than payload | E | reconstruction from Source A | strong mechanism inference |
| DDR5 final-standard era includes Same Bank Refresh | H/P | Source B; Source C continuity | manufacturer-primary continuity |
| December 2017 draft = final JESD79-5 wording | X | not established | rejected |
| 2017 or 2020 = invention priority | X | not established | rejected |
| LPDDR2 REFpb and DDR5 REFsb share a proven direct genealogy | X | not established | rejected |

## Historical cautions

- Source A is a publicly mirrored **proposed** DDR5 committee draft, not an official-hosted final standard copy.
- The 2017 date establishes a floor for this compiled proposal text, not the first conception or implementation of Same Bank Refresh.
- The July 2020 announcement establishes a publication/adoption node, not an invention date.
- Micron's later summaries are manufacturer explanations, not independent verification of the complete standards history.
- `same bank` must be interpreted with the bank-group geometry; collapsing it to one physical bank creates a technical error.
- Refresh-accounting progress is not a semantic application-data integrity certificate.
- Service concurrency does not imply that the target set is simultaneously available.

## Related-repository check

A current GitHub search of `tmzncty/computing-archaeology` for `DDR5 same-bank refresh`, `REFsb`, and the adjacent terminology did not expose a dedicated case. Full standards genealogy, underlying ballots/proposals, controller scheduling implementation, performance/energy modeling, and cross-vendor comparison belong there if developed comprehensively.
