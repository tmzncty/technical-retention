# Evidence 105B — Hynix 2009–2012 Per-Bank Refresh Prior Art and Product Witness

**Status:** `bounded deepening complete`

**Canonical case:** [`../cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md`](../cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md)

## Research question

Case 105 was originally grounded on Micron LPDDR2 product documentation from 2014–2015. That evidence established a useful retention boundary:

```text
one refresh transaction can be bank-local
    while
refresh coverage remains an obligation across the whole bank set
```

The canonical case deliberately left two nearby questions open:

1. can the same control boundary be grounded in an **earlier cross-vendor product contract** rather than inferred from Micron alone?;
2. can an earlier manufacturer-primary design record show that **per-bank refresh address/control machinery** was already a public engineering problem before that product witness, without turning patent chronology into invention priority or a direct implementation genealogy?

This slice answers both questions in bounded form with a Hynix/SK hynix source pair:

- Hynix Semiconductor, US20090116326A1, _Semiconductor memory device capable of performing per-bank refresh_, published 7 May 2009, priority 2 November 2007;
- SK hynix, _16Gb LPDDR2-S4B (x32, 2CS) H9TCNNNBLDMMPR_, Rev. 1.1, June 2012.

The 2012 product specification survives through a third-party PDF mirror rather than a currently located SK hynix origin URL. Its document body, revision history, part number, and manufacturer branding are explicit; it is therefore treated as a **manufacturer-authored product specification surviving via a mirror**, not as an origin-hosted archival record.

The patent is a manufacturer-primary design disclosure. It is not treated as proof that the later LPDDR2 product used the patented circuit.

---

## Source handling and chronology

### 1. Hynix patent publication — 7 May 2009

Google Patents identifies:

- publication: `US20090116326A1`;
- title: _Semiconductor memory device capable of performing per-bank refresh_;
- original assignee: Hynix Semiconductor Inc.;
- inventor: Sang Kwon Lee;
- priority date: 2 November 2007;
- US filing: 27 June 2008;
- publication: 7 May 2009;
- later grant: US7911867B2, 22 March 2011.

For public chronology, this evidence uses **7 May 2009** as the publication floor. The 2007 priority date is not silently converted into a public-disclosure date.

### 2. SK hynix H9TCNNNBLDMMPR product specification — June 2012

The inspected product document identifies itself as:

- `MCP Specification`;
- `16Gb LPDDR2-S4B (x32, 2CS)`;
- `H9TCNNNBLDMMPR`;
- `Rev 1.1 / Jun. 2012`.

Its revision-history page records:

- Rev. 0.1 — `Initial Draft`, December 2011, preliminary;
- later revisions culminating in Rev. 1.1, June 2012.

This slice uses **June 2012** as the conservative dated product-document witness. It does not use the December 2011 internal draft date as a demonstrated public-release date.

---

## Historical record — 2009 design disclosure

### H/P — Hynix publicly treated per-bank refresh as a distinct address/control problem by May 2009

US20090116326A1 says the conventional row-address counter it describes can support ordinary auto-bank refresh and self refresh but makes per-bank refresh difficult because it lacks a bank-address counter and mode-sensitive count control.

The patent's stated design objective is to support:

- per-bank refresh;
- all-bank refresh; and
- self refresh

through address-counting/control circuitry that reacts differently to those refresh modes.

The description explicitly says that during a per-bank refresh:

- only one bank is refreshed;
- ordinary read or write operations may proceed in other banks; and
- the bank address should be internally counted sequentially in round-robin order.

This is a useful prior-art guardrail for Case 105. It shows that the functional relation

```text
bank-local refresh work
    + service in other banks
    + internal bank-sequence state
```

was already present in a Hynix public design disclosure by 2009.

It does **not** establish that Hynix invented the relation, that the patented embodiment shipped, or that it is the exact implementation behind the 2012 LPDDR2 part.

### H/P — the patent separates bank-address state from row-address state

The disclosed counting unit includes bank-address and row-address counting behavior. In the described embodiment:

- a per-bank refresh command advances/uses bank-address state together with row-address state;
- all-bank or self-refresh command paths use different control conditions;
- reset/control signals can reinitialize parts of that counting relation, including in response to power-up or all-bank/self-refresh paths.

This matters to the retention analysis because `refresh counter` is not necessarily one undifferentiated number. A maintenance enumerator can contain more than one coordinate and can have mode-dependent reset rules.

That is a mechanism-level observation about this disclosed circuit, not a claim about the internal implementation of every LPDDR2 DRAM.

---

## Historical record — 2012 named product contract

### H/P — SK hynix exposes both all-bank and per-bank refresh in a named LPDDR2-S4B product document

The June-2012 H9TCNNNBLDMMPR specification lists both all-bank auto refresh and per-bank auto refresh among the LPDDR2-S4B functions.

In the `Refresh Command` section, the command encoding distinguishes:

- `REFpb` — Per Bank Refresh;
- `REFab` — All Bank Refresh.

This moves the bounded cross-vendor **product-document floor** for Case 105 from Micron's July 2014 witness to SK hynix's June 2012 witness.

It does not establish the first commercial LPDDR2 per-bank-refresh product.

### H/P — REFpb follows a fixed round-robin bank sequence

The product specification says that REFpb operates on the bank scheduled by an internal bank counter and gives the fixed sequence:

```text
0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 0 -> ...
```

It further says the bank count is synchronized between controller and SDRAM by resetting the bank count to zero:

- on RESET; or
- on every exit from self refresh.

The controller is explicitly responsible for tracking which bank is being refreshed.

This is a strong product-level witness that the target sequence is a **shared controller/device coordination relation**, not merely invisible internal work.

### H/P — target-bank service withdrawal is local, not device-wide

The document states that the REFpb target bank is inaccessible during `tRFCpb`, while other banks remain accessible and may receive ordinary operations, including reads and writes, subject to the other timing/state rules.

The product contract therefore directly supports:

```text
bank currently being maintained
    !=
device globally unavailable
```

and:

```text
service from another bank
    !=
proof that the target bank has completed its refresh
```

### H/P — a full cycle of eight REFpb commands substitutes for one REFab in refresh accounting

The LPDDR2 refresh-requirements section defines a rolling refresh-window obligation and states that, on devices supporting per-bank refresh, **one REFab may be replaced by a full cycle of eight REFpb commands**.

For the documented high-density eight-bank organization, the specification therefore makes a useful scope distinction explicit:

```text
one REFpb
    = one bank-local refresh transaction

full cycle of eight REFpb
    = accounting substitute for one REFab
```

This is an interface/accounting equivalence. It is not a claim that one REFab and eight REFpb are identical in latency, service interference, internal physical sequencing, energy, or controller scheduling burden.

### H/P — self-refresh exit exposes an additional maintenance-accounting boundary

The same specification warns that an internally timed refresh event can be missed during self-refresh exit. Before entering a subsequent self-refresh interval, it requires at least one refresh command, explicitly glossed as:

```text
8 per-bank or 1 all-bank
```

This is especially useful for technical-retention because it shows a maintenance obligation spanning a **regime transition**:

```text
self-refresh mode exited
    !=
all refresh accounting automatically settled
```

The controller may have to issue explicit follow-up maintenance before the next self-refresh entry.

Nothing in this statement proves that exact in-flight refresh progress is persisted across power loss or that the bank counter is a durable checkpoint.

### H/P — PASR supplies an in-product counterexample to equating bank-local transaction scope with retained-set scope

The same H9TCNNNBLDMMPR document separately defines Partial Array Self Refresh bank masking. It states that if a bank is masked, refresh for the entire bank is blocked and **data retention by that bank is not guaranteed in self-refresh mode**.

Thus, within one manufacturer's one product specification, two superficially `partial` mechanisms have different meanings:

```text
REFpb
    one maintenance transaction targets one bank
    but repeated transactions still contribute to full-bank refresh coverage

PASR bank masking
    a bank can be excluded from self-refresh maintenance
    and retention for that bank is not guaranteed
```

This independently corroborates the canonical Case-105 distinction from Case 104:

> **maintenance transaction scope != retained-set scope**.

---

## Engineering reconstruction

### E — Case 105's main boundary is not Micron-specific

The original Micron witness remains valid, but the 2012 SK hynix product document independently exposes the same broad LPDDR2 relation:

```text
bank-local refresh transaction
    + other-bank concurrency
    + controller/device bank-sequence coordination
    + full-bank rolling refresh obligation
```

The defensible cross-vendor result is therefore stronger than a single-vendor reading:

> By June 2012, a named SK hynix LPDDR2 product specification publicly documented the same bounded interface relation that the original Case 105 grounded from Micron in 2014.

This does not establish identical silicon or a direct Hynix -> Micron genealogy.

### E — maintenance completion needs a typed scope

The source set now supplies three different completion units:

1. completion of **one REFpb transaction** for one bank;
2. completion of **a full eight-bank REFpb cycle** that can stand in for one REFab in the documented accounting;
3. satisfaction of the **rolling refresh-window obligation**, which requires enough refresh work over time.

Therefore:

```text
one maintenance command completed
    !=
full bank-set cycle completed
    !=
rolling retention obligation satisfied
```

A statement such as `refresh complete` is under-specified unless its scope and accounting horizon are named.

### E — bank-sequence state is coordination infrastructure, not application history

The internal bank counter and the controller's corresponding tracking relation determine which bank a REFpb applies to next. RESET and self-refresh exit re-synchronize that relation to bank zero in the product contract.

This supports a bounded persistence-horizon interpretation:

```text
maintenance target-sequence state
    must remain coherent while the regime relies on it
    but
need not be preserved as durable application history across every reset boundary
```

Reinitialization of maintenance enumeration is not application-data rollback.

### E — regime transitions can create maintenance handoff debt

The self-refresh-exit rule shows that leaving an internally maintained regime can create or expose a bounded follow-up obligation before another self-refresh interval is entered.

Project-level reconstruction:

```text
internal maintenance regime
    -> exit transition
    -> possible missed internal refresh event
    -> explicit controller-issued refresh requirement
    -> next self-refresh entry admitted
```

`maintenance handoff debt` is project vocabulary, not SK hynix terminology.

### E — concurrency is not reduced retention work

REFpb permits ordinary operations in non-target banks. This reduces the **service interference scope** of a refresh transaction, not the physical requirement to refresh the target bank or the global requirement to cover all banks over the refresh window.

Therefore:

```text
more foreground concurrency
    !=
less total retention obligation
```

---

## Prior-art boundary

This slice establishes two conservative floors for different claims:

### 2009 — manufacturer-primary design-publication floor

By 7 May 2009, Hynix publicly disclosed a per-bank-refresh address/control design in which a specific bank can be refreshed while other banks continue ordinary access and in which bank-address sequencing is internally tracked.

This is **design prior art**, not a named shipping-product witness.

### 2012 — cross-vendor named-product-document floor

By the June-2012 revision of H9TCNNNBLDMMPR, SK hynix documented LPDDR2-S4B product semantics for:

- REFpb and REFab;
- fixed round-robin bank targeting;
- controller bank tracking;
- other-bank service during `tRFCpb`;
- full-cycle eight-REFpb substitution for one REFab;
- self-refresh-exit follow-up refresh;
- PASR bank masking with no retention guarantee for masked banks.

This moves Case 105's bounded product-document floor earlier than the original Micron July-2014 witness.

### What remains open

This evidence does **not** close:

- first invention of per-bank refresh;
- first product shipment;
- exact normative JEDEC introduction/revision chronology;
- direct lineage from US20090116326A1 to H9TCNNNBLDMMPR;
- Hynix-to-Micron influence;
- exact circuit identity across vendors;
- controller implementation strategies;
- cross-vendor conformance traces;
- timing/energy measurements under REFpb versus REFab;
- reset/power-failure fault injection;
- whether the mirrored PDF is byte-identical to every contemporaneous SK hynix distribution copy.

A direct revision-by-revision JEDEC investigation remains the clean next step for standards genealogy. Broad DRAM per-bank-refresh history should primarily be routed to `computing-archaeology`.

---

## Functional comparison

### Case 104 — PASR

Case 104 changes **which payload regions are promised self-refresh maintenance**. The 2012 SK hynix PASR text directly says a masked bank may lose retention guarantee.

Case 105 REFpb changes the **scope of one refresh transaction** while retaining a bank-complete rolling maintenance obligation.

This is a functional comparison, not a claim that one feature descended from the other.

### Case 106 — DDR5 REFsb

Case 106 later shows a different target geometry: same-bank refresh can target corresponding banks across bank groups. The common analytical question is target-set scope versus whole retention obligation.

The mechanisms and interface contracts are not identical, and the comparison makes no LPDDR2 -> DDR5 direct genealogy claim.

### Case 09 — refresh-address internalization

Case 09 established that row enumeration can move on-chip without moving all cadence authority. The Hynix patent/product evidence adds another coordinate: **bank target enumeration** can itself become retained maintenance-control state.

Again, this is a functional bridge, not a historical continuity claim.

---

## Philosophical limit

A narrow conceptual result follows from the mechanism:

> A system can preserve a globally required relation through a sequence of locally scoped maintenance acts, while retaining just enough coordination state to know which local act comes next.

The source documents do not formulate a philosophy of memory, temporality, or distributed obligation. Terms such as `maintenance debt`, `global obligation`, and `coordination state` are engineering/philosophical reconstruction vocabulary used to expose the relation.

The analogy stops before treating a DRAM bank sequence as an archive, institutional schedule, or distributed consensus protocol.

---

## Counterexamples and non-claims

The following shortcuts are explicitly rejected:

```text
per-bank refresh exists in a patent
    !=
patented circuit shipped in H9TCNNNBLDMMPR

2007 priority date
    !=
2007 public disclosure

June-2012 product document
    !=
first commercial LPDDR2 per-bank-refresh product

same broad REFpb semantics across Hynix and Micron
    !=
identical silicon
    !=
direct vendor-to-vendor genealogy

8 REFpb can substitute for 1 REFab in accounting
    !=
identical timing
    !=
identical physical action
    !=
identical energy or service cost

one REFpb complete
    !=
all-bank maintenance complete
    !=
rolling refresh obligation discharged

other-bank access available
    !=
target-bank refresh complete

bank counter synchronized at RESET/self-refresh exit
    !=
cross-reset persistent checkpoint

PASR masked bank not guaranteed retained
    !=
secure erasure or sanitization

manufacturer-authored mirrored PDF
    !=
currently origin-hosted archival copy

similarity to JEDEC-era interface language
    !=
directly inspected normative JEDEC genealogy
```

---

## Claim ledger

| Claim | Label | Evidence | Strength |
| --- | --- | --- | --- |
| Hynix publicly disclosed a per-bank-refresh address/control design by 7 May 2009 | H/P | US20090116326A1 publication metadata and description | strong |
| the patent describes one-bank refresh with ordinary operations possible in other banks | H/P | US20090116326A1 description | strong |
| the patent describes internal sequential/round-robin bank-address counting for per-bank refresh | H/P | US20090116326A1 description | strong |
| the patent was necessarily implemented by the 2012 LPDDR2 product | X | not established | rejected |
| SK hynix H9TCNNNBLDMMPR Rev. 1.1 is dated June 2012 | H/P | document title/revision pages | strong, mirrored manufacturer document |
| H9TCNNNBLDMMPR exposes REFpb and REFab | H/P | refresh-command section | strong |
| REFpb follows a fixed 0..7 round-robin bank sequence | H/P | refresh-command section | strong |
| controller and SDRAM bank count are synchronized to zero by RESET and self-refresh exit | H/P | refresh-command section | strong |
| controller must track the REFpb bank | H/P | refresh-command section | strong |
| target bank is inaccessible during tRFCpb while other banks can remain accessible/read/write | H/P | refresh-command section | strong |
| one REFab can be replaced by one full cycle of eight REFpb for the documented refresh accounting | H/P | refresh-requirements section | strong |
| before a subsequent self-refresh entry, exit may require 8 per-bank or 1 all-bank refresh command | H/P | self-refresh section | strong |
| a PASR-masked bank has refresh blocked and its data retention is not guaranteed in self refresh | H/P | PASR bank-masking section | strong |
| one completed REFpb proves whole-array refresh freshness | X | contradicted by full-cycle/rolling-window requirement | rejected |
| REFpb and PASR mean the same kind of `partial refresh` | X | contradicted by source semantics | rejected |
| the cross-vendor product comparison proves exact JEDEC clause ancestry | X | normative standard not directly inspected here | rejected |
| Case 105's `transaction scope != retained-set scope` relation is independently supported by SK hynix 2012 | E | reconstruction from REFpb full-cycle requirement plus PASR retention warning | strong bounded reconstruction |

---

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for the relevant self-/per-bank-refresh terms found no dedicated study to reuse.

Keep here:

- retention-specific target-scope / coverage-scope distinction;
- maintenance-enumerator persistence horizon;
- cross-vendor counterexample to a Micron-only reading;
- PASR versus REFpb retention boundary.

Route primarily to `computing-archaeology` if pursued broadly:

- pre-2009 per-bank-refresh circuit genealogy;
- LPDDR/LPDDR2 standards committee chronology;
- vendor product/shipment chronology;
- controller scheduling history;
- circuit-family lineage and patent-prosecution history.

---

## Sources

1. Sang Kwon Lee / Hynix Semiconductor Inc., US20090116326A1, _Semiconductor memory device capable of performing per-bank refresh_, US publication 7 May 2009; priority 2 November 2007; filed 27 June 2008. Google Patents: <https://patents.google.com/patent/US20090116326A1/en>.
2. SK hynix, _16Gb LPDDR2-S4B (x32, 2CS) H9TCNNNBLDMMPR_, MCP Specification, Rev. 1.1, June 2012. Manufacturer-authored PDF surviving through a third-party mirror: <https://14469692.s21i.faiusr.com/61/ABUIABA9GAAgpfTMqgYoysi4pgQ.pdf>. Relevant document sections include the title/revision-history pages, `Refresh Command`, `LPDDR2 SDRAM Refresh Requirements`, `Self refresh operation`, and `Partial Array Self Refresh: Bank Masking`.

## Bounded conclusion

The new evidence changes Case 105 in one precise way. The original Micron 2014 product witness is no longer the earliest product-document anchor in the case. A June-2012 SK hynix LPDDR2-S4B specification independently documents the bank-local transaction / other-bank concurrency / round-robin target tracking / full-bank rolling-coverage relation, while the same product's PASR text proves that bank-local transaction scope is not the same thing as selectively withdrawing a bank from the retained set. A 2009 Hynix patent supplies an earlier manufacturer-primary design floor for per-bank address/control machinery but is kept separate from product implementation.

The defensible result is:

```text
bank-local maintenance execution
    != bank-local retention promise

one transaction complete
    != one bank-set cycle complete
    != rolling refresh obligation satisfied

maintenance target-sequence state
    != application payload
    != durable cross-reset history

2009 design disclosure
    != 2012 product implementation proof
    != invention priority
```
