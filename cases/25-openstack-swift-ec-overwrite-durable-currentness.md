# OpenStack Swift EC Overwrites: Timestamp Cohorts, `.durable` Markers, and Mutable Coded Currentness

## Scope

- **Bounded system:** OpenStack Swift erasure-coded object storage as released in Swift 2.3.0 (Kilo, 30 April 2015) and sharpened by Swift 2.10.1 (December 2016).
- **Bounded mechanism:** mutable object PUT/overwrite under an erasure-code storage policy, especially fragment-archive timestamps/indexes, the multi-phase PUT conversation, `.durable` commit markers, same-timestamp GET reconstruction, delayed deletion of older object versions, and reconstructor repair.
- **Primary source base:** the OpenStack Swift source tree and release documentation at the signed `2.3.0` tag and `2.10.1` tag/release state.
- **Research question:** when several coded fragments and several object timestamps can coexist, what retained relations let Swift decide that a particular coded object version is sufficiently committed to serve, repair, and eventually replace an older one?

This is **not** a general history of OpenStack Swift, object storage, Reed–Solomon coding, eventual consistency, two-phase commit, or OpenStack releases. It does not claim that Swift invented erasure coding, quorum storage, version timestamps, or transaction commit protocols.

The bounded retention claim is:

> **For mutable erasure-coded objects, mathematical reconstructability is insufficient. Swift must retain and recover a version-qualified relation among a timestamp, distinct fragment indexes, and a durability marker before that coded version is admissible for normal recovery and before older timestamped state can be retired.**

That statement is an **engineering reconstruction** from documented Swift behavior. `timestamp cohort`, `admissible coded version`, and `version-retirement gate` below are project terms, not historical Swift vocabulary.

---

## Historical vocabulary

The 2015–2016 Swift material directly uses:

- `erasure code` / `EC`;
- `storage policy`;
- `segment`;
- `fragment`;
- `fragment archive` / `EC archive`;
- `fragment archive index`;
- `.data`;
- `.durable` / `durable file`;
- `timestamp`;
- `quorum`;
- `multi-phase` / `multiphase commit`;
- the `essence of a 2 phase commit`;
- `reconstructor` / `reconstruction`;
- `handoff`;
- `primary` node;
- `ssync`;
- `bit rot`;
- `quarantine`.

The following are **project engineering terms** only:

- `timestamp cohort` — fragments sharing one object timestamp and usable fragment-index relation;
- `durability witness` — the role played by `.durable` in qualifying a timestamped fragment set;
- `admissible coded version`;
- `version-retirement gate`;
- `coded currentness`.

Swift's own documentation warns that its multi-phase conversation is used **without introducing strong consistency semantics** and describes it only as having the `essence` of a two-phase commit. This case therefore does not silently normalize the mechanism into database `2PC` or distributed consensus.

---

## Historical record

### H/P — Swift 2.3.0 introduced EC as a beta storage-policy type

The signed `2.3.0` tag points to commit `f8dee761bd36f857aa1288c27e095907032fad68`; the tagger timestamp is **2015-04-30**. Its changelog states that Swift now supports an erasure-code storage-policy type, that the external client API remains the same as for replicated storage, that PyECLib/liberasurecode supplies coding functions, and that the feature is **beta** and relies on `ssync` for durability.

This matters as a historical boundary: the first source used here describes a feature still being validated, not a settled universal object-store contract.

**Primary anchors:** OpenStack Swift signed `2.3.0` tag; `CHANGELOG`, `swift (2.3.0)` entry; `doc/source/overview_erasure_code.rst` at the same commit.

### H/P — an EC fragment archive carries both timestamp and fragment index

The 2.3.0 EC overview says that EC archives are stored with the fragment archive index encoded in the filename. Its concrete example is:

```text
1418673556.92690#5.data
```

A corresponding marker for the timestamp is:

```text
1418673556.92690.durable
```

The fragment index is needed because a node can hold archives of different indexes; without distinct names one fragment-index embodiment could overwrite another.

The 2.10.1 documentation retains the same fundamental separation: a fragment archive has an index, while `.durable` is timestamp-scoped rather than one marker per fragment index.

**Primary anchors:** Swift 2.3.0 and 2.10.1, `overview_erasure_code.rst`, `On Disk Storage`.

### H/P — the PUT path separates fragment landing from durable commit

The 2.3.0 design uses a multipart MIME conversation between proxy and object servers. The documentation says this is necessary because the proxy must know that enough fragment archives have actually made it to disk before it tells the client that a PUT succeeded. It explicitly says the design does this **without introducing strong consistency semantics** and provides the `essence of a 2 phase commit`.

The documented flow is:

```text
encode/stream fragment archives
    -> object servers finish data/metadata write
    -> first-phase responses
    -> proxy observes quorum
    -> proxy sends commit confirmation
    -> object servers create <timestamp>.durable
    -> final success responses
    -> proxy may report client success
```

The `.durable` file is described as an indicator of the `last known durable set of fragment archives` for an object timestamp.

**Primary anchor:** Swift 2.3.0, `overview_erasure_code.rst`, `Multi_Phase Conversation`.

### H/P — commitment of the newer timestamp gates deletion of older timestamped state

The 2.3.0 documentation states that completion of the commit phase is also the signal allowing object servers to delete older timestamp files. It gives the reason explicitly: the old object must not be deleted until the server receives confirmation that enough fragments of the new object have landed elsewhere for a quorum.

The 2.10.1 documentation preserves this sequencing after its quorum rules are tightened: completion of the commit phase again authorizes immediate deletion of older timestamp files, and the text again says this is critical because the older object must not disappear before the new fragment quorum is known to exist.

This is direct historical evidence that **new fragment bytes may coexist with an older object version, and mere creation of the newer bytes is not itself sufficient authority to retire the previous version.**

**Primary anchors:** Swift 2.3.0 and 2.10.1, `overview_erasure_code.rst`, `Multi_Phase Conversation`.

### H/P — partial pre-commit PUTs can leave fragment bytes that do not count as a successful object PUT

Swift 2.3.0 describes a proxy failure after fragment transmission has begun but before the commit message. Storage nodes can then contain `.data` fragment archives while lacking knowledge that enough fragments exist elsewhere for the object to be reconstructed. The client has not received a success response; the documented release treats the PUT as failed and leaves stale fragment archives for cleanup.

Thus the period implementation itself provides a counterexample to the shortcut:

```text
newer fragment physically present
    == newer object successfully retained
```

That equivalence is false in the bounded Swift regime.

**Primary anchor:** Swift 2.3.0, `overview_erasure_code.rst`, `Partial PUT Failures`.

### H/P — Swift 2.10.1 makes the durability quorum stronger and explicit

The 2.10.1 documentation does **not** have exactly the same second-phase rule as the original 2.3.0 text. It requires:

- first-phase success from `ec_ndata + 1` fragment archives;
- second-phase success from `ec_ndata + 1` commits;
- creation of `<timestamp>.durable` after commit confirmation;
- reconstructor propagation of missing `.durable` markers.

The documentation explains the extra fragment as preserving reconstructability even if one fragment archive later becomes unavailable.

This case therefore keeps 2015 and 2016 semantics separate. It uses the evolution as evidence that **durability/currentness thresholds are protocol-version properties**, not timeless consequences of erasure-code algebra.

**Primary anchor:** Swift 2.10.1, `overview_erasure_code.rst`, `Multi_Phase Conversation`.

### H/P — a successful GET requires a same-timestamp, distinct-index fragment set plus a durability indication

Swift 2.10.1 gives the strongest bounded currentness rule in this case. The proxy seeks:

1. `ec_ndata` **distinct EC archives**;
2. at the **same timestamp**;
3. plus an indication from at least one object server that a `<timestamp>.durable` file exists for that timestamp.

If the first primaries do not provide that set, the proxy continues to other primaries and then handoffs.

The documentation also says that the proxy can receive archives from several timestamps and several archives with the same fragment index; it must ensure that it has enough archives **with the same timestamp and distinct fragment indexes** before considering the GET successful.

This directly blocks an algebra-only model in which any `k` surviving fragments are interchangeable merely because they belong to the same coding scheme.

**Primary anchor:** Swift 2.10.1, `overview_erasure_code.rst`, `GET`.

### H/P — one same-timestamp durability marker can qualify fragments whose local nodes lack the marker

The 2.10.1 GET description says the proxy does not require every object server returning a fragment archive to possess its own `.durable` file. It is sufficient that at least one object server reports a `.durable` marker at the same timestamp as the usable fragment archives.

That makes `.durable` neither a payload fragment nor simply a per-file checksum. It is a retained control fact about a **set-level commit relation** whose effect can qualify fragment archives distributed elsewhere.

**Primary anchor:** Swift 2.10.1, `overview_erasure_code.rst`, `GET`.

### H/P — repair can restore missing fragments and missing durability markers after service-level commitment

The 2.3.0 and 2.10.1 descriptions assign EC repair to the `reconstructor`. Unlike simple replication, it may have to read enough surviving fragments, decode the missing index locally, and then push the reconstructed fragment. Reconstruction can follow drive failure, rebalance, handoff reversion, or bit rot.

The 2.10.1 text also states that the reconstructor propagates missing `.durable` markers. Therefore service-level commitment and the fully converged physical distribution of both payload fragments and durability markers can be separated in time.

**Primary anchors:** Swift 2.3.0/2.10.1, `Reconstruction` / `The Reconstructor`.

### H/P — fragment validity is not reducible to fragment existence

The Swift 2.10.1 release changelog records a concrete EC integrity correction: `ssync` could under some circumstances write bad fragment data, so Swift added a check for the correct fragment byte count before finalizing a write; EC fragment metadata is validated on read, and bad data is quarantined.

This source is used only for an implementation boundary:

> a physically present fragment archive can still fail the implementation's validity checks.

It does not prove that all earlier Swift fragments were unreliable, and it does not substitute for the timestamp/commit rule above.

**Primary anchor:** Swift 2.10.1 release changelog / release-note entry, December 2016.

---

## Retained state

The bounded mechanism retains more than encoded payload.

### 1. Object payload

The client-visible object state represented by a reconstructable collection of data/parity fragment archives.

### 2. Object timestamp

The timestamp distinguishes versions of the same object name and participates directly in selecting a usable coded set.

### 3. Fragment index

Distinct indexes identify complementary encoded contributions. Several archives with the same index are not equivalent to a reconstructable set of distinct indexes.

### 4. Durability marker

`<timestamp>.durable` records that the timestamp has crossed Swift's documented commit condition. It is zero-byte control state, not application payload.

### 5. Placement and handoff state

The ring determines primaries; handoffs temporarily extend the search/placement set when primaries are unavailable.

### 6. Reconstruction / synchronization state

The reconstructor repairs missing fragment archives, returns handoff data toward primaries, and propagates durability markers.

### 7. Integrity metadata

Fragment metadata, object ETag/content length metadata, and later validation/quarantine behavior help distinguish a usable fragment archive from bytes that merely exist on disk.

---

## Physical / logical substrate

The case spans:

- ordinary files in object-server filesystems;
- timestamped `.data` fragment archives;
- fragment-index naming;
- zero-byte `.durable` files;
- ring-derived node placement;
- proxy-side erasure coding and reconstruction;
- storage-node metadata and `ssync`/reconstructor maintenance.

The mathematical code determines what combinations *could* reconstruct a payload. Swift's retained timestamp/index/durability relations determine which combinations the object service is willing to treat as one successfully committed version.

---

## Retention mechanism

### During PUT

The proxy encodes the object, distributes indexed fragment archives, waits for the documented first-phase threshold, sends a commit confirmation, then waits for the documented commit threshold before client success.

### Across overwrite/version replacement

Older timestamped state remains protected from deletion until the newer timestamp crosses the commit boundary. The new representation therefore has a transition period in which old and new physical state may coexist.

### During GET

The proxy selects enough **same-timestamp** and **distinct-index** archives and requires a same-timestamp durability indication before reconstructing the client-visible object.

### During repair

The reconstructor can synthesize a missing fragment index from surviving fragments and propagate missing `.durable` state; repair and steady-state placement can therefore continue after an object is already serviceable.

---

## Addressing and access geometry

Client addressing remains object-like and hides EC details. Internally, a recovery path is closer to:

```text
account/container/object
    -> storage policy + ring
    -> candidate primaries/handoffs
    -> timestamped EC archives
    -> choose one same-timestamp cohort
    -> require distinct fragment indexes
    -> require same-timestamp durability indication
    -> decode object segments
    -> return client-visible object
```

The case therefore adds a **version-qualified coded-access geometry** to Cases 19 and 24. A physical fragment location alone does not identify the retained object, and coding algebra alone does not identify the current version.

---

## Read semantics

A successful GET is reconstructive: the proxy may contact several nodes and decode from enough fragment archives.

The important bounded read rule is not simply `collect k fragments`. The 2.10.1 proxy checks timestamp equality, fragment-index distinctness, and durability evidence. A returned object is therefore the result of **selection + admissibility + decoding**, not decoding alone.

This case does not claim linearizable reads or a universal Swift consistency model.

---

## Write and erasure semantics

A PUT can create newer timestamped fragment archives while the previous version still exists. The newer bytes do not immediately erase or deauthorize the old version.

Deletion of older timestamp files is gated by successful completion of the newer commit phase. In the bounded docs, this is explicitly intended to avoid destroying the older object before enough of the replacement coded representation is known to have landed.

This is not secure erasure. `older timestamp deletion` here is logical/filesystem retirement in the object-store implementation, not a claim about raw-media sanitization.

---

## Time

Relevant timescales include:

- streaming/encoding time during PUT;
- time between first-phase fragment landing and commit confirmation;
- a period of coexistence between old and new timestamps;
- delayed propagation of `.durable` markers;
- reconstruction after partial failure, rebalance, handoff use, or bit rot;
- cleanup of stale pre-commit fragment archives.

Unlike DRAM refresh, none of these is a fixed physical decay deadline. They are **protocol-, failure-, workload-, and maintenance-triggered** retention intervals.

---

## Maintenance and labor

Persistence depends on invisible distributed work:

- proxy-side segment buffering and encoding;
- quorum tracking;
- multi-phase commit messaging;
- ring placement and handoffs;
- object-server file/metadata maintenance;
- `ssync`;
- reconstructor scanning, decoding, and transfer;
- auditor/integrity validation and quarantine;
- stale-fragment cleanup.

A client can experience a simple PUT/GET API while the system continuously maintains the relations that make one coded timestamp usable.

---

## Failure / forgetting modes

Keep these distinct:

- insufficient first-phase fragment landing;
- proxy failure before commit;
- newer partial fragments without a durability marker;
- missing `.durable` propagation;
- too few distinct fragment indexes;
- fragment archives from incompatible timestamps;
- primary-node unavailability requiring handoff search;
- corrupted/truncated fragment archive;
- fragment metadata failure and quarantine;
- drive loss / bit rot requiring reconstruction;
- premature deletion of an older timestamp before replacement durability — explicitly the condition the documented commit gate is meant to avoid;
- stale pre-commit fragment archives that survive physically but are not a successful committed version.

These are not one generic `data loss` mechanism.

---

## Engineering reconstruction

### E1 — coded recoverability ≠ version admissibility

Erasure coding says which indexed fragments are mathematically sufficient to decode. Swift additionally requires those fragments to belong to the same timestamped version and requires durability evidence.

### E2 — fragment presence ≠ committed object retention

A pre-commit proxy failure can leave `.data` files on storage nodes while the PUT remains failed. Physical presence of newly encoded bytes is therefore weaker than successful object retention under the documented service contract.

### E3 — newer timestamp ≠ authority to forget the older timestamp

Old files are deleted only after the new commit phase succeeds. Version order alone does not authorize retirement; successful replacement retention does.

### E4 — currentness can be cohort-level rather than fragment-local

In 2.10.1, one same-timestamp `.durable` indication can qualify a reconstructable set whose other contributing nodes lack their own marker. The relevant retained currentness fact concerns a distributed set relation.

### E5 — client success ≠ completed placement/marker convergence

The reconstructor can later fill missing fragments and propagate durability markers. The service boundary and the fully repaired steady-state topology can finish at different times.

### E6 — durability semantics are protocol-version-specific

Swift 2.3.0 and 2.10.1 do not use identical commit thresholds. The repository must therefore cite the version before turning `Swift EC durability` into a stable abstract property.

---

## Philosophical / media-theoretical interpretation

This case sharpens a modest point about identity and technical availability.

The retained object is not exhausted by one material fragment, nor even by `enough bytes somewhere`. A version becomes ordinarily recoverable because the system preserves a relation among:

- one object designation;
- one timestamp;
- a sufficient set of distinct coded indexes;
- a durability witness;
- placement/recovery machinery capable of resolving and decoding them.

That makes **availability an achieved technical relation**, not evidence of immateriality. The interpretation stops there. `.durable` is not a philosophical memory object, and Swift's object protocol is not automatically a case of Stieglerian tertiary retention or Heideggerian `Bestand`.

---

## Functional analogies

### With Case 23 — Dynamo

Both systems can temporarily contain multiple versions/copies and rely on repair metadata. But the bounded currentness regimes differ:

- Dynamo may intentionally return several causally unrelated current leaves for application reconciliation;
- Swift EC GET seeks one coherent **same-timestamp coded cohort** with durability evidence.

`distributed currentness` is therefore a useful functional comparison, not one shared historical algorithm.

### With Case 24 — Windows Azure Storage LRC

Both cases gate retirement of an older representation on a stronger completion relation. But Case 24 seals an immutable extent, produces a new coded representation asynchronously, validates it, then retires full replicas. Swift Case 25 handles **client-visible mutable object replacement under an EC policy**, where old/new timestamped coded state may coexist and read admissibility is version-qualified.

### With Cases 17 and 19 — RAID and f4

All use coded reconstruction. Swift adds a different currentness problem: surviving fragments must not only be sufficient; they must belong to one admissible timestamped version.

---

## Counterexamples and limits

- **Not a universal Swift consistency claim.** The source explicitly says the multi-phase mechanism is not the introduction of strong consistency semantics.
- **Not generic two-phase commit.** Swift says `essence of a 2 phase commit`; this case preserves that bounded wording.
- **Not invention priority.** Reed–Solomon and erasure coding predate Swift by decades; Cases 19 and 24 already retain that prior-art boundary.
- **Not one timeless Swift protocol.** The 2.3.0 and 2.10.1 commit thresholds differ and are intentionally reported separately.
- **Not a secure-deletion case.** Removal of older timestamp files is not physical sanitization.
- **Not a complete object-versioning history.** User-facing versioned-container modes, tombstone history, and later Swift EC-on-disk format changes are outside scope.
- **Not proof that any physically decodable cross-timestamp mixture would produce useful bytes.** The historical claim needed here is stronger and simpler: the implementation requires same-timestamp archives, so cross-version mixing is not an admissible GET set.
- **Not a statement about current Swift.** Later releases changed on-disk durability-marker representation and other implementation details; those require their own revision-specific case if relevant.

---

## Related repositories

A GitHub code search of `tmzncty/computing-archaeology` for a dedicated OpenStack Swift EC / fragment-currentness treatment returned no indexed dedicated result during this slice.

Routing remains:

- general OpenStack Swift architecture/history, coding-library genealogy, and storage-policy evolution → `computing-archaeology` if developed there;
- this bounded comparison of **mutable coded-version admissibility, commit markers, and safe old-version retirement** → `technical-retention`.

Case 19 and Case 24 are reused for coding-theory and immutable-coded-system comparisons rather than rebuilding their historical material here.

---

## Sources

### Primary

1. OpenStack Swift, signed tag **2.3.0**, tagger date 2015-04-30, commit `f8dee761bd36f857aa1288c27e095907032fad68`: <https://github.com/openstack/swift/tree/2.3.0>
2. OpenStack Swift 2.3.0, `CHANGELOG`, `swift (2.3.0)` entry: <https://github.com/openstack/swift/blob/2.3.0/CHANGELOG>
3. OpenStack Swift 2.3.0, `doc/source/overview_erasure_code.rst`: <https://github.com/openstack/swift/blob/2.3.0/doc/source/overview_erasure_code.rst>
4. OpenStack Swift **2.10.1**, `doc/source/overview_erasure_code.rst`: <https://github.com/openstack/swift/blob/2.10.1/doc/source/overview_erasure_code.rst>
5. OpenStack Swift 2.10.1 release commit `3129a55d4418e0dc4207c2026e7ef8c59704c6a1`, including the EC fragment-validation release-note change: <https://github.com/openstack/swift/commit/3129a55d4418e0dc4207c2026e7ef8c59704c6a1>

### Reused prior-art boundary

6. [`Case 19`](19-facebook-f4-erasure-coded-failure-domains.md) and its grounding record retain the Reed–Solomon/coding-theory priority boundary.
7. [`Case 24`](24-windows-azure-lrc-repair-locality-handoff.md) retains the LRC/Pyramid-code repair-locality and immutable redundancy-handoff boundary.
