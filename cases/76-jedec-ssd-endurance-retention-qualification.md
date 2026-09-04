# JEDEC JESD218 SSD Endurance Qualification: Workload-Qualified TBW and Power-Off Retention

## Status

**`grounded`** — bounded to the September 2010 JESD218 SSD-level endurance/retention qualification relation, with Intel's June 2012 retention application note used to expose the difference between standardized TBW and actual media wear, and Intel's September 2015 DC P3608 specification used as a named commercial product witness.

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

JESD218 itself cites **JESD22-A117, _Electrically Erasable Programmable ROM (EEPROM) Program/Erase Endurance and Data Retention Stress Test_** as a reference document.[^jesd218]

Therefore this repository does **not** claim that JESD218 invented the practice of cycling nonvolatile memory and then testing retention. The bounded historical contribution used here is more specific:

> by September 2010, JESD218 standardized an **SSD-level**, application-class-specific endurance rating expressed as host TBW and tied it to workload, capacity, UBER/FFR, and a subsequent power-off retention requirement.

A full history of JESD22-A117, JESD219, NAND qualification, or the later A/B revisions of JESD218 remains separate work.

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

- **Case 15 / Case 20** — immediate power-loss durability and interface persistence;
- **Case 36** — powered ECC-bounded Flash correct-and-refresh maintenance;
- **Case 37** — commercial old-data read-performance restoration/refresh;
- **Case 55** — current/lifetime endurance telemetry and model-derived health state;
- **Cases 44 / 47** — logical/sanitization/forensic forgetting rather than wear qualification.

The mechanisms should not be collapsed simply because all of them can be described as SSD `reliability`.

## Sources

[^jesd218]: JEDEC, **JESD218, _Solid-State Drive (SSD) Requirements and Endurance Test Method_**, September 2010. Public copy preserved as USPTO PTAB Exhibit 1009: <https://ptacts.uspto.gov/ptacts/public-informations/petitions/1557329/download-documents?artifactId=2_lC_lThPTFMDbmibT3Hg39BJ0KyMU5imHIj-TvKQIl7pYfwt1_SX4I>. Key locations: pp. 1–5 definitions and references; p. 7 §§6.2–6.3 / Table 1; p. 8 §7.
[^intel-ret]: Intel, **_Data Retention in Intel Solid-State Drives_**, Application Note 325999-002US, June 2012. Preserved by Solidigm: <https://community.solidigm.com/hzhwu46669/attachments/hzhwu46669/Solid_State_Drives/3096/1/App_note_SSD_Data_retention.pdf>. Key locations: pp. 4–7 for powered refresh and wear/temperature mechanisms; pp. 12–18 for JESD218A qualification and Intel SSD wear/retention examples.
[^p3608]: Intel, **_Intel Solid-State Drive DC P3608 Series Product Specification_**, 333055-001US, September 2015, especially §2.6 / Table 14: <https://www.intel.com/content/dam/www/public/us/en/documents/product-specifications/ssd-dc-p3608-spec.pdf>.
