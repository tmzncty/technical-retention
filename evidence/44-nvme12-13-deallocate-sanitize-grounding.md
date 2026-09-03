# Case 44 Grounding — NVMe Deallocate and Sanitize (2016–2017)

## Purpose

This record grounds [`../cases/44-nvme13-deallocate-sanitize-forgetting.md`](../cases/44-nvme13-deallocate-sanitize-forgetting.md) in official NVM Express Revision 1.3 and Revision 1.2.1 text. It records the exact evidence needed to keep four different relations apart:

```text
host deallocation hint
    !=
logical deallocation state
    !=
physical/media erasure
    !=
successful subsystem sanitization
```

It also records the prior-art boundary needed to avoid claiming that Revision 1.3 invented secure erase, cryptographic erasure, deallocation, or media sanitization.

## Primary sources

### NVM Express Revision 1.3

NVM Express, **NVM Express Revision 1.3**, May 1, 2017; the specification states that Revision 1.3 was ratified April 26, 2017.

Direct source:

- <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>

Sections inspected:

- §5.24, `Sanitize command` — printed pp. 168–170 / PDF pages around 167–169;
- §6.7 and §6.7.1.1, `Dataset Management command` / `Deallocate` — printed pp. 182–185 / PDF pages around 181–184;
- §8.15, `Sanitize Operations` — printed pp. 267–270 / PDF pages around 266–269.

### NVM Express Revision 1.2.1

NVM Express, **NVM Express Revision 1.2.1**, June 2016.

Direct source:

- <https://nvmexpress.org/wp-content/uploads/NVM_Express_1_2_1_Gold_20160603-1.pdf>

Section inspected:

- §5.16, `Format NVM command – NVM Command Set Specific` — printed pp. 137–139 / PDF pages around 136–138.

## Directly grounded historical claims

### Revision 1.3 §6.7 — Dataset Management is advisory

The specification defines Dataset Management as a host mechanism for indicating attributes of logical-block ranges, including information intended to help performance and reliability decisions.

The decisive boundary is explicit: the command is **advisory**, and a compliant controller may choose to take no action based on the supplied information.

In the command field definition, `Attribute – Deallocate (AD)` set to `1` means the NVM subsystem **may deallocate** the provided ranges.

**Supported historical claim:** host expression of deallocation eligibility is not itself proof that a particular physical erase has occurred.

### Revision 1.3 §6.7.1.1 — a deallocated LBA may return its last-written value

The specification states that:

- writing a deallocated logical block makes it no longer deallocated;
- reads do not change deallocation status;
- reads from a deallocated logical block are deterministic until a later write;
- the returned value may be all `00h`, all `FFh`, **or the last data written** to the logical block and metadata;
- access is prohibited to values written before the most recent successful sanitize operation;
- the host may optionally enable an error for reads of unwritten/deallocated blocks when the feature is supported.

The section also notes that NVMe Deallocate is similar to ATA DATA SET MANAGEMENT with Trim (ACS-2) and SCSI UNMAP (SBC-3).

**Evidence consequence:** `deallocated` cannot be normalized into `physically erased` or even `old logical value must be unreadable` under the bounded Revision-1.3 contract.

### Revision 1.3 §5.24 — command completion is not operation completion

The specification says all three sanitize-operation classes — Block Erase, Crypto Erase, and Overwrite — execute in the background.

A successful `Sanitize` command completion means that the sanitize operation was started. It explicitly does **not** indicate that the sanitize operation itself has completed.

If the Sanitize command does not complete successfully, the operation for that command is not started, the Sanitize Status log is not modified for that command, and user data is not altered by that failed command initiation.

**Evidence consequence:** command acknowledgement and completed forgetting are separate temporal/interface states.

### Revision 1.3 §8.15 — sanitization scope

The specification defines the scope of a sanitize operation as all locations in the NVM subsystem that are able to contain user data, explicitly including:

- caches;
- unallocated areas;
- deallocated areas of the media.

It separately excludes regions that do not contain user data under the bounded text, including the Replay Protected Memory Block and boot partitions.

Once started, the operation cannot be aborted and continues across Controller Level Reset, including across power cycles.

**Evidence consequence:** the sanitization target is broader than the host's currently allocated LBA set, and persistence of the sanitization process itself across resets/power cycles is part of the operation contract.

### Revision 1.3 §8.15 — three sanitize mechanisms

The specification distinguishes:

- **Block Erase** — media-specific low-level block erase for locations in which user data may be stored;
- **Crypto Erase** — changes media encryption keys for such locations;
- **Overwrite** — writes fixed/related patterns one or more times over such locations.

It warns that multiple-pass Overwrite may adversely affect NAND endurance.

**Evidence consequence:** one interface-level forgetting objective can be satisfied through materially different mechanisms. The standard itself does not license treating key destruction, block erasure, and overwrite as one physical process.

### Revision 1.3 §8.15 — retained status of a forgetting operation

The `Sanitize Status` log contains a consistent snapshot of the most recently started sanitize operation, including whether one is in progress, its parameters, and its status. The standard says this page is updated before command completion, on operation completion, and should be updated periodically so the host can inspect progress.

When no sanitize is in progress, `Global Data Erased` indicates whether the NVM subsystem may contain user data under the field's defined conditions.

**Evidence consequence:** successful forgetting of payload is accompanied by retained control/status evidence describing the forgetting process and its result.

### Revision 1.2.1 §5.16 — secure erase predates the dedicated Sanitize command

Revision 1.2.1 already lets `Format NVM` request secure erase.

The inspected text distinguishes:

- `User Data Erase`;
- `Cryptographic Erase`.

Secure erase applies to user data regardless of location, with the field definition explicitly giving examples including an exposed LBA, a cache, and deallocated LBAs. Cryptographic Erase operates by deleting the encryption key used for the user data. Successful Format NVM also bars the controller from returning user data that had previously been contained in the affected namespace.

**Evidence consequence:** Revision 1.3 should be credited narrowly with the dedicated Sanitize command/operation model, not with inventing NVMe secure erase as a general concept.

## Visual inspection note

The following original-specification pages were visually inspected in addition to extracted text:

- Revision 1.3 Sanitize-command page showing that sanitize operations run in the background and command completion is not operation completion;
- Revision 1.3 Deallocate page showing that a deallocated read may return zeroes, `FFh`, or the last-written data, plus the ATA Trim / SCSI UNMAP comparison;
- Revision 1.3 Sanitize Operations page showing the Block Erase, Crypto Erase, and Overwrite mechanism definitions;
- Revision 1.2.1 Format NVM secure-erase settings page showing User Data Erase / Cryptographic Erase and the scope across exposed/cache/deallocated locations.

No claim in the case depends solely on inferred layout or an unreadable figure.

## Institutional release-context evidence

NVM Express's 2017 release announcement identifies **Sanitize** among the major new features of Revision 1.3. A later NVM Express NVMe-CLI explainer likewise says Sanitize was introduced in Revision 1.3 and that Format had previously provided the secure-erase path.

These are used as institutional chronology support. The ratified specifications remain the primary normative evidence.

## Broader prior-art boundary

NIST **SP 800-88 Rev. 1**, finalized December 17, 2014, defines media sanitization as rendering access to target data infeasible for a given level of effort and includes `crypto erase` and `secure erase` in its keyword vocabulary.

This establishes that media-sanitization / crypto-erase terminology predates NVMe Revision 1.3. It does **not** establish direct standards genealogy from NIST into NVMe and is not used to reinterpret normative NVMe fields.

Revision 1.3 itself points from Deallocate to earlier ATA Trim and SCSI UNMAP. That note is sufficient to block a claim that NVMe originated the deallocation idea.

## Evidence distinctions supported

### Historical record

- Revision 1.3 Dataset Management is advisory.
- `AD=1` permits the subsystem to deallocate supplied ranges.
- A deallocated LBA may still return its last-written value.
- Successful sanitize establishes a stronger access boundary for pre-sanitize data.
- Sanitize scope includes caches and unallocated/deallocated areas able to hold user data.
- Sanitize has distinct Block Erase, Crypto Erase, and Overwrite mechanisms.
- Sanitize command completion and sanitize-operation completion are separate.
- Sanitize Status / Global Data Erased expose operation/result state.
- Revision 1.2.1 already defines secure erase via Format NVM.

### Engineering reconstruction

From those normative relations, the repository may infer:

- `logical deallocation != media erasure`;
- `host no-longer-needs hint != proof bytes are gone`;
- `sanitization target != currently allocated LBA set`;
- `logical forgetting can precede material forgetting`;
- `sanitize request acknowledgement != completed sanitize state`;
- `forgetting payload can depend on retaining erasure-progress/result state`;
- `stronger forgetting work != zero medium/endurance cost`.

### Functional analogy

NVMe Deallocate may be compared with ATA Trim and SCSI UNMAP because Revision 1.3 itself makes that interface-level comparison. No claim of implementation identity or invention lineage follows.

Sanitize may also be compared functionally with higher-level delete/tombstone cases only to expose that **currentness deletion** and **media sanitization** are different targets.

### Philosophical interpretation

A narrow interpretation is allowed:

> Technical forgetting can be layered. A system may first withdraw an obligation to preserve one logical association, later reclaim embodiments, and separately perform a sanitization process whose completion must itself be retained as control evidence.

This is project language, not terminology attributed to the NVMe workgroup.

## Unsupported upgrades

The bounded evidence does **not** establish:

- that deallocation physically erases NAND immediately;
- that every post-deallocate read returns zeroes;
- that every NVMe controller supports every sanitize mechanism;
- that a specification-level successful sanitize proves every named product's hidden media has been independently forensically audited;
- that NVMe 1.3 invented secure erase, crypto erase, sanitization, TRIM-like deallocation, or media sanitization;
- that crypto erase, block erase, and overwrite are physically equivalent;
- that sanitizing an NVMe device establishes application/filesystem/database deletion semantics above the device.

## Related-repository check

`tmzncty/computing-archaeology` was searched before writing for `NVMe sanitize`, `secure erase`, `deallocate`, `TRIM`, and SSD sanitization. No dedicated case was found. Generic Flash/SSD implementation history remains routed there; this record exists because the **retention/forgetting-layer distinction** changes the cross-case argument in `technical-retention`.
