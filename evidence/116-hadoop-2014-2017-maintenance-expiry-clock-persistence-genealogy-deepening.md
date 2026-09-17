# Evidence 116 — Hadoop 2014–2017 Maintenance Expiry Clock/Persistence Genealogy

## Status

**`bounded deepening complete`** — this slice traces one narrow design/implementation question inside Apache HDFS maintenance state:

> **How did a temporary DataNode-maintenance expiry evolve from proposal-level soft/process-local state into an externally retained deadline that a later NameNode process could interpret after restart?**

This is not a general history of HDFS maintenance mode, NameNode HA, leases, timeout design, or distributed clocks. Case 116 already grounds the broader maintenance-state mechanism and a separate Hadoop 3.0.1 restart-reconstitution slice. The purpose here is to close a smaller genealogy debt that those records left open: **the evolution of the expiry representation itself and the clock domain used to interpret it.**

The bounded record shows a real design movement:

```text
2014–Jan 2015 proposal
    maintenance is intentionally temporary
    + expiration exists
    + restart/failover loss can be accepted as soft state

April 2015 HDFS-7877 design
    host-file administrative intent
    + explicit requirement that maintenance state survive NN restart
    + timeout still an open design question

October 2015 discussion
    persist expiration as UTC time is proposed explicitly

August 2016 HDFS-9392 implementation
    maintenanceExpireTimeInMS enters static admin configuration
    + expiration is still compared against JVM monotonic time

January 2017 HDFS-11296
    comparison changes from Time.monotonicNow() to Time.now()
    + deadline becomes an externally expressible epoch-time contract

September 2017 HDFS-12473 / released 3.0.x family
    combined hosts JSON carries adminState + maintenanceExpireTimeInMS
    + fresh NameNode can reload that configuration
```

The key result is not “wall clock is better than monotonic time.” It is narrower:

> **A deadline serialized for interpretation by another process needs a reference frame whose meaning survives that process boundary.**

A JVM-local monotonic clock is useful for elapsed-time measurement inside one process lifetime; an absolute epoch time is useful for an externally authored/reloaded deadline. They solve different problems and have different failure modes.

---

## Source custody

Primary or near-primary Apache project records inspected for this slice:

1. **ASF HDFS-6729 — “Support maintenance mode for DN”**, created 22 July 2014, later resolved as duplicate of HDFS-7877.
   - issue: <https://issues.apache.org/jira/browse/HDFS-6729>
   - the public issue record preserves proposal comments from August 2014 and January 2015.
2. **HDFS-7877 Maintenance States Design Doc**, second attachment uploaded 4 April 2015.
   - <https://issues.apache.org/jira/secure/attachment/12709388/Supportmaintenancestatefordatanodes-2.pdf>
   - the PDF was directly opened through the ASF attachment endpoint during this research round; screenshot retrieval was attempted but the remote endpoint returned a cache-miss error, so no screenshot-specific visual claim is made.
3. **ASF HDFS-7877 umbrella discussion**, including the 2 October 2015 comment proposing persistence of maintenance expiration UTC time.
   - <https://issues.apache.org/jira/browse/HDFS-7877>
4. **Apache Hadoop commit `9dcbdbdb5a34d85910707f81ebc1bb1f81c99978`**, 30 August 2016, `HDFS-9392. Admins support for maintenance state`.
   - <https://github.com/apache/hadoop/commit/9dcbdbdb5a34d85910707f81ebc1bb1f81c99978>
5. **ASF HDFS-11296 — “Maintenance state expiry should be an epoch time and not jvm monotonic”**, plus its Apache Hadoop commit.
   - public issue/mailing record: <https://www.mail-archive.com/hdfs-issues@hadoop.apache.org/msg178212.html>
   - commit `f3fb94be05a61a4c4c06ab279897e5de2b181b0e`, 20 January 2017 UTC:
     <https://github.com/apache/hadoop/commit/f3fb94be05a61a4c4c06ab279897e5de2b181b0e>
6. **Apache Hadoop commit `230b85d5865b7e08fb7aaeab45295b5b966011ef`**, 20 September 2017, `HDFS-12473. Change hosts JSON file format`.
   - <https://github.com/apache/hadoop/commit/230b85d5865b7e08fb7aaeab45295b5b966011ef>
7. **Apache Hadoop `rel/release-3.0.1` source**, especially:
   - `DatanodeAdminProperties.java`:
     <https://github.com/apache/hadoop/blob/rel/release-3.0.1/hadoop-hdfs-project/hadoop-hdfs-client/src/main/java/org/apache/hadoop/hdfs/protocol/DatanodeAdminProperties.java>
   - `CombinedHostFileManager.java`:
     <https://github.com/apache/hadoop/blob/rel/release-3.0.1/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/CombinedHostFileManager.java>

A fresh search in `tmzncty/computing-archaeology` for HDFS maintenance expiration, HDFS-11296, and HDFS-7877 found no dedicated overlapping packet. This evidence therefore stays here as a retention-control-state genealogy rather than duplicating an existing technical-history module.

---

## Historical record

### H/P — the 2014 proposal already had an expiry, but treated maintenance as intentionally temporary operational state

HDFS-6729 begins from the short-outage problem: administrators may take a DataNode down briefly for work such as adding RAM or disks, and do not want the normal missing-block/decommission consequences when the same node is expected back shortly.

A 21 August 2014 project comment says the proposed patch sets an expiration time for maintenance mode. If the NameNode has not heard the DataNode heartbeat after expiry, the NameNode should consider it dead and ordinary data recovery should resume.

So expiry was not a late afterthought. From the earliest inspected HDFS proposal family it already bounded the temporary exception:

```text
maintenance exception
    -> valid for bounded time
    -> expiry
    -> ordinary failure/recovery treatment resumes
```

This does **not** yet tell us how the expiry itself survives process restart.

### H/P — the August 2014 proposal deliberately avoided a maintenance file

A 25 August 2014 HDFS-6729 comment says the patch uses a direct `hdfs dfsadmin -maintainDatanode` control rather than a maintenance file analogous to the decommission exclude file. The stated reason is itself temporal: maintenance should be temporary, and a generic `-refreshNodes` operation should not accidentally extend a DataNode's expiration time.

That records an early design concern that remains important here:

> **retaining administrative intent can accidentally retain or renew temporal authority unless the deadline semantics are defined separately.**

At this point, “where the node state is recorded” and “what operation can alter the expiry horizon” were already recognized as coupled but distinct design questions.

### H/P — by January 2015 the proposal explicitly called maintenance mode soft state

In the HDFS-6729 discussion on 27 January 2015, Lei (Eddy) Xu answers a restart/failover concern by calling maintenance mode a **soft state**. The comment says NameNode restarts/failovers are relatively rare and that after such an event the NameNode can treat the DataNode as stale/dead without sacrificing durability/availability.

Within that abandoned proposal branch, therefore:

```text
maintenance relation survives process restart
    = not required
```

The important boundary is historical, not normative: this is an early HDFS proposal that was later absorbed into HDFS-7877. It must not be projected onto the released maintenance-state contract.

### H/P — the April 2015 HDFS-7877 design reverses the restart expectation for administrative state

The second HDFS-7877 design attachment, uploaded 4 April 2015, takes a different approach. It defines a maintenance hosts file and the `dfsadmin -refreshNodes` workflow. More importantly, the block-management requirements include the statement that after a NameNode restart, the DataNode should remain in the same administrative state.

This is a substantive design change from the January soft-state answer:

```text
January 2015 HDFS-6729 proposal:
    losing maintenance state across NN restart is acceptable

April 2015 HDFS-7877 design:
    DN should remain in the same maintenance state after NN restart
```

This does not prove that the April design already had a complete persistence implementation. It proves that **restart continuity had become an explicit requirement**.

### H/P — the April 2015 design still leaves timeout ownership unresolved

The same HDFS-7877 design document lists timeout support as an open issue. It asks whether HDFS itself should return a node to service after it remains in `ENTERING_MAINTENANCE` / `IN_MAINTENANCE` too long and says the authors at that moment felt the timeout might be better handled outside HDFS, for example by an admin script removing the node from the maintenance file.

This creates a useful historical split:

```text
restart-surviving maintenance administrative intent
    !=
restart-surviving in-HDFS expiry semantics
```

The first had become a requirement; the second was still undecided.

### H/P — October 2015 discussion makes expiry persistence an explicit design problem

On 2 October 2015 in HDFS-7877, Ming Ma proposes supporting persistence for timeout by persisting the maintenance expiration **UTC time**. The same comment notes that NameNode clocks can be out of sync, but suggests that this can be accepted because maintenance-timeout precision is on the order of minutes.

This is strong historical evidence for two separate points:

1. the project explicitly recognized that timeout persistence required a clock representation suitable for multiple NameNode/process lifetimes;
2. absolute wall-clock representation introduced clock-synchronization assumptions rather than eliminating timing assumptions altogether.

Therefore:

> **persistent absolute deadline != perfectly synchronized distributed time.**

The design accepted a bounded operational clock-quality assumption.

### H/P — HDFS-9392 in August 2016 externalizes the deadline but still interprets it in the JVM monotonic clock domain

Apache Hadoop commit `9dcbdbdb5a34d85910707f81ebc1bb1f81c99978` (`HDFS-9392. Admins support for maintenance state`) adds `maintenanceExpireTimeInMS` to `DatanodeAdminProperties`, the administrator-facing static DataNode properties used by the combined-host configuration path.

The same commit also adds the deadline to runtime `DatanodeInfo`, passes the configured value through `CombinedHostFileManager`, invokes `startMaintenance(node, maintenanceExpireTimeInMS)`, and keeps maintenance nodes tracked until expiry.

But the commit's expiration predicate is:

```java
public static boolean maintenanceNotExpired(long maintenanceExpireTimeInMS) {
  return Time.monotonicNow() < maintenanceExpireTimeInMS;
}
```

That is the key intermediate state in this genealogy:

```text
expiry value is externally represented as configuration
    +
expiry comparison uses process-local monotonic clock
```

The project had crossed the **storage/serialization boundary** before fully aligning the **clock-reference boundary**.

### E/H boundary — why this intermediate representation is not equivalent to durable deadline semantics

The historical fact is only the code shown above. The following is engineering reconstruction:

A monotonic clock is intentionally not a civil/epoch timestamp. Its value is meaningful for measuring elapsed intervals inside a clock domain whose arbitrary origin need not correspond to a portable external timestamp. If a raw absolute scalar derived for one JVM's monotonic clock is serialized and interpreted after another JVM starts, the scalar does not automatically preserve the same deadline meaning.

Thus:

> **serializable number != serializable temporal meaning.**

No claim is made that every HDFS-9392 deployment necessarily experienced a restart bug. The claim is narrower: HDFS-11296 itself identifies the mismatch as difficult for external users and changes the clock domain.

### H/P — HDFS-11296 in January 2017 explicitly changes the expiry reference frame

HDFS-11296 is titled **“Maintenance state expiry should be an epoch time and not jvm monotonic.”** Its project description explains that the expiry is intended as an absolute time and that checking an externally configured value against `Time.monotonicNow()` makes it difficult to configure externally.

Apache commit `f3fb94be05a61a4c4c06ab279897e5de2b181b0e` makes the production change extremely small and therefore very legible:

```diff
 public static boolean maintenanceNotExpired(long maintenanceExpireTimeInMS) {
-  return Time.monotonicNow() < maintenanceExpireTimeInMS;
+  return Time.now() < maintenanceExpireTimeInMS;
 }
```

Associated maintenance tests are changed from `Time.monotonicNow() + EXPIRATION_IN_MS` to `Time.now() + EXPIRATION_IN_MS`.

This is not merely an implementation cleanup. It changes what a persisted/admin-authored deadline **means**:

```text
before:
    scalar interpreted in JVM monotonic-time coordinates

after:
    scalar interpreted as wall-clock epoch time
```

The control state becomes portable across process lifetimes in a way the earlier monotonic scalar was not designed to be.

### H/P — HDFS-12473 preserves the expiry field while regularizing the JSON container format

Apache commit `230b85d5865b7e08fb7aaeab45295b5b966011ef` (`HDFS-12473. Change hosts JSON file format`) changes the combined-host file from a sequence of standalone JSON objects to a top-level JSON array and retains backward parsing support for the old form.

Its test fixture explicitly contains entries such as:

```json
{
  "hostName": "host7",
  "adminState": "IN_MAINTENANCE",
  "maintenanceExpireTimeInMS": "112233"
}
```

The important point is not the array syntax itself. It is that by September 2017 the expiry value is firmly part of the externally retained **administrative host property record**, rather than only an in-memory monitor variable.

### H/P — released 3.0.1 names the configuration/runtime distinction directly

In `rel/release-3.0.1`, `DatanodeAdminProperties` documents itself as the **static configuration specified by administrators** and explicitly says it is different from runtime state. The class retains both:

- `AdminStates adminState`;
- `long maintenanceExpireTimeInMS`.

`CombinedHostFileManager.refresh()` reads the JSON host file into fresh `DatanodeAdminProperties` objects and replaces the manager's in-memory host properties. `getMaintenanceExpirationTimeInMS(...)` then exposes the configured deadline to the DataNode administrative path.

That released representation completes the bounded chain needed for this slice:

```text
external retained record
    -> admin state + absolute expiry
    -> reload into fresh NN process
    -> runtime maintenance transition/monitoring
```

The already-existing Case-116 restart evidence covers the later runtime consequences in more detail. This file does not duplicate them.

---

## Engineering reconstruction

### E — persistence requires both a value and a stable interpretation context

The most useful technical abstraction from HDFS-11296 is:

```text
persisted scalar
    + reference frame / interpretation rule
    = persisted meaning
```

A timestamp-like field can be perfectly preserved byte-for-byte while failing to preserve the intended temporal relation if the new process interprets it against a different clock origin.

Therefore:

> **bitwise persistence != semantic persistence.**

The missing state need not be another explicit field. It can be an implicit coordinate system.

### E — monotonic clocks and epoch clocks support different retention contracts

For one process lifetime, monotonic time is attractive for elapsed-time decisions because it is not meant to jump when wall-clock time is adjusted. But an externally authored absolute deadline must be interpretable by a later process or another administrative tool.

The HDFS transition therefore exposes a trade:

```text
process-local elapsed-time robustness
    vs
cross-process / externally addressable absolute-time meaning
```

The 2017 design chooses the second property for maintenance expiry.

This file does **not** claim that wall-clock time is universally safer. Clock steps, skew, NTP behavior, and misconfiguration remain separate hazards.

### E — administrative-state persistence and deadline persistence are separate obligations

The April 2015 design already required that a DataNode remain in the same maintenance state after NameNode restart while still treating timeout support as open.

That means the system can preserve:

```text
"host H is in maintenance"
```

without yet having a complete answer for:

```text
"host H is in maintenance only until absolute time T"
```

So:

> **persistent mode identity != persistent temporal authority.**

Case 116 should preserve that distinction whenever discussing restart continuity.

### E — deadline persistence changes the authority horizon, not payload durability

`maintenanceExpireTimeInMS` does not preserve HDFS block bytes. It preserves **how long the control plane is allowed to rely on the temporary-withdrawal assumption**.

The chain is:

```text
payload replicas may survive on maintenance DN
    +
admin intent says the DN is expected back
    +
expiry bounds how long that expectation may relax ordinary redundancy work
```

Losing or misinterpreting the deadline can therefore change repair policy even when no payload bit has changed.

### E — reloading configuration is not the same as persisting the old runtime object graph

The final bounded implementation does not require a Java `DatanodeDescriptor` instance to survive restart. It can reconstruct desired maintenance state from an external configuration record.

Thus:

> **control-state continuity != object-instance continuity.**

This is already compatible with the separate restart-reconstitution evidence, where runtime replica-location knowledge can still require re-observation.

### E — persistence medium and policy authority are distinct dimensions

The combined hosts JSON is a durable/external representation only insofar as the operator's configuration file itself is retained and supplied to the NameNode. HDFS source defines how to read and interpret it; it does not magically guarantee deployment-level replication of that file to every HA NameNode.

Therefore:

```text
format supports restart reconstitution
    != deployment guarantees every NN sees identical retained file
```

That HA distribution question remains open below.

### E — expiry conversion is a control-state semantic migration

The HDFS-11296 diff changes no block data and no maintenance identifier. Yet it changes the semantics of an already-existing stored field.

This is a useful retention case because migrations can occur at the **meaning layer**:

```text
same field name
    + same integer type
    + different clock interpretation
    = different persistence contract
```

Schema stability alone does not prove semantic stability.

---

## Functional analogy

### A/X — lease/deadline systems share a shape, not a mechanism

Many distributed systems retain an absolute expiry, lease deadline, certificate validity time, or cleanup horizon. The HDFS example is functionally comparable only at this broad level:

```text
retained authority
    -> valid until deadline
    -> deadline crossing revokes or changes authority
```

But HDFS maintenance expiry is **not established here as a consensus lease**, lock lease, filesystem lease, security-token expiry, or distributed transaction timeout. Its failure response is maintenance-policy exit/re-replication behavior, not ownership transfer guaranteed by a quorum protocol.

No genealogy is asserted.

### A/X — restart-reconstitution cases elsewhere do not prove this clock choice

Cases involving manifests, WAL markers, checkpoints, or configuration replay can also reconstruct control state after restart. They are useful functional comparisons for `durable representation -> runtime reconstruction`, but they do not establish why HDFS chose epoch time or what its clock-skew envelope is.

---

## Philosophical interpretation

### I — preserving a value can fail to preserve the relation that made the value meaningful

A bounded interpretation supported by this case is:

> **Technical memory is not always contained in the stored field itself; some of its meaning lives in the coordinate system used to interpret that field.**

`maintenanceExpireTimeInMS` can survive as digits while its deadline meaning fails if the consuming process uses an unrelated clock origin. In that sense, retention includes preservation of **interpretive context**.

Do not inflate this into a claim that all meaning is external, that clocks are merely philosophical constructs, or that epoch time guarantees truth. The claim is an engineering one about reference frames and restart semantics.

---

## Explicit non-equivalences / non-claims

This deepening fixes the following boundaries:

- `maintenance mode exists != maintenance expiry is durable`;
- `admin state survives restart != deadline survives restart with the same meaning`;
- `serialized integer != semantically portable timestamp`;
- `same field name/type != same clock semantics`;
- `monotonic clock != epoch / civil wall clock`;
- `epoch timestamp != perfectly synchronized cluster time`;
- `absolute expiry != consensus lease`;
- `configuration file can retain state != every HA NameNode necessarily has an identical file`;
- `configuration reload != FSImage/edit-log serialization`;
- `retained maintenance policy != retained replica-location evidence`;
- `deadline expiry != block deletion`;
- `deadline expiry != physical media retention failure`;
- `soft-state proposal in HDFS-6729 != released HDFS maintenance semantics`;
- `April 2015 design requirement != proof that implementation was already complete`;
- `HDFS-11296 commit date != invention date for persistent deadlines generally`;
- `HDFS-12473 JSON-format change != invention of maintenance expiry`;
- `Apache project regression/source evidence != independent production validation`.

---

## Claim ledger

| Claim | Class | Evidence strength | Boundary |
|---|---|---:|---|
| HDFS-6729 proposed an expiration-bounded maintenance mode in 2014 | H/P | high | public ASF project record |
| January 2015 HDFS-6729 discussion explicitly described maintenance as soft state across NN restart/failover | H/P | high | abandoned/duplicated proposal lineage |
| April 2015 HDFS-7877 design required maintenance admin state to survive NN restart | H/P | high | design document, not released implementation |
| the same design left timeout support open and suggested external handling | H/P | high | design-stage position only |
| October 2015 HDFS-7877 discussion proposed persisting expiration UTC time | H/P | high | design discussion, not yet implementation |
| HDFS-9392 added configured `maintenanceExpireTimeInMS` while comparing against `Time.monotonicNow()` | H/P | very high | inspected Apache commit |
| HDFS-11296 changed the comparison to `Time.now()` and tests to epoch-based deadlines | H/P | very high | inspected Apache commit |
| HDFS-12473 retained expiry in combined JSON host records while regularizing JSON format | H/P | very high | inspected Apache commit |
| Hadoop 3.0.1 treats admin properties as static configuration distinct from runtime state and reloads them through `CombinedHostFileManager` | H/P | very high | released source |
| persisted scalar needs a stable interpretation context to preserve deadline meaning | E | high | direct reconstruction from the clock-domain migration |
| maintenance-state persistence and maintenance-deadline persistence are different obligations | E | high | directly supported by 2015 design chronology |
| the epoch conversion creates a consensus-grade distributed lease | X | rejected | no supporting evidence |
| every HA failover path shares identical configuration distribution and clock behavior | X | open/rejected as current claim | not inspected here |

---

## What this changes in Case 116

The broader Case 116 can now say more precisely that restart continuity did not arrive as one indivisible feature. The public project record shows at least three separately evolving obligations:

```text
1. preserve / reconstruct desired maintenance administrative state
2. preserve / reconstruct the expiry horizon of that authority
3. reconstruct runtime evidence about which replicas/blocks are actually on the node
```

The existing 3.0.1 restart deepening already separates (1)/(2) from (3). This genealogy further separates (1) from (2) and shows why the **clock reference** became part of the persistence contract.

The strongest compact result is:

> **persistent control state = retained representation + retained interpretation rule, not merely retained bytes.**

---

## Remaining debt

This bounded slice does **not** close:

1. exact HA active/standby failover behavior when the two NameNodes have stale, missing, or divergent combined-host configuration files;
2. whether and how every maintenance-related field appears in FSImage/edit-log serialization paths;
3. operational tooling that distributes/atomically replaces the combined JSON file across HA NameNodes;
4. clock-step / skew / NTP fault-injection around `maintenanceExpireTimeInMS`;
5. complete branch/backport genealogy for HDFS-9392, HDFS-11296, and HDFS-12473 across Hadoop 2.x/3.x;
6. production incident evidence caused specifically by expiry-clock or host-file divergence;
7. broad distributed-storage genealogy of maintenance deadlines, leases, and temporary-membership state.

Items 5 and 7 are better suited to `computing-archaeology` if expanded into full technical history. Items 1–4 remain plausible future `technical-retention` slices because they directly concern preservation of maintenance-control authority.
