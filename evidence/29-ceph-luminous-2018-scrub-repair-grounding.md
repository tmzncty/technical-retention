# Case 29 Grounding Record — Ceph Luminous Scrub Authority and EC Repair Path (2018)

## Promotion target

This record grounds [`cases/29-ceph-luminous-ec-scrub-authoritative-repair.md`](../cases/29-ceph-luminous-ec-scrub-authoritative-repair.md).

The bounded claim is:

> In Ceph Luminous `v12.2.8`, scrub repair does not equate mismatch with immediate decode. The scrub backend filters shard candidates using read/stat/EC-hash/size/ObjectInfo/HashInfo evidence, selects operational object-info authority, constructs an authoritative candidate set, and records missing/inconsistent peers. Repair mode then marks the bad shard/object missing and records candidate locations. The EC backend separately filters available/non-error/non-missing shard indexes, asks the code for a `minimum_to_decode` set, and reconstructs the missing shard.

Status target: **`grounded`**.

---

## Evidence classes

### P1 — tag-matched Luminous scrub backend source

Repository: `ceph/ceph`

Tag: `v12.2.8`

File: `src/osd/PGBackend.cc`

Blob SHA inspected through GitHub: `f77b8bfad933203c9c3d3e6520f988f90c3f069e`

Functions directly inspected:

- `PGBackend::be_select_auth_object()`;
- `PGBackend::be_compare_scrubmaps()`;
- helper `dcount()`;
- `PGBackend::be_compare_scrub_objects()` where relevant to error classification.

### P2 — tag-matched PG scrub/repair orchestration source

Repository: `ceph/ceph`

Tag: `v12.2.8`

File: `src/osd/PG.cc`

Blob SHA inspected through GitHub: `9e45796b89a77c523afd77409827d203dd2e3f47`

Functions directly inspected:

- `PG::scrub_compare_maps()`;
- `PG::scrub_process_inconsistent()`;
- `PG::repair_object()`.

### P3 — tag-matched EC recovery source

Repository: `ceph/ceph`

Tag: `v12.2.8`

File: `src/osd/ECBackend.cc`

Blob SHA inspected through GitHub: `23e5a50f0166ceb891f11e602ea81503f0412307`

Functions/paths directly inspected:

- `ECBackend::get_all_avail_shards()`;
- `ECBackend::get_min_avail_to_read_shards()`;
- remaining-shard retry logic after read errors;
- `ECBackend::handle_recovery_read_complete()`;
- recovery-op missing-shard bookkeeping.

### P4 — release/version boundary reused from Case 27

Case 27 already grounds the official Ceph `v12.2.8` release record and its 4 September 2018 correction context. This slice reuses that release boundary rather than creating a duplicate release-note history. The present evidence claim depends primarily on the tag-matched source implementation above.

---

## Direct source ledger

### 1. `PGBackend::be_select_auth_object()` — candidate ordering and exclusion

Directly established in `v12.2.8`:

- the function constructs a shard list with the primary first;
- the source comment explains this is so the primary becomes auth **all other things being equal**;
- per-shard scrub state records `read_error`, `ec_hash_mismatch`, `ec_size_mismatch`, and `stat_error`;
- for EC pools it requires the `ECUtil::HashInfo` attribute to be present/decodable and records cross-shard inconsistency;
- it requires `OI_ATTR` object information to be present and decodable;
- it records object-info and object-size inconsistencies;
- after these checks, `if (shard_info.errors) goto out;` is preceded by the comment `Don't use this particular shard due to previous errors`;
- eligible candidates are ranked by `oi.version`, then by `dcount(...)` at equal version;
- because the primary is scanned first and replacement requires a strict `>` ranking, equal candidates leave the primary selected.

Evidence use:

- physical presence is insufficient for scrub repair-source eligibility;
- primary status is a tie preference, not unconditional truth authority;
- ObjectInfo/version plus structural/integrity error state are retained inputs to repair-source selection.

### 2. `dcount()` / digest-distrust branch — exact scope boundary

Directly established:

- `dcount()` increments for retained `data_digest` and `omap_digest` fields;
- an additional 1000-point prioritization can be applied when `prioritize` is true;
- the source comment says this prioritizes BlueStore/builtin-checksum objects when `osd_distrust_data_digest` is set;
- however the branch that sets this priority is explicitly guarded by `parent->get_pool().is_replicated()`.

Evidence use:

- the 12.2.7/12.2.8 digest-distrust incident from Case 27 must not be silently turned into the EC auth-selection rule here;
- source-level version archaeology can narrow a claim that release notes alone leave broader.

### 3. `be_compare_scrubmaps()` — candidate authority list, missing/inconsistent state, and uncertainty

Directly established:

- `be_select_auth_object()` is called first for each object;
- failure to choose a suitable ObjectInfo produces an explicit `failed to pick suitable object info` error;
- each shard is compared with the auth object/object-info;
- shard-specific errors populate `cur_inconsistent`;
- absent objects populate `cur_missing`;
- shards without the relevant error path are appended to `auth_list`;
- object-level errors that cannot immediately be assigned to one shard populate an intermediate `object_errors` set;
- if `auth_list` is empty but object-level-error candidates remain, the code prefers the selected auth shard if possible, otherwise the first remaining candidate, and marks the others inconsistent;
- the source comment explicitly says: `The auth shard might get here that we don't know that it has the "correct" data.`;
- when missing/inconsistent peers exist, the candidate list is exported through `authoritative[*k] = auth_list`.

Evidence use:

- operational repair authority is evidence-conditioned rather than guaranteed correctness;
- the system retains both positive candidate-source relations and negative missing/inconsistent relations;
- fallback under ambiguity is part of the period implementation and must remain visible in the case boundary.

### 4. `PG::scrub_compare_maps()` — materializing the candidate relation

Directly established:

- `PG::scrub_compare_maps()` asks the backend to fill `missing`, `inconsistent`, and `authoritative` maps;
- for each object in `authoritative`, it builds a list of `(ScrubMap::object, pg_shard_t)` `good_peers`;
- it stores that list in `scrubber.authoritative`.

Evidence use:

- the source relation is not merely a local temporary comparison result; it is passed into the PG's repair orchestration state.

### 5. `PG::scrub_process_inconsistent()` — diagnosis and repair invocation are distinct

Directly established:

- the source comment says authoritative state stores objects that are missing or inconsistent;
- in repair mode, the code iterates `scrubber.authoritative`;
- for each missing bad peer it calls `repair_object(object, ok_peers, bad_peer)`;
- it does the same for each inconsistent bad peer;
- a `fixed` counter is incremented after these calls.

Evidence use / limit:

- scrub diagnosis produces repair work;
- the `fixed` increment is **not** used as proof that reconstructed bytes already exist, because `repair_object()` and ECBackend show later recovery stages.

### 6. `PG::repair_object()` — scrub error becomes missing-state

Directly established:

- `repair_object()` receives the candidate `ok_peers` list and a `bad_peer`;
- it takes ObjectInfo from one of the candidate scrub-map objects and decodes the object's version;
- for a non-primary bad peer it adds that object/version to `peer_missing[bad_peer]`;
- for a bad primary it adds the object/version to the local `pg_log.missing` state;
- if the PG is EC (or the primary is bad), it calls `missing_loc.add_missing(...)`;
- for every candidate `ok_peers` shard it calls `missing_loc.add_location(...)`.

Evidence use:

- a present-but-inconsistent shard can be transformed into ordinary **missing** recovery state;
- the candidate repair-source relation is retained as locations for subsequent recovery;
- integrity diagnosis and the recovery state machine are joined by explicit metadata mutation, not by an implicit conceptual leap.

### 7. `ECBackend::get_all_avail_shards()` — missing/error state constrains code inputs

Directly established:

- acting shards are inspected through each shard's PG missing map;
- shards in an `error_shards` set are skipped;
- shards where the object is marked missing are not inserted into `have`;
- recovery can also consider suitable backfill and `missing_loc` shards, again excluding reported error shards.

Evidence use:

- physical existence or membership in the acting set is not enough to be a decode source;
- retained negative knowledge (`missing`, errors) actively removes possible inputs.

### 8. `minimum_to_decode()` — codec sufficiency is a later, separate selection

Directly established:

- `get_min_avail_to_read_shards()` first calls `get_all_avail_shards()`;
- it then calls `ec_impl->minimum_to_decode(want, have, &need)`;
- recovery mode explicitly disables redundant reads in this helper (`assert(!for_recovery || !do_redundant_reads)`);
- if read results later contain errors, the retry path converts those sources to `error_shards`, rebuilds the available set, and again calls `minimum_to_decode`;
- when no sufficient remaining set exists, the path returns `-EIO`.

Evidence use:

- the scrub `auth_list` / candidate-locations set is not the same thing as the codec's eventual minimum input set;
- source selection can change after new read-time failure evidence;
- coding sufficiency is evaluated after currentness/integrity/availability filtering rather than replacing it.

### 9. `handle_recovery_read_complete()` — actual reconstruction follows source qualification

Directly established:

- recovery tracks `missing_on_shards`;
- returned data are organized by source shard index;
- target buffers are prepared for the missing shard indexes;
- `ECUtil::decode(sinfo, ec_impl, from, target)` reconstructs the requested missing contributions;
- subsequent recovery code installs/completes the repaired object/shard state.

Evidence use:

- `repair_object()` is an authorization/bookkeeping transition, not the final reconstruction operation;
- the source path supports the sequence `diagnosis → missing-state → source selection → decode`.

---

## Source-inspection boundary

All three implementation files were read directly from the `ceph/ceph` `v12.2.8` tag through GitHub, not from today's `main` documentation. The recorded blob SHAs above fix the inspected text.

This is source-level implementation evidence. It is stronger for exact program behavior than a later operator tutorial, but it has its own limits:

- no claim is made that every possible runtime interleaving has been experimentally reproduced;
- no claim is made that later Ceph refactors preserve the same function boundaries or ranking rules;
- no claim is made that variable name `authoritative` establishes objective correctness;
- no claim is made that the inspected `osd_distrust_data_digest` preference applies to EC, because the source explicitly gates that branch to replicated pools;
- no claim is made that every `ceph pg repair` invocation necessarily completes successfully after this path starts.

No PDF/facsimile assertion is involved in this slice.

---

## Historical / engineering boundary

### Historical record

Historical claims are limited to what the `v12.2.8` source does and calls things:

- `auth`, `auth_list`, `authoritative`;
- `missing`, `inconsistent`, `missing_loc`;
- error flags and ObjectInfo/HashInfo checks;
- `repair_object`;
- `minimum_to_decode`;
- actual branching/ranking/order in those functions.

### Engineering reconstruction

The following are project descriptions, not period Ceph terminology:

- `evidence-conditioned repair authority`;
- `scrub-authority set ≠ decode set`;
- `missing-state injection`;
- `repair-source admissibility`;
- `operational authority ≠ certainty`.

### Functional analogy

Comparisons to GFS, f4, WAS LRC, Swift EC, ZFS, or later Ceph are functional comparisons only. Shared words such as `repair`, `scrub`, `valid`, or `authoritative` do not prove mechanism identity.

### Philosophical interpretation

The narrow interpretive claim is that retention can depend on retained relations that disqualify some surviving embodiments and authorize others as sources of reconstitution. No philosophical concept is attributed to the Ceph implementation.

---

## Prior-art boundary

No invention-priority claim is made.

- Case 18 already records scrub terminology/prior art;
- Case 26 already supplies an earlier production example of checksum-qualified replica repair;
- Cases 19 and 24 already control Reed–Solomon/LRC coding-history boundaries;
- Case 05 already covers the much earlier RADOS peering/currentness regime;
- Case 27 already covers the Luminous checksum/deep-scrub and digest-authority incident.

The novelty of this repository slice is not historical invention. It is the **retention-specific decomposition of a directly inspected 2018 implementation path** from scrub evidence to repair authority to missing-state to EC decode.

---

## Cross-case controls

### Case 27 — same release family, different question

Case 27: can checksum/integrity metadata itself lose authority, and what verification work restores trust?

Case 29: given the scrub-map evidence path, how are usable repair candidates selected, how is the bad shard reclassified into recovery state, and how does the EC layer later choose a sufficient decode set?

Required distinction: the replicated-only `osd_distrust_data_digest` priority branch must not be projected as the EC authority-selection rule.

### Case 26 — GFS

Shared function: existing physical copies/fragments are not automatically valid repair sources.

Required distinction: GFS clones a full valid replica; Ceph EC can require several shard indexes selected after scrub/missing/error filtering and a code-specific `minimum_to_decode` calculation.

### Cases 19 / 24 — f4 and WAS LRC

Shared function: coded recovery can precede full redundancy restoration and depends on source geometry.

Required distinction: Case 29 is specifically about **integrity-conditioned source authority** and conversion of a scrub inconsistency into ordinary EC recovery bookkeeping.

### Case 25 — Swift EC

Shared function: EC needs more retained relations than parity/data bytes.

Required distinction: Swift's bounded case qualifies a version-coherent committed fragment cohort; Ceph's bounded case qualifies repair candidates inside a scrub/recovery path. Cohort admissibility and repair authority are not one protocol.

---

## Related-repository check

`tmzncty/computing-archaeology` was searched for combinations of `Ceph`, `BlueStore`, `scrub`, `authoritative`, `ECBackend`, and `PGBackend`. No dedicated matching case was found during this slice.

Therefore no existing technical-history treatment was copied. If a broader source-level Ceph implementation history is later developed, it should primarily live in `computing-archaeology`; `technical-retention` should preserve only this retention-specific comparison.

---

## Evidence maturity

**`grounded`** is justified because:

1. the entire central mechanism is directly anchored in the exact `v12.2.8` project source tag;
2. the path crosses three independently inspectable implementation layers — scrub backend, PG orchestration, and EC recovery;
3. the source exposes both positive selection rules and explicit uncertainty/fallback language;
4. the key negative boundary (`osd_distrust_data_digest` prioritization is replicated-only here) is checked in code rather than assumed from release notes;
5. the repair handoff is visible as concrete mutation of missing/location state;
6. the EC backend independently shows filtering plus `minimum_to_decode` and reconstruction;
7. related-repository duplication was checked;
8. unsupported stronger claims are explicitly rejected.

Remaining work is separate rather than a blocker: later Ceph scrub-backend refactors and auto-repair policy, operator-visible behavior under particular failure matrices, experimental reproduction, and cross-version continuity from Luminous to modern releases.
