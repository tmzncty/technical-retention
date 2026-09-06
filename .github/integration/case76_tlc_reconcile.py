from pathlib import Path


def update(path, old, new, label):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"{label}: expected one anchor, found {text.count(old)}")
    text = text.replace(old, new, 1).rstrip("\n") + "\n"
    p.write_text(text, encoding="utf-8", newline="\n")


update(
    "evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md",
    "10. **HPE Solid State Disk Drives QuickSpecs Version 72 + P5430 product page (January 2026)** — manufacturer/OEM primary evidence for a named QLC P5430 SKU, its host-level endurance rating, and HPE's three-month unpowered post-endurance data-retention statement; used as a product witness, not an independent JEDEC compliance audit or raw-cell retention measurement.",
    "10. **HPE Solid State Disk Drives QuickSpecs Version 72 + P5430 product page (January 2026)** — manufacturer/OEM primary evidence for the named QLC P5430 `P63934-B21` witness and the same-document TLC CM7 `P61183-B21` cross-check, their host-level endurance ratings, and HPE's three-month unpowered post-endurance data-retention statement; used as a bounded product-contract comparison, not an independent JEDEC compliance audit, controlled TLC/QLC experiment, or raw-cell retention measurement.",
    "evidence source hierarchy",
)

update(
    "CASE_INDEX.md",
    "1583. **one named QLC product witness ≠ universal TLC/QLC comparison** — Case 76 now has a bounded QLC-era product witness, while TLC cross-checks, cross-vendor QLC evidence, direct qualification reports, and post-rating fault tests remain open.",
    "1583. **one named QLC product witness ≠ universal TLC/QLC comparison** — the original P5430-only witness was insufficient for a TLC/QLC comparison; the named TLC cross-check below advances that gap while still leaving cross-vendor evidence, controlled media comparisons, direct qualification reports, and post-rating fault tests open.",
    "CASE_INDEX finding 1583",
)
