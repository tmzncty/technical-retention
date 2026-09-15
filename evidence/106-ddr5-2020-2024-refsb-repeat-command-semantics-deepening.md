# DDR5 2020–2024 REFsb repeat-command and transition semantics deepening

Status: **bounded deepening complete**

Canonical case: [`../cases/106-ddr5-same-bank-refresh-parallel-target-set.md`](../cases/106-ddr5-same-bank-refresh-parallel-target-set.md)

## Bounded question

The existing Case 106 grounding establishes the December 2017 proposed-spec floor for DDR5 Same Bank Refresh (`REFsb`): one corresponding bank in each bank group is the maintenance target, target banks are unavailable during `tRFCsb`, non-target banks remain serviceable, and an internal-bank/global-refresh accounting relation tracks coverage.

This deepening asks a narrower historical and engineering question:

> Did the externally visible semantics of **repeating the same REFsb bank before all bank indices had been serviced** remain fixed between the proposed/final early DDR5 text and later standard/product documents? What does the answer imply for the distinction among command execution, physical refresh work, and maintenance-accounting progress?

A second bounded question follows from the same source family:

> What happens to incomplete same-bank-refresh accounting when the device crosses a refresh-mode or self-refresh transition that resets the internal bank counter?

The purpose is not to produce a complete DDR5 standards genealogy. It is to document one concrete semantic change/continuity chain and the retention-control boundary it exposes.

## Source ladder

### A — December 2017 proposed DDR5 Full Spec Rev0.1

Existing repository grounding:

- [`106-ddr5-2017-2023-same-bank-refresh-grounding.md`](106-ddr5-2017-2023-same-bank-refresh-grounding.md)
- public mirror: <https://www.pedestrian.com.cn/_downloads/4928176668e6494cc99abfb887fdf326/DDR5_JESD79-5.pdf>

Relevant proposed-spec rule:

- REFsb may be issued in any bank order;
- every bank index must receive one REFsb before the same bank may receive another;
- an early repeat is described as **illegal**;
- the global refresh counter advances only after all bank indices have been covered.

This is a proposed-standards primary text, not the final standard.

### B — JESD79-5 initial DDR5 standard, July 2020

Public mirror:

<https://github.com/RAMGuide/TheRamGuide-WIP-/blob/main/DDR5%20Spec%20JESD79-5.pdf>

The mirrored JESD79-5 text in §4.13.3 retains the early-repeat restriction. It says REFsb may be issued in any bank order, but every bank must receive one REFsb before a bank may receive a subsequent REFsb; repeating a bank before all banks are covered is described as **illegal**.

A standards catalog identifies the initial JESD79-5 publication date as July 2020 and records later revisions JESD79-5A (October 2021) and JESD79-5B (September 2022):

<https://standards.globalspec.com/std/14328154/jedec-jesd-79-5>

The catalog is used only for revision chronology. The command semantics come from the standard text mirror.

### C — JESD79-5B_v1.20, September 2022

Public text mirror:

<https://studylib.net/doc/27611087/jesd79-5b-v1>

The same §4.13.3 relation is worded differently in JESD79-5B_v1.20. It still says:

- REFsb may be issued to any bank and in any bank order;
- the global refresh counter does not advance until all banks in a bank group have received REFsb.

But the consequence of an early repeat is no longer stated as an illegal command. Instead, the text says a subsequent REFsb to the same bank before every bank has received one **repeats refreshing the same row**, because the global refresh counter has not advanced.

The same section states that a REFab issued while the same-bank internal counter is nonzero resets that counter and the incomplete REFsb credits do not advance the global refresh counter.

The standards catalog gives JESD79-5B a September 2022 publication date:

<https://standards.globalspec.com/std/14562454/JESD79-5B>

### D — JESD79-5B refresh-mode and self-refresh transition rules

The same JESD79-5B_v1.20 text provides two explicit transition cases.

#### D1. Changing refresh mode

When operating with REFsb, the standard recommends reaching a complete/even same-bank condition before changing refresh mode because the transition path resets same-bank accounting. If the condition is not met, an extra REFab is required after the mode change. The extra command is not counted toward average `tREFI` computation, while still interacting with postponed-refresh limits.

#### D2. Entering/exiting self refresh

For REFsb, the standard recommends that all banks receive REFsb before entering Self Refresh because entering/exiting Self Refresh resets the internal bank counter. If the pre-entry condition is not met, after Self Refresh exit the host must issue either:

- one extra REFab; or
- an extra REFsb to each bank.

The same figures label incomplete pre-transition same-bank commands as receiving **no credit** after the transition and show compensating extra commands.

Thus the document itself distinguishes physical refresh commands that occurred before the transition from maintenance-accounting credit that survives the transition boundary.

### E — SK hynix DDR5 16 Gb A-die product specification, Rev. 1.1

Public product-document mirror:

<https://uttc.com.tw/wp-content/uploads/2025/12/Consumer_CP16GD5_H5CG448%EF%BC%866AGBDJXxxx_Rev.1.1_1anm.pdf>

The SK hynix product specification carries the later JESD79-5B-style semantics:

- REFsb targets a specific bank in each bank group;
- REFsb can be issued to any bank and in any bank order;
- an early repeated REFsb refreshes the same row again because the global refresh counter has not advanced;
- the internal bank counter resets when every bank is covered, on RESET, on entering/exiting Self Refresh, or on REFab;
- incomplete REFsb progress before Self Refresh requires compensating refresh after exit.

This is useful as a named-vendor product contract. It does not establish which internal circuit implements the counters and does not by itself prove the behavior of every DDR5 device.

### F — Micron DDR5 SDRAM product core specification, Rev. E, November 2024

Public product-document mirror:

<https://www.avnet.com/wcm/connect/dacdfea7-999f-4ee0-b514-6f9e0bf68c6d/ddr5-sdram-core.pdf?MOD=AJPERES>

The document identifies itself as Micron's DDR5 SDRAM product core specification, Rev. E 11/2024, and as JESD79-5C compliant. Its Same Bank Refresh section likewise states that an early REFsb repeat refreshes the same row because the device global refresh counter does not advance until all banks in the group have received REFsb.

This provides later cross-vendor product-era continuity for the 5B-style rule.

## Historical record

### H1 — 2017 proposed text and 2020 initial standard both prohibit the early repeat

The existing 2017 grounding and the mirrored July 2020 JESD79-5 text agree on the essential early rule:

```text
bank order may vary
    but
bank i cannot be repeated
    until
all bank indices have received one REFsb
```

The early repeat is not merely described as unhelpful; the standard text calls it illegal.

Therefore the repository can now move beyond the weaker statement that the 2017 proposal happened to contain this restriction. The restriction survived into the initial published DDR5 standard.

This is a **publication-floor** result. It is not invention priority.

### H2 — by JESD79-5B in September 2022, the consequence is defined as redundant physical refresh rather than illegality

JESD79-5B_v1.20 keeps the same global-coverage invariant but changes the stated consequence of repeating too early:

```text
early repeated REFsb
    -> same bank is refreshed again
    -> same row is refreshed again
    -> global refresh counter does not advance
```

The command therefore can perform physical maintenance work without earning new coverage progress.

The source set used in this run does **not** establish whether this exact wording first appeared in JESD79-5A (October 2021), an intermediate editorial draft, or JESD79-5B itself. The bounded chronology is only:

```text
July 2020 JESD79-5:
    early repeat explicitly illegal

September 2022 JESD79-5B:
    early repeat has defined redundant-refresh behavior
```

The transition occurred no later than JESD79-5B, but the exact ballot/revision that introduced it remains open.

### H3 — later vendor product documents preserve the 5B-style behavior

SK hynix's 16 Gb A-die product specification and Micron's 2024 DDR5 core specification both describe the later behavior in product-facing terms: an early repeat can refresh the same row while the global row-address/refresh counter remains at the current position until the remaining bank indices receive service.

This is stronger than relying on one standards mirror alone because the semantics appear in independent vendor product-document families.

It still does not prove identical silicon implementation, internal state encoding, or timing behavior beyond the documented interface contract.

### H4 — incomplete REFsb credit is intentionally discarded across certain transitions

JESD79-5B and the SK hynix product specification both describe internal bank-counter reset conditions that include:

- RESET;
- entering/exiting Self Refresh;
- REFab;
- completing the bank-index coverage sequence.

When a transition occurs before the REFsb bank-index set is complete, already-issued REFsb commands may no longer count as surviving progress toward the next global refresh-counter step. The standard then prescribes compensating refresh after the transition.

This is not a generic claim that the device forgets all physical effects of the prior refreshes. The physical refresh events happened. What is lost/reset is **credit in the accounting relation used to advance the global refresh sequence**.

## Retained-state decomposition

This deepening benefits from separating at least seven layers:

1. **payload charge state** — the user data that periodic refresh must preserve;
2. **physical row just refreshed** — the row whose cells actually received restorative refresh work;
3. **REFsb target coordinate** — the bank index named by the command and applied across bank groups;
4. **per-sequence bank coverage relation** — which bank indices have already contributed one REFsb to the current synchronization set;
5. **internal bank-counter state** — the device-side accounting position associated with the set;
6. **global refresh / row-address progression** — the broader sequence that advances after sufficient same-bank coverage or REFab;
7. **transition compensation obligation** — extra REFab or per-bank REFsb work required when a reset/mode transition invalidates incomplete accounting credit.

Only item 1 is the application payload itself.

The remaining items are control, interpretation, and maintenance-accounting relations that help ensure recurring restoration covers the full retained set.

## Engineering reconstruction

### E1 — physical maintenance execution is not the same thing as maintenance-credit progress

The 5B-style early-repeat rule provides a particularly sharp counterexample to treating every completed maintenance command as new maintenance progress.

```text
REFsb accepted/executed
    -> target row is physically refreshed

but

same bank repeated before full bank-index coverage
    -> global refresh counter does not advance
```

Therefore:

> **maintenance work happened ≠ maintenance frontier advanced**.

This is an engineering reconstruction from the documented command/accounting semantics, not JEDEC terminology.

### E2 — redundant restoration can be safe locally while still failing to satisfy global coverage

Refreshing the same row again can improve or renew that row's charge state, yet it does not service the omitted bank indices for the current global row position.

So the later semantics expose two independent questions:

```text
Was useful restorative work performed somewhere?

versus

Did the operation reduce the outstanding full-device coverage obligation?
```

A controller that repeatedly refreshes one same-bank coordinate can keep doing real physical work while making no progress on the coverage dimension that matters for the omitted coordinates.

This is a bounded functional statement. It does not quantify how long omitted cells survive or model undocumented internal refresh grouping.

### E3 — the standards change is a change in admissible command behavior, not necessarily in retention physics

The 2020 text and 2022 5B text differ in what happens if software/controller scheduling presents the same bank again too early:

```text
2020 interface rule:
    reject/forbid the sequence as illegal

2022 5B interface rule:
    define the sequence's physical effect
    but with no new global-counter progress
```

Nothing in this evidence set demonstrates that DRAM-cell retention physics changed between those revisions.

A safer reading is that the **interface contract for handling a scheduling mistake/redundancy** became less prohibitive or more explicitly defined.

The exact committee motivation is not established here.

### E4 — reset of accounting state creates a compensating-maintenance obligation

The Self Refresh and refresh-mode transition rules show a second distinction:

```text
pre-transition REFsb physical work
    !=
post-transition surviving accounting credit
```

If the internal bank counter is reset before a synchronization set is complete, the host cannot simply resume as though the old partial coverage relation still existed. The standard requires compensating work.

Thus:

> **control-state reset ≠ payload loss, but control-state reset can create additional maintenance work needed to preserve the payload guarantee.**

### E5 — a safe transition can deliberately forget progress if it also repairs the obligation

The standard does not require preserving partial REFsb credit across Self Refresh entry/exit. It permits the accounting relation to reset, then restores safety by requiring extra refresh after the transition when necessary.

This gives a useful retention design pattern:

```text
preserve progress metadata across boundary
    OR
forget progress metadata
    + conservatively redo enough work
```

The DDR5 rule in this bounded case uses the second pattern for incomplete same-bank credit across the stated transition.

This is a functional reconstruction. It should not be generalized into a claim about all DDR5 internal state.

### E6 — command legality and command usefulness are revision-sensitive

A controller model built from the 2020 standard can legitimately treat an early repeated bank as a protocol violation. A model built from the 5B/product-era documents should instead represent a real but redundant refresh whose global progress remains unchanged.

Therefore:

> **DDR5 Same Bank Refresh semantics are revisioned protocol semantics, not a timeless one-line feature definition.**

This matters for simulators, validation environments, historical reconstruction, and fault-injection models. A model that flattens all DDR5 revisions into one behavior can manufacture either false illegality or false permissiveness.

## Functional comparison

### With Case 105 — LPDDR2 REFpb

Case 105's product evidence uses a fixed round-robin per-bank maintenance sequence in which a full per-bank cycle composes the broader obligation.

Case 106's later DDR5 REFsb semantics permit bank-order freedom and even define a redundant early repeat, while withholding global-row progress until all bank indices are covered.

The bounded comparison is:

```text
LPDDR2 REFpb:
    local transaction + constrained bank sequence

DDR5 REFsb (5B-era):
    parallel same-coordinate target set
    + flexible bank ordering
    + redundant repeat can execute
    + coverage progress waits for the complete bank-index set
```

This is functional comparison only. No direct implementation lineage is claimed.

### With Case 69 — refresh scheduling flexibility

Case 69 establishes that refresh timing can be postponed/pulled in within bounded windows. This deepening adds a different axis:

- timing flexibility asks **when** maintenance may be issued;
- REFsb coverage accounting asks **which target coordinates have earned progress credit**.

A controller can satisfy one axis while mishandling the other.

### With recovery/replay cases outside DRAM

The pattern `forget progress metadata + conservatively redo work` has functional parallels in crash recovery, scrub restart, and distributed repair cases elsewhere in the repository.

The comparison must remain structural:

- DDR5 REFsb counters are not a database WAL;
- Self Refresh exit is not a distributed-system crash recovery protocol;
- repeated refresh is not an idempotency proof for arbitrary maintenance systems.

## Historical interpretation boundary

### Historical record

Supported directly by period/standard/vendor documents:

- 2017 proposed DDR5 and July 2020 JESD79-5 describe early repeated REFsb as illegal;
- JESD79-5B_v1.20 describes it as repeating refresh of the same row without global-counter advance;
- later SK hynix and Micron product documents use the 5B-style rule;
- mode/Self Refresh transitions reset incomplete bank-counter progress and can require extra refresh.

### Engineering reconstruction

Inferred from those documented semantics:

- physical maintenance execution can be distinct from credited coverage progress;
- discarding maintenance-progress metadata can be safe if sufficient conservative maintenance is replayed;
- controller/simulator behavior must be keyed to the standard/product revision when modeling early repeats.

### Functional analogy

Permitted only at the structural level:

- redundant maintenance work resembles replayed maintenance that does not advance a logical frontier;
- transition compensation resembles conservative redo after progress metadata is discarded.

### Philosophical interpretation

A bounded conceptual reading is that a technical system can preserve an object not only by doing maintenance, but by maintaining an **account of what maintenance still counts toward the current obligation**.

That is present-day analytical vocabulary. JEDEC and the vendors are not being attributed a philosophical theory of memory, credit, or forgetting.

## Claim ledger

| Claim | Label | Evidence | Strength |
| --- | --- | --- | --- |
| December 2017 proposed DDR5 text treats an early repeated REFsb as illegal | H/P | existing Source A grounding | strong proposed-standard primary text |
| July 2020 initial JESD79-5 also treats an early repeated REFsb as illegal | H/P | Source B §4.13.3 mirror | strong final-standard text mirror |
| JESD79-5B_v1.20 says an early repeat refreshes the same row while global counter does not advance | H/P | Source C §4.13.3 | strong standard text mirror |
| by September 2022 DDR5 had defined behavior for the early repeat rather than only an illegality rule | H | Source C + publication chronology | strong bounded chronology |
| the exact change first appeared in JESD79-5A | X | not established | rejected pending 5A text/ballot genealogy |
| 2020→2022 wording change proves DRAM retention physics changed | X | not supported | rejected |
| later SK hynix product documentation carries the 5B-style repeat behavior | H/P | Source E §4.13.3 | strong vendor-product document |
| Micron Rev. E 11/2024 carries the 5B-style repeat behavior | H/P | Source F Same Bank Refresh section | strong vendor-product document |
| entering/exiting Self Refresh resets the REFsb internal bank counter | H/P | Source C §4.13.7; Source E | strong standard/vendor text |
| incomplete pre-Self-Refresh REFsb accounting can require extra REFab or per-bank REFsb after exit | H/P | Source C §4.13.7; Source E | strong standard/vendor text |
| a repeated REFsb can do physical refresh work without advancing global coverage | E | reconstruction from Source C/E/F | strong mechanism inference |
| losing/resetting partial REFsb credit means the payload was lost | X | contradicted by the compensation model | rejected |
| internal bank/global counters are necessarily nonvolatile physical registers with a particular circuit implementation | X | not established | rejected |
| all DDR5 revisions and devices share identical early-repeat semantics | X | contradicted by 2020 vs 5B wording | rejected |

## What this closes

This deepening boundedly closes three gaps in Case 106:

1. **final-standard continuity for the 2017 early-repeat restriction** — the rule is present in the initial July 2020 JESD79-5 text, not only the proposed 2017 draft;
2. **later semantic evolution** — by JESD79-5B in September 2022, an early repeat has defined redundant-refresh behavior rather than only an illegality statement;
3. **cross-vendor product-era corroboration** — later SK hynix and Micron product documents carry the 5B-style semantics and the transition-compensation model.

## What remains open

The following are still open and should not be silently inferred:

- the exact JESD79-5A or ballot/change item that first replaced the `illegal` rule with defined repeat behavior;
- committee motivation for the change;
- whether any 2020-era shipping DDR5 devices implemented permissive repeat behavior before the standard wording changed;
- exact vendor silicon/circuit implementation of the internal bank and global refresh counters;
- controller behavior in Intel/AMD/other memory controllers when software or hardware schedules redundant REFsb sequences;
- fault-injection tests around REFsb, RESET, refresh-mode change, and Self Refresh entry/exit;
- whether later JESD79-5C revisions further alter corner-case semantics beyond the continuity seen in Micron's 5C-compliant 2024 core specification.

A full revision/ballot genealogy belongs primarily in `tmzncty/computing-archaeology`; this repository should retain the bounded relation among maintenance execution, coverage credit, transition reset, and compensating maintenance.

## Related-repository check

A current GitHub search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `DDR5 REFsb Same Bank Refresh` returned no dedicated case. No technical-history module was available to reuse during this run.

If the standards genealogy is expanded, `computing-archaeology` should own:

- JESD79-5 / 5A / 5B / 5C clause-by-clause history;
- underlying JC-42.3 ballot identifiers and proposal lineage;
- controller implementation history;
- vendor-device chronology.

Case 106 should continue to own the retention-specific conclusion about maintenance target geometry, coverage accounting, and progress-state reset/replay.

## Sources

1. JEDEC JC-42.3 proposed material, _DDR5 Full Spec Draft Rev0.1_, 5 December 2017, §4.10.3 `Same Bank Refresh`; public mirror: <https://www.pedestrian.com.cn/_downloads/4928176668e6494cc99abfb887fdf326/DDR5_JESD79-5.pdf>.
2. JEDEC, _DDR5 SDRAM_, JESD79-5, July 2020, §4.13.3 `Same Bank Refresh`; public mirror: <https://github.com/RAMGuide/TheRamGuide-WIP-/blob/main/DDR5%20Spec%20JESD79-5.pdf>.
3. GlobalSpec standards catalog, `JEDEC JESD 79-5`, publication/revision chronology: <https://standards.globalspec.com/std/14328154/jedec-jesd-79-5>.
4. JEDEC, _DDR5 SDRAM_, JESD79-5B_v1.20, September 2022, especially §§4.13.2, 4.13.3, 4.13.7; public text mirror: <https://studylib.net/doc/27611087/jesd79-5b-v1>.
5. GlobalSpec standards catalog, `JESD79-5B`, publication date/history: <https://standards.globalspec.com/std/14562454/JESD79-5B>.
6. SK hynix, _DDR5 SDRAM 16Gb A-die_, Rev. 1.1, especially §§4.13.3 and 4.13.7; public product-document mirror: <https://uttc.com.tw/wp-content/uploads/2025/12/Consumer_CP16GD5_H5CG448%EF%BC%866AGBDJXxxx_Rev.1.1_1anm.pdf>.
7. Micron Technology, _DDR5 SDRAM Product Core Data Sheet_, Rev. E 11/2024, JESD79-5C-compliant core specification, Same Bank Refresh section; public mirror: <https://www.avnet.com/wcm/connect/dacdfea7-999f-4ee0-b514-6f9e0bf68c6d/ddr5-sdram-core.pdf?MOD=AJPERES>.
