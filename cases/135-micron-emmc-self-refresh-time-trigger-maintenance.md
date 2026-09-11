# Micron Automotive eMMC 5.1 Self-Refresh: Host Time, Selective Renewal, and Maintenance Evidence

## Status

**`grounded`** for the bounded Armadillo-IoT Gateway G4 / Micron automotive eMMC 5.1 integration described below.

Grounding record: [`../evidence/135-micron-emmc-2021-2023-self-refresh-grounding.md`](../evidence/135-micron-emmc-2021-2023-self-refresh-grounding.md).

Deepening record: [`../evidence/135-jedec-emmc51-bkops-maintenance-opportunity-deepening.md`](../evidence/135-jedec-emmc51-bkops-maintenance-opportunity-deepening.md).

## Scope

This case asks a narrow managed-Flash retention question:

> What changes when an embedded eMMC retention feature uses host-supplied time, a reset-bounded command window, bus-idle detection, an ECC-error threshold, and retained maintenance statistics to decide when and where renewal work is due?

The bounded product witness is Atmark Techno's **Armadillo-IoT Gateway G4**, whose version 1.0.0 product manual is dated **9 December 2021** and documents an automatic eMMC `data retention` / `self refresh` path. Micron's official software-and-technical-note catalog independently lists **TN-FC-60, _Refresh Features for Micron e.MMC Automotive 5.1 Devices_**, dated **11 April 2023**, and describes it as covering additional data-refresh features in Micron-firmware automotive eMMC 5.1 devices.

This case is **not**:

- a generic history of eMMC, JEDEC eMMC 5.1, BKOPS, NAND read reclaim, or Flash refresh;
- a claim that every Micron eMMC device implements this feature identically;
- a claim that every eMMC `CMD49` use means `SET_TIME` or triggers refresh;
- proof of the exact physical page/block relocation or rewrite geometry inside the controller;
- proof that every NAND cell is read or rewritten during one self-refresh run;
- a claim that one day is a NAND data-retention limit;
- an invention-priority claim for self-refresh, retention scanning, ECC-conditioned renewal, or host-assisted Flash maintenance;
- a claim that the product's `self refresh` is the same mechanism as DRAM refresh.

The useful retention boundary is narrower:

> **A managed nonvolatile device can retain both payload and second-order evidence used to schedule future renewal. In the bounded Armadillo/Micron integration, host time injection, reset, elapsed-time eligibility, bus idleness, ECC-threshold selection, execution, and completion/history telemetry are distinct states and transitions.**

## Historical vocabulary

The inspected Atmark manual uses:

- `data retention`;
- `self refresh`;
- `SET_TIME (CMD49)`;
- `RTC`;
- `Delay 1` and `Delay 2`;
- `ECC`;
- `Self Refresh progress of scan`;
- `Number of Blocks in Refresh Queue`;
- `Self Refresh Completion date`;
- `Self Refresh Loop Count`;
- `Refresh Count`;
- `Power Loss Counter`.

Terms such as **maintenance eligibility**, **host-supplied time evidence**, **maintenance authority**, **renewal selection**, and **second-order maintenance history** are project engineering terms. They must not be projected backward as vendor vocabulary.

## Historical record

### H/P — the 2021 product manual already documents automatic eMMC retention work

Atmark Techno's Armadillo-IoT Gateway G4 Product Manual version 1.0.0 is dated **2021-12-09**. Its eMMC data-retention section explains that the product's eMMC can perform data-retention work automatically when data has gone unread for long periods. The manual describes the operation as `self refresh` in Micron tooling.

The same version 1.0.0 HTML manual documents two start policies selected by a one-time-programmable setting:

1. execute after every reset; or
2. compare an eMMC internal-register value with a value supplied by command and execute when at least one day has elapsed.

The Armadillo-shipped configuration is the second policy.

This establishes a product-integration floor. It does **not** establish when Micron first invented or first shipped the feature, nor when any corresponding eMMC-standard command semantics first appeared.

### H/P — reset opens a time-supply window; reset is not the maintenance action

For the shipped second policy, the manual gives this sequence:

1. the host performs a hardware or software reset of the eMMC;
2. within `Delay 1`, the host issues `SET_TIME (CMD49)`;
3. the eMMC controller monitors bus activity;
4. after the bus becomes idle and `Delay 2` elapses, the controller performs self refresh.

The documented Armadillo settings are:

- `RTC`: ON;
- `Delay 1`: **60 s**;
- `Delay 2`: **100 ms**.

Therefore the reset transition is a **control window boundary**, not evidence that renewal itself has completed.

### H/P — elapsed-time eligibility does not force immediate execution

Atmark's sequence inserts bus-idle observation and a post-idle delay between time qualification and self-refresh execution. This is important because the controller may know that maintenance is due while still deferring the work until a service opportunity exists.

The bounded record therefore separates:

```text
elapsed-time condition satisfied
    !=
bus idle
    !=
self-refresh started
    !=
self-refresh completed
```

### H/P — renewal is selective under the documented policy

The implementation section says self refresh is performed **only for cells whose ECC-related errors exceed threshold 2**. The source does not expose the controller's exact raw-NAND geometry, relocation algorithm, codeword mapping, or whether the maintenance physically rewrites the same cells versus moves corrected data elsewhere.

Thus the safe historical statement is:

> the product documentation describes **error-threshold-selected** self-refresh work, not an unconditional full-medium rewrite.

### H/P — maintenance state is itself observable and partly retained

The manual says Micron's `emmcparm` tool can expose data-retention statistics stored inside the eMMC. It describes at least:

- execution count;
- the counter value at the most recent completed retention operation;
- current progress of the retention operation.

The shown Secure Smart Report also includes fields such as `Self Refresh progress of scan`, `Self Refresh Loop Count`, `Refresh Count`, `Power Loss Counter`, and a refresh queue/completion-related state in the fuller report.

This gives a concrete managed-Flash example where the user payload is not the only retained state relevant to future retention work.

### H/P* — Micron's 2023 catalog independently confirms the vendor feature family

Micron's official eMMC software/download page lists **TN-FC-60** on **11 April 2023** with the title _Refresh Features for Micron e.MMC Automotive 5.1 Devices_. Micron's catalog description says the note covers additional data-refresh features available in automotive eMMC 5.1 devices built with Micron firmware.

The full TN-FC-60 body was login-gated during this research pass, so this source is used only for title/date/scope confirmation. Detailed timing, threshold, trigger, and statistics claims above remain anchored to the Atmark product documentation rather than silently attributed to an uninspected Micron note.

## Retained states and control states

At least six state classes must remain separate in this case:

1. **user payload** — the logical data whose later readability is the ultimate service concern;
2. **physical/electrical media condition** — charge distribution and error tendency in NAND, not directly exposed as a complete history;
3. **time/eligibility state** — the eMMC internal value compared with host-supplied time under the shipped RTC policy;
4. **current maintenance work state** — scan progress and refresh queue/progress information;
5. **maintenance history/telemetry** — loop count, refresh count, completion-related values, and power-loss count;
6. **policy configuration** — the OTP-selected trigger mode and integration parameters such as Delay 1/Delay 2.

They have different lifetimes and meanings. Preserving one does not imply preserving the others.

## Engineering reconstruction

### E — host time evidence is neither payload nor maintenance execution

`SET_TIME` supplies a value used by the device's retained-control relation. It does not itself prove that a data-bearing NAND region was renewed.

> **host time injection != self-refresh execution**.

Likewise, a correct time comparison can establish that maintenance is eligible while the controller still waits for bus idleness.

### E — reset is a protocol opportunity, not a refresh synonym

Because the documented path begins after reset but still requires the command window, idleness, delay, selection, and execution:

> **reset != refresh**;

and:

> **successful boot != demonstrated maintenance completion**.

This matters for systems that boot often but remain too busy, fail to supply the required time value, lose power during work, or otherwise do not complete the described path.

### E — one-day policy interval is not a one-day physical retention constant

The manual's shipped policy compares values and begins retention when at least one day has elapsed. That is an **operator/device control cadence**. It is not evidence that NAND becomes unreadable after 24 hours, nor that every selected cell requires daily rewriting.

> **maintenance-trigger interval != physical failure deadline**.

### E — error evidence can authorize selective renewal without preserving a full error history

The threshold supplies enough information to select regions for maintenance. It does not produce a complete chronology of charge loss or every corrected bit.

> **ECC-threshold crossing != complete degradation history**.

The mechanism therefore fits a broader repository pattern: a compressed or derived maintenance state can be operationally sufficient without being an archive of the physical process it summarizes.

### E — maintenance telemetry does not become payload merely because it persists

A `Refresh Count` or `Self Refresh Loop Count` may survive long enough to inform later tooling while remaining second-order device state.

> **retained maintenance history != retained user object**.

Conversely, a progress field of zero can mean “not running now” while past loop/refresh counts still attest to earlier maintenance. Current activity and historical activity are separate.

### E — powered idle opportunity can be retention infrastructure

The controller waits for an idle bus before executing. Therefore ordinary service load and retention work share a scheduling boundary:

> **maintenance due != maintenance schedulable immediately**.

A device may be physically powered and logically healthy while a maintenance obligation waits for an acceptable execution opportunity.

### E — host assistance does not imply host selection of physical targets

The host supplies reset/time conditions; the controller evaluates idleness and ECC-related selection. The inspected source does not show the host naming individual physical NAND cells or blocks to refresh.

This is a useful authority split:

```text
host: provides temporal/control input
controller: evaluates device-local condition and schedules work
media path: executes undisclosed renewal mechanics
```

Do not collapse that into either “fully autonomous device refresh” or “host directly refreshes NAND.”

## Cross-case comparison

### Case 36 — Flash Correct-and-Refresh

Case 36 is a research mechanism in which ECC-related evidence is used to identify data needing correction/refresh. Case 135 supplies a shipped embedded-product witness in which ECC-error thresholding participates in selective self-refresh.

The similarity is **functional only**. The sources do not establish algorithm identity, implementation descent, or a Case-36-to-Micron genealogy.

### Case 37 — Samsung 840 EVO periodic refresh

Both cases show powered controller maintenance in managed Flash, but the documented target property, trigger, product family, and control path differ. Case 37 must not be used to fill gaps in the Micron eMMC implementation, or vice versa.

### Case 111 — enterprise SSD extended shutdown

Case 111 shows vendor/operator runbooks that reserve powered time for hidden SSD retention work. Case 135 moves the boundary inward: an embedded host can supply time and reset conditions, after which the eMMC controller waits for idle opportunity and selects error-threshold-qualified work.

Thus:

> **operator maintenance schedule != embedded device maintenance protocol**.

They can be compared as different places where retention work crosses a system boundary, not as one mechanism.

### Syntheses 24, 26, and 27

Case 135 is a useful concrete stress test for the existing maintenance framework:

- **Synthesis 24:** the trigger is composite, combining reset, elapsed-time evidence, bus-idle opportunity, delay, and local error selection rather than one pure `periodic` trigger;
- **Synthesis 26:** trigger policy, current progress, and accumulated maintenance statistics have different persistence horizons;
- **Synthesis 27:** host-supplied time and ECC evidence are policy inputs whose validity/representativeness must not be confused with the payload they help protect.

These are project comparisons, not vendor historical vocabulary.

## Failure and forgetting boundaries

Distinct failure modes include:

- payload charge/error margin degrades while the device remains powered off or unread;
- reset occurs but the required time command is not supplied inside the documented window;
- the elapsed-time condition is met but bus activity delays execution;
- self refresh begins but power loss interrupts or prevents completion;
- maintenance statistics survive even though they do not prove every payload region is currently safe;
- current progress becomes zero after work ends, while maintenance history still records prior activity;
- a region never crosses the documented error threshold during a given scan and therefore is not selected by that rule;
- the device/controller or its tooling becomes unavailable even though NAND state physically remains.

None of these transitions, by itself, proves secure erasure, physical remanence elimination, or a new universal retention guarantee.

## Claim ledger

| Claim | Layer | Evidence strength | Boundary |
| --- | --- | --- | --- |
| Armadillo G4 manual v1.0.0 documents automatic eMMC data-retention/self-refresh behavior | `H/P` | strong | product integration evidence, not eMMC-wide law |
| shipped configuration compares retained/internal time state with command-supplied value and uses a >=1-day condition | `H/P` | strong | bounded Armadillo/Micron integration |
| reset opens a Delay-1 command window and is followed by bus-idle/Delay-2 gating | `H/P` | strong | documented integration values 60 s / 100 ms |
| ECC-related threshold 2 selects cells for self refresh | `H/P` | strong | source wording; exact raw-NAND geometry undisclosed |
| emmcparm exposes current and historical self-refresh statistics | `H/P` | strong | tool/report surface, not payload history |
| Micron TN-FC-60 exists and covers extra refresh features for automotive eMMC 5.1 Micron firmware | `H/P*` | strong for metadata | full body not inspected in this pass |
| host time injection != refresh execution | `E` | strong | derived from multi-stage documented sequence |
| one-day trigger != one-day media-retention limit | `E/X` | strong | policy interval must not become physical cliff |
| progress/history telemetry != future-retention guarantee | `E/X` | strong | no such guarantee in inspected sources |
| Case 36 / 37 / 111 similarity proves genealogy | `X` | rejected | comparison is functional only |
| `self refresh` here is identical to DRAM refresh | `X` | rejected | same English label, different managed-Flash mechanism |

## Philosophical / media-theoretical limit

A narrow project-level interpretation is defensible:

> Technical persistence may require retaining not only a payload, but enough evidence to decide **when renewal is due** and enough control state to stage that renewal later.

The value of this case is that temporal evidence, workload opportunity, error evidence, and maintenance history all sit around the payload without becoming the payload itself.

The interpretation stops there. Atmark and Micron do not present this mechanism as a theory of memory, temporality, or human remembering.

## Related repositories

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Micron eMMC` and `SET_TIME eMMC` found no dedicated matching technical-history module during this pass.

A broad genealogy of eMMC maintenance commands, JEDEC revision history, BKOPS, controller architecture, read reclaim, and Micron firmware generations belongs primarily in `computing-archaeology` if developed. This case keeps only the retention-specific relation among time evidence, execution opportunity, selective renewal, and retained maintenance state.

## Deepening — standard BKOPS is a maintenance-opportunity interface, not a synonym for vendor self refresh

JESD84-B51 (February 2015) gives e.MMC a standard **Background Operations** control surface. Manual BKOPS uses `BKOPS_START[164]`; `MANUAL_EN` lets the host advertise periodic service windows; `BKOPS_STATUS[246]` reports urgency from no work required through critical outstanding work. With `AUTO_EN`, the device may start or stop background work during idle time without notifying the host, while the host is advised to keep device power active.

That surface must stay separate from the Micron/Armadillo retention path documented above. BKOPS exposes **maintenance support, urgency, and scheduling opportunity**; the vendor path exposes **reset/time eligibility, bus-idle gating, ECC-threshold selection, and self-refresh telemetry**. The inspected sources do not establish that either state machine drives the other.

```text
BKOPS supported
    != BKOPS work outstanding
    != BKOPS urgent
    != BKOPS executing
    != a particular hidden Flash algorithm demonstrated

vendor self-refresh due != generic BKOPS urgency
shared powered-idle opportunity != shared mechanism
```

JESD84-B51 also defines `SANITIZE_START[165]` separately from `BKOPS_START[164]`. Accordingly, `BKOPS_STATUS = 0` or completed BKOPS is not evidence of sanitize completion, secure erasure, or elimination of stale physical embodiments.

The bounded evidence and chronology ledger is in [`../evidence/135-jedec-emmc51-bkops-maintenance-opportunity-deepening.md`](../evidence/135-jedec-emmc51-bkops-maintenance-opportunity-deepening.md). February 2015 is used only as the public floor for the inspected e.MMC 5.1 control semantics, not as an invention date for Flash background maintenance or manual BKOPS.


## Open research debt

- obtain and directly inspect the full Micron TN-FC-60 body;
- identify the exact Micron eMMC part/firmware revision in the bounded Armadillo configuration and any product errata;
- trace `SET_TIME (CMD49)` and the relevant vendor extension against official JEDEC eMMC revision history without assuming command-number identity across contexts;
- trace pre-5.1 manual BKOPS and the later background-operation-control genealogy directly in JEDEC revisions; do not infer the full genealogy from JESD84-B51 alone;
- obtain independent fault-injection evidence for interrupted self-refresh and time-source faults;
- determine the exact physical rewrite/relocation and ECC-codeword geometry only from appropriate implementation evidence;
- test whether the exposed maintenance statistics survive specific power/reset/firmware transitions and what their reset semantics are.

## Sources

- Atmark Techno, **Armadillo-IoT Gateway G4 Product Manual, version 1.0.0**, 9 December 2021. eMMC data-retention section 9.9: <https://manual.atmark-techno.com/armadillo-iot-g4/armadillo-iotg-g4_product_manual_ja-1.0.0/ch09.html>. Versioned PDF cover/date: <https://armadillo.atmark-techno.com/files/downloads/armadillo-iot-g4/document/armadillo-iotg-g4_product_manual_ja-1.0.0.pdf?v=1639041210>.
- Atmark Techno, **Armadillo-IoT Gateway G4 Product Manual, current maintained HTML**, eMMC data-retention section (later editions preserve the mechanism with section renumbering): <https://manual.atmark-techno.com/armadillo-iot-g4/armadillo-iotg-g4_product_manual_ja/ch06.html>.
- Micron Technology, **eMMC software / technical-note catalog**, entry for `TN-FC-60: Refresh Features for Micron e.MMC Automotive 5.1 Devices`, dated 11 April 2023: <https://www.micron.com/sales-support/downloads/software-drivers/emmc-software>.

## Prior-art follow-up — manual BKOPS is publicly grounded by e.MMC 4.41

A bounded follow-up moves the repository's conservative public standardized floor for **generic manual BKOPS** earlier than the 2015 e.MMC 5.1 witness. JESD84-A441's public record is dated **1 March 2010** and names `Background Operation` in the e.MMC 4.41 title; period SanDisk (25 February 2010) and Kingston Solutions (June 2011) e.MMC 4.41 product documents expose `BKOPS_START[164]` / `BKOPS_EN[163]`, with the Kingston document also exposing `BKOPS_SUPPORT[502]` and `BKOPS_STATUS[246]`.

This is a lower-bound correction, not an invention claim:

```text
public standardized generic manual-BKOPS floor <= e.MMC 4.41 / 2010
e.MMC 5.1 witness != origin of generic manual BKOPS
manual host-granted opportunity != later inspected AUTO_EN device scheduling
scheduling authority != physical-target authority != hidden algorithm identity
```

The 2009 e.MMC 4.4 public title lacks the later `Background Operation` phrase, but title metadata is not a clause-level A44→A441 diff and therefore cannot prove a first-introduction event. Direct normative diffing and the 4.41→4.5→4.51→5.0→5.1 genealogy remain evidence debt, with broader pre-eMMC maintenance history routed to `computing-archaeology`.

Prior-art deepening: [`../evidence/135-emmc441-2010-manual-bkops-prior-art-deepening.md`](../evidence/135-emmc441-2010-manual-bkops-prior-art-deepening.md).
