# Case 135 deepening evidence — e.MMC 4.5/4.51 RTC lineage before e.MMC 5.0 (2011–2012)

## Status

**`bounded deepening complete`** for one chronology question: the host/device time-maintenance control surface used by Case 135 did not begin with e.MMC 5.0. JEDEC's own later revision history identifies **real-time-clock support as an e.MMC 4.5 reliability addition**, and a maintained `mmc-utils` implementation classifies `PERIODIC_WAKEUP[131]` in its **B45** EXT_CSD block.

The direct clause-by-clause text of JESD84-B45/B451 was not recovered in a sufficiently inspectable primary copy in this pass. Accordingly, this record **does not** claim that every `SET_TIME`, `PERIODIC_WAKEUP`, encoding, reset, optionality, or completion rule visible in JESD84-B50/B51 was already textually identical in 4.5 or 4.51.

Case 135 remains **`grounded`**. This pass corrects chronology and narrows the remaining standards debt; it does not justify a maturity promotion.

## Research question

The existing Case 135 standards deepening established a directly inspectable floor at JESD84-B50 (e.MMC 5.0, September 2013):

- host-supplied absolute or relative time through `SET_TIME (CMD49)`;
- a `PERIODIC_WAKEUP` control at EXT_CSD byte 131;
- periodic power-up combined with at least one completed background operation before power-down; and
- explicit discussion of host-provided time as potentially useful for internal maintenance.

That record deliberately left invention/origin open.

This pass asks a narrower prior-art/chronology question:

> Does the public standards record put RTC-related maintenance support, and specifically the `PERIODIC_WAKEUP` register family, before e.MMC 5.0?

The answer is **yes at the feature-lineage level**, but with an important clause-level caveat.

## Source boundary and source classes

### A1 — JEDEC-origin e.MMC 4.5 announcement, 15 June 2011

A contemporaneous republication of JEDEC's announcement identifies **JESD84-B45** as e.MMC 4.5 and is dated **15 June 2011**:

<https://www.design-reuse.com/news/202520380-jedec-announces-publication-of-e-mmc-standard-update-v4-5/>

The announcement says that e.MMC 4.5 adds the capability for the device to retrieve **Real-Time Clock information from the host system**, and that the information may be used by the device's internal memory management to improve data integrity and reliability.

This is a near-contemporaneous JEDEC-origin publication witness. It is strong evidence for the public feature milestone, but it is not a substitute for every normative bit/field rule in JESD84-B45.

### A2 — JEDEC JESD84-B51 Annex C revision history, February 2015

A public text-preserving copy of **JESD84-B51, _Embedded Multi-Media Card (e.MMC) Electrical Standard (5.1)_**, February 2015, preserves Annex C's revision history:

<https://pdfcoffee.com/jedec-standard-embedded-multi-media-card-e-mmc-electrical-standard-51-pdf-free.html>

A second independently hosted text-preserving copy is available at:

<https://studylib.net/doc/27873175/emmc5.1%E5%AE%98%E6%96%B9%E6%A0%87%E5%87%86%E5%8D%8F%E8%AE%AE>

Annex C.6, **Changes from version 4.41 to 4.5**, lists among the reliability-oriented additions:

- real-time clock; and
- dynamic device capacity.

The exact wording is preserved as JEDEC standard content, although the transport copies are third-party mirrors. It is therefore used here as primary-origin standard text carried by non-primary hosts.

### A3 — `mmc-utils` EXT_CSD decoder as implementation corroboration

A maintained `mmc-utils` source snapshot hosted by Android's Git service contains an EXT_CSD decoding block explicitly labeled:

```c
/* B45 */
if (ext_csd_rev >= 6) {
    ...
    printf("Periodic Wake-up [PERIODIC_WAKEUP]: 0x%02x\n",
           ext_csd[131]);
    ...
}
```

Source:

<https://android.googlesource.com/platform/external/mmc-utils/+/50b68547ad895803128519af71c31b9f14bfc791/mmc_cmds.c>

This is strong implementation corroboration that tooling associates `PERIODIC_WAKEUP[131]` with the B45-generation EXT_CSD layout. It is **not** promoted into normative-priority evidence by itself.

### A4 — e.MMC 4.51 publication metadata / continuity witness

Arasan's July 2012 announcement records that JEDEC published **JESD84-B451 (e.MMC 4.51) in June 2012**, replacing 4.5. It describes 4.51 as adding corrections/clarifications and additional functionality while otherwise maintaining the 4.5 functionality:

<https://www.arasan.com/news/arasan-chip-systems-announces-support-of-new-jedec-standard-emmc-4-51/>

This is a vendor/standards-participant continuity witness, not JEDEC normative text. It supports the revision chronology and the proposition that 4.51 was an incremental successor, but it cannot establish that every RTC-related sentence or field was bit-for-bit unchanged.

### Existing Case 135 sources retained by reference

This pass does not re-ground the later product behavior. The canonical case and prior evidence already cover:

- Atmark Techno's 2021 Armadillo-IoT Gateway G4 product manual;
- Micron's later automotive eMMC refresh-note scope;
- e.MMC Background Operations;
- JESD84-B50's inspectable `SET_TIME` / RTC / `PERIODIC_WAKEUP` semantics.

See:

- [`../cases/135-micron-emmc-self-refresh-time-trigger-maintenance.md`](../cases/135-micron-emmc-self-refresh-time-trigger-maintenance.md)
- [`135-micron-emmc-2021-2023-self-refresh-grounding.md`](135-micron-emmc-2021-2023-self-refresh-grounding.md)
- [`135-jedec-emmc51-bkops-maintenance-opportunity-deepening.md`](135-jedec-emmc51-bkops-maintenance-opportunity-deepening.md)
- [`135-jesd84-b50-2013-rtc-periodic-wakeup-time-maintenance-deepening.md`](135-jesd84-b50-2013-rtc-periodic-wakeup-time-maintenance-deepening.md)

## Historical record

### H/P — e.MMC 4.5 publicly introduced RTC-related reliability support in June 2011

The 15 June 2011 JEDEC-origin announcement is explicit that the new e.MMC 4.5 standard adds a host-to-device **Real-Time Clock information** capability. It also supplies the intended reliability context: the device may use that information inside its memory management to improve data integrity and reliability.

This establishes a public 2011 floor for the general relation:

```text
host temporal information
    -> available to e.MMC device
    -> may inform internal memory management
    -> reliability / integrity purpose
```

The safe historical claim is therefore:

> By June 2011, e.MMC 4.5 publicly standardized RTC-related host/device support for device-internal reliability management.

This is earlier than the September-2013 e.MMC 5.0 floor previously used by this case.

### H/P — JEDEC's own later revision history assigns RTC to the 4.41 -> 4.5 transition

JESD84-B51 Annex C.6 retrospectively enumerates the changes from e.MMC 4.41 to 4.5. The list places **real time clock** under enhanced host/device communication techniques to improve reliability, alongside dynamic device capacity.

That later JEDEC revision history is especially useful because it is not merely a 2011 marketing summary. It is a standards-family genealogy written into a later JEDEC standard.

The bounded conclusion is:

```text
e.MMC 4.41
    -> e.MMC 4.5 adds RTC-related reliability capability
    -> e.MMC 4.51 revises the 4.5 generation
    -> e.MMC 5.0 later exposes inspectable RTC / periodic-wakeup clauses
```

This directly rejects the overly strong chronology:

```text
"e.MMC 5.0 introduced RTC support"
```

for Case 135.

### H/P — `PERIODIC_WAKEUP[131]` is associated with B45 in implementation tooling

The inspected `mmc-utils` source labels a decoding block `/* B45 */`, guards it with `ext_csd_rev >= 6`, and within that block prints EXT_CSD byte 131 as:

```text
Periodic Wake-up [PERIODIC_WAKEUP]
```

This is valuable because it narrows the prior-art question from a generic RTC feature to the actual field family used in later e.MMC text.

The strongest safe claim is:

> A maintained implementation of the e.MMC EXT_CSD version map treats `PERIODIC_WAKEUP[131]` as a B45-generation field.

The source does **not** by itself prove:

- the exact first normative publication date of the field;
- whether B45 and B451 define every encoding exactly as B50 does;
- whether the field was mandatory or optional in every relevant device profile;
- whether the B45 text imposed the same completed-BKOPS-before-power-down sequence later visible in B50.

### H/P — e.MMC 4.51 is an intervening standards epoch, not evidence that RTC began in 5.0

JESD84-B451 was published in June 2012 as e.MMC 4.51. Arasan's standards-support announcement describes it as a replacement for 4.5 centered on errata, clarifications, e2MMC supply detail, security-protocol pass-through, and restored Secure Trim/Secure Erase definitions, while otherwise retaining 4.5 functionality.

This means the historical chain contains an intermediate standards epoch:

```text
JESD84-B45 / e.MMC 4.5      June 2011
        ↓
JESD84-B451 / e.MMC 4.51    June 2012
        ↓
JESD84-B50 / e.MMC 5.0      September 2013
```

A citation to B50 is therefore a valid **directly inspected normative floor** for the later semantics, but it is not a valid **feature-origin date** for RTC-related maintenance support.

### H/P — e.MMC 5.0 remains the current direct clause-level floor in this repository

The earlier chronology correction does not make the existing B50 deepening obsolete.

The B50 evidence remains stronger for exact clause-level claims already made there because the inspected text directly exposes:

- absolute vs relative time information;
- host update timing;
- `SET_TIME (CMD49)`;
- the `PERIODIC_WAKEUP` field and encodings;
- the periodic wake-up sequence; and
- the requirement to allow at least one background operation to complete before the relevant power-down sequence.

So two different evidence questions now have two different floors:

```text
feature-lineage floor:
    e.MMC 4.5 / 2011

current directly inspected clause-level floor:
    e.MMC 5.0 / 2013
```

Those floors should not be collapsed.

## Engineering reconstruction

### E — standards chronology and behavioral identity are separate variables

A common failure mode in protocol history is to see a familiar field in a later standard and infer both its behavior and origin from that later text.

Case 135 now needs an explicit two-axis model:

```text
axis A — feature chronology
4.41
  -> 4.5 RTC-related reliability addition
  -> 4.51 revision
  -> 5.0 later revision
  -> 5.1 later clarification/evolution

axis B — inspected behavioral contract
field existence
  -> encoding
  -> command semantics
  -> lifecycle update rules
  -> wakeup obligation
  -> maintenance completion rule
```

Evidence on axis A does not automatically fill every cell on axis B.

### E — real-time information is maintenance evidence, not maintenance execution

The 2011 announcement already gives the useful high-level dependency:

```text
host temporal observation
    -> device receives temporal evidence
    -> internal memory management may use evidence
```

But temporal evidence is still only an input to a policy.

Therefore:

```text
RTC information available
    !=
maintenance due
    !=
maintenance admitted
    !=
maintenance executed
    !=
maintenance completed
```

This is consistent with the later Case 135 product witness, where time eligibility, bus-idle gating, selective queueing, execution, and completion/history are separately observable concepts.

### E — revision-bounded semantics matter for retention arguments

If a retention argument depends on a control field such as `PERIODIC_WAKEUP`, then the relevant state is not merely:

```text
field = some value
```

It is better represented as:

```text
(protocol revision, field definition, device state, host action)
```

because a future or earlier standard revision can change:

- field presence;
- encoding;
- reset value;
- write restrictions;
- optionality;
- command ordering;
- maintenance-completion requirements.

The current evidence does not show that those changes occurred between 4.5 and 5.0; it shows why they cannot be assumed absent without the direct texts.

### E — implementation corroboration is not normative provenance

`mmc-utils` is useful because it operationalizes a version map used by real software. But its role in the evidence hierarchy is narrower:

```text
JEDEC revision history
    -> feature-lineage evidence

mmc-utils B45 decoder
    -> implementation corroboration

later B50 clause text
    -> directly inspected behavioral semantics
```

A robust chronology uses these sources together without promoting one into the role of another.

## Functional analogy

### F — e.MMC 4.5 RTC support and Micron's later self-refresh share a maintenance-time role, not a proven implementation lineage

At the level of function, both the e.MMC 4.5 announcement and the later Armadillo/Micron path support the idea that temporal information can influence internal storage maintenance.

The controlled analogy is:

```text
e.MMC 4.5 standardized temporal input
    ↕ functional analogy
later Micron product uses host-supplied time in refresh eligibility
```

The unsupported stronger claim is:

```text
e.MMC 4.5 RTC feature
    == Micron Self Refresh algorithm
```

No inspected source establishes that identity.

### F — `PERIODIC_WAKEUP` and product self-refresh both create maintenance opportunities, but authority differs

The later standard path describes host/device scheduling around periodic wakeup and background operations. The product path describes an internal elapsed-time and bus-idleness policy tied to Micron self refresh.

Both can be described functionally as opening a maintenance opportunity. But their authorities differ:

```text
standard wakeup contract:
    host participates in creating the opportunity

product self-refresh policy:
    controller makes a vendor-defined internal eligibility/execution decision
```

The analogy is useful only if those loci remain explicit.

### F — relation to DRAM refresh remains analogy only

The existence of a periodic wakeup or RTC-driven NAND-maintenance path does not make the mechanism equivalent to DRAM refresh.

DRAM refresh usually concerns repeated restoration of volatile charge on a much shorter cadence and with a very different externally visible contract. Case 135 remains a managed-Flash maintenance case.

## Philosophical interpretation

### P — retained data may depend on retained or reconstructable time relation

The technical significance of the earlier e.MMC lineage is not that a clock is philosophically special. It is that the survival of payload can depend on a second-order relation used to decide whether intervention is due.

A minimal abstraction is:

```text
payload
    + temporal evidence
    + maintenance policy
    + maintenance opportunity
    -> future renewal decision
```

The temporal evidence can be host-supplied rather than fully autonomous inside the device. This shows that a retention system may preserve continuity by **reconstituting maintenance-relevant state** after power/lifecycle boundaries rather than by retaining every element of that state continuously.

### P — retaining full history is stronger than retaining enough state to recover a safe decision

The standard lineage is compatible with a broader project distinction:

```text
retain complete event history
    !=
retain / reconstruct enough temporal relation
       to make the next maintenance decision
```

Case 135 should not infer which internal representation a particular device uses. The point is only that the interface exposes a compact temporal relation that can stand in for richer elapsed history in a maintenance policy.

## Cross-case comparison

### Case 111 — enterprise SSD extended-shutdown maintenance

Case 111 includes mechanisms that can re-observe current media state after power-up rather than retaining a complete age history. Case 135 adds the complementary pattern in which a host can supply temporal evidence that helps reconstruct maintenance-relevant age/time state.

Controlled comparison:

```text
Case 111:
    re-observe media condition after power-up

Case 135:
    re-supply / update temporal evidence after lifecycle boundaries

both:
    complete historical event log is not always required
```

This is functional comparison, not shared implementation ancestry.

### Case 43 — AVATAR DRAM refresh policy metadata

Case 43 shows that retention policy state itself can require protection. Case 135 shows a different problem: maintenance decisions may depend on **time-related evidence whose validity and revision-bounded semantics must be maintained**.

The shared abstraction is second-order maintenance state; the substrates and mechanisms are different.

### Case 03 — DRAM refresh control

Case 03 separates cadence locus from coverage-state locus. Case 135 similarly separates:

- where time evidence comes from;
- where wakeup policy is represented;
- where maintenance execution is decided; and
- where payload renewal occurs.

Again, this is an engineering analogy, not a historical genealogy.

## Chronology correction for Case 135

The repository should now use the following bounded chronology:

```text
2010 / e.MMC 4.41
    generic Background Operations already exist
        ↓
15 Jun 2011 / e.MMC 4.5
    RTC-related host/device reliability capability publicly announced
    later JEDEC revision history assigns RTC to 4.41 -> 4.5
    mmc-utils corroborates PERIODIC_WAKEUP[131] as B45-generation
        ↓
Jun 2012 / e.MMC 4.51
    intervening revision / clarification epoch
        ↓
Sep 2013 / e.MMC 5.0
    directly inspected repository floor for detailed
    SET_TIME / RTC / PERIODIC_WAKEUP semantics
        ↓
2021+ bounded Micron/Armadillo product path
    vendor-specific self-refresh eligibility / execution / telemetry
```

The chronology deliberately mixes no more than the sources justify. In particular:

```text
feature present by 4.5
    !=
all later normative semantics proven identical in 4.5
```

## Explicit non-claims

This pass does **not** claim any of the following:

1. that e.MMC 4.5 invented the general idea of time-triggered Flash maintenance;
2. that e.MMC 4.5 invented Flash refresh;
3. that e.MMC 4.5 introduced Micron's branded `Self Refresh` implementation;
4. that every e.MMC 4.5 device implemented the RTC feature in the same physical way;
5. that a host-supplied RTC necessarily implies a battery-backed clock inside the eMMC;
6. that `PERIODIC_WAKEUP[131]` was first invented in B45 solely because `mmc-utils` labels it B45;
7. that `mmc-utils` is a normative JEDEC source;
8. that every B45 `PERIODIC_WAKEUP` encoding is proven identical to B50/B51;
9. that `SET_TIME (CMD49)` wording is proven byte-for-byte identical in B45, B451, B50, and B51;
10. that B45 imposed the exact B50 completion-before-power-down sequence without direct B45 clause inspection;
11. that e.MMC 4.51 made no RTC-related normative clarification;
12. that Arasan's statement of retained 4.5 functionality substitutes for JESD84-B451 text;
13. that a standards capability proves any named shipping component enabled or used it;
14. that RTC information by itself refreshes NAND charge;
15. that periodic wakeup guarantees maintenance completion in every device state;
16. that Background Operations are identical to vendor self refresh;
17. that one wakeup interval is a NAND retention limit;
18. that the host has full visibility into the controller's internal age model;
19. that a time value records complete payload or block history;
20. that the standard defines Micron's ECC threshold, queue, relocation geometry, or internal refresh algorithm;
21. that e.MMC time-maintenance support is technically identical to DRAM refresh;
22. that a later standard's historical annex proves all intermediate errata and implementations were behaviorally identical;
23. that feature-introduction date, publication date, product-support date, and customer-deployment date are the same event;
24. that the 2011 announcement alone proves the exact first silicon implementation of the feature.

## Remaining debt

The broad chronology debt is now closed. The remaining work is narrower and more source-specific:

1. obtain a directly inspectable copy of **JESD84-B45** and locate the exact RTC / `SET_TIME` / `PERIODIC_WAKEUP` clauses;
2. obtain a directly inspectable copy of **JESD84-B451** and diff those clauses against B45 and B50;
3. determine whether `PERIODIC_WAKEUP`'s encoding, reset/default behavior, and maintenance-completion language changed across 4.5 -> 4.51 -> 5.0;
4. find a dated **named e.MMC 4.5 shipping-device datasheet** that exposes the RTC / periodic-wakeup feature rather than merely claiming version compliance;
5. if useful, trace host-side Linux or bootloader support for `SET_TIME` / `PERIODIC_WAKEUP` to a dated implementation, while keeping software-adoption chronology separate from standard origin;
6. keep the vendor-specific Micron Self Refresh algorithm separate unless a primary vendor source explicitly maps it to the standardized RTC / wakeup contract.

## Status decision

**No maturity promotion.**

The slice materially strengthens prior-art chronology:

```text
e.MMC 5.0 direct clause floor
    -> remains useful

but

e.MMC 5.0 feature-origin claim
    -> rejected

RTC-related reliability lineage
    -> now grounded to e.MMC 4.5 / June 2011

PERIODIC_WAKEUP B45 association
    -> strongly corroborated by implementation tooling

exact B45/B451 normative semantics
    -> still open
```

That is enough to close the broad pre-5.0 chronology question while preserving the correct residual uncertainty.