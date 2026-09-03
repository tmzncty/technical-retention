from pathlib import Path


def insert_after_line(text: str, needle: str, new_line: str) -> str:
    if new_line in text:
        return text
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if needle in line:
            lines.insert(i + 1, new_line)
            suffix = "\n" if text.endswith("\n") else ""
            return "\n".join(lines) + suffix
    raise RuntimeError(f"anchor not found: {needle}")


# README navigation
p = Path("README.md")
t = p.read_text()
t = insert_after_line(
    t,
    "cases/35-micron-mobile-ddr-automatic-tcsr.md",
    "- [`cases/36-nand-flash-correct-and-refresh-maintenance.md`](cases/36-nand-flash-correct-and-refresh-maintenance.md) — grounded NAND-Flash retention-maintenance bridge: Cai et al.’s 2012 FCR proposal periodically reads and ECC-corrects aging MLC NAND, then reprograms in place or remaps to a new block before retention errors outrun correction margin; adaptive cadence, wear metadata, and refresh-induced wear keep nonvolatility distinct from maintenance-free reliable retention.",
)
t = insert_after_line(
    t,
    "evidence/35-micron-2005-2008-mobile-ddr-tcsr-grounding.md",
    "- [`evidence/36-cai-2012-flash-correct-refresh-grounding.md`](evidence/36-cai-2012-flash-correct-refresh-grounding.md) — Case-36 grounding record: the directly inspected ICCD 2012 paper anchors FCR terminology, ECC-bounded retention-error renewal, remap versus in-place/hybrid repair, adaptive P/E-cycle-based cadence, background/power costs, and the simulation-versus-deployment evidence boundary.",
)
p.write_text(t)


# ROADMAP: extend the SSD/controller-mediated retention bridge without closing the broad item.
p = Path("ROADMAP.md")
t = p.read_text()
old = "**partially advanced by grounded Cases 15, 20, 30, 31, and 32**"
new = "**partially advanced by grounded Cases 15, 20, 30, 31, 32, and 36**"
if old in t:
    t = t.replace(old, new, 1)
elif new not in t:
    raise RuntimeError("SSD case-count anchor not found")

start = t.find("- [ ] SSD FTL/controller-mediated persistence")
end = t.find("\n- [ ] RAID / scrubbing / rebuild", start)
if start < 0 or end < 0:
    raise RuntimeError("SSD roadmap section boundary not found")
section = t[start:end]
addition = (
    "[`cases/36-nand-flash-correct-and-refresh-maintenance.md`](cases/36-nand-flash-correct-and-refresh-maintenance.md), "
    "grounded by [`evidence/36-cai-2012-flash-correct-refresh-grounding.md`](evidence/36-cai-2012-flash-correct-refresh-grounding.md), "
    "adds a different controller-maintenance regime above nonvolatile NAND: time/wear-dependent retention errors may remain ECC-correctable before logical loss, while FCR renews correction margin through in-place reprogramming or remapping; adaptive cadence reuses P/E-cycle metadata, and overly aggressive refresh can itself consume endurance or create program-interference errors. "
)
if "cases/36-nand-flash-correct-and-refresh-maintenance.md" not in section:
    marker = "The broad item stays unchecked because"
    if marker not in section:
        raise RuntimeError("SSD open-gap marker not found")
    section = section.replace(marker, addition + marker, 1)
    t = t[:start] + section + t[end:]
p.write_text(t)


# CASE_INDEX case ledger, comparison matrix, counts, and findings.
p = Path("CASE_INDEX.md")
t = p.read_text()
case_row = "| [NAND Flash Correct-and-Refresh: ECC-Bounded Retention Through Controller Maintenance](cases/36-nand-flash-correct-and-refresh-maintenance.md) | **grounded** | nonvolatile MLC NAND + retention-error accumulation + ECC-corrected read + remap/in-place reprogram + adaptive controller scheduling | separate physical nonvolatility from maintenance-free reliable retention; show error-margin renewal can relocate state and consume endurance | [2012 FCR grounding](evidence/36-cai-2012-flash-correct-refresh-grounding.md); commercial deployment, later 3D-NAND/read-retry interaction, vendor-specific refresh, and controller reliability genealogy remain separate work |"
t = insert_after_line(t, "cases/35-micron-mobile-ddr-automatic-tcsr.md", case_row)

matrix_row = "| NAND Flash FCR / 2012 bounded regime | floating-gate charge + raw error population + ECC-corrected logical payload + FTL mapping/validity + per-block P/E state | periodic/adaptive read + ECC correction + in-place reprogram or remap; background scheduling; remap consumes erase cycles | controller reads raw page, ECC produces corrected logical data before rewrite; uncorrectable threshold is a failure boundary | logical page/block designation through FTL; remap refresh may change physical block while preserving logical identity | can remain stable under in-place reprogram or deliberately change under remap; location is not required for logical continuation | no complete history; current payload plus mapping/validity/wear/error-margin policy state are retained |"
t = insert_after_line(t, "| [Micron Mobile DDR Automatic TCSR]", matrix_row)

old_count = "After thirty-six bounded cases, **all thirty-six cases are now `grounded`.**"
new_count = "After thirty-seven bounded cases, **all thirty-seven cases are now `grounded`.**"
if old_count in t:
    t = t.replace(old_count, new_count, 1)
elif new_count not in t:
    raise RuntimeError("cross-case count anchor not found")

t = t.replace("thirty-six grounded regimes now support", "thirty-seven grounded regimes now support", 1)
old80 = "commercial Mobile-DDR automatic-TCSR/selective-retention bridges;"
new80 = "commercial Mobile-DDR automatic-TCSR/selective-retention, and NAND-Flash FCR controller-maintenance bridges;"
if old80 in t:
    t = t.replace(old80, new80, 1)
elif new80 not in t:
    raise RuntimeError("finding-80 mechanism-list anchor not found")
t = t.replace("currently thirty-six;", "currently thirty-seven;", 1)

if "328. **nonvolatile medium ≠ maintenance-free reliable retention" not in t:
    marker = "\nThese are provisional cross-case findings, not final philosophical conclusions."
    if marker not in t:
        raise RuntimeError("findings footer marker not found")
    findings = """
328. **nonvolatile medium ≠ maintenance-free reliable retention at a specified error target** — the 2012 FCR proposal starts from NAND cells that remain nonvolatile yet accumulate time/wear-dependent retention errors; periodic controller work is proposed to keep those errors inside an ECC-qualified reliability margin without redefining Flash as DRAM-like volatile memory.
329. **raw physical error accumulation ≠ immediate logical payload loss** — the controller can ECC-correct a page whose raw NAND read already contains retention errors, so physical degradation can precede host-visible logical failure.
330. **ECC-correctability margin ≠ indefinite retention margin** — correctable errors are surviving error budget, not proof that maintenance can be postponed without bound; FCR is deliberately scheduled before accumulated errors exceed the chosen ECC capability.
331. **long logical retention interval ≠ one uninterrupted physical-embodiment interval** — the paper’s bounded model uses repeated short refresh intervals to satisfy a longer storage objective; the specific three-day/three-year numbers are experiment/model results, not universal NAND constants.
332. **Flash FCR `refresh` ≠ DRAM refresh** — FCR may remap corrected data to a newly erased block or add charge in place through ISPP, while DRAM refresh restores volatile dynamic-cell state through a different substrate, granularity, and control path. Shared vocabulary supports a functional comparison, not mechanism identity.
333. **retention maintenance ≠ location stability** — remapping-based FCR preserves a logical designation by programming corrected data to a new physical block and updating the map, extending Case 04’s identity/location separation under a new trigger: retention-error margin rather than ordinary rewrite/reclamation pressure.
334. **more maintenance ≠ more lifetime** — more frequent remapping adds erase/reclaim cycles, and the paper reports workload regimes in which increasing refresh frequency eventually reduces projected lifetime.
335. **maintenance operation ≠ error-neutral repair** — in-place reprogramming can repair charge-loss retention errors while also introducing program-interference errors and cannot remove charge to repair the opposite error direction; hybrid FCR therefore needs a distinct remap fallback.
336. **refresh cadence ≠ one fixed medium constant** — adaptive-rate FCR begins with no refresh in the bounded early-life regime and increases cadence with P/E wear and observed error behavior; maintenance frequency is policy/state dependent rather than one timeless property of NAND.
337. **payload retention can depend on retained maintenance metadata** — adaptive FCR relies on per-block P/E-cycle and validity state already maintained for wear leveling; those controller records are not user payload but help determine future preservation work.
338. **FCR proposal/evaluation ≠ commercial deployment** — the 46× headline is produced by SSD simulation driven by measured chip characterization and workload traces; it must not be rewritten as a measured multi-year production-drive lifetime or universal deployed controller contract.
339. **retention refresh ≠ integrity scrub** — ZFS/GFS verification cases seek evidence that retained copies are already corrupt/inconsistent, whereas FCR is a proactive controller policy intended to renew an aging NAND page before time/wear-dependent raw errors outrun ECC. Both can run in background, but their failure models and repair semantics differ.
"""
    t = t.replace(marker, "\n" + findings.strip() + "\n" + marker, 1)

p.write_text(t)


# Final invariants.
checks = {
    "README case": (Path("README.md"), "cases/36-nand-flash-correct-and-refresh-maintenance.md"),
    "README evidence": (Path("README.md"), "evidence/36-cai-2012-flash-correct-refresh-grounding.md"),
    "ROADMAP case": (Path("ROADMAP.md"), "cases/36-nand-flash-correct-and-refresh-maintenance.md"),
    "CASE_INDEX case": (Path("CASE_INDEX.md"), case_row),
    "CASE_INDEX matrix": (Path("CASE_INDEX.md"), matrix_row),
    "CASE_INDEX count": (Path("CASE_INDEX.md"), new_count),
    "CASE_INDEX finding": (Path("CASE_INDEX.md"), "339. **retention refresh ≠ integrity scrub**"),
}
for name, (path, needle) in checks.items():
    if needle not in path.read_text():
        raise RuntimeError(f"postcondition failed: {name}")
