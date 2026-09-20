# Case 85 Evidence Deepening — ONFI Feature-State Reset Semantics and EZ NAND Automatic Retry, 2006–2011

**Status:** `bounded deepening complete`

**Parent case:** [`../cases/85-toshiba-nand-shift-read-retry-recoverability.md`](../cases/85-toshiba-nand-shift-read-retry-recoverability.md)

## Research question

Case 85 already establishes a reader-side recoverability regime in which changing NAND read thresholds can move a page from default-read failure back inside the ECC-correctable region without first rewriting the payload. Existing deepenings also establish that vendor read-retry capability/calibration state, the currently selected retry mode, reset class, and power-cycle lifetime are different state classes.

This slice asks a narrower standards question:

> What did ONFI standardize about feature-state persistence and automatic retry, and what did it deliberately leave vendor-specific?

The point is not to write a general history of ONFI. It is to determine whether the existence of `SET FEATURES`, reset commands, and a standardized EZ NAND automatic-retry control licenses stronger claims about raw-NAND read-retry parameter formats or reset behavior than the vendor evidence actually supports.

The bounded answer is:

> **ONFI made feature state explicitly feature-scoped and reset-class-sensitive, and ONFI 2.3 standardized a higher-level EZ NAND control over automatic retry. It did not thereby standardize Micron feature address `89h`, one cross-vendor raw-NAND retry table, one threshold-search algorithm, or one universal reset lifetime for vendor-specific retry state.**

This sharpens Case 85's existing rule:

```text
standardized retry policy/control surface
    !=
standardized retry parameter representation
    !=
standardized internal retry algorithm
    !=
standardized vendor-specific reset lifetime
```

---

## Scope and source custody

### Primary standards inspected

This slice uses official ONFI-hosted specifications:

1. **Open NAND Flash Interface Specification, Revision 1.0, 28 December 2006**
   - official ONFI PDF: <https://onfi.org/files/onfi_1_0_gold.pdf>
   - relevant material: `Set Features`, `Get Features`, feature-address table, Timing Mode feature.

2. **Open NAND Flash Interface Specification, Revision 2.0, 27 February 2008**
   - official ONFI PDF: <https://onfi.org/files/onfi_2_0_gold.pdf>
   - relevant material: Reset definition, Synchronous Reset, feature-address table, Timing Mode and I/O Drive Strength feature persistence.

3. **Open NAND Flash Interface Specification, Revision 2.3 family / archived 2.3a gold PDF**
   - official ONFI PDF: <https://onfi.org/files/onfi_2_3a_gold.pdf>
   - relevant material: EZ NAND support field, feature address `50h` EZ NAND control, `Retry Disable (RD)`, automatic retry semantics, timing consequence.

4. **Open NAND Flash Interface Specification, Revision 3.0, 9 March 2011**
   - official ONFI PDF: <https://onfi.org/files/onfi_3_0_gold.pdf>
   - relevant material: continued EZ NAND automatic-retry capability and `Reset LUN (FAh)` as a reset scope distinct from whole-target reset.

### Contemporary implementation/industry context

5. **SanDisk, “EZ NAND F2F,” Flash Memory Summit, 19 August 2010**
   - conference proceedings PDF: <https://files.futurememorystorage.com/proceedings/2010/20100819_S201_Lassa.pdf>
   - used only as a contemporary vendor presentation showing how the ONFI 2.3 EZ NAND retry control was explained operationally: local retry after ECC failure, default automatic retry, host-disable capability, and read-latency consequences.

The ONFI specifications are the normative primary anchors. The SanDisk deck is a contemporary vendor/industry witness, not a substitute for the standard and not proof that every shipping EZ NAND implementation used one identical internal retry mechanism.

### Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `ONFI Set Features Reset read retry 89h` found no dedicated overlapping packet. Broad ONFI interface history, JEDEC/Toggle-mode rivalry, command genealogy, and vendor implementation history still belong there if pursued. This file keeps only the retention/recoverability seam.

---

## Historical record

### H/P — ONFI 1.0 already makes feature state a first-class interface object

ONFI 1.0 defines `Set Features` and `Get Features`. Its feature-address table reserves:

- `01h` for Timing Mode;
- `02h–7Fh` as reserved in that revision;
- **`80h–FFh` as vendor specific**.

The important retention point is not merely that a configuration command exists. `Get Features` returns the **current settings/parameters** associated with a feature address, while `Set Features` changes them.

So by the first ONFI revision, the interface already distinguishes:

```text
array payload
    !=
current device feature state
```

That does not make all feature state nonvolatile. It establishes a separately addressable control-state class whose lifetime is defined by the relevant feature and event semantics.

**Primary anchor:** ONFI 1.0, section 5.20 and surrounding Set/Get Features material.

### H/P — ONFI 1.0 places later Micron `89h` inside a vendor-specific address range

Feature addresses `80h–FFh` are explicitly vendor specific in ONFI 1.0. Address `89h` lies inside that range.

This matters for Case 85 because Micron's later raw-NAND read-retry interface uses feature address `89h`. ONFI's existence therefore does **not** make `89h` a cross-vendor read-retry standard.

The safe statement is:

```text
ONFI standardizes Set/Get Features framing
    + reserves a vendor-specific address space

Micron later assigns read-retry meaning to 89h
```

The unsafe shortcut is:

```text
Micron uses ONFI Set Features
    -> ONFI standardized Micron's retry parameter format
```

Nothing in the inspected ONFI material licenses that conclusion.

### H/P — ONFI 1.0 explicitly lets one standardized feature survive Reset

For Timing Mode, ONFI 1.0 states that the timing-mode settings are retained across Reset commands.

This is a useful early counterexample to treating `RESET` as an undifferentiated erasure of every runtime control state.

The historical claim must remain feature-specific:

> ONFI 1.0 specifies reset survival for Timing Mode.

It does **not** say every standard or vendor-specific feature survives every reset.

### H/P — ONFI 2.0 makes the general Reset description explicitly subordinate to per-feature exceptions

ONFI 2.0 describes `Reset (FFh)` as putting the target in its default power-up state and, in that revision's interface model, placing it in the asynchronous data interface. The same Reset section immediately warns that **some feature settings are retained across Reset commands**, with the relevant behavior specified in the feature-definition section.

This creates an important standards-level boundary:

```text
whole-command label: Reset
    !=
one universal state-retirement rule for every feature
```

The default-power-up wording therefore cannot be read in isolation as proof that every feature register returns to its power-on default.

**Primary anchor:** ONFI 2.0, section 5.3 `Reset Definition`.

### H/P — ONFI 2.0 gives two different reset lifetimes inside its own standardized feature set

ONFI 2.0's Timing Mode feature separates the data-interface selection from other timing-mode settings:

- the **Data Interface** setting is not retained across `Reset (FFh)`; after reset the interface returns to asynchronous;
- other timing-mode settings are retained across `Reset (FFh)` and `Synchronous Reset (FCh)`.

The I/O Drive Strength feature is also retained across `FFh` and `FCh` in the inspected revision.

Thus one standard already contains both:

```text
feature substate retired by FFh
```

and

```text
feature substate retained across FFh/FCh
```

This is direct historical evidence for Case 85's broader engineering rule that **reset lifetime must be attached to a named state class, not inferred from the word `reset` alone**.

It still says nothing specific about later Micron `89h` behavior, because `89h` remains vendor-specific.

### H/P — ONFI 2.3 standardizes an EZ NAND automatic-retry control surface

The ONFI 2.3 family adds EZ NAND. Its parameter page includes an `EZ NAND support` field. Bit 0 states whether the target supports host control over automatic retries through `Set Features`.

The standard distinguishes two cases:

1. if the capability bit is set, the host may explicitly enable or disable automatic retries;
2. if the bit is clear, the EZ NAND controller itself determines whether to perform retry without host intervention.

This is a standards-level allocation of **retry control authority**.

It does not expose the internal threshold table, voltage offsets, retry ordering, ECC implementation, or a per-vendor calibration representation.

### H/P — feature address `50h` controls EZ NAND retry admission, not retry-voltage content

ONFI 2.3's `EZ NAND control` feature uses feature address `50h`. Its `Retry Disable (RD)` bit has the following bounded semantics:

- `RD = 0`: the EZ NAND device may automatically perform retries during error conditions at its discretion;
- `RD = 1`: the EZ NAND device shall not automatically perform retries;
- automatic retry may make actual page-read time exceed the typical `tR`;
- if automatic retry is disabled, the device may exceed the specified UBER;
- host disable is only allowed when the parameter page says the capability is supported.

The retention-specific consequence is that ONFI standardized a policy/admission knob over a hidden recovery mechanism:

```text
retry allowed / disabled
    !=
retry threshold selected
    !=
retry calibration table
    !=
retry search algorithm
```

This is the key standards boundary added by this deepening.

**Primary anchor:** ONFI 2.3a, section 5.26.3 `EZ NAND control`, feature address `50h`.

### H/P — the parameter page itself carries capability evidence about retry authority

ONFI 2.3's `EZ NAND support` field is not merely descriptive marketing text. It is machine-readable capability state exposed through the parameter page.

For automatic retries, the capability bit tells the host whether it is authorized to override device discretion through `Set Features`.

This yields three distinct state/authority classes:

```text
capability advertised by parameter page
    !=
current Retry Disable policy
    !=
internal retry attempt / parameters used for one read
```

The host can therefore know that a control path exists without knowing the internal retry state that an EZ NAND controller will choose.

### H/P — ONFI 2.3 explicitly allows retry work to surface as read-latency expansion

When an EZ NAND controller performs an automatic retry, the specification warns that the typical page read time `tR` may be exceeded.

This means retry can be externally visible indirectly through **time**, even if the internal threshold-search trajectory is not externally represented.

Safe bounded relation:

```text
nominal read request
    + internal recovery work
    -> completion may take longer than typical tR
```

Unsafe inference:

```text
longer-than-typical read
    -> proof that retry happened
```

Other causes can affect latency; the standard only permits retry to extend the typical read time.

### H/P — disabling retry changes the error contract without proving media mutation

ONFI 2.3 warns that disabling automatic retries may allow the device to exceed the specified UBER.

This is especially useful for technical-retention because the physical array does not need to change for the externally observed error outcome to worsen. Changing whether the device is allowed to perform recovery work can change whether the device meets the interface's error-rate contract.

Therefore:

```text
same physical NAND state
    + retry admitted
    !=
same physical NAND state
    + retry disabled
```

at the level of observable recoverability/error behavior.

This is not evidence that retry repairs the cells. The standard describes retry as read-side work.

### H/S — SanDisk's August 2010 FMS material explains EZ NAND as local retry after ECC failure

A SanDisk presentation dated **19 August 2010** describes EZ NAND as offloading technology-dependent work into the NAND module and explicitly lists `Read Retry` among the offloaded capabilities.

Its retry slide describes:

- local read retry after ECC failure;
- automatic retry as the default EZ NAND behavior;
- host disable through the `0x50` EZ NAND Control feature when supported;
- typical-versus-maximum read-time planning because recovery work can extend a read.

This is a valuable contemporaneous explanation of the same control surface found in the ONFI 2.3 specification.

It is **not** promoted above the standard and does not prove what thresholds, voltages, ECC algorithms, or search order a particular shipping implementation used.

### H/P — ONFI 3.0 continues the automatic-retry capability and adds another reset scope

ONFI 3.0 retains the EZ NAND support field and its automatic-retry capability semantics. It also defines `Reset LUN (FAh)` as a command aimed at one addressed LUN and states that the command does not affect the target's data-interface configuration.

The standard recommends Reset LUN for cancelling ongoing command operations at one LUN, while whole-target `FFh/FCh` is reserved for broader target problems such as a hang condition.

This adds another direct standards example that reset scope is not one-dimensional:

```text
Reset one LUN
    !=
Reset whole target
    !=
Synchronous Reset
    !=
power cycle
```

Again, this does not establish later Micron `Hard Reset (FDh)` semantics. The command class and vendor evidence must remain named.

---

## Engineering reconstruction

### E — standards can expose recovery authority without exposing recovery interpretation state

ONFI 2.3 lets a host know whether it can disable automatic retries and lets it set the `RD` policy bit when allowed.

But the standard does not require that the host receive the internal read-reference values used for those retries.

Thus:

```text
host-visible recovery policy
    !=
host-visible recovery calibration
```

A protocol can standardize **who may decide whether recovery work runs** while leaving **how the recovery work interprets the medium** inside the device.

### E — retry capability ≠ retry policy ≠ retry execution

The EZ NAND parameter-page bit says whether explicit host enable/disable control is supported.

The feature-50h `RD` bit says whether automatic retries are currently disabled.

Neither one proves that a retry is executing on a particular read.

Therefore:

```text
capability present
    !=
policy permits retry
    !=
retry needed
    !=
retry attempted
    !=
retry succeeds
```

This is the read-recovery counterpart to the repository's maintenance-observability rule that feature existence, admission, execution, coverage, and closure are separate claims.

### E — standardized control address ≠ standardized hidden state machine

Feature `50h` standardizes a control point for EZ NAND. That does not make all internal retry paths interoperable in the stronger sense of exposing one threshold table or one algorithm.

A host may interact portably with `RD` while two compliant devices use different hidden recovery strategies.

### E — vendor-specific address allocation is retained namespace, not standardized semantics

ONFI's `80h–FFh` vendor-specific range is itself a standardized namespace rule. But the meaning of a specific address inside that range comes from the vendor contract.

So:

```text
address space standardized
    !=
address meaning standardized
```

This is why Micron `89h` must remain a Micron-source claim even though it travels through the ONFI `Set Features` mechanism.

### E — `Reset` is an event class whose effects are state-specific

The inspected standards repeatedly force a relational formulation:

```text
state S
    survives / does not survive
    event E
```

rather than:

```text
device is reset
    -> everything is reset
```

ONFI 2.0 alone contains feature substates with different `FFh` behavior. ONFI 3.0 adds per-LUN versus target reset scope. The later Micron evidence already in Case 85 adds still another vendor-specific `FDh` boundary.

### E — power-on default ≠ universal post-reset state

A feature may have a power-on default while still being specified to survive a reset command. ONFI's standardized feature behavior demonstrates that these are different lifecycle events.

Therefore:

```text
power cycle
    !=
FFh
    !=
FCh
    !=
FAh
```

unless a specific feature contract explicitly equates them.

### E — automatic recovery can be a hidden part of one nominal read

EZ NAND allows the device/controller to retry internally when an error condition occurs. From the host's viewpoint, this can remain one read operation whose latency expands.

This establishes a bounded layering distinction:

```text
one host-visible read
    !=
one physical sense attempt
```

That does not mean every ONFI read uses retry or that a host can reconstruct the internal attempt count from latency alone.

### E — turning recovery off can move the recoverability frontier without changing the payload

Case 85 uses `recoverability frontier` as project reconstruction vocabulary. ONFI 2.3 supplies a clean control-policy example: if the host disables automatic retry, the device may fail the specified UBER that it could meet when recovery work is admitted.

No payload rewrite is required for that frontier to move.

This strengthens the parent case's relation:

```text
recoverability
    = function(
        physical media state,
        reader/recovery policy,
        available interpretation machinery,
        ECC capability,
        interface contract
      )
```

without claiming ONFI itself uses that formula or terminology.

---

## Controlled functional comparisons

### A — Micron feature `89h` versus ONFI EZ NAND feature `50h`

The two are functionally adjacent because both influence read-recovery behavior through `Set Features`.

They are not the same interface:

- ONFI `50h` in the EZ NAND model controls whether automatic retries may run;
- Micron `89h` selects vendor-defined read-retry options/settings in the product evidence already grounded by Case 85;
- `50h` does not establish one cross-vendor threshold table;
- `89h` remains inside ONFI's vendor-specific address range.

No genealogy is inferred.

### A — Case 38 current/saved feature state

[`../cases/38-intel-s3700-power-loss-imminent-capacitor-self-test.md`](../cases/38-intel-s3700-power-loss-imminent-capacitor-self-test.md) distinguishes current feature state, saved state, and event-specific persistence at an SSD interface.

Case 85's ONFI layer supplies a raw-NAND counterpart:

```text
feature currently set
    !=
feature survives reset
    !=
feature survives power loss
```

The command sets and devices are unrelated; this is only a persistence-horizon comparison.

### A — Synthesis 26 maintenance-control-state persistence horizons

[`../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md) separates maintenance-control state by role, authority, reconstitution path, and persistence horizon.

EZ NAND retry control fits the same analytical discipline even though read retry is a recovery/interpretation path rather than periodic maintenance:

- capability evidence;
- current admission policy;
- hidden runtime work;
- event-specific state lifetime.

No claim is made that read retry is refresh or scrub.

### A — Synthesis 29 maintenance observability

[`../docs/SYNTHESIS_29_MAINTENANCE_OBSERVABILITY_COVERAGE_ACCOUNTING.md`](../docs/SYNTHESIS_29_MAINTENANCE_OBSERVABILITY_COVERAGE_ACCOUNTING.md) warns that policy, admission, execution, and closure are different observable claims.

The EZ NAND standard provides a recovery-side analogue:

```text
retry-control capability exposed
    !=
retry currently enabled
    !=
retry executed for this read
    !=
retry succeeded
```

This is a functional comparison of state-observability shape only.

---

## Philosophical interpretation — bounded

This slice supports one limited proposition about technical retention:

> A recovery relation can be standardized at the level of **authority and policy** without making the internal interpretation procedure public or uniform.

ONFI 2.3 allows the host to know whether automatic retry can be disabled and to control that permission when supported. Yet the internal decision thresholds and retry search can remain device-local.

This means technical legibility has layers:

- the host may know that a recovery capability exists;
- it may know whether it is currently permitted;
- it may observe a read eventually succeed or fail;
- it may still not possess the internal interpretive state that produced the result.

A second bounded proposition concerns reset:

> `Reset` is not a metaphysical return of a device to one total origin state. It is a command whose retirement effects are specified over particular state classes.

That proposition is grounded here in standards text, not used as a free-floating analogy.

The slice does **not** establish that standards hide information for philosophical reasons, that all device-local state is inaccessible, or that opaque recovery is inherently undesirable.

---

## Prior-art and chronology boundary

### Safe claims

- By **28 December 2006**, ONFI 1.0 standardized `Set Features` / `Get Features`, reserved feature addresses `80h–FFh` as vendor specific, and explicitly specified reset retention for Timing Mode state.
- By **27 February 2008**, ONFI 2.0 explicitly stated that some feature settings survive Reset and provided different reset lifetimes for different standardized feature substates.
- In the **ONFI 2.3** generation publicly presented in August 2010, EZ NAND included a standardized machine-readable capability for host control of automatic retry and feature address `50h` with `Retry Disable` semantics.
- A SanDisk Flash Memory Summit presentation dated **19 August 2010** contemporaneously described EZ NAND local read retry after ECC failure and the same `0x50` retry-disable control.
- ONFI 3.0, dated **9 March 2011**, continued the EZ NAND retry-capability semantics and separately defined `Reset LUN (FAh)`.
- These standards are sufficient to show that **feature-state lifetime and retry authority were already explicit interface concerns** before the 2014 Linux Micron read-retry patch and 2015 Micron L83A datasheet used elsewhere in Case 85.

### Chronology that must not be overread

- Toshiba's bounded patent family has Japanese priority **2009-11-06**. ONFI 2.3's August-2010 public standard/presentation therefore must **not** be described as proven prior art that caused Toshiba's 2009 design.
- ONFI 1.0/2.0 predate that Toshiba priority, but the inspected material does not standardize the later EZ NAND automatic-retry mechanism there.
- ONFI 2.3's existence does not prove that Micron's later `89h` design descends from EZ NAND feature `50h`.
- Similar use of `Set Features` is not enough to establish a design genealogy.

---

## Explicit non-claims

This deepening does **not** claim that:

1. ONFI invented NAND read retry.
2. ONFI 2.3 is the first device to perform read retry.
3. EZ NAND automatic retry necessarily changes read-reference voltages.
4. Every EZ NAND automatic retry uses the same internal algorithm.
5. Every EZ NAND implementation exposes host disable control.
6. Feature address `50h` and Micron feature address `89h` are aliases.
7. ONFI standardizes Micron's `89h` subfeature values.
8. ONFI standardizes one cross-vendor raw-NAND retry table.
9. ONFI standardizes one cross-vendor retry-voltage step sequence.
10. The vendor-specific address range makes vendor meanings interoperable.
11. `Set Features` settings are necessarily nonvolatile.
12. Every feature survives `FFh`.
13. Every feature is cleared by `FFh`.
14. Every feature that survives `FFh` also survives power loss.
15. `FFh`, `FCh`, `FAh`, and later vendor `FDh` are equivalent reset events.
16. ONFI 1.0 Timing Mode persistence proves Micron `89h` persistence.
17. ONFI 2.0's default-power-up wording overrides its explicit feature-retention exceptions.
18. Reset LUN affects every target-wide state class.
19. Automatic retry success implies payload rewrite or refresh.
20. Automatic retry renews the NAND threshold distribution.
21. Automatic retry clears P/E wear.
22. Disabling automatic retry physically damages NAND.
23. Disabling automatic retry guarantees an uncorrectable read.
24. A read exceeding typical `tR` proves that retry occurred.
25. A read within typical `tR` proves that retry did not occur.
26. Host visibility of `RD` reveals the internal retry count.
27. Host visibility of retry capability reveals retry thresholds.
28. The SanDisk FMS deck is a universal implementation specification.
29. The SanDisk presentation proves all ONFI 2.3 devices shipped the described behavior.
30. ONFI 2.3 caused Toshiba's 2009-priority patent design.
31. ONFI 2.3 caused Micron's later `89h` implementation.
32. Similar `Set Features` framing proves vendor genealogy.
33. EZ NAND automatic retry is identical to Case 36 Correct-and-Refresh.
34. EZ NAND automatic retry is equivalent to reclaim, copyback, scrub, or garbage collection.
35. A standardized control surface means the internal recovery mechanism is standardized.
36. A capability bit is proof that a retry occurred on any particular read.

---

## Claim ledger

| Claim | Type | Source class | Evidence strength | Boundary |
| --- | --- | --- | --- | --- |
| ONFI 1.0 defines Set/Get Features and vendor-specific feature range `80h–FFh` | Historical record | ONFI official specification | H/P | says nothing about later vendor-specific meanings |
| ONFI 1.0 Timing Mode settings survive Reset | Historical record | ONFI official specification | H/P | feature-specific, not universal |
| ONFI 2.0 Reset has explicit feature-state exceptions | Historical record | ONFI official specification | H/P | does not define `89h` |
| ONFI 2.0 standardized feature substates have different `FFh/FCh` lifetimes | Historical record | ONFI official specification | H/P | no power-cycle inference |
| ONFI 2.3 EZ NAND exposes automatic-retry-control capability | Historical record | ONFI official specification | H/P | capability != execution |
| ONFI 2.3 feature `50h` RD controls automatic retry admission | Historical record | ONFI official specification | H/P | policy != retry parameters |
| disabling retry may allow specified UBER to be exceeded | Historical record | ONFI official specification | H/P | not a claim of guaranteed data loss |
| automatic retry may exceed typical `tR` | Historical record | ONFI official specification | H/P | latency is not proof of retry |
| SanDisk 2010 presents local retry after ECC failure for EZ NAND | Historical record | contemporary vendor conference deck | H/S | implementation/context witness, not universal conformance proof |
| ONFI 3.0 distinguishes Reset LUN from target reset | Historical record | ONFI official specification | H/P | distinct from later vendor FDh |
| standardized retry authority != standardized retry calibration | Engineering reconstruction | synthesis from primary sources | E | project analytical relation |
| reset effects are state-class × event-class relations | Engineering reconstruction | synthesis from ONFI feature semantics | E | not ONFI vocabulary |
| feature address namespace standardization != feature meaning standardization | Engineering reconstruction | synthesis from ONFI vendor range + Micron case | E | no genealogy claim |
| ONFI `50h` and Micron `89h` are functionally adjacent but not identical | Functional analogy/comparison | ONFI + parent-case vendor sources | A | no common implementation implied |

---

## What this changes in Case 85

Before this slice, Case 85 already safely said:

- retry state can be vendor-specific;
- Micron `89h` is not a universal ONFI retry format;
- selected retry state can have a shorter lifetime than NAND payload;
- reset class must be named.

This slice adds a standards-level reason those claims should remain separated:

```text
ONFI 1.0/2.0:
feature lifetime is explicitly feature-specific across Reset

ONFI 2.3:
retry admission/control can be standardized for EZ NAND
without exposing a standardized raw-NAND retry parameter table

ONFI 3.0:
reset scope itself can be LUN-specific rather than target-wide
```

So the stronger bounded conclusion is:

> **The existence of a standardized recovery control plane does not imply a standardized recovery interpretation state, and the existence of a standardized Reset command does not imply one universal feature-state retirement rule.**

### Parent-case maturity

**No maturity promotion is warranted.** Case 85 remains `grounded`.

The slice deepens standards context and closes one ambiguity — `ONFI standardized nothing about retry` would be too broad because ONFI 2.3 EZ NAND does standardize automatic-retry control. But the exact Micron L83A `89h` behavior across `RESET (FFh)` remains open because ONFI explicitly leaves `89h` in vendor-specific space and per-feature reset semantics cannot be inferred from unrelated standardized features.

---

## Remaining debt

The following remain legitimate future slices rather than gaps to fill by inference:

1. **Exact 2015 Micron L83A `89h` behavior across `FFh`.** The 2015 datasheet establishes lifetime until feature rewrite or power-down but the inspected evidence still does not directly close ordinary `FFh` semantics for that exact family.
2. **ONFI 2.3 normative publication archaeology.** The official archived 2.3a PDF is authoritative for mechanism; if exact ballot/publication chronology of 2.3 versus 2.3a matters later, inspect dated ONFI release records rather than relying on later summaries.
3. **Shipping EZ NAND implementation evidence.** A named device/manual/conformance trace would be needed before claiming a particular product used the standardized automatic-retry path.
4. **Internal EZ NAND retry mechanism.** The standard deliberately does not prove which threshold-search or ECC strategy a device used.
5. **Vendor comparison.** Samsung/Toggle, Toshiba/Kioxia, Hynix, and later Micron raw-NAND retry command/parameter genealogies remain broad technical-history work for `computing-archaeology` unless a retention-specific seam requires them.
6. **Fault-injection / timing observation.** Independent experiments would be needed to connect `tR` expansion to concrete retry sequences on a named implementation.

---

## Sources

### Primary / normative

- Open NAND Flash Interface Working Group, **Open NAND Flash Interface Specification, Revision 1.0**, 28 December 2006: <https://onfi.org/files/onfi_1_0_gold.pdf>.
- Open NAND Flash Interface Working Group, **Open NAND Flash Interface Specification, Revision 2.0**, 27 February 2008: <https://onfi.org/files/onfi_2_0_gold.pdf>.
- Open NAND Flash Interface Working Group, **Open NAND Flash Interface Specification, Revision 2.3 family / 2.3a gold archive**: <https://onfi.org/files/onfi_2_3a_gold.pdf>.
- Open NAND Flash Interface Working Group, **Open NAND Flash Interface Specification, Revision 3.0**, 9 March 2011: <https://onfi.org/files/onfi_3_0_gold.pdf>.

### Contemporary industry context

- SanDisk, **“EZ NAND F2F,”** Flash Memory Summit, 19 August 2010: <https://files.futurememorystorage.com/proceedings/2010/20100819_S201_Lassa.pdf>.

### Parent-case sources retained as context, not re-grounded here

- Micron Technology, **32Gb, Asynchronous/Synchronous NAND**, Rev. A 5/15, `L83A_32Gb_Async_Sync_NAND_mlc_plus.pdf`.
- Linux upstream commit `8429bb3975ef81c114cde4da111e64d224d19f83`, **“mtd: nand: support Micron READ RETRY,”** 2014-01-14.
- Micron Technology patent family, **“Read retry scratch space,”** priority 2018-01-12, US20200371876A1 / US11586498B2.

---

## Bounded conclusion

ONFI's standards history supplies a useful correction to two opposite overstatements.

The first overstatement is:

> `ONFI did not standardize retry at all.`

That is too broad. ONFI 2.3's EZ NAND model standardizes automatic-retry capability reporting and a `Retry Disable` control at feature address `50h`.

The second overstatement is:

> `Because ONFI standardized retry control, raw-NAND read-retry settings such as Micron 89h are standardized too.`

That is also wrong. ONFI places `89h` inside vendor-specific feature space, while EZ NAND `50h` controls whether automatic recovery may run without exposing one common threshold table or algorithm.

The resulting retention boundary is:

```text
standardized capability evidence
    !=
current recovery-admission policy
    !=
hidden retry execution
    !=
internal retry calibration / interpretation state
    !=
physical NAND payload
```

And the reset boundary is:

```text
feature state S
    × named event E
    -> specified survival / retirement relation
```

not:

```text
RESET
    -> all state returns to one universal origin
```

That is the bounded contribution of this deepening.