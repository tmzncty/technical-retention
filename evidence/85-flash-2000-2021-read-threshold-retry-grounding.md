# Case 85 Grounding — Flash Read-Threshold Adjustment and Retry, 2000–2021

**Case:** [`../cases/85-toshiba-nand-shift-read-retry-recoverability.md`](../cases/85-toshiba-nand-shift-read-retry-recoverability.md)

**Promotion target:** `grounded`

**Bounded question:** What direct evidence supports the claim that a NAND/MLC Flash page can fail ECC under one read/reference-voltage choice yet become recoverable when the same stored cells are reread with changed decision thresholds, without thereby proving that the stored representation has already been refreshed or rewritten?

---

## 1. Claim-type discipline

This record follows [`../docs/METHOD.md`](../docs/METHOD.md).

- **H/P — Historical / primary:** patent text, dates, terminology, described controller behavior.
- **S/E — Scholarly / empirical:** later independent experimental characterization.
- **E — Engineering reconstruction:** consequences of the mechanism that are not asserted as historical vocabulary.
- **F — Functional analogy:** cross-case comparison only; not genealogy.
- **P — Philosophical interpretation:** bounded conceptual reading after mechanism is established.

Project terms such as `read-decision state`, `interpretation margin`, `recoverability frontier`, and `reader-side requalification` are **E/P terms**, not source vocabulary.

---

## 2. Sources inspected

### Source A — Toshiba/Nagashima 2009-priority memory-system family

Hiroyuki Nagashima, **“Memory system,”** US20120268994A1 / US8929140B2.

- Japanese priority: **2009-11-06**.
- PCT filing: 2010-11-04.
- US publication: 2012-10-25.
- Google Patents record: <https://patents.google.com/patent/US20120268994A1/en>.
- Later continuation specifically titled **“Memory system changing a memory cell read voltage upon detecting a memory cell read error,”** US9524786B2: <https://patents.google.com/patent/US9524786B2/en>.

Why it matters: this family directly provides the bounded historical vocabulary and a controller flow connecting threshold-distribution movement, positive/negative read-level shifts, ECC evaluation, `retry read`, and a distinct later refresh/copy action.

### Source B — earlier MLC Flash adaptive-reference prior-art witness

Frank Yu, Charles C. Lee, Abraham C. Ma, Ming-Shiang Shen et al., **“Cell-Downgrading and Reference-Voltage Adjustment for a Multi-Bit-Cell Flash Memory,”** US20070201274A1 / US7333364B2.

- Claimed prior-art / priority chain begins **2000-01-06**.
- US application publication: 2007-08-30.
- Google Patents: <https://patents.google.com/patent/US20070201274A1/en>.

Why it matters: it establishes that ECC-triggered adjustment of Flash reference voltages and rereading predates the 2009-priority Toshiba family. It is used only to block a false invention-priority claim, not to prove direct genealogy.

### Source C — independent empirical modern witness

Jisung Park, Myungsuk Kim, Myoungjun Chun, Lois Orosa, Jihong Kim, Onur Mutlu, **“Reducing Solid-State Drive Read Latency by Optimizing Read-Retry,”** ASPLOS 2021, DOI **10.1145/3445814.3446719**.

- arXiv manuscript submitted 2021-03-25: <https://arxiv.org/abs/2104.09611>.
- Study reports characterization of **160 real 3D TLC NAND flash chips**.

Why it matters: it independently confirms the operational relation in modern NAND: read-retry rereads a target page with adjusted read-reference voltages, with success defined by moving the raw-error count inside ECC capability. It is not used to project 2021 3D-TLC details backward into Toshiba's 2009 design.

---

## 3. Source A — exact bounded claims

### A1. Threshold distributions and read levels are different variables

**H/P.** The Toshiba publication describes threshold-voltage distributions moving under different effects:

- program disturb (`PD`) and read disturb (`RD`) can shift distributions toward higher voltage in the illustrated embodiment;
- data retention degradation (`DR`) can shift distributions toward lower voltage.

The source then changes the **read levels** in response. This directly establishes that the stored cell distribution and the voltage boundary used to classify it are not the same state variable.

**Allowed claim:** a controller can compensate for a changed cell distribution by changing read levels.

**Not allowed:** all NAND drift always has one sign, or one shift direction is universally correct.

### A2. `default read`, `+ shift read`, and `- shift read`

**H/P.** The first embodiment explicitly distinguishes:

- `default read`;
- `+ shift read`, moving read levels higher;
- `- shift read`, moving read levels lower.

The source says the shift direction can be selected with regard to PD, RD, and DR, and discusses use-state information such as elapsed/standing time and operation counts.

**Allowed claim:** read classification boundaries are adjustable control state in this bounded design.

**Not allowed:** the controller is physically restoring cell charge merely by changing the read level.

### A3. Temperature and management-state inputs

**H/P.** The publication states that temperature data recorded in the management table can also be used when changing read levels. It also describes management tables / work-area state in the SSD controller.

**Allowed claim:** the bounded design may retain condition metadata used to choose a read interpretation.

**Not allowed:** every commercial SSD keeps the same fields, same granularity, or same table format.

### A4. First-read ECC failure followed by `shift read (retry read)`

**H/P.** In the second embodiment the source states, in substance:

- if the first read has a large error-bit count and ECC correction is impossible (`ECC error`),
- `shift read (retry read)` is performed,
- ECC correction is executed again.

This is the most important direct grounding for Case 85.

**Allowed claim:** an ECC-uncorrectable default read does not end the bounded recovery path; the same target can be reread under a changed read-level condition and re-evaluated by ECC.

**Not allowed:** a default-read ECC failure proves that the physical data was absent and then recreated by retry.

### A5. Refresh is a later, separate operation

**H/P.** The first embodiment separately states that if the error-bit count remains larger than a predetermined value after read/ECC determination, a `refresh operation` can be executed for the block; the source describes this refresh as copying the block's data to a new erased block. It also says the refresh step need not always be executed.

This yields a very strong boundary:

- shift/retry read changes the reading condition;
- refresh/copy changes the stored physical embodiment.

**Allowed claim:** `successful shifted read ≠ completed physical refresh`.

**Allowed claim:** current recoverability and future-margin renewal are distinct obligations.

**Not allowed:** call every adjusted reread a refresh.

### A6. Later family continuations retain the same relation

**H/P.** Later continuations in the Nagashima family preserve the same 2009 priority and continue to describe changed read voltages, condition/history information, ECC outcomes, and remembered read conditions. These later grants are useful for exact wording and implementation variants, but the historical priority claim remains anchored to the 2009 Japanese filing.

**Boundary:** continuations do not create new evidence that the design was commercially deployed exactly as written.

---

## 4. Source B — prior-art boundary

### B1. Dating

**H/P.** US20070201274A1 identifies a continuation/priority chain beginning with a filing dated **2000-01-06**. The publication is later (2007), so this record carefully says `2000-priority patent family`, not `published in 2000`.

### B2. ECC-triggered reference-voltage adjustment

**H/P.** The source describes read errors detected using ECC. It states that reference voltages compared to the Flash bit-line voltage can be adjusted to try to recover data. The adjustment can continue while ECC indicates excessive errors.

The read-error flow includes the possibility of rereading with changed references, using ECC to decide whether the error count has returned within the correction limit, and relocating data after recovery.

**Allowed claim:** adaptive reference-voltage recovery in MLC Flash is demonstrably older than Toshiba's 2009-priority family.

**Not allowed:** this is the first adaptive-voltage memory reader in history.

### B3. No genealogy claim

No source inspected here establishes that Toshiba/Nagashima derived its design from Yu et al. Therefore the relation is recorded as:

> **chronological prior-art witness, not demonstrated genealogy**.

This follows the repository's anti-anachronism/prior-art rule.

---

## 5. Source C — independent empirical witness

### C1. What read-retry is in the measured modern devices

**S/E.** Park et al. state that modern SSDs employ strong ECC and, when ECC cannot correct all initial raw bit errors, perform read-retry by reading the erroneous page again with slightly adjusted `VREF` values.

They explain the physical relation:

- NAND stores data in cell threshold-voltage `VTH` levels;
- a read-reference voltage `VREF` distinguishes the states;
- errors arise when `VTH` distributions move relative to those boundaries;
- appropriately shifted `VREF` can reduce raw bit errors.

### C2. Retry success is defined relative to ECC capability

**S/E.** The paper describes retry steps continuing until either:

- the page RBER falls below ECC correction capability, or
- the system determines the page cannot be read without uncorrectable errors under the available retry path.

This independently supports the engineering reconstruction:

> `recoverability = function(physical distribution, sensing boundary, ECC capability, retry policy)`.

### C3. 160-chip empirical basis

**S/E.** Park et al. report detailed characterization of **160 real 3D TLC NAND flash chips**. They observe frequent multi-step retry under realistic retention/cycling conditions and show that near-optimal reference voltages in the final retry step can sharply reduce RBER, leaving a positive ECC-capability margin.

**Allowed claim:** adjusted read thresholds are operationally significant in real modern 3D TLC NAND, not only in patent diagrams.

**Not allowed:** the exact retry-table values, retention behavior, or timing results apply to Toshiba's 2009 NAND embodiment.

### C4. Retention age and P/E cycling affect retry behavior

**S/E.** The paper reports that read-retry behavior varies with operating condition, including retention age and P/E cycles. This supports the claim that a once-good read boundary can become a poor one as the physical distribution evolves.

It does **not** prove that a controller must persist one specific historical variable or table. That remains implementation-specific.

---

## 6. Claim ledger

| Claim | Type | Source | Strength | Boundary |
| --- | --- | --- | --- | --- |
| NAND cell threshold distributions can move relative to default read levels under PD/RD/DR | H/P | A | strong | bounded Toshiba embodiment/sign conventions |
| read levels can be shifted higher or lower | H/P | A | strong | not universal shift direction |
| management state can inform the chosen read condition | H/P | A | strong | not universal table format/granularity |
| ECC-uncorrectable first read can trigger `shift read (retry read)` and another ECC attempt | H/P | A | strong | patent mechanism, not deployment proof |
| shift read is distinct from later refresh/copy to a new erased block | H/P | A | strong | refresh semantics bounded to family |
| reference-voltage rereading predates Toshiba 2009 priority | H/P | B | strong for chronology | no first-invention or genealogy claim |
| modern read-retry repeatedly adjusts VREF until RBER enters ECC capability or fails | S/E | C | strong | modern 3D TLC, not all NAND generations |
| the 2021 study used 160 real 3D TLC chips | S/E | C | strong | sampled devices/conditions only |
| physical cell state and read-decision boundary are separate state classes | E | A+B+C | strong reconstruction | project terminology |
| default-read failure does not imply no recoverable information remains | E | A+B+C | strong | only relative to available retry/ECC paths |
| successful retry does not itself rewrite/refresh the medium | E | A | strong | later proprietary implementations may couple extra work, so do not universalize command internals |
| current ECC success does not imply restored future retention margin | E | A+C | strong | margin is bounded by actual device/ECC conditions |
| retained read-condition metadata can preserve future interpretability | E | A | moderate-strong | bounded design; metadata can become stale |
| `recoverability frontier` is historical vocabulary | — | none | **rejected** | project reconstruction only |

---

## 7. Rejected shortcuts

### R1. `ECC failure = data gone`

Rejected. Source A explicitly retries with changed read levels and another ECC attempt; Source C independently describes the same general relation in modern NAND.

### R2. `read retry repairs the cells`

Rejected. Source A separates changed read conditions from a later refresh/copy operation.

### R3. `successful retry = zero raw errors`

Rejected. Source C frames success against ECC correction capability and explicitly discusses remaining ECC-capability margin.

### R4. `correctable now = safe indefinitely`

Rejected. Source A can trigger refresh when error count is high; Source C shows retry behavior changing with retention/cycling condition.

### R5. `Toshiba invented read retry`

Rejected. Source B supplies an earlier 2000-priority MLC Flash family with ECC-triggered reference-voltage adjustment/rereading.

### R6. `the 2000 family directly led to Toshiba`

Rejected. Chronology is established; genealogy is not.

### R7. `all NAND stores a successful VREF per page`

Rejected. Retaining successful conditions is supported for bounded designs/continuations, but exact granularity and persistence are vendor/implementation specific.

### R8. `retention is only a material property of the cell`

Rejected as an engineering description of operational availability. Sources A–C jointly show that recoverability also depends on the sensing boundary and ECC path. This does not make the physical substrate irrelevant.

---

## 8. Cross-case evidence boundaries

### Case 36 — Correct-and-Refresh

Case 36's Cai et al. regime uses error correction plus data refresh/rewrite as proactive retention maintenance. Case 85 closes the complementary boundary: a changed read threshold can restore current logical recoverability **before** a rewrite occurs.

Evidence-level distinction:

> `reader-side recovery ≠ representation renewal`.

### Cases 52 and 59 — read disturb and program interference

Those cases explain physical causes of threshold drift. Case 85 treats those causes only as inputs to a changed sensing decision. It does not re-prove their device physics.

### Case 65 — early retention loss / age-aware reading

Case 65 provides a later 3D-NAND age-aware reading regime. Case 85 adds the earlier bounded patent/prior-art chain and isolates the retry/ECC decision boundary.

### Case 67 — adaptive reclaim

Reclaim moves or renews data after accumulated risk. Retry read can succeed while leaving the physical location unchanged.

### Case 82 — COPYBACK

Case 82 shows relocation without automatic ECC requalification; Case 85 shows read requalification without relocation. Their comparison is functional and engineering-structural, not historical genealogy.

---

## 9. Related-repository check

Before creating the case, the current `tmzncty/computing-archaeology` repository was searched for `NAND read retry reference voltage` and no dedicated matching case was found.

Therefore this slice records only the retention-specific comparison here. If a complete history of reference sensing, vendor retry commands, adaptive `VREF`, soft-decision LDPC, or calibration circuits is later written, it should primarily live in `computing-archaeology` and be linked rather than duplicated.

---

## 10. Promotion decision

**Decision: `grounded`.**

Reason:

1. a period-primary Toshiba patent family directly supplies the key vocabulary and separates shifted rereading from later refresh/copy;
2. an earlier primary patent family blocks a false 2009-first invention claim;
3. a peer-reviewed 2021 study on 160 real 3D TLC chips independently confirms the modern operational relation among adjusted read-reference voltage, RBER, ECC capability, and retry count;
4. the case keeps historical description, engineering reconstruction, functional analogy, and philosophy explicitly separated;
5. no unsupported commercial-deployment or universal-all-NAND claim is needed for the bounded finding.

Remaining work is deliberately outside this case:

- exact first-use genealogy of `read retry` vocabulary;
- vendor-command standardization and proprietary retry-table history;
- detailed soft-decision/LDPC evolution;
- named commercial SSD firmware behavior under raw retry telemetry;
- cross-vendor fault injection and retention-aging validation;
- complete reference-cell / sense-amplifier history.

Those are valid future slices, not prerequisites for the bounded claim established here.