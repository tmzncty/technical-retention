# NVM Express 1.3 Deallocate and Sanitize: Logical Forgetting, Media Sanitization, and Completion State

## Status

**`grounded`** — bounded to the NVM Express 1.3 interface semantics for Dataset Management `Deallocate` and `Sanitize`, with NVM Express 1.2.1 `Format NVM` secure-erase semantics used as the immediate prior-version boundary. The case asks what the interface means when a host says that a logical range is no longer needed, versus when it requests that prior user data be made unavailable across the NVM subsystem.

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

## Broader prior art boundary

Media-sanitization vocabulary and cryptographic erasure also predate NVMe 1.3. NIST SP 800-88 Rev. 1 was finalized in December 2014 and defines media sanitization as rendering access to target data infeasible for a stated level of effort; its keyword set includes `crypto erase` and `secure erase`.

This source is used only to block an invention-priority shortcut. It does **not** imply that NVMe 1.3 simply copied NIST's taxonomy or that the interface semantics are reducible to the policy document.

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
- NIST, **SP 800-88 Rev. 1, Guidelines for Media Sanitization**, final December 17, 2014: <https://csrc.nist.gov/pubs/sp/800/88/r1/final>.

## Related repository check

`tmzncty/computing-archaeology` was searched before writing for `NVMe sanitize`, `secure erase`, `deallocate`, `TRIM`, and SSD sanitization. No dedicated retention/sanitization case was found. Generic SSD/Flash engineering history therefore remains routed there, while this case keeps the retention-specific distinction among logical deallocation, material embodiments, sanitization mechanisms, and sanitization-completion evidence.
