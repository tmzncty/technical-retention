# Case 05 — RADOS replicated-object repair evidence index

## Status

**Case maturity: `grounded`.**

This index is navigation and evidence-layer control for [`../cases/05-rados-replicated-object-repair.md`](../cases/05-rados-replicated-object-repair.md). It does not promote the case beyond the maturity stated by the parent case / authoritative ledger.

Case 05 asks how one logical object can remain current and recoverable while replica membership, placement, authority, payload completeness, and recovery history change across independently failing OSDs.

The current anti-collapse rule is:

```text
physical replica survival
    != current placement membership
    != content currentness
    != peering/admission completeness
    != local payload completeness
    != desired redundancy restored
    != durable write commit
    != distributed PG-completion frontier
    != authority to retire old recovery history
    != trim enacted on every participant
    != old history bytes physically erased
```

---

## Evidence chain 1 — 2005–2007 peering and PG-metadata retention

**Packet:** [`05-rados-2005-2007-peering-pg-metadata-retention-deepening.md`](05-rados-2005-2007-peering-pg-metadata-retention-deepening.md)

This chain establishes the central retention decomposition.

The August-2005 source already distinguishes local completeness, peering/currentness knowledge, clean replication, persisted group attributes, and soft peer-session state. The 2007 RADOS record then makes `last_update`, `last_complete`, PG-log history, missing-state metadata, prior-participant reconstruction, and background repair explicit.

Core relation:

```text
payload bytes survive somewhere
    != enough state survives to identify current PG contents

PG metadata says object/version should exist
    != payload repair has already completed
```

Historical caution: the 2005 `RG` / RUSH-era source is an incomplete predecessor, not the mature 2007 state machine frozen earlier in time.

---

## Evidence chain 2 — 2006 CRUSH map/epoch placement currentness

**Packet:** [`05-crush-2006-map-epoch-placement-currentness-deepening.md`](05-crush-2006-map-epoch-placement-currentness-deepening.md)

Direct CRUSH / OSDI inspection separates deterministic placement calculation from timeless placement identity.

```text
physical replica survives
    != replica remains a current placement target

current placement target
    != payload there is current / complete

deterministic recomputation
    != no retained map / policy state is required
```

This packet is about the placement relation. It does not replace peering/version-history evidence for content currentness.

---

## Evidence chain 3 — September-2007 OSDMap restart persistence

**Packet:** [`05-ceph-2007-osdmap-restart-persistence-deepening.md`](05-ceph-2007-osdmap-restart-persistence-deepening.md)

This source-level restart witness separates:

```text
persisted map bytes
    != persisted current_epoch
    != restart-local placement context
    != cluster-current placement knowledge
    != distributed peering admission
```

The local OSD can reconstruct a usable local map/PG basis after restart without implying that its local map is globally current forever.

---

## Evidence chain 4 — 2007 EBOFS journal / local persistence boundary

**Packet:** [`05-ceph-2007-ebofs-journal-persistence-boundary-deepening.md`](05-ceph-2007-ebofs-journal-persistence-boundary-deepening.md)

This packet keeps the local object-store durability layer distinct from higher-level RADOS currentness.

It separates transaction receipt/application, journal/replay-qualified local evidence, checkpoint/restart reconstruction, OSD epoch/map state, and distributed PG admission.

```text
local transaction durable enough for replay/restart
    != cluster-wide replica currentness established
```

It should not be used to claim arbitrary physical power-cut guarantees below every disk/controller/cache layer.

---

## Evidence chain 5 — bounded 2005 RG/RUSH → 2006 PG/CRUSH transition

**Packet:** [`05-2005-2006-rg-rush-to-pg-crush-boundary-deepening.md`](05-2005-2006-rg-rush-to-pg-crush-boundary-deepening.md)

This packet prevents historical vocabulary collapse.

The August-2005 source visibly uses `repgroup_t` / `RG` plus RUSH-backed mapping. A December-2006 endpoint contains `pg_t` / `PG`, explicit PG history/log/missing structures, and CRUSH-backed PG placement.

Safe continuity claim:

```text
same broad retention problem:
placement / membership change can invalidate prior currentness knowledge

but

RG != automatically PG
RUSH != automatically CRUSH
2005 peering state machine != automatically 2006 recovery state machine
```

Exact commit-by-commit genealogy is intentionally routed to `computing-archaeology`.

---

## Evidence chain 6 — December-2006 peer-bounded PG-log retirement authority

**Packet:** [`05-ceph-2006-pg-log-retirement-authority-deepening.md`](05-ceph-2006-pg-log-retirement-authority-deepening.md)

The late-2006 source exposes a distinct retention boundary after local completion.

The primary tracks `peers_complete_thru`, derives it conservatively from acting-participant completion information, carries it to replicas as `pg_trim_to`, and the PG append path advances in-memory and on-disk log floors only to the authorized trim frontier.

The immediate on-disk trim path advances `ondisklog.bottom` and restart reads begin there; it does not, in that function, immediately remove/truncate every older byte.

Core relation:

```text
local last_complete
    != acting-set completion frontier
    != old PG history retireable
    != trim instruction delivered
    != trim enacted everywhere
    != old bytes physically erased
```

`history-retirement authority` and `distributed completion frontier` are repository engineering terms, not historical Ceph terminology.

---

## Unified evidence model

The six evidence chains support the following bounded model without pretending every revision has identical structures:

```text
logical object identity
    ↓
object -> PG assignment
    ↓
current cluster map / placement rule / epoch
    ↓
intended acting replica set
    ↓
peering / prior-participant history collection
    ↓
authoritative PG history reconstructed
    ↓
expected object-version set + missing/stale state
    ↓
PG admitted for service under currentness rules
    ↓
payload recovery / replica repair proceeds
    ↓
local completion frontiers advance
    ↓
acting-set completion frontier advances
    ↓
old recovery history becomes logically trim-eligible
    ↓
trim is propagated/enacted on participants
    ↓
underlying retired history bytes may later be physically reclaimed
```

Not every arrow is one atomic transaction. The evidence specifically warns against treating the chain as a single `repair complete` bit.

---

## Historical record / engineering reconstruction / analogy / philosophy boundary

### Historical / source record (`H/P`)

Direct primary sources establish, within the bounded revisions:

- `RG`/RUSH and later `PG`/CRUSH are visibly different source endpoints;
- objects map through PGs to ordered OSD sets under map/epoch state;
- role/map changes can invalidate prior peering knowledge before local bytes disappear;
- PG history distinguishes `last_update`, `last_complete`, logs, missing objects, and prior-participant state;
- locally persisted map/object-store state is distinct from cluster-current admission;
- `peers_complete_thru` and `pg_trim_to` provide an explicit completion-to-trim control path at the December-2006 endpoint;
- logical on-disk log retirement can advance by moving the persisted log bottom without immediate byte erasure in that path.

### Engineering reconstruction (`E`)

The repository infers:

- currentness is a retained relation, not merely a property of surviving bytes;
- repair debt can be retained as metadata before payload restoration completes;
- completion has local and distributed horizons;
- retirement of recovery history requires evidence and can be staged;
- logical history retirement and physical byte disappearance are separate persistence events.

### Functional analogy (`A`)

Useful comparisons include:

- Case 04 mapped Flash: replacement/current embodiment vs old-embodiment retirement;
- Case 25 Swift EC handoff cleanup: remote recovery success vs local retirement authority;
- Case 78 mirrored BBT: one current metadata copy vs convergence of redundant copies;
- Case 100 ZFS DTL: repair-control metadata vs repaired payload.

These are functional comparisons only. No shared implementation or historical descent is claimed.

### Philosophical interpretation (`Φ`)

Case 05 may later support the observation that a system sometimes must retain enough evidence to justify forgetting older evidence. That interpretation is downstream of the source-backed engineering mechanism and is not required for the case.

---

## Open evidence debts

The parent case remains `grounded`; the following are useful deepenings, not maturity blockers.

1. **PG-log trim fault trace** — interrupt/restart around an append that advances `info.log_bottom` / `ondisklog_bottom`, then inspect restart reconstruction.
2. **Slow-peer trim trace** — intentionally hold one acting peer's completion frontier back and observe whether the primary trim frontier remains bounded until catch-up.
3. **Physical reclamation below on-disk log bottom** — inspect the bounded EBOFS path that eventually rewrites/reclaims bytes below the logical floor without confusing that with PG logical retirement.
4. **Later completion-frontier terminology** — trace `peers_complete_thru` into later Ceph names/mechanisms in `computing-archaeology` unless a new retention-specific semantic discontinuity appears.
5. **Historically bounded counterexample** — find a revision or configuration in which the participant set or trim rule materially differs, to prevent accidental universalization of the December-2006 implementation.

---

## Related repositories

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `peers_complete_thru` and `Ceph PG log trim` found no dedicated packet to reuse.

Accordingly, this index keeps only retention-specific source seams. A broader source genealogy of RUSH→CRUSH, RG→PG, EBOFS/FileStore/BlueStore, peering evolution, and later completion-frontier terminology belongs in `computing-archaeology` and should be linked back rather than duplicated here.
