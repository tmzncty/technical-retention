# Evidence 04E — TrueFFS 2003–2004 mapping coherence across power failure and restart reconstruction

## Status

**`bounded deepening complete`** — this record deepens Case 04 only at the boundary between **logical-currentness metadata, power-failure update semantics, and restart reconstruction of the volatile mapping view**.

Canonical case: [`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md)

Preceding power-failure slice: [`04-m-systems-2001-2003-interrupted-erase-recovery-deepening.md`](04-m-systems-2001-2003-interrupted-erase-recovery-deepening.md)

The bounded question is:

> When a Flash translation layer deliberately moves a logical sector to a new physical location, what must remain after sudden power loss so that restart can still determine which physical embodiment counts as current?

The inspected 2003–2004 TrueFFS record supplies a product-level answer that was not established by the 1993 Ban patent alone:

- critical mapping information is retained in Flash rather than only in the live RAM table;
- the RAM-resident mapping table can be **reconstructed or verified** from Flash-resident information after power restoration or media reconnection;
- mapping updates participate in an `erase after write` regime in which old data are not retired before the replacement has completed and been verified;
- interrupted garbage collection is restarted rather than treated as completed merely because some relocation work occurred;
- a first-time write with no previously committed copy remains a deliberate counterexample: the new data can be lost if the fault occurs before it has become safely resident.

This closes a narrower part of the canonical debt `add power-failure / atomicity evidence before making claims about mapping-update crash consistency`.

It does **not** close that debt universally and does **not** retroactively prove that the exact 1993 Ban implementation had the later TrueFFS product behavior documented here.

---

## Why this slice is distinct from Evidence 04D

Evidence 04D established a different failure boundary:

```text
intended erase
    != completed erase
    != qualified reusable erase unit
```

That slice showed how M-Systems retained enough pending/completion history to avoid mistaking an interrupted destructive erase for a successfully erased unit.

This file asks a different question:

```text
new physical embodiment written
    != current logical embodiment published
    != volatile runtime map surviving
```

The object being protected is not only the physical erase state of a unit. It is the **relation that says which physical embodiment currently answers for a logical sector**.

The two recovery problems compose but must not be collapsed:

```text
operation-completion evidence
    protects reuse authority

mapping/currentness evidence
    protects logical resolution authority
```

A storage system can need both.

---

## Evidence classes used here

- `H/P` — primary manufacturer product documentation from M-Systems;
- `H/C` — contemporary third-party product/integration documentation from Wind River;
- `E` — engineering reconstruction from documented mechanisms;
- `A` — bounded functional analogy to another technical-retention case;
- `I` — project-level philosophical/media interpretation;
- `X` — rejected shortcut / non-claim.

Project terms such as `currentness evidence`, `publication`, `resolution authority`, and `reconstructed currentness map` are analytical vocabulary. They are **not** attributed to M-Systems or Wind River as historical terms.

---

## Source ledger

### S1 — M-Systems, *DiskOnChip 2000 DIP Data Sheet*, Rev. 3.8, September 2004 (`H/P`)

- Corporate author: **M-Systems Flash Disk Pioneers**.
- Product: **DiskOnChip 2000 DIP**, 16 MByte to 1 GByte.
- Revision: **3.8**.
- Date: **September 2004**.
- Document number: `91-SR-002-42-8L`.
- Manufacturer-authored PDF currently mirrored by DigiKey:
  <https://media.digikey.com/pdf/Data%20Sheets/M-Systems%20Inc%20PDFs/MD2200(02,03)-D.pdf>
- Relevant printed section: **§5.2 Power Failure Management**, printed p. 12.

Custody note:

The inspected PDF is plainly M-Systems-authored and carries the M-Systems corporate mark, revision, document number, and date, but this copy is presently served by a distributor mirror rather than the historical `m-systems.com` host. The evidence class is therefore **manufacturer-authored product documentation with mirrored custody**, not a claim that the current download endpoint is an original archive.

Why S1 matters:

- the first page advertises both `Dynamic virtual mapping` and data integrity across power failure as named product capabilities;
- §5.2 connects power-failure handling directly to mapping-information update/storage;
- it explicitly distinguishes Flash-resident mapping information from a smaller RAM-resident table used to locate it;
- it explicitly says the RAM table is reconstructed after power-up/reset from Flash-resident information;
- it exposes a service-level old-or-new validity rule around interrupted writes.

### S2 — Wind River Systems, *VxWorks Programmer’s Guide 5.5*, Edition 2, 5 March 2003 (`H/C`)

- Corporate author: **Wind River Systems, Inc.**
- Title: *VxWorks Programmer’s Guide 5.5*.
- Edition: **2**.
- Date: **5 March 2003**.
- Part number: `DOC-14617-ZD-01`.
- Contemporary PDF copy hosted by Jefferson Lab:
  <https://prex.jlab.org/wiki/images/8/86/Vxworks_programmers_guide5.5.pdf>
- Relevant chapter: Flash Memory Block Device Driver / TrueFFS.
- Relevant printed pages: **340–344**, especially **343–344**, `Fault Recovery in TrueFFS`.

Custody note:

This is a Wind River manual describing TrueFFS integration and operation in the VxWorks 5.5 environment. It is contemporary technical documentation but is **not** M-Systems-authored documentation. It is therefore used as an independent contemporary implementation/integration witness, not as a substitute for M-Systems internal design records.

Why S2 matters:

- it describes dynamic block-to-Flash mapping and transfer-unit reclamation in operational terms;
- it states that faults may occur during host write, garbage collection, erase, or format;
- it documents `erase after write`, verification, and write retry;
- it states that critical mapping information is Flash-resident while the RAM mapping table is rebuilt or verified from that retained information;
- it adds the useful detail that erase-unit headers at predictable locations can be cross-checked to rebuild or verify the RAM copy;
- it explicitly says incomplete garbage collection must restart;
- it also preserves an important negative boundary: new data being written for the first time can be lost.

### S3 — Amir Ban / M-Systems, US 5,404,485, “Flash file system,” filed 8 March 1993 (`H/P`, contextual anchor only)

- Google Patents:
  <https://patents.google.com/patent/US5404485A/en>

S3 remains the canonical historical anchor for:

- virtual versus physical address spaces;
- out-of-place replacement;
- transfer-unit reclamation;
- stable logical-unit identity despite physical relocation;
- retention/reconstruction of mapping support.

This packet does **not** treat the 2003–2004 TrueFFS behavior as proof that every mechanism described in S1/S2 was already present, unchanged, in S3.

Safe chronology:

```text
1993-filed Ban mapping design
    -> establishes mapped-Flash identity/relocation problem

2003–2004 TrueFFS documentation
    -> establishes a later shipped/product software contract
       for power-failure mapping coherence and restart reconstruction
```

Chronological continuity within the same corporate/product lineage is useful context, but exact implementation descent remains separate historical work.

---

## Historical / implementation record

### 1. S1 presents dynamic virtual mapping and power-failure integrity as features of the same named product stack (`H/P`)

The DiskOnChip 2000 data sheet presents TrueFFS as the software layer that provides hard-disk emulation over NAND Flash. On the first page it names both:

- `Dynamic virtual mapping`; and
- data integrity across power failure.

This matters because the power-failure claim is not attached only to raw cell nonvolatility. The later §5.2 explanation explicitly reaches into **mapping-information update and recovery**.

Historical claim:

> By September 2004, M-Systems publicly documented a DiskOnChip/TrueFFS product in which logical mapping and power-failure management were part of the same exposed storage-service contract.

This is stronger than a generic later textbook statement that FTL metadata “must be crash consistent.”

### 2. S1 says mapping information itself is updated under the `erase after write` regime (`H/P`)

Section 5.2 states that TrueFFS uses an `erase after write` approach rather than destroying the old state before the replacement is safely established.

The same section then applies that rule to **mapping information**, not only to user payload.

The source-level relation is therefore:

```text
payload update safety
    and
mapping-information update safety

share a documented power-failure management regime
```

The document says mapping information remains coherent through power failure.

It does **not** disclose the exact commit-bit encoding, generation counter, log ordering, or NAND-page layout by which this coherence is implemented.

### 3. The live RAM mapping table is not the sole retained representation of the map (`H/P`)

S1 draws a direct representation boundary:

- actual mapping information is stored in Flash;
- the mapping information in RAM is only a table pointing to where that actual mapping information resides;
- after power-up or reset, that RAM table is reconstructed from the Flash-resident information.

This gives Case 04 an important new restart boundary:

```text
RAM mapping representation disappears
    !=
mapping relation disappears
```

The volatile representation can be lost because the system retains enough authoritative/reconstructible evidence elsewhere to create a usable runtime view again.

### 4. The product-level update contract preserves an old valid sector until a new one is completed and verified (`H/P`)

S1 states that previous data are not erased until the operation has completed and the new data have been verified.

At the storage-service level, it presents a two-outcome contract:

```text
operation completed
    -> new sector contents valid

operation incomplete / failed
    -> old sector contents remain valid
```

This is a statement about TrueFFS-visible sector validity, not a proof that an interrupted NAND page contains no partial analog/programming state.

The source itself is describing how the software/storage architecture prevents such an interrupted physical candidate from becoming a partially published logical sector.

### 5. S2 independently describes read-back verification and retry on another Flash location (`H/C`)

Wind River’s 2003 guide describes the same operational boundary in more detail.

For a write/update:

1. the previous data are not erased before the update succeeds;
2. the written candidate is read back and compared with the user data;
3. a failed write can be retried at a different Flash location;
4. successful completion makes the new sector valid;
5. failed update leaves the old data available.

This makes verification part of the documented transition from **candidate embodiment** to **accepted current data**.

Engineering significance:

```text
bits were attempted at a new location
    !=
that location has earned currentness
```

### 6. S2 says critical mapping information is Flash-resident and survives power interruption/removal (`H/C`)

The `Recovering Mapping Information` subsection says critical mapping information is stored in Flash-resident memory so it is not lost merely because power disappears or the medium is removed.

It then distinguishes that from the RAM-resident mapping table used during operation.

After restoration/reconnection, the RAM table is:

- reconstructed; or
- verified

from the Flash-resident information.

This is unusually direct contemporary evidence for the distinction:

```text
retained mapping evidence
    !=
volatile operational mapping view
```

### 7. S2 identifies erase-unit headers as restart evidence used to rebuild/verify the RAM map (`H/C`)

Wind River adds a detail absent from the short product-sheet description: mapping information can reside anywhere on the medium, while each erase unit has header information at a predictable location.

The guide says TrueFFS can cross-check these headers to rebuild or verify the RAM mapping table.

The bounded historical statement is therefore:

> TrueFFS’s restart reconstruction uses Flash-resident per-erase-unit header information as evidence from which the runtime mapping view can be rebuilt or checked.

The source does not expose enough layout detail here to reconstruct the exact version-selection algorithm.

### 8. Mapping reconstruction is therefore not byte-for-byte persistence of the live RAM table (`E`, grounded directly in S1/S2)

A common shortcut would be:

```text
mapping survives power failure
    -> the mapping table itself must be nonvolatile
```

The documentation rejects that simplification.

A more precise description is:

```text
Flash-resident mapping evidence survives
        +
restart procedure interprets/cross-checks it
        ->
RAM-resident mapping table is reconstituted
```

What persists is enough evidence for the **relation** to be recovered, not necessarily the exact in-memory data structure that existed one instruction before power loss.

### 9. Interrupted garbage collection is restarted rather than promoted to completed progress (`H/C`)

S2 says that if a fault interrupts garbage collection, that incomplete garbage-collection operation must be restarted.

Its reclamation sequence is described as:

```text
move still-needed data to another transfer unit
    -> erase original unit
```

The restart rule matters because partial maintenance work is not automatically treated as proof of completion.

This gives the bounded relation:

```text
some relocation work may have occurred
    !=
GC completion is established
```

This is a maintenance-progress rule, not the same thing as mapping-currentness selection.

### 10. S2 preserves a crucial counterexample: first-time new data can still be lost (`H/C`)

Wind River explicitly says TrueFFS can recover from the listed fault scenarios **except when new data are being written to Flash for the first time**; that not-yet-safely-stored new data can be lost.

This blocks a tempting overclaim:

```text
power-failure coherent mapping
    !=
every in-flight host write is guaranteed to survive
```

The old-or-new fallback works especially clearly when there is an **old valid state to fall back to**.

For a first publication of entirely new data, there may be no older committed embodiment that can satisfy the request after interruption.

### 11. S2 also gives a bounded degraded-mode outcome when relocation resources fail (`H/C`)

During garbage collection, TrueFFS can retry a failed transfer using another transfer unit.

If all transfer units fail, the guide says the medium can cease accepting new data and become read-only while already stored user data remain safe.

This produces another useful retention distinction:

```text
ability to retain/read already committed state
    !=
ability to continue accepting mutations
```

A system can preserve current readable state while losing the maintenance headroom needed for continued writable service.

---

## Engineering reconstruction

### E1 — The authoritative relation can outlive one of its operational representations

The runtime RAM table is useful for efficient resolution, but S1/S2 show it is not the sole embodiment of the mapping relation.

A bounded reconstruction is:

```text
logical sector L
    -> current physical embodiment P

is operationally represented in RAM during service

but

restart can derive/verify that relation
from Flash-resident mapping/header evidence
```

Therefore:

> **representation persistence is not required if relation-supporting evidence persists and the representation is reconstructible.**

This is a project-level engineering statement, not TrueFFS’s historical wording.

### E2 — Mapping currentness requires a publication boundary, not merely a successful physical program attempt

The sources document three separate facts:

- candidate data can be written to another location;
- write success is verified;
- mapping information is kept coherent under the same power-failure regime.

Together they support the conservative reconstruction:

```text
candidate embodiment exists
    !=
candidate embodiment is current
```

A logical update needs some transition in retained mapping/currentness evidence after or together with successful verification.

The exact low-level ordering of every metadata program operation is **not** disclosed, so this packet stops before asserting a specific commit protocol.

### E3 — Safe fallback depends on retaining an older admissible state until replacement is qualified

The product contract is naturally reconstructed as:

```text
old valid embodiment + old valid currentness evidence
        |
        v
write new candidate elsewhere
        |
        v
verify candidate
        |
        v
establish coherent mapping/currentness for replacement
        |
        v
retire/reclaim old embodiment later
```

Power failure at an intermediate point is survivable because the architecture avoids destroying the only established version before the replacement has earned validity.

This is **not** a claim that all metadata transitions are one atomic NAND program.

### E4 — Nonvolatile payload is insufficient without nonvolatile or reconstructible currentness evidence

Suppose both old and new physical payloads survive a power cut.

Physical survival alone does not answer:

> Which one counts?

That question is resolved by retained mapping/header state plus the restart interpretation procedure.

Therefore:

```text
payload survival
    !=
currentness determination
```

This deepens the canonical Case-04 claim that the retained object is `data + a retained mapping relation`.

### E5 — Restart reconstruction is a controlled form of forgetting

TrueFFS does not need to preserve the full live RAM table across the outage.

It can lose that derived representation and later rebuild it from stronger retained evidence.

The safely forgettable state is therefore not arbitrary. What can be discarded is the part that is **derivable from a more authoritative retained substrate**.

### E6 — Garbage-collection progress and mapping authority are separate recovery dimensions

S2’s restart rule says incomplete GC must be restarted.

That does not imply that every already verified relocated sector becomes invalid. Nor does successful survival of mapping evidence imply that the GC operation as a whole completed.

Thus:

```text
current logical mapping after restart
    !=
maintenance operation completed before crash
```

A system can recover the correct logical state while still owing maintenance work.

### E7 — Free/transfer capacity is also failure-recovery infrastructure

The ability to retry a failed relocation in another transfer unit depends on having alternative writable space.

This extends the canonical Case-04 observation that reserved capacity is not simply unused storage.

Here it also functions as:

- relocation workspace;
- retry headroom;
- a condition for continued writable service after local Flash failures.

If that headroom collapses, S2 allows a read-only outcome rather than sacrificing already committed data.

---

## Failure-window matrix

| Failure window | What may have happened physically | What retained evidence matters | Safe restart / service claim supported by source | What is **not** proved |
| --- | --- | --- | --- | --- |
| Before new candidate has safely completed | partial/failed new write possible | old valid data + old mapping/currentness evidence | old data remain valid for an update case | exact NAND-cell state of failed page |
| New candidate written but verification not established | candidate bits may exist | old state remains authoritative until success is established | do not promote candidate merely because it exists | exact hidden commit marker ordering |
| After successful write/verification during mapping update | new candidate is qualified at service level | coherent Flash-resident mapping information | restart can recover which embodiment counts | one universal atomic metadata primitive |
| Power loss destroys RAM table | RAM working view gone | Flash-resident mapping/header information | reconstruct or verify RAM map after restart | byte-identical recovery of pre-crash RAM structure |
| Power loss during GC | some copies/moves may have occurred | retained payload + mapping/header evidence | restart incomplete GC | preservation of exact GC progress cursor |
| All transfer units become unusable | existing committed payload may remain | already safe user data/current mappings | device may become read-only | continued mutation service |
| First-time write of genuinely new data interrupted | no prior committed version may exist | no old payload fallback for that new value | new data may be lost | universal write-survival guarantee |

The table is a project reconstruction of source-described boundaries. It is not a recovered TrueFFS internal state machine.

---

## Relation to Evidence 04D: completion evidence versus currentness evidence

The preceding interrupted-erase packet and this mapping packet expose two different kinds of retained control evidence.

### Evidence 04D

The system needs to know:

```text
Was this destructive erase proven complete?
```

If not, the physical unit cannot safely regain reuse authority.

### Evidence 04E

The system needs to know:

```text
Which physical embodiment is the current value of this logical sector?
```

If the runtime table disappears, restart must reconstruct/verify that relation from retained Flash evidence.

The combined model is:

```text
currentness authority
    decides which data embodiment counts

completion/reuse authority
    decides which physical region can safely be reused
```

These are related but not interchangeable.

---

## Functional comparisons

### A — SQLite WAL checkpoint restart (Case 152)

Case 152 shows a different system in which the runtime checkpoint-progress value `nBackfill` can be discarded after restart while stronger committed WAL evidence is retained and replayable/reconstructible.

The bounded functional similarity is:

```text
TrueFFS
    volatile RAM mapping view may disappear
    -> rebuild/verify from retained Flash evidence

SQLite WAL
    checkpoint progress may disappear
    -> reconstruct WAL geometry and conservatively replay maintenance
```

The analogy is **not** historical genealogy and the retained evidence differs radically.

TrueFFS is reconstructing a logical-to-physical resolution relation over Flash; SQLite is reconstructing database/WAL recovery state.

### A — Kafka cleaner checkpoint currentness (Case 42)

Kafka supplies an opposite warning: a persisted cleaner coordinate can survive as bytes while the log geometry to which it refers changes, so the coordinate may require validation/reset.

The useful contrast is:

```text
persisting a derived coordinate
    may require later currentness validation

reconstructing a derived view from retained substrate evidence
    may avoid trusting one stale runtime image
```

This does not establish that reconstruction is always superior to checkpointing. It identifies different recovery contracts.

### A — Copy-on-write

The old-valid/new-candidate transition is functionally copy-on-write-like because replacement is created before the old embodiment is retired.

This remains a functional analogy only.

This packet does not claim TrueFFS inherited filesystem COW algorithms or shares their transaction semantics.

---

## Philosophical / media-theoretical interpretation

### I1 — Logical identity can survive both relocation and loss of a volatile interpreter representation

The canonical Case 04 already showed:

```text
same logical identity
    !=
same physical location
```

This packet adds:

```text
same recoverable logical identity
    !=
same surviving runtime mapping-table embodiment
```

The relation can be materially exteriorized in a form from which a temporary operational representation is regenerated.

The conceptual pressure point is therefore not “information becomes immaterial.” It is the opposite: continuity depends on **multiple material embodiments playing different roles**.

### I2 — What survives is partly a rule for deciding what counts

Old and new physical sectors may both remain present across part of an update window.

Retention of the user object therefore depends not only on preserving bit patterns but on preserving enough evidence to decide which pattern has current authority.

This sharpens, but does not universalize, the repository’s broader claim that retention can be relational.

### I3 — Forgetting one representation can preserve a stronger continuity

The live RAM table may vanish at power loss without constituting loss of the logical storage relation, because it is reconstructible from Flash-resident evidence.

This is a useful counterexample to the intuition that maximum continuity means preserving every intermediate representation.

Some derived state may be safely forgotten precisely because the system preserves the evidence needed to recreate it.

### I4 — No direct Heidegger/Stiegler equivalence follows

Nothing in this packet licenses the equations:

```text
mapping table = tertiary retention
```

or

```text
logical-sector currentness = Bestand
```

The sources establish a technical mechanism. Philosophical comparison must remain downstream of that mechanism and preserve the distinction between machine-operational control metadata and cultural/epistemic trace.

---

## Explicit non-claims / stop conditions

1. **X:** This packet does not prove that US 5,404,485 in 1993 implemented the exact 2003–2004 TrueFFS recovery scheme.
2. **X:** It does not claim all TrueFFS releases used an identical on-media format.
3. **X:** It does not claim all DiskOnChip generations used the same mapping headers or update ordering.
4. **X:** It does not recover the exact binary layout of the Flash-resident mapping information.
5. **X:** It does not recover the exact erase-unit header fields used for map reconstruction.
6. **X:** It does not prove a particular generation counter, sequence number, commit bit, journal, or checksum was used unless separately sourced.
7. **X:** It does not prove every metadata program is individually atomic at the NAND-cell level.
8. **X:** The service-level statement that a sector is old-or-new does not mean an interrupted physical NAND page contains no partially programmed cells.
9. **X:** `mapping coherent during power failure` is not expanded into a claim of universal filesystem-level transaction atomicity.
10. **X:** It does not claim every in-flight host write survives sudden power loss.
11. **X:** The Wind River manual explicitly blocks that claim for first-time new data.
12. **X:** It does not claim successful physical programming alone publishes a new logical value.
13. **X:** It does not claim physical survival of an old copy means that old copy remains logically current.
14. **X:** It does not claim physical survival of a new candidate means that candidate is logically current.
15. **X:** It does not claim the RAM table itself is nonvolatile.
16. **X:** It does not claim restart reconstructs a byte-identical RAM data structure.
17. **X:** It does not claim reconstructed mapping evidence is infallible under arbitrary multi-bit corruption or catastrophic media damage.
18. **X:** It does not claim all erase-unit headers survive every failure model.
19. **X:** It does not equate mapping reconstruction with garbage-collection completion.
20. **X:** It does not equate a restartable incomplete GC operation with a retained exact GC-progress checkpoint.
21. **X:** It does not claim read-only degraded service preserves the ability to accept new state.
22. **X:** It does not claim alternative transfer units eliminate all correlated Flash failures.
23. **X:** It does not turn `erase after write` into a universal historical name for all out-of-place Flash update schemes.
24. **X:** It does not identify TrueFFS with every later SSD FTL.
25. **X:** It does not infer TRIM, DEALLOCATE, crypto-erase, modern SSD superblock logging, or NVMe atomic-write semantics from these sources.
26. **X:** It does not infer modern database ACID transactions from the vendor’s sector-validity contract.
27. **X:** It does not claim Wind River independently audited every M-Systems reliability statement.
28. **X:** It does not claim current distributor/laboratory mirrors are the original publication hosts.
29. **X:** It does not establish invention priority for power-fail-safe Flash mapping.
30. **X:** It does not establish direct genealogy from filesystem copy-on-write, WAL, Kafka, or SQLite to TrueFFS.
31. **X:** It does not treat project terms such as `currentness authority` as historical TrueFFS vocabulary.
32. **X:** It does not equate controller-internal mapping state with philosophical memory or tertiary retention.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| M-Systems’ September 2004 DiskOnChip 2000 sheet names TrueFFS dynamic virtual mapping and power-failure integrity as product features | H/P | direct manufacturer-authored product document |
| The same sheet says `erase after write` is used for mapping-information update/storage | H/P | direct §5.2 statement |
| The sheet says mapping information is kept coherent across power failure | H/P | direct §5.2 statement |
| The sheet distinguishes Flash-resident mapping information from a RAM table pointing to it | H/P | direct §5.2 statement |
| The RAM table is reconstructed after power-up/reset from Flash-resident information | H/P | direct §5.2 statement |
| The product contract keeps old data valid until replacement completion/verification | H/P | direct §5.2 statement |
| Wind River 5.5 documents TrueFFS fault recovery for write/GC/erase/format | H/C | contemporary integration manual |
| Wind River documents read-back verification and retry to another Flash location after write failure | H/C | printed p. 343 |
| Wind River says critical mapping information is Flash-resident and the RAM table is reconstructed/verified after restoration | H/C | printed p. 344 |
| Wind River says per-erase-unit header information can be cross-checked to rebuild/verify the RAM mapping table | H/C | printed p. 344 note |
| Wind River says incomplete GC must restart | H/C | printed pp. 343–344 |
| Wind River says first-time new data can be lost if interrupted before safe residence | H/C | printed p. 343 |
| A volatile mapping representation can therefore disappear while the logical mapping relation remains reconstructible | E | bounded reconstruction from S1/S2 |
| A physically written candidate is not necessarily the current logical embodiment before qualification/publication | E | bounded reconstruction from write verification + mapping-coherence contract |
| Mapping currentness and erase-unit reuse completion are separate retained relations | E | comparison of 04D and 04E |
| TrueFFS proves all Flash mapping metadata updates are one physically atomic NAND operation | X | unsupported / rejected |
| The later TrueFFS behavior proves the exact 1993 Ban implementation was crash-atomic | X | unsupported / rejected |
| Power-failure-safe mapping guarantees every in-flight first write survives | X | contradicted by S2 boundary |
| Surviving physical copies alone determine which logical value is current | X | contradicted by mapping dependence |

---

## What this changes in Case 04

Before this slice, Case 04 could safely say:

```text
logical identity survives physical relocation
    +
mapping/allocation state is needed for restart
```

but it deliberately stopped short of mapping-update crash-consistency claims.

The new bounded result is stronger and narrower:

```text
for documented 2003–2004 TrueFFS / DiskOnChip practice:

Flash-resident mapping evidence
    + erase-after-write update discipline
    + verification before old-state retirement
    + reset-time reconstruction/verification of the RAM map
        ->
logical currentness can be recovered without preserving the live RAM map itself
```

The case therefore gains a concrete product-level witness for:

> **retention of the relation can be implemented as retention of reconstructible evidence rather than retention of one operational representation.**

This does not alter Case 04’s current maturity label. It deepens an already-grounded case.

---

## Remaining evidence debt

### 1. Exact mapping publication protocol

The inspected documents state the invariant but do not fully expose the internal commit protocol.

Still open:

- precise metadata record layout;
- generation/version selection;
- commit markers or checksums;
- order of data verification versus mapping-record write at NAND-operation granularity;
- handling of two individually valid but competing mapping records;
- behavior under corruption of the mapping/header evidence itself.

A source-code release, on-media format specification, patent with exact record ordering, or controlled raw-media experiment would be needed before claiming these details.

### 2. 1993 → 2003 implementation genealogy

Same-company/product-family continuity is not enough to prove mechanism identity.

Still open:

- which TrueFFS versions introduced the documented power-failure mapping scheme;
- whether early Ban-era commercial products used the same header reconstruction model;
- how DiskOnChip generations changed on-media metadata representation;
- whether later patents can establish an explicit implementation lineage.

This broader genealogy belongs primarily in `computing-archaeology` unless it changes the retention comparison.

### 3. Fault-injection validation

The sources are documentary.

Still open:

- named-device repeated sudden-power-cut experiments;
- raw Flash imaging before/after interruption;
- reconstruction of old/new mapping records;
- first-write versus rewrite behavior under controlled cuts;
- GC interruption at multiple internal phases.

Such experiments would strengthen implementation evidence but are not required for the bounded documentary claim made here.

### 4. Failure-model limits

The documents discuss ordinary power failure/hardware write failure, not every destructive event.

Still open:

- simultaneous metadata-header corruption;
- controller/firmware defect;
- torn reads from failing media;
- multiple-unit correlated failure;
- adversarial fault injection;
- loss of all retained mapping evidence.

### 5. Currentness semantics beyond sectors

This packet is about the block-device mapping layer.

It does not establish filesystem namespace transaction semantics, application-level durability, or database commit semantics above TrueFFS.

---

## Related repositories

### `tmzncty/computing-archaeology`

Fresh searches for `TrueFFS`, `TrueFFS flash mapping power failure virtual map`, and related terms found no dedicated packet to reuse.

This repository should therefore keep only the retention-specific seam:

```text
physical replacement candidate
    -> verification
    -> retained mapping/currentness evidence
    -> restart reconstruction/verification
    -> current logical resolution
```

Broader work belongs primarily in `computing-archaeology`:

- TrueFFS and DiskOnChip product chronology;
- detailed on-media format genealogy;
- M-Systems patent-family lineage;
- first commercial introduction of power-fail-safe mapping;
- Flash controller implementation history;
- later SSD FTL crash-consistency evolution.

### `tmzncty/problem-history`

Anti-anachronism remains essential.

Historical vocabulary in the inspected sources includes:

- `erase after write`;
- `mapping information`;
- `RAM-resident mapping table`;
- `flash-resident information`;
- `Recovering Mapping Information`;
- `garbage collection` in the 2003 Wind River integration context.

Project terms such as `currentness authority`, `publication boundary`, and `reconstructed currentness map` must remain labeled analysis.

---

## Sources

### Primary / manufacturer-authored

1. M-Systems Flash Disk Pioneers, **DiskOnChip 2000 DIP — Data Sheet**, Rev. 3.8, `91-SR-002-42-8L`, September 2004, especially §5.2 `Power Failure Management`, printed p. 12. Current distributor mirror:
   <https://media.digikey.com/pdf/Data%20Sheets/M-Systems%20Inc%20PDFs/MD2200(02,03)-D.pdf>

2. Amir Ban / M-Systems Flash Disk Pioneers Ltd., **“Flash file system,”** US 5,404,485, filed 8 March 1993, issued 4 April 1995. Contextual canonical anchor only:
   <https://patents.google.com/patent/US5404485A/en>

### Contemporary technical / integration documentation

3. Wind River Systems, **VxWorks Programmer’s Guide 5.5**, Edition 2, `DOC-14617-ZD-01`, 5 March 2003, Flash Memory Block Device Driver chapter, especially printed pp. 340–344 and §8.13.5 `Fault Recovery in TrueFFS`. Current institutional mirror:
   <https://prex.jlab.org/wiki/images/8/86/Vxworks_programmers_guide5.5.pdf>

### Internal repository context

4. [`04-m-systems-2001-2003-interrupted-erase-recovery-deepening.md`](04-m-systems-2001-2003-interrupted-erase-recovery-deepening.md) — interrupted erase, retained completion evidence, and reuse authority.
5. [`42-kafka-081-cleaner-checkpoint-restart-currentness-deepening.md`](42-kafka-081-cleaner-checkpoint-restart-currentness-deepening.md) — persisted maintenance coordinate versus referent currentness.
6. [`152-sqlite-wal-recovery-backfill-progress-reset-deepening.md`](152-sqlite-wal-recovery-backfill-progress-reset-deepening.md) — discardable maintenance progress reconstructed from stronger retained recovery evidence.

---

## Bounded conclusion

The strongest source-controlled conclusion is not that `Flash writes are atomic`.

It is this:

```text
nonvolatile data bits
    are not enough

volatile RAM mapping table
    need not survive

what must survive is enough mapping/currentness evidence
    to decide or reconstruct which physical embodiment counts

and replacement must not destroy the old established state
    before the new candidate is completed and verified
```

For this documented TrueFFS regime, **logical continuity across power failure is produced by preserving reconstructible currentness evidence while allowing one runtime representation of that evidence to disappear**.

That is a stronger and more precise retention claim than either `Flash is nonvolatile` or `the mapping table persists`.