# Case 88 evidence deepening — Linux MD PPL write-back-cache flush boundary (2018)

## Status

**Bounded implementation deepening for Case 88 — grounded.**

This file closes one explicit debt left by [`Case 88 — Linux MD RAID5 Partial Parity Log`](../cases/88-linux-md-raid5-partial-parity-log.md): the evolution from the Linux 4.12-era requirement that member-drive volatile write-back caches be disabled to the later Linux MD implementation that admits write-back-cached members by adding an explicit flush stage before the next PPL entry may proceed.

No maturity promotion is made here. The slice is intentionally narrow:

> **What additional state and ordering obligation appears when ordinary RAID-member write completion may mean only “accepted into a volatile device cache,” while the PPL record is supposed to protect the array across power failure?**

It is not a general history of RAID5, disk caches, barriers, SCSI/ATA flush commands, Linux block I/O, Intel IMSM, or PPL.

---

## Result in one sentence

The original Linux 4.12 PPL documentation required volatile write-back cache to be disabled on all member drives; commit `1532d9e87e8b2377f12929f9e40724d5fbe6ecc5`, committed 2018-01-15, changed the implementation so that PPL records which participating member disks have write-back cache enabled and, after the corresponding stripe writes complete, issues cache flushes to those disks and waits for all required flushes before the PPL I/O unit is finished and the next PPL log submission may advance.

The new boundary is therefore:

```text
stripe write BIO completion
    != member-state durability closure across power loss
```

and:

```text
PPL recovery record durable
    != home data/parity state already durable
```

The 2018 code inserts an explicit durability-closure stage between those two conditions.

---

## Source boundary

### Primary Linux sources checked

1. Linux `v4.12`, `Documentation/md/raid5-ppl.txt`.
   - The original documentation says volatile write-back cache should be disabled on **all member drives** when PPL is used; otherwise PPL cannot guarantee consistency on power failure.
2. Linux `v4.12`, `drivers/md/raid5-ppl.c`.
   - The PPL log BIO itself is submitted with `REQ_FUA`.
   - When all associated stripe writes finish, the PPL I/O unit is immediately finished; there is no per-member cache-flush stage in this version.
3. Tomasz Majchrzak / Shaohua Li, Linux commit `1532d9e87e8b2377f12929f9e40724d5fbe6ecc5`, **`raid5-ppl: PPL support for disks with write-back cache enabled`**.
   - authored 2017-12-27;
   - committed 2018-01-15;
   - adds member write-back-cache detection, a disk-flush bitmap, per-I/O-unit pending-flush tracking, and cache-flush submission before advancing PPL work.
4. Linux `v4.16`, `drivers/md/raid5-ppl.c` and `Documentation/md/raid5-ppl.txt`.
   - The new flush path is present in the tagged source.
   - The earlier blanket warning requiring member write-back caches to be disabled is gone from the documentation.

### Companion-repository check

A fresh search of `tmzncty/computing-archaeology` for `raid5-ppl`, `Partial Parity Log`, `PPL`, and write-back-cache combinations found no existing focused technical-history packet to reuse. This deepening therefore remains limited to the retention-specific implementation boundary rather than creating a parallel RAID/PPL history.

---

## Historical record

### H/P — Linux 4.12 explicitly treated volatile member write-back cache as outside the safe PPL contract

The `v4.12` PPL documentation ends with a direct restriction:

```text
volatile member write-back cache
    -> should be disabled when PPL is used
```

because otherwise PPL could not guarantee consistency after power failure.

This is stronger evidence than a generic statement that “caches are dangerous.” It is a named implementation limitation attached to the initial Linux MD PPL mechanism.

The same `v4.12` implementation writes the PPL log BIO with `REQ_FUA`. Thus the initial implementation already distinguishes the log record's own persistence request from the later home data/parity writes. The remaining problem is not that Linux had no durability primitive at all; it is that **member home writes can complete at the block layer while still residing in volatile device caches**.

### H/P — the 2018 patch removes the blanket prohibition by adding a new sequencing stage

Commit `1532d9e87e8b2377f12929f9e40724d5fbe6ecc5` says in its own commit message:

- with write-back cache enabled, all data must be flushed to disks before the next PPL entry;
- disks requiring flush are marked in a bitmap;
- when write-back cache is disabled, the next PPL entry can follow completion of the current data writes;
- when cache flushing is required, that flush defers the next log submission.

The documentation diff removes the earlier three-line warning that volatile member write-back caches must be disabled.

This is a historical implementation change, not a project inference.

### H/P — the implementation tracks write-back-cache capability separately from actual write participation

In the 2018/v4.16 code, each PPL child log records whether its associated member queue advertises write-back cache (`wb_cache_on`).

When a PPL I/O unit is submitted, the code examines the stripes attached to that I/O unit. A member is added to `disk_flush_bitmap` only when both conditions hold:

```text
member write-back cache is enabled
AND
this stripe wants a write to that member
```

Therefore the bitmap is not simply “all disks with caches.” It is a per-I/O-unit set of **participating cached members whose volatile write state still creates a durability obligation**.

### H/P — PPL log durability and home-write durability use different mechanisms

The PPL log write itself is submitted with:

```text
REQ_OP_WRITE | REQ_FUA
```

The later cache-closing operation for affected RAID members is submitted as a separate zero-data write BIO carrying:

```text
REQ_OP_WRITE | REQ_PREFLUSH
```

This is important historical detail. The implementation is not accurately described as “PPL uses FUA everywhere” or “PPL uses flush everywhere.” The code uses different block-layer durability/order mechanisms for different state transitions.

### H/P — stripe completion no longer immediately finishes the PPL I/O unit when cache obligations remain

In Linux `v4.12`, when the last pending stripe write associated with an I/O unit completes, `ppl_stripe_write_finished()` directly calls `ppl_io_unit_finished()`.

In Linux `v4.16`, the corresponding path instead checks `disk_flush_bitmap`:

```text
last pending stripe write completes
    ↓
if no cached-member flush debt:
    ppl_io_unit_finished()

if cached-member flush debt exists:
    ppl_do_flush()
```

Thus a new explicit state exists between “all stripe write BIOs completed” and “this PPL I/O unit is finished.”

### H/P — flush completion is counted before the I/O unit is retired

`ppl_do_flush()` sets `pending_flushes`, submits a preflush BIO to each relevant non-faulty member, clears the runtime bitmap after submission, and accounts for members that do not receive a flush.

`ppl_flush_endio()` handles each completion. Only when the last pending flush has completed does it call:

```text
ppl_io_unit_finished(io)
```

and wake the MD thread.

A flush error is not silently treated as an ordinary successful completion: the completion path looks up the corresponding MD member and reports it through `md_error()` when the flush BIO carries an error status.

The bounded fact is therefore not merely that “Linux sends flushes.” It **keeps the PPL I/O unit live until the required flush-completion set has closed**.

### H/P — the code deliberately makes PPL absorb upper-layer flush requests under its stronger completion rule

The 2018 commit message states that because PPL now assures data is flushed to disk at request completion, a flush request can simply be acknowledged when PPL is enabled. The corresponding PPL flush-request handler treats an empty flush request as immediately complete and otherwise removes `REQ_PREFLUSH` before retrying the data-bearing request through the PPL path.

This source-level behavior should be described narrowly: the PPL write path is assuming responsibility for the relevant durability closure. It does **not** prove that every physical drive firmware implementation faithfully honors every cache-flush command under every failure mode.

---

## Retained-state decomposition

The 2018 evolution makes at least four state classes worth separating.

| State | Where | Survival / lifetime | Role |
| --- | --- | --- | --- |
| PPL partial-parity record + header | PPL area on a member disk | intended to survive crash/power loss under block-device durability semantics | persistent crash-recovery evidence |
| new data/parity home writes | ordinary RAID member locations | target durable state once lower-layer cache obligations close | future array relation |
| dirty member write-back-cache contents | device volatile cache | may disappear on power loss | intermediate accepted-but-not-yet-closed target state |
| `wb_cache_on`, `disk_flush_bitmap`, `pending_flushes` | kernel runtime state | not itself crash-persistent | sequencing evidence / outstanding durability obligation tracking |

Do not collapse them.

In particular:

```text
persistent recovery evidence
    != target state

volatile target embodiment
    != durable target state

runtime obligation tracking
    != crash-recovery metadata
```

---

## Engineering reconstruction

### E — command/BIO completion is not the strongest persistence boundary in the stack

The 2018 patch is a concrete counterexample to treating completion as a single universal event.

For a member with write-back cache enabled:

```text
home write accepted/completed
    ↓
may still reside in volatile device cache
    ↓
explicit cache flush completes
    ↓
PPL may close this I/O unit / allow subsequent log progress
```

So:

```text
write completion
    != power-loss durability closure
```

This reconstruction is grounded in the implementation's own added flush stage; it does not require assuming anything about a particular disk's internal cache design beyond the block layer's advertised write-cache semantics.

### E — durability obligations are selective, not global

The bitmap tracks only members that both participate in the current stripe work and advertise write-back cache.

Thus the implementation's obligation set is:

```text
O(io) = { member d |
          d participated in this I/O unit
          AND d has write-back cache enabled }
```

The I/O unit can close only after the required flushes for `O(io)` are accounted for.

This is a useful technical-retention pattern: **the system retains an explicit finite set of still-unclosed durability obligations rather than treating the whole device set as uniformly dirty.**

### E — a durable PPL record is intentionally kept authoritative while home-state durability remains unresolved

The reason the next PPL entry must wait is that the current PPL evidence may still be needed if power fails while the home writes exist only in volatile caches.

The sequence can therefore be reconstructed as:

```text
construct current PPL evidence
    ↓
write PPL with FUA
    ↓
submit home data/parity writes
    ↓
stripe BIOs complete
    ↓
flush participating write-back-cached members
    ↓
all required flushes complete
    ↓
current recovery obligation closes
    ↓
next PPL log submission may advance
```

The key point is authority/lifetime, not a claim that every byte of the old PPL record is physically erased at that exact instant.

### E — log durability and log retirement are different questions

`REQ_FUA` addresses the durability of the newly written PPL record.

The later member-cache flush stage addresses when it becomes safe to stop relying on that recovery record and advance PPL work.

Therefore:

```text
recovery record is durable
    != recovery record is already disposable
```

The first is a persistence question about the log. The second is a closure question about the target/home state.

### E — the runtime bitmap is obligation evidence, not persistent truth

`disk_flush_bitmap` and `pending_flushes` are in-memory control state. Losing them in a crash is not equivalent to losing the PPL record itself.

Their function is to prevent normal execution from retiring the I/O unit too early. If a crash occurs instead, recovery falls back to the durable PPL evidence and the documented dirty-start logic.

Thus:

```text
runtime sequencing state
    != post-crash recovery state
```

---

## Old and new contract boundary

### Linux 4.12 bounded contract

```text
PPL enabled
    + member volatile write-back cache disabled
    -> documented power-failure consistency contract
```

The implementation already issued the PPL log write with FUA, but did not insert the later per-member cache-flush stage after stripe write completion.

### 2018 / Linux 4.16-era bounded contract

```text
PPL enabled
    + member write-back cache may be enabled
    + participating cached members tracked
    + stripe writes complete
    + required cache flushes complete
    -> PPL I/O unit may close / subsequent PPL work may advance
```

This should **not** be back-projected into Linux 4.12.

Likewise, the Linux 4.12 warning should not be repeated as though it remained the implementation contract after the 2018 cache-flush support landed.

---

## Failure boundaries

Keep these separate:

1. power loss after PPL is durable but before some home writes complete;
2. power loss after home writes are acknowledged but while their device caches remain volatile;
3. flush command failure on one participating member;
4. a drive falsely advertising or violating cache-flush semantics;
5. media read/write failure independent of volatile-cache ordering;
6. loss of a member that exceeds PPL's documented recoverability assumptions;
7. corruption of the PPL record itself;
8. ordinary successful closure in which the PPL evidence can later be superseded/reused.

The 2018 patch materially addresses item 2 within the Linux/block-device contract. It does not make the other failure classes equivalent or disappear.

---

## Functional analogies

### A — write-ahead/redo-log retirement

At the relation level, PPL's 2018 sequencing resembles systems that keep durable recovery evidence until home-state writes have crossed the persistence boundary required to make that evidence unnecessary.

The safe analogy is:

```text
recovery evidence durable
    -> target/home state becomes durable
    -> recovery evidence may be retired/reused
```

This does not establish genealogy from database WAL, journaling filesystems, or controller redo logs.

### A — Case 04 mapping publication / retirement

Case 04 similarly distinguishes physical relocation, validation, mapping publication, and old-location retirement. Case 88 distinguishes log durability, home-write completion, cache durability closure, and log progress.

The shared abstraction is that **“new thing written” does not by itself prove the old authority/evidence may be forgotten.** The objects and failure models are different.

### A — Case 87 / block-cache durability vocabulary

Case 87 distinguishes command completion, volatile cache, non-volatile cache, and medium commitment at a storage-interface level. Case 88 gives a concrete array implementation that consumes an analogous lower-layer distinction.

This is a functional comparison only. Do not import SCSI terminology into the historical Linux PPL source unless the source actually uses it.

---

## Philosophical interpretation

No philosophical premise is required for the historical claim.

A downstream project interpretation is nevertheless useful:

> A system may have already “done the write” in one operational sense while still retaining evidence that the write is not yet safe to forget in a stronger failure model.

The important point is not semantic wordplay around `complete`. It is that **different layers grant different kinds of closure**:

```text
submitted
    != block-layer completed
    != volatile-cache drained
    != recovery evidence disposable
```

These are project interpretations, not language attributed to Linux developers.

---

## Explicit non-claims

This deepening does **not** claim that:

- Linux PPL invented cache flushing, FUA, write-ahead logging, parity logging, or RAID write-hole protection;
- commit `1532d9e...` is the first storage system ever to permit RAID with volatile member caches;
- every member home write is itself issued with FUA;
- PPL “uses FUA everywhere” — the checked code uses FUA for the PPL log BIO and a separate preflush path for relevant member caches;
- cache-flush completion proves an individual drive's firmware cannot lie, lose data outside the modeled contract, or suffer unrelated media failure;
- `disk_flush_bitmap` is persistent on-disk metadata;
- a PPL I/O unit finishing means the interrupted application transaction has database/filesystem-level atomicity;
- PPL protects all in-flight user data;
- PPL repairs failed members or restores redundancy margin;
- the 2018 patch changes the mathematical partial-parity recovery relation established by the 2017 case;
- the code proves exact platter/NAND physical residency rather than the durability semantics exported by the block device;
- all Linux downstream/vendor kernels acquired the change on the same date as upstream;
- the companion `computing-archaeology` repository already contains a historical lineage for this mechanism.

---

## What this closes in Case 88

The canonical Case 88 ended with the open item:

> `modern PPL cache-flush evolution`

That broad mechanism debt is now closed for the upstream 2018 transition represented by commit `1532d9e87e8b2377f12929f9e40724d5fbe6ecc5` and checked Linux `v4.16` source.

The refined remaining questions are narrower:

- fault injection at each boundary: after PPL FUA completion, after some home-write completions, during member cache flush, and immediately before the next PPL entry;
- exact behavior and array-state consequences after a cache-flush error marks a member faulty;
- later changes to block-layer cache/FUA APIs that alter implementation details without changing the conceptual obligation;
- hardware that misreports or violates flush/FUA guarantees;
- interaction of PPL with device power-loss protection / nonvolatile write cache;
- later PPL changes affecting multiple PPL areas, wrap/reuse, or queueing;
- exact upstream/downstream backport history;
- end-to-end validation that the documented closure survives real controller, HBA, firmware, and power-cut combinations.

These are implementation/fault-model questions. They are no longer the generic question of whether upstream Linux added a member-cache flush stage.

---

## Claim ledger

| Claim | Type | Status |
| --- | --- | --- |
| Linux v4.12 PPL docs require volatile member write-back cache to be disabled | H/P | grounded |
| Linux v4.12 PPL log BIO uses `REQ_FUA` | H/P | grounded |
| v4.12 finishes the PPL I/O unit after the final stripe-write completion without the later per-member flush stage | H/P | grounded |
| commit `1532d9e...` adds support for PPL with member write-back cache enabled | H/P | grounded |
| the 2018 code tracks cached members that actually participate in writes | H/P | grounded |
| the 2018 code submits `REQ_PREFLUSH` BIOs to relevant members after stripe writes complete | H/P | grounded |
| the I/O unit remains live until all required flush completions are accounted for | H/P | grounded |
| the v4.16 documentation no longer carries the v4.12 blanket cache-disable warning | H/P | grounded |
| stripe-write completion is weaker than the durability closure required before subsequent PPL log progress | E | supported reconstruction |
| durable recovery evidence can remain necessary after target writes have completed at a weaker interface boundary | E | supported reconstruction |
| `disk_flush_bitmap` is crash-persistent metadata | X | rejected |
| all member home writes use FUA | X | rejected |
| flush support makes PPL a full user-data journal | X | rejected |
| upstream Linux patch proves compliant behavior of every real disk/controller | X | rejected |

---

## Sources

### Primary Linux source

- Linux `v4.12`, **Partial Parity Log** documentation: <https://github.com/torvalds/linux/blob/v4.12/Documentation/md/raid5-ppl.txt>
- Linux `v4.12`, `drivers/md/raid5-ppl.c`: <https://github.com/torvalds/linux/blob/v4.12/drivers/md/raid5-ppl.c>
- Tomasz Majchrzak / Shaohua Li, **`raid5-ppl: PPL support for disks with write-back cache enabled`**, commit `1532d9e87e8b2377f12929f9e40724d5fbe6ecc5`: <https://github.com/torvalds/linux/commit/1532d9e87e8b2377f12929f9e40724d5fbe6ecc5>
- Linux `v4.16`, `drivers/md/raid5-ppl.c`: <https://github.com/torvalds/linux/blob/v4.16/drivers/md/raid5-ppl.c>
- Linux `v4.16`, **Partial Parity Log** documentation: <https://github.com/torvalds/linux/blob/v4.16/Documentation/md/raid5-ppl.txt>

### Existing Case 88 grounding / prior-art boundary

- [`../cases/88-linux-md-raid5-partial-parity-log.md`](../cases/88-linux-md-raid5-partial-parity-log.md)
- Stodolsky, Holland, Gibson, **“Parity Logging: Overcoming the Small Write Problem in Redundant Disk Arrays,”** ISCA 1993 — retained in the canonical case as earlier parity-logging prior art.
- Digital Equipment Corporation, **Enhanced raid write hole protection and recovery**, US5774643A, filed 1995 — retained in the canonical case as earlier write-hole recovery prior art.

---

## Maturity judgment

**Case 88 remains `grounded`.**

This evidence materially improves the implementation boundary because it closes the canonical case's broad “modern cache-flush evolution” debt with upstream source and a named commit. It does not justify a maturity promotion because real power-cut fault injection, device noncompliance behavior, downstream backport coverage, and later API evolution remain outside this slice.

The retained result is:

```text
PPL record durable
    ↓
home stripe writes complete
    ↓
participating volatile member caches still owe durability closure
    ↓
required cache flushes complete
    ↓
PPL I/O unit may close / later log work may advance
```

and therefore:

```text
write completed
    != write durability obligation retired
```
