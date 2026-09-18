# Case 04 Deepening — Masuoka et al. 1987 IEDM NAND Direct-Facsimile Inspection

**Status:** `bounded deepening complete`

**Canonical case:** [`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md)

**Parent device-history evidence:** [`04-1987-1989-nand-device-geometry-before-ftl-deepening.md`](04-1987-1989-nand-device-geometry-before-ftl-deepening.md)

**Patent-side chronology:** [`04-toshiba-1987-series-cell-nand-patent-chronology-deepening.md`](04-toshiba-1987-series-cell-nand-patent-chronology-deepening.md)

## Question

The parent 1987–1989 device-history record deliberately stopped at an abstract-level treatment of the 1987 IEDM paper and left one explicit evidence debt:

> directly inspect a renderable full copy of Fujio Masuoka, Masaki Momodomi, Yoshihisa Iwata, and Riichiro Shirota, `New Ultra High Density EPROM and Flash EEPROM with NAND Structure Cell`, IEDM 1987, pp. 552–555.

A four-page facsimile is now directly inspectable. This slice closes that narrow debt and asks only what the full paper itself adds to the retention boundary between:

```text
NAND device / string geometry
    !=
device-level program, read, erase, and disturbance behavior
    !=
later logical-to-physical translation / FTL semantics
```

It does **not** turn Case 04 into a general history of NAND Flash or settle invention priority, commercial shipment chronology, or later controller genealogy.

---

## Related-repository check

A fresh search of `tmzncty/computing-archaeology` for the exact 1987 title / NAND paper did not expose a dedicated reusable packet. The broad semiconductor-memory history therefore remains outside this repository. This file retains only the direct-facsimile facts needed to stop later FTL vocabulary from being projected backward onto a 1987 device paper.

---

## Source custody

### Primary paper facsimile inspected

Fujio Masuoka, Masaki Momodomi, Yoshihisa Iwata, and Riichiro Shirota, **“New Ultra High Density EPROM and Flash EEPROM with NAND Structure Cell,”** *International Electron Devices Meeting Technical Digest*, 1987, pp. 552–555, DOI `10.1109/IEDM.1987.191485`.

Directly inspected facsimile:

- https://rust-class.org/static/classes/class17/nandflash.pdf

Independent bibliographic / abstract corroboration:

- https://scholar.nycu.edu.tw/en/publications/new-ultra-high-density-eprom-and-flash-eeprom-with-nand-structure/
- https://ndlsearch.ndl.go.jp/books/R100000136-I1574231875756379520

### Custody qualification

The directly inspectable PDF is served by a third-party educational mirror rather than an IEEE-controlled host. The file nevertheless visibly carries the 1987 IEEE copyright line, the IEDM page markers `552` through `555`, the same title and Toshiba authors, and the conference paper number / pagination matching the independently corroborated bibliographic record.

Therefore this evidence uses the mirror as a **directly inspected facsimile copy of the paper**, while avoiding the stronger claim that the mirror itself supplies official archival custody.

---

# Historical record

## H1 — The paper presents NAND first as a density / cell-organization proposal

The abstract and introduction state the immediate problem in device terms: conventional EPROM scaling was increasingly constrained by contact-hole size and spacing, so the authors proposed a NAND structure that could reduce cell area without simply shrinking all device dimensions.

The paper reports a cell area of **6.43 µm² per bit under a 1.0-µm design rule**, described as about **30% smaller per bit** than the compared conventional 4-Mbit EPROM structure using the same design rule.

This is a physical-layout / density claim. The paper does not describe a host-visible logical block address, a translation table, garbage collection, or out-of-place update policy.

## H2 — The inspected array is a four-bit serial NAND cell

On p. 552 the paper states that the demonstrated NAND structure cell has **four bits** and that the bits are arranged **in series**. Figure 1 shows the layout, an equivalent series circuit with four cells, and a conventional comparison cell. Figure 2 then plots occupied area per bit as the number of serially connected bits increases.

The paper explains the density advantage through reduced contact overhead: the conventional comparison uses repeated contact area, while the NAND arrangement shares contact structure across the serial cell unit.

Thus the full paper directly grounds:

```text
serial physical cell organization
    -> shared current path / reduced contact overhead
    -> density advantage
```

It does not yet ground:

```text
stable logical identity
    -> remapped current physical page
```

## H3 — Selective programming is explained through different operating regimes inside one string

The full text adds substantially more than the abstract-level statement that one bit can be programmed selectively.

For the demonstrated programming mode, the paper states that approximately:

- `9 V` is applied to the bit line;
- `10 V` is applied to the selected word line;
- `20 V` is applied to the three unselected word lines in the four-bit NAND cell.

The authors explain the selectivity by operating the selected bit in saturation so that channel hot electrons are generated, while the unselected bits are driven in deep-triode operation and therefore do not generate the same hot-electron programming condition.

This is a device-level program-isolation mechanism, not a mapping policy.

## H4 — The experiments test selected-bit programming against already-erased and already-written neighbors

Figures 4 and 5 are especially useful for the retention boundary.

In one experiment all four bits begin erased and one selected bit is programmed. The paper reports that the selected bit is written while the three unselected bits are not written.

In the second arrangement, the selected bit begins erased while the other three bits are already in the written state. The selected bit is then programmed while the threshold voltages of the three unselected bits remain at their initial values.

The paper further reports that after sequential programming of the four-bit NAND cell, the threshold windows remain larger than `2 V` in the plotted experiment.

A safe historical statement is therefore:

> the 1987 paper does not merely propose serial geometry; it experimentally treats preservation of non-target threshold states during selected / sequential programming as part of demonstrating the new cell.

This remains bounded to the reported four-bit device and test conditions.

## H5 — Readout is a string-level electrical path but the addressed bit determines the observed current

The read description applies about `1 V` to the bit line, a lower control voltage to the selected word line, and a higher voltage to the unselected word lines. Under that condition, the selected bit conducts when it is in the erased state and blocks current when it is in the written state.

The full paper therefore makes the distinction visible between:

```text
shared serial read path
    !=
all cells interpreted as one logical bit
```

The string is electrically shared, but the operation is organized to interrogate one addressed cell state while biasing the other cells into a pass condition.

## H6 — The paper contains a bounded read-retention / disturbance result

The reliability section states that the authors observed **no threshold shift during read operation in any bit of the NAND cell** in their reported read-retention test. The plotted read-retention figure spans approximately `1` to `10^4` seconds on its horizontal axis and shows the four cell thresholds remaining close to their initial levels over that test range.

The prose then says that data retention of the NAND cell is the same as the compared contemporary EPROM because each bit uses the same cell structure.

Two qualifications are important:

1. the paper's prose refers to a figure number that does not match the figure number printed under the surviving plotted graphic (`Fig.10` in prose versus `Fig.8` under the plot); this record does not silently “correct” the source;
2. this is a bounded 1987 device experiment, not a universal guarantee of immunity to all later-known forms of NAND read disturb, retention loss, cycling damage, temperature acceleration, or scaled-device behavior.

## H7 — The conclusion still places Flash-EEPROM behind an additional erase structure

The conclusion states that the developed NAND structure allows individual bits to be programmed and read separately, and says that a Flash-EEPROM using the NAND array can be realized by adding an extra erase gate.

That wording is useful because the paper itself is not yet a modern managed-NAND storage architecture. It is discussing how the cell structure can support EPROM / Flash-EEPROM device construction.

---

# Engineering reconstruction

## E1 — Physical sharing and logical selectivity are simultaneous properties

The full paper gives a compact counterexample to the intuition that shared physical organization necessarily destroys cell-level selectivity.

```text
four cells share a serial current path
    +
word-line bias distinguishes selected from unselected cells
    ->
selected program / selected read can remain operationally separable
```

This is a device-level relation. It does not require a translation table or a stable host-visible sector identity.

## E2 — “Selective program” is already a retention claim about non-target state, but only at the device layer

To establish useful selected programming, the experiment must show more than “the target threshold changed.” It must also show that non-target states remained sufficiently unchanged under the tested program sequence.

That yields a bounded retention relation:

```text
target state intentionally changed
    +
non-target threshold states remain within the demonstrated window
    ->
selected programming succeeds for the tested string
```

The relevant retained states are floating-gate threshold states inside one NAND string. They are not FTL mappings, logical-sector versions, or SSD metadata.

## E3 — Shared operation geometry does not itself supply currentness / authority semantics

The direct facsimile strengthens the physical-device side of the chronology but leaves the mapped-storage boundary intact.

Nothing in the inspected paper defines:

- a logical-to-physical address table;
- a rule selecting one physical copy as the current version of a logical address;
- invalid / obsolete page metadata;
- reclaim selection;
- copying of still-current pages before erase;
- wear-level policy;
- host discard / TRIM;
- SSD controller recovery semantics.

Therefore:

```text
NAND cell / string selectivity
    !=
logical embodiment authority
```

## E4 — Read-disturb evidence must be scoped to the tested regime

The 1987 result is a useful negative witness: under the reported read-retention experiment, the authors did not observe threshold shift in the four NAND-cell bits.

But it cannot support:

```text
1987 reported no shift
    ->
NAND read disturb does not exist
```

The correct reconstruction is:

```text
one tested cell structure + one tested read-bias regime + one reported interval
    -> bounded evidence of state preservation under those conditions
```

Later NAND technologies, dimensions, voltages, program states, cycling histories, and read counts require separate evidence.

## E5 — A device paper can expose constraints that later FTLs must live with without containing the FTL abstraction

The stronger full-text record makes the historical layering clearer rather than weaker:

```text
1987 device layer
serial cells + shared path + selected biasing + measured threshold behavior

later mapped-storage layer
stable logical name + mapping/currentness metadata + out-of-place replacement + reclamation
```

The first layer supplies physical constraints. The second adds a different retained relation: which physical embodiment currently counts for a stable logical identity.

Constraint is not genealogy, and physical necessity is not evidence that the later abstraction was already formulated.

---

# Functional analogy

A narrow analogy to later NAND / SSD disturbance-management work is legitimate only at the level of **target versus non-target state preservation**:

```text
one operation intentionally changes / interrogates a target
while neighboring or unselected states must remain serviceable
```

That functional similarity does **not** establish one unchanged mechanism from the 1987 four-bit NAND cell to modern planar MLC/TLC, 3D NAND, read-retry, read reclaim, refresh, or controller-level disturbance management.

Likewise, the paper's serial NAND arrangement can be compared functionally with later shared-resource storage geometries, but not treated as historical evidence for later FTL or SSD policies.

---

# Philosophical interpretation

The direct facsimile sharpens one modest point already latent in Case 04:

> physical persistence is relational to an operation regime, not merely a material adjective attached to an isolated bit.

The stored threshold state of one floating-gate cell is physically embodied in that cell, yet whether it remains usable during access depends on how the selected and unselected members of the shared string are biased.

This does not make the 1987 NAND cell an example of “distributed identity,” nor does it collapse it into later mapped Flash. The conceptual lesson is narrower: **a retained state can depend on surrounding operation geometry even before any logical-remapping layer exists.**

This interpretation is project vocabulary, not language attributed to Masuoka, Momodomi, Iwata, or Shirota.

---

# Prior-art / anti-anachronism boundaries

The direct facsimile closes the parent record's full-paper inspection debt, but it does **not** establish any of the following:

- that this paper is the uncontested first invention of NAND memory;
- that the paper date is a first commercial shipment date;
- that the third-party mirror is the official IEEE archival copy;
- that every numerical bias is a universal NAND voltage rather than a value for the demonstrated device;
- that the four-bit demonstrated string is the geometry of all later NAND products;
- that the paper's bounded read-retention test proves indefinite shelf retention;
- that the paper proves immunity to later-known read disturb;
- that selected-bit programming under the tested conditions proves zero disturbance under every program/cycling condition;
- that `read retention` in this paper is interchangeable with later SSD retention specifications;
- that serial NAND geometry is already an FTL;
- that block erase is already garbage collection;
- that page programming is already out-of-place remapping;
- that selective programming establishes stable logical identity across relocation;
- that the 1987 Toshiba paper directly caused the 1992–1995 mapping / FTL line;
- that contemporaneous Toshiba patents and this IEDM circuit are bit-for-bit identical without an explicit cross-document proof;
- that later controller policies can be inferred from the 1987 cell paper.

---

# Resulting bounded distinctions

```text
full 1987 NAND device paper
    !=
later mapped-Flash / FTL architecture

serial physical organization
    !=
logical address translation

shared current path
    !=
absence of cell-level selectivity

selected program success
    !=
proof of zero non-target disturbance under all conditions

reported no threshold shift in one read-retention test
    !=
universal read-disturb immunity

physical operation constraint
    !=
controller policy

historical precedence
    !=
demonstrated actor-to-actor genealogy
```

---

# What this closes

The parent `04-1987-1989-nand-device-geometry-before-ftl-deepening.md` previously carried an explicit source-custody / evidence debt because only the 1987 bibliographic record and reproduced abstract were directly available.

This slice closes that debt at the **page-level facsimile inspection** level:

- all four paper pages were directly inspected;
- the serial four-bit geometry is visible in the paper and Figure 1;
- the selected/unselected programming mechanism is described in the text;
- Figures 4–6 provide the reported selected / sequential programming threshold behavior;
- the read path and the reported read-retention result are directly visible;
- the conclusion's EPROM / Flash-EEPROM scope is directly visible.

The evidence gain is not “we now know NAND had an FTL in 1987.” It is the opposite: the stronger primary record lets the repository define the device / later-translation boundary with greater confidence.

---

# Remaining work

Still open, but no longer part of the direct-facsimile debt:

- page-level inspection of selected 1988–1989 Toshiba papers where exact circuit wording matters;
- earlier NAND-string / serial nonvolatile-cell genealogy beyond the already bounded 1987 patent slice;
- commercial-shipment chronology;
- direct citation / influence genealogy between the early Toshiba device work and later mapping / FTL actors;
- later disturbance, refresh, bad-block, ECC, wear-leveling, and garbage-collection history only where a separate retention question requires it;
- reproduction or electrical characterization of the 1987 device is outside this documentary slice.

Broader semiconductor-memory history remains primarily `computing-archaeology` work.
