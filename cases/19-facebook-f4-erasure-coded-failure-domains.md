# Facebook f4 Erasure-Coded Warm Storage: Failure-Domain Placement, Online Reconstruction, and Background Rebuild

## Scope

- **Bounded system:** Facebook `f4` warm BLOB storage as described at OSDI 2014.
- **Bounded mechanism:** distributed erasure-coded retention across disk/host/rack/datacenter failure domains, especially Reed–Solomon `(10,4)` within a cell plus geo-replicated XOR, with separate online requested-BLOB reconstruction, background full-block rebuild, and placement rebalancing.
- **Bounded period:** the production system described in the October 6–8, 2014 OSDI paper. The paper reports that f4 had already been in production for more than nineteen months and stored more than 65 PB of logical BLOB data at the time of publication.
- **Primary source:** Subramanian Muralidhar et al., “f4: Facebook’s Warm BLOB Storage System,” *11th USENIX Symposium on Operating Systems Design and Implementation (OSDI ’14)*, pp. 383–398.
- **Prior-art control:** Irving S. Reed and Gustave Solomon, “Polynomial Codes Over Certain Finite Fields,” *Journal of the Society for Industrial and Applied Mathematics* 8(2), June 1960, pp. 300–304; plus the f4 paper’s own Related Work statement that f4 uses erasure codes as tools and does not claim to innovate in coding theory.
- **Research question:** what must remain besides coded fragments themselves for a distributed erasure-coded object to remain readable and repairable across multiple physical failure domains?

This is **not** a general history of erasure coding, Facebook storage, Haystack, Reed–Solomon coding theory, RAID, geo-replication, or modern distributed object stores. It does not claim that f4 invented erasure-coded storage.

The bounded comparison is:

> **Coded recoverability is not supplied by parity algebra alone. In f4, usable retention also depends on fragment placement across failure domains, retained mapping/index relations, distinct online and background reconstruction paths, and maintenance that restores both missing content and the intended placement geometry.**

---

## Historical vocabulary

The 2014 f4 paper explicitly uses:

- `warm BLOB storage`;
- `BLOB` / `Binary Large OBject`;
- `immutable binary data`;
- `cell`;
- `distributed erasure coding`;
- `Reed-Solomon(n, k)` and `Reed-Solomon(10,4)`;
- `data blocks`;
- `parity blocks`;
- `stripe`;
- `companion blocks`;
- `normal-case read`;
- `failure-case read`;
- `online reconstruction`;
- `backoff node`;
- `rebuilder node`;
- `coordinator node`;
- `placement balancer`;
- `failure domains`;
- `geo-replicated XOR coding`;
- `buddy block`;
- `XOR block`;
- `effective-replication-factor`.

The following phrases are **project engineering terms**, not claims about Facebook’s historical vocabulary:

- `repair geometry`;
- `fault-domain independence as retained relation`;
- `availability restoration`;
- `redundancy-margin restoration`;
- `nested reconstruction`;
- `coded-state admissibility`;
- `state-class-specific redundancy`.

---

## Historical record

### H/P — f4 stores immutable warm BLOBs with distributed erasure coding

The paper defines Facebook BLOBs as immutable binary data: created once, read many times, never modified, and sometimes deleted. f4 is the specialized warm-storage subsystem for BLOBs whose request rates have fallen enough that lower peak throughput can be traded for greater storage efficiency.

The paper states that f4 stores warm BLOB volumes in cells using distributed erasure coding. Within a datacenter it uses Reed–Solomon `(10,4)` in recent cells and places blocks on different racks to obtain resilience to disk, machine, and rack failures. It separately uses XOR coding across datacenters for datacenter-failure tolerance.

**Primary anchors:** Muralidhar et al. 2014, pp. 384–385 and §5.2–5.5.

### H/P — the encoded data and the index/mapping state use different redundancy regimes

In §5.3 the paper states that f4’s index files use **triple replication within a cell** because the files are small enough that the storage gain from encoding them is not worth the added complexity. The actual BLOB data file, by contrast, is encoded with Reed–Solomon `(n,k)`; recent f4 cells use `n = 10` and `k = 4`.

A name node maintains the mapping between data blocks, parity blocks, and the storage nodes holding them. Storage nodes also hold the index relation from BLOB to data file, offset, and length, plus a location map from data-file offsets to physically stored blocks.

This prevents a simplistic description in which `f4 = Reed–Solomon`. The service requires several retained state classes with different protection choices:

- immutable BLOB payload;
- encoded data/parity blocks;
- BLOB → file/offset/length index state;
- block/parity → storage-node mapping;
- per-volume location maps;
- placement state across racks and datacenters.

**Primary anchors:** Muralidhar et al. 2014, p. 388–389, §5.3.

### H/P — normal reads and failure reads are different recovery paths

The paper says that in normal operation BLOBs are read directly from their data block. If a block is unavailable, it can be recovered from any `n` companion/parity blocks in its stripe. More specifically, the subset of a block corresponding to one BLOB can be decoded from only the equivalent subsets of any `n` companion/parity blocks.

For a failure-case read, a backoff node receives a request already mapped to data file, offset, and length. It reads the equivalent offsets from the surviving companion/parity blocks and, after receiving `n` responses, decodes **only the requested BLOB**.

The paper explicitly contrasts this with full-block repair: the online path does not rebuild the entire block; full-block rebuilding is handled offline by rebuilder nodes.

**Primary anchor:** Muralidhar et al. 2014, p. 389–390, §5.3.

### H/P — background rebuild restores missing blocks under a separate maintenance path

Rebuilder nodes detect disk/node failures by probing and report them to a coordinator node. A rebuilder reconstructs a missing block by fetching `n` companion or parity blocks and decoding them. The paper describes this as heavyweight I/O/network work and says rebuilder nodes throttle themselves to avoid harming online requests.

Coordinator nodes schedule block rebuilds so as to minimize the likelihood of data loss. They also perform cell-wide maintenance work beyond reconstruction itself.

This gives a period-primary separation between:

```text
normal read
    -> direct current data block

failure-case read
    -> online reconstruction of requested BLOB only

background repair
    -> full missing block reconstruction
```

These are different retention operations with different completion conditions and costs.

**Primary anchor:** Muralidhar et al. 2014, p. 390, `Rebuilder Nodes` and `Coordinator Nodes`.

### H/P — coding parameters do not by themselves establish rack-failure independence

The paper treats a rack as the largest failure domain within an f4 cell and attempts to place every data/parity block in a stripe on a different rack and at least a different node. With `(n,k)` coding, this requires at least `n + k` racks of roughly comparable size for the preferred layout.

The implementation is described as best effort. After initial placement, failure, reconstruction, or replacement can produce **placement violations** in which multiple blocks of one stripe occupy the same failure domain. The coordinator’s placement balancer detects and corrects these violations.

Therefore the period system itself separates:

- the algebraic relation among `n` data + `k` parity blocks;
- the physical/topological placement of those blocks;
- maintenance that repairs placement after failures/reconstruction.

**Primary anchor:** Muralidhar et al. 2014, pp. 390–391, §5.5 `Failure Domains and Block Placement`.

### H/P — geo-replicated XOR is a second coding layer with a distinct failure domain

For datacenter tolerance, f4 pairs equivalent blocks from volumes primarily stored in two different datacenters and stores their XOR in a third datacenter. A geo-backoff node can reconstruct a requested region using the local XOR block and the remote buddy/XOR-companion block.

The paper’s quadruple-failure example shows that these layers can compose: a datacenter-level recovery request may encounter rack/host/disk failures affecting the XOR or buddy inputs, causing ordinary single-cell backoff reconstruction to run beneath the geo-level XOR reconstruction.

Thus the system is not one flat code over a homogeneous failure domain. It composes local Reed–Solomon protection with geo-level XOR and ordinary mapping/routing machinery.

**Primary anchors:** Muralidhar et al. 2014, p. 390–391, §§5.4–5.5.

### H/P — logical deletion can depend on a key relation outside the coded fragments

The f4 cells hold read-only data/index files for locked volumes. Rather than keeping Haystack’s delete journal inside f4, each BLOB is encrypted with a per-BLOB key held in a separate key store. The paper says deleting that encryption key renders the BLOB unreadable and thereby logically/effectively deletes it without requiring compaction inside f4.

This is relevant only as a bounded forgetting relation. It does **not** establish that the encoded fragments have been physically erased, nor does it establish cryptographic-erasure semantics for every later Facebook storage system.

**Primary anchor:** Muralidhar et al. 2014, p. 388–389, §5.3.

### H/P — f4 explicitly disclaims erasure-code invention priority

The Related Work section says erasure codes have a long history, names Reed–Solomon and XOR codes, and states that **f4 uses erasure codes as tools and does not innovate in this area**. The paper positions its contribution as the production system design and failure-domain organization, not the invention of the underlying codes.

Reed and Solomon’s 1960 paper provides an external primary anchor for the earlier coding lineage. Its bibliographic record is *Journal of the Society for Industrial and Applied Mathematics* 8(2), June 1960, pp. 300–304, submitted 21 January 1959.

Therefore:

> `f4 production use of Reed–Solomon` ≠ `f4 invention of Reed–Solomon or erasure coding`.

---

## Retained state

The bounded f4 mechanism requires several distinct retention targets.

### 1. Immutable BLOB payload

The application-level binary object expected to remain readable after migration into warm storage.

### 2. Data and parity fragments

The Reed–Solomon stripe embodies enough coded information that missing block content can be reconstructed when a sufficient subset survives.

### 3. Index and location relations

The system must retain how a BLOB maps to its data file, offset, and length, and how logical block ranges map to storage nodes and physical blocks.

### 4. Failure-domain placement relation

Which stripe fragments occupy which racks/nodes/datacenters matters to the fault model. `Fourteen fragments exist` is not equivalent to `fourteen fragments are independently placed`.

### 5. Repair/rebuild state and scheduling

Coordinator/rebuilder activity determines which missing fragments are being regenerated and when reduced redundancy is restored.

### 6. Encryption-key relation

For the bounded delete path, readability additionally depends on the per-BLOB key stored outside f4. This is not a coded data fragment but can determine whether surviving coded data remains service-readable.

---

## Physical / logical substrate

This case spans several layers:

- magnetic disk blocks on storage nodes;
- Reed–Solomon data/parity block relations within an f4 cell;
- XOR relations among equivalent blocks across datacenters;
- rack/host/disk/datacenter topology;
- index and location maps;
- software roles such as storage nodes, name nodes, backoff nodes, rebuilder nodes, coordinator nodes, and router tier;
- external per-BLOB encryption keys.

No single physical fragment is the whole retained BLOB, and no coding equation alone supplies the service’s complete recoverability relation.

---

## Retention mechanism

### Quiescent media retention

The underlying disks retain individual physical blocks. This case does not duplicate disk-media physics.

### Coded redundancy

Within a cell, `n` data blocks and `k` parity blocks create an erasure-coded stripe. A missing contribution can be synthesized from a sufficient surviving subset.

### Failure-domain separation

Fragments are deliberately placed across racks/nodes so one rack or host failure does not consume too many members of the same stripe.

### Online failure reconstruction

Backoff nodes decode only the requested BLOB range after a normal read fails.

### Background full-block rebuilding

Rebuilder nodes restore missing full blocks later, with coordinator scheduling and throttling.

### Placement repair

A placement balancer detects and corrects post-repair/replacement violations that put multiple stripe blocks in one failure domain.

### Geo-level XOR reconstruction

A second coding relation protects against datacenter loss and can itself invoke local Reed–Solomon reconstruction when the needed XOR/buddy blocks have lower-level failures.

---

## Addressing and access geometry

The BLOB-facing interface is not the same as the coded-fragment geometry.

A read begins with a BLOB handle and resolves through index/mapping state to:

```text
BLOB
    -> data file
    -> offset + length
    -> enclosing data block
    -> storage node / physical block
```

Normal read:

```text
mapped BLOB range
    -> direct read from current data block
```

Failure read:

```text
same BLOB range
    -> equivalent ranges from companion/parity blocks
    -> n successful inputs
    -> decode requested BLOB
```

Geo failure:

```text
BLOB range
    -> XOR block range + buddy range
    -> possibly local backoff reconstruction of either input
    -> XOR reconstruction
    -> BLOB
```

Thus application designation, fragment selection, topology placement, and reconstruction are separate relations.

---

## Read semantics

Ordinary f4 reads are nondestructive at the logical interface and usually read the target BLOB directly from its current data block.

Failure changes the read path without necessarily changing the requested logical object. A backoff read is a **reconstructive read**: it gathers equivalent subranges from other coded blocks and decodes the desired BLOB.

Crucially:

> A successful failure-case read does not imply that the failed full block has already been rebuilt.

The service can restore read availability for one object before background maintenance restores the missing block and redundancy margin for the stripe.

---

## Write and erasure semantics

The bounded f4 cells contain locked volumes and therefore primarily support read/delete rather than in-place BLOB modification. Newer content is accumulated elsewhere and migrated into f4 once it becomes warm.

For the deletion path described in §5.3, deleting the externally stored encryption key makes the BLOB unreadable. The encoded physical blocks need not be rewritten or compacted at that moment.

Do not infer from this:

- physical erasure of all coded fragments;
- secure deletion against every adversary;
- an immutable policy for later f4 versions;
- equivalence between loss of a key relation and medium destruction.

---

## Time

This case contains several distinct timescales:

- normal BLOB read latency;
- failure detection by probing;
- online requested-BLOB reconstruction latency;
- full-block reconstruction duration;
- time spent with reduced redundancy after a block/node failure;
- background rebuild scheduling delay;
- placement-balancer convergence after reconstruction/replacement;
- datacenter-failure detection and geo-backoff latency;
- warm-content migration timescale;
- logical-delete time via removal of the external key relation.

These should not be collapsed into one `repair time`.

---

## Maintenance and labor

Persistence in f4 depends on substantial work below the simple BLOB read interface:

- storage-node operation;
- primary/backup name-node state;
- distribution and retention of index/location maps;
- failure probing;
- online decoding on backoff nodes;
- background decoding/rebuild on rebuilder nodes;
- coordinator scheduling of repairs;
- placement balancing after reconstruction/replacement;
- rack/datacenter capacity sufficient to sustain intended failure-domain separation;
- network bandwidth for reconstruction;
- throttling so repair does not destroy foreground service quality;
- separate key-store availability for encrypted BLOBs.

The 2014 paper directly identifies the machine/software roles. Broader operator, datacenter, and manufacturing labor should not be invented from this system paper alone.

---

## Failure / forgetting modes

Distinct failures include:

- disk failure removing one encoded block;
- host failure removing several local resources;
- rack failure simultaneously removing all fragments accidentally colocated there;
- datacenter failure removing an entire cell-level protection domain;
- too many unavailable fragments in one Reed–Solomon stripe to decode;
- loss/corruption of the mapping needed to locate data/parity blocks;
- a placement violation concentrating fragments in one failure domain;
- rebuild delay leaving the stripe at reduced redundancy while more faults arrive;
- resource pressure throttling or delaying background reconstruction;
- failure of inputs needed for geo-level XOR recovery;
- lower-level failures forcing nested reconstruction during geo recovery;
- loss/deletion of a per-BLOB encryption key making surviving coded material unreadable at the service layer.

Do not collapse these into generic `data loss`.

---

## Engineering reconstruction

### E — erasure-code algebra ≠ failure-domain independence

`RS(10,4)` defines what combinations of coded fragments can reconstruct missing data. It does not decide whether fragments sit on independent racks. f4 separately retains and repairs a topological placement relation.

The retention target therefore includes something like:

```text
coded information sufficient
    + placement sufficiently independent for the stated failure model
```

That second line is a system property, not a theorem supplied merely by naming the code.

### E — read availability ≠ completed repair

Backoff nodes can reconstruct one requested BLOB range while the failed full block remains absent. Rebuilder nodes later restore the full block.

Therefore:

> `can answer this read now` ≠ `redundancy has been restored`.

This extends Case 17’s degraded-service distinction into a distributed object-level read path.

### E — reconstructed content ≠ restored placement geometry

Even after reconstruction creates a replacement block, the resulting layout may violate the intended one-fragment-per-failure-domain relation. The placement balancer performs another maintenance step.

So there are at least two repair targets:

1. **content repair** — recreate the missing coded contribution;
2. **geometry repair** — restore fault-domain separation.

### E — distributed erasure coding ≠ replication with smaller copies

A parity block is not merely a partial independent replica of the missing BLOB. The missing contribution is computed from a coded relation across surviving fragments.

At the same time, f4 triple-replicates index files. One system can deliberately combine replication and erasure coding according to state size, complexity, and failure role.

### E — reconstruction can be compositional

The geo-XOR layer can request inputs whose local copies are themselves unavailable, causing local Reed–Solomon backoff reconstruction before the datacenter-level XOR result can be obtained.

The higher-level recovery therefore depends on the continued recoverability of lower-level coded relations. `One repair` can be a stack of nested repairs rather than one flat operation.

### E — redundancy method can be state-class-specific

Bulk BLOB data is Reed–Solomon encoded; small index files are triple replicated; geo protection uses XOR; metadata/name-node relations use their own replication/assignment mechanisms.

`The system uses erasure coding` is therefore too coarse to describe what kind of retention protects each constitutive state.

### E — coded-fragment survival ≠ service readability

For the bounded deletion path, encoded fragments can remain physically present while deletion of an external per-BLOB key makes the service unable to recover the plaintext BLOB.

This is a relation-loss form of logical forgetting, not physical erasure.

---

## Philosophical / media-theoretical interpretation

The mechanism sharpens a narrow problem of **technical sameness without one complete privileged embodiment**.

The BLOB can remain the same service object while:

- no surviving fragment contains the whole missing block;
- one missing contribution is reconstructed from other fragments;
- the reconstruction path changes from direct read to online decoding;
- the full missing block is restored later;
- its placement may then move again to recover failure-domain independence;
- datacenter-level recovery may compose multiple lower-level reconstruction operations.

A cautious philosophical question is therefore:

> If continued availability is secured by relations among fragments, topology, mappings, and repair procedures, which part of that distributed relation is the technical support of the retained object?

This case does **not** answer that by calling parity `memory`, erasure coding `tertiary retention`, or a datacenter topology `Bestand`. Those are separate interpretive questions and must remain subordinate to the mechanism.

---

## Functional analogies

### A — Case 17 RAID parity reconstruction

Both cases reconstruct missing content from coded redundancy rather than a full duplicate. The analogy stops there.

Case 17 is bounded around parity/checksum reconstruction, currentness meta state, degraded operation, and background repair in a disk-array lineage. f4 adds explicitly distributed rack/datacenter failure domains, object-subrange online reconstruction, placement balancing, and nested local/geo coding.

This is functional continuity, not evidence that f4 is simply `RAID over a datacenter`.

### A — Case 05 RADOS replica repair

RADOS can restore an object from version/currentness-qualified complete replicas. f4 can restore missing block/BLOB content from coded fragments, none of which need be a complete duplicate of the missing contribution.

f4’s BLOBs are also immutable in this bounded system, so the case does not supply the same version-order/currentness problem as the RADOS case.

### A — Case 18 ZFS scrub

ZFS scrub proactively looks for unknown integrity failures before ordinary demand. The f4 slice here instead focuses on known/unavailable blocks, failure reads, background rebuild, and placement repair. It does not establish a distributed scrub protocol.

---

## Counterexamples and limits

- Reed–Solomon and erasure coding long predate f4; the paper itself explicitly disclaims coding-theory innovation.
- The case does not establish that every f4 deployment used exactly `(10,4)` forever; the source says **recent f4 cells** used `n = 10`, `k = 4`.
- Code parameters alone do not prove rack/datacenter tolerance; the paper’s placement policy and geo layer are separate evidence.
- A successful online BLOB reconstruction does not prove that the failed full block or redundancy margin has already been restored.
- A successfully rebuilt block does not prove the placement geometry is already ideal; the source explicitly provides a placement-balancer correction path.
- Triple-replicated f4 index files are a direct counterexample to `all constitutive f4 state is erasure-coded`.
- The case does not establish mutable-object consistency, consensus, version conflict resolution, or a generic distributed-currentness protocol.
- The key-delete path establishes service unreadability/logical deletion in this design, not physical sanitization of encoded fragments or a universal cryptographic-erasure guarantee.
- Later Facebook warm/cold-storage systems, Local Reconstruction Codes, modern object-store erasure coding, and distributed scrubbing remain outside the bounded period.

---

## Related repositories

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `f4`, `Reed-Solomon`, and Facebook erasure-coding material found no existing dedicated case to reuse. This file therefore keeps only the retention-specific system argument rather than attempting a full coding or datacenter-storage history.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the methodological guardrail: later abstractions such as `repair geometry`, `nested reconstruction`, and `retention relation` are engineering descriptions, not historical Facebook terms.

---

## Sources

### Primary / contemporary

1. Subramanian Muralidhar, Wyatt Lloyd, Sabyasachi Roy, Cory Hill, Ernest Lin, Weiwen Liu, Satadru Pan, Shiva Shankar, Viswanath Sivakumar, Linpeng Tang, and Sanjeev Kumar, **“f4: Facebook’s Warm BLOB Storage System,”** *Proceedings of the 11th USENIX Symposium on Operating Systems Design and Implementation (OSDI ’14)*, Broomfield, Colorado, 6–8 October 2014, pp. 383–398. USENIX open-access PDF: <https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-muralidhar.pdf>.
   - pp. 384–385: immutable BLOB workload; f4 overview; Reed–Solomon `(10,4)` and geo XOR.
   - pp. 388–389: cell design; triple-replicated index files; encoded data; stripe/companion vocabulary; index/location mapping; key-based logical delete.
   - pp. 389–390: direct read, online requested-BLOB reconstruction, backoff nodes, offline full-block rebuilding, rebuilder/coordinator roles.
   - pp. 390–391: geo-XOR layer, rack failure domain, fragment placement, placement-balancer correction, nested failure example.
   - pp. 395–396: related-work boundary; f4 explicitly treats erasure codes as prior tools rather than its coding invention.
2. Irving S. Reed and Gustave Solomon, **“Polynomial Codes Over Certain Finite Fields,”** *Journal of the Society for Industrial and Applied Mathematics* 8, no. 2 (June 1960): 300–304. DOI: `10.1137/0108018`. Used only to control Reed–Solomon priority/genealogy, not to establish f4 implementation semantics.

### Evidence record

See [`../evidence/19-facebook-f4-2014-erasure-coding-grounding.md`](../evidence/19-facebook-f4-2014-erasure-coding-grounding.md).
