# Case 121 Deepening — PRAC Counter Integrity, Uncorrectable State, and Error-Authority Handoff

## Status

**`bounded deepening complete`** for one narrow question:

> Once per-row activation counts are initialized and operational, what happens if the *maintenance metadata itself* is detected as corrupted or untrustworthy?

This record does not attempt to reconstruct the complete JEDEC PRAC error-handling contract. It uses two primary patent disclosures to establish a bounded pre-/post-standard mechanism comparison:

- Intel, US20210365316A1, filed 4 June 2021 and published 25 November 2021, for ECC-protected per-row activation-count state and a conservative response to an uncorrectable count;
- AMD, US20250383947A1, filed 17 June 2024 and published 18 December 2025, for immediate host notification of a detected PRAC-counter error through alert-path logic, with embodiments that either continue or disable PRAC monitoring.

The parent case remains [`../cases/121-ddr5-prac-activation-counter-initialization.md`](../cases/121-ddr5-prac-activation-counter-initialization.md). Its earlier grounding already establishes Micron's ACI/readiness and refresh-dependence boundary. This note adds a different failure class: **a counter may be initialized and temporally current yet still cease to be trustworthy because its bits or associated error-detection state are faulty.**

---

## Source custody and source typing

### Source A — Intel, US20210365316A1

**Type:** patent / primary technical disclosure (`H/P`, prior-art and mechanism witness)

- Title: `Memory chip with per row activation count having error correction code protection`
- Assignee: Intel Corporation
- filing / priority date: 4 June 2021
- publication: US20210365316A1, 25 November 2021
- later grant: US12164373B2, 10 December 2024
- public text: https://patents.google.com/patent/US20210365316A1/en

The patent describes row-associated storage cells holding an activation-count value and ECC information, ECC read logic that can correct an error, updated ECC generation when the count is incremented, and implementation-dependent responses when a count/ECC error is detected but cannot be corrected.

Its especially useful negative-control embodiment treats an uncorrectable count as potentially being at or near the hammer threshold and therefore refreshes possible victim rows rather than pretending the exact count has been recovered.

This is a patent embodiment, not evidence that the exact design shipped in a named Intel DRAM product or that it became the later JEDEC PRAC contract.

### Source B — AMD, US20250383947A1

**Type:** patent / primary technical disclosure (`H/P`, post-standard mechanism witness)

- Title: `Per row activation counting error handling`
- Assignee: Advanced Micro Devices, Inc.
- filing / priority date: 17 June 2024
- publication: US20250383947A1, 18 December 2025
- related PCT priority record: PCT/US2025/028210
- public text: https://patents.google.com/patent/US20250383947A1/en

The application states that the row-hammer mitigation technique depends on PRAC-counter accuracy/validity and that PRAC counters can themselves experience errors. It describes detecting such an error and routing a signal to logic that also handles the PRAC alert path so the host can be notified without waiting for a later error-scrubbing pass.

The disclosure further describes embodiments in which:

- an address associated with the error can be retained in alert logic or mode registers;
- the host can poll mode registers to evaluate the error;
- the DRAM can continue PRAC monitoring after the notification; or
- PRAC monitoring can be disabled, depending on configured behavior.

The document mentions a scrub interval such as once per 24 hours only as an example. This record does **not** generalize that number into a DDR5 requirement or a shipping-product schedule.

This source is not a normative JEDEC document and does not prove that any named AMD memory controller or DRAM product implements the disclosed path.

### Source C — existing Case 121 Micron product grounding

The existing repository record uses Micron's `DDR5 SDRAM Product Core Data Sheet`, Rev. E (11/2024), to establish that activation-counter bits require refresh, ACI establishes known counter state, and counting/ABO are withheld until initialization completes.

See:

- [`121-ddr5-2021-2025-prac-activation-counter-grounding.md`](121-ddr5-2021-2025-prac-activation-counter-grounding.md)
- [`121-ddr5-prac-powerup-reset-reconstitution-deepening.md`](121-ddr5-prac-powerup-reset-reconstitution-deepening.md)

Those records are reused rather than re-copying the Micron product history here.

---

## Historical record

### 2021: per-row activation-count state is already treated as error-protected metadata

Intel's 2021 filing predates the April 2024 public JESD79-5C PRAC announcement used by the parent case. It describes a memory-chip design in which each row has activation-count storage plus ECC information. On a count update, both the count and ECC information are read; correctable corruption can be repaired in the ECC path, and new ECC information is generated for the incremented count before writeback.

The historical claim is intentionally narrow:

> By 4 June 2021, a primary patent disclosure already treats per-row activation-count state as metadata whose own bit integrity can require ECC protection.

This does **not** show that Intel invented all counter protection, that the design shipped, or that later JEDEC PRAC copied the patent.

### 2021: an uncorrectable count can trigger conservative mitigation without count recovery

The same Intel disclosure explicitly considers an error in the count/ECC state that is detected but cannot be corrected. One described response is to act as though the unknown correct count may be at or near the hammer threshold and refresh possible victim rows.

That is a strong retention-specific witness because the safety action does not require reconstruction of the exact lost count.

The historical record supports:

> **uncorrectable maintenance metadata can cause a conservative protection action even when the precise previous metadata value is unavailable.**

It does not prove that all PRAC implementations use this fail-safe rule.

### June 2024 filing / December 2025 publication: AMD separates counter-error detection from later scrub reporting

AMD's filing came after JEDEC publicly announced JESD79-5C in April 2024. It therefore cannot be used as prior art for the 2024 public naming of PRAC itself.

Its useful contribution is later and narrower. The disclosure identifies a problem in waiting for an ordinary error-scrubbing protocol to discover/report a PRAC-counter error. It instead routes a detected PRAC-counter error into alert-path logic for prompt host notification.

The chronology must therefore remain:

```text
Intel filing: 2021-06-04
    -> earlier public mechanism floor for ECC-protected per-row counts

JESD79-5C public PRAC announcement: 2024-04-17
    -> named standards-publication floor used by Case 121

AMD filing: 2024-06-17
    -> later PRAC-specific counter-error handling disclosure

AMD publication: 2025-12-18
    -> public disclosure date of that application text
```

Filing chronology, standards-publication chronology, and patent-publication chronology are kept separate.

---

## Engineering reconstruction

### Initialized ≠ indefinitely trustworthy

The existing Case 121 ACI evidence establishes a readiness transition:

```text
unknown / uninitialized counter state
    -> ACI
    -> initialized / ready counter state
```

The Intel and AMD error-handling disclosures add another axis:

```text
initialized / operational counter state
    -> bit or counter-integrity error detected
    -> exact count may remain correctable, uncertain, or unrecoverable
    -> protection logic must choose a response
```

Therefore:

> **counter initialized ≠ counter guaranteed correct forever.**

ACI readiness and later counter integrity are different relations.

### Freshness/refresh validity ≠ bit-integrity validity

Micron's bounded product evidence says activation-counter bits require refresh and can become unknown after refresh requirements are violated. Intel/AMD instead expose error-detection/correction paths for counter corruption.

These should not be collapsed:

> **refresh-valid lifetime ≠ ECC/parity integrity state.**

A counter can become untrustworthy because its retention regime was violated, or because an error is detected despite being inside a nominally valid operational regime. The inspected sources do not establish that those causes are physically identical.

### Correcting the counter ≠ mitigating the payload risk

Intel's disclosure separates two operations:

1. recover/correct the counter when ECC can do so;
2. if the count cannot be corrected, conservatively refresh possible victim rows.

Thus:

> **maintenance-metadata repair ≠ payload-protection action.**

A corrected counter restores the decision state. A victim-row refresh acts on the state being protected. One may lead to the other, but they are not the same retained object or same operation.

### Uncorrectable count ≠ recovered count

The most important Intel boundary is that safety can be retained without recovering exact history. If an uncorrectable count is pessimistically treated as near threshold, the system is deliberately replacing epistemic precision with a conservative action.

Therefore:

> **fail-safe mitigation != recovery of the previous activation count.**

and:

> **protection continuity can survive loss of exact maintenance-history precision if the system has a safe fallback.**

This is a bounded engineering reconstruction from the patent embodiment, not a universal RowHammer-defense theorem.

### Error detection ≠ exact error localization

AMD explicitly treats immediate notification as separable from identifying the exact row address. Its embodiments can retain an address near the alert logic or in mode registers, and the host can poll status; it also notes that exact localization may not always be practical immediately.

Therefore:

> **knowing that protection metadata is faulty ≠ knowing the exact faulty metadata location.**

This matters because a state can lose authority before the system possesses a complete diagnostic explanation of the fault.

### Alert transport ≠ mitigation

AMD reuses or couples to alert-path logic to notify the host of a counter error. The notification transports a condition across the DRAM/host boundary. It does not by itself restore the count or refresh a victim row.

> **error notification != counter repair != RowHammer mitigation.**

A shared signal path must not be mistaken for shared semantics of the events carried over it.

### Continue monitoring ≠ trust restored

AMD claims cover both continuing PRAC monitoring and disabling monitoring while an error notification is sent. That alternative is useful precisely because notification does not settle the counter's later authority.

A continued-monitoring embodiment cannot safely be generalized into:

> `error detected -> all counters remain fully authoritative`.

Likewise a disabled-monitoring embodiment does not establish that all PRAC errors require global shutdown.

The bounded lesson is only:

> **error handling includes an authority-policy decision about whether the damaged monitoring regime may continue.**

### Scrub schedule ≠ immediate protection deadline

AMD contrasts immediate notification with a broader scrub process that may discover/report errors later. The patent gives `once every 24 hours` as an example scrub cadence, not a normative timing requirement.

Therefore:

> **event-triggered counter-error alert != periodic whole-array scrub.**

and:

> **an example scrub interval != PRAC counter-error tolerance window.**

The reason for the fast path is semantic urgency: a corrupted counter participates in deciding whether future mitigation is owed.

---

## A four-way failure-handling taxonomy for Case 121

Across the already-grounded Micron product contract and these Intel/AMD patent embodiments, at least four distinct responses to untrustworthy maintenance metadata can now be kept separate:

1. **reinitialize** — ACI establishes a new known starting condition when activation-counter state is unknown;
2. **correct** — ECC can repair a correctable counter-state error and preserve the count relation;
3. **act conservatively** — an uncorrectable count can be treated as near threshold and cause mitigation without exact count recovery;
4. **revoke / hand off authority** — an error can be signaled to the host, which may continue or disable monitoring according to the disclosed policy.

These are not a universal JEDEC state machine. They are a comparative vocabulary grounded in different source types.

The central retention relation is:

> **when second-order state becomes untrustworthy, preserving system protection does not always require preserving that state's exact previous value; systems can reconstitute, correct, conservatively substitute, or revoke its authority.**

---

## Functional comparisons — bounded

### Case 45 — DDR5 on-die ECC / ECS

Case 45 concerns error correction/scrubbing of DRAM data and exposed maintenance state. The Intel/AMD PRAC evidence adds a different target for integrity machinery: the metadata that decides when disturbance protection should occur.

Safe comparison:

> **payload ECC state != protection-counter integrity state.**

Both can use error-detection/correction ideas, but no common physical ECC layout or implementation genealogy is asserted.

### Case 83 — HDFS scanner checkpoint state

Case 83's scanner cursor can be checkpointed so maintenance progress can resume after restart. Case 121's corrupted activation count exposes almost the opposite requirement: the system may refuse to preserve the exact state if that state is no longer trustworthy.

> **preserving maintenance progress != preserving untrusted maintenance metadata.**

No genealogy is asserted.

### Case 55 — SSD health telemetry

Case 55 shows controller-maintained health state that influences later service decisions. Case 121 adds a stricter failure boundary: metadata used for protection may itself require an integrity/error path before it is allowed to govern further work.

The comparison is functional only:

> **maintenance telemetry exists != maintenance telemetry is authoritative under every error condition.**

---

## Philosophical interpretation — bounded

This slice sharpens one project-wide distinction:

> retention is not merely the survival of a state; it can also require retaining or re-establishing the *right to trust that state*.

For PRAC counters, continued physical bits are insufficient if error detection says the count is corrupt. Conversely, exact historical reconstruction of the count is not always necessary for protection continuity if the system can choose a conservative safe action.

That yields a cautious distinction among:

- **embodiment survival** — some counter bits still physically exist;
- **value integrity** — the count is believed correct or correctable;
- **authority** — the count is permitted to govern mitigation decisions;
- **fallback safety** — the system can remain protective even after exact count authority is lost.

These are project analytical terms, not Intel, AMD, Micron, or JEDEC philosophical vocabulary.

---

## Rejected claims / stop conditions

This slice does **not** establish any of the following:

- Intel's 2021 patent is the direct ancestor of JESD79-5C PRAC;
- AMD's 2024 filing predates or caused the April 2024 PRAC standard publication;
- either patent embodiment shipped in a named commercial product;
- every DDR5 PRAC implementation stores counters in DRAM cells with ECC;
- every PRAC counter error is a DRAM retention failure;
- refresh violation, soft error, logic fault, parity error, and uncorrectable ECC event are physically identical;
- every counter error can be localized to one exact row immediately;
- the PRAC alert signal itself performs mitigation;
- continuing monitoring after an error proves the affected counter is trustworthy;
- disabling monitoring after one error is required by JEDEC;
- `once every 24 hours` is a standard scrub cadence, timeout, or safety deadline;
- conservative victim refresh recovers the lost count value;
- preserving a safe outcome means preserving the same maintenance metadata value;
- Case 45, Case 55, Case 83, and Case 121 share a historical implementation lineage.

---

## Related-repository boundary

A fresh repository search found no dedicated `PRAC` / activation-counter treatment in `tmzncty/computing-archaeology`.

The broader history of RowHammer counter designs, ECC layouts for counter cells, JEDEC committee development, vendor implementation chronology, and controller deployment still belongs primarily there if developed. This file keeps only the retention-specific boundary: **maintenance metadata can lose integrity/authority after initialization, and a protection system can respond by correction, reinitialization, conservative action, or authority handoff rather than pretending the old count remains trustworthy.**

---

## Remaining evidence debt after this slice

This pass closes only the patent-side `counter integrity / error authority` slice. Still open:

- normative JESD79-5C / JESD79-5D clauses for PRAC counter-error reporting, if publicly inspectable under usable terms;
- named shipping DRAM product documentation that exposes PRAC-counter ECC/parity/error behavior;
- named memory-controller behavior after a PRAC-counter error indication;
- independent hardware fault injection into PRAC counter cells or their error path;
- physical distinction among correctable bit errors, retention violations, logic faults, and counter-cell wear/defect mechanisms;
- whether shipping implementations continue or disable counting after particular PRAC error classes;
- cross-vendor ACI/reset/counter-refresh product contracts;
- exact JEDEC proposal/ballot genealogy;
- broader counter-protection history, which remains a `computing-archaeology` task rather than a reason to duplicate generic DRAM history here.
