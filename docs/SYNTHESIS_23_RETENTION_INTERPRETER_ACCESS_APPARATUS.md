# Synthesis 23 — Retained State, Interpreter Admissibility, and Access Apparatus

> **Question:** when the material inscription still survives, what else must survive—or be reconstructed—for a future system to make that state operationally available again?

**Status:** bounded cross-case synthesis over already-grounded evidence. This document does not add an invention-priority claim or collapse software interpreters, tape drives, controller firmware, mapping metadata, and human interpretation into one mechanism.

Grounded cases used here:

- [`39 — Flash mapping reconstruction after volatile map loss`](../cases/39-flash-mapping-reconstruction-after-power-loss.md);
- [`128 — ZFS vdev labels and uberblock restart roots`](../cases/128-zfs-vdev-label-uberblock-import-root-recovery.md);
- [`129 — ZFS feature flags and software-format admissibility`](../cases/129-zfs-feature-flags-format-compatibility.md);
- [`130 — LTO generational reader compatibility`](../cases/130-lto-generational-compatibility-reader-obsolescence.md);
- [`131 — Dell PERC foreign configuration / controller replacement`](../cases/131-dell-perc-foreign-configuration-controller-replacement.md).

The underlying historical claims remain sourced in those cases and their evidence records. The synthesis below is an **engineering reconstruction and functional comparison** unless explicitly labeled otherwise.

---

## 1. Verdict

The repository can now defend a stronger version of an old caution:

> **material survival is only one condition of recoverability. A future operation may also depend on retained or reproducible roots, mappings, format semantics, reader/transducer capability, controller admission rules, and operation-specific authority.**

But the stronger shortcut is rejected:

```text
state survives physically
        therefore
state remains operationally accessible
```

A better bounded decomposition is:

```text
material embodiment survives
        ↓
identity / restart root / topology is recoverable
        ↓
a compatible access apparatus can interpret or transduce it
        ↓
currentness / admissibility rules accept the candidate
        ↓
the requested service mode is authorized
        ↓
read / recovery / migration / repair can proceed
```

Not every case instantiates every stage, and the stages are not a historical progression. They are comparison axes.

The important negative result is that **technical forgetting can occur as loss of an access relation without requiring physical erasure**, while equally important counterexamples prevent that statement from becoming too broad: restoring a compatible apparatus may recover the state without rewriting the payload; read-only access may survive after write compatibility is lost; and a compatible interpreter never proves that the underlying medium is intact.

---

## 2. Why `interpreter` is not a universal mechanism

This synthesis deliberately uses two terms.

### Software interpreter

Case 129 is genuinely about retained format requirements and software capability. A ZFS implementation that does not understand an active feature can reject read-write import or, depending on the feature class, all import. Here `interpreter` is a useful project term for software that implements the semantics required by the retained on-disk format.

### Access apparatus

Case 130 is different. An LTO drive is not merely a semantic decoder. It is a physical reader/writer with head, servo, signal-processing, channel, firmware, cartridge, and generation-specific format capabilities. Calling it only an `interpreter` would erase the electromechanical and signal path that makes the magnetic inscription readable.

Case 131 differs again. A PERC controller recognizes disk-resident array configuration, admits or rejects a foreign configuration, and may also own pending write-back state on a separate retained-cache carrier. Its role includes protocol authority and reconstruction of an array service relation, not just symbol decoding.

Therefore the umbrella used here is **access apparatus**:

> the hardware, software, firmware, retained control metadata, and admission logic needed to turn a surviving embodiment into an admissible future operation.

This is a project comparison term, not vocabulary attributed to ZFS, LTO, Dell, or Flash-controller engineers.

---

## 3. Cross-case state decomposition

| Layer | Bounded question | Cases that expose it |
| --- | --- | --- |
| Material embodiment | Do the relevant physical bytes / magnetic state / Flash pages still exist? | 39, 128–131 |
| Identity / restart legibility | Can the system locate the retained object and the root/topology needed to traverse it? | 39, 128, 131 |
| Format / signal capability | Does the available software or hardware know how to interpret or transduce the retained representation? | 129, 130, 131 |
| Currentness / admission | Even if readable, is this candidate accepted as the state that may answer now? | 39, 128, 131 |
| Service mode | Is read, write, boot, import, or recovery permitted under the available capability set? | 129, 130, 131 |
| Pending obligation | Is there retained work that still must be completed before ordinary service is fully restored? | 39, 131 |
| Migration / repair | Must state be moved or apparatus preserved before a compatibility window disappears? | 130; functionally 129/131 |

The table is intentionally typed. `readable`, `importable`, `bootable`, `writable`, and `recoverable` are not interchangeable predicates.

---

## 4. Case 39 — payload survival can outlive the resolver inside one device class

Case 39 provides an important internal counterexample to the temptation to treat access-apparatus loss only as archival obsolescence.

The mapped Flash payload may remain nonvolatile while a volatile working map disappears at power loss. Later designs retain checkpoints, logs, validity information, or reconstructible metadata so the controller can rebuild the logical-to-physical relation before ordinary service resumes.

The retained problem is therefore not yet `old hardware no longer exists`. The missing access relation sits *inside* the device/controller architecture:

```text
Flash payload survives
        +
reconstruction substrate survives
        ↓
logical mapping is rebuilt
        ↓
logical addressability returns
```

This yields two limits for the wider synthesis:

- **payload survival ≠ logical legibility**;
- **reconstructing a resolver ≠ reconstructing the payload it resolves**.

A lost mapping relation and an obsolete tape reader are functionally comparable only in the narrow sense that both can separate surviving embodiment from ordinary access. Their physical causes, historical actors, and recovery paths are different.

---

## 5. Case 128 — restart roots are a prerequisite, not the payload itself

ZFS vdev labels and uberblocks show that a large surviving store still needs a small amount of retained control state to become a traversable current pool.

The four vdev labels retain topology/configuration information; multiple uberblock candidates retain restart roots; checksum and transaction-generation rules qualify which root can act as the restart authority. The pool's user blocks are not duplicated four times merely because label copies exist.

The bounded relation is:

```text
payload blocks survive
        +
qualified topology / root evidence survives
        ↓
pool graph becomes restart-legible
```

This is already more than physical persistence, but it is still not the same as Case 129. A perfectly qualified restart root can point into a pool whose active format requirements the available software does not understand.

So:

> **restart legibility ≠ format interpretability**.

That distinction is essential when discussing long-term preservation. Keeping the root that tells software *where the state is* is not enough if the software no longer knows *what the retained structures mean*.

---

## 6. Case 129 — format requirements can outlive the software that understands them

ZFS feature flags give a particularly clean software-obsolescence boundary.

The retained pool records feature requirements. `features_for_read` and `features_for_write` are distinct; `enabled` and `active` are distinct; unsupported active features can block read-write import while some read-only-compatible cases retain a narrower access path.

This produces a typed compatibility relation:

```text
pool bytes survive
        +
restart root survives
        +
active feature requirements survive
        ↓
available software capability is tested
        ↓
read-only / read-write / no-import outcome
```

The strongest result is not `old software loses data`. The data can remain materially unchanged while an older interpreter becomes inadmissible.

Equally, reinstalling or preserving compatible software does not establish medium integrity. It restores one access condition only.

Therefore:

- **software downgrade/absence ≠ physical erasure**;
- **compatible interpreter ≠ verified media integrity**;
- **read compatibility ≠ write compatibility**;
- **recognizing a feature identifier ≠ implementing its semantics**.

---

## 7. Case 130 — a surviving format can lose its physical reader population

LTO adds the hardware side of the same analytical problem without turning it into the same mechanism.

The official compatibility rules give bounded read/write generation windows, and the current LTO-10 generation breaks the older assumption that buying a newer drive necessarily extends access to older cartridges. An old tape may remain physically intact while the population of drives capable of reading it shrinks.

The relation is:

```text
magnetic cartridge survives
        +
compatible drive generation remains available
        ↓
signal / format recovery remains possible
```

A newer drive generation does not erase the old tape. Conversely, media survival does not manufacture a compatible reader.

This case therefore grounds a practical migration pressure:

> **when reader compatibility is bounded, preservation may require either retaining a functioning reader path or migrating the state while that path still exists.**

This is an engineering consequence, not a vendor-prescribed universal migration interval. It also remains separate from software-format compatibility: an LTO drive is a physical transduction apparatus, not merely a file-format parser.

---

## 8. Case 131 — controller admission and pending-write continuation are separate access relations

Dell PERC foreign configuration sharpens the distinction between *recognition* and *completion*.

Member disks can retain array configuration after the controller's current admitted configuration is gone. A compatible controller can detect the disks as `foreign` and, under supported conditions, import that configuration. The disks therefore carry enough retained topology/configuration state to help reconstruct the virtual-disk relation.

But the H800 deepening adds another state class. A transportable TBBU/TNVC can preserve pending write-back state across failure of the controller card and move to another H800. That retained cache still has to be flushed to the virtual disks.

Thus two access/recovery layers coexist:

```text
member disks:
    array configuration + payload/parity embodiments

retained cache carrier:
    pending acknowledged writes not yet committed to members
```

A replacement controller can need both, but they answer different questions.

Therefore:

- **foreign configuration recognized ≠ foreign configuration admitted**;
- **array topology recovered ≠ pending writes committed**;
- **compatible replacement controller ≠ arbitrary cross-generation portability**;
- **controller-card failure ≠ retained-cache-carrier failure**.

This prevents `controller replacement` from becoming a loose synonym for `data recovery`.

---

## 9. Operation-specific compatibility

The cases jointly reject a scalar notion of `compatible`.

Compatibility is typed by the requested operation:

```text
can identify
can read
can reconstruct
can import read-only
can import read-write
can boot
can modify safely
can complete pending writes
can migrate
```

Case 129 explicitly separates read and write feature requirements. Case 130 separates read and write generation support. Case 131 separates configuration recognition/import from later dirty-cache commitment. Case 128 separates root selection from later integrity verification.

A preservation plan that records only `compatible: yes/no` therefore loses relevant state about *what operation remains possible*.

---

## 10. Access apparatus as retention infrastructure

### Engineering reconstruction

A tape drive, boot loader, compatible ZFS implementation, controller firmware, mapping-recovery substrate, or replacement-controller cache interface may contain no copy of the user payload being preserved. Yet without it the surviving payload may be unusable.

So this synthesis adds a controlled extension to the project's idea of retention infrastructure:

> **some retention infrastructure preserves not the payload but the future ability to interpret, transduce, admit, or continue it.**

This is analogous to spare capacity or hold-up energy only at the level of `necessary enabling infrastructure`. It is not the same mechanism.

The distinction also explains why long-term preservation can require work *before* physical decay is visible. The operator may have to preserve readers, software, keys, adapters, metadata, documentation, or a migration path while all current bits still read correctly.

---

## 11. Loss of access relation is not automatically irreversible forgetting

A particularly important counterexample is recoverability after apparatus restoration.

If an old LTO drive can still be obtained and operated, or compatible ZFS software can be restored, ordinary access can return without changing the retained payload first. Likewise, Case 39 can reconstruct a mapping relation from surviving controller metadata.

Therefore:

```text
unavailable under the current apparatus
        ≠
irrecoverably forgotten
```

A better distinction is:

- **current service unavailable** — the present stack cannot answer;
- **recoverable with preserved/reconstructible apparatus** — a viable access path still exists;
- **migration-required risk** — the viable path is shrinking or depends on aging infrastructure;
- **access-path exhaustion** — no admissible interpreter/reader/controller path is currently known;
- **physical erasure/destruction** — the relevant material embodiment itself is gone or unusable.

Those conditions can overlap, but they should not be collapsed.

---

## 12. Functional analogies and hard stops

### A — ZFS software compatibility and LTO drive compatibility

Both can make surviving bytes unavailable when capability is missing.

**Stop:** ZFS feature semantics are software-format interpretation; LTO depends on a physical drive/media signal path and generation-specific recording format. No common mechanism or genealogy is asserted.

### A — Flash mapping reconstruction and PERC foreign configuration

Both use retained control metadata to reconstruct a logical service relation above surviving media.

**Stop:** FTL mapping reconstruction resolves logical blocks inside managed Flash; PERC foreign import reconstructs a RAID virtual-disk topology/admission relation. They are not the same metadata format or historical lineage.

### A — ZFS restart roots and PERC array metadata

Both show that small retained control structures can organize a much larger surviving payload set.

**Stop:** ZFS root selection and hardware-RAID foreign import have different consistency, redundancy, authority, and failure rules.

### X — `all technical access is interpretation`

Rejected as too broad. Physical transduction, servo control, ECC, mapping reconstruction, software parsing, and administrator admission are technically different operations. `Interpretation` can be useful philosophically only after those distinctions are preserved.

---

## 13. Philosophical interpretation — bounded

### I — technical forgetting can occur through relation loss

The cases support a limited philosophical statement:

> A technical inscription can remain materially present while the system loses the relation that makes the inscription available as a usable continuation of a prior state.

That relation may involve mapping, root authority, software semantics, reader capability, or controller admission.

This is stronger than saying `meaning is contextual`, because the contexts here are exact engineering dependencies that can often be tested: feature support, generation compatibility, checksums, topology metadata, controller model, or mapping-recovery evidence.

### Limit

Do not turn this into `physical survival is irrelevant`. If the medium is destroyed, the access apparatus cannot reconstruct arbitrary missing payload. And do not equate machine compatibility with human semantic understanding: preserving an LTO reader and ZFS implementation does not by itself preserve the institutional, linguistic, or cultural meaning of the files recovered through them.

The open human/procedural-context problem therefore remains larger than this synthesis.

---

## 14. Related-repository boundary

[`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) remains the proper home for broad histories of tape transports, storage-controller families, interface adapters, boot environments, and file-format/device genealogy. The grounded source cases already record searches that found no dedicated overlapping ZFS-feature, LTO-reader, PERC-H800, or FTL-recovery case to reuse at those moments.

`technical-retention` keeps only the cross-case result: **access apparatus and compatibility relations can be constitutive parts of retention even though they are not themselves the retained payload.**

Future work that should not be forced into this synthesis includes:

- actual controlled migrations between LTO generations;
- reader-head/servo aging and repair labor;
- host-interface and adapter obsolescence;
- emulator/VM preservation and operating-system dependency chains;
- application schemas, encodings, and external semantic context;
- encrypted stores where key/KMS availability composes with format and reader compatibility;
- independent fault injection for controller replacement and format downgrade/upgrade paths.

---

## 15. Bounded conclusion

The mature comparison is no longer:

```text
stored state = durable physical inscription
```

Nor should it become:

```text
stored state = interpretation alone
```

The defensible relation is narrower:

> **A surviving embodiment remains operationally retained for a future task only when the task still has an admissible path through the required identity/root, access apparatus, format or signal capability, currentness rules, and service authority. Those supporting relations can fail, be preserved, be reconstructed, or require migration independently of the payload's physical survival.**

This is an analytical invariant across the selected cases, not evidence that Flash controllers, ZFS, LTO, and PERC share one historical lineage.
