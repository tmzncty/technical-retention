from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

synthesis_path = ROOT / "docs/SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md"
if synthesis_path.exists():
    raise SystemExit(f"refusing to overwrite existing {synthesis_path.relative_to(ROOT)}")

synthesis = r'''# Synthesis 24 — Retention Maintenance Regimes: Trigger, Obligation, and Response

> **Question:** when a retained state needs work in order to remain usable, what makes that work become due?

**Status:** bounded cross-case synthesis over already-grounded evidence. This document formalizes a project vocabulary requested by the roadmap; it does not add an invention-priority claim or assert one historical lineage among delay-line memory, magnetic core, DRAM, Flash/SSD, RAID, or distributed repair.

Grounded cases used here:

- [`01 — Mercury delay-line circulation`](../cases/01-mercury-delay-line-circulation.md) — continuing circulation, regeneration, retiming, and environmental control;
- [`02 — Magnetic-core destructive read`](../cases/02-magnetic-core-destructive-read.md) — quiescent remanence plus access-triggered restore in the bounded classic scheme;
- [`03 — DRAM scheduled restoration`](../cases/03-dram-refresh-as-scheduled-restoration.md) — access restore plus elapsed-time/deadline regeneration;
- [`04 — Mapped Flash`](../cases/04-flash-virtual-mapping-logical-identity.md) — quiescent cell retention plus capacity/reclaim-driven relocation and erase;
- [`36 — NAND Flash correct-and-refresh`](../cases/36-nand-flash-correct-and-refresh-maintenance.md) — renewal whose policy can compose elapsed time, wear, and error evidence;
- [`76 — JESD218 SSD endurance/retention qualification`](../cases/76-jedec-ssd-endurance-retention-qualification.md) — workload/endurance history composed with later power-off retention qualification;
- [`111 — Enterprise SSD extended shutdown`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md) — wear/lifetime and powered-maintenance admission at the deployed-product layer;
- [`17 — RAID parity reconstruction`](../cases/17-raid-parity-reconstruction-degraded-repair.md) — failure-triggered reconstruction and restoration of redundancy margin.

Case 05 RADOS, the access-disturbance cases in Synthesis 11, and other mature cases are used only as bounded counterexamples where noted. The historical claims remain sourced in the individual case/evidence records. The regime names below are **project-controlled engineering terms** unless a source independently uses the same word.

---

## 1. Verdict

The roadmap's proposed distinction is useful, but only under a strict rule:

> **A retention-maintenance regime classifies a particular retained relation by the condition that makes preservation work due. It does not classify an entire technology once and for all.**

The repository can therefore use the following seven regime terms:

1. **quiescent retention**;
2. **continuous maintenance**;
3. **access-triggered restoration**;
4. **deadline-driven maintenance**;
5. **capacity/reclaim-triggered maintenance**;
6. **wear/lifetime-triggered policy**;
7. **failure/repair-triggered maintenance**.

These are not mutually exclusive device classes. Magnetic core already gives a decisive counterexample: the same memory can be quiescent at rest and still owe restoration after a destructive read. DRAM can compose access-triggered restore with a separate elapsed-time refresh deadline. Managed Flash can combine quiescent cell state, capacity reclamation, wear-aware placement, and later refresh/renewal. RAID members can retain ordinary media state quiescently while array-level failure consumes redundancy margin and triggers rebuild.

A better analytical shape is therefore:

```text
retained target
    + bounded operating / failure condition
        ↓
maintenance obligation
        ↓
trigger basis
        ↓
evidence / control state, where needed
        ↓
response action
        ↓
current service / admissibility result
        ↓
remaining or restored future retention margin
```

The trigger and the response are separate axes. `rewrite`, `refresh`, `relocate`, `rebuild`, or `replace` does not by itself tell us why the work became due.

---

## 2. Claim discipline

This synthesis follows [`METHOD.md`](METHOD.md) and [`AGENTS.md`](../AGENTS.md).

- **H/P — historical / primary:** historical vocabulary, dates, mechanisms, and product/standard contracts remain in the grounded case records.
- **E — engineering reconstruction:** the seven regime names and the trigger/obligation decomposition are project analytical tools.
- **A — functional analogy:** saying that two systems perform maintenance after a trigger does not establish a shared physical mechanism or genealogy.
- **I — philosophical interpretation:** the final interpretation is downstream of the engineering distinctions and deliberately narrow.

The synthesis also preserves the project's anti-anachronism rule. `Continuous maintenance`, `deadline-driven maintenance`, and the other regime names are not retroactively attributed to Eckert, Mauchly, Wilkes, core-memory engineers, Dennard, M-Systems, JEDEC, IBM, NetApp, or the Berkeley RAID authors unless an individual source actually uses those words.

---

## 3. Why this is not a duplicate of Synthesis 11

[`SYNTHESIS_11_ACCESS_DISTURBANCE_MAINTENANCE.md`](SYNTHESIS_11_ACCESS_DISTURBANCE_MAINTENANCE.md) asks what happens when **access itself changes the retention problem**. It separates request target, physical effect scope, disturbance exposure, current correctness, remaining margin, trigger evidence, and later restore/refresh/reclaim response.

The present synthesis asks a different question:

> **Across the repository as a whole, what kinds of conditions can make retention work due, including cases where access is not the trigger at all?**

Synthesis 11 therefore becomes one important subcase rather than being restated here. Access-triggered restoration remains distinct from access-conditioned cumulative disturbance, and both remain distinct from time, capacity, wear, or failure triggers.

---

## 4. Regime table

| Project regime | What makes work due? | Grounded witness | What the label does **not** mean |
| --- | --- | --- | --- |
| **quiescent retention** | no recurring preservation action is constitutively due while the bounded retention conditions hold | Case 02 core at rest; Case 04 Flash cell state | immutable; maintenance-free under every access; archival forever; whole-system recoverability |
| **continuous maintenance** | the retained relation exists through continuing circulation/feedback/regeneration | Case 01 delay line | merely `powered`; periodic deadline refresh; one immutable carrier token survives |
| **access-triggered restoration** | a particular access disturbs/destroys the selected physical state enough that restore is owed as part of preserving it | Case 02; bounded Case 03 read/restore | cumulative read-disturb policy; elapsed-time refresh; all reads in the technology are destructive |
| **deadline-driven maintenance** | elapsed time / a bounded retention deadline makes restoration due even without a triggering foreground access | Case 03 DRAM | exact physical failure instant; proof every cell fails when the deadline is crossed |
| **capacity/reclaim-triggered maintenance** | obsolete-state accumulation, free-space pressure, or erase-unit reuse makes copy/erase/remap work due | Case 04 mapped Flash | leakage refresh; wear leveling; secure erase; evidence that current payload was already failing |
| **wear/lifetime-triggered policy** | accumulated use/wear/lifetime evidence changes placement, renewal cadence, future-retention admission, or retirement action | Cases 36, 76, 111 | immediate unreadability; one universal endurance clock; a raw-cell law inferred from service telemetry |
| **failure/repair-triggered maintenance** | a failure, missing member, or consumed redundancy margin creates reconstruction/re-replication/rebuild work | Case 17; functionally Case 05 | ordinary periodic refresh; backup; proof that current service was already unavailable |

The table is intentionally about **obligation timing and trigger basis**, not about one universal maintenance algorithm.

---

## 5. Quiescent retention

### Definition

**Quiescent retention** means that, for the retained relation and bounded environmental/operational conditions being discussed, no recurring preservation operation is constitutively required merely for elapsed time to pass.

Magnetic-core remanence supplies the clean early case. The core can retain a magnetic state without holding power, yet the same bounded classic scheme can destroy the selected state during readout and then require rewrite. Mapped Flash similarly gives nonvolatile cell state while the logical store above it still depends on mapping metadata, reclamation, ECC, controller procedures, and later maintenance.

Therefore:

> **quiescent retention ≠ immutable state**

and

> **quiescent retention ≠ maintenance-free system**.

The regime applies to one relation under stated conditions. It says nothing by itself about access disturbance, explicit reset, erase, mapping loss, reader compatibility, or long-term environmental degradation.

---

## 6. Continuous maintenance

### Definition

**Continuous maintenance** means that continuing operation is constitutive of the current retained relation: circulation, feedback, regeneration, retiming, or an equivalent recurrent process must keep occurring for the state to persist as that relation.

Case 01 is the canonical witness. The mercury delay-line bit pattern survives because pulse sequences keep propagating and are detected, reshaped, retimed, and recirculated. The logical pattern persists through corrected successors rather than by leaving one physical pulse untouched.

This must remain distinct from deadline-driven DRAM refresh:

```text
continuous maintenance:
    the retained relation is a continuing process

deadline-driven maintenance:
    a state may sit between restoration events,
    but work must recur before a bounded deadline
```

Both can look `periodic` from a distance, but their obligation structure is different.

> **continuous maintenance ≠ deadline-driven maintenance**.

---

## 7. Access-triggered restoration

### Definition

**Access-triggered restoration** means that a particular access creates a near-immediate preservation obligation because the selected physical state has been disturbed or destroyed by the read path.

Classic destructive-read magnetic core is the cleanest bounded witness: a read that must leave the logical value retained owes a rewrite/restore. Dennard's bounded dynamic-cell evidence separately permits read-triggered restoration in addition to elapsed-time regeneration.

The label is deliberately narrower than `access-conditioned maintenance`. Synthesis 11 shows that NAND read disturb and RowHammer can let the current access succeed while consuming future margin elsewhere; those regimes may be driven by accumulated access history rather than requiring restoration as part of the single access itself.

Therefore:

> **access-triggered restoration ≠ access-count-triggered preventive maintenance**

and

> **access-triggered restoration ≠ deadline-driven maintenance**.

---

## 8. Deadline-driven maintenance

### Definition

**Deadline-driven maintenance** means that preservation work is due because elapsed time is approaching a bounded retention/service deadline, even if the state has not just been accessed.

Case 03 DRAM grounds the canonical form: leakage makes periodic regeneration necessary for reliable service. A quiet row still owes restoration on the schedule.

Two limits matter.

First, the service deadline is not an exact microscopic loss timestamp. Case 127 later shows that residual DRAM state can outlive ordinary service guarantees after refresh/power withdrawal. So:

> **maintenance deadline ≠ physical failure instant**.

Second, later adaptive designs can make the deadline itself policy-dependent. Case 93's VRT work and Case 36's Flash renewal show that time can be combined with profile, wear, or error evidence. The existence of hybrids does not erase the usefulness of a time-triggered axis.

---

## 9. Capacity/reclaim-triggered maintenance

### Definition

**Capacity/reclaim-triggered maintenance** means that preservation work becomes due because obsolete physical embodiments occupy erase/reuse units and writable/free capacity has to be recovered while current state is preserved.

Case 04 gives the bounded mapped-Flash relation:

```text
current + obsolete blocks share an erase unit
        ↓
current blocks are copied / transferred
        ↓
old unit is erased / freed
        ↓
mapping / allocation state is updated
```

The work can preserve current logical state while destroying obsolete physical embodiments, but the trigger is not primarily that current cells are decaying.

This is why the controlled vocabulary already insists:

> **reclamation ≠ wear leveling**.

The present synthesis adds another guardrail:

> **capacity reclamation ≠ decay refresh**.

A reclaim cycle may happen to rewrite current data and thereby renew its embodiment, but that side effect does not make free-space pressure historically identical to a retention-time deadline.

---

## 10. Wear/lifetime-triggered policy

### Definition

**Wear/lifetime-triggered policy** means that accumulated use, program/erase burden, endurance history, rated-life state, or another lifetime estimate changes the maintenance or admission decision applied to future retention.

This regime is intentionally broader than `wear leveling` and narrower than `anything that ages`.

- Case 36's FCR evidence makes P/E history one input to renewal cadence/policy.
- Case 76 composes host-visible TBW/workload history with a subsequent power-off retention qualification contract.
- Case 111 shows deployed-product telemetry withdrawing confidence in long powered-off retention as rated life is consumed, even when the SSD is not yet declared immediately failed.

Thus:

> **wear/lifetime threshold ≠ present payload failure**.

A system can still read current data while a retained wear estimate changes what future offline interval is considered safe or when the operator should replace the device.

The trigger evidence can be model-derived rather than a direct measurement of every physical cell. `Rated Life Used`, P/E count, TBW, spare consumption, and measured error rate are not interchangeable variables.

---

## 11. Failure/repair-triggered maintenance

### Definition

**Failure/repair-triggered maintenance** means that an actual failure, missing member, lost replica, or consumed redundancy margin creates work whose purpose is to reconstruct state and/or restore the intended future failure tolerance.

Case 17 is the canonical coded-storage witness. After one RAID member fails, a requested contribution can remain reconstructable and service can continue in degraded mode, while background reconstruction still owes restoration of the array's ordinary redundancy margin.

This gives a strong boundary:

> **current service availability ≠ maintenance completion**.

The trigger is also distinct from ordinary recurring refresh. Rebuild is exceptional with respect to a declared failure state, even if the system later performs the repair automatically in the background.

Case 05 RADOS supplies a functionally similar but historically and mechanically different distributed example: failure/membership changes can trigger re-replication from surviving current replicas. That analogy does not turn parity reconstruction and replica repair into one mechanism.

---

## 12. Trigger regime ≠ response mechanism

A major reason to formalize the taxonomy is to stop inferring cause from the name of the response.

The same broad response can serve different trigger regimes:

| Response | Possible trigger classes in grounded cases |
| --- | --- |
| rewrite / restore | destructive read; elapsed-time deadline; retention/error evidence |
| relocate / remap | capacity reclamation; wear distribution; bad-block/failure response; refresh policy |
| refresh | elapsed-time deadline; targeted disturbance policy; vendor/product renewal policy |
| rebuild / reconstruct | device/member failure; missing fragment; changed placement/redundancy state |
| replace / retire | failure; depleted spare capacity; rated-life/offline-retention admission policy |

Conversely, one trigger class can produce multiple responses. A wear/lifetime condition might change placement, shorten a refresh interval, request retirement, or merely warn an operator.

Therefore:

> **trigger regime ≠ response mechanism**.

This is an engineering reconstruction across already-grounded cases, not a historical vocabulary claim.

---

## 13. Evidence/control state ≠ payload state

Many regimes need retained evidence about whether maintenance is due:

- a refresh counter or row pointer;
- a mapping/free-space relation;
- read-count or error evidence;
- wear/endurance telemetry;
- validity/currentness metadata;
- reconstruction progress;
- failure/membership state.

Those states can be retention infrastructure without being the user payload they protect.

Case 111 is especially useful because rated-life telemetry can change future-retention admission while the current payload remains readable. Case 17 similarly treats rebuild progress as constitutive `meta state` while the user data are a separate retained target.

> **maintenance evidence ≠ maintained payload**.

And, following Case 93/Synthesis 11:

> **evidence survival ≠ evidence authority**.

A retained counter, profile, or health estimate can itself become stale, incomplete, or model-dependent.

---

## 14. One technology can occupy several regimes

The taxonomy fails if it is used as `one device → one box`. The grounded cases force composition.

### Magnetic core

```text
at rest:
    quiescent remanent retention

on destructive read:
    access-triggered restoration

on explicit clear/reset:
    deliberate state transition, not a retention-maintenance regime
```

### DRAM

```text
on selected destructive read in the bounded 1T1C relation:
    access-triggered restoration

with elapsed time:
    deadline-driven maintenance

with RowHammer/VRT-era policies:
    workload/evidence-conditioned modifiers can alter urgency or target
```

### Managed Flash / SSD

```text
cell state at rest:
    quiescent retention

obsolete-space accumulation:
    capacity/reclaim-triggered maintenance

wear/endurance history:
    wear/lifetime-triggered policy

retention/error evidence:
    time/evidence/wear-conditioned renewal can be composed
```

### RAID / replicated storage

```text
ordinary member/media state:
    may be quiescent at the component layer

member/replica loss:
    failure/repair-triggered maintenance at the redundancy layer
```

The regime label therefore always needs a **target and layer**.

---

## 15. Orthogonal modifiers: evidence and environment

The seven roadmap regimes are useful but should not be promoted into an exhaustive ontology of every future trigger.

Two recurrent dimensions are better treated as **orthogonal modifiers** for now:

- **evidence-conditioned** — measured/corrected error state, counters, profiles, telemetry, checksums, or policy evidence changes when maintenance is due;
- **environment-conditioned** — temperature, power regime, or another operating condition changes retention validity or maintenance policy.

Case 36 combines time, P/E wear, and error evidence. Case 93 combines an existing refresh regime with runtime evidence that can reclassify rows. Case 132 shows that temperature can change retention qualification and operation validity without becoming one universal `temperature-triggered refresh` mechanism.

Keeping these as modifiers avoids inventing a new top-level regime for every sensor or policy input while preserving the evidence that real systems compose clocks and conditions.

---

## 16. Anti-anachronism and prior-art boundary

This synthesis makes **no origin claim** for maintenance categories.

Chronological precedence does not create genealogy:

```text
delay-line circulation
    ≠ ancestor mechanism of DRAM refresh

magnetic-core destructive restore
    ≠ ancestor mechanism of NAND refresh/reclaim

Flash reclamation
    ≠ ancestor mechanism of RAID rebuild
```

Likewise, shared words do not create identity. `refresh`, `restore`, `scrub`, `reclaim`, `rebuild`, `regenerate`, and `repair` have period- and system-specific meanings.

> **shared maintenance vocabulary ≠ shared trigger ≠ shared physical mechanism ≠ shared genealogy**.

The purpose of the project taxonomy is comparison after source-specific histories are established, not retrospective renaming of those histories.

---

## 17. Bounded philosophical interpretation

### I — technical persistence can impose different kinds of time

The grounded mechanisms support a narrow philosophical result: the work that keeps a technical state available need not obey one privileged temporality.

A state can be:

- stable while nothing happens;
- maintained by continuous recurrence;
- restored because it was accessed;
- restored before a deadline;
- moved because capacity must be reclaimed;
- requalified because wear history changed its future margin;
- rebuilt because a failure consumed redundancy.

This makes `persistence` a poor synonym for `unchanging endurance`. But the cases do **not** show that every retained state is secretly one form of continuous operation, nor that these engineering clocks are one universal philosophy of memory.

The safe interpretive claim is only:

> **technical retention can be constituted by differently triggered obligations whose timing changes what it means for a state to remain available.**

---

## 18. Related-repository boundary

[`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) remains the home for broad histories of delay-line circuitry, core-memory selection, DRAM generations, Flash/SSD controllers, RAID hardware, and product genealogy. A fresh companion-repository search for a cross-technology `retention maintenance / refresh / reclamation / repair` taxonomy did not reveal a dedicated overlapping synthesis to reuse.

That division of labor is deliberate:

- `computing-archaeology` — how each historical mechanism worked and why it made engineering sense in its period;
- `technical-retention` — what the mature cases jointly force us to distinguish about the conditions of persistence.

The present document therefore keeps only the bounded cross-case regime vocabulary and routes future broad mechanism genealogy outward.

---

## 19. Roadmap closure and open edges

This synthesis closes the roadmap question of whether the project should **formally distinguish**:

- quiescent retention;
- continuous maintenance;
- access-triggered restoration;
- deadline-driven maintenance;
- capacity/reclaim-triggered maintenance;
- wear/lifetime-triggered policy;
- failure/repair-triggered maintenance.

The answer is **yes, as relation-and-trigger classes, not mutually exclusive technology classes**.

Still open:

- whether later case pressure justifies promoting `evidence-conditioned` or `environment-conditioned` from modifiers to top-level regimes;
- quantitative energy/labor comparison among maintenance regimes;
- named-controller and production fault-injection evidence for several Flash/SSD/RAID responses;
- deeper histories of the words `refresh`, `restore`, `rebuild`, `scrub`, and `reclaim` in their own technical communities;
- whether additional regimes are needed for migration/obsolescence work where no physical failure has yet occurred.

The taxonomy should be revised when grounded counterexamples expose a bad distinction. It is a working research instrument, not a closed universal ontology.
'''

synthesis_path.write_text(synthesis, encoding="utf-8")

# README navigation: insert after Synthesis 23 and before the heuristic warning.
readme_path = ROOT / "README.md"
readme = readme_path.read_text(encoding="utf-8")
if "SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md" in readme:
    raise SystemExit("README already contains Synthesis 24")
readme_anchor = "\n\nThis chain is a **research heuristic**, not a claim that all of these mechanisms are historically or philosophically identical."
readme_insert = """

A bounded retention-maintenance regime synthesis is now available in [`docs/SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md`](docs/SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md). Across grounded delay-line, magnetic-core, DRAM, mapped-Flash/Flash/SSD, and RAID cases it formally separates quiescent retention, continuous maintenance, access-triggered restoration, deadline-driven maintenance, capacity/reclaim-triggered maintenance, wear/lifetime-triggered policy, and failure/repair-triggered maintenance. It fixes the counterexamples `quiescent ≠ immutable`, `continuous maintenance ≠ deadline refresh`, `access-triggered restore ≠ deadline maintenance`, `reclamation ≠ decay refresh`, `wear threshold ≠ present failure`, and `service available ≠ maintenance complete`, while treating these as relation/trigger classes rather than one label per technology.

This chain is a **research heuristic**, not a claim that all of these mechanisms are historically or philosophically identical."""
if readme.count(readme_anchor) != 1:
    raise SystemExit(f"README anchor count is {readme.count(readme_anchor)}, expected 1")
readme = readme.replace(readme_anchor, readme_insert, 1)
readme_path.write_text(readme, encoding="utf-8")

# ROADMAP: close exactly the still-open formal-regime question.
roadmap_path = ROOT / "ROADMAP.md"
roadmap = roadmap_path.read_text(encoding="utf-8")
old_roadmap = "- [ ] Should the project formally distinguish quiescent retention, continuous maintenance, access-triggered restoration, deadline-driven maintenance, capacity/reclaim-triggered maintenance, wear/lifetime-triggered placement, and failure/repair-triggered maintenance?"
new_roadmap = "- [x] Formally distinguish quiescent retention, continuous maintenance, access-triggered restoration, deadline-driven maintenance, capacity/reclaim-triggered maintenance, wear/lifetime-triggered policy, and failure/repair-triggered maintenance — bounded by [`docs/SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md`](docs/SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md): the taxonomy classifies a retained relation and the condition that makes preservation work due, not an entire technology; it separates trigger basis from response mechanism and permits one system to compose several regimes. Grounded Cases 01–04, 17, 36, 76, and 111 provide the main counterexamples. Evidence-conditioned and environment-conditioned policies remain orthogonal modifiers rather than a claim of exhaustive universal taxonomy, while broad mechanism and terminology genealogy remains routed to `computing-archaeology`."
if roadmap.count(old_roadmap) != 1:
    raise SystemExit(f"ROADMAP target count is {roadmap.count(old_roadmap)}, expected 1")
roadmap = roadmap.replace(old_roadmap, new_roadmap, 1)
roadmap_path.write_text(roadmap, encoding="utf-8")

# Controlled vocabulary: add the regime taxonomy without redefining historical source terms.
glossary_path = ROOT / "docs/GLOSSARY.md"
glossary = glossary_path.read_text(encoding="utf-8")
if "## retention-maintenance regime" in glossary:
    raise SystemExit("GLOSSARY already contains retention-maintenance regime")
glossary_anchor = """## refresh

Periodic restoration required because the physical state would otherwise decay or become unreliable.

Refresh is not merely maintenance performed after failure. In some systems it is **constitutive of ordinary persistence**.

## remanence"""
glossary_replacement = """## refresh

Periodic restoration required because the physical state would otherwise decay or become unreliable.

Refresh is not merely maintenance performed after failure. In some systems it is **constitutive of ordinary persistence**.

## retention-maintenance regime

A project-controlled classification of **what condition makes preservation work due for a particular retained relation**. It is not a historical actor's vocabulary, not a device taxonomy, and not a rule that one technology belongs to only one regime.

The current bounded regime terms are:

- **quiescent retention** — no recurring preservation action is constitutively due while the stated retention conditions hold;
- **continuous maintenance** — continuing circulation, feedback, regeneration, or an equivalent process constitutes the retained relation;
- **access-triggered restoration** — a particular access creates an immediate/near-immediate restore obligation for the selected state;
- **deadline-driven maintenance** — elapsed time or a retention deadline makes work due even without a foreground access;
- **capacity/reclaim-triggered maintenance** — obsolete-state accumulation or free-space/reuse pressure makes copy/erase/remap work due while current state is preserved;
- **wear/lifetime-triggered policy** — accumulated use, wear, endurance, or lifetime evidence changes placement, renewal, admission, retirement, or replacement policy;
- **failure/repair-triggered maintenance** — a failure, missing member, or consumed redundancy margin creates reconstruction/re-replication/rebuild work.

A regime label identifies the **trigger/obligation relation**, not the response mechanism. Rewrite, relocation, refresh, rebuild, or replacement can answer different triggers. One system can compose several regimes at different layers or times. `Evidence-conditioned` and `environment-conditioned` may be used as orthogonal modifiers where grounded rather than promoted automatically into new universal classes.

See [`SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md`](SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md).

## remanence"""
if glossary.count(glossary_anchor) != 1:
    raise SystemExit(f"GLOSSARY anchor count is {glossary.count(glossary_anchor)}, expected 1")
glossary = glossary.replace(glossary_anchor, glossary_replacement, 1)
glossary_path.write_text(glossary, encoding="utf-8")

# CASE_INDEX: append bounded synthesis findings after the current 2500 endpoint.
case_index_path = ROOT / "CASE_INDEX.md"
case_index = case_index_path.read_text(encoding="utf-8")
if "## Synthesis 24 — retention-maintenance trigger-regime findings" in case_index:
    raise SystemExit("CASE_INDEX already contains Synthesis 24")
if "**2500 — future-retention authority can be withdrawn while physical embodiment survives." not in case_index:
    raise SystemExit("CASE_INDEX no longer has expected finding 2500 endpoint")
findings = r'''

## Synthesis 24 — retention-maintenance trigger-regime findings

Evidence basis: grounded Cases 01–04, 17, 36, 76, and 111, with Synthesis 11 and Case 05 used only as bounded comparison/counterexample controls. Cross-case regime names are project engineering terms, not retroactive historical vocabulary.

- **2501 — retention-maintenance regime classifies a retained relation and trigger, not an entire technology.** The same device/system can occupy several regimes at different layers or times. (`E`)
- **2502 — quiescent retention ≠ immutable or universally maintenance-free retention.** Magnetic core and Flash can retain physical state at rest while access, reset, mapping, reclamation, environmental control, or later renewal still create other obligations. (`E`, `X`)
- **2503 — continuous maintenance ≠ deadline-driven maintenance.** Delay-line circulation constitutes the retained relation through continuing recurrence, whereas DRAM can retain state between restoration events but owes work before an elapsed-time deadline. (`E`, `A`, `X`)
- **2504 — access-triggered restoration ≠ deadline-driven maintenance.** A destructive read can create an immediate restore obligation even when no elapsed-time deadline caused the access; leakage-driven refresh can become due without any foreground access. (`H/P` inherited, `E`)
- **2505 — capacity/reclaim-triggered maintenance ≠ decay refresh.** Mapped-Flash reclamation can copy current blocks and erase an old unit because free/reusable capacity is needed, without establishing that the current payload had reached a physical retention deadline. (`H/P` inherited, `E`, `X`)
- **2506 — wear/lifetime-triggered policy ≠ present payload failure.** P/E history, TBW/rated-life state, or related telemetry can shorten renewal intervals, change future-retention admission, or trigger replacement before current service becomes unreadable. (`H/P` inherited, `E`, `X`)
- **2507 — failure/repair-triggered maintenance ≠ ordinary recurring maintenance.** RAID reconstruction and replica repair become due after failure/redundancy loss; their purpose is to restore an embodiment or future failure margin rather than satisfy a normal refresh clock. (`H/P` inherited, `E`, `A`)
- **2508 — trigger regime ≠ response mechanism.** Rewrite, refresh, relocation, rebuild, or replacement can answer different trigger classes, so the action name alone does not identify why preservation work became due. (`E`)
- **2509 — maintenance evidence/control state ≠ maintained payload.** Maps, counters, profiles, wear estimates, validity state, failure state, and rebuild progress can govern preservation work without being the user data they protect. (`E`)
- **2510 — maintenance clock/deadline ≠ physical failure instant.** A specified refresh interval, endurance threshold, or maintenance envelope is an operational/qualification boundary, not automatically the timestamp at which every physical embodiment becomes unreadable. (`H/P` inherited, `E`, `X`)
- **2511 — current service availability ≠ maintenance completion or restored future margin.** Degraded RAID service, ECC-correctable Flash reads, or a currently readable worn SSD can coexist with outstanding rebuild, renewal, or replacement obligations. (`H/P` inherited, `E`)
- **2512 — one medium/system can compose multiple regimes without contradiction.** Core can be quiescent at rest plus access-restored; DRAM can be access-restored plus deadline-refreshed; managed Flash can combine quiescent cells, reclamation, wear-aware policy, and renewal; RAID can combine quiescent component media with failure-triggered array repair. (`E`, `A`)
- **2513 — evidence-conditioned and environment-conditioned policy are orthogonal modifiers, not yet universal top-level device classes.** Cases 36, 93, and 132 show clocks combined with error/profile/wear/temperature evidence without forcing one new regime for every sensor or condition. (`E`, `A`)
- **2514 — shared maintenance vocabulary ≠ shared trigger, physical mechanism, or genealogy.** `Refresh`, `restore`, `scrub`, `reclaim`, `rebuild`, and `repair` remain source- and system-specific even when the project compares their retention role. (`H/P` inherited, `A`, `X`)
- **2515 — related-repository boundary remains explicit.** A fresh `computing-archaeology` search found no dedicated cross-technology retention-maintenance trigger taxonomy to reuse; broad histories of delay lines, core, DRAM, Flash/SSD, RAID hardware, and maintenance terminology remain routed there, while Synthesis 24 keeps the cross-case relation vocabulary. (`H/P` project-state record)
'''
case_index = case_index.rstrip() + findings + "\n"
case_index_path.write_text(case_index, encoding="utf-8")

print("Synthesis 24 canonical files generated/updated")
