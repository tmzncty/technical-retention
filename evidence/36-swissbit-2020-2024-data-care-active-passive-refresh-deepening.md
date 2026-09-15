# Case 36 Deepening — Swissbit Data Care Management: Adaptive Read Refresh and Background Media Scan

## Status

**`bounded deepening complete`** — this slice adds a manufacturer-primary, named-commercial-product witness outside the IBM/TMS family for controller-managed Flash maintenance. It is bounded to what Swissbit publicly documents for the EN-20 product family in 2020 and the N3202 product fact sheet dated 28 October 2024.

The result is useful because Swissbit does not merely use the generic word `refresh`: the N3202 fact sheet explicitly divides `Data Care Management` into two named modes:

- **Active: Adaptive Read Refresh**;
- **Passive: Background Media Scan**.

The sources are strong enough to establish that a named shipping/marketed managed-Flash product family exposed distinct active/read-related and passive/background maintenance categories. They are **not** strong enough to reconstruct the firmware thresholds, physical rewrite geometry, exact ECC decision rule, low-power-state eligibility, completion telemetry, or any identity with Cai et al.'s 2012 FCR algorithm.

This is therefore a **commercial-product control-mode deepening**, not an FCR deployment claim and not an invention-priority claim.

---

## Research question

Case 36 already has three evidence layers:

1. pre-2012 public refresh prior art;
2. Cai et al.'s 2012 research proposal/evaluation with explicit ECC/refresh mechanics;
3. IBM FlashSystem 840 product-era documentation showing automatic commercial retention maintenance.

One open gap remained broader commercial comparison outside IBM/TMS:

> Can a different storage vendor's first-party product documentation expose a more differentiated maintenance vocabulary than generic `refresh`, while still leaving the internal algorithm opaque?

For the bounded Swissbit record, the answer is **yes**.

A second question follows:

> Does the vendor's `Active` / `Passive` split prove that one mode is triggered by every host read and the other rewrites data on a fixed background schedule?

The answer is **no**. The labels and feature names are historical vendor vocabulary; the exact event-to-action semantics remain undisclosed in the inspected material.

---

## Sources inspected

### A. Swissbit press release — EN-20 launch, 6 August 2020

Swissbit AG, **“Miniaturized highly reliable PCIe M.2 BGA SSD for ultra-small industrial applications”**, dated **6 August 2020**:

<https://www.swissbit.com/files/public/press_news/Press_Releases/2020/2020-08-06_Miniaturized_highly_reliable_PCIe_M.2_BGA_SSD_for_ultra-small_industrial_applications_EN.pdf>

The release identifies EN-20 as a managed industrial SSD using 3D NAND, a PCIe controller, and firmware. It states that `Data care management` adds extra protection for stored data at high operating temperatures. It also records product availability/qualification context rather than describing a research prototype.

**Evidence class:** `H/P` — manufacturer-primary product announcement and named-product feature statement.

**What it establishes:**

- EN-20 was publicly launched as a named managed SSD in 2020;
- Data Care Management was part of its reliability vocabulary;
- Swissbit tied that feature family to protection of stored data under demanding temperature conditions.

**What it does not establish:**

- the 2020 EN-20 implementation used the exact active/passive split documented for N3202 in 2024;
- every read invokes a physical refresh;
- any fixed scan period, ECC threshold, remap policy, or in-place rewrite policy;
- that EN-20 implements FCR, Case 67's SK hynix algorithm, or IBM FlashSystem's maintenance path.

### B. Swissbit N3202 Product Fact Sheet — 28 October 2024, Revision 1.01

Swissbit AG, **N3202 Series Product Fact Sheet**, dated **28 October 2024**, Revision **1.01**, file `P000000294.2`:

<https://www.swissbit.com/data/N3202/N3202_fact_sheet.pdf>

The fact sheet identifies N3202 as an industrial M.2 PCIe 4.0 SSD using 3D TLC NAND and NVMe 1.4. In the same product document it publishes both a bounded data-retention target and the Data Care Management mode names.

The product summary states:

- `Data Retention: 3 Years @ Life Begin; 4 Months @ Life End, @40 °C`;
- the retention footnote says NAND Flash suppliers refer to JEDEC JESD47 and JESD22 for retention testing and that the displayed target is based on information supplied by the NAND vendors.

The product-features page states:

- `Data Care Management`;
- `Active: Adaptive Read Refresh`;
- `Passive: Background Media Scan`.

The same page separately lists drive self-test, S.M.A.R.T./Telemetry, End-to-End Data Protection, power-loss protection, and security features.

**Evidence class:** `H/P` — manufacturer-primary named-product fact sheet with explicit revision/date.

### C. Swissbit Product Guide — current inspected product-family continuity

Swissbit AG, current **Product Guide**:

<https://www.swissbit.com/files/public/Documents/Swissbit_Product-Guide.pdf>

The currently inspected guide continues to list `Data Care Management` across managed NAND/SSD families, including PCIe BGA products in the EN/E-series family, and separately publishes product-family data-retention targets. The guide is useful as continuity/context, but because the inspected PDF does not expose a clear formal publication date in the extracted front matter, this addendum does **not** assign it a precise historical date or use it to move the chronology earlier.

**Evidence class:** `H/P` for current manufacturer product-family vocabulary; weak for exact chronology.

### D. Secondary corroboration — distributors reproducing Swissbit feature vocabulary

Contemporaneous product pages from major distributors reproduce the same feature vocabulary for Swissbit products, including `Adaptive Read Refresh` and `Background Media Scan`, and in some cases explicitly describe the combination as maintaining Flash-block retention. Examples include the EN-20/EN-26 product pages from Mouser and DigiKey.

These are useful only as **secondary corroboration**. The core claims in this addendum do not depend on them because first-party Swissbit documents already establish the named-product and mode vocabulary.

---

## Historical record

### H/P — Data Care Management is a named commercial feature, not only a research term

The 2020 EN-20 launch release presents Data Care Management alongside controller/firmware, LDPC error correction, power-fail protection, encryption, and thermal-management features of a named commercial product.

This gives a different evidence class from Cai et al. 2012:

```text
research proposal/evaluation
    !=
manufacturer product feature contract
```

The two may address overlapping reliability goals, but the commercial feature name is Swissbit's own vocabulary and should not be silently renamed `FCR`.

### H/P — N3202 exposes two distinct maintenance categories

The N3202 fact sheet explicitly separates:

```text
Data Care Management
    -> Active: Adaptive Read Refresh
    -> Passive: Background Media Scan
```

This is stronger than a generic statement that the SSD performs “refresh.” It shows that, at least at product-interface/documentation level, Swissbit distinguishes a read-related/adaptive maintenance mode from a passive/background scanning mode.

The exact internal state machines are not disclosed.

### H/P — the same product document keeps retention qualification and maintenance features separate

The N3202 fact sheet places a data-retention target in the product-summary section and Data Care Management in the product-features section.

That layout is evidence of coexistence, not mathematical dependence. The document does **not** say:

```text
3-year / 4-month target
    =
result of a specific Data Care Management schedule
```

Nor does it specify that the retention target assumes a particular amount of powered background scan time.

The conservative historical statement is only:

> the named product publishes both a retention target and controller-managed data-care features.

### H/P — `Active` and `Passive` are vendor labels, not project reconstruction terms

Unlike project terms such as `maintenance opportunity`, Swissbit itself uses `Active` and `Passive` in the N3202 feature list.

That makes the vocabulary historically useful, but it still requires restraint. In particular:

- `Active` is paired with `Adaptive Read Refresh`;
- `Passive` is paired with `Background Media Scan`;
- the fact sheet does not define `Active` as “every host read immediately rewrites NAND”;
- the fact sheet does not define `Passive` as “fixed-period whole-drive physical refresh.”

The labels identify categories. They do not expose the full trigger/action semantics.

---

## Retained state and control-state decomposition

The Swissbit documentation supports, or at minimum requires us to keep separate, the following layers:

1. **logical payload** — the host-visible value that is expected to remain readable;
2. **physical NAND state** — charge/threshold distributions and error margin in 3D TLC NAND;
3. **read-time evidence** — whatever evidence the implementation uses to make `Adaptive Read Refresh` adaptive;
4. **background-scan progress/state** — whatever state allows `Background Media Scan` to operate across media over time;
5. **refresh/rewrite decision state** — internal policy determining whether a discovered condition warrants physical renewal;
6. **mapping/currentness state** — required if renewal relocates data rather than restoring in place;
7. **health/telemetry state** — S.M.A.R.T./Telemetry is separately exposed by the product, but no inspected source maps a telemetry field to Data Care completion;
8. **retention qualification state** — life-begin/life-end and temperature qualification values shown in the product sheet.

Items 3–8 are partly engineering decomposition rather than vendor-defined internal structures. The source does not publish their exact implementation.

The important separation is:

```text
retention target
    !=
maintenance trigger evidence
    !=
maintenance action
    !=
maintenance progress/completion evidence
```

---

## Engineering reconstruction

### E — one managed SSD can expose more than one maintenance clock

The active/passive split is useful because it resists a one-dimensional model in which “Flash refresh” has one universal timer.

A read-related adaptive mode and a background scan can be driven by different event classes:

```text
foreground/read path evidence
    -> possible adaptive maintenance decision

background execution opportunity
    -> media scan / qualification work
```

The exact Swissbit triggers are not disclosed, so the arrows above are **functional reconstruction**, not literal firmware pseudocode.

The bounded result is:

> **one product's data-care regime can contain multiple maintenance modes rather than one universal refresh cadence**.

### E — `Adaptive Read Refresh` does not mean `every read rewrites`

The product term contains both `Read` and `Refresh`, but the documentation does not specify the condition between them.

Possible implementations could use ECC margin, read count, retry evidence, age, temperature, block state, or combinations of those signals. The inspected documents do not choose among them.

Therefore:

> **read-related maintenance feature != proof that every successful host read causes a physical rewrite**.

And:

> **feature name != exposed trigger threshold**.

This boundary is especially important when comparing with Case 67, where the patent evidence actually exposes a read-count proxy, test-read threshold, error qualification, adaptive threshold, and reclaim path.

### E — `Background Media Scan` does not by itself prove rewrite renewal

`Scan` directly establishes inspection/background traversal semantics more safely than rewrite semantics.

The fact sheet does not say whether every scanned region is:

- merely read;
- ECC-corrected in transit;
- rewritten in place;
- remapped to a fresh block;
- refreshed only when an error-margin threshold is exceeded;
- or left unchanged when sufficiently healthy.

Therefore:

> **background scan != background rewrite of every scanned block**.

The IBM FlashSystem 720/820 `sweeper` evidence in the existing Case 36 deepening has the same methodological stop condition: periodic reading is not automatically physical renewal.

### E — retention rating and maintenance regime are different relations

The N3202 fact sheet's retention target and Data Care Management feature list coexist, but the document does not provide a formula connecting them.

The correct decomposition is:

```text
retention qualification / product target
    -> bounded claim about expected storage behavior under stated conditions

runtime maintenance regime
    -> controller actions that may protect/requalify data during powered operation
```

Thus:

> **retention rating != refresh schedule**.

And:

> **maintenance feature != proof that the published retention number was measured with that feature continuously active**.

The N3202 footnote also prevents another shortcut: the product sheet refers to NAND suppliers' JESD47/JESD22 retention testing information. This must not be silently normalized into Case 76's JESD218 enterprise-SSD qualification relation.

### E — telemetry availability does not equal maintenance-completion evidence

The N3202 product sheet separately advertises S.M.A.R.T./Telemetry and Data Care Management.

That coexistence does **not** establish a telemetry field for:

- last adaptive read refresh;
- blocks refreshed;
- media-scan percentage;
- scan completion;
- corrected-retention-error count;
- next maintenance deadline.

Therefore:

> **device telemetry exists != retention-maintenance completion is externally observable**.

This is a useful negative result for Case 111 as well, where operator guidance raises the question of how powered background work can be proven complete.

### E — commercial maintenance can remain algorithmically opaque

Swissbit publishes enough to establish named maintenance categories but not enough to reconstruct the exact physical path.

The evidence boundary is therefore:

```text
commercial maintenance vocabulary
    !=
firmware algorithm disclosure
```

That distinction matters because Case 36's academic FCR source is unusually transparent about mechanisms while commercial sources can expose operational contracts but hide controller internals.

---

## Cross-case comparison

### Versus Case 36's 2012 FCR proposal

**FCR exposes:**

- measured retention-error behavior;
- ECC-bounded refresh logic;
- remapping and in-place reprogram paths;
- adaptive rate tied to P/E wear;
- endurance/refresh trade-offs.

**Swissbit exposes:**

- named commercial Data Care Management;
- explicit `Active: Adaptive Read Refresh`;
- explicit `Passive: Background Media Scan`;
- named product retention targets;
- no inspected algorithm-level threshold/rewrite details.

Functional overlap is real; mechanism identity is not established.

```text
FCR-like functional goal
    !=
FCR algorithm deployment
```

### Versus Case 67 — SK hynix read-disturb reclaim

Case 67's patent evidence exposes an actual controller-policy chain:

```text
read-count proxy
    -> thresholded test
    -> ECC/error evidence
    -> adaptive future threshold
    -> conditional reclaim/relocation
```

Swissbit's `Adaptive Read Refresh` is a product feature name only. It does not disclose a read-count proxy, error threshold, relocation rule, or counter persistence.

Therefore:

> **shared read-related maintenance goal != shared implementation**.

Swissbit does, however, provide a second named-commercial witness that read-associated maintenance exists as product vocabulary outside the Samsung PM963 telemetry witness already used in Case 67.

### Versus Case 111 — enterprise SSD extended-shutdown maintenance

Case 111 documents operator-facing powered maintenance windows and Dell's statement that a full read of used NAND can trigger retention tasks.

Swissbit provides a lower product-local layer:

- `Adaptive Read Refresh`;
- `Background Media Scan`.

But N3202 is an industrial SSD product, not evidence about Dell's affected PowerEdge drives or IBM ESS schedules. It supplies a functional comparison only:

> **read activity can coexist with a hidden maintenance path, and background maintenance can be separately named**.

It does not close Case 111's named-Dell-firmware or completion-telemetry debts.

### Versus Case 76 — JESD218 SSD qualification

Case 76 studies standards-level endurance/retention qualification. N3202 publishes a product retention target but explicitly grounds its footnote in NAND-supplier JESD47/JESD22 information.

Therefore:

> **product-sheet retention target != automatically a JESD218 enterprise-SSD qualification result**.

This avoids converting similar-looking `life begin / life end / temperature` numbers into an unsupported standards genealogy.

### Versus Case 150 — garbage collection

Background Media Scan and garbage collection can both consume idle/background controller time, but the trigger and objective are different evidence classes.

> **background media scan != capacity-reclamation garbage collection**.

Nothing in the Swissbit fact sheet says its scan selects erase-block victims for free-space recovery.

---

## Prior art / chronology boundary

This deepening makes **no invention-priority claim** for Swissbit.

Case 36 already has public nonvolatile-memory refresh records from 1978–2009 and commercial IBM retention-maintenance evidence in the 2013–2015 product era. The Swissbit material is later and contributes a different point:

> a named commercial product family publicly distinguishes multiple data-care modes using `Adaptive Read Refresh` and `Background Media Scan` vocabulary.

The 6-August-2020 EN-20 release gives a dated floor for Swissbit publicly associating `Data care management` with a named managed SSD and stored-data protection under high operating temperatures.

The 28-October-2024 N3202 fact sheet gives a dated floor, within the sources inspected for this slice, for the explicit `Active` / `Passive` mode labels on that named product.

Neither date is claimed as Swissbit's first-ever use of the concept or terminology.

No genealogy is asserted among:

```text
pre-2012 refresh patents
    -> Cai et al. FCR
    -> IBM FlashSystem maintenance
    -> Swissbit Data Care Management
```

The sequence is an evidence comparison, not a descent tree.

---

## Functional analogy and philosophical limit

A narrow project-level interpretation is useful:

> A retained object may depend on more than one maintenance pathway: one coupled to access/measurement and another coupled to background opportunity. “Persistence” therefore need not be implemented by one repeated operation or one clock.

This is not Swissbit's philosophical vocabulary. It is a bounded abstraction from the vendor's explicit active/passive maintenance categories.

The analogy must stop before claims such as:

- the drive “remembers to care for itself”;
- active and passive modes correspond to human attention and forgetting;
- every hidden controller action is constitutive of storage identity.

Those claims are neither necessary nor sourced.

---

## Explicit non-claims

This addendum does **not** claim that:

1. Swissbit invented Flash refresh, read refresh, media scanning, or Data Care Management as a general concept;
2. EN-20 was the first Swissbit product with Data Care Management;
3. N3202 was the first product to use the `Active` / `Passive` labels;
4. EN-20 in 2020 necessarily implemented exactly the same mode split as N3202 in 2024;
5. every host read triggers physical refresh;
6. `Adaptive Read Refresh` is identical to SK hynix's Case 67 read-count/reclaim algorithm;
7. `Adaptive Read Refresh` is identical to Samsung PM963 `read Reclaim` telemetry;
8. `Background Media Scan` rewrites every block it scans;
9. `Background Media Scan` is equivalent to IBM `deep scrub and refresh`;
10. the scan has a fixed whole-drive cadence;
11. S.M.A.R.T./Telemetry exposes Data Care completion or progress;
12. the published N3202 retention target is caused by, or mathematically derived from, Data Care Management;
13. N3202's retention values are a JESD218 enterprise qualification result;
14. Data Care Management runs in every NVMe power state;
15. the feature runs while the device is unpowered;
16. the documents reveal whether refresh is in-place, remap-based, or both;
17. the documents reveal controller ECC thresholds or read-reference logic;
18. commercial feature documentation is independent fault-injection validation;
19. functional similarity proves genealogy from FCR, IBM FlashSystem, Samsung, SK hynix, or earlier patents;
20. background retention maintenance implies sanitization or deletion of superseded physical embodiments.

---

## Claim ledger

| Claim | Layer | Strength / boundary |
| --- | --- | --- |
| Swissbit launched EN-20 on 6-Aug-2020 as a managed industrial PCIe/NVMe SSD using 3D NAND, controller, and firmware | `H/P` | strong; manufacturer launch release |
| The EN-20 launch release says Data Care Management adds extra protection for stored data at high operating temperatures | `H/P` | strong; manufacturer wording |
| Swissbit's N3202 fact sheet is dated 28-Oct-2024, Rev. 1.01 | `H/P` | strong; document-control field |
| N3202 is documented as PCIe 4.0 / NVMe 1.4 with 3D TLC NAND | `H/P` | strong; product summary |
| N3202 Data Care Management lists `Active: Adaptive Read Refresh` and `Passive: Background Media Scan` | `H/P` | strong; explicit product feature list |
| N3202 publishes `3 Years @ Life Begin; 4 Months @ Life End, @40 °C` | `H/P` | strong; product summary, product-specific |
| N3202 fact sheet ties that retention footnote to NAND-supplier JESD47/JESD22 information | `H/P` | strong; footnote; not JESD218 identity |
| N3202 separately lists S.M.A.R.T./Telemetry | `H/P` | strong; feature list |
| S.M.A.R.T./Telemetry therefore exposes Data Care progress/completion | `X` | rejected; no such field mapped in inspected sources |
| `Adaptive Read Refresh` means every host read rewrites NAND | `X` | rejected; trigger/action threshold not disclosed |
| `Background Media Scan` means every scanned region is rewritten | `X` | rejected; scan does not itself prove rewrite geometry |
| EN-20 and N3202 use an identical firmware algorithm | `X` | rejected; cross-generation identity not documented |
| Swissbit implements Cai et al.'s exact FCR algorithm | `X` | rejected; no algorithm identity/genealogy evidence |
| One managed SSD can expose multiple maintenance categories with different execution contexts | `E` | strong bounded reconstruction from explicit active/passive split |
| Retention rating, maintenance trigger, maintenance action, and completion evidence should be modeled separately | `E` | strong methodological reconstruction; source does not equate them |
| Active/passive data-care categories prove a universal taxonomy for SSD maintenance | `X` | rejected; vendor/product vocabulary only |

---

## Related-repository audit

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Swissbit` returned no dedicated case to reuse.

Division of labor remains:

- a broad history of Swissbit controller generations, EN/E/N-series product genealogy, NAND suppliers, firmware architecture, and the evolution of industrial SSD reliability features belongs primarily in `computing-archaeology`;
- the retention-specific distinction among product retention target, active read-related refresh, passive background scanning, opaque controller policy, and observable completion belongs in `technical-retention`.

This addendum intentionally avoids building a full Swissbit product history here.

---

## Remaining evidence debt

The next useful work is narrower than “find more commercial refresh examples”:

- obtain a Swissbit design-in guide, firmware manual, or support note that defines the trigger condition for `Adaptive Read Refresh`;
- determine whether adaptive read refresh is triggered by ECC correction count, raw/decoded error margin, read count, retry count, retention age, temperature, or a composite policy;
- determine what `Background Media Scan` does after detecting weak data: read-only qualification, in-place rewrite, remap/reclaim, or another path;
- identify whether the scan has a fixed/variable cadence and whether its progress survives reset/power loss;
- locate SBDM/S.M.A.R.T. documentation mapping any counters or progress fields specifically to Data Care operations;
- test a named firmware revision under controlled retention/read-disturb fault injection;
- recover older first-party Swissbit datasheets to establish when the active/passive vocabulary first appeared, without treating distributor publication dates as invention dates.

Until then, the correct conclusion remains bounded:

```text
named commercial Data Care Management
    -> explicit active read-refresh category
    + explicit passive background-scan category

but

feature vocabulary
    != trigger algorithm
    != rewrite geometry
    != completion telemetry
    != FCR identity
```

---

## Sources

1. Swissbit AG, **“Miniaturized highly reliable PCIe M.2 BGA SSD for ultra-small industrial applications”**, Press Release, 6 August 2020. <https://www.swissbit.com/files/public/press_news/Press_Releases/2020/2020-08-06_Miniaturized_highly_reliable_PCIe_M.2_BGA_SSD_for_ultra-small_industrial_applications_EN.pdf>
2. Swissbit AG, **N3202 Series Product Fact Sheet**, 28 October 2024, Revision 1.01, file `P000000294.2`. <https://www.swissbit.com/data/N3202/N3202_fact_sheet.pdf>
3. Swissbit AG, **Product Guide**, current inspected edition; used for current family continuity, not exact chronology. <https://www.swissbit.com/files/public/Documents/Swissbit_Product-Guide.pdf>
4. Mouser, **Swissbit EN-20/EN-26 Industrial BGA SSDs**, secondary product-page corroboration; not used as the primary basis for manufacturer claims. <https://www.mouser.com/new/swissbit/swissbit-en-20-en-26-ssds/>
5. DigiKey, **Swissbit EN-20 M.2 PCIe BGA**, secondary product-page corroboration; not used as the primary basis for chronology. <https://www.digikey.com/en/product-highlight/s/swissbit/en-20-m2-pcie-bga>
