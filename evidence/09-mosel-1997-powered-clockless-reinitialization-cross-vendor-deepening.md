# Case 09 deepening — Mosel Vitelic 1997 powered-clockless reinitialization cross-vendor witness

## Scope

This packet advances [`../cases/09-dram-cbr-refresh-address-internalization.md`](../cases/09-dram-cbr-refresh-address-internalization.md) at one deliberately narrow seam left open by the Hyundai HY534256 packet:

> **Was the rule “continued bias without clocks beyond the refresh interval requires initialization again” unique to the bounded Hyundai product sheet, or can the same interface-level contract be grounded independently in another DRAM vendor's product documentation?**

The bounded cross-vendor witness is Mosel Vitelic's `V53C16129H`, a 128K × 16 EDO-page-mode CMOS DRAM documented in **Rev. 1.2, July 1997**.

The answer is positive at the product-interface level. Mosel Vitelic specifies a 512-cycle / 8 ms refresh obligation, an internal nine-bit row counter for CAS-before-RAS refresh, an initial 200 µs power-on pause followed by at least eight initialization cycles, and—critically—**eight initialization cycles after extended periods of bias without clocks greater than the refresh interval**.

This independently corroborates the existence of a powered-clockless reinitialization contract beyond Hyundai. It does **not** prove that all asynchronous DRAMs behaved this way, that Hyundai and Mosel used the same internal circuit, that one vendor copied the other, that the rule came from a standard, or that eight initialization cycles restore a full array whose payload has already decayed.

Case 09 remains **`grounded`**. This packet deepens evidence; it does not justify a maturity promotion.

---

## Source custody and evidence class

### Mosel Vitelic product documentation

The source is Mosel Vitelic's manufacturer-authored datasheet:

- `V53C16129H HIGH PERFORMANCE 128K x 16 BIT EDO PAGE MODE CMOS DYNAMIC RAM`;
- marked `PRELIMINARY`;
- `V53C16129H Rev. 1.2 July 1997`.

The manufacturer document is currently consulted through a third-party archival mirror. Relevant page-rendered custody paths are:

- page 1, product identity and `Refresh Interval: 512 cycles/8ms`: <https://www.alldatasheet.net/html-pdf/2372/MOSEL/V53C16129H/105/1/V53C16129H.html>;
- page 17, refresh-cycle description and internal nine-bit CBR counter: <https://www.alldatasheet.net/html-pdf/2372/MOSEL/V53C16129H/1849/17/V53C16129H.html>;
- page 18, `Power-On` and powered-clockless initialization rule: <https://www.alldatasheet.net/html-pdf/2372/MOSEL/V53C16129H/1958/18/V53C16129H.html>;
- datasheet landing page identifying Mosel Vitelic as manufacturer: <https://www.alldatasheet.net/datasheet-pdf/pdf/2372/MOSEL/V53C16129H.html>.

The mirror is custody, not independent technical validation. Historical claims below are bounded to the content of Mosel Vitelic's published product sheet.

### Related-repository check

`tmzncty/computing-archaeology` was searched for both `V53C16129H` and the phrase `extended periods of bias without clocks`. No directly reusable packet was identified in this pass.

Accordingly, this file keeps only the retention/control boundary needed by Case 09. A broader genealogy of asynchronous-DRAM initialization wording still belongs in `computing-archaeology` if pursued.

---

## Historical / source record

### H/P — the device has a finite refresh-coverage contract

Mosel Vitelic's feature summary identifies the device as a 128K × 16 CMOS DRAM and lists:

```text
RAS-Only Refresh
CAS-Before-RAS Refresh
Refresh Interval: 512 cycles / 8 ms
```

The functional description later states that retaining data requires **512 refresh cycles in each 8 ms period**.

The source therefore distinguishes continued supply from the recurring work required to retain dynamic data:

```text
VCC present
    != refresh coverage automatically satisfied
```

That inequality is an engineering restatement of the product contract, not Mosel Vitelic's wording.

### H/P — ordinary row refresh and CBR row enumeration are separately described

The refresh section gives two ways to meet the refresh requirement.

First, the host/controller can clock each of the 512 row addresses with RAS. Read, write, read-modify-write, and RAS-only cycles refresh the addressed row.

Second, CAS-before-RAS refresh can be invoked. In that mode the V53C16129H uses the output of an **internal nine-bit counter** as the row-address source and ignores external address inputs.

This directly supports the familiar Case 09 partition:

```text
row-enumeration authority can move on-chip
    while
refresh-event recurrence can still require external interface activity
```

The sheet also says that a CAS-before-RAS counter-test mode exists. That is useful evidence for testability, but it does not by itself reveal the normal counter value after power-up or after a prolonged clockless interval.

### H/P — power-on requires a pause plus eight initialization cycles

Under `Power-On`, Mosel Vitelic specifies:

1. apply VCC;
2. wait an initial **200 µs**;
3. execute at least **eight initialization cycles**;
4. those cycles may be any combination containing a RAS clock.

The source does not define the eight cycles as a full-array refresh traversal. It defines a bounded initialization sequence.

### H/P — the initialization obligation returns without power removal

The same `Power-On` section states that **eight initialization cycles are required after extended periods of bias without clocks**, and bounds the interval parenthetically as **greater than the Refresh Interval**.

For this product the refresh interval is separately specified as 8 ms.

The crucial historical relation is therefore:

```text
VCC/bias retained
    + clocks absent > refresh interval
    -> eight initialization cycles required
```

No power loss is required by the published condition.

This independently reproduces the central interface-level boundary already found in Hyundai's 1992 HY534256 documentation.

### H/P — the datasheet exposes a refresh counter but not the cause of reinitialization

The V53C16129H block diagram names a `REFRESH COUNTER`, and the functional text identifies an internal nine-bit counter for CBR row selection.

However, the `Power-On` paragraph does **not** say:

- that this counter resets to zero after prolonged clocklessness;
- that it keeps its prior value;
- that it becomes invalid;
- that the eight-cycle requirement exists solely for the counter;
- that power-on initialization and powered-clockless reinitialization have the same transistor-level cause.

The existence of a named internal counter therefore narrows the architecture but does not close the hidden-state explanation.

---

## Cross-vendor comparison: Hyundai 1992 vs Mosel Vitelic 1997

The comparison is valuable precisely because the two documents are manufacturer product sheets separated by vendor and time.

| Boundary | Hyundai HY534256 (1992) | Mosel Vitelic V53C16129H (1997) |
| --- | --- | --- |
| DRAM organization | 256K × 4 | 128K × 16 |
| refresh coverage | 512 cycles / 8 ms | 512 cycles / 8 ms |
| CBR row source | internal 9-bit counter | internal 9-bit counter |
| power-on pause | 200 µs | 200 µs |
| minimum initialization | 8 RAS-bearing cycles | 8 RAS-bearing cycles |
| powered-clockless rule | 8 cycles after bias without clocks > refresh interval | 8 cycles after bias without clocks > refresh interval |

This table supports a stronger statement than the Hyundai packet alone:

> **The powered-clockless reinitialization rule is not evidenced only in one Hyundai product sheet; a later Mosel Vitelic product sheet independently publishes the same interface-level structure.**

It does **not** support the stronger historical claims that the rule was universal, standardized, copied, licensed, inherited from one vendor to the other, or implemented by the same circuit.

The unusually similar wording is itself a reason to seek genealogy before making genealogy claims—not a substitute for genealogy evidence.

---

## Engineering reconstruction

The vocabulary in this section is repository analysis, not historical source vocabulary.

### E — cross-vendor evidence strengthens the `powered-bias requalification boundary`

The Hyundai packet introduced the project-level term **powered-bias requalification boundary** for a condition where power remains present but the vendor requires initialization again after an overlong lapse in qualifying clocked activity.

Mosel Vitelic independently supports the same bounded reconstruction:

```text
power continuity
    != maintenance continuity

maintenance continuity interrupted beyond vendor refresh interval
    -> initialization/requalification procedure required
```

The second vendor changes the evidentiary status of the pattern from “one named implementation contract” to “cross-vendor product-contract pattern with at least two named witnesses.”

It still does not justify “all DRAMs”.

### E — one gross power epoch can contain multiple maintenance-qualified regimes

For both named devices, the published rule allows this sequence:

```text
VCC applied
    -> initialization
    -> normal refresh-qualified operation
    -> prolonged clockless interval while VCC remains
    -> initialization required again
    -> normal refresh-qualified operation can resume
```

So a single gross power interval can contain more than one analytically useful **maintenance-qualified epoch**.

That phrase is repository vocabulary. The source only specifies the required initialization behavior.

### E — requalification is not full-array payload restoration

Mosel's numeric relation makes the anti-collapse especially clear:

```text
8 initialization cycles
    != 512 refresh cycles required for full documented coverage
```

Therefore:

```text
re-establishing a control/operational precondition
    != reconstructing every dynamic storage cell
    != recovering information that has already decayed
```

The same distinction was visible in Hyundai; the second vendor corroborates it.

### E — a visible internal counter still does not authorize a hidden-state story

It is tempting to reason:

```text
CBR uses internal counter
+ eight cycles required after clockless gap
therefore counter must have reset / become random
```

That inference is not source-supported.

A product contract can require a procedure for reasons involving several internal nodes, timing generators, sense paths, precharge state, counter state, or interactions not exposed in the public sheet. Without a manufacturer source binding cause to rule, this packet keeps the explanation at the interface level.

### E — the refresh interval is a contractual boundary, not a per-cell analog cliff

Mosel uses `greater than the Refresh Interval` to decide when the initialization rule applies. The same datasheet specifies that interval as 8 ms.

This does not prove that every cell loses information at 8 ms + epsilon. It proves that the vendor's **operational procedure** changes once the clockless interval exceeds the specified refresh interval.

Thus:

```text
vendor procedural threshold
    != deterministic physical failure time of every storage cell
```

---

## Historical record vs engineering reconstruction vs analogy vs interpretation

### Historical/source record

Supported directly for the V53C16129H:

- Rev. 1.2 is dated July 1997;
- the product is a 128K × 16 EDO CMOS DRAM;
- refresh contract is 512 cycles per 8 ms;
- RAS-only and CAS-before-RAS refresh are supported;
- CBR uses an internal nine-bit row counter and ignores external address inputs;
- power-on requires 200 µs then at least eight RAS-bearing initialization cycles;
- eight initialization cycles are again required after extended bias without clocks greater than the refresh interval.

### Engineering reconstruction

Repository-level terms used here:

- `powered-bias requalification boundary`;
- `maintenance-qualified epoch`;
- `maintenance continuity`;
- `control-state qualification`;
- `coverage obligation`.

These terms summarize source-grounded relations. They are not retroactive Mosel or Hyundai terminology.

### Functional analogy

The following comparisons are allowed only as functional parallels:

- Case 04: physical operation completion is separate from later reuse admission;
- Case 38: maintenance policy/execution/readiness are separate predicates;
- Case 101: a gross power epoch and useful maintenance-observability epoch need not be identical.

No genealogy is implied.

### Philosophical interpretation

A restrained interpretation is that **continuity of energy is not identical to continuity of the maintenance relation that keeps dynamic information operationally qualified**.

That is a project interpretation, not a statement by Mosel Vitelic or Hyundai.

---

## Anti-collapse ledger

| Shortcut | Status | Reason |
| --- | --- | --- |
| `powered == refreshed` | rejected | product requires recurring refresh cycles |
| `powered continuously == continuously qualified` | rejected for this product contract | overlong clockless bias triggers initialization requirement |
| `eight initialization cycles == full-array refresh` | rejected | full documented coverage is 512 cycles |
| `initialization == payload recovery` | rejected | no source says lost logical data are reconstructed |
| `internal refresh counter == autonomous refresh scheduler` | rejected | CBR row enumeration still occurs under externally invoked cycles |
| `counter exists == counter is the sole cause of reinitialization` | rejected | internal cause is not bound by source |
| `clockless gap > 8 ms == every bit certainly lost` | rejected | procedural threshold is not per-cell failure proof |
| `Hyundai + Mosel == all asynchronous DRAMs` | rejected | two witnesses are not universality |
| `similar wording == proven standards provenance` | rejected | no standard/genealogy source established |
| `similar wording == direct vendor copying` | rejected | no influence evidence established |
| `same procedure == identical internal circuit` | rejected | source does not expose implementation equivalence |
| `counter test == normal reset semantics` | rejected | diagnostic capability does not bind normal hidden state |
| `same VCC epoch == same maintenance-qualified epoch` | rejected as an analytical shortcut | both vendors require renewed initialization after overlong clocklessness |

---

## Relation to existing Case 09 evidence

### Hyundai 1992 powered-clockless packet

[`09-hyundai-1992-powered-clockless-bias-reinitialization-deepening.md`](09-hyundai-1992-powered-clockless-bias-reinitialization-deepening.md) remains the earlier bounded product witness.

This Mosel packet does not supersede it. It changes the evidentiary shape:

```text
before:
    one named vendor/product witness

after:
    at least two named vendor/product witnesses
    separated by vendor and publication date
```

The correct conclusion is cross-vendor corroboration, not universality.

### Counter-initialization/test packet

[`09-dram-refresh-counter-initialization-test-deepening.md`](09-dram-refresh-counter-initialization-test-deepening.md) should still own claims about disclosed counter initialization/test mechanisms.

The Mosel sheet's named internal counter and counter-test mode are relevant context, but the powered-clockless rule does not reveal the normal-mode counter state after the gap.

### Micron 1999 AUTO REFRESH vs SELF REFRESH packet

[`09-micron-1999-sdram-auto-vs-self-refresh-deepening.md`](09-micron-1999-sdram-auto-vs-self-refresh-deepening.md) remains the later same-product comparison for moving recurring cadence authority onto the SDRAM after SELF REFRESH entry.

Mosel Vitelic's CBR contract still represents a different partition: row enumeration is internal, but recurring refresh activity remains externally exercised.

---

## Functional cross-case comparisons

### Case 04 — Flash reuse admission

Case 04's Linux FTL evidence separates successful erase, post-erase preparation, and permission to reuse a transfer unit. The useful abstraction is:

```text
substrate condition
    != control-layer qualification for next use
```

The mechanisms are unrelated; the comparison is functional only.

### Case 38 — SSD PLI maintenance

Case 38 separates configured maintenance cadence, actual maintenance execution, and readiness evidence. The DRAM cross-vendor witness supplies a much older reminder that availability of a supporting resource (power) does not prove current maintenance qualification.

### Case 101 — SCSI BMS power-epoch observability

Case 101 shows that host-visible maintenance progress can have power-epoch-scoped semantics. Case 09 now adds cross-vendor evidence that **within one continuously powered interval**, an overlong lapse in maintenance-driving clocks can itself create a renewed initialization boundary.

---

## Claim ledger

| Claim | Label | Confidence |
| --- | --- | --- |
| Mosel Vitelic V53C16129H Rev. 1.2 is dated July 1997 | `H/P` | high |
| product refresh contract is 512 cycles / 8 ms | `H/P` | high |
| CBR refresh uses an internal nine-bit row counter | `H/P` | high |
| power-on requires 200 µs then at least eight RAS-bearing initialization cycles | `H/P` | high |
| eight initialization cycles are also required after bias without clocks > refresh interval | `H/P` | high |
| Hyundai is no longer the only named vendor witness in Case 09 for this rule | `H/P` | high |
| powered-bias requalification is a useful cross-vendor engineering category | `E` | medium-high, bounded to two product witnesses |
| the two vendors used identical internal circuits | `X` | unsupported |
| the wording proves a common JEDEC-standard origin | `X` | unsupported |
| the wording proves direct vendor influence/copying | `X` | unsupported |
| eight initialization cycles restore the entire array | `X` | contradicted by 512-cycle coverage contract |
| the CBR counter resets to a known value after the clockless gap | `X` | unsupported |
| all asynchronous DRAMs require the same procedure | `X` | unsupported |

---

## What this slice closes

The previous Case 09 index listed **cross-vendor powered-clockless wording** as the highest-value evidence debt.

This packet closes that debt at a bounded level:

```text
Hyundai HY534256, 1992
    +
Mosel Vitelic V53C16129H, 1997
    -> cross-vendor corroboration of
       initialization after extended powered clocklessness
```

It does **not** close the broader historical-genealogy question of where the wording originated or how widespread it was across the industry.

---

## Remaining evidence debt

The next useful work is now narrower and different:

1. **Genealogy / standard provenance.** Find an earlier manufacturer handbook, JEDEC document, application note, or design guide that can explain whether the near-identical initialization wording came from a shared convention or standard. Put the broad history in `computing-archaeology` and link back.
2. **Hidden-state binding.** Find a manufacturer source explicitly explaining which internal state requires renewed initialization after prolonged powered clocklessness.
3. **Earlier independent witness.** If available, locate a late-1980s/early-1990s non-Hyundai product sheet with the same rule to move the public floor earlier without conflating publication with invention.
4. **Hardware trace.** Keep VDD applied while sweeping clockless gaps below and above the refresh interval; observe payload correctness, normal access behavior, initialization requirements, and CBR counter-test progression independently.
5. **Do not promote universality.** Even if more vendor sheets are found, distinguish common contract wording from identical silicon implementation.

---

## Sources

1. Mosel Vitelic, `V53C16129H HIGH PERFORMANCE 128K x 16 BIT EDO PAGE MODE CMOS DYNAMIC RAM`, Rev. 1.2, July 1997, page 1 (identity, features, 512-cycle/8-ms refresh interval): <https://www.alldatasheet.net/html-pdf/2372/MOSEL/V53C16129H/105/1/V53C16129H.html>.
2. Same datasheet, page 17 (`Refresh Cycle`, 512 cycles / 8 ms, CBR internal nine-bit counter, external addresses ignored): <https://www.alldatasheet.net/html-pdf/2372/MOSEL/V53C16129H/1849/17/V53C16129H.html>.
3. Same datasheet, page 18 (`Power-On`, 200 µs pause, eight initialization cycles, and renewed eight-cycle requirement after extended bias without clocks greater than the refresh interval): <https://www.alldatasheet.net/html-pdf/2372/MOSEL/V53C16129H/1958/18/V53C16129H.html>.
4. Mosel Vitelic datasheet landing page / archival custody metadata: <https://www.alldatasheet.net/datasheet-pdf/pdf/2372/MOSEL/V53C16129H.html>.
5. Hyundai comparison packet and its manufacturer-primary archival sources: [`09-hyundai-1992-powered-clockless-bias-reinitialization-deepening.md`](09-hyundai-1992-powered-clockless-bias-reinitialization-deepening.md).

### Source-boundary note

The Mosel Vitelic document is manufacturer-authored primary technical material preserved by a third-party mirror. The mirror contributes custody, not independent validation. Cross-vendor corroboration here means **two different manufacturers published the same bounded operational relation**; it does not establish common authorship, standards provenance, silicon identity, or direct historical influence.