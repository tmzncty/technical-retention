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
case29 = "- [`cases/29-ceph-luminous-ec-scrub-authoritative-repair.md`](cases/29-ceph-luminous-ec-scrub-authoritative-repair.md) — grounded scrub-repair-authority bridge: Luminous `v12.2.8` source separates scrub evidence, operational authoritative-candidate selection, missing-state injection, EC source filtering, `minimum_to_decode` sufficiency, and completed reconstruction; an auth candidate is explicitly not elevated to certainty of correct data."
case30 = "- [`cases/30-nvme14-pmr-persistence-barriers.md`](cases/30-nvme14-pmr-persistence-barriers.md) — grounded NVMe 1.4 persistent-memory-region bridge: the optional PCIe PMR separates Posted-write completion from persistence barriers, interface persistence from implementation-specific nonvolatile staging, readiness from restored-content continuity, and request completion from valid read/write semantics."
if "cases/30-nvme14-pmr-persistence-barriers.md" not in s:
    s = replace_once(s, case29, case29 + "\n" + case30, "README case")

ev29 = "- [`evidence/29-ceph-luminous-2018-scrub-repair-grounding.md`](evidence/29-ceph-luminous-2018-scrub-repair-grounding.md) — Case-29 grounding record: tag-matched `v12.2.8` `PGBackend.cc`, `PG.cc`, and `ECBackend.cc` establish the source-level handoff from scrub-map error qualification to authoritative candidates, missing/location state, codec-level source filtering, `minimum_to_decode`, and EC reconstruction while preserving the implementation's explicit uncertainty boundary."
ev30 = "- [`evidence/30-nvme14-2019-pmr-grounding.md`](evidence/30-nvme14-2019-pmr-grounding.md) — Case-30 grounding record: the ratified 10 June 2019 NVMe 1.4 specification and NVM Express change record ground PMR introduction, cross-reset/disable persistence, implementation-specific nonvolatile staging, elasticity buffering, read-based persistence barriers, restore/health status, and not-ready completion semantics."
if "evidence/30-nvme14-2019-pmr-grounding.md" not in s:
    s = replace_once(s, ev29, ev29 + "\n" + ev30, "README evidence")
write(p, s)


# ROADMAP
p = Path("ROADMAP.md")
s = read(p)
if "cases/30-nvme14-pmr-persistence-barriers.md" not in s:
    s = replace_once(
        s,
        "partially advanced by grounded Cases 15 and 20",
        "partially advanced by grounded Cases 15, 20, and 30",
        "ROADMAP SSD case count",
    )
    marker = "The broad item stays unchecked because later NVMe persistence-domain terminology/revision history, controller-metadata recovery, enterprise PLP qualification, named-controller fault compliance, and filesystem/database composition remain distinct regimes;"
    insertion = "[`cases/30-nvme14-pmr-persistence-barriers.md`](cases/30-nvme14-pmr-persistence-barriers.md), grounded by [`evidence/30-nvme14-2019-pmr-grounding.md`](evidence/30-nvme14-2019-pmr-grounding.md), adds a later interface regime in which a PCIe Persistent Memory Region persists across specified power/reset/disable transitions while Posted-write completion, read-based persistence barriers, readiness/restore health, and implementation-specific nonvolatile staging remain separate relations. The broad item stays unchecked because exact later NVMe `persistence domain` terminology/revision history beyond this PMR slice, controller-metadata recovery, enterprise PLP qualification, named-controller fault compliance, and filesystem/database composition remain distinct regimes;"
    s = replace_once(s, marker, insertion, "ROADMAP Case 30 paragraph")
write(p, s)


# CASE_INDEX
p = Path("CASE_INDEX.md")
s = read(p)
row29 = "| [Ceph Luminous Scrub Repair: Authoritative-Shard Selection, Missing-State Injection, and EC Reconstruction](cases/29-ceph-luminous-ec-scrub-authoritative-repair.md) | **grounded** | scrub-map evidence + ObjectInfo/HashInfo/version state + per-shard errors + authoritative candidate locations + PG missing state + EC shard indexes/decoder | separate operational repair authority from certainty, scrub candidate sets from codec-minimum decode sets, diagnosis from missing-state injection, and recovery scheduling from reconstruction completion | [2018 Luminous scrub-repair grounding](evidence/29-ceph-luminous-2018-scrub-repair-grounding.md); later Ceph scrub-backend refactors, automatic-repair policy, runtime failure-matrix experiments, and cross-version continuity remain separate work |"
row30 = "| [NVM Express 1.4 Persistent Memory Region: Posted Writes, Persistence Barriers, and Restore Health](cases/30-nvme14-pmr-persistence-barriers.md) | **grounded** | optional PCIe read/write persistent-memory region + implementation-specific nonvolatile staging + optional elasticity buffer + PMR write barriers + ready/error/health state | separate Posted-write completion, persistence qualification, final internal placement, readiness, restore continuity, and read-data validity; show a persistent interface can survive reset/disable without making every completed access valid or every implementation physically identical | [2019 NVMe 1.4 PMR grounding](evidence/30-nvme14-2019-pmr-grounding.md); exact later `persistence domain` terminology, named-controller implementations, host PMEM programming models, and filesystem/database composition remain separate work |"
if "NVM Express 1.4 Persistent Memory Region: Posted Writes" not in s:
    s = replace_once(s, row29, row29 + "\n" + row30, "CASE_INDEX row")

old20 = "[2011 NVMe 1.0 grounding](evidence/20-nvme10-2011-flush-fua-grounding.md); later `persistence domain` terminology/revisions, named-controller implementation/compliance, and filesystem/database composition remain separate regimes"
new20 = "[2011 NVMe 1.0 grounding](evidence/20-nvme10-2011-flush-fua-grounding.md); later PMR persistence semantics are now handled separately in Case 30, while exact later `persistence domain` terminology/revisions, named-controller implementation/compliance, and filesystem/database composition remain separate regimes"
if old20 in s:
    s = s.replace(old20, new20, 1)

matrix29 = "| Ceph Luminous scrub repair / 2018 bounded regime | mutable EC object/shards + ObjectInfo/version + EC HashInfo + per-shard scrub errors + authoritative candidates + missing/location state + decoder inputs | scrub comparison; candidate exclusion/ranking; repair-mode missing-state injection; filtered EC recovery reads; `minimum_to_decode`; reconstruction | scrub can classify a present shard as unusable; `repair_object` records it missing before the EC backend later gathers sufficient usable shard indexes and decodes | object → scrub maps → selected auth ObjectInfo/version → authoritative candidates → missing/location maps → available shard indexes → code-minimum decode set | a bad physical shard can remain present while being administratively excluded, then be replaced by reconstructed content; operational source authority can change as new read errors appear | no complete history; current version plus negative missing/error state, candidate locations, shard-index identity, and recovery progress are retained |"
matrix30 = "| NVM Express PMR / 2019 bounded regime | host-visible PMR bytes + PCIe/controller address ranges + implementation-specific nonvolatile persistence mechanism + optional elasticity-buffer state + ready/error/health status | direct PCIe memory reads/writes; implementation-specific persistence handoff; PMR read-based write barrier; enable/disable save/restore; optional health polling | prior Posted writes require a supported barrier relation to establish completed-and-persistent status; not-ready reads can complete with undefined data and not-ready writes can complete without updating memory | BAR/PCIe range → PMR offset; optional controller address range → same offset; status/barrier state qualifies whether bytes are ready, valid, and persistent | PMR contents persist across specified power/reset/disable transitions while implementation may move bytes through nonvolatile staging; enable/disable can temporarily make persistent content unavailable | no complete history; current PMR bytes plus barrier completion, readiness, error, and health relations are retained; Restore Error can break continuity with prior-cycle contents |"
if "NVM Express PMR / 2019 bounded regime" not in s:
    s = replace_once(s, matrix29, matrix29 + "\n" + matrix30, "CASE_INDEX matrix")

if "271. **persistent interface contract ≠ fixed physical substrate**" not in s:
    findings = """271. **persistent interface contract ≠ fixed physical substrate** — NVMe 1.4 PMR explicitly permits the persistence guarantee to be realized either by completed nonvolatile-memory placement or by a nonvolatile write buffer that is transferred to nonvolatile memory later. The host-visible guarantee underdetermines the internal embodiment.
272. **Posted-write issue/completion ≠ persistence-barrier completion** — `PMRCAP.PMRWBM` exposes read-based mechanisms whose completion establishes that earlier Posted PCIe writes to PMR have completed and are persistent. Issuing ordinary memory writes and establishing their persistence are different interface relations.
273. **persistent write ≠ final internal placement** — the PMR contract can be satisfied by nonvolatile buffered state before a later transfer to nonvolatile memory, so persistence at the interface does not imply that the bytes already occupy their final internal location.
274. **PMR ready ≠ prior contents restored correctly** — `PMRSTS.HSTS = Restore Error` permits a PMR that is operating and persistent while its contents may not match those from before the preceding power/reset/disable transition. Persistence capability and state continuity are separate.
275. **successful request completion ≠ valid recovery or mutation** — when PMR is not ready, reads may complete successfully with undefined values and writes may complete normally without updating memory. Completion must be qualified by interface state.
276. **persistence ≠ immediate availability** — contents may persist across disable/reset while saving/restoring takes time and `NRDY` gates ordinary PCIe memory service. Surviving state and currently callable state are different relations.
277. **persistent capability ≠ perpetual integrity/health authority** — `HSTS` and `ERR` can qualify reads, writes, and prior persistence after the region has been established; delayed health reporting or polling can leave an interval whose operations must be treated as potentially affected.
278. **NVMe PMR persistence ≠ NVMe namespace Flush/FUA semantics** — Case 20 uses queued namespace/LBA commands, VWC, Flush, FUA, and command completion; Case 30 uses memory-mapped PMR, Posted PCIe writes, read-based persistence barriers, and ready/restore/health state. The relation is functional, not a timeless single protocol.
279. **ordinary PMR disable ≠ sanitize-induced unrecoverability** — PMR disable is explicitly inside the persistence guarantee, while the not-ready behavior following sanitize must prevent recovery of previous user data from cache or nonvolatile media. Logical unavailability, retained disable-state continuity, and deliberate forgetting remain distinct.

"""
    s = replace_once(
        s,
        "These are provisional cross-case findings, not final philosophical conclusions.",
        findings + "These are provisional cross-case findings, not final philosophical conclusions.",
        "CASE_INDEX findings 271-279",
    )

s = s.replace(
    "After thirty bounded cases, **all thirty cases are now `grounded`.**",
    "After thirty-one bounded cases, **all thirty-one cases are now `grounded`.**",
    1,
)
s = s.replace("currently thirty;", "currently thirty-one;", 1)
s = s.replace("thirty grounded regimes now support", "thirty-one grounded regimes now support", 1)
s = s.replace(
    "Swift distributed-delete/tombstone-consistency, and Ceph Luminous scrub-repair-authority bridges;",
    "Swift distributed-delete/tombstone-consistency, Ceph Luminous scrub-repair-authority, and NVMe 1.4 persistent-memory-region bridges;",
    1,
)
write(p, s)
