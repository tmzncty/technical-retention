from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ROADMAP = ROOT / "ROADMAP.md"
INDEX = ROOT / "CASE_INDEX.md"
SYNTH = ROOT / "docs/SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md"


def read(path):
    return path.read_text(encoding="utf-8")


def write(path, text):
    path.write_text(text, encoding="utf-8")


def insert_after_prefix_line(path, prefix, addition):
    text = read(path)
    assert addition.strip() not in text, f"addition already present in {path}"
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    assert len(hits) == 1, f"expected one prefix in {path}: {prefix!r}, got {len(hits)}"
    i = hits[0]
    lines[i + 1:i + 1] = ["", addition]
    write(path, "\n".join(lines) + ("\n" if text.endswith("\n") else ""))


def replace_prefix_line(path, prefix, new_line):
    text = read(path)
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    assert len(hits) == 1, f"expected one prefix in {path}: {prefix!r}, got {len(hits)}"
    lines[hits[0]] = new_line
    write(path, "\n".join(lines) + ("\n" if text.endswith("\n") else ""))


def insert_before(path, anchor, addition):
    text = read(path)
    assert addition.strip() not in text, f"addition already present in {path}"
    assert text.count(anchor) == 1, f"expected one anchor in {path}: {anchor!r}"
    write(path, text.replace(anchor, addition + "\n\n" + anchor, 1))


assert not SYNTH.exists(), f"unexpected existing synthesis: {SYNTH}"
SYNTH.write_text(r'''# Synthesis 07 — Coded Recoverability, Degraded Service, and Restored Redundancy Margin

## Scope

This is a **bounded cross-case synthesis**, not a new historical case and not a genealogy of RAID or ZFS.

It closes one relation-decomposition question already present in the roadmap:

> How should `encoded reconstructability`, `degraded-service continuity`, and `restored redundancy margin` be separated in coded-storage regimes?

The comparison is built only from already-grounded repository cases:

- [Case 17 — RAID parity reconstruction](../cases/17-raid-parity-reconstruction-degraded-repair.md);
- [Case 18 — ZFS scrub / latent-error detection](../cases/18-zfs-scrub-latent-error-detection.md);
- [Case 94 — RAID-6 P+Q dual-erasure boundary](../cases/94-raid6-pq-dual-erasure-corruption-boundary.md);
- [Case 96 — OpenZFS dRAID distributed-spare / sequential resilver](../cases/96-openzfs-draid-distributed-spare-sequential-resilver.md);
- [Case 100 — ZFS dirty-time-log / selective resilver](../cases/100-zfs-dirty-time-log-selective-resilver.md).

No new invention-priority claim is made here. Historical claims remain owned by the cited case/evidence records and their primary sources. This document adds an **engineering comparison** across those records.

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `RAID`, `resilver`, and `distributed sparing` found no dedicated overlapping case in the current repository search surface. A full history of RAID levels, controller products, parity declustering, distributed sparing, URE-aware rebuild policy, or ZFS implementation chronology still belongs there if developed.

---

## Historical records kept separate

The comparison works only if the source-bound historical records are not collapsed into one timeless `rebuild` story.

### Case 17 — parity reconstruction and degraded repair, 1977–1994

Ouchi's 1977-filed IBM reconstruction patent establishes a pre-RAID-name parity/check-sum recovery floor. Patterson, Gibson, and Katz supply the later RAID nomenclature. Chen et al. 1993–1994 then make several operational relations explicit: failed-member validity state, parity consistency/currentness, demand reconstruction, stand-by spare use, background reconstruction, and retained `meta state` including how much of a failed disk has already been reconstructed.

The relevant historical result is not merely that parity can solve for missing data. The same period source distinguishes a request being serviceable while a disk is failed from the later completion of whole-member reconstruction.

### Case 94 — P+Q changes the known-erasure algebra, not every diagnosis problem

Chen et al.'s P+Q / RAID Level 6 discussion and H. Peter Anvin's later RAID-6 mathematics note establish a stronger coded relation: two independent syndromes can reconstruct two **known missing positions** under the bounded model. The recovery equations depend on the failed positions. Anvin also supplies the counterexample that arbitrary dual silent corruption is not thereby generally located and repaired.

The historical/mechanism boundary is therefore:

`more syndrome information ≠ complete fault-location information`.

### Case 96 — dRAID changes restoration geometry and duration

OpenZFS dRAID 2.1.0 composes fixed-width redundancy groups, deterministic permutation mappings, and distributed spare capacity so many children can participate in sequential reconstruction. Released source explicitly separates that fast first-phase redundancy restoration from the later checksum-verification scrub.

The bounded claim is about the **bandwidth/geometry and duration of repair**, not a new parity count and not a general claim that every dRAID layout outperforms every other layout.

### Case 100 — DTL changes which state enters repair

The ZFS dirty-time-log family retains transaction-group / birth-time exposure evidence so a returned device need not be treated as if all current data were equally suspect. The repair set can be pruned before reconstruction is scheduled.

This is a different optimization axis from dRAID:

- DTL: **which current blocks need catch-up?**
- dRAID: **how is selected reconstruction work laid out and parallelized?**

### Case 18 — verification is another completion axis

ZFS scrub proactively traverses current data and uses checksums to qualify integrity; when a trustworthy redundant source exists it can repair a bad embodiment. Scrub is therefore not equivalent to resilver/rebuild. Case 96 gives the sharp counterexample: sequential reconstruction can restore coded redundancy first and checksum verification can follow afterward.

---

## Engineering reconstruction: a staged recovery relation

The following decomposition is **project engineering vocabulary (`E`)**, not historical terminology shared by all systems.

### 1. Failure / exposure recognition

The system first needs some basis for treating one contribution or interval as suspect, missing, failed, or incompletely replicated.

Examples:

- failed/invalid member state in Case 17;
- explicit failed positions in Case 94 recovery;
- DTL intervals in Case 100.

This state can be small relative to the payload, yet it changes which recovery equations or repair paths are admissible.

### 2. Coded-currentness qualification

Surviving redundancy bytes are useful only if they still belong to the current coded relation. Case 17's parity-consistency state and Case 94's dirty/degraded boundary prevent a simple inference from `parity sector exists` to `parity is safe to solve with`.

### 3. Encoded reconstructability

Given the surviving current contributions and the required fault-location relation, can the missing logical contribution be derived?

This is an algebraic/relational property of the retained state under a specified failure model. It does not state how long reconstruction takes, whether the system will serve an application request during repair, or whether the desired future failure margin has been restored.

### 4. Degraded-service admissibility

Can the system continue serving a request while one or more physical contributions remain missing?

Case 17's demand reconstruction shows that a request may succeed before background repair finishes. This is a service-policy/implementation relation layered on top of reconstructability.

### 5. Repair-scope selection

Which current state actually needs reconstruction?

Case 100 shows that repair work can be bounded by retained failure-exposure history. A short outage can leave a device needing only catch-up for blocks born in the relevant interval rather than a full replacement-device reconstruction.

### 6. Reconstruction geometry and bandwidth

How is the selected work traversed, sourced, and written?

Case 96 shows that fixed-width dRAID layout plus distributed spare capacity can make many devices participate in sequential reconstruction. This changes repair duration without changing the configured parity count.

### 7. Materialized repaired state

At some point missing current contributions have been written into an admissible replacement/spare embodiment. This is stronger than request-time on-the-fly reconstruction but can still be weaker than every later confidence condition.

### 8. Restored redundancy margin

The configured failure model's ordinary margin is restored only when the missing coded contribution has been re-materialized sufficiently that the next tolerated failure no longer depends on the already-degraded relation.

This is why `a read succeeded` is not the same milestone as `the array is repaired`.

### 9. Integrity revalidation

Case 96 makes the final separation explicit: sequential reconstruction can restore redundancy before a later scrub verifies checksums. A system can therefore regain one future-failure margin while still owing a separate integrity-verification pass.

---

## The compact relation map

```text
failure / exposure evidence
        ↓
currentness-qualified surviving code relation
        ↓
mathematical reconstructability
        ↓
(optional) degraded request service
        ↓
repair-scope selection
        ↓
reconstruction geometry / bandwidth
        ↓
repaired embodiment
        ↓
restored redundancy margin
        ↓
(optional/separate) checksum-qualified confidence
```

This is not asserted as one universal implementation pipeline. Some systems fuse stages, omit stages, or expose different interfaces. Its use is diagnostic: if a statement says only `recovered`, ask **which arrow has actually been crossed**.

---

## Cross-case comparison

| Relation | Case 17 | Case 94 | Case 96 | Case 100 | Case 18 |
| --- | --- | --- | --- | --- | --- |
| failure/location evidence | failed/invalid member + meta state | known failed positions are inputs to recovery | failed child / layout state | txg/birth-time exposure intervals | verification discovers previously unknown defects |
| coded reconstructability | one-missing parity relation | two-known-erasure P+Q relation | inherited RAID-Z/dRAID code relation | assumes surviving redundancy sufficient for catch-up | repair requires trustworthy redundancy when corruption is found |
| degraded request service | demand reconstruction can serve before rebuild ends | algebra permits recovery under bounded model | not the central slice | not the central slice | ordinary pool can remain usable during scrub |
| repair-scope selection | failed-member reconstruction frontier | failed positions define unknowns | allocated regions scanned for rebuild | DTL prunes unaffected state | scrub deliberately broadens verification scope |
| repair geometry | background reconstruction / spare | not determined by P+Q alone | distributed spare + sequential reconstruction | orthogonal to DTL selection | scrub traversal / conditional healing |
| restoration milestone | full failed-member reconstruction | re-materializing lost members restores code margin | sequential rebuild restores redundancy | catch-up clears repair debt for exposed state | detected bad embodiment repaired if source exists |
| post-repair integrity confidence | separate issue | extra checksum/diagnosis may still be needed | later scrub explicitly separate | DTL membership is not checksum evidence | central concern |

The table is a functional comparison (`A/E`). It does not imply historical descent among Berkeley RAID, Linux RAID-6, Sun/Oracle ZFS, or OpenZFS dRAID.

---

## Findings

### E — code strength ≠ repair scope

P+Q changes which known-erasure combinations can be reconstructed. A DTL changes which blocks need catch-up. These are independent axes.

### E — repair scope ≠ reconstruction geometry

Selecting less work and scheduling the selected work more efficiently are different mechanisms. DTL temporal pruning and dRAID distributed sequential reconstruction demonstrate the distinction directly.

### E — reconstruction geometry ≠ code strength

A layout can shorten the duration of reduced redundancy without adding another independent syndrome. Conversely, a stronger code can tolerate another known erasure without saying anything about how quickly the array returns to its fully repaired condition.

### E — failure-location knowledge ≠ redundancy equations

Case 94 is the clearest counterexample: two syndromes do not remove the need to know which positions are missing, and they do not in general solve arbitrary dual silent corruption diagnosis.

### E — coded-byte survival ≠ usable coded currentness

Parity can survive physically while being inconsistent with the current data relation. Reconstruction therefore depends on retained currentness/admissibility state, not merely on the amount of material redundancy that remains.

### E — integrity confidence can lag redundancy restoration

Case 96 restores dRAID redundancy through sequential reconstruction before the follow-up scrub re-enters block-pointer/checksum verification space. `repaired enough for the next device failure` and `revalidated against every checksum reached by scrub` are different conditions.

### E — redundancy margin has an algebraic axis and a temporal axis

The configured code determines which failure combinations are tolerable. Repair design determines how long the system remains in a reduced-margin state after one failure consumes part of that tolerance. The same parity count can therefore be paired with different redundancy-restoration intervals.

This is not a probability claim or a universal reliability metric; it is a relation decomposition. Actual risk still depends on workload, device faults, correlated failures, latent errors, capacity, controller behavior, and environment.

---

## What must not be inferred

This synthesis does **not** establish:

- that RAID, ZFS, dRAID, DTL, and scrubbing share one historical lineage;
- that all coded-storage systems expose the same recovery stages;
- that two-parity systems can diagnose any two corruptions;
- that faster reconstruction increases code distance;
- that a successful degraded read means the array has been repaired;
- that restoring redundancy proves all reconstructed bytes have been checksum-verified;
- that a DTL proves corruption rather than possible missed replication;
- that a scrub is a rebuild;
- that one numerical `health` or `redundancy` scalar can replace the typed states above.

---

## Philosophical boundary

`I` — Coded storage makes a useful form of technical retention visible: what persists can be a **conditional capacity for future reconstruction**, not a second complete copy of the missing state.

`I` — But that capacity is typed. A system may still be able to answer the present request while having less ability to survive the next failure, and it may later restore that failure margin before it restores a stronger verification claim. The retained thing is therefore not adequately described by a single `exists / does not exist` predicate.

These are project interpretations. They are not historical claims attributed to Ouchi, Chen et al., Sun, or OpenZFS developers.

---

## Source ownership and next work

Historical source details remain in the grounded evidence records linked from Cases 17, 18, 94, 96, and 100. This synthesis deliberately does not duplicate their bibliographies.

Still-open work includes:

- named production-controller rebuild/crash behavior;
- URE-aware and correlated-failure policy;
- rebuild throttling and foreground-workload interaction;
- fault-injected verification of repair/currentness metadata;
- wider erasure-coded distributed systems where content repair and failure-domain placement converge on different schedules;
- a broader RAID / parity-declustering / distributed-sparing history in `computing-archaeology` if that repository takes up the topic.

Those are additional research slices, not blockers for the bounded relation decomposition completed here.
''', encoding="utf-8")

insert_after_prefix_line(
    README,
    "A focused Flash/SSD comparison is now available in [`docs/SYNTHESIS_06_FLASH_READ_PATH_VS_RENEWAL.md`]",
    "A bounded coded-storage recovery comparison is now available in [`docs/SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md`](docs/SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md). Across grounded RAID/ZFS cases it separates failure/currentness evidence, mathematical reconstructability, degraded request service, repair-scope selection, reconstruction geometry, restored redundancy margin, and later integrity verification."
)

insert_before(
    ROADMAP,
    "Coordinate with `computing-archaeology` rather than duplicating it.",
    "- [x] Coded-recoverability / degraded-service / repair-margin synthesis — [`docs/SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md`](docs/SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md) closes the bounded relation-decomposition question across grounded Cases 17, 18, 94, 96, and 100. It separates failure/currentness evidence, algebraic reconstructability, degraded request service, repair-scope selection, reconstruction geometry/bandwidth, restored redundancy margin, and post-rebuild integrity verification; it also fixes `code strength ≠ repair scope ≠ reconstruction geometry`. This is cross-case engineering synthesis, not a RAID/ZFS genealogy. Controller products, URE-aware policy, correlated failures, rebuild throttling, field fault injection, and broader parity-declustering/distributed-sparing history remain open."
)

replace_prefix_line(
    ROADMAP,
    "- [ ] How should `encoded reconstructability`, `degraded-service continuity`, and `restored redundancy margin` be separated in coded-storage regimes?",
    "- [x] In coded-storage recovery, separate `failure/location evidence`, `coded-currentness`, `encoded reconstructability`, `degraded-service continuity`, `repair-scope selection`, `reconstruction geometry/bandwidth`, `repaired embodiment`, `restored redundancy margin`, and later `integrity revalidation` — closed at the bounded cross-case level by [`docs/SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md`](docs/SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md), synthesizing grounded Cases 17, 18, 94, 96, and 100. Named-controller behavior, URE/correlated-failure policy, production fault injection, and broader RAID history remain separate work."
)

insert_after_prefix_line(
    INDEX,
    "1364. **later controller composition ≠ 1999 device history or JEDEC chronology**",
    """1365. **failure model, service model, and repair model are independent axes** — a coded state can remain mathematically reconstructable, be request-serviceable in degraded mode, and still owe physical reconstruction before ordinary redundancy margin is restored.\n1366. **code strength ≠ repair scope** — an extra independent syndrome changes which known-erasure combinations are solvable, while DTL-like exposure history changes which current blocks need catch-up.\n1367. **repair scope ≠ reconstruction geometry** — temporal pruning of the repair set and dRAID-style distribution/sequentialization of selected work reduce different components of recovery cost.\n1368. **reconstruction geometry ≠ code strength** — a layout can shorten the reduced-redundancy interval without increasing the number of independent erasures the code tolerates.\n1369. **failure-location/currentness evidence is constitutive recovery state, not redundant payload** — P+Q solving needs failed positions, while surviving parity/syndromes must still be qualified as belonging to the current coded relation.\n1370. **integrity confidence can lag redundancy restoration** — sequential reconstruction can restore the configured redundancy relation before a later checksum scrub completes stronger verification.\n1371. **redundancy margin has algebraic and temporal dimensions** — code distance bounds tolerated failure combinations, while repair design controls how long a system remains at reduced margin after a failure consumes part of that tolerance; neither dimension substitutes for the other.\n1372. **cross-case recovery pipeline ≠ historical genealogy** — failure evidence → reconstructability → degraded service → repair selection/execution → restored margin → verification is an analytical decomposition, not a claim that Berkeley RAID, ZFS, Linux RAID-6, and OpenZFS share one implementation lineage."""
)

# Sanity checks for the bounded navigation/status update.
assert "SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md" in read(README)
assert "SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md" in read(ROADMAP)
assert "1372. **cross-case recovery pipeline" in read(INDEX)
for rel in [
    "cases/17-raid-parity-reconstruction-degraded-repair.md",
    "cases/18-zfs-scrub-latent-error-detection.md",
    "cases/94-raid6-pq-dual-erasure-corruption-boundary.md",
    "cases/96-openzfs-draid-distributed-spare-sequential-resilver.md",
    "cases/100-zfs-dirty-time-log-selective-resilver.md",
]:
    assert (ROOT / rel).exists(), rel
