# Synthesis 08 — Proactive Integrity Verification, Defect Discovery, and Restored Repair Margin

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

## Distributed replica-integrity lifecycle addendum

The roadmap also asked a narrower distributed-storage question:

> How should `version currentness`, `checksum validity`, `demand-time versus idle-time discovery`, `fallback read availability`, `valid-replica count`, `clone repair`, and `restored replication goal` be separated?

The already-grounded GFS and HDFS cases supply a direct answer, while Ceph supplies the counterexample that prevents checksum metadata from being treated as unquestionable truth. This subsection therefore **deepens this existing synthesis instead of creating another near-duplicate synthesis document**.

### Version/currentness is not checksum validity

GFS Case 26 gives the cleanest historical split. Chunk version numbers exclude stale replicas from ordinary service; per-replica checksums separately qualify the contents of a replica that belongs to the expected version. HDFS Case 83 similarly separates Blockreport/inventory presence from later checksum verification. A physical copy can therefore be present yet inadmissible because it is stale, or current yet later rejected because its local integrity relation fails.

This yields a qualified-count rule:

```text
physical replica count
    != current-version replica count
    != integrity-qualified replica count
```

The last count is the one relevant to immediate repair opportunity under the bounded accidental-corruption model.

### Demand-time discovery is not idle/periodic discovery

GFS verifies checksum blocks before returning requested data and can also `scan and verify` inactive chunks during idle periods. HDFS documentation describes client-side checksum checking on retrieval, while the DataNode `BlockScanner` / `VolumeScanner` path deliberately reads replicas without an application request, under a rate-limited periodic/suspect-triggered maintenance regime.

The integrity relation may be the same kind of checksum relation, but the **trigger and timing of discovery differ**:

```text
demand-time verification
    -> defect is discovered because current service touched the replica

idle / periodic verification
    -> defect may be discovered before current service needs the replica
```

Background verification therefore changes the interval during which a latent defect can silently consume future repair margin. It does not prove that corruption happened during the scan, nor does a successful scan create permanent future validity.

### Fallback read availability is not repair completion

In GFS, a checksum mismatch can cause the requester to use another replica while the master separately arranges cloning from a valid source. HDFS likewise allows checksum failure on one replica to be bypassed by retrieving another copy while distributed control later handles re-replication.

So a successful request can occur in a degraded-but-serviceable state:

```text
one replica rejected
    -> another valid replica serves the read
    -> configured replication goal may still be unmet
    -> clone / re-replication remains pending
```

`read succeeded` therefore says less than `repair completed`, and both say less than `all intended replicas are again present and qualified`.

### Valid-replica count is a qualified count, not an inventory count

GFS explicitly warns that an inactive corrupted replica can make the master believe enough valid replicas exist until the defect is discovered. HDFS Case 79/83 provides the complementary inventory counterexample: a Blockreport can positively re-observe a block location without establishing that a later full checksum verification will succeed.

The system can consequently move through several different counts:

```text
inventoried / physically present replicas
        ↓ currentness filter
current-version replicas
        ↓ integrity qualification
currently acceptable repair/service sources
        ↓ clone / re-replication
restored configured replication goal
```

These counts can coincide in a healthy steady state, but they are not the same retained relation.

### Clone repair is not discovery, and restored goal is not revalidation of everything

GFS makes the ordering particularly explicit: after corruption is detected, another **valid replica** is used to create a replacement; only after the replacement exists does the master tell the server holding the corrupted copy to delete it. The clone consumes network/disk bandwidth and is throttled separately from ordinary service. HDFS's DataNode scanner similarly stops at verification/reporting; NameNode-directed re-replication is a later distributed action.

This gives a bounded lifecycle:

```text
currentness + integrity qualification
        ↓
defect discovery
        ↓
repair-source admissibility
        ↓
(optional) fallback service
        ↓
clone / re-replication
        ↓
configured replication goal restored
        ↓
future periodic verification remains necessary
```

The final line matters. Restoring the replica goal recreates multiplicity; it does not turn every embodiment into timelessly verified state. Later scans can still discover new corruption, and Ceph Case 27 shows that integrity metadata itself can require requalification.

### What this distributed addendum does not establish

This relation map does **not** establish that GFS, HDFS, Ceph, and ZFS share one repair implementation or historical lineage. It does not equate GFS `scan and verify` with the later historical term `scrub`, does not treat HDFS BlockScanner as the origin of distributed integrity maintenance, and does not turn checksum equality into a Byzantine-authenticity proof. It also does not collapse anti-entropy/version reconciliation into corruption detection: GFS itself explicitly notes that legal replicas can diverge, so bytewise equality is not its universal corruption criterion.

The bounded result is narrower: in distributed replicated storage, **currentness, integrity qualification, discovery timing, request fallback, qualified replica count, repair execution, and restored replication goal are separate retention relations even when a healthy system often makes them appear to move together**.

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
