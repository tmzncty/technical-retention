from pathlib import Path

CASE = r'''# Google File System Lazy Garbage Collection: Hidden-Name Grace, Orphaned Chunks, and Stale-Replica Retirement

## Status

**`grounded`** — bounded to the lazy file/chunk reclamation and stale-replica retirement semantics documented in Ghemawat, Gobioff, and Leung's 2003 Google File System (GFS) paper, especially §§4.3–4.5. The Google Research publication record is used for bibliographic control; the paper itself is the primary technical source.

Grounding record: [`../evidence/73-gfs-2003-lazy-garbage-collection-grounding.md`](../evidence/73-gfs-2003-lazy-garbage-collection-grounding.md).

## Scope

This case asks one narrow distributed-retention / forgetting question left between Cases 26 and 46:

> **What exactly has been forgotten after a GFS application deletes a file, while namespace state, file-to-chunk references, chunk metadata, and physical chunk replicas are retired at different times?**

The bounded default path is:

```text
application DELETE
    -> deletion is logged
    -> file is renamed to a hidden name containing deletion time
    -> for a configurable grace interval (three days in the paper)
         the hidden file remains readable and can be undeleted
         its chunks may still exist and may still receive lower-priority re-replication
    -> namespace scan removes the aged hidden file
    -> file metadata / file-to-chunk links disappear
    -> chunk scan classifies now-unreachable chunks as orphaned
    -> master forgets orphan chunk metadata
    -> later HeartBeat inventory exposes physical replicas no longer known to master
    -> chunkserver may delete those replicas
```

A second retirement path concerns **stale replicas**: chunk version numbers can disqualify an older replica from client service before regular garbage collection physically removes that replica.

This is **not**:

- a general history of garbage collection, distributed garbage collection, file-system deletion, Unix unlink, trash/recycle-bin interfaces, or Google storage;
- a claim that GFS invented lazy deletion, deferred reclamation, garbage collection, version numbers, or background cleanup;
- a claim that a GFS delete, hidden-name expiration, metadata deletion, chunk deletion, disk overwrite, or secure sanitization are the same event;
- a reconstruction of later Colossus behavior;
- a claim that every deleted-file chunk remains triply replicated throughout the grace interval;
- a claim that a stale replica is the same thing as an orphaned or checksum-corrupt replica.

The retention-specific contribution is narrower:

> **GFS makes deletion a staged retirement of authority and reachability. A logical delete can be durable and user-visible before the system has retired namespace references, chunk metadata, or physical replicas; conversely, a surviving replica can cease to count before its bytes are deleted.**

`retirement frontier`, `grace-retained positive state`, and `maintenance-priority attenuation` below are project engineering terms, not GFS historical vocabulary.

## Related-repository check

Fresh code searches in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `GFS garbage collection`, `orphaned chunks`, and `Google File System` found no dedicated technical-history case to reuse. Case 73 therefore keeps the bounded retention/forgetting decomposition here rather than duplicating a companion-repository account.

If a broader GFS or distributed-filesystem history is later built there, this case should link to it and retain only the staged-retirement comparison.

## Historical vocabulary and source boundary

The 2003 paper directly uses:

- `Garbage Collection`;
- `hidden name`;
- `deletion timestamp`;
- `undeleted`;
- `orphaned chunks`;
- `garbage`;
- `HeartBeat`;
- `stale replica`;
- `chunk version number`;
- `regular garbage collection`;
- `reclaim unused storage`.

The source does not describe this path with the later distributed-database vocabulary `tombstone`, `reclaim_age`, `compaction tombstone`, or `secure erase`. Those terms must not be projected backward into the historical record.

The paper is:

Sanjay Ghemawat, Howard Gobioff, and Shun-Tak Leung, **“The Google File System,”** SOSP 2003, pp. 29–43, DOI `10.1145/945445.945450`.

Google Research publication record: <https://research.google/pubs/the-google-file-system/>

Primary PDF: <https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf>

## Historical record

### H/P — application deletion is logged immediately, but default physical reclamation is deliberately lazy

Section 4.4 opens by stating that after a file is deleted, GFS **does not immediately reclaim the available physical storage**. Reclamation occurs lazily through regular garbage collection at both the file and chunk levels.

Section 4.4.1 says the master logs the application deletion immediately like other changes, but instead of immediately reclaiming resources it renames the file to a hidden name containing the deletion timestamp.

This establishes a period-primary sequence in which durable deletion intent and physical-storage reclamation are separate events.

**Primary anchor:** Ghemawat et al. 2003, §4.4 and §4.4.1.

### H/P — the default hidden-name state preserves a bounded undelete path

During regular namespace scans, the master removes hidden files that have existed for more than three days; the interval is configurable. Until then, the paper explicitly says the file can still be read under its special name and can be undeleted by renaming it back.

The hidden object is therefore not merely an abstract negative marker. Under the bounded default policy it remains a positive, name-addressable file state whose ordinary name has been replaced by a special hidden one.

**Primary anchor:** §4.4.1.

### H/P — file-metadata retirement precedes chunk-replica retirement

When the aged hidden file is removed from the namespace, its in-memory metadata is erased, severing the links from that file to its chunks.

A separate regular scan of the chunk namespace then identifies **orphaned chunks**, defined by the paper as chunks not reachable from any file, and erases their master metadata.

Only after this control-state retirement do later HeartBeat exchanges expose chunkserver replicas that are no longer present in the master's metadata; the chunkserver is then free to delete those replicas.

The source itself therefore supplies at least three distinct retirement layers:

```text
file naming/reference state
    -> master chunk metadata / reachability state
    -> chunkserver physical replica files
```

**Primary anchor:** §4.4.1.

### H/P — garbage collection was chosen partly to survive lost or partial creation/deletion work

Section 4.4.2 explains why GFS preferred this scheme over eager deletion. Chunk creation can succeed on only some chunkservers, leaving replicas unknown to the master; explicit replica-deletion messages can also be lost, creating retry/bookkeeping burdens across master and chunkserver failures.

The paper says regular garbage collection gives a uniform way to clean up replicas that are not known to be useful, merges reclamation into namespace scans and chunkserver handshakes, batches the work, amortizes its cost, and lets the master defer it until relatively free.

**Primary anchor:** §4.4.2.

### H/P — deferred reclamation is also an intentional safety policy, not only cleanup lag

The authors identify the delay itself as a safety net against accidental irreversible deletion. They also report the cost: when storage is tight, applications that repeatedly create and delete temporary files may be unable to reuse space immediately.

GFS can expedite reclamation when a deleted file is explicitly deleted again, and the paper says users can apply different replication/reclamation policies to parts of the namespace. One example permits deleted files in a directory tree to be removed immediately and irrevocably from **file-system state**.

The historical claim stops at file-system state. The source does not turn that phrase into a media-sanitization guarantee.

**Primary anchor:** §4.4.2.

### H/P — recently deleted files can remain inside the replication-maintenance economy, but at reduced priority

Section 4.3 says the master prefers re-replicating chunks for live files before chunks belonging to recently deleted files.

That sentence is important for retention semantics. Deletion under the default grace regime does not instantly collapse all preservation activity to zero. The system can still treat recently deleted chunks as candidates for re-replication, while explicitly lowering their priority relative to live data.

**Primary anchor:** §4.3, immediately before the cloning discussion.

### H/P — stale replica currentness is revoked before physical garbage collection

Section 4.5 treats another reason a surviving chunk file may no longer count. If a chunkserver was unavailable and missed mutations, its replica can have an older chunk version number. The master detects the mismatch when the chunkserver reports its chunks and versions.

The paper then states that stale replicas are removed during regular garbage collection, but **before removal** the master effectively considers them nonexistent when answering client chunk-location requests. Version numbers are also carried in lease and cloning paths so clients/chunkservers can verify they are accessing current data.

Therefore a physical replica can survive after its service authority has already been revoked.

**Primary anchor:** §4.5.

## Retained state

The bounded reclamation path depends on retaining or reconstructing more than the user payload:

1. **file payload embodied in chunk replicas**;
2. **namespace/name state**, including the temporary hidden name;
3. **deletion timestamp**, which makes the grace/reclamation decision time-relative;
4. **file-to-chunk mappings**, which determine whether chunks remain reachable from a file;
5. **chunk metadata at the master**, whose absence eventually makes a physical replica garbage from the master's perspective;
6. **chunkserver inventory**, re-observed through HeartBeat exchanges rather than inferred solely from old master placement records;
7. **chunk version numbers**, which qualify surviving replicas as current or stale;
8. **reclamation/replication policy**, which can change timing and the maintenance priority of recently deleted state.

The deleted file's user bytes are therefore only one part of the state machine that governs forgetting.

## Retention / forgetting mechanism

### Stage 1 — deletion intent becomes durable

The master logs the delete operation. Case 46 separately grounds the operation-log durability/recovery mechanics; Case 73 uses that fact only to locate the beginning of the retirement sequence.

### Stage 2 — ordinary naming is withdrawn while a special positive state survives

The file is renamed to a hidden timestamped name. The default grace policy still permits reading and undeleting it.

This is not yet physical forgetting and is not equivalent to a replicated negative tombstone.

### Stage 3 — namespace reachability is retired

After the grace threshold, regular scanning removes the hidden file and its file metadata, severing file-to-chunk links.

### Stage 4 — orphaned chunk metadata is retired

A chunk-namespace scan identifies chunks unreachable from any file and removes their master metadata.

### Stage 5 — physical replica files become deletable when re-observed

Chunkservers report chunk inventories in HeartBeats. The master replies with chunk identities no longer present in its metadata; those replicas can then be deleted locally.

This is a convergence process, not one atomic global delete transaction.

### Parallel currentness path — stale replicas are deauthorized first and collected later

Version-number comparison can exclude a stale replica from location replies, reads, mutations, or cloning before the local chunk file is eventually garbage collected.

The same physical-survival / authority split therefore appears in both namespace reclamation and replica-currentness cleanup, for different historical reasons.

## Addressing and access geometry

Before deletion:

```text
ordinary pathname
    -> namespace metadata
    -> file-to-chunk mapping
    -> chunk handle
    -> current replica locations / versions
    -> chunkserver Linux file
```

During the default grace period:

```text
hidden timestamped pathname
    -> still-retained file metadata
    -> same chunk relations
    -> readable / undeletable positive state
```

After namespace/chunk-metadata retirement:

```text
no file reference
    -> orphan classification
    -> master no longer keeps chunk metadata
    -> surviving chunkserver Linux file may still physically exist
    -> HeartBeat reconciliation makes it deletable
```

Physical existence alone is therefore weaker than namespace reachability or current service authority.

## Read / delete / reclamation semantics

### Read

A default-policy deleted file can still be read under its hidden special name during the grace interval. Separately, a stale replica may still exist physically while the master refuses to return it as a valid location.

### Delete

The application delete is logged and transformed into a hidden rename under the default policy. It is not an immediate physical erase operation.

### Undelete

Before hidden-file reclamation, the file can be restored by renaming it back to normal. This depends on retaining enough namespace and mapping state for the special positive object still to exist.

### Reclamation

Regular namespace scans retire old hidden files; chunk scans retire unreachable master chunk metadata; HeartBeat reconciliation permits chunkserver replica deletion. Storage reclamation is thus distributed across time and control locations.

## Time, maintenance, and labor

Relevant timescales include:

- immediate logging of the delete operation;
- the configurable hidden-file grace interval (three days in the paper's default description);
- periodic namespace scans;
- periodic chunk-namespace scans;
- regular HeartBeat exchanges;
- lower re-replication priority for recently deleted chunks;
- expedited reclamation when policy or repeated deletion requests demand it.

The source explicitly treats reclamation as background work that is batched and preferentially done when the master is relatively free. Deletion therefore competes with foreground service indirectly through reclamation timing and resource policy even though it is not implemented as a synchronous full-cluster erase.

## Failure / forgetting modes

Keep these distinct:

- **ordinary-path name withdrawal** — the user's original pathname is gone;
- **grace-retained hidden positive state** — file still exists under a special name and may be undeleted;
- **expired hidden-file metadata** — file-to-chunk references have been severed;
- **orphaned chunk** — chunk is no longer reachable from any file;
- **master-forgotten chunk** — chunk metadata is absent from the master while a chunkserver file may survive;
- **stale replica** — physical replica belongs to an older chunk version and is deauthorized from normal service;
- **checksum-corrupt replica** — Case 26's independent integrity-failure class;
- **physically surviving replica** — may still exist below all of the above logical/currentness retirements;
- **securely sanitized media** — not established by this case.

These are different axes. `orphaned`, `stale`, `corrupt`, and `physically deleted` must not be collapsed into one generic `dead copy` category.

## Engineering reconstruction

### E — application delete ≠ immediate physical-storage reclamation

This is almost directly historical vocabulary: the paper states the physical-storage delay. The engineering consequence is that user-visible deletion can precede removal of multiple lower-layer embodiments.

### E — delete-time metadata can preserve reversibility

The hidden name and deletion timestamp are not user payload, but they keep a bounded relation between `deleted now` and `eligible for final namespace reclamation later`. Under the default policy, retaining this control state is what makes undelete possible.

### E — logical deletion can attenuate maintenance before it terminates retention

Because recently deleted chunks receive lower re-replication priority than live-file chunks, deletion can alter how strongly the system invests in preserving an embodiment before final reclamation occurs.

`deleted` is therefore not a single instantaneous transition from full protection to zero maintenance in this bounded design.

### E — metadata absence can revoke authority before bytes disappear

Once the master no longer knows a chunk, a surviving local Linux file is garbage from GFS's authoritative namespace perspective even before local deletion executes.

Likewise, an older-version replica can be excluded from client responses before physical garbage collection.

### E — garbage collection substitutes convergence over retained references/inventory for perfect delete-message memory

The source motivates GC partly by failures that make exact per-replica creation/deletion bookkeeping awkward. Periodic namespace scans plus re-observed chunkserver inventories let the system converge on `known useful` vs `garbage` without requiring every earlier eager-delete message to be remembered and retried forever.

This is an engineering reconstruction of the documented control flow, not a claim that GFS implements a general distributed-garbage-collection algorithm for arbitrary object graphs.

### E — reclamation delay can be retention infrastructure

The three-day default delay consumes storage, but the authors explicitly value it as protection against accidental irreversible deletion. In this bounded regime, retaining unwanted state temporarily can be a reliability feature rather than a failure to forget.

## Functional analogies and limits

### A — Case 26 GFS integrity qualification

Case 26 asks whether a replica is current enough and checksum-valid enough to count as a repair/service source. Case 73 asks when a file/chunk/replica should cease to count at all.

The boundaries are:

> **orphaned chunk ≠ stale replica ≠ checksum-corrupt replica**.

A chunk can be orphaned because no file references it while its bytes/checksum are perfectly intact. A stale replica can belong to a live chunk but have an older version. A checksum-corrupt replica can have the expected logical generation yet fail local integrity verification.

### A — Case 46 GFS master log/checkpoint recovery

Case 46 explains why metadata mutations such as deletion can survive master restart through the replicated operation log and checkpoints. Case 73 begins from the already-grounded fact that deletion is logged, then studies later reclamation stages. It does not repeat checkpoint mechanics.

### A — Swift/Cassandra/Kafka negative-state cases

Swift `.ts`, Cassandra tombstones, and Kafka delete markers retain explicit negative state so older positive state does not reassert itself under their respective replication/compaction rules.

GFS's default deleted file is different: it is renamed to a hidden timestamped **positive file state** that remains readable and undeletable during the grace period. GFS later removes file/chunk references and discovers garbage through authoritative namespace/inventory relations.

Therefore:

> **GFS hidden-name grace ≠ replicated tombstone semantics**.

The functional analogy is only that delayed forgetting can require temporary retained control state.

### A — mapped Flash and NVMe deletion/sanitize cases

Case 04 already shows logical invalidation preceding physical Flash erase. Case 44 distinguishes NVMe deallocation from subsystem sanitization.

GFS supplies a higher distributed-filesystem layer in which namespace/chunk authority can disappear while lower storage still physically holds bytes. It does not establish what the disk/SSD below the chunkserver does with freed blocks.

Therefore:

> **GFS reclamation ≠ media sanitization**.

## Prior art and novelty boundary

No invention-priority claim is made.

The GFS paper itself frames garbage collection as an already-known hard problem in programming-language contexts and contrasts that broader problem with the simpler reference structure available to GFS. Its contribution in this case is not `inventing garbage collection`, but documenting a particular production distributed-filesystem composition:

- deletion logged immediately;
- timestamped hidden-name grace;
- recoverable undelete during that grace;
- namespace-reference retirement;
- orphan detection through the master's file-to-chunk mappings;
- physical-replica discovery through regular chunkserver HeartBeats;
- background deletion of replicas no longer known to be useful;
- version-based deauthorization of stale replicas before later GC.

A broader genealogy of lazy deletion, file-system garbage collection, Unix unlink/orphan semantics, distributed GC, and later object-store tombstones belongs in a separate history slice, preferably coordinated with `computing-archaeology` or `problem-history` where the actor/problem chronology is the main contribution.

## Philosophical interpretation

### I — forgetting can be a change in admissible relation before it is a destruction of material state

The technical fact that creates the conceptual problem is exact: GFS can remove an ordinary name, later sever file-to-chunk references, later forget chunk metadata, and only later delete surviving replica files. A stale replica can also become inadmissible before its bytes disappear.

This supports a narrow philosophical interpretation:

> **technical forgetting can be staged as withdrawal of naming, reachability, currentness, and repair authority before material traces are destroyed.**

The concept clarifies why `the bits still exist` and `the system still has the file` are different propositions.

The interpretation stops there. It does not turn GFS garbage collection into a theory of human forgetting, archival erasure, or secure destruction.

### I — temporary retention can be part of forgetting policy

The default grace period deliberately retains enough state to reverse an accidental deletion. In this case, forgetting is not maximized by deleting everything as quickly as possible; reliability is partly produced by delaying irreversible retirement.

Again, this is a project interpretation of the documented design tradeoff, not vocabulary attributed to the GFS authors.

## Counterexamples / limits

This case does **not** establish that:

- a GFS delete immediately frees disk sectors;
- every deleted file remains recoverable for exactly three days under every namespace policy;
- recently deleted chunks retain the same replication priority as live chunks;
- an orphaned chunk is stale or corrupt;
- a stale replica is physically absent;
- a stale client cache can never briefly contact an older replica (the 2003 paper separately describes a bounded client-cache window);
- master metadata deletion securely erases chunkserver media;
- immediate and irrevocable removal from GFS file-system state is secure sanitization;
- later Google Colossus uses the same mechanism;
- GFS invented lazy deletion, garbage collection, or version-based stale-replica retirement.

## Claim ledger

| Claim | Label | Evidence / status |
| --- | --- | --- |
| application deletion is logged immediately | H/P | GFS 2003 §4.4.1 |
| default delete renames to hidden name containing deletion timestamp | H/P | §4.4.1 |
| hidden file is readable and undeletable during the default grace interval | H/P | §4.4.1 |
| namespace scan removes aged hidden files after a configurable interval | H/P | §4.4.1 |
| file metadata retirement severs file-to-chunk links | H/P | §4.4.1 |
| chunk scan identifies chunks unreachable from any file as orphaned | H/P | §4.4.1 |
| HeartBeat inventory lets master identify replicas absent from its metadata | H/P | §4.4.1 |
| chunkserver may delete such replicas | H/P | §4.4.1 |
| GC batches/amortizes cleanup and tolerates partial/lost eager-delete work | H/P | §4.4.2 |
| delayed reclamation is explicitly valued as an accidental-delete safety net | H/P | §4.4.2 |
| recently deleted chunks have lower re-replication priority than live-file chunks | H/P | §4.3 |
| stale replicas are excluded before regular GC removes them | H/P | §4.5 |
| physical replica survival does not establish authoritative namespace/currentness | E | follows from §4.4–4.5 staged authority/GC relations |
| grace-state retention can make deletion reversible | E | follows from hidden-name + timestamp + undelete semantics |
| GFS hidden-name grace is historically a tombstone | X | rejected; source uses hidden positive file state, not tombstone vocabulary |
| GFS reclamation proves secure media erasure | X | rejected; source defines file-system GC, not sanitization |

## Sources

### Primary

- Sanjay Ghemawat, Howard Gobioff, and Shun-Tak Leung, **“The Google File System,”** SOSP 2003, especially §§4.3–4.5. Google Research: <https://research.google/pubs/the-google-file-system/>. Primary PDF: <https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf>. DOI: <https://doi.org/10.1145/945445.945450>.

### Existing repository controls

- [`26-google-gfs-inactive-chunk-integrity.md`](26-google-gfs-inactive-chunk-integrity.md) — currentness/integrity qualification and background verification;
- [`46-google-gfs-master-log-checkpoint-recovery.md`](46-google-gfs-master-log-checkpoint-recovery.md) — master operation-log/checkpoint recovery boundary;
- [`28-openstack-swift-tombstone-consistency-window.md`](28-openstack-swift-tombstone-consistency-window.md) and [`41-apache-cassandra-tombstone-gc-grace-resurrection.md`](41-apache-cassandra-tombstone-gc-grace-resurrection.md) — distinct negative-state reclamation regimes;
- [`44-nvme13-deallocate-sanitize-forgetting.md`](44-nvme13-deallocate-sanitize-forgetting.md) — logical deallocation versus media sanitization.
'''

EVIDENCE = r'''# Case 73 grounding record — GFS lazy garbage collection and stale-replica retirement, 2003

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
'''

README_ENTRY = "- [`cases/73-google-gfs-lazy-garbage-collection.md`](cases/73-google-gfs-lazy-garbage-collection.md) — grounded GFS 2003 forgetting/reclamation slice: application deletion is logged before a timestamped hidden-name grace period, file/chunk references are retired by later scans, HeartBeat inventory converges physical replica cleanup, and stale versions can lose service authority before their bytes are garbage-collected; separates logical deletion, reversibility, reachability, currentness, reclamation, and sanitization."

CASE_ROW = "| [Google File System Lazy Garbage Collection: Hidden-Name Grace, Orphaned Chunks, and Stale-Replica Retirement](cases/73-google-gfs-lazy-garbage-collection.md) | **grounded** | logged delete + timestamped hidden positive state + configurable grace + namespace/chunk scans + HeartBeat inventory cleanup + version-qualified stale-replica retirement | separate logical delete, bounded reversibility, namespace reachability, master metadata, physical replica survival, currentness deauthorization, reclamation, and secure sanitization | [2003 GFS lazy-GC grounding](evidence/73-gfs-2003-lazy-garbage-collection-grounding.md); earlier lazy-deletion/distributed-GC genealogy, later Colossus behavior, timing traces, and lower-layer media-forensics validation remain separate work |"

MATRIX_ROW = "| Google File System / 2003 bounded lazy-GC regime | chunk payload + hidden timestamped file state + file-to-chunk reachability + master chunk metadata + chunkserver inventory + chunk version currentness | logged deletion; configurable hidden-name grace; namespace/chunk scans; HeartBeat-driven replica cleanup; version-based stale-replica exclusion; lower repair priority for recent deletes | hidden file remains readable/undeletable during grace; stale replicas can still exist physically while excluded from ordinary location replies | ordinary pathname can become hidden timestamped name; later removal severs file→chunk references; orphan classification and master-metadata absence then qualify surviving local files as garbage | physical replica files can outlive ordinary naming, file metadata, master chunk metadata, or currentness authority until later GC | bounded deletion/grace/reclamation-control state only; not a complete deletion history and not evidence of secure media erasure |"

FINDINGS = r'''845. **application delete ≠ immediate physical-storage reclamation** — GFS logs deletion immediately but lazily reclaims physical storage through later file/chunk garbage collection;
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
860. **storage reclamation ≠ secure sanitization** — GFS garbage collection retires file/chunk state and local replicas but supplies no forensic/media-erasure guarantee.'''

case_path = Path('cases/73-google-gfs-lazy-garbage-collection.md')
evidence_path = Path('evidence/73-gfs-2003-lazy-garbage-collection-grounding.md')
assert not case_path.exists(), case_path
assert not evidence_path.exists(), evidence_path
case_path.write_text(CASE, encoding='utf-8')
evidence_path.write_text(EVIDENCE, encoding='utf-8')

# README navigation: append immediately after current Case 72.
readme = Path('README.md')
text = readme.read_text(encoding='utf-8')
lines = text.splitlines()
for i, line in enumerate(lines):
    if 'cases/72-ibm-store-in-cache-currentness-castout.md' in line:
        lines.insert(i + 1, README_ENTRY)
        break
else:
    raise RuntimeError('README Case 72 anchor not found')
readme.write_text('\n'.join(lines) + '\n', encoding='utf-8')

# ROADMAP: add Case 73 to the distributed-storage slice and annotate the broad GC checklist.
roadmap = Path('ROADMAP.md')
text = roadmap.read_text(encoding='utf-8')
old_header = 'distributed replication and erasure coding beyond RADOS — **partially advanced by grounded Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, 51, 56, 57, 58, 61, 63, and 64**.'
new_header = 'distributed replication and erasure coding beyond RADOS — **partially advanced by grounded Cases 19, 23, 24, 25, 26, 27, 28, 29, 41, 46, 48, 49, 50, 51, 56, 57, 58, 61, 63, 64, and 73**.'
assert old_header in text, 'ROADMAP distributed header anchor missing'
text = text.replace(old_header, new_header, 1)
case27_marker = ' [`cases/27-ceph-luminous-ec-deep-scrub-checksum-authority.md`](cases/27-ceph-luminous-ec-deep-scrub-checksum-authority.md)'
assert case27_marker in text, 'ROADMAP Case 27 marker missing'
case73_roadmap = " [`cases/73-google-gfs-lazy-garbage-collection.md`](cases/73-google-gfs-lazy-garbage-collection.md), grounded by [`evidence/73-gfs-2003-lazy-garbage-collection-grounding.md`](evidence/73-gfs-2003-lazy-garbage-collection-grounding.md), adds the file/chunk retirement layer left outside Cases 26 and 46: default application deletion is logged before a timestamped hidden-name grace period; later namespace/chunk scans sever references and classify orphaned chunks; regular HeartBeat inventory then converges physical replica cleanup, while version numbers can deauthorize stale replicas before garbage collection. This separates deletion intent, bounded undelete capability, repair priority, namespace reachability, currentness, physical survival, reclamation, and secure sanitization."
text = text.replace(case27_marker, case73_roadmap + case27_marker, 1)
old_gc = '- [ ] garbage collection / reclamation;'
new_gc = '- [ ] garbage collection / reclamation — **partially advanced by grounded Case 73 at the distributed-filesystem layer**: GFS 2003 separates logged deletion, hidden-name grace, namespace/chunk reference retirement, HeartBeat-driven replica cleanup, and stale-replica deauthorization; broader filesystem, database, Flash/controller, and media-reclamation genealogies remain open;'
assert old_gc in text, 'ROADMAP GC checklist anchor missing'
text = text.replace(old_gc, new_gc, 1)
roadmap.write_text(text, encoding='utf-8')

# CASE_INDEX main ledger row.
index_path = Path('CASE_INDEX.md')
text = index_path.read_text(encoding='utf-8')
lines = text.splitlines()
for i, line in enumerate(lines):
    if 'cases/72-ibm-store-in-cache-currentness-castout.md' in line and line.startswith('| ['):
        lines.insert(i + 1, CASE_ROW)
        break
else:
    raise RuntimeError('CASE_INDEX Case 72 ledger anchor not found')
text = '\n'.join(lines) + '\n'

# Comparison matrix: insert directly after the existing GFS integrity row.
lines = text.splitlines()
for i, line in enumerate(lines):
    if line.startswith('| Google File System / 2003 bounded integrity regime |'):
        lines.insert(i + 1, MATRIX_ROW)
        break
else:
    raise RuntimeError('CASE_INDEX GFS matrix anchor not found')
text = '\n'.join(lines) + '\n'

# Append new findings after current final finding 844.
lines = text.splitlines()
for i, line in enumerate(lines):
    if line.startswith('844. **IBM 1971/3081 evidence ≠ invention-priority proof for write-back caching**'):
        lines[i + 1:i + 1] = FINDINGS.splitlines()
        break
else:
    raise RuntimeError('CASE_INDEX finding 844 anchor not found')
index_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

print('Case 73 research slice applied')
