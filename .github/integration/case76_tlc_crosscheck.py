from pathlib import Path


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    text = text.rstrip("\n") + "\n"
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one anchor, found {count}")
    return text.replace(old, new, 1)


# --- Case 76 ---------------------------------------------------------------
case_path = "cases/76-jedec-ssd-endurance-retention-qualification.md"
case = read(case_path)

status_old = (
    "A January 2026 HPE QuickSpecs/product witness now adds a named QLC P5430 SKU "
    "to the commercial-product layer, while keeping its QLC media label, workload "
    "label, write-endurance rating, and post-endurance power-off retention statement "
    "separate from raw-cell physics or an independently audited JESD218 compliance claim."
)
status_new = status_old + (
    " The same QuickSpecs now also supplies a bounded 7.68 TB TLC CM7 cross-check, "
    "used only to compare product-level endurance/retention contracts rather than to "
    "infer a universal TLC-versus-QLC media law."
)
case = replace_once(case, status_old, status_new, "case status")

engineering_marker = "\n---\n\n## Engineering reconstruction"
tlc_section = r'''

### HPE 2026 CM7: a same-capacity TLC cross-check, not a media-only experiment

The same **5 January 2026** HPE QuickSpecs provides a useful control against overreading the P5430's QLC label. The exact **P61183-B21** CM7 SKU is also **7.68 TB** and E3.S/NVMe, but HPE classifies it as **Read Intensive (`RI`)**, **Gen5 High Performance**, and **`TLC`**. Its corresponding speeds/endurance row gives **14,016 TB lifetime writes** and **1 DWPD**.[^hpe-qspec]

Because the QuickSpecs' `Data Retention` clause applies the same **three-month, no-power, post-maximum-rated-write-endurance** statement to the listed SSD family, the document supplies a bounded commercial comparison in which two equal-capacity products carry different media labels and different rated-write envelopes while remaining under the same family-level post-endurance retention clause.[^hpe-qspec]

That is useful precisely because it does **not** isolate NAND density as a causal variable. The products also differ in workload class (`RI` versus `VRO`), product/controller generation, performance positioning, and likely implementation details that the QuickSpecs does not disclose. Therefore:

```text
same nominal capacity (7.68 TB)
    !=
same workload class
    !=
same media label
    !=
same lifetime-write / DWPD rating
    !=
same controller or product generation

and

same product-family retention clause
    !=
same prior endurance history
    !=
same raw-cell retention law
```

The historically supportable product statement is narrow: **HPE documented a 7.68 TB TLC CM7 at 14,016 TB / 1 DWPD and a 7.68 TB QLC P5430 at 8,040 TB / 0.57 DWPD in the same QuickSpecs family, whose general data-retention clause states three months unpowered after maximum rated write endurance.** It is not evidence that TLC intrinsically has a particular multiple of QLC endurance, that the two drives use the same controller/ECC margin, or that equal capacity makes the pair a controlled media-physics experiment.
'''
case = replace_once(case, engineering_marker, tlc_section + engineering_marker, "case TLC section")

case = replace_once(
    case,
    "later JESD218 revision history, TLC named-product comparison, and cross-vendor QLC qualification/fault evidence remain separate work best coordinated with `computing-archaeology`.",
    "later JESD218 revision history, and broader cross-vendor TLC/QLC qualification/fault evidence remain separate work best coordinated with `computing-archaeology`. The bounded HPE same-capacity TLC/QLC product cross-check is now grounded above; it is not a substitute for controlled media experiments or independent qualification evidence.",
    "case prior-art open work",
)
case = replace_once(
    case,
    "Fresh repository searches for `JESD219A`, `SSD endurance workload`, `P5430`, and `QLC retention JESD218 SSD` found no dedicated `computing-archaeology` case to reuse;",
    "Fresh repository searches for `JESD219A`, `SSD endurance workload`, `P5430`, `CM7`, and `TLC QLC SSD retention` found no dedicated `computing-archaeology` case to reuse;",
    "case related-repo search",
)

cross_marker = "\nIt complements:\n"
cross_add = (
    "\nThe CM7 cross-check sharpens that warning: **same nominal capacity and the same "
    "family-level post-endurance retention interval ≠ a controlled TLC/QLC comparison**. "
    "The documented endurance ratings differ, but workload class, product generation, "
    "controller design, ECC margin, and other implementation variables are not held constant. "
    "The comparison therefore constrains product-contract interpretation without ranking the "
    "intrinsic retention physics of TLC and QLC.\n"
)
case = replace_once(case, cross_marker, cross_add + cross_marker, "case cross-case TLC result")
write(case_path, case)


# --- Evidence 76 -----------------------------------------------------------
ev_path = "evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md"
ev = read(ev_path)

ev = replace_once(
    ev,
    "## Source 10 — HPE P5430 QLC product witness, QuickSpecs Version 72, January 2026",
    "## Source 10 — HPE QLC/TLC commercial-product pair, QuickSpecs Version 72, January 2026",
    "evidence Source 10 heading",
)

loc_anchor = "- corresponding `Speeds and Feeds` table: `P63934-B21` is listed at **8,040 TB Lifetime Writes** and **0.57 Endurance DWPD**."
loc_new = loc_anchor + (
    "\n- the same E3.S capacity/workload table lists **`P61183-B21`**, a **7.68 TB** "
    "Gen5 High Performance Read Intensive CM7 SSD, with `Flash Type` **TLC**;\n"
    "- its corresponding `Speeds and Feeds` row gives **14,016 TB Lifetime Writes** and **1 Endurance DWPD**."
)
ev = replace_once(ev, loc_anchor, loc_new, "evidence TLC locators")

product_anchor = "- HPE independently described the P5430 product family as QLC 3D NAND."
product_new = product_anchor + (
    "\n- within the same Version 72 document, HPE also documented the equal-capacity "
    "`P61183-B21` CM7 as TLC/RI with a 14,016 TB / 1 DWPD product endurance rating;\n"
    "- the document-level `Data Retention` clause therefore supplies one common "
    "post-endurance retention statement above two differently labeled/rated products."
)
ev = replace_once(ev, product_anchor, product_new, "evidence direct-grounding TLC bullets")

recon_anchor = "The source set is especially useful because the media-density label and the SSD-level service envelope coexist in one manufacturer product family without becoming the same variable."
recon_new = recon_anchor + r'''

The TLC/QLC pair adds a second bounded relation:

```text
P61183-B21: 7.68 TB / RI / TLC / 14,016 TB / 1 DWPD
    !=
P63934-B21: 7.68 TB / VRO / QLC / 8,040 TB / 0.57 DWPD

while both remain under the same QuickSpecs family-level
three-month post-maximum-endurance no-power retention statement.
```

This is **product-contract comparison**, not a controlled experiment. Equal user capacity does not hold workload class, interface/product generation, controller design, ECC margin, over-provisioning, NAND process, firmware, or qualification method constant.
'''
ev = replace_once(ev, recon_anchor, recon_new, "evidence TLC reconstruction")

limit_anchor = (
    "This source therefore closes only a **named QLC product / post-endurance unpowered-retention witness**. "
    "It does not establish that all QLC SSDs have three-month retention, that QLC cells intrinsically retain for three months, "
    "or that TLC/QLC density alone determines an SSD's endurance/retention contract."
)
limit_new = (
    "This source now closes only a **bounded named HPE TLC/QLC commercial-product cross-check** above the already-grounded QLC witness. "
    "It does not establish that all TLC or QLC SSDs have three-month retention, that either cell type intrinsically retains for three months, "
    "that the higher rated writes of the cited TLC CM7 are caused by TLC rather than the many other differing product variables, or that TLC/QLC density alone determines an SSD's endurance/retention contract."
)
ev = replace_once(ev, limit_anchor, limit_new, "evidence limit")

claim_marker = "\n---\n\n## Rejected shortcuts"
claim_rows = r'''
| HPE QuickSpecs Version 72 lists exact CM7 `P61183-B21` as 7.68 TB RI/TLC | H/P | HPE 2026 E3.S capacity/workload table | direct named-product/OEM witness |
| HPE documents 14,016 TB lifetime writes / 1 DWPD for P61183-B21 | H/P | HPE 2026 speeds/endurance table | direct product rating; host-level metric, not raw P/E count |
| Equal 7.68 TB capacity ≠ controlled TLC/QLC media experiment | E/X | HPE P61183 + P63934 rows | strong anti-overreach boundary: workload class, generation, controller/media internals are not controlled |
| Same family-level three-month retention clause ≠ same prior endurance history | E | HPE retention clause + product endurance rows | bounded product-contract reconstruction; each rating defines a different maximum-rated-endurance precondition |
| Higher TLC product TBW in this pair ≠ proof that TLC intrinsically causes higher endurance | E/X | HPE product rows only | causal mechanism not identified by the source |
| Same post-endurance interval across the pair ≠ same raw-cell retention law | E/X | HPE family clause + TLC/QLC labels | controller/media qualification remains undisclosed |
'''
ev = replace_once(ev, claim_marker, "\n" + claim_rows.rstrip("\n") + claim_marker, "evidence TLC claim rows")

shortcut_anchor = "- `Endurance exhaustion is sanitization.`"
shortcut_new = (
    "- `Matching 7.68 TB capacity makes P61183-B21 and P63934-B21 a controlled TLC-versus-QLC media experiment.`\n"
    "- `Because the cited TLC CM7 has a higher HPE lifetime-write rating, TLC intrinsically has higher endurance by that ratio.`\n"
    "- `Because both products sit under the same three-month HPE retention clause, TLC and QLC raw cells have the same retention law.`\n"
    + shortcut_anchor
)
ev = replace_once(ev, shortcut_anchor, shortcut_new, "evidence rejected TLC shortcuts")

ev = replace_once(
    ev,
    "searches in `tmzncty/computing-archaeology` for `JESD218`, `JESD22-A117`, `P5430`, and `QLC retention JESD218 SSD` did not find a dedicated case.",
    "searches in `tmzncty/computing-archaeology` for `JESD218`, `JESD22-A117`, `P5430`, `CM7`, and `TLC QLC SSD retention` did not find a dedicated case.",
    "evidence related-repo search",
)
write(ev_path, ev)


# --- ROADMAP ---------------------------------------------------------------
road_path = "ROADMAP.md"
road = read(road_path)
road = replace_once(
    road,
    "post-rating fault tests, TLC named-product validation, cross-vendor QLC corroboration, and independent compliance testing remain open; the narrower HPE P5430 QLC product witness is now grounded separately below.",
    "post-rating fault tests, broader cross-vendor TLC/QLC corroboration, and independent compliance testing remain open; the narrower HPE TLC/QLC commercial-product comparison is now grounded separately below.",
    "roadmap JESD218 remaining work",
)
road = replace_once(
    road,
    "- [x] Named QLC commercial-product post-endurance retention witness — canonical",
    "- [x] Named QLC/TLC commercial-product post-endurance retention comparison — canonical",
    "roadmap product heading",
)
road = replace_once(
    road,
    "This is a bounded manufacturer/OEM product witness, not a raw QLC-cell retention law, an independently audited JESD218 compliance certificate, or a claim that HPE's VRO workload label equals a JEDEC application class. TLC named-product comparison, cross-vendor QLC corroboration, direct later-JESD218 revision archaeology, and post-rating fault tests remain open.",
    "The same Version 72 now adds equal-capacity TLC CM7 `P61183-B21` (7.68 TB, RI, 14,016 TB / 1 DWPD) under the same family-level three-month post-endurance no-power clause. This is a bounded manufacturer/OEM product-contract comparison, not a raw TLC/QLC-cell retention law, an independently audited JESD218 compliance certificate, or a controlled media-only experiment: workload class, product generation, controller/ECC margin, and other implementation variables differ. Cross-vendor TLC/QLC corroboration, direct later-JESD218 revision archaeology, independent compliance evidence, and post-rating fault tests remain open.",
    "roadmap TLC cross-check detail",
)
write(road_path, road)


# --- CASE_INDEX ------------------------------------------------------------
idx_path = "CASE_INDEX.md"
idx = read(idx_path)
idx_anchor = (
    "1583. **one named QLC product witness ≠ universal TLC/QLC comparison** — Case 76 now has a bounded QLC-era product witness, while TLC cross-checks, cross-vendor QLC evidence, direct qualification reports, and post-rating fault tests remain open."
)
idx_add = idx_anchor + r'''

### Case 76 HPE TLC/QLC commercial cross-check — same capacity, different rated-write envelopes, shared retention clause

1584. **same nominal capacity ≠ controlled media comparison** — HPE lists both cited drives at 7.68 TB, but the TLC CM7 is RI/Gen5 High Performance while the QLC P5430 is VRO/Gen4 Mainstream Performance; equal capacity does not hold the rest of the product relation constant.
1585. **TLC flash-type label ≠ causal explanation of a product endurance rating** — the CM7's 14,016 TB / 1 DWPD exceeds the P5430's 8,040 TB / 0.57 DWPD in this pair, but the document does not isolate NAND cell density from controller, workload, generation, over-provisioning, firmware, or qualification policy.
1586. **same product-family retention clause ≠ same endurance rating** — both products sit under HPE's three-month post-maximum-endurance no-power statement while their lifetime-write/DWPD ratings differ.
1587. **same post-endurance retention interval ≠ same prior write history** — the common three-month interval starts only after each product reaches its own maximum rated write endurance; an equal endpoint duration does not erase different preconditions.
1588. **same retained service interval ≠ same raw-cell retention law** — HPE's product-family contract is controller/media inclusive and does not disclose a TLC-versus-QLC threshold-voltage or charge-loss equivalence.
1589. **workload label difference ≠ media label difference** — `RI` versus `VRO` and `TLC` versus `QLC` are separate axes in the QuickSpecs; neither label can be substituted for the other when explaining rated endurance.
1590. **same manufacturer document ≠ independent qualification evidence** — one QuickSpecs creates a strong internally consistent product comparison, but it is not an independent laboratory audit of either drive's JESD218 path or post-rating fault behavior.
1591. **bounded HPE TLC/QLC comparison ≠ universal TLC/QLC ranking** — the named pair closes the roadmap's TLC product cross-check only; cross-vendor corroboration, controlled media comparisons, direct later-standard archaeology, independent compliance testing, and fault injection remain open.
'''
idx = replace_once(idx, idx_anchor, idx_add, "CASE_INDEX TLC findings")
write(idx_path, idx)
