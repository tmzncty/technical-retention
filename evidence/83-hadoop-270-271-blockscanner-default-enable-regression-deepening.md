# Case 83 deepening — Hadoop 2.7.0→2.7.1 BlockScanner default-enable regression

**Status:** `bounded deepening complete`

**Canonical case:** [`../cases/83-apache-hdfs-block-scanner-checksum-verification.md`](../cases/83-apache-hdfs-block-scanner-checksum-verification.md)

## Scope

This packet isolates one release-bounded control-plane question in Case 83:

> **Can a DataNode contain the block-scanner implementation, retain its block payload and checksum files, and still silently lose ordinary proactive verification because the maintenance mechanism is disabled by a configuration/default interaction?**

The bounded transition is Apache Hadoop **2.7.0 → 2.7.1** in 2015, using Apache JIRA HDFS-8681 and the corresponding Apache Hadoop commit `c6793dd8cc69ea994eb23c3e1349efe4b9feca9a`.

This is intentionally narrower than a general history of HDFS block scanning. Case 83 already grounds the later Hadoop 2.7.3 `BlockScanner` / `VolumeScanner` mechanism, suspect-block priority, persisted scan cursor, HDFS-11160 checksum/data coherence, and HDFS-11187 reconstructible last-partial-checksum state. This packet instead closes a missing release-boundary seam immediately before that 2.7.3 snapshot.

It also does **not** claim that Hadoop 2.7.0 erased or corrupted blocks. The defect is about **maintenance admission / enablement**: ordinary background integrity verification could be absent by default even while payload and checksum embodiments survived.

---

## Why this slice is not duplicate work

The existing canonical says, correctly for the later 2.7.3 bounded implementation, that a negative scan period disables scanning, a configured zero is converted to a three-week period for compatibility, and `isEnabled()` additionally requires a positive per-volume scan rate.

Without the 2.7.0→2.7.1 release history, that later rule can look timeless. HDFS-8681 shows that it was not.

The Apache issue is explicit that Hadoop **2.7.0** was affected: after the HDFS-7430 scanner rewrite, the default scan-period value remained `0`, while the new enable test required `scanPeriodMs > 0`. The result was that the block scanner was **disabled by default**. Apache treated the issue as a **Blocker** for 2.7.1 and supplied a configuration workaround: set the value greater than zero.

The later 2.7.3 behavior used by Case 83 therefore sits on top of a concrete compatibility repair rather than being safely projectable backward into the first 2.7 release.

---

## Historical record

### H/P — HDFS-8681 identifies Hadoop 2.7.0 as an affected release

Apache JIRA HDFS-8681 is titled **“BlockScanner is incorrectly disabled by default.”** It records:

- type: Bug;
- priority: Blocker;
- affected version: **2.7.0**;
- fix versions: **2.7.1, 2.8.0, 3.0.0-alpha1**;
- component: DataNode.

The issue description reproduces the decisive enable test:

```java
public boolean isEnabled() {
  return (conf.scanPeriodMs) > 0 && (conf.targetBytesPerSec > 0);
}
```

and states that the default scan-period value was still `0`, so the scanner was disabled by default.

Source: Apache JIRA HDFS-8681, <https://issues.apache.org/jira/browse/HDFS-8681>.

This is stronger than inferring behavior from a configuration manual alone: the project itself classified the shipped/default interaction as a defect in 2.7.0.

### H/P — the project linked the regression to the HDFS-7430 scanner rewrite

HDFS-8681 is linked in Apache JIRA as **broken by HDFS-7430**, the improvement that rewrote the BlockScanner to use O(1) memory and multiple threads.

That relationship supports a bounded historical statement:

```text
scanner rewrite shipped
    + old/default scan-period value remained 0
    + new enable predicate required > 0
    -> ordinary BlockScanner disabled by default in 2.7.0
```

This does **not** establish that every deployment actually ran with defaults. Operators could override the setting, and the JIRA discussion explicitly notes the workaround of setting a value greater than zero.

Source: HDFS-8681 issue link to HDFS-7430 and Andrew Wang / Arpit Agarwal comments, <https://issues.apache.org/jira/browse/HDFS-8681>.

### H/P — the JIRA discussion preserves the compatibility archaeology

The HDFS-8681 discussion is unusually useful because maintainers looked backward while deciding what `0` should mean.

Arpit Agarwal quoted the branch-2.6-era logic in which a nonpositive configured number was replaced with an internal three-week scan period. The discussion then converged on restoring a three-week fallback for the zero/default case while giving an explicit negative value the disable role in the new contract.

This is release-history evidence, not a claim that every older branch had identical code or documentation. The packet uses it only to establish that the maintainers themselves treated the 2.7.0 result as a compatibility regression rather than a deliberate new default policy.

Source: Apache JIRA HDFS-8681 comments dated 27–28 June 2015, <https://issues.apache.org/jira/browse/HDFS-8681>.

### H/P — commit `c6793dd8` repairs both the code default and the documented configuration contract

Apache Hadoop commit `c6793dd8cc69ea994eb23c3e1349efe4b9feca9a`, committed **28 June 2015**, is titled:

> `HDFS-8681. BlockScanner is incorrectly disabled by default.`

The commit changes several independently useful artifacts.

#### `DFSConfigKeys.java`

The default changes from:

```java
DFS_DATANODE_SCAN_PERIOD_HOURS_DEFAULT = 0;
```

to:

```java
DFS_DATANODE_SCAN_PERIOD_HOURS_DEFAULT = 21 * 24;  // 3 weeks.
```

#### `BlockScanner.java`

The commit adds `getConfiguredScanPeriodMs(...)` with an explicit compatibility rule:

- a configured `0` is converted to the default three-week period;
- a negative value is left negative so the scanner can be disabled;
- `isEnabled()` still requires both a positive scan period and a positive target byte rate.

This matters because the fix is not merely a documentation correction. It changes the value feeding the runtime admission predicate.

#### `hdfs-default.xml`

The documented default changes from `0` to `504` hours. The description now distinguishes:

```text
positive value
    -> scan-period constraint

zero
    -> use 504 h / three-week default

negative
    -> disable block scanner
```

The new documentation also says prior HDFS versions incorrectly documented zero as disabling the scanner.

#### `CHANGES.txt`

The change is recorded under `Release 2.7.1 - UNRELEASED`, immediately above the `Release 2.7.0 - 2015-04-20` boundary in that historical file.

Primary commit: <https://github.com/apache/hadoop/commit/c6793dd8cc69ea994eb23c3e1349efe4b9feca9a>.

### H/P — Apache released 2.7.1 as the stable point release after 2.7.0

Apache's release page states that Hadoop **2.7.1** was released on **6 July 2015** as a point release for the 2.7 line and points readers to its bug-fix release notes.

Source: Apache Hadoop, **Release 2.7.1 (stable) available**, <https://hadoop.apache.org/release/2.7.1.html>.

The dates establish a narrow sequence:

```text
20 Apr 2015  Hadoop 2.7.0 release boundary recorded in CHANGES
28 Jun 2015  HDFS-8681 fix commit
06 Jul 2015  Hadoop 2.7.1 stable release announcement
```

The packet does not infer field-upgrade speed or operator uptake from this chronology.

---

## Engineering reconstruction

The historical record exposes a maintenance-control stack that should not be collapsed into one Boolean.

```text
maintenance implementation exists
    !=
configuration admits maintenance
    !=
scanner threads actually run
    !=
volume/block-pool traversal progresses
    !=
particular block is successfully verified
    !=
corruption, if found, is later repaired
```

HDFS-8681 sits specifically between the first two layers.

### 1. Capability presence is not maintenance admission

Hadoop 2.7.0 contained the rewritten BlockScanner code. That fact did not make ordinary background verification happen under the shipped default because the enable predicate rejected the default scan period.

Therefore:

> **maintenance code present ≠ maintenance enabled.**

This is different from Case 83's later cursor-checkpoint defect. A broken cursor checkpoint can lose/replay *progress after scanning has been admitted*. HDFS-8681 can prevent the ordinary scanner from entering that maintenance regime at all.

### 2. Default configuration is control state, not payload state

The values controlling scan period and scan rate do not encode HDFS user data. They govern whether and how rapidly the system spends resources renewing integrity qualification.

So:

> **payload retention ≠ retention of the policy that causes payload integrity to be rechecked.**

A DataNode can retain block files and checksum files while proactive verification coverage quietly stops.

The immediate consequence is not `data lost`. It is weaker and more precise:

```text
scanner disabled
    -> no ordinary background scan work from that scanner
    -> latent corruption can remain undiscovered longer
```

Whether corruption actually exists is a separate physical/software event.

### 3. A configured interval is not an observed coverage guarantee

Even after the 2.7.1 fix, `504 hours` is a policy/default, not proof that every block is successfully checked exactly every 21 days.

Case 83 already records rate limiting, scanner scheduling, cursor state, suspect prioritization, exceptions, and later cursor-checkpoint defects. Accordingly:

> **scanner enabled ≠ full-pass completion.**

> **nominal scan period ≠ measured verification-age bound for every replica.**

HDFS-8681 closes only the admission/default seam.

### 4. The same configuration token can acquire a different effective control meaning across a release boundary

This slice is especially useful because the literal value `0` sits on both sides of the transition.

In the affected 2.7.0 interaction described by HDFS-8681:

```text
scanPeriodMs = 0
    + isEnabled requires > 0
    -> disabled
```

After `c6793dd8`:

```text
configured 0
    -> translated to default 504 h
    -> positive scan period enters isEnabled
```

while a negative value becomes the explicit disable path.

Thus, within this bounded software transition:

> **retained configuration bytes ≠ retained operational meaning across software versions.**

That is an engineering reconstruction. Apache does not use the project phrase `operational meaning retention`.

It also does not mean every explicit `0` configuration was actually carried through an upgrade. No deployment telemetry is supplied here.

### 5. Compatibility repair itself is a policy choice

The fix could have been implemented merely by changing `> 0` to `>= 0`, by choosing a new default, or by changing documented disable semantics. The accepted commit instead combines a concrete default of 504 hours with a zero→default compatibility conversion and an explicit negative disable path.

The important retention point is not which choice was philosophically best. It is that maintenance continuity depends on **configuration interpretation as well as on persisted data and executable code**.

---

## Controlled functional comparisons

### Case 83 cursor checkpoint defect

Same case, different layer:

```text
HDFS-8681
    -> maintenance admission/default defect

HDFS-12209-related cursor path
    -> maintenance-progress checkpoint cadence defect
```

Both can increase repeated/unperformed verification work without directly corrupting payload, but they are not the same failure mode.

> **admission state ≠ progress state.**

### Case 102 — MegaRAID Patrol Read

Case 102 separates a configured patrol schedule from maintenance admission and execution. HDFS-8681 is a software counterpart at a different stack level: a nominal maintenance feature can exist while a control gate prevents the expected background activity.

This is a functional comparison only. No historical influence or implementation genealogy is claimed between MegaRAID Patrol Read and HDFS BlockScanner.

### Case 111 — enterprise-SSD powered maintenance opportunity

Case 111 separates retention-maintenance capability from having enough powered time for the controller to perform maintenance. HDFS-8681 separates capability from being enabled by software configuration.

The common abstraction is only:

```text
maintenance capability
    !=
maintenance opportunity/admission
    !=
maintenance completion
```

The mechanisms, media, actors, and timescales are different.

### Case 18 — ZFS scrub

Both HDFS background scanning and ZFS scrub can renew knowledge about integrity by actively reading retained data. HDFS-8681 adds a negative control-plane lesson: having a verifier in the software does not establish that proactive verification is operating in a deployment.

No ZFS→HDFS genealogy is inferred.

---

## Philosophical interpretation — downstream only

The bounded philosophical consequence is modest:

> **A retained object can outlive the activity by which a system periodically renews its justification for trusting that object.**

HDFS-8681 is useful because nothing in the bug requires block bytes to disappear. What disappears under the affected default is a recurring *practice of verification*.

A second bounded consequence concerns configuration:

> **Preserving a control symbol is not enough when the software interpreting that symbol changes.**

The literal `0` can remain `0` while its relation to scanner admission changes across the release boundary. This is not a general theory of software meaning; it is a concrete engineering example in which configuration interpretation participates in whether maintenance occurs.

These are project interpretations. Apache's historical vocabulary is `BlockScanner`, scan period, default, enabled/disabled, and the HDFS-8681 compatibility discussion.

---

## Explicit non-claims

This packet does **not** claim that:

1. Hadoop 2.7.0 lost user payload because HDFS-8681 existed.
2. Every 2.7.0 deployment used the default scan period.
3. Every 2.7.0 deployment therefore had scanning disabled.
4. Operators could not work around the issue; the JIRA explicitly names a positive configured period as a workaround.
5. A disabled background scanner disables demand-read checksum verification.
6. A disabled scanner prevents NameNode block reports.
7. A disabled scanner immediately makes every replica corrupt.
8. A 21-day configured period proves every block is scanned within exactly 21 days.
9. The 504-hour value is a physical media-retention threshold.
10. The 504-hour value is a corruption-latency guarantee.
11. HDFS-8681 is the origin of HDFS integrity scanning.
12. HDFS-7430 invented background block verification.
13. The 2.7.1 fix proves all later scanner scheduling paths were correct.
14. The 2.7.1 fix repairs the later cursor clock-domain defect discussed elsewhere in Case 83.
15. Cursor persistence and scanner enablement are the same state.
16. `isEnabled() == true` proves a scanner thread is healthy forever.
17. `isEnabled() == true` proves a complete block-pool pass occurred.
18. A successful scanner pass repairs a bad replica locally.
19. Reporting a bad block is the same thing as re-replication.
20. The issue demonstrates Byzantine integrity protection.
21. The issue demonstrates cryptographic attestation.
22. The commit's compatibility wording proves what every pre-2.7 branch actually did without separate inspection.
23. An explicit `0` was necessarily present in every upgraded site's persistent configuration.
24. The same literal configuration value has unstable meaning in all software systems.
25. The HDFS configuration regression is historically descended from RAID patrol-read or SSD maintenance systems.

---

## Claim ledger

| Claim | Type | Evidence | Strength |
| --- | --- | --- | --- |
| HDFS-8681 affected Hadoop 2.7.0 | Historical record | Apache JIRA affected-version field | H/P |
| 2.7.0's BlockScanner was disabled by default because default scan period was 0 while `isEnabled()` required `> 0` | Historical record | HDFS-8681 description | H/P |
| Apache treated the defect as a Blocker for 2.7.1 | Historical record | HDFS-8681 priority/fix-version fields and comments | H/P |
| Setting a positive scan period was an available workaround | Historical record | HDFS-8681 maintainer comment | H/P |
| Commit `c6793dd8` changed the code default to 504 h / three weeks | Historical record | Apache commit diff | H/P |
| The same commit maps configured zero to the default and leaves negative values as the disable path | Historical record | `getConfiguredScanPeriodMs` diff + `hdfs-default.xml` | H/P |
| The fix is recorded under the 2.7.1 section of `CHANGES.txt` | Historical record | Apache commit diff | H/P |
| Hadoop 2.7.1 was announced 6 July 2015 | Historical record | Apache release page | H/P |
| Maintenance implementation can exist while maintenance admission is disabled | Engineering reconstruction | bounded synthesis of issue + source diff | E |
| Scanner admission is distinct from cursor/progress persistence | Engineering reconstruction | HDFS-8681 compared with existing Case 83 cursor evidence | E |
| Same retained config token can have different effective meaning across release versions | Engineering reconstruction | bounded `0` semantics comparison | E |
| Configuration-meaning retention is a general property of software | Philosophical/general claim | not established | rejected |

---

## Source custody / quality

### Apache JIRA HDFS-8681

First-party Apache project issue record. It supplies affected/fix versions, priority, issue linkage, maintainer comments, patch history, and integration references. It is stronger for project intent and regression classification than a third-party retrospective.

<https://issues.apache.org/jira/browse/HDFS-8681>

### Apache Hadoop commit `c6793dd8cc69ea994eb23c3e1349efe4b9feca9a`

First-party Apache source-history artifact. The inspected commit changes `DFSConfigKeys.java`, `BlockScanner.java`, `hdfs-default.xml`, a test setup, and `CHANGES.txt`.

<https://github.com/apache/hadoop/commit/c6793dd8cc69ea994eb23c3e1349efe4b9feca9a>

### Apache Hadoop 2.7.1 release page

First-party Apache release announcement dated 6 July 2015.

<https://hadoop.apache.org/release/2.7.1.html>

### Apache Hadoop 2.7.1 documentation

First-party release documentation identifies the published documentation as Hadoop 2.7.1 and provides the stable post-fix release context.

<https://hadoop.apache.org/docs/r2.7.1/>

---

## Related-repository routing

A fresh search of `tmzncty/computing-archaeology` for `BlockScanner` found no dedicated packet to reuse.

Accordingly this evidence record keeps only the retention-specific seam:

```text
verification mechanism exists
    -> configuration admits or suppresses it
    -> coverage work occurs or does not occur
    -> integrity currentness can later be renewed or remain stale
```

A full history of HDFS-7430, `DataBlockScanner`→`BlockScanner` rewrite lineage, branch-by-branch configuration compatibility, release engineering, or GFS/Nutch/HDFS scanner genealogy should live primarily in `computing-archaeology` and be linked back rather than duplicated here.

---

## Remaining debt after this slice

This packet closes the narrow **2.7.0 default-disable → 2.7.1 repaired-default** boundary. It does not close:

- exact source archaeology of the pre-HDFS-7430 `DataBlockScanner` configuration semantics across every 2.x branch;
- empirical evidence from real 2.7.0 deployments showing how often operators overrode the default;
- end-to-end fault injection measuring how long a disabled scanner delays latent-corruption discovery;
- post-2018 `BlockScanner` / `VolumeScanner` evolution;
- filesystem/power-loss durability of scanner cursor files;
- device-layer ECC/scrub interactions beneath HDFS;
- correlated corruption across all replicas.

Those are independent slices. No maturity promotion is required: Case 83 remains `grounded`.