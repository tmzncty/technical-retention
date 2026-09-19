# Evidence 130B — IBM 2003–2010 LTO bridge-generation and host-path deepening

**Case:** [`cases/130-lto-generational-compatibility-reader-obsolescence.md`](../cases/130-lto-generational-compatibility-reader-obsolescence.md)

**Status:** `bounded deepening complete`

## Research question

This slice asks two deliberately narrow questions left open by the initial Case 130 grounding:

1. Can the repository replace a purely current compatibility summary with contemporaneous or period IBM product evidence showing how an older LTO cartridge moved from **read/write** to **read-only** and then out of a later drive's supported media set?
2. Can the repository directly ground the additional claim that preserving the cartridge and even preserving a compatible drive does not by itself preserve a documented access path, because the drive also depends on a host interface, supported host platform / OS, and a usable software / driver path?

The slice does **not** attempt to reconstruct the whole LTO specification history, identify the inventor of backward compatibility, infer undocumented head geometry, or prove that every unsupported combination is physically impossible to operate with unofficial adapters or software.

Repository labels follow normal convention:

- `H/P` — historical / primary or contemporaneous vendor record;
- `H/S` — later official institutional or vendor continuity evidence;
- `E` — engineering reconstruction from the records;
- `A` — functional comparison only;
- `I` — philosophical interpretation;
- `X` — explicit rejected overclaim.

## Anti-duplication check

Before opening this slice, the current Case 130 canonical and its grounding packet were reviewed. They already establish from current LTO Program and IBM compatibility matrices that:

- compatibility is generation-bounded;
- read and write compatibility are different axes;
- later generations do not monotonically read every older LTO cartridge;
- a mixed-generation library can be constrained by the intersection of drive/media support sets.

The open gaps explicitly included:

- direct primary / period chronology for earlier generations; and
- host-interface and driver obsolescence above a preserved drive.

A fresh search of `tmzncty/computing-archaeology` for `LTO` returned no existing dedicated packet to reuse. This evidence therefore stays on the retention seam and leaves the broader SCSI / Fibre Channel / SAS and tape-device genealogy to that companion repository.

## Source set

### S1 — IBM TotalStorage Ultrium Tape Drive 3580 Model L23 overview, 2003

IBM Support, **Overview — IBM TotalStorage Ultrium Tape Drive (3580-L23)**:

<https://www.ibm.com/support/pages/overview-ibm-totalstorage-ultrium-tape-drive-3580-l23>

The IBM page records:

- worldwide announce date: **9 September 2003**;
- planned availability date: **12 September 2003**;
- product: IBM TotalStorage Ultrium 2 Tape Drive, 3580 Model L23;
- the LTO-2 drive can **read and write original LTO Ultrium data cartridges** at the original LTO-1 capacity;
- the new 200 GB LTO-2 cartridge is for the new LTO-2 drive;
- the drive uses an **Ultra160 SCSI Low Voltage Differential (LVD)** attachment;
- the package includes a SCSI terminator, SCSI cables, open-systems device drivers, and a device-driver installation / user's guide;
- IBM lists supported host families and minimum operating-system levels and points users to its interoperability matrix for current supported server / OS combinations;
- the SCSI attachment has cable-length and topology limits.

**Classification:** `H/P` for the dated product announcement / product documentation record preserved by IBM Support.

**Why it matters:** this source simultaneously records media-generation compatibility and the surrounding host attachment / driver contract. It therefore supports a more complete access relation than `cartridge + drive` alone.

### S2 — IBM 400/800 GB LTO-3 Tape Drive User's Guide landing record, 2005

IBM Support, **User's Guide — IBM 400/800GB LTO 3 tape drive**:

<https://www.ibm.com/support/pages/users-guide-ibm-400800gb-lto-3-tape-drive>

IBM records the User's Guide release date as **5 May 2005** and identifies the downloadable IBM guide as `39m5625.pdf`.

**Classification:** `H/P` for publication chronology.

**Boundary:** this landing record is used here to anchor the existence and date of IBM's LTO-3 product guide. Compatibility semantics below are taken from the IBM 3583 support record rather than reconstructed from an inaccessible or mirrored PDF copy.

### S3 — IBM TotalStorage 3583 Setup and Operator Guide support record, 2003/2005

IBM Support, **IBM TotalStorage Ultrium Scalable Tape Library 3583 Setup and Operator Guide for Multi-path Libraries**:

<https://www.ibm.com/support/pages/ibm-totalstorage-ultrium-scalable-tape-library-3583-setup-and-operator-guide-multi-path-libraries>

IBM identifies publication number `GA32-0411-06`, copyright **2003, 2005**. Its support abstract states:

- new LTO-3 drives read and write LTO-2 cartridges;
- LTO-3 drives **read** LTO-1 cartridges;
- LTO-3 drives and cartridges can coexist in the same 3583 library with LTO-1 and LTO-2 drives / cartridges;
- LTO-3 drive features were available with **LVD Ultra160 SCSI** and **2 Gbps switched-fabric Fibre Channel** attachment;
- storage and tape management depend on software such as Tivoli Storage Manager and other compatible offerings.

**Classification:** `H/P` / period IBM product documentation preserved on the vendor support site.

**Why it matters:** this is the direct bridge-generation witness. The LTO-1 cartridge that was read/write on IBM's 2003 LTO-2 drive is described only as readable by the LTO-3 drive.

### S4 — IBM Half-High LTO Generation 3 / 4 SAS product overview

IBM Support, **Overview — IBM Half-High LTO Gen 3 External SAS Tape Drive, IBM Half-High LTO Gen 4 External SAS Tape Drive**:

<https://www.ibm.com/support/pages/overview-ibm-half-high-lto-gen-3-external-sas-tape-drive-ibm-half-high-lto-gen-4-external-sas-tape-drive>

The preserved IBM overview records:

- LTO Gen 3 SAS drive: read/write LTO Gen 2, read LTO Gen 1;
- LTO Gen 4 SAS drive: read/write LTO Gen 3 and read LTO Gen 2;
- both product paths use a **6 Gbps SAS host interface** in the documented configurations;
- IBM lists supported System x combinations, supported operating systems and backup software;
- documented internal / external use requires a supported SAS host-bus adapter, and some paths require a supported enclosure / adapter kit.

The page was later maintained by IBM Support, so it is used as **official continuity / product-configuration evidence**, not as a precise announcement-date witness for every listed Gen 3 / Gen 4 model.

**Classification:** `H/S` official vendor continuity / configuration record.

### S5 — IBM current cartridge compatibility table

IBM Documentation, **Cartridge Compatibility**:

<https://www.ibm.com/docs/en/t-tt-and-t?topic=cartridges-cartridge-compatibility>

The current IBM table gives the operation matrix explicitly:

- LTO-2 drive: LTO-2 and LTO-1 read/write;
- LTO-3 drive: LTO-3 and LTO-2 read/write, LTO-1 read-only;
- LTO-4 drive: LTO-4 and LTO-3 read/write, LTO-2 read-only, with no LTO-1 support cell;
- later generations continue the bounded matrix described in the grounding packet.

**Classification:** `H/S` current official compatibility continuity.

**Use:** corroborates the bridge-generation sequence and makes the LTO-1 / LTO-4 unsupported endpoint explicit. It is not used to date when the original product policy was invented.

## Historical record

### H/P — IBM LTO-2 exposed an explicit migration bridge in 2003

At announcement in September 2003, IBM documented the 3580 L23 LTO-2 drive as able to read and write original LTO-1 cartridges.

For an LTO-1 cartridge, the operation relation in this product record is therefore:

```text
LTO-1 cartridge + IBM LTO-2 drive + READ  -> supported
LTO-1 cartridge + IBM LTO-2 drive + WRITE -> supported
```

This is not a current-program retrospective alone; it is a dated IBM product record.

### H/P — by the LTO-3 bridge, LTO-1 had become read-only

The 2005-era IBM 3583 material states that LTO-3 drives read/write LTO-2 but read LTO-1.

For the same older media generation, the operation relation had narrowed:

```text
LTO-1 cartridge + IBM LTO-3 drive + READ  -> supported
LTO-1 cartridge + IBM LTO-3 drive + WRITE -> not documented as supported
```

This gives a clean period witness for the project's existing distinction:

> **recoverability window != rewrite window.**

The LTO-1 payload could still be extracted through the documented LTO-3 path after rewrite support had already disappeared from that path.

### H/S — the next bridge no longer includes LTO-1

IBM's official Gen 3 / Gen 4 product overview and current compatibility table put the LTO-4 compatibility set at LTO-4 / LTO-3 read-write plus LTO-2 read support. LTO-1 is outside that documented set.

So the bounded sequence for **one media generation** is:

```text
LTO-1 on LTO-2: read/write
LTO-1 on LTO-3: read-only
LTO-1 on LTO-4: unsupported in the documented compatibility matrix
```

This sequence is more informative than a generic statement that a drive can "read two generations back": it shows the operation authority changing in stages while the cartridge itself need not change at all.

### H/P — the documented reader path already included host attachment and software constraints

The 2003 LTO-2 record does not describe a reader as an isolated mechanism. The documented path includes:

- Ultra160 LVD SCSI attachment;
- server / workstation families that support that interface;
- specified minimum OS levels;
- open-systems device drivers;
- storage / tape management software obtained separately;
- cable and bus-topology limits.

The 2005 3583 record likewise gives LVD SCSI and Fibre Channel attachment variants, and the later Gen 3 / Gen 4 overview shows SAS host-bus-adapter and platform compatibility requirements.

Historical claim boundary:

> IBM documented LTO drives as components of a host attachment / software compatibility relation, not as media readers independent of the rest of the system.

This does **not** prove that any configuration omitted from the vendor matrix is physically incapable of operation.

## Engineering reconstruction

### E — bridge-generation compatibility is a staged authority horizon

A useful reconstruction from the LTO-1 sequence is:

```text
media remains physically present
    + generation N reader
        -> read/write authority
    + generation N+1 reader
        -> read-only authority
    + generation N+2 reader
        -> no documented media authority
```

For the named LTO-1 / LTO-2 / LTO-3 / LTO-4 sequence above, this is directly instantiated by IBM's compatibility records.

The general pattern must not be projected mechanically onto every later generation: LTO-8/9 and especially LTO-10 have different official compatibility windows, already documented in the Case 130 grounding packet.

### E — a migration obligation can begin before the last read path disappears

Once an older medium has entered a read-only generation, an operator still has a documented extraction path but no longer has the same in-place rewrite relation on that drive.

Therefore the retention-relevant transition is not only:

```text
readable -> unreadable
```

but also:

```text
read/write -> read-only -> unsupported
```

This makes the **last writable bridge** and the **last readable bridge** distinct planning boundaries.

No universal migration cadence follows from this evidence.

### E — preserving a drive is not identical to preserving a usable reader path

The 2003 IBM 3580 L23 record directly supports the following more complete relation:

```text
surviving cartridge
  + compatible LTO drive
  + compatible host attachment
  + supported / workable host adapter and cabling
  + usable driver / OS / application path
  -> documented access path
```

The first two terms are necessary to the bounded Case 130 claim, but the IBM product record shows that the vendor-supported access path was wider than those two objects.

Thus:

> **drive survival != host attachability.**

and:

> **host attachability != supported software path.**

and therefore:

> **media + drive survival != documented end-to-end recoverability.**

### E — interface succession creates a second obsolescence axis

The named records span Ultra160 LVD SCSI, switched-fabric Fibre Channel, and later SAS product paths.

The defensible retention conclusion is not "old interfaces make old drives impossible to use." It is narrower:

- drive/media compatibility and host-interface compatibility are different relations;
- preserving the correct tape drive does not automatically preserve a supported HBA / cable / platform / driver path;
- migration planning can therefore fail at the **apparatus-to-host** boundary even when the **media-to-drive** boundary remains satisfied.

### E — compatibility support is relational at more than one layer

For a retained cartridge `M`, tape drive `D`, host attachment `H`, and software path `S`, the project can now use the layered form:

```text
media_admissible(M,D,operation)
  AND host_attachable(D,H)
  AND software_usable(H,S)
  -> documented access path
```

This is a model of the evidence, not IBM source terminology.

It prevents an overly simple statement such as "the archive is readable because we kept an LTO-2 drive."

## Functional comparisons

### A — Case 129 / ZFS feature flags

Both cases require an interpreter / access apparatus that understands retained state, but the gates differ:

- Case 129: software-format / feature semantics;
- Case 130: physical media-generation relation plus hardware attachment and software path.

Therefore:

```text
software-format admissibility != media/drive admissibility != host attachment admissibility
```

No genealogy is implied.

### A — Case 89 / ATA LBA-CHS addressing

Both cases show that retained payload is accessed through a translation / apparatus relation rather than by physical persistence alone. ATA address translation and LTO generation compatibility are unrelated mechanisms.

### A — Case 111 / enterprise SSD extended shutdown

Case 111 can fail through physical charge-retention degradation while the controller remains otherwise compatible. Case 130 can fail with perfectly surviving magnetic state because one of the required reader / attachment layers disappears.

Therefore:

```text
physical media decay != access-apparatus obsolescence
```

## Philosophical interpretation

### I — access can age without the inscription changing

The LTO-1 sequence is a particularly clean example of relational obsolescence. The same cartridge can pass through read/write, read-only, and unsupported relations as the available reader generation changes, without requiring the recorded magnetic state itself to change.

This is a project interpretation, not IBM historical vocabulary.

### I — retention can require preserving a chain rather than an object

The 2003 product record shows that even "keep the old drive" is incomplete. Practical legibility may depend on a chain:

```text
medium -> drive -> interface -> host -> driver/software
```

A break at any layer can retire the practical access path while the lower-layer objects remain intact.

Again, this is a project interpretation.

## Explicit non-claims / rejected upgrades

This evidence does **not** establish that:

1. LTO invented backward compatibility. (`X`)
2. IBM invented the two-generation read / one-generation write pattern. (`X`)
3. every LTO implementation had exactly the same host-interface options as the named IBM products. (`X`)
4. an LTO-1 cartridge becomes physically unreadable merely because an LTO-4 drive is present. (`X`)
5. LTO-4 physically cannot load an LTO-1 cartridge; the claim is only that the IBM compatibility matrix does not support that media/operation path. (`X`)
6. every configuration omitted from IBM's supported-server matrix is technically impossible. (`X`)
7. preserving an Ultra160 SCSI adapter is sufficient to preserve the entire 3580 L23 access path. (`X`)
8. a modern protocol converter necessarily restores a vendor-supported path to every old drive. (`X`)
9. the 2003 Windows / Linux version list is a timeless lower or upper bound on what software could ever operate the drive. (`X`)
10. Fibre Channel, SCSI, and SAS variants share identical firmware or mechanics. (`X`)
11. the later Gen 3 / Gen 4 SAS support page supplies exact launch chronology for every model listed on it. (`X`)
12. the loss of write compatibility necessarily means the data should immediately be migrated. (`X`)
13. a read-only bridge guarantees successful recovery of a damaged or degraded cartridge. (`X`)
14. a compatible drive guarantees encryption-key, LTFS, filesystem, application, or catalog availability. (`X`)
15. the compatibility-window pattern documented for LTO-1 through LTO-4 can be projected unchanged to LTO-8, LTO-9, or LTO-10. (`X`)
16. preserving a drive in storage guarantees that the drive will remain mechanically serviceable. (`X`)
17. current IBM support matrices alone reveal the design deliberations that produced the original LTO compatibility policy. (`X`)
18. a host-interface transition itself destroys the payload. (`X`)
19. unsupported and physically impossible are synonyms. (`X`)
20. the evidence proves one optimal archive migration ladder for all institutions. (`X`)

## Claim ledger additions

| ID | Claim | Label | Best source |
| --- | --- | --- | --- |
| G-130.14 | IBM's 3580 L23 was announced 9 Sep 2003 and documented LTO-2 read/write of original LTO-1 cartridges | `H/P` | S1 |
| G-130.15 | The 2003 3580 L23 documented Ultra160 LVD SCSI attachment, host/OS support constraints, open-system drivers, and SCSI topology limits | `H/P` | S1 |
| G-130.16 | IBM's 2005-era 3583 record documents LTO-3 read/write of LTO-2 and read access to LTO-1 | `H/P` | S3 |
| G-130.17 | The same IBM 3583 record documents LTO-3 LVD SCSI and 2 Gbps Fibre Channel attachment variants | `H/P` | S3 |
| G-130.18 | IBM's later Gen 3 / Gen 4 overview documents a SAS access path requiring supported HBAs / systems and separates media compatibility from host compatibility | `H/S` | S4 |
| G-130.19 | For LTO-1, the inspected IBM compatibility sequence is LTO-2 R/W -> LTO-3 read-only -> LTO-4 unsupported | `H/P`,`H/S` | S1/S3/S5 |
| G-130.20 | last writable bridge and last readable bridge are distinct retention boundaries | `E` | S1/S3/S5 |
| G-130.21 | preserved media + preserved compatible drive does not by itself prove a documented end-to-end host/software path | `E` | S1/S3/S4 |
| G-130.22 | unsupported by the vendor matrix means physically impossible | `X` | boundary |
| G-130.23 | all later LTO generations follow the exact LTO-1-to-LTO-4 bridge sequence | `X` | S5 + grounding packet |

## Prior-art / terminology boundary

This packet deepens **period evidence**, not invention priority.

The terms `read/write compatibility`, `read compatibility`, `host interface`, `device driver`, and specific SCSI / Fibre Channel / SAS names are source-level technical vocabulary.

The terms:

- `bridge generation`;
- `last writable bridge`;
- `last readable bridge`;
- `apparatus-to-host boundary`;
- `staged authority horizon`;

are project engineering language introduced to compare retention relations. They must not be attributed to IBM or the LTO Program.

Magnetic-tape format migrations and hardware-reader dependencies predate LTO by decades. The repository still makes no claim that LTO originated these problems. Earlier IBM 7-track / 9-track, reel-to-reel, cartridge, and removable-media transitions remain a `computing-archaeology` task requiring direct primary-manual inspection before a detailed genealogy is written here.

## Related-repository routing

Fresh GitHub search found no dedicated LTO packet in `tmzncty/computing-archaeology`.

Keep in this repository:

```text
media generation
  -> read/write authority window
  -> reader availability
  -> host attachment availability
  -> software path availability
  -> practical recoverability
```

Route to `computing-archaeology` if developed:

- full IBM 3580 / 3583 product genealogy;
- SCSI LVD -> Fibre Channel -> SAS tape attachment history;
- HBA, cabling, enclosure and transport evolution;
- pre-LTO magnetic-tape format transitions;
- industry-standardization and vendor-competition history.

## Remaining evidence debt

After this slice, the narrow debts are:

- exact contemporaneous launch / specification records for LTO-4 through LTO-10 rather than relying on current continuity matrices;
- direct primary design evidence for why each generation changed its compatibility window;
- direct LTO-10 head / servo / format engineering evidence beyond the current LTO Program roadmap explanation;
- a named migration case showing data actually moved before the last compatible reader class disappeared;
- drive aging / maintenance / spare-parts evidence for keeping legacy readers serviceable;
- controlled recovery experiments using retained old drives and modern adapter paths;
- encryption-key, LTFS, catalog and application-layer dependencies above the hardware path;
- pre-LTO tape-reader prior art in `computing-archaeology`.

The previously broad debts **"direct primary chronology for earlier generations"** and **"host-interface / driver dependency above a preserved drive"** are therefore partially closed and reframed, not declared exhausted.
