# Case 113 grounding — ATA/ATAPI-6 48-bit LBA reachability, 2000–2003

## Status

**`grounded`** for the bounded claim that ATA/ATAPI-6 adds a 48-bit LBA command/addressing regime while preserving legacy 28-bit commands, allowing one device to expose a larger logical-sector population than legacy commands can reach. Manufacturer documentation from 2003 provides a named >137 GB product witness and a host-stack compatibility boundary.

This record does **not** establish the invention priority of 48-bit disk addressing, the complete BIOS/IDE/ATA capacity-barrier history, first shipping-product priority, physical platter layout, or a direct genealogy to later SATA/ACS, 4Kn, GPT, or other large-storage transitions.

---

## Research question

What evidence is sufficient to say that, in the bounded ATA/ATAPI-6 regime:

1. a device may retain/report more logical sectors than legacy 28-bit commands can designate;
2. a 48-bit-capable device still supports 28-bit commands rather than replacing them outright;
3. legacy and extended capacity/max-address reporting must be interpreted in the command-feature context;
4. greater LBA reach does not disclose physical media geometry or imply payload relocation;
5. device-side support is distinct from end-to-end host-stack ability to use high LBAs safely;
6. the 2000–2003 records provide a standards-development/product floor without proving invention priority?

---

## Repository pre-check

Before selecting this slice, the current repository state was re-read:

- `README.md`;
- `ROADMAP.md`;
- `CASE_INDEX.md`;
- `AGENTS.md`;
- `docs/METHOD.md`;
- `docs/PRIOR_ART.md`;
- `docs/TECHNICAL_SPINE.md`;
- `RELATED_REPOS.md`;
- recent Case 112 integration and the latest main-branch commit chain.

The roadmap's broad HDD item remained unchecked and explicitly listed `LBA28→LBA48` among the open histories. Case 89 explicitly left `48-bit LBA` as a separate future slice, while Case 108 separately owns the physical ZBR geometry relation and Case 14 owns failure-triggered physical defect reassignment.

Repository searches of `tmzncty/computing-archaeology` for `LBA48`, `48-bit LBA`, and `ATA-6` returned no dedicated case/doc match. Therefore this case records only the retention-specific reachability relation here; a complete ATA/BIOS/storage-interface history should be developed in the companion repository rather than duplicated here.

---

## Source set

### P1 — T13 48-bit LBA proposal document record

Technical Committee T13 document index, entries `e00101r0` through `e00101r6`, titled **“48-bit LBA proposal”**.

T13's public index records:

- `e00101r0` — 10 January 2000;
- subsequent revisions during 2000;
- `e00101r6` — 31 August 2000.

URL:

<https://www.t13.org/Documents/?created%5Bmax%5D=&created%5Bmin%5D=&order=field_document_number&page=21&sort=asc>

Use: standards-development chronology only. The index does not establish first conception or invention priority.

### P2 — ATA/ATAPI-6 working draft

**T13/1410D Revision 3a, _AT Attachment with Packet Interface - 6 (ATA/ATAPI-6)_**, 14 December 2001.

Public facsimile mirror:

<https://www.cs.utexas.edu/~dahlin/Classes/439/ref/hardware/ATA-d1410r3a.pdf>

Important source-status boundary: the cover states that it is an internal working document and not an approved standard.

Relevant locations:

- document history: revision 0b, 2 October 2000, records `Added E00101R6 48-bit LBA`;
- §6.2, LBA / capacity reporting;
- §6.20, `48-bit Address feature set`;
- `IDENTIFY DEVICE`, especially word 83 bit 10, words 60–61, and words 100–103;
- `READ NATIVE MAX ADDRESS` / `READ NATIVE MAX ADDRESS EXT`;
- the `... EXT` read/write command family.

Bounded primary findings from the draft:

1. the optional 48-bit feature extends the LBA range and expands sector count to 16 bits;
2. the feature operates in LBA mode only;
3. a device implementing the feature must continue to implement 28-bit addressing commands;
4. 28-bit and 48-bit commands may be intermixed;
5. the task-file address/count registers are treated as two-byte-deep FIFOs for the wider parameters;
6. words 60–61 describe the legacy 28-bit-addressable capacity while words 100–103 describe the 48-bit maximum-user-LBA relation;
7. support is indicated by the defined feature bit rather than inferred solely from capacity values;
8. legacy and EXT maximum-address queries can return different upper bounds on a sufficiently large device.

### P3 — T13 published-standard archive context

Technical Committee T13, **Standards — Expired**, listing:

`INCITS 361-2002 (1410D): AT Attachment - 6 with Packet Interface (ATA/ATAPI-6)`.

URL:

<https://t13.org/standards-expired>

Use: institutional context separating the inspected December-2001 working draft from the later published-standard record. This page is not substituted for exact final-standard clause archaeology.

### P4 — Maxtor named product witness

Maxtor, **_DiamondMax16 60/80/120/160GB Product Manual_**, 16 October 2003, Part Number 1837.

Seagate-hosted manufacturer PDF:

<https://www.seagate.com/staticfiles/maxtor/en_us/documentation/manuals/diamondmax_16_manual.pdf>

Relevant locations:

- product-specification table around printed p. 3-2: 160 GB model, `Sectors per Drive (max LBA)` = **320,173,056**; interface `Maxtor Ultra ATA/133 (ATA-5/ATA-6)`;
- interface chapter around printed p. 5-2: ATA/ATAPI-6 command/control register set including 48-bit addressing;
- Appendix A: `137GB Barrier`, the earlier 28-bit limitation, and the 48-bit feature;
- Appendix A also states that 48-bit and 28-bit command families coexist for interoperability and that 48-bit addressing is LBA-only.

Use: named commercial product contract above the legacy capacity boundary. It does not prove first shipping implementation.

### P5 — Seagate host-stack compatibility witness

Seagate Technology, **_Windows 137GB Capacity Barrier — 48-bit Logical Block Addressing Support for ATA, Serial ATA or ATAPI Disc Drives_**, Version 1.0, 7 March 2003.

PDF:

<https://www.seagate.com/support/kb/disc/tp/137gb.pdf>

Relevant locations:

- title/date page and overview;
- printed pp. 5–6 for the 28-bit capacity barrier and ATA/ATAPI-6 48-bit transition;
- support matrix/discussion distinguishing drive support from operating-system, driver, BIOS/controller support;
- Windows-specific warning that an unsupported path can wrap writes into lower filesystem locations and overwrite data.

The printed pp. 5–6 were inspected as page images in addition to text extraction. The wraparound warning is retained strictly as a bounded Seagate/Windows ecosystem statement, not generalized into an ATA protocol law.

---

## Claim ledger

| ID | Claim | Evidence | Label | Strength / limit |
| --- | --- | --- | --- | --- |
| 113-H1 | T13 publicly records a `48-bit LBA proposal` revision series beginning 10 Jan 2000 and continuing through Aug 2000. | P1 | H/P | strong institutional chronology; not priority |
| 113-H2 | 1410D rev. 0b records incorporation of `E00101R6 48-bit LBA` on 2 Oct 2000. | P2 | H/P | strong draft-history anchor |
| 113-H3 | 1410D rev. 3a defines an optional 48-bit Address feature set. | P2 | H/P | strong for inspected working draft |
| 113-H4 | The feature operates in LBA mode only. | P2 | H/P | strong |
| 113-H5 | Supporting devices must continue to implement 28-bit-addressing commands and may intermix 28/48-bit commands. | P2 | H/P | central strong claim |
| 113-H6 | The 48-bit feature widens address/count command parameters using the existing task-file register names as two-byte-deep FIFOs. | P2 | H/P | strong; interface encoding, not physical map |
| 113-H7 | IDENTIFY DEVICE distinguishes legacy 28-bit capacity fields from 48-bit maximum-user-LBA fields. | P2 | H/P | central strong claim |
| 113-H8 | The feature-support bit, not the capacity field alone, is the defined support indicator. | P2 | H/P | strong |
| 113-H9 | Legacy and EXT native-maximum commands can expose different upper bounds on a sufficiently large device. | P2 | H/P | strong |
| 113-H10 | T13's archive lists INCITS 361-2002 as ATA/ATAPI-6. | P3 | H/P | institutional publication context |
| 113-H11 | Maxtor's 2003 DiamondMax16 manual documents a 160 GB / 320,173,056-sector ATA-5/ATA-6 product family with 48-bit-address support. | P4 | H/P | strong named-product witness |
| 113-H12 | Maxtor describes the 137 GB boundary as an earlier 28-bit addressing limit and keeps legacy commands for interoperability. | P4 | H/P | strong manufacturer explanation |
| 113-H13 | Seagate says full use of >137 GB ATA capacity depends on host-stack support, not drive support alone. | P5 | H/P | strong for documented 2003 ecosystem |
| 113-H14 | Seagate warns that unsupported 48-bit addressing in the Windows configurations discussed can cause high-range writes to overwrite lower filesystem data. | P5 | H/P | bounded vendor/OS warning, not universal ATA law |
| 113-E1 | A device's logical-sector population can exceed what one legacy command family can designate. | P2/P4 | E | direct reconstruction |
| 113-E2 | Backward command compatibility does not imply backward full-capacity reachability. | P2/P4 | E | strong |
| 113-E3 | High-LBA unreachability through a legacy command is not evidence of physical absence. | P2/P4 | E | strong negative boundary |
| 113-E4 | Wider command addressing does not itself establish data relocation. | P2 | E/X | strong negative boundary |
| 113-E5 | More LBA bits do not expose physical platter geometry. | P2 + Case 89/108 | E | strong relation-level synthesis |
| 113-E6 | Capability, capacity reporting, and reachable namespace are distinct interface state relations. | P2 | E | strong |
| 113-E7 | Device payload retention and end-to-end host reachability can diverge. | P4/P5 | E | strong bounded ecosystem reconstruction |
| 113-E8 | Address interpretation/support can be constitutive of usable retention without being user payload. | P2/P5 | E | strong; operational relation |
| 113-A1 | Case 89 and Case 113 both concern logical designation but on different axes: coordinate representation vs numeric command reach. | Case 89 + P2 | A | functional comparison only |
| 113-A2 | Case 108's physical ZBR geometry and Case 113's address-width expansion are separate lower/upper layers beneath logical-block service. | Case 108 + P2 | A | functional comparison only |
| 113-A3 | Case 14 physical defect reassignment and Case 113 reachability extension can both preserve LBA semantics but change different relations. | Case 14 + P2 | A | functional comparison only |
| 113-I1 | Availability of a retained object depends on preservation of an interpretable addressing relation, not only substrate persistence. | E1–E8 | I | project interpretation, not period vocabulary |
| 113-X1 | January 2000 is the invention date of 48-bit LBA. | P1/P2 | X | rejected |
| 113-X2 | December 2001 rev. 3a is itself the approved final standard. | P2/P3 | X | rejected |
| 113-X3 | 48-bit addressing physically moves sectors or reveals platter locations. | P2 + Cases 89/108 | X | rejected |

---

## Exact boundaries established

### 1. `device logical-sector population ≠ legacy command-family reach`

The standards draft has separate legacy and 48-bit capacity/max-address relations, and the Maxtor product supplies a named device above the legacy 137 GB boundary.

A high LBA can therefore be part of the device's logical sector population even though a 28-bit command cannot encode it.

### 2. `48-bit support ≠ retirement of 28-bit commands`

ATA/ATAPI-6 requires the legacy command family to remain available on a device implementing 48-bit addressing and permits intermixing the two forms.

This blocks a simplistic historical story in which `LBA28` disappears at the instant `LBA48` arrives.

### 3. `legacy capacity descriptor ≠ whole 48-bit-addressable capacity`

The standard intentionally retains different capacity fields for the two regimes. On a sufficiently large drive, the legacy field reaches its legacy ceiling while the 48-bit field describes a larger user-addressable range.

### 4. `capacity value ≠ feature-support indication`

ATA/ATAPI-6 assigns the 48-bit feature-support relation to the defined IDENTIFY capability bit. A host must not treat a capacity field as a substitute for that feature-state contract.

### 5. `legacy max-address result ≠ physical native-capacity ceiling`

The legacy maximum-address command can return the legacy ceiling even when the device supports a larger native range reachable through its EXT counterpart.

The result is qualified by command semantics.

### 6. `wider LBA ≠ physical relocation or geometry exposure`

The 48-bit feature changes command/address width inside a logical block addressing regime. Case 89 already blocks reading logical address as physical location, while Case 108 separately owns actual physical ZBR geometry.

### 7. `device-side support ≠ end-to-end host-stack reachability`

Seagate's 2003 support note shows that the drive can be capable while a BIOS/controller/driver/OS path remains unable to safely use the larger namespace.

This is an important retention boundary: surviving payload is not sufficient for practical availability if the interpretation/addressing path is incompatible.

### 8. `address-interpretation failure ≠ media-retention failure`

In Seagate's bounded Windows warning, incorrect high-address handling can overwrite other logical content. The immediate failure relation is address interpretation/translation in the system path, not prior spontaneous decay of magnetic state.

---

## Prior-art / genealogy controls

### Do not claim ATA/ATAPI-6 invented LBA

Case 89 already grounds LBA in ATA-2/ATA-3 and Case 14 supplies earlier/parallel disk-controller evidence separating host LBA from physical target addresses.

### Do not turn the T13 proposal date into invention priority

`e00101r0` provides a public standards-development record by 10 January 2000. It does not exclude earlier vendor work, committee discussion, patent filings, controller designs, or related large-address schemes.

### Do not equate the working draft with the approved standard

The inspected 14 December 2001 1410D revision 3a explicitly labels itself an internal working document. T13's archive separately lists INCITS 361-2002.

### Do not infer a direct lineage into later SATA/ACS, 4Kn, GPT, or filesystem limits

Those later systems can be compared functionally only after their own sources are established.

### Route the larger history elsewhere

The full history of:

- BIOS INT 13h / EDD extensions;
- ATA proposal meetings and final revision genealogy;
- first >137 GB commercial drives;
- Windows/Linux/BSD adoption and bugs;
- HPA/DCO capacity controls;
- SATA / ACS continuation;
- MBR/GPT and 2 TiB partition boundaries;
- 512e/4Kn logical/physical-sector size;
- controller internals;

belongs primarily in `tmzncty/computing-archaeology`.

---

## Cross-case comparison matrix

| Relation | Case 113 ATA 48-bit reachability | Case 89 ATA CHS/LBA translation | Case 108 ZBR geometry | Case 14 defect reassignment |
| --- | --- | --- | --- | --- |
| Stable upper designation | LBA namespace | LBA of a logical sector | fixed logical block | LBA |
| What changes | command address width / reachable range | logical CHS representation | physical radial zone capacity | physical serving sector |
| Physical relocation established? | No | No for translation change | No dynamic relocation implied by zoning | Yes in reassignment path |
| Key control state | feature support + legacy/48-bit capacity + host support | current CHS translation/addressing mode | notch/zone layout + scoped parameters | defect/replacement metadata |
| Main failure boundary | high LBA not safely representable/interpretable by legacy stack | wrong coordinate interpretation / mode reach | physical/layout reliability is separate | grown defect / spare exhaustion |
| Historical identity | ATA/ATAPI-6 48-bit Address feature | ATA-2/ATA-3 translation | magnetic ZBR | SCSI/disk defect management |

The matrix is a layer decomposition, not a genealogy.

---

## Rejected / unsupported claims

- `ATA/ATAPI-6 invented LBA` — **rejected**.
- `10 January 2000 is the invention date of 48-bit LBA` — **unsupported / rejected**.
- `1410D revision 3a is the approved final standard` — **rejected by its own source-status statement**.
- `a 48-bit-capable drive no longer supports 28-bit commands` — **rejected**.
- `28-bit and 48-bit commands address two unrelated payload populations` — **rejected**.
- `high-LBA sectors do not physically exist because a legacy command cannot name them` — **rejected**.
- `the value in a capacity field alone proves 48-bit feature support` — **rejected**.
- `48-bit LBA moves existing sectors to new physical tracks` — **unsupported / rejected**.
- `48-bit LBA exposes physical CHS or ZBR geometry` — **rejected**.
- `48-bit LBA is the same transition as 4Kn/512e` — **rejected**.
- `drive support alone guarantees every BIOS/driver/OS can use the full drive` — **rejected**.
- `the Seagate Windows wrap warning is a universal ATA protocol behavior` — **rejected**; it is kept system/version-bounded.
- `Maxtor DiamondMax16 is proven to be the first >137 GB 48-bit ATA product` — **unsupported**.
- `larger address space means greater physical data-retention lifetime` — **rejected**.

---

## Evidence limits

1. The exact inspected normative text is T13/1410D revision 3a, a December-2001 working draft, not the purchased final INCITS 361-2002 text.
2. The T13 public document index establishes proposal chronology but not private design history or invention priority.
3. Maxtor supplies one named 2003 commercial product-family witness; first-shipping priority is unclaimed.
4. Seagate's wraparound warning is specific to the Windows/system configurations discussed in its 2003 note and must not be universalized.
5. No BIOS source code, Windows driver source, Linux/BSD implementation, or controller firmware is inspected.
6. No HPA/DCO/SET MAX interaction is reconstructed.
7. No platter geometry, zone allocation, defect map, or sector-relocation algorithm is inferred from LBA width.
8. No experiment writes across the 137 GB boundary under a deliberately incompatible stack.
9. No sector-size transition is included; this case assumes the bounded sources' logical-sector conventions.
10. No first-invention or direct later-genealogy claim is made.

---

## Grounded synthesis

The bounded sources establish a four-layer separation:

```text
retained logical-sector population on the device
        ≠
reachability through legacy 28-bit ATA commands
        ≠
reachability through 48-bit EXT commands
        ≠
end-to-end host-stack ability to interpret/use those commands safely
```

ATA/ATAPI-6 adds a wider LBA command regime while preserving the legacy command family. Maxtor's 160 GB DiamondMax16 provides a named 2003 witness that the larger namespace is not merely hypothetical, while Seagate's 2003 system note shows that device capability still does not guarantee full-stack reachability.

For `technical-retention`, the important result is not that 48 bits retain data better. It is more exact: **a retained object can remain on the medium yet fall outside the designation power of an older command/interpretation regime; preserving future availability therefore includes preserving enough addressing semantics and compatible machinery to reach the retained state.**
