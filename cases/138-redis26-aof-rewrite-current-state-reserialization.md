# Redis 2.6 AOF Rewrite: Current-State Re-serialization, Concurrent Delta Capture, and Log Replacement

## Status

**`grounded`** — bounded to Redis tag `2.6.0` (annotated 22 October 2012, pointing to commit `5eec376c2f56dbf617cc8bc19476fd5431cd664d`) and the checked-in `src/aof.c` / `redis.conf` implementation and configuration documentation.

Grounding record: [`../evidence/138-redis26-aof-rewrite-grounding.md`](../evidence/138-redis26-aof-rewrite-grounding.md).

Automatic-rewrite genealogy deepening: [`../evidence/138-redis-2011-2012-auto-aof-rewrite-genealogy-deepening.md`](../evidence/138-redis-2011-2012-auto-aof-rewrite-genealogy-deepening.md).

This case does **not** claim that Redis invented append-only persistence, command logging, log compaction, snapshotting, fork-based persistence, or atomic file replacement. It uses Redis 2.6.0 as a bounded released implementation in which the relation between append history, reconstructed current state, concurrent change capture, replacement authority, and durability policy is unusually explicit.

## Scope

The repository already has several ways of discarding history while preserving recoverability:

- Case 42: Kafka 0.8.1 keyed log compaction keeps at least the latest keyed value while preserving logical offsets;
- Case 57: Bigtable materializes current tablet state into SSTables and advances redo points;
- Case 58: Raft snapshots committed applied state and can discard a covered log prefix;
- Case 137: LevelDB keeps a user WAL separate from a MANIFEST log that reconstructs current SSTable membership.

Redis 2.6.0 supplies a different mechanism:

> **The AOF is replayable command history, but AOF rewrite does not need to preserve that command history. The rewrite child walks the current in-memory dataset and emits a new command sequence sufficient to reconstruct that state. While the child works, the parent separately accumulates post-fork changes; after successful child completion, those differences are appended to the replacement AOF before the file is switched into the configured AOF name.**

The bounded retention question is:

> When an append log is used to reconstruct current state, which parts of the old operation sequence must remain, which may be replaced by an equivalent state-producing representation, and what bridge state is needed so concurrent mutations are not lost while the replacement is constructed?

This case is not a general Redis persistence history and does not cover Redis 7 multipart AOF semantics except as explicitly excluded later evolution.

## Historical vocabulary

The inspected Redis 2.6.0 artifacts use:

- `Append Only File` / `AOF`;
- `append only log`;
- `appendonly`;
- `appendfsync`;
- `REWRITEAOF`;
- `BGREWRITEAOF`;
- `AOF rewrite`;
- `background append only file rewriting`;
- `AOF rewrite buffer`;
- `temporary AOF`;
- `differences`;
- `current size`;
- `rewrite base size`;
- `auto-aof-rewrite-percentage`;
- `auto-aof-rewrite-min-size`;
- `PEXPIREAT`;
- `current dataset` / dataset-rebuilding language in source comments.

`current-state re-serialization`, `concurrent delta bridge`, `replacement authority`, and `history-equivalence boundary` below are **project engineering terms**, not Redis 2.6 historical vocabulary.

## Historical record

### H/P — Redis 2.6.0 is a dated released implementation floor, not an invention claim

The official Redis Git tag `2.6.0` is an annotated tag dated 22 October 2012 and points to commit `5eec376c2f56dbf617cc8bc19476fd5431cd664d`.

The bounded source references below are therefore tied to one released tree rather than to current Redis behavior.

**Primary anchor:** Redis repository, annotated tag `2.6.0`.

### H/P — AOF startup recovery replays commands to reconstruct the dataset

`loadAppendOnlyFile()` opens the append log, parses command records, looks up each command, and executes it using a synthetic/fake client while temporarily disabling AOF feeding.

The retained AOF is therefore not merely an opaque byte archive in this implementation. Its recovery function depends on the command stream remaining parseable and executable enough to reconstruct Redis state.

**Primary anchor:** Redis 2.6.0 `src/aof.c`, `loadAppendOnlyFile()`.

### H/P — rewrite is generated from current in-memory state rather than by filtering the old AOF

The source comment above `rewriteAppendOnlyFile()` describes its job as writing a sequence of commands able to fully rebuild the dataset. The function iterates each database dictionary and emits rebuilding commands according to object type:

- strings become `SET`;
- lists are emitted through list-rebuild commands;
- sets through `SADD`;
- sorted sets through `ZADD`;
- hashes through `HMSET`;
- expiration state is emitted separately.

The routine does not read the old AOF and select a surviving subset of its records. It materializes a replacement command stream from the **current dataset representation**.

**Primary anchor:** Redis 2.6.0 `src/aof.c`, `rewriteAppendOnlyFile()` and the object-specific rewrite helpers.

### H/P — expiration state is normalized during rewrite

For ordinary AOF feeding, relative expiration commands such as `EXPIRE`, `PEXPIRE`, `SETEX`, and `PSETEX` are translated into absolute `PEXPIREAT` state before being appended. The source comment explicitly says this keeps the time absolute rather than relative.

During AOF rewrite, keys with an expiration are also represented with `PEXPIREAT`; a key already expired relative to the rewrite's current time is skipped.

This is direct evidence that a replacement AOF need not preserve the exact historical command form that originally produced the current expiration relation.

**Primary anchor:** Redis 2.6.0 `src/aof.c`, `catAppendOnlyExpireAtCommand()`, `feedAppendOnlyFile()`, and `rewriteAppendOnlyFile()`.

### H/P — background rewrite splits work into a fork-time base and a parent-held difference stream

The source's own background-rewrite comment gives the sequence:

1. `BGREWRITEAOF` causes a `fork()`;
2. the child rewrites the dataset into a temporary AOF;
3. the parent accumulates differences while the child works;
4. after successful child completion, the parent appends the accumulated differences to the temporary file;
5. the temporary file is renamed to the configured AOF name and becomes the file used for later appends.

`feedAppendOnlyFile()` independently confirms that while `server.aof_child_pid != -1`, generated AOF command bytes are appended to `aofRewriteBufferAppend()` in addition to their ordinary AOF role when AOF is active.

**Primary anchors:** Redis 2.6.0 `src/aof.c`, `rewriteAppendOnlyFileBackground()`, `feedAppendOnlyFile()`, and `backgroundRewriteDoneHandler()`.

### H/P — child rewrite completion is not yet replacement-AOF completion

When the child exits successfully, `backgroundRewriteDoneHandler()` still has several steps to perform:

- open the child-produced temporary AOF;
- append the parent's rewrite buffer;
- rename the temporary AOF to the configured AOF filename;
- switch `server.aof_fd` to the new file when AOF is enabled;
- reset rewrite bookkeeping.

A child that successfully serialized its fork-time dataset has therefore not by itself produced the final authoritative AOF for the concurrently changing server.

**Primary anchor:** Redis 2.6.0 `src/aof.c`, `backgroundRewriteDoneHandler()`.

### H/P — failed rewrite does not intentionally replace the old AOF

If the child exits with an error or signal, the handler marks the rewrite status as an error and cleans up the temporary file/buffer rather than switching the configured AOF to that incomplete product. Rename failure likewise follows the cleanup path.

This is a bounded application-level failure property: **failed rewrite attempts are designed not to make the failed replacement authoritative**.

It is not a universal claim about every possible filesystem, kernel, or storage-device crash during the rename/switch sequence.

**Primary anchor:** Redis 2.6.0 `src/aof.c`, `backgroundRewriteDoneHandler()`.

### H/P — AOF rewrite scheduling is based on physical/log-file growth, not a retention-age deadline

The 2.6.0 `redis.conf` says Redis remembers the AOF size after the latest rewrite, or the startup size if no rewrite has happened since restart. Automatic rewrite compares current AOF size with that base and triggers when the configured percentage growth and minimum-size conditions are met.

The shipped example defaults are:

- `auto-aof-rewrite-percentage 100`;
- `auto-aof-rewrite-min-size 64mb`.

A percentage of zero disables automatic rewrite.

**Primary anchor:** Redis 2.6.0 `redis.conf`, `Automatic rewrite of the append only file`.

### H/P — append durability policy is separately configurable from rewrite policy

The same 2.6.0 configuration exposes three AOF synchronization policies:

- `appendfsync no`;
- `appendfsync everysec`;
- `appendfsync always`.

The default shown is `everysec`.

Separately, `no-appendfsync-on-rewrite` can suppress main-process fsync while `BGSAVE` or `BGREWRITEAOF` is performing heavy I/O. The checked-in documentation warns that enabling this option weakens durability during the background operation and, under the stated default Linux assumptions, can expose a substantially larger loss window.

This directly establishes that **rewrite/compaction maintenance policy and write-durability policy are distinct controls that can interact**.

**Primary anchors:** Redis 2.6.0 `redis.conf`; `src/aof.c`, `flushAppendOnlyFile()`.

## Retained state

At least seven distinct state classes matter in this bounded mechanism.

### 1. Current in-memory dataset

This is the live Redis key/value/object state from which the rewrite child constructs its base replacement AOF.

It is not identical to the old AOF's complete command sequence.

### 2. Existing authoritative AOF

Before successful replacement, the configured AOF remains the ordinary recovery history and receives normal appends while AOF is active.

### 3. Temporary rewritten base AOF

The child serializes a fork-time view of current dataset state into a temporary file.

Physical existence of this file does not yet make it the configured recovery authority.

### 4. Parent rewrite-difference buffer

Commands generated after the fork are accumulated in `server.aof_rewrite_buf_blocks` while the child works.

This is transaction-specific bridge state between the child base and the later live state. It is not a second complete database or a complete historic AOF.

### 5. Ordinary AOF write buffer / sync state

`server.aof_buf`, file descriptor state, fsync timing, and background-fsync state govern ordinary append persistence.

These have a different role from the rewrite-difference buffer even though some generated command bytes can feed both paths.

### 6. Rewrite scheduling/accounting state

`aof_rewrite_base_size`, current AOF size, configured percentage/minimum thresholds, child PID, scheduled flag, and last rewrite status determine whether work is due/in progress and how its result is classified.

These are maintenance-control state, not application payload.

### 7. Expiration relation

Current expiration deadlines are reconstructed as absolute expiration times. The useful retained relation is the deadline attached to the current key, not preservation of the exact sequence of earlier relative-expiration commands.

## Engineering reconstruction

### Append history != current dataset

An append-only command history can contain many operations whose cumulative effect is one small current state. Redis 2.6 rewrite proves this operationally by rebuilding the replacement AOF from the dataset rather than requiring the full old command sequence.

> **operation-history retention is stronger than current-state reconstructability.**

### AOF rewrite != old-log record filtering

Kafka Case 42 selects surviving keyed records from a log while retaining their logical offsets. Redis 2.6 takes a different route: it walks current state and emits a fresh recovery program.

> **log compaction can mean current-state re-serialization rather than selecting records from the old log.**

`compaction` here is a project comparison term; the historical Redis term is `rewrite`.

### Exact command-history identity != recovery-state equivalence

The replacement may use commands different from the original mutation sequence. Multiple historical updates can collapse into one state-producing command, and expiration commands are normalized into absolute `PEXPIREAT`.

The recovery requirement in this bounded path is therefore not “replay exactly the same event sequence.” It is “execute a replacement sequence that reconstructs the intended current state closely enough for Redis's recovery contract.”

### Fork-time base != final concurrent state

The child starts from a process snapshot created by `fork()`. Writes can continue in the parent.

> **a consistent-enough base representation can become stale while it is being serialized.**

This creates the need for bridge state rather than proving the rewrite is already current.

### Concurrent delta bridge != base representation

The rewrite buffer carries changes that occur after the child snapshot. It is needed because neither the fork-time base nor the old AOF alone is the final replacement artifact being built.

> **replacement construction can require retaining the difference between a frozen reconstruction base and ongoing live mutation.**

### Same command bytes != same retention role

A newly executed write can be represented in the ordinary AOF path and also copied into the rewrite-difference buffer during BGREWRITEAOF.

The byte encoding may match while the state role differs:

- one contributes to the currently authoritative append history;
- the other is temporary handoff state needed to close the replacement gap.

### Rewritten base complete != authoritative replacement

Successful child serialization still precedes parent-delta append and rename/file-descriptor switch.

> **representation completeness for one snapshot != current recovery authority.**

### BGREWRITEAOF admission/scheduling != rewrite completion

The command can start or schedule background work; the process later reports success/error and performs the switch.

> **maintenance request accepted != maintenance result installed.**

### Rewrite failure != automatic loss of the old recovery representation

The failure path deliberately retains the previous AOF as the active artifact rather than promoting the failed temporary file.

This protects against one class of maintenance failure but does **not** prove that unrelated recent writes were durable under the selected `appendfsync` policy.

### AOF-file growth != logical-dataset growth

Repeated updates to the same keys can grow append history without proportionally increasing current logical state.

The automatic rewrite trigger therefore responds to **history-carrier growth**, not directly to current dataset size or medium-retention decay.

### Rewrite trigger != payload-retention deadline

`auto-aof-rewrite-percentage` and minimum file size are space/history-amplification maintenance controls. They are not evidence that a key/value becomes unreadable after a time interval.

### Rewrite policy != fsync durability policy

Redis can choose when to rewrite the AOF independently of whether appends are synchronized `always`, `everysec`, or left to the OS.

> **history compaction and persistence-boundary cadence are orthogonal controls.**

### Background maintenance can change durability exposure

The optional `no-appendfsync-on-rewrite yes` setting trades lower rewrite-time latency/blocking against weaker synchronization during heavy background persistence work.

Maintenance therefore need not be a neutral background process with respect to the retention guarantees of new foreground mutations.

### Relative command history != retained absolute expiration relation

Converting relative expiration commands to `PEXPIREAT` preserves an absolute deadline relation for replay while discarding the original relative-command form.

This is not complete temporal history. It is a current/recovery representation of one time-dependent state relation.

### Rename/switch intent != universal crash-durability theorem

Redis 2.6 comments describe rename as the atomic switch mechanism and fsync the temporary AOF before rename. Case 124 shows why that application sequence must not be inflated into a proof that the new pathname binding is crash-durable across every filesystem, controller, and power-failure model.

The exact source sequence is historical evidence; universal crash closure would require a separate fault model and lower-layer evidence.

### Old-AOF retirement != media sanitization

After a successful switch the old file may be unlinked/closed and cease to be Redis's active AOF.

That does not establish overwrite, Flash block erase, cryptographic erasure, or forensic disappearance of the old bytes.

## Functional analogies and limits

### A — Redis AOF rewrite vs Kafka Case 42 log compaction

Both mechanisms can preserve a current-state reconstruction capability while discarding some detailed historical redundancy.

But the bounded mechanisms differ sharply:

- **Kafka 0.8.1:** scans keyed log state, retains latest-per-key records, preserves logical offsets, and leaves a sparse ordered log.
- **Redis 2.6.0:** walks the current in-memory dataset, generates a new recovery command sequence, and does not preserve the old AOF's record positions as a stable logical coordinate system.

This is a functional comparison, not genealogy.

### A — Redis AOF rewrite vs LevelDB Case 137

Both use staged replacement and delay retirement of an older authoritative representation until a new relation is ready.

But:

- LevelDB's MANIFEST is metadata history selecting immutable SSTable membership while recent user mutations are in separate `*.log` files;
- Redis's AOF is itself a replayable user-command recovery representation, and rewrite derives a compact replacement from current in-memory dataset state plus concurrent deltas.

`log`, `manifest`, `rewrite`, and `compaction` are not interchangeable historical categories.

### A — Redis AOF rewrite vs Bigtable/Raft materialization

Bigtable minor compaction and Raft snapshotting also permit older detailed history to become dispensable after a replacement state relation exists.

The similarity is only the abstract retention function:

> **current-state continuation can survive deliberate reduction of the historical path that produced it.**

The authorization rules, fault models, replay boundaries, distributed consensus requirements, and physical embodiments remain different.

## Prior art and anti-anachronism

This case establishes only a conservative dated floor:

- Redis 2.6.0 publicly contains the bounded AOF rewrite/replay/delta/switch behavior by 22 October 2012;
- the configuration itself says automatic AOF rewriting already exists as a product feature in this released tree;
- current Redis documentation reports older feature availability, but those later pages are not used here to claim exact first invention or every earlier implementation detail.

Do **not** infer:

- that Redis invented command logging;
- that Redis invented append-only persistence;
- that Redis invented state-based log rewrite;
- that the 2.6 implementation equals Redis 7 multipart AOF;
- that a source comment calling rename atomic proves full end-to-end crash durability;
- that rewritten-away historical commands are securely erased.

Exact first-introduction genealogy for AOF/BGREWRITEAOF/automatic rewrite, earlier database logging/checkpoint precedents, and later Redis persistence evolution belong primarily in `computing-archaeology` if developed.



## Historical deepening — manual rewrite vs automatic rewrite policy, 2011 to Redis 2.4

The companion 2011–2012 evidence closes one of this case's original genealogy debts without turning the case into a general Redis history.

Released Redis **2.2.0** (22 February 2011) already contains `bgrewriteaofCommand()` and `rewriteAppendOnlyFileBackground()`. Its configuration tells operators to use `BGREWRITEAOF` when an append log becomes too large, but the released tree does not expose the later automatic-rewrite percentage/minimum-size policy.

On **10 June 2011**, public commit `b333e2399778e624174e00d123c2cb3785333e3d` adds automatic AOF rewrite as a policy layer: percentage/minimum-size configuration, remembered base/current AOF sizes, scheduled-rewrite state, and a `serverCron` trigger that can invoke the existing background rewrite path. The commit message itself calls this the first implementation and says it still needs testing.

The following public history matters methodologically. Within hours and days Redis fixes division-by-zero, option parsing, child-concurrency, and the growth formula; on **12 June 2011** commit `0b17517...` changes the calculation from current-size percentage to **growth above the remembered base**. On **9 August 2011**, `11aaf523...` widens the base arithmetic after an integer-overflow report. Released **2.4.0** (14 October 2011) contains the automatic-rewrite controls and guarded trigger.

This establishes a bounded chain:

> `manual/background rewrite mechanism exists` **before** `automatic rewrite policy exists`.

and:

> `maintenance threshold due != work admitted now != rewrite completed != replacement installed`.

The first inequality is grounded by the 2.2→June-2011 source history; the later phases remain grounded by this case's 2.6 handoff analysis. The retained base-size/current-size bookkeeping is maintenance-control state: small state about prior rewrite/startup history that governs a future large representation-maintenance action.

The chronology is not an invention-priority claim. It does not establish the first Redis AOF or `BGREWRITEAOF` commit, private experiments, or broader database checkpoint/log-compaction priority. Those broader questions still belong primarily in `computing-archaeology`.

## Philosophical interpretation — bounded

The technical fact that matters here is narrow:

> A system can continue to recover “the same current state” while deliberately abandoning the identity of the operation sequence that produced it.

Redis 2.6 AOF rewrite therefore makes one distinction concrete:

- **retention of recoverable state-equivalence**
- is not the same as
- **retention of historical event-sequence identity**.

The rewrite does not make history philosophically unreal, nor does it prove that all memory is reconstruction. It shows only that one technical persistence contract can choose a replacement representation whose legitimacy depends on what it reconstructs, not on preserving every prior inscription.

## Counterexamples / stop conditions

Keep the following explicit:

- AOF replay success does not imply complete historical fidelity.
- AOF rewrite success does not prove every recent write survived a power failure; `appendfsync` policy remains separate.
- A child rewrite completing does not mean the new AOF is current before parent differences are merged and authority is switched.
- A configured automatic-rewrite threshold is not a retention lifetime.
- Smaller AOF size is not proof of smaller logical dataset size.
- A rename-based application switch is not universal crash-durability evidence.
- Old-file logical retirement is not sanitization.
- Redis AOF rewrite is not Kafka keyed compaction, LevelDB MANIFEST recovery, Raft snapshotting, or Bigtable compaction.
- Redis 2.6 semantics must not be projected onto Redis 7 multipart AOF.

## Related repositories

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for Redis AOF / BGREWRITEAOF found no dedicated overlapping study.

Division of labor:

- **technical-retention:** keep the current-state/history/delta/replacement-authority/durability-policy comparison developed here;
- **computing-archaeology:** if pursued, recover the broader genealogy of Redis persistence, the earliest AOF/BGREWRITEAOF commits/releases, broader automatic-maintenance/database-checkpoint precedents, background-fork design constraints, RDB/AOF evolution, and Redis 7 multipart-AOF transition;
- **problem-history:** useful only if later work asks what problem Redis authors explicitly framed AOF rewrite as solving at different dates.

## Sources

### Primary

- Redis official repository, annotated tag `2.6.0` (22 October 2012): <https://github.com/redis/redis/releases/tag/2.6.0>
- Redis 2.6.0, `src/aof.c`: <https://github.com/redis/redis/blob/2.6.0/src/aof.c>
- Redis 2.6.0, `redis.conf`: <https://github.com/redis/redis/blob/2.6.0/redis.conf>

### Later first-party cross-check

- Redis documentation, persistence / AOF rewrite: <https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/>
- Redis command documentation, `BGREWRITEAOF`: <https://redis.io/docs/latest/commands/bgrewriteaof/>

The current documentation is useful for later continuity/evolution and feature-history pointers. The 2012 source tree remains the authority for the bounded implementation claims above.

## Next work

- locate and inspect the exact first public AOF/BGREWRITEAOF implementations rather than inferring them from later documentation;
- the bounded June-2011 -> Redis-2.4 automatic-rewrite introduction/release chain is now closed by the companion genealogy deepening; exact first AOF/BGREWRITEAOF implementation history remains open;
- compare 2.6 single-file rewrite with Redis 7 multipart AOF without back-projecting the later manifest/base/incremental structure;
- run crash/fault injection around child completion, parent-delta merge, rename, directory durability, and process/power interruption;
- compare rewrite amplification and recovery time empirically under update-heavy workloads;
- route broad database-log/checkpoint genealogy to `computing-archaeology`.
