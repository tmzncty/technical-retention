# JEDEC JESD218 SSD Endurance Qualification: Workload-Qualified TBW and Power-Off Retention

## Status

**`grounded`** — bounded to the September 2010 JESD218 SSD-level endurance/retention qualification relation, with Intel's June 2012 retention application note used to expose the difference between standardized TBW and actual media wear, and Intel's September 2015 DC P3608 specification used as a named commercial product witness. Prior-art deepening now also separates the earlier JESD22-A117 device-level program/erase-endurance-and-retention test family from JESD218's later SSD-level host-TBW service contract, using a 2006 Renesas standards inventory, JEDEC's own later revision ledger, and a 2002 IEEE post-cycling retention paper. The 2010→2012 workload chronology is now further bounded by July 2012 JESD219A publication metadata and its separately distributed Master/Test Trace artifacts; this does not substitute for direct inspection of the normative JESD219A body. A January 2026 HPE QuickSpecs/product witness now adds a named QLC P5430 SKU to the commercial-product layer, while keeping its QLC media label, workload label, write-endurance rating, and post-endurance power-off retention statement separate from raw-cell physics or an independently audited JESD218 compliance claim. The same QuickSpecs now also supplies a bounded 7.68 TB TLC CM7 cross-check, used only to compare product-level endurance/retention contracts rather than to infer a universal TLC-versus-QLC media law.

Grounding record: [`../evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md`](../evidence/76-jedec-2000-2015-ssd-endurance-retention-grounding.md).

## Scope

This case asks a narrow question left open by Cases 36, 37, and 55:

> When an SSD is given an endurance rating in host-written terabytes, what exactly is being promised about retention at that rating, and how is that promise related to workload, internal media wear, power state, and later read correctness?

The bounded object is **JESD218's SSD-level qualification relation**. It is not:

- a NAND cell-physics history;
- an assertion that TBW is the instant at which an SSD physically fails;
- a claim that all SSDs have one universal shelf life;
- a claim that client SSDs inherently retain data longer than enterprise SSDs under all conditions;
- a replacement for JESD219 workload history;
- a named-controller wear-leveling implementation study;
- a claim about secure erasure or forensic disappearance;
- an invention-priority claim for endurance or data-retention testing.

The central historical source is JEDEC **JESD218, _Solid-State Drive (SSD) Requirements and Endurance Test Method_, September 2010**.[^jesd218]

---

## Historical vocabulary

JESD218 itself defines or uses:

- `Data Retention`;
- `Endurance`;
- `Endurance Rating (TBW rating)`;
- `Host writes`;
- `Program/erase cycle (p/e cycle)`;
- `Workload`;
- `Write amplification factor (WAF)`;
- `Wear leveling`;
- `Retention failure`;
- `Functional Failure Requirement (FFR)`;
- `Uncorrectable Bit Error Rate (UBER)`;
- `Client` and `Enterprise` application classes;
- `Active Use (power on)` and `Retention Use (power off)`.

The phrases **qualification relation**, **wear-conditioned retention**, **rating boundary**, and **power-off retention contract** below are project engineering reconstructions. They are not substituted for the standard's vocabulary.

Intel's 2012 application note additionally uses `Media Wearout Indicator` when explaining its own SSD products.[^intel-ret]

---

## Historical record

### Device-level program/erase endurance and retention qualification predates the SSD-level TBW relation

JESD218 itself cites **JESD22-A117, _Electrically Erasable Programmable ROM (EEPROM) Program/Erase Endurance and Data Retention Stress Test_**.[^jesd218] A Renesas Technology reliability handbook dated August 31, 2006 lists `JESD22-A117` in its JEDEC standards table as established in **2000**.[^renesas2006] This is manufacturer-retrospective standards evidence rather than a directly inspected original 2000 JEDEC facsimile, so the bounded historical claim is only that the A117 device-level test family existed by 2000.

JEDEC's later **JESD22-A117E** retains an informative predecessor ledger. It identifies `JESD22-A117B` as the **March 2009** predecessor to A117C and records, among the changes from A117A to A117B, a read-disturb addition to the retention definition, a new `Uncorrectable bit error rate` definition, bad-block-aware endurance-failure wording, transient-error handling, and UBER calculation.[^a117e] Because this evidence comes from a later JEDEC revision ledger, it establishes revision-level terminology by A117B; it does **not** prove that A117B invented read disturb, UBER, bad-block management, or endurance testing.

A separate period technical witness predates both A117B and JESD218. Belgal et al.'s 2002 IEEE IRPS paper describes stress-induced leakage after Flash program/erase cycling, fits data from several technology generations and multi-year bakes, and reports that the affected fraction scales with cycle count.[^belgal2002] This grounds a physical reason why **post-cycling retention** is not the same question as retention of an otherwise identical but uncycled cell.

Together these sources block a false chronology:

```text
JESD218 (2010)
    != origin of cycling-conditioned data-retention qualification
    != origin of UBER/read-disturb vocabulary in JEDEC NVM qualification
```

The bounded contribution of JESD218 in this case is different: it composes a **whole-SSD**, host-visible endurance rating in TBW with application-class workload, capacity, UBER/FFR, and a subsequent power-off retention requirement.

### JESD218 makes endurance and retention separate concepts, then composes them

JESD218 defines `Data Retention` as the SSD's ability to retain data over time and `Endurance` as the ability to withstand multiple rewrites. Its `Endurance Rating (TBW rating)` is then the number of host-written terabytes for which the drive must still satisfy the requirements of section 6.2.[^jesd218]

Section 6.2 makes that rating a bundle rather than a single-media-wear number. At the stated TBW, under the workload associated with the application class, the drive must still:

- maintain advertised user capacity;
- meet the class UBER requirement;
- meet the class FFR requirement; and
- retain data with power off for the class-required time.[^jesd218]

Thus the standard itself blocks the shortcut:

> **endurance ≠ data retention**.

The rating deliberately composes both.

### The rating is expressed at the host interface, not as a raw NAND cycle count

JESD218 defines `Host writes` as data transmitted through the primary SSD interface for writing. It separately defines WAF as data written to NVM divided by data written by the host, and notes that WAF depends on workload and may vary over device life. Its TBW note also names wear-leveling quality, WAF, NAND cycling capability, and workload as factors affecting the rating.[^jesd218]

Therefore the period standard already distinguishes:

```text
host-written TB
        !=
internal NVM writes / P-E cycling
```

A TBW value is deliberately user-visible, but it is mediated by controller and workload behavior below that interface.

### JESD218 uses a two-phase life model

Section 6.3 states a use scenario in which SSDs are actively used and written to their endurance ratings, **followed by a power-down period in which data must be retained**.[^jesd218]

Its 2010 Table 1 defines two standard classes:

| Application class | Workload | Active use | Retention use, power off | FFR | UBER |
| --- | --- | --- | --- | --- | --- |
| Client | Client / JESD219 | 40 °C, 8 h/day | 30 °C, 1 year | ≤3% | ≤10^-15 |
| Enterprise | Enterprise / JESD219 | 55 °C, 24 h/day | 40 °C, 3 months | ≤3% | ≤10^-16 |

The table values are **class qualification conditions**, not universal physical constants. JESD218 explicitly says the active-use and retention-use columns refer to different periods and that retention-use time is the period over which data must remain with power off.[^jesd218]

### The September 2010 standards pair was not workload-complete for both classes

The original JESD218 and JESD219 were published as a pair in September 2010, but their coverage was not yet symmetrical. JESD218 Table 1 already defines both `Client` and `Enterprise` application classes and points the workload column to JESD219.[^jesd218] The September 2010 JESD219, however, contains only an `Enterprise endurance workload` section and explicitly says that the client workloads were still under development and would be added when available.[^jesd219-2010]

That creates a release-bounded historical distinction that the earlier Case 76 text did not make explicit:

> **application-class requirement specified ≠ complete companion workload available in the same publication moment**.

This does not mean that JESD218 lacked a client retention requirement. The one-year, 30 °C power-off condition and the client UBER/FFR requirements are already present in the September 2010 JESD218. It means more narrowly that the referenced workload standard did not yet supply a normative client workload alongside its enterprise workload in that original issue.

A contemporaneous August 2011 presentation by Alvin Cox, chairman of JEDEC JC-64.8, names `JESD218A`, describes both client and enterprise workload work under JESD219, and labels the client workload as based on a real trace including TRIM. The same presentation says one client-test detail — testing at 100% full — was still under discussion.[^cox2011] This is useful committee-chair evidence that the standards pair was evolving, but it is not silently substituted for a directly inspected normative JESD219 revision.

The bounded chronology therefore remains:

```text
September 2010 JESD218
    defines Client + Enterprise endurance/retention classes

September 2010 JESD219
    supplies Enterprise endurance workload
    + explicitly says Client workload is still under development

by August 2011
    JC-64.8 chair presents JESD218A
    + an evolving JESD219 Client workload
```

Direct facsimile archaeology of JESD218A and the later normative JESD219A client-workload text remains open. The purpose of this deepening is to prevent later revisions from being silently projected backward into September 2010.

### By July 2012 the client workload had become a standard-plus-trace artifact set

A later publication boundary can now be grounded without pretending that a standards-catalog record is a substitute for the full normative text. Accuris's JEDEC catalog records **JESD219A, _Solid-State Drive (SSD) Endurance Workloads_**, as a 26-page standard published **1 July 2012**. Its description says that the workloads are used with JESD218 and explicitly points to separate `JESD219A_MT` and `JESD219A_TT` **supporting trace files**.[^jesd219a-catalog]

The companion catalog records make the client-workload embodiment more concrete. `JESD219A_MT`, **Master Trace for 128 GB SSD**, is described as a supporting file for implementing the endurance-verification client workload. The record says that it represents actual SSD activity over **seven months**, applies to client endurance verification for user capacities of at least 64 GB, can serve directly as the test trace for 128–256 GB devices with its existing LBA range, and can be compressed or expanded for other capacities under the stated maximum-LBA relation.[^jesd219a-mt]

`JESD219A_TT`, **Test Trace for 64 GB–128 GB SSD**, is separately described as a trace **derived from the 128 GB Master Trace** using the compression method in JESD219, with the same workload characteristics except that its maximum LBA represents 64 GB of user capacity.[^jesd219a-tt]

This closes a narrower gap than direct normative facsimile archaeology. It establishes that, by July 2012, the client workload was no longer merely a committee presentation or an unfinished promise in the September 2010 issue: JEDEC's cataloged revision had named supporting workload artifacts, including a captured Master Trace and a derived Test Trace. It does **not** establish every clause, preconditioning rule, trace transformation algorithm, or later revision change inside the full JESD219A text.

The retention-specific point is also narrower than a generic workload-history claim. The trace files are not the SSD payload being protected. They are retained **workload history/control input** used to reproduce a qualification stress relation later. That gives a useful engineering decomposition:

```text
application-class requirement
    !=
workload-standard prose
    !=
captured Master Trace history
    !=
capacity-adapted Test Trace
    !=
endurance-stress execution
    !=
JESD218 qualification verdict
    !=
later power-off retention interval
```

From the artifact descriptions alone, several boundaries follow:

> **workload-standard text ≠ supporting trace artifact**;

> **Master Trace ≠ derived Test Trace**;

> **workload role continuity ≠ one fixed LBA geometry**;

> **seven months represented by the source trace ≠ the later JESD218 power-off retention interval**.

The first three are historical-record-plus-engineering boundaries around the July 2012 artifact set. The last is a cross-document engineering reconstruction: one interval characterizes the history represented by the workload source, while JESD218's retention-use interval is a separate post-endurance service requirement. Neither should be silently substituted for the other.

### Retention qualification is controller-inclusive and statistically bounded

The original 2010 JESD218 also gives a stronger boundary than a simple `one year` or `three months` slogan.

First, clause 7.1.1 makes endurance/retention verification a **sample-based qualification exercise**: the sample must be large enough to establish the FFR and UBER requirements at 60% confidence.[^jesd218] This does not turn the standard into a deterministic countdown for every individual drive.

Second, Annex D treats useful retention as an SSD-level recoverability relation rather than a requirement for physically error-free NAND. It permits raw bit error rate (`RBER`) to grow with cycling and retention time, then requires the extrapolated RBER to remain below the SSD controller's ECC capability. It also warns that the ECC calculation assumes randomly distributed errors more perfectly than real devices provide, so a safety margin is required for device-to-device and location-to-location variation.[^jesd218]

This supports two engineering reconstructions:

> **raw-media bit errors ≠ host-visible data loss**

and

> **retention qualification ≠ zero raw errors in the NVM**.

ECC is part of the qualified recovery relation. This does not imply that ECC creates unlimited retention: the extrapolated raw-error population still has to remain inside a guarded correction envelope.

Third, the Table 1 temperatures are explicitly use-period temperatures for endurance/retention estimation, not datasheet absolute maxima/minima. Informative Annex C then shows that the expected retention duration changes when active-use or power-off temperature changes; its example maps the standard client condition (40 °C active, 30 °C power off) to 52 weeks, but a 25 °C power-off condition to at least 105 weeks under the stated model.[^jesd218]

So the historically defensible claim is not `client SSDs retain for one year` as a substrate constant. It is:

> **the September 2010 client qualification relation requires one year of power-off retention at its specified class conditions, under the standard's test/model/error criteria**.

The model-dependent Annex C extrapolation is not generalized here to every later NAND generation, charge-trap implementation, TLC/QLC device, controller ECC design, or storage environment.

### Verification may be accelerated without changing the target use condition

Clause 7 says endurance verification is followed by retention verification. In the direct method drives are stressed to stated TBW using specified workloads and then retention-tested; because the use-time retention requirements are long, extrapolation or acceleration is used to validate the requirement.[^jesd218]

Hence:

> **accelerated qualification chronology ≠ ordinary user chronology**.

A high-temperature bake or extrapolation is evidence about an intended use-condition relation under the specified model; it is not a statement that the drive literally spent the same wall-clock time in ordinary use.

---

## Named manufacturer witnesses

### Intel 2012: TBW and media wear can diverge

Intel's June 2012 application note explains JESD218A through its own NAND/SSD retention model. It says powered-on internal data movement can refresh data, while such moves are impossible during a powered-off retention interval.[^intel-ret]

More importantly for the qualification boundary, Intel separates:

- a **TBW rating**, based on a reference workload; from
- its **Media Wearout Indicator**, based on actual NAND P/E-cycle consumption.

Intel warns that actual workload can cause one limit to be reached before the other. For the Intel SSD 320, its own plotted model also shows retention changing strongly with accumulated media wear and says the overall 30 °C retention at the media-wearout limit is about one year, while less-worn states can retain substantially longer.[^intel-ret]

Therefore:

> **TBW rating ≠ physical-media wearout state**.

And:

> **qualification minimum ≠ product-specific upper bound**.

### Intel 2015 P3608: a named enterprise product contract

Intel's September 2015 DC P3608 product specification states that the series meets or exceeds JESD218 endurance and retention requirements. Its reliability table defines data retention as retention in NAND at maximum rated endurance and specifies **three months of power-off retention once rated write endurance is reached at 40 °C**. The same table gives PBW endurance ratings and links endurance verification to JESD218.[^p3608]

This is a named commercial witness for the enterprise-class relation. It is not evidence that every SSD implements the same hidden wear-management mechanism.


### HPE 2026 P5430: a named QLC product witness without a substrate shortcut

HPE's **5 January 2026** _HPE Solid State Disk Drives_ QuickSpecs Version 72 lists the P5430 family under `NVMe Main Performance Very-read-optimized EDSFF E3.S SSDs`. The exact **P63934-B21** 7.68 TB SKU is labeled `VRO`, `NVMe`, `E3.S`, and **`QLC`**; the corresponding speeds/endurance table gives **8,040 TB lifetime writes** and **0.57 DWPD**.[^hpe-qspec] HPE's product page independently describes the P5430 family as using **Next Gen QLC 3D NAND**.[^hpe-p5430]

The same QuickSpecs defines `Data Retention` as retaining NAND data after the **maximum rated endurance level** has been reached, and states that these SSDs are rated for **three months with no power applied once maximum rated write endurance is reached**.[^hpe-qspec]

This gives a named modern QLC commercial witness for the same broad end-of-endurance → unpowered-retention relation that Case 76 studies, but it must not be overread. The cited HPE rows do **not** disclose the P5430's raw-cell retention curve, ECC/retry budget, over-provisioning, wear distribution, refresh policy, or qualification raw data. Nor does the cited P5430 row itself say `JESD218`; the HPE statement is therefore retained here as a manufacturer/OEM product-family contract, **not** silently promoted into an independent JEDEC-compliance certificate.

The bounded decomposition is:

```text
QLC media label
    !=
product workload label (VRO)
    !=
lifetime-write / DWPD endurance rating
    !=
post-endurance unpowered retention requirement
    !=
raw NAND-cell retention law
```

In particular, the fact that HPE's product-family statement also uses a three-month interval does not prove that the P5430 reached that number through the identical test path, temperature condition, controller margin, or standards revision used by the September 2010 JESD218 enterprise row.


### HPE 2026 CM7: a same-capacity TLC cross-check, not a media-only experiment

The same **5 January 2026** HPE QuickSpecs provides a useful control against overreading the P5430's QLC label. The exact **P61183-B21** CM7 SKU is also **7.68 TB** and E3.S/NVMe, but HPE classifies it as **Read Intensive (`RI`)**, **Gen5 High Performance**, and **`TLC`**. Its corresponding speeds/endurance row gives **14,016 TB lifetime writes** and **1 DWPD**.[^hpe-qspec]

Because the QuickSpecs' `Data Retention` clause applies the same **three-month, no-power, post-maximum-rated-write-endurance** statement to the listed SSD family, the document supplies a bounded commercial comparison in which two equal-capacity products carry different media labels and different rated-write envelopes while remaining under the same family-level post-endurance retention clause.[^hpe-qspec]

That is useful precisely because it does **not** isolate NAND density as a causal variable. The products also differ in workload class (`RI` versus `VRO`), product/controller generation, performance positioning, and likely implementation details that the QuickSpecs does not disclose. Therefore:

```text
same nominal capacity (7.68 TB)
    !=
same workload class
    !=
same media label
    !=
same lifetime-write / DWPD rating
    !=
same controller or product generation

and

same product-family retention clause
    !=
same prior endurance history
    !=
same raw-cell retention law
```

The historically supportable product statement is narrow: **HPE documented a 7.68 TB TLC CM7 at 14,016 TB / 1 DWPD and a 7.68 TB QLC P5430 at 8,040 TB / 0.57 DWPD in the same QuickSpecs family, whose general data-retention clause states three months unpowered after maximum rated write endurance.** It is not evidence that TLC intrinsically has a particular multiple of QLC endurance, that the two drives use the same controller/ECC margin, or that equal capacity makes the pair a controlled media-physics experiment.

---

## Engineering reconstruction

### Device qualification and drive qualification operate at different interface levels

The A117 family and JESD218 should not be collapsed merely because both use `endurance`, `retention`, and later `UBER` vocabulary. A117 is a device/cell/module qualification method for reprogrammable nonvolatile memories; JESD218 deliberately expresses its endurance boundary in **host-written terabytes** for an SSD and composes that boundary with controller/workload effects and drive-level capacity/error/failure requirements.

Project reconstruction:

```text
cell / device cycling-retention qualification
        can inform
SSD controller + media design and qualification
        but is not identical to
host-visible SSD TBW + service-envelope qualification
```

The distinction matters because controller write amplification, wear leveling, bad-block replacement, ECC, and workload can mediate the relation between one host write and the physical stress experienced by individual NVM cells. Lower-level qualification evidence can therefore underwrite a higher-level service contract without becoming that contract.

### Rated endurance is a qualification boundary, not an instant physical death line

The standard says the drive must meet a set of requirements **through the stated rating**. It does not say the first write beyond TBW instantaneously destroys the payload, nor does it define TBW as the physical P/E limit of every NAND block.

Therefore:

> **SSD endurance rating ≠ instant failure threshold**.

This distinction is reinforced by Intel's separation of reference-workload TBW from actual media P/E wear.

### Power-loss durability is not the same problem as power-off retention duration

Cases 15 and 20 ask whether an acknowledged/flush-qualified write reaches a recoverable nonvolatile state across an interruption. JESD218 asks a later question: after the endurance phase and power-down, can the already-written data still be read correctly after a specified **unpowered interval**?

So:

> **power-fail durability handoff ≠ power-off retention interval**.

A drive may correctly flush data to nonvolatile media and still face finite long-term retention after sufficient wear. Conversely, a long-retention medium does not prove that an acknowledged write had crossed the required persistence boundary before sudden power loss.

### Powered refresh opportunity is excluded by the qualification interval itself

Intel notes that internal data movement while powered can refresh data and that such movement is impossible while the drive is powered off.[^intel-ret]

That makes JESD218's retention-use phase especially useful beside Cases 36 and 37:

> **powered maintenance opportunity ≠ power-off retention qualification**.

The standard's retention requirement cannot silently assume background controller rewriting during the specified off interval.

### Application class is part of the rating relation

The client and enterprise rows differ in workload, active-use temperature/duty, retention-use temperature/time, and UBER target. It is therefore invalid to interpret the one-year versus three-month values as a substrate-only ranking.

> **client 1 year at 30 °C ≠ enterprise 3 months at 40 °C as an inherent-media ordering**.

They are different qualified service models.

### Retention duration is conditional on prior history

In this case `retention time` cannot be treated as one timeless material constant. The qualification relation includes prior endurance stressing, workload, temperature, and a declared rating. Intel's product analysis further shows the same drive family can have different expected retention at different wear states.[^intel-ret]

Project reconstruction:

```text
retention claim
    = relation among
      current payload recoverability
      + prior write/wear history
      + workload/controller amplification
      + temperature history
      + powered/unpowered phase
      + required error/failure criteria
```

This is an analytical decomposition, not JEDEC's philosophical vocabulary.

---

## Failure and forgetting boundaries

Several different failures must remain separate:

- exceeding a host TBW rating;
- reaching a media wearout estimate;
- exhausting ECC/error margin during a later read;
- failing the UBER or FFR qualification criterion;
- losing data during the powered-off retention interval;
- losing an acknowledged write before it ever reached the intended persistence boundary;
- logical deallocation or sanitization;
- controller telemetry reporting a high wear estimate.

In particular:

> **rated endurance ≠ secure erase / forgetting**.

TBW provides no claim that data is erased when the rating is reached or exceeded.

---

## Prior art and anti-anachronism

The prior-art boundary is now stronger than the earlier observation that JESD218 merely cites A117.

- Renesas's 2006 manufacturer handbook inventories **JESD22-A117** as established in **2000**.[^renesas2006]
- Belgal et al. 2002 independently document program/erase-cycling-conditioned Flash retention physics.[^belgal2002]
- JEDEC's own later A117E revision ledger identifies **A117B (March 2009)** and records that A117B added UBER definition/calculation and read-disturb wording to the A117 family.[^a117e]
- JESD218 then cites A117 while defining a distinct SSD-level qualification relation.[^jesd218]

Therefore this repository does **not** claim that JESD218 invented cycling-plus-retention testing, cycling-conditioned retention physics, read-disturb vocabulary, or UBER as a NVM reliability metric. Nor does the later A117E revision ledger establish invention priority for any of those concepts; it establishes only what that standards family says changed between revisions.

The bounded historical contribution used here remains more specific:

> by September 2010, JESD218 standardized an **SSD-level**, application-class-specific endurance rating expressed as host TBW and tied it to workload, capacity, UBER/FFR, and a subsequent power-off retention requirement, above an already-existing device-level endurance/retention qualification tradition.

A full pre-2000 EEPROM/Flash qualification genealogy, direct facsimile archaeology of original A117/A117B, the complete JESD219 workload history, later JESD218 revision history, and broader cross-vendor TLC/QLC qualification/fault evidence remain separate work best coordinated with `computing-archaeology`. The bounded HPE same-capacity TLC/QLC product cross-check is now grounded above; it is not a substitute for controlled media experiments or independent qualification evidence. Fresh repository searches for `JESD219A`, `SSD endurance workload`, `P5430`, `CM7`, and `TLC QLC SSD retention` found no dedicated `computing-archaeology` case to reuse; this repository therefore keeps only the bounded retention-specific standard/product relation while leaving broad standards and NAND-generation genealogy to that companion project.

---

## Functional analogies and philosophical limit

A useful functional analogy is to a **qualified service envelope** rather than to a countdown timer: the TBW number names a boundary inside which a bundle of conditions is still required to hold under a reference use model.

The analogy stops there. TBW is not a universal biological `lifespan`, and this repository does not convert JEDEC qualification language into a philosophical claim about finitude.

The narrow philosophical pressure is only this:

> A technical statement that something is `retained for one year` may describe not a timeless property of a substrate, but a relation conditioned by what happened to that substrate before the clock began.

That sentence is a project interpretation, not an attributed JEDEC intention.

---

## Cross-case result

Case 76 adds the following controlled comparison:

```text
host write acknowledged / flushed
    !=
write counted toward TBW
    !=
internal NAND write / P-E wear
    !=
current health / wear telemetry
    !=
rated-endurance qualification boundary
    !=
power-off retention interval after that boundary
    !=
actual instant of future unreadability
```

The HPE P5430 witness adds a second orthogonal warning: **NAND density label (for example QLC) ≠ the SSD-level endurance/retention contract**. Product-class media, host-workload assumptions, controller correction margin, rated writes, and the later unpowered interval remain separate relations even when a vendor documents them in one QuickSpecs family.

The CM7 cross-check sharpens that warning: **same nominal capacity and the same family-level post-endurance retention interval ≠ a controlled TLC/QLC comparison**. The documented endurance ratings differ, but workload class, product generation, controller design, ECC margin, and other implementation variables are not held constant. The comparison therefore constrains product-contract interpretation without ranking the intrinsic retention physics of TLC and QLC.

It complements:

- **Cases 11–13** — floating-gate/EEPROM/early-Flash substrate, program, erase, and cycling constraints below the SSD qualification layer;
- **Case 15 / Case 20** — immediate power-loss durability and interface persistence;
- **Case 36** — powered ECC-bounded Flash correct-and-refresh maintenance;
- **Case 37** — commercial old-data read-performance restoration/refresh;
- **Case 52** — read-disturb as a concrete access-induced NAND mechanism; A117B's terminology is prior-art evidence, not evidence that read disturb and time-aged retention are one mechanism;
- **Case 55** — current/lifetime endurance telemetry and model-derived health state;
- **Cases 44 / 47** — logical/sanitization/forensic forgetting rather than wear qualification.

The mechanisms should not be collapsed simply because all of them can be described as SSD `reliability`.

## Sources

[^jesd218]: JEDEC, **JESD218, _Solid-State Drive (SSD) Requirements and Endurance Test Method_**, September 2010. Public copy preserved as USPTO PTAB Exhibit 1009: <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1557329/download-documents?artifactId=2_lC_lThPTFMDbmibT3Hg39BJ0KyMU5imHIj-TvKQIl7pYfwt1_SX4I>. Key locations: pp. 1–5 definitions and references; p. 7 §§6.2–6.3 / Table 1; p. 8 §7.
[^intel-ret]: Intel, **_Data Retention in Intel Solid-State Drives_**, Application Note 325999-002US, June 2012. Preserved by Solidigm: <https://community.solidigm.com/hzhwu46669/attachments/hzhwu46669/Solid_State_Drives/3096/1/App_note_SSD_Data_retention.pdf>. Key locations: pp. 4–7 for powered refresh and wear/temperature mechanisms; pp. 12–18 for JESD218A qualification and Intel SSD wear/retention examples.
[^p3608]: Intel, **_Intel Solid-State Drive DC P3608 Series Product Specification_**, 333055-001US, September 2015, especially §2.6 / Table 14: <https://www.intel.com/content/dam/www/public/us/en/documents/product-specifications/ssd-dc-p3608-spec.pdf>.

[^hpe-qspec]: Hewlett Packard Enterprise, **_HPE Solid State Disk Drives_**, QuickSpecs Version 72, dated **5 January 2026**. Versioned PDF: <https://www.hpe.com/psnow/downloadDoc/HPE%20Solid%20State%20Disk%20Drives%20QuickSpecs-a00001288enw.pdf?contentDisposition=attachment&deepLink=&form=false&hf=regular&id=a00001288enw.pdf&isFutureVersion=true&isLinearized=false&originalObjectName=&prelaunchSection=&preview=false&print=&r=&section=&softrollSection=&ver=72>. Relevant locations: `Data Retention` under Standard Features; the E3.S SKU table identifying `P63934-B21` / P5430 as `QLC`; its `Lifetime Writes (TB)` / `Endurance DWPD` table; and the Summary of Changes identifying Version 72 as 05-Jan-2026.
[^hpe-p5430]: Hewlett Packard Enterprise, **HPE 7.68TB NVMe Gen4 Mainstream Performance Very Read Optimized E3S EC1 EDSFF P5430 SSD**, SKU `P63934-B21`, product page: <https://buy.hpe.com/us/en/options/drives-storage/server-solid-state-drives/hpe-7-68tb-nvme-gen4-mainstream-performance-very-read-optimized-e3s-ec1-edsff-p5430-ssd/p/p63934-b21>. The page identifies the family as `Next Gen QLC 3D NAND`; the QuickSpecs remains the stronger source for the retention and rated-write relation.
[^renesas2006]: Renesas Technology, **_Semiconductor Reliability Handbook_**, REJ27L0001-0100, Rev. 1.00, August 31, 2006, Section 7 JEDEC-standards table, pp. 335–336 of the handbook pagination; the table lists `JESD22-A117` and `2000` under `Established`: <https://studylib.net/doc/28351596/semiconductor-reliability>. This is manufacturer-retrospective standards inventory evidence, not a substitute for an original 2000 JEDEC facsimile.
[^a117e]: JEDEC, **JESD22-A117E, _Electrically Erasable Programmable ROM (EEPROM) Program / Erase Endurance and Data Retention Stress Test_**, November 2018, especially Annex A.2–A.3. Publicly indexed inspection copy: <https://www.scribd.com/document/837818477/22A117E>. Annex A.2 identifies A117B as March 2009; Annex A.3 records the A117A→A117B additions of read-disturb wording, UBER definition/calculation, bad-block-aware endurance-failure wording, and transient-error handling. This later JEDEC ledger is used as revision evidence, not invention-priority evidence.
[^belgal2002]: Hanmant P. Belgal et al., **“A New Reliability Model for Post-Cycling Charge Retention of Flash Memories,”** _2002 IEEE International Reliability Physics Symposium_, 7–11 April 2002, DOI 10.1109/RELPHY.2002.996604: <https://doi.org/10.1109/RELPHY.2002.996604>. The abstract directly describes stress-induced leakage after P/E cycling, multi-generation/multi-year-bake data, and cycle-count dependence.

[^jesd219-2010]: JEDEC, **JESD219, _Solid-State Drive (SSD) Endurance Workloads_**, September 2010. Public text-preserving inspection copy: <https://studylib.net/doc/18339575/jesd219>. Cover/scope identify the September 2010 issue; printed p. 1 states that the client workloads were still under development and were to be added when available, while §3 is the enterprise endurance workload. This mirror is used for document inspection and cross-checked against contemporaneous September 2010 publication notices; it is not used for invention priority.
[^cox2011]: Alvin Cox (Seagate; Chairman, JEDEC JC-64.8), **_JEDEC SSD Endurance Workloads_**, Flash Memory Summit, 10 August 2011: <https://old.flashmemorysummit.com/English/Collaterals/Proceedings/2011/20110810_T1B_Cox.pdf>. Slides 3–7 identify JESD218A and the class requirements; slides 12–13 describe the client workload as based on a real trace including TRIM and note that testing at 100% full was still under discussion. This is contemporaneous committee-chair presentation evidence, not a substitute for a normative standards facsimile.

[^jesd219a-catalog]: Accuris / JEDEC catalog, **JESD219A, _Solid-State Drive (SSD) Endurance Workloads_**, published 1 July 2012, 26 pages. The catalog description says the workloads are used with JESD218 and points to `JESD219A_MT` and `JESD219A_TT` as supporting trace files: <https://store.accuristech.com/asa/standards/jedec-jesd219a?product_id=1837609>. Accuris's JEDEC browse page also lists the September 2010 `JESD 219` and July 2012 `JESD219A` as separate catalog entries: <https://store.accuristech.com/products?page=23&per_page=10&publisher_id=110&sort_direction=asc&sort_order=doc_no>. This is publication/catalog evidence, not direct inspection of the full secured normative standard.
[^jesd219a-mt]: Accuris / JEDEC catalog, **JESD219A_MT, _Master Trace for 128 GB SSD_**, published 1 July 2012. The description identifies it as a supporting file for the endurance-verification client workload, says it represents seven months of actual SSD activity, and documents its direct/scaled capacity use: <https://store.accuristech.com/standards/jedec-jesd219a_mt?product_id=1838012>.
[^jesd219a-tt]: Accuris / JEDEC catalog, **JESD219A_TT, _Test Trace for 64 GB - 128 GB SSD_**, published 1 July 2012. The description says it is derived from the 128 GB Master Trace using the JESD219 compression method and preserves the Master Trace characteristics except for maximum LBA: <https://store.accuristech.com/standards/jedec-jesd219a_tt?product_id=1837608>.
