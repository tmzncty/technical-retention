# Case 73 grounding record — GFS lazy garbage collection and stale-replica retirement, 2003

## Result

**Promote Case 73 directly as `grounded`.**

The bounded question is unusually explicit in the 2003 GFS primary paper: §§4.3–4.5 describe the complete staged relation from application deletion to hidden-name grace, namespace-reference retirement, orphan discovery, HeartBeat-based physical-replica cleanup, and separate version-based stale-replica deauthorization. The source also records the design reasons and tradeoff rather than leaving them to reconstruction.

## Research question

> When GFS deletes a file, which retained relations disappear immediately, which remain for a grace interval, which are retired by later scans/HeartBeats, and when can a surviving physical replica cease to count before its bytes are actually removed?

This closes a distributed technical-forgetting/reclamation sub-slice without repeating Case 26's checksum/integrity work or Case 46's operation-log/checkpoint recovery work.

## Source A — Ghemawat, Gobioff, and Leung, SOSP 2003

**Type:** period-primary system paper / Google engineering account.

**Citation:** Sanjay Ghemawat, Howard Gobioff, and Shun-Tak Leung, “The Google File System,” *Proceedings of the 19th ACM Symposium on Operating Systems Principles* (SOSP 2003), pp. 29–43. DOI `10.1145/945445.945450`.

**Google Research record:** <https://research.google/pubs/the-google-file-system/>

**Primary PDF:** <https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf>

### Directly inspected anchors — §4.3

- re-replication priorities prefer chunks for live files over chunks belonging to recently deleted files;
- therefore the paper itself distinguishes deletion status from immediate disappearance of all replication maintenance.

### Directly inspected anchors — §4.4 / §4.4.1

- after file deletion GFS does not immediately reclaim physical storage;
- application deletion is logged immediately like other changes;
- default path renames the file to a hidden name containing deletion timestamp;
- namespace scan removes hidden files older than three days, with interval configurable;
- before removal the hidden file can still be read under the special name and undeleted by renaming it back;
- removal of the hidden file erases in-memory file metadata and severs links to its chunks;
- chunk-namespace scan identifies orphaned chunks, defined as not reachable from any file, and erases their metadata;
- chunkservers report subsets of their local chunk inventory in HeartBeat exchanges;
- master replies with chunks no longer present in master metadata;
- chunkserver is free to delete those physical replicas.

### Directly inspected anchors — §4.4.2

- paper contrasts GFS's simple authoritative reference structure with harder general distributed-GC problems;
- GC is motivated partly by partial chunk creation, lost delete messages, and the difficulty of remembering/retrying eager deletions across failures;
- regular scans/handshakes supply a uniform cleanup path for replicas not known to be useful;
- reclamation is batched/amortized and done when master is relatively free;
- delay provides a safety net against accidental irreversible deletion;
- delay can hinder space reuse when storage is tight;
- repeated explicit delete can expedite reclamation;
- per-namespace policy can choose different replication/reclamation behavior, including immediate irrevocable removal from **file-system state**.

### Directly inspected anchors — §4.5

- chunkservers that miss mutations can retain stale replicas;
- master persists a chunk version number and up-to-date replicas record the advanced version before new client writes begin;
- restarting chunkservers report chunk/version sets and the master identifies stale replicas;
- stale replicas are removed in regular garbage collection;
- before removal, the master effectively treats them as nonexistent when returning chunk locations;
- version checking also protects lease/cloning access paths.

**Evidence strength:** high for the bounded 2003 production-system design and its period terminology.

**Limits:**

- system paper, not a later Colossus implementation audit;
- no block-device/media-forensics evidence below the chunkserver's Linux file deletion;
- no invention-priority proof for lazy deletion or distributed garbage collection;
- the configurable three-day interval is a documented default/design value, not a universal timeless GFS constant.

## Source B — Google Research publication record

**Type:** authoritative institutional bibliographic record.

**URL:** <https://research.google/pubs/the-google-file-system/>

It confirms the title, authors, 2003 SOSP publication venue and Google provenance. It is used for bibliographic control, not as a substitute for the technical text in §§4.3–4.5.

## PDF-inspection note

The primary Google-hosted PDF was inspected through its parsed page text at the relevant §4.4–4.5 pages. Screenshot retrieval was also attempted for the relevant PDF pages; the web screenshot backend returned a cache/content-type error during this run. No claim in the case depends on OCR or on an unread image-only feature: the cited section text is available in the PDF's parsed text layer.

## Related-repository duplication check

Before drafting, GitHub code searches in `tmzncty/computing-archaeology` for:

- `GFS garbage collection deleted file orphaned chunks stale replica`;
- `Google File System GFS`;

returned no dedicated case or mechanism history to reuse.

A broader distributed-filesystem history should go there if later developed; the present contribution stays retention-specific.

## Separation from existing technical-retention cases

### Case 26 — GFS inactive-chunk integrity

Case 26 already establishes:

- chunk-version currentness;
- per-block checksum integrity;
- read-time verification;
- idle `scan and verify`;
- re-replication from a valid replica.

Case 73 does not repeat that integrity story. It asks when a file/chunk/replica should be retired from the authoritative object graph and when physical cleanup follows.

The critical separation is:

```text
orphaned chunk
    != stale replica
    != checksum-corrupt replica
```

### Case 46 — GFS master log/checkpoint recovery

Case 46 explains how master metadata mutations survive restart and how older log history becomes dispensable after checkpoints. Case 73 reuses only the period fact that deletion is logged, then follows the later garbage-collection lifecycle.

### Swift / Cassandra / Kafka delete-state cases

Those cases retain explicit negative/tombstone state to suppress older positive records under replica/compaction rules. GFS's default hidden-name grace retains a positive file object that remains readable and can be renamed back.

This is a functional comparison only, not shared terminology or genealogy.

### NVMe / Flash forgetting cases

GFS metadata/reclamation cannot prove underlying media sanitization. File-system retirement, block allocation, controller deallocation, Flash reclamation, and secure sanitization remain different layers.

## Engineering reconstruction boundary

The following are project reconstructions justified by the source, not GFS quotations:

1. **staged retirement of authority** — naming/reachability/currentness can disappear before physical replica bytes;
2. **grace-retained positive state** — deletion can temporarily retain enough namespace/mapping state to support reversal;
3. **maintenance-priority attenuation** — recently deleted state can receive less re-replication priority before final retirement;
4. **inventory-driven convergence** — re-observation through regular HeartBeats lets GC clean up replicas without perfect memory of every earlier eager-delete RPC;
5. **retirement frontier** — different layers cross the `no longer counts` boundary at different times.

None of those phrases is presented as historical GFS vocabulary.

## Prior-art boundary

No first-invention claim is supported or needed.

The GFS paper itself acknowledges garbage collection as a pre-existing problem class and says the GFS case is simpler because references are centralized in the master's file-to-chunk mappings and replicas are identifiable Linux files on chunkservers.

Therefore do **not** claim:

- GFS invented garbage collection;
- GFS invented lazy deletion;
- GFS invented deferred physical reclamation;
- GFS invented version-number stale-replica filtering;
- GFS hidden names are the historical ancestor of Cassandra/Swift/Kafka tombstones.

The defensible historical claim is only that the 2003 GFS paper documents this particular production composition and its explicit design rationale.

## Evidence classification

| Proposition | Label | Grounding |
| --- | --- | --- |
| GFS logs application delete before later reclamation | H/P | GFS 2003 §4.4.1 |
| default deleted file becomes hidden timestamped file | H/P | §4.4.1 |
| hidden file remains readable/undeletable during grace | H/P | §4.4.1 |
| expired hidden-file removal severs file-to-chunk links | H/P | §4.4.1 |
| orphan chunks are chunks unreachable from any file | H/P | §4.4.1 |
| HeartBeat inventory supports later physical-replica deletion | H/P | §4.4.1 |
| lazy GC is motivated by failure/lost-message simplicity and batching | H/P | §4.4.2 |
| delayed reclamation is explicitly a safety net | H/P | §4.4.2 |
| recent-delete chunks are lower re-replication priority than live chunks | H/P | §4.3 |
| stale replicas are excluded from service before GC physically removes them | H/P | §4.5 |
| physical replica survival does not establish namespace/currentness authority | E | follows from §§4.4–4.5 |
| delete-time control state can temporarily preserve undelete capability | E | follows from hidden-name/timestamp semantics |
| orphaned = stale = corrupt | X | explicitly rejected by mechanism separation |
| immediate irrevocable removal from GFS state = secure media erase | X | no lower-layer sanitization evidence |
| GFS invented garbage collection | X | source itself frames GC as an existing problem class |

## Findings to add to CASE_INDEX

845. **application delete ≠ immediate physical-storage reclamation** — GFS logs deletion immediately but lazily reclaims physical storage through later file/chunk garbage collection;
846. **deletion log record ≠ final namespace/chunk retirement** — durable delete intent precedes hidden-file expiry, orphan discovery, and local replica removal;
847. **hidden-name grace ≠ namespace absence** — the default deleted file remains readable under a special name and can be undeleted before grace expiry;
848. **deletion timestamp can become reclamation-control state** — the retained timestamp helps determine when the hidden positive state is eligible for later removal;
849. **logical deletion can reduce repair priority before retention terminates** — GFS prefers live-file chunks over recently deleted chunks for re-replication rather than treating deletion as instantaneous zero-maintenance state;
850. **file-metadata retirement ≠ chunk-replica deletion** — severing file-to-chunk links and forgetting orphan metadata precede deletion of chunkserver Linux files;
851. **orphaned chunk ≠ stale replica** — orphaned means unreachable from any file, whereas stale means an older chunk version after missed mutations;
852. **stale replica ≠ checksum-corrupt replica** — Case 26's integrity failure and Case 73's version-currentness failure are independent qualification axes;
853. **master metadata absence can deauthorize a physically surviving replica** — an unreferenced local chunk file can be garbage from the authoritative namespace perspective before local deletion;
854. **physical replica survival ≠ authoritative namespace reachability/currentness** — bytes can remain below a retired naming/currentness relation;
855. **stale-replica deauthorization ≠ physical deletion** — the master excludes stale versions from ordinary location replies before regular GC removes them;
856. **background GC convergence ≠ perfect retry history for every delete RPC** — periodic namespace scans and HeartBeat inventories give GFS a uniform cleanup path across partial creation/deletion and failures;
857. **reclamation latency can be deliberate reliability policy** — the documented delay provides an accidental-deletion safety net even though it temporarily consumes storage;
858. **immediate irrevocable file-system-state removal ≠ secure media erase** — namespace policy can eliminate GFS recovery without proving lower-layer sanitization;
859. **GFS hidden-name grace ≠ replicated tombstone semantics** — the default grace object is a readable/undeletable positive file state, unlike the explicit negative records in Swift/Cassandra/Kafka cases;
860. **storage reclamation ≠ secure sanitization** — GFS garbage collection retires file/chunk state and local replicas but supplies no forensic/media-erasure guarantee.

## Promotion rationale

Case 73 can be `grounded` now because:

1. the primary system paper explicitly documents every important stage of the bounded deletion/reclamation lifecycle;
2. it explains why the design was chosen, including failure handling, background batching, user safety, and storage-pressure tradeoffs;
3. stale-replica exclusion provides a second direct primary example of `authority retirement before physical removal` inside the same source;
4. existing Cases 26 and 46 already cover the adjacent integrity and master-recovery mechanisms, so this slice adds a distinct result rather than duplicating GFS history;
5. the source itself blocks a generic garbage-collection invention claim;
6. lower-layer physical sanitization and later Colossus behavior remain explicitly unclaimed.

## Remaining work that does not block this case

- earlier lazy-deletion / file-system reclamation genealogy;
- a dedicated distributed-garbage-collection prior-art map outside the GFS-specific mechanism;
- later GFS/Colossus reclamation evolution;
- implementation traces measuring actual hidden-file, namespace-scan, HeartBeat, and replica-delete timing;
- named chunkserver filesystem/device evidence for block reuse after replica deletion;
- forensic validation below the Linux file-system and storage-controller layers.
