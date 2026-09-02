# Case 13 Grounding Record — Early Flash Coarse-Erase Transition, 1980–1988

## Purpose

This record grounds the bounded transition used in Case 13:

> electrically erasable nonvolatile memory can deliberately trade fine-grained erase authority for a one-transistor/high-density cell and shared erase infrastructure, while preserving finer-grained read/program addressing and in-system control.

The claim is narrower than a general invention history of Flash, NOR, NAND, EEPROM, or SSDs.

It is also narrower than saying that coarse erase was the only way to build Flash. The evidence establishes a historically real design path and its retention consequences, not a universal law of nonvolatile memory.

## Evidence-layer rule

The sources are used in distinct roles:

- **H/P** — period patents and papers establish vocabulary, cell/array organization, erase/program geometry, timing, control, and design objectives;
- **H/S** — a later technical retrospective by an Intel Flash pioneer is used only to corroborate the cost/function tradeoff, not to substitute for period evidence;
- **E** — the repository reconstructs what asymmetric erase/program granularity implies for retention and rewrite;
- **A** — later terms such as `erase domain`, `coarse-grained forgetting`, and `rewrite amplification` are comparison vocabulary only;
- **X** — invention-priority and exact-product-identity claims are rejected unless directly established.

## Source A — Masuoka and Iizuka / Toshiba, US4531203A

**Fujio Masuoka and Hisakazu Iizuka, _Semiconductor memory device and method for manufacturing the same_, US4531203A.**

- Japanese priority: 20 December 1980;
- U.S. filing: 13 November 1981;
- publication/grant: 23 July 1985;
- original assignee: Tokyo Shibaura Electric Co., Ltd. / Toshiba lineage.

Primary text: <https://patents.google.com/patent/US4531203A/en>

### Directly inspected anchors

Google Patents transcription:

- metadata / priority / inventors / assignee: lines 15–39;
- background comparison between UV-erasable EPROM and electrically erasable PROM: lines 390–403;
- conventional two-transistor electrically erasable cell and density penalty: lines 394–399;
- one-bit cell as one MOS transistor with floating, control, and erase gates: lines 478–482;
- shared control/erase gates and array lines: lines 479–483;
- write/read/nonvolatile behavior: lines 485–490;
- electrical erase by high-voltage erase line and field emission: lines 491–494;
- one-transistor electrically erasable cell and packaging-density rationale: lines 497–503;
- common erase gate can serve multiple cells; example four-bit grouping and alternatives: lines 539–559;
- reduced contact count / packaging-density consequence: lines 545–548.

### What Source A establishes

**H/P** — the patent explicitly treats packaging density as a design problem. Its background contrasts a conventional two-transistor electrically erasable cell with the one-transistor-per-cell density available to UV EPROM.

**H/P** — the disclosed design uses a single MOS memory transistor with floating gate, control gate, and erase gate. Erase infrastructure can be shared across multiple cells rather than requiring a separate selection transistor for every bit.

**H/P** — writing, reading, and erasing are physically distinct regimes. Writing injects carriers into the floating gate; reading senses the resulting threshold/conduction state at lower stress; erasing removes stored charge through a high-field path to the erase gate.

**H/P** — the patent explicitly links the one-transistor organization and shared erase infrastructure to packaging density, and it treats short-period electrical erase as a design objective.

### What Source A does not establish

**X** — it does not by itself establish the exact 1984 IEDM `Flash` array or a named commercial Toshiba Flash product.

**X** — it does not establish that every embodiment has one fixed erase granularity. The patent itself discusses several sharing arrangements for erase gates.

**X** — it does not establish that Masuoka/Iizuka were the first people ever to propose a one-transistor electrically erasable cell. Its own background cites prior E²PROM work, including Kupec et al. 1980.

That last point is important: the patent is evidence for a bounded mechanism and design tradeoff, not a universal priority claim.

## Source B — Masuoka et al., IEDM 1984

**F. Masuoka, M. Asano, H. Iwahashi, T. Komuro, S. Tanaka et al., “A new flash E²PROM cell using triple polysilicon technology,” _1984 International Electron Devices Meeting_, pp. 464–467.**

DOI: <https://doi.org/10.1109/IEDM.1984.190752>

### Evidence status

The bibliographic record and abstract text were checked through multiple scholarly indexes. A directly renderable full-paper facsimile was not obtained in this slice.

Therefore:

- title, venue, year, page range, DOI, and abstract-level claims are usable as **H/P indexed primary evidence**;
- figure-level topology, exact page wording beyond the indexed abstract, and detailed measured curves remain archival cleanup.

### Abstract-level claims checked

The indexed abstract describes:

- a `Flash Electrically Erasable-PROM` cell;
- one transistor per bit;
- suitability for a 256-Kbit design;
- hot-carrier programming similar to EPROM;
- simultaneous erasure of all memory-cell contents through field emission from floating gate to erase gate.

This source supplies the period `Flash` vocabulary and the explicit whole-array erase relation needed for the bounded transition.

### Boundary

The repository does not use the abstract as if the complete IEDM paper had been visually inspected. All claims requiring figures, measured distributions, oxide-thickness interpretation, or precise internal array routing remain outside this record unless separately sourced.

## Source C — Intel, US5053990A, filed 1988

**Jerry A. Kreifels, Alan Baker, George Hoekstra, Virgil N. Kynett, Steven Wells, Mark Winston / Intel, _Program/erase selection for flash memory_, US5053990A.**

- filed / priority: 17 February 1988;
- assignee: Intel Corporation;
- publication/grant: 1 October 1991.

Primary text: <https://patents.google.com/patent/US5053990A/en>

### Directly inspected anchors

Google Patents transcription:

- metadata: lines 15–47;
- historical distinction among EPROM, EEPROM, and `flash EPROM`: lines 149–168;
- entire-array simultaneous electrical erase and one-device-per-cell statement: lines 162–166;
- command-port architecture and erase/program verification: lines 168–176;
- preferred 32,768 × 8, one-transistor, 1.5-µm Flash embodiment: lines 189–200;
- X/Y addressing, data path, command port, and erase/program voltage generation: lines 201–224;
- erase-voltage generator explicitly connected to simultaneously erase the memory array: lines 215–216;
- two-write erase command and all-array source-voltage application: lines 244–247;
- addressed-cell programming: lines 249–253;
- iterative erase / verify loop, address-by-address verification, pulse growth, and failure limit: lines 254–264.

### What Source C establishes

**H/P** — Intel's period patent vocabulary explicitly defines a `flash EPROM` / electrically erasable EPROM/EEPROM regime in which the entire array is electrically erased simultaneously while cells use one device per cell.

**H/P** — the preferred embodiment is a 32K × 8, 256-Kbit array with a one-transistor cell. Erasure uses Fowler–Nordheim tunneling from floating gate toward the source; programming uses hot-electron injection.

**H/P** — erase and program have different address geometry. The erase-voltage generator acts on the entire array, while programming loads an address and data and applies the programming condition to the addressed cell/byte path.

**H/P** — in-system electrical alterability is mediated by retained control state and algorithmic work: command/state registers, voltage generators, erase/program commands, and verify cycles.

**H/P** — whole-array physical erase does not imply that verification is one undifferentiated action. The disclosed algorithm repeatedly erases, then walks addresses to verify erased state and can repeat the bulk erase pulse if a byte fails verification.

### What Source C does not establish

**X** — it is not silently identified with a specific catalog part number in this repository.

The preferred dimensions and the authors overlap closely with period Intel Flash papers, but the source itself is sufficient for the mechanism claim without making an exact product-identity inference.

**X** — the patent does not prove that all Flash technologies erase the whole array. Later sector/block architectures are distinct regimes.

## Source D — Kynett et al., IEEE JSSC 1988

**V. N. Kynett, A. Baker, M. L. Fandrich, G. P. Hoekstra, O. W. Jungroth, J. A. Kreifels, S. Wells, M. D. Winston, “An In-System Reprogrammable 32 K × 8 CMOS Flash Memory,” _IEEE Journal of Solid-State Circuits_ 23(5), 1988, pp. 1157–1163.**

DOI: <https://doi.org/10.1109/4.5938>

### Evidence status

The bibliographic record and abstract were checked through scholarly indexes; a directly renderable full-paper facsimile was not obtained in this slice.

The indexed abstract reports:

- 256 Kbit / 32K × 8 organization;
- one-transistor 6 × 6 µm² cell;
- electrical erasure of all cells in the array matrix in roughly 200 ms;
- typical electrical programming at roughly 100 µs per byte;
- a command-port interface for microprocessor-controlled reprogramming;
- cycling demonstrated beyond 10,000 erase/program cycles.

These abstract-level facts independently corroborate the asymmetric erase/program geometry in a period peer-reviewed Intel engineering paper.

### Boundary

No figure-specific, waveform-specific, or page-specific claim beyond the indexed abstract is treated as directly inspected. Exact page anchors remain archival cleanup.

## Source E — Lai 2023 retrospective on Intel ETOX

**Stefan K. Lai, “Development of ETOX NOR Flash Memory,” in _75th Anniversary of the Transistor_, 2023.**

DOI: <https://doi.org/10.1002/9781394202478.ch16>

This is **H/S**, not period evidence.

Its summary describes Intel ETOX Flash as an effort to obtain EEPROM-like in-system alterability at a product cost approaching EPROM, with the eventual design compromise limiting alterability to large blocks rather than EEPROM-style single-byte alterability.

This retrospective is useful because it states the cost/function tradeoff explicitly. It does not replace the period patents/papers for mechanism or chronology, and it does not establish universal invention priority.

## Related-repository duplication check

Before writing this slice, `tmzncty/computing-archaeology` was searched for:

- `Masuoka flash EEPROM`;
- `flash memory EEPROM NAND`.

No dedicated matching Flash case was returned by repository code search.

Therefore Case 13 contains only the retention-specific mechanism argument. A future detailed device/process history should still be routed to `computing-archaeology` rather than expanded here.

## Grounded mechanism reconstruction

The sources support the following bounded relation:

```text
fine-grained electrically erasable EEPROM
    can spend cell area / selection circuitry
    to make erase finely selectable

one-transistor Flash lineage
    shares erase infrastructure across many cells
    while keeping finer-grained program/read selection

therefore
program/read granularity
    can be finer than
erase granularity
```

This is an **engineering reconstruction grounded in period design evidence**, not a claim that every historical engineer formulated the tradeoff in these exact words.

## Retention-specific consequences

### 1. Erase geometry becomes a retention dependency among neighbors

If one physical erase action resets many current cells together, revising one logical value can require preserving other still-current values before that erase and restoring them afterward.

The bounded 1988 Intel device does not itself provide an FTL. The consequence may therefore be handled by external software/programming procedures.

Case 04 later shows a different layer in which mapping, copy-forward, invalidation, and reclamation automate this problem while preserving stable logical identity.

### 2. Bulk erase speed is not the same thing as fine-grained rewrite latency

Masuoka's 1984 abstract emphasizes simultaneous erase; Kynett's 1988 abstract reports whole-array erase in hundreds of milliseconds while programming remains byte-by-byte.

Thus `fast bulk forgetting` must not be rewritten as `fast arbitrary overwrite`.

### 3. Coarse physical erase can coexist with fine-grained verification

Intel's 1988 patent verifies erased state by walking addresses after a bulk erase pulse and repeats erase when verification fails.

Therefore:

```text
physical erase domain
    !=
verification / diagnostic granularity
```

A maintenance operation can change state collectively yet validate success locally.

### 4. In-system alterability does not determine erase granularity

Case 12 already showed an in-system electrically erasable Intel 2816 with byte erase. Case 13 shows a period Flash regime with in-system electrical program/erase but whole-array erase.

Therefore:

```text
in-system electrical control
    !=
byte-level forgetting authority
```

## Cross-case controls added by this record

1. **program addressability ≠ erase addressability**;
2. **electrical erasability ≠ fine-grained erasability**;
3. **one-transistor density objective can be coupled to shared/coarser erase infrastructure in a bounded historical design without becoming a universal law**;
4. **bulk erase speed ≠ arbitrary rewrite speed**;
5. **coarse physical state change ≠ coarse verification granularity**;
6. **Flash erase geometry creates the device-level precondition for later copy/reclaim/remap machinery but does not itself imply an FTL**.

## Promotion decision

Case 13 is `grounded` because its central mechanism claims no longer depend on a tertiary history or on an uninspected conference figure:

- Toshiba's 1980-priority manufacturer patent directly establishes the density pressure, one-transistor electrically erasable cell, shared erase infrastructure, and distinct program/read/erase paths;
- Masuoka et al. 1984 supplies period `Flash` vocabulary and whole-array simultaneous erase at the abstract level;
- Intel's 1988-filed manufacturer patent directly establishes a one-transistor 32K × 8 Flash design with whole-array simultaneous electrical erase, addressed programming, command control, and iterative verification;
- Kynett et al. 1988 independently supplies peer-reviewed abstract-level timing and granularity corroboration;
- Lai 2023 is kept in the secondary/retrospective layer.

Remaining archival cleanup:

- obtain directly renderable full facsimiles of Masuoka et al. 1984 IEDM pp. 464–467 and Kynett et al. 1988 JSSC pp. 1157–1163;
- if a named commercial Intel/Toshiba product is later attached to this case, ground that identity with manufacturer datasheets rather than inference from matching capacity/timing;
- treat sector erase, NAND page/block geometry, and SSD controller policies as separate later regimes rather than folding them backward into this whole-array case.
