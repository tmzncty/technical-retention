from pathlib import Path
import subprocess

CASE_PATH = Path("cases/108-seagate-medalist-zone-bit-recording-geometry.md")
EVIDENCE_PATH = Path("evidence/108-seagate-1989-1995-zbr-geometry-grounding.md")
ROADMAP_PATH = Path("ROADMAP.md")
INDEX_PATH = Path("CASE_INDEX.md")
CASE89_PATH = Path("cases/89-ata-lba-chs-translation-logical-sector-identity.md")
WORKFLOW_PATH = Path(".github/workflows/case108-integration.yml")

case_text = r'''# Seagate Medalist 1080sl Zone-Bit Recording: Logical Blocks Across Nonuniform Physical Geometry

## Status

**`grounded`** — bounded to the physical zone/notch geometry exposed by Seagate's August 1995 Medalist 1080sl SCSI product manual, with an earlier 1989 National Semiconductor engineering note and a 1991-filed patent used only to establish a prior-art floor. This case does **not** claim a complete history of zone-bit recording, hard-disk geometry, SCSI/ATA addressing, servo design, or invention priority.

Grounding record: [`../evidence/108-seagate-1989-1995-zbr-geometry-grounding.md`](../evidence/108-seagate-1989-1995-zbr-geometry-grounding.md).

## Scope

The open HDD roadmap item still contains several different histories: physical recording geometry, defect reassignment, CHS/LBA representation, BIOS translation, interface capacity limits, and later controller implementation. Cases 14 and 89 already cover two of those relations. This case adds only the missing physical-layout bridge:

> How can a drive expose ordinary fixed-size logical blocks while the physical cylinders underneath them have **nonuniform block capacity** because the medium is divided into recording zones?

The bounded product is the Seagate ST51080N / Medalist 1080sl SCSI drive. The period manual uses `Zone Bit Recording`, `zone`, `notch`, `logical block`, `physical geometry`, `active notch`, `starting boundary`, `ending boundary`, and `pages notched`. Those terms are preserved below.

Project terms such as `logical identity`, `geometry abstraction`, and `retention relation` are engineering vocabulary, not claims about Seagate's own conceptual language.

## Historical record

### H/P — the named drive combines fixed-size logical sectors with explicit physical geometry and ZBR

Seagate's August 1995 product manual identifies the drive as Fast SCSI-2 and gives:

- formatted capacity: 1,080.23 MB;
- total sectors: 2,109,840;
- bytes per sector: 512;
- physical discs: 2;
- physical read/write heads: 4;
- physical cylinders: 4,826;
- Zone Bit Recording method: RLL (1,7);
- internal data-transfer rate: 33 to 65 Mbit/s.

The capacity figure explicitly excludes spare sectors and cylinders. The same page says the medium contains one spare sector per track and two spare cylinders per drive.

**Primary anchor:** Seagate, *Medalist 1080sl SCSI Interface Drive Product Manual*, Publication 36321-101, Rev. A, August 1995, printed p. 4 / PDF p. 13.

The fixed 512-byte logical-sector size therefore coexists with a physical recording scheme whose track/cylinder capacity is not uniform.

### H/P — outer cylinders contain more logical blocks than inner cylinders

The manual's SCSI Notch page (0Ch) states the physical-layout rule directly: the drive uses Zone Bit Recording, the outer cylinders contain more logical blocks than the inner cylinders, cylinders are organized into groups called `zones` or `notches`, every logical block belongs to a notch, and notches do not overlap.

This is stronger than saying merely that the drive has a hidden geometry. It is a period product statement that one logical-block interface spans a physical medium whose radial regions hold different numbers of those blocks.

**Primary anchor:** Seagate 1995, Appendix C.8, printed p. 95 / PDF p. 104.

### H/P — the product exposes retained/control state for the notch geometry

The same Notch page exposes fields for:

- maximum number of notches (`0013h` in the documented default, i.e. 19);
- active notch;
- starting boundary;
- ending boundary;
- a `pages notched` bitmap.

The manual says the `active notch` selects the notch to which the current and future Mode Select / Mode Sense operations refer until changed. When active notch is zero, the parameters apply to all notches.

For this drive the `logical or physical notch` (`LPN`) bit is zero, and the start/end boundaries are based on physical parameters of the logical unit. The boundary encoding uses cylinder and head fields. The `pages notched` bitmap identifies which mode pages may contain different parameter values for different notches.

**Primary anchor:** Seagate 1995, printed pp. 95–96 / PDF pp. 104–105.

The notch relation is therefore not only implicit in platter manufacturing. Some of its geometry and parameter scope is explicitly represented through interface-visible control metadata.

### H/P — earlier engineering material blocks a 1995-origin claim

National Semiconductor's 1989 *Mass Storage Handbook* includes Kern Wong's Application Note 599, `DP8459 Zoned Bit Recording`. The note treats ZBR as an engineering response to capacity pressure, contrasts it with a more continuously varying recording-rate scheme, and discusses implementation using a programmable read-channel/data-synchronizer device.

A separate patent family, US5257143A, filed 15 January 1991, is even more explicit about the novelty boundary. Its background calls zone-bit recording a **known technique** and describes concentric zones containing different numbers of sectors according to available track space. The claimed invention is instead about head/sector-position handling across zone changes.

These sources establish only that ZBR engineering and implementation problems predate the 1995 Medalist manual. They do not establish the first invention, first commercial product, or a direct National Semiconductor/US5257143A → Medalist implementation genealogy.

## Retained state and geometry state

This bounded case separates at least six classes of state or structure.

### 1. User payload

Each user sector contains 512 bytes in the documented product interface.

### 2. Logical-block designation

The host addresses logical blocks. The Notch page states that every logical block belongs to one physical zone/notch, but the logical block remains an interface object rather than a literal statement of sectors-per-track geometry.

### 3. Magnetic physical embodiment

Payload is magnetically recorded on the disk surfaces. Ordinary retention at rest is supplied by the magnetic medium, not by the ZBR metadata itself.

### 4. Physical radial geometry

The drive has physical cylinders, heads, tracks, and zones/notches. Different radial zones can contain different numbers of logical blocks per cylinder/track regime.

### 5. Notch boundary and parameter state

Active-notch selection, start/end boundaries, and `pages notched` determine which physical region and parameter set a Mode Sense/Select exchange refers to. This is control/interpretation state, not application payload.

### 6. Spare/defect-management capacity

The same manual exposes per-track and per-drive spare capacity, but that belongs to the distinct failure-repair relation grounded in Case 14. ZBR layout and defect substitution must not be collapsed merely because both involve physical sectors.

## Engineering reconstruction

### E — fixed logical-block size does not imply fixed physical track capacity

The drive keeps a 512-byte sector size while outer cylinders contain more logical blocks than inner cylinders.

> **same logical-block size ≠ same number of logical blocks per physical cylinder/track regime**.

A uniform object exposed to software can therefore be embodied by a nonuniform physical geometry.

### E — more blocks per outer cylinder does not mean larger logical blocks

ZBR takes advantage of longer outer tracks by changing how many fixed-size logical blocks fit in a radial region. It does not make each outer logical block semantically larger.

> **more logical blocks per outer cylinder ≠ more bytes per logical block**.

### E — geometry metadata is not payload

The active notch, physical start/end boundaries, and notch-specific mode-page applicability tell the drive/host how a region is parameterized. They do not encode the 512-byte user values stored in that region.

> **notch geometry/control state ≠ user payload**.

Yet losing or misinterpreting layout/control information can still make otherwise surviving magnetic states harder or impossible to access correctly. Geometry can therefore be retention-relevant without being the retained application value.

### E — active-notch selection is not payload relocation

Changing which notch a Mode Sense/Select operation refers to changes the scope of a control query/parameter operation. The source does not say that selecting a different active notch moves logical blocks between radial zones.

> **active-notch selection ≠ logical-block relocation**.

This is an important guardrail against reading every mapping/control field as a relocation command.

### E — variable physical transfer regime does not change the logical sector contract

The manual reports an internal transfer-rate range of 33–65 Mbit/s while separately exposing fixed 512-byte sectors and Fast SCSI-2 external transfer limits. Those are different layers.

> **physical-zone recording rate ≠ host logical-block size or external SCSI transfer contract**.

The product hides some geometry-dependent physical work behind a stable block service without making the physical differences unreal.

## Cross-case comparison

### A — ZBR is not CHS translation (Case 89)

Case 89 shows that ATA logical CHS parameters can be re-parameterized while a logical sector's LBA remains stable, and that logical CHS need not disclose actual media location.

Case 108 addresses a different layer: the **actual physical recording surface is radially nonuniform** because different zones contain different numbers of logical blocks.

So:

> **physical zone geometry ≠ host-visible CHS translation geometry**.

A drive may hide physical nonuniformity behind a logical address representation, but that does not make the two geometries identical or prove that one historically caused the other.

### A — ZBR is not defect reassignment (Case 14)

Case 14 grounds failure-triggered substitution of a spare physical sector for a defective physical location while preserving an upper logical designation when possible. ZBR, by contrast, is ordinary recording-layout geometry: zones determine how capacity is distributed across radial regions before a later grown-defect repair is considered.

> **zone layout ≠ defect-remap relation**.

The same product family can need both.

### A — ZBR is not an FTL (Case 04)

Mapped Flash dynamically preserves a logical/virtual designation while erase-constrained updates, reclamation, and remapping change current physical embodiments. The Seagate ZBR evidence here establishes a nonuniform physical geometry, not an erase-before-write mapping layer or dynamic relocation policy.

The only safe analogy is that a simple logical block interface can conceal a more complicated physical organization.

### A — physical layout can remain operative beneath an abstract address

Cases 04, 14, 89, and 108 now separate four different relations:

```text
Case 04  logical identity ↔ dynamic Flash mapping / reclamation
Case 14  logical identity ↔ failure-triggered disk-sector replacement
Case 89  LBA identity ↔ mutable logical-CHS representation
Case 108 logical blocks ↔ nonuniform physical zone/notch geometry
```

This is a functional decomposition, not a genealogy.

## Failure and forgetting

The bounded source set supports only a limited failure analysis.

- Magnetic media can fail independently of how zones are represented.
- Wrong or unavailable geometry/control information can impair resolution of a surviving physical recording.
- Defect reassignment can later substitute spare sectors, but Case 14 shows that address continuity and payload recovery are separate.
- The current case does not establish power-fail atomicity, controller firmware recovery, servo-sector failure, or a complete physical-to-LBA mapping algorithm.

ZBR itself is therefore not a generic `retention mechanism` like DRAM refresh. It is a physical-layout and access-interpretation regime that participates in whether retained magnetic state can be efficiently and correctly addressed.

## Prior art and novelty boundary

The 1995 Medalist manual is a strong named-product witness, not an origin date.

The evidence used here establishes a conservative floor:

- National Semiconductor was publishing a ZBR implementation/design application note in 1989;
- US5257143A, filed in January 1991, calls ZBR a known technique and describes different sector counts across zones;
- Seagate documents a shipping-product ZBR/notch contract in August 1995.

This does **not** prove:

- who first invented zoned recording;
- when the first hard-disk ZBR product shipped;
- direct lineage among the three sources;
- that all ZBR drives use Seagate's Notch-page semantics;
- or that later HDD physical layout can be reconstructed from this one 1995 product.

The complete recording-technology and product genealogy belongs primarily in `computing-archaeology` if pursued.

## Philosophical limit

### I — abstraction does not eliminate material differentiation

Case 108 supplies one narrow conceptual correction: a uniform logical-block service can remain usable even though the physical substrate is deliberately nonuniform across radius.

That does not make the logical block immaterial. The magnetic surface, head position, zone boundaries, read-channel rate, controller state, and defect/spare machinery are precisely what make the apparently regular block service possible.

The case can therefore discipline claims about `addressability` or `availability`, but it does not by itself establish `Bestand`, `tertiary retention`, or a general metaphysics of virtual objects.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Medalist 1080sl uses ZBR and exposes fixed 512-byte sectors | H/P | strong: Seagate 1995 printed p. 4 |
| outer cylinders contain more logical blocks than inner cylinders | H/P | strong: Seagate 1995 printed p. 95 |
| cylinders are grouped into nonoverlapping zones/notches and every logical block belongs to one | H/P | strong: Seagate 1995 printed p. 95 |
| active-notch, boundary, and pages-notched state are exposed by the product | H/P | strong: Seagate 1995 printed pp. 95–96 |
| fixed logical-sector size = uniform physical track capacity | X | directly contradicted by named-product ZBR semantics |
| active-notch selection = payload relocation | X | not established |
| ZBR = CHS translation | X | contradicted by cross-case layer separation |
| ZBR = defect reassignment | X | contradicted by Case 14 / product semantics |
| ZBR = Flash Translation Layer | X | functional analogy only, not mechanism identity |
| August 1995 manual = ZBR invention date | X | blocked by 1989/1991 prior-art floor |
| 1989/1991 prior art = proven direct genealogy into Medalist | X | not established |

## Related repositories

A current GitHub search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `zone bit recording`, `Medalist 1080`, and disk-geometry/logical-block combinations did not expose a dedicated ZBR history to reuse. If the broader recording-history question is pursued, that repository should own the full engineering chronology, read-channel/servo constraints, and product lineage.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the anti-anachronism guard: `logical identity`, `geometry abstraction`, and `retention relation` are modern project vocabulary unless period sources independently use them.

## Sources

1. Seagate Technology, **_Medalist 1080sl SCSI Interface Drive Product Manual_**, Publication Number 36321-101, Rev. A, August 1995. Primary anchors: printed p. 4 and Appendix C.8 printed pp. 95–96. <https://www.seagate.com/support/disc/manuals/scsi/518pmra1.pdf>
2. Kern Wong, National Semiconductor, **_DP8459 Zoned Bit Recording_**, Application Note 599, in the 1989 *National Mass Storage Handbook*, Section 2, around handbook p. 2-163. <https://bitsavers.computerhistory.org/components/national/_dataBooks/1989_National_Mass_Storage_Handbook/1989_Mass_Storage_Handbook_02.pdf>
3. Saied Zangenehpour, **US5257143A, _Method and apparatus for positioning head of disk drive using zone-bit-recording_**, filed 15 January 1991, issued 26 October 1993. Used for the earlier `known technique` / multi-zone sector-count floor, not as a first-invention certificate. <https://patents.google.com/patent/US5257143A/en>
'''

evidence_text = r'''# Evidence 108 — Seagate 1989–1995 Zone-Bit Recording Geometry Grounding

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
'''

if CASE_PATH.exists() or EVIDENCE_PATH.exists():
    raise SystemExit("Case 108 or Evidence 108 already exists; aborting to avoid duplicate work")

CASE_PATH.write_text(case_text, encoding="utf-8")
EVIDENCE_PATH.write_text(evidence_text, encoding="utf-8")

roadmap = ROADMAP_PATH.read_text(encoding="utf-8")
lines = roadmap.splitlines()
idx = next((i for i, line in enumerate(lines) if line.startswith("- [ ] HDD geometry, bad-sector remapping, CHS → LBA —")), None)
if idx is None:
    raise SystemExit("ROADMAP HDD anchor not found")
if "Case 108" in lines[idx] or "cases/108-seagate-medalist-zone-bit-recording-geometry.md" in roadmap:
    raise SystemExit("ROADMAP already mentions Case 108")
completed = "- [x] Seagate Medalist 1080sl Zone Bit Recording physical-zone / logical-block geometry boundary — [`cases/108-seagate-medalist-zone-bit-recording-geometry.md`](cases/108-seagate-medalist-zone-bit-recording-geometry.md), grounded by [`evidence/108-seagate-1989-1995-zbr-geometry-grounding.md`](evidence/108-seagate-1989-1995-zbr-geometry-grounding.md): the August 1995 named-drive manual keeps 512-byte logical sectors while outer physical cylinders carry more logical blocks than inner cylinders, groups cylinders into nonoverlapping zones/notches, and exposes physical notch boundaries plus notch-scoped parameter state. National Semiconductor AN-599 (1989) and a 1991-filed ZBR patent provide an earlier engineering/prior-art floor. This closes only the bounded `fixed logical-block service vs nonuniform physical recording geometry` relation; complete ZBR invention/product genealogy, track/servo/read-channel implementation, BIOS/ATA geometry history, LBA28→LBA48, and modern physical-layout validation remain open and belong primarily in `computing-archaeology`."
line = lines[idx].replace("Cases 14 and 89", "Cases 14, 89, and 108")
needle = " The broad item stays unchecked because"
if needle not in line:
    raise SystemExit("ROADMAP broad-item continuation anchor not found")
case108_clause = " [`cases/108-seagate-medalist-zone-bit-recording-geometry.md`](cases/108-seagate-medalist-zone-bit-recording-geometry.md), grounded by [`evidence/108-seagate-1989-1995-zbr-geometry-grounding.md`](evidence/108-seagate-1989-1995-zbr-geometry-grounding.md), now adds the physical-layout axis: fixed 512-byte logical sectors coexist with nonuniform ZBR zone/notch capacity, physical boundaries, and notch-scoped parameter state without implying dynamic block relocation."
line = line.replace(needle, case108_clause + needle, 1)
lines[idx:idx+1] = [completed, line]
ROADMAP_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

case89 = CASE89_PATH.read_text(encoding="utf-8")
anchor89 = "This case advances the open `HDD tracks / heads / cylinders / sectors; CHS → LBA` item without pretending to be a complete history of disk geometry.\n"
if anchor89 not in case89:
    raise SystemExit("Case 89 continuation anchor not found")
if "Case 108" in case89:
    raise SystemExit("Case 89 already links Case 108")
case89 = case89.replace(anchor89, anchor89 + "\nThe physical-layout counterpart is grounded separately in [Case 108](108-seagate-medalist-zone-bit-recording-geometry.md): Seagate's 1995 Medalist ZBR/notch contract shows that fixed-size logical blocks can span a medium whose outer and inner physical cylinders have different block capacities. That link is a layer decomposition, not a claim that CHS translation and ZBR are the same mechanism.\n", 1)
CASE89_PATH.write_text(case89, encoding="utf-8")

index = INDEX_PATH.read_text(encoding="utf-8")
if "## Case 108 — Seagate Medalist ZBR findings" in index or "1666. **fixed logical-block size" in index:
    raise SystemExit("CASE_INDEX already contains Case 108 findings")
if "1665. **Atlas paging ≠ universal later virtual-memory copy policy**" not in index:
    raise SystemExit("CASE_INDEX expected latest finding 1665 not found")
findings = r'''

## Case 108 — Seagate Medalist ZBR findings

1666. **fixed logical-block size ≠ uniform physical track/cylinder capacity** — the Medalist 1080sl keeps 512-byte sectors while its ZBR layout places more logical blocks on outer cylinders than inner cylinders.
1667. **more logical blocks per outer cylinder ≠ larger logical block** — ZBR changes how many fixed-size blocks fit in a radial region rather than changing the host-visible byte size of each logical sector.
1668. **logical-block service ≠ exposed physical geometry** — every logical block belongs to a notch, yet the host-facing block abstraction does not itself state a constant sectors-per-track geometry.
1669. **notch membership/boundaries ≠ user payload** — physical zone boundaries and the relation identifying which notch is active qualify layout/control interpretation rather than encoding the 512-byte application value.
1670. **active-notch selection ≠ payload relocation** — changing which notch Mode Sense/Select refers to changes control/query scope; the bounded source does not say that this operation moves logical blocks between zones.
1671. **notch-specific parameter scope ≠ one uniform physical operating regime** — `pages notched` explicitly permits some mode-page parameters to differ by notch while other pages remain common across the drive.
1672. **internal ZBR data-rate range ≠ external SCSI transfer contract** — the manual separately reports a 33–65 Mbit/s internal range, fixed-size sectors, and external Fast SCSI-2 transfer limits; physical recording rate and interface service are different layers.
1673. **ZBR physical geometry ≠ ATA logical-CHS translation** — Case 108 concerns real radial layout differences, whereas Case 89 concerns mutable host-visible logical-coordinate representation and explicitly blocks equating logical CHS with actual media coordinates.
1674. **ZBR zone layout ≠ defect reassignment** — ordinary radial capacity zoning differs from Case 14's failure-triggered spare-sector substitution even though both operate below a stable logical-block service.
1675. **ZBR ≠ Flash Translation Layer** — a nonuniform magnetic recording geometry does not imply erase-before-write, dynamic mapping, garbage collection, or wear-leveling semantics from Case 04.
1676. **physical-zone membership ≠ guaranteed lifetime physical-location stability** — the ZBR layout describes ordinary geometry, while Case 14 independently shows a later defect can substitute a different physical sector for the same logical designation.
1677. **geometry abstraction ≠ geometry disappearance** — hidden radial structure still shapes capacity, internal transfer regime, notch boundaries, and controller/positioning obligations even when software receives regular logical blocks.
1678. **August 1995 named-product documentation ≠ ZBR invention date** — National Semiconductor AN-599 (1989) already treats Zoned Bit Recording as an engineering design topic, and a January-1991-filed patent calls zone-bit recording a known technique.
1679. **earlier ZBR prior art ≠ demonstrated Medalist genealogy** — chronological and functional similarity do not prove that the Medalist uses the DP8459 implementation or the 1991 patent's positioning circuit.
1680. **Cases 14/89/108 form a layer decomposition, not one remapping genealogy** — defect replacement, logical CHS/LBA representation, and physical zone/notch geometry can all sit beneath logical block service while retaining different triggers, metadata, and historical vocabularies.
'''
INDEX_PATH.write_text(index.rstrip() + findings + "\n", encoding="utf-8")

# Validation before making the research commit.
for path in (CASE_PATH, EVIDENCE_PATH, ROADMAP_PATH, INDEX_PATH, CASE89_PATH):
    if not path.exists():
        raise SystemExit(f"missing expected file: {path}")

checks = {
    CASE_PATH: ["**`grounded`**", "fixed logical-block size ≠ same number", "Case 89", "US5257143A"],
    EVIDENCE_PATH: ["printed pp. 95–96", "AN-599", "fixed 512-byte block ≠ uniform physical track capacity"],
    ROADMAP_PATH: ["cases/108-seagate-medalist-zone-bit-recording-geometry.md", "Cases 14, 89, and 108"],
    INDEX_PATH: ["## Case 108 — Seagate Medalist ZBR findings", "1680. **Cases 14/89/108 form a layer decomposition"],
    CASE89_PATH: ["The physical-layout counterpart is grounded separately in [Case 108]"],
}
for path, needles in checks.items():
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"validation failed for {path}: {needle}")

subprocess.run(["git", "diff", "--check"], check=True)

# One-shot integration files must not survive in the research tree.
Path(__file__).unlink()
if WORKFLOW_PATH.exists():
    WORKFLOW_PATH.unlink()
