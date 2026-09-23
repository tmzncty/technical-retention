# Case 24 deepening — Windows Azure Storage source-replica retirement authority boundary (2012)

## Purpose

This is a narrow follow-on to [`cases/24-windows-azure-lrc-repair-locality-handoff.md`](../cases/24-windows-azure-lrc-repair-locality-handoff.md) and [`24-windows-azure-2012-lrc-grounding.md`](24-windows-azure-2012-lrc-grounding.md).

The existing Case 24 grounding already establishes that Windows Azure Storage (WAS) moved sealed immutable extents from three full replicas to Local Reconstruction Code (LRC) fragments through an asynchronous, resumable, CRC-checked transition. This note asks one smaller question:

> **What exactly does the 2012 paper establish before the old full replicas become eligible for retirement, and what does it *not* establish about the later physical deletion/reclamation step?**

The answer matters because the detailed implementation text says that after coding completes and the Stream Manager updates extent metadata, the old replicas are **“scheduled for deletion.”** That is a weaker and more useful historical statement than silently rewriting the source as “the old bytes are now gone.”

**Bounded result:** the paper directly supports a validation-and-publication gate before source-replica retirement is scheduled. It does **not** provide enough detail to equate retirement eligibility, deletion scheduling, physical deletion, storage-space reclamation, or secure sanitization.

Case 24 remains **`grounded`**. This note deepens one already-grounded boundary; it does not justify a maturity promotion.

---

## Source set

### P1 — Huang et al., USENIX ATC 2012

Cheng Huang, Huseyin Simitci, Yikang Xu, Aaron Ogus, Brad Calder, Parikshit Gopalan, Jin Li, and Sergey Yekhanin, **“Erasure Coding in Windows Azure Storage,”** *2012 USENIX Annual Technical Conference*, June 2012, pp. 15–26.

- USENIX record: <https://www.usenix.org/conference/atc12/technical-sessions/presentation/huang>
- USENIX paper PDF: <https://www.usenix.org/system/files/conference/atc12/atc12-final181_0.pdf>
- Microsoft Research record: <https://www.microsoft.com/en-us/research/publication/erasure-coding-in-windows-azure-storage/>

The two sections used here are deliberately small:

- PDF p. 7, §4.2, for persisted conversion progress, Stream Manager notification, extent-metadata update, completion flags, and scheduling of the full replicas for deletion;
- PDF p. 9, §4.4 `Consistency of Coded Data`, for decode/CRC validation, coded-fragment persistence, abort-on-failure, preservation of the full copies, and retry.

Both relevant PDF pages were directly rendered and inspected in this research pass. No claim here depends only on a search-result snippet.

### Reused repository boundaries

- [`Case 19`](../cases/19-facebook-f4-erasure-coded-failure-domains.md) is reused for the contrast between an already-coded regime and Case 24's **replication → coding** representation transition.
- [`Case 25`](../cases/25-openstack-swift-ec-overwrite-durable-currentness.md) is used only as a later functional comparison for “replacement/current placement evidence before source retirement.”
- [`Case 04`](../cases/04-flash-virtual-mapping-logical-identity.md) is used only as a functional comparison for “replacement embodiment publication before old embodiment reclamation.”

No historical genealogy between those systems is asserted.

---

## Historical record

### H/P — coding progress can survive a worker failure before the representation transition completes

In §4.2, the coordinator Extent Node (EN) chooses fragment boundaries, communicates them to the target ENs, and sends encoded fragments to their destinations. The coordinator and target ENs **track progress and persist that progress into each new fragment**. If failure occurs during the process, another EN can continue from the progress information retained in the fragments.

That gives the conversion an explicit intermediate state:

```text
source full replicas still exist
    + some coded work already exists
    + persisted progress describes how far conversion has advanced
    != completed coded representation
```

This note therefore does not treat “some fragments have been written” as the retirement gate.

**Primary anchor:** P1, PDF p. 7, §4.2.

### H/P — the detailed completion path updates extent metadata before source replicas are scheduled for deletion

The same §4.2 says that **after an entire extent is coded**, the coordinator EN notifies the Stream Manager (SM). The SM then **updates the metadata of the extent with fragment boundaries and completion flags**. The next sentence states that **finally** the SM schedules the full replicas of the extent for deletion because they are no longer needed.

The narrow historical sequence is therefore:

```text
entire extent coded
    -> coordinator notifies SM
    -> SM updates extent metadata
       with fragment boundaries + completion flags
    -> SM schedules full replicas for deletion
```

The exact historical phrase `schedules ... for deletion` is retained intentionally.

**Primary anchor:** P1, PDF p. 7, §4.2.

### H/P — conversion has an integrity gate before EC is allowed to complete

The `Consistency of Coded Data` subsection adds a condition that the p. 7 high-level sequence alone does not expose.

After erasure encoding, the coordinator tries several decoding combinations from memory. Reconstructed fragments are checked by CRC. It also computes a CRC across the final data fragments and compares it with the original CRC for the full extent.

The paper explicitly says these validations are performed **before allowing the EC to complete**.

For the production `LRC (12,2,2)` example, the checks include:

- local-group reconstruction checks;
- reconstruction using each global parity path;
- multiple-data-fragment reconstruction checks;
- CRC comparison for decoded fragments;
- a final full-data CRC comparison against the original extent.

**Primary anchor:** P1, PDF p. 9, §4.4 `Consistency of Coded Data`.

### H/P — validation failure keeps the old full copies intact

The same subsection gives a direct negative-path witness. If the validation process detects a failure, the erasure-coding operation is aborted, **the full extent copies remain intact**, and the SM schedules the coding operation to be tried later on another EN.

This is stronger than merely saying that three replicas happened to coexist during background coding. It shows that the old representation has a deliberate retention role while the new representation is still unqualified.

```text
new coded work exists
    + validation fails
    -> abort conversion
    -> retain full copies
    -> retry later
```

**Primary anchor:** P1, PDF p. 9, §4.4.

### H/P — successful checks lead to coded fragments being persisted on storage disks

The paper says that if the checks pass, the resulting coded fragments are persisted on storage disks. Read together with §4.2, this gives a source-supported transition from produced/checked coded state toward the later SM completion-metadata update and source-replica retirement scheduling.

This note does **not** infer a lower-level disk-cache/flush contract from the word `persisted`. The paper is an architecture/production-system account, not a block-interface persistence specification.

**Primary anchor:** P1, PDF p. 9, §4.4.

### H/P — the introduction's “deleted” summary does not erase the more precise implementation boundary

The paper's introduction summarizes the scheme by saying that once a sealed extent is erasure-coded, the original three full copies are deleted.

The detailed implementation section is more precise about the immediate control-plane action: after coding and metadata update, the SM **schedules** the full replicas for deletion.

Both statements can be true at different levels of abstraction. For this retention question, the detailed implementation wording is the stronger anchor because it exposes an intermediate state between “old replicas no longer needed” and “physical storage has definitely been reclaimed.”

**Primary anchors:** P1, PDF p. 1, Introduction; PDF p. 7, §4.2.

---

## Historical sequence reconstructed from the two implementation sections

Taken together, the directly documented steps support this conservative ordering:

```text
three full replicas of a sealed immutable extent
    |
    v
background LRC fragment production
    |
    +--> coding progress persisted in new fragments
    |       so another EN can resume after failure
    v
encoding reaches a candidate-complete coded state
    |
    v
multiple decode / CRC validation checks
    |
    +--> failure:
    |       abort EC
    |       keep full extent copies intact
    |       retry later
    |
    +--> success:
            coded fragments persisted on storage disks
            |
            v
            coordinator notifies Stream Manager
            |
            v
            extent metadata updated with
            fragment boundaries + completion flags
            |
            v
            full replicas scheduled for deletion
```

The ordering across the p. 7 and p. 9 descriptions is reconstructed conservatively from the paper's own `before allowing the EC to complete` language and its statement that validation failure aborts coding while preserving the full copies. It is not a claim about undocumented internal transaction boundaries.

---

## Engineering reconstruction

Everything in this section is project vocabulary. It should not be quoted as Microsoft terminology from 2012.

### E — source replicas function as a transition reserve until the coded representation is qualified

During conversion, the old full replicas are not merely redundant historical debris. The documented failure path relies on them remaining intact when coding validation fails.

A useful engineering description is therefore:

```text
source replicas
    = fallback retention reserve
      while replacement coded representation
      is still being produced / checked / published
```

This is **not** a statement that all three full replicas are consulted for every successful coding operation, nor that their only purpose during the transition is rollback.

### E — retirement authority is a permission relation, not a physical event

This repository uses **source-replica retirement authority** or **retirement eligibility** for the bounded condition under which the old representation is no longer needed as the current retention regime and may be handed to cleanup/deletion work.

The term is useful because the historical paper exposes at least three separable moments:

```text
coded representation qualified/current
    != old replicas scheduled for deletion
    != old replicas physically gone
```

`Retirement authority` is therefore a modern analytical label for the first permission boundary. The paper itself uses `completion flags`, `no longer needed`, and `schedules ... for deletion`.

### E — validation and publication are different obligations

The p. 9 checks answer a data-integrity / reconstructability question: can the coded result successfully restore data under the tested decode combinations and CRC comparisons?

The p. 7 SM update answers a control-plane representation question: what fragment boundaries and completion state should the system now record for this extent?

These are related but not interchangeable:

```text
coded bytes pass validation
    != system metadata has published the coded layout/current state
```

The source does not say that a successful CRC check alone permits the old replicas to be discarded.

### E — retirement eligibility, retirement execution, and reclamation completion are distinct predicates

For later comparisons, use the following predicate split:

```text
P0: source full replicas physically exist
P1: coded fragments have been produced
P2: coded result passes required decode / CRC checks
P3: coded fragments are persisted according to WAS's documented operation
P4: SM records fragment boundaries + completion flags
P5: source replicas are scheduled for deletion
P6: source-replica deletion actually executes
P7: storage allocation/capacity is reclaimed for reuse
P8: old physical embodiments are sanitized against recovery
```

P1–P5 are supported to varying degrees by the paper.

P6–P8 are **not** established by the inspected passages.

The central boundary is:

```text
retirement eligibility / scheduling
    != retirement execution
    != reclamation completion
    != sanitization
```

### E — “completion flag” should not be inflated into a universal durability theorem

The paper names completion flags in extent metadata, but it does not specify in the inspected passages:

- the exact record layout;
- an atomic transaction joining metadata update and deletion scheduling;
- how the update is flushed through every underlying persistence layer;
- whether deletion scheduling has a separately persisted queue entry;
- how a crash in each post-publication cleanup window is replayed.

Accordingly:

```text
completion flag present
    != proof of every lower-layer durability guarantee
```

The completion metadata is still important as **system-level currentness/admissibility evidence** in the published design.

---

## Failure-boundary audit

### F1 — worker failure during coding

**Documented response:** conversion progress is persisted in new fragments and another EN can resume.

**Supported conclusion:** worker/process placement of the conversion task is not itself the only retained state required to continue the transition.

**Not established:** exact crash consistency of every progress-field update or every partially written fragment.

### F2 — coding/integrity validation failure

**Documented response:** abort coding, leave full extent copies intact, schedule another coding attempt later.

**Supported conclusion:** old full replicas remain the safer representation when the candidate coded representation does not pass the qualification gate.

### F3 — crash after coded fragments pass checks but before SM metadata publication

The inspected paper does not explicitly walk this crash window.

A safe repository statement is only:

```text
candidate coded state may exist
    != source retirement authority has been demonstrated
```

Do not invent a rollback/replay protocol for this interval.

### F4 — crash after SM metadata publication but before deletion scheduling is durably retained

The inspected source does not define this boundary either.

Open questions include:

- whether the cleanup intent is derived by scanning metadata;
- whether deletion scheduling is itself logged/persisted;
- whether repeated scheduling is idempotent;
- how long obsolete full replicas may remain after representation handoff.

### F5 — crash after deletion scheduling but before all source replicas are deleted

Again, the paper does not specify recovery behavior. The detailed source only establishes that deletion is **scheduled**.

Possible implementations could rediscover cleanup, retry queued work, leave leaked storage until later garbage collection, or use another mechanism. None should be attributed to 2012 WAS without another source.

### F6 — capacity exhaustion caused by delayed cleanup

The paper discusses scheduling and system-maintenance resource competition, but the inspected source does not quantify a space-reclamation lag between representation handoff and physical deletion.

Therefore this note does not claim a measured or guaranteed conversion-overlap headroom requirement.

---

## Why this is a retention boundary rather than merely a deletion wording note

The same payload can be present in two redundancy regimes during conversion:

```text
old regime:
    three complete replicas

new regime:
    distributed LRC data/local/global-parity fragments
```

The system must decide when the old regime stops being constitutive to safe retention. The paper's failure path and completion metadata show that this decision depends on more than the existence of new bytes.

The relation can be expressed as:

```text
replacement embodiment production
    + integrity/reconstruction qualification
    + representation-currentness publication
    -> old source representation may become unnecessary
```

What happens afterward is a different class of operation:

```text
unnecessary / retired-from-currentness
    -> cleanup scheduling
    -> physical deletion
    -> allocation reuse
```

The 2012 paper directly shows the left side and the first cleanup handoff. It does not fully describe the right side.

---

## Functional comparisons — not genealogy

### Case 25 — OpenStack Swift EC handoff retirement

Case 25 supplies a later, source-code-level example where a local handoff fragment is purged only after destination-specific synchronization evidence is combined across the required targets.

Functional similarity:

```text
replacement/current placement established
    -> source embodiment becomes purge-eligible
```

Difference:

- Swift's bounded slice is handoff reversion within an erasure-coded object regime;
- WAS Case 24 transitions an immutable extent from **full replication to LRC**;
- Swift's modern source exposes per-object synchronization/purge logic much more directly than the 2012 WAS paper exposes deletion execution.

No WAS→Swift or Swift→WAS lineage is claimed.

### Case 04 — mapped Flash relocation

Mapped Flash supplies a lower-layer functional analogy:

```text
new embodiment written/qualified
    + mapping/currentness publication
    -> old embodiment may later be retired/reclaimed
```

The mechanisms are not historically or physically equivalent. Flash uses device/media mapping and erase geometry; WAS uses distributed redundancy conversion and stream-layer metadata.

The analogy is useful only for preserving the predicate split:

```text
superseded
    != physically erased
```

### Case 19 — Facebook f4 contrast

Case 19 mostly studies repair and placement inside an already erasure-coded regime. Case 24 adds a different obligation:

```text
replicated regime
    -> coded regime
```

The transition itself has persisted progress, validation, completion metadata, and source-retirement work.

This is a contrast, not a genealogy.

---

## Philosophical interpretation — deliberately minimal

The case supports one restrained interpretation:

> **An old technical embodiment can cease to be authoritative/necessary before it ceases to exist physically.**

That is enough for the repository's retention question. It does not require the stronger claim that logical currentness and physical existence are philosophically independent in every technical system.

A second restrained point is that “completion” is typed by the question being asked:

```text
coding complete
    != metadata handoff complete
    != cleanup scheduled
    != cleanup executed
    != capacity reclaimed
```

Treating all of these as one event would erase exactly the engineering relations this repository is trying to recover.

---

## Explicit non-claims

This deepening does **not** claim that:

1. Microsoft invented erasure coding, LRC-like locality, background conversion, or garbage collection;
2. the 2012 paper specifies the complete production deletion-worker implementation;
3. `scheduled for deletion` means deletion is synchronous;
4. `scheduled for deletion` means all three replicas are already physically absent;
5. deletion scheduling is atomically committed with the SM metadata update;
6. completion flags alone prove the lower-level persistence of every fragment or metadata sector;
7. the paper specifies host flush/FUA semantics for fragment persistence;
8. a delete operation immediately returns underlying sectors/blocks to an allocator;
9. allocator reclamation immediately overwrites the previous bytes;
10. deleting the WAS replica is secure erasure or sanitization;
11. TRIM/UNMAP/discard is involved;
12. all source replicas are deleted in one operation or at one moment;
13. no stale source bytes can survive after the coded representation becomes current;
14. a crash after metadata publication but before cleanup cannot leak space;
15. a crash in that interval necessarily loses data;
16. a background cleanup worker reconstructs retirement intent in any particular way;
17. the old replicas are read-inadmissible immediately at exactly the same instant they become deletion-eligible;
18. the paper supplies a formal transaction/linearization point for the representation handoff;
19. the Swift or Flash analogies demonstrate shared implementation ancestry;
20. this narrow deepening warrants promotion beyond `grounded`.

---

## Evidence debt after this slice

The highest-value next evidence would not be another generic LRC explanation. It would target the right-hand side of the transition that the 2012 paper leaves abstract.

### P1 — post-publication / pre-deletion crash behavior

Find a primary implementation, patent, production talk, source disclosure, or later Microsoft engineering paper that states what happens if the extent metadata already names the coded representation but one or more old full replicas remain.

Questions:

- Is deletion intent re-derived from metadata?
- Is there a durable cleanup queue?
- Can repeated cleanup be safely replayed?
- Does the system tolerate long-lived obsolete replicas?

### P2 — deletion/reclamation completion signal

Look for evidence distinguishing:

```text
delete requested
    -> namespace/object retirement
    -> storage allocation reclaimed
    -> lower-layer media effect
```

Do not infer these stages from the 2012 architecture paper.

### P3 — stale/incomplete completion metadata

The current evidence shows completion flags exist, but not every failure mode of those flags. A later source that treats incomplete/stale/corrupt conversion metadata would directly advance the ROADMAP failure-mode item about asynchronous redundancy-mode conversion.

### P4 — coexistence/headroom telemetry

A production trace that measures how long source replicas coexist with coded fragments, or how cleanup delay affects capacity headroom, would connect representation handoff to finite repair/maintenance resources without inventing quantitative bounds.

---

## Status

**Case 24 remains `grounded`.**

This slice closes only the bounded claim:

> In the 2012 WAS implementation description, source-replica retirement is gated by successful coded-state validation and representation-completion metadata before the Stream Manager schedules the old full replicas for deletion; that scheduling event is not evidence that physical deletion, storage reclamation, or sanitization has already completed.

The broader ROADMAP concern remains open for failed/asynchronous conversion after publication, stale/incomplete completion metadata, deletion execution/retry, and empirical fault validation.
