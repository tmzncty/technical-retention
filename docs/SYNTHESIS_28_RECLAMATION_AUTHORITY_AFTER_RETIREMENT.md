# Synthesis 28 — Reclamation Authority After Retirement: Eligibility, Cleanup Obligations, Reuse, and Sanitization

> **Question:** after a system decides that some name, version, mapping, snapshot relation, construction attempt, or physical embodiment no longer counts as current, what still has to remain true before the associated storage can actually be reclaimed or reused?

**Status:** bounded cross-case synthesis over already-grounded evidence. This document adds no new invention-priority claim and does not assert one genealogy among distributed filesystems, local filesystems, raw-Flash filesystems, cloud object stores, managed SSD firmware, or Ceph. Historical claims remain in the individual case/evidence records.

Grounded anchors used here:

- [`Case 73 — GFS lazy garbage collection`](../cases/73-google-gfs-lazy-garbage-collection.md) — deletion, hidden-name grace, orphaned chunks, master metadata retirement, and later chunkserver deletion;
- [`Case 125 — ext3/ext4 orphan tracking`](../cases/125-linux-ext3-ext4-orphan-crash-cleanup-reclamation.md) — crash-persistent cleanup obligations after namespace/current-size state has advanced;
- [`Case 145 — JFFS2 garbage collection`](../cases/145-jffs2-garbage-collection-negative-state-evidence.md) — obsolete-node retirement, live-node relocation, explicit zero-state retention, and `CLEANMARKER` reuse admission;
- [`Case 147 — S3 multipart upload`](../cases/147-s3-multipart-upload-preobject-retention.md) — aborting construction authority while uploaded part storage can still require verified cleanup;
- [`Case 150 — Crucial M550 / managed-SSD garbage collection`](../cases/150-crucial-m550-active-garbage-collection.md) — logical invalidation/TRIM knowledge separated from controller-local relocation and erase-block reclamation;
- [`Case 153 — Ceph RADOS snap trimming`](../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md) — snapshot retirement separated from shared-clone liveness, queued trim work, replicated cleanup, and completion.

[`Synthesis 22`](SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md) supplies the stronger erase/reuse/sanitization boundary; [`Synthesis 24`](SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md) supplies the broader `capacity/reclaim-triggered maintenance` category. This synthesis does not replace either one. It asks what **authority and retained work relations** sit between logical retirement and reuse.

Fresh repository searches found no dedicated cross-layer reclamation synthesis in `tmzncty/computing-archaeology`. Broader histories of filesystem GC, FTLs, SSD controllers, and distributed storage should remain there if developed; the present document keeps only the cross-mechanism retention analysis.

---

## 1. Verdict

The grounded cases reject a single transition called `delete` or `garbage collect`.

A more defensible cross-case sequence is:

```text
current / reachable / admitted relation
        ↓
authority or reference retirement
        ↓
target qualification
        ↓
reclamation eligibility
        ↓
retained cleanup obligation
        ↓
(optional) preservation / relocation of still-live state
        ↓
reclamation execution
        ↓
cleanup completion
        ↓
reuse admission / free-space authority
```

A separate stronger path may then ask about sanitization:

```text
reuse admission
        ≠
sanitation objective
        ≠
verified sanitization
```

Not every system exposes every stage as a distinct named object. The synthesis vocabulary is therefore **engineering reconstruction**, not a claim that GFS, ext3, JFFS2, AWS, Crucial, or Ceph historically used one common state machine.

The central rule is:

> **Retiring an old relation can create a new maintenance obligation rather than instantly erase the old embodiment.**

That obligation can itself need to be retained, replicated, re-observed, qualified, or resumed before capacity is safely reusable.

---

## 2. Claim discipline

This synthesis follows [`METHOD.md`](METHOD.md) and [`AGENTS.md`](../AGENTS.md).

- **H/P — historical / primary:** dates, vocabulary, product/standard behavior, and implementation details stay with the grounded cases and their evidence ledgers.
- **E — engineering reconstruction:** `authority retirement`, `reclamation eligibility`, `cleanup obligation`, `reclamation closure`, and `reuse admission` are project analytical terms unless a source independently uses equivalent language.
- **A — functional analogy:** two systems may stage retirement and cleanup without sharing algorithms, data structures, media, consistency models, or historical lineage.
- **I — philosophical interpretation:** any statement about forgetting requiring memory is downstream of the engineering evidence and is kept narrow.

The source base is deliberately heterogeneous. GFS and Ceph expose distributed control relations; ext3/ext4 and JFFS2 expose filesystem recovery/reclamation logic; S3 exposes a service contract; the M550 case combines a named product witness with vendor-neutral SSD-GC explanation. The synthesis compares **relations**, not implementation equivalence.

---

## 3. Why this is not a duplicate of Synthesis 22 or 24

### Synthesis 22 asks what kind of forgetting occurred

[`Synthesis 22`](SYNTHESIS_22_ERASE_INVALIDATION_SANITIZATION_VERIFICATION.md) separates:

```text
logical invalidation
    != physical erase
    != reclamation / reuse
    != sanitization objective
    != verification evidence
```

The present synthesis narrows the middle of that chain. It asks what must still be retained or established between **logical retirement** and **reclamation/reuse**.

### Synthesis 24 asks why maintenance becomes due

[`Synthesis 24`](SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md) defines `capacity/reclaim-triggered maintenance` as one trigger regime among several. The present synthesis asks what happens **after** reclamation work is due: how targets become eligible, how live references block disposal, what cleanup state must persist, and what evidence admits capacity to reuse.

Thus:

> **maintenance trigger != reclamation authority != cleanup completion**.

---

## 4. Cross-case matrix

| Case | What retires first? | What can still survive? | What blocks or conditions reclamation? | What counts as a later closure? |
| --- | --- | --- | --- | --- |
| **GFS 73** | ordinary pathname / later file-to-chunk and master-chunk relations | hidden positive state, chunk metadata, physical replicas, stale replicas | grace interval, namespace/chunk scans, authoritative metadata, HeartBeat re-observation | orphan metadata retired and later replica files made deletable/deleted |
| **ext3/ext4 125** | directory reachability or desired truncate size can advance | inode, blocks, unfinished delete/truncate work | crash-persistent orphan target plus qualified inode state; journal recovery ordering | orphan cleanup discharges delete/truncate work and allocation becomes reclaimable |
| **JFFS2 145** | older node becomes obsolete / range loses currentness | stale nodes in mixed erase blocks; still-live nodes sharing the block | live-node preservation, explicit negative/zero evidence, successful erase evidence | old block erased and `CLEANMARKER` admits it as safely reusable |
| **S3 147** | multipart construction authority can be aborted | uploaded/racing part storage | in-flight `UploadPart`, upload/part identity, cleanup verification | no remaining parts for the retired upload at the service boundary |
| **SSD GC 150** | host/file-system data becomes unneeded; TRIM may communicate that | stale physical pages mixed with still-live pages | mapping/currentness plus enough relocation workspace; controller maintenance opportunity | live data relocated, victim block erased, block returned to free capacity |
| **Ceph 153** | snapshot relation is retired | clones, shared snapshot membership, queued trim work | any remaining live snapshot membership; PG/trim/recovery state | memberships revised and clone removed only when no live snapshot still needs it |

The matrix is a comparison aid. It does not assert that a hidden GFS file, an ext4 orphan inode, a JFFS2 obsolete node, an S3 part, an SSD invalid page, and a Ceph clone are one ontological category.

---

## 5. E — authority retirement is weaker than material disappearance

The first stable cross-case relation is:

> **no longer authoritative != no longer embodied**.

GFS makes this visible twice. A file can lose its ordinary name yet remain readable under a hidden timestamped name during the grace interval. Later, a chunk replica can physically survive after the master no longer admits it as a current/useful chunk; a stale replica can likewise be excluded from client location replies before regular garbage collection removes the local file.

JFFS2 gives a local raw-Flash version. A newer node/version/range relation can make an older physical node obsolete while the old bytes remain in a dirty erase block until later collection.

Managed SSDs hide the physical detail, but the logical relation is still bounded: host deletion or TRIM/deallocation knowledge does not itself prove that the corresponding NAND embodiment has already been erased.

Ceph snaptrim gives the versioned-object counterpart: retiring one snapshot relation can occur before clones touched by that snapshot have been removed.

S3 multipart upload shows that the same split can occur even **before an object ever existed**. Abort can retire an upload ID's future construction authority while service-retained part data still require cleanup.

Therefore material survival is not by itself evidence of continued authority, and authority retirement is not by itself evidence of material disappearance.

---

## 6. E — reclamation eligibility is a qualified relation, not a synonym for deletion

A second distinction is:

> **retired != reclaimable now**.

### Reference-conditioned liveness

Ceph provides the clearest reference counterexample. A clone can serve multiple snapshots. Removing one snapshot removes one membership relation, but the clone remains live if another snapshot still requires it.

GFS similarly makes reachability decisive at another layer. A chunk becomes orphaned when no file reaches it; later authoritative metadata and HeartBeat reconciliation determine how a surviving local replica is treated.

### Mixed-embodiment liveness

JFFS2 and managed SSD GC show a different reason for blocking reclamation: the erase unit can mix stale and current state. A stale node/page does not make the whole erase block disposable. Current state must be preserved elsewhere first.

### Recovery-qualified targets

ext3/ext4 orphan tracking shows that target identity alone can be insufficient. The orphan list/file says which inode requires cleanup, but the surviving inode state still qualifies whether recovery should truncate or delete. The 2023 power-cut bug is an especially strong warning: retaining an orphan target while the on-disk target state is stale can fail to discharge the cleanup correctly.

Thus reclamation eligibility is a **relation among target identity, current references/currentness, and the state needed to interpret the target**, not merely a Boolean named `deleted`.

---

## 7. E — cleanup obligation is retained state in its own right

Several cases make unfinished reclamation a positive state that must survive long enough to be completed.

### ext3/ext4

The orphan list/file is explicitly an on-disk population of inodes whose delete/truncate work may need recovery after a crash. The namespace or desired file size can already have advanced while cleanup remains outstanding.

So:

> **cleanup obligation != payload replica**

and:

> **cleanup obligation != cleanup completion**.

### Ceph

Snapshot retirement feeds a trimming queue/purged-snapshot relation; object membership changes are propagated through normal log/repop/replica machinery. Maintained PG states distinguish waiting, executing, and error-stopped trim work.

So:

> **queued cleanup != executing cleanup != successful cleanup**.

### GFS

GFS does not retain one named `cleanup obligation` object equivalent to ext4's orphan file. Instead, regular namespace scans, chunk scans, and re-observed chunkserver inventories let the system converge on what is no longer useful. This is a counterexample to treating all reclamation debt as one durable queue structure.

### S3

The API makes another form visible: one abort request does not prove that every racing part write has already disappeared. The service contract explicitly requires later observation (`ListParts`) when the caller needs to verify that part storage is exhausted.

Across these cases, cleanup can therefore depend on retained work state **or** on repeatable re-observation/reconciliation. What matters is not one universal queue representation but the continued ability to distinguish `work still owed` from `work closed`.

---

## 8. E — forgetting stale state can require active preservation of live state

This is the strongest Flash/SSD contribution to the synthesis.

In JFFS2, a victim erase block can contain both obsolete and current nodes. Garbage collection must preserve/rewrite still-current nodes before the block can be erased. Managed SSD GC has the same broad relation behind a different abstraction boundary: valid pages in a mixed block must be relocated before the victim block becomes reusable.

Therefore:

```text
stale embodiments identified
        +
still-live embodiments share reclamation unit
        ↓
preserve / relocate live state
        ↓
retire old embodiments
        ↓
erase / reclaim unit
```

This yields:

> **forgetting one embodiment can require producing another embodiment of what must remain.**

The statement is an engineering analogy only. JFFS2 exposes inode/node/version semantics in an open raw-Flash filesystem; a managed SSD hides proprietary mapping, victim selection, and crash recovery behind a block interface. Shared `garbage collection` vocabulary does not make the state machines identical.

---

## 9. E — negative state can need to outlive stale positive state

JFFS2 adds a relation not present in every reclamation system. After truncation/extension, explicit zero-range state can be necessary so old physical payload does not `show through` while stale nodes survive elsewhere. The negative/currentness evidence may therefore need a lifetime constrained by the stale positive state it suppresses.

Functionally related cases elsewhere in the repository include Cassandra tombstones and JBD revoke records, but this synthesis does not enlarge into a general tombstone history. The bounded point is:

> **absence of a current positive object is not always enough information to make stale older embodiments harmless.**

This guards against a simplistic model in which retirement means `delete metadata immediately, infer absence later`.

---

## 10. E — re-observation can substitute for perfect remembered delete bookkeeping

GFS's motivation for lazy garbage collection is especially useful. Chunk creation/deletion messages can be partial or lost, so the system repeatedly scans authoritative namespace state and re-observes chunkserver inventory through HeartBeat exchanges. Physical replicas not represented in current master metadata can then be treated as garbage.

The engineering lesson is not `periodic scan is better than eager deletion`. It is narrower:

> **reclamation closure can be reached by convergence over current authority plus re-observed embodiment inventory, rather than by retaining an exact durable record of every earlier delete message.**

Ceph and ext4 provide useful counterpoints because they retain more explicit unfinished-work relations. The repository should therefore distinguish at least two broad cleanup strategies:

```text
explicit retained obligation / target set
        versus
re-observation + authoritative-current-state reconciliation
```

A real system can combine both.

---

## 11. E — reuse admission is another state transition

Reclamation work and permission to reuse capacity should not be collapsed.

JFFS2 supplies the strongest explicit witness. After erase, it writes `CLEANMARKER` so the filesystem has evidence that the erase completed successfully; merely reading an erase block as all `0xFF` was not considered sufficient after power-fail experience.

Thus:

> **empty-looking != admitted for reuse**.

Managed SSD GC supplies a more opaque interface-level relation: stale pages can exist, live pages are relocated, a block is erased, and the controller returns it to its internal free pool. Host-visible free logical address space is not the same thing as a pool of already-erased physical pages ready for immediate programming.

ext3/ext4 similarly shows that namespace disappearance is weaker than allocation reuse: blocks/inodes remain allocated until delete/truncate cleanup actually updates ownership/allocation state.

So this synthesis uses **reuse admission / free-space authority** for the project-level relation that says a reclamation unit may now safely participate in future allocation. The term does not imply that every system records a JFFS2-like marker.

---

## 12. E — cleanup completion is not sanitization

This is the hard stop inherited from Synthesis 22.

GFS chunk-file deletion, ext4 block reclamation, JFFS2 erase for filesystem reuse, S3 part cleanup, managed-SSD garbage collection, and Ceph clone removal all have bounded correctness goals that are weaker than a verified media-sanitization contract.

None of the six anchor cases, merely by completing its ordinary reclamation path, establishes all of the following:

- every lower-layer cached or remapped embodiment was reached;
- every replica or spare-area copy was synchronously purged;
- cryptographic keys governing old ciphertext were destroyed;
- forensic recovery under a specified attacker model is impossible;
- independent verification has confirmed the intended sanitization scope.

Therefore:

```text
logical authority retired
    != reclamation eligible
    != cleanup complete
    != capacity reusable
    != sanitized
    != independently verified sanitized
```

Cases [`44`](../cases/44-nvme13-deallocate-sanitize-forgetting.md) and [`47`](../cases/47-fast11-ssd-sanitization-verification.md) remain the stronger forgetting/sanitization boundary.

---

## 13. A — the word `garbage collection` hides different authority layers

The grounded cases make `garbage collection` an unsafe cross-system shortcut.

### GFS

Garbage is defined through distributed namespace/chunk reachability and authoritative master metadata; later HeartBeat reconciliation exposes unneeded chunkserver replicas.

### JFFS2

Garbage consists of obsolete physical filesystem nodes sharing erase blocks with valid nodes. Version/range semantics decide currentness; raw-Flash erase geometry governs reclamation.

### Managed SSD

The host sees a block device while firmware privately manages invalid/valid physical pages, mapping state, victim blocks, erase-before-reuse constraints, and relocation workspace.

### Ceph snaptrim

The bounded operation is not named generic GC in the same way; snapshot membership and clone liveness determine what trim may remove, and cleanup is replicated/asynchronous object-system work.

The common functional relation is only:

> **some state has lost the relation that made it worth retaining, while additional work is required before its resources are safely recoverable.**

That is enough for comparison and far too little for implementation or genealogy claims.

---

## 14. A — retirement frontier and reclamation frontier are different

For comparison, the repository can use two project-level frontiers.

### Retirement frontier

The boundary behind which state no longer counts as current/reachable/admitted under the relevant logical relation.

Examples:

- a GFS stale replica no longer returned as current;
- a JFFS2 node superseded by a newer version/range;
- an S3 multipart upload ID after abort no longer accepting new construction work;
- a Ceph snapshot identifier no longer live.

### Reclamation frontier

The boundary behind which the system has discharged enough reference, preservation, cleanup, and reuse conditions that the old resource can be reclaimed or safely admitted to later allocation.

The two frontiers can move at different times.

A third frontier — **sanitization assurance** — belongs to a stronger objective and must not be silently identified with either one.

These are project analytical terms. They should not be projected backward as period vocabulary.

---

## 15. Counterexamples that keep the model honest

A useful synthesis must survive its own counterexamples.

### Counterexample 1 — retirement can be reversible

GFS default deletion initially renames a file to a hidden timestamped name and permits undelete during the grace interval. So `ordinary name retired` does not even imply `object authority fully retired` yet.

### Counterexample 2 — one retired reference may leave an object live

Ceph shared clones can remain required by another snapshot. Reference retirement is therefore not object retirement.

### Counterexample 3 — cleanup metadata can survive while target semantics are wrong

The ext4 2023 power-cut bug shows that a retained orphan entry is not sufficient if the target inode state used to interpret it is stale.

### Counterexample 4 — physical erase can preserve the higher-level object

JFFS2 and SSD GC erase old blocks after moving live state elsewhere. Erasing one embodiment can be maintenance for continued retention.

### Counterexample 5 — command success can precede verified material cleanup

S3 documents races in which in-flight part uploads may complete around abort, so callers may need to repeat abort/list operations to verify that parts are gone.

### Counterexample 6 — cleanup can converge without one durable per-object debt record

GFS relies heavily on scans and re-observed inventories. A theory that requires every reclamation system to maintain one explicit tombstone/queue per obsolete embodiment is too strong.

These counterexamples are why the synthesis is staged and relational rather than a universal finite-state-machine claim.

---

## 16. Comparison with adjacent cases

### Case 99 — ZFS snapshot reference-pinned retention

Case 99 is the clean companion for the rule `reference persists -> old block remains needed`. Case 153 adds the later asynchronous cleanup side: removing one snapshot reference may still leave another reference live, and final clone removal is separate work.

### Case 41 / Case 42 — tombstone/compaction forgetting

Cassandra tombstones and Kafka compaction show other forms of negative-state retention and delayed removal. They are not expanded here because their consistency/compaction problems already have dedicated cases. Functionally, they reinforce the rule that negative evidence can need to survive longer than the positive state it retires.

### Case 152 — SQLite WAL reader-gated reuse

SQLite WAL adds a useful observer counterexample: even when frames have been backfilled, active readers can still delay WAL reset/reuse. Payload transfer completion and reuse authority are therefore not universally the same event.

### Cases 44 / 47 — sanitization

These remain outside ordinary reclamation closure. The present synthesis routes security claims to them rather than inflating filesystem/object-store/GC deletion into a sanitization statement.

---

## 17. Related-repository division of labor

[`RELATED_REPOS.md`](../RELATED_REPOS.md) assigns historical mechanism/genealogy work primarily to `tmzncty/computing-archaeology`. Fresh searches there for `garbage collection`, `reclamation`, `JFFS2`, `ext3 orphan`, `snaptrim`, `SSD garbage collection`, and `GFS` found no dedicated cross-layer reclamation synthesis to reuse.

If such history is built later, likely divisions are:

- `computing-archaeology`: history of log-structured filesystems, Flash erase/reclaim architecture, FTL/SSD controller GC, distributed-filesystem cleanup machinery;
- `technical-retention`: authority/currentness/reference retirement, cleanup obligation, reuse admission, and cross-layer comparison;
- `problem-history`: whether historical actors framed a problem as `garbage collection`, `reclamation`, `delete safety`, `free-space recovery`, or something else in their own period vocabulary.

This synthesis should link outward rather than absorb those histories.

---

## 18. I — bounded philosophical interpretation

The engineering evidence supports one restrained interpretation:

> **Technical forgetting is often maintained work rather than a single absence.**

A system can need to retain a timestamp, orphan relation, zero-range marker, upload identity, mapping/currentness relation, snapshot membership set, trim queue, log entry, or re-observation procedure precisely because some other state is supposed to stop counting.

But the evidence does not justify the stronger slogan that `all forgetting requires memory`. Some systems can infer garbage from current authoritative state plus re-observation; some lower-layer transformations may eliminate a state without preserving a semantically rich deletion record.

The defensible project claim is narrower:

> **Where retirement, reclamation, and reuse are separated in time, correctness depends on retaining or reconstructing enough relation to know what no longer counts, what still does count, what work remains, and when reuse is safe.**

That is a technical-retention claim before it is a philosophy of memory.

---

## 19. Stop conditions and open debt

This synthesis does **not** close:

- invention genealogy of filesystem or storage garbage collection;
- exact ext3/ext4/JFFS2 historical lineage before the bounded records;
- proprietary M550 victim selection, mapping commit ordering, or power-loss GC recovery;
- S3 backend replica/part placement or physical deletion timing;
- Ceph lower-layer BlueStore/FileStore allocator reclamation after clone removal;
- all distributed-GC algorithms or tracing/reference-counting theory;
- secure deletion of every storage technology;
- proof that one project-level staged model is literally implemented by every cited system.

Those remain separate research tasks. The present slice is complete when the repository has a stable routing distinction among:

```text
retirement
eligibility
cleanup obligation
preservation of still-live state
reclamation execution
cleanup completion
reuse admission
sanitization
verification
```

and when future cases can be compared against those distinctions without being forced into one shared historical vocabulary.
