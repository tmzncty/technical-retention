from pathlib import Path

CASE = "cases/84-nvme-zns-zone-reset-logical-reuse.md"
EVID = "evidence/84-nvme-2020-2021-zns-zone-reset-grounding.md"


def insert_after_line(text: str, predicate, new_line: str, label: str) -> str:
    if new_line in text:
        return text
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if predicate(line):
            lines.insert(i + 1, new_line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    raise RuntimeError(f"anchor not found: {label}")


# README repository map.
p = Path("README.md")
text = p.read_text()
readme_line = (
    "- [`cases/84-nvme-zns-zone-reset-logical-reuse.md`]"
    "(cases/84-nvme-zns-zone-reset-logical-reuse.md) — grounded NVMe ZNS reuse/frontier bridge: "
    "a per-zone write pointer retains the next sequential-write frontier; successful Reset Zone returns an eligible zone to `ZSE:Empty`, "
    "returns the pointer to `ZSLBA`, and leaves the zone's logical blocks deallocated for a new write cycle without thereby proving secure media sanitization; "
    "see [`evidence/84-nvme-2020-2021-zns-zone-reset-grounding.md`](evidence/84-nvme-2020-2021-zns-zone-reset-grounding.md)."
)
text = insert_after_line(
    text,
    lambda line: line.startswith("- [") and "cases/83-apache-hdfs-block-scanner-checksum-verification.md" in line,
    readme_line,
    "README Case 83 repository-map line",
)
p.write_text(text)


# ROADMAP bounded bridge.
p = Path("ROADMAP.md")
text = p.read_text()
roadmap_line = (
    "- [x] NVMe Zoned Namespace write-pointer / Reset Zone reuse boundary — "
    "[`cases/84-nvme-zns-zone-reset-logical-reuse.md`](cases/84-nvme-zns-zone-reset-logical-reuse.md), "
    "grounded by [`evidence/84-nvme-2020-2021-zns-zone-reset-grounding.md`](evidence/84-nvme-2020-2021-zns-zone-reset-grounding.md), "
    "adds a host-visible zoned-storage regime in which a retained per-zone write pointer summarizes the next admissible sequential-write frontier without preserving complete write history; "
    "Reset Zone returns an eligible zone to `ZSE:Empty`, rewinds the pointer to `ZSLBA`, and marks its logical blocks deallocated for reuse, while NVMe Sanitize remains a separate stronger forgetting operation. "
    "This is distinct from early Flash physical erase geometry (Case 13), mapped-Flash remapping/reclamation (Case 04), NVMe Deallocate/Sanitize (Case 44), and NAND COPYBACK (Case 82); full SMR/ZBC/ZAC→ZNS genealogy and named-device raw-media/fault validation remain separate work."
)
text = insert_after_line(
    text,
    lambda line: line.startswith("- [x]") and "cases/83-apache-hdfs-block-scanner-checksum-verification.md" in line,
    roadmap_line,
    "ROADMAP Case 83 bridge line",
)
p.write_text(text)


# CASE_INDEX main ledger row.
p = Path("CASE_INDEX.md")
text = p.read_text()
ledger_row = (
    "| [NVMe Zoned Namespace Zone Reset: Retained Write Frontiers, Logical Deallocation, and Reuse Without Sanitization]"
    "(cases/84-nvme-zns-zone-reset-logical-reuse.md) | **grounded** | "
    "zoned LBA range + per-zone state + retained Write Pointer + explicit Reset Zone + Empty/deallocated logical blocks + separate Sanitize operation | "
    "separate current write frontier from complete history; reset/reuse authority from payload restoration; logical deallocation from physical blankness and secure sanitization; controller reset recommendation from host deletion authority | "
    "[2020–2021 NVM Express/USENIX grounding](evidence/84-nvme-2020-2021-zns-zone-reset-grounding.md); ZNS 1.0 archival wording, full ZBC/ZAC genealogy, zone-metadata power-loss behavior, and named-device physical/forensic validation remain separate work |"
)
text = insert_after_line(
    text,
    lambda line: line.startswith("| [") and "cases/83-apache-hdfs-block-scanner-checksum-verification.md" in line,
    ledger_row,
    "CASE_INDEX Case 83 ledger row",
)


# Comparison matrix row.
matrix_row = (
    "| NVMe ZNS Reset Zone / 2020–2021 bounded regime | "
    "user payload + zone state + per-zone Write Pointer + zone-management attributes + logical allocation/deallocation state | "
    "sequential writes advance current frontier; Zone Management Receive re-observes it; Reset Zone returns eligible zone to Empty, rewinds pointer to ZSLBA, clears bounded management attributes, and enables a new write cycle | "
    "random reads may remain addressable while ordinary writes are constrained by the sequential frontier; reset withdraws prior logical allocation rather than reading/restoring old payload | "
    "namespace LBA -> zone -> current Zone Descriptor/state + Write Pointer; physical NAND mapping remains controller-internal unless separately evidenced | "
    "logical zone identity persists across reuse cycles while prior logical allocation/currentness is discarded; physical trace disappearance is not proven by Reset Zone and Sanitize remains separate | "
    "current frontier/state is retained control information rather than complete event history; resetting it forgets the prior admissibility frontier so future writes can begin again from the zone start |"
)
text = insert_after_line(
    text,
    lambda line: line.startswith("| HDFS DataNode BlockScanner / 2008–2016 bounded regime |"),
    matrix_row,
    "CASE_INDEX Case 83 comparison row",
)


# Findings 1021–1036.
findings = """
## Case 84 — NVMe ZNS Zone Reset findings

1021. **zone write pointer ≠ payload** — the per-zone pointer is control/admissibility state identifying the next sequential-write position, not the user data being retained;
1022. **write-pointer frontier ≠ complete write history** — a current pointer summarizes where writing may continue without retaining every command or physical program event that produced that frontier;
1023. **random-read permission ≠ random-write permission** — ZNS can leave a zone randomly readable while constraining ordinary writes to the current sequential frontier;
1024. **Reset Zone ≠ ordinary overwrite** — reset changes zone-control/allocation state and reopens the writing cycle rather than merely replacing one logical block's value;
1025. **write-pointer reset ≠ physical-time rewind** — returning the pointer to `ZSLBA` changes present write admissibility without undoing the historical media operations of the previous cycle;
1026. **`ZSE:Empty` ≠ physical blankness proof** — Empty establishes the specified zone/allocation state; it does not certify that every hidden physical trace has disappeared;
1027. **logical deallocation ≠ secure sanitization** — Empty marks the zone's logical blocks deallocated, while NVMe Sanitize remains a distinct stronger operation already separated in Case 44;
1028. **zone reuse authority ≠ payload restoration** — Reset Zone authorizes a new sequential write cycle from the zone start; it does not recreate the old payload;
1029. **zone state ≠ allocation state ≠ write-pointer state** — these control dimensions are related and may change coherently on reset, but they answer different questions about status, current data, and next-write position;
1030. **Reset Zone ≠ pointer update alone** — the bounded specification also changes zone state and clears descriptor/recommendation attributes, so reset is a broader control transition;
1031. **Reset Zone Recommended ≠ mandatory reset** — the controller may recommend reset before internal work while the host can decline because reset discards host-visible zone contents;
1032. **controller reset recommendation ≠ sanitization request** — the recommendation coordinates maintenance/performance and host data authority, not a secure-erasure contract;
1033. **host-visible write/erase geometry ≠ complete physical implementation exposure** — ZNS exposes zone boundaries and sequential-write constraints without proving a one-to-one synchronous mapping from Reset Zone to raw NAND erase;
1034. **host placement responsibility ≠ ownership of all media reliability** — contemporary ZNS literature shifts placement/order responsibility toward software while leaving media reliability duties inside the SSD;
1035. **ZNS ≠ invention of zoned storage** — contemporary NVM Express and USENIX sources place ZNS after the SMR/ZBC/ZAC zoned-storage model and alongside earlier distinct host/device-cooperation strategies;
1036. **logical forgetting can enable future write admissibility** — Reset Zone withdraws the previous logical allocation/frontier precisely so the same zone address range can enter a new controlled write cycle.
"""
if "## Case 84 — NVMe ZNS Zone Reset findings" not in text:
    anchor = "1020. **HDFS does not establish invention priority for proactive distributed integrity scanning**"
    lines = text.splitlines()
    idx = next((i for i, line in enumerate(lines) if line.startswith(anchor)), None)
    if idx is None:
        raise RuntimeError("CASE_INDEX finding 1020 anchor not found")
    lines.insert(idx + 1, findings.rstrip("\n"))
    text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")

p.write_text(text)


# Integration/idempotency checks.
readme = Path("README.md").read_text()
roadmap = Path("ROADMAP.md").read_text()
index = Path("CASE_INDEX.md").read_text()
for name, doc in [("README", readme), ("ROADMAP", roadmap), ("CASE_INDEX", index)]:
    if CASE not in doc:
        raise RuntimeError(f"{name} missing Case 84 path")
if EVID not in readme or EVID not in roadmap or EVID not in index:
    raise RuntimeError("Case 84 grounding path not fully integrated")
if index.count(CASE) != 1:
    raise RuntimeError(f"expected one Case 84 ledger link in CASE_INDEX, got {index.count(CASE)}")
for n in range(1021, 1037):
    if index.count(f"{n}. **") != 1:
        raise RuntimeError(f"finding {n} missing or duplicated")
if index.count("| NVMe ZNS Reset Zone / 2020–2021 bounded regime |") != 1:
    raise RuntimeError("Case 84 comparison-matrix row missing or duplicated")
print("case84 integration checks passed")
