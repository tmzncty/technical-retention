from pathlib import Path

CASE_PATH = Path("cases/109-amazon-s3-versioning-delete-marker-lifecycle.md")
EVIDENCE_PATH = Path("evidence/109-amazon-s3-2010-2014-versioning-lifecycle-grounding.md")
ROADMAP_PATH = Path("ROADMAP.md")
INDEX_PATH = Path("CASE_INDEX.md")

roadmap_bullet = '- [x] Amazon S3 Versioning delete-marker / noncurrent-version lifecycle boundary — [`cases/109-amazon-s3-versioning-delete-marker-lifecycle.md`](cases/109-amazon-s3-versioning-delete-marker-lifecycle.md), grounded by [`evidence/109-amazon-s3-2010-2014-versioning-lifecycle-grounding.md`](evidence/109-amazon-s3-2010-2014-versioning-lifecycle-grounding.md): AWS\'s 8 February / 16 March 2010 Versioning records establish version IDs and retained predecessor versions, while current service semantics make simple DELETE create a data-less current delete marker and keep older versions directly addressable; the 20 May 2014 lifecycle/versioning announcement plus current lifecycle contract separates current-version expiration, noncurrent-version permanent retirement, and expired-marker cleanup. This closes only the bounded `default-current visibility vs retained version history vs policy-driven reclamation` relation; internal S3 replication/consensus, physical erase/sanitization, Object Lock, cross-region replication, provider-independent comparison, and implementation fault validation remain open.'
index_row = '| [Amazon S3 Versioning: Delete Markers, Noncurrent Versions, and Lifecycle Reclamation](cases/109-amazon-s3-versioning-delete-marker-lifecycle.md) | **grounded** | versioned object identity + current/noncurrent relation + data-less delete-marker currentness + policy-driven old-version retirement | separate default-key visibility from historical-version recoverability, delete marker from payload erasure, noncurrentness from corruption, and lifecycle eligibility from physical sanitization | [2010–2014 + current-contract grounding](evidence/109-amazon-s3-2010-2014-versioning-lifecycle-grounding.md); internal replication topology, Object Lock, physical deletion, and provider-independent validation remain separate |'
findings = '''

## Case 109 — Amazon S3 Versioning findings

1681. **current key view ≠ only retained version** — one version can be current for ordinary key access while predecessor versions remain explicitly retrievable by `versionId`.
1682. **delete marker ≠ payload erasure** — a versioned DELETE can install a data-less current marker while older payload versions remain retained.
1683. **default GET `404` ≠ old-version unrecoverability** — when a delete marker is current, ordinary GET can return `404` while an explicitly named noncurrent payload version remains retrievable.
1684. **noncurrent ≠ invalid or corrupt** — noncurrentness follows supersession/current-version selection rather than integrity failure.
1685. **version ID ≠ physical location** — `versionId` selects a service-level historical version and does not expose disk, SSD, replica, or coding placement.
1686. **delete-marker identity ≠ data-bearing object version** — a marker has key/version identity and currentness semantics without becoming a replacement copy of the old payload.
1687. **delete-marker removal ≠ payload rewrite** — deleting the current marker by its version ID can re-expose a retained predecessor as current.
1688. **simple DELETE ≠ version-specific DELETE** — the former can insert a current delete marker; the latter removes one explicitly selected version from the service.
1689. **Lifecycle `Expiration` ≠ immediate destruction of the previous current payload version** — in a versioning-enabled bucket it can add a delete marker and leave the former current payload as noncurrent.
1690. **`NoncurrentVersionExpiration` ≠ current-version expiration** — current AWS lifecycle semantics assign these actions to different version classes.
1691. **noncurrent age ≠ original object age** — current AWS lifecycle semantics measure noncurrent age from the creation of the successor that displaced the version.
1692. **expired delete-marker cleanup ≠ noncurrent payload cleanup** — a marker can become cleanup-eligible as its own state class after other versions are gone.
1693. **policy eligibility ≠ physical sanitization completion** — S3 lifecycle or version deletion establishes service-level retirement, not proof of media overwrite, Flash erase, or cryptographic erasure.
1694. **Versioning ≠ immutable / WORM retention** — retaining predecessor versions does not itself establish Object Lock, legal hold, or immutable-retention semantics.
1695. **service-level version history ≠ disclosed physical replica history** — public Versioning semantics do not reveal the number, placement, or exact retirement timing of lower-level embodiments.
1696. **S3 delete marker ≠ Swift tombstone implementation** — Case 28 supplies a bounded functional analogy, but Swift's `.ts`, timestamp-convergence, replication, and `reclaim_age` mechanisms are not established for S3 and no genealogy is implied.
'''

for path in (CASE_PATH, EVIDENCE_PATH):
    if not path.exists():
        raise SystemExit(f"missing expected file: {path}")

roadmap = ROADMAP_PATH.read_text(encoding="utf-8")
if "cases/109-amazon-s3-versioning-delete-marker-lifecycle.md" not in roadmap:
    lines = roadmap.splitlines()
    idx = next((i for i, line in enumerate(lines) if line.startswith("- [ ] distributed replication and erasure coding beyond RADOS —")), None)
    if idx is None:
        raise SystemExit("ROADMAP distributed-storage anchor not found")
    lines.insert(idx, roadmap_bullet)
    ROADMAP_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

index = INDEX_PATH.read_text(encoding="utf-8")
if "cases/109-amazon-s3-versioning-delete-marker-lifecycle.md" not in index:
    lines = index.splitlines()
    idx = next((i for i, line in enumerate(lines) if "(cases/108-seagate-medalist-zone-bit-recording-geometry.md)" in line), None)
    if idx is None:
        raise SystemExit("CASE_INDEX Case 108 row anchor not found")
    lines.insert(idx + 1, index_row)
    index = "\n".join(lines) + "\n"

if "## Case 109 — Amazon S3 Versioning findings" not in index:
    if "1680. **Cases 14/89/108 form a layer decomposition" not in index:
        raise SystemExit("CASE_INDEX latest finding anchor not found")
    index = index.rstrip() + findings.rstrip() + "\n"
INDEX_PATH.write_text(index, encoding="utf-8")

checks = {
    CASE_PATH: ["**`grounded`**", "current version ≠ only retained version", "delete marker ≠ payload erasure", "Case 28", "20 May 2014"],
    EVIDENCE_PATH: ["**`grounded`**", "8 February 2010", "20 May 2014", "service-level permanent delete ≠ physical sanitization"],
    ROADMAP_PATH: ["Amazon S3 Versioning delete-marker / noncurrent-version lifecycle boundary", "cases/109-amazon-s3-versioning-delete-marker-lifecycle.md"],
    INDEX_PATH: ["Amazon S3 Versioning: Delete Markers, Noncurrent Versions, and Lifecycle Reclamation", "## Case 109 — Amazon S3 Versioning findings", "1681. **current key view ≠ only retained version**", "1696. **S3 delete marker ≠ Swift tombstone implementation**"],
}
for path, needles in checks.items():
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"validation failed in {path}: {needle}")
