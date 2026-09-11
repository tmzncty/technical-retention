# Evidence: NVMe 1.0 `Write Uncorrectable` — logical unreadability without deallocation or sanitization

**Status:** `grounded`

**Case:** [Case 44 — NVM Express 1.3 Deallocate and Sanitize](../cases/44-nvme13-deallocate-sanitize-forgetting.md)

**Scope:** host-interface semantics and a bounded earlier functional prior-art touchpoint. This record does **not** infer controller/NAND implementation, physical erasure, forensic unrecoverability, or a direct SCSI→NVMe genealogy.

## Research question

What does a storage interface retain when the host deliberately asks that an LBA become unreadable? In particular, is a host-visible read error the same state as deallocation, physical erasure, or sanitization?

The answer from the original NVMe 1.0 specification is unusually sharp: **no**. `Write Uncorrectable` creates a reversible invalid-LBA/read-error state while the same specification treats the LBA as allocated.

## Primary source A — original NVM Express 1.0 (2011)

**Document:** *NVM Express 1.0*, ratified March 1, 2011.  
**First-party source:** NVM Express, original “Gold” PDF: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0-Gold.pdf>

### Command identity and visible effect

The original specification lists opcode `04h` `Write Uncorrectable` as an **optional** NVM command. Section 6.10 states that the command marks an LBA invalid. A later read of a marked LBA returns failure with `Unrecovered Read Error`. The same section says a **successful write** to the affected logical blocks clears the invalid-LBA status.

Historical record:

```text
ordinary / current LBA
    -- Write Uncorrectable -->
invalid LBA; later read => Unrecovered Read Error
    -- successful Write -->
invalid status cleared
```

This is a host-visible state transition defined by the interface. The text does not specify which internal medium/controller transformation realizes it.

### Allocation state is a separate axis

The Identify Namespace data structure (Figure 67) separately defines allocation semantics. It says a logical block is **allocated** when written with a `Write` **or `Write Uncorrectable`** command; Dataset Management is the command that may deallocate it. The same relationship is used for Namespace Utilization.

That clause rules out a common semantic shortcut:

> **`Write Uncorrectable` invalid/unreadable != deallocated**

Indeed, the interface can classify the affected logical block as allocated while subsequent host reads fail.

### Payload-write accounting is separate again

The SMART/Health information definition for `Data Units Written` says ordinary NVM Write operations contribute to the counter while `Write Uncorrectable` commands do **not**. Read together with the allocation rule, this gives a useful three-way separation:

```text
host payload-write accounting
    !=
allocation state
    !=
readability / validity state
```

The command can change allocation/validity relations without being counted as ordinary host data written.

## Engineering reconstruction

The safest reconstruction is not “the host destroyed the data.” It is:

```text
readability / validity
allocation / deallocation
physical embodiment
sanitization / irrecoverability assurance
```

are independent axes unless a stronger source connects them.

For this command the standard establishes the first two axes only:

- later normal reads fail with `Unrecovered Read Error`;
- the logical block is allocated rather than deallocated;
- a later successful write clears the invalid state.

It does **not** establish:

- that old NAND pages were block-erased;
- that every stale/remapped physical embodiment was overwritten;
- that an encryption key was destroyed;
- that forensic recovery is impossible;
- that a controller uses ECC corruption, an FTL metadata bit, remapping, or any other named internal mechanism.

Therefore:

> **host-visible unreadability != physical absence != sanitization**.

The clearing rule matters methodologically. A status that ordinary write service can clear is strong evidence that the interface is defining a reversible logical/service state. It is not evidence of the much stronger NVMe 1.3 Sanitize postcondition over all user-data-capable subsystem locations.

## Primary source B — T10/05-374r0 `WRITE LONG` pseudo-uncorrectable proposal (2005)

**Document:** George Penokie (IBM/Tivoli), *SBC-3: SPC-4: Disabling Reassign on Write Long Logical Blocks*, T10/05-374 revision 0, October 3, 2005.  
**T10 source:** <https://www.t10.org/ftp/t10/document.05/05-374r0.pdf>

This is **proposal-level committee primary evidence**, not a final-standard facsimile.

Its overview says some SCSI/SAS host controllers used `WRITE LONG` to **intentionally create unrecoverable errors on the media**, calling the intentionally created cases “pseudo uncorrectable errors.” The proposal sought a `COR_DIS` bit so the logical unit would not perform normal error recovery or automatic reallocation for the affected logical block and would return a medium error identifying an LBA marked bad by the application client. The proposed condition remained until the block was later written by another qualifying write/format path.

This supports only a bounded earlier functional claim:

> by October 2005, a T10 committee proposal documented host-controller practice in which a host deliberately induced a later unrecoverable/read-error condition and supplied a rewrite/replace path that removed the condition.

It does **not** prove:

- that T10/05-374r0 itself was final normative standard text;
- the first invention or first implementation of such a practice;
- direct ancestry from SCSI `WRITE LONG` to NVMe `Write Uncorrectable`;
- identical medium behavior.

The last limitation is especially important. The T10 proposal describes `WRITE LONG` as writing a logical block to the medium. NVMe 1.0 `Write Uncorrectable`, by contrast, specifies an invalid-LBA/read-error contract and allocation state without saying how the controller physically creates that state. Functional similarity is therefore not mechanism identity.

## Cross-case use

This deepening sharpens Case 44's existing decomposition:

```text
Write Uncorrectable
    -> allocated + intentionally invalid for normal reads
    -> later successful Write can clear the mark

Dataset Management / Deallocate
    -> allocation relation may be retired
    -> later read value follows the deallocated-LBA contract

Write Zeroes
    -> later read-value contract is zero
    -> may or may not be coupled to deallocation depending on revision/capability

Sanitize
    -> subsystem-wide forgetting operation over locations able to contain user data
    -> separate operation progress/completion semantics
```

The useful lesson is not that these commands form one strength ladder. They alter **different relations**. A command may make a range unreadable while keeping it allocated; another may deallocate it while permitting the last data value to remain readable; another may guarantee zero-valued future reads; sanitization carries a much stronger subsystem-scoped prior-data accessibility contract.

## Prior-art and repository boundary

A repository search found no dedicated `Write Uncorrectable` or `WRITE LONG` history in `tmzncty/computing-archaeology`, so there is no companion technical-history module to duplicate or reuse yet.

The T10 document is enough to block an origin claim for the broad functional idea, but not enough to write a complete genealogy. The following remain open and should stay outside this bounded slice unless separately grounded:

- final-standard history of the relevant SCSI `WRITE LONG` / `COR_DIS` clauses;
- ATA analogues and diagnostic/error-injection command history;
- proposal/ECN genealogy leading into NVMe 1.0 `Write Uncorrectable`;
- named-controller implementation details;
- physical-NAND or forensic experiments comparing invalid marking, deallocation, overwrite, block erase, and sanitize.

## Claim ledger

| Claim | Layer | Evidence strength | Boundary |
| --- | --- | --- | --- |
| NVMe 1.0 contains optional `Write Uncorrectable` | historical / primary | strong | standards-version boundary, not invention priority |
| command marks LBA invalid and later reads return `Unrecovered Read Error` | historical / primary | strong | host-interface semantics only |
| successful later write clears invalid status | historical / primary | strong | does not identify physical cleanup mechanism |
| `Write Uncorrectable` allocates rather than deallocates the logical block | historical / primary | strong | allocation relation, not proof of a payload write |
| `Write Uncorrectable` does not contribute to `Data Units Written` | historical / primary | strong | accounting semantics only |
| unreadable/error-marked state differs from deallocation and sanitization | engineering reconstruction | strong from contrasted clauses | project vocabulary, not historical wording |
| 2005 T10 proposal documents intentional pseudo-uncorrectable `WRITE LONG` use | historical / primary proposal | strong for proposal/practice statement | not final-standard proof or invention priority |
| SCSI and NVMe behavior are directly genealogical or physically identical | rejected | unsupported | functional comparison only |
| read failure proves physical erasure or forensic unrecoverability | rejected | unsupported | requires separate named-device/physical evidence |

## Sources

1. NVM Express, *NVM Express 1.0*, ratified March 1, 2011, especially Identify Namespace Figure 67, SMART/Health accounting, and §6.10 `Write Uncorrectable`: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0-Gold.pdf>
2. George Penokie, T10/05-374r0, *SBC-3: SPC-4: Disabling Reassign on Write Long Logical Blocks*, October 3, 2005: <https://www.t10.org/ftp/t10/document.05/05-374r0.pdf>
