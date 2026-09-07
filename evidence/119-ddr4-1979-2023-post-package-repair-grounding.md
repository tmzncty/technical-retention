# Evidence 119 — DDR4 Post-Package Repair, 1979–2023 grounding

## Purpose

This evidence record grounds [`../cases/119-ddr4-post-package-repair-row-remapping.md`](../cases/119-ddr4-post-package-repair-row-remapping.md).

The bounded question is:

> What evidence supports treating DDR4 Post-Package Repair as a retained row-address substitution relation whose lifetime can be temporary (`sPPR`) or persistent (`hPPR`), while keeping payload volatility, ECC, spare capacity, repair authority, and repair-transition safety separate?

The evidence supports a strong bounded result. It does **not** establish a complete JEDEC PPR genealogy or a universal transistor/fuse implementation across vendors.

## Evidence classification

- **H/P** — historical / primary, manufacturer, patent, or platform technical record.
- **E** — engineering reconstruction constrained by those records.
- **A** — bounded functional analogy.
- **X** — explicitly unsupported or rejected stronger inference.

---

## Source A — Procyk/Cenker spare-row redundancy, 1979 filing / 1980 publication

### Identity

F. Procyk and R. Cenker, **“Memory with redundant rows and columns.”**

Public patent-family record:

<https://patents.google.com/patent/WO1980001732A1/fulltext>

Relevant chronology:

- U.S. priority/filing: **1979-02-09**;
- PCT filing: **1980-01-28**;
- WO publication: **1980-08-21**;
- U.S. publication/grant family includes US4228528.

### Mechanism actually established

The patent describes a semiconductor memory augmented with spare rows and columns. Standard row/column decoders are normally active; spare decoders are normally deselected. After test identifies a defective row or column:

- the decoder of the defective standard element can be permanently disabled;
- a spare decoder can be programmed so that it responds to the address formerly selecting the defective element;
- fusible links opened by laser provide the disclosed programming mechanism.

The source explicitly says the spare element is thereafter substituted in the operative array for the disabled standard element.

Safe use in Case 119:

> **redundant-row/column address takeover is explicit prior art by the 1979 filing.**

Unsafe use:

> `1979 patent = DDR4 PPR`.

The older mechanism is manufacturing/test-time laser-fuse redundancy, not the later post-package command/firmware lifecycle.

### Claim strength

- **Strong H/P** for the 1979 priority floor and the described spare decoder/address substitution mechanism.
- **Strong X** against claiming DDR4 PPR invented spare-row address replacement.
- **No genealogy claim** from this family to JEDEC DDR4 PPR.

---

## Source B — Micron 16Gb DDR4 product documentation, Rev. G, August 2020

### Identity and provenance

Manufacturer-authored product document:

- **16Gb: x4, x8, x16 DDR4 SDRAM**;
- Micron document family `16gb_ddr4_dram.pdf`;
- Rev. G, `08/2020` in the publicly indexed datasheet extraction;
- PPR capability is exposed in Mode Register 4 / MPR capability information.

Public HTML extraction used in this round:

<https://www.alldatasheet.es/html-pdf/2163888/MICRON/MT40A4G4VA-062E%3AB/15805/59/MT40A4G4VA-062E%3AB.html>

Additional manufacturer-document extraction with the PPR sequence text:

<https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/imx-processors/231284/1/16Gb_DDR4_SDRAM.pdf>

The text is **Micron-authored manufacturer documentation accessed through public mirrors**, not a stable current Micron-hosted archive. That provenance is a real evidence limitation and is not hidden.

### Product semantics

The bounded product documentation states that:

- hard Post-Package Repair (`hPPR`) is an irreversible repair mode;
- soft Post-Package Repair (`sPPR`) is a distinct supported mode;
- the controller supplies the failing row address to the device during the repair sequence;
- the product exposes PPR-support capability bits;
- the bounded Micron design provides finite row-repair resources, including at least one repair row per bank in the documented family.

A later indexed Micron extraction states the lifetime distinction directly:

- `sPPR` is **non-persistent**, reversible/reassignable, and can later be made permanent through `hPPR`;
- `hPPR` is **persistent/permanent** and cannot be reversed;
- a later PPR does not simply overwrite a previously established hard-PPR address in the same bank.

### What this source does not establish

It does not establish:

- the first JEDEC revision to introduce PPR;
- a universal physical fuse technology across DDR4 vendors;
- that the target row's current payload is copied to the spare row;
- a universal spare-row count for all DDR4 densities/revisions.

### Claim strength

- **Strong H/P** for the bounded Micron product's PPR modes and finite repair resources.
- **Medium-to-strong provenance** because the document is manufacturer-authored but presently accessed through mirrors.
- **Strong X** against universalizing the product-specific resource count or mechanism.

---

## Source C — Intel 12th Generation Core platform PPR documentation, 2023 public revision

### Identity

Intel, **12th Generation Intel Core Processors Datasheet, Volume 1 of 2**, public document ID `655258`, revision dated **2023-06-15**, section **Post Package Repair (PPR)**.

Public Intel page:

<https://edc.intel.com/content/www/us/en/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/12th-generation-intel-core-processors-datasheet-volume-1-of-2/010/post-package-repair-ppr/>

### Platform boundary

The Intel documentation states that PPR is supported according to JEDEC specification and that BIOS can:

- identify a single row failure per bank in DRAM;
- perform PPR to exchange the failing row with a spare row.

DDR4 is listed among the supported technologies.

This establishes a system-level authority relation:

```text
platform/BIOS identifies failing row
    -> platform invokes PPR
    -> DRAM substitutes spare row
```

Safe inference:

> **DRAM repair capability does not imply that all diagnosis and invocation authority is internal to the DRAM.**

The document does not reveal every internal DRAM mapping mechanism.

### Claim strength

- **Strong H/P** for a named Intel platform path and BIOS participation.
- **No claim** that every controller/BIOS uses the same threshold, telemetry, or timing.

---

## Source D — Lenovo ThinkSystem boot-cycle and permanent PPR behavior

### Identity

Lenovo ThinkSystem service documentation includes PPR success/event guidance and describes the two repair lifetimes.

Representative current Lenovo documentation:

<https://pubs.lenovo.com/sr850-v2/FQXSFMA0026I>

A named SR860 V2 support workflow additionally documents reboot-triggered DIMM self-healing / hard-PPR attempt:

<https://support.lenovo.com/us/en/solutions/ht516292>

### Operational semantics

Lenovo states that PPR substitutes access to a bad cell or address row with a spare row inside the DRAM device and distinguishes:

- **sPPR** — repair for the current boot cycle; removal of power or reset/reboot returns the DIMM to its original state;
- **hPPR** — permanent row repair.

The SR860 V2 guidance tells an operator to restart the system to allow DIMM self-healing to attempt hard PPR and then confirm a success event.

This is especially useful because it converts an interface feature into an observed service workflow:

> **repair-state lifetime can be tied to a boot/power boundary, and hard repair can be scheduled as a firmware/reboot maintenance action.**

### Claim strength

- **Strong H/P** for Lenovo's supported-system operational contract.
- **Not universal** across all servers, firmware revisions, or DRAM parts.

---

## Source E — Intel hard-PPR power-failure mitigation patent, 2020 priority

### Identity

Intel Corporation, **“Dynamic random access memory built-in self-test power fail mitigation.”**

Public patent record:

<https://patents.google.com/patent/US12190979B2/en>

Relevant chronology:

- family priority: **2020-02-04**;
- continuation filing represented by US18/373,658: **2023-09-27**;
- A1 publication: **2024-01-18**;
- B2 publication: **2025-01-07**.

The 2020 priority date and later public publication dates are kept separate.

### PPR background relation

The disclosure describes PPR as remapping the row address of a defective row to a previously unused spare row so future reads/writes that would have targeted the defective row are redirected to the replacement row.

It further distinguishes:

- `sPPR`: quick, temporary repair;
- `hPPR`: slower, permanent repair;
- one described hard-repair implementation can program electrical fuses to disconnect faulty rows/columns and substitute redundant ones.

It also describes a controller retaining a defective row address and issuing PPR on a later reboot.

### Repair-transition failure window

The disclosure's most important retention-specific point is not simply that hard repair is permanent. It says that in the described power environment an unexpected power failure during hard PPR may leave electrical fuses partially blown and make the SDRAM unusable.

Its mitigation therefore separates long self-test work from the hard-repair phase and starts/bounds hard repair so it can complete while power remains stable.

This supports:

> **persistent repair result != failure-proof transition into persistent repair state.**

It is a useful second-order durability example: the mapping/configuration that is intended to outlive power cycles may itself require a protected establishment interval.

### Boundaries

This patent is not used to claim:

- every DDR4 PPR device uses electrical fuses;
- every hard PPR has the same timing;
- every PPR transition is non-atomic in the same way;
- Intel invented PPR.

The source is a bounded problem/implementation disclosure.

---

## Cross-source synthesis

The sources jointly support the following decomposition:

```text
row defect exists
    != defect is detected
    != defect evidence is retained
    != repair is authorized
    != repair sequence starts
    != persistent repair state is safely established
    != logical row address
    != original physical row
    != spare physical row
    != current payload contents
    != future refresh obligation
    != remaining spare capacity
```

### Grounded finding 1 — logical row-address identity can survive physical row substitution

The platform and patent records explicitly describe a failing row being exchanged/remapped to a spare row while future accesses continue through the row address relation.

**Strength:** strong H/P + conservative E.

### Grounded finding 2 — repair-state lifetime is independent of payload volatility

The same volatile DRAM technology supports non-persistent soft repair and persistent hard repair. The hard repair relation can survive a power cycle even though ordinary DRAM payload cannot.

**Strength:** strong H/P + E.

### Grounded finding 3 — address continuity is weaker than payload continuity

None of the inspected sources establishes a universal copy of the defective row's current payload into the spare row as the meaning of PPR. The safe claim is future address redirection.

**Strength:** strong X against overclaim; E.

### Grounded finding 4 — repair authority can be distributed across platform and device

Intel and Lenovo show BIOS/firmware/reboot participation while the DRAM supplies internal spare-row substitution capability.

**Strength:** strong H/P for named platform paths.

### Grounded finding 5 — establishing persistent repair state can itself have a failure envelope

Intel's power-fail disclosure gives a bounded example where fuse programming can be interrupted, so `permanent` describes the intended completed state, not immunity of the transition process.

**Strength:** strong H/P within disclosed implementation; no universalization.

### Grounded finding 6 — spare-row substitution long predates DDR4 PPR

The 1979-filed patent explicitly provides spare rows/columns and address takeover through programmable decoders.

**Strength:** strong H/P prior-art floor; no direct genealogy.

---

## Cross-case boundaries

### Case 14 — SCSI defect reassignment

Functional similarity:

```text
stable logical designation
    -> defective physical embodiment retired
    -> spare/replacement embodiment substituted
```

Critical difference:

- SCSI case operates at drive logical-block/physical-sector mapping level;
- DDR4 PPR operates inside a volatile semiconductor array at row-repair/decoder level.

Case 14 also helps preserve the warning that remap success and payload recovery are separate questions.

**Classification:** `A`, not genealogy.

### Case 04 — mapped Flash

Both allow logical identity to outlive one physical embodiment, but Flash translation is an active controller-managed mapping/reclamation system under erase/program/wear constraints. DDR4 PPR is a sparse defect-repair substitution relation with finite spare rows.

**Classification:** `A`, not mechanism identity.

### Cases 03/21/54/105/106/118 — DRAM refresh family

PPR does not satisfy the ordinary charge-restoration obligation. A repaired spare row is still DRAM and still requires the applicable refresh regime.

Therefore:

> **row substitution != refresh.**

**Classification:** `H/P` + `A` boundary.

---

## Rejected stronger claims

- **`DDR4 PPR invented redundant-row repair`** — rejected by 1979 prior art.
- **`1979 spare-row redundancy is DDR4 PPR`** — rejected; historical mechanism/lifecycle differs.
- **`hPPR makes DRAM nonvolatile`** — rejected; repair configuration and payload have different retention lifetimes.
- **`sPPR is merely a failed or incomplete hPPR`** — rejected; it is a distinct temporary/reversible repair contract.
- **`PPR copies the old row payload into the spare row`** — unsupported by the inspected evidence as a universal rule.
- **`PPR is ECC`** — rejected; correction and physical-row substitution are different relations.
- **`all hPPR uses the Intel disclosed fuse mechanism`** — rejected.
- **`one successful PPR means unlimited future healing capacity`** — rejected by finite repair resources in the bounded product.
- **`retired bad row is securely erased`** — unsupported.
- **`earlier spare-row function proves direct 1979→DDR4 genealogy`** — rejected.

---

## Related-repository check

Searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Post Package Repair` and `PPR DDR4` returned no dedicated case in this round.

Division of labor:

- **technical-retention** keeps the bounded relation `row address vs physical row vs repair-state lifetime vs payload lifetime`;
- **computing-archaeology** should take a broader semiconductor redundancy / laser-fuse→eFuse / JEDEC PPR / controller-platform genealogy if that work is later developed.

---

## Evidence debt

1. Obtain a stable official Micron-hosted archive or page-preserving facsimile for the exact bounded DDR4 product revision.
2. Establish the exact JESD79-4 revision/ballot chronology for hPPR and sPPR; do not assume initial September-2012 DDR4 already had the final PPR contract.
3. Add cross-vendor Samsung/SK hynix product documentation and distinguish eFuse/antifuse/other internal implementations.
4. Determine exact target-row data-preservation semantics for each PPR sequence and product rather than inferring payload migration from address continuity.
5. Trace platform error telemetry/ECC/patrol-scrub evidence into BIOS PPR decision thresholds on named systems.
6. Validate repair-resource exhaustion and post-repair telemetry on named DIMMs.
7. Add safe power-fail/fault-injection evidence for hard-PPR transition behavior if sacrificial hardware and a controlled setup become available.
8. Separate manufacturing-time redundancy, PPR, RowHammer repair/mitigation, and later DDR5 repair features in a standards chronology.

None of these debts invalidates the bounded findings above.
