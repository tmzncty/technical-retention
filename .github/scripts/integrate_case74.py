from pathlib import Path

CASE_PATH = 'cases/74-linux-jbd-revoke-stale-replay-suppression.md'
EVIDENCE_PATH = Path('evidence/74-linux-jbd-1998-2005-revoke-grounding.md')

EVIDENCE = r'''# Case 74 grounding record — Linux JBD revoke and stale-redo suppression, 1998–2005

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
'''


def write_text(path, text):
    Path(path).write_text(text.rstrip() + '\n', encoding='utf-8')


def insert_after_line_containing(path, needle, new_line, uniqueness=None):
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    check = uniqueness or new_line
    if check in text:
        return
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if needle in line]
    assert len(matches) == 1, (path, needle, matches)
    lines.insert(matches[0] + 1, new_line)
    write_text(p, '\n'.join(lines))


def replace_line_starting(path, prefix, new_line):
    p = Path(path)
    lines = p.read_text(encoding='utf-8').splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    assert len(matches) == 1, (path, prefix, matches)
    lines[matches[0]] = new_line
    write_text(p, '\n'.join(lines))


assert Path(CASE_PATH).exists(), CASE_PATH
assert not EVIDENCE_PATH.exists(), EVIDENCE_PATH
write_text(EVIDENCE_PATH, EVIDENCE)

# README navigation: keep the new case next to the immediately preceding bounded case.
README_ROW = '- [`cases/74-linux-jbd-revoke-stale-replay-suppression.md`](cases/74-linux-jbd-revoke-stale-replay-suppression.md) — grounded filesystem-recovery bridge: Linux JBD retains transaction-sequenced revoke records so an older committed journal image can remain physically present yet lose replay authority after the same block number is freed/reused; later journal generations can become replayable again.'
insert_after_line_containing(
    'README.md',
    'cases/73-google-gfs-lazy-garbage-collection.md',
    README_ROW,
    'cases/74-linux-jbd-revoke-stale-replay-suppression.md',
)

# ROADMAP: integrate Case 74 into the open filesystem-crash-consistency bridge.
ROADMAP_FS = "- [ ] file-system crash consistency — **partially advanced by grounded Cases 16 and 74**: [`cases/16-bsd-ffs-soft-updates-crash-admissibility.md`](cases/16-bsd-ffs-soft-updates-crash-admissibility.md) uses 1999–2000 period-primary author/implementation evidence to separate volatile application-visible metadata, dependency-safe stable writeback, immediate crash-admissible mount state, explicit `fsync` durability closure, and later resource reclamation. [`cases/74-linux-jbd-revoke-stale-replay-suppression.md`](cases/74-linux-jbd-revoke-stale-replay-suppression.md), grounded by [`evidence/74-linux-jbd-1998-2005-revoke-grounding.md`](evidence/74-linux-jbd-1998-2005-revoke-grounding.md), adds a redo-journal reuse boundary: an older committed journal image can survive yet become replay-inadmissible after a later transaction records a block revoke before that physical block number is reused; recovery reconstructs latest revoke sequence state and later post-revoke journal generations can become eligible again. The broad item stays unchecked because copy-on-write/checkpoint consistency, transactional filesystems, modern `fsync`/rename semantics, complete WAL/journaling genealogy, fault-injected replay validation, and lower-layer device-persistence composition remain distinct regimes;"
replace_line_starting('ROADMAP.md', '- [ ] file-system crash consistency —', ROADMAP_FS)

ROADMAP_PHASE3 = "- [x] In redo-journal recovery under physical block reuse, separate committed positive journal images, transaction-sequenced revoke state, home-location current data, allocation/reuse state, replay authority, and transient recovery-time revoke tables — grounded in [`cases/74-linux-jbd-revoke-stale-replay-suppression.md`](cases/74-linux-jbd-revoke-stale-replay-suppression.md), with [`evidence/74-linux-jbd-1998-2005-revoke-grounding.md`](evidence/74-linux-jbd-1998-2005-revoke-grounding.md); broader journaling/WAL history and lower-layer persistence composition remain open."
insert_after_line_containing(
    'ROADMAP.md',
    'How should `returned/visible`, `crash-admissible`, `explicitly durable`, and `reclaimed/converged` be separated in filesystem regimes?',
    ROADMAP_PHASE3,
    'In redo-journal recovery under physical block reuse',
)

ROADMAP_PHASE4 = "- [x] stale committed recovery evidence becoming replay-inadmissible after block reuse — grounded in Case 74: JBD revoke retains a transaction-relative negative relation that suppresses older redo without erasing the old journal bytes; secure media deletion and broader negative-log genealogy remain separate work;"
insert_after_line_containing(
    'ROADMAP.md',
    '- [ ] unsafe filesystem dependency ordering or incomplete durability closure;',
    ROADMAP_PHASE4,
    'stale committed recovery evidence becoming replay-inadmissible',
)

# CASE_INDEX case ledger.
CASE_ROW = '| [Linux JBD Journal Revoke Records: Negative Recovery State, Block Reuse, and Stale-Redo Suppression](cases/74-linux-jbd-revoke-stale-replay-suppression.md) | **grounded** | committed redo images + transaction sequence/commit state + block-number revoke records + allocation/reuse state + transient recovery revoke table | separate prior commit from present replay authority; show negative recovery evidence can preserve newer reused-block state without erasing older positive history; distinguish physical block identity from semantic generation | [1998–2005 JBD revoke grounding](evidence/74-linux-jbd-1998-2005-revoke-grounding.md); exact first revoke-like implementation, full JBD/JBD2 chronology, ext3 data-mode history, fault injection, and lower-layer persistence remain separate work |'
insert_after_line_containing(
    'CASE_INDEX.md',
    'cases/73-google-gfs-lazy-garbage-collection.md',
    CASE_ROW,
    'cases/74-linux-jbd-revoke-stale-replay-suppression.md',
)

# Repair a stale aggregate count that had stopped at Case 64.
idxp = Path('CASE_INDEX.md')
idx = idxp.read_text(encoding='utf-8')
old_count = 'After sixty-five bounded cases, **all sixty-five cases are now `grounded`.**'
new_count = 'After seventy-five bounded cases, **all seventy-five cases are now `grounded`.**'
assert old_count in idx or new_count in idx
idx = idx.replace(old_count, new_count)
write_text(idxp, idx)

FINDINGS = r'''861. **committed journal image ≠ permanently replay-authoritative image** — a later JBD revoke can make an older committed block image ineligible for recovery without erasing it;
862. **revoke record ≠ physical erase** — revoke changes crash-replay admissibility for a block/transaction range, not the bytes of the old journal record or home medium;
863. **block-number continuity ≠ semantic-generation continuity** — one physical block number can move from metadata use to later ordinary file-data use while stale journal history for the earlier role still survives;
864. **transaction commit ≠ unconditional future replay authority** — commit establishes a recovery candidate, but later filesystem evolution can legitimately withdraw that candidate's authority;
865. **latest revoke sequence can qualify older positive history** — recovery needs an ordering relation between the candidate journal transaction and the newest relevant revoke, not just evidence that the candidate once committed;
866. **negative recovery state can preserve newer positive state** — the revoke contains no replacement payload yet prevents stale redo from overwriting a newer home-block generation;
867. **same-transaction event order can determine recovery authority** — `revoke -> journal` and `journal -> revoke` have different final precedence in the bounded JBD source;
868. **ordinary data write after revoke ≠ revoke cancellation** — the later non-journaled data write is precisely what still needs protection from an older metadata redo image;
869. **allocation-reuse exposure must not outrun replay protection** — ext3's documented rule to revoke metadata before clearing its block bitmap establishes the negative recovery relation before the address can be reused;
870. **durable revoke record ≠ recovery-time revoke hash** — crash-surviving journal evidence is reconstructed into a transient in-memory table used only while replay decisions are made;
871. **latest-per-block revoke summary ≠ complete revoke history** — the bounded recovery test can retain only the latest relevant revoke sequence rather than every revoke event forever;
872. **revoke scope ≠ permanent block prohibition** — a journal image from a transaction later than the latest revoke can become replay-eligible for the same physical block number;
873. **checkpoint obligation ≠ revoke obligation** — positive journal history remains needed until home propagation closes, while revoke separately decides whether an older retained image is still allowed to act after reuse;
874. **JBD revoke ≠ Swift/Cassandra/Kafka tombstone semantics** — all can function as negative admissibility evidence, but their replication models, lifetimes, objects, and historical mechanisms differ;
875. **post-recovery revoke-table clearing ≠ secure forgetting** — retiring the transient hash does not establish removal of durable journal bytes or lower-layer forensic traces;
876. **replay currentness can depend on retained negative evidence** — correct recovery may require remembering not only which positive transaction committed, but which surviving committed history a later ordered relation has disqualified.'''

idx = idxp.read_text(encoding='utf-8')
if '861. **committed journal image ≠ permanently replay-authoritative image**' not in idx:
    lines = idx.splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith('860. **storage reclamation ≠ secure sanitization**')]
    assert len(matches) == 1, matches
    lines[matches[0] + 1:matches[0] + 1] = FINDINGS.splitlines()
    write_text(idxp, '\n'.join(lines))

MATRIX_ROW = '| Linux JBD revoke / 2000-source bounded regime | home-block bytes + committed journal block images + transaction commit/sequence state + per-block revoke records + allocation/reuse state + transient recovery revoke table | commit positive journal images; checkpoint to home locations; later revoke before reuse; recovery reconstructs latest revoke sequences and suppresses stale earlier redo | ordinary read is not the focus; crash recovery evaluates positive log images together with later negative revoke evidence, so a committed older image can be skipped | the physical block number can remain constant while its semantic role changes; transaction sequence scopes which historical image may act on that address | missing/late revoke can let stale metadata overwrite newer file data; clearing the recovery hash retires only transient control state | no complete history is required for the bounded test; current home/journal state plus latest relevant revoke sequence per block is sufficient to decide replay |'
insert_after_line_containing(
    'CASE_INDEX.md',
    '| Google File System / 2003 bounded lazy-GC regime |',
    MATRIX_ROW,
    '| Linux JBD revoke / 2000-source bounded regime |',
)

print('Case 74 evidence and repository integration prepared')
