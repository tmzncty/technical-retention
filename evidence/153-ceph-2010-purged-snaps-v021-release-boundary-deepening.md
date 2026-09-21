# Case 153 deepening — Ceph 2010 `purged_snaps` source-to-release boundary

**Status:** `bounded deepening complete`  
**Canonical:** [`../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md`](../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md)  
**Scope:** Ceph v0.20/v0.20.x/v0.21 public source and release provenance around the May-2010 `purged_snaps` transition.  
**Question:** after the 15-May-2010 source change replaced persistent `PG::Info::snap_trimq` with retained `purged_snaps` plus activation-time reconstruction of runtime `snap_trimq`, what is the first numbered Ceph release whose inspected source actually contains that retention relation?

## Bounded conclusion

The answer is **Ceph v0.21**, released **29 July 2010**.

The chronology is not inferable from wall-clock release dates alone:

```text
v0.20                         30 Apr 2010
    persistent PG::Info::snap_trimq

ceph-v0.20.1 source point     14 May 2010
    persistent PG::Info::snap_trimq

15 May 2010 PDT
(d006ae93; 16 May UTC)
    source-tree transition:
    PG::Info::snap_trimq
        -> PG::Info::purged_snaps
        + runtime PG::snap_trimq
        + activation-time reconstruction

v0.20.1 public release        17 May 2010
    inspected v0.20.1 source still has PG::Info::snap_trimq

v0.20.2 public release        27 May 2010
    inspected v0.20.2 source still has PG::Info::snap_trimq

v0.21                         29 Jul 2010
    inspected tagged source has PG::Info::purged_snaps
    and reconstructs runtime snap_trimq at PG activation
```

The retention-specific result is therefore:

```text
source change exists on one development line
    !=
a later-dated maintenance release necessarily contains it
```

and, more specifically:

```text
May-2010 source introduction
    !=
v0.20.x release-line inclusion

first inspected numbered release carrying the new relation
    = v0.21
```

This closes the previous Case-153 debt to map the May-2010 `purged_snaps` / reconstructed-queue transition onto an exact first numbered release boundary.

It does **not** close the separate question of the first runtime point at which early snap trimming can be demonstrated functionally correct, nor does it independently hash/inspect the historical v0.21 tarball bytes.

---

## Claim-type discipline

### Historical record

Primary Ceph source commits, exact Git tags, tagged source files, in-tree version metadata, and the project's contemporaneous release announcement establish the source/release chronology.

### Engineering reconstruction

Terms such as `retained completion frontier`, `reconstructed maintenance obligation`, `release-line inclusion`, and `source-to-release boundary` are project vocabulary used to describe relations visible in the source. They are not silently attributed to Ceph developers.

### Functional analogy

The only cross-case analogy permitted here is the generic one that a maintenance release can preserve an older state model while a development line has already moved to a newer one. This is not a claim of shared implementation or release engineering with another system.

### Philosophical interpretation

The bounded interpretive point is that persistence of a maintenance obligation can depend on retaining a relation from which work is regenerated, rather than preserving the exact worker queue. No broader claim about technological memory follows from the release chronology alone.

---

# Primary source ladder

| Source | Date | Evidence class | Use here |
| --- | --- | --- | --- |
| Ceph v0.20 annotated tag | 2010-04-30 | `H/P` | numbered release before the `purged_snaps` source change |
| Ceph `ceph-v0.20.1` inner annotated tag -> commit `14528d58...` | 2010-05-14 | `H/P` | source point for the v0.20.1 maintenance line; predates `d006ae93` |
| Ceph commit `d006ae9331216d413b5b0ef44b7b69ab8580d669`, `osd: purged_snaps in PG::Info, queue snap trim on primary` | 2010-05-15 PDT / 2010-05-16 UTC | `H/P` | introduces encoded `purged_snaps`, runtime `snap_trimq`, activation reconstruction, and PG-info v22 |
| Ceph `v0.20.1` tagged source `src/osd/PG.h` | public release line May 2010 | `H/P` | still encodes PG-info v21 `snap_trimq` |
| Ceph `v0.20.2` annotated tag / tagged source | 2010-05-27 | `H/P` | later-dated maintenance release still encodes PG-info v21 `snap_trimq` |
| Ceph official `v0.20.2 released` announcement | 2010-05-27 | `H/P` | confirms public v0.20.2 release/download event |
| Ceph v0.21 annotated tag -> commit `090436f5...` | 2010-07-29 | `H/P` | numbered release tag containing the new state model |
| Ceph v0.21 `src/osd/PG.h` | v0.21 | `H/P` | tagged source encodes PG-info v22 `purged_snaps` |
| Ceph v0.21 `src/osd/PG.cc` | v0.21 | `H/P` | tagged source reconstructs runtime `snap_trimq = cached_removed_snaps - purged_snaps` at activation |
| Ceph v0.21 `configure.ac` | v0.21 | `H/P` | in-tree source version metadata says `0.21` |
| Ceph v0.21 `debian/changelog` | 2010-07-27 entry | `H/P` | package metadata records `ceph (0.21-1)` |
| Ceph official `v0.21 released` announcement | 2010-07-29 | `H/P` | contemporaneous public release announcement with direct tarball link |

Primary URLs:

- <https://github.com/ceph/ceph/commit/d006ae9331216d413b5b0ef44b7b69ab8580d669>
- <https://github.com/ceph/ceph/blob/v0.20.1/src/osd/PG.h>
- <https://github.com/ceph/ceph/blob/v0.20.2/src/osd/PG.h>
- <https://github.com/ceph/ceph/blob/v0.20.2/src/osd/PG.cc>
- <https://github.com/ceph/ceph/blob/v0.21/src/osd/PG.h>
- <https://github.com/ceph/ceph/blob/v0.21/src/osd/PG.cc>
- <https://github.com/ceph/ceph/blob/v0.21/configure.ac>
- <https://github.com/ceph/ceph/blob/v0.21/debian/changelog>
- <https://www.ceph.com/en/news/blog/2010/v0-20-2-released/>
- <https://ceph.com/en/news/blog/2010/v0-21-released/>

---

# Historical record

## H/P — v0.20 precedes the state-model transition

Ceph's v0.20 release announcement is dated 30 April 2010. The later `d006ae93` change is therefore not part of the v0.20 source point simply by chronology.

This observation alone is weak: release-date ordering does not establish branch ancestry for later point releases. The important evidence comes from direct inspection of v0.20.1 and v0.20.2 tagged source.

---

## H/P — the v0.20.1 maintenance source still retains the old queue directly

The public `v0.20.1` ref resolves through an annotated-tag chain. The inner `ceph-v0.20.1` tag is dated 14 May 2010 and points to commit `14528d58f36ddcccbb01dca8dfe460598fbd6606`.

Direct inspection of `src/osd/PG.h` at `v0.20.1` shows:

```cpp
set<snapid_t> snap_trimq; // snaps we need to trim
```

inside `PG::Info`.

The same tagged source encodes:

```cpp
__u8 v = 21;
...
::encode(snap_trimq, bl);
```

and decodes the same field directly.

Therefore the v0.20.1 source state is still:

```text
persistent PG info
    contains exact snap_trimq
```

not the later:

```text
persistent PG info
    contains purged_snaps

runtime PG state
    reconstructs snap_trimq
```

The fact that a public v0.20.1 release announcement occurred after the `d006ae93` development commit does not change what the tagged maintenance source contains.

---

## H/P — `d006ae93` changes the persistence model on 15 May PDT / 16 May UTC

Commit `d006ae9331216d413b5b0ef44b7b69ab8580d669` is titled:

```text
osd: purged_snaps in PG::Info, queue snap trim on primary
```

Its commit timestamp is `2010-05-16T03:55:44Z`, corresponding to the evening of 15 May in the committer's `-0700` timezone used by the historical Git record.

The diff changes `PG::Info` from:

```cpp
set<snapid_t> snap_trimq;
```

to:

```cpp
interval_set<snapid_t> purged_snaps;
```

and bumps the encoded PG-info version:

```text
21 -> 22
```

The runtime PG object gains a separate:

```cpp
interval_set<snapid_t> snap_trimq;
```

while `PG::activate()` computes:

```cpp
snap_trimq = pool->cached_removed_snaps;
snap_trimq.subtract(info.purged_snaps);
```

This is the source transition already established in the earlier Case-153 genealogy evidence.

The new question here is not what the source change means, but when that state model first appears in an inspected numbered release.

---

## H/P — v0.20.2 is later in wall-clock time but still carries the old PG-info representation

Ceph's official v0.20.2 release announcement is dated **27 May 2010**, twelve days after the local-date `d006ae93` development change.

If one used only date ordering, it would be tempting to assume:

```text
15 May change
    ->
27 May release
    ->
release must include change
```

Direct tagged-source inspection disproves that inference.

At `v0.20.2`, `src/osd/PG.h` still contains:

```cpp
set<snapid_t> snap_trimq;
```

inside `PG::Info`, still encodes version `21`, and still serializes `snap_trimq` directly.

At `v0.20.2`, `PG::activate()` still checks:

```cpp
if (!info.snap_trimq.empty())
  queue_snap_trim();
```

rather than reconstructing runtime work from `cached_removed_snaps - purged_snaps`.

The v0.20.2 tagged source identifies itself in `configure.ac` as:

```text
AM_INIT_AUTOMAKE(ceph, 0.20.2)
```

Therefore:

```text
later release date
    !=
development-line commit included
```

This is direct source evidence of a branch/release-line boundary, not merely a reconstructed guess about stable-versus-development workflow.

---

## H/P — v0.21 is the first inspected numbered release with `purged_snaps`

The Ceph v0.21 annotated tag is dated **29 July 2010** and points to commit `090436f56ac293b309bf18ccffb7e9bafeb2ffad`.

Direct inspection of `src/osd/PG.h` at `v0.21` shows:

```cpp
interval_set<snapid_t> purged_snaps;
```

inside `PG::Info`.

The tagged source also encodes:

```cpp
__u8 v = 22;
...
::encode(purged_snaps, bl);
```

and keeps compatibility handling for older input:

```cpp
if (v >= 22)
  ::decode(purged_snaps, bl);
else {
  set<snapid_t> snap_trimq;
  ::decode(snap_trimq, bl);
}
```

More importantly, `src/osd/PG.cc` in the same v0.21 tagged tree contains the activation-time reconstruction:

```cpp
snap_trimq = pool->cached_removed_snaps;
snap_trimq.subtract(info.purged_snaps);
if (!snap_trimq.empty())
  queue_snap_trim();
```

This establishes that v0.21 contains the complete retention-specific relation of interest:

```text
retained removed-snapshot relation
    - retained purged/completed relation
    -> reconstructed runtime trim obligation
```

It is not merely a tag whose name postdates the commit; the tagged source itself contains the changed schema and reconstruction code.

---

## H/P — v0.21 is also a contemporaneously announced public release

The Ceph project published `v0.21 released` on 29 July 2010. The announcement states that v0.21 is ready, lists changes since v0.20, and provides a direct `ceph-0.21.tar.gz` download URL.

The v0.21 tree's own version-bearing artifacts agree:

```text
configure.ac
    AM_INIT_AUTOMAKE(ceph, 0.21)

debian/changelog
    ceph (0.21-1) unstable
```

This is stronger than a bare source-commit chronology: a numbered source state containing the new relation was publicly announced as v0.21.

However, this slice has **not** independently downloaded and hash-compared the historical tarball against the Git tag. Therefore the safe wording is:

> v0.21 is the first inspected numbered Ceph release/tag whose source contains the `purged_snaps` + reconstructed-`snap_trimq` relation, and Ceph contemporaneously announced v0.21 with a source tarball download.

Do not silently strengthen that to a bit-for-bit tarball identity claim without inspecting the archive itself.

---

# Engineering reconstruction

## E — a maintenance release can preserve an older persistence schema after development has moved on

The key engineering-history lesson is not specific to Ceph snapshots:

```text
development source chronology
    !=
maintenance-release inclusion chronology
```

Case 153 provides a concrete witness:

```text
15 May development change exists
    ↓
17 May v0.20.1 release line: old PG-info queue model
    ↓
27 May v0.20.2 release line: old PG-info queue model
    ↓
29 Jul v0.21 release: new purged/completion relation + reconstructed queue
```

A later wall-clock release can intentionally remain on an older maintenance branch.

For retention research, this matters because a statement such as:

> "Ceph changed from retained exact trim queue to retained completion evidence in May 2010"

is a **source-tree chronology** claim.

A statement such as:

> "Ceph v0.21 exposes that model in the inspected numbered release source"

is a **release-boundary** claim.

They are related but not interchangeable.

---

## E — release identity and retained-state semantics must be joined through inspected source, not date proximity

The robust chain is:

```text
named release/tag
    -> inspected source tree
    -> exact serialized field
    -> exact reconstruction logic
    -> bounded retention claim
```

not:

```text
commit date < release date
    -> assume inclusion
```

This distinction prevents a common form of accidental genealogy inflation.

---

## E — v0.21 retains completion evidence, not the exact pre-interruption worker embodiment

The tagged v0.21 source preserves the same retention relation seen in the May development commit:

```text
PG::Info::purged_snaps       retained/encoded relation
PG::snap_trimq               runtime work state
PG::activate()               reconstruction step
```

Therefore release inclusion does not change the earlier bounded conclusion:

```text
cleanup obligation can survive/reconstruct
    !=
exact worker queue survives byte-for-byte
```

The v0.21 release mapping strengthens provenance. It does not change the mechanism into a durable worker-queue checkpoint.

---

# Controlled functional comparison

## FA — source inclusion and service availability are different boundaries

A numbered release can be used as a provenance boundary for source semantics without being treated as proof of every runtime property.

For Case 153:

```text
source commit exists
    !=
numbered release contains it
    !=
release announcement exists
    !=
mechanism demonstrated correct under faults
    !=
deployed installations all run that version
```

This is a functional comparison rule for release archaeology. It is not a Ceph-specific historical vocabulary.

---

## FA — do not conflate branch divergence with contradictory historical evidence

The apparent chronology:

```text
May 15: new state model committed
May 27: v0.20.2 released with old state model
```

is not contradictory once the evidence is partitioned by release line.

The sources are describing different source histories:

```text
development line
    vs
v0.20 maintenance line
```

This is a useful guardrail when comparing vendor firmware, kernels, distributed systems, or standards branches elsewhere in the repository, but no common implementation lineage is implied.

---

# Philosophical interpretation

The narrow interpretive point remains downstream of the mechanism:

> What persists is not necessarily the execution episode itself. A system can retain a relation sufficient to regenerate unfinished work later.

The v0.21 boundary adds another layer:

> The public identity of a version is itself an access path to a historically specific retention contract; version chronology only becomes meaningful after the source state attached to that version is inspected.

This should not be inflated into a general theory of archival identity. Here it means only that release labels, commit dates, and runtime semantics are distinct evidentiary objects.

---

# Explicit non-claims

This slice does **not** claim that:

1. Ceph invented asynchronous snapshot reclamation;
2. `d006ae93` is the first conceptual invention of `purged_snaps`;
3. the May-2010 change is the first working snap-trimmer implementation;
4. v0.20.1 or v0.20.2 had no snapshot trimming;
5. v0.20.1 or v0.20.2 are chronologically earlier than the May-2010 development commit in every metadata sense;
6. a release dated after a commit must contain that commit;
7. the v0.20 maintenance line and the development line were identical;
8. v0.21 preserves the exact worker queue across restart;
9. `purged_snaps` by itself is the whole cleanup obligation;
10. `purged_snaps` proves lower-layer bytes were physically erased;
11. `purged_snaps` means secure sanitization;
12. PG-info v22 proves crash consistency of every associated update;
13. compatibility decode of old v21 data proves a complete migration protocol;
14. v0.21's presence of the code proves every fault path was correct;
15. v0.21's release announcement proves widespread deployment;
16. the historical tarball has been independently hash-compared with the Git tag in this slice;
17. Debian package publication timing is identical to Git tag timing;
18. the v0.21 changelog entry specifically documents `purged_snaps`;
19. branch/release engineering in Ceph is directly genealogical with another project's maintenance branches;
20. first inspected numbered release means first private build, first test deployment, or first user installation.

---

# Why this changes the case

Before this slice, Case 153 already knew the source-level transition:

```text
15 May 2010
persistent exact trim queue
    -> retained purged/completion relation
       + reconstructed runtime queue
```

but the evidence index still carried an explicit debt:

> map the May-2010 `purged_snaps` / reconstructed-queue state change to its exact first numbered tag/release boundary.

That debt is now closed at the level of inspected public tags/releases:

```text
v0.20.1   old PG::Info::snap_trimq
v0.20.2   old PG::Info::snap_trimq
v0.21     PG::Info::purged_snaps + reconstructed PG::snap_trimq
```

The important negative result is just as useful as the positive one:

> **v0.20.2 was released after the May source change but does not carry the new retention representation.**

That prevents future researchers from assigning the new model to v0.20.2 merely by comparing dates.

---

# Remaining debt

This slice closes only the numbered release-boundary question for the May-2010 state-model transition.

Still open:

- establish the first source/runtime point at which the early 2008 trimmer can be demonstrated functional rather than merely present/fixed/tagged;
- inspect the complete PG-info v21 -> v22 upgrade/migration behavior beyond the local decoder fragment;
- finish the June-2011 state-machine series around replica application acknowledgement and completion publication;
- fault-inject interruption around clone removal, replicated application, PG-info update, and collection removal;
- if bit-for-bit distribution provenance becomes necessary, retrieve and hash/inspect the historical `ceph-0.21.tar.gz` archive against the tag;
- trace lower-layer allocator reuse separately from RADOS logical reclamation;
- keep sanitization and forensic remanence as separate evidence questions.

---

# Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `purged_snaps`, `snap_trimmer`, and the Ceph snapshot-trim transition found no dedicated packet to reuse.

Keep here:

- release-boundary provenance when it changes the date/version attached to the retention relation;
- exact `PG::Info` representation boundary;
- reconstruction of runtime maintenance obligation from retained relations;
- explicit source/tag/release non-equivalence guardrails.

Route primarily to `computing-archaeology` if pursued:

- full Ceph stable/development branch-management history;
- all v0.20.x packaging mechanics;
- broad snapshot implementation history;
- complete release engineering / distribution infrastructure archaeology;
- deployment/adoption chronology not needed for the retention claim.
