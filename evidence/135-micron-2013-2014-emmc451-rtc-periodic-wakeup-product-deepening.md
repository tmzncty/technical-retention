# Case 135 deepening — Micron 2013–2014 e.MMC 4.51 RTC / PERIODIC_WAKEUP named-product witness

## Scope

This is a bounded product-level deepening for Case 135.

Question:

> Can the repository move from standards-level evidence that e.MMC 4.5/4.51 carried RTC-related maintenance support to a named Micron component whose own datasheet exposes both RTC capability and the `PERIODIC_WAKEUP` control state?

The answer is **yes for a 4.51-generation named Micron MCP**, with an important limit: the inspected datasheet is not yet a direct 4.5-device witness, and it does not reproduce the full `SET_TIME (CMD49)` protocol text.

The primary document is Micron's datasheet for:

- **MT29PZZZ4D4BKESK-18 W.94H**;
- a 162-ball MCP combining **4GB MLC e.MMC** with **4Gb x32 LPDDR2**;
- document `162ball_ps8210_80s_451_lpddr2_j94h.pdf`;
- initial revision **Rev. A — 10/13**;
- inspected revision **Rev. D — 05/14**.

The copy inspected here is hosted on NXP Community, but the document body is a Micron primary technical datasheet with Micron title, copyright, document code, revision history, part number, and product-specific tables.

Primary document mirror:

- Micron, *MLC e·MMC and Mobile LPDDR2 162-Ball MCP, MT29PZZZ4D4BKESK-18 W.94H*, Rev. D, May 2014: <https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/imx-processors/52186/2/162ball_ps8210_451_80s_pb_lpddr2_2e0e_j94h.pdf>

This slice does **not** claim:

- that this is the first e.MMC product with RTC support;
- that the part first shipped in October 2013;
- that e.MMC 4.51 introduced RTC or `PERIODIC_WAKEUP`;
- that every e.MMC 4.51 device implements the field identically;
- that a nonzero `PERIODIC_WAKEUP` value was factory enabled in this part;
- that RTC support by itself proves maintenance executed;
- that the product's e.MMC maintenance mechanism is the same as the LPDDR2 `SELF REFRESH` mechanism elsewhere in the same MCP datasheet;
- that the full `SET_TIME (CMD49)` semantics have been directly inspected in JESD84-B451 during this pass.

---

## Historical record

### H/P — named part, revision, and standard generation

The front page names the device **MT29PZZZ4D4BKESK-18 W.94H** and identifies it as a Micron MLC e.MMC + Mobile LPDDR2 162-ball MCP.

Under `e-MMC-Specific Features`, the datasheet states that the e.MMC side is **JEDEC/MMC standard version 4.51-compliant**.

The same front page lists **Real-time clock** among the e.MMC-specific features.

The revision history gives:

- Rev. A — 10/13 — initial release;
- Rev. B — 01/14;
- Rev. C — 03/14;
- Rev. D — 05/14.

Therefore the repository now has a **named Micron 4.51-generation component document** in the 2013–2014 interval, rather than only a later generic standard or vendor integration.

Boundary:

```text
named product datasheet dated 2013/2014
    !=
proven first shipment date
    !=
proven first implementation date
```

### H/P — RTC is a product-level feature, not only a standards-history label

The datasheet front page directly includes **Real-time clock** in the e.MMC-specific feature list.

That materially strengthens Case 135's chronology because earlier evidence had established that later JEDEC revision history assigns RTC-related support to the 4.41 -> 4.5 transition, but a standards revision does not by itself prove a particular named component exposed that capability.

For this Micron part:

```text
standards-era RTC capability
    ->
named component advertises RTC
```

The arrow is a product witness, not proof of invention origin or universal adoption.

### H/P — `PERIODIC_WAKEUP` exists as EXT_CSD byte 131 in the named part

In the product's `ECSD Register Field Parameters` table, Micron lists:

- Name: `Periodic wake-up`;
- Field: `PERIODIC_WAKEUP`;
- size: 1 byte;
- EXT_CSD byte: **[131]**;
- cell type: **R/W/E**;
- shown value: **00h**.

This is direct product-document evidence that the field exists in the named Micron e.MMC implementation.

It is stronger than simply saying the device is 4.51-compliant.

### H/P — the field's access class gives it a reset/power-cycle persistence horizon

The same Micron table defines `R/W/E` as:

> multiple writable, readable, with the value kept after a power cycle, assertion of `RST_n`, and any `CMD0` reset.

Therefore, for this datasheet's register model, `PERIODIC_WAKEUP[131]` is not merely a transient runtime bit. Its configured value is described as surviving the listed reset/power transitions.

This creates a retention-specific distinction:

```text
runtime wakeup event
    !=
retained wakeup-policy configuration
```

and, more narrowly:

```text
power cycle / RST_n / CMD0 reset
    does not imply
PERIODIC_WAKEUP policy value is cleared
```

The document does not establish the physical nonvolatile cell technology used to retain this EXT_CSD value.

### H/P — default/current table value `00h` must not be confused with unsupported capability

The product table shows `00h` for `PERIODIC_WAKEUP[131]`.

That does **not** erase the fact that the field is present and writable; equally, field presence does **not** prove that periodic wakeup is active in an arbitrary deployed device.

The safe product-level distinction is:

```text
field implemented
    !=
field configured nonzero
    !=
wakeup event occurred
    !=
maintenance completed
```

This matters because Case 135 is explicitly about the state chain around maintenance rather than treating one capability bit as completed retention work.

### H/P — `PERIODIC_WAKEUP` and BKOPS are adjacent but distinct control surfaces

The same EXT_CSD table separately lists:

- `BKOPS_START[164]` — manually start background operations;
- `BKOPS_EN[163]` — enable background-operations handshake;
- `PERIODIC_WAKEUP[131]` — periodic wake-up.

Their coexistence in the same named device is useful negative evidence against collapsing all maintenance-related state into one field.

At minimum, the product model exposes separate state for:

```text
periodic wakeup policy
    !=
background-operation enablement
    !=
manual background-operation start
```

This document alone does not prove the exact runtime causal relation among those fields for every maintenance sequence.

### H/P — the datasheet does not reproduce `SET_TIME (CMD49)` semantics

A search of the inspected Micron PDF finds no product-level prose entry for `CMD49` or `SET_TIME`.

Therefore this slice does **not** promote the following into a product-specific claim:

```text
this datasheet explicitly documents the full host time-update protocol
```

Instead the evidence boundary is:

```text
named product advertises RTC
+ named product exposes PERIODIC_WAKEUP[131]
+ named product defines persistence class of that field

but

exact SET_TIME/CMD49 transaction semantics
remain standards-level debt
```

This prevents a common evidence shortcut in which compliance with a standard is treated as though every normative clause had been directly reproduced and checked in the product datasheet.

---

## A useful same-package terminology trap

### H/P — the same MCP document also contains LPDDR2 `SELF REFRESH`

The inspected PDF is a multichip-package datasheet: one package contains a managed e.MMC device and an LPDDR2 device with separate interfaces and power domains.

Later in the same document, the LPDDR2 section has a heading **`SELF REFRESH Operation`** and describes DRAM array retention without external clocking while the DRAM remains in self-refresh mode.

That mechanism belongs to the **LPDDR2 component**, not to the e.MMC RTC / `PERIODIC_WAKEUP` control surface.

The document therefore contains, within one physical package and one datasheet, two retention vocabularies that must not be merged:

```text
e.MMC:
RTC + PERIODIC_WAKEUP + BKOPS-related control state

LPDDR2:
SELF REFRESH command + internal DRAM refresh operation
```

This is a particularly strong anti-collapse witness because the ambiguity is not caused by comparing distant vendors or decades. It occurs inside one Micron MCP document.

### Engineering reconstruction

The same-package evidence supports the reconstruction:

```text
shared package
    !=
shared retention mechanism

same English word "refresh"
    !=
same technical operation

same vendor
    !=
same controller / substrate / timing contract
```

The e.MMC side is managed nonvolatile Flash with controller-mediated maintenance interfaces. The LPDDR2 side is volatile DRAM whose self-refresh operation maintains array state under a different electrical and protocol regime.

No genealogy is inferred between them.

---

## Engineering reconstruction

### E — maintenance policy can have a longer persistence horizon than one execution episode

Because `PERIODIC_WAKEUP[131]` is typed `R/W/E` in this product and `R/W/E` is defined to survive power cycle, `RST_n`, and `CMD0`, the configured wakeup policy can outlive one boot/reset episode.

That supports a bounded control-state decomposition:

```text
retained policy configuration
    ↓
future wakeup opportunity
    ↓
possible maintenance admission
    ↓
possible maintenance execution
    ↓
possible completion
```

The source directly supports the first persistence relation and the field existence. The later arrows remain dependent on standards/device runtime semantics and must not be inferred merely from the register table.

### E — policy persistence is not evidence of payload renewal

A persisted `PERIODIC_WAKEUP` value can survive while no relevant maintenance event has yet run.

Therefore:

```text
policy survived reset
    !=
payload was refreshed during reset
```

and:

```text
control state is durable enough to schedule work later
    !=
the work is already durable/completed
```

This is exactly the kind of second-order retention distinction Case 135 is intended to expose.

### E — capability, configuration, event, and completion need separate evidence

For this named part, four levels should remain separate:

1. **capability** — RTC and `PERIODIC_WAKEUP` are exposed by the product document;
2. **configuration** — the field has a writable retained value;
3. **event** — a wakeup/maintenance opportunity actually occurs;
4. **completion** — background or refresh work reaches its completion condition.

Only the first two are directly established by this datasheet slice.

### E — a register persistence class is not a complete crash-consistency model

The `R/W/E` definition specifies value retention across listed reset/power transitions. It does not by itself specify:

- atomicity if power fails while the field is being changed;
- ordering relative to other EXT_CSD writes;
- how firmware internally mirrors or journals the setting;
- whether a partially completed maintenance operation resumes;
- whether a wakeup that was due before power loss is remembered as an outstanding obligation.

Therefore:

```text
reset-surviving configuration
    !=
restart-surviving maintenance progress
```

and:

```text
persistent policy field
    !=
transactional persistence of all maintenance state
```

---

## Functional comparisons

### Case 03 — DRAM refresh control

The comparison is only functional:

- Case 03 studies cadence/traversal state used to make repeated DRAM restoration happen;
- this Case 135 slice exposes a managed-Flash wakeup-policy field that survives named reset/power transitions.

Useful relation:

```text
maintenance-control state can outlive one immediate operation
```

Rejected relation:

```text
e.MMC PERIODIC_WAKEUP == DRAM refresh counter
```

### Case 111 — enterprise SSD shutdown / refresh policy

Case 111 shows firmware/product-policy epochs and powered maintenance opportunity around SSD retention.

Case 135 adds a smaller product-level control-state witness:

```text
retained policy configuration
    !=
current media-condition evidence
    !=
completed renewal
```

No shared implementation lineage is claimed.

### Synthesis 26 — maintenance-control-state persistence horizons

This named product strengthens the synthesis with an unusually explicit field-level persistence class:

- `PERIODIC_WAKEUP` is not merely inferred to survive reset;
- the product table classifies it as `R/W/E`;
- the table separately defines the transitions across which the value is retained.

That makes it a useful concrete witness for:

```text
policy-state persistence horizon
    !=
maintenance-progress persistence horizon
```

---

## Philosophical interpretation

A narrow interpretation remains defensible:

> A system can retain not only data, but a rule for when future preservation work should become possible.

The product-level technical fact behind that statement is specific: Micron exposes a periodic-wakeup control value that its register model says survives named reset and power transitions.

The interpretation stops before claiming that the register is a memory of past maintenance, a history archive, or a guarantee that future maintenance succeeds.

---

## Claim ledger

| Claim | Layer | Strength | Boundary |
| --- | --- | --- | --- |
| MT29PZZZ4D4BKESK-18 W.94H is a named Micron 4GB e.MMC + 4Gb LPDDR2 MCP | Historical record | strong | product document, not shipment chronology |
| e.MMC side is documented as JEDEC/MMC 4.51-compliant | Historical record | strong | does not prove every normative clause was checked here |
| `Real-time clock` is listed as an e.MMC-specific feature | Historical record | strong | does not prove time was supplied in a given deployment |
| `PERIODIC_WAKEUP` exists at EXT_CSD[131] | Historical record | strong | named product table |
| `PERIODIC_WAKEUP` is typed `R/W/E` | Historical record | strong | named product table |
| `R/W/E` values are documented as retained across power cycle, `RST_n`, and `CMD0` reset | Historical record | strong | register-model persistence; physical embodiment unspecified |
| `00h` means feature absent | rejected | strong rejection | field exists and is writable; zero/default is not absence of capability |
| field presence proves a wakeup happened | rejected | strong rejection | capability/config/event must be separate |
| wakeup event proves maintenance completed | rejected | strong rejection | opportunity != completion |
| this PDF directly documents `SET_TIME (CMD49)` | rejected for this slice | strong rejection | exact command prose not found in inspected product PDF |
| LPDDR2 `SELF REFRESH` in same PDF is the e.MMC maintenance mechanism | rejected | strong rejection | different component and protocol domain |
| product-document date proves first shipment | rejected | strong rejection | no shipment record inspected |

---

## What this changes in Case 135

Before this slice, Case 135 had:

- standards-history evidence placing RTC support in the e.MMC 4.5 generation;
- an e.MMC 5.0 direct-clause floor for `SET_TIME` / RTC / periodic wakeup semantics;
- a much later Micron/Armadillo product integration for selective Self Refresh.

This slice inserts a product-level bridge:

```text
2011 e.MMC 4.5
    standards-history RTC introduction floor
        ↓
2012 e.MMC 4.51
    intervening standards epoch
        ↓
Oct 2013 / May 2014 Micron MT29PZZZ4D4BKESK-18 W.94H
    named product document
    RTC advertised
    PERIODIC_WAKEUP[131] exposed
    R/W/E persistence class documented
        ↓
2021+ Armadillo/Micron automotive e.MMC 5.1 integration
    vendor-specific selective Self Refresh behavior
```

This does **not** close the remaining direct-B45/direct-B451 normative-text debt. It does, however, remove the need to treat product adoption as wholly hypothetical until the 2021 integration.

---

## Remaining debt after this slice

1. Directly inspect **JESD84-B45** clauses for RTC, `SET_TIME`, `PERIODIC_WAKEUP`, reset/default behavior, and maintenance sequencing.
2. Directly inspect **JESD84-B451** and compare exact semantics against B45 and B50.
3. Find a **named e.MMC 4.5 (not merely 4.51) component** whose own datasheet exposes RTC / periodic wakeup.
4. Find contemporaneous ordering/shipment or board/BOM evidence if a claim about actual 2011–2013 deployment is needed.
5. Determine the legal encodings/units of `PERIODIC_WAKEUP[131]` in B45/B451 and whether optionality/default behavior changed by B50.
6. Keep host-software archaeology out of this case unless it resolves one of the above control-state boundaries.

---

## Related repositories

A fresh search of `tmzncty/computing-archaeology` for `eMMC PERIODIC_WAKEUP RTC SET_TIME` returned no dedicated reusable module in this pass.

Broader e.MMC standard genealogy, controller-market history, Micron MCP product-line history, host-driver adoption, and mobile-platform deployment belong primarily in `computing-archaeology` if pursued. This file keeps only the retention-specific evidence about named-product RTC capability, retained wakeup-policy state, and the boundary between policy persistence and maintenance completion.
