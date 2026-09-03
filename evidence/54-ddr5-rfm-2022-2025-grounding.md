# Case 54 Grounding Record — DDR5 RFM, 2022–2025

## Purpose

This record grounds [`../cases/54-ddr5-rfm-split-maintenance-authority.md`](../cases/54-ddr5-rfm-split-maintenance-authority.md).

The bounded question is not whether DDR5 is generally reliable or whether RFM defeats every RowHammer attack. It is:

> What public evidence establishes the DDR5-era responsibility split among a device-advertised RFM requirement, controller-side activity accounting / command scheduling, internal DRAM management time, platform enablement, and observed command behavior?

The case is intentionally later than Case 53. Case 53 already grounds RowHammer disturbance and targeted-refresh prior art through 2020; this record must not rewrite RFM as the origin of RowHammer-aware maintenance.

## Evidence classes

- **H/P** — historical record from manufacturer/platform primary technical documentation.
- **H/S** — independent scholarly observation of implemented platform behavior.
- **E** — engineering reconstruction from the documented interface composition.
- **X** — claim explicitly rejected by the bounded evidence.

## Source 1 — Micron DDR5 SDRAM Product Core Data Sheet

**Source type:** manufacturer-authored technical datasheet, accessed through a distributor mirror.

**Title:** `DDR5 SDRAM Product Core Data Sheet` / Micron DDR5 SDRAM core documentation.

**Public mirror used:**
<https://www.avnet.com/wcm/connect/dacdfea7-999f-4ee0-b514-6f9e0bf68c6d/ddr5-sdram-core.pdf?MOD=AJPERES>

### Relevant indexed text

The public indexed copy contains a section titled `Refresh Management` that states, in substance:

- periods of high device activity may require additional refresh commands to protect data integrity;
- the device determines whether additional RFM support is required and reports the requirement through read-only `MR58:OP[0]`;
- `0` means RFM is not required beyond the ordinary refresh requirement;
- `1` means RFM is required;
- a suggested controller implementation monitors `ACT` commands per bank using a `Rolling Accumulated ACT (RAA)` count;
- each ACT increments the individual bank's RAA count;
- the DRAM vendor supplies an `RAA Initial Management Threshold (RAAIMT)` in read-only MR58 fields;
- when RAA reaches that threshold, additional refresh management is needed;
- executing `RFM` provides additional time for the device to manage refresh internally;
- the bounded document distinguishes all-bank (`RFMab`) from same-bank-address (`RFMsb`) forms;
- a device that does not require RFM treats the RFM command as a REF command.

### Claims grounded

**H/P:** a DDR5 device can advertise `RFM required` / `RFM not required` through a read-only interface field.

**H/P:** the public Micron interface supplies vendor threshold information for controller refresh-management accounting.

**H/P:** per-bank RAA is described as a suggested controller-side implementation.

**H/P:** RFM gives the device additional time to manage refresh internally.

**E:** ordinary periodic refresh and RFM are distinct maintenance obligations: the source explicitly defines the no-RFM case as requiring no additional refresh beyond ordinary REFRESH operation.

**E:** the end-to-end retention mechanism is split across layers: device requirement/threshold → controller pressure accounting / command scheduling → internal DRAM management.

### Provenance limitation

The document is Micron-authored, but the accessible public copy used in this run is hosted by Avnet rather than Micron. Search indexing exposed the relevant text; the large PDF could not be fetched through the research renderer in this run. Therefore:

- treat the technical text as **manufacturer-authored primary evidence with distributor-mirror provenance**;
- do not claim that this run directly inspected an official JEDEC PDF or a current Micron-hosted copy;
- do not infer revision-by-revision JEDEC chronology from this single product core document.

**Evidence strength:** strong for the bounded Micron interface description; insufficient for full normative-standard history.

## Source 2 — Micron 16Gb DDR5 SDRAM Die Rev A addendum

**Source type:** manufacturer-authored die-revision addendum, publicly mirrored.

**Title / revision:** `16Gb DDR5 SDRAM Die Rev A`, Rev. D, February 2023.

**Document identifier visible in the indexed copy:** `CCM005-0005-1684161373-30`.

**Public mirror used:**
<https://device.report/m/e4760da10ba9aca558ff5b3b6cd76607ea2c4dcd4ebcfe964553bb4d1c5aa6ac>

### Relevant function-matrix notes

The indexed manufacturer text includes:

- `RFM not required`;
- a note that `RAAMMT`, `RAAIMT`, and RAA-counter decrement are applicable only when the RFM requirement bit is `1` (`MR58:OP[0]=1`).

### Claims grounded

**H/P:** at least one documented Micron 16Gb DDR5 die revision explicitly says RFM is not required.

**X:** `all DDR5 devices require RFM` is unsupported and directly contradicted by this bounded manufacturer record.

**E:** the DDR generation / interface family does not by itself determine the exact disturbance-maintenance obligation of every physical device; the advertised requirement bit matters.

### Limitation

This is one die revision, not a statement about all Micron DDR5 and not a general historical claim about all 16Gb parts.

**Evidence strength:** strong counterexample to universal requirement; narrow product scope.

## Source 3 — Intel processor datasheet 743844 Rev. 015

**Source type:** first-party platform datasheet.

**Title:** `13th Generation Intel Core, Intel Core 14th Generation, Intel Core Processor (Series 1) and (Series 2), Intel Xeon E 2400 Processor and Intel Xeon 6300 Processor — Datasheet, Volume 1 of 2`.

**Document:** 743844, Rev. 015, May 2025.

**Official Intel PDF:**
<https://cdrdv2-public.intel.com/743844/743844-015.pdf>

### Exact location

- table of contents places `5.1.20 Refresh Management (RFM)` on printed page 129;
- extracted PDF page index 128 / printed page 129 contains the section;
- the same PDF revision identifies itself as Rev. 015, May 2025.

### Relevant text

Section 5.1.20 states:

- `RFM is supported according to JEDEC spec.`
- `LPDDR5/x: RFM feature is enabled.`
- `DDR5: RFM feature is not yet enabled.`

### Claims grounded

**H/P:** the bounded Intel processor/platform family documents RFM support while separately saying DDR5 RFM is not yet enabled.

**E:** standardized/interface support does not imply feature enablement in the platform's DDR5 controller path.

**X:** `Intel documentation saying RFM is supported according to JEDEC proves DDR5 RFM is enabled` is contradicted by the immediately following product statement.

### Limitation

This is a platform-family and revision-specific statement. It must not be projected onto all Intel DDR5 controllers, later products, firmware, or future revisions.

**Evidence strength:** very strong first-party evidence for the support/enablement distinction.

## Source 4 — McSee, USENIX Security 2025

**Source type:** peer-reviewed independent measurement / reverse engineering.

Patrick Jattke, Michele Marazzi, Flavien Solt, Max Wipfli, Stefan Gloor, Kaveh Razavi, **“McSee: Evaluating Advanced Rowhammer Attacks and Defenses via Automated DRAM Traffic Analysis,”** 34th USENIX Security Symposium, August 2025, pp. 5621–5640.

**USENIX record:**
<https://www.usenix.org/conference/usenixsecurity25/presentation/jattke>

**Paper:**
<https://www.usenix.org/system/files/usenixsecurity25-jattke.pdf>

### Method relevant to this case

McSee uses high-frequency oscilloscope capture plus automated DDR4/DDR5 command decoding to observe actual DRAM-bus traffic. The paper therefore provides implementation evidence below a marketing/feature list: whether RFM commands are actually transmitted on tested systems.

### Main bounded results

The authors report that:

- neither the tested Intel nor AMD CPUs sent RFM commands;
- about one third of the DDR5 devices in their test pool required RFM for proper RowHammer mitigation;
- tested Intel systems instead emitted additional mitigative activations, which the authors characterized;
- the artifact appendix identifies concrete DDR5 systems including Alder Lake i7-12700K, Raptor Lake i7-13700K, and AMD Zen 4 Ryzen 7 7700X, together with RFM-capable/required UDIMM test requirements.

### Claims grounded

**H/S:** in the tested platforms, absence of RFM command traffic was empirically observed rather than inferred from documentation alone.

**H/S:** some devices in the test pool advertised a requirement for RFM while the tested controller path did not issue RFM.

**H/S:** tested Intel platforms performed other mitigative activations, so no-RFM cannot be equated with no mitigation at all.

**E:** device-advertised requirement, controller implementation, actual command execution, and empirical mitigation behavior are distinct evidence layers.

**X:** the study does not prove that every Intel or AMD DDR5 platform universally lacks RFM command issuance.

### Evidence strength

Strong independent implementation evidence for the tested systems and module pool; intentionally not universalized beyond the sample.

## Standards chronology boundary

The original DDR5 standard, JESD79-5, was publicly announced in July 2020. Public manufacturer and platform documents examined here use RFM terminology and Intel explicitly describes its implementation relative to the JEDEC specification.

However, **this grounding pass did not directly inspect the official full JESD79-5 revision series**. JEDEC's specific standard pages were not directly accessible through the research path used in this run, and nonofficial copies discovered on the web are not promoted to authoritative normative evidence.

Therefore this case does **not** claim:

- the exact first ballot/revision that introduced every RFM field;
- revision-by-revision changes to RAA, ARFM, DRFM, PRAC, timings, or command semantics;
- that the Micron product datasheet is a substitute for the normative JEDEC specification.

Future direct standard inspection should become a separate bounded chronology/semantics slice.

## Prior-art boundary

Case 53 already grounds an Intel targeted-refresh architecture with 2012 priority and Kim et al. 2014's RowHammer characterization/PARA work. Thus the following claim is rejected:

**X:** `DDR5 RFM invented RowHammer-aware targeted refresh`.

The historical contribution investigated here is later and narrower: public DDR5-era interface and platform evidence makes a controller/device **responsibility split** visible and testable.

## Cross-case deductions supported by this record

The source set supports the following engineering distinctions without attributing project vocabulary to historical actors:

1. **ordinary periodic REF ≠ RFM maintenance opportunity**;
2. **device-advertised mitigation requirement ≠ controller-side maintenance execution**;
3. **per-bank activation-pressure state ≠ payload state**;
4. **activity accounting ≠ complete access history**;
5. **controller command issuance ≠ in-DRAM mitigation algorithm**;
6. **host-visible bank accounting ≠ physical victim-row knowledge**;
7. **standard/interface support ≠ feature enablement**;
8. **DDR5 support for RFM ≠ RFM requirement for every device**;
9. **absence of RFM command ≠ absence of all RowHammer mitigation**;
10. **documented capability ≠ observed execution**;
11. **independent observation in a test pool ≠ universal vendor guarantee**;
12. **DDR5 RFM evolution ≠ origin of RowHammer-aware targeted refresh**.

## Why `grounded`

The case is promoted directly to `grounded` because its bounded argument does not depend on a single source class:

- Micron manufacturer documentation grounds the device/controller RFM contract and supplies a product-specific `RFM not required` counterexample;
- Intel first-party May 2025 platform documentation independently grounds the difference between RFM support and DDR5 enablement;
- McSee 2025 provides peer-reviewed independent observation of actual bus command behavior and a counterexample to equating no-RFM with no mitigation;
- Case 53 already supplies the earlier targeted-refresh / RowHammer prior-art boundary, preventing a false DDR5-origin narrative.

The remaining gaps are **different research questions**, not hidden blockers for this bounded case.

## Open follow-up slices

- direct official JESD79-5/5A/5B/5C/later revision archaeology for exact RFM chronology and normative wording;
- ARFM / DRFM / PRAC evolution as separate maintenance-policy/interface regimes;
- named-DIMM/device fault injection where the device advertises RFM required and the controller claims a corresponding guarantee;
- later Intel/AMD platform behavior after the bounded May/August 2025 evidence;
- controller-reset / sleep / power-state semantics for RAA-like accounting if normative evidence establishes retained/reset state boundaries;
- whether alternative controller-side mitigations satisfy the same device-specific fault model as RFM-required operation.