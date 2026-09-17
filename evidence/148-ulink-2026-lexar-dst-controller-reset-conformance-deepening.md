# Evidence 148 — 2026 ULINK / Lexar Device Self-test controller-reset conformance witness

Status: **`bounded deepening complete`**

Canonical case: [`../cases/148-nvme13-device-self-test-reset-surviving-maintenance.md`](../cases/148-nvme13-device-self-test-reset-surviving-maintenance.md)

## Research question

Case 148 already establishes a normative retention contract in NVM Express 1.3:

- a **short** Device Self-test is aborted by a Controller Level Reset;
- an **extended** Device Self-test persists across Controller Level Reset and resumes after reset / restoration of power;
- the exact segment at which the extended test resumes is vendor specific.

The existing commercial witness, Intel D7-P5510, only proved that a named NVMe 1.3c product family publicly advertised Device Self-test. It did **not** provide a named-device reset experiment.

This slice asks a narrower evidence-class question:

> Can a public third-party protocol-test record show that a named SSD / firmware revision was actually exercised through Device Self-test reset scenarios, without pretending that a summary `PASS` result reveals the firmware's internal checkpoint mechanism or proves every power-loss branch?

The answer is **yes, but only at a bounded conformance-summary level**.

A March 2026 ULINK NVMe Protocol test record for a **LEXAR NM7A1 SSD**, firmware **M7100**, identifies Device Self-test tests and reports:

```text
Short DST with RESET
    Controller Reset      PASS
    Power Cycle Reset     PASS

Extended DST with RESET
    Controller Reset      PASS
    Power Cycle Reset     N/A
```

That closes one part of the product-evidence gap while preserving a crucial negative boundary:

```text
named controller-reset test PASS
    != raw before/after state trace
    != disclosed resume checkpoint
    != extended power-restoration test
```

---

## Claim types used here

This record follows [`../docs/METHOD.md`](../docs/METHOD.md):

- **Historical / technical record** — what NVM Express, ULINK's public test list, and the dated ULINK report actually state.
- **Experiment / test evidence** — the ULINK report is a third-party test artifact for one named device and firmware revision.
- **Engineering reconstruction** — what can safely be inferred about the evidence boundary between a standard contract and observed conformance.
- **Functional analogy** — comparisons with other cases are explicitly bounded and establish no genealogy.
- **Philosophical interpretation** — limited to what the evidence says about retaining unfinished technical obligations across interruption.

---

## Source ledger

### S1 — NVM Express Revision 1.3 (`historical primary / normative baseline`)

- Organization: NVM Express, Inc.
- Revision: 1.3.
- Ratified: **26-Apr-2017**.
- Document date: **1-May-2017**.
- URL: <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>
- Existing Case-148 use:
  - §8.11.1 — short Device Self-test is aborted by Controller Level Reset;
  - §8.11.2 — extended Device Self-test persists across Controller Level Reset and resumes after reset or restoration of power;
  - resume segment is vendor specific.

This slice does not re-ground the whole specification. It uses the already-inspected normative distinction as the contract against which later test evidence is classified.

### S2 — ULINK Test List (`third-party institutional test registry`)

- Organization: ULINK Technology.
- Page: **ULINK Test Suites List / UTL – ULINK Test List**.
- URL: <https://ulinktech.com/ulink-test-suites-list/>
- Relevant public entry:
  - Make: **Lexar**;
  - Type: **NVMe SSD**;
  - Model / tested identifier: **LEXAR NM7A1 SSD 0C6BEJXU4TBG94UZYY6P**;
  - firmware: **M7100**;
  - suite: **NVMe Protocol v7.0**;
  - date listed: **2026/3/6**.

ULINK describes the UTL as a database of components that passed specified ULINK Test Suites and links the corresponding report.

### S3 — ULINK NVMe-PTC test result (`third-party experiment / test artifact`)

- Report title: **NVMe-PTC Test Result**.
- Script: **REV 7.0**.
- Test software: **ULINK DriveMaster Enterprise (NVME+DRV) Version 10.1.1900**.
- Model: **LEXAR NM7A1 SSD**.
- Serial: **0C6BEJXU4TBG94UZYY6P**.
- Firmware: **M7100**.
- Start date printed in report: **Wed March 04 2026**.
- Capacity printed in report: **1024.209 G**.
- URL: <https://ulinktech.com/wp-content/uploads/2026/03/NVMe_Ptc_LexarNM7A1SSD_0C6BEJXU4TBG94UZYY6P_02.pdf>
- Relevant report area: Device Self-Test block around report pp. 45–46 / extracted PDF page index 45.

The report is public third-party conformance evidence. It is **not** manufacturer design documentation and does not disclose the test script's raw command trace in the summary PDF.

### S4 — ULINK NVMe test-suite / DriveMaster capability pages (`test-infrastructure context`)

- ULINK NVMe Suites: <https://ulinktech.com/products/ulink-nvme-test-suites/>
- DriveMaster 10 NVMe: <https://ulinktech.com/products/drivemaster-10-nvme/>

Relevant bounded facts:

- ULINK lists **Device Self Test** among NVMe Protocol Test Suite areas.
- ULINK lists protocol validation, regression/data-integrity testing, and power-related testing among DriveMaster capabilities.
- ULINK states that its PCIe-SSD Power Adaptor Plus hardware is required for power-cycle testing.

These pages establish that ULINK's platform has explicit NVMe protocol and power-cycle test capabilities. They do **not** explain why a particular individual row in S3 is `N/A`.

---

## Historical / technical record A — a named device and firmware were tested, not merely advertised

The UTL entry and report identify the same concrete target:

```text
LEXAR NM7A1 SSD
serial 0C6BEJXU4TBG94UZYY6P
firmware M7100
```

The report started on **4 March 2026**; the public UTL lists the NVMe Protocol v7.0 result on **6 March 2026**.

This is a stronger product witness than a feature bullet in a product brief because the public record associates:

```text
named device instance
    + named firmware revision
    + named protocol test suite
    + dated test run
```

It therefore closes a narrow part of the original Case-148 debt:

> a public named-device third-party conformance artifact exists for Device Self-test reset scenarios.

It does **not** turn a 2026 device into evidence for what a 2017 NVMe 1.3 controller implementation did internally.

---

## Historical / technical record B — the report exercises ordinary Device Self-test command forms

The Device Self-Test block first reports `PASS` for command cases using several NSID forms and for:

- `STC = 1h (Short)`;
- `STC = 2h (Extended)`;
- `STC = fh (Abort)`.

This confirms that the tested device/suite did not reach the reset rows only through an abstract capability declaration. The report includes actual Device Self-test command-path test items before the reset-specific group.

Safe claim:

> **named device passed the ULINK report's ordinary short / extended / abort Device Self-test test items.**

Unsafe claim:

> **the report proves every namespace, segment, error, and internal diagnostic path was exhaustively tested.**

The summary report does not justify that stronger statement.

---

## Experiment record C — reset testing distinguishes short and extended rows

The decisive report fragment is:

```text
Short DST with RESET            PASS
  Controller Reset              PASS
  Power Cycle Reset             PASS

Extended DST with RESET         PASS
  Controller Reset              PASS
  Power Cycle Reset             N/A
```

At minimum, this establishes three concrete facts about the public test artifact:

1. the suite treats **short DST with reset** and **extended DST with reset** as separate test groups;
2. the tested NM7A1 / M7100 instance received a `PASS` result for the **controller-reset** row in both groups;
3. the **extended power-cycle** row was explicitly **not executed / not applicable in this report** (`N/A`).

This is exactly the sort of boundary the case needed, because it prevents an easy but false escalation from a successful controller-reset test to a successful power-restoration test.

```text
Extended DST + Controller Reset PASS
    !=
Extended DST + Power Cycle Reset PASS
```

The second relation is not present in S3; the report says `N/A`.

---

## Engineering reconstruction — contract evidence and conformance evidence are different layers

The repository should distinguish at least four evidence layers for reset-surviving maintenance:

```text
1. normative contract
      NVMe 1.3 says what short and extended DST shall do

2. product feature witness
      a vendor says a named product supports Device Self-test

3. named-product conformance observation
      a third-party test artifact records PASS/N/A for bounded reset scenarios

4. implementation / raw-state evidence
      command trace, before/after log values, persisted checkpoint format,
      firmware implementation, or fault-injection trace exposing how resume works
```

Case 148 already had layers 1 and 2.

S2/S3 now add a bounded instance of layer 3.

They still do **not** provide layer 4.

Therefore:

```text
standard requires continuation
    != product advertises feature
    != third-party scenario passes
    != internal persistence mechanism disclosed
```

Each step strengthens a different claim.

---

## Engineering reconstruction — `PASS` is not a disclosed checkpoint

The ULINK summary PDF does not expose:

- Current Device Self-test Operation immediately before reset;
- Current Percentage Complete immediately before reset;
- Current Percentage Complete immediately after reset;
- the segment resumed after reset;
- whether the implementation replayed all or part of the last segment;
- the physical/nonvolatile object in which resume state was stored;
- a firmware trace showing restore/reconstitution logic;
- the exact assertions inside the proprietary protocol-test script.

So the strongest safe statement is:

> The named drive/firmware passed ULINK's published **controller-reset Device Self-test test rows**.

It is **not**:

> The report proves the exact resume state or proves that the controller resumed at the next physical LBA.

This preserves the original NVMe 1.3 stop condition:

```text
operation-level continuation contract
    != exact microstate preservation
```

---

## Engineering reconstruction — the `N/A` row is positive negative evidence

An `N/A` result is not “missing formatting” here. It is part of the same structured test-result block that reports `PASS` for adjacent reset rows.

For the evidence ledger, this means:

```text
controller-reset conformance observation available
    +
extended power-cycle observation unavailable in this report
```

That is useful because Case 148's most ambitious open product question was whether a named drive actually demonstrates the extended-test **power restoration** branch.

S3 does not close it.

The report instead narrows the debt:

- named controller-reset scenario: **public third-party summary now exists**;
- named extended power-cycle resume: **still open**;
- exact resume segment / checkpoint embodiment: **still open**.

---

## Engineering reconstruction — test-platform capability does not explain one `N/A`

ULINK's DriveMaster / NVMe suite pages show that the platform supports power-cycle testing and that dedicated power-control hardware is used for such tests.

But that does not license a reason for the NM7A1 report's extended-DST power-cycle `N/A`.

Possible explanations might include suite gating, device-advertised capability, test duration, lab configuration, or another rule — but none is established by the inspected public sources.

Therefore:

> **platform can perform power-cycle tests != this particular extended-DST power-cycle row was runnable or was run**.

The repository should preserve `N/A` as `N/A`, not silently convert it into `PASS`, `FAIL`, or an inferred lab limitation.

---

## Relationship to the 2017 normative distinction

The 2026 report is later than the original NVMe 1.3 case by almost nine years.

It therefore does not prove the original drafting history of TP001a and does not show how first-generation NVMe 1.3 devices implemented resume state.

Its value is different:

> a distinction introduced into the NVMe interface contract — separate short/extended reset behavior — remained concrete enough to appear as separate testable protocol scenarios on a later named SSD.

That is a later conformance witness, not a genealogy claim.

Safe chronology:

```text
2017 NVMe 1.3 normative contract
    -> later revisions retain/evolve Device Self-test behavior
    -> 2026 ULINK protocol test artifact exposes reset scenarios on a named SSD
```

Unsafe chronology:

```text
2026 ULINK report
    -> therefore the same Lexar firmware mechanism existed in 2017
```

No such inference is made.

---

## Result-history boundary remains open

The test report confirms that the Device Self-test log itself is among tested Get Log paths and that Device Self-test scenarios are executed.

However, the public summary does not show the before/after **20-entry result population** around the reset tests.

It therefore does not establish:

- that every existing historical result survived controller reset;
- that every existing historical result survived power cycle;
- whether a short-test reset generated the expected abort result entry in the exact observed trace;
- whether any later format/sanitize/firmware transition changed those entries;
- how result-history persistence compares with active extended-test resume persistence.

Thus the original distinction remains necessary:

```text
active extended-test continuity
    != bounded result-history persistence
```

---

## Maintenance-state decomposition after this deepening

For Case 148, at least eight separable state / evidence relations should now remain visible:

1. **feature capability** — whether Device Self-test is supported;
2. **current operation identity** — none / short / extended / vendor-specific;
3. **progress reporting** — Current Percentage Complete;
4. **resume/reconstitution state** — enough hidden state for extended operation continuity;
5. **authority / exclusion scope** — controller-local or subsystem-wide according to `DSTO`;
6. **bounded result history** — newest 20 completed/aborted operations;
7. **normative persistence contract** — what the standard requires across specific events;
8. **observed conformance evidence** — which bounded scenarios a named implementation has actually been recorded as passing.

The eighth item is not device state. It is an **evidence class about the device state machine**.

That distinction matters for repository method:

```text
retained state
    != evidence that retained state behaved as specified
```

---

## Functional comparison — Case 15 Intel SSD 320 (`A`)

Case 15 already separates:

- a manufacturer-described power-loss-protection architecture;
- an interface durability contract;
- and independent fault experiments that can test implementation robustness.

Case 148 now has a similar evidence-class separation:

```text
NVMe normative reset contract
    + named-product feature advertisement
    + named-product third-party reset-test summary
```

But the mechanisms are not the same.

Case 15 concerns write durability and emergency retention of user/system state during power loss. Case 148 concerns continuity or retirement of an unfinished diagnostic operation.

Shared methodological lesson only:

> **feature / contract evidence != measured behavior evidence**.

No genealogy is claimed.

---

## Functional comparison — Case 18 OpenZFS scrub (`A`)

Case 18 exposes implementation-level checkpoint machinery for long-running maintenance.

The ULINK report does not elevate Case 148 to that evidence level. It shows a scenario result but still leaves the NVMe device's checkpoint/reconstitution embodiment opaque.

Therefore:

```text
named conformance PASS
    != implementation checkpoint disclosure
```

This keeps the existing Case-18 / Case-148 distinction intact.

---

## Functional comparison — Synthesis 29 semantic persistence (`A/E`)

Synthesis 29 distinguishes:

- obligation/task identity persistence;
- progress/checkpoint persistence;
- semantic interpretation persistence;
- restart authority.

The ULINK controller-reset result strengthens only one layer of empirical support:

> a named later implementation passed a test scenario corresponding to the reset boundary.

It does not reveal whether exact progress checkpointing, replay, or another reconstruction method produced that result.

So:

```text
behavioral continuity observed at interface
    != internal representation continuity observed
```

---

## Philosophical / media-theoretical interpretation

The bounded interpretive point is methodological rather than metaphysical.

A technical obligation can be specified as surviving interruption, but that statement belongs to a different evidentiary order from observing one implementation cross the interruption successfully. Conversely, successful observed behavior does not tell us what internal object was preserved unchanged; continuity may be produced by replay, reconstruction, redundancy, or another hidden mechanism.

The case therefore resists a simplistic equation:

> persistence = one thing remaining physically untouched.

But it does **not** justify claims about human memory, institutional persistence, or universal technical identity. The inspected evidence concerns an NVMe diagnostic state machine and a third-party protocol-test result.

---

## Explicit non-claims

This evidence does **not** claim that:

1. ULINK is the designer or manufacturer of the Lexar NM7A1 firmware.
2. the 2026 report is primary evidence for NVMe TP001a drafting in 2017.
3. the NM7A1 is an NVMe 1.3 device merely because Case 148 began from NVMe 1.3.
4. the report discloses the controller's internal resume-state format.
5. `PASS` proves an exact LBA-level or instruction-level checkpoint.
6. `PASS` proves zero replay after reset.
7. the extended test's Current Percentage Complete was bitwise identical before and after reset.
8. the public summary PDF contains the proprietary script's complete oracle or raw command trace.
9. the short and extended controller-reset rows prove identical internal reset handling.
10. the short power-cycle `PASS` means short Device Self-test continued across power loss rather than being correctly terminated according to the test oracle.
11. the extended power-cycle branch passed; the report explicitly says `N/A`.
12. `N/A` means the drive failed the extended power-cycle test.
13. `N/A` means ULINK's platform lacks power-cycle capability in general.
14. the report proves last-20 Device Self-test result history survives a power cycle.
15. the report proves a reset-generated abort result was durably retained across all later operations.
16. the report proves every Device Self-test segment or every LBA was tested by the short operation.
17. a passing Device Self-test proves archival retention, secure erasure, or host-write power-loss protection.
18. a later 2026 product test can be projected backward as evidence of 2017 implementation practice.
19. ULINK's public test result establishes a direct genealogy from ATA/SCSI self-test to NVMe.
20. Case 148 maturity should be raised merely because a later third-party product test was found.

---

## Claim ledger

| Claim | Type | Strength | Evidence |
| --- | --- | --- | --- |
| NVMe 1.3 gives short and extended Device Self-test different Controller Level Reset horizons | historical / normative | strong | NVM Express Revision 1.3, already grounded in Evidence 148 |
| ULINK publicly lists the Lexar NM7A1 / M7100 as passing NVMe Protocol v7.0 | third-party institutional record | strong | ULINK UTL entry dated 2026/3/6 |
| ULINK report identifies the tested instance, firmware M7100, and start date 2026-03-04 | experiment record | strong | NVMe-PTC report header |
| Ordinary short, extended, and abort Device Self-test test items are marked PASS | experiment record | strong within report scope | NVMe-PTC Device Self-Test block |
| Short DST + Controller Reset is marked PASS | experiment record | strong within report scope | NVMe-PTC report |
| Short DST + Power Cycle Reset is marked PASS | experiment record | strong within report scope | NVMe-PTC report |
| Extended DST + Controller Reset is marked PASS | experiment record | strong within report scope | NVMe-PTC report |
| Extended DST + Power Cycle Reset is marked N/A | experiment record | strong | NVMe-PTC report |
| The report reveals exact extended-DST resume checkpoint state | rejected | unsupported | summary report contains no such trace |
| Extended power-restoration continuation was empirically demonstrated by this report | rejected | contradicted by `N/A` row | NVMe-PTC report |
| Last-20 result history persistence across power cycle is demonstrated | rejected | unsupported | no before/after result-population trace |
| A later named conformance witness proves 2017 implementation genealogy | rejected | anachronistic | source dates / evidence class |

---

## Related-repository boundary

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Device Self-test` found no dedicated packet to reuse.

A broad history of:

- NVMe conformance programs and test houses;
- DriveMaster / protocol-test tooling;
- ATA/SCSI diagnostic test genealogy;
- vendor firmware implementation details;
- NVMe TP001a / later revision drafting;

belongs primarily in `computing-archaeology` if developed as technical history.

`technical-retention` keeps the narrower seam:

> **normative maintenance-continuation contract -> named implementation conformance evidence -> still-undisclosed internal resume embodiment**.

---

## Remaining evidence debt

This slice closes only the **named controller-reset conformance-summary** gap.

Still open:

- a named product test where **extended Device Self-test is actually interrupted by a full power cycle and demonstrably resumes**;
- raw pre-reset / post-reset Device Self-test Log captures showing current operation and progress;
- evidence identifying the resumed segment or replay granularity on a named device;
- firmware/source/design documentation disclosing how resume state is persisted or reconstructed;
- product-specific persistence behavior of the newest-20 result history across controller reset, power cycle, format, sanitize, and firmware update;
- exact public TP001a drafting / approval chronology;
- a raw multi-controller experiment for `DSTO` subsystem-wide visibility.

The most important stop condition is now narrower than before:

```text
controller-reset behavior has a named third-party conformance witness
    but
extended power-restoration behavior + checkpoint embodiment remain ungrounded at product level
```

---

## Sources

1. NVM Express, **NVM Express Revision 1.3**, ratified 26-Apr-2017, document dated 1-May-2017: <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>.
2. ULINK Technology, **UTL — ULINK Test Suites List**, Lexar NM7A1 / M7100 / NVMe Protocol v7.0 entry, listed 6-Mar-2026: <https://ulinktech.com/ulink-test-suites-list/>.
3. ULINK Technology, **NVMe-PTC Test Result**, LEXAR NM7A1 SSD, serial `0C6BEJXU4TBG94UZYY6P`, firmware `M7100`, test start 4-Mar-2026: <https://ulinktech.com/wp-content/uploads/2026/03/NVMe_Ptc_LexarNM7A1SSD_0C6BEJXU4TBG94UZYY6P_02.pdf>.
4. ULINK Technology, **ULINK NVMe Suites**: <https://ulinktech.com/products/ulink-nvme-test-suites/>.
5. ULINK Technology, **DriveMaster 10 NVMe**: <https://ulinktech.com/products/drivemaster-10-nvme/>.
