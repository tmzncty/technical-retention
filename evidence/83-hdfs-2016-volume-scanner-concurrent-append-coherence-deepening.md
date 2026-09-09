# Case 83 deepening — HDFS-11160 concurrent append, checksum/data coherence, and false corruption classification (2014–2017)

## Purpose

Deepen Case 83 at a boundary that the Hadoop 2.7.3 scanner evidence only partially exposed: **a checksum-verification path can reject a physically good replica when the verifier observes payload bytes and checksum metadata from different concurrent versions of that replica.**

The bounded historical anchor is Apache HDFS-11160, created 20 November 2016 and resolved 16 December 2016, together with the corresponding Apache Hadoop commit `aebb9127bae872835d057e1c6a6e6b3c6a8be6cd`. HDFS-6804 supplies an earlier 2014 operational witness for the same broad append/transfer race family. HDFS-12136 is used only as a 2017 follow-up showing that one coherence fix had a service-cost tradeoff.

This addendum separates:

- **historical record (`H/P`)** — what Apache JIRA and Apache Hadoop source/commit history directly document;
- **engineering reconstruction (`E`)** — the retention relations inferred from that race and its fix;
- **functional analogy (`A`)** — comparison to stale integrity evidence in other cases;
- **rejected strengthening (`X`)** — claims the evidence does not support.

It does **not** establish invention priority for checksum coherency, snapshot-consistent verification, append semantics, locking, scrubbing, or distributed corruption reporting.

---

## Source set and evidence grade

| Source | Date | Type | Use here | Grade |
| --- | --- | --- | --- | --- |
| Apache JIRA HDFS-6804 | created 2014-08-01; resolved 2018-01-13 | contemporary Apache bug record | earlier witness that append/transfer concurrency could yield an unexpected checksum mismatch and wrongly mark a valid source replica corrupt | **H/P** |
| Apache JIRA HDFS-11160 | created 2016-11-20; resolved 2016-12-16 | contemporary Apache bug record | primary issue statement for `VolumeScanner` false corruption classification during concurrent append | **H/P** |
| Apache Hadoop commit `aebb9127...` | 2016-12-16 UTC | Apache source commit | implementation witness for reading the last partial checksum of a finalized replica while holding the dataset lock; adds a concurrent append/scan regression test | **H/P** |
| Apache JIRA HDFS-12136 | created 2017-07-13 | contemporary Apache follow-up | documents performance/lock-contention consequences attributed to the HDFS-11160 fix and warns the race is not scanner-exclusive | **H/P** |
| Case 83 base grounding | current repository | grounded internal evidence | establishes the 2.7.3 scanner, reporting path, periodic coverage, and existing race-aware exception handling | **H/P + E** |
| Case 27 Ceph Luminous EC scrub | current repository | grounded internal case | bounded functional comparison to stale/incoherent integrity metadata | **A** |

`H/P` means historical/primary project evidence under this repository's conventions, not peer-reviewed publication status.

---

## Historical record

### H/P — 2014: a valid source replica could be wrongly marked corrupt after an append/transfer checksum race

Apache HDFS-6804 was created on 1 August 2014 after operators observed an `Unexpected checksum mismatch` while transferring a block. The issue states that the destination reported a bad block to the NameNode, the NameNode marked the source replica corrupt, yet the source replica itself remained valid and could pass checksum verification.

This is useful as an earlier operational witness for the **broad race family**. It does not prove that the exact later `VolumeScanner` path, code structure, or HDFS-11160 fix already existed in 2014.

Controlled historical statement:

> By 2014 Apache HDFS issue history recorded an append/transfer concurrency path in which a checksum mismatch could produce a false corrupt-replica classification even though the source embodiment remained valid.

---

### H/P — 2016: HDFS-11160 identifies a specific `VolumeScanner` new-checksum/old-data race

HDFS-11160's release note says the fix addresses a race that caused `VolumeScanner` to recognize a good replica as bad while the replica was being written concurrently.

The issue description gives the mechanism more precisely:

1. a replica is being appended while `VolumeScanner` scans it;
2. the scanner can obtain the **new checksum**;
3. it can still read/compare that checksum against **old data**;
4. the resulting mismatch is therefore not sufficient evidence that the retained payload embodiment is physically corrupt.

The issue also records a reported cluster incident with a high block-corruption rate and calls the bug serious because, in some cases, declaring all replicas corrupt can result in data loss. That statement is an Apache issue report about an observed/problematic path; it is **not** evidence that every HDFS deployment or every mismatch suffered physical data loss.

This directly sharpens the Case-83 relation:

> **checksum mismatch != necessarily payload corruption when the verifier's checksum and payload observations are not version-coherent.**

---

### H/P — the 2016 fix captures the last partial checksum under the dataset lock

Apache Hadoop commit `aebb9127bae872835d057e1c6a6e6b3c6a8be6cd`, authored/committed 16 December 2016 UTC, is titled `HDFS-11160. VolumeScanner reports write-in-progress replicas as corrupt incorrectly.`

In `BlockSender`, the patch:

- acquires the dataset lock;
- obtains the replica and its visible length;
- when the replica is a `FinalizedReplica`, calls `getLastChecksumAndDataLen()` while that lock is held;
- retains that last-partial-chunk checksum for the subsequent send/verification path if a concurrent append occurs.

The new `FinalizedReplica.getLastChecksumAndDataLen()` method explicitly says it needs to be called with the `FsDataset` lock acquired. The same commit adds a `testAppendWhileScanning` regression test whose comment names concurrent append and scan.

Safe conclusion:

> The fix changes **observation coherence around the last partial chunk**; it does not strengthen the checksum algorithm, rewrite the payload, or add another user-data replica.

Do not rewrite this as `the dataset lock makes all scanner observations atomic`. The inspected patch is narrower and specifically addresses the finalized-replica last-checksum race.

---

### H/P — the coherence fix itself had a later service-cost boundary

Apache HDFS-12136 (2017) says HDFS-11160's approach reads the last checksum of finalized blocks while holding the exclusive dataset lock and reports severe serialization/throughput effects under heavy I/O or xceiver activity. The follow-up also emphasizes that the underlying concurrent-reader/writer false-positive race was not unique to `VolumeScanner`.

This later issue is important because it blocks an easy conceptual shortcut:

> **verification coherence != free verification.**

A mechanism that improves the currentness/coherence of integrity evidence can consume locking and I/O resources and interfere with foreground or recovery traffic. This is a historical implementation tradeoff, not a universal law that every correct checksum verifier must take a global exclusive lock.

---

## Engineering reconstruction

The primary evidence supports these project-level distinctions.

### 1. Checksum strength and observation coherence are different properties

A checksum function can be working exactly as designed while a verifier compares a checksum for one logical version against bytes from another.

Therefore:

> **checksum algorithm correctness != checksum/data observation coherence.**

A stronger checksum does not, by itself, repair a time-of-check/version-mixing race.

### 2. Integrity evidence has currentness/version scope

Case 83 already distinguishes `replica presence` from `integrity qualification`. HDFS-11160 adds another layer:

> **integrity metadata presence != integrity metadata currentness for the payload bytes being judged.**

The checksum is not merely `present` or `missing`; the verifier needs a checksum relation that corresponds to the particular visible payload state it is evaluating.

### 3. A corruption report is a control-plane judgment, not ground truth

HDFS-11160 and HDFS-6804 both show a path where a good source embodiment can be classified/reported as corrupt after a racy mismatch.

Thus:

> **corrupt-replica report != proof of physical media corruption.**

This does not make corruption reports useless. It establishes that the report inherits the epistemic quality and concurrency semantics of the verification path that produced it.

### 4. False disqualification can reduce retention margin without first damaging the bytes

If a distributed system deauthorizes a good replica because of a false mismatch, the physical bytes can remain valid while the system's **admissible redundancy set** shrinks.

That gives a useful retention relation:

> **physical embodiment survival != continued qualification as repair source.**

The HDFS-11160 issue explicitly warns that all replicas being declared corrupt can lead to data loss. The engineering reconstruction here is only that false disqualification can consume redundancy/repair margin; it does not claim that the verifier itself magnetically/electrically damages the local medium.

### 5. Verification work can have control-plane effects

The scanner is not philosophically or physically `passive observation`: on a qualifying failure it can feed `reportBadBlocks`, which changes how the distributed system treats a replica. Yet the check normally does not rewrite the payload.

So distinguish:

> **verification-induced control-state change != physical disturbance of the retained payload.**

### 6. Coherence repair and payload repair are different operations

The HDFS-11160 patch changes how checksum evidence is captured so that later verification does not mix incompatible observations. It does not reconstruct a corrupt block from another replica.

Therefore:

> **verification-coherence fix != payload repair.**

---

## Functional comparisons

### A — Case 27 Ceph Luminous EC scrub

Case 27 already separates current payload state from checksum/integrity metadata and records situations in which stale checksum metadata can produce mismatch/EIO behavior.

The bounded analogy is:

> **integrity evidence must correspond to the payload state it is being used to qualify.**

Mechanisms differ materially:

- HDFS-11160 is a concurrent append/read observation race around a finalized replica's last partial checksum;
- the Ceph case concerns EC scrub/checksum state inside a different object-store/PG architecture.

No code, organizational, or historical genealogy is inferred.

### A — Case 18 ZFS scrub

Both Case 18 and Case 83 use background reads/checks to renew confidence in retained data. HDFS-11160 adds a counterexample to any abstract formulation that says `background checksum scan = neutral truth oracle`: the observation itself must be coherent with concurrent mutation semantics.

This is a functional comparison only. It does not project HDFS locking, append semantics, or last-partial-chunk checksums onto ZFS.

---

## Philosophical interpretation — bounded

The useful interpretive lesson is not that `truth is a checksum`.

It is narrower:

> A retained embodiment can survive materially while the system's evidence for admitting it as current/good becomes stale, incoherent, or wrongly interpreted.

Technical retention can therefore require maintenance of **relations of qualification** as well as preservation of payload bits. HDFS-11160 also shows why this relation is temporal: checksum evidence has to belong to the same relevant payload state being judged.

Stop there. This is not Apache's philosophical vocabulary and it is not a claim about archives or human memory in general.

---

## Rejected / unsupported claims

Do **not** claim:

- every HDFS checksum mismatch is a false positive;
- HDFS checksums are generally unreliable;
- HDFS-11160 proves the disk payload was physically corrupt;
- the bug always causes data loss;
- a corruption report physically deletes or sanitizes the replica;
- the 2016 patch makes all DataNode reads globally snapshot-atomic;
- holding the dataset lock is a universal requirement for coherent verification;
- HDFS-11160 is the first historical discovery of checksum/version races;
- HDFS-6804 proves an exact code genealogy into the 2016 VolumeScanner bug;
- the HDFS race and Ceph stale-integrity-metadata case are the same mechanism;
- the 2017 performance regression means the 2016 correctness issue should simply have been ignored.

---

## Related-repository check

A fresh repository search of `tmzncty/computing-archaeology` for `HDFS-11160`, `VolumeScanner`, and `BlockScanner` found no dedicated case to reuse during this slice.

Accordingly this addendum keeps the retention-specific currentness/coherence boundary here. A broader history of HDFS checksum implementation, append semantics, scanner rewrites, or GFS→HDFS genealogy still belongs primarily in `computing-archaeology` if pursued.

---

## Sources

### Primary / contemporary

- Apache JIRA HDFS-6804, **Add test for race condition between transferring block and appending block causes "Unexpected checksum mismatch exception"**, created 1 August 2014: <https://issues.apache.org/jira/browse/HDFS-6804>
- Apache JIRA HDFS-11160, **VolumeScanner reports write-in-progress replicas as corrupt incorrectly**, created 20 November 2016, resolved 16 December 2016: <https://issues.apache.org/jira/browse/HDFS-11160>
- Apache Hadoop commit `aebb9127bae872835d057e1c6a6e6b3c6a8be6cd`, **HDFS-11160. VolumeScanner reports write-in-progress replicas as corrupt incorrectly**, 16 December 2016 UTC: <https://github.com/apache/hadoop/commit/aebb9127bae872835d057e1c6a6e6b3c6a8be6cd>
- Apache JIRA HDFS-12136, **BlockSender performance regression due to volume scanner edge case**, created 13 July 2017: <https://issues.apache.org/jira/browse/HDFS-12136>

### Internal

- [`../cases/83-apache-hdfs-block-scanner-checksum-verification.md`](../cases/83-apache-hdfs-block-scanner-checksum-verification.md)
- [`83-hadoop-2003-2016-block-scanner-grounding.md`](83-hadoop-2003-2016-block-scanner-grounding.md)
- [`../cases/27-ceph-luminous-ec-deep-scrub.md`](../cases/27-ceph-luminous-ec-deep-scrub.md)
- [`../cases/18-zfs-scrub-latent-error-detection.md`](../cases/18-zfs-scrub-latent-error-detection.md)

---

## Promotion judgment

**Status: `grounded bounded deepening`.**

The core mechanism is supported by Apache's own issue report and the corresponding Apache Hadoop source commit. The 2014 and 2017 issues bound the race historically and operationally without being converted into invention/genealogy claims. The slice closes a specific `verification evidence currentness / concurrent observation coherence` gap while leaving broader HDFS scanner history and independent fault injection open.
