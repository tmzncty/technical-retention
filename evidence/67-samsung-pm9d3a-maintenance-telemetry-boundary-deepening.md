# Evidence 67F — Samsung PM9D3a maintenance telemetry: lifetime read reclaim, patrol read reclaim, and refresh counts

## Status

**`bounded deepening complete`** for the product-interface distinction between three separately exposed maintenance counters in a Samsung PM9D3a datasheet: `Lifetime read Reclaim count`, `Patrol Read Reclaim Count`, and OCP `Refresh Counts`.

This packet deepens Case 67 at the **named-product telemetry / terminology** layer. It does **not** establish the firmware trigger logic behind any counter, counter reset/persistence semantics, one-to-one correspondence between counter increments and physical NAND operations, or identity with the SK hynix mechanism that grounds the canonical case.

---

## Question

Case 67 already had a 2018 Samsung PM963 product witness exposing one Extended SMART field named `Lifetime read Reclaim count`.

That witness left a narrower product-interface question open:

> Does a later named enterprise SSD still present `read reclaim` as one undifferentiated maintenance category, or does its telemetry expose multiple maintenance categories whose names force us to keep reclaim, patrol-associated reclaim, and refresh distinct?

The bounded answer from the inspected PM9D3a material is:

```text
Lifetime read Reclaim count
    !=
Patrol Read Reclaim Count
    !=
Refresh Counts
```

The inequality here is an **interface/semantic distinction only**. It says that the product documentation gives these counters separate fields and names. It does not yet tell us the firmware relation among the underlying operations.

---

## Source custody and evidence grade

### Manufacturer identity / product context

Samsung's current datacenter-SSD pages identify PM9D3a as a Samsung PCIe 5.0 datacenter SSD. Samsung's PM9D3a technical blog describes eighth-generation three-bit V-NAND and explicitly advertises enhanced telemetry for datacenter management.

Manufacturer pages:

- Samsung Semiconductor, datacenter SSD portfolio: <https://semiconductor.samsung.com/ssd/datacenter-ssd/>
- Samsung Semiconductor, **“Samsung's PM9D3a Solid State Drive”**: <https://semiconductor.samsung.com/news-events/tech-blog/samsung-pm9d3a-solid-state-drive/>
- Samsung Semiconductor, **“Empowering AI: Samsung Showcases Next-Gen Memory Solutions at the 2024 OCP Global Summit”**: <https://semiconductor.samsung.com/news-events/tech-blog/empowering-ai-samsung-showcases-next-gen-memory-solutions-at-the-2024-ocp-global-summit/>

These sources are used only for named-product identity, generation context, and public product status. They do not document the three counter fields studied below.

### Detailed datasheet used for the counter fields

The detailed source inspected in this packet is:

- **Samsung SSD PM9D3a Specification (PCIe NVMe U.2), Rev. 1.3, May 2024**, publicly reachable through an xFusion-hosted PDF mirror: <https://www.xfusion.com/wp-content/uploads/2025/11/PM9D3a-NVMe-U.2-Datasheet.pdf>

The PDF itself identifies Samsung Electronics, PM9D3a part numbers, copyright 2024 Samsung Electronics, and `Rev. 1.3, May. 2024`. Its revision history gives:

- Rev. 1.0 — initial issue — 26 September 2023;
- Rev. 1.1 — 29 January 2024;
- Rev. 1.2 — 14 March 2024;
- Rev. 1.3 — 29 May 2024.

However, the copy inspected here is **not hosted on an official Samsung domain** and visibly carries `CONFIDENTIAL` markings. Therefore its custody is weaker than the official Samsung DC Toolkit source used for the PM963 evidence. This packet treats it as a publicly reachable **Samsung-authored datasheet mirror**, not as proof that Samsung itself publicly released this exact PDF from its own site.

That custody caveat matters. The exact field names and byte layouts below are strong product-interface evidence from the mirrored document, but any stronger publication-history claim should wait for an official Samsung-hosted copy or another independent manufacturer distribution channel.

---

## Historical record

### 1. PM9D3a still exposes a lifetime read-reclaim counter

In **Table 148, Enhanced SMART Information Log (LID `0xC4`)**, the PM9D3a datasheet assigns bytes `331:324` to:

```text
Lifetime read Reclaim count
```

Adjacent lifetime-style fields include host reads, NAND writes, retired blocks, UECC count, power-on hours, and power-loss shutdown counts.

This is a direct product-interface continuation of a maintenance vocabulary already visible in the 2018 PM963 DC Toolkit evidence:

```text
2018 PM963:  Lifetime read Reclaim count
2024 PM9D3a: Lifetime read Reclaim count
```

But semantic-label continuity does **not** prove implementation continuity.

The PM963 field appeared at a different Extended SMART position in the inspected Toolkit output. The PM9D3a field resides at bytes `331:324` of its documented `0xC4` page. Therefore:

```text
same-looking maintenance label
    !=
stable telemetry byte layout across generations
```

and:

```text
same-looking maintenance label
    !=
same controller algorithm
```

### 2. PM9D3a separately exposes `Patrol Read Reclaim Count`

In **Table 149, Enhanced SMART Information Log (LID `0xD0`)**, the PM9D3a datasheet assigns bytes `114:111` to:

```text
Patrol Read Reclaim Count
```

The immediately preceding documented fields include `Read Fail Block Count` and `Read Recovery Count`; following fields include `Fast Cycle Count`, `Deep Erase Count`, and blocking-GC counters.

The key historical fact is intentionally narrow:

> A named Samsung PM9D3a product interface documents a `Patrol Read Reclaim Count` separately from the `Lifetime read Reclaim count` exposed on another log page.

Nothing in the inspected table defines the patrol algorithm, scan interval, trigger threshold, physical victim geometry, or whether a patrol read directly causes each reclaim event.

Thus the safe statement is:

```text
separately named patrol-associated reclaim telemetry
    !=
proved patrol-read state machine
```

### 3. PM9D3a separately exposes OCP `Refresh Counts`

In **Table 150, Cloud Attribute Log Page (LID `0xC0`) OCP Spec 2.0**, bytes `87:81` are documented as:

```text
Refresh Counts
```

The same table also exposes physical media units written/read, bad NAND-block counts, XOR recovery count, uncorrectable-read count, soft-ECC count, system-data percentage used, user-data erase counts, capacitor health, PLP start count, and endurance estimate.

Again, the evidence boundary is the interface field itself. The table does not define what NAND-level action the firmware counts as one `Refresh`, whether refresh always rewrites user payload, whether it is retention-driven, disturb-driven, patrol-driven, metadata-only, or whether one event can increment both a refresh counter and one of the reclaim counters.

Therefore:

```text
field named Refresh Counts
    !=
proved physical refresh mechanism
```

and especially:

```text
PM9D3a Refresh Counts
    !=
DRAM refresh
    !=
Case 36 correct-and-refresh by terminology alone
```

The word is insufficient to establish mechanism identity.

---

## What the three fields do establish

The PM9D3a telemetry schema forces at least a **three-way product-interface distinction**:

```text
A. Lifetime read Reclaim count
B. Patrol Read Reclaim Count
C. Refresh Counts
```

Because the datasheet assigns them separate fields, the repository should not collapse them into one generic `maintenance count` merely because all three can plausibly relate to media health.

This is enough to improve Case 67 in two ways.

First, it blocks a vocabulary shortcut:

```text
read reclaim
    !=
all proactive media maintenance
```

Second, it blocks a historical-schema shortcut:

```text
one vendor's maintenance term survives across products
    !=
the surrounding telemetry contract remains stable
```

---

## Engineering reconstruction

The following is reconstruction, not direct firmware disclosure.

### 1. Multiple counters imply multiple observation categories, not necessarily multiple physical mechanisms

A product can expose several counters even if some counters are incremented by overlapping internal work. Conversely, two counters can represent genuinely different maintenance paths.

The interface alone proves neither.

The most defensible abstraction is:

```text
physical / controller maintenance events
        |
        +--> accounting rule A --> Lifetime read Reclaim count
        |
        +--> accounting rule B --> Patrol Read Reclaim Count
        |
        `--> accounting rule C --> Refresh Counts
```

The accounting rules are not recovered from the table.

Therefore:

```text
separate counters
    !=
proved disjoint event sets
```

and:

```text
separate counters
    !=
proved identical event sets
```

The missing relation itself is the important evidence boundary.

### 2. Lifetime summary is not a complete causal history

`Lifetime read Reclaim count` is a cumulative summary. Even if it persists for the full supported lifetime implied by the label, the field cannot by itself answer:

- which blocks were reclaimed;
- when the events occurred;
- which read locations contributed to the decision;
- what ECC margin existed before relocation;
- whether events were host-read-triggered or background-triggered;
- what physical destinations received copied data;
- whether repeated work concerned the same logical payload.

So:

```text
cumulative maintenance summary
    !=
maintenance event history
```

This extends the PM963 boundary without changing it.

### 3. A `Lifetime` label does not prove the power-loss persistence implementation

The adjective `Lifetime` is useful interface vocabulary, but the inspected PM9D3a tables do not specify:

- where the counter is stored;
- when it is checkpointed;
- whether it is updated atomically with the maintenance event;
- whether sudden power loss can lose the most recent increment;
- behavior across firmware update, format, sanitize, namespace recreation, secure erase, RMA tooling, or controller replacement;
- overflow/saturation semantics.

Therefore:

```text
field labelled Lifetime
    !=
proved crash-consistent lifetime persistence protocol
```

This preserves the distinction central to Case 67:

```text
maintenance evidence lifetime
    !=
physical condition lifetime
```

### 4. Patrol-associated maintenance should not be equated with ordinary host reads

`Patrol Read Reclaim Count` has a distinct label from the lifetime read-reclaim counter. That supports a cautious engineering hypothesis that some reclaim accounting is associated with a patrol/background read regime rather than only direct host I/O.

But the product table alone does not establish:

```text
patrol read
    -> threshold crossing
    -> ECC qualification
    -> reclaim
```

as a deterministic state machine.

That chain remains a target for firmware documentation, tooling, trace evidence, or controlled experiments.

### 5. `Refresh` and `reclaim` should remain distinct until implementation evidence joins them

A rewrite can functionally refresh a NAND payload by moving it into a new physical population. Yet a field named `Refresh Counts` need not be that same operation.

For this product-interface slice:

```text
re-embodiment as a general function
    !=
product field named reclaim
    !=
product field named refresh
```

The repository may compare those functions, but it should not silently merge the counters.

---

## Functional comparisons

### Versus the PM963 evidence in this case

PM963 (2018 inspected Toolkit evidence) contributes:

```text
named shipping-family reference output
    -> Lifetime read Reclaim count
```

PM9D3a Rev. 1.3 contributes:

```text
0xC4 -> Lifetime read Reclaim count
0xD0 -> Patrol Read Reclaim Count
0xC0 -> Refresh Counts
```

The useful comparison is not “the algorithm evolved from X to Y.” It is:

> By the PM9D3a documentation, Samsung product telemetry distinguishes multiple maintenance-accounting categories around read reclaim / patrol / refresh that the older inspected PM963 reference output did not separately expose in the same way.

No firmware genealogy is asserted.

### Versus Case 36 — Flash Correct-and-Refresh

Case 36 studies a specified/published **function** in which correctable retention errors can motivate physical renewal.

Case 67F studies **product telemetry labels**.

The only safe comparison is:

```text
physical renewal may be functionally refresh-like
    !=
a counter named Refresh Counts proves Case 36's mechanism
```

### Versus Case 52 — read disturb

Case 52 establishes read-disturb physics and research/controller mitigation regimes.

The PM9D3a fields are product-interface observations. They do not prove the physical trigger for either reclaim field.

Thus:

```text
read-disturb mechanism evidence
    !=
read-reclaim telemetry label
```

### Versus proactive scan / scrub cases

The phrase `Patrol Read Reclaim Count` is functionally suggestive of proactive/background inspection plus corrective work. That is useful for cross-case vocabulary, but the name alone does not establish a scrub coverage contract, scan cursor, retry policy, cadence authority, or complete-media traversal.

Therefore:

```text
Patrol Read Reclaim Count
    !=
proved periodic full-media scrub
```

---

## Historical record / engineering reconstruction / functional comparison / interpretation ledger

| ID | Layer | Claim | Boundary |
| --- | --- | --- | --- |
| H-67F.1 | Historical record | PM9D3a Rev. 1.3 identifies Samsung PM9D3a U.2 products and is dated May 2024 | mirrored Samsung-authored datasheet; custody caveat applies |
| H-67F.2 | Historical record | revision history lists initial issue 2023-09-26 and Rev. 1.3 on 2024-05-29 | mirrored datasheet revision table |
| H-67F.3 | Historical record | `0xC4` bytes `331:324` are `Lifetime read Reclaim count` | Table 148 |
| H-67F.4 | Historical record | `0xD0` bytes `114:111` are `Patrol Read Reclaim Count` | Table 149 |
| H-67F.5 | Historical record | OCP `0xC0` bytes `87:81` are `Refresh Counts` | Table 150 |
| H-67F.6 | Historical record | Samsung's official PM9D3a page/blog identifies PM9D3a as a Samsung datacenter SSD and discusses enhanced telemetry | official Samsung web pages |
| E-67F.1 | Engineering reconstruction | three separately documented fields should remain separate accounting categories until stronger evidence joins them | follows from distinct interface fields |
| E-67F.2 | Engineering reconstruction | a cumulative count is a compressed maintenance summary, not a complete event history | follows from scalar/counter form |
| E-67F.3 | Engineering reconstruction | label continuity does not establish telemetry-layout or algorithm continuity | PM963/PM9D3a comparison |
| E-67F.4 | Engineering reconstruction | `Lifetime` does not by itself establish crash-consistent persistence semantics | persistence mechanism absent from inspected table |
| F-67F.1 | Functional comparison | patrol-associated reclaim is suggestive of proactive inspection/repair but is not proof of a scrub state machine | terminology-only comparison |
| F-67F.2 | Functional comparison | `Refresh Counts` may be compared with renewal functions, but not equated with Case 36 or DRAM refresh | mechanism not disclosed |
| I-67F.1 | Philosophical interpretation | systems can retain summaries of maintenance history without retaining the complete history itself | downstream interpretation only |

---

## Explicit non-claims

This packet does **not** claim that:

1. the xFusion-hosted PDF is an official Samsung-hosted public release;
2. the PDF's `CONFIDENTIAL` marking has no relevance to source custody;
3. Rev. 1.0's 2023-09-26 date is the PM9D3a product launch date;
4. Rev. 1.3's 2024-05-29 date is the first date these counters existed in firmware;
5. every PM9D3a capacity, form factor, firmware branch, or customer SKU implements identical counters;
6. PM963 and PM9D3a use the same controller architecture;
7. PM963 and PM9D3a use the same read-reclaim algorithm;
8. the PM9D3a lifetime counter has the same reset semantics as the PM963 field;
9. the word `Lifetime` proves power-loss-safe persistence of every increment;
10. the counter survives format, sanitize, firmware update, namespace recreation, or all service operations;
11. `Lifetime read Reclaim count` counts per-block read accesses;
12. `Lifetime read Reclaim count` is the same state as the read-count proxy in US20190066809A1;
13. `Patrol Read Reclaim Count` proves a periodic full-media scan;
14. one patrol read necessarily increments the patrol-reclaim counter;
15. one patrol reclaim necessarily increments the lifetime read-reclaim counter;
16. the two reclaim counters are mutually exclusive;
17. the two reclaim counters overlap;
18. `Refresh Counts` is retention refresh;
19. `Refresh Counts` is read-disturb repair;
20. `Refresh Counts` is metadata refresh;
21. `Refresh Counts` is identical to DRAM refresh;
22. `Refresh Counts` is identical to Case 36 correct-and-refresh;
23. a reclaim operation always performs physical erase immediately;
24. a reclaim operation securely erases the superseded cells;
25. reclaim is synonymous with capacity-driven garbage collection;
26. refresh is synonymous with reclaim;
27. telemetry counters disclose the victim-selection algorithm;
28. telemetry counters disclose threshold values or ECC margins;
29. telemetry counters prove relocation atomicity/currentness handoff semantics;
30. Samsung's telemetry design is genealogically derived from the SK hynix patent grounding Case 67.

---

## Philosophical interpretation — bounded and downstream

The strongest permissible interpretation is modest:

> A storage controller may retain compact summaries of maintenance work while discarding most of the causal history that led to each intervention.

PM9D3a's separate interface categories add another refinement:

> What a system chooses to count is itself part of the control boundary. Multiple counters can preserve distinctions among maintenance regimes without preserving the full physical history of the NAND cells or the full decision trace of the firmware.

This is not historical evidence about designer intent. It is a downstream systems interpretation of the exposed interface.

---

## Remaining evidence debt

The following remain open and should not be inferred from this packet:

- an official Samsung-hosted PM9D3a datasheet copy containing the same detailed tables;
- exact PM9D3a firmware meaning of `Patrol Read Reclaim`;
- exact firmware meaning of `Refresh Counts`;
- whether one physical maintenance event increments more than one counter;
- trigger thresholds and error-margin criteria;
- patrol cadence / coverage state / scan cursor semantics;
- counter update atomicity;
- power-cycle and sudden-power-loss persistence of the counters;
- reset/format/sanitize/firmware-update semantics;
- overflow/saturation semantics;
- reclaim destination selection and mapping/currentness handoff;
- independent product traces that correlate workload, telemetry deltas, and NAND maintenance;
- firmware-generation continuity between PM963, PM9A3, and PM9D3a.

The most valuable next experiment would be a controlled PM9D3a telemetry trace across:

```text
baseline
 -> sustained reads of a bounded LBA range
 -> idle / patrol interval
 -> power cycle
 -> repeated log-page reads
```

while recording `0xC4`, `0xD0`, and `0xC0` together. That could begin separating host-read reclaim, patrol-associated reclaim, refresh accounting, and power-cycle persistence without assuming their relation from names.

---

## Related-repository routing

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated PM9D3a read-reclaim / patrol-reclaim packet to reuse.

Keep in **technical-retention**:

- retention-specific distinctions among read-reclaim, patrol-associated reclaim, and refresh telemetry;
- persistence-horizon questions for maintenance counters;
- payload / physical-state / maintenance-evidence distinctions;
- cross-case comparison with read disturb, retention refresh, scrub, and relocation.

Route to **computing-archaeology** if pursued:

- Samsung enterprise-SSD product genealogy;
- controller-generation history;
- PM963 -> PM9A3 -> PM9D3a commercial lineage;
- V-NAND generation history;
- OCP/NVMe telemetry schema history outside the retention question;
- vendor/customer deployment chronology.

---

## Sources

1. Samsung Electronics, **Samsung SSD PM9D3a Specification (PCIe NVMe U.2), Rev. 1.3, May 2024**, publicly reachable mirror hosted by xFusion: <https://www.xfusion.com/wp-content/uploads/2025/11/PM9D3a-NVMe-U.2-Datasheet.pdf>. Relevant locations: cover/revision history; Table 148 (`0xC4`); Table 149 (`0xD0`); Table 150 (`0xC0`). Source-custody caveat above.
2. Samsung Semiconductor, **Datacenter SSD** portfolio / PM9D3a product context: <https://semiconductor.samsung.com/ssd/datacenter-ssd/>.
3. Samsung Semiconductor, **“Samsung's PM9D3a Solid State Drive”**, manufacturer technical blog: <https://semiconductor.samsung.com/news-events/tech-blog/samsung-pm9d3a-solid-state-drive/>.
4. Samsung Semiconductor, **“Empowering AI: Samsung Showcases Next-Gen Memory Solutions at the 2024 OCP Global Summit”**, manufacturer technical blog: <https://semiconductor.samsung.com/news-events/tech-blog/empowering-ai-samsung-showcases-next-gen-memory-solutions-at-the-2024-ocp-global-summit/>.
5. Existing repository evidence for the earlier named-product baseline: [`67-samsung-pm963-2016-2018-read-reclaim-telemetry-deepening.md`](./67-samsung-pm963-2016-2018-read-reclaim-telemetry-deepening.md).
