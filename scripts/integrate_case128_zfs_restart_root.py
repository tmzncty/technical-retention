from pathlib import Path
import re

CASE_PATH = Path('cases/128-zfs-vdev-label-uberblock-import-root-recovery.md')
EVIDENCE_PATH = Path('evidence/128-zfs-2005-2026-vdev-label-uberblock-grounding.md')
WORKFLOW_PATH = Path('.github/workflows/integrate-case128-zfs-restart-root.yml')
SELF_PATH = Path('scripts/integrate_case128_zfs_restart_root.py')

case_text = r'''# ZFS Vdev Labels and Uberblocks: Retained Pool Topology and Restart Roots

**Status:** `grounded`

## Scope

This case asks one bounded retention question:

> When process-local or host-local control state disappears, what on-device ZFS metadata is retained so a storage pool can be rediscovered, its topology interpreted, and a current committed root selected again?

The historical core is bounded to Sun Microsystems' **9 December 2005 draft ZFS On-Disk Specification**, especially Chapter One sections 1.2–1.3.4. Current OpenZFS documentation and pinned OpenZFS source are used only as later implementation/operational witnesses for import-time discovery and best-uberblock selection.

This case is not:

- a generic ZFS history;
- a second scrub case (Case 18);
- a second RAID-Z write-hole case (Case 95);
- a second dirty-time-log/resilver case (Case 100);
- proof that ZFS invented superblocks, restart roots, redundant labels, or copy-on-write roots;
- proof that four label copies make every pool recoverable after arbitrary device damage;
- proof that a physically present payload is importable without surviving control metadata;
- proof that an importable pool has restored redundancy or passed a complete integrity scan;
- a claim about vendor RAID-controller metadata or hardware-HBA replacement.

A fresh search of `tmzncty/computing-archaeology` found no dedicated ZFS vdev-label / uberblock case to reuse. Broad superblock history, ZFS genealogy, storage-controller history, and filesystem implementation archaeology belong there if developed.

## Historical vocabulary

Historical/source vocabulary retained here:

- `vdev` / `virtual device`;
- `physical vdev` / `leaf vdev`;
- `root vdev` / `top-level vdev`;
- `vdev label`;
- `name-value pair list`;
- `uberblock`;
- `transaction group` / `txg`;
- `pool_guid`, `top_guid`, `guid`;
- `ub_guid_sum`;
- `ub_rootbp`;
- `MOS` / Meta Object Set.

Project engineering vocabulary:

- **restart root** — a retained root pointer plus qualification state from which the current storage graph can be traversed after volatile control state is gone;
- **topology witness** — retained metadata that identifies pool/vdev relationships needed to interpret member devices;
- **root admissibility** — the relation by which one physically present candidate root is qualified for use rather than merely observed.

These project terms are analytical reconstructions, not claims about Sun's historical vocabulary.

## Historical record

### H/P — each physical vdev carries redundant labels

The 2005 Sun on-disk specification states that each physical vdev contains a 256 KB vdev label. It says the label describes that physical vdev and the related vdevs sharing its top-level-vdev ancestor.

The specification states that **four copies** are written on each physical vdev, with two near the front and two near the back. The stated rationale is to improve the chance that some label remains accessible after contiguous media failure or accidental overwrite.

This is retained control metadata, not four copies of all pool payload.

### H/P — label update uses an overwrite-safe staged sequence

Unlike most ZFS copy-on-write data, the fixed-location labels are overwritten. The 2005 specification therefore describes a two-stage update: even labels are written first while odd labels remain valid; after the even labels reach stable storage, the odd labels are updated.

The historical claim is narrow: the design tries to keep at least one valid label copy available across an interrupted label update. It is not a proof against arbitrary multi-location corruption.

### H/P — the label carries topology/configuration relations

The label's name-value-pair area includes pool/vdev identity and transaction state. The specification explicitly documents fields including `txg`, `pool_guid`, `top_guid`, and per-vdev `guid`, alongside a nested vdev-tree description.

Thus a member device retains more than a payload address space. It also retains relations needed to answer questions such as:

```text
which pool is this device part of?
which top-level vdev subtree does it belong to?
which configuration generation does this label describe?
```

### H/P — each label contains an uberblock array

The same specification divides the label into blank space, boot-header space, a name/value area, and **128 KB of 1 KB uberblock structures**.

Section 1.3.4 says the uberblock contains information necessary to access pool contents. In the bounded 2005 description, the active uberblock is the candidate with the highest transaction-group number and a valid SHA-256 checksum.

The specification also says an active uberblock is not overwritten in place; an updated uberblock is written into another element of the uberblock array, and uberblocks are written round-robin across pool vdevs.

### H/P — `ub_rootbp` anchors traversal into the MOS

The 2005 specification identifies `ub_rootbp` as a block pointer locating the MOS. The pool's larger object/metadata graph is therefore not recovered by scanning every payload block and guessing its role; a qualified uberblock supplies a root pointer into the metadata tree.

The same section documents `ub_guid_sum` as a check against the GUIDs of leaf vdevs encountered when opening a pool. This is another reminder that root selection and member availability are relational, not merely a matter of choosing the newest-looking bytes.

### H/P — modern OpenZFS retains the same broad root-selection architecture

Current OpenZFS documentation describes the pool as a tree rooted at the uberblock, says each device carries four label copies and each label carries a 128 KiB uberblock ring, and states that import chooses a valid uberblock with the highest transaction number.

Pinned current source at OpenZFS commit `33ae06bb617f586d43eb0a443cd69dad2f15467d` contains `vdev_uberblock_load()` and explicitly comments that configuration is read from the same vdev as the best uberblock. The implementation also has `vdev_uberblock_compare()` and modern MMP-related tie/activity logic, so this case does **not** reduce every current selection path to the historical shorthand `max(txg)`.

This is later continuity only; it is not projected backward as proof of every 2005 implementation detail.

### H/S — current `zpool import` can rediscover pools by scanning devices

Current OpenZFS `zpool-import(8)` documents pool discovery by scanning devices when no cachefile is supplied and reports pool identity, vdev layout, and health for candidate pools. This operational interface is consistent with the on-device label/configuration design.

It does not prove that every damaged set of labels is recoverable or that scanning alone validates all reachable payload.

## Retained state

The bounded restart/import path requires several different retained things:

1. payload and metadata blocks reachable from a usable root;
2. vdev-label copies on member devices;
3. pool/vdev identity and topology relations inside label configuration state;
4. multiple uberblock candidates carrying transaction/root state;
5. checksums and other qualification fields used to reject invalid candidates;
6. at least one `ub_rootbp` that reaches a usable MOS tree;
7. enough member devices / redundancy to satisfy the pool's availability requirements;
8. software capable of interpreting the on-disk format.

None of these is interchangeable with the others.

## Physical / logical substrate

At the bounded on-disk level:

```text
member block device
  -> fixed-position redundant vdev labels
      -> configuration nvlist + uberblock ring
          -> selected/admissible uberblock
              -> ub_rootbp
                  -> MOS and the rest of the reachable pool tree
```

The pool's logical continuity therefore depends on retained **relations among control structures**, not only on survival of user-data sectors.

## Retention mechanism

### Redundant fixed-location control metadata

Four separated label copies reduce dependence on one small physical region. Their placement is itself part of the recovery geometry.

### Staged overwrite of labels

Because labels are fixed-location structures, the 2005 design retains one old valid subset while writing another subset. This is a different consistency mechanism from copy-on-write replacement of ordinary tree blocks.

### Rotating root candidates

The uberblock ring retains several root candidates instead of overwriting the sole root in place. Qualification state — transaction number plus integrity/availability checks in the bounded sources — allows software to choose among candidates.

### Copy-on-write tree handoff

Current OpenZFS documentation describes a transaction group as reaching the committed pool state when the new root/uberblock is written after the changed path through the tree. Older roots can remain physically present in the ring while a newer committed root becomes current.

Engineering reconstruction:

> **root replacement can preserve restartability by retaining both an old admissible root and a newly written candidate until the newer state crosses its qualification boundary.**

## Addressing and access geometry

Restart/import is layered addressing:

1. discover candidate member devices;
2. read fixed-position label areas;
3. interpret pool/vdev identities and topology;
4. inspect uberblock candidates;
5. select an admissible root candidate;
6. follow `ub_rootbp` into the MOS;
7. traverse block pointers to recover higher-level objects and datasets.

This is not the same access path as an already-open file read. The restart path first has to recover the relations that make ordinary logical addressing meaningful.

## Read semantics

Reading a vdev label or uberblock is not described as destructive. The important read-side problem is **interpretive qualification**: a physically readable candidate can be stale, invalid, incompatible, or otherwise not the root software should use.

Thus:

> **physically readable control metadata ≠ current restart authority.**

## Write and erasure semantics

Label updates overwrite fixed regions using the staged even/odd sequence. Uberblock updates use different ring slots rather than replacing the only candidate in place.

Old labels/uberblocks can therefore survive physically after they stop being current. Their survival is not equivalent to a user-visible snapshot or guaranteed rollback point.

> **old restart-root bytes ≠ intentionally retained historical version.**

## Time

Several temporal relations are separate:

- a label-copy lifetime;
- a label-configuration `txg` generation;
- an uberblock candidate's transaction generation;
- the interval while a new label subset is being written;
- the interval while a txg is syncing before its root becomes committed;
- the later import/restart time needed to rediscover and traverse the pool.

A control structure can be physically old yet still useful as a fallback; another can be newer yet inadmissible because its integrity/reachability relation fails.

## Maintenance and labor

Persistence here depends on hidden work even though the on-device structures themselves are nonvolatile:

- generating and updating topology/configuration metadata;
- maintaining separated label copies;
- staging label writes so an older valid copy remains;
- computing and checking integrity metadata;
- rotating uberblock writes;
- importing/scanning candidate devices after restart;
- interpreting feature/version compatibility;
- diagnosing insufficient or inconsistent member sets.

The medium does not autonomously reconstruct a pool. Software must re-establish legibility from retained structures.

## Failure / forgetting modes

Distinct bounded failures include:

- all useful label copies on a required member becoming unreadable/corrupt;
- topology/configuration evidence becoming stale or inconsistent with the available member set;
- uberblock candidates being physically present but failing validity checks;
- the selected root pointer reaching unavailable/corrupt metadata;
- too few required vdev contributions surviving for the pool to open;
- format/feature incompatibility preventing interpretation;
- administrative rewind selecting an older state and intentionally discarding later logical history;
- ordinary payload corruption discovered only after import.

These are not one generic event called `data loss`.

## Engineering reconstruction

The central relation is:

```text
payload/media survival
    + topology witness survival
    + admissible restart-root survival
    + interpreter availability
    -> possible pool re-legibility
```

This yields the following guarded conclusions:

> **payload survival ≠ restart legibility.**

> **label presence ≠ label admissibility.**

> **uberblock presence ≠ active/current root.**

> **restart-root recovery ≠ complete integrity verification.**

> **pool import ≠ restored redundancy.**

> **on-device control metadata ≠ controller-independent hardware semantics.**

## Prior art and genealogy boundary

The 2005 specification itself says the uberblock is similar to the UFS superblock. Superblock-like restart roots therefore plainly predate ZFS.

The safe historical claim is only that the bounded ZFS design combines redundant vdev labels, topology/configuration state, an uberblock ring, transaction qualification, and a root block pointer in this documented way.

Chronology/function does not support:

> `ZFS invented superblocks`.

Nor does the existence of earlier superblocks establish a complete direct genealogy for every ZFS label/uberblock design choice.

## Cross-case comparison

### Case 46 — GFS master log/checkpoint recovery

Both cases retain compact control state that makes a larger store legible after restart. GFS combines replicated log/checkpoint state with re-observation of chunk locations; ZFS embeds topology/root evidence on member devices and traverses a copy-on-write object tree.

Functional comparison only:

> **recovery root ≠ one universal checkpoint mechanism.**

### Case 58 — Raft snapshotting

Raft snapshots replace committed command history and carry continuation metadata for consensus repair. A ZFS uberblock is a root into a committed storage tree, not a consensus snapshot and not a replacement for follower log lineage.

### Case 90 — Kafka leader-epoch admissibility

Both cases show that retained metadata must be qualified before it may authorize recovery. The mechanism and history are unrelated.

> **metadata presence ≠ metadata admissibility.**

### Case 95 — RAID-Z write-hole avoidance

Case 95 asks whether a multi-block coded update leaves an admissible on-disk state. Case 128 asks how restart discovers and chooses a root/topology after volatile control state is gone. Update consistency and restart legibility are adjacent but distinct.

### Case 100 — ZFS DTL selective resilver

Case 100 retains failure-exposure history to bound later repair scope. Case 128 retains topology/root state to make the pool interpretable in the first place.

> **repair-scope evidence ≠ restart-root evidence.**

## Functional analogy

A bounded analogy is a self-describing archive with several catalog covers and several recent root indexes: the content can survive, but a reader still needs an admissible catalog/root to know how the pieces compose.

This is only a functional analogy. It must not replace the historical ZFS vocabulary or imply that a filesystem is literally an archive institution.

## Philosophical / media-theoretical interpretation

`I` — Case 128 sharpens a distinction between **material survival** and **technical legibility**. Persistence is not exhausted by whether payload bits remain on media; the relations that make those bits addressable as *this pool, this topology, this current tree* must also survive or be reconstructable.

`I` — The retained root is not a miniature duplicate of the whole store. A small relation can organize access to a much larger body of surviving state.

`I` — Forgetting can therefore occur through loss of a root or topology witness even when much of the underlying material remains physically present.

These are project interpretations, not historical claims about Sun/OpenZFS authors' philosophy.

## Counterexamples and limits

This case does not establish:

- that four labels guarantee recovery after arbitrary corruption;
- that the newest physically readable uberblock is always safe to use;
- that modern MMP/import logic is identical to the 2005 draft;
- that every old uberblock is a supported rollback point;
- that successful import proves all files are intact;
- that successful import restores missing redundancy;
- that label redundancy duplicates the user payload;
- that host cachefile loss is the only reason import scanning is needed;
- that hardware RAID/HBA controller metadata behaves like ZFS labels;
- that ZFS originated the superblock/restart-root idea.

## Related repositories

- [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) — fresh searches for `ZFS`, `uberblock`, and `vdev label` found no dedicated case to reuse. Broad superblock history, ZFS source genealogy, controller history, and filesystem implementation archaeology belong there if developed.
- [`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) — a future problem-history slice could ask how actors distinguished `consistent on-disk state`, `import`, `recovery`, `rollback`, and `repair` across filesystem generations.

## Claim ledger

| Claim | Label | Evidence | Limit |
| --- | --- | --- | --- |
| each physical vdev carries four separated label copies | `H/P` | Sun 2005 on-disk spec §1.2.1 | bounded to documented design |
| fixed labels use a two-stage even/odd update | `H/P` | Sun 2005 §1.2.2 | not proof against arbitrary corruption |
| label nvlist retains pool/vdev identity and topology relations | `H/P` | Sun 2005 §1.3.3 | not a complete history of configuration changes |
| label contains a 128 KB uberblock array | `H/P` | Sun 2005 §1.3 / §1.3.4 | historical layout witness |
| bounded 2005 active root uses highest txg plus valid SHA-256 | `H/P` | Sun 2005 §1.3.4 | do not universalize to all modern tie/activity logic |
| `ub_rootbp` locates the MOS | `H/P` | Sun 2005 §1.3.4 | root pointer is not payload duplication |
| modern OpenZFS import retains the broad label/ring/best-root architecture | `H/P` later continuity | OpenZFS docs + pinned `vdev_label.c` | later implementation witness only |
| payload survival guarantees importability | `X` | mechanism decomposition | rejected |
| physically newest candidate is automatically authoritative | `X` | validity/selection requirements | rejected |
| successful import proves complete integrity and restored redundancy | `X` | operation-scope comparison | rejected |
| ZFS invented superblocks/restart roots | `X` | Sun spec's own UFS analogy + prior art | rejected |

## Sources

- Sun Microsystems, **ZFS On-Disk Specification**, draft 2005-12-09, Chapter One §§1.2–1.3.4, preserved PDF: <https://www.filibeto.org/~aduritz/truetrue/solaris10/ondiskformatfinal.pdf>
- Matthew Ahrens preservation repository for the original on-disk specification artifacts: <https://github.com/ahrens/zfsondisk>
- OpenZFS, **Copy-on-Write** documentation, current documentation witness: <https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Copy-on-write.html>
- OpenZFS pinned source, `module/zfs/vdev_label.c`, commit `33ae06bb617f586d43eb0a443cd69dad2f15467d`: <https://github.com/openzfs/zfs/blob/33ae06bb617f586d43eb0a443cd69dad2f15467d/module/zfs/vdev_label.c>
- OpenZFS, **zpool-import(8)**, current manual: <https://openzfs.github.io/openzfs-docs/man/master/8/zpool-import.8.html>
'''

evidence_text = r'''# Evidence 128 — ZFS vdev-label / uberblock restart-root grounding, 2005–2026

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
- feature-flag/format-obsolescence behavior across old/new implementations;
- historical genealogy of superblocks and redundant restart roots.

Those gaps should not be inferred closed from this case.
'''

if CASE_PATH.exists() or EVIDENCE_PATH.exists():
    raise SystemExit('Case 128 canonical files already exist; refusing duplicate integration')

CASE_PATH.write_text(case_text.rstrip() + '\n', encoding='utf-8')
EVIDENCE_PATH.write_text(evidence_text.rstrip() + '\n', encoding='utf-8')

# README: insert Case 128 immediately after the canonical Case 127 row.
readme_path = Path('README.md')
readme = readme_path.read_text(encoding='utf-8')
if '(cases/128-zfs-vdev-label-uberblock-import-root-recovery.md)' not in readme:
    lines = readme.splitlines()
    positions = [i for i, line in enumerate(lines) if '(cases/127-dram-power-off-remanence-gradual-decay.md)' in line]
    if len(positions) != 1:
        raise SystemExit(f'Expected exactly one README Case 127 row, found {len(positions)}')
    insert_at = positions[0] + 1
    lines.insert(insert_at, '- [`cases/128-zfs-vdev-label-uberblock-import-root-recovery.md`](cases/128-zfs-vdev-label-uberblock-import-root-recovery.md) — grounded ZFS restart-root/topology bridge: four separated vdev-label copies, staged label overwrite, retained pool/vdev identity, an uberblock ring, root-currentness qualification, and `ub_rootbp` make payload survival, topology legibility, restart-root authority, importability, integrity verification, and restored redundancy distinct relations.')
    readme_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

# ROADMAP: add a completed Phase-2 case line and make the restart-root forgetting gap explicit.
roadmap_path = Path('ROADMAP.md')
roadmap = roadmap_path.read_text(encoding='utf-8')
if 'Case 128 ZFS vdev-label / uberblock restart-root grounding' not in roadmap:
    lines = roadmap.splitlines()
    positions = [i for i, line in enumerate(lines) if line.startswith('- [x]') and 'Case 127' in line]
    if not positions:
        raise SystemExit('Could not locate Phase-2 Case 127 completion line')
    i = positions[0] + 1
    lines.insert(i, '- [x] Case 128 ZFS vdev-label / uberblock restart-root grounding — [`cases/128-zfs-vdev-label-uberblock-import-root-recovery.md`](cases/128-zfs-vdev-label-uberblock-import-root-recovery.md), grounded by [`evidence/128-zfs-2005-2026-vdev-label-uberblock-grounding.md`](evidence/128-zfs-2005-2026-vdev-label-uberblock-grounding.md): the 9-Dec-2005 Sun on-disk specification anchors four spatially separated labels, staged fixed-label updates, topology/identity nvlist state, a rotating uberblock array, transaction/checksum qualification, and `ub_rootbp` into the MOS; current OpenZFS docs/source are later continuity witnesses only. This closes the bounded `payload survival ≠ restart legibility` and `root presence ≠ root admissibility` relations, while hardware-controller loss, severe root-chain corruption, format-obsolescence, release genealogy, and empirical fault injection remain open.')
    roadmap = '\n'.join(lines) + '\n'

marker = '- [ ] loss of index or mapping metadata — **substantially advanced by grounded Case 39**:'
new_bullet = '- [ ] loss or corruption of restart roots, superblocks, or pool-topology metadata — **substantially advanced at the ZFS on-device control-metadata layer by grounded Case 128**: Sun 2005 separates payload from four redundant vdev labels, retained pool/vdev topology, multiple uberblock candidates, validity/currentness qualification, and the `ub_rootbp` restart root into the MOS. This grounds `payload survival ≠ restart legibility`, `control-metadata presence ≠ control-metadata admissibility`, and `restart-root recovery ≠ complete integrity verification`. Hardware RAID/HBA controller metadata, total root/topology loss, corrupted-but-plausible roots, cross-version feature incompatibility, other filesystems/databases, and controlled fault injection remain open;'
if new_bullet not in roadmap:
    lines = roadmap.splitlines()
    positions = [i for i, line in enumerate(lines) if line.startswith(marker)]
    if len(positions) != 1:
        raise SystemExit(f'Expected one mapping-metadata roadmap marker, found {len(positions)}')
    lines.insert(positions[0] + 1, new_bullet)
    roadmap = '\n'.join(lines) + '\n'
roadmap_path.write_text(roadmap, encoding='utf-8')

# CASE_INDEX: insert canonical case row after Case 127 and append bounded findings with dynamic numbering.
index_path = Path('CASE_INDEX.md')
index = index_path.read_text(encoding='utf-8')
if '(cases/128-zfs-vdev-label-uberblock-import-root-recovery.md)' not in index:
    lines = index.splitlines()
    positions = [i for i, line in enumerate(lines) if '(cases/127-dram-power-off-remanence-gradual-decay.md)' in line and line.startswith('|')]
    if len(positions) != 1:
        raise SystemExit(f'Expected one CASE_INDEX Case 127 table row, found {len(positions)}')
    row = '| [ZFS Vdev Labels and Uberblocks: Retained Pool Topology and Restart Roots](cases/128-zfs-vdev-label-uberblock-import-root-recovery.md) | **grounded** | nonvolatile pool payload + four separated fixed vdev-label copies + topology/configuration nvlist + rotating uberblock restart roots + validity/currentness qualification | separate physical payload survival, topology legibility, restart-root authority, importability, integrity verification, and redundancy repair; show that a small retained root relation can organize access to a much larger surviving store | [2005–2026 grounding record](evidence/128-zfs-2005-2026-vdev-label-uberblock-grounding.md); release-by-release evolution, severe root corruption, modern MMP tie-breaking, hardware-controller failure, format obsolescence, and fault injection remain open |'
    lines.insert(positions[0] + 1, row)
    index = '\n'.join(lines) + '\n'

if '## Case 128 — ZFS vdev-label / uberblock restart-root findings' not in index:
    nums = [int(x) for x in re.findall(r'(?m)^- \*\*(\d+) —', index)]
    if not nums:
        raise SystemExit('Could not determine latest CASE_INDEX finding number')
    n = max(nums) + 1
    findings = [
        ('four label copies ≠ four payload copies', 'Sun 2005 duplicates control labels on each physical vdev; it does not describe four complete copies of pool user data. (`H/P`, `E`, `X`)'),
        ('label survival ≠ pool legibility by itself', 'a label supplies topology/configuration evidence, but restart still needs an admissible uberblock/root, required member state, and a compatible interpreter. (`H/P`, `E`)'),
        ('payload survival ≠ restart legibility', 'surviving blocks do not by themselves reveal the qualified pool topology and current root needed for ordinary logical traversal. (`E`)'),
        ('fixed-label overwrite ≠ ordinary ZFS copy-on-write', 'the 2005 spec explicitly gives labels a staged even/odd overwrite path because their locations are fixed. (`H/P`)'),
        ('staged label update ≠ arbitrary-fault immunity', 'retaining an old valid subset during update narrows one crash window but does not guarantee survival of all labels under broader damage. (`H/P`, `X`)'),
        ('uberblock ring ≠ complete transaction history', 'several root candidates survive, but the ring is a bounded rotating set of restart roots rather than an archive of every past state. (`H/P`, `E`)'),
        ('uberblock presence ≠ active-root authority', 'the bounded 2005 rule qualifies candidates by transaction generation and checksum; physical readability alone does not make a candidate current. (`H/P`, `E`)'),
        ('historical highest-txg rule ≠ universal modern selector', 'current OpenZFS retains comparator/MMP activity logic, so the 2005 shorthand must not be projected as the whole modern decision procedure. (`H/P`, `X`)'),
        ('`ub_rootbp` ≠ duplicated pool payload', 'the root block pointer organizes reachability into the MOS; it is a compact relation to larger retained state, not a copy of that state. (`H/P`, `E`)'),
        ('restart-root recovery ≠ whole-pool integrity verification', 'selecting a usable root makes traversal possible; scrub/checksum coverage of the reachable pool remains a distinct operation. (`E`, `A`)'),
        ('successful import ≠ restored redundancy', 'a pool can become legible/serviceable while resilver or other repair obligations still remain. (`E`, `A`)'),
        ('old uberblock survival ≠ user snapshot', 'a physically surviving former root is not automatically an intentional, supported historical-version retention contract. (`H/P`, `E`, `X`)'),
        ('root/topology loss can cause forgetting without immediate payload erasure', 'loss of the relations that identify and root the pool can destroy ordinary technical legibility even while many underlying blocks remain. (`E`, `I`)'),
        ('ZFS restart-root evidence ≠ GFS/Raft/Kafka recovery metadata', 'the cases are functionally comparable at the admissibility/recovery-root level but have different mechanisms and histories. (`A`, `X`)'),
        ('ZFS uberblock ≠ invention of the superblock', 'the 2005 specification itself compares the uberblock to the UFS superblock; this case makes no first/invention claim. (`H/P`, `X`)'),
        ('related-repository boundary', 'fresh `tmzncty/computing-archaeology` searches found no dedicated ZFS/vdev-label/uberblock case; broad superblock, ZFS, storage-controller, and filesystem genealogy belongs there if developed. (`H/P` project-state record)'),
    ]
    block = ['','## Case 128 — ZFS vdev-label / uberblock restart-root findings','']
    for title, body in findings:
        block.append(f'- **{n} — {title}:** {body}')
        n += 1
    index = index.rstrip() + '\n' + '\n'.join(block) + '\n'

index_path.write_text(index, encoding='utf-8')

# Normalize only canonical files.
for p in [CASE_PATH, EVIDENCE_PATH, readme_path, roadmap_path, index_path]:
    lines = p.read_text(encoding='utf-8').splitlines()
    p.write_text('\n'.join(line.rstrip() for line in lines) + '\n', encoding='utf-8')

# One-shot helper/workflow cleanup. Their deletion is committed with the research change.
for p in [WORKFLOW_PATH, SELF_PATH]:
    if p.exists():
        p.unlink()
