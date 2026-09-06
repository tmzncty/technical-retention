from pathlib import Path


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    if not text.endswith("\n"):
        text += "\n"
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one anchor, found {count}")
    return text.replace(old, new, 1)


# --- Case 76 ---------------------------------------------------------------
case_path = "cases/76-jedec-ssd-endurance-retention-qualification.md"
case = read(case_path)

status_anchor = (
    "The 2010→2012 workload chronology is now further bounded by July 2012 "
    "JESD219A publication metadata and its separately distributed Master/Test "
    "Trace artifacts; this does not substitute for direct inspection of the "
    "normative JESD219A body."
)
status_new = status_anchor + (
    " A January 2026 HPE QuickSpecs/product witness now adds a named QLC P5430 "
    "SKU to the commercial-product layer, while keeping its QLC media label, "
    "workload label, write-endurance rating, and post-endurance power-off "
    "retention statement separate from raw-cell physics or an independently "
    "audited JESD218 compliance claim."
)
case = replace_once(case, status_anchor, status_new, "case status")

p3608_anchor = (
    "### Intel 2015 P3608: a named enterprise product contract\n\n"
    "Intel's September 2015 DC P3608 product specification states that the series meets or exceeds JESD218 endurance and retention requirements. Its reliability table defines data retention as retention in NAND at maximum rated endurance and specifies **three months of power-off retention once rated write endurance is reached at 40 °C**. The same table gives PBW endurance ratings and links endurance verification to JESD218.[^p3608]\n\n"
    "This is a named commercial witness for the enterprise-class relation. It is not evidence that every SSD implements the same hidden wear-management mechanism.\n"
)
qlc_section = p3608_anchor + """

### HPE 2026 P5430: a named QLC product witness without a substrate shortcut

HPE's **5 January 2026** _HPE Solid State Disk Drives_ QuickSpecs Version 72 lists the P5430 family under `NVMe Main Performance Very-read-optimized EDSFF E3.S SSDs`. The exact **P63934-B21** 7.68 TB SKU is labeled `VRO`, `NVMe`, `E3.S`, and **`QLC`**; the corresponding speeds/endurance table gives **8,040 TB lifetime writes** and **0.57 DWPD**.[^hpe-qspec] HPE's product page independently describes the P5430 family as using **Next Gen QLC 3D NAND**.[^hpe-p5430]

The same QuickSpecs defines `Data Retention` as retaining NAND data after the **maximum rated endurance level** has been reached, and states that these SSDs are rated for **three months with no power applied once maximum rated write endurance is reached**.[^hpe-qspec]

This gives a named modern QLC commercial witness for the same broad end-of-endurance → unpowered-retention relation that Case 76 studies, but it must not be overread. The cited HPE rows do **not** disclose the P5430's raw-cell retention curve, ECC/retry budget, over-provisioning, wear distribution, refresh policy, or qualification raw data. Nor does the cited P5430 row itself say `JESD218`; the HPE statement is therefore retained here as a manufacturer/OEM product-family contract, **not** silently promoted into an independent JEDEC-compliance certificate.

The bounded decomposition is:

```text
QLC media label
    !=
product workload label (VRO)
    !=
lifetime-write / DWPD endurance rating
    !=
post-endurance unpowered retention requirement
    !=
raw NAND-cell retention law
```

In particular, the fact that HPE's product-family statement also uses a three-month interval does not prove that the P5430 reached that number through the identical test path, temperature condition, controller margin, or standards revision used by the September 2010 JESD218 enterprise row.
"""
case = replace_once(case, p3608_anchor, qlc_section, "case QLC section")

prior_anchor = (
    "A full pre-2000 EEPROM/Flash qualification genealogy, direct facsimile archaeology of original A117/A117B, the complete JESD219 workload history, and later JESD218 revision history remain separate work best coordinated with `computing-archaeology`. A fresh repository search for `JESD219A`, `SSD endurance workload`, and the trace-artifact names found no dedicated `computing-archaeology` case to reuse; this repository therefore keeps only the bounded retention-specific standard/trace relation while leaving any broad standards genealogy to that companion project."
)
prior_new = (
    "A full pre-2000 EEPROM/Flash qualification genealogy, direct facsimile archaeology of original A117/A117B, the complete JESD219 workload history, later JESD218 revision history, TLC named-product comparison, and cross-vendor QLC qualification/fault evidence remain separate work best coordinated with `computing-archaeology`. Fresh repository searches for `JESD219A`, `SSD endurance workload`, `P5430`, and `QLC retention JESD218 SSD` found no dedicated `computing-archaeology` case to reuse; this repository therefore keeps only the bounded retention-specific standard/product relation while leaving broad standards and NAND-generation genealogy to that companion project."
)
case = replace_once(case, prior_anchor, prior_new, "case related-repo boundary")

cross_anchor = (
    "    !=\nactual instant of future unreadability\n```"
)
cross_new = (
    "    !=\nactual instant of future unreadability\n```\n\n"
    "The HPE P5430 witness adds a second orthogonal warning: **NAND density label (for example QLC) ≠ the SSD-level endurance/retention contract**. Product-class media, host-workload assumptions, controller correction margin, rated writes, and the later unpowered interval remain separate relations even when a vendor documents them in one QuickSpecs family."
)
case = replace_once(case, cross_anchor, cross_new, "case cross-case QLC result")

p3608_footnote = (
    "[^p3608]: Intel, **_Intel Solid-State Drive DC P3608 Series Product Specification_**, 333055-001US, September 2015, especially §2.6 / Table 14: <https://www.intel.com/content/dam/www/public/us/en/documents/product-specifications/ssd-dc-p3608-spec.pdf>."
)
hpe_footnotes = p3608_footnote + """

[^hpe-qspec]: Hewlett Packard Enterprise, **_HPE Solid State Disk Drives_**, QuickSpecs Version 72, dated **5 January 2026**. Versioned PDF: <https://www.hpe.com/psnow/downloadDoc/HPE%20Solid%20State%20Disk%20Drives%20QuickSpecs-a00001288enw.pdf?contentDisposition=attachment&deepLink=&form=false&hf=regular&id=a00001288enw.pdf&isFutureVersion=true&isLinearized=false&originalObjectName=&prelaunchSection=&preview=false&print=&r=&section=&softrollSection=&ver=72>. Relevant locations: `Data Retention` under Standard Features; the E3.S SKU table identifying `P63934-B21` / P5430 as `QLC`; its `Lifetime Writes (TB)` / `Endurance DWPD` table; and the Summary of Changes identifying Version 72 as 05-Jan-2026.
[^hpe-p5430]: Hewlett Packard Enterprise, **HPE 7.68TB NVMe Gen4 Mainstream Performance Very Read Optimized E3S EC1 EDSFF P5430 SSD**, SKU `P63934-B21`, product page: <https://buy.hpe.com/us/en/options/drives-storage/server-solid-state-drives/hpe-7-68tb-nvme-gen4-mainstream-performance-very-read-optimized-e3s-ec1-edsff-p5430-ssd/p/p63934-b21>. The page identifies the family as `Next Gen QLC 3D NAND`; the QuickSpecs remains the stronger source for the retention and rated-write relation.
"""
case = replace_once(case, p3608_footnote, hpe_footnotes.rstrip("\n"), "case HPE footnotes")
write(case_path, case)


# --- Evidence 76 -----------------------------------------------------------
ev_path = "evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md"
ev = read(ev_path)
ev = replace_once(
    ev,
    "# Case 76 Grounding — JESD218 SSD Endurance Rating and Power-Off Retention, 2000–2015",
    "# Case 76 Grounding — JESD218 SSD Endurance Rating and Power-Off Retention, 2000–2026",
    "evidence title",
)

source9 = (
    "9. **JEDEC/Accuris JESD219A + MT/TT catalog records (July 2012)** — publication and supporting-artifact evidence that the client workload had become a standard-plus-trace artifact set; used below the authority of directly inspected normative text."
)
source10 = source9 + (
    "\n10. **HPE Solid State Disk Drives QuickSpecs Version 72 + P5430 product page (January 2026)** — manufacturer/OEM primary evidence for a named QLC P5430 SKU, its host-level endurance rating, and HPE's three-month unpowered post-endurance data-retention statement; used as a product witness, not an independent JEDEC compliance audit or raw-cell retention measurement."
)
ev = replace_once(ev, source9, source10, "evidence source hierarchy")

qual_marker = "\n---\n\n## Qualification-semantics deepening from the original JESD218 facsimile"
source10_section = r'''

---

## Source 10 — HPE P5430 QLC product witness, QuickSpecs Version 72, January 2026

**Documents:**

- Hewlett Packard Enterprise, _HPE Solid State Disk Drives_, QuickSpecs **Version 72**, dated **5 January 2026**: <https://www.hpe.com/psnow/downloadDoc/HPE%20Solid%20State%20Disk%20Drives%20QuickSpecs-a00001288enw.pdf?contentDisposition=attachment&deepLink=&form=false&hf=regular&id=a00001288enw.pdf&isFutureVersion=true&isLinearized=false&originalObjectName=&prelaunchSection=&preview=false&print=&r=&section=&softrollSection=&ver=72>;
- HPE product page for **P63934-B21**, _HPE 7.68TB NVMe Gen4 Mainstream Performance Very Read Optimized E3S EC1 EDSFF P5430 SSD_: <https://buy.hpe.com/us/en/options/drives-storage/server-solid-state-drives/hpe-7-68tb-nvme-gen4-mainstream-performance-very-read-optimized-e3s-ec1-edsff-p5430-ssd/p/p63934-b21>.

### Exact locations inspected

QuickSpecs Version 72:

- `Summary of Changes`: Version 72 is dated **05-Jan-2026**;
- `Standard Features` → `Data Retention`: HPE defines data retention as retaining NAND data once the maximum rated endurance level has occurred and states that the listed SSDs are rated for **3 months if no power is applied once maximum rated write endurance is reached**;
- `PCIe/NVMe EDSFF E3.S – SKUs`: `P63934-B21` is the HPE 7.68 TB Gen4 Mainstream Performance Very-read-optimized P5430 SSD and its `Flash Type` is **QLC**;
- corresponding `Speeds and Feeds` table: `P63934-B21` is listed at **8,040 TB Lifetime Writes** and **0.57 Endurance DWPD**.

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

### Evidence limit

The HPE documents are **manufacturer/OEM product documentation**, not an independent qualification laboratory report. The P5430 table rows do not expose raw-cell threshold-voltage distributions, controller ECC margin, over-provisioning, wear-leveling distribution, refresh/rewrite policy, or retention-test raw data. The cited P5430 row also does not explicitly state `JESD218`, so this record does **not** infer a particular JEDEC revision, temperature profile, or compliance path merely because HPE's three-month interval resembles the 2010 enterprise-class figure.

This source therefore closes only a **named QLC product / post-endurance unpowered-retention witness**. It does not establish that all QLC SSDs have three-month retention, that QLC cells intrinsically retain for three months, or that TLC/QLC density alone determines an SSD's endurance/retention contract.
'''
ev = replace_once(ev, qual_marker, source10_section + qual_marker, "evidence Source 10")

claim_anchor = (
    "| Table 1 retention duration is condition-specific rather than a universal shelf-life constant | H/P/E | JESD218 §6.3 + Annex C | direct standard/example + bounded interpretation |"
)
claim_new = claim_anchor + """

| HPE QuickSpecs Version 72 lists exact P5430 `P63934-B21` as QLC | H/P | HPE 2026 E3.S SKU table + product page | direct named-product/OEM witness |
| HPE documents 8,040 TB lifetime writes / 0.57 DWPD for P63934-B21 | H/P | HPE 2026 speeds/endurance table | direct product rating; host-level metric, not raw P/E count |
| HPE states three months unpowered after maximum rated write endurance for covered SSDs | H/P | HPE 2026 `Data Retention` clause | direct manufacturer/OEM product-family statement; not independent lab certification |
| QLC label ≠ SSD-level retention contract or raw-cell retention constant | E | HPE media-type + endurance + retention fields | strong bounded reconstruction; controller/media internals remain undisclosed |
| same three-month interval ≠ proof of identical JESD218 qualification path | E/X | HPE 2026 + JESD218 2010 | explicit anti-overreach boundary; HPE P5430 row does not name JESD218 |
"""
ev = replace_once(ev, claim_anchor, claim_new.rstrip("\n"), "evidence claim ledger")

reject_anchor = "- `Endurance exhaustion is sanitization.`"
reject_new = """- `A QLC label by itself implies a universal three-month raw-cell retention constant.`
- `HPE's P5430 row proves an independently audited JESD218 qualification or the exact JESD218 revision/test path.`
- `HPE's VRO workload label is interchangeable with JEDEC's Client or Enterprise application class.`
- `The same three-month number in HPE and JESD218 proves identical controller margin, temperature conditions, or qualification chronology.`
- `Endurance exhaustion is sanitization.`"""
ev = replace_once(ev, reject_anchor, reject_new, "evidence rejected shortcuts")

related_anchor = (
    "Before this deepening, searches in `tmzncty/computing-archaeology` for `JESD218` and `JESD22-A117` did not find a dedicated case. The full JEDEC/NAND qualification genealogy therefore was **not** recreated here. If a standards-history slice is later built there, Case 76 should link to it and keep only this retention-specific decomposition between lower-level device qualification and the SSD-level service contract."
)
related_new = (
    "Before this deepening, searches in `tmzncty/computing-archaeology` for `JESD218`, `JESD22-A117`, `P5430`, and `QLC retention JESD218 SSD` did not find a dedicated case. The full JEDEC/NAND-generation qualification genealogy therefore was **not** recreated here. If a standards-history or QLC-controller slice is later built there, Case 76 should link to it and keep only this retention-specific decomposition between lower-level media type, host-rated endurance, and the SSD-level post-endurance service contract."
)
ev = replace_once(ev, related_anchor, related_new, "evidence related repo check")
write(ev_path, ev)


# --- ROADMAP ---------------------------------------------------------------
road_path = "ROADMAP.md"
road = read(road_path)
open_phrase = (
    "Direct normative JESD218A/JESD219A facsimiles, later B/C revision history, post-rating fault tests, and TLC/QLC named-product validation remain open."
)
new_phrase = (
    "Direct normative JESD218A/JESD219A facsimiles, later B/C revision history, post-rating fault tests, TLC named-product validation, cross-vendor QLC corroboration, and independent compliance testing remain open; the narrower HPE P5430 QLC product witness is now grounded separately below."
)
road = replace_once(road, open_phrase, new_phrase, "roadmap Case 76 open boundary")

ceph_marker = "- [x] Ceph `deep scrub` historical prior-art deepening —"
if ceph_marker not in road:
    raise SystemExit("roadmap insertion marker missing")
qlc_bullet = (
    "- [x] Named QLC commercial-product post-endurance retention witness — canonical [`cases/76-jedec-ssd-endurance-retention-qualification.md`](cases/76-jedec-ssd-endurance-retention-qualification.md), with [`evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md`](evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md), now adds HPE _Solid State Disk Drives_ QuickSpecs Version 72 (5 January 2026) and exact P5430 `P63934-B21`: the SKU is labeled QLC, carries an 8,040 TB / 0.57 DWPD endurance rating, and sits under HPE's explicit three-month no-power data-retention statement after maximum rated write endurance. This is a bounded manufacturer/OEM product witness, not a raw QLC-cell retention law, an independently audited JESD218 compliance certificate, or a claim that HPE's VRO workload label equals a JEDEC application class. TLC named-product comparison, cross-vendor QLC corroboration, direct later-JESD218 revision archaeology, and post-rating fault tests remain open.\n"
)
road = road.replace(ceph_marker, qlc_bullet + ceph_marker, 1)
write(road_path, road)


# --- CASE_INDEX ------------------------------------------------------------
idx_path = "CASE_INDEX.md"
idx = read(idx_path)
last = (
    "1572. **ATA off-line self-test ≠ SCSI BMS ≠ host SCSI VERIFY** — Cases 55, 101, and 103 support a bounded maintenance-locus/qualification analogy, but different triggers, scopes, execution contracts, and retained result state do not establish historical genealogy."
)
if idx.count(last) != 1:
    raise SystemExit(f"CASE_INDEX last-anchor count {idx.count(last)}")
append = last + r'''

## Case 76 HPE P5430 QLC product deepening — media label, rated writes, and post-endurance retention

1573. **QLC flash-type label ≠ raw-cell retention interval** — HPE identifies the named P5430 SKU as QLC while stating an SSD-level post-endurance retention requirement; the product contract cannot be reduced to an intrinsic three-month property of every QLC cell.
1574. **product workload label (`VRO`) ≠ JEDEC Client/Enterprise application class** — HPE's market/workload classification and JESD218's qualification classes answer different questions even when both condition endurance interpretation.
1575. **lifetime writes (TB) ≠ DWPD** — HPE publishes both an accumulated host-write quantity and a normalized daily-write rate for the same P5430 SKU; neither should be silently substituted for the other or for raw NAND P/E cycles.
1576. **maximum rated write endurance ≠ instant physical unreadability** — HPE defines a retention interval beginning after the rated endurance boundary, which itself demonstrates that crossing the rating is not equivalent to immediate payload disappearance.
1577. **three-month post-endurance retention ≠ three-month shelf life from manufacture or first write** — the HPE interval is conditioned on having reached maximum rated write endurance and then removing power.
1578. **product-family retention statement ≠ disclosed controller/media mechanism** — the QuickSpecs supplies an external service statement without exposing ECC margin, over-provisioning, wear distribution, refresh policy, or the raw-cell retention curve.
1579. **named QLC SKU + retention statement ≠ independent JEDEC compliance certification** — the cited P5430 row does not name JESD218, so the project does not infer a standards revision or audit path from a superficially similar interval.
1580. **same three-month interval ≠ same qualification conditions** — HPE's three-month product statement and the September 2010 JESD218 enterprise row cannot be equated without evidence for temperature, workload, revision, test method, and controller-margin equivalence.
1581. **2026 commercial witness ≠ 2010 historical adoption evidence** — the modern P5430 demonstrates that the end-of-endurance → unpowered-retention relation remains product-visible in a QLC-era offering; it does not prove when HPE, Micron, or the industry first adopted that relation.
1582. **NAND density/generation label ≠ host-visible endurance contract** — QLC identifies cell encoding density, while the SSD's host-rated write budget and later retention obligation emerge through media, controller, workload, and qualification relations above that label.
1583. **one named QLC product witness ≠ universal TLC/QLC comparison** — Case 76 now has a bounded QLC-era product witness, while TLC cross-checks, cross-vendor QLC evidence, direct qualification reports, and post-rating fault tests remain open.
'''
idx = idx.replace(last, append, 1)
write(idx_path, idx)

# Final content assertions
for path, needles in {
    case_path: ["HPE 2026 P5430", "[^hpe-qspec]", "8,040 TB"],
    ev_path: ["## Source 10 — HPE P5430 QLC product witness", "2000–2026", "independent JEDEC compliance"],
    road_path: ["Named QLC commercial-product post-endurance retention witness", "P63934-B21"],
    idx_path: ["1573.", "1583.", "Case 76 HPE P5430 QLC product deepening"],
}.items():
    text = read(path)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"{path}: missing {needle}")

print("case76 QLC product witness integration applied")
