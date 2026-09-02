# Evidence — BSD FFS Soft Updates, 1999–2000

## Promotion target

This record supports promotion of [`cases/16-bsd-ffs-soft-updates-crash-admissibility.md`](../cases/16-bsd-ffs-soft-updates-crash-admissibility.md) directly to **`grounded`** for one bounded claim:

> In the 1999–2000 production-quality 4.4BSD FFS soft-updates regime, the newest application-visible metadata may remain volatile while the filesystem constrains each stable-storage write to preserve crash-safe metadata invariants; immediate post-crash usability therefore does not imply durability of the newest operation, and explicit `fsync` requires a larger payload-plus-metadata persistence closure.

The record does **not** ground generic journaling history, all BSD versions, modern Linux/POSIX `fsync`, hardware write barriers, drive-cache semantics, or invention priority.

---

## Source 1 — Ganger et al., ACM TOCS 2000

**Citation:** Gregory R. Ganger, Marshall Kirk McKusick, Craig A. N. Soules, and Yale N. Patt, “Soft Updates: A Solution to the Metadata Update Problem in File Systems,” _ACM Transactions on Computer Systems_ 18(2), May 2000, pp. 127–153.

- Author-hosted abstract: <https://users.ece.cmu.edu/~ganger/papers/softupdates_abs.html>
- Author-hosted PDF: <https://users.ece.cmu.edu/~ganger/papers/softupdates.pdf>
- Evidence class: **H/P** — contemporary peer-reviewed technical article by the mechanism’s authors, describing the research lineage and its 4.4BSD production implementation.
- Inspection status: full text inspected; page-preserving PDF text and selected rendered pages were inspected during research. Exact claims below are tied to printed-page locations.

### Anchor A — crash model and admissible stable state

**Printed p. 128 / PDF p. 2, Introduction.**

The article states that crashes such as power failures and OS failures normally discard volatile main-memory state. It then requires nonvolatile disk information to remain consistent enough to deterministically reconstruct a coherent filesystem, naming forbidden conditions such as dangling pointers to uninitialized space, ambiguous resource ownership, and live unreferenced resources.

**Supports:**

- H/P: the historical problem is metadata integrity across unpredictable crashes, not merely raw-sector survival;
- E: the bounded retention target after a crash is a coherent/admissible filesystem state, which may differ from the newest pre-crash state.

### Anchor B — current in-memory state versus dependency-safe disk state

**Printed pp. 128 and 133–134 / PDF pp. 2 and 7–8, Introduction and §3.1.**

Soft updates tracks dependencies among in-memory cached metadata and enforces them during writeback. Dependency information is kept at fine field/pointer granularity. If a metadata block is selected for write while some contained changes still depend on earlier writes, those changes are temporarily rolled back in the disk-bound image and restored in memory after I/O completes.

The article explicitly distinguishes what applications see from what disk sees: applications continue to use the newest in-memory metadata while disk receives versions consistent with its already-stable contents.

**Supports:**

- `application-visible current state ≠ crash-admissible stable state`;
- `write-back occurrence ≠ permission for every current field to become stable`;
- `consistency can be produced by selective withholding/rollback rather than only by synchronous whole-operation persistence`.

### Anchor C — three metadata update rules

**Printed pp. 129–130 / PDF pp. 3–4, §2.**

The authors reduce the metadata-ordering problem to three constraints: a reference must not become stable before its target is initialized; a resource must not be reused while older stable references can still name it; and the last stable reference to a live object must not disappear before the replacement reference is established.

**Supports:**

- crash consistency as a relation among several retained metadata objects;
- write ordering as retention machinery;
- a file/object can depend on preservation of reference and allocation relations, not payload alone.

### Anchor D — immediate safe mount with residual inconsistencies

**Printed p. 138 / PDF p. 12, §3.3.**

The production soft-updates design protects enough dependencies that the on-disk metadata is safe for immediate use after a non-media-corruption failure. The same section allows minor residual inconsistencies: unused blocks may remain absent from free maps, unreferenced inodes may remain allocated, and link counts may be too high. Those resources/counts can be reclaimed or corrected later, including by background `fsck`.

**Supports:**

- `safe mountability ≠ perfect accounting convergence`;
- `crash admissibility ≠ reclamation complete`;
- maintenance can continue after service resumes.

### Anchor E — ordinary call return versus permanence

**Printed pp. 138–139 / PDF pp. 12–13, §3.4.**

The article explicitly says that synchronous sequencing of dependent metadata writes does not imply synchronous filesystem semantics. A system call can return while its final update remains delayed, so the change is not necessarily permanent. The authors preserve the conventional write-back vulnerability window for recent information.

**Supports:**

- `crash consistency ≠ latest-operation durability`;
- `visible/returned ≠ durable` in this bounded filesystem regime.

### Anchor F — `fsync` is a relational persistence closure

**Printed pp. 139–140 / PDF pp. 13–14, §3.5, “The fsync System Call.”**

For this implementation, `fsync` requests complete commitment of the specified file to stable storage before returning. The required work extends beyond dirty data blocks: allocation bitmaps, data blocks, indirect blocks, the inode, and unwritten directory entries/naming paths can all have to reach stable storage. The writes can be queued efficiently, but all required writes must complete before the call returns.

**Supports:**

- `fsync durability ≠ payload-block completion`;
- the durable file is a relation among content, allocation, indirection, inode, and naming state;
- higher-layer durability scope cannot be inferred from a lower-layer media-flush event alone.

### Anchor G — prior art and mechanism boundary

**Printed pp. 130–132 / PDF pp. 4–6, §2.1–2.2.**

The authors explicitly discuss established alternatives including synchronous metadata writes, NVRAM, write-ahead logging, shadow paging, scheduler-enforced ordering, and interbuffer dependency approaches.

**Supports:**

- X: `soft updates invented crash consistency` is unsupported;
- X: `soft updates is the only mechanism for metadata integrity` is unsupported;
- the valid historical claim is bounded to this dependency-tracking/writeback mechanism.

---

## Source 2 — McKusick and Ganger, USENIX 1999

**Citation:** Marshall Kirk McKusick and Gregory R. Ganger, “Soft Updates: A Technique for Eliminating Most Synchronous Writes in the Fast Filesystem,” FREENIX track, 1999 USENIX Annual Technical Conference, June 1999, pp. 1–17.

- USENIX institutional record: <https://www.usenix.org/conference/1999-usenix-annual-technical-conference/soft-updates-technique-eliminating-most>
- Evidence class: **H/P** — contemporary implementation paper by the production-integration authors, institutionally archived by USENIX.
- Inspection status: USENIX landing page and extracted paper text inspected. A fresh page-image render of the 1999 PDF was unreliable in this slice; no claim depends on unverified visual interpretation of a figure.

### Anchor H — production integration and no-separate-log mechanism

The abstract says soft updates tracks and enforces metadata dependencies so the disk image remains consistent, avoiding a separate recovery log and most synchronous writes. It explicitly describes incorporation into the 4.4BSD fast filesystem and the work required to turn the prototype into production-quality code.

**Supports:**

- H/P: 4.4BSD FFS is a named production implementation context, not a generic later textbook example;
- H/P/E: dependency enforcement can preserve a crash-usable disk image without a persistent write-ahead recovery log;
- X: `no journal = no crash-consistency machinery` is false in this bounded regime.

### Anchor I — bounded residual inconsistency and later reclamation

The abstract describes the remaining inconsistency class as unclaimed blocks/inodes and says the system can be brought up immediately while a background task later reclaims them.

**Supports:**

- independent contemporary corroboration of the `safe service ≠ reclamation complete` boundary.

### Anchor J — production `fsync` complication

The production paper explicitly treats `fsync` as one of the non-focal operations that required additional design/code, and its implementation discussion requires the state associated with a file to be committed before return rather than merely writing one payload block.

**Supports:**

- the `fsync` closure is part of the production mechanism, not an interpretation invented from the 2000 retrospective alone.

---

## Related-repository reuse check

A GitHub search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) using `soft updates`, `FFS crash consistency`, and `fsync` terms did not locate an existing dedicated technical-history case. No technical narrative was copied from that repository.

If a later computing-archaeology slice builds a general history of FFS, journaling, or filesystem crash recovery, this case should remain focused on the retention-specific distinction among:

```text
application-visible current state
        ↓
crash-admissible stable state
        ↓
explicitly durable fsync closure
        ↓
post-crash reclamation / convergence
```

---

## Cross-case controls

### Case 15 — SSD power-loss durability

Case 15 establishes a device-level `volatile write cache → nonvolatile media` completion boundary and power-loss emergency transfer. Case 16 adds a higher-layer ordering problem: **even if each individual write really becomes nonvolatile, the filesystem can still be unsafe if dependent writes become durable in the wrong relation**.

Therefore:

- device flush completion ≠ filesystem crash consistency;
- filesystem `fsync` scope ≠ one device-cache flush claim;
- the two layers must be composed, not substituted for one another.

### Case 08 — Model 85 cache

Case 08 uses a derivative fast copy whose validity/currentness is controlled relative to authoritative main storage. Case 16 instead permits the application-visible in-memory metadata to be newer than a deliberately dependency-safe stable image. Similarity in “fast copy versus backing state” does not make the historical consistency semantics identical.

### Case 05 — RADOS

RADOS already separates replicated acknowledgement, protocol currentness, and later durable commit. Case 16 shows that comparable **functional** distinctions can arise without distributed replicas: returned/visible, crash-admissible, and explicit durability can diverge inside one filesystem. This is analogy, not genealogy.

---

## Rejected overclaims

- **X:** every operation visible to an application is durable once soft updates is enabled.
- **X:** immediately mountable after crash means no residual inconsistency or cleanup remains.
- **X:** soft-updates dependency state is a persistent journal.
- **X:** file payload reaching disk alone satisfies the bounded FFS `fsync` relation.
- **X:** filesystem stable-storage wording proves the behavior of every lower-level drive cache/controller.
- **X:** the 1999–2000 BSD implementation defines universal modern `fsync` semantics.
- **X:** McKusick/Ganger invented crash consistency, stable storage, or ordered filesystem updates.

---

## Promotion decision

**Promote Case 16 to `grounded`.**

The central mechanism no longer depends on secondary reconstruction: contemporary authors directly document the crash model, dependency invariants, fine-grained in-memory tracking, rollback/roll-forward writeback, immediate safe post-crash use, residual resource leaks, ordinary-return-versus-permanence distinction, and the production `fsync` closure. The remaining open topics are different regimes, not missing prerequisites for this bounded claim.