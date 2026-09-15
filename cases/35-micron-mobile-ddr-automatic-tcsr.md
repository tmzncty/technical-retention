# Micron Mobile DDR Automatic TCSR: On-Die Temperature Sensing, Self-Refresh Cadence, and Selective Retention

## Status

**`grounded`** — bounded to Micron's 512Mb Mobile DDR SDRAM documentation, especially the Rev. J 2/08 product datasheet, with Micron Technical Note TN-46-12 (Rev. A 10/05) used for terminology and implementation-locus context. A later bounded deepening adds Samsung 2005–2006 and Hynix 2008 product-document evidence showing that closely related automatic-TCSR / separate-PASR semantics were not Micron-local, while deliberately stopping short of a JEDEC genealogy or inter-vendor lineage claim.

Grounding records:

- [`../evidence/35-micron-2005-2008-mobile-ddr-tcsr-grounding.md`](../evidence/35-micron-2005-2008-mobile-ddr-tcsr-grounding.md)
- [`../evidence/35-samsung-hynix-2005-2008-auto-tcsr-cross-vendor-deepening.md`](../evidence/35-samsung-hynix-2005-2008-auto-tcsr-cross-vendor-deepening.md)

## Scope

This case asks a narrow question left open by Cases 21 and 34:

> What changes when temperature-conditioned refresh cadence is not merely disclosed as a circuit idea, but appears in a commercial Mobile DDR product contract whose self-refresh oscillator is automatically controlled by an on-die temperature sensor?

The bounded Micron device combines:

- `SELF REFRESH` with internal clocking and internally generated refresh cycles;
- an on-chip temperature sensor that automatically controls the self-refresh oscillator;
- a documented `TCSR` field whose programming has **no effect on this product version** because the automatic sensor path is used instead;
- `PASR`, through which the controller can separately select how much of the array is refreshed during self refresh;
- `Deep Power-Down`, which deliberately stops retaining array payload while documented mode-register settings survive the transition.

The cross-vendor deepening adds only one further historical proposition: Samsung and Hynix contemporaneously documented named Mobile-DDR families with automatic internal temperature-conditioned refresh and separately described PASR. Samsung's October 2005 Rev. 0.6 preliminary K4X51323PC specification and February 2006 K4X51163PC document explicitly say an external TCSR EMRS code is ignored while the internal sensor/control path automatically controls the self-refresh cycle; Hynix's July 2008 H5MS5122DFR/H5MS5132DFR document describes Auto TCSR using an internal sensor and no external EMRS command. These are product-document comparisons, not standards genealogy.

This is **not**:

- a full JEDEC genealogy of temperature-compensated self refresh;
- proof that Micron, Samsung, or Hynix invented TCSR;
- a claim that every Mobile DDR / LPDDR generation implements TCSR identically;
- evidence that the on-die sensor directly measures every cell or row's remaining retention margin;
- modern per-row retention-aware refresh;
- RowHammer mitigation;
- proof that a register field is operational merely because it appears in an interface diagram;
- proof that similar cross-vendor semantics imply direct technical transfer or identical circuitry;
- proof that Samsung's October 2005 preliminary specification was already a volume-shipped implementation.

The case therefore grounds a **commercial automatic self-refresh-cadence / selective-retention relation**, then shows that the broad relation appears in multiple contemporary vendor product documents.

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
    how commercial Mobile DDR devices combine self-refresh authority
    with automatic on-die temperature-conditioned cadence,
    while retaining separate controller authority over retained array coverage
    and, in some products, leaving historical external-TCSR controls ineffective
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

### Cross-vendor product-document deepening

Samsung's **K4X51323PC-7(8)E/G 16M x32 Mobile-DDR SDRAM**, Rev. 0.6, October 2005, is explicitly marked `Preliminary`. Its revision table traces the document family back to an October 27, 2004 target specification, but the currently inspected Rev. 0.6—not the uninspected earlier revision—is the safe evidence floor for the TCSR wording used here.

The Rev. 0.6 product text lists `Internal Temperature Compensated Self Refresh`, PASR, and DPD. Its TCSR section says an internal temperature sensor and control units automatically control the self-refresh cycle according to temperature ranges and says that if the controller issues the EMRS code for external TCSR, that TCSR code is **ignored**. PASR is separately described with full-, half-, and quarter-array choices.

A second Samsung family, **K4X51163PC-L(F)E/G 32M x16 Mobile-DDR SDRAM**, February 2006, repeats the same broad automatic-TCSR / ignored-external-TCSR pattern and separately documents PASR. This reduces the risk of treating the 2005 preliminary wording as a one-document anomaly while still not proving identical die implementation across Samsung families.

Hynix's **H5MS5122DFR / H5MS5132DFR Mobile DDR SDRAM 512Mbit**, Rev. 1.2, July 2008, lists `AUTO TCSR` and PASR as low-power features. It says an internal temperature sensor allows automatic refresh-rate adjustment according to temperature **without external EMRS command**, while PASR separately selects the memory array to be refreshed. Hynix's wording is not promoted into Samsung's stronger claim that an issued external TCSR command is ignored.

These records support a bounded cross-vendor historical result:

> By 2005–2008, multiple Mobile-DDR vendors documented designs in which temperature-conditioned self-refresh cadence could be internalized in the DRAM while PASR remained a separate mechanism for choosing retained array scope.

They do not establish identical circuitry, a direct inter-vendor technology-transfer chain, or the exact JEDEC clause history that produced the shared vocabulary.

## Retained state and control state

The protected payload is still charge-dependent dynamic-array state. Case 35 adds several distinct control relations:

1. **self-refresh mode state** — entered through command/CKE conditions;
2. **internal refresh clocking** — recurring maintenance continues without the external system clock;
3. **temperature measurement** — an on-die sensor observes a thermal condition relevant to cadence;
4. **oscillator/cadence authority** — the product automatically selects a factory-programmed rate appropriate to device temperature;
5. **PASR coverage state** — EMR bits tell the device which array regions are to remain refreshed;
6. **mode-register state** — documented by the Micron product as retained even across exit from deep power-down;
7. **array payload state** — explicitly *not* retained in Micron deep power-down;
8. **interface vocabulary/state** — a TCSR-labelled field or external command can remain visible even when the bounded product's automatic internal path is authoritative and the external path is ineffective or unnecessary.

`Cadence authority`, `retention coverage authority`, `effective control locus`, and `control-state retention` are project reconstruction terms, not manufacturer historical vocabulary.

## Engineering reconstruction

### Temperature-conditioned cadence can be automatic while host-visible TCSR bits are inert

The most important Micron interface counterexample is explicit in the datasheet:

> the TCSR field exists in the EMR definition, yet programming those bits has no effect on this device version because an on-die sensor automatically controls the self-refresh oscillator.

Therefore:

> **register-field presence ≠ effective software authority**.

And more specifically:

> **temperature-conditioned cadence ≠ host-visible cadence programmability**.

A retention relation cannot safely be reconstructed from field names alone. Product-specific semantics determine whether the host actually controls the mechanism.

Samsung independently strengthens this boundary: its 2005–2006 Mobile-DDR text says the external-TCSR EMRS code is ignored while the internal temperature-sensor/control path automatically controls the self-refresh cycle. Hynix in 2008 says its Auto TCSR operates without an external EMRS command.

Thus the methodological point is no longer dependent on one Micron product:

```text
external TCSR vocabulary present
    !=
external controller necessarily owns effective cadence authority
```

The exact negative semantics still remain product-specific: Samsung says `ignored`; Micron says the TCSR settings have no effect on the bounded device version; Hynix says automatic operation does not require external EMRS.

### Self-refresh without an external clock is not inactivity

The Micron device says that, after entering self refresh, it supplies its own internal clocking and performs its own refresh cycles; it may remain in this mode indefinitely within the specified operating conditions.

Therefore:

> **external-clock absence ≠ maintenance absence**.

Case 21 already grounded the general AUTO REFRESH / SELF REFRESH authority handoff in a 1999 Micron SDRAM. Case 35 adds commercial devices in which that internalized recurring work is itself temperature-conditioned. Hynix's 2008 document independently describes self-refresh operation without external clocking while separately describing Auto TCSR.

### Environmental policy and maintenance authority can converge in one package

Case 34's 1991 Micron circuit sent its temperature-derived cadence signal onward to system logic. Case 35 instead documents product families in which an on-die sensor automatically controls or adjusts self-refresh cadence during a mode whose recurring refresh is internally generated.

Thus:

> **temperature-conditioned cadence + self-refresh authority can be co-located without becoming the same analytical relation**.

The temperature relation answers *how frequently maintenance should recur under the sensed condition*. The self-refresh relation answers *who continues generating the recurring maintenance when ordinary external clocking is absent*.

Historical co-location does not erase the distinction.

### Cadence authority is independent of retention-coverage authority

The Micron EMR section makes PASR separately programmable. The controller can select all banks, two banks, one bank, half a bank, or a quarter bank for self-refresh maintenance in this product description. The following page says that normal READ/WRITE can address any bank during ordinary operation, but during PASR only the selected banks/segments are refreshed and data in the unused regions will be lost.

Samsung's 2005–2006 product documents and Hynix's 2008 product document independently preserve the same broad analytical split: automatic temperature-conditioned cadence is described separately from PASR-selected array coverage.

Therefore:

> **self-refresh cadence authority ≠ retained-array coverage authority**.

The device can automatically decide cadence from temperature while the controller independently decides *which subset deserves continued retention*.

This is a stronger retention distinction than a generic low-power feature list: maintenance frequency and preservation scope are separate control dimensions, and the distinction survives cross-vendor comparison.

### Self refresh does not imply whole-array preservation

Once PASR is enabled, `SELF REFRESH` no longer entails that every previously writable location remains protected.

Therefore:

> **self-refresh active ≠ whole-array retained**.

Retention becomes intentionally selective. The controller must place data that is meant to survive into regions still covered by PASR.

For the central Micron product, the unrefreshed region is not merely temporarily unavailable; the datasheet explicitly warns that its data will be lost. The cross-vendor comparison uses Samsung/Hynix PASR chiefly to establish separate coverage control, not to silently import every Micron failure wording into those products.

### Deep power-down separates payload retention from control-state retention

The Micron Deep Power-Down section says the mode shuts off power to the entire memory array and that array data are not retained. Yet the exit procedure says the mode-register and extended-mode-register values are retained upon exit.

This yields a particularly sharp bounded result:

> **array-payload retention ≠ mode/control-state retention**.

The device can deliberately abandon the principal memory payload while preserving enough configuration state for later operation.

This claim is restricted to the documented Micron product behavior. The source does not establish the physical substrate by which those register values survive DPD, and the Samsung/Hynix documents are not used to generalize this exact control-state-survival behavior across vendors.

### Power saving is not a single forgetting mechanism

TN-46-12 and the product datasheet distinguish three different power-saving moves:

- TCSR changes maintenance cadence according to temperature;
- PASR narrows the region receiving maintenance;
- DPD removes array retention altogether.

Therefore:

> **lower retention cost ≠ one uniform reduction of retention work**.

The same product family can save energy by doing maintenance less often, by maintaining less state, or by accepting complete loss of a state class. The Samsung/Hynix comparison shows that at least the first two dimensions were also independently visible in contemporary non-Micron Mobile-DDR product documentation.

## Failure and forgetting boundaries

The source set supports several bounded failure/forgetting distinctions:

- treating TCSR-labelled bits as effective software controls on the bounded Micron device would mis-model actual cadence authority;
- Samsung's documented external-TCSR EMRS code can be issued yet ignored, so command issuance is not proof of effective policy control;
- Hynix's automatic path does not require external EMRS, but that wording alone does not prove Samsung-identical ignore semantics;
- a correct automatic cadence cannot preserve data deliberately excluded by PASR;
- entering Micron DPD intentionally crosses a boundary where array payload is no longer retained;
- surviving Micron mode-register values do not imply surviving array payload;
- an on-die temperature sensor is evidence of a temperature proxy, not proof of per-cell retention measurement or perfect thermal coverage;
- a preliminary Samsung specification is not volume-shipment proof;
- similar cross-vendor product semantics do not prove identical implementation, direct transfer, or a particular normative JEDEC revision.

The retention failure risk is therefore not only `refresh stops`. It can also be **wrongly assigning authority or preservation scope when interpreting the interface**.

## Prior art and anti-anachronism

Case 34 already blocks a Micron-first narrative by grounding 1987-priority temperature-adaptive DRAM-refresh prior art and Micron's own 1991 acknowledgment of it. Case 35 therefore makes no invention-priority claim.

The Samsung/Hynix deepening strengthens this anti-anachronism rule rather than weakening it. Samsung's October 2005 Rev. 0.6 and February 2006 product records show that automatic internal TCSR semantics appeared in contemporary non-Micron product documentation; Hynix documents Auto TCSR in 2008. These records support cross-vendor coexistence, not a winner-takes-priority story.

The Samsung Rev. 0.6 revision table traces its document lineage to an October 27, 2004 target specification, but because the earlier revision content was not directly inspected, this case does **not** backdate the inspected TCSR semantics to that date.

Nor does this case treat `automatic TCSR`, `cadence authority`, `retention coverage authority`, or `selective retention` as universal JEDEC terminology. Historical claims preserve each source's product vocabulary: `TCSR`, `Internal Temperature Compensated Self Refresh`, `AUTO TCSR`, `PASR`, `SELF REFRESH`, `self refresh oscillator`, `on-die/internal temperature sensor`, and `Deep Power-Down`.

Micron TN-46-12 provides period manufacturer context that these were mobile-DRAM power-management features discussed in relation to JEDEC members. Samsung and Hynix product documents show overlapping vocabulary and behavior. A complete JEDEC revision-by-revision genealogy still requires the relevant standards themselves.

## Functional analogy and philosophical limit

A bounded functional analogy can compare PASR with other systems that preserve only a selected working set while intentionally allowing other state to disappear. The comparable function is **policy-controlled retention scope**.

A second bounded analogy can compare the TCSR interface situation with systems in which a legacy-visible control surface remains present after operational authority has moved into an automatic internal policy. The comparable function is **visible control vocabulary without guaranteed effective external authority**.

The analogies stop there. PASR is not virtual-memory eviction, cache replacement, garbage collection, archival appraisal, distributed tombstoning, or secure deletion; automatic TCSR is not an abstract autonomous-agent architecture.

A narrow conceptual pressure does follow:

> A technical system can make persistence selective not only by deciding *when* maintenance occurs, but by deciding *which state remains entitled to maintenance at all*; and the visible language of external control can outlive the external control's actual authority.

That is an engineering/philosophical interpretation of the documented mechanisms. It is not evidence that Samsung, Micron, or Hynix engineers formulated a philosophy of selective memory or delegated agency.

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
effective cadence-control locus
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
    !=
host-visible interface vocabulary
```

Case 35's main contribution is that several of these axes coexist in commercial/product-level Mobile-DDR documentation while remaining independently controllable or independently meaningful. The Samsung/Micron/Hynix comparison adds a stronger methodological boundary:

```text
shared historical interface vocabulary
    !=
shared effective authority
    !=
identical physical implementation
    !=
proven standards genealogy
```

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Micron's Rev. J 2/08 512Mb Mobile SDRAM datasheet lists an on-chip temperature sensor, PASR, and DPD | H/P | direct manufacturer product document |
| The Micron product's on-die temperature sensor automatically controls the self-refresh oscillator | H/P | direct TCSR section |
| Programming the documented Micron TCSR bits has no effect on this device version | H/P | direct EMR note and TCSR prose |
| Micron SELF REFRESH continues through internal clocking without external clocking | H/P | direct SELF REFRESH command description |
| Micron PASR lets the controller select only part of the array for self-refresh maintenance | H/P | direct PASR section |
| Data in Micron PASR-excluded regions will be lost | H/P | direct product warning |
| Micron Deep power-down does not retain array data | H/P | direct DPD section |
| Micron mode-register and extended-mode-register values are retained across exit from DPD | H/P | direct DPD exit description |
| Samsung K4X51323PC Rev. 0.6 is an October 2005 preliminary Mobile-DDR specification | H/P | Samsung manufacturer document via archival mirror |
| Samsung Rev. 0.6 documents Internal TCSR with internal temperature sensor/control units | H/P | direct Samsung TCSR section via archival mirror |
| Samsung says an external TCSR EMRS code is ignored | H/P | direct negative interface statement |
| Samsung separately documents full / half / quarter-array PASR | H/P | direct PASR section |
| Samsung's February 2006 K4X51163PC document repeats the same broad automatic-TCSR / ignored-external-TCSR pattern | H/P | named-family manufacturer document via archival mirror |
| Hynix Rev. 1.2 July 2008 documents Auto TCSR using an internal temperature sensor and no external EMRS command | H/P | manufacturer document via archival mirror |
| The on-die/internal sensors measure every row's exact retention time | X | not the documented mechanism |
| Presence of TCSR-labelled bits proves host cadence control | X | directly contradicted by Micron/Samsung bounded product semantics |
| Samsung's October 2005 preliminary specification proves volume shipment | X | not established |
| Similar Samsung/Micron/Hynix behavior proves identical circuitry or direct technology transfer | X | no genealogy evidence |
| TCSR/PASR/DPD are one mechanism | X | documentation distinguishes the functions |
| This product-document set establishes a complete JEDEC TCSR genealogy | X | standards text still requires direct revision-by-revision inspection |

## Related repositories

Current searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `temperature compensated self refresh`, `TCSR`, and mobile/LPDDR refresh returned no dedicated case to reuse. A broad JEDEC/mobile-DRAM standards and vendor genealogy should be routed there if developed comprehensively; this repository keeps the retention-specific authority/coverage comparison.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the anti-anachronism discipline: the products' `TCSR` / `Internal TCSR` / `AUTO TCSR` / `PASR` vocabulary can be quoted historically, while `cadence authority`, `effective control locus`, and `retention coverage authority` remain modern reconstruction labels.

## Sources

1. Micron Technology, Inc., **512Mb: 32 Meg x 16, 16 Meg x 32 Mobile SDRAM**, `MT48H32M16LF_1.fm - Rev. J 2/08 EN`, ©2005 Micron Technology, Inc. Relevant locations: feature list p. 1; Extended Mode Register / TCSR / PASR pp. 16–18 (printed pp. 17–18); AUTO REFRESH / SELF REFRESH p. 21 (printed p. 21); Deep Power-Down pp. 35–36 (printed pp. 35–36). Public mirror of the Micron PDF: <https://media.digikey.com/pdf/Data%20Sheets/Micron%20Technology%20Inc%20PDFs/MT48H(16,32)MxxL(F,G).pdf>.
2. Micron Technology, Inc., **TN-46-12: Mobile DRAM Power-Saving Features/Calculations**, Rev. A 10/05 EN, ©2005 Micron Technology, Inc. — used for period manufacturer terminology and the distinction between automatic on-device sensing and controller-programmed TCSR: <https://notes-application.abcelectronique.com/024/24-19986.pdf>.
3. Samsung Electronics, `K4X51323PC-7(8)E/G`, **16M x32 Mobile-DDR SDRAM**, Rev. 0.6, October 2005, preliminary. Revision-history archival HTML: <https://www.alldatasheet.com/html-pdf/168597/SAMSUNG/K4X51323PC-7E/606/2/K4X51323PC-7E.html>; feature page: <https://www.alldatasheet.com/html-pdf/168597/SAMSUNG/K4X51323PC-7E/912/3/K4X51323PC-7E.html>; TCSR/PASR text preserved in the mirrored Samsung document: <https://datasheet4u.com/pdf-down/K/4/X/K4X51323PC-7E_Samsungsemiconductor.pdf>.
4. Samsung Electronics, `K4X51163PC-L(F)E/G`, **32M x16 Mobile-DDR SDRAM**, February 2006. Archival overview: <https://www.alldatasheet.com/datasheet-pdf/pdf/146538/SAMSUNG/K4X51163PC.html>; TCSR/PASR page transcription: <https://www.alldatasheet.co.kr/html-pdf/146538/SAMSUNG/K4X51163PC/2721/9/K4X51163PC.html>.
5. Hynix Semiconductor, `H5MS5122DFR Series / H5MS5132DFR Series`, **Mobile DDR SDRAM 512Mbit (16M x 32bit)**, Rev. 1.2, July 2008. Public archival transcription: <https://dtsheet.com/doc/642277/hynix-h5ms5132dfr>.
6. Internal comparison only: [`34-micron-temperature-dependent-dram-refresh.md`](34-micron-temperature-dependent-dram-refresh.md), [`21-micron-sdram-refresh-mode-handoff.md`](21-micron-sdram-refresh-mode-handoff.md), and the cross-vendor deepening record linked above.
