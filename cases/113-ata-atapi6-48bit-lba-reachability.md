# Case 113 — ATA/ATAPI-6 48-bit Address Feature: Reachability Beyond the 28-bit Ceiling

## Status

**`grounded`** — bounded to the 2000–2003 ATA/ATAPI-6 48-bit Address feature transition, with T13 standards-development records, the December 2001 1410D revision 3a draft, and 2003 Maxtor/Seagate manufacturer witnesses. The case establishes an address-reachability relation: a device can retain and report a logical-sector population larger than legacy 28-bit commands can reach, while 28-bit and 48-bit command families coexist over the lower part of the same LBA namespace.

Grounding record: [`../evidence/113-ata-2000-2003-48bit-lba-grounding.md`](../evidence/113-ata-2000-2003-48bit-lba-grounding.md).

## Scope

Case 89 already establishes that mid-1990s ATA can preserve one logical sector's LBA while its logical-CHS presentation changes, and that logical sector addresses must not be equated with actual media coordinates. Case 108 separately establishes nonuniform ZBR physical geometry beneath fixed-size logical blocks.

Case 113 asks the next bounded question:

> What remains the same, and what changes, when the ATA LBA namespace outgrows the address width of the older command family?


Policy-reach continuation: [`122-ata4-host-protected-area-addressability-retention.md`](122-ata4-host-protected-area-addressability-retention.md) grounds the distinct ATA/ATAPI-4 relation in which a host-set current maximum can intentionally withhold ordinary access to part of a larger native address population; this is separate from Case 113's command-encoding width ceiling.

This case is **not**:

- a complete history of IDE/ATA capacity barriers;
- a BIOS INT 13h / EDD genealogy;
- a history of every operating-system large-disk bug;
- a claim that ATA/ATAPI-6 invented LBA;
- a claim that the January 2000 T13 proposal was the first conception of 48-bit disk addressing;
- a reconstruction of platter geometry or controller firmware placement;
- a defect-remapping case;
- an HPA/DCO or secure-erasure case;
- a 4Kn/512e sector-size transition case;
- a claim that 48-bit addressing itself improves magnetic retention.

The broader ATA/BIOS/storage-interface history belongs primarily in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). Current repository searches there for `LBA48`, `48-bit LBA`, and `ATA-6` returned no dedicated case to reuse.

---

## Historical vocabulary

The inspected sources directly use:

- `48-bit Address feature set`;
- `28-bit addressing`;
- `48-bit addressing`;
- `logical block address` / `LBA`;
- `maximum user LBA`;
- `native maximum address`;
- `READ SECTOR(S) EXT`;
- `WRITE SECTOR(S) EXT`;
- `READ NATIVE MAX ADDRESS EXT`;
- `SET MAX ADDRESS EXT`;
- `IDENTIFY DEVICE`;
- `previous content` / `most recently written` register contents;
- `137GB storage barrier` in the manufacturer documentation.

The following are **project engineering terms**, not period ATA vocabulary:

- `namespace reachability`;
- `address-width ceiling`;
- `designation continuity`;
- `command-family reachability`;
- `reachability-retention relation`.

---

## Historical record

### H/P — a 48-bit LBA proposal is visible in the T13 record during 2000

T13's surviving document index lists `e00101r0 — 48-bit LBA proposal` dated **10 January 2000**, followed by revisions through `e00101r6` dated **31 August 2000**.

The ATA/ATAPI-6 1410D revision history then says revision 0b, dated **2 October 2000**, added `E00101R6 48-bit LBA`.

This supplies a standards-development floor. It does **not** establish invention priority, private design chronology, or a complete proposal genealogy.

### H/P — ATA/ATAPI-6 keeps 28-bit commands while adding a larger LBA command family

T13/1410D revision 3a, dated **14 December 2001**, defines the optional `48-bit Address feature set` in §6.20.

The draft says:

- the feature extends the addressable sector range to approximately 144 PB at the then-assumed sector geometry;
- it increases the command sector-count field to 16 bits;
- it defines `... EXT` commands including `READ SECTOR(S) EXT`, `WRITE SECTOR(S) EXT`, `READ NATIVE MAX ADDRESS EXT`, and `SET MAX ADDRESS EXT`;
- the 48-bit feature operates in LBA mode only;
- devices implementing it must still implement commands using 28-bit addressing;
- 28-bit and 48-bit commands may be intermixed.

This is not a one-step replacement in which the old command family vanishes.

> **48-bit Address support ≠ retirement of 28-bit commands**

### H/P — address width changes while the basic task-file register interface is extended

The same clause describes the Features, Sector Count, LBA Low, LBA Mid, and LBA High registers as two-byte-deep FIFOs for the 48-bit feature. The host writes high-order and low-order address/count portions through the existing register names, with `previous content` and `most recently written` positions supplying the wider command parameters.

That matters historically because the interface extension does not expose a new physical-disk coordinate system.

> **wider command encoding ≠ newly exposed physical geometry**

The extension changes how far the host can designate logical sectors through ATA commands, not what a platter cylinder or physical sector is.

### H/P — the device exposes distinct 28-bit and 48-bit capacity descriptors

ATA/ATAPI-6 §6.2 and §6.20 distinguish:

- `IDENTIFY DEVICE` words 60–61 for the 28-bit-addressable sector count;
- words 100–103 for the 48-bit feature's maximum user LBA + 1;
- word 83 bit 10 as the feature-support indication.

The draft explicitly says the capacity words themselves must not be used as the test for whether 48-bit addressing is supported; the capability bit supplies that relation.

If the device's 48-bit-addressable capacity exceeds the legacy range, words 60–61 remain limited to the maximum capacity addressable by 28-bit commands while words 100–103 describe the larger 48-bit-addressable space.

This yields two distinct relations:

> **legacy reported capacity ≠ whole device LBA reachability**

and:

> **capacity field value ≠ feature-support evidence**

### H/P — one physical device can have a native maximum beyond the legacy command's observable maximum

The same standard distinguishes `READ NATIVE MAX ADDRESS` from `READ NATIVE MAX ADDRESS EXT`.

For a device whose native maximum exceeds the 28-bit limit, the legacy command returns the legacy maximum, while the EXT form is the command associated with the larger native range.

So the bounded interface permits:

```text
same device
    + legacy command family -> bounded observable/reachable maximum
    + 48-bit EXT family      -> larger observable/reachable maximum
```

The lower result is not evidence that the higher-LBA sectors are physically absent.

> **unreachable through a legacy command ≠ absent from the device's larger logical sector set**

### H/P — a 160 GB Maxtor product is a concrete post-standardization witness

Maxtor's **DiamondMax16 60/80/120/160GB Product Manual**, dated **16 October 2003**, lists the 160 GB model at **320,173,056 sectors** and identifies its interface as `Maxtor Ultra ATA/133 (ATA-5/ATA-6)`.

The interface chapter says DiamondMax16 supports the ATA/ATAPI-6 command/control register set, including the 48-bit Address feature. Appendix A explicitly presents the 137 GB barrier as a consequence of the earlier 28-bit ATA address width and describes the 48-bit feature as the solution while retaining 28-bit commands for interoperability with older system components.

This is a named shipping-product contract, not merely a theoretical maximum in a standards draft.

### H/P — device-side support is not enough for full-system reachability

Seagate's **7 March 2003** public technical note, *Windows 137GB Capacity Barrier — 48-bit Logical Block Addressing Support for ATA, Serial ATA or ATAPI Disc Drives*, says that full access to ATA drives larger than 137 GB depends on system support, including the operating-system/driver and, in relevant configurations, BIOS/controller support.

The note warns that on the Windows configurations it discusses, using capacity beyond the boundary without proper 48-bit support can cause writes to wrap into lower filesystem locations and overwrite data.

This is a vendor-specific ecosystem warning, not a universal ATA-standard rule. Its methodological value is narrower:

> **device-retained capacity ≠ host-stack reachability**

and:

> **address-interpretation failure can destroy payload without any prior failure of magnetic retention**

---

## Retained state

The bounded case separates at least six state classes.

### 1. User payload

Bytes stored in logical sectors remain the data the host ultimately wants to retrieve.

### 2. LBA designation

A logical sector is named in the linear LBA namespace. Case 89 already establishes that this designation must not be mistaken for physical location.

### 3. Command-family address width

The host command can carry either the legacy 28-bit LBA form or the 48-bit EXT form. This determines which portion of the namespace can be designated through that command family.

### 4. Capability state

`IDENTIFY DEVICE` word 83 bit 10 reports whether the 48-bit Address feature set is supported. This is distinct from merely seeing a large capacity number.

### 5. Capacity descriptors

Legacy and 48-bit capacity fields can report different upper reachability bounds for the same device.

### 6. Host-stack interpretation/support

BIOS, controller, driver, and operating-system support can determine whether a particular machine can safely issue and interpret the larger address form. This is not user payload and is not the physical magnetic representation.

---

## Retention mechanism

48-bit LBA is not a substrate-retention mechanism. It does not refresh charge, restore magnetic domains, add parity, or replicate payload.

The retention-specific mechanism is **continued designation and safe reachability as the address namespace grows**.

```text
retained payload on device
        |
        +--> LBA within legacy range
        |       -> 28-bit command can designate it
        |       -> 48-bit command may also designate it on supporting device
        |
        +--> LBA above legacy range
                -> retained/logically present on larger device
                -> requires 48-bit-capable command + supporting host path
```

The crucial distinction is therefore:

> **payload existence ≠ reachability through every historical address width**

A logical object can remain on the device while becoming inaccessible or dangerously misaddressed to a host stack that has lost the interpretation machinery needed for its address range.

---

## Read / write semantics

### Read

`READ SECTOR(S) EXT` carries the wider LBA. For lower addresses, the standard permits 28-bit and 48-bit commands to coexist; for addresses beyond the legacy ceiling, the legacy family cannot represent the target.

### Write

The same address-width distinction applies to the extended write command family. Nothing in this case establishes that an LBA write is physically in-place, and nothing says widening the command address itself relocates pre-existing sectors.

> **address-width extension ≠ payload relocation**

### Maximum-address queries

Legacy and EXT native-maximum queries can intentionally reveal different ceilings on a large device. The returned maximum is therefore qualified by command semantics.

> **reported maximum address ≠ one observer-independent property unless the command regime is specified**

---

## Failure / forgetting modes

Keep separate:

- **magnetic payload loss** — the medium can no longer recover the stored value;
- **address-width insufficiency** — the command cannot represent the requested high LBA;
- **capability misdetection** — software infers support from the wrong field rather than the defined capability bit;
- **host-stack incompatibility** — a BIOS/controller/driver/OS path cannot safely handle the larger address regime;
- **misaddressed or wrapped writes in the bounded Seagate Windows warning** — incorrect address handling overwrites other logical content;
- **defect reassignment** — Case 14's physical replacement path;
- **physical zoning** — Case 108's ZBR layout;
- **secure deletion** — not established by reducing or changing address reachability.

A sector can be **present yet unreachable through one command family**. Conversely, an address can remain syntactically valid while the payload it designates has failed physically. Reachability and retention must not be collapsed.

---

## Engineering reconstruction

### E — namespace size and command reach are separate

ATA/ATAPI-6 explicitly lets the 48-bit capacity descriptor exceed the legacy descriptor on the same device.

Therefore:

> **device logical-sector population ≠ legacy command-family reach**

### E — compatibility can preserve an old interface path without preserving full capacity

A 48-bit-capable device still supports 28-bit commands. That compatibility allows older operations over the lower range but cannot make a 28-bit command encode a high LBA.

> **backward command compatibility ≠ backward full-capacity reachability**

### E — address-width extension preserves abstraction rather than exposing placement

The wider form remains LBA-only and reuses task-file register semantics. It adds address bits; it does not turn the host-visible number into a physical track/head/sector coordinate.

> **more address bits ≠ more physical-location disclosure**

### E — correct interpretation is constitutive infrastructure

The Seagate support record shows a system can possess a large ATA drive while the software path is unable to safely use the high range.

Therefore:

> **retained payload + retained medium ≠ usable state without compatible address interpretation**

This is a relation-level claim, not a claim that the host software stores the payload itself.

---

## Functional comparisons

### A — Case 89 ATA CHS/LBA translation

Case 89 and Case 113 concern different address problems.

- Case 89: the same logical sector keeps its LBA while the **logical CHS representation** can change.
- Case 113: the same linear LBA model persists while the **command address width** grows so a larger namespace becomes reachable.

Together they show that `address abstraction` is not one operation. Coordinate representation and numeric reach are separate axes.

### A — Case 108 ZBR geometry

Case 108 grounds nonuniform physical radial geometry beneath fixed logical blocks. Case 113 does not change that geometry and supplies no evidence of sector relocation.

> **larger LBA range ≠ changed ZBR geometry**

### A — Case 14 defect reassignment

Case 14 changes which physical sector serves a stable LBA after a defect. Case 113 changes which LBAs a host command can encode.

> **reachability extension ≠ physical embodiment replacement**

### A — virtual-memory and object-store namespace growth

Other systems can also retain objects beyond the reach of an older pointer/address regime, but that is only a functional comparison. ATA's task-file encoding, T13 history, and disk interface constraints are specific to this case.

---

## Historical-priority boundary

T13's document list gives a public `48-bit LBA proposal` record beginning in January 2000, and the 1410D history says revision 0b integrated revision 6 in October 2000. The December 2001 revision 3a draft is still explicitly labeled an internal working document rather than an approved standard. T13's standards archive separately lists `INCITS 361-2002 (1410D): ATA/ATAPI-6`.

Therefore:

> **January 2000 proposal record ≠ invention date**

> **December 2001 working draft ≠ approved-final-standard identity**

> **2003 Maxtor product witness ≠ first commercial implementation proof**

The case establishes a standards-development and named-product floor, not priority.

---

## Claim ledger

| Claim | Type | Strength / limit |
| --- | --- | --- |
| T13 lists 48-bit LBA proposal revisions during 2000 | H/P | strong institutional chronology |
| 1410D rev. 0b says it added E00101R6 | H/P | strong draft-history anchor |
| 1410D rev. 3a defines the 48-bit Address feature | H/P | strong for inspected working draft |
| 48-bit commands coexist with mandatory 28-bit commands on supporting devices | H/P | strong |
| 48-bit feature operates in LBA only | H/P | strong |
| words 60–61 and 100–103 can expose different capacity ceilings | H/P | strong |
| word 83 bit 10, not the capacity words alone, indicates support | H/P | strong |
| legacy max-address query can be capped below the EXT-native maximum | H/P | strong |
| DiamondMax16 160 GB is a named 2003 product witness above the legacy barrier | H/P | strong manufacturer-primary witness |
| full device capacity can require host-stack support | H/P | strong for Seagate's documented 2003 Windows ecosystem |
| high-LBA unreachability means the sector is physically absent | X | rejected |
| wider LBA means physical sector relocation | X | rejected |
| 48-bit LBA exposes platter geometry | X | rejected |
| 48-bit support alone guarantees every legacy BIOS/OS can use full capacity | X | rejected |
| January 2000 is invention priority | X | rejected |

---

## Open work

Still open:

- the proposal's pre-January-2000 design genealogy and meeting history;
- exact final INCITS 361-2002 text/revision comparison against 1410D rev. 3a;
- BIOS Enhanced Disk Drive / INT 13h extension history;
- Windows/Linux/BSD driver adoption chronology and fault reproduction;
- first shipping >137 GB ATA-product priority;
- HPA/DCO interactions and capacity hiding;
- SATA/ACS continuation;
- 2 TiB partition-table barriers;
- 4Kn/512e and later logical/physical-sector-size transitions;
- controller implementation and fault injection.

Those belong mainly in `computing-archaeology` unless a future slice exposes a distinct retention relation.

## Sources

1. Technical Committee T13, document index for **e00101r0–r6, “48-bit LBA proposal”**, January–August 2000: <https://www.t13.org/Documents/?created%5Bmax%5D=&created%5Bmin%5D=&order=field_document_number&page=21&sort=asc>.
2. T13/1410D Revision 3a, **AT Attachment with Packet Interface - 6 (ATA/ATAPI-6)**, 14 December 2001, especially document history; §6.2; §6.20; IDENTIFY DEVICE; READ NATIVE MAX ADDRESS / EXT: <https://www.cs.utexas.edu/~dahlin/Classes/439/ref/hardware/ATA-d1410r3a.pdf>.
3. Technical Committee T13, **Standards — Expired**, listing `INCITS 361-2002 (1410D): ATA/ATAPI-6`: <https://t13.org/standards-expired>.
4. Maxtor, **DiamondMax16 60/80/120/160GB Product Manual**, 16 October 2003, Part No. 1837, hosted by Seagate: <https://www.seagate.com/staticfiles/maxtor/en_us/documentation/manuals/diamondmax_16_manual.pdf>.
5. Seagate Technology, **Windows 137GB Capacity Barrier — 48-bit Logical Block Addressing Support for ATA, Serial ATA or ATAPI Disc Drives**, Version 1.0, 7 March 2003: <https://www.seagate.com/support/kb/disc/tp/137gb.pdf>.
