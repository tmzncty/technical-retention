from pathlib import Path


def insert_after_line(text: str, needle: str, new_line: str, *, label: str) -> str:
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if needle in line]
    if len(matches) != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {len(matches)}")
    i = matches[0]
    lines.insert(i + 1, new_line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


# README navigation
p = Path("README.md")
readme = p.read_text()
if "cases/54-ddr5-rfm-split-maintenance-authority.md" not in readme:
    readme = insert_after_line(
        readme,
        "cases/53-dram-rowhammer-targeted-refresh-policy.md",
        "- [`cases/54-ddr5-rfm-split-maintenance-authority.md`](cases/54-ddr5-rfm-split-maintenance-authority.md) — grounded DDR5 Refresh Management bridge: device-advertised RFM requirement, controller-side per-bank activation accounting, host-issued maintenance opportunity, and hidden in-DRAM mitigation remain distinct; Intel 2025 platform documentation and McSee 2025 show that standardized support, enabled controller behavior, and observed execution can diverge.",
        label="README case navigation",
    )
if "evidence/54-ddr5-rfm-2022-2025-grounding.md" not in readme:
    readme = insert_after_line(
        readme,
        "evidence/53-rowhammer-2012-2020-targeted-refresh-grounding.md",
        "- [`evidence/54-ddr5-rfm-2022-2025-grounding.md`](evidence/54-ddr5-rfm-2022-2025-grounding.md) — Case-54 grounding record: Micron DDR5 manufacturer documentation grounds the MR58/RAA/RFM responsibility split and a die revision with RFM not required; Intel May-2025 first-party platform documentation and USENIX 2025 McSee independently bound controller enablement and observed command behavior.",
        label="README evidence navigation",
    )
p.write_text(readme)


# ROADMAP DRAM bridge
p = Path("ROADMAP.md")
roadmap = p.read_text()
roadmap = roadmap.replace(
    "partially advanced by ten grounded bounded sub-slices",
    "partially advanced by eleven grounded bounded sub-slices",
    1,
)
lines = roadmap.splitlines()
dram_idxs = [i for i, line in enumerate(lines) if "DRAM evolution and refresh machinery beyond the bounded case" in line]
if len(dram_idxs) != 1:
    raise SystemExit(f"ROADMAP DRAM bridge: expected one long bridge line, found {len(dram_idxs)}")
i = dram_idxs[0]
line = lines[i]
if "cases/54-ddr5-rfm-split-maintenance-authority.md" not in line:
    anchor = " The broad item stays unchecked because"
    if anchor not in line:
        raise SystemExit("ROADMAP DRAM bridge: broad-item anchor missing")
    addition = (
        " [`cases/54-ddr5-rfm-split-maintenance-authority.md`](cases/54-ddr5-rfm-split-maintenance-authority.md), "
        "grounded by [`evidence/54-ddr5-rfm-2022-2025-grounding.md`](evidence/54-ddr5-rfm-2022-2025-grounding.md), "
        "adds the later DDR5 RFM responsibility split: a device can advertise whether extra refresh management is required and expose vendor thresholds, "
        "while the controller can retain/derive per-bank activation pressure and issue an RFM maintenance opportunity for hidden in-DRAM work. "
        "A Micron die revision with `RFM not required`, Intel's May-2025 `DDR5: RFM feature is not yet enabled` platform statement, and McSee's independent 2025 bus observation "
        "separate standardized support, device requirement, controller enablement, alternative mitigation, and observed command execution."
    )
    line = line.replace(anchor, addition + anchor, 1)
old_gap = "post-2020 RowHammer / DDR5 Refresh Management (`RFM`) evolution, exact normative mitigation semantics, and independent named-product fault validation"
new_gap = "full JESD79-5 revision-by-revision RFM/ARFM/DRFM/PRAC chronology, exact later normative timing/counter semantics, and independent named-DIMM/device fault validation"
if old_gap in line:
    line = line.replace(old_gap, new_gap, 1)
lines[i] = line
roadmap = "\n".join(lines) + ("\n" if roadmap.endswith("\n") else "")
p.write_text(roadmap)


# CASE_INDEX case ledger, comparison matrix, counts, and findings
p = Path("CASE_INDEX.md")
idx = p.read_text()
lines = idx.splitlines()

case_row = "| [DDR5 Refresh Management: Split Maintenance Authority, RAA Accounting, and Platform Enablement](cases/54-ddr5-rfm-split-maintenance-authority.md) | **grounded** | periodic DRAM refresh + device-advertised RFM requirement + controller per-bank activation-pressure accounting + host-issued RFM opportunity + hidden in-DRAM mitigation | separate ordinary REF from disturbance-management time; device requirement from controller execution; activation-pressure metadata from payload; standardized support from platform enablement and empirical behavior | [2022–2025 DDR5 RFM grounding](evidence/54-ddr5-rfm-2022-2025-grounding.md); full JEDEC revision chronology, ARFM/DRFM/PRAC evolution, exact later normative timing, and independent named-DIMM fault validation remain separate work |"
if not any("cases/54-ddr5-rfm-split-maintenance-authority.md" in line for line in lines):
    anchors = [i for i, line in enumerate(lines) if "cases/53-dram-rowhammer-targeted-refresh-policy.md" in line and line.startswith("|")]
    if len(anchors) != 1:
        raise SystemExit(f"CASE_INDEX case row: expected one Case-53 ledger row, found {len(anchors)}")
    lines.insert(anchors[0] + 1, case_row)

matrix_row = "| DDR5 RFM / 2022–2025 bounded regime | dynamic-cell payload + ordinary refresh obligation + device-advertised RFM requirement/thresholds + controller activation-pressure state + platform enablement + hidden in-DRAM mitigation | periodic REF continues; controller can account per-bank ACT pressure and issue RFM to grant additional internal-management time; alternative controller mitigations may exist | ordinary reads can remain successful while activation pressure accumulates; RFM is maintenance opportunity rather than a payload read | controller-visible bank/ACT accounting scopes the pressure budget, while exact physical victim resolution can remain inside DRAM | fixed logical DRAM locations; the changed relation is maintenance responsibility and admissible activity budget rather than payload relocation | no application history; RAA-like state is rolling second-order maintenance pressure rather than a complete ACT archive, while requirement/enablement state qualifies whether the RFM path exists |"
if not any(line.startswith("| DDR5 RFM / 2022–2025 bounded regime |") for line in lines):
    anchors = [i for i, line in enumerate(lines) if line.startswith("| DRAM RowHammer / 2012–2020 bounded regime |")]
    if len(anchors) != 1:
        raise SystemExit(f"CASE_INDEX matrix row: expected one RowHammer matrix row, found {len(anchors)}")
    lines.insert(anchors[0] + 1, matrix_row)

idx = "\n".join(lines) + ("\n" if idx.endswith("\n") else "")
idx = idx.replace(
    "After fifty-four bounded cases, **all fifty-four cases are now `grounded`.**",
    "After fifty-five bounded cases, **all fifty-five cases are now `grounded`.**",
    1,
)
idx = idx.replace("currently fifty-four;", "currently fifty-five;", 1)

if "545. **ordinary periodic REF ≠ RFM maintenance opportunity**" not in idx:
    lines = idx.splitlines()
    anchors = [i for i, line in enumerate(lines) if line.startswith("544. **2014 experimental characterization ≠ invention of RowHammer-aware targeted refresh**")]
    if len(anchors) != 1:
        raise SystemExit(f"CASE_INDEX findings: expected finding 544 anchor, found {len(anchors)}")
    new_findings = [
        "545. **ordinary periodic REF ≠ RFM maintenance opportunity** — the bounded Micron DDR5 interface distinguishes baseline REFRESH requirements from additional RFM work required under high activity; RFM does not replace the ordinary retention deadline;",
        "546. **device-advertised mitigation requirement ≠ controller-side maintenance execution** — MR58 can state that extra management is required while controller-side accounting/scheduling must still create the RFM opportunity;",
        "547. **per-bank activation-pressure state ≠ payload state** — RAA-like controller accounting can be constitutive retention infrastructure because it determines when additional disturbance-management work becomes due;",
        "548. **activity accounting ≠ complete access history** — a rolling accumulated ACT budget retains enough pressure evidence for maintenance decisions without preserving an archival sequence of every activation;",
        "549. **controller RFM issuance ≠ in-DRAM mitigation algorithm** — the public command grants internal management time without exposing the device's complete victim-selection, topology, or restoration implementation;",
        "550. **host-visible bank accounting ≠ physical victim-row knowledge** — the controller can police a bank-level activation budget while physical adjacency and exact victim selection remain hidden inside the DRAM;",
        "551. **standard/interface support ≠ enabled platform behavior** — Intel document 743844 Rev. 015 (May 2025) says RFM is supported according to JEDEC while separately stating that DDR5 RFM is not yet enabled on the bounded platform family;",
        "552. **DDR5 RFM support ≠ RFM requirement for every DDR5 device** — a Micron 16Gb DDR5 die-revision addendum explicitly records `RFM not required`, so the memory-generation label alone does not determine the extra-maintenance obligation;",
        "553. **absence of RFM command ≠ absence of all RowHammer mitigation** — McSee observed no RFM commands on its tested Intel platforms but did observe additional mitigative activations, so command absence cannot be equated with zero defense;",
        "554. **platform mitigation presence ≠ conformance to a device-required RFM path** — an alternative controller defense and a DRAM's advertised RFM requirement are separate relations whose equivalence requires empirical validation rather than assumption;",
        "555. **documented capability ≠ observed execution** — manufacturer/platform documents define requirements and enablement, while McSee's bus capture separately tests what commands a running controller actually emits;",
        "556. **independent bus observation ≠ universal vendor/platform guarantee** — McSee's Intel/AMD result is strong for its tested CPUs, firmware/configurations, and DIMM pool but cannot be projected onto every DDR5 system;",
        "557. **retention work can be protocol-composed across incomplete authorities** — the device can expose requirement/threshold state, the controller can retain activity pressure and schedule a command, and the DRAM can perform opaque internal work; no one layer alone supplies the whole maintenance relation;",
        "558. **DDR5 RFM evolution ≠ origin of RowHammer-aware targeted refresh** — Case 53's 2012-priority Intel evidence already predates DDR5 RFM, so the later contribution here is the controller/device responsibility split rather than an invention claim.",
    ]
    lines[anchors[0] + 1:anchors[0] + 1] = new_findings
    idx = "\n".join(lines) + "\n"

p.write_text(idx)


# Assertions: fail the one-shot workflow rather than silently writing a malformed ledger.
readme = Path("README.md").read_text()
roadmap = Path("ROADMAP.md").read_text()
idx = Path("CASE_INDEX.md").read_text()

assert readme.count("cases/54-ddr5-rfm-split-maintenance-authority.md") == 2  # link target + text in one nav line
assert readme.count("evidence/54-ddr5-rfm-2022-2025-grounding.md") == 2
assert "partially advanced by eleven grounded bounded sub-slices" in roadmap
assert roadmap.count("cases/54-ddr5-rfm-split-maintenance-authority.md") == 2
assert idx.count("cases/54-ddr5-rfm-split-maintenance-authority.md") == 1
assert idx.count("| DDR5 RFM / 2022–2025 bounded regime |") == 1
assert "After fifty-five bounded cases, **all fifty-five cases are now `grounded`.**" in idx
assert "currently fifty-five;" in idx
assert "After fifty-four bounded cases" not in idx
assert "currently fifty-four;" not in idx
for n in range(545, 559):
    assert idx.count(f"{n}. **") == 1, n

print("Case 54 navigation/status integration validated")
