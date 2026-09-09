# Case 25 deepening — Swift 2.28.0 `commit_window`, in-flight non-durable fragments, and cleanup authority (2021)

## Purpose

This addendum deepens [`Case 25 — OpenStack Swift EC Overwrites`](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md) at one narrowly bounded seam left open by the 2015–2016 grounding:

> **When an EC fragment is not durable yet, when is it actually safe for background cleanup to delete it?**

The answer is not simply `when its object timestamp is old` or `when it lacks durable status`. Swift's 2021 fix for Bug `#1936508`, together with the immediately preceding handoff-race change and the Swift 2.28.0 release record, shows that a freshly written non-durable fragment can have an intentionally old logical `X-Timestamp` while still being in the middle of a valid PUT/commit transition. Background cleanup that reasons only from the logical timestamp can therefore destroy a fragment that is **about to become durable**.

This record is deliberately **not** a general history of Swift's reconciler, container-sync, handoff reversion, reclaim policy, filesystem `mtime`, or EC durability. It adds one implementation-level concurrency/currentness boundary to the already-grounded Case 25.

---

## Source set

### P1 — development change: handoff reversion purge delay, 24 June 2021

OpenStack Swift commit `2934818d608e6cedd30ecb81900d02969476275c`, **2021-06-24**, `reconstructor: Delay purging reverted non-durable datafiles`:

<https://github.com/openstack/swift/commit/2934818d608e6cedd30ecb81900d02969476275c>

The commit records a race in which the reconstructor can revert a non-durable data file from a handoff concurrently with an object-server PUT that is about to make that same file durable. Immediate purge can delete the recently written file before the object server performs the durable rename. The development fix introduces an `mtime`-based delay named `nondurable_purge_delay`, default 60 seconds.

**Chronology guardrail:** P3 below explicitly says this option was **never present in a tagged release**; it is development-history evidence, not released operator vocabulary.

### P2 — Bug #1936508 fix: `commit_window`, 19 July 2021

OpenStack Swift commit `bbaed18e9b681ce9cf26ffa6a5d5292f5cb219b7`, **2021-07-19**, `diskfile: don't remove recently written non-durables`:

<https://github.com/openstack/swift/commit/bbaed18e9b681ce9cf26ffa6a5d5292f5cb219b7>

The commit message directly states the failure mechanism:

- `cleanup_ondisk_files()` treats tombstones and non-durable EC data fragments older than `reclaim_age` as stale/reclaimable;
- an agent may intentionally PUT an object with an older `X-Timestamp`, with the reconciler and container-sync named as examples;
- there is then a window after the old-timestamp `.data` file has been freshly written but before it has been committed/durable;
- another process such as the reconstructor can call cleanup during this interval and remove the data file;
- the later commit/rename then fails because the file no longer exists, and the commit message explicitly says the data file is lost.

The patch adds `commit_window`, default `60.0` seconds, and changes cleanup so an otherwise reclaimable **non-durable** file is protected when its filesystem modification time is still inside that window.

The code therefore uses two different time relations for two different questions:

1. the object's logical timestamp participates in stale/reclaim eligibility;
2. local filesystem `mtime` supplies a freshness guard for whether the physical file may still be part of an in-flight commit transition.

### P3 — development cleanup: one released `commit_window`, 19 July 2021

OpenStack Swift commit `2696a79f098b02988136b13caf1c2565ec09481f`, **2021-07-19**, `reconstructor: retire nondurable_purge_delay option`:

<https://github.com/openstack/swift/commit/2696a79f098b02988136b13caf1c2565ec09481f>

This change says the earlier `nondurable_purge_delay` had **not been available in any tagged release**. It removes that separate option and reuses the DiskFileManager's `commit_window` for reconstructor handoff cleanup. The sample configuration is simultaneously sharpened to say that `commit_window` also prevents the reconstructor from removing recently written non-durable files from a handoff after reversion, giving the object server time to finish a concurrent PUT and mark the data durable.

This is useful source criticism: a commit can be historically real and technically informative without its temporary configuration name ever becoming released public interface vocabulary.

### P4 — Swift 2.28.0 release tag, 27 July 2021

The annotated `2.28.0` tag was created by the OpenStack Release Bot on **2021-07-27T09:59:25Z** and points to commit `a8f15128639f7e62a3e8d51c607b45c496206191`:

<https://github.com/openstack/swift/tree/2.28.0>

A direct commit comparison shows P2 is an ancestor of that release commit. The 2.28.0 changelog lists `commit_window` under **Erasure coding fixes** and says the delay improves durability for both:

- back-dated PUTs such as reconciler/container-sync writes; and
- fresh writes to handoffs,

by preventing the reconstructor from deleting data the object server was still writing.

Primary release text:

<https://github.com/openstack/swift/blob/2.28.0/CHANGELOG>

---

## Historical record (`H/P`)

### H/P1 — an old logical object timestamp can describe a freshly created physical file

P2 does not treat a back-dated PUT as malformed merely because `X-Timestamp` is older than `reclaim_age`. It names reconciler and container-sync as legitimate examples of agents that may write with older timestamps.

Therefore, in this bounded implementation:

```text
old object timestamp
    !=
old local file incarnation
```

This is a direct implementation distinction, not a general claim about all object stores.

### H/P2 — non-durable can mean `in transition`, not `failed forever`

P1 and P2 both describe a non-durable fragment that the object server is still expected to make durable. Its lack of durable status is therefore not sufficient evidence that cleanup may delete it immediately.

### H/P3 — cleanup could previously destroy the future commit candidate

P2 states that a concurrent cleanup could remove the data file before the later commit rename and that the data file would be lost. This is stronger than a theoretical race reconstruction: the project's own fix record names the concrete destructive ordering.

### H/P4 — Swift 2.28.0 exposes a bounded grace relation via `commit_window`

The released configuration uses a default 60-second `commit_window`. For non-durable data otherwise old enough for reclamation, recent filesystem `mtime` temporarily vetoes removal.

The release documentation recommends a value greater than zero and much less than `reclaim_age`.

### H/P5 — the same released option is reused for handoff cleanup

P3 removes the separate unreleased purge-delay setting and makes the reconstructor use DiskFileManager `commit_window` when deciding whether a reverted non-durable handoff fragment is old enough to remove.

The release-facing relation is therefore one `commit_window` serving two closely related cleanup races, not two independently standardized mechanisms.

---

## Engineering reconstruction (`E`)

### E1 — logical version age != physical-write age

Case 25 already treats timestamp as part of version/currentness selection. The 2021 fix adds another time coordinate: the age of the **local file incarnation** involved in a commit transition.

A fragment can therefore be logically old while physically new.

### E2 — reclaim eligibility != immediate deletion authority

An object timestamp can satisfy `reclaim_age` while an in-flight write still makes deletion unsafe. `commit_window` adds a phase-sensitive veto to a broader stale/reclaim rule.

The useful project relation is:

```text
eligible by long-term reclamation policy
    !=
safe to delete at this instant
```

### E3 — non-durable != discardable-now

`non-durable` identifies a current protocol/ondisk status; it does not by itself distinguish:

- abandoned stale debris that should eventually be reclaimed; from
- a freshly written candidate that has not yet crossed the durable transition.

The mtime grace provides extra evidence about which interpretation is temporarily safer.

### E4 — `commit_window` is a preservation guard, not a durability witness

A file surviving inside `commit_window` is **not thereby committed**. The window merely prevents cleanup from destroying a candidate while a concurrent commit may still complete.

Therefore:

```text
protected from cleanup
    !=
durable / service-admissible object version
```

This keeps the 2021 mechanism separate from Case 25's `.durable` / durable-filename relation.

### E5 — local mtime recency != logical currentness

The same separation works in the other direction. A recent filesystem `mtime` can protect a fragment from cleanup without proving that its object timestamp is the newest admissible version, that an EC quorum exists, or that the client PUT succeeded.

### E6 — transition safety can depend on retaining a not-yet-authoritative embodiment

The pre-commit fragment is not yet sufficient to serve as the committed object, but deleting it too early can prevent the system from completing the transition that would make the new state authoritative. This extends Case 25's earlier distinction from `fragment presence != committed retention` to:

> **not-yet-authoritative state can still be necessary retention infrastructure for an unfinished authority transition.**

### E7 — cleanup policy composes long and short timescales

`reclaim_age` and `commit_window` do not describe one clock with two names. The first controls long-lived stale-state reclamation; the second is a short concurrency grace keyed to local file-write recency. Their composition prevents a legitimate old logical timestamp from being mistaken for an old physical write.

---

## Functional analogies (`A`) — bounded only

### A1 — Case 24 representation handoff

Case 24's Windows Azure LRC witness preserves old full replicas until a new coded representation has passed its transition/validation boundary. Swift's 2021 race is much narrower and local: it prevents cleanup from deleting a non-durable fragment that may still complete commit.

The functional analogy is only:

> transition-source/candidate state may need temporary protection until a replacement or authority transition finishes.

It does **not** establish shared code, shared protocol, direct genealogy, or identical consistency semantics.

### A2 — Case 28 tombstone reclamation

Case 28 shows that negative state may need to survive a distributed consistency window before reclamation. Case 25's `commit_window` is not that tombstone window: it protects fresh non-durable positive state during a short write/cleanup race. Shared vocabulary such as `reclaim` and `window` must not collapse the two mechanisms.

---

## Philosophical interpretation (`I`) — deliberately narrow

The bounded technical result supports one modest conceptual observation:

> a retained embodiment can be **not yet authoritative** and still be something the system must temporarily preserve because it is part of the process by which a future authoritative state may be established.

This is not evidence that every unfinished state is valuable, nor that `becoming durable` is a general metaphysics of memory. The historical claim remains the Swift race and its cleanup guard; the philosophical layer adds only a vocabulary for distinguishing present authority from future-transition necessity.

---

## Counterexamples and stop conditions (`X`)

- **`commit_window` != `.durable`.** The former delays cleanup; the latter participates in the EC version's durability/currentness relation.
- **Default 60 seconds != universal safe bound.** The inspected sources publish a default and recommendation, not a proof that every deployment, filesystem, load condition, or PUT finishes within 60 seconds.
- **Recent `mtime` != current object version.** File recency does not establish timestamp currentness, quorum, or client success.
- **Old `X-Timestamp` != stale garbage.** The cited agents can intentionally make back-dated writes.
- **Reclaimable by timestamp != physically erased.** Cleanup unlinks object-server files; no lower-layer secure sanitization claim follows.
- **Bug fix != incidence estimate.** The commits establish a failure mode and fix, not how often production clusters encountered it.
- **Development option != released interface.** `nondurable_purge_delay` is explicitly documented as never having appeared in a tagged release.
- **2021 fix != proof that the 2015 design was conceptually wrong.** It demonstrates a later implementation/concurrency seam in cleanup and commit handling, not a refutation of the earlier multi-phase design.
- **One Swift race != universal mutable-EC law.** Other coded stores may use different versioning, commit, cleanup, and handoff mechanisms.

---

## Claim ledger

| Claim | Source | Layer | Strength |
| --- | --- | --- | --- |
| back-dated PUTs can produce fresh files whose logical timestamps are older than reclaim age | P2/P4 | H/P | direct |
| prior cleanup could delete such a non-durable file before commit and lose it | P2 | H/P | direct |
| handoff reversion could race a concurrent PUT that was about to mark a fragment durable | P1/P3 | H/P | direct |
| `commit_window` defaults to 60 seconds in the released 2.28.0 behavior | P2/P4 | H/P | direct |
| released `commit_window` uses local `mtime` recency to veto cleanup of otherwise reclaimable non-durable data | P2/P3 | H/P | direct |
| separate `nondurable_purge_delay` never reached a tagged release | P3 | H/P | direct |
| logical timestamp age and local physical-write age are distinct retention coordinates | P2 | E | strong reconstruction |
| non-durable status alone is insufficient deletion authority during an in-flight commit | P1/P2 | E | strong reconstruction |
| protection by `commit_window` does not itself make a fragment durable/admissible | P2 + Case-25 earlier commit semantics | E | strong reconstruction |
| transition safety can require retaining a candidate that is not yet authoritative | P1/P2 | E/I | bounded synthesis |

---

## Related-repository check

A current GitHub search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `commit_window`, `nondurable_purge_delay`, `OpenStack Swift`, and `erasure coding` returned no dedicated treatment to reuse.

Routing remains:

- broad OpenStack Swift implementation history, reconciler/container-sync genealogy, filesystem cleanup mechanics, or general EC protocol history -> `computing-archaeology` if developed;
- this bounded relation among **logical timestamp age, local write age, in-flight durability transition, and cleanup authority** -> `technical-retention`.

---

## Sources

1. OpenStack Swift commit `2934818d608e6cedd30ecb81900d02969476275c`, 24 June 2021, `reconstructor: Delay purging reverted non-durable datafiles`: <https://github.com/openstack/swift/commit/2934818d608e6cedd30ecb81900d02969476275c>
2. OpenStack Swift commit `bbaed18e9b681ce9cf26ffa6a5d5292f5cb219b7`, 19 July 2021, `diskfile: don't remove recently written non-durables`, closes Bug #1936508: <https://github.com/openstack/swift/commit/bbaed18e9b681ce9cf26ffa6a5d5292f5cb219b7>
3. OpenStack Swift commit `2696a79f098b02988136b13caf1c2565ec09481f`, 19 July 2021, `reconstructor: retire nondurable_purge_delay option`: <https://github.com/openstack/swift/commit/2696a79f098b02988136b13caf1c2565ec09481f>
4. OpenStack Swift 2.28.0 tag, 27 July 2021: <https://github.com/openstack/swift/tree/2.28.0>
5. OpenStack Swift 2.28.0 `CHANGELOG`, `Erasure coding fixes`: <https://github.com/openstack/swift/blob/2.28.0/CHANGELOG>
6. OpenStack Swift 2.28.0 `etc/object-server.conf-sample`, `commit_window`: <https://github.com/openstack/swift/blob/2.28.0/etc/object-server.conf-sample>
