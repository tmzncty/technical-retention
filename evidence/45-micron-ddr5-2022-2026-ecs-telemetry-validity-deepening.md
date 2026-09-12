# Case 45 deepening — Micron DDR5 ECS telemetry validity, filtering, reset, and reporting horizon (2022–2026)

## Status

**Deepening evidence for grounded Case 45.**

Case: [`../cases/45-micron-ddr5-on-die-ecc-ecs.md`](../cases/45-micron-ddr5-on-die-ecc-ecs.md).

Cross-case comparison: [`../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md).

This slice closes a bounded evidence debt left by the original Case 45: what proposition does DDR5 ECS correction telemetry actually retain, and what does a reset or zero value mean? It does **not** claim to complete a revision-by-revision audit of JESD79-5, establish cross-vendor identity, or prove power-fail persistence of the reporting registers.

## Research question

The original case correctly treated ECS correction telemetry as second-order retention state, but the phrase is too broad unless the telemetry contract is reconstructed precisely.

The bounded question is:

> Is an ECS error count a complete, lifetime history of corrected DRAM errors, or is it a mode-relative, filtered, resettable summary whose meaning depends on the current ECS reporting configuration and scrub-progress boundary?

The inspected Micron product record and later Linux control surface support the second interpretation.

## Evidence custody and source roles

### E1 — Micron DDR5 SDRAM Product Core Data Sheet, Rev. D 10/2022

**Source:** Micron Technology, *DDR5 SDRAM Product Core Data Sheet*, document identifier `CCM005-1684161373-23`, Rev. D 10/2022, especially pp. 281–286, `ECC Transparency and Error Scrub`.

Public vendor-document mirror used in this slice:

<https://static6.arrow.com/aropdfconversion/fc2b144ccf061160504edd742d01cb58fdda91bb/ddr5_sdram_core.pdf>

**Custody note:** the document is Micron-authored and carries Micron revision/document identifiers, but this slice accessed it through a distributor mirror rather than an origin-hosted Micron archive. It is therefore used as a strong manufacturer-primary content witness with a custody caveat. A byte-identical or origin-hosted archival copy would improve provenance but is not required for the bounded relations below.

The relevant manufacturer vocabulary includes:

- `ECC transparency and error scrub` / `ECS`;
- Manual ECS and Automatic ECS;
- `Error Counter (EC)`;
- `Errors per Row Counter (EpRC)`;
- row-count and code-word-count modes;
- ECS threshold filters;
- `Reset ECS counters` in MR14;
- result/reporting registers MR16–MR20 in the inspected revision.

### E2 — Linux kernel EDAC Scrub Control, written for Linux 6.15 and maintained current documentation

**Sources:**

- Linux kernel documentation, `Scrub Control`, written for Linux 6.15: <https://docs.kernel.org/6.15/edac/scrub.html>;
- maintained current `Scrub Control`: <https://docs.kernel.org/edac/scrub.html>;
- Linux testing ABI documentation for `sysfs-edac-ecs`, including `mode`, `reset`, and `threshold`: <https://docs.kernel.org/admin-guide/abi-testing.html>.

**Role:** later host/control-surface evidence. Linux documents CXL DDR5 ECS as a JEDEC DDR5 feature, describes internal read/correct/writeback, and exposes host-visible controls for count mode, threshold, and reset where the underlying driver implements them.

This source is **not** used to project Linux/CXL sysfs encoding backward into every bare DDR5 device or to claim that its exposed numeric threshold set is identical to every Micron MR15 encoding.

## Historical record

### 1. Micron exposes two different ECS count semantics

Micron's Rev. D product document says ECS maintains an `Error Counter (EC)` plus an `Errors per Row Counter (EpRC)`.

The EC does not have one timeless meaning. It can operate in:

- **row mode** — count rows in which at least one code-word error was detected;
- **code-word mode** — count detected code-word errors.

The selection is represented in MR14. Therefore two identical numeric EC values do not necessarily state the same proposition unless the count mode is also known.

Historical record:

> the product interface exposes a configurable measurement definition for ECS error counting.

Engineering reconstruction:

> **same numeric field != same metric without count-mode context**.

### 2. ECS telemetry is filtered before reporting

Micron states that EC counting/reporting is subject to an ECS threshold filter and that EpRC reporting is subject to a separate threshold relation. The later Linux ECS ABI independently exposes a threshold control and explicitly says error counts below the configured threshold are masked in that control model.

This blocks a common diagnostic shortcut:

> **no reported/count-visible error under a thresholded interface != proof that no correctable error occurred**.

The device can perform corrective work while the exposed summary remains below the reporting threshold.

This is not a claim that every hidden event is lost internally in the same way; it is only a claim about what the inspected reporting contract warrants an external observer to infer.

### 3. EpRC is a maximum-row summary, not a per-row event ledger

Micron's `Errors per Row Counter` tracks the row with the largest code-word error count together with that row's address, subject to its reporting threshold.

That is a deliberately lossy summary relation:

```text
many rows may be visited
    -> one row can be retained as the current maximum-error row
    -> its error count + address can be reported
```

Therefore:

> **maximum-row summary != complete row-by-row scrub history**.

Nor does it establish the temporal order of detected errors within a scrub traversal.

### 4. Reset clears the reporting state and reinitializes ECS control state

Micron states that the ECC transparency/ECS counters are set to zero and internal ECS address counters are initialized by device `RESET` or by manually writing the ECS reset control (`MR14:OP[6] = 1b`). The document further says the ECS reset operation resets MR16–MR20.

Crucially, while the manual reset control remains asserted, ECS counters are reset and **additional ECS operations do not continue**; the control must return to zero before manual or automatic ECS proceeds again.

This makes reset more than a passive log-clear operation. It participates in the maintenance-control state machine.

Engineering reconstruction:

> **telemetry reset != repair rollback** — corrected array state already written by earlier scrub work is not thereby undone.

and:

> **counter reset != passive observation-only action** — in the documented state machine, holding reset also gates further ECS execution.

### 5. Reporting configuration has an epoch-like validity boundary

Micron says ECS selections including automatic ECS in self-refresh, threshold filter, manual/automatic mode, and row/code-word mode are to be programmed during device initialization and should not be changed after the first ECS operation unless followed by device RESET or `ECS RESET COUNTERS`; otherwise subsequent ECS behavior can be unknown.

`configuration epoch` / `reporting epoch` is a **project engineering term**, not Micron vocabulary. It captures the bounded relation:

```text
count-mode + threshold + ECS mode
    -> determine what later count state means

change those semantics
    -> reset/reinitialize before treating subsequent telemetry as a clean continuation
```

Thus:

> **retained counter value without retained configuration context != self-interpreting evidence**.

### 6. Manual ECS is corrective work, not merely measurement

Micron documents manual ECS as an internally timed sequence that includes activation, read, write, and precharge. Its internal read-modify-write cycle reads the protected code word, corrects a single-bit error if detected, and writes the resulting code word back to the array.

This preserves the original Case 45 distinction:

> **error evidence generation is coupled to corrective maintenance work, but evidence retention and repaired-array retention are not the same state**.

Resetting the former does not logically recreate the corrected physical defect that the earlier writeback repaired.

### 7. ECS requires initialized array/codeword state before its evidence is meaningful

Micron instructs that all array bits must have been written before executing ECS to avoid false failures.

This supplies a useful evidence-validity boundary:

> **telemetry mechanism available != telemetry evidence already semantically valid for unwritten/uninitialized array state**.

ECS interpretation presupposes initialized protected content/code state; otherwise observed failures can be artifacts of uninitialized state rather than evidence of an operationally retained payload defect.

### 8. The result registers retain a recent summary rather than a chronological archive

The same Micron ECS section describes loading the error summary / maximum-error-row information into the reporting mode registers at the scrub traversal boundary and retaining the most recently written result until a later result replaces it or an ECS/device reset clears it. Reads do not themselves constitute a history-preserving append operation.

The retention consequence is bounded but important:

> **latest retained ECS summary != event-by-event error history != lifetime error history**.

A result can outlive the immediate correction work that produced it while still being only the latest report for the relevant reporting epoch.

This slice does **not** claim that these report registers survive removal of power; the product evidence inspected here is used only to establish in-regime/reporting-state semantics.

## Later Linux control-surface boundary

Linux's EDAC ECS documentation makes the reporting semantics explicitly controllable from a later host stack where supported:

- `mode=0` represents row-count mode;
- `mode=1` represents code-word-count mode;
- `reset=1` resets the exposed ECS ECC counter to its default value;
- `threshold` masks counts below the selected threshold in the CXL ECS control model.

The general Scrub Control documentation also says the host/userspace can change error-count mode, reporting threshold, and reset the ECS counter, and that initiation may be a memory-controller/platform responsibility when unexpectedly high error rates are observed.

This supports a layered authority conclusion:

> **device-internal corrective work != device-exclusive authority over the meaning, visibility, and lifecycle of its diagnostic summary**.

But the Linux evidence remains a later CXL/EDAC composition. It does not prove that every 2022 Micron DDR5 deployment exposed these knobs to Linux, nor that sysfs values map one-to-one onto every vendor mode-register encoding.

## Cross-case comparison

### Case 15 — Intel SSD 320 unsafe-shutdown count

Case 15 grounds a cumulative lifetime count of unsafe shutdown events. It is a compact history summary, but its documented intent is cumulative over the drive lifetime.

Case 45 now supplies a counterexample to treating all diagnostic counters this way:

```text
Intel SSD 320 SMART C0h
    -> cumulative lifetime event count

DDR5 ECS report state
    -> mode-relative + threshold-filtered
    -> explicitly resettable
    -> latest/epoch-bounded corrective diagnostic summary
```

Functional analogy only:

> **both are second-order evidence about conditions affecting retained state; they do not share history semantics, mechanism, or genealogy**.

### Case 55 — NVMe Persistent Event Log

Case 55's PEL is a bounded typed event log with deletion/suppression rules. DDR5 ECS telemetry is not an event-by-event log simply because both can persist diagnostic information past an immediate operation.

Therefore:

> **diagnostic state retained after an operation != event log**.

### Synthesis 26 — maintenance-control-state persistence horizons

This slice adds a sixth form to the existing comparison:

- regime-local phase;
- restart-progress checkpoint;
- qualification/currentness map;
- retained policy plus re-observed runtime state;
- cumulative event-history summary;
- **resettable, filtered, mode-relative latest maintenance summary**.

That sixth form is useful because its persistence horizon and interpretation depend on a configuration/reporting epoch rather than a simple `durable / volatile` binary.

## Historical / reconstruction / analogy / interpretation boundary

### Historical record

Supported by the Micron manufacturer document and later Linux documentation:

- Manual and Automatic ECS;
- EC and EpRC;
- row-count vs code-word-count mode;
- threshold-filtered reporting/count semantics;
- resettable ECS counters and internal address-counter initialization;
- reset gating of subsequent ECS while asserted;
- mode/threshold selection constraints around initialization/reset;
- corrective read-modify-write behavior;
- later host-visible mode/threshold/reset controls in Linux's CXL ECS abstraction.

### Engineering reconstruction

Project-level relations:

- `same numeric field != same metric without count-mode context`;
- `thresholded absence != absence of correction/error`;
- `maximum-row summary != row-by-row history`;
- `telemetry reset != repair rollback`;
- `latest summary != event log != lifetime history`;
- reporting/configuration epoch as an evidence-validity boundary.

### Functional analogy

Case 15 and Case 55 are used only to compare history semantics and persistence horizon. No controller lineage, standards genealogy, or shared implementation is asserted.

### Philosophical interpretation

The bounded conceptual result is only this:

> technical systems can retain evidence that maintenance happened without retaining a complete history of that maintenance; what remains is selected by a reporting relation that can itself be configured, filtered, reset, and reinitialized.

This does not make the DRAM a historical archive or imply human-like memory of repair.

## Rejected upgrades / stop conditions

- **`ECS counter = lifetime error history` — rejected.** Count mode, thresholding, wrap/report replacement, and reset prevent that reading.
- **`counter is zero = no correctable errors have ever occurred` — rejected.** The counter can be reset and reporting can be threshold-filtered.
- **`counter reset = corrected array state is reverted` — rejected.** Diagnostic state and repaired payload embodiment are separate relations.
- **`MR16–MR20 survive device power removal` — not established.** This slice does not claim cross-power telemetry durability.
- **`Linux ECS ABI = every DDR5 device's exact MR encoding` — rejected.** Linux is a later standardized host abstraction over supported hardware/control paths.
- **`threshold-hidden = physically nonexistent` — rejected.** Visibility policy is not a physical non-occurrence proof.
- **`ECS telemetry predicts remaining device lifetime` — not established.** No reliability-prognosis model is grounded here.
- **`this closes JESD79-5 revision chronology` — rejected.** Direct normative revision-by-revision audit remains open.
- **`Micron invented ECS / memory scrubbing / ECC telemetry` — rejected.** No priority claim is made.
- **`all DDR5 vendors implement identical telemetry semantics` — rejected.** Cross-vendor product audit remains open.

## Evidence maturity consequence

Case 45 remains **`grounded`**. The new evidence does not change its maturity label; it sharpens what the existing phrase `correction telemetry` is allowed to mean.

The case can now safely distinguish:

```text
corrective array work
    !=
counted diagnostic event
    !=
threshold-visible diagnostic event
    !=
latest retained report
    !=
complete maintenance history
```

and:

```text
reported value
    + count mode
    + threshold/reporting configuration
    + reset/reporting epoch
        -> interpretable diagnostic evidence
```

## Related-repository duplication check

`tmzncty/computing-archaeology` was re-searched for `DDR5 ECS` before this deepening. No dedicated ECS technical-history study was found. Broad JEDEC revision history, DDR5 controller adoption, on-die-ECC genealogy, and vendor implementation history therefore remain work for the companion repository if developed. This evidence file keeps only the retention-specific telemetry-validity relation.

## Sources

### Manufacturer-primary content, distributor-mirror custody

- Micron Technology, *DDR5 SDRAM Product Core Data Sheet*, `CCM005-1684161373-23`, Rev. D 10/2022, `ECC Transparency and Error Scrub`, public Arrow mirror: <https://static6.arrow.com/aropdfconversion/fc2b144ccf061160504edd742d01cb58fdda91bb/ddr5_sdram_core.pdf>.

### Later authoritative software/control documentation

- Linux Kernel documentation, *Scrub Control*, written for Linux 6.15: <https://docs.kernel.org/6.15/edac/scrub.html>.
- Linux Kernel documentation, current *Scrub Control*: <https://docs.kernel.org/edac/scrub.html>.
- Linux Kernel documentation, testing ABI entries for `sysfs-edac-ecs` (`mode`, `reset`, `threshold`): <https://docs.kernel.org/admin-guide/abi-testing.html>.
