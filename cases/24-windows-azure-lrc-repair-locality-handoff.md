# Windows Azure Storage LRC: Repair Locality, Redundancy-Mode Handoff, and Failure-Domain Placement

## Scope

- **Bounded system:** Windows Azure Storage (WAS) as described by Huang et al. at USENIX ATC 2012.
- **Bounded mechanism:** the production use of Local Reconstruction Codes (LRC), especially `LRC (12, 2, 2)`, together with the stream-layer transition from three full replicas of an active/sealed extent to validated erasure-coded fragments, on-demand reconstruction reads, durable fragment reconstruction, and fault-/upgrade-domain placement.
- **Bounded period:** the production design reported in June 2012. The paper states that WAS had been in production since November 2008; this case does **not** reconstruct the whole 2008–2012 evolution.
- **Primary source:** Cheng Huang, Huseyin Simitci, Yikang Xu, Aaron Ogus, Brad Calder, Parikshit Gopalan, Jin Li, and Sergey Yekhanin, “Erasure Coding in Windows Azure Storage,” *2012 USENIX Annual Technical Conference*, June 2012, pp. 15–26.
- **Near prior-art control:** Cheng Huang, Minghua Chen, and Jin Li, “Pyramid Codes: Flexible Schemes to Trade Space for Access Efficiency in Reliable Data Storage Systems,” Microsoft Research Technical Report MSR-TR-2007-25, March 2007. Case 19 already carries the older Reed–Solomon 1960 boundary, so it is reused rather than rebuilt here.
- **Research question:** what changes when an erasure-coded system optimizes not only whether lost data is reconstructable, but **how much distributed state must be read to reconstruct it**, and when the system itself changes a retained extent from one redundancy regime to another?

This is **not** a general history of Windows Azure Storage, cloud storage, erasure coding, Reed–Solomon codes, locality theory, Azure durability SLAs, or modern Azure Storage. It does not claim that Microsoft invented erasure coding, non-MDS local repair, or the general space-versus-repair trade-off.

The bounded retention comparison is:

> **Recoverability is not a sufficient description of a coded retention regime. In WAS, the cost and topology of exercising recoverability matter, and the system can itself move an immutable extent from triple replication to LRC only through a resumable, checked, metadata-marked handoff before the old replicas are discarded.**

---

## Historical vocabulary

The 2012 paper explicitly uses:

- `Windows Azure Storage (WAS)`;
- `stream layer`;
- `extent`;
- `active extent` and `sealed` extent;
- `replica set`;
- `erasure coding`;
- `Local Reconstruction Codes (LRC)`;
- `LRC (12, 2, 2)`;
- `data fragment`, `local parity`, and `global parity`;
- `reconstruction cost`;
- `reconstruction read`;
- `Stream Manager (SM)` and `Extent Node (EN)`;
- `coordinator`;
- `fragment boundaries` and `completion flags`;
- `fault domain` and `upgrade domain`;
- `CRC`;
- `scrub`;
- `throttling` and `scheduling`.

The following are **project engineering terms**, not historical vocabulary attributed to Microsoft:

- `repair-cost geometry`;
- `repair/read-set locality`;
- `redundancy-mode handoff`;
- `transition gate`;
- `redundancy-regime currentness`;
- `source-replica retirement`;
- `planned-unavailability topology`.

`Local` in LRC is therefore preserved as a code/design term. It is not silently translated into `physically nearby` or `co-located`.

---

## Historical record

### H/P — active extents are first retained by full replication; sealed extents become coding candidates

The paper describes the WAS stream layer as append-only. Data is appended to **active extents**, and the stream layer normally keeps three replicas. In the implementation section, each write is committed to all nodes in the replica set before the client is acknowledged. An extent is sealed when it reaches its size threshold or the replica set changes after failure; sealing makes its data immutable and makes it eligible for erasure coding.

The introduction states the representation transition plainly: data begins as three full copies, sealed extents are erasure-coded lazily in the background, and the old full copies are deleted after the extent becomes erasure-coded.

**Primary anchors:** Huang et al. 2012, PDF p. 1, Introduction; PDF p. 7, §§4.1–4.2.

This case uses that transition as a retention problem. It does **not** infer that active mutable client data is directly maintained as LRC fragments.

### H/P — LRC introduces reconstruction cost as a first-class code-design concern

The paper defines `reconstruction cost` as the number of fragments that must be read to reconstruct an unavailable data fragment. Its small `(6,2,2)` example divides six data fragments into two local groups, adds one local parity per group plus two global parities, and can reconstruct a single missing data fragment from three other fragments rather than the six required by the compared Reed–Solomon example.

The production comparison uses `LRC (12, 2, 2)`: twelve data fragments, two local parities, and two global parities, for sixteen total fragments and `1.33x` normalized storage. The paper compares it with `RS (12,4)`, also `1.33x`, and reports that a single data-fragment reconstruction with production LRC reads six fragments while ordinary RS reconstruction requires twelve.

**Primary anchors:** Huang et al. 2012, PDF pp. 2–3, §2.1; PDF p. 10, §5.1.

The retention-specific point is narrower than a performance claim:

> two coding regimes can have the same normalized storage overhead while imposing different amounts of distributed read work to recover one missing current fragment.

### H/P — LRC is not MDS, so locality is a trade-off rather than free extra fault tolerance

The paper explicitly states that its LRC is not Maximum Distance Separable (MDS). The local-parity structure reduces reconstruction cost, but a code with the same total number of parity fragments need not decode every failure pattern of that cardinality. The authors choose equations with a maximally recoverable property relative to the information-theoretically decodable patterns of their LRC topology.

The Related Work section makes the trade-off explicit again: additional local-parity/storage structure is used to obtain more efficient reconstruction than the compared Reed–Solomon design.

**Primary anchors:** Huang et al. 2012, PDF pp. 2–4, §2.2; PDF p. 11, Related Work.

Therefore this case does not treat `local repair` as an unqualified durability improvement. Fault tolerance remains code- and failure-pattern-dependent.

### H/P — erasure coding is asynchronous and its progress is itself persisted

For sealed extents, the Stream Manager periodically selects coding work according to policy and load. The paper says the coding process is **completely asynchronous** and off the critical path of client writes.

For `LRC (12,2,2)`, the Stream Manager creates sixteen target fragments and designates a coordinator EN. The coordinator chooses fragment boundaries and streams encoded fragments to the target ENs. Crucially, the coordinator and targets track encoding progress and **persist that progress into the new fragments**, allowing a different EN to resume work after a failure.

**Primary anchor:** Huang et al. 2012, PDF p. 7, §4.2 and Figure 7.

This is direct evidence that the transition itself has retained control state. The data fragments are not the only state that must survive for the conversion to complete correctly.

### H/P — completion metadata gates retirement of the old full replicas

After an entire extent has been coded, the coordinator notifies the Stream Manager. The Stream Manager then updates extent metadata with fragment boundaries and **completion flags**. Only after that documented sequence does it schedule the full replicas for deletion.

The paper’s consistency section adds a stronger gate. After encoding, the coordinator attempts several decoding combinations, checks reconstructed-fragment CRCs, then computes a full-data CRC against the original extent. If validation succeeds, coded fragments are persisted. If validation fails, the coding operation is aborted, **the full extent copies remain intact**, and coding is scheduled again later.

**Primary anchors:** Huang et al. 2012, PDF p. 7, §4.2; PDF p. 9, §4.4 `Consistency of Coded Data`.

This establishes a bounded transition relation:

```text
three full replicas of sealed extent
    -> asynchronous fragment production
    -> persisted coding progress
    -> decoding / CRC validation
    -> coded-fragment persistence
    -> extent metadata + completion flags
    -> schedule old full replicas for deletion
```

The project calls this a **redundancy-mode handoff**. That phrase is an engineering reconstruction, not a period WAS term.

### H/P — an on-demand reconstruction read and durable fragment repair use similar decoding but different completion conditions

If the EN holding a requested fragment is unavailable or hot, the client can contact another fragment-holding EN. That EN reads the needed source fragments, reconstructs the requested fragment, caches it locally, and returns the result to the client. Figure 8 names this path `Reconstruction for On-Demand Read`.

If an EN or disk remains unavailable for an extended period, the Stream Manager instead initiates reconstruction on another EN. The paper says the operation is nearly the same decoding process, except that it is initiated by the SM and **the result is written to disk rather than returned to the client**.

**Primary anchor:** Huang et al. 2012, PDF p. 8, Figure 8 and §4.2.

Thus the same algebra can support two different retention operations:

```text
missing / slow fragment + client demand
    -> reconstruct enough for service
    -> cache / return result

extended fragment unavailability
    -> system-initiated reconstruction
    -> write replacement fragment to disk
```

Successful read recovery is not the same completion event as durable replacement of a lost fragment.

### H/P — code locality and physical failure-domain placement are separate design relations

WAS places fragments according to load and reliability. The paper distinguishes two correlated domains:

- a **fault domain**, such as a rack whose members can fail together because of common hardware;
- an **upgrade domain**, whose members are intentionally taken offline together during an upgrade cycle.

For maximum rack-failure independence in the example stamp, the sixteen LRC fragments are placed on different racks. Yet WAS intentionally uses fewer upgrade domains than fragments. It exploits LRC’s local-group structure by putting corresponding members of different local groups in the same **upgrade domain while keeping them in different fault domains**. The paper reports nine upgrade domains for its illustrated `LRC (12,2,2)` layout and says that taking one upgrade domain offline still leaves each data fragment directly readable or efficiently reconstructable from its local group.

**Primary anchor:** Huang et al. 2012, PDF p. 8, §4.3.

This blocks a misleading reading of `local reconstruction`:

> `local` in the code does not mean `physically co-located`.

The smaller reconstruction dependency set and the physical/administrative topology are related by placement policy, but they are not the same relation.

### H/P — maintenance consumes capacity and is explicitly scheduled against foreground service

The stream layer simultaneously handles foreground operations and system work including replication, reconstruction, scrub, movement, deletion, and erasure coding. The paper warns that allowing all I/O types to run freely can make the system unusable, so ENs and the Stream Manager throttle and schedule work using local/system load. Coding must also keep up with incoming data while critical re-replication can have competing priority.

**Primary anchor:** Huang et al. 2012, PDF pp. 8–9, §4.4 `Scheduling of Various I/O Types`.

This is a second production witness, after Dynamo Case 23, that automated retention maintenance remains resource-bounded work rather than disappearing merely because it is background activity.

### H/P — corruption detection and coding validation are separate from mere fragment existence

WAS uses CRC fields for data and metadata. A read or reconstruction that fails CRC can retry using other fragment combinations, while the fragment containing the corrupted block is scheduled for regeneration. During initial encoding, reconstruction combinations and a final full-extent CRC check must succeed before the coding operation is allowed to complete; failure aborts the conversion and preserves the full copies.

**Primary anchor:** Huang et al. 2012, PDF p. 9, §4.4 `Consistency of Coded Data`.

That evidence supports a specific currentness/admissibility distinction: physically produced coded bytes are not automatically the representation whose existence authorizes retirement of the previous redundancy regime.

### H/S/P boundary — LRC is a 2012 WAS design, not the invention of erasure coding or the general locality trade-off

The 2012 paper itself describes LRC as an improvement over the authors’ earlier **Pyramid Codes** and situates it among Reed–Solomon, LDPC-derived storage codes, Weaver, HoVer, Stepped Combination, and other repair-bandwidth work.

Microsoft Research’s record for Huang, Chen, and Li’s **MSR-TR-2007-25, March 2007** describes Pyramid Codes as exploring the trade-off between storage space and access efficiency in reliable data storage. Case 19 already records Reed and Solomon’s 1960 paper as older coding-theory prior art.

Therefore:

- `WAS production LRC in 2012` ≠ `invention of erasure coding`;
- `LRC repair locality` ≠ `first historical recognition that redundancy can trade storage for repair/access efficiency`;
- `production adoption` ≠ `genealogy of every later locally repairable code`.

---

## Retained state

The bounded WAS mechanism retains more than client payload.

### 1. Extent payload

The append-block contents that must remain readable as the extent moves from active replicated state to sealed coded state.

### 2. Replication/coding representation state

Before conversion, the extent exists as full replicas. After successful conversion, its durable representation is a set of LRC data/local-parity/global-parity fragments. During conversion, both forms can coexist.

### 3. Fragment boundaries and placement

Clients and storage components must know which byte ranges belong to which fragments and which ENs hold them.

### 4. Coding progress

Progress persisted in newly produced fragments lets another EN resume an interrupted conversion.

### 5. Completion/admissibility metadata

Extent metadata and completion flags mark that the new representation has crossed the system’s documented completion boundary before old replicas are retired.

### 6. Integrity evidence

CRCs are retained relations used to reject corrupt reads/fragments and to validate the new encoded representation.

### 7. Failure-/upgrade-domain placement

The same set of fragment bytes can present different practical fault/maintenance exposure depending on rack and upgrade-domain assignment.

### 8. Maintenance scheduling state

SM/EN load and scheduling decisions determine when coding, reconstruction, regeneration, scrub, and deletion can consume resources. This is not payload, but it affects how quickly degraded or transitional states converge.

---

## Substrate and representation

This case crosses several layers:

- disks on Extent Nodes;
- full replicated immutable extents;
- LRC data fragments;
- local and global parity relations;
- Stream Manager metadata;
- fragment-local persisted conversion progress;
- CRC-protected append blocks and metadata;
- rack/fault-domain topology;
- rolling-upgrade domains;
- in-memory reconstructed caches for foreground reads.

The case deliberately avoids treating the mathematical code as the whole storage system. Coding equations determine reconstructability, but the actual retained service also depends on placement, integrity checking, metadata, transition progress, scheduling, and repair.

---

## Retention mechanism

### Full replication while active

Client writes are committed to the full replica set before acknowledgement in the bounded stream-layer description.

### Immutability boundary

Sealing makes an extent an immutable candidate for background erasure coding. This is an important precondition: this case does not establish how WAS would maintain arbitrary in-place mutations across coded fragments.

### Asynchronous erasure-code conversion

A coordinator EN converts a sealed extent into data/local/global parity fragments while progress is persisted for restartability.

### Validation-gated representation change

The new coded state is checked through decode trials and CRC comparison. Failure aborts the transition and retains the old full copies.

### Metadata-gated source retirement

Fragment boundaries/completion flags are recorded before old full replicas are scheduled for deletion.

### Low-read-set reconstruction

For one unavailable data fragment, LRC’s local parity permits reconstruction from a smaller group than the compared RS design.

### Foreground recovery

A reconstruction read can synthesize and cache a requested fragment without waiting for the system to establish a new durable fragment placement.

### Background durable repair

Longer unavailability triggers Stream-Manager-initiated reconstruction whose result is written to disk on another EN.

### Integrity repair

CRC failures can cause alternate decoding attempts and regeneration of a corrupt fragment.

### Placement maintenance

Fragment placement separately manages hardware-correlated fault domains and planned upgrade domains.

---

## Addressing and access geometry

The client-facing request does not directly name a parity equation. The stream layer resolves an extent and fragment to an EN; direct reads normally contact the EN holding the required fragment.

When that path is unavailable or too slow:

```text
requested extent range
    -> target fragment unavailable/hot
    -> choose reconstruction path
    -> read the dependency set required by code/local group
    -> decode requested fragment
    -> cache / return to client
```

For durable repair:

```text
extended fragment unavailability
    -> SM chooses replacement EN
    -> read reconstruction dependency set
    -> decode missing fragment
    -> write replacement fragment to disk
```

The access geometry of a missing fragment is therefore a **distributed dependency geometry**. LRC changes that geometry by reducing the number of fragments that must participate in the common single-data-fragment reconstruction path.

---

## Read, write, conversion, and deletion semantics

### Read

- direct when the target fragment is available;
- reconstruction read when the target is unavailable/hot;
- reconstruction can be cached in memory without constituting durable fragment repair.

### Write

For the bounded coded regime, extents are immutable. The paper’s client write path applies to active replicated extents before sealing.

### Conversion

Conversion is not one atomic physical write. It is resumable background work with persisted progress, validation, final fragment persistence, metadata completion, and later retirement of source replicas.

### Deletion

The deletion relevant here is **deletion of the old full replicas after successful coding**, not application-level object deletion. This is a representation transition, not forgetting of the client’s extent.

---

## Failure and forgetting

### Interrupted coding

Because progress is persisted in new fragments, interruption need not force conversion to restart from zero. But the system still distinguishes work-in-progress from a completed coding representation.

### Failed validation

If decode/CRC checks fail, conversion is aborted and the old full copies remain. Therefore partially produced fragments do not authorize source-replica retirement.

### Missing fragment

A fragment can be unavailable transiently and reconstructed for a read without immediately changing durable placement.

### Extended fragment loss

Longer unavailability causes durable reconstruction onto another EN.

### Corrupt fragment

CRC failure can reject the candidate read/reconstruction and schedule fragment regeneration.

### Correlated hardware failure

Fault-domain placement is intended to keep related coding fragments from sharing the same rack failure.

### Planned upgrade unavailability

Upgrade domains represent a different source of simultaneous unavailability. WAS deliberately maps code groups across this administrative topology rather than treating it as identical to hardware fault domains.

### Resource starvation / delayed maintenance

Coding and reconstruction consume network/disk resources and must be scheduled. The code can be mathematically recoverable while actual repair/conversion time is lengthened by foreground load and maintenance priorities.

---

## Engineering reconstruction

### E — coded recoverability ≠ repair cost

Knowing that surviving fragments mathematically determine a missing fragment does not determine the amount of network/disk work required to exercise that relation. In the production comparison, RS(12,4) and LRC(12,2,2) both have `1.33x` storage, yet the common single-data-fragment read set differs.

This is **not** a claim that smaller read sets always dominate: straggler strategy, parity reconstruction, fault patterns, topology, CPU work, and workload can change the trade-off.

### E — local reconstruction ≠ physical co-location

The code’s locality is a smaller dependency set. Physical placement is separately constrained by racks/fault domains and upgrade domains. Indeed, WAS can put members of different local groups in the same upgrade domain while keeping them in different fault domains.

### E — on-demand recoverability ≠ restored durable redundancy

The reconstruction-read path can satisfy a client and leave a cache result, while durable repair writes a replacement fragment after longer unavailability. Availability can therefore recover before the system has repaired durable placement.

### E — a redundancy regime can have a transition state

An immutable extent need not be simply `replicated` or `coded` at every instant. During asynchronous conversion, full copies and partial/new coded fragments coexist, progress metadata permits resumption, validation has not necessarily passed, and completion metadata has not necessarily authorized old-replica deletion.

The project therefore treats **representation transition** as a retention state in its own right.

### E — transition metadata can be constitutive retention state

Persisted progress makes conversion resumable; completion flags and fragment boundaries mark the accepted new representation; CRCs qualify it. Losing or corrupting this control state can change whether identical-looking fragment bytes are actionable as the completed retained object.

### E — failure domain ≠ upgrade domain

The paper’s topology distinguishes correlated hardware failure from planned simultaneous maintenance. A retention system can therefore need to remain available across an administrative offline event even when no medium has physically failed.

---

## Functional analogies and cross-case comparison

### A — Case 19 f4: coding algebra vs repair-cost geometry

Case 19 already proves that erasure-code algebra is not the same thing as failure-domain independence and that requested-object read continuity can precede full-fragment repair. Case 24 adds a different axis: **among code designs that can retain comparable storage efficiency, the amount of source state needed for one reconstruction can itself be an explicit design target**.

The overlap is functional, not genealogical. f4 and WAS are different production systems with different code structures and maintenance paths.

### A — Case 17 RAID: reconstructability vs distributed locality

RAID Case 17 shows that parity can synthesize a missing contribution and that degraded service can precede completed rebuild. WAS LRC adds a distributed read-set/topology problem: reconstruction may involve many ENs, so locality and scheduling change the operational cost of exercising the redundancy relation.

This does not make LRC merely `RAID over the network`.

### A — Case 23 Dynamo: maintenance budgeting

Both systems explicitly budget background retention work against foreground service. Dynamo budgets handoff/synchronization; WAS schedules coding, replication, reconstruction, scrub, movement, and deletion. The shared conclusion is only that automated maintenance has resource cost. The historical mechanisms and currentness semantics are different.

### A — Cases 04 / 22: representation change without object forgetting

Mapped Flash can retire an old physical embodiment after remapping, and OS/VS2 paging can release a frame when a sufficient backing copy exists. WAS can delete old full replicas after a new coded representation passes validation and is marked complete. In each case, ending one embodiment relation need not end the higher-level retained state.

The triggers and proof obligations differ, so this is a relation-level analogy only.

---

## Philosophical interpretation

### I — recoverability is a qualified capability, not a bare yes/no property

LRC is useful for this project because it makes a normally hidden condition of persistence measurable: not only *can* a lost current fragment be reconstructed, but *how much other retained state must be mobilized*, across which nodes/domains, and under what scheduling pressure?

This supports a narrow philosophical caution:

> technical availability is partly constituted by the cost and organization of the recovery path, not merely by the abstract existence of enough information somewhere in the system.

This is not a definition of memory, archive, or `Bestand`.

### I — persistence can include a validated change of its own redundancy form

The replicated extent and the coded extent are materially/organizationally different embodiments of one higher-level stream extent. The transition is not trusted merely because new bytes exist: resumable progress, integrity validation, completion metadata, and delayed source retirement mediate when the new form counts as sufficient.

The philosophical use is therefore about **continuity across a governed change of representation**, not about claiming that software metadata makes physical media irrelevant.

---

## Counterexamples and limits

1. **LRC is not evidence that all erasure coding has low repair cost.** The comparison is parameter- and workload-specific.
2. **Lower reconstruction cost is not free fault tolerance.** The paper explicitly distinguishes LRC from MDS codes and analyzes failure-pattern limits.
3. **`Local` does not mean physically nearby.** WAS separately spreads fragments across hardware fault domains and arranges upgrade domains.
4. **A reconstruction read is not durable repair.** One serves/caches a request; the SM-initiated path writes a replacement fragment to disk.
5. **Fragment production is not conversion completion.** Validation and completion metadata precede full-replica retirement.
6. **The case is about immutable sealed extents.** It does not establish mutable erasure-coded object currentness or conflict semantics.
7. **The 2012 paper is not a complete Azure chronology.** Later Azure Storage designs, codes, SLAs, hardware, and topology require separate sources.
8. **Production LRC is not invention priority for erasure coding/local repair.** Pyramid Codes 2007 and older coding work constrain that claim; Case 19 already records the Reed–Solomon 1960 anchor.
9. **Mode-handoff vocabulary is reconstructed.** WAS documents its sequence; the project’s `redundancy-mode handoff` / `transition gate` terms are analytical labels.

---

## Related-repository routing

Before writing this case, `tmzncty/computing-archaeology` was searched for `Azure LRC Local Reconstruction Code erasure coding` and for the broader term `erasure coding`; no dedicated indexed treatment was found. This case therefore keeps only the retention-specific comparison.

If a future project reconstructs:

- the coding-theory genealogy from Reed–Solomon through Pyramid/LRC and later LRC families;
- the detailed architecture/evolution of Windows Azure Storage;
- coding coefficients, CPU-vectorization, network topology, or hardware economics as historical engineering problems;

that broader material should primarily live in `computing-archaeology`, with this case linking back to it.

---

## Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| WAS initially writes active extents to a usually three-node replica set and seals them before EC eligibility | H/P | direct 2012 paper |
| LRC reduces the read-set/reconstruction cost for one unavailable data fragment relative to the compared RS design | H/P | direct 2012 paper |
| LRC(12,2,2) and RS(12,4) are compared at the same 1.33x storage cost | H/P | direct 2012 paper |
| LRC is not MDS and locality/fault tolerance involve a trade-off | H/P | direct 2012 paper |
| coding occurs asynchronously and persists progress in new fragments for resume | H/P | direct 2012 paper + directly inspected Figure 7 page |
| fragment boundaries/completion flags precede scheduling old replicas for deletion | H/P | direct 2012 paper + directly inspected Figure 7 page |
| decode/CRC validation failure leaves full copies intact and retries conversion later | H/P | direct 2012 paper |
| on-demand reconstruction read and durable fragment reconstruction have different initiators/destinations | H/P | direct 2012 paper + directly inspected Figure 8 page |
| fault domains and upgrade domains are distinct placement constraints | H/P | direct 2012 paper + directly inspected Figure 8/placement page |
| coded recoverability ≠ repair cost | E | bounded comparison from production LRC/RS parameters |
| local reconstruction ≠ physical co-location | E | bounded inference from code definition + documented placement |
| reconstruction read ≠ restored durable redundancy | E/A | direct mechanism + comparison to Cases 17/19 |
| coding progress/completion metadata is constitutive of the representation handoff | E | grounded in documented resume/completion/deletion sequence |
| LRC production use ≠ invention of erasure coding or storage/repair trade-offs | H/S boundary | 2012 Related Work + 2007 Pyramid record + reused Case 19 prior-art boundary |
| LRC solves mutable coded-object currentness | X | explicitly unsupported by this immutable sealed-extent case |
| `local` means same rack / nearby node | X | contradicted by documented placement policy |
| produced coded fragments alone authorize replica deletion | X | contradicted by validation/completion sequence |

---

## Sources

### Primary / contemporary

1. Cheng Huang et al., **“Erasure Coding in Windows Azure Storage,”** *2012 USENIX Annual Technical Conference (USENIX ATC ’12)*, June 2012, pp. 15–26. Microsoft Research publication record: <https://www.microsoft.com/en-us/research/publication/erasure-coding-windows-azure-storage/>. Official Microsoft-hosted paper PDF: <https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/LRC12-cheng-webpage.pdf>.
   - PDF p. 1: active three-copy extent → sealed immutable extent → lazy background EC → deletion of full copies; motivation and reconstruction cost.
   - PDF pp. 2–4: LRC definition, local/global parities, reconstruction cost, non-MDS / maximally-recoverable boundary.
   - PDF p. 7: stream-layer replica semantics, asynchronous coding, coordinator, persisted progress, fragment boundaries/completion flags, replica-deletion sequence.
   - PDF p. 8: Figure 8, on-demand reconstruction versus SM-initiated durable reconstruction; fault vs upgrade domains; LRC-aware placement.
   - PDF p. 9: throttling/scheduling; CRC-based corruption handling; validation before EC completion; abort while retaining full copies.
   - PDF p. 10: production `LRC (12,2,2)` vs `RS (12,4)` at `1.33x` and reconstruction-I/O/latency comparison.
   - PDF p. 11: coding-design prior art and storage-overhead/reconstruction-efficiency trade-off.

2. Cheng Huang, Minghua Chen, and Jin Li, **“Pyramid Codes: Flexible Schemes to Trade Space for Access Efficiency in Reliable Data Storage Systems,”** Microsoft Research Technical Report **MSR-TR-2007-25**, March 2007. <https://www.microsoft.com/en-us/research/publication/pyramid-codes-flexible-schemes-to-trade-space-for-access-efficiency-in-reliable-data-storage-systems/>.
   - Used only as a near prior-art boundary showing that the authors’ storage-space/access-efficiency trade-off predates the 2012 production LRC paper.

### Reused repository prior art

3. [`Case 19 — Facebook f4`](19-facebook-f4-erasure-coded-failure-domains.md) and its grounding record already establish Reed & Solomon 1960 as a canonical earlier code-theory anchor. That work is linked rather than duplicated here.

---

## Evidence maturity

**Status: `grounded`.**

Reasons:

- the central mechanism comes from a named 2012 production-system paper by the engineers involved;
- the Microsoft Research bibliographic record independently fixes title, authors, venue, and June 2012 date;
- the official Microsoft-hosted PDF was directly inspected at the mechanism sections;
- PDF p. 7 was visually inspected, including Figure 7 and the text describing asynchronous coding, persisted progress, completion flags, and old-replica deletion;
- PDF p. 8 was visually inspected, including Figure 8 and the text distinguishing reconstruction read from persistent repair plus fault-/upgrade-domain placement;
- the code/failure trade-off is bounded by the paper’s own non-MDS discussion;
- prior art is controlled by the paper’s Related Work, the authors’ 2007 Pyramid Codes record, and the already-grounded Reed–Solomon boundary in Case 19;
- `computing-archaeology` was checked before creating a new dedicated slice;
- mutable coded-object currentness, later Azure evolution, and general LRC genealogy remain explicitly out of scope.
