# Case 96 evidence index — OpenZFS dRAID distributed spare and sequential rebuild

**Case:** [`cases/96-openzfs-draid-distributed-spare-sequential-resilver.md`](../cases/96-openzfs-draid-distributed-spare-sequential-resilver.md)  
**Current maturity:** `grounded`  
**Maturity change in this index:** none

This file is the navigation layer for Case 96. It does not replace the case narrative or evidence records; it makes the current evidence chains, boundaries, and remaining debt explicit so later rounds do not repeat already-grounded work.

---

## 1. Canonical case

- [`cases/96-openzfs-draid-distributed-spare-sequential-resilver.md`](../cases/96-openzfs-draid-distributed-spare-sequential-resilver.md)

Bounded question:

> How does OpenZFS dRAID alter the duration and structure of redundancy restoration after device failure, and what retained control/layout/progress state makes that recovery possible?

Canonical status remains `grounded`.

---

## 2. Evidence chain A — distributed spare / fixed-width dRAID / sequential reconstruction grounding

- [`96-openzfs-1992-2021-draid-recovery-grounding.md`](96-openzfs-1992-2021-draid-recovery-grounding.md)

### Historical record established

The grounding record directly anchors:

- OpenZFS 2.1.0 as the release boundary;
- accepted PR #10102 as the development/merge record;
- all-child participation in a distributed spare rebuild;
- fixed-width dRAID redundancy groups;
- deterministic permutation mapping;
- distributed spare capacity;
- sequential reconstruction / device rebuild;
- space-map-guided allocated-range traversal;
- the first-phase checksum-verification limitation;
- default follow-up scrub;
- earlier parity-declustering and distributed-sparing prior art in 1992–1994 CMU work.

### Core boundaries already closed

```text
spare capacity
    != spare-path bandwidth

parity count
    != recovery speed

redundancy restored
    != integrity fully revalidated

sequential reconstruction
    != healing reconstruction

fixed-width dRAID
    != variable-width ordinary RAID-Z

OpenZFS dRAID
    != invention of parity declustering / distributed sparing
```

### Do not repeat

Future rounds should not spend a slice merely re-establishing:

- that dRAID has distributed spares;
- that distributed spare participation can shorten rebuild time;
- that sequential rebuild omits first-pass block checksum verification;
- that a later scrub supplies a separate verification phase;
- that parity declustering/distributed sparing predate OpenZFS.

Those points are already grounded.

---

## 3. Evidence chain B — rebuild-progress persistence and restart boundary

- [`96-openzfs-2021-rebuild-progress-restart-boundary-deepening.md`](96-openzfs-2021-rebuild-progress-restart-boundary-deepening.md)

### Historical record established

OpenZFS 2.1.0 source directly shows:

- an explicitly on-disk `vdev_rebuild_phys_t`;
- persistent `vrp_rebuild_state` and `vrp_last_offset`;
- saved min/max missing-TXG bounds and rebuild statistics;
- separate in-core per-TXG scan offsets and in-flight state;
- sync-time update of `vrp_last_offset` into the top-level vdev ZAP;
- rebuild suspension during export while leaving the episode active;
- reload of rebuild state from disk;
- creation of a fresh rebuild thread when active state is found during pool load;
- restart selection that clears already-rebuilt ranges below the saved offset;
- deliberate import continuation when the rebuild-state ZAP value is missing/damaged;
- DTL reassessment only after successful rebuild completion;
- later scrub as a separate integrity-verification phase.

### Core boundaries now closed

```text
repair need
    != repair-progress checkpoint

persisted rebuild episode
    != live rebuild thread

restartable progress
    != full repair-history retention

saved last-offset frontier
    != all in-core scan / I/O microstate

pool importability
    != rebuild-checkpoint recoverability

rebuild progress retained
    != rebuild completion
    != DTL debt retirement
    != checksum revalidation
```

### Important new state decomposition

```text
DTL / missing-TXG relation
    ↓  says why repair is owed

persistent rebuild state
    ↓  says whether a sequential episode is active and where its restart frontier lies

in-core scan state
    ↓  drives the currently executing pass

material reconstruction
    ↓  restores missing coded contributions

follow-up scrub
    ↓  restores stronger checksum-qualified confidence
```

This decomposition is now part of the Case-96 evidence base and should be reused rather than rediscovered.

---

## 4. Cross-case routing

### Case 17 — RAID degraded reconstruction

Use Case 17 for generic parity reconstruction and the distinction between degraded service and repaired redundancy.

Case 96 should remain focused on the OpenZFS dRAID composition and its maintenance-state boundaries.

### Case 18 — ZFS scrub

Use Case 18 for checksum-qualified proactive verification/self-healing.

Case 96 uses scrub only to mark the post-rebuild confidence boundary:

```text
first-phase coded redundancy
    != later checksum verification
```

### Case 94 — RAID-6 P+Q

Use Case 94 for dual-erasure algebra and the corruption-location boundary.

Case 96 answers a different question:

```text
code strength
    != repair geometry
    != repair duration
```

### Case 95 — RAID-Z write-hole avoidance

Use Case 95 for variable-width COW RAID-Z write semantics.

Case 96's fixed width is a recovery-enabling geometry, not a universal replacement for ordinary RAID-Z layout.

### Case 100 — ZFS DTL selective resilver

Use Case 100 for retained failure intervals / missing-TXG repair scope.

The new Case-96 deepening adds the complementary repair-progress axis:

```text
DTL repair scope
    != sequential rebuild progress frontier
```

### Case 83 — HDFS scanner cursor

Use only as functional comparison for restartable maintenance progress.

Do not infer shared genealogy or equal failure consequences.

### Case 148 — NVMe extended self-test

Use only as functional comparison for:

```text
operation identity survival
    != exact execution microstate survival
```

Case 96 has source-visible persisted frontier state; that must not be projected into NVMe implementations without product evidence.

---

## 5. Related-repository routing

`tmzncty/computing-archaeology` remains the correct destination for broader history such as:

- general RAID-controller rebuild chronology;
- first rebuild-checkpoint implementations;
- parity-declustering genealogy beyond the bounded prior-art guardrails;
- broad ZFS resilver history;
- vendor-array reconstruction architecture not needed to answer the Case-96 retention question.

A repository search performed for this round found no existing dRAID-specific companion packet to reuse.

Case 96 should therefore retain only the mechanism-specific evidence needed for technical-retention analysis.

---

## 6. Evidence-strength map

| Claim | Current evidence | Strength | Remaining qualifier |
| --- | --- | --- | --- |
| dRAID was released in OpenZFS 2.1.0 | release record | strong primary | none for release claim |
| distributed spare uses broad device participation | PR + released source | strong primary | benchmark magnitude remains configuration-specific |
| fixed width enables the released sequential-rebuild path | released source | strong primary | not universal RAID law |
| sequential first phase omits checksum verification | released source | strong primary | later scrub supplies different evidence |
| parity declustering/distributed sparing predate dRAID | peer-reviewed paper + dissertation | strong scholarly prior art | no direct genealogy claim |
| rebuild state/progress is represented on disk | 2.1.0 header + source | strong primary | lower media persistence composition not independently fault-tested here |
| export/import can resume an active rebuild | released source + pool-load path | strong primary implementation | hardware power-cut behavior remains separate |
| saved last offset changes restart work selection | released source | strong primary | exact crash-point replay window not experimentally measured here |
| missing/damaged rebuild-state value need not block pool import | released source | strong primary implementation | may lose progress / repeat work |
| rebuild progress state is distinct from DTL repair need | released source composition | strong engineering reconstruction from primary code | exact fault-injection matrix remains open |
| same behavior holds in all later OpenZFS versions | not established | unsupported | requires version archaeology |

---

## 7. Current compact model

```text
failed / missing device relation
    ↓
DTL records repair scope / missing history
    ↓
sequential rebuild episode starts
    ↓
ACTIVE + min/max TXG + last-offset state retained on disk
    ↓
in-core worker traverses current allocated space
    ↓
progress periodically becomes persisted restart frontier
    ↓
export/import may destroy and recreate execution machinery
    ↓
retained ACTIVE state + last offset reconstruct continuation
    ↓
material redundancy restored
    ↓
DTL reassessed / repair debt retired
    ↓
follow-up scrub verifies stronger checksum relation
```

This is the current Case-96 retention pipeline. It is an analytical decomposition, not a claim that OpenZFS developers used this exact diagram or vocabulary.

---

## 8. Remaining research debt

The highest-value next slices are now narrow:

1. **Export/import or reboot test provenance** — identify a released ZTS test that explicitly interrupts and resumes sequential rebuild, then compare the test's asserted progress semantics with the implementation path.
2. **Checkpoint ordering** — inspect the exact TXG/I/O ordering that justifies advancement of `vrp_last_offset`; keep this separate from lower-device power-loss guarantees.
3. **Crash replay window** — fault-inject around the persistent frontier and measure which work may be repeated after restart.
4. **Damaged checkpoint experiment** — corrupt/remove `VDEV_TOP_ZAP_VDEV_REBUILD_PHYS` while preserving DTL repair evidence and observe fallback to a new repair pass.
5. **Post-2.1 version archaeology** — determine whether later OpenZFS changes the checkpoint fields, restart admission, or scrub handoff.
6. **Named hardware fault validation** — only if needed to make a stronger power-loss claim than the source-level transaction boundary currently supports.

Lower priority for this repository:

- generic dRAID performance summaries;
- another explanation of distributed spares;
- broad RAID/ZFS history;
- unrestricted parity-declustering genealogy.

---

## 9. Maturity decision

**Case 96 remains `grounded`.**

The new evidence materially deepens the maintenance-control-state story but does not justify a maturity promotion by itself. The source-level restart path is strong, yet exact crash-point replay, lower-layer persistence composition, explicit ZTS interruption evidence, and later-version evolution remain open.

That is the correct bounded status: the mechanism is grounded; several implementation and fault-validation edges remain available for future deepening.
