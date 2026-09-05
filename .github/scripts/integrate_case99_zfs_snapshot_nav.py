from pathlib import Path

ROOT = Path('.')


def insert_after_unique_line(path: str, needle: str, block: str) -> None:
    p = ROOT / path
    lines = p.read_text(encoding='utf-8').splitlines()
    matches = [i for i, line in enumerate(lines) if needle in line]
    if len(matches) != 1:
        raise SystemExit(f'{path}: expected one line containing {needle!r}, found {len(matches)}')
    i = matches[0]
    addition = block.rstrip('\n').splitlines()
    lines[i + 1:i + 1] = addition
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')


insert_after_unique_line(
    'README.md',
    'cases/98-ceph-unfound-recovery-exhaustion-administrative-loss.md',
    '- [`cases/99-zfs-snapshot-reference-pinned-retention.md`](cases/99-zfs-snapshot-reference-pinned-retention.md) — grounded ZFS snapshot / deferred-reclamation case: 2010 Solaris documentation shows a snapshot preserving an old point-in-time tree by continuing to reference blocks that the live dataset no longer needs, so supersession, reference retirement, allocator reclamation, and secure erasure remain separate; holds/deferred destroy make `destroy request ≠ immediate forgetting`; WAFL 1994 supplies an explicit earlier COW-snapshot prior-art floor. See [`evidence/99-zfs-1994-2010-snapshot-reference-grounding.md`](evidence/99-zfs-1994-2010-snapshot-reference-grounding.md).'
)

insert_after_unique_line(
    'ROADMAP.md',
    'Ceph `unfound` / administrator-gated `lost` recovery-exhaustion boundary',
    '- [x] ZFS snapshot reference-pinning / deferred reclamation boundary — [`cases/99-zfs-snapshot-reference-pinned-retention.md`](cases/99-zfs-snapshot-reference-pinned-retention.md), grounded by [`evidence/99-zfs-1994-2010-snapshot-reference-grounding.md`](evidence/99-zfs-1994-2010-snapshot-reference-grounding.md): a 2010 Solaris ZFS snapshot keeps an older point-in-time tree admissible by retaining references to old blocks, separating live-dataset supersession from reclamation eligibility; `hold`, clone dependencies, and `defer_destroy` further separate destroy intent from permission/completion. WAFL 1994 is retained only as an earlier COW-snapshot prior-art floor, not as proven direct genealogy. Broader filesystem snapshot/COW lineage, ZFS send/receive retention policy, clone genealogy, field space-exhaustion behavior, and secure media erasure remain open.'
)

insert_after_unique_line(
    'CASE_INDEX.md',
    'cases/98-ceph-unfound-recovery-exhaustion-administrative-loss.md',
    '| [ZFS Snapshots: Reference-Pinned Old Blocks, Rollback, and Deferred Reclamation](cases/99-zfs-snapshot-reference-pinned-retention.md) | **grounded** | copy-on-write old tree + snapshot/root references + shared/unique block accounting + clone/hold destruction constraints + rollback | separate live supersession from historical reachability; logical retained extent from unique physical charge; destroy request from reclamation; reference retirement from secure erase | [WAFL 1994 / Solaris ZFS 2010 grounding](evidence/99-zfs-1994-2010-snapshot-reference-grounding.md); broader COW/snapshot genealogy, send/receive policy, clones, pool-space field evidence, and secure-erasure validation remain separate work |'
)

insert_after_unique_line(
    'CASE_INDEX.md',
    '1304. **retention can preserve an obligation toward absent state**',
    r'''

### Case 99 — ZFS snapshot / reference-pinned-retention findings

1305. **copy-on-write old-block survival ≠ snapshot retention** — COW can leave an old embodiment intact during replacement, but a snapshot makes that old tree intentionally persistent by retaining a valid reachability relation.
1306. **live-dataset supersession ≠ reclamation eligibility** — a block no longer current in the live dataset can remain non-reclaimable because a snapshot still references it.
1307. **logical retained extent ≠ unique physical-space charge** — a new snapshot can expose a complete point-in-time view while initially sharing almost all blocks with the live dataset.
1308. **temporal namespace separation ≠ separate backing store** — `.zfs/snapshot` can expose an older filesystem view while the snapshot shares the same pool and many of the same blocks.
1309. **one physical block ≠ one temporal owner** — the same block can be simultaneously reachable from the live filesystem and multiple snapshots until later divergence changes the reference graph.
1310. **snapshot `used` ≠ total historical content visible through the snapshot** — `used` accounts for snapshot-unique space, while `referenced`/reachability describe a larger logical view.
1311. **destroy request ≠ immediate destruction** — ZFS holds and clone dependencies can block ordinary snapshot destroy, while deferred destroy records an intent that cannot yet complete.
1312. **intent to forget ≠ permission to reclaim ≠ physical secure erase** — these are three separate lifecycle stages across snapshot policy, allocator liveness, and lower-layer media behavior.
1313. **small reference/control metadata can have large retention consequences** — a snapshot root or hold/user-reference state can keep a much larger set of payload blocks non-reclaimable.
1314. **historical retention ≠ historical currentness** — a snapshot can remain readable while the live dataset advances; rollback is the separate act that can reselect an older state as current.
1315. **rollback ≠ recovery of discarded newer state** — rollback changes currentness authority by discarding later logical changes, not by reconstructing them.
1316. **reference retirement ≠ secure sanitization** — destroying a last snapshot may make blocks free/reusable without proving immediate overwrite or erasure of every physical embodiment.
1317. **WAFL 1994 is prior art for COW filesystem snapshots ≠ proven WAFL→ZFS genealogy** — chronological/functional precedence blocks a ZFS-first claim but does not prove direct inheritance.
1318. **retention cost can be deferred into future divergence and reclamation work** — nearly instantaneous snapshot creation can create long-lived space/accounting obligations that become visible only as the live tree changes.
'''
)
