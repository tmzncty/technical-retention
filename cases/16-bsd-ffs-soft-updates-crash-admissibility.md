# BSD FFS Soft Updates: Crash Admissibility Through Dependency-Preserving Writeback

## Scope

- **Bounded period:** 1999–2000 production-quality soft updates in the 4.4BSD Fast File System (FFS).
- **Primary implementation witness:** Marshall Kirk McKusick and Gregory R. Ganger, **“Soft Updates: A Technique for Eliminating Most Synchronous Writes in the Fast Filesystem,”** FREENIX track, 1999 USENIX Annual Technical Conference, June 1999, pp. 1–17.
- **Primary expanded mechanism witness:** Gregory R. Ganger, Marshall Kirk McKusick, Craig A. N. Soules, and Yale N. Patt, **“Soft Updates: A Solution to the Metadata Update Problem in File Systems,”** _ACM Transactions on Computer Systems_ 18(2), May 2000, pp. 127–153.
- **Research question:** when a filesystem keeps its newest metadata in volatile memory, what exactly must be retained on stable storage so that an unexpected crash still leaves a usable filesystem, and how does that relation differ from making the newest operation durable?

This is **not** a history of filesystem crash consistency in general. It does not claim to cover journaling, log replay, copy-on-write/checkpoint filesystems, modern Linux `fsync` semantics, database transactions, disk-cache ordering, barriers/FUA, or NVMe persistence domains. Case 15 already establishes a lower device-level boundary between volatile cache and nonvolatile media. This case begins one layer higher:

> **A filesystem may intentionally let its current in-memory state run ahead of stable storage while continuously constraining the stable image to remain crash-admissible.**

The bounded mechanism is 4.4BSD FFS soft updates: track metadata dependencies in memory, enforce them as dirty blocks are written back, and temporarily roll back still-dependent pointer/field updates in the disk-bound image while leaving the application-visible in-memory state current.

---

## Historical vocabulary

The period sources themselves use terms including:

- `soft updates`;
- `metadata`;
- `stable storage`;
- `nonvolatile storage`;
- `write-back caching`;
- `delayed writes`;
- `update dependency`;
- `dependency information`;
- `per-pointer` / per-field dependency tracking;
- `roll-back` / `rolled-back` and `roll-forward`;
- `fsck`;
- `fsync`;
- `inode`;
- `directory entry`;
- `free space map` / bitmap;
- `indirect block`;
- `unclaimed blocks` and `unclaimed inodes`.

The following are **project engineering terms**, not claims about the authors’ historical vocabulary:

- `crash-admissible state`;
- `stable-state frontier`;
- `persistence closure`;
- `dependency-preserving writeback`;
- `application-visible currentness / crash-admissible stable-state split`.

These terms summarize relations made explicit by the period mechanism. They must not be used to imply that McKusick, Ganger, Soules, or Patt formulated a general philosophy of retention in those terms.

---

## Historical record

### H/P — crashes destroy volatile state, so the disk image must remain reconstructible as a coherent filesystem

Ganger et al. 2000 begin from an explicit failure boundary: power interruptions or operating-system failures ordinarily destroy volatile main-memory state. The nonvolatile disk image therefore has to remain consistent enough that a coherent filesystem can be deterministically reconstructed. The article names concrete forbidden states: pointers to uninitialized space, ambiguous ownership through multiple pointers, and live resources with no pointer.

This gives the case a more precise retention target than “all recent writes survive”:

```text
newest in-memory filesystem state
        may be lost

but

surviving stable-storage state
        must remain coherent enough for safe reconstruction/use
```

**Primary anchor:** Ganger et al. 2000, printed p. 128 / PDF p. 2, Introduction.

### H/P — soft updates tracks dependencies in volatile cached metadata and enforces them only when dirty blocks reach stable storage

The 2000 article describes soft updates as fine-grained sequencing for write-back cached metadata. Dependencies are maintained with dirty in-memory metadata; when a dirty block is flushed, the dependency information is consulted. Dependencies are tracked at field/pointer granularity rather than only at block granularity.

If a dirty block contains updates whose prerequisites have not yet reached stable storage, those still-dependent changes are temporarily undone in the disk-bound version. The write proceeds with a version safe relative to the current disk image; after the write finishes, the current in-memory version is restored. Applications therefore continue to see the newest metadata while disk writes are constrained to states consistent with what is already stable.

**Primary anchors:** Ganger et al. 2000, printed pp. 128 and 133–134 / PDF pp. 2 and 7–8, Introduction and §3.1.

### H/P — the required ordering is expressed as metadata invariants, not as a requirement to synchronously persist every operation

For a new file, the initialized inode has to reach stable storage before a directory entry is allowed to point to it. Ganger et al. reduce the general metadata-ordering problem to three rules:

1. do not create an on-disk pointer to a structure before that structure is initialized;
2. do not reuse a resource before previous pointers to it are removed;
3. do not remove the last existing pointer to a live resource before its replacement pointer has become established.

The key historical mechanism is therefore **ordered admissibility among related metadata updates**, not universal synchronous persistence.

**Primary anchor:** Ganger et al. 2000, printed pp. 129–130 / PDF pp. 3–4, §2.

### H/P — safe immediate mount after a crash can coexist with bounded residual inconsistencies

The 2000 article states that the enhanced soft-updates FFS protects enough update dependencies that on-disk metadata can be safely used immediately after a system failure other than media corruption. It simultaneously identifies residual states that may remain: unused blocks absent from free maps, unreferenced inodes absent from the free-inode map, and link counts that are too high. These can be reclaimed or corrected later, including by background `fsck`.

So the source itself distinguishes:

```text
safe for immediate filesystem use
        ≠
all accounting/reclamation work already complete
```

This matters for retention because “a coherent current service can continue” is weaker than “every derived accounting relation has already converged.”

**Primary anchor:** Ganger et al. 2000, printed p. 138 / PDF p. 12, §3.3.

### H/P — return from an ordinary filesystem call does not generally mean the newest change is permanent

The article explicitly warns that synchronous sequencing of some metadata does not imply synchronous filesystem semantics. For common updates, when a filesystem call returns, the final change may still be delayed and therefore not permanent. The authors discuss a normal vulnerability window for recent information under UNIX-derived write-back strategies.

This directly blocks an easy but false equation:

> **crash consistency = all application-visible operations are already durable.**

Soft updates is instead designed to preserve filesystem structural integrity while still allowing delayed persistence of recent operations.

**Primary anchor:** Ganger et al. 2000, printed pp. 138–139 / PDF pp. 12–13, §3.4.

### H/P — `fsync` requests a stronger per-file stable-storage relation whose closure crosses data and metadata

The production 4.4BSD discussion treats `fsync` as a distinct operation: a requested file must be completely committed to stable storage before the call returns. The work is not limited to dirty payload blocks. It can require allocation bitmaps, file data blocks, indirect blocks, the inode, and unwritten directory entries/naming paths that make the file reachable.

The implementation can queue groups of writes efficiently rather than serialize every one, but it must wait for all required writes to finish before the `fsync` completes.

This is a particularly useful retention boundary:

```text
file payload on disk
        ≠
file durably constituted as the requested filesystem object
```

The current file is a relation among payload, allocation, indirection, inode, and naming metadata.

**Primary anchor:** Ganger et al. 2000, printed pp. 139–140 / PDF pp. 13–14, §3.5, “The fsync System Call.”

### H/P — the 1999 production paper independently grounds the mechanism in 4.4BSD FFS and its no-log boundary

McKusick and Ganger 1999 describe the production-quality incorporation into the 4.4BSD Fast File System. Their abstract explicitly contrasts soft updates with synchronous ordering and write-ahead logging: metadata dependencies are tracked and enforced so that the disk image remains consistent, without requiring a separate recovery log or most synchronous metadata writes. They also state that the bounded residual inconsistencies are unclaimed blocks/inodes and that normal service can resume immediately, with reclamation later.

This is important prior-art control. The 1999 paper does **not** establish that soft updates invented crash consistency, update ordering, or stable-storage semantics. Its own framing names synchronous writes and write-ahead logging as established alternative approaches.

**Primary/institutional anchor:** McKusick and Ganger 1999, USENIX FREENIX paper, especially abstract, §§1–3, and the `fsync` implementation discussion.

---

## Retained state

This case requires several distinct targets.

### 1. Application-visible current metadata

The in-memory metadata image can contain the newest directory entries, pointers, allocation state, and inode changes visible to running applications.

### 2. Crash-admissible stable metadata

The disk image may lag behind that newest state, but soft updates constrains what combinations are allowed to become stable. This is the state that must survive loss of volatile memory without containing dangerous dependency violations.

### 3. User payload

File data blocks may be dirty or already stable. Their physical persistence alone does not establish that the current file object is durably named, allocated, and reachable.

### 4. Dependency-control state

Soft updates maintains in-memory dependency structures describing which metadata changes are safe to expose to disk. They are constitutive of pre-crash writeback behavior but are not, in this bounded design, a separate persistent recovery log that must itself survive the crash.

### 5. Free-space and reference/accounting state

Some accounting state can legally lag after a crash: resources may remain allocated but unclaimed, or link counts may be conservatively high. These conditions can require later reclamation without making the mounted filesystem structurally unsafe.

---

## Physical / logical substrate

The bounded retention relation is layered:

```text
application-visible filesystem operations
        ↓
current metadata + payload in volatile memory/cache
        ↓
volatile dependency structures
        ↓
writeback selects / constructs a dependency-safe block version
        ↓
stable disk image
        ↓
post-crash mount and reconstruction
```

This is different from Case 15’s device-internal volatile-cache → nonvolatile-media handoff. Case 15 asks whether a lower-layer write has crossed the device’s durability boundary. Case 16 asks **which higher-level combinations of writes are safe to have crossed that boundary at any given crash point**.

---

## Retention mechanism

### Dependency tracking

Before or while metadata is changed in memory, soft updates records the dependencies required for a safe stable-storage order.

### Safe writeback through temporary rollback

A dirty metadata block is not simply copied byte-for-byte to disk whenever the cache chooses to flush it. Still-dependent fields can be temporarily rolled back to an earlier safe value in the write image. Once the physical write finishes, the current in-memory values are restored for applications.

This creates a deliberate split:

```text
current in-memory version
        ≠
currently admissible disk version
```

Both are intentional states of the same filesystem at the same moment.

### Deferred resource release

For deallocation, resources are not made reusable until old on-disk pointers have safely been nullified. Thus an operation can be logically requested and visible before the corresponding capacity becomes safely reusable.

### Explicit durability closure through `fsync`

When the caller asks for the stronger `fsync` relation, the implementation has to drive the relevant dependency closure to stable storage: bitmaps, data, indirect blocks, inode, and relevant naming metadata.

### Post-crash reclamation

After a crash, remaining resource leaks/accounting overestimates can be repaired later without blocking immediate safe use. Retention of serviceability and completion of reclamation are separate maintenance phases.

---

## Addressing and access geometry

Unlike a physical memory case, the important “address” here is a graph of filesystem references:

- directory names point to inodes;
- inodes and indirect blocks point to data blocks;
- allocation maps constrain ownership and reuse;
- link counts summarize reference relations.

A block can physically survive on disk while ceasing to be a safely reachable part of the current filesystem relation, or a newly written payload block can exist before the metadata chain making it part of the durably reachable file has been completed.

The filesystem object’s recoverability is therefore **relational and graph-structured**, not reducible to one stable sector address.

---

## Read semantics

Ordinary reads are not the main bounded mechanism. The important recovery read is after a crash:

- can the surviving on-disk metadata be traversed without unsafe dangling ownership/reference states?
- can allocation and reference relations be interpreted safely enough to resume service?
- if some resources are unclaimed, can they be identified as cleanup work rather than mistaken as live current content?

Thus “readable sectors” are necessary but not sufficient for “usable filesystem state.”

---

## Write and durability semantics

### Ordinary metadata mutation

The caller may see a new current in-memory state before every dependency needed to make that exact state permanent has reached disk.

### Background writeback

Dirty blocks may be written in flexible order because the system can expose a dependency-safe version to disk, even if that disk version temporarily lags the in-memory version.

### `fsync`

A caller can request a stronger boundary where the file and required constitutive metadata are committed to stable storage before return.

### Crash

A crash destroys volatile current/dependency state. The bounded goal is not to replay the entire volatile history but to ensure that whatever stable prefix/composition remains is structurally admissible.

---

## Time

This case adds several timescales to the comparison:

- application operation return time;
- write-back cache residence time;
- dependency lifetime;
- asynchronous disk-write completion time;
- `fsync` closure/completion time;
- crash instant, which can cut across any of the above;
- post-crash mount/reconstruction time;
- later background reclamation time.

A key temporal lesson is that **one filesystem can intentionally maintain two different “nows”**:

- the newest application-visible in-memory state;
- an older or partially advanced but dependency-safe stable-storage state.

The latter is not merely stale by accident; its admissibility is engineered.

---

## Maintenance and labor

The apparently simple promise that “the filesystem is still usable after a crash” depends on substantial hidden work:

- dependency creation and retirement;
- per-field/pointer bookkeeping;
- rollback/roll-forward of disk-bound metadata versions;
- ordering of allocation and pointer transitions;
- dirty-block writeback;
- explicit `fsync` closure across several metadata classes;
- mount-time recomputation of some counts;
- later reclamation of unclaimed blocks/inodes;
- implementation/debugging of dependency cases for each filesystem operation.

The 1999 production paper is especially useful here because it records that moving from the research idea into production FFS required rethinking non-focal operations such as `fsck` and `fsync` and correcting detailed dependency cases. Crash admissibility is therefore not an abstract property conferred by one label; it is sustained by an implementation that must enumerate and enforce the relevant relations.

---

## Failure / forgetting modes

Distinct failures include:

- a dependency not being recorded for an update that actually needs ordering;
- a dependent pointer reaching stable storage before its prerequisite structure is initialized;
- a resource being reused while an old stable pointer can still refer to it;
- the last old reference being removed before the new reference is stable;
- a crash before a recent operation becomes permanent, causing that recent operation to disappear while the filesystem remains coherent;
- incomplete `fsync` closure, where payload survives but allocation/indirection/inode/name state does not satisfy the promised durable file relation;
- media corruption, explicitly outside the ordinary soft-updates crash guarantee;
- accumulated unclaimed resources reducing capacity until reclamation occurs.

A crash that loses a recent file creation while leaving a safe pre-creation state is therefore different from a crash that leaves an inconsistent pointer graph. Both involve “something did not persist,” but they violate different retention targets.

---

## Engineering reconstruction

### E — application-visible currentness ≠ crash-admissible stable currentness

Soft updates deliberately permits the latest in-memory state to outrun disk. The disk receives only combinations that are safe relative to what is already stable. “Current” must therefore be qualified by observer and failure contract.

### E — crash consistency ≠ latest-operation durability

The filesystem can remain safe to mount immediately after a crash even though some recent operations never became permanent. Structural admissibility and recency durability are different retention claims.

### E — dependency-control metadata ≠ necessarily persistent recovery metadata

The soft-updates dependency structures guide pre-crash ordering and rollback, yet the bounded design does not require a separate write-ahead recovery log to survive the crash. A system can use volatile control state to shape what becomes persistent so that the persistent image is self-admissible afterward.

### E — `fsync` defines relational durability closure

Durability of “the file” can require more than the file’s data sectors. Allocation state, indirect blocks, inode state, and directory names can be constitutive of the durable object the caller expects to recover.

### E — crash admissibility ≠ complete resource reclamation

The on-disk image can be safe to use with conservatively leaked resources that are reclaimed later. Service continuity and accounting convergence need not occur at the same time.

### E — lower-layer stable media ≠ higher-layer crash consistency

Case 15 gives a device-level transition to nonvolatile media. Case 16 shows that even if individual writes truly reach stable media, the filesystem still has to control **which dependent writes may become durable first**. A device durability guarantee cannot substitute for filesystem invariants.

---

## Functional analogies

### A — comparison with Case 15 SSD power-loss durability

Case 15 separates volatile device staging from nonvolatile media and gives `FLUSH CACHE` an explicit completion boundary. Case 16 operates above that boundary: it determines the dependency closure and ordering among filesystem writes that must be made stable for a particular durability or crash-admissibility promise.

The analogy is functional only. `fsync` in 4.4BSD FFS and ATA `FLUSH CACHE` are not historically identical commands and one source set does not prove the complete lower-layer stack semantics of the other.

### A — comparison with Case 08 cache currentness

Both cases separate a current volatile/fast state from a slower backing state. But Model 85 cache residency is a derivative-copy service optimization with an authoritative main-storage value, whereas soft updates can deliberately let stable filesystem metadata encode an older/safe relational state while the application-visible metadata has advanced. The cache analogy therefore stops before treating the two as one consistency problem.

### A — comparison with Case 05 RADOS

RADOS already forces the project to separate acknowledgement, currentness, and durable commit across replicas. Soft updates adds a non-distributed counterexample: even on one filesystem image, application visibility, structural crash admissibility, and explicit durability can be distinct relations.

### A — comparison with write-ahead logging

The period authors themselves discuss logging as an alternative. The useful comparison is that both are mechanisms for controlling crash-recoverable metadata state, while their retained recovery structures differ. This case does not claim that soft updates is “better than journaling” in general or that every logging filesystem has one universal commit/replay semantics.

---

## Philosophical interpretation

### I — technical retention can target an admissible relation rather than the newest trace

This case is a strong counterexample to any simple philosophy in which retention means “the latest produced state remains materially present.” After a crash, the intended surviving target can be a **coherent, admissible filesystem relation** that is older than what users had most recently observed.

What matters is not maximal survival of every recent trace but survival of a state that can still count as a valid filesystem world: references resolve safely, ownership is unambiguous, and service can resume.

### I — forgetting and recovery are layer-relative

The most recent file creation can be forgotten while the filesystem remains intact. An unclaimed block can persist physically while no longer participating in a live file. A link count can be conservatively wrong while the reference graph is still safe enough for service. These are different forms of loss and remainder.

### I — continuity may be produced by refusing some new state permission to become stable yet

Soft updates makes a useful conceptual reversal: retention is not only “preserve what has been written.” Sometimes persistence requires **withholding** a new pointer or allocation relation from stable storage until prerequisite states have crossed the durability boundary. A future state is delayed so that the surviving past remains admissible.

This is an interpretation of the mechanism, not period actor vocabulary and not a claim about all filesystems.

---

## Counterexamples and limits

### X — soft updates does not mean every returned operation is durable

The source explicitly rejects this. Recent changes can remain in the normal write-back vulnerability window unless a stronger persistence operation is requested.

### X — safe immediate mount does not mean the disk image is perfectly reconciled

Unclaimed blocks/inodes and conservative link counts can remain and be repaired later.

### X — dependency tracking does not mean the dependency structures themselves are a durable transaction log

The bounded design uses in-memory dependency state to constrain writes. Do not silently rename that machinery a journal.

### X — `fsync` here is not a universal modern filesystem contract

This case records the 1999–2000 4.4BSD FFS soft-updates implementation described by its authors. Different filesystems and later standards can define directory durability, rename semantics, device flush ordering, and persistence domains differently.

### X — stable-storage wording in the filesystem paper does not independently prove a particular disk drive’s volatile-cache behavior

The paper reasons at the filesystem/storage interface. Case 15 separately shows why device-level volatile caches and flush contracts are another evidence layer. This case does not retroactively prove which exact lower-layer hardware configuration was used in every 4.4BSD deployment.

### X — no invention-priority claim

The authors explicitly discuss synchronous sequencing, NVRAM, write-ahead logging, shadow paging, and scheduler-enforced ordering as prior/alternative mechanisms. This case grounds **the bounded soft-updates mechanism**, not a claim that its authors invented crash consistency or ordered metadata persistence.

---

## Sources

### Primary / contemporary

1. Gregory R. Ganger, Marshall Kirk McKusick, Craig A. N. Soules, and Yale N. Patt, **“Soft Updates: A Solution to the Metadata Update Problem in File Systems,”** _ACM Transactions on Computer Systems_ 18(2), May 2000, pp. 127–153. Author-hosted page and PDF: <https://users.ece.cmu.edu/~ganger/papers/softupdates_abs.html> and <https://users.ece.cmu.edu/~ganger/papers/softupdates.pdf>. Directly inspected for the mechanism and the printed-page anchors used above.
2. Marshall Kirk McKusick and Gregory R. Ganger, **“Soft Updates: A Technique for Eliminating Most Synchronous Writes in the Fast Filesystem,”** FREENIX track, 1999 USENIX Annual Technical Conference, June 1999, pp. 1–17. USENIX record: <https://www.usenix.org/conference/1999-usenix-annual-technical-conference/soft-updates-technique-eliminating-most>. The institutional landing page and extracted paper text were inspected; fresh page-image rendering of this 1999 PDF was not reliable in this research slice, so no unverified figure/page-image claim depends on it.

### Related-repository check

A repository search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for soft updates / FFS crash-consistency / `fsync` terms did not find an existing dedicated case. This file therefore keeps only the retention-specific argument rather than duplicating a known historical treatment.

---

## Evidence status

**Grounded** for the bounded 1999–2000 4.4BSD FFS soft-updates mechanism.

The promotion is justified because the primary sources directly establish:

- the crash model and coherent-on-disk-state requirement;
- per-field/pointer dependency tracking;
- temporary rollback/roll-forward during writeback;
- concrete ordering invariants;
- immediate post-crash mountability with bounded residual inconsistencies;
- ordinary-call return versus permanence distinction;
- production `fsync` closure across payload and constitutive metadata;
- explicit prior/alternative mechanisms, blocking an invention-priority shortcut.

Open work is deliberately separate: journaling/log replay, copy-on-write/checkpoint consistency, modern `fsync`/rename contracts, lower-layer cache/barrier semantics, and distributed filesystem crash recovery should be treated as later bounded regimes rather than hidden prerequisites for this case.