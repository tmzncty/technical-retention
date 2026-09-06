# Micron 64Mb SDRAM: AUTO REFRESH, SELF REFRESH, and Refresh-Responsibility Handoff

## Status

**`grounded`** — bounded primarily to the refresh command/mode semantics documented for Micron's 64Mb x4/x8/x16 SDR SDRAM family in the November 1999 (`Rev. 11/99`) manufacturer datasheet, with a later Infineon XMC4700/XMC4800 external-memory-controller witness (2016) used only to deepen the system-side distinction among self-refresh request, observed transition completion, power-down admission, and access readiness.

Grounding record: [`../evidence/21-micron-1999-sdram-refresh-mode-grounding.md`](../evidence/21-micron-1999-sdram-refresh-mode-grounding.md).

## Scope

This case asks a narrow question left open by Cases 09 and 10:

> What changes when the same SDRAM exposes both an externally repeated refresh command and a self-refresh mode that temporarily internalizes recurring refresh work?

The bounded object is Micron's 64Mb `MT48LC16M4A2`, `MT48LC8M8A2`, and `MT48LC4M16A2` family as documented in `64MSDRAM.p65 – Rev. 11/99`.

This is **not** a general history of SDRAM, a JEDEC standards history, or an invention-priority claim for self refresh. It does not infer that every SDR SDRAM used exactly the same internal circuit. The historical record is the Micron command/interface behavior and the internal blocks the manufacturer actually documented.

## Relation to Cases 03, 09, and 10

The earlier DRAM cases separate three layers:

```text
Case 03: why dynamic state requires periodic restoration
Case 09: where the next refresh-row address comes from
Case 10: where an autonomous refresh trigger/schedule can come from
```

The Micron SDRAM adds an interface-level transition between two maintenance regimes in one named product family:

```text
normal operation
    external controller repeatedly issues AUTO REFRESH
    internal refresh controller/counter supplies refresh addressing

SELF REFRESH mode
    host enters the mode with the refresh command encoding while CKE is LOW
    device supplies its own internal clocking and recurring refresh cycles

exit
    external clock must be stable
    CKE returns HIGH
    NOPs are required through tXSR while internal refresh may finish
    external AUTO REFRESH cadence resumes
```

The refresh obligation remains. What changes is **who must generate the recurring maintenance events and which interface state makes that responsibility active**.

## Historical vocabulary and record

Micron's November 1999 datasheet uses the period terms `AUTO REFRESH`, `SELF REFRESH`, `CKE`, `internal refresh controller`, `row refresh counter`, `tREF`, and `tXSR`.

The functional block diagrams for the x4, x8, and x16 organizations show `CKE`, `CLK`, command/control logic, a `REFRESH COUNTER`, a row-address multiplexer, row-address latch/decoder, sense amplifiers, and the memory array.

For normal operation, the datasheet says `AUTO REFRESH` is analogous to CBR refresh in conventional DRAMs. It calls the command **nonpersistent**: it must be issued each time refresh is required. Refresh addressing is generated internally, making external address bits irrelevant during the command. The bounded 64Mb parts require 4,096 refresh cycles per 64 ms, and Micron describes either distributed commands or a burst of refresh commands as valid ways to satisfy that requirement.

For `SELF REFRESH`, Micron says the device can retain data even if the rest of the system is powered down and that external clocking is not required while the mode is active. Entry uses the same command encoding as `AUTO REFRESH` with `CKE` LOW. After entry, all other inputs become `Don't Care` while CKE must remain LOW; the SDRAM supplies internal clocking and performs its own refresh cycles.

Exit is not instantaneous ordinary service. The external clock must first be stable; CKE is then returned HIGH; and NOP commands are required for `tXSR` because an internal refresh may still be in progress. After exit, externally issued `AUTO REFRESH` commands must resume at the required cadence. Micron explicitly notes that `SELF REFRESH` and `AUTO REFRESH` use the same row refresh counter.

## Later system/controller witness — Infineon XMC4700/XMC4800 EBU (2016)

Infineon's _XMC4700 / XMC4800 XMC4000 Family Reference Manual_, V1.3 (2016-07), adds a later controller-side composition that the 1999 Micron device document does not expose.[^infineon-ebu]

In §14.12.18 (printed p. 14-82), software requests self-refresh entry by writing `SELFREN`. The EBU then precharges the banks and issues the self-refresh command to the attached SDRAM devices. A separate read-only `SELFRENST` bit reports the status of that operation; the manual states that power-down may be entered safely when the command has completed. Exit is similarly split: software writes `SELFREX`, the controller raises CKE, and read-only `SELFREXST` reports completion before SDRAM access resumes. The same section also describes an optional post-exit auto-refresh step and a programmable `SELFREX_DLY` NOP interval before later access.[^infineon-ebu]

The register description on printed pp. 14-120–14-122 makes the request/status separation explicit: `SELFREN` and `SELFREX` are writable command controls, while `SELFRENST` and `SELFREXST` are read-only status fields. A later official Infineon XMCLib API preserves this distinction in software-facing form through entry/exit-status enums and `XMC_EBU_SdramGetRefreshStatus()`.[^infineon-xmclib]

This is **not** evidence that the XMC controller was paired with the 1999 Micron part, that Micron used Infineon's internal logic, or that the 2016 register model defines the 1999 historical meaning of `SELF REFRESH`. It is a later primary system witness for a separate layer: the controller must decide when the device transition is sufficiently complete to admit a surrounding power-state change or ordinary access.

## Retained state and control state

The payload remains volatile dynamic-memory state. The documented refresh counter is maintenance-control state: it helps determine which row receives the next refresh operation. The interface also has a mode/control relation defined by CKE and the command sequence.

The project should not turn these into one undifferentiated `memory state`. At least three things differ:

1. **payload state** — the data represented by dynamic cells;
2. **maintenance-enumeration state** — the row refresh counter/control path;
3. **maintenance-authority state** — whether recurring refresh requests must arrive from outside or are generated under self-refresh mode inside the device.

`Maintenance authority` is project reconstruction vocabulary, not Micron's historical term.

## Engineering reconstruction

### Refresh obligation is not recurring command-generation responsibility

The dynamic-cell retention requirement does not disappear when self refresh is entered. Instead, the repeated maintenance events change source.

In normal operation, `AUTO REFRESH` is explicitly nonpersistent: external control must issue a new command each time refresh is required, although the chip internally chooses the refresh row. In self refresh, one mode-entry transition allows the chip to supply its own clocking and repeated refresh cycles until the mode is exited.

Therefore:

> **refresh obligation ≠ recurring command-generation responsibility**.

### Internal row addressing is not autonomous recurrence

Case 09 already showed a bounded CBR regime in which an on-chip counter supplied refresh rows while cadence remained external. Micron's normal `AUTO REFRESH` mode independently reproduces this separation at an SDRAM command interface: addresses are internal, but the command must recur externally.

Only the separate self-refresh mode moves recurring refresh generation inside the device.

### Maintenance responsibility can be transferred and transferred back

The important transition is reversible.

External control normally bears the obligation to issue refresh commands on time. `SELF REFRESH` entry transfers repeated scheduling/clocking to the SDRAM. Exit returns the device to a regime in which external refresh commands again have to arrive at the specified interval.

This is a bounded example of **mode-mediated maintenance-responsibility handoff**. That phrase is engineering reconstruction, not period vocabulary.

### Retention availability is not ordinary service availability

Micron says that after self-refresh entry the other inputs become `Don't Care` except CKE. The device is preserving data, but it is not simultaneously accepting ordinary read/write command traffic as though nothing changed.

This gives a useful retention distinction:

> **retention availability ≠ ordinary service availability**.

A state may be actively preserved through a low-power retention mode while normal access is deliberately suspended.

### Exit timing is part of the service-restoration relation

`tXSR` exists because internal refresh may still be in progress when self-refresh exit begins. The host must restore a stable clock, raise CKE, and wait through the required NOP interval before treating normal command service as resumed.

The payload can therefore remain retained while the interface is temporarily not yet ready for ordinary access. Retention and service recovery have different timing conditions.

### Command request, observed transition completion, and system admission are separate

The Micron device contract already separates mode entry/exit from ordinary service timing. The later Infineon controller makes a further system-level distinction visible:

```text
software requests entry
    !=
controller observes/records entry-command completion
    !=
system admits power-down

software requests exit
    !=
controller observes/records exit-command completion
    !=
post-exit delay/refresh work completes
    !=
ordinary SDRAM access is admitted
```

This is a bounded engineering reconstruction from two historical interfaces separated by seventeen years. It does not assert a direct genealogy between the products.

The status bits are also not physical proof that every DRAM cell is healthy. They are controller-level evidence that the documented command transition has been issued/completed sufficiently for the next system action under that controller's contract. Therefore:

> **transition-completion evidence ≠ direct measurement of payload retention margin**.

And:

> **retention-mode admission ≠ power-down/access admission**.

A small amount of non-payload control state can thus gate whether a much larger dynamic-memory payload is treated as safely maintainable across a system power-state transition.

### Self refresh is not nonvolatility

The phrase `retain data ... even if the rest of the system is powered down` must not be shortened to `the SDRAM retains data without power`. The datasheet says the device supplies its **own internal clocking** and refresh cycles. The bounded claim is independence from **external clocking** and much of the surrounding system while the SDRAM itself remains in its powered self-refresh regime.

Therefore:

> **self-refresh autonomy ≠ intrinsic nonvolatility**.

## Failure boundaries

The interface decomposition exposes distinct failure classes without assigning unsourced product failure rates:

- during normal operation, external control can fail to issue enough `AUTO REFRESH` commands within the required refresh interval;
- the internal refresh controller/counter can be a separate locus from external command generation;
- an incorrect self-refresh entry sequence can fail to establish the intended retention mode;
- premature exit/service resumption can violate the documented `tXSR` recovery interval;
- correct self-refresh command semantics still do not imply survival of device power loss;
- successful payload retention does not imply ordinary read/write availability while self refresh is active.

These are mechanism-level boundaries derived from the documented control partition, not measured Micron field-failure statistics.

The later controller witness adds two failure boundaries without inventing measured failure rates:

- software can request self-refresh entry yet violate the controller's documented sequencing if surrounding power-down is admitted before the entry transition is complete;
- software can request self-refresh exit yet resume SDRAM access before exit status and the configured post-exit delay/refresh sequence permit access.

Neither condition is automatically identical to immediate payload loss. It means the system has crossed outside the documented transition/admission contract; the actual physical outcome still depends on device timing, refresh continuity, power, and workload.

## Prior art and anti-anachronism

This case makes **no claim that Micron invented self refresh or SDRAM refresh commands**.

Case 10 already grounds a Toshiba patent with 1984 priority that places autonomous refresh scheduling, an oscillator, and a refresh-address counter on-chip; that patent itself cites still-earlier Hitachi automatic refresh-frequency work. The historical contribution of Case 21 is therefore not an invention story. It is a manufacturer-primary, named-product-family account of a late-1990s SDRAM interface in which recurring refresh responsibility is explicitly different in normal `AUTO REFRESH` and `SELF REFRESH` operation.

Likewise, the Micron datasheet is not silently promoted into a complete JEDEC standard history. Terms such as `responsibility handoff`, `maintenance authority`, `retention availability`, and `service availability` are modern analytical labels used to compare mechanisms. Period claims remain in Micron's own vocabulary.

The 2016 Infineon controller is used only as a **later system-composition witness**. It is not projected backward as Micron's 1999 internal implementation, not treated as a JEDEC normative chronology, and not used to infer a direct Micron→Infineon lineage. Its value here is relational: a system controller can retain explicit transition status and delay policy around an SDRAM self-refresh mode whose recurring maintenance work is performed inside the memory device.

## Functional analogy and philosophical limit

A modern operating-system analogy might compare self refresh to handing a maintenance task from one scheduler to another, but that analogy is only functional. The actual historical mechanism is a hardware command/mode relation involving CKE, internal clocking, the refresh controller/counter, and explicit exit timing.

A bounded conceptual lesson follows: persistence can depend not only on *whether* maintenance occurs but on a controlled transfer of who is responsible for causing it. That does not establish a general philosophy in which every retained state has an `owner`, nor does it imply that Micron engineers described self refresh philosophically.

## Cross-case result

The DRAM refresh-control decomposition can now be written more precisely:

```text
payload decay / retention deadline
    !=
row restoration mechanism
    !=
refresh-row enumeration
    !=
recurring maintenance-event generation
    !=
mode/authority controlling where recurrence occurs
    !=
ordinary service availability
    !=
exit/recovery timing
```

Cases 03, 09, and 10 established the first distinctions across different historical designs. Case 21 adds a named SDRAM family in which **one device crosses between external recurring-command responsibility and internal recurring self-refresh work, then crosses back on exit**.

Case 104 now continues this decomposition for a later Micron LPDDR family by separating **self-refresh maintenance rate** (temperature-compensated internal cadence) from **self-refresh maintenance coverage** (PASR-selected array regions). That continuation is functional and source-bounded; it does not establish a direct product genealogy.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Micron's Rev. 11/99 64Mb SDRAM uses an internal refresh counter/control path | H/P | manufacturer datasheet block diagrams and command text |
| Normal `AUTO REFRESH` is nonpersistent and must be issued each time refresh is needed | H/P | Micron Rev. 11/99 p. 13 |
| `AUTO REFRESH` uses internally generated refresh addressing | H/P | Micron Rev. 11/99 pp. 11, 13 |
| `SELF REFRESH` entry uses the refresh command with CKE LOW and then supplies internal clocking/refresh cycles | H/P | Micron Rev. 11/99 pp. 11, 13 |
| Exit requires stable CLK, CKE HIGH, and a `tXSR` NOP interval before normal operation resumes | H/P | Micron Rev. 11/99 p. 13 |
| External `AUTO REFRESH` cadence resumes after self-refresh exit | H/P | Micron Rev. 11/99 p. 13 |
| Refresh responsibility can be transferred across the device boundary and later transferred back | E | bounded reconstruction from the two documented modes |
| Infineon XMC4700/XMC4800 EBU exposes separate writable self-refresh entry/exit controls and read-only entry/exit status | H/P | 2016 Infineon reference manual §14.12.18 and SDRMREF register description |
| Infineon gates safe power-down/access on completion of the corresponding self-refresh transition | H/P | 2016 Infineon reference manual printed p. 14-82 |
| Self-refresh request, transition-completion evidence, and system admission are separate retention-control relations | E | bounded reconstruction from Micron 1999 + Infineon 2016; no direct genealogy claim |
| Controller transition status proves every DRAM cell has sufficient physical retention margin | X | status is command/controller evidence, not a direct cell-retention measurement |
| Retained data in self refresh remain ordinarily serviceable without exiting the mode | X | contradicted by input/CKE and exit semantics |
| Self refresh makes the SDRAM nonvolatile or independent of device power | X | datasheet describes internal clocking/refresh, not unpowered retention |
| Micron invented self refresh or these semantics define the complete JEDEC history | X | outside source scope and blocked by earlier primary evidence |

## Related repositories

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for SDRAM self-refresh / `AUTO REFRESH` / `CKE` did not find a dedicated case. The broader engineering history of SDRAM generations, JEDEC evolution, controller design, per-bank refresh, and later retention-aware policies belongs there if developed comprehensively. This repository retains only the bounded retention-responsibility comparison.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the anti-anachronism guard: later concepts such as `maintenance ownership`, DDR refresh taxonomy, per-bank refresh, or modern retention-aware control must not be projected backward into this 1999 datasheet without separate period evidence.

## Sources

1. Micron Technology, Inc., _64Mb: x4, x8, x16 SDRAM_, `64MSDRAM.p65 – Rev. 11/99`, November 1999, especially printed pp. 1, 4–6, 11, and 13. Preserved manufacturer-datasheet transcription: <https://pdf.elecfans.com/MICRON/MT48LC4M16A2.html>.
2. Micron Technology, current SDRAM obsolete-part catalog, confirming the `MT48LC4M16A2` 64Mb x16 family identity and manufacturer provenance: <https://www.micron.com/products/obsolete/obsolete-sdram/part-catalog>.
3. For earlier self-refresh prior-art control rather than Micron product semantics: Takayasu Sakurai and Tetsuya Iizuka, Toshiba Corp., US4682306A, _Self-refresh control circuit for dynamic semiconductor memory device_, Japanese priority 20 August 1984: <https://patents.google.com/patent/US4682306A/en>.
4. [^infineon-ebu]: Infineon Technologies AG, _XMC4700 / XMC4800 XMC4000 Family Reference Manual_, EBU V1.6, manual V1.3, 2016-07, especially §14.12.18 printed p. 14-82 and SDRMREF register description pp. 14-120–14-122: <https://www.infineon.com/assets/row/public/documents/30/44/infineon-referencemanual-xmc4700-xmc4800-um-en.pdf>.
5. [^infineon-xmclib]: Infineon Technologies AG, XMCLib EBU driver, official `Infineon/mtb-xmclib-cat3` repository, `XMC_EBU_SdramGetRefreshStatus` and self-refresh entry/exit status enums: <https://github.com/Infineon/mtb-xmclib-cat3/blob/c24888699c6c5cfd6e5475be90d9703e43540d04/XMCLib/inc/xmc_ebu.h>.
