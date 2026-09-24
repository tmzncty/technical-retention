# Case 09 deepening — Hyundai HY534256 powered-clockless bias and reinitialization

## Scope

This packet deepens [`../cases/09-dram-cbr-refresh-address-internalization.md`](../cases/09-dram-cbr-refresh-address-internalization.md) at one narrow boundary:

> **If a DRAM remains electrically biased but receives no qualifying row clocks for longer than its refresh interval, does continued power alone leave the device in a state that the vendor treats as immediately ready for normal use?**

The bounded witness is Hyundai Electronics Industries' January-1992 documentation for the `HY534256`, a 262,144 × 4-bit CMOS DRAM with RAS-only, hidden, and CAS-before-RAS refresh modes.

The result is deliberately narrower than a general DRAM initialization theory. The product documentation says that eight initialization cycles are required not only after power application, but also after an extended period of bias without clocks greater than the refresh interval. That establishes a **powered-but-maintenance-interrupted reinitialization boundary** for this named device. It does not expose the exact hidden state that motivates the rule, does not prove a particular normal-mode refresh-counter reset value, and does not imply that initialization reconstructs payload data that have already leaked away.

Case 09 remains **`grounded`**. This packet does not justify a maturity promotion.

---

## Source custody and evidence class

### Hyundai product documentation

The primary source is Hyundai Electronics Industries' HY534256 product documentation preserved in the 1992 *Hyundai Semiconductor Data Book*. The device sheet identifies itself as `HY534256 256K × 4-Bit CMOS DRAM`, revision marker `M181202B-JAN92`.

The source is manufacturer-primary technical documentation preserved by third-party archives. The principal archived copy used for this packet is:

- Hyundai Electronics Industries, *1992 Hyundai Semiconductor Data Book*, HY534256 section, archived by Bitsavers: <https://www.bitsavers.org/components/hyundai/1992_Hyundai_Semiconductor_Data_Book.pdf>.

A page-extracted facsimile is also available at:

- <https://www.ardent-tool.com/datasheets/Hyundai_HY534256.pdf>.

Third-party custody does not turn the document into independent validation; claims below remain bounded to Hyundai's published product contract.

### Why this source is useful

Most of Case 09 concerns where refresh cadence, row enumeration, and refresh-address authority live. The HY534256 adds a different seam: **what happens to the device's operational qualification when power remains present but the qualifying clocked maintenance regime is interrupted beyond the refresh interval.**

That is useful because it prevents an overly coarse two-state model in which only `powered` and `unpowered` matter.

---

## Historical / source record

### H/P — the HY534256 has an explicit refresh obligation

The HY534256 feature summary specifies `512 refresh cycles/8 ms`.

The refresh section states that, to retain data, 512 RAS refresh cycles are required in an 8 ms period. It gives two relevant ways to satisfy that requirement:

1. present each of the 512 row addresses externally while clocking RAS through qualifying cycles; or
2. use CAS-before-RAS refresh, in which the device ignores the external address inputs and uses an internal nine-bit counter as the source of the row address.

Thus the product contract itself separates:

```text
continued electrical bias
    from
periodic restorative row activity
```

Power is necessary for this operating regime, but the documentation still requires refresh activity within a finite interval.

### H/P — power-up requires pause plus initialization cycles

Under `POWER ON`, Hyundai specifies an initial pause of 200 microseconds after application of the VDD supply, followed by at least eight initialization cycles.

The documentation says those initialization cycles can be any combination of cycles containing a RAS clock, and gives RAS-only refresh as an example.

The source therefore does not define initialization as eight ordinary payload reads or writes. The common requirement is qualifying RAS-clocked activity.

### H/P — the same initialization obligation reappears without a power loss

The same `POWER ON` note contains the key sentence for this packet: eight initialization cycles are required after **extended periods of bias without clocks**, with the parenthetical condition `greater than the refresh interval`.

This is the central historical fact.

The source explicitly describes a case in which:

```text
bias remains present
    + clocks are absent beyond the refresh interval
    -> eight initialization cycles required
```

It therefore blocks the shortcut:

> **VDD continuously present != vendor-documented immediate operational qualification after an overlong clockless interval.**

The source does not say that VDD was removed and restored. The boundary is explicitly about prolonged bias **without clocks**.

### H/P — CBR row selection is internal, but recurrence still depends on external activity

For CAS-before-RAS refresh, Hyundai says an internal nine-bit counter supplies the row address and the external address inputs are ignored.

This is consistent with the central Case 09 partition:

```text
row enumeration authority
    can be internal
while
refresh-event recurrence
    still depends on qualifying interface activity
```

The HY534256 evidence therefore does not turn CBR into an autonomous self-refresh regime. It documents internal row enumeration under an externally exercised refresh mode.

---

## Engineering reconstruction

The terminology in this section is repository analysis, not Hyundai's historical vocabulary.

### E — power continuity and maintenance continuity are separate predicates

For this bounded product, the control relation can be reconstructed as:

```text
VDD present
    != refresh obligation satisfied

VDD present continuously
    != qualifying row-clock activity continuous

qualifying row-clock activity interrupted > refresh interval
    -> vendor requires reinitialization cycles
```

A useful project-level term for the seam is **powered-bias requalification boundary**: the device can remain biased while the documented conditions for immediate normal operation must nevertheless be re-established.

This is not a claim that Hyundai used the term `requalification`, nor that one hidden latch is known to lose state at exactly this boundary.

### E — maintenance-control qualification is distinct from payload retention

The eight required initialization cycles should not be collapsed into data restoration.

The same sheet separately states that maintaining payload requires 512 refresh cycles per 8 ms. Eight initialization cycles are therefore not equivalent to a full 512-row refresh traversal.

So:

```text
8 initialization cycles
    != 512-row refresh coverage
    != reconstruction of already-lost payload
```

If a row's stored charge has decayed past the device's valid retention envelope, the documentation does not say that initialization can infer or recreate its previous logical value.

This yields a four-way separation:

```text
power continuity
    != maintenance continuity
    != control-state qualification
    != payload recovery
```

### E — a maintenance interruption can matter even when the gross power epoch does not change

A common persistence model treats power removal as the important boundary. The HY534256 note demonstrates a finer operational partition: **continued power can coexist with loss of the refresh regime that the product contract expects**.

For this device, therefore:

```text
same gross powered interval
    can contain
multiple maintenance-qualified / maintenance-interrupted sub-regimes
```

That does not prove that every internal state is reset after an 8 ms clockless interval. It proves that the vendor requires the initialization procedure again.

### E — hidden maintenance state should not be over-specified from an external initialization rule

The source does not identify which internal node or nodes make the eight-cycle sequence necessary after prolonged clocklessness. Possible internal mechanisms are not evidence.

Accordingly, this packet does **not** infer:

- that the normal CBR refresh counter is forced to zero;
- that it retains its prior count;
- that it becomes indeterminate in one particular digital sense;
- that all eight cycles are consumed solely by the refresh counter;
- that the product's power-up initialization and powered-clockless reinitialization have an identical transistor-level cause.

The correct engineering statement is interface-level:

> **the published product contract requires an initialization sequence after this maintenance interruption.**

### E — the parenthetical threshold should be kept source-bounded

Hyundai says the relevant clockless interval is `greater than the refresh interval`. For the ordinary HY534256 feature table, the documented refresh relation is 512 cycles per 8 ms.

That supports a product-level relation between the maintenance deadline and the reinitialization rule. It does not establish an analog cliff at exactly one mathematical instant, and this packet does not claim that every stored bit necessarily fails immediately after 8 ms.

The distinction is:

```text
vendor-specified operational boundary
    != deterministic physical failure instant for every cell
```

---

## Anti-collapse ledger

The following shortcuts are explicitly rejected.

| Shortcut | Status | Why |
| --- | --- | --- |
| `powered == refreshed` | rejected | refresh activity is separately required |
| `powered continuously == continuously qualified` | rejected for this named product | Hyundai requires reinitialization after overlong clockless bias |
| `8 initialization cycles == full-array refresh` | rejected | full coverage is documented as 512 refresh cycles |
| `initialization == payload repair` | rejected | no source says initialization reconstructs lost logical contents |
| `CBR internal counter == autonomous refresh scheduler` | rejected | CBR supplies internal row enumeration under externally exercised timing |
| `clockless interval > refresh interval == all data definitely lost` | rejected | interface requirement does not specify per-cell failure instant |
| `reinitialization rule == proof of counter reset-to-zero` | rejected | hidden normal-mode counter state is not exposed by this rule |
| `test-mode counter semantics == normal-mode power/bias semantics` | rejected | no source binds them here |
| `HY534256 behavior == all asynchronous DRAM behavior` | rejected | evidence is device-specific |
| `power-up cause == powered-clockless cause` | rejected | same prescribed procedure does not prove identical internal cause |

---

## Relation to existing Case 09 evidence

### TI / Motorola counter-initialization packet

[`09-dram-refresh-counter-initialization-test-deepening.md`](09-dram-refresh-counter-initialization-test-deepening.md) establishes two different source-bounded facts:

- TI disclosed a CBR refresh-counter embodiment with an explicit power-on-zero phase;
- Motorola exposed a commercial CBR refresh-counter test and required prior initialization cycles.

The HY534256 packet adds a different boundary. It does **not** identify Hyundai's normal counter starting value. Instead it shows that a named commercial DRAM requires initialization again after an overlong **powered** clockless interval.

Therefore:

```text
known power-on counter value in one disclosed TI design
    != universal DRAM counter initialization semantics

vendor-required reinitialization in Hyundai product
    != proof of Hyundai's hidden counter value
```

### Micron 1999 AUTO REFRESH / SELF REFRESH packet

[`09-micron-1999-sdram-auto-vs-self-refresh-deepening.md`](09-micron-1999-sdram-auto-vs-self-refresh-deepening.md) supplies a later control-partition contrast in which a SELF REFRESH mode can move recurring refresh timing onto the SDRAM after mode entry.

The HY534256 witness is intentionally earlier and different: its CBR mode internalizes row enumeration, while refresh recurrence still depends on external clocked activity.

The comparison is functional only. It is not a Hyundai-to-Micron genealogy.

---

## Functional comparisons across cases

The comparisons below are repository-level analogies, not historical influence claims.

### A — Case 04 Flash: physical operation and reuse qualification are different gates

Case 04 now shows a Linux FTL path in which successful erase is followed by metadata preparation before a transfer unit becomes an eligible relocation destination.

The shared abstraction is limited but useful:

```text
physical substrate condition
    != control-layer eligibility for the next regime
```

For HY534256, continued bias is not itself the vendor's sufficient condition for immediate post-interruption operation; qualifying cycles are required. For the FTL, erased media are not yet a prepared transfer unit.

The mechanisms and persistence horizons are otherwise unrelated.

### A — Case 38 SSD PLI: maintenance execution and maintenance qualification remain separate

Case 38 distinguishes configured PLI maintenance policy, self-test execution, and health/readiness evidence. HY534256 makes an older, much smaller-scale version of the same anti-collapse useful:

```text
maintenance-supporting resource exists
    != maintenance is occurring correctly
    != current operational qualification is established
```

No DRAM-to-SSD genealogy is claimed.

### A — Case 101 BMS: a power epoch is not always the only useful maintenance epoch

Case 101's SCSI background-medium-scan evidence distinguishes current power-epoch observability from maintenance history. HY534256 adds a complementary warning: even **within one continued-power interval**, maintenance can be interrupted long enough that the device requires a new initialization sequence.

Thus `power epoch` and `maintenance-qualified epoch` need not be identical analytical partitions.

---

## Philosophical interpretation

### I — persistence is not equivalent to mere continued energization

The technical record is narrow: Hyundai requires recurring refresh to retain payload, and requires eight initialization cycles after a sufficiently long clockless interval even if the device remained biased.

A restrained project-level interpretation follows:

> **For a maintained dynamic state, continued existence of the substrate or continued supply of energy is not identical to continuity of the maintenance relation that makes the information usable as current state.**

The important word is `relation`: power, timing, row coverage, initialization, and sense/restore activity jointly constitute the operating retention regime.

This is an interpretation, not Hyundai's historical statement, and it should not be turned into a universal metaphysics of memory.

---

## Claim ledger

| Claim | Label | Evidence |
| --- | --- | --- |
| HY534256 is a 262,144 × 4-bit CMOS DRAM | `H/P` | Hyundai 1992 product sheet |
| HY534256 specifies 512 refresh cycles per 8 ms | `H/P` | Hyundai feature summary and refresh section |
| CBR refresh uses an internal nine-bit row counter and ignores external row addresses | `H/P` | Hyundai refresh-cycle description |
| Power-up requires 200 µs pause plus at least eight RAS-bearing initialization cycles | `H/P` | Hyundai `POWER ON` note |
| Eight initialization cycles are also required after bias without clocks for longer than the refresh interval | `H/P` | Hyundai `POWER ON` note |
| Continuous VDD therefore proves continuous maintenance qualification | `X` | contradicted by the powered-clockless reinitialization rule |
| Eight initialization cycles refresh the entire array | `X` | contradicted by the separate 512-cycle coverage contract |
| Eight initialization cycles restore logical payload that has already decayed | `X` | unsupported |
| Hyundai's CBR counter is proven to reset to zero after the clockless interval | `X` | hidden state not specified |
| The device has a powered-bias requalification boundary | `E` | project reconstruction of the documented interface rule |
| A power epoch and a maintenance-qualified epoch can differ | `E` | bounded reconstruction from continued bias plus renewed initialization obligation |
| The HY534256 establishes behavior for all asynchronous DRAMs | `X` | device-specific evidence only |
| Flash/SSD/SCSI cases share a historical lineage with this rule | `A/X` | functional comparison only; no genealogy established |

---

## Remaining evidence debt

The highest-value next questions are deliberately narrow:

1. find another named late-1980s/early-1990s DRAM vendor product that explicitly states initialization after extended bias without clocks, to determine whether this was a broad product-contract pattern rather than a Hyundai-only wording;
2. find a vendor source that binds the powered-clockless reinitialization rule to a specific internal circuit state, if one exists;
3. construct a real-device trace with preserved VDD and a clockless interval swept across the documented refresh boundary, while separately checking payload retention and CBR counter-test behavior;
4. keep normal-mode counter initialization distinct from diagnostic counter-test semantics;
5. leave broad asynchronous-DRAM initialization genealogy to `tmzncty/computing-archaeology` if that history is developed there.

A useful fault matrix would distinguish at least:

```text
VDD removed
VDD retained + clocks continue
VDD retained + clock gap < refresh interval
VDD retained + clock gap > refresh interval
```

and would observe separately:

```text
payload correctness
initialization-sequence requirement
CBR counter-test progression
normal access behavior
```

That would test the present interface-level reconstruction without assuming the hidden implementation in advance.

---

## Sources

1. Hyundai Electronics Industries, `HY534256 256K × 4-Bit CMOS DRAM`, revision marker `M181202B-JAN92`, in *1992 Hyundai Semiconductor Data Book*, especially the feature summary, `REFRESH CYCLE`, and `POWER ON` sections: <https://www.bitsavers.org/components/hyundai/1992_Hyundai_Semiconductor_Data_Book.pdf>.
2. Page-extracted archival facsimile of the same Hyundai device sheet: <https://www.ardent-tool.com/datasheets/Hyundai_HY534256.pdf>.

### Source-boundary note

The manufacturer document is used for the product-level refresh requirement, CBR address-source behavior, and the initialization rule after power-up and powered clocklessness. The archive hosts are custody paths only. No claim here depends on a third-party interpretation of the circuit.