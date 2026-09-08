# Evidence 128 — ZFS vdev-label / uberblock restart-root grounding, 2005–2026

**Case:** [`cases/128-zfs-vdev-label-uberblock-import-root-recovery.md`](../cases/128-zfs-vdev-label-uberblock-import-root-recovery.md)

## Research question

What primary evidence supports the bounded claim that ZFS retains on-device topology and restart-root metadata separately from payload, so a pool can be rediscovered and a qualified root selected after volatile host/process state disappears?

## Evidence discipline

This record distinguishes:

- `H/P` — historical/primary source statement;
- `H/S` — institutional operational documentation;
- `E` — project engineering reconstruction;
- `A` — functional analogy;
- `X` — rejected/unsupported overclaim.

The 2005 Sun specification is the historical core. Current OpenZFS docs/source are used only to show later continuity and modern operational boundaries. No modern source is silently backdated to 2005.

## Source P1 — Sun Microsystems, ZFS On-Disk Specification, draft 2005-12-09

Stable surviving copy:

<https://www.filibeto.org/~aduritz/truetrue/solaris10/ondiskformatfinal.pdf>

Document identity visible on the title page:

- `ZFS On-Disk Specification`;
- `DRAFT: 12/9/2005`;
- Sun Microsystems, Inc.

The bounded sections inspected are Chapter One §§1.2–1.3.4 (PDF pages corresponding to printed pp. 6–14).

### P1.1 — vdev label scope

Section 1.2 states that each physical vdev contains a 256 KB vdev label and that the label describes that vdev plus related vdevs sharing the same top-level-vdev ancestor.

**Supports:** topology/configuration state is retained on member media separately from user payload. (`H/P`)

**Does not support:** every member independently contains a complete copy of every possible modern pool configuration. (`X`)

### P1.2 — four label copies and separated placement

Section 1.2.1 states that four copies are written on each physical vdev, with two at the front and two at the back. The text explicitly motivates non-contiguous placement by resilience against contiguous corruption/overwrite.

**Supports:** redundant, spatially separated control metadata. (`H/P`)

**Does not support:** arbitrary-fault tolerance or four-way payload replication. (`X`)

### P1.3 — staged label overwrite

Section 1.2.2 distinguishes fixed-location label updates from ordinary ZFS copy-on-write. It describes writing even labels first while odd labels remain valid, then updating odd labels after the even set reaches stable storage.

**Supports:** the label-update path retains an older valid subset while another subset is overwritten. (`H/P`, `E`)

**Does not support:** that no combination of media/device failure can destroy all label copies. (`X`)

### P1.4 — label composition

Section 1.3 says a label contains:

- 8 KB blank space;
- 8 KB boot-header information;
- 112 KB name/value pairs;
- 128 KB of 1 KB uberblock structures.

**Supports:** topology/configuration and restart-root candidates coexist in the label but are distinct structures. (`H/P`)

### P1.5 — configuration identity fields

Section 1.3.3 documents fields including:

- `txg` — transaction group in which the label was written;
- `pool_guid` — pool identifier;
- `top_guid` — top-level-vdev identifier;
- `guid` — vdev identifier;
- nested vdev-tree information.

**Supports:** a member carries retained relational identity/topology evidence needed to interpret it as part of a pool. (`H/P`, `E`)

**Does not support:** the label is a complete operation/configuration history. (`X`)

### P1.6 — active uberblock qualification

Section 1.3.4 says the uberblock contains information necessary to access pool contents and, in this bounded 2005 description, defines the active uberblock by highest transaction-group number plus a valid SHA-256 checksum.

**Supports:** root currentness is a qualified selection relation among retained candidates. (`H/P`, `E`)

**Does not support:** `highest txg` as a complete description of every later OpenZFS import/MMP decision. (`X`)

### P1.7 — uberblock is rotated, not uniquely overwritten

The same section says the active uberblock is never overwritten; a modified uberblock is written to another uberblock-array element, with transaction number/timestamp advanced, and writes occur round-robin across pool vdevs.

**Supports:** several physically surviving root candidates can coexist while one is current. (`H/P`, `E`)

**Does not support:** every older candidate is a supported user snapshot or safe arbitrary rollback point. (`X`)

### P1.8 — `ub_rootbp` and `ub_guid_sum`

Section 1.3.4 identifies `ub_rootbp` as the block pointer locating the MOS. It also describes `ub_guid_sum` as an availability check against encountered leaf-vdev GUIDs during pool open.

**Supports:** restart requires both a root into the object graph and enough member/topology evidence to qualify the pool. (`H/P`, `E`)

## Source P2 — OpenZFS current Copy-on-Write documentation

<https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Copy-on-write.html>

The current documentation states that:

- the pool is a tree whose root is the uberblock;
- changed blocks/parents are written copy-on-write and the new uberblock is written last;
- each device carries four label copies;
- each label carries a 128 KiB uberblock ring;
- import chooses a valid uberblock with the highest transaction number;
- unfinished asynchronous txgs can be lost while the pool returns at the last committed state.

**Classification:** `H/P` as current project documentation, not 2005 evidence.

**Use:** later continuity and a compact modern operational explanation.

**Boundary:** current documentation is explanatory and cannot by itself establish every source-code tie-breaker, MMP rule, or historical implementation detail.

## Source P3 — OpenZFS current source pinned at `33ae06bb...`

<https://github.com/openzfs/zfs/blob/33ae06bb617f586d43eb0a443cd69dad2f15467d/module/zfs/vdev_label.c>

Relevant source-level observations:

- `vdev_uberblock_load()` exists as the import/open path for reading candidate uberblocks;
- the source comment says configuration is then read from the same vdev as the best uberblock;
- `vdev_uberblock_compare()` is a distinct comparator;
- modern code interacts with MMP/activity semantics and therefore has selection detail beyond a naive universal `max(txg)` slogan.

**Supports:** current implementation still treats candidate-root selection and corresponding configuration as linked recovery work. (`H/P`, `E`)

**Boundary:** pinned modern source is not backdated into the 2005 draft and does not establish all release history between those endpoints.

## Source S1 — OpenZFS `zpool-import(8)` current manual

<https://openzfs.github.io/openzfs-docs/man/master/8/zpool-import.8.html>

The manual documents that `zpool import` can scan devices/directories when no cachefile is supplied, list importable pools, and display name/identifier, vdev layout, and health. It also documents recovery/rewind options separately.

**Supports:** import/discovery is an explicit restart operation distinct from ordinary already-open dataset access. (`H/S`)

**Boundary:** device scanning does not guarantee that damaged labels, roots, or payload are valid. Destructive rewind flags are not ordinary import semantics.

## Preservation/provenance source

Matthew Ahrens maintains <https://github.com/ahrens/zfsondisk>, which preserves the original on-disk-specification artifacts. This run inspected repository provenance/listing but does not rely on the binary ODT as an independently quoted source because its exact content was not separately rendered here.

## Claim matrix

| ID | Claim | Label | Best source | Strength / boundary |
| --- | --- | --- | --- | --- |
| G-128.1 | each physical vdev has four separated label copies | `H/P` | P1 §1.2.1 | direct historical statement |
| G-128.2 | fixed labels use staged even/odd overwrite | `H/P` | P1 §1.2.2 | direct historical mechanism |
| G-128.3 | label configuration carries pool/top/vdev identity relations | `H/P` | P1 §1.3.3 | direct field documentation |
| G-128.4 | label includes a 128 KB uberblock array | `H/P` | P1 §1.3 | direct layout statement |
| G-128.5 | 2005 active-root rule uses txg + valid SHA-256 | `H/P` | P1 §1.3.4 | bounded historical semantics |
| G-128.6 | uberblock candidates rotate rather than one root being overwritten | `H/P` | P1 §1.3.4 | direct historical mechanism |
| G-128.7 | `ub_rootbp` locates MOS | `H/P` | P1 §1.3.4 | direct root relation |
| G-128.8 | modern docs retain label/ring/highest-valid-txg import model | `H/P` later continuity | P2 | current explanatory witness |
| G-128.9 | current source couples best-uberblock load with config from same vdev | `H/P` later continuity | P3 | pinned source witness |
| G-128.10 | payload survival alone guarantees restart legibility | `X` | source/mechanism comparison | rejected |
| G-128.11 | every physically present uberblock is admissible/current | `X` | P1/P3 | rejected |
| G-128.12 | successful import proves complete integrity/redundancy | `X` | operation-scope comparison | rejected |
| G-128.13 | older uberblock survival equals intentional snapshot retention | `X` | P1 + current docs | rejected |
| G-128.14 | ZFS invented superblocks | `X` | P1's explicit UFS analogy | rejected |

## Engineering reconstruction

The sources support this bounded relation:

```text
surviving pool blocks
    + surviving label/config topology evidence
    + at least one admissible uberblock/root
    + compatible interpreter
    -> restart can re-establish pool legibility
```

The following are project reconstructions rather than source quotations:

- `payload survival ≠ restart legibility`;
- `label presence ≠ topology/currentness validity`;
- `uberblock presence ≠ active-root authority`;
- `restart-root recovery ≠ whole-pool integrity verification`;
- `import success ≠ restored redundancy`;
- `old root bytes ≠ user snapshot`.

## Functional comparisons, not genealogy

- **Case 46 / GFS:** checkpoint/log state plus re-observation recovers master control state; ZFS uses on-device label/root evidence. Similar recovery function, different mechanism/history.
- **Case 58 / Raft:** snapshot continuation metadata replaces command-history prefixes for consensus repair; ZFS uberblocks root a storage tree rather than consensus history.
- **Case 90 / Kafka:** both show retained metadata requires admissibility, but leader-epoch lineage and filesystem-root selection are unrelated mechanisms.
- **Case 95 / RAID-Z:** update consistency is not the same problem as restart root/topology legibility.
- **Case 100 / ZFS DTL:** repair-scope history is not restart-root evidence.

## Open gaps

This slice intentionally leaves open:

- exact release-by-release ZFS label/uberblock evolution after the 2005 draft;
- direct controlled corruption experiments over combinations of label copies and uberblock roots;
- modern MMP/import tie-breaking archaeology;
- hardware HBA / RAID-controller failure and metadata portability;
- severe MOS/root-chain corruption and forensic recovery;
- feature-flag / format-software admissibility is now handled separately by grounded [`Case 129`](../cases/129-zfs-feature-flags-format-compatibility.md); exact cross-release matrices and broader obsolescence remain open there;
- historical genealogy of superblocks and redundant restart roots.

Those gaps should not be inferred closed from this case.
