# Ceph Luminous EC Overwrites: BlueStore Checksums, Deep Scrub, and Integrity-Metadata Authority

## Scope

- **Bounded system:** Ceph Luminous `v12.2.x`, primarily the 2017 `v12.2.0` release documentation plus the 2018 `v12.2.7`/`v12.2.8` correction record.
- **Bounded mechanism:** erasure-coded pools with overwrites on BlueStore; per-device data checksums; periodic light/deep PG scrubbing; and the later Luminous incident in which checksum metadata itself became inconsistent and had to be distrusted/repaired.
- **Research question:** when an erasure-coded object is mutable, what additional retained integrity state is required to decide whether a surviving fragment is trustworthy, and what happens when that integrity state itself is wrong?
- **Historical prior-art boundary:** Ceph's own replicated-PG `deep scrub` implementation is anchored separately to September–October 2012. That earlier mechanism prevents a false Luminous-origin claim; it is not treated as if 2012 replicated scrub already had 2017 BlueStore/EC semantics.

This is **not** a general history of Ceph, BlueStore, erasure coding, RBD, CephFS, CRC algorithms, or scrubbing. It does not claim that Ceph invented checksums, erasure coding, bit-rot detection, or background scrub. Early RADOS replication/currentness is already handled in Case 05; the present case is a later, release-specific integrity regime.

The bounded retention claim is:

> **In Luminous, mutable erasure-coded storage was explicitly tied to BlueStore checksumming and deep scrub. The code algebra that makes an object reconstructable was therefore not sufficient by itself: stored fragments also had to remain integrity-qualified. The 12.2.6 checksum regression then shows that the verifier itself is retained state that can become inconsistent, so `checksum mismatch` cannot be universalized as `payload corruption`.**

`integrity-qualified coded fragment`, `verification authority`, `integrity-metadata currentness`, and `repair-margin qualification` below are **project engineering terms**, not historical Ceph vocabulary.

---

## Historical vocabulary

The bounded sources directly use:

- `erasure coded pool`;
- `chunk`;
- `K` / `M`;
- `allow_ec_overwrites`;
- `BlueStore` / `bluestore`;
- `checksumming`;
- `bitrot` / `corruption`;
- `scrubbing`;
- `deep scrubbing` / `deep-scrub`;
- `data_digest` / per-object checksum in the 2018 correction record;
- `osd distrust data digest`;
- `EIO`;
- `inconsistencies`.

The project terms above should not be substituted into historical quotations as if they were Ceph's own 2017–2018 vocabulary.

---

## Historical record

### H/P — Ceph `deep scrub` predates Luminous and began as replicated-PG comparison

Ceph commit [`9013efd3a3cf92d1ec8e2a39639214792067d0d2`](https://github.com/ceph/ceph/commit/9013efd3a3cf92d1ec8e2a39639214792067d0d2), dated 5 September 2012, introduced the bounded deep-scrub witness used here. Its commit message says deep scrub reads every file's contents from the store, computes a `crc32` digest, and has the primary compare digests across replicas; a mismatch marks the PG `inconsistent`. The patch also adds `last_deep_scrub` / `last_deep_scrub_stamp` and a default `osd_deep_scrub_interval` of one week.

The same source preserves an important compatibility boundary. OSDs without deep-scrub support perform ordinary chunky scrub, while the subset that supports deep scrub has its content digests compared. During such a mixed-capability rollout, requesting deep scrub therefore did **not** itself prove equivalent content-level verification of every replica.

A companion documentation commit, [`3fd5914cf35829c3f2e9e5c0a548fae0862732aa`](https://github.com/ceph/ceph/commit/3fd5914cf35829c3f2e9e5c0a548fae0862732aa), explicitly distinguishes three September-2012 operations: `scrub` compares replica object metadata, `deep-scrub` additionally compares object contents, and `repair` fixes an inconsistent replicated PG by replacing inconsistent objects with the primary's copy. Ceph's official `v0.53` release notice of 16 October 2012 likewise announces the new deep scrub as comparing object content across replicas, once per week by default.

This changes the historical boundary without changing the bounded Luminous question: **Luminous did not introduce Ceph's concept of deep scrub.** The 2017–2018 contribution studied below is the later composition of mutable EC overwrites, BlueStore-retained checksums, scheduled deep scrub, and a release incident in which integrity metadata itself lost authority.

The 2012 `repair` wording is retained as historical policy, not promoted into a claim that the primary is objectively correct. Case 29's 2018 source-level analysis later shows a more qualified `authoritative` candidate path and explicitly preserves uncertainty about correctness.

**Primary anchors:** Ceph commits `9013efd3...` and `3fd5914c...`; Ceph `v0.53 released`, 16 October 2012.

### H/P — Luminous ties EC overwrites to BlueStore integrity support

Ceph `v12.2.0 Luminous`, released 29 August 2017, made BlueStore stable and the default backend for newly created OSDs, advertised full data and metadata checksums, and made erasure-coded pools fully support overwrites. The release's compatibility notes say RBD and CephFS can use erasure coding with BlueStore and that `allow_ec_overwrites=true` relies on **BlueStore's checksumming to do deep scrubbing**; enabling that mode on FileStore is not allowed.

The tag-matched `v12.2.0` `erasure-code.rst` documentation states the same constraint: partial writes for EC pools are allowed only on BlueStore because BlueStore checksumming is used to detect bit rot or other corruption during deep scrub.

**Primary anchors:** Ceph `v12.2.0` release notes; `ceph/ceph` tag `v12.2.0`, `doc/rados/operations/erasure-code.rst`.

### H/P — coding geometry and integrity qualification are separate relations

The same `v12.2.0` erasure-code documentation defines an EC object in terms of `K` data chunks and `M` coding chunks, with failure-domain placement controlled separately by CRUSH. This establishes the algebraic/redundancy side of the object.

The BlueStore/deep-scrub requirement adds another relation: a fragment can belong to the correct EC geometry yet still require local integrity verification.

**Primary anchor:** `doc/rados/operations/erasure-code.rst` at `v12.2.0`.

### H/P — BlueStore stores integrity metadata for data and metadata

The `v12.2.0` BlueStore configuration reference says BlueStore checksums all metadata and data written to disk. Metadata checksumming is handled by RocksDB using `crc32c`; data checksumming is performed by BlueStore and can use `crc32c`, `xxhash32`, `xxhash64`, or truncated CRC variants. The default is `crc32c`.

The document also makes the metadata cost explicit: full data checksumming increases the amount of metadata BlueStore must store/manage, and in many cases a checksum value is maintained for every 4 KiB of data.

**Primary anchor:** `ceph/ceph` tag `v12.2.0`, `doc/rados/configuration/bluestore-config-ref.rst`, section `Checksums`.

### H/P — scheduled scrub and deep scrub are distinct maintenance regimes

The `v12.2.0` OSD configuration reference describes scrubbing as an object-storage-layer integrity mechanism. Light scrubbing checks object size and attributes; deep scrubbing fully reads data and uses checksums. The same section exposes scheduling and load controls: minimum/maximum scrub intervals, a separate deep-scrub interval, maximum simultaneous scrubs, time windows, load thresholds, sleeps, and priorities.

This makes integrity verification real background work competing with ordinary service, not a zero-cost property of having stored checksums.

**Primary anchor:** `ceph/ceph` tag `v12.2.0`, `doc/rados/configuration/osd-config-ref.rst`, section `Scrubbing`.

### H/P — 12.2.6 shows checksum metadata itself can be wrong

Ceph's official `v12.2.7` release notice, dated 17 July 2018, records a serious regression in `v12.2.6`. An incomplete backport of a BlueStore optimization intended to avoid maintaining both a per-object checksum and BlueStore's internal checksum failed to update the stored per-object checksum for some objects. The release note states that this could produce `EIO` when trying to read affected objects.

This is a crucial negative example: a checksum mismatch in this release family did not necessarily establish that the underlying object payload had suffered media corruption. The retained integrity metadata could itself be stale/inconsistent because software failed to maintain it.

**Primary anchor:** official Ceph `12.2.7 Luminous released` notice, `Upgrading from v12.2.6`.

### H/P — trust can be withdrawn from integrity metadata

The `v12.2.8` release notice, dated 4 September 2018, says `12.2.7` introduced a workaround option `osd distrust data digest = true` for clusters exposed to the regression. The name itself records an operational state in which a normally useful integrity datum is intentionally denied ordinary authority.

The source does not license the project to generalize this exact option into all later Ceph versions. It is used only as a release-bounded witness that **verification metadata can require its own trust/currentness qualification**.

**Primary anchor:** official Ceph `v12.2.8 released` notice.

### H/P — deep scrub can repair integrity-state inconsistency

The same `v12.2.8` notice says deep-scrub code was improved to automatically repair these inconsistencies. Operators were told to upgrade the entire cluster, fully deep scrub it, resolve the inconsistencies, and only then disable `osd distrust data digest = true`.

The maintenance sequence is therefore not merely `detect bad user bytes → reconstruct bytes`. In this bounded incident, a full-cluster deep-scrub pass was part of restoring the **trustworthiness of the integrity relation itself**.

**Primary anchor:** official Ceph `v12.2.8 released` notice.

---

## Retained state

The bounded regime retains more than the logical object payload:

1. **EC data/coding chunks** — the material contributions from which an object can be decoded;
2. **placement relation** — which OSD/failure domain is responsible for each chunk;
3. **BlueStore data checksums** — local integrity metadata associated with stored extents/blocks;
4. **BlueStore/RocksDB metadata checksums** — integrity state protecting storage metadata;
5. **PG/object metadata used during scrub** — enough distributed state to compare expected and observed object/shard conditions;
6. **scrub scheduling/progress state** — operational machinery deciding when verification work is actually exercised;
7. **software-version/trust regime** — during the 12.2.6–12.2.8 incident, whether stored per-object digests may be treated as authoritative becomes release- and repair-state-dependent.

The last item is deliberately narrow. It does not mean every integrity system needs an explicit `trust bit`; it means this historical incident demonstrates that the usefulness of retained verification metadata depends on the correctness of the mechanism that maintains it.

---

## Retention mechanism

### Coded survival

`K+M` EC chunks determine which loss patterns remain algebraically recoverable under the chosen profile and placement rules.

### Local integrity qualification

BlueStore retains checksums with stored data/metadata. Deep scrub exercises those relations by reading data and checking integrity rather than inferring correctness from fragment presence alone.

### Periodic verification

Scrub/deep-scrub work is scheduled and throttled. Integrity may therefore be physically endangered before verification discovers the problem; the verification interval is part of the exposure window.

### Integrity-metadata repair

The 2018 regression shows an exceptional reverse direction: instead of checksum metadata exposing bad payload, payload/storage state could coexist with a bad stored digest. The system temporarily withdrew trust from that digest and later used a full deep-scrub pass to repair inconsistent verification state.

---

## Addressing and access geometry

The relevant bounded path is not just:

```text
logical object
    -> K+M chunks
    -> decode
```

It is closer to:

```text
logical object
    -> EC profile / chunk index / CRUSH placement
    -> stored BlueStore extent
    -> retained checksum relation
    -> ordinary access and/or scheduled deep scrub
    -> integrity-qualified chunk
       OR mismatch / inconsistency
    -> repair / distrust / requalification path
```

The exact Luminous EC reconstruction algorithm after every scrub-detected error is **not established by the sources used here** and is therefore not reconstructed beyond this boundary.

---

## Read / write / overwrite semantics

The bounded 2017 transition matters because EC pools previously emphasized full-object writes/appends, while Luminous made partial overwrites available for RBD/CephFS on BlueStore. Mutation increases the importance of maintaining integrity metadata correctly through changes to coded/storage state.

The 12.2.6 incident is direct evidence of that maintenance burden: failure to update a stored checksum value can make later reads fail even when the diagnostic relation, rather than simply the user payload, is what became inconsistent.

This case does not claim that every `EIO` in affected releases was harmless or that no data corruption existed. It claims only what the release notes establish: at least some failures arose from a checksum-maintenance regression.

---

## Time, maintenance, and labor

Relevant timescales include:

- immediate write/overwrite maintenance of data plus integrity metadata;
- ordinary read-time interaction with storage checks;
- daily-ish light-scrub defaults in the bounded documentation;
- weekly-ish deep-scrub defaults;
- cluster load/time-window delays before a scrub is run;
- incident-scale periods during which an operator must upgrade, distrust affected digests, fully deep scrub, and wait until inconsistencies are resolved.

Scrub consumes resources. Luminous exposes concurrency, priority, load threshold, interval, sleep, and recovery-interaction knobs. This is operational evidence that integrity retention is sustained by scheduled background work with a service budget.

---

## Failure / forgetting modes

Keep distinct:

- loss of too many EC chunks for the configured code;
- correct-version chunk whose local stored bytes are corrupt;
- checksum/integrity metadata that is stale or wrong;
- mismatch whose cause is payload corruption;
- mismatch whose cause is integrity-metadata inconsistency;
- scrub that has not yet exercised a latent defect;
- scrub delayed/throttled by cluster conditions;
- insufficient surviving trustworthy chunks for later reconstruction;
- software-version regression that changes the meaning/trustworthiness of stored control state;
- operator disabling distrust before the prescribed full deep-scrub repair cycle has completed.

The final item follows the explicit upgrade sequence in the 12.2.8 notice; it is not a claim about all Ceph repair procedures.

---

## Engineering reconstruction

### E — coded recoverability ≠ integrity-qualified recoverability

An EC profile can say how many missing chunks are tolerable, but that algebra assumes the participating survivors are suitable inputs. BlueStore checksum/deep-scrub machinery exists because physical presence and index membership do not prove that a surviving chunk is good.

### E — checksum presence ≠ checksum authority

Normally the checksum relation qualifies stored data. The 12.2.6 incident reverses the direction of suspicion: the stored checksum can itself become the untrustworthy state. The 12.2.7 `distrust` workaround makes that loss of authority explicit.

### E — checksum mismatch ≠ universal proof of payload corruption

A mismatch establishes an inconsistency in the checked relation. Determining which side is wrong may depend on additional implementation/version knowledge. The Luminous regression is a concrete counterexample to the shortcut `mismatch = bad payload`.

### E — verification state is maintained state

Checksums are not timeless mathematical facts attached to data from outside the system. They are stored, updated, read, compared, and sometimes repaired. Their ability to certify later data therefore depends on the correctness of maintenance paths.

### E — verified repair margin is weaker than nominal EC margin

A code may nominally tolerate `M` lost chunks while hidden corruption or untrusted integrity metadata has already reduced confidence in the surviving repair set. Deep scrub is one mechanism for converting nominal redundancy into more strongly qualified redundancy.

### E — full verification coverage can itself be a repair milestone

The 12.2.8 instruction to fully deep scrub before disabling the distrust workaround makes **verification coverage** part of the system's return-to-trust process. The bytes, the stored digests, and the fact that the relevant population has been rechecked are distinct pieces of operational state.

---

## Functional analogies and limits

### A — Case 18 ZFS scrub

Both make proactive checksum verification explicit and resource-bearing. ZFS Case 18 focuses on latent media/data corruption and conditional self-healing. Case 27 adds a different counterexample: integrity metadata itself can be the inconsistent state. `scrub detects corruption` is therefore too coarse for a universal model.

### A — Case 26 GFS integrity verification

GFS separates version currentness from local checksum validity under replication. Ceph Luminous adds erasure-coded fragments, mutable overwrites, storage-backend checksums, and a later failure in checksum maintenance. Both show `copy/fragment present ≠ integrity-qualified repair source`.

### A — Cases 19, 24, 25 coded storage

- f4: code algebra versus failure-domain placement and repair completion;
- WAS LRC: recoverability versus repair cost and representation handoff;
- Swift EC: version-coherent committed fragment cohort;
- Ceph Luminous here: local fragment/storage integrity qualification and the fallibility of that qualification metadata.

These are complementary relations, not one universal EC protocol.

### A — Case 05 early RADOS

Both belong to Ceph/RADOS history, but Case 05 is bounded to 2006–2007 replicated currentness/peering/commit semantics. Case 27 is a 2017–2018 BlueStore + EC-overwrite + deep-scrub integrity case. The shared project name is not permission to collapse a decade of semantic evolution.

---

## Prior-art and terminology boundary

Case 26 already documents a 2003 GFS functional precedent for proactive background integrity verification under the phrase `scan and verify`; Case 18 records a 2004 direct `disk scrubbing` terminology anchor. Within Ceph itself, the September–October 2012 source/release record now establishes replicated `deep scrub` years before Luminous. Reed–Solomon and distributed EC prior art remain controlled in Cases 19 and 24.

The resulting historical ladder is deliberately non-genealogical: **GFS 2003 distributed verification ≠ 2004 disk-scrubbing prior art ≠ Ceph 2012 replicated deep scrub ≠ Luminous 2017–2018 BlueStore/EC integrity authority.** Chronology and functional resemblance alone do not prove direct inheritance.

Therefore this case makes **no invention-priority claim** for Ceph. Its contribution is narrower:

> a release-specific production system ties mutable erasure-coded overwrites to checksummed storage and deep scrub, then supplies a concrete operational counterexample in which retained integrity metadata itself becomes inconsistent and must be distrusted/repaired.

---

## Philosophical interpretation

The exact technical pressure is that a retained state may require another retained state to certify it, while that certificate is itself historically produced, mutable, fallible, and repairable.

This sharpens one repository-wide claim: persistence is not only `bytes continue to exist`. It can depend on a chain of qualified relations whose authority is maintained over time. The interpretation stops there. No philosophical vocabulary is attributed to Ceph developers or release authors.

---

## Counterexamples / limits

This case does **not** establish that checksums are cryptographic authentication; that CRC32C detects every corruption; that every deep scrub repairs every EC error; that a checksum mismatch always means payload corruption; that a checksum mismatch never means payload corruption; that the 12.2.6 regression affected every object; that `osd distrust data digest` is a timeless Ceph concept; that later Ceph repair semantics are identical to Luminous; or that Ceph invented EC overwrites, checksums, or scrubbing.

Most importantly, the present source set does **not** fully ground the exact per-shard reconstruction/authoritative-source algorithm used after every deep-scrub-detected EC corruption. That remains a separate implementation-archeology slice.

The 2012 compatibility path adds another limit: **`deep-scrub requested ≠ every replica content-qualified`** when some OSDs do not support deep scrub. This is a rolling-capability boundary for that implementation, not a claim about modern homogeneous clusters. Likewise, matching `crc32` values are error-detection evidence inside the comparison protocol, not cryptographic authentication or proof that every physical failure mode has been excluded.

---

## Claim ledger

| Claim | Label | Evidence / status |
| --- | --- | --- |
| Luminous made BlueStore stable/default and EC overwrites fully supported | H/P | official `v12.2.0` release note |
| `allow_ec_overwrites` is BlueStore-only because BlueStore checksumming supports deep scrub corruption detection | H/P | `v12.2.0` release note + tag-matched `erasure-code.rst` |
| BlueStore checksums all data/metadata written to disk and stores checksum metadata | H/P | `v12.2.0` `bluestore-config-ref.rst` |
| light scrub and deep scrub are distinct; deep scrub reads data and uses checksums | H/P | `v12.2.0` `osd-config-ref.rst` |
| scrub work is scheduled/throttled/resource-limited | H/P | same config reference |
| 12.2.6 could fail to update stored per-object checksum values and produce EIO | H/P | official `12.2.7` release notice |
| 12.2.7 introduced `osd distrust data digest = true` workaround | H/P | official `12.2.8` release notice |
| 12.2.8 improved deep scrub to automatically repair these checksum inconsistencies | H/P | official `12.2.8` release notice |
| coded recoverability ≠ integrity-qualified recoverability | E | reconstruction from EC + checksum/deep-scrub sources |
| checksum presence ≠ checksum authority | E | 12.2.6–12.2.8 incident |
| checksum mismatch ≠ universal proof of payload corruption | E | bounded counterexample from failed checksum maintenance |
| Ceph Luminous deep scrub is functionally comparable to ZFS/GFS proactive verification but not the same historical mechanism | A | Cases 18, 26, 27 |

---

## Sources

### Primary / system-primary

Ceph Project primary source history, **deep scrub introduction**, 5 September–16 October 2012.

- implementation commit: <https://github.com/ceph/ceph/commit/9013efd3a3cf92d1ec8e2a39639214792067d0d2>
- command/documentation commit: <https://github.com/ceph/ceph/commit/3fd5914cf35829c3f2e9e5c0a548fae0862732aa>
- `v0.53 released`: <https://www.ceph.io/en/news/blog/2012/v0-53-released/>

Ceph Project, **`v12.2.0 Luminous Released`**, 29 August 2017.

- <https://ceph.com/releases/v12-2-0-luminous-released/>

Ceph source tree, tag **`v12.2.0`**:

- `doc/rados/operations/erasure-code.rst`: <https://github.com/ceph/ceph/blob/v12.2.0/doc/rados/operations/erasure-code.rst>
- `doc/rados/configuration/bluestore-config-ref.rst`: <https://github.com/ceph/ceph/blob/v12.2.0/doc/rados/configuration/bluestore-config-ref.rst>
- `doc/rados/configuration/osd-config-ref.rst`: <https://github.com/ceph/ceph/blob/v12.2.0/doc/rados/configuration/osd-config-ref.rst>

Ceph Project, **`12.2.7 Luminous released`**, 17 July 2018.

- <https://ceph.io/en/news/blog/2018/12-2-7-luminous-released/>

Ceph Project, **`v12.2.8 released`**, 4 September 2018.

- <https://ceph.io/en/news/blog/2018/v12-2-8-released/>

### Repository controls

- [`cases/05-rados-replicated-object-repair.md`](05-rados-replicated-object-repair.md) — early RADOS currentness/replication boundary.
- [`cases/18-zfs-scrub-latent-error-detection.md`](18-zfs-scrub-latent-error-detection.md) — named scrub / latent-error comparison.
- [`cases/19-facebook-f4-erasure-coded-failure-domains.md`](19-facebook-f4-erasure-coded-failure-domains.md) — distributed EC placement/rebuild comparison.
- [`cases/25-openstack-swift-ec-overwrite-durable-currentness.md`](25-openstack-swift-ec-overwrite-durable-currentness.md) — mutable EC currentness/commit comparison.
- [`cases/26-google-gfs-inactive-chunk-integrity.md`](26-google-gfs-inactive-chunk-integrity.md) — replicated distributed integrity comparison.

### Related-repository duplication check

`tmzncty/computing-archaeology` was searched for `Ceph`, `BlueStore`, `deep scrub`, `erasure coding`, and checksum-focused matches; no dedicated matching case was found in this slice. A broad BlueStore/Ceph architectural history should still live there if developed later.

---

## Status

**`grounded`**

Grounding basis: exact Ceph Luminous release dates; tag-matched `v12.2.0` source documentation for EC overwrites, BlueStore checksum semantics, and scrub scheduling; official 2018 incident/correction records that expose checksum metadata as fallible retained state; explicit source and terminology boundaries; related-repository duplication check; and separation of historical record, engineering reconstruction, functional analogy, and philosophical interpretation.
