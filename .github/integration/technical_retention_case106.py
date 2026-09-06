from pathlib import Path

case_path = Path('cases/106-ddr5-same-bank-refresh-parallel-target-set.md')
evidence_path = Path('evidence/106-ddr5-2017-2023-same-bank-refresh-grounding.md')
if case_path.exists() or evidence_path.exists():
    raise SystemExit('Case/Evidence 106 already exists; refusing duplicate integration')

case = r'''# DDR5 Same-Bank REFRESH: Parallel Bank-Group Targets, Coverage Accounting, and Service Concurrency

## Status

**`grounded`** — bounded to a December 2017 proposed DDR5 full-spec draft carrying Q3'17 ballots plus later Micron manufacturer explanations of DDR5 Same Bank Refresh. This case establishes the retention relation and a dated draft floor; it does **not** claim final-revision wording, invention priority, or a complete JEDEC genealogy.

Grounding record: [`../evidence/106-ddr5-2017-2023-same-bank-refresh-grounding.md`](../evidence/106-ddr5-2017-2023-same-bank-refresh-grounding.md).

## Scope

Case 105 established one LPDDR2 regime in which a `REFpb` transaction targets one bank, leaves other banks serviceable, and contributes to a rolling full-bank refresh obligation. The next bounded question is deliberately narrower than a DDR5 history:

> What changes when one refresh command targets the **same bank coordinate across every bank group in parallel**, while the device still owes refresh coverage across all bank coordinates over time?

The primary historical anchor is the proposed DDR5 Full Spec Rev0.1 dated 5 December 2017, which says it includes ballots through Q3'17 and contains section 4.10.3, `Same Bank Refresh`. Later Micron manufacturer material corroborates that DDR5 shipped/was presented with Same Bank Refresh as a bank-granular availability feature.

This case does not establish who originated Same Bank Refresh, the exact wording of JESD79-5 final/revisions, how every DDR5 controller schedules REFsb, or whether every vendor/device implements all optional details identically.

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

### H/P — Later Micron material preserves the same service-concurrency explanation

A Micron DDR5 Technology Enablement Program page states that JEDEC announced the DDR5 standard in **July 2020** and describes Same Bank Refresh as an improved refresh scheme that targets one bank per bank group.

A later Micron data-center article tied to the January 2023 4th Gen Intel Xeon platform launch lists Same Bank Refresh among DDR5 RAS/availability capabilities and explains the intended service benefit as retaining access to non-target banks while granular refresh proceeds.

These later sources are continuity/product-era witnesses. They do not turn the 2017 proposed draft into final-standard text or prove a Micron origin claim.

## Retained state and control state

At least five relations should remain separate:

1. **payload state** — charge-encoded user data across DDR5 banks;
2. **bank-group coordinate** — the bank index whose corresponding bank in each bank group becomes a REFsb target;
3. **maintenance target set** — the parallel set of target banks for one REFsb transaction;
4. **refresh-coverage / synchronization state** — the counters and sequence relation used to account for which bank indices have been serviced;
5. **service/admission state** — which banks can accept ordinary access while the target set is under refresh.

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

A REFsb command can finish its own `tRFCsb` interval while the synchronization sequence still owes other bank indices maintenance before the same index can legally repeat.

> **one REFsb completion ≠ full same-bank refresh cycle completed**.

And even completing the accounting cycle is not a semantic payload-correctness certificate; it records maintenance progress under the interface contract.

### E — Order flexibility remains bounded by coverage constraints

The draft permits bank indices to be serviced in any order, but forbids repeating one before every bank index has received one REFsb in the sequence. Thus scheduling flexibility is real but constrained:

> **arbitrary order ≠ arbitrary repetition/postponement**.

This extends Case 69's broader lesson that refresh scheduling elasticity does not abolish maintenance deadlines or coverage obligations.

## Contrast with Case 105

Cases 105 and 106 expose two forms of bank-granular refresh without making them command-identical:

```text
Case 105 — LPDDR2 REFpb
    one bank is the maintenance target
    other banks can remain serviceable
    a full bank cycle composes the rolling refresh obligation

Case 106 — proposed DDR5 REFsb
    one corresponding bank in every bank group is targeted in parallel
    non-target banks in each group can remain serviceable
    synchronization/accounting spans all bank indices before repeat
```

The functional continuity is useful: both separate transaction scope from whole retained-set obligation and exploit bank granularity for service concurrency. It is **not** evidence that LPDDR2 REFpb directly evolved into DDR5 REFsb through one proven implementation lineage.

## Prior-art and standards boundary

The strongest bounded historical claim here is:

> a proposed DDR5 full-spec draft dated 5 December 2017, incorporating Q3'17 ballots, already contains the named REFsb mechanism and the target/coverage semantics analyzed above.

That is a standards-development floor, not an origin date. The later July 2020 final-standard announcement is likewise a publication/adoption node, not proof of invention.

A complete genealogy would require the underlying ballot/proposal history before this compiled draft, revision-by-revision comparison through published JESD79-5 versions, earlier vendor or research proposals, cross-vendor device documentation, and memory-controller implementations. That broader historical engineering work belongs primarily in `computing-archaeology` if pursued comprehensively.

## Functional analogy and philosophical limit

A functional analogy to rotating maintenance crews working on the same numbered unit in several independent sections can make the target geometry intuitive. The analogy stops there. Bank groups are not archival departments, REFsb is not cultural selection, and the synchronization counter is not human memory.

The bounded conceptual result is technical:

> apparent continuous availability can arise because recurring retention work is **spatially partitioned and parallelized**, while the obligation to preserve the full payload remains global across time.

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
Case 106  one transaction can target corresponding banks across groups in parallel while coverage accounting spans all bank indices
```

This is a functional decomposition, not a proof of direct historical descent.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| proposed DDR5 Rev0.1 is dated 12/5/17 and says it includes Q3'17 ballots | H/P | proposed full-spec revision history |
| REFsb targets a specific bank in each bank group | H/P | proposed full spec §4.10.3, printed p. 176 |
| target banks are inaccessible during `tRFCsb` while other banks remain accessible | H/P | proposed full spec §4.10.3, printed p. 176 |
| every bank index must receive one REFsb before the same index may repeat in the synchronization sequence | H/P | proposed full spec §4.10.3, printed p. 176 |
| same-bank target geometry is one physical bank total | X | contradicted by the draft's `one in each Bank Group` wording |
| one completed REFsb establishes full-array payload correctness | X | command/accounting scope does not provide that certificate |
| the 2017 draft is identical to final JESD79-5 wording | X | not established |
| July 2020 publication proves DDR5 Same Bank Refresh invention priority | X | not established |
| LPDDR2 REFpb → DDR5 REFsb is a proven direct genealogy | X | not established; comparison is functional only |

## Related repositories

A current GitHub search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated DDR5 REFsb / Same Bank Refresh case. Complete JEDEC chronology, pre-2017 ballot genealogy, controller scheduling implementations, performance modeling, and cross-vendor semantics should be developed there if pursued broadly. This repository keeps the bounded retention relation among target-set geometry, coverage accounting, and service concurrency.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the anti-anachronism guard: `maintenance target-set width`, `coverage accounting`, and `retained set` are present analytical vocabulary, not terms attributed to the 2017 committee authors.

## Sources

1. JEDEC JC-42.3 proposed material, _DDR5 Full Spec Draft Rev0.1_, dated 5 December 2017, especially revision history and §4.10.3 `Same Bank Refresh`, printed p. 176. Public mirror: <https://www.pedestrian.com.cn/_downloads/4928176668e6494cc99abfb887fdf326/DDR5_JESD79-5.pdf>.
2. Micron Technology, `Micron's DDR5 Technology Enablement Program empowers an ecosystem`, manufacturer page, especially its July 2020 standards reference and Same Bank Refresh summary: <https://www.micron.com/about/blog/memory/dram/microns-ddr5-technology-enablement-program-empowers-ecosystem>.
3. Micron Technology, `Redefining performance With DDR5 and 4th Gen Intel Xeon scalable processors`, 2023 product/platform-era manufacturer explanation, especially the Same Bank Refresh availability discussion: <https://www.micron.com/about/blog/company/partners/redefining-performance-with-ddr5-and-4th-gen-intel-xeon-scalable>.
'''
case_path.write_text(case, encoding='utf-8')

evidence = r'''# DDR5 2017–2023 Same Bank Refresh grounding record

This record grounds [`../cases/106-ddr5-same-bank-refresh-parallel-target-set.md`](../cases/106-ddr5-same-bank-refresh-parallel-target-set.md).

The bounded question is whether DDR5 Same Bank Refresh can localize one maintenance transaction to corresponding bank positions across multiple bank groups while retaining a broader coverage obligation, and how that differs from the one-bank LPDDR2 REFpb regime in Case 105.

## Source A — proposed DDR5 Full Spec Rev0.1, 5 December 2017

Publicly mirrored PDF:
<https://www.pedestrian.com.cn/_downloads/4928176668e6494cc99abfb887fdf326/DDR5_JESD79-5.pdf>

The PDF text was inspected directly. The page image for printed p. 176 / PDF page 184 containing §4.10.3 was also visually inspected. The remote screenshot cache did not return the revision-history page image during this run, so the 12/5/17 revision line is grounded in direct PDF text extraction rather than a claimed visual facsimile check.

### A1. Document status and date boundary

The front matter labels the file `DDR5 Full Spec Draft Rev0.1`, identifies committee JC42.3, and marks it as committee letter-ballot/proposed material. The revision history gives:

- `Rev0.1`;
- author `C.Cox`;
- date `12/5/17`;
- description `Initial Format Rev0.1 - Includes all ballots through Q3'17`.

This means the repository can establish a **December 2017 proposed-draft floor**. It must not describe this public mirror as the final published JESD79-5 standard.

### A2. REFsb target geometry — printed p. 176, §4.10.3

The section says Same Bank Refresh (`REFsb`) applies refresh to a specific bank **in each bank group**, in contrast to All Bank Refresh (`REFab`) over all banks in every bank group. In this draft REFsb is valid only in FGR mode.

The visual page inspection confirms the same wording and the section title `4.10.3 Same Bank Refresh`.

This grounds:

- `same bank` ≠ one unique physical bank in the whole device;
- one REFsb target set = corresponding target bank in multiple bank groups;
- REFsb ≠ REFab.

### A3. Synchronization / coverage accounting — printed p. 176

The draft says each REFsb increments an internal bank counter. A REFsb can be issued in any bank order, but every bank must receive one before the same bank can receive a subsequent REFsb; repeating early is illegal.

The first command is described as the `Synchronization` REFsb. The internal count resets after every bank has received one REFsb, RESET, entering/exiting self refresh, or REFab. The global refresh counter increments on REFab or after all banks have received one REFsb and the synchronization count resets. A REFab in the middle of a same-bank sequence does not increment the global counter for that incomplete sequence.

The exact implementation of these counters is not exposed. The primary evidence establishes interface/accounting semantics, not a transistor-level controller design.

### A4. Target-bank unavailability and non-target service — printed p. 176

The draft explicitly says the target banks — `one in each Bank Group` — are inaccessible during `tRFCsb`, while other banks in each bank group are accessible/addressable. On completion, the refreshed banks are idle.

This directly supports:

- target-set maintenance ≠ whole-device blackout;
- non-target availability ≠ target-bank availability;
- command completion for one target set ≠ coverage completion across all bank indices.

### A5. Scheduling flexibility is bounded

The same section allows bank indices in any order but forbids early repetition, and states that a single REFab can be replaced by 2 or 4 REFsb commands **for scheduling in terms of postponing and pulling in refresh commands**.

That wording is kept narrow. It is not rewritten here as a claim that 2/4 REFsb are universally semantically identical to one REFab for every retention, accounting, timing, or service property.

## Source B — Micron DDR5 ecosystem page, final-standard/product-era continuity

Micron manufacturer page:
<https://www.micron.com/about/blog/memory/dram/microns-ddr5-technology-enablement-program-empowers-ecosystem>

The page states that JEDEC announced the DDR5 standard in **July 2020** and lists Same Bank Refresh among DDR5 improvements, describing it as targeting one bank per bank group.

Use here: later manufacturer continuity and a publication-era anchor.

Do not use it for: invention priority, exact final normative wording, or proof that every DDR5 part exposes identical optional behavior.

## Source C — Micron 2023 platform-era explanation

Micron manufacturer page:
<https://www.micron.com/about/blog/company/partners/redefining-performance-with-ddr5-and-4th-gen-intel-xeon-scalable>

The article is situated around Intel's 10 January 2023 launch of 4th Gen Xeon Scalable systems. It lists Same Bank Refresh among DDR5 RAS/availability features and explains its practical purpose as granular refresh that keeps non-target banks available for access.

This source is useful as a product/platform-era service interpretation. It is not stronger than Source A for exact 2017 command/accounting semantics.

## Cross-case evidence boundary

### Case 105 — LPDDR2 REFpb

Case 105's Micron LPDDR2 documents ground a one-bank REFpb target, a fixed round-robin sequence, non-target-bank service, and full-cycle rolling refresh accounting.

### Case 106 — proposed DDR5 REFsb

Source A instead grounds a parallel target set: one corresponding bank in each bank group, with coverage/synchronization across all bank indices.

Therefore the defensible comparison is:

> both localize recurring refresh work relative to whole-device maintenance, but their transaction target geometry and accounting semantics are not command-identical.

Nothing in the present source set proves a direct LPDDR2 REFpb → DDR5 REFsb implementation genealogy.

## Evidence ledger

| Claim | Label | Location | Strength |
| --- | --- | --- | --- |
| Rev0.1 dated 12/5/17 includes ballots through Q3'17 | H/P | Source A revision history | strong proposed-standards primary text |
| REFsb targets one specific bank in each bank group | H/P | Source A §4.10.3, printed p. 176 | strong proposed-standards primary text + page-image inspection |
| REFsb is restricted to FGR mode in this draft | H/P | Source A §4.10.3, printed p. 176 | strong proposed-standards primary text |
| target banks are unavailable during `tRFCsb`; others remain accessible | H/P | Source A §4.10.3, printed p. 176 | strong proposed-standards primary text + page-image inspection |
| every bank index must be serviced before one repeats | H/P | Source A §4.10.3, printed p. 176 | strong proposed-standards primary text |
| synchronization/global counter state records maintenance coverage rather than payload | E | reconstruction from Source A | strong mechanism inference |
| DDR5 final-standard era includes Same Bank Refresh | H/P | Source B; Source C continuity | manufacturer-primary continuity |
| December 2017 draft = final JESD79-5 wording | X | not established | rejected |
| 2017 or 2020 = invention priority | X | not established | rejected |
| LPDDR2 REFpb and DDR5 REFsb share a proven direct genealogy | X | not established | rejected |

## Historical cautions

- Source A is a publicly mirrored **proposed** DDR5 committee draft, not an official-hosted final standard copy.
- The 2017 date establishes a floor for this compiled proposal text, not the first conception or implementation of Same Bank Refresh.
- The July 2020 announcement establishes a publication/adoption node, not an invention date.
- Micron's later summaries are manufacturer explanations, not independent verification of the complete standards history.
- `same bank` must be interpreted with the bank-group geometry; collapsing it to one physical bank creates a technical error.
- Refresh-accounting progress is not a semantic application-data integrity certificate.
- Service concurrency does not imply that the target set is simultaneously available.

## Related-repository check

A current GitHub search of `tmzncty/computing-archaeology` for `DDR5 same-bank refresh`, `REFsb`, and the adjacent terminology did not expose a dedicated case. Full standards genealogy, underlying ballots/proposals, controller scheduling implementation, performance/energy modeling, and cross-vendor comparison belong there if developed comprehensively.
'''
evidence_path.write_text(evidence, encoding='utf-8')

# Cross-link the adjacent LPDDR2 REFpb case without rewriting its historical claims.
case105_path = Path('cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md')
case105 = case105_path.read_text(encoding='utf-8')
anchor105 = "A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated LPDDR2 REFpb / per-bank-refresh case. Full JEDEC chronology, earlier per-bank-refresh prior art, controller scheduling history, and cross-vendor implementation should be developed there if pursued broadly. This repository keeps the bounded retention relation between maintenance-event scope, full-bank coverage, and service concurrency."
replacement105 = "A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated LPDDR2 REFpb or DDR5 REFsb case. [`Case 106`](106-ddr5-same-bank-refresh-parallel-target-set.md) now handles the bounded later DDR5 same-bank target-set / coverage-accounting relation while preserving Case 105's one-bank LPDDR2 boundary. Full JEDEC genealogy beyond these bounded source floors, earlier prior art, controller scheduling history, and cross-vendor implementation should be developed there if pursued broadly."
if case105.count(anchor105) != 1:
    raise SystemExit('Case105 related-repo anchor mismatch')
case105_path.write_text(case105.replace(anchor105, replacement105, 1), encoding='utf-8')

# Update Phase 2 roadmap and insert the bounded DDR5 item after Case 105.
roadmap_path = Path('ROADMAP.md')
roadmap = roadmap_path.read_text(encoding='utf-8')
if '106-ddr5-same-bank-refresh-parallel-target-set.md' in roadmap:
    raise SystemExit('ROADMAP already references Case106')
lines = roadmap.splitlines()
idxs = [i for i, line in enumerate(lines) if '105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md' in line]
if len(idxs) != 1:
    raise SystemExit(f'ROADMAP Case105 item count mismatch: {len(idxs)}')
i = idxs[0]
old = lines[i]
needle = 'complete JEDEC genealogy, earlier vendor prior art, cross-vendor semantics, controller implementation, later per-bank/same-bank refresh evolution, and fault injection remain open.'
if needle not in old:
    raise SystemExit('ROADMAP Case105 open-work phrase mismatch')
lines[i] = old.replace(needle, 'complete JEDEC genealogy, earlier vendor prior art, cross-vendor semantics, controller implementation, later per-bank/same-bank refresh evolution beyond bounded DDR5 REFsb Case 106, and fault injection remain open.')
new_item = "- [x] DDR5 Same Bank REFRESH parallel target-set / service-concurrency boundary — [`cases/106-ddr5-same-bank-refresh-parallel-target-set.md`](cases/106-ddr5-same-bank-refresh-parallel-target-set.md), grounded by [`evidence/106-ddr5-2017-2023-same-bank-refresh-grounding.md`](evidence/106-ddr5-2017-2023-same-bank-refresh-grounding.md): a 5 December 2017 proposed DDR5 full-spec draft already defines `REFsb` as refreshing one corresponding bank in each bank group, makes those target banks unavailable while leaving other banks accessible, and uses bank-index synchronization/accounting that requires every index to be serviced before one repeats. Later Micron manufacturer material supplies 2020-standard-era and 2023-platform continuity. This closes only the bounded `parallel target-set vs full retained-set obligation` relation and the functional Case 105 REFpb/Case 106 REFsb comparison; final revision-by-revision JESD79-5 genealogy, pre-2017 proposal history, controller implementation, cross-vendor semantics, performance/energy validation, and fault injection remain open."
lines.insert(i + 1, new_item)
roadmap_path.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')

# Add Case106 to the maturity table and append findings 1636–1650.
index_path = Path('CASE_INDEX.md')
index = index_path.read_text(encoding='utf-8')
if 'cases/106-ddr5-same-bank-refresh-parallel-target-set.md' in index or '\n1636.' in index:
    raise SystemExit('CASE_INDEX already contains Case106/findings')
lines = index.splitlines()
insert_at = None
for j, line in enumerate(lines):
    if line.startswith('| [') and 'cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md' in line:
        insert_at = j + 1
        break
if insert_at is None:
    raise SystemExit('CASE_INDEX Case105 table row not found')
row = '| [DDR5 Same-Bank REFRESH: Parallel Bank-Group Targets, Coverage Accounting, and Service Concurrency](cases/106-ddr5-same-bank-refresh-parallel-target-set.md) | **grounded** | volatile DDR5 payload + one-per-bank-group REFsb target set + bank-index synchronization/coverage accounting + non-target service concurrency | separate `same bank` coordinate from one physical bank; target-set width from retained-set scope; one REFsb completion from full synchronization cycle; functional comparison with LPDDR2 REFpb without genealogy | [2017–2023 DDR5 Same Bank Refresh grounding](evidence/106-ddr5-2017-2023-same-bank-refresh-grounding.md); final JESD79-5 revision genealogy, pre-2017 proposals, controllers, cross-vendor semantics, performance/fault validation remain separate work |'
lines.insert(insert_at, row)
index = '\n'.join(lines).rstrip() + '\n'

findings = r'''

## Case 106 — DDR5 Same Bank REFRESH findings

1636. **same-bank REFRESH ≠ one physical bank total** — the 2017 proposed DDR5 draft defines REFsb as targeting one specific bank in **each bank group**, so one command operates on a parallel set of physical banks.
1637. **same bank index across groups ≠ same physical bank** — `same` denotes corresponding bank coordinates inside distinct bank groups; coordinate identity must not be collapsed into embodiment identity.
1638. **maintenance target-set width ≠ retained-set scope** — targeting several corresponding banks in parallel changes one transaction's geometry without shrinking the device-wide payload that recurring refresh must preserve.
1639. **DDR5 REFsb ≠ LPDDR2 REFpb** — Case 105 grounds a one-bank transaction, whereas Case 106 grounds one target bank per bank group; shared bank-granular purpose does not make the commands semantically identical.
1640. **target-bank inaccessibility ≠ whole-device service blackout** — the draft explicitly keeps non-target banks in each bank group accessible/addressable during `tRFCsb`.
1641. **non-target-bank availability ≠ target-bank availability or maintenance completion** — useful service elsewhere can overlap refresh while saying nothing about whether the current target set has finished.
1642. **one completed REFsb ≠ full same-bank refresh synchronization cycle** — `tRFCsb` can finish for one target coordinate while other bank indices still owe service before the sequence is complete.
1643. **bank-order flexibility ≠ duplicate-target freedom** — the 2017 draft permits any bank order but makes it illegal to repeat one bank index before every bank has received one REFsb in the sequence.
1644. **synchronization / refresh-counter state ≠ user payload** — the retained bookkeeping qualifies maintenance coverage/progress rather than encoding application data.
1645. **global refresh-counter advance ≠ payload correctness certificate** — advancing after REFab or a completed REFsb synchronization cycle records maintenance accounting, not semantic integrity of every stored word.
1646. **FGR-mode eligibility ≠ universal stronger retention guarantee** — REFsb is allowed only in FGR mode in the bounded draft, but that interface condition does not by itself establish application durability, correctness, or superiority under every failure model.
1647. **2/4 REFsb scheduling substitution ≠ universal semantic identity with one REFab** — the draft scopes this substitution to postponing/pulling-in refresh scheduling; it must not be generalized across every timing, accounting, or service property.
1648. **December 2017 proposed draft ≠ final JESD79-5 normative wording** — the source establishes a dated standards-development floor and directly inspectable mechanism, while later final revisions still require separate archaeology.
1649. **July 2020 final-standard announcement ≠ invention priority** — publication/adoption timing does not identify the first proposal, implementation, or inventor of Same Bank Refresh.
1650. **Cases 105/106 form a functional comparison, not a direct genealogy** — one-bank LPDDR2 REFpb and one-per-bank-group DDR5 REFsb both expose maintenance granularity/service concurrency, but the present evidence does not prove linear design descent or identical implementation.
'''
index_path.write_text(index.rstrip() + findings + '\n', encoding='utf-8')
