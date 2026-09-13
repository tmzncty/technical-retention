from pathlib import Path

case = Path('cases/19-facebook-f4-erasure-coded-failure-domains.md')
synth = Path('docs/SYNTHESIS_07_CODED_RECOVERABILITY_REPAIR_MARGIN.md')
roadmap = Path('ROADMAP.md')
index = Path('CASE_INDEX.md')
evidence = Path('evidence/19-facebook-f4-fragment-placement-failure-domain-margin-deepening.md')

marker = '## Deepening: reconstruction can restore blocks before it restores failure-domain margin'
assert not evidence.exists(), evidence
assert marker not in case.read_text(encoding='utf-8')
assert 'Finding 3876' not in index.read_text(encoding='utf-8')

evidence.write_text('''# Evidence 19B — Facebook f4 fragment placement and failure-domain repair margin

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
''', encoding='utf-8')

case_text = case.read_text(encoding='utf-8')
anchor = '## What this case does not prove'
assert anchor in case_text
deepening = '''## Deepening: reconstruction can restore blocks before it restores failure-domain margin

The 2014 f4 paper gives a useful negative control for the difference between **code-level recoverability** and **failure-domain repair margin**. Its `(10,4)` Reed–Solomon stripe has fourteen blocks and is recoverable from any ten, while normal placement assigns the fourteen blocks across fourteen different racks. More specifically, the deployment described in the paper configures `MaxRebuildFailures` as two for Data and one for Parity and requires that no more than that many same-stripe blocks occupy one Rebuilder failure domain.

The source then draws a distinction that matters directly for this repository: ordinary Block/Rebuilder failure recovery maintains that placement invariant, whereas reconstruction uses heuristics that can, under rare circumstances, leave a post-reconstruction violation. f4 subsequently tries to move blocks to correct violations, can split a failure domain when necessary, and checks for unrecoverable filesets before retiring a drive.

This supports a stronger bounded claim than the earlier generic placement discussion:

`coded-fragment count restored != failure-domain topology restored`

and therefore:

`current readability restored != future correlated-failure margin restored`.

If one correlated domain contains `m` blocks from the same stripe, one domain outage consumes `m` erased-block positions. Under the paper's “any ten of fourteen” model, more than four simultaneous erased blocks exceed the stated algebraic budget. The code parameters therefore do not by themselves determine how many correlated physical failures are tolerable; placement controls how much of the algebraic budget one physical event can consume.

The claim remains deliberately narrow. The paper does not quantify how often its rare post-reconstruction placement violation occurred, does not thereby document a data-loss incident, and does not show that every live stripe is always in a fourteen-distinct-Rebuilder-domain configuration. It also does not prove reconstructed content current merely because placement has been corrected. A complete restored-margin claim needs both content/currentness evidence and placement/topology evidence.

See `evidence/19-facebook-f4-fragment-placement-failure-domain-margin-deepening.md` for the historical record, engineering reconstruction, explicit non-claims, and the bounded functional comparison with Case 24.

'''
case.write_text(case_text.replace(anchor, deepening + anchor, 1), encoding='utf-8')

synth_text = synth.read_text(encoding='utf-8')
synth_marker = '## Case 19 negative control: fragment-count recovery is not geometry recovery'
assert synth_marker not in synth_text
synth.write_text(synth_text.rstrip() + '''\n\n## Case 19 negative control: fragment-count recovery is not geometry recovery

Facebook f4 supplies a primary-source negative control for one of the synthesis's central distinctions. The OSDI 2014 paper documents a `(10,4)` code in which any ten of fourteen blocks recover the stripe, but it separately constrains how many same-stripe blocks may share one Rebuilder failure domain. It further states that ordinary recovery preserves the placement invariant while reconstruction can, rarely, leave a violation that later block movement or domain splitting attempts to correct.

That means restored **symbol count** and restored **fault geometry** are observably separable operational states:

`enough current fragments to decode`  
`!=`  
`fragments distributed so that the intended next-fault margin has been restored`.

For retention analysis, the repair-margin state of a coded object therefore has at least three independent coordinates: code budget, fragment currentness, and correlated-failure placement geometry. A system can be readable on the first two while still carrying placement debt on the third. Case 24 provides a functional comparison from Azure LRC, where code locality and cross-rack placement are likewise distinct, but this comparison is not a genealogy claim.

See `evidence/19-facebook-f4-fragment-placement-failure-domain-margin-deepening.md`.
''', encoding='utf-8')

roadmap_text = roadmap.read_text(encoding='utf-8')
needle = 'coded-fragment loss concentrated in one failure domain, incomplete rebuild, or placement violation that silently reduces future repair margin.'
assert needle in roadmap_text
replacement = (needle + ' **Case 19 placement-violation slice closed (2026-09-13):** the OSDI 2014 f4 primary source now grounds normal 14-rack spreading, per-Rebuilder-domain `MaxRebuildFailures` concentration limits, and the possibility of a rare reconstruction-time placement violation followed by corrective movement/domain splitting. Remaining debt is the incomplete-rebuild/currentness side and a separately evidenced production incident or telemetry trace; do not infer either from the placement result alone.')
roadmap.write_text(roadmap_text.replace(needle, replacement, 1), encoding='utf-8')

index_text = index.read_text(encoding='utf-8')
additions = '''\n\n## Findings 3876–3891 — Case 19 f4 failure-domain placement margin deepening

- **Finding 3876 (H)** — Muralidhar et al., OSDI 2014, is the primary engineering publication used here for Facebook f4's warm-BLOB storage design; this evidence slice treats it as a source for the deployed design described by the authors, not as a universal erasure-coding history.
- **Finding 3877 (H)** — f4's documented stripe uses ten data blocks plus four parity blocks; any ten of the fourteen recover the original ten data blocks under the paper's code model.
- **Finding 3878 (H)** — The normal placement described by f4 assigns a stripe's fourteen blocks to fourteen different racks, making physical spreading a separate part of the fault-tolerance design.
- **Finding 3879 (H)** — The paper keeps Data- and Parity-stripe failure domains disjoint in the described placement scheme; this is a placement property, not a consequence of Reed–Solomon algebra alone.
- **Finding 3880 (H)** — The described deployment configures `MaxRebuildFailures` as two for Data and one for Parity and requires that no more than the configured number of same-stripe blocks occupy one Rebuilder failure domain.
- **Finding 3881 (H)** — The f4 paper says regular Block- and Rebuilder-based failure recovery maintains the placement invariant.
- **Finding 3882 (H)** — The same source says reconstruction heuristics can, in rare circumstances, leave a post-reconstruction placement violation; f4 then attempts corrective block movement, may split a failure domain, and verifies recoverability before retiring a drive.
- **Finding 3883 (E)** — An erasure-count budget is not automatically a failure-domain-count budget: the latter depends on how many same-stripe fragments one correlated physical event can remove.
- **Finding 3884 (E)** — If one correlated domain contains `m` fragments from a stripe, losing that domain consumes `m` erasure positions at once; placement therefore determines how quickly a physical fault consumes algebraic redundancy.
- **Finding 3885 (E)** — Holding f4's documented “any ten of fourteen” model fixed, more than four simultaneous unavailable blocks exceed the stated algebraic recovery budget; this does not imply that exactly four arbitrary correlated domains are tolerable.
- **Finding 3886 (E)** — Reconstructing enough valid fragments for current readability does not by itself prove that the intended future correlated-failure margin has been restored.
- **Finding 3887 (E)** — `coded-fragment count restored != failure-domain topology restored`; the f4 reconstruction path provides a source-backed negative control rather than a purely hypothetical one.
- **Finding 3888 (E)** — A documented placement policy is not proof of continuous live compliance at every intermediate moment; f4's rare post-reconstruction violation explicitly demonstrates that operational placement state can diverge from intended geometry.
- **Finding 3889 (E)** — A restored-margin claim for coded storage needs evidence for both fragment content/currentness and current failure-domain geometry; validating only one dimension can overstate resilience to the next correlated fault.
- **Finding 3890 (F)** — Case 24 Azure LRC provides a bounded functional comparison in which code geometry and rack-placement geometry are also distinct; this does not establish shared algorithm, implementation, or genealogy with f4.
- **Finding 3891 (boundary/synthesis)** — The f4 paper documents the possibility of a rare placement violation, not a source-quantified frequency or necessarily a documented data-loss incident. Its safe synthesis is that usable coded-repair margin jointly depends on code budget, fragment currentness, and correlated-failure placement geometry.
'''
index.write_text(index_text.rstrip() + additions + '\n', encoding='utf-8')
