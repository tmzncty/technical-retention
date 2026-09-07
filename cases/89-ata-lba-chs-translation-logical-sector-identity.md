# ATA LBA / CHS Translation: Logical-Sector Identity Across Geometry Representation

## Status

**`grounded`** — bounded to ATA-2 / ATA-3 logical CHS translation and LBA semantics in the mid-1990s, with a 1997 SyQuest EIDE product manual as an implementation witness. The case establishes a narrow addressing-retention relation: a logical sector can retain one LBA while the CHS tuple used to present it changes, and neither logical CHS representation is thereby proven to be the sector's actual physical disk location.

Grounding record: [`../evidence/89-ata-1994-1997-lba-chs-translation-grounding.md`](../evidence/89-ata-1994-1997-lba-chs-translation-grounding.md).

## Scope

- **Bounded period:** 1994–1997.
- **Standards witnesses:** X3T10/0948D Revision 4c, *AT Attachment Interface with Extensions (ATA-2)*; X3T13/2008D Revision 7b, *AT Attachment-3 Interface (ATA-3)*.
- **Named-product witness:** SyQuest, *SparQ Internal EIDE Technical Reference*, 113277-001A, 1997.
- **Research question:** what exactly remains the same when a disk exposes a stable logical-block number while the host/controller may describe the same logical sector using different cylinder/head/sector translation parameters?

This case advances the open `HDD tracks / heads / cylinders / sectors; CHS → LBA` item without pretending to be a complete history of disk geometry.

The physical-layout counterpart is grounded separately in [Case 108](108-seagate-medalist-zone-bit-recording-geometry.md): Seagate's 1995 Medalist ZBR/notch contract shows that fixed-size logical blocks can span a medium whose outer and inner physical cylinders have different block capacities. That link is a layer decomposition, not a claim that CHS translation and ZBR are the same mechanism.

It is **not**:

- a general history of IDE/ATA;
- a chronology of BIOS 528 MB / 8.4 GB capacity barriers;
- a claim that ATA invented logical block addressing;
- a reconstruction of actual platter zoning, servo wedges, track skew, zone-bit recording, or drive firmware placement algorithms;
- a defect-remapping case — that is Case 14;
- a Flash Translation Layer analogy elevated into genealogy;
- a claim that changing logical CHS translation necessarily moves user data on the medium.

The bounded contribution is simpler:

> **logical sector identity can be stabilized at one addressing layer even while another host-visible geometry representation is re-parameterized.**

---

## Historical vocabulary

The period sources directly use:

- `CHS translation` / `CHS addressing`;
- `logical cylinder`, `logical head`, `logical sector`;
- `current translation mode`;
- `default translation`;
- `LBA addressing` / `Logical Block Addressing`;
- `logical sector address`;
- `INITIALIZE DEVICE PARAMETERS`;
- `IDENTIFY DEVICE`;
- `current capacity in sectors`;
- `total number of user addressable sectors`;
- `orphan sectors` in the ATA-3 informative annex.

The following are **project engineering terms**, not period ATA vocabulary:

- `designation continuity`;
- `geometry-representation continuity`;
- `address invariance`;
- `representation re-parameterization`;
- `address-retention relation`.

Likewise, `mapping layer` is used below only as an engineering description where necessary. It must not be read as a claim that ATA CHS translation was historically called an FTL or was technically identical to later Flash mapping.

---

## Historical record

### H/P — ATA-2 permits CHS translation parameters to change

The ATA-2 working draft describes a `default CHS translation mode`, and permits a host to select another logical translation by issuing `INITIALIZE DEVICE PARAMETERS`.

The host supplies:

- sectors per logical track;
- heads per logical cylinder.

The device then computes the available logical cylinders for that requested translation.

The important word is **logical**. The command changes how the host-visible CHS address space is parameterized; the source does not say that it mechanically reorganizes platter tracks or relocates every sector to new physical coordinates.

**Primary anchor:** X3T10/0948D Revision 4c, ATA-2, addressing section around §7.2 / printed p. 21 in the surviving draft.

### H/P — the same logical sector keeps the same LBA across CHS translations

The same ATA-2 text makes a much stronger invariant explicit. For devices supporting LBA, logical sectors are linearly mapped beginning with LBA 0 corresponding to logical CHS cylinder 0, head 0, sector 1. It then states that **irrespective of the logical CHS translation mode currently in effect, the LBA address of a given logical sector does not change**.

The draft supplies the familiar conversion relation:

```text
LBA = ((cylinder * heads_per_cylinder + head)
       * sectors_per_track) + sector - 1
```

where `heads_per_cylinder` and `sectors_per_track` are the **current translation-mode values**.

Thus one logical sector can acquire a different CHS tuple after translation parameters change while its LBA remains invariant.

This is direct period evidence for:

> **CHS-coordinate continuity ≠ LBA-designation continuity**.

### H/P — ATA can choose CHS or LBA on a command-by-command basis

ATA-2 says that a supporting device allows the host to select the currently selected CHS translation or LBA addressing on a command-by-command basis using the L bit in the Device/Head register.

The two forms are therefore not necessarily different data populations. They can be two ways of designating logical sectors on the same device interface.

This matters because a later observer must not infer:

```text
changed command address syntax
    -> changed payload
```

or:

```text
changed logical CHS tuple
    -> physical sector relocation
```

Neither implication is established by the addressing rule.

### H/P — ATA-3 separately records current CHS geometry and total LBA capacity

ATA-3's `IDENTIFY DEVICE` layout makes the distinction inspectable as device state.

Words 54–56 report:

- current logical cylinders;
- current logical heads;
- current logical sectors per track.

Words 57–58 report the **current capacity in sectors** for that CHS translation.

Words 60–61 separately report the **total number of user-addressable sectors in LBA translation**, and the draft states that this value **does not depend on the current device geometry**.

The interface therefore retains at least two different descriptions:

```text
current logical-CHS presentation
        ≠
total LBA-addressable sector set
```

**Primary anchor:** X3T13/2008D Revision 7b, ATA-3, `IDENTIFY DEVICE` words 54–61 and Annex B.

### H/P — the current CHS translation is mutable working configuration

ATA-3's annex describes the current heads/sectors values as those specified by the last `INITIALIZE DEVICE PARAMETERS` command, with reset/default behavior treated separately.

So the current CHS tuple-space is not itself the user payload, nor must its exact runtime parameterization be the invariant by which the payload's logical sector identity survives.

This adds a retention-specific distinction:

> **current address-presentation state ≠ retained user-sector identity**.

A controller can return to a default translation after reset while the LBA numbering relation remains the stable address convention for the logical sector set.

### H/P — ATA-3 names sectors that can exist in LBA space but fall outside current CHS reach

ATA-3's informative Annex B uses the term `orphan sectors` for sectors between the last sector addressable in CHS mode and the last sector addressable in LBA mode. It notes that a device may or may not allow access to those sectors through CHS addressing and that host-selected translation values can increase the orphan population.

This is a particularly useful negative result:

> **not addressable through the current CHS presentation ≠ absent from the device's LBA-addressable logical sector set**.

Addressability must be qualified by interface mode.

### H/P — a 1997 commercial EIDE drive explicitly denies a necessary relation between logical address and physical media location

SyQuest's 1997 *SparQ Internal EIDE Technical Reference* states that all addressing of recorded data sectors for register-delivered commands uses a **logical sector address**, and that there is **no implied relationship** between logical sector addresses and the actual physical location of the data sector on the medium.

The manual then supports both CHS and LBA modes and repeats the ATA rule that the LBA of a given logical sector does not change when the logical CHS translation changes.

This is the strongest boundary in the case:

> **logical CHS ≠ actual physical CHS**.

The word `cylinder` in a host-visible translated CHS tuple must not automatically be read as a literal platter cylinder.

**Primary anchor:** SyQuest, *SparQ Internal EIDE Technical Reference*, 113277-001A, 1997, pp. 5-10 to 5-12; IDENTIFY discussion around p. 6-20.

---

## Retained state

The bounded interface separates several state classes.

### 1. User payload

The data contents of each logical sector remain the object the host ultimately wants to read or write.

### 2. LBA designation

For an LBA-capable device, the logical-sector number is a stable linear designation independent of which logical CHS translation is currently active.

### 3. Current CHS translation parameters

Heads-per-logical-cylinder and sectors-per-logical-track are current interface/configuration state. They influence the CHS tuple used to designate a logical sector.

### 4. Default CHS translation parameters

Reset/default geometry and current geometry are distinct concepts in the standards chain.

### 5. Capacity descriptors

Current CHS capacity and total LBA-addressable sector count are separately reported. They need not denote the same reachable set under a particular CHS translation.

### 6. Hidden physical placement

Actual media position remains a lower-layer fact. The SyQuest witness explicitly refuses to identify it with the logical sector address.

---

## Retention mechanism

This is not a retention mechanism in the sense of refresh, magnetic remanence, or replication. The payload remains physically retained by the disk medium and its controller machinery.

The case instead concerns **retention of designation across changing representations**.

A simplified relation is:

```text
logical sector identity
        |
        +--> stable LBA number
        |
        +--> current CHS tuple
                depends on current translation parameters

actual media location
        -> separately hidden / not implied by logical address
```

Changing CHS translation can therefore change an address representation without changing the sector's stable LBA and without, from the evidence here, requiring a data relocation.

The apparently simple statement `sector N remains sector N` is thus maintained at the **logical designation layer**, not proved by one immutable geometric coordinate.

---

## Addressing and access geometry

### LBA path

An LBA-capable host can address the logical sector linearly.

```text
host LBA
    -> device logical-sector selection
    -> internal media resolution
```

The bounded standards do not expose the final physical-resolution algorithm.

### Logical CHS path

Under CHS translation:

```text
host cylinder/head/sector tuple
    + current heads-per-cylinder
    + current sectors-per-track
        -> corresponding logical sector / LBA relation
        -> internal media resolution
```

If the host changes the translation parameters, the tuple used for a logical sector can change.

### Physical geometry

The SyQuest witness blocks a common retrospective mistake: a logical CHS tuple is not evidence that the tuple names the literal cylinder/head/sector physically containing the data.

Therefore:

> **geometry-shaped syntax ≠ exposed physical geometry**.

---

## Read / write semantics

### Read

The host can request a sector through the active addressing mode. The case does not establish any destructive-read behavior; magnetic-media integrity and ECC/servo internals remain outside scope.

### Write

A write addresses a logical sector through CHS or LBA syntax. This case does not establish that writing one LBA is physically in-place, nor that the same physical surface sector serves that LBA for the device's whole life.

Case 14 separately establishes defect-triggered physical reassignment behind a stable LBA.

### Translation change

`INITIALIZE DEVICE PARAMETERS` changes logical CHS translation parameters. It is not evidenced here as a user-payload rewrite command.

Thus:

> **translation update ≠ payload update**.

---

## Time and maintenance

Several temporal relations remain distinct:

- user data may remain on nonvolatile magnetic media across power cycles;
- a current CHS translation can be runtime configuration and later return to a default after reset;
- LBA numbering provides a designation relation that does not depend on which current CHS translation is active;
- physical defect reassignment may later move the sector serving an LBA, but that is a separate exceptional maintenance path established in Case 14.

This means a stable logical sector identity can outlive one particular **presentation configuration** even when no historical log of every prior CHS translation is retained.

---

## Failure / forgetting modes

Keep separate:

- **payload media failure** — the magnetic representation becomes unreadable;
- **logical-address confusion** — software interprets CHS values using the wrong translation parameters;
- **capacity mismatch** — current CHS representation reaches fewer sectors than the LBA address space;
- **orphan-sector inaccessibility through CHS** — a sector remains in the LBA set but lacks a current CHS route;
- **loss of device/controller interpretation** — logical designation no longer resolves correctly to media;
- **defect reassignment failure** — Case 14's separate spare/remap path cannot sustain an LBA after media defect;
- **secure erasure/deletion** — not established by any change of address representation here.

Changing the address map through which something is reachable is not automatically equivalent to physically forgetting it.

---

## Engineering reconstruction

### E — a stable address can preserve identity across mutable address representations

The ATA sources explicitly preserve the LBA of a logical sector while CHS translation changes.

Therefore:

> **logical designation continuity does not require coordinate-string continuity**.

### E — logical geometry can be representational rather than topological

SyQuest explicitly says logical sector addresses have no implied relationship to actual physical position.

Therefore:

> **host-visible geometry-shaped coordinates need not be a literal map of the medium**.

This is an important historical correction to simplistic stories in which CHS always means that software directly addresses platter geometry and LBA then suddenly abolishes geometry.

### E — addressability is observer/interface-relative

ATA-3 `orphan sectors` show that one sector can belong to the device's LBA-addressable set while being outside a particular CHS translation's reachable range.

Therefore:

> **present through LBA ≠ present through every addressing regime**.

Physical presence, logical existence, and reachability through one interface mode are separate relations.

### E — current geometry metadata is retention infrastructure, not payload

The current heads/sectors/cylinders determine how CHS commands resolve. Losing or changing that interpretation can make the same tuple designate something else even when payload bytes remain intact.

Therefore:

> **address-interpretation state can be operationally constitutive without being user data**.

### E — LBA continuity alone does not prove physical-location continuity

Case 89 proves that LBA can stay invariant while the CHS *representation* changes. Case 14 separately proves that an LBA can stay invariant while the serving physical sector changes after defect reassignment.

Together they reject two different shortcuts:

```text
same LBA -> same CHS tuple        [false under translation change]
same LBA -> same physical sector  [false under defect reassignment]
```

But the mechanisms must not be collapsed. Translation change can be representational; defect reassignment is a repair event that changes physical embodiment.

---

## Functional comparisons

### A — Case 04 mapped Flash

Both cases show a stable logical designation above hidden physical detail.

The analogy stops there.

Case 04's Flash mapping participates in erase-constrained relocation, invalidation, transfer-unit copying, and reclamation. Case 89 does **not** establish those behaviors for ATA CHS/LBA translation.

So:

> **ATA logical translation ≈ mapped Flash only as a bounded designation/location analogy, not historical or mechanism identity.**

### A — Case 14 SCSI disk defect reassignment

This is the closest local comparison and also the most important distinction.

- Case 89: a logical sector's LBA stays fixed while its **CHS representation** can change.
- Case 14: a logical block's LBA stays fixed while its **physical sector embodiment** can change.

These are different axes of continuity.

### A — Case 22 virtual paging

A virtual page can remain designated while real-frame residency changes. This is useful only as a functional comparison about stable logical designation above mutable lower-layer resolution. ATA translation is not virtual memory and the historical lineages are separate.

---

## Philosophical interpretation

### I — retained identity can belong to a relation rather than a place

This case supplies a modest philosophical pressure test: the thing that remains available as `the same sector` need not be defined by one enduring coordinate at every layer.

The technical evidence supports only the engineering premise:

- one LBA remains invariant;
- logical CHS representation can change;
- actual physical location is not implied by that logical address.

A stronger claim about identity, abstraction, or technical memory is interpretive and must remain labeled as such.

### I — availability is not identical to physical presence

`Orphan sectors` make the point sharply: a sector may still belong to the LBA-addressable device while one CHS representation cannot reach it.

This can inform later analysis of technical availability, but it is **not** evidence that ATA engineers were formulating a Heideggerian problem of `Bestand`.

---

## Prior-art boundary

This case does **not** claim:

- that ATA-2 invented LBA;
- that ATA invented logical/physical address separation;
- that SyQuest invented translation;
- that CHS→LBA occurred at one clean historical moment;
- that one ATA standards draft establishes the complete BIOS/drive/controller genealogy.

Case 14 already contains an earlier 1990-filed disk-controller witness that distinguishes host LBA from physical target address. That alone blocks an ATA-2-first claim inside this repository.

The broader history — SCSI logical blocks, early IDE/ATA, BIOS translation, zone-bit recording, controller intelligence, ATA capacity barriers, and later LBA48 — belongs primarily in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). A repository search performed for this slice did not find an existing ATA/CHS/LBA treatment there, so this case records only the retention-specific bridge rather than attempting to fill that whole historical gap here.

---

## Counterexamples and limits

1. **No physical platter map is reconstructed.** The case is deliberately about logical addressing and translation.
2. **No claim that translation is the only internal mapping.** A drive may have defect, zoning, servo, caching, or firmware indirection not exposed by the host syntax.
3. **No claim that all CHS implementations behave identically.** The evidence is bounded to the stated ATA drafts and named product witness.
4. **No claim that LBA guarantees payload survival.** A stable designation can remain while the data itself becomes corrupt or unrecoverable.
5. **No claim that LBA is permanently immutable under all later ATA features.** HPA/SET MAX, LBA48, remapping, security, deallocation, and later standards require separate cases.
6. **No secure-erasure claim.** Making a sector unreachable through one presentation does not prove its physical contents are erased.
7. **No direct ATA→Flash genealogy.** The comparison to mapped Flash is functional only.

---

## Source links

### Primary / period technical sources

- X3T10/0948D Revision 4c, *AT Attachment Interface with Extensions (ATA-2)*, surviving draft mirror: <https://arxv.wirehaze.ovh/ATA-2_X3T10_0948D_R4C.PDF>
- X3T13/2008D Revision 7b, *AT Attachment-3 Interface (ATA-3)*, searchable surviving transcription: <https://paperzz.com/doc/7545036/at-attachment-3-interface--ata-3--working-draft>
- SyQuest, *SparQ Internal EIDE Technical Reference*, 113277-001A, 1997, Bitsavers scan: <https://www.bitsavers.org/pdf/syquest/sparq/113277-001A_Syquest_SparQ_Internal_EIDE_Technical_Reference_1997.pdf>

### Institutional provenance / standards context

- Technical Committee T13 — AT Attachment: <https://www.t13.org/>

### Repository comparisons

- [`14-scsi-disk-defect-reassignment-logical-identity.md`](14-scsi-disk-defect-reassignment-logical-identity.md)
- [`04-flash-virtual-mapping-logical-identity.md`](04-flash-virtual-mapping-logical-identity.md)
- [`22-ibm-system370-paging-currentness.md`](22-ibm-system370-paging-currentness.md)
- [`../docs/TECHNICAL_SPINE.md`](../docs/TECHNICAL_SPINE.md)
- [`../RELATED_REPOS.md`](../RELATED_REPOS.md)

---

## Bounded conclusion

The mid-1990s ATA evidence makes a useful retention distinction unusually explicit.

A logical sector can keep one stable LBA while:

- its logical CHS tuple changes with the current translation parameters;
- current CHS capacity differs from the total LBA-addressable sector set;
- some LBAs fall outside current CHS reach;
- and the logical address itself need not imply actual physical media location.

Therefore:

> **stable logical identity ≠ stable geometric representation ≠ stable physical location.**

Case 89 adds the middle term that Case 14 and mapped Flash leave easy to blur. A state can remain designated not only while its embodiment moves, but also while the coordinate system used to talk about it changes.