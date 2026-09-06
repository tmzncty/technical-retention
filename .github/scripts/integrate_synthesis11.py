from pathlib import Path

SYNTHESIS = r'''# Access-Disturbance Synthesis — Target Scope, Restore Obligation, and Workload-Conditioned Maintenance

**Status:** `grounded cross-case synthesis`

**Cases compared:**

- [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md) — selected-core destructive read and immediate rewrite/restore in the bounded classic core regime;
- [`../cases/03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md) — destructive-read restore and a separate elapsed-time regeneration obligation in Dennard's bounded dynamic-cell embodiments;
- [`../cases/70-magnetic-core-half-select-disturbance.md`](../cases/70-magnetic-core-half-select-disturbance.md) — non-target partial excitation, retained-state margin, and sense-line disturbance in coincident-current core arrays;
- [`../cases/52-nand-flash-read-disturb-access-induced-decay.md`](../cases/52-nand-flash-read-disturb-access-induced-decay.md) — cumulative NAND pass-voltage read disturb, ECC margin, and read-count-triggered maintenance;
- [`../cases/53-dram-rowhammer-targeted-refresh-policy.md`](../cases/53-dram-rowhammer-targeted-refresh-policy.md) — access-induced victim-row retention loss and targeted-refresh policy;
- [`../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md`](../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md) — compressed read-count evidence, ECC qualification, adaptive checking, and conditional physical reclaim.

This document closes one narrow roadmap question:

> When access itself changes the retention problem, how should the **logical request target**, **physical effect scope**, **immediate restore obligation**, **cumulative disturbance exposure**, **present service correctness**, **remaining retention/error margin**, **maintenance clock/evidence**, and **later refresh/rewrite/reclaim response** be separated?

It does **not** claim that magnetic core, DRAM RowHammer, and NAND read disturb are one physical mechanism, one historical lineage, or one universal definition of `destructive read`. It is an engineering comparison across already grounded cases.

---

## 1. Claim discipline

This synthesis follows [`METHOD.md`](METHOD.md).

- **H/P — historical / primary:** only vocabulary and mechanisms already grounded in the case/evidence records are treated as historical claims.
- **E — engineering reconstruction:** the cross-case state decomposition and relation names below are project analytical tools.
- **A — functional analogy:** comparisons such as `access can create a preservation obligation` do not imply genealogy.
- **I — philosophical interpretation:** the final interpretive claim is deliberately narrow and downstream of the engineering distinctions.

Project terms such as `physical effect scope`, `disturbance debt`, `maintenance clock`, and `residual retention margin` are not retroactively attributed to Forrester, Papian, Dennard, Fujitsu, Intel, Micron, SK hynix, or the RowHammer researchers.

---

## 2. Why this is not a duplicate of existing work

Case 52 already makes a bounded two-case analogy to magnetic-core destructive read: both show that access can create a preservation obligation, while explicitly rejecting physical or historical identity. This synthesis extends that local comparison into a reusable **effect-scope / trigger / response decomposition** by adding Case 70's half-select evidence, Case 03's separation of read-triggered restore from elapsed-time refresh, Case 53's neighbor-victim disturbance, and Case 67's compressed workload evidence plus conditional reclaim.

[`SYNTHESIS_06_FLASH_READ_PATH_VS_RENEWAL.md`](SYNTHESIS_06_FLASH_READ_PATH_VS_RENEWAL.md) asks a different question: how an already-aged/noisy Flash embodiment can remain readable through changed reference voltages, retry, ECC, and later physical renewal. The present synthesis asks what changes when **the access workload itself contributes to future retention risk**.

The broader magnetic-core engineering and manufacturing history remains in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md). Current companion-repository searches for `read disturb` and `half-select` did not expose a separate NAND/RowHammer access-disturbance history to reuse, so this document keeps only the retention-specific cross-case relation rather than building a second semiconductor-memory history.

---

## 3. Historical evidence that forces the separation

### 3.1 Selected access can create an immediate restore obligation — Case 02

In the bounded classic magnetic-core regime, the selected core's normal readout can drive the magnetic state through the switching process used to sense its prior value. If the prior value must remain stored, the machine must rewrite/restore it as part of the access cycle.

```text
selected retained state
    -> destructive read/sense event
    -> recovered logical value
    -> restore/rewrite of selected state
```

**E:** `read success ≠ retained selected embodiment after the read`.

The access itself creates a near-immediate preservation obligation toward the selected state.

### 3.2 Dynamic memory can have two maintenance clocks at once — Case 03

Dennard's bounded dynamic-cell evidence separates two obligations often collapsed under `refresh`:

1. a selected dynamic node can require restoration because a read path disturbed it;
2. charge leakage can require regeneration even when the cell has not just been read.

Therefore:

> **access-triggered restore ≠ elapsed-time-triggered regeneration**.

The same payload technology can be subject to more than one maintenance clock, and a stable logical address does not reveal which clock caused the latest restoration.

### 3.3 Logical nonselection does not imply zero physical effect — Case 70

Coincident-current magnetic core provides a useful non-semiconductor control. Forrester/Papian-period evidence and the later IBM disturbance-cancellation witness show that cores on one selected coordinate can be physically excited below the full switching threshold even though they are logically unselected. Repeated nonselecting excitation can be a retained-state-margin concern, while partial-select output can also disturb a shared sense path without proving stored-state corruption.

This gives two distinct relations:

> **logical request target ≠ complete physical excitation/effect scope**

and

> **physical disturbance / sense contribution ≠ payload corruption**.

The access can be logically local while its material and electrical consequences are wider.

### 3.4 NAND reads can spend future margin outside the requested page — Case 52

NAND read disturb supplies a later, physically different counterexample. Reading a selected page requires pass-through bias on unselected cells in the NAND string. Repeated exposure can shift threshold-voltage distributions in cells whose logical value was not requested.

A selected-page read can therefore succeed while making future reads of neighboring retained state less reliable:

> **logical nondestructiveness of the requested read ≠ material nondisturbance of the surrounding block**.

Case 52 also supplies an important negative result: the NASA/JPL qualification study did not reproduce disturb failures in the tested devices despite large read counts. Thus `read disturb exists` does not justify a universal fixed read-count failure threshold.

### 3.5 RowHammer separates aggressor service from victim preservation — Case 53

RowHammer makes the target/effect split even sharper. Repeated activation of an aggressor row can accelerate charge loss in physically adjacent victim rows. The ordinary access path can repeatedly sense/restore the aggressor while the neighboring victim loses retention margin.

```text
restorative for the accessed/aggressor row
and
retention-destructive for a nearby victim relation
```

This also separates ordinary periodic refresh from workload-conditioned urgency. Meeting the nominal DRAM refresh schedule does not establish immunity to an access pattern that makes a victim unsafe before that ordinary deadline.

### 3.6 Access history can be compressed, checked, and partly forgotten — Case 67

SK hynix's bounded 3-D NAND controller disclosure can use a grouped/compressed read-count proxy to schedule tests, then use ECC/bit-error evidence to decide whether reclaim is needed and how aggressively to check later. It does not retain an exhaustive physical history of every disturbed cell.

The source even allows the read-count proxy to be cleared after power-off while the underlying physical read-disturb condition does not thereby rewind. Safety is recovered by conservative checking policy rather than by pretending the medium's history disappeared.

> **maintenance proxy ≠ physical hazard state**

> **maintenance-proxy lifetime can be shorter than hazard lifetime**

> **threshold crossing ≠ proven corruption ≠ automatic relocation requirement**.

---

## 4. Cross-case state decomposition

The following is an **engineering reconstruction**, not a historical state machine shared by the six technologies.

```text
logical request target
        !=
physical excitation / effect scope
        !=
selected-state post-access condition
        !=
neighbor / coupled-state disturbance exposure
        !=
present logical service correctness
        !=
remaining physical / ECC retention margin
        !=
maintenance trigger evidence or clock
        !=
maintenance target selection
        !=
restore / targeted refresh / rewrite / reclaim action
        !=
post-maintenance qualified state
```

| Case | What access physically affects | Can current access succeed while debt remains? | Maintenance trigger | Principal response |
| --- | --- | --- | --- | --- |
| 02 core destructive read | selected core directly switches during readout | not if selected value must remain; restore is part of the access relation | the read itself | immediate selected-core rewrite/restore |
| 03 bounded dynamic cell | selected state can need read restore; leakage also continues with time | yes across the separate time-driven obligation | read event and/or elapsed retention interval | access restore and scheduled regeneration remain distinct |
| 70 half-selected core | target plus many partially excited non-target cores and shared sense path | yes; non-target state may remain valid while margin/sense disturbance exists | ordinary array traffic / pulse patterns | design margin, sensing/cancellation, inhibit/control rather than one universal rewrite rule |
| 52 NAND read disturb | selected read plus unselected same-block/string cells under pass voltage | yes; selected payload can return correctly while neighbor margin is consumed | cumulative reads, device/error state | tune read stress, verify/recover, rewrite or relocate when policy requires |
| 53 RowHammer | aggressor activation plus physically adjacent victim rows | yes; aggressor service can succeed while victim risk rises | activation pattern/history + topology/policy | targeted/probabilistic/extra victim refresh or other mitigation |
| 67 adaptive read reclaim | requested page/group plus controller-defined disturbed neighborhood | yes; ECC-correctable reads can coexist with shrinking future margin | compressed read count followed by measured ECC/error evidence | adaptive checking and conditional reclaim/relocation |

---

## 5. Engineering reconstruction

### 5.1 Logical target ≠ physical effect scope

A software-visible or address-decoder-visible target answers `which state is being requested?` It does not automatically answer `which physical states are energized, coupled, sensed, or stressed while servicing that request?`

Core half selection, NAND pass voltage, and RowHammer force this distinction through different mechanisms.

> **an access can be logically local while its retention consequences are materially nonlocal**.

That sentence is functional comparison, not a claim that the nonlocal mechanisms are equivalent.

### 5.2 Successful service now ≠ zero future retention debt

Case 02 is the immediate form: if the selected state is destructively read, debt exists before the operation is retention-complete. Cases 52, 53, and 67 expose delayed forms: current logical service can succeed while the operation consumes future physical or ECC margin elsewhere.

> **service correctness at `t1` ≠ unchanged recoverability margin after `t1`**.

### 5.3 Immediate restore ≠ cumulative preventive maintenance

It is tempting to place all of these cases under `destructive read`. That would erase an important timing boundary.

- classic core restore follows each relevant destructive read;
- NAND read disturb is cumulative and can be thresholded, delayed, ECC-masked, or answered by later relocation;
- RowHammer mitigation can be conditioned on recent activity and physical adjacency;
- dynamic memory can have an independent elapsed-time refresh obligation even without unusual access.

> **access-triggered restoration ≠ access-conditioned maintenance**.

The former can be constitutive of completing the individual access. The latter can accumulate debt across many accesses before policy schedules a response.

### 5.4 Access count ≠ elapsed time

Cases 52/67 make read count a workload clock. Case 53 makes activation density within a time window a disturbance-policy input. Case 03 retains the classic time/deadline clock.

> **many accesses in a short interval can create more retention pressure than a quiet interval of equal duration**,

while ordinary leakage means the converse is also possible: a quiet interval can still consume dynamic-retention margin.

### 5.5 Disturbance evidence ≠ disturbance state ≠ corruption

A counter, threshold, or policy bit is evidence about exposure under one model; it is not the charge, magnetization, or threshold-voltage state itself. Likewise, physical excursion or accumulated error margin does not immediately imply a wrong logical answer.

```text
exposure / proxy
    -> possible physical disturbance
    -> measurable margin/error change
    -> maybe still correctable/recoverable
    -> eventual logical corruption only if recovery margin is exceeded
```

Case 67's power-off-cleared counter is a particularly strong counterexample to treating proxy state as the underlying physical condition.

### 5.6 Restoring the target ≠ preserving every coupled neighbor

Case 53 is the cleanest witness: opening an aggressor row can restore its own cells while increasing retention pressure on victims. Case 70 similarly separates selected-core behavior from repeated half-select disturbance and from sense-line discrimination.

> **target-local maintenance completion ≠ neighborhood-wide retention qualification**.

### 5.7 ECC/read recovery ≠ renewed future margin

NAND and DRAM cases can preserve a correct present answer through ECC or changed read/mitigation policy while the physical representation remains closer to a failure boundary. Case 67's reclaim path makes the next stage explicit: after qualification, valid values may be copied into a new physical population.

> **recoverable now ≠ physically renewed for later**.

This directly complements Synthesis 06 rather than replacing it.

### 5.8 The word `refresh` does not identify one maintenance relation

Across these cases, `restore`, `refresh`, `targeted refresh`, `reclaim`, and `rewrite` have different historical scopes and physical operations. A project taxonomy should name at least:

- what triggered the work;
- which state was at risk;
- whether the current access itself was destructive;
- whether the work restores the same embodiment or creates a new one;
- whether the trigger is time, access count, error evidence, topology, or a composition of them.

> **shared maintenance vocabulary ≠ shared mechanism or trigger**.

---

## 6. Prior-art and anti-anachronism boundary

No new invention-priority claim is made by this synthesis.

- the 1950s magnetic-core evidence establishes an early access/partial-select preservation problem in its own vocabulary;
- Case 03 keeps Dennard's dynamic-cell read/restore and regeneration vocabulary local to the 1967 filing and rejects `all DRAM reads are destructive` as a universal statement;
- Case 52 already places explicit NAND `read disturb` vocabulary and read-count relocation before the 2015 characterization;
- Case 53 already places row-hammer-specific targeted-refresh work in Intel's 2012-priority filing before the 2014 open experimental characterization;
- Case 67 already uses earlier Samsung families to block an SK-hynix-first claim for generic ECC-margin-triggered read reclaim.

Chronological precedence across media does **not** establish descent. `magnetic-core destructive read -> DRAM destructive restore -> NAND read disturb -> RowHammer` is not asserted as a lineage. The cross-case result is only that each system makes some part of access materially relevant to later preservation.

---

## 7. Bounded philosophical interpretation

The mechanism comparison supports one deliberately narrow interpretive claim:

> **access is not always external to retention.**

In some systems, the act of making a state available changes the state itself, changes neighboring state, changes the remaining recovery margin, or changes the maintenance work now owed to the future.

This should not be universalized. Static/nondisturbing reads, passive inscriptions, and many other retention regimes remain counterexamples. The philosophical value is therefore not `all reading destroys`, but the more precise observation that **technical availability can be causally entangled with the maintenance of what is made available**.

This is a project interpretation, not historical vocabulary.

---

## 8. Bounded roadmap closure

For the present repository, the access-disturbance comparison can be treated as closed at the **relation-decomposition level**:

```text
request target
    != physical effect scope
    != immediate post-access state
    != accumulated disturbance exposure
    != present service correctness
    != remaining retention/error margin
    != maintenance clock/evidence
    != maintenance target selection
    != maintenance action
    != post-maintenance qualification
```

The following remain valid future work without reopening this exact synthesis question:

- a broader history of destructive/nondestructive read terminology across Williams tubes, drums, core, and semiconductor memories;
- vendor/controller implementation histories for RowHammer/TRR/RFM and modern 3-D NAND read-reclaim policy;
- post-2020 RowHammer and DDR5 mitigation evolution;
- exact 3-D NAND disturb geometry across generations and vendors;
- quantitative fault injection connecting access counts to measured margin and maintenance cost;
- a broader maintenance taxonomy spanning access-triggered, deadline-driven, capacity/reclaim-triggered, wear-triggered, and failure/repair-triggered regimes.

---

## Source boundary

This synthesis introduces no new historical evidence beyond the grounded case records. The principal primary/institutional chains remain:

1. Forrester/Papian/IBM magnetic-core records in [Case 02](../cases/02-magnetic-core-destructive-read.md) and [Case 70](../cases/70-magnetic-core-half-select-disturbance.md);
2. R. H. Dennard, 1967 dynamic-memory patent record in [Case 03](../cases/03-dram-refresh-as-scheduled-restoration.md);
3. Fujitsu 2002-priority NAND read-disturb filing, NASA/JPL 2008 qualification, and later experimental characterization in [Case 52](../cases/52-nand-flash-read-disturb-access-induced-decay.md);
4. Intel 2012-priority row-hammer targeted-refresh filing, Kim et al. ISCA 2014, Micron 2015 DDR4 documentation, and TRRespass 2020 in [Case 53](../cases/53-dram-rowhammer-targeted-refresh-policy.md);
5. SK hynix 2017-priority adaptive read-reclaim filing and its earlier Samsung prior-art controls in [Case 67](../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md).

Exact source locations, evidence grades, and caveats remain in those cases' grounding records and should be cited there rather than being silently flattened into this synthesis.
'''


def insert_once(path: str, marker: str, addition: str, presence: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    if presence in text:
        return
    if marker not in text:
        raise RuntimeError(f'{path}: anchor missing')
    p.write_text(text.replace(marker, addition + marker, 1), encoding='utf-8')


Path('docs/SYNTHESIS_11_ACCESS_DISTURBANCE_MAINTENANCE.md').write_text(SYNTHESIS, encoding='utf-8')

insert_once(
    'README.md',
    'This chain is a **research heuristic**, not a claim that all of these mechanisms are historically or philosophically identical.',
    'A bounded access-disturbance comparison is now available in [`docs/SYNTHESIS_11_ACCESS_DISTURBANCE_MAINTENANCE.md`](docs/SYNTHESIS_11_ACCESS_DISTURBANCE_MAINTENANCE.md). Across grounded magnetic-core, DRAM, RowHammer, and NAND cases it separates the logical request target, physical effect scope, immediate restore obligation, cumulative disturbance exposure, present service correctness, remaining retention/error margin, maintenance clocks/evidence, and later refresh/rewrite/reclaim response; the comparison is explicitly functional and does not assert a shared physical mechanism or genealogy.\n\n',
    'SYNTHESIS_11_ACCESS_DISTURBANCE_MAINTENANCE.md',
)

insert_once(
    'ROADMAP.md',
    '- [ ] How should `returned/visible`, `crash-admissible`, `explicitly durable`, and `reclaimed/converged` be separated in filesystem regimes?',
    '- [x] In access-disturbing memory/storage, separate `logical request target`, `physical excitation/effect scope`, `selected-state post-access condition`, `neighbor/coupled disturbance exposure`, `present service correctness`, `remaining retention/error margin`, `maintenance trigger evidence/clock`, and later `restore/refresh/rewrite/reclaim` response — closed at the bounded cross-case relation level by [`docs/SYNTHESIS_11_ACCESS_DISTURBANCE_MAINTENANCE.md`](docs/SYNTHESIS_11_ACCESS_DISTURBANCE_MAINTENANCE.md), synthesizing grounded Cases 02, 03, 52, 53, 67, and 70. This is a functional/mechanism comparison, not a genealogy; broader destructive-read terminology history, modern RowHammer/TRR/RFM evolution, cross-vendor 3-D NAND disturb policy, and quantitative fault injection remain separate work.\n',
    'SYNTHESIS_11_ACCESS_DISTURBANCE_MAINTENANCE.md',
)

index = Path('CASE_INDEX.md')
text = index.read_text(encoding='utf-8')
if '1436. **logical request target ≠ physical effect scope**' not in text:
    if '1435. **manufacturer product semantics ≠ complete JEDEC chronology**' not in text:
        raise RuntimeError('CASE_INDEX tail anchor missing')
    appendix = r'''

### Cross-case access-disturbance synthesis — target scope, maintenance clocks, and preservation response

1436. **logical request target ≠ physical effect scope** — core half selection, NAND pass-through bias, and RowHammer all show that servicing one address can electrically or materially affect retained state outside the requested target.
1437. **selected-state restoration ≠ neighbor-state preservation** — an accessed core/DRAM row can be correctly restored while half-selected or physically adjacent state still carries a separate disturbance/margin obligation.
1438. **logical nondestructiveness ≠ material nondisturbance** — a NAND selected-page read can return the intended value without directly destroying that page while cumulative pass-voltage stress changes unselected cells' future margin.
1439. **successful current access ≠ unchanged future recoverability margin** — ECC-correctable NAND reads and disturbance-free current service can coexist with a smaller margin against later errors.
1440. **access-triggered restore ≠ access-conditioned maintenance** — classic destructive-read restore can be constitutive of completing one access, whereas NAND read reclaim or RowHammer mitigation may accumulate evidence/debt across many accesses before acting.
1441. **access-count clock ≠ elapsed-time retention deadline** — read/activation history can create workload-conditioned urgency, while ordinary leakage can create a separate deadline even during quiet periods.
1442. **maintenance proxy ≠ physical disturbance state** — a read counter, threshold, or policy summary represents exposure under one controller model; it is not the cells' magnetization, charge, threshold-voltage distribution, or direct proof of corruption.
1443. **maintenance-proxy lifetime ≠ hazard lifetime** — Case 67 allows a read-count proxy to be cleared after power-off while the medium condition persists, provided conservative requalification policy compensates for lost history.
1444. **disturbance evidence ≠ logical corruption** — half-select output, elevated raw errors, or threshold-crossing exposure can create maintenance/diagnostic work before the requested payload becomes wrong or uncorrectable.
1445. **targeted refresh / reclaim ≠ ordinary periodic refresh** — both can preserve a logical value, but their trigger, target geometry, timing, control state, and physical operation remain distinct.
1446. **read recovery ≠ representation renewal** — present ECC/read-path success can recover a value from a stressed embodiment, while rewrite/reclaim creates a different future physical support and restores a different kind of margin.
1447. **cross-case access-disturbance decomposition ≠ historical genealogy** — magnetic-core destructive read/half-select, Dennard dynamic-cell restore, NAND read disturb, RowHammer, and later controller reclaim are compared only at the relation level; chronological order does not prove descent or one shared mechanism.
'''
    index.write_text(text.rstrip() + appendix + '\n', encoding='utf-8')
