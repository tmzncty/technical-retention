# Evidence 105C — JEDEC 2009–2010 LPDDR2 Per-Bank Refresh Standards Chronology

**Status:** `bounded deepening complete`

**Canonical case:** [`../cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md`](../cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md)

## Research question

Case 105 already has two kinds of witness for LPDDR2 per-bank refresh:

- a Hynix manufacturer-primary design disclosure published 7 May 2009;
- named SK hynix (2012) and Micron (2014–2015) product documents.

The canonical case deliberately left the **JEDEC introduction / revision chronology** open. This slice asks a narrower question:

> By what public date can `Per-Bank Refresh` be tied to the LPDDR2 JEDEC standard itself, and by what later revision can the detailed `REFpb` control relation be inspected directly?

The answer is bounded in two layers:

1. **2 April 2009:** a contemporaneous JEDEC release announcement for `JESD209-2` explicitly names `Per-Bank Refresh` among LPDDR2 power-management mechanisms;
2. **February 2010:** a mirrored copy of `JESD209-2B` directly exposes the normative `REFpb` / `REFab` command semantics, bank sequencing, controller tracking, service-concurrency rule, refresh-accounting rule, and self-refresh handoff obligation.

This closes the broad claim that the feature was already part of the public LPDDR2 standards surface by April 2009 and that the detailed command relation is directly inspectable by revision 2B. It does **not** close the exact clause-by-clause wording of the initial April-2009 JESD209-2 release because an origin-host or independently archived full initial-release facsimile was not inspected in this slice.

---

## Source custody

### S1 — contemporaneous JEDEC release announcement, republished

Design-Reuse retains a release titled **“JEDEC Announces Publication of LPDDR2 Standard for Low Power Memory Devices”**, dated **2 April 2009**. The body identifies JEDEC as the announcing organization, states that `JESD209-2 LPDDR2 Low Power Memory Device Standard` had been published, and explicitly says LPDDR2 supports power-management mechanisms including **Partial Array Self Refresh and Per-Bank Refresh**.

Source: <https://www.design-reuse.com/news/202516498-jedec-announces-publication-of-lpddr2-standard-for-low-power-memory-devices/>

Evidence class here: **H/P*** — contemporaneous JEDEC announcement text surviving on a third-party publisher, not a currently inspected origin-host JEDEC page.

### S2 — independent contemporaneous reporting

EE Times, **2 April 2009**, independently reported that JEDEC had published `JESD209-2` and likewise named Partial Array Self Refresh and Per-Bank Refresh among LPDDR2 power-management mechanisms.

Source: <https://www.eetimes.com/jedec-releases-new-standard-for-low-power-memory-devices/>

Evidence class: **H/S** — contemporaneous independent reporting.

### S3 — JESD209-2B normative text via mirror

A mirrored copy of **JEDEC Standard No. 209-2B, Low Power Double Data Rate 2 (LPDDR2), February 2010** identifies itself as a revision of **JESD209-2A, October 2009**. Its informative revision annex lists:

- initial release `JESD209-2`;
- update to `JESD209-2A`;
- update to `JESD209-2B`.

The same document's §5.10 directly specifies `REFpb` / `REFab` behavior.

Source: <https://studylib.net/doc/18425613/jedec-standard--low-power-double-data-rate-2>

Evidence class: **H/P*** — standards text with explicit JEDEC document identity, inspected through a third-party mirror rather than an origin-host facsimile.

---

## Historical record

### H/P* + H/S — Per-Bank Refresh is on the public LPDDR2 standards surface by 2 April 2009

The 2 April 2009 release announcement states that JEDEC had published `JESD209-2` and explicitly names **Per-Bank Refresh** as an LPDDR2 power-management mechanism. EE Times independently reports the same publication and feature on the same date.

This changes the public chronology used by Case 105:

```text
2 Apr 2009
    JESD209-2 publicly announced
    Per-Bank Refresh explicitly named at feature level

7 May 2009
    Hynix US20090116326A1 published
    detailed manufacturer-primary per-bank address/control disclosure
```

Therefore the 7 May 2009 Hynix patent publication remains an important **mechanism-level manufacturer disclosure**, but it is no longer the earliest public floor in this case for the bare fact that LPDDR2 exposed a standardized Per-Bank Refresh feature.

This does not turn the JEDEC announcement into an invention-priority claim. The Hynix family has a 2 November 2007 priority date, but patent priority is not silently converted into public disclosure, and neither source establishes who first invented per-bank refresh.

### H/P* — revision chronology is explicit by JESD209-2B

The February-2010 document identifies itself as `JESD209-2B` and as a revision of `JESD209-2A, October 2009`. Annex C labels:

- `C.1 Initial Release JESD209-2`;
- `C.2 Updated Specification to JESD209-2A`;
- the subsequent update to `JESD209-2B`.

This provides a bounded revision chain:

```text
JESD209-2      public release announced 2 Apr 2009
    ->
JESD209-2A     October 2009
    ->
JESD209-2B     February 2010
```

The annex also records changes between revisions, including refresh-related terminology changes elsewhere in the document. For that reason this slice does **not** infer that every word of the 2B refresh section is byte-for-byte identical to the initial April-2009 release.

### H/P* — by JESD209-2B, REFpb is a bank-local command with shared target-sequence state

Section 5.10 states that:

- `Per Bank Refresh` is selected separately from `All Bank Refresh`;
- `REFpb` applies to the bank scheduled by a bank counter in the memory device;
- the bank sequence is a fixed sequential round-robin over banks 0 through 7;
- RESET and every self-refresh exit synchronize the controller and SDRAM bank count to zero;
- the controller is responsible for tracking which bank is being refreshed.

This is not merely a vendor implementation hint. By February 2010 it appears as a JEDEC interface contract.

The retained relation is therefore explicitly split between device and controller:

```text
memory-side bank counter
    +
controller-side knowledge of the same sequence
    ->
shared meaning of the next REFpb command
```

The standard does not say this coordination state is nonvolatile or survives power removal.

### H/P* — bank-local maintenance does not imply device-wide service withdrawal

JESD209-2B states that the target bank is inaccessible for `tRFCpb`, while other banks remain accessible and may remain active or receive reads/writes subject to timing rules.

Thus the standard directly supports:

```text
one bank under maintenance
    !=
entire device unavailable
```

and:

```text
other-bank service continues
    !=
target-bank maintenance already complete
```

### H/P* — one REFpb does not discharge the whole refresh obligation

The refresh-requirements section says that LPDDR2 devices require a minimum number of refresh commands in a rolling refresh window. For devices supporting Per-Bank Refresh, **one REFab may be replaced by a full cycle of eight REFpb commands**.

This is the strongest standards-level support for Case 105's central boundary:

```text
one REFpb transaction complete
    !=
one full eight-bank REFpb cycle complete
    !=
rolling refresh-window obligation satisfied
```

The standard therefore distinguishes **transaction scope** from **coverage/accounting scope**.

### H/P* — self-refresh exit can create an explicit follow-up refresh obligation

JESD209-2B states that self-refresh exit can miss an internally timed refresh event and therefore requires at least one refresh command — glossed as **8 per-bank or 1 all-bank** — before entering a subsequent self-refresh period.

The standards-level sequence is:

```text
self-refresh exit
    -> possible missed internally timed refresh event
    -> explicit follow-up refresh requirement
    -> later self-refresh entry
```

This independently corroborates the later SK hynix product wording already used by Case 105.

It is evidence for a **maintenance handoff obligation**, not evidence that exact refresh progress is durably checkpointed across power loss.

### H/P* — Per-Bank Refresh is capability-scoped, not universal across every LPDDR2 device

The 2B text qualifies the operation: Per-Bank Refresh is allowed only for the relevant eight-bank devices, and the refresh-accounting clause is explicitly conditional on devices **supporting** Per-Bank Refresh.

Therefore:

```text
feature present in LPDDR2 standard
    !=
feature mandatory on every possible LPDDR2 device configuration
```

This guardrail matters when moving from a standards document to named products.

---

## Engineering reconstruction

### E — the chronology now separates feature standardization, disclosed circuitry, and product adoption

Case 105 can now carry three different historical layers without collapsing them:

```text
standard feature surface
    2 Apr 2009 JESD209-2 announcement

manufacturer design disclosure
    7 May 2009 Hynix patent publication

named product contracts
    Jun 2012 SK hynix
    Jul 2014 Micron
```

These dates answer different questions. Earlier standard visibility does not prove a specific circuit; a patent does not prove product adoption; a later product document does not establish first invention.

### E — standardization preserves the controller/device coordination relation while leaving implementation open

The 2B contract requires both a device-side bank schedule and controller-side tracking. It specifies the observable coordination semantics, not the transistor-level implementation of the counter, how a controller stores its tracking state, or what vendor microarchitecture realizes the command.

Thus:

```text
standardized control relation
    !=
standardized internal implementation
```

### E — maintenance completion remains typed by scope

The standard makes at least three completion predicates visible:

1. the target-bank `REFpb` operation has completed;
2. all eight bank positions in one REFpb cycle have been covered;
3. the rolling-window refresh requirement has been satisfied.

Using a single phrase such as `refresh complete` without naming which predicate is meant loses important retention information.

### E — resetting coordination state is not payload rollback

RESET and self-refresh exit can re-synchronize the bank counter to zero. This reinitializes maintenance-control geometry while leaving the question of payload retention governed by the surrounding DRAM state/mode rules.

The bounded lesson is:

```text
maintenance enumerator reinitialized
    !=
application data intentionally rolled back
```

No claim is made here about payload survival across an actual power-removal event.

---

## Functional comparison, not genealogy

- **Case 03** supplies the basic DRAM relation: leakage creates a recurring restoration deadline.
- **Case 104 / PASR** can shrink the set whose retention is promised in self refresh.
- **Case 105 / REFpb** shrinks the target of one maintenance transaction while preserving bank-complete refresh accounting over time.
- **Case 106 / DDR5 REFsb** later exposes a different parallel target set spanning corresponding banks across bank groups.

These are functional comparisons. This slice does not claim a direct LPDDR2 REFpb -> DDR5 REFsb genealogy.

---

## Philosophical limit

The evidence supports a narrow systems claim: continuous availability can be produced by maintenance whose **execution is spatially local** while whose **obligation is temporally global over a larger retained set**.

It does not support claims about human memory, cultural forgetting, or a universal philosophy of persistence.

---

## Explicit non-claims

This slice does **not** claim that:

1. JEDEC invented per-bank refresh;
2. 2 April 2009 is the invention date;
3. Hynix's 2 November 2007 priority date was a public disclosure date;
4. the Hynix patent caused or directly entered JESD209-2;
5. the Hynix patent embodiment is the implementation used by the SK hynix product;
6. the initial April-2009 JESD209-2 wording was byte-for-byte identical to JESD209-2B;
7. every 2B refresh clause existed unchanged in the initial release;
8. the third-party 2B mirror is equivalent in provenance to a JEDEC-hosted archival facsimile;
9. every LPDDR2 device supports Per-Bank Refresh;
10. one REFpb refreshes the full device;
11. eight REFpb are identical to one REFab in latency, energy, interference, or internal execution;
12. other-bank accessibility means the target bank is already maintained;
13. the controller/device bank counter is nonvolatile;
14. bank-counter synchronization is an application-data checkpoint;
15. self-refresh exit preserves exact internal refresh progress;
16. follow-up refresh after self-refresh exit proves a power-failure recovery protocol;
17. standardization establishes named-product shipment;
18. later product conformance proves exact silicon implementation;
19. LPDDR2 REFpb and DDR5 REFsb are the same mechanism;
20. any of these sources establish secure erasure, sanitization, or forensic forgetting.

---

## Claim ledger

| Claim | Label | Evidence |
| --- | --- | --- |
| JEDEC publicly announced JESD209-2 on 2 Apr 2009 | H/P* + H/S | republished JEDEC announcement + contemporaneous EE Times |
| the 2 Apr 2009 public LPDDR2 release material explicitly names Per-Bank Refresh | H/P* + H/S | same source pair |
| JESD209-2B is dated Feb 2010 and identifies JESD209-2A as Oct 2009 | H/P* | JESD209-2B front matter via mirror |
| 2B Annex C identifies an initial JESD209-2 release followed by 2A and 2B updates | H/P* | JESD209-2B Annex C |
| by 2B, REFpb uses a fixed round-robin bank schedule | H/P* | JESD209-2B §5.10 |
| by 2B, controller and SDRAM bank count are synchronized on RESET / self-refresh exit | H/P* | JESD209-2B §5.10 |
| by 2B, the controller is responsible for tracking the REFpb target bank | H/P* | JESD209-2B §5.10 |
| target bank unavailable while other banks remain usable during REFpb | H/P* | JESD209-2B §5.10 |
| one REFab may be replaced by a full cycle of eight REFpb on supporting devices | H/P* | JESD209-2B §5.10.1 |
| self-refresh exit requires a later refresh before a subsequent self-refresh entry | H/P* | JESD209-2B §5.11 |
| April-2009 standard visibility predates the May-2009 Hynix patent publication as a public feature-level floor | H/E | dated source comparison |
| exact initial-release clause wording remains unverified | U | initial JESD209-2 full facsimile not inspected |

---

## Remaining evidence debt

1. Obtain an origin-host or independently archived full facsimile of the **initial April-2009 JESD209-2** and inspect its refresh section directly.
2. Obtain / inspect full `JESD209-2A` and perform a clause-level `2 -> 2A -> 2B` refresh diff rather than infer continuity from revision ancestry.
3. Recover JEDEC ballot / committee proposal chronology, if publicly available, for the introduction and wording evolution of Per-Bank Refresh.
4. Determine whether earlier JEDEC mobile-memory standards or public proposals exposed an equivalent per-bank refresh contract under different terminology.
5. Keep named-controller scheduling traces, silicon implementation, fault injection, and power/reset persistence tests separate from the standards history.
6. Route the broader LPDDR standards/product genealogy to `tmzncty/computing-archaeology` if that repository later develops a dedicated mobile-DRAM history packet.

---

## Bounded conclusion

Case 105 no longer needs to leave the **broad JEDEC appearance** of LPDDR2 Per-Bank Refresh wholly open. A contemporaneous 2 April 2009 JEDEC release announcement explicitly names the feature in published `JESD209-2`, and February-2010 `JESD209-2B` directly exposes the detailed command-level relation that later appears in SK hynix and Micron product documents.

The remaining standards debt is narrower and more exacting: the full initial-release clause text, the 2A intermediate wording, committee/proposal history, and exact revision-by-revision changes.
