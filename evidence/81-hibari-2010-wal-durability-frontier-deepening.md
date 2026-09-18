# Case 81 deepening — Hibari 2010 WAL durability frontier beneath chain replication

## Status

**`bounded deepening complete`**

This slice closes one of Case 81's explicitly listed follow-on debts: a production-oriented chain-replication implementation with an implementation-specific stable-storage contract.

It does **not** replace the 2004 van Renesse–Schneider protocol model. Instead, it asks what extra retention state appears when Hibari composes chain replication with local write-ahead logging, `fsync(2)`, group commit, and per-write serial-number progress.

---

## Research question

The original 2004 Chain Replication paper makes the tail the service-level completion point, but it does not turn `ack(r)` into a general claim about disk-controller, filesystem, or storage-media durability.

By 2010, Scott Lystig Fritchie's Hibari implementation report gives a much more concrete lower-layer policy:

> how does a chain-replication implementation remember which ordered writes are locally safe enough to propagate, and what does that add to — or fail to add to — tail-qualified completion?

The narrow answer developed below is:

```text
ordered chain update
    + local WAL admission
    + local flush completion
    + retained serial-number durability frontier
    -> downstream propagation eligibility
    -> eventual tail/client acknowledgement
```

That is a Hibari implementation contract, not an intrinsic theorem about all chain-replication systems.

---

## Source ledger

### P1 — Fritchie, “Chain Replication in Theory and in Practice,” Erlang'10

**Author:** Scott Lystig Fritchie, Gemini Mobile Technologies, Inc.

**Venue/date:** 9th ACM SIGPLAN Workshop on Erlang, September 30, 2010, pp. 33–44.

**Proceedings facsimile inspected:**

- <https://www.erlang-solutions.com/wp-content/uploads/2024/05/Erlang_10-Workshop.pdf>

**Bibliographic cross-check:**

- DOI `10.1145/1863509.1863515`;
- DBLP record: <https://dblp.org/rec/conf/erlang/Fritchie10>.

**Directly inspected portions:**

- paper overview and Hibari architecture;
- §4, “Problems with Disk Write I/O Latency”;
- local WAL / group-commit discussion;
- serial-number safe-flush frontier;
- early WAL/brick race-condition discussion;
- repair/re-sync discussion;
- release note stating Gemini released Hibari source in July 2010.

**Evidence class:** contemporary implementation paper / primary engineering report (`H/P`).

### P2 — author slides for the same 2010 workshop paper

**Source:** Scott Lystig Fritchie, “Chain Replication in Theory and in Practice,” Erlang Workshop 2010 slides.

- <https://www.snookles.com/scott/presentations/erlang2010-slf-slides.pdf>

The slides independently summarize the relevant operational policy:

- append-only logs;
- `fsync(2)` latency;
- “Hibari default: all updates are durable”;
- all logical-brick logs aggregated through a common log;
- most Hibari bugs occurred in write/sync management code;
- replica repair must preserve update order while coping with write/sync delays.

**Evidence class:** contemporary author presentation (`H/P`).

### P3 — Hibari system-administrator documentation

**Repository:** `hibari/hibari-doc`.

**Relevant source:** `src/hibari/hibari-sysadmin-guide.en.txt`.

The project documentation distinguishes the default durability policy from optional weaker modes:

- ordinary/default durable updates use disk logging and `fsync()`;
- **Asynchronous writes** may disable `fsync()` for higher performance, explicitly accepting possible data loss after system crash or power failure;
- **Non-durable updates** may disable update logging, explicitly accepting data loss if all nodes in a chain crash.

Current project documentation rendering:

- <https://hibari.readthedocs.io/en/latest/admin-guide/main-features.html>

**Evidence class:** first-party implementation/operator documentation (`H/P` for the documented Hibari behavior; not proof that every historical deployment used every default).

### P4 — Hibari contributor documentation

**Repository:** `hibari/hibari-doc`.

**Relevant source:** `src/hibari/hibari-contributor-guide.en.txt`.

The contributor guide describes asynchronous handling of `file:sync/1`, buffering while a sync is in progress, and the implementation work needed to prevent the log process from blocking callers unnecessarily.

This is supporting implementation documentation, not a replacement for P1's 2010 historical report.

---

## Historical record

### H/P — Hibari adds a local durability requirement below chain-replication ordering

Fritchie's 2010 paper describes Hibari as a distributed key-value store using chain replication and states that, **by default**, updates are persistent: each server flushes updates to local stable storage before client reply.

This wording matters because the 2004 protocol case deliberately refused to infer physical-media durability from tail acknowledgement alone.

Hibari therefore contributes an implementation-specific additional layer:

```text
protocol ordering / chain role
    !=
local stable-storage qualification
```

The latter is an implementation policy layered underneath the former.

### H/P — write-ahead log and group commit convert many writes into a prefix-style durability frontier

The 2010 paper says Hibari uses both a write-ahead log and group commit. Multiple updates can therefore share one `fsync(2)` instead of requiring a separate synchronous flush for every operation.

This is not merely a performance detail. Group commit means that the implementation needs a retained answer to:

> which prefix of the ordered update stream has actually crossed the local flush boundary?

Fritchie states that chain replication already associates a serial number with each write and propagates updates in serial-number order. Hibari's WAL process uses those serial numbers to report to a logical brick the **largest serial number safely flushed to disk**.

That number is a compact local durability frontier.

### H/P — downstream propagation is gated by local safe-flush progress in the described implementation

Immediately after describing the “largest serial number safely flushed to disk,” the 2010 paper says a brick can then send those updates to downstream bricks.

The most conservative reconstruction of the described normal path is therefore:

```text
brick receives ordered update
    -> update enters local WAL work
    -> one or more writes share group-commit flush work
    -> WAL reports largest safely flushed serial
    -> brick may propagate that safe prefix downstream
```

The source does not justify rewriting this as a universal property of chain replication. It is an implementation-specific Hibari ordering between a local persistence frontier and downstream propagation.

### H/P — safe-flush progress is not the same state as “write call issued”

Fritchie explicitly separates the logical brick from the shared WAL process. The brick can continue other work while the WAL process performs `write(2)` and `fsync(2)`; the WAL later sends a message when I/O completes.

Thus the implementation visibly contains at least these states:

```text
update known to brick
    !=
WAL I/O requested
    !=
WAL flush completed
    !=
brick has learned safe serial frontier
    !=
downstream propagation completed
```

Collapsing these into one “write happened” event would erase exactly the implementation boundary that caused bugs.

### H/P — early ordering/frontier bugs caused data loss

The 2010 paper reports that early brick/WAL implementations suffered subtle race conditions including:

- local WAL writes occurring out of order;
- `fsync(2)` completions being acknowledged with the wrong log serial number;
- log replay messages being sent downstream in the wrong order.

Fritchie states that many of these bugs caused data loss.

This is unusually strong evidence for the retention significance of bookkeeping state. The serial number is not decorative metadata: an incorrect relation between serial order and safe-flush knowledge can make later propagation/recovery unsound.

### H/P — repair adds another ordered data movement path, not a bypass around durability concerns

The same paper says replica repair can generate large amounts of disk I/O and must coexist with concurrent updates. The author slides summarize repair/re-sync as requiring replay of updates in the same order while managing `write(2)` and `fsync(2)` delays on both participating bricks.

Therefore “repairing replica has received bytes” should not be treated as synonymous with “repairing replica has crossed the same local durability/admission boundary required of an ordinary full chain member.”

This evidence does not by itself reconstruct every repair-state transition or prove the exact admission predicate for every Hibari release; it only establishes that repair and sync ordering were operationally coupled to local I/O completion.

### H/P — Hibari documentation exposes weaker durability modes

First-party Hibari documentation later makes the default/option boundary explicit:

- `fsync()` can be disabled for asynchronous writes, trading performance for possible crash/power-failure data loss;
- logging can be disabled entirely for non-durable updates, accepting loss if all chain nodes crash.

This is an important historical/engineering counterexample to any claim of the form:

```text
chain replication
    -> necessarily fsyncs every replica before acknowledgement
```

No: Hibari's durable default composed the two mechanisms, while Hibari also documented modes that weaken the local persistence contract without ceasing to be a chain-replicated system.

---

## Engineering reconstruction

### E — there are two distinct completion frontiers

For the bounded Hibari default described by the 2010 paper, separate at least:

1. **local durability frontier** — largest write serial locally reported safe after WAL flush;
2. **chain/service completion frontier** — update has propagated through the chain far enough for the tail/client completion rule.

They are related but not identical.

```text
local safe serial on one brick
    !=
client-visible chain completion
```

Conversely, in a configuration that relaxes local fsync/logging, protocol completion need not carry the same crash/power-failure meaning as in the durable default.

### E — a tail acknowledgement acquires stronger meaning only by composition

The 2004 protocol gives tail processing/acknowledgement a service-ordering meaning.

Hibari's default implementation adds local persistence gates on the path. The resulting acknowledgement can therefore be reconstructed as a **composed** event:

```text
protocol completion
    + implementation-specific local persistence prerequisites
    -> stronger practical acknowledgement contract
```

The stronger property comes from composition. It should not be projected backward into the abstract 2004 protocol.

### E — prefix durability is retained as a compact frontier, not as one Boolean per write

Because writes are ordered by serial number and group commit may flush many at once, “largest safely flushed serial” compactly denotes a prefix:

```text
safe_serial = N
    -> implementation may treat ordered prefix <= N as locally flushed
```

This is a frontier representation. It resembles many other retention systems that store a monotonic progress boundary rather than independent status bits for every prior item.

But it is only safe if the relation `serial order -> WAL order -> flush acknowledgement` is correct.

### E — group commit changes the geometry of completion evidence

A single `fsync(2)` can qualify multiple writes together. Therefore:

```text
one fsync completion
    != one logical update completion
```

and:

```text
many logical writes
    -> one physical/logical flush episode
    -> frontier advances over a prefix
```

The completion evidence is batched even though chain operations remain separately serialized.

### E — stale or incorrect progress metadata can be more dangerous than absent metadata

An absent safe-flush update can delay propagation. A falsely advanced safe-flush serial can authorize propagation/replay based on work not actually qualified by the intended local durability barrier.

Fritchie's report of wrong serial acknowledgements and data loss supplies a concrete witness for this distinction:

```text
missing progress evidence
    -> possible stall

false progress evidence
    -> possible safety violation / data loss
```

This is an engineering reconstruction of the reported failure class, not a claim that every such bug has exactly one failure outcome.

### E — local `fsync` completion still has an abstraction boundary

The 2010 paper uses `fsync(2)` as the stable-storage boundary required against cluster-wide catastrophe. That is the software contract it reports.

This case does **not** infer from that alone that every drive cache, RAID controller, firmware implementation, filesystem, kernel, or power-loss scenario honored stronger hardware persistence guarantees than the operating-system/storage stack exposed.

So retain:

```text
Hibari WAL reports fsync-complete
    !=
independent proof of final physical-media persistence under every hardware fault model
```

---

## Functional comparisons — not genealogy

### A — Case 81's 2004 `Sent_i` state

`Sent_i` and Hibari's safe-flush frontier preserve different obligations.

- `Sent_i` remembers forwarded work whose tail completion may still be unknown and supports suffix repair.
- Hibari's safe-flush serial remembers how far local WAL persistence has progressed and gates which ordered updates may proceed downstream in the described implementation.

They can coexist in one implementation but are not synonyms.

### A — Case 56, Kafka high watermark

Both can be represented as monotonic-looking frontiers over an ordered sequence, but their authority differs:

- Hibari's local safe serial is a **per-brick persistence frontier**;
- Kafka's high watermark is a **replication/visibility frontier** derived from replica progress.

Frontier-shaped metadata does not imply identical semantics.

### A — Case 152, SQLite WAL

Both use a write-ahead log and distinguish working state from retained log evidence and later completion/visibility boundaries. SQLite's transaction/checkpoint rules and Hibari's chain/WAL propagation rules are different systems with no genealogy asserted here.

### A — Case 05, Ceph EBOFS journal deepening

Both cases show why “submitted to a logging subsystem” must not automatically be treated as “safe under the intended restart/power-failure model.” EBOFS's journal/checkpoint machinery and Hibari's shared WAL/group-commit machinery have different ordering and authority rules.

---

## Philosophical interpretation — bounded

### I — completion is layered, not a single metaphysical event

The technically supported lesson is narrow:

> a distributed write can cross several independently meaningful boundaries — ordering, local logging, local flush, propagation, tail processing, client knowledge — and the word “complete” is unsafe unless the boundary and failure model are named.

No broader claim about memory, archives, human trust, or philosophical identity follows automatically.

### I — retained progress evidence can be constitutive without being payload

The largest safely flushed serial number is not the user's value. Yet it can determine which values are allowed to advance to the next protocol stage. This is a concrete example of technical retention in which a small control relation governs the admissibility of a much larger payload history.

---

## Explicit non-claims

This slice does **not** claim that:

1. chain replication intrinsically requires stable storage;
2. the 2004 OSDI protocol itself specifies Hibari's WAL or `fsync(2)` policy;
3. every Hibari deployment used the durable default;
4. every Hibari release had identical logging internals;
5. `write(2)` completion equals `fsync(2)` completion;
6. `fsync(2)` completion proves persistence through every possible disk/RAID/firmware power-loss behavior;
7. one `fsync(2)` corresponds to exactly one logical write;
8. a safe local serial is identical to tail-qualified client completion;
9. a tail reply proves that the client received the reply;
10. `Sent_i` and the WAL safe-serial frontier are the same state;
11. a WAL is an application audit log;
12. group commit makes write ordering irrelevant;
13. an update present in page cache is already safely flushed;
14. a repairing brick is authoritative merely because it contains some copied keys;
15. Hibari invented write-ahead logging, group commit, `fsync`, serial numbers, or chain replication;
16. the reported race conditions exhaust all Hibari durability bugs;
17. the reported bugs establish one unique crash trace for every data-loss incident;
18. later Hibari documentation proves that all 2010 production clusters used exactly those optional settings;
19. project documentation's phrase “stable storage” proves a stronger hardware guarantee than the OS/storage stack exposed;
20. this implementation history is a genealogy from Hibari to later distributed stores.

---

## Claim ledger

| Claim | Type | Evidence |
| --- | --- | --- |
| Hibari implements chain replication and by default persists updates locally | `H/P` | P1 |
| the 2010 implementation uses WAL + group commit + `fsync(2)` | `H/P` | P1 |
| the WAL reports the largest serial safely flushed to disk | `H/P` | P1 |
| updates may then be sent downstream from the safe prefix | `H/P` | P1 |
| wrong log order / wrong safe serial / wrong replay order occurred in early implementations | `H/P` | P1 |
| the paper reports that many such bugs caused data loss | `H/P` | P1 |
| author slides independently summarize durable-default logging and write/sync bug concentration | `H/P` | P2 |
| Hibari docs expose asynchronous/non-durable modes that weaken the local persistence contract | `H/P` | P3 |
| safe serial is usefully reconstructed as a local durability frontier | `E` | P1 ordering + largest-safe-serial semantics |
| tail/service completion and per-brick persistence completion are distinct frontiers | `E` | P1 + Case 81 2004 grounding |
| stronger Hibari acknowledgement semantics arise by composition, not from chain replication alone | `E` | P1 + P3 + original protocol boundary |
| frontier correctness is retention-critical because false advancement can authorize unsafe progress | `E` | P1's reported wrong-serial/data-loss failures |
| no genealogy is inferred from functional similarity to Kafka/SQLite/Ceph | `A/X` | project method boundary |

---

## Relation to the 2004 canonical case

The original Case 81 grounding already established:

```text
upstream application
    != tail-qualified completion
    != client knowledge of completion
```

This deepening adds a lower-layer axis for the Hibari implementation:

```text
local update accepted
    != WAL work queued
    != WAL flush complete
    != safe-serial frontier advanced
    != downstream propagation complete
    != tail-qualified completion
    != client knowledge of completion
```

The key result is not that one chain got “more durable.” It is that the practical system exposes **orthogonal completion dimensions**:

- replication/order position;
- local persistence position;
- reconfiguration/role position;
- observer/client knowledge.

---

## Cross-repository duplication check

A GitHub search of `tmzncty/computing-archaeology` for both `Hibari` and `Chain Replication` returned no dedicated packet during this slice.

**Routing decision:**

- keep here: the retention-specific seam `ordered update -> local WAL -> safe serial frontier -> downstream eligibility -> tail completion`;
- route elsewhere if developed later: broader Hibari/Gemini product history, Erlang adoption history, chain-replication genealogy, CRAQ/Hibari influence relations, carrier deployments, and storage-stack archaeology below `fsync(2)`.

---

## Remaining evidence debt

This bounded deepening closes the canonical Case 81 bullet “production implementations such as Hibari and their product-specific stable-storage contracts” **for the 2010 default-policy / WAL-frontier question only**.

Still open:

- exact historical source revision/tag corresponding to the September 2010 paper;
- source-level reconstruction of the brick ↔ shared-WAL message protocol at that exact revision;
- crash/fault-injection tests showing the safe-serial boundary under process and power failures;
- exact durability semantics of every optional Hibari write mode across releases;
- disk-cache / RAID-controller / filesystem behavior beneath `fsync(2)` in documented deployments;
- master/Admin-Server configuration durability and partition behavior;
- broader Hibari production genealogy and deployment history.

---

## Promotion decision

**No maturity change. Case 81 remains `grounded`.**

Reason: the new evidence strengthens one implementation-specific lower-layer contract and closes a named evidence debt, but it does not turn the whole case into an exhaustive production or hardware-durability study.
