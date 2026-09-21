# Evidence 79C — Hadoop SafeMode Destructive-Command Guard and Startup Evidence Boundary (2006–2008)

## Status

**`bounded deepening complete`**. Canonical Case 79 remains **`grounded`**; this slice does not justify a maturity promotion.

This record deepens [`../cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md`](../cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md) around one narrow question:

> When a NameNode is still rebuilding its working view of replicas, what does the historical HDFS SafeMode record say about **destructive authority**—especially block-removal commands—and what may we safely infer from that record?

The bounded answer is stronger than “SafeMode is read-only,” but narrower than a universal theorem about incomplete knowledge:

- HDFS SafeMode was introduced in 2006 as a startup regime in which filesystem modifications were forbidden and block replication was inhibited;
- the safe-mode threshold was immediately tightened from `0.95` to `0.999` so that nearly all blocks had to be reported before filesystem modifications were permitted;
- HADOOP-3002 in 2008 documented a concrete violation: DataNodes were removing blocks while the NameNode was in SafeMode because block-report processing could return block-removal commands through a path not covered by the heartbeat guard;
- the issue was treated as a **Blocker**, fixed for Hadoop 0.17.2, and the release changelog summarizes the fix as **“Hold off block removal while in safe mode.”**

The project-level reconstruction is therefore:

```text
startup inventory still being re-observed
    + SafeMode active
    -> destructive block-removal authority should remain withheld
```

But the historical sources do **not** prove the stronger universal statement that every removal decision in every HDFS release was derived from a missing block report, nor that a SafeMode threshold means the entire replica inventory is complete.

---

## Scope

This slice is intentionally bounded to:

1. the 2006 introduction and early quantitative tightening of DFS SafeMode;
2. the 2008 HADOOP-3002 bug in which block-report processing could still return removal commands during SafeMode;
3. the distinction between positive report progress and permission to perform destructive mutation;
4. one controlled corroborating startup-loss incident, HADOOP-4810, used only to show that destructive classification at startup remained a concrete engineering hazard after HADOOP-3002.

It does **not** reconstruct:

- the complete history of HDFS SafeMode;
- every block invalidation path in every release;
- the exact patch diff for every HADOOP-3002 attachment;
- every condition under which a block is classified invalid, corrupt, excess, or stale;
- the complete HADOOP-4810 root cause;
- HA/fencing semantics;
- checksum verification;
- lease recovery;
- Byzantine or adversarial report handling;
- the genealogy of restricted startup modes outside Hadoop.

Those remain separate slices.

---

## Source custody and chronology

### Primary / contemporary source A — HADOOP-306, release 0.7.0 change record

Apache's historical `CHANGES.txt` records HADOOP-306 in **Release 0.7.0 (2006-10-06)** as adding a “safe” mode to DFS. The change record states that the NameNode enters it when less than a specified percentage of file data is complete, that it was then used on startup, and that while in SafeMode **filesystem modifications are not permitted and block replication is inhibited**.

Source:

- Apache Hadoop historical `CHANGES.txt` mirror, HADOOP-306 entry: <https://apache.googlesource.com/hadoop-common/+/9e6c62124f0812e0f70d960ba0744354edfab738/CHANGES.txt>

This is a release-history statement, not proof that HADOOP-306 invented the general idea of a safe/restricted startup mode.

### Primary / contemporary source B — HADOOP-594, 2006-10-11

Apache commit mail for SVN revision **462907**, dated **2006-10-11**, records HADOOP-594 changing `dfs.safemode.threshold.pct` from `0.95f` to `0.999f`. The accompanying changelog explanation says the purpose was for **nearly all blocks to be reported before filesystem modifications are permitted**.

Source:

- Apache commit archive for SVN r462907: <https://www.mail-archive.com/hadoop-commits%40lucene.apache.org/msg00669.html>

This is important because it ties the quantitative threshold directly to an admission policy. It does not say that `0.999` equals a complete cluster inventory or that every DataNode must have reported.

### Primary / contemporary source C — HADOOP-3002, 2008-03 to 2008-07

ASF JIRA HADOOP-3002 is titled **“HDFS should not remove blocks while in safemode.”** It was created **2008-03-12**, marked **Blocker**, affected **0.16.0**, resolved **2008-07-08**, and lists **0.17.2** as the fix version.

The reporter, Konstantin Shvachko, records the observed failure in an experimental cluster during a prolonged distributed upgrade: DataNodes were removing blocks while the NameNode was in SafeMode. He then states the intended SafeMode contract:

- no namespace-changing client requests;
- no scheduled block replication or block removal for DataNodes.

The issue explains the uncovered seam precisely enough for this bounded study: heartbeat processing explicitly checked SafeMode and did not return block commands, **but block-report processing could also return block commands**, and those commands likewise needed to be banned while SafeMode was active.

Source:

- ASF JIRA HADOOP-3002: <https://issues.apache.org/jira/browse/HADOOP-3002>

The issue history records patch iterations in July 2008 and a final comment on **2008-07-08** saying the fix was committed. QA tested the latest attachment against trunk revision `674932`; the patch passed core and contrib tests, although the automated review noted no new/modified tests in that attachment.

### Primary / institutional source D — Hadoop 0.17.2 release changelog

Apache's historical changelog lists **HADOOP-3002 — “HDFS should not remove blocks while in safemode.”** as a Blocker bug fix in **Hadoop 0.17.2**, released **2008-08-11**. The older source-tree changelog wording is even more implementation-oriented: **“Hold off block removal while in safe mode.”**

Sources:

- Apache Hadoop 0.17.2 changelog: <https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/release/0.17.2/CHANGELOG.0.17.2.html>
- Apache Hadoop historical `CHANGES.txt` mirror containing the HADOOP-3002 line: <https://apache.googlesource.com/hadoop-hdfs/+/fb327f685b43ab328667d11747f8cb015d5de62b/CHANGES.txt>

### Primary / institutional source E — HDFS architecture wording

Apache HDFS architecture documentation describes a `Blockreport` as the list of blocks hosted by a DataNode and describes startup SafeMode as a period in which the NameNode receives Heartbeat and Blockreport messages while waiting for a configured percentage of blocks to satisfy the minimum-replica condition before exiting SafeMode.

Source:

- Apache HDFS architecture source/documentation: <https://apache.googlesource.com/hadoop-hdfs/+/refs/heads/HDFS-326/src/docs/src/documentation/content/xdocs/hdfs_design.xml>

This is used only to ground the positive observation surface and threshold semantics. It is not used to retrofit later implementation details into the 2006 code.

### Corroborating contemporary source F — HADOOP-4810, December 2008

ASF JIRA HADOOP-4810, **“Data lost at cluster startup time,”** was created **2008-12-09**, marked Blocker, affected 0.18.2, and fixed for 0.18.3. Its attached NameNode log trace records inconsistent-size replicas, attempted invalidation of two replicas being rejected with `SafeModeException`, and other replicas later being placed in invalidation/deletion handling before the file became unreadable.

Source:

- ASF JIRA HADOOP-4810: <https://issues.apache.org/jira/browse/HADOOP-4810>

This issue is **not** treated as the same bug as HADOOP-3002. It is included only because it demonstrates, in the same historical period, that startup-time replica classification plus deletion could be a real data-loss boundary and that a SafeMode guard on one invalidation path did not amount to a universal proof that all later destructive decisions were safe.

---

## Historical record

### H/P — SafeMode begins as a mutation/replication admission regime, not just a status label

The HADOOP-306 release record gives the earliest bounded source in this slice. SafeMode is not described merely as an informational state. It changes what the NameNode is permitted to do:

```text
SafeMode active
    -> filesystem modifications forbidden
    -> block replication inhibited
```

That means the state has operational authority semantics from the beginning of the bounded Hadoop record.

### H/P — the threshold was explicitly tied to report progress before mutation

HADOOP-594 changed the default SafeMode threshold from `0.95` to `0.999`. The historical explanation matters more than the number alone: the intended effect was to require **nearly all blocks to be reported before filesystem modifications are permitted**.

Therefore, in this bounded 2006 record:

```text
report progress
    -> SafeMode admission progress
    -> later permission for ordinary mutation
```

But:

```text
0.999 threshold reached
    != every block reported
    != every DataNode reported
    != every replica relation globally complete
```

The configuration is deliberately a threshold, not a claim of exhaustive inventory closure.

### H/P — HADOOP-3002 exposes a command-path hole

HADOOP-3002 records a concrete mismatch between the intended SafeMode contract and one command path. Heartbeat processing already checked SafeMode and withheld block commands. Block-report processing could also return block commands, but the same prohibition had not been applied there.

This is historically important because it rules out an overly abstract description such as:

> “SafeMode existed, therefore destructive commands were impossible.”

The actual 2008 system had multiple outbound-command paths, and one required an explicit fix.

The bounded historical relation is:

```text
policy says no removal in SafeMode
    != every implementation path already enforces that policy
```

### H/P — the fix was release-bearing

HADOOP-3002 was not merely an abandoned proposal. JIRA records it as fixed, and the Apache 0.17.2 changelog lists it as a Blocker bug fix. The source-tree changelog summarizes the result as holding off block removal while in SafeMode.

This supports a concrete historical statement:

> **By Hadoop 0.17.2, Apache treated withholding block removal during SafeMode as part of the released correctness boundary.**

It does not establish that every subsequent invalidation/classification bug was thereby eliminated.

### H/P — December 2008 still shows deletion safety was not reducible to one guard

HADOOP-4810 is useful precisely because it should **not** be collapsed into HADOOP-3002. Its log trace shows SafeMode rejecting attempted invalidation of replicas with inconsistent sizes, while other deletion/excess-replica processing was also involved in the eventual unreadable-block outcome.

The safe claim is:

> **A SafeMode check on one destructive path is not equivalent to a proof that all replica classification and deletion paths are safe under startup conditions.**

The issue does not authorize a broader claim about every removal path, and this slice does not reconstruct the complete patch/root cause.

---

## Engineering reconstruction

### E — positive observation and destructive authority are different state transitions

Case 79 already establishes that a restarted NameNode reconstructs block-location knowledge from DataNode reports. HADOOP-3002 adds a different question: what may the NameNode **do** while that relation is still being established?

The useful decomposition is:

```text
DataNode reports replica(s)
    -> NameNode gains positive inventory evidence

inventory evidence/progress
    -> SafeMode progress may increase

SafeMode active
    -> destructive removal authority withheld
```

Thus:

> **receiving evidence ≠ permission to destroy evidence-bearing objects.**

The same RPC family can both improve the NameNode's inventory knowledge and, if incorrectly wired, return a destructive command. HADOOP-3002 is valuable because it shows those roles had to be separated by an explicit gate.

### E — evidence sufficiency is action-relative

A NameNode may know enough to accept a positive fact such as “DataNode D reports block B” before it is willing to resume ordinary mutation/removal policy.

That supports the bounded relation:

```text
sufficient evidence to add an observed replica relation
    !=
sufficient evidence to authorize destructive removal work
```

This is stronger and safer than claiming that HDFS requires total knowledge before any action. The historical system explicitly used thresholds and later post-SafeMode repair work, so the evidence requirement is **action-relative**, not absolute.

### E — SafeMode threshold is an admission rule, not an inventory-completeness certificate

HADOOP-594 is a particularly clean guardrail against a common overstatement. The threshold was raised to `0.999`, not `1.0`, and the stated purpose was to delay filesystem modifications until nearly all blocks had been reported.

Therefore:

> **SafeMode exit threshold reached ≠ proof of complete replica inventory.**

And:

> **destructive work permitted after the gate ≠ logically impossible for undiscovered/stale replica information to remain.**

The mechanism is a bounded risk/admission policy, not a mathematical closure proof.

### E — absence from the current view must be kept separate from positive destruction evidence

Case 79's canonical record already establishes:

```text
not yet reported
    != physically destroyed
```

HADOOP-3002 gives a complementary control-side reason not to erase that distinction too early: SafeMode deliberately withholds removal commands while startup/reporting work is still underway.

The project may therefore use the following **engineering reconstruction**:

```text
current working inventory lacks relation R
    != automatically entitled to destroy every embodiment that might later affect R
```

This is **not** attributed to Hadoop developers as “negative knowledge” terminology, and HADOOP-3002 by itself does not prove that the buggy deletions were caused specifically by treating an unreported replica as nonexistent. The claim is about action gating under incomplete startup observation, not a reconstructed hidden branch condition.

### E — safety policy must cover all command-emission surfaces that can violate it

HADOOP-3002 gives an unusually concrete implementation lesson:

```text
heartbeat path checks SafeMode
    + block-report path can also return block commands
    -> heartbeat-only guard is incomplete
```

So:

> **policy coverage ≠ one-path coverage.**

For retention work, this matters because deletion authority is only as safe as the set of paths able to emit or enqueue deletion work.

### E — retention depends on withholding some maintenance actions, not only performing maintenance

Block removal is normally legitimate maintenance: stale, excess, or otherwise invalid replicas eventually need reclamation. Yet during a startup/re-observation interval, performing that maintenance too early can be riskier than deferring it.

Hence:

```text
retention-supporting maintenance
    can include
    deliberate non-execution of reclamation
    until an admission boundary is satisfied
```

This is not maintenance abandonment. It is timing/authority control over a destructive maintenance operation.

---

## Controlled functional comparisons

### A — Case 46, Google File System location reconstruction

Case 46 provides a bounded functional comparison: GFS can reconstruct chunk-location knowledge from chunkservers rather than persist every location centrally. Case 79 adds a Hadoop-specific control surface in which mutation/removal authority is restricted during startup re-observation.

Functional analogy only:

```text
re-derived distributed location knowledge
    + delayed destructive/repair authority
```

No historical derivation from GFS to HDFS is claimed here.

### A — Case 28 / Case 150 reclamation authority

Other repository cases distinguish logical retirement, reclamation authority, and physical reuse/erase. HADOOP-3002 is analogous only at the level of **destructive authority gating**: a block-removal command is not equivalent to the mere existence of a reason that might eventually justify reclamation.

No ATA/TRIM/SSD mechanism is being projected onto HDFS.

### A — Case 83 maintenance-history control state

Case 83 shows that losing recent verification history can change future maintenance eligibility. Case 79 is different: the relevant startup relation is current distributed inventory evidence and a SafeMode admission gate, not a history log.

Therefore:

> **historical completion evidence ≠ current inventory re-observation.**

---

## Philosophical interpretation — bounded

The narrow conceptual pressure is this:

> A technical system does not gain safe destructive authority merely because it possesses some facts about an object. Authority depends on whether the evidence needed for the contemplated action is sufficiently established under that operation's own contract.

This permits one bounded project formulation:

```text
what is currently known
    != what may safely be destroyed
```

The stronger phrase “absence becomes knowledge only when an observation boundary closes” can be useful as a philosophical shorthand, but it must remain clearly marked as project interpretation. HDFS SafeMode uses configurable thresholds and does not wait for universal epistemic closure.

The historical actors used terms such as SafeMode, Blockreport, block removal, replication, threshold, and filesystem modification—not `epistemic closure`, `negative knowledge`, or `ontology`.

---

## Explicit non-claims

This evidence does **not** establish that:

1. HADOOP-306 invented safe/restricted startup modes;
2. Hadoop 0.7.0 was the first distributed filesystem to delay mutation during recovery;
3. HADOOP-594's `0.999` threshold means all DataNodes or all replicas have reported;
4. SafeMode exit is a certificate of globally complete replica knowledge;
5. every HDFS release uses the same threshold, extension, or removal machinery;
6. HADOOP-3002 was caused specifically by interpreting an unreported replica as destroyed;
7. every block-removal decision is based on negative evidence;
8. block reports are cryptographic proofs;
9. a reported replica is byte-integrity-qualified forever;
10. SafeMode prevents every possible data-loss bug;
11. one SafeMode check covers every command-emission path automatically;
12. HADOOP-4810 has the same root cause as HADOOP-3002;
13. HADOOP-4810 proves that HADOOP-3002's fix failed;
14. every deletion visible in HADOOP-4810 occurred while SafeMode was active;
15. withholding deletion restores an already missing replica;
16. suppressing removal means repair/replication should also run immediately;
17. SafeMode is a consensus protocol;
18. SafeMode is a quorum proof;
19. SafeMode is a sanitization mechanism;
20. SafeMode is equivalent to filesystem-wide write-ahead logging;
21. the current NameNode inventory lacking a replica proves the replica physically does not exist;
22. `nearly all blocks reported` is equivalent to `all future block reports are redundant`;
23. after SafeMode exit there can be no under-replicated blocks;
24. Hadoop authors used the terms `negative knowledge`, `evidence closure`, or `action-relative evidence sufficiency`;
25. the GFS comparison establishes a historical genealogy;
26. block deletion and SSD TRIM share one implementation lineage;
27. a bug marked Blocker implies every production deployment experienced data loss;
28. JIRA creation date is the invention date of the mechanism;
29. release changelog inclusion proves the exact patch behavior beyond the bounded issue statement;
30. this evidence closes the wider history of HDFS startup safety.

---

## Claim ledger

| Claim | Layer | Support / boundary |
| --- | --- | --- |
| HADOOP-306 introduced DFS SafeMode into the bounded Hadoop release record by 0.7.0 | `H/P` | Apache historical `CHANGES.txt`; no broader invention claim |
| the 2006 SafeMode record prohibits filesystem modifications and inhibits replication | `H/P` | HADOOP-306 changelog wording |
| HADOOP-594 changed the default threshold from 0.95 to 0.999 so nearly all blocks would report before modifications were permitted | `H/P` | Apache SVN r462907 commit archive |
| HADOOP-3002 observed DataNodes removing blocks while the NameNode was in SafeMode | `H/P` | ASF JIRA description |
| heartbeat handling already guarded block commands while block-report handling could also return block commands and needed the same ban | `H/P` | HADOOP-3002 description |
| HADOOP-3002 was fixed for 0.17.2 and the changelog describes holding off block removal in SafeMode | `H/P` | ASF JIRA + Apache 0.17.2 changelog |
| positive inventory evidence can be accepted before destructive authority is resumed | `E` | block-report progress + SafeMode removal gate |
| threshold satisfaction is not a complete-inventory certificate | `E` grounded in `H/P` | explicit 0.999 threshold and later threshold-based architecture semantics |
| policy coverage must include every command-emission path capable of removal | `E` | heartbeat vs block-report seam in HADOOP-3002 |
| HADOOP-4810 demonstrates a separate startup-time deletion/data-loss hazard, not the same bug | `H/P` + boundary | ASF JIRA; no root-cause merger |
| an absent current relation proves physical loss | `X` | contradicted by Case 79's report-rebuilt location model |
| SafeMode prevents all destructive bugs | `X` | HADOOP-3002 itself is a counterexample to policy-by-name assumptions |

---

## Sources

### Primary / contemporary / institutional

- Apache Hadoop historical `CHANGES.txt`, HADOOP-306 and early SafeMode release record: <https://apache.googlesource.com/hadoop-common/+/9e6c62124f0812e0f70d960ba0744354edfab738/CHANGES.txt>.
- Apache commit archive, SVN r462907, HADOOP-594, **2006-10-11**: <https://www.mail-archive.com/hadoop-commits%40lucene.apache.org/msg00669.html>.
- ASF JIRA, HADOOP-3002, **“HDFS should not remove blocks while in safemode.”**: <https://issues.apache.org/jira/browse/HADOOP-3002>.
- Apache Hadoop 0.17.2 changelog, release **2008-08-11**: <https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/release/0.17.2/CHANGELOG.0.17.2.html>.
- Apache Hadoop historical `CHANGES.txt`, HADOOP-3002 **“Hold off block removal while in safe mode.”**: <https://apache.googlesource.com/hadoop-hdfs/+/fb327f685b43ab328667d11747f8cb015d5de62b/CHANGES.txt>.
- Apache HDFS architecture source, Blockreport and startup SafeMode description: <https://apache.googlesource.com/hadoop-hdfs/+/refs/heads/HDFS-326/src/docs/src/documentation/content/xdocs/hdfs_design.xml>.
- ASF JIRA, HADOOP-4810, **“Data lost at cluster startup time.”**: <https://issues.apache.org/jira/browse/HADOOP-4810>.

### Repository controls

- [`../cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md`](../cases/79-apache-hdfs-startup-safemode-block-report-reobservation.md) — canonical startup re-observation case.
- [`79-hadoop-2008-2016-manual-safemode-restart-lifetime-deepening.md`](79-hadoop-2008-2016-manual-safemode-restart-lifetime-deepening.md) — manual SafeMode process-lifetime versus startup reconstruction.
- Case 46 — GFS master recovery/location reconstruction, functional comparison only.
- Case 83 — HDFS block-scanner verification history, contrasting history-based control state.

---

## Remaining work

This slice closes only the **SafeMode destructive-command guard** boundary. Useful follow-ups remain:

1. retrieve and diff the final HADOOP-3002 branch-0.17 / branch-0.18 patch against its immediate parent to identify the exact removal-command return-site changes;
2. locate the exact SVN/Git commit corresponding to the 2008-07-08 final HADOOP-3002 commit, rather than relying only on JIRA + release changelog;
3. reconstruct HADOOP-4810 separately if startup corrupt/excess classification becomes a dedicated case slice;
4. test a period-correct MiniDFSCluster build with delayed/partial block reports and instrument when invalidate commands become eligible;
5. compare automatic SafeMode threshold exit with the last-arriving DataNode/block-report frontier without assuming equality;
6. keep broader distributed-filesystem recovery genealogy in `tmzncty/computing-archaeology` rather than duplicating it here.

---

## Bounded conclusion

The 2006–2008 Hadoop record supports a precise retention/control boundary:

```text
re-observing distributed replica state
    !=
authority to mutate or remove replicas
```

SafeMode was historically an admission regime, its threshold was explicitly tied to report progress before modification, and HADOOP-3002 shows that the destructive-removal prohibition had to be enforced across more than one command-emission path. The safest project-level conclusion is therefore not that HDFS waits for perfect knowledge, but that **destructive maintenance has an evidence/admission boundary distinct from merely receiving positive inventory reports**.
