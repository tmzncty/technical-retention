# Evidence 116 — Hadoop 3.3.5→3.3.6 EC Maintenance Sufficiency Boundary

## Status

**`bounded deepening complete`**

## Scope

This evidence note closes one narrow debt left by Case 116:

> **Can the same maintenance-admission minimum safely govern both ordinary replicated HDFS blocks and erasure-coded striped block groups?**

The bounded comparison is deliberately release-specific:

- Apache Hadoop `rel/release-3.3.5`, tagged 22 March 2023, as a direct released pre-fix witness;
- ASF issue **HDFS-16809**, opened 20 October 2022 and resolved 5 December 2022;
- Apache Hadoop pull request **#5050**, merged 5 December 2022;
- Apache Hadoop `rel/release-3.3.6`, tagged 26 June 2023, as a direct released post-fix witness.

The result is not a general history of HDFS erasure coding, not an invention claim for coded-storage maintenance, and not a claim about all later Hadoop releases. It isolates one retention-control relation: the amount of currently live non-maintenance storage that must remain before a DataNode may safely count as being in maintenance.

This note also does **not** treat HDFS's administrative word `maintenance` as equivalent to physical-media maintenance, DRAM refresh, SSD garbage collection, or RAID scrub. Here it is a distributed control-plane state governing temporary withdrawal and redundancy obligations.

---

## Source custody and exact locations

Primary Apache/ASF materials inspected for this slice:

1. **Apache Hadoop 3.3.5 annotated release tag** — `rel/release-3.3.5`, tag object `3e9942ab64554d5468f90afb46f34af10ddaaa07`, pointing to commit `706d88266abcee09ed78fbaa0ad5f74d818ab0e9`, tagger date 22 March 2023.
   - <https://github.com/apache/hadoop/releases/tag/rel%2Frelease-3.3.5>
   - <https://github.com/apache/hadoop/tree/706d88266abcee09ed78fbaa0ad5f74d818ab0e9>
2. **Hadoop 3.3.5 `DatanodeAdminManager.java`** — released pre-fix maintenance sufficiency predicate.
   - <https://github.com/apache/hadoop/blob/rel/release-3.3.5/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DatanodeAdminManager.java>
3. **ASF HDFS-16809**, “EC striped block is not sufficient when doing in maintenance,” opened 20 October 2022, resolved 5 December 2022.
   - <https://issues.apache.org/jira/browse/HDFS-16809>
4. **Apache Hadoop PR #5050**, merged 5 December 2022, merge commit `02afb9ebe137a024a3dae49af3bf03dacb8c5fc8`.
   - <https://github.com/apache/hadoop/pull/5050>
5. **PR #5050 patch** — changes `DatanodeAdminManager.isSufficient(...)`, exposes `BlockManager.getMinMaintenanceStorageNum(...)` to that caller, and adds `TestMaintenanceWithStriped.java`.
   - <https://github.com/apache/hadoop/pull/5050/files>
6. **Apache Hadoop 3.3.6 annotated release tag** — `rel/release-3.3.6`, tag object `92311d26d0547f7ad247a3f73681e277cdc10ca9`, pointing to commit `1be78238728da9266a4f88195058f08fd012bf9c`, tagger date 26 June 2023.
   - <https://github.com/apache/hadoop/releases/tag/rel%2Frelease-3.3.6>
   - <https://github.com/apache/hadoop/tree/1be78238728da9266a4f88195058f08fd012bf9c>
7. **Hadoop 3.3.6 `BlockManager.java`** — post-fix block-type-aware maintenance minimum and maintenance reconstruction predicates.
   - <https://github.com/apache/hadoop/blob/rel/release-3.3.6/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/BlockManager.java>
8. **Hadoop 3.3.6 `DatanodeAdminManager.java`** — post-fix maintenance-admission caller.
   - <https://github.com/apache/hadoop/blob/rel/release-3.3.6/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/DatanodeAdminManager.java>
9. **Hadoop 3.3.6 `TestMaintenanceWithStriped.java`** — released regression test for striped maintenance.
   - <https://github.com/apache/hadoop/blob/rel/release-3.3.6/hadoop-hdfs-project/hadoop-hdfs/src/test/java/org/apache/hadoop/hdfs/TestMaintenanceWithStriped.java>
10. **Current/continuity `BlockInfoStriped#getRealDataBlockNum()` implementation** — documents the distinction between a full stripe's configured data-unit count and a short block group's actual data internal-block count.
   - <https://github.com/apache/hadoop/blob/trunk/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/BlockInfoStriped.java>

A fresh search in `tmzncty/computing-archaeology` for `HDFS-16809`, HDFS maintenance, and erasure-coded maintenance found no dedicated overlapping study. A broader history of HDFS erasure coding or distributed-store maintenance modes therefore remains a companion-repository task rather than something to reproduce here.

---

## Historical record

### H/P — Hadoop 3.3.5 used one generic maintenance-replication threshold in `isSufficient(...)`

The released Hadoop 3.3.5 `DatanodeAdminManager.isSufficient(...)` distinguishes decommission from maintenance. Its maintenance branch admits sufficiency when the count of live replicas is at least `blockManager.getMinReplicationToBeInMaintenance()`.

In that released method, the maintenance test is not conditioned on whether the block is an ordinary replicated block or a striped erasure-coded block group.

The relevant shape is:

```text
isMaintenance
    + live-count >= configured maintenance minimum
    -> sufficient
```

This is historical implementation evidence, not merely a reconstruction from later bug reports.

The surrounding class documentation likewise describes maintenance entry in replication-oriented language: blocks need to be replicated at least to `dfs.namenode.maintenance.replication.min`, after which a DataNode can enter `IN_MAINTENANCE` and the ordinary replication factor may remain relaxed until expiry.

This note does not infer that every 3.3.5 deployment necessarily encountered an unsafe EC state. It establishes only the released predicate inspected here.

### H/P — HDFS-16809 identified striped-block maintenance sufficiency as a concrete bug

ASF issue HDFS-16809 was opened on 20 October 2022 under the title **“EC striped block is not sufficient when doing in maintenance.”** Its short problem statement says that, during maintenance, an EC striped block can be insufficient and can lead to a missing-block condition.

The issue was resolved on 5 December 2022. The ASF record associates the fix with Hadoop 3.4.0, 3.2.5, and 3.3.6 release lines.

This issue is evidence that the generic maintenance-sufficiency relation was recognized inside the Hadoop project as inadequate for at least one erasure-coded regime.

It is **not** evidence of a public production data-loss incident. The issue description is a project bug statement, not an incident report, forensic postmortem, or independent field study.

### H/P — PR #5050 changes the decision from a generic configured minimum to a block-type-aware minimum

Apache Hadoop PR #5050, merged 5 December 2022, makes the central correction in a very small production-code diff.

Before the patch, `DatanodeAdminManager.isSufficient(...)` uses:

```text
getMinReplicationToBeInMaintenance()
```

After the patch, the same maintenance decision uses:

```text
getMinMaintenanceStorageNum(block)
```

The patch simultaneously changes `BlockManager.getMinMaintenanceStorageNum(...)` from private to package-visible so `DatanodeAdminManager` can call it.

The important historical fact is therefore not merely “a test was added.” The **authority predicate for entering/remaining in the maintenance transition was changed to depend on the redundancy representation of the block being evaluated.**

### H/P — Hadoop 3.3.6 explicitly gives replicated and striped blocks different maintenance minima

The released Hadoop 3.3.6 `BlockManager` documents the maintenance safety relation in its class comment and then implements it in `getMinMaintenanceStorageNum(BlockInfo block)`.

For ordinary replicated blocks, the method returns the smaller of:

- the configured maintenance minimum; and
- the block's own replication factor.

For striped blocks, it instead returns:

```text
BlockInfoStriped#getRealDataBlockNum()
```

The class comment states the same distinction directly: regular replication uses the maintenance-replication configuration key, while erasure encoding uses the striped block's real data-block count.

This is a released product/source contract. It establishes a specific Hadoop rule; it does not establish a universal theorem that every coded store must use the same formula.

### H/P — the same block-type-aware predicate is used for maintenance reconstruction pressure

The 3.3.6 `BlockManager.isNeededReconstructionForMaintenance(...)` asks whether a complete block has fewer live replicas than `getMinMaintenanceStorageNum(storedBlock)` or fails the placement policy.

Thus, in this release, the corrected minimum is not isolated to one cosmetic status check. It also participates in deciding whether maintenance-related reconstruction work is needed.

A second method, `getExpectedLiveRedundancyNum(...)`, also floors the expected live count at `getMinMaintenanceStorageNum(block)` after accounting for maintenance replicas.

This gives the block-type-aware minimum a broader control role:

```text
maintenance admission / sufficiency
    +
maintenance reconstruction need
    +
expected live redundancy floor
```

share the same representation-aware threshold relation in the inspected release.

### H/P — `getRealDataBlockNum()` is not simply a hard-coded full-stripe `k`

`BlockInfoStriped#getRealDataBlockNum()` distinguishes a full stripe from a short block group. For a complete or committed block group, it returns the smaller of:

- the erasure-coding policy's data-unit count; and
- the number of data internal blocks actually required by the block group's byte length and cell size.

Therefore the 3.3.6 maintenance threshold should not be paraphrased carelessly as “always keep the configured number of data units live.” For a short final block group, the implementation can use the **actual data-block count represented by that group**.

This is an important anti-overgeneralization boundary:

> `EC maintenance minimum = real data-block count in this implementation`
>
> is more precise than
>
> `EC maintenance minimum = one universal fixed k`.

### H/P — the released regression test reconstructs enough live internal blocks before accepting the bounded scenario

`TestMaintenanceWithStriped.testInMaintenance()` in Hadoop 3.3.6 creates an erasure-coded file using the test suite's default policy and begins with a block group described by the test as internal blocks `d0` through `d8`.

It then places five holders (`d4` through `d8`) into maintenance. The test waits for the maintenance transition and inspects the resulting block group.

Its own explanatory comment records the post-reconstruction state as:

```text
6 live internal blocks
+ 5 in-maintenance internal blocks
= 11 total internal-block embodiments
```

The test asserts the six-live / five-maintenance counts and verifies that a file checksum taken after the transition matches the checksum taken before it.

This is useful **project regression evidence** that the intended fixed behavior reconstructs additional live internal blocks rather than accepting the old smaller live set.

It is not independent storage validation, a proof against all correlated failures, or a field measurement of production repair timing.

---

## Engineering reconstruction

### E — one administrative label does not imply one preservation predicate

Both replicated and erasure-coded data may be placed under the same HDFS administrative state, `IN_MAINTENANCE`. But the representation underneath that administrative label differs.

For a replicated block, each valid replica is an alternative full embodiment of the block payload. A live-replica count can therefore serve directly as a quantity of surviving complete embodiments.

For a striped erasure-coded block group, a live count refers to internal blocks whose joint recoverability depends on coding geometry. “One live storage” and “one full payload copy” are not the same unit.

So the fixed release makes explicit:

> **same maintenance state != same sufficiency predicate across redundancy representations.**

### E — replica-count policy and coded reconstructability policy are different relations

A configurable scalar named `maintenance.replication.min` is meaningful for replicated blocks because the counted objects are full replicas. Reusing that scalar unchanged for an EC block group can admit a live set that is below the representation's reconstruction floor.

The corrected implementation therefore separates:

```text
replicated block
    -> configured minimum of full replicas

striped block group
    -> real data-internal-block minimum
```

This supports the bounded project statement:

> **replica-count floor != coded reconstructability floor.**

The phrase `coded reconstructability floor` is an engineering reconstruction. Hadoop's historical identifiers are `getMinMaintenanceStorageNum` and `getRealDataBlockNum`.

### E — temporary withdrawal optimization cannot erase the current recoverability floor

Case 116's original maintenance mechanism deliberately avoids the full cost of decommission because the same DataNode is expected to return. That expectation permits some ordinary redundancy obligations to be relaxed for a bounded interval.

HDFS-16809 shows the limit of that optimization. Expected future return cannot safely substitute for the present minimum needed to preserve the block group's recoverable state under the maintenance contract.

So:

> **expected return can justify reduced redundancy work**
>
> but
>
> **expected return != permission to cross the current representation's minimum recoverability floor.**

This is a retention-specific result: a future-oriented administrative expectation is useful control state only within a mechanically valid preservation envelope.

### E — “maintenance replicas still count” does not mean they are ordinary live service units

The fixed 3.3.6 class-level safety description keeps separate:

- live replicas/internal blocks;
- maintenance replicas/internal blocks;
- expected redundancy;
- a minimum live floor.

The maintenance relation can credit temporarily withdrawn embodiments toward the broader topology while still demanding a representation-specific live minimum.

Thus:

> **maintenance credit != ordinary live service availability**

and:

> **live minimum != full redundancy restoration**.

The latter matters because reaching the data-block floor is not the same as restoring all parity/internal-block redundancy or completing every later convergence task.

### E — sufficiency is not only a count; placement remains separate

The 3.3.6 maintenance reconstruction predicate also checks `isPlacementPolicySatisfied(storedBlock)`.

Therefore this slice must not reduce safety to a single number. The count threshold answers one question — whether enough live storage units remain for the block's representation — while placement policy answers another — whether those embodiments satisfy the configured topology/failure-domain constraints.

So:

> **enough live internal blocks != placement policy satisfied.**

This is another reason not to describe HDFS-16809 as proving one universal algebraic rule for all failure scenarios.

### E — persisted policy intent and correct policy semantics are separate retention problems

The earlier Case 116 restart deepening showed that maintenance intent and expiry can survive/reconstitute across a NameNode restart through retained host configuration, while runtime embodiment knowledge may need to be re-observed.

The HDFS-16809 slice adds a different boundary:

> **policy persistence != policy correctness.**

A maintenance request may be perfectly retained across restart and still be unsafe if the sufficiency predicate applied to an EC block group is wrong. Conversely, a correct predicate is not useful if the policy state itself is lost or mis-reconstituted.

These are independent layers:

```text
maintenance intent survives?
    !=
current embodiments are known?
    !=
sufficiency predicate matches representation?
    !=
transition/convergence completed?
```

This is a same-system functional decomposition, not a claim that HDFS developers historically framed the bug in these philosophical terms.

---

## Functional comparison

### A — Case 80 decommissioning: same system, different administrative horizon

Case 80 studies planned retirement, while Case 116 studies temporary withdrawal. Both require the NameNode to decide whether enough acceptable state remains elsewhere before changing a node's administrative role.

The HDFS-16809 deepening adds that “enough” cannot be assumed to mean the same thing for replicated and coded representations.

This is a direct same-system engineering comparison. It does not mean maintenance and decommission use identical thresholds or reconstruction topology.

### A — coded-recovery cases: decode sufficiency != restored redundancy margin

The repository's RAID/ZFS/EC cases already distinguish the ability to reconstruct a payload from the later restoration of redundancy margin.

Case 116 now supplies an HDFS maintenance-admission version of that distinction:

- the real-data-block count acts as a bounded live floor for striped maintenance;
- the system may create additional internal-block embodiments to reach that floor;
- reaching that floor does not mean every parity/internal block is live or that all future repair/placement work is complete.

This is a **functional analogy** to coded-recovery cases, not a genealogy between HDFS EC and RAID/ZFS designs.

### A — no cross-repository genealogy is asserted

A search of `tmzncty/computing-archaeology` found no dedicated HDFS-16809/EC-maintenance module to reuse. This evidence note therefore keeps only the retention-specific control relation.

If a wider history of HDFS erasure coding, striped reconstruction, or distributed maintenance modes is written later, it should live primarily in `computing-archaeology` and be linked here.

---

## Philosophical interpretation

### I — a retained policy is not sufficient unless its predicate fits the representation it governs

A narrow conceptual conclusion survives the engineering details:

> **Persistence of a rule is not persistence of the condition that makes the rule valid.**

HDFS can retain the same administrative word — maintenance — across replicated and erasure-coded data, but the preservation relation underneath that word is representation-dependent. A policy that is meaningful for complete replicas can become inadequate when its counted units are coded fragments.

This does not establish a universal philosophical law, and it is not Hadoop's historical vocabulary. It is a bounded interpretation of the exact correction from a generic scalar threshold to a block-type-aware sufficiency predicate.

---

## Explicit non-equivalences fixed by this deepening

- `same administrative maintenance state != same sufficiency predicate for every redundancy representation`;
- `replica count != count of full payload copies for an EC striped block group`;
- `dfs.namenode.maintenance.replication.min != universal EC decode threshold`;
- `getRealDataBlockNum() != always the configured full-stripe data-unit count`;
- `enough live internal blocks != full parity/redundancy restoration`;
- `enough live internal blocks != placement policy satisfied`;
- `maintenance replica retained in accounting != ordinary live/read service eligibility`;
- `expected DataNode return != permission to cross the current recoverability floor`;
- `maintenance intent persisted != maintenance policy mechanically correct`;
- `project regression test != independent production validation`;
- `HDFS-16809 bug statement != proof of a public production data-loss incident`;
- `fixing maintenance sufficiency != inventing HDFS erasure coding or maintenance mode`;
- `3.3.5 released predicate != claim that every 3.3.5 deployment necessarily failed`;
- `3.3.6 fixed release witness != universal semantics for every later Hadoop branch`;
- `functional similarity to RAID/ZFS coded recovery != shared genealogy`.

---

## Claim ledger

| Claim | Type | Evidence | Confidence | Boundary |
|---|---|---|---|---|
| Hadoop 3.3.5 `isSufficient(...)` uses the generic maintenance-replication minimum for maintenance admission | Historical record | released 3.3.5 `DatanodeAdminManager.java` | high | method/release specific |
| HDFS-16809 identifies EC striped maintenance insufficiency as a bug | Historical record | ASF JIRA HDFS-16809 | high | project bug record, not field incident |
| PR #5050 changes maintenance sufficiency to `getMinMaintenanceStorageNum(block)` | Historical record | Apache PR #5050 patch | high | exact patch only |
| Hadoop 3.3.6 uses `getRealDataBlockNum()` for striped maintenance minimum | Historical record | released 3.3.6 `BlockManager.java` | high | release specific |
| Replicated blocks retain a configuration-derived maintenance minimum | Historical record | released 3.3.6 `BlockManager.java` | high | bounded implementation contract |
| Short block groups may have a real data-block count below the policy's full data-unit count | Historical record | `BlockInfoStriped#getRealDataBlockNum()` | high | implementation semantics, not universal EC law |
| 3.3.6 regression test reaches six live + five maintenance internal blocks and preserves file checksum in its bounded scenario | Historical record / experiment | released `TestMaintenanceWithStriped.java` | high for test intent | project test, not independent field validation |
| Same admin state can require representation-specific preservation predicates | Engineering reconstruction | 3.3.5→3.3.6 correction | high | bounded to inspected relation |
| Replica-count floor and coded reconstructability floor should remain distinct | Engineering reconstruction | helper split + striped real-data threshold | high | terminology is project vocabulary |
| Policy persistence and policy correctness are separate retention relations | Engineering reconstruction | Case 116 restart deepening + HDFS-16809 | medium-high | conceptual decomposition |
| Coded-maintenance admission resembles other coded-recovery “recoverability vs restored margin” distinctions | Functional analogy | Case 116 + mature coded-recovery cases | medium | no genealogy |

---

## Remaining evidence debt

This slice closes only the bounded 3.3.5→3.3.6 maintenance-sufficiency seam. Useful later work remains:

1. trace the exact branch/backport genealogy into 3.2.5, 3.3.6, and the 3.4 line rather than inferring it from fix-version labels alone;
2. test short final block groups explicitly, where `getRealDataBlockNum()` is below the full policy data-unit count;
3. compare several EC policies and failure-domain layouts instead of relying on the released default-policy regression test;
4. inject node loss during `ENTERING_MAINTENANCE`, after `IN_MAINTENANCE`, and around expiry to observe reconstructability and convergence boundaries;
5. inspect HA active/standby failover with EC maintenance state rather than assuming the process-restart path covers it;
6. find production/operator incident evidence, if any, without upgrading a JIRA bug report into an incident claim;
7. keep wider HDFS EC history, decoder/reconstruction implementation history, and cross-store maintenance-mode genealogy in `computing-archaeology` if developed.

---

## Result

The bounded result is:

```text
one administrative maintenance regime
    !=
one encoding-independent sufficiency rule

replicated block
    -> full-replica maintenance floor

striped EC block group
    -> real data-internal-block maintenance floor
    + separate placement qualification

expected future return
    -> can relax ordinary redundancy work
    != can cross present recoverability minimum
```

This deepening therefore partially closes Case 116's earlier open `erasure-coded behavior` debt without turning the case into a general HDFS EC history.
