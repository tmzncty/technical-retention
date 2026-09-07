# Atlas One-Level Store: Virtual Designation, Core Residency, Drum Location, and Page-Turn Obligation

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
