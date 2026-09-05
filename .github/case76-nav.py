from pathlib import Path


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    Path(path).write_text(text, encoding="utf-8")


def replace_once(path, old, new):
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one anchor, found {count}")
    write(path, text.replace(old, new, 1))


readme_old = "- [`Case 76 — JEDEC JESD218 SSD Endurance Qualification: Workload-Qualified TBW and Power-Off Retention`](cases/76-jedec-ssd-endurance-retention-qualification.md) — `grounded`; the 2010 standard makes host-interface TBW a workload-qualified boundary that still requires capacity, UBER/FFR, and class-specific post-endurance power-off retention. Intel 2012 separates reference-workload TBW from actual media wear, and Intel's 2015 DC P3608 supplies a named enterprise product witness. Grounding: [`evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md`](evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md)."
readme_new = "- [`Case 76 — JEDEC JESD218 SSD Endurance Qualification: Workload-Qualified TBW and Power-Off Retention`](cases/76-jedec-ssd-endurance-retention-qualification.md) — `grounded`; the 2010 standard makes host-interface TBW a workload-qualified boundary that still requires capacity, UBER/FFR, and class-specific post-endurance power-off retention. Intel 2012 separates reference-workload TBW from actual media wear, and Intel's 2015 DC P3608 supplies a named enterprise product witness. Prior-art deepening now separates this SSD-level contract from the earlier JESD22-A117 device-level endurance/retention tradition: a 2006 Renesas inventory lists A117 as established in 2000, JEDEC's later revision ledger places A117B in March 2009 with UBER/read-disturb additions, and Belgal et al. 2002 supply a period post-cycling-retention physics witness. Grounding: [`evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md`](evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md)."
replace_once("README.md", readme_old, readme_new)

roadmap_anchor = "\nCoordinate with `computing-archaeology` rather than duplicating it.\n"
roadmap_new = """
- [x] JESD22-A117 → JESD218 qualification-layer prior-art deepening — canonical [`cases/76-jedec-ssd-endurance-retention-qualification.md`](cases/76-jedec-ssd-endurance-retention-qualification.md), with [`evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md`](evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md), now separates the earlier device-level P/E-endurance-and-retention test tradition from JESD218's SSD-level host-TBW service envelope. A 2006 Renesas standards inventory lists A117 as established in 2000; JEDEC's later A117E revision ledger identifies A117B as March 2009 and records UBER/read-disturb additions; Belgal et al. 2002 independently ground cycling-conditioned Flash-retention physics. This blocks a JESD218-origin myth without treating standards revision history as invention history. Direct original A117/A117B facsimile archaeology, pre-2000 EEPROM qualification genealogy, complete JESD219 history, and later JESD218 revision history remain open and should be coordinated with `computing-archaeology`.

Coordinate with `computing-archaeology` rather than duplicating it.
"""
replace_once("ROADMAP.md", roadmap_anchor, roadmap_new)

idx_old = "| [JEDEC JESD218 SSD Endurance Qualification: Workload-Qualified TBW and Power-Off Retention](cases/76-jedec-ssd-endurance-retention-qualification.md) | **grounded** | host-write TBW rating + class/reference workload + WAF/media-wear relation + active-use endurance stress + class-specific post-endurance power-off retention + UBER/FFR/capacity requirements | separate rated endurance from physical wearout or instant failure; standardized power-off retention from shelf-life folklore; host writes from NVM writes; and qualification target from current telemetry, powered refresh, or sanitization | [2000–2015 JEDEC/Intel endurance-retention grounding](evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md); exact JESD218/JESD219 revision history, post-rating fault testing, TLC/QLC named-product validation, and physical retention models remain separate work |"
idx_new = "| [JEDEC JESD218 SSD Endurance Qualification: Workload-Qualified TBW and Power-Off Retention](cases/76-jedec-ssd-endurance-retention-qualification.md) | **grounded** | host-write TBW rating + class/reference workload + WAF/media-wear relation + active-use endurance stress + class-specific post-endurance power-off retention + UBER/FFR/capacity requirements | separate rated endurance from physical wearout or instant failure; standardized power-off retention from shelf-life folklore; host writes from NVM writes; device-level A117 qualification from SSD-level JESD218 service contract; and qualification target from current telemetry, powered refresh, or sanitization | [2000–2015 JEDEC/Intel endurance-retention grounding](evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md), now deepened with A117/2002 physics prior art; direct original A117/A117B facsimiles, exact JESD218/JESD219 revision history, post-rating fault testing, TLC/QLC named-product validation, and physical retention models remain separate work |"
replace_once("CASE_INDEX.md", idx_old, idx_new)

idx = read("CASE_INDEX.md")
marker = "### Case 76 deepening — JESD22-A117 device qualification vs JESD218 SSD qualification"
if marker in idx:
    raise SystemExit("Case 76 deepening findings already present")
findings = """

### Case 76 deepening — JESD22-A117 device qualification vs JESD218 SSD qualification

1247. **device-level P/E endurance qualification ≠ SSD-level host-TBW qualification** — A117 qualifies reprogrammable nonvolatile-memory endurance/retention at the device/cell/module test layer, while JESD218 expresses a whole-drive endurance boundary in host-written terabytes and adds workload, capacity, FFR/UBER, and a later power-off service phase.

1248. **post-cycling data retention ≠ uncycled shelf retention** — Belgal et al. 2002 show that P/E cycling can create stress-induced leakage whose affected fraction depends on cycle count, so prior use history can alter the later retention problem before any SSD-level rating is considered.

1249. **host TBW ≠ cell P/E cycle count** — the earlier device-level test history sharpens JESD218's own WAF distinction: one host-visible write amount is mediated by controller placement/amplification and cannot be read as a direct count for every physical cell.

1250. **A117B UBER terminology ≠ JESD218 invention of UBER** — JEDEC's later revision ledger places A117B in March 2009 and records a new UBER definition/calculation there, before September 2010 JESD218; this is terminology prior art, not proof that thresholds or implementations are identical.

1251. **read-disturb vocabulary inside the A117 family ≠ identity of read disturb and ordinary time-aged retention** — the A117A→A117B ledger records read-disturb wording under retention, but Case 52's access-induced mechanism remains distinct from elapsed-time charge loss and from Case 76's SSD-level power-off qualification.

1252. **cycling-conditioned retention physics ≠ standards-only artifact** — the 2002 IEEE IRPS evidence independently measures/models post-P/E-cycle Flash leakage across several technology generations, so the qualification relation reflects a period engineering problem rather than only standards terminology.

1253. **standard revision lineage ≠ invention lineage** — A117E can document what JEDEC says changed between its own revisions; it does not establish who first discovered or invented endurance testing, retention testing, UBER, read disturb, or bad-block management.

1254. **lower-level qualification evidence can underwrite a higher-level contract without becoming that contract** — device/cell endurance-retention tests and physics can inform an SSD qualification whose observable promise additionally depends on controller behavior, workload, host TBW, capacity, error/failure criteria, and power-state chronology.
"""
write("CASE_INDEX.md", idx.rstrip() + findings + "\n")
