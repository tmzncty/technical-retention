from pathlib import Path

ROOT = Path('.')


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def write(path, text):
    if not text.endswith('\n'):
        text += '\n'
    (ROOT / path).write_text(text, encoding='utf-8')


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected one anchor, found {count}')
    return text.replace(old, new, 1)

addendum_path = 'evidence/83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md'
if (ROOT / addendum_path).exists():
    raise SystemExit(f'{addendum_path} already exists')

addendum = r'''# Case 83 deepening — HDFS-11160 concurrent append, checksum/data coherence, and false corruption classification (2014–2017)

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
'''
write(addendum_path, addendum)

# Case 83: add the 2016 coherence deepening and controlled relations.
case_path = 'cases/83-apache-hdfs-block-scanner-checksum-verification.md'
case = read(case_path)
anchor = "The implementation preserves room for concurrency/race interpretation before deauthorizing a replica.\n\n"
insert = anchor + r'''### H/P — 2016 HDFS-11160: checksum verification can fail on an incoherent concurrent observation

A later Apache bug record closes an important limit in the 2.7.3 account above. HDFS-11160, created 20 November 2016 and resolved 16 December 2016, reports that `VolumeScanner` could classify a **good** replica as corrupt when an append raced the scan. The issue identifies the specific comparison failure: the scanner could use a **new checksum** against **old data**, producing a mismatch even though the retained replica was not physically bad.

The corresponding Apache Hadoop commit `aebb9127bae872835d057e1c6a6e6b3c6a8be6cd` changes `BlockSender` so that, for a `FinalizedReplica`, the last partial checksum and its data length are obtained while the dataset lock is held. The commit also adds a concurrent append/scan regression test.

This yields three stricter boundaries:

> **checksum mismatch != necessarily physical payload corruption.**

> **checksum algorithm correctness != checksum/data observation coherence.**

> **integrity metadata presence != currentness for the particular payload state being judged.**

The 2017 follow-up HDFS-12136 reports that this lock-based coherence strategy could serialize `BlockSender` construction under load, so the historical fix also supplies a cost boundary: **coherent verification != free verification**. This is a product/code-path tradeoff, not a claim that every correct verifier must take a global exclusive lock.

The detailed source/claim map is in [`../evidence/83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md`](../evidence/83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md).

'''
case = replace_once(case, anchor, insert, 'case historical insert')
case = replace_once(
    case,
    "14. `distributed repair capacity ≠ corruption discovery`.\n",
    "14. `distributed repair capacity ≠ corruption discovery`;\n15. `checksum mismatch ≠ necessarily physical payload corruption`;\n16. `checksum algorithm correctness ≠ checksum/data observation coherence`;\n17. `integrity metadata presence ≠ integrity metadata currentness for the payload state being judged`;\n18. `corrupt-replica report ≠ ground truth about media damage`;\n19. `verification-coherence fix ≠ payload repair`;\n20. `coherent verification ≠ free verification`.\n",
    'case engineering list')
case = replace_once(
    case,
    "- later `BlockScanner` / `VolumeScanner` changes after 2.7.3;\n",
    "- later `BlockScanner` / `VolumeScanner` evolution beyond the bounded HDFS-11160 fix, including later alternatives to its locking tradeoff;\n",
    'case future work')
case = replace_once(
    case,
    "- Apache JIRA, `HDFS-7548`, **Corrupt block reporting delayed until datablock scanner thread detects it** (2014–2015): <https://issues.apache.org/jira/browse/HDFS-7548>\n",
    "- Apache JIRA, `HDFS-7548`, **Corrupt block reporting delayed until datablock scanner thread detects it** (2014–2015): <https://issues.apache.org/jira/browse/HDFS-7548>\n- Apache JIRA, `HDFS-11160`, **VolumeScanner reports write-in-progress replicas as corrupt incorrectly** (2016): <https://issues.apache.org/jira/browse/HDFS-11160>\n- Apache Hadoop commit `aebb9127bae872835d057e1c6a6e6b3c6a8be6cd`, **HDFS-11160. VolumeScanner reports write-in-progress replicas as corrupt incorrectly** (2016-12-16 UTC): <https://github.com/apache/hadoop/commit/aebb9127bae872835d057e1c6a6e6b3c6a8be6cd>\n- Apache JIRA, `HDFS-12136`, **BlockSender performance regression due to volume scanner edge case** (2017): <https://issues.apache.org/jira/browse/HDFS-12136>\n",
    'case sources')
case = replace_once(
    case,
    "The central claims are directly supported by Apache documentation, tag-matched Hadoop 2.7.3 source, and earlier Apache issue history; GFS 2003 supplies a conservative prior-art boundary.",
    "The central claims are directly supported by Apache documentation, tag-matched Hadoop 2.7.3 source, earlier Apache issue history, and the 2016 HDFS-11160 issue/commit deepening; GFS 2003 supplies a conservative prior-art boundary."
    , 'case status')
write(case_path, case)

# Base evidence record: link the addendum and add a compact claim map.
ev_path = 'evidence/83-hadoop-2003-2016-block-scanner-grounding.md'
ev = read(ev_path)
ev = replace_once(
    ev,
    "| Hadoop `rel/release-2.7.3`, `VolumeScanner.java` | 2.7.3 | tag-matched source | per-volume threads, verification path, race handling, bad-block reporting, cursor persistence, coverage scheduling | **H/P** |\n",
    "| Hadoop `rel/release-2.7.3`, `VolumeScanner.java` | 2.7.3 | tag-matched source | per-volume threads, verification path, race handling, bad-block reporting, cursor persistence, coverage scheduling | **H/P** |\n| Apache JIRA HDFS-11160 + Hadoop commit `aebb9127...` | 2016 | project issue + matching source commit | concurrent append can mix new checksum with old data; fix captures last partial checksum under dataset lock | **H/P** |\n| Apache JIRA HDFS-12136 | 2017 | project follow-up | lock-based HDFS-11160 fix had a documented BlockSender contention/performance cost | **H/P** |\n",
    'evidence source table')
claim_anchor = "## Claim ledger\n"
claim_insert = r'''## 2016 addendum — verification evidence must be coherent with the payload state

Detailed record: [`83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md`](83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md).

HDFS-11160 records a concrete counterexample to the shortcut `checksum mismatch = corrupt bytes`: during concurrent append, `VolumeScanner` could compare a new checksum against old data and report a good replica as corrupt. Apache's matching commit captures the finalized replica's last partial checksum while holding the dataset lock and adds a concurrent append/scan regression test.

This later evidence deepens, rather than contradicts, the 2.7.3 `ScanResultHandler` boundary above. The earlier handler already recognized that some race-related failures should not automatically become bad-block reports; HDFS-11160 shows another race that escaped that classification logic because the read/check path itself could construct an incoherent checksum/data observation.

The safe engineering relations are:

- `checksum mismatch != necessarily physical payload corruption`;
- `checksum algorithm correctness != observation coherence`;
- `integrity metadata presence != currentness for the judged payload version`;
- `corrupt-replica report != ground truth`;
- `verification-coherence fix != payload repair`.

HDFS-12136 is retained as a separate 2017 cost boundary: the issue attributes severe serialization under some load to the HDFS-11160 lock/read strategy. It does not prove that every coherent verifier requires that locking design.

---

'''
ev = replace_once(ev, claim_anchor, claim_insert + claim_anchor, 'evidence addendum insert')
ev = replace_once(
    ev,
    "| HDFS scanner and ZFS scrub are functionally comparable but historically distinct | A | Case 18 + HDFS evidence | analogy only |\n",
    "| HDFS scanner and ZFS scrub are functionally comparable but historically distinct | A | Case 18 + HDFS evidence | analogy only |\n| concurrent append can make checksum/data observations incoherent | H/P | HDFS-11160 | bounded to documented race; not every mismatch |\n| the 2016 fix captures last partial checksum under dataset lock | H/P | commit `aebb9127...` | does not establish global snapshot atomicity |\n| checksum mismatch can be a false corruption verdict | H/P + E | HDFS-11160, HDFS-6804 | does not deny genuine corruption mismatches |\n| coherence correction can have service cost | H/P + E | HDFS-12136 | product/code-path witness, not universal law |\n",
    'evidence claim rows')
ev = replace_once(
    ev,
    "15. `corruption deauthorization ≠ secure sanitization`.\n",
    "15. `corruption deauthorization ≠ secure sanitization`;\n16. `checksum mismatch ≠ necessarily physical payload corruption`;\n17. `checksum algorithm correctness ≠ checksum/data observation coherence`;\n18. `integrity metadata presence ≠ currentness for the judged payload state`;\n19. `corrupt-replica report ≠ ground truth about media damage`;\n20. `verification-coherence fix ≠ payload repair`;\n21. `coherent verification ≠ free verification`.\n",
    'evidence engineering list')
ev = replace_once(
    ev,
    "Searches of `tmzncty/computing-archaeology` for `HDFS`, `HDFS block scanner checksum`, and the specific scanner mechanism returned no dedicated case at the time of this slice.\n",
    "Searches of `tmzncty/computing-archaeology` for `HDFS`, `HDFS block scanner checksum`, and the specific scanner mechanism returned no dedicated case at the time of the original slice. A fresh check during the HDFS-11160 deepening likewise found no dedicated `HDFS-11160`, `VolumeScanner`, or `BlockScanner` case to reuse.\n",
    'evidence related repo')
write(ev_path, ev)

# ROADMAP: mark this bounded later-scanner slice and refine the open false-mismatch item.
roadmap_path = 'ROADMAP.md'
roadmap = read(roadmap_path)
case83_end = "broad scanner genealogy and production fault validation remain separate work.\n"
roadmap = replace_once(
    roadmap,
    case83_end,
    case83_end + "- [x] HDFS `VolumeScanner` concurrent-append verification-coherence deepening — [`evidence/83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md`](evidence/83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md) grounds HDFS-11160 (2016): a scanner can compare a new checksum with old data during append and falsely classify a good replica as corrupt; the matching Apache commit captures the finalized replica's last partial checksum under the dataset lock, while HDFS-12136 supplies the bounded performance-cost counterexample. This advances integrity-evidence currentness/coherence without treating every checksum mismatch as false or claiming the lock strategy is universal.\n",
    'roadmap Case83 completion')
roadmap = replace_once(
    roadmap,
    "- [ ] stale/corrupt integrity metadata, false checksum mismatch, or premature restoration of trust before prescribed verification coverage;\n",
    "- [ ] stale/corrupt integrity metadata, false checksum mismatch, or premature restoration of trust before prescribed verification coverage — **partially advanced by the Case 83 HDFS-11160 deepening**: concurrent append can make a verifier compare a new checksum against old data and falsely deauthorize a good replica, so checksum/data observation coherence is distinct from checksum strength. Still open: persistent integrity-metadata corruption, cross-replica correlated false evidence, premature trust restoration, broader distributed-store regimes, and independent fault injection;\n",
    'roadmap forgetting item')
write(roadmap_path, roadmap)

# CASE_INDEX: append new bounded findings after the existing current maximum (2462).
index_path = 'CASE_INDEX.md'
index = read(index_path)
if '## Case 83 deepening — HDFS-11160 concurrent-append verification-coherence findings' in index:
    raise SystemExit('CASE_INDEX HDFS-11160 section already present')
for n in range(2463, 2475):
    if f'**{n} —' in index or f'{n}. **' in index:
        raise SystemExit(f'finding {n} already present')
section = r'''

## Case 83 deepening — HDFS-11160 concurrent-append verification-coherence findings

Evidence: [`evidence/83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md`](evidence/83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md)

- **2463 — HDFS-11160 is a later failure/fix witness, not BlockScanner invention priority.** The issue was created 20-Nov-2016 and resolved 16-Dec-2016; it deepens the already-grounded scanner case without moving HDFS background-scanning origins to 2016. (`H/P`, `X`)
- **2464 — checksum mismatch != necessarily physical payload corruption.** HDFS-11160 directly records `VolumeScanner` comparing a new checksum against old data during concurrent append and recognizing a good replica as bad. (`H/P`, `E`)
- **2465 — checksum algorithm correctness != checksum/data observation coherence.** The documented failure can arise from mixing two payload/checksum states even when the checksum computation itself behaves correctly. (`H/P`, `E`)
- **2466 — integrity-metadata presence != integrity-metadata currentness for the judged payload state.** A checksum can exist yet belong to a different concurrent version from the bytes being verified. (`H/P`, `E`)
- **2467 — corrupt-replica report != ground truth about media damage.** HDFS-6804 and HDFS-11160 provide bounded Apache witnesses in which a valid/good replica could be wrongly classified after a racy checksum mismatch. (`H/P`, `E`)
- **2468 — physical embodiment survival != continued qualification as repair source.** False deauthorization can shrink the system's admissible replica set while the local bytes remain valid. (`E`)
- **2469 — false-positive qualification failure != physical disturbance.** The verifier can change distributed control state by reporting a replica bad without first magnetically/electrically damaging the retained payload. (`H/P`, `E`)
- **2470 — verification-coherence fix != payload repair.** Commit `aebb9127...` changes capture of the last partial checksum under the dataset lock; it does not reconstruct corrupt user data from another replica. (`H/P`, `E`)
- **2471 — coherent verification != free verification.** HDFS-12136 attributes serious BlockSender serialization under some workloads to the HDFS-11160 lock/read strategy, showing a historical correctness/service-cost tradeoff without making global locking universal. (`H/P`, `E`, `X`)
- **2472 — scanner-specific bug framing != scanner-exclusive race family.** HDFS-12136 explicitly warns that concurrent-reader/writer false-positive checksum errors can affect readers beyond `VolumeScanner`; Case 83 nevertheless remains bounded to the scanner path it can directly ground. (`H/P`, `X`)
- **2473 — HDFS/Ceph integrity-currentness comparison is functional, not genealogical.** Case 27 stale-integrity evidence and HDFS-11160 both show that integrity evidence must correspond to the judged payload state, but their object models, mechanisms, code, and histories differ. (`A`, `X`)
- **2474 — related-repository nonduplication remains explicit.** A fresh `computing-archaeology` search found no dedicated HDFS-11160/VolumeScanner/BlockScanner case; this slice retains the retention-specific currentness relation here and leaves broader scanner/append/checksum genealogy to the companion repository. (`H/P` project-state record)
'''
index += section
write(index_path, index)

# Canonical validation inside the helper, before the workflow's git checks.
expected = [
    addendum_path,
    case_path,
    ev_path,
    roadmap_path,
    index_path,
]
for path in expected:
    if not (ROOT / path).is_file():
        raise SystemExit(f'missing expected file {path}')

idx = read(index_path)
for n in range(2463, 2475):
    token = f'**{n} —'
    if idx.count(token) != 1:
        raise SystemExit(f'finding token {token!r} occurs {idx.count(token)} times')

print('Case 83 HDFS-11160 integration applied successfully')
