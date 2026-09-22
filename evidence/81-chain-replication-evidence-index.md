# Case 81 evidence index — Chain Replication currentness, durability, and configuration authority

## Status

**Case 81: `grounded`.**

This index separates three evidence layers that should not be collapsed into one generic claim that “chain replication retains data.”

```text
service-ordering / in-process obligation
    !=
per-brick persistence frontier
    !=
configuration authority / bootstrap state
```

The three packets below are complementary. None should be used to silently strengthen another layer's contract.

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
| Admin private/history state | retain management knowledge across Admin-process loss | separately replicated management state |
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

replica exists
    !=
replica belongs to current chain
    !=
replica has current role authority
    !=
all participants have learned the same configuration
```

---

## Prior-art / vocabulary guardrails

Historical vocabulary from the sources includes `chain`, `head`, `tail`, `master`, `Sent_i`, `ack(r)`, `Paxos`, `Admin Server`, WAL, `fsync`, serial number, and quorum voting.

Project engineering terms such as `tail-qualified currentness`, `forwarding obligation`, `configuration authority`, `bootstrap dependency cut`, `local durability frontier`, and `configuration publication` are analytical labels, not quotations from the historical actors.

Do not infer invention priority for:

- primary/backup replication;
- state-machine replication;
- Paxos;
- configuration services;
- failure detection;
- write-ahead logging;
- group commit;
- quorum replication;
- fencing or epochs.

The repository claim is narrower: these sources expose different retained relations inside specific 2004 and 2010 chain-replication regimes.

---

## Cross-case comparison map — functional only

- **Case 05, Ceph RADOS repair:** placement/version/peering authority rather than fixed head-to-tail ordering.
- **Case 23, Dynamo:** membership and divergent-version reconciliation under a different consistency/failure model.
- **Case 50, HDFS QJM epoch fencing:** retained authority/fencing state with different quorum and role semantics.
- **Case 56, Kafka high watermark:** replication/visibility frontier, distinct from Hibari's per-brick persistence frontier.
- **Case 68, Dynamo membership/failure boundary:** replica presence versus membership/failure knowledge.

These are comparisons of retained-state roles, not genealogical claims.

---

## Current evidence debt

The highest-value remaining Case 81 work is now narrower than before:

1. obtain source-level evidence for the 2004 prototype master's Paxos state, persistence boundary, and configuration-version/fencing semantics;
2. inspect Hibari source for Admin private-state quorum reads/writes, stable-storage boundary, retry/repair, and total-restart bootstrap;
3. fault-inject configuration changes between durable control-state update, brick-role change, and client routing publication;
4. test suffix repair and tail extension under process crash/restart rather than only reason from the protocol paper;
5. keep later CRAQ/self-reconfiguring descendants separate unless a future slice explicitly studies them.

No maturity promotion follows from the new configuration packet alone. **Case 81 remains `grounded`.**
