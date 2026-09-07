# Amazon S3 Versioning: Delete Markers, Noncurrent Versions, and Lifecycle Reclamation

## Status

**`grounded`** for the bounded service-contract relation described below.

## Scope

- **Object / system:** Amazon S3 general-purpose buckets with Versioning enabled.
- **Historical anchors:** public beta announcement on 8 February 2010; production-status announcement on 16 March 2010; lifecycle support for versioned buckets announced on 20 May 2014.
- **Later contract evidence:** current AWS API and User Guide documentation is used only to clarify the presently documented semantics of delete markers, version-specific deletion, and lifecycle actions. It is not silently projected backward as exact 2010/2014 implementation wording.
- **Research question:** how can the default current view of an object disappear while earlier payload versions remain explicitly recoverable, and how is later reclamation of those retained versions authorized?

This is **not** a history of Amazon S3 internals, replication topology, physical media erasure, Object Lock, cross-region replication, or cloud storage generally. The public service contract does not disclose enough to infer which physical copies survive or when underlying media are sanitized.

The bounded retention claim is:

> **With S3 Versioning enabled, a key can cease to return its previous payload by default without that predecessor ceasing to exist as a retrievable version. An ordinary DELETE creates a data-less delete marker that becomes current, while older versions remain addressable by version ID; version-specific deletion and lifecycle rules can later retire those retained versions separately.**

`currentness`, `negative current state`, `retained predecessor`, and `reclamation authority` are project engineering terms unless explicitly attributed to AWS.

## Historical vocabulary

AWS sources use:

- `Versioning`;
- `version`;
- `version ID` / `versionId`;
- `current version`;
- `noncurrent version`;
- `delete marker`;
- `DELETE`;
- `Expiration`;
- `NoncurrentVersionExpiration`;
- `ExpiredObjectDeleteMarker`;
- `Lifecycle`.

The following are project terms, not AWS historical vocabulary:

- `negative current state`;
- `retained predecessor`;
- `default-view currentness`;
- `reclamation authority`;
- `history-retention layer`.

## Historical record

### H/P — 8 February 2010: Versioning is publicly available in beta

AWS announced beta Versioning across all Amazon S3 Regions on **8 February 2010**. The announcement states that operations which would overwrite or delete an object retain the old version, that each version receives a version ID, and that a version-aware request can retrieve an earlier version by that ID.

This establishes a strong public service-contract floor no later than that date. It does **not** establish invention priority, first internal implementation, or the exact implementation mechanisms behind the service.

Primary anchor: AWS News Blog, **“New Feature: Amazon S3 now supports Object Versioning,”** 8 February 2010.

### H/P — the original launch already separates default retrieval from version-aware retrieval

The same launch record says that a default GET retrieves the most recent version, whereas an explicit version-aware request can retrieve a current or former version.

Therefore the service contract already distinguishes:

```text
what the key returns by default
    ≠
which retained versions can still be named explicitly
```

This is a historical service distinction, not a reconstruction from modern object-store terminology.

### H/P — the original launch already makes DELETE compatible with predecessor retention

The February 2010 announcement says that after DELETE, subsequent default requests no longer retrieve the object, while the previous version remains preserved and retrievable by version ID. It also distinguishes ordinary deletion from permanent deletion of a version.

This blocks the shortcut:

```text
DELETE visible at the default key
    -> all earlier payload embodiments are gone
```

The public contract instead establishes a retained version history behind the changed default view.

### H/P — 16 March 2010 marks production status, not invention

AWS announced on **16 March 2010** that Versioning had “graduated to production status,” again stating that old versions continue to exist and remain accessible.

The chronology should therefore be stated conservatively:

- 8 February 2010 — public beta availability;
- 16 March 2010 — production-status announcement.

Neither date is evidence that AWS invented object versioning, multi-version storage, tombstones, or retention policies.

### H/P — current API documentation names the delete-marker operation explicitly

The current `DeleteObject` API documentation states that when Versioning is enabled, a DELETE without a `versionId` inserts a **delete marker** which becomes the current version. A request that includes a specific `versionId` permanently deletes that version.

This later documentation supplies exact present-day service vocabulary for a relation that the February 2010 launch already described functionally.

It must not be used to claim that every present field, permission rule, or implementation detail existed unchanged in February 2010.

### H/P — current GET semantics make currentness and recoverability visibly different

Current AWS documentation states that when the current version is a delete marker, a default `GET Object` returns `404 Not Found`. The same documentation states that a noncurrent payload version can still be retrieved by specifying its version ID.

Thus:

```text
default GET says “not found”
    ≠
no historical payload version remains retrievable
```

The distinction is directly service-visible.

### H/P — the delete marker is not a data-bearing replacement object

AWS describes a delete marker as a placeholder associated with the key and a version ID, without payload data. It changes which version is current rather than replacing the earlier object bytes with another data-bearing version.

Deleting the current delete marker by its version ID can make the previous payload version current again.

The service can therefore reverse the default negative view without rewriting that predecessor payload.

### H/P — 20 May 2014: lifecycle rules are explicitly combined with Versioning

On **20 May 2014**, AWS announced lifecycle-rule support for versioned buckets. The announcement says Versioning preserves previous versions, while lifecycle rules can transition or delete those previous versions after configured time periods; its example keeps a 100-day rollback window.

This is a useful historical boundary because history retention is no longer only a manually managed consequence of versioning. The service exposes policy-driven retirement of retained predecessor versions.

### H/P — current lifecycle documentation separates current, noncurrent, and marker cleanup

Current AWS documentation distinguishes at least three relevant lifecycle relations:

1. `Expiration` acts on the **current** version; in a versioning-enabled bucket it can add a delete marker and make the former current payload noncurrent.
2. `NoncurrentVersionExpiration` acts on **noncurrent** object versions and permanently removes them at the service layer.
3. `ExpiredObjectDeleteMarker` cleanup can remove a delete marker after it is the only remaining version.

The same documentation calculates a version's noncurrent age from the creation time of its successor, not simply from the original object's creation time.

These current semantics are used as a later contract decomposition, not as proof that every option or exact rule existed in 2014.

## Retained state

The bounded case requires several distinct retained relations.

### 1. Logical key

The bucket/key designation remains the ordinary object name even as different versions become current.

### 2. Version identity

Each retained version has a `versionId` that allows explicit selection independently of whether that version is current.

### 3. Payload version

A predecessor object version can remain retrievable after a later PUT or DELETE changes the default current view.

### 4. Current/noncurrent relation

One version is selected as current for ordinary key access, while older versions are noncurrent but may remain retained.

### 5. Delete-marker version

A delete marker is itself a versioned service state. Its meaning is negative for default access, but it is not itself the previous payload.

### 6. Lifecycle policy state

Lifecycle configuration determines when classes of retained versions or markers become eligible for later service-level deletion.

These relations demonstrate that `object exists` is too coarse a state variable for a versioned object service.

## Physical / logical substrate

At the public interface, the relevant substrate is logical and service-managed:

```text
bucket + key
    -> ordered/versioned object history
        -> one current version
        -> zero or more noncurrent versions
        -> optional current delete marker
        -> lifecycle policy
```

The public sources used here do not establish:

- physical device location;
- internal replica count;
- erasure-code layout;
- replica-currentness protocol;
- media-block reclamation timing;
- sanitization completion.

Those belong to a different evidence layer.

## Retention mechanism

### Ordinary overwrite

A newly written version becomes current; the predecessor can remain as a noncurrent version.

### Ordinary DELETE

The default view becomes negative through insertion of a delete marker. Older payload versions can remain separately addressable.

### Explicit historical recovery

A client can name a noncurrent version by version ID and retrieve it even when it is not the default current version.

### Marker removal

Deleting the current delete marker by its version ID removes that negative current layer and can expose the predecessor as current again.

### Lifecycle retirement

Lifecycle rules can later make noncurrent versions or expired delete markers eligible for service-level removal.

The same logical key can therefore pass through several currentness and retention states without implying one simultaneous physical erase event.

## Addressing and access geometry

A simplified service relation is:

```text
bucket/key
    -> default GET
        -> current version
            -> payload
            -> or delete marker => 404

bucket/key + versionId
    -> explicitly selected version
        -> retained historical payload or marker
```

This is an addressing distinction, not evidence about physical layout.

A version ID is a service-level selector. It must not be reinterpreted as a storage address.

## Read semantics

A default read is currentness-sensitive. It does not ask, “does any version of this payload still exist?” It asks for the current version under ordinary key access.

Consequently:

```text
default GET failure due to current delete marker
    ≠
historical-version retrieval failure
```

An explicit version-aware GET can recover a retained predecessor.

Read does not, in the bounded public contract, imply restoration, rewriting, or physical refresh of that version.

## Write and erasure semantics

Keep at least four operations distinct:

1. **new version creation** — a new payload becomes current and the predecessor becomes noncurrent;
2. **ordinary DELETE** — insert a current delete marker;
3. **version-specific DELETE** — remove one selected version from the service;
4. **lifecycle retirement** — policy-driven expiration/removal of selected version classes.

None of these service-level operations, by itself, proves physical media sanitization.

Especially:

```text
delete marker insertion
    ≠ payload overwrite
    ≠ noncurrent-version deletion
    ≠ physical-sector/block sanitization
```

## Time

Relevant timescales include:

- request completion for PUT/DELETE/GET;
- how long a predecessor remains noncurrent but retrievable;
- time since a version became noncurrent;
- lifecycle transition/expiration windows;
- later provider-internal reclamation, which the bounded public sources do not expose.

The current lifecycle rule that measures noncurrent age from the creation of a successor is particularly useful: **history-retention time can begin at supersession, not at original creation**.

## Maintenance and labor

Versioned retention is not passive “extra copies exist” storage. The service must sustain:

- version identifiers;
- current/noncurrent classification;
- default-versus-version-aware lookup;
- delete-marker interpretation;
- lifecycle evaluation;
- authorization for permanent version deletion;
- billing/capacity consequences of retained predecessors;
- operator choices about lifecycle windows.

This is service-level maintenance. No claim is made here about AWS's undisclosed lower-level repair or media-management mechanisms.

## Failure / forgetting modes

Keep separate:

- accidental overwrite without sufficient version retention;
- accidental ordinary DELETE, recoverable while the predecessor remains;
- intentional or accidental deletion of a specific version;
- deletion of a current delete marker, which can re-expose an older predecessor;
- lifecycle policy that retires versions earlier than intended;
- failure to retain or know a needed version ID;
- permission/configuration errors affecting version deletion;
- physical storage failure beneath the service contract;
- secure-erasure/sanitization failure, which this case does not test.

The service-level state machine and the physical media lifecycle are different failure domains.

## Engineering reconstruction

### E — currentness is not uniqueness of retained state

The ordinary key view identifies one current answer while older valid payload versions may remain directly retrievable.

So:

> **current version ≠ only retained version**

### E — negative currentness can coexist with positive history

A delete marker makes the default current answer negative while predecessor versions remain selectable.

So:

> **current absence ≠ historical absence**

This is a stronger technical statement than the vague claim that “cloud deletion is delayed.” The negative current state and the retained positive history are separately addressable service relations.

### E — noncurrentness is not corruption

A noncurrent object version can be entirely valid and intentionally retained. It is excluded from the default view because a successor exists, not because its payload failed integrity qualification.

### E — lifecycle adds policy-governed forgetting to version history

Versioning creates a service-level history relation; lifecycle policy can later reduce that retained history.

The transition is not:

```text
object present -> object absent
```

but may instead be:

```text
payload v1 current
    -> payload v2 current / v1 noncurrent
    -> delete marker current / v2 + v1 noncurrent
    -> selected noncurrent versions retired
    -> expired marker retired
```

Different states carry different recovery possibilities.

### E — “permanently delete” is bounded to the service contract

AWS uses “permanently delete” for version-specific and lifecycle removal. Within this case, that means the version is no longer retained as an S3 object version through the ordinary service contract.

It does **not** establish cryptographic erasure, media overwrite, NAND block erasure, or absence of provider-internal traces.

## Philosophical / media-theoretical interpretation

The exact technical problem is:

> **A service can make an object absent in the present tense while preserving an explicitly addressable past tense.**

That makes technical forgetting less like instantaneous disappearance and more like a change in admissibility plus an optional later retirement of history.

The conceptual value is limited but useful: “the present object” is not identical to the set of all retained embodiments or versions that remain technically recoverable.

This does not make S3 Versioning equivalent to human memory, an archive in the institutional sense, or Stieglerian tertiary retention by definition. The case only supplies a precise mechanism against which broader claims about technical pastness can be tested.

## Functional analogies

### A — Swift tombstone comparison

[Case 28](28-openstack-swift-tombstone-consistency-window.md) also retains a negative state while older positive state may survive.

The analogy is deliberately bounded:

- Swift 2.10.1 exposes implementation-level `.ts` tombstones, timestamps, asynchronous replication, and `reclaim_age`;
- S3 here is grounded at the public service-contract level through version IDs, delete markers, and lifecycle rules;
- this case does **not** import Swift's consistency-window or replica-convergence mechanism into S3;
- no historical genealogy is claimed.

### A — GFS lazy garbage collection

[Case 73](73-gfs-lazy-garbage-collection.md) separates namespace deletion from later replica reclamation. S3 Versioning likewise separates a current visibility transition from later retirement of older retained state.

The triggers, data model, replication machinery, and historical systems differ.

### A — ZFS snapshot/reference-pinned history

[Case 99](99-zfs-snapshot-reference-pinned-retention.md) retains older filesystem state through snapshot references; S3 Versioning retains older object versions through service-managed version identity.

This is a functional comparison about historical-state admissibility, not a shared implementation.

## Counterexamples and limits

This case does **not** establish:

- that Amazon invented object versioning;
- that Versioning is an immutable/WORM retention mechanism;
- that a delete marker physically overwrites or erases older data;
- that a version ID reveals a physical location;
- that current AWS lifecycle syntax existed unchanged in 2014;
- that all internal replicas retain exactly the same version history at every instant;
- that a service-level permanent delete proves lower-level sanitization;
- that S3 delete markers implement Swift-style tombstone replication;
- that Object Lock, legal hold, replication, backup, or archival tiers are semantically identical to Versioning.

## Related repositories

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no existing S3 Versioning/delete-marker/lifecycle treatment to reuse. This case therefore keeps the contribution retention-specific rather than opening a generic Amazon S3 architecture history.

Broader cloud-storage engineering history, if developed, belongs primarily in `computing-archaeology`. Anti-anachronism follows `problem-history`: 2010 AWS vocabulary should not be replaced by later generic database terminology without labels.

## Sources

Primary / first-party anchors:

1. AWS News Blog, **“New Feature: Amazon S3 now supports Object Versioning,”** 8 February 2010: <https://aws.amazon.com/blogs/aws/amazon-s3-enhancement-versioning/>
2. AWS News Blog, **“Amazon S3 Versioning Is Now Ready,”** 16 March 2010: <https://aws.amazon.com/blogs/aws/amazon-s3-versioning-now-ready/>
3. AWS, **“Amazon S3 Now Supports Lifecycle Rules for Versioning,”** 20 May 2014: <https://aws.amazon.com/about-aws/whats-new/2014/05/20/amazon-s3-now-supports-lifecycle-rules-for-versioning/>
4. Amazon S3 API Reference, **`DeleteObject`**: <https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteObject.html>
5. Amazon S3 User Guide, **“How S3 Versioning works”**: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/versioning-workflows.html>
6. Amazon S3 User Guide, **“Working with delete markers”**: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeleteMarker.html>
7. Amazon S3 User Guide, **“Managing delete markers”**: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/ManagingDelMarkers.html>
8. Amazon S3 User Guide, **“Lifecycle configuration elements”**: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html>
9. Amazon S3 User Guide, **“Deleting object versions from a versioning-enabled bucket”**: <https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeletingObjectVersions.html>
