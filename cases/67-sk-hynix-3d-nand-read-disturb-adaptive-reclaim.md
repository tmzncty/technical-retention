# SK hynix 3-D NAND Read-Disturb Reclaim: Read-Count Proxies, Adaptive Thresholds, and Relocation

## Status

**`grounded`** — bounded to the manufacturer-primary controller design documented in SK hynix / SK hynix Memory Solutions America patent publication **US20190066809A1**, with priority dated 31 August 2017 and publication dated 28 February 2019. Earlier manufacturer-primary evidence includes a MegaChips 2007-priority / 2008-public thresholded read-disturb repair design plus Samsung 2009- and 2013-priority families. Named-product evidence now spans a 2018 PM963 `Lifetime read Reclaim count` witness and a 2024 PM9D3a telemetry schema that separately exposes `Lifetime read Reclaim count`, `Patrol Read Reclaim Count`, and OCP `Refresh Counts`; OCP primary specifications bound the last field to integrity-maintenance block reallocation rather than leaving it as an opaque product label.

Grounding record: [`../evidence/67-sk-hynix-2009-2019-read-reclaim-grounding.md`](../evidence/67-sk-hynix-2009-2019-read-reclaim-grounding.md).

Pre-2009 prior-art deepening: [`../evidence/67-megachips-2007-2008-read-disturb-rewrite-prior-art-deepening.md`](../evidence/67-megachips-2007-2008-read-disturb-rewrite-prior-art-deepening.md).

PM963 named-product telemetry deepening: [`../evidence/67-samsung-pm963-2016-2018-read-reclaim-telemetry-deepening.md`](../evidence/67-samsung-pm963-2016-2018-read-reclaim-telemetry-deepening.md).

PM9D3a maintenance-telemetry taxonomy deepening: [`../evidence/67-samsung-pm9d3a-maintenance-telemetry-boundary-deepening.md`](../evidence/67-samsung-pm9d3a-maintenance-telemetry-boundary-deepening.md).

OCP `Refresh Counts` semantics / background-refresh boundary: [`../evidence/67-2020-2025-ocp-refresh-count-semantics-deepening.md`](../evidence/67-2020-2025-ocp-refresh-count-semantics-deepening.md).

## Scope

This case asks a narrow question left open by Cases 52 and 65:

> What changes when a 3-D NAND controller treats **read activity and measured error margin as maintenance evidence**, adapts how often it tests potentially disturbed regions, and can preserve the logical payload by copying valid values into a new physical population before the old embodiment becomes uncorrectable?

The bounded object in US20190066809A1 is a composition of:

- a read-count proxy associated with a block/group of blocks;
- a read threshold that determines when to perform read-disturb checking;
- test reads of an associated or expanded region;
- ECC-derived bit-error evidence;
- adaptive read thresholds / error thresholds;
- a read-reclaim operation that copies valid values to other memory cells;
- clearing/resetting the read-count proxy after reclaim and, in the disclosed design, after power-off;
- 3-D neighborhood sampling that can include wordlines above and below the original read location.

This case additionally tracks **named-product maintenance telemetry** when it can be separated from the patent algorithm itself.

This is **not**:

- proof that a named commercial SK hynix SSD shipped the exact patented algorithm, threshold table, counter width, or persistence behavior;
- a generic history of NAND read disturb;
- a claim that SK hynix invented read reclaim, ECC-margin-triggered relocation, garbage collection, wear leveling, ECC, or 3-D NAND;
- evidence that a controller counter directly measures trapped charge or threshold-voltage shift;
- a claim that power-off physically resets read-disturb damage;
- a claim that read reclaim securely erases superseded physical cells;
- a claim that Samsung PM963 or PM9D3a implements the SK hynix patent;
- a claim that OCP `Refresh Counts` is physically identical to read reclaim, DRAM refresh, or Case 36 correct-and-refresh;
- a claim that OCP SMART-10 is exactly the event set produced by OCP's background-data-refresh requirement;
- a substitute for Case 52's physical read-disturb characterization or Case 65's retention-age-aware read-reference adaptation.

## Historical record

### Successful reads can create a future retention obligation outside the logical target

US20190066809A1 describes pass-bias read disturb: a read can succeed for the requested page while repeated accesses contribute stress to other cells in a larger physical region.

Therefore:

> **successful logical read ≠ absence of future retention debt**.

and:

> **logical read target ≠ complete physically stressed neighborhood**.

### The design retains a workload proxy rather than the physical condition itself

The patent discusses the storage cost of per-page counters and instead groups read activity under compressed counters/proxies. The read count records selected workload history under one policy; it is not the threshold-voltage distribution of the victim cells.

> **read-count proxy ≠ physical read-disturb state**.

### Threshold crossing qualifies inspection; it does not by itself prove failure or relocation need

The disclosed flow increments the relevant read count. At a threshold or multiple of a threshold, the controller performs a read-disturb test and derives bit-error evidence that can be compared with an error threshold.

Thus:

> **read-count threshold crossing ≠ uncorrectable payload**.

> **read-count threshold crossing ≠ automatic proof that relocation is required**.

The count schedules/qualifies further observation; the measured error state can decide whether reclaim should occur.

### Error evidence can change future maintenance cadence

The patent describes target read thresholds selected from bit-error evidence, including lookup-table forms in which higher error counts can lead to lower future read thresholds.

> **adaptive read threshold ≠ fixed physical failure limit**.

The threshold is controller policy about when to inspect again.

### Read reclaim can re-embody valid values

The claims define a read-reclaim operation capable of copying valid values from one plurality of cells to another. Other passages describe invoking reclaim/GC-like movement when read-disturb evidence warrants it.

> **ECC-correctable logical data ≠ data that must remain in the same cells**.

> **read reclaim relocation ≠ logical payload change**.

### The disclosed read-count proxy may be cleared at power-off

The patent explicitly permits clearing a read-count proxy after power-off and discusses avoiding NAND persistence for shorter counters when conservative post-reset checking compensates.

This establishes:

> **controller counter continuity ≠ medium damage continuity**.

and:

> **power-off-cleared maintenance proxy ≠ power-off-cleared read disturb**.

The controller may forget one compressed history variable while the physical cell state persists.

### 3-D geometry affects what should be sampled

The disclosed 3-D embodiment can test pages/wordlines above and below an original read location. This does not establish universal 3-D disturb geometry, but it does establish that maintenance sampling may be driven by physical adjacency beyond the host-visible page.

## Retained states and control state

At least seven separable states appear in the bounded design:

1. **logical payload** — the value the host expects to remain recoverable;
2. **physical cell state** — charge/threshold distributions whose margin can be altered by read disturb;
3. **logical-to-physical mapping** — needed if reclaim relocates current data;
4. **read-count proxy** — compressed workload-history state used to schedule checks;
5. **last-read / grouping information** — state used by some counter/sampling variants;
6. **bit-error / ECC evidence** — observed qualification of current recoverability margin;
7. **adaptive policy state** — target read threshold, error threshold, sampling factor, or lookup relation governing future maintenance.

These states do not share one lifetime. In the disclosed SK hynix design, the physical condition survives power-off while a read-count proxy may not.

Product telemetry adds another class:

8. **maintenance summaries** — cumulative or category-specific counters exposed to management software, such as Samsung's `Lifetime read Reclaim count`, `Patrol Read Reclaim Count`, and OCP SMART-10 `Refresh Counts`.

A management counter is not automatically the same state used internally to trigger maintenance. OCP also supplies a separate **background-refresh coverage obligation**: a device must maintain powered-on retention with whole-device background coverage, but the standard does not say the cumulative SMART-10 value itself is the coverage-control state.

## Engineering reconstruction

### A maintenance proxy may intentionally be less durable than the condition it protects against

Case 67 is a useful counterexample to the assumption that every risk-history variable must persist as long as the physical risk. The patented design trades counter-storage persistence against conservative checking and threshold policy.

> **maintenance-proxy lifetime can be shorter than physical-condition lifetime**.

This is design-specific, not permission to discard arbitrary metadata.

### ECC correction and physical renewal are separate acts

ECC can make the current read logically successful while error count indicates shrinking future margin. Reclaim can then copy valid values elsewhere.

> **current ECC correction ≠ future margin restoration**.

> **read reclaim ≠ ECC correction**.

### Read-reference adaptation and reclaim are different recovery loci

Case 65 shows read interpretation can be adapted according to retention age; Case 59 shows reference adaptation after interference. Those operations can recover a value from the same physical cells. Reclaim instead changes which cells carry the current value.

> **read-reference adaptation ≠ read-reclaim relocation**.

### Reliability-triggered reclaim is not the same as capacity-triggered garbage collection

The copy/erase machinery may overlap, but the reason for selecting work and the evidence authorizing it can differ.

> **reliability-triggered reclaim ≠ capacity-triggered garbage collection**.

OCP SMART-10 makes this separation explicit at the telemetry-contract level: it counts blocks re-allocated to maintain data integrity while excluding ordinary GC; later OCP wording also explicitly excludes wear-leveling relocation.

### Relocation is not sanitization

Preserving a value by copying it elsewhere does not prove physical removal of all superseded charge states.

> **read-reclaim relocation ≠ secure erase / sanitization**.

Cases 44 and 47 remain the forgetting/sanitization boundary.

### Maintenance telemetry is an accounting surface, not a recovered firmware state machine

The Samsung product and OCP evidence support a further distinction:

```text
maintenance work
    !=
maintenance trigger state
    !=
coverage-control state
    !=
maintenance accounting counter
    !=
complete maintenance history
```

A cumulative field can summarize completed work without exposing which blocks were involved, why an event was admitted, what ECC margin existed, how currentness changed during relocation, or whether the whole-device background-refresh coverage obligation is currently satisfied.

The OCP source narrows one previous ambiguity:

```text
SMART-10 Refresh Counts
    = standardized integrity-maintenance block-reallocation accounting
```

but still:

```text
standardized accounting semantics
    != vendor firmware algorithm
    != exact background-refresh event set
```

## Cross-case boundaries

### Versus Case 52 — NAND read disturb

Case 52 establishes the physical/access-induced regime. Case 67 adds a manufacturer-primary controller-policy slice:

```text
read activity
    -> compressed read-count proxy
    -> thresholded test-read schedule
    -> ECC/bit-error qualification
    -> adaptive future threshold
    -> conditional reclaim / relocation
```

The patent does not replace Case 52's characterization evidence or prove a shipped commercial implementation.

### Versus Case 65 — 3-D NAND early retention loss

Case 65 is principally elapsed-time / retention-age driven:

```text
program age + P/E state
    -> age-aware read reference
    -> improved interpretation of the same physical embodiment
```

Case 67 is principally read-workload / disturb driven:

```text
read-count proxy + measured bit errors
    -> inspection urgency
    -> conditional physical relocation
```

The two clocks can coexist but are not the same mechanism.

### Versus Case 36 — Flash Correct-and-Refresh

Case 36 studies retention-error correction and refresh/reprogram policy. Case 67 studies read-disturb pressure plus reclaim. Both can lead to renewed physical embodiment, but trigger and diagnostic relations differ.

The OCP primary specification now gives `Refresh Counts` a bounded semantics: blocks re-allocated to maintain data integrity, excluding ordinary GC and, in later wording, wear-leveling relocation. OCP v1.0 also separately requires powered-on background data refresh with whole-device coverage and continuous background service.

That is stronger than a terminology-only product label, but it still does not establish Case 36's exact mechanism or a one-to-one relation between SMART-10 increments and OCP background-refresh operations.

### Versus Case 04 — mapped Flash

Case 04 establishes logical identity surviving physical relocation under a mapping relation. Case 67 supplies a reliability-maintenance reason for relocation.

### Versus Case 59 — program interference

Program interference is write-induced neighbor coupling; read disturb is read-induced pass-voltage stress. Their commonality is functional only:

> an operation that succeeds for its logical target can alter the future reliability margin of another retained state.

## Failure and forgetting boundaries

Distinct failure or policy-failure modes include:

- read-count proxy underestimates relevant stress;
- grouping/sampling misses the most disturbed victim region;
- a threshold is too lax for actual error growth;
- power-off resets volatile proxy state and post-reset qualification is not conservative enough;
- ECC margin falls faster than scheduled checking anticipates;
- valid data cannot be recovered well enough to seed relocation;
- relocation/GC is interrupted or mapping/currentness handoff fails;
- reclaim consumes extra program/erase endurance;
- a controller confuses successful retry with sufficient future retention margin;
- a physical old embodiment survives logical relocation, so no secure-erasure implication follows;
- management counters lose or reset state in ways not disclosed by the telemetry table;
- whole-device background-refresh coverage falls behind even though a cumulative maintenance counter continues to increase;
- host tooling collapses distinct reclaim / patrol / refresh counters into one category and thereby obscures the maintenance contract.

These are not one generic `bit rot` mechanism.

## Named-product deepening — Samsung PM963 read-reclaim telemetry

Samsung's *DC Toolkit 2.1 User Guide* (initial release October 2018) lists PM963 as a supported SSD and shows PM963 reference output (`SAMSUNGNVMeSSDPM963`, firmware `CXV83M1Q`) whose Extended SMART fields include `Lifetime read Reclaim count`. Samsung separately identifies PM963 as a datacenter TLC V-NAND NVMe SSD and later states that the family launched in 2016.

This establishes named-product telemetry, not identity with the SK hynix patent implementation.

The evidence adds three boundaries:

> **named product exposes read-reclaim telemetry ≠ named product implements this patented reclaim algorithm**.

> **lifetime read-reclaim count ≠ per-block read-count proxy**.

> **cumulative maintenance count ≠ complete maintenance history**.

The inspected PM963 example value is zero; that is one reference-output state, not proof that the field/category is unsupported. The public field floor grounded by the inspected Toolkit source is October 2018, not the 2016 product-launch date.

See [`../evidence/67-samsung-pm963-2016-2018-read-reclaim-telemetry-deepening.md`](../evidence/67-samsung-pm963-2016-2018-read-reclaim-telemetry-deepening.md).

## Later named-product deepening — Samsung PM9D3a telemetry separates reclaim, patrol-reclaim, and refresh

A later Samsung-authored PM9D3a U.2 datasheet, **Rev. 1.3 dated May 2024**, is publicly reachable through an xFusion-hosted mirror. Its source custody is weaker than an official Samsung-hosted document, so the repository treats it as a **publicly reachable Samsung-authored datasheet mirror**, not as proof that Samsung itself publicly distributed that exact PDF URL.

Within that document:

- Enhanced SMART `0xC4`, bytes `331:324`: `Lifetime read Reclaim count`;
- Enhanced SMART `0xD0`, bytes `114:111`: `Patrol Read Reclaim Count`;
- OCP Cloud Attribute `0xC0`, bytes `87:81`: `Refresh Counts`.

This yields an interface-level distinction:

```text
Lifetime read Reclaim count
    !=
Patrol Read Reclaim Count
    !=
Refresh Counts
```

The three fields are separately named and located. That is enough to prevent the repository from collapsing them into one generic maintenance count. It is **not** enough to prove that their underlying event sets are disjoint, overlapping, or causally ordered.

The comparison with PM963 also establishes a schema guardrail:

```text
same-looking maintenance label across products
    !=
stable telemetry byte layout
    !=
same controller algorithm
    !=
same persistence/reset semantics
```

The word `Lifetime` likewise does not disclose checkpointing, sudden-power-loss atomicity, format/sanitize behavior, overflow semantics, or firmware-update handling.

`Patrol Read Reclaim Count` is suggestive of a background/proactive inspection regime, but the table does not prove a full-media scrub, scan cursor, cadence, or deterministic `patrol read -> reclaim` state machine.

The earlier 67F packet correctly refused to infer a mechanism from the `Refresh Counts` name alone. OCP primary specifications now provide a stronger interface definition: SMART-10 counts blocks re-allocated to maintain data integrity and excludes ordinary garbage collection; later wording also explicitly excludes wear leveling. That resolves the **standardized accounting meaning**, not the PM9D3a internal trigger or event-set overlap with Samsung's two reclaim counters.

See [`../evidence/67-samsung-pm9d3a-maintenance-telemetry-boundary-deepening.md`](../evidence/67-samsung-pm9d3a-maintenance-telemetry-boundary-deepening.md).

## OCP standardized-maintenance deepening — `Refresh Counts` versus background-data-refresh coverage

OCP's **NVMe Cloud SSD Specification v1.0 (03182020)** already defines SMART-10 at bytes `87:81` as `Refresh Counts`. The field counts blocks re-allocated to maintain data integrity and excludes creating free space due to garbage collection. OCP's accepted-contributions record dates the v1.0 contribution to **22 May 2020** by Facebook and Microsoft.

The same v1.0 specification separately defines **Background Data Refresh** requirements:

- BKGND-1 requires powered-on background refresh to prevent retention-related data loss;
- BKGND-2 requires design/testing for normal NAND operating temperature;
- BKGND-3 requires entire-device coverage and continuous background operation rather than idle-only service.

This creates a stronger retention distinction than telemetry naming alone:

```text
background refresh obligation
    -> purpose + coverage + service regime

SMART-10 Refresh Counts
    -> cumulative integrity-maintenance reallocation accounting
```

The document does not explicitly say those two sets are identical. Therefore:

```text
background-refresh coverage authority
    != SMART-10 accounting state
```

and:

```text
Refresh Counts increased
    != whole-device refresh coverage proved
```

Later OCP Datacenter NVMe SSD wording retains SMART-10 and explicitly excludes ordinary GC and wear-leveling relocation, so the standardized field is not a count of every internal block move.

See [`../evidence/67-2020-2025-ocp-refresh-count-semantics-deepening.md`](../evidence/67-2020-2025-ocp-refresh-count-semantics-deepening.md).

## Pre-2009 prior-art deepening — MegaChips thresholded repair / rewrite

The 2007-02-07-priority MegaChips family `JP2008192267A / US20080189588A1` moves the inspected functional floor earlier than the previously cited 2009-priority Samsung `read reclaim` family. Public application texts appeared in August 2008, so priority and public availability remain distinct.

The family treats read disturb as a condition where repeated reads can create a repair obligation. Repair can be driven by read count, current bit-error count, or accumulated occurrences of bit errors, including an ECC-margin example below maximum correction capability.

It separates:

```text
ECC-correct current value
    !=
recognize repair condition
    !=
rewrite / renew the physical embodiment
```

The description includes block- and page-level paths that write replacement data into unused physical space and update storage-management information. It also contemplates same-location rewrite, so the older term `rewrite` is broader than physical relocation.

The preferred embodiment stores threshold policy in Flash redundant-area metadata and can read it at power-on. That does **not** prove the running read-count comparison value itself persists:

```text
retained repair-policy threshold
    !=
proven retained read-history counter
```

Maintenance admission is also separable from the repair condition. The family permits work inline with host reads or at power-on/off, idle, sleep, charging, periodic, and externally instructed opportunities.

The terminology guardrail is:

> **first inspected `read reclaim` terminology ≠ first inspected proactive read-disturb rewrite / re-embodiment mechanism**.

No genealogy from MegaChips to Samsung or SK hynix is asserted.

See [`../evidence/67-megachips-2007-2008-read-disturb-rewrite-prior-art-deepening.md`](../evidence/67-megachips-2007-2008-read-disturb-rewrite-prior-art-deepening.md).

---

## Historical record / engineering reconstruction / interpretation ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| US20190066809A1 has 2017-08-31 priority, 2019-02-28 publication, and SK hynix assignees | `H/P` | patent bibliographic record |
| repeated single-page reads are treated as capable of disturbing a larger block | `H/P` | patent background/description |
| controller increments read-count state and schedules test reads at threshold/multiple conditions | `H/P` | patent abstract, description, claims |
| bit-error evidence can select adaptive target read/error thresholds | `H/P` | patent description/claims |
| read reclaim can copy valid values into another plurality of cells | `H/P` | explicit claims |
| the disclosed read count may be reset at power-off without storing it in NAND | `H/P` | explicit description/claims |
| MegaChips read-disturb repair family has 2007-02-07 priority and August 2008 public application texts | `H/P` | patent-family bibliographic record |
| MegaChips permits read-count, bit-error-count, or accumulated-error thresholds to trigger corrected rewrite | `H/P` | patent abstract/description/claims |
| a MegaChips repair path can write into unused physical space and update storage-management information | `H/P` | patent description |
| Samsung PM963 reference output exposes `Lifetime read Reclaim count` | `H/P` | Samsung DC Toolkit 2.1 product output |
| PM9D3a Rev. 1.3 mirrored datasheet exposes `Lifetime read Reclaim count` at `0xC4` bytes `331:324` | `H/P` | Table 148; mirror custody caveat |
| PM9D3a exposes `Patrol Read Reclaim Count` at `0xD0` bytes `114:111` | `H/P` | Table 149; mirror custody caveat |
| PM9D3a OCP `0xC0` page exposes `Refresh Counts` at bytes `87:81` | `H/P` | Table 150; mirror custody caveat |
| OCP v1.0 SMART-10 defines `Refresh Counts` at bytes `87:81` as blocks re-allocated to maintain data integrity, excluding GC free-space creation | `H/P` | OCP NVMe Cloud SSD Specification v1.0 |
| OCP v1.0 requires powered-on background data refresh with entire-device coverage and continuous background service | `H/P` | BKGND-1 through BKGND-3 |
| later OCP wording explicitly excludes ordinary GC and wear-leveling relocation from SMART-10 | `H/P` | OCP Datacenter NVMe SSD specification |
| separate PM9D3a fields prove disjoint physical maintenance mechanisms | `X` | interface separation does not recover event-set relation |
| OCP background-refresh operations and SMART-10 increments are exactly one-to-one | `X` | no explicit cross-reference establishing event-set identity |
| `Lifetime` proves crash-consistent counter persistence | `X` | persistence/update protocol not disclosed |
| `Refresh Counts` proves Case 36 or DRAM-refresh mechanism identity | `X` | standardized accounting semantics still do not establish mechanism identity |
| physical read-disturb state resets at power-off | `X` | controller proxy and cell condition are distinct |
| SK hynix invented read reclaim or ECC-margin-triggered relocation in 2017 | `X` | earlier MegaChips and Samsung evidence |
| patent evidence proves a named commercial SK hynix SSD shipped the exact algorithm | `X` | design evidence is not deployment evidence |
| logical payload can survive a controller-authorized change of physical embodiment | `E` | valid-value copy + mapping/currentness handoff |
| a lossy maintenance proxy may support retention when reset is paired with conservative requalification | `E` | bounded reconstruction of disclosed composition |
| cumulative maintenance telemetry is a summary rather than a complete causal history | `E` | counter interface does not encode full event trace |
| a cumulative SMART-10 value is not enough to prove whole-device background-refresh coverage is current | `E` | counter lacks region identity / coverage position |
| this is equivalent to human memory, forgetting, or recollection | `X/I` | unsupported anthropomorphism |

## Philosophical interpretation — bounded

Case 67 supports a narrow systems statement:

> **A system does not need to retain every causal trace in order to retain a usable object. It may preserve a deliberately compressed, even resettable maintenance proxy, provided that later requalification and repair re-establish enough confidence before physical margin is exhausted.**

The MegaChips evidence adds that a system may retain **repair policy itself** — thresholds and coverage information used to interpret later observations.

The PM9D3a and OCP telemetry evidence add another downstream observation:

> **What a system chooses to count is itself part of the control boundary. Separate summaries can preserve distinctions among maintenance regimes without preserving the full physical history or full firmware decision trace.**

OCP's whole-device background-refresh requirement sharpens this further:

> **retaining evidence that maintenance happened is not the same as retaining enough state to prove the maintenance obligation is satisfied.**

These are engineering interpretations, not claims about human memory or historical designer intent.

## Cross-case result

Case 67 now supports this chain:

```text
correct read now
    !=
no read-induced physical stress
    !=
read-count proxy
    !=
measured bit-error condition
    !=
adaptive maintenance threshold
    !=
reclaim decision
    !=
new physical embodiment
    !=
background-refresh coverage obligation
    !=
management telemetry counter
    !=
complete maintenance history
    !=
secure erasure of the old embodiment
```

Its strongest result remains that **controller-maintained risk history can be intentionally less durable than the medium state it approximates**, while safe retention can be rebuilt through conservative re-testing and relocation. The later Samsung/OCP evidence shows that management-visible maintenance accounting is another state layer: OCP standardizes `Refresh Counts` as integrity-maintenance reallocation accounting while separately requiring whole-device background-refresh coverage, and Samsung PM9D3a exposes that OCP counter alongside reclaim and patrol-associated reclaim counters without disclosing their event-set overlap.

## Prior art and anti-anachronism

The 2017-priority SK hynix design is not the origin of read reclaim or proactive read-disturb repair.

MegaChips `JP2008192267A / US20080189588A1`, with **2007-02-07 priority** and public application texts in **August 2008**, already describes read-disturb / bit-error repair conditions based on read count or error evidence, ECC correction before rewrite, and block/page repair paths that can move data into unused physical space while updating storage-management information. It uses `repair`, `recovery`, and `rewrite` rather than the later inspected `read reclaim` term.

Samsung `US20100235713A1`, with 2009 priority and 2010 publication, explicitly describes an ECC circuit counting read-data error bits, a threshold below maximum correctable-error count, a `read reclaim` indication, and reassignment/change of the affected block before ECC capability is exceeded.

Samsung `US20140237165A1`, with 2013 priority and 2014 publication, separately describes controller read reclaim as copying data to another block, compares bit-error rate with a threshold, uses read voltage/retry state in the decision, and notes that reclaim adds erase/write work and can shorten device life.

Therefore:

```text
2007 priority / 2008 public   MegaChips: thresholded read-disturb repair + corrected rewrite / optional relocation
2009 priority / 2010 public   Samsung: explicit read-reclaim indication below ECC limit + block reassignment
2013 priority / 2014 public   Samsung: BER/read-voltage-qualified reclaim + endurance cost
2017 priority / 2019 public   SK hynix: compressed proxy + adaptive test cadence + 3-D sampling + reclaim
2018 product documentation    Samsung PM963: lifetime read-reclaim telemetry witness
2020 OCP v1.0                SMART-10 integrity-maintenance reallocation count + whole-device background refresh requirement
2024 product documentation    Samsung PM9D3a: lifetime reclaim + patrol-reclaim + OCP refresh telemetry categories
```

Guardrails:

> **priority date ≠ public availability date**.

> **first inspected terminology ≠ first inspected broader function**.

> **functional similarity ≠ demonstrated genealogy**.

> **telemetry label continuity ≠ algorithm continuity**.

> **standardized telemetry semantics ≠ disclosed firmware implementation**.

> **same word `refresh` ≠ same mechanism**.

## Remaining evidence debt

The case remains `grounded`; this round does not justify a maturity increase. Important open work includes:

- exact shipped read-reclaim trigger logic in named products;
- threshold values and ECC-margin criteria;
- PM9D3a `Patrol Read Reclaim` firmware meaning and scan/cadence/coverage state;
- exact mapping from PM9D3a internal maintenance events into OCP SMART-10 `Refresh Counts`;
- whether PM9D3a maintenance events increment more than one of the three counters;
- counter persistence/reset/format/sanitize/firmware-update/overflow semantics;
- relocation atomicity and mapping/currentness handoff;
- physical victim geometry in named products;
- independent workload-to-telemetry validation;
- an official Samsung-hosted PM9D3a detailed datasheet carrying the same tables;
- direct qualification evidence for how an implementation demonstrates BKGND whole-device coverage;
- exact versioned wording changes across OCP v1.0, v2.0, v2.5, v2.6, and v2.7;
- firmware/product genealogy across PM963, PM9A3, and PM9D3a.

A high-value next experiment would read PM9D3a `0xC4`, `0xD0`, and `0xC0` telemetry together across bounded sustained-read, idle/patrol, and power-cycle phases to see which counters move and what state survives reset. A separate coverage-oriented experiment would need evidence beyond the cumulative SMART-10 value to show that whole-device background refresh is actually making bounded progress.

## Sources

1. SK hynix Inc. / SK hynix Memory Solutions America Inc., **US20190066809A1, “Read disturb detection and recovery with adaptive thresholding for 3-d nand storage,”** priority 31 August 2017, filed 7 December 2017, published 28 February 2019; granted as US10714195B2, 14 July 2020: <https://patents.google.com/patent/US20190066809A1/en>
2. MegaChips Corporation, **US20080189588A1, “Bit error prevention method and information processing apparatus,”** priority 7 February 2007, filed 3 January 2008, published 7 August 2008; later granted as US8214720B2: <https://patents.google.com/patent/US20080189588A1/en>
3. MegaChips family, **JP2008192267A, “Method of preventing bit error, and information processing device,”** filed/priority 7 February 2007, published 21 August 2008: <https://patents.google.com/patent/JP2008192267A/en>
4. Samsung Electronics Co., Ltd., **US20100235713A1, “Non-volatile memory generating read reclaim signal and memory system,”** priority 12 March 2009, published 16 September 2010: <https://patents.google.com/patent/US20100235713A1/en>
5. Samsung Electronics Co., Ltd., **US20140237165A1, “Memory controller, method of operating the same and memory system including the same,”** priority 19 February 2013, published 21 August 2014: <https://patents.google.com/patent/US20140237165A1/en>
6. Samsung Electronics, **Samsung DC Toolkit 2.1 User Guide**, October 2018, PM963 reference output with `Lifetime read Reclaim count`: <https://download.semiconductor.samsung.com/resources/user-manual/Samsung_DCToolkit_V2.1_User_Guide.pdf>
7. Samsung Electronics, **Samsung SSD PM9D3a Specification (PCIe NVMe U.2), Rev. 1.3, May 2024**, publicly reachable xFusion-hosted mirror; relevant Tables 148–150: <https://www.xfusion.com/wp-content/uploads/2025/11/PM9D3a-NVMe-U.2-Datasheet.pdf>. Source-custody caveat applies.
8. Samsung Semiconductor, **Samsung's PM9D3a Solid State Drive**, manufacturer product/technical context: <https://semiconductor.samsung.com/news-events/tech-blog/samsung-pm9d3a-solid-state-drive/>.
9. Open Compute Project, **NVMe Cloud SSD Specification, Version 1.0 (03182020)**, SMART-10 plus BKGND-1 through BKGND-3: <https://www.opencompute.org/documents/nvme-cloud-ssd-specification-v1-0-3-pdf>.
10. Open Compute Project, **Storage Project Approved Contributions**, v1.0 accepted-contribution record dated 22 May 2020: <https://www.opencompute.org/wiki/Storage_Project_Approved_Contributions>.
11. Open Compute Project, **Datacenter NVMe SSD Specification, Version 2.6**, later SMART-10 wording: <https://www.opencompute.org/documents/datacenter-nvme-ssd-specification-v2-6-2-pdf>.
12. Open Compute Project, **Datacenter NVMe SSD Specification, Version 2.7**, later SMART-10 wording: <https://www.opencompute.org/documents/datacenter-nvme-ssd-specification-v2-7-final-pdf>.
13. Open Compute Project, **Samsung PM9D3a PCIe Gen5 NVMe SSD**, OCP product page: <https://www.opencompute.org/products/441/samsung-pm9d3a-pcie-gen5-nvme-ssd>.

## Related repositories

A current search found no dedicated PM9D3a read-reclaim / patrol-reclaim or OCP `Refresh Counts` packet in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). Keep the retention-specific relation among workload/error evidence, whole-device background-refresh obligations, reclaim/refresh maintenance categories, maintenance-counter persistence horizons, and re-embodiment here. Broader Samsung enterprise-SSD genealogy, controller-generation history, V-NAND generations, OCP/NVMe telemetry standardization history, commercial deployment, and product-line archaeology belong in `computing-archaeology` rather than being duplicated here.