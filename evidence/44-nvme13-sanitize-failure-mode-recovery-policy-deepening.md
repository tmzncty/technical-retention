# Case 44 deepening — NVMe 1.3 Sanitize failure mode as retained recovery-policy authority

## Status

**`bounded deepening complete`** — this record isolates one narrow part of NVM Express Revision 1.3 that the parent Case 44 previously summarized only as “sanitize failure becomes a service state”: the relation among the launch-time `AUSE` policy bit, later sanitize-operation failure, the retained Sanitize Status record, and the recovery transitions that remain admissible after failure.

It does **not** claim named-controller conformance, successful physical erasure, forensic unrecoverability, or invention priority for sanitize failure handling.

Parent case: [`../cases/44-nvme13-deallocate-sanitize-forgetting.md`](../cases/44-nvme13-deallocate-sanitize-forgetting.md)

Grounding record: [`44-nvme12-13-deallocate-sanitize-grounding.md`](44-nvme12-13-deallocate-sanitize-grounding.md)

Related empirical sanitization case: [`../cases/47-fast11-ssd-sanitization-verification.md`](../cases/47-fast11-ssd-sanitization-verification.md)

## Bounded question

When an NVMe 1.3 sanitize operation fails, does the interface merely report a generic error, or does it retain enough information about the operation and its launch policy to constrain what recovery actions are allowed later?

The primary-source answer is the latter. Revision 1.3 makes the operation's initiation policy consequential after the initiating command has already completed and the background sanitize has subsequently failed.

This yields a retention relation that is easy to miss if `Sanitize` is treated as one instantaneous erase verb:

```text
accepted start command + launch policy
        -> background sanitize operation
        -> terminal failure state
        -> retained failure/status record
        -> policy-constrained recovery transitions
```

## Primary source and provenance

The main source is **NVM Express Revision 1.3**, dated May 1, 2017 and ratified April 26, 2017:

<https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>

The relevant normative surfaces are the `Sanitize` command definition, the Sanitize Status log, and §8.15 / §8.15.1 sanitize-operation and failure behavior. This record uses Revision 1.3 as an interface specification; it does not treat a standards contract as evidence that every shipping SSD implemented the contract correctly.

A later operational/tooling witness is Seagate's open-source **openSeaChest** utility. It is used only to show that the restricted/unrestricted distinction remains operationally legible in vendor-maintained tooling, not as proof of any particular controller firmware implementation:

- current pinned source: <https://github.com/Seagate/openSeaChest/blob/d2f01584f1265b899e0d84af0ded61521c822213/src/openseachest_util_options.c>
- pinned erase-tool history: <https://github.com/Seagate/openSeaChest/blob/d2f01584f1265b899e0d84af0ded61521c822213/docs/openSeaChest/openSeaChest_Erase_Version_History.txt>

## Historical record 1 — `AUSE` is a launch-time recovery-policy choice

Revision 1.3 defines `AUSE` (`Allow Unrestricted Sanitize Exit`) in Sanitize command dword 10.

At operation launch:

- `AUSE = 0` selects **restricted** sanitize completion/failure behavior;
- `AUSE = 1` selects **unrestricted** sanitize completion/failure behavior;
- `AUSE` is ignored when the requested Sanitize Action is `Exit Failure Mode`.

The bit therefore does not select Block Erase versus Crypto Erase versus Overwrite. `SANACT` selects the sanitize action; `AUSE` selects a policy governing how a later failure may be exited.

This distinction matters because the policy remains relevant after the initiating command is gone:

> **sanitize mechanism choice != sanitize-failure recovery policy**.

## Historical record 2 — restricted and unrestricted failure states have different legal exits

Revision 1.3 §8.15.1 distinguishes two failure regimes.

If a sanitize operation started in **restricted** mode fails, the NVM subsystem remains in sanitize failure mode until a subsequent sanitize operation completes successfully. In that state, a later attempt to use `Exit Failure Mode`, or to start a subsequent sanitize in unrestricted mode, is rejected with `Invalid Field` under the bounded specification text.

If a sanitize operation started in **unrestricted** mode fails, the host has a broader recovery set: it may start another sanitize operation or use the `Exit Failure Mode` Sanitize Action.

So the later recovery graph depends on an earlier policy choice:

```text
AUSE=0 at accepted operation start
    -> later failure
    -> restricted failure mode
    -> successful subsequent restricted sanitize required

AUSE=1 at accepted operation start
    -> later failure
    -> unrestricted failure mode
    -> subsequent sanitize OR Exit Failure Mode may recover service
```

This supports a precise engineering statement:

> **retained initiating policy can constrain future recovery authority**.

That sentence is project-level engineering reconstruction, not wording used by the NVMe authors.

## Historical record 3 — command rejection is not sanitize-operation failure

Revision 1.3 separately defines what happens when the **Sanitize command itself does not complete successfully**. In that case, the Sanitize Status log is not modified and user data is not modified by the rejected command.

That is a materially different state from:

1. a Sanitize command completing successfully;
2. the background sanitize operation actually starting;
3. the operation later failing;
4. the subsystem entering sanitize failure mode.

The case therefore must not collapse these events into a single `sanitize failed` label.

A safer state decomposition is:

```text
command rejected before operation start
    !=
operation accepted and in progress
    !=
operation later failed
    !=
failed-state recovery completed
```

This also blocks a common diagnostic error: an unsuccessful command submission is not evidence that a destructive sanitize ran partially or that the subsystem entered its sanitize-failure service state.

## Historical record 4 — the status log retains both terminal state and initiating command context

The Revision-1.3 **Sanitize Status** log is global to the NVM subsystem and is retained across power cycles and resets. Its `SSTAT` field distinguishes at least:

- no sanitize operation has ever been completed;
- the most recent sanitize completed successfully;
- a sanitize operation is currently in progress;
- the most recent sanitize operation failed.

The log also contains `SCDW10`, the command dword 10 of the Sanitize command that **started** the operation whose status is being reported. Because command dword 10 contains both `SANACT` and `AUSE`, the interface preserves a compact relation between later operation status and the launch parameters that created that operation.

This is stronger than merely retaining a generic progress percentage:

> **retained terminal status + retained initiating parameters > generic “last command failed” telemetry**.

The specification does not state where a controller physically stores this state. It may be implemented in controller metadata, reserved nonvolatile storage, reconstructed state, or another conforming mechanism. This case therefore makes no claim that `SSTAT` or `SCDW10` must exist as a byte-identical NAND record.

## Historical record 5 — failure-state exit restores admissibility, not erasure proof

`Exit Failure Mode` is itself a Sanitize Action. It is available only in the unrestricted failure regime described above. Its role is to exit sanitize failure mode; it is not defined as Block Erase, Crypto Erase, or Overwrite.

The Sanitize Status log separately defines **Global Data Erased (`GDE`)** in relation to manufacture and the most recent **successful sanitize operation**, and it tracks whether nonvolatile storage has subsequently been written.

Those definitions require a conservative reading:

> **successful Exit Failure Mode != evidence that a sanitize operation successfully erased prior user data**.

And:

> **restored command admissibility != erasure assurance**.

This does not assert a device-specific `GDE` transition after every Exit Failure Mode implementation. It states the narrower interface boundary: service-state recovery must not be silently promoted into proof that one of the successful sanitize mechanisms completed.

That boundary connects directly to Case 47 and later NIST assurance vocabulary: a command path becoming usable again is not empirical verification that stale physical embodiments are unrecoverable.

## Historical record 6 — sanitize failure changes ordinary command admissibility

While the NVM subsystem is in sanitize failure mode, Revision 1.3 requires commands that are not allowed in that state to be aborted with `Sanitize Failed`. The failed operation therefore leaves behind more than a historical event record: its retained state participates in the admission decision for future commands.

This gives a compact relation:

```text
past maintenance outcome
    -> retained control state
    -> present command-admission policy
```

The point is not that all commands are blocked identically or that a sanitize failure destroys payload. The point is that a past failed forgetting attempt remains operationally authoritative until an allowed recovery transition changes that state.

## Operational witness — Seagate openSeaChest keeps the restricted/unrestricted distinction explicit

Seagate's current openSeaChest erase help exposes `--ause` for NVMe sanitize and describes the default as **restricted** failure-exit behavior: after a failure, the way out is another sanitize that eventually succeeds. With `--ause`, the tool describes the **unrestricted** path, in which `Exit Failure Mode` becomes an additional recovery option.

The project's `openSeaChest_Erase` version history records, for **v4.6.0 (28-Aug-2024)**, a sanitize-handling refactor, addition of an option to run sanitize in unrestricted mode, and improved handling of an existing sanitize-failure condition by continuing/retrying sanitize rather than immediately exiting it.

This is useful operational continuity because a vendor-maintained utility still has to expose the state-machine distinction to users. It is **not** evidence that every Seagate SSD, every NVMe SSD, or any named firmware build exhibits a particular failure under test.

## Engineering reconstruction

The source-supported relation can be modeled as four separate state classes:

| Layer | Example state | What it governs |
| --- | --- | --- |
| launch policy | `AUSE=0/1`, `SANACT` | what operation starts and what failure exits may later be legal |
| runtime maintenance | sanitize in progress | background destructive/cryptographic/overwrite work and ordinary-service restrictions |
| terminal outcome | success / failure | whether the intended operation completed and whether failure mode exists |
| recovery authority | retry-only vs retry-or-exit | which transitions may restore ordinary command admissibility |

The useful technical-retention relations are therefore:

```text
operation-start policy != runtime progress != terminal outcome
terminal outcome != recovery authority
command rejection != sanitize-operation failure
failure-mode exit != successful sanitization
service recovery != sanitization verification
retained initiating policy -> constrains later recovery transitions
```

This is not a claim that NVMe internally implements four literal objects or tables. It is an analytical decomposition of distinct interface-visible obligations.

## Cross-case comparison

### Case 47 — FAST '11 SSD sanitization verification

Case 47 supplies implementation/empirical evidence that a nominal erase or sanitize interface can require independent validation against hidden Flash state. Case 44 supplies a standards-level control-state boundary.

The functional comparison is:

```text
NVMe failure-state exit / service restoration
    !=
empirical evidence that hidden physical embodiments were sanitized
```

There is no genealogy claim from the FAST '11 paper to NVMe 1.3.

### Case 148 — NVMe Device Self-test reset-surviving maintenance

Case 148 shows another NVMe 1.3-era background maintenance operation whose lifecycle is not reducible to the initiating command. Both cases therefore warn against `command completion == maintenance completion`.

But the mechanisms remain different. Sanitize has destructive/forgetting scope and a dedicated failure-mode admission policy; Device Self-test has its own result/resume/abort semantics. Functional similarity does not establish shared implementation lineage.

## Philosophical interpretation — explicitly downstream of the engineering record

A narrow project-level interpretation is that a system can preserve **a constraint on future action** even when the maintenance action that created the constraint has failed.

In this case the retained thing of interest is not user payload. It is a relation of authority:

> a past launch policy plus a later failure determines which future recovery transitions are admissible.

That may be philosophically suggestive for `technical-retention`, but it is not historical NVMe vocabulary and must not be used as evidence about the intentions of the standards authors.

## Explicit non-claims

This deepening does **not** establish any of the following:

1. that NVMe 1.3 invented restricted/unrestricted sanitize failure recovery;
2. that May 1, 2017 is the invention date of the mechanism;
3. that every NVMe 1.3 controller implements Sanitize or every optional sanitize action;
4. that every shipping controller correctly persists the required status across real power failures;
5. that `AUSE` selects an erase algorithm;
6. that `Exit Failure Mode` physically erases, overwrites, or cryptographically severs prior user data;
7. that exiting failure mode sets `GDE` or proves `GDE=1` on every implementation;
8. that an unsuccessful Sanitize command implies a partially executed sanitize operation;
9. that the Sanitize Status log is physically stored in ordinary NAND user blocks or in any specific medium;
10. that a retained status record is itself adequate sanitization verification;
11. that Seagate openSeaChest behavior proves a named SSD firmware's internal implementation;
12. that NVMe 1.4, NVMe 2.x, SCSI sanitize, ATA sanitize/security erase, or TCG Opal use an identical failure-state machine;
13. that service recovery and confidentiality-risk validation are the same operation;
14. that the specification alone proves forensic unrecoverability of hidden Flash embodiments.

## Related-repository check

`tmzncty/computing-archaeology` was checked for an existing `NVMe sanitize failure`, `Exit Failure Mode`, or equivalent dedicated technical-history slice. No overlapping module was found. A broader genealogy of storage sanitize state machines, controller implementations, or vendor firmware belongs there if developed; this file keeps only the retention-specific control-state relation.

## Remaining evidence debt

This bounded slice closes the **normative Revision-1.3 relation among `AUSE`, sanitize failure, retained status, and legal recovery transitions**. It does not close:

- exact proposal / technical-proposal genealogy for `AUSE` and `Exit Failure Mode` before Revision 1.3;
- named SSD/controller conformance under injected sanitize failure;
- measured persistence of `SSTAT` / `SCDW10` through real reset and power-loss sequences;
- real-device behavior of `GDE` around unrestricted failure and `Exit Failure Mode`;
- Linux kernel / `nvme-cli` handling of restricted versus unrestricted failed states across historical releases;
- Revision 1.3 → 1.4 → 2.x semantic evolution;
- independent post-sanitize physical-media verification, which remains a Case 47 / assurance-layer problem.

## Sources

### Primary standard

- NVM Express, **NVM Express Revision 1.3**, May 1, 2017, ratified April 26, 2017. `Sanitize` command, Sanitize Status log, and §8.15 / §8.15.1: <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>

### Vendor-maintained operational/tooling witness

- Seagate, **openSeaChest**, pinned source at commit `d2f01584f1265b899e0d84af0ded61521c822213`, sanitize help including restricted/unrestricted exit behavior and `--ause`: <https://github.com/Seagate/openSeaChest/blob/d2f01584f1265b899e0d84af0ded61521c822213/src/openseachest_util_options.c>
- Seagate, **openSeaChest_Erase Version History**, pinned at the same commit; v4.6.0 dated 28-Aug-2024 records unrestricted-mode option and failed-state handling changes: <https://github.com/Seagate/openSeaChest/blob/d2f01584f1265b899e0d84af0ded61521c822213/docs/openSeaChest/openSeaChest_Erase_Version_History.txt>
