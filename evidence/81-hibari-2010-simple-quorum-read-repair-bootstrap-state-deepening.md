# Case 81 deepening — Hibari 2010 simple-quorum Admin state, read repair, and bootstrap retention

## Scope

This packet narrows one open Case 81 question:

> What did Hibari's source actually retain for the Admin Server, how did the `brick_squorum` path decide that a value was usable, and what did a successful quorum operation *not* prove?

The slice is deliberately bounded to source-visible control-state retention around the late-2010 Hibari code line. It does **not** attempt a general history of Hibari, Chain Replication, quorum systems, or Erlang storage.

The core source snapshot inspected here is `hibari/gdss-admin` at commit `5b3485ee0d8cda08fe10cddad940e6da52ec3de3`, committed 29 December 2010. That commit itself is a small type-spec clarification, but it gives a dated source tree in which the Admin Server's simple-quorum path can be inspected directly.

Primary source anchors:

- [`brick_squorum.erl` at the 2010-12-29 snapshot](https://github.com/hibari/gdss-admin/blob/5b3485ee0d8cda08fe10cddad940e6da52ec3de3/src/brick_squorum.erl)
- [`brick_sb.erl` at the same snapshot](https://github.com/hibari/gdss-admin/blob/5b3485ee0d8cda08fe10cddad940e6da52ec3de3/src/brick_sb.erl)
- [`brick_admin.erl` at the same snapshot](https://github.com/hibari/gdss-admin/blob/5b3485ee0d8cda08fe10cddad940e6da52ec3de3/src/brick_admin.erl)
- [2010-12-29 commit `5b3485ee`](https://github.com/hibari/gdss-admin/commit/5b3485ee0d8cda08fe10cddad940e6da52ec3de3)
- [2015-03-24 timestamp correction `a8fc2ed9`](https://github.com/hibari/gdss-admin/commit/a8fc2ed9bc2d358e3b3e1299d42a1e608488662d), used only to bound later implementation drift

The broader 2010 Hibari paper already established that Admin private state was distributed across bricks with a quorum-voting-style mechanism rather than stored through the ordinary data chains. This packet does not repeat that paper-level history. It inspects the implementation boundary that the paper leaves abstract.

---

## Claim-type legend

- **Historical record** — directly established by the dated source tree or commit history.
- **Engineering reconstruction** — a bounded consequence of those mechanisms; not historical actor vocabulary unless explicitly quoted.
- **Functional analogy** — comparison to another retention regime; never evidence of genealogy.
- **Philosophical interpretation** — conceptual reading applied after the mechanism is fixed.

No experiment is reported in this packet.

---

## 1. Historical record — the Admin state has a separate bootstrap storage path

The module-level documentation in `brick_squorum.erl` states its purpose unusually clearly.

It is a client for **simple quorum redundancy** intended to provide persistent data for a cluster Admin/manager server. The source rejects keeping that data only on the Admin machine's local disk and instead spreads it over multiple bricks.

The source also names the bootstrap problem directly: if the cluster must already be running in order to serve the manager state, how can the manager obtain the state needed to start the cluster?

Its implementation answer is a statically configured list of bricks used for cluster-manager data, with a simple quorum technique over that list.

This establishes a concrete retention split:

```text
ordinary user-data chain
    !=
Admin / cluster-manager retained state

normal chain discovery
    !=
statically known bootstrap-brick contact set
```

The static contact set is not itself the full cluster schema. It is the path by which the manager reaches the separately retained state needed to reconstruct administrative knowledge.

### Boundary

This is stronger than saying only that Hibari “used quorum voting.” The source shows *why* this path is outside ordinary Chain Replication: its purpose is to break the startup dependency between knowing cluster configuration and needing the configured cluster to read that configuration.

It does **not** prove that every bootstrap scenario succeeds. Availability still depends on enough configured bootstrap bricks being reachable and useful.

---

## 2. Historical record — quorum replication is not a manager-election or fencing protocol

The same module says it provides **no transaction support** and assumes some other mechanism prevents multiple managers from running simultaneously.

That gives a strict boundary:

```text
quorum-replicated Admin state
    !=
transaction protocol
    !=
manager-election protocol
    !=
fencing / epoch protocol
```

The simple-quorum store retains values and resolves replica disagreement. It is not, by itself, the authority that proves only one Admin process may act.

This matters for Case 81 because “configuration state survives” and “only the right configuration authority can act” are distinct retention questions.

A later slice may recover the separate single-manager / fencing mechanism. This packet does not infer it from `brick_squorum`.

---

## 3. Historical record — a successful set does not imply all bootstrap copies agree

`strict_quorum_answer_set/3` counts matching replies and computes the minimum quorum. If there are nonconforming bricks but the popular answer still reaches quorum, the function accepts that answer.

The source comment is explicit that some other actor will have to repair those nonconforming bricks.

Therefore, in this implementation:

```text
set accepted by quorum
    !=
all bootstrap bricks contain the same state
    !=
replica convergence complete
```

This is a useful Case 81 counterexample to treating “replicated” as a single boolean property.

The retained relation after a successful operation can be:

```text
quorum-admissible value
+ known or latent divergent copies
+ future repair obligation
```

### Engineering reconstruction

The implementation therefore separates at least three control-state conditions:

1. a value exists on one or more bricks;
2. a value has enough agreement to be accepted by the quorum rule;
3. every configured copy has converged.

Only the second is necessary for this set path to return the accepted answer.

---

## 4. Historical record — reads can perform repair and then resubmit

`strict_quorum_answer_get/3` has a stronger convergence role than the successful-set path.

When a quorum supports one answer but another brick disagrees, the code repairs **one nonconforming brick**, then returns `re_submit`; the outer path may retry the operation repeatedly.

The repair uses `testset` conditions so that a repair does not blindly overwrite a value changed concurrently after the stale response was observed.

The source distinguishes at least these disagreement forms:

- a nonconforming brick is missing a key that the quorum says exists;
- a nonconforming brick has an older timestamp/value;
- a minority brick has a newer timestamp than the quorum-supported value, which the source comment treats as a possible interrupted update;
- the quorum says the key should be absent while a minority still has a value.

The implementation then repairs toward the quorum-supported answer.

Thus:

```text
quorum-readable currentness
    !=
all copies already current

read admitted
    -> may create repair work
    -> retry / re-evaluate
    -> later convergence
```

### Important non-claim

This is not evidence for a universal “largest timestamp wins” rule. In the inspected 2010 path, a minority value with a newer timestamp can be treated as an interrupted update and replaced by the quorum-supported value.

So:

```text
larger local timestamp
    !=
automatically authoritative current state
```

The authority relation is quorum-shaped in this code path, not reducible to timestamp order alone.

---

## 5. Historical record — the two-brick case has an explicit anti-deletion bias

`popular_answer/2` contains a special rule for exactly two responding copies.

If one says `key_not_exist` and the other returns an existing value, the source chooses the existing value as the preferred answer. Its comment states the intended effect directly: with a two-brick quorum, if only one brick has key X, replicate X rather than delete it from the other brick.

This gives a particularly clear retention bias:

```text
one present copy + one absence
    -> prefer preserving / replicating the present value
```

within that bounded two-copy case.

### Boundary

This is an implementation policy for this simple-quorum store. It is not a general theorem that “presence is always more authoritative than absence,” and it should not be projected onto ordinary Hibari chain state, tombstone semantics in other systems, or quorum systems generally.

---

## 6. Historical record — the scoreboard separates runtime status from retained history

`brick_sb.erl` is equally important because it exposes a different state split.

The source describes the scoreboard as a snapshot of brick and chain health in the very recent past. It warns that the information can be somewhat out of sync with reality because it is fed by polling entities such as brick pingers and chain monitors.

Therefore:

```text
recorded / remembered health evidence
    !=
perfectly current failure truth
```

This is a first-order source warning, not merely a modern distributed-systems reconstruction.

---

## 7. Historical record — runtime state can advance even when history persistence fails

The scoreboard's status-report path first computes `NewState` in memory and then tries to write the corresponding history operations through `squorum_multiset`.

The code's TODO is unusually candid: if there is a quorum error, losing history is not immediately fatal, though it “can be bad.” On failure the code logs an error and still returns with `NewState` as the process state.

That means the 2010 source itself supports:

```text
runtime scoreboard state advanced
    !=
history durably retained through the quorum path
```

and:

```text
current service-management knowledge
    !=
complete retained audit / recovery history
```

This is a useful retention failure mode because it is neither simple payload loss nor total service failure. The system can continue with more recent volatile management knowledge while losing part of the history that would otherwise survive the Admin process.

### Engineering reconstruction

Case 81 should therefore not model Admin knowledge as one undifferentiated state variable.

At minimum:

```text
observed health/status now
    ↓
in-memory scoreboard state

separate path:

history event
    ↓
quorum write admission
    ↓
retained bootstrap history
    ↓
future Admin-process reconstruction
```

A failure can interrupt the second path without immediately invalidating the first.

---

## 8. Historical record — process restart reconstructs history from bootstrap storage

During initialization, the scoreboard waits for `brick_admin`, then loads its historical data from the bootstrap-data path and reconstructs the in-memory history dictionary.

The source therefore directly supports a bounded restart claim:

```text
scoreboard process memory lost
    + bootstrap state still quorum-readable
    -> history can be reconstructed into process memory
```

This is stronger than merely saying the Admin Server has a standby process. The historical record identifies a reconstruction path from retained data.

### What it still does not establish

It does not prove:

- restart when no bootstrap quorum is reachable;
- complete-cluster restart from all nodes simultaneously down;
- the lower storage stack's exact `fsync` / controller / media persistence boundary;
- atomic reconstruction of every Admin subsystem at one common configuration epoch;
- that reconstructed health history is still a correct description of present physical health.

Thus:

```text
restart-readable retained history
    !=
total-cluster bootstrap proof
    !=
current failure truth
```

---

## 9. Historical record — configuration values are actual simple-quorum clients

The dated 29 December 2010 commit is useful beyond merely dating the source tree. Its type-spec change explicitly narrows the Admin wrappers around `brick_squorum:get()` / `set()` to real administrative values including `schema_definition` and the client-monitor list.

This is implementation-level evidence that the simple-quorum module is not an unused helper or an abstract paper mechanism. The Admin code is wired to it for configuration-bearing state.

That yields:

```text
bootstrap quorum mechanism exists
    + Admin wrappers use it for schema/control values
    -> source-level control-state retention path
```

without claiming that every configuration field or every later Hibari release used exactly the same representation.

---

## 10. Historical record — later timestamp repair shows why source revision matters

A 24 March 2015 commit changes `brick_squorum:set/6` and `multiset/2` to assign a client-side timestamp before issuing operations to the bricks.

The commit message says why: the simple-quorum scheme used by the Admin Server “doesn't work with server-side timestamp.”

This is not a minor provenance detail. It means that the current `dev` implementation cannot be silently projected backward onto the 2010 source snapshot.

The evidence boundary is:

```text
same module name
    !=
same conflict-resolution implementation across revisions
```

and:

```text
2015 fix documents a later problem/change
    !=
proof that the 2010 deployment experienced a particular failure
```

For Case 81, source revision is itself part of the retention contract whenever claims depend on timestamp assignment or disagreement repair.

---

## 11. State taxonomy after this deepening

The combined Case 81 state stack can now distinguish at least:

| State / relation | Role | Retention / advancement boundary |
| --- | --- | --- |
| object payload | useful service state | ordinary chain protocol |
| `Sent_i` / pending forwarding obligation | unfinished protocol work | backwards acknowledgement |
| local WAL safe serial | Hibari brick persistence prefix | local flush/group-commit evidence |
| chain topology / roles | configuration authority | Admin/master reconfiguration |
| static bootstrap-brick hint | where Admin state can initially be sought | local/bootstrap configuration |
| quorum-admissible Admin value | usable retained configuration/history value | simple-quorum agreement rule |
| nonconforming Admin copy | divergence / repair debt | later read repair or other repair |
| in-memory scoreboard status | recent runtime management knowledge | polling/report path |
| retained scoreboard history | restart-reconstructable management history | quorum write path |
| current failure truth | actual present condition | not guaranteed by retained history alone |

The central new distinction is:

```text
configuration present somewhere
    !=
configuration quorum-admissible
    !=
all configuration copies converged
    !=
configuration authority fenced
    !=
all participants have learned the configuration
```

---

## 12. Engineering reconstruction — bootstrap retention has two different dependencies

The source permits a bounded two-stage reconstruction:

```text
A. bootstrap locator state
   "which bricks should I ask?"

B. replicated administrative state
   "what schema/history/configuration do those bricks support?"
```

The point is not that these are philosophically two memories. The engineering point is simpler: retaining B is useless at restart if the system has lost every usable route to the bricks that hold B.

So Case 81 gains another anti-collapse rule:

```text
retained control payload
    !=
retained ability to locate / admit that payload
```

This is structurally similar to other interpreter/access-apparatus cases in the repository, but no historical genealogy is asserted.

---

## 13. Functional analogy — bounded only

A useful functional comparison is the repository's existing distinction between payload retention and retained access apparatus.

Hibari's bootstrap hint plus quorum-replicated schema can be compared functionally to systems where a root pointer, checkpoint selector, map epoch, or configuration service is needed before retained lower-level state becomes operationally usable.

The comparison stops at that role.

It does **not** imply that Hibari's simple quorum is historically derived from filesystem superblocks, Ceph OSDMaps, HDFS QJM epochs, ZooKeeper zxids, or any other case.

---

## 14. Philosophical interpretation — a narrow retention point

The source makes one conceptual point worth preserving without enlarging it into a general theory:

> Control state can survive as data while still depending on a retained route, an admissibility relation, and later reconstruction before it again functions as authority.

That is a project interpretation, not Hibari's historical vocabulary.

The mechanism constrains the interpretation: the stored administrative record is not automatically identical to live authority, live observation, or converged configuration.

---

## 15. Explicit non-claims

This packet does **not** establish any of the following:

1. the 2004 Chain Replication prototype master's exact Paxos stable-state format;
2. a Paxos genealogy for Hibari's `brick_squorum` implementation;
3. that simple quorum itself performs manager election or fencing;
4. transactional atomicity across all Admin keys;
5. an atomic global configuration-publication point;
6. that every successful quorum write synchronously repairs every bootstrap brick;
7. that a quorum-readable configuration means every client/server already acts on it;
8. that a retained health-history record is current failure truth;
9. that scoreboard in-memory progress always has a retained history counterpart;
10. total-cluster restart with every process and brick initially down;
11. the exact stable-media boundary under each bootstrap brick write;
12. immunity to power loss, torn lower-layer writes, or storage-controller cache loss;
13. that a larger timestamp is universally more authoritative than quorum agreement;
14. that current `dev` source has exactly the same timestamp semantics as the 2010 source;
15. that the 2015 timestamp change proves a specific 2010 production incident;
16. that two-copy presence preference is a universal quorum-storage rule;
17. Byzantine-fault tolerance;
18. that all Admin private state uses one identical durability contract;
19. production deployment frequency or topology;
20. a universal philosophical claim that retained state always requires a separate bootstrap locator.

---

## 16. Evidence-strength update

### Newly closed or narrowed

- **Admin private-state quorum mechanics:** moved from paper-level description to dated source-level set/get disagreement behavior.
- **Repair semantics:** source now directly shows quorum-supported read repair and retry.
- **Write-completion boundary:** source shows quorum acceptance can precede full copy convergence.
- **Runtime-versus-history boundary:** scoreboard can advance while quorum history persistence fails.
- **Process-restart reconstruction:** source loads historical data from bootstrap storage into runtime state.
- **Bootstrap circularity:** source comments directly explain the static bootstrap-brick list as the mechanism used to break it.
- **Revision provenance:** 2015 timestamp repair prevents back-projecting current source semantics into 2010.

### Still open

The highest-value remaining work is now narrower:

1. trace the lower `brick_server` / WAL path used by bootstrap writes far enough to establish the exact stable-storage boundary of Admin-state quorum acknowledgement in the 2010 code line;
2. inspect the bootstrap hint-file lifecycle in the 2010 source specifically, including how it is repaired when the schema-brick list changes;
3. reconstruct total-cluster-restart behavior with all bootstrap bricks initially stopped, then progressively restored;
4. identify the separate mechanism that prevents multiple Admin managers from acting and determine whether it carries an epoch/fencing state;
5. fault-inject a schema/configuration change between quorum acceptance, role reconfiguration, and client routing publication;
6. keep the 2004 prototype master's Paxos state as a separate evidence debt rather than merging it with Hibari's simple quorum.

No maturity promotion follows from this packet. **Case 81 remains `grounded`.**

---

## 17. Related-repository routing

Fresh code search in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Hibari` and `Hibari brick_squorum` did not surface a dedicated reusable packet during this slice.

Keep in `technical-retention`:

- Admin-state persistence/currentness distinctions;
- bootstrap-locator versus retained-control-state boundaries;
- quorum admissibility versus copy convergence;
- restart reconstruction;
- runtime observation versus retained history;
- version-bounded semantics when source changes alter currentness rules.

Prefer `computing-archaeology` for any future broad work on:

- Gemini / Hibari product and organizational history;
- Erlang/OTP deployment history;
- general Chain Replication descendants;
- detailed `gdss_*` component genealogy;
- performance/benchmark archaeology not needed to answer a retention question.

---

## Result

The important result is not merely that Hibari replicated its Admin state.

The 2010 source exposes a layered retention contract:

```text
static bootstrap contact knowledge
    ↓
quorum-readable Admin state
    ↓
possible divergent-copy repair
    ↓
runtime reconstruction
    ↓
separate configuration / health action
```

with two explicit negative results:

```text
quorum success
    !=
all copies converged
```

and:

```text
retained management history
    !=
current management truth
    !=
fenced configuration authority
```

That makes Hibari a useful Case 81 witness for the proposition that retaining distributed control state requires more than keeping several copies: the system must also retain or reconstruct the relations that make some copy set admissible, reachable, and operationally authoritative.