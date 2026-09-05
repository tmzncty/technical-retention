from pathlib import Path


def insert_after_unique_line(path, predicate, new_lines, label):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if predicate(line)]
    if len(matches) != 1:
        raise RuntimeError(f"{label}: expected one anchor, found {len(matches)}")
    # Idempotency: if the first inserted substantive line already exists, do nothing.
    probe = next((x for x in new_lines if x.strip()), "")
    if probe and probe in text:
        return
    i = matches[0] + 1
    lines[i:i] = new_lines
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


readme_line = "- [`cases/85-toshiba-nand-shift-read-retry-recoverability.md`](cases/85-toshiba-nand-shift-read-retry-recoverability.md) — grounded NAND read-decision bridge: Toshiba's 2009-priority family separates default/+/- shift read, ECC retry, retained read-condition state, and later refresh/copy, showing that default-read failure can be recoverable without immediate rewrite; earlier 2000-priority adaptive-reference prior art blocks invention priority, and ASPLOS 2021 real-chip data provides an independent modern witness; see [`evidence/85-flash-2000-2021-read-threshold-retry-grounding.md`](evidence/85-flash-2000-2021-read-threshold-retry-grounding.md)."
insert_after_unique_line(
    "README.md",
    lambda l: "cases/84-nvme-zns-zone-reset-logical-reuse.md" in l,
    [readme_line],
    "README case84",
)

roadmap_line = "- [x] NAND adaptive-read / retry-read retention bridge — Case 85 grounds Toshiba's 2009-priority `default read` / `+ shift read` / `- shift read` / `retry read` flow against earlier MLC adaptive-reference prior art and 2021 real-chip characterization, separating physical threshold state, reader decision boundaries, ECC recoverability, retained read-condition metadata, and later physical refresh/copy; keeps full vendor-command / soft-decision / LDPC genealogy open for `computing-archaeology` ([case](cases/85-toshiba-nand-shift-read-retry-recoverability.md), [grounding](evidence/85-flash-2000-2021-read-threshold-retry-grounding.md))."
insert_after_unique_line(
    "ROADMAP.md",
    lambda l: "cases/84-nvme-zns-zone-reset-logical-reuse.md" in l,
    [roadmap_line],
    "ROADMAP case84",
)

ledger_row = "| [Toshiba NAND Shift Read / Retry Read: Mutable Read Thresholds, Recoverability Without Immediate Rewrite](cases/85-toshiba-nand-shift-read-retry-recoverability.md) | **grounded** | NAND threshold-voltage state + ECC redundancy + mutable read/reference levels + retained condition/read-history metadata + separate later refresh/copy | separate physical cell state from read-decision boundary; first-read failure from data absence; reader-side recovery from representation renewal; and current correctability from restored future margin | [2000–2021 adaptive-reference/read-retry grounding](evidence/85-flash-2000-2021-read-threshold-retry-grounding.md); exact first-use vocabulary, proprietary vendor command tables, soft-decision/LDPC genealogy, named-product firmware behavior, and cross-vendor fault validation remain separate work |"
insert_after_unique_line(
    "CASE_INDEX.md",
    lambda l: l.startswith("| [") and "cases/84-nvme-zns-zone-reset-logical-reuse.md" in l,
    [ledger_row],
    "CASE_INDEX ledger case84",
)

matrix_row = "| Toshiba NAND shift/read retry / 2000–2021 bounded chain | threshold-voltage distributions + ECC redundancy + mutable read/reference levels + condition/history metadata | default read; ECC evaluation; +/− shift / retry reads; optional later refresh/copy when error margin is high | same page can be reread under changed decision thresholds; logical correction may succeed without NAND rewrite | physical page/block address remains unchanged during retry; management tables can select read-condition state | location can remain fixed while interpretation boundary changes; later refresh/copy may create a new embodiment | no complete history; bounded condition/successful-read metadata can preserve future interpretability but may become stale |"
insert_after_unique_line(
    "CASE_INDEX.md",
    lambda l: l.startswith("| NVMe ZNS Reset Zone / 2020–2021 bounded regime |"),
    [matrix_row],
    "CASE_INDEX matrix case84",
)

findings = [
    "",
    "## Case 85 — NAND shifted-read / retry-read findings",
    "",
    "1037. **physical threshold state ≠ read-decision boundary** — NAND cell distributions and the read/reference voltages used to classify them are distinct state classes;",
    "1038. **default-read ECC failure ≠ physical data absence** — an uncorrectable first read can become correctable when the same cells are reread with shifted levels;",
    "1039. **retry read ≠ rewrite** — changing read levels changes sensing/interpretation without necessarily reprogramming the target cells;",
    "1040. **successful retry read ≠ refreshed physical representation** — Toshiba separates shifted rereading from a later refresh operation that copies data to a fresh erased block;",
    "1041. **ECC recovery ≠ zero raw errors** — retry succeeds when errors fall inside correction capability, not necessarily when the sensed codeword is intrinsically error-free;",
    "1042. **correctable now ≠ restored future retention margin** — the source can still trigger refresh when error count is high even though ECC succeeds;",
    "1043. **PD/RD compensation direction ≠ DR compensation direction** — Toshiba's bounded embodiment shifts read levels in opposite directions for different threshold-distribution movement classes rather than defining one universal retry direction;",
    "1044. **read-condition metadata ≠ user payload** — standing time, counters, temperature, and successful read settings can be retained control state needed for future interpretability;",
    "1045. **successful-read setting ≠ permanently valid setting** — physical distributions continue to evolve, so interpretation metadata can itself become stale;",
    "1046. **recoverability is relational across substrate, sensing, ECC, and policy** — operational availability is not determined by cell charge alone;",
    "1047. **reader-side recovery ≠ representation renewal** — Case 85 recovers access by changing interpretation, while Case 36 renews data through correction plus rewrite/refresh;",
    "1048. **read-side requalification ≠ reclaim/relocation** — Cases 67 and 82 change placement/embodiment relations that Case 85 can leave untouched;",
    "1049. **COPYBACK relocation ≠ read-retry requalification** — Case 82 can move data without automatic integrity renewal; Case 85 can improve recoverability without moving the page;",
    "1050. **disturb mechanism ≠ retry mechanism** — Cases 52 and 59 explain physical drift, while Case 85 explains one reader-side response to drift;",
    "1051. **Toshiba 2009-priority family ≠ origin of adaptive reference rereading** — a 2000-priority MLC Flash patent family already describes ECC-triggered reference-voltage adjustment and rereading;",
    "1052. **chronological prior art ≠ demonstrated genealogy** — the earlier MLC Flash family blocks a first-invention claim but does not prove lineage into Toshiba's design;",
]
insert_after_unique_line(
    "CASE_INDEX.md",
    lambda l: l.startswith("1036. **logical forgetting can enable future write admissibility**"),
    findings,
    "CASE_INDEX finding 1036",
)

p = Path("CASE_INDEX.md")
text = p.read_text(encoding="utf-8")
replacements = {
    "After eighty-three bounded cases, **all eighty-three cases are now `grounded`.**": "After eighty-six bounded cases, **all eighty-six cases are now `grounded`.**",
    "currently eighty-five (Cases 00–84)": "currently eighty-six (Cases 00–85)",
}
for old, new in replacements.items():
    if new in text:
        continue
    if text.count(old) != 1:
        raise RuntimeError(f"CASE_INDEX aggregate update expected one occurrence of {old!r}, found {text.count(old)}")
    text = text.replace(old, new, 1)
p.write_text(text, encoding="utf-8")

# Final structural checks.
checks = {
    "README.md": ["cases/85-toshiba-nand-shift-read-retry-recoverability.md", "evidence/85-flash-2000-2021-read-threshold-retry-grounding.md"],
    "ROADMAP.md": ["cases/85-toshiba-nand-shift-read-retry-recoverability.md", "evidence/85-flash-2000-2021-read-threshold-retry-grounding.md"],
    "CASE_INDEX.md": ["cases/85-toshiba-nand-shift-read-retry-recoverability.md", "| Toshiba NAND shift/read retry / 2000–2021 bounded chain |", "## Case 85 — NAND shifted-read / retry-read findings", "1037. **physical threshold state ≠ read-decision boundary**", "1052. **chronological prior art ≠ demonstrated genealogy**", "currently eighty-six (Cases 00–85)", "After eighty-six bounded cases, **all eighty-six cases are now `grounded`.**"],
}
for path, needles in checks.items():
    data = Path(path).read_text(encoding="utf-8")
    for needle in needles:
        if needle not in data:
            raise RuntimeError(f"missing {needle!r} in {path}")

for required in [
    Path("cases/85-toshiba-nand-shift-read-retry-recoverability.md"),
    Path("evidence/85-flash-2000-2021-read-threshold-retry-grounding.md"),
]:
    if not required.exists():
        raise RuntimeError(f"missing required research file: {required}")
