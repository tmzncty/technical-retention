# Evidence 108 — Seagate 1989–1995 Zone-Bit Recording Geometry Grounding

## Purpose

This record grounds [`../cases/108-seagate-medalist-zone-bit-recording-geometry.md`](../cases/108-seagate-medalist-zone-bit-recording-geometry.md).

The bounded question is not `who invented ZBR?` and not `how do all HDDs map LBAs to platter sectors?`. It is narrower:

> Can a named hard disk expose fixed-size logical blocks while the underlying physical cylinders are organized into zones with different logical-block capacity, and what retained/control state makes that geometry explicit?

## Evidence hierarchy

### Primary source A — Seagate Medalist 1080sl product manual, August 1995

**Document:** Seagate Technology, *Medalist 1080sl SCSI Interface Drive Product Manual*, Publication Number 36321-101, Rev. A, August 1995.

**URL:** <https://www.seagate.com/support/disc/manuals/scsi/518pmra1.pdf>

**Inspection status:** direct page-preserving PDF inspection completed for the core claims, including printed p. 4 / PDF p. 13 and printed pp. 95–96 / PDF pp. 104–105.

#### Anchor A1 — publication identity

PDF p. 3 identifies Publication Number 36321-101, Rev. A, August 1995.

Use: dates and identifies the named product manual. It is a product-contract witness, not an invention date.

#### Anchor A2 — formatted capacity, physical geometry, ZBR, sector size, internal-rate range

Printed p. 4 / PDF p. 13 gives:

- formatted capacity 1080.23 MB;
- total sectors 2,109,840;
- capacities exclude spare sectors/cylinders;
- one spare sector per track and two spare cylinders per drive;
- 2 discs, 4 read/write heads, 4,826 physical cylinders;
- Fast SCSI-2 interface;
- `Zone Bit Recording method RLL (1,7)`;
- internal data transfer 33 to 65 Mbit/s;
- spindle speed 5,376 RPM ±0.5%;
- 512 bytes per sector.

**Supported claims:** fixed logical sector size coexists with an explicitly zoned physical recording regime; physical geometry and spare geometry are distinct from the user-data capacity figure; internal physical transfer regime is not identical to the external SCSI contract.

**Does not support:** exact per-zone sector counts, an LBA→physical-sector reconstruction algorithm, or a statement that every logical block moves during operation.

#### Anchor A3 — product definition of Zone Bit Recording

Appendix C.8, printed p. 95 / PDF p. 104, says the drive uses Zone Bit Recording and explains that:

- outer cylinders contain more logical blocks than inner cylinders;
- cylinders are grouped into `zones or notches`;
- every logical block is part of a notch;
- notches do not overlap.

**Supported claims:** nonuniform physical radial capacity beneath one logical-block service; period terminology `zone` / `notch`; logical-block membership in a physical zone.

**Does not support:** logical-block relocation across zones, one universal ZBR topology, or a complete track/servo implementation.

#### Anchor A4 — Notch-page control and geometry fields

Printed p. 95 / PDF p. 104 exposes:

- maximum number of notches: `0013h`;
- active notch;
- starting boundary;
- ending boundary;
- pages-notched bitmap;
- `ND` and `LPN` bits.

The text states that the notch recording densities are not the same and that, with `LPN=0`, notch boundaries are based on physical parameters of the logical unit, with cylinder/head significance specified.

Printed p. 96 / PDF p. 105 says:

- `active notch` scopes the current and future Mode Select / Mode Sense commands until changed;
- active notch 0 refers to parameters applying to all notches;
- start/end boundaries encode cylinder/head when LPN=0;
- `pages notched` tells which mode pages may contain different parameters for each notch.

**Supported claims:** the physical zone relation has explicit boundary/scope metadata; some operational parameterization may differ by notch; active-notch selection is query/control scope.

**Does not support:** that changing the active-notch field relocates user data, or that the host can arbitrarily rewrite the manufactured physical zone layout.

### Primary source B — National Semiconductor AN-599, 1989

**Document:** Kern Wong, National Semiconductor, *DP8459 Zoned Bit Recording*, Application Note 599, in the 1989 *National Mass Storage Handbook*, Section 2, around p. 2-163.

**URL:** <https://bitsavers.computerhistory.org/components/national/_dataBooks/1989_National_Mass_Storage_Handbook/1989_Mass_Storage_Handbook_02.pdf>

The surviving scanned handbook/searchable text presents ZBR as a disk-capacity engineering technique and discusses a DP8459 data-synchronizer implementation. The note contrasts fully continuously varying recording-rate ideas with a zoned compromise and ties the problem to multiple data rates/read-channel electronics.

**Use in Case 108:** prior-art / engineering floor only: ZBR was already a named engineering subject in a semiconductor vendor application note by 1989.

**Not used to establish:** first invention, first product, Seagate implementation lineage, exact Medalist notch semantics, or universal hard-disk history.

### Primary source C — US5257143A, filed 1991

**Document:** Saied Zangenehpour, *Method and apparatus for positioning head of disk drive using zone-bit-recording*, US5257143A; filed 15 January 1991, issued 26 October 1993.

**URL:** <https://patents.google.com/patent/US5257143A/en>

#### Anchor C1 — ZBR is described as known technique

Background, around the discussion corresponding to patent text lines 170–172 in the public transcription, calls zone-bit recording a `known technique`. It says several concentric zones may contain one or more tracks and that each zone is divided into a different number of sectors according to available space.

**Supported claim:** by January 1991, this patent applicant treated multi-zone/different-sector-count recording as prior/known art rather than the novelty of the patent.

**Does not support:** who invented ZBR, when it first shipped, or whether the patent's background is a complete history.

#### Anchor C2 — zone crossing changes positional bookkeeping

The patent's claimed mechanism handles a head moving between zones with different sector counts and resets/qualifies sector-position counting after the new zone/index condition. Later description explains that a sector count valid in one zone can become invalid after crossing into a zone with a different sectors-per-track relation.

**Supported claim:** nonuniform zone geometry creates concrete controller/positioning obligations; geometry is operational, not decorative terminology.

**Does not support:** the Seagate Medalist's exact controller circuit or a direct implementation genealogy.

## Source boundary and rejected shortcuts

### 1. 1995 product manual ≠ invention date

The 1989 National Semiconductor application note and 1991-filed patent both predate the Medalist manual. The 1995 source is used because it is a strong named-product witness with explicit logical-block/notch semantics.

### 2. earlier source ≠ proven genealogy

Chronology alone does not show that the Medalist 1080sl inherited a particular National Semiconductor circuit or the patented positioning method.

### 3. ZBR ≠ CHS translation

Case 89 concerns a host-visible logical-coordinate representation whose parameters can change while a logical sector's LBA does not. Evidence 108 concerns radial recording geometry that really differs across physical zones.

### 4. ZBR ≠ defect reassignment

Case 14 concerns replacement of defective physical sectors and the mapping/repair relation around an LBA. The Medalist manual's spare geometry is relevant context, but ordinary ZBR zone layout is not itself a grown-defect replacement event.

### 5. ZBR ≠ FTL

Case 04 concerns erase-constrained dynamic mapping and reclamation. A nonuniform disk zone layout does not supply that mechanism.

### 6. fixed 512-byte block ≠ uniform physical track capacity

This is the central bounded result and is directly supported by combining Seagate's 512-byte sector specification with its statement that outer cylinders contain more logical blocks than inner cylinders.

### 7. physical geometry difference ≠ automatic payload movement

Neither the Notch page nor the supporting prior art says that ordinary active-notch selection or existence of zones dynamically migrates a logical block from one zone to another.

## Related-repository check

Current code searches of `tmzncty/computing-archaeology` for `zone bit recording`, `Medalist 1080`, and disk-geometry/logical-block combinations returned no dedicated ZBR case to reuse. The broad engineering history remains better placed there if later research pursues:

- early zoned-recording priority and product chronology;
- track/servo/read-channel implementation;
- exact physical-to-logical mapping algorithms;
- BIOS/IDE/ATA capacity barriers;
- LBA28→LBA48;
- modern named-drive physical-layout validation.

`technical-retention` keeps only the retention-specific relation among logical blocks, physical zone geometry, notch metadata, and hidden access infrastructure.

## Evidence strength summary

| Claim | Strength | Reason |
| --- | --- | --- |
| named 1995 drive uses ZBR with 512-byte sectors | **strong primary** | direct Seagate product manual, printed p. 4 |
| outer cylinders contain more logical blocks than inner cylinders | **strong primary** | direct Seagate Notch-page definition, printed p. 95 |
| zones/notches are nonoverlapping and every logical block belongs to one | **strong primary** | direct Seagate Notch-page definition |
| physical notch boundaries and notch-scoped parameter state are exposed | **strong primary** | direct Seagate pp. 95–96 |
| ZBR engineering predates 1995 Medalist | **strong prior-art floor** | 1989 National Semiconductor AN-599 + 1991-filed patent |
| 1989/1991 source directly caused Medalist implementation | **unsupported** | chronology/function alone do not prove lineage |
| active-notch selection moves payload | **unsupported / rejected** | control-scope semantics do not state relocation |
| ZBR closes complete HDD geometry history | **unsupported / rejected** | bounded product case only |
