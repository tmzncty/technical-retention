from pathlib import Path


def insert_after_line(path, needle, new_line, marker):
    p = Path(path)
    text = p.read_text()
    if marker in text:
        return
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if needle in line:
            lines.insert(i + 1, new_line)
            p.write_text("\n".join(lines) + "\n")
            return
    raise SystemExit(f"missing insertion anchor in {path}: {needle}")


def replace_once_if_present(path, old, new):
    p = Path(path)
    text = p.read_text()
    if old in text:
        p.write_text(text.replace(old, new, 1))
        return True
    return False


case_path = "cases/96-openzfs-draid-distributed-spare-sequential-resilver.md"
evidence_path = "evidence/96-openzfs-1992-2021-draid-recovery-grounding.md"

readme_line = (
    "- [`cases/96-openzfs-draid-distributed-spare-sequential-resilver.md`](cases/96-openzfs-draid-distributed-spare-sequential-resilver.md) — "
    "grounded OpenZFS dRAID recovery bridge: 2017–2021 project records and released 2.1.0 source show fixed-width declustered groups, deterministic permutation mapping, distributed spare capacity, and sequential reconstruction using many children to shorten the degraded redundancy-restoration interval; the first phase restores coded redundancy without block-checksum verification, so a later scrub supplies a distinct integrity-validation relation; earlier CMU parity-declustering/distributed-sparing work is retained as prior art; see [`evidence/96-openzfs-1992-2021-draid-recovery-grounding.md`](evidence/96-openzfs-1992-2021-draid-recovery-grounding.md)."
)
insert_after_line(
    "README.md",
    "cases/95-zfs-raidz-dynamic-stripe-write-hole.md",
    readme_line,
    case_path,
)

roadmap_line = (
    "- [x] OpenZFS dRAID distributed-spare / sequential-resilver recovery window — "
    "[`cases/96-openzfs-draid-distributed-spare-sequential-resilver.md`](cases/96-openzfs-draid-distributed-spare-sequential-resilver.md), grounded by "
    "[`evidence/96-openzfs-1992-2021-draid-recovery-grounding.md`](evidence/96-openzfs-1992-2021-draid-recovery-grounding.md), adds the 2017–2021 dRAID-specific retention relation: fixed-width declustered redundancy groups and deterministic permutation mappings distribute both recovery reads and spare writes across many children, while sequential device reconstruction restores redundancy before a separate checksum-verification scrub. This separates parity count from redundancy-restoration time, dedicated-spare capacity from distributed transition bandwidth, and fast reconstruction from checksum-qualified repair. Holland/Gibson parity declustering (1992) and Holland distributed sparing (1994) remain explicit prior art, so the case makes no invention claim. Broader ZFS/RAID controller genealogy, dRAID failure-domain extensions, URE-aware probabilistic rebuild policy, and field fault injection remain open."
)
insert_after_line(
    "ROADMAP.md",
    "cases/95-zfs-raidz-dynamic-stripe-write-hole.md",
    roadmap_line,
    case_path,
)

# Narrow stale-open wording left by Case 95: the bounded dRAID recovery slice is now closed,
# while later failure-domain and broader genealogy work remains open.
replace_once_if_present(
    "ROADMAP.md",
    "Broad ZFS/WAFL/COW/parity genealogy, RAID-Z2/3/dRAID, ZIL/SLOG, modern expansion, and fault injection remain separate work for `computing-archaeology` or later bounded cases.",
    "Broad ZFS/WAFL/COW/parity genealogy, RAID-Z2/3, dRAID failure-domain extensions, ZIL/SLOG, modern expansion, and fault injection remain separate work for `computing-archaeology` or later bounded cases.",
)

case_row = (
    "| [OpenZFS dRAID: Distributed Spare Capacity, Sequential Resilver, and the Duration of Reduced Redundancy](cases/96-openzfs-draid-distributed-spare-sequential-resilver.md) | **grounded** | "
    "fixed-width declustered RAID-Z groups + deterministic permutation mapping + distributed spare capacity + sequential rebuild state + later checksum scrub | "
    "separate parity count from degraded-window duration; distinguish dedicated spare capacity from distributed repair bandwidth, redundancy restoration from checksum revalidation, and stable mapping compatibility from user payload | "
    "[1992–2021 dRAID/recovery grounding](evidence/96-openzfs-1992-2021-draid-recovery-grounding.md); broader parity-declustering/distributed-sparing genealogy, RAID controller history, dRAID failure-domain extensions, URE-aware probabilistic modeling, and named-system fault injection remain separate work |"
)
insert_after_line(
    "CASE_INDEX.md",
    "cases/95-zfs-raidz-dynamic-stripe-write-hole.md",
    case_row,
    case_path,
)

matrix_row = (
    "| OpenZFS dRAID / 2017–2021 bounded recovery regime | surviving data/parity + fixed-width redundancy-group geometry + deterministic permutation mapping + distributed spare regions + space-map/rebuild progress + later block-pointer/checksum authority | "
    "after device loss, reconstruct allocated ranges sequentially in LBA order across many children into distributed spare capacity; restore coded redundancy first; run later scrub/healing verification | "
    "sequential reconstruction reads surviving coded contributions without per-block checksum verification in the first phase; later scrub re-enters block-pointer/checksum space | "
    "logical blocks map through fixed-width dRAID groups and deterministic permutations; recovery traversal can use space-map/device-address order rather than full block-tree traversal | "
    "distributed spare regions become recovery destinations; replacement/rebalancing can later move state again while restoring spare availability | "
    "does not preserve a complete mutation history; preserves layout/rebuild state sufficient to restore missing contributions, then separately revalidates integrity |"
)
insert_after_line(
    "CASE_INDEX.md",
    "| ZFS RAID-Z dynamic-stripe COW / 2005–2010 bounded regime |",
    matrix_row,
    "| OpenZFS dRAID / 2017–2021 bounded recovery regime |",
)

idx = Path("CASE_INDEX.md")
text = idx.read_text()
if "### Case 96 — OpenZFS dRAID redundancy-restoration findings" not in text:
    findings = """

### Case 96 — OpenZFS dRAID redundancy-restoration findings

1213. **spare capacity presence ≠ spare-path bandwidth** — a dedicated hot spare can provide enough destination capacity while its single-device write bandwidth still prolongs the degraded interval; dRAID distributes that destination capacity across many children.

1214. **parity count ≠ redundancy-restoration speed** — the configured number of parity contributions describes an erasure margin, while layout, stripe width, recovery traversal, and available device bandwidth determine how quickly a lost contribution can be reconstituted.

1215. **same nominal redundancy ≠ same duration of reduced redundancy** — two layouts can tolerate the same initial failure yet expose retained state to different lengths of degraded operation because one removes recovery bottlenecks more effectively.

1216. **distributed spare ≠ independent full replica** — dRAID spare regions are reserved transition capacity distributed through the vdev; they are not an additional ordinary current copy of every logical block.

1217. **parity declustering ≠ increased parity count** — distributing redundancy groups and recovery load across more devices changes placement and repair parallelism without by itself adding another independent parity equation.

1218. **sequential reconstruction ≠ healing reconstruction** — the released implementation deliberately separates LBA-ordered device rebuild from block-aware healing traversal; the former can restore redundancy faster while omitting per-block checksum verification in that phase.

1219. **redundancy restored ≠ integrity fully revalidated** — after the sequential first phase, the configured coded margin can be back even though a follow-up scrub is still needed to verify block checksums.

1220. **fixed dRAID stripe width ≠ RAID-Z variable-width stripe** — Case 95's variable geometry and Case 96's fixed-width recovery geometry solve different constraints; one layout choice must not be universalized across both problems.

1221. **faster first-phase recovery ≠ shorter total verification work** — `vdev_rebuild.c` explicitly allows a later scrub; reducing time to regain redundancy can move checksum work into a second phase rather than eliminate it.

1222. **space-map-guided recovery ≠ block-pointer-guided validation** — sequential reconstruction can recover allocated device ranges without traversing every block pointer, but that same shortcut removes the block-pointer/checksum context used for immediate integrity verification.

1223. **stable payload sectors ≠ stable recoverability under mapping drift** — released dRAID source warns that its deterministic permutation maps must remain reproducible because existing pools depend on them to locate data; software compatibility can therefore be part of storage interpretability.

1224. **hard-coded mapping continuity ≠ user-payload retention** — constants and mapping algorithms can be constitutive recovery infrastructure even though applications never treat them as stored file content.

1225. **benchmark speedup ≠ universal durability ratio** — PR #10102's roughly 30-hour versus 7–8-hour example is evidence for one 90-HDD bottleneck regime, not a portable multiplier for all dRAID configurations.

1226. **OpenZFS dRAID ≠ invention of parity declustering or distributed sparing** — CMU work from 1992–1994 already treated both recovery-load declustering and distributed spare capacity; the defensible claim is a specific OpenZFS composition and released implementation.

1227. **repair performance can be retention infrastructure without becoming mere performance analysis** — when failure reduces redundancy margin, recovery throughput changes the time during which another failure would exceed that margin; foreground throughput and retention exposure must still be kept distinct.

1228. **redundancy is a time-varying relation during repair** — after failure, the system can remain serviceable while possessing less future failure tolerance, and maintenance work can later reconstitute that margin; nominal layout alone does not describe the whole retention trajectory.
"""
    idx.write_text(text.rstrip() + findings + "\n")

for p in (Path(case_path), Path(evidence_path)):
    if not p.exists():
        raise SystemExit(f"missing permanent Case 96 file: {p}")

case_files = sorted(Path("cases").glob("[0-9][0-9]-*.md"))
grounded = sum("**Status:** `grounded`" in p.read_text() for p in case_files)
if len(case_files) != 95 or grounded != 95:
    raise SystemExit(f"unexpected aggregate: cases={len(case_files)} grounded={grounded}")

checks = [
    ("README.md", case_path),
    ("ROADMAP.md", case_path),
    ("CASE_INDEX.md", case_path),
    ("CASE_INDEX.md", "### Case 96 — OpenZFS dRAID redundancy-restoration findings"),
    ("CASE_INDEX.md", "| OpenZFS dRAID / 2017–2021 bounded recovery regime |"),
]
for path, marker in checks:
    if marker not in Path(path).read_text():
        raise SystemExit(f"integration marker missing: {path}: {marker}")

# Structural sanity: every comparison row must remain inside a Markdown table neighborhood.
lines = Path("CASE_INDEX.md").read_text().splitlines()
for marker in ["| OpenZFS dRAID / 2017–2021 bounded recovery regime |"]:
    i = next((n for n, line in enumerate(lines) if marker in line), None)
    if i is None or i == 0 or i + 1 >= len(lines):
        raise SystemExit("comparison row structure check failed")
    if not lines[i - 1].startswith("|") or not lines[i + 1].startswith("|"):
        raise SystemExit("Case 96 comparison row is outside its Markdown table")

print(f"validated canonical aggregate: {len(case_files)} cases, {grounded} grounded")
