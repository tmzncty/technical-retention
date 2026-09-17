# Case 43 Deepening — AVATAR RRT Embodiment, Same-Substrate Vulnerability, and Runtime-Only Policy State

## Status

**`bounded deepening complete`**

This evidence note deepens [`../cases/43-avatar-vrt-aware-dram-refresh-feedback.md`](../cases/43-avatar-vrt-aware-dram-refresh-feedback.md) without changing its maturity.

The narrow question is:

> If a DRAM refresh policy depends on a row-classification table, what protects the table that says how the DRAM itself should be refreshed?

The 2015 AVATAR paper gives an unusually useful answer in a short implementation footnote. Its generic multirate-refresh design uses a `Row Refresh Table` (`RRT`) with one bit per row. The authors assume that the RRT information is available at the memory controller, but also note that SRAM overhead can be avoided by storing the RRT in a reserved DRAM region. They then explicitly propose triplicating the DRAM-resident RRT to tolerate VRT-related errors in the RRT itself.

That small design detail adds a distinct retention boundary that the existing Case 43 grounding did not yet isolate:

```text
payload-retention policy metadata
    can itself be placed on the substrate whose retention it governs

therefore

policy semantic currentness
    != policy-bit integrity
    != policy-state persistence across power loss
```

The case remains bounded to the research architecture in Qureshi et al. It does **not** establish that a commercial memory controller implemented this RRT organization, that AVATAR's RRT survived machine power loss, or that the paper specifies a complete voting/recovery protocol for the three copies.

---

## 1. Primary source custody

### 1.1 AVATAR paper

Primary source:

- Moinuddin K. Qureshi, Dae-Hyun Kim, Samira Manabi Khan, Prashant J. Nair, and Onur Mutlu, **“AVATAR: A Variable-Retention-Time (VRT) Aware Refresh for DRAM Systems,”** 45th Annual IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 2015, pp. 427–437, DOI `10.1109/DSN.2015.58`.

Institutional/author mirrors inspected:

- <https://www.istc-cc.cmu.edu/publications/papers/2015/avatar-dram-refresh_dsn15.pdf>
- <https://memlab.ece.gatech.edu/papers/DSN_2015_1.pdf>

The page-resolved text and a rendered institutional-mirror page were inspected during this research slice. No claim below depends only on a diagram label that was unavailable in text extraction.

### 1.2 RAIDR prior-art cross-check

AVATAR itself cites RAIDR when discussing memory-controller storage for retention classifications and contrasts its own one-bit-per-row RRT with RAIDR's Bloom-filter representation.

Institutional record inspected:

- Jamie Liu, Ben Jaiyen, Richard Veras, Onur Mutlu, **“RAIDR: Retention-Aware Intelligent DRAM Refresh,”** ISCA 2012.
- Carnegie Mellon KiltHub record: <https://kilthub.cmu.edu/articles/journal_contribution/RAIDR_Retention-Aware_Intelligent_DRAM_Refresh/6469205>
- CMU Parallel Data Laboratory abstract: <https://pdl.cmu.edu/PDL-FTP/NVM/raidr-isca12_abs.shtml>

Those records state that RAIDR stores retention-time bins in Bloom filters, requires only minimal memory-controller modification, and reports 1.25 KB controller storage in its evaluated 32 GB system.

This note uses RAIDR only as the prior-art contrast AVATAR itself invokes. It does not recreate the broader history of DRAM refresh optimization.

---

## 2. Historical / implementation record

### 2.1 The RRT is an explicit row-policy representation

In the paper's multirate-refresh background, retention testing identifies rows that need `Fast Refresh` and populates an RRT. At runtime the RRT determines the refresh rate for each row.

For the paper's example of an 8 GB DIMM with an 8 KB row buffer, the RRT is **128 KB**.

The same section describes a two-class representation:

```text
0 -> SlowRefresh
1 -> FastRefresh
```

The authors state that their target configuration places roughly 10% or more of rows in the fast-refresh class. Because the tracked set is no longer tiny, they use an RRT with **one bit per row** rather than the compact Bloom-filter organization used by RAIDR for a much smaller weak-row population.

This is important for evidence discipline. The RRT is not an abstract metaphor for “memory of memory.” It is a concrete policy representation whose storage cost is derived from row count and classification width.

### 2.2 The paper assumes RRT information is available at the memory controller

The paper says that for its studies, RRT information is assumed to be available at the memory controller, similar to RAIDR.

That sentence alone does not determine the physical medium. The footnote immediately gives at least two implementation choices:

1. pay SRAM overhead for controller-resident table storage; or
2. avoid that SRAM overhead by placing the RRT in a reserved area of DRAM.

Therefore:

```text
memory-controller-visible policy state
    != necessarily on-controller SRAM state
```

The logical authority of the controller over the classification and the physical embodiment of the classification are separate questions.

### 2.3 A DRAM-resident RRT is explicitly contemplated

The paper states that the SRAM overhead can be avoided by storing the RRT in a reserved DRAM region. For the 8 GB example, 128 KB is reported as about **0.0015%** of memory space.

This creates a same-substrate relation:

```text
DRAM payload rows
    governed by refresh-policy metadata

refresh-policy metadata
    may itself reside in DRAM
```

The paper does not frame this as a philosophical recursion. It is an engineering storage-overhead option.

But for this repository it is a valuable retention boundary: the metadata that determines future restoration cadence can inhabit a substrate exposed to the same broad class of retention faults that motivated the policy.

### 2.4 The paper proposes prefetching RRT lines

For the DRAM-resident option, the paper says that while refresh decisions for the current RRT line — covering **512 rows** — are used, the next RRT line can be prefetched from DRAM to hide lookup latency.

This establishes another useful separation:

```text
policy authority
    != instantaneous local availability of all policy bits
```

The complete table can be resident in DRAM while a working portion is brought near the controller as needed.

The source does not define this as a cache hierarchy with a specified replacement/coherence protocol, so this note does not introduce one.

### 2.5 The paper explicitly protects the DRAM-resident RRT against VRT-related errors

The most important statement for this slice is that the RRT in DRAM can be **replicated three times** to tolerate VRT-related errors in the RRT, with total reported storage overhead of about **0.005%**.

This is direct historical/engineering-source evidence that the authors recognized the refresh-policy metadata itself as vulnerable when embodied in DRAM.

The resulting relation is not merely inferred from first principles:

```text
VRT can threaten data
    -> RRT controls refresh policy for data
    -> if RRT is kept in DRAM, VRT can also threaten RRT bits
    -> replicate RRT to tolerate that metadata error mode
```

The paper does **not** provide, in this short footnote, a complete description of how three copies are compared, voted, repaired, or scrubbed. The supported claim is therefore the narrower one: triplication is proposed for tolerating VRT-related RRT errors.

---

## 3. Engineering reconstruction: two different ways the policy can become wrong

Case 43 already establishes that VRT can make a perfectly preserved old row classification semantically stale. This slice adds a different failure mode: the bits encoding the classification can themselves be corrupted.

These should not be collapsed.

### 3.1 Semantic-currentness failure

A row is correctly recorded as `SlowRefresh`, but later VRT changes the cell behavior.

```text
RRT bit intact
    + substrate behavior changed
    -> policy relation no longer conservative
```

AVATAR addresses that problem through ECC observation, scrubbing, row upgrade, and later retesting.

### 3.2 Representation-integrity failure

The substrate behavior may not have changed in a way that invalidates the intended classification, but the RRT bit itself is damaged.

```text
intended policy remains valid
    + policy representation is corrupted
    -> controller may apply the wrong maintenance class
```

For the DRAM-resident option, the paper proposes three copies to tolerate VRT-related RRT errors.

Therefore:

```text
policy-bit integrity
    != policy semantic currentness
```

and:

```text
protecting the metadata bits
    != revalidating what those bits mean
```

Triplication can address representation corruption without proving that an old classification still matches present retention behavior. Conversely, yearly re-testing can revise semantic classification without by itself explaining how a corrupted RRT copy is detected or repaired.

This distinction is important because “metadata protection” is otherwise easy to overstate as “the policy is safe.”

---

## 4. Same-substrate metadata does not create an infinite regress claim

It is tempting to turn the DRAM-resident RRT into an abstract recursion:

```text
what protects the table that says how to protect memory?
what protects the protection for that table?
...
```

That is not what the historical source says.

The source gives a finite engineering move: replicate the RRT three times to tolerate VRT-related errors, at small storage cost.

A bounded reconstruction is:

> A maintenance policy may need an explicit protection mechanism for its own representation when that representation is placed inside the same broad failure domain as the data it governs.

A stronger statement such as “all protection metadata requires endlessly recursive protection metadata” is rejected.

Practical systems terminate such chains through assumptions, stronger mechanisms, spatial redundancy, different media, conservative defaults, or some combination. AVATAR's paper only supplies the triplication proposal here; it does not specify a general theory of recursion termination.

---

## 5. Runtime retention is not power-loss persistence

The repository uses “retention” across many horizons, so this boundary must be explicit.

The AVATAR paper discusses keeping and revising RRT classifications during system operation. Its implementation alternatives are SRAM or ordinary reserved DRAM.

Neither medium, by itself, establishes nonvolatile survival across loss of power.

The paper does not specify:

- an NVRAM copy of the RRT;
- firmware persistence of the RRT across reboot;
- a disk/SSD checkpoint for refresh classifications;
- a boot-time restore protocol;
- a crash-consistent RRT update format;
- whether a restarted system re-runs full retention testing before using slow refresh.

Therefore the safe statement is:

```text
RRT survives and evolves during powered runtime
    !=
RRT is proven to survive machine power loss
```

and:

```text
runtime policy state
    != restart-persistent configuration
```

The fact that AVATAR begins with retention testing provides a way to *create* the table, but the paper does not give enough evidence to turn that into a documented restart-reconstruction contract.

This matters especially for the project vocabulary “retained control state.” Here, “retained” means state preserved long enough to govern subsequent runtime maintenance decisions unless a narrower persistence horizon is explicitly proven. It must not silently be read as “nonvolatile.”

---

## 6. Authority, embodiment, and access path are separate dimensions

The RRT detail supports a useful three-way decomposition.

### 6.1 Authority

The classification bit answers a policy question:

```text
which refresh class should this row receive?
```

### 6.2 Embodiment

That bit can be represented in:

- controller SRAM; or
- reserved DRAM, according to the paper's implementation discussion.

### 6.3 Access path

For the DRAM-resident option, RRT lines can be prefetched so that the next group of decisions is locally available when needed.

Thus:

```text
who interprets the policy
    != where the policy bits physically live
    != how the current policy bits arrive in time for use
```

This is an engineering reconstruction from the paper's implementation choices, not terminology attributed to Qureshi et al.

---

## 7. The same physical substrate can carry payload and policy with different logical roles

If the RRT is placed in reserved DRAM, ordinary payload and RRT bits share the same broad storage technology but not the same logical role.

```text
payload bit
    -> object being preserved

RRT bit
    -> instruction/state governing how aggressively payload rows are restored
```

A physical-medium taxonomy alone therefore loses an important distinction:

```text
same DRAM technology
    != same retention role
```

The policy state is “second-order” only in the repository's analytical vocabulary: it describes maintenance of other state. The paper does not use that philosophical label.

---

## 8. Triplication is not the same as ECC, scrubbing, or refresh

AVATAR uses several reliability mechanisms simultaneously. They must remain distinct.

### Data ECC

Detects/corrects errors on data accesses and supplies a trigger for row upgrade.

### Memory scrub

Proactively reads/checks memory so cold locations do not depend solely on demand accesses for error observation.

### DRAM refresh

Restores cell charge; AVATAR varies its cadence by row class.

### RRT triplication

For the DRAM-resident RRT implementation option, provides redundant copies intended to tolerate VRT-related errors in the policy table itself.

Therefore:

```text
RRT triplication
    != data ECC
    != scrub
    != refresh
    != retention retesting
```

The paper's short footnote does not establish that the three RRT copies are protected by the same ECC path as ordinary payload, or that scrub treats them identically to payload. This note does not assume either.

---

## 9. Prior-art representation boundary: RAIDR Bloom filters vs AVATAR RRT

RAIDR is useful here because AVATAR itself invokes it.

The 2012 RAIDR record describes retention-time bins stored as Bloom filters in the memory controller, with 1.25 KB storage in the evaluated 32 GB system.

AVATAR's 2015 paper notes that Bloom filters are attractive when the weak-row population is very small, giving RAIDR's example of tracking roughly 1000 weak rows among one million rows. It then argues that Bloom filters become ineffective at reducing storage once weak rows become a few percent of the total. For AVATAR's target configuration, 10% or more rows can be in the fast-refresh class, so the paper uses a direct one-bit-per-row RRT.

The bounded historical relation is therefore:

```text
RAIDR:
    sparse weak-row representation
    -> Bloom-filter bins

AVATAR implementation discussion:
    materially denser fast-row population
    -> one bit per row RRT
    -> optional reserved-DRAM embodiment
```

This is not evidence that Bloom filters are generally unsafe or that direct tables are universally preferable. It is a density/storage-overhead tradeoff in these research designs.

Nor does this note claim that AVATAR's triplicated DRAM RRT is a direct implementation descendant of RAIDR's controller Bloom filters. The source relationship is one of cited prior art and design contrast.

---

## 10. Failure-boundary matrix

| Failure / change | Payload bits intact? | RRT bits intact? | RRT meaning current? | Mechanism discussed by AVATAR |
| --- | --- | --- | --- | --- |
| ordinary cell leakage under correct cadence | intended yes | intended yes | yes | refresh |
| payload VRT error on an accessed word | no before correction | may be yes | old row class may now be too weak | ECC correction + row upgrade |
| VRT vulnerability in cold memory | at risk | may be yes | old row class may now be too weak | proactive scrub + upgrade |
| accumulated conservative upgrades | payload may be fine | yes | policy is safe but may be over-conservative | infrequent retention retesting / downgrade |
| VRT-related error in DRAM-resident RRT | payload may be fine | no / one copy may be wrong | intended policy may still be current | proposed RRT triplication |
| machine power loss | DRAM contents not proven persistent | SRAM/DRAM RRT not proven persistent | not enough evidence | no restart-persistence contract in paper |

The table is a repository reconstruction. It maps source-supported mechanisms onto distinct failure dimensions and must not be read as a verbatim table from the paper.

---

## 11. Cross-case comparison

### 11.1 Case 40 — profile validity vs profile survival

Case 40 establishes that static DRAM retention profiling is threatened by DPD/VRT:

```text
profile survives
    != profile remains conservative
```

This Case 43 deepening adds:

```text
profile/classification remains semantically justified
    != representation bits remain intact
```

Together:

```text
policy safety
    requires attention to both

    semantic currentness
        and
    representation integrity
```

The mechanisms are different and must not be collapsed into one “metadata reliability” bucket.

### 11.2 Relation to restart-progress cases

A bounded functional comparison can be made with Kafka Case 42 or SQLite Case 152: all involve control/maintenance state whose usefulness depends on more than mere byte survival.

But the failure modes differ:

- Kafka: a persisted progress coordinate can become stale relative to changed log geometry;
- SQLite: checkpoint progress can be deliberately forgotten and rebuilt from stronger WAL evidence;
- AVATAR: a runtime row-policy bit can become semantically stale as VRT changes, or physically corrupt if stored in DRAM.

No historical or technical genealogy is asserted across these systems.

---

## 12. Historical record / reconstruction / analogy / philosophy separation

### Historical / source-grounded record

Supported directly by the 2015 paper:

- multirate refresh uses an RRT to choose per-row refresh class;
- the example RRT is 128 KB for an 8 GB DIMM with an 8 KB row buffer;
- the evaluated design uses one bit per row;
- the paper assumes RRT information is available at the memory controller;
- SRAM overhead can be avoided by placing the RRT in reserved DRAM;
- the next RRT line can be prefetched while the current line is used;
- the DRAM-resident RRT can be replicated three times to tolerate VRT-related RRT errors;
- runtime ECC/scrub feedback can upgrade rows and later retention testing can downgrade them.

### Engineering reconstruction

Repository-level deductions, not paper vocabulary:

- policy-bit integrity is distinct from policy semantic currentness;
- controller authority is distinct from metadata embodiment;
- same-substrate policy metadata creates a second-order protection obligation;
- runtime-retained policy state is not automatically restart-persistent state;
- same medium can carry first-order payload and second-order policy roles.

### Functional analogy

A bounded analogy is to any system that stores maintenance metadata inside the same failure domain as the object being maintained and therefore adds redundancy for the metadata.

The analogy is structural only.

### Philosophical interpretation

A narrow conceptual pressure is:

> A system can preserve an object by retaining instructions about how to preserve it, yet those instructions themselves remain technical objects with their own integrity and validity conditions.

And:

> “Remembering how to remember” does not remove material dependence; it relocates part of the dependence into another representation that may itself need protection or revalidation.

These are repository interpretations. They are not claims about the authors' philosophical intent.

---

## 13. Explicit non-claims

This evidence note does **not** claim that:

1. AVATAR was commercially deployed.
2. A commercial DRAM controller used the paper's exact 128 KB RRT.
3. The RRT was necessarily stored in DRAM rather than SRAM.
4. The RRT survives loss of machine power.
5. The RRT survives controller reset.
6. The paper specifies a persistent boot-time restore protocol for RRT state.
7. Triplication means the paper specifies a particular majority-voter circuit.
8. Triplication guarantees correction of every possible multi-copy corruption.
9. The three RRT copies fail independently.
10. RRT copies are physically placed in different DRAM banks/ranks/channels.
11. The RRT rows receive a particular refresh cadence not stated by the source.
12. Ordinary data ECC necessarily covers the RRT copies.
13. Ordinary memory scrub necessarily scrubs RRT copies in the same way as payload.
14. Prefetching an RRT line constitutes a fully specified cache protocol.
15. RAIDR's Bloom filters and AVATAR's direct RRT are interchangeable representations at every weak-row density.
16. Bloom filters are inherently less reliable than direct tables.
17. Three copies make semantic staleness from VRT disappear.
18. Yearly retesting repairs physical corruption of an RRT copy.
19. The source establishes crash consistency for concurrent RRT updates.
20. The source proves atomicity of a row-class update with respect to refresh scheduling.
21. The source establishes recovery behavior if a failure occurs while an RRT classification is being changed.
22. Same-substrate metadata implies an infinite regress of protection mechanisms.
23. “Second-order retention infrastructure” is terminology used by Qureshi et al.
24. The research design's modeled reliability numbers are field-observed commercial lifetimes.

---

## 14. Claim ledger

| Claim | Label | Evidence strength |
| --- | --- | --- |
| AVATAR/multirate refresh uses an RRT to select row refresh rate | H/P | direct 2015 paper |
| The paper's 8 GB / 8 KB-row example gives a 128 KB RRT | H/P | direct 2015 paper |
| The AVATAR discussion uses one bit per row because the fast-row population can be around 10% or more | H/P | direct 2015 paper footnote/context |
| RRT information is assumed available at the memory controller | H/P | direct 2015 paper |
| The RRT can be stored in reserved DRAM to avoid SRAM overhead | H/P | direct 2015 paper footnote |
| The next RRT line can be prefetched while current decisions are used | H/P | direct 2015 paper footnote |
| The DRAM-resident RRT can be triplicated to tolerate VRT-related RRT errors | H/P | direct 2015 paper footnote |
| RAIDR uses Bloom filters to represent retention-time bins | H/P | RAIDR institutional record + AVATAR citation |
| Policy-bit integrity and policy semantic currentness are separate failure dimensions | E | reconstruction from source mechanisms |
| Controller-visible policy state and physical embodiment are separate dimensions | E | reconstruction from SRAM/DRAM alternatives |
| Same-substrate policy metadata can require its own protection | E | reconstruction strongly grounded by explicit triplication proposal |
| AVATAR RRT is nonvolatile across power loss | X | not established |
| Triplication fully specifies detection/voting/repair | X | not established |
| DRAM-resident RRT is the mandatory AVATAR implementation | X | contradicted by source's implementation-choice framing |

Legend follows repository convention: `H/P` historical/primary-source record; `E` engineering reconstruction; `X` rejected/unsupported stronger claim.

---

## 15. Remaining evidence debt

This slice closes the narrow **RRT embodiment / same-substrate metadata protection** gap but leaves several useful questions open:

1. **Update atomicity** — the paper does not specify whether changing a row's RRT bit is atomic relative to the refresh scheduler.
2. **Three-copy protocol** — the cited footnote does not fully describe comparison, voting, repair, placement, or correlated-failure handling for the replicated RRT.
3. **Reset / reboot behavior** — there is no documented power-cycle persistence or reconstruction contract for runtime row classifications.
4. **RRT refresh policy** — the source does not clearly state whether reserved RRT rows are always fast-refreshed, specially refreshed, or protected through another exact cadence rule.
5. **Commercial correspondence** — no claim has been established that a production memory controller adopted AVATAR's exact RRT embodiment.
6. **Historical antecedents** — broader history of protected controller metadata and same-substrate maintenance metadata belongs primarily in `computing-archaeology` if pursued.

These are deliberately left as evidence debt rather than filled by architectural guesswork.

---

## 16. Related-repository boundary

A fresh search of `tmzncty/computing-archaeology` for `AVATAR`, `VRT`, `RAIDR`, and DRAM refresh found no dedicated packet to reuse.

Accordingly, `technical-retention` keeps only this bounded seam:

```text
retention-policy authority
    -> physical metadata embodiment
    -> metadata's own integrity exposure
    -> protection of the policy representation
    -> separate semantic revalidation of the policy
```

A wider history of retention-aware DRAM refresh, Bloom-filter controller structures, memory-controller metadata placement, VRT device physics, and commercial adoption should be developed in `computing-archaeology` rather than duplicated here.
