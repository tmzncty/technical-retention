# Case 38 Grounding Record — Intel DC S3700/S3500 PLI Health, Self-Test, and Validation

## Purpose

This record supports [`cases/38-intel-dc-s3700-pli-self-test-validation.md`](../cases/38-intel-dc-s3700-pli-self-test-validation.md).

The bounded grounding question is:

> Can a named commercial SSD case directly establish that a power-loss retention mechanism has its own monitored health state, recurring self-test, retained event/test history, operator-facing control surface, and manufacturer fault-validation procedure, without confusing those claims with independent compliance evidence?

**Result: yes.** Intel's 2014-era PLI technology brief and January 2015 S3700 Product Specification directly establish the product-level health/test relation. The case is therefore `grounded` for that bounded mechanism.

It remains explicitly **not grounded** for independent fleet-wide fault compliance, complete controller-metadata recovery under every interrupted operation, or filesystem/database durability.

---

## Source set and evidence classes

### Source A — Intel _Power Loss Imminent (PLI) Technology_, document 330275-001US

**Document:** Intel Corporation, _Power Loss Imminent (PLI) Technology_, technology brief, document 330275-001US.

**Dating boundary:** the PDF does not expose a clean publication date on the title page in the inspected copy. Its references state `Sample Pricing: As of February 28, 2014`. This record therefore calls the artifact **2014-era** and does not manufacture a more precise publication date.

**Inspection:** direct Intel-hosted PDF text plus rendered-page inspection.

**Evidence class:** `H/P` — manufacturer-primary named-product / architecture / validation evidence.

**Direct URL:**
<https://www.intel.com/content/dam/www/public/us/en/documents/technology-briefs/ssd-power-loss-imminent-technology-brief.pdf>

#### Source A, pp. 1–2 — failure-time mechanism and lifetime readiness

Directly establishes:

- PLI-enabled SSDs contain energy-storing capacitors;
- a supply-voltage detector monitors the drive;
- when voltage falls below a predefined level, capacitor energy is used to write temporary-buffer state to NAND;
- capacitors recharge after power returns;
- Intel treats periodic verification of PLI circuitry over SSD life as an architectural requirement;
- the S3700/S3500 PLI architecture includes voltage detection, capacitor bank, and SMART attribute extraction;
- administrators can retrieve PLI health/status values.

**Boundary:** this is Intel's own product/technology description. It establishes what Intel documented, not third-party empirical compliance.

#### Source A, p. 4, Table 2 — event state and self-test state

Directly establishes:

- SMART `AEh` = `Unexpected Power Loss`;
- its raw value cumulatively counts unclean shutdowns over drive life;
- Intel says that definition is independent of PLI activity using capacitor power;
- SMART `AFh` = `Power Loss Protection Failure`;
- AFh reports the most recent PLI test through three health-check values;
- the self-test partially discharges the PLI capacitors to test whether they can release/sustain energy as designed;
- for S3700/S3500 Intel specifies a minimum result of 25 µs;
- the drive retains minutes since the last test;
- the drive retains cumulative lifetime test count;
- normalized state distinguishes failure, excessive-temperature test, and ordinary status.

**Rendered-page inspection:** the actual Table 2 layout was visually checked, including the AEh/AFh split and the three AFh output fields.

#### Source A, p. 5 — operator access and test control

Directly establishes:

- Intel SSD Toolbox can display AEh/AFh;
- SCT can manually invoke a capacitor test;
- SCT can set capacitor-test intervals;
- Intel frames the resulting health state as information an administrator can use to take action, including drive replacement before a later power loss compromises data.

**Boundary:** this establishes a management/control surface, not that every deployment used Intel SSD Toolbox or the same operator policy.

#### Source A, p. 6 — validation beyond self-test

Directly establishes that Intel describes a distinct PLI validation problem including:

- PLI circuitry and switch timing;
- rare cases such as power loss during firmware update or secure erase;
- stability after power returns;
- enumeration after the stated recovery interval;
- no data loss for commands acknowledged as complete;
- shorn writes with aligned/unaligned data;
- Intel tooling that tracks the SATA stream, removes power, reinserts the drive, then verifies the intended LBAs;
- Figure 6's test flow repeating 7000 times before pass/fail.

**Rendered-page inspection:** p. 6 and Figure 6 were visually inspected. The repetition count is therefore not taken only from extracted text.

**Boundary:** the flow is manufacturer-described validation. This record does not call it independent certification, an industry standard, or proof that every field unit passes every future waveform/failure state.

#### Source A, p. 7 — named-product applicability

Directly establishes that Intel identifies S3700 and S3500 SATA products as containing enabled PLI hardware and firmware.

---

### Source B — Intel SSD DC S3700 Series Product Specification, January 2015

**Document:** Intel Corporation, _Intel Solid-State Drive DC S3700 Series Product Specification_, January 2015, order 328171-010US.

**Inspection:** direct Intel-hosted PDF text plus rendered-page inspection.

**Evidence class:** `H/P` — manufacturer-primary named-product specification.

**Direct URL:**
<https://www.intel.com/content/dam/www/public/us/en/documents/product-specifications/ssd-dc-s3700-spec.pdf>

#### Source B, feature summary

Directly establishes:

- `Enhanced power-loss data protection` is a named product feature;
- power-loss protection capacitor self-test is a named product capability.

#### Source B, printed pp. 9–10 — power-transition envelope

Directly establishes:

- the documented 5 V, 12 V, and 3.3 V operating-characteristic tables give a minimum fall time of 1 ms;
- note 2 says fall time must meet that minimum to guarantee full functionality of enhanced power-loss management.

**Use in this case:** narrow evidence that the failure contract includes supply-transition timing, not merely the eventual absence of power.

**Boundary:** this does not authorize extrapolating a universal SSD waveform rule or inferring behavior for arbitrary faster/slower/noisy transients beyond the documented contract.

#### Source B, printed p. 13 §2.8 — capacitor test

Directly establishes:

- S3700 supports testing of the power-loss capacitor;
- the result can be monitored through SMART `AFh`.

**Rendered-page inspection:** printed p. 13 was visually checked, including the `Power Loss Capacitor Test` section.

#### Source B, printed p. 21 — SMART event/health semantics

Directly establishes:

- `AEh` Unexpected Power Loss counts unclean shutdowns over SSD life;
- `AFh` Power Loss Protection Failure records last test result in microseconds, minutes since last test, and lifetime number of tests;
- the expected last-test-result range begins at 25 µs;
- the normalized value distinguishes test failure, excessive-temperature testing, and ordinary status.

**Rendered-page inspection:** printed p. 21 was visually checked; the `AEh` and `AFh` rows are independently visible in the SMART table.

---

## Related evidence boundary — Case 15 / FAST '13

Case 15 already uses Zheng et al., FAST '13, as an independent experimental warning that host/interface/manufacturer semantics do not automatically prove correct behavior under injected power faults. The tested SSD identities in that study are anonymized.

For Case 38 this means:

- the FAST '13 study remains relevant to the **methodological distinction** `contract/validation claim ≠ independent compliance evidence`;
- it **must not** be cited as a failure or success test of S3700/S3500;
- Intel's Figure 6 and AFh self-test can be grounded as real manufacturer procedures without being mislabeled independent certification.

No new product attribution is made from the anonymous study.

---

## Grounded mechanism

The combined Intel evidence supports this bounded model:

```text
ordinary service
    │
    ├─ recurring / operator-invoked PLI capacitor self-test
    │       ↓
    │   partial capacitor discharge
    │       ↓
    │   AFh health state
    │   ├─ last discharge result
    │   ├─ minutes since test
    │   └─ lifetime test count / normalized condition
    │       ↓
    │   operator or management decision
    │
    └─ future unexpected power loss
            ↓
        voltage detection + switching
            ↓
        stored capacitor energy
            ↓
        controller-buffer state → NAND

separate event-history state:
AEh = cumulative unclean shutdown count
```

Intel's wider validation flow sits around the second branch rather than being identical to the self-test:

```text
I/O stream → hot-unplug → off interval → reinsert/enumerate
    → verify committed/intended data → repeat → pass/fail
```

---

## Claims strengthened by this slice

### G-38.1 — `retention mechanism presence ≠ retention mechanism readiness`

**Evidence:** Intel describes recurring self-test of the installed PLI capacitor path and a failure state when the discharge test does not satisfy expectations.

**Status:** grounded engineering reconstruction from manufacturer-primary evidence.

### G-38.2 — retention infrastructure can itself require periodic verification

**Evidence:** Intel explicitly says PLI SMART functionality periodically verifies that PLI circuitry continues to function over the life of the SSD.

**Status:** grounded historical/engineering relation.

### G-38.3 — future-fault protection depends on retained management state beyond payload

**Evidence:** AFh retains last discharge result, time since test, and lifetime test count; AEh separately retains unclean-shutdown history.

**Status:** grounded.

### G-38.4 — `power-loss event history ≠ protection-capability health`

**Evidence:** AEh and AFh are separate attributes with different semantics; AEh explicitly counts unclean shutdowns regardless of PLI activity.

**Status:** grounded.

### G-38.5 — `self-test evidence ≠ whole-device power-fault validation`

**Evidence:** Intel documents a partial-discharge self-test separately from a wider validation section covering switching, hot-unplug/reinsertion, data verification, and rare operations.

**Status:** grounded methodological/engineering distinction.

### G-38.6 — automatic monitoring does not remove operator action

**Evidence:** SMART/Toolbox exposes status; SCT permits manual invocation/interval control; Intel explicitly connects the normalized state to administrator replacement decisions.

**Status:** grounded engineering reconstruction.

### G-38.7 — failure semantics can depend on transition shape/timing

**Evidence:** the S3700 Product Specification conditions full enhanced-power-loss-management functionality on meeting the minimum supply fall time.

**Status:** grounded for the named-product contract only.

### G-38.8 — `manufacturer validation ≠ independent compliance evidence`

**Evidence:** Intel provides an explicit validation flow, while the only independent power-fault evidence already used by the repository is anonymized and cannot be assigned to S3700/S3500.

**Status:** grounded evidence-control rule.

### G-38.9 — acknowledged-command durability target ≠ all possible in-flight/higher-layer state

**Evidence:** Intel identifies no-data-loss for commands acknowledged complete as a key validation deliverable while separately discussing shorn/unaligned and reordered write scenarios.

**Status:** grounded as a scope boundary. Do not generalize the manufacturer wording into filesystem/database crash consistency.

---

## Claims deliberately not made

### X-38.1 — “Intel invented PLI / power-loss protection / capacitor backup”

Not established or required.

### X-38.2 — “a passing AFh self-test proves the whole SSD will survive every power failure”

Rejected. The test is a partial-discharge capability probe; Intel separately documents broader validation.

### X-38.3 — “an AFh failure means user data has already been lost”

Rejected. The field reports protection-path health, not a direct payload-loss event.

### X-38.4 — “AEh power-loss count is a count of failed PLI events”

Rejected. Intel explicitly says AEh counts unclean shutdowns regardless of PLI activity.

### X-38.5 — “Intel's 7000-repeat validation flow is independent certification”

Rejected. It is first-party manufacturer documentation of a validation method.

### X-38.6 — “FAST '13 tested or failed the S3700/S3500”

Rejected. Device identities are anonymized.

### X-38.7 — “the S3700 1 ms supply-fall requirement is a universal SSD rule”

Rejected. It is a named-product electrical contract.

### X-38.8 — “PLI proves filesystem/database durability”

Rejected. Higher-layer ordering, atomicity, and recovery semantics remain separate.

---

## Historical record / reconstruction / analogy separation

### Historical record

Direct Intel documents establish the names, products, fields, tests, numeric criteria/ranges, management access, validation flow, and electrical-envelope condition.

### Engineering reconstruction

Project phrases such as `retention-infrastructure readiness`, `future-fault capability`, and `maintenance-of-maintenance` summarize the relation exposed by those mechanisms. They are not period Intel terminology.

### Functional analogy

Comparison with DRAM refresh is restricted to the fact that recurring maintenance can be constitutive of a retention regime. The actual mechanisms are different: DRAM refresh restores payload; PLI self-test checks an exceptional future protection path.

Comparison with ADR/eADR is restricted to stored-energy/failure-triggered-transfer relations. No interface identity or genealogy is claimed.

### Philosophical interpretation

The only bounded interpretive pressure is that future technical availability can depend on retained evidence about the present health of the apparatus that will perform later retention work. No stronger Stiegler/Heidegger claim follows automatically.

---

## Related-repository duplication check

Before writing, `tmzncty/computing-archaeology` was searched for:

- `S3700 PLI power loss capacitor SSD`;
- `power loss protection SSD capacitor`.

No dedicated existing case was found by those searches. The current contribution is therefore limited to the retention-specific health/readiness/validation relation rather than duplicating general SSD history.

---

## Promotion judgment

**Case 38 status: `grounded`.**

Why that status is justified:

- two directly inspected Intel first-party documents independently anchor the named product and capacitor-test control surface;
- the PLI brief exposes exact SMART event/health fields and the self-test mechanism rather than merely advertising `power-loss protection`;
- rendered p. 4 verifies the AFh table and its three retained outputs;
- rendered p. 6 verifies Intel's distinct hot-unplug/data-verification validation workflow and 7000-repeat loop;
- the January 2015 S3700 product spec separately anchors the capacitor-test feature, SMART semantics, and supply-fall envelope;
- invention priority is not claimed;
- manufacturer validation and independent compliance remain separate evidence layers;
- historical record, engineering reconstruction, functional analogy, and philosophical pressure are explicitly separated.

The next useful SSD slice should therefore **not** restate the capacitor mechanism. It should pursue either independent named-product power-fault compliance, controller-metadata recovery under interruption, or higher-layer filesystem/database composition.