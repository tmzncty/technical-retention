# Redis 2011–2012 Automatic AOF Rewrite Genealogy Deepening

## Scope

This record deepens Case 138 with one bounded chronology left open by the Redis 2.6 grounding: the separation between an already-existing **manual/background AOF rewrite mechanism** and the later **automatic rewrite trigger policy** that became part of Redis 2.4.

The bounded chain is:

1. released Redis 2.2.0 on 22 February 2011;
2. the public 10 June 2011 initial automatic-rewrite implementation and immediate hardening commits;
3. released Redis 2.4.0 on 14 October 2011;
4. continuity into the already-grounded Redis 2.6.0 behavior.

This does **not** establish the first invention of append-only logging, database-log compaction priority, or private/unpublished experiments. The separate 2009 origin deepening now supplies bounded public-repository first-appearance evidence for Redis AOF serialization and `BGREWRITEAOF`; this record remains scoped to the later automatic-policy layer.

Case: [`../cases/138-redis26-aof-rewrite-current-state-reserialization.md`](../cases/138-redis26-aof-rewrite-current-state-reserialization.md)

Grounding record: [`138-redis26-aof-rewrite-grounding.md`](138-redis26-aof-rewrite-grounding.md)

Earlier public-implementation origin record: [`138-redis-2009-aof-bgrewriteaof-origin-deepening.md`](138-redis-2009-aof-bgrewriteaof-origin-deepening.md). It now bounds append-only serialization to 30 October 2009 and the first directly parent-diffed public `BGREWRITEAOF` implementation to 26 November 2009; this file remains responsible for the later automatic-policy layer.

## Evidence labels

- `H/P` — direct historical / primary evidence from released Redis tags or the official Redis repository history;
- `E` — engineering reconstruction from those artifacts;
- `A` — bounded functional comparison;
- `X` — claim explicitly not established.

## Source 1 — Redis 2.2.0: manual/background rewrite already exists

### H/P — released floor

The official Redis repository's annotated `2.2.0` tag is dated **2011-02-22T17:24:07Z**.

Primary record:

- <https://github.com/redis/redis/releases/tag/2.2.0>
- tag object `0c1085b0514c740597041f3a103e3aed89747a91` in the official repository.

### H/P — `BGREWRITEAOF` is already a callable maintenance mechanism

Released `2.2.0` `src/aof.c` contains `bgrewriteaofCommand()`. If no background AOF rewrite is already running, the command invokes `rewriteAppendOnlyFileBackground()`.

Primary artifact:

- <https://github.com/redis/redis/blob/2.2.0/src/aof.c>

The released `redis.conf` also tells the operator to check `BGREWRITEAOF` for rewriting an append log in the background when it becomes too big.

Primary artifact:

- <https://github.com/redis/redis/blob/2.2.0/redis.conf>

### H/P — the released 2.2 configuration has no automatic-rewrite controls

The same released `2.2.0` configuration documents AOF enablement and fsync policy, but does not contain the later `auto-aof-rewrite-percentage` / `auto-aof-rewrite-min-size` stanza. The released `src/redis.c` likewise has no `auto_aof...` trigger state found in the 2.4 implementation.

This absence is used only to bound the **released 2.2 tree**.

**X:** `not present in released 2.2.0 = no earlier branch, patch, prototype, or unpublished experiment ever existed`.

## Source 2 — 10 June 2011: automatic rewrite is added as a policy layer

### H/P — first bounded public implementation commit

Official Redis commit:

- `b333e2399778e624174e00d123c2cb3785333e3d`;
- authored/committed **2011-06-10T10:39:23Z**;
- message: `automatic AOF rewrite first implementation. Still to be tested.`

Primary record:

- <https://github.com/redis/redis/commit/b333e2399778e624174e00d123c2cb3785333e3d>

The patch does not introduce AOF rewrite from nothing. Instead it layers automatic scheduling and accounting onto machinery that already had `BGREWRITEAOF`.

### H/P — the commit adds the historical configuration vocabulary

The commit adds to `redis.conf`:

- `auto-aof-rewrite-percentage 100`;
- `auto-aof-rewrite-min-size 64mb`;
- documentation that Redis remembers AOF size after the latest rewrite, or startup size if no rewrite has occurred since restart, compares that base with current size, and implicitly calls `BGREWRITEAOF` when configured growth/minimum conditions are met.

It also adds server state for rewrite percentage, minimum size, rewrite base size, current AOF size, and a scheduled-rewrite flag.

### H/P — automatic scheduling depends on retained maintenance-control state

The same patch updates current AOF size after writes/restarts/rewrites, retains a base-size reference, and adds a `serverCron` trigger that can call the existing background rewrite path.

It also adds a scheduled path for the case where a user requests `BGREWRITEAOF` while `BGSAVE` is active: the request can be represented by `aofrewrite_scheduled` and launched after conflicting background work ends.

These are direct examples of non-payload state that exists because future maintenance decisions depend on previous maintenance/startup events.

## Source 3 — immediate hardening shows introduction != settled semantics

The official repository history between 2.2.0 and 2.4.0 records a cluster of automatic-rewrite fixes immediately after the first implementation:

- **2011-06-10 — `e3d27a726162e9faefe2d6223caf3b459b7f94f7`** — avoid division-by-zero issues in automatically triggered rewrite;
- **2011-06-10 — `4ff34b6adb9f5f9daad1f27e3aac8e016554b86c`** — fix automatic-rewrite percentage option parsing;
- **2011-06-10 — `d630abcdaf869345fed8fe508774d0318d1d82ff`** — expose new auto-rewrite state in `INFO`;
- **2011-06-10 — `19b46c9a0938ccda1bfd61afb06c63bb2f468398`** — ensure an automatic rewrite is triggered only when no other child is executing;
- **2011-06-12 — `0b17517c7c9f1f6b1c299346b7b4fa374e343fbc`** — fix automatic rewrite starting too early and adjust growth calculation;
- **2011-08-09 — `11aaf523131d4f3aa4507043f46984854505bc28`** — fix integer overflow in auto-rewrite calculation.

### H/P — the 12 June fix changes the meaning of `growth`

Commit `0b17517...` changes the calculation from `current_size * 100 / base` to `current_size * 100 / base - 100` before comparing with the configured percentage. The commit message explicitly says the previous behavior could start automatic rewrite too early.

This is a useful historical warning: the configuration name was present in the initial patch, but its effective trigger semantics were not yet settled correctly.

### H/P — the August fix widens the base-size arithmetic

Commit `11aaf523...` changes the local `base` used in the trigger calculation from `int` to `long long`, with a commit message explicitly identifying an auto-rewrite integer-overflow defect.

Thus even after the June trigger correction, large-size arithmetic remained part of the maintenance-policy correctness envelope.

## Source 4 — Redis 2.4.0: the policy is in a released stable tree

### H/P — released adoption floor

The official annotated `2.4.0` tag is dated **2011-10-14T15:54:41Z** and is labeled `Redis 2.4.0 Stable`.

Primary record:

- <https://github.com/redis/redis/releases/tag/2.4.0>
- tag object `05001b884a34ea2f40436224ad46a4f31eb077b5`.

### H/P — released 2.4 retains the automatic-rewrite controls and guarded trigger

Released `2.4.0` `redis.conf` contains the automatic-rewrite stanza with the 100% / 64 MB defaults. Released `src/redis.c` checks, before triggering automatic rewrite, that no RDB child is active, no AOF rewrite child is active, automatic rewrite percentage is nonzero, current AOF size exceeds the configured minimum, and calculated growth relative to the remembered base reaches the configured threshold. It then calls `rewriteAppendOnlyFileBackground()`.

Primary artifacts:

- <https://github.com/redis/redis/blob/2.4.0/redis.conf>
- <https://github.com/redis/redis/blob/2.4.0/src/redis.c>

This gives the bounded public chain needed by Case 138:

> released manual rewrite in 2.2.0 -> automatic policy introduced and hardened in public 2011 commits -> automatic policy present in released 2.4.0 -> later 2.6.0 mechanism already grounded by the parent evidence record.

## Engineering reconstruction

### E — manual maintenance mechanism != automatic trigger policy

Redis 2.2.0 already knew how to execute a background AOF rewrite. The June 2011 work adds policy state and a scheduler that decides when to invoke that pre-existing class of work.

Therefore:

> `rewrite mechanism exists != automatic rewrite policy exists`.

This is exactly the distinction that a release-only reading of 2.6 would hide.

### E — maintenance policy depends on retained control history

Automatic rewrite uses a remembered base size from the latest rewrite or startup plus the current AOF size. The scheduler therefore cannot be described as a stateless reaction to one instantaneous file-size observation.

The retained relation is small compared with the AOF payload, but it changes future maintenance admissibility.

> `small maintenance-control state != payload`, yet it can govern when a large payload representation is replaced.

### E — trigger threshold reached != rewrite starts immediately

Released 2.4 guards automatic invocation against concurrent RDB/AOF child work. The 2011 history also contains an explicit fix requiring that no other child be executing.

Hence:

> `rewrite due by size policy != rewrite admitted now != rewrite completed != replacement installed`.

Case 138's existing handoff analysis covers the later phases.

### E — feature-introduction commit != stable operating semantics

The initial commit says `Still to be tested`, and the next hours/days/months repair division-by-zero, option parsing, child-concurrency, growth semantics, and integer width.

For historical method this matters: a first public commit is a **lower-bound implementation event**, not proof that all later semantics were already correct or final.

### E — rewrite percentage is relative growth, not percent-of-capacity

The 12 June arithmetic fix makes the intended relation especially clear: the percentage expresses growth above a remembered base, not current-size-as-a-percent-of-some-storage-capacity.

This is a maintenance-amplification policy, not a media-retention threshold.

## Functional comparison and limits

### A — maintenance obligation / admission / execution separation

Case 136 (RAID repair priority) and Case 142 (Ceph capacity-gated recovery) also separate a reason for maintenance from the conditions under which work is admitted or scheduled. Redis automatic AOF rewrite is functionally comparable at that abstract level.

The compared systems retain different objects and use different mechanisms. No protocol, implementation, or genealogy is inferred.

### X — no sanitization claim

Automatically rewriting and later replacing an AOF does not establish overwrite of the old file's physical sectors/pages, Flash erase, crypto erase, or forensic disappearance. It changes Redis's active recovery representation, not the security-erasure status of underlying media.

### X — no invention-priority claim

`b333e239...` is the first bounded public implementation commit established by this repository slice. It is not claimed as the invention of automatic log compaction, automatic database checkpointing, or even necessarily the earliest private Redis experiment.

## Related-repository check

Fresh code searches of `tmzncty/computing-archaeology` for `BGREWRITEAOF` and `auto-aof-rewrite` returned no dedicated overlapping module.

Division of labor remains:

- **technical-retention:** this bounded relation among rewrite machinery, automatic maintenance policy, retained trigger state, admission, and authority handoff;
- **computing-archaeology:** broader Redis persistence history, exact first AOF/BGREWRITEAOF commits, database/checkpoint prior art, and cross-system genealogy if later developed.

## Claim ledger

| Claim | Label | Strength | Boundary |
| --- | --- | --- | --- |
| Redis 2.2.0 released tree already has callable background AOF rewrite | `H/P` | strong | released floor, not first invention |
| Redis 2.2.0 config directs operators to BGREWRITEAOF when the AOF is too large | `H/P` | strong | manual guidance only |
| Released 2.2.0 lacks the later automatic-rewrite controls | `H/P` | strong negative evidence | bounded to inspected released tree |
| `b333e239...` publicly introduces automatic AOF rewrite policy on 10 June 2011 | `H/P` | strong | public implementation event, not invention priority |
| initial patch adds percentage/min-size/base/current-size/scheduled control state | `H/P` | strong | exact commit |
| immediate follow-up commits harden arithmetic/config/concurrency/observability | `H/P` | strong | official repository history |
| 12 June fix corrects growth calculation to growth-above-base | `H/P` | strong | exact diff |
| August fix widens base arithmetic after overflow report | `H/P` | strong | exact diff |
| Redis 2.4.0 released tree contains the guarded automatic trigger | `H/P` | strong | release floor |
| manual rewrite mechanism and automatic trigger policy are separable | `E` | strong reconstruction | bounded Redis chain |
| automatic maintenance uses retained small control state | `E` | strong reconstruction | not application payload |
| threshold due does not imply immediate admission/completion/install | `E` | strong reconstruction | child-work guards + Case 138 handoff |
| 2011 first implementation does not prove settled semantics | `E`, `X` | strong boundary | multiple subsequent fixes |
| cross-case scheduler comparisons are functional only | `A`, `X` | bounded | no genealogy |
| rewrite/replacement does not prove media sanitization | `X` | strong boundary | lower-layer media separate |
| broader AOF/BGREWRITEAOF and database-checkpoint priority remains open | `X` | explicit scope | route history to computing-archaeology |

## What this closes

This closes the **bounded automatic-rewrite introduction / 2.4 release genealogy** that the original Case 138 grounding left open.

It does **not** close:

1. exact first public Redis AOF implementation;
2. exact first public `BGREWRITEAOF` implementation;
3. broader pre-Redis database log-rewrite/checkpoint prior art;
4. Redis 7 multipart-AOF evolution;
5. crash/power fault injection around rewrite handoff.
