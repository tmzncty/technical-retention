# Evidence 05 — Ceph 2006 PG-log retirement authority deepening

## Status

**`bounded deepening complete`**

This record deepens [Case 05 — RADOS Replicated Objects: Retention by Replica Agreement and Repair](../cases/05-rados-replicated-object-repair.md).

It closes one narrow retention question left implicit by the existing 2005–2007 peering evidence:

> **Once one OSD has become locally complete through some PG version, is that local fact by itself enough to retire older PG-log history?**

At the inspected **2006-12-06** Ceph source endpoint, the answer is no. The primary maintains a `peers_complete_thru` frontier derived from completion information for the current acting set, sends that frontier to replicas as `pg_trim_to`, and the PG-log append path only advances the in-memory and on-disk logical trim frontier to that value. The same source also shows that advancing the on-disk log bottom is a **logical read-floor change**, not necessarily immediate physical erasure of the earlier bytes.

The bounded result is therefore:

```text
local PG completion
    != acting-set completion frontier
    != authority to retire older recovery history
    != trim instruction delivered to a replica
    != old log bytes physically erased
```

`history-retirement authority`, `distributed completion frontier`, and `logical retirement` are **engineering-reconstruction terms used by this repository**. They are not historical Ceph vocabulary.

---

## 1. Bounded source custody

Primary source endpoint:

- repository: `ceph/ceph`;
- commit: `283b68e12a9847ca7ea7adb16d9a9b45af138ef3`;
- author/commit date: **2006-12-06 21:04:15 UTC**;
- imported SVN revision: `@977`;
- commit message: `improved support for forcing the first element of a crush result`.

Commit record:

- <https://github.com/ceph/ceph/commit/283b68e12a9847ca7ea7adb16d9a9b45af138ef3>

Files inspected at that exact revision:

- `ceph/osd/PG.h`
  - <https://github.com/ceph/ceph/blob/283b68e12a9847ca7ea7adb16d9a9b45af138ef3/ceph/osd/PG.h>
- `ceph/osd/PG.cc`
  - <https://github.com/ceph/ceph/blob/283b68e12a9847ca7ea7adb16d9a9b45af138ef3/ceph/osd/PG.cc>
- `ceph/osd/OSD.cc`
  - <https://github.com/ceph/ceph/blob/283b68e12a9847ca7ea7adb16d9a9b45af138ef3/ceph/osd/OSD.cc>
- `ceph/messages/MOSDOp.h`
  - <https://github.com/ceph/ceph/blob/283b68e12a9847ca7ea7adb16d9a9b45af138ef3/ceph/messages/MOSDOp.h>
- `ceph/messages/MOSDOpReply.h`
  - <https://github.com/ceph/ceph/blob/283b68e12a9847ca7ea7adb16d9a9b45af138ef3/ceph/messages/MOSDOpReply.h>

This is the same late-2006 endpoint already used by the bounded RG/RUSH → PG/CRUSH bridge. The present packet asks a different question: **what evidence controls retirement of recent PG history?**

It does not reconstruct the entire later evolution of `min_last_complete_ondisk`, `pg_committed_to`, modern BlueStore, or modern peering.

---

# Historical / source record

## 2. `last_complete` is already distinct from `last_update`

`PG::Info` in `PG.h` carries both:

```text
last_update    // last object version applied to store
last_complete  // last version pg was complete through
```

The accompanying source comment is stronger than the field names alone. It says that `last_complete` means the PG has all objects that existed as of that stamp, or a newer object, or a later delete has already been applied.

The same comment then links completeness to retained log history:

```text
if last_complete >= log.bottom,
then we know pg contents through log.top;
otherwise, we have no idea what the pg is supposed to contain.
```

This immediately rules out a one-dimensional model in which `last_update` alone is enough recovery evidence.

Historical relation:

```text
latest applied update
    != latest point through which local PG contents are complete
    != amount of recent history still needed to reason about PG contents
```

This packet does not claim that the 2006 definitions are byte-for-byte identical to later Ceph releases.

---

## 3. The PG log itself has a recoverability floor

The same `PG::Log` implementation defines:

```text
top     = newest update/delete entry
bottom  = version before the oldest update/delete for which complete negative information exists
```

The source comment states the consequence directly: PG contents can be inferred for a store whose `last_update >= bottom`.

The log is therefore not merely an audit trail. In this implementation, its retained lower boundary participates in the system's ability to interpret a participant's PG state.

That gives a source-level retention relation:

```text
recent history retained
    -> older / lagging replica state may remain interpretable

history below the required floor discarded from active log state
    -> that exact historical interval is no longer available from this log representation
```

The second line is deliberately narrow. It does not claim unrecoverability of the whole PG under every topology, because another participant or a backlog/content listing may still provide sufficient state.

---

## 4. The primary tracks a peer-bounded completion frontier

At this revision `PG` contains a primary-side field:

```text
peers_complete_thru
```

During peering, `PG.cc` initializes it from the primary's own `info.last_complete`, then walks peer information. For OSDs that are in the current acting set, a peer with a smaller `last_complete` lowers the frontier.

The source therefore constructs, at this point in the protocol, a minimum completion horizon across relevant acting participants rather than simply copying the primary's local completion point.

Historical/source relation:

```text
primary local last_complete
    != peers_complete_thru

peers_complete_thru
    = bounded by the least-complete acting participant observed by this logic
```

This is the crucial anti-collapse boundary for the present packet.

A locally complete primary does not automatically gain permission, merely from its own local state, to forget every older piece of PG history.

---

## 5. Replica commit replies carry PG-completion information back to the coordinator

The 2006 message format makes this frontier maintenance explicit on the wire.

`MOSDOpReply_st` contains:

```text
eversion_t pg_complete_thru;
```

with corresponding `get_pg_complete_thru()` / `set_pg_complete_thru()` methods.

In `OSD.cc`, replica-side commit handling constructs a commit reply and sets `pg_complete_thru` from the replica's supplied `last_complete` value before sending the reply to the coordinating OSD.

On the coordinating side, `repop_ack()` records the peer's `pg_complete_thru` when the reply is a commit reply.

This produces a concrete message-level distinction:

```text
replica acknowledged an operation
    != coordinator has received that replica's commit/completion report
```

and, more specifically for retention:

```text
one replica reports completion through V
    != all acting replicas report completion through V
```

The packet does not turn this field into a generic modern quorum theorem. It is evidence for this specific implementation endpoint.

---

## 6. `peers_complete_thru` advances only from gathered participant completion reports

When the replication gather object can be deleted — after its outstanding acknowledgement/commit sets have drained — `OSD::put_repop_gather()` examines the collected `pg_complete_thru` values.

The code starts with the primary's local `info.last_complete`, then takes the minimum across the acting OSDs' reported completion values. If that minimum is later than the existing `peers_complete_thru`, the primary advances the frontier.

A missing report is conservatively represented as zero in this calculation.

Historical/source relation:

```text
all required replication-gather completion information observed
    -> compute minimum completion frontier
    -> maybe advance peers_complete_thru
```

This means the frontier is intentionally conservative with respect to the slowest or not-yet-proven participant in the acting set.

It is therefore unsafe to rewrite the mechanism as:

```text
primary completed V
    -> history <= V can immediately be discarded everywhere
```

That is not what this source does.

---

## 7. The distributed completion frontier becomes an explicit trim instruction

The write/replication path carries the primary's current `peers_complete_thru` to replicas.

`MOSDOp_st` contains:

```text
eversion_t pg_trim_to;   // primary->replica: trim to here
```

and `OSD.cc` sets:

```text
wr->set_pg_trim_to(pg->peers_complete_thru);
```

The receiving path then passes the value through `prepare_log_transaction(..., op->get_pg_trim_to())` into `PG::append_log()`.

This directly connects two otherwise easy-to-confuse facts:

```text
what the acting set has proved complete through
    -> what history the primary authorizes a replica to trim through
```

The code does not derive `pg_trim_to` merely from the receiver's own local `last_complete`.

---

## 8. Trim is piggybacked on later log append work

`peers_complete_thru` advancing is not itself the same event as every replica's log being trimmed.

At this revision the primary attaches the current frontier to a replicated operation, and `PG::append_log()` performs trimming while appending a new log entry when:

```text
trim_to > log.bottom
```

The function then:

1. trims the in-memory indexed log;
2. updates `info.log_bottom` / backlog state;
3. calls `trim_ondisklog_to()`.

So the observed sequence is:

```text
participant completion evidence gathered
    -> peers_complete_thru advances
    -> later replicated op carries pg_trim_to
    -> receiver append path applies trim frontier
```

This supports another precise distinction:

```text
distributed retirement authority exists
    != every copy of the old log has already enacted retirement
```

The phrase `distributed retirement authority` is the repository's engineering reconstruction. Ceph's source vocabulary is `peers_complete_thru`, `pg_trim_to`, `log.bottom`, and `trim`.

---

## 9. The on-disk trim path advances a logical bottom; it does not immediately erase all older bytes

The low-level on-disk behavior is especially useful for technical-retention analysis.

`trim_ondisklog_to()` walks the on-disk block map to find a trim boundary, then advances:

```text
ondisklog.bottom
```

and persists the new `ondisklog_bottom` / `ondisklog_top` collection attributes.

In the inspected function, this path does **not** issue an immediate remove/truncate of all bytes before the new bottom.

`read_log()` later reads only:

```text
[ondisklog.bottom, ondisklog.top)
```

and separately ignores entries at or below the logical `log.bottom` unless backlog semantics require them.

Therefore, for this implementation path:

```text
history retired from active PG-log interpretation
    != historical bytes necessarily overwritten or physically absent immediately
```

This is a particularly important boundary. `Trimmed` here means that earlier history has fallen below the active logical read/interpretation floor. It is not evidence of secure deletion or immediate media reclamation.

A different path can later rewrite/remove the log object; this packet makes no claim that old bytes remain indefinitely.

---

## 10. Recovery itself advances local `last_complete`

`OSD.cc` also shows how local completeness can move independently from the acting-set trim frontier.

After an object being pulled during recovery is received, the code removes it from the local missing state and advances `info.last_complete` while the next logged objects are no longer missing. It persists the updated PG info in the object-store transaction.

That gives a concrete local sequence:

```text
missing object recovered locally
    -> missing entry removed
    -> local last_complete may advance
```

But the earlier sections show why this local transition must not be collapsed into global history retirement:

```text
local last_complete advances
    != peers_complete_thru necessarily advances immediately
    != pg_trim_to necessarily delivered immediately
    != remote log bottom necessarily advanced immediately
```

The maintenance state therefore has multiple horizons.

---

# Engineering reconstruction

## 11. History has its own retirement authority

The source supports a useful repository-level reconstruction:

```text
payload update applied
    != local completeness established
    != distributed completeness established
    != recovery history retireable
```

The retained PG log is not merely passive historical decoration. It is part of the evidence used to reconstruct what the PG should contain and to compare participants across peering/recovery boundaries.

Consequently, removing old log history is itself a maintenance decision that requires evidence.

For this packet, the repository names that evidence relation **history-retirement authority**.

That term means only:

> enough distributed completion information has accumulated, under the inspected protocol's rules, to authorize advancing the active PG-log floor.

It does not mean a cryptographic authority, operator permission, consensus certificate, or modern Ceph term.

---

## 12. Retained payload and retained repairability evidence have different lifetimes

The source now gives Case 05 a lifecycle that is more precise than `replicate data, then delete old logs`:

```text
object update
    -> per-OSD application / commit
    -> per-OSD completeness horizon
    -> acting-set minimum completion frontier
    -> trim authority piggybacked to participants
    -> active PG-log floor advances
    -> older bytes may remain physically present below that floor
```

This shows two different kinds of retained material:

```text
payload embodiments
recovery/currentness history
```

Their retirement conditions are not identical.

The PG can need recent history even after some payload copies already contain the corresponding state; conversely, bytes belonging to logically retired history can physically remain in the underlying log object for some time.

---

## 13. Completion evidence is monotonic here, but enactment is distributed and staged

`peers_complete_thru` only advances when a newer minimum is proved; the inspected code does not move it backwards through ordinary gather completion.

Yet enactment is staged:

```text
frontier known at primary
    -> frontier transmitted
    -> receiver processes later operation
    -> receiver advances logical trim state
```

So a monotonic control frontier does not imply one atomic cluster-wide retirement instant.

This is a useful general retention distinction:

```text
monotonic decision frontier
    != atomic distributed enactment
```

Again, this is an engineering reconstruction from the source path, not period Ceph terminology.

---

# Functional comparison only

## 14. Case 04 — mapped Flash currentness / old-embodiment retirement

Case 04 asks when an old physical Flash embodiment stops being current and when its space may later become reclaimable.

Case 05 here asks when old distributed **history** stops being needed for the active recovery representation.

The functional resemblance is:

```text
replacement/current state exists
    != old supporting representation may immediately be retired
```

But the mechanisms are entirely different:

- Case 04 concerns controller-local logical-to-physical mapping, relocation, erase, and reuse;
- Case 05 concerns distributed PG completion state and recovery-history trimming.

No historical lineage is claimed.

---

## 15. Case 25 — Swift handoff cleanup

Case 25 separates successful remote synchronization from permission to remove a local handoff copy.

This Case 05 slice similarly separates local/individual completion from permission to retire older shared recovery history.

The functional family resemblance is:

```text
some replacement/current state established
    != retirement authority for old state is automatic
```

But Swift's handoff cleanup and Ceph's PG-log trimming are not the same algorithm, state machine, quorum rule, or historical family.

---

## 16. Case 78 — replicated BBT metadata convergence

Case 78 shows serial publication of primary and mirror bad-block tables, so one metadata copy becoming current does not imply the other copy has converged.

Case 05 shows a different distributed asymmetry:

```text
primary knows a newer safe trim frontier
    != all participants have already enacted that trim
```

The comparison is functional only. NAND BBT replication is not an ancestor of RADOS PG logs and vice versa.

---

# Philosophical interpretation — deliberately downstream

The mechanism can support a later interpretation that **retention sometimes includes retaining the evidence needed to justify forgetting**.

That is:

```text
history exists
    -> system can reason about divergent / incomplete state

sufficient completion evidence accumulates
    -> some history becomes retireable
```

But the philosophical phrasing is not needed to establish the engineering claim. The source-level result is simply that the 2006 implementation computes a peer-bounded completion frontier and uses it to control PG-log trimming.

---

## 17. Explicit non-claims

This packet does **not** claim that:

1. `peers_complete_thru` is identical to modern `min_last_complete_ondisk` or `pg_committed_to`;
2. modern Ceph uses the exact same message fields or trimming path;
3. the December-2006 endpoint is production-grade or representative of every deployed Ceph cluster;
4. `last_complete` means the same thing in every Ceph release;
5. the acting-set minimum is a generic quorum theorem;
6. every historical participant must be complete before any log retirement can occur;
7. `peers_complete_thru` is a consensus certificate;
8. receipt of a normal ACK is the same as receipt of the commit/completion report;
9. one peer's `pg_complete_thru` is enough to advance the acting-set frontier;
10. advancing `peers_complete_thru` instantly trims every replica;
11. transmitting `pg_trim_to` proves the receiver durably enacted it;
12. `append_log()` trimming is one atomic cluster-wide transaction;
13. logical trim means secure deletion;
14. old bytes below `ondisklog.bottom` remain forever;
15. bytes below `ondisklog.bottom` are guaranteed recoverable by ordinary Ceph restart logic;
16. physical persistence of retired bytes makes them current or admissible;
17. PG-log retention alone can recover payload if all necessary object bytes are gone;
18. a backlog/content listing has the same semantics as the incremental log;
19. this packet reconstructs the full RUSH→CRUSH or RG→PG genealogy;
20. the exact later evolution of PG-log trimming belongs in this case rather than `computing-archaeology`;
21. EBOFS transaction callbacks prove arbitrary power-cut durability below every controller/cache layer;
22. a source-level commit callback is equivalent to a measured fault-injection trace;
23. Case 04, Case 25, or Case 78 historically influenced this Ceph mechanism;
24. the project terms `history-retirement authority` or `distributed completion frontier` were used by Ceph developers in 2006.

---

## 18. Evidence-strength assessment

### Strongly established by primary source

- the exact 2006 source distinguishes `last_update` and `last_complete`;
- PG-log `bottom` participates in what state can be inferred from a participant;
- a primary tracks `peers_complete_thru`;
- acting peers' `last_complete` values bound that frontier during peering;
- replica commit replies carry `pg_complete_thru`;
- the replication gather computes a minimum completion point across the acting set before advancing `peers_complete_thru`;
- replicated operations carry `pg_trim_to` from primary to replica;
- `append_log()` uses the trim value to advance in-memory and on-disk log bounds;
- `trim_ondisklog_to()` advances the on-disk logical bottom without immediately deleting/truncating all earlier bytes in that function;
- restart log reading begins at the persisted `ondisklog.bottom`.

### Engineering reconstruction

- `peers_complete_thru` is a distributed completion frontier for this bounded analysis;
- the frontier constitutes a form of history-retirement authority;
- log retirement is staged rather than one atomic cluster-wide event;
- logical retirement and physical byte erasure are separate persistence horizons.

### Still open

The highest-value next steps are narrower than another general Ceph history pass:

1. **fault trace:** interrupt/restart around a transaction that both appends a log record and advances the trim floor, then observe the persisted `info.log_bottom` / `ondisklog_bottom` and restart reconstruction;
2. **distributed lag trace:** hold one acting peer's completion frontier back, verify the primary's trim frontier does not cross it, then let the peer catch up and observe the later trim enactment;
3. **physical-retirement boundary:** determine under the inspected EBOFS implementation when bytes below `ondisklog.bottom` are eventually overwritten/reclaimed, without confusing that storage detail with PG logical retirement;
4. **later terminology genealogy:** trace `peers_complete_thru` → later completion/commit frontier names only in `computing-archaeology` unless the evolution exposes a new retention-specific semantic boundary.

None of these is required to promote the parent case; **Case 05 remains `grounded`**.

---

## 19. Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `peers_complete_thru` and `Ceph PG log trim` found no dedicated packet to reuse.

Accordingly, this file keeps only the retention-specific seam needed here: **peer-bounded completion evidence before PG-history retirement**. Broader source genealogy and the later evolution of Ceph completion-frontier terminology should be developed in `computing-archaeology` if needed, then linked back rather than duplicated.
