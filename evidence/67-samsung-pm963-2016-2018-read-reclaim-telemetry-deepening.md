# Case 67 deepening — Samsung PM963 named-product read-reclaim telemetry, 2016–2018

## Status and purpose

**Evidence deepening for grounded Case 67.**

This note closes one narrow part of Case 67's explicit next-work gap: a **named shipping SSD for which the manufacturer exposed a read-reclaim maintenance counter through first-party tooling**.

The witness is Samsung's PM963 NVMe data-center SSD. Samsung later states that the PM963 was launched in 2016. Samsung's October 2018 *DC Toolkit 2.1 User Guide* lists PM963 among supported SSDs and shows an Extended SMART reference output for a device identified as `SAMSUNGNVMeSSDPM963`, firmware `CXV83M1Q`, containing the field `Lifetime read Reclaim count`.

This is deliberately **not** evidence that PM963 implements the specific 2017-priority SK hynix adaptive-threshold algorithm grounded in Case 67. It does not reveal Samsung's internal trigger, threshold, victim geometry, copy path, counter persistence implementation, mapping handoff, or exact meaning of one counted reclaim event.

The defensible result is narrower:

> **By October 2018, a first-party Samsung diagnostic guide publicly exposed a `Lifetime read Reclaim count` for a named PM963 SSD example, grounding read-reclaim as a product-visible maintenance/telemetry category rather than only a patent or research proposal.**

---

## Source ladder

### 1. Samsung DC Toolkit 2.1 User Guide — October 2018

**Type:** `H/P` manufacturer-primary public technical documentation.

The guide identifies itself as *Samsung DC Toolkit 2.1 User Guide*, Revision 1.0. Its revision history says `Initial Release — October, 2018`.

Its hardware requirements list includes `Samsung SSD PM963`. The PM963 support table separately shows SMART and health-monitor support across the documented operating-system/driver combinations, subject to the table's limitations.

The NVMe Get Log Pages section defines `--smart-extended` as the option that extracts extended SMART values. The reference-output page then shows:

- `Model Name: SAMSUNGNVMeSSDPM963`;
- firmware `CXV83M1Q`;
- a vendor extended-log field named `Lifetime read Reclaim count`;
- neighboring lifetime/health fields including user reads, NAND writes, retired-block count, reserve-block count, UECC count, reallocated-sector count, power-on hours, and clean/unclean shutdown counts.

The displayed `Lifetime read Reclaim count` value is zero in this reference output. That zero is an **observed example value**, not evidence that the operation is unsupported or never occurs. The evidential point is the manufacturer-defined field and its association with the named PM963 reference output.

The command-output screenshot itself carries a 2017 Samsung copyright line. That embedded program-output copyright is **not used to backdate the manual or the public telemetry floor**. The document's revision history supplies the defensible October-2018 publication anchor for this note.

### 2. Samsung DC Toolkit support page — current continuity witness

**Type:** `P/current vendor documentation`, not a 2018 historical anchor by itself.

Samsung's current Tools & Software page states that DC Toolkit 2.1 is designed to work with several Samsung SSD products including `PM963 non-customized`, and links the same Version 2.1 user guide.

This current page is useful to establish provenance and continued availability of the vendor document. It must not be treated as evidence that every wording on today's support page existed in 2018.

### 3. Samsung PM963 product material

**Type:** manufacturer product documentation / later first-party retrospective.

Samsung's PM963 brochure identifies the product as an NVMe SSD engineered for data-center workloads, especially read-intensive environments, using Samsung TLC V-NAND and a Samsung NVMe controller. The brochure also says Samsung SSD Toolkit can monitor essential PM963 health status.

A later Samsung Semiconductor technical article says the PM963 was **launched in 2016** and describes it as a data-center NVMe SSD based on TLC Vertical NAND.

The 2016 launch statement is therefore a manufacturer retrospective floor for product existence. It does **not** prove that the exact `Lifetime read Reclaim count` field, the 2018 toolkit version, or the shown firmware revision was present on launch day.

---

## Historical record

### A named product exposes a read-reclaim count

The strongest bounded fact is unusually concrete. The 2018 guide does not merely say that a controller *could* perform read reclaim. Its PM963 Extended SMART example places a `Lifetime read Reclaim count` beside other device-health counters.

This changes the evidence class available to Case 67:

- the SK hynix patent remains a manufacturer-primary **design disclosure** for one adaptive read-disturb policy;
- the earlier Samsung patents remain prior art for read-reclaim / ECC-margin-triggered relocation;
- the PM963 guide adds a **named product + firmware example + vendor diagnostic interface** in which read reclaim is a maintained/observable device category.

That does not make the three artifacts one implementation genealogy.

### Product launch and telemetry-publication dates are different

Samsung's later article says PM963 launched in 2016. The inspected DC Toolkit 2.1 guide is initial-release October 2018.

Therefore:

> `PM963 launched in 2016 != read-reclaim telemetry publicly documented in 2016`.

The October-2018 manual is the evidence floor used here for the named `Lifetime read Reclaim count` field. An older toolkit release may exist, but this slice does not infer an earlier counter date from product age.

---

## Engineering reconstruction

### Lifetime reclaim count is not the same state as a read-count proxy

Case 67's SK hynix design retains a **read-count proxy** that helps decide when to test for disturb and possibly reclaim. Samsung's PM963 reference output instead exposes a **lifetime read-reclaim count**.

Even if both participate in read-disturb maintenance, they occupy different places in the control chain:

```text
workload / physical stress evidence
        -> maintenance trigger / qualification
        -> reclaim decision
        -> reclaim operation
        -> cumulative product telemetry about reclaim
```

The PM963 field is evidence about a counted maintenance outcome/category. It does not expose the hidden trigger state that caused an event.

Thus:

> **`lifetime read-reclaim count != per-block read-count proxy`.**

### Maintenance telemetry is not maintenance policy

A cumulative count can tell an operator that the device has a category of internal work worth counting without revealing:

- how many reads trigger inspection;
- whether ECC margin, raw BER, read retry, temperature, age, or another signal is consulted;
- whether thresholds are fixed or adaptive;
- which physical pages/blocks/wordlines are selected;
- whether data are corrected before movement;
- how currentness/mapping is made crash-safe;
- how an interrupted reclaim is recovered.

Therefore:

> **`reclaim telemetry != reclaim policy != reclaim implementation`.**

The PM963 witness partially closes a product-deployment gap only at the product-visible telemetry/vocabulary level.

### A lifetime counter is intentionally lossy history

The field name presents a cumulative `Lifetime ... count`; it does not enumerate events. The inspected documentation supplies no timestamp, LBA, block ID, victim/aggressor relation, trigger reason, or before/after error margin for each counted event.

So:

> **`cumulative maintenance count != complete maintenance history`.**

This is a useful companion to Case 55's distinction between cumulative SSD health counters and payload/event history, while remaining vendor-specific rather than being silently normalized into the base NVMe SMART/Health contract.

### Product-visible maintenance evidence can be downstream of hidden physical work

The host can observe a number even though the maintenance action it summarizes is controller-internal. The retained relation is therefore layered:

```text
NAND physical condition
    != controller trigger state
    != reclaim execution/progress state
    != cumulative reclaim telemetry
    != user payload
```

The PM963 documentation does not establish that all of these states have the same persistence horizon. In particular, the word `Lifetime` is not enough to prove the exact reset/power-cycle/firmware-update persistence rules of the counter; those remain open until a stronger contract or experiment is found.

---

## Cross-case boundaries

### Versus canonical Case 67 — SK hynix adaptive reclaim

The PM963 evidence strengthens the **named-product boundary**, not the exact SK hynix algorithm.

It is now defensible to say that a shipping Samsung PM963 family was represented in first-party tooling by 2018 with read-reclaim lifetime telemetry. It is not defensible to say the PM963 uses:

- the SK hynix grouped read-counter scheme;
- its adaptive threshold table;
- its 3-D neighborhood sampling rule;
- its power-off counter-reset strategy.

Shared `read reclaim` vocabulary is a functional/industry-class relation, not proof of direct implementation identity or genealogy.

### Versus Case 55 — NVMe SMART / Health telemetry

Case 55 grounds standardized NVMe health/endurance fields and the wider distinction between cumulative device history and user payload history. The PM963 `Lifetime read Reclaim count` appears in **Samsung Extended SMART** tooling. It should therefore be treated as vendor-specific maintenance telemetry unless a normative NVMe source independently assigns the same field/semantics.

> `vendor extended SMART field != base NVMe standardized SMART field`.

### Versus Cases 52 and 65

Case 52 grounds NAND read-disturb physics and research/controller mitigation paths. Case 65 grounds 3-D NAND early-retention loss and age-aware reading. PM963's TLC V-NAND/read-intensive product context does not prove which physical mechanism triggered any given reclaim count and does not prove ReMAR-like age-aware read policy.

### Versus Cases 44 and 47

A read-reclaim action is maintenance intended to preserve usable data by moving/renewing an embodiment. Neither the counter nor the product documentation establishes secure erasure of the retired physical location.

> `read reclaim counted != old embodiment sanitized`.

---

## Prior-art and chronology boundary

Case 67 already uses Samsung patent families with 2009 and 2013 priority to reject any claim that the 2017-priority SK hynix patent invented read reclaim.

PM963 adds a different kind of evidence: a named data-center product launched in 2016 and a manufacturer toolkit that, by October 2018, exposes read-reclaim telemetry for a PM963 reference output.

This evidence should **not** be used to claim:

- Samsung invented read reclaim;
- PM963 was the first SSD with read reclaim;
- the PM963 read-reclaim mechanism was public in 2016;
- the SK hynix patent copied Samsung;
- Samsung's and SK hynix's controller state machines are identical.

The safe historical statement is only that the term/function had both earlier patent prior art and, by the inspected 2018 documentation, a named-product telemetry witness.

---

## Related-repository boundary

A fresh search of `tmzncty/computing-archaeology` for `PM963 read reclaim` found no dedicated PM963/read-reclaim study to reuse.

If future work becomes a broader history of Samsung enterprise SSD firmware, V-NAND generations, vendor-specific SMART logs, or read-reclaim algorithm genealogy, that engineering history belongs primarily in `computing-archaeology`. Case 67 should retain the narrower relation among physical stress, hidden maintenance policy, re-embodiment, and retained maintenance evidence.

---

## Philosophical interpretation — bounded

This product witness supports one modest extension of the repository's maintenance vocabulary:

> **A maintenance system may retain not only the state needed to decide or perform repair, but also a compressed trace that repair occurred.**

That trace can outlive the immediate operation while remaining far poorer than an event history and far smaller than the payload whose preservation it summarizes. This is an engineering fact about telemetry and maintenance evidence. It is not evidence that the SSD has memory in a psychological sense, and it is not automatically Stieglerian tertiary retention.

---

## Findings contributed by this deepening

1. PM963 product existence and read-reclaim telemetry have different date floors: 2016 launch versus inspected October-2018 telemetry documentation.
2. A named Samsung PM963 reference output publicly exposes `Lifetime read Reclaim count` through first-party tooling.
3. Named-product telemetry does not prove the exact hidden reclaim trigger or algorithm.
4. A cumulative read-reclaim count is not the per-block/read-group stress counter grounded in the SK hynix design.
5. Maintenance-outcome telemetry is not a complete maintenance-event history.
6. An example counter value of zero is not evidence that the counter/feature category is unsupported.
7. Samsung Extended SMART is not automatically identical to the normative NVMe SMART/Health log.
8. Shared `read reclaim` vocabulary across Samsung product tooling and SK hynix/Samsung patents does not establish one controller genealogy.
9. Reclaim maintenance still does not imply sanitization of retired NAND embodiments.

---

## Sources

1. Samsung Electronics, **Samsung DC Toolkit 2.1 User Guide**, Revision 1.0, initial release October 2018, especially pp. 3, 8, 19, 41, and 43. Samsung Semiconductor: <https://semiconductor.samsung.com/resources/user-manual/Samsung_DCToolkit_V2.1_User_Guide.pdf>
2. Samsung Semiconductor, **Tools & Software — Samsung DC Toolkit Version 2.1**, current support/provenance page, accessed 11 September 2026: <https://semiconductor.samsung.com/consumer-storage/support/tools/>
3. Samsung Electronics, **Samsung SSD PM963 — An NVMe SSD engineered for data center environments**, product brochure, especially p. 2: <https://image.semiconductor.samsung.com/content/samsung/p6/semiconductor/newsroom/tech-blog/samsung-ssd-pm963-brochure/Samsung_PM963-1.pdf>
4. Samsung Semiconductor, **“Faster flash is taking over data centers (Part 2)”**, later first-party retrospective stating that PM963 launched in 2016: <https://semiconductor.samsung.com/news-events/tech-blog/faster-flash-is-taking-over-data-centers-part-2/>
5. Canonical Case 67 earlier sources, including SK hynix `US20190066809A1` and Samsung `US20100235713A1` / `US20140237165A1`, remain the mechanism/prior-art sources; this deepening does not replace them.
