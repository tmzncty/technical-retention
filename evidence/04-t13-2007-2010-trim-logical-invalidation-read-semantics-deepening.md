# Case 04 Deepening — T13 TRIM, Logical Invalidation, and Read-After-Invalidation Semantics (2007–2010)

**Status:** `bounded deepening complete`

**Supports:** [`../cases/04-flash-virtual-mapping-logical-identity.md`](../cases/04-flash-virtual-mapping-logical-identity.md)

## Purpose

Case 04 already establishes a 1993–1995 M-Systems relation in which a stable virtual identity can continue to name current data while the physical Flash block that embodies that identity changes. It also establishes, inside that bounded system, that an old block may lose logical currentness before the larger erase unit is physically reclaimed.

This record asks a later and different question:

> once the host knows that a logical range no longer contains data it needs to preserve, how does that information cross the storage interface, and what does the interface promise about reads after that logical invalidation?

The bounded historical center is the T13 proposal sequence that introduced ATA `DATA SET MANAGEMENT` / `Trim` and then refined read-after-Trim behavior between 2007 and 2010.

The result is useful for `technical-retention` because it separates four events that are easy to collapse:

```text
host decides old content is no longer needed
    !=
that fact reaches the device
    !=
host-visible read semantics after notification
    !=
physical media reclamation / sanitization
```

This is **later boundary evidence** for Case 04. It is not projected backward into Amir Ban's 1993 patent, and it is not a general history of SATA, SSD firmware, garbage collection, secure erase, SCSI UNMAP, or NVMe deallocation.

---

## Source custody and chronology

### A — T13 document index for the original proposal family

**Source:** Technical Committee T13 AT Attachment, document index.

Official index: <https://t13.org/docsearch>

The index records the following public proposal sequence by Frank Shu (Microsoft):

- `e07154r0`, **Notification for Deleted Data Proposal for ATA-ACS2**, submitted 23 April 2007;
- `e07154r1` through `e07154r5`, retitled **Data Set Management Proposal for ATA-ACS2**, August–November 2007;
- `e07154r6`, **Data Set Management Proposal for ATA-ACS2**, submitted 10 January 2008.

The surviving revision-6 document itself is dated December 2007. The committee index submission date and the document's internal revision date are therefore kept distinct rather than silently normalized into one date.

**Evidence class:** H/P — standards-committee primary metadata.

### B — T13/e07154r6, Data Set Management Commands Proposal for ATA8-ACS2

**Source:** Frank Shu, `T13/e07154r6`, *Data Set Management Commands Proposal for ATA8-ACS2*, revision 6, December 2007 / T13 submission 10 January 2008.

A public mirror of the surviving proposal is available at:

<https://www.sgv417.jp/~makopi/blog/wp-content/uploads/2018/05/e07154r6-Data-Set-Management-Proposal-for-ATA-ACS2.pdf>

The T13 index above supplies committee custody for the document number/title/author/submission date. The mirrored PDF is used for body text because the current T13 site did not reliably return the old file body during this pass.

The proposal says that file deletion happens in the filesystem while information about deleted files is kept by the OS rather than the device. Consequently, the device treats valid and invalid/deleted data alike and continues applying operations needed to keep data alive. The proposal explicitly gives SSD examples including **merge, wear leveling and erase**.

It then proposes `DATA SET MANAGEMENT` as a host-to-device abstraction and says that, since revision 3, the proposal focuses first on the `Trim` attribute.

**Evidence class:** H/P — contemporary standards proposal body, with source-custody limitation recorded above.

### C — T13/e08137r4, Deterministic TRIM Proposal for ATA8-ACS2

**Source:** Fred Knight / Curtis E. Stevens, `T13/e08137r4`, *Deterministic TRIM Proposal for ATA8-ACS2*, 17 December 2008.

Public copy inspected:

<https://pcper.com/wp-content/uploads/2009/04/b2e2-e08137r4-drat-deterministic-read-after-trim.pdf>

T13's official index records the `e08137` proposal family beginning in October 2008 under the title **DRAT - Deterministic Read After Trim**.

The revision-4 proposal explicitly says that `e07154r6` added `DATA SET MANAGEMENT` and `TRIM`, and that the earlier proposal created non-deterministic read behavior. It introduces a capability bit to distinguish deterministic from non-deterministic read-after-Trim behavior.

Its proposed semantics include:

- if deterministic behavior is advertised, after a trimmed LBA has been read, reads to that logical block return the same data until a later successful write to that logical block;
- if deterministic behavior is not advertised, data read after Trim are indeterminate;
- data read from a trimmed LBA must not be obtained from application-client data previously addressed to **another** LBA;
- after the trimmed LBA is successfully written, the logical block again contains determinate written data.

**Evidence class:** H/P — contemporary standards proposal.

### D — T13/e09117, Read Zero after Trim

**Source:** Fred Knight, `T13/e09117r1`, *Read zero after TRIM Proposal for ATA8-ACS2*, revision dated June 2009.

T13's official index records:

- `e09117r0`, **Read Zero after Trim**, submitted 13 April 2009;
- `e09117r1`, **Read Zero after Trim**, submitted 16 June 2009.

Public copy inspected:

<https://www.sgv417.jp/~makopi/blog/wp-content/uploads/2018/05/e09117r1-Read-Zero-after-Trim.pdf>

The proposal says host systems have use cases in which reads after Trim return all-zero data, notes the analogous identification need for SCSI/SAT translation, and proposes a capability identifying this behavior.

The proposed text retains the earlier distinction between determinate and indeterminate post-Trim reads, while adding a determinate subcase in which read data are all words cleared to zero.

**Evidence class:** H/P — contemporary standards proposal.

### E — T13/e09158, Trim Clarifications

**Source:** T13 document index for Fred Knight's `e09158` family, **Trim Clarifications**.

The official index records:

- `e09158r0`, submitted 14 December 2009;
- `e09158r1`, submitted 14 December 2009;
- `e09158r2`, submitted 22 February 2010.

The proposal family is useful as chronology showing that DRAT / read-zero behavior continued to be consolidated and clarified during ACS-2 work. The old committee PDF body did not render reliably through the current T13 site in this pass, so this record does not pretend to have inspected every final editorial change in `e09158r2`.

A contemporary 2010 academic paper by Graeme B. Bell and Richard Boddington cites `e09158r2` as **TRIM – DRAT / RZAT clarifications for ATA8-ACS2 (Draft)**, providing independent contemporary bibliographic corroboration:

<https://commons.erau.edu/jdfsl/vol5/iss3/1/>

**Evidence class:** H/P for T13 index metadata; H/S for the contemporary academic bibliographic corroboration.

---

## Historical record

### H/P — the original problem is a missing validity relation between filesystem and device

The most important historical statement in `e07154r6` is not that SSDs have an erase cost. That is already well known elsewhere in Case 04.

The proposal identifies a **knowledge boundary**:

```text
filesystem / OS knows
    which data have become invalid because a file was deleted

storage device does not know
    unless that information crosses the interface
```

The device therefore continues treating both sets as if they require preservation.

In the proposal's SSD example, that means maintenance such as merge, wear leveling, and erase may continue to account for data the host has already declared unnecessary.

This is direct historical evidence that retention can be wasteful when the component performing maintenance lacks the authority/knowledge needed to distinguish current from no-longer-needed data.

### H/P — `Trim` is introduced as an attribute of DATA SET MANAGEMENT, not as a synonym for physical erase

The proposal describes `DATA SET MANAGEMENT` as a way for the host to communicate filesystem information for device optimization. Revision 6 focuses on the `Trim` attribute.

That vocabulary matters. The period proposal is about conveying information about logical block ranges to the device. It does not define Trim as a host command that must synchronously erase a corresponding set of NAND cells before command completion.

The safe historical statement is therefore:

```text
Trim notification
    = host-to-device statement about logical data being no longer required

Trim notification
    != proof of immediate physical erase
```

The second line is a boundary on what the inspected proposal establishes, not an empirical claim that every trimmed device necessarily keeps stale cell contents for some interval.

### H/P — the original proposal left read-after-Trim behavior non-deterministic

The 2008 DRAT proposal states this directly: `e07154r6` added the command/function, and the resulting read-after-Trim behavior was non-deterministic.

The historical sequence therefore includes a standards-level realization that **withdrawal of the obligation to preserve old content leaves a separate question: what should a later read return?**

That question mattered enough for T13/T10/SAT interoperability that a separate proposal was written to expose deterministic versus non-deterministic behavior.

### H/P — deterministic post-Trim behavior does not mean preservation of the pre-Trim payload

In `e08137r4`, deterministic behavior means that, after the trimmed LBA has been read, later reads to that logical block return the same data until a successful write changes the block again.

The proposal does **not** say that the stable value must be the payload that existed before Trim.

That yields an important historical boundary:

```text
deterministic read after Trim
    !=
old payload retained as logically current
```

The word `deterministic` here concerns repeatability of the host-visible read result under the proposed rule, not historical continuity of the invalidated content.

### H/P — non-deterministic and deterministic post-Trim behavior were both contemplated

The 2008 proposal exposes both behaviors as device properties:

```text
TRIM supported + deterministic bit clear
    -> post-Trim read data may be indeterminate

TRIM supported + deterministic bit set
    -> post-Trim read behavior follows the determinate rule
```

This is valuable for retention analysis because it shows the same logical address can continue to exist in the address space while the interface deliberately weakens or changes the promise attached to the old payload.

### H/P — `Read Zero after Trim` is a further contract, not evidence that the NAND cells are physically zero

The 2009 `e09117` proposal introduces a way to identify devices that return zero data after Trim.

That produces three separable layers:

```text
logical block has been trimmed
    ↓
read-after-Trim behavior advertised by interface
    ↓
possible host-visible zero result
```

Nothing in that sequence, by itself, proves that every underlying physical cell previously associated with the LBA has been erased to a physical zero representation.

`Read zero after Trim` is therefore a **read contract**, not a direct microscope on the NAND array.

### H/P — later successful write re-establishes a determinate logical payload

Both the 2008 DRAT proposal and the 2009 read-zero proposal preserve a clear transition back into ordinary logical currentness: after a subsequent successful write to the trimmed LBA, the logical block becomes determinate with the written data.

The bounded relation is:

```text
old logical payload current
    ↓ Trim
old payload no longer required to remain the logical result
    ↓ post-Trim read contract applies
later successful write
    ↓
new written payload is determinate/current at that LBA
```

This is a logical/interface transition. It should not be rewritten as a claim about exact internal FTL page allocation or erase scheduling.

---

## Engineering reconstruction

### E — Trim transfers discardability information across an abstraction boundary

A useful project-level reconstruction is:

```text
filesystem knows a range is no longer semantically live
        ↓
without notification:
device must conservatively preserve/treat it like live data
        ↓
with Trim:
discardability crosses the interface
        ↓
device may stop spending the same retention/maintenance effort on that old logical content
```

`Discardability` is project vocabulary here. The T13 proposal uses `Trim`, `invalid data`, `deleted file`, and Data Set Management vocabulary.

The key point is that the interface conveys **permission/knowledge about what no longer needs continuity**.

### E — logical address continuity and payload continuity can be separated

The LBA namespace remains usable after Trim. Yet the old payload can lose the interface's continuity guarantee.

Thus:

```text
address remains valid
    !=
pre-Trim payload remains current
```

Case 04 already shows that logical identity need not equal physical location. TRIM adds a different separation: logical addressability need not imply continuity of the previous logical payload.

### E — invalidation, read semantics, and physical reclaim are separate state transitions

The proposal sequence supports a clean engineering decomposition:

1. **host semantic invalidation** — the host decides old data are no longer needed;
2. **device notification** — Trim communicates that fact for specified logical blocks;
3. **read contract** — device capabilities determine what post-Trim reads promise;
4. **internal reclamation** — controller/medium may later use the new information in maintenance;
5. **republication** — a later successful write establishes new current data at the LBA.

Conflating these stages causes several bad inferences:

```text
file deleted
    != Trim necessarily issued

Trim issued
    != immediate physical erase proven

read returns zero
    != physical cell state proven zero

old content no longer current
    != secure sanitization completed
```

### E — a weaker retention obligation can itself be an optimization resource

The original proposal's motivation is striking from a retention perspective. The device spends resources keeping data alive because it cannot tell which data the host still cares about.

Once the host communicates that a range is no longer needed, the device may optimize maintenance.

So retention has a cost not only when state is difficult to preserve, but also when **unnecessary state is preserved because currentness information failed to cross a boundary**.

This is an engineering reconstruction of the proposal's motivation, not period philosophical vocabulary.

### E — deterministic read semantics retain a new relation rather than the old payload

For DRAT, what must remain stable after the defining read is not necessarily the former user data. The retained relation is instead closer to:

```text
trimmed logical block
    + advertised deterministic behavior
    + first qualifying post-Trim read result
        -> later reads remain consistent until successful write
```

This is another form of technical retention: stability of **interface behavior** after continuity of the old payload has been withdrawn.

### E — RZAT can preserve semantic predictability while forgetting historical content

A zero-return rule is particularly clear:

```text
historical pre-Trim content
    no longer promised

but

future read result
    highly predictable
```

Predictability and historical continuity are therefore independent dimensions.

---

## Functional analogy — bounded cross-case comparisons

### Case 04 base patent: replacement invalidation

Ban's bounded 1993 system invalidates an old physical block because a replacement becomes the current embodiment of the same virtual address.

The TRIM slice is different:

```text
Ban overwrite path:
new payload becomes current
    -> old physical embodiment loses logical currentness

TRIM path:
host withdraws need for the old logical payload
    -> no replacement payload is required at that moment
```

They share a distinction between **physical survival** and **logical currentness**, but they are not the same historical mechanism.

### Case 05 CRUSH: physical presence versus current authority

A purely functional analogy exists with replicated storage: a physical copy may remain somewhere without retaining current placement/content authority.

TRIM likewise shows that historical bits and current logical authority are not identical concepts.

No historical genealogy between ATA TRIM and Ceph is asserted.

### Secure erase / sanitize

TRIM must not be treated as a functional synonym for an erase/sanitize command.

The T13 DRAT proposal itself mentions `SECURITY ERASE UNIT` as an example of a later operation that can make a logical block determinate, which is already enough to show that Trim and Security Erase are distinct command/semantic categories in the proposal text.

Therefore:

```text
logical discardability
    !=
security-assured destruction
```

---

## Philosophical interpretation — forgetting can be an explicit interface permission

The historical fact is narrow: T13 proposals created a way for the host to tell a device that certain logical data no longer needed ordinary preservation, then refined what reads were allowed to mean afterward.

A bounded interpretation follows:

> some technical forgetting is not merely passive decay or accidental loss. It can begin when one layer explicitly withdraws another layer's obligation to preserve an earlier state as current.

This does not mean the old physical representation instantly disappears. Nor does it mean standards participants framed TRIM philosophically.

The useful conceptual sequence is:

```text
past state existed
    ↓
future operations no longer owe that state continuity
    ↓
interface defines what may count instead
```

That is a different phenomenon from both physical erasure and accidental corruption.

---

## Semantic / failure boundary matrix

| Situation | What is established | What is not established |
| --- | --- | --- |
| filesystem marks blocks free but sends no Trim | host-side invalidation may exist | device knows range is discardable |
| Trim successfully communicates a range | device receives host discardability information under the command contract | corresponding NAND cells have already been erased |
| post-Trim read is indeterminate | old payload is not promised by that read contract | random physical bits, a specific stale value, or secure destruction |
| DRAT behavior is advertised | proposed deterministic rule governs post-Trim reads | determinate value equals pre-Trim payload |
| read-zero behavior is advertised | host-visible reads may return all-zero words under the proposal | old physical cells are proven zero/erased |
| later successful write completes | new written data become determinate at the LBA | every earlier physical embodiment is already reclaimed |
| Trim reduces preservation work | device may optimize around host-declared invalid data | any universal controller algorithm or immediate garbage-collection schedule |

---

## Explicit non-claims

This deepening does **not** claim that:

1. T13 invented the general idea of notifying storage that data are no longer needed.
2. `e07154r0` is the first historical proposal anywhere for discard/deallocation semantics.
3. the 2007–2010 proposal sequence directly descends from Amir Ban's 1993 patent.
4. Amir Ban's patent used the word `TRIM` in this ATA sense.
5. every filesystem deletion issues ATA Trim.
6. every ATA device supports Trim.
7. every device supporting Trim is an SSD.
8. a successful Trim command proves immediate physical NAND erase.
9. a successful Trim command proves stale physical data remain recoverable.
10. a successful Trim command proves stale physical data are unrecoverable.
11. a zero returned after Trim proves the underlying cells physically contain zeros.
12. DRAT preserves the pre-Trim payload.
13. non-deterministic read-after-Trim means that each read must differ from every prior read.
14. `indeterminate` means electrical randomness.
15. Trim is a secure erase, sanitize, purge, or cryptographic-erase primitive.
16. Security Erase and Trim have the same authorization or completion semantics.
17. the proposals expose the exact FTL metadata bit used to mark a range invalid.
18. the proposals specify a universal garbage-collection latency after Trim.
19. the proposals require a particular wear-leveling algorithm.
20. all later ACS revisions retained every wording choice of the cited proposals unchanged.
21. T13 committee proposal dates are invention-priority dates.
22. DRAT/RZAT terminology proves one specific NAND physical implementation.
23. Trim guarantees a specific forensic-recovery outcome across devices.
24. old physical embodiment survival implies old logical currentness.
25. logical invalidation by itself is physical destruction.

---

## Claim ledger

| Claim | Evidence | Layer | Strength |
| --- | --- | --- | --- |
| T13 has a 23 Apr 2007 `Notification for Deleted Data` proposal and later `Data Set Management` revisions | official T13 document index | H/P | strong |
| `e07154r6` says delete knowledge is retained by OS rather than device | proposal body | H/P | strong |
| proposal says devices otherwise treat valid and deleted/invalid data similarly | proposal body | H/P | strong |
| proposal names merge, wear leveling and erase as SSD operations applied while keeping data alive | proposal body | H/P | strong |
| e07154r6 added DATA SET MANAGEMENT and TRIM | e08137r4 retrospective statement | H/P | strong |
| original Trim proposal allowed non-deterministic read behavior | e08137r4 | H/P | strong |
| e08137r4 proposes advertised deterministic vs non-deterministic post-Trim behavior | e08137r4 | H/P | strong |
| deterministic post-Trim result need not be the old payload | e08137r4 semantics | E | strong bounded inference |
| e09117 proposes identifying devices that return zero after Trim | e09117r1 | H/P | strong |
| zero-return contract does not prove physical zeroing | proposal/interface boundary | E | strong bounded inference |
| later successful write re-establishes determinate written content | e08137r4 / e09117r1 | H/P | strong |
| logical invalidation, post-invalidation read semantics, and physical reclaim are distinct questions | proposal sequence + Case 04 | E | strong reconstruction |
| Trim is not secure-sanitization evidence | command/claim boundary | E | strong negative boundary |
| 2009–2010 T13 proposal history continued with Read Zero and Trim Clarifications | official T13 index | H/P | strong metadata claim |

---

## Remaining evidence debt

This slice deliberately leaves several questions open:

1. **final-standard wording** — inspect a stable facsimile of the relevant final ACS-2 text and compare it line-by-line with `e08137`, `e09117`, and `e09158` proposal wording;
2. **committee decision trail** — inspect plenary/ad-hoc minutes to determine exactly which revisions were accepted and when, rather than treating proposal submission as adoption;
3. **SCSI/SAT cross-standard genealogy** — follow the T10 documents cited by DRAT and Read Zero proposals without assuming simple one-way influence;
4. **named-product behavior** — add a bounded early SSD that advertises specific DRAT/RZAT bits and, ideally, contemporaneous test evidence;
5. **power-failure boundary** — determine whether early devices persisted Trim/deallocation metadata atomically across power loss, rather than inferring this from host-visible command semantics;
6. **physical reclamation timing** — use controller/vendor/measurement evidence if the project later needs to state when invalidated physical pages actually become erase candidates or are erased;
7. **security boundary** — use ATA Security/Sanitize specifications for claims about assured destruction rather than importing those claims into Trim.

These debts are intentionally narrower than “write a history of TRIM.”

---

## Relation to `computing-archaeology`

A fresh repository search found no dedicated `TRIM` / `ATA Data Set Management` packet in `tmzncty/computing-archaeology` to reuse.

This record therefore keeps only the retention-specific seam:

```text
host-side validity knowledge
    -> explicit discardability notification
    -> changed obligation to preserve old logical content
    -> separately advertised post-invalidation read semantics
    -> later republication by write
```

Broader ATA/SATA command genealogy, T13/T10 committee history, SSD-controller implementation history, early product adoption, filesystem support chronology, SCSI UNMAP, and NVMe deallocation belong in `computing-archaeology` if/when developed.

---

## Sources

### Primary / committee sources

- Technical Committee T13 AT Attachment, document search/index: <https://t13.org/docsearch>.
- Frank Shu, `T13/e07154r6`, *Data Set Management Commands Proposal for ATA8-ACS2*, rev. 6, December 2007 / submitted 10 January 2008. Public mirror: <https://www.sgv417.jp/~makopi/blog/wp-content/uploads/2018/05/e07154r6-Data-Set-Management-Proposal-for-ATA-ACS2.pdf>.
- Fred Knight / Curtis E. Stevens, `T13/e08137r4`, *Deterministic TRIM Proposal for ATA8-ACS2*, 17 December 2008. Public copy: <https://pcper.com/wp-content/uploads/2009/04/b2e2-e08137r4-drat-deterministic-read-after-trim.pdf>.
- Fred Knight, `T13/e09117r1`, *Read zero after TRIM Proposal for ATA8-ACS2*, June 2009. Public mirror: <https://www.sgv417.jp/~makopi/blog/wp-content/uploads/2018/05/e09117r1-Read-Zero-after-Trim.pdf>.
- Technical Committee T13 AT Attachment, `e09158r0–r2`, *Trim Clarifications*, official index metadata, 2009–2010.

### Contemporary secondary corroboration

- Graeme B. Bell and Richard Boddington, “Solid State Drives: The Beginning of the End for Current Practice in Digital Forensic Recovery?”, *Journal of Digital Forensics, Security and Law* 5(3), 2010, DOI `10.15394/jdfsl.2010.1078`: <https://commons.erau.edu/jdfsl/vol5/iss3/1/>.

---

## Bounded conclusion

The T13 proposal sequence makes a useful later boundary visible for Case 04:

```text
physical bits may have a history
        !=
old payload retains logical currentness

logical address remains addressable
        !=
pre-Trim content must remain readable

post-Trim read returns a predictable value
        !=
that value is a proof of physical erasure

host withdraws retention obligation
        !=
secure destruction has completed
```

The important retention event is not merely that data can be erased. It is that **one layer can explicitly tell another layer that an earlier logical state no longer needs to be preserved as current, after which the interface separately defines what future reads are allowed to mean**.
