# Case 89 grounding — ATA logical CHS translation and LBA invariance, 1994–1997

## Status

**`grounded`** for the bounded claim that mid-1990s ATA specifications separate mutable logical-CHS translation from an invariant LBA designation, and that a period commercial EIDE manual explicitly denies a necessary relationship between logical sector address and actual physical media location.

This record does **not** establish the invention priority of LBA, the complete CHS→LBA chronology, BIOS translation history, actual platter geometry, or a direct genealogy to later FTLs.

---

## Research question

What evidence is sufficient to say that, in the bounded ATA regime:

1. host-visible `cylinder/head/sector` can be a **logical translation** rather than literal physical location;
2. CHS translation parameters can change;
3. a logical sector can nevertheless keep the same LBA;
4. current CHS reachability and total LBA reachability can differ;
5. the resulting stable designation must not be confused with data relocation, defect remapping, payload survival, or secure erasure?

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
- recent Case 87–88 commits.

Case 14 explicitly leaves `broad CHS→LBA chronology, earlier standards lineage, ATA/IDE translation` as separate work. The technical spine likewise keeps `HDD tracks / heads / cylinders / sectors` and `CHS → LBA` open under `Geometry hidden behind logical addresses`.

A repository search of `tmzncty/computing-archaeology` for `ATA`, `CHS LBA ATA IDE`, and related terms returned no existing case/doc match in the connector search. Therefore this slice records only the retention-specific address-identity relation here; it does not attempt to replace the still-needed general technical history there.

---

## Source set

### P1 — ATA-2 working draft

**X3T10/0948D Revision 4c, _AT Attachment Interface with Extensions (ATA-2)_**, surviving mirror:

<https://arxv.wirehaze.ovh/ATA-2_X3T10_0948D_R4C.PDF>

Relevant indexed text in the surviving draft:

- default and alternative logical CHS translation modes;
- `INITIALIZE DEVICE PARAMETERS` sets sectors per logical track and heads per logical cylinder;
- a device may support LBA;
- the host can select current CHS translation or LBA on a command-by-command basis;
- logical sectors are linearly mapped in LBA mode;
- the LBA of a given logical sector does not change with the current logical CHS translation;
- conversion formula uses the **current translation mode** values.

### P2 — ATA-3 working draft / published-text transcription

**X3T13/2008D Revision 7b, _AT Attachment-3 Interface (ATA-3)_**, searchable transcription:

<https://paperzz.com/doc/7545036/at-attachment-3-interface--ata-3--working-draft>

Relevant sections / fields:

- `IDENTIFY DEVICE` words 54–56: current logical cylinders, heads, sectors per logical track;
- words 57–58: current capacity in sectors;
- words 60–61: total number of user-addressable sectors in LBA translation;
- text states the LBA-capacity value does not depend on current device geometry;
- Annex B describes current values after `INITIALIZE DEVICE PARAMETERS`;
- Annex B names `orphan sectors` between the end of CHS-addressable range and end of LBA-addressable range.

The transcription also contains an ANSI publication statement and the draft identifiers. It is used as a searchable witness to period standards text, not as proof that this web host is the standards authority.

### P3 — SyQuest commercial implementation witness

**SyQuest, _SparQ Internal EIDE Technical Reference_, 113277-001A, 1997**, Bitsavers scan:

<https://www.bitsavers.org/pdf/syquest/sparq/113277-001A_Syquest_SparQ_Internal_EIDE_Technical_Reference_1997.pdf>

Relevant pp. 5-10 to 5-12:

- all register-delivered data-sector addressing uses a **logical sector address**;
- there is **no implied relationship** between logical sector addresses and actual physical media location;
- both CHS and LBA addressing are supported;
- a logical sector's LBA does not change when the logical CHS translation changes.

Relevant IDENTIFY discussion around p. 6-20:

- words 54–56 describe current logical geometry;
- words 57–58 current CHS capacity;
- words 60–61 total LBA-addressable sectors;
- the LBA total does not depend on current SparQ geometry.

### I1 — T13 institutional context

Technical Committee T13 — AT Attachment:

<https://www.t13.org/>

T13 describes itself as the INCITS technical committee responsible for AT Attachment storage-interface standards. This source is used only for standards-body context, not for the 1994–1997 mechanism claims above.

### R1 — existing repository prior-art boundary

[`../cases/14-scsi-disk-defect-reassignment-logical-identity.md`](../cases/14-scsi-disk-defect-reassignment-logical-identity.md)

Case 14 uses a 1990-filed disk-controller patent that already distinguishes host LBA from physical target address. That is sufficient inside this repository to block an ATA-2-first or SyQuest-first invention claim.

---

## Claim ledger

| ID | Claim | Evidence | Label | Strength / limit |
| --- | --- | --- | --- | --- |
| 89-H1 | ATA-2 permits a host to select logical CHS translation parameters with `INITIALIZE DEVICE PARAMETERS`. | P1 | H/P | strong for bounded draft semantics |
| 89-H2 | The parameters include sectors per logical track and heads per logical cylinder; device computes logical cylinders. | P1 | H/P | strong |
| 89-H3 | LBA-capable ATA-2 devices can select CHS or LBA per command. | P1 | H/P | strong for supporting devices |
| 89-H4 | ATA-2 explicitly states a logical sector's LBA does not change with current CHS translation. | P1 | H/P | central strong claim |
| 89-H5 | The LBA↔CHS formula depends on current translation values. | P1 | H/P | strong; formula is logical translation, not physical map |
| 89-H6 | ATA-3 exposes current CHS geometry in words 54–56 and current CHS capacity in 57–58. | P2 | H/P | strong |
| 89-H7 | ATA-3 separately exposes total LBA-addressable sectors in 60–61 and says this does not depend on current geometry. | P2 | H/P | central strong claim |
| 89-H8 | ATA-3 Annex B identifies sectors outside current CHS reach but inside LBA reach as `orphan sectors`. | P2 | H/P | strong, informative annex |
| 89-H9 | SyQuest says logical sector address does not imply actual physical media location. | P3 | H/P | strongest product-specific physical/logical boundary |
| 89-H10 | SyQuest repeats LBA invariance across logical CHS translations. | P3 | H/P | independent commercial witness |
| 89-E1 | Changing CHS translation can change the CHS tuple representing a logical sector while preserving its LBA. | P1/P2/P3 | E | direct reconstruction from sourced rule |
| 89-E2 | CHS-coordinate continuity and LBA-designation continuity are distinct. | P1/P3 | E | strong |
| 89-E3 | Logical CHS and actual physical CHS/location are not interchangeable categories. | P3 | E | directly bounded by manufacturer wording |
| 89-E4 | Current CHS reachability is not equivalent to logical-sector existence in the LBA set. | P2 | E | strongly supported by `orphan sectors` |
| 89-E5 | Translation-state change does not by itself establish data relocation. | P1/P3 | E/X | supported as a negative boundary; no relocation claim in command semantics |
| 89-E6 | Stable LBA does not establish stable physical embodiment. | R1 + P3 | E | cross-case synthesis; Case 14 supplies actual remap counterexample |
| 89-A1 | ATA logical translation and mapped Flash both separate upper-level designation from lower-level placement detail. | Case 04 + P3 | A | functional analogy only |
| 89-A2 | ATA translation and virtual paging both stabilize a logical designation above a mutable resolution layer. | Case 22 + P1/P2 | A | functional analogy only |
| 89-I1 | Retained identity can be constituted by a stable relation rather than one coordinate/place. | E1–E6 | I | philosophical interpretation, not period vocabulary |

---

## Exact boundaries established

### 1. `logical CHS coordinate ≠ physical media coordinate`

This is not merely inferred from modern disk architecture. The SyQuest manual directly says that logical sector address has no implied relationship to the actual physical location of the sector on the media.

### 2. `current CHS translation ≠ LBA identity`

ATA-2/ATA-3 separate the current translation parameters from LBA numbering and explicitly preserve the latter across translation changes.

### 3. `current CHS capacity ≠ total LBA capacity`

ATA-3 and the SparQ manual report these as distinct IDENTIFY quantities.

### 4. `unreachable through current CHS ≠ absent`

ATA-3's `orphan sectors` provide direct terminology for sectors which can lie beyond current CHS reach while remaining part of the LBA range.

### 5. `translation change ≠ defect reassignment`

A CHS translation change changes address presentation. Case 14's grown-defect path changes which physical sector serves an LBA. The two mechanisms must remain separate.

### 6. `stable LBA ≠ guaranteed payload survival`

Neither the ATA translation rule nor a stable address protects against media corruption. Case 14 even shows that a reassignment command can preserve an LBA while failing to preserve the affected old payload unless it is separately recovered.

---

## Prior-art / genealogy controls

### Do not claim ATA invented LBA

Case 14 already contains a 1990-filed disk-controller witness with host LBA and physical-target terminology. The broader SCSI and controller genealogy predates or runs in parallel with this bounded ATA standards slice.

### Do not claim ATA invented logical/physical indirection

That would be far broader than the evidence. The case only says the mid-1990s ATA standardization makes a particular CHS/LBA relation explicit.

### Do not write a clean `CHS → LBA` replacement story

The bounded sources show coexistence:

- ATA supports logical CHS translation;
- LBA can coexist and be selected per command;
- current CHS and LBA capacities are separately visible;
- a commercial 1997 product supports both.

The historical transition is therefore not evidenced here as one instantaneous replacement event.

### Do not infer physical geometry from logical CHS vocabulary

The product witness explicitly blocks this.

### Route the larger history elsewhere

The full history of:

- ST-506 / IDE / ATA interface evolution;
- BIOS geometry translation;
- zoned recording / zone-bit recording;
- real head/cylinder/sector organization;
- capacity barriers;
- LBA28 → LBA48;
- controller firmware geometry;
- SCSI/ATA comparative genealogy;

belongs primarily in `tmzncty/computing-archaeology`.

---

## Cross-case comparison matrix

| Relation | Case 89 ATA translation | Case 14 disk defect reassignment | Case 04 mapped Flash |
| --- | --- | --- | --- |
| Stable upper designation | LBA | LBA | virtual/logical block |
| What can change underneath | logical CHS representation | physical serving sector | physical Flash block/page relation |
| Is physical relocation established? | **No** for translation change itself | **Yes** in reassignment path | **Yes** in bounded copy/reclaim mapping path |
| Control state | current CHS translation + addressing mode | defect/replacement metadata | virtual map / allocation status |
| Primary trigger | host-selected address presentation | grown media defect / repair | erase/rewrite/reclamation constraints |
| Old payload erasure established? | No | No | old block can remain until later erase |
| Historical identity | ATA/IDE standards regime | disk defect management/SCSI | Flash virtual mapping |

The comparison should be used to keep **representation change**, **physical relocation**, and **logical identity** as separate axes.

---

## Rejected / unsupported claims

- `ATA-2 invented LBA` — **unsupported / rejected**.
- `CHS in ATA names literal platter cylinder/head/sector` — **rejected for the bounded SparQ witness**.
- `changing INITIALIZE DEVICE PARAMETERS moves all affected user data` — **unsupported**.
- `same LBA proves same physical sector` — **rejected by Case 14 and SyQuest's physical/logical boundary**.
- `LBA is an FTL` — **rejected**.
- `LBA hides every physical property relevant to reliability` — **unsupported**.
- `an orphan sector is deleted data` — **rejected**; it is an addressing-reachability term in the annex.
- `CHS inaccessibility is secure erase` — **rejected**.
- `1997 SyQuest behavior is universal for every ATA drive` — **unsupported**.
- `logical-sector identity is philosophically identical to personal/cultural identity` — **rejected as category collapse**.

---

## Evidence limits

1. The ATA-2 source used here is a surviving standards-draft mirror, not an official ANSI sales copy.
2. ATA-3 is inspected through a searchable transcription/mirror; exact archival facsimile control can be deepened later if needed.
3. SyQuest is one named commercial implementation witness; it does not define all ATA internals.
4. No physical platter geometry, zoning, defect table, or servo implementation is reconstructed.
5. No BIOS translation code is inspected in this case.
6. No benchmark or experiment demonstrates what a particular operating system did when changing translation parameters.
7. No first-invention claim is made.
8. HPA/SET MAX, DCO, 48-bit LBA, SATA-era semantics, and modern 4Kn/512e geometry remain separate slices.

---

## Grounded synthesis

The bounded evidence establishes a three-layer separation:

```text
stable logical sector / LBA
        ≠
current logical CHS representation
        ≠
actual physical media location
```

ATA-2/ATA-3 explicitly preserve the first while allowing the second to change, and the 1997 SyQuest manual explicitly denies that the second necessarily describes the third.

That makes Case 89 a useful retention case even though it is not about improving magnetic remanence. It shows that **remaining the same technical object can require retention of a designation relation across changes in the coordinate scheme through which the object is presented**.

The philosophical interpretation comes later. The historical record first says something much more exact: **the same logical sector need not have the same CHS tuple, and a logical CHS tuple need not be its physical place.**