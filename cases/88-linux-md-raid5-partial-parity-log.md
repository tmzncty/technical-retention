# Linux MD RAID5 Partial Parity Log: Retaining Just Enough Recovery Evidence Before a Non-Atomic Stripe Update

## Scope

- **Bounded mechanism:** Linux MD RAID5 Partial Parity Log (PPL) as merged for Linux 4.12 in 2017.
- **Primary implementation anchor:** Artur Paszkiewicz, commit `3418d036c81dcb604b7c7c71b209d5890a8418aa`, `raid5-ppl: Partial Parity Log write logging implementation`, committed 16 March 2017 and merged for Linux 4.12.
- **Primary integration witness:** Shaohua Li, `[GIT PULL] MD update for 4.12`, 1 May 2017, describing PPL as a feature found in Intel IMSM arrays and as another way to close the RAID5 write hole.
- **Prior-art boundary:** earlier RAID parity/currentness work already exists in Case 17; 1993 parity-logging research and 1995-filed Digital Equipment Corporation write-hole recovery work predate Linux PPL.
- **Research question:** what must be retained before a parity-stripe update begins when the data/parity writes cannot be assumed to become durable atomically?

This case is deliberately **not** a general history of RAID5, Linux MD, parity logging, Intel Matrix Storage Manager, storage journaling, or hardware RAID. Case 17 already establishes encoded reconstructability, degraded service, repair margin, and parity-currentness metadata in the 1977–1994 RAID literature. Case 88 asks a later and narrower question:

> **Can the system preserve the ability to reconstruct a parity-consistent pre-update stripe without retaining a complete copy of every in-flight write?**

For Linux MD PPL, the answer is yes under the mechanism's stated failure assumptions. The log retains a **partial parity relation plus bounded write-location metadata** before dispatching the ordinary data and parity writes. That retained evidence is intentionally weaker than a full write journal and therefore provides a narrower guarantee.

---

## Historical vocabulary

The Linux 4.12 patch/documentation uses:

- `Partial Parity Log` / `PPL`;
- `RAID5 Write Hole`;
- `dirty shutdown`;
- `partial parity`;
- `recovery`;
- `distributed log`;
- `metadata area`;
- `parity disk`;
- `full stripe write`;
- `write-back cache`;
- `consistency-policy=ppl`.

The following are **project engineering terms**, not historical Linux vocabulary:

- `recovery-sufficient evidence`;
- `parity-currentness witness`;
- `pre-update recoverability closure`;
- `reconstruction authority`;
- `retained relation budget`.

Do not substitute those project terms for the source vocabulary when describing the historical implementation.

---

## Historical record

### H/P — the write hole is a relation failure, not necessarily immediate loss of every payload block

The PPL documentation added in commit `3418d036...` defines the bounded failure: after a dirty shutdown, parity for a stripe may be inconsistent with the data on the other member disks. If the array is also degraded, the missing contribution prevents ordinary parity recalculation; using inconsistent parity can then produce silent corruption during degraded reads or rebuild.

This sharpens Case 17's earlier parity-currentness result. The problem is not simply that a disk sector vanished. Individually readable sectors can survive while the **cross-member redundancy relation is no longer trustworthy**.

**Primary anchor:** Linux commit `3418d036...`, added `Documentation/md/raid5-ppl.txt`.

### H/P — PPL records partial parity before ordinary data/parity writes are dispatched

The original PPL documentation states that, for a write request, PPL writes partial parity **before** the new data and parity are dispatched to the RAID members.

The implementation commit defines partial parity as the XOR of stripe data chunks not modified by the write. It gives separate calculation paths for reconstruct-write and read-modify-write cases and requires the calculation to occur while the old data needed for that relation are still available.

The source therefore establishes an ordering requirement:

```text
old/current stripe relation available
        ↓
calculate + persist PPL evidence
        ↓
ordinary data/parity stripe writes may proceed
```

The PPL record is not an after-the-fact diagnostic. It is retained **before** exposing the stripe to the non-atomic update interval that creates the write-hole risk.

**Primary anchors:** Linux commit `3418d036...`, commit message and added `raid5-ppl.c` / PPL documentation.

### H/P — the retained evidence is deliberately smaller than a full data journal

The Linux documentation says partial parity is “just enough data” to recover from the write hole. XORing the retained partial parity with the modified chunks can reconstruct a parity value consistent with the stripe's pre-write state, regardless of which member writes completed before interruption.

The implementation's on-disk structure reinforces that boundedness. A PPL area contains a header plus partial-parity data; entries identify affected stripe ranges, parity-disk identity, sizes, and checksums. Full-stripe writes do not need stored partial parity; their entries can merely mark stripes whose parity should be recalculated after an unclean shutdown.

So the mechanism does **not** retain a second complete user-data history for every request. It retains a smaller relation chosen to make one specific future recovery operation possible.

**Primary anchor:** Linux commit `3418d036...`, `Documentation/md/raid5-ppl.txt` and `drivers/md/raid5-ppl.c`.

### H/P — PPL is distributed across member metadata areas rather than placed on one dedicated journal device

The 2017 documentation calls PPL a `distributed log`. The log for a given write is stored in the metadata area of the parity drive for the corresponding stripe; it therefore does not require a dedicated journaling device.

Shaohua Li's Linux 4.12 pull request describes the feature as found in Intel IMSM RAID arrays and states that the Linux implementation is also available to ordinary RAID5 arrays when the relevant superblock bit is set.

This grounds the Linux historical claim without claiming that Linux or Intel invented parity logging or write-hole recovery.

**Primary anchors:** Linux commit `3418d036...`; Shaohua Li, `[GIT PULL] MD update for 4.12`, 1 May 2017.

### H/P — PPL recovery does not equal preservation of the interrupted write

The original documentation is explicit that PPL is **not a true journal**. It protects against silent corruption from parity inconsistency but does not protect the in-flight data itself from loss.

If a dirty disk containing part of the written region is lost, PPL recovery is not performed for that stripe and arbitrary data may remain in the written portion. The documentation explicitly says this behavior is then the same as plain RAID5.

That limitation is central to the case:

> **preserving redundancy consistency ≠ preserving the newest interrupted payload**.

PPL can retain enough state to stop stale/inconsistent parity from silently corrupting an otherwise untouched missing contribution while still declining to promise application-level atomic durability for the interrupted write.

### H/P — the original 2017 implementation exposed a lower-layer cache dependency

The PPL commit warns that volatile write-back cache on RAID member disks should be disabled because, at that point, the implementation could not guarantee consistency on power failure if the supposedly preceding PPL write remained volatile or was reordered below the member disks' caches.

This is a direct cross-layer retention boundary. A software log that is logically ordered “before” later writes does not close a power-failure window unless the lower storage layer actually preserves that order/durability relation.

Later Linux source evolved additional flush/FUA handling; this case does not retroactively attribute those later details to the initial Linux 4.12 implementation.

**Primary anchor:** Linux commit `3418d036...`, commit message and added PPL documentation.

### H/P — Linux 4.12 did not invent write-hole protection or parity logging

Earlier evidence blocks any first-invention claim:

- Stodolsky, Holland, and Gibson's 1993 work explicitly presents `parity logging` for redundant disk arrays, primarily as a solution to the small-write performance problem.
- Digital Equipment Corporation's `Enhanced raid write hole protection and recovery`, filed 13 October 1995 and issued as US5774643A in 1998, explicitly uses non-volatile write-back cache plus metadata to identify interrupted RAID5 writes and restore parity consistency after a crash.
- Case 17 already grounds Chen et al.'s 1993–1994 discussion of parity sectors becoming inconsistent during crash-interrupted writes and the need for retained meta state about consistency.

These are **prior-art witnesses**, not evidence that Linux PPL directly descends from any one of them. The defensible Linux-specific historical claim is the 2017 composition of MD RAID5, distributed member-local PPL metadata, partial-parity logging, and the documented recovery policy.

---

## Retained state

Case 88 requires at least six distinct state classes.

### 1. Current user-data chunks

The ordinary RAID5 payload contributions. PPL does not duplicate all of them as a general transaction journal.

### 2. Ordinary parity chunk

The normal RAID5 redundancy contribution. During a torn/non-atomic update it may remain physically present while becoming inconsistent with the surviving data chunks.

### 3. Partial-parity recovery evidence

The XOR relation over the unmodified data contributions needed to reconstruct a parity-consistent pre-update relation after interruption.

### 4. PPL header / affected-stripe metadata

The log must identify which stripe range and parity disk the evidence concerns, plus sizes/generation/checksum information sufficient to validate and interpret the record.

### 5. Durability/order state at lower layers

The guarantee depends on the PPL write crossing an appropriate persistence/order boundary before later data/parity writes can make the stripe ambiguous. The initial implementation's warning about member-drive volatile write-back caches makes this dependency historically explicit.

### 6. Array membership/currentness relation

PPL only has meaning relative to the RAID membership and parity placement relation that identifies how the stripe is reconstructed. This is constitutive control state, not another user-data copy.

---

## Retention mechanism

### Before the vulnerable update

The controller derives partial parity while the required old/current values are still available and forms a checked PPL record describing the affected write.

### Persistence before dispatch

The log record is written before normal member data/parity writes are released. That ordering is what preserves a recovery path across the interval in which some member writes may complete and others may not.

### Crash/dirty-start recovery

After an unclean shutdown, the retained PPL entry can be used to restore a parity relation consistent with the pre-write stripe under the documented recoverable cases. When all disks are present, PPL recovery can eliminate the need for a full resync; in the relevant degraded case, the partial parity can protect reconstruction of an unmodified missing contribution.

### Retirement

PPL entries are not a permanent historical archive. They are temporary recovery infrastructure associated with in-flight/unclean stripe state and become unnecessary once the corresponding update/recovery relation has safely closed.

---

## Read / write / recovery semantics

### Ordinary read

PPL does not change the fundamental fact that RAID5 can normally read data directly from surviving data chunks and reconstruct a missing contribution from parity plus the other members.

### Write

A partial-stripe update creates a temporary multi-device atomicity problem: new data and matching new parity cannot be assumed to reach all independent members as one indivisible physical event.

PPL addresses that problem by retaining an auxiliary relation **before** releasing the ordinary writes.

### Recovery

Recovery asks a narrower question than “what was the newest requested user value?” It asks whether enough verified evidence remains to re-establish a parity relation that will not silently reconstruct unrelated data incorrectly.

That is why the same mechanism can close the write hole without being a full write journal.

---

## Failure and forgetting modes

Keep these failure modes separate:

- dirty shutdown after only part of a stripe update reaches member media;
- physically surviving but parity-inconsistent stripe state;
- subsequent/degraded member loss that makes ordinary recomputation impossible;
- corrupt or uninterpretable PPL header/partial-parity evidence;
- PPL evidence that was logically issued first but remained in a volatile lower-layer cache;
- loss of a dirty member whose in-flight payload PPL does not promise to reconstruct;
- loss/corruption of RAID membership or metadata needed to interpret the stripe relation;
- ordinary retirement/reuse of PPL records after recovery closure.

Do not collapse these into `RAID lost power` or `journal saved the write`. The bounded implementation protects one consistency relation under stated assumptions.

---

## Engineering reconstruction

### E — parity bytes ≠ parity currentness

A parity block can physically survive while no longer corresponding to the current combination of data chunks. Reconstruction authority therefore depends on relation-qualified state, not mere media presence.

### E — recovery-sufficient evidence ≠ complete in-flight payload copy

PPL demonstrates that a system can retain **less than the whole write** while still preserving one future recovery capability. The retained target is a mathematical/metadata relation chosen for the fault model.

### E — closing the write hole ≠ making the interrupted user write atomic

PPL protects parity consistency / reconstruction correctness under its documented cases. It explicitly does not guarantee preservation of all in-flight user data.

### E — write ordering at one layer ≠ durable ordering through the stack

The 2017 volatile-write-cache warning shows that software sequencing is insufficient if a lower layer can acknowledge/reorder/cache the supposedly durable precursor state. Case 87 provides a historically earlier interface vocabulary for this distinction; the comparison is functional, not a direct genealogy claim.

### E — temporary recovery metadata can be constitutive without becoming long-term history

PPL records have value because an update is not yet safely closed. Once the update/recovery relation is complete, retaining those records forever is unnecessary. Successful retention can therefore include deliberate later forgetting of recovery evidence.

### E — redundancy consistency ≠ redundancy margin

PPL can restore a trustworthy parity relation, but that does not by itself replace a failed member or restore a consumed failure margin. Case 17's degraded-repair distinction remains separate.

---

## Functional analogies

### A — PPL and a write-ahead log

Both can retain precursor recovery state before riskier updates proceed. But Linux's own documentation says PPL is **not a true journal** and does not protect all in-flight data. The analogy is therefore limited to `retained-before-update recovery evidence`.

### A — PPL and JBD revoke / ZooKeeper snapshot recovery

Cases 74 and 71 also retain auxiliary state that controls later recovery interpretation. Their objects and semantics are different: JBD revoke suppresses stale replay; ZooKeeper combines fuzzy snapshots with ordered replay; PPL reconstructs a parity-consistency relation. No genealogy is implied.

### A — PPL and SCSI/NVMe durability controls

Cases 87 and 20 distinguish command completion, volatile caching, media commitment, and ordering. PPL depends on an analogous lower-layer closure, but it is an array-level consistency mechanism, not a block-interface FUA/Flush command.

---

## Philosophical interpretation

### I — retention can preserve a relation rather than a duplicate object

PPL is a useful counterexample to an object-only picture of memory. What must survive the interruption is not necessarily another complete copy of the user's newest data. A compact relation can be sufficient to make a later reconstruction admissible.

### I — forgetting can be part of successful retention

The PPL record is valuable precisely while the update's outcome is unresolved. Once consistency has been re-established, the old recovery evidence can be retired. The mechanism therefore couples retention and forgetting through a completion condition rather than treating maximum indefinite accumulation as the goal.

These are project interpretations, not claims that Linux developers used philosophical `retention` terminology.

---

## Counterexamples and limits

- PPL does not make RAID5 writes universally atomic.
- PPL does not guarantee the newest interrupted application write survives.
- PPL does not repair a failed disk or restore full redundancy margin by itself.
- PPL does not make checksums, filesystems, databases, or application transaction protocols unnecessary.
- The 2017 patch does not prove Linux invented parity logging, RAID journaling, write-hole protection, or Intel IMSM's earlier PPL design.
- The 2017 implementation's volatile-cache warning means its power-failure guarantee depended on lower-layer cache policy; later Linux code must not be silently projected backward.
- This case does not establish a complete Intel IMSM PPL genealogy or exact earliest implementation date. Shaohua Li's 2017 pull request is evidence that the feature was found in Intel IMSM arrays, not a complete history of that lineage.
- `partial parity` here is a RAID5 recovery relation, not a generic synonym for erasure-code parity fragments.

---

## Cross-case comparison

### Case 17 — RAID parity reconstruction

Case 17 asks how a missing member remains reconstructable and why degraded service differs from repaired redundancy. Case 88 asks how **an interrupted write can poison the parity relation before any member has necessarily failed**, and how a small retained log can keep later reconstruction trustworthy.

### Case 74 — Linux JBD revoke

Both retain negative/auxiliary recovery state whose significance appears after interruption. JBD revoke changes whether an older journal image may be replayed to a reused block; PPL preserves enough relation to rebuild parity consistently. Function only, not historical identity.

### Case 87 — SCSI cache durability

Case 87 shows that command completion can occur before physical-medium residency and that volatile/non-volatile cache/medium are separate retention classes. Case 88's initial volatile-cache warning demonstrates the same cross-layer problem from the array side: a logically preceding recovery record is useless after power loss if it never crossed the necessary lower persistence boundary.

### Cases 20 / 31 / 32 — NVMe and persistence domains

These later/other layers help compare `issued`, `completed`, `durable`, and `ordered`, but their terminology must not be imported into the 2017 MD historical record. PPL is not itself a persistence-domain specification.

---

## Related repositories

### `tmzncty/computing-archaeology`

Search before this case did not reveal an existing RAID/PPL history in the companion repository. A future full history of RAID5 small-write algorithms, controller architecture, parity logging, Intel IMSM, and Linux MD evolution belongs there. This case should remain the retention-specific slice and link outward rather than grow into that broader genealogy.

### `tmzncty/problem-history`

Useful methodological warning: `write hole`, `parity logging`, and `Partial Parity Log` are historically situated terms. The project should not rewrite 1993 parity-logging research or 1995 controller patents as though they were already solving Linux 4.12's exact implementation problem in Linux's later vocabulary.

---

## Claim ledger

| Claim | Type | Status |
| --- | --- | --- |
| Linux 4.12 PPL writes partial parity before ordinary RAID data/parity writes | H/P | grounded |
| PPL is stored on RAID member metadata areas and described as a distributed log | H/P | grounded |
| PPL can close the RAID5 write hole without protecting all in-flight user data | H/P | grounded |
| initial 2017 PPL warns against volatile member write-back caches for power-failure consistency | H/P | grounded |
| Linux 4.12 pull request says PPL was found in Intel IMSM arrays | H/P | grounded, bounded wording only |
| Linux invented parity logging / write-hole protection | X | rejected by 1993 research and 1995-filed prior art |
| PPL is a full write-ahead journal | X | explicitly rejected by Linux documentation |
| PPL guarantees application-write atomicity | X | rejected |
| parity presence implies parity currentness | X | rejected |
| software-before ordering implies power-fail durability through volatile lower caches | X | rejected |
| compact recovery evidence can preserve a later admissible relation without duplicating the complete payload | E | supported engineering reconstruction |
| successful closure can make temporary recovery evidence disposable | E/I | supported project interpretation |

---

## Sources

### Primary / contemporary

- Artur Paszkiewicz, **`raid5-ppl: Partial Parity Log write logging implementation`**, Linux commit `3418d036c81dcb604b7c7c71b209d5890a8418aa`, 2017-03-09/16: <https://github.com/torvalds/linux/commit/3418d036c81dcb604b7c7c71b209d5890a8418aa>
- Linux kernel, **Partial Parity Log** documentation (current descendant of the text introduced in the above commit): <https://docs.kernel.org/driver-api/md/raid5-ppl.html>
- Shaohua Li, **[GIT PULL] MD update for 4.12**, 1 May 2017: <https://lkml.iu.edu/hypermail/linux/kernel/1705.0/00532.html>
- Artur Paszkiewicz, **[PATCH v4 0/7] Partial Parity Log for MD RAID 5**, 21 February 2017: <https://lwn.net/Articles/715280/>
- Digital Equipment Corporation, Clark E. Lubbers, Susan G. Elkington, Ronald H. McLean, **Enhanced raid write hole protection and recovery**, US5774643A, filed 13 October 1995, issued 30 June 1998.

### Scholarly / institutional prior art

- Daniel Stodolsky, Mark Holland, Garth A. Gibson, **“Parity Logging: Overcoming the Small Write Problem in Redundant Disk Arrays,”** ISCA 1993, pp. 64–75: <https://www.cs.cmu.edu/afs/cs/project/nectar-io/ftp/ParityLogging/ISCA93.abstract>
- Peter M. Chen et al., **“RAID: High-Performance, Reliable Secondary Storage,”** UCB/CSD-93-778 / _ACM Computing Surveys_ 26(2), 1994 — already grounded in Case 17.

---

## Maturity

**`grounded`** for the bounded 2017 Linux MD PPL mechanism and its principal retention distinction:

> **a parity-protected system can retain a compact, temporary relation before a non-atomic update so that later recovery remains trustworthy, while still not promising that the interrupted newest payload itself survives.**

A full Intel IMSM lineage, cross-vendor controller history, exact parity-logging genealogy, modern PPL cache-flush evolution, and hardware fault-injection validation remain separate work.