# Case 44 Deepening — NVMe Write Zeroes, Deallocation, and Logical-Value Semantics (2011–2017)

## Purpose

This record deepens [`../cases/44-nvme13-deallocate-sanitize-forgetting.md`](../cases/44-nvme13-deallocate-sanitize-forgetting.md) around one bounded interface question:

> when an NVMe host wants a range to read as zero, how is that relation different from saying that the range is deallocated, and how are both different from sanitizing prior user data?

The existing Case 44 already grounds `Deallocate` and `Sanitize`. This addendum does **not** create a second generic erase case. It reconstructs the intervening `Write Zeroes` branch from official NVM Express 1.0, 1.1, and 1.3 material and uses it to keep three relations distinct:

```text
allocation/currentness state
    !=
future logical read-value contract
    !=
media-sanitization / prior-data-unrecoverability contract
```

Claim labels used below follow repository policy: **Historical record**, **Engineering reconstruction**, **Functional analogy**, and **Philosophical interpretation** are kept separate.

## Sources inspected

### NVM Express Revision 1.0 — March 1, 2011

Official NVM Express PDF:

- <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0-Gold.pdf>

Directly inspected:

- front matter: Revision 1.0, dated and ratified **March 1, 2011**;
- §6 / Figure 98, `Opcodes for NVM Commands`, printed p. 87 / PDF page 86.

Figure 98 lists `Flush`, `Write`, `Read`, `Write Uncorrectable`, `Compare`, and `Dataset Management` as the standard NVM commands in that revision and states that opcodes not listed are reserved. `Write Zeroes` is not present in that command table.

**Historical-record boundary:** this establishes that the inspected NVMe 1.0 command set did not yet contain the later standardized `Write Zeroes` command. It does not establish that zero-fill operations, controller-side zero generation, or analogous commands were invented by NVMe 1.1.

### NVM Express Revision 1.1 — October 11, 2012

Official NVM Express PDF:

- <https://www.nvmexpress.org/wp-content/uploads/NVM-Express-1_1.pdf>

Directly inspected:

- front matter: Revision 1.1, **October 11, 2012**;
- Identify Controller `Optional NVM Command Support (ONCS)`, printed p. 86 / PDF page 85;
- §6 / Figure 121, NVM command opcodes, printed p. 110 / PDF page 109;
- §6.6.1.1 `Deallocate`, printed p. 117 / PDF page 116;
- §6.15 `Write Zeroes command`, printed p. 129 / PDF page 128.

The ONCS field makes `Write Zeroes` optional in Revision 1.1: bit 3 indicates whether the controller supports it. Figure 121 separately lists opcode `08h` as optional `Write Zeroes` and opcode `09h` as optional `Dataset Management`.

### NVM Express Revision 1.3 — May 1, 2017; ratified April 26, 2017

Official NVM Express PDF:

- <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>

Official NVM Express revision-change summary:

- <https://nvmexpress.org/changes-in-nvme-revision-1-3/>

Directly inspected:

- Revision 1.3 front matter for date / ratification;
- §6.16 `Write Zeroes`, printed pp. 198–199 / PDF pages 197–198;
- the revision-change entry `Deallocated Value for Logical Block Data`, which points to Technical Proposal 019 and says Revision 1.3 added a mechanism for determining values returned for deallocated logical blocks and a mechanism for requesting deallocation as part of `Write Zeroes`.

The Technical Proposal itself is member-workspace material in the cited NVM Express page and was not used as if independently inspected here.

## Historical record — Revision 1.1 creates a value-setting path distinct from deallocation

Revision 1.1 §6.6.1.1 says that a deallocated LBA returns a deterministic value until another write, but that value may be:

- all zeroes;
- all ones; or
- the last data written to the LBA.

The same section explicitly compares NVMe Deallocate to ATA Data Set Management with Trim and SCSI UNMAP. It does not promise that deallocation alone establishes a zero-valued logical block.

Revision 1.1 §6.15 gives `Write Zeroes` a different contract: after successful completion, subsequent reads of the specified logical blocks **shall return zeroes until another write occurs**.

Therefore, within one dated specification:

> **deallocated != guaranteed-zero-on-read**.

And conversely:

> **guaranteed-zero-on-read != necessarily deallocated**.

The two operations answer different interface questions even though an implementation may later combine them.

## Historical record — Write Zeroes is optional in Revision 1.1

The Identify Controller `ONCS` field in Revision 1.1 assigns one capability bit to `Write Zeroes` and another to Dataset Management. A controller may therefore support one, both, or neither optional command under the bounded Revision-1.1 contract.

This blocks a common retrospective collapse:

> **NVMe 1.1 support != universal Write Zeroes support on every Revision-1.1 controller**.

It also supplies a clean interface-level separation between the command vocabulary and a particular product's implementation.

## Historical record — Force Unit Access strengthens persistence, not sanitization

Revision 1.1 `Write Zeroes` includes an `FUA` bit. When set, the specification says the data shall be written to non-volatile media before command completion and explicitly says that this creates no implied ordering with other commands.

The bounded conclusion is:

> **FUA-qualified Write Zeroes completion != sanitize completion**.

FUA strengthens the persistence boundary for the resulting write operation. It does not say that every previous physical embodiment, remapped location, cache residue outside the bounded write path, or forensic trace has been erased or made unrecoverable.

That distinction is especially important because Case 44 already grounds a much broader `Sanitize` target: locations in the subsystem capable of containing user data, including deallocated areas and caches under the Revision-1.3 contract.

## Historical record — Revision 1.3 can combine zero-read semantics with deallocation

Revision 1.3 §6.16 retains the `Write Zeroes` logical contract: successful completion makes subsequent reads return `00h` until another write.

It also adds the `DEAC` bit and conditions its behavior on the namespace's deallocated-read feature. Where the namespace supports zero-valued reads from deallocated logical blocks, a `Write Zeroes` command may produce its required zero-read result while deallocating the affected logical blocks. If the namespace cannot provide zero-valued deallocated reads, the controller shall not deallocate logical blocks in the range as part of that `Write Zeroes` operation.

The NVM Express Revision-1.3 changes page describes this explicitly as a change to deallocated-value behavior and as adding a host mechanism to request deallocation as part of `Write Zeroes`.

This produces a useful interface counterexample:

```text
same host-visible zero result
    can coexist with
allocated/write-zero state
    or
zero-reading deallocated state
```

The visible value contract therefore does not uniquely identify the allocation state underneath it.

## Engineering reconstruction — value, allocation, embodiment, and sanitization are separate axes

The standards evidence supports a four-axis reconstruction:

1. **logical value contract** — what a later read is required to return;
2. **allocation/deallocation relation** — whether the LBA is treated as deallocated;
3. **persistence boundary** — whether the command completion includes nonvolatile-media completion under `FUA`;
4. **prior-embodiment sanitization** — whether previous user data is required to be unrecoverable across the sanitize scope.

A single word such as `zeroed`, `trimmed`, `erased`, or `forgotten` cannot safely stand in for all four.

The most important counterexample is:

> **zero returned by future reads != proof that old physical embodiments have been sanitized**.

That conclusion is not a claim about one hidden NAND implementation. It follows from the interface contracts themselves: `Write Zeroes` specifies a later logical value, while `Sanitize` separately defines a stronger prior-data-unrecoverability objective over a broader subsystem scope.

## Engineering reconstruction — one visible value can have multiple admissible lower-layer realizations

Revision 1.3 makes the distinction unusually explicit because `Write Zeroes` can either write zero-valued data or use deallocation when the namespace guarantees zero-valued reads from deallocated blocks.

Thus:

> **logical zero is not a unique physical-state description**.

A future read returning `00h` establishes an interface-visible value relation. It does not, by itself, tell an observer whether the controller retained programmed zero data, changed mapping/allocation metadata, reclaimed media, or used another compliant embodiment.

This is a bounded reconstruction of the interface relation, not a claim that every controller uses FTL mapping or one specific zero optimization.

## Functional analogy — negative state and zero value must not be conflated

At a functional level only, this result resembles other repository cases in which a negative or retirement relation is not equivalent to one payload value. JFFS2 Case 145 distinguishes an explicit `JFFS2_COMPR_ZERO` node from mere absence/obsolescence; distributed cases distinguish tombstones or retired references from physical disappearance.

The analogy stops at the relation:

> **absence/retirement metadata and a positive value representation answer different questions**.

There is no claim of shared implementation, genealogy, or historical vocabulary between NVMe and those systems.

## Philosophical interpretation — replacement is not the same operation as forgetting

The technical fact that creates the conceptual problem is simple: a range may become observably zero without the interface claiming that every previous embodiment is unrecoverable, while a sanitize operation explicitly targets prior-data recovery.

A narrow philosophical interpretation is therefore:

> **making a new present value authoritative is not identical to eliminating every technical condition under which an older state might survive.**

This is an interpretation of the engineering distinction, not language attributed to NVM Express designers.

## Prior-art and anti-anachronism boundaries

This deepening makes only a narrow version-history claim:

- NVMe 1.0's inspected NVM command table lacks `Write Zeroes`;
- NVMe 1.1 explicitly contains optional `Write Zeroes` and its zero-read contract;
- NVMe 1.3 later couples `Write Zeroes` to optional deallocation semantics under defined namespace behavior.

It does **not** claim:

- that NVMe 1.1 invented zero-fill or controller-generated zeroing;
- that NVMe invented deallocation, which Revision 1.1 itself compares with ATA Trim and SCSI UNMAP;
- that `Write Zeroes` causes physical NAND programming in every implementation;
- that `FUA` implies media sanitization, whole-device durability ordering, or removal of stale remapped embodiments;
- that a zero-valued deallocated read proves physical erasure;
- that TP019's drafting chronology has been independently reconstructed from member-only proposal material;
- that one interface revision implies immediate implementation in every shipping SSD.

Broader zeroing/deallocation command genealogy, product adoption, controller optimizations, and device-level forensic validation belong primarily in `tmzncty/computing-archaeology` or in a future named-product validation slice rather than being inferred here.

## Resulting bounded distinctions

This addendum grounds the following reusable distinctions for Case 44:

```text
NVMe 1.0 command set
    !=
NVMe 1.1 optional Write Zeroes

Deallocate
    !=
Write Zeroes
    !=
Sanitize

deallocated
    !=
guaranteed-zero-on-read

guaranteed-zero-on-read
    !=
deallocated

logical zero
    !=
unique physical embodiment

FUA-qualified command completion
    !=
sanitation / prior-data-unrecoverability proof

zero-valued future read
    !=
proof of physical erase
    !=
proof of sanitization

Revision-1.3 DEAC coupling
    !=
collapse of value semantics and allocation semantics
```

## Open work deliberately left outside this slice

- exact proposal/ballot history between NVMe 1.0 and 1.1 for `Write Zeroes`;
- public TP019 drafting history beyond the NVM Express change summary;
- ATA `WRITE SAME` / SCSI `WRITE SAME`, UNMAP, and zeroing genealogy;
- named-controller / named-SSD implementation behavior for zero-write optimization;
- tracing of physical NAND behavior under `Write Zeroes` with and without `DEAC`;
- crash/power-cut experiments around FUA and controller caches;
- forensic comparison of logical zeroing, deallocation, secure erase, and Sanitize on named devices.

Those are separate technical-history or validation tasks, not prerequisites for the bounded interface distinction established here.
