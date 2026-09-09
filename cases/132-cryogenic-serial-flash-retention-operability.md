# Cryogenic Serial Flash: Retention Without Full Cryogenic Operability

## Status

**`grounded`** — bounded to Frank R. Ihmig, Stephen G. Shirley, and Heiko Zimmermann's 2015 peer-reviewed batch experiment on commercial serial Flash ICs manufactured from 2007 to 2012. The case uses the authors' accepted manuscript for the experimental sections and Fraunhofer's institutional publication record for bibliographic identity.

Grounding record: [`../evidence/132-2015-cryogenic-serial-flash-grounding.md`](../evidence/132-2015-cryogenic-serial-flash-grounding.md).

Temperature-conditioned qualification deepening: [`../evidence/132-2014-2018-temperature-conditioned-retention-contract-deepening.md`](../evidence/132-2014-2018-temperature-conditioned-retention-contract-deepening.md). This later/deeper evidence is a bounded comparison, not an identification of the anonymous cryogenic-test ICs with Cypress products.

## Scope

- **Object / system:** six production batches of commercial serial Flash-memory ICs, 3,600 devices in total;
- **device-production interval:** 2007–2012;
- **publication:** *Cryogenics* (2015), DOI `10.1016/j.cryogenics.2015.05.005`;
- **test environment:** approximately room temperature down to liquid-nitrogen temperature, plus a separate long-duration cryogenic-storage group;
- **retention question:** can a temperature regime preserve an already-written bit pattern while the same regime makes some active Flash operations slow or unavailable?

This is **not** a general history of Flash memory, a universal low-temperature reliability law, a replacement for SSD retention qualification, or a claim that all colder storage monotonically improves every Flash property. Cases 04 and 11–13 cover other Flash mechanisms and history; Case 76 covers the JESD218 SSD-level endurance/retention contract. The broader history of cryogenic electronics belongs in `tmzncty/computing-archaeology` if later developed.

---

## Historical vocabulary

The 2015 article itself uses vocabulary including:

- `data retention`;
- `functional and performance characteristics`;
- `page programming`;
- `sector erase`;
- `pass rate`;
- `hard errors` and `soft errors`;
- `bit errors`;
- `cryogenic storage`.

The phrases **retention-valid environment**, **operation-valid environment**, **environmental operating envelope**, and **mode-switching maintenance** below are project engineering reconstructions. They are not presented as the authors' historical terminology.

---

## Historical record

### H/P — the experiment deliberately separated operation testing from long-duration retention testing

Ihmig, Shirley, and Zimmermann tested **3,600 ICs** drawn from six manufacturing batches. Their design separated two groups rather than treating `works at low temperature` as one indivisible property:

- **Group 1:** 500 ICs per batch for functional/performance testing across temperatures, including programming and erasing;
- **Group 2:** 100 ICs per batch for data-retention testing during continuous cryogenic storage.

That separation is already methodologically important. The experiment did not infer long-term stored-bit survival from a successful low-temperature command, nor infer command-set availability from data retention.

### H/P — active operation degraded strongly at the coldest temperatures

Across the Group-1 temperature sweep, no failures were observed down to **188 K (-85 °C)**. At lower temperatures the batches diverged. Some devices began to fail at 138 K or 108 K, while other batches first showed failures around 88 K. At liquid-nitrogen temperature, pass rates were substantially below 100% and strongly batch-dependent.

Programming and sector-erase times also increased substantially as temperature fell. The article's abstract reports page-programming times typically increasing by a factor of **4–6 at -196 °C**.

The safe historical claim is therefore not `Flash stops working when cold`. It is narrower:

> in these six commercial batches, low-temperature active-operation margins degraded sharply and non-uniformly, especially near liquid-nitrogen temperature.

### H/P — the observed low-temperature failures were generally reversible after warm-up

The authors report that they found **no irreversible functional damage** in the tested Group-1 devices: after warm-up, all ICs again operated properly at room temperature.

That is a direct counterexample to collapsing an unavailable operation into permanent technical forgetting:

```text
operation fails in the current environment
    !=
retained device state is permanently destroyed
```

The experiment does not prove that every conceivable cryogenic exposure is harmless, nor that every payload bit survives every failed operation.

### H/P — the retention group used a different temporal procedure

For Group 2, the devices were written with the test pattern `ALL55`, verified, removed from the active test setup, and stored cryogenically. At roughly six-month intervals the group was warmed, the stored pattern was checked at room temperature, and the devices were returned to cryogenic storage.

The authors report four checks over **24 months** and no observed bit errors in the stored pattern. The monitored storage-temperature range was approximately **-130 °C to -195 °C**.

This is a bounded experimental result. It is not a `24-month retention rating` for serial Flash as a technology and it does not prove an unbounded shelf life.

### H/P — manufacturing batch matters

The same nominal device family showed substantial batch-to-batch variation in low-temperature pass rates. The paper connects this to manufacturing tolerances and product evolution across batches manufactured between 2007 and 2012.

This blocks another shortcut:

```text
one memory type
    =>
one universal low-temperature operating boundary
```

A historical product family can preserve its ordinary interface identity while the physical margin underneath that interface changes across production revisions.

### H/P — elevated-temperature qualification is a separate retention relation

A 14-February-2014 Cypress PSoC 3 CY8C34 Automotive datasheet provides a useful pre-publication counterweight to the cryogenic experiment. Its Flash write/erase/program timing is specified over an active range extending to `TA <= 125 °C`, while retention is separately qualified by **average ambient temperature and prior cycling**: after 100 K erase/program cycles the table gives 20 years at `TA <= 55 °C` but 10 years at `TA <= 85 °C`. The same datasheet says the retention period is measured from the last erase cycle and offers a calculator based on an application's temperature profile.

Cypress KBA203737, dated 15 October 2015, independently tells users that low erase counts do not remove temperature dependence: extended higher-temperature storage requires a longevity calculation. Later S25FL1-K serial-Flash documentation preserves the same separation between P/E-conditioned retention and a broader active operating-temperature grade.

These are not evidence about the identity or process of the 2015 paper's anonymous samples. They establish a **vendor qualification boundary**:

> **operating-temperature support != a uniform retention guarantee over that entire operating range.**

Detailed evidence and provenance are kept in the temperature-conditioned addendum.

---

## Retained state and substrate

The object whose survival is actually checked in the retention experiment is a previously written digital bit pattern in nonvolatile serial Flash ICs.

The article is a device-level functional experiment, not a transistor-level charge-loss study. This case therefore does **not** infer an exact microscopic leakage law from the zero-error observation. The retention statement remains at the tested device/result level:

```text
written pattern
    -> cryogenic storage interval
    -> warm-up
    -> read/verify
    -> no observed bit errors in the tested interval
```

The absence of observed errors is evidence about recoverability under the procedure, not a direct measurement of every cell's analog threshold history.

---

## Addressing and access geometry

The devices remain ordinary serial Flash components from the host/tester's point of view, but access is environmentally qualified.

The central comparison is not about logical-address remapping as in Case 04. It is about whether the physical/electrical device can successfully execute its commands at a given temperature.

Thus:

```text
logical command exists
    !=
command is operationally executable at every temperature
```

The command vocabulary can remain stable while the physical operating envelope narrows.

---

## Read semantics

The 24-month retention claim was not established by continuous in-situ service at cryogenic temperature. The retention group was periodically **warmed and verified**.

Therefore:

> **successful warm verification after cold storage ≠ demonstrated continuous cryogenic read service.**

This distinction matters because retention and access were experimentally staged into different environmental modes.

---

## Write and erase semantics

The functional tests show that page programming and sector erase become substantially slower at very low temperatures and may fail in some devices/batches before room-temperature functionality is lost permanently.

So:

> **stored-state survival ≠ successful write/erase service in the same environment.**

The intended cryobiological application made this asymmetry practically useful: rewriting was rare enough that an operation could, when necessary, be deferred until the device was warmer. The repository treats that as a bounded operational strategy, not as a universal prescription for Flash preservation.

---

## Time

At least four different times must stay separate:

1. **storage interval** — the duration for which an already-written pattern remains recoverable under the tested cryogenic-storage procedure;
2. **verification interval** — roughly six months between warm checks in the retention group;
3. **command latency** — program/erase time, which increased substantially at lower temperature;
4. **environmental transition time** — the warm/cold mode change needed to perform the periodic verification procedure.

None of these intervals is interchangeable with a JEDEC SSD retention class, a NAND raw-cell retention constant, or a DRAM refresh interval.

---

## Maintenance and invisible work

The experiment exposes environmental management as part of a retention relation:

- cryogenic storage infrastructure;
- continuous temperature and liquid-level monitoring;
- periodic thaw/warm-up;
- bit-pattern verification;
- return to cryogenic storage;
- batch screening to identify devices that remain usable at the required low-temperature operating point.

The retained bit pattern can therefore appear `passively stored` only because a larger test/preservation regime controls temperature and periodically re-establishes an access environment.

This does **not** mean the Flash cells require refresh like DRAM. The maintenance is around the **environment and verification path**, not periodic rewriting required for ordinary Flash retention.

---

## Failure / forgetting modes

This bounded case separates:

- **cryogenic operation failure** — a command no longer completes correctly at the current temperature;
- **performance-margin loss** — program/erase latency grows before complete operation failure;
- **batch-dependent operating-envelope shift** — different production batches fail at different low temperatures;
- **retention failure** — a stored bit no longer verifies as the intended value after the storage interval;
- **irreversible device damage** — functionality does not return after warm-up;
- **verification-path failure** — the state may physically survive but cannot presently be checked through the planned warm-read procedure.

The 2015 experiments observed the first three categories but reported no retention bit errors in the 24-month Group-2 checks and no irreversible Group-1 functional damage after warm-up.

---

## Engineering reconstruction

### E — retention-valid environment ≠ full-operation-valid environment

The same cryogenic regime can be compatible with preserving an already-written state while being poor for active page program or sector erase.

This means `environmental suitability` must be typed by operation.

### E — stored-state survival ≠ command-set availability

A device can retain data while temporarily failing some active operations. Availability of the full command set is therefore a stronger requirement than survival of the retained payload.

### E — reversible environmental unavailability ≠ irreversible forgetting

Because the Group-1 devices recovered ordinary room-temperature operation after warm-up, low-temperature failure in this experiment is not evidence that the retained technical object was permanently lost.

### E — periodic verification ≠ continuous service

The Group-2 result proves recoverability at the scheduled warm verification points. It does not prove that the same devices continuously provided reliable reads, writes, or erases throughout the cryogenic interval.

### E — zero observed errors ≠ universal retention law

A bounded sample, pattern, duration, manufacturing range, and verification procedure cannot establish a technology-wide archival lifetime or zero failure probability.

### E — environment can preserve one relation while degrading another

`colder` is not one scalar measure of `better memory`. In this case the environment can support long storage of an already-written pattern while worsening active-operation timing and pass rate.

### E — active operating range != retention qualification range

The 2014 Cypress product evidence makes the converse boundary explicit: Flash operations may remain specified across a broad high-temperature range while the qualified retention interval is separately conditioned by average temperature and prior cycling. A product's operating-grade ceiling is therefore not a hidden promise that its headline retention number applies unchanged at that ceiling.

### E — temperature history can be retained as a condition even when no temperature log is stored in the memory

The Cypress retention-calculator note makes the guarantee depend on an application's temperature profile. The Flash payload does not need to store a temperature log for environmental history to matter physically and contractually. `retention depends on history` therefore does not imply `the device archives that history`.

### X — cold result != inverse high-temperature acceleration law

The cryogenic paper and Cypress qualification tables constrain the environmental problem from different sides, but they do not establish one measured activation energy or a quantitative conversion from `24 months with zero observed errors while cold` to a predicted room/high-temperature lifetime.

---

## Functional analogies and limits

### A — Case 127 DRAM cooling

Both Case 127 and Case 132 make temperature part of the retention relation. That is the useful comparison.

The mechanisms and service contracts are different:

```text
Case 127:
volatile DRAM after refresh/power withdrawal
    -> residual charge decay window extended by cooling

Case 132:
nonvolatile serial Flash already written
    -> cryogenic storage with periodic warm verification
    + degraded cryogenic program/erase operability
```

Therefore:

> **same environmental intervention ≠ same retention mechanism.**

### A — Case 76 JESD218 SSD retention qualification

Case 76 is an SSD-level standardized service/qualification relation that composes host TBW, workload, power-off retention, error limits, and temperature. Case 132 is a component-level cryogenic experiment outside ordinary commercial operating conditions.

Therefore:

> **component cryogenic experiment ≠ SSD retention contract.**

### A — Cases 12 and 13 EEPROM / early Flash

Those cases establish electrical erase/program asymmetry and erase geometry historically. Case 132 adds a later environmental constraint on whether a commercial device can execute active operations. It does not prove a direct genealogy from the early devices to the tested batches.

---

## Philosophical / media-theoretical interpretation

### I — persistence can depend on changing the conditions of access

A retained technical state need not be continuously callable under the same environmental conditions in which it is best preserved. The bounded experiment makes a useful distinction between:

- the condition under which a state is kept;
- the condition under which it is verified;
- the condition under which it can be rewritten efficiently.

That sharpens the repository's broader claim that `being retained` is relational rather than equivalent to permanent immediate availability.

This is a project interpretation. The 2015 authors do not present the experiment as a theory of memory, archive, or tertiary retention.

---

## Counterexamples and limits

- The 24-month no-error result is not an archival-lifetime guarantee.
- The paper does not directly measure floating-gate threshold-charge decay kinetics across the storage interval.
- The retention group was periodically warmed for verification; this is not a continuous in-situ cryogenic read-availability test.
- The six production batches do not represent every serial Flash process, vendor, capacity, or generation.
- Very-low-temperature program/erase degradation does not imply the same behavior at elevated storage temperatures. The Cypress addendum supplies only a separate vendor qualification/derating boundary, not a common microscopic model.
- Elevated-temperature product contracts do not identify the anonymous 2015 samples, prove raw-cell charge-loss kinetics, or provide a universal Flash activation energy.
- The experiment does not replace JESD218/JESD219 SSD qualification or named SSD/controller validation.
- A cryogenic storage result cannot be projected backward into EPROM/EEPROM/early-Flash history without separate evidence.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| 3,600 commercial serial Flash ICs from six 2007–2012 batches were tested | `H/P` | strong primary experimental paper |
| Group 1 and Group 2 separated functional/performance testing from long-duration retention testing | `H/P` | strong experimental-design evidence |
| no Group-1 failures were observed down to 188 K, with colder failures strongly batch-dependent | `H/P` | strong bounded result |
| page-programming time typically increased 4–6x at -196 °C | `H/P` | article abstract + experimental results |
| Group-1 low-temperature failures were generally reversible after warm-up | `H/P` | strong bounded result |
| Group 2 used `ALL55`, periodic warm verification, and cryogenic storage | `H/P` | primary experimental procedure |
| four checks across 24 months found no bit errors in the stored test pattern | `H/P` | strong bounded result |
| this proves a universal 24-month-or-longer retention guarantee for serial Flash | `X` | explicitly unsupported |
| successful warm verification proves continuous in-situ cryogenic read/write service | `X` | procedure does not establish this |
| cryogenic Flash and cooled DRAM share one physical retention mechanism | `X` | functional analogy only |
| retention-valid environment can differ from operation-valid environment | `E` | bounded reconstruction from split test results |
| at fixed 100 K P/E history, Cypress PSoC Flash qualified 20 years at average `TA <= 55 °C` but 10 years at `TA <= 85 °C` | `H/P` | 2014 manufacturer datasheet |
| active operating-temperature range implies the same retention lifetime at every supported temperature | `X` | manufacturer retention conditions reject this shortcut |
| cryogenic zero-error observation determines a quantitative high-temperature acceleration law | `X` | no common activation-energy/kinetics measurement |

---

## Related repositories

### `tmzncty/computing-archaeology`

Fresh searches for `cryogenic` and `serial flash` found no dedicated case to reuse. A broader history of low-temperature electronics, serial-Flash product evolution, device packaging, and cryogenic instrumentation belongs there if developed. This case retains only the retention-specific relation among environmental storage, operation availability, verification, and reversibility.

### `tmzncty/problem-history`

The historical problem in the 2015 paper is not `how can Flash become an archive?` in the abstract. It is a specific cryobiological instrumentation problem: whether commercial Flash components can accompany long-term low-temperature biological storage and what screening/operational limits that entails. Later philosophical vocabulary must not be projected backward as the actors' own problem statement.

---

## Sources

1. Frank R. Ihmig, Stephen G. Shirley, Heiko Zimmermann, **“Batch screening of commercial serial flash-memory integrated circuits for low-temperature applications,”** *Cryogenics* 71 (2015), DOI `10.1016/j.cryogenics.2015.05.005`. Fraunhofer institutional record: <https://publica.fraunhofer.de/entities/publication/bec6d545-e1b1-4a6c-a3cc-ca9d1043ad60>.
2. Author-uploaded accepted manuscript for the same article, PII `S0011-2275(15)00064-8`, Manuscript ID `CRYOGENICS-D-15-00007`, received 7 January 2015, revised 7 May 2015, accepted 14 May 2015. ResearchGate record: <https://www.researchgate.net/publication/277338221_Batch_screening_of_commercial_serial_flash-memory_integrated_circuits_for_low-temperature_applications>.
3. Cypress Semiconductor, *PSoC 3: CY8C34 Automotive Family Datasheet*, Document 001-57331 Rev. *G, revised 14 February 2014; first-party legacy copy preserved by Infineon: <https://www.infineon.com/dgdl/Infineon-PSoC_3_CY8C34_Automotive_Family_Datasheet_Programmable_System-on-Chip_%28PSoC%29_Datasheet-AdditionalTechnicalInformation-v08_00-EN.pdf?fileId=8ac78c8c7d0d8da4017d0ecabcb643c4>.
4. Cypress/Infineon, KBA203737, **“How long will data be retained in Cypress Flash memory devices if only a few erase cycles are planned?”**, 15 October 2015: <https://community.infineon.com/t5/Knowledge-Base-Articles/How-long-will-data-be-retained-in-Cypress-Flash-memory-devices-if-only-a-few/ta-p/249710>.
5. Cypress Semiconductor, *S25FL116K/S25FL132K/S25FL164K* SPI Flash datasheet, Document 002-00497, current legacy Rev. *I (4 July 2018), with revision history recording Data Retention section addition in 2016: <https://www.infineon.com/assets/row/public/documents/10/49/infineon-s25fl116k-s25fl132k-s25fl164k-16-mbit-2-mbyte-32-mbit-4-mbyte-64-mbit-8-mbyte-3.0-v-spi-flash-memory-datasheet-en.pdf?fileId=8ac78c8c7d0d8da4017d0ed4ebee537f>.

The accepted manuscript, not a publisher-typeset facsimile, is the directly text-inspected cryogenic experimental source. The Cypress documents are separate product/vendor qualification witnesses used to bound elevated-temperature claims; they are not evidence that the anonymous cryogenic-test parts were Cypress devices.
