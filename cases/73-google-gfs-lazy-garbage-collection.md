# Google File System Lazy Garbage Collection: Hidden-Name Grace, Orphaned Chunks, and Stale-Replica Retirement

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
