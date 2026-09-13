# DDR5 PRAC Activation-Counter Initialization: Volatile Maintenance Metadata and Protection Readiness

## Status

**`grounded`** — bounded to the public 2024–2025 DDR5 Per-Row Activation Counting (`PRAC`) / Activation Counter Initialization (`ACI`) contract. The case uses JEDEC's 17 April 2024 publication announcement, Micron's manufacturer DDR5 core documentation (Rev. E, 11/2024), a 2021 Intel per-row-count patent as a prior-art floor, a later Micron ACI patent disclosure, independent 2025 hardware/architecture work, and a bounded Intel/AMD patent-side deepening of activation-counter integrity/error handling.

Grounding record: [`../evidence/121-ddr5-2021-2025-prac-activation-counter-grounding.md`](../evidence/121-ddr5-2021-2025-prac-activation-counter-grounding.md).

Reset/power-up deepening: [`../evidence/121-ddr5-prac-powerup-reset-reconstitution-deepening.md`](../evidence/121-ddr5-prac-powerup-reset-reconstitution-deepening.md).

Counter-integrity/error-authority deepening: [`../evidence/121-intel-amd-prac-counter-integrity-error-handling-deepening.md`](../evidence/121-intel-amd-prac-counter-integrity-error-handling-deepening.md).

This is a retention-specific continuation of [`54-ddr5-rfm-split-maintenance-authority.md`](54-ddr5-rfm-split-maintenance-authority.md), not a replacement for it. Case 54 asks who owns activity accounting and creates an RFM maintenance opportunity. Case 121 asks a different question: **what has to be retained before per-row activation accounting itself can be trusted?**

## Scope

JEDEC announced JESD79-5C on 17 April 2024 and described PRAC as wordline-granular activation counting coordinated between DRAM and the system. Micron's later public DDR5 core documentation exposes an especially useful implementation contract: PRAC/Alert Back-Off (`ABO`) is optional, disabled by default, and does not begin counting or issuing ABO until a full-array activation-counter initialization completes.

The same Micron document then states something unusually important for this repository: the activation-counter bits themselves require refresh like normal device cells. If their refresh requirements are violated, the counters can no longer be treated as known state and ACI must establish a new known starting condition.

The later Intel/AMD error-handling deepening adds a second validity axis. Even after initialization, activation-count state may require ECC/error detection; if exact count state becomes uncorrectable, a design can conservatively mitigate, signal the host, continue monitoring under policy, or revoke monitoring rather than pretending the old value remains authoritative.

This case therefore asks:

> What changes when the metadata used to decide whether retention-protection work is due is itself volatile retained state with its own initialization, refresh, integrity, validity, and transition requirements?

This case is **not**:

- a complete history of JESD79-5C or later DDR5 revisions;
- a universal claim that every DDR5 device implements PRAC;
- a security proof that PRAC/ABO prevents all RowHammer patterns;
- a reconstruction of one vendor's hidden victim-row-selection algorithm;
- a complete treatment of RFM, ARFM, DRFM, or PRAC mitigation scheduling;
- a claim that the physical counter-cell topology described by one product/patent is universal;
- a claim that activation counters are an archival access log;
- an empirical fault-injection demonstration of counter corruption;
- a claim that patent embodiments from Intel or AMD are normative JEDEC rules or shipping-product contracts.

## Historical record

### 17 April 2024: JESD79-5C publicly introduces PRAC

JEDEC's publication announcement for JESD79-5C says PRAC counts DRAM activations at wordline granularity. When a PRAC-enabled DRAM detects excessive activation, it alerts the system so traffic can be paused and time designated for mitigation.

That establishes a 2024 standards-publication floor for **PRAC as the named DDR5 feature**. It does not establish invention priority for per-row activation counters in general.

### November 2024: Micron exposes the PRAC/ACI product contract

Micron's `DDR5 SDRAM Core Data Sheet`, Rev. E (11/2024), identifies `MR70` as `PRAC, ABO`. Its register table separates:

- PRAC/ABO support (`OP[0]`);
- PRAC/ABO enable (`OP[1]`), disabled by default;
- Activation Counter Initialization mode (`OP[2]`);
- ACI completion (`OP[3]`);
- the ABO-source flag (`OP[5]`).

The PRAC section further states that once PRAC is enabled, a full-array ACI shall be performed. Until the activation-counter bits are initialized, the device does **not** track activation counts and does **not** issue ABO.

The initialization sequence uses a full refresh pass under a restricted command regime, exposes completion status, and only then begins normal activation counting.

Most importantly for this case, Micron states that the activation-counter bits require refresh like normal device cells. After refresh violations, ACI is required to put those bits back into a known state.

### Power-up / system-reset reconstitution deepening

A later bounded pass adds a reset/power-up distinction that the original grounding left open. Micron Rev. E (11/2024) states that a system reset which disables PRAC also clears ACI-completion status (`MR70:OP[3]=0`). That is a product-contract statement about readiness/control state; it does not establish that reset physically erases the activation-counter cells themselves.

Micron's later ACI patent application, US20250316301A1 (published 9 October 2025), separately describes power-up as a condition in which activation-counter bits may be unknown and therefore require initialization to a known state before reliance. Because this is a patent embodiment rather than an inspected normative JEDEC clause, it is used only as a primary mechanism witness, not as a universal DDR5 rule.

Evidence: [`../evidence/121-ddr5-prac-powerup-reset-reconstitution-deepening.md`](../evidence/121-ddr5-prac-powerup-reset-reconstitution-deepening.md).

### Earlier prior art: per-row activation-count state predates JESD79-5C

Intel's US20210365316A1, filed 4 June 2021 and published 25 November 2021, describes a memory chip in which storage cells associated with a row hold that row's activation count, with ECC protecting the count, comparison against a threshold, and increment/writeback circuitry.

Therefore:

> **JESD79-5C PRAC ≠ invention of per-row activation-count state.**

This patent is a prior-art/mechanism floor, not proof that its exact design became JEDEC PRAC or that there is a demonstrated Intel→JEDEC implementation genealogy.

### 2021–2025 patent-side integrity/error handling deepening

The same Intel disclosure also matters for a different reason: it treats the count as error-protected maintenance metadata. Correctable count/ECC errors can be repaired in the ECC path; one described response to an uncorrectable count is to pessimistically act as though the row may already be near threshold and refresh possible victim rows rather than claim the exact count has been recovered.

AMD's US20250383947A1, filed 17 June 2024 and published 18 December 2025, is later than the public JESD79-5C PRAC announcement. It therefore is not used as PRAC invention prior art. Its narrower contribution is a PRAC-specific error path: detect a PRAC-counter error, route it to alert logic for prompt host notification rather than waiting for a later scrub, and permit embodiments that continue or disable PRAC monitoring according to policy.

Evidence: [`../evidence/121-intel-amd-prac-counter-integrity-error-handling-deepening.md`](../evidence/121-intel-amd-prac-counter-integrity-error-handling-deepening.md).

This establishes a further boundary:

> **counter initialized ≠ counter guaranteed trustworthy forever.**

and:

> **counter-error detection ≠ exact count recovery ≠ mitigation ≠ host notification.**

## Retained states and relations

The bounded PRAC/ACI regime contains at least these distinct states:

1. **DRAM payload charge** — the application data whose integrity is ultimately protected;
2. **per-row activation-count state** — maintenance metadata summarizing activity pressure;
3. **counter validity/readiness** — whether those count bits are known enough to be used after initialization/refresh-regime transitions;
4. **counter integrity/error state** — whether an operational count is believed correct/correctable, detected as faulty, or no longer safely usable as an exact value;
5. **PRAC enable state** — host-visible policy enabling PRAC/ABO;
6. **ACI in-progress state** — a transition regime in which counters are being established;
7. **ACI-complete evidence** — the status that permits the host to finish the handoff;
8. **ABO state** — the device-to-system request path that can demand mitigation time;
9. **ordinary refresh state** — the maintenance regime that preserves volatile payload and counter cells themselves;
10. **mitigation/RFM state** — the later work that an alert can cause, handled more fully in Case 54;
11. **counter-error reporting/authority state** — the later decision about whether to correct, conservatively act, notify the host, continue monitoring, or revoke monitoring after the count itself is suspect.

Only item 1 is user payload. Items 2–11 are **retention infrastructure and control state**, but several of them must themselves be retained, checked, or re-established before they can protect item 1.

## Engineering reconstruction

### PRAC enabled ≠ protection ready

Micron separates feature enablement from counter initialization and completion. The device does not count activations or issue ABO until ACI has completed.

Therefore:

> **PRAC enabled ≠ activation counters initialized ≠ ABO protection active.**

This is a transition-readiness relation, not merely a mode bit. A system can have selected the PRAC policy while the state required to execute that policy is not yet trustworthy.

### Reset can invalidate counter authority without proving physical erasure

The reset path exposes a useful distinction among embodiment, readiness, and authority. Clearing ACI-completion state means the old trusted-counter relation does not transparently survive the transition. The inspected product text does not say that the counter cells are physically erased by that reset.

Therefore:

> **ACI-complete cleared ≠ activation-counter cells physically erased.**

and:

> **possible physical survival ≠ post-reset protocol authority.**

The later patent's power-up path reinforces the reconstitution boundary: counter values may be unknown, and the safe response is to establish a known starting condition through ACI rather than to assume that old values remain trustworthy.

> **counter reinitialization ≠ recovery of previous activation history.**

This gives the PRAC maintenance-control state a bounded persistence horizon: its authority can end at a reset/power-up regime boundary even though the protection mechanism can become usable again after explicit reinitialization. It is therefore not a durable-checkpoint contract.

### Maintenance metadata is itself volatile

Micron explicitly says activation-counter bits require refresh like normal device cells.

Therefore:

> **payload volatility ≠ maintenance-metadata nonvolatility.**

and more strongly:

> **retention infrastructure can itself require retention work.**

The counter is not outside the physical problem it helps manage. The device has created a second retained state whose survival matters because later protection decisions depend on it.

### Initialized and refreshed ≠ necessarily error-free

The Intel/AMD error-handling disclosures add an integrity dimension that ACI alone does not close. A count can be operationally initialized yet later be detected as corrupt or uncorrectable.

Therefore:

> **counter readiness ≠ counter integrity.**

and:

> **refresh-valid lifetime ≠ ECC/parity validity.**

A refresh violation and a detected counter error can both remove trust from activation-count state, but the inspected evidence does not justify treating their physical causes or recovery paths as identical.

### Exact count recovery is not the only way to preserve protection

Intel's bounded embodiment permits correctable count errors to be repaired, but treats an uncorrectable count conservatively by triggering victim-row mitigation as though the true count could already be near the threshold.

Therefore:

> **fail-safe mitigation ≠ recovery of the previous activation count.**

A system can retain the *safety obligation* while deliberately giving up precision about the exact maintenance-history summary that produced it.

AMD's later disclosure adds a different response: quickly notify the host that counter authority is in question, with embodiments that either continue or disable monitoring.

> **error notification ≠ counter repair ≠ RowHammer mitigation.**

### Counter refresh ≠ payload refresh, even if both use volatile cells

The payload and the activation count answer different questions:

```text
payload cell state
    -> what value should a later read return?

activation-count state
    -> how much relevant activation pressure has accumulated?
```

Both may rely on refresh, but refreshing one class of bits does not make the classes semantically interchangeable.

> **same volatility class ≠ same retained object.**

### ACI is not a preservation operation for pre-existing payload

Micron's PRAC text states that during ACI the device does not need to refresh the main array and previously written data may be corrupted. It also requires ACI after operations such as MBIST/mPPR before data is rewritten.

Therefore:

> **initializing protection metadata ≠ preserving existing payload.**

ACI establishes trustworthy future counter state. It must not be described as a transparent in-place repair pass that preserves whatever application data happened to be present before entry.

### Loss of counter history can invalidate protection state without being an archive loss

When refresh requirements for activation counters are violated, old counts are no longer trustworthy and ACI replaces them with a known starting condition.

This is a form of deliberate forgetting, but not loss of a complete access log:

> **activation-count state ≠ complete activation history.**

A count retains only the summary needed by the protection mechanism. It discards ordering, timing, and identities of other accesses that a forensic trace would require.

The counter-error deepening adds a second route to the same authority boundary: an exact summary may become uncorrectable, yet a design can preserve safety by pessimistically mitigating rather than reconstructing the lost exact value.

### Maintenance-metadata relevance is conditional on payload continuity

Micron's documentation says that after a refresh violation, array data can also be corrupted and previous activation-counter values become irrelevant.

That creates a useful boundary:

> **retaining maintenance history is useful only while the state to which that history applies remains an admissible continuation.**

If the old payload itself is no longer valid, preserving the exact previous activation-pressure count does not automatically restore that lost payload or make the old counter history operationally authoritative.

### Hidden metadata is not free metadata

Micron says PRAC adds counter cells per row and updates them through a read-modify-write operation (`ACU`), changing core timing parameters. Independent 2025 hardware work likewise observes PRAC's timing effects on real systems.

Therefore:

> **interface-hidden maintenance metadata ≠ zero-cost maintenance metadata.**

A state can be invisible to ordinary software yet consume array area, update time, refresh obligation, integrity machinery, and service margin.

## Relation to neighboring cases

### Case 03 — ordinary DRAM refresh

Case 03 grounds periodic restoration of volatile payload state. Case 121 adds a later control layer in which **the metadata used to decide extra disturbance-protection work is also volatile**.

> **payload restoration ≠ protection-metadata preservation.**

### Case 54 — DDR5 RFM split authority

Case 54's bounded RFM interface permits controller-side rolling activation accounting and controller-issued RFM. PRAC adds a different coordination path: precise per-row counting resides in the DRAM and the DRAM can alert the system when mitigation time is needed.

The useful comparison is functional:

> **controller-maintained activity budget ≠ in-DRAM per-row activation-count state.**

No claim of a single linear mechanism evolution is required.

### Case 118 — Directed Refresh Management

Case 118 asks which physical-neighbor rows are refreshed around a sampled address. Case 121 asks whether the activity-accounting state used to request mitigation is initialized and valid.

> **counter validity ≠ mitigation-target geometry.**

### Cases 40/43 — retention profiling

RAIDR/AVATAR retain profile/error information that influences future refresh policy. PRAC retains activation-pressure state for disturbance management. They are all second-order retention states, but have different inputs, update rules, lifetimes, and historical lineages.

### Case 45 — on-die ECC/ECS

Intel's 2021 prior-art patent protects row activation-count values with ECC. The new error-path deepening makes the boundary explicit: ECC/error handling can be applied to the **maintenance metadata that governs disturbance protection**, not only to application payload.

> **payload ECC state ≠ protection-counter integrity state.**

That is a functional comparison. It is not evidence that payload ODECC and PRAC counter protection share one physical code layout or implementation genealogy.

## Failure and forgetting boundaries

A bounded PRAC system can fail even before discussing the hidden victim-refresh algorithm:

- PRAC support exists but is not enabled;
- PRAC is enabled but ACI is incomplete;
- refresh of activation-counter state is violated and counters become unknown;
- a counter is initialized but later suffers a correctable or uncorrectable integrity error;
- counter-error detection occurs without immediate exact localization;
- a host is notified of a counter fault but no repair/mitigation policy is correctly executed;
- monitoring continues even though the affected counter state should no longer govern decisions;
- monitoring is disabled without an appropriate fallback protection regime;
- ACI completion/status is mishandled by the host;
- counter update/read-modify-write timing is not correctly composed with memory service;
- ABO is unavailable until counter state is ready;
- a system treats `PRAC present` as proof of complete RowHammer immunity;
- a researcher treats per-row counts as a complete access-history archive.

The key retention failure is therefore not only `payload charge leaked`. It can be:

> **the system lost, never established, or can no longer justify trusting the second-order state needed to know when protection work is owed.**

## Prior art and anti-anachronism

The safe historical claims are deliberately narrow:

- **4 June 2021:** Intel files an ECC-protected per-row activation-count design, including a conservative response to an uncorrectable count;
- **17 April 2024:** JEDEC publicly announces JESD79-5C and PRAC as a named DDR5 feature;
- **17 June 2024:** AMD files a later PRAC-specific counter-error handling application; this is after the public JESD79-5C announcement and is not used as PRAC invention prior art;
- **November 2024:** Micron Rev. E product documentation publicly exposes the PRAC/ACI/ABO contract used in this case;
- **2025:** Micron's ACI patent disclosure independently documents the need to initialize unknown activation-count state and the host/device handoff;
- **18 December 2025:** AMD's PRAC counter-error handling application is published, providing a primary public witness for immediate counter-error notification and alternative continue/disable-monitoring responses.

This does **not** establish the first-ever row counter, the full JEDEC committee genealogy, direct descent from the Intel patent into JESD79-5C, direct descent from JEDEC into the AMD application, or shipping implementation of either patent embodiment.

## Philosophical interpretation — bounded

Case 121 provides a compact counterexample to the idea that maintenance metadata sits outside the material conditions it governs.

A per-row activation counter can be second-order state: it is not the user bit, but later decisions about whether that user bit needs disturbance mitigation depend on the counter. Yet the counter is itself embodied in volatile state, needs refresh, has an initialization history, can lose validity, can suffer integrity errors, and can require re-establishment or an authority fallback before it is allowed to govern future work.

The error-handling deepening adds one further distinction:

> **technical retention may depend not only on keeping state, but on retaining or re-establishing justified trust in that state.**

Exact historical precision is also not always necessary for safety. If an uncorrectable count is conservatively treated as dangerous, protection continuity can survive even though the exact prior count no longer does.

That is an engineering-derived interpretation. It is not historical JEDEC, Intel, AMD, or Micron vocabulary, and it does not imply that every controller counter or health statistic should be called `memory` in the same philosophical sense.

## Open evidence debt

- exact JESD79-5C committee/proposal genealogy before the April 2024 publication;
- revision-by-revision PRAC changes through JESD79-5D;
- cross-vendor **product** contracts for ACI/counter refresh and PRAC-counter error reporting (the new Intel/AMD comparison is patent-side only);
- exact physical counter-cell/ECC topology across named DDR5 parts;
- direct normative JEDEC reset/power-up and counter-error semantics, where publicly inspectable;
- named-controller reset → enable → ACI → completion → ABO and counter-error traces;
- independent fault injection that deliberately corrupts/invalidates activation-counter state or exercises the error-report path;
- PRAC + ARFM/DRFM interaction on named controllers and DRAMs;
- full security evaluation of ABO/RFM implementations;
- broader history of per-row activation counting and counter-protection designs, which belongs primarily in `computing-archaeology`.
