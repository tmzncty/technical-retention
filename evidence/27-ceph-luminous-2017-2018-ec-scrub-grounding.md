# Case 27 Grounding Record — Ceph Luminous EC Overwrites, BlueStore Checksums, and Deep Scrub (2017–2018)

## Promotion target

This record grounds [`cases/27-ceph-luminous-ec-deep-scrub-checksum-authority.md`](../cases/27-ceph-luminous-ec-deep-scrub-checksum-authority.md).

The bounded claim is:

> In Ceph Luminous, mutable erasure-coded pools depended on BlueStore checksumming and deep scrub for integrity qualification. BlueStore retained checksums as storage metadata, scrub/deep-scrub exercised those relations as scheduled background work, and a 12.2.6 regression later showed that stored checksum metadata itself could become inconsistent, requiring temporary distrust and a full deep-scrub repair cycle before ordinary trust was restored.

Status target: **`grounded`**.

---

## Evidence classes

### P1 — official Luminous release record

Ceph's official `v12.2.0 Luminous Released` notice is dated 29 August 2017 and identifies Luminous as the first `12.2.x` long-term stable release. It records BlueStore as stable/default for newly created OSDs, full data/metadata checksumming, and full support for EC overwrites.

URL: <https://ceph.com/releases/v12-2-0-luminous-released/>

### P2 — tag-matched source documentation

The Ceph source tree at tag `v12.2.0` provides period documentation matched to the release rather than today's manuals:

- `doc/rados/operations/erasure-code.rst`
- `doc/rados/configuration/bluestore-config-ref.rst`
- `doc/rados/configuration/osd-config-ref.rst`

These were fetched directly from the `ceph/ceph` GitHub repository at the release tag.

### P3 — official regression/correction record

Ceph's official `12.2.7 Luminous released` notice (17 July 2018) records the `12.2.6` per-object checksum maintenance regression and possible read `EIO`.

URL: <https://ceph.io/en/news/blog/2018/12-2-7-luminous-released/>

### P4 — official repair/requalification record

Ceph's official `v12.2.8 released` notice (4 September 2018) records the `osd distrust data digest = true` workaround and improved deep-scrub automatic repair of the resulting inconsistencies, with a full deep scrub required before disabling the workaround.

URL: <https://ceph.io/en/news/blog/2018/v12-2-8-released/>

---

## Direct source ledger

### 1. `v12.2.0` release notice — BlueStore + EC overwrite boundary

Directly established:

- release date: 29 August 2017;
- BlueStore is stable and default for newly created OSDs;
- BlueStore supports full data and metadata checksums;
- erasure-coded pools have full overwrite support;
- RBD/CephFS EC use relies on BlueStore;
- `allow_ec_overwrites=true` depends on BlueStore checksumming for deep scrub;
- the same capability is disallowed on FileStore.

Evidence use:

- integrity qualification is part of the supported mutable-EC regime, not an optional philosophical addition;
- `coded recoverability` alone does not describe the production retention contract.

### 2. `v12.2.0` `erasure-code.rst` — code geometry + checksum/deep-scrub requirement

Directly established:

- object data is split into `K` data chunks plus `M` coding chunks;
- `M` determines the number of simultaneous OSD losses tolerated in the documented examples;
- CRUSH failure-domain settings separately govern chunk placement;
- partial EC overwrites can be enabled with `allow_ec_overwrites`;
- that mode can only be used with BlueStore because BlueStore checksumming detects bit rot/corruption during deep scrub;
- FileStore + EC overwrites is explicitly described as unsafe.

Evidence use:

- code algebra, failure-domain placement, and integrity verification are distinct retained relations;
- mutable EC support is bounded to a storage backend with integrity machinery.

### 3. `v12.2.0` `bluestore-config-ref.rst` — integrity metadata is stored state

Directly established:

- BlueStore checksums all metadata and data written to disk;
- RocksDB metadata uses `crc32c`;
- BlueStore data checksumming can use `crc32c`, `xxhash32`, `xxhash64`, or truncated CRC variants;
- default data checksum is `crc32c`;
- full checksumming increases metadata that must be stored and managed;
- in many cases a checksum value is stored per 4 KiB of data;
- smaller/truncated checksums reduce metadata at the cost of higher undetected-error probability.

Evidence use:

- checksum state is not an abstract calculation performed only at read time; it is retained metadata with storage/management cost;
- `checksum metadata ≠ payload` but later verification depends on their relation.

### 4. `v12.2.0` `osd-config-ref.rst` — verification is scheduled background work

Directly established:

- Ceph calls the mechanism `scrubbing`;
- light scrub compares object/catalog metadata such as size/attributes;
- deep scrub fully reads data and uses checksums;
- scrub has minimum/maximum intervals and a separate deep-scrub interval;
- defaults in the bounded document are roughly daily light scrub / weekly deep scrub;
- concurrency, time windows, system-load thresholds, sleeps, recovery interaction, and scrub priority can all delay or throttle maintenance;
- the documentation explicitly notes scrub can reduce cluster performance.

Evidence use:

- checksum retention does not automatically mean checksum relations have recently been exercised;
- proactive integrity maintenance consumes schedulable service resources.

### 5. official `12.2.7` notice — checksum maintenance regression

Directly established:

- `12.2.6` is described as a broken release with serious regressions;
- an incomplete backport attempted to avoid maintaining both per-object checksum and internal BlueStore checksum;
- omission of a critical follow-on patch meant the stored per-object checksum failed to update for some objects;
- this could result in an `EIO` when reading those objects.

Evidence use:

- retained integrity metadata can itself be inconsistent;
- a read/checksum failure is not automatically a proof of payload/media corruption;
- correctness of the checksum-maintenance path is part of the integrity regime.

### 6. official `v12.2.8` notice — distrust and repair of integrity metadata

Directly established:

- `12.2.7` introduced `osd distrust data digest = true` as a workaround for clusters exposed to the broken release;
- affected clusters could continue to report `data_digest` mismatch health errors;
- `12.2.8` improved deep-scrub code to automatically repair these inconsistencies;
- after upgrading the entire cluster, operators were instructed to fully deep scrub it and resolve all such inconsistencies;
- only after that full verification/repair pass was it considered safe to disable the distrust workaround.

Evidence use:

- verification metadata can lose and later regain operational authority;
- full verification coverage can itself be a repair/requalification milestone;
- deep scrub can repair the integrity relation, not only detect bad user payload.

---

## Source-inspection boundary

The tag-matched Ceph source documentation was read directly from GitHub at `v12.2.0`. These are text/source files, so no PDF facsimile or screenshot claim is involved.

The official Ceph release notices were read as maintained project release records. This grounding record does **not** claim to have reconstructed the exact code path responsible for the `12.2.6` regression or the complete per-shard repair algorithm after every EC scrub inconsistency. Those implementation details remain outside the bounded claim.

The absence of a source-level reconstruction is intentional: the historical record already establishes the integrity-metadata failure and repair sequence without requiring speculative reverse engineering.

---

## Terminology and prior-art boundary

Historical vocabulary is preserved as `BlueStore`, `checksumming`, `deep scrub`, `allow_ec_overwrites`, `data_digest`, `distrust`, `EIO`, and `inconsistencies`.

Project terms such as `verification authority`, `integrity-metadata currentness`, and `integrity-qualified fragment` are engineering reconstructions and must remain labeled as such.

No invention-priority claim is made:

- Case 26 already records GFS 2003 `scan and verify` as a proactive background-integrity precedent;
- Case 18 records 2004 `disk scrubbing` terminology/prior art;
- Cases 19 and 24 already control Reed–Solomon/LRC coding-priority boundaries;
- Case 05 covers earlier Ceph/RADOS replicated currentness without implying that later BlueStore semantics were present in 2006–2007.

The novelty of this bounded case is the **combination of mutable EC support, backend checksumming/deep scrub, and a documented release incident in which checksum metadata itself became untrustworthy**.

---

## Cross-case controls

### Case 05 — early RADOS

Shared family: Ceph/RADOS.

Required distinction: Case 05 is a 2006–2007 replicated-object currentness/peering/commit regime. Case 27 is a 2017–2018 BlueStore/EC-overwrite/integrity-maintenance regime. Shared product lineage does not establish identical semantics.

### Case 18 — ZFS scrub

Shared function: proactive checksum verification can reveal latent integrity problems.

Required distinction: ZFS Case 18 treats the checksum as an integrity qualifier for payload/copies; the Luminous regression adds a direct counterexample in which the stored integrity datum can itself be wrong. Therefore `checksum mismatch = payload corruption` is rejected as a universal inference.

### Case 26 — GFS

Shared function: stored checksum state qualifies potential repair sources before trusting them.

Required distinction: GFS 2003 uses full replicas and local per-block checksums. Ceph Luminous here operates with erasure-coded chunks, mutable overwrites, BlueStore extent/data checksums, and a later release-specific digest-trust failure.

### Cases 19 / 24 / 25 — coded storage

- f4 establishes coding algebra versus failure-domain placement and staged repair;
- WAS LRC establishes reconstruction cost and validated representation handoff;
- Swift establishes committed, timestamp-coherent coded currentness;
- Ceph Luminous here establishes local integrity qualification and fallible verification metadata.

No case substitutes for the others.

---

## Related-repository check

GitHub search of `tmzncty/computing-archaeology` for `Ceph`, `BlueStore`, `deep scrub`, `erasure coding`, and checksum-focused combinations returned no dedicated matching case during this slice. No existing technical history was copied.

If a broader Ceph/BlueStore implementation history is later developed, it should primarily live in `computing-archaeology`; `technical-retention` should keep only the retention-specific integrity/currentness argument.

---

## Evidence maturity

**`grounded`** is justified because:

1. the 2017 mechanism is supported by official release documentation and tag-matched project source files;
2. EC overwrite support, checksum semantics, and scrub scheduling each have direct period/project-primary anchors;
3. the 2018 failure/correction sequence is recorded in official Ceph release notes with exact affected versions and operational workaround/repair instructions;
4. the case includes a strong counterexample rather than merely another positive description of checksum integrity;
5. terminology/prior-art boundaries are explicit;
6. related-repository duplication was checked;
7. the ungrounded exact per-shard repair implementation is explicitly excluded rather than inferred.

Remaining work is a separate implementation-archeology problem: exact Luminous-era EC deep-scrub shard comparison/authoritative-source selection, reconstruction after a bad shard, later BlueStore checksum evolution, and modern automatic-repair semantics.
