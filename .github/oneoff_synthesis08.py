from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ROADMAP = ROOT / "ROADMAP.md"
INDEX = ROOT / "CASE_INDEX.md"
SYNTH = ROOT / "docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md"


def read(path):
    return path.read_text(encoding="utf-8")


def write(path, text):
    path.write_text(text, encoding="utf-8")


def insert_after_prefix_line(path, prefix, addition):
    text = read(path)
    assert addition.strip() not in text, f"addition already present in {path}"
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    assert len(hits) == 1, f"expected one prefix in {path}: {prefix!r}, got {len(hits)}"
    i = hits[0]
    lines[i + 1:i + 1] = ["", addition]
    write(path, "\n".join(lines) + ("\n" if text.endswith("\n") else ""))


def replace_exact_line(path, old_line, new_line):
    text = read(path)
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if line == old_line]
    assert len(hits) == 1, f"expected one exact line in {path}: {old_line!r}, got {len(hits)}"
    lines[hits[0]] = new_line
    write(path, "\n".join(lines) + ("\n" if text.endswith("\n") else ""))


def insert_before(path, anchor, addition):
    text = read(path)
    assert addition.strip() not in text, f"addition already present in {path}"
    assert text.count(anchor) == 1, f"expected one anchor in {path}: {anchor!r}"
    write(path, text.replace(anchor, addition + "\n\n" + anchor, 1))


assert not SYNTH.exists(), f"unexpected existing synthesis: {SYNTH}"
SYNTH.write_text(r'''# Synthesis 08 — Proactive Integrity Verification, Defect Discovery, and Restored Repair Margin

## Scope

This is a **bounded cross-case synthesis**, not a new historical case and not a genealogy of checksums, scrubbing, HDFS, GFS, Ceph, or ZFS.

It closes one relation-decomposition question already present in the roadmap:

> How should `physical presence`, `verified integrity`, `defect discovery`, `repairability`, and `restored redundancy` be separated in proactively checked storage?

The comparison is built only from already-grounded repository cases:

- [Case 18 — ZFS scrub / latent-error detection](../cases/18-zfs-scrub-latent-error-detection.md);
- [Case 26 — GFS inactive-chunk verification](../cases/26-google-gfs-inactive-chunk-integrity.md);
- [Case 27 — Ceph deep scrub / checksum authority](../cases/27-ceph-luminous-ec-deep-scrub-checksum-authority.md);
- [Case 29 — Ceph scrub-authoritative EC repair](../cases/29-ceph-luminous-ec-scrub-authoritative-repair.md);
- [Case 83 — HDFS DataNode block scanner](../cases/83-apache-hdfs-block-scanner-checksum-verification.md);
- [Case 96 — OpenZFS dRAID sequential reconstruction](../cases/96-openzfs-draid-distributed-spare-sequential-resilver.md).

Historical claims remain owned by those case/evidence records. This document adds a typed **engineering comparison (`E`)** across them. Functional similarities are marked as comparison only and do not establish genealogy.

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `scrub`, HDFS, Ceph, and related integrity-maintenance terms found no dedicated overlapping case in the current repository search surface. A broader history of checksum algorithms, disk scrubbing, storage-controller patrol reads, RAID verification, or distributed repair should live there if developed rather than being recreated here.

---

## Historical records kept separate

### GFS 2003 — currentness, checksums, idle verification, and clone-before-delete

The 2003 GFS paper distinguishes chunk-version currentness from per-replica checksum validity. A stale replica is excluded by version state; a current-version replica is still checked locally by checksum. During idle periods chunkservers may `scan and verify` inactive chunks so corruption can be found before ordinary demand. When a corrupt replica is found, the master can create a valid replacement from another valid replica and only then instruct deletion of the bad embodiment.

The bounded result is not that GFS invented scrubbing. Its own vocabulary is `scan and verify`, and Case 26 explicitly keeps later `scrub` terminology separate.

### ZFS 2004–2010 — proactive pool traversal and self-healing are not resilvering

Case 18 combines the 2004 disk-scrubbing prior-art anchor with Sun/Oracle ZFS documentation. ZFS checksums data and metadata; `zpool scrub` deliberately traverses pool data before applications necessarily request it; a bad block can be repaired when a trustworthy redundant source exists. The same documentation treats replacement-device resilvering as a different maintenance relation.

Thus proactive verification can expose a latent defect while the repair path still exists, but the scan itself is neither equivalent to a device failure nor to completed redundancy restoration.

### HDFS 2008–2016 — background verification has its own coverage state

Case 83 anchors a DataNode block scanner by 2008 and studies the Hadoop 2.7.3 `BlockScanner` / `VolumeScanner` path in detail. A block report establishes local presence, while periodic or suspect-triggered reads separately qualify content through checksums. The scanner can save traversal cursor state across restart and report a qualifying failure through `reportBadBlocks`; replacement replication remains a later distributed action.

This gives a particularly sharp distinction between **payload state**, **integrity evidence**, and **maintenance-progress state**.

### Ceph 2012 and Luminous 2017–2018 — mismatch can implicate the verifier

Case 27 establishes Ceph deep scrub in 2012 as content comparison across replicas, then separately studies Luminous BlueStore/EC integrity. The 12.2.6 regression is the counterexample that prevents `checksum mismatch` from becoming a universal synonym for `payload corruption`: stored integrity metadata could itself become inconsistent. The 12.2.7/12.2.8 workaround and repair sequence temporarily withdrew trust from the affected digest relation and used full deep-scrub coverage as part of returning that relation to service.

### Ceph Luminous 2018 — diagnosis must be converted into repair authority and recovery state

Case 29 follows the source-level path after scrub disagreement. Candidate shards can be excluded for read/stat/hash/size/info errors; an operational `authoritative` candidate set is selected under explicit rules; bad shards are injected into missing-state and source-location bookkeeping; only then does the EC backend compute a sufficient `minimum_to_decode` set and reconstruct missing state.

The source even preserves uncertainty that an operational auth candidate is not necessarily known to contain objectively `correct` data. Detection, source admissibility, mathematical sufficiency, and reconstruction therefore remain separate relations.

### OpenZFS dRAID 2021 — restored redundancy can precede renewed integrity confidence

Case 96 supplies the reverse ordering needed to avoid another collapse. Sequential dRAID reconstruction can restore the configured redundancy relation first; because that pass does not perform ordinary block-pointer checksum verification, a scrub follows by default. `redundancy restored` is therefore not the strongest possible integrity statement.

---

## Engineering reconstruction: ten typed relations

The following terms are project engineering vocabulary. They are not claimed as shared historical terminology.

### 1. Physical presence

An embodiment exists at an expected storage location or is positively inventoried.

Examples include an HDFS block appearing in a Blockreport or a GFS/Ceph replica/shard existing on a storage node. Presence is the weakest relation in this synthesis: it does not establish currentness, readability, or integrity.

### 2. Currentness / admissibility

Does the embodiment belong to the logical version or protocol state that is allowed to count now?

GFS chunk versions and Ceph object/version authority show that a physically intact older copy can be inadmissible before any checksum question is asked.

### 3. Integrity evidence

What retained relation is used to qualify bytes or structure?

Examples include GFS/HDFS checksums, ZFS block checksums, and BlueStore/checksum metadata. Integrity evidence is not another payload copy. It is retained control/evidence state whose own correctness may need protection and revalidation.

### 4. Verification coverage and age

Has the relevant embodiment actually been checked recently enough under the chosen maintenance policy?

A configured scrub interval, scanner cursor, or successful pass is evidence about **work performed**, not a timeless property of the medium. A block successfully verified at `t1` can fail at `t2`.

### 5. Defect discovery / inconsistency observation

A verification operation can reveal that an expected relation does not hold: checksum mismatch, read error, structural inconsistency, or other evidence.

Discovery is an epistemic/control transition. It does not by itself say which side of a comparison is wrong, whether another good source exists, or whether repair has started.

### 6. Diagnosis and source admissibility

Which surviving state is allowed to count as a repair source?

Case 29 is the strongest example: shards with particular error classes are excluded before an operational authority/candidate set is formed. GFS similarly requires a `valid replica`, while HDFS reporting can cause a local embodiment to stop counting as a usable replica.

### 7. Repairability

Given the surviving admissible sources, can the logical state still be reconstructed or copied?

This is weaker than `repair completed`. A system may discover corruption when no good source remains. Conversely, repairability may already exist before the latent defect is discovered.

### 8. Service fallback availability

Can ordinary demand still be served while one embodiment is rejected and repair remains pending?

GFS and HDFS can use another replica; ZFS may heal from redundancy. Service continuity can therefore precede restoration of the configured replication/redundancy goal.

### 9. Repair execution and restored redundancy

A clone, reconstruction, or replacement must actually materialize admissible current state. Only after enough replacement state is installed does the system regain the intended redundancy/replication margin.

`reportBadBlocks`, `repair_object()`, or a scrub mismatch are not that completion point.

### 10. Revalidation / return to trust

Even restored redundancy can be followed by stronger verification work. OpenZFS dRAID makes this explicit by restoring redundancy through sequential reconstruction before a later scrub verifies checksums. Ceph 12.2.8 likewise makes full verification coverage part of restoring trust in previously suspect integrity metadata.

---

## Compact relation map

```text
physical embodiment present / inventoried
        ↓
currentness / protocol admissibility
        ↓
integrity evidence available
        ↓
verification actually exercises that relation
        ↓
defect or inconsistency discovered
        ↓
diagnosis + repair-source admissibility
        ↓
repairability established
        ↓
(optional) fallback service continues
        ↓
repair / replacement / reconstruction executes
        ↓
configured redundancy or replication goal restored
        ↓
(optional/separate) wider integrity revalidation
```

This is a diagnostic decomposition, not one universal implementation pipeline. Some systems combine steps, omit them, or order them differently. Its use is to prevent words such as `healthy`, `verified`, `repair`, and `recovered` from standing in for several incompatible relations.

---

## Cross-case matrix

| Relation | GFS Case 26 | ZFS Case 18 | HDFS Case 83 | Ceph Cases 27/29 | dRAID Case 96 |
| --- | --- | --- | --- | --- | --- |
| physical presence | chunk replica exists | block exists in pool | local block / Blockreport presence | shard/object exists | surviving/rebuilt contributions exist |
| currentness filter | chunk version | filesystem/current block relation | generation/current dataset outside scanner slice | object/version + PG authority | current allocated/coded state |
| integrity evidence | per-64 KB checksum | filesystem checksum | stored checksum metadata | BlueStore / object / EC integrity metadata | later block-pointer checksums |
| proactive verification | idle `scan and verify` | `zpool scrub` | periodic + suspect scan | scrub/deep scrub | post-sequential-rebuild scrub |
| discovery result | corrupt replica report | bad block | verification failure + `reportBadBlocks` | mismatch/error/inconsistent shard | first phase can intentionally defer this layer |
| repair-source qualification | existing valid replica | trustworthy redundant copy | another good replica through distributed control | filtered auth/ok-peers + missing locations | surviving coded contributors |
| repair mechanism | clone valid replica | self-heal / separate resilver | later re-replication | missing-state injection + EC decode | sequential reconstruction |
| restoration milestone | replica goal restored | bad copy repaired / resilver completes | desired replication restored | reconstructed admissible shard/object state | coded redundancy restored |
| stronger later confidence | future checks still needed | later scrub can recheck | periodic rescanning renews observation | full deep-scrub can restore digest trust | explicit follow-up scrub |

The matrix is `A/E`: a functional comparison across independently grounded systems, not evidence of one lineage.

---

## Findings

### E — physical presence ≠ verified integrity

A replica can be positively inventoried and still fail a later checksum/read verification. HDFS Case 83 and GFS Case 26 make this distinction explicit.

### E — verification success is time-bounded evidence

A successful check records that a relation held when exercised. It does not confer permanent immunity from later media, metadata, or software failure. Periodic scanning exists because confidence ages.

### E — defect discovery ≠ fault localization

A mismatch says that an expected relation failed. Ceph's digest regression shows why it cannot automatically prove that payload bytes are the defective side rather than integrity metadata or maintenance logic.

### E — defect discovery ≠ repairability

Discovery can occur after all good repair sources are gone. Conversely, redundant repair capacity may exist for a long time before a latent fault is discovered. Proactive verification matters partly because it tries to exercise repair opportunity before it disappears.

### E — repairability ≠ restored redundancy

Having an admissible source or sufficient decode set means repair can proceed. It does not mean replacement state has been written or the configured replica/parity goal has been restored.

### E — service availability can precede repair completion

GFS/HDFS can fall back to another replica; parity/coded systems may reconstruct for demand. A successful current request therefore does not prove that future-failure margin is back to normal.

### E — restored redundancy ≠ full integrity revalidation

OpenZFS dRAID supplies a direct implementation counterexample: sequential reconstruction can restore redundancy before the follow-up checksum scrub. Repair-margin restoration and verification coverage are distinct milestones.

### E — integrity metadata has its own authority lifecycle

Checksums are retained and maintained state, not external truths. The Ceph 12.2.6–12.2.8 sequence shows that verification metadata can become suspect, be deliberately distrusted, and later be returned to trust through additional maintenance.

### E — verification-progress state ≠ verification result

An HDFS scanner cursor can preserve where a background traversal should resume. It helps sustain coverage but does not itself certify any unchecked block. Maintenance metadata can be retention infrastructure without being integrity evidence for the payload.

### E — valid-replica count is qualified, not merely physical

A system can physically hold several replicas while fewer count as current, integrity-valid repair sources. `copy count` and `repair margin` therefore should not be used interchangeably.

### E — proactive checking converts hidden-defect exposure into scheduled work, not certainty

Scrubbing/scanning spends I/O, time, energy, scheduling capacity, and control state to reduce the interval in which defects remain undiscovered. It does not eliminate all fault classes, prove cryptographic authenticity, or guarantee a repair source will still exist when a defect is found.

---

## Relationship to Synthesis 07

[Synthesis 07](SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md) asks what happens **after a failure/exposure relation is known** in coded storage: reconstructability, degraded service, repair scope, reconstruction geometry, restored redundancy, and later integrity validation.

This synthesis moves one step upstream and sideways: **how does a system know that a physically present embodiment should stop counting, and what evidence turns latent corruption into qualified repair work?**

The overlap at `restored redundancy → later verification` is intentional. It is the seam between the two analyses, not a duplicate conclusion.

---

## What must not be inferred

This synthesis does **not** establish:

- that GFS `scan and verify`, ZFS scrub, HDFS BlockScanner, and Ceph deep scrub share one implementation lineage;
- that any one checksum detects every corruption or proves authenticity;
- that replica equality is a universal integrity test;
- that a checksum mismatch always identifies bad payload bytes;
- that a successful scan proves future integrity;
- that reporting a bad replica means a replacement has already been created;
- that fallback read availability means the replication goal is restored;
- that restored redundancy means every reconstructed block has been checksum-verified;
- that scan cursor/progress state is itself a payload-integrity certificate;
- that one scalar `health` value can replace presence, currentness, verification, repairability, service, redundancy, and confidence state.

---

## Philosophical boundary

`I` — These cases support a narrow claim that technical retention can depend on **renewed qualification of survivors**, not only on keeping physical embodiments in existence. What persists operationally is partly a relation saying which survivor is still allowed to count.

`I` — That does not make verification the essence of all retention. Passive magnetic/positional cases elsewhere in the repository remain counterexamples to a universal `to persist is to be continuously verified` thesis. This synthesis is bounded to systems that deliberately maintain integrity evidence and proactive checking paths.

No philosophical vocabulary is attributed to the historical engineers or system authors.

---

## Source ownership and next work

Historical source locations and evidence grades remain in the case/evidence records linked above; this synthesis deliberately avoids duplicating their bibliographies.

Still-open work includes:

- storage-controller patrol-read / media-scrub genealogy and named-controller behavior;
- checksum collision/authenticity limits under adversarial rather than accidental-corruption models;
- URE and correlated-failure policy under real rebuild workloads;
- independent production fault-injection evidence for scanner starvation, repair-source loss, and post-repair revalidation;
- distributed scrub coordination where different replicas complete verification at different times;
- integrity-metadata corruption beyond the bounded Ceph incident;
- a broader historical treatment in `computing-archaeology` if that repository develops a checksum/scrub/repair-maintenance track.

Those are additional research slices, not blockers for the bounded relation decomposition completed here.
''', encoding="utf-8")

insert_after_prefix_line(
    README,
    "A bounded coded-storage recovery comparison is now available in [`docs/SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md`]",
    "A bounded proactive-integrity comparison is now available in [`docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md`](docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md). Across grounded GFS, ZFS, HDFS, Ceph, and OpenZFS cases it separates physical presence, currentness/admissibility, integrity evidence, verification coverage, defect discovery, repair-source qualification, repairability, fallback service, restored redundancy, and later revalidation."
)

insert_before(
    ROADMAP,
    "Coordinate with `computing-archaeology` rather than duplicating it.",
    "- [x] Proactive-integrity / defect-discovery / repair-margin synthesis — [`docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md`](docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md) closes the bounded relation-decomposition question across grounded Cases 18, 26, 27, 29, 83, and 96. It separates physical presence, version/currentness admissibility, retained integrity evidence, verification coverage/age, mismatch discovery, diagnosis/source admissibility, repairability, fallback service, repair execution, restored redundancy, and later revalidation. This is cross-case engineering synthesis, not a scrub/checksum genealogy; controller patrol-read history, adversarial integrity, correlated failures, cross-node scan coordination, and field fault injection remain open."
)

replace_exact_line(
    ROADMAP,
    "- [ ] How should `physical presence`, `verified integrity`, `defect discovery`, `repairability`, and `restored redundancy` be separated in proactively checked storage?",
    "- [x] In proactively checked storage, separate `physical presence`, `currentness/admissibility`, `integrity evidence`, `verification coverage/age`, `defect discovery`, `diagnosis/source admissibility`, `repairability`, `fallback service availability`, `repair execution`, `restored redundancy`, and later `integrity revalidation` — closed at the bounded cross-case level by [`docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md`](docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md), synthesizing grounded Cases 18, 26, 27, 29, 83, and 96. Controller patrol-read history, checksum/authenticity limits, correlated failures, production fault injection, and distributed scan coordination remain separate work."
)

replace_exact_line(
    ROADMAP,
    "- [ ] latent integrity defect remaining undiscovered until another failure removes the available repair path;",
    "- [ ] latent integrity defect remaining undiscovered until another failure removes the available repair path — **partially advanced by Synthesis 08 and grounded Cases 18, 26, 83, 27, and 29**: proactive scan/scrub can move discovery before demand, but physical presence, currentness, verification coverage, diagnosis, repair-source admissibility, and restored redundancy remain distinct relations. Device/media fault physics, correlated failures, scan starvation, independent fault injection, and adversarial integrity remain open;"
)

insert_after_prefix_line(
    INDEX,
    "1372. **cross-case recovery pipeline ≠ historical genealogy**",
    """### Cross-case proactive-integrity synthesis — presence, verification, discovery, and repair margin\n\n1373. **physical presence ≠ verified integrity** — a replica or block can be positively inventoried yet fail a later checksum/read verification; presence is not an integrity certificate.\n1374. **successful verification at `t1` ≠ integrity at `t2`** — a scan records a bounded observation under one failure model, while later media, metadata, or software faults can invalidate that relation; verification confidence therefore has age.\n1375. **defect discovery ≠ fault localization** — a checksum or structural mismatch establishes inconsistency but need not identify whether payload, integrity metadata, or another maintained relation is the defective side.\n1376. **defect discovery ≠ repairability** — a bad embodiment can be discovered after all good sources are gone, while repair capacity can conversely exist before a latent defect has been exercised by verification.\n1377. **repairability ≠ restored redundancy** — an admissible source replica or sufficient decode set makes replacement possible; configured replica/parity margin returns only after replacement state is materialized.\n1378. **fallback service availability ≠ repair completion** — another replica or on-demand reconstruction can satisfy present reads while repair remains pending and future-failure margin is still reduced.\n1379. **restored redundancy ≠ full integrity revalidation** — OpenZFS dRAID can restore coded redundancy through sequential reconstruction before a later checksum scrub supplies stronger verification coverage.\n1380. **checksum mismatch ≠ universal proof of payload corruption** — Ceph Luminous supplies a concrete counterexample in which retained digest metadata became inconsistent and its authority had to be temporarily withdrawn and repaired.\n1381. **verification-progress state ≠ verification result** — an HDFS scanner cursor can preserve maintenance coverage progress across restart without certifying blocks that have not yet been checked.\n1382. **physical replica count ≠ integrity-qualified repair margin** — version/currentness filters, checksum validity, read errors, and operational authority can make only a subset of surviving embodiments admissible as future repair sources.\n1383. **proactive checking ≠ timeless certainty or one historical lineage** — scan/scrub shifts hidden-defect discovery into scheduled maintenance work, but it neither proves every fault class nor makes GFS, ZFS, HDFS, Ceph, and OpenZFS one mechanism or genealogy."""
)
