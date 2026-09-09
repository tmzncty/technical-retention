# Case 83 deepening — HDFS BlockScanner cursor checkpointing, restart continuity, and the clock-domain boundary

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
