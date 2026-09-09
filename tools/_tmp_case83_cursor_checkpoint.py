from pathlib import Path
import re
import subprocess

ROOT = Path('.')


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def write(path, text):
    text = text.rstrip() + '\n'
    (ROOT / path).write_text(text, encoding='utf-8')


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one match, found {count}')
    return text.replace(old, new, 1)

EVIDENCE_PATH = 'evidence/83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md'
EVIDENCE = r'''# Case 83 deepening — HDFS BlockScanner cursor checkpointing, restart continuity, and the clock-domain boundary

## Purpose

This addendum deepens the scan-progress part of Case 83. The earlier grounding established that Hadoop 2.7.3 has a persistent `BlockIterator` / cursor mechanism, but deliberately left its crash and atomicity semantics open.

The bounded question here is narrower:

> What does the HDFS scanner actually persist about maintenance progress, how does it recover when that state is unavailable, and does the configured periodic checkpoint interval equal the checkpoint behavior of the inspected implementation?

The answer matters because the scanner's retained control state is not user payload, yet it changes how much verification work must be repeated after interruption and therefore can change how long some still-unchecked replicas wait for renewed integrity evidence.

This record separates:

- **historical / primary record** — Apache JIRA and tag-matched Apache source;
- **engineering reconstruction** — what those state transitions mean for retention and maintenance continuity;
- **functional analogy** — a narrow comparison to other retained control-state cases;
- **philosophical interpretation** — limited to the fact that a preservation process can itself depend on retained state.

It does **not** claim a first invention of scan cursors, checkpoints, atomic rename, or background scrubbing.

---

## Source set

| Source | Date / version | Type | Use | Grade |
| --- | --- | --- | --- | --- |
| Apache HDFS-7430, `Rewrite the BlockScanner to use O(1) memory and use multiple threads` | created 24 Nov 2014; resolved 22 Jan 2015 for 2.7.0 | project design / implementation issue | direct design intent: track the last-scanned position rather than per-block scan status; use one verification thread per volume | **H/P** |
| Apache Hadoop `rel/release-2.7.3`, `FsVolumeImpl.java` | release 2.7.3 | tag-matched source | exact cursor state, temp-file save, `ATOMIC_MOVE`, load behavior | **H/P** |
| Apache Hadoop `rel/release-2.7.3`, `BlockScanner.java` | release 2.7.3 | tag-matched source | configured cursor-save interval; default internal value of ten minutes | **H/P** |
| Apache Hadoop `rel/release-2.7.3`, `VolumeScanner.java` | release 2.7.3 | tag-matched source | load fallback, EOF/shutdown saves, intended periodic save branch, wall-clock rescan scheduling | **H/P** |
| Apache HDFS-12209, `VolumeScanner scan cursor not save periodic` | later project bug linked from HDFS-7430; current JIRA state exposed as `Patch Available` | project defect witness | confirms that the intended periodic cursor save did not in fact occur as expected | **H/P** |
| Cloudera, `HDFS DataNode Scanners and Disk Checker Explained` | 2017-era operational documentation | vendor / near-contemporary secondary explanation | corroborates intended model: disk cursor, periodic save, ten-minute default, restart continuity | **B** |
| Apache Hadoop `trunk`, `VolumeScanner.java` + `FsVolumeImpl.java` | inspected 9 Sep 2026 | current-source continuity witness | shows the same `monotonicNow()` versus wall-clock `lastSavedMs` comparison remains present in current source; not a claim about every binary release | **H/P*** |

`H/P*` here means direct current project source used only as a continuity check, not as a historical origin witness.

Primary URLs:

- HDFS-7430: <https://issues.apache.org/jira/browse/HDFS-7430>
- HDFS-12209: <https://issues.apache.org/jira/browse/HDFS-12209>
- Hadoop 2.7.3 `FsVolumeImpl.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/fsdataset/impl/FsVolumeImpl.java>
- Hadoop 2.7.3 `BlockScanner.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/BlockScanner.java>
- Hadoop 2.7.3 `VolumeScanner.java`: <https://github.com/apache/hadoop/blob/rel/release-2.7.3/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/VolumeScanner.java>
- Cloudera explanation: <https://www.cloudera.com/blog/technical/hdfs-datanode-scanners-and-disk-checker-explained.html>

---

## Historical record

### H/P — HDFS-7430 explicitly trades per-block history for bounded traversal state

HDFS-7430 describes the 2.7.0 scanner rewrite as using a constant amount of memory by keeping track of **what block was scanned last**, rather than retaining the scan status of all blocks in memory. It also moves to a verification thread per disk / volume and a configurable byte rate.

This is important negative evidence. The rewrite's intended persisted state is a compact traversal position, not a durable table saying when every block was last verified and whether every verification succeeded.

Therefore:

> **retained traversal position != retained per-block verification history.**

And, because HDFS-7430 is an implementation-change record rather than an origin survey:

> **2014–2015 rewrite != invention of scan checkpointing.**

The older HDFS scanner and GFS prior-art boundaries in the base Case 83 remain unchanged.

### H/P — the 2.7.3 cursor is concrete serialized control state

`FsVolumeImpl.BlockIteratorState` serializes:

- `lastSavedMs` — documented in source as wall-clock milliseconds since the epoch when the iterator was last saved;
- `iterStartMs` — also wall-clock milliseconds since the epoch when the iterator was created / rewound;
- `curFinalizedDir`;
- `curFinalizedSubDir`;
- `curEntry`;
- `atEnd`.

The directory/subdirectory/entry fields encode where sorted traversal has reached. `atEnd` records whether the pass has exhausted the iterator. This is not payload, checksum content, replica-placement state, or a complete verification log.

The source therefore permits a more exact project term than the earlier generic phrase `saved scanner state`:

> **the cursor is a retained maintenance-traversal checkpoint.**

`maintenance-traversal checkpoint` is project reconstruction vocabulary, not Apache terminology.

### H/P — save uses temp-file serialization followed by a requested atomic move

`BlockIteratorImpl.save()` in 2.7.3:

1. updates `lastSavedMs` with `Time.now()`;
2. serializes state to `<name>.cursor.tmp` through a `FileOutputStream` / writer;
3. closes the writer;
4. requests `Files.move(temp, final, StandardCopyOption.ATOMIC_MOVE)` to `<name>.cursor`.

This is materially stronger than overwriting the live cursor file in place: the code asks the filesystem for an atomic pathname transition after writing a complete temporary representation.

But this source does **not** call `FileDescriptor.sync`, `FileChannel.force`, or a directory `fsync` in the inspected save method. Therefore the bounded claim is only:

> **atomic cursor-path replacement is requested.**

It is not:

> **the cursor is proven durable across every sudden power-loss / filesystem / controller failure point.**

Hence:

> **atomic rename/move semantics != demonstrated power-loss durability.**

That remaining physical durability question requires filesystem/platform evidence or fault injection, not inference from the Java call alone.

### H/P — unreadable or absent saved state falls back to a fresh iterator

`VolumeScanner.enableBlockPoolId` attempts `volume.loadBlockIterator(...)`. It handles both `FileNotFoundException` and broader `IOException`; if no iterator was loaded, it creates `volume.newBlockIterator(...)` instead.

That fallback is an important retention boundary:

> **cursor load failure != scanner disablement.**

For this bounded implementation, losing or failing to parse the saved cursor can cause traversal to restart rather than making the user payload disappear.

The safe engineering consequence is:

> **maintenance-progress loss can become repeated maintenance work.**

Do not strengthen that to `cursor loss is harmless`. Repeating earlier blocks consumes the scanner's bounded I/O budget and can delay arrival at blocks later in the traversal, increasing their verification age even though no payload was directly corrupted by cursor loss.

### H/P — EOF and orderly-shutdown checkpoints are distinct from the configured periodic checkpoint

`VolumeScanner` calls `saveBlockIterator(curBlockIter)` when the iterator reaches EOF. When the scanner thread exits, it loops over all block iterators and saves them before cleanup.

Those are real save paths in the inspected code.

A separate in-pass branch is intended to save after `conf.cursorSaveMs`. `BlockScanner.Conf` gives that internal cursor-save interval a ten-minute default.

These events must not be collapsed:

- end-of-pass save;
- orderly scanner-exit save;
- interval-triggered save during a long pass.

The first two can occur even if the third is defective.

### H/P — the 2.7.3 in-pass interval check mixes incompatible clock domains

The bounded source contains a subtle but direct contradiction between its state definition and its save scheduler:

- `BlockIteratorState.lastSavedMs` is initialized and updated with `Time.now()` and is explicitly documented as **wall-clock ms since the epoch**;
- `VolumeScanner.runLoop` sets `monotonicMs = Time.monotonicNow()`;
- the periodic condition computes `saveDelta = monotonicMs - curBlockIter.getLastSavedMs()`.

A monotonic-uptime-style value and an epoch wall-clock value are not a meaningful common timestamp domain. On ordinary platforms the subtraction is negative / nonsensical for the intended elapsed-time comparison, so the configured interval branch does not provide the intended periodic checkpoint cadence.

This is not merely a modern reviewer inference. Apache links **HDFS-12209 — `VolumeScanner scan cursor not save periodic`** directly from the HDFS-7430 issue and exposes it as a Major bug with a patch available.

Therefore the earlier Case 83 wording must be narrowed:

> **configured periodic-save branch != effective periodic checkpoint behavior.**

And more generally:

> **retention policy intent != effective retention of maintenance state.**

This is a particularly useful counterexample for a repository about retention because the state whose retention fails is the state of the process responsible for renewing trust in other retained state.

### H/P* — current Apache trunk remains a continuity witness, not an origin claim

A 9-Sep-2026 check of Apache Hadoop `trunk` still shows:

- `BlockIteratorState.lastSavedMs` initialized with `Time.now()` and documented as wall-clock time;
- `save()` setting it via `Time.now()`;
- `VolumeScanner.runLoop` computing `monotonicMs = Time.monotonicNow()` and subtracting `getLastSavedMs()`.

This supports only a narrow continuity statement about the currently visible source tree. It does not prove that every release, downstream distribution, patched vendor build, or running HDFS cluster shares the same behavior.

---

## What a cursor position does and does not prove

The iterator advances to a block entry before `scanBlock` finishes verification. The scanner can record a scan error while continuing later work. The cursor therefore cannot be promoted into a certificate that every prior entry verified successfully.

A saved cursor supports:

> **where broad traversal had reached.**

It does not by itself support:

> **every earlier block is currently healthy.**

Nor does it support:

> **every earlier block was successfully checked during this pass.**

This yields:

> **traversal progress != successful-verification ledger.**

At EOF the scanner may have completed a traversal while `scanErrorsSinceRestart` is nonzero. The relevant error/reporting state is analytically separate from the position checkpoint.

---

## Restart semantics

The bounded recovery paths can be reconstructed as:

```text
live scan traversal
      |
      +--> EOF save ------------------------------+
      |                                           |
      +--> orderly-exit save ---------------------+--> saved .cursor
      |                                           |
      +--> intended interval save --[clock bug]---+
                                                  |
                                                  v
restart / block-pool enable
      |
      +--> cursor parses --> resume from retained traversal position
      |
      +--> missing/unreadable cursor --> create fresh iterator / replay traversal
```

This is a replay-tolerant maintenance mechanism, not exactly-once scan execution.

A stale cursor generally moves restart position **backward relative to actual work already completed**, causing some checks to be repeated. That is different from a journal checkpoint whose loss can authorize an unsafe newer state. But the repeated work still has a retention cost because the scanner is bandwidth-limited: replay can postpone checks of later blocks.

Therefore:

> **restart continuity != exact-once maintenance traversal.**

and:

> **replayed verification work != payload repair.**

---

## Cross-case comparison — progress checkpoint versus correctness-authority checkpoint

A narrow functional comparison to Case 90 (Kafka leader-epoch recovery) is useful because both systems retain small non-payload control records across restart.

The similarity stops at **retained control state used by a later recovery/maintenance procedure**.

The semantics differ sharply:

- HDFS Case 83's cursor is traversal progress. If it cannot be loaded, the bounded code creates a fresh iterator and can repeat work.
- Kafka Case 90's leader-epoch checkpoint participates in log-lineage / safe-truncation reasoning. It is not merely an optimization cursor for replayable background coverage.

Thus:

> **checkpointed control state != one universal correctness role.**

This is a functional analogy only. It is not evidence of HDFS↔Kafka design genealogy.

---

## Engineering reconstruction

The source set supports the following bounded relations:

1. `scanner cursor != user payload`;
2. `cursor position != per-block verification history`;
3. `cursor position != certificate that prior blocks are healthy`;
4. `configured checkpoint interval != effective checkpoint cadence`;
5. `wall-clock timestamp != monotonic timestamp`;
6. `EOF checkpoint != periodic in-pass checkpoint`;
7. `orderly-shutdown checkpoint != sudden-crash checkpoint`;
8. `ATOMIC_MOVE request != demonstrated power-loss durability`;
9. `cursor load failure != scanner disablement`;
10. `checkpoint rollback/replay != payload rollback`;
11. `replayed verification != payload repair`;
12. `maintenance-progress retention != maintenance correctness proof`;
13. `restart continuity != exactly-once traversal`;
14. `maintenance-state retention failure can change verification timeliness without directly corrupting payload`.

These are project engineering terms, not Apache historical vocabulary.

---

## Philosophical limit

The bounded conceptual result is modest:

> A process that exists to renew confidence in retained data may itself depend on retained state whose loss or staleness changes the temporal pattern of that maintenance.

That does not make every checkpoint a `memory of memory`, does not turn the scanner into an epistemological subject, and does not imply that losing maintenance state is equivalent to losing payload.

The point is operational: **retention infrastructure can have its own retention obligations and failure modes.**

---

## Rejected / unsupported claims

Do not claim:

- HDFS invented persistent scan cursors;
- HDFS-7430 invented O(1) maintenance checkpointing generally;
- the cursor is a complete durable log of verification results;
- a cursor positioned after a block proves that block verified successfully;
- `ATOMIC_MOVE` alone proves power-loss durability of the cursor;
- the ten-minute configured interval means the 2.7.3 cursor was effectively saved every ten minutes;
- cursor loss corrupts the HDFS block payload;
- fallback to a fresh iterator makes cursor failure cost-free;
- the HDFS cursor and Kafka leader-epoch checkpoint are the same mechanism or share a genealogy;
- current Apache trunk source describes every historical or vendor HDFS deployment.

---

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `BlockScanner`, `VolumeScanner`, `HDFS-7430`, `HDFS-12209`, and cursor terminology found no dedicated technical-history case to reuse.

The broad BlockScanner rewrite genealogy, Java/filesystem atomic-move history, HDFS storage-layout evolution, and vendor deployment history should go there if pursued. `technical-retention` keeps only the retention-specific distinction between payload, integrity evidence, maintenance traversal state, checkpoint durability, and effective maintenance cadence.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the anti-anachronism boundary: Apache's `cursor file`, `BlockIterator`, `save`, and issue vocabulary are historical; `maintenance-traversal checkpoint`, `verification age`, and `retention of maintenance state` are project reconstructions.

---

## Remaining work

This slice closes the **source-level cursor format / checkpoint-path / clock-domain behavior** gap for the bounded 2.7.3 scanner. It does not close:

- filesystem-specific atomic-move and directory-durability behavior;
- sudden power-loss fault injection around temp write / move / restart;
- downstream-vendor patches and release-by-release HDFS-12209 handling;
- quantified delay added by replaying a stale cursor on very large volumes;
- earliest HDFS scanner/cursor genealogy;
- independent production-cluster observations.
'''

# 1. New evidence file.
if (ROOT / EVIDENCE_PATH).exists():
    raise RuntimeError(f'{EVIDENCE_PATH} already exists')
write(EVIDENCE_PATH, EVIDENCE)

# 2. Deepen Case 83 and correct the earlier overstatement about effective periodic saving.
case_path = 'cases/83-apache-hdfs-block-scanner-checksum-verification.md'
case = read(case_path)
case = replace_once(
    case,
    'The iterator is also saved at the end of a block-pool pass and at configured intervals during a pass.',
    'The code saves the iterator at the end of a block-pool pass and contains a configured-interval save branch during a pass. A source-level deepening plus Apache HDFS-12209 now shows that the bounded 2.7.3 interval branch mixes monotonic time with the cursor\'s wall-clock `lastSavedMs`, so `configured periodic save` must be treated as design intent rather than demonstrated effective cadence; EOF and orderly-shutdown saves remain separate real paths.',
    'case83 periodic-save sentence')
case = replace_once(
    case,
    'The exact durability/atomicity guarantees of the cursor implementation are outside this case, but the design intent is direct: scanner progress is not merely ephemeral loop-local state.',
    'The cursor path is now source-audited more closely in [`../evidence/83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md`](../evidence/83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md). `FsVolumeImpl` serializes the iterator to a temporary file and requests an `ATOMIC_MOVE` to the live `.cursor`; load failure falls back to a fresh iterator. This establishes a concrete restart checkpoint mechanism while still stopping short of claiming power-loss durability, because the inspected method does not itself establish file/directory flush semantics.',
    'case83 atomicity paragraph')
insert_marker = 'The cursor is not payload and does not make an unchecked block trustworthy. It preserves where the maintenance process was in its coverage traversal.\n\n---\n\n## Verification is not repair'
insert_text = '''The cursor is not payload and does not make an unchecked block trustworthy. It preserves where the maintenance process was in its coverage traversal.

### H/P — the checkpoint mechanism can exist while its periodic cadence is defective

HDFS-7430 (2014–2015) states the rewrite goal directly: use O(1) memory by retaining what block was scanned last rather than keeping scan status for all blocks, and use a verification thread per volume. The 2.7.3 `BlockIteratorState` then makes that compact state inspectable: wall-clock `lastSavedMs` / `iterStartMs`, current finalized directory/subdirectory/entry, and `atEnd`.

The important correction is that **retained checkpoint representation and effective checkpoint cadence are different claims**. `BlockScanner.Conf` defines a ten-minute internal cursor-save interval, but `VolumeScanner.runLoop` computes the interval using `Time.monotonicNow() - getLastSavedMs()` while `lastSavedMs` is explicitly an epoch wall-clock value set by `Time.now()`. Apache's later HDFS-12209 is titled `VolumeScanner scan cursor not save periodic` and is linked from HDFS-7430 as a Major bug with a patch available.

Therefore:

> **configured cursor-save interval ≠ effective periodic cursor checkpointing.**

The failure does not erase block payload. A missing/unreadable saved cursor causes `enableBlockPoolId` to create a fresh iterator, so progress loss is converted into repeated traversal. That replay can still matter: scanner bandwidth is bounded, so rechecking earlier blocks can delay integrity renewal for later blocks.

The save path itself writes a temporary cursor then requests `StandardCopyOption.ATOMIC_MOVE`. This supports `atomic pathname replacement requested`, not a universal sudden-power-loss durability guarantee. No independent filesystem/power-cut experiment is added here.

Finally, a cursor is not a success ledger. Iterator position can advance even when a block scan records an error, so:

> **traversal position ≠ proof that every prior block passed verification.**

Detailed record: [`../evidence/83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md`](../evidence/83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md).

---

## Verification is not repair'''
case = replace_once(case, insert_marker, insert_text, 'case83 cursor-deepening insertion')
case = case.replace('7. **lifetime of the saved scanner cursor across restart**.', '7. **lifetime and freshness of the saved scanner cursor across restart**.', 1)
case = replace_once(
    case,
    '- **coverage/progress state loss** — may cause inefficient/repeated coverage or enlarge the interval before some blocks are revisited, depending on implementation recovery;',
    '- **coverage/progress state loss or staleness** — in the bounded loader, a missing/unreadable cursor falls back to a fresh iterator and a stale valid cursor can replay already-covered entries; this does not directly corrupt payload but can consume scan budget and delay later verification;',
    'case83 failure-mode cursor bullet')
case = replace_once(
    case,
    'per-volume scanners rate-limit periodic coverage, prioritize suspect blocks, persist iterator/cursor progress, distinguish some transient races from bad-block verdicts, and report qualifying failures into the distributed replica-management path.',
    'per-volume scanners rate-limit periodic coverage, prioritize suspect blocks, use a persisted iterator/cursor mechanism whose 2.7.3 periodic checkpoint branch has a documented clock-domain defect, distinguish some transient races from bad-block verdicts, and report qualifying failures into the distributed replica-management path.',
    'case83 prior-art bounded claim')
case = replace_once(
    case,
    '20. `coherent verification ≠ free verification`.',
    '''20. `coherent verification ≠ free verification`;
21. `cursor position ≠ per-block verification history`;
22. `configured checkpoint interval ≠ effective checkpoint cadence`;
23. `ATOMIC_MOVE request ≠ demonstrated power-loss durability`;
24. `cursor load failure ≠ scanner disablement`;
25. `checkpoint rollback/replay ≠ payload rollback`;
26. `restart continuity ≠ exactly-once maintenance traversal`.''',
    'case83 reconstruction list')
case = replace_once(
    case,
    '- exact durability/atomicity guarantees of the saved block-iterator cursor;',
    '- filesystem-specific / power-loss durability of the saved block-iterator cursor and independent crash fault injection; the source-level temp-file / `ATOMIC_MOVE` / load-fallback path and the periodic-save clock-domain defect are now grounded;',
    'case83 future-work cursor item')
write(case_path, case)

# 3. Update the base evidence record so it no longer presents periodic save as effective behavior.
base_path = 'evidence/83-hadoop-2003-2016-block-scanner-grounding.md'
base = read(base_path)
base = replace_once(
    base,
    '| Apache JIRA HDFS-7548, `Corrupt block reporting delayed until datablock scanner thread detects it` | 2014–2015 | project issue | confirms scanner-mediated corruption discovery/reporting remained operationally consequential | **H/P** |',
    '''| Apache JIRA HDFS-7548, `Corrupt block reporting delayed until datablock scanner thread detects it` | 2014–2015 | project issue | confirms scanner-mediated corruption discovery/reporting remained operationally consequential | **H/P** |
| Apache JIRA HDFS-7430, `Rewrite the BlockScanner to use O(1) memory and use multiple threads` | 2014–2015 | project design / implementation issue | grounds compact last-scanned-position design and per-volume rewrite | **H/P** |
| Apache JIRA HDFS-12209, `VolumeScanner scan cursor not save periodic` | later project bug, linked from HDFS-7430 | project defect witness | corrects the assumption that the configured in-pass cursor-save interval was effective | **H/P** |''',
    'base evidence source table')
old_cursor = '''#### Retained iterator / cursor

The scanner calls `iter.save()` through `saveBlockIterator`.

In `findNextUsableBlockIter`, the source explicitly explains that the saved cursor file uses wall-clock time because monotonic time commonly resets when the machine reboots. The iterator is saved at block-pool EOF and periodically during scanning based on a cursor-save interval.

Supported claim:

> The implementation intentionally persists enough scanner traversal state to cross process/machine reboot boundaries rather than treating one scan pass as disposable volatile loop state.

Evidence limit:

- this case does not audit the cursor-file format;
- it does not establish atomicity under every crash point;
- it does not establish a durable per-block cryptographic verification ledger.

The safe reconstruction is `retained scan-progress/cursor state`, not `perfect durable proof of verification history`.'''
new_cursor = '''#### Retained iterator / cursor

The scanner calls `iter.save()` through `saveBlockIterator`. `findNextUsableBlockIter` explicitly explains that the persisted cursor uses wall-clock time because monotonic time commonly resets when the machine reboots.

The source-level mechanism is now deepened in [`83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md`](83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md): `FsVolumeImpl` serializes directory/subdirectory/entry/EOF position plus wall-clock save/start timestamps to a temporary file and requests `ATOMIC_MOVE` to the live `.cursor`; `VolumeScanner` falls back to a fresh iterator if loading fails.

However, the earlier phrase `saved periodically` is too strong for effective 2.7.3 behavior. The in-pass interval branch subtracts the wall-clock `lastSavedMs` from `Time.monotonicNow()`, and Apache HDFS-12209 is explicitly titled `VolumeScanner scan cursor not save periodic`. EOF and orderly-exit saves are separate code paths and remain grounded.

Supported claims:

> The implementation has an explicit restart-persistent scanner traversal checkpoint mechanism.

> Configured periodic-save intent does not establish effective periodic checkpoint cadence.

> Missing/unreadable checkpoint state can fall back to replay from a fresh iterator.

Evidence limits:

- requested `ATOMIC_MOVE` does not by itself establish file/directory durability under sudden power loss;
- a cursor position is not a complete per-block success history;
- this slice does not provide filesystem fault injection or downstream-vendor patch genealogy.

The safe reconstruction is `retained maintenance-traversal checkpoint`, not `perfect durable proof of verification history`.'''
base = replace_once(base, old_cursor, new_cursor, 'base evidence cursor section')
addendum_marker = '## Claim ledger\n'
addendum = '''## Cursor checkpoint addendum — retained maintenance state can have a defective retention cadence

Detailed record: [`83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md`](83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md).

HDFS-7430 makes the O(1) design goal explicit: retain last-scanned traversal position instead of per-block scan status. The 2.7.3 source serializes that compact cursor and requests a temp-file-to-live-file atomic move. But the periodic checkpoint condition mixes monotonic and wall-clock time domains, and HDFS-12209 records the resulting failure to save the cursor periodically.

The safe engineering relations are:

- `cursor position != per-block verification history`;
- `configured cursor-save interval != effective periodic checkpoint cadence`;
- `ATOMIC_MOVE request != demonstrated power-loss durability`;
- `cursor load failure != scanner disablement`;
- `checkpoint replay != payload rollback`;
- `restart continuity != exactly-once scan execution`.

This narrows an earlier Case 83 overstatement without changing the broader conclusion that scan progress is a real retained control-state class.

---

## Claim ledger
'''
base = replace_once(base, addendum_marker, addendum, 'base evidence addendum insertion')
base = replace_once(
    base,
    '| scanner traversal/cursor state is saved | H/P | `saveBlockIterator`, cursor-file comment | no crash-atomicity proof for cursor format |',
    '| scanner traversal/cursor state has explicit save/load paths | H/P | `FsVolumeImpl.BlockIteratorImpl`, `VolumeScanner` | EOF/orderly-exit saves are grounded; in-pass periodic save is affected by the HDFS-12209 clock-domain defect |',
    'base evidence claim row')
claim_anchor = '| coherence correction can have service cost | H/P + E | HDFS-12136 | product/code-path witness, not universal law |'
claim_rows = '''| coherence correction can have service cost | H/P + E | HDFS-12136 | product/code-path witness, not universal law |
| HDFS-7430 intentionally replaces per-block scan-status memory with last-scanned traversal position | H/P | HDFS-7430 | rewrite witness, not checkpoint invention priority |
| 2.7.3 cursor save uses temp serialization plus requested `ATOMIC_MOVE` | H/P | `FsVolumeImpl.java` | does not establish sudden-power-loss durability |
| missing/unreadable cursor load falls back to a fresh iterator | H/P | `VolumeScanner.enableBlockPoolId` | replay can still consume bounded scan budget |
| 2.7.3 periodic cursor-save check mixes monotonic and wall-clock timestamps | H/P | `VolumeScanner.java` + `FsVolumeImpl.java` | exact elapsed-time comparison is invalid across those domains |
| Apache records a bug titled `VolumeScanner scan cursor not save periodic` | H/P | HDFS-12209 | supports defect boundary, not every downstream deployment |
| cursor progress is not a successful-verification ledger | E | iterator advance + separate scan-error path | project reconstruction |'''
base = replace_once(base, claim_anchor, claim_rows, 'base evidence claim rows')
base = replace_once(
    base,
    '21. `coherent verification ≠ free verification`.',
    '''21. `coherent verification ≠ free verification`;
22. `cursor position ≠ per-block verification history`;
23. `configured checkpoint interval ≠ effective checkpoint cadence`;
24. `ATOMIC_MOVE request ≠ demonstrated power-loss durability`;
25. `cursor load failure ≠ scanner disablement`;
26. `checkpoint replay ≠ payload rollback`;
27. `restart continuity ≠ exactly-once scan traversal`.''',
    'base evidence reconstruction list')
base = replace_once(
    base,
    'Searches of `tmzncty/computing-archaeology` for `HDFS`, `HDFS block scanner checksum`, and the specific scanner mechanism returned no dedicated case at the time of the original slice. A fresh check during the HDFS-11160 deepening likewise found no dedicated `HDFS-11160`, `VolumeScanner`, or `BlockScanner` case to reuse.',
    'Searches of `tmzncty/computing-archaeology` for `HDFS`, `HDFS block scanner checksum`, and the specific scanner mechanism returned no dedicated case at the time of the original slice. Fresh checks during the HDFS-11160 deepening and this cursor-checkpoint deepening likewise found no dedicated `HDFS-11160`, `HDFS-7430`, `HDFS-12209`, `VolumeScanner`, or `BlockScanner` case to reuse.',
    'base evidence related repo')
base = replace_once(
    base,
    '- saved scan progress is a complete durable history of every verification event;',
    '- saved scan progress is a complete durable history of every verification event;\n- the configured ten-minute cursor-save interval proves the 2.7.3 implementation checkpointed effectively every ten minutes;\n- requested `ATOMIC_MOVE` alone proves power-loss durability of the cursor;',
    'base evidence rejected claims')
base = replace_once(
    base,
    '- uncertainty about exact scanner genealogy, cursor crash atomicity, and later product behavior is explicitly retained rather than hidden.',
    '- uncertainty about exact scanner genealogy, filesystem/power-loss cursor durability, HDFS-12209 release/downstream handling, and later product behavior is explicitly retained rather than hidden.',
    'base evidence promotion judgment')
write(base_path, base)

# 4. Add a completed Phase-2 roadmap slice.
roadmap_path = 'ROADMAP.md'
roadmap = read(roadmap_path)
roadmap_marker = '## Phase 2 — Build missing technical bridges\n\n'
roadmap_bullet = '''## Phase 2 — Build missing technical bridges

- [x] Case 83 HDFS BlockScanner cursor checkpoint / clock-domain deepening — [`cases/83-apache-hdfs-block-scanner-checksum-verification.md`](cases/83-apache-hdfs-block-scanner-checksum-verification.md), deepened by [`evidence/83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md`](evidence/83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md): HDFS-7430 grounds the O(1) last-scanned-position design; Hadoop 2.7.3 source grounds the serialized directory/subdirectory/entry/EOF cursor, temp-file + requested `ATOMIC_MOVE` save, EOF/orderly-exit checkpoints, and load-failure fallback to a fresh iterator. The same source also exposes a monotonic-versus-wall-clock mismatch in the configured in-pass save condition, while HDFS-12209 records `VolumeScanner scan cursor not save periodic`. This closes the bounded **source-level maintenance-progress checkpoint / effective-cadence** gap and corrects the earlier shortcut `configured save interval = effective periodic checkpoint`. Filesystem-specific power-loss durability, HDFS-12209 release/downstream genealogy, replay-cost measurement, earliest scanner genealogy, and fault injection remain open.

'''
roadmap = replace_once(roadmap, roadmap_marker, roadmap_bullet, 'ROADMAP Phase2 insertion')
write(roadmap_path, roadmap)

# 5. Update Case Index navigation row and append findings 2516-2530.
index_path = 'CASE_INDEX.md'
index = read(index_path)
lines = index.splitlines()
row_prefix = '| [Apache HDFS DataNode Block Scanner: Periodic Checksum Verification, Retained Scan Progress, and Corrupt-Replica Reporting]('
row_idxs = [i for i, line in enumerate(lines) if line.startswith(row_prefix)]
if len(row_idxs) != 1:
    raise RuntimeError(f'CASE_INDEX Case83 row count {len(row_idxs)}')
i = row_idxs[0]
row = lines[i]
old_tail = '[2003–2016 GFS/Apache grounding](evidence/83-hadoop-2003-2016-block-scanner-grounding.md); earliest HDFS scanner genealogy, cursor crash-atomicity, post-2.7 evolution, correlated-corruption analysis, and named-cluster fault validation remain separate work'
new_tail = '[2003–2016 GFS/Apache grounding](evidence/83-hadoop-2003-2016-block-scanner-grounding.md) + [2016 concurrent-append coherence deepening](evidence/83-hdfs-2016-volume-scanner-concurrent-append-coherence-deepening.md) + [cursor checkpoint / clock-domain deepening](evidence/83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md); earliest HDFS scanner genealogy, filesystem/power-loss cursor durability, HDFS-12209 release/downstream handling, post-2.7 evolution, correlated-corruption analysis, and named-cluster fault validation remain separate work'
if old_tail not in row:
    raise RuntimeError('CASE_INDEX Case83 expected tail not found')
lines[i] = row.replace(old_tail, new_tail)
index = '\n'.join(lines)

findings = r'''

## Case 83 deepening — HDFS BlockScanner cursor checkpoint / clock-domain findings

Evidence: [`evidence/83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md`](evidence/83-hdfs-blockscanner-cursor-checkpoint-clock-domain-deepening.md)

- **2516 — HDFS-7430 explicitly redesigns BlockScanner around O(1) last-scanned-position state rather than retaining scan status for all blocks.** The bounded historical witness is a 2014–2015 scanner rewrite, not an invention-priority claim for checkpoints or scrubbing. (`H/P`)
- **2517 — Hadoop 2.7.3 `BlockIteratorState` retains wall-clock save/start timestamps, current finalized directory/subdirectory/entry, and EOF state.** This is concrete maintenance-traversal state distinct from block payload and checksum content. (`H/P`)
- **2518 — The 2.7.3 cursor save path serializes to a temporary file and then requests `StandardCopyOption.ATOMIC_MOVE` to the live `.cursor`.** This grounds an atomic-path-replacement design, not a universal storage-stack durability guarantee. (`H/P`)
- **2519 — `ATOMIC_MOVE` request ≠ demonstrated sudden-power-loss durability.** The inspected save method does not itself establish file-data and parent-directory persistence under every filesystem/controller failure point; that requires separate platform evidence or experiment. (`E/X`)
- **2520 — A missing or unreadable saved cursor does not disable scanning in the bounded loader.** `enableBlockPoolId` falls back from failed `loadBlockIterator` to `newBlockIterator`, converting checkpoint loss into renewed traversal. (`H/P`)
- **2521 — Maintenance-progress loss can become repeated maintenance work without becoming payload loss.** Fresh-iterator fallback can rescan earlier entries; because scanner I/O is rate-limited, replay can still delay later integrity renewal. (`E`)
- **2522 — A saved scanner cursor is not a per-block verification-success ledger.** Iterator position can advance independently of the separate scan-error/reporting outcome, so `cursor after B` does not prove `B passed verification`. (`E`)
- **2523 — `cursor at EOF` ≠ `zero scan errors`.** Traversal completion and integrity outcomes are separate retained/operational relations. (`E`)
- **2524 — Hadoop 2.7.3 defines an internal cursor-save interval with a ten-minute default.** This is configuration/policy evidence, not by itself evidence that the interval-triggered checkpoint executes effectively. (`H/P`)
- **2525 — The 2.7.3 interval condition compares `Time.monotonicNow()` with `lastSavedMs` recorded by `Time.now()` and explicitly documented as epoch wall-clock time.** The two timestamps do not share the intended elapsed-time domain. (`H/P`)
- **2526 — Apache HDFS-12209 records the consequence as `VolumeScanner scan cursor not save periodic`.** Therefore `configured periodic-save branch` must be separated from `effective periodic checkpoint cadence`. (`H/P`, `E`)
- **2527 — EOF save, orderly-shutdown save, and interval-triggered in-pass save are three different checkpoint events.** Failure of the interval branch does not erase the existence of the other two save paths. (`H/P`, `E`)
- **2528 — Restart continuity ≠ exactly-once maintenance traversal.** A stale or missing cursor can replay verification work; that is different from rolling back user payload or repairing it. (`E`)
- **2529 — A 9-Sep-2026 inspection of Apache Hadoop `trunk` still shows the wall-clock `lastSavedMs` / monotonic `saveDelta` pattern.** This is only a current-source continuity witness, not a claim about every release or downstream distribution. (`H/P*`, `X`)
- **2530 — HDFS cursor checkpointing and Kafka leader-epoch checkpointing are only functionally analogous as retained non-payload control state.** HDFS can reconstruct scanner progress by replaying traversal after cursor-load failure; Kafka Case 90's epoch checkpoint participates in log-lineage and safe-truncation authority. Similar persistence form does not imply the same correctness role or genealogy. (`A`, `X`)
'''
if '## Case 83 deepening — HDFS BlockScanner cursor checkpoint / clock-domain findings' in index:
    raise RuntimeError('CASE_INDEX findings section already exists')
index = index.rstrip() + findings.rstrip() + '\n'
write(index_path, index)

# 6. Canonical validation.
for p in [EVIDENCE_PATH, case_path, base_path, roadmap_path, index_path]:
    if not (ROOT / p).is_file():
        raise RuntimeError(f'missing canonical file {p}')

# Findings must each occur exactly once in CASE_INDEX.
index_check = read(index_path)
for n in range(2516, 2531):
    hits = len(re.findall(rf'\b{n}\b', index_check))
    if hits != 1:
        raise RuntimeError(f'finding {n}: expected once, got {hits}')

# Strong guardrails against reintroducing the corrected overclaim.
case_check = read(case_path)
if 'The iterator is also saved at the end of a block-pool pass and at configured intervals during a pass.' in case_check:
    raise RuntimeError('old periodic-save overclaim remains in Case83')
if 'configured cursor-save interval ≠ effective periodic cursor checkpointing' not in case_check:
    raise RuntimeError('Case83 checkpoint guardrail missing')
if 'HDFS-12209' not in read(EVIDENCE_PATH):
    raise RuntimeError('new evidence missing HDFS-12209')

subprocess.run(['git', 'diff', '--check'], check=True)
print('Case 83 cursor checkpoint integration validated')
