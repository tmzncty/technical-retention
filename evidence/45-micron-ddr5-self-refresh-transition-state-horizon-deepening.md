# Case 45 deepening — DDR5 ECS self-refresh continuity, PASR coverage, and transition-specific maintenance-state horizons

## Status

**Deepening evidence for grounded Case 45.**

Case: [`../cases/45-micron-ddr5-on-die-ecc-ecs.md`](../cases/45-micron-ddr5-on-die-ecc-ecs.md).

Cross-case comparison: [`../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md).

This slice closes a bounded transition-semantics debt left by the earlier ECS telemetry deepening: what happens to different pieces of DDR5 maintenance-control state when the device enters and exits self refresh, and can a diagnostic summary remain physically present while its coverage meaning becomes invalid?

It does **not** claim power-loss persistence of ECS registers, a complete JESD79-5 revision history, universal cross-vendor identity, or measured fault tolerance.

## Bounded question

The previous deepening established that Micron DDR5 ECS reporting is mode-relative, threshold-filtered, latest-summary state whose counters can be reset. It left the persistence horizon of that state deliberately open.

The narrower question here is:

> Across a documented self-refresh transition, which maintenance-control relations continue, which are reinitialized, and when can a surviving ECS summary cease to be valid evidence for the same full-array population?

The manufacturer record supports three distinct answers inside one DRAM generation:

```text
ECS transparency counters/registers
    -> survive ordinary self-refresh entry/exit

same-bank-refresh bank counter
    -> resets on self-refresh entry/exit

PASR changes the population under maintenance
    -> ECS state may survive physically
    -> but full-array transparency can become semantically invalid
    -> known-data reinitialization + ECS counter reset are required before treating the next full-array scrub as accurate
```

That is a retention-specific distinction among **state survival**, **maintenance phase**, and **evidence validity**.

## Evidence custody and source roles

### E1 — Micron DDR5 SDRAM Product Core Data Sheet, Rev. D 10/2022

**Source:** Micron Technology, *DDR5 SDRAM Product Core Data Sheet*, document identifier `CCM005-1684161373-23`, Rev. D 10/2022. Relevant sections include `Self Refresh Entry and Exit`, `ECC Transparency and Error Scrub`, the average periodic ECS interval discussion, and `ECS Operation with PASR Support`.

Public manufacturer-document mirror used in the repository:

<https://static6.arrow.com/aropdfconversion/fc2b144ccf061160504edd742d01cb58fdda91bb/ddr5_sdram_core.pdf>

This is Micron-authored primary product content with distributor-mirror custody. The mirror preserves the document identifier, revision, and page numbering, but it is not represented here as an origin-hosted archival facsimile.

### E2 — Micron DDR5 SDRAM Product Core Data Sheet, Rev. E 11/2024 continuity witness

A later public mirror of the same Micron core document family identifies Rev. E 11/2024 and retains the PASR/ECS boundary while noting that PASR support is deprecated and applies only to devices that support the feature:

<https://www.avnet.com/wcm/connect/dacdfea7-999f-4ee0-b514-6f9e0bf68c6d/ddr5-sdram-core.pdf?MOD=AJPERES>

This is used as a later continuity witness, not to back-project every 2024 clause into every 2022 device.

### E3 — SK hynix DDR5 product documents, bounded independent-vendor witness

Public mirrors of SK hynix DDR5 product documents independently expose the same broad ECS control vocabulary: automatic ECS in self refresh, RESET / `MR14 OP[6]` counter initialization, `MR16–MR20` reset, and product text stating that self-refresh entry/exit does not reset ECS transparency counters/registers.

Representative public mirrors inspected for this slice include:

- SK hynix 16Gb A-die Rev. 1.1: <https://uttc.com.tw/wp-content/uploads/2025/12/Consumer_CP16GD5_H5CG448%EF%BC%866AGBDJXxxx_Rev.1.1_1anm.pdf>;
- SK hynix H5CG4(8&6)MEBDX Rev. 1.1 family mirror: <https://atta.szlcsc.com/upload/public/pdf/source/20260310/8FC2DFFF69AECDAC2CA42897896E303D.pdf>.

These are manufacturer-authored product documents obtained through third-party mirrors. They are used only as a bounded independent product-family corroboration. They do not establish a complete cross-vendor conformance matrix or normative JEDEC identity.

## Historical record

### 1. Ordinary self-refresh entry/exit does not clear Micron ECS transparency state

Micron's Rev. D ECS section states directly that entering and exiting self refresh does **not** reset the ECS transparency counters/registers. The same paragraph says that, in Automatic ECS mode, the device must continue to perform ECS work in self refresh so that the average periodic ECS requirement can be met; the internal scrub rate can vary because operation must synchronize to the internal oscillator.

The document separately allows the maximum-spacing interval used for later REFab or another self-refresh entry to restart when self refresh exits.

Historical record:

```text
self-refresh transition
    -> ECS transparency counters/registers remain
    -> ECS scheduling interval may begin a new post-exit interval
```

This is already enough to reject a one-bit model in which `self-refresh exit` means `all maintenance state reset`.

### 2. The same self-refresh transition resets same-bank-refresh enumeration state

Micron's `Self Refresh Entry and Exit` discussion gives a different rule for Same Bank Refresh (`REFsb`). Entering and exiting self refresh resets the internal bank counter used by the REFsb coverage relation.

Micron therefore recommends that every bank receive REFsb before entering self refresh. If that condition is not met, the post-exit contract requires an extra REFab or an extra REFsb to each bank, in addition to the normal post-self-refresh requirements.

Historical record:

```text
REFsb bank-coverage phase
    -> reset across self-refresh entry/exit

unfinished pre-entry bank coverage
    -> cannot simply be inferred from the old phase after exit
    -> compensating refresh work is prescribed
```

The ECS transparency state and REFsb bank phase thus have different disclosed transition lifetimes inside the same product documentation.

### 3. ECS interval state and ECS diagnostic state are not one state

Micron allows the interval timing for the maximum spacing between REFab commands or another self-refresh entry to restart upon self-refresh exit, while explicitly preserving the transparency counters/registers.

That gives a manufacturer-level separation between:

- the time/schedule relation governing when enough automatic ECS opportunity must be supplied; and
- the diagnostic/result state produced by ECS work.

The word `epoch` below is project reconstruction, not Micron vocabulary:

> a scheduling interval can restart without clearing the diagnostic reporting epoch.

### 4. PASR can preserve the counter bits while invalidating their full-array meaning

Micron's PASR/ECS section makes the strongest evidence-validity boundary in this slice.

When PASR masks segments during self refresh:

- masked segments are not guaranteed to retain their data;
- automatic ECS still scrubs unmasked segments when enabled;
- the DRAM is not required to run ECS on masked segments;
- ECS transparency may not produce accurate results if any mask bit is set;
- after self-refresh exit, masked segments must be initialized with known data and ECS counters reset if accurate ECS data is required for the next scrub through the full array.

Therefore the physical continuation of a counter/register value is not sufficient to preserve the proposition that the value summarizes one continuous full-array measurement population.

Historical record:

```text
counter/register state may remain
    +
coverage domain changes under PASR
    -> old full-array interpretation no longer warranted
```

### 5. Explicit RESET / ECS RESET COUNTERS remains a different boundary

The earlier Case 45 telemetry deepening already grounds that device RESET or `MR14:OP[6]=1` initializes ECS counters/address state and resets MR16–MR20. Holding the manual ECS reset control also prevents further ECS operation until the bit is returned to zero.

The new self-refresh evidence sharpens that contrast:

```text
ordinary self-refresh entry/exit
    != ECS reset

self-refresh transition
    -> preserve ECS transparency counters/registers

RESET / ECS RESET COUNTERS
    -> reinitialize ECS reporting/control state
```

A transition can therefore preserve one maintenance record without making that record indefinitely authoritative.

### 6. Independent SK hynix product documentation supports the bounded product-level pattern

The inspected SK hynix product documentation independently states that ECS counters/internal ECS address counters are initialized by RESET or manual ECS reset, that `MR16–MR20` are reset by ECS RESET COUNTERS, and that automatic ECS can operate during self refresh. A separate product-family excerpt states that entering and exiting self refresh does not reset ECS transparency counters/registers.

This supports a cautious cross-vendor observation:

> more than one public DDR5 vendor product document exhibits a distinction between ordinary self-refresh transition and explicit ECS-reset authority.

It does **not** prove that every vendor, density, revision, or JEDEC revision has byte-for-byte identical behavior.

## Engineering reconstruction

### 1. Same transition does not imply same persistence horizon for every maintenance-control state

The key relation is internal to one device-generation contract:

```text
self-refresh entry/exit
    -> ECS transparency state survives
    -> REFsb bank phase resets
```

Therefore:

> **same device transition != same persistence horizon for every maintenance-control state**.

`volatile` versus `persistent` is too coarse even before leaving one DRAM package. The relevant question is always: persistent **across which transition, for which relation, and for what later decision?**

### 2. State survival is not evidence validity

PASR is the counterexample that prevents the new finding from becoming another naive persistence claim.

If masked segments are omitted from refresh/ECS coverage, the existing ECS transparency state may still survive self refresh, yet Micron warns that transparency may be inaccurate and requires reinitialization/reset before the next accurate full-array scrub.

Therefore:

> **retained diagnostic bits != retained diagnostic validity**

and:

> **report continuity != measurement-population continuity**.

The evidence's semantic scope can fail before the storage holding the evidence is cleared.

### 3. Maintenance-phase reset is not payload forgetting

Resetting the REFsb bank counter changes the enumeration state used to cover banks after the transition. It does not itself mean that payload bits were cleared, nor that ECS diagnostic state was erased.

The post-exit extra-refresh rule is important because it supplies the safe continuation relation: losing the old bank phase creates additional coverage work, not automatically a demonstrated retention failure.

Thus:

> **maintenance-coverage phase reset != payload reset != diagnostic-summary reset**.

### 4. Self-refresh continuity is not cross-power nonvolatility

The source establishes continuity across **self-refresh mode entry/exit**. That is a powered DRAM retention mode, not evidence that MR16–MR20 survive removal of device power.

The repository therefore keeps the earlier stop condition:

> **self-refresh-persistent != power-loss-persistent**.

A later cross-power claim would require a source or fault test that actually crosses the power-removal boundary.

### 5. Schedule state and history state must be separated

The post-exit ECS interval may restart even though error transparency state remains. This is another counterexample to using `maintenance state` as one bucket.

At least four relations are visible here:

1. payload state maintained by refresh;
2. REFsb bank-enumeration phase;
3. ECS scheduling/interval relation;
4. ECS diagnostic/report state.

They need not share a reset boundary.

## Functional comparisons

### Case 09 — CBR refresh counter

Case 09 already shows a maintenance counter whose phase can be reinitialized without preserving a history of prior refresh operations. Case 45 now adds a product-generation counterexample inside DDR5: one transition can reset refresh-enumeration state while leaving ECS diagnostic state intact.

The comparison is functional only:

> both cases show that maintenance phase and maintenance history are different relations; no TI→DDR5 genealogy is asserted.

### Case 21 — SDRAM self-refresh responsibility handoff

Case 21 grounds self refresh as a mode in which refresh responsibility moves inside the DRAM while ordinary service is suspended. Case 45 does not repeat that history. It adds a later DDR5-specific question: which auxiliary maintenance states survive the mode transition and which require reconstitution afterward?

Thus:

> **maintenance-authority handoff != uniform preservation of all maintenance-control state**.

### Synthesis 26 — persistence horizons

This slice strengthens the synthesis without adding a seventh technology family. The same Case 45 now demonstrates **transition-relative differentiation**:

- ECS diagnostic summary: preserved across ordinary self-refresh entry/exit;
- ECS schedule interval: may restart after exit;
- REFsb bank phase: reset by entry/exit;
- full-array ECS evidence validity: can be broken by PASR coverage changes even while register values remain.

The comparison rule becomes:

> **classify the transition as carefully as the state: one interruption boundary can preserve, reset, restart, or invalidate different supporting relations.**

## Philosophical interpretation — bounded

The exact technical fact is modest but conceptually useful: a technical trace can remain present while losing the conditions that made it valid evidence about a larger population.

The narrow interpretation is:

> persistence of an inscription and persistence of its evidential relation are separable technical problems.

This is not a claim that DRAM has an archive in the historical or human sense. The mechanism is mode-register state, refresh/ECS coverage, reset rules, and a changing measurement population.

## Rejected upgrades / stop conditions

- **`ECS transparency survives self refresh = ECS telemetry is nonvolatile` — rejected.** The source crosses a self-refresh transition, not device power removal.
- **`self-refresh exit resets all DRAM maintenance state` — rejected.** Micron explicitly preserves ECS transparency counters/registers while resetting the REFsb bank counter.
- **`surviving counter value = valid full-array summary` — rejected.** PASR can change the covered population and make ECS transparency inaccurate.
- **`REFsb bank-counter reset = payload loss` — rejected.** The documented response is compensating refresh coverage; physical loss is not established by the counter reset itself.
- **`ECS interval restart = error counter reset` — rejected.** Micron documents these as distinct behaviors.
- **`Micron + SK hynix product similarity = universal JEDEC identity` — rejected.** A direct normative revision-by-revision audit remains open.
- **`product-document behavior = measured silicon behavior under every fault` — rejected.** Independent fault/power-transition validation remains open.
- **`PASR-masked segment not guaranteed = deterministic immediate loss` — rejected.** Loss is possible outside the retained-data guarantee; the document does not specify deterministic failure time.

## Evidence maturity consequence

Case 45 remains **`grounded`**. The contribution is a narrower persistence-horizon result rather than a maturity promotion.

The case can now safely distinguish:

```text
state survives transition
    !=
state keeps the same semantic coverage
    !=
maintenance schedule continues from the same phase
    !=
full-array diagnostic evidence remains valid
```

and:

```text
self-refresh entry/exit
    -> preserve ECS transparency state
    -> reset REFsb bank phase
    -> may restart ECS interval timing
    -> PASR may invalidate full-array ECS interpretation
```

## Related-repository duplication check

`tmzncty/computing-archaeology` was searched for both `DDR5 ECS` and `DDR5 self refresh` before this slice. No dedicated technical-history treatment was found. Broad DDR5/JEDEC evolution, vendor implementation genealogy, and circuit-level self-refresh/ECS design should therefore remain companion-repository work if developed. This file keeps only the retention-specific transition-horizon and evidence-validity relation.

## Sources

### Manufacturer-primary content, distributor-mirror custody

- Micron Technology, *DDR5 SDRAM Product Core Data Sheet*, `CCM005-1684161373-23`, Rev. D 10/2022, public Arrow mirror: <https://static6.arrow.com/aropdfconversion/fc2b144ccf061160504edd742d01cb58fdda91bb/ddr5_sdram_core.pdf>.
- Micron Technology, *DDR5 SDRAM Product Core Data Sheet*, later Rev. E 11/2024 continuity witness, public Avnet mirror: <https://www.avnet.com/wcm/connect/dacdfea7-999f-4ee0-b514-6f9e0bf68c6d/ddr5-sdram-core.pdf?MOD=AJPERES>.

### Independent vendor-product witnesses, third-party mirror custody

- SK hynix, 16Gb DDR5 A-die Rev. 1.1 product document, public UTTC mirror: <https://uttc.com.tw/wp-content/uploads/2025/12/Consumer_CP16GD5_H5CG448%EF%BC%866AGBDJXxxx_Rev.1.1_1anm.pdf>.
- SK hynix, H5CG4(8&6)MEBDX Rev. 1.1 product-family document, public LCSC mirror: <https://atta.szlcsc.com/upload/public/pdf/source/20260310/8FC2DFFF69AECDAC2CA42897896E303D.pdf>.
