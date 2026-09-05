# JEDEC JESD218 SSD Endurance Qualification: Workload-Qualified TBW and Power-Off Retention

## Status

**`grounded`** — bounded to the September 2010 JESD218 SSD-level endurance/retention qualification relation, with Intel's June 2012 retention application note used to expose the difference between standardized TBW and actual media wear, and Intel's September 2015 DC P3608 specification used as a named commercial product witness. Prior-art deepening now also separates the earlier JESD22-A117 device-level program/erase-endurance-and-retention test family from JESD218's later SSD-level host-TBW service contract, using a 2006 Renesas standards inventory, JEDEC's own later revision ledger, and a 2002 IEEE post-cycling retention paper.

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

A full pre-2000 EEPROM/Flash qualification genealogy, direct facsimile archaeology of original A117/A117B, the complete JESD219 workload history, and later JESD218 revision history remain separate work best coordinated with `computing-archaeology`.

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
[^renesas2006]: Renesas Technology, **_Semiconductor Reliability Handbook_**, REJ27L0001-0100, Rev. 1.00, August 31, 2006, Section 7 JEDEC-standards table, pp. 335–336 of the handbook pagination; the table lists `JESD22-A117` and `2000` under `Established`: <https://studylib.net/doc/28351596/semiconductor-reliability>. This is manufacturer-retrospective standards inventory evidence, not a substitute for an original 2000 JEDEC facsimile.
[^a117e]: JEDEC, **JESD22-A117E, _Electrically Erasable Programmable ROM (EEPROM) Program / Erase Endurance and Data Retention Stress Test_**, November 2018, especially Annex A.2–A.3. Publicly indexed inspection copy: <https://www.scribd.com/document/837818477/22A117E>. Annex A.2 identifies A117B as March 2009; Annex A.3 records the A117A→A117B additions of read-disturb wording, UBER definition/calculation, bad-block-aware endurance-failure wording, and transient-error handling. This later JEDEC ledger is used as revision evidence, not invention-priority evidence.
[^belgal2002]: Hanmant P. Belgal et al., **“A New Reliability Model for Post-Cycling Charge Retention of Flash Memories,”** _2002 IEEE International Reliability Physics Symposium_, 7–11 April 2002, DOI 10.1109/RELPHY.2002.996604: <https://doi.org/10.1109/RELPHY.2002.996604>. The abstract directly describes stress-induced leakage after P/E cycling, multi-generation/multi-year-bake data, and cycle-count dependence.