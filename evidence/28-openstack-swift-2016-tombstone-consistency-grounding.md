# Grounding Record 28 — OpenStack Swift 2.10.1 Tombstones, Consistency Window, and Reclamation

## Purpose

Ground Case 28 against a **release-scoped primary source set** and keep three relations separate:

1. user-visible deletion / currentness;
2. distributed propagation of deletion evidence;
3. later reclamation of the deletion marker itself.

The bounded release is **OpenStack Swift 2.10.1 (Newton), 13 December 2016**.

---

## Evidence maturity

**Case status:** `grounded`.

The central claims do not depend on a retrospective blog post or generic description of eventual consistency. They are supported by:

- the annotated release tag;
- release-matched project documentation;
- release-matched implementation source;
- release-matched configuration;
- release-matched executable unit-test expectations.

A later Swift configuration warning is retained only as a **later corroborating boundary**, not as evidence of 2016 historical vocabulary.

---

## Primary anchor A — release identity

### Source

OpenStack Swift Git ref/tag:

- ref: `refs/tags/2.10.1`;
- tag object: `388b89f64f64fc72be968d1438fcdce5caa3ca6a`;
- target commit: `3129a55d4418e0dc4207c2026e7ef8c59704c6a1`;
- tagger: OpenStack Release Bot;
- tagger date: **2016-12-13T19:15:44Z**;
- release series in tag message: `newton`.

### Stable locations

- <https://api.github.com/repos/openstack/swift/git/ref/tags/2.10.1>
- <https://api.github.com/repos/openstack/swift/git/tags/388b89f64f64fc72be968d1438fcdce5caa3ca6a>

### Claim supported

This establishes the exact release boundary used by the case. It prevents later Swift behavior from being treated as if it were timeless 2016 semantics.

### Strength

**Strong primary project metadata.**

---

## Primary anchor B — replication documentation

### Source

OpenStack Swift `2.10.1`:

`doc/source/overview_replication.rst`

<https://github.com/openstack/swift/blob/2.10.1/doc/source/overview_replication.rst>

The fetched source is release-matched; repository metadata reports a modification date of 7 July 2016 for this file at the tag.

### Directly inspected statements

The document establishes the following in Swift's own period vocabulary:

1. replicas function independently;
2. temporary conditions such as network partitions can cause replica divergence;
3. asynchronous peer-to-peer replicators reconcile those differences;
4. deleted records/files are marked by a **tombstone** so deletion can be replicated alongside creation;
5. tombstones are cleaned after a period called the **consistency window**;
6. that window encompasses replication duration and how long transient failure may remove a node from the cluster;
7. tombstone cleanup **must be tied to replication to reach replica convergence**;
8. object replication is push-oriented; a node that contains relevant state bears responsibility for getting it where it belongs;
9. EC policies use the reconstructor rather than the replication daemon, but the same release documentation treats hashes/state comparison as durability-maintenance machinery.

### Claims supported

- deletion is represented as retained synchronizable state;
- replica divergence gives that state a distributed purpose;
- tombstone lifetime is coupled to convergence/failure assumptions rather than being pure local space cleanup;
- physical absence on one node is not by itself the distributed deletion protocol.

### Strength

**Strong primary project documentation.** This is the central historical-language anchor for `tombstone`, `consistency window`, `replication`, and convergence.

---

## Primary anchor C — on-disk implementation

### Source

OpenStack Swift `2.10.1`:

`swift/obj/diskfile.py`

<https://github.com/openstack/swift/blob/2.10.1/swift/obj/diskfile.py>

### Directly inspected implementation points

#### 1. Default reclamation scale

The module defines:

```text
ONE_WEEK = 604800
```

The disk-file manager reads `reclaim_age`, defaulting to `ONE_WEEK`.

#### 2. Delete creates a tombstone file

`DiskFile.delete(timestamp)` converts the timestamp and creates a file through the ordinary diskfile writer path with extension:

```text
.ts
```

The method's docstring says the implementation **creates a tombstone file using the given timestamp**.

#### 3. Tombstone participates in currentness selection

The on-disk-file selector sorts extensions in reverse chronological order. When one or more `.ts` files exist:

- non-tombstones older than or equal to the newest tombstone are classified obsolete;
- all but the newest tombstone are obsolete;
- if no later valid data file is chosen, the tombstone is returned as the current `ts_info` state.

This is stronger than simply saying a delete marker is stored. It shows that timestamped negative state directly participates in determining which local embodiment counts.

#### 4. Tombstone reclamation is age-gated

`cleanup_ondisk_files(hsh_path, reclaim_age=ONE_WEEK, ...)` defines reclaimability by comparing wall-clock time to the tombstone timestamp. A tombstone is physically removed only when it is older than the configured reclamation age.

### Claims supported

- `.ts` is a concrete retained embodiment of deletion;
- delete currentness is timestamp ordered;
- older/equal positive states can become obsolete because of the tombstone relation;
- tombstone retirement is a later operation distinct from payload deauthorization;
- `reclaim_age` is operative implementation state, not just documentation prose.

### Strength

**Strong primary implementation evidence.** No claim is made that the Python implementation is a universal object-store architecture.

---

## Primary anchor D — object-server configuration

### Source

OpenStack Swift `2.10.1`:

`etc/object-server.conf-sample`

<https://github.com/openstack/swift/blob/2.10.1/etc/object-server.conf-sample>

### Directly inspected configuration points

Under `[object-replicator]` the release-matched sample says:

- the replicator also performs reclamation;
- sample/default `reclaim_age = 604800`.

The `[object-reconstructor]` section also exposes `reclaim_age = 604800` for EC maintenance.

### Claims supported

- reclamation is tied operationally to distributed maintenance components;
- one-week retention of tombstone/control state is a configurable policy scale in this release;
- the interval is not a physical medium-decay constant.

### Boundary

The sample value is **not** treated as a universally safe value or as proof that all 2016 deployments used exactly one week.

### Strength

**Strong primary operational/configuration evidence.**

---

## Primary anchor E — executable unit-test expectations

### Source

OpenStack Swift `2.10.1`:

`test/unit/obj/test_diskfile.py`

<https://github.com/openstack/swift/blob/2.10.1/test/unit/obj/test_diskfile.py>

### Directly inspected test expectations

The release-matched tests cover the following scenarios:

- a fresh tombstone is preserved while an old tombstone is reclaimed under a configured age threshold;
- older tombstones lose to newer tombstones;
- older data loses to a newer tombstone;
- a tombstone at the same timestamp trumps `.meta` and `.data`;
- in the EC diskfile tests, a tombstone trumps older or same-timestamp `.durable` and indexed fragment `.data` files;
- a state set can be constructed in which **only the tombstone is yield/sync-able**.

### Claims supported

These tests independently reinforce the release implementation's intended invariants:

- tombstone precedence is part of correctness behavior, not incidental file naming;
- the negative state is synchronization material;
- EC durability files do not automatically override a newer delete marker;
- reclamation is intentionally delayed.

### Strength

**Strong primary executable project evidence.** Tests demonstrate intended behavior but are not treated as measurements of a production cluster.

---

## Secondary / later corroboration — do not back-project terminology

### Source

Current/later OpenStack Swift object-server configuration documentation:

<https://docs.openstack.org/swift/latest/config/object_server_config.html>

### Later wording

Later documentation describes `reclaim_age` as the maximum window for the consistency engine and explicitly warns that reintroducing a node after that interval without purging stale data can result in `dark data`.

### Use in this case

Only as **later corroboration** of the engineering risk already implied by the 2016 rule that tombstone cleanup must be tied to the consistency window and replica convergence.

The phrase `dark data` is **not** attributed to Swift 2.10.1 unless independently found in a 2016 source.

---

## Engineering reconstruction derived from the source set

The following are project conclusions, not period quotations.

### E1 — deletion can create a retention obligation

Because a replica can be offline while deletion occurs, deleting the positive payload locally is insufficient to communicate that older remote state is no longer current. The system therefore retains a newer negative state that can be synchronized.

### E2 — `absence` and `negative currentness` are distinct

Local absence has no version order. A timestamped tombstone does. In this bounded Swift regime, the latter is what can defeat an older positive embodiment during synchronization/currentness selection.

### E3 — payload retirement and tombstone retirement are different forgetting events

The object can cease to be a valid current payload before the tombstone is reclaimable. The tombstone persists because the system still needs evidence of the earlier deletion transition.

### E4 — the reclamation interval is a correctness/capacity tradeoff

Longer retention spends more storage/scan work on negative state. Earlier reclamation removes that state sooner but narrows the interval in which disconnected stale embodiments are expected to be safely suppressed by the deletion marker.

The case does **not** turn this into a probability formula or universal optimal window.

### E5 — the retained object state is relational

Currentness depends on at least:

```text
logical object identity
+ timestamp order
+ local state kind (.data/.meta/.ts/.durable)
+ replica placement/synchronization
+ reclamation policy
```

The tombstone is therefore best analyzed as retained control/currentness state rather than as a zero-length replacement payload.

---

## Cross-case controls

### Case 04 — mapped Flash

**Functional analogy only:** both regimes can logically invalidate/deauthorize an older positive embodiment before every physical trace is erased.

Do not merge the mechanisms. Flash invalidation/reclamation is constrained by device mapping and erase geometry; Swift deletion is timestamped distributed version state.

### Case 23 — Dynamo

Both expose currentness as a relation among versions and maintenance state. Dynamo can retain causally incomparable positive leaves; Swift's bounded tombstone regime uses timestamp ordering so a newer negative state suppresses older payload embodiments. No claim of identical consistency semantics is made.

### Case 25 — Swift mutable EC

Case 25 asks **which positive coded cohort is committed/admissible**. Case 28 asks **how a later negative version suppresses an older positive object and how long the negative state itself must remain**. They share release artifacts but answer different retention questions.

### Case 27 — Ceph integrity authority

Case 27 is about qualifying extant coded payload as trustworthy after checksum inconsistency. Case 28 is about retaining a negative currentness state. `integrity verification` and `distributed deletion` are not one maintenance mechanism.

---

## Prior-art / novelty boundary

No evidence in this record supports:

- `Swift invented tombstones`;
- `Swift invented eventual consistency`;
- `Swift invented delayed reclamation`.

The contribution is a **bounded mechanism study**, not an invention-priority claim.

A repository search of `tmzncty/computing-archaeology` for `Swift`, `tombstone`, `reclaim_age`, and distributed deletion found no dedicated technical-history slice to reuse. If a broader tombstone/LSM/database genealogy is built later, it should primarily live there and this case should retain only its distributed-retention comparison.

---

## Rejected shortcuts

| Shortcut | Status | Reason |
| --- | --- | --- |
| `delete = immediate physical erasure everywhere` | rejected | tombstone and asynchronous convergence directly contradict it |
| `no local data = distributed deletion has converged` | rejected | disconnected divergent replicas are part of the documented failure model |
| `tombstone = payload` | rejected | it is a timestamped control/currentness artifact with different semantics |
| `reclaim_age = physical retention lifetime` | rejected | it is a configurable protocol/maintenance interval |
| `old tombstone removed = secure sanitization complete` | rejected | no raw-media secure-erasure evidence in the bounded case |
| `one week is universally safe` | rejected | configuration is deployment-dependent and tied to replication/failure assumptions |
| `Swift 2.10.1 semantics = all later Swift` | rejected | case is release-scoped |

---

## Evidence-strength summary

| Claim | Evidence | Strength |
| --- | --- | --- |
| release/date boundary | annotated tag | strong primary |
| deletion is represented by tombstone and replicated | 2.10.1 replication docs | strong primary |
| `.ts` materialization | 2.10.1 implementation | strong primary |
| timestamp precedence over old payload | implementation + tests | strong primary |
| age-gated tombstone reclamation | implementation + config + tests | strong primary |
| cleanup tied to consistency window / convergence | 2.10.1 replication docs | strong primary |
| deletion requires temporary negative-state retention | engineering reconstruction | strong, explicitly reconstructed |
| premature reclamation can enable stale-state return | engineering reconstruction + later official warning | bounded; later wording not back-projected |
| secure erasure | not established | rejected/out of scope |
| invention priority | not established | rejected/out of scope |

---

## Grounding decision

**Promote/use as `grounded`.**

The case has a precise release boundary, period vocabulary, source-level mechanism, executable expectations, a failure/convergence rationale, explicit prior-art limits, and related-repository duplication checking. No remaining source gap blocks the bounded retention claim.
