# Synthesis 30 — Maintenance Coverage: Local Work, Domain Completion, and Completion Evidence

> **Question:** when preservation work is performed repeatedly on local targets, what justifies saying that the relevant protected domain has actually been covered, and what evidence distinguishes local work, traversal progress, domain completion, and renewed future margin?

**Status:** bounded cross-case engineering synthesis over already-grounded evidence. This document adds no invention-priority claim and asserts no historical genealogy among LPDDR2 refresh, Data General DRAM sniffing, HDFS background verification, or enterprise-SSD/storage-system scrub practice.

The synthesis is centered on:

- [`Case 105 — LPDDR2 Per-Bank REFRESH`](../cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md) — one bank-local refresh transaction can complete while the rolling retained-set obligation still requires a full bank cycle;
- [`Case 77 — Data General DRAM sniffing`](../cases/77-data-general-dram-sniff-refresh-ecc-scrub.md) — the same recurring refresh opportunity can advance two maintenance domains with different target geometry and revisit periods;
- [`Case 83 — HDFS DataNode BlockScanner`](../cases/83-apache-hdfs-block-scanner-checksum-verification.md) — a resumable traversal cursor can preserve where maintenance should continue without becoming proof that every earlier target passed verification;
- [`Case 111 — Enterprise SSD extended-shutdown maintenance`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md) — powered maintenance opportunity, named scrub execution, per-vdisk completion evidence, and hidden device-local retention work remain distinct.

Historical and implementation claims remain owned by the case/evidence records. The terms **maintenance coverage**, **coverage domain**, **coverage accounting**, **completion evidence**, and **residual obligation** below are project engineering vocabulary unless a source independently uses equivalent language.

---

## 1. Verdict

The repository should not use `maintenance complete` without naming both a **scope** and an **evidence relation**.

The four grounded cases require at least this decomposition:

```text
one local maintenance action
    != target traversal / advancement
    != protected-domain coverage
    != proof or evidence of that coverage
    != permanent future safety
```

A more useful comparison frame is:

```text
protected domain
    + target-selection / admission rule
        ↓
local maintenance event
        ↓
target-local result
        ↓
coverage accounting / traversal state
        ↓
domain-complete condition
        ↓
completion evidence, if exposed
        ↓
remaining / renewed maintenance obligation
```

This is **not** a universal implementation pipeline. Some mechanisms use a rolling-window rule rather than a pass, some expose no durable progress state, some permit replay after cursor loss, and some report completion only at a system layer that cannot certify hidden lower-layer work.

The central rule is therefore:

> **maintenance execution must be typed by target, coverage domain, accounting horizon, and completion evidence.**

---

## 2. Claim discipline

This synthesis follows [`METHOD.md`](METHOD.md) and [`../AGENTS.md`](../AGENTS.md).

- **H/P — historical / primary:** source vocabulary, device behavior, dates, product contracts, and implementation facts remain in the grounded cases and their evidence records.
- **E — engineering reconstruction:** the cross-case decomposition into local work, coverage accounting, domain completion, completion evidence, and residual obligation is project analytical vocabulary.
- **A — functional analogy:** similarity in coverage structure does not establish shared mechanism, architecture, standard ancestry, or technical genealogy.
- **I — philosophical interpretation:** any interpretation of maintenance as a temporally renewed relation comes only after the engineering distinctions are fixed.

This document makes no claim that `refresh`, `sniff`, `scan`, and `scrub` are historical synonyms. They are intentionally kept source-specific.

---

## 3. Why this is not Synthesis 08, 24, or 26 again

Three existing syntheses define neighboring but different questions.

### Synthesis 08 — integrity lifecycle

[`SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md`](SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md) asks how physical presence, integrity evidence, verification coverage, defect discovery, repairability, restored redundancy, and later revalidation differ.

The present synthesis is broader in one axis and narrower in another. It does **not** restate the integrity/repair lifecycle. It asks how repeated maintenance work establishes coverage even when the work is not fundamentally an integrity check — LPDDR2 refresh is the decisive counterexample.

### Synthesis 24 — why work is due and when it can run

[`SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md`](SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md) separates maintenance trigger/obligation, opportunity/admission, credit/progress, execution, and completion.

The present synthesis deepens only the last two terms:

> **What scope does one unit of progress cover, and what evidence allows a claim of completion over the whole relevant domain?**

Synthesis 24 therefore supplies the temporal/control-plane distinction; Synthesis 30 supplies the **coverage geometry and proof boundary**.

### Synthesis 26 — how maintenance-control state survives

[`SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md) asks what state maintenance machinery needs across interruption and compares persist-and-resume, persist-and-validate/rebind, and discard-and-replay strategies.

The present synthesis asks a different question. A cursor may survive perfectly and still fail to prove successful work on every earlier target. Conversely, a system may complete a bounded coverage obligation without retaining an event-by-event history of how it did so.

Therefore:

```text
progress-state persistence
    != coverage proof

coverage proof
    != complete maintenance history
```

---

## 4. Six relations that must remain distinct

### 4.1 Protected domain

Question:

> Which set of state is the maintenance obligation supposed to protect or inspect?

Examples in the bounded cases differ sharply:

- the LPDDR2 bank set under a rolling refresh obligation;
- the full ECC-protected memory address space admitted to Data General sniffing;
- the HDFS blocks of a volume/block-pool traversal;
- the vdisks / storage-system scope named by IBM ESS scrub guidance.

The protected domain is not automatically identical to every physically present carrier. Retired, absent, failed, or administratively excluded elements can fall outside the active maintenance set under system-specific rules.

### 4.2 Local maintenance target

Question:

> What does one maintenance action actually touch?

One LPDDR2 `REFpb` targets one bank. One Data General sniff opportunity checks a selected word even while row refresh has a different target geometry. One HDFS scan operation verifies one block replica. A storage-system scrub can report work at a vdisk/system layer without exposing every hidden NAND operation.

Therefore:

> **local target != protected domain.**

### 4.3 Coverage accounting / traversal relation

Question:

> What connects many local actions into a claim that the intended domain is being covered?

The bounded cases expose several non-identical forms:

- fixed bank sequencing plus rolling refresh accounting;
- a fuller rotating sniff address over memory words;
- a block iterator/cursor over a volume;
- system-layer scrub progress/completion reporting.

This relation can be implicit, volatile, restart-persistent, reconstructed, or exposed only through status messages depending on the system.

### 4.4 Domain-complete condition

Question:

> What condition means the relevant bounded coverage unit is complete?

Examples:

- one full cycle of eight LPDDR2 `REFpb` commands can substitute for one all-bank refresh in the documented accounting relation;
- Data General product documentation describes sniffing as covering all memory locations on a recurring cadence;
- HDFS reaches a block-iterator pass boundary, but that traversal boundary is not itself a certificate that every encountered block passed verification;
- IBM ESS operator guidance asks for a named scrub run to complete and exposes per-vdisk completion messages.

The completion predicate is therefore system-specific. `N operations happened` is insufficient unless the target-selection and success rules make the count meaningful.

### 4.5 Completion evidence

Question:

> What retained or observable evidence supports the assertion that the bounded coverage condition has been reached?

A source may expose:

- a deterministic sequence rule rather than a `done` bit;
- a cursor or pass boundary;
- counters/status;
- a log or completion message;
- nothing more than an interface timing/coverage contract.

Evidence strength must match the claim. A cursor is evidence of traversal position, not automatically of prior success. A system scrub completion message is evidence about the named system scrub, not hidden controller internals.

### 4.6 Residual / renewed obligation

Question:

> What remains due after this coverage unit finishes?

Completion is usually scoped in time.

- LPDDR2 refresh coverage belongs to a rolling refresh requirement; the next interval creates continuing work.
- Data General sniffing is recurrent because new correctable errors can arise after a previous pass.
- HDFS periodic verification ages and later blocks need renewed observation.
- SSD/storage-system retention maintenance does not make future unpowered retention risk disappear forever.

Therefore:

> **coverage completion != permanent immunity from future maintenance.**

---

## 5. Case 105 — local REFpb completion is not bank-complete or window-complete maintenance

### H/P inherited from the grounded case

Micron and SK hynix LPDDR2 product documentation distinguish `REFpb` from `REFab`. In the bounded eight-bank devices, one `REFpb` targets the bank selected by the device's fixed bank-count sequence. The target bank is unavailable during `tRFCpb`, while other banks can remain accessible.

The same documentation states that, for the documented refresh accounting, one `REFab` can be replaced by a **full cycle of eight `REFpb` commands**.

### E — three completion scopes coexist

The case therefore directly requires:

```text
one REFpb completed
    != one full eight-bank REFpb cycle completed
    != rolling refresh-window obligation satisfied
```

This is stronger than the generic statement `maintenance takes several commands`. It identifies three different scopes:

1. **transaction-local completion** — the selected bank's current `REFpb` command finishes;
2. **bank-set cycle completion** — every bank index has received its place in the full per-bank sequence;
3. **rolling-horizon satisfaction** — enough refresh work occurs within the applicable refresh window.

A counter can coordinate the target sequence without being a durable ledger of every historical refresh. RESET/self-refresh-exit resynchronization further shows that local sequencing state is regime control state, not application history.

### E — service concurrency says nothing about global completion

Because non-target banks may remain accessible while one bank is being refreshed:

> **some of the protected domain remains serviceable != the maintenance obligation for the whole protected domain is complete.**

The feature localizes service disruption. It does not shrink the retained set the way PASR can.

---

## 6. Case 77 — one clock can advance two coverage domains at different rates

### H/P inherited from the grounded case

Data General's 1980-filed design uses recurring DRAM refresh opportunities both for ordinary row refresh and for a separate ECC word check called `sniffing`. The patent's illustrative geometry refreshes rows on the millisecond scale while advancing a fuller word address so the same word is sniffed on a much longer interval. Later MV/4000 product documentation makes refresh-coupled sniffing a named-product behavior and describes all memory locations as being checked recurrently.

### E — shared opportunity does not collapse coverage geometry

The important relation is:

```text
row-refresh coverage
    != word-sniff coverage
```

The same recurring scheduler opportunity can advance two maintenance processes whose:

- targets differ;
- success predicates differ;
- revisit periods differ;
- physical purposes differ.

Ordinary refresh renews charge representation. Sniffing asks whether an ECC-protected word already contains a correctable error and, when appropriate, writes corrected state back.

Thus:

> **shared clock/opportunity != shared coverage domain.**

### E — a successful demand read does not close the sniff obligation

Data General also separates corrected value delivery from stored-state repair. A requester can receive a corrected logical value while the stored embodiment still awaits later periodic writeback.

That gives another coverage warning:

> **successful service at one target != preventive maintenance coverage of the domain.**

### E — coverage applies to the admitted set

The later Data General `PAGEINH` witness allows failed/no-longer-used pages to be skipped by recurring refresh/sniff work. That means even `whole-memory coverage` must be read through the system's current admission relation rather than as a metaphysical claim that every physical carrier is always serviced.

---

## 7. Case 83 — a traversal cursor is not a success certificate

### H/P inherited from the grounded case

HDFS `BlockScanner` / `VolumeScanner` performs rate-limited periodic or suspect-triggered checksum verification over local block replicas. The implementation retains block-iterator state and can save a cursor for restart-oriented traversal continuation. If a saved cursor is unavailable, it can create a fresh iterator and repeat work.

The grounded case also identifies a concrete implementation bug in the intended periodic cursor-save cadence and explicitly notes that iterator position can advance even when block verification records an error.

### E — traversal progress and verification outcome are different state

The sharpest rule from this case is:

```text
cursor says where traversal should continue
    != cursor proves all earlier blocks verified successfully
```

A persisted cursor can be:

- useful for avoiding repeated scanning;
- current enough to resume traversal;
- completely insufficient as a per-block success ledger.

This is exactly why `coverage state` needs a typed claim. There are at least two meanings that must not be collapsed:

1. **coverage progress** — where the scanner is in the traversal;
2. **coverage result** — what happened when individual targets were checked.

### E — suspect priority does not replace broad coverage

HDFS can pull a suspect block forward for quick rescan while retaining a separate broad periodic iterator. Therefore:

> **priority work on one target != replacement for whole-domain periodic coverage.**

This parallels LPDDR2 only functionally: local priority and local completion do not, by themselves, discharge the broader obligation. The mechanisms and historical lineages are unrelated.

### E — coverage evidence ages

Even a successful pass does not permanently prove future integrity. The scanner exists precisely because a later fault can appear after an earlier success.

So:

> **verified in a previous pass != verified forever.**

---

## 8. Case 111 — system-layer completion evidence has a bounded scope

### H/P inherited from the grounded case

IBM and Dell extended-shutdown guidance separates passive powered-off retention from later powered maintenance opportunity. Dell explicitly assigns powered time to background retention work and warns against equating power restoration with completion.

The IBM ESS-specific follow-up goes further: after a sufficiently long powered-off period, the operator is told to power the system so disk scrubbing can complete a run and to observe an `mmfs` completion message for each vdisk in each declustered array.

### E — opportunity, execution, and completion can all be visible at different levels

The bounded state machine is:

```text
calendar intervention point
    != powered maintenance opportunity
    != named scrub execution
    != observed per-vdisk scrub completion
```

This gives the synthesis something the DRAM cases do not: explicit operator-visible completion evidence.

### E — a completion message is only as broad as the named mechanism

The grounded case is careful not to inflate this message into controller-internal certainty. An ESS scrub-completion record does not prove that:

- every NAND cell was physically rewritten;
- every hidden SSD-firmware retention task has completed;
- every future retention risk is eliminated;
- sanitization has occurred.

Therefore:

> **system-layer scrub completion != universal lower-layer maintenance completion.**

This is a general claim-discipline rule, not a criticism of the product. Completion evidence can be perfectly valid for the mechanism it names while remaining silent about another layer.

---

## 9. Cross-case matrix

| Relation | LPDDR2 Case 105 | Data General Case 77 | HDFS Case 83 | Enterprise SSD / ESS Case 111 |
| --- | --- | --- | --- | --- |
| protected domain | retained bank set / rolling refresh accounting | admitted ECC-protected memory words plus distinct row-refresh domain | blocks in scanner traversal | named storage-system / vdisk scrub scope; hidden device work remains separate |
| local target | one bank per `REFpb` | one refresh row plus one selected sniff word under distinct address geometry | one block replica | implementation-specific scrub work; operator observes vdisk-level status |
| selection/progress relation | internal bank sequence + controller tracking | rotating full sniff address; refresh addressing separate | block iterator / cursor + suspect queue | system scrub progress/status |
| bounded domain-complete relation | full bank cycle inside rolling refresh accounting | recurrent whole-memory word coverage | iterator/pass coverage, not automatically all-success ledger | named scrub run complete for each vdisk |
| completion evidence | command/sequence contract; no universal historical ledger implied | schedule/product behavior, not a permanent certificate | iterator/cursor and scan results are separate | explicit `mmfs` per-vdisk completion message in bounded ESS guidance |
| continuing obligation | next rolling refresh horizon | next recurrent sniff/refresh cycles | later periodic re-verification | future offline/maintenance cycles remain possible |
| major anti-shortcut | one bank done != all banks done | shared refresh opportunity != same maintenance coverage | cursor advanced != all prior blocks passed | scrub done != all hidden NAND work/sanitize done |

The matrix is **A/E** — a functional comparison over independently grounded historical records.

---

## 10. Cross-case findings

### E — operation count is not coverage without target identity

Counting maintenance actions is meaningful only if the system also knows which targets those actions serviced and what rule defines a complete domain.

LPDDR2 makes this explicit: eight arbitrary refresh-like events are not the useful historical claim; the documented bank-sequence/accounting relation is what makes a full cycle meaningful.

### E — local completion is not domain completion

A bank can finish `REFpb`, a word can finish a sniff/writeback, and a block can finish verification while the larger protected set remains outstanding.

> **target-local done != domain done.**

### E — domain completion is not permanent safety

Rolling refresh, recurrent sniffing, periodic HDFS scanning, and field SSD-maintenance guidance all show that a completed pass/window can be followed by another maintenance obligation.

> **coverage complete at t1 != future state guaranteed at t2.**

### E — progress coordinate is not a success ledger

HDFS supplies the strongest counterexample. A traversal cursor can validly identify where to resume without certifying the success of every earlier target.

This blocks a common category error:

> **maintenance progress != maintenance result history.**

### E — one scheduler can serve more than one maintenance domain

Data General shows that recurring refresh timing can create an opportunity for both charge restoration and ECC sniffing without equal target geometry or revisit period.

> **same scheduler opportunity != same maintenance predicate.**

### E — full-domain language is layer-relative

`all banks`, `all memory locations`, `all blocks in a pass`, and `each vdisk` each denote a domain defined at a particular interface/system layer. None automatically proves a stronger statement such as `every physical cell was rewritten`.

> **whole-domain at layer N != whole physical substrate at layer N-1.**

### E — completion evidence can be valid and still non-transitive

IBM ESS completion messages can validly close the named system scrub without proving every hidden device-local task. HDFS cursor state can validly preserve traversal position without proving integrity outcomes.

The rule is:

> **completion evidence should not be promoted across abstraction layers without an explicit source-backed handoff.**

### E — exclusion/admission state changes what `complete` means

Data General's later page-inhibit evidence and HDFS's handling of no-longer-present/racing blocks show that a maintenance traversal is defined over an admitted target set, not necessarily every carrier that ever existed.

Therefore:

> **coverage completeness depends on the current target-set definition.**

---

## 11. Relationship to maintenance-control state

Synthesis 26 classifies maintenance-control state by persistence horizon and restart strategy. The present comparison adds another audit axis:

> **What proposition does the control state actually justify?**

Examples:

```text
LPDDR2 bank counter
    -> next-target / sequencing coherence
    != proof of all historical refreshes

Data General sniff address
    -> rotating target selection
    != permanent integrity certificate

HDFS cursor
    -> traversal restart position
    != per-block success ledger

ESS completion message
    -> named scrub completion at system/vdisk layer
    != hidden controller/NAND completion proof
```

This yields a useful refinement:

```text
control-state persistence horizon
    + semantic role
    + coverage referent
    + evidence scope
        -> defensible completion claim
```

Retaining more metadata is not automatically stronger if its semantics do not support the proposition being asserted.

---

## 12. Failure and restart boundary

Coverage can also be interrupted. The cases show three different consequences without supporting one universal policy.

### LPDDR2

RESET or self-refresh exit can resynchronize the per-bank count. The source-backed claim is a regime coordination rule, not durable exact refresh-history persistence.

### Data General

The bounded source set establishes recurrent scheduling but does not justify a cross-power exact sniff-frontier checkpoint claim.

### HDFS

Cursor loss can fall back to a fresh iterator, trading repeated work for conservative renewed coverage. A malformed or stale progress coordinate need not be trusted merely because it survived.

### Enterprise SSD / ESS

The operator-visible system guidance is about allowing named maintenance to run and observing bounded completion. It does not disclose an exact hidden SSD firmware checkpoint across every interruption.

Therefore:

> **exact maintenance frontier persistence is one possible implementation strategy, not a prerequisite for every defensible coverage contract.**

What matters is whether the post-interruption mechanism can safely re-establish the required coverage relation.

---

## 13. Anti-anachronism and prior-art boundary

This synthesis makes no historical continuity claim among the four case families.

It specifically rejects:

- `LPDDR2 REFpb is a form of scrubbing`;
- `Data General sniffing is an ancestor of HDFS BlockScanner`;
- `HDFS cursor files and DRAM bank counters are the same kind of checkpoint`;
- `IBM ESS scrub completion reveals SSD controller internals`;
- `one maintenance vocabulary migrated unchanged from semiconductor memory to distributed storage`.

The shared vocabulary here is analytical only:

> **local work / domain coverage / completion evidence** is a project comparison frame, not a recovered historical tradition.

Broad histories of DRAM refresh interfaces, ECC memory scrub, HDFS scanner evolution, and enterprise-SSD maintenance/runbook practice remain separate historical projects.

---

## 14. Bounded philosophical interpretation

### I — persistence can depend on renewed evidence, not only renewed matter

The four cases permit one restrained interpretive claim. Technical persistence can require repeated work over a domain, and the system may also need enough evidence to know whether that work has covered what it was supposed to cover.

That does not mean `memory requires proof` in a universal philosophical sense. Magnetic remanence or other quiescent states provide immediate counterexamples. The narrower result is:

> **in maintenance-dependent systems, persistence may include not only preservation work but a bounded relation between local acts, the domain they are meant to cover, and the evidence by which completion is recognized.**

This also makes `finished` a technical relation rather than a purely temporal adjective. A worker can stop, a command can complete, a pass can end, or a system can emit a completion message while stronger maintenance obligations at another layer remain outstanding.

---

## 15. Related-repository boundary

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for a cross-technology maintenance-coverage / refresh / scrub / scanner synthesis found no dedicated packet to reuse.

The repository split remains:

- `computing-archaeology` — broad LPDDR refresh-standard genealogy, Data General/IBM ECC-scrub history, HDFS scanner implementation evolution, enterprise SSD/product support chronology, controller internals, and production archaeology;
- `technical-retention` — the bounded cross-case relation among **local maintenance work, target-set coverage, progress state, completion evidence, and renewed obligation**.

This document therefore does not duplicate those broader technical histories.

---

## 16. Non-claims

This synthesis does **not** establish that:

1. all maintenance is pass-based;
2. all maintenance has a durable cursor;
3. all completed maintenance exposes a `done` bit or log record;
4. one `REFpb` refreshes every LPDDR2 bank;
5. eight arbitrary commands are equivalent to the documented ordered/full-cycle refresh relation;
6. Data General row refresh and ECC sniff are the same operation;
7. Data General's illustrative patent cadence is a universal product constant;
8. every physically present memory page belongs to the active sniff domain;
9. an HDFS cursor certifies successful verification of all earlier blocks;
10. a completed HDFS pass makes later verification unnecessary;
11. IBM ESS scrub completion proves every NAND cell was rewritten;
12. IBM ESS scrub completion proves every hidden SSD-firmware retention task completed;
13. powered time alone is completion evidence;
14. a vendor runbook interval is a physical failure deadline;
15. completion at one layer automatically closes obligations at every lower layer;
16. maintenance coverage implies sanitization;
17. maintenance coverage implies archival completeness;
18. maintenance coverage implies cryptographic authenticity;
19. the four systems share one terminology or genealogy;
20. a project-level analytical term used here was historical actor vocabulary.

---

## 17. Open edges

The bounded synthesis is complete, but several evidence questions remain open:

- direct controller/device traces that distinguish issued LPDDR refresh commands from full rolling-window coverage in named platforms;
- exact MV/4000 sniff traversal state and restart behavior beyond the current product/manual boundary;
- HDFS production evidence correlating cursor state, per-block outcomes, restart replay, and real coverage delay;
- stronger completion telemetry for device-local SSD retention refresh rather than only system-layer scrub/runbook evidence;
- cross-layer handoff contracts where system scrub completion explicitly depends on lower-device self-test/refresh completion;
- starvation and fairness: whether a target can remain indefinitely uncovered even while aggregate maintenance activity is high;
- quantitative comparison of coverage age distributions rather than nominal pass/window settings;
- whether some future case requires a controlled distinction between **coverage completeness**, **coverage freshness**, and **coverage confidence** beyond the bounded framework here.

These are follow-up slices, not blockers for the current relation decomposition.