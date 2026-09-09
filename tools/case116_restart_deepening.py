from pathlib import Path

CASE = Path('cases/116-apache-hdfs-datanode-maintenance-state.md')
EVIDENCE = Path('evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md')
ROADMAP = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')

EVIDENCE_TEXT = r'''# Evidence 116 — Hadoop 3.0.1 Maintenance Restart Reconstitution

## Scope

This deepening closes one bounded follow-up question from Case 116:

> **In the released Hadoop 3.0.1 implementation, what survives a NameNode restart as durable maintenance intent, and what runtime replica relation must instead be reconstructed or re-observed?**

The inspected boundary is the exact Apache Hadoop `rel/release-3.0.1` tag, whose annotated tag points to commit `496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0` and is dated 23 March 2018. The claim is therefore release-specific. It is not a general statement about all later HDFS HA/failover implementations, and it does not claim that every maintenance-related field is or is not serialized in FSImage/edit logs.

This slice is intentionally about **restart reconstitution of retention-control relations**, not generic Hadoop restart history.

## Source custody and exact locations

Primary Apache sources, all inspected at commit `496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0`:

1. Apache Hadoop annotated tag `rel/release-3.0.1` — tag object `f8f37e90115ef5de75643fa980aa3ff5fd1ffc18`, pointing to commit `496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0`.
   - <https://github.com/apache/hadoop/tree/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0>
2. `HdfsDataNodeAdminGuide.md` — section describing the combined JSON hosts file, `adminState: IN_MAINTENANCE`, `maintenanceExpireTimeInMS`, and the `-refreshNodes` workflow.
   - <https://github.com/apache/hadoop/blob/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0/hadoop-hdfs-project/hadoop-hdfs/src/site/markdown/HdfsDataNodeAdminGuide.md>
3. `CombinedHostFileManager.java` — `refresh()` and `getMaintenanceExpirationTimeInMS(...)`.
   - <https://github.com/apache/hadoop/blob/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/CombinedHostFileManager.java>
4. `DatanodeManager.java` — constructor host-configuration refresh and `startAdminOperationIfNecessary(...)` on DataNode registration.
   - <https://github.com/apache/hadoop/blob/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DatanodeManager.java>
5. `TestMaintenanceState.java` — project regression tests covering NameNode restart while maintenance nodes/replicas are present, including the dead-maintenance-node case in which the restarted NameNode initially restores ordinary live replicas because it does not yet know that the maintenance node still carries a replica.
   - <https://github.com/apache/hadoop/blob/496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0/hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop/hdfs/TestMaintenanceState.java>

A fresh repository search in `tmzncty/computing-archaeology` for HDFS maintenance/restart material found no dedicated overlapping study to reuse. Broader NameNode/HA history remains a companion-repository task if pursued.

---

## Historical record

### H/P — released 3.0.1 makes maintenance intent and expiry external host-configuration properties

The released DataNode Administration guide requires the combined JSON host-file format for maintenance mode. Its host records can carry an administrative state of `IN_MAINTENANCE` and a `maintenanceExpireTimeInMS` epoch value; operators change host-level state in the hosts file and ask the NameNode to refresh nodes.

This gives the bounded release an externally retained configuration representation for two relations that Case 116 already treats as retention-control state:

```text
wanted maintenance administrative state
+
maintenance expiry horizon
```

The guide's configuration representation should not be confused with the current in-memory `DatanodeDescriptor` or with a block-replica location report.

### H/P — released source reloads that host configuration into a fresh NameNode process

`DatanodeManager` constructs the configured host-file manager and calls its `refresh()` path. In the combined-host implementation, `CombinedHostFileManager.refresh()` reads the configured hosts file and replaces the manager's in-memory host properties.

`CombinedHostFileManager.getMaintenanceExpirationTimeInMS(...)` returns the configured expiry for entries whose administrative state is `IN_MAINTENANCE`. `DatanodeManager.startAdminOperationIfNecessary(...)` consults that value when a DataNode registers and calls `startMaintenance(...)` when the configured maintenance condition is applicable.

Therefore, within this exact release path:

> **maintenance intent and its expiry can be reconstituted from retained host configuration rather than requiring the old Java object graph to survive process restart.**

This is a source-of-truth statement about the inspected code path, not a claim that no related state is ever stored elsewhere.

### H/P — the released test suite distinguishes restart-surviving policy from runtime knowledge of a dead maintenance replica

`TestMaintenanceState` contains a NameNode-restart scenario in which a maintenance DataNode carrying a replica is down. After NameNode restart, the test expects HDFS to restore the ordinary number of live replicas because the restarted NameNode does not yet know that the absent maintenance DataNode has that replica. When the DataNode returns, the maintenance replica relation is again visible and the test can observe both the live replicas and the maintenance replica.

The same test class also checks that out-of-service nodes represented in the block map remain appropriately represented across a NameNode restart in the bounded scenarios it exercises.

These are Apache project regression tests, not independent production validation. Their value here is narrower: they expose which relations the implementation deliberately treats differently at restart.

---

## Engineering reconstruction

### E — persisted admin intent != persisted runtime replica-location knowledge

The restart path exposes at least two retention contracts:

```text
host JSON
    -> retained desired admin relation + expiry
    -> reloaded by fresh NameNode process

runtime block / DataNode observations
    -> knowledge that a particular DataNode currently embodies a replica
    -> may require post-restart re-observation / DataNode return
```

The first relation can survive by configuration replay. The bounded dead-maintenance-node test demonstrates that the second relation is not simply assumed to have identical restart persistence semantics: the NameNode can compensate with ordinary live replicas while the maintenance holder is absent and unknown.

### E — policy survival != service-side reliance survival

It is possible for the system to retain the operator's statement “this host is in maintenance until time T” while declining, after restart, to rely on an unobserved dead host as though its replica were presently available evidence.

Thus:

> **surviving policy authority does not imply surviving operational credit for every embodiment named by that policy.**

This is particularly important because Case 116's maintenance optimization relies on expected return. After restart, the expectation can remain configured while runtime topology evidence is rebuilt more conservatively.

### E — temporary dependency credit before restart != guaranteed durable restart credit

Before restart, a known maintenance replica may be counted within the maintenance regime while ordinary live-replica obligations are relaxed. In the bounded regression scenario, a restarted NameNode that does not know the dead maintenance node's replica restores ordinary live replicas instead of treating the old credit as unquestioned durable knowledge.

That yields a useful stop condition:

> **an optimization based on presently known embodiment does not automatically become a durable restart promise.**

This does not mean the replica bytes vanished. It means the authority to rely on their known location is a different retained relation from the bytes themselves.

### E — NameNode restart != DataNode restart / re-registration

A NameNode process restart reconstructs control state from configuration and runtime discovery paths. A DataNode's later return/re-registration is a separate event that can supply fresh evidence about embodiment and bring the maintenance relation back into active block accounting.

Do not collapse these into one generic “restart persistence” claim.

### E/X — host-config-derived reconstruction != proven FSImage/edit-log serialization

The inspected materials are sufficient to show a configuration-derived reconstruction path. They are **not** sufficient to prove a repository-wide negative such as “maintenance state is never serialized in FSImage/edit logs,” nor a positive such as “all maintenance runtime state is checkpointed there.”

That question remains outside this bounded slice unless separately traced through image/edit-log serialization code and failover tests.

---

## Functional comparison

### A/X — Case 79 HDFS startup re-observation is a bounded same-system analogy, not mechanism identity

Case 79 grounds the older HDFS startup distinction between durable namespace/block metadata and block-to-DataNode location knowledge rebuilt by DataNode reports. Case 116's 3.0.1 maintenance path presents a related shape:

- desired maintenance state and expiry have an external configuration source of truth;
- runtime knowledge that an absent DataNode currently embodies a usable replica can require re-observation.

The analogy is useful because both cases separate **retained policy/metadata** from **runtime evidence reconstructed from participants**. But the mechanisms are not interchangeable: startup SafeMode thresholds and BlockReports are not the same state machine as maintenance admission, expiry, or `CombinedHostFileManager`.

No genealogy claim is made.

### A/X — this is not a generic distributed consensus or lease case

`maintenanceExpireTimeInMS` is an operator-supplied maintenance horizon in the inspected HDFS design. Nothing here establishes quorum lease semantics, consensus-log replication of the relation, or a universal distributed “maintenance lease” abstraction.

---

## Philosophical interpretation

### I — persistence can be split across state classes with different restart contracts

A narrow interpretation is now defensible:

> **A technical preservation relation can survive restart through one retained representation while the evidence needed to rely on a particular physical embodiment must be re-observed.**

Here the operator's maintenance intention and expiry can persist as configuration, while runtime replica-location knowledge has a different restart contract. The resulting continuity is therefore neither “everything persisted” nor “everything was reconstructed from scratch.”

Do not inflate this into “memory of memory,” a universal theory of distributed storage, or a claim that configuration is intrinsically more authoritative than runtime evidence. The authority ordering is specific to the bounded HDFS paths inspected here.

---

## Explicit non-equivalences fixed by this deepening

- `persisted host-admin intent != in-memory DatanodeDescriptor continuity`;
- `persisted maintenance expiry != persisted runtime replica-location knowledge`;
- `known replica before restart != automatically credited replica after restart`;
- `replica bytes may physically survive != NameNode presently knows/credits that embodiment`;
- `maintenance policy survives != relaxed-redundancy reliance necessarily survives unchanged`;
- `NameNode restart != DataNode return/re-registration`;
- `configuration replay != proof of FSImage/edit-log serialization`;
- `Apache regression test != independent production validation`;
- `same-system functional analogy != mechanism identity or genealogy`.

---

## What remains open

This slice does **not** close:

1. exact HDFS-7877 subtask/commit genealogy before the released 3.0.1 state;
2. full HA active/standby failover semantics and whether every path behaves identically to the bounded process-restart tests;
3. exact FSImage/edit-log serialization status for every maintenance-related field;
4. erasure-coded block-group maintenance semantics;
5. expiry/dead-node convergence under injected failures;
6. broad maintenance-mode history across distributed storage systems.

Those are separate research slices. The broader implementation/history items should primarily be routed to `computing-archaeology` if developed.
'''

CASE_SECTION = r'''## Restart reconstitution deepening — Hadoop 3.0.1

A later source-level deepening now separates two restart contracts that the broad maintenance-state case previously left together. In the exact Hadoop 3.0.1 tag, the combined JSON hosts file can retain `adminState: IN_MAINTENANCE` together with `maintenanceExpireTimeInMS`; `CombinedHostFileManager.refresh()` reloads those host properties, and `DatanodeManager` consults them when DataNodes register. Thus a fresh NameNode process can reconstitute maintenance intent and its expiry from retained external configuration.

The same released test suite provides an important counterexample to the shortcut “maintenance policy survived, therefore every replica credit survived.” In a bounded restart scenario where the maintenance DataNode is down, the restarted NameNode restores the normal live-replica count because it does not yet know that the absent maintenance node still carries the replica. When that DataNode later returns, its maintenance replica relation becomes visible again.

So the bounded release now supports:

> **persisted maintenance intent / expiry != persisted runtime knowledge of a particular replica embodiment**

and:

> **policy survival != service-side reliance survival**.

A maintenance replica's bytes may physically survive the NameNode restart while the restarted control plane declines to rely on that unobserved location. This is not payload loss; it is a difference in the restart lifetime of **embodiment evidence**.

The deepening also fixes an important negative boundary. The inspected configuration-reload path does not by itself establish whether every maintenance-related field is or is not serialized through FSImage/edit logs, and a NameNode process restart is not the same event as a DataNode return/re-registration or every HA failover path.

Deepening record: [`../evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md`](../evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md).

---

'''

ROADMAP_LINE = r'''- [x] Case 116 Hadoop 3.0.1 restart-reconstitution deepening — [`cases/116-apache-hdfs-datanode-maintenance-state.md`](cases/116-apache-hdfs-datanode-maintenance-state.md), deepened by [`evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md`](evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md): the released 3.0.1 Admin Guide and source ground a combined-host JSON source of truth for `IN_MAINTENANCE` plus `maintenanceExpireTimeInMS`, reloaded into a fresh NameNode process and consulted on DataNode registration. Released regression tests then expose the complementary boundary: a restarted NameNode can restore ordinary live replicas when a dead maintenance holder is not yet known, even though maintenance intent remains configured. This closes the bounded `persisted admin intent != persisted runtime replica-location knowledge` / `policy survival != service-side reliance survival` seam without claiming universal HA behavior or FSImage/edit-log serialization semantics. Exact subtask genealogy, full active/standby failover semantics, EC behavior, serialization tracing, and fault injection remain open; broad HDFS restart/maintenance history belongs primarily in `computing-archaeology`.
'''

FINDINGS = r'''
- **2635 — Hadoop 3.0.1 has a released external maintenance-intent representation.** The combined JSON hosts-file contract can retain `adminState: IN_MAINTENANCE` plus `maintenanceExpireTimeInMS`; these are control-plane properties, not block payload. (`H/P`)
- **2636 — the combined hosts configuration is reloaded by a fresh NameNode process.** `CombinedHostFileManager.refresh()` reloads host properties, and `DatanodeManager` consults the resulting maintenance expiry/admin relation on DataNode registration. (`H/P`)
- **2637 — persisted host-admin intent != in-memory descriptor continuity.** The bounded restart path can recreate the maintenance relation from external configuration without preserving the old Java object graph. (`E`)
- **2638 — persisted maintenance expiry != persisted runtime replica-location knowledge.** The two relations have distinct reconstruction paths and must not be treated as one checkpointed object. (`E`)
- **2639 — a dead maintenance replica may lose restart-time operational credit without losing its bytes.** Apache's bounded regression scenario restores ordinary live replicas because the restarted NameNode does not yet know the absent maintenance holder has the replica. (`H/P`, `E`)
- **2640 — temporary dependency credit before restart != guaranteed durable restart credit.** A replica counted under the pre-restart maintenance regime need not remain unquestioned evidence after control-plane restart. (`E`)
- **2641 — policy survival != service-side reliance survival.** The operator's maintenance intention can remain authoritative while the restarted NameNode behaves conservatively about an unobserved embodiment. (`E`)
- **2642 — physical survival != observed/credited embodiment.** A DataNode disk can still contain the block while the NameNode lacks current knowledge authorizing reliance on that location. (`E`)
- **2643 — DataNode return/re-registration is a new evidence event.** When the maintenance DataNode returns, the control plane can once again observe the maintenance replica relation; this is distinct from NameNode restart itself. (`H/P`, `E`)
- **2644 — configuration-derived reconstitution != proof of FSImage/edit-log serialization.** The inspected path establishes one restart source of truth but neither proves nor disproves serialization of every related field elsewhere. (`X`)
- **2645 — NameNode process restart != universal HA failover semantics.** The released tests bound a restart behavior; active/standby failover and every later release remain separate evidence questions. (`X`)
- **2646 — Apache regression coverage != independent production validation.** `TestMaintenanceState` is executable project evidence for intended behavior, not field evidence that every deployment reproduces it. (`H/P`, `X`)
- **2647 — Case 79 startup re-observation ~= Case 116 restart reconstitution only at a bounded same-system structure.** Both distinguish retained control/metadata from runtime relations re-observed from participants; SafeMode/BlockReport mechanics are not maintenance-state mechanics. (`A`, `X`)
- **2648 — restart persistence is state-class-specific.** A single distributed preservation regime can retain policy/expiry through configuration while reconstructing embodiment evidence through later observation. (`E`, `I`)
- **2649 — related-repository boundary:** a fresh `tmzncty/computing-archaeology` search found no dedicated HDFS maintenance/restart study to reuse; broad HDFS/NameNode/HA genealogy belongs there if developed, while Case 116 keeps the retention-specific restart-contract boundary. (`H/P` project-state record)
'''

# Create the bounded evidence artifact.
if EVIDENCE.exists():
    existing = EVIDENCE.read_text()
    if existing != EVIDENCE_TEXT:
        raise SystemExit(f'{EVIDENCE} already exists with different content')
else:
    EVIDENCE.write_text(EVIDENCE_TEXT)

# Deepen Case 116 without disturbing the rest of the case.
case = CASE.read_text()
old_grounding = 'Grounding record: [`../evidence/116-hadoop-2014-2018-datanode-maintenance-grounding.md`](../evidence/116-hadoop-2014-2018-datanode-maintenance-grounding.md).'
new_grounding = old_grounding + '\n\nRestart-reconstitution deepening: [`../evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md`](../evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md).'
if '116-hadoop-301-maintenance-restart-reconstitution-deepening.md' not in case:
    if old_grounding not in case:
        raise SystemExit('Case 116 grounding anchor not found')
    case = case.replace(old_grounding, new_grounding, 1)
    anchor = '## Retained state\n'
    if anchor not in case:
        raise SystemExit('Case 116 retained-state anchor not found')
    case = case.replace(anchor, CASE_SECTION + anchor, 1)
CASE.write_text(case)

# Add bounded completion status near the recent Phase-2 deepenings.
roadmap = ROADMAP.read_text()
if 'Case 116 Hadoop 3.0.1 restart-reconstitution deepening' not in roadmap:
    lines = roadmap.splitlines(keepends=True)
    idx = next((i for i, line in enumerate(lines) if 'Case 78 Linux MTD mirrored/versioned Flash-BBT deepening' in line), None)
    if idx is None:
        raise SystemExit('ROADMAP Case 78 recent-deepening anchor not found')
    lines.insert(idx + 1, '\n' + ROADMAP_LINE)
    roadmap = ''.join(lines)
ROADMAP.write_text(roadmap)

# Update the Case 116 navigation row and append the findings ledger.
index = INDEX.read_text()
old_row = '| [Apache HDFS DataNode Maintenance State: Temporary Withdrawal, Relaxed Redundancy, and Expiry](cases/116-apache-hdfs-datanode-maintenance-state.md) | **grounded** | HDFS block payload + normal replication objective + maintenance-specific redundancy minimum + DataNode liveness/admin state + retained maintenance expiry + transition/reconstruction progress | separate temporary withdrawal from decommission; replica presence from service eligibility; maintenance minimum from permanent replication factor; policy expiry from payload deletion; expected return from present physical availability | [2014–2018 HDFS maintenance-state grounding](evidence/116-hadoop-2014-2018-datanode-maintenance-grounding.md); exact subtask/commit genealogy, NameNode failover persistence, EC-specific behavior, fault injection, and broad maintenance-mode history remain separate work |'
new_row = '| [Apache HDFS DataNode Maintenance State: Temporary Withdrawal, Relaxed Redundancy, and Expiry](cases/116-apache-hdfs-datanode-maintenance-state.md) | **grounded** | HDFS block payload + normal replication objective + maintenance-specific redundancy minimum + DataNode liveness/admin state + retained maintenance expiry + transition/reconstruction progress + configuration-derived restart reconstitution | separate temporary withdrawal from decommission; replica presence from service eligibility; maintenance minimum from permanent replication factor; policy expiry from payload deletion; persisted admin intent from runtime embodiment evidence | [2014–2018 HDFS maintenance-state grounding](evidence/116-hadoop-2014-2018-datanode-maintenance-grounding.md) + [3.0.1 restart-reconstitution deepening](evidence/116-hadoop-301-maintenance-restart-reconstitution-deepening.md); exact subtask genealogy, full HA failover/serialization semantics, EC behavior, fault injection, and broad maintenance-mode history remain separate work |'
if old_row in index:
    index = index.replace(old_row, new_row, 1)
elif new_row not in index:
    raise SystemExit('CASE_INDEX Case 116 row anchor not found')

if '**2635 —' not in index:
    if '**2634 —' not in index:
        raise SystemExit('CASE_INDEX expected prior finding 2634 not found')
    index = index.rstrip() + '\n' + FINDINGS.lstrip('\n')
INDEX.write_text(index.rstrip() + '\n')
