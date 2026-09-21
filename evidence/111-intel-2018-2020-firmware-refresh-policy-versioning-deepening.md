# Case 111 Deepening — Intel SSD Firmware Revision Histories and Refresh-Policy Versioning, 2018–2020

## Scope

This packet deepens **Case 111 — Enterprise SSD Extended Shutdown** at a narrower layer than the operator runbooks and earlier powered-refresh prior art already in the repository.

The bounded question is:

> **Can a named SSD family keep the same product identity while a later firmware revision explicitly changes its NAND refresh policy?**

The answer is yes for the evidence inspected here. Intel's surviving first-party firmware revision histories explicitly record later firmware revisions that **improve** or **optimize** NAND refresh algorithms for several named SSD families. This is useful because it establishes that the retention-maintenance policy is not fixed solely by NAND generation, product family, or model name.

This packet does **not** establish the internal refresh algorithm, its thresholds, its traversal order, its persistence semantics, or the magnitude of the retention improvement.

Current Case 111 maturity remains **`grounded`**.

## Why this slice belongs in `technical-retention`

Case 111 already separates:

```text
media condition
    -> device-local maintenance admission
    -> maintenance execution
    -> maintenance progress / completion
    -> operator policy
```

This packet adds a missing versioning layer:

```text
named product
    + firmware revision / implementation epoch
    -> concrete device-local maintenance policy
```

The relevant retention relation is therefore not simply:

```text
product model
    -> one timeless refresh behavior
```

but potentially:

```text
product model
    + firmware revision
    -> refresh-policy implementation
```

That is a technical-retention question because later claims about what a powered SSD does cannot safely ignore the policy-bearing firmware version.

---

## Source ledger

### S1 — Intel SSD 540s Series product brief

**Source:** Intel, *Intel® Solid State Drive 540s Series*, product brief, document `333967-003US`, printed `0318/RA/JL`, copyright 2018.

URL:

<https://www.intel.com/content/dam/www/public/us/en/documents/product-briefs/ssd-540s-series-brief.pdf>

Directly inspected facts used here:

- model family: **Intel SSD 540s Series**;
- NAND: **16 nm NAND Flash Memory, Tri-Level Cell (TLC)**;
- SATA 6 Gb/s product family;
- the brief describes the 540s as the first TLC-based drive in Intel's SSD 5 Series family.

Evidence role:

- named-product and substrate identity;
- not firmware-behavior evidence by itself.

### S2 — Intel Memory and Storage Tool CLI release notes

**Source:** Intel, *Intel® Memory and Storage Tool — CLI*, Release Notes, document `342335-013US`, September 2021.

URL:

<https://downloadmirror.intel.com/647001/CLI-Intel-MAS-1.10-v2-Release-Notes-342335-013.pdf>

This later first-party release-note document preserves historical per-product firmware revision tables. Relevant entries include:

- **Intel SSD 540s** — July 2020 — firmware `043C/017C` — “Optimizations for NAND data refresh algorithms”;
- **Intel SSD Pro 5400s** — July 2020 — firmware `043P/017P` — the same refresh-optimization wording plus a security-vulnerability mitigation in the preserved revision history;
- **Intel SSD Pro 5450s** — October 2018 — firmware `LHF004P/LHF0B2P` — “Improved NAND data refresh algorithms”, alongside improved unsafe-shutdown recovery and other firmware-policy changes;
- **Intel SSD 760p** — September 2018 — firmware `004C` — “Improved NAND refresh algorithms”.

Evidence role:

- first-party historical revision ledger for named firmware changes;
- not source-code or controlled-test evidence;
- the 2021 document is a later preserved revision history, not itself proof that the 2018 or 2020 text was published on exactly the historical revision date.

### S3 — Intel SSD 545s product brief

**Source:** Intel, *Intel® Solid State Drive 545s Product Brief*.

URL:

<https://www.intel.com/content/dam/www/public/us/en/documents/product-briefs/ssd-545s-brief.pdf>

Directly inspected facts used here:

- model: **Intel SSD 545s**;
- nonvolatile media: **Intel 3D NAND technology, 64-layer, TLC**.

Evidence role:

- demonstrates that Intel's 2018 refresh-algorithm revision language is not confined to the older 16 nm planar-TLC 540s generation;
- this packet does not infer identical algorithms across 540s, 545s/5450s, or 760p.

### S4 — Intel SSD 760p product brief

**Source:** Intel, *Intel® Solid State Drive 760p Series Product Brief*.

URL:

<https://www.intel.com/content/dam/www/public/us/en/documents/product-briefs/ssd-760p-product-brief.pdf>

Directly inspected facts used here:

- model family: **Intel SSD 760p Series**;
- NAND: **64-layer TLC Intel 3D NAND**;
- PCIe Gen3 x4 / NVMe product family.

Evidence role:

- controlled cross-family context for the September-2018 `004C` refresh-algorithm revision entry;
- not proof that the SATA and NVMe families share a controller or common refresh implementation.

---

# 1. Historical / documentary record

## H1 — the 540s substrate identity is stable enough to make firmware revision a separate variable

Intel's 2018 product brief identifies the 540s as a named product family using **16 nm TLC NAND**.

The later Intel MAS release-note ledger does not rename the product into a different family when it records the July-2020 firmware change. It records a new firmware revision inside the **Intel SSD 540s Revision History**:

```text
July 2020
043C/017C
Optimizations for NAND data refresh algorithms
```

The directly supported historical relation is therefore:

```text
same named product family
    + later firmware revision
    -> explicitly changed NAND refresh algorithm/policy
```

This is stronger than a generic statement that “newer SSD generations use different refresh.” Here the revision history says that the maintenance behavior changed **within a named family lineage**.

It does not establish how many physical 540s hardware revisions existed under that family name, nor whether every capacity or bill-of-materials variant behaved identically.

## H2 — the 2020 540s update is not merely a security-only release-note entry

The July-2020 540s revision entry specifically names **NAND data refresh algorithms**.

That matters because firmware updates can contain unrelated host-interface, security, power-management, or logging changes. The source itself names the retention-maintenance domain rather than requiring us to infer it from a generic “reliability improvements” phrase.

Direct documentary claim:

```text
firmware 043C/017C
    -> refresh-algorithm optimization is an explicitly named change
```

Not directly documented:

```text
what threshold changed
what scan interval changed
what error metric changed
what page/block selection changed
what rewrite/relocation primitive changed
whether scan progress became more persistent
whether powered dwell required for completion changed
```

## H3 — Intel recorded similar refresh-policy changes on other SSD families in 2018

The preserved Intel revision histories record several 2018 examples:

### Intel SSD Pro 5450s

October 2018 firmware `LHF004P/LHF0B2P` includes:

- improved SMART E8/E9 implementation;
- **improved NAND data refresh algorithms**;
- improved SSD recovery flows from unsafe shutdown scenarios;
- firmware-policy optimizations around NAND-block retirement, media-page-count changes during power-state transitions, and E2E-error flows during secure erase.

This list is useful because Intel itself groups refresh changes with other controller-policy changes rather than describing refresh as immutable media physics.

### Intel SSD 760p

September 2018 firmware `004C` includes **improved NAND refresh algorithms** among other firmware changes.

Intel's product brief identifies this as a 64-layer TLC 3D NAND NVMe family.

The narrow historical conclusion is:

> Intel's surviving first-party revision histories explicitly record NAND-refresh-algorithm changes across more than one product family and interface context.

This packet does **not** infer one shared algorithm from the repeated wording.

## H4 — the revision-history source has its own chronology boundary

The main revision ledger inspected here is Intel's September-2021 MAS release-notes document. It preserves older 2018 and 2020 rows.

Therefore:

```text
revision-history row says “October 2018”
    !=
this exact 2021 PDF existed in October 2018
```

The source is first-party retrospective release history. It supports the existence and dating of the firmware revision entry as Intel later recorded it, but this packet does not claim to have archived the exact contemporaneous 2018 release-note artifact for every row.

This distinction matters because Case 111 already treats:

```text
implementation chronology
    !=
documentation chronology
    !=
publication chronology
```

as separate evidence questions.

---

# 2. Engineering reconstruction

The following are repository engineering reconstructions. They are not Intel vocabulary unless explicitly quoted above.

## E1 — product identity is not sufficient to identify retention-maintenance behavior

The 540s evidence directly blocks the shortcut:

```text
model == Intel SSD 540s
    -> therefore one timeless refresh policy
```

A safer relation is:

```text
product identity
    + firmware revision
    -> implementation epoch
    -> retention-maintenance policy
```

Project term used here:

- **implementation epoch** — a bounded interval in which a particular firmware revision is treated as the relevant policy-bearing implementation for a named product.

This term is not Intel historical vocabulary.

## E2 — firmware version belongs in any serious retention reproducer

Suppose two tests use drives carrying the same model label, but one has pre-July-2020 540s firmware and the other has `043C/017C`.

The release history itself tells us not to assume that their NAND-refresh behavior is equivalent.

Therefore a retention reproducer should capture, at minimum:

```text
model / family
capacity / form factor where relevant
firmware revision
NAND generation if known
power history
workload / wear state
thermal condition
observation method
```

This is not a claim that firmware revision dominates all other variables. It is a claim that the source proves firmware revision can be one of the variables that matters.

## E3 — installing newer firmware is not the same event as refreshing existing payload

The release note documents a policy-bearing firmware change.

It does not say that the act of installing `043C/017C` immediately rewrites all user data.

Therefore:

```text
firmware update installed
    !=
all existing payload refreshed
```

and:

```text
new refresh policy available
    !=
new refresh policy has run over all relevant media
```

For Case 111 this is especially important because operator guidance is about **maintenance opportunity and completion**, not only about possession of code capable of maintenance.

## E4 — changed refresh code does not reveal changed maintenance-completion semantics

The release history names an algorithm optimization but does not describe:

- whether refresh work is resumable after interruption;
- whether a cursor/checkpoint is persisted;
- whether work restarts from the beginning;
- whether eligibility is reconstructed from current ECC/media state;
- whether completion is externally observable;
- how the controller treats reset or unsafe shutdown during the pass.

Thus:

```text
refresh algorithm changed
    !=
restart semantics disclosed
```

and:

```text
refresh algorithm changed
    !=
completion telemetry disclosed
```

This leaves Case 111 debt #3 and #6 substantially open.

## E5 — firmware policy drift and NAND-generation drift are different variables

The evidence index previously framed one open problem as “later NAND-generation drift.” The Intel evidence shows why that wording is too coarse.

At least two dimensions can move independently:

```text
A. substrate / NAND generation changes
B. firmware maintenance policy changes
```

The 540s row is especially valuable because it establishes dimension B without requiring a new named product family.

Across families, Intel also records refresh-algorithm changes on later 3D-NAND products, but this does not tell us whether those changes were caused by NAND generation, controller revision, field failures, qualification learning, power-management interactions, or another factor.

Therefore:

```text
later NAND generation
    !=
causal explanation for later refresh firmware
```

## E6 — an operator schedule cannot be back-derived from a firmware release note

IBM and Dell's later extended-shutdown guidance provides operator-facing powered intervals. Intel's firmware release notes do not.

So:

```text
refresh algorithm improved
    !=
operator must power drive for N days
```

and:

```text
firmware policy changed
    !=
field shutdown cadence changed
```

A direct bridge would require evidence connecting a specific firmware revision to a measured maintenance duration, measured retention margin, or revised operator recommendation.

That bridge is currently absent.

---

# 3. Controlled functional comparison

These comparisons are functional only. They do not assert shared implementation ancestry.

## F1 — comparison with the earlier Coulson power-up scan packet

The prior Case 111 packet on `US20090327581A1` gives a public SSD-specific mechanism in which power-up can admit a background scan and current correctable-error burden can trigger rewrite/relocation.

The Intel 2018–2020 release histories give later **named-product firmware revision evidence** that NAND refresh algorithms changed.

The useful comparison is:

```text
Coulson patent disclosure
    -> mechanism-level public prior art

Intel revision histories
    -> named-product firmware-policy change evidence
```

What is still missing is the historical bridge:

```text
Coulson mechanism
    -> specific named Intel shipping product implementation
```

The shared Intel connection is not enough.

```text
same / related assignee history
    !=
implementation genealogy
```

This packet therefore **does not close** the Case 111 “Intel implementation bridge” debt.

## F2 — comparison with Seagate product-manual evidence

The early Seagate Pulsar evidence says powered firmware/hardware can monitor and refresh memory cells.

The Intel revision histories show that a later named product family's refresh algorithm can itself change with firmware revision.

Functional relation:

```text
device-local maintenance exists
    !=
device-local maintenance is timeless
```

No claim is made that Seagate and Intel use the same trigger, ECC metric, traversal, relocation policy, or progress semantics.

## F3 — comparison with Case 43 AVATAR

Case 43 demonstrates, at the research-architecture level, that a refresh decision can depend on mutable policy state such as a Row Refresh Table.

Case 111 here supplies a different layer:

```text
Case 43:
mutable data structure participates in refresh classification

Case 111 / Intel:
firmware revision itself changes the implementation of NAND refresh policy
```

The controlled analogy is that **maintenance policy is mutable stateful infrastructure**.

There is no historical genealogy claimed between AVATAR and Intel SSD firmware.

## F4 — comparison with operator runbooks

The IBM/Dell runbook layer asks whether enough powered opportunity has been given for maintenance.

The Intel firmware layer shows that “maintenance” is not necessarily a single fixed implementation even for one family.

Therefore a future field study should avoid treating:

```text
same number of powered hours
    -> same maintenance work
```

as an invariant across firmware revisions without direct evidence.

This is a methodological warning, not a demonstrated measured difference in powered dwell time.

---

# 4. Philosophical interpretation

This section is deliberately interpretive rather than historical.

## P1 — retention depends on policy-bearing machinery, not only on the retained substrate

A NAND array can remain physically the same named product class while its maintenance behavior changes because firmware changes.

For the repository's larger question, this suggests:

> What lets a state outlive the event that produced it can include a mutable policy layer that decides when the substrate should be re-observed, corrected, rewritten, or relocated.

The payload's persistence is therefore partly dependent on another state-bearing object: firmware and its policy.

This is a repository interpretation, not Intel's historical language.

## P2 — “the same drive” can hide a changed retention contract

At ordinary inventory granularity two devices may be called the same model. At technical-retention granularity they can belong to different implementation epochs if firmware changes refresh behavior.

That gives a useful distinction:

```text
inventory identity
    !=
retention-policy identity
```

Again, this is a project abstraction, not a vendor term.

---

# 5. Explicit non-claims

This packet does **not** claim any of the following:

1. that Intel invented NAND refresh;
2. that the 540s was Intel's first SSD with refresh firmware;
3. that July 2020 was the first time the 540s ever performed refresh;
4. that the pre-2020 540s refresh implementation was defective;
5. that `043C/017C` rewrites every LBA or physical page;
6. that installing `043C/017C` itself refreshes existing payload;
7. that the release note exposes refresh thresholds;
8. that it exposes ECC trigger levels;
9. that it exposes traversal order;
10. that it exposes page/block selection;
11. that it exposes relocation versus in-place rewrite semantics;
12. that it exposes persistent maintenance progress;
13. that it exposes completion telemetry;
14. that it exposes power-interruption behavior;
15. that “optimization” proves a quantified retention improvement;
16. that the 2018 and 2020 changes were caused by a particular field failure;
17. that planar TLC necessarily needs a different algorithm from 3D TLC;
18. that NAND generation alone explains the firmware changes;
19. that all Intel SSD families share one refresh implementation;
20. that repeated release-note wording proves shared controller code;
21. that SATA and NVMe products share a refresh scheduler;
22. that the Intel 2018–2020 firmware is an implementation of Coulson's patent;
23. that assignee continuity proves technical genealogy;
24. that a firmware revision changes IBM or Dell operator schedules;
25. that a changed algorithm changes required powered dwell time;
26. that the 2021 Intel MAS release-note PDF is a contemporaneous 2018 artifact;
27. that every capacity or hardware BOM under one model label is identical;
28. that a product brief proves firmware internals;
29. that release-note claims are independent experimental validation;
30. that Case 111 should be promoted beyond `grounded` from this packet alone.

---

# 6. Resulting evidence graph

The new bounded graph is:

```text
NAND / media condition
    ↓
firmware revision / implementation epoch
    ↓
refresh-policy implementation
    ↓
maintenance admission / selection
    ↓
rewrite / relocation / other renewal action
    ↓
progress / completion state
    ↓
future retention margin
```

Only the upper **firmware-revision -> refresh-policy-change** edge is directly strengthened by this packet.

The downstream edges remain implementation questions unless independently documented.

A second graph captures the historical comparison:

```text
2009-public Coulson mechanism
    -> public SSD refresh prior art
    X
    -> named Intel product implementation not yet proven

2018 Intel named families
    -> explicit firmware revision says refresh algorithm improved

2020 Intel 540s
    -> explicit firmware revision says refresh algorithm optimized
```

The `X` is deliberate: this packet does not manufacture the missing genealogy bridge.

---

# 7. What this closes and what remains open

## Partially closed

The evidence-index debt previously called **later NAND-generation drift** can now be split more precisely.

This packet establishes:

```text
firmware maintenance-policy drift exists
```

for named Intel SSD revision histories.

It therefore closes the weaker question:

> Can retention-maintenance policy change without changing the inventory-level product-family name?

Yes, at least at the release-note level.

## Still open

Higher-value follow-up questions are now narrower:

1. **Measured effect** — connect a named refresh-policy firmware revision to controlled before/after retention-margin or error-rate measurements.
2. **Operator effect** — determine whether a named firmware revision changed a vendor's recommended powered dwell or shutdown cadence.
3. **Progress semantics** — determine whether the firmware persists, reconstructs, or discards refresh-scan progress across reset / unsafe shutdown.
4. **Completion telemetry** — identify any device-local log, SMART field, vendor log page, or service command that proves a refresh pass completed.
5. **Implementation bridge** — connect Coulson's public Intel-assigned mechanism to a named shipping implementation, or preserve the absence of such proof.
6. **Hardware-revision control** — determine whether one model/firmware label spans NAND or controller substitutions relevant to refresh behavior.

---

# 8. Status decision

**No maturity promotion.**

Case 111 remains **`grounded`**.

The packet adds named-product firmware-version evidence and improves the case's control-variable model, but it does not provide independent measurement, firmware internals, restart semantics, or a direct operator-schedule bridge.

The most useful new guardrail is:

```text
same product family
    !=
same retention-maintenance policy
```

and the corresponding research requirement is:

```text
retention evidence for an SSD
    should record firmware revision
```

when the claim depends on controller-local maintenance behavior.
