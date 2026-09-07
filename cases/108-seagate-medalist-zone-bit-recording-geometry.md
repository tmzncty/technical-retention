# Seagate Medalist 1080sl Zone-Bit Recording: Logical Blocks Across Nonuniform Physical Geometry

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
