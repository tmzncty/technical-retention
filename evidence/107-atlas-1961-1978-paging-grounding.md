# Atlas 1961–1978 one-level-store paging grounding record

This record grounds [`../cases/107-atlas-one-level-store-paging-residency.md`](../cases/107-atlas-one-level-store-paging-residency.md).

The bounded question is not `who invented virtual memory?` It is:

> How does the Atlas record separate program-visible block designation, current core-page residency, backing-copy currentness, drum-location metadata, replacement/page-out work, and recovery after a nonresident access?

## Source A — Kilburn et al. 1962, primary one-level-store paper

T. Kilburn, D. B. G. Edwards, M. J. Lanigan, and F. H. Sumner, **“One-level storage system,”** *IRE Transactions on Electronic Computers* EC-11(2), April 1962, pp. 223–235.

Page-preserving public copy:
<https://tcm.computerhistory.org/ComputerTimeline/Chap23_atlas_CS1_10CS2.pdf>

The PDF text was inspected directly. The page images corresponding to reprint printed pp. **279–280** were also visually inspected in this research pass. Those two pages contain the main mechanism claims below.

### A1. Apparent one-level storage — primary paper introduction / §3

The paper says Atlas combines core and drum economically and automates transfers so that the programmer sees an apparent one-level store. The central store is divided into 512-word blocks, and 512-word core positions are called pages for identification.

**Grounded boundary:** one-level appearance is produced by automatic transfer/address machinery; it is not evidence that core and drum are physically one medium.

### A2. P.A.R. equivalence — printed p. 279

Each core page position has a Page Address Register containing the block address presently occupying that page. The demanded block address is compared against all P.A.R.s. `Equivalence` admits access to the matching page; `not equivalence` stores the demanded address, raises an interrupt, and invokes a fixed-store routine to organize drum/core transfer.

**Grounded boundaries:** `block designation ≠ core-page position`; `not equivalence ≠ payload loss`; P.A.R. state is retained resolution/control state distinct from payload.

### A3. Drum directory and relocatable external position — printed p. 279

For a write transfer, Atlas places a block in the first available empty block position on any drum. The paper therefore requires transfers to be carried out by reference to a directory in subsidiary store and says the directory is updated whenever a transfer occurs. On a read, the routine resolves the absolute drum position of the requested block and transfers it to an empty core page.

**Grounded boundaries:** `virtual block designation ≠ fixed drum position`; `drum-location directory ≠ payload`; physical presence without the required location relation is not the same as resolved availability.

### A4. Read-in and outgoing write are separate parts of page turning — printed pp. 279–280

After ordering the requested read from drum, the routine chooses a core-resident block to transfer back to drum so that a core page will be empty for a future read. The paper describes one read and one write to the drum as two necessary, sequential transfers that can occur in either order. Maintaining a vacant page allows the read to occur first while the learning program selects the outgoing page.

The replacement-selection aid includes `use` digits associated with core page positions.

**Grounded boundaries:** `current fault recovery ≠ free-page reserve restored`; `incoming transfer ≠ outgoing transfer`; replacement-policy state ≠ payload.

### A5. Lock-out and service admission — printed p. 280

A lock-out digit is associated with each P.A.R. During a transfer ordinary program access to that page can be blocked. After block transfer completes, the organizing program clears lock-out and central-machine access becomes available.

**Grounded boundary:** `core-page residency ≠ ordinary-program access admission`.

### A6. What Source A does not establish

Source A does not establish:

- modern `dirty bit`, `swap cache`, or anonymous-page semantics;
- a filesystem/database durability API;
- power-fail atomicity or crash consistency;
- a universal backing-copy policy for later virtual-memory systems;
- invention priority merely from its April 1962 publication date.

## Source B — Fotheringham 1961 publication floor

John Fotheringham, **“Dynamic Storage Allocation in the Atlas Computer, Including an Automatic Use of a Backing Store,”** *Communications of the ACM* 4(10), October 1961, pp. 435–436, DOI 10.1145/366786.366800.

This pass uses the bibliographic/publication record only to establish an earlier Atlas publication floor. The original full text was not needed for the mechanism claims above and is therefore not silently paraphrased here.

**Grounded boundary:** April 1962 paper publication ≠ first public Atlas discussion ≠ invention date.

## Source C — Lavington 1978 historical retrospective

S. H. Lavington, **“The Manchester Mark I and Atlas: A Historical Perspective,”** *Communications of the ACM* 21(1), January 1978.

Public PDF used here:
<https://pages.cs.wisc.edu/~remzi/Classes/537/LectureNotes/Papers/atlas.pdf>

Printed p. 5 describes the 512-word Atlas paging system and the learning replacement program, then states that **no copy was normally kept on drum**, contrasting Atlas with later paging machines that could keep a drum copy and avoid writing back an unaltered page.

This is retrospective scholarship, not a contemporary 1962 interface specification. It is used because it directly addresses the historical copy-currentness relation that the project needs to avoid projecting later assumptions backward.

**Grounded boundaries:** `core residency ≠ guaranteed simultaneous drum copy`; `Atlas copy policy ≠ universal later paging policy`.

## Source D — IEEE institutional patent/history navigation

IEEE Engineering and Technology History Wiki, **“Atlas Computer and the Invention of Virtual Memory, 1957–1962.”**
<https://ethw.org/Milestones%3AAtlas_Computer_and_the_Invention_of_Virtual_Memory%2C_1957-1962>

The institutional retrospective lists Manchester/NRDC paging-related UK patent applications filed in March and April 1960 and situates Fotheringham/Kilburn-era publications in the Atlas development chronology.

Use here: navigation and an earlier documentary floor showing why the 1962 paper cannot safely be equated with first conception.

Do not use here: sole proof of exclusive invention priority or exact mechanism details where Source A is available.

## Evidence ledger

| Claim | Label | Location | Strength |
| --- | --- | --- | --- |
| core and drum are presented to the programmer as an apparent one-level central store | H/P | Source A, introduction/§3 | strong contemporary primary text |
| 512-word core positions are pages and P.A.R.s retain the block currently occupying them | H/P | Source A, printed p. 279 | strong primary text + page-image inspection |
| `not equivalence` invokes interrupt/Supervisor transfer work | H/P | Source A, printed p. 279 | strong primary text + page-image inspection |
| outgoing blocks can go to first available empty drum positions and require an updated directory | H/P | Source A, printed p. 279 | strong primary text + page-image inspection |
| requested read and outgoing write are distinct transfers; vacant page permits read-first scheduling | H/P | Source A, printed pp. 279–280 | strong primary text + page-image inspection |
| lock-out can block ordinary program access to a core page during transfer | H/P | Source A, printed p. 280 | strong primary text + page-image inspection |
| Atlas normally kept no simultaneous drum copy of a page in main core store | H/S | Source C, printed p. 5 | strong scholarly historical witness |
| 1961 publication and 1960 patent applications predate the 1962 paper | H/P + H/S | Source B metadata; Source D institutional chronology | strong chronology, not priority proof |
| page-out is a modern durability request | X | not established | rejected |
| every resident page has a current backing copy | X | contradicted for bounded Atlas regime by Source C |
| 1962 publication proves invention priority | X | not established | rejected |

## Historical cautions

- `page`, `P.A.R.`, `equivalence`, `directory`, `use`, and `lock out` are period vocabulary in Source A.
- `virtual designation`, `real-frame residency`, `backing-copy currentness`, `page-out obligation`, and `page-fault recovery` are present project vocabulary used to compare relations.
- A `not equivalence` interrupt is functionally page-fault-like, but this record does not claim the 1962 paper used the later phrase `page fault` in the same conceptual taxonomy.
- Lavington 1978 is valuable precisely because it distinguishes Atlas's normal no-copy-on-drum behavior from later paging machines; it should not be back-projected as 1962 authorial wording.
- Core/drum migration is not itself an application crash-durability contract.
- The patent/application chronology constrains novelty claims but does not settle every historical priority dispute.

## Related-repository duplication check

A current GitHub search of `tmzncty/computing-archaeology` for `Atlas`, paging, and `one-level store` did not expose a dedicated case to reuse. A broad Atlas/virtual-memory engineering genealogy should be developed there if needed. `technical-retention` keeps only the bounded relation among designation, residency, copy-currentness, location metadata, page-turn work, and recovery/admission.
