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


case_path = "cases/95-zfs-raidz-dynamic-stripe-write-hole.md"
evidence_path = "evidence/95-zfs-2005-2010-raidz-write-hole-grounding.md"

readme_line = (
    "- [`cases/95-zfs-raidz-dynamic-stripe-write-hole.md`](cases/95-zfs-raidz-dynamic-stripe-write-hole.md) — "
    "grounded ZFS RAID-Z write-hole bridge: Sun/Oracle documentation ties variable-width full-stripe writes to integrated filesystem/device metadata and ZFS copy-on-write transactional replacement, so an interrupted update need not leave the authoritative block as a half-overwritten fixed parity stripe; the case keeps latest-write durability, device-cache persistence, checksum diagnosis, parity count, and secure erasure separate; see [`evidence/95-zfs-2005-2010-raidz-write-hole-grounding.md`](evidence/95-zfs-2005-2010-raidz-write-hole-grounding.md)."
)
insert_after_line(
    "README.md",
    "cases/94-raid6-pq-dual-erasure-corruption-boundary.md",
    readme_line,
    case_path,
)

roadmap_line = (
    "- [x] ZFS RAID-Z dynamic-width full-stripe / copy-on-write write-hole boundary — "
    "[`cases/95-zfs-raidz-dynamic-stripe-write-hole.md`](cases/95-zfs-raidz-dynamic-stripe-write-hole.md), grounded by "
    "[`evidence/95-zfs-2005-2010-raidz-write-hole-grounding.md`](evidence/95-zfs-2005-2010-raidz-write-hole-grounding.md), adds a bounded alternative to Case 88's PPL strategy: Sun/Oracle documentation states that RAID-Z uses variable-width stripes so each RAID-Z write is a full-stripe write, with filesystem metadata carrying enough redundancy/layout information to interpret that geometry, while ZFS copy-on-write keeps the old committed tree distinct until the new state becomes authoritative. This separates write-hole avoidance from newest-write durability, lower-layer cache persistence, checksum/scrub authority, RAID-Z2/3 failure margin, and secure erasure. Broad ZFS/WAFL/COW/parity genealogy, RAID-Z2/3/dRAID, ZIL/SLOG, modern expansion, and fault injection remain separate work for `computing-archaeology` or later bounded cases."
)
insert_after_line(
    "ROADMAP.md",
    "cases/94-raid6-pq-dual-erasure-corruption-boundary.md",
    roadmap_line,
    case_path,
)

case_row = (
    "| [ZFS RAID-Z: Dynamic-Width Full-Stripe Writes and Write-Hole Avoidance](cases/95-zfs-raidz-dynamic-stripe-write-hole.md) | **grounded** | "
    "copy-on-write filesystem tree + variable-width RAID-Z data/parity stripe + retained block-pointer/redundancy geometry + transaction/commit authority | "
    "separate fixed-stripe partial-update repair from layout-mediated write-hole avoidance; distinguish full-stripe from fixed all-member width, coded-byte survival from geometry interpretability, filesystem consistency from newest-write durability, and RAID-Z layout from checksum/scrub or lower-layer persistence | "
    "[2005–2010 ZFS/RAID-Z grounding](evidence/95-zfs-2005-2010-raidz-write-hole-grounding.md); original Sun weblog/source-code archaeology, WAFL/COW/parity genealogy, RAID-Z2/3/dRAID, ZIL/SLOG, expansion/reflow, named-system fault injection, and retired-block forensics remain separate work |"
)
insert_after_line(
    "CASE_INDEX.md",
    "cases/94-raid6-pq-dual-erasure-corruption-boundary.md",
    case_row,
    case_path,
)

matrix_row = (
    "| ZFS RAID-Z dynamic-stripe COW / 2005–2010 bounded regime | committed block tree + variable-width RAID-Z data/parity columns + block-pointer/redundancy geometry + transaction authority | "
    "allocate/write new COW blocks; calculate a complete parity relation for the selected dynamic stripe; retain metadata needed to interpret geometry; commit/select the new tree; reclaim older embodiments later | "
    "ordinary reads are outside this bounded write-hole slice; reconstruction still depends on geometry and separate checksum/integrity qualification | "
    "filesystem block pointer resolves logical block to vdev/RAID-Z layout whose width is not globally fixed | "
    "old committed embodiment can remain separately admissible while new physical sectors/columns are written; later reclamation can retire the old embodiment | "
    "no complete write history by default; retains current committed tree/geometry relations rather than a PPL-style repair log, while uncommitted newest async state may be lost |"
)
insert_after_line(
    "CASE_INDEX.md",
    "| RAID-6 P+Q / 1993–2011 bounded regime |",
    matrix_row,
    "| ZFS RAID-Z dynamic-stripe COW / 2005–2010 bounded regime |",
)

idx = Path("CASE_INDEX.md")
text = idx.read_text()
if "### Case 95 — ZFS RAID-Z dynamic-stripe write-hole findings" not in text:
    findings = """

### Case 95 — ZFS RAID-Z dynamic-stripe write-hole findings

1197. **write-hole avoidance ≠ mere parity presence** — the traditional failure is a currentness relation: individually surviving data/parity blocks can cease to describe one coherent stripe after an interrupted partial update.

1198. **RAID-Z full-stripe write ≠ fixed-width all-member write** — the bounded Sun/Oracle mechanism is variable-width; completeness is relative to the RAID-Z block's chosen geometry rather than one globally fixed stripe width.

1199. **copy-on-write old-state survival ≠ latest-write durability** — keeping the old committed tree admissible while a new tree is assembled prevents one class of mixed old/new filesystem state, while Solaris documentation still allows the most recent asynchronous data to be lost.

1200. **layout-mediated write-hole avoidance ≠ recovery logging** — RAID-Z changes the update/layout composition, whereas Case 88 PPL retains bounded temporary evidence before an otherwise non-atomic standing-stripe update.

1201. **stripe-geometry metadata ≠ user payload** — filesystem/device metadata can be required to interpret which data/parity columns form a variable-width coded block even though those metadata are not the file's ordinary payload.

1202. **surviving data/parity bytes ≠ interpretable RAID-Z block** — when width/layout is variable, coded material alone is not sufficient if the relation that identifies the block's geometry is unavailable or untrusted.

1203. **metadata integration ≠ parity self-description** — the official design explanation makes higher-level metadata knowledge part of handling the redundancy geometry rather than claiming that parity sectors independently encode all interpretation needed for reconstruction.

1204. **RAID-Z write-hole avoidance ≠ lower-layer power-loss persistence** — filesystem-level COW/full-stripe composition does not make a volatile device/controller cache nonvolatile; Cases 20/87 remain separate durability boundaries.

1205. **RAID-Z write-hole avoidance ≠ silent-corruption diagnosis** — preventing an interrupted partial parity update from becoming authoritative is distinct from checksum-qualified detection and repair, which Case 18 treats separately.

1206. **single-parity RAID-Z write-hole semantics ≠ RAID-Z2/3 failure margin** — stripe-update consistency and the number of tolerated missing device contributions are different axes; Case 94's coding-strength distinction remains separate.

1207. **temporary survival of superseded COW blocks ≠ user-visible version-history guarantee** — old physical/tree material can remain until reclamation without becoming a promised historical archive.

1208. **loss of current-tree authority ≠ secure erasure** — an old COW block can cease to participate in current filesystem service before lower-layer media sanitization; Cases 44/47 remain the stronger forgetting boundary.

1209. **period-preserved Bonwick quotation ≠ direct inspection of the original Sun weblog** — the 2006 preservation corroborates period explanation, while official surviving Sun/Oracle documentation carries the central mechanism claim.

1210. **Oracle software-first wording ≠ universal invention-priority proof** — full-stripe writes, parity arrays, and copy-on-write all have earlier histories; a broad priority claim requires separate genealogy rather than vendor documentation alone.

1211. **per-block dynamic stripe ≠ absence of retained layout state** — making each logical RAID-Z block its own coded stripe increases, rather than removes, the need to preserve enough metadata to recover that block's geometry later.

1212. **admissible continuation can be preserved by replacement-before-retirement rather than maximal repair history** — RAID-Z supplies a bounded counterexample in which an older committed embodiment remains usable until a new complete coded/layout relation becomes authoritative, instead of retaining a complete history of the interrupted mutation.
"""
    idx.write_text(text.rstrip() + findings + "\n")

for p in (Path(case_path), Path(evidence_path)):
    if not p.exists():
        raise SystemExit(f"missing permanent Case 95 file: {p}")

case_files = sorted(Path("cases").glob("[0-9][0-9]-*.md"))
grounded = sum("**Status:** `grounded`" in p.read_text() for p in case_files)
if len(case_files) != 94 or grounded != 94:
    raise SystemExit(f"unexpected aggregate: cases={len(case_files)} grounded={grounded}")

for path, marker in [
    ("README.md", case_path),
    ("ROADMAP.md", case_path),
    ("CASE_INDEX.md", case_path),
    ("CASE_INDEX.md", "### Case 95 — ZFS RAID-Z dynamic-stripe write-hole findings"),
    ("CASE_INDEX.md", "| ZFS RAID-Z dynamic-stripe COW / 2005–2010 bounded regime |"),
]:
    if marker not in Path(path).read_text():
        raise SystemExit(f"integration marker missing: {path}: {marker}")

print(f"validated canonical aggregate: {len(case_files)} cases, {grounded} grounded")
