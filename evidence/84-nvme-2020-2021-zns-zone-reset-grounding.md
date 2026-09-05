# Case 84 grounding — NVMe ZNS write pointer, Zone Reset, logical deallocation, and reuse (2020–2021)

## Purpose

Ground the bounded Case 84 claim that an NVMe Zoned Namespace retains **zone-control state** beyond user payload: a per-zone write pointer and zone state determine the next admissible sequential write position, while an explicit `Reset Zone` returns the zone to `ZSE:Empty`, rewinds the pointer to `ZSLBA`, and marks the zone's logical blocks deallocated without thereby establishing secure media sanitization.

This record separates:

- **historical record** — what NVM Express sources and contemporary systems literature actually specify or describe;
- **engineering reconstruction** — `write frontier`, `reuse authority`, and `logical forgetting for reuse`;
- **functional analogy** — comparisons to mapped Flash, coarse erase, and other currentness/frontier cases;
- **philosophical interpretation** — the limited claim that forgetting can reopen future technical action.

It makes no invention-priority claim for zones, sequential-write storage, host-managed placement, deallocation, or sanitization.

---

## Source set and evidence grade

| Source | Date / version | Type | Use here | Grade |
| --- | --- | --- | --- | --- |
| NVM Express, *Zoned Namespace Command Set Specification* | Rev. 1.1, 18 May 2021 | normative industry specification | write pointer, zone state, Empty/deallocation relation, Reset Zone, reset recommendation, ZNS-specific sanitize behavior | **H/P** |
| NVM Express, *NVM Command Set Specification* | Rev. 1.0a, 2021 | normative industry specification | general semantics of deallocated / unwritten logical blocks | **H/P** |
| NVM Express, *NVMe Zoned Namespace SSDs: The Zoned Storage Linux Software Ecosystem* | 2020 | institutional/contemporary presentation | ZBC/ZAC compatibility boundary; zoned-storage host model; SSD/NAND motivation | **H/P** |
| Bjørling et al., *ZNS: Avoiding the Block Interface Tax for Flash-based SSDs*, USENIX ATC | 2021 | peer-reviewed systems paper | host/device responsibility boundary; prior zoned-storage and Open-Channel/Streams context | **P/S** |
| `technical-retention` Case 04 | current repo | grounded internal case | functional comparison to mapped Flash currentness and stale embodiment | **A/E** |
| `technical-retention` Case 13 | current repo | grounded internal case | functional comparison to coarse erase geometry | **A** |
| `technical-retention` Case 44 | current repo | grounded internal case | direct semantic boundary: deallocation is weaker than sanitization | **E/A** |
| `technical-retention` Case 82 | current repo | grounded internal case | methodological comparison: visible operation does not prove unsupported hidden physical transformation | **A** |

`P` here means primary or contemporary evidence under repository convention; it does not mean every source is a peer-reviewed publication.

---

## Source anchor A — NVM Express Zoned Namespace Command Set Revision 1.1

Primary source:
<https://nvmexpress.org/wp-content/uploads/NVM-Express-Zoned-Namespace-Command-Set-Specification-1.1-2021.06.02-Ratified.pdf>

Revision header: **Revision 1.1, May 18, 2021**.

### A1. Zone descriptor / write-pointer semantics

Relevant specification area: zone terminology and Zone Descriptor / Write Pointer definitions.

Grounded observations:

1. A zone is a contiguous range of logical block addresses governed by zone-management state.
2. Sequential Write Required zones expose a current `Write Pointer`.
3. The host can obtain the current write pointer using Zone Management Receive.
4. Successful sequential writes advance the pointer.
5. The pointer identifies the next unwritten / next admissible logical-block location in the current zone-writing progression.

Supported historical claim:

> The ZNS interface retains a per-zone current write-position relation in addition to user payload.

Engineering reconstruction:

> `write pointer` can be treated as a **write frontier** because it summarizes where the next ordinary sequential write is admissible.

Boundary:

> Nothing in this definition makes the pointer a complete log of all prior write commands or physical program operations.

Therefore:

- `zone write pointer ≠ payload`;
- `write-pointer frontier ≠ complete write history`.

### A2. Reset Zone action

Relevant specification area: Zone Management Send, `Reset Zone` action.

Grounded observations:

1. Reset Zone applies to eligible open, closed, or full zones under the specified state-transition rules.
2. On successful reset, the zone transitions to `ZSE:Empty`.
3. Its write pointer is set to `ZSLBA`, the zone-start logical block address.
4. Reset also clears several zone-management attributes, including descriptor-extension validity and reset/finish recommendation state under the bounded revision.
5. Variable Zone Capacity may be updated as allowed by the specification.

Supported claim:

> Reset Zone is a coordinated zone-control transition, not merely host-side arithmetic on an LBA counter.

Therefore:

- `Reset Zone ≠ ordinary overwrite`;
- `Reset Zone ≠ pointer update alone`;
- `write-pointer reset ≠ physical-time rewind`.

The last relation is engineering reconstruction: returning a current pointer to the beginning does not reverse the historical physical events that produced prior media states.

### A3. Empty-zone allocation semantics

Relevant specification area: allocation management / `ZSE:Empty` semantics.

Grounded observation:

> All logical blocks in a zone are marked deallocated when the zone is in `ZSE:Empty`.

This directly connects zone reset to a host-visible forgetting/currentness relation: successful reset produces Empty, and Empty carries deallocated logical-block semantics.

Supported claim:

> `Reset Zone` can withdraw the previous zone allocation/currentness relation and reopen the zone for a new sequential-write cycle.

Unsupported strengthening:

> Empty proves every stale NAND page or physical media trace has been erased.

The specification defines the logical/interface state, not a forensic audit of hidden embodiments.

### A4. Reset Zone Recommended

Relevant specification area: `Reset Zone Recommended` zone attribute / controller recommendation.

Grounded observations:

1. A controller may recommend a zone reset before an internal operation.
2. Resetting the zone destroys the host-visible data currently associated with that zone.
3. The host is not forced to comply with the recommendation.
4. If the host does not reset, the controller may still perform its internal operation with a potential performance impact.

Supported claims:

- `Reset Zone Recommended ≠ mandatory reset`;
- `controller maintenance recommendation ≠ host authority to forget data`.

This is strong evidence that maintenance knowledge and data-destruction authority can be separated across the host/controller boundary.

### A5. Sanitize remains a separate operation

Relevant specification area: ZNS additions to Sanitize behavior.

Grounded observation:

> The ZNS specification separately defines how zones and zone contents behave in relation to an NVMe Sanitize operation; Sanitize is not specified as an alias for `Reset Zone`.

Supported claim:

- `Reset Zone ≠ Sanitize`.

Case 44 supplies the deeper internal repository grounding for why deallocation and sanitization should remain distinct.

---

## Source anchor B — NVM Express NVM Command Set Revision 1.0a

Primary source:
<https://nvmexpress.org/wp-content/uploads/NVMe-NVM-Command-Set-Specification-1.0a-2021.07.26-Ratified.pdf>

Relevant area: **deallocated / unwritten logical block** semantics.

Grounded observations:

1. A logical block can be in a deallocated/unwritten state distinct from ordinary allocated current data.
2. Depending on controller feature configuration and command-set semantics, a read can return a deallocated/unwritten-block error or a deterministic conventional value.
3. A subsequent write removes the deallocated status for that logical block.
4. Read or verify does not itself reallocate the block.

Evidence consequence for Case 84:

> The fact that ZNS `ZSE:Empty` marks a zone's logical blocks deallocated establishes an interface currentness/allocation transition; it does not establish a secure-media-erasure contract.

This also supports:

- `logical deallocation ≠ physical blankness proof`;
- `zone reuse authority ≠ payload restoration`.

Do not infer a specific hidden stale-page result from the allowed host read behavior alone.

---

## Source anchor C — NVM Express 2020 ZNS ecosystem presentation

Primary/institutional source:
<https://nvmexpress.org/wp-content/uploads/NVMe_Zoned_Namespace_SSDs_The_Zoned_Storage_Linux_Software_Ecosystem.pdf>

Relevant presentation material:

- ZNS uses a zoned-block interface for NVMe SSDs;
- Linux zoned-storage abstractions are presented across ZBC, ZAC, and ZNS;
- the model exposes media-related sequential-write constraints / zones to host software;
- the presentation motivates ZNS partly by aligning host data placement with SSD/NAND organization and reducing unnecessary device-internal data movement / garbage collection.

Prior-art consequence:

> ZNS is presented in an ecosystem that already includes ZBC/ZAC zoned-storage interfaces; it is not defensible to claim that NVMe ZNS invented the abstract zoned-storage model.

Boundary:

> Compatibility and shared host abstractions do not by themselves prove a complete standards genealogy or implementation identity among ZBC, ZAC, and ZNS.

---

## Source anchor D — Bjørling et al., USENIX ATC 2021

Source:

Matias Bjørling et al., **“ZNS: Avoiding the Block Interface Tax for Flash-based SSDs,”** *2021 USENIX Annual Technical Conference*.

Landing page:
<https://www.usenix.org/conference/atc21/presentation/bjorling>

Paper:
<https://www.usenix.org/system/files/atc21-bjorling.pdf>

### D1. Host/device responsibility boundary

The paper's architectural argument is that conventional block-interface SSDs hide flash erase-block constraints behind a large FTL responsibility. ZNS exposes zone boundaries and write ordering so host software can participate in placement, while the SSD remains responsible for media reliability.

Supported engineering boundary:

> **host-visible write/erase geometry ≠ complete transfer of physical-media responsibility to the host**.

Do not infer that ZNS removes ECC, bad-block management, retention-error handling, or all controller metadata.

### D2. Random reads with sequential writes

The paper describes ZNS zones as allowing random reads while constraining writes sequentially according to the zone's write position.

Supported claim:

- `random-read permission ≠ random-write permission`.

This matters for the repository's addressability vocabulary: read addressability and write admissibility can differ even over the same LBA range.

### D3. Prior zoned-storage model

The paper explicitly situates the zoned-storage model first in shingled magnetic recording HDDs and then discusses adaptation to flash-based SSDs.

Prior-art boundary:

- `ZNS ≠ invention of zoned storage`.

### D4. Other host/device cooperation precedents

The paper discusses earlier approaches such as Streams SSDs and Open-Channel SSDs.

Prior-art boundary:

- `ZNS ≠ Open-Channel SSD historical identity`;
- earlier host/device cooperation strategies do not make all such interfaces technically identical.

### D5. High-level “erase between rewrites” language must stay at the model layer

The paper describes a zone as requiring reset/erase preparation before a new rewrite cycle. This is useful architectural evidence, but it should not override the normative interface boundary.

Safe statement:

> ZNS exposes a reset/reuse abstraction aligned with flash-management geometry.

Unsafe strengthening:

> Every Zone Reset command is one synchronous raw NAND erase with a one-zone-to-one-erase-block physical mapping.

That implementation claim would require named-controller/device evidence.

---

## Claim ledger

| Claim | Label | Evidence | Boundary |
| --- | --- | --- | --- |
| ZNS retains a per-zone Write Pointer | H/P | ZNS 1.1 | interface state, not payload |
| successful writes advance the pointer | H/P | ZNS 1.1 | sequential-write regime only |
| write pointer identifies the next write position | H/P + E | ZNS 1.1 | project term `write frontier` is reconstruction |
| write pointer is not a complete historical log | E/X | semantics of current pointer | no claim that all implementations persist it identically |
| Reset Zone returns eligible zone to Empty | H/P | ZNS 1.1 | state rules are revision-specific |
| Reset Zone returns pointer to ZSLBA | H/P | ZNS 1.1 | not a physical-time reversal |
| Reset clears additional descriptor/recommendation state | H/P | ZNS 1.1 | exact bit set is revision-specific |
| Empty means logical blocks in zone are deallocated | H/P | ZNS 1.1 | not secure-erasure proof |
| deallocated state is distinct from secure sanitization | H/P + E | NVM 1.0a + Case 44 | no forensic implementation claim |
| Sanitize is a separate operation from Reset Zone | H/P | ZNS 1.1 + Case 44 | do not equate scopes/results |
| controller can recommend reset without forcing host to discard data | H/P | ZNS 1.1 | bounded to recommendation semantics |
| ZNS can allow random read while constraining writes sequentially | H/P | ZNS 1.1 / USENIX 2021 | not every zone type/command path generalized |
| host sees more placement/write geometry while device keeps media reliability duties | H/P + E | USENIX 2021 | not proof of exact internal firmware structure |
| zoned storage predates ZNS in SMR/ZBC/ZAC ecosystem | H/P + S | NVM Express 2020 + USENIX 2021 | complete genealogy remains open |
| Open-Channel SSD is prior adjacent work, not identical to ZNS | H/P + A | USENIX 2021 | no direct genealogy claim |
| zone reset can be reconstructed as logical forgetting that enables reuse | E/I | Reset→Empty→deallocated→write pointer at ZSLBA | project interpretation, not NVM Express terminology |

---

## Engineering reconstruction

The evidence supports these controlled project relations:

1. `zone write pointer ≠ payload`;
2. `write-pointer frontier ≠ complete write history`;
3. `random-read permission ≠ random-write permission`;
4. `Reset Zone ≠ ordinary overwrite`;
5. `write-pointer reset ≠ physical-time rewind`;
6. `ZSE:Empty ≠ physical blankness proof`;
7. `logical deallocation ≠ secure sanitization`;
8. `zone reuse authority ≠ payload restoration`;
9. `zone state ≠ allocation state ≠ write-pointer state`;
10. `Reset Zone ≠ pointer update alone`;
11. `Reset Zone Recommended ≠ mandatory reset`;
12. `controller reset recommendation ≠ sanitization request`;
13. `host-visible write/erase geometry ≠ complete physical implementation exposure`;
14. `host placement responsibility ≠ ownership of all media reliability`;
15. `ZNS ≠ invention of zoned storage`;
16. `logical forgetting can enable future write admissibility`.

The central contribution is #2 + #7 + #16: **a retained current frontier can govern future action without preserving complete past history, and resetting that frontier can logically forget an old allocation state in order to authorize controlled reuse without amounting to secure sanitization.**

---

## Cross-case boundary

### Case 04 — mapped Flash

Shared function:

- current logical state can diverge from stale physical embodiment;
- future reuse depends on retained mapping/allocation/control state.

Different mechanism:

- Case 04 centers logical-to-physical mapping and reclamation;
- Case 84 centers exposed zone state, write pointer, and explicit reset.

No genealogy claim.

### Case 13 — early Flash coarse erase

Shared functional issue:

- rewriting is constrained by an erase/rewrite geometry broader than an individual byte-like update.

Different evidence layer:

- Case 13 is cell/device-era erase geometry;
- Case 84 is a modern host-visible zoned command-set relation.

Do not project `Reset Zone` backward into early Flash vocabulary.

### Case 44 — Deallocate and Sanitize

This is the strongest direct boundary:

> `Reset Zone -> Empty -> logical blocks deallocated`

is **not** equivalent to:

> `Sanitize -> stronger subsystem-level prior-user-data inaccessibility contract`.

Case 84 should therefore never use `secure erase` as a synonym for zone reset.

### Case 82 — COPYBACK

The functional comparison is methodological only: both cases warn against inferring hidden physical transformation from an interface/operation label.

- COPYBACK relocation does not automatically imply integrity requalification.
- Zone Reset does not automatically imply secure physical sanitization.

No technical lineage is claimed.

---

## Philosophical interpretation boundary

The engineering relation allows one bounded conceptual observation:

> A system may have to forget one **currentness/admissibility relation** in order to make future inscription possible.

That does not mean the physical past is erased, nor that the system preserves a historical narrative of the old zone. The retained write pointer exists to coordinate current/future action; resetting it discards the previous allocation frontier and opens another cycle.

Label this **I/E**, not H:

- it is not NVM Express's philosophical language;
- it does not prove a universal theory of technical forgetting;
- it should not be converted automatically into `Bestand`, `tertiary retention`, or forensic-materiality vocabulary.

---

## Related-repository check

Searches of `tmzncty/computing-archaeology` for:

- `ZNS`;
- `zoned namespace`;
- `NVMe zone reset`;
- `zoned storage`;

returned no dedicated technical-history case at the time of this slice.

Therefore no companion history is duplicated here. A future historical engineering treatment should go there first if it covers:

- SMR and host-managed HDD zones;
- ZBC / ZAC standardization;
- ZNS 1.0/1.1 chronology;
- Open-Channel SSD and Streams predecessor/adjacent designs;
- named ZNS SSD implementation and Linux support history.

Case 84 remains only the retention-specific decomposition.

---

## Rejected / unsupported claims

Do **not** claim:

- ZNS invented zoned storage;
- ZNS and ZBC/ZAC are implementation-identical;
- ZNS and Open-Channel SSD are the same system;
- `Reset Zone` necessarily maps one-to-one to a physical NAND erase block;
- `Reset Zone` proves stale physical data is unrecoverable;
- `ZSE:Empty` means the underlying NAND is physically blank;
- `Reset Zone` equals NVMe Sanitize;
- the write pointer is a complete write history;
- a reset recommendation authorizes the controller to discard host data without host action;
- ZNS removes all device firmware, ECC, FTL-like metadata, wear handling, or bad-block management;
- the bounded 2021 source establishes every later ZNS revision's semantics;
- zone reset restores previous payload;
- deallocation is forensic sanitization.

---

## Evidence strength

**Strong for the bounded interface claims.**

The primary normative specification directly grounds:

- write-pointer semantics;
- Reset Zone state transition;
- return of the pointer to ZSLBA;
- Empty-zone logical deallocation;
- reset recommendation semantics;
- the separation of Sanitize from Reset Zone.

The contemporary NVM Express presentation and peer-reviewed USENIX paper independently ground the host/device responsibility and prior-art boundaries.

Still open:

- exact earliest ZNS 1.0 wording and change history;
- full ZBC/ZAC→ZNS genealogy;
- power-loss persistence details for zone metadata in named devices;
- raw-media behavior after reset in specific SSDs;
- forensic comparison of Reset Zone, block erase, Format, Crypto Erase, and Sanitize on named controllers;
- physical mapping between logical zones and NAND erase units in real products.

These gaps do not block the bounded `grounded` status because Case 84 does not make those stronger claims.
