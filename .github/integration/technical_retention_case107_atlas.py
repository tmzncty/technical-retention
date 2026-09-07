from pathlib import Path

CASE = Path('cases/107-atlas-one-level-store-paging-residency.md')
EVID = Path('evidence/107-atlas-1961-1978-paging-grounding.md')
ROAD = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')

if CASE.exists() or EVID.exists():
    raise SystemExit('Case 107 already exists')

case = r'''# Atlas One-Level Store: Virtual Designation, Core Residency, Drum Location, and Page-Turn Obligation

## Status

**`grounded`** — bounded to the Manchester Atlas one-level-store mechanism documented in 1961–1962, with a 1978 scholarly historical witness for the important no-current-drum-copy regime. This case establishes a retention-specific paging decomposition; it does **not** claim a complete virtual-memory genealogy, universal modern paging semantics, crash durability, or invention priority.

Grounding record: [`../evidence/107-atlas-1961-1978-paging-grounding.md`](../evidence/107-atlas-1961-1978-paging-grounding.md).

## Scope

The open roadmap question is deliberately narrower than a history of virtual memory:

> In a paged one-level store, how should **virtual designation**, **real-frame residency**, **backing-copy currentness**, **external-location state**, **page-out obligation**, and **fault recovery** be separated?

Atlas is unusually useful because the 1962 primary paper exposes all of these relations without the later assumption that a current backing-store copy necessarily exists while a page is resident in main memory.

The historical sources use terms such as `block`, `page`, `page address register`, `equivalence`, `not equivalence`, `directory`, `use` digit, and `lock out`. The modern phrase **page fault** is used here only as bounded analytical shorthand for the documented `not equivalence` interrupt path; it is not silently projected back as the paper's own vocabulary.

## Historical record

### H/P — Atlas presents core and drum as an apparent one-level central store

Kilburn, Edwards, Lanigan, and Sumner's April 1962 paper describes the Atlas central store as a fast core store plus drum store whose transfers are made automatic so that the combination can appear to the programmer as one storage level. The implementation works in 512-word blocks; the physical core positions holding such blocks are called `pages` in the paper.

This is not merely a capacity statement. The one-level appearance depends on retained translation and transfer machinery that decides where a demanded block currently resides and moves it when necessary.

### H/P — A Page Address Register binds a virtual block designation to a current core page

Each core-store page position has a Page Address Register (`P.A.R.`) containing the address of the block currently occupying that page. A demanded block address is compared with the P.A.R.s. An `equivalence` permits access to the matching page position; a `not equivalence` causes an interrupt and enters a fixed-store routine that organizes the required core/drum transfers.

The important retention relation is therefore already visible in period vocabulary:

```text
block designation
    !=
current core page position
```

The block can move while its program-visible designation remains the same.

### H/P — Drum location is separately retained in a directory and can change on write-back

The 1962 paper says that a block written from core to drum is placed in the first available empty block position on any drum. Because the physical drum destination is therefore not fixed by the block's logical designation, transfers are performed by reference to a **directory stored in subsidiary store**, and that directory is updated whenever a transfer occurs.

On a later read, the drum-transfer routine first determines the absolute drum position of the required block, transfers it to an empty core page, and updates the relevant P.A.R. relation.

Thus the location relation is second-order retained state: losing the directory can make surviving drum payload difficult or impossible to resolve correctly even though the bytes/words themselves are physically present.

### H/P — One page-in request and the broader page-turn obligation are different events

After ordering a required block to be read from drum, Atlas continues by selecting a core-resident block to transfer back to drum. The paper explicitly explains the reason: preserve an empty core page position for the next required read. It describes a read from drum and a write to drum as two necessary transfers for interchange between core and drums; they are sequential but may occur in either order. A deliberately vacant core page lets the needed read occur first while the `learning` program selects a later outgoing page.

This gives a clean distinction:

> **requested-block recovery ≠ completion of the broader page-turn / free-frame maintenance obligation**.

The `use` digits and learning program help choose an outgoing page; they are replacement-policy state, not application payload.

### H/P — Core residency does not automatically mean ordinary-program admission

A `lock out` digit accompanies each P.A.R. While a drum or tape transfer is taking place to a page, ordinary program access can be prohibited even though that physical page position exists in core. When the transfer completes, the organizing program clears the lock-out state and ordinary central-machine access is admitted again.

Hence:

> **real-frame residency ≠ ordinary-program service admission**.

### H/S — Atlas normally did not keep a simultaneous drum copy of a core-resident page

S. H. Lavington's 1978 historical account states that Atlas normally kept **no copy on drum** while a page was in main core store, and contrasts this with later paging computers that could retain drum copies and avoid writing back unaltered pages.

This retrospective witness is crucial for the roadmap term `backing-copy currentness`. It blocks a modern assumption that every resident Atlas page had a current shadow copy in backing store.

The 1978 article is used as scholarship about the historical machine, not as a substitute for the 1962 paper where the latter directly specifies the mechanism.

## Retained state and control state

At least seven relations should remain separate:

1. **payload state** — the 512-word block content;
2. **virtual/program designation** — the block address used by the program-visible central-store address space;
3. **core residency relation** — which core page, if any, currently holds that block, represented through the P.A.R. relation;
4. **external drum-location relation** — where a nonresident block is currently placed on drum, retained in the directory;
5. **backing-copy state/currentness** — whether a second usable/current drum embodiment exists while the block is core-resident; in the bounded Atlas regime it normally did not;
6. **replacement/free-page state** — vacant-page availability plus `use`/learning information that guides an outgoing transfer;
7. **service-admission state** — lock-out and transfer completion determine whether ordinary program access is currently admitted.

Only the first is the user's payload. The other relations sustain addressability, relocation, recovery, and service of that payload.

## Engineering reconstruction

### E — Virtual designation is not real-frame residency

A program can continue to designate the same central-store block while the block migrates between a drum position and different core pages.

> **virtual designation ≠ real-frame residency**.

This is a stronger statement than `addresses are translated`: it identifies what must remain stable when the physical embodiment changes.

### E — Core residency is not backing-copy currentness

Lavington's no-copy observation makes Atlas an especially useful counterexample to a later dirty/clean-page intuition. If a current block is in core and no current drum copy is normally retained, then `resident in core` cannot be interpreted as `resident in core plus safely duplicated in backing store`.

> **real-frame residency ≠ current backing-copy existence**.

The outgoing write is therefore not merely optional performance cleanup. In the bounded regime it can be the operation that recreates an external embodiment before that core page is reused.

### E — Backing location and backing content are different retained relations

A drum block can be physically present while the system separately needs the directory that says which absolute drum position corresponds to which demanded block. The directory can change because Atlas writes outgoing blocks to the first available empty drum position.

> **external-location metadata ≠ payload embodiment**.

Both can be retention-critical for later resolution.

### E — A `not equivalence` interrupt is not evidence of data loss

The interrupt means the demanded block is not currently represented by an accessible matching P.A.R. relation in core. The Supervisor path resolves the block's drum location and transfers it into a core page.

Therefore, in this bounded case:

> **page-fault-like nonresidency ≠ payload loss**.

It is a temporary failure of immediate service/residency that invokes recovery/migration machinery.

### E — Page-out obligation is not an application durability request

Atlas writes a selected page to drum to sustain the one-level-store operating regime and preserve a vacant core page for future demand. That is a placement/retention-maintenance obligation inside the storage hierarchy.

It must not be silently rewritten as a modern `fsync`, database commit, or explicit crash-durability contract:

> **page-out / replacement transfer ≠ application durability request**.

The present sources do not establish Atlas power-fail atomicity, crash-consistency ordering, or an application-visible durability boundary.

### E — Incoming recovery and outgoing capacity maintenance can be temporally decoupled

The vacant-page technique lets Atlas read the requested block first and select/write an outgoing page afterward. This means the event that restores immediate service for one designation can be distinct from the maintenance work that restores the reserve needed for the next miss.

> **current request satisfied ≠ replacement/free-page infrastructure fully restored**.

### E — Residency is still not enough for availability

During a transfer the lock-out state can deny ordinary program access to a core page. So a physical-presence bit alone cannot answer whether a block is presently usable by the requesting program.

> **physical residency ≠ current service admissibility**.

This anticipates a distinction that reappears in cache, distributed-storage, and transaction cases without implying historical descent.

## Functional comparison with later paging

### A — Atlas is a counterexample to a universal dirty-page model

Later virtual-memory systems often distinguish clean resident pages that still have an unchanged backing copy from dirty resident pages that require write-back. Lavington explicitly contrasts that later practice with Atlas's usual no-copy-on-drum regime.

That makes later `dirty bit`, `swap cache`, `anonymous memory`, and `writeback` vocabulary useful only as **functional comparison**. Those terms must not be attributed to the 1962 authors unless independently found in period sources.

The stable comparison question is narrower:

```text
What designation remains stable?
Where is the current embodiment?
Does another current embodiment exist?
What metadata resolves the external location?
What must be written before a frame can be reused?
What event restores service after nonresidency?
```

## Prior art and novelty boundary

The 1962 IRE paper is a strong primary mechanism source, not a safe invention date. John Fotheringham published `Dynamic Storage Allocation in the Atlas Computer, Including an Automatic Use of a Backing Store` in *Communications of the ACM* in October 1961. An IEEE institutional history also records relevant University of Manchester/NRDC paging-related UK patent applications filed in March and April 1960.

These earlier records constrain novelty language. This case therefore does **not** claim:

- that the April 1962 paper is the first conception of virtual memory;
- that Atlas is the sole possible priority claimant in every definition of virtual memory;
- that the modern term `virtual memory` was the period term used throughout the 1962 mechanism paper;
- or that later paging systems inherit Atlas's exact no-copy, replacement, or directory semantics.

The defensible historical claim is simply that the 1961–1962 Atlas record supplies an early, directly documented one-level-store/paging mechanism with automatic movement between core and drum and separable designation, residency, location, replacement, and admission state.

## Philosophical limit

### I — Stable availability can depend on retained relations rather than stable embodiment

Atlas makes one conceptual point unusually concrete: what remains available to a program can be the **designation and resolution relation**, not a permanently fixed material location. A block can move while the system maintains enough state to treat later access as access to the same block.

This does not make Atlas a proof of `tertiary retention`, `Bestand`, or any general theory of immateriality. The physical core/drum embodiments, directory, P.A.R.s, Supervisor code, and transfer time are exactly what make the apparently location-independent object operationally available.

## Cross-case result

Case 107 extends the repository's identity/availability decomposition without making paging a derivative of mapped Flash or cache:

```text
Case 08   stable main-storage designation can outlive cache-copy residency
Case 72   a modified cache copy can temporarily outrun main-storage currentness
Case 04   Flash logical identity can outlive physical-block location through mapping
Case 107  Atlas block designation can outlive core-page residency while drum location,
          copy existence, replacement obligation, and service admission remain separate
```

This is a functional comparison across unlike mechanisms, not a genealogy.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Atlas automatic core/drum transfers present the central store as an apparent one-level store | H/P | Kilburn et al. 1962, primary paper |
| 512-word blocks can occupy different core `page` positions and P.A.R.s identify the block currently there | H/P | Kilburn et al. 1962, printed p. 279 |
| `not equivalence` invokes interrupt/Supervisor transfer work | H/P | Kilburn et al. 1962, printed p. 279 |
| outgoing blocks can be written to the first available empty drum position and located through an updated directory | H/P | Kilburn et al. 1962, printed p. 279 |
| a requested read and a separate outgoing write compose the bounded page-turn regime | H/P | Kilburn et al. 1962, printed pp. 279–280 |
| lock-out can make a core page unavailable to an ordinary program during transfer | H/P | Kilburn et al. 1962, printed p. 280 |
| Atlas normally retained no simultaneous drum copy of a core-resident page | H/S | Lavington 1978 historical account, printed p. 5 |
| virtual designation = real-frame residency | X | contradicted by P.A.R./transfer mechanism |
| core residency = current backing-copy existence | X | contradicted by Lavington's bounded Atlas account |
| page-fault-like nonresidency = payload loss | X | contradicted by transfer/recovery path |
| page-out transfer = modern application durability contract | X | not established |
| Atlas paging semantics = universal later virtual-memory semantics | X | not established |
| 1962 paper date = invention priority | X | not established |

## Related repositories

A current GitHub search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for Atlas paging / `one-level store` did not expose a dedicated case to reuse. A complete Atlas engineering history, patent genealogy, comparative virtual-memory chronology, later page-replacement evolution, or controller/MMU implementation history belongs there if pursued broadly. This repository keeps the bounded retention relation among designation, residency, backing-copy currentness, external location, page-out work, and recovery.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) remains the anti-anachronism guard. Terms such as `virtual designation`, `real-frame residency`, `backing-copy currentness`, and `page-fault recovery` are project analytical vocabulary; they are not attributed to Atlas engineers unless independently present in the period source.

## Sources

1. T. Kilburn, D. B. G. Edwards, M. J. Lanigan, and F. H. Sumner, **“One-level storage system,”** *IRE Transactions on Electronic Computers* EC-11(2), April 1962, pp. 223–235. Page-preserving public copy used here: <https://tcm.computerhistory.org/ComputerTimeline/Chap23_atlas_CS1_10CS2.pdf>. Mechanism anchors: reprint printed pp. 279–280, especially the P.A.R./equivalence path, directory, vacant-page/write-back sequence, and lock-out behavior.
2. John Fotheringham, **“Dynamic Storage Allocation in the Atlas Computer, Including an Automatic Use of a Backing Store,”** *Communications of the ACM* 4(10), October 1961, pp. 435–436, DOI 10.1145/366786.366800. Used here only as an earlier publication floor unless the original full text is inspected in a later pass.
3. S. H. Lavington, **“The Manchester Mark I and Atlas: A Historical Perspective,”** *Communications of the ACM* 21(1), January 1978, especially printed pp. 5–6: <https://pages.cs.wisc.edu/~remzi/Classes/537/LectureNotes/Papers/atlas.pdf>. Used for the historical no-copy-on-drum comparison and later-versus-Atlas boundary.
4. IEEE Engineering and Technology History Wiki, **“Atlas Computer and the Invention of Virtual Memory, 1957–1962,”** institutional milestone/history page: <https://ethw.org/Milestones%3AAtlas_Computer_and_the_Invention_of_Virtual_Memory%2C_1957-1962>. Used only for patent-navigation/application-date context and institutional retrospective, not as a substitute for the primary 1962 mechanism paper or as an unqualified priority proof.
'''

evid = r'''# Atlas 1961–1978 one-level-store paging grounding record

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
'''

CASE.write_text(case.rstrip() + '\n', encoding='utf-8')
EVID.write_text(evid.rstrip() + '\n', encoding='utf-8')

road = ROAD.read_text(encoding='utf-8')
old_road = '- [ ] In paging, how should `virtual designation`, `real-frame residency`, `backing-copy currentness`, `external-location state`, `page-out obligation`, and `page-fault recovery` be separated?'
new_road = '- [x] In paging, separate `virtual designation`, `real-frame residency`, `backing-copy currentness`, `external-location state`, `page-out obligation`, `page-fault recovery`, and transfer-time service admission — grounded in [`cases/107-atlas-one-level-store-paging-residency.md`](cases/107-atlas-one-level-store-paging-residency.md), with [`evidence/107-atlas-1961-1978-paging-grounding.md`](evidence/107-atlas-1961-1978-paging-grounding.md). The bounded Atlas 1961–1962 one-level-store record separates stable block designation from current core page, relocatable drum location/directory state, non-equivalence recovery, outgoing page-turn work, and lock-out admission; Lavington 1978 supplies the crucial historical witness that Atlas normally kept no simultaneous drum copy of a core-resident page. This closes the relation-decomposition question only for the bounded Atlas regime; full virtual-memory/patent genealogy, later clean/dirty backing-copy policy, OS-specific swap semantics, crash/power-fail durability composition, and fault injection remain open and should be coordinated with `computing-archaeology`.'
if old_road not in road:
    raise SystemExit('missing open paging roadmap item')
road = road.replace(old_road, new_road, 1)
ROAD.write_text(road.rstrip() + '\n', encoding='utf-8')

index = INDEX.read_text(encoding='utf-8')
if '(cases/107-atlas-one-level-store-paging-residency.md)' in index:
    raise SystemExit('Case 107 index row already exists')
lines = index.splitlines()
inserted = False
for i, line in enumerate(lines):
    if '(cases/106-ddr5-same-bank-refresh-parallel-target-set.md)' in line:
        row = '| [Atlas One-Level Store: Virtual Designation, Core Residency, Drum Location, and Page-Turn Obligation](cases/107-atlas-one-level-store-paging-residency.md) | **grounded** | program-visible block designation + relocatable core/drum embodiment + P.A.R./directory resolution state + replacement/free-page work + lock-out admission | separate virtual designation, core residency, backing-copy currentness, external location, page-turn work, and page-fault-like recovery without importing later dirty-page or durability semantics | [1961–1978 Atlas paging grounding](evidence/107-atlas-1961-1978-paging-grounding.md); full VM/patent genealogy, later copy/dirty policy, crash durability, controller/OS implementation, and fault validation remain separate work |'
        lines.insert(i + 1, row)
        inserted = True
        break
if not inserted:
    raise SystemExit('missing Case 106 row anchor')
index = '\n'.join(lines).rstrip() + '\n'

if '1651. **virtual designation ≠ real-frame residency**' in index:
    raise SystemExit('Case 107 findings already exist')
if '1650. **Cases 105/106 form a functional comparison, not a direct genealogy**' not in index:
    raise SystemExit('missing finding 1650 anchor')
findings = r'''
1651. **virtual designation ≠ real-frame residency** — an Atlas block address remains the program-facing designation while the current core page can change or be absent.
1652. **P.A.R. correspondence ≠ permanent physical home** — a Page Address Register records which block currently occupies a core page; it does not make that page the block's enduring location.
1653. **real-frame residency ≠ backing-copy currentness** — a core-resident Atlas page normally need not have a simultaneous current drum copy in the bounded historical regime.
1654. **core residency ≠ duplicated durability** — physical presence in core does not by itself establish a second retained embodiment or a crash-durability guarantee.
1655. **external-location directory state ≠ payload** — the drum directory tells Atlas where a nonresident block is placed after relocatable write-back; the location relation is retention-critical control state distinct from the block contents.
1656. **`not equivalence` ≠ payload loss** — absence of a matching accessible core-page relation invokes transfer/recovery rather than proving the requested block has disappeared.
1657. **page-fault-like recovery ≠ programmer-managed overlay** — Atlas's documented fixed-store/Supervisor path automates the transfer that earlier two-level regimes could require the programmer to schedule explicitly.
1658. **incoming read completion ≠ page-turn maintenance completion** — servicing the requested block and restoring a vacant-page reserve through a separate outgoing write are distinct events.
1659. **page-out obligation ≠ application durability request** — the outgoing drum transfer sustains residency/replacement capacity inside the one-level store; the sources do not make it an `fsync`-like crash-persistence contract.
1660. **vacant core page ≠ unallocated virtual block** — an intentionally empty physical page position is capacity reserved for movement; it says nothing about whether the program-visible block designation exists.
1661. **core-page residency ≠ ordinary-program admission** — Atlas lock-out can make a physically resident/transfer-target page temporarily unavailable to the ordinary program.
1662. **transfer completion ≠ designation creation** — clearing lock-out and establishing the P.A.R. relation restores service for an already designated block; it does not create that block's logical identity.
1663. **page replacement ≠ forgetting** — moving a selected block from core to a directory-resolved drum location can end one physical residency while preserving the block's designation and later recoverability.
1664. **same virtual block ≠ same physical embodiment** — Atlas one-level storage is a direct historical case in which identity can continue through migration between core and drum positions.
1665. **Atlas paging ≠ universal later virtual-memory copy policy** — later clean/dirty-page and retained-backing-copy regimes are legitimate functional comparisons, but Lavington's no-copy witness blocks projecting them onto Atlas as if the semantics were identical.
'''
index = index.rstrip() + '\n' + findings.strip() + '\n'
INDEX.write_text(index, encoding='utf-8')

# Final bounded validation.
for path in (CASE, EVID, ROAD, INDEX):
    text = path.read_text(encoding='utf-8')
    if '\t' in text:
        raise SystemExit(f'tab introduced in {path}')
    path.write_text(text.rstrip() + '\n', encoding='utf-8')

checks = {
    CASE: [
        'virtual designation ≠ real-frame residency',
        'real-frame residency ≠ current backing-copy existence',
        'page-out / replacement transfer ≠ application durability request',
        'real-frame residency ≠ ordinary-program service admission',
    ],
    EVID: [
        'printed pp. **279–280**',
        'no copy was normally kept on drum',
        'Atlas 1961–1978 one-level-store paging grounding record',
    ],
    ROAD: [
        'cases/107-atlas-one-level-store-paging-residency.md',
        'full virtual-memory/patent genealogy',
    ],
    INDEX: [
        '(cases/107-atlas-one-level-store-paging-residency.md)',
        '1651. **virtual designation ≠ real-frame residency**',
        '1665. **Atlas paging ≠ universal later virtual-memory copy policy**',
    ],
}
for path, needles in checks.items():
    text = path.read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'missing {needle!r} in {path}')

print('Case 107 Atlas paging slice integrated')
