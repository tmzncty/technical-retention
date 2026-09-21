# Case 153 deepening — Ceph 2010 PG-info v21→v22 snap-trim migration semantics

**Status:** `bounded deepening complete`  
**Canonical:** [`../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md`](../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md)  
**Scope:** the May–July 2010 transition from encoded `PG::Info::snap_trimq` (PG-info v21) to encoded `PG::Info::purged_snaps` plus runtime-reconstructed `PG::snap_trimq` (PG-info v22).  
**Question:** when Ceph changed the retained representation of snapshot-trim progress, did the compatibility decoder preserve the old pending-work set as equivalent new completion state, or did it merely remain able to parse the old bytes and reconstruct future work from a different retained relation?

## Bounded conclusion

The inspected source supports a sharper answer than “Ceph upgraded PG info from v21 to v22.”

Before the transition, PG-info v21 directly retained the pending snapshot-trim queue:

```text
v21 retained state
    P = snap_trimq
        = snapshots still designated for trim
```

Commit `d006ae9331216d413b5b0ef44b7b69ab8580d669` (15 May 2010 PDT / 16 May UTC) changed the encoded PG information to retain a completion relation instead:

```text
v22 retained state
    C = purged_snaps
        = snapshots recorded as already purged

runtime state
    Q = snap_trimq
        = known_removed_snaps - purged_snaps
```

The v22 decoder remains able to **parse** older v21 PG-info bytes, but its legacy branch decodes the old `snap_trimq` into a local temporary variable and does not translate that value into `purged_snaps`:

```cpp
if (v >= 22)
  ::decode(purged_snaps, bl);
else {
  set<snapid_t> snap_trimq;
  ::decode(snap_trimq, bl);
}
```

Therefore the migration boundary is:

```text
legacy bytes are decodable
    !=
legacy pending/completed partition is semantically preserved
```

and:

```text
schema compatibility
    !=
lossless progress-state translation
```

At activation, runtime trim work is reconstructed from the pool's known removed-snapshot relation minus whatever `purged_snaps` completion evidence is available in the v22 PG info:

```cpp
snap_trimq = pool->cached_removed_snaps;
snap_trimq.subtract(info.purged_snaps);
```

The old v21 queue is therefore **not** the authoritative source of the new runtime queue after v22 decoding. The new model makes the retained completion relation and the pool-wide removed-snapshot relation authoritative inputs to reconstruction.

This is a bounded retention result, not a claim that the transition was bug-free. Later 2011 fixes explicitly show that early `snap_trimq` / `purged_snaps` interactions still had correctness bugs.

---

## Claim-type discipline

### Historical record

Primary Ceph source establishes:

- what v21 encoded;
- what commit `d006ae93` changed;
- how v22 decodes older input;
- how runtime `snap_trimq` is reconstructed;
- how the pool-level removed-snapshot relation is built;
- how the later 19-May-2010 completion update records and replicates `purged_snaps`;
- how v0.20.2 and v0.21 differ in completion/progress update ordering.

### Engineering reconstruction

Project terms such as `pending-work state`, `completion relation`, `semantic migration`, `progress partition`, and `conservative reconstruction` describe consequences of the source-level relation. They are not claimed as historical Ceph vocabulary.

### Functional analogy

A bounded comparison to other restart/reconstruction cases is permitted only at the level:

```text
exact transient work representation may be discarded
while a retained relation is used to regenerate operational work
```

This is not evidence of shared implementation, design lineage, or common terminology.

### Philosophical interpretation

The narrow interpretive point is that persistence across a representation change can preserve the **capacity to resume an obligation** without preserving an exact historical image of every prior progress state. That statement is downstream of the source mechanics; it is not attributed to Ceph developers.

---

# Primary source ladder

| Source | Date | Evidence class | Use here |
| --- | --- | --- | --- |
| Ceph parent commit `47ba928ba928f4f4ae0202b7a509748a6bb06c95`, `src/osd/PG.h` | before 16-May-2010 UTC | `H/P` | v21 directly encodes `PG::Info::snap_trimq` |
| Ceph commit `d006ae9331216d413b5b0ef44b7b69ab8580d669`, `osd: purged_snaps in PG::Info, queue snap trim on primary` | 15-May-2010 PDT / 16-May UTC | `H/P` | v21→v22 schema change; legacy decode branch; runtime queue reconstruction; primary-only scheduling changes |
| Ceph `src/osd/osd_types.h` at `d006ae93` | May 2010 | `H/P` | `build_removed_snaps()` defines the known-removed relation from explicit `removed_snaps` or inferred gaps in the pool snapshot set |
| Ceph `src/osd/OSD.cc` at `d006ae93` | May 2010 | `H/P` | builds `PGPool::cached_removed_snaps` from pool state and tracks newly removed snaps |
| Ceph commit `4ed3acb08a99ee4562c23bd38ccc98fffd019e8b`, `osd: update purged_snaps in PG::Info on trim completion; and replicate` | 19-May-2010 PDT / 19-May UTC | `H/P` | makes `purged_snaps` an explicit trim-completion relation and propagates updated PG info to replicas |
| Ceph v0.20.2 `src/osd/ReplicatedPG.cc` | 27-May-2010 release line | `H/P` | old queue-in-PG-info trim/completion ordering |
| Ceph v0.21 `src/osd/PG.h` | 29-Jul-2010 release | `H/P` | public numbered release still carries the v22 legacy decoder that discards decoded v21 queue contents |
| Ceph v0.21 `src/osd/PG.cc` | 29-Jul-2010 release | `H/P` | activation reconstructs runtime `snap_trimq = cached_removed_snaps - purged_snaps` |
| Ceph v0.21 `src/osd/ReplicatedPG.cc` | 29-Jul-2010 release | `H/P` | primary inserts `sn` into `purged_snaps`, removes it from runtime queue, and writes PG info with collection removal in one submitted ObjectStore transaction |
| Ceph commits `8f327d11...` and `f2755a53...` | 12–13-Jan-2011 | `H/P` | later bug/fix witnesses that constrain any claim of universal correctness in the early model |

Primary URLs:

- <https://github.com/ceph/ceph/commit/d006ae9331216d413b5b0ef44b7b69ab8580d669>
- <https://github.com/ceph/ceph/commit/4ed3acb08a99ee4562c23bd38ccc98fffd019e8b>
- <https://github.com/ceph/ceph/blob/47ba928ba928f4f4ae0202b7a509748a6bb06c95/src/osd/PG.h>
- <https://github.com/ceph/ceph/blob/d006ae9331216d413b5b0ef44b7b69ab8580d669/src/osd/osd_types.h>
- <https://github.com/ceph/ceph/blob/d006ae9331216d413b5b0ef44b7b69ab8580d669/src/osd/OSD.cc>
- <https://github.com/ceph/ceph/blob/v0.20.2/src/osd/ReplicatedPG.cc>
- <https://github.com/ceph/ceph/blob/v0.21/src/osd/PG.h>
- <https://github.com/ceph/ceph/blob/v0.21/src/osd/PG.cc>
- <https://github.com/ceph/ceph/blob/v0.21/src/osd/ReplicatedPG.cc>
- <https://github.com/ceph/ceph/commit/8f327d11cab449b875ffe9818c9ee7ecfe854204>
- <https://github.com/ceph/ceph/commit/f2755a533753767979e0aac00953cb870340a880>

---

# Historical record

## H/P — v21 directly retains the pending trim set

In the parent of `d006ae93`, `PG::Info` contains:

```cpp
set<snapid_t> snap_trimq; // snaps we need to trim
```

The encoder identifies the structure as version 21 and serializes the queue directly:

```cpp
__u8 v = 21;
...
::encode(snap_trimq, bl);
```

The decoder directly restores the member:

```cpp
::decode(snap_trimq, bl);
```

This is not merely a field-name observation. The v0.20.2 trimmer consumes `info.snap_trimq` directly:

```cpp
while (info.snap_trimq.size() && is_active()) {
  snapid_t sn = *info.snap_trimq.begin();
  ...
  info.snap_trimq.erase(sn);
}
```

So the retained field and the worker's pending set are the same representation in that source line.

Bounded result:

```text
v21 PG info
    retains pending work directly
```

Do not strengthen this into a claim that every mutation of the in-memory set was already durably persisted at every instruction boundary.

---

## H/P — v0.20.2 completion updates the direct queue representation

The v0.20.2 `snap_trimmer()` processes one snapshot ID `sn`, changes object/snapshot metadata, then constructs an ObjectStore transaction that includes:

```cpp
snap_collections.erase(sn);
write_info(*t);
t->remove_collection(c);
```

After submitting that transaction, it executes:

```cpp
info.snap_trimq.erase(sn);
```

After the loop completes, it submits another transaction containing:

```cpp
write_info(*t);
```

The exact persistence semantics depend on the ObjectStore/journal layer and are not re-proved here. The source-level ordering nevertheless matters: the queue member is erased **after** the per-snapshot collection-removal transaction is submitted, and the emptied/reduced queue is written again later.

This supports a bounded observation:

```text
old model:
physical/logical trim work
    -> queue progress mutation
    -> later PG-info write of reduced pending set
```

It does **not** establish a formal exactly-once protocol.

---

## H/P — `d006ae93` changes the retained meaning, not only the container type

Commit `d006ae93` replaces:

```cpp
set<snapid_t> snap_trimq;
```

inside encoded `PG::Info` with:

```cpp
interval_set<snapid_t> purged_snaps;
```

and changes:

```text
PG-info v21 -> PG-info v22
```

At the same time, the runtime `PG` object gains:

```cpp
interval_set<snapid_t> snap_trimq;
```

This is a semantic inversion of which side of the maintenance relation is retained:

```text
before:
retain what remains to be done

later:
retain what has been completed
and reconstruct what remains to be done
```

The word “inversion” here is project engineering vocabulary. The source itself uses `snap_trimq` and `purged_snaps`.

---

## H/P — the v22 legacy branch parses v21 but discards the old queue value

The most important migration detail is the v22 decoder:

```cpp
if (v >= 22)
  ::decode(purged_snaps, bl);
else {
  set<snapid_t> snap_trimq;
  ::decode(snap_trimq, bl);
}
```

The legacy value is decoded into a **local** variable named `snap_trimq`.

There is no source statement in that branch equivalent to:

```cpp
this->purged_snaps = ...derived from legacy snap_trimq...;
```

nor is the local v21 queue assigned to the runtime `PG::snap_trimq` from inside the decoder.

Therefore the narrow historical/source claim is strong:

> the compatibility decoder consumes the old serialized field so that the record can be parsed, but the decoded v21 pending set is not itself migrated into the new retained `purged_snaps` field.

This is why:

```text
wire/on-disk decode compatibility
    !=
semantic preservation of the old progress partition
```

---

## H/P — runtime work is rebuilt from pool removal state minus retained completion state

The same May-2010 change makes `PG::activate()` compute:

```cpp
snap_trimq = pool->cached_removed_snaps;
snap_trimq.subtract(info.purged_snaps);
```

and queues trim work if the result is not empty.

`PGPool::cached_removed_snaps` is not an arbitrary worker checkpoint. `OSD.cc` initializes it from the pool description through:

```cpp
pi->build_removed_snaps(p->cached_removed_snaps);
```

and `pg_pool_t::build_removed_snaps()` is documented in source as building the set of known removed snapshots from either the explicit `removed_snaps` set or the pool's snapshot set/sequence.

Its core logic is:

```cpp
if (removed_snaps.empty()) {
  rs.clear();
  for (snapid_t s = 1; s <= get_snap_seq(); s = s + 1)
    if (snaps.count(s) == 0)
      rs.insert(s);
} else {
  rs = removed_snaps;
}
```

Thus the new runtime queue is derived from two relations of different scope:

```text
R = pool-known removed snapshots
C = PG-retained purged/completed snapshots

Q = R - C
```

This is a stronger reconstruction basis than the statement “the queue gets rebuilt somehow.”

---

## H/P — the v0.21 public release keeps this compatibility behavior unchanged

The tagged v0.21 `PG.h` still encodes v22 and still contains the same older-version branch:

```cpp
if (v >= 22)
  ::decode(purged_snaps, bl);
else {
  set<snapid_t> snap_trimq;
  ::decode(snap_trimq, bl);
}
```

The tagged v0.21 `PG.cc` still reconstructs:

```cpp
snap_trimq = pool->cached_removed_snaps;
snap_trimq.subtract(info.purged_snaps);
```

Therefore this is not merely a transient development-tree artifact between commits. It is present in the first inspected numbered release already established to carry the v22 state model.

---

## H/P — `purged_snaps` becomes explicit completion evidence on 19 May 2010

Commit `4ed3acb08a99ee4562c23bd38ccc98fffd019e8b` is titled:

```text
osd: update purged_snaps in PG::Info on trim completion; and replicate
```

In the primary trimmer it adds:

```cpp
info.purged_snaps.insert(sn);
```

and sends the updated `PG::Info` to replicas.

On receipt, a replica computes newly learned completed snapshots:

```cpp
interval_set<snapid_t> p = info.purged_snaps;
p.subtract(pg->info.purged_snaps);
```

and, when new completion evidence is present, removes the matching snapshot collection and updates its own `pg->info.purged_snaps` before writing PG info.

This source is important because it prevents a weak interpretation of the new field as merely a renamed queue. Its direction is the opposite:

```text
membership in purged_snaps
    = completion/retirement evidence used to suppress future trim obligation
```

---

## H/P — v0.21 couples local completion marking with collection removal more tightly than v0.20.2

In tagged v0.21, after per-object trim work for a snapshot completes, the primary does:

```cpp
info.purged_snaps.insert(sn);
snap_trimq.erase(sn);
```

then builds one ObjectStore transaction containing:

```cpp
write_info(*t);
t->remove_collection(c);
```

and submits that transaction.

This gives a clear source-level local coupling:

```text
mark sn completed in retained PG info
    + remove local snapshot collection
    -> same submitted ObjectStore transaction
```

That differs from the v0.20.2 source ordering, where the queue reduction happens after the per-snapshot transaction and is persisted by a later PG-info write.

This evidence does **not** prove that the distributed operation is globally atomic. Replica propagation is a separate step, and lower-layer crash semantics depend on ObjectStore/journal behavior outside this slice.

---

## H/P — later fixes prohibit treating v22 reconstruction as a universal correctness certificate

Two early-2011 commits are direct counterevidence to any claim that the new relation immediately solved every edge case.

`8f327d11cab449b875ffe9818c9ee7ecfe854204` says an OSD bug could cause `snap_trimq` to contain snapshots already present in `purged_snaps`; the commit calls itself a work-around and says a real fix is still needed.

`f2755a533753767979e0aac00953cb870340a880` says activation on replicas could queue snap trimming when `purged_snaps` lagged behind `pool->cached_removed_snaps`, “guaranteeing a crash” for the described condition, and changes activation so replicas do not enqueue the trimmer that way.

These later records do not negate the 2010 state-model analysis. They bound it:

```text
reconstructable obligation relation
    !=
all authority / role / propagation conditions correct
```

---

# Engineering reconstruction

## E — the migration does not preserve an exact old pending/completed partition

Let:

```text
R = all snapshots currently known by the pool state to be removed
P = old v21 pending trim set
C = completed/purged set
```

If the old state were perfectly partitioned at one instant, one might algebraically imagine:

```text
C = R - P
```

But the v22 compatibility decoder does not perform that conversion. It does not receive/use the pool-wide `R` relation there, and it does not assign a derived value to `purged_snaps`.

Instead it consumes the old `P` bytes and later runtime activation computes work from:

```text
Q = R - C
```

where `C` is the new retained field.

Therefore the schema conversion itself does not carry forward the old partition between:

- removed snapshots already completed; and
- removed snapshots still pending.

This is the precise sense in which the compatibility path is **decode-compatible but not a lossless semantic migration of trim progress**.

---

## E — obligation preservation can be conservative rather than history-preserving

Because runtime work is regenerated from a broader removed-snapshot relation, the system can preserve the ability to rediscover work without preserving the exact old worker-state history.

The bounded shape is:

```text
retain/recover a superset relation R
    + retain completion evidence C where available
    -> regenerate candidate work Q = R - C
```

If completion evidence is missing or not translated, the reconstruction can conservatively classify more removed snapshots as candidates for trim than an exact old pending queue would have contained.

This is not automatically data loss. It is a change in how maintenance progress is represented and recovered.

Whether repeated processing is harmless depends on the idempotence/role/error behavior of the concrete trimmer; later bugs show that this must not be assumed universally.

---

## E — “retained completion evidence” and “retained worker checkpoint” have different failure semantics

The two schemas answer different restart questions.

### v21-style question

```text
What exact snapshots did this PG still think it had to trim?
```

### v22-style question

```text
Which removed snapshots has this PG already recorded as purged?
What remains after subtracting them from the pool's removed relation?
```

The v22 model therefore makes restart work depend on a relation between two retained/current sources rather than on restoration of one serialized queue.

This is a retention architecture change, not just a serialization optimization.

---

## E — state authority changes with representation

The runtime queue itself is no longer sufficient evidence of durable completion.

In v22:

```text
runtime snap_trimq membership
    = current candidate / worker state

purged_snaps membership
    = retained completion evidence

pool cached_removed_snaps membership
    = source relation for removed snapshots
```

These states have different authority and persistence horizons.

Therefore:

```text
runtime queue empty
    !=
proof that the pool has no removed snapshots
    !=
proof that completion evidence is globally converged
```

The 2011 replica bug is a concrete reason not to collapse those layers.

---

# Controlled functional comparison

## FA — relation reconstruction versus exact worker-state retention

A useful cross-case comparison is Case 79's HDFS startup re-observation boundary.

In HDFS, some runtime replica-location knowledge is reconstructed from later block reports rather than retained as an exact restart image. In this Ceph slice, runtime trim work is reconstructed from already-retained pool removal state and per-PG completion state rather than from a retained exact worker queue.

The shared functional pattern is only:

```text
exact operational working set need not itself be the durable object
if authoritative enough relations can regenerate it
```

The mechanisms are otherwise different:

- HDFS re-observes DataNode state through protocol reports;
- Ceph v22 computes a set difference over snapshot-removal/completion relations;
- neither comparison proves historical influence or shared design ancestry.

---

## FA — queue checkpoint versus completion frontier

Another bounded functional contrast is maintenance systems that checkpoint a progress cursor or event counter.

```text
checkpointed worker progress
    -> resume near prior execution point

retained completion relation
    -> recompute remaining obligation from source relation - completion relation
```

Both can support restart, but their loss/replay behavior differs. A missing checkpoint may redo a suffix; missing completion evidence can reintroduce already-performed items into the candidate set.

This is a functional comparison, not a universal taxonomy claim.

---

# Philosophical interpretation

## PI — continuity of obligation does not require continuity of representation

The narrow philosophical result is that a maintenance obligation may remain actionable across a schema change even when the system no longer preserves the same representation of “what is left to do.”

The identity that survives is relational:

```text
removed snapshot relation
    + recorded completion relation
    -> what still requires work
```

not necessarily:

```text
the same serialized queue bytes survive every version transition
```

This matters for technical retention because “the system remembers the unfinished work” can hide several distinct mechanisms:

- preserve the exact pending set;
- preserve a cursor/checkpoint;
- preserve completion evidence;
- preserve/recover a source relation from which unfinished work can be derived;
- re-observe the world and reconstruct work.

Ceph's v21→v22 transition is evidence for one concrete shift between those forms. It is not evidence that all technical memory is fundamentally relational, nor that recomputation is always preferable to direct persistence.

---

# Explicit non-claims

This slice does **not** claim that:

1. PG-info v22 was the first design ever to retain completion rather than pending work.
2. `purged_snaps` was invented in May 2010 rather than merely introduced at this inspected public-tree boundary.
3. decoding v21 bytes means the old trim queue is semantically migrated.
4. the v21 queue is copied into runtime `PG::snap_trimq` by the v22 decoder.
5. the v21 queue is transformed into `purged_snaps` by the v22 decoder.
6. `purged_snaps` is identical to the old pending queue under a renamed field.
7. `cached_removed_snaps` is a durable worker queue.
8. `cached_removed_snaps` is itself the complete historical record of snapshot deletion events.
9. every removed snapshot in the pool necessarily has physical clone material remaining.
10. a reconstructed `snap_trimq` entry proves that useful payload still exists.
11. queue membership proves trim execution has started.
12. queue absence proves lower-layer physical reclamation or sanitization.
13. `purged_snaps` membership proves NAND/disk sectors have been securely erased.
14. `purged_snaps` membership proves every replica has already converged.
15. one ObjectStore transaction here proves cluster-wide atomicity.
16. one ObjectStore transaction here re-proves FileStore/journal crash semantics.
17. v0.20.2's ordering is a formally specified exactly-once algorithm.
18. v0.21's ordering is a formally specified exactly-once algorithm.
19. conservative replay/retrim is harmless under every error and role transition.
20. the 2011 bugs invalidate the bounded 2010 source-state relation.
21. the 2011 fixes close every later snaptrim bug.
22. v22's compatibility decoder was intended by developers as a philosophical statement about memory.
23. a local temporary variable being discarded necessarily constitutes user-visible data loss.
24. completion evidence and pending-work evidence are interchangeable without the source relation `R`.
25. `R - C` is valid if `R` or `C` is stale, corrupt, or semantically inapplicable.
26. runtime queue reconstruction means no state needs persistence.
27. schema compatibility implies behavioral equivalence across versions.
28. source compatibility implies deployment compatibility.
29. v0.21 tag inclusion proves every production cluster upgraded through this exact path.
30. the HDFS comparison establishes Ceph↔HDFS influence or shared genealogy.

---

# What this changes in Case 153

Before this slice, Case 153 had already established:

```text
retained removed-snapshot relation
    - retained purged/completed relation
    -> reconstructed runtime trim obligation
```

and had mapped that state model to v0.21.

This slice closes the narrower migration question:

> What happens when a v22 decoder encounters the old v21 encoded pending queue?

Answer:

```text
v21 pending queue bytes
    -> parsed into a temporary compatibility variable
    -> not translated into v22 purged/completion state

then, at PG activation:

pool removed-snapshot relation
    - retained v22 purged relation
    -> runtime trim queue
```

The new boundary is therefore:

```text
legacy record legibility
    !=
legacy progress-state preservation
```

Case 153 remains **`grounded`**. This evidence strengthens one restart/version-migration seam but does not close the separate early functional-demonstration, June-2011 distributed-completion, fault-injection, or lower-layer reclamation questions.

---

# Remaining debt after this slice

Highest-value follow-ups now are:

1. establish the first source/runtime point where the 2008 trimmer can be demonstrated functional rather than merely present/fixed/tagged;
2. finish the June-2011 replica-application / completion-publication state-machine series;
3. fault-inject interruption around primary trim completion, PG-info persistence, replica propagation, and collection removal;
4. trace how later PG-info / peering code preserves or repairs `purged_snaps` currentness;
5. trace lower-layer allocator reuse separately from logical clone reclamation;
6. keep sanitization / forensic remanence as a separate evidence problem;
7. retrieve/hash historical release archives only if bit-for-bit distribution provenance becomes necessary.

The previously open **PG-info v21→v22 migration-semantics** debt is closed at the inspected source level by this file.

---

# Related-repository boundary

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `purged_snaps` returned no dedicated packet to reuse in this round.

Keep here:

- pending-work versus completion-state persistence;
- exact compatibility-decoder behavior where it changes a retention claim;
- runtime reconstruction of maintenance obligation;
- source-level ordering relevant to retained progress/completion evidence;
- bounded cross-case comparison.

Route primarily to `computing-archaeology` if pursued:

- full Ceph serialization/feature-bit genealogy;
- generic PG-info format history;
- complete FileStore/ObjectStore journal archaeology;
- broad Ceph upgrade/release engineering history;
- deployment/adoption chronology independent of this retention seam.
