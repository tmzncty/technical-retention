# Evidence 153D — Ceph 2017 snaptrim observability and error-stop semantics

**Status:** `bounded deepening complete`

## Bounded question

Case 153 already establishes the high-level RADOS relation:

```text
snapshot retirement
    != asynchronous trim execution
    != successful clone reclamation
```

This evidence pass asks a narrower implementation-history question:

> When did Ceph make the difference between **waiting to trim**, **actively trimming**, and **trimming stopped by an error** visible as explicit PG state, and what does the source say about the difference between transient scheduling friction and an error serious enough to stop reclamation work for repair?

The answer is bounded to upstream Ceph source-tree commits in 2017, a later 2018 regression/QA witness, and maintained Ceph documentation. It does not identify the invention of snapshot trimming, prove that every release behaved identically, or establish persistence of these PG-state bits across crash/restart.

---

## Source ladder

### H/P — upstream implementation, 13 February 2017

Ceph commit `c2eac34c86517e410eb4842d8b8085da7d8d7973`, Samuel Just:

> `osd/: add PG_STATE_SNAPTRIM[_WAIT] to expose snap trim state to user`

The patch adds:

- `PG_STATE_SNAPTRIM` with the source comment `trimming snaps`;
- `PG_STATE_SNAPTRIM_WAIT` with the source comment `queued to trim snaps`;
- string conversion for `snaptrim` and `snaptrim_wait`;
- explicit `publish_stats_to_osd()` calls when these bits are set or cleared.

The implementation sets `PG_STATE_SNAPTRIM_WAIT` while waiting for a snap-trim reservation and clears it on state exit. It sets `PG_STATE_SNAPTRIM` when entering the asynchronous work stage and clears it when leaving trimming.

Primary source:

<https://github.com/ceph/ceph/commit/c2eac34c86517e410eb4842d8b8085da7d8d7973>

### H/P — upstream implementation, 22 June 2017

Ceph commit `658a2f63b98bab9f23ae31c23b22866e5c92d55d`, David Zafman:

> `osd: On errors during snaptrim stop so pg can be repaired`

The patch adds `PG_STATE_SNAPTRIM_ERROR`, source-commented as `error stopped trimming snaps`, and includes it in PG health accounting. It also changes trim error handling so that missing/inconsistent object/snapset state can return an error instead of aborting the daemon.

The patch distinguishes at least two classes of inability to proceed:

- `-ENOLCK`: failure to obtain a write lock; the trimmer waits for the lock and does not classify this as `snaptrim_error`;
- non-lock failures such as missing object/snapset state or decode problems: set `PG_STATE_SNAPTRIM_ERROR`, allow already-started replicated operations to finish, then leave/reset the trim loop rather than continuing blindly.

Primary source:

<https://github.com/ceph/ceph/commit/658a2f63b98bab9f23ae31c23b22866e5c92d55d>

### H/P-release — Luminous stable release notes

Ceph's Luminous 12.2.5 release notes preserve the user-facing summary:

> `osd: Corrupt objects stop snaptrim and mark pg snaptrim_error`

This is useful as a shipped-release continuity witness. The underlying mechanism claim remains anchored to the implementation commit rather than inferred from the release-note sentence alone.

Source:

<https://docs.ceph.com/en/mimic/releases/luminous/>

### H/P-later-test — 8 November 2018 QA behavior

Ceph commit `a159f162c52fb9d12da5bb05ad512e610e67cdee`, David Zafman, updates `qa/standalone/scrub/osd-scrub-snaps.sh` so snapshot-removal tests wait while PG state contains `snaptrim`, but break out when `snaptrim_error` appears under deliberately corrupted conditions.

The commit message says:

> `Due to deliberate corruptions snaptrim_error means snaptrim is done`

That wording must be read in the test-control sense: the active trim loop has reached a stopped/error terminal condition for that test. It is **not** evidence that all reclamation work completed successfully.

Primary source:

<https://github.com/ceph/ceph/commit/a159f162c52fb9d12da5bb05ad512e610e67cdee>

### H/P-current — maintained documentation

Maintained Ceph placement-group documentation continues to distinguish:

- `snaptrim` — trimming snapshots;
- `snaptrim_wait` — queued to trim snapshots;
- `snaptrim_error` — error stopped trimming snapshots.

This is a continuity witness, not evidence that the same external vocabulary existed in the 2013 snaptrim document.

Source:

<https://docs.ceph.com/en/latest/rados/operations/pg-states/>

---

## Historical record

### H/P — operator-visible state was deliberately added after the underlying async mechanism

Case 153's 2013 source-tree documentation already describes asynchronous snapshot trimming. The 13-Feb-2017 commit is therefore not the origin of snaptrim itself. Its commit message is narrower: add PG state **to expose snap trim state to the user**.

This provides a useful chronology:

```text
2013: asynchronous snap-trim mechanism publicly documented
    ↓
2017-02: waiting vs active trim state deliberately exposed as PG state
    ↓
2017-06: stopped-by-error condition receives its own PG state
```

Safe conclusion:

> **maintenance work can predate explicit operator-visible phase vocabulary.**

Unsafe conclusion rejected:

> `PG_STATE_SNAPTRIM` was invented at the same time as snapshot trimming.

### H/P — waiting and working are not one state

The February 2017 patch does not merely add strings. It connects them to different state-machine locations:

- `snaptrim_wait` is set around reservation waiting;
- `snaptrim` is set when work is queued/entered for asynchronous trimming.

Both are explicitly published to the OSD statistics path when set and cleared.

Therefore:

```text
trim obligation exists
    != reservation acquired
    != trim worker active
```

and:

```text
operator sees snaptrim_wait
    != operator sees snaptrim
```

The patch grounds a bounded **publication relation**: the internal state transition is deliberately followed by PG-stat publication. It does not establish instantaneous cluster-wide observation or a linearizable monitoring API.

### H/P — lock contention is not classified as trim corruption/error

The June 2017 patch makes `trim_object()` return explicit status. Failure to acquire the relevant write lock returns `-ENOLCK`; the state machine waits for the lock to clear.

By contrast, missing object/snapset state, invalid clone relations, or snapset decode failures can return non-lock errors and drive `PG_STATE_SNAPTRIM_ERROR`.

Therefore the implementation itself distinguishes:

```text
cannot proceed now because resource/lock unavailable
    !=
cannot safely continue because required trim state is missing/inconsistent
```

This distinction matters for retention analysis because both conditions delay reclamation, but they imply different next actions.

### H/P — error publication changes the safe action from continue to stop/repair

The June 2017 commit message says errors during snaptrim should stop so the PG can be repaired. The code sets `PG_STATE_SNAPTRIM_ERROR` for the relevant non-lock failure path, lets already-started `repop` work finish, and then resets/leaves trimming rather than continuing through the remaining objects.

This grounds:

> **remaining cleanup obligation can survive while execution authority is withdrawn.**

The error state is not a new snapshot-retirement relation. It is an operational statement that the currently available metadata/state is insufficient to continue trimming safely.

### H/P — already-started work is allowed to settle before the trimmer stops

If an error is discovered while other trim operations are already in flight, the patch does not simply tear them down. It transitions to `WaitRepops`; when the in-flight set becomes empty, an error state causes reset rather than ordinary `RepopsComplete` continuation.

This is a small but important ordering witness:

```text
new error discovered
    != already-started replicated work instantly disappears
```

and:

```text
stop admitting further trim work
    +
allow already-started work to settle
    ->
leave/reset trimmer
```

This is source-level behavior for that implementation path, not a proof of transactional atomicity across every crash or lower-layer fault.

### H/P — `snaptrim_error` is a stopped-work state, not success evidence

The 2018 QA commit waits while `snaptrim` is present and breaks when `snaptrim_error` appears in deliberately corrupted tests. Its message colloquially says the error means snaptrim is `done` for the test.

The maintained state description is more precise: `snaptrim_error` means an error **stopped** trimming.

Accordingly:

```text
active trim loop no longer running
    != successful trim completion
```

and:

```text
terminal-for-this-attempt
    != reclamation obligation discharged
```

The test is useful precisely because it prevents a monitoring/test harness from waiting forever for a success state that cannot be reached until the underlying PG is repaired.

---

## Retained-state decomposition

This deepening adds three operator/control-state layers to the existing Case 153 decomposition.

### 1. Snapshot-retirement relation

The snapshot is no longer live and cleanup is owed.

### 2. Reconstructible/pending trim obligation

The PG has snapshot IDs / membership work that still requires trimming. Existing Case 153 evidence shows this obligation can be reconstructed from removed-vs-purged relations rather than requiring a byte-identical old queue.

### 3. Scheduling/reservation state

`snaptrim_wait` indicates work is queued/waiting for the relevant reservation opportunity.

### 4. Active execution state

`snaptrim` indicates the PG is actively in the trimming phase.

### 5. Error-stop state

`snaptrim_error` indicates a failure stopped trim execution.

### 6. Payload/membership state already revised by completed sub-operations

Some earlier objects may already have had snapshot membership updated before a later object exposes an error.

These relations must not be collapsed:

```text
snapshot retired
    != trim owed
    != trim waiting
    != trim active
    != trim error-stopped
    != all object memberships revised
    != all obsolete clones reclaimed
```

---

## Engineering reconstruction

### E — maintenance observability is a retained/publication layer, not the maintenance work itself

The 2017 PG bits summarize where the trimmer is in its control path. They do not contain the historical clone payload and do not by themselves perform reclamation.

Therefore:

> **maintenance-status evidence != maintenance effect.**

A small status bit can nevertheless be operationally important because it changes what an operator or automation system should infer about remaining work.

### E — `waiting`, `working`, and `blocked` are different debt states

All three can coexist with the same high-level fact: the snapshot has already been retired but cleanup is not yet fully complete.

A useful project model is:

```text
TRIM OWED
  |
  +--> WAITING FOR SERVICE/RESERVATION
  |
  +--> ACTIVE WORK
  |
  +--> ERROR-STOPPED / REPAIR REQUIRED
```

This is an engineering reconstruction. Ceph does not claim these are mutually exclusive philosophical kinds of `debt`; the source supplies concrete PG states and transitions.

### E — error state is evidence about execution admissibility, not about snapshot liveness

`snaptrim_error` does not make the retired snapshot live again. Nor does it establish that every clone is still present. It says the trimmer encountered a condition under which it should stop.

Therefore:

```text
reclamation execution invalid
    != historical snapshot authority restored
```

and:

```text
some cleanup already committed
    + later error
    != rollback of the whole trim history
```

The latter is bounded to the observed state-machine shape; it is not a universal idempotence or partial-commit theorem.

### E — repair can be prerequisite maintenance for maintenance

The commit's explicit reason for stopping is so the PG can be repaired. In this bounded path, therefore, one maintenance process (snapshot reclamation) can become contingent on another correctness process (repair of the state it relies on).

Functional relation:

> **cleanup machinery can itself depend on retained metadata being repairable and trustworthy.**

This is not a claim that Ceph `snaptrim_error` and media scrubbing, database repair, or SSD self-test are the same mechanism.

---

## Functional comparisons

### Case 142 — Ceph capacity-gated recovery

Case 142 distinguishes a repair obligation from the current ability to execute recovery/backfill because capacity can gate admission. Case 153D distinguishes a reclamation obligation from the ability to continue trim because reservation state or metadata/error conditions can gate execution.

Functional analogy only:

```text
work remains owed
    != work is currently admissible/executable
```

The gates and consequences differ. `backfill_toofull` is capacity admission; `snaptrim_error` is an error-stop state in snapshot reclamation.

### Case 61 — HDFS Observer state publication

Case 61 shows that useful internal/currentness state may need an explicit publication ordering before a caller can safely use it. Case 153D is not a consistency-protocol analogue, but the February 2017 patch similarly makes internal snaptrim phase transitions explicitly publishable to operator-visible PG statistics.

The bounded comparison is:

> **internal state transition != observer has been given corresponding state evidence.**

No shared algorithm or genealogy is implied.

### Case 38 — PLI self-test / health telemetry

Case 38 separates the existence of a protection mechanism from evidence about whether the protection path is currently healthy. Case 153D similarly separates the existence of a trim obligation from status saying the maintenance worker is waiting, active, or stopped by error.

Again, this is only a functional analogy about second-order operational evidence.

---

## Philosophical interpretation — bounded

`I` — Case 153 already shows that forgetting can require retained control state. This deepening adds a smaller point: **a system may also need to retain and publish state about whether forgetting is merely pending, actively being performed, or blocked because the conditions for safe forgetting are not satisfied.**

`I` — An error can therefore preserve an obligation by stopping its execution. Refusing to continue reclamation is not failure to remember what should be forgotten; it can be the action that prevents uncertain metadata from authorizing destructive cleanup.

These are project interpretations, not Ceph developers' historical philosophical claims.

---

## Explicit non-claims

This evidence does **not** establish that:

1. February 2017 is the invention date of asynchronous snap trimming;
2. `snaptrim_wait` existed as public user vocabulary in the 2013 document;
3. `snaptrim_error` itself is durably persisted across OSD crash/restart;
4. one PG-state publication is instantaneously visible to every monitor/client;
5. every `-ENOENT` in every Ceph release means physical payload loss;
6. every trim error requires the same repair procedure;
7. a lock wait and a corruption error are the only possible reasons snaptrim can pause;
8. `snaptrim_error` means successful reclamation completion;
9. leaving the active trim loop cancels the snapshot-retirement relation;
10. already-completed object-level trim operations are rolled back by a later error;
11. waiting for in-flight repops proves crash atomicity or exactly-once execution;
12. the 2018 test's word `done` means all cleanup succeeded;
13. PG repair and snapshot trimming are the same maintenance mechanism;
14. operator-visible PG state is itself the authoritative source of every underlying clone/membership fact;
15. current Ceph Crimson/classic OSD implementation details are identical to the 2017 code;
16. stopping logical reclamation says anything about lower-layer physical sanitization.

---

## Claim ledger

| Claim | Label | Evidence | Limit |
| --- | --- | --- | --- |
| Ceph added `snaptrim` and `snaptrim_wait` PG states on 2017-02-13 specifically to expose trim state to users | `H/P` | commit `c2eac34c` message + diff | source-tree/public implementation floor, not invention date |
| `snaptrim_wait` and `snaptrim` were attached to different state-machine phases and published to PG stats | `H/P/E` | commit `c2eac34c` diff | not a proof of instantaneous cluster-wide observation |
| Ceph added `snaptrim_error` on 2017-06-22 so corrupt/error conditions stop trimming for repair | `H/P` | commit `658a2f63` message + diff | exact recovery procedure not reconstructed here |
| lock contention follows a wait path instead of being classified as `snaptrim_error` in the inspected patch | `H/P/E` | `-ENOLCK` handling in `658a2f63` | bounded to inspected implementation |
| in-flight repops are allowed to finish before error-driven reset of the trimmer | `H/P/E` | `WaitRepops` / callback logic in `658a2f63` | not crash-atomicity proof |
| Luminous stable release notes expose the corrupt-object / `snaptrim_error` fix | `H/P-release` | Ceph 12.2.5 notes | release continuity, not mechanism detail source |
| 2018 QA treats `snaptrim_error` as a terminal condition for a deliberately corrupted test attempt | `H/P-later-test` | commit `a159f162` | terminal attempt != successful reclamation |
| current docs still distinguish wait / active / error-stopped snaptrim | `H/P-current` | maintained PG-state docs | current continuity only |
| trim obligation can persist while execution authority is withdrawn | `E` | 2017 stop-for-repair logic + existing Case 153 obligation model | project reconstruction |
| error-stop restores the retired snapshot to live status | `X` | no source | explicitly rejected |
| `snaptrim_error` proves all clones remain physically present | `X` | no source | explicitly rejected |

---

## Related-repository routing

A fresh search of `tmzncty/computing-archaeology` for `snaptrim` returned no dedicated module. This file therefore keeps only the retention-specific relation among:

- retired snapshot authority;
- pending reclamation obligation;
- reservation/wait state;
- active trim state;
- error-stop state;
- operator-visible publication.

A broader history of Ceph PG state vocabulary, snap-trimmer state-machine refactors, classic OSD versus Crimson, and release/backport genealogy belongs in `computing-archaeology` if pursued.

---

## Sources

1. Ceph commit `c2eac34c86517e410eb4842d8b8085da7d8d7973`, Samuel Just, 2017-02-13, **`osd/: add PG_STATE_SNAPTRIM[_WAIT] to expose snap trim state to user`**:
   <https://github.com/ceph/ceph/commit/c2eac34c86517e410eb4842d8b8085da7d8d7973>
2. Ceph commit `658a2f63b98bab9f23ae31c23b22866e5c92d55d`, David Zafman, 2017-06-22, **`osd: On errors during snaptrim stop so pg can be repaired`**:
   <https://github.com/ceph/ceph/commit/658a2f63b98bab9f23ae31c23b22866e5c92d55d>
3. Ceph Luminous 12.2.5 release notes, including the `snaptrim_error` fix:
   <https://docs.ceph.com/en/mimic/releases/luminous/>
4. Ceph commit `a159f162c52fb9d12da5bb05ad512e610e67cdee`, David Zafman, 2018-11-08, **`test: osd-scrub-snaps.sh: After snapshot removal wait for snaptrim to complete`**:
   <https://github.com/ceph/ceph/commit/a159f162c52fb9d12da5bb05ad512e610e67cdee>
5. Ceph maintained Placement Group States documentation:
   <https://docs.ceph.com/en/latest/rados/operations/pg-states/>
6. Case 153 canonical:
   [`../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md`](../cases/153-ceph-rados-snaptrim-asynchronous-reclamation.md)

---

## Result

This slice closes one previously implicit historical boundary in Case 153:

> **Ceph's operator-visible distinction between snaptrim waiting and active work was deliberately added in February 2017; a separate stopped-by-error state followed in June 2017, with source-level behavior that distinguishes transient lock waiting from errors serious enough to stop further trim work for repair.**

The resulting retention model is stronger than the generic statement `snapshot deletion is asynchronous`:

```text
retired snapshot authority
    -> reclamation obligation retained
    -> waiting / reservation state
    -> active trim state
    -> success
       OR
       error-stop / repair prerequisite
```

The state exposed to operators is evidence about the **execution condition of forgetting**, not proof that forgetting has already completed.