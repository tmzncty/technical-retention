# Case 121 — DDR5 PRAC Evidence Index

**Status:** `grounded`

**Canonical case:** [`../cases/121-ddr5-prac-activation-counter-initialization.md`](../cases/121-ddr5-prac-activation-counter-initialization.md)

## Purpose

This index keeps Case 121's evidence layers separate while the case is still being deepened.

The central subject is not merely that DDR5 can count row activations. The retention question is narrower and more demanding:

> when disturbance mitigation depends on per-row activation history, what state must exist, when is that state trustworthy, how is it initialized/reconstituted, how are errors handled, and which technical-document revision defines the contract being asserted?

The evidence currently supports a useful decomposition, but not yet a maturity promotion.

---

## Evidence chain

### 1. Baseline PRAC / activation-counter grounding

[`121-ddr5-2021-2025-prac-activation-counter-grounding.md`](121-ddr5-2021-2025-prac-activation-counter-grounding.md)

Role:

- establishes the baseline DDR5 PRAC / per-row activation-counter mechanism;
- grounds the distinction between useful payload state and maintenance-coordination state;
- records the evidence used for activation counting, mitigation triggering, and counter-related handling;
- separates standards-level evidence from manufacturer/platform evidence.

Core retention relation:

```text
row activations
    -> retained / accumulated activation history
    -> mitigation decision
```

This evidence is the baseline. Later deepenings should not silently overwrite its document epoch.

---

### 2. Power-up / reset / reconstitution boundary

[`121-ddr5-prac-powerup-reset-reconstitution-deepening.md`](121-ddr5-prac-powerup-reset-reconstitution-deepening.md)

Role:

- examines what happens when activation-counter state cannot simply be assumed valid from the beginning of an operating epoch;
- separates physical power-up/reset events from readiness of the disturbance-mitigation state;
- deepens the meaning of activation-counter initialization and re-establishment.

Core boundary:

```text
DRAM powered / reset released
    !=
activation-count state initialized
    !=
PRAC state trustworthy for mitigation
```

This is second-order retention infrastructure: state that helps protect DRAM contents can itself require initialization and validity conditions.

---

### 3. Counter integrity / platform error-handling boundary

[`121-intel-amd-prac-counter-integrity-error-handling-deepening.md`](121-intel-amd-prac-counter-integrity-error-handling-deepening.md)

Role:

- follows the activation-counter integrity problem into platform / processor documentation;
- separates a DRAM-internal maintenance mechanism from platform-visible reaction to counter-related failures;
- records that maintenance metadata can acquire its own error path rather than being treated as infallible hidden state.

Core boundary:

```text
payload ECC / payload error handling
    !=
activation-counter integrity handling
```

and:

```text
maintenance state exists
    !=
maintenance state is valid
    !=
platform knows how to react when it is invalid
```

This evidence should not be back-projected into every DDR5 implementation merely because it appears in named Intel/AMD material.

---

### 4. JESD79-5C → 5C.01 → 5D revision provenance

[`121-jedec-2024-2025-prac-revision-provenance-deepening.md`](121-jedec-2024-2025-prac-revision-provenance-deepening.md)

Role:

- anchors the April 2024 public JESD79-5C PRAC milestone;
- records the July 2024 `JESD79-5C.01_v1.31` identity and its explicit `Editorial Revision` relation to 5C;
- confirms public table-of-contents continuity of the named PRAC Clause 16 architecture through JESD79-5D;
- records the November 2025 JESD79-5D document lineage;
- identifies Annex D / Annex E as the standards-defined loci for revision differences;
- prevents one revision's normative contract from being silently projected into another.

Core provenance boundary:

```text
same feature name across revisions
    !=
same complete normative contract
```

and:

```text
whole-standard revision
    !=
proof of PRAC-specific change
```

This evidence deliberately stops before claiming a clause-by-clause semantic diff.

---

## Current state decomposition

The evidence now supports the following **engineering reconstruction**, not JEDEC terminology:

```text
activation events
    ↓
per-row activation-counter state
    ↓
initialization / readiness / validity
    ↓
alert / back-off / mitigation eligibility
    ↓
mitigation action
    ↓
continued integrity / error handling
```

A separate provenance axis runs alongside that mechanism:

```text
protocol-contract epoch

JESD79-5C
    ↓
JESD79-5C.01
    ↓
JESD79-5D
```

These axes must not be collapsed.

A state-machine claim may be true for one document/product epoch without yet being proven for another.

---

## Evidence-class discipline

### Historical / primary record (`H/P`)

Use for:

- JEDEC publication identity and revision metadata;
- visible standards clause / TOC structure;
- manufacturer product/core-document statements;
- processor/platform documentation;
- dated document lineage.

### Engineering reconstruction (`E`)

Use for project-level decompositions such as:

```text
state exists
    !=
state initialized
    !=
state trustworthy
    !=
state sufficient to authorize mitigation
```

or:

```text
mechanism epoch
    !=
evidence epoch
```

These relations help compare cases but are not quotations from JEDEC, Micron, Intel, AMD, or another vendor.

### Functional analogy (`A`)

A bounded analogy to firmware/schema versioning is acceptable:

```text
same named field / feature across versions
    !=
same complete contract
```

No implementation genealogy is implied.

### Philosophical interpretation (`V`)

The project may observe that maintenance continuity depends not only on retained bits but on the continued validity of the rules that interpret those bits.

That interpretation must remain explicitly project-level and must not be attributed to standards authors.

---

## Current cross-case comparisons

### Case 43 — AVATAR RRT self-protection

Functional comparison only:

```text
Case 43:
refresh-policy metadata can itself require protection

Case 121:
activation-history metadata can itself require initialization / integrity handling
```

Shared abstraction:

```text
maintenance metadata
    is itself part of the protected operational state
```

Different mechanisms and historical lineages; no genealogy is claimed.

### Case 111 — SSD firmware refresh-policy versioning

Functional comparison only:

```text
Case 111:
same product family + different firmware revision
    -> implementation epoch may change maintenance behavior

Case 121:
same PRAC feature family + different JEDEC revision
    -> normative-contract epoch may change what can safely be asserted
```

Shared methodological point:

> technical claims should be version-bounded.

A firmware revision and a standards revision are not equivalent historical objects.

---

## Current conclusions that are safe

1. PRAC makes activation-history state part of the disturbance-mitigation control path.
2. The existence of a counter is not enough; initialization/readiness matters.
3. Maintenance-coordination state can require its own integrity/error path.
4. Power/reset state and maintenance-state readiness must be distinguished.
5. JEDEC publicly introduced named PRAC in the 2024 JESD79-5C publication epoch.
6. JESD79-5C.01 identifies itself as an editorial revision of 5C and retains the named PRAC Clause 16 architecture at public-TOC level.
7. JESD79-5D retains a named PRAC Clause 16 architecture and provides an informative revision-difference annex against 5C.01.
8. None of those facts alone proves that every PRAC timing, MR definition, error rule, initialization rule, or reset semantic is identical across 5C, 5C.01, and 5D.
9. Manufacturer documents and JEDEC revisions are separate evidence axes.
10. Case 121 therefore remains `grounded` rather than promoted.

---

## Explicit guardrails

Do not infer any of the following from the current evidence:

- PRAC is enabled or implemented identically in every DDR5 device;
- every DDR5 product exposes the same counter-error behavior;
- Micron product documentation is a substitute for the complete JEDEC normative standard;
- Intel/AMD platform documentation defines universal DRAM behavior;
- `Editorial Revision` proves byte-identical text;
- unchanged PRAC section titles prove unchanged requirements;
- a newer JEDEC edition proves PRAC changed;
- absence of a public delta proves PRAC did not change;
- activation-counter initialization is equivalent to physical DRAM power-up;
- successful payload access proves PRAC counter state is valid;
- maintenance-state loss necessarily means payload loss has already occurred;
- a maintenance-state error path establishes a particular die-level implementation;
- a standard revision establishes a product firmware or silicon revision;
- standards lineage establishes invention priority;
- platform support establishes that every installed DIMM uses the feature.

---

## Remaining evidence debt

The broad `revision-by-revision PRAC changes` debt is now narrowed to concrete work:

1. inspect JESD79-5C.01 **Annex D** and record whether any 5C→5C.01 difference touches PRAC text, tables, cross-references, timing, mode registers, reset, or error handling;
2. inspect JESD79-5D **Annex E** and extract only PRAC-relevant 5D→5C.01 deltas;
3. compare the affected Clause 16 / MR / timing tables directly under lawful full-text access rather than inferring deltas from page numbers or section titles;
4. keep ACI/reset/counter-error claims explicitly revision-scoped until those comparisons are complete;
5. map public manufacturer document revisions to the JEDEC edition(s) they explicitly claim to implement or support;
6. broaden named-vendor evidence beyond the current Micron / Intel / AMD set where suitable public primary material exists;
7. find named DIMM/platform documentation showing reset, reboot, suspend, or replacement behavior around PRAC/ACI state where exposed;
8. treat committee proposal genealogy / invention priority as a separate historical task rather than deriving it from publication order;
9. if testing is feasible later, distinguish specified reset semantics from measured state behavior on a named platform.

The next standards slice should therefore be **Annex D / Annex E PRAC delta extraction**, not another general DDR5 overview.

---

## Related-repository check

A repository search of `tmzncty/computing-archaeology` for `JESD79-5C PRAC Per-Row Activation Counting` found no dedicated reusable packet in this round.

Division of labor remains:

- `technical-retention`: activation-history state, initialization/readiness, error handling, revision-bounded retention contract, and cross-case comparison;
- `computing-archaeology`: broader JEDEC committee genealogy, proposal/ballot history, vendor adoption chronology, and platform evolution if those become dedicated research topics.

This index should link to companion research if such a packet appears later rather than duplicating it.

---

## Maturity

**Current maturity: `grounded`.**

No promotion is justified in this round.

The revision-provenance evidence is substantially better than before, but the actual 5C.01→5D PRAC normative delta has not yet been inspected directly, and named cross-vendor/platform coverage remains incomplete.

`CASE_INDEX.md` on the current repository branch is presently empty; this index therefore records the local Case 121 maturity state without attempting to reconstruct or repopulate the global case ledger automatically.
