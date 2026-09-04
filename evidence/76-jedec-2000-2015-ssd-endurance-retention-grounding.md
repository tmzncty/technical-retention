# Case 76 Grounding — JESD218 SSD Endurance Rating and Power-Off Retention, 2010–2015

## Purpose

This record grounds Case 76's narrow claim that an SSD endurance rating can be a **workload-qualified host-write boundary whose validity includes a later power-off data-retention requirement**, while keeping that rating distinct from raw NAND P/E wear, powered refresh, current health telemetry, and an instantaneous physical failure threshold.

The source hierarchy is:

1. **JEDEC JESD218 (September 2010)** — normative primary source for the SSD-level rating and test relation;
2. **Intel 2012 retention application note** — manufacturer-primary explanation that separates reference-workload TBW from actual media wear and makes powered refresh versus power-off retention explicit;
3. **Intel DC P3608 product specification (September 2015)** — named commercial enterprise-product witness.

No source in this record is used to establish an invention-priority claim.

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

## Prior art boundary

The 2010 JESD218 standard itself references **JESD22-A117, _Electrically Erasable Programmable ROM (EEPROM) Program/Erase Endurance and Data Retention Stress Test_**.

That is enough to block a false statement that JESD218 invented cycling-plus-retention qualification as such. The historically supportable contribution used in Case 76 is narrower:

> JESD218 makes an SSD-level, host-interface endurance rating depend on application-class workload and on meeting a later power-off retention requirement along with capacity, FFR, and UBER conditions.

A revision-by-revision genealogy of JESD22-A117, JESD218A/B, and JESD219 belongs in a future standards-history slice or `computing-archaeology`, not in this bounded case.

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
- `Endurance exhaustion is sanitization.`

---

## Related-repository check

Before this slice, searches in `tmzncty/computing-archaeology` for `JESD218` and SSD endurance/data-retention/TBW did not find a dedicated case. The full standards genealogy therefore was **not** recreated here. If a JEDEC/NAND qualification history is later built there, Case 76 should link to it and keep only this retention-specific decomposition.
