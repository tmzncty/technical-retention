from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CASE_PATH = ROOT / "cases/76-jedec-ssd-endurance-retention-qualification.md"
EVIDENCE_PATH = ROOT / "evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md"
README = ROOT / "README.md"
ROADMAP = ROOT / "ROADMAP.md"
INDEX = ROOT / "CASE_INDEX.md"

case_text = r'''# JEDEC JESD218 SSD Endurance Qualification: Workload-Qualified TBW and Power-Off Retention

## Status

**`grounded`** — bounded to the September 2010 JESD218 SSD-level endurance/retention qualification relation, with Intel's June 2012 retention application note used to expose the difference between standardized TBW and actual media wear, and Intel's September 2015 DC P3608 specification used as a named commercial product witness.

Grounding record: [`../evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md`](../evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md).

## Scope

This case asks a narrow question left open by Cases 36, 37, and 55:

> When an SSD is given an endurance rating in host-written terabytes, what exactly is being promised about retention at that rating, and how is that promise related to workload, internal media wear, power state, and later read correctness?

The bounded object is **JESD218's SSD-level qualification relation**. It is not:

- a NAND cell-physics history;
- an assertion that TBW is the instant at which an SSD physically fails;
- a claim that all SSDs have one universal shelf life;
- a claim that client SSDs inherently retain data longer than enterprise SSDs under all conditions;
- a replacement for JESD219 workload history;
- a named-controller wear-leveling implementation study;
- a claim about secure erasure or forensic disappearance;
- an invention-priority claim for endurance or data-retention testing.

The central historical source is JEDEC **JESD218, _Solid-State Drive (SSD) Requirements and Endurance Test Method_, September 2010**.[^jesd218]

---

## Historical vocabulary

JESD218 itself defines or uses:

- `Data Retention`;
- `Endurance`;
- `Endurance Rating (TBW rating)`;
- `Host writes`;
- `Program/erase cycle (p/e cycle)`;
- `Workload`;
- `Write amplification factor (WAF)`;
- `Wear leveling`;
- `Retention failure`;
- `Functional Failure Requirement (FFR)`;
- `Uncorrectable Bit Error Rate (UBER)`;
- `Client` and `Enterprise` application classes;
- `Active Use (power on)` and `Retention Use (power off)`.

The phrases **qualification relation**, **wear-conditioned retention**, **rating boundary**, and **power-off retention contract** below are project engineering reconstructions. They are not substituted for the standard's vocabulary.

Intel's 2012 application note additionally uses `Media Wearout Indicator` when explaining its own SSD products.[^intel-ret]

---

## Historical record

### JESD218 makes endurance and retention separate concepts, then composes them

JESD218 defines `Data Retention` as the SSD's ability to retain data over time and `Endurance` as the ability to withstand multiple rewrites. Its `Endurance Rating (TBW rating)` is then the number of host-written terabytes for which the drive must still satisfy the requirements of section 6.2.[^jesd218]

Section 6.2 makes that rating a bundle rather than a single-media-wear number. At the stated TBW, under the workload associated with the application class, the drive must still:

- maintain advertised user capacity;
- meet the class UBER requirement;
- meet the class FFR requirement; and
- retain data with power off for the class-required time.[^jesd218]

Thus the standard itself blocks the shortcut:

> **endurance ≠ data retention**.

The rating deliberately composes both.

### The rating is expressed at the host interface, not as a raw NAND cycle count

JESD218 defines `Host writes` as data transmitted through the primary SSD interface for writing. It separately defines WAF as data written to NVM divided by data written by the host, and notes that WAF depends on workload and may vary over device life. Its TBW note also names wear-leveling quality, WAF, NAND cycling capability, and workload as factors affecting the rating.[^jesd218]

Therefore the period standard already distinguishes:

```text
host-written TB
        !=
internal NVM writes / P-E cycling
```

A TBW value is deliberately user-visible, but it is mediated by controller and workload behavior below that interface.

### JESD218 uses a two-phase life model

Section 6.3 states a use scenario in which SSDs are actively used and written to their endurance ratings, **followed by a power-down period in which data must be retained**.[^jesd218]

Its 2010 Table 1 defines two standard classes:

| Application class | Workload | Active use | Retention use, power off | FFR | UBER |
| --- | --- | --- | --- | --- | --- |
| Client | Client / JESD219 | 40 °C, 8 h/day | 30 °C, 1 year | ≤3% | ≤10^-15 |
| Enterprise | Enterprise / JESD219 | 55 °C, 24 h/day | 40 °C, 3 months | ≤3% | ≤10^-16 |

The table values are **class qualification conditions**, not universal physical constants. JESD218 explicitly says the active-use and retention-use columns refer to different periods and that retention-use time is the period over which data must remain with power off.[^jesd218]

### Verification may be accelerated without changing the target use condition

Clause 7 says endurance verification is followed by retention verification. In the direct method drives are stressed to stated TBW using specified workloads and then retention-tested; because the use-time retention requirements are long, extrapolation or acceleration is used to validate the requirement.[^jesd218]

Hence:

> **accelerated qualification chronology ≠ ordinary user chronology**.

A high-temperature bake or extrapolation is evidence about an intended use-condition relation under the specified model; it is not a statement that the drive literally spent the same wall-clock time in ordinary use.

---

## Named manufacturer witnesses

### Intel 2012: TBW and media wear can diverge

Intel's June 2012 application note explains JESD218A through its own NAND/SSD retention model. It says powered-on internal data movement can refresh data, while such moves are impossible during a powered-off retention interval.[^intel-ret]

More importantly for the qualification boundary, Intel separates:

- a **TBW rating**, based on a reference workload; from
- its **Media Wearout Indicator**, based on actual NAND P/E-cycle consumption.

Intel warns that actual workload can cause one limit to be reached before the other. For the Intel SSD 320, its own plotted model also shows retention changing strongly with accumulated media wear and says the overall 30 °C retention at the media-wearout limit is about one year, while less-worn states can retain substantially longer.[^intel-ret]

Therefore:

> **TBW rating ≠ physical-media wearout state**.

And:

> **qualification minimum ≠ product-specific upper bound**.

### Intel 2015 P3608: a named enterprise product contract

Intel's September 2015 DC P3608 product specification states that the series meets or exceeds JESD218 endurance and retention requirements. Its reliability table defines data retention as retention in NAND at maximum rated endurance and specifies **three months of power-off retention once rated write endurance is reached at 40 °C**. The same table gives PBW endurance ratings and links endurance verification to JESD218.[^p3608]

This is a named commercial witness for the enterprise-class relation. It is not evidence that every SSD implements the same hidden wear-management mechanism.

---

## Engineering reconstruction

### Rated endurance is a qualification boundary, not an instant physical death line

The standard says the drive must meet a set of requirements **through the stated rating**. It does not say the first write beyond TBW instantaneously destroys the payload, nor does it define TBW as the physical P/E limit of every NAND block.

Therefore:

> **SSD endurance rating ≠ instant failure threshold**.

This distinction is reinforced by Intel's separation of reference-workload TBW from actual media P/E wear.

### Power-loss durability is not the same problem as power-off retention duration

Cases 15 and 20 ask whether an acknowledged/flush-qualified write reaches a recoverable nonvolatile state across an interruption. JESD218 asks a later question: after the endurance phase and power-down, can the already-written data still be read correctly after a specified **unpowered interval**?

So:

> **power-fail durability handoff ≠ power-off retention interval**.

A drive may correctly flush data to nonvolatile media and still face finite long-term retention after sufficient wear. Conversely, a long-retention medium does not prove that an acknowledged write had crossed the required persistence boundary before sudden power loss.

### Powered refresh opportunity is excluded by the qualification interval itself

Intel notes that internal data movement while powered can refresh data and that such movement is impossible while the drive is powered off.[^intel-ret]

That makes JESD218's retention-use phase especially useful beside Cases 36 and 37:

> **powered maintenance opportunity ≠ power-off retention qualification**.

The standard's retention requirement cannot silently assume background controller rewriting during the specified off interval.

### Application class is part of the rating relation

The client and enterprise rows differ in workload, active-use temperature/duty, retention-use temperature/time, and UBER target. It is therefore invalid to interpret the one-year versus three-month values as a substrate-only ranking.

> **client 1 year at 30 °C ≠ enterprise 3 months at 40 °C as an inherent-media ordering**.

They are different qualified service models.

### Retention duration is conditional on prior history

In this case `retention time` cannot be treated as one timeless material constant. The qualification relation includes prior endurance stressing, workload, temperature, and a declared rating. Intel's product analysis further shows the same drive family can have different expected retention at different wear states.[^intel-ret]

Project reconstruction:

```text
retention claim
    = relation among
      current payload recoverability
      + prior write/wear history
      + workload/controller amplification
      + temperature history
      + powered/unpowered phase
      + required error/failure criteria
```

This is an analytical decomposition, not JEDEC's philosophical vocabulary.

---

## Failure and forgetting boundaries

Several different failures must remain separate:

- exceeding a host TBW rating;
- reaching a media wearout estimate;
- exhausting ECC/error margin during a later read;
- failing the UBER or FFR qualification criterion;
- losing data during the powered-off retention interval;
- losing an acknowledged write before it ever reached the intended persistence boundary;
- logical deallocation or sanitization;
- controller telemetry reporting a high wear estimate.

In particular:

> **rated endurance ≠ secure erase / forgetting**.

TBW provides no claim that data is erased when the rating is reached or exceeded.

---

## Prior art and anti-anachronism

JESD218 itself cites **JESD22-A117, _Electrically Erasable Programmable ROM (EEPROM) Program/Erase Endurance and Data Retention Stress Test_** as a reference document.[^jesd218]

Therefore this repository does **not** claim that JESD218 invented the practice of cycling nonvolatile memory and then testing retention. The bounded historical contribution used here is more specific:

> by September 2010, JESD218 standardized an **SSD-level**, application-class-specific endurance rating expressed as host TBW and tied it to workload, capacity, UBER/FFR, and a subsequent power-off retention requirement.

A full history of JESD22-A117, JESD219, NAND qualification, or the later A/B revisions of JESD218 remains separate work.

---

## Functional analogies and philosophical limit

A useful functional analogy is to a **qualified service envelope** rather than to a countdown timer: the TBW number names a boundary inside which a bundle of conditions is still required to hold under a reference use model.

The analogy stops there. TBW is not a universal biological `lifespan`, and this repository does not convert JEDEC qualification language into a philosophical claim about finitude.

The narrow philosophical pressure is only this:

> A technical statement that something is `retained for one year` may describe not a timeless property of a substrate, but a relation conditioned by what happened to that substrate before the clock began.

That sentence is a project interpretation, not an attributed JEDEC intention.

---

## Cross-case result

Case 76 adds the following controlled comparison:

```text
host write acknowledged / flushed
    !=
write counted toward TBW
    !=
internal NAND write / P-E wear
    !=
current health / wear telemetry
    !=
rated-endurance qualification boundary
    !=
power-off retention interval after that boundary
    !=
actual instant of future unreadability
```

It complements:

- **Case 15 / Case 20** — immediate power-loss durability and interface persistence;
- **Case 36** — powered ECC-bounded Flash correct-and-refresh maintenance;
- **Case 37** — commercial old-data read-performance restoration/refresh;
- **Case 55** — current/lifetime endurance telemetry and model-derived health state;
- **Cases 44 / 47** — logical/sanitization/forensic forgetting rather than wear qualification.

The mechanisms should not be collapsed simply because all of them can be described as SSD `reliability`.

## Sources

[^jesd218]: JEDEC, **JESD218, _Solid-State Drive (SSD) Requirements and Endurance Test Method_**, September 2010. Public copy preserved as USPTO PTAB Exhibit 1009: <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1557329/download-documents?artifactId=2_lC_lThPTFMDbmibT3Hg39BJ0KyMU5imHIj-TvKQIl7pYfwt1_SX4I>. Key locations: pp. 1–5 definitions and references; p. 7 §§6.2–6.3 / Table 1; p. 8 §7.
[^intel-ret]: Intel, **_Data Retention in Intel Solid-State Drives_**, Application Note 325999-002US, June 2012. Preserved by Solidigm: <https://community.solidigm.com/hzhwu46669/attachments/hzhwu46669/Solid_State_Drives/3096/1/App_note_SSD_Data_retention.pdf>. Key locations: pp. 4–7 for powered refresh and wear/temperature mechanisms; pp. 12–18 for JESD218A qualification and Intel SSD wear/retention examples.
[^p3608]: Intel, **_Intel Solid-State Drive DC P3608 Series Product Specification_**, 333055-001US, September 2015, especially §2.6 / Table 14: <https://www.intel.com/content/dam/www/public/us/en/documents/product-specifications/ssd-dc-p3608-spec.pdf>.
'''

evidence_text = r'''# Case 76 Grounding — JESD218 SSD Endurance Rating and Power-Off Retention, 2010–2015

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
'''

if CASE_PATH.exists() or EVIDENCE_PATH.exists():
    raise SystemExit("Case 76 or evidence already exists; refusing duplicate integration")
CASE_PATH.write_text(case_text, encoding="utf-8")
EVIDENCE_PATH.write_text(evidence_text, encoding="utf-8")

# README: append the new case immediately after Case 75, before the evidence list.
readme = README.read_text(encoding="utf-8")
case75_line = "- [`Case 75 — NVM Express 1.3d Reservations: Retained Access Authority, PTPL, and Preemption`](cases/75-nvme13-reservation-persistence-ptpl.md) — `grounded`; registration/reservation state survives ordinary controller/subsystem reset, while namespace PTPL separately decides whether that access-authority relation crosses power loss. Preemption changes authority without relocating payload, and Reservation Report `GEN` is bounded change evidence rather than a complete history. Grounding: [`evidence/75-nvme-2001-2019-reservation-persistence-grounding.md`](evidence/75-nvme-2001-2019-reservation-persistence-grounding.md)."
case76_line = "- [`Case 76 — JEDEC JESD218 SSD Endurance Qualification: Workload-Qualified TBW and Power-Off Retention`](cases/76-jedec-ssd-endurance-retention-qualification.md) — `grounded`; the 2010 standard makes host-interface TBW a workload-qualified boundary that still requires capacity, UBER/FFR, and class-specific post-endurance power-off retention. Intel 2012 separates reference-workload TBW from actual media wear, and Intel's 2015 DC P3608 supplies a named enterprise product witness. Grounding: [`evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md`](evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md)."
assert case75_line in readme, "README Case 75 anchor not found"
assert "cases/76-jedec-ssd-endurance-retention-qualification.md" not in readme
readme = readme.replace(case75_line, case75_line + "\n" + case76_line, 1)
README.write_text(readme, encoding="utf-8")

# ROADMAP: extend SSD/controller line, add Case 76 bounded-question closure, and record qualification maintenance work.
roadmap = ROADMAP.read_text(encoding="utf-8")
old_count = "partially advanced by grounded Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, 47, 52, 55, 59, 65, 66, and 67"
new_count = "partially advanced by grounded Cases 15, 20, 30, 31, 32, 36, 37, 38, 39, 44, 47, 52, 55, 59, 65, 66, 67, and 76"
assert old_count in roadmap, "ROADMAP SSD case-list anchor not found"
roadmap = roadmap.replace(old_count, new_count, 1)

ssd_start = roadmap.index("- [ ] SSD FTL/controller-mediated persistence beyond the bounded Ban/1990s case")
ssd_end = roadmap.index("\n- [ ] RAID / scrubbing / rebuild", ssd_start)
ssd_block = roadmap[ssd_start:ssd_end]
needle = "The broad item stays unchecked because independent named-product PLP fault compliance"
assert needle in ssd_block, "ROADMAP SSD open-gap sentence not found"
case76_clause = "[`cases/76-jedec-ssd-endurance-retention-qualification.md`](cases/76-jedec-ssd-endurance-retention-qualification.md), grounded by [`evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md`](evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md), adds an SSD-level qualification boundary above device physics: JESD218 ties host-write TBW under an application workload to capacity, UBER/FFR, and a class-specific post-endurance power-off retention interval. Intel's 2012 retention note separates reference-workload TBW from actual media wear, and its 2015 DC P3608 specification supplies a named enterprise witness for three-month power-off retention at rated endurance. This keeps standardized endurance rating, physical P/E wear, powered refresh, health telemetry, and actual post-rating data survival distinct. "
ssd_block = ssd_block.replace(needle, case76_clause + needle, 1)
roadmap = roadmap[:ssd_start] + ssd_block + roadmap[ssd_end:]

phase3_anchor = "- [ ] How should `command completion`, `volatile-cache residence`, `nonvolatile-media commitment`, `cross-command ordering`, and `power-fail atomicity` be separated at storage interfaces?"
phase3_case76 = "- [x] In SSD endurance qualification, separate `host-write TBW rating`, reference workload, internal NVM writes/WAF and media wear, active-use endurance stress, subsequent power-off retention, and current health telemetry — grounded in [`cases/76-jedec-ssd-endurance-retention-qualification.md`](cases/76-jedec-ssd-endurance-retention-qualification.md), with [`evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md`](evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md); full JESD218/JESD219 revision chronology and later TLC/QLC named-product validation remain separate work."
assert phase3_anchor in roadmap, "ROADMAP Phase-3 anchor not found"
assert phase3_case76 not in roadmap
roadmap = roadmap.replace(phase3_anchor, phase3_anchor + "\n" + phase3_case76, 1)

phase5_anchor = "- SSD firmware, reclamation, wear management, bad-block replacement;"
phase5_add = "- SSD endurance/retention qualification, reference workloads, accelerated stress, and power-off verification;"
assert phase5_anchor in roadmap, "ROADMAP Phase-5 anchor not found"
roadmap = roadmap.replace(phase5_anchor, phase5_anchor + "\n" + phase5_add, 1)
ROADMAP.write_text(roadmap, encoding="utf-8")

# CASE_INDEX: main ledger row.
index = INDEX.read_text(encoding="utf-8")
case75_prefix = "| [NVM Express 1.3d Reservations: Retained Access Authority, PTPL, and Preemption](cases/75-nvme13-reservation-persistence-ptpl.md) |"
lines = index.splitlines()
positions = [i for i, line in enumerate(lines) if line.startswith(case75_prefix)]
assert len(positions) == 1, f"Expected one Case 75 ledger row, found {len(positions)}"
ledger76 = "| [JEDEC JESD218 SSD Endurance Qualification: Workload-Qualified TBW and Power-Off Retention](cases/76-jedec-ssd-endurance-retention-qualification.md) | **grounded** | host-write TBW rating + class/reference workload + WAF/media-wear relation + active-use endurance stress + class-specific post-endurance power-off retention + UBER/FFR/capacity requirements | separate rated endurance from physical wearout or instant failure; standardized power-off retention from shelf-life folklore; host writes from NVM writes; and qualification target from current telemetry, powered refresh, or sanitization | [2000–2015 JEDEC/Intel endurance-retention grounding](evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md); exact JESD218/JESD219 revision history, post-rating fault testing, TLC/QLC named-product validation, and physical retention models remain separate work |"
assert not any("cases/76-jedec-ssd-endurance-retention-qualification.md" in line for line in lines)
lines.insert(positions[0] + 1, ledger76)
index = "\n".join(lines) + ("\n" if index.endswith("\n") else "")

# Repair an existing comparison-matrix drift: rows stopped at Case 68 even though Cases 69–75 were grounded.
lines = index.splitlines()
dynamo_positions = [i for i, line in enumerate(lines) if line.startswith("| Amazon Dynamo membership / failure boundary, 2007 |")]
assert len(dynamo_positions) == 1, f"Expected one Dynamo comparison row, found {len(dynamo_positions)}"
matrix_rows = [
"| JEDEC DDR4 refresh scheduling / 2012 bounded regime | DRAM array + controller refresh-accounting relation + FGR mode | externally issued REF with bounded postpone/pull-in; catch-up across rate/Self Refresh transitions | ordinary reads/writes are timing-qualified around REF; maintenance is not payload access | bank/row refresh schedule + recent command-group position | same physical cells; maintenance timing moves rather than payload location | no payload history; only bounded recent scheduling/accounting relation |",
"| Magnetic-core half-select / 1951–1959 bounded regime | remanent ferrite + coordinate excitation + shared sense path + inhibit relation | repeated nonselecting pulses must stay within state/sense margins; selected restore remains separate | target and half-selected cores can contribute to shared sense output | coincident X/Y selection plus inhibit/bit qualification | fixed cores in the bounded arrays | no access history by default; current remanent state and operational margins only |",
"| ZooKeeper fuzzy snapshot / 2006–2019 bounded regime | in-memory tree + transaction log + fuzzy snapshots + zxid/replay boundary | durable logging, nonlocking snapshotting, ordered idempotent replay, purge of older recovery sets | service from in-memory state; restart materializes snapshot plus logs | zxid + snapshot-start/recovery-set relation | snapshot/log files can be replaced or retired after a newer recovery closure | bounded redo history until safe retirement; complete history not required |",
"| IBM store-in cache / 1971–1982 bounded regime | cache-local payload + modified/store bits + shared/central backing copy + directory authority | writeback/castout preserves newer cache value before replacement or conflicting access | cache/central reads are qualified by currentness and ownership state | architectural address + directory/store/RO-EX relation | current embodiment can reside in cache and later return to central storage | no full store history; modified/currentness relation only |",
"| Google File System lazy GC / 2003 | namespace log + hidden-name deleted file + file→chunk references + chunk replicas/version state | grace-period retention, namespace/chunk scans, HeartBeat cleanup | hidden deleted file can remain specially readable; stale replicas can be excluded before deletion | namespace name + chunk handle/version | replicas may survive after namespace/currentness retirement | bounded delete/grace evidence rather than complete deletion history |",
"| Linux JBD revoke / 1998–2005 bounded regime | redo journal images + revoke records + transaction sequence + home blocks | commit positive redo; record negative revoke before reuse; reconstruct transient revoke table at recovery | replay only journal images not disqualified by a later revoke | block number + transaction sequence + allocation/reuse generation | old journal bytes may persist after losing replay authority | bounded negative recovery evidence, not full block history |",
"| NVMe 1.3d reservations / 2019 | namespace registrant/key/holder/type state + PTPL policy + GEN/current report | register/acquire/release/preempt; optional power-loss persistence of authority | namespace I/O is qualified by reservation-conflict rules | namespace + Host Identifier/key/holder relation | payload location can remain unchanged while authority changes | current authority + wrapping GEN evidence, not complete transition history |",
"| JESD218 SSD endurance qualification / 2010–2015 bounded regime | SSD NVM + controller-mediated host/media write relation + qualified payload + class/workload/test metadata | endurance stress under reference workload followed by power-off retention verification/acceleration | post-stress reads verify retained correctness/UBER; ordinary read-path implementation is unspecified | host LBA + application class; TBW counts host writes while WAF links to NVM writes | physical embodiment/FTL is unspecified; logical service may persist across internal relocation | no operational history required by the standard; qualification evidence/rating summarize a bounded service relation |",
]
for row in matrix_rows:
    assert row not in lines
insert_at = dynamo_positions[0] + 1
lines[insert_at:insert_at] = matrix_rows
index = "\n".join(lines) + ("\n" if index.endswith("\n") else "")

old_aggregate = "After seventy-six bounded cases, **all seventy-six cases are now `grounded`.**"
new_aggregate = "After seventy-seven bounded cases, **all seventy-seven cases are now `grounded`.**"
assert old_aggregate in index, "CASE_INDEX aggregate anchor not found"
index = index.replace(old_aggregate, new_aggregate, 1)

assert "## Case 76 — JESD218 endurance/retention qualification findings" not in index
findings = r'''

## Case 76 — JESD218 endurance/retention qualification findings

893. **SSD endurance rating ≠ instant failure threshold** — JESD218 defines TBW as the host-written amount for which a bundle of requirements must still be met, not as a claim that the next write instantaneously destroys the drive or payload;
894. **TBW rating ≠ raw NAND P/E-cycle limit** — wear leveling, WAF, NAND cycling capability, and workload mediate the relation between host-written terabytes and internal media wear;
895. **host bytes written ≠ bytes written to NVM** — JESD218 defines WAF precisely to separate the two, and notes that the relation is workload dependent;
896. **endurance ≠ data retention** — the standard defines them separately and then requires retention to remain satisfied at the endurance-rating boundary;
897. **power-fail durability ≠ power-off retention interval** — reaching nonvolatile state across an interruption and remaining readable after months/year without power are different qualification questions;
898. **powered refresh opportunity ≠ power-off retention qualification** — Intel describes internal powered data movement as a refresh path while the JESD218 retention-use interval is explicitly power-off;
899. **retention requirement ≠ generic SSD shelf life** — the specified interval is conditioned on application class, workload/endurance history, temperature, and qualification criteria;
900. **client one-year / 30 °C ≠ enterprise three-month / 40 °C as an inherent-media ranking** — the rows are different service/test classes with different active-use, retention-use, workload, and UBER conditions;
901. **retention at rated endurance ≠ retention at low wear** — Intel's product analysis shows lower-wear NAND can retain substantially longer than the end-of-rated-life requirement;
902. **standard qualification minimum ≠ product-specific upper bound** — a product can exceed the class retention requirement without changing what JESD218 requires at the stated rating;
903. **reference-workload TBW ≠ actual-use wear history** — Intel's TBW/Media-Wearout distinction shows actual workload can consume physical P/E budget differently from the rating workload;
904. **accelerated qualification chronology ≠ ordinary user chronology** — JESD218 permits retention acceleration/extrapolation after endurance stress because the use-time retention interval is long;
905. **active-use temperature ≠ retention-use temperature** — the standard deliberately assigns separate temperature/time conditions to powered endurance stressing and the later unpowered retention phase;
906. **rated endurance ≠ secure erase / forgetting** — reaching or exceeding TBW carries no implication of sanitization, immediate logical deletion, or forensic absence;
907. **current health telemetry ≠ standardized endurance-rating contract** — Case 55's counters/model-derived health state estimate what has happened to one device, while JESD218 defines the conditions under which a product rating is qualified;
908. **JESD218 SSD-level composition ≠ invention of endurance/retention testing** — the 2010 standard itself cites the earlier JESD22-A117 component-level program/erase endurance and data-retention stress procedure; the bounded claim is the SSD-level application-class/TBW/retention composition.
'''
index = index.rstrip() + findings + "\n"
INDEX.write_text(index, encoding="utf-8")

# Remove the temporary integration machinery from the final tree.
workflow = ROOT / ".github/workflows/case76-integrate.yml"
script = Path(__file__)
if workflow.exists():
    workflow.unlink()
if script.exists():
    script.unlink()
