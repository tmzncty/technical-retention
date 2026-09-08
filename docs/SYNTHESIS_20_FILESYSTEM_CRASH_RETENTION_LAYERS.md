# Synthesis 20 — Filesystem Crash Retention: Visibility, Crash Admissibility, Durability Closure, Recovery Authority, and Reclamation

## Status and scope

**Bounded engineering synthesis over already-grounded filesystem cases.** This document closes one explicit ROADMAP question:

> How should `returned/visible`, `crash-admissible`, `explicitly durable`, and `reclaimed/converged` be separated in filesystem regimes?

The bounded answer is:

> **A filesystem operation can be visible to a running process before the corresponding state is the crash-surviving state; a crash-surviving filesystem can be structurally admissible without containing the newest visible operation; explicit durability can close only a specified file or namespace relation; surviving recovery evidence can later become replay-inadmissible; and successful recovery can restore service while resource cleanup and reclamation remain unfinished.**

The synthesis is centered on:

- [Case 16 — BSD FFS soft updates](../cases/16-bsd-ffs-soft-updates-crash-admissibility.md), which separates application-visible current state, dependency-constrained crash-admissible stable state, explicit `fsync` closure, and later reclamation;
- [Case 74 — Linux JBD revoke](../cases/74-linux-jbd-revoke-stale-replay-suppression.md), which shows that even a committed surviving redo image can lose recovery authority after block reuse;
- [Case 124 — Linux ext4 replace-by-rename](../cases/124-linux-ext4-rename-fsync-durability-closure.md), which separates pathname visibility atomicity, file durability, containing-directory durability, and lower-layer persistence;
- [Case 125 — Linux ext3/ext4 orphan tracking](../cases/125-linux-ext3-ext4-orphan-crash-cleanup-reclamation.md), which separates namespace detachment, retained post-crash cleanup obligation, journal replay, and final block/inode reclamation.

Historical facts remain in those canonical cases and their evidence records. The decomposition below is **engineering reconstruction**. Cross-case comparisons are **functional analogies** unless explicitly identified as inherited historical record. This synthesis does not claim a soft-updates → JBD → ext4 genealogy, does not define POSIX filesystem semantics in general, and does not treat these four cases as an exhaustive history of crash consistency.

---

## 1. Why one word such as `consistent` is too weak

A common simplified model is:

```text
system call returns
    -> operation happened
    -> filesystem is consistent
    -> data is durable
    -> crash recovery restores it
    -> cleanup is finished
```

The grounded cases break every strong implication in that chain.

Soft updates permits the running in-memory filesystem to be newer than the stable disk image while constraining that stable image to remain safe after a crash. ext4 `rename()` can make one pathname replacement atomic for ordinary observers without thereby making the replacement durable against power loss. `fsync(file)` can close a file's synchronization scope while the containing directory entry remains a separate durability target. JBD can retain a committed positive journal image that later must *not* be replayed because a newer revoke record changes its recovery authority. ext3/ext4 orphan recovery can leave a filesystem usable after journal replay while inode/block cleanup is still outstanding.

The useful question is therefore not simply:

> Is the filesystem consistent?

It is:

> **Which observer sees which state, which failure model is being survived, which retained evidence is authorized to reconstruct current state, and which maintenance obligations are still open?**

---

## 2. Six filesystem-retention relations that must remain distinct

### 2.1 Returned / live-visible state

Question:

> What state may a running caller or pathname observer treat as current after an operation returns?

Case 16 shows that an ordinary filesystem call can return while the final change remains delayed and therefore not permanent. Case 124 adds a namespace-specific form: `rename()` can atomically replace `newpath` for concurrent observers.

This gives a first boundary:

```text
returned / currently visible
    !=
failure-surviving
```

Visibility is observer- and interface-qualified. It says what a live system currently presents, not what a sudden crash is guaranteed to leave behind.

### 2.2 Crash-admissible stable state

Question:

> If volatile state disappears now, is the surviving stable image structurally safe enough to mount, interpret, or reconstruct?

Soft updates makes this relation unusually explicit. The stable disk image may intentionally lag the newest in-memory state, but dependency rules prevent dangerous pointer/allocation combinations from reaching disk. After a crash, the filesystem can be safe for immediate use even though recent operations may be absent and some conservative accounting/reclamation work remains.

Thus:

```text
crash-admissible
    !=
latest visible state durable
```

A crash-admissible state is not necessarily the newest state. It is a state that satisfies the recovery invariants of the bounded mechanism.

### 2.3 Explicit durability closure

Question:

> Which requested object/relation has been forced across the filesystem's durability boundary before the operation returns?

Case 16 treats `fsync` as a stronger closure that can span data, allocation metadata, indirection, inode state, and naming state. Case 124 then prevents the word `fsync` from becoming too coarse: current Linux documentation explicitly says that syncing a file does not necessarily sync the containing directory entry.

For replace-by-rename, a conservative relation can therefore be written:

```text
write replacement payload
    -> fsync(replacement file)
    -> rename(replacement, target)
    -> fsync(parent directory)
```

These steps do not repeat one operation. They close different retention targets.

Hence:

```text
file durability
    !=
namespace-binding durability
```

and:

```text
explicit durability
    !=
one universal whole-filesystem commit
```

The scope must always be named.

### 2.4 Recovery / replay authority

Question:

> Among the stable bytes and recovery records that survived, which are allowed to become current during recovery?

Case 74 adds a relation that the simpler `visible → durable` ladder misses. A positive journal block image can have been committed and can still exist physically, yet a later revoke record can make that older image replay-inadmissible after the same home block has entered a new semantic generation.

Therefore:

```text
surviving committed recovery evidence
    !=
currently authorized recovery evidence
```

Recovery is not merely reading whatever durable bytes remain. It can require retained ordering and negative evidence that determines which surviving history is still admissible.

### 2.5 Post-crash cleanup obligation

Question:

> What work does the recovered filesystem still remember that it must finish?

Case 125 makes this a first-class retained object. An inode may no longer be ordinarily named, yet an on-disk orphan relation preserves the fact that delete or truncate work is unfinished. Journal replay happens first; orphan processing then resumes cleanup.

Thus:

```text
recovery/replay completed
    !=
all cleanup obligations discharged
```

The retained orphan relation is not user payload and not a full operation history. It is future-work metadata: enough state survives to say that a particular maintenance action is still owed.

### 2.6 Reclamation / convergence completion

Question:

> When may blocks, inodes, journal space, or other representations be safely reused or retired?

Cases 16 and 125 both show that ordinary service can resume before all resource accounting/reclamation has converged. Case 125 further shows that pathname disappearance does not authorize immediate block/inode reuse.

Therefore:

```text
logical disappearance
    !=
reclamation eligibility

safe service
    !=
reclamation complete
```

Reclamation is a later authority transition over resources. It is not identical to visibility, durability, or recovery.

---

## 3. A layered crash timeline

The four grounded cases can be composed into a deliberately abstract timeline:

```text
live operation
    ↓
caller-visible / namespace-visible state
    ↓
dependency/order/control work
    ↓
some stable crash-admissible state
    ↓
optional explicit durability closure for named scope
    ↓
crash
    ↓
select admissible recovery evidence
    ↓
replay / reconstruct a serviceable filesystem
    ↓
resume remembered cleanup obligations
    ↓
reclaim resources / retire obsolete recovery state
```

This is an **engineering comparison**, not one historical implementation sequence.

Different systems can skip, merge, or implement these stages differently. Soft updates can preserve crash admissibility without a persistent redo log of the bounded dependency state. JBD uses a persistent journal and negative revoke evidence. ext4 replace-by-rename adds a live namespace atomicity plus explicit file/directory durability distinction. Orphan tracking retains cleanup targets after normal namespace reachability has ended.

The value of the diagram is precisely that it prevents the common vocabulary from hiding those differences.

---

## 4. Counterexample: live atomicity is not failure atomicity

Case 124 gives the simplest counterexample.

Linux `rename()` can ensure that another live process does not observe a moment in which the destination pathname disappears during replacement. That is a strong atomicity property for one live namespace observation.

But:

```text
atomic pathname visibility
    !=
replacement survives power loss
```

The replacement file may still need `fsync(file)`, and the new directory binding may still need `fsync(parent directory)`.

This blocks two shortcuts:

```text
atomic
    !=
durable

same pathname after return
    !=
same pathname binding guaranteed after crash
```

The word `atomic` must therefore be qualified by the observer, operation, and failure model.

---

## 5. Counterexample: crash admissibility is not recency durability

Soft updates is the strongest evidence against a monotonic ladder in which a `consistent filesystem` means the newest state is permanent.

The mechanism deliberately maintains two simultaneous versions of “now”:

```text
newest application-visible in-memory state
    !=
dependency-safe stable image
```

The second can be older yet intentionally correct for the crash contract. If the machine fails, some recent operation can disappear without leaving an unsafe pointer graph.

Therefore the relevant loss classes differ:

```text
recent operation absent after a crash
    !=
filesystem structurally inconsistent after crash
```

A retention account that calls both outcomes simply `data loss` loses the mechanism that made soft updates useful.

---

## 6. Counterexample: durability closure has scope

Case 124 prevents `fsync` from being treated as a magic whole-filesystem durability verb.

A file can be synchronized while the containing directory entry remains outside the completed scope. Conversely, syncing a directory entry is not a claim that arbitrary lower storage layers have fulfilled persistence semantics beyond the contract the filesystem depends on.

The useful decomposition is:

```text
payload/file-object closure
    +
namespace-binding closure
    +
lower-layer persistence contract
```

No term should silently substitute for the others.

This also means that two application protocols can both call `fsync` and still retain different failure relations depending on:

- which file descriptors they synchronize;
- whether they create or replace names;
- which directories are involved;
- what ordering the filesystem supplies;
- what durability contract the block device/controller actually honors.

---

## 7. Counterexample: durable evidence can become unsafe to replay

Case 74 is especially important because it breaks a naive rule that **more durable history is always safer**.

An old metadata image can satisfy all of these statements:

```text
it was journaled
it belonged to a committed transaction
its journal bytes still survive
```

and still fail this statement:

```text
it is authorized to overwrite the current home block during recovery
```

After block reuse, a later revoke record changes the admissibility relation. Recovery must preserve newer state by *refusing* to apply some older committed history.

Hence:

```text
durable history
    !=
eternal recovery authority

more surviving redo bytes
    !=
monotonically safer recovery
```

This is a filesystem-specific instance of a broader repository lesson: physical survival and historical legitimacy are not the same currentness relation.

---

## 8. Counterexample: replay completion is not reclamation completion

Case 125 gives a post-recovery temporal layer that is easy to erase from diagrams.

An unlinked-open inode or multi-transaction truncate can require work after a crash. The journal can be replayed first, producing a crash-admissible metadata state, while an orphan relation still says that delete or truncate work remains.

The sequence is:

```text
journal replay
    -> serviceable recovered state
    -> orphan target qualification
    -> resumed truncate/delete
    -> allocation resources become safely reusable
```

Therefore:

```text
replay complete
    !=
recovery maintenance complete
    !=
resource reclamation complete
```

The 2023 orphan-file power-cut bug adds another guardrail: preserving the target inode number alone is insufficient when the on-disk inode fields used to interpret that target are stale. A retained recovery index and the state it indexes must remain mutually admissible.

---

## 9. Reclamation is not secure forgetting

Cases 16, 74, 124, and 125 are about logical/service/recovery relations, not media sanitization.

When an inode or block becomes reusable, the filesystem has changed allocation authority. It has not thereby established that older physical bytes are unrecoverable from the underlying device.

Thus:

```text
reclaimed / reusable
    !=
physically erased
    !=
cryptographically erased
    !=
forensically unrecoverable
```

Case 44 remains the repository's bounded storage-interface sanitization/deallocation comparison. Filesystem reclamation should not silently inherit that stronger forgetting semantics.

---

## 10. Lower-layer persistence remains a separate contract

Cases 15, 20, and 87 plus [Synthesis 13](SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md) already separate command completion, volatile-cache residence, FUA/Flush scope, persistence-boundary arrival, ordering, and power-fail atomicity.

Filesystem-level reasoning composes with those layers; it does not override them.

A filesystem may correctly order its own metadata and issue the required synchronization requests, yet the end-to-end promise still depends on the storage stack satisfying the assumed lower contract.

Therefore:

```text
filesystem durability protocol correct
    !=
device implementation necessarily compliant

filesystem ordering
    !=
controller/media persistence by definition
```

This synthesis keeps that boundary explicit rather than turning high-level `fsync` into a claim about platter or NAND physics.

---

## 11. The four cases are not one historical genealogy

The selected cases are historically adjacent enough that a synthesis could accidentally become a progress story:

```text
soft updates
    -> journaling
    -> ext4 rename fixes
    -> orphan file
```

That would be unsupported.

The cases answer different bounded questions:

| Case | Main retained relation | What it does not establish |
| --- | --- | --- |
| 16 — BSD FFS soft updates | volatile dependency state constrains crash-admissible stable writeback; `fsync` closes a stronger scope | a JBD/ext3 genealogy or persistent redo design |
| 74 — Linux JBD revoke | negative journal evidence changes replay authority after block reuse | general deletion/tombstone semantics |
| 124 — ext4 replace-by-rename | live namespace atomicity, file durability, and directory durability are separate | one portable rename-durability theorem |
| 125 — ext3/ext4 orphan tracking | crash-persistent target set preserves unfinished cleanup obligations | secure erasure or a complete recovery log |

The shared analytical vocabulary belongs to this repository. It is not evidence that the historical actors used one common theory of `retention layers`.

---

## 12. Failure taxonomy

The synthesis produces a more useful failure vocabulary than `filesystem state was lost`.

### 12.1 Visibility survives only until crash

The live system exposes a state that has not crossed its required durability scope.

### 12.2 Crash-admissibility failure

The stable image violates the filesystem's structural invariants even if many recent bytes are physically present.

### 12.3 Durability-scope failure

A file, directory binding, or other required constituent did not cross the explicit synchronization boundary the application needed.

### 12.4 Recovery-authority failure

Stable evidence exists but replay chooses an obsolete or semantically wrong generation, or lacks the negative/currentness evidence needed to suppress it.

### 12.5 Cleanup-obligation loss

The filesystem recovers a usable state but loses or corrupts the metadata saying that further delete/truncate/reclamation work remains.

### 12.6 Target-state inconsistency

A cleanup target survives but the state needed to interpret the target is stale or contradictory, as in the bounded 2023 ext4 orphan-file failure.

### 12.7 Reclamation failure

The logical object is gone or service is restored, yet blocks/inodes remain allocated and unavailable for reuse.

### 12.8 Lower-layer persistence failure

The filesystem issues the correct operation under its model, but cache/controller/media behavior fails the persistence contract assumed by the higher layer.

These failures can coexist, but they are not synonyms.

---

## 13. What `convergence` means here

The ROADMAP question pairs `reclaimed/converged`, but the cases show that `convergence` needs qualification.

In this bounded filesystem slice, convergence can mean at least:

- disk/stable state has reached a crash-admissible relation;
- explicit file/namespace durability obligations are closed;
- replay has chosen and applied the admissible recovery history;
- orphan/delete/truncate cleanup has finished;
- allocation/accounting state no longer carries conservative leaks;
- obsolete journal or recovery-control state can be retired.

Those frontiers need not coincide.

It is therefore safer to write:

```text
converged with respect to X
```

than to call the whole filesystem simply `converged`.

---

## 14. Philosophical boundary

### I — persistence can be a relation among several differently timed “presents”

The cases expose a technical problem with treating persistence as one object's uninterrupted presence.

At one instant a filesystem can contain:

- a newest live-visible state;
- an older crash-admissible stable state;
- retained evidence authorizing or forbidding future replay;
- unfinished cleanup obligations referring to objects already absent from ordinary naming;
- physical bytes that are no longer current or not yet safely reusable.

The philosophical relevance is modest but real: **technical continuation can depend on coordinating several temporal relations whose “currentness” is qualified by observer, failure contract, recovery authority, and maintenance phase.**

This does not mean `fsync`, journals, or orphan lists are themselves Stieglerian tertiary retention, Heideggerian `Bestand`, or universal models of memory. The mechanism disciplines the interpretation; it does not become a philosophical identity claim.

---

## 15. Prior-art and novelty boundary

Do not claim:

- that these cases define filesystem crash consistency universally;
- that a returned syscall is normally durable unless a source says so;
- that crash-admissible means newest-operation durable;
- that `fsync(file)` automatically closes directory-entry durability;
- that an atomic rename is power-fail atomic;
- that every committed journal image remains forever replay-authorized;
- that recovery completion implies cleanup/reclamation completion;
- that block/inode reuse means old media contents were sanitized;
- that soft updates, JBD revoke, ext4 rename handling, and orphan tracking form a demonstrated historical genealogy;
- that one Linux/BSD mechanism supplies semantics for copy-on-write filesystems, databases, network filesystems, or all POSIX implementations.

The narrower contribution is:

> **Across four grounded filesystem cases, retention after a crash is better modeled as a set of typed relations among live visibility, crash-admissible stable state, explicit durability scope, recovery-evidence authority, remembered cleanup obligations, and reclamation completion. A stronger state on one axis does not automatically close the others.**

This is an engineering synthesis over primary-grounded cases, not a new invention-priority claim.

---

## 16. Related repositories and remaining work

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `soft updates fsync rename orphan revoke crash consistency` found no dedicated synthesis to reuse during this slice.

The division of labor remains:

- `technical-retention`: the typed relation among visibility, crash admissibility, durability, replay authority, cleanup obligation, and reclamation;
- `computing-archaeology`: broader filesystem engineering genealogy, including journaling/WAL, copy-on-write/checkpoint filesystems, ext2/ext3/ext4 history, FFS lineage, barriers, and device-stack evolution if developed;
- future experiments: fault-injection matrices belong in a dedicated experimental slice or companion project rather than being inferred from source text.

Still open after this synthesis:

- copy-on-write/checkpoint filesystem crash semantics;
- cross-filesystem `fsync` / rename comparison;
- ext4 fast-commit evolution;
- multi-directory rename durability;
- lost/corrupt orphan metadata and recovery-index fault injection;
- database WAL and transaction durability composition;
- end-to-end filesystem → block layer → controller → media fault validation;
- complete historical genealogy of crash-consistency mechanisms.

The broad ROADMAP item **file-system crash consistency** therefore remains intentionally unchecked. This document closes only the bounded relation-decomposition question.
