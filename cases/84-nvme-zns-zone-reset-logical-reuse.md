# NVMe Zoned Namespace Zone Reset: Retained Write Frontiers, Logical Deallocation, and Reuse Without Sanitization

## Status

**`grounded`** — bounded primarily to the NVM Express Zoned Namespace Command Set Specification Revision 1.1 (May 18, 2021), with the NVM Command Set deallocation semantics, a 2020 NVM Express ecosystem presentation, and the 2021 USENIX ATC ZNS paper used for interface context and prior-art boundaries.

Grounding record: [`../evidence/84-nvme-2020-2021-zns-zone-reset-grounding.md`](../evidence/84-nvme-2020-2021-zns-zone-reset-grounding.md).

## Scope

This case asks a deliberately narrow question:

> What state must remain current in a Zoned Namespace so the controller and host know **where the next sequential write is admissible**, and what exactly is forgotten when the host resets a zone for reuse?

The bounded mechanism is:

```text
zone begins Empty
      ↓
sequential writes advance a zone write pointer
      ↓
write pointer records the next admissible LBA frontier
      ↓
zone may become Open / Closed / Full
      ↓
Reset Zone
      ↓
zone returns to ZSE:Empty
write pointer returns to ZSLBA
logical blocks in the Empty zone are deallocated
      ↓
future writes may begin again at the zone start
```

This is **not**:

- a general history of zoned storage, SMR, ZBC/ZAC, Open-Channel SSDs, or ZNS adoption;
- a claim that NVMe invented zoned storage;
- a claim that `Reset Zone` is physically identical to one NAND block-erase pulse;
- a claim that `ZSE:Empty` proves every prior physical trace has disappeared;
- a secure-sanitization case — NVMe Sanitize is a separate interface operation already analyzed in Case 44;
- a complete treatment of zone persistence across power loss, controller reset, namespace format, or media failure;
- an FTL or garbage-collection history.

The project terms `write frontier`, `reuse authority`, and `logical forgetting for reuse` below are **engineering reconstructions**, not historical NVM Express vocabulary.

---

## Historical vocabulary

Revision 1.1 uses these terms directly:

- `zone`;
- `Zone Descriptor`;
- `Zone State`;
- `Write Pointer`;
- `Zone Start Logical Block Address (ZSLBA)`;
- `ZSE:Empty`;
- `ZSF:Full`;
- `Sequential Write Required`;
- `Zone Management Send`;
- `Reset Zone`;
- `Reset Zone Recommended`;
- `deallocated logical block`;
- `Sanitize`.

Do not silently replace these with project phrases such as `write frontier`, `forgetting`, `reuse certificate`, or `erase epoch`. Those can be useful reconstructions, but they are not the standard's historical terminology.

---

## Retained state

A ZNS namespace exposes several state classes that should not be collapsed.

### 1. User payload in logical blocks

The data written into LBAs remains the ordinary payload whose current logical availability matters to applications.

### 2. Zone state

The zone descriptor carries a state such as Empty, Open, Closed, or Full. This state constrains which management and write operations are currently admissible.

### 3. Zone write pointer

For a Sequential Write Required zone, the write pointer identifies the lowest-numbered logical block that has not yet been written in the current zone-writing cycle and therefore the next position at which an ordinary sequential write may begin.

The pointer is not the payload and is not a complete record of the writes that produced it.

### 4. Zone-management attributes

Revision 1.1 defines additional descriptor / recommendation state, including descriptor-extension validity and controller recommendation bits. A successful Reset Zone clears several of these alongside resetting the pointer.

### 5. Lower-layer physical/media state

The specification defines host-visible zoned semantics. It does not thereby expose every physical page, erase block, FTL structure, ECC state, or controller-internal relocation decision.

This boundary is central:

> **host-visible zone state is constitutive of interface currentness without being a complete forensic map of the medium.**

---

## Historical record

### H/P — ZNS exposes a per-zone write pointer as current control state

NVM Express Zoned Namespace Command Set Revision 1.1 defines the Write Pointer in the Zone Descriptor. For a Sequential Write Required zone, successful writes advance it. The host can retrieve the current pointer through Zone Management Receive.

The normative description gives the pointer a sharply bounded meaning: it identifies the lowest-numbered unwritten LBA in the current sequential-write progression.

That supports:

> **write pointer ≠ payload**

and:

> **write pointer ≠ complete write history**.

The pointer compresses one current ordering relation: where the next admissible write frontier stands. It does not tell the host every command, timestamp, retry, or physical program operation that happened earlier.

### H/P — Reset Zone rewinds the interface write frontier and changes zone state

Revision 1.1 specifies `Reset Zone` as a Zone Management Send action. A successful reset of an eligible zone transitions it to `ZSE:Empty` and sets its write pointer to the zone's `ZSLBA`.

The operation also clears several zone-descriptor / recommendation attributes, including the Zone Descriptor Extension Valid, Finish Zone Recommended, Reset Zone Recommended, and Zone Finished by Controller indicators under the bounded specification text. Variable Zone Capacity may also change as allowed by the specification.

Therefore:

> **Reset Zone ≠ pointer arithmetic alone**.

It is a coordinated zone-control transition that changes the write frontier, zone state, and associated management attributes.

### H/P — an Empty zone marks its logical blocks deallocated

Revision 1.1's allocation-management rules state that all logical blocks in a zone are marked deallocated when the zone is in `ZSE:Empty`.

The NVM Command Set's general deallocated/unwritten-block semantics are deliberately weaker than sanitization. Depending on negotiated feature behavior, later reads of a deallocated block may produce a deallocated/unwritten-block error or a deterministic conventional value; a later write returns the block to allocated/current use.

The safe cross-specification conclusion is:

> **ZSE:Empty establishes logical deallocation / reuse semantics, not a proof of secure physical erasure.**

The case does not infer a particular stale-page or raw-NAND outcome that the standard does not specify.

### H/P — Reset Zone and Sanitize are distinct standardized operations

The ZNS specification treats Sanitize separately from Zone Management Send / Reset Zone. It adds ZNS-specific rules for zone state and contents after a Sanitize operation, while the sanitize operation itself remains defined through the NVMe Base / NVM command-set framework.

That separation blocks a common over-reading:

> **Reset Zone ≠ Sanitize**.

Case 44 already establishes that NVMe sanitization has a stronger objective over prior user data than ordinary logical deallocation. Case 84 therefore does not re-litigate Sanitize; it uses that grounded case as a boundary condition for what Reset Zone does **not** prove.

### H/P — the controller may recommend a reset without owning the host's data decision

Revision 1.1 defines `Reset Zone Recommended`. The controller may set this before an internal operation for which resetting the zone would be beneficial. The specification warns that resetting the zone destroys host-visible data in that zone, so the host may choose not to issue the reset. If the host declines, the controller may proceed with its internal operation at a possible performance cost.

This exposes an unusually clean authority split:

```text
controller knows an internal maintenance/performance preference
        ↓
controller sets Reset Zone Recommended
        ↓
host decides whether prior zone contents may be logically discarded
        ↓
optional Reset Zone command
```

Thus:

> **maintenance recommendation ≠ authority to forget host data**.

And:

> **Reset Zone Recommended ≠ mandatory reset**.

The controller can surface a preference without silently turning that preference into host-level deletion authority.

---

## Write semantics — current frontier rather than complete history

For a Sequential Write Required zone, ordinary writes must respect the current zone write pointer. Random reads and sequential-write restrictions therefore coexist.

This matters because `addressable` is not one universal property. A zone can permit arbitrary read selection while constraining where the next ordinary write may begin.

> **random-read permission ≠ random-write permission**.

The write pointer is best reconstructed as a **current write frontier**. If the pointer is at LBA `N`, that does not mean the system has retained an append-only history proving exactly how all prior LBAs were written. It means the current interface state declares writes before that frontier non-admissible in the current sequential cycle unless the zone is reset through the specified management path.

This yields:

> **frontier retention ≠ history retention**.

The distinction is similar in form to other repository cases where a current counter, high-water mark, generation, or cursor summarizes an admissibility relation without retaining every event that generated it. That is a functional comparison only.

---

## Reset as logical forgetting for reuse

Reset Zone is especially useful for the repository because it joins two usually separated ideas:

1. the previous logical allocation/currentness relation is withdrawn;
2. future write authority is reopened from the beginning of the zone.

The operation does not `restore` the old payload. Instead, it makes the former zone contents no longer current at the logical interface and re-establishes a write frontier from `ZSLBA`.

A bounded engineering reconstruction is:

> **some technical forgetting is not an endpoint; it is the condition of controlled reuse.**

This is not philosophical vocabulary from NVM Express. It is a project-level way to compare zone reuse with mapped Flash reclamation, filesystem free-space reuse, cache replacement, and distributed retirement while preserving their different mechanisms.

The stronger relations are:

> **write-pointer reset ≠ physical-time rewind**

and:

> **reuse authority ≠ payload restoration**.

Resetting the current frontier does not undo the physical events that previously programmed media, nor does it recreate the discarded logical value.

---

## Interface geometry versus hidden media work

Bjørling et al., in the 2021 USENIX ATC paper on ZNS, describe the model as exposing flash erase-block boundaries and write-order constraints so host software can participate in data placement while the SSD continues to handle media reliability. Their broader architectural argument is that the conventional block-interface FTL tax can be reduced by shifting some data-management responsibility to the host.

That is valuable evidence for the division of responsibility, but it must not be over-literalized.

The paper's high-level statement that a zone must be erased between rewrites expresses the zoned-storage model. The normative ZNS interface text gives the host `Reset Zone`, zone-state transitions, write-pointer reset, and deallocation semantics. Neither source alone proves that a host Reset command maps one-to-one and synchronously onto a single raw NAND erase operation on every SSD implementation.

Therefore:

> **host-visible erase/rewrite geometry ≠ complete exposure of physical erase implementation**.

And:

> **host participation in placement ≠ host ownership of all media reliability work**.

ECC, bad-block management, read-disturb handling, retention error management, and other media-specific reliability mechanisms can remain inside the device even when write ordering and zone boundaries become visible.

---

## Failure and forgetting boundaries

Keep these states distinct:

- **zone payload remains current and the write pointer advances** — ordinary sequential use;
- **zone reaches Full** — no more ordinary sequential write capacity remains in that cycle;
- **controller recommends Reset** — maintenance/performance advice, not deletion authority;
- **host resets the zone** — explicit logical reuse transition;
- **zone becomes Empty** — zone state changes and logical blocks are deallocated;
- **write pointer returns to ZSLBA** — next-write frontier is reopened from the start;
- **old physical charge/patterns may or may not remain somewhere internally** — not established by Reset Zone semantics;
- **Sanitize succeeds** — a separate, stronger forgetting operation analyzed in Case 44;
- **new writes populate the reset zone** — new current payload replaces the logically discarded allocation relation;
- **physical medium eventually performs erase/GC/relocation/reliability work** — implementation detail unless independently sourced.

Calling all of these `erase` would hide the distinction among logical allocation, write admissibility, media operation, and secure sanitization.

---

## Cross-case comparison

### Case 13 — early Flash coarse erase

Case 13 grounds a physical/programming asymmetry: finer-grained programming/read coexist with a coarser erase operation in early Flash.

Case 84 is not a repetition of that device-level mechanism. ZNS exposes a host-visible zone write/reuse discipline whose boundaries may align with internal media-management geometry, while the exact physical implementation remains controller-specific.

Functional analogy only:

> **coarse rewrite preparation can couple neighbors while the layer at which that coupling is exposed changes.**

No direct technical genealogy is claimed.

### Case 04 — mapped Flash logical identity

Case 04 shows that logical currentness can change before stale physical embodiments are reclaimed. Case 84 supplies another interface-level instance: a reset zone becomes logically deallocated/Empty and eligible for a new writing cycle without that transition itself proving forensic media absence.

> **logical currentness transition ≠ physical trace proof**.

The mechanisms differ: Case 04 centers FTL-style virtual mapping and reclamation; Case 84 centers zone state plus sequential-write frontier.

### Case 44 — NVMe Deallocate and Sanitize

Case 44 is the direct boundary case.

- Case 44: ordinary Deallocate is weaker than Sanitize.
- Case 84: `Reset Zone` makes an entire zone Empty, marks its logical blocks deallocated, and reopens write admissibility from the beginning.

Therefore:

> **zone reset / deallocation ≠ sanitization**.

Case 84 adds reuse-frontier semantics rather than duplicating Case 44's sanitization analysis.

### Case 82 — NAND COPYBACK

COPYBACK shows that payload can move to a new physical embodiment without automatic controller-side ECC requalification. Zone Reset shows that logical reuse can be authorized without the interface proving one specific low-level erase history.

The functional commonality is methodological:

> **a visible high-level transition does not license an unsupported hidden-physical transformation claim**.

The historical mechanisms are unrelated unless separately demonstrated.

---

## Prior-art boundary

This case makes no invention-priority claim for zoned storage, sequential-write media, host-managed placement, or host/device cooperation.

Bjørling et al. explicitly situate the zoned-storage model before ZNS in shingled magnetic recording (SMR) HDDs. Their 2021 paper describes ZNS as adapting the model to flash-based SSDs, not inventing the abstract idea of zones.

NVM Express's 2020 ecosystem presentation likewise emphasizes compatibility with the earlier ZBC/ZAC host-managed model and presents Linux zoned-storage abstractions as spanning ZBC, ZAC, and ZNS.

The same USENIX paper discusses Streams SSDs and Open-Channel SSDs as earlier, distinct strategies for reducing the conventional FTL tax or moving some data-management responsibility toward host software.

Therefore:

> **ZNS ≠ invention of zoned storage**

and:

> **ZNS ≠ Open-Channel SSD historical identity**.

The safe historical claim is narrower:

> **By 2020–2021, NVM Express had standardized an SSD zoned-storage interface in which zone state and a write pointer govern sequential-write admissibility, explicit Reset Zone returns a zone to Empty and its write pointer to ZSLBA, Empty marks the zone's logical blocks deallocated, and Sanitize remains a separate operation.**

A full SMR/ZBC/ZAC → ZNS genealogy belongs primarily in `computing-archaeology` if developed later.

---

## Engineering reconstruction

The bounded evidence supports these project-level distinctions:

1. `zone write pointer ≠ payload`;
2. `write-pointer frontier ≠ complete write history`;
3. `random-read permission ≠ random-write permission`;
4. `Reset Zone ≠ ordinary overwrite`;
5. `write-pointer reset ≠ physical-time rewind`;
6. `ZSE:Empty ≠ proof of physical blankness`;
7. `logical deallocation ≠ secure sanitization`;
8. `zone reuse authority ≠ payload restoration`;
9. `zone state ≠ allocation state ≠ write-pointer state`, even when one command changes all three coherently;
10. `Reset Zone ≠ pointer update alone`;
11. `Reset Zone Recommended ≠ mandatory reset`;
12. `controller maintenance recommendation ≠ host authority to forget data`;
13. `host-visible rewrite geometry ≠ complete physical implementation exposure`;
14. `host placement responsibility ≠ ownership of all media reliability`;
15. `ZNS ≠ invention of zoned storage`;
16. `logical forgetting can enable future write admissibility`.

These are engineering / comparative formulations. They are not claims that the standard authors used this exact ontology.

---

## Philosophical interpretation — bounded

Case 84 gives the repository a compact instance of **forgetting as a condition of renewed technical availability**.

The zone's previous contents do not need to vanish from every possible physical witness before the interface can withdraw their current allocation status and make the address range available for a new sequential writing cycle. In that limited engineering sense, forgetting is not simply destruction. It can be a change in **which state still counts** and **what future action is now permitted**.

That observation can discipline philosophical discussion of availability, erasure, and technical temporality, but it does not establish a Heideggerian, Stieglerian, or Kirschenbaum-style conclusion by itself. The mechanism remains the evidence-bearing core:

```text
past writes occurred
    ≠
complete past history retained

current write pointer retained
    ->
next admissible action known

zone reset
    ->
previous logical allocation withdrawn
    ->
future write frontier reopened
```

The analogy stops at the engineering relation. `Reset Zone` is not a philosophical theory of forgetting.

---

## Rejected / unsupported claims

Do **not** claim:

- NVMe ZNS invented zoned storage;
- `Reset Zone` is necessarily one synchronous physical NAND erase;
- `ZSE:Empty` proves the entire underlying medium is physically blank;
- Zone Reset is equivalent to NVMe Sanitize;
- a write pointer is a durable complete log of past writes;
- controller recommendation implies authority to destroy host data;
- ZNS removes all SSD firmware, FTL-like metadata, ECC, bad-block management, or reliability work;
- ZNS and Open-Channel SSDs are the same historical mechanism;
- the bounded sources establish every reset/power-loss persistence rule for zone metadata;
- resetting a zone restores its old payload;
- deallocation proves forensic unrecoverability.

---

## Related-repository check

Searches of `tmzncty/computing-archaeology` for `ZNS`, `zoned namespace`, `NVMe zone reset`, and related terms returned no dedicated ZNS case at the time of this slice.

Therefore this case does not duplicate a companion-repository history. It deliberately leaves the following broader work to `computing-archaeology` if pursued:

- SMR / ZBC / ZAC → ZNS standards chronology;
- Open-Channel SSD and Streams lineage;
- concrete SSD internal mapping/erase geometry under ZNS;
- named-controller performance and media-management implementation;
- Linux zoned-block implementation history.

`technical-retention` keeps only the retention-specific decomposition of **current zone state + write frontier + logical deallocation + reuse authority**.

---

## Sources

### Primary / institutional

- NVM Express, **NVM Express Zoned Namespace Command Set Specification, Revision 1.1**, May 18, 2021. Relevant areas: zone terminology and descriptors; write-pointer semantics; allocation management; Zone Management Send / `Reset Zone`; `Reset Zone Recommended`; ZNS-specific Sanitize behavior.  
  <https://nvmexpress.org/wp-content/uploads/NVM-Express-Zoned-Namespace-Command-Set-Specification-1.1-2021.06.02-Ratified.pdf>

- NVM Express, **NVM Express NVM Command Set Specification, Revision 1.0a**, 2021. Relevant area: deallocated / unwritten logical-block read and rewrite semantics.  
  <https://nvmexpress.org/wp-content/uploads/NVMe-NVM-Command-Set-Specification-1.0a-2021.07.26-Ratified.pdf>

- NVM Express, **“NVMe Zoned Namespace SSDs: The Zoned Storage Linux Software Ecosystem,”** 2020. Institutional ecosystem witness for ZBC/ZAC compatibility and host-managed zoned abstractions.  
  <https://nvmexpress.org/wp-content/uploads/NVMe_Zoned_Namespace_SSDs_The_Zoned_Storage_Linux_Software_Ecosystem.pdf>

### Scholarly / systems

- Matias Bjørling et al., **“ZNS: Avoiding the Block Interface Tax for Flash-based SSDs,”** *USENIX Annual Technical Conference*, 2021. Use here for architectural responsibility boundaries and prior-art context, not to override normative specification semantics.  
  <https://www.usenix.org/conference/atc21/presentation/bjorling>

---

## Current maturity

**`grounded`**.

The central claims no longer depend on a single tertiary explanation: the normative NVM Express specifications establish the write-pointer / Empty / deallocation / Reset / Sanitize boundaries, while NVM Express institutional material and the USENIX paper independently bound the historical relationship to earlier zoned-storage and host-managed models.

Future work is intentionally narrower:

- direct archival recovery of the earliest ratified ZNS 1.0 text and change history;
- exact ZBC/ZAC → ZNS standards genealogy;
- named-controller fault/forensic tests distinguishing reset, media erase, and sanitize;
- power-loss/reset persistence archaeology for zone metadata;
- concrete physical erase/mapping behavior in a specific ZNS SSD.
