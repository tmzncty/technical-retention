# Case 03 Deepening — TI 1978 On-Chip Refresh Counter Prior Art and Coverage-State Topology

**Status:** `bounded deepening complete`

## Research question

Case 03 already separates the physical DRAM payload from the control state that keeps refresh coverage moving. Existing evidence now includes:

- Dennard's charge-retention / regeneration obligation;
- late-1970s RAS-only refresh;
- Intel external refresh timers, counters, and arbitration;
- Mostek's 1979–1980 MK4164 `RFSH` mode, including an on-chip refresh counter that Mostek explicitly calls dynamic;
- later CAS-before-RAS refresh and self-refresh evidence;
- a bounded cross-vendor 64K refresh-organization comparison.

One debt remained unusually exposed: the repository had a **1979 public-product-document floor** for Mostek's on-chip refresh counter, but it had not yet inspected an earlier same-die refresh-counter filing or recovered a contemporary internal counter embodiment.

This slice asks two bounded questions:

> By what date can the current source set establish a filed patent claim for a refresh-address counter on the same semiconductor body as the DRAM array?

and:

> What did that source actually require the counter to remember, and did the refresh-coverage obligation require a particular numerical traversal order?

Texas Instruments' White/Rao patent family supplies a useful answer. The US application was filed on **26 June 1978** and later published/granted as `US4207618A` on **10 June 1980**. Its British family publication `GB2024474A` appeared on **9 January 1980**. The claimed architecture places the refresh-address counter and address-selection circuitry on the DRAM chip while still requiring an externally generated refresh command. The preferred embodiment describes eight clocked D-type latches holding refresh-address state produced by binary adder/counter stages, and the text explicitly says the row sequence need not be numerical if every required address is covered without repetition inside the refresh window.

The bounded result is therefore:

```text
same-die refresh-address state
    !=
autonomous refresh cadence

refresh-coverage obligation
    !=
mandatory numerical traversal order

1978 filing / priority
    !=
1978 public availability
    !=
1979 product documentation
    !=
shipping implementation
```

This slice moves a **filing / priority floor** and adds a concrete claimed counter topology. It does **not** establish invention priority, product adoption, first silicon, first shipment, or a TI-to-Mostek genealogy.

---

## Why this slice is not a duplicate

The existing Mostek deepening, [`03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md`](03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md), establishes a different and unusually strong product-document fact:

```text
Mostek MK4164 internal refresh counter
    -> explicitly described as dynamic
    -> explicitly said to require refreshing
```

It also establishes a **1979 public Mostek product-brief floor** for the phrase `On chip refresh counter on pin 1`.

The present TI slice changes neither result. Instead it adds:

1. a **26-Jun-1978 filing/priority date** for an on-chip refresh-address-counter architecture;
2. a **9-Jan-1980 public British-family publication date** and **10-Jun-1980 US publication/grant date**;
3. a source-level description of one claimed / preferred counter organization;
4. explicit evidence that refresh coverage is a set-and-deadline obligation rather than necessarily a numerical-counting obligation;
5. an earlier GTE system-level prior-art boundary that already had autonomous cadence and external coverage traversal without putting the counter on the DRAM die.

The distinction matters because four different historical propositions can otherwise be silently collapsed:

```text
a concept was filed
    !=
a concept was publicly disclosed
    !=
a product document advertised it
    !=
a product shipped with it
```

---

## Source custody and dating

### Primary patent — Texas Instruments, White / Rao

**Lionel S. White, Jr. and G. R. Mohan Rao, “On-chip refresh for dynamic memory,” US4207618A.**

- assignee: Texas Instruments Incorporated;
- US application / priority date: **1978-06-26**;
- US publication / grant date: **1980-06-10**;
- patent family includes British application `GB7922161A`;
- British A-publication `GB2024474A`: **1980-01-09**.

Public records:

- Google Patents, US family record: <https://patents.google.com/patent/US4207618A/en>
- Google Patents, British family record: <https://patents.google.com/patent/GB2024474A/en>

The US record identifies White and Rao as inventors and TI as assignee. Its description says conventional high-density dynamic RAMs require external refresh systems and names the system-level components then commonly needed: a refresh-address counter, a mechanism to let refresh occur, and a timer deciding when refresh should happen. The proposed device moves the refresh-address counter and address-multiplexing circuitry onto the DRAM chip.

**Chronology boundary:** the **1978 filing / priority date is not a 1978 public-publication date**. The earliest public patent-family publication directly established in this round is the British `GB2024474A` publication on 9 January 1980. Mostek's separately inspected **1979 product brief** therefore remains earlier in the repository's current public-product-document chain.

### Earlier system-level prior art — GTE / Shuba

**Joseph Patrick Shuba, “Dynamic mode integrated circuit memory with self-initiating refresh means,” US3729722A.**

- assignee at filing: GTE Automatic Electric Laboratories Incorporated;
- filing / priority date: **1971-09-17**;
- publication / grant date: **1973-04-24**.

Public record:

- <https://patents.google.com/patent/US3729722A/en>

This is important because it prevents the TI filing from being narrated as if the idea of autonomous dynamic-memory refresh control began in 1978. Shuba describes a **memory system** with:

- a free-running clock;
- a refresh pulse generator;
- a row-address counter;
- gating into memory row-address drivers;
- periodic traversal sufficient to refresh all rows before the deadline.

The preferred embodiment is described using commercially available Intel 1103 memory chips. The refresh counter is system-level support circuitry; the source does not establish that the row-address counter is integrated into each 1103 die.

The TI patent itself cites Shuba's `US3729722A` among its prior patents. That citation supports a real documentary relationship at the patent-prior-art level, but not a claim that every TI circuit detail descends from Shuba.

### Existing product-document comparison — Mostek MK4164

Case 03 already directly inspected:

- Mostek's **1979 Memory Data Book and Designers Guide** product brief;
- Mostek's **1980 Memory Data Book and Designers Guide** detailed MK4164 entry;
- Mostek's 1980 product guide, which still described the device as `Available Soon` in that record.

See:

- [`03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md`](03-mostek-1979-1980-rfsh-dynamic-counter-deepening.md)

This remains the repository's stronger source for a **named product / product-plan documentation** claim. The TI patent is a mechanism / claimed-architecture source, not a substitute for shipment evidence.

---

## Historical record

### H/P — 1971–1973 GTE already separates cadence, coverage state, and DRAM payload at system level

Shuba's GTE patent is a useful earlier boundary because it makes several refresh-control functions explicit outside the DRAM chips.

The described system uses a free-running clock to trigger a refresh pulse generator periodically. The pulse generator advances a row-address counter and gates that address into the memory row drivers. In the Intel 1103 example, the patent describes 32 rows that must all be refreshed within two milliseconds; a 16 kHz clock generates one refresh opportunity every 62.5 microseconds.

The period architecture can therefore be decomposed as:

```text
DRAM stored charge
    !=
refresh cadence source
    !=
next-row / coverage state
    !=
address-selection gating
```

This source is earlier than the TI filing, but it is not an on-chip-refresh-counter witness. Its relevance is precisely to show that **system-level self-initiation** and **same-die refresh-address state** are different historical propositions.

### H/P — the TI filing moves refresh-address state and selection onto the DRAM chip

The TI patent's background says high-density dynamic RAMs require external refresh systems and explicitly lists a refresh-address counter and timing/control overhead as part of that burden.

Its proposed solution is a memory device with:

- a refresh-address counter on the dynamic-RAM chip;
- address multiplexing / selection on the chip;
- an externally supplied refresh command;
- internal selection of a row according to the counter;
- advancement of the counter for later refresh.

For a 65,536-cell example, the description uses 256 rows × 256 columns. Normal access receives row / column addresses through the external address pins, while refresh substitutes an internally generated row address into the row decoder.

The historical control boundary is direct:

```text
normal access address
    -> external address pins

refresh row address
    -> on-chip counter
    -> on-chip selection / multiplexing
```

but:

```text
refresh event / command
    -> still supplied externally
```

Therefore the patent is evidence for **on-chip coverage-state generation**, not for fully autonomous self-refresh.

### H/P — the preferred counter embodiment has separately held address state

The patent's FIG. 3 description gives a concrete preferred embodiment rather than merely naming an abstract counter.

It describes:

- eight latches;
- those latches as clocked D-type flip-flops;
- eight binary adder / counter stages;
- carry propagation between stages;
- a clock at the end of a refresh cycle that transfers the next generated address into the latches;
- the stored latch value remaining until another refresh signal advances the sequence.

In bounded historical terms:

```text
refresh-address state
    -> held in latches

next-address computation
    -> adder / counter stages

refresh-cycle boundary
    -> state update
```

This is valuable because it exposes the contemporary mechanism used to embody `where refresh is in its traversal`.

The patent is not used to claim that every TI implementation, every later 64K DRAM, or the Mostek MK4164 used this exact transistor-level organization.

### H/P — the coverage sequence need not be numerical

The same description explicitly says the rows must be addressed in some sequence so every row is reached within the maximum refresh time. It then says the address sequence **need not advance in numerical order** so long as addresses are not repeated before the necessary coverage is obtained, and gives a pseudo-random shift counter as an alternative.

This is unusually useful for Case 03 because it separates the obligation from one implementation convenience:

```text
refresh correctness requires:
    required row set covered
    within deadline

refresh correctness does not inherently require:
    0, 1, 2, 3, ... numerical traversal
```

The document's regular binary counter is an embodiment. Numerical ordering is not the retention invariant.

### H/P — an external refresh command remains part of the claimed contract

The TI proposal is sometimes easy to misread as `self-refresh` because it moves the address counter on-chip. The patent itself blocks that shortcut: it states that the only external signal needed for the proposed on-chip-refresh path is a refresh command that causes a row to be accessed according to the internal counter and advances the counter.

Accordingly:

```text
on-chip address generation
    !=
on-chip deadline generation
```

The earlier GTE system can have a free-running clock and autonomous system-level refresh initiation without an on-die counter; the TI chip can have an on-die counter while still needing an external refresh event. `Where coverage state lives` and `who decides when the next refresh occurs` are orthogonal questions.

### H/P — patent-family chronology must not be flattened

The directly checked dates produce this bounded chronology:

```text
1971-09-17
    GTE / Shuba files system-level self-initiating refresh apparatus

1973-04-24
    US3729722A publicly issues

1978-06-26
    TI / White-Rao US on-chip-refresh application filed
    priority date for the patent family

1979
    Mostek public product brief advertises
    “On chip refresh counter on pin 1”

1980-01-09
    TI family GB2024474A publicly published

1980-06-10
    US4207618A publicly issued / published
```

This chronology supports two different floors:

```text
current bounded filing / priority floor for same-die counter:
    TI, 26-Jun-1978

current bounded public product-document floor:
    Mostek, 1979
```

Neither floor is an invention-priority or first-shipment conclusion.

---

## Engineering reconstruction

### E — refresh retention has at least four separable control dimensions

Combining the GTE, TI, Mostek, and later Case-03 material supports a sharper decomposition:

```text
retention deadline
    !=
refresh-event / cadence source
    !=
coverage-set cardinality
    !=
coverage position / progression state
    !=
traversal order
    !=
restore execution
```

The important new term in this slice is **traversal order**.

A counter often suggests numerical progression, but the TI patent explicitly permits another sequence. The retention contract is therefore better described as a coverage condition than as a requirement to preserve one canonical order.

### E — coverage state is a compressed maintenance history, not a complete history log

An on-chip counter answers a narrow operational question:

> Which refresh address should be supplied next under this traversal scheme?

It does not retain a full record of every past refresh event, elapsed interval, access, or disturbance.

For the regular counter embodiment:

```text
retained / operational coverage position
    +
known traversal rule
    -> next refresh address
```

This is enough for a particular recurrence regime even though the historical event stream is discarded.

Thus:

```text
sufficient state to continue maintenance
    !=
complete history of maintenance
```

This is an engineering reconstruction, not terminology attributed to White, Rao, Shuba, or Mostek.

### E — the same coverage invariant can admit different state encodings

Because the TI patent permits both a regular numerical counter and a pseudo-random shift-counter alternative, the same bounded maintenance obligation can be implemented through different state-transition systems.

At the interface level:

```text
implementation A:
    binary count state
    -> numerical next row

implementation B:
    shift / pseudo-random state
    -> nonnumerical next row

shared obligation:
    cover every required row before the deadline
```

This is useful beyond DRAM only as a functional pattern. It does not imply equivalence of the circuits, failure modes, or testability.

### E — coverage-state survival is not coverage-state correctness

The TI latches can hold a refresh address between refresh events. That establishes an operational state locus in the described architecture.

It does not establish:

- independent integrity protection for that state;
- detection of skipped / duplicated coverage positions;
- persistence across power loss;
- correctness after an arbitrary control upset;
- proof of completed row-set coverage.

So the existing Case-03 distinction remains necessary:

```text
coverage state exists
    !=
coverage state is correct
    !=
coverage obligation has been satisfied
```

The later Intel 8202A TEST-mode evidence remains a stronger product-level witness for control-state disturbance creating later retention risk.

### E — same-die placement reduces one external apparatus without eliminating system dependency

The TI architecture reduces external refresh-address-support hardware by moving the row-address progression and selection onto the DRAM chip.

But an external refresh event still has to arrive in time. Therefore:

```text
external address-counter burden reduced
    !=
external timing responsibility eliminated
```

This strengthens the repository's repeated rule:

```text
internalization of one maintenance function
    !=
internalization of the whole maintenance regime
```

### E — the TI topology should not be projected onto the MK4164

The Mostek source explicitly calls its internal refresh counter **dynamic** and says it requires refreshing. The TI source instead describes refresh-address storage using clocked D-type latches and adder/counter stages; it does not make the same statement that this counter state itself needs periodic refresh.

The safe comparison is:

```text
Mostek product documentation:
    on-chip RFSH counter
    explicitly dynamic / refresh-dependent

TI patent embodiment:
    on-chip counter
    latch + adder/counter organization described
    no equivalent counter-refresh requirement established here
```

This does **not** prove that the two circuits used different device physics in every implementation detail. It only proves that the inspected sources expose different claims and different levels of implementation detail.

---

## Functional comparison — not genealogy

### A — GTE system-level refresh controller vs TI same-die coverage state

```text
GTE / Shuba 1971-filed system:
    free-running clock
    refresh pulse generator
    external row-address counter
    gating to DRAM row drivers
    autonomous system-level cadence

TI / White-Rao 1978-filed device:
    external refresh command
    on-chip refresh-address counter
    on-chip address selection
    internal row refresh execution
```

Useful functional distinction:

```text
cadence locus
    !=
coverage-state locus
```

No broader GTE→TI invention genealogy is asserted beyond the documented fact that the TI patent cites Shuba among prior patents.

### A — TI patent vs Mostek MK4164 product record

```text
TI:
    earlier filing / priority floor
    later public patent publication
    claimed on-chip counter architecture
    explicit preferred latch/adder embodiment

Mostek:
    earlier currently inspected public product-document witness
    named MK4164 product brief / data-book context
    RFSH interface
    counter explicitly described as dynamic
```

Useful provenance rule:

```text
patent filing chronology
    !=
public disclosure chronology
    !=
product-document chronology
    !=
shipment chronology
```

### A — numerical counter vs pseudo-random traversal

The patent itself offers this comparison; it is not a later analogy.

What the repository adds is the retention formulation:

```text
one exact next-row encoding
    is contingent

complete bounded row-set coverage
    is the relevant obligation
```

This should not be generalized into a claim that all DRAM refresh controllers may use arbitrary permutations without additional timing / implementation constraints.

---

## Philosophical interpretation

### P — persistence can depend on retaining only enough past to continue a recurrence

The counter does not preserve a narrative history of refresh. It preserves a small operational difference that lets the mechanism continue the maintenance traversal.

The bounded interpretive point is:

> a technical system may retain enough of its own maintenance past to continue preserving another state, while discarding almost all of the event history that produced the current maintenance position.

That is not a claim that a refresh counter is `memory of memory` in a psychological sense. It is a precise engineering condition that can discipline such a metaphor rather than license it.

### P — identity of an obligation need not imply identity of sequence

If two traversal mechanisms cover the same required row set before the same deadline, they can satisfy the same bounded retention obligation while visiting rows in different orders.

So:

```text
same retention obligation
    !=
same temporal sequence of maintenance events
```

This is a project-level interpretation of the patent's explicit sequence flexibility, not historical vocabulary attributed to TI.

---

## Explicit non-claims

This evidence does **not** establish any of the following:

1. White and Rao invented the first on-chip DRAM refresh counter.
2. The 26-Jun-1978 filing date is a 1978 public-disclosure date.
3. `GB2024474A` was public in 1978; the checked A-publication date is 9-Jan-1980.
4. The US patent was public before 10-Jun-1980.
5. The TI architecture shipped in a named 1978, 1979, or 1980 DRAM product.
6. The TI patent describes the Mostek MK4164 circuit.
7. The Mostek MK4164 derives from the TI patent.
8. TI's patent filing predates every unpublished or published same-die refresh-counter proposal.
9. Shuba's 1971-filed GTE architecture places the refresh row counter on each Intel 1103 chip.
10. `self-initiating` in the GTE system means that the 1103 itself contains an autonomous self-refresh timer.
11. An on-chip refresh counter is equivalent to self-refresh.
12. Internal refresh-address generation is equivalent to internal refresh-cadence generation.
13. A D-type latch label proves the complete transistor-level or leakage behavior of every implemented TI counter bit.
14. The TI counter is proven non-dynamic in every physical sense; this source simply does not make Mostek's explicit counter-refresh claim.
15. The TI preferred embodiment is the only circuit covered by the patent claims.
16. A pseudo-random sequence was used in a shipping product.
17. Any arbitrary pseudo-random sequence satisfies a DRAM refresh contract.
18. `no address repeated` alone is sufficient without also meeting complete coverage and the device's maximum refresh time.
19. A surviving refresh-counter state is necessarily correct.
20. Counter correctness proves that every row was actually restored electrically.
21. Moving the counter on-chip removes refresh/access arbitration or all external support logic.
22. Patent citations prove detailed circuit genealogy.
23. A patent mechanism proves first silicon, yield, production readiness, market adoption, or shipment date.
24. The 1979 Mostek product brief proves 1979 volume shipment; existing Mostek evidence explicitly preserves that boundary.
25. The current bounded source search exhausts the pre-1978 patent / publication record.

---

## What this changes in Case 03

This slice closes part of the previously broad `earliest on-chip refresh-counter prior art` debt by replacing an undifferentiated unknown with a source-controlled boundary:

```text
same-die refresh-counter filing / priority:
    established at least by 26-Jun-1978
    in TI White/Rao US application

public patent-family disclosure:
    established by 9-Jan-1980
    in GB2024474A

public product-document witness:
    still separately established in 1979
    by Mostek MK4164 product brief
```

It also adds an explicit contemporary topology for one claimed on-chip refresh counter and sharpens the control decomposition with **traversal order**.

Case 03 remains **`grounded`**. This evidence does not justify maturity promotion.

The remaining debt is narrower:

1. search pre-26-Jun-1978 same-die refresh-address-counter patents, papers, or product documents before making any priority claim;
2. establish whether a named TI DRAM product implemented the White/Rao architecture, rather than treating patent disclosure as product evidence;
3. preserve the separate Mostek first-silicon / first-shipment question;
4. recover the exact MK4164 internal counter topology from circuit disclosure, die analysis, or other primary engineering evidence if available;
5. compare TI / Mostek / other contemporary counter failure modes only when implementation-level sources permit it;
6. perform controlled hardware observation only as **Experiment**, not as historical proof.

---

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for both `US4207618A` and `on-chip refresh dynamic memory` returned no dedicated packet to reuse in this round.

Keep here:

- the retention-specific chronology boundary between filing, public disclosure, product documentation, and shipment;
- the location of refresh-coverage state;
- the distinction between coverage state and cadence authority;
- the distinction between coverage invariant and traversal order;
- the role of minimal retained control state in continuing maintenance.

Route primarily to `computing-archaeology` if pursued:

- a broad TI / Mostek / Intel / NEC DRAM product genealogy;
- the full patent-family / examiner-history network;
- semiconductor process and die-layout history;
- manufacturing, pricing, shipment, and market-adoption chronology;
- general DRAM controller evolution beyond the retention seam.

---

## Compact map

```text
DRAM payload charge
    |
    +-- retention deadline
    |
    +-- refresh event / cadence
    |      GTE: free-running system clock
    |      TI same-die-counter patent: still external refresh command
    |
    +-- coverage state
    |      GTE: system-level row counter
    |      TI: same-die counter
    |      Mostek MK4164: on-chip RFSH counter
    |
    +-- traversal representation
    |      binary numerical sequence
    |      or another complete nonrepeating sequence
    |
    +-- restore execution
           DRAM array / sense-restore path
```

The strongest new Case-03 rule from this slice is:

```text
where the system remembers “which row comes next”
    !=
who decides “when the next refresh must happen”

and

which row comes next
    !=
the retention invariant that all required rows be covered in time
```
