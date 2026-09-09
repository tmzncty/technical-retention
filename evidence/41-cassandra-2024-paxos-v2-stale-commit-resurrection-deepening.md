# Case 41 deepening — Cassandra 4.1 Paxos v2 stale-commit redistribution after tombstone collection (2024)

## Purpose

This addendum deepens [`Case 41 — Apache Cassandra GC Grace`](../cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md) at one bounded post-4.0 seam:

> **Can an older positive value return after ordinary tombstone evidence has been collected even when the dangerous survivor is not merely a stale user-data replica, but retained auxiliary Paxos state?**

Apache's 2024 CASSANDRA-19617 defect record answers yes for a specific Cassandra 4.1 Paxos-v2 configuration. A sufficiently old committed Paxos record could survive the newer state that should supersede it, later be treated as the latest known commit by a coordinator, and be redistributed after `gc_grace_seconds` had elapsed and the user-data tombstone had been collected. The 4.1.6 fix adds purge/admissibility filtering on Paxos-state load and applies the Paxos repair low bound while preparing transactions.

This is **not** a general history of Paxos, Cassandra lightweight transactions, Paxos repair, or `system.paxos`. It is one implementation-level retention/currentness failure that changes the safe-forgetting boundary of Case 41.

Project terms such as `auxiliary-state resurrection path`, `cross-state-class forgetting closure`, and `authority filter` below are engineering reconstructions, not Apache historical vocabulary.

---

## Source set

### P1 — Cassandra 4.1 release NEWS: Paxos v2 and Paxos Repair

Apache Cassandra `NEWS.txt` for the 4.1 release records a new Paxos implementation named `v2`, together with a new Paxos Repair mechanism. The same release record says Paxos repair runs automatically alongside normal repairs for v2 and recommends moving to `paxos_state_purging: repaired` once regular repairs include Paxos repair.

**Primary anchor:** <https://github.com/apache/cassandra/blob/cassandra-4.1.6/NEWS.txt>

**Use:** establishes the release-family vocabulary and the fact that Paxos-state retirement can be qualified by repair state rather than being only a fixed TTL relation.

**Boundary:** this release note does not by itself establish the later CASSANDRA-19617 defect.

### P2 — Cassandra 4.1.6 `Config.java`: purging modes and default

The tagged 4.1.6 source defines `PaxosStatePurging` modes including `legacy`, `gc_grace`, and `repaired`. Its comments say the default is `legacy`; they also warn that once migrated away from legacy it is unsafe simply to return to legacy because newer state may have been written without the legacy TTL behavior.

**Primary anchor:** <https://github.com/apache/cassandra/blob/cassandra-4.1.6/src/java/org/apache/cassandra/config/Config.java>

**Use:** prevents a scope error. The 2024 defect is not evidence that every Cassandra 4.1 cluster or every Paxos-v2 deployment had the same resurrection path.

### P3 — CASSANDRA-19617 defect record, 3 May–11 June 2024

Apache issue **CASSANDRA-19617**, `Paxos may re-distribute stale commits that predate a collectable tombstone`, is marked:

- bug;
- `Correctness - Recoverable Corruption / Loss`;
- severity `Critical`;
- since version `4.1.0`;
- fixed in `4.1.6`, `5.0-rc1`, `5.0`, `6.0-alpha1`, and `6.0`.

The issue explicitly limits the bug to `paxos_state_purging: {gc_grace, repaired}`, the modes introduced with Paxos v2. It says the legacy/default TTL purging mode is not affected by the described defect.

The issue identifies two implementation failures:

1. purging was applied during compaction but not when Paxos state was loaded, allowing very old commits to resurface in some compaction layouts;
2. `PaxosPrepare` did not filter commits against the Paxos repair low bound.

It then gives the retention consequence directly: some replicas could purge newer commits while another retained an older commit; the coordinator could see that old commit as not universally known and redistribute it, permitting an **insert to be reapplied after GC grace had elapsed and the tombstone had been collected**.

**Primary/institutional anchor:** <https://issues.apache.org/jira/browse/CASSANDRA-19617>

### P4 — Apache fix commit `53b06453...`, 11 June 2024

Apache Cassandra commit `53b06453b7dea147ef6369765e0b7ac7fb0990fd`, `Refresh stale paxos commit`, is the source-control link attached to CASSANDRA-19617 and adds the 4.1.6 change record.

**Commit:** <https://github.com/apache/cassandra/commit/53b06453b7dea147ef6369765e0b7ac7fb0990fd>

The inspected diff changes two especially relevant paths.

In `SystemKeyspace.loadPaxosState(...)`, it derives a `purgeBefore` boundary according to the configured purging mode and filters promises, accepted state, and committed state that fall below the applicable boundary. For `repaired`, the boundary is tied to the table's Paxos repair low bound minus the configured Paxos purge grace.

In `PaxosPrepare`, the coordinator tracks the maximum low bound returned by participants and treats committed state older than that bound as `none` rather than as a candidate to refresh/redistribute.

**Evidence use:** the fix is an authority/admissibility repair for retained Paxos state. It does not rewrite the already-collected user-data tombstone back into existence.

### P5 — regression test `testStaleCommitInSystemPaxos`

The same commit adds a distributed regression test in `CasWriteTest.java`. The test creates a conditional insert, records its Paxos commit, creates a later conditional delete, runs Paxos repair, arranges compaction so older Paxos state can occupy a different level, waits for the table tombstone to become collectible, compacts, and then exercises a later Paxos operation. The post-fix assertion requires the deleted row to remain absent.

**Primary anchor:** <https://github.com/apache/cassandra/blob/53b06453b7dea147ef6369765e0b7ac7fb0990fd/test/distributed/org/apache/cassandra/distributed/test/CasWriteTest.java>

**Use:** executable project evidence that the source change targets the precise stale-commit/tombstone interaction named in the issue.

---

## Historical record (`H/P`)

### H/P — Cassandra 4.1 introduced a second retention relation around Paxos state

The 4.1 release record distinguishes ordinary table data from retained Paxos coordination state and introduces Paxos Repair plus new state-purging choices. `paxos_state_purging: repaired` makes maintenance history relevant to when old Paxos state becomes discardable.

This is historically later than Case 41's 2009 GC-grace floor and 2015 `only_purge_repaired_tombstones` option. Do not project the 4.1 Paxos-v2 machinery backward into Cassandra 1.2/3.x.

### H/P — CASSANDRA-19617 is an auxiliary-state resurrection path

The defect record does not merely repeat the classic stale-replica story from Cassandra's tombstone documentation. The dangerous survivor in the named scenario is an old **Paxos commit** in `system.paxos`. Compaction can remove newer Paxos records while leaving an older record in a different level; without the correct load/prepare filtering, that older record can regain protocol significance.

The user-data tombstone may already have completed its ordinary grace/reclamation path when the old insert is redistributed.

### H/P — the fix changes currentness qualification, not just physical cleanup

`53b06453...` applies the applicable purge/repair boundary when loading and comparing Paxos state. This means the engineering question is not only whether old bytes still physically exist in an SSTable; it is whether a retained old commit is still **admissible to the Paxos protocol**.

A physically surviving old commit below the relevant boundary is supposed to be treated as absent for protocol purposes.

---

## Engineering reconstruction (`E`)

### E — tombstone retirement safety spans more than the user-data replica set

The classic Case 41 relation is:

```text
stale positive replica
    + premature tombstone retirement
    -> possible resurrection during repair
```

CASSANDRA-19617 adds a second bounded path:

```text
stale positive Paxos commit
    + newer Paxos state retired asymmetrically
    + user-data tombstone later collected
    + stale commit treated as admissible/latest
    -> old insert can be redistributed
```

Therefore:

```text
ordinary replica convergence
    != complete proof that every auxiliary re-authorization path is closed
```

This is a project reconstruction from the Apache defect/fix, not Apache terminology.

### E — physical survival != protocol authority

After the fix, an old Paxos commit can still exist physically yet fall below the `gc_grace`/repair-derived admissibility boundary. Its continued embodiment is not supposed to make it a valid commit for re-distribution.

That gives the same anti-collapse rule seen elsewhere in the repository:

```text
retained bytes
    != current authoritative state
```

Here the boundary is particularly important because misclassifying old auxiliary state can recreate a user-visible positive value that a tombstone had previously suppressed.

### E — purge boundary != payload-deletion timestamp

The Paxos repair low bound and the user-data tombstone timestamp/grace relation are different retained/control relations. The fix composes them operationally, but they must not be treated as one timestamp or one metadata object.

### E — the fix prevents stale re-authorization; it does not restore forgotten negative evidence

Once the ordinary tombstone has been legitimately collected, the CASSANDRA-19617 fix does not reconstruct that tombstone. It instead prevents obsolete Paxos state below the applicable boundary from being promoted back into current protocol state.

So:

```text
prevent stale positive authority
    != restore deleted negative marker
```

### E — safe forgetting can require closure across state classes

A local reclaim decision can be correct relative to one state class and still be unsafe end-to-end if another retained state class can later recreate what was forgotten. In this bounded Cassandra case, user-data tombstones and `system.paxos` commits participate in different mechanisms but interact at the deletion/currentness boundary.

This supports a narrower project rule:

> **Before declaring a negative marker safely forgettable, audit whether another retained mechanism can still re-authorize the superseded positive state.**

It is not a universal theorem about every distributed database; it is the exact lesson of this defect class.

---

## Functional analogies (`A`)

### A — relation to Case 48 Cassandra incremental-repair state

[`Case 48`](../cases/48-apache-cassandra-incremental-repair-state.md) shows `repairedAt` / pending-repair state changing future incremental-repair eligibility. The 4.1 Paxos-v2 deepening here uses a different repair-derived relation: a Paxos repair low bound can make older coordination state inadmissible.

Shared function:

```text
retained maintenance history
    -> changes what old state future maintenance/protocol logic may trust
```

But:

```text
SSTable repairedAt / pendingRepair
    != Paxos repair low bound
    != user-data tombstone age
```

This is a bounded same-project comparison, not mechanism identity.

### A — relation to Case 90 Kafka leader-epoch admissibility

Case 90 shows that surviving currentness metadata can be present but unusable or unsafe because format/lineage conditions make it inadmissible. CASSANDRA-19617 similarly demonstrates that retained old metadata/state must be filtered by an authority boundary before it is allowed to guide recovery or redistribution.

The mechanisms and histories are unrelated; only the `presence != admissibility` function is compared.

---

## Philosophical interpretation (`I`)

The narrow interpretive result is stronger than `deletion leaves traces` but weaker than a general theory of forgetting:

> **A system can finish forgetting one negative trace and still fail to keep the deletion forgotten if an older positive coordination trace elsewhere can reacquire authority.**

This makes technical forgetting a relation among multiple retained state classes, not a single erasure event. The interpretation does **not** identify Paxos state with human memory, archival memory, or Stieglerian tertiary retention, and it does not license the slogan `the system remembers its memory`.

---

## Counterexamples and stop conditions (`X`)

- **The bug is configuration-bounded.** CASSANDRA-19617 explicitly limits it to `paxos_state_purging: gc_grace` and `repaired`; the legacy/default TTL mode is outside the described defect.
- **The bug is version-bounded.** The issue records `Since Version: 4.1.0` and fix versions beginning at 4.1.6. Do not project it onto Cassandra 3.x.
- **This is not a proof that Paxos is generally unsafe.** It is an implementation/purging interaction in Cassandra's Paxos-v2 state lifecycle.
- **Paxos-state purge is not user-data tombstone purge.** They are separate state classes with interacting consequences.
- **Repair low bound is not proof of present payload integrity.** It is used here as an admissibility boundary for old Paxos state.
- **Compaction removing newer Paxos state is not by itself corruption.** The defect requires the remaining older state to be incorrectly allowed to resurface/redistribute.
- **No secure-erasure claim follows.** The issue concerns logical currentness and redistributable state, not forensic media sanitization.
- **The 2024 fix does not establish that every post-4.1.6 Paxos/tombstone interaction is complete or bug-free.** Later evolution and independent fault injection remain open.

---

## Related-repository check

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Cassandra Paxos tombstone` and `Paxos v2` found no dedicated technical-history case to reuse. The broad history of Cassandra LWT/Paxos v2, Paxos repair, and `system.paxos` belongs there if developed; this addendum keeps only the retention-specific cross-state-class resurrection boundary.

---

## Claim ledger

| Claim | Type | Grounding | Boundary |
| --- | --- | --- | --- |
| Cassandra 4.1 introduced Paxos v2 and Paxos Repair | `H/P` | P1 | release-family statement |
| `paxos_state_purging` includes legacy/gc_grace/repaired and 4.1.6 source documents legacy as default | `H/P` | P2 | configuration/version scoped |
| CASSANDRA-19617 can reapply an insert after GC grace and tombstone collection | `H/P` | P3 | only named affected purging modes |
| Some old Paxos commits survived newer state because purge occurred on compaction but not load | `H/P` | P3 | defect-specific |
| `PaxosPrepare` failed to filter commits below the Paxos repair low bound | `H/P` | P3 | defect-specific |
| Fix commit filters loaded/prepare-time Paxos state by applicable purge/repair boundary | `H/P` | P4 | 4.1.6 fix implementation |
| Regression test preserves deletion after constructing stale `system.paxos` state | `H/P` | P5 | project test, not independent product validation |
| ordinary user-data tombstone safety alone closes every stale-state path | `X` | P3–P5 contradict this for the bounded configuration | rejected |
| physical survival of old Paxos state implies protocol authority | `X` | P4 | rejected |
| repair low bound and tombstone timestamp are the same retained state | `X` | P3–P4 | rejected |
| Cassandra Paxos v2 is generally unsafe | `X` | none | rejected |
| this fix proves secure deletion | `X` | none | rejected |

---

## Open work

- identify the exact CEP-14 / 4.1 commit genealogy that first introduced each non-legacy Paxos-state purging mode, beyond the release-level floor used here;
- inspect post-4.1.6 evolution of Paxos-state purging and repair lower-bound handling release by release;
- determine whether comparable auxiliary-state resurrection bugs exist in other LWT/consensus implementations;
- add independent fault injection only if it can reproduce the bounded stale-commit path without silently changing Cassandra's timing/compaction assumptions;
- keep ordinary range/TTL tombstone semantics, secure deletion, and generic Paxos history outside this addendum.
