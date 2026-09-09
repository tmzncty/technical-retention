from pathlib import Path
import re

ROOT = Path('.')


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def write(path, text):
    text = text.rstrip() + '\n'
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one match, got {count}')
    return text.replace(old, new, 1)


EVIDENCE_PATH = 'evidence/41-cassandra-2024-paxos-v2-stale-commit-resurrection-deepening.md'
if (ROOT / EVIDENCE_PATH).exists():
    raise RuntimeError(f'{EVIDENCE_PATH} already exists; refusing duplicate slice')

index_before = read('CASE_INDEX.md')
if '**2545 —' not in index_before:
    raise RuntimeError('CASE_INDEX does not end at the expected prior finding 2545')
if re.search(r'^- \*\*2546\b', index_before, re.M):
    raise RuntimeError('finding 2546 already exists; refusing to collide with newer work')

new_evidence = r'''# Case 41 deepening — Cassandra 4.1 Paxos v2 stale-commit redistribution after tombstone collection (2024)

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
'''
write(EVIDENCE_PATH, new_evidence)

# ---- Case 41 ---------------------------------------------------------------
case_path = 'cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md'
case = read(case_path)
case = replace_once(
    case,
    '- **Bounded system:** Apache Cassandra 3.x operational semantics remain the principal behavior layer, with bounded historical floors from Apache Incubator Cassandra in 2009 and Cassandra 1.2.19 in 2014; these older artifacts are used only where they directly expose deletion-marker retention and reclamation policy.',
    '- **Bounded system:** Apache Cassandra 3.x operational semantics remain the principal behavior layer, with bounded historical floors from Apache Incubator Cassandra in 2009 and Cassandra 1.2.19 in 2014, plus a narrowly bounded Cassandra 4.1.0–4.1.6 Paxos-v2 defect/fix deepening; the older and later artifacts are used only where they directly change deletion-evidence retention, reclamation, or resurrection boundaries.',
    'Case 41 scope')

later_section = r'''
## Historical deepening — Cassandra 4.1.0–4.1.6 Paxos v2 stale-commit redistribution

This later slice is grounded separately in [`evidence/41-cassandra-2024-paxos-v2-stale-commit-resurrection-deepening.md`](../evidence/41-cassandra-2024-paxos-v2-stale-commit-resurrection-deepening.md). It does **not** replace the 1.2/3.x mechanism above. It adds one post-4.0 counterexample to an overly narrow safe-forgetting model.

### H/P — Cassandra 4.1 adds Paxos v2, Paxos Repair, and non-legacy Paxos-state purge modes

The Cassandra 4.1 release `NEWS.txt` introduces Paxos v2 and a Paxos Repair mechanism. After regular repairs include Paxos repair, the release record encourages operators to move to `paxos_state_purging: repaired`. Tagged 4.1.6 source defines `legacy`, `gc_grace`, and `repaired` purging modes and documents `legacy` as the default.

These are separate from the ordinary table tombstone / `gc_grace_seconds` mechanism already established by the case, even though the later modes deliberately relate Paxos-state retirement to GC grace or repair evidence.

### H/P — CASSANDRA-19617 shows a stale Paxos commit can reapply an insert after tombstone collection

Apache issue CASSANDRA-19617, created **3 May 2024** and resolved **11 June 2024**, is recorded as a critical correctness bug since Cassandra 4.1.0 and fixed beginning with 4.1.6. The issue explicitly limits the defect to `paxos_state_purging: gc_grace` and `repaired`.

Apache identifies two failures: old Paxos state could be purged on compaction but not filtered on load, and `PaxosPrepare` did not filter commits against the Paxos repair low bound. Under the described compaction pattern, some replicas could discard newer Paxos commits while an older commit survived elsewhere. A coordinator could then redistribute that old commit, allowing an **insert to be reapplied after GC grace elapsed and the user-data tombstone had been collected**.

**Primary anchor:** <https://issues.apache.org/jira/browse/CASSANDRA-19617>

### H/P — the 4.1.6 fix makes stale-state admissibility explicit at load and prepare time

Apache commit [`53b06453b7dea147ef6369765e0b7ac7fb0990fd`](https://github.com/apache/cassandra/commit/53b06453b7dea147ef6369765e0b7ac7fb0990fd), `Refresh stale paxos commit`, filters loaded promises/accepted/committed Paxos state using the applicable purge boundary and makes `PaxosPrepare` discard committed state below the maximum repair low bound returned by participants. Its distributed regression test constructs stale `system.paxos` state and requires the deleted row to remain absent after the later Paxos operation.

This fix is not tombstone restoration. It changes which surviving Paxos state is allowed to count.

### E — safe forgetting must close auxiliary re-authorization paths

The earlier case already established:

```text
stale positive replica
    + lost deletion evidence
    -> possible resurrection
```

The 2024 defect adds:

```text
stale positive Paxos commit
    + asymmetric retirement of newer Paxos state
    + later tombstone collection
    + obsolete commit wrongly treated as admissible
    -> possible reapplication of old insert
```

Therefore `replicas repaired enough for ordinary tombstone retirement` and `every auxiliary mechanism can no longer re-authorize older positive state` are not the same proposition.

This is a bounded engineering reconstruction from one Apache defect class, not a universal theorem about Paxos or distributed deletion.

---
'''
case = replace_once(case, '\n---\n\n## Retained state', '\n---\n' + later_section + '\n## Retained state', 'Case 41 later deepening insertion')

case = replace_once(
    case,
    '### 6. Hint state\n\nHints are temporary retained mutations for unavailable replicas. They can shorten inconsistency duration but do not substitute for the stronger repair relation.\n\nThe client-visible result `not found` is therefore supported by several hidden states that can outlive the DELETE request itself.',
    '### 6. Hint state\n\nHints are temporary retained mutations for unavailable replicas. They can shorten inconsistency duration but do not substitute for the stronger repair relation.\n\n### 7. Paxos coordination state and repair lower bound in the bounded 4.1 deepening\n\nFor Paxos-v2/LWT operations, `system.paxos` can retain older accepted/committed coordination state separately from the user-table tombstone. CASSANDRA-19617 shows that this auxiliary positive state also needs an admissibility boundary: a physically surviving old commit below the applicable GC-grace/repair floor must not regain redistribution authority.\n\nThe client-visible result `not found` is therefore supported by several hidden states that can outlive the DELETE request itself.',
    'Case 41 retained state addition')

case = replace_once(
    case,
    '- loss of repair/currentness evidence;\n- operator configuration of a grace window shorter than the real outage/repair envelope;',
    '- loss of repair/currentness evidence;\n- in the bounded Cassandra 4.1 Paxos-v2 defect, stale auxiliary Paxos commit state surviving newer coordination state and later being treated as redistributable after the user-data tombstone is collected;\n- operator configuration of a grace window shorter than the real outage/repair envelope;',
    'Case 41 failure mode')

eng_add = r'''
### E — auxiliary positive state can defeat otherwise-completed negative-state retirement

CASSANDRA-19617 narrows the earlier phrase `safe-forgetting condition`. Tombstone age, local overlap closure, and ordinary repair evidence can be insufficient if a separate retained coordination substrate can still re-authorize a superseded positive mutation.

So, in the bounded 4.1 Paxos-v2 configuration:

```text
user-data tombstone reclaimed
    != proof every older positive state is non-authoritative
```

The fix does not preserve the tombstone longer. It filters old Paxos state so physical survival does not automatically become protocol authority.

### E — purge-on-compaction != purge-on-observation

A retained record can be physically eligible for cleanup yet still reappear between compaction events unless read/load/prepare paths apply the same semantic boundary. CASSANDRA-19617 is therefore also a currentness-check placement failure: applying retirement only during one maintenance path did not guarantee that every later observer would treat the old state as retired.

'''
case = replace_once(case, '\n---\n\n## Functional analogies', '\n' + eng_add + '---\n\n## Functional analogies', 'Case 41 engineering addendum')

case = replace_once(
    case,
    '- `only_purge_repaired_tombstones` strengthens one reclamation condition but does not prove absence of every possible stale/corrupt copy.\n- The case does not establish secure erasure.',
    '- `only_purge_repaired_tombstones` strengthens one reclamation condition but does not prove absence of every possible stale/corrupt copy.\n- CASSANDRA-19617 is bounded to Cassandra 4.1 Paxos-v2 `paxos_state_purging: gc_grace` / `repaired`; the issue explicitly says the legacy/default TTL purging mode is not affected by this defect.\n- The 4.1.6 fix is an old-Paxos-state admissibility correction, not proof that all later Paxos/tombstone interactions are closed.\n- The case does not establish secure erasure.',
    'Case 41 limits')

source_add = r'''
### Cassandra 4.1 Paxos-v2 stale-commit deepening

6. Apache Cassandra 4.1.6 `NEWS.txt`, Paxos v2 / Paxos Repair release record: <https://github.com/apache/cassandra/blob/cassandra-4.1.6/NEWS.txt>
7. Apache Cassandra 4.1.6 `Config.java`, `PaxosStatePurging` modes/default: <https://github.com/apache/cassandra/blob/cassandra-4.1.6/src/java/org/apache/cassandra/config/Config.java>
8. Apache JIRA CASSANDRA-19617, **Paxos may re-distribute stale commits that predate a collectable tombstone**: <https://issues.apache.org/jira/browse/CASSANDRA-19617>
9. Apache Cassandra commit `53b06453b7dea147ef6369765e0b7ac7fb0990fd`, **Refresh stale paxos commit**: <https://github.com/apache/cassandra/commit/53b06453b7dea147ef6369765e0b7ac7fb0990fd>
10. Regression test `CasWriteTest.testStaleCommitInSystemPaxos` at the fix commit: <https://github.com/apache/cassandra/blob/53b06453b7dea147ef6369765e0b7ac7fb0990fd/test/distributed/org/apache/cassandra/distributed/test/CasWriteTest.java>

'''
case = replace_once(case, '### Later terminology / continuity check\n\n6. Apache Cassandra current documentation, **Tombstones**:', source_add + '### Later terminology / continuity check\n\n11. Apache Cassandra current documentation, **Tombstones**:', 'Case 41 sources')
case = replace_once(
    case,
    'The central mechanism is supported by Apache\'s release-family documentation, source, tests, and release notes. Remaining work is later-version semantic archaeology or broader genealogy, not a blocker for this bounded case.',
    'The central mechanism is supported by Apache\'s release-family documentation, source, tests, and release notes. The 4.1.0–4.1.6 Paxos-v2 deepening additionally grounds one auxiliary-state resurrection path after tombstone collection. Remaining work includes post-4.1.6 Paxos/tombstone semantics, broader range/TTL-tombstone evolution, independent fault injection, and genealogy; none blocks the bounded case.',
    'Case 41 status')
write(case_path, case)

# ---- ROADMAP ---------------------------------------------------------------
roadmap_path = 'ROADMAP.md'
roadmap = read(roadmap_path)
roadmap_line = (
    '- [x] Case 41 Paxos-v2 auxiliary-state resurrection deepening — '
    '[`evidence/41-cassandra-2024-paxos-v2-stale-commit-resurrection-deepening.md`]'
    '(evidence/41-cassandra-2024-paxos-v2-stale-commit-resurrection-deepening.md) grounds CASSANDRA-19617 and the 4.1.6 fix: '
    'for `paxos_state_purging: gc_grace` / `repaired`, stale `system.paxos` commits could survive newer coordination state and be redistributed after ordinary GC grace and user-data tombstone collection; the fix applies purge/repair lower bounds on load and prepare. '
    'This advances the distributed-delete roadmap from `stale replica + forgotten tombstone` to a bounded `auxiliary positive state can reacquire authority` failure without claiming a general Paxos flaw. '
    'Post-4.1.6 evolution, other tombstone kinds, independent fault injection, and full Paxos/LWT genealogy remain open.'
)
if roadmap_line in roadmap:
    raise RuntimeError('ROADMAP already contains the new Case 41 Paxos deepening')
pat = re.compile(r'(^- \[x\] Case 41 historical-policy deepening — Apache Cassandra 2009 GC-grace floor — .*?$)', re.M)
m = pat.search(roadmap)
if not m:
    raise RuntimeError('ROADMAP Case 41 historical-policy anchor not found')
roadmap = roadmap[:m.end()] + '\n' + roadmap_line + roadmap[m.end():]
write(roadmap_path, roadmap)

# ---- CASE_INDEX case row + findings ----------------------------------------
index_path = 'CASE_INDEX.md'
index = read(index_path)
row_pat = re.compile(r'^\| \[Apache Cassandra GC Grace: Tombstone Retention, Repair Windows, and Data Resurrection\]\(cases/41-apache-cassandra-tombstone-gc-grace-resurrection\.md\).*$', re.M)
m = row_pat.search(index)
if not m:
    raise RuntimeError('CASE_INDEX Case 41 row not found')
new_row = ('| [Apache Cassandra GC Grace: Tombstone Retention, Repair Windows, and Data Resurrection]'
           '(cases/41-apache-cassandra-tombstone-gc-grace-resurrection.md) | **grounded** | '
           'replicated positive values + timestamped tombstone negative state + hints/repair + SSTable repaired/unrepaired state + overlap-aware compaction + bounded Paxos-v2 accepted/committed state and purge/repair lower bounds | '
           'show deletion can depend on retained negative evidence; separate marker age, local shadow closure, replica convergence, repair evidence, auxiliary coordination-state admissibility, and physical reclamation; use CASSANDRA-7810 for local purge ordering and CASSANDRA-19617 for post-tombstone stale-Paxos reauthorization | '
           '[1.2.19 + 3.x Cassandra tombstone/repair grounding](evidence/41-cassandra-3x-tombstone-repair-grounding.md) + '
           '[2024 Paxos-v2 stale-commit deepening](evidence/41-cassandra-2024-paxos-v2-stale-commit-resurrection-deepening.md); '
           'the case now spans stale replicas, local compaction ordering, and one 4.1 auxiliary-state resurrection path; pre-1.2 genealogy, range/TTL tombstones, post-4.1.6 evolution, other Paxos purging/failure modes, production fault injection, and secure erasure remain separate work |')
index = index[:m.start()] + new_row + index[m.end():]

findings = r'''

## Case 41 — Cassandra 4.1 Paxos-v2 stale-commit resurrection findings

Evidence: [`evidence/41-cassandra-2024-paxos-v2-stale-commit-resurrection-deepening.md`](evidence/41-cassandra-2024-paxos-v2-stale-commit-resurrection-deepening.md)

- **2546 — Cassandra 4.1 introduces Paxos v2 and Paxos Repair as a distinct retained coordination-state regime.** The 4.1 release record says v2 may use Paxos Repair and later `paxos_state_purging: repaired`; this is historically later than Case 41's 2009/2015 tombstone-grace evidence. (`H/P`)
- **2547 — 4.1.6 source documents `legacy`, `gc_grace`, and `repaired` as distinct Paxos-state purging modes, with `legacy` as the default.** Configuration choice is therefore part of the historical defect boundary. (`H/P`)
- **2548 — CASSANDRA-19617 is version/configuration bounded, not a generic Cassandra-deletion claim.** ASF records the bug since 4.1.0 and explicitly limits it to `paxos_state_purging: gc_grace` / `repaired`; legacy/default TTL purging is outside the described failure. (`H/P`, `X`)
- **2549 — newer auxiliary state can disappear while older auxiliary state survives.** The issue's compaction-purgatory scenario allows newer Paxos commits to be purged while an older commit remains in another level, so simple age ordering of physical survivors is not enough to determine authority. (`H/P`, `E`)
- **2550 — a stale Paxos commit can reapply a positive value after ordinary tombstone collection.** Apache explicitly says the coordinator could redistribute the old commit and thereby reapply an insert after GC grace elapsed and the tombstone was collected. (`H/P`)
- **2551 — ordinary replica convergence != closure of every resurrection path.** In this bounded defect, the dangerous survivor is auxiliary `system.paxos` state rather than merely an unavailable user-data replica retaining an old value. (`E`)
- **2552 — purge-on-compaction != purge-on-observation.** CASSANDRA-19617 identifies that purging old Paxos state only during compaction did not stop stale commits resurfacing when state was later loaded; semantic retirement must also constrain relevant observation/use paths. (`H/P`, `E`)
- **2553 — Paxos repair low bound != user-data tombstone timestamp.** The two relations interact in the bug/fix but remain different retained/control state and must not be collapsed into one deletion clock. (`E`, `X`)
- **2554 — the 4.1.6 fix is an authority/admissibility filter, not payload repair.** `loadPaxosState` and `PaxosPrepare` discard state below applicable purge/repair bounds; they do not reconstruct the deleted row's tombstone. (`H/P`, `E`)
- **2555 — preventing stale positive reauthorization != restoring forgotten negative evidence.** After a tombstone is legitimately collected, the fix keeps obsolete Paxos state from regaining protocol significance rather than recreating the tombstone. (`E`)
- **2556 — physical survival of internal coordination state != current protocol authority.** An old Paxos commit can remain embodied yet be semantically inadmissible below the purge/repair boundary. (`E`)
- **2557 — safe forgetting can require cross-state-class closure.** A negative marker can be locally reclaimable while another retained mechanism still has enough obsolete positive state to recreate what that marker had suppressed. (`E`)
- **2558 — Case 48 repair-history state is only a bounded functional comparison.** `repairedAt` / pending-repair classify future incremental-repair work, whereas the Paxos repair low bound qualifies old consensus-state admissibility; neither is identical to tombstone age. (`A`, `X`)
- **2559 — CASSANDRA-19617 does not establish a general Paxos flaw or secure-delete failure.** It is a Cassandra Paxos-v2 state-lifecycle bug in named purging modes, concerning logical currentness/redistribution rather than media sanitization. (`X`)
- **2560 — related-repository boundary:** current `tmzncty/computing-archaeology` searches for `Cassandra Paxos tombstone` and `Paxos v2` found no dedicated case to reuse; broad Paxos-v2/LWT/Paxos-repair history should live there if developed, while Case 41 keeps the retention-specific cross-state-class resurrection boundary. (`H/P` project-state record)
'''
index = index.rstrip() + findings + '\n'
write(index_path, index)

print('Case 41 Paxos-v2 stale-commit deepening applied')
