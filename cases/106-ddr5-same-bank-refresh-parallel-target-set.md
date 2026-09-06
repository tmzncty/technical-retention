# DDR5 Same-Bank REFRESH: Parallel Bank-Group Targets, Coverage Accounting, and Service Concurrency

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
