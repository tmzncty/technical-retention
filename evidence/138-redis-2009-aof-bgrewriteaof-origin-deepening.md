# Redis 2009 AOF / BGREWRITEAOF Public-Implementation Origin Deepening

## Scope

This record closes a narrow chronology debt left open by Case 138 and the later 2011–2012 automatic-rewrite genealogy: **when can the public Redis repository first be shown to contain the append-only write path, and when can it first be shown to contain the background AOF rewrite mechanism?**

The answer is intentionally bounded to the public `redis/redis` repository history inspected here. It is not an invention-priority claim for append-only logging, command logging, log compaction, snapshotting, fork-based persistence, or atomic replacement, and it does not exclude private branches, unpublished experiments, imported patches, or older mechanisms in other systems.

Case: [`../cases/138-redis26-aof-rewrite-current-state-reserialization.md`](../cases/138-redis26-aof-rewrite-current-state-reserialization.md)

Later automatic-policy genealogy: [`138-redis-2011-2012-auto-aof-rewrite-genealogy-deepening.md`](138-redis-2011-2012-auto-aof-rewrite-genealogy-deepening.md)

## Evidence labels

- `H/P` — direct historical / primary evidence from the official Redis repository history;
- `E` — engineering reconstruction from those artifacts;
- `A` — bounded functional comparison;
- `X` — claim explicitly not established.

## Source 1 — 30 October 2009: append-only write serialization appears before replay support

### H/P — explicit initial implementation commit

Official Redis commit `44b38ef43259e8805b01db01ad9a1c67479c6194`, authored **2009-10-30T01:04:17+01:00**, is titled `Initial implementation of append-only mode. Loading still not implemented.`

Primary record:

- <https://github.com/redis/redis/commit/44b38ef43259e8805b01db01ad9a1c67479c6194>

The patch adds the server's append-only enable/file state, opens an append file, adds `feedAppendOnlyFile()`, and serializes processed commands into the append file. The same commit message explicitly says loading is not yet implemented.

This is the earliest public repository commit located in this audit that explicitly identifies itself as the initial append-only implementation. That wording is a repository-history lower bound, not a claim about global invention priority.

### H/P — the configuration described an intended startup-rebuild contract before that contract was implemented

The same commit adds `redis.conf` prose saying the append-only file will be read at startup to rebuild the in-memory dataset, even though the commit message says loading is still absent from the implementation at that point.

This is useful historical evidence because documentation intent and executable recovery capability are temporarily out of phase in the same commit.

### H/P — replay matures in later public commits

On **2009-11-01**, commit `f80dff6212661a404c7c32c6741691b6255a4e31` adds a first append-only loading implementation while warning `STILL BROKEN don't use it`; ten minutes later, `9387d17dfeb757d685236ff5c792d102ea296631` is titled `append only file loading fixed`.

Primary records:

- <https://github.com/redis/redis/commit/f80dff6212661a404c7c32c6741691b6255a4e31>
- <https://github.com/redis/redis/commit/9387d17dfeb757d685236ff5c792d102ea296631>

These commits do not by themselves prove a released or production-mature persistence contract; they show public implementation maturation after the write path already existed.

## Source 2 — 26 November 2009: background AOF rewrite enters the public tree

### H/P — parent snapshot lacks the background-rewrite command/function

Commit `210e29f7d276be1bbbaf1b711b654dd6834f8e93`, authored **2009-11-24T20:44:20Z**, is the parent of the rewrite-introduction commit below. Its checked-in `redis.c` contains the ordinary append-only machinery but no `bgrewriteaofCommand` symbol.

Primary artifacts:

- <https://github.com/redis/redis/commit/210e29f7d276be1bbbaf1b711b654dd6834f8e93>
- <https://github.com/redis/redis/blob/210e29f7d276be1bbbaf1b711b654dd6834f8e93/redis.c>

This parent/child comparison is stronger than merely searching later documentation for the command name.

### H/P — `9d65a1...` introduces `BGREWRITEAOF` and its parent-delta handoff structure

Official Redis commit `9d65a1bbae9e59269472e8067cb2fff1e1cce24c`, authored **2009-11-26T17:10:02Z**, is titled `log rebuilding, random refactoring, work in progress please wait for an OK commit before to use this version`.

Primary record:

- <https://github.com/redis/redis/commit/9d65a1bbae9e59269472e8067cb2fff1e1cce24c>

Its patch adds, among other AOF-rebuild state:

- the `bgrewriteaof` command entry;
- `bgrewriteaofCommand()`;
- background-rewrite child state;
- a parent-side rewrite buffer;
- `backgroundRewriteDoneHandler()` logic for appending the parent's accumulated differences to the child-produced temporary AOF before replacement.

The companion `redis-cli.c` patch recognizes both `rewriteaof` and `bgrewriteaof`, while the server command table shown in this commit adds `bgrewriteaof`. The bounded claim here is therefore specifically about the public **background** rewrite mechanism evidenced by server code, not about a separately supported synchronous `REWRITEAOF` server command.

### H/P — introduction is explicitly work-in-progress, not a release/maturity date

The introduction commit itself says to wait for an `OK` commit before using that version. Later the same day, commit `85a831729fc5d38370b304dffee0fa381e27de42` is titled `append only file fixes`.

Primary record:

- <https://github.com/redis/redis/commit/85a831729fc5d38370b304dffee0fa381e27de42>

Accordingly, `2009-11-26` is used here as a public implementation boundary for the mechanism, not as a claim that a stable release contract was already established at the first commit.

### H/P — by 12 December 2009 BGREWRITEAOF has explicit observability state

Commit `b3fad521cc3752b48fdf43c10237527ea2a99d5b`, authored **2009-12-12T21:41:10Z**, is titled `bgrewriteaof_in_progress added to INFO`.

Primary record:

- <https://github.com/redis/redis/commit/b3fad521cc3752b48fdf43c10237527ea2a99d5b>

Its parent already contains `bgrewriteaofCommand()` and `rewriteAppendOnlyFileBackground()`. This later commit is therefore an observability addition, not the origin of BGREWRITEAOF.

## Source 3 — 2011 policy layer is later than the 2009 mechanism

The companion Evidence 138B establishes that released Redis 2.2.0 already had manual/background rewrite, while commit `b333e2399778e624174e00d123c2cb3785333e3d` on **2011-06-10** added the first bounded public automatic-rewrite policy implementation later released in the Redis 2.4 line.

The chronology can therefore be stated conservatively as:

`2009-10-30 append serialization` → `2009-11-01 replay/loading maturation` → `2009-11-26 background rewrite mechanism` → `2011-06-10 automatic rewrite policy layer` → `2011-10-14 Redis 2.4.0 release` → `2012-10-22 grounded Redis 2.6.0 implementation`.

This chain is repository genealogy for Redis, not genealogy for log compaction as a general computing technique.

## Engineering reconstruction

### E — append serialization != restart recovery

Commit `44b38ef...` is a direct counterexample to collapsing “the system writes an append log” into “the system can already recover by replaying that log.” The write path existed while loading was explicitly absent.

> **append-only serialization exists != replay/recovery exists**

### E — intended recovery documentation != implemented recovery path

The configuration text already described startup reconstruction while the implementation commit said loading was absent. Historical documentation can therefore express an intended contract before executable support closes it.

> **documented intended behavior != implemented behavior at the same revision**

### E — first replay implementation != mature replay contract

The first public loading commit labels itself broken, then receives an immediate fix. A chronology should preserve that qualification rather than treating the first appearance of code as a release-quality boundary.

> **first public implementation != tested/released/stable behavior**

### E — rewrite mechanism != automatic rewrite policy

The 2009 background mechanism can be invoked without the later 2011 size-growth policy that decides automatically when rewrite is due.

> **manual/background rewrite mechanism exists != automatic rewrite trigger policy exists**

The later policy therefore retains a small amount of maintenance-control history (`base size`, current size, threshold configuration, scheduled state) for deciding when to invoke a mechanism that had existed earlier.

### E — BGREWRITEAOF command presence != completion or authority transfer

The 2009 introduction already separates a child-produced base rewrite from parent-held differences and later completion handling. That yields the same bounded state distinctions grounded more fully in Redis 2.6:

`command accepted / child launched`
`!= child rewrite produced`
`!= parent delta appended`
`!= replacement made authoritative`.

This does not assert that all later 2.6 details were byte-for-byte identical in the 2009 work-in-progress implementation.

### E — child snapshot != current live state

The parent rewrite buffer exists because writes can continue while the child serializes a fork-time view. The bridge state is evidence of a retained relation between an older base representation and newer mutations, not a second complete database.

### E — public-repository lower bound != invention priority

A dated first appearance in the audited public repository establishes only that the mechanism is present by that revision and absent from the inspected direct parent where stated. It cannot exclude private development, lost history, external prior art, or independent earlier systems.

### E — logical AOF retirement != physical sanitization

Successful application-level replacement can retire an older AOF from Redis's active recovery relation. It does not prove that filesystem blocks were overwritten, Flash pages erased, controller copies purged, or forensic recovery made impossible.

## Functional analogies and limits

### A — mechanism/policy separation compared with other maintenance systems

Cases 136 and 142 provide bounded functional comparisons in which a reason/policy for maintenance, admission of maintenance work, and actual execution/completion are separable. Redis's 2009 mechanism followed by its 2011 automatic policy is another instance of that broad systems pattern.

This comparison establishes no shared implementation lineage or historical influence.

## Explicit non-claims

- **X:** `44b38ef...` is not claimed to be the invention of append-only logging, command logging, WAL, journaling, or durable replay.
- **X:** `9d65a1...` is not claimed to be the invention of log rewriting, compaction, checkpointing, fork-based snapshotting, or copy-and-switch replacement.
- **X:** repository-parent absence is not evidence that no private or unpublished Redis implementation existed earlier.
- **X:** the work-in-progress introduction date is not silently promoted into a stable release date.
- **X:** `rewriteaof` appearing in the CLI table is not treated as proof that a synchronous server command with that name was supported by the same revision.
- **X:** successful logical replacement is not a storage-media sanitization witness.

## Related-repository reuse boundary

A repository search of `tmzncty/computing-archaeology` for `BGREWRITEAOF` and `Redis AOF` found no dedicated Redis/AOF archaeology module to reuse in this slice. Broader append-log, database-checkpoint, fork, filesystem-replacement, and compaction history belongs there rather than being rebuilt here.

## Open debt after this deepening

This slice closes the **bounded public-repository first-appearance debt** for Redis AOF write serialization and BGREWRITEAOF by direct parent/child evidence. It deliberately leaves open:

1. release/tag genealogy between the 2009 work-in-progress BGREWRITEAOF introduction and released 2.2.0;
2. private/unpublished Redis development history;
3. prior art outside Redis for append logging, log rewriting, checkpointing, copy-and-switch replacement, and fork-based persistence;
4. exact crash/fault behavior of the 2009 implementation;
5. lower-layer filesystem/device durability and sanitization behavior.
