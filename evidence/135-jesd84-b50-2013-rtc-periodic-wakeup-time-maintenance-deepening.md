# Case 135 deepening evidence — e.MMC 5.0 SET_TIME / RTC and PERIODIC_WAKEUP as maintenance-time infrastructure (2013)

## Status

**`bounded deepening complete`** for a narrow standards/control-surface question: by JESD84-B50 (e.MMC 5.0, September 2013), the public e.MMC interface already standardized host-supplied real/relative time through `SET_TIME (CMD49)` and a separate `PERIODIC_WAKEUP` host/device maintenance schedule tied to completion of at least one Background Operation before power-down.

This record does **not** claim that e.MMC 5.0 invented `SET_TIME`, real-time-clock support, timed Flash maintenance, Background Operations, or refresh. It establishes a directly inspectable public normative floor for the specific 5.0 semantics used here and then compares that standard control surface with the later Micron/Armadillo self-refresh integration in Case 135.

## Research question

Case 135 already grounded a 2021 Armadillo/Micron path in which reset is followed by `SET_TIME (CMD49)`, an internal elapsed-time comparison, bus-idle gating, and selective self refresh. It also separately grounded generic BKOPS prior art back to e.MMC 4.41.

The open question was narrower:

> Before attributing the time-based behavior to Micron's vendor extension, what did the standard e.MMC command/control surface itself already say about host-supplied time and maintenance scheduling?

This pass asks only that question. It does not attempt a complete e.MMC 4.51→5.0 command genealogy or infer Micron's hidden firmware algorithm from standard clauses.

## Source boundary

### Standard text — JESD84-B50

The inspected text is a public text-preserving copy of JEDEC **JESD84-B50, _Embedded Multi-Media Card (e•MMC) Electrical Standard (5.0)_**, revision of JESD84-B451, June 2012, dated **September 2013**:

<https://pdfcoffee.com/jesd84-b50-pdf-free.html>

Relevant locations in the preserved pagination:

- printed p. 103, §6.6.38 `Real Time Clock Information`;
- printed p. 104, §6.6.38.1 `Periodic Wake-up`;
- printed p. 199, §7.4.89 `PERIODIC_WAKEUP [131]`;
- command table entry for `CMD49`, `SET_TIME`.

A contemporaneous republication of JEDEC's 2 October 2013 announcement independently identifies JESD84-B50 as the published e.MMC 5.0 revision and links to JEDEC's then-public download endpoint:

<https://www.design-reuse.com/news/202524265-jedec-announces-publication-of-e-mmc-standard-update-v5-0/>

The mirrored standard is used for clause-level inspection because the current JEDEC site was not directly crawlable in this research pass. The republication is publication-metadata corroboration, not a substitute for the clauses.

### Product/integration witness — Atmark Techno

Atmark Techno's official Armadillo-IoT Gateway G4 manual preserves the later product-specific path:

- version 1.0.0, dated 9 December 2021: <https://manual.atmark-techno.com/armadillo-iot-g4/armadillo-iotg-g4_product_manual_ja-1.0.0/ch09.html>;
- current maintained manual: <https://manual.atmark-techno.com/armadillo-iot-g4/armadillo-iotg-g4_product_manual_ja/ch06.html>.

The manual says the shipped RTC-on policy compares an internal register with the value supplied by `SET_TIME (CMD49)`, uses a one-day eligibility condition, then waits for bus idleness and `Delay 2` before running selective self refresh on cells whose ECC-related errors exceed threshold 2.

### Micron scope witness

Micron's official eMMC software/technical-note catalog lists **TN-FC-60, _Refresh Features for Micron e.MMC Automotive 5.1 Devices_**, dated 11 April 2023, and describes it as covering additional data-refresh features in Micron-firmware automotive eMMC 5.1 devices:

<https://www.micron.com/sales-support/downloads/software-drivers/emmc-software>

The full TN-FC-60 body is account/sign-in gated in this pass. It is therefore used only for title/date/scope confirmation, not for uninspected internal details.

## Historical record

### H/P — e.MMC 5.0 explicitly connects host-provided time to internal maintenance

JESD84-B50 §6.6.38 states that providing real-time-clock information to the device **may be useful for internal maintenance operations**. The host may provide either:

- absolute time based on UTC; or
- relative time.

The standard therefore exposes time information as a device-control input whose use can extend beyond ordinary timestamp presentation.

The bounded historical claim is:

> by the September-2013 e.MMC 5.0 text, host-supplied time was explicitly standardized as information that a device could use for internal maintenance.

This does not establish the first appearance of the idea in e.MMC or storage history.

### H/P — `SET_TIME (CMD49)` transfers a typed time-information block

The same section says the host shall use `CMD49 (SET_TIME)` to set the real-time-clock information. The command transfers a 512-byte information block whose `RTC_INFO_TYPE` distinguishes three allowed time relations:

1. absolute time;
2. set-base for relative time; and
3. relative time measured since the most recent set-base operation.

The standard thus does not require one single interpretation of “time.” It provides both absolute and relative temporal references.

The command table separately names `CMD49` as `SET_TIME`.

### H/P — the host is expected to renew time information at lifecycle boundaries

JESD84-B50 says the host should send time information:

- after power-up, as early as possible;
- after waking from sleep, as early as possible; and
- periodically, with examples such as hourly or daily updates.

This makes the time relation itself subject to maintenance/update. The host is not merely a passive reader of a permanently correct device clock.

The safe relation is:

```text
standard exposes time state
    != standard guarantees an autonomous battery-backed wall clock
```

The source specifies host updates; it does not justify importing a particular oscillator, battery, or persistence implementation.

### H/P — e.MMC 5.0 separately standardizes a periodic maintenance wake-up contract

JESD84-B50 §6.6.38.1 defines `PERIODIC_WAKEUP` at EXT_CSD byte 131. The host may set this register to indicate how often it shall wake the device.

Once configured, the host must repeat a sequence at least as often as the configured interval:

```text
power up device
    -> execute at least one BKOPS_START background operation
    -> let that operation run to completion without interruption
    -> only then power the device down
```

The host may perform other work while powered, provided the device is not left powered down longer than the configured interval.

This is a stronger relation than merely “turn the device on sometimes.” It names a maintenance execution and completion requirement before the next shutdown.

### H/P — `PERIODIC_WAKEUP` includes an explicit no-wakeup value

JESD84-B50 §7.4.89 defines the encoded time unit and period. Unit `0x0` means **infinity / no wakeups**; other units include months, weeks, days, hours, and minutes.

Therefore:

> the presence of a standard periodic-wakeup field does not mean every conforming device necessarily demands periodic wakeups.

The field is a control surface with a disabled/infinite state, not a universal NAND retention timer.

### H/P — generic Background Operations already have their own control relation

The same e.MMC 5.0 text's Background Operations section describes device-internal maintenance that is preferably performed when the host is not being serviced, and the host/device handshake around `BKOPS_START` / `BKOPS_EN`.

Case 135's separate prior-art record already moves generic manual BKOPS to e.MMC 4.41 / 2010. The significance here is not to re-ground BKOPS history, but to show how e.MMC 5.0 composes:

- host-supplied time information;
- a periodic wakeup schedule;
- a background-maintenance execution interface; and
- an explicit completion-before-power-down relation.

## Retained/control-state decomposition

This standard-level witness requires several states to remain separate.

### 1. User payload

Logical data stored in the eMMC. Neither `SET_TIME` nor `PERIODIC_WAKEUP` is itself the payload.

### 2. Host time source / supplied temporal evidence

The host supplies absolute or relative time information. This is evidence used by device logic, not proof that any media region has been renewed.

### 3. Device time relation

The device receives/updates the real or relative time relation addressed by `SET_TIME`. The standard defines behavior at the interface, not the exact physical register or persistence substrate.

### 4. Periodic wakeup policy

`PERIODIC_WAKEUP[131]` expresses the configured maximum interval between maintenance wakeups, including an infinity/no-wakeup state.

### 5. Background-maintenance obligation/status

Generic BKOPS support/status says maintenance may exist or be required. It is not the same state as the wakeup interval.

### 6. Maintenance execution

Writing `BKOPS_START` opens the actual background-operation execution path.

### 7. Completion relation

For the periodic-wakeup sequence, the standard requires at least one background operation to run to completion without interruption before power-down.

These relations cannot be collapsed into one field called “refresh state.”

## Engineering reconstruction

### E — temporal reference is maintenance input, not maintenance execution

JESD84-B50 directly licenses the weaker statement that time information may assist internal maintenance. It does not say `SET_TIME` itself rewrites NAND.

```text
host supplies time
    != maintenance due
    != maintenance selected
    != maintenance executing
    != maintenance completed
```

This is especially important when reading the later Armadillo/Micron integration, where the vendor flow adds a one-day comparison, idle gating, and ECC-threshold selection after `SET_TIME`.

### E — time transport and maintenance policy can be standardized at different layers

The standard defines how to convey absolute/relative time and how to configure a generic wakeup cadence. A vendor firmware can then use that temporal evidence in a more specific retention policy.

Thus:

> **standard temporal plumbing != standardized vendor self-refresh algorithm**.

The Armadillo/Micron one-day rule is not automatically a JEDEC rule merely because it consumes `CMD49`.

### E — scheduling state, maintenance debt, execution, and completion are different

`PERIODIC_WAKEUP` gives a schedule/deadline relation. BKOPS exposes maintenance work and a way to run it. Completion is a further transition.

```text
configured wakeup interval
    != current BKOPS debt/status
    != BKOPS execution
    != BKOPS completion
```

A configured interval can exist before work starts. A background operation can run without revealing which physical pages or blocks it services. Completion of generic BKOPS still does not prove completion of a vendor-specific self-refresh algorithm unless device-specific evidence links the two.

### E — maintenance opportunity can cross a power-management boundary

The periodic-wakeup sequence makes host power policy part of the maintenance contract:

```text
device powered down
    -> host reaches configured wakeup boundary
    -> host powers device
    -> host grants background-operation execution
    -> operation completes
    -> host may power down again
```

This is not the same claim as “NAND needs power every N days.” The configured interval is a control value whose admissible units range from minutes to months and includes no-wakeup/infinity.

### E — host assistance does not reveal physical-target authority

In the standard witness the host supplies time, power opportunity, and BKOPS invocation. The standard does not thereby expose which NAND regions the controller selects or what hidden maintenance algorithm runs.

For the later Armadillo/Micron witness, Atmark adds evidence that the controller applies an ECC-related threshold. That device-specific selection evidence must remain separate from generic JEDEC BKOPS.

## Direct comparison with the Armadillo/Micron self-refresh path

The later product integration can now be decomposed without treating every component as proprietary.

### Standard part visible by e.MMC 5.0

- `CMD49` is `SET_TIME`;
- absolute and relative time can be host supplied;
- time information may be useful for internal maintenance;
- generic BKOPS supplies a maintenance-execution control surface;
- `PERIODIC_WAKEUP` supplies a generic wakeup/maintenance cadence relation.

### Product/vendor-specific relation documented by Atmark

- reset opens a `Delay 1` window;
- Armadillo sends `SET_TIME` inside that window;
- firmware compares an internal value with the supplied value;
- the shipped RTC-on policy uses a >=1-day condition;
- the controller waits for bus idleness plus `Delay 2`;
- self refresh is selected only for cells above an ECC-related threshold;
- vendor tooling exposes self-refresh progress/history statistics.

The bounded result is:

```text
standard SET_TIME semantics
    + vendor elapsed-time policy
    + vendor idle gating
    + vendor error-threshold selection
    + vendor maintenance telemetry
    = documented Armadillo/Micron retention path
```

But this is an analytical decomposition, not proof that Micron's hidden firmware literally implements the standard `PERIODIC_WAKEUP` state machine or uses generic BKOPS to perform its self refresh.

### Critical non-equivalences

```text
SET_TIME accepted != self refresh started
PERIODIC_WAKEUP configured != self refresh due
BKOPS started != Micron self refresh demonstrated
BKOPS completed != Micron self-refresh completion demonstrated
one-day Micron/Armadillo policy != JEDEC retention interval
standard time input != standard physical refresh algorithm
```

## Functional comparisons only

### Case 03 — DRAM refresh

Both cases make time relevant to continued technical availability. The mechanisms are not the same.

- DRAM refresh periodically restores volatile cell charge under a deadline/coverage relation.
- e.MMC 5.0 `SET_TIME` supplies temporal evidence to a managed nonvolatile device; the standard does not require that each time update itself regenerate media.

Therefore:

> **time-bearing maintenance relation != one common refresh mechanism**.

No genealogy is asserted.

### Case 111 — enterprise SSD extended-shutdown maintenance

Case 111 shows operator/system runbooks that schedule powered time after extended shutdown so hidden SSD maintenance can occur. JESD84-B50 exposes a lower-level host/device contract in which a configured wakeup interval leads to power-up and completed background work before shutdown.

The functional comparison is:

```text
human/operator maintenance schedule
    != protocol-level host/device wakeup contract
```

Both can make external scheduling part of retention infrastructure, but they differ in scope, product class, authority, and evidence.

## Prior-art and chronology boundary

The safe chronology is deliberately conservative:

- JESD84-B50 is dated September 2013 and is a revision of JESD84-B451, June 2012;
- the inspected 5.0 text definitely contains `SET_TIME`, real/relative time semantics, and `PERIODIC_WAKEUP`;
- Case 135 separately grounds generic manual BKOPS no later than e.MMC 4.41 / 2010;
- this pass does **not** inspect JESD84-B451 clause-by-clause and therefore does not claim that 5.0 first introduced RTC / `SET_TIME` / `PERIODIC_WAKEUP`;
- no direct genealogy is asserted from JEDEC's generic maintenance controls to Micron's later automotive self-refresh implementation.

This closes only the Case 135 debt of establishing a directly inspectable standard-level floor for the `SET_TIME (CMD49)` semantics relevant to the later integration.

## Explicit non-claims

This evidence does **not** establish that:

1. e.MMC 5.0 invented `SET_TIME`, RTC support, timed maintenance, or periodic wakeup;
2. `SET_TIME` itself refreshes, rewrites, relocates, or repairs NAND;
3. the device contains an autonomous battery-backed wall-clock merely because the interface says `Real Time Clock Information`;
4. every device requires periodic wakeups;
5. `PERIODIC_WAKEUP` is a raw NAND retention-limit field;
6. a configured wakeup interval is a prediction of physical failure time;
7. all BKOPS work is retention refresh;
8. completion of generic BKOPS proves Micron self-refresh completion;
9. Micron's one-day Armadillo policy is standardized by JEDEC;
10. Micron's self refresh is driven by the standard `PERIODIC_WAKEUP` field;
11. Micron's self refresh is implemented as generic `BKOPS_START` work;
12. host-provided time identifies the physical NAND targets to renew;
13. every time update or every boot causes media renewal;
14. the full TN-FC-60 body was inspected in this pass;
15. similarity between DRAM refresh, SSD maintenance windows, and eMMC timed maintenance proves a shared historical lineage.

## Claim ledger

| Claim | Layer | Evidence strength | Boundary |
| --- | --- | --- | --- |
| JESD84-B50 is e.MMC 5.0, revision of B451, dated September 2013 | `H/P` | strong | preserved JEDEC text + contemporaneous publication notice |
| B50 says RTC information may be useful for internal maintenance | `H/P` | strong | direct §6.6.38 wording |
| B50 `CMD49` is `SET_TIME` with a 512-byte typed time-information block | `H/P` | strong | direct §6.6.38 + command table |
| B50 permits absolute time, relative-time base, and relative-time delta | `H/P` | strong | direct table |
| host should update time after power-up, wake, and periodically | `H/P` | strong | direct §6.6.38 wording |
| B50 `PERIODIC_WAKEUP[131]` can require power-up + at least one uninterrupted BKOPS to completion before power-down | `H/P` | strong | direct §6.6.38.1 wording |
| `PERIODIC_WAKEUP` includes infinity/no wakeups | `H/P` | strong | direct §7.4.89 wording |
| time input != maintenance execution | `E` | strong | standard separates input/control from BKOPS work |
| wakeup schedule != maintenance debt != execution != completion | `E` | strong | separate standard fields/transitions |
| B50 semantics explain Micron's entire later self-refresh algorithm | `X` | rejected | device-specific policy remains separate |
| e.MMC 5.0 invented RTC/SET_TIME | `X` | rejected | 4.51 normative diff not inspected |
| BKOPS completion proves vendor self-refresh completion | `X` | rejected | no inspected linkage |

## Related-repository check

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `SET_TIME eMMC`, `PERIODIC_WAKEUP`, and `eMMC RTC` returned no dedicated matching technical-history module in this pass.

A full eMMC command-history genealogy — especially direct 4.51→5.0→5.1 clause diffs and pre-eMMC timed-maintenance ancestry — belongs primarily there if developed. This evidence record keeps only the retention-specific boundary between temporal input, wakeup scheduling, maintenance opportunity, execution/completion, and vendor-specific renewal policy.

## Philosophical limit

A narrow project-level interpretation survives:

> time itself can become an externally supplied operational relation that helps a storage device decide when maintenance should be possible or due.

That does not make `SET_TIME` a theory of temporality, human memory, or cultural retention. It is a protocol/control fact about how one technical system can depend on temporal evidence to sustain future availability.

## Resulting bounded relations

```text
host time source
    != device time relation
    != maintenance eligibility
    != maintenance debt/status
    != execution opportunity
    != maintenance execution
    != completion

SET_TIME semantics standardized by inspected e.MMC 5.0
    != vendor self-refresh standardized

PERIODIC_WAKEUP
    -> host/device maintenance schedule
    != physical NAND retention deadline

standard temporal plumbing
    != vendor physical-target policy
```

## Remaining evidence debt

- directly inspect JESD84-B451 and earlier revisions before assigning a first-introduction point to `SET_TIME`, RTC, or `PERIODIC_WAKEUP`;
- obtain and inspect the full Micron TN-FC-60 body under an authorized access path before attributing undocumented internal semantics to Micron;
- identify the exact Micron part and firmware revision in the Armadillo G4 configuration;
- obtain fault-injection evidence for missing/incorrect time input, interruption during self refresh, and restart/recovery behavior;
- determine persistence/reset semantics of vendor maintenance statistics from appropriate implementation evidence;
- keep generic eMMC command-history work in `computing-archaeology` unless it directly changes a retention claim in this repository.
