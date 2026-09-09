from pathlib import Path
import re

ROOT = Path('.')


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def write(path, text):
    text = text.rstrip() + '\n'
    (ROOT / path).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / path).write_text(text, encoding='utf-8')

new_evidence_path = 'evidence/25-swift-2021-commit-window-nondurable-cleanup-deepening.md'
new_evidence = r'''# Case 25 deepening — Swift 2.28.0 `commit_window`, in-flight non-durable fragments, and cleanup authority (2021)

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

## Direct historical record (`H/P`)

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
'''

new_path = ROOT / new_evidence_path
if new_path.exists():
    raise SystemExit(f'{new_evidence_path} already exists; refusing duplicate slice')
write(new_evidence_path, new_evidence)

# --- Case 25 ---
case_path = 'cases/25-openstack-swift-ec-overwrite-durable-currentness.md'
case = read(case_path)
old_scope = '- **Bounded system:** OpenStack Swift erasure-coded object storage as released in Swift 2.3.0 (Kilo, 30 April 2015) and sharpened by Swift 2.10.1 (December 2016).'
new_scope = old_scope + ' A later bounded deepening uses Swift 2.28.0 (27 July 2021) only for the `commit_window` / concurrent non-durable-cleanup race.'
if old_scope not in case:
    raise SystemExit('Case 25 scope anchor missing')
case = case.replace(old_scope, new_scope, 1)
old_source_base = '- **Primary source base:** the OpenStack Swift source tree and release documentation at the signed `2.3.0` tag and `2.10.1` tag/release state.'
new_source_base = old_source_base + ' The 2021 deepening additionally inspects commits `2934818d`, `bbaed18e`, `2696a79f`, and the signed/tagged 2.28.0 release state.'
if old_source_base not in case:
    raise SystemExit('Case 25 source-base anchor missing')
case = case.replace(old_source_base, new_source_base, 1)

insert_anchor = '\n---\n\n## Retained state\n'
if case.count(insert_anchor) != 1:
    raise SystemExit('Case 25 retained-state insertion anchor not unique')
case_deepening = r'''

### H/P — Swift 2.28.0 adds a grace window against deleting in-flight non-durable fragments

A later, separately bounded implementation witness sharpens the earlier `fragment presence != committed object retention` result. OpenStack Swift commit `bbaed18e9b681ce9cf26ffa6a5d5292f5cb219b7` (19 July 2021; released in 2.28.0 on 27 July) records Bug `#1936508`: an agent such as the reconciler or container-sync can intentionally PUT an object using an older `X-Timestamp`, so a newly written non-durable EC `.data` file may already be older than `reclaim_age` in **logical object time**. If another process calls `cleanup_ondisk_files()` before the object server finishes the commit/rename, the old cleanup rule can remove the file and the later commit fails because its source data file is gone.

The fix adds `commit_window`, default 60 seconds. For otherwise reclaimable non-durable data, cleanup now also checks local filesystem `mtime` and protects files written within that short window. The 2.28.0 changelog explicitly says this improves durability for both back-dated PUTs and fresh writes to handoffs by preventing the reconstructor from deleting data the object server is still writing.

A preceding 24 June development commit (`2934818d`) had introduced a separate `nondurable_purge_delay` for the handoff-reversion race. Commit `2696a79f` (19 July) explicitly says that option never appeared in a tagged release, removes it, and reuses `commit_window` for the reconstructor path. The repository therefore treats `nondurable_purge_delay` as development-history vocabulary only and `commit_window` as the released operator-facing relation.

**Primary anchors:** OpenStack Swift commits `2934818d608e6cedd30ecb81900d02969476275c`, `bbaed18e9b681ce9cf26ffa6a5d5292f5cb219b7`, `2696a79f098b02988136b13caf1c2565ec09481f`; Swift 2.28.0 `CHANGELOG` and object-server sample configuration. See the [2021 commit-window evidence deepening](../evidence/25-swift-2021-commit-window-nondurable-cleanup-deepening.md).

### E — old logical timestamp != old physical file incarnation

The 2021 fix exposes two clocks with different roles. The Swift object timestamp participates in object-version/currentness and stale/reclaim reasoning; filesystem `mtime` can say that the physical file carrying that old logical timestamp was created only moments ago and may still be part of an unfinished commit.

Thus:

```text
reclaimable by logical timestamp
    !=
safe to delete during an in-flight write
```

and:

```text
non-durable
    !=
discardable-now
```

The second relation is intentionally narrower than saying every non-durable fragment deserves preservation. A failed pre-commit fragment may still become cleanup debris; `commit_window` merely prevents a freshness-blind cleanup path from deciding that **too early**.

### E/X — `commit_window` protection != durability/currentness authority

A recent `mtime` does not prove that the object version reached quorum, that a `.durable`/durable-filename relation exists, or that the client PUT succeeded. The grace window protects a candidate **while it may become durable**; it is not itself the durability witness.

This extends Case 25's currentness ladder with a transition-safety boundary:

```text
physical candidate exists
    -> temporarily protected from cleanup while in-flight
    -> commit/durability qualification (if it succeeds)
```

The arrow is conditional. `commit_window` expiration is not a proof that the PUT failed, and the published 60-second default is not treated as a universal upper bound on every write path.
'''
case = case.replace(insert_anchor, case_deepening + insert_anchor, 1)

# Add later sources without renumbering the already-cited prior-art items ambiguously.
src_anchor = '\n### Reused prior-art boundary\n'
if case.count(src_anchor) != 1:
    raise SystemExit('Case 25 source-list insertion anchor not unique')
later_sources = r'''

6. OpenStack Swift commit `2934818d608e6cedd30ecb81900d02969476275c`, 24 June 2021, `reconstructor: Delay purging reverted non-durable datafiles`: <https://github.com/openstack/swift/commit/2934818d608e6cedd30ecb81900d02969476275c>
7. OpenStack Swift commit `bbaed18e9b681ce9cf26ffa6a5d5292f5cb219b7`, 19 July 2021, `diskfile: don't remove recently written non-durables`: <https://github.com/openstack/swift/commit/bbaed18e9b681ce9cf26ffa6a5d5292f5cb219b7>
8. OpenStack Swift commit `2696a79f098b02988136b13caf1c2565ec09481f`, 19 July 2021, `reconstructor: retire nondurable_purge_delay option`: <https://github.com/openstack/swift/commit/2696a79f098b02988136b13caf1c2565ec09481f>
9. OpenStack Swift **2.28.0**, tag date 27 July 2021, `CHANGELOG` `Erasure coding fixes`: <https://github.com/openstack/swift/blob/2.28.0/CHANGELOG>
'''
case = case.replace(src_anchor, later_sources + src_anchor, 1)
# Existing prior-art items are numbered 6/7; renumber only those two exact list prefixes after heading.
case = case.replace('### Reused prior-art boundary\n\n6. [`Case 19`', '### Reused prior-art boundary\n\n10. [`Case 19`', 1)
case = case.replace('\n7. [`Case 24`', '\n11. [`Case 24`', 1)
write(case_path, case)

# --- Original Case-25 grounding record: preserve its 2015–2016 scope, link later evidence only. ---
base_ev_path = 'evidence/25-openstack-swift-2015-2016-ec-currentness-grounding.md'
base_ev = read(base_ev_path)
if '25-swift-2021-commit-window-nondurable-cleanup-deepening.md' not in base_ev:
    base_ev += r'''

---

## Later bounded deepening (kept separate from the 2015–2016 grounding)

The original grounding above remains scoped to Swift 2.3.0–2.10.1. A separate [2021 `commit_window` / non-durable-cleanup addendum](25-swift-2021-commit-window-nondurable-cleanup-deepening.md) examines Swift 2.28.0's fix for a race in which background cleanup could delete a freshly written, intentionally back-dated EC fragment before the object server finished making it durable.

That later record adds `logical object timestamp age != local file-write age`, `non-durable != discardable-now`, and `cleanup protection != durability witness` without back-projecting the 2021 implementation into the earlier release design.
'''
write(base_ev_path, base_ev)

# --- Synthesis 10 ---
syn_path = 'docs/SYNTHESIS_10_MUTABLE_EC_CURRENTNESS_RETIREMENT_REPAIR.md'
syn = read(syn_path)
anchor = '- OpenStack Swift **2.11.0** changelog, used here only as a later implementation-continuity witness: <https://github.com/openstack/swift/blob/2.11.0/CHANGELOG>.'
if anchor not in syn:
    raise SystemExit('Synthesis 10 source anchor missing')
extra_anchor = anchor + '\n- OpenStack Swift **2.28.0** changelog plus 2021 commits `2934818d`, `bbaed18e`, and `2696a79f`, used only for the later in-flight non-durable-cleanup / `commit_window` boundary: <https://github.com/openstack/swift/blob/2.28.0/CHANGELOG>.'
syn = syn.replace(anchor, extra_anchor, 1)

eng_anchor = '\n---\n\n## Engineering reconstruction: ten typed relations\n'
if syn.count(eng_anchor) != 1:
    raise SystemExit('Synthesis 10 engineering anchor not unique')
syn_deepening = r'''

### Swift 2.28.0 — cleanup authority must distinguish logical timestamp age from in-flight file age

The later Case-25 [2021 evidence deepening](../evidence/25-swift-2021-commit-window-nondurable-cleanup-deepening.md) adds a transition-race counterexample to an overly simple cleanup model. Bug `#1936508` records that reconciler/container-sync writes can intentionally carry an `X-Timestamp` already older than `reclaim_age` while the local EC `.data` file has only just been written and has not yet been committed. Background cleanup could therefore classify the fragment as stale by logical timestamp and delete it before the object server completed the durable rename.

Swift 2.28.0's released `commit_window` adds a short local-`mtime` grace (default 60 seconds) that temporarily protects otherwise reclaimable non-durable data. The key decomposition is:

```text
logical version age
    != local physical-file age

reclaim-eligible by long-term policy
    != safe to delete during an unfinished commit

protected from cleanup while in-flight
    != durable / currentness-qualified
```

This does not add an eleventh universal EC state. It sharpens Relations 6, 8, and 9 by showing that **cleanup itself has a transition-admissibility condition**: state that is not yet authoritative may nevertheless need temporary protection because it is a candidate through which the authority transition is still completing.

The 24 June development name `nondurable_purge_delay` is not treated as released terminology; the 19 July follow-up explicitly says it never appeared in a tagged release and consolidates the behavior under `commit_window` before 2.28.0.
'''
syn = syn.replace(eng_anchor, syn_deepening + eng_anchor, 1)
write(syn_path, syn)

# --- ROADMAP ---
roadmap_path = 'ROADMAP.md'
roadmap = read(roadmap_path)
lines = roadmap.splitlines()
prefix = '- [ ] cross-timestamp fragment mixing, missing durability witness, stale pre-commit fragments, or premature old-version retirement during mutable EC overwrite;'
idxs = [i for i, line in enumerate(lines) if line == prefix]
if len(idxs) != 1:
    raise SystemExit(f'ROADMAP target count {len(idxs)}')
lines[idxs[0]] = '- [ ] cross-timestamp fragment mixing, missing durability witness, stale pre-commit fragments, or premature old-version retirement during mutable EC overwrite — **partially advanced by the Case 25 Swift-2.28.0 `commit_window` deepening**: the 2021 Bug #1936508 fix shows that a freshly written non-durable EC fragment can carry an intentionally old logical `X-Timestamp`, be old enough for `reclaim_age`, and still be in the middle of a valid commit; cleanup that ignores local write recency can delete the fragment before it becomes durable. Swift 2.28.0 adds an `mtime`-based `commit_window` grace, grounding `logical timestamp age != local physical-write age`, `reclaim eligibility != immediate deletion authority`, and `non-durable != discardable-now`. Cross-timestamp selection failures, missing/corrupt durability witnesses, premature retirement of an older *committed* version, commit-window sizing/failure beyond the grace, other mutable EC protocols, and independent fault injection remain open;'
roadmap = '\n'.join(lines)
write(roadmap_path, roadmap)

# --- CASE_INDEX row + findings ---
index_path = 'CASE_INDEX.md'
index = read(index_path)
lines = index.splitlines()
row_prefix = '| [OpenStack Swift EC Overwrites: Timestamp Cohorts, `.durable` Markers, and Mutable Coded Currentness]'
idxs = [i for i, line in enumerate(lines) if line.startswith(row_prefix)]
if len(idxs) != 1:
    raise SystemExit(f'CASE_INDEX Case25 row count {len(idxs)}')
lines[idxs[0]] = '| [OpenStack Swift EC Overwrites: Timestamp Cohorts, `.durable` Markers, and Mutable Coded Currentness](cases/25-openstack-swift-ec-overwrite-durable-currentness.md) | **grounded** | mutable object versions + timestamped indexed EC archives + set-level durability marker + ring/handoff placement + reconstructor repair + in-flight non-durable cleanup grace | separate fragment presence, version coherence, coded reconstructability, commit/admissibility, safe old-version retirement, later repair convergence, and cleanup authority during unfinished commit | [2015–2016 Swift EC grounding](evidence/25-openstack-swift-2015-2016-ec-currentness-grounding.md) + [2021 Swift 2.28.0 `commit_window` deepening](evidence/25-swift-2021-commit-window-nondurable-cleanup-deepening.md); later tombstone/versioning semantics, `#d` durability representation beyond the bounded continuity witness, cross-region EC, commit-window fault/latency validation, and other mutable coded protocols remain separate work |'
index = '\n'.join(lines).rstrip()
if re.search(r'^- \*\*2531\b', index, re.M):
    raise SystemExit('finding 2531 already exists')
findings = r'''

## Case 25 — Swift 2.28.0 `commit_window` / in-flight non-durable cleanup findings

Evidence: [`evidence/25-swift-2021-commit-window-nondurable-cleanup-deepening.md`](evidence/25-swift-2021-commit-window-nondurable-cleanup-deepening.md)

- **2531 — Swift 2.28.0 releases the `commit_window` EC cleanup guard on 27 July 2021.** The tagged changelog explicitly places it under erasure-coding fixes and ties it to back-dated PUTs and fresh handoff writes; this is a release-history anchor, not an invention-priority claim. (`H/P`)
- **2532 — old logical `X-Timestamp` != old local file incarnation.** Bug #1936508 names reconciler/container-sync writes that intentionally carry older object timestamps even though the non-durable `.data` file has only just been written. (`H/P`, `E`)
- **2533 — non-durable != discardable-now.** P1/P2 describe non-durable fragments that the object server is still expected to make durable; lack of durable status alone cannot authorize immediate cleanup during the transition. (`H/P`, `E`)
- **2534 — `reclaim_age` eligibility != immediate deletion authority.** A fragment may be old enough by object timestamp for normal stale-state reclamation yet temporarily unsafe to delete because its physical write/commit transition is still active. (`H/P`, `E`)
- **2535 — background cleanup can destroy future commit state without first corrupting the fragment bytes.** The 2021 fix record says cleanup could unlink the newly written file before commit rename, after which the commit path fails because the data file is gone. (`H/P`)
- **2536 — released `commit_window` adds local-`mtime` evidence to the cleanup decision.** Swift protects otherwise reclaimable non-durable files whose filesystem modification time is inside the configured grace; the default is 60 seconds. (`H/P`)
- **2537 — `commit_window` protection != durability witness.** Surviving the grace only keeps a candidate available for a possible commit; it does not establish quorum, client success, or the timestamp-level durable/currentness relation. (`E`, `X`)
- **2538 — recent filesystem `mtime` != current object version.** Local physical recency can veto cleanup without proving that the logical timestamp is newest, admissible, or reconstructable. (`E`, `X`)
- **2539 — the published 60-second default != universal maximum PUT/commit time.** The source exposes a configurable safety window and recommendation, not a theorem that every deployment completes the relevant transition inside 60 seconds. (`H/P`, `X`)
- **2540 — handoff reversion cleanup has its own concurrency seam.** The 24-June development change records the reconstructor reverting a non-durable handoff fragment while an object-server PUT is about to make it durable; immediate purge can race that transition. (`H/P`)
- **2541 — development vocabulary != released vocabulary.** `nondurable_purge_delay` was a real 24-June implementation name, but the 19-July follow-up explicitly says it was never present in a tagged release and consolidates the behavior under `commit_window`. (`H/P`, `X`)
- **2542 — reconstructor cleanup after reversion != reconstruction/repair itself.** Removing a handoff copy after transfer and protecting a concurrently written non-durable candidate concern cleanup/convergence authority, not Reed–Solomon decoding or proof of payload correction. (`E`)
- **2543 — protocol currentness safety includes transition/cleanup ordering, not only the final durable marker.** Case 25's earlier commit relation says what eventually qualifies a version; the 2021 race shows the implementation must also avoid destroying candidate state before that qualification can finish. (`E`)
- **2544 — temporary candidate protection is only functionally analogous to Case 24's representation-handoff source protection.** Both defer destructive retirement across an unfinished transition, but Swift's local non-durable cleanup race and Azure's sealed-extent redundancy conversion have different mechanisms, histories, and authority rules. (`A`, `X`)
- **2545 — related-repository boundary:** current `tmzncty/computing-archaeology` search found no dedicated `commit_window` / `nondurable_purge_delay` / Swift-EC cleanup case to reuse; broad Swift implementation and reconciler/container-sync history should live there if developed, while Case 25 keeps the retention-specific timestamp/write-age/cleanup-authority relation. (`H/P` project-state record)
'''
index += findings
write(index_path, index)

# Canonical sanity checks independent of git.
for p in [case_path, base_ev_path, new_evidence_path, syn_path, roadmap_path, index_path]:
    if not (ROOT / p).is_file():
        raise SystemExit(f'missing canonical file {p}')

index = read(index_path)
nums = [int(x) for x in re.findall(r'^- \*\*(\d+)\b', index, re.M)]
for n in range(2531, 2546):
    if nums.count(n) != 1:
        raise SystemExit(f'finding {n} count={nums.count(n)}')

# Guard against accidental project-label collapse in the new evidence.
new_text = read(new_evidence_path)
for required in ['Historical record (`H/P`)', 'Engineering reconstruction (`E`)', 'Functional analogies (`A`)', 'Philosophical interpretation (`I`)', 'Counterexamples and stop conditions (`X`)']:
    if required not in new_text:
        raise SystemExit(f'missing layer heading: {required}')

print('Case 25 Swift 2.28.0 commit-window deepening applied')
