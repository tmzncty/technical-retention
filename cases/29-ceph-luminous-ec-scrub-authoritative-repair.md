# Ceph Luminous Scrub Repair: Authoritative-Shard Selection, Missing-State Injection, and EC Reconstruction

## Scope

- **Bounded system:** Ceph Luminous `v12.2.8` source tree, released in September 2018.
- **Bounded mechanism:** the source-level path from PG scrub comparison, through selection of an `auth` / `authoritative` candidate set, to repair-mode conversion of a bad or missing shard into PG missing-state and erasure-code reconstruction work.
- **Research question:** after scrub has found disagreement in an erasure-coded object, what retained relations let Ceph decide which surviving state may be used for repair, turn an integrity diagnosis into recovery work, and choose a sufficient decode set?

This is a deliberately narrow implementation-archaeology continuation of Case 27. Case 27 established that Luminous mutable EC depends on BlueStore checksums/deep scrub and that integrity metadata can itself become untrustworthy. It explicitly left the exact per-shard repair path ungrounded. The present case closes that bounded gap without becoming a general Ceph recovery history.

The bounded retention claim is:

> **Luminous repair does not jump directly from `scrub mismatch` to `decode`. The scrub backend first excludes shards carrying particular structural/read/integrity errors, chooses usable object-info authority under explicit ranking rules, constructs an authoritative candidate list, and records missing/inconsistent peers. Repair mode then injects the diagnosed bad shard into the ordinary PG missing-state machinery and records candidate source locations. Only after that filtering does the EC backend ask the code for a `minimum_to_decode` set and reconstruct the missing shard.**

`evidence-conditioned repair authority`, `missing-state injection`, `repair-source admissibility`, and `scrub-authority set` below are **project engineering terms**, not historical Ceph vocabulary.

---

## Historical vocabulary

The inspected `v12.2.8` source directly uses:

- `auth` / `auth object` / `authoritative`;
- `auth_list`;
- `missing`;
- `inconsistent`;
- `repair` / `repair_object`;
- `read_error`;
- `ec_hash_mismatch`;
- `ec_size_mismatch`;
- `stat_error`;
- `hinfo_key_missing`, `hinfo_corrupted`, `hinfo_inconsistency`;
- `info_missing`, `info_corrupted`, `object_info_inconsistency`;
- `missing_loc`;
- `missing_on` / `missing_on_shards`;
- `minimum_to_decode`;
- `error_shards`.

The project terms above must not be substituted into historical quotations as if they were Ceph developers' own conceptual vocabulary.

---

## Historical record

### H/P — scrub authority is selected from inspected shard state, not assumed from physical presence

In `src/osd/PGBackend.cc`, `be_select_auth_object()` builds a shard list with the primary first, explicitly so that it will become the auth copy **all other things being equal**. It then inspects each shard's scrub-map object.

The function records and reacts to several conditions before a shard can serve as the selected authority:

- `read_error`;
- `ec_hash_mismatch`;
- `ec_size_mismatch`;
- `stat_error`;
- for EC pools, missing/corrupt/inconsistent `ECUtil::HashInfo`;
- missing or undecodable `OI_ATTR` / object information;
- object-info and size inconsistencies.

After these checks, the code states: `Don't use this particular shard due to previous errors`; a shard with `shard_info.errors` is skipped for auth selection.

**Primary anchor:** `ceph/ceph` tag `v12.2.8`, `src/osd/PGBackend.cc`, `PGBackend::be_select_auth_object()`.

### H/P — among eligible candidates, object version outranks topology; primary is only a tie preference

For shards that survive the exclusion path, `be_select_auth_object()` prefers a higher `object_info_t::version`. At equal version it uses `dcount()` as a tiebreaker; in the ordinary bounded path this counts recorded data/omap digest fields. Because the primary is scanned first, it remains selected when later candidates do not outrank it.

This is not a rule that "the primary is always correct." The primary preference is explicitly conditional on other things being equal, and error-marked primary state can be skipped.

A separate `osd_distrust_data_digest` preference for a backend with built-in checksums is guarded by `parent->get_pool().is_replicated()`. It therefore must **not** be projected into this bounded EC repair path.

**Primary anchor:** `PGBackend.cc`, `dcount()` and `be_select_auth_object()` at tag `v12.2.8`.

### H/P — scrub comparison constructs a candidate authority list and preserves uncertainty

`be_compare_scrubmaps()` compares every shard's scrub-map object against the selected auth object/object-info and sorts outcomes into missing, inconsistent, object-level error, or candidate-authoritative states.

A shard without the relevant error indications is appended to `auth_list`. If there are missing or inconsistent peers, that list is exported through `authoritative[*k]`.

The implementation contains an unusually useful warning comment: **`The auth shard might get here that we don't know that it has the "correct" data.`** If `auth_list` is empty but there are unresolved object-level errors, the code falls back to the selected auth shard when possible, otherwise to the first remaining candidate, and treats the other candidates as inconsistent.

That comment is direct period-source evidence against a stronger epistemic claim. In this implementation, `authoritative` is an operational repair role selected under available checks, not a proof of metaphysical or cryptographic certainty.

**Primary anchor:** `PGBackend.cc`, `PGBackend::be_compare_scrubmaps()` at `v12.2.8`.

### H/P — PG materializes the authoritative candidates and invokes repair only for missing/inconsistent objects

`PG::scrub_compare_maps()` receives the backend's `authoritative` map and materializes each candidate as a `(ScrubMap::object, pg_shard_t)` pair in `scrubber.authoritative`.

`PG::scrub_process_inconsistent()` comments that `authoritative` stores only objects that are missing or inconsistent. When the PG is in repair mode, it iterates the missing and inconsistent bad peers and calls `repair_object()` with the object plus its `ok_peers` candidate list.

**Primary anchor:** `ceph/ceph` tag `v12.2.8`, `src/osd/PG.cc`, `PG::scrub_compare_maps()` and `PG::scrub_process_inconsistent()`.

### H/P — repair converts a scrub diagnosis into PG missing-state

`PG::repair_object()` decodes `OI_ATTR` from one of the `ok_peers` to recover the object version used by recovery bookkeeping. It then marks the bad location missing:

- for a non-primary bad peer, `peer_missing[bad_peer].add(...)`;
- for a bad primary, `pg_log.missing_add(...)`.

For an EC PG, the function additionally calls `missing_loc.add_missing(...)` and adds every `ok_peers` shard as a possible location with `missing_loc.add_location(...)`.

This is a concrete transition from **scrub-diagnosed inconsistency** into the retained missing/location relations consumed by ordinary recovery.

**Primary anchor:** `src/osd/PG.cc`, `PG::repair_object()` at `v12.2.8`.

### H/P — the EC backend separately computes a sufficient decode set

In `src/osd/ECBackend.cc`, `get_all_avail_shards()` constructs the currently usable shard-index set. It excludes shards present in `error_shards` and excludes shards whose PG missing state says the object is missing. Recovery may also consider suitable backfill / `missing_loc` locations.

`get_min_avail_to_read_shards()` then calls the erasure-code implementation's `minimum_to_decode(want, have, &need)`. If later reads fail, the retry path builds `error_shards` from the failed read results, recomputes the remaining available set, and again asks `minimum_to_decode`; failure to retain enough usable shards becomes `-EIO`.

When recovery reads complete, `handle_recovery_read_complete()` gathers the returned shard buffers and calls `ECUtil::decode(...)` into the target buffers for `missing_on_shards`.

**Primary anchor:** `ceph/ceph` tag `v12.2.8`, `src/osd/ECBackend.cc`, `get_all_avail_shards()`, `get_min_avail_to_read_shards()`, the remaining-shard retry path, and `handle_recovery_read_complete()`.

---

## Retained state

The bounded repair path depends on more than EC payload fragments:

1. **per-shard stored object/shard state** exposed to the scrub map;
2. **ObjectInfo (`OI_ATTR`) and version state** used to select/identify the repair version;
3. **EC `HashInfo` state** and its consistency/decodability in the bounded scrub-selection path;
4. **per-shard scrub error state** such as read/stat/hash/size/info errors;
5. **missing and inconsistent sets** produced by scrub comparison;
6. **the `authoritative` / `auth_list` candidate relation** associating an object with acceptable repair candidates under the current comparison;
7. **PG missing maps** (`peer_missing` / local missing state) that make the failed shard an object of recovery;
8. **`missing_loc` locations** that retain where candidate source state can be found;
9. **EC shard indexes and code profile** needed by `minimum_to_decode`;
10. **recovery progress / missing-on-shard state** used while reconstructed state is being produced and installed.

These are not one undifferentiated metadata blob. Each relation answers a different question: what version, which shard is suspect, where usable inputs may live, and what subset is mathematically sufficient to reconstruct the missing contribution.

---

## Retention / repair mechanism

The bounded path can be represented as:

```text
per-shard scrub maps
    -> structural/read/integrity error classification
    -> eligible ObjectInfo candidates
    -> selected auth ObjectInfo/version
    -> compare all shards
    -> auth_list + missing/inconsistent sets
    -> repair_object(bad shard, ok_peers)
    -> bad shard recorded as missing
    -> ok_peers recorded as candidate locations
    -> ECBackend filters currently available/non-error/non-missing shard indexes
    -> minimum_to_decode(...)
    -> recovery reads
    -> ECUtil::decode(...)
    -> reconstructed missing shard installed through ordinary recovery
```

The important methodological point is that **authority selection and code sufficiency occur at different layers**. Scrub comparison asks which surviving states are operationally admissible as repair candidates; EC decoding later asks which subset of the currently available shard indexes is sufficient for the requested reconstruction.

---

## Read, repair, and completion semantics

A scrub mismatch is not itself a repaired object. `be_compare_scrubmaps()` produces diagnostic/candidate state. `repair_object()` does not directly perform the final EC decode; it changes recovery bookkeeping by marking the bad shard/object missing and exposing candidate locations. The EC backend then performs the ordinary shard selection/read/decode path.

Therefore:

> **diagnosis → repair authorization/bookkeeping → decode-source planning → reconstruction**

must not be collapsed into one event.

Likewise, the fact that `scrub_process_inconsistent()` increments its fixed counter after invoking `repair_object()` is not used here as evidence that physical reconstruction has completed at that exact instant. The source-level data path shows additional recovery work remains.

---

## Failure / forgetting modes

Keep distinct:

- a physically absent shard;
- a shard present but carrying a read/stat error;
- EC hash or size mismatch;
- missing/corrupt/inconsistent EC hash-info metadata;
- missing/corrupt/inconsistent ObjectInfo;
- a higher-version eligible candidate versus a lower-version one;
- no candidate passing the ordinary auth checks;
- an operational fallback candidate that still is not proven to contain objectively correct bytes;
- enough physical shards present but too few usable/non-error shard indexes for `minimum_to_decode`;
- repair bookkeeping established but reconstruction not yet completed;
- later read failure invalidating an initially planned decode source and forcing another source-set calculation.

Forgetting or losing any of the control relations above can reduce recoverability even when some coded bytes remain physically present.

---

## Engineering reconstruction

### E — scrub-authoritative set ≠ EC minimum decode set

`auth_list` is produced by scrub comparison and represents surviving candidates not disqualified by the current comparison/error path. `minimum_to_decode` is a later coding-layer calculation over currently available shard indexes. A larger admissible candidate set may exist even though only a subset is needed to reconstruct one target.

### E — operational authority ≠ certainty of correct payload

The source itself warns that an auth shard can reach the candidate path without the system knowing that it has the "correct" data. The bounded meaning of `authoritative` is therefore procedural: usable under the implementation's available evidence and fallback rules. It must not be upgraded into an epistemological guarantee.

### E — integrity diagnosis ≠ recovery-state transition

Scrub identifies missing/inconsistent state; `repair_object()` then records the bad location as missing and registers source locations. This retained administrative state is what makes the ordinary recovery machinery treat a previously present-but-bad shard as something that must be reconstructed.

### E — physical presence ≠ source admissibility

A shard can exist on disk yet be excluded because of read/stat/hash/size/info errors or because the PG missing relation says the object is missing there. EC algebra only acts on the filtered `have` set.

### E — source admissibility ≠ code sufficiency

Even after unsuitable sources are removed, the remaining indexes may fail `minimum_to_decode`. Conversely, a sufficiently large clean candidate population can permit several possible minimum decode sets. Integrity/currentness qualification and mathematical sufficiency are different relations.

### E — planned decode set ≠ stable decode set

The read path can encounter new errors, exclude the newly failing shards, and ask `minimum_to_decode` again. Repair source selection is therefore not necessarily a once-for-all retained list; it can be revised as access exposes new failure evidence.

### E — repair scheduling ≠ repair completion

Marking the object missing and registering source locations changes what recovery must do. It does not itself create the repaired shard. Completion requires successful reads, decoding, and installation through recovery.

### E — a present coded object can depend on retained negative knowledge

The recovery system must retain not only where good candidates may be, but also where the object is **missing or unusable**. Negative per-shard state constrains future decode choices and can be as operationally important as the surviving fragments themselves.

---

## Functional analogies and limits

### A — Case 27 Ceph Luminous checksum authority

Case 27 asks whether coded state and its integrity metadata can be trusted and documents the digest regression/requalification incident. This case begins one layer later: given scrub-map evidence, how does the `v12.2.8` implementation choose operational repair candidates and turn inconsistency into EC recovery state?

The two cases are adjacent but not interchangeable. In particular, the `osd_distrust_data_digest` source-priority branch inspected here is replicated-pool-only and must not be used to claim the exact EC authority rule that Case 27 intentionally left open.

### A — Case 26 GFS valid replicas

Both systems distinguish physically existing state from repair-source state. GFS can clone a whole chunk from another valid replica. Ceph EC repair can instead retain a candidate set and later choose a mathematically sufficient subset of shard indexes to reconstruct a missing coded contribution. `valid replica` and `minimum decode set` are functionally comparable only at the broad problem of repair-source qualification.

### A — Case 19 f4 and Case 24 WAS LRC

f4 and WAS already show that reconstructability, repair cost, and completed redundancy restoration are distinct. Case 29 adds a different relation: **who is currently admissible to participate in reconstruction after integrity comparison**, before the codec computes a sufficient set.

### A — Case 25 Swift EC

Swift Case 25 decides whether fragments form a version-coherent committed cohort. Ceph Case 29 begins from one release-specific PG/object repair context and asks which shard copies are usable as repair sources after scrub. Version admissibility and scrub repair-source authority must not be normalized into one generic "fragment quorum."

---

## Prior-art and genealogy boundary

No invention-priority claim is made for Ceph, erasure coding, scrub, repair, or source selection.

- Case 18 already controls scrubbing prior art;
- Cases 19 and 24 control Reed–Solomon/LRC coding boundaries;
- Case 26 supplies an earlier production example of integrity-qualified replica repair;
- Case 05 covers early RADOS peering/currentness rather than this 2018 scrub-repair implementation.

The contribution of this slice is source-level semantic precision within one historical release: **the exact handoff from scrub evidence to authoritative candidates, missing-state bookkeeping, and EC minimum-decode recovery**.

A search of `tmzncty/computing-archaeology` for Ceph/BlueStore/scrub/authoritative/ECBackend/PGBackend did not locate a dedicated existing case during this slice, so no technical history was duplicated. A broader Ceph implementation history should still live primarily there.

---

## Philosophical interpretation

The exact technical pressure is modest but useful: a system can preserve state only by preserving relations about **which surviving embodiments should no longer count** and **which remaining embodiments are allowed to stand in as sources for reconstitution**.

That supports a narrow interpretation of technical retention as qualified continuation rather than bare material survival. It does not license a claim that Ceph's `authoritative` variable is a philosophical theory of authority, truth, memory, or identity.

---

## Counterexamples / limits

This case does **not** establish that:

- the selected auth shard is certainly correct;
- repair uses majority voting over bytes;
- every member of `auth_list` is byte-identical;
- the primary is always authoritative;
- the `osd_distrust_data_digest` preference governs EC pools in this path;
- `minimum_to_decode` decides object currentness or integrity;
- `repair_object()` immediately completes physical repair;
- every Luminous scrub inconsistency is automatically repairable;
- later Ceph releases preserve these exact selection rules;
- the inspected code proves every operator-facing outcome of `ceph pg repair` under all configurations.

Most importantly, the code's own uncertainty comment is retained as a boundary: **operational authority is evidence-conditioned and can include fallback under ambiguity.**

---

## Claim ledger

| Claim | Label | Evidence / limit |
| --- | --- | --- |
| `be_select_auth_object()` skips shards carrying recorded selection errors | H/P | `PGBackend.cc` `v12.2.8` |
| eligible auth selection prefers higher `oi.version`; primary wins only unresolved ties from first position | H/P/E | `PGBackend.cc`; do not generalize to all Ceph releases |
| EC HashInfo/ObjectInfo decodability/consistency participate in source eligibility | H/P | `PGBackend.cc` |
| the implementation explicitly admits that an auth candidate may not be known to hold "correct" data | H/P/X | rejects `authoritative = certain truth` |
| missing/inconsistent scrub results produce an authoritative candidate list | H/P | `be_compare_scrubmaps()` |
| repair marks the bad shard/object missing and records good candidate locations | H/P | `PG.cc` `repair_object()` |
| EC recovery excludes missing/error sources before code selection | H/P | `ECBackend.cc` |
| `minimum_to_decode` chooses coding-sufficient indexes only after that filtering | H/P/E | `ECBackend.cc` |
| recovery can recalculate a source set after read errors | H/P/E | `ECBackend.cc` retry path |
| scrub authority set and decode set are distinct retained relations | E | bounded reconstruction from the source path |
| `authoritative` in this case is procedural rather than philosophical authority | E/I boundary | interpretation stops at mechanism |

---

## Status

**`grounded`**.

The central path is anchored directly in tag-matched `v12.2.8` project source across `PGBackend.cc`, `PG.cc`, and `ECBackend.cc`; the implementation itself supplies both positive rules and explicit uncertainty/counterexample comments. Broader later-Ceph automatic-repair policy, post-Luminous scrub-backend refactors, operator-visible policy evolution, and cross-version semantic continuity remain separate work.
