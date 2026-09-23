# Case 88 — Linux MD RAID5 PPL evidence index

## Status

**Case status: grounded**

This file is the compact evidence navigation for [`Case 88 — Linux MD RAID5 Partial Parity Log`](../cases/88-linux-md-raid5-partial-parity-log.md).

It does not replace the canonical case. It keeps three implementation layers separate:

1. the original 2017 partial-parity recovery relation;
2. the 2018 member write-back-cache durability-closure path;
3. the 2018 flush-error transition from a PPL-local durability obligation into MD member-fault / degraded-array state.

No maturity promotion is made by this index.

---

## Canonical case

- [`../cases/88-linux-md-raid5-partial-parity-log.md`](../cases/88-linux-md-raid5-partial-parity-log.md)

Canonical bounded question:

> What must be retained before a parity-stripe update begins when the data/parity writes cannot be assumed to become durable atomically?

The Linux 4.12 grounding establishes:

```text
old/current stripe relation available
    ↓
calculate + persist partial-parity recovery evidence
    ↓
ordinary data/parity writes may proceed
```

with the central negative boundary:

```text
write-hole protection
    != preservation of all interrupted user data
```

The initial implementation also exposed a lower-layer durability dependency: volatile member-drive write-back cache had to be disabled for the documented power-failure guarantee.

---

## Evidence chain 1 — 2017 Linux MD PPL grounding

### Record

- canonical case: [`../cases/88-linux-md-raid5-partial-parity-log.md`](../cases/88-linux-md-raid5-partial-parity-log.md)
- grounding: [`88-linux-1993-2017-raid5-ppl-grounding.md`](88-linux-1993-2017-raid5-ppl-grounding.md)

### Primary anchors

- Artur Paszkiewicz, commit `3418d036c81dcb604b7c7c71b209d5890a8418aa`, `raid5-ppl: Partial Parity Log write logging implementation`;
- Linux 4.12 PPL documentation and source;
- Shaohua Li, `[GIT PULL] MD update for 4.12`;
- 1993 parity-logging research and 1995-filed DEC write-hole-recovery prior art, used only to block first-invention inflation.

### Established relations

```text
parity bytes present
    != parity relation current
```

```text
compact partial-parity recovery evidence
    != complete duplicate of in-flight payload
```

```text
PPL parity-consistency recovery
    != full write journal
```

```text
software issue ordering
    != lower-layer power-failure durability
```

### Status

**grounded in canonical case**

---

## Evidence chain 2 — 2018 member write-back-cache durability closure

- [`88-linux-md-2018-ppl-writeback-cache-flush-boundary-deepening.md`](88-linux-md-2018-ppl-writeback-cache-flush-boundary-deepening.md)

### Scope

Upstream Linux commit `1532d9e87e8b2377f12929f9e40724d5fbe6ecc5`, committed 2018-01-15, checked against Linux `v4.12` and `v4.16` source.

### Historical result

The implementation moves from the Linux 4.12 restriction:

```text
PPL
    + volatile member write-back cache disabled
```

to a path that can admit member write-back cache by retaining and closing per-I/O-unit flush obligations:

```text
PPL log BIO written with FUA
    ↓
home data/parity writes submitted
    ↓
track participating members with write-back cache enabled
    ↓
all stripe write BIOs complete
    ↓
submit REQ_PREFLUSH to relevant members
    ↓
account for asynchronous flush completions
    ↓
finish PPL I/O unit / allow later PPL work to advance
```

Relevant runtime state includes:

- per-member `wb_cache_on`;
- `disk_flush_bitmap`;
- per-I/O-unit `pending_flushes`.

These are execution/sequencing state, not the persistent PPL recovery record.

### Established relations

```text
stripe write completion
    != member-cache durability closure
```

```text
PPL record durable
    != home state already durable
```

```text
recovery evidence durable
    != recovery evidence already disposable
```

```text
runtime flush-obligation tracking
    != persistent crash-recovery metadata
```

### Status

**bounded deepening complete**

The broad `modern PPL cache-flush evolution` debt is closed for the checked upstream 2018 transition.

---

## Evidence chain 3 — 2018 flush error transfers authority to MD fault/recovery state

- [`88-linux-md-2018-ppl-flush-error-fault-transition-deepening.md`](88-linux-md-2018-ppl-flush-error-fault-transition-deepening.md)

### Scope

The exact Linux `v4.16` path from `ppl_flush_endio()` through generic `md_error()` to RAID5's `raid5_error()`.

### Primary anchors

- Linux `v4.16`, `drivers/md/raid5-ppl.c`;
- Linux `v4.16`, `drivers/md/md.c`;
- Linux `v4.16`, `drivers/md/raid5.c`;
- the same upstream `1532d9e...` commit that introduced the PPL flush stage.

### Historical result

When one PPL-issued member-cache flush returns an error:

```text
ppl_flush_endio sees bio->bi_status error
    ↓
resolve corresponding md_rdev
    ↓
md_error()
    ↓
RAID5 raid5_error()
    ↓
set Faulty
clear In_sync
recalculate degraded count
set Blocked
mark device-state metadata change/pending
set recovery-related flags
```

The callback then still retires its asynchronous `pending_flushes` slot. When no PPL-local flush callback remains outstanding, the I/O unit can finish.

### Established relations

```text
flush callback accounted
    != flush succeeded
```

```text
pending_flushes == 0
    != every originally participating member proved durable
```

```text
flush error
    != demonstrated physical loss of every affected byte
```

```text
physical bytes may remain readable
    != member remains In_sync authoritative
```

```text
failed durability closure
    -> member disqualification
    -> degraded/recovery obligation
```

```text
PPL-local obligation retired
    != array returned to full health
```

### Status

**bounded deepening complete**

The former open item `exact state transition after a member cache-flush error and resulting MD fault handling` is now closed for the checked upstream v4.16 implementation. Fault injection, already-degraded-array behavior, later kernel evolution, and hardware compliance remain open.

---

## Consolidated state decomposition

Case 88 now distinguishes at least these classes:

| State / relation | Where | Role | What it is not |
| --- | --- | --- | --- |
| user-data chunks | RAID member home locations | payload contribution | complete transaction history |
| ordinary parity chunk | RAID member home location | redundancy contribution | proof parity is current |
| PPL partial parity | member PPL metadata area | crash-recovery relation | full data journal |
| PPL header / sequence / location metadata | member PPL area | identify and validate recovery evidence | user payload |
| PPL-log FUA completion | block/device durability contract | log-record persistence boundary | proof home writes are durable |
| home data/parity write completion | RAID write path | weaker completion evidence | necessarily power-loss-safe state with WBC enabled |
| volatile member write-back cache | member device | intermediate accepted write state | stable-medium state by definition |
| `wb_cache_on` | kernel runtime | capability/property used by PPL | persistent repair record |
| `disk_flush_bitmap` | kernel runtime | participating cached members owing flush | on-disk bitmap |
| `pending_flushes` | kernel runtime | unresolved asynchronous flush accounting | number of successful flushes |
| flush `bio->bi_status` | callback-time runtime evidence | success/error result for one flush | persistent PPL state |
| `Faulty` / `In_sync` | MD member state | member admissibility/currentness | physical content map |
| `Blocked` | MD member control state | failure/metadata transition gating | proof media is unreadable |
| `mddev->degraded` | MD array state | reduced qualified-member summary | restored redundancy margin |
| MD recovery flags | MD array control state | request follow-up recovery handling | repair completion |
| dirty-start PPL recovery relation | recovery path | restore parity consistency after interruption | newest application transaction guarantee |

Compactly:

```text
payload
    != parity relation
    != persistent recovery evidence
    != target-write completion
    != volatile-cache state
    != flush result
    != runtime pending-operation count
    != member currentness/admissibility
    != degraded-array state
    != repair completion
```

---

## Evidence-lifetime / obligation-transfer model

The three evidence chains together support a more precise lifecycle than the earlier shorthand “PPL logs the write”:

```text
create recovery evidence before vulnerable update
    ↓
keep it authoritative while target outcome is unresolved
    ↓
close ordinary home-write BIOs
    ↓
for relevant cached members, request cache flush
    ↓
for each submitted flush:
    ├─ success -> durability qualification for that member under the interface contract
    └─ error   -> withdraw In_sync authority / enter degraded-recovery state
    ↓
no PPL-local flush callback remains outstanding
    ↓
PPL I/O unit may finish
```

The central new rule is:

> **an outstanding durability obligation can cease to be a PPL-local obligation either because it succeeds or because the suspect embodiment is disqualified and the preservation burden moves into degraded-array recovery.**

This must not be shortened to “errors count as successful flushes.” They do not.

---

## Historical record / reconstruction discipline

### Historical record

Source-level facts include:

- Linux 4.12 PPL writes partial parity before ordinary member writes;
- the initial volatile-member-cache prohibition;
- PPL log BIO use of `REQ_FUA`;
- commit `1532d9e...` adding write-back-cache support;
- `REQ_PREFLUSH` submission to relevant non-faulty members;
- `ppl_flush_endio()` checking `bio->bi_status`;
- a failed flush calling `md_error()` for the corresponding `md_rdev`;
- `md_error()` delegating to the RAID personality and setting recovery flags;
- RAID5 binding `.error_handler = raid5_error`;
- `raid5_error()` setting `Faulty`, clearing `In_sync`, recomputing degraded state, setting `Blocked`, and marking member-state metadata change;
- `pending_flushes` being decremented after both successful and failed callback paths.

### Engineering reconstruction

Project abstractions include:

- `durability closure`;
- `outstanding durability obligation set`;
- `completion accounting` versus `success evidence`;
- `obligation transfer`;
- `member authority withdrawal`;
- `recovery-evidence authority lifetime`.

These terms summarize checked implementation relations. They are not historical Linux vocabulary.

### Functional analogy

Comparisons with replica exclusion, quorum membership, database WAL retirement, or other currentness systems are relation-level analogies only. They do not establish genealogy or shared failure mathematics.

### Philosophical interpretation

A bounded interpretation may note that correctness can be preserved by withdrawing authority from a suspect embodiment rather than proving that embodiment durable. This is a project interpretation, not language attributed to Linux developers.

---

## Cross-case boundaries

### Case 17 — degraded RAID / repair margin

Case 17 distinguishes mathematical reconstructability, degraded service, and restored redundancy margin. Case 88 now supplies one concrete route into degraded state:

```text
cache-durability control failure
    -> member disqualification
    -> degraded RAID state
```

Not every degraded transition is a cache-flush failure, and the flush-error transition does not itself restore margin.

### Case 87 — storage-interface durability controls

Case 87 separates write completion, volatile cache, medium commitment, FUA, and synchronization. Case 88 consumes that lower-layer distinction and adds:

```text
persistence request issued
    != persistence request succeeded
```

Do not rewrite the Linux PPL source in SCSI vocabulary it does not use.

### Case 04 — mapped-Flash currentness / retirement

Both cases show that physical survival and current authority are separable. Case 04 does so through logical-to-physical mapping; Case 88 does so through RAID member qualification after an I/O-control failure.

The shared shape is functional only:

```text
physical embodiment exists
    != embodiment currently counts
```

### Case 96 — persistent repair progress versus in-core worker state

Case 96 keeps long-running repair progress distinct from runtime worker state. Case 88 similarly separates persistent PPL recovery evidence from in-core flush tracking, but the lifetimes and roles differ sharply.

---

## Current open work

With both the broad 2018 cache-flush evolution and the checked v4.16 flush-error state transition closed, useful remaining slices are narrower:

- power-cut fault injection at each PPL/FUA/home-write/flush boundary;
- forced `REQ_PREFLUSH` failure tests that observe `Faulty`, `In_sync`, `Blocked`, degraded count, superblock update, and recovery end to end;
- behavior when the array is already degraded before the flush error and another member is disqualified;
- hardware/controller/HBA paths that lie about, suppress, or transform FUA/PREFLUSH completion/error semantics;
- devices with genuine power-loss-protected or nonvolatile write cache;
- later Linux block-layer/API and MD/PPL error-path evolution;
- PPL multiple-area/wrap/reuse evolution after the checked 4.16-era source;
- exact upstream stable/downstream backport history;
- named hardware fault-injection validation with write-back caches enabled;
- broader Linux MD PPL / Intel IMSM lineage in `computing-archaeology` if that history becomes useful.

---

## Maturity judgment

**grounded — unchanged**

Why no promotion:

- the 2017 mechanism is source-grounded;
- the 2018 cache-flush evolution is source-grounded and checked against tagged code;
- the flush-error handoff into MD/RAID5 fault state is now source-grounded;
- historical prior art already blocks first-invention inflation;
- but hardware power-cut/fault-injection validation is still absent;
- later kernel/backport history is not exhaustively covered;
- block-device compliance remains an external assumption rather than a property proved by source inspection.

The correct update is therefore **deeper implementation grounding and better navigation, not a maturity-level increase**.