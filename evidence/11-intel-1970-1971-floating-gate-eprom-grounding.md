# Case 11 grounding record — Intel/Frohman floating-gate programmable ROM, 1970–1971

## Purpose

This record grounds the bounded mechanism claims used by [`../cases/11-intel-frohman-floating-gate-eprom-erasure.md`](../cases/11-intel-frohman-floating-gate-eprom-erasure.md).

The case is deliberately narrower than a history of ROM, PROM, EPROM, EEPROM, or Flash. It asks what changes in the retention comparison when a semiconductor state:

- is held as charge on an electrically isolated floating gate;
- survives without continuous operating power;
- can be selected and programmed electrically;
- can be read at a lower electrical stress without reproducing the programming event;
- but, in the bounded Intel/Frohman device disclosure, can be deliberately discharged by radiation applied to the physical device rather than by an ordinary addressed electrical erase command.

## Source classes

### P1 — Intel/Frohman device patent

Dov Frohman-Bentchkowsky, Intel Corp., US3660819A, _Floating gate transistor and method for charging and discharging same_. Filed 15 June 1970; published 2 May 1972.

Primary transcription: <https://patents.google.com/patent/US3660819A/en>

Directly inspected HTML-transcription anchors used in this case:

- metadata / filing / assignment: lines 15–35;
- device summary and long-term-storage objective: lines 124–140 and 215–224;
- prior-art boundary, including Kahng/Sze: lines 211–214;
- floating-gate insulation and avalanche-injection mechanism: lines 238–244 and 169–178 in the structured transcription;
- charge persistence / low-stress sensing: lines 174–178 in the structured transcription and lines 228–230 in the rendered patent text;
- radiation / thermal discharge methods: lines 179–180 in the structured transcription;
- claimed charging method: lines 185–189.

Central sourced facts:

1. The gate is surrounded by insulating material and has no ordinary electrical connection.
2. Charge is placed on the gate by avalanche injection across the insulation.
3. The patent explicitly seeks long-term storage without continuous application of power.
4. The existence of charge is sensed through transistor conductivity at a voltage below avalanche breakdown.
5. Charge can be removed by X-rays or ultraviolet light; the patent also mentions high-temperature discharge but warns that this may damage the device.

The OCR around one numerical retention estimate is malformed in the web transcription. This case therefore does **not** depend on that number. It uses only the patent's unambiguous qualitative claims of long-term / usefully long retention without continuous power.

### P2 — Intel/Frohman array patent

Dov Frohman-Bentchkowsky, Intel Corp., US3744036A, _Electrically programmable read only memory array_. Filed 24 May 1971; published 3 July 1973.

Primary transcription: <https://patents.google.com/patent/US3744036A/en>

Directly inspected HTML-transcription anchors:

- field, motivation, and prior-art categories: lines 227–233;
- successful 2,048-bit / 256 × 8 fully decoded floating-gate array: lines 234–236;
- floating-gate storage element and avalanche-injection write mechanism: lines 236–239;
- selected write cycle and preferred approximately 50 V example: lines 284–289;
- nondestructive read and preferred approximately 15 V read example: lines 290–293;
- later summary of nondestructive sensing condition: lines 297–300.

Central sourced facts:

1. The patent's period term is `electrically programmable read only memory` / `read only semiconductor memories`.
2. It explicitly defines nonvolatile storage as retention without an external power source.
3. It distinguishes one-time fusible-link ROMs from alterable ROMs in its own prior-art discussion.
4. Its disclosed floating-gate cells are selected through X/Y lines and programmed by avalanche injection.
5. The preferred embodiment uses a higher electrical stress for writing than for reading.
6. The patent states that information can be read without destruction; the read voltage is kept below the avalanche condition that would reprogram the storage element.

The approximately 50 V program and 15 V read values are **preferred-embodiment values**, not universal EPROM values and not silently assigned to every Intel 1702/1702A production revision.

### P3 — Kahng prior-art control

Dawon Kahng, Bell Telephone Laboratories, US3500142A, _Field effect semiconductor apparatus with memory involving entrapment of charge carriers_. Filed 5 June 1967; published 10 March 1970.

Primary transcription: <https://patents.google.com/patent/US3500142A/en>

Directly inspected anchors:

- filing and abstract / `relatively long memory` language: lines 180–204;
- trapped-charge mechanism after removal of inducing force: lines 191–204;
- carrier trapping after the field falls below transport conditions: lines 113–124 in the structured transcription;
- light-assisted transport / release boundary: lines 125–129.

This source is a **priority-control and mechanism-neighbor**, not evidence that the Intel/Frohman implementation is identical to Kahng's embodiment. It matters because it blocks the historical shortcut `Frohman invented floating-gate memory as such`. Frohman's own 1970-filed patent cites the Kahng/Sze floating-gate work as prior art.

### S1 — Institutional product context only

Intel, _A Success…Out of Quality Control Issues_, current corporate-history page: <https://www.intel.com/content/www/us/en/history/virtual-vault/articles/eprom.html>.

Computer History Museum, _1971: Reusable Programmable ROM Introduces Iterative Design Flexibility_: <https://www.computerhistory.org/siliconengine/reusable-programmable-rom-introduces-iterative-design-flexibility/>.

These later institutional sources identify the 1971 Intel 1702 with the EPROM product category and describe UV erasure through a quartz window. They are used only to connect the patent-bounded mechanism to the familiar historical category/product context. They do not substitute for a directly inspected 1702/1702A manufacturer datasheet or prove that every production detail equals either patent's preferred embodiment.

## Grounded claim ledger

| Claim | Label | Grounding |
| --- | --- | --- |
| Intel/Frohman disclosed an insulated floating gate whose stored charge can persist without continuous operating power | H/P | US3660819A |
| Avalanche injection can place charge on the bounded floating gate | H/P | US3660819A; US3744036A |
| X/Y-selected electrical programming was disclosed for a 2,048-bit fully decoded array | H/P | US3744036A |
| The array patent explicitly describes nondestructive read at lower stress than programming | H/P | US3744036A |
| Radiation can deliberately remove floating-gate charge in the bounded device disclosure | H/P | US3660819A |
| The 1971 Intel product category is historically called EPROM and associated with UV erasure | H/S | Intel institutional history; Computer History Museum |
| Floating-gate trapped-charge memory existed as prior art before Frohman's Intel filings | H/P | Kahng US3500142A; Frohman patent's own prior-art citation |
| `nonvolatile` means `physically immutable` | X | contradicted by deliberate discharge/erase mechanisms |
| electrical programmability implies electrical erasability | X | contradicted by the bounded Intel/Frohman radiation-erasure design |
| normal addressed read/write geometry must equal erase geometry | X | contradicted by electrically selected array access versus device-level radiation erase |
| the patents prove every exact production detail of Intel 1702/1702A | X | unsupported product-identity leap |
| Frohman was the first person to propose floating-gate memory in general | X | blocked by Kahng/Sze prior art and Frohman's own citation |

## Engineering reconstruction supported by the sources

The bounded retention relation is:

```text
program event
    -> avalanche injection places charge on an insulated floating gate
    -> charge remains after program voltage and ordinary operating power are removed
    -> later low-stress electrical sensing distinguishes charged / uncharged state
    -> separate erase intervention can remove the trapped charge
```

This yields several project-level decompositions:

```text
state-holding mechanism
    !=
programming mechanism
    !=
read/sense mechanism
    !=
erase mechanism
```

and

```text
read/program addressability
    !=
erase authority / erase geometry
```

The second distinction is the main reason this is a separate retention case rather than a generic semiconductor-memory chronology.

## Failure / forgetting boundaries

The primary sources support the existence of an insulated trapped-charge state and deliberate discharge mechanisms, but they do not justify a universal quantitative retention-life model for commercial EPROMs.

Within the bounded mechanism, relevant failure/forgetting classes include:

- unintended loss or transport of charge across the insulating barrier;
- insufficient program stress to establish the intended state;
- excessive or inappropriate stress that damages insulation or causes unintended programming;
- read stress approaching the programming regime rather than staying below it;
- deliberate radiation-induced discharge;
- loss of the package/window/environmental access needed for the intended erase procedure at product level.

Only the first five are direct mechanism consequences of the patents. Package/window serviceability is retained as product-context analysis and should be grounded from a directly inspected manufacturer datasheet before quantitative claims are added.

## Anti-anachronism and terminology controls

- `EPROM` is a useful product/category label supported by Intel and CHM retrospective history, but the central period patents themselves use `read-only memory`, `electrically programmable read only memory`, `floating gate`, and `storage element`.
- `hot-electron injection`, `FAMOS`, `EEPROM`, `Flash`, Fowler–Nordheim tunneling, page programming, block erase, and modern endurance/ECC terminology must not be projected backward unless separately sourced for the relevant design.
- The source supports radiation erase of the disclosed floating-gate transistor; it does **not** establish a universal rule that every floating-gate memory is UV-erasable.
- The 1971 array patent grounds selective electrical programming and nondestructive read; the exact production 1702/1702A circuit, package, programming algorithm, and UV dose remain product-specific questions.

## Related-repository duplication check

Searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `EPROM` and for floating-gate / EEPROM / Flash terms returned no dedicated case. The companion repository's current scope notes identify the semiconductor-memory middle as a gap rather than an already-grounded duplicate.

Accordingly this file keeps only the retention-specific comparison. A broad history of ROM masks, fuse PROM vendors, MNOS, floating-gate process development, commercial product generations, EEPROM, and Flash belongs primarily in `computing-archaeology` and should be linked here when developed.

## Promotion decision

**Case 11 is `grounded` at the bounded mechanism level.**

Promotion is justified because:

- two Intel manufacturer-primary patent families directly establish the storage, programming, array-selection, sensing, and discharge mechanisms;
- an earlier Bell Labs primary patent controls priority/genealogy claims;
- historical vocabulary is preserved;
- read, write/program, erase, power, and failure relations are separated;
- product identity and later EEPROM/Flash semantics are explicitly left outside the claim boundary;
- related-repository duplication was checked.

Remaining archival/deepening tasks are optional for this bounded case rather than promotion blockers: directly inspect a period 1702/1702A manufacturer datasheet/manual or the 1971 ISSCC material; establish product-specific UV wavelength/dose/timing only from such a source; and later build a **separate** EEPROM case for electrically controlled erasure before attempting the EEPROM → Flash transition.
