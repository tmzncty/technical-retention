# Evidence Index — Case 116 HDFS DataNode Maintenance State

## Status

- Case: [`cases/116-apache-hdfs-datanode-maintenance-state.md`](../cases/116-apache-hdfs-datanode-maintenance-state.md)
- Current maturity: **`grounded`**
- Scope: temporary DataNode maintenance, maintenance-specific redundancy, expiration, restart reconstruction, erasure-coded sufficiency, and HA/controller-local policy materialization
- This index is navigation and claim-boundary control. It does not replace the canonical case or `CASE_INDEX.md`.

Case 116 should remain `grounded`: the historical/released mechanism is well supported, but the newly isolated HA seam still lacks a direct active-only-refresh → failover → re-observation behavioral trace.

---

## Why this evidence family needs a dedicated index

Case 116 now spans several different persistence and control horizons that are easy to collapse into one sentence:

```text
operator maintenance intent
    -> durable/external policy representation
    -> controller-local policy snapshot
    -> DataNode admin-state materialization
    -> maintenance admission / service exclusion
    -> maintenance-specific redundancy accounting
    -> expiry / exit
    -> reconstruction or cleanup consequences
```

The packets below intentionally separate those steps. In particular:

- temporary maintenance is not decommissioning;
- a retained replica is not automatically ordinary-service eligible;
- maintenance expiry is not physical media expiry;
- restart reconstruction is not persistence of one volatile Java object;
- one NameNode's refreshed policy snapshot is not proof that every HA peer has refreshed the same external policy;
- replicated namespace history is not automatically the same persistence mechanism as external host-policy configuration.

---

## Evidence chain 1 — Historical and released maintenance-state grounding

### File

[`116-hadoop-2014-2018-datanode-maintenance-grounding.md`](116-hadoop-2014-2018-datanode-maintenance-grounding.md)

### Role

Establishes the bounded HDFS chronology and released mechanism:

- HDFS-6729 as a 2014 public project-floor proposal;
- HDFS-7877 design/release chronology;
- separation of `ENTERING_MAINTENANCE` and `IN_MAINTENANCE`;
- maintenance-specific minimum redundancy;
- temporary service exclusion without immediate erasure of the retained replica;
- released expiration semantics;
- different convergence work for live and dead maintenance exit.

### Key boundary

```text
maintenance relation
    != decommission relation
```

and:

```text
retained / known replica
    != ordinary read/write eligibility
```

### Do not infer

- HDFS invention priority;
- physical-media retention or sanitization;
- that the final expiration contract already existed in the 2015 design draft.

---

## Evidence chain 2 — Expiration-clock persistence genealogy

### File

[`116-hadoop-2014-2017-maintenance-expiry-clock-persistence-genealogy-deepening.md`](116-hadoop-2014-2017-maintenance-expiry-clock-persistence-genealogy-deepening.md)

### Role

Tracks how a maintenance timeout/expiration relation became durable administrative input rather than merely an open design question. It separates:

```text
maintenance requested
    != maintenance indefinitely valid
```

and:

```text
policy expiration timestamp
    != physical media retention deadline
```

### Key boundary

The expiration clock is control metadata governing how long the relaxed maintenance relation may be trusted. It is not a flash/DRAM retention specification and does not itself delete data.

---

## Evidence chain 3 — NameNode restart reconstruction

### File

[`116-hadoop-301-maintenance-restart-reconstitution-deepening.md`](116-hadoop-301-maintenance-restart-reconstitution-deepening.md)

### Role

Shows, for the Hadoop 3.0.1 generation, that maintenance state need not survive restart as one serialized volatile `DatanodeDescriptor` state machine. Durable host-policy input plus the restarted NameNode's later observations can reconstruct the relevant administrative relation.

### Key boundary

```text
volatile controller object survives
    != maintenance obligation survives
```

A stronger reconstruction shape is:

```text
external maintenance policy
    + DataNode re-registration / observation
    + current block-management rules
    -> reconstructed maintenance admin state
```

### Do not infer

- exact crash-durability of every external host-file write;
- that every reconstruction cut point has been fault-injected;
- that restart reconstruction and HA failover are identical paths.

---

## Evidence chain 4 — Erasure-coded maintenance sufficiency

### File

[`116-hadoop-335-336-ec-maintenance-sufficiency-deepening.md`](116-hadoop-335-336-ec-maintenance-sufficiency-deepening.md)

### Role

Deepens the meaning of “sufficiently protected” when maintenance interacts with erasure coding. It prevents a replicated-block intuition from being silently applied to EC groups.

### Key boundary

```text
maintenance admission relation
    depends on protection model
```

and therefore:

```text
replicated-block sufficiency rule
    != erasure-coded sufficiency rule
```

### Do not infer

- that one universal replica-count threshold describes all HDFS protection policies;
- that maintenance means the same reconstruction cost for replicated and EC data.

---

## Evidence chain 5 — HA policy refresh and controller-local materialization

### File

[`116-hadoop-301-ha-maintenance-intent-refresh-boundary-deepening.md`](116-hadoop-301-ha-maintenance-intent-refresh-boundary-deepening.md)

### Role

Pins the Hadoop 3.0.1 source path showing that:

1. `CombinedHostFileManager.refresh()` reads external host-policy data into a manager-local `HostProperties` snapshot;
2. `DatanodeManager.refreshNodes()` refreshes that host provider and reevaluates that manager's local DataNode map;
3. HA-capable test infrastructure addresses refresh to a specific NameNode index;
4. external host-policy mutation and NameNode-local materialization are distinct operations.

### Key boundary

```text
external maintenance intent exists
    != active NameNode has loaded current intent
    != standby NameNode has loaded current intent
```

and:

```text
refresh NameNode A
    != source-level proof that NameNode B refreshed
```

### Engineering shorthand

The packet uses the repository terms:

- **per-controller policy snapshot**;
- **controller-local materialization**;
- **independently materialized maintenance intent**.

These are analytical terms, not historical Hadoop vocabulary.

### Do not infer

- that failover necessarily loses maintenance state;
- that active-only refresh is an endorsed operational workflow;
- that decommission standby tests prove maintenance failover behavior;
- that no later Hadoop version adds stronger synchronization or tests.

---

## Unified retention/control model

The current evidence family supports this layered model:

```text
[1] operator intent
        |
        v
[2] external maintenance-policy representation
    - DataNode identity / admin operation
    - maintenance expiration
        |
        +-------------------------------+
        |                               |
        v                               v
[3A] NameNode A policy snapshot   [3B] NameNode B policy snapshot
        |                               |
        v                               v
[4A] local descriptor/admin state [4B] local descriptor/admin state
        |                               |
        +---------------+---------------+
                        |
                        v
[5] service / redundancy consequences
    - entering maintenance
    - in maintenance
    - ordinary target/read exclusion
    - maintenance-specific protection threshold
        |
                        v
[6] expiry / exit / return
        |
                        v
[7] reconstruction or excess-replica cleanup as required
```

The model explicitly blocks several category collapses:

```text
policy durability
    != simultaneous runtime materialization
```

```text
admin-state retention
    != payload-media retention
```

```text
maintenance request
    != completed maintenance admission
```

```text
known replica
    != ordinary service authority
```

```text
maintenance expiry
    != immediate physical deletion
```

---

## Cross-packet claim matrix

| Question | Best packet | Current answer | Evidence limit |
| --- | --- | --- | --- |
| Why is maintenance distinct from decommission? | grounding | temporary relation, different redundancy/service semantics | HDFS-specific |
| When did timeout become part of the concrete control relation? | expiry genealogy + released grounding | final released behavior includes expiration; 2015 draft still had timeout open | not invention priority |
| Must volatile NameNode admin objects themselves survive restart? | restart reconstitution | no; state can be reconstructed from external policy + current observations | source/restart path, not every crash cut point |
| Is a replicated-block count enough to describe EC maintenance safety? | EC sufficiency | no | version/policy specific |
| Does refreshing one HA NameNode prove its peer loaded the same maintenance policy? | HA refresh boundary | no, not from the inspected source path | direct failover behavior still needs experiment |

---

## Historical record vs engineering reconstruction

### Historical / source record

Supported directly by ASF design records, released documentation, released source, or released tests:

- maintenance exists as a distinct HDFS DataNode admin relation;
- maintenance has an entering state and an in-maintenance state;
- maintenance can use a different redundancy threshold from decommission;
- maintenance expiration is retained and can terminate the relaxed relation;
- Hadoop 3.0.1 reads combined host-policy entries into a local host-manager snapshot;
- Hadoop 3.0.1 `DatanodeManager.refreshNodes()` reevaluates local DataNode descriptors from that snapshot;
- the HA-capable admin-state test base directs refresh to a named NameNode index.

### Engineering reconstruction

Repository analytical vocabulary built from those source facts:

- maintenance obligation;
- policy persistence horizon;
- controller-local materialization;
- per-controller policy snapshot;
- independently materialized maintenance intent;
- reconstruction from durable external evidence.

These terms must not be retroactively attributed to ASF developers unless an original source uses them.

### Functional analogy

Permitted only as shape comparison:

- Swift Case 25: later re-observation can reconstruct pending maintenance/cleanup authority;
- Ceph Case 142: maintenance need, admission, and current execution authority are distinct relations.

No genealogy or design influence is claimed.

### Philosophical interpretation

A rule can persist even when one runtime representation of the rule does not. This is interpretive language only and carries no independent evidentiary weight.

---

## Current open debts

### P1 — Direct HA active-only-refresh / failover trace

Build a two-NameNode HA test with `CombinedHostFileManager` and record:

```text
write maintenance policy
    -> refresh active only
    -> compare NN0 / NN1 admin states
    -> fail over
    -> inspect immediate new-active state
    -> explicit refresh
    -> inspect convergence
```

This is now the highest-value debt because the source-level seam is already clear.

### P1 — Expiration crossing during failover

Repeat the above while the configured maintenance expiration crosses between:

- policy write;
- active refresh;
- failover;
- peer refresh.

Record both stored expiry and resulting admin/reconstruction behavior.

### P1 — Both-refreshed control experiment

Refresh both NameNodes before failover and use it as the control arm. This distinguishes a refresh/materialization seam from unrelated failover behavior.

### P2 — Controlled failover vs restart

Compare:

- controlled active→standby failover;
- standby restart before promotion;
- active restart;
- full HA pair restart.

This should remain separate from the existing single-NameNode restart reconstruction packet.

### P2 — Operator workflow documentation

Audit version-pinned ASF operational documentation for whether operators are told to run `-refreshNodes` separately against HA peers, through failover-aware tooling, or by another mechanism. Documentation should be used to characterize supported procedure, not to overwrite source behavior.

### P2 — Later-version regression/genealogy

Search later Hadoop releases for maintenance-specific HA/failover tests or fixes. If found, record the change as later chronology rather than silently projecting it into Hadoop 3.0.1.

---

## Related-repository reuse note

A fresh search of `tmzncty/computing-archaeology` for HDFS maintenance / standby / failover material did not identify a dedicated packet that could be imported directly for this slice. That is a bounded search result, not a universal absence claim. Broader HDFS HA history should remain in the archaeology repository if it becomes a research target; this repository should keep only the control-state/retention-specific evidence needed by Case 116.

---

## Navigation

### Canonical case

- [`../cases/116-apache-hdfs-datanode-maintenance-state.md`](../cases/116-apache-hdfs-datanode-maintenance-state.md)

### Evidence

- [`116-hadoop-2014-2018-datanode-maintenance-grounding.md`](116-hadoop-2014-2018-datanode-maintenance-grounding.md)
- [`116-hadoop-2014-2017-maintenance-expiry-clock-persistence-genealogy-deepening.md`](116-hadoop-2014-2017-maintenance-expiry-clock-persistence-genealogy-deepening.md)
- [`116-hadoop-301-maintenance-restart-reconstitution-deepening.md`](116-hadoop-301-maintenance-restart-reconstitution-deepening.md)
- [`116-hadoop-335-336-ec-maintenance-sufficiency-deepening.md`](116-hadoop-335-336-ec-maintenance-sufficiency-deepening.md)
- [`116-hadoop-301-ha-maintenance-intent-refresh-boundary-deepening.md`](116-hadoop-301-ha-maintenance-intent-refresh-boundary-deepening.md)

### Primary source baseline for the new HA slice

Apache Hadoop commit:

- `496dc57cc2e4f4da117f7a8e3840aaeac0c1d2d0`

Pinned source links are collected in the HA evidence packet.

---

## Maturity decision

**No promotion.**

Case 116 remains `grounded` because:

- chronology and released mechanism are strongly sourced;
- restart reconstruction is grounded at source level;
- EC-specific sufficiency is separately deepened;
- the new HA source topology is now explicit;
- but the highest-value HA cut point still lacks a direct behavioral/failover trace.

A maturity change should wait for experimental evidence or equivalently strong released regression coverage of the active-only-refresh / peer-state / failover boundary.
