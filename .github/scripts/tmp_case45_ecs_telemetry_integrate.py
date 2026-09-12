from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text.rstrip() + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"missing anchor: {label}")
    if text.count(old) != 1:
        raise SystemExit(f"non-unique anchor ({text.count(old)}): {label}")
    return text.replace(old, new, 1)


evidence_path = Path("evidence/45-micron-ddr5-2022-2026-ecs-telemetry-validity-deepening.md")
if evidence_path.exists():
    raise SystemExit(f"refusing to overwrite existing {evidence_path}")

evidence = r'''# Case 45 deepening — Micron DDR5 ECS telemetry validity, filtering, reset, and reporting horizon (2022–2026)

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
'''
evidence_path.write_text(evidence.rstrip() + "\n", encoding="utf-8")

# Update Case 45 navigation and bounded interpretation.
case_path = "cases/45-micron-ddr5-on-die-ecc-ecs.md"
case = read(case_path)
nav_anchor = "Grounding record: [`../evidence/45-micron-ddr5-2021-2026-odecc-ecs-grounding.md`](../evidence/45-micron-ddr5-2021-2026-odecc-ecs-grounding.md).\n"
nav_replacement = nav_anchor + "\nTelemetry-validity deepening: [`../evidence/45-micron-ddr5-2022-2026-ecs-telemetry-validity-deepening.md`](../evidence/45-micron-ddr5-2022-2026-ecs-telemetry-validity-deepening.md).\n"
case = replace_once(case, nav_anchor, nav_replacement, "Case 45 grounding navigation")

case_section = r'''
## ECS telemetry validity: count mode, thresholding, reset, and reporting epochs

The 2022 Micron DDR5 product-core document makes the earlier phrase `correction telemetry` more precise. ECS exposes an `Error Counter (EC)` and an `Errors per Row Counter (EpRC)`, but their values are not a universal lifetime error ledger.

The EC can count either rows containing at least one detected code-word error or detected code-word errors themselves, depending on the configured count mode. Both EC and EpRC reporting are threshold-conditioned, and EpRC retains a maximum-error-row relation rather than a row-by-row traversal history. Consequently:

> **same counter value != same proposition without count-mode context**

and:

> **thresholded absence of a report != proof that no correctable error occurred**.

Micron also documents an explicit ECS counter reset. Device RESET or the ECS reset control reinitializes counters/address state and resets the reporting registers; while the manual ECS reset control remains asserted, further ECS operations do not continue. The reset therefore belongs to the maintenance-control state machine rather than being only an observer-side log deletion.

This yields another key boundary:

> **telemetry reset != repair rollback**.

Corrected array data already written by earlier scrub work and the later diagnostic summary about that work are separate retained relations.

The product document further says ECS mode/threshold/count selections should not be changed after the first ECS operation without a following RESET / ECS RESET COUNTERS boundary. The project calls the resulting interval a **reporting/configuration epoch**. This is engineering reconstruction, not Micron vocabulary. It means that a retained count is interpretable only together with the measurement definition under which it accumulated.

At the reporting boundary, the Micron interface retains the most recently produced error/max-row summary until a later report replaces it or reset clears it. That makes the state a latest/epoch-bounded diagnostic summary rather than an append-only archive:

> **latest ECS summary != event-by-event history != lifetime error history**.

The later Linux EDAC/CXL ECS control surface independently preserves the same semantic distinctions at a host-policy layer: `mode` selects row versus code-word counting, `threshold` can mask counts below the selected threshold, and `reset` explicitly resets the ECS counter. Linux is used only as a later authority/control boundary; its sysfs values are not projected backward as every Micron DDR5 mode-register encoding.

This deepening also adds an evidence-validity prerequisite. Micron instructs that all array bits be written before ECS to avoid false failures. Therefore **ECS capability != already-valid diagnostic evidence over uninitialized protected state**.

Cross-case comparison is intentionally functional. Case 15's Intel SSD 320 unsafe-shutdown attribute is a cumulative lifetime event count; DDR5 ECS report state is resettable, mode-relative, threshold-filtered, and latest/epoch-bounded. Case 55's NVMe PEL is a bounded typed event log; ECS telemetry is not an event log simply because it survives beyond one corrective operation. [`SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md) now records this as a distinct maintenance-control-state horizon.

No cross-power persistence claim follows. The inspected evidence does not establish that MR16–MR20 survive removal of device power, nor does it close JESD79-5 revision chronology, cross-vendor identity, or hardware fault-validation questions.

Deepening record: [`../evidence/45-micron-ddr5-2022-2026-ecs-telemetry-validity-deepening.md`](../evidence/45-micron-ddr5-2022-2026-ecs-telemetry-validity-deepening.md).
'''
case = replace_once(case, "\n## Maintenance and labor\n", "\n" + case_section.strip() + "\n\n## Maintenance and labor\n", "Case 45 maintenance section")
write(case_path, case)

# Add bounded roadmap item while preserving the broad DRAM item as open.
roadmap_path = "ROADMAP.md"
roadmap = read(roadmap_path)
roadmap_anchor = "## Phase 2 — Build missing technical bridges\n\n"
roadmap_item = r'''- [x] **Case 45 DDR5 ECS telemetry-validity deepening:** [`cases/45-micron-ddr5-on-die-ecc-ecs.md`](cases/45-micron-ddr5-on-die-ecc-ecs.md) + [`evidence/45-micron-ddr5-2022-2026-ecs-telemetry-validity-deepening.md`](evidence/45-micron-ddr5-2022-2026-ecs-telemetry-validity-deepening.md) use Micron's Rev. D 10/2022 product-core ECS contract plus the later official Linux EDAC/CXL control surface to separate corrective array work from the diagnostic summary it produces. EC row/code-word modes, threshold filtering, maximum-error-row reporting, explicit reset, reset-gated ECS execution, and configuration/reset validity boundaries close `same counter value != same metric without mode context`, `thresholded absence != no correctable error`, `telemetry reset != repair rollback`, and `latest ECS summary != event log != lifetime history`. The slice adds ECS to the maintenance-control-state persistence-horizon synthesis as a resettable, filtered, mode-relative latest summary; cross-power register persistence, direct JESD79-5 revision chronology, cross-vendor identity, and hardware fault validation remain open, with broad ECC/ECS genealogy routed to `computing-archaeology`.

'''
roadmap = replace_once(roadmap, roadmap_anchor, roadmap_anchor + roadmap_item, "ROADMAP Phase 2 anchor")
write(roadmap_path, roadmap)

# Append CASE_INDEX findings. This index is a chronological finding ledger, so appending is intentional.
index_path = "CASE_INDEX.md"
index = read(index_path).rstrip()
if "## Case 45 — DDR5 ECS telemetry-validity deepening findings" in index:
    raise SystemExit("Case 45 telemetry findings already exist")
index_append = r'''

## Case 45 — DDR5 ECS telemetry-validity deepening findings

Deepening record: [`evidence/45-micron-ddr5-2022-2026-ecs-telemetry-validity-deepening.md`](evidence/45-micron-ddr5-2022-2026-ecs-telemetry-validity-deepening.md).

- **3572 — Micron ECS maintains EC and EpRC rather than one undifferentiated error count:** the Rev. D 10/2022 product-core record names an Error Counter plus an Errors per Row Counter. (`H/P`)
- **3573 — EC meaning is mode-relative:** row mode counts rows with at least one detected code-word error while code-word mode counts detected code-word errors, so an equal numeric value does not imply an equal measured proposition. (`H/P, E`)
- **3574 — ECS reporting is threshold-conditioned:** Micron subjects EC and EpRC reporting/count semantics to threshold filters; later Linux CXL ECS control independently exposes a threshold that masks sub-threshold counts. (`H/P`)
- **3575 — EpRC is a maximum-row summary:** it retains the row with the largest code-word error count plus that row's address rather than preserving a row-by-row event ledger. (`H/P, E`)
- **3576 — RESET/ECS reset reinitializes diagnostic and traversal state:** Micron documents counter reset plus internal ECS-address-counter initialization, and ECS RESET COUNTERS resets MR16–MR20. (`H/P`)
- **3577 — ECS reset is not merely passive log deletion:** while the manual reset control remains asserted, additional ECS operations do not proceed; it must be released before ECS resumes. (`H/P, E`)
- **3578 — telemetry reset != repair rollback:** clearing diagnostic/control state does not imply reversal of corrected codewords already written back by previous ECS work. (`E`)
- **3579 — ECS configuration has a reset-bounded validity relation:** Micron says automatic-in-self-refresh, threshold, manual/automatic, and row/code-word selections should not change after the first ECS operation without RESET/ECS RESET COUNTERS; `reporting/configuration epoch` is the project's name for this evidence boundary. (`H/P, E`)
- **3580 — retained count without configuration context is not self-interpreting:** count mode and threshold are part of the proposition required to interpret a later numeric summary. (`E`)
- **3581 — ECS result state is latest-summary state rather than append-only history:** the reporting relation retains the most recently produced summary until later replacement or reset, so `latest report != chronological event log != lifetime history`. (`H/P, E`)
- **3582 — zero/report absence is not an all-history negative proof:** explicit reset and threshold filtering block the inference `zero/hidden counter = no correctable error has ever occurred`. (`E`)
- **3583 — Linux exposes later host authority over ECS evidence semantics:** official EDAC/CXL ECS controls expose row/code-word mode, threshold, and reset where supported, while remaining a later abstraction rather than proof of identical bare-DDR5 encodings. (`H/P, E, X`)
- **3584 — corrective work and retained evidence are separate:** ECS read/correct/writeback can alter the array while the diagnostic summary is independently filtered, replaced, or reset. (`E`)
- **3585 — initialized protected state is an evidence prerequisite:** Micron requires array bits to be written before ECS to avoid false failures, so feature availability does not by itself make telemetry semantically valid over uninitialized state. (`H/P, E`)
- **3586 — lifetime event count != resettable scrub summary:** Intel SSD 320 SMART C0h and DDR5 ECS telemetry are only functionally analogous second-order evidence; the former is a documented cumulative lifetime event count while the latter is mode-relative, filtered, resettable, and latest/epoch-bounded. (`A, E`)
- **3587 — no power-cycle, universality, or priority upgrade:** this slice does not establish MR16–MR20 survival across power removal, one-to-one Linux/CXL-to-vendor MR encoding, complete JESD79-5 revision chronology, identical cross-vendor behavior, invention priority, or hardware fault-validation results. (`X`, rejected upgrade)
'''
write(index_path, index + index_append)

# Extend Synthesis 26 with a sixth maintenance-control-state horizon.
synth_path = "docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md"
synth = read(synth_path)
witness_anchor = "The historical claims remain in those case/evidence records. The categories below are **engineering reconstruction**, not source vocabulary unless a source independently uses the same words."
witness_add = "- [`Case 45 — DDR5 on-die ECC / ECS`](../cases/45-micron-ddr5-on-die-ecc-ecs.md), especially [`evidence/45-micron-ddr5-2022-2026-ecs-telemetry-validity-deepening.md`](../evidence/45-micron-ddr5-2022-2026-ecs-telemetry-validity-deepening.md): a latest scrub diagnostic summary can be mode-relative, threshold-filtered, explicitly resettable, and interpretable only within a reporting/configuration epoch.\n\n"
synth = replace_once(synth, witness_anchor, witness_add + witness_anchor, "Synthesis 26 witness list")
synth = synth.replace("The five witnesses immediately reject that shortcut:", "The six witnesses immediately reject that shortcut:", 1)
verdict_anchor = "SSD unsafe-shutdown counter\n    -> cumulative event-history summary\n    -> persists as telemetry, not as a durability verdict\n"
verdict_replacement = verdict_anchor + "\nDDR5 ECS report state\n    -> mode-relative + threshold-filtered latest maintenance summary\n    -> explicitly resettable; not a lifetime event ledger\n"
synth = replace_once(synth, verdict_anchor, verdict_replacement, "Synthesis 26 verdict block")

synth_section = r'''
## 9A. Resettable, threshold-filtered diagnostic summary — Case 45

DDR5 ECS adds a persistence horizon not represented by the first five witnesses. Micron's 2022 product-core record exposes a correction summary whose interpretation depends on count mode and threshold, whose maximum-row component compresses many visited rows into one retained diagnostic relation, and whose counters/report registers can be explicitly reset.

The later Linux CXL ECS control surface independently exposes row/code-word count mode, reporting threshold, and counter reset as host-visible policy where supported.

This means that the retained state is neither a lifetime event count nor an append-only event log:

```text
ECS corrective work
    -> may repair array state

reporting mode + threshold
    -> define what later count means / what becomes visible

latest report registers
    -> retain bounded diagnostic summary

reset / later reporting boundary
    -> retire or replace that summary
```

Therefore:

> **summary persistence != repair persistence**

> **latest diagnostic state != complete maintenance history**

> **telemetry reset != rollback of earlier corrective work**.

This also sharpens the comparison with Case 15. A cumulative lifetime unsafe-shutdown count and a resettable ECS summary can both be long enough-lived to inform later diagnosis while having different history semantics. `counter` is therefore not a sufficient persistence-horizon category.

The project term `reporting/configuration epoch` is used only to describe the validity interval over which a count mode/threshold and its accumulated summary can be interpreted together. It is not Micron or JEDEC historical vocabulary, and this synthesis does not claim the reporting registers survive power removal.

---
'''
synth = replace_once(synth, "## 10. Persistence horizon ≠ authority\n", synth_section + "\n## 10. Persistence horizon ≠ authority\n", "Synthesis 26 section 10")
synth = synth.replace("The five cases show that persistence duration and decision authority are independent axes.", "The six cases show that persistence duration and decision authority are independent axes.", 1)
authority_anchor = "- A lifetime SMART count can persist for diagnosis without selecting payload currentness.\n"
authority_replacement = authority_anchor + "- A resettable ECS summary can persist beyond one corrective operation while remaining filtered, mode-relative diagnostic evidence rather than a complete repair history.\n"
synth = replace_once(synth, authority_anchor, authority_replacement, "Synthesis 26 authority bullets")
source_anchor = "- Intel SSD 320 September/March 2011 manufacturer documents through Case 15 evidence.\n"
source_replacement = source_anchor + "- Micron DDR5 SDRAM Product Core Data Sheet Rev. D 10/2022 plus official Linux EDAC/CXL ECS documentation through the Case 45 deepening evidence.\n"
synth = replace_once(synth, source_anchor, source_replacement, "Synthesis 26 sources")
write(synth_path, synth)

# Remove the one-shot integration scaffolding so the final research commit contains canonical files only.
Path(".github/scripts/tmp_case45_ecs_telemetry_integrate.py").unlink(missing_ok=True)
Path(".github/workflows/tmp-case45-ecs-telemetry-integrate.yml").unlink(missing_ok=True)
