# Intel/Frohman Floating-Gate EPROM: Retention by Trapped Charge and External Erasure

## Status

**`grounded`** — bounded to the Intel/Frohman floating-gate storage/transistor and programmable-ROM disclosures filed in 1970–1971, with Kahng's 1967-filed Bell Labs patent used as a prior-art control.

Grounding record: [`../evidence/11-intel-1970-1971-floating-gate-eprom-grounding.md`](../evidence/11-intel-1970-1971-floating-gate-eprom-grounding.md).

## Scope

This case is not a general history of ROM, fuse PROM, EPROM, EEPROM, or Flash. It asks one narrower retention question:

> What changes when a nonvolatile semiconductor state can be created by an addressed electrical programming operation, read without recreating that operation, yet deliberately erased by a different physical intervention applied to the device?

The core primary sources are:

1. Dov Frohman-Bentchkowsky / Intel, US3660819A, _Floating gate transistor and method for charging and discharging same_, filed 15 June 1970;
2. Dov Frohman-Bentchkowsky / Intel, US3744036A, _Electrically programmable read only memory array_, filed 24 May 1971;
3. Dawon Kahng / Bell Telephone Laboratories, US3500142A, _Field effect semiconductor apparatus with memory involving entrapment of charge carriers_, filed 5 June 1967, used to prevent a false invention-priority claim.

Later Intel and Computer History Museum histories identify the 1971 Intel 1702 with the `EPROM` category and UV erasure. Those institutional histories are product/context evidence, not substitutes for a directly inspected period 1702/1702A datasheet.

## Why this changes the comparison

Mapped Flash Case 04 began after the medium already had nonvolatile cell state and asked how logical identity survives remapping, invalidation, copying, and erase-unit reclamation.

Case 11 moves downward and backward one mechanism layer. Its central distinction is not mapping but **asymmetry among holding, programming, reading, and erasing**:

```text
hold
    trapped charge remains on insulated floating gate

program
    selected electrical stress produces avalanche injection

read
    smaller electrical stress senses state without causing avalanche

erase
    radiation can remove the trapped charge in the bounded device disclosure
```

The same retained bit therefore participates in several different control geometries. `Nonvolatile` describes the hold condition, not the entire write/read/forgetting regime.

## Historical vocabulary

The Intel patents use period terms including:

- `floating gate`;
- `storage retention transistor`;
- `read-only memory`;
- `electrically programmable read only memory`;
- `nonvolatile semiconductor storage device`;
- `storage element`;
- `avalanche injection`;
- `write cycle` and `read cycle`;
- `X lines` and `Y lines`.

The central patents do not need later `Flash`, page/block-erase, FTL, or SSD vocabulary to explain their mechanism.

`EPROM` is used in this case title as the established historical product/category label for Intel's 1971 1702 context. It is not silently substituted for the patents' own phrases when reporting what Frohman wrote.

## Historical record

### H/P — an electrically isolated gate can retain charge without continuous operating power

US3660819A describes a floating gate substantially enclosed by insulating material, with no ordinary electrical connection to it. Charge is placed onto that gate by avalanche injection from the semiconductor substrate/junction region through the insulating layer.

The patent explicitly states an objective of long-term storage **without continuous application of power**. Once charged, the gate has no ordinary discharge path; later electrical sensing can distinguish charged from uncharged state through the transistor's conductivity characteristics.

This is a stronger retention statement than `the chip is a ROM`: the physical distinction being retained is an electrical charge trapped on an isolated gate, and quiescent retention does not require a DRAM-like refresh schedule or SRAM-like continuous support supply.

### H/P — programming is an addressed electrical operation

US3744036A embeds the floating-gate element in an electrically programmable memory array. The patent describes a successful fully decoded 2,048-bit array organized as 256 words × 8 bits, with memory cells connected to X/Y selection lines.

A selected cell is programmed by applying sufficient electrical stress to produce avalanche injection and charge its floating gate. In the preferred P-channel embodiment the patent gives an approximately 50 V programming example; this value is kept strictly within that disclosed embodiment and is not treated as a universal EPROM voltage.

### H/P — read is explicitly nondestructive in the bounded array

The same array patent separates the read cycle from the write/program cycle. Reading uses a smaller electrical magnitude than programming; the preferred example gives approximately 15 V for read.

The patent explicitly says the stored information can be read without destruction and explains that the read voltage remains below the avalanche condition. The relevant retention result is therefore:

> **sensing the state does not require reproducing the physical event that created it.**

This contrasts with the bounded destructive-read magnetic-core regime and with destructive sensing/restoration in some dynamic-cell designs.

### H/P — the storage device can be deliberately discharged by radiation

US3660819A states that X-rays can remove charge from the floating gate and that ultraviolet light applied directly to the transistor can also remove it. High-temperature discharge is mentioned as another possibility, with an explicit warning that it may damage the device.

For the retention comparison, this is crucial: the same insulation that makes the state durable under ordinary quiescent conditions does not make the state physically immutable. The design contains a deliberate route from retained state to erased state.

### H/P — floating-gate memory predates the Intel/Frohman filing

Frohman's own patent identifies the Kahng/Sze 1967 floating-gate work as prior art. Kahng's US3500142A, filed in 1967, describes charge trapped in an insulated metallic layer so that an induced semiconductor condition persists after the inducing force is removed, and discusses erasing/modifying memory.

Accordingly this case does **not** say that Frohman invented floating-gate memory in the unrestricted sense. The bounded Intel contribution studied here is the particular practical avalanche-injection / isolated-gate design and its integration into an electrically programmable array, not a universal priority claim.

### H/S — the 1971 Intel 1702 provides the EPROM product context

Intel's later institutional history and the Computer History Museum identify the 1702 as an EPROM introduced in 1971 and describe UV erasure through a quartz-window package.

These sources justify using the familiar category label and show the product-level significance of external optical erasure. They are not used to infer exact transistor topology, UV dose, programming algorithm, or production revision from the patents.

## Retained state and substrate

The retained state is charge occupancy on an electrically isolated floating gate together with the resulting change in transistor conduction/threshold behavior sufficient for later sensing.

The physical retention condition can be summarized as:

```text
charge injected onto floating gate
    +
insulating barrier suppresses ordinary charge escape
    ->
state remains after programming field is removed
```

Unlike SRAM, retention does not require a continuously powered regenerative feedback loop. Unlike DRAM, the bounded device has no periodic refresh deadline merely to keep the programmed state present. Unlike magnetic core, the distinction is trapped electronic charge rather than remanent magnetization.

These are engineering comparisons, not historical claims that Intel engineers organized the technologies under the repository's present taxonomy.

## Programming, read, and erase are different operations

### Programming

The array uses electrical selection and a sufficiently large field to produce avalanche injection in the selected storage device.

### Reading

The array uses electrical selection at lower stress, below the avalanche condition, to sense the stored state. The source explicitly calls the read nondestructive.

### Erasure

The bounded device patent removes charge with radiation rather than with the ordinary lower-stress read operation or the X/Y-selected avalanche-programming step.

This gives the case its main decomposition:

```text
retention mechanism
    !=
program mechanism
    !=
read mechanism
    !=
erase mechanism
```

A storage technology should therefore not be classified only by what keeps a bit present. The mechanisms that create, inspect, and deliberately destroy the distinction may be physically different.

## Addressability and erase geometry

US3744036A makes read/program selection an array operation through X/Y lines. US3660819A, by contrast, describes charge removal by radiation applied to the transistor/device.

At the bounded mechanism level this supports:

> **read/program addressability ≠ erase authority or erase geometry.**

A bit may be individually selected for ordinary electrical operations while the mechanism available for forgetting is physically coarser or externally applied.

The later 1702 quartz-window product context makes this especially visible, but this case does not yet quantify the exact erase granularity/dose of a production 1702A from a period manufacturer manual. That remains archival deepening.

## Engineering reconstruction

### Nonvolatility is a hold relation, not immutability

The floating gate can retain charge without continuous operating power, yet the same stored charge can be deliberately removed. `Nonvolatile` therefore answers one question — what happens when ordinary power disappears — rather than the stronger question whether a state can ever be altered or forgotten.

### Electrical programmability does not imply electrical erasability

The bounded Intel array is electrically programmable, but the device patent's erase path uses X-ray/UV radiation. Later EEPROM/Flash work changes this relation and requires a separate case.

Project comparison term:

```text
program-control geometry != erase-control geometry
```

### Read-only is an operational regime, not a statement of physical impossibility

The historical phrase `electrically programmable read only memory` already contains the apparent tension. Normal use can treat the device as read-only while a separate programming/erase regime exists outside ordinary read service.

This should not be flattened into the modern slogan `ROM is immutable`.

### Retention barriers also shape forgetting

The insulating barrier is what suppresses ordinary loss of trapped charge. Erasure works by creating a condition under which that retained charge can leave. At the engineering level, forgetting is not simply the absence of retention; it can be a deliberately induced transition across the same physical barrier that made retention possible.

## Failure and forgetting

Several failure classes must remain separate:

- **retention failure:** charge leaks or is transported away unintentionally;
- **program failure:** the intended selected state is not established;
- **read disturbance:** sensing stress approaches a regime capable of changing state, even though the sourced preferred read stays below avalanche;
- **erase failure:** the deliberate discharge operation does not sufficiently remove the trapped charge;
- **device damage:** an erase method such as excessive heat can destroy the device rather than merely reset its memory state.

The patents do not supply a universal commercial reliability model. This case therefore does not invent retention-year distributions, endurance-cycle counts, UV-dose margins, or failure rates.

## Functional analogy and anti-anachronism

Useful modern analytical phrases include `erase geometry`, `program/erase asymmetry`, and `control-plane asymmetry`. They are not period Intel terminology.

Likewise, it is reasonable to compare external UV erase with later block erase as two examples in which forgetting has a geometry different from ordinary read addressing, but they are not the same engineering mechanism. Case 04's Flash erase/reclamation semantics must not be projected backward into this EPROM case.

## Philosophical limit

The mechanism makes one conceptual problem concrete: a state can be highly resistant to ordinary disappearance yet intentionally vulnerable to a special erasure environment. Durability and erasability are therefore not simple opposites.

That observation may later matter for a philosophy of technical forgetting, but no patent source is evidence that Frohman or Kahng formulated a philosophical theory of memory, forgetting, or exteriorization.

## Cross-case result

Case 11 adds a new comparison axis that Cases 02–10 did not force as sharply:

```text
what keeps a state
    !=
what creates it
    !=
what senses it
    !=
what is authorized/able to erase it
```

It also adds a boundary between **addressable access** and **erasability**. Selection can be fine-grained for programming/read while deletion/reset may require a physically different intervention.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Frohman's Intel floating-gate device retains charge without continuous operating power | H/P | US3660819A |
| Charge is programmed by avalanche injection in the bounded Intel device/array | H/P | US3660819A; US3744036A |
| The 1971-filed array uses X/Y selection and a fully decoded 2,048-bit floating-gate design | H/P | US3744036A |
| The bounded array read is nondestructive and below programming avalanche stress | H/P | US3744036A |
| Radiation can remove charge from the bounded floating-gate transistor | H/P | US3660819A |
| Intel's 1702 belongs to the 1971 EPROM product context | H/S | Intel institutional history; Computer History Museum |
| Frohman invented floating-gate memory generally | X | contradicted by Kahng/Sze prior art and Frohman's own citation |
| electrical programmability implies electrical erasure | X | contradicted by bounded radiation-erasure mechanism |
| `read-only` means the physical state cannot be changed | X | contradicted by programming and erase regimes |
| exact 1702/1702A production topology and UV parameters are proven by these patents | X | product-specific evidence gap |
| program/read addressability and erase geometry must be identical | X | contradicted by bounded mechanism partition |

## Related repositories

Searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated EPROM / floating-gate case to reuse. Its current semiconductor-memory gap should eventually carry the broader engineering history.

`technical-retention` therefore keeps only the retention-specific distinction among quiescent trapped-charge persistence, addressed programming, nondestructive read, and external erasure.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the anti-anachronism discipline: a later lineage `ROM → PROM → EPROM → EEPROM → Flash` can organize present research, but it must not be mistaken for the problem vocabulary or teleology of the historical actors.

## Sources

1. Dov Frohman-Bentchkowsky, Intel Corp., US3660819A, _Floating gate transistor and method for charging and discharging same_: <https://patents.google.com/patent/US3660819A/en>.
2. Dov Frohman-Bentchkowsky, Intel Corp., US3744036A, _Electrically programmable read only memory array_: <https://patents.google.com/patent/US3744036A/en>.
3. Dawon Kahng, Bell Telephone Laboratories, US3500142A, _Field effect semiconductor apparatus with memory involving entrapment of charge carriers_: <https://patents.google.com/patent/US3500142A/en>.
4. Intel, _A Success…Out of Quality Control Issues_: <https://www.intel.com/content/www/us/en/history/virtual-vault/articles/eprom.html>.
5. Computer History Museum, _1971: Reusable Programmable ROM Introduces Iterative Design Flexibility_: <https://www.computerhistory.org/siliconengine/reusable-programmable-rom-introduces-iterative-design-flexibility/>.

## Next bounded bridge

Do **not** jump directly to generic Flash history. The next source-worthy step is an EEPROM case in which erasure itself becomes electrically controlled, followed only then by a separate Flash case about erase granularity / fast bulk erase if it changes the retention comparison. The key question is whether the locus and geometry of forgetting move back inside ordinary electrical control and what new endurance/maintenance obligations appear.
