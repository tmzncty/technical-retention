# OpenStack Swift Tombstones: Deletion as Retained Negative State and Consistency-Window Reclamation

## Scope

- **Bounded system:** OpenStack Swift 2.10.1 / Newton-era object storage, released 13 December 2016.
- **Bounded mechanism:** object deletion under Swift's replicated and erasure-coded on-disk object semantics, especially timestamped `.ts` tombstones, asynchronous replication/reconstruction, `reclaim_age`, and the consistency window.
- **Primary source base:** the signed Swift `2.10.1` tag, its `overview_replication.rst`, `swift/obj/diskfile.py`, object-server configuration, and release-matched unit tests.
- **Research question:** why must a distributed storage system retain a representation of deletion after the user-visible object has already disappeared, and what authorizes that negative state itself to be forgotten?

This is **not** a general history of deletion, garbage collection, distributed databases, Swift replication, or object-store lifecycle management. It does not claim that Swift invented tombstones, eventual consistency, or delayed reclamation.

The bounded retention claim is:

> **In Swift 2.10.1, deletion is not initially the absence of retained state. A timestamped tombstone becomes the newest operational state, is propagated so that older object embodiments remain suppressed across divergent replicas, and is only later reclaimable after a configured interval intended to cover the system's consistency window.**

That sentence is an **engineering reconstruction** from Swift's documented and implemented behavior. `retained negative state`, `forgetting authority`, and `anti-resurrection obligation` below are project terms, not historical Swift vocabulary.

---

## Historical vocabulary

The release-matched Swift sources directly use:

- `tombstone`;
- `.ts`;
- `timestamp`;
- `replica`;
- `replication` / `replicator`;
- `reconstructor`;
- `latest version`;
- `consistency window`;
- `reclaim_age`;
- `reclamation`;
- `obsolete`;
- `handoff`;
- `primary`;
- `sync` / `ssync`;
- `.data`;
- `.meta`;
- `.durable` for EC state.

The following are **project engineering terms only**:

- `retained negative state` — a state whose operational meaning is that an older payload version must not be served;
- `anti-resurrection obligation` — the need to preserve/propagate deletion evidence long enough that an isolated stale replica cannot later re-establish an older payload as current;
- `forgetting authority` — the condition under which the deletion marker itself may be reclaimed without violating the intended distributed state;
- `negative-state convergence` — replica convergence on deletion rather than on a positive payload.

---

## Historical record

### H/P — Swift 2.10.1 is a signed Newton-era release

The Git tag `2.10.1` is an annotated release tag created by the OpenStack Release Bot on **2016-12-13 19:15:44 UTC** and points to commit `3129a55d4418e0dc4207c2026e7ef8c59704c6a1`.

This case is therefore release-scoped. Later Swift documentation may clarify risks, but later terminology is not silently projected backward into the 2016 mechanism.

**Primary anchor:** OpenStack Swift annotated tag `2.10.1`.

### H/P — Swift says deletion is replicated by retaining a tombstone as the latest version

The release-matched replication documentation states that every deleted record or file is marked by a **tombstone so that deletions can be replicated alongside creations**. It also says the replicator ensures data is removed from the system by seeing the tombstone and propagating that state.

The architectural overview for the same release family describes the tombstone as the **latest version** of the item.

That historical wording directly blocks the shortcut:

```text
DELETE succeeded
    -> nothing remains
```

For the distributed consistency machinery, something must remain: a timestamped negative fact that can defeat an older positive copy.

**Primary anchors:** Swift `2.10.1`, `doc/source/overview_replication.rst`; release-matched architectural overview.

### H/P — the object-server implementation materializes deletion as a `.ts` file

In `swift/obj/diskfile.py`, `DiskFile.delete(timestamp)` creates a new on-disk file whose extension is `.ts` and whose metadata contains the delete timestamp. The implementation is explicit: the operation **creates a tombstone file using the given timestamp**.

The same file-selection code sorts candidate files by timestamp and makes the newest tombstone authoritative against older or equal-timestamp non-tombstone state. Older/equal `.data`, `.meta`, and, for EC, `.durable` state becomes obsolete relative to that tombstone.

**Primary anchor:** Swift `2.10.1`, `swift/obj/diskfile.py`, `DiskFile.delete` and on-disk-file selection logic.

### H/P — release-matched tests enforce tombstone precedence over payload and metadata

The `2.10.1` unit tests encode the same precedence rules as executable implementation evidence:

- an older tombstone is ignored when a newer tombstone exists;
- older data is ignored when a newer tombstone exists;
- a tombstone at the same timestamp trumps `.meta` and `.data`;
- in the EC diskfile tests, a tombstone also trumps older or same-timestamp `.durable` and fragment `.data` files;
- a tombstone can be the only object state yielded for synchronization.

These tests matter because they show that the negative marker is not decorative metadata. It participates directly in deciding which retained embodiment is currently admissible.

**Primary anchor:** Swift `2.10.1`, `test/unit/obj/test_diskfile.py`.

### H/P — reclamation is delayed by `reclaim_age`

The same implementation contains `cleanup_ondisk_files(hsh_path, reclaim_age=ONE_WEEK, ...)`, where `ONE_WEEK` is `604800` seconds. A tombstone is removed only when its timestamp is older than `reclaim_age`; fresh tombstones remain.

The release-matched `object-server.conf-sample` documents that the object replicator **also performs reclamation** and gives `reclaim_age = 604800` as the sample/default interval. The EC reconstructor section exposes the same setting.

The unit tests explicitly distinguish fresh tombstones from reclaimable old tombstones under a configured age threshold.

**Primary anchors:** Swift `2.10.1`, `swift/obj/diskfile.py`; `etc/object-server.conf-sample`; `test/unit/obj/test_diskfile.py`.

### H/P — Swift names the retention interval a `consistency window` and ties cleanup to convergence

The 2.10.1 replication documentation states that the replication process cleans up tombstones after a time period known as the **consistency window**. It defines that window in terms of replication duration and the time a transient failure can remove a node from the cluster, then states that **tombstone cleanup must be tied to replication to reach replica convergence**.

This is the strongest direct historical evidence in the bounded case. Tombstone lifetime is not presented simply as disk-space housekeeping. It is coupled to the period in which deletion still has to propagate across potentially divergent replicas.

**Primary anchor:** Swift `2.10.1`, `doc/source/overview_replication.rst`.

### H/P — temporary failures can leave replicas divergent before asynchronous maintenance converges them

The same document says each replica functions independently and that transient failures such as network partitions can quickly cause replicas to diverge. Asynchronous peer-to-peer replication later reconciles those differences. The storage node holding data has a responsibility to push it toward where it belongs.

A deletion can therefore coexist temporarily with an isolated older copy elsewhere. The tombstone's job is meaningful precisely because distributed state is not assumed to change everywhere at one instant.

**Primary anchor:** Swift `2.10.1`, `doc/source/overview_replication.rst`.

---

## Retained state

The bounded deletion regime retains more than either `object bytes` or `nothing`.

### 1. Object identity

The account/container/object path continues to designate the logical object even when the current outcome of lookup is deletion/nonexistence.

### 2. Positive payload embodiments

Older `.data` files or EC fragment archives may still physically exist on some replicas during asynchronous convergence or temporary failure.

### 3. Delete timestamp

Timestamp ordering establishes whether a tombstone is newer than competing positive state.

### 4. Tombstone embodiment

The `.ts` file is the local on-disk representation of the deletion state.

### 5. Replica-placement / synchronization relations

The ring, primary/handoff relationships, and replication/reconstruction machinery determine where deletion evidence must travel.

### 6. Reclamation policy state

`reclaim_age` determines when the system considers an old tombstone eligible for physical removal.

The user-visible object may therefore be absent while the system still has to retain a non-payload relation that says **which older embodiments no longer count**.

---

## Physical / logical substrate

The bounded mechanism spans:

- timestamped files in object hash directories;
- `.data`, `.meta`, `.ts`, and, for EC, `.durable` / fragment-indexed files;
- per-object file-selection logic;
- partition/suffix hashes used by replication or reconstruction;
- ring-derived replica placement;
- asynchronous replicator/reconstructor passes;
- an operator-configurable reclamation interval.

The negative state is material in an ordinary sense — it is a file and metadata on storage devices — but its operational meaning is relational: **newer tombstone timestamp defeats older positive object timestamp**.

---

## Retention mechanism

### During DELETE

The object server writes a timestamped tombstone and removes or marks older local object versions obsolete according to the on-disk selection rules.

### During divergence

A remote replica may still hold an older payload. The tombstone remains a synchronizable state so asynchronous maintenance can communicate that the positive embodiment is no longer current.

### During convergence

Replication/reconstruction propagates the newest relevant object state until replicas agree sufficiently for the system's intended consistency behavior.

### During reclamation

After the tombstone exceeds `reclaim_age`, cleanup code may remove the `.ts` file. At that point the system is no longer depending on that local marker to suppress older state in the bounded expected failure window.

This final sentence is an **engineering reconstruction**, not an assertion that elapsed time magically proves global convergence. The historical documentation itself says cleanup must be tied to replication.

---

## Addressing and access geometry

A simplified object lookup relation is:

```text
account/container/object
    -> storage policy + ring
    -> candidate replica/handoff locations
    -> timestamped local object-state files
    -> compare newest admissible .data/.meta/.ts(/.durable)
    -> if newest authoritative state is tombstone: object is deleted
```

Deletion therefore preserves the logical designation while changing which state is admissible under that designation.

This is different from physical-address erasure. The object name remains meaningful enough for the system to answer that its latest state is deletion.

---

## Read semantics

A read after deletion does not need to recover application payload in order to depend on retained state. It depends on the timestamp/currentness relation that prevents an older payload from being treated as the present object.

The negative result is therefore state-sensitive:

```text
same logical object name
    + newer tombstone
    -> older payload is not a valid current answer
```

This case does not claim that every 404 response in Swift proves the presence of a local tombstone. It analyzes the bounded replicated-deletion path in which tombstones carry the distributed delete relation.

---

## Write and erasure semantics

A Swift DELETE in this regime performs several conceptually different operations:

1. create a newer negative object version (`.ts`);
2. make older local payload/metadata states obsolete relative to it;
3. propagate the negative version through distributed maintenance;
4. eventually reclaim the tombstone itself after the configured age condition.

These must not be collapsed into one word `erase`.

In particular:

- tombstone creation is **not physical sanitization** of every old payload block;
- logical deletion can precede physical removal of every stale positive embodiment;
- tombstone reclamation is a second-order forgetting operation — the system forgets the fact that it previously needed to say `deleted` only after that fact has served its convergence role.

---

## Time

Relevant timescales include:

- client DELETE request/response time;
- time during which replicas can diverge;
- replication/reconstruction pass intervals;
- duration of transient node/network unavailability;
- the configured `reclaim_age` / consistency-window scale;
- later filesystem/media reclamation of obsolete bytes.

This is not a DRAM-style physical decay deadline. It is a **protocol/failure/maintenance deadline** whose purpose is to keep negative state available while older positive state may still re-enter the synchronization graph.

---

## Maintenance and labor

Deletion persistence depends on work that is invisible to the client API:

- timestamp generation and comparison;
- tombstone creation;
- suffix/hash invalidation;
- replication/reconstruction scans;
- network synchronization;
- handoff handling;
- cleanup/reclamation;
- operator choice of a reclamation window compatible with actual failure and replication behavior.

The system therefore spends storage and maintenance effort to make `nothing` remain the correct answer.

---

## Failure / forgetting modes

Keep these distinct:

- tombstone write failure;
- stale replica isolated during DELETE;
- failed or delayed propagation of the tombstone;
- clock/timestamp ordering mistakes that alter currentness comparison;
- reclamation before an operationally sufficient convergence interval;
- stale positive data surviving physically after logical deletion;
- loss/corruption of ring or synchronization state needed to reach the relevant replica;
- EC fragment/durability-state interactions where a tombstone must suppress a prior coded cohort;
- physical trace survival after the object is no longer logically current;
- secure-erasure failure, which this case does **not** test.

The important project distinction is:

> **logical deletion failure, distributed convergence failure, tombstone-reclamation failure, and media-sanitization failure are different failure classes.**

---

## Engineering reconstruction

### E — deletion can require retention

Swift supplies a strong counterexample to the intuitive opposition `retention versus deletion`.

The object payload is to be forgotten as current state, yet the system must temporarily retain a **newer negative state** to make that forgetting stable across asynchronous replicas.

### E — absence ≠ distributed proof of absence

A local node that no longer stores positive bytes cannot by local absence alone tell a disconnected peer that its older object should be discarded. A synchronizable tombstone supplies an ordered statement that can defeat stale positive state.

### E — forgetting can have a second stage

The first forgetting event deauthorizes/removes the positive object. The later reclamation event removes the evidence that had been required to maintain that negative state.

So:

```text
payload retirement
    ≠ tombstone retirement
```

### E — reclamation age is part of consistency risk, not merely capacity policy

Because the historical docs tie tombstone cleanup to the consistency window, `reclaim_age` participates in the system's correctness envelope. A shorter interval saves retained control state sooner; a longer interval preserves more anti-resurrection evidence and consumes more space/scan work.

This is a bounded engineering consequence of Swift's own coupling, not a universal formula for every eventually consistent store.

### E — negative state has version semantics

The tombstone wins because it is ordered against `.data`, `.meta`, and EC state by timestamp. `Deleted` is therefore not represented as timeless emptiness. It is a **versioned state transition**.

---

## Philosophical / media-theoretical interpretation

This case sharpens a narrow problem of technical forgetting:

> **A system may have to remember that something is to be forgotten.**

That sentence is not a claim about human memory or Derridean trace by itself. The exact technical fact is more modest: a distributed object store retains a timestamped negative marker because mere local absence cannot safely suppress older positive replicas during asynchronous convergence.

The case therefore disciplines two easy metaphors:

- `forgetting = disappearance` is technically false in the bounded regime;
- `retention = preservation of positive content` is also too narrow.

A retained relation can preserve **non-admissibility** rather than payload.

For Stiegler or archival theory, no stronger philosophical equivalence follows automatically. The tombstone is machine-operational control state; whether a human/social practice of deletion or institutional forgetting should be read through it requires a separate argument.

---

## Functional analogies

### A — tombstone and Flash invalidation

Case 04 mapped Flash and Case 28 Swift both show a logical object becoming noncurrent before all old physical traces are necessarily erased.

The analogy stops there:

- Flash invalidation/reclamation occurs inside a mapped storage device under erase-unit geometry;
- Swift tombstones are timestamped distributed object versions propagated among replicas;
- neither establishes a historical genealogy to the other.

### A — tombstone and cache/VM currentness metadata

Like cache validity bits or VM change/currentness state, a Swift tombstone helps determine which embodiment counts. But a tombstone is itself a versioned negative object-state artifact that must be synchronized across failure domains; the historical mechanisms and failure conditions differ.

### A — tombstone and Dynamo divergent versions

Case 23 allows multiple causally unrelated positive versions to remain simultaneously admissible until reconciliation. Swift's bounded tombstone case instead gives one newer deletion timestamp authority to suppress older object state. Both make `currentness` relational, but their version semantics are not the same.

---

## Counterexamples and limits

This case does **not** establish:

- that Swift invented distributed tombstones;
- that every Swift DELETE is secure physical erasure;
- that elapsed `reclaim_age` proves every replica has converged;
- that tombstones are unique to eventually consistent stores;
- that all negative information must be stored as a separate file;
- that deletion markers are archival records intended for human recovery;
- that the same semantics apply unchanged to later Swift releases;
- that one consistency-window value is safe for every deployment;
- that object tombstones, account/container deletion records, object expiration, versioning, or legal-retention policies are one mechanism.

Later Swift documentation explicitly warns about stale data reappearing as `dark data` when a node returns after the tombstone-reclamation window. That later wording is useful corroboration of the risk model, but it is not used here as if the phrase were part of the 2016 historical vocabulary.

---

## Prior-art boundary

Deletion markers/tombstones and delayed physical reclamation predate this bounded Swift release in storage/database systems. The case therefore makes **no invention-priority claim** for Swift.

The repository's contribution is narrower:

- a release-scoped primary-source account of how Swift makes deletion itself a retained, timestamp-ordered, synchronizable state;
- a comparison between payload retirement and deletion-marker retirement;
- a mechanism-level example in which the system's ability to forget positive content depends temporarily on preserving negative control state.

Broader genealogy of tombstones, LSM compaction, anti-entropy deletion, and database garbage collection belongs in `computing-archaeology` or a dedicated history, not in this case.

---

## Related repositories

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Swift`, `tombstone`, `reclaim_age`, and distributed delete semantics found no dedicated case to reuse at this point. This file therefore keeps only the retention-specific argument and does not attempt a general Swift history.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the methodological warning: `retained negative state` is our reconstruction, not a period problem label attributed to Swift developers.

---

## Claim ledger

| Claim | Label | Evidence / boundary |
| --- | --- | --- |
| Swift 2.10.1 represents deleted objects with timestamped tombstone files | H/P | release-matched `diskfile.py` and docs |
| tombstones are propagated so deletions can converge across divergent replicas | H/P | `overview_replication.rst` |
| the latest tombstone suppresses older/equal positive on-disk states | H/P | `diskfile.py` + unit tests |
| tombstones are reclaimed only after `reclaim_age` | H/P | implementation, config sample, tests |
| Swift names the relevant interval a consistency window and ties cleanup to replication | H/P | `overview_replication.rst` |
| deletion can require retaining a negative state | E | reconstruction from above mechanism |
| payload retirement is distinct from tombstone retirement | E/A | direct implementation sequencing; project comparison |
| tombstone creation is secure physical erasure | X | unsupported and explicitly rejected |
| elapsed reclaim age proves universal convergence | X | unsupported; historical docs make cleanup dependent on replication/failure assumptions |
| Swift invented tombstones | X | no priority evidence; explicitly rejected |

---

## Sources

### Primary / release-matched

1. OpenStack Swift, annotated Git tag `2.10.1`, 13 December 2016: <https://api.github.com/repos/openstack/swift/git/ref/tags/2.10.1>.
2. OpenStack Swift `2.10.1`, `doc/source/overview_replication.rst`: <https://github.com/openstack/swift/blob/2.10.1/doc/source/overview_replication.rst>.
3. OpenStack Swift `2.10.1`, `swift/obj/diskfile.py`: <https://github.com/openstack/swift/blob/2.10.1/swift/obj/diskfile.py>.
4. OpenStack Swift `2.10.1`, `etc/object-server.conf-sample`: <https://github.com/openstack/swift/blob/2.10.1/etc/object-server.conf-sample>.
5. OpenStack Swift `2.10.1`, `test/unit/obj/test_diskfile.py`: <https://github.com/openstack/swift/blob/2.10.1/test/unit/obj/test_diskfile.py>.
6. OpenStack Swift 2.10.1 documentation root: <https://docs.openstack.org/swift/2.10.1/>.

### Later corroborating boundary only

7. OpenStack Swift current/later object-server configuration documentation, `reclaim_age` warning about the consistency-engine window and stale `dark data`: <https://docs.openstack.org/swift/latest/config/object_server_config.html>. This source is **not** used to project later wording into the 2016 release; it only corroborates the continuing engineering risk of reclaiming deletion evidence before stale nodes have been safely dealt with.

---

## Status

**grounded** — the central mechanism is supported by a signed release boundary, release-matched project documentation, implementation source, configuration, and executable unit-test evidence. The case makes no tombstone-invention claim and keeps secure erasure, later Swift evolution, account/container deletion, object expiration, and broader database tombstone history outside scope.
