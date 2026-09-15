# DDR5 Same-Bank REFRESH: Parallel Bank-Group Targets, Coverage Accounting, and Service Concurrency

## Status

**`grounded`** — bounded to a December 2017 proposed DDR5 full-spec draft carrying Q3'17 ballots, the July 2020 initial JESD79-5 publication, JESD79-5B_v1.20 (September 2022), and later Micron/SK hynix manufacturer product-era explanations. This case establishes the retention relation, a dated draft/final-standard floor, and one bounded revision-semantic change; it does **not** claim invention priority, identify the exact 5A/ballot change that introduced the later repeat-command behavior, or provide a complete JEDEC genealogy.

Grounding records:

- [`../evidence/106-ddr5-2017-2023-same-bank-refresh-grounding.md`](../evidence/106-ddr5-2017-2023-same-bank-refresh-grounding.md)
- [`../evidence/106-ddr5-2020-2024-refsb-repeat-command-semantics-deepening.md`](../evidence/106-ddr5-2020-2024-refsb-repeat-command-semantics-deepening.md)

## Scope

Case 105 established one LPDDR2 regime in which a `REFpb` transaction targets one bank, leaves other banks serviceable, and contributes to a rolling full-bank refresh obligation. The next bounded question is deliberately narrower than a DDR5 history:

> What changes when one refresh command targets the **same bank coordinate across every bank group in parallel**, while the device still owes refresh coverage across all bank coordinates over time?

The primary historical anchor is the proposed DDR5 Full Spec Rev0.1 dated 5 December 2017, which says it includes ballots through Q3'17 and contains section 4.10.3, `Same Bank Refresh`. The initial July 2020 JESD79-5 text retains the early rule that one bank may not be repeated before all bank indices receive REFsb. By JESD79-5B_v1.20 in September 2022, the same corner case has a defined redundant-refresh behavior: an early repeat refreshes the same row again but does not advance the global refresh counter. Later Micron and SK hynix product documents preserve that later behavior.

This case does not establish who originated Same Bank Refresh, which exact JESD79-5A/committee ballot changed the repeat-command rule, how every DDR5 controller schedules REFsb, or whether every vendor/device implements all optional details identically.

## Historical record

### H/P — The December 2017 proposed DDR5 draft already names and defines REFsb

The proposed DDR5 Full Spec Rev0.1 revision history is dated **12/5/17** and describes the draft as including all ballots through Q3'17. In section 4.10.3, the draft names `Same Bank Refresh command (REFsb)` and contrasts it with `All Bank Refresh command (REFab)`.

The draft states that REFsb applies refresh to a **specific bank in each bank group**, while REFab applies refresh to all banks in every bank group. It also restricts REFsb to Fine Granularity Refresh (`FGR`) mode in this draft.

The source is a public mirror of a proposed committee ballot/draft, not the final published standard. It therefore supplies a dated proposal/draft floor, not final normative or invention-priority proof.

### H/P — "Same bank" is a parallel target set, not one physical bank total

The same section says that, once REFsb is issued, the target banks — explicitly **one in each Bank Group** — are inaccessible for `tRFCsb`. Other banks in each bank group remain accessible/addressable during the same-bank-refresh cycle.

This matters because the phrase `same bank refresh` can be misread if detached from the bank-group geometry. The command does not select one unique bank for the entire device; it selects corresponding bank positions across bank groups.

### H/P — A full bank-index cycle remains part of refresh accounting

The 2017 draft retains an internal bank counter and a global refresh counter for this operation. It permits REFsb commands in any bank order, but requires every bank index to receive one REFsb before the same index may receive another. The first command establishes a synchronization sequence; after every bank index has received one REFsb, the synchronization count resets and the global refresh counter advances.

RESET, entering/exiting self refresh, and REFab also reset/synchronize the internal bank counter under the stated conditions. A REFab issued in the middle of same-bank refreshing does not automatically count as completion of that partial same-bank cycle for the global counter.

Thus one completed REFsb transaction and one completed refresh-accounting cycle are distinct events.

### H/P — The early-repeat rule survives into July 2020 JESD79-5, then changes by JESD79-5B

The initial July 2020 JESD79-5 publication retains the proposed-spec rule that every bank index must receive REFsb before one bank may be repeated; an early repeat is explicitly described as **illegal**.

JESD79-5B_v1.20, published in September 2022, keeps the same broad coverage invariant but changes the stated consequence. It says an early REFsb to a bank that already participated in the current sequence **repeats refreshing the same row**, because the global refresh counter does not advance until all banks in the group receive REFsb.

This produces a bounded revision chronology:

```text
2017 proposed draft + July 2020 JESD79-5:
    early repeat = illegal

September 2022 JESD79-5B:
    early repeat = defined redundant refresh
    global coverage frontier does not advance
```

The present source set does not establish whether the exact change first appeared in JESD79-5A (October 2021), an intermediate ballot, or JESD79-5B itself.

### H/P — Later SK hynix and Micron product documents preserve the 5B-style behavior

SK hynix's DDR5 16 Gb A-die product specification and Micron's DDR5 SDRAM product core specification carry the later rule: REFsb may be issued in flexible bank order, but repeating the same bank before all bank indices have received REFsb refreshes the same row again while the global refresh counter remains at the same row position.

Micron's Rev. E 11/2024 core document identifies itself as JESD79-5C compliant, providing later product-era continuity. These are independent vendor-document families, not proof of identical silicon implementation.

### H/P — Target-bank unavailability and non-target service remain part of the contract

The proposed draft and later manufacturer material agree that target banks are unavailable during their REFsb cycle while non-target banks remain accessible subject to the defined timing restrictions.

This directly supports:

- target-set maintenance ≠ whole-device blackout;
- non-target availability ≠ target-bank availability;
- command completion for one target set ≠ coverage completion across all bank indices.

### H/P — Transition boundaries can discard incomplete REFsb credit and require compensation

JESD79-5B states that entering/exiting Self Refresh resets the internal same-bank counter. It recommends completing the bank-index REFsb set before entry; if the set is incomplete, the host must issue either one extra REFab or an extra REFsb to each bank after Self Refresh exit.

The refresh-mode-change path similarly treats incomplete REFsb accounting conservatively and requires extra refresh work when the recommended pre-transition condition is not met.

The figures label incomplete pre-transition REFsb work as receiving `No credit` after the transition. That does **not** mean the earlier physical refresh operations did not occur. It means their partial accounting state is not carried through as completed progress toward the next global refresh-counter step.

### H/P — Scheduling flexibility is bounded

The source family permits bank indices to be serviced in flexible order and permits bounded refresh postponement/pull-in behavior, but full coverage still constrains progress. Under 5B-style semantics, an early repeat may execute rather than being illegal, yet it still does not substitute for the omitted bank indices.

Thus:

> **flexible order ≠ arbitrary progress**.

This extends Case 69's broader lesson that refresh scheduling elasticity does not abolish maintenance deadlines or coverage obligations.

## Retained state and control state

At least seven relations should remain separate:

1. **payload state** — charge-encoded user data across DDR5 banks;
2. **bank-group coordinate** — the bank index whose corresponding bank in each bank group becomes a REFsb target;
3. **maintenance target set** — the parallel set of target banks for one REFsb transaction;
4. **physical row just refreshed** — the row that actually received restorative work;
5. **refresh-coverage / synchronization state** — the counters and sequence relation used to account for which bank indices have been serviced;
6. **service/admission state** — which banks can accept ordinary access while the target set is under refresh;
7. **transition compensation obligation** — extra refresh work required when a boundary resets incomplete coverage accounting.

Only the first is application payload. The other relations help organize recurring maintenance and availability of that payload.

## Engineering reconstruction

### E — Transaction target-set width is not retained-set scope

REFsb widens one maintenance transaction from Case 105's one-bank LPDDR2 REFpb target to a **parallel one-per-bank-group target set**. But this does not shrink the set of data the DDR5 device is expected to retain.

> **maintenance target-set width ≠ retained-set scope**.

The device still needs refresh coverage over the bank indices through time.

### E — "Same" denotes coordinate correspondence, not physical identity

In this interface, `same bank` is a relation across bank groups. Multiple physical banks participate in one command because they share the selected bank coordinate within their respective groups.

> **same bank index across groups ≠ one physical bank**.

This is an addressing/maintenance-geometry relation, not an assertion that the targeted storage cells are one physical object.

### E — Localized unavailability can coexist with broad device service

During `tRFCsb`, the target bank in each bank group is unavailable while other banks remain accessible. Therefore:

```text
payload remains retained
    !=
bank is currently being refreshed
    !=
bank is currently admitted for ordinary service
```

The availability benefit is a scheduling/service property. It is not a weaker promise to retain data in the target banks.

### E — One command completion does not certify coverage completion

A REFsb command can finish its own `tRFCsb` interval while the synchronization sequence still owes other bank indices maintenance before the global refresh row position advances.

> **one REFsb completion ≠ full same-bank refresh cycle completed**.

And even completing the accounting cycle is not a semantic payload-correctness certificate; it records maintenance progress under the interface contract.

### E — Physical maintenance execution is not the same as credited maintenance progress

The JESD79-5B/product-era early-repeat rule sharpens the previous distinction. A repeated REFsb can physically refresh the same row again while contributing no new global-counter progress.

```text
REFsb executed
    -> restorative work happened

but

early repeated bank
    -> same row refreshed again
    -> omitted bank indices still owed
    -> global refresh frontier does not advance
```

Therefore:

> **maintenance work happened ≠ maintenance frontier advanced**.

This is engineering reconstruction from the command/accounting contract, not JEDEC terminology.

### E — The revision change concerns admissible interface behavior, not proven retention-physics change

The 2020 standard forbids the early repeat; the 2022 5B text defines what happens if it occurs. The evidence does not show that cell leakage or restorative physics changed between those documents.

A bounded reading is that the externally visible **protocol semantics for redundant scheduling** changed or became more permissively defined.

The exact committee motivation remains unproven.

### E — Order flexibility remains bounded by coverage constraints

The later standard permits bank indices in any order and defines redundant repeats, but the global row position still waits for complete bank-index coverage.

Thus:

> **arbitrary order ≠ arbitrary repetition as useful progress**.

A controller can issue real maintenance commands yet fail to reduce the outstanding full-device coverage obligation if it keeps selecting already-covered bank indices.

### E — A transition can safely forget progress if it conservatively redoes enough work

Self Refresh entry/exit and refresh-mode changes show another persistence-horizon choice. The device need not carry an incomplete same-bank coverage set across the transition. Instead, the contract can reset that accounting state and require compensating refresh.

```text
preserve partial maintenance progress
    OR
reset partial progress
    + conservatively redo enough maintenance
```

Therefore:

> **control-state reset ≠ payload loss, but control-state reset can create additional maintenance work needed to preserve the payload guarantee**.

This is a bounded functional reconstruction. It is not a claim that every DDR5 internal state is discarded at those boundaries.

### E — DDR5 REFsb semantics are revision-sensitive

A simulator or controller validator keyed to initial JESD79-5 can legitimately reject an early repeated bank as illegal. A model keyed to JESD79-5B/product-era documents should instead model the redundant refresh and unchanged global-progress position.

Flattening all DDR5 revisions into one timeless REFsb rule risks either false illegality or false permissiveness.

## Contrast with Case 105

Cases 105 and 106 expose two forms of bank-granular refresh without making them command-identical:

```text
Case 105 — LPDDR2 REFpb
    one bank is the maintenance target
    other banks can remain serviceable
    a full bank cycle composes the rolling refresh obligation

Case 106 — DDR5 REFsb
    one corresponding bank in every bank group is targeted in parallel
    non-target banks in each group can remain serviceable
    synchronization/accounting spans all bank indices
    by 5B, redundant repeats can execute without advancing coverage
```

The functional continuity is useful: both separate transaction scope from whole retained-set obligation and exploit bank granularity for service concurrency. It is **not** evidence that LPDDR2 REFpb directly evolved into DDR5 REFsb through one proven implementation lineage.

## Prior-art and standards boundary

The strongest bounded historical claims now are:

- a proposed DDR5 full-spec draft dated 5 December 2017, incorporating Q3'17 ballots, already contains the named REFsb mechanism and target/coverage semantics;
- the July 2020 initial JESD79-5 carries the early-repeat illegality rule into the published standard;
- by JESD79-5B_v1.20 in September 2022, the same corner case has defined redundant-refresh behavior instead;
- later SK hynix and Micron product documents preserve the 5B-style behavior.

These are standards-development/publication/product-document nodes, not invention dates. A complete genealogy would require the underlying ballot/proposal history, JESD79-5A text, revision-by-revision comparison through later JESD79-5 revisions, earlier vendor/research proposals, and controller implementations.

That broader historical engineering work belongs primarily in `computing-archaeology` if pursued comprehensively.

## Coverage relationship with Case 33 and LPDDR controls

This case is intentionally narrower than [`Case 33`](33-micron-ddr5-same-bank-refresh-localization.md), not a second independent claim that DDR5 introduced localized refresh. Case 33 carries Micron's 2019–2023 manufacturer-primary evidence for target idleness, lockout, residual timing, and service interference. Case 106 carries the earlier **2017 proposed-spec floor**, the **2020→2022 repeat-command semantic boundary**, explicit bank-index synchronization, coverage accounting, and transition compensation. The two should be cited together when both chronology and operational geometry matter.

Earlier per-bank refresh is already bounded separately in [`Case 105`](105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md), while [`Case 139`](139-lpddr3-lpddr4-per-bank-refresh-target-authority.md) isolates the LPDDR3→LPDDR4 migration of bank-target selection authority. Chronology across these cases is not treated as direct genealogy.

## Functional analogy and philosophical limit

A functional analogy to rotating maintenance crews working on the same numbered unit in several independent sections can make the target geometry intuitive. The later repeat-command rule adds another limited analogy: redoing maintenance on a unit can be real work while failing to advance a checklist that still contains untouched units.

The analogy stops there. Bank groups are not archival departments, REFsb is not cultural selection, and the synchronization/global refresh counters are not human memory.

The bounded conceptual result is technical:

> apparent continuous availability can arise because recurring retention work is **spatially partitioned and parallelized**, while the obligation to preserve the full payload remains global across time; doing maintenance and accounting that maintenance as new coverage are distinct relations.

## Cross-case result

The DRAM refresh decomposition now includes another independent axis without turning the cases into an invention ladder:

```text
Case 03   leakage creates a refresh deadline
Case 09   refresh-row enumeration can move on-chip
Case 10   refresh scheduling can become autonomous and condition-derived
Case 21   recurring refresh responsibility can hand off between controller and SDRAM
Case 69   refresh issue time can have bounded scheduling elasticity
Case 104  self-refresh cadence and retained coverage can vary independently
Case 105  one transaction can be one-bank-local while coverage remains full-bank over time
Case 106  one transaction can target corresponding banks across groups in parallel;
          command execution, coverage credit, and transition compensation remain distinct
```

This is a functional decomposition, not a proof of direct historical descent.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| proposed DDR5 Rev0.1 is dated 12/5/17 and says it includes Q3'17 ballots | H/P | proposed full-spec revision history |
| REFsb targets a specific bank in each bank group | H/P | proposed full spec §4.10.3; later standard/vendor continuity |
| target banks are inaccessible during `tRFCsb` while other banks remain accessible | H/P | proposed full spec §4.10.3; later manufacturer continuity |
| 2017 proposed text and July 2020 JESD79-5 require every bank index before an early repeat | H/P | proposed/final standard text mirrors |
| the initial JESD79-5 calls an early repeated REFsb illegal | H/P | July 2020 standard text mirror |
| JESD79-5B says an early repeat refreshes the same row without global-counter advance | H/P | JESD79-5B_v1.20 §4.13.3 |
| the exact rule change first appeared in JESD79-5A | X | not established; revision/ballot gap remains |
| entering/exiting Self Refresh can reset incomplete REFsb accounting and require extra refresh | H/P | JESD79-5B §4.13.7; SK hynix product document |
| maintenance execution always implies new coverage progress | X | contradicted by 5B-style redundant-repeat semantics |
| same-bank target geometry is one physical bank total | X | contradicted by the `one in each Bank Group` wording |
| one completed REFsb establishes full-array payload correctness | X | command/accounting scope does not provide that certificate |
| the 2017 draft is identical to final JESD79-5 wording in every respect | X | not established |
| July 2020 publication proves DDR5 Same Bank Refresh invention priority | X | not established |
| LPDDR2 REFpb → DDR5 REFsb is a proven direct genealogy | X | not established; comparison is functional only |

## Related repositories

A current GitHub search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `DDR5 REFsb Same Bank Refresh` found no dedicated case. Complete JEDEC chronology, the exact 5A/ballot change that altered repeat semantics, controller scheduling implementations, performance modeling, and cross-vendor device genealogy should be developed there if pursued broadly. This repository keeps the bounded retention relation among target-set geometry, physical maintenance execution, coverage accounting, transition compensation, and service concurrency.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the anti-anachronism guard: `maintenance target-set width`, `coverage accounting`, `maintenance frontier`, and `transition compensation` are present analytical vocabulary, not terms attributed to JEDEC committee authors or DRAM vendors.

## Sources

1. JEDEC JC-42.3 proposed material, _DDR5 Full Spec Draft Rev0.1_, dated 5 December 2017, especially revision history and §4.10.3 `Same Bank Refresh`, printed p. 176. Public mirror: <https://www.pedestrian.com.cn/_downloads/4928176668e6494cc99abfb887fdf326/DDR5_JESD79-5.pdf>.
2. JEDEC, _DDR5 SDRAM_, JESD79-5, July 2020, §4.13.3 `Same Bank Refresh`. Public mirror: <https://github.com/RAMGuide/TheRamGuide-WIP-/blob/main/DDR5%20Spec%20JESD79-5.pdf>.
3. JEDEC, _DDR5 SDRAM_, JESD79-5B_v1.20, September 2022, especially §§4.13.2, 4.13.3, 4.13.7. Public text mirror: <https://studylib.net/doc/27611087/jesd79-5b-v1>.
4. GlobalSpec standards catalog, JESD79-5 / JESD79-5A / JESD79-5B publication chronology: <https://standards.globalspec.com/std/14328154/jedec-jesd-79-5>.
5. SK hynix, _DDR5 SDRAM 16Gb A-die_, Rev. 1.1, especially §§4.13.3 and 4.13.7. Public product-document mirror: <https://uttc.com.tw/wp-content/uploads/2025/12/Consumer_CP16GD5_H5CG448%EF%BC%866AGBDJXxxx_Rev.1.1_1anm.pdf>.
6. Micron Technology, _DDR5 SDRAM Product Core Data Sheet_, Rev. E 11/2024, JESD79-5C-compliant product core specification, Same Bank Refresh section. Public mirror: <https://www.avnet.com/wcm/connect/dacdfea7-999f-4ee0-b514-6f9e0bf68c6d/ddr5-sdram-core.pdf?MOD=AJPERES>.
7. Micron Technology, `Micron's DDR5 Technology Enablement Program empowers an ecosystem`, manufacturer page, especially its July 2020 standards reference and Same Bank Refresh summary: <https://www.micron.com/about/blog/memory/dram/microns-ddr5-technology-enablement-program-empowers-ecosystem>.
8. Micron Technology, `Redefining performance With DDR5 and 4th Gen Intel Xeon scalable processors`, 2023 product/platform-era manufacturer explanation, especially the Same Bank Refresh availability discussion: <https://www.micron.com/about/blog/company/partners/redefining-performance-with-ddr5-and-4th-gen-intel-xeon-scalable>.
