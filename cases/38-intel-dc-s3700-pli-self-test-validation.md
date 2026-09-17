# Intel DC S3700/S3500 PLI Self-Test: Retention-Infrastructure Health, Fault Validation, and Readiness State

## Scope

- **Bounded period:** 2012–2015. The chronology now begins with Intel's October-2012 _Intel Solid-State Drive DC S3700 Product Specification_ (328171-001US), whose internal revision history records `June 2012 | 001 | Initial release`, and a dated Intel public S3700 fact sheet of 12 November 2012. The later explanatory witnesses remain Intel's 2014-era _Power Loss Imminent (PLI) Technology_ brief (330275-001US; references preserve sample pricing dated 28 February 2014) and the January-2015 S3700 Product Specification (328171-010US).
- **Named products:** Intel SSD DC S3700 Series and S3500 Series where the PLI brief addresses both; product-specification claims are restricted to the S3700 where that is the inspected source.
- **Primary sources:** Intel manufacturer documentation, directly inspected as PDF text and rendered pages.
- **Research question:** when a future power-loss survival path depends on capacitors, switching, firmware, and NAND transfer, what state and verification work must itself be retained so that the protection mechanism is still trustworthy when the power-fail event arrives?

Chronology deepening: [`../evidence/38-intel-s3700-2012-pli-self-test-control-surface-prior-art-deepening.md`](../evidence/38-intel-s3700-2012-pli-self-test-control-surface-prior-art-deepening.md) moves the named-product documentary floor earlier than the 2014-era explanatory brief. The October-2012 S3700 specification already exposes capacitor self-test, separate `AEh`/`AFh` event-vs-readiness state, and SCT feature `D000h` for the capacitor-test interval; the 12-November-2012 Intel fact sheet publicly advertises a `Power safe write cache with built in self-test`. The internal `June 2012` revision-history entry is kept distinct from independently dated public disclosure.

This case does **not** repeat Case 15's Intel SSD 320 mechanism history. Case 15 establishes the basic controller-mediated durability handoff: volatile temporary state can sit in front of nonvolatile NAND, and stored capacitor energy can fund emergency transfer after external power begins to disappear. The present case asks a later and narrower question:

> **How is the health of that retention infrastructure itself made operationally visible, periodically tested, and qualified?**

It is also not independent fault-injection certification of Intel products. Intel's documents are first-party evidence for the product contract, telemetry, self-test, and validation method Intel described. The independent FAST '13 evidence already bounded in Case 15 remains the methodological warning that a manufacturer/interface claim and measured implementation compliance are different evidence classes.

---

## Historical vocabulary

The inspected Intel sources themselves use:

- `Power safe write cache with built in self-test`;
- `Power Loss Capacitor Test`;
- `Power Safe Write Cache capacitor test interval`;
- `Power Loss Imminent (PLI)`;
- `Enhanced power-loss data protection`;
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

### H/P — the S3700 self-test / readiness control surface is already present in 2012 product documentation

The directly inspected Intel-hosted S3700 product specification, order **328171-001US**, repeatedly prints `October 2012 Product Specification`. Its feature list separately names `Enhanced power-loss data protection` and `Power loss protection capacitor self-test`; §2.9 says the power-loss capacitor can be tested and monitored through SMART attribute `AFh`.

The same 2012 SMART table already separates:

- `AEh Unexpected Power Loss`, a cumulative count of unclean shutdowns explicitly defined regardless of PLI capacitor activity;
- `AFh Power Loss Protection Failure`, which records the latest capacitor-discharge result, minutes since the last test, and lifetime test count.

Its SCT section also lists vendor feature **D000h**, `Power Safe Write Cache capacitor test interval`.

Thus the basic named-product relations later explained in the 2014-era PLI brief were already visible in a 2012 S3700 product specification:

```text
power-loss-protection mechanism
    !=
readiness-test result
    !=
readiness-test recency / accumulated test history
    !=
test-interval control
```

The source is terse about mechanism. It does **not** by itself license back-projecting the later brief's partial-discharge explanation or 25 µs minimum into every 2012 statement.

**Primary anchors:** Intel 328171-001US, October 2012, printed pp. 5, 11, 19, 24 and 28.

### H/P — June / October / November 2012 are different chronology claims

The surviving 328171-001US PDF's revision-history table says `June 2012 | 001 | Initial release`, while the document itself prints October 2012. A separate Intel news fact sheet dated **12 November 2012** calls the S3700 `newly unveiled` and publicly advertises `Power safe write cache with built in self-test` under `Strong Data Protection`.

These records establish different things and are not collapsed:

```text
June 2012
    Intel's internal revision-history statement

October 2012
    printed date of the directly inspected surviving specification

12 November 2012
    independently dated public Intel product-news witness
```

The June row is not treated as independently proven public-web availability of the currently hosted PDF. The November fact sheet supplies the clean dated public-facing witness; the October product specification supplies the detailed management/control surface.

**Primary anchors:** Intel 328171-001US, printed p. 28; Intel News Fact Sheet, 12 November 2012, first page.

### H/P — PLI is a failure-triggered transfer path, but Intel also treats its future readiness as a design problem

Intel's PLI brief describes PLI-enabled SSDs as containing energy-storing capacitors. A voltage detector monitors the drive supply; when voltage falls below a predefined level, capacitor energy is used so temporary-buffer state can be written to nonvolatile NAND. After normal power returns, the capacitors recharge for a future event.

The same brief then moves beyond the emergency transfer itself. Intel says an important architectural requirement is to monitor PLI health, performance, and usage count, and that SMART functionality is incorporated to **periodically verify that the PLI circuitry continues to function properly over the life of the SSD**.

That is the key historical fact for this case. A retention path is not treated as timelessly trustworthy merely because its capacitors and switches were installed at manufacture.

The 2012 deepening now shows that the named S3700 product surface for self-test and test-state monitoring predates this later explanatory brief; the brief remains the stronger source for explaining how Intel describes the test and validation mechanism.

**Primary anchors:** Intel 330275-001US, pp. 1–2, especially the sections `PLI Technology Details`, `Architecting and Implementing PLI Technology Solution into a Solid-State Drive`, and `PLI Technology Architecture`.

### H/P — S3700/S3500 expose power-loss event history separately from PLI-capability health

Intel's PLI brief identifies two SMART attributes for the DC S3700 and S3500:

- `AEh`, `Unexpected Power Loss`, whose raw value counts unclean shutdowns over drive life. Intel explicitly says this count is independent of whether the PLI capacitor path was active.
- `AFh`, `Power Loss Protection Failure`, which reports information about the most recent PLI self-test and PLI-capacitor health.

The October-2012 and January-2015 S3700 Product Specifications preserve the same basic distinction in their SMART tables. The event count and the health/test record are therefore not one statistic.

```text
history of unsafe power-removal events
        ≠
current evidence that the protection hardware can still perform its job
```

**Primary anchors:** Intel 328171-001US, October 2012, printed p. 19; Intel 330275-001US, p. 4, Table 2; Intel 328171-010US, January 2015, printed p. 21, SMART attributes `AEh` and `AFh`.

### H/P — AFh retains three different pieces of PLI self-test state

Intel describes `AFh` as carrying three health-check outputs.

1. **Microseconds to discharge capacitors.** The 2012 S3700 specification already describes the last test result in capacitor-discharge microseconds. The later PLI brief explains that the SSD partially discharges the backup capacitors to check whether they can release and sustain energy as designed for transferring in-flight committed buffer data to NAND. For the S3700/S3500, the later brief gives a minimum of **25 µs**; the January-2015 S3700 specification defines an expected reported range beginning at 25 µs.
2. **Minutes since last test.** The drive keeps a time-since-test value, saturating at the field's maximum.
3. **Lifetime number of tests.** The drive accumulates a test count; the later detailed documents further expose normalized-state handling for failed or excessive-temperature tests.

These fields are not the user payload. They are retained operational records about whether the apparatus intended to protect future payload still appears serviceable.

The chronology matters: the **basic result / recency / lifetime-count decomposition is already documented in 2012**, while the later brief supplies the fuller explanatory semantics.

**Primary anchors:** Intel 328171-001US, October 2012, printed p. 19; Intel 330275-001US, p. 4, Table 2; Intel 328171-010US, printed p. 21.

### H/P — the capacitor test is a partial-discharge readiness test, not the same operation as a real power-loss event

Intel's later PLI brief says the self-test **partially discharges** the backup capacitors to verify that they can release and sustain the required energy. That matters methodologically: a self-test does not need to recreate every aspect of a real external outage to produce useful evidence about one component of the future failure path.

The test result is therefore evidence about a bounded capability — capacitor discharge behavior under the product's self-test — rather than direct proof of every switch, firmware path, NAND-program operation, filesystem sequence, power waveform, or host command under every future outage.

This `partial discharge` wording is sourced to the later brief, not silently attributed to the terse 2012 product specification.

### H/P — the operator can inspect, manually invoke, and schedule PLI tests

The 2012 S3700 specification already exposes `D000h (Power Safe Write Cache capacitor test interval)` through SCT, establishing an early named-product control surface for test cadence. The later PLI brief shows PLI attributes exposed through Intel SSD Toolbox and states more explicitly that the S3700/S3500 support SCT commands through which an administrator can manually invoke a capacitor test or set capacitor-test intervals. Intel frames the health log as information that can support action, including replacement before a later power loss compromises data.

So automation does not eliminate operational labor. It relocates some detection and measurement into the drive while exposing the resulting state to an administrator or management stack.

The 2012 D000h text alone does not prove that the selected test interval survives every reset or power cycle; `control surface exists` is kept separate from `policy is restart-persistent`.

**Primary anchors:** Intel 328171-001US, October 2012, printed p. 24; Intel 330275-001US, p. 5.

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

The October-2012 S3700 specification already lists `Enhanced power-loss data protection` and `Power loss protection capacitor self-test`, states in §2.9 that the power-loss capacitor test is monitored through SMART `AFh`, and exposes the D000h test-interval control through SCT. The January-2015 S3700 specification preserves the self-test relation in a later product revision.

This changes the source role of the 2015 document: it remains useful as later product-contract continuity and for additional product details, but it is no longer the earliest directly inspected S3700 product-specification witness for the capacitor-test surface.

**Primary anchors:** Intel 328171-001US, October 2012, printed pp. 5, 11, 19 and 24; Intel 328171-010US, January 2015, feature summary, printed p. 13 §2.8 and p. 21 SMART table.

### H/P — the same 2012 product specification keeps NAND data-retention qualification separate from PLI readiness

The October-2012 S3700 reliability table specifies **3 months power-off data retention after the SSD reaches rated write endurance at 40 °C**. Immediately after the reliability/temperature material, §2.9 separately documents the power-loss capacitor test.

These are different product claims:

```text
longer-horizon NAND data retention after power is absent
        ≠
short emergency-energy readiness while power is disappearing
```

The proximity in one product specification is useful because it prevents the generic word `retention` from collapsing medium aging and failure-triggered durability infrastructure into one property.

**Primary anchor:** Intel 328171-001US, October 2012, printed p. 11, Table 14 and §2.9.

---

## Retained state

The case requires at least seven different state/control classes to remain distinct.

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

### 7. Test-cadence control

The 2012 SCT feature D000h exposes a `Power Safe Write Cache capacitor test interval`. This is policy/control state about **when readiness evidence should be refreshed**, not the readiness result itself. The inspected 2012 passage does not establish its persistence across every restart boundary.

The device therefore retains not only user data but also **state about the condition, recency, history, and maintenance cadence of the mechanism responsible for protecting future data**.

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
test cadence / explicit test control
        ↓
periodic or manually invoked capacitor self-test
        ↓
partial discharge measurement (later Intel explanation)
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
- Intel SSD Toolbox exposes those fields to an administrator in the later brief;
- SCT can invoke or schedule the capacitor test;
- the 2012 S3700 specification already exposes D000h as the capacitor-test-interval feature.

Thus “access to retained state” includes operational telemetry and maintenance-policy state that are not application LBAs.

---

## Read / write / test semantics

### Ordinary payload reads/writes

They are not re-derived here. Case 15 and the SSD/FTL cases handle the relevant data-path distinction.

### Self-test

The capacitor test is neither an ordinary read nor a destructive payload read. The 2012 product specification exposes the test and discharge-time result; the later Intel PLI brief explains that the test deliberately consumes some stored energy in a **partial discharge**, measures the resulting discharge behavior, and records health state.

That makes testing itself a maintenance action on retention infrastructure.

### Health-state update

AFh's current result, recency, and test count evolve as tests occur. AEh evolves when unclean shutdowns occur. These management records have their own write/update semantics independent of application data updates.

### Test-policy control

D000h adds another relation: the cadence at which readiness evidence is refreshed can itself be controlled. `test interval configured` and `test result passed` are not interchangeable states.

---

## Time

Case 38 adds several timescales to the repository:

- instantaneous/short capacitor discharge measurement;
- the minimum discharge criterion reported by the later explanatory self-test source;
- minutes since last self-test;
- configured/selected test interval;
- cumulative lifetime test count;
- cumulative unsafe-power-loss event count;
- the bounded supply-fall interval during a real event;
- emergency transfer time;
- post-power-restoration enumeration/recovery time used in Intel's validation flow;
- product-lifetime aging of the energy-storage components;
- NAND's separately specified power-off data-retention horizon at rated endurance.

These timescales should not be compressed into one generic `durability time`.

---

## Maintenance, labor, and infrastructure

The case makes the maintenance burden of a nominally automatic power-loss feature visible.

It includes:

- capacitor chemistry selection and lifetime margin;
- voltage detection and switching hardware;
- firmware for the emergency path;
- periodic self-test machinery;
- test-cadence control;
- SMART state encoding;
- SCT control;
- administrator inspection and replacement decisions;
- manufacturer validation tooling and repeated hot-unplug testing;
- qualification of the external power-transition envelope.

This is a useful counterexample to the idea that nonvolatile storage eliminates maintenance. Even the **mechanism that protects a nonvolatile transition** can itself require health checks, retained history, maintenance policy, replacement policy, and human/institutional interpretation.

---

## Failure / forgetting modes

Distinct failures include:

- capacitor energy reserve degrading below what the protection path expects;
- a self-test failure;
- a self-test performed outside specified temperature conditions;
- stale health evidence because too much time has elapsed since the last test;
- an inappropriate or stale test-cadence policy;
- voltage detection/switch timing failure;
- a supply transition outside the manufacturer's documented fall-time envelope;
- firmware failure during the emergency path;
- NAND/controller failure despite adequate capacitor discharge capability;
- a power-loss event during unusual controller operations such as firmware update or secure erase;
- acknowledged-write data loss under a fault despite the intended contract;
- operator failure to inspect or act on reported health state.

A failed AFh test is therefore not synonymous with user-data loss. Conversely, a passing capacitor self-test is not proof that every possible power-fault sequence will preserve every relevant higher-layer invariant.

---

## Independent named-product follow-up — Intel DC S3500 system-stack power-cut observation

A bounded independent follow-up is available in [`../evidence/38-intel-s3500-2014-independent-power-cut-stack-validation-deepening.md`](../evidence/38-intel-s3500-2014-independent-power-cut-stack-validation-deepening.md).

Intel's January-2015 S3500 product specification independently anchors `Enhanced power-loss data protection`, the power-loss capacitor self-test, and the separation between `AEh` unexpected-power-loss history and `AFh` protection-health state. Nordeus Engineering then supplies a different source role: it reports **December-2014 hard-power-cut testing of a named Intel DC S3500** inside a Dell R420 / H710p / CentOS 6.5 / XFS stack. Its `fsync` test used an external side-channel record, physically unplugged the server, waited ten minutes, rebooted, and verified the file; its PostgreSQL 9.3 path used data checksums and `pg_dumpall` after the same class of hard cut. The displayed S3500 configuration with disk cache on, barriers off, and RAID write-back is reported `OK` in both test families, with tested parameter combinations requiring at least five successful repetitions to count as passed.

This closes only the **independent named-product witness** part of the old evidence debt. It is explicitly **system-stack evidence**, not isolated SSD-only certification: RAID-controller behavior, software, host power transition, and drive state all remain in the causal path. `>=5 observed passes != complete failure-envelope coverage`, and successful filesystem/database recovery does not expose every hidden FTL/controller-metadata path.

---

## Engineering reconstruction

### E — retention mechanism presence ≠ retention mechanism readiness

A drive can physically contain the intended capacitors and switching path while the current ability of those parts to supply the required emergency energy is a separate condition. The self-test exists because installation-time presence and lifetime readiness are not the same relation.

### E — retention infrastructure can itself require periodic verification

The PLI mechanism protects state only at a future exceptional event. Intel's architecture therefore spends ordinary powered time checking whether that future-event mechanism still works. The work needed for retention includes **maintenance of the apparatus that will later perform retention work**.

### E — maintenance cadence ≠ maintenance evidence

The 2012 D000h interval and AFh result expose different relations:

```text
when should readiness be tested?
        ≠
what did the last readiness test observe?
        ≠
how old is that observation?
```

The existence of a host-visible interval setting does not, by itself, prove that the setting persists across every reset or firmware transition.

### E — future-fault protection ≠ payload-only retained state

AEh/AFh show that power-loss protection depends on additional retained management state: event count, last result, recency, and lifetime test count. D000h adds a separate maintenance-policy surface. The payload is not the only state needed for a defensible durability regime.

### E — self-test evidence ≠ full power-fault validation

Partial capacitor discharge tests a bounded capability. Intel separately documents whole-device validation involving switch timing, hot removal, recovery, LBA verification, and rare scenarios. The project should not collapse a component health probe into complete system assurance.

### E — power-loss occurrence ≠ power-loss-protection failure

AEh and AFh are deliberately separate as early as the 2012 S3700 specification. An unclean shutdown can occur even if PLI performs correctly; PLI health can degrade even before a future external event exposes the problem.

### E — medium retention ≠ emergency-transfer readiness

The 2012 S3700 product specification can simultaneously specify a NAND power-off data-retention horizon and a capacitor-test mechanism because they qualify different physical/operational relations. Nonvolatile payload aging and short hold-up-energy readiness should not be merged into one generic SSD-retention property.

### E — failure envelope includes transition geometry

A persistence guarantee may depend not only on whether a failure occurs but on its time profile. The later S3700 power specification's fall-time condition makes that hidden relation explicit.

### E — automatic monitoring ≠ no operator responsibility

The drive can generate and retain health state automatically, but Intel also exposes that state and test control so an administrator can decide whether investigation or replacement is required.

### E — manufacturer validation ≠ independent compliance evidence

Intel's 7000-repeat validation flow is meaningful first-party evidence for the test method Intel describes. It is not an independent field study of every shipped device, nor does it identify the anonymized FAST '13 devices from Case 15.

### E — independent system-stack observation ≠ isolated SSD-only causality

Nordeus supplies an independent named-product fault observation, but the S3500 is tested inside a Dell/H710p/Linux/XFS/PostgreSQL stack rather than on an isolated component bench. A passing stack is evidence about that tested composition; it does not prove that every successful outcome is attributable only to the drive-local PLI mechanism.

### E — repeated pass ≠ complete power-fault envelope

Nordeus requires at least five passes for a parameter combination and reports success for the displayed S3500 configuration. That is useful independent fault-injection evidence, but it does not sweep supply waveform, cut timing against every internal operation, temperature, age, firmware, or every host/controller/software composition.

---

## Functional analogies

### A — comparison with Case 15 SSD 320

Case 15 asks how stored energy funds an emergency transition from volatile controller state to NAND. Case 38 asks how a later data-center SSD architecture **checks and records the health of that emergency capability**. The 2012 product evidence additionally shows that a test cadence can be exposed as a control surface. The relation is a same-vendor product-family comparison across periods, not proof that all implementation details are identical.

### A — comparison with DRAM refresh monitoring

Both DRAM refresh and PLI self-test can involve recurring maintenance activity. But they do different jobs:

- DRAM refresh reconstructs the payload state itself before charge decay crosses a deadline;
- PLI self-test checks the future readiness of an exceptional protection path while ordinary NAND payload is already nonvolatile.

`periodic maintenance` is therefore only a functional comparison, not a shared mechanism.

### A — comparison with proactive integrity scans

At a narrow relation level, PLI readiness testing and a scrub/scanner both perform work before an observed demand failure so latent loss of capability can be discovered. But the verified object differs: scrub cases qualify stored payload/redundancy; Case 38 qualifies a component/path that may later preserve in-flight payload. No shared mechanism or genealogy is implied.

### A — comparison with Intel ADR/eADR, Case 32

ADR/eADR and SSD PLI both make stored energy and failure-triggered transfer relevant to persistence. Case 38 adds an explicit drive-local telemetry/self-test layer for its capacitor path. This does not establish a historical genealogy or imply that platform ADR and SATA SSD PLI expose the same interface contract.

---

## Philosophical pressure — bounded

A narrow conceptual result follows from the mechanism:

> technical retention may depend on retaining evidence about the continued availability of the mechanism that is supposed to perform future retention work.

That is stronger than saying “the device stores health metadata.” The health record has a temporal role: it links a past test to a future decision about whether the drive's failure-time protection should still be trusted. The 2012 test-interval control adds a further layer: the system can expose a policy for when this evidence should be refreshed.

But the boundary is strict. A SMART attribute is not automatically human or cultural memory, and this case does not turn PLI telemetry into Stieglerian tertiary retention or Heideggerian `Bestand`. The engineering case only shows that **availability of future durability can itself become an addressable, updated, interpreted technical state**.

---

## Counterexamples and limits

This case does **not** establish:

- that Intel invented power-loss protection, capacitor backup, SMART, self-test, or fault injection;
- that Intel invented a capacitor-health test in 2012;
- that the internal `June 2012` revision-history row independently proves the exact public-web publication date of the surviving specification;
- that the S3700 and S3500 are internally identical;
- that the terse 2012 S3700 specification by itself establishes the later brief's partial-discharge mechanism or 25 µs explanatory minimum;
- that D000h is proven to persist across every power cycle, reset, or firmware update;
- that a passing AFh result guarantees every future power-fault outcome;
- that a failing AFh result means user payload has already been lost;
- that Intel's 7000-cycle validation flow is an industry-wide standard;
- that the exact supply-fall requirement applies to all SSDs;
- that the anonymous SSDs in FAST '13 included an S3700/S3500;
- that filesystem/database durability follows automatically from drive-level PLI;
- that controller metadata recovery under every interrupted operation has been independently characterized.

The case is grounded for **manufacturer-described PLI health monitoring, capacitor self-test, retained test/event state, test-cadence control, and Intel's named validation procedure**, not for independent fleet-wide compliance or invention priority.

---

## Prior-art and related-repository boundary

No invention-priority claim is needed. The historical terms are Intel's product/technology vocabulary in the directly inspected 2012–2015 documents.

The 2012 chronology deepening supplies an earlier named-product documentary/public-product floor for this case without establishing industry priority:

```text
2012 S3700 product specification
    -> self-test + AFh/AEh + D000h control surface

12 Nov 2012 Intel public fact sheet
    -> power-safe write cache with built-in self-test

2014-era PLI brief
    -> detailed partial-discharge / health interpretation / validation narrative

Jan 2015 S3700 specification
    -> later product-contract continuity
```

Before writing and again during the 2012 deepening, `tmzncty/computing-archaeology` was searched for dedicated material using combinations of:

- `S3700`;
- `S3700 PLI power loss capacitor SSD`;
- `power loss protection SSD capacitor`.

No dedicated existing case was found in the current search surface. Generic SSD/Flash history remains outside this case; the retention-specific contribution is the **readiness/health/validation relation and its source chronology**.

Internal links:

- [Case 04 — Flash virtual mapping](04-flash-virtual-mapping-logical-identity.md)
- [Case 15 — Intel SSD 320 power-loss durability](15-intel-ssd320-power-loss-durability.md)
- [Case 20 — NVMe 1.0 Flush/FUA](20-nvme10-fua-flush-persistence-ordering.md)
- [Case 32 — Intel ADR/eADR](32-intel-adr-eadr-power-fail-domain.md)
- [Synthesis 13 — durability handoff / retention-infrastructure readiness](../docs/SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md)

---

## Sources and inspection notes

### Primary — Intel SSD DC S3700 Product Specification, 2012

Intel Corporation, **_Intel Solid-State Drive DC S3700 Product Specification_**, order 328171-001US. The surviving Intel-hosted PDF repeatedly prints **October 2012**; its §9 revision history records `June 2012 | 001 | Initial release`.

Direct Intel-hosted PDF:
<https://download.intel.com/newsroom/kits/ssd/pdfs/Intel_SSD_DC_S3700_Product_Specification.pdf>

Directly inspected:

- printed p. 5 — `Enhanced power-loss data protection` and `Power loss protection capacitor self-test` in the feature list;
- printed p. 11 — three-month NAND data-retention specification at rated endurance / 40 °C, followed by §2.9 `Power Loss Capacitor Test` monitored through `AFh`;
- printed p. 19 — `AEh` unclean-power history and `AFh` last discharge result / minutes since last test / lifetime test count;
- printed p. 24 — SCT vendor feature D000h `Power Safe Write Cache capacitor test interval`;
- printed p. 28 — revision-history row `June 2012 | 001 | Initial release`.

The June date is reported as Intel's own internal revision-history statement; it is not silently upgraded into independently proven public-web availability.

### Primary — Intel S3700 public news fact sheet, 12 November 2012

Intel, **_Intel Solid-State Drive DC S3700 Series Engineered to Eliminate Bottlenecks for Breakthrough High Performance Computing_**, News Fact Sheet, 12 November 2012.

Direct Intel-hosted PDF:
<https://download.intel.com/newsroom/kits/xeon/phi/pdfs/FactSheet_Intel_SSDs_for_HPC_SC12.pdf>

Directly inspected first page: `newly unveiled Intel SSD DC S3700 Series`; under `Strong Data Protection`, `Power safe write cache with built in self-test`.

This source anchors dated public product vocabulary. It does not itself expose the AFh/D000h field structure.

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

The brief is the stronger explanatory witness for the partial-discharge mechanism and wider validation narrative; the 2012 specification now supplies the earlier named-product control-surface chronology.

### Primary — Intel SSD DC S3700 Product Specification, 2015

Intel Corporation, **_Intel Solid-State Drive DC S3700 Series Product Specification_**, January 2015, order 328171-010US.

Direct Intel-hosted PDF:
<https://www.intel.com/content/dam/www/public/us/en/documents/product-specifications/ssd-dc-s3700-spec.pdf>

Directly inspected:

- feature summary — enhanced power-loss data protection and capacitor self-test;
- printed pp. 9–10 — power-supply fall-time condition for enhanced power-loss management;
- printed p. 13 §2.8 — `Power Loss Capacitor Test`, monitored through SMART `AFh`;
- printed p. 21 — `AEh` and `AFh`, discharge-test range, recency, lifetime count, normalized failure/excess-temperature states.

This remains a useful later product-contract witness but is no longer the earliest directly inspected S3700 product-specification witness for the self-test/control surface.

### Independent practitioner — Nordeus S3500 power-cut test

Strahinja Kustudic, Nordeus Engineering, **“Power Failure Testing with SSDs,”** published 12 November 2015; the article states testing was performed in December 2014.

<https://engineering.nordeus.com/power-failure-testing-with-ssds/>

Directly inspected:

- named Intel DC S3500 test subject and test date;
- Dell R420 / H710p / CentOS 6.5 / XFS stack;
- `fsync` side-channel + physical-unplug procedure;
- PostgreSQL 9.3 checksums + `pg_dumpall` recovery procedure;
- at-least-five-pass rule and displayed S3500 results.

See the bounded evidence record for source-role and causality limits.

---

## Status

**`grounded`** for the bounded PLI-health / self-test / manufacturer-validation relation, now with an **earlier 2012 named-product chronology** and an independent named-product **system-stack** power-cut witness.

The source chronology is now sharper: the October-2012 S3700 specification directly exposes capacitor self-test, AFh/AEh state and D000h test-interval control; the 12-November-2012 Intel fact sheet publicly advertises the built-in self-test; the 2014-era brief adds the detailed partial-discharge and validation explanation; the January-2015 specification supplies later product-contract continuity. The internal `June 2012` revision-history entry remains explicitly weaker than an independently archived public-disclosure date.

This does not justify a maturity promotion beyond `grounded`. Remaining work is narrower: **an independently archived June-2012 public-document witness if exact disclosure chronology matters; earlier industry/controller prior art for capacitor-health self-test; controlled component-only S3500/S3700 power-waveform replication; lifetime/temperature coverage; and deeper controller-metadata recovery evidence**, not another repetition of the capacitor-transfer mechanism.