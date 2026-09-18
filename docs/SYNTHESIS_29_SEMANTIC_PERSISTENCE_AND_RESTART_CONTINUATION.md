# Synthesis 29 — Semantic Persistence and Restart Continuation

**Status:** bounded cross-case synthesis  
**Updated:** 2026-09-18  
**Scope:** Cases 04, 36, 116, and 136; refinement of [`Synthesis 26`](SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md)  
**Evidence basis:** already-grounded primary/contemporary case evidence. This synthesis adds no new invention-priority claim and does not assert one genealogy among TrueFFS mapping recovery, NAND/SSD controller refresh, HDFS administrative maintenance, and RAID-controller repair.

---

## 1. Question

`Synthesis 26` separates maintenance state by persistence horizon: request-local, runtime, restart-persistent, authority-bound, and configuration/control-plane persistent state.

Recent evidence sharpens a second question that cannot be answered only by asking whether some bits survive restart:

> **When a control or currentness relation remains usable after interruption, what exactly has survived: the relation itself, one runtime representation of it, the task, its progress, the meaning of a stored value, or the authority to continue?**

The four cases in this slice provide deliberately different counterexamples:

- **Case 04:** the live TrueFFS RAM mapping table can disappear at power loss while Flash-resident mapping/header evidence survives and allows a runtime map to be reconstructed or verified after restart;
- **Case 36:** an elapsed-time record can survive power cycles while intentionally representing cumulative **powered-on intervals**, not complete wall-clock retention age;
- **Case 116:** an externally retained deadline scalar can survive while its intended meaning is unstable if a later process interprets it in a new JVM-local monotonic-clock coordinate system;
- **Case 136:** a controller can promise that rebuild/check-consistency work continues after power failure/reset/hard boot without the inspected source disclosing an exact stripe/LBA progress checkpoint.

The result is a refinement of the repository's persistence vocabulary:

```text
relation survival
    != representation survival
    != semantic survival
    != exact progress survival
    != restart authority
```

A retained relation may persist strongly along one of these dimensions and weakly or opaquely along another. In particular, exact persistence of a volatile runtime representation is not always required when authoritative evidence survives and a later runtime can reconstruct an equivalent operational relation.

---

## 2. Claim discipline

This synthesis follows [`METHOD.md`](METHOD.md) and [`AGENTS.md`](../AGENTS.md).

### H/P / H/C — historical and implementation record

Historical dates, product vocabulary, source wording, and implementation facts remain grounded in the individual case/evidence records:

- [`Case 04 deepening — TrueFFS mapping power-failure reconstruction`](../evidence/04-trueffs-2003-2004-mapping-power-failure-reconstruction-deepening.md);
- [`Case 36 deepening — Intel power-cycle elapsed-time refresh state`](../evidence/36-intel-2011-2013-power-cycle-elapsed-time-refresh-deepening.md);
- [`Case 116 deepening — Hadoop maintenance-expiry clock/persistence genealogy`](../evidence/116-hadoop-2014-2017-maintenance-expiry-clock-persistence-genealogy-deepening.md);
- [`Case 136 deepening — LSI FlexRAID PowerFail`](../evidence/136-lsi-2006-flexraid-powerfail-maintenance-continuation-deepening.md).

Case 04 uses manufacturer-primary M-Systems product documentation together with contemporary Wind River TrueFFS integration documentation. The other case packets preserve their own source classes. This synthesis does not flatten those source layers into one evidentiary category.

### E — engineering reconstruction

Terms introduced here such as **semantic persistence**, **interpretation frame**, **task continuity**, **relation reconstitution**, **representation continuity**, and **restart authority** are project analytical vocabulary unless a source independently uses an equivalent term.

### A — functional analogy

The comparison is relational. It does **not** claim that Flash mapping reconstruction, Flash refresh metadata, HDFS host configuration, and MegaRAID firmware use the same representation, recovery algorithm, clock model, durability primitive, or historical lineage.

### I — philosophical interpretation

Interpretive statements about retaining a usable past are downstream of the engineering record. They are not attributed to M-Systems, Wind River, Intel, Apache Hadoop contributors, or LSI.

---

## 3. Historical / implementation record

### 3.1 Case 36 — a cross-power maintenance clock can preserve a selected history rather than total physical age

The Intel-origin record inspected in Case 36 is U.S. application `13/174,926`, later published as **US20130007344A1** and granted as **US8650353B2**, _Apparatus, system, and method for refreshing non-volatile memory_. The application was filed on **2011-07-01** and publicly published on **2013-01-03**.

The record describes elapsed-time or timestamp state associated with data/data locations. That control state can be stored in nonvolatile memory at power-down, loaded again after power-up, compared with a refresh threshold, and reset when the data is moved to a fresh physical location.

The important persistence relation is therefore:

```text
nonvolatile elapsed-time / timestamp record
    -> power interruption
    -> reload into runtime controller state
    -> threshold evaluation
    -> possible refresh / relocation
```

But the worked timing semantics in the inspected disclosure accumulate **powered-on intervals** across operating sessions. The stored timer therefore does not automatically mean:

```text
wall-clock time since programming
```

or:

```text
complete physical retention age including all unpowered intervals
```

The historical record supports cross-power continuity of a maintenance-time representation. It does not support equating that representation with every physical aging process affecting the medium.

### 3.2 Case 116 — retaining a deadline scalar did not by itself preserve a restart-stable clock coordinate

The HDFS maintenance-state genealogy shows a different failure mode.

The project moved from an early 2014–January 2015 proposal in which maintenance could be treated as soft state across NameNode restart/failover, to an April 2015 HDFS-7877 design in which a DataNode should remain in the same administrative state after NameNode restart.

By August 2016, HDFS-9392 placed `maintenanceExpireTimeInMS` in static administrative properties that could be reloaded. Yet the implementation still compared the externally retained value with `Time.monotonicNow()`.

A JVM monotonic clock is useful for elapsed-time measurement inside one process lifetime, but a new process does not inherit the old process's monotonic-clock origin as a portable external coordinate.

HDFS-11296 therefore changed the comparison in January 2017 from:

```text
Time.monotonicNow() < maintenanceExpireTimeInMS
```

to:

```text
Time.now() < maintenanceExpireTimeInMS
```

and the tests changed accordingly.

The narrow historical result is not that wall clock is universally superior. It is that the project aligned an externally retained/reloaded deadline with a reference frame that a later process could interpret as an externally expressible epoch-time contract.

Thus the source trail directly motivates:

```text
persisted scalar
    != persisted deadline meaning
```

unless the interpretation coordinate also remains valid.

### 3.3 Case 136 — maintenance continuation can be promised without disclosing exact work-position persistence

The 2006 LSI _MegaRAID Configuration Software User's Guide_ documents both ordinary rebuild restart behavior and the named **`FlexRAID PowerFail`** control.

The manual states that if a system goes down during rebuild, the controller automatically restarts the rebuild after reboot. WebBIOS describes `FlexRAID PowerFail` as allowing reconstruction, rebuild, and check consistency to continue after power failure, reset, or hard boot; the documented default is Enabled.

This establishes a cross-restart maintenance relation:

```text
maintenance task exists
    -> interruption
    -> controller restart
    -> selected maintenance class is re-entered / continued
```

The inspected manual does **not** disclose whether the controller persists:

- an exact stripe number;
- an exact LBA/extent frontier;
- a bitmap;
- a percentage;
- a bounded replay window;
- or some other progress representation.

Therefore the historical record supports **maintenance-task continuation**, not a claim of exact progress-checkpoint persistence.

### 3.4 Case 04 — TrueFFS can lose the live RAM map while retaining enough evidence to rebuild the relation

The 2003–2004 TrueFFS evidence adds a different restart pattern. M-Systems' September 2004 _DiskOnChip 2000 DIP Data Sheet_ states that actual mapping information is stored in Flash, while the RAM-resident table is used to locate that mapping information and is reconstructed after power-up/reset. Wind River's March 2003 _VxWorks Programmer's Guide 5.5_ independently describes critical mapping information as Flash-resident and says the RAM mapping table is reconstructed or verified after power restoration or media reconnection; predictable erase-unit header information participates in that reconstruction/checking path.

The bounded restart relation is therefore:

```text
volatile RAM mapping view disappears
    + Flash-resident mapping / header evidence survives
    + restart procedure interprets that evidence
    -> usable runtime mapping view is reconstructed / verified
```

The same source record keeps currentness and interruption discipline separate. A new candidate sector is not treated as current merely because a physical write was attempted; old data remain available until the replacement operation completes and is verified. Interrupted garbage collection is restarted rather than promoted to completed maintenance progress.

This supports a stronger distinction than simple bit persistence:

```text
runtime representation survives
    != logical/currentness relation survives
```

The inspected sources do **not** expose the exact on-media generation counter, commit-bit layout, ordering protocol, or algorithm that resolves every possible competing mapping record. Nor do they say that the post-restart RAM table is byte-for-byte identical to the pre-failure in-memory structure.

---

## 4. Engineering reconstruction — five different continuity dimensions

The four cases make it useful to separate five dimensions.

### 4.1 Obligation / task identity persistence

Question:

> After restart, does the system still know that some maintenance obligation exists or that some maintenance class should continue?

Case 136 grounds this strongly: rebuild/check-consistency continuation is explicitly represented as controller behavior/policy.

Case 116 also has an administrative-state form of this relation: later HDFS designs require the DataNode's maintenance state to survive NameNode restart through reloadable administrative configuration.

Case 36 carries a different form: retained age/timestamp metadata can cause a later controller runtime to reconstruct that refresh may be due.

Case 04 is not primarily a maintenance-obligation case. Its strongest restart object is the **logical resolution/currentness relation** itself, reconstructed from retained evidence.

This is **not yet** progress persistence.

### 4.2 Progress / checkpoint persistence

Question:

> How much already-completed work can the restarted system distinguish from work still outstanding?

The four records provide different answers.

- Case 136 does not expose enough information to characterize an exact rebuild/check-consistency checkpoint.
- Case 36 retains a compact temporal summary but that summary is not a byte/erase-block migration checkpoint for all previous maintenance work.
- Case 116's maintenance expiry is a deadline relation, not a progress counter through a maintenance scan.
- Case 04 explicitly permits interrupted garbage collection to restart; the inspected documentation does not require a persisted exact GC frontier in order to recover a coherent current mapping relation.

Accordingly:

```text
maintenance continuity
    != exact work-position continuity
```

and:

```text
restart continuation
    != exactly-once maintenance execution
```

A system may safely repeat some work, reconstruct work from other state, or resume from a coarser checkpoint.

### 4.3 Semantic / interpretation-frame persistence

Question:

> If a scalar, timestamp, counter, identifier, status bit, or mapping record survives, can a later runtime interpret it in the same operational coordinate system?

This is the dimension Case 116 exposes most sharply.

A stored value can be bitwise unchanged yet become semantically unusable if its coordinate is process-local and the process that defined that coordinate is gone.

A compact project-level reconstruction is:

```text
retained value
    + stable interpretation frame
    -> restart-usable meaning
```

This is not a mathematical sufficiency theorem. Other authority, validation, freshness, and consistency conditions may still apply.

The point is only that:

```text
bitwise persistence
    != semantic persistence
```

Case 36 supplies a complementary counterexample. Its persisted time record can remain semantically well-defined across reboot while still representing only the history the controller chose to accumulate. Stable semantics do not imply complete physical history.

Case 04 adds another qualification: retained Flash-resident mapping evidence is useful only because restart software knows how to interpret/cross-check that evidence into a usable current mapping view. Surviving bytes alone are not the whole recovery contract.

Thus:

```text
semantic persistence
    != completeness of represented history
```

and:

```text
retained evidence
    != self-interpreting evidence
```

### 4.4 Restart authority / continuation policy

Question:

> Even if task identity, progress, and interpretation survive, is the restarted component actually authorized or required to continue?

Case 136 makes this visible as a named policy surface: `FlexRAID PowerFail` is a controller option rather than an invisible consequence of repair being possible.

Case 116 similarly shows that restart continuity was a design decision that changed over time: early proposal-level soft state could be discarded, while later design explicitly required maintenance administrative state to remain after restart.

Case 04 shows a different authority relation: Flash-resident evidence can support reconstruction, but a candidate physical write does not automatically acquire currentness. The recovery procedure must re-establish which embodiment is admissible as the current logical sector.

Therefore:

```text
recoverable state
    != authority to resume
```

and:

```text
state can be reconstructed
    != system policy says it must be reconstructed
```

and:

```text
candidate embodiment exists
    != candidate embodiment has currentness authority
```

### 4.5 Representation persistence / relation reconstitution

Question:

> Must the exact runtime data structure survive, or is it enough for a later runtime to reconstruct an equivalent operational relation from retained evidence?

Case 04 supplies the clearest direct counterexample to a representation-centric model. The live RAM mapping table is volatile. The historical product/integration documentation nevertheless says the mapping relation can be reconstructed or verified from Flash-resident evidence after restart.

So:

```text
representation R1 disappears
    + authoritative/reconstructible evidence E survives
    + reconstruction procedure remains available
    -> operationally usable relation R2 is re-established
```

The synthesis deliberately says **operationally usable relation**, not `R2 == R1` byte-for-byte.

This yields two project rules:

> **relation continuity does not require persistence of every runtime representation of that relation.**

> **reconstructibility is itself conditional on retained evidence plus a surviving interpreter/procedure.**

This dimension is adjacent to [`Synthesis 23`](SYNTHESIS_23_RETENTION_INTERPRETER_ACCESS_APPARATUS.md), but the emphasis here is narrower: restart continuation of an operational relation after one representation has vanished.

---

## 5. Cross-case matrix

| Case | Retained / reconstructed control/currentness state | Interruption boundary | Interpretation frame | Restart behavior grounded | Exact progress grounded? | Key non-claim |
| --- | --- | --- | --- | --- | --- | --- |
| 04 — TrueFFS mapping | Flash-resident mapping/header evidence; volatile RAM map is reconstructed or verified | power loss / reset / media reconnection | TrueFFS mapping/header interpretation and currentness rules | rebuild/verify runtime mapping view; incomplete GC restarts | No exact GC frontier or mapping-generation algorithm is exposed | reconstructed relation does not imply byte-identical RAM-table persistence or universal FTL crash atomicity |
| 36 — Intel NVM refresh | elapsed-time / timestamp record associated with data/location | power-down / power-up | disclosed elapsed-time semantics; worked example accumulates powered-on intervals | reload timing state; evaluate refresh threshold; possibly relocate/renew | No — this is maintenance-age state, not a complete migration checkpoint | persisted elapsed time is not automatically complete wall-clock retention age |
| 116 — HDFS maintenance | administrative state + `maintenanceExpireTimeInMS` in external/static configuration | NameNode/JVM restart | evolved from process-local monotonic comparison to externally interpretable epoch-time comparison | later design/runtime can reload maintenance intent and expiry | Not applicable as a scan frontier; this is administrative/deadline state | epoch deadline is not a consensus lease and does not remove wall-clock skew/step risks |
| 136 — MegaRAID | maintenance obligation / continuation policy for rebuild, reconstruction, check consistency | power failure / reset / hard boot | no clock semantics needed for the documented claim | maintenance class continues/re-enters after restart | **Not established** by inspected manual | continuation does not prove exact stripe/LBA checkpoint or exactly-once work |

The matrix is intentionally asymmetric. “No” and “not established” do different work: the first says a field has another role; the second marks an evidence gap.

---

## 6. Anti-conflation ledger

### 6.1 Control-state survival != semantic survival

A value may survive at the bit level while losing the coordinate needed to interpret it.

Case 116 is the strongest witness.

### 6.2 Semantic survival != complete historical capture

A retained summary may remain perfectly meaningful while intentionally omitting parts of physical history.

Case 36 is the strongest witness: cross-reboot accumulated powered-on time is not thereby total unpowered-plus-powered retention age.

### 6.3 Task continuation != exact progress resumption

A system may know which maintenance operation remains due without the source proving the exact work frontier.

Case 136 is the strongest witness, while Case 04 shows that coherent restart may coexist with restarting an interrupted GC operation rather than preserving an exact GC frontier.

### 6.4 Restart continuity != exactly-once maintenance

Nothing in the four cases proves that no maintenance unit can be replayed after interruption.

Repeated work can be compatible with correct continuation.

### 6.5 Persisted deadline != perfect distributed time

HDFS's move to epoch time makes the deadline interpretable across process boundaries. It does not make clocks perfectly synchronized or immune to NTP adjustments, manual changes, leap behavior, or deployment-specific clock faults.

### 6.6 Persisted maintenance timer != physical-retention oracle

Controller bookkeeping can be one input to a maintenance decision without being a direct measurement of physical charge loss, threshold shift, or remaining retention margin.

### 6.7 Configured continuation != existence of repair capability

Case 136 shows that “repair can run” and “repair should be resumed after interruption” are separate policy questions.

### 6.8 Runtime representation survival != relation survival

Case 04 blocks the shortcut that a logical/currentness relation survives only when its in-memory table survives unchanged.

A stronger restart decomposition is:

```text
retained authoritative evidence
    + surviving interpretation/reconstruction procedure
    -> reconstructed operational relation
```

This does not make the runtime representation irrelevant. It means the representation can be **derived state** rather than the sole authority-bearing embodiment.

### 6.9 Relation reconstitution != every in-flight mutation survived

TrueFFS documentation explicitly preserves a counterexample for first-time new data: if no older safely stored version exists, new in-flight data may still be lost.

Therefore:

```text
coherent mapping after restart
    != every requested write survived
```

A system can recover a coherent current-state relation while legitimately losing an update that never crossed its publication/durability boundary.

---

## 7. Relation to Synthesis 26

[`Synthesis 26`](SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md) asks **how long maintenance control state must survive**.

This synthesis adds an orthogonal question:

> **What must remain invariant, or be reconstructible, for the retained relation to mean the same operational thing after that horizon has been crossed?**

A two-axis model is therefore safer than one persistence ladder:

```text
Axis A — persistence horizon
    request-local
    runtime
    restart-persistent
    role/authority-bound
    configuration/control-plane persistent

Axis B — continuity dimension
    operational relation / currentness
    runtime representation / reconstitution evidence
    obligation / task identity
    progress / checkpoint
    semantic interpretation frame
    restart authority / policy
```

A control object can occupy different positions on the two axes.

For example:

- a RAM mapping table can be volatile while the relation it represents is restart-reconstructible from Flash evidence;
- a deadline can be configuration-persistent but semantically defective across restart if its clock coordinate is process-local;
- a rebuild can be restart-continuous while its exact progress representation remains undocumented;
- an elapsed-time record can be restart-persistent and semantically stable while representing only selected operating intervals.

This refinement prevents `restart-persistent` from becoming a catch-all synonym for “fully recoverable,” and prevents `volatile representation` from becoming a synonym for `volatile relation`.

---

## 8. Bounded functional analogies

### A — checkpoint systems

A checkpoint commonly separates “which computation/task exists” from “where execution resumes.” Case 136 has a functionally similar distinction between maintenance-task continuation and an undisclosed exact rebuild frontier.

This is an analogy only. No shared checkpoint format or algorithm is claimed.

### A — leases and deadlines

Distributed systems often need a time value plus a defined clock/reference frame. Case 116 is functionally comparable at that level.

But HDFS maintenance expiry is **not** thereby a consensus lease, fencing token, or linearizable expiration mechanism.

### A — compressed histories

Case 36's accumulated elapsed-time control state functions like a compressed history: it preserves the quantity the maintenance policy needs without retaining every power-cycle event or every physical-aging variable.

This does not imply that all compressed maintenance histories are sufficient for every future policy.

### A — regenerated runtime indexes / caches

Case 04 is functionally comparable to systems that discard a volatile derived index or cache and reconstruct it from a more authoritative persisted representation after restart.

The analogy stops at that relation. TrueFFS mapping recovery is not evidence that database indexes, filesystem caches, distributed placement maps, or other reconstructed structures share its on-media format, publication protocol, or failure semantics.

---

## 9. Philosophical interpretation

A narrow interpretation follows from the engineering record:

> A technical system does not preserve “the past” simply by preserving old bits or one frozen data structure. It preserves selected relations that a later state can still interpret, reconstruct where necessary, and act upon.

The selected past can be deliberately incomplete or differently embodied:

- Case 04 preserves enough mapping/currentness evidence to regenerate a runtime relation even though the volatile map itself disappears;
- Case 36 keeps a maintenance-age summary rather than a complete physical history;
- Case 116 shows that a retained number needs a durable interpretive coordinate;
- Case 136 shows that a remembered obligation may be enough to continue even when exact prior work position is not exposed.

This does **not** establish a general philosophy of memory. It is only a project-level interpretation of four engineered restart patterns.

---

## 10. Explicit non-claims

This synthesis does **not** claim that:

1. Intel's patent design was deployed in every Intel SSD or NAND controller;
2. the 2011 filing was public in 2011 — the inspected U.S. application publication is dated 2013-01-03;
3. Case 36's elapsed-time value equals total wall-clock retention age;
4. a persisted timer directly measures charge loss or physical retention margin;
5. HDFS wall-clock/epoch-time deadlines are immune to skew, step, NTP, or administrative clock error;
6. HDFS maintenance expiry is a lease, fencing mechanism, or consensus timestamp;
7. bitwise persistence plus an interpretation frame is universally sufficient for correct recovery;
8. LSI documents the exact persisted stripe/LBA/extent position of rebuild;
9. `FlexRAID PowerFail` proves zero repeated work after restart;
10. restart continuation implies exactly-once execution;
11. all four systems share one historical genealogy;
12. all four systems store control/currentness state in the same persistence domain;
13. all maintenance state should use wall clock;
14. all monotonic clocks are unsuitable for persistence — process-local monotonic time remains useful inside its intended lifetime;
15. a task that can be reconstructed is necessarily authorized to resume;
16. preserving a maintenance obligation implies preserving the payload embodiment it concerns;
17. preserving semantic meaning implies preserving a complete event log;
18. TrueFFS preserves its live RAM mapping table byte-for-byte across power loss;
19. the inspected TrueFFS documentation discloses the exact generation/commit-bit/currentness-selection algorithm for every competing mapping record;
20. coherent TrueFFS restart means every in-flight first-time write survives;
21. TrueFFS's reconstruction procedure is historically or technically ancestral to the HDFS, Intel-refresh, or MegaRAID mechanisms compared here;
22. any case maturity should change solely because this cross-case synthesis exists.

---

## 11. Related-repository boundary

Fresh repository searches for:

- `TrueFFS`;
- `FlexRAID PowerFail`;
- `maintenanceExpireTimeInMS` / HDFS maintenance-expiry specifics;
- the Intel elapsed-time refresh wording;

found no dedicated overlapping packet in `tmzncty/computing-archaeology` for the TrueFFS slice or the already bounded maintenance-control examples.

That repository remains the better home for a future broad history of:

- TrueFFS/DiskOnChip implementation genealogy and on-media mapping formats;
- RAID rebuild checkpoint mechanisms across controller generations;
- distributed-systems clock/deadline design history;
- SSD-controller maintenance metadata evolution.

This repository keeps the narrower retention question:

> **what control/currentness relation must survive or be reconstituted, in what interpretable form, so service or maintenance can remain operationally continuous after interruption?**

---

## 12. Follow-up research debt

This synthesis deliberately leaves several bounded questions open.

### Case 04

- Recover a more detailed primary TrueFFS on-media-format or implementation source that exposes the exact mapping/currentness record selection protocol across power failure.
- Find a named DiskOnChip/TrueFFS fault-injection or restart trace that distinguishes reconstructed mapping relation from the exact pre-failure RAM representation.
- Keep interrupted erase/reuse qualification, mapping-currentness reconstruction, and host-write durability as separate failure contracts.

### Case 36

- Find a commercial Intel product/qualification source that confirms whether an analogous cross-power maintenance timer was deployed.
- Distinguish controller-maintained powered-on age from any product telemetry that exposes true power-off-aware age or host RTC-derived time.

### Case 116

- Trace branch/backport history of HDFS-11296 where useful.
- Keep HA/clock-synchronization behavior separate from the already-grounded representation change.
- Do not re-open the broader maintenance-mode history unless a new source changes the persistence interpretation.

### Case 136

- Find first-party firmware/controller documentation for the actual rebuild/check-consistency checkpoint representation.
- Determine whether continuation resumes from an exact frontier, a coarse bitmap, reconstructed metadata, or bounded replay.
- Trace whether later PERC/MegaRAID generations preserve, rename, or replace `FlexRAID PowerFail` semantics.

### Cross-case

A future bounded synthesis could compare **restart replay tolerance**:

```text
exact-resume required
    vs bounded replay allowed
    vs full maintenance restart allowed
```

but that requires stronger progress-representation evidence than Case 136 currently provides.

A second future comparison could distinguish:

```text
exact representation persistence
    vs relation reconstruction from authoritative retained evidence
    vs semantic inference from surviving physical traces
```

using the current TrueFFS result together with the separately grounded DDR3 scrambling/reconstruction evidence in Case 127. That broader comparison belongs with Synthesis 23/29 coordination rather than being silently folded into this slice.

---

## 13. Navigation and status

This is a **bounded synthesis deepening**, not a new canonical case and not a maturity promotion.

Primary navigation:

- [`Synthesis 26 — Maintenance Control-State Persistence Horizons`](SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md)
- [`Synthesis 23 — Retention, Interpreter, and Access Apparatus`](SYNTHESIS_23_RETENTION_INTERPRETER_ACCESS_APPARATUS.md)
- [`Case 04 — Flash Virtual Mapping`](../cases/04-flash-virtual-mapping-logical-identity.md)
- [`Case 36 — NAND Flash Correct-and-Refresh Maintenance`](../cases/36-nand-flash-correct-and-refresh-maintenance.md)
- [`Case 116 — HDFS DataNode Maintenance State`](../cases/116-hdfs-datanode-maintenance-state.md)
- [`Case 136 — MegaRAID/PERC Rebuild Rate and Repair Priority`](../cases/136-megaraid-perc-rebuild-rate-repair-priority.md)
- [`Case 04 TrueFFS restart-reconstruction deepening`](../evidence/04-trueffs-2003-2004-mapping-power-failure-reconstruction-deepening.md)
- [`Case 36 power-cycle elapsed-time deepening`](../evidence/36-intel-2011-2013-power-cycle-elapsed-time-refresh-deepening.md)
- [`Case 116 expiry-clock persistence genealogy`](../evidence/116-hadoop-2014-2017-maintenance-expiry-clock-persistence-genealogy-deepening.md)
- [`Case 136 FlexRAID continuation deepening`](../evidence/136-lsi-2006-flexraid-powerfail-maintenance-continuation-deepening.md)

No `CASE_INDEX.md` maturity entry changes are implied by this document. The authoritative case maturities remain unchanged; this is a cross-case analytical update only.

### Compact result

```text
restart-persistent / restart-recoverable technical state
    is not one property

it can decompose into:
    relation / currentness continuity
    + representation persistence or reconstitution
    + task / obligation continuity
    + progress continuity
    + semantic / interpretation continuity
    + restart authority

and these dimensions can diverge.
```