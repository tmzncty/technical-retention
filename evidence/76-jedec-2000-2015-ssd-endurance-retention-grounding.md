# Case 76 Grounding — JESD218 SSD Endurance Rating and Power-Off Retention, 2000–2015

## Purpose

This record grounds Case 76's narrow claim that an SSD endurance rating can be a **workload-qualified host-write boundary whose validity includes a later power-off data-retention requirement**, while keeping that rating distinct from raw NAND P/E wear, powered refresh, current health telemetry, and an instantaneous physical failure threshold.

The source hierarchy is:

1. **JEDEC JESD218 (September 2010)** — normative primary source for the SSD-level rating and test relation;
2. **Intel 2012 retention application note** — manufacturer-primary explanation that separates reference-workload TBW from actual media wear and makes powered refresh versus power-off retention explicit;
3. **Intel DC P3608 product specification (September 2015)** — named commercial enterprise-product witness;
4. **Renesas Technology 2006 reliability handbook** — manufacturer-retrospective standards inventory establishing that JESD22-A117 was already listed as established in 2000;
5. **JEDEC JESD22-A117E (November 2018), Annex A** — later standards-body revision ledger used narrowly to recover A117B's March 2009 date and revision-level terminology changes;
6. **Belgal et al., IEEE IRPS 2002** — period technical evidence for program/erase-cycling-conditioned Flash retention physics.

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

## Prior art boundary

The 2010 JESD218 standard itself references **JESD22-A117, _Electrically Erasable Programmable ROM (EEPROM) Program/Erase Endurance and Data Retention Stress Test_**. The deeper evidence now shows more than citation precedence:

- a 2006 Renesas standards inventory lists A117 as established in **2000**;
- the later JEDEC A117E revision ledger records **A117B (March 2009)** as already adding read-disturb wording and UBER definition/calculation to the device-level test family;
- Belgal et al. 2002 independently establish a period engineering literature on P/E-cycling-conditioned Flash retention.

This blocks false statements that JESD218 invented cycling-plus-retention qualification, cycling-conditioned retention physics, UBER in JEDEC NVM qualification, or read-disturb terminology. The historically supportable contribution used in Case 76 is narrower:

> JESD218 makes an SSD-level, host-interface endurance rating depend on application-class workload and on meeting a later power-off retention requirement along with capacity, FFR, and UBER conditions, above an already-existing device-level endurance/retention qualification tradition.

A pre-2000 qualification genealogy, direct original A117/A117B facsimile archaeology, JESD219 history, and revision-by-revision JESD218A/B history belong in future standards-history work or `computing-archaeology`, not in this bounded case.

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
- `The later A117E revision ledger proves who first invented read disturb, UBER, or endurance qualification.`
- `Endurance exhaustion is sanitization.`

---

## Related-repository check

Before this deepening, searches in `tmzncty/computing-archaeology` for `JESD218` and `JESD22-A117` did not find a dedicated case. The full JEDEC/NAND qualification genealogy therefore was **not** recreated here. If a standards-history slice is later built there, Case 76 should link to it and keep only this retention-specific decomposition between lower-level device qualification and the SSD-level service contract.