# Evidence 119 — SK hynix 2015 PPR resource-state reconstruction and exhaustion boundary

## Purpose

This note deepens [`../cases/119-ddr4-post-package-repair-row-remapping.md`](../cases/119-ddr4-post-package-repair-row-remapping.md) at one bounded remaining debt after the Micron and Samsung passes:

> What does a third DDR4-era vendor primary source show about how Post-Package Repair resource availability is represented, recovered after power-up, and prevented from being over-consumed?

The source is an SK hynix patent family with Korean priority on **26 January 2015**, US filing on **28 April 2015**, publication as **US20160217873A1** on **28 July 2016**, and grant as **US9666308B2** on **30 May 2017**. The disclosure describes an electrical-fuse PPR implementation in which failed-address information is retained in an Array Rupture Electrical-fuse (`ARE`) array, the fuse array is scanned during boot-up to recover resource-use information, and a masking path prevents another irreversible rupture operation when no unused repair fuse remains.

This is a **manufacturer-primary patent embodiment**, not a named shipping-product datasheet and not a universal SK hynix DDR4 contract. It therefore closes a bounded implementation/prior-art seam while leaving product-level capability counts, JEDEC conformance, and exact shipping topology open.

## Evidence classification

- **H/P — historical / manufacturer-primary patent record.**
- **E — engineering reconstruction constrained by the patent disclosure.**
- **A — bounded functional comparison with the already-grounded Samsung and Micron records.**
- **I — project interpretation only.**
- **X — explicitly rejected stronger inference.**

---

## Primary source

SK hynix Inc., Young Kyu Noh, **“Post package repair device.”**

- Korean priority: **2015-01-26**.
- US application: **US14/698,617**, filed **2015-04-28**.
- US publication: **US20160217873A1**, **2016-07-28**.
- US grant: **US9666308B2**, **2017-05-30**.
- Public patent record: <https://patents.google.com/patent/US9666308B2/en>.
- Public application record: <https://patents.google.com/patent/US20160217873A1/en>.

The patent is useful here because it exposes an implementation-level relation that product operation tables often hide: **persistent repair-fuse contents, boot-time scanning of those contents, derived remaining-resource state, and gating of the next irreversible repair transition**.

The patent is not used as evidence that every SK hynix DDR4 part shipped this exact circuit or that the claimed bank/fuse topology is identical to JEDEC's abstract minimum resource model.

---

## Historical record

### H1. The disclosure stores failed-address information in an electrical-fuse array

The patent describes a PPR device containing an **Array Rupture Electrical-fuse (`ARE`) array**. Each fuse set can be programmed by electrical rupture, and the disclosure says the array permanently stores failure information for failed parts. It further states that the stored fuse data includes row and column repair information.

The bounded historical claim is therefore:

```text
repair decision / failed-address information
    -> irreversible electrical-fuse state
    -> available again after later power-up
```

This is a patent embodiment, not a proof that all SK hynix PPR generations or all DDR4 vendors use the same fuse structure.

### H2. Power-up does not merely restore payload operation; it reconstructs repair-resource knowledge

The patent states that, after power-up, the device performs a boot-up operation that reads the ARE array's previously stored fuse data. The boot-up controller scans fuse sets used for PPR and sends fuse-resource information to a resource-detection unit.

The disclosure therefore distinguishes at least two layers:

1. **persistent fuse/repair information** stored in the ARE array;
2. **runtime resource-availability state** reconstructed by scanning that persistent information during boot-up.

The patent also exposes channel, bank-group, left/right-bank, mat, and fuse-address selectors used when locating whether an unused fuse exists for the relevant region.

This is direct manufacturer-primary evidence that one PPR implementation can recover maintenance admissibility from more durable repair history rather than requiring one separately persistent `resource available` flag for every runtime decision.

### H3. Repair fuses may be shared across a bank grouping while availability is still checked per bank

The patent's detailed description says that **two banks are shared by one group during the test mode so that fuse lines can be shared**, while fuses can still be controlled per bank. The claims likewise state that two banks may be classified into one bank group to share fuse lines and that the resource detector can distinguish per-channel, per-bank-group, per-left/right-bank, and per-mat regions.

Safe historical use:

> the disclosed repair-resource topology is not simply `one completely independent repair object per bank`.

But this does **not** license the stronger claim that the patent's `bank group` is a complete description of every shipping SK hynix DDR4 device's physical spare-row topology or that it equals Samsung's or Micron's exposed product resource count.

### H4. Resource exhaustion changes whether an irreversible rupture transition is allowed to occur

The patent's central control path is a **resource detection unit + masking controller + rupture controller**. It says that when no unused fuse is present, the masking signal prevents repeated execution of the rupture operation. The claims repeat that the masking controller blocks rupture when no unused fuse remains.

Therefore the primary record supports:

```text
PPR mode entered / target bank active
    + no unused repair fuse
    -> irreversible rupture operation masked
```

This independently reinforces an important boundary already visible in Micron and Samsung documentation:

> **requesting or sequencing a repair is not the same fact as successfully consuming a new repair resource.**

### H5. The runtime resource signal is derived from retained fuse state, not identical to it

The patent says the boot-up controller scans the fuse array and outputs fuse-resource information; the resource-detection unit stores/compares that information and emits a resource signal indicating whether a fuse is available. The masking controller then combines that resource signal with the active-bank signal to decide whether rupture is allowed.

Thus the disclosed control chain is explicitly staged:

```text
persistent fuse contents
    -> boot-up scan
    -> derived resource-use / availability information
    -> bank-qualified masking decision
    -> rupture allowed or blocked
```

The historical source does not call this a `persistence horizon` model; that language belongs to this repository's reconstruction.

---

## Engineering reconstruction

### E1. Remaining repair capacity can be a reconstructed relation rather than an independently persistent counter

The patent exposes durable fuse state and a boot-time scan that derives which repair resources remain available. The bounded engineering consequence is:

> **remaining repair capacity need not survive power loss as one separately serialized runtime object if it can be recomputed from more persistent repair-allocation state.**

This should not be generalized to every PPR implementation. It is one concrete manufacturer-primary example of `persistent allocation history -> reconstructed maintenance admissibility`.

### E2. Repair history and future repair possibility are coupled

Each irreversible fuse rupture changes both the current repair mapping and the future set of admissible repairs. Once the relevant fuse pool is exhausted, the masking controller prevents another rupture transition.

Therefore:

```text
current repair relation
    + consumed repair-resource state
    -> future repair possibility
```

The retained state is not only `which defective address maps to which replacement`; it also constrains whether another persistent substitution can still be established later.

### E3. Shared resource topology means local repairability cannot be inferred from a global feature bit alone

Because the patent describes shared fuse lines across a bank grouping and per-bank/per-region resource checks, `PPR supported` is weaker than `this target region still has an admissible repair resource`.

The safe engineering distinction is:

```text
feature capability
    != target-specific resource availability
    != successful irreversible programming
```

This sharpens the Case 119 distinction already grounded from Micron product documentation.

### E4. Persistent mapping state and runtime control state can have different lifetimes

The ARE fuse information is described as permanent, while the resource detector and masking decision are runtime logic reconstructed after power-up. That supports a bounded retention-layer distinction:

```text
persistent repair history
    != boot-local derived availability state
    != one repair command's transient control state
```

The case therefore should not treat all `PPR state` as having one persistence horizon.

---

## Cross-vendor functional comparison only

The comparison below is functional and evidence-layered. It does not assert shared silicon, direct influence, or identical compliance implementation.

### Samsung 2014 operation document

[`119-samsung-2014-ddr4-ppr-cross-vendor-resource-transition-deepening.md`](119-samsung-2014-ddr4-ppr-cross-vendor-resource-transition-deepening.md) establishes a vendor operation contract with:

- one repair element per bank group in the exposed contract;
- volatile sPPR versus permanent hPPR;
- a requirement to clear outstanding soft repair before the documented hard-repair path;
- exhausted resource causing a repair programming sequence to be ignored.

### Micron bounded product documentation

[`119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md`](119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md) establishes for the bounded product families:

- at least one repair row per bank, exceeding the stated one-per-bank-group JEDEC minimum;
- no requirement to clear an existing sPPR address before hPPR in the documented Micron path;
- target-bank resource exhaustion changing later sPPR/hPPR availability;
- a repair sequence with no resource being ignored.

### SK hynix 2015 patent embodiment

This note adds an implementation-level manufacturer record in which:

- repair information is stored in an electrical-fuse array;
- fuse-resource information is scanned on boot;
- repair fuses can be shared across a bank grouping while checked per bank/region;
- no-unused-fuse state masks the irreversible rupture operation.

The three source types therefore support a stronger negative control:

```text
shared PPR vocabulary
    != identical exposed capacity
    != identical physical/shared resource topology
    != identical transition preconditions
    != identical representation of remaining repair capacity
```

The SK hynix patent is **not** promoted to a shipping-product contract to force a three-column product comparison where the evidence layers differ.

---

## Prior-art / genealogy boundary

The patent has a **2015-01-26** Korean priority date, after Samsung's September/October 2014 operation-document witness and before the later Micron product documentation used in this case. That establishes documentary ordering only.

It does **not** establish:

- that Samsung influenced SK hynix;
- that SK hynix influenced Micron;
- the first JEDEC ballot introducing PPR;
- the first commercial shipment using the disclosed SK hynix circuit;
- the invention date of electrical-fuse repair or post-package repair in general.

The older 1979 redundant-row patent in the Case 119 grounding remains the broader prior-art floor for address takeover by spare memory rows, not a direct genealogy into this 2015 PPR embodiment.

---

## Philosophical / media-theoretical interpretation

Project interpretation only:

> **A retained technical possibility can be reconstructed from the durable traces of possibilities already consumed.**

In this patent embodiment, the device does not need the same transient resource-control object to persist across power cycles. Durable fuse state can be reread, and from it the device can re-establish which later repair transitions remain possible.

This is not historical SK hynix vocabulary and should not be universalized into a theory of all memory maintenance.

---

## Explicit non-claims

This evidence does **not** establish that:

1. every SK hynix DDR4 product shipped the exact US9666308B2 circuit;
2. the patent's `bank group` is identical in every respect to the JEDEC architectural bank-group abstraction used by every product;
3. two banks sharing fuse lines means there are exactly two physical spare wordlines, or any other exact hidden spare-row count;
4. the patent proves a named shipping DIMM's PPR capacity;
5. SK hynix requires the Samsung clear-sPPR-before-hPPR transition rule;
6. SK hynix follows Micron's no-clear-before-hPPR rule;
7. resource masking proves a repair command is reported to software with any particular status code;
8. irreversible fuse programming preserves the volatile payload of the repaired row;
9. a reconstructed resource signal is itself persistent across power loss;
10. PPR remapping sanitizes or physically erases the retired row;
11. the 2015 priority date is the invention or first-use date of PPR;
12. Samsung, SK hynix, and Micron have a demonstrated direct genealogy from the ordering of these documents.

---

## Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `post package repair` returned no dedicated PPR technical-history module to reuse. Broader semiconductor-redundancy, e-fuse/antifuse, decoder, and JEDEC-standard genealogy should still be developed there rather than duplicated here if that history is pursued.

---

## Result / status

This slice **partially closes the remaining SK hynix comparison debt** for Case 119, but at the patent-implementation level rather than the named-product level.

The new bounded relations are:

> **persistent repair-fuse state != runtime resource-availability state**

> **remaining repair capacity can be reconstructed from retained allocation history**

> **PPR capability != target-specific resource available now**

> **repair request/sequence != irreversible resource consumption**

> **shared public PPR vocabulary != shared internal resource topology**

Still open are a named SK hynix DDR4 product operation/datasheet witness, exact JEDEC hPPR/sPPR adoption chronology, direct product-level payload-retention rules, physical spare-row/fuse topology, and fault-injection validation.