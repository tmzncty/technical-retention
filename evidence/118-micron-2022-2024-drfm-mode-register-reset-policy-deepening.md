# Evidence 118 — Micron DDR5 DRFM mode-register policy lifetime across reset, 2022–2024

## Purpose

This evidence record deepens [`../cases/118-micron-ddr5-directed-refresh-management.md`](../cases/118-micron-ddr5-directed-refresh-management.md).

The existing Case 118 grounding establishes a product contract in which a sampled row address directs refresh toward a bounded set of physically adjacent neighboring rows, with BRC selecting the coverage bound. This record asks a narrower retention question:

> **What state says that DRFM is enabled and which BRC policy is in force, and what does the documented DDR5 reset/initialization contract require a controller to do if it wants a nondefault policy after reset?**

The bounded answer is useful because it separates three things that are easy to collapse:

```text
DRFM capability implemented by the device
    !=
current mode-register maintenance policy
    !=
controller/platform desired maintenance policy
```

The inspected records support a strong interface-level conclusion: Micron exposes DRFM enable and BRC selection as mode-register state; the documented reset/initialization path has defined defaults and requires mode-register writes for settings that must differ from those defaults. A controller that relies on a nondefault DRFM policy therefore has a **post-reset restoration obligation**.

This record does **not** claim that a particular internal latch is physically erased by RESET_n, does not establish array-data fate across reset, and does not experimentally observe a Micron part through a reset.

## Evidence classification

- **H/P** — historical record from a standard or manufacturer-authored technical document.
- **E** — engineering reconstruction constrained by those records.
- **A** — controlled functional comparison to other repository cases.
- **I** — philosophical interpretation kept separate from period terminology.
- **X** — explicitly unsupported or rejected stronger inference.

---

# 1. Historical record

## Source A — Micron DDR5 SDRAM Product Core Data Sheet, Rev. D, October 2022

### Identity and provenance

Manufacturer: **Micron Technology, Inc.**

Document:

- **DDR5 SDRAM Product Core Data Sheet**;
- document identifier shown in public copies: `CCM005-1684161373-23`;
- Rev. D, `10/2022`.

Publicly inspectable copies/extractions of the manufacturer-authored document include:

- Avnet-hosted Micron PDF: <https://www.avnet.com/wcm/connect/dacdfea7-999f-4ee0-b514-6f9e0bf68c6d/ddr5-sdram-core.pdf?MOD=AJPERES>
- public extraction preserving the Micron document identity and page text: <https://device.report/m/309f15b18a593d25adef0074731926b4d967dcc3e45cab62ed9eefb3a338666c.pdf>

The source is **manufacturer-primary in authorship**, while the inspected public copies are distributor/mirror hosted rather than a current Micron archive URL. That custody distinction is retained here.

### MR59 separates capability/status from host policy

The Micron core data sheet identifies **MR59** as the register for `DRFM, ARFM, RFM RAA Counter`.

The relevant fields are especially important for Case 118:

| Field | Access semantics in the Micron table | Documented meaning relevant here |
| --- | --- | --- |
| `MR59:OP[0]` | `SR/W` | Status Read reports whether DRFM is implemented; Host Write enables/disables DRFM |
| `MR59:OP[2:1]` | `R/W` | Bounded Refresh Configuration (BRC) |
| `MR59:OP[3]` | `R` in the core table | BRC support level |

For `MR59:OP[0]`, the table distinguishes two views of the same bit position:

- **Status Read**: `0b` = DRFM not implemented; `1b` = DRFM implemented.
- **Host Write**: `0b` = DRFM disabled (**default**); `1b` = DRFM enabled.

That is direct manufacturer evidence for:

```text
feature implemented
    !=
feature currently enabled by host policy
```

A device can report that the mechanism exists while the host-programmable enable state remains at its disabled default.

This is stronger than merely saying that DRFM is “optional.” The interface itself separates **capability/status** from **configuration**.

### MR59 gives BRC a defined default

The same table defines `MR59:OP[2:1]` as:

| `MR59:OP[2:1]` | BRC setting |
| --- | --- |
| `00b` | BRC2 (**default**) |
| `01b` | BRC3 |
| `10b` | BRC4 |
| `11b` | RFU |

Thus a controller that wants BRC3 or BRC4 is relying on a **nondefault mode-register policy**.

The core table also identifies a BRC support-level status field. That creates another useful split:

```text
which BRC choices the silicon supports
    !=
which BRC choice is currently selected
```

Support is a device capability statement; selection is a current control-state statement.

### Reset initialization with stable power

The same Micron core data sheet contains a section titled **Reset Initialization with Stable Power**.

Its initialization sequence says that, beginning at the configuration point after the required reset/training steps, **MRW commands must be issued to all mode registers that require nondefault settings**.

That sentence is the decisive lifetime boundary for this record.

The source does not need to say “MR59 is nonpersistent” in those words. It provides a more operational contract:

1. DDR5 has defined/default mode-register settings for reset/initialization;
2. a stable-power reset enters the documented initialization procedure;
3. settings that must differ from default are to be written again by the host.

For the DRFM fields above, Micron separately documents:

- host DRFM enable default = disabled;
- BRC default = BRC2.

Therefore, if platform policy requires **DRFM enabled** and/or **BRC3/BRC4**, that policy is not safely recoverable merely from the device's silicon capability. The host must re-establish the desired nondefault register state in the reset/initialization sequence.

Safe statement:

> **The documented interface contract does not permit software/firmware to assume that a nondefault MR59 maintenance policy survives RESET_n without reprogramming.**

This is intentionally narrower than claiming the physical implementation of every MR bit.

---

## Source B — JEDEC JESD79-5, DDR5 SDRAM, July 2020 public text copy

### Identity and custody

Document:

- **JEDEC Standard JESD79-5, DDR5 SDRAM**;
- July 2020.

Publicly inspectable text copy:

<https://studylib.net/doc/27820325/ddr5-spec-jesd79-5>

JEDEC's official site identifies JEDEC as the standards body for main memory / DDR SDRAM, but the historical standard text inspected for this record is a **public mirror copy**, not an authenticated download from the current JEDEC portal. Therefore this source is treated as **standards-authored text inspected through a secondary custody path**.

Official JEDEC document portal/home:

<https://www.jedec.org/>

### Default settings are part of reset/initialization semantics

The standard's `RESET and Initialization Procedure` states that power-up and reset initialization require defined defaults for mode-register settings and provides an MR default-settings table.

Its `Reset Initialization with Stable Power` procedure requires asserting `RESET_n`, then repeating the relevant initialization/configuration steps. The procedure explicitly says that MRW commands must be issued to mode registers requiring defined settings.

The important point for this case is not a specific analog implementation behind RESET_n. It is the **host-visible initialization contract**:

```text
reset
    -> initialization/configuration regime
    -> host re-establishes required MR settings
    -> normal operation
```

This standards text provides a broader protocol-level frame for Micron's 2022 manufacturer wording.

### What the 2020 source does and does not prove about DRFM

The July 2020 standard is used here for reset/mode-register lifetime semantics, **not** to claim that the exact later Micron DRFM/BRC product contract already existed unchanged in every 2020 device.

The historical layers therefore remain separate:

```text
2020 DDR5 reset/configuration framework
    !=
2022 Micron MR59 DRFM/BRC field contract
    !=
2024 Micron product-specific DRFM variance
```

The later records can operate within the earlier mode-register/reset framework without proving identity of every field across revisions.

---

## Source C — Micron 16Gb DDR5 SDRAM Die Rev D addendum, Rev. E, January 2024

### Identity and relation to existing Case 118 evidence

Manufacturer: **Micron Technology, Inc.**

Document:

- **16Gb DDR5 SDRAM Die Rev D**;
- document identifier `CCM005-1684161373-39`;
- Rev. E, `01/2024`.

Publicly inspectable extraction:

<https://device.report/m/79c9b0cad85e0bf0b889e0e3b5f5704f52b7b91c61a05a0b158e47c64f7ae743>

DigiKey-hosted manufacturer PDF copy:

<https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7969/16gb-ddr5-sdram-dierevd.pdf>

The product addendum is already the main grounding source for Case 118. This record reuses it only for the **capability/configuration boundary** and does not duplicate the existing physical-neighbor analysis.

### Function matrix: DRFM exists, but host-write enable defaults off

The product function matrix marks **Directed RFM** as supported. In the same row/field description it records:

- `MR59:OP[0] = 1 (SR)` for the status-read view;
- `MR59:OP[0] = 0 (W)` for the host-write/default configuration view;
- `MR59:OP[2:1] = 00 (R/W)` for BRC;
- the product supports BRC2/BRC3/BRC4 in its DRFM variance section.

Thus, on this named Micron 16Gb DDR5 product family:

```text
DRFM supported by the die
    !=
DRFM enabled in current host policy
```

and:

```text
BRC3/BRC4 supported
    !=
BRC3/BRC4 selected
```

The product-specific evidence prevents the reset-policy argument from floating at a generic JEDEC level only.

### Spatial policy changes service cost

The existing grounding already establishes that BRC2, BRC3, and BRC4 alter the bounded physical-neighbor scope and the corresponding `tDRFM` maintenance duration.

That matters to the present slice because MR59 is not just an arbitrary configuration byte. Re-establishing BRC after reset re-establishes a policy that changes:

- which physical-neighbor distance is included in the bounded DRFM operation;
- which farther rows are ratio-controlled;
- how much maintenance service time the command reserves.

So a lost/non-restored BRC policy is a change in the **maintenance contract**, not merely a cosmetic configuration mismatch.

---

# 2. Engineering reconstruction

The following statements are engineering reconstruction constrained by the sources above. They are not quotations from Micron or JEDEC.

## 2.1 Three retained-state layers must be kept distinct

For this product family, a robust model is:

```text
Layer A — device capability
    DRFM implemented?
    supported BRC choices?

Layer B — current device control state
    DRFM host-enable value
    selected BRC

Layer C — controller/platform policy
    what firmware intends to program after initialization
```

These layers can agree during normal operation but have different lifetime contracts.

The key retention relation is:

```text
capability survives as a property of the part
    !=
current nondefault control state may be assumed across reset
    !=
platform intent survives unless the controller retains/reconstructs it
```

The last line is intentionally architecture-level: the source does not tell us whether a BIOS constant, SPD-derived rule, firmware variable, policy table, or other mechanism supplies the intended value.

## 2.2 Reset creates a policy-restoration obligation

Suppose a platform operates with:

```text
DRFM enable = 1
BRC = BRC4
```

while the documented defaults are:

```text
host DRFM enable = 0
BRC = BRC2
```

After a RESET_n event that invokes the documented stable-power initialization procedure, the controller cannot safely reason:

```text
"the die still supports DRFM"
    ->
"therefore my prior enabled/BRC4 policy is still in force"
```

The documented procedure instead creates an obligation:

```text
reset/init transition
    ->
recover desired platform policy
    ->
issue required MRW(s)
    ->
re-establish nondefault MR59 state
    ->
resume operation under intended maintenance policy
```

Thus:

> **maintenance capability retention does not close maintenance-policy continuity.**

## 2.3 Default is a fallback configuration, not proof of desired policy

The presence of a defined default is valuable because reset has a known configuration baseline. But it creates a common inference trap:

```text
known default
    !=
known desired runtime policy
```

BRC2 is a valid documented default. That does not mean BRC2 is the platform's desired post-training policy on every system.

Likewise:

```text
DRFM disabled by default
    !=
DRFM unsupported
```

because the status-read view separately reports implementation capability.

## 2.4 Reset completion and maintenance-policy closure are different milestones

A system can satisfy the electrical/timing requirements of reset initialization while still needing to restore a platform-specific nondefault maintenance policy.

Therefore:

```text
RESET_n sequence completed
    !=
all desired nondefault maintenance policy restored
```

A more precise closure chain is:

```text
reset accepted
    -> initialization/training prerequisites satisfied
    -> required nondefault MR state restored
    -> maintenance policy active as intended
```

The source records do not provide a controller trace proving a real platform followed or violated that chain. The chain is a contract-level reconstruction.

## 2.5 Policy restoration is not payload restoration

This evidence slice concerns configuration controlling **future maintenance**. It does not establish what happened to DRAM payload bits across the reset event.

Keep separate:

```text
payload state
    !=
maintenance-policy state
```

and:

```text
payload retained
    !=
future maintenance policy correctly restored
```

A platform can have a control-plane error even if the array contents have not yet experienced a visible data failure.

Conversely, this record does not prove that payload survives RESET_n at all. That is outside the bounded claim.

## 2.6 Policy state has a second-order retention role

DRFM exists to help preserve future data integrity against disturbance-related risk. MR59 then configures how that maintenance mechanism operates.

This gives a second-order relation:

```text
payload retention / integrity
    depends partly on
maintenance mechanism
    whose behavior depends partly on
maintenance-policy state
```

The policy state is small, but its consequence can be larger than its byte count suggests.

That is an engineering observation, not a claim that MR59 itself stores payload history.

## 2.7 Service cost is part of the policy that must be reconstructed

Because BRC changes `tDRFM`, restoring a BRC value restores both a coverage policy and a service-time policy.

Thus:

```text
restore BRC
    !=
restore only a spatial label
```

It also restores a setting associated with a different maintenance exclusion duration on the inspected Micron part.

The record does not infer a platform's performance objective or claim which BRC is optimal.

---

# 3. Controlled functional comparisons

These are **functional comparisons only**. They are not genealogical claims and do not imply shared implementation.

## 3.1 Case 38 — Intel S3700 PLI maintenance-policy state

Case 38 separates:

```text
maintenance capability
    !=
current maintenance-policy value
    !=
persistent/saved policy semantics
```

Case 118 now has a related but different split:

```text
DRFM silicon capability
    !=
MR59 current configuration
    !=
controller-desired post-reset policy
```

The analogy is useful because both cases show that **the rule controlling a maintenance mechanism has its own lifetime**.

But the mechanisms differ sharply:

- Case 38 uses ATA/SCT feature-control semantics and asks about volatile versus saved feature state;
- Case 118 uses DDR5 mode-register initialization semantics and asks whether the host must re-establish nondefault state after reset.

No common persistence mechanism or genealogy is claimed.

## 3.2 Case 21 — DRAM self-refresh handoff

Case 21 shows that crossing a DRAM maintenance-mode boundary can leave transition-specific obligations before ordinary service is safely resumed.

Case 118 adds a different seam:

```text
self-refresh handoff debt
    !=
reset-time policy reconstruction debt
```

Both are useful examples of:

> **transition completed at one layer != maintenance closure completed at every layer.**

But self-refresh accounting and MR59 reprogramming are distinct mechanisms.

## 3.3 Case 03 — maintenance-control state can itself require retention

Case 03's Mostek material shows a refresh-address counter that participates in retention maintenance and is itself dynamic state.

Case 118 is not physically analogous to that counter, but the functional lesson remains controlled:

```text
state that controls retention maintenance
    can itself have a retention/lifetime contract
```

For Case 03 the control state requires physical refreshing. For Case 118 the relevant problem is **configuration reconstruction across reset**. These are deliberately not conflated.

## 3.4 Case 54 — split authority in DDR5 Refresh Management

Case 54 remains the broader canonical case for DDR5 RFM/RAA split authority.

Case 118 contributes a narrower configuration-lifetime point:

- the device owns product-specific physical-neighbor handling and support capability;
- the host can own an enable/BRC selection that must be programmed through MR59;
- after reset, the host-visible configuration contract requires rebuilding required nondefault settings.

Thus authority is not only spatially split; it can also be **temporally split across reset/reinitialization**.

This does not replace Case 54's broader command/accounting analysis.

---

# 4. Philosophical interpretation

The sources themselves do not use the repository's philosophical vocabulary. The following is therefore explicitly interpretive.

## 4.1 A mechanism can survive while its policy does not

Technical-retention analysis often asks whether the physical mechanism survives. Case 118 shows why that question is incomplete.

A DRAM die can still *possess* DRFM capability after a reset transition while the controller must nevertheless reconstruct the nondefault policy under which that capability is supposed to operate.

So:

```text
mechanism continuity
    !=
policy continuity
```

This is not “memory” in a psychological sense. It is a distinction between two engineering state relations.

## 4.2 Defaults are institutionalized forgetting with a safe baseline

A reset/default mechanism intentionally discards or refuses to rely on some prior configuration and returns the interface to a defined baseline from which software can rebuild policy.

Within this repository's interpretive vocabulary, that can be described as:

> **controlled forgetting plus reconstruction.**

The phrase is not JEDEC or Micron terminology and must never be presented as historical actor language.

## 4.3 Retention is about future obligations, not merely past data

MR59 does not primarily preserve a record of past payload. It determines what future maintenance will be performed.

This case therefore supports a broader project distinction:

```text
retaining what happened
    !=
retaining what must happen next
```

The latter can be correctness-relevant even when the state representation is only a few configuration bits.

---

# 5. Explicit non-claims

This evidence record does **not** claim any of the following:

1. That RESET_n physically erases every internal mode-register storage node.
2. That every MR bit uses the same internal circuit implementation.
3. That array payload survives DDR5 RESET_n.
4. That array payload is destroyed by DDR5 RESET_n.
5. That Micron guarantees a previous nondefault MR59 value after reset.
6. That a host may omit required MR programming after reset because the feature is implemented in silicon.
7. That `DRFM implemented` and `DRFM enabled` mean the same thing.
8. That `BRC supported` and `BRC selected` mean the same thing.
9. That BRC2 is the correct platform policy merely because it is the default.
10. That BRC4 is always preferable to BRC2 or BRC3.
11. That a wider BRC is free in latency or service exclusion time.
12. That Micron's exact `tDRFM` values apply to every DDR5 device.
13. That the 2020 JEDEC reset text proves every detail of Micron's 2024 DRFM implementation.
14. That the 2022 Micron core sheet proves which internal latch technology stores MR59.
15. That a reset necessarily occurs during normal platform operation.
16. That a missing MR59 restore immediately produces RowHammer corruption.
17. That a missing MR59 restore is sufficient by itself to cause a data error.
18. That a correctly restored MR59 setting is sufficient by itself to prove RowHammer immunity.
19. That DRFM replaces ordinary periodic refresh.
20. That DRFM replaces ECC, scrubbing, PPR, remapping, or controller-level mitigation.
21. That BRC defines a conventional logical-address radius visible to software.
22. That controller-visible address adjacency equals physical row adjacency.
23. That a platform's desired policy necessarily lives in SPD, BIOS, firmware, or any one named store.
24. That the repository has measured MR59 across an actual hardware RESET_n sequence.
25. That this record establishes the first invention or first shipment of DRFM.
26. That the Intel prior-art material in the Case 118 grounding is genealogically connected to Micron's implementation.
27. That Case 38 SCT saved/current semantics are the same as DDR5 MR semantics.
28. That Case 03's dynamic refresh counter is physically analogous to MR59 configuration storage.
29. That Case 21's self-refresh handoff mechanism is the same as reset-time policy restoration.
30. That `reset completed` automatically means `all platform-specific maintenance policy restored`.

---

# 6. Claim ledger

| Claim | Evidence class | Support | Strength |
| --- | --- | --- | --- |
| Micron MR59 exposes DRFM implementation status separately from host enable | H/P | Micron 2022 core data sheet | strong |
| Micron host DRFM enable defaults to disabled | H/P | Micron 2022 MR59 table | strong |
| Micron BRC defaults to BRC2; BRC3/BRC4 are nondefault selections | H/P | Micron 2022 MR59 table | strong |
| Micron stable-power reset initialization requires reissuing mode-register writes for required nondefault settings | H/P | Micron 2022 reset section | strong |
| JEDEC DDR5 reset/init defines MR defaults and a reconfiguration phase | H/P, mirror custody | JESD79-5 public text copy | strong for interface semantics; custody caveat retained |
| Named Micron 16Gb product reports DRFM support while host-write enable default is 0 | H/P | Micron 2024 product addendum | strong |
| A platform requiring enabled DRFM or BRC3/BRC4 has a post-reset policy-restoration obligation | E | combined reset + MR59 contracts | strong engineering reconstruction |
| Capability persistence does not imply nondefault policy continuity | E | combined evidence | strong |
| Reset completion and policy-restoration closure are separate milestones | E | combined evidence | medium-strong; controller trace still absent |
| Maintenance-policy state has its own lifetime distinct from payload state | E | combined evidence | strong conceptual reconstruction |
| Case 38 / 21 / 03 parallels are functional only | A | repository comparisons | controlled |
| “controlled forgetting plus reconstruction” | I | repository interpretation | interpretive only |

---

# 7. Source and inspection boundary

## Directly inspected / publicly retrievable records

1. Micron Technology, **DDR5 SDRAM Product Core Data Sheet**, Rev. D, 10/2022, manufacturer-authored PDF available through distributor/mirror copies.
2. JEDEC, **JESD79-5 DDR5 SDRAM**, July 2020, inspected through a public text mirror; official JEDEC site used only to anchor standards-body identity.
3. Micron Technology, **16Gb DDR5 SDRAM Die Rev D**, Rev. E, 01/2024, manufacturer-authored addendum available through DigiKey/device.report public copies.

## Not directly established in this slice

- an oscilloscope/logic-analyzer trace of RESET_n followed by MR59 reads/writes;
- a platform BIOS/firmware source showing the exact MR59 restore sequence;
- an authenticated current JEDEC portal download of the historical 2020 PDF;
- internal Micron schematics for MR59 storage;
- payload behavior during or immediately after RESET_n;
- a fault-injection result showing data corruption from omitted DRFM reprogramming;
- cross-vendor reset-policy behavior beyond the common standards framework.

---

# 8. Consequence for Case 118

The case can now carry a more precise retention statement:

> **DDR5 DRFM is not only a maintenance mechanism with bounded physical-neighbor coverage. It also has controller-programmed policy state whose lifetime is bounded by reset/initialization semantics: silicon capability, current MR59 configuration, and platform-desired policy are distinct state relations.**

The clean engineering chain is:

```text
named DRFM-capable die
    -> capability/status exposed
    -> host programs enable + BRC policy
    -> reset enters initialization/configuration regime
    -> nondefault MR policy must be reconstructed
    -> intended maintenance behavior resumes
```

That closes a previously under-specified control-state boundary without pretending to close the larger DRFM genealogy, fault-injection, remapping, or cross-vendor evidence debt.

## Status recommendation

Keep Case 118 at **`grounded`**.

This slice deepens the evidence for maintenance-policy lifetime but does not justify promotion because important debts remain:

- controller/platform traces showing real MR59 programming and restoration;
- standards-version genealogy for DRFM/ARFM/PRAC;
- cross-vendor product comparison;
- PPR/remapping interaction;
- fault injection / row-disturbance observations;
- exact outer-row ratio behavior and independent empirical validation.
