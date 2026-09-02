# Case 14 grounding record — disk LBA / defect reassignment, 1990–1997

## Promotion decision

**Case:** [`cases/14-scsi-disk-defect-reassignment-logical-identity.md`](../cases/14-scsi-disk-defect-reassignment-logical-identity.md)  
**Decision:** `grounded`

The bounded case is grounded because the central retention claim no longer depends on a textbook analogy or a single later retrospective. It is supported by:

1. a directly inspected 1990-filed primary patent that explicitly separates host `logical block address` from `physical target address` and documents defect-list-mediated replacement;
2. a 1997 Seagate manufacturer interface manual whose `REASSIGN BLOCKS` semantics explicitly change the physical medium serving an LBA while retaining the same logical designation;
3. a critical negative boundary in that same manual: reassignment **does not preserve the affected block's payload by itself**;
4. a 1994 named-product Seagate manual that independently exposes automatic reallocation, grown/primary defect-list failures, spare exhaustion, and defect-list update failure;
5. explicit rejection of invention-priority, universal-implementation, FTL-equivalence, and whole-CHS→LBA-history claims.

---

## Bounded question

> What technical relation is retained when a host-visible disk logical block remains addressable under the same LBA after a media defect causes the controller to substitute another physical sector?

The answer supported by the source set is deliberately narrower than “disk data survives remapping”:

> **The logical designation / address relation can survive physical replacement. Payload survival is a separate recovery obligation and may fail.**

This distinction is the principal reason the case belongs in `technical-retention` rather than as another generic disk-history entry.

---

## Source 1 — Chan / NeXT, US5271018A

### Bibliography

Litko Chan, **“Method and apparatus for media defect management and media addressing,”** US5271018A.

- priority / filing: 27 April 1990;
- publication / grant: 14 December 1993;
- original assignee: NeXT, Inc.

Primary text: <https://patents.google.com/patent/US5271018A>

### Directly established historical record

The background states that:

- each sector is identified by both a `logical block address` and `physical target address`;
- the host uses the LBA for reads and writes;
- the physical target identifies the actual disk-surface location, typically by track and sector;
- a controller translator converts host LBA to physical target and vice versa;
- a `primary defect list` supports manufacturer-defect sector slipping;
- a `secondary defect list` records grown defects and their replacement sectors;
- changing subsequent LBAs after user data are present would produce lost data or misreads, so a grown defective LBA is instead assigned to a spare physical sector;
- a normal operation can translate LBA → physical target → PDL adjustment → SDL replacement → current physical target;
- PDL and SDL data are stored on the disk and loaded into controller RAM at power-up.

### Exact source regions

- background / definitions surrounding FIGS. 1A–1C: LBA versus physical target, sector slipping, spare consumption;
- `LINEAR DISPLACEMENT`: grown-defect replacement and the reason later LBAs cannot simply be renumbered;
- FIG. 2 flow discussion: LBA translation, PDL search, SDL replacement lookup;
- `STORAGE OF PDL AND SDL`: media-resident defect lists loaded into controller RAM.

### Boundary

The patent labels sector slipping and linear displacement as **prior art** while proposing its own zone/partition/spare-list improvements. Therefore it is evidence that those logical/physical separation mechanisms were already part of the engineering problem by the 1990 filing date, **not** evidence that Chan or NeXT invented LBA or defect remapping.

---

## Source 2 — Seagate SCSI-2/SCSI-3 interface manual, Rev. H

### Bibliography

Seagate Technology, **_Disc Drive SCSI-2/SCSI-3 Interface Product Manual (Vol. 2; Ver. 2), Rev. H_**, Publication 77738479, August 1997.

Primary PDF: <https://bitsavers.trailing-edge.com/pdf/seagate/scsi/77738479H_SCSI-2_SCSI-3_Interface_Product_Manual_Volume_2_Version_2.pdf_199708.pdf>

### Directly established historical record

Section 5.2.1.3, `Reassign Blocks Command (07h)`, manual pp. 137–138, establishes all of the following in manufacturer interface language:

- the initiator supplies a list of defective logical block addresses;
- the target reassigns them to an area reserved for that purpose;
- the drive changes the **physical medium used for each logical block address**;
- the affected blocks' data is **not preserved** by the command;
- the initiator is advised to recover data before reassignment;
- recovered data can then be written to the **same Logical Block Addresses**;
- a previously reassigned LBA can be reassigned again;
- over medium life, one logical block can therefore be associated with multiple physical addresses;
- this continues only until spare locations are exhausted;
- insufficient spare capacity produces `NO DEFECT SPARE LOCATION AVAILABLE` and identifies the first LBA not reassigned when available.

The same manual immediately preceding `REASSIGN BLOCKS` documents physical defect descriptors containing cylinder, head, and physical sector fields. This is useful evidence that a logical-block interface and physical geometry can coexist rather than one simply replacing the other everywhere inside the drive.

### Inspection boundary

The PDF was directly inspected through page-preserving extracted text. Screenshot rendering of the relevant pages on the large Bitsavers mirror timed out during this pass. Therefore:

- command semantics and page references are used;
- no layout, diagram, typography, or visual-figure claim is made from an unrendered page.

This is an archival-cleanup issue, not a mechanism blocker.

---

## Source 3 — Seagate ST43401N/ND / ST43402ND product manual

### Bibliography

Seagate Technology, **_ST43401N/ND and ST43402ND Reference Manual, Rev. C_**, Publication 83327730, December 1994.

Primary PDF: <https://www.seagate.com/support/disc/manuals/scsi/27730c.pdf>

### Directly established product-level boundary

The manual is explicitly for the named ST43401N/ND and ST43402ND Elite SCSI drives. Its additional-sense-code tables include:

- `Write error recovered with auto reallocation`;
- `Write error—auto reallocation failed`;
- `Recovered data ... data auto-reallocated`;
- `Defect list error`;
- `Defect list error in primary list`;
- `Defect list error in grown list`;
- missing primary / grown defect list;
- `No defect spare location available`;
- `Defect list update failure`.

The relevant manual pages were directly text-inspected and visually rendered in this pass.

### Why this source matters

The 1997 generic interface manual is already enough to ground the command semantics. The 1994 product manual adds a useful independent check that defect-list state, automatic reallocation, and spare exhaustion were concrete named-drive failure/service conditions rather than only abstract command-language possibilities.

---

## Discovery-only / unresolved sources

### HP 97540 SCSI-2 Technical Reference Manual

A 1989/1990 HP 97540 manual was found in archival search with indexed `REASSIGN BLOCKS` material. Direct PDF retrieval was unreliable during this pass, so it is **not** used for a central claim.

### SCSI-2 standard

A public scan of the 1994 SCSI-2 standard was located, but direct retrieval/rendering was unreliable in this pass. The case therefore does not claim standard-level invention priority or exact first-standard wording from an uninspected scan.

These sources remain optional archival deepening because the manufacturer-primary source chain is already sufficient for the bounded mechanism claim.

---

## Claim-by-claim grounding

| Claim | Label | Primary support | Status |
| --- | --- | --- | --- |
| period disk-controller discourse distinguishes host LBA from physical target | H/P | US5271018A | grounded |
| manufacturer defects can be hidden by sector slipping while preserving a contiguous LBA space | H/P | US5271018A | grounded for bounded account |
| grown defects can redirect an existing LBA to a spare physical target | H/P | US5271018A + Seagate 1997 | grounded |
| renumbering already-used later LBAs is rejected because it would cause lost data/misreads | H/P | US5271018A | grounded |
| defect/replacement metadata participates in later address resolution | H/P + E | US5271018A | grounded |
| defect metadata can itself require persistence across power cycles | H/P + E | US5271018A PDL/SDL disk→RAM startup path | grounded for bounded account |
| `REASSIGN BLOCKS` changes physical medium serving the same LBA | H/P | Seagate 1997 §5.2.1.3 | grounded |
| reassignment does not itself preserve the selected block's old payload | H/P | Seagate 1997 §5.2.1.3 | grounded |
| the initiator may recover before remap and rewrite recovered data to the same LBA | H/P | Seagate 1997 §5.2.1.3 | grounded |
| one LBA can traverse multiple physical addresses during medium life | H/P | Seagate 1997 §5.2.1.3 | grounded |
| spare exhaustion is an explicit repair failure | H/P | Seagate 1997 + Seagate 1994 | grounded |
| defect-list loss/update failure is an explicit failure class | H/P | Seagate 1994 | grounded |
| LBA interface implies physical geometry ceased to matter internally | X | contradicted by source set | rejected |
| HDD remapping is historically an FTL | X | no historical evidence; mechanisms differ | rejected |
| logical-address continuity guarantees data continuity | X | directly contradicted by Seagate | rejected |
| NeXT invented LBA / defect remapping | X | Chan text itself labels bounded schemes prior art | rejected |

---

## Engineering reconstruction added by this case

### 1. `logical-block identity ≠ physical-sector identity`

A stable logical designation can resolve to different physical sectors over time.

### 2. `reassignment continuity ≠ payload continuity`

This is the strongest counterexample supplied by the case. The address slot can survive reassignment even when the old value does not.

### 3. `defect metadata is retention state`

To provide the same logical-block service after a defect, the controller must preserve or reconstruct which sectors are bad and where replacements live.

### 4. `spare capacity is latent repair capability`

Finite reserved space is part of the system's ability to continue a logical service after future defects. Exhaustion converts a hidden capacity reserve into an explicit retention failure.

### 5. `LBA abstraction ≠ disappearance of geometry`

Physical defect geometry can remain operational below a host-visible logical address interface.

These are project reconstructions. They should not be presented as period terminology.

---

## Cross-case comparison boundary

### Case 04 — mapped Flash

Both mechanisms can preserve a logical designation while changing physical location.

But:

- the HDD case is bounded around **defect/failure-triggered substitution into spares**;
- Case 04 is bounded around **normal rewrite under erase-before-write**, out-of-place update, map change, and later copy/reclamation.

Therefore:

> **logical/physical indirection is a useful cross-case invariant; “FTL” is not a historically neutral name for every indirection mechanism.**

### Case 05 — RADOS

Both can survive replacement of a physical embodiment, but RADOS adds replicas, protocol authority/currentness, epochs/maps, peering, and distributed repair. The disk case has neither that replication model nor the same authority problem.

---

## Related-repository routing check

Before writing, `tmzncty/computing-archaeology` code search was run for combinations including:

- `bad sector LBA CHS disk defect remap`;
- `disk sector defect remapping Winchester`;
- `SCSI disk`.

No directly overlapping dedicated case was returned. This is a practical duplication check, **not** evidence that the companion repository contains no disk history.

The broad history of HDD geometry, zone recording, CHS/LBA interfaces, standards evolution, and controller architecture should still be developed primarily in `computing-archaeology` if pursued. `technical-retention` keeps the narrower logical-identity / repair comparison.

---

## Why `grounded` rather than `first-pass`

The central claims now satisfy the repository's `grounded` criteria:

- **strong primary evidence:** patent + manufacturer manuals;
- **precise source locations:** patent mechanism sections and Seagate §5.2.1.3 / product sense-code pages;
- **historical vocabulary:** LBA, physical target, PDL/SDL, grown defect, sector slipping, linear displacement, Reassign Blocks, automatic reallocation;
- **mechanism:** host designation → translation/defect metadata → current physical target;
- **failure modes:** unreadable payload, spare exhaustion, defect-list absence/corruption/update failure, failed auto reallocation;
- **counterexamples / limits:** reassignment without data preservation; LBA without disappearance of geometry;
- **related-repository duplication checked:** no direct dedicated overlap found through code search.

The unresolved direct rendering of one large Seagate PDF and the broader CHS→LBA chronology are archival / adjacent-history tasks, not blockers for the bounded defect-reassignment claim.