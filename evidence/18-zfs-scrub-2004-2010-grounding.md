# Case 18 Grounding Record — ZFS Scrub, Latent-Error Detection, and Repair Timing (2004–2010)

## Promotion target

This record grounds [`cases/18-zfs-scrub-latent-error-detection.md`](../cases/18-zfs-scrub-latent-error-detection.md).

The bounded claim is:

> A storage system can retain enough redundant information to repair a block yet fail to exercise that repair opportunity until the defect is discovered. ZFS `scrub` deliberately moves verification before ordinary demand by traversing current pool data, while checksum validation and redundant copies permit conditional self-healing. This is distinct from device-replacement `resilvering`, which restores known-missing/out-of-date embodiments and redundancy margin.

Status target: **`grounded`**.

---

## Evidence classes

### P1 — system-primary / manufacturer-institutional documentation

Oracle's archive of the Sun/OpenSolaris-era _Solaris ZFS Administration Guide_ is used for the bounded ZFS semantics:

1. `Checksums and Self-Healing Data`
2. `Controlling ZFS Data Scrubbing`
3. `Viewing Resilvering Status`

These pages directly support the named ZFS operations, their service-level semantics, and the relationship among checksum validation, redundant-copy repair, scrubbing, and resilvering.

### P2 — scholarly prior art

Schwarz et al., MASCOTS 2004, supplies a direct pre-ZFS-priority boundary for the general term and mechanism `disk scrubbing`: periodic access intended to detect failures, with all-data scrubbing able to reveal block failures and permit rebuilding from redundancy.

### S1 — independent empirical context

Bairavasundaram et al., SIGMETRICS 2007, supplies independent field-study context for `latent sector errors`: faults that can remain undetected until the corresponding sectors are accessed.

The SIGMETRICS study is **not** used as evidence about ZFS implementation or product-specific rates.

---

## Direct source ledger

### 1. Solaris ZFS Administration Guide — checksums and self-healing

URL: <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gaypb/index.html>

Directly established:

- all ZFS data and metadata is checksummed using a selectable algorithm;
- checksums are arranged so that failures such as a complete block being written to the wrong location can be detected;
- checksumming and recovery are performed at the filesystem layer and are transparent to applications;
- when a bad data block is detected and redundancy is available, ZFS fetches correct data from another redundant copy and repairs the bad data.

Evidence use:

- `physical bytes returned ≠ verified acceptable block`;
- checksum evidence is constitutive of the bounded currentness/integrity decision;
- repair requires both detection and a trustworthy redundant source.

Not established by this page:

- one universal checksum algorithm for every ZFS deployment;
- immunity to every possible corruption class;
- an invention-priority claim for filesystem checksumming or self-healing.

### 2. Solaris ZFS Administration Guide — controlling data scrubbing

URL: <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gbbxi/index.html>

Directly established:

- ZFS can encounter errors either during scrubbing or when a file is accessed on demand;
- explicit scrubbing traverses all pool data once and verifies that all blocks can be read;
- ordinary I/O has priority over the scrub;
- the pool remains usable while scrubbing proceeds;
- only one active scrub-class operation occurs per pool;
- routine scrubbing generates continuous disk I/O and can prevent low-power idle behavior;
- device replacement/resilvering can suspend an in-progress scrub until resilvering finishes.

Evidence use:

- proactive verification is distinct from application-demand discovery;
- integrity maintenance consumes time, bandwidth, and energy;
- scrub scheduling is retention infrastructure rather than a free property of the medium.

Important wording boundary:

The historical documentation says that the scrub verifies blocks can be read and elsewhere documents checksum-based integrity/self-healing. The project describes the combined mechanism as **proactive integrity verification**. It does not fabricate a historical variable called `verification age` or claim that every scrub detection necessarily results in repair.

### 3. Solaris ZFS Administration Guide — resilvering

URL: <https://docs.oracle.com/cd/E19120-01/open.solaris/817-2271/gbcus/index.html>

Directly established:

- moving data from a good copy to a replacement device is called `resilvering`;
- ZFS can resilver only the minimum necessary data rather than blindly copying unused regions;
- resilvering is interruptible/resumable;
- the pool may remain `ONLINE` or `DEGRADED` while the desired redundancy level has not yet been restored;
- completion returns the configuration to the intended complete state.

Evidence use:

- `serving data during maintenance ≠ redundancy restoration complete`;
- scrub and resilver can share scan/repair infrastructure while remaining different trigger/completion relations.

### 4. Schwarz et al. — disk-scrubbing prior art

Publication record: <https://www.ssrc.us/pub/schwarz-mascots04.html>

Bibliographic record:

- Thomas Schwarz, Qin Xin, Ethan L. Miller, Darrell D. E. Long, Andy Hospodor, Spencer Ng;
- `Disk Scrubbing in Large Archival Storage Systems`;
- MASCOTS 2004, pp. 409–418;
- publication date: October 2004.

The authors' research-center record/abstract directly states:

- archival systems can lose data through device- and block-level failures;
- failures must be detected early enough to use available redundancy;
- they call periodic access for detection `disk scrubbing`;
- scrubbing all stored data can detect block failures and allow affected blocks to be rebuilt;
- `opportunistic` scrubbing is a distinct scheduling strategy.

Evidence use:

- blocks the claim `ZFS invented scrubbing`;
- supplies a pre-existing engineering relation between detection timing and redundancy-assisted repair;
- shows that scrub **schedule** is itself a reliability parameter rather than an implementation afterthought.

Not established:

- ZFS design lineage from this paper;
- identity between the paper's archival-storage design and ZFS;
- one universally optimal scrub interval.

### 5. Bairavasundaram et al. — latent sector errors

Bibliographic anchor: <https://dl.acm.org/doi/10.1145/1254882.1254917>

Metadata/abstract-level point used in this slice:

- the study treats latent sector errors as errors that remain undetected until the corresponding disk sectors are accessed;
- it analyzes production storage data at large scale and frames LSEs as a reliability mechanism problem distinct from complete drive failure.

Evidence use:

- independent empirical support for the category `defect exists before discovery`;
- motivates why moving verification earlier can affect effective repair opportunity.

Boundary:

The paper's measured rates, device models, and storage-system implementation details are **not** assigned to ZFS. No exact percentage is needed for Case 18's mechanism claim.

---

## Claim matrix

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| `disk scrubbing` was a named reliability technique by October 2004 | H/P | Schwarz et al. MASCOTS 2004 publication record/abstract | grounded |
| ZFS explicit scrub traverses all pool data and checks readability before application demand necessarily reaches every block | H/P | Solaris ZFS Administration Guide, `Controlling ZFS Data Scrubbing` | grounded |
| ZFS checksums all data and metadata at the filesystem layer in the bounded documentation | H/P | `Checksums and Self-Healing Data` | grounded |
| detected bad data can be repaired from a redundant copy | H/P | `Checksums and Self-Healing Data` | grounded |
| scrubbing consumes background I/O and can prevent disks entering low-power idle state | H/P | `Controlling ZFS Data Scrubbing` | grounded |
| ZFS resilvering reconstructs/copies required data to replacement/out-of-date devices and desired redundancy is not restored until completion | H/P | `Viewing Resilvering Status` | grounded |
| latent sector faults can exist before they are discovered by access | H/S | Bairavasundaram et al. SIGMETRICS 2007 | grounded as independent empirical context |
| `physical presence/readability ≠ verified integrity` | E | checksum/self-healing system semantics | supported |
| `redundancy exists ≠ defect has been discovered` | E | ZFS scrub vs demand + latent-error context | supported |
| `detection work ≠ repair work` | E | scrub traversal + conditional self-healing | supported |
| `scrub ≠ resilver/rebuild` | E/A | ZFS operation semantics + Case 17 comparison | supported |
| earlier verification can preserve a repair opportunity that would otherwise disappear after another failure | E | scrub/prior-art/latent-error relation | supported, failure-model-relative |
| ZFS invented disk scrubbing | X | contradicted by 2004 prior art | rejected |
| successful scrub guarantees indefinite future integrity | X | unsupported; future faults remain possible | rejected |
| SIGMETRICS field rates describe ZFS pools | X | unsupported | rejected |
| scrub is technically identical to DRAM refresh | X | mechanism differs: verification/conditional repair vs mandatory periodic restoration | rejected |

---

## Cross-case comparison controls

### Case 03 — DRAM refresh

DRAM refresh performs scheduled restoration because retained charge predictably decays. Case 18's scrub performs scheduled/proactive **verification** and only conditionally repairs a block.

Therefore:

> `scheduled maintenance ≠ scheduled reconstruction of every healthy state`.

### Case 05 — RADOS replica repair

RADOS repair depends on placement/version/authority state after membership/object inconsistency. ZFS self-healing depends on checksum validation and another redundant pool copy.

Therefore:

> `repair from another embodiment` is a functional similarity, not identical currentness machinery.

### Case 14 — HDD defect reassignment

Case 14 grounds changing the serving physical sector after a defect and explicitly separates reassignment from payload preservation. Case 18 adds **proactive discovery** and checksum-qualified repair before/without a full device replacement event.

### Case 17 — RAID parity reconstruction

Case 17 focuses on reconstructability after a known failed member and the interval before redundancy margin is restored. Case 18 adds the earlier detection problem:

```text
latent bad block exists
    + redundancy still available
    + no demand has touched the block
        -> defect may remain operationally unknown

scrub reaches block
        -> defect becomes known
        -> repair can occur while redundancy source still exists
```

Thus:

> `nominal redundancy ≠ verified repair margin`.

This is a project engineering finding, not historical RAID/ZFS vocabulary.

---

## Related-repository audit

Searched `tmzncty/computing-archaeology` for:

- `scrub`;
- `scrubbing`;
- `latent sector`;
- `ZFS`.

No dedicated case/result was found in this slice. No generic history of ZFS or disk integrity checking is therefore duplicated here. If such a history appears later, Case 18 should retain only its retention-specific detection/repair-timing argument and link outward.

---

## Facsimile / access boundary

No PDF figure or scanned page is necessary for the central claims in this case. The core ZFS evidence is directly inspectable as official HTML documentation. The Schwarz prior-art claim is grounded at the authors' institutional publication-record/abstract level. The SIGMETRICS latent-sector-error point is used only at metadata/abstract level.

Therefore this grounding record **does not** claim:

- direct visual inspection of every page/figure of the MASCOTS 2004 paper;
- direct visual inspection of the ACM SIGMETRICS paper;
- source-code-level reconstruction of the historical ZFS scan implementation.

Those are possible deepening tasks, not blockers for the bounded mechanism.

---

## Promotion decision

**Promote Case 18 directly to `grounded`.**

Reasons:

1. system-primary/institutional ZFS documentation directly defines scrub, checksumming/self-healing, and resilvering;
2. 2004 scholarly prior art prevents a false invention claim;
3. independent 2007 empirical work supports the latent-before-access failure category;
4. the case has explicit historical/engineering/analogy boundaries;
5. related-repository duplication was checked;
6. central claims do not depend on a single fragile secondary source or an uninspected diagram.

Remaining work is optional deepening: original Sun source/man-page archaeology by specific build, exact historical scan implementation, automatic scheduling history, later OpenZFS scan redesign, and distributed scrub semantics.
