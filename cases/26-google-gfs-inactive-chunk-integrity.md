# Google File System Inactive-Chunk Verification: Checksums, Valid Replicas, and Background Repair

## Scope

- **Bounded system:** the Google File System (GFS) as documented by Ghemawat, Gobioff, and Leung at SOSP 2003.
- **Bounded mechanism:** chunk-version filtering, per-64 KB block checksums, verification before read return, idle-period scanning of inactive chunks, corruption reporting, alternate-replica reads, and master-coordinated re-replication from a valid replica.
- **Primary source base:** the 2003 GFS paper preserved by Google Research.
- **Research question:** when replication already exists, what additional retained relations and maintenance work are required to know that replicas counted toward future recovery are both current enough and integrity-valid?

This is **not** a general history of GFS, Google infrastructure, distributed filesystems, checksums, replication, or scrubbing. It does not claim that Google invented checksumming, replicated storage, background verification, or the later term `scrub`.

The bounded retention claim is:

> **Replica multiplicity does not by itself establish a trustworthy repair margin. In 2003 GFS, chunk version numbers exclude stale replicas while per-replica checksums independently qualify stored data; demand-time verification and idle-period scanning can discover corruption, after which the system restores a valid replica count by cloning from another valid copy and only then deletes the corrupted embodiment.**

`integrity-qualified replica`, `repair margin`, `proactive integrity scan`, and `currentness filter` below are **project engineering terms**, not historical GFS vocabulary.

---

## Historical vocabulary

The 2003 paper directly uses `chunk`, `chunkserver`, `replica`, `valid replica`, `replication goal`, `chunk version number`, `stale replica`, `checksum`, `checksum block`, `32 bit checksum`, `corruption`, `clone`, `re-replicate`, `scan and verify`, and `inactive chunks`.

The paper does **not** call the idle verification operation `scrubbing`. This case preserves `scan and verify` as the period phrase and uses `proactive integrity scan` only as a modern functional description.

---

## Historical record

### H/P — version currentness and integrity are separate mechanisms

Section 4.5 uses chunk version numbers to distinguish up-to-date replicas from stale replicas. Stale replicas are not returned to clients and are treated as nonexistent for normal service pending garbage collection. Section 5.2 separately treats post-write corruption as a checksum-detected failure class.

The source therefore requires two different questions:

```text
Is this replica from the current chunk version?
Is this replica's stored content still integrity-valid?
```

**Primary anchors:** Ghemawat, Gobioff, and Leung 2003, §§4.5, 5.2.

### H/P — re-replication restores a configured replica goal

Section 4.3 says the master re-replicates a chunk when available replicas fall below a user-specified goal. Causes include an unavailable chunkserver, a replica reported as possibly corrupted, a disabled disk, or an increased replication goal. The master instructs a destination to copy from an existing **valid replica**.

Clone work is explicitly budgeted: the master limits active clone operations and chunkservers throttle clone-read bandwidth to avoid overwhelming client traffic.

**Primary anchor:** §4.3.

### H/P — bytewise replica equality is not the corruption test

Section 5.2 says replica comparison would be impractical and, more importantly, that divergent replicas can be legal because GFS mutation semantics—especially atomic record append—do not guarantee identical replicas. Each chunkserver therefore independently verifies its own copy with checksums.

This gives a strong negative rule:

> **replica divergence is not by itself evidence of corruption.**

**Primary anchor:** §5.2 `Data Integrity`.

### H/P — checksum metadata is separately retained control state

A chunk is divided into 64 KB blocks, each with a corresponding 32-bit checksum. Checksums are kept in memory and stored persistently with logging, separately from user data.

The checksum is not payload, yet later service and repair depend on the relation between data and its recorded checksum.

**Primary anchor:** §5.2.

### H/P — reads verify before returning data

Before returning requested data, a chunkserver verifies checksums for blocks overlapping the read range. On mismatch it returns an error and reports the mismatch to the master. The requester can read another replica while the master clones the chunk from another replica. Only **after a valid new replica is in place** does the master instruct the server holding the corrupted replica to delete it.

**Primary anchor:** §5.2.

### H/P — inactive chunks can be verified before ordinary demand

During idle periods chunkservers can `scan and verify` inactive chunks. The paper states that this finds corruption in rarely read chunks; after detection the master can create a new uncorrupted replica and delete the bad one. Its explicit reason is to prevent an inactive corrupted replica from fooling the master into thinking that enough valid replicas exist.

**Primary anchor:** §5.2.

---

## Retained state

The bounded mechanism retains more than user bytes:

1. **chunk payload** — file data embodied in replicas;
2. **chunk version number** — currentness state used to exclude stale replicas;
3. **per-block checksum** — integrity state for each 64 KB checksum block;
4. **replica-location and replication-goal state** — enough control state to identify under-replication and select repair work;
5. **failure/integrity observations** — unavailability, possible corruption, disabled disks, and checksum mismatches change which embodiments may count;
6. **repair/placement control state** — cloning destinations, rack distribution, prioritization, and throttling govern restoration of redundancy.

---

## Retention mechanism

### Ordinary service

A read resolves a chunk to candidate replicas and a chosen chunkserver verifies relevant checksum blocks before returning data.

### Currentness filtering

Chunk version numbers keep stale replicas out of normal service. This is logically distinct from checksum validation of a replica with the expected version.

### Proactive discovery

During idle periods a chunkserver can scan inactive chunks, exercising checksum relations before an application requests those blocks.

### Repair

Detection can cause the master to clone from an existing valid replica. The corrupt embodiment is removed after a valid replacement exists.

### Redundancy restoration

Usable copies are compared with a replication goal. A client can remain served by another replica while full intended redundancy is still being repaired.

---

## Addressing and access geometry

A bounded recovery path is:

```text
file + byte offset
    -> chunk handle
    -> current chunk version
    -> candidate replica location
    -> per-block checksum verification
    -> return data
       OR reject/report corrupt replica
    -> alternate valid replica
    -> master-coordinated clone
    -> restored replica count / placement
```

Physical location alone does not establish the retained object. Version and integrity relations qualify whether a surviving copy may answer or serve as a repair source.

---

## Read / write semantics

A normal read is **integrity-qualified before return**. If a local copy fails, service can continue from another replica while repair proceeds separately.

Checksums are also maintained through writes. The paper says append-heavy writes can update checksums incrementally; overwriting an existing range requires verifying boundary checksum blocks before the write so a new checksum cannot hide old corruption in untouched bytes.

This case does not generalize those details into a universal checksum algorithm.

---

## Time, maintenance, and labor

Relevant timescales include immediate read-time verification, potentially long delay before rare data is demanded, opportunistic idle-period verification, the interval between discovery and completed cloning, and longer placement/rebalancing intervals.

Retention depends on background work: checksum persistence/verification, idle scans, error reporting, master prioritization, network/disk cloning, deletion of known-corrupt embodiments, rack-aware placement, and bandwidth/concurrency throttling. `Background` therefore does not mean `free` or `optional`.

These are not DRAM-style physical refresh deadlines. Their triggers are demand-, idleness-, failure-, workload-, and policy-dependent.

---

## Failure / forgetting modes

Keep distinct:

- stale-version replica;
- checksum-invalid/corrupted replica;
- unavailable chunkserver or disabled disk;
- insufficient usable replicas relative to the goal;
- legal byte divergence among replicas under GFS mutation semantics;
- rarely read corruption remaining undiscovered until demand or idle verification;
- loss of all valid repair sources;
- loss/corruption of version, checksum, or other control metadata.

The last item is an engineering boundary: the paper makes the metadata operationally necessary, but this case does not invent a complete recovery protocol for every metadata-loss combination.

---

## Engineering reconstruction

### E — replica multiplicity is weaker than verified repair margin

Several physical copies do not automatically mean several safe repair sources. GFS itself warns that an inactive corrupted replica can make the master think it has enough valid replicas until the defect is discovered.

### E — currentness and integrity are orthogonal filters

A version number asks whether a replica belongs to the expected logical generation. A checksum asks whether local stored data still matches its integrity metadata. One mechanism cannot substitute for the other.

### E — discovery timing is part of retention risk

Redundancy may already be sufficient to repair a latent defect while the opportunity remains unexercised until verification occurs. Idle scanning shortens the period during which hidden corruption silently consumes repair margin.

### E — fallback availability can precede repair completion

A requester can use another copy after a checksum error while a master-directed clone remains pending. `good read available ≠ replication goal restored`.

### E — validity is not a replica-equality vote

Because legal GFS mutations can yield divergent replicas, current integrity is not established by simple equality comparison. It depends on local checksum relations plus version/protocol state.

---

## Functional analogies and limits

### A — Case 18 ZFS scrub

Both cases expose **proactive verification before ordinary demand**, but the historical names and system boundaries differ. ZFS explicitly calls its operation `scrub`; GFS 2003 says `scan and verify` inactive chunks and adds distributed replica-version and clone-repair relations.

### A — Case 23 Dynamo anti-entropy

Both perform background distributed maintenance, but the target differs. Dynamo's Merkle-tree anti-entropy detects replica divergence/currentness. GFS explicitly says legal replicas can diverge, so it uses per-copy checksums for local corruption. `anti-entropy ≠ integrity scanning`.

### A — Case 17 RAID reconstruction

Both distinguish service continuity from restored redundancy margin, but RAID parity can reconstruct a missing contribution algebraically while this GFS regime copies another valid full replica.

### A — Case 25 Swift mutable EC

Swift must assemble an admissible same-timestamp coded cohort. GFS filters full replicas through version and checksum relations. `coded-version admissibility ≠ replicated-copy integrity`.

These are functional comparisons only, not claims of one historical lineage.

---

## Prior-art and terminology boundary

Case 18 records Schwarz et al., MASCOTS 2004, as a direct source for the term/mechanism `disk scrubbing`. The 2003 GFS paper is earlier and documents idle-time `scan and verify` behavior that is functionally scrubbing-like, but it does **not** use the word `scrub`.

The justified correction is therefore narrower:

> proactive background integrity verification existed in this production distributed-filesystem account by 2003, before the repository's current 2004 `disk scrubbing` terminology anchor.

This does not establish that GFS invented scrubbing or that later named scrub protocols are historically identical.

---

## Philosophical interpretation

The exact technical pressure is that redundancy can physically exist while its future usefulness remains uncertain until validity is exercised. `Having several copies` is weaker than `having several copies presently qualified to sustain future recovery`.

That can discipline a philosophy of retention: persistence is not exhausted by material multiplicity. Verification, currentness criteria, repair-source qualification, and maintenance participate in making an earlier state available later. The interpretation stops there; no philosophical vocabulary is attributed to the GFS authors.

---

## Counterexamples / limits

This case does **not** establish that all GFS replicas are byte-identical; that checksums prove semantic correctness/authenticity; that 32-bit checksums detect every corruption; that inactive chunks are scanned on one fixed schedule; that GFS historically calls the operation `scrub`; that successful alternate reads mean redundancy is restored; that the 2003 regime uses erasure coding; that later Colossus has identical semantics; or that GFS invented replication, checksumming, proactive verification, or background repair.

---

## Claim ledger

| Claim | Label | Evidence / status |
| --- | --- | --- |
| chunk version numbers distinguish stale replicas | H/P | 2003 paper §4.5 |
| per-64 KB blocks have separately retained 32-bit checksums | H/P | §5.2 |
| read data is checksum-verified before return | H/P | §5.2 |
| checksum mismatch triggers error/report and alternate-replica service | H/P | §5.2 |
| master clones a valid replacement before deleting corrupt copy | H/P | §5.2 |
| idle chunkservers can scan and verify inactive chunks | H/P | §5.2 |
| under-replication repair clones from a valid replica and is throttled | H/P | §4.3 |
| legal replica divergence is not a universal corruption test | H/P/E | §5.2 |
| version currentness ≠ integrity validity | E | reconstruction from §§4.5, 5.2 |
| replica multiplicity ≠ verified repair margin | E | reconstruction from §§4.3, 5.2 |
| GFS idle verification is functionally comparable to ZFS scrub but not the same historical named mechanism | A | Cases 18, 26 |
| GFS integrity scanning ≠ Dynamo anti-entropy | A | Cases 23, 26 |

---

## Sources

### Primary

Sanjay Ghemawat, Howard Gobioff, Shun-Tak Leung, **“The Google File System,”** *Proceedings of the 19th ACM Symposium on Operating Systems Principles (SOSP)*, 2003, pp. 20–43.

- Google Research record: <https://research.google/pubs/the-google-file-system/>
- Google-hosted paper: <https://storage.googleapis.com/gweb-research2023-media/pubtools/pdf/035fc972c796d33122033a0614bc94cff1527999.pdf>
- bounded anchors: §§2.5, 4.3, 4.5, 5.1.2, especially §5.2 `Data Integrity`.

### Repository controls

- [`evidence/18-zfs-scrub-2004-2010-grounding.md`](../evidence/18-zfs-scrub-2004-2010-grounding.md) — 2004 `disk scrubbing` terminology anchor.
- [`cases/23-amazon-dynamo-divergent-version-anti-entropy.md`](23-amazon-dynamo-divergent-version-anti-entropy.md) — distributed currentness/anti-entropy comparison.
- [`cases/25-openstack-swift-ec-overwrite-durable-currentness.md`](25-openstack-swift-ec-overwrite-durable-currentness.md) — mutable coded-currentness comparison.

### Related-repository duplication check

`tmzncty/computing-archaeology` was searched for GFS / Google File System / checksum inactive-chunk integrity; no dedicated matching case was found in this slice. A broader GFS/Google-storage history should still live there if developed later.

---

## Status

**`grounded`**

Grounding basis: system-primary period paper; precise section anchors for versioning, re-replication, checksums, read validation, and idle verification; direct text inspection plus visual inspection of the §5.2 facsimile page; explicit terminology/prior-art boundary; related-repository duplication check; and separation of historical record, engineering reconstruction, functional analogy, and philosophical interpretation.
