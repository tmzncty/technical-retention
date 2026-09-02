# Case 19 Grounding Record — Facebook f4 Distributed Erasure Coding, 2014

## Promotion target

Promote [`../cases/19-facebook-f4-erasure-coded-failure-domains.md`](../cases/19-facebook-f4-erasure-coded-failure-domains.md) directly to **`grounded`** for a bounded claim:

> In the 2014 f4 design, distributed coded retention depends not only on Reed–Solomon/XOR algebra but also on retained index/location mappings, fragment placement across physical failure domains, separate online and background reconstruction paths, and maintenance that can restore placement geometry after reconstruction or replacement.

This record does **not** promote a general history of erasure coding, Facebook storage, mutable distributed consistency, or modern f4 descendants.

---

## Evidence classes

### P1 — Muralidhar et al., OSDI 2014 full paper

**Source:** Subramanian Muralidhar et al., “f4: Facebook’s Warm BLOB Storage System,” *11th USENIX Symposium on Operating Systems Design and Implementation (OSDI ’14)*, pp. 383–398.

**Stable source:** <https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-muralidhar.pdf>

**Inspection status:** direct full-text inspection plus direct visual inspection of the relevant facsimile pages. The PDF is 17 pages including the USENIX cover sheet. Printed conference pages 388, 389, and 390 were inspected; printed p. 388 visibly contains §5.1–§5.3 and Figure 7, p. 389 visibly contains Figure 8 plus the normal/failure read and backoff-node account, and p. 390 visibly contains rebuilder/coordinator, geo-XOR, and failure-domain placement text.

### P2 — Reed & Solomon, 1960

**Source:** Irving S. Reed and Gustave Solomon, “Polynomial Codes Over Certain Finite Fields,” *Journal of the Society for Industrial and Applied Mathematics* 8(2), June 1960, pp. 300–304. DOI `10.1137/0108018`.

**Inspection status:** bibliographic/publisher-level source inspected. It is used only as an external priority anchor that Reed–Solomon coding predates f4 by decades. No f4 implementation claim depends on this paper.

### R1 — related-repository duplication check

A GitHub code search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for f4 / Facebook / Reed–Solomon erasure-coding material returned no dedicated existing treatment to reuse. The new case therefore adds a retention-specific distributed-system bridge rather than duplicating an already-developed technical history.

---

## Claim ledger

| Claim | Type | Evidence | Status / boundary |
| --- | --- | --- | --- |
| Facebook BLOBs in the bounded system are immutable, created once/read many, and may be deleted | H/P | Muralidhar 2014 pp. 384–385 | directly sourced; not generalized to all Facebook data |
| f4 stores warm BLOBs in cells using distributed erasure coding | H/P | Muralidhar 2014 pp. 384–385, §5 | directly sourced |
| recent f4 cells use Reed–Solomon with `n=10`, `k=4` | H/P | Muralidhar 2014 p. 388 | scoped to “recent f4 cells” in source; not made universal across versions |
| the cell’s index files use triple replication while actual BLOB data is encoded | H/P | Muralidhar 2014 p. 388 | directly sourced; blocks `f4 = one redundancy method` simplification |
| a name node retains block/parity → storage-node mapping and storage nodes retain BLOB → file/offset/length plus location maps | H/P | Muralidhar 2014 p. 389 | directly sourced; specific ownership system partly out of paper scope |
| a normal read uses the target data block directly | H/P | Muralidhar 2014 p. 389 | directly sourced |
| an unavailable block can be decoded from any `n` surviving companion/parity blocks | H/P | Muralidhar 2014 p. 389 | directly sourced for bounded RS organization |
| a BLOB-sized subrange can be decoded from equivalent subranges of `n` surviving blocks | H/P | Muralidhar 2014 p. 389 | directly sourced and central to online-reconstruction distinction |
| backoff nodes reconstruct only the requested BLOB after a normal read fails | H/P | Muralidhar 2014 pp. 389–390 | directly sourced |
| full missing blocks are reconstructed offline by rebuilder nodes | H/P | Muralidhar 2014 p. 390 | directly sourced |
| rebuild work is heavyweight and throttled; coordinators schedule repairs to reduce data-loss likelihood | H/P | Muralidhar 2014 p. 390 | directly sourced |
| stripe fragments are intended to occupy different racks/nodes | H/P | Muralidhar 2014 pp. 390–391 | directly sourced; source calls placement best-effort |
| placement violations can arise after failure/reconstruction/replacement and are corrected by placement balancing | H/P | Muralidhar 2014 p. 390 | directly sourced |
| geo-level XOR combines equivalent blocks from two datacenters and stores XOR in a third | H/P | Muralidhar 2014 p. 390 | directly sourced |
| geo recovery can invoke lower-level cell/backoff recovery for an unavailable XOR/buddy input | H/P | Muralidhar 2014 pp. 390–391 | directly sourced from read path and compound-failure example |
| deleting an external per-BLOB encryption key renders the BLOB unreadable/logically deleted | H/P | Muralidhar 2014 pp. 388–389 | source-supported service semantic; does not prove fragment erasure or universal secure deletion |
| f4 does not claim invention of erasure coding | H/P/X-control | Muralidhar 2014 Related Work, pp. 395–396 | paper explicitly says erasure codes are tools and f4 does not innovate in that area |
| Reed–Solomon coding predates f4 | H/P | Reed & Solomon 1960 publisher record; f4 ref. 46 | used only for historical-priority boundary |
| erasure-code algebra ≠ failure-domain independence | E | code relation + explicit rack-placement/balancer evidence | engineering reconstruction, not period phrase |
| successful requested-object reconstruction ≠ full block repaired | E | backoff vs rebuilder split | directly compelled by system behavior |
| full content repair ≠ restored placement geometry | E | rebuild/replacement can create placement violation + balancer | engineering reconstruction from explicit maintenance sequence |
| distributed erasure coding ≠ replication with smaller copies | E/A | RS decoding relation plus separately triple-replicated index | functional comparison, not a historical actor phrase |
| reconstruction can be compositional across protection layers | E | geo backoff + lower-level backoff path | supported by paper’s compound-failure path; project phrase `nested reconstruction` is modern |
| redundancy policy can be state-class-specific | E | encoded data + replicated index + geo XOR | direct system design supports reconstruction |
| fragment survival ≠ service readability | E | external-key delete path | bounded to logical/service readability; physical erasure not claimed |

---

## Direct source anchors

### Immutable BLOB workload and system scale

Muralidhar 2014 printed pp. 384–385:

- BLOBs are immutable binary data;
- they are created once, read many times, never modified, sometimes deleted;
- the paper reports f4 storing more than 65 PB logical data;
- f4 uses distributed erasure coding in cells and describes resilience across disk, machine, rack, and datacenter failures.

### Cell coding and state classes

Printed p. 388, §5.2–5.3:

- a cell stores locked volumes;
- distributed erasure coding trades increased rebuild/recovery time and lower maximum read throughput for lower storage overhead;
- recent cells use `n=10`, `k=4`;
- index files remain triple replicated because coding them is not worth the extra complexity;
- data files use Reed–Solomon encoding;
- geo protection uses a separate XOR coding scheme.

This page was directly visually inspected.

### Mapping and sub-object reconstruction

Printed p. 389:

- companion/parity-block vocabulary;
- direct normal read from a data block;
- any `n` companions/parity blocks can recover an unavailable block;
- a BLOB-sized subset can be decoded using only equivalent subsets;
- name nodes maintain data/parity-block → storage-node mappings;
- storage nodes keep BLOB → file/offset/length and volume location-map state;
- backoff nodes reconstruct requested BLOBs after normal reads fail.

This page was directly visually inspected.

### Online reconstruction versus background repair

Printed pp. 389–390:

- backoff nodes fetch equal-length ranges at equivalent offsets and decode once `n` inputs arrive;
- online reconstruction rebuilds **only the requested BLOB**, not the full block;
- full block rebuilding is offline and assigned to rebuilder nodes;
- rebuilder nodes probe for failure, report to coordinators, decode whole blocks, and throttle heavyweight I/O/network work;
- coordinator nodes schedule repairs.

### Placement is separate maintenance state

Printed p. 390 and p. 391:

- racks are treated as the largest single-cell failure domain;
- f4 attempts to place every stripe data/parity block on a different rack and at least a different node;
- initial placement is best effort;
- failure, reconstruction, and replacement can produce placement violations;
- placement balancer work detects and corrects those violations.

This is the central source anchor for rejecting `code parameters alone = fault-domain independence`.

### Geo XOR and compositional recovery

Printed pp. 390–391:

- geo-XOR uses volumes/blocks in two datacenters plus their XOR in a third;
- geo reads retrieve the relevant XOR and buddy ranges;
- those ordinary inputs themselves travel through normal single-cell read or backoff paths;
- the compound-failure example layers datacenter, rack, host, and disk failures around one BLOB.

### Prior-art boundary

Printed pp. 395–396, Related Work:

- f4 places itself after a long erasure-code lineage;
- it cites Reed–Solomon and multiple earlier erasure-coded storage systems;
- it explicitly says it uses erasure codes as tools and does not innovate in coding theory.

The Reed–Solomon publisher record independently fixes the canonical paper at June 1960, vol. 8(2), pp. 300–304.

---

## Why `grounded` is justified

The bounded case satisfies the repository’s `grounded` requirements:

1. **strong primary evidence:** one detailed period system paper by the system’s builders, with production scale and explicit architecture/failure semantics;
2. **precise source locations:** printed pages and named subsections recorded above;
3. **historical vocabulary:** f4’s own terms are preserved instead of replacing them with later object-store/EC terminology;
4. **mechanism:** coding, mapping, placement, normal/failure read, sub-object decode, full rebuild, geo recovery, and placement repair are all separated;
5. **failure modes:** disk/host/rack/datacenter, fragment unavailability, placement violation, reduced redundancy, and nested reconstruction are bounded by the source;
6. **counterexamples / limits:** triple-replicated index files and the paper’s own coding-priority disclaimer block overgeneralization;
7. **related-repository check:** no dedicated `computing-archaeology` f4/RS case was found.

The case does **not** need a second implementation paper merely to reach `grounded`, because its central claims are specific statements about the documented 2014 f4 design and are all supported by the builders’ detailed production paper. Future independent failure-study or source-code archaeology could deepen it toward `mature` but is not required for the bounded mechanism claim.

---

## Residual evidence gaps

These are deliberately **not** promotion blockers:

- the volume-to-storage-node assignment system is described as outside the paper’s scope;
- exact production code/configuration and revision history were not inspected;
- later f4 architecture changes are outside the 2014 boundary;
- the paper’s production evaluation does not independently prove every advertised failure guarantee under every correlated fault;
- no attempt was made to reconstruct Reed–Solomon mathematics from the 1960 paper;
- modern Local Reconstruction Codes, cross-cluster EC, mutable coded-object consistency, and distributed scrub protocols remain separate cases;
- key deletion is not promoted to a general secure-erasure claim.

---

## Cross-case consequence

Case 17 established that parity-coded reconstructability differs from complete replication and that degraded service can precede restored redundancy. Case 19 adds three distributed-system obligations that are not visible if the comparison stops at a disk-array code equation:

1. **failure-domain placement is an independent retained relation**;
2. **requested-object availability can be restored before the missing coded block is rebuilt**;
3. **content reconstruction and placement-geometry repair can complete at different times**.

It also supplies a concrete nested-reconstruction case in which a datacenter-level XOR recovery can depend on local Reed–Solomon reconstruction of one of its own inputs.
