from pathlib import Path

CASE_PATH = Path('cases/125-linux-ext3-ext4-orphan-crash-cleanup-reclamation.md')
EVIDENCE_PATH = Path('evidence/125-linux-ext3-ext4-2000-2023-orphan-recovery-grounding.md')
INDEX_PATH = Path('CASE_INDEX.md')
ROADMAP_PATH = Path('ROADMAP.md')

assert CASE_PATH.exists(), CASE_PATH
assert EVIDENCE_PATH.exists(), EVIDENCE_PATH

idx = INDEX_PATH.read_text(encoding='utf-8')

row = (
    '| [Linux ext3/ext4 Orphan Tracking: Crash-Persistent Cleanup Obligations and Deferred Reclamation]'
    '(cases/125-linux-ext3-ext4-orphan-crash-cleanup-reclamation.md) | **grounded** | '
    'namespace/link state + inode/block ownership + on-disk orphan target set + journal recovery + scan-admission feature state | '
    'separate namespace detachment from reclamation; cleanup obligation from completion; replay from orphan restart; target identity from target-state consistency; and recovery function from one metadata representation | '
    '[2000–2023 ext3/ext4 orphan-recovery grounding](evidence/125-linux-ext3-ext4-2000-2023-orphan-recovery-grounding.md); '
    'earliest Andreas Dilger patch/tarball, damaged-orphan/e2fsprogs behavior, fault-injection matrix, cross-filesystem genealogy, and lower-layer sanitization remain open |'
)

table_marker = '\n\n---\n\n\n## Comparison matrix — provisional'
if 'cases/125-linux-ext3-ext4-orphan-crash-cleanup-reclamation.md' not in idx:
    assert table_marker in idx
    idx = idx.replace(table_marker, '\n' + row + table_marker, 1)

findings = '''

## Case 125 — Linux ext3/ext4 orphan recovery findings

- **2125 — July-2000 ext3 orphan-list implementation floor ≠ invention date:** `ext3-0.0.2e` publicly announces orphan-list code and explicitly credits an Andreas Dilger implementation basis; the source cannot support a sole-inventor or first-ever-filesystem claim. (`H/P`, `X`)
- **2126 — namespace detachment ≠ storage reclamation:** an inode can lose ordinary directory reachability while remaining alive through an open reference or while truncate/delete cleanup is unfinished. (`H/P`, `E`)
- **2127 — unlinked-open inode lifetime ≠ pathname lifetime:** the 2000 release record and current ext4 documentation both make the crash-cleanup problem arise precisely because directory hierarchy and inode/resource lifetime can diverge. (`H/P`, `E`)
- **2128 — orphan-target metadata ≠ user payload:** the on-disk list/file identifies inodes needing later cleanup; it does not duplicate the file bytes it helps retire. (`H/P`, `E`)
- **2129 — orphan membership ≠ cleanup completion:** retaining an inode in the orphan structure records outstanding delete/truncate work rather than proving that blocks/inode have already been reclaimed. (`H/P`, `E`)
- **2130 — cleanup-target identity ≠ sufficient target semantics:** the 2023 orphan-file power-cut bug shows that a retained inode number can still be misinterpreted when the on-disk inode link-count state is stale. (`H/P`, `E`)
- **2131 — journal replay ≠ orphan cleanup:** Linux v2.6.12 `ext3_truncate()` explicitly orders journal replay before restart of truncate against the orphan list; these are compositional recovery phases, not synonyms. (`H/P`)
- **2132 — desired committed file size ≠ blocks already reclaimed:** the v2.6.12 truncate comment allows committed `i_size` to coexist after crash with blocks beyond the truncation point that later orphan cleanup must release. (`H/P`, `E`)
- **2133 — crash-restartable cleanup ≠ zero recovery work:** orphan cleanup reuses journaled deletion/truncate paths so another crash can remain recoverable, but that restartability does not make mount-time cleanup instantaneous or unnecessary. (`H/P`, `E`)
- **2134 — traditional linked list ≠ modern orphan-file representation:** ext4's 2021 change stores inode numbers in a special file for scalability while retaining the same bounded future-cleanup function; representation continuity and mechanism origin are separate claims. (`H/P`, `E`, `X`)
- **2135 — `RO_COMPAT_ORPHAN_PRESENT` ≠ orphan population:** the feature bit summarizes whether mount should treat the orphan file as possibly containing valid entries, while the entries themselves identify cleanup targets. (`H/P`, `E`)
- **2136 — clean-unmount clearing of scan state ≠ payload erasure:** removing `RO_COMPAT_ORPHAN_PRESENT` after clean unmount avoids an unnecessary future scan; it is not evidence that user data were sanitized or media were overwritten. (`H/P`, `E`, `X`)
- **2137 — 2021 scaling change ≠ invention of orphan recovery:** commit `02f310fcf47f...` explicitly starts from the pre-existing on-disk linked list and changes how orphan inodes are represented/contended. (`H/P`, `X`)
- **2138 — 2023 power-cut inconsistency ≠ demonstrated payload loss:** the documented failure is an allocated unattached inode left after recovery; the evidence validates recovery-metadata consistency requirements without proving that the file payload vanished. (`H/P`, `X`)
- **2139 — physical block survival ≠ safely reusable capacity:** blocks can remain present while allocation ownership/reclamation is unresolved; reuse requires filesystem metadata to close the ownership transition. (`E`)
- **2140 — Case 16 deferred reclamation ≠ Case 125 orphan tracking:** BSD FFS soft updates can preserve crash-admissible state while later repair reclaims leaks; ext3/ext4 retain explicit inode targets for resumed cleanup. The similarity is functional, not demonstrated genealogy. (`A`, `X`)
- **2141 — Case 74/124 recovery adjacency ≠ one filesystem-retention mechanism:** JBD revoke suppresses stale redo, Case 124 separates pathname/file durability, and Case 125 retains post-crash cleanup targets; replay authority, namespace durability, and reclamation obligation remain distinct relations. (`A`, `X`)
- **2142 — related-repository boundary:** fresh `tmzncty/computing-archaeology` searches found no dedicated ext3/ext4 orphan case to reuse; broad Unix inode lifetime, ext-family/JBD genealogy, `fsck`, and crash-consistency history belong there if developed. (`H/P` project-state record)
'''
if '## Case 125 — Linux ext3/ext4 orphan recovery findings' not in idx:
    assert '**2124 — related-repository boundary:**' in idx
    idx = idx.rstrip() + findings + '\n'

INDEX_PATH.write_text('\n'.join(line.rstrip() for line in idx.splitlines()) + '\n', encoding='utf-8')

road = ROADMAP_PATH.read_text(encoding='utf-8')
old_gc = '- [ ] garbage collection / reclamation — **partially advanced by grounded Case 73 at the distributed-filesystem layer**: GFS 2003 separates logged deletion, hidden-name grace, namespace/chunk reference retirement, HeartBeat-driven replica cleanup, and stale-replica deauthorization; broader filesystem, database, Flash/controller, and media-reclamation genealogies remain open;'
new_gc = '- [ ] garbage collection / reclamation — **partially advanced by grounded Cases 73 and 125**: GFS 2003 separates logged deletion, hidden-name grace, namespace/chunk reference retirement, HeartBeat-driven replica cleanup, and stale-replica deauthorization; Case 125 adds the local-filesystem crash boundary in which ext3/ext4 retain explicit orphan inode targets so delete/truncate cleanup can resume after replay before blocks/inodes become reusable. Database, Flash/controller, distributed/object-store, damaged-recovery-metadata, and media-reclamation genealogies remain open;'
if new_gc not in road:
    assert old_gc in road
    road = road.replace(old_gc, new_gc, 1)

old_leak = '- [ ] post-crash resource leakage / unreclaimed allocation state;'
new_leak = '- [ ] post-crash resource leakage / unreclaimed allocation state — **substantially advanced at the filesystem layer by grounded Cases 16 and 125**: Case 16 shows BSD FFS soft updates can preserve a crash-admissible image while later reclamation remains outstanding; Case 125 adds explicit ext3/ext4 crash-persistent cleanup targets for unlinked-open inodes and multi-transaction truncates, separates journal replay from orphan restart, and uses the 2023 orphan-file power-cut bug to show `cleanup-target identity ≠ sufficient target-state consistency`. Corrupt/lost orphan metadata, cross-filesystem allocation leaks, database/controller allocation recovery, and empirical fault matrices remain open;'
if new_leak not in road:
    assert old_leak in road
    road = road.replace(old_leak, new_leak, 1)

ROADMAP_PATH.write_text('\n'.join(line.rstrip() for line in road.splitlines()) + '\n', encoding='utf-8')
