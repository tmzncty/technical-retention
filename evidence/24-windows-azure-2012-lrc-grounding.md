# Case 24 grounding — Windows Azure Storage LRC repair locality and redundancy-mode handoff (2012)

## Purpose

This record grounds [`cases/24-windows-azure-lrc-repair-locality-handoff.md`](../cases/24-windows-azure-lrc-repair-locality-handoff.md).

The evidence target is deliberately narrow. It is **not** “prove that LRC is good,” “write the history of Azure Storage,” or “establish invention priority for locally repairable erasure codes.” It asks whether period-primary material supports five retention distinctions:

1. mathematical recoverability versus the distributed read/I/O cost of exercising it;
2. code-local dependency versus physical / administrative placement;
3. on-demand reconstruction for service versus durable fragment repair;
4. mere existence of newly encoded fragments versus a completed, validated handoff from full replication to coded retention;
5. payload fragments versus the progress, completion, integrity, and topology state needed to sustain the coded representation.

**Result:** all five are directly supported by the 2012 WAS paper strongly enough for `grounded` status.

---

## Source set

### P1 — Huang et al., USENIX ATC 2012

Cheng Huang, Huseyin Simitci, Yikang Xu, Aaron Ogus, Brad Calder, Parikshit Gopalan, Jin Li, and Sergey Yekhanin, **“Erasure Coding in Windows Azure Storage,”** *2012 USENIX Annual Technical Conference*, June 2012, pp. 15–26.

- Microsoft Research record: <https://www.microsoft.com/en-us/research/publication/erasure-coding-windows-azure-storage/>
- Microsoft-hosted PDF: <https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/LRC12-cheng-webpage.pdf>

The Microsoft Research record identifies the eight authors, `USENIX ATC 2012`, June 2012, and USENIX as publisher. The PDF is the central primary source for both the LRC code definition and the production WAS implementation.

### P2 — Huang, Chen, Li, Pyramid Codes, 2007

Cheng Huang, Minghua Chen, Jin Li, **“Pyramid Codes: Flexible Schemes to Trade Space for Access Efficiency in Reliable Data Storage Systems,”** Microsoft Research Technical Report **MSR-TR-2007-25**, March 2007.

- Microsoft Research record: <https://www.microsoft.com/en-us/research/publication/pyramid-codes-flexible-schemes-to-trade-space-for-access-efficiency-in-reliable-data-storage-systems/>

Used only as near prior art for the **space / access-efficiency trade-off** and as a boundary against a novelty story in which the 2012 paper created the general idea of sacrificing code structure/space to reduce recovery access work.

### Reused repository source boundary

[`Case 19`](../cases/19-facebook-f4-erasure-coded-failure-domains.md) and [`evidence/19-facebook-f4-2014-erasure-coding-grounding.md`](19-facebook-f4-2014-erasure-coding-grounding.md) already anchor Reed and Solomon’s 1960 paper. Case 24 reuses that boundary rather than reproducing another coding-history section.

---

## Direct-inspection ledger

### P1 PDF p. 1 — replication → sealing → background erasure coding

Direct text inspection establishes:

- WAS stream-layer data is appended to active extents;
- active data starts with three full copies;
- extents become sealed/immutable at a size threshold;
- sealed extents are erasure-coded lazily in the background;
- the original full copies are deleted after the extent is erasure-coded;
- the motivating performance cost is reconstruction when a fragment is unavailable/offline or a node is hot;
- ordinary `RS (12,4)` at `1.33x` would require reading twelve fragments in the compared reconstruction path.

Relevant sections: Introduction and opening of §2.

### P1 PDF pp. 2–4 — LRC definition, reconstruction cost, non-MDS boundary

Direct text inspection establishes:

- `reconstruction cost` is the number of fragments required to reconstruct an unavailable data fragment;
- `(k,l,r)` LRC divides `k` data fragments into `l` groups, computes one local parity per group, and adds `r` global parities;
- the small `(6,2,2)` example reconstructs one data fragment from three fragments rather than six in the compared RS example;
- LRC is explicitly **not MDS**;
- the authors target a maximally recoverable construction over the failure patterns that are information-theoretically decodable for that topology.

This supports a repair-cost trade-off, not a generic `LRC is more durable than RS` statement.

### P1 PDF p. 7 — replication semantics, asynchronous conversion, resumable progress, completion metadata

This page was inspected both through the PDF text layer **and visually**.

Directly established on the page:

- each extent is normally replicated on multiple / usually three ENs;
- each write is committed to all nodes in the replica set before acknowledgment;
- sealing makes an extent immutable and eligible for erasure coding;
- erasure coding is asynchronous and off the client-write critical path;
- the SM schedules sealed extents according to policy and system load;
- `LRC (12,2,2)` produces sixteen fragments;
- an EN is designated as the coding coordinator;
- coordinator/target ENs retain conversion progress by persisting it into new fragments;
- another EN can resume conversion from that persisted progress after failure;
- after the whole extent is coded, the SM records fragment boundaries and completion flags;
- full replicas are then scheduled for deletion.

**Visual check:** Figure 7, `Erasure Coding of an Extent`, and the adjacent §4.1–4.2 text were directly rendered. This is sufficient for the topology/sequence claim made in Case 24; no uninspected visual detail is used.

### P1 PDF p. 8 — on-demand reconstruction vs durable repair; fault vs upgrade domains

This page was inspected both through the PDF text layer **and visually**.

Directly established:

- Figure 8 is titled `Reconstruction for On-Demand Read`;
- a fragment can be reconstructed by another EN, cached, and returned to the client when the normal target is unavailable/hot;
- extended EN/disk unavailability instead causes the SM to initiate reconstruction on a different EN;
- the latter operation writes the result to disk rather than returning it to the client;
- placement accounts separately for `fault domain` and `upgrade domain`;
- fault domains describe correlated hardware failure (rack example), while upgrade domains describe nodes intentionally taken offline together;
- they are typically orthogonal;
- the illustrated LRC layout exploits local groups while keeping relevant fragments in different fault domains, even when members from different local groups share an upgrade domain.

**Visual check:** Figure 8 and the complete two-column text around §§4.2–4.4 were rendered. The image supports the distinction between a client reconstruction-read path and the surrounding placement discussion. The case does not infer unlabeled arrows or implementation details beyond the caption/text.

### P1 PDF pp. 8–9 — scheduled maintenance

Direct text inspection establishes that the stream layer simultaneously handles client I/O and system-generated create/delete/replicate/reconstruct/scrub/move work. The authors explicitly warn that unconstrained I/O can make the system unusable and describe throttling/scheduling at EN and SM levels.

This supports the engineering statement:

> automated retention maintenance remains resource-bounded work.

It does **not** support a quantitative universal claim about repair priority or bandwidth for Azure beyond the bounded system.

### P1 PDF p. 9 — CRC and conversion validation gate

Direct text inspection establishes:

- CRCs detect data/metadata corruption;
- CRC-failing reads/reconstructions can retry other encoded fragment combinations;
- a fragment with a corrupt block is scheduled for regeneration;
- after encoding, multiple decoding combinations are tested;
- decoded fragments are CRC-checked;
- a final CRC over the data is checked against the original full extent;
- only after successful checks are coded fragments persisted / EC allowed to complete;
- any detected failure aborts coding, leaves the full copies intact, and causes later retry on another EN.

A visual screenshot of this page was attempted but the remote PDF screenshot cache returned a cache miss. The **text layer was directly inspected**, and no figure/layout claim from this page is used. The grounding record keeps this facsimile boundary explicit.

### P1 PDF p. 10 — production LRC vs RS comparison

Direct text inspection establishes:

- the production comparison is `LRC (12,2,2)` versus `RS (12,4)`;
- both are compared at `1.33x` storage cost;
- the small-I/O section states LRC reconstruction reads six fragments;
- ordinary RS reconstruction reads twelve in the compared path;
- the paper reports production-cluster latency/I/O measurements but Case 24 uses the **dependency/read-set fact**, not a universal performance number.

The case deliberately does not turn one production measurement into a timeless statement that `6 reads is always faster than 12`.

### P1 PDF p. 11 — prior-art / design-trade-off boundary

Direct text inspection establishes:

- LRC is described as an improvement over the authors’ earlier Pyramid Codes;
- the paper discusses Reed–Solomon, LDPC-related storage codes, Weaver, HoVer, Stepped Combination, and other reconstruction-bandwidth approaches;
- the authors explicitly characterize LRC as non-MDS and describe extra/local parity as a storage-overhead-versus-reconstruction-efficiency trade-off.

This blocks invention-priority inflation.

### P2 Microsoft Research record — 2007 near prior art

Direct inspection of the Microsoft Research publication page establishes:

- authors Cheng Huang, Minghua Chen, Jin Li;
- report number `MSR-TR-2007-25`;
- date March 2007;
- abstract framing in terms of trade-offs between storage space and access efficiency in reliable data storage.

No claim from P2 is made about production deployment in WAS.

---

## Claim-by-claim grounding

| Case-24 claim | Source | Location | Layer | Strength |
| --- | --- | --- | --- | --- |
| active/sealed extent begins under full replication before EC conversion | P1 | PDF p. 1; p. 7 §§4.1–4.2 | H/P | direct |
| client write is committed to replica set before acknowledgement | P1 | PDF p. 7 §4.1 | H/P | direct |
| EC conversion is asynchronous / off write critical path | P1 | PDF p. 7 §4.2 | H/P | direct |
| LRC defines smaller reconstruction read-set than compared RS path | P1 | PDF pp. 2–3 §2.1; p. 10 §5.1 | H/P | direct |
| LRC(12,2,2) and RS(12,4) compared at 1.33x | P1 | PDF p. 10 | H/P | direct |
| LRC is non-MDS; failure tolerance is pattern/code dependent | P1 | PDF pp. 3–4; p. 11 | H/P | direct |
| encoding progress is persisted into new fragments and can be resumed by another EN | P1 | PDF p. 7 §4.2 | H/P | direct + visual page inspection |
| fragment-boundary / completion metadata precedes old-replica deletion | P1 | PDF p. 7 §4.2 | H/P | direct + visual page inspection |
| validation failure leaves full extent copies intact and retries later | P1 | PDF p. 9 §4.4 | H/P | direct text inspection |
| on-demand reconstruction result may be cached/returned instead of durably repaired | P1 | PDF pp. 7–8 | H/P | direct + visual page inspection |
| extended unavailability causes SM-initiated reconstruction written to disk | P1 | PDF p. 8 | H/P | direct + visual page inspection |
| `fault domain` and `upgrade domain` are distinct | P1 | PDF p. 8 §4.3 | H/P | direct + visual page inspection |
| `local reconstruction` does not mean physical co-location | P1 | code definition + PDF p. 8 placement | E | strong reconstruction |
| coded recoverability does not identify repair I/O/read-set cost | P1 | §§2.1, 5.1 | E | strong reconstruction |
| representation transition has a distinguishable in-progress state | P1 | §4.2 + §4.4 | E | strong reconstruction |
| progress/completion/integrity metadata can be constitutive retention state | P1 | §4.2 + §4.4 | E | strong reconstruction |
| LRC production use is not erasure-code / repair-tradeoff invention priority | P1 + P2 + reused Case19 | Related Work; 2007 record | H boundary | strong |

---

## Key retention deductions

### D1 — coded recoverability ≠ repair cost

**Evidence:** P1 directly compares reconstruction read-set size under LRC and RS at the same normalized storage cost.

**Inference:** `there exists enough surviving information to reconstruct` is weaker than `reconstruction mobilizes a small amount of distributed state`.

**Boundary:** no universal ranking of codes, latency, or durability follows.

### D2 — local reconstruction ≠ physical co-location

**Evidence:** the code groups fragments algebraically, while §4.3 separately distributes them over racks/fault domains and upgrade domains.

**Inference:** locality is first a dependency relation; placement decides where those dependencies live.

**Boundary:** the case does not define locality for every later LRC/LRC-like code.

### D3 — read recovery ≠ durable fragment repair

**Evidence:** P1 explicitly contrasts a client-initiated reconstruction read whose result is cached/returned with an SM-initiated reconstruction whose result is written to disk after extended unavailability.

**Inference:** service can recover before durable redundancy is repaired.

### D4 — produced coded bytes ≠ accepted coded representation

**Evidence:** progress can be persisted during conversion; validation can still fail; on failure the old full copies remain; completion flags are recorded before old full replicas are scheduled for deletion.

**Inference:** transition/admissibility state is required in addition to the raw presence of new fragments.

### D5 — administrative topology can be a retention constraint

**Evidence:** WAS separately defines upgrade domains, intentionally taken offline together, and maps LRC local groups to remain efficiently readable during upgrade-domain unavailability.

**Inference:** planned maintenance can create a simultaneous-unavailability domain even when nothing has physically failed.

---

## Prior-art controls

### Rejected: “Microsoft invented erasure coding in 2012”

Case 19 already records Reed–Solomon 1960 and f4’s explicit non-priority stance. Case 24 reuses that boundary.

### Rejected: “LRC introduced the idea of trading storage overhead for easier repair/access”

P2 is a same-lab 2007 source whose title and abstract explicitly frame Pyramid Codes as a storage-space/access-efficiency trade-off. P1 itself also names several related code families in its Related Work.

### Allowed bounded historical statement

The 2012 Huang et al. paper introduces the named **Local Reconstruction Codes (LRC)** described there and reports their production use/design in Windows Azure Storage. This is a paper/system contribution claim, not a universal invention claim for local repair.

---

## Related-repository duplication check

GitHub code search was run against `tmzncty/computing-archaeology` for:

- `Azure LRC Local Reconstruction Code erasure coding`;
- `erasure coding`.

No dedicated indexed result was returned. That justifies a retention-specific bounded case here, but does not prove the other repository contains no remotely related distributed-storage material.

The routing rule remains:

- coding-theory genealogy / Azure architecture history → primarily `computing-archaeology` if developed;
- cross-mechanism comparison of recoverability, repair cost, transition state, and retained control metadata → `technical-retention`.

---

## Facsimile / inspection boundary

Direct visual inspection completed:

- **PDF p. 7:** Figure 7 and adjacent text for asynchronous coding, coordinator role, persisted progress, completion metadata, and source-replica deletion sequence.
- **PDF p. 8:** Figure 8 and adjacent text for on-demand reconstruction plus fault-/upgrade-domain placement.

Direct text-layer inspection completed for the rest of the cited primary paper, including the code definition, non-MDS discussion, CRC validation gate, production LRC-vs-RS comparison, and Related Work.

A screenshot request for PDF p. 9 returned a remote cache miss. Therefore this record makes **no visual-layout or figure claim from p. 9**; its consistency/CRC statements rely on directly inspected PDF text only.

---

## Unsupported / deliberately withheld claims

- `WAS LRC guarantees exactly the same durability as every possible 3-replica deployment` — **withheld**; the paper models and compares reliability under specified assumptions, which this case does not universalize.
- `all Azure customer data used LRC(12,2,2)` — **withheld**.
- `active mutable extents were themselves maintained as LRC` — **contradicted by bounded description; coding candidate is sealed/immutable extent**.
- `local parity fragments are physically colocated with their data group` — **contradicted as a general reading by the placement discussion**.
- `a successful reconstruction read means the lost durable fragment has been replaced` — **contradicted by the separate SM-initiated disk-write repair path**.
- `any fragment bytes produced during conversion can replace the three source replicas` — **contradicted by persisted-progress, validation, completion, and deletion sequence**.
- `LRC invented local repair / locality in coding theory` — **withheld and historically overbroad**.
- later Azure Storage code parameters, persistence semantics, SLAs, hardware, geo-redundancy behavior, or current implementation — **out of scope**.

---

## Maturity decision

**Promote / record Case 24 as `grounded`.**

The central comparison does not depend on an uncited blog, a modern retrospective, or an analogy. A single unusually rich period-primary production paper directly supplies:

- code-local reconstruction dependency;
- explicit reconstruction-cost vocabulary;
- production code parameters;
- full-replica → erasure-coded transition sequence;
- resumable conversion progress;
- completion metadata;
- CRC validation and abort behavior;
- on-demand reconstruction versus persistent repair;
- hardware fault domains versus planned upgrade domains;
- background scheduling/throttling.

The 2007 Pyramid record and existing Case-19 Reed–Solomon boundary control novelty claims. Remaining open work is intentionally different: mutable erasure-coded currentness/consistency, other LRC families and repair-bandwidth regimes, distributed integrity scrubbing, and later production semantics.
