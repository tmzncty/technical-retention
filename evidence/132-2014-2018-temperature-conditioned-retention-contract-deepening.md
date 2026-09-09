# Case 132 deepening — Cypress/Infineon temperature-conditioned Flash retention contracts, 2014–2018

This evidence addendum deepens [`../cases/132-cryogenic-serial-flash-retention-operability.md`](../cases/132-cryogenic-serial-flash-retention-operability.md).

**Bounded question:** the 2015 cryogenic experiment shows that an already-written serial-Flash pattern can remain recoverable through a cold-store -> warm-verify procedure while very-low-temperature program/erase operation becomes slow or unavailable. What public manufacturer evidence, available around the same period, shows about the *other* side of the environmental relation: elevated temperature and prior cycling as conditions on retention lifetime?

This addendum does **not** identify the anonymous commercial ICs in the 2015 experiment with any Cypress product. It also does not derive a raw-cell Arrhenius law from product specifications. Its contribution is narrower: it grounds a temperature-conditioned **retention contract / qualification** boundary that prevents `operating temperature`, `storage temperature`, and `retention lifetime` from being collapsed into one number.

---

## Source A — Cypress PSoC 3 CY8C34 Automotive Family Datasheet, Rev. *G, 14 February 2014

**Document:** Cypress Semiconductor, *PSoC 3: CY8C34 Automotive Family Datasheet*, Document 001-57331 Rev. *G, revised 14 February 2014.

**Preserved first-party hosting:** <https://www.infineon.com/dgdl/Infineon-PSoC_3_CY8C34_Automotive_Family_Datasheet_Programmable_System-on-Chip_%28PSoC%29_Datasheet-AdditionalTechnicalInformation-v08_00-EN.pdf?fileId=8ac78c8c7d0d8da4017d0ecabcb643c4>

**Evidence class:** `H/P` — manufacturer datasheet, preserved on Infineon's current site after the Cypress acquisition.

### A1. Active-operation envelope and retention qualification are stated separately

Section 11.7 says the memory specifications are generally valid over `-40 °C <= TA <= 125 °C` unless otherwise noted. The Flash timing table separately gives block write, erase, and program timing over temperature ranges extending to `TA <= 125 °C` / `TJ <= 140 °C`.

The same table then gives **retention-specific exceptions** rather than one lifetime valid everywhere:

- after **100 K erase/program cycles**, minimum Flash retention is **20 years** at average ambient `TA <= 55 °C`;
- after the same **100 K erase/program cycles**, the listed minimum is **10 years** at average ambient `TA <= 85 °C`;
- note 53 says Cypress provides a retention calculator based on an application's individual temperature profile across the broader `-40 °C` to `+125 °C` ambient range.

This is unusually useful for the repository because cycle count can be held fixed while the published retention interval changes with average temperature.

**Grounded boundary:** `active-operation temperature range != one temperature-independent retention lifetime`.

### A2. Retention is dated from a state-changing event, not from manufacture

The table defines the Flash retention period as measured from the **last erase cycle**. That is a service-history relation, not device age from fabrication and not powered uptime.

**Grounded boundary:** `retention clock origin != device manufacturing date != controller power-on time`.

### A3. A temperature profile is stronger than a single maximum-temperature label

The datasheet's retention-calculator note refers to customers' individual temperature profiles. The historical product contract therefore already treats environmental exposure as a time-varying history rather than reducing retention to a single product-grade label.

**Engineering reconstruction:** a retention guarantee can depend on an accumulated environmental/use history even when the logical payload and address remain unchanged.

---

## Source B — Cypress KBA203737, 15 October 2015

**Document:** Cypress/Infineon Knowledge Base, “How long will data be retained in Cypress Flash memory devices if only a few erase cycles are planned?”, KBA203737, dated 15 October 2015.

**Current institutional record:** <https://community.infineon.com/t5/Knowledge-Base-Articles/How-long-will-data-be-retained-in-Cypress-Flash-memory-devices-if-only-a-few/ta-p/249710>

**Evidence class:** `H/P*` — manufacturer institutional guidance contemporaneous with Case 132's publication year, but not a product-specific datasheet or standards text. It cites Cypress application note AN98549.

The KBA says that with very few erase cycles, typical retention can be expected around the long end of the product guidance, but it immediately qualifies that answer by storage temperature: below about `55 °C` may not create the same issue, whereas higher temperatures over extended periods require calculation to ensure the desired longevity.

The safe use here is not the wording `20 years for all Cypress Flash`. It is the relationship the vendor explicitly foregrounds:

> low cycling burden does not make retention independent of temperature history.

**Grounded boundary:** `few P/E cycles != temperature-independent shelf life`.

---

## Source C — S25FL1-K serial Flash datasheet continuity

**Document:** Cypress Semiconductor, *S25FL116K/S25FL132K/S25FL164K, 3.0 V SPI Flash Memory*, Document 002-00497. The current Infineon-hosted legacy PDF is Rev. *I, revised 4 July 2018; its revision history records that the Data Retention section was added in Rev. *E on 29 June 2016.

**First-party preserved PDF:** <https://www.infineon.com/assets/row/public/documents/10/49/infineon-s25fl116k-s25fl132k-s25fl164k-16-mbit-2-mbyte-32-mbit-4-mbyte-64-mbit-8-mbyte-3.0-v-spi-flash-memory-datasheet-en.pdf?fileId=8ac78c8c7d0d8da4017d0ed4ebee537f>

**Evidence class:** `H/P` for the named product specification and revision history; later than the 2015 cryogenic paper and therefore used only as same-vendor serial-Flash continuity, not as evidence about the anonymous tested batches.

The Data Integrity table lists:

- `10K Program/Erase Cycles -> 20 Years` minimum retention;
- `100K Program/Erase Cycles -> 2 Years` minimum retention.

The same product family separately exposes Industrial / Industrial Plus operating grades up to `+85 °C` / `+105 °C`. The retention table itself does **not** print a temperature qualifier next to those two rows. Therefore this document alone must **not** be paraphrased as `20 years at +105 °C`.

A later Infineon NOR-Flash FAQ makes the vendor's interpretation explicit: the 10K/100K retention examples assume about **55 °C average field temperature**, and retention after cycling depends on field temperature, P/E count, and cycling interval.

**Later institutional continuity:** <https://community.infineon.com/t5/Knowledge-Base-Articles/NOR-Flash-FAQs/ta-p/255345>

**Grounded boundary:** `product operating-grade ceiling != implied retention-test temperature`.

---

## Evidence decomposition

The sources require at least four separate environmental/use variables:

```text
current operating temperature
    -> can the device execute read/program/erase within its active specification?

average / time-profiled retention temperature
    -> how long is the post-write/post-erase state qualified to remain recoverable?

prior P/E cycling
    -> how much endurance history precedes the retention interval?

cycling interval / annealing history
    -> what temporal pattern produced that wear state?
```

Only the first variable is an instantaneous command-environment question. The others can encode a history that matters after active writes stop.

---

## Engineering reconstruction

### E1. Operating-temperature admissibility != retention-duration qualification

A device can be specified to operate at a temperature at which the guaranteed retention interval, after a given cycling history, is shorter than at a lower average temperature. `The command is supported here` is therefore weaker than `the written state is guaranteed for N years here`.

### E2. Retention lifetime is history-conditioned

For the bounded Cypress evidence, retention cannot be reconstructed from `nonvolatile` alone. At minimum it is conditioned by temperature history and P/E history, and vendor guidance also calls out cycling interval.

### E3. Case 132's cryogenic result is not an acceleration model

The 2015 cryogenic paper reports zero observed bit errors at four warm verification points over 24 months for one finite experiment. The Cypress high-temperature qualification evidence independently shows temperature-conditioned retention contracts, but the two do not supply a measured common activation energy or a quantitative cold-vs-hot lifetime ratio.

Therefore:

`cryogenic no-error observation != measured Arrhenius acceleration coefficient`.

### E4. `Colder` is not one monotonic system-level quality axis

Case 132 already shows very low temperature worsening program/erase service. The elevated-temperature product evidence shows that hotter average exposure can shorten qualified retention. These can coexist because **operation margin** and **retention lifetime** are different relations.

This does not justify a universal optimum temperature or a claim that every Flash mechanism has the same temperature dependence.

---

## Historical / mechanism boundaries

- PSoC 3 embedded Flash is **not** the same product/process as the anonymous serial-Flash batches in Ihmig et al. 2015.
- Cypress's 2015 KBA is manufacturer guidance, not a JEDEC normative standard or direct raw-cell experiment.
- The later S25FL1-K / Infineon FAQ continuity does not retroactively prove that the anonymous 2015 samples used the same retention model.
- Product qualification numbers do not expose a complete trap/charge-loss distribution or a universal activation energy.
- The sequence `2014 datasheet -> 2015 cryogenic paper -> 2016/2018 serial-Flash datasheet` is a source chronology, **not a proven engineering genealogy** among products or authors.

---

## Cross-case controls

### Case 76 — JESD218 SSD qualification

Case 76 already shows that SSD endurance and power-off retention are application-class/workload/temperature-qualified service contracts. This addendum remains below that level: it shows a manufacturer Flash/embedded-memory contract in which environmental history and cycling condition the retained state.

Safe comparison: `retention lifetime is qualified by use/environment history`.

Rejected identity: `PSoC/serial-NOR product table == JESD218 SSD contract`.

### Cases 03 / 127 — DRAM

DRAM cooling and Flash temperature-conditioned retention can be compared only as environment-sensitive recoverability. DRAM's volatile charge restoration/remanence regime is not Flash's nonvolatile post-cycling retention regime.

### Cases 36 / 52 / 59 / 67 — Flash maintenance/disturbance

Those cases show retention debt from age, reads, programming interference, and controller policy. This addendum adds **environmental/use-history qualification**, not a new refresh/reclaim mechanism.

---

## Readiness assessment

This slice closes the bounded roadmap item **“elevated-temperature comparison” at the vendor qualification/contract layer**:

- direct 2014 manufacturer datasheet with fixed-cycle-count, temperature-conditioned retention numbers;
- a contemporaneous 2015 manufacturer KBA explicitly warning that higher-temperature exposure requires longevity calculation;
- later named serial-Flash product continuity with explicit P/E-conditioned retention and a separate operating-temperature range;
- explicit anti-overclaim boundaries against product identity, raw-cell kinetics, and genealogy.

It does **not** close direct Flash/EEPROM charge-loss kinetics, activation-energy measurement, accelerated bake methodology, independent replication, or controlled fault injection. Those remain open.
