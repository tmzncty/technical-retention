# Intel DC S3700/S3500 PLI Self-Test: Retention-Infrastructure Health, Fault Validation, and Readiness State

## Scope

- **Bounded period:** Intel's 2014-era _Power Loss Imminent (PLI) Technology_ brief (document 330275-001US; its references preserve sample pricing dated 28 February 2014) and the January 2015 Intel SSD DC S3700 Series Product Specification, order 328171-010US.
- **Named products:** Intel SSD DC S3700 Series and S3500 Series where the PLI brief addresses both; product-specification claims are restricted to the S3700 where that is the inspected source.
- **Primary sources:** Intel manufacturer documentation, directly inspected as PDF text and rendered pages.
- **Research question:** when a future power-loss survival path depends on capacitors, switching, firmware, and NAND transfer, what state and verification work must itself be retained so that the protection mechanism is still trustworthy when the power-fail event arrives?

This case does **not** repeat Case 15's Intel SSD 320 mechanism history. Case 15 establishes the basic controller-mediated durability handoff: volatile temporary state can sit in front of nonvolatile NAND, and stored capacitor energy can fund emergency transfer after external power begins to disappear. The present case asks a later and narrower question:

> **How is the health of that retention infrastructure itself made operationally visible, periodically tested, and qualified?**

It is also not independent fault-injection certification of Intel products. Intel's documents are first-party evidence for the product contract, telemetry, self-test, and validation method Intel described. The independent FAST '13 evidence already bounded in Case 15 remains the methodological warning that a manufacturer/interface claim and measured implementation compliance are different evidence classes.

---

## Historical vocabulary

The inspected Intel sources themselves use:

- `Power Loss Imminent (PLI)`;
- `Enhanced power-loss data protection`;
- `Power Loss Capacitor Test`;
- `SMART`;
- `SCT` / `SMART Command Transport`;
- SMART attribute `AEh` — `Unexpected Power Loss`;
- SMART attribute `AFh` — `Power Loss Protection Failure`;
- `Microseconds to Discharge Capacitors`;
- `Minutes since last test`;
- `Lifetime number of tests`;
- `self-test`;
- `shorn writes`;
- `unserialized writes`;
- `validation`;
- `STANDBY IMMEDIATE`;
- `temporary buffers`;
- `NAND Flash`.

The following are **project engineering terms**, not historical Intel vocabulary:

- `retention-infrastructure readiness`;
- `protection-path health`;
- `future-fault capability`;
- `readiness state`;
- `qualification closure`;
- `maintenance-of-maintenance`.

That distinction matters. Intel documents a capacitor test and PLI health telemetry. The repository may reconstruct those as retained state about the ability to retain other state, but it must not pretend Intel framed the feature philosophically as a system “remembering how to remember.”

---

## Historical record

### H/P — PLI is a failure-triggered transfer path, but Intel also treats its future readiness as a design problem

Intel's PLI brief describes PLI-enabled SSDs as containing energy-storing capacitors. A voltage detector monitors the drive supply; when voltage falls below a predefined level, capacitor energy is used so temporary-buffer state can be written to nonvolatile NAND. After normal power returns, the capacitors recharge for a future event.

The same brief then moves beyond the emergency transfer itself. Intel says an important architectural requirement is to monitor PLI health, performance, and usage count, and that SMART functionality is incorporated to **periodically verify that the PLI circuitry continues to function properly over the life of the SSD**.

That is the key historical fact for this case. A retention path is not treated as timelessly trustworthy merely because its capacitors and switches were installed at manufacture.

**Primary anchors:** Intel 330275-001US, pp. 1–2, especially the sections `PLI Technology Details`, `Architecting and Implementing PLI Technology Solution into a Solid-State Drive`, and `PLI Technology Architecture`.

### H/P — S3700/S3500 expose power-loss event history separately from PLI-capability health

Intel's PLI brief identifies two SMART attributes for the DC S3700 and S3500:

- `AEh`, `Unexpected Power Loss`, whose raw value counts unclean shutdowns over drive life. Intel explicitly says this count is independent of whether the PLI capacitor path was active.
- `AFh`, `Power Loss Protection Failure`, which reports information about the most recent PLI self-test and PLI-capacitor health.

The January 2015 S3700 Product Specification preserves the same distinction in its SMART table. The event count and the health/test record are therefore not one statistic.

```text
history of unsafe power-removal events
        ≠
current evidence that the protection hardware can still perform its job
```

**Primary anchors:** Intel 330275-001US, p. 4, Table 2; Intel 328171-010US, January 2015, printed p. 21, SMART attributes `AEh` and `AFh`.

### H/P — AFh retains three different pieces of PLI self-test state

Intel describes `AFh` as carrying three health-check outputs.

1. **Microseconds to discharge capacitors.** The SSD partially discharges the backup capacitors to check whether they can release and sustain energy as designed for transferring in-flight committed buffer data to NAND. For the S3700/S3500, the brief gives a minimum of **25 µs**. The S3700 Product Specification defines an expected reported range beginning at 25 µs.
2. **Minutes since last test.** The drive keeps a time-since-test value, saturating at the field's maximum.
3. **Lifetime number of tests.** The drive accumulates a test count; the normalized value distinguishes ordinary status from a failed test and a test performed under excessive temperature.

These fields are not the user payload. They are retained operational records about whether the apparatus intended to protect future payload still appears serviceable.

**Primary anchors:** Intel 330275-001US, p. 4, Table 2; Intel 328171-010US, printed p. 21.

### H/P — the capacitor test is a partial-discharge readiness test, not the same operation as a real power-loss event

Intel says the self-test **partially discharges** the backup capacitors to verify that they can release and sustain the required energy. That matters methodologically: a self-test does not need to recreate every aspect of a real external outage to produce useful evidence about one component of the future failure path.

The test result is therefore evidence about a bounded capability — capacitor discharge behavior under the product's self-test — rather than direct proof of every switch, firmware path, NAND-program operation, filesystem sequence, power waveform, or host command under every future outage.

### H/P — the operator can inspect, manually invoke, and schedule PLI tests

Intel's brief shows the PLI attributes exposed through Intel SSD Toolbox and states that the S3700/S3500 support SCT commands through which an administrator can manually invoke a capacitor test or set capacitor-test intervals. Intel explicitly frames the health log as information that can support action, including replacement before a later power loss compromises data.

So automation does not eliminate operational labor. It relocates some detection and measurement into the drive while exposing the resulting state to an administrator or management stack.

**Primary anchor:** Intel 330275-001US, p. 5.

### H/P — Intel separates self-test from wider power-loss validation

The PLI brief has a distinct section, `Validating Solid-State Drives with PLI`. It says validation includes checking PLI circuitry and switch timing, plus rare but plausible cases such as power loss during firmware update or secure erase. It names a key validation deliverable: the drive should return to a stable state, enumerate after the specified recovery interval, and commands that had been acknowledged complete should not have suffered data loss.

Intel also discusses shorn writes with aligned and unaligned data and describes a validation flow in which an SSD is hot-unplugged during an I/O stream, left off, reinserted, and then checked to verify that the intended LBAs were committed. Figure 6 shows that flow repeating **7000 times** before pass/fail.

This is not the same evidence class as AFh self-test telemetry:

```text
component/path readiness probe
        ≠
whole-device fault-validation campaign
```

**Primary anchor:** Intel 330275-001US, p. 6 and Figure 6.

### H/P — enhanced power-loss management has an external power-transition envelope

The January 2015 S3700 specification does not reduce enhanced power-loss protection to a Boolean property of “power present / power absent.” Its electrical characteristics specify a minimum supply fall time of **1 ms** for the documented rails, and the footnote states that fall time must meet the minimum in order to guarantee full functionality of enhanced power-loss management.

The exact interpretation of all possible abnormal waveforms is outside this case. The bounded point is simpler:

> the manufacturer contract itself makes the failure path dependent on the shape/timing of the supply transition, not only on the eventual fact that power reached zero.

**Primary anchor:** Intel 328171-010US, January 2015, printed pp. 9–10, Tables 7 and 10 plus note 2.

### H/P — the product specification explicitly preserves a capacitor-test control surface

The January 2015 S3700 specification lists `Enhanced power-loss data protection` among product features and separately states in §2.8 that the drive supports testing of the power-loss capacitor, monitored through SMART attribute `AFh`.

That later named-product specification independently anchors the self-test relation that the technology brief explains in more detail.

**Primary anchors:** Intel 328171-010US, January 2015, feature summary and printed p. 13 §2.8; printed p. 21 SMART table.

---

## Retained state

The case requires at least six different state classes to remain distinct.

### 1. User/system data in ordinary temporary buffers

This is the payload threatened by sudden power loss and protected by the PLI handoff already established in Case 15's earlier product context.

### 2. NAND-resident current state

This is the nonvolatile destination after a successful emergency transfer.

### 3. Stored capacitor energy

The capacitor charge is not payload. It is a finite energy reserve intended to keep the controller/NAND path alive long enough to finish the transition.

### 4. PLI health result

AFh retains the most recent self-test result. This state describes the protection apparatus rather than the application object.

### 5. Test recency and lifetime count

Time since last test and cumulative number of tests are retained operational-history fields. They answer different questions from the last instantaneous result.

### 6. Power-loss event history

AEh accumulates unclean shutdown events. This record describes exposure to a class of events, not proof that the protection mechanism failed during them.

The device therefore retains not only user data but also **state about the condition, recency, and history of the mechanism responsible for protecting future data**.

---

## Retention mechanism

The full bounded relation has two temporal layers.

### Failure-time path

```text
supply falls below threshold
        ↓
PLI voltage detector
        ↓
switch/isolate ordinary supply path
        ↓
capacitor energy powers controller/NAND work
        ↓
temporary committed state transferred to NAND
```

### Before-the-failure readiness path

```text
normal powered operation
        ↓
periodic or manually invoked capacitor self-test
        ↓
partial discharge measurement
        ↓
AFh last-result + recency + lifetime-test state
        ↓
operator / management interpretation
        ↓
continue service, investigate, or replace
```

The second path does not itself save the user payload during the outage. It preserves and updates evidence about whether the first path remains plausibly capable of doing so when needed.

---

## Addressing and access geometry

The protected payload remains addressed through the SSD's host-visible block interface and hidden controller/NAND mapping. The new addressability relation in this case is management-oriented rather than payload-oriented:

- SMART attribute `AEh` addresses event-history state;
- SMART attribute `AFh` addresses PLI health/test state;
- Intel SSD Toolbox exposes those fields to an administrator;
- SCT can invoke or schedule the capacitor test.

Thus “access to retained state” includes operational telemetry that is not an application LBA.

---

## Read / write / test semantics

### Ordinary payload reads/writes

They are not re-derived here. Case 15 and the SSD/FTL cases handle the relevant data-path distinction.

### Self-test

The capacitor test is neither an ordinary read nor a destructive payload read. It deliberately consumes some stored energy in a **partial discharge**, measures the resulting discharge behavior, and records health state.

That makes testing itself a maintenance action on retention infrastructure.

### Health-state update

AFh's current result, recency, and test count evolve as tests occur. AEh evolves when unclean shutdowns occur. These management records have their own write/update semantics independent of application data updates.

---

## Time

Case 38 adds several timescales to the repository:

- instantaneous/short capacitor discharge measurement;
- the minimum discharge criterion reported by the self-test;
- minutes since last self-test;
- cumulative lifetime test count;
- cumulative unsafe-power-loss event count;
- the bounded supply-fall interval during a real event;
- emergency transfer time;
- post-power-restoration enumeration/recovery time used in Intel's validation flow;
- product-lifetime aging of the energy-storage components.

These timescales should not be compressed into one generic `durability time`.

---

## Maintenance, labor, and infrastructure

The case makes the maintenance burden of a nominally automatic power-loss feature visible.

It includes:

- capacitor chemistry selection and lifetime margin;
- voltage detection and switching hardware;
- firmware for the emergency path;
- periodic self-test machinery;
- SMART state encoding;
- SCT control;
- administrator inspection and replacement decisions;
- manufacturer validation tooling and repeated hot-unplug testing;
- qualification of the external power-transition envelope.

This is a useful counterexample to the idea that nonvolatile storage eliminates maintenance. Even the **mechanism that protects a nonvolatile transition** can itself require health checks, retained history, replacement policy, and human/institutional interpretation.

---

## Failure / forgetting modes

Distinct failures include:

- capacitor energy reserve degrading below what the protection path expects;
- a self-test failure;
- a self-test performed outside specified temperature conditions;
- stale health evidence because too much time has elapsed since the last test;
- voltage detection/switch timing failure;
- a supply transition outside the manufacturer's documented fall-time envelope;
- firmware failure during the emergency path;
- NAND/controller failure despite adequate capacitor discharge capability;
- a power-loss event during unusual controller operations such as firmware update or secure erase;
- acknowledged-write data loss under a fault despite the intended contract;
- operator failure to inspect or act on reported health state.

A failed AFh test is therefore not synonymous with user-data loss. Conversely, a passing capacitor self-test is not proof that every possible power-fault sequence will preserve every relevant higher-layer invariant.

---

## Engineering reconstruction

### E — retention mechanism presence ≠ retention mechanism readiness

A drive can physically contain the intended capacitors and switching path while the current ability of those parts to supply the required emergency energy is a separate condition. The self-test exists because installation-time presence and lifetime readiness are not the same relation.

### E — retention infrastructure can itself require periodic verification

The PLI mechanism protects state only at a future exceptional event. Intel's architecture therefore spends ordinary powered time checking whether that future-event mechanism still works. The work needed for retention includes **maintenance of the apparatus that will later perform retention work**.

### E — future-fault protection ≠ payload-only retained state

AEh/AFh show that power-loss protection depends on additional retained management state: event count, last result, recency, and lifetime test count. The payload is not the only state needed for a defensible durability regime.

### E — self-test evidence ≠ full power-fault validation

Partial capacitor discharge tests a bounded capability. Intel separately documents whole-device validation involving switch timing, hot removal, recovery, LBA verification, and rare scenarios. The project should not collapse a component health probe into complete system assurance.

### E — power-loss occurrence ≠ power-loss-protection failure

AEh and AFh are deliberately separate. An unclean shutdown can occur even if PLI performs correctly; PLI health can degrade even before a future external event exposes the problem.

### E — failure envelope includes transition geometry

A persistence guarantee may depend not only on whether a failure occurs but on its time profile. The S3700 power specification's fall-time condition makes that hidden relation explicit.

### E — automatic monitoring ≠ no operator responsibility

The drive can generate and retain health state automatically, but Intel also exposes that state and test control so an administrator can decide whether investigation or replacement is required.

### E — manufacturer validation ≠ independent compliance evidence

Intel's 7000-repeat validation flow is meaningful first-party evidence for the test method Intel describes. It is not an independent field study of every shipped device, nor does it identify the anonymized FAST '13 devices from Case 15.

---

## Functional analogies

### A — comparison with Case 15 SSD 320

Case 15 asks how stored energy funds an emergency transition from volatile controller state to NAND. Case 38 asks how a later data-center SSD architecture **checks and records the health of that emergency capability**. The relation is a same-vendor product-family comparison across periods, not proof that all implementation details are identical.

### A — comparison with DRAM refresh monitoring

Both DRAM refresh and PLI self-test can involve recurring maintenance activity. But they do different jobs:

- DRAM refresh reconstructs the payload state itself before charge decay crosses a deadline;
- PLI self-test checks the future readiness of an exceptional protection path while ordinary NAND payload is already nonvolatile.

`periodic maintenance` is therefore only a functional comparison, not a shared mechanism.

### A — comparison with Intel ADR/eADR, Case 32

ADR/eADR and SSD PLI both make stored energy and failure-triggered transfer relevant to persistence. Case 38 adds an explicit drive-local telemetry/self-test layer for its capacitor path. This does not establish a historical genealogy or imply that platform ADR and SATA SSD PLI expose the same interface contract.

---

## Philosophical pressure — bounded

A narrow conceptual result follows from the mechanism:

> technical retention may depend on retaining evidence about the continued availability of the mechanism that is supposed to perform future retention work.

That is stronger than saying “the device stores health metadata.” The health record has a temporal role: it links a past test to a future decision about whether the drive's failure-time protection should still be trusted.

But the boundary is strict. A SMART attribute is not automatically human or cultural memory, and this case does not turn PLI telemetry into Stieglerian tertiary retention or Heideggerian `Bestand`. The engineering case only shows that **availability of future durability can itself become an addressable, updated, interpreted technical state**.

---

## Counterexamples and limits

This case does **not** establish:

- that Intel invented power-loss protection, capacitor backup, SMART, self-test, or fault injection;
- that the S3700 and S3500 are internally identical;
- that a passing AFh result guarantees every future power-fault outcome;
- that a failing AFh result means user payload has already been lost;
- that Intel's 7000-cycle validation flow is an industry-wide standard;
- that the exact supply-fall requirement applies to all SSDs;
- that the anonymous SSDs in FAST '13 included an S3700/S3500;
- that filesystem/database durability follows automatically from drive-level PLI;
- that controller metadata recovery under every interrupted operation has been independently characterized.

The case is grounded for **manufacturer-described PLI health monitoring, capacitor self-test, retained test/event state, and Intel's named validation procedure**, not for independent fleet-wide compliance.

---

## Prior-art and related-repository boundary

No invention-priority claim is needed. The historical terms are Intel's product/technology vocabulary in the inspected 2014-era/2015 documents.

Before writing, `tmzncty/computing-archaeology` was searched for dedicated material using combinations of:

- `S3700 PLI power loss capacitor SSD`;
- `power loss protection SSD capacitor`.

No dedicated existing case was found by those searches. Generic SSD/Flash history remains outside this case; the retention-specific contribution is the **readiness/health/validation relation**.

Internal links:

- [Case 04 — Flash virtual mapping](04-flash-virtual-mapping-logical-identity.md)
- [Case 15 — Intel SSD 320 power-loss durability](15-intel-ssd320-power-loss-durability.md)
- [Case 20 — NVMe 1.0 Flush/FUA](20-nvme10-fua-flush-persistence-ordering.md)
- [Case 32 — Intel ADR/eADR](32-intel-adr-eadr-power-fail-domain.md)

---

## Sources and inspection notes

### Primary — Intel PLI technology brief

Intel Corporation, **_Power Loss Imminent (PLI) Technology_**, document 330275-001US. The inspected document does not expose a clean title-page publication date; its references state sample pricing `As of February 28, 2014`, so this case describes it conservatively as **2014-era** rather than inventing an exact publication day.

Direct Intel-hosted PDF:
<https://www.intel.com/content/dam/www/public/us/en/documents/technology-briefs/ssd-power-loss-imminent-technology-brief.pdf>

Directly inspected:

- pp. 1–2 — PLI capacitor/voltage-detector path and periodic verification requirement;
- p. 4 — Table 2, `AEh` / `AFh`, partial-discharge self-test, minimum 25 µs, time-since-test, lifetime-test count;
- p. 5 — Toolbox/SCT exposure and administrator action;
- p. 6 — validation scope, acknowledged-complete command target, hot-unplug/LBA verification, Figure 6 7000-repeat flow;
- p. 7 — S3700/S3500 identified as products with enabled PLI hardware/firmware.

### Primary — Intel SSD DC S3700 Product Specification

Intel Corporation, **_Intel Solid-State Drive DC S3700 Series Product Specification_**, January 2015, order 328171-010US.

Direct Intel-hosted PDF:
<https://www.intel.com/content/dam/www/public/us/en/documents/product-specifications/ssd-dc-s3700-spec.pdf>

Directly inspected:

- feature summary — enhanced power-loss data protection and capacitor self-test;
- printed pp. 9–10 — power-supply fall-time condition for enhanced power-loss management;
- printed p. 13 §2.8 — `Power Loss Capacitor Test`, monitored through SMART `AFh`;
- printed p. 21 — `AEh` and `AFh`, discharge-test range, recency, lifetime count, normalized failure/excess-temperature states.

---

## Status

**`grounded`** for the bounded PLI-health / self-test / manufacturer-validation relation.

The sources are unusually strong for the historical/product layer because they directly expose not only the power-fail mechanism but also the drive's own health state, self-test procedure, operator-visible control surface, and Intel's validation workflow. The unresolved next step is deliberately different: **independent named-product fault-compliance evidence or deeper controller-metadata recovery**, not another repetition of the capacitor-transfer mechanism.