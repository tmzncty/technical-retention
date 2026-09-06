# NVM Express 1.3 Deallocate and Sanitize: Logical Forgetting, Media Sanitization, and Completion State

## Status

**`grounded`** — bounded to the NVM Express 1.3 interface semantics for Dataset Management `Deallocate` and `Sanitize`, with NVM Express 1.2.1 `Format NVM` secure-erase semantics used as the immediate prior-version boundary. TCG Opal 1.0 Revision 1.0 (January 2009) is now used as an earlier storage-security prior-art boundary for media-encryption-key eradication and for the explicit `KeepGlobalRangeKey` counterexample in which a security-provider lifecycle reset occurs without cryptographic erase. The case asks what the interface means when a host says that a logical range is no longer needed, versus when it requests that prior user data be made unavailable across the NVM subsystem.

Grounding record: [`../evidence/44-nvme12-13-deallocate-sanitize-grounding.md`](../evidence/44-nvme12-13-deallocate-sanitize-grounding.md).

## Scope

This case addresses one open edge left by mapped Flash Case 04:

> When does a storage interface merely stop promising the continued logical value of a range, and when does it establish a stronger forgetting operation over media locations that may still contain prior user data?

The bounded comparison is:

```text
Dataset Management / Deallocate
    -> host says ranges may be deallocated
    -> controller may act on an advisory command
    -> a later read may still return the last data written

Sanitize
    -> host starts a subsystem-wide sanitization operation
    -> Block Erase / Crypto Erase / Overwrite are distinct mechanisms
    -> operation continues in the background
    -> completion is tracked separately from command completion
    -> successful sanitization prohibits access to pre-sanitize data
```

This is **not**:

- a complete ATA `TRIM`, SCSI `UNMAP`, NVMe sanitization, or SSD-forensics history;
- a claim that NVMe invented deallocation, secure erase, cryptographic erase, or media sanitization;
- evidence that every NVMe SSD implements every optional sanitize mechanism;
- a named-product audit proving that a particular controller actually purges every hidden physical embodiment;
- a claim that logical deallocation physically erases NAND immediately;
- a claim that Block Erase, Crypto Erase, and Overwrite are physically equivalent;
- a claim that `Sanitize` is merely a stronger spelling of `Deallocate`.

The contribution is a bounded **technical-forgetting decomposition** at one standardized interface.

## Historical vocabulary and record

NVM Express Revision 1.3 is dated **May 1, 2017** and records ratification on **April 26, 2017**. Its own vocabulary includes:

- `Dataset Management command`;
- `Attribute – Deallocate (AD)`;
- `deallocated logical block`;
- `Sanitize command`;
- `sanitize operation`;
- `Block Erase`;
- `Crypto Erase`;
- `Overwrite`;
- `No Deallocate After Sanitize`;
- `Sanitize Status`;
- `Global Data Erased`.

Revision 1.3 §6.7 says Dataset Management lets a host communicate attributes for ranges of logical blocks and explicitly characterizes the command as **advisory**: a compliant controller may choose to take no action based on the information supplied. When the `AD` bit is set, the subsystem **may deallocate** the provided ranges.

Revision 1.3 §6.7.1.1 then defines the read semantics of a deallocated logical block. Reads remain deterministic until a later write, but the returned value may be all zeroes, all `FFh`, **or the last data written** to the logical block. The same section says access is prohibited to data and metadata written before the most recent successful sanitize operation.

Those clauses are enough to establish a sharp historical distinction inside the standard itself:

> **deallocation does not, by itself, mean that the prior logical value has become inaccessible through every permitted read behavior.**

The section also states that NVMe Deallocate is similar to ATA DATA SET MANAGEMENT with Trim and SCSI UNMAP. That is an interface comparison made by the standard; it is not evidence that the three mechanisms are historically identical or that one invented the others.

## Mechanism 1 — Deallocation changes allocation/currentness semantics without proving media erasure

A deallocated logical block is no longer deallocated when it is written again. Merely reading it does not change that status.

The important retention relation is what the standard does **not** require. A compliant post-deallocate read can return the last data written. The host's statement that a range may be deallocated therefore cannot be used as evidence that the former physical embodiment was erased, overwritten, or cryptographically severed.

This gives the first central distinction:

> **logical deallocation ≠ physical/media erasure**.

And a stronger interface-level form:

> **host no-longer-needs hint ≠ proof that old bytes are gone**.

This extends Case 04 rather than repeating it. Case 04 grounds logical invalidation, physical relocation, and deferred reclamation in mapped Flash. Case 44 shows a later host/controller interface whose deallocation contract deliberately permits a value relation weaker than sanitization.

## Mechanism 2 — Sanitization scopes beyond the currently allocated LBA set

Revision 1.3 §8.15 defines the scope of a sanitize operation as **all locations in the NVM subsystem able to contain user data**, including caches and unallocated or deallocated areas of the media. It separately excludes regions that do not contain user data, such as the Replay Protected Memory Block and boot partitions under the bounded text.

That scope matters because host-visible allocation state is not a complete inventory of possible old embodiments.

Therefore:

> **sanitization target ≠ currently allocated LBA set**.

A logical address can already have been deallocated while some medium or cache location remains within the sanitization target precisely because it may still contain user data.

This also sharpens the Kirschenbaum/forensics boundary already recorded in the repository:

```text
host-interface currentness
    !=
possible surviving material witness
    !=
post-sanitize admissible user data
```

The case does not claim that every internal physical trace is independently observable or auditable. The standard defines the interface operation and its target scope; actual named-device compliance is a separate evidence class.

## Mechanism 3 — One forgetting objective can be implemented by different state transformations

Revision 1.3 names three sanitize-operation types:

1. **Block Erase** — a media-specific low-level block erase over locations in which user data may be stored;
2. **Crypto Erase** — changes media encryption keys for those locations;
3. **Overwrite** — writes a fixed pattern or related patterns one or more times over those locations.

These operations aim at the same higher-level sanitization relation but alter different things.

Block erase changes storage-media state through the medium's erase mechanism. Crypto erase can leave ciphertext physically present while changing the key relation that made it intelligible. Overwrite deliberately replaces stored patterns.

Therefore:

> **Crypto Erase ≠ Block Erase ≠ Overwrite**.

And:

> **logical forgetting can be achieved without one universal physical act of erasure**.

This is a functional comparison among mechanisms named by the same standard, not a claim that they have identical forensic properties under every implementation or attack model.

The standard also warns that multiple-pass overwrite on NAND can adversely affect endurance. Forgetting work can therefore consume the same finite medium lifetime that ordinary writing consumes:

> **stronger forgetting work ≠ zero material cost**.

## Mechanism 4 — Sanitize command completion is not sanitize-operation completion

Revision 1.3 makes a second unusually clean distinction. Block Erase, Crypto Erase, and Overwrite sanitize operations run **in the background**. Successful completion of the `Sanitize` command means the operation was started; it does **not** mean the sanitize operation has finished.

The later operation has its own progress and completion state in the `Sanitize Status` log and can generate a `Sanitize Operation Completed` asynchronous event.

Therefore:

> **sanitize command completion ≠ sanitize operation completion**.

This resembles other cases in the repository in which an initiating command and the retention/repair work it causes complete at different times, but the historical operation remains NVMe-specific.

The interface also makes sanitization resistant to interruption: once started, the operation cannot be aborted and continues across Controller Level Reset, including across power cycles under the bounded specification text.

So a new temporal relation appears:

```text
request accepted
    -> sanitize work in progress
    -> restricted ordinary service
    -> progress/status retained
    -> sanitize operation completed
    -> post-sanitize accessibility contract
```

The exact transition state matters. A host that sees command completion but does not inspect sanitize-operation status does not yet possess the same evidence as a host that observes successful operation completion.

## Mechanism 5 — Forgetting payload requires retaining proof/state about the forgetting process

The `Sanitize Status` log retains a consistent snapshot of the most recently started operation, including whether sanitization is in progress, parameters, and status. The specification also defines `Global Data Erased`, which indicates whether the subsystem may contain user data when sanitization is not in progress, subject to the bounded definition.

This produces a useful second-order retention relation:

> **forgetting user data can require retaining sanitization state**.

The payload target is to become inaccessible, yet the controller must maintain enough control/status state for the host and the subsystem to distinguish:

- operation not started;
- operation in progress;
- successful completion;
- failure / recovery state;
- whether user data may again have been written since the most recent successful sanitize.

This is not paradoxical. The retained state and the forgotten state have different roles.

A stronger project formulation is:

> **erasure completion is itself a state that must remain knowable long enough to govern later use.**

That formulation is engineering reconstruction, not NVMe's historical phrase.

## Mechanism 6 — Failure of forgetting can become a service state

Revision 1.3 specifies failure-recovery behavior for sanitize operations and restricts commands while sanitization is in progress. A failed sanitize is not simply identical to “nothing happened”: the interface preserves status and can require a subsequent sanitize/recovery path before normal assumptions are restored.

This yields:

> **sanitize failure ≠ ordinary unsanitized service state**.

The point is not that every failure destroys data. It is that the interface gives the sanitization process its own admissibility and recovery state rather than reducing the entire operation to one instantaneous Boolean transition.

## Immediate prior-version boundary — secure erase existed before the 1.3 Sanitize command

NVM Express Revision 1.2.1 (June 2016) already defines secure erase through the `Format NVM` command. The host could request:

- `User Data Erase`;
- `Cryptographic Erase`.

The secure-erase setting explicitly applied to user data regardless of location, including an exposed LBA, cache, and deallocated LBAs. Successful Format NVM also prohibited the controller from returning user data previously contained in an affected namespace.

Therefore:

> **NVMe 1.3 Sanitize ≠ invention of NVMe secure erase**.

The narrower historical claim is that Revision 1.3 introduced the dedicated `Sanitize` command/operation model with explicit background execution, operation status, failure handling, broad subsystem sanitization scope, and the three named action classes in the bounded source.

NVM Express's own later material likewise describes Sanitize as a Revision-1.3 addition and contrasts it with the pre-existing Format secure-erase path.

## Earlier storage-security prior art — TCG Opal 1.0 key eradication (2009)

The **TCG Storage Security Subsystem Class: Opal Specification, Version 1.0, Revision 1.0**, dated **January 27, 2009**, supplies an earlier storage-interface witness for a relation that later appears in NVMe Crypto Erase. The direct TCG PDF is:

<https://trustedcomputinggroup.org/wp-content/uploads/Opal_SSC_1.0_rev1.0-Final.pdf>

Historical vocabulary must remain source-specific. Opal speaks about a `Locking SP`, `Revert`, `RevertSP`, a `media encryption key`, `KeepGlobalRangeKey`, and `cryptographic erase`; this repository should not silently rewrite those 2009 lifecycle/security terms into later NVMe `Sanitize` terminology.

In §5.2.2 (`Revert`, printed p. 76), the specification says that reverting the Locking SP returns it to its original factory state and securely erases personalization. An informative note then states that reverting the Locking SP causes **media encryption keys to be eradicated**, with the side effect of securely erasing data in the User LBA portion. The precise secure-erasure implementation is left implementation-specific.

Section §5.2.3 (`RevertSP`, printed p. 77) provides the more important counterexample. Its optional `KeepGlobalRangeKey` parameter allows the Locking SP to be turned off **without eradicating the media encryption key for the Global locking range** and explicitly describes this as avoiding a **cryptographic erase** of the user data associated with that range. If the parameter is true, the TPer continues using the existing media encryption key after the state transition.

That primary source supports two separate layers.

**Historical record:**

> **security-provider lifecycle reset ≠ cryptographic erase.**

The same family of reset operations can either eradicate a relevant media key or deliberately preserve it.

**Engineering reconstruction:**

> **media-encryption-key eradication ≠ physical ciphertext overwrite.**

In an encrypted-storage regime, recoverability can depend on a retained relation between ciphertext and key material. Destroying that relation can make the old user data unavailable without requiring the same physical transformation as block erase or overwrite. Conversely, preserving the key can preserve that decryptability relation while ownership/security-provider state is reset.

This also blocks a tempting category error:

> **factory-state reset ≠ universal proof of data destruction.**

The effect depends on which retained control and key relations the operation actually retires.

This is a **prior-art boundary**, not an invention claim. The 2009 specification establishes that explicit media-key-eradication / cryptographic-erase semantics predate NIST SP 800-88 Rev. 1 (2014) and NVMe 1.2.1/1.3 (2016–2017), but it does not prove that TCG invented cryptographic erasure, nor does a standards-level contract prove named-product compliance.

## NIST SP 800-88 Rev. 1 — Cryptographic Erase is a key-coverage relation, not a one-key verb

NIST **SP 800-88 Rev. 1, Guidelines for Media Sanitization** (December 2014) is a later institutional guidance source than TCG Opal 1.0 and an earlier source than NVMe 1.2.1/1.3. It is used here for a different purpose from the Opal prior-art boundary: to make explicit the **conditions under which key destruction can or cannot count as Cryptographic Erase (CE)**.

The source is now historical rather than current guidance: NIST withdrew Revision 1 on **September 26, 2025** and superseded it with Revision 2. The claims below are therefore release-bounded to the 2014 document and are not presented as current NIST policy.

### Historical record — target-data coverage precedes key destruction

Section 2.6.1 says CE should not be used to purge a device when sensitive data may have been stored there before encryption was enabled and was not first sanitized. Section 2.6.2 likewise says CE should be considered when **all data intended for CE, including virtualized copies, was encrypted before storage on the media**.

This supplies a direct counterexample to the shortcut `destroy a key -> every historical embodiment is sanitized`:

> **later key destruction ≠ sanitization of earlier plaintext embodiments that were never protected by that key relation**.

The retained/forgotten target must first have been inside the encryption relation on which CE depends.

### Historical record — every relevant key copy and wrapping level matters

Section 2.6.2 says CE should be considered when the organization can know where the target-data encryption key, or an associated wrapping key, is stored and can sanitize those locations; when **all copies** of the encryption keys used for the target data are sanitized; and, where target-data keys are themselves encrypted, when the corresponding wrapping keys can be sanitized with confidence.

Appendix D then makes the hierarchy explicit: the key sanitized by CE may be the **Media Encryption Key (MEK)** or instead a **Key Encryption Key (KEK)** that wraps the MEK or another key. It separately asks implementers to document the wrapping method and assurance level.

Therefore the historical guidance itself blocks a one-object picture of cryptographic erase:

> **one local MEK instance sanitized ≠ every decryptability path retired**.

And:

> **CE key level can be MEK or KEK; key-destruction semantics therefore depend on the retained wrapping relation, not only on physical ciphertext presence**.

The second sentence is an engineering reconstruction of the NIST hierarchy, not NIST's own philosophical vocabulary.

### Historical record — backup and escrow can preserve future recoverability

Section 2.6.3 explicitly warns that a key existing **outside the storage device**, typically because of backup or escrow, may later be used to recover data from the encrypted media. It says CE should not be trusted on devices whose keys have been backed up or escrowed unless the organization has high confidence about how those external keys were stored and managed; backup/escrowed copies belong under a separate sanitization policy for the devices on which they actually reside.

Appendix D therefore asks a vendor statement to identify whether key escrow or backup is supported and whether keys at or below the relevant level have ever been escrowed from or injected into the device.

This grounds a sharper boundary than the earlier Opal case could establish alone:

> **device-local Cryptographic Erase ≠ sanitization of externally retained key copies**.

A storage device can correctly retire its local key relation while another retained key embodiment remains outside that device's sanitization scope.

### Historical record — rewrapping history can create additional key-retention obligations

Appendix D requires documentation of key lifecycle management across wrapping, unwrapping, and rewrapping. It specifically asks how a previous MEK instance was sanitized when the key was wrapped with a user's authentication credentials.

Therefore:

> **terminal CE event ≠ complete key-lifecycle sanitization history**.

A later erase request can only justify the intended forgetting claim if earlier key instances created by lifecycle transitions did not leave an unretired recovery path.

### Historical record — multi-key scope and partial sanitization are separate

Appendix D also requires interface documentation to state what happens when a device supports multiple MEKs: which interface commands change which MEKs, and what additional actions are needed to ensure the intended set is changed. It explicitly notes that not every MEK must be cleared in a **partial sanitization** case.

Therefore:

> **a CE-capable interface ≠ whole-device key retirement by category alone**.

The operation's target set remains part of the sanitization claim.

### Historical record — key-storage failure and verification remain separate from command invocation

NIST's guidance asks how error conditions are handled when a key-storage location cannot be sanitized, and whether the CE operation reports success or failure. Section 2.4/2.6 further warns that CE can be difficult to verify and recommends alternative or additional verifiable methods when sufficient verification cannot be performed.

This keeps three layers apart:

```text
CE command / mechanism available
    !=
all relevant key paths actually retired
    !=
adequate evidence that the intended sanitization result was achieved
```

That decomposition complements, rather than replaces, Case 47's independent raw-Flash compliance evidence.

### Engineering reconstruction — decryptability closure is relational

The bounded sources support a project-level reconstruction:

> **cryptographic forgetting is closure over a decryptability relation, not merely destruction of one named key object.**

For the 2014 NIST model, that relation can include target ciphertext, one or more MEKs, wrapping/KEKs, previous key instances, externally backed-up or escrowed copies, the set of data areas actually encrypted, and the command scope that selects which keys are retired.

This is **engineering reconstruction**, not historical NIST terminology and not a universal theorem about every encryption system. Application/file-level key hierarchies, KMS/HSM implementations, threshold/recovery keys, cloud key services, and named-product behavior remain outside this bounded storage-media case.

## Broader prior art boundary

Media-sanitization vocabulary and cryptographic erasure also predate NVMe 1.3. The TCG Opal 1.0 witness above pushes explicit storage-interface key-eradication / cryptographic-erase semantics back to 2009. NIST SP 800-88 Rev. 1 was finalized in December 2014 and defines media sanitization as rendering access to target data infeasible for a stated level of effort; its keyword set includes `crypto erase` and `secure erase`.

These sources are used to block invention-priority shortcuts and to separate engineering layers. They do **not** imply that NVMe 1.3 simply copied TCG or NIST taxonomy, that TCG originated cryptographic erasure, or that later NVMe interface semantics are reducible to either earlier document.

Similarly, Revision 1.3 itself points from Deallocate to earlier ATA Trim and SCSI UNMAP interfaces. The case therefore makes no `NVMe invented deallocation` claim.

## Failure and forgetting boundaries

The case now separates at least seven meanings that can otherwise be collapsed into `deleted`:

1. **host no longer needs the range** — Dataset Management advisory information;
2. **logical block is deallocated** — allocation/currentness state at the NVMe interface;
3. **a post-deallocate read returns a conventional value** — zeroes, `FFh`, last-written data, or an enabled deallocation error path;
4. **old physical embodiments become reclaimable/reusable** — controller/media policy below the interface;
5. **sanitize operation has started** — successful `Sanitize` command completion;
6. **sanitize operation has successfully finished** — separately reported status/event;
7. **pre-sanitize user data is no longer admissibly accessible** — the stronger sanitization result.

A single verb such as `erase` or `delete` is therefore too weak for cross-case work unless the layer and evidence are specified.

## Cross-case comparison

### With mapped Flash Case 04

Case 04 gives the lower-level relation:

> logical invalidation can precede physical reclamation.

Case 44 adds a standardized host/controller boundary in which Deallocate can leave the last-written value among legal read results, while Sanitize has a broader user-data-removal scope.

The cases are complementary, not a genealogy claim.

### With Kafka/Cassandra/Swift negative-state cases

Cassandra tombstones, Swift `.ts`, and Kafka delete markers retain negative currentness evidence so distributed/log-compacted systems know that an older positive state should not count as current.

NVMe Sanitize has a different target: making prior user data inaccessible across a storage subsystem. A Cassandra tombstone can be perfectly retained while stale lower-layer Flash embodiments remain physically present; conversely, a sanitized device need not retain an application-level tombstone.

Therefore:

> **logical deletion evidence ≠ media sanitization evidence**.

### With SSD retention-maintenance Cases 36–39

Cases 36–39 ask how a controller preserves payload or controller state despite retention error, old-data read cost, power failure, and volatile mapping loss. Case 44 inverts the objective: how does the interface establish that prior payload should no longer remain accessible?

The same controller indirection that complicates preservation also complicates forgetting. Hidden/deallocated/cache locations matter precisely because logical visibility is not an exhaustive map of material embodiments.

## Functional analogy and philosophical limit

A bounded functional analogy can describe Deallocate and Sanitize as two different forms of technical forgetting:

- **deallocation** weakens the obligation to preserve a logical association;
- **sanitization** establishes a stronger operation whose target is prior user-data accessibility across the subsystem.

The analogy stops at the engineering relation. This case is not evidence about human forgetting, repression, social memory, or intentional oblivion.

A narrow philosophical pressure does survive the mechanism:

> A technical system can stop treating a value as current before it has eliminated every material condition from which that value might still be recovered.

And conversely:

> To prove that something has been forgotten at one layer, the system may have to remember the progress and outcome of the forgetting operation at another layer.

These are project interpretations, not claims about the intentions of the NVMe authors.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| NVMe 1.3 Dataset Management is advisory and `AD=1` permits deallocation of supplied ranges | H/P | Revision 1.3 §6.7 |
| A deallocated LBA may legally read back its last-written data | H/P | Revision 1.3 §6.7.1.1 |
| Successful sanitization prohibits access to data/metadata written before that sanitize | H/P | Revision 1.3 §6.7.1.1 + §8.15 |
| Sanitize scope includes caches and unallocated/deallocated areas able to contain user data | H/P | Revision 1.3 §8.15 |
| Revision 1.3 defines Block Erase, Crypto Erase, and Overwrite as distinct sanitize mechanisms | H/P | Revision 1.3 §8.15 |
| Sanitize command completion does not mean sanitize-operation completion | H/P | Revision 1.3 §5.24 + §8.15 |
| Sanitize progress/result is separately represented in Sanitize Status / Global Data Erased state | H/P | Revision 1.3 §8.15 |
| Multi-pass overwrite may adversely affect NAND endurance | H/P | Revision 1.3 §8.15 |
| NVMe 1.2.1 already provided User Data Erase / Cryptographic Erase through Format NVM | H/P | Revision 1.2.1 §5.16 |
| TCG Opal 1.0 Rev. 1.0 (Jan. 27, 2009) states that Locking-SP Revert eradicates media encryption keys, with secure erasure of User-LBA data as the described side effect | H/P | Opal 1.0 Rev. 1.0 §5.2.2, printed p. 76; secure-erasure note is informative |
| Opal `RevertSP` with `KeepGlobalRangeKey=true` can reset/turn off the Locking SP while preserving the Global-range media key and avoiding cryptographic erase for that range | H/P | Opal 1.0 Rev. 1.0 §5.2.3, printed p. 77 |
| `security-provider lifecycle reset != cryptographic erase` | E | reconstruction from the `KeepGlobalRangeKey` counterexample |
| `media-encryption-key eradication != physical ciphertext overwrite` | E | bounded reconstruction from encrypted-storage key dependence; not a forensic-unrecoverability claim |
| NIST SP 800-88 Rev. 1 requires CE reasoning to cover all relevant key copies, wrapping-key levels, encrypted target-data areas, lifecycle key instances, and backup/escrow conditions | H/S | NIST SP 800-88 Rev. 1 §§2.6.1–2.6.3 and Appendix D; institutional guidance, not an NVMe interface contract |
| A device-local CE event automatically sanitizes backed-up or escrowed key copies outside the device | X | contradicted by SP 800-88 Rev. 1 §2.6.3 and Appendix D |
| `one local MEK sanitized != every decryptability path retired` | E | reconstruction from NIST all-copies, wrapping-key, escrow/backup, and lifecycle conditions |
| `logical deallocation != physical/media erasure` | E | reconstruction from permitted deallocated-read semantics and sanitize scope |
| `forgetting user data can require retaining sanitization state` | E/I | reconstruction from background operation + status contract |
| NVMe 1.3 invented secure erase, sanitization, crypto erase, or deallocation | X | contradicted by 1.2.1, NIST prior vocabulary, and NVMe's own ATA/SCSI comparison |
| Every NVMe 1.3 product implements every sanitize action and perfectly purges all hidden media | X | not established by an optional standard interface; requires implementation/compliance evidence |

## Sources

### Primary

- NVM Express, **NVM Express Revision 1.3**, May 1, 2017, ratified April 26, 2017. Especially §5.24 `Sanitize command`, §6.7 / §6.7.1.1 `Dataset Management / Deallocate`, and §8.15 `Sanitize Operations`: <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>.
- NVM Express, **NVM Express Revision 1.2.1**, June 2016. Especially §5.16 `Format NVM` secure-erase semantics: <https://nvmexpress.org/wp-content/uploads/NVM_Express_1_2_1_Gold_20160603-1.pdf>.

### Institutional prior-art / release context

- NVM Express, **“NVMe Revision 1.3 Expands Reach of Fast Storage for Enterprise, Client, and Cloud Power Users”** (2017), identifying Sanitize among the Revision-1.3 additions: <https://nvmexpress.org/nvme-revision-1-3-expands-reach-of-fast-storage-for-enterprise-client-and-cloud-power-users/>.
- NIST, **SP 800-88 Rev. 1, Guidelines for Media Sanitization**, final December 17, 2014; historical Revision 1 withdrawn September 26, 2025 and superseded by Revision 2. Inspected §§2.6.1–2.6.3 and Appendix D for CE coverage, key hierarchy/wrapping, lifecycle, escrow/backup, multi-MEK scope, and error handling: <https://csrc.nist.gov/pubs/sp/800/88/r1/final>; archived PDF: <https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-88r1.pdf>.

## Related repository check

`tmzncty/computing-archaeology` was searched before writing for `NVMe sanitize`, `secure erase`, `deallocate`, `TRIM`, SSD sanitization, and during this deepening for `cryptographic erase`, `Opal`, `key destruction`, `wrapping key`, and `key escrow`. No dedicated retention/sanitization or key-hierarchy case was found. Generic SSD/Flash/SED and cryptographic-storage implementation history therefore remains routed there, while this case keeps the retention-specific distinction among logical deallocation, material embodiments, key-mediated recoverability, sanitization mechanisms, and sanitization-completion evidence.
