# Evidence 110 deepening — NetApp SnapLock on-premises disk WORM, 2003 prior-art and retention-clock boundary

## Case

[`cases/110-amazon-s3-object-lock-version-worm-retention.md`](../cases/110-amazon-s3-object-lock-version-worm-retention.md)

## Evidence status

**Grounded for a bounded on-premises WORM prior-art and retention-control comparison.**

This pass adds **NetApp SnapLock** as a named pre-cloud WORM system. It is deliberately narrower than a history of compliant storage: the goal is to establish that software/controller-enforced WORM on ordinary disk-based network storage was publicly documented by 2003, then compare its retained file/clock/authority relations with the later cloud-object contracts already grounded in Case 110.

It does **not** claim that NetApp invented disk WORM, that SnapLock is the direct ancestor of S3 Object Lock, or that the current ONTAP implementation is unchanged from 2003.

Claim labels follow [`docs/METHOD.md`](../docs/METHOD.md):

- **H** — historical record;
- **P** — primary/provider evidence;
- **P\*** — provider documentation preserved on a non-origin mirror;
- **E** — engineering reconstruction from documented behavior;
- **A** — functional analogy/comparison;
- **I** — bounded philosophical interpretation;
- **X** — explicit exclusion / unsupported stronger claim.

## Sources

### P1 — Network Appliance FY2003 Form 10-K

Network Appliance, Inc., **Form 10-K for the fiscal year ended 25 April 2003**, filed with the U.S. Securities and Exchange Commission.

<https://www.sec.gov/Archives/edgar/data/1002047/000089161803003272/f91038e10vk.htm>

The filing says **SnapLock was introduced during fiscal year 2003** and describes it as meeting regulatory `data permanence` requirements by providing WORM attributes, including nonerasability and nonrewritability, for data stored on NearStore. The same filing describes NearStore as disk-based nearline storage.

Evidence strength: **strong period, company-authored public filing**.

Chronology limit: this establishes introduction no later than the fiscal year ending 25 April 2003. It does not by itself establish an exact public-launch day or invention priority.

### P2 — Network Appliance FY2004 Q2 Form 10-Q

Network Appliance, Inc., **Form 10-Q for the quarter / six months ended 31 October 2003**.

<https://www.sec.gov/Archives/edgar/data/1002047/000089161803006173/f94954e10vq.htm>

The filing says SnapLock Compliance and SnapLock Enterprise were then available on NetApp FAS servers **in addition to the NearStore platform**, and distinguishes the regulated-data purpose of Compliance from the broader data-integrity/governance purpose of Enterprise.

Evidence strength: **strong period, company-authored public filing**.

This later-2003 record is used to establish product/mode availability, not to rewrite the exact feature set of the earlier fiscal-2003 introduction.

### P*3 — Data ONTAP 7-era NetApp documentation preserved by University of Wollongong

NetApp documentation mirror, **“What SnapLock is”** and **“What the ComplianceClock is.”**

<https://documents.uow.edu.au/~blane/netapp/ontap/archive/complying/concept/c_oc_cmpl_snplk-what-is.html>

<https://documents.uow.edu.au/~blane/netapp/ontap/archive/complying/concept/c_oc_cmpl_snplk-comlplianceclock-what-is.html>

The preserved vendor documentation describes SnapLock as a **license-based, disk-based, open-protocol** feature that provides storage-enforced WORM and retention over CIFS/NFS at individual-file granularity. It also states that SnapLock is a persistent property of SnapLock volumes/files and remains enforced regardless of licensing state. The companion ComplianceClock page describes a secure software time base, replicated/retained in system/volume-related state, used so ordinary system-clock changes cannot prematurely release compliant data.

Evidence strength: **useful provider-text historical witness, but not origin-hosted**. The mirror appears to preserve Data ONTAP 7-generation documentation. It is therefore not used as proof that every listed detail existed in the April-2003 release.

### P4 — current ONTAP SnapLock overview, 16 June 2026

NetApp, **“Learn about ONTAP SnapLock,”** updated 16 June 2026.

<https://docs.netapp.com/us-en/ontap/snaplock/>

Current documentation states that SnapLock creates special-purpose volumes in which files can be committed to non-erasable, non-writable WORM state for a defined period or indefinitely, at file level over NFS/CIFS. It distinguishes **Compliance** and **Enterprise** modes: current Compliance does not permit deletion of retained WORM files, while current Enterprise permits an audited privileged-delete path. It also states that, after retention expires, the operator remains responsible for deleting files no longer required, and that a file committed to WORM cannot be modified even after expiry.

Evidence strength: **strong current provider contract**, not a frozen 2003 witness.

### P5 — current retention-time contract, 16 June 2026

NetApp, **“Set the ONTAP SnapLock retention time,”** updated 16 June 2026.

<https://docs.netapp.com/us-en/ontap/snaplock/set-retention-period-task.html>

Current documentation distinguishes a **retention period** (duration after WORM commit) from a **retention time** (the absolute time after which the file no longer needs to be retained). It states that after a file is committed to WORM the retention period/time may be extended but not shortened, and that an explicitly set file retention time is stored in the file's `atime` field.

Evidence strength: **strong current provider contract**.

### P6 — current Compliance Clock contract, 16 April 2026

NetApp, **“Initialize the ONTAP Compliance Clock,”** updated 16 April 2026.

<https://docs.netapp.com/us-en/ontap/snaplock/initialize-complianceclock-task.html>

Current documentation states that the volume Compliance Clock controls WORM-file retention periods and inherits its initial time from a system Compliance Clock. It also records an important version boundary: in ONTAP 9.13.1 and earlier the node clock could not be reinitialized after initialization; beginning with ONTAP 9.14.1 reinitialization is allowed only under restrictive conditions, including the absence of SnapLock volumes and locked-snapshot state.

Evidence strength: **strong current provider contract and explicit version boundary**.

## Historical record

### H/P — a named disk-based WORM system was public by fiscal 2003

P1 is a contemporary corporate filing, not a later retrospective. It says SnapLock was introduced during fiscal year 2003 and supplied WORM nonerasability/nonrewritability for data on NearStore. Because that fiscal year ended **25 April 2003**, the safe lower bound is:

```text
NetApp SnapLock public/product history by FY ended 25 Apr 2003
    <<
Azure / GCS / S3 public cloud-WORM launches in 2018
```

This materially narrows Case 110's prior-art boundary. The cloud services did not invent the general idea of enforcing WORM semantics through a managed storage system built on rewritable disks.

The evidence does **not** establish that SnapLock was first. Other compliant-storage products, including content-addressed systems, require their own chronology if invention or market priority ever matters.

### H/P — late-2003 SnapLock already had multiple policy/authority modes

P2 records both SnapLock Compliance and SnapLock Enterprise as available on FAS as well as NearStore by the quarter ended 31 October 2003. That demonstrates that `WORM` was already a family of authority contracts in this product line rather than one undifferentiated bit-level property.

The exact later/current semantics of those two modes are not projected backward wholesale into the fiscal-2003 introduction.

### H/P* — later Data ONTAP 7 documentation explicitly called SnapLock disk-based and open-protocol

P*3 is useful because it states the architectural claim directly: SnapLock is described as disk-based and enforced through Data ONTAP while clients use ordinary CIFS/NFS file protocols. That is a closer functional prior art to cloud policy WORM than ECMA-153 optical WORM, because the carrier need not itself be a physically write-once optical medium.

The mirror's provenance is weaker than P1/P2, so it supports mechanism continuity rather than exact 2003 launch wording.

## Engineering reconstruction

### E1 — rewrite-capable substrate != rewrite-authorized retained object

The period record and later product documentation together show a WORM relation implemented on disk-based network storage. The retention property therefore cannot be reduced to `the medium is physically incapable of another write`.

For the bounded SnapLock system, at least these layers are separable:

```text
physical disk/SSD embodiment
    !=
file identity and WORM state
    !=
retention deadline
    !=
clock used to judge expiry
    !=
authority allowed to delete
```

This is the on-premises counterpart to Case 110's existing rule `service-level WORM != physically write-once medium`.

### E2 — file-level WORM != object-version WORM

SnapLock's documented protected identity is a file in a SnapLock volume, exposed through file protocols. S3 Object Lock protects a specific S3 object version; GCS 2018 Bucket Lock applied a bucket policy; Azure's 2018 witness was container-scoped.

Thus a shared `WORM` category does not define one universal retained object:

```text
same WORM vocabulary
    !=
same identity granularity
    !=
same currentness/version relation
```

### E3 — a retention deadline needs an admissible reference clock

P*3/P6 expose the time source as explicit retained control infrastructure. A file's deadline is not self-executing: deletion admission depends on comparing retained retention state against a clock that the storage system treats as authoritative.

Therefore:

```text
retention timestamp exists
    !=
ordinary wall/system clock may redefine expiry at will
```

The engineering point is not that ComplianceClock is unique. It is that time-based retention contains a hidden **time-authority relation** in addition to the payload and deadline value.

### E4 — retention time stored in `atime` != access-history retention

P5 says current ONTAP stores an explicitly set retention time in the file's `atime` field. That means the same conventional metadata slot can carry a SnapLock-specific future-admission meaning.

This supports a narrow distinction:

```text
field name / conventional metadata role
    !=
semantic role under a retention regime
```

It does not imply that current ONTAP preserves a complete access history; in this path, `atime` is evidence about a future retention boundary.

### E5 — retention expiry != deletion, and expiry != restored mutability

P4 says that after retention expires the operator is responsible for deleting files no longer needed. It separately says a file committed to WORM cannot be modified even after the retention period has expired.

Thus current SnapLock gives a particularly useful decomposition:

```text
retention obligation satisfied
    !=
file deleted
    !=
ordinary in-place mutability restored
    !=
physical sanitization
```

This is not identical to the lifecycle/currentness behavior of S3, GCS, or Azure.

### E6 — protection lifetime can outlive licensing/capability-admission state

P*3 says existing SnapLock volume/file WORM properties remain enforced even if the SnapLock license is removed; licensing is needed for creating new protected volumes/commits rather than for dissolving already established protection.

So, for that documented Data ONTAP generation:

```text
ability to create new WORM state
    !=
continued enforcement of existing WORM state
```

A capability-control relation and an already-committed retention relation can have different lifetimes.

### E7 — retention-rule mutability != retention duration

P5 says a committed file's retention period/time can be extended but not shortened. The retained rule therefore has both a value and an authority relation governing which direction that value may move.

This is functionally comparable to locked cloud retention policies but does not imply identical implementation or legal semantics.

## Cross-provider comparison

| Relation | NetApp SnapLock | Azure/GCS/S3 Case-110 cloud evidence |
| --- | --- | --- |
| dated public floor used here | FY ended 25-Apr-2003 | 2018 provider launches |
| carrier/service class | on-premises managed disk storage | hyperscale cloud object/blob storage |
| protected identity established here | file in SnapLock volume | container/bucket/object-version depending provider/date |
| WORM enforced by managed control state | yes | yes at service-contract layer |
| physical write-once carrier required by evidence | no | no |
| explicit retained time-authority apparatus exposed | ComplianceClock | provider clocks are implicit; retain-until/policy state is exposed |
| expiry itself deletes payload | no | no in the bounded contracts |
| authority modes have identical semantics | no | no |

### A — `Compliance` and `Enterprise/Governance` labels are false friends unless mechanism is checked

NetApp and AWS both use `Compliance`, while NetApp's looser mode is called `Enterprise` and S3's is `Governance`. Similar mode names/functions are useful comparison prompts, not a translation table.

Current NetApp Enterprise uses an audited privileged-delete path; S3 Governance uses its own permission plus explicit bypass contract. Their scope, identity, clock, request, and audit semantics are separately defined.

Therefore:

```text
SnapLock Compliance != S3 Compliance by name alone
SnapLock Enterprise != S3 Governance by function alone
```

No implementation genealogy is inferred.

### A — on-premises WORM prior art != cloud-WORM genealogy

The safe historical conclusion is only chronological and functional:

> managed storage could impose WORM retention on rewritable disk-based storage at least by NetApp's fiscal 2003 SnapLock product generation, long before the 2018 cloud services in Case 110.

That does not show that Azure, Google, or AWS copied SnapLock, inherited its data structures, or adopted its ComplianceClock design.

## Philosophical interpretation — bounded

### I — time-based retention retains a rule about future admissibility, not only a payload

The technical fact is concrete: current SnapLock keeps a file WORM state, retention time, and an authoritative Compliance Clock relation that together determine when deletion can become admissible.

A narrow interpretation is:

> a technically retained object can include a retained constraint on **when a future operation is allowed to count as legitimate**, and that constraint itself depends on maintained control state.

The limit is equally important. ComplianceClock is not `time itself`, policy is not a physical force, and this file-level control state is not automatically Stieglerian tertiary retention or Heideggerian `Bestand`.

## Anti-anachronism and negative claims

This deepening does **not** establish:

- an exact calendar-day SnapLock launch before 25 April 2003;
- that SnapLock was the first disk-based or software-enforced WORM product;
- a NetApp -> Azure/GCS/AWS genealogy;
- that current ONTAP SnapLock semantics were all present in the initial fiscal-2003 product;
- that Data ONTAP 7-era mirrored documentation is an origin-hosted facsimile;
- that current `Compliance` / `Enterprise` semantics exactly equal the 2003 modes;
- that `atime` is a universal retention-metadata field outside current SnapLock;
- that ComplianceClock has had one unchanged initialization/synchronization contract across releases;
- that `disk-level` protection in current NetApp vocabulary means the magnetic/Flash medium is physically write-once;
- that expiry, privileged deletion, file unlink, block reclamation, key retirement, or media sanitization are one event;
- regulatory or legal sufficiency for any particular deployment.

P6 explicitly blocks one especially easy backward projection: ONTAP 9.14.1 changed ComplianceClock reinitialization possibilities under restricted no-protected-state conditions. Current clock-management semantics therefore must be versioned rather than treated as timeless SnapLock essence.

## Related-repository boundary

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated `SnapLock` case to reuse. If broader compliant-storage history is developed — EMC Centera, optical-to-disk WORM migration, WAFL/ONTAP implementation, regulation-driven product design, or exact release genealogy — it belongs primarily there.

`technical-retention` keeps only the bounded relation needed here:

> **rewritable disk embodiment + retained WORM state + retention deadline + authoritative clock + deletion authority can make a file operationally non-rewritable/non-erasable without turning the underlying medium into a physically write-once carrier.**

## Readiness

This on-premises prior-art slice is complete enough to integrate into grounded Case 110 because it has:

- a period first-party SEC filing establishing SnapLock introduction and WORM purpose by fiscal 2003;
- an independent later-2003 first-party filing establishing Compliance/Enterprise product availability;
- preserved vendor documentation exposing the disk/open-protocol/file/ComplianceClock mechanism, with mirror provenance labeled rather than hidden;
- current first-party documentation exposing present retention-time, expiry, mode, and clock semantics with explicit version boundaries;
- negative claims preventing priority, genealogy, physical-WORM, sanitization, and current-to-2003 back-projection.

Remaining work should be separate slices: exact 2003 product-release/ONTAP revision archaeology, EMC Centera and other disk-WORM chronology, regulation/certification history, internal WAFL retention implementation, lower-layer deletion/sanitization, and fault/clock-manipulation validation.
