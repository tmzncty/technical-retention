# Case 26 Grounding Record — GFS Checksums, Inactive-Chunk Verification, and Repair (2003)

## Promotion target

This record grounds [`cases/26-google-gfs-inactive-chunk-integrity.md`](../cases/26-google-gfs-inactive-chunk-integrity.md).

The bounded claim is:

> In the 2003 Google File System, replication count, version currentness, and replica integrity are separate relations. Chunkservers verify per-block checksums on reads and can scan inactive chunks during idle periods; discovered corruption can then be removed from the usable replica set and repaired by cloning from a valid replica toward the configured replication goal.

Status target: **`grounded`**.

---

## Evidence classes

### P1 — system-primary publication record

Google Research's official publication page identifies Sanjay Ghemawat, Howard Gobioff, and Shun-Tak Leung, `The Google File System`, Proceedings of the 19th ACM Symposium on Operating Systems Principles, 2003, pp. 20–43.

URL: <https://research.google/pubs/the-google-file-system/>

### P2 — system-primary paper / implementation account

Google-hosted SOSP 2003 PDF:

<https://storage.googleapis.com/gweb-research2023-media/pubtools/pdf/035fc972c796d33122033a0614bc94cff1527999.pdf>

The bounded claims are taken directly from §§4.3, 4.5, 5.1.2, and 5.2 rather than from later GFS retrospectives.

### P3 — repository-controlled prior-art boundary

[`evidence/18-zfs-scrub-2004-2010-grounding.md`](18-zfs-scrub-2004-2010-grounding.md) already records Schwarz et al., MASCOTS 2004, as a direct source for `disk scrubbing` terminology/mechanism. This record uses that ledger only to prevent a terminology mistake: GFS 2003 documents `scan and verify` of inactive chunks but does not call it `scrub`.

---

## Direct source ledger

### 1. Official Google Research publication record

Directly established:

- authorship;
- SOSP venue;
- 2003 publication year;
- pp. 20–43;
- Google hosts the paper in its research publication record.

Evidence use: bibliographic identity and period/system-primary provenance.

### 2. GFS §4.3 — replica creation / re-replication

Directly established:

- master re-replicates when available replicas fall below a user-specified goal;
- reported possible corruption is one trigger alongside server/disk unavailability or changed goal;
- re-replication priority considers distance from the goal and foreground client impact;
- a destination copies from an existing `valid replica`;
- clone concurrency and bandwidth are limited/throttled;
- placement attempts to spread replicas across racks.

Evidence use:

- `copy count ≠ restored replication goal`;
- repair work has a resource budget;
- a repair source must be considered valid, not merely physically present.

### 3. GFS §4.5 — stale replicas and chunk version numbers

Directly established:

- chunk version numbers distinguish up-to-date from stale replicas;
- stale replicas are not returned to clients;
- stale replicas are later removed through regular garbage collection;
- version checks protect operations from stale state.

Evidence use: version/currentness is retained control state and is not silently treated as an integrity checksum.

### 4. GFS §5.1.2 — replication as availability/reliability policy

Directly established: chunk replicas are distributed across chunkservers/racks, and the master clones replicas to preserve intended replication when servers go offline or checksum detection identifies corruption.

Evidence use: redundancy is a managed distributed relation rather than a property of one disk embodiment.

### 5. GFS §5.2 — checksum integrity mechanism

Directly established:

- each chunkserver uses checksumming to detect stored-data corruption;
- replica comparison is unsuitable as the corruption detector;
- divergent replicas can be legal under GFS mutation semantics, particularly record append;
- therefore each chunkserver independently verifies its copy;
- a chunk is divided into 64 KB blocks with a 32-bit checksum each;
- checksums are kept in memory and stored persistently with logging, separately from user data.

Evidence use:

- `legal replica divergence ≠ corruption`;
- checksum metadata is constitutive non-payload retention state;
- per-copy integrity and replica-version currentness are separate dimensions.

### 6. GFS §5.2 — demand-time verification and repair sequence

Directly established:

- before a read returns data, overlapping checksum blocks are verified;
- on mismatch the chunkserver returns an error and reports it to the master;
- the requester can read another replica;
- the master clones from another replica;
- after a valid new replica is in place, the corrupted replica is ordered deleted.

Evidence use: `detection ≠ fallback availability ≠ completed durable repair`.

### 7. GFS §5.2 — idle verification of inactive chunks

Directly established:

- during idle periods chunkservers can `scan and verify` inactive chunks;
- this targets corruption in rarely read chunks;
- after detection the master can create a new uncorrupted replica and delete the corrupted one;
- the purpose includes preventing an inactive corrupt replica from making the master believe it has enough valid replicas.

Evidence use:

- `redundancy present ≠ redundancy already verified`;
- discovery timing affects how long hidden corruption consumes repair margin;
- proactive verification exists here without the historical word `scrub`.

### 8. GFS §5.2 — checksum maintenance on writes

Directly established:

- append-heavy workloads permit incremental checksum maintenance;
- overwrite of an existing range requires verifying boundary checksum blocks before writing and then computing/recording new checksums;
- otherwise new checksums could hide old corruption in bytes not overwritten.

Evidence use: integrity metadata must be maintained through mutation rather than blindly regenerated from a partially overwritten image.

---

## Facsimile / text inspection boundary

The Google-hosted 15-page PDF was opened directly. The §5.2 `Data Integrity` page was visually inspected as a facsimile as well as through the text layer. The inspected page visibly contains the legal-divergence warning, 64 KB/32-bit checksum description, verification before read return, alternate-replica/cloning sequence, idle-period `scan and verify`, and the warning about a corrupt inactive replica falsely inflating the apparent valid-replica count.

One attempted screenshot of the earlier re-replication page returned a transient cache miss. No layout-, typography-, or figure-specific claim depends on that failed render; §4.3 is used only through directly inspected PDF text.

---

## Terminology and prior-art boundary

Historical GFS vocabulary is preserved as `scan and verify`, `inactive chunks`, `checksum`, `valid replica`, `chunk version number`, `stale replica`, `clone`, and `replication goal`.

The project may call the operation **proactive integrity verification** as engineering description, but it must not rewrite the 2003 source as though it used the later term `scrub`.

Case 18's 2004 Schwarz et al. source remains the current direct terminology anchor for `disk scrubbing`. GFS 2003 changes the novelty boundary only at the functional level:

> a production distributed-filesystem account documented proactive idle-time integrity verification before that 2004 terminology anchor.

This is not an invention-priority claim.

---

## Cross-case controls

### Case 18 — ZFS scrub

Shared function: proactive verification can discover latent corruption before ordinary demand.

Required distinction: ZFS names an explicit pool `scrub` and integrates filesystem checksum/self-healing semantics; GFS uses local per-copy checksums, idle chunkserver scanning, replicated fallback, and master-directed cloning. Functional similarity does not establish historical identity.

### Case 23 — Dynamo anti-entropy

Dynamo's Merkle-tree mechanism compares replica state to discover synchronization/currentness divergence. GFS explicitly says legal replica divergence prevents equality comparison from serving as its corruption test. Therefore `anti-entropy ≠ integrity scan`.

### Case 17 — RAID

RAID reconstructs a missing contribution from encoded surviving members/parity. GFS bounded repair clones another valid full replica. Both can separate service continuity from restored redundancy margin, but the repair algebra is different.

### Case 25 — Swift EC

Swift requires version-coherent coded fragment cohorts plus commit evidence. GFS requires a current-enough full replica whose local stored bytes pass checksum verification. `coded-version admissibility ≠ replicated-copy integrity`.

---

## Related-repository check

GitHub search of `tmzncty/computing-archaeology` for GFS / Google File System / checksum inactive-chunk integrity returned no dedicated matching case during this slice. No pre-existing technical history was copied.

If a broad history of GFS architecture, Google cluster design, or GFS→Colossus lineage is later written, it should primarily live in `computing-archaeology`; this repository should retain the narrower currentness/integrity/repair comparison.

---

## Evidence maturity

**`grounded`** is justified because:

1. the central mechanism is supported by a system-primary, period technical paper;
2. version currentness, replication repair, checksum integrity, read-time validation, and idle verification each have section-level anchors;
3. the key §5.2 page was visually inspected;
4. terminology is kept period-correct and bounded against later `scrub` vocabulary;
5. cross-case analogies are explicit rather than treated as genealogy;
6. related-repository duplication was checked.

Remaining work is outside this slice: later GFS/Colossus integrity evolution, cryptographic checksums, encoded-fragment scrub protocols, large-scale audit sampling, and empirical checksum-collision/failure-rate analysis.
