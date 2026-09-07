# DDR5 PRAC Activation-Counter Initialization: Volatile Maintenance Metadata and Protection Readiness

## Status

**`grounded`** — bounded to the public 2024–2025 DDR5 Per-Row Activation Counting (`PRAC`) / Activation Counter Initialization (`ACI`) contract. The case uses JEDEC's 17 April 2024 publication announcement, Micron's manufacturer DDR5 core documentation (Rev. E, 11/2024), a 2021 Intel per-row-count patent as a prior-art floor, a later Micron ACI patent disclosure, and independent 2025 hardware/architecture work.

Grounding record: [`../evidence/121-ddr5-2021-2025-prac-activation-counter-grounding.md`](../evidence/121-ddr5-2021-2025-prac-activation-counter-grounding.md).

This is a retention-specific continuation of [`54-ddr5-rfm-split-maintenance-authority.md`](54-ddr5-rfm-split-maintenance-authority.md), not a replacement for it. Case 54 asks who owns activity accounting and creates an RFM maintenance opportunity. Case 121 asks a different question: **what has to be retained before per-row activation accounting itself can be trusted?**

## Scope

JEDEC announced JESD79-5C on 17 April 2024 and described PRAC as wordline-granular activation counting coordinated between DRAM and the system. Micron's later public DDR5 core documentation exposes an especially useful implementation contract: PRAC/Alert Back-Off (`ABO`) is optional, disabled by default, and does not begin counting or issuing ABO until a full-array activation-counter initialization completes.

The same Micron document then states something unusually important for this repository: the activation-counter bits themselves require refresh like normal device cells. If their refresh requirements are violated, the counters can no longer be treated as known state and ACI must establish a new known starting condition.

This case therefore asks:

> What changes when the metadata used to decide whether retention-protection work is due is itself volatile retained state with its own initialization, refresh, validity, and transition requirements?

This case is **not**:

- a complete history of JESD79-5C or later DDR5 revisions;
- a universal claim that every DDR5 device implements PRAC;
- a security proof that PRAC/ABO prevents all RowHammer patterns;
- a reconstruction of one vendor's hidden victim-row-selection algorithm;
- a complete treatment of RFM, ARFM, DRFM, or PRAC mitigation scheduling;
- a claim that the physical counter-cell topology described by one product/patent is universal;
- a claim that activation counters are an archival access log;
- an empirical fault-injection demonstration of counter corruption.

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

### Earlier prior art: per-row activation-count state predates JESD79-5C

Intel's US20210365316A1, filed 4 June 2021 and published 25 November 2021, describes a memory chip in which storage cells associated with a row hold that row's activation count, with ECC protecting the count, comparison against a threshold, and increment/writeback circuitry.

Therefore:

> **JESD79-5C PRAC ≠ invention of per-row activation-count state.**

This patent is a prior-art/mechanism floor, not proof that its exact design became JEDEC PRAC or that there is a demonstrated Intel→JEDEC implementation genealogy.

## Retained states and relations

The bounded PRAC/ACI regime contains at least these distinct states:

1. **DRAM payload charge** — the application data whose integrity is ultimately protected;
2. **per-row activation-count state** — maintenance metadata summarizing activity pressure;
3. **counter validity/readiness** — whether those count bits are known enough to be used;
4. **PRAC enable state** — host-visible policy enabling PRAC/ABO;
5. **ACI in-progress state** — a transition regime in which counters are being established;
6. **ACI-complete evidence** — the status that permits the host to finish the handoff;
7. **ABO state** — the device-to-system request path that can demand mitigation time;
8. **ordinary refresh state** — the maintenance regime that preserves volatile payload and counter cells themselves;
9. **mitigation/RFM state** — the later work that an alert can cause, handled more fully in Case 54.

Only item 1 is user payload. Items 2–8 are **retention infrastructure and control state**, but several of them must themselves be retained or re-established before they can protect item 1.

## Engineering reconstruction

### PRAC enabled ≠ protection ready

Micron separates feature enablement from counter initialization and completion. The device does not count activations or issue ABO until ACI has completed.

Therefore:

> **PRAC enabled ≠ activation counters initialized ≠ ABO protection active.**

This is a transition-readiness relation, not merely a mode bit. A system can have selected the PRAC policy while the state required to execute that policy is not yet trustworthy.

### Maintenance metadata is itself volatile

Micron explicitly says activation-counter bits require refresh like normal device cells.

Therefore:

> **payload volatility ≠ maintenance-metadata nonvolatility.**

and more strongly:

> **retention infrastructure can itself require retention work.**

The counter is not outside the physical problem it helps manage. The device has created a second retained state whose survival matters because later protection decisions depend on it.

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

### Maintenance-metadata relevance is conditional on payload continuity

Micron's documentation says that after a refresh violation, array data can also be corrupted and previous activation-counter values become irrelevant.

That creates a useful boundary:

> **retaining maintenance history is useful only while the state to which that history applies remains an admissible continuation.**

If the old payload itself is no longer valid, preserving the exact previous activation-pressure count does not automatically restore that lost payload or make the old counter history operationally authoritative.

### Hidden metadata is not free metadata

Micron says PRAC adds counter cells per row and updates them through a read-modify-write operation (`ACU`), changing core timing parameters. Independent 2025 hardware work likewise observes PRAC's timing effects on real systems.

Therefore:

> **interface-hidden maintenance metadata ≠ zero-cost maintenance metadata.**

A state can be invisible to ordinary software yet consume array area, update time, refresh obligation, and service margin.

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

Intel's 2021 prior-art patent protects row activation-count values with ECC. That is useful evidence that maintenance metadata can itself need integrity protection. It is not evidence that payload ODECC and PRAC counter protection are the same state or same contract.

## Failure and forgetting boundaries

A bounded PRAC system can fail even before discussing the hidden victim-refresh algorithm:

- PRAC support exists but is not enabled;
- PRAC is enabled but ACI is incomplete;
- refresh of activation-counter state is violated and counters become unknown;
- ACI completion/status is mishandled by the host;
- counter update/read-modify-write timing is not correctly composed with memory service;
- ABO is unavailable until counter state is ready;
- a system treats `PRAC present` as proof of complete RowHammer immunity;
- a researcher treats per-row counts as a complete access-history archive.

The key retention failure is therefore not only `payload charge leaked`. It can be:

> **the system lost or never established trustworthy second-order state needed to know when protection work is owed.**

## Prior art and anti-anachronism

The safe historical claims are deliberately narrow:

- **17 April 2024:** JEDEC publicly announces JESD79-5C and PRAC as a named DDR5 feature;
- **November 2024:** Micron Rev. E product documentation publicly exposes the PRAC/ACI/ABO contract used in this case;
- **2021:** Intel already has a filed/public per-row activation-count design, so 2024 cannot safely be called the invention of per-row counting;
- **2025:** Micron's ACI patent disclosure independently documents the need to initialize unknown activation-count state and the host/device handoff.

This does **not** establish the first-ever row counter, the full JEDEC committee genealogy, or direct descent from the Intel patent into JESD79-5C.

## Philosophical interpretation — bounded

Case 121 provides a compact counterexample to the idea that maintenance metadata sits outside the material conditions it governs.

A per-row activation counter can be second-order state: it is not the user bit, but later decisions about whether that user bit needs disturbance mitigation depend on the counter. Yet the counter is itself embodied in volatile state, needs refresh, has an initialization history, can lose validity, and can require re-establishment before it is allowed to govern future work.

A cautious formulation is therefore:

> technical retention may depend on retained descriptions of prior stress, while those descriptions have their own retention and validity conditions.

That is an engineering-derived interpretation. It is not historical JEDEC or Micron vocabulary, and it does not imply that every controller counter or health statistic should be called `memory` in the same philosophical sense.

## Open evidence debt

- exact JESD79-5C committee/proposal genealogy before the April 2024 publication;
- revision-by-revision PRAC changes after JESD79-5C;
- cross-vendor product contracts for ACI/counter refresh;
- exact physical counter-cell topology across named DDR5 parts;
- power-cycle/reset semantics beyond the bounded public product contract;
- independent fault injection that deliberately corrupts/invalidates activation-counter state;
- PRAC + ARFM/DRFM interaction on named controllers and DRAMs;
- full security evaluation of ABO/RFM implementations;
- broader history of per-row activation counting, which belongs primarily in `computing-archaeology`.
