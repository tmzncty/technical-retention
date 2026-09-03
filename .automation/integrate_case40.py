from pathlib import Path


def insert_after_line(path: str, marker: str, new_line: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if new_line in text:
        return
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if marker in line]
    if len(matches) != 1:
        raise SystemExit(f"{path}: expected one marker {marker!r}, found {len(matches)}")
    lines.insert(matches[0] + 1, new_line)
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


# README navigation: keep case and evidence lists contiguous. The evidence list had drifted
# and stopped at Case 37, so restore the missing Case 38/39 records while adding Case 40.
insert_after_line(
    "README.md",
    "cases/39-geckoftl-power-failure-metadata-recovery.md",
    "- [`cases/40-raidr-retention-aware-dram-refresh.md`](cases/40-raidr-retention-aware-dram-refresh.md) — grounded retention-aware DRAM-refresh bridge: RAIDR retains row-level profiling/bin metadata in the memory controller to assign selective refresh cadence, while the 2013 commodity-DDR3 study shows that data-pattern dependence and variable retention time can make a surviving profile incomplete or non-conservative.",
)
insert_after_line(
    "README.md",
    "evidence/37-samsung-840-evo-2014-2015-performance-refresh-grounding.md",
    "- [`evidence/38-intel-2014-2015-pli-health-validation-grounding.md`](evidence/38-intel-2014-2015-pli-health-validation-grounding.md) — Case-38 grounding record: Intel DC S3700/S3500 primary documentation separates PLI event history, capacitor-readiness self-test state, manufacturer hot-unplug validation, supply-fall-time envelope, and independent-compliance limits.",
)
insert_after_line(
    "README.md",
    "evidence/38-intel-2014-2015-pli-health-validation-grounding.md",
    "- [`evidence/39-geckoftl-2015-2017-metadata-recovery-grounding.md`](evidence/39-geckoftl-2015-2017-metadata-recovery-grounding.md) — Case-39 grounding record: GeckoFTL research evidence separates nonvolatile NAND payload, Flash-resident mapping/validity metadata, checkpoint-bounded volatile state, partial-run admissibility, restart reconstruction, and commercial-deployment limits.",
)
insert_after_line(
    "README.md",
    "evidence/39-geckoftl-2015-2017-metadata-recovery-grounding.md",
    "- [`evidence/40-raidr-2012-2013-retention-profile-grounding.md`](evidence/40-raidr-2012-2013-retention-profile-grounding.md) — Case-40 grounding record: the ISCA 2012 RAIDR mechanism and ISCA 2013 248-chip retention study separate physical retention margin, profiling, row/bin maintenance metadata, conservative Bloom-filter representation, global temperature scaling, and future profile validity without claiming commercial deployment.",
)

# ROADMAP: close the bounded per-row retention-aware-policy slice while preserving broader standards/deployment gaps.
p = Path("ROADMAP.md")
roadmap = p.read_text(encoding="utf-8")
old_count = "**partially advanced by six grounded bounded sub-slices**"
new_count = "**partially advanced by seven grounded bounded sub-slices**"
if old_count in roadmap:
    roadmap = roadmap.replace(old_count, new_count, 1)
elif new_count not in roadmap:
    raise SystemExit("ROADMAP.md: DRAM sub-slice count marker not found")

case40_clause = "[`cases/40-raidr-retention-aware-dram-refresh.md`](cases/40-raidr-retention-aware-dram-refresh.md), grounded by [`evidence/40-raidr-2012-2013-retention-profile-grounding.md`](evidence/40-raidr-2012-2013-retention-profile-grounding.md), adds a row-retention-profile policy regime: measured row heterogeneity becomes retained controller bin/Bloom-filter state that selects cadence, while the 2013 DPD/VRT measurements make profile accuracy and future conservatism independent retention obligations. "
roadmap_anchor = "The broad item stays unchecked because a true JEDEC standards chronology"
if case40_clause not in roadmap:
    if roadmap_anchor not in roadmap:
        raise SystemExit("ROADMAP.md: DRAM remaining-work anchor not found")
    roadmap = roadmap.replace(roadmap_anchor, case40_clause + roadmap_anchor, 1)

old_gap = "and modern per-row retention-aware policy remain distinct open regimes;"
new_gap = "and commercial retention-aware-refresh deployment, online VRT/DPD-aware profile revalidation or ECC composition, and RowHammer-oriented refresh policy remain distinct open regimes;"
if old_gap in roadmap:
    roadmap = roadmap.replace(old_gap, new_gap, 1)
elif new_gap not in roadmap:
    raise SystemExit("ROADMAP.md: old per-row policy gap not found")
p.write_text(roadmap, encoding="utf-8")

# CASE_INDEX case row and comparison matrix.
case_row = "| [RAIDR Retention-Aware DRAM Refresh: Row Binning, Profiling Metadata, and Variable-Retention Limits](cases/40-raidr-retention-aware-dram-refresh.md) | **grounded** | volatile dynamic payload + measured row-retention heterogeneity + retained controller profile/bin metadata + Bloom-filter conservative representation + row-selective cadence + global temperature scaler | separate physical retention margin, measured profile, profile validity, row-level cadence policy, and controller-side maintenance authority; use DPD/VRT to show retained maintenance metadata can survive while becoming non-conservative | [2012–2013 RAIDR/profiling grounding](evidence/40-raidr-2012-2013-retention-profile-grounding.md); commercial deployment, online VRT-aware profiling/ECC, JEDEC standardization, and RowHammer-oriented refresh remain separate work |"
insert_after_line(
    "CASE_INDEX.md",
    "cases/39-geckoftl-power-failure-metadata-recovery.md",
    case_row,
)

comparison_row = "| RAIDR retention-aware DRAM refresh / 2012–2013 bounded research regime | dynamic-cell charge + measured row-retention profile + Bloom-filter/bin membership + controller scheduling/temperature-scaler state | controller profiles rows and applies shorter cadence to weak-row bins; global temperature scaling is separately applied; 2013 DPD/VRT evidence challenges static conservative profiles | ordinary service reads remain DRAM reads; profiling deliberately disables refresh to observe failure thresholds, while normal retention policy restores selected rows by activation/RAS-only-style refresh | row address plus controller-retained bin membership; row retention time is the minimum over cells in the row | fixed DRAM row location; identity does not migrate, but the maintenance classification attached to the row can change after re-profiling | no application history; the profile is second-order maintenance state and may be saved across boots, yet its survival does not guarantee future validity |"
insert_after_line(
    "CASE_INDEX.md",
    "| GeckoFTL power-failure metadata recovery / 2015–2017 research regime |",
    comparison_row,
)

p = Path("CASE_INDEX.md")
index = p.read_text(encoding="utf-8")
if "forty-one grounded regimes" not in index:
    if "forty grounded regimes" not in index:
        raise SystemExit("CASE_INDEX.md: grounded-regime count marker not found")
    index = index.replace("forty grounded regimes", "forty-one grounded regimes", 1)

old_bridge = "and GeckoFTL controller-metadata-recovery bridges;"
new_bridge = "GeckoFTL controller-metadata-recovery, and RAIDR retention-profile/row-selective-refresh bridges;"
if old_bridge in index:
    index = index.replace(old_bridge, new_bridge, 1)
elif new_bridge not in index:
    raise SystemExit("CASE_INDEX.md: category-coherence bridge marker not found")

findings = """369. **refresh obligation ≠ one device-wide maintenance cadence** — RAIDR preserves the dynamic-cell restoration obligation while assigning different row classes different refresh intervals; `must refresh` does not imply `refresh every row at the weakest-cell cadence`.
370. **row-retention heterogeneity ≠ temperature-conditioned global scaling** — RAIDR stores row/bin distinctions while separately applying a multiplicative temperature scaler to all rows, so spatial variation and environmental adaptation are independent policy axes.
371. **profile metadata ≠ payload, while profile metadata can be retention infrastructure** — the 2012 design can save profiling results in an OS file and reload them to control later refresh decisions; a description of substrate behavior can therefore become constitutive of retaining the payload.
372. **maintenance-metadata approximation direction matters** — RAIDR's Bloom-filter false positives cause safe over-refresh under the paper's model, whereas an omitted weak-row classification could cause unsafe under-refresh; `approximate` is not one symmetric reliability category.
373. **Bloom-filter no-false-negative property ≠ no profiling false negatives** — the set representation cannot falsely reject an inserted weak row, but the 2013 DPD/VRT evidence shows that measurement can fail to discover a weak state or can later become non-conservative.
374. **row-level retention class ≠ exact per-cell retention policy** — RAIDR defines a row's retention time as the minimum across its cells, so one weak cell can pull an entire row into a faster-maintenance class.
375. **measured retention time ≠ guaranteed future minimum retention time** — the 2013 study reports VRT transitions below prior measurements and states that even a 2x safety margin may be insufficient in the presence of VRT.
376. **retention profile ≠ immutable physical truth** — DPD makes measured retention depend on stored patterns and neighboring state, while VRT makes some cell behavior change over time; a profile is an empirical policy input, not a timeless cell constant.
377. **control-state survival ≠ control-state validity** — a saved retention profile can survive across boots while becoming stale or having been incomplete from the start; retaining maintenance metadata is insufficient unless its represented relation remains conservative.
378. **more selective maintenance ≠ zero profiling/control cost** — RAIDR reduces restoration operations by adding profiling, retained bin/Bloom-filter state, counters, hashing, row-specific commands, and temperature scaling.
379. **retention-aware refresh policy ≠ self-refresh authority** — the 2012 paper separately models DRAM self refresh as internally managed, while RAIDR keeps row-selection policy on the controller side and wakes DRAM for selected refreshes.
380. **research evaluation ≠ commercial deployment** — RAIDR's reported refresh/power/performance/storage figures are research evaluation results; the source set does not establish a shipped controller using RAIDR or a JEDEC per-row retention-profile contract.

"""
anchor = "These are provisional cross-case findings, not final philosophical conclusions."
if findings.strip() not in index:
    if anchor not in index:
        raise SystemExit("CASE_INDEX.md: findings anchor not found")
    index = index.replace(anchor, findings + anchor, 1)
p.write_text(index, encoding="utf-8")

# Sanity checks: all navigation targets and count must be present.
checks = {
    "README.md": ["cases/40-raidr-retention-aware-dram-refresh.md", "evidence/38-intel-2014-2015-pli-health-validation-grounding.md", "evidence/39-geckoftl-2015-2017-metadata-recovery-grounding.md", "evidence/40-raidr-2012-2013-retention-profile-grounding.md"],
    "ROADMAP.md": ["seven grounded bounded sub-slices", "cases/40-raidr-retention-aware-dram-refresh.md"],
    "CASE_INDEX.md": ["forty-one grounded regimes", "369. **refresh obligation", "380. **research evaluation"],
}
for path, needles in checks.items():
    text = Path(path).read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"{path}: missing expected postcondition {needle!r}")
