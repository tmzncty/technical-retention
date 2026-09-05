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


readme_line = "- [`cases/87-scsi2-writeback-cache-fua-synchronize-cache.md`](cases/87-scsi2-writeback-cache-fua-synchronize-cache.md) — grounded storage-interface prior-art bridge: ANSI SCSI-2 write-back caching lets a command complete before the physical medium is current, while FUA and SYNCHRONIZE CACHE establish stronger media-access relations; 2004 SBC-2 work then separates volatile cache, finite-retention non-volatile cache, and physical medium, making short power-cycle survival distinct from controller/media independence; see [`evidence/87-scsi-1994-2004-cache-durability-grounding.md`](evidence/87-scsi-1994-2004-cache-durability-grounding.md)."
insert_after_unique_line(
    "README.md",
    lambda l: l.startswith("- [") and "cases/86-dec-pdp8-core-power-fail-auto-restart.md" in l,
    [readme_line],
    "README case86",
)

roadmap_line = "- [x] SCSI-2 write-back-cache / FUA / SYNCHRONIZE CACHE durability prior-art bridge — [`cases/87-scsi2-writeback-cache-fua-synchronize-cache.md`](cases/87-scsi2-writeback-cache-fua-synchronize-cache.md), grounded by [`evidence/87-scsi-1994-2004-cache-durability-grounding.md`](evidence/87-scsi-1994-2004-cache-durability-grounding.md), separates ordinary GOOD/command completion, newest-value cache residence, forced physical-medium access, explicit cache synchronization, deferred media-write error, and the later volatile-cache/non-volatile-cache/medium distinction. The 2004 SBC-2 chain further shows that short power-cycle survival can be weaker than controller-independent/removable-media completeness. This is earlier interface prior art for Case 20's NVMe comparison, not a claimed direct SCSI→NVMe genealogy; the broader SCSI/controller history remains routed to `computing-archaeology`."
insert_after_unique_line(
    "ROADMAP.md",
    lambda l: l.startswith("- [x]") and "magnetic-core whole-system power-fail / restart boundary" in l,
    [roadmap_line],
    "ROADMAP case86",
)

ledger_row = "| [SCSI-2 Write-Back Cache, FUA, and SYNCHRONIZE CACHE: Completion Before Medium and Typed Durability](cases/87-scsi2-writeback-cache-fua-synchronize-cache.md) | **grounded** | host-visible logical block + volatile/non-volatile device/controller cache + physical medium + FUA/synchronization control + deferred-error state | separate command completion from media commitment; newest cache value from medium currentness; per-command forced access from cache synchronization; power-cycle survival from controller/media independence; and interface contract from implementation mechanism | [1994–2004 SCSI cache-durability grounding](evidence/87-scsi-1994-2004-cache-durability-grounding.md); pre-SCSI-2 cache-control genealogy, exact later SBC-3 change history, controller-specific NV-cache fault validation, ordering semantics, and full SCSI→SAS/NVMe lineage remain separate work |"
insert_after_unique_line(
    "CASE_INDEX.md",
    lambda l: l.startswith("| [") and "cases/86-dec-pdp8-core-power-fail-auto-restart.md" in l,
    [ledger_row],
    "CASE_INDEX ledger case86",
)

matrix_row = "| SCSI-2 / SBC-2 cache durability / 1994–2004 bounded chain | newest logical-block value + volatile or non-volatile cache copy + physical-medium representation + deferred-error/control state | write-back scheduling; per-command FUA; explicit SYNCHRONIZE CACHE; later FUA_NV/SYNC_NV transitions where supported | ordinary cached write may complete before medium write; FUA write reaches medium before completion; synchronization propagates pending newer cached values without requiring cache eviction | initiator LBA/range + command-scoped FUA or synchronization scope; cache cells and physical sectors remain behind the device interface | logical-block identity stays stable while the newest embodiment can temporarily live in cache; non-volatile controller cache can survive power cycles yet remain weaker than a medium that must travel independently | no complete operation history; deferred-error state can outlive the causing command, while cache/medium currentness tracks only the relations needed for service and later propagation |"
insert_after_unique_line(
    "CASE_INDEX.md",
    lambda l: l.startswith("| DEC PDP-8 KR01 power-fail restart / 1966 bounded system |"),
    [matrix_row],
    "CASE_INDEX matrix case86",
)

findings = [
    "",
    "## Case 87 — SCSI cache completion / media-commit findings",
    "",
    "1069. **command completion / `GOOD` ≠ physical-medium residency** — SCSI-2 write-back caching explicitly permits a write command to complete while the newest logical-block value still awaits its medium write;",
    "1070. **cache currentness ≠ medium currentness** — during that interval the cache can hold the newest value while the physical medium still embodies an older value;",
    "1071. **per-command FUA ≠ generic cache synchronization** — `FUA=1` strengthens the addressed write so its data reach physical medium before command completion, while `SYNCHRONIZE CACHE` acts on pending cached state over a requested range;",
    "1072. **SYNCHRONIZE CACHE ≠ ordinary payload write** — it is a control over already-pending current cache state rather than another independent user-data value;",
    "1073. **synchronization to medium ≠ compulsory cache eviction** — later SBC-2 text permits synchronized logical blocks to remain cached after the lower layer has become current;",
    "1074. **later media-write failure ≠ necessarily immediate failure of the causing command** — write-back caching can return `GOOD` first and report a subsequent write failure as a deferred error on a later command;",
    "1075. **deferred-error state ≠ user payload** — the system may need to retain/report failure evidence after the operation that supplied the data has already crossed its ordinary completion boundary;",
    "1076. **volatile cache ≠ non-volatile cache ≠ physical medium** — the 2004 SBC-2 chain explicitly separates all three as different locations/retention classes for current logical-block state;",
    "1077. **power-cycle survival ≠ controller-independent media completeness** — battery-backed/non-volatile controller cache can be sufficient for short interruption while still being insufficient when disks are moved to another controller or removable media are detached;",
    "1078. **non-volatile cache ≠ indefinite retention** — SBC-2 Revision 16 explicitly allows a finite no-power retention time for non-volatile cache;",
    "1079. **short power loss ≠ extended shutdown ≠ medium removal as one failure model** — the T10 proposal names these transitions separately because they can require different retention destinations;",
    "1080. **SCSI-2 FUA/SYNCHRONIZE CACHE ≠ retroactive FUA_NV/SYNC_NV vocabulary** — the 1994 standard grounds the former, while the non-volatile-cache-specific bits belong to the later 2004 SBC-2 standards chain;",
    "1081. **interface durability class ≠ one physical protection mechanism** — T10's battery-backed RAID example motivates the distinction but does not prove every qualifying cache uses a battery or any one implementation technology;",
    "1082. **SCSI-2 cache controls ≠ invention-priority proof for write-back/stable storage** — the bounded case establishes a period interface contract, not the first invention of caching, forced write, flushing, or stable storage;",
    "1083. **SCSI prior art ≠ demonstrated SCSI→NVMe genealogy** — Case 87 supplies an earlier functional/interface comparison for Case 20, while direct design lineage requires separate historical evidence;",
    "1084. **the required retention boundary depends on the transition to be survived** — one current value can be adequate for ordinary service in cache, adequate for a short power cycle in non-volatile cache, yet still inadequate for controller separation until the physical medium itself is current;",
]
insert_after_unique_line(
    "CASE_INDEX.md",
    lambda l: l.startswith("1068. **retention can require state-class migration before interruption**"),
    findings,
    "CASE_INDEX finding 1068",
)

p = Path("CASE_INDEX.md")
text = p.read_text(encoding="utf-8")
replacements = {
    "After eighty-seven bounded cases, **all eighty-seven cases are now `grounded`.**": "After eighty-eight bounded cases, **all eighty-eight cases are now `grounded`.**",
    "currently eighty-seven (Cases 00–86)": "currently eighty-eight (Cases 00–87)",
}
for old, new in replacements.items():
    if new in text:
        continue
    if text.count(old) != 1:
        raise RuntimeError(f"CASE_INDEX aggregate update expected one occurrence of {old!r}, found {text.count(old)}")
    text = text.replace(old, new, 1)
p.write_text(text, encoding="utf-8")

checks = {
    "README.md": ["cases/87-scsi2-writeback-cache-fua-synchronize-cache.md", "evidence/87-scsi-1994-2004-cache-durability-grounding.md"],
    "ROADMAP.md": ["cases/87-scsi2-writeback-cache-fua-synchronize-cache.md", "evidence/87-scsi-1994-2004-cache-durability-grounding.md"],
    "CASE_INDEX.md": [
        "cases/87-scsi2-writeback-cache-fua-synchronize-cache.md",
        "| SCSI-2 / SBC-2 cache durability / 1994–2004 bounded chain |",
        "## Case 87 — SCSI cache completion / media-commit findings",
        "1069. **command completion / `GOOD` ≠ physical-medium residency**",
        "1084. **the required retention boundary depends on the transition to be survived**",
        "currently eighty-eight (Cases 00–87)",
        "After eighty-eight bounded cases, **all eighty-eight cases are now `grounded`.**",
    ],
}
for path, needles in checks.items():
    data = Path(path).read_text(encoding="utf-8")
    for needle in needles:
        if needle not in data:
            raise RuntimeError(f"missing {needle!r} in {path}")

for required in [
    Path("cases/87-scsi2-writeback-cache-fua-synchronize-cache.md"),
    Path("evidence/87-scsi-1994-2004-cache-durability-grounding.md"),
]:
    if not required.exists():
        raise RuntimeError(f"missing required research file: {required}")
