# Case 38 Deepening — PLI Health Failure and Write-Cache Authority Revocation

## Status

**`bounded deepening complete`**

This evidence note deepens [`../cases/38-intel-dc-s3700-pli-self-test-validation.md`](../cases/38-intel-dc-s3700-pli-self-test-validation.md) without changing its maturity.

The narrow question is:

> When a power-loss-protection self-test says the hold-up-energy path is no longer trustworthy, is that result merely diagnostic information, or can it change whether a volatile write-back path is still allowed to operate?

The evidence supports a bounded answer at three different source levels:

1. Intel's October-2012 S3700 product specification directly exposes the **health-test state**, a pre-fail threshold, a separate **write-cache control**, and a capacitor-test cadence control, but does not itself state that AFh failure automatically disables write caching.
2. A contemporary 31-January-2013 Tom's Hardware review of the named S3700 reports that capacitor failure or degraded performance triggers a SMART event and disables write caching. This is useful period product reporting, but it is **secondary**, not an Intel normative product-contract clause or an instrumented firmware trace.
3. The Open Compute Project's **Datacenter SAS-SATA Device Specification v1.0 (28 March 2023)** makes the same control topology explicit as a later datacenter procurement/interface requirement: PLP-capable SSDs must periodically test PLP, and insufficient PLP charge requires flushing cached writes, disabling volatile write cache, issuing a SMART trip, clearing the host-visible WCE bit, and rejecting host attempts to re-enable write cache.

The resulting retention-specific seam is:

```text
readiness evidence
    -> qualification of a future durability path
    -> authority to use a risk-bearing volatile optimization

negative readiness evidence
    -> preserve already-cached state
    -> revoke volatile write-cache authority
    -> expose degraded capability to the host
```

This note does **not** claim that the 2023 OCP requirement descended from the S3700, that Intel invented this pattern, or that the exact OCP transition sequence was implemented by every S3700 firmware revision.

---

## 1. Source custody and chronology

### 1.1 Intel S3700 Product Specification — manufacturer-primary, October 2012

Intel Corporation, **_Intel Solid-State Drive DC S3700 Product Specification_**, order `328171-001US`, October 2012:

<https://download.intel.com/newsroom/kits/ssd/pdfs/Intel_SSD_DC_S3700_Product_Specification.pdf>

Directly inspected rendered pages and text:

- printed p. 5: `Enhanced power-loss data protection` and `Power loss protection capacitor self-test`;
- printed p. 11: §2.9 `Power Loss Capacitor Test` monitored with SMART `AFh`;
- printed p. 19: `AFh Power Loss Protection Failure`, last discharge-test result, minutes since last test, lifetime number of tests, status flags and threshold `10`;
- printed p. 24: SCT Feature Control code `0001h` for write cache and vendor feature `D000h` for `Power Safe Write Cache capacitor test interval`;
- §5.4: support for `SMART RETURN STATUS`.

This is the strongest 2012 product-contract anchor. It proves that the named drive exposes the relevant **test state**, **thresholded health surface**, **write-cache control surface**, and **test-cadence control surface** as distinct interfaces.

It does **not**, on the inspected pages, say:

- `AFh failure automatically disables write cache`;
- what exact internal event maps AFh threshold crossing to a cache-state change;
- what happens to already-cached writes at that transition;
- whether a host can immediately re-enable caching after such a failure;
- how behavior varies by firmware revision.

Those distinctions are preserved below.

### 1.2 Tom's Hardware — contemporary named-product secondary witness, 31 January 2013

Drew Riley, **“Intel SSD DC S3700 Review: Benchmarking Consistency,”** Tom's Hardware, published **31 January 2013**:

<https://www.tomshardware.com/reviews/ssd-dc-s3700-enterprise-storage,3352-2.html>

In the hardware discussion of the 200 GB and 800 GB S3700 samples, the review describes the capacitor bank used to commit write-cache data to NAND during power loss. It then reports that Intel uses sensor logic to periodically check capacitor health, and that outright failure or degraded performance **triggers a SMART event and disables write caching**.

This source is valuable because it is:

- period-adjacent to the product launch;
- explicitly about the named S3700;
- consistent with the 2012 Intel specification's independently visible self-test, AFh threshold surface, write-cache feature, and test cadence.

But its evidence class is bounded. The article does not show:

- a raw SCT/SMART command transcript before and after induced capacitor degradation;
- a firmware version matrix;
- a scope trace of the capacitor-fault transition;
- proof that the wording came from a public Intel normative document rather than briefing material or reviewer explanation.

Therefore the article supports **contemporary product reporting of the coupling**, not a manufacturer-primary command-level contract.

### 1.3 Open Compute Project v1.0 — institutional/datacenter requirement, 28 March 2023

Open Compute Project, **_Datacenter SAS-SATA Device Specification_**, Version **1.0 (03282023)**, authors/contributors listed from HPE, Meta, and Microsoft:

<https://www.opencompute.org/documents/datacenter-sas-sata-device-specification-rev-1-0-pdf>

Directly inspected:

- p. 6, `WCH-4`: a device is responsible for temporarily or permanently disabling write caching if current operating conditions indicate normal writes are at risk;
- p. 14 in the rendered PDF (`SATA-19`, PDF page index 13): if an SSD has PLP, it must periodically test PLP even if power is never removed;
- the same requirement says PLP must have sufficient charge to back up all user data and/or metadata in cache;
- if PLP fails or degrades below that guarantee, the device must:
  - flush all cached writes to NAND;
  - disable volatile write cache if enabled;
  - generate a SMART trip for `Power Loss Protection Failure`;
  - clear `WCE` in IDENTIFY DEVICE word 85 bit 5;
  - reject host attempts to enable write cache with `ABRT`.

This is not an ATA standard and is not treated as one. It is a later OCP datacenter device specification: a procurement/interface requirement that turns a broad safe-degradation principle into explicit externally testable behavior.

### 1.4 Chronology discipline

The source sequence is therefore:

```text
October 2012 — Intel product contract
    self-test + AFh thresholded health state
    + write-cache Feature Control
    + D000h test cadence

31 January 2013 — contemporary secondary named-product report
    capacitor degradation/failure
        -> SMART event
        -> write caching disabled

28 March 2023 — OCP datacenter specification v1.0
    PLP periodic test
        -> insufficient guaranteed hold-up energy
        -> flush + disable cache + SMART trip + clear WCE + reject re-enable
```

This sequence is **not** a genealogy. Ten years of intervening product, hyperscaler, standards, and procurement history remain unresearched here.

---

## 2. Historical / interface record

### 2.1 Intel's 2012 interface already separates health evidence from cache authority

The S3700 specification does not encode PLI readiness and write caching as one field.

Instead it exposes at least:

```text
AFh
    -> Power Loss Protection Failure / test-state surface

0001h SCT Feature Control
    -> write-cache control

D000h SCT Feature Control
    -> capacitor-test interval
```

This matters because a system can, in principle, observe or alter these relations independently.

The health result describes the support infrastructure. The write-cache feature describes whether the host/device path may use a volatile optimization. The cadence controls when new health evidence should be produced.

### 2.2 AFh is not merely a passive lifetime counter

In the October-2012 SMART table, AFh is marked with a threshold value of `10` and the `PW` pre-fail flag. Its raw content includes the latest capacitor-discharge test, elapsed minutes since the last test, and lifetime test count.

That structure differs from `AEh Unexpected Power Loss`, whose role is cumulative event history and which has no corresponding threshold in the table.

The relation is therefore already typed:

```text
AEh
    -> history that an external class of event occurred

AFh
    -> evidence that the apparatus intended to survive that class of event remains qualified
```

The present note does not infer the complete SMART trip algorithm from the table alone. The stronger host-visible trip sequence comes from the later OCP requirement.

### 2.3 Contemporary S3700 reporting couples negative health to degraded write behavior

Tom's Hardware reports a further product behavior not stated on the inspected Intel pages: if the periodic capacitor-health logic finds outright failure or degraded performance, the drive generates a SMART event and disables write caching.

At the level of engineering relations, that means the self-test can be more than an alert source:

```text
health test fails / degrades
    -> ordinary assumption behind volatile write caching no longer holds
    -> write-cache authority withdrawn
```

Because the witness is secondary, the repository does not promote this into an exact Intel firmware-state-machine claim.

### 2.4 OCP 2023 makes the safe-degradation sequence explicit

`SATA-19` in OCP v1.0 is unusually valuable for retention analysis because it does not stop at `report failure`.

The required sequence contains several distinct operations:

```text
PLP becomes insufficient
    -> flush already-cached writes to NAND
    -> disable volatile write cache
    -> publish failure through SMART
    -> publish WCE=0 through IDENTIFY DEVICE
    -> reject host attempts to restore the unsafe mode
```

The sequence therefore separates:

- settling already accepted work;
- changing future write semantics;
- reporting the degraded state;
- defending the degraded state against an incompatible host request.

### 2.5 A health failure can alter command admissibility

The last OCP requirement is particularly important. `WCE=0` is not only diagnostic telemetry; attempts to enable write cache are to be rejected.

Thus:

```text
health evidence
    !=
passive observability only
```

Instead, under this later institutional contract:

```text
negative health evidence
    -> changes which host-requested state transitions are admissible
```

That is a distinct retention relation: **evidence about the durability apparatus participates in authorization of future performance behavior**.

---

## 3. Engineering reconstruction

### 3.1 Retention infrastructure can gate optimization authority

Volatile write caching is valuable because acknowledgement can be decoupled from immediate NAND completion. That optimization is defensible only if the device has another mechanism that preserves already-acknowledged state across the relevant failure boundary.

With PLP:

```text
volatile write cache
    + qualified hold-up-energy path
    -> cache can participate in the advertised persistence contract
```

If qualification is lost:

```text
volatile write cache
    + unqualified hold-up-energy path
    -> same operating mode carries a different data-loss risk
```

The later OCP rule responds by revoking the operating mode rather than pretending the infrastructure state is irrelevant.

### 3.2 Failure evidence creates a transition obligation, not merely an alert

A diagnostic-only model would be:

```text
self-test fails
    -> log / alert
    -> continue unchanged
```

The OCP model is stronger:

```text
self-test / health regime establishes insufficiency
    -> settle vulnerable cached state
    -> change future operating mode
    -> expose changed mode
    -> prevent immediate host override
```

This is a useful example of **negative evidence producing maintenance/control work**.

### 3.3 Flush and disable are different operations

`flush cached writes` and `disable volatile write cache` are not synonyms.

The first concerns state already admitted under the old operating regime. The second concerns what future writes may do.

Therefore:

```text
retire old risk-bearing mode safely
    =
settle prior obligations
    +
change future admission semantics
```

Skipping the first step could strand previously acknowledged volatile state. Skipping the second could immediately recreate the same unsafe dependence on failed PLP.

### 3.4 SMART trip and WCE state are different interfaces to the same degradation

The OCP requirement separately asks for:

- SMART failure reporting;
- `WCE=0` in IDENTIFY DEVICE;
- command rejection on attempted re-enable.

These are not one bit repeated three times conceptually.

They serve different relations:

```text
SMART trip
    -> health / failure reporting

WCE=0
    -> current capability/configuration exposure

ABRT on enable request
    -> enforcement of current admissibility
```

A host that can observe failure but still force the unsafe mode would have a different contract from one where the device enforces the safety boundary.

### 3.5 Periodic testing closes a temporal gap only if its result has consequences

A periodic self-test reduces the interval during which latent PLP degradation may go unnoticed. But periodicity alone does not define the operational consequence of a bad result.

Case 38 can now separate:

```text
when evidence is refreshed
    !=
what the evidence says
    !=
what the device does because of it
```

D000h belongs to the first relation. AFh belongs to the second. The write-cache revocation path belongs to the third.

### 3.6 Safe degradation is still not proof of payload correctness

Disabling write cache after PLP degradation narrows future exposure, but it does not establish that:

- every previously cached write was successfully flushed;
- NAND/controller metadata was internally consistent;
- every filesystem/database higher-layer invariant held;
- no other failure accompanied the capacitor problem.

Safe degradation is a **risk-control response**, not retrospective proof that no damage occurred.

---

## 4. State / authority matrix

| State or relation | 2012 Intel primary | 2013 S3700 secondary | 2023 OCP institutional requirement |
| --- | --- | --- | --- |
| periodic PLP/capacitor health testing | yes | yes | required |
| latest PLP health/test state | AFh | discussed via SMART event | SMART trip required on insufficiency |
| test cadence | D000h exposed | periodic checking described | periodic testing required |
| write-cache state/control | SCT Feature Control `0001h` | write caching said to be disabled on degradation/failure | disable volatile write cache required |
| flush already-cached writes on PLP failure | not stated on inspected page | not detailed | required |
| host-visible WCE cleared | not established here | not shown | required |
| host re-enable attempt rejected | not established here | not shown | required |
| exact S3700 firmware transition trace | no | no | not an S3700 source |

The matrix is intentionally asymmetric. The later OCP source is more explicit about behavior, but it is not evidence about a 2012 Intel firmware image.

---

## 5. Functional comparisons — not genealogy

### 5.1 Case 15 — emergency energy path versus permission to depend on it

Case 15 establishes the earlier Intel SSD 320 relation in which stored capacitor energy funds transfer from volatile controller state to NAND during power loss.

This Case 38 deepening adds a different question:

```text
a protection mechanism exists
    !=
current evidence says it remains qualified
    !=
the system should continue using an optimization that depends on it
```

The comparison is same-domain and partly same-vendor, but it does not establish identical controllers or firmware lineage.

### 5.2 Case 20 — Flush/FUA versus device-internal safe degradation

Case 20 concerns host-visible commands/order semantics that request durable completion behavior.

The OCP PLP-failure sequence is different: the device changes whether volatile write caching is available at all when its supporting retention infrastructure is no longer trustworthy.

Thus:

```text
host asks for a persistence boundary
    !=
device withdraws an unsafe optimization because its physical support failed
```

No protocol genealogy is claimed.

### 5.3 Proactive integrity scans — discovering payload risk versus discovering infrastructure risk

Scrub / patrol-read cases proactively inspect stored payload or redundancy so latent media errors can be found before a later demand read or second failure.

PLI self-test proactively inspects the **apparatus that will protect future in-flight state**.

The shared functional structure is:

```text
latent risk
    -> proactive test
    -> evidence
    -> corrective / restrictive action
```

The verified object and corrective action differ, so the analogy remains bounded.

---

## 6. Philosophical interpretation — capability is conditional, not merely possessed

A narrow project-level interpretation is now available:

> A technical system may not simply “have” a durability capability. It may continuously qualify that capability, and negative qualification evidence can revoke the system's permission to operate in a mode that presupposes the capability.

That strengthens the case's earlier `maintenance-of-maintenance` point without turning a SMART attribute into a philosophical subject.

The relevant relation is operational:

```text
capability installed
    !=
capability currently qualified
    !=
authority to depend on that capability
```

The interpretation remains bounded. Intel and OCP do not use the project's terms `authority`, `qualification closure`, or `retention-infrastructure readiness` as philosophical vocabulary.

---

## 7. Explicit non-claims

This deepening does **not** claim that:

1. Intel invented PLP, capacitor-backed write caching, SMART, health self-test, or cache-disable-on-failure behavior;
2. the October-2012 S3700 specification explicitly says AFh failure disables write cache;
3. AFh threshold value `10` by itself proves the exact S3700 cache-disable state machine;
4. Tom's Hardware is a manufacturer-primary or standards source;
5. the 2013 review includes an induced-capacitor-failure command trace;
6. every S3700 firmware revision behaves exactly as the 2013 review describes;
7. S3500 behavior is proven identical by the S3700 review;
8. the 2023 OCP specification is an ATA, SATA-IO, ANSI, or JEDEC standard;
9. OCP `SATA-19` retroactively defines the S3700 product contract;
10. OCP copied this requirement from Intel;
11. Intel's S3700 directly caused the later OCP requirement;
12. the same internal threshold or energy margin is used by S3700 and OCP-conforming later devices;
13. a SMART trip and a WCE-bit change are the same interface action;
14. disabling write cache proves all previously acknowledged writes reached NAND safely;
15. a successful flush proves all hidden FTL metadata is consistent;
16. cache disablement repairs failed capacitors;
17. host-visible `WCE=0` alone proves the physical PLP path is absent or failed;
18. rejecting re-enable requests defines how or when a device may later recover from the degraded state;
19. periodic PLP testing guarantees immediate detection of every degradation mode;
20. safe degradation guarantees higher-layer filesystem or database durability;
21. the 2012-to-2023 sequence establishes a continuous documented genealogy;
22. a risk-bearing optimization should always be disabled on every warning condition in every storage system.

---

## 8. Claim ledger

| Claim | Type | Evidence status |
| --- | --- | --- |
| October-2012 S3700 exposes capacitor self-test and AFh `Power Loss Protection Failure` | H/P | strong: Intel 328171-001US |
| AFh carries last discharge-test result, minutes since last test, lifetime test count, threshold 10 and pre-fail flag | H/P | strong: Intel 328171-001US printed p. 19 |
| same 2012 product exposes write cache as SCT Feature Control `0001h` | H/P | strong: Intel 328171-001US printed p. 24 |
| same 2012 product exposes capacitor-test interval as vendor Feature Control `D000h` | H/P | strong: Intel 328171-001US printed p. 24 |
| 2013 Tom's Hardware reports S3700 capacitor degradation/failure triggers SMART event and disables write caching | H/S | useful contemporary secondary named-product witness |
| OCP v1.0 is dated 28 March 2023 and authored/contributed by HPE/Meta/Microsoft participants | H/P | strong institutional-primary source |
| OCP SATA-19 requires periodic PLP tests on PLP-equipped SATA SSDs | H/P | strong: OCP v1.0 p. 14 |
| OCP SATA-19 requires flush then volatile-cache disable on insufficient PLP charge | H/P | strong: OCP v1.0 p. 14 |
| OCP SATA-19 separately requires SMART trip, WCE=0, and rejection of re-enable attempts | H/P | strong: OCP v1.0 p. 14 |
| readiness evidence can gate authority to use a risk-bearing volatile optimization | E | strongly supported by OCP's explicit transition sequence; compatible with 2013 S3700 reporting |
| flushing prior cached data and disabling future cache use are different obligations | E | directly reconstructed from ordered distinct OCP requirements |
| S3700 and OCP share a proven design genealogy | H | **not established** |

`H/P` = historical/interface record from primary source.  
`H/S` = historical report from a secondary source.  
`E` = engineering reconstruction.

---

## 9. Relation to the existing D000h persistence deepening

[`38-intel-s3700-sct-test-cadence-persistence-boundary-deepening.md`](38-intel-s3700-sct-test-cadence-persistence-boundary-deepening.md) asks how long the **policy controlling test cadence** may remain authoritative across resets.

This note asks what happens after health evidence says the **protected operating assumption** is no longer valid.

They should remain distinct:

```text
cadence-policy persistence
    -> when should another test occur?

health-result interpretation
    -> does the protection path remain qualified?

write-cache authority
    -> may the device continue using a volatile optimization that depends on PLP?
```

Device-specific D000h power-cycle behavior is still unverified by direct S3700 hardware transcript. The new evidence does not close that debt and should not be presented as doing so.

---

## 10. Related-repository routing

A fresh search of `tmzncty/computing-archaeology` for `S3700`, `PLI`, `D000h`, and capacitor-test terms found no dedicated packet to reuse.

This note therefore keeps only the retention-specific seam here:

```text
readiness test
    -> negative readiness evidence
    -> settlement of already-exposed volatile state
    -> withdrawal of future volatile-cache authority
    -> host-visible degraded capability
```

The following broader work belongs primarily in `computing-archaeology`:

- the genealogy of enterprise SSD capacitor-backed write caches;
- Intel controller/firmware evolution from SSD 320/710 to S3700/S3500;
- the precise provenance of the 2013 reviewer statement;
- Facebook/Meta/Microsoft/HPE datacenter-drive requirement history before OCP v1.0;
- ATA/SCT/SMART command genealogy beyond the bounded interface relation used here;
- capacitor chemistry, aging curves, replacement/service practice, and vendor implementation details.

---

## 11. Remaining evidence debt

This slice closes the broad conceptual question **whether readiness failure can participate in revoking a durability-dependent optimization**: the 2013 S3700 reporting supplies a named-period product witness, and OCP 2023 supplies an explicit later institutional requirement.

The remaining debt is narrower:

1. **Manufacturer-primary S3700 coupling witness:** locate an Intel public document that explicitly states the cache-disable behavior on capacitor degradation/failure, if one survives.
2. **Device transcript:** capture S3700/S3500 SMART/IDENTIFY/write-cache state before and after an induced or emulated PLI failure, with firmware revision recorded.
3. **Transition atomicity:** determine how the device handles cached writes if the capacitor self-test fails while writes are active.
4. **Recovery semantics:** establish what event permits cache re-enable after a transient/excess-temperature test result versus a permanent PLP failure.
5. **OCP chronology:** trace whether `SATA-19` existed in pre-2023 hyperscaler/vendor requirements or draft lineage.
6. **S3500/S3700 divergence:** verify whether both families use the same fail-safe write-cache policy.

These are appropriate future slices. They do not justify expanding this note into a general enterprise-SSD history.