from pathlib import Path


def insert_after_line(text: str, needle: str, new_line: str, *, last: bool = False) -> str:
    if new_line in text:
        return text
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if needle in line]
    if not hits:
        raise RuntimeError(f"anchor not found: {needle}")
    idx = hits[-1] if last else hits[0]
    lines.insert(idx + 1, new_line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


# README
p = Path("README.md")
t = p.read_text()
case_anchor = "- [`cases/34-micron-temperature-dependent-dram-refresh.md`](cases/34-micron-temperature-dependent-dram-refresh.md) — grounded temperature-conditioned DRAM refresh bridge: Micron’s 1991-filed circuit maps a nearby temperature sensor through discrete comparator bands into oscillator/refresh cadence, separating the continuing refresh obligation from a worst-case fixed maintenance frequency and preserving earlier 1987-priority temperature-adaptive prior art."
case_new = "- [`cases/35-micron-mobile-ddr-automatic-tcsr.md`](cases/35-micron-mobile-ddr-automatic-tcsr.md) — grounded commercial Mobile DDR TCSR bridge: Micron’s Rev. J 2/08 product contract combines internally clocked self refresh with automatic on-die temperature control of the self-refresh oscillator, keeps PASR retention coverage separately controller-programmable, and distinguishes DPD array-payload loss from surviving mode-register state."
if case_new not in t:
    if case_anchor not in t:
        raise RuntimeError("README Case 34 anchor missing")
    t = t.replace(case_anchor, case_anchor + "\n" + case_new, 1)
ev_anchor = "- [`evidence/34-micron-1991-temperature-dependent-refresh-grounding.md`](evidence/34-micron-1991-temperature-dependent-refresh-grounding.md) — Case-34 grounding record: Micron US5278796A anchors sensor → band classification → oscillator → refresh cadence, CardioData’s 1987-priority family blocks a Micron-first claim, and a later self-refresh patent preserves the cadence-versus-authority boundary."
ev_new = "- [`evidence/35-micron-2005-2008-mobile-ddr-tcsr-grounding.md`](evidence/35-micron-2005-2008-mobile-ddr-tcsr-grounding.md) — Case-35 grounding record: Micron’s Rev. J 2/08 Mobile DDR product datasheet directly anchors automatic on-die temperature control of the self-refresh oscillator, inert TCSR programming bits on this version, controller-selectable PASR coverage, internally clocked self refresh, and the DPD split between lost array payload and retained mode-register values."
if ev_new not in t:
    if ev_anchor not in t:
        raise RuntimeError("README Case 34 evidence anchor missing")
    t = t.replace(ev_anchor, ev_anchor + "\n" + ev_new, 1)
p.write_text(t)

# ROADMAP
p = Path("ROADMAP.md")
t = p.read_text()
t = t.replace("partially advanced by five grounded bounded sub-slices", "partially advanced by six grounded bounded sub-slices", 1)
old = "and [`cases/34-micron-temperature-dependent-dram-refresh.md`](cases/34-micron-temperature-dependent-dram-refresh.md), grounded by [`evidence/34-micron-1991-temperature-dependent-refresh-grounding.md`](evidence/34-micron-1991-temperature-dependent-refresh-grounding.md), adds temperature-conditioned cadence selection, guardband classification, sensor/control overhead, and an explicit prior-art boundary back to a 1987-priority ambient-temperature refresh system. The broad item stays unchecked because a true JEDEC standards chronology, exact normative DDR5 timing, broader LPDDR/per-bank refresh genealogy, standardized/commercial temperature-compensated self-refresh evolution beyond this patent slice, and modern per-row retention-aware policy remain distinct open regimes;"
new = "and [`cases/34-micron-temperature-dependent-dram-refresh.md`](cases/34-micron-temperature-dependent-dram-refresh.md), grounded by [`evidence/34-micron-1991-temperature-dependent-refresh-grounding.md`](evidence/34-micron-1991-temperature-dependent-refresh-grounding.md), adds temperature-conditioned cadence selection, guardband classification, sensor/control overhead, and an explicit prior-art boundary back to a 1987-priority ambient-temperature refresh system; [`cases/35-micron-mobile-ddr-automatic-tcsr.md`](cases/35-micron-mobile-ddr-automatic-tcsr.md), grounded by [`evidence/35-micron-2005-2008-mobile-ddr-tcsr-grounding.md`](evidence/35-micron-2005-2008-mobile-ddr-tcsr-grounding.md), then supplies the commercial automatic-TCSR bridge: internally clocked self refresh and on-die temperature-conditioned cadence coexist while PASR retention coverage remains separately controller-selectable, and DPD separates array-payload loss from surviving mode-register state. The broad item stays unchecked because a true JEDEC standards chronology, exact normative DDR5 timing, broader LPDDR/per-bank refresh genealogy, later LPDDR sensor/thermal-offset and fault-qualification semantics, and modern per-row retention-aware policy remain distinct open regimes;"
if old in t:
    t = t.replace(old, new, 1)
elif new not in t:
    raise RuntimeError("ROADMAP DRAM anchor missing")
p.write_text(t)

# CASE_INDEX
p = Path("CASE_INDEX.md")
t = p.read_text()
marker = "## Comparison matrix — provisional"
if marker not in t:
    raise RuntimeError("comparison marker missing")
before, after = t.split(marker, 1)
case_row = "| [Micron Mobile DDR Automatic TCSR: On-Die Temperature Sensing, Self-Refresh Cadence, and Selective Retention](cases/35-micron-mobile-ddr-automatic-tcsr.md) | **grounded** | volatile dynamic payload + internally clocked self refresh + on-die temperature-controlled oscillator + controller-selectable PASR coverage + DPD/control-state split | separate field presence from effective software authority; cadence from coverage; external-clock absence from maintenance absence; array-payload retention from control-state retention | [2005–2008 Mobile DDR TCSR grounding](evidence/35-micron-2005-2008-mobile-ddr-tcsr-grounding.md); full JEDEC TCSR/PASR genealogy, later LPDDR thermal/sensor semantics, and per-row retention-aware refresh remain separate work |"
before = insert_after_line(before, "cases/34-micron-temperature-dependent-dram-refresh.md", case_row, last=True)
matrix_row = "| [Micron Mobile DDR Automatic TCSR](cases/35-micron-mobile-ddr-automatic-tcsr.md) | dynamic-cell charge + on-die temperature sensor/oscillator + EMR/PASR control state | internal self-refresh cycles; temperature-conditioned cadence; selected-region maintenance | normal SDRAM reads are nondestructive at the interface level | bank/row/column access in ordinary operation; internal refresh addressing during self refresh | logical array locations remain designated, but PASR changes which locations receive retention work | No — PASR-excluded array state and DPD array payload can be intentionally lost |"
if matrix_row not in after:
    section_end = "\n---\n"
    pos = after.find(section_end)
    if pos < 0:
        raise RuntimeError("comparison matrix end marker missing")
    after = after[:pos].rstrip() + "\n" + matrix_row + "\n\n" + after[pos:]
t = before + marker + after

findings = """319. **register-field presence ≠ effective software authority** — the bounded Mobile DDR EMR still displays TCSR-labelled positions while the datasheet explicitly says programming them has no effect because the on-die sensor controls the self-refresh oscillator.
320. **temperature-conditioned cadence ≠ host-visible cadence programmability** — automatic on-die sensing can select a temperature-appropriate self-refresh rate without granting the controller effective TCSR-bit authority on this product version.
321. **external-clock absence ≠ maintenance absence** — SELF REFRESH retains array data without external clocking precisely because the SDRAM supplies internal clocking and performs its own recurring refresh cycles.
322. **self-refresh cadence authority ≠ retained-array coverage authority** — the device automatically controls cadence from temperature while PASR separately lets the controller choose which banks/segments continue receiving refresh.
323. **self-refresh active ≠ whole-array retained** — under PASR, only selected regions are refreshed and the datasheet explicitly warns that data in excluded regions will be lost.
324. **array-payload retention ≠ mode/control-state retention** — Deep Power-Down stops retaining array data while the documented mode-register and extended-mode-register values survive exit from DPD; the physical mechanism for that control-state survival remains unspecified.
325. **lower retention cost ≠ one uniform reduction of retention work** — TCSR reduces maintenance frequency, PASR reduces maintained state coverage, and DPD abandons array retention; three power-saving features change different retention relations.
326. **automatic commercial TCSR ≠ invention priority or complete JEDEC genealogy** — Case 34 already grounds earlier temperature-adaptive prior art, while this product datasheet and Micron technical note do not replace revision-by-revision normative JEDEC evidence.
327. **low-power mode ≠ retention mode** — ordinary power-down performs no refresh and is time-limited by the refresh period, SELF REFRESH performs internal maintenance, and DPD intentionally loses array payload; low-power states require mode-specific retention semantics."""
if "319. **register-field presence ≠ effective software authority**" not in t:
    token = "\n\nThese are provisional cross-case findings"
    if token not in t:
        raise RuntimeError("findings marker missing")
    t = t.replace(token, "\n\n" + findings + token, 1)

summary_anchor = "Case 34 is the grounded temperature-conditioned refresh continuation; [`evidence/34-micron-1991-temperature-dependent-refresh-grounding.md`](evidence/34-micron-1991-temperature-dependent-refresh-grounding.md) uses Micron's 1991-filed patent to anchor nearby temperature sensing, discrete guardbanded classification, oscillator-selected cadence, and sensing/control power tradeoffs, while the patent's own citation of a 1987-priority CardioData family blocks a Micron-first claim. It adds environmental condition → measurement/proxy → policy band → cadence to the DRAM retention decomposition without projecting later JEDEC TCSR, on-chip self-refresh authority, or per-row retention-aware refresh backward."
summary_new = "Case 35 is the grounded commercial automatic-TCSR continuation; [`evidence/35-micron-2005-2008-mobile-ddr-tcsr-grounding.md`](evidence/35-micron-2005-2008-mobile-ddr-tcsr-grounding.md) uses Micron's Rev. J 2/08 Mobile DDR product contract plus period manufacturer context to combine internally clocked SELF REFRESH with automatic on-die temperature control, while preserving independent PASR coverage authority and a DPD payload/control-state split. It closes the commercial-product bridge left by Case 34 without pretending the product datasheet is a complete JEDEC genealogy."
if summary_new not in t:
    if summary_anchor not in t:
        raise RuntimeError("Case 34 summary anchor missing")
    t = t.replace(summary_anchor, summary_anchor + "\n" + summary_new, 1)

t = t.replace("thirty-five grounded regimes", "thirty-six grounded regimes", 1)
t = t.replace("currently thirty-five;", "currently thirty-six;", 1)
t = t.replace(
    "named-product adoption, JEDEC temperature-compensated-self-refresh genealogy, exact modern DDR/LPDDR semantics, sensor fault qualification, and per-row retention-aware scheduling remain separate work",
    "commercial automatic TCSR is now handled separately in Case 35; JEDEC temperature-compensated-self-refresh genealogy, exact later DDR/LPDDR semantics, sensor fault qualification, and per-row retention-aware scheduling remain separate work",
    1,
)
p.write_text(t)
