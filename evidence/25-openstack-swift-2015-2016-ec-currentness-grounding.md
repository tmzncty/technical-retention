# Case 25 grounding — OpenStack Swift EC mutable currentness and `.durable` commit semantics (2015–2016)

## Purpose

This record grounds [`cases/25-openstack-swift-ec-overwrite-durable-currentness.md`](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md).

The evidence target is deliberately narrow. It does **not** ask whether Swift invented erasure coding or whether Swift as a whole is strongly consistent. It asks whether official period source material supports six retention distinctions:

1. fragment bytes physically present versus a successfully committed EC object version;
2. mathematical reconstructability versus a version-qualified admissible fragment set;
3. newer timestamped fragment production versus authority to retire an older timestamp;
4. per-fragment existence versus a set-level `.durable` relation;
5. foreground PUT/GET success versus later fragment/marker convergence and repair;
6. one historical release's durability threshold versus another release's revised threshold.

**Result:** official Swift 2.3.0 and 2.10.1 source/release documentation directly support all six strongly enough for `grounded` status.

---

## Source set

### P1 — OpenStack Swift 2.3.0 signed release tag, 30 April 2015

OpenStack Swift signed tag `2.3.0` points to commit:

`f8dee761bd36f857aa1288c27e095907032fad68`

The annotated tag was created by Thierry Carrez on **2015-04-30T13:57:12Z** and is GitHub-verified.

- tag: <https://github.com/openstack/swift/releases/tag/2.3.0>
- source tree: <https://github.com/openstack/swift/tree/2.3.0>
- exact commit: <https://github.com/openstack/swift/commit/f8dee761bd36f857aa1288c27e095907032fad68>

This fixes the date and exact source state used for the 2015 semantics.

### P2 — Swift 2.3.0 `CHANGELOG`

<https://github.com/openstack/swift/blob/2.3.0/CHANGELOG>

The `swift (2.3.0)` entry directly states:

- EC support is added as a storage-policy type;
- it is transparent at the external API level;
- PyECLib/liberasurecode provide the coding backend;
- EC support is beta;
- it relies on `ssync` for durability;
- deployers are urged to test rather than assume production readiness.

Used to bound maturity and historical status, not to establish the detailed currentness protocol.

### P3 — Swift 2.3.0 EC overview source documentation

`doc/source/overview_erasure_code.rst` at tag `2.3.0`:

<https://github.com/openstack/swift/blob/2.3.0/doc/source/overview_erasure_code.rst>

This is the central primary source for:

- fragment archive naming/indexes;
- `.durable` files;
- the multipart/multi-phase PUT conversation;
- quorum-before-client-success behavior;
- old-timestamp deletion only after commit;
- partial PUT failure behavior;
- reconstruction and handoffs.

### P4 — Swift 2.10.1 EC overview source documentation

`doc/source/overview_erasure_code.rst` at tag `2.10.1`:

<https://github.com/openstack/swift/blob/2.10.1/doc/source/overview_erasure_code.rst>

This source is used because it makes the later same-timestamp/distinct-index GET rule and the tightened `ec_ndata + 1` commit rules explicit.

It is **not** silently merged with P3: where 2015 and 2016 thresholds differ, this grounding record reports both.

### P5 — Swift 2.10.1 release commit / changelog update

Commit `3129a55d4418e0dc4207c2026e7ef8c59704c6a1`, dated **2016-12-12**:

<https://github.com/openstack/swift/commit/3129a55d4418e0dc4207c2026e7ef8c59704c6a1>

Its 2.10.1 changelog/release note records an EC fix in which:

- `ssync` could write bad fragment data under some circumstances;
- a correct-byte-count check was added before finalization;
- EC fragment metadata is validated when read;
- bad fragment data is quarantined.

Used only for the fragment-validity boundary.

### Reused repository prior-art boundary

[`Case 19`](../cases/19-facebook-f4-erasure-coded-failure-domains.md) already retains the Reed–Solomon 1960 coding-theory boundary, and [`Case 24`](../cases/24-windows-azure-lrc-repair-locality-handoff.md) retains LRC/Pyramid-code repair-locality prior art. This record reuses them rather than reproducing a coding-history survey.

---

## Direct-inspection ledger

### P1 — signed release identity

Direct GitHub tag inspection established:

- `refs/tags/2.3.0` is an annotated tag;
- tag object SHA `045cff4b7cbee305d1a7ee688d0accb106bcdd66`;
- target commit `f8dee761bd36f857aa1288c27e095907032fad68`;
- tagger timestamp `2015-04-30T13:57:12Z`;
- GitHub reports a valid verification for the tag.

This supports the exact period boundary used in the case.

### P2 — 2.3.0 maturity boundary

Direct `CHANGELOG` inspection established that EC arrives in Swift 2.3.0 as **beta**, that no external API difference is intended between replication and EC storage, and that the implementation relies on `ssync` plus external erasure-code libraries.

This blocks any claim that the April 2015 source represents already-proven production-scale behavior.

### P3 — fragment-index and `.durable` naming

Direct source inspection established:

- fragment archives of different indexes may coexist on one node;
- fragment index is encoded into the `.data` filename;
- example: `1418673556.92690#5.data`;
- `.durable` is separately timestamp-named, e.g. `1418673556.92690.durable`;
- `.durable` is created alongside fragment data after successful PUT processing.

**Location:** `On Disk Storage`.

### P3 — multi-phase PUT and set-level durability marker

Direct source inspection of `Multi_Phase Conversation` established:

- the proxy needs a conversation with object servers after fragment archives land;
- the goal is to know when a quorum of fragment archives is on disk before client success;
- the document explicitly says this is done `Without introducing strong consistency semantics`;
- the mechanism provides the `essence of a 2 phase commit`;
- after commit confirmation, object servers write `<timestamp>.durable`;
- the marker is described as an indicator of the `last known durable set of fragment archives` for that object timestamp.

The case therefore preserves Swift's own bounded wording and **does not** relabel the mechanism as transaction-manager 2PC or consensus.

### P3 — old version deletion is commit-gated

Direct source inspection established that commit completion signals object servers to delete older timestamp files and explicitly explains why: the system must not delete the older object until the server has confirmation that enough replacement fragments have landed elsewhere for quorum.

This is the strongest direct historical anchor for:

> newer fragment production ≠ authority to retire older retained state.

### P3 — partial pre-commit PUT failure

Direct inspection of `Partial PUT Failures` established:

- a proxy can die after some fragment archives have been written but before commit;
- nodes can therefore contain `.data` archives without knowing that enough other archives exist to reconstruct the object;
- the client has not received 2xx;
- the 2.3.0 behavior treats the PUT as failed and leaves stale fragment archives for later cleanup.

This directly grounds `physical fragment presence ≠ successful object retention`.

### P3 — 2015 commit threshold boundary

The 2.3.0 text describes a looser second-phase rule than later Swift: after the data quorum, only a minimum of two final confirmations are required before proxy success, with the reconstructor expected to propagate missing durability markers.

This is recorded because **the protocol changed**. No case statement treats that threshold as the permanent definition of Swift EC durability.

### P4 — 2016 first/second-phase thresholds

Direct source inspection at `2.10.1` established:

- first phase requires `ec_ndata + 1` successfully stored fragment archives;
- proxy then sends commit confirmation;
- object servers create `ts.durable`;
- second phase requires `ec_ndata + 1` successful commits;
- the documented rationale is that enough committed fragments remain to reconstruct even if one becomes unavailable;
- the reconstructor propagates `.durable` to nodes where it is missing.

This supports a version-specific durability contract rather than one timeless Swift rule.

### P4 — same-timestamp / distinct-index GET rule

Direct source inspection of `GET` established that the proxy seeks:

- `ec_ndata` distinct EC archives;
- all at the **same timestamp**;
- with at least one object server indicating a `<timestamp>.durable` marker for that timestamp.

If the initial primaries do not supply the set, requests expand across remaining primaries and handoffs.

The document further says:

- one object server may have archives from multiple timestamps and/or fragment indexes;
- the proxy may receive archives with different timestamps;
- it may receive several archives carrying the same index;
- it must ensure a sufficient set of **same-timestamp, distinct-index** archives before successful GET.

This is direct support for `coded recoverability ≠ version admissibility`.

### P4 — `.durable` need not be local to every contributing fragment

Direct source inspection established that the proxy does not require every object server contributing an archive to have a local `.durable` marker. One same-timestamp `.durable` indication can qualify the reconstructable cohort.

This supports the engineering reconstruction that the durability fact is **set-level / relation-level**, not simply a property stored inside each payload fragment.

### P4 — reconstruction after availability loss

Direct source inspection established that the reconstructor handles:

- drive failure;
- rebalance movement;
- handoff reversion;
- fragment loss after bit rot.

Unlike replication, reconstructing a missing EC index can require reading sufficient surviving indexes and decoding the needed fragment before sending it to the target node.

This supports the separation between service-level committed/reconstructable state and later steady-state repair.

### P5 — fragment validation / quarantine boundary

Direct commit/changelog inspection established that 2.10.1 fixed a path in which bad fragment data could be written by `ssync`, added a fragment-size completion check, validates EC fragment metadata on read, and quarantines bad fragment data.

The case uses this only to reject:

> file physically exists == fragment is necessarily valid/admissible.

It does **not** attribute the bug to all versions, all devices, or the `.durable` mechanism itself.

---

## Claim-by-claim grounding

| Case-25 claim | Source | Location | Layer | Strength |
| --- | --- | --- | --- | --- |
| Swift 2.3.0 EC was a beta storage-policy feature | P1/P2 | signed tag + 2.3.0 changelog | H/P | direct |
| fragment archive filename records fragment index | P3/P4 | `On Disk Storage` | H/P | direct |
| `.durable` is timestamp-scoped control state | P3/P4 | `On Disk Storage`; `Multi_Phase Conversation` | H/P | direct |
| PUT separates fragment landing from commit confirmation | P3/P4 | `Multi_Phase Conversation` | H/P | direct |
| Swift explicitly avoids claiming strong consistency in this mechanism | P3 | `Multi_Phase Conversation` | H/P boundary | direct |
| old timestamps are deleted only after new commit confirmation | P3/P4 | `Multi_Phase Conversation` | H/P | direct |
| pre-commit proxy failure can leave stale `.data` archives without successful PUT | P3 | `Partial PUT Failures` | H/P | direct |
| 2.3.0 and 2.10.1 commit thresholds differ | P3/P4 | `Multi_Phase Conversation` | H/P | direct |
| 2.10.1 GET requires same timestamp + distinct indexes + durability indication | P4 | `GET` | H/P | direct |
| one same-timestamp `.durable` can qualify archives whose local nodes lack markers | P4 | `GET` | H/P | direct |
| reconstructor can later restore missing fragments/markers | P3/P4 | `Reconstruction` / `The Reconstructor` | H/P | direct |
| physically present fragment can still fail validity checks | P5 | 2.10.1 changelog/release note | H/P | direct |
| coded recoverability does not itself select the current/admissible object version | P4 | same-timestamp/distinct-index GET rule | E | strong reconstruction |
| new fragment presence does not authorize old-version retirement | P3/P4 | commit-gated old deletion + partial PUT | E | strong reconstruction |
| `.durable` participates in a cohort-level currentness/durability relation | P4 | GET uses one same-timestamp marker across distributed archives | E | strong reconstruction |
| client success can precede complete marker/fragment convergence | P3/P4 | commit threshold + later reconstructor propagation | E | strong reconstruction |

---

## Key retention deductions

### D1 — fragment presence ≠ durable object version

**Evidence:** P3 explicitly allows a failed pre-commit PUT to leave fragment `.data` files on disk.

**Inference:** physical embodiment is weaker than successful retention under the object-store protocol.

### D2 — coded recoverability ≠ current-version admissibility

**Evidence:** P4 requires enough **same-timestamp**, **distinct-index** archives plus same-timestamp durability evidence.

**Inference:** the code relation answers `can these complementary symbols decode?`; the storage protocol separately answers `do these symbols belong to one committed object version?`.

### D3 — newer timestamp ≠ safe-forgetting authority

**Evidence:** P3/P4 delay old-timestamp deletion until commit confirmation for the replacement.

**Inference:** chronological/new-version designation is weaker than demonstrated replacement retention.

### D4 — durability/currentness can be a distributed relation

**Evidence:** P4 allows one same-timestamp `.durable` indication to qualify a cohort containing fragments from nodes without their own marker.

**Inference:** no one payload fragment needs to carry the complete fact that its cohort is an admissible retained object.

### D5 — committed availability ≠ complete repair convergence

**Evidence:** missing fragments and `.durable` markers may later be propagated/reconstructed.

**Inference:** service completion and full steady-state redundancy/metadata distribution can be separated.

### D6 — implementation/protocol version ≠ timeless mechanism essence

**Evidence:** P3 and P4 differ in commit thresholds.

**Inference:** any synthesis must retain exact Swift release/version when using quorum/durability semantics.

---

## Prior-art and terminology controls

### Rejected — “Swift invented erasure-coded storage”

Cases 19 and 24 already retain older Reed–Solomon and coded-storage prior art. Swift 2.3.0 itself describes EC as using existing coding theory and external libraries.

### Rejected — “Swift invented two-phase commit”

The source makes no such claim and deliberately says the mechanism has the **essence** of a two-phase commit while not introducing strong consistency semantics. A general transaction-history genealogy is outside this case.

### Rejected — “`.durable` means each fragment is individually durable”

The docs define the marker in terms of a timestamped **set** and 2.10.1 GET can use fragments from nodes without local `.durable` files when a same-timestamp marker is available elsewhere.

### Rejected — “same timestamp means payload bytes alone establish currentness”

The GET rule needs both the fragment cohort and durability evidence. Timestamp, index distinctness, and commit marker are separate retained relations.

### Allowed bounded statement

In Swift's 2015–2016 EC implementation, timestamp/index-qualified fragment archives plus a commit marker are documented mechanisms for deciding which coded object version can be treated as durable/reconstructable through the normal object path, while older timestamped state is protected until the replacement crosses its commit boundary.

---

## Cross-case controls

### Case 23 — Dynamo

Dynamo may intentionally return causally unrelated concurrent versions. Swift EC's bounded GET instead constructs one same-timestamp coded version. Currentness is plural in one regime and cohort-selected in the other.

### Case 24 — Windows Azure LRC

WAS Case 24 moves a **sealed immutable extent** from triple replication to coded retention and validates that representation transition. Swift Case 25 instead exposes mutable client PUT/overwrite under an EC policy and guards replacement of older timestamped coded state.

### Case 17 / Case 19

RAID and f4 demonstrate coded reconstructability and repair, but neither bounded case makes `same object name, several timestamped coded cohorts` the central currentness condition. Swift adds that missing relation.

### Case 18 — ZFS scrub

Swift's auditor/quarantine and reconstructor can interact with corruption, but the central case is not proactive integrity scrubbing. The core contribution is version-qualified coded currentness.

---

## Related-repository duplication check

GitHub code search was run against `tmzncty/computing-archaeology` for a dedicated `OpenStack Swift erasure fragment` treatment. No indexed dedicated result was returned.

That justifies this retention-specific bounded case, but does not prove there is no remotely related object-storage material in that repository.

Routing remains:

- broad Swift architecture, OpenStack release history, PyECLib/liberasurecode genealogy, and generic EC history → `computing-archaeology` if developed;
- mutable coded-version admissibility, durability markers, and safe old-version retirement → `technical-retention`.

---

## Inspection boundary

All central claims in this grounding record come from **official OpenStack Swift source/release material** retrieved at exact repository tags/commits.

No PDF or facsimile is involved in this case. No screenshot/layout claim is made.

The release documents are implementation documentation rather than a formal external standards specification. Accordingly, this case grounds what the Swift project documented for these source states; it does not infer universal object-store guarantees beyond them.

---

## Unsupported / deliberately withheld claims

- `Swift EC is strongly consistent` — **withheld / source boundary rejects this shortcut**.
- `Swift's multipart conversation is identical to database two-phase commit` — **withheld**.
- `every later Swift release uses standalone .durable files with exactly these semantics` — **withheld**; later implementation evolved.
- `all physically reconstructable fragments from different timestamps would decode to garbage` — **not needed and withheld**; the implementation's same-timestamp rule is the historical fact.
- `a 2.3.0 client success means every intended fragment and durability marker is already present` — **withheld**; the source explicitly assigns later propagation/repair work to the reconstructor.
- `file deletion of an old timestamp is secure physical erasure` — **withheld**.
- `2.10.1 fragment-validation fixes prove the 2.3.0 protocol was unsafe` — **withheld**.

---

## Status decision

**Case status: `grounded`.**

Reason:

- exact signed release anchor for the initial EC implementation;
- official implementation documentation for fragment/index/marker semantics;
- direct partial-failure counterexample;
- exact later source documenting same-timestamp/distinct-index GET selection;
- explicit release-to-release threshold distinction;
- direct implementation evidence for repair and fragment validity;
- prior-art and strong-consistency boundaries kept explicit;
- related-repository duplication checked.

Further work should be a separate bounded case if it addresses later on-disk `#d` durability markers, tombstones/versioned-writes, EC shard ranges, or another consistency regime. Do not expand this case into a complete Swift history.
