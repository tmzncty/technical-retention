# Case 88 evidence deepening — Linux MD PPL flush-error / member-fault transition (2018)

## Status

**Bounded implementation deepening for Case 88 — grounded.**

This file closes one narrow debt left by [`88-linux-md-2018-ppl-writeback-cache-flush-boundary-deepening.md`](88-linux-md-2018-ppl-writeback-cache-flush-boundary-deepening.md):

> When a PPL-triggered member-cache flush itself completes with an error, does Linux MD treat that callback as proof of durability, wait forever for a successful flush, or transfer the unresolved persistence problem into another array state?

The checked Linux 4.16 path does the third thing. The failed flush is reported through `md_error()`, RAID5 marks the member `Faulty`, clears `In_sync`, recomputes the degraded count, blocks the device while metadata state changes are propagated, and schedules recovery work. Independently, the asynchronous `pending_flushes` accounting still retires that flush callback; when all callbacks/accounting slots have closed, the PPL I/O unit can finish.

The bounded result is therefore:

```text
flush callback accounted
    != flush succeeded
    != member home state proved durable
```

and, more importantly:

```text
failed durability closure
    -> member loses current in-sync authority
    -> array continues, if its remaining redundancy permits
    -> recovery/repair obligation is raised
```

This is not a claim that the failed device physically lost data, that every array can continue after such an error, or that source inspection substitutes for hardware power-cut validation.

---

## Source boundary

### Primary implementation sources

1. Tomasz Majchrzak / Shaohua Li, Linux commit `1532d9e87e8b2377f12929f9e40724d5fbe6ecc5`, **`raid5-ppl: PPL support for disks with write-back cache enabled`**, committed 2018-01-15:
   <https://github.com/torvalds/linux/commit/1532d9e87e8b2377f12929f9e40724d5fbe6ecc5>
2. Linux `v4.16`, `drivers/md/raid5-ppl.c`:
   <https://github.com/torvalds/linux/blob/v4.16/drivers/md/raid5-ppl.c>
3. Linux `v4.16`, `drivers/md/md.c`:
   <https://github.com/torvalds/linux/blob/v4.16/drivers/md/md.c>
4. Linux `v4.16`, `drivers/md/raid5.c`:
   <https://github.com/torvalds/linux/blob/v4.16/drivers/md/raid5.c>

The prior Case 88 deepening already established why the flush stage exists: with member write-back cache enabled, PPL keeps the current I/O unit open after stripe BIO completion, issues `REQ_PREFLUSH` to participating cached members, and does not advance ordinary PPL sequencing until those asynchronous flush operations are accounted for.

### Companion-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `raid5-ppl` found no dedicated PPL / flush-error technical-history packet to reuse. This record therefore keeps only the retention-specific state transition. A broader Linux MD / Intel IMSM / block-layer flush genealogy still belongs primarily there.

---

## Historical record

### H/P — PPL distinguishes a failed flush callback from an ordinary successful callback

In Linux `v4.16`, `ppl_do_flush()` creates zero-data BIOs with:

```text
REQ_OP_WRITE | REQ_PREFLUSH
```

for relevant non-faulty RAID members whose write-back-cache state creates a flush obligation.

The completion callback `ppl_flush_endio()` checks `bio->bi_status`. If that status reports an error, the callback looks up the `md_rdev` corresponding to the BIO's block device and calls:

```c
md_error(rdev->mddev, rdev);
```

The implementation therefore does **not** silently reinterpret a failed cache flush as a successful durability confirmation.

### H/P — completion accounting proceeds even when the flush reports failure

After the error branch, `ppl_flush_endio()` releases the BIO and then decrements `io->pending_flushes` regardless of whether `bio->bi_status` indicated success or failure.

When the decrement closes the last pending slot, the code calls:

```c
ppl_io_unit_finished(io);
md_wakeup_thread(conf->mddev->thread);
```

Thus `pending_flushes` is an **asynchronous-operation accounting counter**, not a success counter.

Historically accurate wording is therefore:

```text
all required flush callbacks/accounting slots closed
```

not:

```text
all member caches successfully became durable
```

The latter is true only for members whose flush path actually succeeded under the block-device contract.

### H/P — already-faulty or unavailable members are not used as reasons to wait forever

`ppl_do_flush()` initializes `pending_flushes` from the RAID-disk count, but submits a flush only when the selected slot resolves to an `rdev` and that member is not already marked `Faulty`.

Slots that do not result in a submitted flush are subsequently decremented out of the pending count. This fits the same implementation rule: the counter tracks whether the PPL unit still has asynchronous flush work outstanding, not whether every nominal array slot produced a successful durability event.

### H/P — generic MD error handling delegates the failure to the RAID personality and schedules recovery

Linux `v4.16` `md_error()` first ignores a missing or already-`Faulty` `rdev`. Otherwise, if the active MD personality supplies an error handler, it invokes that handler.

After the personality-specific transition, generic MD:

- sets `MD_RECOVERY_RECOVER` when the array is degraded;
- notifies the device-state sysfs attribute;
- sets `MD_RECOVERY_INTR`;
- sets `MD_RECOVERY_NEEDED`.

A PPL flush error therefore enters the ordinary MD failure/recovery machinery instead of being retained solely as a PPL-local status bit.

### H/P — RAID5's error handler disqualifies the member from the in-sync set

For RAID5/6 in Linux `v4.16`, the personality's `.error_handler` is `raid5_error`.

`raid5_error()`:

```text
sets Faulty on the rdev
clears In_sync on the rdev
recalculates mddev->degraded
sets MD_RECOVERY_INTR
sets Blocked on the rdev
marks MD superblock device-state change/pending flags
reports the disk failure and continuing-device count
```

The critical retention fact is the loss of `In_sync` authority. The implementation does not need to prove the exact physical contents of the failing drive before excluding that embodiment from the set trusted as an ordinary current RAID member.

### H/P — the PPL I/O unit can finish after the member has been faulted

The same `ppl_flush_endio()` that calls `md_error()` still closes its pending asynchronous slot. Consequently, after the failed member has been transferred into MD's fault/degraded-state machinery, the PPL I/O unit need not remain permanently pinned waiting for a successful flush from that same embodiment.

This is an implementation-level handoff:

```text
PPL-local flush obligation
    -> flush error
    -> MD member-fault / degraded-array state
    -> recovery machinery
```

It is not a claim that the array has already regained full redundancy.

---

## Engineering reconstruction

### E — operation completion evidence and success evidence are different state classes

The prior deepening established a runtime set of outstanding cache-flush obligations. This follow-up shows that the set closes on **callback accounting**, while semantic success is handled separately.

For one member `d`:

```text
flush submitted(d)
    ↓
callback arrives(d)
    ├─ success -> member remains eligible as current/in-sync
    └─ error   -> md_error -> Faulty + !In_sync + degraded/recovery state
```

In both branches the asynchronous callback is no longer outstanding.

Therefore:

> **completion accounting != successful durability qualification**.

### E — a failed durability obligation can be converted into a membership/currentness obligation

Before the flush returns, the problem is:

```text
this participating member may still contain the newest home write only in volatile cache
```

After a flush error and `raid5_error()`, Linux no longer treats that member as an ordinary `In_sync` contribution. The preservation problem changes form:

```text
unclosed member-cache durability
    -> member disqualification
    -> degraded redundancy
    -> recovery / replacement obligation
```

That is a stronger statement than “Linux logs an error,” but it remains an engineering reconstruction of the checked state transitions, not historical Linux terminology.

### E — a PPL I/O unit finishing is not a universal all-members-durable certificate

The earlier shorthand:

```text
all required flushes complete
    -> PPL I/O unit may finish
```

needs a typed reading. In the checked implementation, `ppl_io_unit_finished()` may be reached after:

1. all submitted flushes return successfully; **or**
2. one or more submitted flushes return errors, those members are passed through MD failure handling, and all asynchronous pending slots are accounted for.

Therefore:

```text
PPL I/O unit finished
    != every originally participating member proved durable
```

A more precise relation is:

```text
PPL I/O unit finished
    -> no PPL-local flush callback remains outstanding
    + failed members, if any, have been transferred into MD fault handling
```

### E — authority can be preserved by exclusion rather than by proving a suspect copy correct

The RAID5 handler does not need a forensic determination of whether the cache-flush failure actually destroyed the member's newest bytes. It changes the member's authority relation:

```text
physical device may still contain readable bytes
    != device remains an In_sync authoritative array member
```

This mirrors a broader repository rule already visible in distributed and mapped-storage cases: **physical presence is weaker than currentness/admissibility**.

Here, however, the historical mechanism is Linux MD RAID membership, not a distributed quorum or Flash FTL mapping.

### E — fault transition closes one obligation by creating another

The system does not make the problem disappear. It changes the retained state that matters:

```text
runtime flush debt
    ↓ error
member Faulty / !In_sync / Blocked
    ↓
array degraded state + recovery-needed state
    ↓
future reconstruction / spare activation / repair path
```

So:

> **obligation retirement != system returned to full health**.

The flush obligation can cease to be the active control relation because the suspect member has ceased to be trusted as a normal current embodiment. A separate repair obligation then remains.

### E — this is not proof that a flush error means physical data loss

The source proves the software policy transition, not the medium's exact post-error contents.

A flush can fail for reasons that do not permit a source-only inference about which cache lines or sectors reached stable media. Linux reacts conservatively by changing member authority.

Therefore:

```text
flush error
    != demonstrated physical loss of every affected sector
```

and also:

```text
bytes still readable from failed member
    != safe basis for treating it as In_sync
```

---

## State decomposition added by this slice

Case 88 should now keep at least these additional state/evidence classes distinct:

| State / evidence | Lifetime / location | Role |
| --- | --- | --- |
| `bio->bi_status` for one flush | completion-time runtime evidence | says whether that flush operation succeeded under the block layer |
| `pending_flushes` | PPL I/O-unit runtime state | counts unresolved asynchronous flush-accounting slots |
| `Faulty` | MD member state | disqualifies failed member from normal use |
| `In_sync` | MD member currentness/qualification state | says whether member counts as synchronized array contribution |
| `Blocked` | MD member control state | blocks the device while failure/metadata handling proceeds |
| `mddev->degraded` | array runtime/state summary | records reduced qualified-member set |
| MD recovery flags | array recovery control state | schedules/interrupts follow-up recovery work |
| persistent PPL record | member metadata area | crash-recovery evidence for parity consistency |

These are related but not interchangeable:

```text
flush result
    != pending-operation count
    != member currentness
    != array redundancy margin
    != PPL recovery evidence
```

---

## Functional analogies only

### A — replica exclusion after failed durability qualification

At a very abstract level, this resembles a replicated system that stops counting a copy after the copy fails a durability/currentness qualification and continues with a reduced trusted set.

The analogy stops at that relation. Linux MD RAID5 parity, distributed replica protocols, and quorum systems have different mathematics, failure models, authority rules, and histories.

### A — Case 17 degraded RAID state

Case 17 supplies the broader distinction between degraded service, mathematical reconstructability, and restored redundancy margin. This Case 88 deepening shows one concrete path by which a **durability-control failure during an update** can produce a degraded-member transition.

Do not reverse the comparison: not every degraded RAID transition originates in a cache-flush failure.

### A — Case 87 interface durability

Case 87 explains why a cache flush is a durability-control operation rather than a payload write. Case 88 now adds the array-side response when that control operation itself fails.

The shared relation is functional only:

```text
persistence request issued
    != persistence request succeeded
```

---

## Philosophical interpretation

No philosophy is required for the historical result.

A narrow project interpretation is defensible:

> Technical retention can preserve correctness not only by making a suspect embodiment durable, but by **withdrawing authority from that embodiment** and transferring the future-retention burden to redundancy and repair.

The point is not that “failure is memory.” It is that the system retains enough control state to know which physical survivor must no longer count as a trustworthy current contribution.

This interpretation stops at the implementation boundary. Linux developers are not being credited with this philosophical vocabulary.

---

## Explicit non-claims

This deepening does **not** claim that:

- a failed `REQ_PREFLUSH` proves all data in that drive's volatile cache was lost;
- a drive returning a flush error is physically dead;
- every RAID5 array can continue after one more failed member;
- `ppl_io_unit_finished()` means the original application transaction is durable or atomic;
- the persistent PPL record itself is erased when the I/O unit finishes;
- `pending_flushes` is a success counter;
- `Faulty` / `In_sync` are PPL-private metadata — they belong to MD/RAID state;
- the PPL flush-error path restores redundancy margin;
- source inspection demonstrates real-device compliance with FUA/PREFLUSH semantics;
- this is first-invention evidence for faulted-member exclusion, RAID recovery, or failed-flush handling;
- the checked v4.16 behavior is unchanged in every later kernel or vendor backport.

---

## Prior-art / genealogy boundary

This record makes no new invention claim. It is an implementation deepening of the already-grounded 2017–2018 Linux PPL case.

The broad histories of RAID member failure, Linux MD recovery, SCSI/ATA flush semantics, controller caches, and Intel IMSM belong primarily in `computing-archaeology` if developed. Here they are included only to explain the retention-specific transition from an unresolved durability obligation to a member-authority/recovery obligation.

---

## Resulting bounded relations

```text
flush BIO callback != successful flush
pending_flushes reaching zero != every member durable
flush failure != proven physical data loss
physical readability != In_sync authority
failed durability closure -> member disqualification + degraded/recovery state
member disqualification != restored redundancy
PPL I/O-unit retirement != application-level atomic durability
runtime flush debt != persistent PPL recovery evidence
obligation transfer != obligation disappearance
```

---

## Remaining evidence debt

The broad `exact state transition after a member cache-flush error` debt is closed for the checked upstream v4.16 implementation. Useful narrower work remains:

- fault-injection tests that force `REQ_PREFLUSH` failure and observe `Faulty`, `In_sync`, `Blocked`, degraded count, superblock update, and recovery behavior end to end;
- behavior when the array is already degraded before the flush error and the new fault exceeds available parity margin;
- whether later kernels changed PPL flush-error handling, block-layer status propagation, or MD fault sequencing;
- controller/HBA behavior that transforms or suppresses flush errors;
- devices that falsely report successful flush/FUA completion;
- real power-cut validation around PPL log FUA, home writes, cache flush, and post-error recovery;
- downstream stable/vendor backports of commit `1532d9e...` and any later fixes.

Case 88 remains **`grounded`**. This slice deepens the implementation boundary; it does not justify a maturity promotion.