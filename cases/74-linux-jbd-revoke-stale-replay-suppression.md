# Linux JBD Journal Revoke Records: Negative Recovery State, Block Reuse, and Stale-Redo Suppression

## Status

**`grounded`** — bounded to the Linux Journal Block Device (JBD) revoke mechanism visible in the `linux-2.5.12` kernel source, with Stephen C. Tweedie's 1998 Linux journaling paper used as the pre-revoke journal/checkpoint baseline and Sivathanu et al. FAST '05 used as independent scholarly analysis of the resulting non-rollback/reuse problem.

Grounding record: [`../evidence/74-linux-jbd-1998-2005-revoke-grounding.md`](../evidence/74-linux-jbd-1998-2005-revoke-grounding.md).

## Scope

This case asks one narrow filesystem-retention question left open by Case 16:

> **How can a filesystem preserve newer state by retaining a recovery record whose meaning is “do not restore this older committed block image”?**

The bounded path is:

```text
T1: metadata block B is journaled and committed
    -> an old positive image of B is now valid redo evidence

later: metadata B is freed
    -> JBD records revoke(B) in a later transaction
    -> the same physical block number can be re-used for ordinary file data
    -> newer data reaches B's home location

crash
    -> recovery scans revoke records and remembers the latest revoke sequence for B
    -> an older journal image of B is still physically present and may belong to a committed transaction
    -> but that older image is not replay-eligible
    -> replay therefore does not roll B back over the newer file data
```

A later transaction can journal B again after the revoke and regain replay eligibility because the prohibition is transaction-sequence-relative rather than permanent.

This is **not**:

- a general history of ext3, JBD/JBD2, journaling, write-ahead logging, log-structured filesystems, databases, or crash consistency;
- a claim that Linux, ext3, or JBD invented journaling, redo recovery, revoke records, negative logging, or block-generation protection;
- a full account of ext3 `data=journal`, `ordered`, or `writeback` mode semantics;
- a reconstruction of every JBD/JBD2 on-disk format revision;
- a claim that revoking a block erases its old bytes, sanitizes the medium, or makes the block unusable forever;
- a claim that a JBD revoke is historically or semantically identical to a Cassandra/Swift/Kafka tombstone;
- a claim that the `linux-2.5.12` source is the first appearance of the mechanism.

The retention-specific contribution is narrower:

> **A committed positive recovery image can remain physically present yet lose recovery authority because a later retained negative record says replay would restore the wrong semantic generation of the reused block.**

`negative recovery evidence`, `replay authority`, `semantic generation`, and `stale-redo suppression` below are project engineering terms, not Linux/JBD period vocabulary.

## Related-repository check

Fresh code searches in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `ext3 JBD journal revoke` and `journaling filesystem` found no dedicated JBD/ext3 revoke case to reuse. Case 74 therefore keeps only the retention/recovery decomposition here.

A later broad Linux-filesystem or journaling history belongs in the companion repository; this case should then link to it rather than duplicate that chronology.

## Historical vocabulary and source boundary

The `linux-2.5.12` JBD source directly uses:

- `revoke` / `revoked blocks`;
- `journal` / `journalled`;
- `transaction ID` / transaction sequence;
- `commit`;
- `recovery` / `replayed`;
- `metadata`;
- `block bitmap`;
- `revoke table`.

The 1998 paper directly uses `journaling`, `log enhanced`, `journal`, `commit record`, `redo`, `checkpointing`, `head`, `tail`, and `sequence number`.

The source does not describe the mechanism using this repository's later vocabulary `negative currentness`, `semantic generation`, `tombstone`, `secure erase`, or `anti-resurrection`. Those are analytical comparisons only when explicitly labeled.

### Primary / contemporary technical sources

Stephen C. Tweedie, **“Journaling the Linux ext2fs Filesystem,”** LinuxExpo '98.

- PDF mirror used for direct inspection: <https://pdos.csail.mit.edu/6.828/2012/readings/journal-design.pdf>

Linux kernel `linux-2.5.12`, `fs/jbd/revoke.c`, file header states `Written by Stephen C. Tweedie ... 2000`:

- <https://kernel.googlesource.com/pub/scm/linux/kernel/git/ralf/linux/+/refs/tags/linux-2.5.12/fs/jbd/revoke.c>

Current Linux kernel JBD2 on-disk documentation is used only as continuity/cross-check evidence for revocation-block semantics, not as a substitute for the period source:

- <https://www.kernel.org/doc/html/latest/filesystems/ext4/journal.html>

### Independent scholarly analysis

Muthian Sivathanu, Andrea C. Arpaci-Dusseau, Remzi H. Arpaci-Dusseau, and Somesh Jha, **“A Logic of File Systems,”** FAST '05, pp. 1–15.

- USENIX record: <https://www.usenix.org/conference/fast-05/logic-file-systems>

## Historical record

### H/P — 1998 Linux journaling already separates commit from checkpoint/home propagation

Tweedie's 1998 LinuxExpo paper describes journaling as a pre-existing class of filesystem design. Updated metadata is first written into a separate journal. A commit record marks a transaction as committed; only after the commit is safely on disk may the new metadata be copied back to its normal home location.

The same paper then makes the post-commit retention obligation explicit. A committed transaction is not immediately disposable: until its metadata buffers have been synchronized to their home locations, the journal copy cannot be deleted/reused because it remains the recovery representation required after a crash.

This supplies the positive baseline for Case 74:

```text
journal image + commit evidence
    -> replay authority exists
    -> checkpoint/home propagation may still be outstanding
    -> old journal space remains needed until that handoff closes
```

**Primary anchors:** Tweedie 1998, printed pp. 3 and 6, sections describing journaling and `Committing and checkpointing the journal`.

### H/P — the period JBD source defines revoke specifically as protection against replaying deleted metadata over newer data

The `linux-2.5.12` `fs/jbd/revoke.c` header states that revoke prevents old log records for deleted metadata from being replayed over newer data using the same blocks.

The comment separates two phases:

1. **commit** writes the current transaction's list of revoked blocks into the journal;
2. **recovery** records the transaction ID of revoked blocks and uses that state to decide which journal entries may be replayed.

This directly establishes that the negative state is itself journaled and later reconstructed into recovery-control state.

**Primary anchor:** `linux-2.5.12/fs/jbd/revoke.c`, lines 16–30 in the inspected Gitiles rendering.

### H/P — revoke is sequence-relative rather than a permanent ban on one physical block number

The same source states that if several revoke records exist for one block, only the latest matters, and a later log entry beyond the last revoke still gets replayed.

The recovery implementation makes the rule explicit: a revoke with transaction sequence `R` suppresses the block in transaction `R` and earlier transactions, while a later transaction with a greater sequence remains replayable.

Therefore the retained negative state does **not** mean:

```text
block B can never again appear in the journal
```

It means, approximately:

```text
for recovery of block B:
    reject positive journal images at/before latest_revoke_sequence(B)
    allow later journal images
```

**Primary anchor:** `revoke.c` header lines 26–30 and recovery comments/code around `journal_set_revoke()` / `journal_test_revoke()`.

### H/P — event order inside one transaction changes the final revoke relation

The source explicitly documents both same-transaction orderings.

If a block is **revoked and then journaled**, the later metadata journaling cancels the revoke because the desired final result is the new journal image.

If a block is **journaled and then revoked**, the revoke takes precedence; the implementation arranges this through the rule that journaling cancels only an already-existing revoke, so a later revoke survives to commit.

Thus `revoke` is not a timeless property attached to a physical block. It is a transaction-ordered recovery relation.

**Primary anchor:** `revoke.c` header lines 32–46.

### H/P — a later ordinary data write does not cancel the prior revoke

The source's next interaction is retention-critical. After a block is revoked, the same block can be written as ordinary data. That data write must **not** cancel the revoke, because an older journal image of metadata can still exist and would overwrite the newer file data during recovery.

This is the core stale-redo hazard:

```text
old journal evidence survives
same block number is reused for a new semantic role/generation
newer data reaches home block
crash recovery replays old metadata without revoke
=> newer data can be overwritten by stale metadata
```

A new physical write at the home address is therefore insufficient to establish recovery safety while older redo evidence remains replay-eligible.

**Primary anchor:** `revoke.c` introductory interaction comments immediately following the journaled/revoked cases.

### H/P — ext3 must establish revoke before freeing the metadata block for reuse

The `journal_revoke()` comment says that after the current transaction commits, the operation prevents the block from being replayed during recovery; later metadata writes in the same transaction can cancel it.

The same comment gives an ext3 ordering constraint: when deleting metadata, ext3 must call revoke **before clearing the block bitmap**.

That ordering is not merely bookkeeping style. Clearing allocation state can make the physical block available for another semantic use; the replay prohibition must therefore be established before reuse becomes possible.

**Primary anchor:** `revoke.c`, `journal_revoke()` comment around lines 256–267.

### H/P — crash recovery materializes a transient latest-revoke table and discards it afterward

The recovery section says it must:

- record all revoke records and the latest transaction ID for each block;
- test whether a block from a given journal transaction has been revoked by that transaction or a later one;
- empty the revoke table after recovery.

The code retains only the latest sequence number per block in the in-memory hash and clears the table once recovery finishes.

This yields two different retained embodiments of the same control relation:

1. durable revoke records in the journal, needed across the crash boundary;
2. a transient recovery-time hash table reconstructed from those records, needed while deciding replay admissibility.

The transient table's safe retirement after recovery does not imply that the historical bytes containing revoke records have been securely erased.

**Primary anchor:** `revoke.c`, recovery support around lines 555–637.

### H/S — independent FAST '05 analysis identifies revoke as a non-rollback mechanism under block type/reuse changes

Sivathanu et al. define a `non-rollback property`: disk contents should not be overwritten by older contents from a previous epoch. Their analysis specifically considers a container/block changing between journaled and non-journaled roles.

They show the danger in which an older journaled epoch is propagated after a later non-journaled epoch has already reached the block. The paper then states that ext3 journal revoke records prevent this by pre-scanning the log and refusing to propagate the corresponding older block image. It separately requires reuse ordering so the freeing transaction is committed before the block changes type.

This is independent scholarly confirmation of the retention relation reconstructed here:

> physical survival and prior commit of an older positive image are not sufficient to make that image admissible after block reuse.

**Scholarly anchor:** Sivathanu et al. 2005, §7.2.1, pp. 8–10.

## Retained state

The bounded mechanism depends on several state classes that must not be collapsed:

1. **home-location block bytes** — the current or stale embodiment at the filesystem's ordinary block address;
2. **positive journal block images** — redo candidates for committed transactions;
3. **transaction commit/sequence state** — identifies the ordered transactions to which journal entries and revokes belong;
4. **revoke records** — block-number negative recovery state retained in the journal;
5. **allocation / block-bitmap state** — participates in whether a former metadata block can be reused;
6. **the block's current semantic role/generation** — metadata versus later ordinary file data is the key reuse boundary in the bounded examples;
7. **checkpoint/home-write progress** — determines when positive journal copies remain needed;
8. **recovery-time revoke hash state** — a transient reconstruction used to decide replay.

Only items 1 and 2 contain the relevant block payload bytes. The remaining state can still determine which bytes are allowed to become current after recovery.

## Retention / recovery mechanism

### Stage 1 — positive redo evidence becomes committed

A transaction writes journal images and reaches its commit boundary. Those images can now be replay authority for restoring the committed filesystem state if home propagation is incomplete.

### Stage 2 — later filesystem evolution can invalidate that replay authority without erasing the older image

The old metadata block is freed. Before reuse can be exposed through allocation state, JBD records a revoke for that physical block number in the later transaction.

The older journal image may remain physically intact and belong to a committed transaction. The new negative record changes whether it counts during future recovery.

### Stage 3 — the home block can enter a new semantic generation

The physical address is reused, for example as ordinary file data. Its newer contents are now semantically unrelated to the old metadata image despite sharing the same block number.

This motivates the project reconstruction:

> **block-number continuity ≠ semantic-generation continuity**.

The phrase `semantic generation` is analytical shorthand for the source's concrete metadata-free/reallocate-as-data case; it is not a JBD field or period term.

### Stage 4 — recovery combines positive and negative journal evidence

Recovery first obtains latest revoke sequence information. When it encounters a journaled image for block `B`, it asks whether a revoke in the same or a later transaction suppresses that image.

An older committed image can therefore survive yet fail the admissibility test.

### Stage 5 — later journal reuse can restore positive replay authority

If `B` is journaled in a transaction later than its latest revoke, the source explicitly allows that later image to replay. The negative state has bounded sequence scope rather than permanent physical-address scope.

## Addressing and reuse geometry

The central hazard exists because the same block number can participate in different semantic lifetimes:

```text
block number B
    at T1: metadata object/generation M1
        -> positive journal image J(M1,B)

    freed in T2
        -> revoke(B,T2)

    after reuse: ordinary file data generation D2
        -> home(B) = D2

    crash recovery:
        J(M1,B) physically exists
        J(M1,B) may be committed
        but revoke(B,T2) makes J(M1,B) ineligible
```

The physical address stayed the same. What changed was the meaning and currentness relation attached to that address.

This differs from mapped Flash or virtual memory, where one higher-level identity may move across physical addresses. Here one **physical address remains fixed while the semantic identity carried by that address changes**.

## Read / write / recovery semantics

### Ordinary read

Case 74 is not about the normal read path. Its key read-like operation is crash recovery examining retained journal/revoke state to decide what may overwrite the home filesystem.

### Journal write / commit

Writing and committing a positive journal image can make it eligible for later redo. It does not make that eligibility immutable under all future filesystem transitions.

### Revoke

Revoke writes negative recovery control state: for the applicable transaction-sequence range, older journal images for the same block number must not be replayed.

It does not erase those images or the home block.

### Checkpoint / home propagation

Checkpointing copies committed journaled state to home locations. Tweedie's 1998 account shows why the corresponding journal copy remains needed until that propagation closes.

Revoke adds a later qualification: a retained older journal image that once served as positive recovery evidence can become actively dangerous after block reuse.

## Time, maintenance, and bounded state

Several timescales coexist:

- transaction ordering/sequence;
- commit completion;
- later free/reuse of a block;
- home-location writeback;
- checkpoint completion and journal-space reuse;
- crash occurrence;
- recovery pre-scan and replay;
- retirement of the transient recovery revoke table.

No one retention interval captures the case. Correctness depends on preserving enough **ordering relation** to know whether old positive evidence is still admissible when recovery eventually occurs.

The system also does not need a complete forever-history of every revoke. The period source keeps the **latest revoke sequence per block** during recovery because that is sufficient for the bounded replay test; later entries beyond that sequence can replay normally.

## Failure / forgetting modes

### Lose or omit the required revoke before reuse

An older committed metadata image can remain replay-eligible after the home block has entered a newer data generation. A later crash/replay can then overwrite the new data with stale metadata.

### Treat commit as unconditional future replay authority

This confuses `was committed` with `is still admissible to restore now` after subsequent block reuse.

### Treat block-number identity as object-generation identity

The same physical block number can host distinct semantic roles over time. Recovery must not infer sameness of current object merely from address equality.

### Ignore same-transaction ordering

The source explicitly gives different results for `revoke -> journal` and `journal -> revoke`. Collapsing both to one unordered state loses the final recovery relation.

### Cancel revoke on an ordinary data write

The source warns against this: the old journal image is precisely what can overwrite the newer non-journaled data after a crash.

### Reuse journal space before checkpoint closes

This is the older 1998 positive-retention failure: discarding the only committed journal representation before home synchronization can destroy the recovery path.

### Treat post-recovery revoke-table deletion as secure forgetting

Clearing the in-memory hash only ends that transient recovery embodiment. It does not prove physical erasure of journal sectors or lower-layer media traces.

## Cross-case comparison

### Case 16 — FFS soft updates

Case 16's bounded FFS regime tries to ensure every stable metadata image is dependency-safe **before** it reaches disk, using primarily volatile dependency structures and carefully ordered writeback. It does not require a persistent redo/revoke journal to make the stable image admissible.

Case 74 permits committed redo history and therefore needs a different safety relation: **some committed retained history must later be excluded from replay after block reuse**.

So:

> **soft-update dependency ordering ≠ journal stale-redo suppression**.

### Cases 28 / 41 / 42 — Swift, Cassandra, Kafka negative state

All four cases show useful negative retained state, but the negative relation differs:

- Swift tombstone: suppress older distributed object replicas until convergence/reclamation;
- Cassandra tombstone: suppress older replicated values while repair/GC grace risks resurrection;
- Kafka compaction tombstone: represent keyed deletion long enough for compacted-log readers to observe it;
- JBD revoke: suppress an older local crash-recovery image after a physical block number has been freed/reused.

The functional analogy is **negative evidence changes later admissibility**. No shared genealogy, protocol, lifetime, or deletion semantics is claimed.

### Case 71 — ZooKeeper fuzzy snapshot/replay

ZooKeeper Case 71 shows that correct recovery may depend on combining a materialized representation with ordered replay history. JBD Case 74 adds a different condition: retaining a committed log image is not enough because later negative state may prohibit replay of that specific physical destination.

### Case 73 — GFS lazy garbage collection

Case 73 shows a physical chunk can survive after namespace/currentness authority is withdrawn. Case 74 similarly shows old journal bytes can survive after recovery authority is withdrawn. The historical mechanisms are unrelated beyond the functional separation between physical survival and admissibility.

## Prior art and chronology boundary

Tweedie's 1998 paper itself prevents a false `Linux invented journaling` narrative. It describes journaling/log-enhanced filesystems as an existing class and says many modern filesystems had already adopted variations of the design.

Sivathanu et al. 2005 likewise cite earlier filesystem/database consistency and logging work while analyzing ext3. This case therefore makes no priority claim for journaling, redo, transaction commit, checkpointing, or negative logging in general.

The strongest bounded historical statement is only:

> **By the `linux-2.5.12` JBD source lineage whose file header dates `revoke.c` to Stephen Tweedie in 2000, Linux JBD had an explicit transaction-sequenced revoke mechanism that journaled block-number prohibitions and reconstructed them during crash recovery to prevent stale metadata replay over newer reused-block data.**

That is an implementation witness, not proof of first invention.

## Philosophical interpretation — deliberately bounded

**I — interpretation, not historical vocabulary:** Case 74 is a particularly clear example in which retaining a state can preserve a **prohibition** rather than a positive value. The future system continues correctly because it can remember not to restore something that is still materially recoverable.

That does **not** justify a universal equation such as `forgetting requires memory`, `every absence is stored`, or `negative state is philosophically equivalent to memory`. The technical claim is narrower: this one recovery protocol preserves newer state by retaining enough negative evidence to disqualify older positive evidence.

## Claim ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| 1998 Linux journaling account separates transaction commit from later checkpoint/home propagation | H/P | Tweedie 1998 pp. 3, 6 | established |
| committed journal representation remains needed until its home copies are synchronized | H/P | Tweedie 1998 checkpoint section | established |
| JBD revoke prevents old deleted-metadata log records from replaying over newer data using the same blocks | H/P | `linux-2.5.12` `fs/jbd/revoke.c` header | established |
| revoke records are written at commit and reconstructed with transaction IDs during recovery | H/P | same source | established |
| latest revoke sequence suppresses that transaction and earlier while later log entries remain replayable | H/P | `journal_set_revoke()` / `journal_test_revoke()` | established |
| same-transaction `revoke -> journal` and `journal -> revoke` have different final precedence | H/P | `revoke.c` header comments | established |
| ordinary data write after revoke does not cancel the revoke because stale log replay remains dangerous | H/P | `revoke.c` interaction comments | established |
| ext3 must revoke deleting metadata before clearing the block bitmap | H/P | `journal_revoke()` comment | established |
| recovery-time revoke hash is cleared after recovery | H/P | recovery support comments/code | established |
| ext3 revoke protects a non-rollback property under block type/reuse changes | H/S | Sivathanu et al. FAST '05 §7.2.1 | established as independent analysis |
| block-number continuity does not imply semantic-generation continuity | E | source-backed reconstruction of metadata-free/reuse-as-data path | supported |
| committed positive evidence can lose replay authority without being erased | E | JBD sequence/revoke semantics | supported |
| JBD revoke is equivalent to Cassandra/Swift/Kafka tombstones | X | no genealogy or semantic identity established | rejected |
| revoke performs secure erase | X | sources do not establish media sanitization | rejected |
| Linux/ext3/JBD invented journaling or revoke mechanisms in general | X | prior art not exhausted; 1998 source treats journaling as existing class | rejected |

## What remains uncertain

1. The exact first historical implementation or invention of a revoke-like recovery record is not established here.
2. The `linux-2.5.12` file is a reproducible period implementation witness whose header dates the file to 2000; it is not claimed to be the first JBD/ext3 tree containing the mechanism.
3. Current JBD2 documentation confirms continuing revocation-block semantics, but this case does not claim byte-for-byte on-disk-format continuity from early JBD to current JBD2.
4. The case does not reconstruct the complete ext3 transaction/checkpoint state machine or data-mode semantics.
5. The case does not experimentally fault-inject a period kernel or measure the exact crash windows.
6. The case does not establish lower-layer disk-cache, write-barrier, FUA, or media-persistence composition.
7. No secure-erasure or forensic-remanence conclusion follows from journal retirement or recovery-table clearing.

## Why this case matters for the repository

Cases 28, 41, 42, and 63 already showed that negative state can keep older positive state from counting at a distributed/object/transaction interface. Case 74 adds a lower-level crash-recovery counterexample:

> **The thing that must survive a crash may be neither the newest payload nor a complete history, but a bounded negative relation that says which surviving committed history must no longer be allowed to act on the current physical address.**

That deepens `technical retention` without reducing every negative record to one universal tombstone mechanism.