# Case 150 deepening — Linux 2014 M550 blacklist identity coverage and workaround enforcement

## Scope

This addendum deepens [`../cases/150-crucial-m550-active-garbage-collection.md`](../cases/150-crucial-m550-active-garbage-collection.md) at one narrow seam:

> **What happens when the host has already retained a safety rule for a known-bad maintenance command path, but its device-identity classifier fails to recognize one affected member of the product family?**

The bounded evidence is:

1. upstream Linux commit `d121f7d0cbb875abce249dbf7eb191f9bafe80b7`, 2 April 2014, which explicitly adds M550 entries to the queued-TRIM blacklist while a firmware fix is still pending;
2. upstream Linux commit `2a13772a144d2956a7fedd18685921d0a9b8b783`, 18 August 2014, which changes the Crucial M550 model pattern because the existing three-character capacity match does not cover the 1 TB / `1024` model string;
3. the Ubuntu bug/archive record for bug 1363462, which preserves a field report from an owner of a `Crucial_CT1024M550SSD1` / MU01 device and the downstream test-kernel/SRU discussion around the upstream fix;
4. the already-established 27 March 2015 Linux update `ff7f53fb82a7801a778e5902bdbbc5e195ab0de0`, used only as a later boundary showing that the blacklist eventually becomes firmware-qualified after MU02.

This is **not** an attempt to reverse-engineer the M550 controller, prove the exact internal NCQ-TRIM corruption mechanism, or turn one bug report into a controlled hardware experiment. The slice is about **compatibility-policy applicability**: retained host knowledge is useful only if runtime identity matching selects the rule for the device actually present.

---

## Source custody and evidence class

### Upstream Linux commits

The two principal sources are immutable upstream Linux commit records and diffs in `drivers/ata/libata-core.c`.

They are primary software-history evidence for:

- what libata maintainers believed the command-path risk to be;
- what blacklist predicate they encoded;
- what exact matching defect they later corrected;
- which safety flag was attached to a matching device.

They are **not** primary evidence for the proprietary firmware's transistor-level or FTL-level failure mechanism.

### Ubuntu / Launchpad mailing-list preservation

The Launchpad bug itself is not reliably fetchable through every current interface, but its notification stream is preserved in public Ubuntu/kernel-package mailing-list archives. The preserved bug description says the reporter owned a 1 TB M550 that experienced data loss when using NCQ TRIM and that the then-current Trusty blacklist failed to match the 1024 GB model because the capacity field was wider than the pattern expected.

That material is valuable as a contemporaneous operational report and downstream-integration record. It is weaker than a controlled reproducer because the surviving report does not provide a complete workload, command trace, media image, or firmware-internal diagnosis.

A later November 2014 participant report in the same bug thread shows `Crucial_CT1024M550SSD1, MU01` being recognized with `disabling queued TRIM support`, but also reports separate `WRITE FPDMA QUEUED` / link-reset problems that required disabling NCQ entirely. That later report is therefore **not** treated as proof that the queued-TRIM blacklist solved every M550/controller failure mode.

---

## Historical record

### H/P — by 2 April 2014 Linux carried explicit M550 queued-TRIM distrust

Upstream commit `d121f7d0cbb875abce249dbf7eb191f9bafe80b7`, authored by Martin K. Petersen and committed by Tejun Heo on 2 April 2014, is titled:

`libata: Update queued trim blacklist for M5x0 drives`

Its commit message says that early M550 drives suffer from the same queued-TRIM issue as the M500 line and that a bug-fix firmware is in the pipeline but not yet ready. The patch adds:

```c
{ "Micron_M550*",          NULL, ATA_HORKAGE_NO_NCQ_TRIM, },
{ "Crucial_CT???M550SSD*", NULL, ATA_HORKAGE_NO_NCQ_TRIM, },
```

The relevant historical point is already stronger than a later retrospective support article:

> **By April 2014, upstream libata had an explicit product-family safety rule withholding queued TRIM from M550 devices.**

The source does not explain the proprietary firmware defect beyond the command-path symptom/risk class.

### H/P — the original Crucial predicate encoded a fixed-width capacity assumption

The Crucial matcher used three literal wildcard positions between `CT` and `M550SSD`:

```text
Crucial_CT???M550SSD*
```

That matches three-character capacity fields such as common `128`, `256`, or `512` forms, but it does not match a four-character `1024` capacity field.

The important fact is not inferred from glob theory alone. The later upstream fix says exactly why the predicate was wrong: the 1 TB model's capacity section is four characters rather than three.

Thus the compatibility state had two separable parts:

```text
policy payload:
    M550 queued TRIM is unsafe -> do not use queued TRIM

applicability predicate:
    which runtime model strings are members of that affected class?
```

The first could be correct while the second was incomplete.

### H/P — 18 August 2014 changes only the identity predicate

Upstream commit `2a13772a144d2956a7fedd18685921d0a9b8b783`, authored and committed by Tejun Heo on 18 August 2014, is titled:

`libata: widen Crucial M550 blacklist matching`

The commit message states that the M550 may cause data corruption on queued TRIM, that it is already blacklisted, and that the existing pattern fails to match the 1 TB unit because its capacity section has four characters.

The code change is only:

```diff
- { "Crucial_CT???M550SSD*", NULL, ATA_HORKAGE_NO_NCQ_TRIM, },
+ { "Crucial_CT*M550SSD*",   NULL, ATA_HORKAGE_NO_NCQ_TRIM, },
```

No new device-safety theory is introduced in this patch. The rule already existed. The correction widens the **recognition relation** that determines where the rule applies.

This is a unusually clean source-level boundary:

```text
known safety policy
    !=
complete identity coverage for that policy
```

### H/P* — downstream field report identifies the uncovered 1 TB model

Ubuntu bug 1363462 preserves the report that a Crucial/Micron M550 1 TB SSD experienced data loss when NCQ TRIM was used and that the Trusty blacklist missed this size because the model-pattern capacity field assumed three digits.

The report points directly to upstream commit `2a13772...` and asks for a kernel containing the corrected matcher so installation does not proceed with the unsafe queued-TRIM path enabled.

Ubuntu kernel maintainers then built a Trusty test kernel with the upstream change and tracked it for stable integration.

This record corroborates that the wildcard bug was not merely a theoretical string-matching concern: it mattered to whether the host selected a protective command policy for a shipping model string.

The surviving field report still does **not** establish a minimal reproducer or the firmware-internal cause of the corruption.

### H/P* — later reports show why the workaround boundary must remain narrow

A later participant in the same Ubuntu thread reported two `Crucial_CT1024M550SSD1` / MU01 drives with log lines showing:

```text
ata*.00: disabling queued TRIM support
```

That confirms the widened policy could recognize the 1 TB model and disable queued TRIM.

However, the same participant also reported `WRITE FPDMA QUEUED` bus errors, hard link resets, RAID1 repair/resync symptoms, and eventual relief only after disabling NCQ generally.

Therefore this evidence must **not** be summarized as:

```text
M550 failure == queued TRIM only
```

or:

```text
NO_NCQ_TRIM workaround == proof all M550 data-integrity hazards are gone
```

It instead supplies a useful negative boundary: one compatibility rule can correctly mitigate one command-path class while other controller/device/link problems remain possible.

### H/P — later MU02 changes the applicability relation again

The existing Case-150 firmware deepening already records upstream commit `ff7f53fb82a7801a778e5902bdbbc5e195ab0de0` from 27 March 2015. Linux maintainers state that Micron released MU02 for M510/M550/MX100 to fix queued-TRIM issues and narrow the M550 workaround to MU01.

So the history becomes:

```text
April 2014:
    family-level M550 queued-TRIM distrust

August 2014:
    fix incomplete model-string coverage for 1 TB Crucial M550

March 2015:
    narrow M550 distrust by firmware revision after MU02
```

This is not a single static blacklist fact. It is a changing host-side compatibility relation over **model identity × firmware identity × command path**.

---

## Engineering reconstruction

### E — retained compatibility knowledge has an applicability relation

The earlier Case-150 deepening established that host software can retain compatibility knowledge such as:

```text
M550 + MU01
    -> do not use queued TRIM
```

The 2014 matcher defect shows that this knowledge is not operational merely because it exists in source code.

A more complete model is:

```text
retained compatibility rule
    + runtime device identity
    + classifier/matcher
    -> selected workaround state
    -> command-path admission
```

If the classifier maps an affected device outside the rule's domain, the safety knowledge is present but causally inert for that instance.

Therefore:

> **policy retention != policy applicability != policy enforcement.**

### E — an identity schema can become part of the safety boundary

The original wildcard encoded an assumption about how capacity was represented inside the model string. Moving from three-digit capacities to `1024` changed no queued-TRIM semantics by itself, but it changed whether the host recognized the device as belonging to the guarded family.

Thus an apparently cosmetic naming convention can become operationally significant when software uses that string as a compatibility key.

The bounded rule is:

```text
same engineering family
    !=
same syntactic identity shape

same safety requirement
    !=
automatically selected safety policy
```

This does not imply that model strings are intrinsically authoritative hardware identities. It shows only that libata used them as a practical classification key in this path.

### E — safety knowledge can fail by under-coverage without being false

The August patch did not reverse the proposition that queued TRIM was unsafe for early M550 units. Instead, it corrected the set of device strings to which that proposition was applied.

That gives a useful distinction for technical-retention work:

```text
false policy
    = retained rule itself is wrong

stale policy
    = rule was once appropriate but no longer matches current behavior

under-covered policy
    = rule may be correct where applied,
      but some affected instances fail to enter its domain
```

Case 150 now contains examples of both under-coverage and later staleness/overbreadth pressure:

- August 2014 widens coverage to include a missed 1 TB model;
- March 2015 narrows coverage because MU02 changes the relevant firmware behavior.

So compatibility maintenance is not simply additive. A safe table may need both widening and narrowing over time.

### E — guard selection is separate from the guarded operation

The blacklist is host-side control state about whether queued TRIM should be used. It is not the TRIM command itself, the deallocation relation, garbage collection, or physical erase.

The fuller chain is:

```text
host knows deallocation is possible
    ↓
host identifies model / firmware
    ↓
host compatibility policy admits or rejects queued TRIM path
    ↓
if admitted, retirement information may be transmitted
    ↓
controller may later use that information in reclamation
```

A failure in identity matching therefore occurs **before** the managed-SSD reclamation stages developed elsewhere in Case 150.

### E — mitigation success and root-cause diagnosis are different evidence tasks

A blacklist can be justified operationally before firmware internals are publicly known. Conversely, observing that a blacklist prevents one dangerous command path does not reveal whether the proprietary defect lies in queue ordering, DSM range parsing, error recovery, mapping publication, FTL metadata, DMA handling, or some other internal mechanism.

The current evidence supports:

```text
queued-TRIM path distrusted
    + affected device missed by matcher
    + matcher widened
```

It does **not** support:

```text
exact proprietary corruption mechanism reconstructed
```

That distinction keeps workaround history from being over-promoted into firmware archaeology.

---

## Controlled functional comparison

### A — Case 79 HDFS SafeMode: policy existence versus enforcement-surface coverage

[`../cases/79-apache-hdfs-startup-safemode-reobservation.md`](../cases/79-apache-hdfs-startup-safemode-reobservation.md) supplies a useful software-level comparison. HADOOP-3002 showed that a SafeMode policy could exist while one block-report command-emission path did not enforce the same destructive-operation guard as the heartbeat path.

Case 150 is structurally similar only at a high level:

```text
Case 79:
    safety policy exists
        != every destructive execution path is guarded

Case 150:
    compatibility policy exists
        != every affected runtime identity is classified into the guard
```

The comparison is about **coverage of a safety relation**, not shared implementation or genealogy.

### A — Case 118 / Case 10: policy state versus policy authority

DRAM cases such as Case 118 and Case 10 distinguish capability, current policy state, and which actor has authority to set maintenance behavior. Case 150 adds a different axis: a host may possess the policy and authority to withhold a command, yet still fail to apply it because device classification misses the target.

Thus:

```text
policy represented
    != policy selected
    != policy effective
```

Again, this is a functional comparison only.

---

## Philosophical interpretation

### I — retained knowledge is not operational knowledge until it is bound to the right referent

The technical fact is narrow: Linux contained the relevant M550 safety rule, but one product-string form escaped the predicate that connected that rule to the physical device.

A cautious project-level interpretation is:

> **Retaining a true rule does not guarantee useful continuity if the system cannot correctly bind the rule to the present object.**

This is not a claim about human semantics, identity metaphysics, or representation in general. It is simply a reminder that technical retention often concerns relations rather than isolated values:

```text
rule
    + referent identity
    + applicability relation
    -> actionable control state
```

If the applicability relation is wrong, the retained rule can survive perfectly while the intended protection fails.

---

## Claim ledger

| Claim | Label | Evidence |
| --- | --- | --- |
| Linux explicitly blacklisted early M550 queued TRIM by April 2014 | `H/P` | upstream `d121f7d0...` |
| The Crucial matcher originally used exactly three wildcard characters for the capacity field | `H/P` | upstream `d121f7d0...` diff |
| Upstream later said this matcher missed the 1 TB model because `1024` uses four characters | `H/P` | upstream `2a13772a...` commit message |
| The August 2014 fix widened the identity pattern without changing the `NO_NCQ_TRIM` policy flag | `H/P` | upstream `2a13772a...` diff |
| A contemporaneous Ubuntu report tied the missed `CT1024M550SSD1` class to data loss under NCQ TRIM | `H/P*` | Ubuntu bug 1363462 archive |
| The downstream thread proves a minimal, repeatable firmware-internal reproducer | `X` | surviving report lacks that evidence |
| The queued-TRIM blacklist fixes every M550 NCQ/controller failure mode | `X` | later field report shows additional WRITE FPDMA / link-reset issues |
| MU02 later caused Linux to narrow M550 queued-TRIM distrust to MU01 | `H/P` | upstream `ff7f53fb...`, already grounded in prior Case-150 evidence |
| Retained compatibility policy and applicability predicate are separate control relations | `E` | reconstruction from the rule/pattern/fix sequence |
| Device naming strings are universally authoritative hardware identities | `X` | not established; they are only the key used by this libata matcher |
| Case 79 and Case 150 share a direct design genealogy | `X` | functional comparison only |

---

## Explicit non-claims

This addendum does **not** establish that:

1. Linux invented queued-TRIM compatibility blacklists;
2. the M550 was the first SSD with a queued-TRIM defect;
3. every M550 capacity used exactly the same firmware behavior;
4. every 1 TB M550 definitely corrupted data under every queued-TRIM workload;
5. the Ubuntu report is a controlled laboratory reproduction;
6. the report's later RAID1 repair proves queued TRIM was the sole cause;
7. `WRITE FPDMA QUEUED` errors in the later report are themselves TRIM commands;
8. disabling queued TRIM disables all NCQ;
9. disabling queued TRIM disables ordinary nonqueued TRIM;
10. the blacklist entry is evidence that all TRIM should be disabled;
11. the Linux model string is cryptographically authenticated device identity;
12. a wider wildcard can never over-match unrelated devices;
13. `Crucial_CT*M550SSD*` is a universally correct product taxonomy outside this historical code path;
14. the model matcher explains the proprietary firmware bug;
15. the exact M550 FTL mapping corruption sequence is known;
16. the exact NCQ queue-ordering bug is known;
17. a successful workaround proves root cause;
18. MU02 reached every fielded M550;
19. MU02 fixed every unrelated power, link, or NCQ issue;
20. a firmware-qualified rule eliminates the need for model qualification;
21. host compatibility state is SSD-internal mapping metadata;
22. blacklist matching is garbage collection itself;
23. preventing queued TRIM proves physical erase never occurs;
24. allowing nonqueued TRIM proves garbage collection immediately completes;
25. Case 79 and Case 150 implement the same guard mechanism;
26. one missed SKU implies the rest of the blacklist was wrong;
27. one correct rule implies all affected identities are correctly covered;
28. retained source code automatically implies effective runtime policy;
29. compatibility tables are complete historical archives of every observed failure;
30. this slice closes controlled MU01-vs-MU02 hardware validation or proprietary failure-mechanism archaeology.

---

## What this closes

This addendum closes one bounded Case-150 evidence debt:

> **The 2014 Linux M550 workaround did not merely evolve by firmware revision; it also suffered an identity-coverage defect in which the safety rule existed but a 1 TB Crucial model string escaped the matcher.**

It therefore adds the relation:

```text
compatibility knowledge retained
    !=
correct referent coverage
    !=
workaround selected
    !=
unsafe command path actually withheld
```

The exact proprietary queued-TRIM corruption mechanism remains open.

---

## Remaining evidence debt

- recover the original kernel Bugzilla 81071 body/attachments if a stable archival copy becomes available;
- find a controlled minimal M550 MU01 queued-TRIM reproducer rather than relying on operational field reports;
- controlled MU01 vs MU02 hardware tests;
- power-cut fault injection during garbage collection;
- exact GC transaction/progress recovery after interruption;
- exact victim-selection / live-page publication ordering;
- raw-NAND observation of stale embodiments before and after reclaim;
- broad libata blacklist/model-string genealogy belongs primarily in `tmzncty/computing-archaeology`.

---

## Sources

1. Linux upstream commit `d121f7d0cbb875abce249dbf7eb191f9bafe80b7`, **libata: Update queued trim blacklist for M5x0 drives**, 2 April 2014: <https://github.com/torvalds/linux/commit/d121f7d0cbb875abce249dbf7eb191f9bafe80b7>.
2. Linux upstream commit `2a13772a144d2956a7fedd18685921d0a9b8b783`, **libata: widen Crucial M550 blacklist matching**, 18 August 2014: <https://github.com/torvalds/linux/commit/2a13772a144d2956a7fedd18685921d0a9b8b783>.
3. Ubuntu / Launchpad bug 1363462 notification archive, **Crucial M550 1TB SSD missing from NCQ TRIM blacklist**, contemporaneous 2014 thread preserved by public mailing-list archives: <https://www.mail-archive.com/search?f=1&l=kernel-packages%40lists.launchpad.net&o=newest&q=subject%3A%22%5BKernel-packages%5D%20%5BBug%201363462%5D%22>.
4. Linux upstream commit `ff7f53fb82a7801a778e5902bdbbc5e195ab0de0`, **libata: Update Crucial/Micron blacklist**, 27 March 2015: <https://github.com/torvalds/linux/commit/ff7f53fb82a7801a778e5902bdbbc5e195ab0de0>.

### Source-boundary note

The upstream Linux commits are primary evidence for host-side compatibility policy and its matcher. The Ubuntu archive is contemporaneous field evidence, not a controlled hardware validation. None of these sources disclose the exact proprietary M550 firmware mechanism behind queued-TRIM corruption.