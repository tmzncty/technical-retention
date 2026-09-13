# Evidence 19B — Facebook f4 fragment placement and failure-domain repair margin

## Purpose

This evidence note deepens Case 19 at one narrow boundary: the difference between algebraic Reed–Solomon erasure budget and the physical failure-domain geometry that determines how many coded fragments a correlated failure can remove at once. It also records a particularly useful negative-control fact from the primary f4 paper: normal recovery preserves its placement invariant, but reconstruction can, in rare circumstances, leave a post-reconstruction placement violation that the system then attempts to correct.

The note therefore distinguishes four layers throughout:

- **H — historical record:** what the 2014 f4 paper explicitly documents;
- **E — engineering reconstruction:** consequences that follow from the documented code and placement geometry;
- **F — functional comparison:** bounded comparison with other coded-storage cases in this repository;
- **P — philosophical interpretation:** none is required for the technical claims below.

## Primary source

**Muralidhar et al., “f4: Facebook’s Warm BLOB Storage System,” 11th USENIX Symposium on Operating Systems Design and Implementation (OSDI 14), 2014.**

- USENIX session page: https://www.usenix.org/conference/osdi14/technical-sessions/presentation/muralidhar
- Paper PDF: https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-muralidhar.pdf
- Accessed: 2026-09-13.

The paper is treated as a primary engineering publication for the deployed f4 design described by its authors. It is not treated as a universal statement about all erasure-coded stores, nor as proof that f4 invented any of the underlying coding or placement techniques.

## H — Historical record

### H1. The code-level budget is 10 data plus 4 parity blocks

The paper describes f4 as encoding ten data blocks into four additional parity blocks, yielding fourteen blocks per stripe. The original ten data blocks can be reconstructed from any ten of those fourteen blocks. At this level of description, the stripe therefore has an algebraic erasure budget of four unavailable blocks.

This is a statement about the code geometry used by f4. It does **not** yet say how many machine, rack, or larger correlated failures the stripe tolerates, because one correlated failure can remove more than one coded block if placement allows that concentration.

### H2. Normal placement deliberately spreads a stripe across racks

For the placement described in §4, the fourteen blocks of a stripe are assigned to fourteen different racks. The paper separately describes Rebuilder failure domains and states that Data and Parity stripe failure domains are kept disjoint in the described placement scheme.

This makes physical placement part of the fault-tolerance design rather than an incidental implementation detail.

### H3. f4 constrains per-domain fragment concentration

The paper gives `MaxRebuildFailures` values of two for Data and one for Parity in the described deployment and states the corresponding placement requirement: no more than the configured `MaxRebuildFailures` blocks for a given stripe may be placed in a single Rebuilder failure domain.

The important historical point is that the implementation reasons explicitly about **how many same-stripe blocks a correlated domain may contain**. The Reed–Solomon `(10,4)` parameters alone are not used as a substitute for that placement constraint.

### H4. Ordinary recovery and reconstruction are not documented as equivalent with respect to placement

The paper states that normal Block- and Rebuilder-based failure recovery maintains the placement invariant. Reconstruction uses heuristics that first try to maintain it as well, but the authors explicitly acknowledge that, under rare circumstances, reconstruction can leave a situation that violates the requirement.

The system then attempts to repair the geometry: after reconstruction it tries to move blocks to correct violations; the paper also discusses splitting a failure domain when needed and checking that no unrecoverable filesets remain before retiring a drive.

This is unusually valuable evidence because it is not merely a hypothetical warning added by later analysis. The primary source itself distinguishes:

1. intended placement policy;
2. ordinary recovery that maintains it;
3. a reconstruction path that can rarely leave a violation; and
4. subsequent corrective work intended to restore an acceptable geometry.

## E — Engineering reconstruction

### E1. Erasure-count budget is not failure-domain-count budget

Let one correlated failure domain contain `m` coded blocks from the same f4 stripe. If that whole domain becomes unavailable at once, the code experiences `m` simultaneous block erasures from that one physical event.

For the documented RS(10,4)-style stripe, the source says that any ten of fourteen blocks suffice. Holding that model fixed, a correlated event that makes more than four same-stripe blocks unavailable exceeds the stated algebraic recovery budget. Thus:

`4-block erasure budget != 4 arbitrary failure domains tolerated`

unless placement separately constrains how many same-stripe blocks each such domain can remove.

### E2. Restoring block count can precede restoring future correlated-failure margin

A reconstruction can produce enough valid blocks for a stripe to be readable again while placing those blocks in a geometry that violates the intended failure-domain concentration rule. The f4 paper's documented rare post-reconstruction violation makes this more than a purely invented counterexample.

Accordingly:

`current readability restored != future correlated-failure margin restored`

and:

`coded-fragment count restored != failure-domain topology restored`.

The second property requires a placement condition in addition to a content/currentness condition.

### E3. Placement policy is operational state, not merely a static design diagram

Because reconstruction can temporarily leave a violation and later corrective movement is needed, “the placement policy says fourteen racks” is not proof that every live stripe continuously satisfies the intended topology at every intermediate moment.

A claim that repair margin has been restored therefore needs evidence about at least two independent dimensions:

- **content/currentness:** the reconstructed fragments are valid for the authoritative stripe state; and
- **geometry:** their current locations again satisfy the relevant failure-domain concentration rules.

This does not imply that f4 exposed one universal scalar “repair margin” metric. It is an engineering decomposition of what the source-backed placement behavior means for retention analysis.

### E4. The negative control is bounded

The paper's wording that such reconstruction violations are rare does not provide a rate, probability, MTBF, duration distribution, or production incident count. Nothing in this evidence note converts “rare” into a quantitative reliability estimate.

Likewise, the source documents a possible placement violation, not necessarily a documented user-visible data-loss incident caused by that violation.

## F — Functional comparison

Case 24 (Windows Azure Storage LRC) independently separates coding geometry from rack-placement geometry: its locality-oriented code structure does not by itself guarantee independence from correlated rack faults, so fragments are placed across racks as a separate operational concern.

That is a **functional comparison only**. It does not establish shared implementation, direct influence, common genealogy, or identical failure-domain semantics between Azure LRC and Facebook f4.

The cross-case lesson is narrower:

`code geometry + placement geometry + currentness evidence -> usable repair-margin claim`

Removing any one of those terms can leave a coded object readable now while overstating its resilience to the next fault.

## Explicit non-claims

This evidence does **not** establish that:

- every f4 stripe always occupied fourteen distinct Rebuilder failure domains;
- every correlated failure aligns perfectly with a declared Rebuilder domain;
- every post-reconstruction placement violation caused data loss or an outage;
- “rare” has a source-supported numerical frequency;
- moving a fragment automatically proves that its content is current and durable before validation;
- f4 invented Reed–Solomon coding, failure-domain placement, or reconstruction;
- the f4 placement mechanism and Azure LRC share algorithmic or historical genealogy.

## Retention consequence

Case 19 can now use a primary-source negative control instead of a merely hypothetical one. The important retention boundary is:

`algebraically sufficient fragments != safely distributed fragments`

and, after a repair:

`readability recovered != full future-failure margin recovered`.

The f4 source documents both the intended placement invariant and the possibility of a rare reconstruction-time violation, making it a strong witness that coded-storage repair state includes not just **which fragments exist**, but **where correlated faults can remove them together**.

## Follow-on production witness and status

The adjacent deepening [`19-facebook-f4-production-correlated-failure-and-rebuild-deepening.md`](19-facebook-f4-production-correlated-failure-and-rebuild-deepening.md) now supplies the production/operational witness that this note deliberately did not claim: the same OSDI paper reports a bad-disk cohort plus elevated temperature driving AFR above 60% for weeks within one cell, with no reported data loss because buddy/XOR material lived in unaffected cells, and separately reports a 240-TB two-host rebuild drill taking three days while p99 latency rose to 500 ms.

That follow-on closes the **bounded production correlated-failure / rebuild-window witness** debt for Case 19. It does not convert the placement violation above into a documented data-loss incident, and it leaves direct per-fragment currentness evidence during incomplete reconstruction open.
