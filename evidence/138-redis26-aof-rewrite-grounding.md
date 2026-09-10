# Redis 2.6 AOF Rewrite Grounding Record

## Scope

This evidence record grounds Case 138:

[`../cases/138-redis26-aof-rewrite-current-state-reserialization.md`](../cases/138-redis26-aof-rewrite-current-state-reserialization.md)

The bounded object is Redis **2.6.0**, specifically the released `src/aof.c` and `redis.conf` behavior surrounding:

- AOF command replay;
- AOF rewrite from current in-memory state;
- fork-time background rewrite;
- parent-side concurrent-difference buffering;
- replacement-file handoff;
- automatic rewrite scheduling;
- AOF fsync policy.

The purpose is **not** to establish invention priority or a complete Redis persistence genealogy. The evidence supports a retention-specific distinction among operation history, current-state reconstructability, temporary bridge state, replacement authority, and durability policy.

## Evidence labels

- `H/P` — direct historical / primary-source claim from the bounded released Redis tree;
- `E` — engineering reconstruction from the inspected mechanism;
- `A` — functional comparison to another repository case;
- `X` — claim explicitly not established.

## Artifact identity

### H/P — annotated Redis `2.6.0` tag

The official Redis repository exposes an annotated `2.6.0` tag:

- tag object: `9784aba434972aa5257787ccbce0cd15c1fe28b9`;
- tagger: `antirez`;
- tag date: **2012-10-22T21:27:28Z**;
- tag message: `Redis 2.6.0`;
- target commit: `5eec376c2f56dbf617cc8bc19476fd5431cd664d`.

Primary record:

- <https://github.com/redis/redis/releases/tag/2.6.0>
- Git ref/tag data in the official repository.

This is used only as a released-implementation floor.

**X:** `2.6.0 tag date = invention date`.

## Source 1 — `src/aof.c`: ordinary AOF replay

Primary artifact:

- <https://github.com/redis/redis/blob/2.6.0/src/aof.c>
- function: `loadAppendOnlyFile()`.

### H/P — AOF is executable recovery history

The loader:

1. opens the configured append log;
2. parses Redis protocol command records;
3. creates a fake client;
4. looks up each command;
5. invokes the command procedure on that fake client;
6. temporarily disables AOF feeding so recovery execution does not append the same commands back into the file.

This directly grounds:

> `AOF bytes physically present` is not sufficient by itself; startup reconstruction depends on a parseable/executable command relation.

It also grounds the historical use of replay as the recovery mechanism for the AOF.

### X — replay mechanism does not prove perfect historical archive semantics

Executing a command stream to reconstruct current state does not establish that the file is intended as a permanent audit trail, nor that later rewrite preserves every command event.

## Source 2 — `src/aof.c`: rewrite from current dataset

Primary artifact:

- same file;
- function: `rewriteAppendOnlyFile()`;
- helpers: `rewriteListObject()`, `rewriteSetObject()`, `rewriteSortedSetObject()`, `rewriteHashObject()`.

### H/P — replacement sequence is generated from current in-memory state

The source comment states that the function writes a sequence of commands able to fully rebuild the dataset.

The implementation iterates each Redis DB dictionary and emits reconstruction commands by current object type. It does not open or scan the old AOF as the input to the rewrite algorithm.

Examples in the bounded source:

- current string -> `SET`;
- current list -> `RPUSH` reconstruction;
- current set -> `SADD`;
- current sorted set -> `ZADD`;
- current hash -> `HMSET`.

### E — old operation sequence is not the retained invariant of rewrite

Because the algorithm starts from current dataset objects, many historical command sequences can map to one replacement sequence.

The protected relation is current-state reconstructability, not event-sequence identity.

### X — this is not Kafka-style record selection

Nothing in this source supports describing 2.6 AOF rewrite as “keep the latest old AOF record for each key while preserving log offsets.” That is a different mechanism from Kafka Case 42.

## Source 3 — expiration normalization

Primary artifact:

- same file;
- functions: `catAppendOnlyExpireAtCommand()`, `feedAppendOnlyFile()`, `rewriteAppendOnlyFile()`.

### H/P — relative expiry operations are encoded as absolute `PEXPIREAT`

The source explicitly converts several expiration command forms to absolute millisecond timestamps before AOF append.

During rewrite, current keys with expiry state are emitted using `PEXPIREAT`; already-expired keys are omitted.

This grounds:

- current expiry relation can survive while original relative command form does not;
- replacement history can normalize operation representation;
- expired state need not remain as a historic command merely because it once occurred.

### X — absolute deadline representation != complete time history

`PEXPIREAT` preserves the current deadline relation needed for replay. It does not record every earlier TTL change or explain why that deadline was chosen.

## Source 4 — `feedAppendOnlyFile()`: dual role during rewrite

Primary artifact:

- same file;
- function: `feedAppendOnlyFile()`.

### H/P — post-fork command bytes feed the rewrite-difference buffer

The function first builds the command representation for an executed mutation.

- when ordinary AOF is on, it appends those bytes to `server.aof_buf`;
- when a background AOF child exists, it also appends the bytes to the AOF rewrite buffer.

This is primary evidence for one mutation representation participating in two different state roles during the handoff.

### E — same encoding != same retention role

The ordinary AOF path protects the currently authoritative recovery stream according to its write/fsync policy.

The rewrite buffer is temporary bridge state needed to bring the child-produced fork-time base forward to the parent state before authority switches.

The same command bytes do not collapse those roles.

## Source 5 — background rewrite protocol

Primary artifact:

- same file;
- functions: `rewriteAppendOnlyFileBackground()` and `backgroundRewriteDoneHandler()`.

### H/P — fork-time base plus parent differences

The source comment itself enumerates the background-rewrite design:

- fork child;
- child writes a temporary AOF;
- parent accumulates differences;
- parent appends those differences after child completion;
- parent renames/switches the replacement file.

The completion handler independently implements that sequence.

### H/P — successful child exit precedes authoritative replacement

On child success the parent must still:

1. open the temporary result;
2. write the rewrite buffer into it;
3. rename it to the configured AOF filename;
4. switch the live AOF descriptor if AOF is enabled.

Therefore:

> `child finished rewriting fork-time state != replacement AOF current`.

### H/P — error path avoids installing a failed result

Child error/signal and temporary-file/merge/rename errors do not intentionally promote the failed product as the configured AOF.

Cleanup resets rewrite state and removes the temporary rewrite file.

### X — application switch protocol != universal crash theorem

The source comments describe rename as the atomic switch, but this artifact does not prove directory-entry durability under every filesystem, kernel, controller cache, or power-loss model.

Case 124 remains the repository boundary for rename/fsync durability closure.

## Source 6 — `src/aof.c`: rewrite output synchronization and rename

Primary artifact:

- same file;
- `rewriteAppendOnlyFile()`.

### H/P — temporary rewritten output is flushed/synced before local rename

The synchronous rewrite function:

- flushes stdio;
- calls the AOF fsync abstraction;
- closes the file;
- renames the temporary path to the final destination.

The background path similarly produces a temporary file before later parent-side handoff.

This is evidence of the application protocol Redis 2.6 intended.

### X — synced file content != durable pathname binding under every crash model

The inspected source does not establish all lower-layer conditions needed for that stronger claim.

## Source 7 — `redis.conf`: ordinary AOF durability modes

Primary artifact:

- <https://github.com/redis/redis/blob/2.6.0/redis.conf>
- section: `APPEND ONLY MODE`.

### H/P — write durability is separately configurable

Redis 2.6.0 documents:

- `appendfsync no`;
- `appendfsync always`;
- `appendfsync everysec`.

The checked-in default is `everysec`.

The source/config discussion treats this as a speed/data-safety choice.

This grounds:

> `AOF is being rewritten` and `how foreground AOF writes cross an fsync boundary` are separate policy axes.

## Source 8 — `redis.conf`: rewrite-time durability interaction

Primary artifact:

- same configuration file;
- `no-appendfsync-on-rewrite`.

### H/P — background persistence work can alter foreground durability exposure

The configuration explains that heavy `BGSAVE`/AOF rewrite I/O can cause blocking and offers an option to suppress fsync calls while such background work runs.

It explicitly warns that, when enabled, durability during that interval falls to the `appendfsync none` class and gives a worst-case loss-window example under the stated Linux assumptions.

This is unusually direct evidence that maintenance work can change the operating retention envelope of concurrent new writes.

### X — warning is not a measured universal loss distribution

The configured warning is a design/operational statement under specified assumptions. It does not establish that every platform loses exactly that amount or that every rewrite causes loss.

## Source 9 — `redis.conf`: automatic rewrite trigger

Primary artifact:

- same configuration file;
- `auto-aof-rewrite-percentage`;
- `auto-aof-rewrite-min-size`.

### H/P — trigger is based on growth relative to remembered base size

The configuration says Redis remembers AOF size after the latest rewrite, or startup size if no rewrite has occurred since restart.

Automatic rewrite is triggered only when:

- current size grows by the configured percentage relative to that base; and
- current size meets the configured minimum.

The example defaults are 100% growth and 64 MB minimum. Percentage zero disables automatic rewrite.

### E — carrier-growth maintenance != payload-aging maintenance

The trigger measures growth of the recovery-history carrier, not elapsed lifetime of keys and not physical medium decay.

`AOF grew enough to rewrite` therefore cannot be translated into `payload has aged enough to refresh`.

## Cross-case evidence discipline

### A — Kafka Case 42

Shared function:

- reduce detailed retained history while preserving current-state reconstruction.

Mechanism difference:

- Kafka 0.8.1 cleans old segments by keyed latest-offset logic and keeps stable logical offsets;
- Redis 2.6.0 reconstructs a new command stream from current in-memory state plus concurrent parent differences.

**X:** shared “log compaction” function proves genealogy.

### A — LevelDB Case 137

Shared function:

- construct a replacement representation and delay old-state retirement until a new authority relation is ready.

Mechanism difference:

- LevelDB MANIFEST is file-membership metadata history separate from user WAL;
- Redis AOF is replayable user-command recovery history, and rewrite derives a state-equivalent replacement from live dataset contents.

**X:** `MANIFEST log = Redis AOF`.

### A — Bigtable / Raft

Shared function:

- a state/materialization boundary can make older detailed history dispensable.

**X:** shared function implies identical replay, consensus, or crash semantics.

## Related-repository check

A fresh GitHub code search in `tmzncty/computing-archaeology` for:

- `Redis AOF`;
- `BGREWRITEAOF`;
- `append only rewrite`

returned no dedicated overlapping research module in the currently indexed repository.

Therefore this case keeps the retention-specific relation here while routing broader Redis persistence genealogy to `computing-archaeology`.

## Claim ledger

| Claim | Label | Evidence strength | Boundary |
| --- | --- | --- | --- |
| Redis 2.6.0 released tree contains the inspected AOF behavior | `H/P` | strong | released floor, not invention |
| AOF recovery replays command records | `H/P` | strong | executable reconstruction, not audit guarantee |
| rewrite walks current dataset rather than old AOF records | `H/P` | strong | bounded to 2.6 source |
| expiration representation is normalized to absolute deadlines | `H/P` | strong | not complete TTL history |
| child rewrite and parent delta capture are separate phases | `H/P` | strong | fork-based 2.6 mechanism |
| successful child result is not current until merge/switch | `H/P`, `E` | strong | exact authority handoff |
| failure does not intentionally install failed replacement | `H/P` | strong | not a universal power-cut theorem |
| auto rewrite is growth/min-size triggered | `H/P` | strong | not time/retention deadline |
| fsync policy is separate from rewrite policy | `H/P`, `E` | strong | lower device still separate |
| rewrite-time option can weaken durability exposure | `H/P`, `E` | strong | config warning, not universal measured loss |
| rewrite preserves state-equivalence rather than event-sequence identity | `E` | strong reconstruction | bounded to represented Redis state |
| Kafka/LevelDB/Bigtable/Raft comparisons are functional only | `A`, `X` | strong boundary | no genealogy |

## Remaining evidence gaps

1. Exact first public AOF and BGREWRITEAOF commits/releases.
2. Exact first automatic-rewrite implementation and its 2.4 release genealogy.
3. Direct source-to-source comparison with Redis 7 multipart AOF.
4. Power-cut/process-kill fault injection at:
   - child temp-file completion;
   - parent delta append;
   - rename;
   - live descriptor switch;
   - directory persistence.
5. Empirical rewrite amplification/recovery-time measurements.
6. Broader database command-log/state-rewrite prior art.

None of these gaps blocks the bounded 2.6.0 mechanism claims above.
