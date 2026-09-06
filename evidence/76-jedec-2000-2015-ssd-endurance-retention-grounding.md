# Case 76 Grounding — JESD218 SSD Endurance Rating and Power-Off Retention, 2000–2026

## Purpose

This record grounds Case 76's narrow claim that an SSD endurance rating can be a **workload-qualified host-write boundary whose validity includes a later power-off data-retention requirement**, while keeping that rating distinct from raw NAND P/E wear, powered refresh, current health telemetry, and an instantaneous physical failure threshold.

The source hierarchy is:

1. **JEDEC JESD218 (September 2010)** — normative primary source for the SSD-level rating and test relation;
2. **Intel 2012 retention application note** — manufacturer-primary explanation that separates reference-workload TBW from actual media wear and makes powered refresh versus power-off retention explicit;
3. **Intel DC P3608 product specification (September 2015)** — named commercial enterprise-product witness;
4. **Renesas Technology 2006 reliability handbook** — manufacturer-retrospective standards inventory establishing that JESD22-A117 was already listed as established in 2000;
5. **JEDEC JESD22-A117E (November 2018), Annex A** — later standards-body revision ledger used narrowly to recover A117B's March 2009 date and revision-level terminology changes;
6. **Belgal et al., IEEE IRPS 2002** — period technical evidence for program/erase-cycling-conditioned Flash retention physics.
7. **JEDEC JESD219 (September 2010)** — normative companion-workload primary text, inspected to bound the original enterprise-only workload coverage and the still-developing client workload;
8. **Alvin Cox / JEDEC JC-64.8 presentation (August 2011)** — contemporaneous committee-chair evidence for the evolving JESD218A/JESD219 client-workload state, kept below normative standards text in authority.
9. **JEDEC/Accuris JESD219A + MT/TT catalog records (July 2012)** — publication and supporting-artifact evidence that the client workload had become a standard-plus-trace artifact set; used below the authority of directly inspected normative text.
10. **HPE Solid State Disk Drives QuickSpecs Version 72 + P5430 product page (January 2026)** — manufacturer/OEM primary evidence for a named QLC P5430 SKU, its host-level endurance rating, and HPE's three-month unpowered post-endurance data-retention statement; used as a product witness, not an independent JEDEC compliance audit or raw-cell retention measurement.

No source in this record is used to establish an invention-priority claim. The later A117E ledger is explicitly treated as revision-history evidence rather than proof of first discovery.

---

## Source 1 — JEDEC JESD218, September 2010

**Document:** JEDEC, _Solid-State Drive (SSD) Requirements and Endurance Test Method_, JESD218, September 2010.

**Public inspected copy:** USPTO PTAB Exhibit 1009, 32-page facsimile:
<https://ptacts.uspto.gov/ptacts/public-informations/petitions/1557329/download-documents?artifactId=2_lC_lThPTFMDbmibT3Hg39BJ0KyMU5imHIj-TvKQIl7pYfwt1_SX4I>

### Exact locations inspected

- cover: `JESD218`, September 2010;
- printed p. 1, §1: the standard defines conditions of use and corresponding endurance verification for each SSD class; it is sufficient for the endurance/retention portion of drive qualification, not complete drive qualification;
- printed p. 1, §2: reference list includes `JESD22-A117` and `JESD219`;
- printed p. 2, §§3.3–3.6: separate definitions of `Data Retention`, `Endurance`, and `Endurance Rating (TBW rating)`;
- printed p. 2, §3.6 note: wear leveling, WAF, NAND cycling capability, and workload affect TBW rating;
- printed p. 3, §§3.13–3.19: `Host writes`, NVM, P/E cycle, and `Retention failure` definitions;
- printed p. 5, §§3.24–3.25: workload is the detailed host read/write sequence; WAF is NVM writes divided by host writes and is workload-dependent;
- printed p. 7, §6.2: TBW is the maximum host-written amount under the class workload for which capacity, UBER, FFR, and power-off data-retention requirements must all remain satisfied;
- printed p. 7, §6.3 / Table 1: client and enterprise class workload, active-use, power-off retention, FFR, and UBER conditions;
- printed p. 7 following Table 1: active-use and retention-use are distinct time periods; retention-use is explicitly power-off;
- printed p. 8, §7: endurance verification is followed by retention verification; the direct method writes to TBW, while retention validation may require acceleration/extrapolation because the target retention interval is long.

### What this source directly grounds

**Historical record:**

- `Endurance` and `Data Retention` are distinct standard terms.
- `TBW rating` is not defined as raw NAND cycles; it is host-written TB under a specified class workload.
- The rating composes capacity, UBER, FFR, and later power-off retention requirements.
- WAF explicitly separates host writes from internal NVM writes.
- The two standard 2010 application classes have different active-use and retention-use conditions:
  - Client: 40 °C active, 8 h/day; 30 °C power-off retention for one year; FFR ≤3%; UBER ≤10^-15.
  - Enterprise: 55 °C active, 24 h/day; 40 °C power-off retention for three months; FFR ≤3%; UBER ≤10^-16.
- Qualification can use accelerated/extrapolated retention stress rather than literal wall-clock waiting through the use interval.

### What it does not ground

- a statement that TBW is the exact physical death point of an SSD;
- a physical implementation for wear leveling or WAF;
- a claim that every block has consumed identical P/E cycles at TBW;
- a universal retention time for all SSDs or all wear states;
- a secure-erasure guarantee;
- commercial compliance of any one named product;
- invention priority for endurance/retention testing.

---

## Source 2 — Intel, _Data Retention in Intel Solid-State Drives_, June 2012

**Document:** Intel Application Note 325999-002US, June 2012.

**Inspected copy:** <https://community.solidigm.com/hzhwu46669/attachments/hzhwu46669/Solid_State_Drives/3096/1/App_note_SSD_Data_retention.pdf>

### Exact locations inspected

- p. 4: NAND data are finite-retention state; internal data moves during powered use can refresh data, while such moves are impossible with the drive powered off;
- pp. 5–7: P/E cycling degrades retention, storage/cycling temperature and dwell history matter, and high-temperature retention bake is used for acceleration;
- JESD218A discussion in the qualification section: endurance and retention testing are composed, with class-specific powered-off retention requirements;
- Intel SSD 320 discussion / p. 14 Figure 3: media-wear state changes the modeled retention interval; at the media wearout limit the overall 30 °C retention is about one year in the plotted model, while lower-wear states can retain longer;
- product/endurance discussion: Intel distinguishes the reference-workload TBW rating from its `Media Wearout Indicator` based on actual P/E-cycle consumption and explains that actual workload can make the two limits occur at different times.

### What this source adds

- **manufacturer-primary product interpretation:** `TBW rating ≠ actual media wearout state`;
- **powered/unpowered boundary:** background internal movement can renew data while powered but cannot be assumed during the power-off retention interval;
- **minimum-versus-upper-bound boundary:** product retention can exceed the class minimum substantially at lower wear;
- **workload boundary:** a reference-workload rating does not encode every actual-use write-amplification/wear history.

### Evidence limit

This is Intel's technical explanation of Intel products and JESD218A, not an independent compliance laboratory report. Its NAND physics discussion should not be generalized to every later charge-trap/TLC/QLC implementation without separate evidence.

---

## Source 3 — Intel DC P3608 Product Specification, September 2015

**Document:** Intel, _Intel Solid-State Drive DC P3608 Series Product Specification_, 333055-001US, September 2015.

**Inspected copy:** <https://www.intel.com/content/dam/www/public/us/en/documents/product-specifications/ssd-dc-p3608-spec.pdf>

### Exact locations inspected

- cover / revision record: initial release September 2015;
- front matter: endurance up to 21.9 PBW, 3 drive writes/day, JESD219 workload;
- §2.6 / Table 14, `Reliability Specifications`:
  - Intel states the P3608 series meets or exceeds JESD218 endurance and data-retention requirements;
  - `Data Retention` is described as retention in NAND at maximum rated endurance;
  - value: three months power-off retention once rated write endurance is reached at 40 °C;
  - `Endurance Rating` is drive writes for which JESD218 requirements remain met, with per-capacity PBW ratings.

### What this source adds

A **named commercial enterprise SSD witness** connecting a product PBW rating to post-rating, powered-off retention. It does not disclose the exact hidden mapping, wear-leveling, physical block-age distribution, or test raw data.

---

## Source 4 — Renesas Technology, _Semiconductor Reliability Handbook_, August 31, 2006

**Document:** Renesas Technology, _Semiconductor Reliability Handbook_, REJ27L0001-0100, Rev. 1.00, August 31, 2006.

**Public indexed inspection copy:** <https://studylib.net/doc/28351596/semiconductor-reliability>

### Exact location inspected

- Section 7, JEDEC standards table, handbook pp. 335–336: columns `Number`, `Title`, `Established`; `JESD22-A117` is listed as `ELECTRICALLY ERASBLE PROGRAMMABLE ROM (EEPROM) PROGRAM/ERASE ENDURANCE AND DATA RETENTION TEST`, established `2000`.

### What this source grounds

- By August 2006, a manufacturer reliability handbook treated A117 as a JEDEC endurance-and-retention test standard established in 2000.

### Evidence limit

This is a manufacturer-retrospective standards inventory. It does not replace direct inspection of the original 2000 A117 issue, prove an exact January publication day, or establish invention priority for endurance/retention testing.

---

## Source 5 — JEDEC JESD22-A117E, November 2018, retrospective revision ledger

**Document:** JEDEC, _Electrically Erasable Programmable ROM (EEPROM) Program / Erase Endurance and Data Retention Stress Test_, JESD22-A117E, November 2018.

**Publicly indexed inspection copy:** <https://www.scribd.com/document/837818477/22A117E>

### Exact locations inspected

- Foreword / pp. ii–1: A117E describes the method as testing repeated data changes (`program/erase endurance`) and retention for the expected EEPROM life;
- pp. 2–4: separate definitions of `data retention`, `endurance`, and `uncorrectable bit-error rate (UBER)`;
- Annex A.2 / p. 15: heading identifies **JESD22-A117B (March 2009)** as the predecessor compared with A117C (October 2011);
- Annex A.3 / p. 16: the A117A→A117B ledger records a read-disturb addition under retention, a new UBER definition, bad-block-aware endurance-failure wording, transient-error handling, and UBER calculation.

### What this source grounds

- Revision-level evidence that UBER and read-disturb terminology were already part of A117B before September 2010 JESD218.
- A117's bounded device-level qualification vocabulary is not identical to JESD218's host-TBW SSD contract.

### Evidence limit

A117E is a **2018 standards-body retrospective**. Its Annex is strong evidence for what JEDEC says changed between its own revisions, but it is not a direct facsimile of A117B and does not establish that A117B invented any named mechanism or metric.

---

## Source 6 — Belgal et al., IEEE IRPS 2002

**Document:** Hanmant P. Belgal et al., “A New Reliability Model for Post-Cycling Charge Retention of Flash Memories,” _2002 IEEE International Reliability Physics Symposium_, 7–11 April 2002, DOI 10.1109/RELPHY.2002.996604.

**IEEE record:** <https://doi.org/10.1109/RELPHY.2002.996604>

### Exact evidence inspected

The IEEE abstract states that:

- stress-induced leakage occurs in a small fraction of Flash cells after program/erase cycling;
- the presented statistical model fits data from several technology generations and multi-year bakes;
- the affected fraction scales as a power law in cycle count;
- the mechanism can anneal/recover at moderate temperatures.

### What this source grounds

- cycling-conditioned Flash retention physics was explicitly measured and modeled in period engineering research before JESD218;
- `post-cycling retention` is physically different from treating retention as a history-free shelf-life constant.

### Evidence limit

This paper does not define JESD218's SSD-level service contract and is not used to infer a universal retention law for all NAND/SSD generations.

---

## Source 7 — JEDEC JESD219, September 2010

**Document:** JEDEC, _Solid-State Drive (SSD) Endurance Workloads_, JESD219, September 2010.

**Public text-preserving inspection copy:** <https://studylib.net/doc/18339575/jesd219>

**Contemporaneous publication cross-check:** JEDEC's September 2010 publication announcement was reproduced by period trade press as announcing JESD218 and JESD219 together; the historical direct JEDEC URL was `jedec.org/sites/default/files/docs/JESD219.pdf`.

### Exact locations inspected

- cover: `JESD219`, September 2010;
- printed p. 1, §1 Scope: workloads are for endurance rating/verification and are to be used with JESD218;
- printed p. 1, scope note: client workloads were still under development and were to be added when available;
- printed p. 1 onward, §3: the body supplies an `Enterprise endurance workload` with transfer-size, LBA-distribution, and randomized-data requirements.

### What this source adds

The September 2010 standards pair is historically **asymmetric**:

- JESD218 already defines client and enterprise class endurance/retention requirements;
- the same-month JESD219 supplies the enterprise workload but not yet the client workload it says is still under development.

This grounds `class requirement published ≠ every referenced companion workload simultaneously complete`.

### Evidence limit

The public inspection copy is a text-preserving third-party mirror of the JEDEC document rather than an official-host facsimile currently served by JEDEC. Its cover/scope/body are cross-checked against contemporaneous publication records, but this source is not used for figure-level claims, cryptographic provenance, or invention priority. Direct archival facsimile recovery remains desirable.

---

## Source 8 — Alvin Cox, JEDEC JC-64.8 / Flash Memory Summit, August 10, 2011

**Document:** Alvin Cox, _JEDEC SSD Endurance Workloads_, Flash Memory Summit 2011. Cox is identified on the presentation as Seagate and Chairman, JC-64.8.

**Inspected PDF:** <https://old.flashmemorysummit.com/English/Collaterals/Proceedings/2011/20110810_T1B_Cox.pdf>

### Exact locations inspected

- slide 3: names `JESD218A` and JESD219 as the active JEDEC SSD standards pair;
- slides 4–7: repeats TBW as a user-interface/application-class rating tied to capacity, UBER, FFR, and power-off retention;
- slide 12: describes a client workload based on a real trace, including TRIM commands, and separately describes the enterprise workload;
- slide 13: labels the client workload `JESD219`, describes preconditioning and trace replay, and says testing at 100% full was still under discussion.

### What this source adds

By August 2011 the committee chair was publicly presenting JESD218A and a client-workload design associated with JESD219. This is a useful dated bridge between the September 2010 enterprise-only JESD219 and later revised workload standards.

### Evidence limit

A conference presentation by the standards subcommittee chair is **contemporary committee evidence**, not the normative text of JESD218A or JESD219A. The phrase `still under discussion` is especially important: it blocks silently treating every slide detail as a finalized standard requirement.

---

## Source 9 — JESD219A publication and supporting trace artifacts, July 2012

**Cataloged standard:** JEDEC, _Solid-State Drive (SSD) Endurance Workloads_, JESD219A, publication date 1 July 2012.

**Inspected catalog record:** Accuris / JEDEC:
<https://store.accuristech.com/asa/standards/jedec-jesd219a?product_id=1837609>

**Supporting artifacts:**

- `JESD219A_MT`, _Master Trace for 128 GB SSD_: <https://store.accuristech.com/standards/jedec-jesd219a_mt?product_id=1838012>;
- `JESD219A_TT`, _Test Trace for 64 GB - 128 GB SSD_: <https://store.accuristech.com/standards/jedec-jesd219a_tt?product_id=1837608>.

### Exact metadata inspected

- JESD219A is cataloged as a 26-page JEDEC standard published **07/01/2012**;
- its catalog description says that it defines workloads for SSD endurance rating/verification in conjunction with JESD218 and explicitly names `JESD219A_MT` and `JESD219A_TT` as supporting trace files;
- `JESD219A_MT` is cataloged on the same date as a supporting file for implementation of the endurance-verification **client workload**;
- the Master Trace description says it represents **seven months of actual SSD activity**, is used for client endurance verification under JESD218 for user capacities ≥64 GB, can be used directly for 128–256 GB with its existing LBA range, and can be compressed/expanded for other capacities under a stated maximum-LBA constraint;
- `JESD219A_TT` is cataloged on the same date as a supporting client-workload file for 64–128 GB devices;
- the Test Trace description says it is **derived from the 128 GB Master Trace** using the compression method described in JESD219 and that its characteristics are identical except for a maximum LBA representing 64 GB user capacity;
- Accuris's JEDEC browse page lists the September 2010 `JESD 219` and July 2012 `JESD219A` as distinct catalog entries, providing a publication-level revision cross-check: <https://store.accuristech.com/products?page=23&per_page=10&publisher_id=110&sort_direction=asc&sort_order=doc_no>.

### What this source set directly grounds

**Historical record:**

- by July 2012, JESD219A and separately named MT/TT supporting artifacts were cataloged as the client-workload implementation set;
- the Master Trace was represented as captured real SSD activity over seven months rather than an invented synthetic command list;
- the 64–128 GB Test Trace was derived from the 128 GB Master Trace rather than recorded as an independent source history;
- capacity adaptation was part of the documented workload-artifact relation.

**Engineering reconstruction:**

```text
workload standard
    !=
supporting trace artifact
    !=
source Master Trace history
    !=
derived capacity-adapted Test Trace
    !=
test execution
    !=
qualification result
```

This also creates a retention-specific control-state observation: the trace is a retained **history used to reproduce future stress**, not the user payload whose endurance/retention is being qualified.

### Evidence limit

These are publisher/distributor catalog records carrying JEDEC document metadata and descriptions. They are adequate for publication date, artifact identity, and the quoted high-level artifact relation, but they are **not a directly inspected full normative JESD219A facsimile**. They therefore do not close clause-level preconditioning, trace-transformation, or later revision archaeology. Nor do they establish invention priority for trace-based SSD workload qualification.


---

## Source 10 — HPE QLC/TLC commercial-product pair, QuickSpecs Version 72, January 2026

**Documents:**

- Hewlett Packard Enterprise, _HPE Solid State Disk Drives_, QuickSpecs **Version 72**, dated **5 January 2026**: <https://www.hpe.com/psnow/downloadDoc/HPE%20Solid%20State%20Disk%20Drives%20QuickSpecs-a00001288enw.pdf?contentDisposition=attachment&deepLink=&form=false&hf=regular&id=a00001288enw.pdf&isFutureVersion=true&isLinearized=false&originalObjectName=&prelaunchSection=&preview=false&print=&r=&section=&softrollSection=&ver=72>;
- HPE product page for **P63934-B21**, _HPE 7.68TB NVMe Gen4 Mainstream Performance Very Read Optimized E3S EC1 EDSFF P5430 SSD_: <https://buy.hpe.com/us/en/options/drives-storage/server-solid-state-drives/hpe-7-68tb-nvme-gen4-mainstream-performance-very-read-optimized-e3s-ec1-edsff-p5430-ssd/p/p63934-b21>.

### Exact locations inspected

QuickSpecs Version 72:

- `Summary of Changes`: Version 72 is dated **05-Jan-2026**;
- `Standard Features` → `Data Retention`: HPE defines data retention as retaining NAND data once the maximum rated endurance level has occurred and states that the listed SSDs are rated for **3 months if no power is applied once maximum rated write endurance is reached**;
- `PCIe/NVMe EDSFF E3.S – SKUs`: `P63934-B21` is the HPE 7.68 TB Gen4 Mainstream Performance Very-read-optimized P5430 SSD and its `Flash Type` is **QLC**;
- corresponding `Speeds and Feeds` table: `P63934-B21` is listed at **8,040 TB Lifetime Writes** and **0.57 Endurance DWPD**.
- the same E3.S capacity/workload table lists **`P61183-B21`**, a **7.68 TB** Gen5 High Performance Read Intensive CM7 SSD, with `Flash Type` **TLC**;
- its corresponding `Speeds and Feeds` row gives **14,016 TB Lifetime Writes** and **1 Endurance DWPD**.

HPE product page:

- exact SKU `P63934-B21` and 7.68 TB P5430 identity;
- HPE describes the P5430 family as offering **Next Gen QLC 3D NAND**.

The retention clause was also checked on the rendered QuickSpecs page rather than inferred solely from search snippets; the SKU/table relation was checked against the text-preserving PDF extraction.

### What this source set directly grounds

**Historical/product record:**

- by 5 January 2026 HPE's current QuickSpecs included a named P5430 QLC SSD family and exact `P63934-B21` 7.68 TB SKU;
- the same QuickSpecs family documented an 8,040 TB / 0.57 DWPD host-level endurance rating for that SKU;
- HPE stated a three-month no-power data-retention interval after maximum rated write endurance for the SSDs covered by the QuickSpecs;
- HPE independently described the P5430 product family as QLC 3D NAND.
- within the same Version 72 document, HPE also documented the equal-capacity `P61183-B21` CM7 as TLC/RI with a 14,016 TB / 1 DWPD product endurance rating;
- the document-level `Data Retention` clause therefore supplies one common post-endurance retention statement above two differently labeled/rated products.

**Engineering reconstruction:**

```text
QLC flash-type label
    !=
very-read-optimized workload label
    !=
lifetime-write / DWPD rating
    !=
maximum-rated-endurance state
    !=
three-month unpowered product retention requirement
    !=
raw NAND-cell retention law
```

The source set is especially useful because the media-density label and the SSD-level service envelope coexist in one manufacturer product family without becoming the same variable.

The TLC/QLC pair adds a second bounded relation:

```text
P61183-B21: 7.68 TB / RI / TLC / 14,016 TB / 1 DWPD
    !=
P63934-B21: 7.68 TB / VRO / QLC / 8,040 TB / 0.57 DWPD

while both remain under the same QuickSpecs family-level
three-month post-maximum-endurance no-power retention statement.
```

This is **product-contract comparison**, not a controlled experiment. Equal user capacity does not hold workload class, interface/product generation, controller design, ECC margin, over-provisioning, NAND process, firmware, or qualification method constant.


### Evidence limit

The HPE documents are **manufacturer/OEM product documentation**, not an independent qualification laboratory report. The P5430 table rows do not expose raw-cell threshold-voltage distributions, controller ECC margin, over-provisioning, wear-leveling distribution, refresh/rewrite policy, or retention-test raw data. The cited P5430 row also does not explicitly state `JESD218`, so this record does **not** infer a particular JEDEC revision, temperature profile, or compliance path merely because HPE's three-month interval resembles the 2010 enterprise-class figure.

This source now closes only a **bounded named HPE TLC/QLC commercial-product cross-check** above the already-grounded QLC witness. It does not establish that all TLC or QLC SSDs have three-month retention, that either cell type intrinsically retains for three months, that the higher rated writes of the cited TLC CM7 are caused by TLC rather than the many other differing product variables, or that TLC/QLC density alone determines an SSD's endurance/retention contract.

---

## Qualification-semantics deepening from the original JESD218 facsimile

Additional directly inspected locations in the September 2010 JESD218 facsimile sharpen the existing case:

- printed p. 7, §6.3: Table 1 temperatures are use-period case temperatures for endurance/retention estimation, not absolute datasheet max/min values;
- printed p. 8, §7: direct and extrapolation methods both perform endurance verification followed by retention verification;
- printed p. 8, §7.1.1: the qualification sample is sized to establish FFR and UBER requirements at **60% confidence**;
- printed p. 24, Annex C: the same qualified SSD can have a different expected retention duration under different active-use/power-off temperatures; the client example gives 52 weeks at 40 °C active / 30 °C off and at least 105 weeks at 40 °C active / 25 °C off under the stated model;
- printed p. 25, Annex D: retention-time/p-e-cycle RBER extrapolation must remain below the SSD controller's ECC capability; the standard warns that random-error assumptions are imperfect and requires margin for device/location variation.

These passages support the bounded reconstruction:

```text
raw NVM error population
    !=
controller-correctable population
    !=
host-visible data error
    !=
class-level UBER/FFR qualification result
```

They also make the test epistemology explicit: **qualification evidence is sampled, statistical, controller-inclusive, and conditioned on a declared use/model envelope**. None of those adjectives means the standard is weak; they specify what kind of claim it actually establishes.

---

## Prior art boundary

The 2010 JESD218 standard itself references **JESD22-A117, _Electrically Erasable Programmable ROM (EEPROM) Program/Erase Endurance and Data Retention Stress Test_**. The deeper evidence now shows more than citation precedence:

- a 2006 Renesas standards inventory lists A117 as established in **2000**;
- the later JEDEC A117E revision ledger records **A117B (March 2009)** as already adding read-disturb wording and UBER definition/calculation to the device-level test family;
- Belgal et al. 2002 independently establish a period engineering literature on P/E-cycling-conditioned Flash retention.

This blocks false statements that JESD218 invented cycling-plus-retention qualification, cycling-conditioned retention physics, UBER in JEDEC NVM qualification, or read-disturb terminology. The historically supportable contribution used in Case 76 is narrower:

> JESD218 makes an SSD-level, host-interface endurance rating depend on application-class workload and on meeting a later power-off retention requirement along with capacity, FFR, and UBER conditions, above an already-existing device-level endurance/retention qualification tradition.

A pre-2000 qualification genealogy and direct original A117/A117B facsimile archaeology remain open. The September-2010 JESD218/JESD219 coverage mismatch and an August-2011 committee bridge are now grounded here, while direct normative facsimiles of JESD218A/JESD219A, later JESD218 B/C revision history, and the full workload-standard genealogy remain future standards-history work best coordinated with `computing-archaeology`.

---

## Claim ledger

| Claim | Type | Evidence | Strength / limit |
| --- | --- | --- | --- |
| JESD218 is dated September 2010 and defines SSD endurance/retention requirements | H/P | JEDEC cover, scope | direct |
| `Data Retention` and `Endurance` are separate defined terms | H/P | JESD218 §§3.3–3.4 | direct |
| TBW is host-written terabytes while requirements remain satisfied | H/P | JESD218 §3.6, §6.2 | direct |
| WAF separates internal NVM writes from host writes and is workload dependent | H/P | JESD218 §3.25 | direct |
| TBW depends on workload, WAF, wear leveling, and NAND cycling capability | H/P | JESD218 §3.6 note | direct |
| Standard class use includes active endurance stressing followed by power-off retention | H/P | JESD218 §6.3 | direct |
| Client and enterprise have different retention-use time/temperature conditions | H/P | JESD218 Table 1 | direct for 2010 revision |
| Retention validation can use acceleration/extrapolation | H/P | JESD218 §7 | direct |
| TBW rating can diverge from actual media-wearout progress | H/P/E | Intel 2012 application note | direct manufacturer explanation; implementation-specific |
| Powered internal data movement can refresh Intel SSD data, unlike power-off interval | H/P | Intel 2012 p. 4 | direct for bounded Intel products |
| Intel DC P3608 specifies 3-month power-off retention at rated write endurance/40 °C | H/P | Intel 2015 §2.6 Table 14 | direct named-product witness |
| TBW rating is not an instant physical failure threshold | E | JEDEC definition + Intel TBW/media-wear distinction | strong reconstruction; no source says post-TBW life is guaranteed |
| Power-fail durability ≠ long power-off retention | E/A | Cases 15/20 + JESD218 two-phase model | controlled cross-case comparison |
| Powered refresh ≠ power-off retention qualification | E/A | Intel 2012 + JESD218 | controlled cross-case comparison |
| Client/enterprise retention numbers are class contracts, not substrate ranking | E | JESD218 Table 1 + class-purpose text | strong reconstruction |
| JESD218 did not invent endurance/retention testing in general | X/H | JESD218 references JESD22-A117 | blocks priority claim; full genealogy not done |
| A117 device-level endurance/retention qualification predates JESD218 | H/S | Renesas 2006 standards table lists A117 established 2000 | strong retrospective manufacturer inventory; original 2000 facsimile not directly inspected |
| A117B predates JESD218 and added UBER/read-disturb terminology inside A117 | H/P | JEDEC A117E Annex A.2–A.3 | standards-body retrospective revision ledger; not invention-priority proof |
| Post-P/E-cycle retention degradation was a period Flash reliability problem by 2002 | H/P | Belgal et al. IEEE IRPS 2002 | direct peer-reviewed engineering evidence; technology-bounded |
| A117 device/cell qualification ≠ JESD218 SSD host-TBW qualification | E | A117E scope/definitions + JESD218 §§3.6/6.2 | strong interface-level reconstruction |
| September 2010 JESD218 defines both client and enterprise classes while same-month JESD219 supplies only the enterprise workload | H/P | JESD218 §6.3 Table 1 + JESD219 §1/§3 | direct release-bounded standards comparison; JESD219 inspection copy is a public mirror |
| Client workload was explicitly still under development in the September 2010 JESD219 | H/P | JESD219 §1 note | direct document statement; does not erase JESD218's already-published client retention requirement |
| By August 2011 JC-64.8 chair Cox publicly presents JESD218A and a JESD219 client-workload design | H/P | Cox FMS 2011 slides 3, 12–13 | contemporary committee evidence; not normative facsimile |
| JESD218 qualification is sample/confidence based rather than a deterministic per-drive countdown | H/P/E | JESD218 §7.1.1 | direct 60% confidence requirement + bounded reconstruction |
| Retention qualification can allow raw bit errors that remain inside guarded controller-ECC capability | H/P/E | JESD218 Annex D | direct standard mechanism; does not imply unlimited retention |
| Table 1 retention duration is condition-specific rather than a universal shelf-life constant | H/P/E | JESD218 §6.3 + Annex C | direct standard/example + bounded interpretation |

| HPE QuickSpecs Version 72 lists exact P5430 `P63934-B21` as QLC | H/P | HPE 2026 E3.S SKU table + product page | direct named-product/OEM witness |
| HPE documents 8,040 TB lifetime writes / 0.57 DWPD for P63934-B21 | H/P | HPE 2026 speeds/endurance table | direct product rating; host-level metric, not raw P/E count |
| HPE states three months unpowered after maximum rated write endurance for covered SSDs | H/P | HPE 2026 `Data Retention` clause | direct manufacturer/OEM product-family statement; not independent lab certification |
| QLC label ≠ SSD-level retention contract or raw-cell retention constant | E | HPE media-type + endurance + retention fields | strong bounded reconstruction; controller/media internals remain undisclosed |
| same three-month interval ≠ proof of identical JESD218 qualification path | E/X | HPE 2026 + JESD218 2010 | explicit anti-overreach boundary; HPE P5430 row does not name JESD218 |


| HPE QuickSpecs Version 72 lists exact CM7 `P61183-B21` as 7.68 TB RI/TLC | H/P | HPE 2026 E3.S capacity/workload table | direct named-product/OEM witness |
| HPE documents 14,016 TB lifetime writes / 1 DWPD for P61183-B21 | H/P | HPE 2026 speeds/endurance table | direct product rating; host-level metric, not raw P/E count |
| Equal 7.68 TB capacity ≠ controlled TLC/QLC media experiment | E/X | HPE P61183 + P63934 rows | strong anti-overreach boundary: workload class, generation, controller/media internals are not controlled |
| Same family-level three-month retention clause ≠ same prior endurance history | E | HPE retention clause + product endurance rows | bounded product-contract reconstruction; each rating defines a different maximum-rated-endurance precondition |
| Higher TLC product TBW in this pair ≠ proof that TLC intrinsically causes higher endurance | E/X | HPE product rows only | causal mechanism not identified by the source |
| Same post-endurance interval across the pair ≠ same raw-cell retention law | E/X | HPE family clause + TLC/QLC labels | controller/media qualification remains undisclosed |
---

## Rejected shortcuts

Do **not** write:

- `A consumer SSD always stores data for exactly one year.`
- `An enterprise SSD intrinsically has worse retention than a client SSD.`
- `TBW is the physical NAND death point.`
- `TBW reached means data is immediately lost.`
- `SMART Percentage Used / Media Wearout Indicator is the same thing as the JESD218 rating.`
- `A successful Flush or power-loss-protection path proves months of power-off retention.`
- `Powered background refresh can operate during the JESD218 power-off retention interval.`
- `JESD218 invented endurance and data-retention testing.`
- `JESD218 introduced UBER or read-disturb terminology into JEDEC NVM qualification.`
- `A117 device-level cycling/retention qualification is the same contract as JESD218 SSD TBW.`
- `The September 2010 JESD219 already contained a finalized client workload merely because JESD218 Table 1 referenced a client workload.`
- `A JEDEC client one-year retention requirement means every individual client SSD has a deterministic one-year physical countdown.`
- `Passing JESD218 retention requires zero raw NAND bit errors.`
- `The later A117E revision ledger proves who first invented read disturb, UBER, or endurance qualification.`
- `A QLC label by itself implies a universal three-month raw-cell retention constant.`
- `HPE's P5430 row proves an independently audited JESD218 qualification or the exact JESD218 revision/test path.`
- `HPE's VRO workload label is interchangeable with JEDEC's Client or Enterprise application class.`
- `The same three-month number in HPE and JESD218 proves identical controller margin, temperature conditions, or qualification chronology.`
- `Matching 7.68 TB capacity makes P61183-B21 and P63934-B21 a controlled TLC-versus-QLC media experiment.`
- `Because the cited TLC CM7 has a higher HPE lifetime-write rating, TLC intrinsically has higher endurance by that ratio.`
- `Because both products sit under the same three-month HPE retention clause, TLC and QLC raw cells have the same retention law.`
- `Endurance exhaustion is sanitization.`

---

## Related-repository check

Before this deepening, searches in `tmzncty/computing-archaeology` for `JESD218`, `JESD22-A117`, `P5430`, `CM7`, and `TLC QLC SSD retention` did not find a dedicated case. The full JEDEC/NAND-generation qualification genealogy therefore was **not** recreated here. If a standards-history or QLC-controller slice is later built there, Case 76 should link to it and keep only this retention-specific decomposition between lower-level media type, host-rated endurance, and the SSD-level post-endurance service contract.
