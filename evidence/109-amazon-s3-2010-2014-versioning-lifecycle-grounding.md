# Evidence 109 — Amazon S3 2010–2014 Versioning / Lifecycle Grounding

## Purpose

This record grounds [`../cases/109-amazon-s3-versioning-delete-marker-lifecycle.md`](../cases/109-amazon-s3-versioning-delete-marker-lifecycle.md).

The bounded question is:

> How does Amazon S3 separate the default current view of a versioned key from retained predecessor versions, and how do delete markers plus later lifecycle rules make negative currentness and historical-version reclamation distinct service states?

It does not attempt to reconstruct undisclosed S3 replica topology or physical-media behavior.

## Status

**`grounded`** for the bounded service-contract relation.

The strongest historical anchors are first-party AWS records from **8 February 2010**, **16 March 2010**, and **20 May 2014**. Current AWS API/User Guide pages are used as later first-party contract evidence and are explicitly not projected backward as unchanged historical wording.

## Source hierarchy

### P1 — AWS News Blog, 8 February 2010

**“New Feature: Amazon S3 now supports Object Versioning.”**

<https://aws.amazon.com/blogs/aws/amazon-s3-enhancement-versioning/>

Supports:

- beta Versioning across all S3 Regions;
- PUT/POST/COPY/DELETE retain old versions;
- each version has a version ID;
- default GET returns the most recent version;
- version-aware GET can retrieve former versions;
- DELETE changes default retrieval while the prior version remains preserved;
- permanent deletion of one version is separately authorized.

Use as a **period first-party service record**.

Do not use it as an invention-priority claim.

### P2 — AWS News Blog, 16 March 2010

**“Amazon S3 Versioning Is Now Ready.”**

<https://aws.amazon.com/blogs/aws/amazon-s3-versioning-now-ready/>

Supports:

- production-status announcement;
- old versions continue to exist and remain accessible.

Use to distinguish the February beta floor from March production status.

### P3 — AWS, 20 May 2014

**“Amazon S3 Now Supports Lifecycle Rules for Versioning.”**

<https://aws.amazon.com/about-aws/whats-new/2014/05/20/amazon-s3-now-supports-lifecycle-rules-for-versioning/>

Supports:

- lifecycle rules extended to versioned buckets;
- previous versions can be transitioned and later deleted;
- AWS's example uses a 100-day rollback window.

Use as the bounded historical floor for combining Versioning with lifecycle-managed predecessor retirement.

### P4 — current `DeleteObject` API reference

<https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteObject.html>

Supports current contract:

- unqualified DELETE in a versioning-enabled bucket inserts a delete marker;
- the marker becomes current;
- deletion with `versionId` permanently deletes the selected version.

This is **later first-party contract evidence**, not exact 2010 wording.

### P5 — current “How S3 Versioning works”

<https://docs.aws.amazon.com/AmazonS3/latest/userguide/versioning-workflows.html>

Supports current contract:

- current delete marker makes default GET return 404;
- noncurrent version remains GET-able by version ID;
- selected version can be permanently deleted.

### P6 — current “Working with delete markers”

<https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeleteMarker.html>

Supports:

- delete marker is a placeholder/versioned negative state rather than data-bearing payload;
- marker has key/version identity and no payload data.

### P7 — current “Managing delete markers”

<https://docs.aws.amazon.com/AmazonS3/latest/userguide/ManagingDelMarkers.html>

Supports:

- deleting the current marker by version ID can make an older payload current again;
- ordinary DELETE against a current marker does not remove that marker and can add another marker.

### P8 — current lifecycle elements

<https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html>

Supports:

- separate expired-delete-marker cleanup;
- a version's noncurrent age is calculated from successor creation;
- current/noncurrent are separate lifecycle classes.

Do not project later lifecycle options/version-count features back to 2014.

### P9 — current “Deleting object versions…”

<https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeletingObjectVersions.html>

Supports:

- `Expiration` applies to current version and in versioning-enabled buckets can create a delete marker while retaining the prior payload as noncurrent;
- `NoncurrentVersionExpiration` applies to noncurrent versions and removes those versions at the service layer.

## Claim matrix

| Claim | Evidence | Type | Boundary |
| --- | --- | --- | --- |
| Versioning publicly available in beta by 2010-02-08 | P1 | H/P | public service floor, not invention date |
| Production status by 2010-03-16 | P2 | H/P | status change, not first implementation |
| former versions remain version-addressable | P1, P2, P5 | H/P | service recoverability, not physical location |
| ordinary versioned DELETE yields negative current view while predecessor survives | P1 + later exact marker wording P4/P5 | H/P | do not project every current detail to 2010 |
| delete marker is a versioned negative placeholder | P4–P7 | H/P later contract | not physical erasure |
| version-specific DELETE differs from marker insertion | P4, P5 | H/P later contract | service deletion ≠ media sanitization |
| lifecycle/versioning combination exists by 2014-05-20 | P3 | H/P | no claim every current lifecycle option existed then |
| current and noncurrent lifecycle retirement are distinct | P8, P9 | H/P later contract | service classes, not implementation topology |
| noncurrent age begins at supersession/successor creation | P8 | H/P later contract | not original object age |
| marker cleanup differs from predecessor-version cleanup | P8, P9 | H/P later contract | distinct retained-state classes |
| default-current visibility ≠ complete retained history | P1, P4, P5 | E | project reconstruction |
| service-level permanent delete ≠ physical sanitization | source-boundary inference | E/X | physical internals not disclosed |
| S3 marker ≠ Swift `.ts` tombstone implementation | Case 28 + P4–P7 | A/X | functional analogy only |

## Historical boundary

The defensible chronology is narrow:

```text
8 Feb 2010
    public beta Versioning record
        -> retained predecessor versions + version IDs + default/version-aware retrieval

16 Mar 2010
    production-status announcement

20 May 2014
    lifecycle support explicitly combined with versioned buckets

current documentation
    exact current delete-marker / version-specific-delete / lifecycle decomposition
```

Do **not** convert that into:

```text
2010 invented multi-version storage
2010 invented tombstones
2014 invented lifecycle retention
```

No such priority conclusion follows.

## Mechanism boundary

The public evidence establishes a service state machine, not storage internals.

Grounded:

```text
logical key
    -> current version selection
    -> versionId-addressable predecessors
    -> current delete marker possible
    -> later policy/version-specific retirement
```

Not grounded:

```text
logical key
    -> exact replica set
    -> exact coding layout
    -> exact disk/SSD block
    -> exact physical erase time
```

This distinction is central to the case.

## Functional-comparison boundary

### With Swift Case 28

Safe:

- both cases can retain a negative state while older positive state may still exist;
- both separate logical/current deletion from later retirement.

Unsafe:

- importing Swift `.ts` files, timestamp ordering, asynchronous replica convergence, or `reclaim_age` into S3;
- inferring a shared genealogy.

### With GFS Case 73

Safe:

- current namespace/object retirement can precede later physical/logical reclamation.

Unsafe:

- equating GFS master/chunk scanning and S3 lifecycle machinery.

### With ZFS Case 99

Safe:

- older logical state may remain deliberately recoverable after a newer current state exists.

Unsafe:

- equating block-reference pinning with S3 version IDs.

## Related-repository check

A repository search for S3 Versioning / delete-marker / lifecycle terminology in `tmzncty/computing-archaeology` returned no existing focused treatment at the time of this slice.

Therefore this case does not duplicate a known companion-repository technical history. If a broader S3 architecture history is later developed, that history should live primarily there, while `technical-retention` keeps the current/noncurrent/history-retirement comparison.

## Rejected stronger claims

| Stronger claim | Status | Reason |
| --- | --- | --- |
| Amazon invented object versioning in 2010 | rejected | launch date ≠ invention priority |
| current AWS docs are exact 2010/2014 contract text | rejected | later documentation contains later-evolved semantics/options |
| delete marker means previous bytes are erased | rejected | marker changes current service state |
| noncurrent version is corrupt or invalid | rejected | it remains explicitly retrievable |
| version ID reveals physical location | rejected | it is a service selector |
| “permanent delete” proves media sanitization | rejected | public service contract does not expose lower-layer erase evidence |
| S3 uses Swift-style replica tombstones | rejected | no implementation evidence |
| Versioning is equivalent to Object Lock/WORM | rejected | distinct service mechanisms |

## Remaining evidence gaps

- archival developer-guide/API snapshots for exact 2010 delete-marker terminology;
- exact May-2014 lifecycle API syntax and rule options from contemporaneous documentation;
- provider-independent measurement of version deletion behavior;
- internal replication/currentness protocol, if ever supported by public engineering evidence;
- lower-layer media reclamation/sanitization evidence;
- Object Lock/legal-hold comparison as a separate bounded case;
- cross-region replication/version-deletion interactions as a separate bounded case.

These gaps do not block the bounded service-contract claim.
