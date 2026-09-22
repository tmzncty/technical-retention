# Case 81 evidence index — Chain Replication currentness, durability, and configuration authority

## Status

**Case 81: `grounded`.**

This index separates four evidence layers that should not be collapsed into one generic claim that “chain replication retains data.”

```text
service-ordering / in-process obligation
    !=
per-brick persistence frontier
    !=
configuration authority / bootstrap state
    !=
quorum-admissible Admin state / repair / retained history
```

The packets below are complementary. None should be used to silently strengthen another layer's contract.

---

## 1. 2004 protocol grounding

[`81-chain-replication-2004-grounding.md`](81-chain-replication-2004-grounding.md)

**Bounded question:** what remains between head receipt and tail-qualified completion, and how is unfinished work preserved across chain repair or tail extension?

**Established:**

- head/tail role asymmetry;
- `Hist` / `Pending` service model;
- per-server `Sent_i` lists;
- backwards `ack(r)` retirement;
- missing-suffix transfer after internal failure;
- state transfer plus concurrent catch-up before new-tail admission;
- explicit primary/backup and state-machine-replication prior-art boundary;
- proof-history representation is not an implementation requirement to store complete history.

**Does not establish:** disk/media durability, exact master-state persistence, production deployment behavior, partition/Byzantine safety, or a universal physical persistence meaning for tail acknowledgement.

---

## 2. 2010 Hibari local WAL durability frontier

[`81-hibari-2010-wal-durability-frontier-deepening.md`](81-hibari-2010-wal-durability-frontier-deepening.md)

**Bounded question:** what additional state appears when a concrete chain-replication implementation composes protocol ordering with WAL, group commit, `fsync(2)`, and serial-number progress?

**Established:**

- default Hibari persistence policy in the 2010 implementation report;
- local WAL/group-commit path;
- “largest serial safely flushed to disk” as a per-brick prefix frontier;
- downstream propagation gating in the described implementation;
- historically reported wrong-order / wrong-safe-serial bugs and associated data loss;
- documented weaker asynchronous/non-durable modes.

**Does not establish:** that every chain-replication implementation uses `fsync`, that every Hibari deployment used the durable default, or that OS-level `fsync` proves persistence through every possible hardware fault model.

---

## 3. 2004–2010 configuration authority and bootstrap

[`81-2004-2010-configuration-authority-bootstrap-deepening.md`](81-2004-2010-configuration-authority-bootstrap-deepening.md)

**Bounded question:** what retains the authority that says which chain exists and which replica may act as head/tail after management-process failure or reconfiguration?

**Established:**

- the 2004 `master` detects failures and publishes predecessor/successor plus head/tail changes;
- the protocol exposition assumes a non-failing master, while the prototype note says the master was Paxos-replicated;
- Hibari's active/standby Admin Server process is distinct from retained Admin private state;
- Hibari distributes Admin private/history state across cluster bricks;
- Hibari avoids chain-replicating that private state because doing so creates a bootstrap circularity;
- a quorum-voting style mechanism is used instead for the Admin private state;
- private-state update traffic can itself bottleneck large startup/reconfiguration waves;
- retained control state does not make failure/partition observations perfectly true.

**Does not establish:** exact Paxos stable-state layout in the 2004 prototype, exact Hibari quorum write/read/persistence semantics, an atomic all-participant configuration-publication point, or total-cluster-restart behavior.

---

## 4. 2010 Hibari simple-quorum source semantics, read repair, and retained history

[`81-hibari-2010-simple-quorum-read-repair-bootstrap-state-deepening.md`](81-hibari-2010-simple-quorum-read-repair-bootstrap-state-deepening.md)

**Bounded question:** what does the late-2010 Hibari source actually do when Admin-state copies disagree, and what survives an Admin/scoreboard process restart?

**Established from the dated 29-Dec-2010 source tree:**

- `brick_squorum` is explicitly intended as persistent storage for cluster-manager/Admin data, separate from normal chain bootstrap;
- the source uses a statically configured bootstrap-brick list to break the circular dependency between needing cluster configuration and needing a running configured cluster to read that configuration;
- the simple-quorum module explicitly provides no transaction support and assumes another mechanism prevents multiple managers from running, so quorum-retained state is not itself manager election/fencing;
- a set may be accepted when a quorum agrees even though one or more bootstrap bricks are nonconforming, so quorum success does not imply full replica convergence;
- a get with quorum-supported disagreement repairs one nonconforming brick using conditional `testset` operations, then re-submits/re-evaluates the read;
- a minority value with a locally newer timestamp can be treated as an interrupted update rather than automatically authoritative, so timestamp order alone is not the currentness rule;
- the two-brick case has an explicit presence-preserving rule when one brick reports a value and the other reports absence;
- the scoreboard warns that polled health/status can be slightly out of sync with reality;
- the scoreboard can advance its in-memory state even if quorum persistence of the corresponding history fails, explicitly separating runtime management knowledge from retained history;
- on startup, scoreboard history is reloaded from the bootstrap-data path into runtime memory;
- the 29-Dec-2010 Admin type-spec change directly identifies `schema_definition` and client-monitor state as actual `brick_squorum` clients;
- a 24-Mar-2015 source change later moved squorum set/multiset timestamp assignment client-side because the Admin simple-quorum scheme did not work with server-side timestamps, proving that current source semantics must not be silently back-projected into the 2010 code line.

**Critical boundaries:**

```text
quorum success
    !=
all copies converged
```

```text
runtime scoreboard state
    !=
retained scoreboard history
    !=
current failure truth
```

```text
quorum-replicated Admin state
    !=
transaction support
    !=
manager election / fencing
```

```text
same module name across revisions
    !=
same currentness / timestamp implementation
```

**Does not establish:** exact lower-level stable-media semantics for bootstrap writes, total-cluster restart with all bootstrap bricks initially down, an atomic global configuration-publication point, the separate single-manager/fencing mechanism, or the 2004 prototype master's Paxos stable-state format.

---

## State taxonomy

Keep at least these Case 81 state classes separate:

| State | Purpose | Retirement / advancement evidence |
| --- | --- | --- |
| object payload | useful service state | application/protocol update path |
| tail-qualified completed state | service-level currentness | tail processing in 2004 model |
| `Pending` relation | specification-level unfinished work | tail processing |
| `Sent_i` | forwarded but not-yet-known-complete obligation | backwards acknowledgement |
| local WAL safe serial | per-brick persistence prefix in Hibari | WAL/group-commit flush report |
| chain topology / roles | head, tail, predecessor, successor authority | master/Admin reconfiguration |
| static bootstrap-brick hint | where Admin state can initially be sought | local/bootstrap configuration |
| quorum-admissible Admin value | retained schema/history/control value usable under simple-quorum rule | matching-answer quorum |
| nonconforming Admin copy | divergence / repair debt | later read repair or separate repair path |
| Admin private/history state | retained management knowledge across Admin-process loss | separately replicated management state |
| in-memory scoreboard status | recent runtime health/management knowledge | polling/report path |
| retained scoreboard history | restart-reconstructable management history | simple-quorum persistence path |
| failure observation | evidence/suspicion used to trigger reconfiguration | monitoring / partition logic |
| client/server configuration knowledge | which published topology a participant is acting on | dissemination / refresh, exact atomicity still open |

This gives the case a more precise currentness stack:

```text
payload exists somewhere
    !=
update reached local stable-storage frontier
    !=
update is tail-qualified complete
    !=
client learned completion

and orthogonally:

configuration exists somewhere
    !=
configuration is quorum-admissible
    !=
all bootstrap copies converged
    !=
configuration authority is fenced
    !=
all participants learned the same configuration

and separately:

health event observed
    !=
runtime scoreboard updated
    !=
history durably retained
    !=
history still describes present reality
```

---

## Prior-art / vocabulary guardrails

Historical vocabulary from the sources includes `chain`, `head`, `tail`, `master`, `Sent_i`, `ack(r)`, `Paxos`, `Admin Server`, WAL, `fsync`, serial number, quorum voting, `brick_squorum`, scoreboard, schema definition, and bootstrap bricks.

Project engineering terms such as `tail-qualified currentness`, `forwarding obligation`, `configuration authority`, `bootstrap dependency cut`, `local durability frontier`, `quorum-admissible Admin value`, `retained management history`, and `configuration publication` are analytical labels, not quotations from the historical actors.

Do not infer invention priority for:

- primary/backup replication;
- state-machine replication;
- Paxos;
- configuration services;
- failure detection;
- write-ahead logging;
- group commit;
- quorum replication;
- read repair;
- fencing or epochs.

The repository claim is narrower: these sources expose different retained relations inside specific 2004 and 2010 chain-replication/Hibari regimes.

---

## Cross-case comparison map — functional only

- **Case 05, Ceph RADOS repair:** placement/version/peering authority rather than fixed head-to-tail ordering.
- **Case 23, Dynamo:** membership and divergent-version reconciliation under a different consistency/failure model.
- **Case 50, HDFS QJM epoch fencing:** retained authority/fencing state with different quorum and role semantics.
- **Case 56, Kafka high watermark:** replication/visibility frontier, distinct from Hibari's per-brick persistence frontier.
- **Case 68, Dynamo membership/failure boundary:** replica presence versus membership/failure knowledge.
- **Synthesis 23, retention interpreter/access apparatus:** useful only as a functional comparison for the distinction between retained control payload and retained ability to locate/admit it.

These are comparisons of retained-state roles, not genealogical claims.

---

## Related-repository routing

Fresh exact-topic code search in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Hibari` and `Hibari brick_squorum` did not surface a dedicated reusable packet during the source-level Admin-state slice.

Keep `technical-retention` focused on:

- service currentness versus local persistence frontier;
- configuration authority and bootstrap dependencies;
- quorum admissibility versus replica convergence;
- retained Admin history versus volatile runtime management state;
- restart reconstruction and control-state currentness;
- version-bounded semantics when source changes alter currentness rules.

Prefer `computing-archaeology` for broad Gemini/Hibari organizational history, Erlang deployment history, `gdss_*` component genealogy, general Chain Replication descendants, and performance archaeology not needed to establish a retention boundary.

---

## Current evidence debt

The highest-value remaining Case 81 work is now narrower than before:

1. obtain source-level evidence for the 2004 prototype master's Paxos state, persistence boundary, and configuration-version/fencing semantics;
2. trace the 2010 Hibari bootstrap-write path into `brick_server` / WAL far enough to establish the lower stable-storage boundary of Admin-state quorum acknowledgement;
3. inspect the **2010** bootstrap hint-file lifecycle and its repair/update semantics when the schema-brick list changes;
4. reconstruct total-cluster restart with all bootstrap bricks initially stopped and then progressively restored;
5. identify the separate single-manager / fencing mechanism assumed by `brick_squorum` and determine what retained epoch/authority state, if any, it uses;
6. fault-inject configuration changes between quorum-accepted control-state update, brick-role change, and client routing publication;
7. test suffix repair and tail extension under process crash/restart rather than only reason from the protocol paper;
8. keep later CRAQ/self-reconfiguring descendants separate unless a future slice explicitly studies them.

No maturity promotion follows from the new source packet alone. **Case 81 remains `grounded`.**