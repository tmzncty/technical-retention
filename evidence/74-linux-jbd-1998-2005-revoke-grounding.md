# Case 74 grounding record — Linux JBD revoke and stale-redo suppression, 1998–2005

## Purpose

This record grounds [`../cases/74-linux-jbd-revoke-stale-replay-suppression.md`](../cases/74-linux-jbd-revoke-stale-replay-suppression.md).

The case is intentionally narrow. It does **not** attempt a general history of ext3, JBD/JBD2, filesystem journaling, database WAL, crash consistency, or secure deletion. It asks one retention-specific recovery question:

> How can a system preserve newer state by retaining a negative recovery record that says an older, still-present, previously committed journal image must no longer be replayed to a reused physical block?

The bounded historical witness is Linux JBD as visible in the `linux-2.5.12` source tree. Stephen C. Tweedie's 1998 LinuxExpo paper supplies the positive journal/commit/checkpoint baseline; Sivathanu et al. FAST '05 supplies independent scholarly analysis of the non-rollback hazard produced when blocks change semantic role or are reused.

## Evidence status

**Grounded.** The central mechanism is supported by:

1. period primary Linux journaling literature;
2. period implementation source for JBD revoke semantics;
3. later official JBD2 documentation used only as continuity/cross-check evidence;
4. independent scholarly analysis of ext3's revoke/non-rollback relation.

No invention-priority claim is made for journaling, redo, revoke-like records, negative logging, or generation protection.

## Source register

### P1 — Tweedie 1998 Linux journaling paper

Stephen C. Tweedie, **“Journaling the Linux ext2fs Filesystem,”** LinuxExpo 1998.

Inspected PDF mirror:

<https://pdos.csail.mit.edu/6.828/2012/readings/journal-design.pdf>

Central anchors:

- printed p. 3: journaling / log-enhanced filesystems are treated as an existing class; metadata updates are first written into a separate journal; a commit record marks the atomic transaction; after commit is safely on disk, metadata may be propagated to home locations;
- printed p. 6, `Committing and checkpointing the journal`: committed buffers remain pinned to the transaction until synchronized to home locations; only after the last buffer is unpinned may the transaction's journal blocks be reused.

Use in Case 74: positive baseline for the distinction among **commit**, **replay authority**, **checkpoint/home propagation**, and **journal-space retirement**.

### P2 — Linux `linux-2.5.12` JBD `revoke.c`

Primary implementation witness:

<https://kernel.googlesource.com/pub/scm/linux/kernel/git/ralf/linux/+/refs/tags/linux-2.5.12/fs/jbd/revoke.c>

The file header identifies Stephen C. Tweedie and dates the revoke code to 2000. The inspected comments and implementation establish:

- revoke exists to stop old journal records for deleted metadata from being replayed over newer data using the same blocks;
- commit writes revoked-block information into the journal;
- recovery reconstructs transaction-sequenced revoke state and tests it before replay;
- when several revokes exist for one block, the latest transaction sequence is sufficient for the bounded replay test;
- an entry in a transaction later than the latest revoke is replayable again;
- within one transaction, `revoke -> journal` and `journal -> revoke` have different final precedence;
- an ordinary data write after revoke must **not** cancel the revoke;
- ext3 must issue revoke before clearing the block bitmap when deleting metadata, so replay protection is established before the block can be reused;
- the recovery-time revoke hash can be emptied after recovery.

Useful inspected regions:

- file header/comments around lines 16–46;
- `journal_revoke()` comments around lines 256–267;
- recovery support around lines 555–637 (`journal_set_revoke()`, `journal_test_revoke()`, revoke-table clearing).

Use in Case 74: primary source for the negative recovery relation itself.

### P3 — current Linux JBD2 on-disk documentation, continuity only

Linux kernel documentation, **JBD2 journal**:

<https://www.kernel.org/doc/html/latest/filesystems/ext4/journal.html>

The current documentation describes revocation blocks as preventing replay of a block in earlier transactions and gives the familiar metadata-freed/reallocated-as-file-data corruption example.

Use boundary: this source is a continuity/cross-check witness. It is **not** substituted for the period JBD source and does not establish byte-for-byte on-disk-format identity across all JBD/JBD2 revisions.

### S1 — Sivathanu et al. FAST '05

Muthian Sivathanu, Andrea C. Arpaci-Dusseau, Remzi H. Arpaci-Dusseau, and Somesh Jha, **“A Logic of File Systems,”** FAST '05, pp. 1–15.

USENIX record:

<https://www.usenix.org/conference/fast-05/logic-file-systems>

Paper:

<https://www.usenix.org/legacy/events/fast05/tech/full_papers/sivathanu/sivathanu.pdf>

Central anchor: §7.2.1, especially the discussion of the **non-rollback property**. The paper analyzes blocks whose type/role changes between journaled and non-journaled uses, explains how an older logged generation can otherwise overwrite newer file contents, and identifies ext3 revoke records plus reuse ordering as the mechanism preventing that rollback.

Use in Case 74: independent scholarly confirmation that physical survival and prior commit of an older positive image do not by themselves make that image admissible after reuse.

## Historical record established

### H/P — commit and checkpoint are separate stages

Tweedie 1998 establishes a positive journal lifecycle:

```text
journal updated metadata
    -> durable commit record
    -> transaction is recoverable through redo
    -> later propagation/checkpoint to home blocks
    -> only after home synchronization may journal space be reused
```

A committed journal image therefore remains constitutive recovery state for some time after commit.

### H/P — JBD adds an explicit negative recovery record

The period JBD source says revoke prevents old log records for deleted metadata from being replayed over newer data that uses the same blocks. The revoke relation is itself retained in the journal at commit and reconstructed during crash recovery.

This is stronger than a generic “old log entry becomes obsolete” statement: the implementation retains a block-number + transaction-sequence relation that actively changes whether another surviving committed record may execute during recovery.

### H/P — revoke authority is sequence-relative

The latest revoke sequence for a block suppresses the corresponding transaction and earlier journal images, while a later transaction can again contain a replayable image for that same physical block number.

Therefore:

```text
revoke(B) != permanent ban on B
```

and:

```text
replay admissibility = relation among block number, journal image transaction, and latest relevant revoke sequence
```

### H/P — within-transaction ordering matters

The source explicitly distinguishes:

```text
revoke(B) -> later journal(B)
    => the later journaling can cancel the revoke

journal(B) -> later revoke(B)
    => revoke survives / wins for recovery
```

Revoke is not a timeless Boolean property of a block address.

### H/P — ordinary data reuse must not cancel the old revoke

If a former metadata block is freed and reused as ordinary file data, a later ordinary data write does not cancel the revoke. Otherwise an older metadata image still surviving in the journal could be replayed after a crash and overwrite the newer file data.

### H/P — replay protection must precede allocation exposure

The `journal_revoke()` comment requires ext3 to revoke deleting metadata **before** clearing the block bitmap. This ordering makes the retention relation operationally significant: the “do not replay this older generation” evidence must exist before allocation state can expose the address to a new semantic use.

### H/P — recovery materializes transient control state from durable negative evidence

Recovery retains the latest revoke transaction for each block in an in-memory hash, tests it during replay, then clears the table after recovery.

Two embodiments therefore remain distinct:

1. durable revoke records that survive the crash boundary;
2. transient recovery-time derived state that exists only while replay decisions are being made.

## Engineering reconstruction

The following are **project reconstructions**, not Linux/JBD historical vocabulary.

### E — committed positive evidence can lose later replay authority without being erased

An old journal image can be:

- physically present;
- from a committed transaction;
- formerly valid recovery evidence;
- yet currently ineligible for replay because a later revoke relation supersedes its authority for that block generation.

This makes `was durably committed` weaker than `is admissible to restore now`.

### E — block-number continuity does not establish object/generation continuity

The bounded example reuses one physical block number first for metadata and later for ordinary file data. Address equality alone cannot identify the semantic state that should be restored.

`semantic generation` is analytical shorthand for that reuse boundary. It is not a JBD field.

### E — negative state can protect newer positive state

The revoke record contains no replacement payload. Its preservation function is to prevent an older positive image from acting on a newer home-block generation during recovery.

### E — complete negative history is not required

For the bounded replay test, the recovery code retains the latest relevant revoke sequence per block rather than a complete forever-history of every revoke. This is compressed control history, not archival event retention.

## Functional analogies — explicitly bounded

### A — Swift / Cassandra / Kafka tombstones

Cases 28, 41, and 42 also retain negative state that makes older positive state stop counting. The only claimed commonality is the functional relation:

> retained negative evidence can change the admissibility of surviving older positive evidence.

No shared genealogy, protocol, replication model, lifetime, or deletion semantics are claimed.

### A — ZooKeeper replay

Case 71 shows that recovery may combine a materialized representation with ordered retained history. Case 74 adds that some retained committed history can become **inadmissible** because later negative evidence qualifies replay.

### A — GFS lazy GC

Case 73 shows physical bytes can survive after namespace/currentness authority is withdrawn. Case 74 shows journal bytes can survive after replay authority is withdrawn. The mechanisms are historically independent.

## Philosophical interpretation boundary

Case 74 supports one bounded observation: a system can preserve continuity by remembering a **prohibition** rather than only a positive payload.

It does **not** support universal claims such as:

- `every absence is stored`;
- `forgetting always requires remembering`;
- `negative state is equivalent to memory in every philosophical sense`.

The technical result is narrower: this recovery protocol needs enough negative evidence to keep an older materially recoverable state from becoming current again.

## Prior-art boundary

Tweedie 1998 already treats journaling/log-enhanced filesystems as an existing class. The case therefore rejects claims that Linux or ext3 invented journaling or redo recovery.

The exact first historical revoke-like mechanism is not established here. The strongest historical statement is only:

> By the JBD source lineage represented in `linux-2.5.12` and whose `revoke.c` header dates the code to 2000, Linux JBD implemented transaction-sequenced revoke records to prevent stale metadata replay over newer reused-block data.

That is an implementation witness, not an invention-priority result.

## Related-repository check

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for:

- `ext3 JBD journal revoke`;
- `journaling filesystem`;

returned no dedicated JBD/ext3 revoke case to reuse. A broader Linux-filesystem or journaling engineering history should live there if later developed; this repository keeps only the retention/recovery decomposition.

## Limits and open work

1. The first historical invention/implementation of revoke-like recovery records remains unresolved.
2. The `linux-2.5.12` source is a reproducible period implementation witness, not proof that the mechanism first appeared in that tag.
3. This slice does not reconstruct all ext3 data modes, transaction/checkpoint state, or JBD/JBD2 format revisions.
4. It does not perform crash/fault injection on a period kernel.
5. It does not establish lower-layer disk-cache, barrier, FUA, or media-persistence composition.
6. Clearing the recovery hash or retiring journal records does not establish secure media erasure.
7. The current JBD2 documentation is continuity evidence only; exact revision genealogy remains separate work.

## Promotion decision

Case 74 meets the repository's `grounded` gate:

- strong period primary source: yes;
- exact source locations for central claims: yes;
- mechanism below UI metaphor: yes;
- maintenance/recovery work stated: yes;
- failure/forgetting modes separated: yes;
- modern analogies labeled: yes;
- philosophical interpretation separated: yes;
- counterexamples/limits included: yes;
- related-repository duplication checked: yes.

The case is **`grounded`**, not `mature`: invention chronology, full JBD/JBD2 evolution, and fault-injected implementation validation remain open.
