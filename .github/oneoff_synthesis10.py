from pathlib import Path

SYNTHESIS = r'''# Synthesis 10 — Mutable EC Currentness: Fragment Presence, Commit Authority, Retirement, and Repair Convergence

## Scope

This is a **bounded retention synthesis**, not a new historical case and not a genealogy of erasure coding, object stores, commit protocols, or OpenStack Swift.

It closes one relation-decomposition question already present in the roadmap:

> In mutable erasure-coded object storage, how should `fragment presence`, `version/timestamp coherence`, `coded reconstructability`, `commit/durability evidence`, `old-version retirement`, and `repair convergence` be separated?

The principal historical witness is the already-grounded [Case 25 — OpenStack Swift EC overwrite/currentness](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md), with its [grounding record](../evidence/25-openstack-swift-2015-2016-ec-currentness-grounding.md). [Case 19 — Facebook f4](../cases/19-facebook-f4-erasure-coded-failure-domains.md) and [Case 24 — Windows Azure Storage LRC](../cases/24-windows-azure-lrc-repair-locality-handoff.md) are used only as **immutable coded-storage controls** already synthesized in [Synthesis 09](SYNTHESIS_09_DISTRIBUTED_CODED_SERVICE_REPAIR_PLACEMENT.md).

Historical vocabulary remains local to the sources. Terms such as `timestamp cohort`, `admissible coded version`, `version-retirement gate`, and `coded currentness` are project **engineering reconstructions (`E`)**, not claims about Swift developers' period terminology.

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for Swift/erasure-coding overlap found no dedicated case in the current repository search surface. Broader Reed–Solomon history, object-store genealogy, distributed commit history, or OpenStack implementation history should therefore be developed there rather than recreated here if needed.

---

## Primary-source anchors

The bounded historical record is already grounded in the Case-25 evidence file. The main source anchors are:

- OpenStack Swift **2.3.0**, `doc/source/overview_erasure_code.rst`, signed release tag 30 April 2015: <https://github.com/openstack/swift/tree/2.3.0>.
- OpenStack Swift **2.10.1**, `Erasure Code Support`: <https://files.openstack.org/docs/swift/2.10.1/overview_erasure_code.html>.
- OpenStack Swift **2.11.0** changelog, used here only as a later implementation-continuity witness: <https://github.com/openstack/swift/blob/2.11.0/CHANGELOG>.

The 2.11.0 changelog is especially useful because it changes the **representation** of durable state without making the underlying currentness/commit relation disappear: instead of a separate `.durable` file, Swift renames the fragment `.data` filename to include a durable marker; existing `.durable` files remain supported. This later witness must not be back-projected into 2.3.0 or 2.10.1 on-disk details.

---

## Historical records kept separate

### Swift 2.3.0 — fragment landing can precede successful object retention

The 2.3.0 EC documentation describes a multi-phase PUT. Fragment archives can be written before the proxy has established the quorum needed for successful completion. Its partial-PUT discussion explicitly allows a proxy failure to leave fragment `.data` files on storage nodes even though the client never received a successful PUT and the system does not know that a reconstructable committed set exists.

That blocks the shortcut:

```text
fragment bytes exist on disk
    ≠
object version successfully retained under the EC protocol
```

The same documentation delays deletion of older timestamped files until commit confirmation for the replacement. New bytes can therefore exist while the older version is still intentionally protected.

### Swift 2.10.1 — same-version coding algebra is qualified by durability/currentness evidence

The 2.10.1 documentation sharpens both PUT and GET semantics.

For PUT, the first phase requires `ec_ndata + 1` fragment archives to land; the proxy then sends commit confirmations; storage nodes create `<timestamp>.durable`; and the second phase requires `ec_ndata + 1` successful commits before the proxy reports success. The reconstructor may later propagate missing durability markers.

For GET, algebraic sufficiency is not evaluated over arbitrary surviving fragment files. The proxy seeks enough **distinct fragment indexes at the same timestamp**, together with same-timestamp durability evidence. Nodes can hold archives from several timestamps and can return duplicate fragment indexes, so physical plurality is not itself a valid decode cohort.

The resulting relation is:

```text
physical fragment presence
    → fragment validity
    → same-version/timestamp membership
    → distinct-index compatible set
    → algebraic reconstructability
    → commit/durability qualification
    → service-admissible coded version
```

This is a diagnostic decomposition, not Swift's own formal state machine.

### Swift 2.10.1 — durability is a relation over a coded set, not a property of every payload fragment

The documentation describes `.durable` as evidence that matching data has enough committed fragment archives somewhere to reconstruct the object. A GET does not require every contributing fragment's local node to carry its own `.durable` file; same-timestamp durability evidence can qualify a distributed cohort.

That makes the bounded engineering point:

> `durability/currentness evidence` can be **relation-level control state** whose scope is larger than one fragment embodiment.

The marker is not the payload, and the payload fragments alone do not contain the complete admissibility relation.

### Swift 2.11.0 — the durability relation survives a metadata-representation change

The 2.11.0 changelog records a deliberate on-disk change: Swift stopped needing one separate `.durable` file per EC archive and instead encoded durable status by renaming the `.data` filename to include a durable marker. The same changelog says existing `.durable` files remain valid.

This supplies a useful later counterexample to reifying one metadata encoding:

```text
retained durability/currentness relation
    ≠
one permanent on-disk marker representation
```

The bounded claim is continuity of an externally meaningful control relation across a Swift implementation change. It is **not** a claim that 2.11.0 was wire/on-disk compatible with every older version; the changelog explicitly warns that data written by 2.11.0 or later is not accessible to earlier Swift versions.

---

## Engineering reconstruction: ten typed relations

The labels below are project vocabulary (`E`). They are not attributed to Swift, Facebook, Microsoft, or coding theory as shared historical terms.

### 1. Fragment physical presence

Does a fragment archive embodiment exist on some storage node?

Presence is the weakest positive fact. A stale pre-commit archive, an invalid archive, a duplicate index, or a fragment from the wrong timestamp can all satisfy it.

### 2. Fragment local validity

Does the local archive pass the implementation's fragment-length/metadata/integrity checks strongly enough to remain a candidate input?

Case 25's 2.10.1 fix supplies the counterexample that a physically present archive can still be quarantined or rejected.

### 3. Version / timestamp coherence

Do candidate fragments belong to one object version rather than several overwrite generations?

A mutable object name can have several timestamped coded cohorts present at once. Coding algebra does not decide which generation is current.

### 4. Fragment-index complementarity

Does the candidate same-version set contain the distinct indexes needed by the code rather than several copies of the same contribution?

Replica count and useful coded degrees of freedom are different quantities.

### 5. Algebraic reconstructability

Given one compatible version cohort, does the surviving distinct-index set contain enough information to decode the object?

This is the coding-theory relation. It still does not establish that the decoded version is the committed/current one the service may return.

### 6. Commit / durability qualification

Has the coded version crossed the implementation's commit boundary and acquired the durability evidence required by the normal object path?

In the bounded Swift release this relation is represented by timestamped durability state produced after the fragment-landing phase. The exact quorum threshold is release-specific protocol policy, not a timeless theorem of erasure coding.

### 7. Service admissibility / client-visible completion

May the normal service return this coded version, or report the replacement PUT as successful?

This depends on more than raw fragment count. It composes version qualification, coding sufficiency, and the release-specific commit contract.

### 8. Old-version retirement authority

Has the replacement crossed the gate that allows older timestamped object state to be deleted from the object-store namespace/on-disk set?

The newer timestamp and the existence of newer fragment files are weaker facts. Case 25's commit-gated deletion makes replacement retention a prerequisite for authorized forgetting of the predecessor.

### 9. Repair / metadata convergence

After the version is already service-admissible, have missing fragment archives, durability state, and handoff placements converged toward the intended steady state?

The reconstructor can continue this work after the foreground PUT/GET relation is already usable. Repair convergence is therefore not identical to the original commit event.

### 10. Physical cleanup / sanitization

Have obsolete embodiments actually been reclaimed or securely erased below the object-store relation?

Logical deletion of old timestamped files does not establish overwrite, Flash-block erase, drive sanitization, or forensic absence. Lower-layer forgetting remains a different question.

---

## Compact relation map

```text
fragment exists
    ↓
locally valid candidate
    ↓
same timestamp / version cohort
    ↓
distinct compatible indexes
    ↓
algebraically reconstructable
    ↓
commit / durability qualified
    ↓
service-admissible current coded version
    ↓
old version becomes retireable
    ↓
repair / marker / handoff convergence
    ↓
object-store cleanup
    ↓
(lower-layer sanitization, if separately performed)
```

The arrows express increasing qualification in this bounded analysis, not a claim that every implementation executes these stages serially or stores one flag for each relation.

---

## Cross-case controls

| Relation | Swift mutable EC, 2015–2016 | f4 immutable warm storage | WAS sealed-extent LRC |
| --- | --- | --- | --- |
| multiple object generations can coexist in bounded case | yes; timestamped overwrite cohorts are central | not the central repair problem | transition is between redundancy representations of a sealed extent |
| algebraic recovery | needs a compatible same-timestamp distinct-index set | reconstructs immutable block/BLOB data | reconstructs sealed-extent fragments |
| additional currentness/commit qualification | explicit durability/currentness evidence | not the canonical issue of Case 19 | handoff validation/completion governs representation transition, not client overwrite currentness |
| foreground service can precede full repair convergence | yes | yes | yes |
| old positive representation retirement | commit-gated older timestamp deletion | not the canonical mechanism | old full replicas retire after coded handoff validation/completion |
| main methodological use | mutable version admissibility and safe retirement | request recovery ≠ block repair ≠ placement restoration | repair cost and representation handoff |

The similarities are **functional comparisons (`A/E`)**, not evidence of direct lineage or one universal EC state machine.

---

## Cross-case findings

### E — fragment presence ≠ fragment validity

A file can survive on disk yet fail archive validation or be quarantined. Physical persistence is not enough to make it a usable coded contribution.

### E — fragment validity ≠ same-version cohort membership

A perfectly valid fragment from another timestamp can still be the wrong input for reconstructing the current object version.

### E — same-version membership ≠ distinct-index sufficiency

Several archives can share one timestamp while duplicating the same fragment index. Multiplicity is weaker than useful coding complementarity.

### E — algebraic reconstructability ≠ committed/current admissibility

Enough compatible fragments can exist to satisfy the code while the object version has not crossed the storage protocol's commit/durability boundary.

### E — durability evidence ≠ one local flag on every contributing fragment

Swift's GET rule can use one same-timestamp durability indication to qualify a distributed cohort containing fragments whose local nodes lack a durability marker. Currentness/durability can therefore be relation-level metadata.

### E — durability relation ≠ fixed metadata representation

The `.durable` file of the bounded 2.10.x implementation and the filename-embedded durable marker introduced in 2.11.0 are different physical encodings of a related control function. Implementation representation must not be confused with the abstract relation it carries.

### E — client-visible success ≠ repair convergence

The foreground commit can succeed before all missing fragment/marker state has propagated. Background reconstruction can still owe work after successful service.

### E — newer timestamp / newer fragment bytes ≠ authority to retire the predecessor

Swift deliberately protects older timestamped state until the replacement crosses the commit boundary. Replacement production and safe source retirement are separate milestones.

### E — retirement authority ≠ completed cleanup

Permission to delete old object-store files is not proof that every stale/handoff/underlying media embodiment has already been reclaimed.

### E — logical retirement ≠ secure erasure

Object-store currentness and file lifecycle say nothing by themselves about lower-layer sanitization.

### E — protocol quorum threshold ≠ code-theoretic minimum

The repository's 2.3.0 versus 2.10.1 comparison already shows commit thresholds changing across Swift releases. A release's safety/service rule must not be normalized into an invariant of the EC scheme.

### E/A — mutable coded currentness ≠ immutable coded-repair pipeline

Synthesis 09 can separate foreground reconstruction, durable repair, placement restoration, and representation handoff for f4/WAS without solving Swift's overwrite-currentness problem. Mutable version selection is an additional axis, not a historical descendant stage that can be inferred from immutable repair semantics.

---

## Relationship to Syntheses 07–09

[Synthesis 07](SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md) separates coded reconstructability from repair scope, reconstruction geometry, restored redundancy margin, and later integrity verification.

[Synthesis 08](SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md) asks when a physically present embodiment should cease to count because integrity verification disqualifies it.

[Synthesis 09](SYNTHESIS_09_DISTRIBUTED_CODED_SERVICE_REPAIR_PLACEMENT.md) separates request-time reconstruction from durable repair and placement/handoff convergence, while deliberately leaving **mutable coded currentness** open.

This synthesis fills that exact seam. It asks what must qualify a coded version **before** normal service and predecessor retirement are legitimate when several overwrite generations may coexist. It therefore complements rather than replaces the repair and integrity syntheses.

---

## Prior-art and genealogy boundary

Nothing here establishes that:

- Swift invented erasure-coded storage;
- Swift invented Reed–Solomon coding;
- Swift invented two-phase commit;
- Swift's documentation phrase `essence of a 2 phase commit` licenses calling the protocol transaction-manager 2PC or strong consistency;
- `.durable` is a universal erasure-coding concept;
- filename-embedded durable status in 2.11.0 is the same on-disk mechanism as the older separate `.durable` file;
- f4, WAS, and Swift form one direct implementation lineage;
- every mutable EC object store must use timestamps or Swift-style durability markers;
- object-store deletion proves secure media erasure.

Cases 19 and 24 already retain the older coding-theory/LRC prior-art boundary. A broader commit-protocol, object-store, or EC implementation genealogy belongs in `computing-archaeology` if pursued.

---

## Why this matters for technical retention

Mutable coded storage makes a useful adversarial case because the same logical object name can be surrounded by many pieces of surviving positive state that are individually real yet jointly insufficient to answer the question **what is the retained current object?**

The answer can depend on relations among:

- surviving bytes;
- local fragment validity;
- version identity;
- coding complementarity;
- commit evidence;
- foreground service rules;
- predecessor-retirement authority;
- later repair convergence.

Retention is therefore not exhausted by asking whether enough bytes remain to decode something. In this bounded case, the system must also retain enough **qualification and transition state** to decide which decodable state counts, when a replacement is trusted, and when the predecessor may legitimately be forgotten.

That conclusion is an **engineering synthesis**. It does not turn Swift's protocol into a universal philosophy of storage.
'''


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    assert count == 1, f'{path}: expected one anchor, found {count}'
    p.write_text(text.replace(old, new, 1), encoding='utf-8')


Path('docs/SYNTHESIS_10_MUTABLE_EC_CURRENTNESS_RETIREMENT_REPAIR.md').write_text(SYNTHESIS, encoding='utf-8')

readme_anchor = '''A bounded distributed-coded-service comparison is now available in [`docs/SYNTHESIS_09_DISTRIBUTED_CODED_SERVICE_REPAIR_PLACEMENT.md`](docs/SYNTHESIS_09_DISTRIBUTED_CODED_SERVICE_REPAIR_PLACEMENT.md). Across grounded f4 and Windows Azure Storage LRC cases, with Swift EC as a mutable-currentness counterexample, it separates algebraic recoverability, reconstruction read-set/cost, foreground recovery, durable fragment repair, failure-domain placement restoration, redundancy-regime handoff completion, and later retirement/convergence.\n'''
readme_new = readme_anchor + '''\nA bounded mutable-EC-currentness comparison is now available in [`docs/SYNTHESIS_10_MUTABLE_EC_CURRENTNESS_RETIREMENT_REPAIR.md`](docs/SYNTHESIS_10_MUTABLE_EC_CURRENTNESS_RETIREMENT_REPAIR.md). Centered on grounded Swift EC Case 25, it separates fragment presence and validity, timestamp/version coherence, distinct-index algebraic reconstructability, commit/durability qualification, service admissibility, old-version retirement authority, repair convergence, and lower-layer cleanup; Swift 2.11.0 additionally shows that the durability relation can survive a change from separate `.durable` files to filename-embedded durable state.\n'''
replace_once('README.md', readme_anchor, readme_new)

roadmap_question = '- [ ] In mutable erasure-coded object storage, how should `fragment presence`, `version/timestamp coherence`, `coded reconstructability`, `commit/durability evidence`, `old-version retirement`, and `repair convergence` be separated?\n'
roadmap_closed = '- [x] In mutable erasure-coded object storage, separate `fragment presence`, `fragment validity`, `version/timestamp coherence`, `distinct-index coded reconstructability`, `commit/durability evidence`, `service admissibility`, `old-version retirement authority`, `repair convergence`, and lower-layer cleanup — closed at the bounded relation-decomposition level by [`docs/SYNTHESIS_10_MUTABLE_EC_CURRENTNESS_RETIREMENT_REPAIR.md`](docs/SYNTHESIS_10_MUTABLE_EC_CURRENTNESS_RETIREMENT_REPAIR.md), centered on grounded Case 25 with Cases 19/24 as immutable controls. Broader object-store/commit genealogy, field fault injection, correlated fragment loss, modern Swift release evolution, and secure-erasure validation remain open.\n'
replace_once('ROADMAP.md', roadmap_question, roadmap_closed)

bridge_old = '''The grounded OpenStack Swift EC bridge adds the mutable coded-currentness relation that the f4 and WAS cases intentionally left open. In the bounded 2015–2016 implementation, fragment archives can exist before a PUT is committed; GET requires enough distinct fragment indexes at one timestamp plus same-timestamp durability evidence; and the previous timestamp is not deleted until the replacement crosses the multi-phase commit boundary. Later reconstruction can still propagate missing fragments and durability markers. Future coded-storage work should therefore distinguish **fragment existence**, **version coherence**, **algebraic reconstructability**, **commit/admissibility state**, **source-version retirement**, and **repair convergence**, while keeping release-specific quorum rules explicit rather than treating `Swift EC durability` as one timeless property.\n'''
bridge_new = '''The grounded OpenStack Swift EC bridge adds the mutable coded-currentness relation that the f4 and WAS cases intentionally left open. In the bounded 2015–2016 implementation, fragment archives can exist before a PUT is committed; GET requires enough distinct fragment indexes at one timestamp plus same-timestamp durability evidence; and the previous timestamp is not deleted until the replacement crosses the multi-phase commit boundary. Later reconstruction can still propagate missing fragments and durability markers. [`docs/SYNTHESIS_10_MUTABLE_EC_CURRENTNESS_RETIREMENT_REPAIR.md`](docs/SYNTHESIS_10_MUTABLE_EC_CURRENTNESS_RETIREMENT_REPAIR.md) now closes that relation decomposition at the bounded cross-case level and adds the Swift 2.11.0 counterexample that durability/currentness semantics can survive a change in their on-disk metadata representation. Broader object-store/commit genealogy, field fault injection, correlated fragment loss, modern Swift evolution, and secure-erasure validation remain open.\n'''
replace_once('ROADMAP.md', bridge_old, bridge_new)

case_index = Path('CASE_INDEX.md')
text = case_index.read_text(encoding='utf-8')
assert text.rstrip().endswith('1394. **immutable coded-repair synthesis ≠ mutable coded-currentness rule or historical genealogy** — Swift supplies a counterexample in which same-timestamp/distinct-index/durability qualification precedes usable decoding; this does not make f4, WAS, and Swift one pipeline or lineage.'), 'CASE_INDEX tail changed; refuse to append blindly'
append = r'''

### Cross-case mutable-EC currentness synthesis — presence, commit, retirement, and convergence

1395. **fragment presence ≠ fragment validity** — an EC archive can physically survive yet fail fragment-length/metadata checks or be quarantined, so embodiment alone does not make it a usable coded contribution.
1396. **fragment validity ≠ same-version cohort membership** — a locally valid archive from another timestamp can still be the wrong input for reconstructing the service-admissible object version.
1397. **same-version multiplicity ≠ distinct-index sufficiency** — several archives at one timestamp can duplicate the same fragment index; physical count is weaker than useful coding complementarity.
1398. **algebraic reconstructability ≠ committed/current admissibility** — enough compatible fragments can satisfy the code while the replacement version has not crossed Swift's release-specific commit/durability boundary.
1399. **durability evidence ≠ one local marker on every contributing fragment** — in the bounded 2.10.1 GET rule, same-timestamp durability evidence can qualify a distributed cohort containing fragments whose local nodes do not each carry a `.durable` marker.
1400. **durability/currentness relation ≠ fixed metadata representation** — Swift 2.11.0 replaces the separate `.durable`-file encoding with filename-embedded durable state while continuing to accept existing `.durable` files; the relation outlives one implementation encoding.
1401. **client-visible commit success ≠ repair convergence** — a version can become service-admissible while the reconstructor still owes propagation/reconstruction of missing fragment or durability state.
1402. **repair convergence ≠ original commit event** — later background reconstruction restores intended steady state after a committed version already exists; it does not retroactively become the event that first authorized that version.
1403. **newer timestamp / newer fragment bytes ≠ authority to retire the predecessor** — Swift protects older timestamped state until the replacement crosses the commit gate.
1404. **old-version retirement authority ≠ completed physical cleanup** — permission to delete older object-store state does not prove that every stale, handoff, filesystem, or media embodiment has already been reclaimed.
1405. **logical old-version retirement ≠ secure erasure** — object-store deletion/currentness transitions establish no overwrite, Flash erase, sanitize-command completion, or forensic absence at lower layers.
1406. **protocol quorum threshold ≠ code-theoretic minimum** — Case 25's 2.3.0/2.10.1 comparison shows Swift commit thresholds changing across releases, so one release's safety/service contract is not a timeless property of erasure coding.
1407. **mutable coded currentness ≠ immutable coded-repair pipeline or historical genealogy** — f4/WAS can illuminate service/repair/handoff distinctions, but coexistence of overwrite generations adds an independent version-admissibility axis and does not make the systems one lineage.
'''
case_index.write_text(text.rstrip() + '\n' + append.lstrip('\n'), encoding='utf-8')
