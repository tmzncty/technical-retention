# Evidence 119 — Samsung 2014 DDR4 PPR cross-vendor resource and transition boundary

## Purpose

This record deepens [`../cases/119-ddr4-post-package-repair-row-remapping.md`](../cases/119-ddr4-post-package-repair-row-remapping.md) around an explicit remaining debt from the Micron slice:

> Does shared DDR4 `PPR` / `sPPR` vocabulary imply the same repair-resource geometry, transition preconditions, persistence lifetime, and payload-retention envelope across vendors?

The bounded answer is **no**. Samsung's September/October 2014 DDR4 device-operation document exposes a bank-group-scoped PPR contract with permanent electrical-fuse repair, volatile soft repair, a one-repair-element-per-bank-group envelope, and a requirement to clear outstanding soft repairs before hard repair. The existing Micron evidence documents a different manufacturer envelope: at least one repair row per **bank**, and an explicit Micron exception to the soft-clear-before-hard restriction.

This record therefore closes one **cross-vendor interface/operation-semantics** debt. It does **not** establish a complete JEDEC adoption genealogy or the hidden physical spare/fuse topology of every Samsung or Micron product.

## Evidence classification

- **H/P** — historical / manufacturer-primary technical record.
- **E** — engineering reconstruction constrained by those records.
- **A** — bounded functional comparison only.
- **I** — project-level philosophical interpretation, not source vocabulary.
- **X** — explicitly rejected stronger inference.

---

## Source A — Samsung DDR4 Device Operation, Rev. 1.1, October 2014

### Identity and provenance

Samsung Electronics, **DDR4 SDRAM Specification — Device Operation & Timing Diagram**, Rev. 1.1, October 2014.

The inspected page-preserving public extraction shows:

- cover: `Rev. 1.1, Oct.2014`, Samsung Electronics copyright 2014;
- revision history: Rev. 1.0 `First Spec release` in September 2014, followed by Rev. 1.1 in October 2014;
- Section 2.32: `Post Package Repair (PPR)`;
- Section 2.33: `Soft Post Package Repair (sPPR)`.

Current public extraction:

<https://studylib.net/doc/28016964/ddr4-device-operations-rev11-oct-14-0>

A historically used Samsung download path is also independently linked in later technical material:

<https://download.semiconductor.samsung.com/resources/device-operation-timing-diagram/DDR4_Device_Operations_Rev11_Oct_14-0.pdf>

The latter endpoint timed out in this research environment, so this record does **not** pretend to have performed fresh facsimile-level inspection of the current Samsung-hosted PDF. Technical claims below are limited to the Samsung-authored text preserved in the page extraction; the provenance limitation is explicit.

---

## Historical record

### 1. PPR capability is density- and product-qualified, not inferred from the name alone

Samsung's Section 2.32 states that DDR4 fail-row address repair is an **optional feature for 4Gb** and **required for 8Gb and above**, while actual support is identified through the manufacturer datasheet and module SPD.

Safe historical use:

> a DDR4 generation label does not by itself prove that every concrete ordering/configuration exposes the same PPR capability.

This is an interface/capability statement in Samsung's 2014 operation document, not a complete JEDEC ballot history.

### 2. The documented hard-PPR mechanism is permanent electrical-fuse programming

Samsung describes fail-row repair as electrical programming of an **Electrical-fuse** scheme and states that the electrical fuse cannot be switched back to the unfused state once programmed. The same section warns the controller to prevent unintended PPR entry/repair and protects entry with a multi-command guard key.

This supplies a bounded Samsung witness for:

```text
hard repair result
    -> persistent / irreversible repair relation

but

persistent result
    != transition can be entered casually or without qualification
```

The document does not justify projecting this exact physical fuse implementation onto Micron, SK hynix, or every later DDR generation.

### 3. Samsung's exposed hard-PPR resource envelope is one row per bank group

Section 2.32 states that PPR can correct **one row per Bank Group**.

Section 2.33 gives the same exposed count for the soft/hard comparison table: soft repair `Only 1 per BG`, hard repair `1 per BG`.

The safe claim is about the **documented repair-resource contract**. It is not a transistor-level proof that exactly one physical spare wordline or one unique fuse object exists per bank group in every implementation.

### 4. Soft repair and hard repair have different persistence horizons

Samsung's Section 2.33 describes soft PPR as quick but temporary and contrasts it with the longer permanent hard repair. Its comparison table states:

- soft repair remains while `VDD` is within the operating range;
- soft repair is erased when power is removed or the device is reset;
- hard repair is nonvolatile/permanent after the repair cycle.

The text later repeats that loss of power or `RESET` returns the soft repair to the unrepaired state.

Therefore the same address-repair function can have different retained-state horizons:

```text
sPPR relation
    -> powered/reset-bounded

hPPR relation
    -> retained beyond that powered session
```

This does not make the DRAM payload itself nonvolatile.

### 5. Outstanding soft repairs are a transition precondition for Samsung's documented hard-PPR path

The soft/hard comparison table states that **outstanding soft repairs must be cleared before a hard repair**, with clearing by either power-down/power-up or reset and reinitialization. The prose likewise says sPPR must be disabled and cleared before entering PPR mode.

This means that repair state is not merely a passive mapping result. Existing temporary repair state can constrain which later transition is admissible.

Safe engineering shorthand:

```text
existing temporary repair state
    -> can constrain next permanent-repair transition
```

That is not a universal DDR4 rule across every vendor implementation; Micron supplies the counterexample below.

### 6. Repair-resource exhaustion is visible in the Samsung operation contract

Samsung states that when the hard-PPR resources for a bank group are used up, that bank group has no available resources for soft PPR; if a repair sequence is issued with no resource available, the DRAM ignores the programming sequence.

This independently confirms the Micron slice's general methodological boundary:

```text
PPR feature present
    != repair capacity remains

repair sequence issued
    != repair mapping necessarily changed
```

But the **scope** of the capacity differs between the Samsung operation document and the later Micron product documentation.

### 7. Hard-PPR sequence choice changes the data-retention envelope

Samsung documents two hard-PPR command sequences:

- the `WRA` path allows refresh and says data retention is ensured **except for the bank containing the repaired row**;
- the `WR` path does not allow refresh in the sequence and therefore does **not** ensure data retention for the target DRAM.

The bounded conclusion is not that PPR always destroys data or always preserves it. It is:

> **persistent repair semantics and payload-retention semantics are separate dimensions even inside one vendor operation contract.**

The first sequence is also not evidence that the target bank's pre-repair payload is preserved; Samsung explicitly excludes that bank from the stated guarantee.

---

## Cross-vendor comparison — Samsung vs Micron

The Micron side is **reused**, not re-researched here; see [`119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md`](119-micron-ddr4-ppr-payload-retention-resource-exhaustion-deepening.md).

That Micron evidence establishes for the bounded product families that:

- JEDEC's minimum support is described as one repair row per bank group;
- Micron exposes at least one repair row per **bank**, exceeding that minimum;
- Micron explicitly says existing sPPR repair addresses do **not** need to be cleared before entering hPPR mode;
- when a bank's hPPR resource is exhausted, that bank should be assumed to have no sPPR resource available;
- an attempted repair with no available resource is ignored.

Samsung's 2014 operation document, by contrast, presents the one-row-per-bank-group envelope and requires outstanding soft repair to be cleared before hard repair.

Therefore:

```text
shared PPR terminology
    != identical repair-resource geometry

shared sPPR/hPPR lifetime distinction
    != identical transition preconditions

shared "repair row" function
    != identical hidden physical implementation
```

This is a **functional and interface-level cross-vendor comparison**. It does not establish direct Samsung↔Micron design influence, shared silicon, or genealogy.

---

## Engineering reconstruction

### A. Repair-resource geometry is part of the retention contract

A repair mechanism does more than preserve a current logical row relation. It also exposes a finite set of future substitutions. Whether that capacity is accounted per bank group or per bank changes the number and locality of future defects that can still be repaired.

Thus:

> **future maintainability depends on retained resource-allocation state as well as current repair mappings.**

This is project terminology, not Samsung's or Micron's historical vocabulary.

### B. Standard/minimum behavior and product behavior must remain separate

Micron explicitly describes its per-bank resource count as exceeding a one-per-bank-group minimum. Samsung's 2014 operation document presents the one-per-bank-group contract. The safe comparison is therefore:

```text
minimum / generic operation envelope
    != vendor product resource envelope
```

It would be a mistake to use either vendor document to infer a universal internal spare-row topology for all DDR4.

### C. Temporary repair state can be a prerequisite state, not just a result state

Samsung's clear-before-hard rule and Micron's explicit exemption show that the existing soft-repair relation can matter to the legality/meaning of the next hard-repair transition, but that this constraint is implementation/vendor specific.

Therefore:

> **repair-state lifetime != repair-transition policy.**

Knowing that sPPR is volatile and hPPR persistent is not enough to reconstruct the transition rules between them.

### D. Interface-visible capacity is not a physical-topology proof

`one row per BG` and `at least one row per bank` are operation/resource guarantees. They do not by themselves reveal:

- exact count of physical spare wordlines;
- whether soft and hard repair share one physical spare pool in every design;
- fuse/antifuse layout;
- decoder implementation;
- address scrambling beneath the visible row address;
- manufacturing-time redundancy that may exist separately from post-package repair.

Those questions remain semiconductor-device archaeology, not safe deductions from an operation table.

---

## Functional analogy only

Case 14 SCSI defect reassignment and Case 04 mapped Flash remain useful because they also separate stable designation from replaceable physical embodiment and expose finite hidden maintenance capacity.

The analogy stops at that relation. DDR4 PPR has volatile payload charge, bank/bank-group organization, repair command sequences, and vendor-specific spare/fuse state. Disk defect reassignment and Flash mapping operate through different media, controllers, failure modes, and cleanup geometry.

---

## Philosophical / media-theoretical interpretation

Project interpretation only:

> **The ability of a technical identity to survive future defects can depend on retained possibility, not only retained current state.**

A repaired row address may be callable now while the device's future ability to keep that callability through another defect has already changed because a finite repair resource was consumed. Samsung/Micron differences add an important limit: even when systems share the same public operation name, the topology of that retained possibility can differ.

This is not historical Samsung/Micron terminology and not evidence for a universal ontology of memory.

---

## Explicit stop conditions

This deepening does **not** establish:

1. the exact JEDEC ballot/revision in which hPPR or sPPR first entered DDR4;
2. that Samsung invented PPR, sPPR, electrical-fuse repair, or spare-row substitution;
3. that every Samsung DDR4 SKU implements exactly one physical spare row per bank group;
4. that Samsung's documented electrical-fuse mechanism is Micron's, SK hynix's, or a universal DDR4 implementation;
5. that Micron's per-bank resource count is universal across all Micron generations/densities;
6. that `one repair per BG` reveals the exact number of hidden spare wordlines/fuses;
7. that the WRA hard-PPR sequence preserves the payload of the bank containing the repaired row;
8. that every hard-PPR sequence destroys target data;
9. that an issued repair command proves a mapping transition succeeded when resources are exhausted;
10. that retiring/remapping a row sanitizes or forensically erases the original physical row;
11. direct Samsung→Micron, Micron→Samsung, or JEDEC→vendor genealogy beyond the bounded documentary relationships explicitly stated by the sources.

---

## Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Post Package Repair` found no dedicated PPR technical-history module to reuse. Broader semiconductor-redundancy genealogy, decoder/fuse implementation history, and exact JEDEC ballot chronology still belong primarily there if developed.

---

## Result / status

This slice partially closes Case 119's cross-vendor debt:

```text
Samsung 2014 operation contract:
    one repair element per bank group
    + volatile sPPR / permanent hPPR
    + soft-clear-before-hard transition rule
    + exhausted resource -> programming ignored

Micron bounded product contract:
    at least one repair row per bank
    + volatile sPPR / permanent hPPR
    + no requirement to clear existing sPPR before hPPR
    + exhausted resource -> programming ignored
```

The resulting bounded claims are:

> **same PPR vocabulary != same repair-resource geometry**

> **same repair-lifetime classes != same transition preconditions**

> **interface-visible repair capacity != demonstrated physical spare topology**

Remaining work is narrower: SK hynix comparison, named Samsung product-level confirmation beyond the generic/vendor operation document, exact JEDEC adoption chronology, and physical implementation/fault-injection evidence.