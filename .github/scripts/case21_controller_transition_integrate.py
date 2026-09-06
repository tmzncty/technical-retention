from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "cases/21-micron-sdram-refresh-mode-handoff.md"
EVIDENCE = ROOT / "evidence/21-micron-1999-sdram-refresh-mode-grounding.md"
README = ROOT / "README.md"
ROADMAP = ROOT / "ROADMAP.md"
INDEX = ROOT / "CASE_INDEX.md"


def read(path):
    return path.read_text(encoding="utf-8")


def write(path, text):
    path.write_text(text, encoding="utf-8")


def replace_once(path, old, new):
    text = read(path)
    assert text.count(old) == 1, f"expected one match in {path}: {old[:80]!r}"
    write(path, text.replace(old, new, 1))


def insert_before(path, anchor, addition):
    text = read(path)
    assert addition.strip() not in text, f"addition already present in {path}"
    assert text.count(anchor) == 1, f"expected one anchor in {path}: {anchor!r}"
    write(path, text.replace(anchor, addition + "\n\n" + anchor, 1))


def insert_after_prefix_line(path, prefix, addition):
    text = read(path)
    assert addition.strip() not in text, f"addition already present in {path}"
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    assert len(hits) == 1, f"expected one prefix in {path}: {prefix!r}, got {len(hits)}"
    i = hits[0]
    lines[i + 1:i + 1] = ["", addition]
    write(path, "\n".join(lines) + ("\n" if text.endswith("\n") else ""))


def replace_prefix_line(path, prefix, new_line):
    text = read(path)
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    assert len(hits) == 1, f"expected one prefix in {path}: {prefix!r}, got {len(hits)}"
    lines[hits[0]] = new_line
    write(path, "\n".join(lines) + ("\n" if text.endswith("\n") else ""))


# ---- Case 21 --------------------------------------------------------------
replace_once(
    CASE,
    "**`grounded`** — bounded to the refresh command/mode semantics documented for Micron's 64Mb x4/x8/x16 SDR SDRAM family in the November 1999 (`Rev. 11/99`) manufacturer datasheet.",
    "**`grounded`** — bounded primarily to the refresh command/mode semantics documented for Micron's 64Mb x4/x8/x16 SDR SDRAM family in the November 1999 (`Rev. 11/99`) manufacturer datasheet, with a later Infineon XMC4700/XMC4800 external-memory-controller witness (2016) used only to deepen the system-side distinction among self-refresh request, observed transition completion, power-down admission, and access readiness."
)

insert_before(
    CASE,
    "## Retained state and control state",
    r'''## Later system/controller witness — Infineon XMC4700/XMC4800 EBU (2016)

Infineon's _XMC4700 / XMC4800 XMC4000 Family Reference Manual_, V1.3 (2016-07), adds a later controller-side composition that the 1999 Micron device document does not expose.[^infineon-ebu]

In §14.12.18 (printed p. 14-82), software requests self-refresh entry by writing `SELFREN`. The EBU then precharges the banks and issues the self-refresh command to the attached SDRAM devices. A separate read-only `SELFRENST` bit reports the status of that operation; the manual states that power-down may be entered safely when the command has completed. Exit is similarly split: software writes `SELFREX`, the controller raises CKE, and read-only `SELFREXST` reports completion before SDRAM access resumes. The same section also describes an optional post-exit auto-refresh step and a programmable `SELFREX_DLY` NOP interval before later access.[^infineon-ebu]

The register description on printed pp. 14-120–14-122 makes the request/status separation explicit: `SELFREN` and `SELFREX` are writable command controls, while `SELFRENST` and `SELFREXST` are read-only status fields. A later official Infineon XMCLib API preserves this distinction in software-facing form through entry/exit-status enums and `XMC_EBU_SdramGetRefreshStatus()`.[^infineon-xmclib]

This is **not** evidence that the XMC controller was paired with the 1999 Micron part, that Micron used Infineon's internal logic, or that the 2016 register model defines the 1999 historical meaning of `SELF REFRESH`. It is a later primary system witness for a separate layer: the controller must decide when the device transition is sufficiently complete to admit a surrounding power-state change or ordinary access.'''
)

insert_before(
    CASE,
    "### Self refresh is not nonvolatility",
    r'''### Command request, observed transition completion, and system admission are separate

The Micron device contract already separates mode entry/exit from ordinary service timing. The later Infineon controller makes a further system-level distinction visible:

```text
software requests entry
    !=
controller observes/records entry-command completion
    !=
system admits power-down

software requests exit
    !=
controller observes/records exit-command completion
    !=
post-exit delay/refresh work completes
    !=
ordinary SDRAM access is admitted
```

This is a bounded engineering reconstruction from two historical interfaces separated by seventeen years. It does not assert a direct genealogy between the products.

The status bits are also not physical proof that every DRAM cell is healthy. They are controller-level evidence that the documented command transition has been issued/completed sufficiently for the next system action under that controller's contract. Therefore:

> **transition-completion evidence ≠ direct measurement of payload retention margin**.

And:

> **retention-mode admission ≠ power-down/access admission**.

A small amount of non-payload control state can thus gate whether a much larger dynamic-memory payload is treated as safely maintainable across a system power-state transition.'''
)

insert_before(
    CASE,
    "## Prior art and anti-anachronism",
    r'''The later controller witness adds two failure boundaries without inventing measured failure rates:

- software can request self-refresh entry yet violate the controller's documented sequencing if surrounding power-down is admitted before the entry transition is complete;
- software can request self-refresh exit yet resume SDRAM access before exit status and the configured post-exit delay/refresh sequence permit access.

Neither condition is automatically identical to immediate payload loss. It means the system has crossed outside the documented transition/admission contract; the actual physical outcome still depends on device timing, refresh continuity, power, and workload.'''
)

insert_before(
    CASE,
    "## Functional analogy and philosophical limit",
    r'''The 2016 Infineon controller is used only as a **later system-composition witness**. It is not projected backward as Micron's 1999 internal implementation, not treated as a JEDEC normative chronology, and not used to infer a direct Micron→Infineon lineage. Its value here is relational: a system controller can retain explicit transition status and delay policy around an SDRAM self-refresh mode whose recurring maintenance work is performed inside the memory device.'''
)

replace_once(
    CASE,
    "| Retained data in self refresh remain ordinarily serviceable without exiting the mode | X | contradicted by input/CKE and exit semantics |",
    "| Infineon XMC4700/XMC4800 EBU exposes separate writable self-refresh entry/exit controls and read-only entry/exit status | H/P | 2016 Infineon reference manual §14.12.18 and SDRMREF register description |\n| Infineon gates safe power-down/access on completion of the corresponding self-refresh transition | H/P | 2016 Infineon reference manual printed p. 14-82 |\n| Self-refresh request, transition-completion evidence, and system admission are separate retention-control relations | E | bounded reconstruction from Micron 1999 + Infineon 2016; no direct genealogy claim |\n| Controller transition status proves every DRAM cell has sufficient physical retention margin | X | status is command/controller evidence, not a direct cell-retention measurement |\n| Retained data in self refresh remain ordinarily serviceable without exiting the mode | X | contradicted by input/CKE and exit semantics |"
)

replace_once(
    CASE,
    "3. For earlier self-refresh prior-art control rather than Micron product semantics: Takayasu Sakurai and Tetsuya Iizuka, Toshiba Corp., US4682306A, _Self-refresh control circuit for dynamic semiconductor memory device_, Japanese priority 20 August 1984: <https://patents.google.com/patent/US4682306A/en>.",
    "3. For earlier self-refresh prior-art control rather than Micron product semantics: Takayasu Sakurai and Tetsuya Iizuka, Toshiba Corp., US4682306A, _Self-refresh control circuit for dynamic semiconductor memory device_, Japanese priority 20 August 1984: <https://patents.google.com/patent/US4682306A/en>.\n4. [^infineon-ebu]: Infineon Technologies AG, _XMC4700 / XMC4800 XMC4000 Family Reference Manual_, EBU V1.6, manual V1.3, 2016-07, especially §14.12.18 printed p. 14-82 and SDRMREF register description pp. 14-120–14-122: <https://www.infineon.com/assets/row/public/documents/30/44/infineon-referencemanual-xmc4700-xmc4800-um-en.pdf>.\n5. [^infineon-xmclib]: Infineon Technologies AG, XMCLib EBU driver, official `Infineon/mtb-xmclib-cat3` repository, `XMC_EBU_SdramGetRefreshStatus` and self-refresh entry/exit status enums: <https://github.com/Infineon/mtb-xmclib-cat3/blob/c24888699c6c5cfd6e5475be90d9703e43540d04/XMCLib/inc/xmc_ebu.h>."
)

# ---- Evidence 21 ----------------------------------------------------------
replace_once(
    EVIDENCE,
    "# Grounding Record — Micron 64Mb SDRAM AUTO REFRESH / SELF REFRESH Mode Handoff (1999)",
    "# Grounding Record — Micron 64Mb SDRAM Refresh-Mode Handoff (1999), with Controller Transition Witness (2016)"
)

insert_before(
    EVIDENCE,
    "## Prior-art control — Cases 09 and 10",
    r'''## Source 4 — Infineon XMC4700/XMC4800 EBU reference manual, 2016

**Source:** Infineon Technologies AG, _XMC4700 / XMC4800 XMC4000 Family Reference Manual_, External Bus Unit (EBU) V1.6, manual V1.3, 2016-07.

**Official PDF:** <https://www.infineon.com/assets/row/public/documents/30/44/infineon-referencemanual-xmc4700-xmc4800-um-en.pdf>

### Printed p. 14-82 — system-side self-refresh sequencing

Section 14.12.18 states that SDRAM self refresh performs internal refresh sequences from an on-chip timer. For controller-managed entry, software writes `SELFREN`; the EBU precharges the banks and issues self refresh to all attached SDRAM devices. Read-only `SELFRENST` reflects the status of issuing/completing this command, and the manual explicitly makes successful completion the point after which power-down can be entered safely.

For exit, software writes `SELFREX`; the EBU asserts CKE for the SDRAM devices; read-only `SELFREXST` reflects completion, after which SDRAM accesses may proceed. The section then describes optional `ARFSH` work and `SELFREX_DLY`, a programmed NOP interval before later access.

This supports a controller-level distinction among **request**, **transition completion evidence**, **power-state admission**, and **ordinary access admission**. It does not directly measure cell-level retention margin.

### Printed pp. 14-120–14-122 — request/status register split

The SDRMREF register exposes separate fields for:

- writable `SELFREN` — issue Self Refresh Entry;
- read-only/status `SELFRENST` — entry command successfully issued;
- writable `SELFREX` — issue Self Refresh Exit / Power Up;
- read-only/status `SELFREXST` — exit command successfully issued;
- `SELFREX_DLY` — NOP cycles after exit before another command is permitted;
- `AUTOSELFR` — controller-managed automatic entry/exit around external-bus ownership.

The exact wording varies between the operational section and field descriptions (`completion` versus `successfully issued`). The repository therefore uses the conservative phrase **controller-observed transition/command-completion evidence** rather than treating the bit as a direct electrical proof of DRAM-cell state.

## Source 5 — later official Infineon XMCLib API continuity

**Source:** Infineon Technologies AG, XMCLib EBU driver in the official `Infineon/mtb-xmclib-cat3` repository:
<https://github.com/Infineon/mtb-xmclib-cat3/blob/c24888699c6c5cfd6e5475be90d9703e43540d04/XMCLib/inc/xmc_ebu.h>

The driver preserves separate self-refresh-entry and self-refresh-exit status identifiers and exposes `XMC_EBU_SdramGetRefreshStatus()`. This is **later implementation/API continuity**, not evidence for 1999 Micron behavior and not an origin claim for this controller architecture.'''
)

replace_once(
    EVIDENCE,
    "6. `tmzncty/computing-archaeology` was searched for `SDRAM`, `SELF REFRESH`, `AUTO REFRESH`, and `CKE`; no dedicated overlapping retention case was found.",
    "6. `tmzncty/computing-archaeology` was searched for `SDRAM`, `SELF REFRESH`, `AUTO REFRESH`, and `CKE`; no dedicated overlapping retention case was found.\n7. the 2016 Infineon XMC4700/XMC4800 reference manual supplies an independent manufacturer-primary controller/system witness for entry/exit request-versus-status and admission gating; a later official XMCLib API is used only as continuity evidence."
)

replace_once(
    EVIDENCE,
    "| Retained data in self refresh remain ordinarily serviceable without exiting the mode | X | contradicted by input/CKE and exit semantics |",
    "| XMC EBU exposes separate self-refresh entry/exit request controls and read-only status fields | H/P | Infineon 2016 §14.12.18 and SDRMREF pp. 14-120–14-122 | direct controller-level primary evidence |\n| XMC EBU ties safe power-down to completed entry and SDRAM access to completed exit | H/P | Infineon 2016 printed p. 14-82 | direct for this controller contract; not a universal SDRAM rule |\n| Request, transition-completion evidence, and next-action admission are distinct relations | E | Micron 1999 + Infineon 2016 comparison | bounded engineering reconstruction; no direct genealogy |\n| Entry/exit status proves physical retention margin of every SDRAM cell | X | rejected | controller status is not direct cell-retention measurement |\n| Retained data in self refresh remain ordinarily serviceable without exiting the mode | X | contradicted by input/CKE and exit semantics |"
)

replace_once(
    EVIDENCE,
    "    !=\nexit/recovery timing violation\n    !=\nordinary-service unavailability while payload remains retained",
    "    !=\nself-refresh entry requested but not yet controller-qualified for power-down\n    !=\nexit requested but not yet controller-qualified for access\n    !=\nexit/recovery timing violation\n    !=\nordinary-service unavailability while payload remains retained"
)

replace_once(
    EVIDENCE,
    "- **mode-transition recovery timing can be constitutive infrastructure**.",
    "- **mode-transition recovery timing can be constitutive infrastructure**;\n- **self-refresh request ≠ controller-observed transition completion ≠ next-action admission**;\n- **small control/status state can gate the retention treatment of a much larger payload without being payload itself**."
)

replace_once(
    EVIDENCE,
    "- empirical failure behavior of named Micron parts.",
    "- empirical failure behavior of named Micron parts;\n- controller/device composition under aborted entry/exit, controller reset, and real power sequencing;\n- independent fault injection validating whether named systems actually honor entry/exit completion before power/access transitions."
)

# ---- README navigation ----------------------------------------------------
replace_prefix_line(
    README,
    "- [`cases/21-micron-sdram-refresh-mode-handoff.md`]",
    "- [`cases/21-micron-sdram-refresh-mode-handoff.md`](cases/21-micron-sdram-refresh-mode-handoff.md) — grounded SDRAM interface bridge: normal `AUTO REFRESH` uses externally repeated nonpersistent commands with internal refresh-row addressing, while CKE-controlled `SELF REFRESH` moves recurring clocking/refresh work inside the device until an explicit `tXSR` exit returns responsibility to the external cadence. A later 2016 Infineon XMC4700/XMC4800 EBU witness now separates entry/exit request from controller-observed completion and from safe power-down/access admission, without projecting the later controller semantics backward into Micron's 1999 device interface."
)

# ---- ROADMAP status/navigation -------------------------------------------
insert_before(
    ROADMAP,
    "Coordinate with `computing-archaeology` rather than duplicating it.",
    "- [x] SDRAM self-refresh transition-completion deepening — canonical [`cases/21-micron-sdram-refresh-mode-handoff.md`](cases/21-micron-sdram-refresh-mode-handoff.md), with [`evidence/21-micron-1999-sdram-refresh-mode-grounding.md`](evidence/21-micron-1999-sdram-refresh-mode-grounding.md), now adds a 2016 Infineon XMC4700/XMC4800 controller witness in which writable entry/exit requests, read-only transition status, safe power-down, post-exit delay, and access admission are distinct. This closes the bounded request→completion→admission decomposition while leaving normative JEDEC chronology, cross-controller behavior, and empirical power-sequencing fault validation open."
)

replace_prefix_line(
    ROADMAP,
    "- [ ] In refresh-driven memory, how should `retention deadline`",
    "- [x] In refresh-driven memory, separate `retention deadline`, `row enumeration`, `recurring command generation`, `self-refresh mode authority`, `transition-completion evidence`, `ordinary service availability`, and `exit/recovery timing` — closed at the bounded relation-decomposition level by [`cases/21-micron-sdram-refresh-mode-handoff.md`](cases/21-micron-sdram-refresh-mode-handoff.md), now deepened with a 2016 Infineon XMC4700/XMC4800 EBU request/status/admission witness. Normative JEDEC chronology, cross-controller composition, and empirical failed-entry/exit validation remain separate work."
)

replace_prefix_line(
    ROADMAP,
    "- [ ] missed externally issued refresh cadence, failed self-refresh entry",
    "- [ ] missed externally issued refresh cadence, failed self-refresh entry, loss of the powered self-refresh regime, or premature service resumption across a refresh-mode exit — **partially advanced by the Case 21 controller-transition deepening**: the 2016 Infineon EBU separates entry/exit request, controller-observed status, safe power-down, post-exit delay, and access admission. Actual payload-loss thresholds under aborted transitions, controller reset/power sequencing, empirical fault injection, and standards-wide semantics remain open;"
)

# ---- CASE_INDEX -----------------------------------------------------------
replace_prefix_line(
    INDEX,
    "| [Micron 64Mb SDRAM: AUTO REFRESH, SELF REFRESH, and Refresh-Responsibility Handoff]",
    "| [Micron 64Mb SDRAM: AUTO REFRESH, SELF REFRESH, and Refresh-Responsibility Handoff](cases/21-micron-sdram-refresh-mode-handoff.md) | **grounded** | volatile dynamic payload + internal refresh counter/controller + externally repeated nonpersistent AUTO REFRESH + CKE-controlled SELF REFRESH internal clocking + explicit tXSR exit + later controller request/status/admission state | separate refresh obligation, row enumeration, recurring-command authority, transition-completion evidence, retention-mode/power-down admission, ordinary service availability, and recovery timing | [1999 Micron + 2016 Infineon controller-transition grounding](evidence/21-micron-1999-sdram-refresh-mode-grounding.md); full JEDEC chronology, cross-controller fault behavior, per-bank/temperature-compensated/retention-aware refresh remain separate work |"
)

insert_after_prefix_line(
    INDEX,
    "**Grounded SDRAM refresh-mode bridge:**",
    "**Case 21 controller-transition deepening:** Infineon's 2016 XMC4700/XMC4800 EBU provides an independent later manufacturer-primary system witness in which `SELFREN`/`SELFREX` requests, `SELFRENST`/`SELFREXST` status, safe power-down, post-exit delay, and access admission are separately represented. This sharpens the 1999 Micron device-level handoff without claiming product pairing or genealogy: **mode request ≠ transition-completion evidence ≠ next-action admission**, and controller status remains distinct from direct measurement of DRAM-cell retention margin."
)

insert_after_prefix_line(
    INDEX,
    "1354. **informative retention extrapolation",
    r'''### Case 21 controller-transition deepening — self-refresh request, completion, and admission

1355. **self-refresh request ≠ controller-observed transition completion** — the XMC EBU exposes writable `SELFREN`/`SELFREX` command controls separately from read-only `SELFRENST`/`SELFREXST` status.
1356. **retention-mode request ≠ power-down admission** — the 2016 controller documentation makes completion of self-refresh entry the boundary after which surrounding power-down is treated as safe.
1357. **exit request ≠ ordinary-service readiness** — exit status plus post-exit refresh/NOP delay can remain outstanding before SDRAM access is permitted.
1358. **device timing contract ≠ controller completion/status policy** — Micron 1999 `tXSR` and Infineon 2016 request/status/delay machinery are comparable layers, not evidence of identical implementation or direct genealogy.
1359. **transition-completion evidence ≠ direct payload-retention measurement** — a controller status bit can qualify command sequencing without measuring the physical retention margin of every DRAM cell.
1360. **small transition/control state can gate retention treatment of a much larger payload** — a few controller fields can determine whether the system is allowed to power down or resume access even though those fields are not the SDRAM payload.
1361. **internal recurrence ≠ total system autonomy** — once self refresh is active the SDRAM can own recurring refresh work, while the external controller still owns surrounding entry/exit sequencing and power/access admission.
1362. **unfinished entry ≠ proven immediate payload loss** — proceeding before the documented transition completes violates the retention contract, but actual data loss remains contingent on power, refresh continuity, timing, and device behavior.
1363. **successful self-refresh entry ≠ nonvolatility** — controller-qualified entry establishes a powered maintenance regime; it does not establish retention after removal of the SDRAM's required supply.
1364. **later controller composition ≠ 1999 device history or JEDEC chronology** — Infineon 2016 is used as a later system witness and must not be projected backward as Micron's internal implementation, a direct product lineage, or normative SDRAM invention history.'''
)

# Integration helpers are intentionally one-shot.
for path in [
    ROOT / ".github/scripts/case21_controller_transition_integrate.py",
    ROOT / ".github/workflows/case21-controller-transition-integrate.yml",
]:
    if path.exists():
        path.unlink()
