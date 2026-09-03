from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {count}")
    return text.replace(old, new, 1)


# README
p = Path("README.md")
text = p.read_text()
case36 = "- [`cases/36-nand-flash-correct-and-refresh-maintenance.md`](cases/36-nand-flash-correct-and-refresh-maintenance.md) — grounded NAND-Flash retention-maintenance bridge: Cai et al.’s 2012 FCR proposal periodically reads and ECC-corrects aging MLC NAND, then reprograms in place or remaps to a new block before retention errors outrun correction margin; adaptive cadence, wear metadata, and refresh-induced wear keep nonvolatility distinct from maintenance-free reliable retention."
case37 = "- [`cases/37-samsung-840-evo-old-data-performance-refresh.md`](cases/37-samsung-840-evo-old-data-performance-refresh.md) — grounded commercial-SSD old-data maintenance bridge: Samsung’s 2014 Performance Restoration path rewrote aging 840 EVO data, while its 2015 revised firmware was described by Samsung as using powered periodic refresh; the case separates logical payload survival, read-retry/calibration cost, read-path adaptation, rewrite renewal, power-off persistence, and read-performance continuity."
text = replace_once(text, case36, case36 + "\n" + case37, "README case")
ev36 = "- [`evidence/36-cai-2012-flash-correct-refresh-grounding.md`](evidence/36-cai-2012-flash-correct-refresh-grounding.md) — Case-36 grounding record: the directly inspected ICCD 2012 paper anchors FCR terminology, ECC-bounded retention-error renewal, remap versus in-place/hybrid repair, adaptive P/E-cycle-based cadence, background/power costs, and the simulation-versus-deployment evidence boundary."
ev37 = "- [`evidence/37-samsung-840-evo-2014-2015-performance-refresh-grounding.md`](evidence/37-samsung-840-evo-2014-2015-performance-refresh-grounding.md) — Case-37 grounding record: surviving Samsung restoration downloads, a later Samsung Magician guide, period direct-vendor statements, and independent 2014–2015 tests separate old-data payload survival, aggressive read-retry/service cost, rewrite restoration, immediate read-path improvement, powered periodic refresh, and manual optimization fallback without equating the product behavior with generic NAND or academic FCR."
text = replace_once(text, ev36, ev36 + "\n" + ev37, "README evidence")
p.write_text(text)


# ROADMAP
p = Path("ROADMAP.md")
text = p.read_text()
lines = text.splitlines()
prefix = "- [ ] SSD FTL/controller-mediated persistence beyond the bounded Ban/1990s case — **partially advanced by grounded Cases 15, 20, 30, 31, 32, and 36**."
matches = [i for i, line in enumerate(lines) if line.startswith(prefix)]
if len(matches) != 1:
    raise SystemExit(f"ROADMAP SSD line: expected 1 match, found {len(matches)}")
i = matches[0]
line = lines[i]
line = line.replace(
    "**partially advanced by grounded Cases 15, 20, 30, 31, 32, and 36**",
    "**partially advanced by grounded Cases 15, 20, 30, 31, 32, 36, and 37**",
    1,
)
needle = " The broad item stays unchecked because"
if line.count(needle) != 1:
    raise SystemExit("ROADMAP SSD broad-item anchor drifted")
addition = (
    " [`cases/37-samsung-840-evo-old-data-performance-refresh.md`](cases/37-samsung-840-evo-old-data-performance-refresh.md), grounded by "
    "[`evidence/37-samsung-840-evo-2014-2015-performance-refresh-grounding.md`](evidence/37-samsung-840-evo-2014-2015-performance-refresh-grounding.md), "
    "closes one commercial-deployment gap without generalizing it: Samsung's 840 EVO moved from a 2014 rewrite-based Performance Restoration action to a 2015 firmware algorithm described by Samsung as powered periodic refresh, while independent testing separates immediate read-path improvement from later rewrite/optimization effects. It therefore separates logical payload continuity, read-retry/calibration cost, service performance, powered maintenance opportunity, and physical renewal rather than treating `nonvolatile` as a complete service contract."
)
line = line.replace(needle, addition + needle, 1)
lines[i] = line
text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
phase3_anchor = "- [ ] How should `store execution`, processor/controller-buffer residence, persistence-domain arrival, synchronization completion, failure-qualified recoverability, atomicity, and ordering be separated in persistent-memory programming models?"
phase3_new = "- [ ] In controller-managed Flash, how should physical embodiment age, read-retry/calibration cost, logical payload recoverability, read-performance envelope, powered maintenance opportunity, read-path adaptation, and rewrite renewal be separated?"
text = replace_once(text, phase3_anchor, phase3_anchor + "\n" + phase3_new, "ROADMAP phase3")
p.write_text(text)


# CASE_INDEX
p = Path("CASE_INDEX.md")
text = p.read_text()
row36 = "| [NAND Flash Correct-and-Refresh: ECC-Bounded Retention Through Controller Maintenance](cases/36-nand-flash-correct-and-refresh-maintenance.md) | **grounded** | nonvolatile MLC NAND + retention-error accumulation + ECC-corrected read + remap/in-place reprogram + adaptive controller scheduling | separate physical nonvolatility from maintenance-free reliable retention; show error-margin renewal can relocate state and consume endurance | [2012 FCR grounding](evidence/36-cai-2012-flash-correct-refresh-grounding.md); commercial deployment, later 3D-NAND/read-retry interaction, vendor-specific refresh, and controller reliability genealogy remain separate work |"
row37 = "| [Samsung 840 EVO Old-Data Performance Restoration: Read Calibration, Rewrite Renewal, and Powered Periodic Refresh](cases/37-samsung-840-evo-old-data-performance-refresh.md) | **grounded** | commercial NAND SSD + age-sensitive read-retry/calibration + one-time rewrite restoration + powered background periodic refresh + manual optimization fallback | separate payload continuity from retrieval-performance continuity; read-path adaptation from physical rewrite; power-off physical persistence from powered maintenance opportunity | [2014–2018 Samsung 840 EVO grounding](evidence/37-samsung-840-evo-2014-2015-performance-refresh-grounding.md); Samsung-hosted 2014/2015 FAQ/Magician-4.6 archival recovery, exact internal read-reference algorithm, other TLC/3D-NAND products, and endurance/compliance measurements remain separate work |"
text = replace_once(text, row36, row36 + "\n" + row37, "CASE_INDEX case row")

matrix36 = "| NAND Flash FCR / 2012 bounded regime | floating-gate charge + raw error population + ECC-corrected logical payload + FTL mapping/validity + per-block P/E state | periodic/adaptive read + ECC correction + in-place reprogram or remap; background scheduling; remap consumes erase cycles | controller reads raw page, ECC produces corrected logical data before rewrite; uncorrectable threshold is a failure boundary | logical page/block designation through FTL; remap refresh may change physical block while preserving logical identity | can remain stable under in-place reprogram or deliberately change under remap; location is not required for logical continuation | no complete history; current payload plus mapping/validity/wear/error-margin policy state are retained |"
matrix37 = "| Samsung 840 EVO old-data maintenance / 2014–2015 bounded regime | NAND cell state + logical payload + FTL relation + controller read-management state + maintenance opportunity | 2014 one-time rewrite restoration; 2015 firmware described by Samsung as powered periodic refresh; supplementary Advanced Performance Optimization | old data remained a readable logical target in the bounded performance incident while aggressive read-retry/service cost could rise; independent testing saw immediate post-firmware improvement before refresh time elapsed | host logical blocks through controller/FTL; exact internal age/calibration representation is not exposed in inspected vendor sources | rewrite/migration can renew the physical embodiment while preserving logical payload; read-path adaptation can also improve service without a demonstrated rewrite | no history by default; current payload plus hidden mapping/read-management/maintenance state |"
text = replace_once(text, matrix36, matrix36 + "\n" + matrix37, "CASE_INDEX matrix")

text = replace_once(
    text,
    "After thirty-seven bounded cases, **all thirty-seven cases are now `grounded`.**",
    "After thirty-eight bounded cases, **all thirty-eight cases are now `grounded`.**",
    "CASE_INDEX count",
)
text = replace_once(
    text,
    "**category coherence is provisional and evidence-gated** — thirty-seven grounded regimes now support",
    "**category coherence is provisional and evidence-gated** — thirty-eight grounded regimes now support",
    "CASE_INDEX finding80 count",
)
text = replace_once(
    text,
    "and NAND-Flash FCR controller-maintenance bridges;",
    "NAND-Flash FCR controller-maintenance, and commercial Samsung 840 EVO old-data performance-refresh bridges;",
    "CASE_INDEX finding80 mechanism list",
)

f339 = "339. **retention refresh ≠ integrity scrub** — ZFS/GFS verification cases seek evidence that retained copies are already corrupt/inconsistent, whereas FCR is a proactive controller policy intended to renew an aging NAND page before time/wear-dependent raw errors outrun ECC. Both can run in background, but their failure models and repair semantics differ."
new_findings = """340. **logical payload continuity ≠ retrieval-performance continuity** — Samsung framed the bounded 840 EVO incident as old-data read-performance degradation rather than data loss; a value can remain recoverable while the throughput/latency cost of retrieving it degrades sharply.
341. **cell-state survival ≠ constant-cost interpretation of cell state** — Samsung's 2014 explanation says SSD software calibrates changes in cell status over time and that the faulty 840 EVO algorithm performed read-retry aggressively; interpreting a surviving physical state can itself acquire age-dependent work.
342. **successful read-retry ≠ bounded read-service cost** — repeated recovery attempts can still return the intended logical bytes while violating the expected performance envelope; recoverability and efficient service are separate retention targets.
343. **read-path improvement ≠ rewrite-based renewal** — PC Perspective measured a large stale-data improvement immediately after the 2015 firmware update, before the drive had time for background refresh; the reviewer's exact read-algorithm explanation remains inference, but the timing rejects `all improvement = later rewriting`.
344. **one successful restoration ≠ stable future maintenance closure** — Samsung's 2014 rewrite-based Performance Restoration restored old-data speed, yet stale samples later slowed again and the 2015 remediation introduced a firmware policy described as periodic refresh.
345. **unpowered physical persistence ≠ unpowered availability of maintenance work** — Samsung explicitly said the periodic-refresh algorithm does not operate while power is off; NAND can retain payload across an unpowered interval while the controller loses the opportunity to perform performance-maintenance work.
346. **power-off retention interval ≠ powered maintenance opportunity** — Samsung separately identified insufficient run-time and extended power-off as circumstances in which Advanced Performance Optimization might be needed, making available powered time part of the service-maintenance relation without redefining NAND as volatile.
347. **automatic background maintenance ≠ zero service cost** — Samsung acknowledged possible occasional foreground performance effects from SSD background work, and later Magician documentation says Advanced Performance Optimization takes time and can reduce responsiveness on a documented platform.
348. **performance retention ≠ physical-embodiment continuity** — the 2014 Samsung statement says migrated/overwritten data does not show the old-data symptom and the restoration software rewrites old data; the same logical payload can regain service performance through a renewed physical embodiment.
349. **commercial refresh deployment ≠ generic NAND requirement or academic-algorithm identity** — Case 37 grounds one Samsung 840 EVO remediation sequence; it neither proves that all TLC/NAND products require the same policy nor establishes that Samsung implemented Cai et al.'s 2012 FCR algorithms."""
text = replace_once(text, f339, f339 + "\n\n" + new_findings, "CASE_INDEX findings")
p.write_text(text)
