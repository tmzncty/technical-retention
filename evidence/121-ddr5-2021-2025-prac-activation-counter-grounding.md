# Evidence 121 — DDR5 PRAC Activation-Counter Initialization and Volatile Maintenance Metadata

## Scope

This record grounds only the retention-specific relation used by Case 121:

> DDR5 PRAC can depend on per-row activation-count state that must first be initialized, is not trusted before initialization completes, and itself requires refresh; therefore maintenance metadata can have a separate retention/readiness contract from the payload it helps protect.

It does **not** claim a complete JESD79-5C genealogy, universal vendor implementation, or complete RowHammer security proof.

## Source 1 — JEDEC, JESD79-5C publication announcement, 17 April 2024

**Type:** standards-organization primary publication announcement (`H/P`)

**Access used:** JEDEC press release redistributed verbatim through Business Wire / FinancialContent.

- Title: `JEDEC Updates JESD79-5C DDR5 SDRAM Standard: Elevating Performance and Security for Next-Gen Technologies`
- Date: 17 April 2024
- URL: https://markets.financialcontent.com/bpas/article/bizwire-2024-4-17-jedec-updates-jesd79-5c-ddr5-sdram-standard-elevating-performance-and-security-for-next-gen-technologies
- Original JEDEC destination identified by the release: https://www.jedec.org/news/pressreleases/jedec-updates-jesd79-5c-ddr5-sdram-standard-elevating-performance-and-security

### Claims supported

The announcement states that JESD79-5C was published and introduces `Per-Row Activation Counting (PRAC)` for DRAM data integrity. It describes PRAC as precisely counting DRAM activations at wordline granularity and says that excessive activation causes the PRAC-enabled DRAM to alert the system so traffic can be paused and time designated for mitigation.

**Safe historical claim:**

> PRAC is publicly named as part of JESD79-5C by 17 April 2024, with wordline-granular counting and explicit DRAM/system coordination.

### Claims not supported

This source does not establish:

- invention priority for per-row activation counters;
- exact MR encodings;
- physical implementation of counter storage;
- that every DDR5 part implements PRAC;
- that PRAC alone guarantees RowHammer immunity.

## Source 2 — Micron, `DDR5 SDRAM Core Data Sheet`, Rev. E, November 2024

**Type:** manufacturer-primary product/core documentation (`H/P`)

**Document identity:**

- document identifier visible in the public copy: `CCM005-1684161373-23`;
- file: `ddr5_sdram_core.pdf`;
- revision: `Rev. E 11/2024 EN`;
- manufacturer: Micron Technology, Inc.;
- public distributor mirror used for this round: https://www.avnet.com/wcm/connect/dacdfea7-999f-4ee0-b514-6f9e0bf68c6d/ddr5-sdram-core.pdf?MOD=AJPERES

The mirror is not treated as the standards authority. The underlying document is manufacturer-authored and identifies Micron copyright/document metadata.

### Locator A — MR70 `PRAC, ABO`, Table 91, document p. 90

The indexed manufacturer text exposes these mode-register relations:

- `OP[0]`: PRAC/ABO support, optional;
- `OP[1]`: PRAC/ABO enable/disable, default disabled;
- `OP[2]`: Activation Counter Initialization mode;
- `OP[3]`: Activation Counter Initialization complete status;
- `OP[5]`: Alert Back-Off source flag.

### Locator B — `Per Row Activation Counting` / `Activation Counter Initialization`

The PRAC section says, in substance:

- before PRAC counting begins, the host enables PRAC;
- after enable, a full-array ACI shall be performed;
- the device does not track activation counts and does not issue ABO until the activation-counter bits are initialized;
- ACI uses a full-array refresh sequence under a restricted command regime;
- completion is exposed through the ACI-complete status and the host exits ACI afterward;
- the device begins counting activations after this transition.

### Locator C — activation-counter retention requirement

The same section states that activation-counter bits require refresh like normal device cells. If refresh is violated during or after ACI, the host performs ACI to put activation-counter bits back into a known state.

It also states that array data can be corrupted when refresh requirements are violated, making previous activation-counter values irrelevant to the now-corrupted prior array state.

### Locator D — ACI and pre-existing payload

The manufacturer text states that during ACI the device does not need to refresh the main array and previously written data may be corrupted. It further notes ACI requirements around MBIST/mPPR before data is rewritten.

### Locator E — counter-update work

Micron's PRAC timing section states that PRAC requires additional counter cells per row to store ACT counts and that updating those cells requires a read-modify-write operation, `activation counter update (ACU)`, changing some core timing parameters.

### Claims supported

- `PRAC supported` and `PRAC enabled` are distinct states.
- PRAC is disabled by default in this bounded product/core contract.
- `PRAC enabled` is not yet equivalent to `counter state initialized`.
- the device does not count or issue ABO before ACI is complete.
- activation-count state itself is volatile/refresh-dependent in this bounded Micron design.
- counter validity can require explicit re-initialization after refresh violation.
- ACI is not a transparent guarantee of preserving already-written payload.
- counter update has physical/timing cost.

### Claims not supported

- universal physical counter-cell layout across all DDR5 vendors;
- exact behavior of every shipping Micron die revision;
- full reset/power-cycle semantics outside the documented sequence;
- universal PRAC security.

## Source 3 — Intel, US20210365316A1, filed 4 June 2021, published 25 November 2021

**Type:** patent / primary technical disclosure (`H/P` prior-art floor)

- Title: `Memory chip with per row activation count having error correction code protection`
- Assignee: Intel Corporation
- Filing / priority date shown by Google Patents: 4 June 2021
- Publication: US20210365316A1, 25 November 2021
- URL: https://patents.google.com/patent/US20210365316A1/en

### Claims supported

The disclosure describes storage cells associated with a row holding that row's activation count, ECC protecting the count value, comparison against a threshold, incrementing the count, and writing updated count/ECC state back.

**Prior-art conclusion:**

> Per-row activation-count storage and threshold-oriented use are publicly disclosed before JESD79-5C's 2024 PRAC publication.

Therefore Case 121 rejects:

> `JESD79-5C PRAC invented the idea of per-row activation counting`.

### Claims not supported

This patent does not by itself establish:

- identity with the final JEDEC PRAC/ABO contract;
- direct Intel→JEDEC genealogy;
- the exact Micron ACI mechanism;
- universal implementation of ECC-protected PRAC counters.

## Source 4 — Micron, US20250316301A1, published 9 October 2025

**Type:** manufacturer patent / primary technical disclosure (`H/P` corroborative later evidence)

- Title: `Apparatuses and methods for activation counter initialization`
- Assignee: Micron Technology, Inc.
- application filing shown by public patent indexes: 21 March 2025
- publication: US20250316301A1, 9 October 2025
- public text: https://patents.justia.com/patent/20250316301

### Claims supported

The disclosure independently describes an ACI mode that initializes activation-count values to known state. In its DDR5 example it identifies MR70 PRAC enable, ACI enable, and ACI status roles; states that PRAC is optional/default disabled; states that after power-up or refresh violation activation-counter bits may be unknown; and says the device does not track counts or issue ABO until initialization completes.

It also describes the bounded ACI sequence and the possibility that previously written array data may be corrupted during ACI.

This later patent is useful as a public manufacturer disclosure of the **initialization/readiness problem**. It is not used to project a March/October 2025 disclosure backward as evidence of what every 2024 implementation did.

## Source 5 — Kim et al., `Per-Row Activation Counting on Real Hardware: Demystifying Performance Overheads`, IEEE Computer Architecture Letters 24(2), 2025

**Type:** independent scholarly / experimental evidence (`S/E`)

- DOI: https://doi.org/10.1109/LCA.2025.3587293
- publication date: 10 July 2025
- pages: 217–220

### Claims supported

The paper describes PRAC as maintaining an activation counter with each row and updating that counter through a read-modify-write path. It reports real-machine timing/performance measurements and confirms that PRAC's altered timing parameters have measurable workload cost on the tested platforms.

This supports the bounded counterexample:

> hidden maintenance metadata can affect ordinary service timing.

It does not establish Micron-specific internal circuitry or universal overhead magnitude.

## Source 6 — Qureshi and Qazi, `MOAT: Securely Mitigating Rowhammer with Per-Row Activation Counters`, 2024

**Type:** independent scholarly security analysis (`S/E`)

- arXiv: https://arxiv.org/abs/2407.09995

The paper treats PRAC+ABO as a framework whose actual security depends on the mitigation implementation. It is used only to prevent an overclaim that presence of the standardized counting/back-off interface itself proves complete RowHammer immunity.

## Claim ledger

| Claim | Type | Strength | Source basis |
| --- | --- | --- | --- |
| JESD79-5C publicly introduces named PRAC on 17 Apr 2024 | `H/P` | high | JEDEC announcement |
| PRAC counts at wordline granularity and coordinates DRAM/system mitigation | `H/P` | high at announcement level | JEDEC announcement |
| Micron Rev. E exposes distinct support, enable, ACI, completion, and ABO state | `H/P` | high for bounded product/core document | Micron Table 91 / PRAC section |
| PRAC enabled does not yet mean counting/ABO active | `H/P`, `E` | high for bounded Micron contract | Micron ACI section |
| activation-counter bits themselves require refresh | `H/P` | high for bounded Micron contract | Micron PRAC section |
| refresh violation can make counter state unknown and require ACI | `H/P`, `E` | high for bounded Micron contract; independently corroborated later | Micron core doc + 2025 Micron patent |
| ACI does not guarantee preservation of previously written array data | `H/P`, `E` | high for bounded Micron contract | Micron core doc + later patent |
| counter state is maintenance metadata rather than application payload | `E` | strong reconstruction | state roles above |
| activation count is not a complete access-history archive | `E/X` | strong negative inference | count semantics + absence of ordering/history fields |
| per-row activation counting predates 2024 PRAC | `H/P` | strong prior-art floor | Intel 2021 patent |
| Intel 2021 patent directly became JEDEC PRAC | `X` | unsupported | no genealogy established |
| PRAC guarantees complete RowHammer immunity | `X` | unsupported | JEDEC scope + independent security literature |
| hidden counter maintenance has zero cost | `X` | contradicted for tested/bounded systems | Micron ACU timing + IEEE 2025 |

## Engineering reconstruction

The source-backed state machine can be represented as:

```text
PRAC supported?
    |
    +-- no -> PRAC/ABO path unavailable
    |
    +-- yes
          |
          -> host enables PRAC
                 |
                 -> counters not yet trustworthy for protection
                 -> ACI full-array initialization
                        |
                        -> completion status
                               |
                               -> host exits ACI
                                      |
                                      -> activation counting + ABO may operate
```

A second relation runs underneath it:

```text
activation-counter cells
    -> themselves require refresh
    -> refresh violation can invalidate count state
    -> ACI re-establishes known count state
```

This is the central Case-121 contribution. The system's preservation logic depends on a retained **description of prior stress**, and that description itself has material retention requirements.

## Counterexamples and anti-anachronism

1. **`DDR5` ≠ `PRAC enabled`.** Micron exposes optional support and a separate default-disabled enable bit.
2. **`PRAC enabled` ≠ `PRAC ready`.** Counter initialization must complete before counting/ABO.
3. **`counter state` ≠ `payload`.** Both may be volatile but have different operational meanings.
4. **`ACI` ≠ `payload-preserving scrub`.** Existing data may be corrupted in the bounded initialization regime.
5. **`per-row count` ≠ `complete access history`.** It is a compressed protection state.
6. **`2024 PRAC` ≠ `invention of per-row counting`.** Intel's 2021 filing is an earlier public floor.
7. **`earlier per-row counter patent` ≠ `proven PRAC genealogy`.** Mechanism similarity is not descent evidence.
8. **`standardized framework` ≠ `universal security guarantee`.** Implementation and system composition remain material.

## Related-repository check

Searches of `tmzncty/computing-archaeology` for `PRAC` and `activation counter` returned no dedicated case during this round.

Division of labor remains:

- `technical-retention`: second-order retained state, initialization/readiness, counter validity, payload/counter lifetime distinction, cross-case comparison;
- `computing-archaeology`: broader RowHammer/DRAM standards genealogy, committee history, vendor/device chronology, controller evolution if developed later.

## Remaining evidence debt

- obtain/record an official JEDEC-hosted JESD79-5C facsimile if needed for clause-level quotation rather than announcement-level chronology;
- exact JEDEC ballot/technical-proposal history for PRAC/ABO;
- exact physical counter implementation in named shipping dies;
- cross-vendor ACI semantics;
- reset/power-cycle and low-power-mode counter-state lifetime across revisions;
- named-platform traces that show PRAC enable → ACI → ABO/RFM handoff;
- controlled violation of counter refresh followed by recovery;
- PRAC/ARFM/DRFM interaction and later JESD79-5 revisions;
- broader per-row-count genealogy in `computing-archaeology`.
