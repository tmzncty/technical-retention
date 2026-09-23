# Case 24 evidence index — Windows Azure Storage LRC

## Scope

This index is the navigation page for [`Case 24 — Windows Azure Storage LRC repair locality and redundancy-mode handoff`](../cases/24-windows-azure-lrc-repair-locality-handoff.md).

**Current maturity:** `grounded`.

The case is bounded to the Windows Azure Storage design reported by Huang et al. at USENIX ATC 2012. It is not a general history of Azure Storage, erasure coding, Reed–Solomon codes, locally repairable codes, cloud-storage garbage collection, or modern Azure durability semantics.

The evidence chain currently answers two different questions:

1. what makes LRC repair geometry and replica→coded conversion a distinct retention regime;
2. when the old full-replica representation becomes eligible for retirement, and how that differs from later physical deletion/reclamation.

---

## Canonical files

- Case: [`../cases/24-windows-azure-lrc-repair-locality-handoff.md`](../cases/24-windows-azure-lrc-repair-locality-handoff.md)
- Grounding: [`24-windows-azure-2012-lrc-grounding.md`](24-windows-azure-2012-lrc-grounding.md)
- Source-retirement deepening: [`24-was-2012-source-replica-retirement-authority-boundary-deepening.md`](24-was-2012-source-replica-retirement-authority-boundary-deepening.md)
- Cross-case distributed-coded synthesis: [`../docs/SYNTHESIS_09_DISTRIBUTED_CODED_SERVICE_REPAIR_PLACEMENT.md`](../docs/SYNTHESIS_09_DISTRIBUTED_CODED_SERVICE_REPAIR_PLACEMENT.md)

---

## Primary source

Cheng Huang, Huseyin Simitci, Yikang Xu, Aaron Ogus, Brad Calder, Parikshit Gopalan, Jin Li, and Sergey Yekhanin, **“Erasure Coding in Windows Azure Storage,”** *2012 USENIX Annual Technical Conference*, June 2012, pp. 15–26.

- USENIX record: <https://www.usenix.org/conference/atc12/technical-sessions/presentation/huang>
- USENIX PDF: <https://www.usenix.org/system/files/conference/atc12/atc12-final181_0.pdf>
- Microsoft Research record: <https://www.microsoft.com/en-us/research/publication/erasure-coding-in-windows-azure-storage/>

The current case does not need a broader Azure chronology to support its bounded claims.

---

## Evidence chain 1 — LRC repair geometry and representation handoff

**File:** [`24-windows-azure-2012-lrc-grounding.md`](24-windows-azure-2012-lrc-grounding.md)

### Direct historical anchors

The 2012 paper directly supports:

- active stream-layer data initially retained by three full replicas;
- immutable sealed extents selected for asynchronous background erasure coding;
- `LRC (12,2,2)` as the production example;
- reconstruction cost as a first-class code property;
- local-group reconstruction reducing the read dependency set relative to the compared `RS (12,4)` path;
- LRC being non-MDS, so locality is not free extra fault tolerance;
- persisted coding progress that allows another EN to resume an interrupted conversion;
- decode/CRC qualification before erasure coding is allowed to complete;
- fragment-boundary/completion metadata at the Stream Manager;
- on-demand reconstruction for foreground service versus system-initiated durable fragment replacement;
- separate fault-domain and upgrade-domain placement;
- scheduling/throttling of background maintenance work.

### Bounded engineering relations

```text
recoverable
    != cheap-to-reconstruct

code-local dependency set
    != physical co-location

foreground reconstruction availability
    != durable fragment repair

some coded fragments exist
    != coded representation accepted/current

representation transition
    != stateless format conversion
```

### Status

**Grounded.** This is the maturity-bearing evidence chain for Case 24.

Remaining work here is not “find another generic LRC explanation.” Useful additions must sharpen a still-open transition, fault, or authority boundary.

---

## Evidence chain 2 — source-replica retirement authority vs deletion/reclamation

**File:** [`24-was-2012-source-replica-retirement-authority-boundary-deepening.md`](24-was-2012-source-replica-retirement-authority-boundary-deepening.md)

### Direct historical anchors

The detailed 2012 implementation account says:

```text
coding progress persisted
    -> entire extent coded
    -> decode / CRC checks before EC completion
    -> coded fragments persisted on storage disks
    -> coordinator notifies Stream Manager
    -> extent metadata gets fragment boundaries + completion flags
    -> Stream Manager schedules full replicas for deletion
```

The negative path is equally important:

```text
validation failure
    -> abort erasure coding
    -> leave full extent copies intact
    -> schedule another coding attempt later
```

### New bounded distinction

The source uses the phrase **“schedules full replicas ... for deletion.”** It does not in the inspected passages provide the later deletion/reclamation state machine.

Therefore:

```text
coded-state qualification
    != coded-state publication/currentness
    != source-replica retirement eligibility
    != deletion scheduling
    != physical deletion
    != allocator/storage reclamation
    != sanitization
```

### Project vocabulary boundary

`retirement authority` and `retirement eligibility` are modern repository terms. Huang et al. use `completion flags`, `no longer needed`, and `schedules ... for deletion`.

### Status

**Bounded deepening complete.** It does not change Case 24 maturity beyond `grounded`.

The historical paper is strong enough to close the permission/scheduling distinction, but not the cleanup-execution or reclamation-completion questions.

---

## Cross-case routing

### Case 19 — Facebook f4

Use Case 19 when the question is repair/service/placement **inside an already erasure-coded regime**.

Use Case 24 when the question is an actual **redundancy-regime transition**:

```text
full replication
    -> validated coded representation
```

Do not collapse the two.

### Case 25 — OpenStack Swift EC

Case 25 is the stronger source-code-level comparison for replacement/current placement evidence before local handoff purge.

Use it as a **functional analogy**, not a historical lineage claim.

### Case 04 — mapped Flash

Case 04 offers the lower-layer functional pattern:

```text
replacement embodiment established/current
    -> old embodiment later becomes reclaimable
```

Again, this is a relation-level comparison only. Flash mapping/erase and distributed EC conversion are not the same mechanism.

---

## Terms to preserve

### Historical terms from the 2012 paper

- `extent`;
- `sealed`;
- `replica set`;
- `erasure coding`;
- `Local Reconstruction Codes (LRC)`;
- `reconstruction cost`;
- `Stream Manager (SM)`;
- `Extent Node (EN)`;
- `coordinator`;
- `fragment boundaries`;
- `completion flags`;
- `fault domain`;
- `upgrade domain`;
- `CRC`;
- `scheduled for deletion`.

### Repository engineering terms

- `repair-cost geometry`;
- `redundancy-mode handoff`;
- `transition gate`;
- `redundancy-regime currentness`;
- `source-replica retirement authority`;
- `retirement eligibility`;
- `reclamation completion`.

Do not back-project the second list into the 2012 authors' vocabulary.

---

## Current status and roadmap effect

Case 24 remains **`grounded`**.

This round advances the open ROADMAP failure-mode item concerning:

> failed/asynchronous redundancy-mode conversion, stale/incomplete completion metadata, or deleting source replicas before coded-state validation.

What is now grounded at the 2012 source level:

```text
source replicas remain intact on validation failure

validated / accepted coded state
    precedes
source replicas being scheduled for deletion

scheduled for deletion
    != demonstrated physical deletion/reclamation completion
```

What remains open:

- stale/corrupt/incomplete Stream Manager completion metadata;
- crash after coded-state publication but before deletion intent is durably retained;
- crash during or after partial source-replica deletion;
- cleanup retry/idempotence mechanics;
- an externally observable deletion-completion or capacity-reclamation signal;
- coexistence duration / capacity-headroom traces;
- independent fault injection.

The broad ROADMAP item therefore remains open. This index records a narrower closed sub-boundary without marking the whole failure family complete.

---

## Next highest-value evidence

Prefer one of these before adding more generic LRC material:

1. a Microsoft primary source that exposes post-publication source-replica deletion/retry behavior;
2. a trace or implementation description showing how stale/incomplete conversion metadata is detected or repaired;
3. a production measurement of replica/coded-fragment coexistence and cleanup lag;
4. a fault experiment around publication → deletion scheduling → deletion execution.

If the work broadens into Azure Storage product history, LRC coding genealogy, or general distributed-storage evolution, route that history to `tmzncty/computing-archaeology` and keep only the retention-specific evidence bridge here.
