# Case 88 — Linux MD RAID5 PPL evidence index

## Status

**Case status: grounded**

This file is the compact evidence navigation for [`Case 88 — Linux MD RAID5 Partial Parity Log`](../cases/88-linux-md-raid5-partial-parity-log.md).

It does not replace the canonical case. Its purpose is to keep the evidence chain navigable while preserving the distinctions among:

- parity/currentness relation;
- persistent PPL recovery evidence;
- ordinary home data/parity writes;
- volatile device write-back cache state;
- runtime durability-obligation tracking;
- recovery-evidence retirement/reuse.

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

and the central negative boundary:

```text
write-hole protection
    != preservation of all interrupted user data
```

The canonical case also records an original implementation limitation: volatile write-back cache was required to be disabled on all member drives when PPL was used.

### Status

**grounded**

---

## Evidence chain 1 — 2017 Linux MD PPL grounding

### Scope

Linux 4.12-era PPL implementation, documentation, integration context, and earlier parity-logging/write-hole prior art.

### Primary anchors

- Artur Paszkiewicz, commit `3418d036c81dcb604b7c7c71b209d5890a8418aa`, `raid5-ppl: Partial Parity Log write logging implementation`;
- Linux 4.12 `Documentation/md/raid5-ppl.txt`;
- Shaohua Li, `[GIT PULL] MD update for 4.12`;
- 1993 Stodolsky/Holland/Gibson parity-logging work and 1995-filed DEC write-hole-recovery prior art, used only to block first-invention claims.

### Established relations

```text
parity bytes present
    != parity relation current
```

```text
compact recovery evidence
    != complete duplicate of in-flight payload
```

```text
PPL protects parity/reconstruction consistency
    != PPL is a full write journal
```

```text
software issue ordering
    != lower-layer power-failure durability
```

### Original cache boundary

The Linux 4.12 documentation explicitly required volatile member-drive write-back caches to be disabled for the stated power-failure consistency guarantee.

The same implementation submitted the PPL log BIO with `REQ_FUA`, but it had no later per-member cache-flush stage after ordinary stripe writes completed.

### Status

**grounded in canonical case**

---

## Evidence chain 2 — 2018 member write-back-cache flush boundary

- [`88-linux-md-2018-ppl-writeback-cache-flush-boundary-deepening.md`](88-linux-md-2018-ppl-writeback-cache-flush-boundary-deepening.md)

### Scope

Upstream Linux commit `1532d9e87e8b2377f12929f9e40724d5fbe6ecc5`, committed 2018-01-15, checked against Linux `v4.12` and `v4.16` source.

### Primary anchors

- commit `1532d9e...` — `raid5-ppl: PPL support for disks with write-back cache enabled`;
- Linux `v4.12` `raid5-ppl.txt` and `raid5-ppl.c`;
- Linux `v4.16` `raid5-ppl.txt` and `raid5-ppl.c`.

### Historical result

The implementation changes from:

```text
PPL
    + volatile member write-back cache disabled
```

to a path that can admit member write-back cache by explicitly retaining and closing a per-I/O-unit flush obligation:

```text
PPL log BIO written with FUA
    ↓
home data/parity writes submitted
    ↓
track participating members with write-back cache enabled
    ↓
all stripe write BIOs complete
    ↓
submit cache flushes to those members
    ↓
wait for all required flush completions
    ↓
finish PPL I/O unit / allow subsequent PPL work to advance
```

The relevant runtime state includes:

- per-member `wb_cache_on`;
- `disk_flush_bitmap`;
- per-I/O-unit `pending_flushes`.

These are execution/sequencing state, not the persistent PPL recovery record itself.

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

The former broad TODO `modern PPL cache-flush evolution` is closed for this upstream 2018 transition. Remaining work is narrower fault-injection, later API evolution, device noncompliance, and backport history.

---

## Consolidated state decomposition

Case 88 now distinguishes at least the following classes:

| State / relation | Where | Role | What it is not |
| --- | --- | --- | --- |
| user-data chunks | RAID member home locations | payload contribution | complete transaction history |
| ordinary parity chunk | RAID member home location | redundancy contribution | proof parity is current |
| PPL partial parity | member PPL metadata area | crash-recovery relation | full data journal |
| PPL header / sequence / location metadata | member PPL metadata area | identify and validate recovery evidence | user payload |
| PPL-log FUA completion | block/device durability contract | establish log-record persistence boundary | proof home writes are durable |
| home data/parity write completions | RAID write path | weaker completion evidence | necessarily power-loss-safe target state when WBC is enabled |
| device volatile write-back cache contents | RAID members | intermediate accepted write state | durable media state by definition |
| `wb_cache_on` | kernel runtime | capability/queue property used by PPL | persistent repair record |
| `disk_flush_bitmap` | kernel runtime | set of participating cached members owing flush | on-disk bitmap |
| `pending_flushes` | kernel runtime | counts unresolved flush completions | crash-surviving log state |
| dirty-start PPL recovery relation | recovery path | decide how to restore parity consistency | newest application transaction guarantee |

Compactly:

```text
payload
    != parity relation
    != recovery evidence
    != target-write completion
    != volatile-cache state
    != cache-durability closure
    != runtime obligation tracking
```

---

## Evidence-lifetime model

The two evidence chains together establish a useful lifetime rule:

```text
create recovery evidence before vulnerable update
    ↓
keep it authoritative while target outcome is unresolved
    ↓
close weaker home-write completions
    ↓
close volatile-cache obligations where required
    ↓
recovery evidence may be superseded/reused
```

This is more precise than saying “PPL logs the write.”

PPL retains only enough evidence for its bounded parity-consistency recovery model, and the 2018 patch shows that the evidence must remain live until **lower-layer durability obligations**, not merely software write submissions, are closed.

---

## Historical record / reconstruction discipline

### Historical record

Actor/source-level facts include:

- Linux 4.12 PPL writing partial parity before ordinary data/parity writes;
- the explicit v4.12 prohibition on volatile member write-back caches;
- PPL log BIOs using `REQ_FUA`;
- commit `1532d9e...` adding write-back-cache support;
- queue write-cache detection;
- per-I/O-unit participating-disk bitmap construction;
- `REQ_PREFLUSH` submissions after stripe completion;
- pending-flush counting before PPL I/O-unit finish;
- the removal of the old blanket cache-disable warning by v4.16.

### Engineering reconstruction

Project abstractions include:

- `durability closure`;
- `outstanding durability obligation set`;
- `recovery-evidence authority lifetime`;
- `target state` versus `recovery evidence`;
- `weaker completion` versus `power-loss persistence boundary`.

These abstractions summarize relationships evidenced by the code; they are not historical Linux terminology.

### Functional analogy

Comparisons with database WAL retirement, journaling-filesystem home-write completion, Case 04 mapping publication/retirement, or Case 87 cache-durability semantics are permitted only at the relation level.

No shared genealogy follows from those analogies.

### Philosophical interpretation

No philosophical claim is required for the mechanism grounding.

A downstream interpretation may note that a system can already regard a write as completed at one layer while still retaining evidence that it is not safe to forget under a stronger failure model. That is interpretation, not language attributed to Linux developers.

---

## Cross-case boundaries

### Case 17 — RAID parity / degraded reconstruction

Case 17 asks whether a missing contribution remains reconstructable and whether redundancy margin has been restored.

Case 88 asks whether an **interrupted update leaves the surviving parity relation trustworthy**.

```text
reconstructability under member loss
    != parity-currentness across interrupted update
```

### Case 87 — storage cache durability

Case 87 provides interface-level vocabulary for volatile/nonvolatile cache and medium commitment.

Case 88 is an array-level consumer of a related distinction:

```text
member write completed
    != member write safe across power loss
```

Do not rewrite the Linux source in SCSI terminology it does not use.

### Case 04 — flash mapping / relocation

Case 04 separates relocation, integrity validation, mapping publication, and old-location retirement.

Case 88 separates log creation, home-write completion, cache durability closure, and PPL progress/retirement.

The common shape is bounded:

```text
new representation/write exists
    != old authority/recovery evidence may already be forgotten
```

### Case 96 — dRAID rebuild-progress persistence

Case 96 distinguishes persistent repair-progress checkpointing from in-core worker state.

Case 88 also distinguishes persistent recovery evidence from in-core control state, but the objects are different:

```text
Case 96: restart frontier for long-running repair
Case 88: transient flush-obligation tracking during stripe-update closure
```

No identity or genealogy is implied.

---

## Current open work

With the generic `modern PPL cache-flush evolution` debt closed, useful remaining slices are:

- power-cut fault injection at each PPL/home-write/flush boundary;
- exact state transition after a member cache-flush error and resulting MD fault handling;
- hardware lying about cache/flush/FUA semantics;
- devices with genuine power-loss-protected or nonvolatile write cache;
- later Linux block-layer API evolution affecting PPL's implementation details;
- PPL multiple-area/wrap/reuse evolution after the checked 4.16-era source;
- exact upstream stable/downstream backport history;
- controller/HBA interactions that can weaken or transform block-layer flush semantics;
- end-to-end tests proving recovery behavior after power loss with write-back caches actually enabled;
- a separate `computing-archaeology` history of Linux MD PPL / Intel IMSM lineage if that broader history becomes useful.

The open work is now implementation- and environment-specific rather than the broad question of whether Linux eventually added write-back-cache support.

---

## Maturity judgment

**grounded — unchanged**

Why no promotion:

- the 2017 mechanism is source-grounded;
- the 2018 cache-flush evolution is source-grounded and checked against tagged code;
- historical prior art already blocks first-invention inflation;
- but hardware power-cut validation is still absent;
- later kernel/backport history is not exhaustively covered;
- block-device compliance remains an external assumption rather than a property proved by source inspection.

The correct update is therefore **deeper implementation grounding and better navigation, not a maturity-level increase**.
