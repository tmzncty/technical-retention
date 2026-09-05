from pathlib import Path


def insert_after_unique_line(path, predicate, new_lines, label):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if predicate(line)]
    if len(matches) != 1:
        raise RuntimeError(f"{label}: expected one anchor, found {len(matches)}")
    probe = next((x for x in new_lines if x.strip()), "")
    if probe and probe in text:
        return
    i = matches[0] + 1
    lines[i:i] = new_lines
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


readme_line = "- [`cases/86-dec-pdp8-core-power-fail-auto-restart.md`](cases/86-dec-pdp8-core-power-fail-auto-restart.md) — grounded magnetic-core/system-restart bridge: DEC's 1966 PDP-8 KR01 turns impending primary-power loss into a bounded 1 ms save interval in which software copies active register/program-count state into known core locations; restored power enters through address 0000 and reconstructs execution state while Power Clear separately resets internal/I/O control state; see [`evidence/86-dec-1960-1970-core-power-restart-grounding.md`](evidence/86-dec-1960-1970-core-power-restart-grounding.md)."
insert_after_unique_line(
    "README.md",
    lambda l: l.startswith("- [") and "cases/85-toshiba-nand-shift-read-retry-recoverability.md" in l,
    [readme_line],
    "README case85",
)

roadmap_line = "- [x] magnetic-core whole-system power-fail / restart boundary — [`cases/86-dec-pdp8-core-power-fail-auto-restart.md`](cases/86-dec-pdp8-core-power-fail-auto-restart.md), grounded by [`evidence/86-dec-1960-1970-core-power-restart-grounding.md`](evidence/86-dec-1960-1970-core-power-restart-grounding.md), answers Case 02's explicit limit that nonvolatile core does not imply automatic machine restart: DEC's 1966 KR01 gives a bounded 1 ms power-low interval for software to save active registers/program count into known core locations, later restarts through address `0000`, restores CPU context, and separately clears internal/I/O control state. IBM 7090 reset-vs-clear evidence is used only as earlier comparative prior art, not lineage; exact KR01 hold-up circuitry and a multi-vendor power-fail genealogy remain separate work for `computing-archaeology`."
insert_after_unique_line(
    "ROADMAP.md",
    lambda l: l.startswith("- [x]") and "NAND adaptive-read / retry-read retention bridge — Case 85" in l,
    [roadmap_line],
    "ROADMAP case85",
)

ledger_row = "| [DEC PDP-8 Automatic Restart: Core-Resident Power-Fail Save and Reconstructed Execution State](cases/86-dec-pdp8-core-power-fail-auto-restart.md) | **grounded** | nonvolatile core payload + volatile active CPU context + power-low interrupt + bounded save interval + core-resident restore entry + selective control/I/O reset | separate core-content survival from execution-state survival; failure detection from state capture; restart entry from restored computation; and CPU continuation from peripheral/external-world continuity | [1960–1970 DEC/IBM core-power-restart grounding](evidence/86-dec-1960-1970-core-power-restart-grounding.md); exact KR01 hold-up circuit, canonical software-library routine, peripheral-specific restart semantics, and broader vendor genealogy remain separate work |"
insert_after_unique_line(
    "CASE_INDEX.md",
    lambda l: l.startswith("| [") and "cases/85-toshiba-nand-shift-read-retry-recoverability.md" in l,
    [ledger_row],
    "CASE_INDEX ledger case85",
)

matrix_row = "| DEC PDP-8 KR01 power-fail restart / 1966 bounded system | ordinary core words + core-resident emergency copies of AC/L/MQ/program count + address-0000 recovery entry + volatile internal/I/O controls | power-low detection; interrupt; software save within ~1 ms; powered stop; ~200-ms post-stability restart delay; Power Clear; software context restore | core-resident saved words survive the interruption relation; active register state survives only after explicit copy into core | known core save locations plus address 0000 retain the recovery relation; processor/I/O control registers may be cleared | execution identity crosses a substrate/state-class migration and is reconstructed after restart; peripheral continuity remains separate | no complete event history; selected context is retained while other control state is deliberately reset |"
insert_after_unique_line(
    "CASE_INDEX.md",
    lambda l: l.startswith("| Toshiba NAND shift/read retry / 2000–2021 bounded chain |"),
    [matrix_row],
    "CASE_INDEX matrix case85",
)

findings = [
    "",
    "## Case 86 — PDP-8 core power-fail / restart findings",
    "",
    "1053. **core-content survival ≠ processor execution-state survival** — nonvolatile main-memory words can remain while AC/L/MQ/program-count state still requires explicit transfer into core before ordinary logic stops;",
    "1054. **core nonvolatility ≠ automatic program restart** — continuation additionally requires failure detection, a save path, a restart entry, context restoration, and an admissible post-power control state;",
    "1055. **power-fail detection ≠ state capture** — the `power low` flag identifies the interrupt cause, while software separately copies the active state needed for later continuation;",
    "1056. **remaining reliable-operation interval ≠ retained payload** — KR01's ~1 ms interval is temporal retention infrastructure that permits state transfer, not the state being preserved;",
    "1057. **register-to-core save ≠ ordinary core payload** — a failure transition can deliberately migrate short-lived working state into a stronger power-loss substrate;",
    "1058. **saved CPU context ≠ whole-system/peripheral state** — DEC separately clears internal controls and I/O device registers and warns that peripheral reset may still be needed;",
    "1059. **power-restoration detection ≠ resumed program** — suitable power only authorizes entry into a restore path; the saved context must still be reconstructed;",
    "1060. **restart at address 0000 ≠ complete restart state** — location 0000 is an entry relation into recovery, not a full image of the interrupted machine;",
    "1061. **Power Clear / logical reset ≠ core-data erase** — DEC's restart can clear internal/I/O controls while preserving the core-resident recovery state; IBM's earlier Reset-vs-Clear control distinction independently bounds the same state-class separation;",
    "1062. **automatic-restart option ≠ guaranteed arbitrary-failure recovery** — the documented path depends on the finite save interval, valid software, surviving core state, and a power transition inside the option's operating assumptions;",
    "1063. **manual restart policy ≠ underlying core survivability** — disabling automatic restart changes restart authority, not magnetic remanence itself;",
    "1064. **200-ms restart delay ≠ retention lifetime** — DEC uses the delay to let slow mechanical devices settle after power becomes satisfactory, not as a claim about how long core retains data;",
    "1065. **core-resident emergency save ≠ SSD power-loss-protection genealogy** — Cases 15/32/38 are useful functional comparisons only; KR01's historical mechanism is CPU-context save to core, not later flash-cache/ADR terminology;",
    "1066. **IBM Reset-vs-Clear distinction ≠ evidence of DEC derivation** — the 7090 manual is earlier comparative prior art for separate control/core forgetting authority, not a lineage claim;",
    "1067. **PDP-8 KR01 continuity ≠ all core-memory systems** — the bounded case establishes one documented DEC restart regime and later PDP-8-family witnesses, not a universal property of core-memory computers;",
    "1068. **retention can require state-class migration before interruption** — selected working state may survive a power boundary only because the system moves it into a more durable embodiment and later reconstructs the working relation;",
]
insert_after_unique_line(
    "CASE_INDEX.md",
    lambda l: l.startswith("1052. **chronological prior art ≠ demonstrated genealogy**"),
    findings,
    "CASE_INDEX finding 1052",
)

p = Path("CASE_INDEX.md")
text = p.read_text(encoding="utf-8")
replacements = {
    "After eighty-six bounded cases, **all eighty-six cases are now `grounded`.**": "After eighty-seven bounded cases, **all eighty-seven cases are now `grounded`.**",
    "currently eighty-six (Cases 00–85)": "currently eighty-seven (Cases 00–86)",
}
for old, new in replacements.items():
    if new in text:
        continue
    if text.count(old) != 1:
        raise RuntimeError(f"CASE_INDEX aggregate update expected one occurrence of {old!r}, found {text.count(old)}")
    text = text.replace(old, new, 1)
p.write_text(text, encoding="utf-8")

checks = {
    "README.md": ["cases/86-dec-pdp8-core-power-fail-auto-restart.md", "evidence/86-dec-1960-1970-core-power-restart-grounding.md"],
    "ROADMAP.md": ["cases/86-dec-pdp8-core-power-fail-auto-restart.md", "evidence/86-dec-1960-1970-core-power-restart-grounding.md"],
    "CASE_INDEX.md": [
        "cases/86-dec-pdp8-core-power-fail-auto-restart.md",
        "| DEC PDP-8 KR01 power-fail restart / 1966 bounded system |",
        "## Case 86 — PDP-8 core power-fail / restart findings",
        "1053. **core-content survival ≠ processor execution-state survival**",
        "1068. **retention can require state-class migration before interruption**",
        "currently eighty-seven (Cases 00–86)",
        "After eighty-seven bounded cases, **all eighty-seven cases are now `grounded`.**",
    ],
}
for path, needles in checks.items():
    data = Path(path).read_text(encoding="utf-8")
    for needle in needles:
        if needle not in data:
            raise RuntimeError(f"missing {needle!r} in {path}")

for required in [
    Path("cases/86-dec-pdp8-core-power-fail-auto-restart.md"),
    Path("evidence/86-dec-1960-1970-core-power-restart-grounding.md"),
]:
    if not required.exists():
        raise RuntimeError(f"missing required research file: {required}")
