# Case 153 deepening — Ceph 2008–2009 snap-trim tag / package provenance boundary

**Status:** `bounded deepening complete`  
**Canonical:** [`../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md`](../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md)  
**Parent evidence:** [`153-ceph-2008-08-snaptrimmer-introduction-boundary-deepening.md`](153-ceph-2008-08-snaptrimmer-introduction-boundary-deepening.md), [`153-ceph-2008-2011-snaptrim-obligation-completion-genealogy-deepening.md`](153-ceph-2008-2011-snaptrim-obligation-completion-genealogy-deepening.md)  
**Scope:** close the narrow Case-153 debt around the earliest numbered Git tags containing the 2008 snap-trimmer source states, while refusing to collapse tag inclusion, package metadata, demonstrated functionality, binary distribution, and deployment into one event.  
**Question:** which early Ceph numbered tags actually contain the August/September/October/November 2008 snap-trimmer changes, and what can those tag boundaries safely establish?

## Bounded conclusion

The inspected upstream Git ancestry establishes three useful numbered-tag boundaries:

1. **`v0.4`** points to commit `13b1bf7c492003ba2dfa2786ba9ae728a2bfe65f`, dated **7 October 2008**. Git ancestry shows that it contains:
   - the **18-August-2008** `e8e57d9a` introduction, whose title says `osd: rough trimmer, non-functional`;
   - the **10-September-2008** `bfb5b8d9` `some snap_trimmer fixes` change.
   `v0.3`, dated **11 July 2008**, predates the introduction. Therefore `v0.4` is the earliest inspected adjacent numbered tag containing the early snap-trimmer implementation.

2. **`v0.5`** points to commit `1dd420957f9ba0e3991512a4627748bf38592d53`, dated **14 November 2008**. Git ancestry shows that it contains the **17-October-2008** `57965a88` fast-path change and `a15fdb91` snapshot-collection tracking/cleanup change. It does **not** contain the later **20-November** `69eea16f` `snap_trim_wq` conversion, because that commit is a descendant of `v0.5`.

3. **`v0.6`** points to commit `a4c752df71356c152d68258a7338b455abce6dc8`, dated **20 January 2009**. Git ancestry shows that it contains both:
   - **20-November-2008** `69eea16f`, converting snap trimming to `snap_trim_wq`;
   - **24-November-2008** `4f8fb979`, removing a snapshot collection after it is trimmed.

The safe chronology is therefore:

```text
v0.3 (11 Jul 2008)
    -> predates located snap_trimmer introduction

18 Aug 2008
    -> rough/non-functional implementation introduced
10 Sep 2008
    -> named snap_trimmer fixes
v0.4 tag (7 Oct 2008)
    -> contains introduction + September fixes

17 Oct 2008
    -> further fast-path / snapshot-collection refinement
v0.5 tag (14 Nov 2008)
    -> contains October refinements

20 Nov 2008
    -> snap_trim_wq worker transition
24 Nov 2008
    -> remove snapshot collection after trim
v0.6 tag (20 Jan 2009)
    -> contains November worker / collection-cleanup state
```

This closes the **numbered-tag ancestry** half of the earlier release-provenance debt for the 2008 changes.

It does **not** establish the first tarball downloaded by users, first Debian package actually published in a repository, first binary deployment, first production use, or the first source point at which the snap trimmer is demonstrated end-to-end functional.

---

# Claim-type discipline

## Historical record

Historical claims here come from:

- exact Git tag refs and the commits to which they point;
- Git ancestry comparisons between the snap-trimmer commits and those tags;
- source files read directly at `v0.4`, `v0.5`, and `v0.6`;
- contemporaneous repository packaging metadata (`configure.ac`, `debian/changelog`).

The word `release` is deliberately avoided where only tag or in-tree package metadata has been established.

## Engineering reconstruction

Terms such as `tag inclusion boundary`, `source-state provenance`, `package-metadata boundary`, and `functionality proof` are project vocabulary for separating different evidence relations. They are not historical Ceph terminology.

## Functional analogy

A bounded analogy may be made to firmware or software compatibility cases elsewhere in this repository: a version label can identify a source state without proving every runtime property attributed to that version. This is only a provenance-function analogy, not a genealogy claim.

## Philosophical interpretation

A narrow downstream interpretation is permitted: retaining a historical version name is not enough if the relation between that name, source state, package state, and demonstrated behavior is lost. This is project interpretation, not a claim about how Ceph developers conceptualized versioning.

---

# Primary source ladder

| Source | Date / tag | Evidence class | Use here |
| --- | --- | --- | --- |
| Ceph tag `v0.3` -> `2e986fe9ddf1ceffc2056bf6d8ee7f49fbebeaf0` | 2008-07-11 | `H/P` | adjacent earlier numbered tag; predates `e8e57d9a` |
| Ceph commit `e8e57d9a1d546d2007a9f82ab54e901464956ad3`, `osd: rough trimmer, non-functional` | 2008-08-18 | `H/P` | public-tree introduction boundary |
| Ceph commit `bfb5b8d9bd66089978fe092182a113631ff315cf`, `osd: some snap_trimmer fixes` | 2008-09-10 | `H/P` | early correctness/refinement change |
| Ceph tag `v0.4` -> `13b1bf7c492003ba2dfa2786ba9ae728a2bfe65f` | 2008-10-07 | `H/P` | first inspected adjacent numbered tag containing introduction + September fixes |
| `configure.ac` at `v0.4` | `v0.4` | `H/P` | tree identifies Automake package version `0.4` |
| Ceph commit `54548de347b951da3fe7bca063a39f261cef2d33`, `debian: changelog update` | 2008-10-09 | `H/P` | adds `ceph (0.4-1)` / `Snapshots.` after the `v0.4` tag point |
| Ceph commits `57965a88...`, `a15fdb91...` | 2008-10-17 | `H/P` | further trimmer / snapshot-collection refinements |
| Ceph tag `v0.5` -> `1dd420957f9ba0e3991512a4627748bf38592d53` | 2008-11-14 | `H/P` | contains October refinements but predates the work-queue conversion |
| `debian/changelog` at `v0.5` | `v0.5` tree | `H/P` | contains `0.4-1` `Snapshots.` entry, not yet a `0.5-1` entry |
| Ceph commit `69eea16f39f2255962041de29d6393ecc37bb0cb`, `osd: convert snap trimming to snap_trim_wq` | 2008-11-20 | `H/P` | later worker-embodiment transition |
| Ceph commit `4f8fb979e833fd1dbda8cc46e598cb67f3e590f0`, `osd: remove snap collection after it is trimmed` | 2008-11-24 | `H/P` | explicit post-trim collection removal |
| Ceph tag / commit `v0.6` -> `a4c752df71356c152d68258a7338b455abce6dc8` | 2009-01-20 | `H/P` | first inspected numbered tag after the November worker/collection changes |
| `debian/changelog` change visible in `v0.6` commit | 2009-01-20 tree | `H/P` | adds historical package entries for `0.5-1` and `0.6-1`, while retaining `0.4-1` `Snapshots.` |
| `src/osd/OSD.h` at `v0.6` | `v0.6` | `H/P` | direct tagged-source witness for `SnapTrimWQ` / `snap_trim_wq` |

Primary URLs:

- <https://github.com/ceph/ceph/tree/v0.3>
- <https://github.com/ceph/ceph/commit/e8e57d9a1d546d2007a9f82ab54e901464956ad3>
- <https://github.com/ceph/ceph/commit/bfb5b8d9bd66089978fe092182a113631ff315cf>
- <https://github.com/ceph/ceph/tree/v0.4>
- <https://github.com/ceph/ceph/commit/54548de347b951da3fe7bca063a39f261cef2d33>
- <https://github.com/ceph/ceph/commit/57965a8849213ddff9260a1e86632687dae58e94>
- <https://github.com/ceph/ceph/commit/a15fdb916ad10e019145c2816221946a76f1228b>
- <https://github.com/ceph/ceph/tree/v0.5>
- <https://github.com/ceph/ceph/commit/69eea16f39f2255962041de29d6393ecc37bb0cb>
- <https://github.com/ceph/ceph/commit/4f8fb979e833fd1dbda8cc46e598cb67f3e590f0>
- <https://github.com/ceph/ceph/tree/v0.6>

---

# Historical record

## H/P — `v0.3` is before the located trimmer introduction

The exact `refs/tags/v0.3` ref points to commit `2e986fe9...`, dated 11 July 2008.

Git ancestry from `v0.3` to the 18-August `e8e57d9a` commit is linear in the inspected comparison: `v0.3` is the merge base and the introduction commit is later.

Therefore the adjacent numbered-tag boundary can be stated conservatively:

```text
v0.3
    -> no claim of the later snap_trimmer introduction

e8e57d9a (18 Aug)
    -> public-tree introduction

v0.4
    -> contains that introduction
```

This does not prove that absolutely no snapshot cleanup code existed anywhere in `v0.3`; it establishes only that the named implementation introduced by `e8e57d9a` is later than that tag.

## H/P — `v0.4` contains both the rough introduction and September fixes

The exact `v0.4` ref points to `13b1bf7c...`, dated 7 October 2008.

Git comparisons establish that both:

- `e8e57d9a` (18 August), and
- `bfb5b8d9` (10 September)

are ancestors of `v0.4`.

The tagged `v0.4` source itself contains the corrected September form. In `ReplicatedPG::snap_trimmer()`, surviving snapshot IDs are appended with:

```cpp
newsnaps.push_back(snaps[i]);
```

rather than the original rough implementation's erroneous index value. The tagged code also loads and revises the head `SnapSet` while processing removed snapshots.

This is strong evidence for **source-state inclusion**.

It is not by itself a functional test result.

The distinction matters because the introduction commit's title says `non-functional`, while the September commit says only `some snap_trimmer fixes`. The safe statement is:

```text
v0.4 contains a later repaired source state
    !=
we have demonstrated that snap trimming works end-to-end in v0.4
```

## H/P — `v0.4` tag time and `0.4-1` packaging changelog time do not coincide

At `v0.4`, `configure.ac` says:

```text
AM_INIT_AUTOMAKE(ceph, 0.4)
```

so the tree itself carries a 0.4 package version marker.

However, the `debian/changelog` **inside the `v0.4` tag** still contains only the older `0.3-1` entry.

Two days later, on 9 October 2008, commit `54548de3` adds:

```text
ceph (0.4-1) unstable
  * Snapshots.
```

That commit is after the `v0.4` tag point and is visible by the later `v0.5` tree.

Therefore:

```text
Git tag named v0.4
    !=
Debian changelog entry for 0.4-1 already present in that exact tagged tree
```

This is a concrete source-provenance reason not to substitute one version artifact for another.

It also blocks an easy but unsafe inference:

```text
0.4 package changelog says "Snapshots."
    -> therefore the v0.4 tagged tree proves snap_trimmer correctness
```

The changelog is product/package-facing feature metadata. It does not isolate the OSD snap-trimmer path or document a passing reclamation test.

## H/P — `v0.5` contains October refinements but predates `snap_trim_wq`

The exact `v0.5` ref points to `1dd42095...`, dated 14 November 2008.

Git ancestry establishes that the 17-October changes `57965a88` and `a15fdb91` are ancestors of this tag.

The tagged `v0.5` `ReplicatedPG::snap_trimmer()` therefore contains the later October-era structure, including per-object `ObjectStore::Transaction` handling and the refined clone/snapshot bookkeeping.

But `v0.5` is an ancestor of the 20-November `69eea16f` work-queue conversion. Therefore:

```text
v0.5
    -> contains October trimmer refinements
    -> does not yet contain the 20-November snap_trim_wq conversion
```

The in-tree version metadata is again not perfectly synchronized: `configure.ac` at `v0.5` still says `AM_INIT_AUTOMAKE(ceph, 0.4)`, while the tag itself is named `v0.5`.

Likewise `debian/changelog` at `v0.5` includes the earlier `0.4-1` `Snapshots.` entry but no `0.5-1` entry yet.

This is not treated as an error to be corrected by inference. It is historical evidence that multiple version-bearing artifacts had different update times.

## H/P — `v0.6` contains the November asynchronous work-queue form

The exact `v0.6` ref points to `a4c752df...`, dated 20 January 2009; the commit message is simply `v0.6`.

Ancestry comparisons establish that both November changes are ancestors of `v0.6`:

- `69eea16f` — convert snap trimming to `snap_trim_wq`;
- `4f8fb979` — remove snapshot collection after it is trimmed.

Direct source inspection at `v0.6` confirms an `OSD::SnapTrimWQ` backed by `snap_trim_queue`, whose `_process(PG *pg)` calls `pg->snap_trimmer()`.

Thus `v0.6` is the first inspected adjacent numbered tag after the November execution-structure transition.

The `v0.6` commit also changes `AM_INIT_AUTOMAKE(ceph, 0.4)` to `0.6` and updates the Debian changelog with entries for `0.5-1` and `0.6-1`. The `0.5-1` entry describes broad `OSD bug fixes`, `efficient snap recovery`, and other work; it does not specifically state that the snap trimmer was fully correct.

Again:

```text
package/release-note language
    !=
mechanism-specific correctness proof
```

---

# Engineering reconstruction

## E — source introduction, tag inclusion, package metadata, and runtime qualification are separate provenance layers

The early history now supports at least five separate relations:

```text
source change introduced
    !=
source change included in numbered tag
    !=
package metadata names a version/feature
    !=
mechanism demonstrated functional
    !=
binary/package distributed or deployed
```

The first two are now directly mapped for the 2008 snap-trimmer changes.

The third is only partially aligned with those tags: the in-tree Debian changelog visibly lags the `v0.4` and `v0.5` tag points.

The fourth and fifth remain separate open evidence questions.

## E — a tag is a source-state boundary, not an automatic quality boundary

A numbered tag answers a specific question:

> Which source state was named by this repository ref?

It does not, without additional evidence, answer:

- whether every advertised subsystem path worked;
- whether tests exercised the path;
- whether a tarball was actually published;
- whether a distribution package was built from exactly that ref;
- whether anyone deployed the code in production.

For Case 153 this distinction is particularly important because the earliest introduction was explicitly called `non-functional` and the next change was only called `some ... fixes`.

## E — version interpretation is itself relational state

A bare string such as `0.4` is insufficient provenance without knowing which artifact carries it:

```text
Git ref v0.4
configure.ac package version 0.4
Debian package changelog 0.4-1
source commit dates
```

These records overlap but are not identical or simultaneous.

For research purposes, preserving the relation among them is more informative than flattening all of them into one synthetic "release date".

## E — first tagged inclusion does not close the first-functional-point debt

`v0.4` is now a strong tag boundary for the repaired September source state, but no controlled runtime evidence was located in this slice that proves the trimmer completed its intended reclamation behavior under representative conditions.

Therefore the earlier open question remains valid:

```text
first numbered tag containing repaired code
    !=
first source/tag proven functional
```

---

# Controlled functional comparison

## A — compatibility / firmware-qualified behavior elsewhere in the repository

Other cases in this repository sometimes distinguish a product/model/version label from the behavior actually qualified for that exact revision.

Case 153 has a boundedly similar provenance problem:

```text
version label retained
    !=
behavioral property established
```

The analogy stops there. Ceph Git tags are not SSD firmware revisions, and no shared implementation genealogy is claimed.

## A — Case 153's later retained-state work

This tag mapping is orthogonal to the stronger 2010 retention result:

```text
removed-snapshot relation
    - purged/completed relation
    -> reconstructed runtime trim obligation
```

The early tags tell us **when particular source embodiments were included in named source states**. They do not retroactively give the 2008 versions the later 2010 persistence semantics.

---

# Philosophical interpretation

## P — names retain less than relations

A version name such as `v0.4` can survive perfectly while the historical relation among source state, package metadata, advertised feature, and runtime evidence is forgotten.

The technical record here supports a restrained interpretation:

> historical retention is not only preservation of labels; it also requires preserving which claims each label actually authorizes.

This remains project-level interpretation. Ceph developers are not being attributed a philosophy of version identity.

---

# Explicit non-claims

1. **Not invention priority.** `e8e57d9a` remains a public-tree introduction boundary, not proof of first conception.
2. **Not first snapshot support.** Snapshot/clone substrate predates the snap trimmer.
3. **Not proof that `v0.4` snap trimming was fully functional.** The tag contains repaired code, but this slice has no end-to-end demonstration.
4. **Not proof that `v0.4` was the first binary release users installed.** This slice maps Git refs/source ancestry.
5. **Not proof that `v0.4-1` Debian binaries were published on 9 October 2008.** The in-tree changelog entry is metadata, not a package-repository publication record.
6. **Not proof that the `v0.4` Git tag was created exactly at the commit timestamp.** The lightweight ref points to that commit; ref-creation time is not separately preserved here.
7. **Not proof that `v0.5` package version metadata was internally consistent.** In fact `configure.ac` still says 0.4 in that tagged tree.
8. **Not permission to replace tag chronology with `debian/changelog` chronology.** They visibly differ.
9. **Not permission to replace package chronology with tag chronology.** The reverse substitution is equally unsafe.
10. **Not proof that the 0.4 `Snapshots.` changelog item specifically means RADOS OSD snap trimming.** It is broad package-facing wording.
11. **Not proof that `some snap_trimmer fixes` fixed every defect.** The message is weaker than that.
12. **Not proof that the October fast-path change demonstrates normal-path correctness.** It handles one empty-collection case.
13. **Not proof that snapshot-collection tracking equals later `SnapMapper`.** Representation changed substantially later.
14. **Not proof that `v0.5` contains `snap_trim_wq`.** It predates that commit in Git ancestry.
15. **Not proof that `v0.6` invented asynchronous trimming.** A dedicated asynchronous worker/thread existed earlier; `snap_trim_wq` changes worker embodiment.
16. **Not proof that `v0.6` has later `purged_snaps` restart semantics.** Those appear in the 2010 source history.
17. **Not proof that tagged source equals deployed production state.** Deployment evidence is absent.
18. **Not proof that a source tag was accompanied by a public announcement.** Announcement archaeology was not required for this slice.
19. **Not proof of secure erasure.** Snapshot clone reclamation is not media sanitization.
20. **Not a genealogy claim to other storage systems.** Comparisons remain functional and bounded.
21. **Not a claim that version metadata should have been synchronized by modern standards.** The observed mismatch is historical evidence, not a normative bug report.
22. **Not a claim that `v0.3` had no snapshot code whatsoever.** It predates the located named trimmer implementation.
23. **Not a claim that commit timestamp equals user-visible release date.** Those are different evidence questions.
24. **Not a claim that `v0.6` Debian changelog retroactively proves exactly what shipped in `v0.5`.** It is later in-tree metadata describing the earlier version line.
25. **Not a maturity promotion for Case 153.** Canonical status remains `grounded`.

---

# Claim ledger

| Claim | Layer | Evidence |
| --- | --- | --- |
| `v0.3` points to a July-2008 commit before the located trimmer introduction | `H/P` | tag ref + ancestry |
| `v0.4` contains `e8e57d9a` | `H/P` | Git ancestry |
| `v0.4` contains `bfb5b8d9` | `H/P` | Git ancestry |
| tagged `v0.4` source has the corrected `newsnaps.push_back(snaps[i])` form | `H/P` | `ReplicatedPG.cc` at `v0.4` |
| `v0.4` tree's `configure.ac` names package version 0.4 | `H/P` | `configure.ac` at tag |
| `v0.4` tree does not yet contain the `0.4-1` Debian changelog entry | `H/P` | `debian/changelog` at `v0.4` |
| 9-Oct commit adds `0.4-1` / `Snapshots.` packaging metadata | `H/P` | `54548de3` |
| `v0.5` contains the 17-Oct trimmer / snapshot-collection refinements | `H/P` | Git ancestry |
| `v0.5` predates `69eea16f` | `H/P` | Git ancestry |
| `v0.5` tree still says Automake package version 0.4 | `H/P` | `configure.ac` at `v0.5` |
| `v0.6` contains `69eea16f` and `4f8fb979` | `H/P` | Git ancestry |
| `v0.6` tagged source directly contains `SnapTrimWQ` | `H/P` | `OSD.h` at `v0.6` |
| tag inclusion != functional qualification | `E` | evidence-type separation |
| tag label != package changelog timing | `E` | observed 0.4/0.5 metadata mismatch |
| source provenance != binary/deployment provenance | `E/X` | distribution/deployment evidence absent |

---

# Debt closed / debt retained

## Closed in this slice

- earliest adjacent numbered-tag boundary for the August introduction + September fixes: **`v0.4`**;
- numbered-tag boundary for the October refinements: **`v0.5`**;
- numbered-tag boundary for the November `snap_trim_wq` / post-trim collection-removal state: **`v0.6`**;
- explicit separation of Git-tag provenance from package changelog timing.

## Still open

- first controlled source/runtime point demonstrating snap-trimmer functionality rather than presence/fixes;
- archival evidence for exact tarball/public-download/package-publication chronology if a stronger **shipping release** claim is needed;
- exact first tag/release containing the **15-May-2010** `purged_snaps` / reconstructed-queue state change;
- complete PG-info v21→v22 migration semantics;
- June-2011 distributed completion-ordering series;
- interruption/fault-injection evidence;
- lower-layer allocator reuse and sanitization boundaries.

---

# Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `snap_trimmer` and `Ceph snapshot trim` found no dedicated packet to reuse in this round.

Keep in `technical-retention`:

- the exact tag/source-state boundary insofar as it prevents an incorrect retention chronology;
- the distinction between source inclusion and functional/reclamation claims;
- source/package provenance distinctions that materially constrain what historical retention claims are allowed.

Route primarily to `computing-archaeology` if later pursued:

- a full Ceph v0.3–v0.6 release history;
- packaging infrastructure history;
- broad snapshot-feature genealogy beyond the reclamation seam;
- deployment/user adoption history not needed to establish the retention relation.
