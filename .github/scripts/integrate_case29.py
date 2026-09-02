from pathlib import Path


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    Path(path).write_text(text, encoding="utf-8")


def replace_once(text, old, new, label):
    if old not in text:
        raise RuntimeError(f"missing marker: {label}")
    return text.replace(old, new, 1)


# README
p = Path("README.md")
s = read(p)
case28 = "- [`cases/28-openstack-swift-tombstone-consistency-window.md`](cases/28-openstack-swift-tombstone-consistency-window.md) — grounded distributed-deletion bridge: Swift retains a timestamped `.ts` tombstone as the newest negative object state so deletion can propagate across divergent replicas; payload retirement, deletion convergence, and later tombstone reclamation remain separate retention events."
case29 = "- [`cases/29-ceph-luminous-ec-scrub-authoritative-repair.md`](cases/29-ceph-luminous-ec-scrub-authoritative-repair.md) — grounded scrub-repair-authority bridge: Luminous `v12.2.8` source separates scrub evidence, operational authoritative-candidate selection, missing-state injection, EC source filtering, `minimum_to_decode` sufficiency, and completed reconstruction; an auth candidate is explicitly not elevated to certainty of correct data."
if "cases/29-ceph-luminous-ec-scrub-authoritative-repair.md" not in s:
    s = replace_once(s, case28, case28 + "\n" + case29, "README case")
ev28 = "- [`evidence/28-openstack-swift-2016-tombstone-consistency-grounding.md`](evidence/28-openstack-swift-2016-tombstone-consistency-grounding.md) — Case-28 grounding record: Swift 2.10.1 release metadata, replication documentation, on-disk implementation, configuration, and unit tests separate timestamped negative currentness, asynchronous delete propagation, the consistency window, and age-gated tombstone reclamation without equating DELETE with secure erasure."
ev29 = "- [`evidence/29-ceph-luminous-2018-scrub-repair-grounding.md`](evidence/29-ceph-luminous-2018-scrub-repair-grounding.md) — Case-29 grounding record: tag-matched `v12.2.8` `PGBackend.cc`, `PG.cc`, and `ECBackend.cc` establish the source-level handoff from scrub-map error qualification to authoritative candidates, missing/location state, codec-level source filtering, `minimum_to_decode`, and EC reconstruction while preserving the implementation's explicit uncertainty boundary."
if "evidence/29-ceph-luminous-2018-scrub-repair-grounding.md" not in s:
    s = replace_once(s, ev28, ev28 + "\n" + ev29, "README evidence")
write(p, s)

# ROADMAP
p = Path("ROADMAP.md")
s = read(p)
if "cases/29-ceph-luminous-ec-scrub-authoritative-repair.md" not in s:
    s = replace_once(
        s,
        "partially advanced by grounded Cases 19, 23, 24, 25, 26, 27, and 28",
        "partially advanced by grounded Cases 19, 23, 24, 25, 26, 27, 28, and 29",
        "ROADMAP count",
    )
    marker = "The broad item stays unchecked because other mutable-EC consistency protocols, exact coded-shard scrub repair and authoritative-source selection, cross-region coded maintenance,"
    insert = "[`cases/29-ceph-luminous-ec-scrub-authoritative-repair.md`](cases/29-ceph-luminous-ec-scrub-authoritative-repair.md), grounded by [`evidence/29-ceph-luminous-2018-scrub-repair-grounding.md`](evidence/29-ceph-luminous-2018-scrub-repair-grounding.md), closes the bounded Luminous source-level handoff from scrub evidence to operational authoritative candidates, missing-state injection, filtered EC source availability, `minimum_to_decode`, and reconstruction while preserving the code's explicit uncertainty about whether an operational auth candidate is objectively correct. The broad item stays unchecked because other mutable-EC consistency protocols, cross-region coded maintenance,"
    s = replace_once(s, marker, insert, "ROADMAP paragraph")
write(p, s)

# CASE_INDEX
p = Path("CASE_INDEX.md")
s = read(p)
row28 = "| [OpenStack Swift Tombstones: Deletion as Retained Negative State and Consistency-Window Reclamation](cases/28-openstack-swift-tombstone-consistency-window.md) | **grounded** | timestamped negative object state + replica divergence + asynchronous propagation + age-gated tombstone reclamation | show deletion can require retained control state; separate local absence, distributed negative currentness, payload retirement, and tombstone retirement | [2016 Swift tombstone grounding](evidence/28-openstack-swift-2016-tombstone-consistency-grounding.md); later Swift reclaim/versioning semantics, account/container deletion, expiration, and secure erasure remain separate work |"
row29 = "| [Ceph Luminous Scrub Repair: Authoritative-Shard Selection, Missing-State Injection, and EC Reconstruction](cases/29-ceph-luminous-ec-scrub-authoritative-repair.md) | **grounded** | scrub-map evidence + ObjectInfo/HashInfo/version state + per-shard errors + authoritative candidate locations + PG missing state + EC shard indexes/decoder | separate operational repair authority from certainty, scrub candidate sets from codec-minimum decode sets, diagnosis from missing-state injection, and recovery scheduling from reconstruction completion | [2018 Luminous scrub-repair grounding](evidence/29-ceph-luminous-2018-scrub-repair-grounding.md); later Ceph scrub-backend refactors, automatic-repair policy, runtime failure-matrix experiments, and cross-version continuity remain separate work |"
if "Ceph Luminous Scrub Repair: Authoritative-Shard Selection" not in s:
    s = replace_once(s, row28, row28 + "\n" + row29, "CASE_INDEX row")

old27 = "[2017–2018 Ceph Luminous EC scrub grounding](evidence/27-ceph-luminous-2017-2018-ec-scrub-grounding.md); exact Luminous per-shard scrub-repair selection, later BlueStore checksum evolution, and modern auto-repair remain separate work"
new27 = "[2017–2018 Ceph Luminous EC scrub grounding](evidence/27-ceph-luminous-2017-2018-ec-scrub-grounding.md); exact `v12.2.8` scrub-repair source selection is now handled separately in Case 29, while later BlueStore checksum evolution and modern auto-repair remain separate work"
if old27 in s:
    s = s.replace(old27, new27, 1)

matrix28 = "| OpenStack Swift tombstones / 2016 bounded regime | object identity + timestamped `.ts` negative state + older positive embodiments + ring/sync/reclaim policy | tombstone creation; asynchronous replication/reconstruction; handoff/sync; age-gated reclamation | lookup/currentness selection treats a newer tombstone as deletion and suppresses older data; the negative state itself can later be reclaimed | object name → policy/ring → candidate nodes → timestamped local state kind → newest admissible state | stale positive embodiments may survive temporarily while the logical object is deleted; the tombstone itself later disappears after reclamation | no payload history by default; current deletion/version state is retained long enough to converge and suppress stale replicas |"
matrix29 = "| Ceph Luminous scrub repair / 2018 bounded regime | mutable EC object/shards + ObjectInfo/version + EC HashInfo + per-shard scrub errors + authoritative candidates + missing/location state + decoder inputs | scrub comparison; candidate exclusion/ranking; repair-mode missing-state injection; filtered EC recovery reads; `minimum_to_decode`; reconstruction | scrub can classify a present shard as unusable; `repair_object` records it missing before the EC backend later gathers sufficient usable shard indexes and decodes | object → scrub maps → selected auth ObjectInfo/version → authoritative candidates → missing/location maps → available shard indexes → code-minimum decode set | a bad physical shard can remain present while being administratively excluded, then be replaced by reconstructed content; operational source authority can change as new read errors appear | no complete history; current version plus negative missing/error state, candidate locations, shard-index identity, and recovery progress are retained |"
if "Ceph Luminous scrub repair / 2018 bounded regime" not in s:
    s = replace_once(s, matrix28, matrix28 + "\n" + matrix29, "CASE_INDEX matrix")

if "262. **scrub-authoritative candidate set ≠ EC minimum decode set**" not in s:
    findings = """262. **scrub-authoritative candidate set ≠ EC minimum decode set** — Luminous `v12.2.8` first constructs repair candidates from scrub/ObjectInfo/error evidence, then the EC backend separately asks `minimum_to_decode` for a coding-sufficient subset of currently usable shard indexes. Operational admissibility and algebraic sufficiency are different retained relations.
263. **operational repair authority ≠ certainty of correct payload** — the implementation itself warns that an auth shard can reach the repair-candidate path without the system knowing that it has the \"correct\" data. `authoritative` is therefore a procedural role under available evidence, not proof of objective truth.
264. **primary preference ≠ unconditional source authority** — `be_select_auth_object()` scans the primary first so it wins otherwise-equal ties, but recorded shard errors disqualify it and higher object versions outrank it. Physical/topological role and repair-source admissibility remain distinct.
265. **integrity diagnosis ≠ recovery-state transition** — scrub comparison identifies missing/inconsistent peers; `repair_object()` then mutates `peer_missing`/local missing and `missing_loc` so ordinary recovery treats the diagnosed bad shard as reconstructable missing state. Detection alone does not schedule the same work as missing-state injection.
266. **physical shard presence ≠ decode-source availability** — EC recovery excludes shards marked missing or newly reported in `error_shards`; a physically present shard can therefore cease to count as a possible decode input without first disappearing from the medium.
267. **planned decode source set ≠ stable source set** — read failures can add new `error_shards`, force recomputation of available indexes, and invoke `minimum_to_decode` again. Retained repair-source relations can change during the repair attempt itself.
268. **repair bookkeeping ≠ reconstructed redundancy** — calling `repair_object()` and recording missing/source locations precede successful EC reads, `ECUtil::decode`, and installation. A PG can know what must be repaired before the missing coded contribution has actually been restored.
269. **negative repair state is constitutive of coded retention** — `missing`, inconsistent/error flags, and excluded-source information are not payload, yet they prevent bad embodiments from participating in reconstruction and guide the system toward a surviving admissible decode set.
270. **Ceph Luminous scrub repair ≠ GFS replica cloning ≠ Swift EC cohort admissibility** — all qualify distributed repair state, but GFS selects whole valid replicas, Swift selects a committed same-version coded cohort, and Luminous here converts scrub evidence into candidate authority/missing state before codec-level minimum decoding. The comparison is functional, not one protocol genealogy.

"""
    s = replace_once(s, "These are provisional cross-case findings, not final philosophical conclusions.", findings + "These are provisional cross-case findings, not final philosophical conclusions.", "findings")

s = s.replace("After twenty-nine bounded cases, **all twenty-nine cases are now `grounded`.**", "After thirty bounded cases, **all thirty cases are now `grounded`.**", 1)
s = s.replace("currently twenty-nine;", "currently thirty;", 1)
s = s.replace("twenty-nine grounded regimes now support", "thirty grounded regimes now support", 1)
s = s.replace("and Swift distributed-delete/tombstone-consistency bridges;", "Swift distributed-delete/tombstone-consistency, and Ceph Luminous scrub-repair-authority bridges;", 1)
write(p, s)
