# Micron Mobile DDR Automatic TCSR: On-Die Temperature Sensing, Self-Refresh Cadence, and Selective Retention

## Status

**`grounded`** — bounded to Micron's 512Mb Mobile DDR SDRAM documentation, especially the Rev. J 2/08 product datasheet, with Micron Technical Note TN-46-12 (Rev. A 10/05) used for terminology and implementation-locus context.

Grounding record: [`../evidence/35-micron-2005-2008-mobile-ddr-tcsr-grounding.md`](../evidence/35-micron-2005-2008-mobile-ddr-tcsr-grounding.md).

## Scope

This case asks a narrow question left open by Cases 21 and 34:

> What changes when temperature-conditioned refresh cadence is not merely disclosed as a circuit idea, but appears in a commercial Mobile DDR product contract whose self-refresh oscillator is automatically controlled by an on-die temperature sensor?

The bounded Micron device combines:

- `SELF REFRESH` with internal clocking and internally generated refresh cycles;
- an on-chip temperature sensor that automatically controls the self-refresh oscillator;
- a documented `TCSR` field whose programming has **no effect on this product version** because the automatic sensor path is used instead;
- `PASR`, through which the controller can separately select how much of the array is refreshed during self refresh;
- `Deep Power-Down`, which deliberately stops retaining array payload while documented mode-register settings survive the transition.

This is **not**:

- a full JEDEC genealogy of temperature-compensated self refresh;
- proof that Micron invented TCSR;
- a claim that every Mobile DDR / LPDDR generation implements TCSR identically;
- evidence that the on-die sensor directly measures every cell or row's remaining retention margin;
- modern per-row retention-aware refresh;
- RowHammer mitigation;
- proof that a register field is operational merely because it appears in an interface diagram.

The case therefore grounds a **commercial automatic self-refresh-cadence / selective-retention relation**, not a general history of mobile DRAM.

## Relation to the earlier DRAM cases

The existing DRAM cases already separate several relations commonly collapsed into `refresh`:

```text
Case 03
    why dynamic-cell state requires repeated restoration

Case 09
    where refresh-row enumeration comes from

Case 10
    how a leakage-related proxy can internalize a maintenance trigger

Case 21
    how AUTO REFRESH and SELF REFRESH move recurring maintenance authority
    across the package boundary

Case 33
    which bank/bank-group resources are blocked by a refresh operation

Case 34
    how measured environment can change selected refresh cadence

Case 35
    how a commercial Mobile DDR device combines self-refresh authority
    with automatic on-die temperature-conditioned cadence,
    while retaining separate controller authority over retained array coverage
```

Case 35 therefore does not replace Case 34. It supplies the commercial/product-contract bridge that Case 34 deliberately left open.

## Historical vocabulary and record

The central primary product document is Micron's **512Mb: 32 Meg x 16, 16 Meg x 32 Mobile SDRAM**, `MT48H32M16LF_1.fm - Rev. J 2/08 EN`, ©2005 Micron Technology, Inc. Its feature list explicitly includes:

- `Auto refresh and self refresh modes`;
- `On-chip temperature sensor to control refresh rate`;
- `Partial-array self refresh (PASR)`;
- `Deep power-down (DPD)`.

The Extended Mode Register section uses the historical terms:

- `Temperature-Compensated Self Refresh (TCSR)`;
- `Partial-Array Self Refresh (PASR)`;
- `self refresh oscillator`;
- `on-die temperature sensor`;
- `factory programmed optimal rate for the device temperature`.

The same product document also gives a particularly useful negative interface fact: although the EMR figure retains positions labelled `TCSR`, the note says the on-die temperature sensor is used in place of TCSR programming and that setting those bits has no effect. The prose then states that the temperature sensor automatically controls the self-refresh oscillator.

Micron Technical Note **TN-46-12, Mobile DRAM Power-Saving Features/Calculations**, Rev. A 10/05, separately explains TCSR as a mobile-DRAM power-saving feature. It describes two implementation loci: an on-board/on-device temperature sensor can automatically adjust self-refresh intervals, while a device without such a sensor can rely on a memory-controller temperature sensor and programmed control bits. The technical note also treats PASR and DPD as distinct power-saving mechanisms.

**Evidence boundary:** TN-46-12 says Micron and other JEDEC members had defined these features, but this case does not elevate that manufacturer note into a complete normative JEDEC standards chronology.

## Retained state and control state

The protected payload is still charge-dependent dynamic-array state. Case 35 adds several distinct control relations:

1. **self-refresh mode state** — entered through command/CKE conditions;
2. **internal refresh clocking** — recurring maintenance continues without the external system clock;
3. **temperature measurement** — an on-die sensor observes a thermal condition relevant to cadence;
4. **oscillator/cadence authority** — the product automatically selects a factory-programmed rate appropriate to device temperature;
5. **PASR coverage state** — EMR bits tell the device which array regions are to remain refreshed;
6. **mode-register state** — documented as retained even across exit from deep power-down;
7. **array payload state** — explicitly *not* retained in deep power-down.

`Cadence authority`, `retention coverage authority`, and `control-state retention` are project reconstruction terms, not Micron's historical vocabulary.

## Engineering reconstruction

### Temperature-conditioned cadence can be automatic while host-visible TCSR bits are inert

The most important interface counterexample is explicit in the datasheet:

> the TCSR field exists in the EMR definition, yet programming those bits has no effect on this device version because an on-die sensor automatically controls the self-refresh oscillator.

Therefore:

> **register-field presence ≠ effective software authority**.

And more specifically:

> **temperature-conditioned cadence ≠ host-visible cadence programmability**.

A retention relation cannot safely be reconstructed from field names alone. Product-specific semantics determine whether the host actually controls the mechanism.

### Self-refresh without an external clock is not inactivity

The device says that, after entering self refresh, it supplies its own internal clocking and performs its own refresh cycles; it may remain in this mode indefinitely within the specified operating conditions.

Therefore:

> **external-clock absence ≠ maintenance absence**.

Case 21 already grounded the general AUTO REFRESH / SELF REFRESH authority handoff in a 1999 Micron SDRAM. Case 35 adds a commercial device in which that internalized recurring work is itself temperature-conditioned.

### Environmental policy and maintenance authority can converge in one package

Case 34's 1991 Micron circuit sent its temperature-derived cadence signal onward to system logic. Case 35 instead documents an on-die sensor that automatically controls the self-refresh oscillator during a mode whose recurring refresh is internally clocked.

Thus:

> **temperature-conditioned cadence + self-refresh authority can be co-located without becoming the same analytical relation**.

The temperature relation answers *how frequently maintenance should recur under the sensed condition*. The self-refresh relation answers *who continues generating the recurring maintenance when ordinary external clocking is absent*.

Historical co-location does not erase the distinction.

### Cadence authority is independent of retention-coverage authority

The same EMR section makes PASR separately programmable. The controller can select all banks, two banks, one bank, half a bank, or a quarter bank for self-refresh maintenance in this product description. The following page says that normal READ/WRITE can address any bank during ordinary operation, but during PASR only the selected banks/segments are refreshed and data in the unused regions will be lost.

Therefore:

> **self-refresh cadence authority ≠ retained-array coverage authority**.

The device can automatically decide cadence from temperature while the controller independently decides *which subset deserves continued retention*.

This is a stronger retention distinction than a generic low-power feature list: maintenance frequency and preservation scope are separate control dimensions.

### Self refresh does not imply whole-array preservation

Once PASR is enabled, `SELF REFRESH` no longer entails that every previously writable location remains protected.

Therefore:

> **self-refresh active ≠ whole-array retained**.

Retention becomes intentionally selective. The controller must place data that is meant to survive into regions still covered by PASR.

The unrefreshed region is not merely temporarily unavailable; the datasheet explicitly warns that its data will be lost.

### Deep power-down separates payload retention from control-state retention

The Deep Power-Down section says the mode shuts off power to the entire memory array and that array data are not retained. Yet the exit procedure says the mode-register and extended-mode-register values are retained upon exit.

This yields a particularly sharp bounded result:

> **array-payload retention ≠ mode/control-state retention**.

The device can deliberately abandon the principal memory payload while preserving enough configuration state for later operation.

This claim is restricted to the documented product behavior. The source does not establish the physical substrate by which those register values survive DPD, and this case does not invent one.

### Power saving is not a single forgetting mechanism

TN-46-12 and the product datasheet distinguish three different power-saving moves:

- TCSR changes maintenance cadence according to temperature;
- PASR narrows the region receiving maintenance;
- DPD removes array retention altogether.

Therefore:

> **lower retention cost ≠ one uniform reduction of retention work**.

The same product family can save energy by doing maintenance less often, by maintaining less state, or by accepting complete loss of a state class.

## Failure and forgetting boundaries

The source set supports several bounded failure/forgetting distinctions:

- treating TCSR-labelled bits as effective software controls on this device would mis-model the actual cadence authority;
- a correct automatic cadence cannot preserve data deliberately excluded by PASR;
- entering DPD intentionally crosses a boundary where array payload is no longer retained;
- surviving mode-register values do not imply surviving array payload;
- the on-die temperature sensor is evidence of a temperature proxy, not proof of per-cell retention measurement or perfect thermal coverage;
- the product contract does not by itself establish what happens under sensor fault, thermal gradients, out-of-spec temperature, or undocumented implementation defects.

The retention failure risk is therefore not only `refresh stops`. It can also be **wrongly assigning authority or preservation scope when interpreting the interface**.

## Prior art and anti-anachronism

Case 34 already blocks a Micron-first narrative by grounding 1987-priority temperature-adaptive DRAM-refresh prior art and Micron's own 1991 acknowledgment of it. Case 35 therefore makes no invention-priority claim.

Nor does this case treat `automatic TCSR`, `retention coverage authority`, or `selective retention` as universal JEDEC terminology. Historical claims preserve the product's own vocabulary: `TCSR`, `PASR`, `SELF REFRESH`, `self refresh oscillator`, `on-die temperature sensor`, and `Deep Power-Down`.

Micron TN-46-12 provides period manufacturer context that these were mobile-DRAM power-management features discussed in relation to JEDEC members. A complete JEDEC revision-by-revision genealogy still requires the relevant standards themselves.

## Functional analogy and philosophical limit

A bounded functional analogy can compare PASR with other systems that preserve only a selected working set while intentionally allowing other state to disappear. The comparable function is **policy-controlled retention scope**.

The analogy stops there. PASR is not virtual-memory eviction, cache replacement, garbage collection, archival appraisal, distributed tombstoning, or secure deletion.

A narrow conceptual pressure does follow:

> A technical system can make persistence selective not only by deciding *when* maintenance occurs, but by deciding *which state remains entitled to maintenance at all*.

That is an engineering/philosophical interpretation of the documented mechanism. It is not evidence that Micron engineers formulated a philosophy of selective memory.

## Cross-case result

The DRAM retention decomposition can now be extended again:

```text
dynamic-cell payload / leakage process
    !=
environmental condition
    !=
temperature measurement
    !=
chosen self-refresh cadence
    !=
recurring maintenance authority
    !=
row enumeration
    !=
retained-array coverage policy
    !=
refresh target / interference geometry
    !=
restoration execution
    !=
intentional no-retention mode
    !=
separately surviving control state
```

Case 35's main contribution is that several of these axes coexist in one commercial product while remaining independently controllable or independently survivable.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Micron's Rev. J 2/08 512Mb Mobile SDRAM datasheet lists an on-chip temperature sensor, PASR, and DPD | H/P | direct manufacturer product document |
| The product's on-die temperature sensor automatically controls the self-refresh oscillator | H/P | direct TCSR section |
| Programming the documented TCSR bits has no effect on this device version | H/P | direct EMR note and TCSR prose |
| SELF REFRESH continues through internal clocking without external clocking | H/P | direct SELF REFRESH command description |
| PASR lets the controller select only part of the array for self-refresh maintenance | H/P | direct PASR section |
| Data in PASR-excluded regions will be lost | H/P | direct product warning |
| Deep power-down does not retain array data | H/P | direct DPD section |
| Mode-register and extended-mode-register values are retained across exit from DPD | H/P | direct DPD exit description |
| The on-die sensor measures every row's exact retention time | X | not the documented mechanism |
| Presence of TCSR-labelled bits proves host cadence control | X | directly contradicted by the datasheet |
| TCSR/PASR/DPD are one mechanism | X | documentation distinguishes three functions |
| This product establishes a complete JEDEC TCSR genealogy | X | product + manufacturer note are insufficient for revision-by-revision standards history |

## Related repositories

Current searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `temperature compensated self refresh`, `TCSR`, and mobile/LPDDR refresh returned no dedicated case to reuse. A broad JEDEC/mobile-DRAM standards genealogy should be routed there if developed comprehensively; this repository keeps the retention-specific authority/coverage comparison.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the anti-anachronism discipline: the product's `TCSR`/`PASR` vocabulary can be quoted historically, while `retention coverage authority` remains a modern reconstruction label.

## Sources

1. Micron Technology, Inc., **512Mb: 32 Meg x 16, 16 Meg x 32 Mobile SDRAM**, `MT48H32M16LF_1.fm - Rev. J 2/08 EN`, ©2005 Micron Technology, Inc. Relevant locations: feature list p. 1; Extended Mode Register / TCSR / PASR pp. 16–18 (printed pp. 17–18); AUTO REFRESH / SELF REFRESH p. 21 (printed p. 21); Deep Power-Down pp. 35–36 (printed pp. 35–36). Public mirror of the Micron PDF: <https://media.digikey.com/pdf/Data%20Sheets/Micron%20Technology%20Inc%20PDFs/MT48H(16,32)MxxL(F,G).pdf>.
2. Micron Technology, Inc., **TN-46-12: Mobile DRAM Power-Saving Features/Calculations**, Rev. A 10/05 EN, ©2005 Micron Technology, Inc. — used for period manufacturer terminology and the distinction between automatic on-device sensing and controller-programmed TCSR: <https://notes-application.abcelectronique.com/024/24-19986.pdf>.
3. Internal comparison only: [`34-micron-temperature-dependent-dram-refresh.md`](34-micron-temperature-dependent-dram-refresh.md) and [`21-micron-sdram-refresh-mode-handoff.md`](21-micron-sdram-refresh-mode-handoff.md).
