from pathlib import Path

roadmap_path = Path("ROADMAP.md")
roadmap = roadmap_path.read_text(encoding="utf-8")
old128 = "- [x] Case 128 ZFS vdev-label / uberblock restart-root grounding — [`cases/128-zfs-vdev-label-uberblock-import-root-recovery.md`](cases/128-zfs-vdev-label-uberblock-import-root-recovery.md), grounded by [`evidence/128-zfs-2005-2026-vdev-label-uberblock-grounding.md`](evidence/128-zfs-2005-2026-vdev-label-uberblock-grounding.md): the 9-Dec-2005 Sun on-disk specification anchors four spatially separated labels, staged fixed-label updates, topology/identity nvlist state, a rotating uberblock array, transaction/checksum qualification, and `ub_rootbp` into the MOS; current OpenZFS docs/source are later continuity witnesses only. This closes the bounded `payload survival ≠ restart legibility` and `root presence ≠ root admissibility` relations, while hardware-controller loss, severe root-chain corruption, format-obsolescence, release genealogy, and empirical fault injection remain open."
new128 = "- [x] Case 128 ZFS vdev-label / uberblock restart-root grounding — [`cases/128-zfs-vdev-label-uberblock-import-root-recovery.md`](cases/128-zfs-vdev-label-uberblock-import-root-recovery.md), grounded by [`evidence/128-zfs-2005-2026-vdev-label-uberblock-grounding.md`](evidence/128-zfs-2005-2026-vdev-label-uberblock-grounding.md): the 9-Dec-2005 Sun on-disk specification anchors four spatially separated labels, staged fixed-label updates, topology/identity nvlist state, a rotating uberblock array, transaction/checksum qualification, and `ub_rootbp` into the MOS; current OpenZFS docs/source are later continuity witnesses only. This closes the bounded `payload survival ≠ restart legibility` and `root presence ≠ root admissibility` relations. Feature-flag / format-software admissibility is now handled separately by grounded Case 129; hardware-controller loss, severe root-chain corruption, release genealogy, and empirical fault injection remain open."
case129_bullet = "- [x] Case 129 ZFS/OpenZFS feature-flags / format-software compatibility boundary — [`cases/129-zfs-feature-flags-format-compatibility.md`](cases/129-zfs-feature-flags-format-compatibility.md), grounded by [`evidence/129-zfs-2012-feature-flags-compatibility-grounding.md`](evidence/129-zfs-2012-feature-flags-compatibility-grounding.md): the 21-May-2012 illumos feature-flags integration separates pre-feature SPA versions from version-5000 feature mode, retains distinct `features_for_read` / `features_for_write` requirements, exposes `disabled` / `enabled` / `active` state, and explicitly distinguishes unsupported-for-read from unsupported-for-write with a possible read-only fallback; FreeBSD's 11-Jun-2012 adoption supplies a contemporary portability witness and its 2016 loader change later confirms that merely enabled-but-unused features need not block a narrower interpreter. This closes the bounded `surviving pool/root ≠ compatible interpreter ≠ read-only admission ≠ read-write admission` relation and substantially advances format/software obsolescence without treating incompatibility as physical erasure. Exact ext-family prior art, per-feature release matrices, send/dataset formats, loader matrices, migration/emulation, corruption tests, and broad obsolescence history remain open."
if old128 not in roadmap:
    raise SystemExit("ROADMAP Case128 anchor not found")
roadmap = roadmap.replace(old128, new128 + "\n" + case129_bullet, 1)
old_obsol = "- [ ] format/software obsolescence;"
new_obsol = "- [ ] format/software obsolescence — **substantially advanced at the ZFS pool-format layer by grounded Case 129**: a physically surviving/import-discoverable pool can remain read-write-inadmissible or fully unreadable to software that lacks semantics required by its retained active feature set, while an enabled-but-unused feature can remain backward-compatible and a read-only-compatible unknown feature can preserve a weaker read path. This establishes `physical survival ≠ interpreter availability ≠ format admissibility` without closing broader filesystem/file-format obsolescence, send-stream/dataset formats, hardware/controller interfaces, emulation/migration, software-preservation infrastructure, or institutional recovery;"
if old_obsol not in roadmap:
    raise SystemExit("ROADMAP obsolescence anchor not found")
roadmap = roadmap.replace(old_obsol, new_obsol, 1)

case128_path = Path("cases/128-zfs-vdev-label-uberblock-import-root-recovery.md")
case128 = case128_path.read_text(encoding="utf-8")
needle = "- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — fresh searches for `ZFS`, `uberblock`, and `vdev label` found no dedicated case to reuse. Broad superblock history, ZFS source genealogy, controller history, and filesystem implementation archaeology belong there if developed."
replacement = needle + "\n- [`Case 129 — ZFS feature flags / format compatibility`](129-zfs-feature-flags-format-compatibility.md) — handles the separate question of whether a surviving, root-legible pool remains interpretable by a particular software/boot environment. `restart-root admissibility ≠ format admissibility`."
if needle not in case128:
    raise SystemExit("Case128 link anchor not found")
case128 = case128.replace(needle, replacement, 1)

e128_path = Path("evidence/128-zfs-2005-2026-vdev-label-uberblock-grounding.md")
e128 = e128_path.read_text(encoding="utf-8")
old_gap = "- feature-flag/format-obsolescence behavior across old/new implementations;"
new_gap = "- feature-flag / format-software admissibility is now handled separately by grounded [`Case 129`](../cases/129-zfs-feature-flags-format-compatibility.md); exact cross-release matrices and broader obsolescence remain open there;"
if old_gap not in e128:
    raise SystemExit("Evidence128 gap anchor not found")
e128 = e128.replace(old_gap, new_gap, 1)

index_path = Path("CASE_INDEX.md")
index = index_path.read_text(encoding="utf-8")
old_row = "| [ZFS Vdev Labels and Uberblocks: Retained Pool Topology and Restart Roots](cases/128-zfs-vdev-label-uberblock-import-root-recovery.md) | **grounded** | nonvolatile pool payload + four separated fixed vdev-label copies + topology/configuration nvlist + rotating uberblock restart roots + validity/currentness qualification | separate physical payload survival, topology legibility, restart-root authority, importability, integrity verification, and redundancy repair; show that a small retained root relation can organize access to a much larger surviving store | [2005–2026 grounding record](evidence/128-zfs-2005-2026-vdev-label-uberblock-grounding.md); release-by-release evolution, severe root corruption, modern MMP tie-breaking, hardware-controller failure, format obsolescence, and fault injection remain open |"
new_row128 = "| [ZFS Vdev Labels and Uberblocks: Retained Pool Topology and Restart Roots](cases/128-zfs-vdev-label-uberblock-import-root-recovery.md) | **grounded** | nonvolatile pool payload + four separated fixed vdev-label copies + topology/configuration nvlist + rotating uberblock restart roots + validity/currentness qualification | separate physical payload survival, topology legibility, restart-root authority, importability, integrity verification, and redundancy repair; show that a small retained root relation can organize access to a much larger surviving store | [2005–2026 grounding record](evidence/128-zfs-2005-2026-vdev-label-uberblock-grounding.md); feature/format admissibility is handled separately in Case 129; release-by-release root evolution, severe corruption, modern MMP tie-breaking, hardware-controller failure, and fault injection remain open |"
row129 = "| [ZFS Feature Flags: Retained Format Requirements and Software Admissibility](cases/129-zfs-feature-flags-format-compatibility.md) | **grounded** | surviving pool bytes/restart roots + retained feature GUID/refcount sets + read/write-required feature classes + software interpreter capability | separate physical survival from software interpretability; enabled capability from active on-disk use; read compatibility from write compatibility; and format-state persistence from interpreter availability | [2012–2016 feature-flags grounding](evidence/129-zfs-2012-feature-flags-compatibility-grounding.md); exact ext-family prior art, per-feature release matrices, send/dataset formats, boot matrices, migration/emulation, fault traces, and broad format-obsolescence genealogy remain open |"
if old_row not in index:
    raise SystemExit("CASE_INDEX Case128 row anchor not found")
index = index.replace(old_row, new_row128 + "\n" + row129, 1)
if "## Case 129 — ZFS feature-flag / format-compatibility findings" in index:
    raise SystemExit("Case129 findings already exist")
findings = r'''

## Case 129 — ZFS feature-flag / format-compatibility findings

- **2269 — payload/root survival ≠ software interpretability:** pool blocks, labels, and an admissible restart root may survive while a particular implementation still lacks semantics required by the retained active feature set. (`H/P`, `E`)
- **2270 — pool discovery/root selection ≠ read-write admissibility:** locating a pool and selecting a root do not by themselves authorize a software version to mutate that on-disk format. (`H/P`, `E`)
- **2271 — `enabled` ≠ `active`:** the 2012 feature-property machinery and current OpenZFS continuity distinguish administratively enabled capability from feature-dependent on-disk format actually being in use. (`H/P`)
- **2272 — feature support ≠ feature use:** software may implement many features that a particular pool never activates; compatibility is determined by the relevant retained pool requirements rather than the implementation's complete capability list. (`H/P`, `E`)
- **2273 — unsupported-for-write ≠ unreadable:** the 2012 load/status path explicitly allows a pool that cannot be opened read-write to remain eligible for read-only access when its read requirements are still understood. (`H/P`)
- **2274 — read-only-compatible unknown feature ≠ full compatibility:** retaining a read path does not imply that the same implementation may safely modify the pool. (`H/P`, `E`)
- **2275 — required-for-read ≠ required-for-write:** `features_for_read` and `features_for_write` are separately retained and separately checked; access mode changes the relevant compatibility obligation. (`H/P`)
- **2276 — feature GUID/name recognition ≠ semantic implementation:** recognizing that an unknown feature exists is enough to reject or downgrade service, not enough to interpret its format changes. (`H/P`, `E`)
- **2277 — active-feature state ≠ complete operation history:** feature/refcount metadata summarizes present format requirements without retaining the full sequence of operations that activated them. (`H/P`, `E`)
- **2278 — software downgrade/absence ≠ physical erasure:** losing a compatible interpreter can remove ordinary access while leaving the pool's material inscription unchanged. (`E`, `I`)
- **2279 — interpreter availability ≠ media integrity:** installing software that understands the active feature set restores one admissibility condition but does not prove checksums, redundancy, or every payload block are healthy. (`E`, `A`)
- **2280 — SPA version 5000 ≠ one monolithic feature level:** the feature regime uses 5000 as a mode boundary while individual feature requirements determine actual post-28 format compatibility. (`H/P`, `E`, `X`)
- **2281 — feature activation can narrow backward compatibility without destroying payload:** a pool may remain physically intact while a newly used feature causes older software to lose read-write or all import admissibility. (`H/P`, `E`)
- **2282 — import compatibility ≠ boot compatibility:** the 2016 FreeBSD loader witness shows a boot environment has its own supported-feature set; userspace that created/uses a pool and a boot loader need not have identical interpreter capability. (`H/P` later continuity, `E`)
- **2283 — Case 128 restart-root admissibility ≠ Case 129 format admissibility:** one relation selects/roots a surviving pool graph; the other asks whether the current interpreter understands the retained format requirements. They compose without becoming one mechanism. (`A`, `E`, `X`)
- **2284 — related-repository boundary:** fresh `tmzncty/computing-archaeology` searches found no dedicated ZFS feature-flag case in the current search surface; broad filesystem compatibility-bit genealogy, software preservation, migration, and format-obsolescence history belong there if developed. (`H/P` project-state record)
'''
index = index.rstrip() + findings.rstrip() + "\n"

roadmap_path.write_text(roadmap.rstrip() + "\n", encoding="utf-8")
case128_path.write_text(case128.rstrip() + "\n", encoding="utf-8")
e128_path.write_text(e128.rstrip() + "\n", encoding="utf-8")
index_path.write_text(index, encoding="utf-8")
