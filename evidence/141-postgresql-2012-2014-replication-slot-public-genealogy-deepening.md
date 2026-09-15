# Evidence 141 — PostgreSQL 2012–2014 replication-slot public genealogy deepening

**Status:** bounded deepening complete  
**Case:** [`../cases/141-postgresql-replication-slot-wal-retention-frontier.md`](../cases/141-postgresql-replication-slot-wal-retention-frontier.md)  
**Claim layer:** historical record + engineering reconstruction + bounded functional analogy + bounded philosophical interpretation  
**Bounded question:** before the 1-February-2014 mainline `Introduce replication slots` commit, what public PostgreSQL development record already existed for slot identity, cross-disconnection / cross-restart continuation, crash-safe slot state, and the shift from a logical-decoding-specific `logical slot` interface toward generic `replication slots` usable by streaming replication?

## Why this slice exists

The canonical Case 141 already has strong released/mainline evidence beginning with PostgreSQL 9.4 development in 2014. It also explicitly left the **pre-2014 proposal/review lineage** open.

This record closes only a bounded portion of that debt. It follows the public PostgreSQL mailing-list sequence from **15 November 2012 through 1 February 2014** and asks a terminology/control-state question rather than trying to write a general history of logical decoding.

The central result is that the public record did not jump directly from ordinary streaming replication to the February-2014 physical-slot commit. By late 2012 and 2013, the logical-decoding patch series already exposed a named slot relation intended to outlive one walsender connection; the development record then made crash/restart persistence explicit and, by June 2013, explicitly proposed **morphing the `logical slot` interface into generic `replication slots` also usable by streaming replication**. The February-2014 mainline commit then introduced the physical form as a crash-safe WAL-retention structure while anticipating forthcoming logical slots with different properties.

This is a **public-development genealogy**, not an invention-priority claim and not proof that every intermediate patch had the same fields, durability contract, API, or released behavior as PostgreSQL 9.4.

## Source ladder

| Source | Date | Evidence class | Bounded use here |
|---|---:|---|---|
| Andres Freund, `logical changeset generation v3`, pgsql-hackers | 2012-11-15 | `H/P` | public logical-decoding patch series; `max_logical_slots` vocabulary/configuration is already visible |
| Andres Freund, reply to v3 review, pgsql-hackers | 2012-12-13 | `H/P` | `INIT_LOGICAL_REPLICATION` once + later `START_LOGICAL_REPLICATION 'slot-id'`; explicit admission that the patch did not yet persist enough across restarts |
| Andres Freund, `logical changeset generation v4`, pgsql-hackers | 2013-01-15 | `H/P` | explicit crash/restart persistence work; `permanent replication slot` create/start/free interface |
| Andres Freund, v4 design/review reply | 2013-01-25 | `H/P` | permanent slot persists across restarts until explicitly freed; continuity purpose described as gapless service across disconnect/crash |
| Andres Freund, `logical changeset generation v5` | 2013-06-14 | `H/P` | explicit TODO to morph `logical slot` into generic `replication slots` usable by streaming replication |
| PostgreSQL commit `858ec11858a914d4c380971985709b6d6b7dd6fc`, `Introduce replication slots` | 2014-02-01 | `H/P` | mainline physical-slot introduction; crash-safe WAL-retention contract; explicit physical/logical terminology split |
| PostgreSQL 9.4 released source/docs | 2014-12-18 release | `H/P` | released boundary already covered by the canonical grounding record; used here only as the endpoint of this public genealogy |

All central sources are PostgreSQL project primary records. Mailing-list patch discussions establish public design/implementation history, but a posted patch series is not silently treated as a released contract.

## Primary-source anchors

- 15-Nov-2012, `logical changeset generation v3`:  
  <https://www.postgresql.org/message-id/20121115002746.GA7692%40awork2.anarazel.de>
- 13-Dec-2012, v3 review reply:  
  <https://www.postgresql.org/message-id/20121213172859.GA7991%40awork2.anarazel.de>
- 15-Jan-2013, `logical changeset generation v4`:  
  <https://www.postgresql.org/message-id/20130115013845.GE22155%40awork2.anarazel.de>
- 25-Jan-2013, v4 design/review reply:  
  <https://www.postgresql.org/message-id/20130125011609.GA15706%40awork2.anarazel.de>
- 14-Jun-2013, `logical changeset generation v5`:  
  <https://www.postgresql.org/message-id/20130614224817.GA19641%40awork2.anarazel.de>
- 1-Feb-2014 mainline commit:  
  <https://github.com/postgres/postgres/commit/858ec11858a914d4c380971985709b6d6b7dd6fc>

## Historical record

### 1. November 2012: public `logical slot` vocabulary exists inside the logical-changeset patch series

On **15 November 2012**, Andres Freund posted `logical changeset generation v3` to pgsql-hackers. The demonstration starts PostgreSQL with, among other settings:

```text
wal_level=logical
max_wal_senders=10
max_logical_slots=10
wal_keep_segments=100
```

For this case, the important fact is not merely that logical decoding work existed. A named/configured population of **logical slots** was already part of the public patch-series interface.

This establishes a conservative public floor:

```text
public `logical slot` mechanism/vocabulary by Nov 2012
    != generic replication-slot mainline contract already released
```

The v3 message does not by itself prove the later PostgreSQL 9.4 persistence layout, `restart_lsn` semantics, physical-slot behavior, or final replication protocol syntax.

### 2. December 2012: the slot is already intended to bridge separate walsender sessions, but persistence is explicitly incomplete

A **13 December 2012** review reply is unusually valuable because it records both the intended lifecycle and a limitation of the then-current patch.

Freund explains the operational pattern as:

```text
INIT_LOGICAL_REPLICATION once when setting up a new replica
    -> later START_LOGICAL_REPLICATION 'slot-id' 'position'
```

The point of finding the slot again is that initialization and later streaming can happen in **different walsender processes**, including after restart. But the same reply immediately says the implementation still needed work because it was **not yet persisting enough between restarts**.

That contemporaneous admission blocks a tempting backward projection:

```text
cross-restart continuity is already a design requirement
    != the December-2012 patch already satisfies full crash-safe persistence
```

This is a strong historical counterexample to treating design intent, object naming, and implemented persistence horizon as one event.

### 3. January 2013 v4 explicitly adds crash/restart persistence work

On **15 January 2013**, `logical changeset generation v4` lists among its changes:

- crash/restart persistence of in-memory structures in a crash-safe manner;
- a shared-memory state layer for replication slots;
- explicit permanent-slot operations.

The posted interface includes:

```text
INIT_LOGICAL_REPLICATION 'plugin' 'slotname' (options)
START_LOGICAL_REPLICATION 'slotname' 'recptr'
FREE_LOGICAL_REPLICATION 'slotname'
```

The message describes `INIT_LOGICAL_REPLICATION` as allocating a **permanent replication slot**.

Two things should remain separate:

```text
slot identity/lifetime is becoming explicit and persistent
    != every later 9.4 slot field/API already exists unchanged
```

and:

```text
mailing-list patch claims crash/restart persistence work
    != independent fault-injection proof of every storage-layer failure mode
```

### 4. January 2013 design discussion makes the continuation purpose explicit

A **25 January 2013** v4 design/review reply gives the slot a clear future-consumer role. It describes a permanent slot, shows it being used by a receiver, and says the slot persists across restarts until an explicit `FREE_LOGICAL_REPLICATION` removes it.

The discussion frames the persistent state as supporting a replication consumer that must continue receiving changes without a gap across interruptions such as disconnection and crash.

For `technical-retention`, this is the important relation:

```text
current receiver connection
    != retained slot identity
    != retained future-continuation claim
```

An absent receiver can cease executing while the retained server-side object remains meaningful for a later continuation attempt.

This does **not** mean the 2013 logical slot was already identical to the 2014 physical slot. Logical decoding additionally carries database/plugin/snapshot/decoding concerns that physical streaming does not share in the same form.

### 5. June 2013: the public TODO explicitly generalizes the abstraction

On **14 June 2013**, `logical changeset generation v5` lists a TODO that is unusually direct for terminology genealogy:

> morph the `logical slot` interface into being `replication slots` that can also be used by streaming replication

The same post says one of the intervening fixes is avoiding rereading all WAL from the establishment of a logical slot.

This gives a clean bounded chronology:

```text
2012–early 2013:
logical-decoding-specific `logical slot`

June 2013 public design direction:
generalize slot abstraction so streaming replication can use it too

February 2014 mainline:
initial generic infrastructure lands with a `physical` slot form,
while logical slots are explicitly anticipated as a related form
```

The wording matters because it prevents two opposite mistakes:

1. treating February 2014 as if the word/concept `slot` appeared from nowhere; and
2. treating the 2012 logical patch as if it were already the final generic PostgreSQL 9.4 replication-slot implementation.

### 6. February 2014: mainline physical slots land as crash-safe WAL-retention state

Commit `858ec11858a914d4c380971985709b6d6b7dd6fc`, committed **1 February 2014**, is titled `Introduce replication slots.` Its commit message defines replication slots as a **crash-safe data structure** capable of preventing premature removal of WAL segments needed by a standby and, with feedback, tuple pruning that would cause replication conflicts.

The same message says the form introduced by that patch is called **physical** in some places because forthcoming logical-decoding patches will also have slots with somewhat different properties.

That mainline commit therefore records both:

```text
a generic slot infrastructure / name
    + an initial physical slot contract
```

and a type boundary:

```text
physical slot
    != logical slot
```

The shared noun does not erase the type-specific retained state or semantics.

### 7. Mainline entry, public proposal history, and released 9.4 are three different dates

The canonical case already distinguishes the **1-February-2014 mainline commit** from the **18-December-2014 PostgreSQL 9.4 release**. This deepening adds a third layer: public logical-slot development is visible from **November 2012**, with explicit genericization by **June 2013**.

The resulting chronology is:

```text
public prototype/design record
    != mainline integration
    != released user contract
    != invention priority
```

This is the main historiographic correction produced by the slice.

## Terminology evolution

| Public period | Bounded term | What the sources justify | What they do not justify |
|---|---|---|---|
| Nov–Dec 2012 | `logical slot`, `max_logical_slots` | a slot-like retained relation exists inside the logical-decoding patch series | final 9.4 persistence semantics or generic physical-slot API |
| Jan 2013 | `permanent replication slot` in logical-decoding discussion | named slot survives receiver sessions/restarts in the evolving patch design; crash/restart persistence becomes explicit work | byte-for-byte identity with final 9.4 slot state |
| Jun 2013 | proposed generic `replication slots` | actor explicitly proposes morphing logical-slot interface so streaming replication can use it | proof the genericization is already complete/released |
| Feb 2014 | `replication slot`; initial type `physical` | generic infrastructure enters mainline with crash-safe physical-slot WAL-retention semantics | logical and physical slots have identical properties |
| Dec 2014 | released PostgreSQL 9.4 slot family | released physical and logical slot behavior belongs to the canonical grounding evidence | proof of first invention/coinage |

This project therefore should not write a teleological sentence such as “logical slots evolved into physical slots.” The historical record is closer to **a logical-decoding-specific slot mechanism being generalized into shared replication-slot infrastructure, after which physical and logical types coexist with different properties**.

## Retained-state decomposition exposed by the genealogy

The pre-2014 record makes several states visible before the final released vocabulary stabilizes:

1. **consumer identity / slot name** — the durable designation by which a later session finds the same continuation relation;
2. **current receiver connection/process** — transient walsender/consumer activity;
3. **continuation position / decoding progress state** — where the stream can resume or what history remains needed;
4. **restart-surviving slot control state** — the subset that must cross process/server restart if the slot is to remain meaningful;
5. **retained WAL/history substrate** — the separate log records the slot relation can require;
6. **slot type semantics** — physical and logical consumers place different requirements on the retained control state and database/catalog history.

The useful inequality is:

```text
same slot name after reconnect
    != same live process
    != sufficient crash-persistent control state automatically proven
    != protected WAL itself
    != one universal physical/logical slot contract
```

## Engineering reconstruction

### A. A restartable consumer needs a retained relation, not merely a retained log

If a future consumer is to reconnect and continue without starting from scratch, the server needs more than old WAL bytes. It needs a retained way to say **which consumer relation this is and what historical range/status still belongs to it**.

The 2012–2013 discussions reveal that need while the persistence implementation was still being completed.

Thus:

```text
history exists
    != future consumer knows/admissibly resumes its place in that history
```

### B. Persistent identity and persistent progress are separate implementation obligations

The December-2012 discussion already assumes that initialization and later use can happen in different processes, potentially after restart. Yet it also says the implementation did not persist enough state.

So:

```text
stable identifier concept exists
    != all state required by that identifier survives restart
```

This is a general engineering distinction, but the evidence here is specifically PostgreSQL's public patch discussion.

### C. Genericization changes the abstraction boundary, not merely the spelling

The June-2013 TODO is significant because it explicitly moves the slot interface from one logical-decoding context toward a replication-wide abstraction usable by streaming replication.

Engineering reconstruction:

> the reusable core is not “logical decoding” itself; it is a retained consumer/continuation relation that different replication modes can specialize.

The later physical/logical split confirms the need for specialization. Therefore:

```text
generic slot identity/lifecycle machinery
    != identical type-specific retained state
```

### D. Crash safety is a property of publication/persistence machinery, not of the word `slot`

The sequence from December-2012 incompleteness to January-2013 crash/restart persistence work is a useful reminder:

```text
object is intended to persist
    != object is already crash-safe
```

A persistence promise becomes an engineering property only when the relevant state crosses the intended durability boundary under the specified failure model.

This evidence does not independently validate filesystem, controller, or drive behavior under arbitrary power loss.

## Functional analogies — bounded

### Case 58 — Raft snapshot continuation metadata

Raft snapshotting also shows that a future continuation/recovery path needs compact retained metadata in addition to materialized state. The analogy is only that **future continuation depends on retained control relations**, not that a PostgreSQL slot is a Raft snapshot or that the systems share genealogy.

### Case 61 — HDFS Observer seen-state frontier

HDFS Observer reads retain a client/server progress relation used to decide whether a lagging reader is fresh enough. PostgreSQL slots likewise retain progress/need relations that outlive one immediate request or connection.

The mechanisms differ sharply:

```text
HDFS read-admission freshness frontier
    != PostgreSQL replay-history retention frontier
```

### Case 137 — LevelDB file liveness

LevelDB demonstrates that old physical files can remain live because another retained relation still depends on them. PostgreSQL slots show a remote-consumer relation keeping old WAL live.

Again, this is a functional comparison of **liveness authority**, not implementation identity.

## Philosophical interpretation — bounded

The public development sequence sharpens one modest point already present in Case 141: technical persistence may require retaining not only an object but also a **relation of future entitlement to earlier history**.

The receiver process can disappear; the relation survives so a later receiver can continue. But the December-2012 record also shows that this relation is not made durable by intention alone. It requires a concrete persistence mechanism.

That is enough for the conceptual observation. The historical actors did not formulate this as a theory of memory, promise, debt, or tertiary retention, and this file does not attribute those concepts to them.

## Anti-anachronism and non-claims

This evidence does **not** claim any of the following:

1. PostgreSQL invented replication progress tracking, retained log positions, or slot-like replication state.
2. November 2012 is the first private implementation or first conceptual origin of replication slots.
3. `max_logical_slots` in v3 proves the final PostgreSQL 9.4 slot architecture already existed.
4. The December-2012 patch was fully crash-safe; the author explicitly says persistence was incomplete.
5. The January-2013 patch was independently fault-tested across every storage stack.
6. A posted mailing-list patch has the same status as a committed mainline feature or released contract.
7. `logical slot` and later `physical slot` are identical mechanisms.
8. The June-2013 genericization TODO proves every later design choice or direct line-by-line code ancestry.
9. The February-2014 mainline commit is the invention date or first use of the word `slot` in replication systems.
10. Slot persistence means all required WAL is immortal; the canonical PostgreSQL-13 evidence directly disproves that under configured retention caps.
11. Slot identity persistence means consumer application state is also persistent/current.
12. Retained WAL implies secure archival preservation or immutable history.
13. Dropping/freeing a slot sanitizes old WAL at lower storage layers.
14. The similarly timed PostgreSQL work on replication identifiers/origins is automatically part of the same mechanism; those are separate state relations unless a source explicitly connects them.
15. Public chronological proximity proves influence from another database or replication system.
16. This slice replaces a broader PostgreSQL logical-decoding/streaming-replication history in `computing-archaeology`.

## Claim ledger

| Claim | Layer | Strength | Source boundary |
|---|---|---:|---|
| Public v3 uses `max_logical_slots` | historical record | high | 15-Nov-2012 pgsql-hackers post |
| v3 intended INIT once and later START by slot id, including across distinct walsenders | historical record | high | 13-Dec-2012 author review reply |
| December-2012 implementation did not yet persist enough state across restart | historical record | high | same author reply |
| v4 explicitly adds crash/restart persistence work | historical record | high | 15-Jan-2013 v4 post |
| v4 exposes a `permanent replication slot` create/start/free lifecycle | historical record | high | same v4 post |
| a permanent logical slot is described as surviving restarts until freed | historical record | high | 25-Jan-2013 design/review reply |
| v5 explicitly proposes morphing logical slots into generic replication slots usable by streaming replication | historical record | high | 14-Jun-2013 v5 post |
| 1-Feb-2014 mainline slots are described as crash-safe and the initial form as physical because logical slots are forthcoming | historical record | high | PostgreSQL commit `858ec118...` |
| intended persistence != implemented crash safety | engineering reconstruction | high, bounded | Dec-2012 limitation + Jan-2013 persistence change |
| retained slot relation != WAL history itself | engineering reconstruction | high, bounded | pre-2014 lifecycle evidence + canonical 9.4 implementation evidence |
| generic slot lifecycle != identical physical/logical semantics | engineering reconstruction | high, bounded | Jun-2013 genericization statement + Feb-2014 physical/logical distinction |
| public proposal date != mainline date != release date != invention date | historiographic boundary | high | 2012–2014 dated primary record |

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for PostgreSQL replication slots did not locate a dedicated existing module to reuse.

That division of labor remains:

- **`technical-retention`:** slot identity as retained relation; cross-session/restart lifetime; history-liveness authority; persistence/publication boundaries; physical/logical type boundary;
- **`computing-archaeology`:** broader PostgreSQL replication/logical-decoding history, patch architecture, performance/operational constraints, ecosystem comparisons, and any longer predecessor genealogy.

Do not expand this evidence file into a complete logical-decoding history merely because the slot concept first appears here in that context.

## What this closes

This slice boundedly closes the roadmap's broadest **pre-2014 public genealogy** gap for Case 141:

```text
Nov 2012 public logical-slot patch interface
    -> Dec 2012 explicit persistence gap
    -> Jan 2013 explicit crash/restart persistence + permanent slot lifecycle
    -> Jun 2013 explicit genericization plan
    -> Feb 2014 mainline crash-safe physical replication slots
    -> Dec 2014 released PostgreSQL 9.4 contract
```

The important result is not a priority claim. It is that the repository can now distinguish the **prototype/design chronology** from the **mainline and release chronology**, while preserving the transition from logical-decoding-specific vocabulary to a generic replication-slot abstraction.

## Remaining evidence debt

Still open after this bounded slice:

1. pre-November-2012 private branches, talks, prototypes, or earlier mailing-list precursors;
2. exact patch-by-patch code ancestry from the 2012–2013 logical-decoding branches into the February-2014 generic/physical-slot mainline commit;
3. the subsequent mainline logical-slot landing sequence before PostgreSQL 9.4 release;
4. complete commitfest/review chronology and abandoned alternatives;
5. non-PostgreSQL prior art for retained replication-consumer positions/claims;
6. independent crash/power-loss validation of intermediate development versions;
7. broad replication/logical-decoding genealogy, which should primarily be developed in `computing-archaeology`.

## Bottom line

**Historical record:** public PostgreSQL development records show `logical slot` machinery by November 2012, an explicit persistence shortfall in December 2012, explicit crash/restart persistence and permanent-slot lifecycle work in January 2013, an explicit June-2013 plan to generalize logical slots into replication slots usable by streaming replication, and a February-2014 mainline physical-slot implementation described as crash-safe.

**Engineering reconstruction:** a future replication consumer needs a retained server-side relation whose identity and required progress/need state can survive beyond one connection; the public sequence demonstrates that naming such an object and making it actually crash-persistent are separate engineering steps.

**Functional analogy:** other systems also retain continuation/currentness/liveness relations, but no shared implementation or genealogy is inferred.

**Philosophical interpretation:** future continuation can act on the present only because a concrete control relation survives; intention to preserve that relation is not equivalent to a working persistence mechanism.
