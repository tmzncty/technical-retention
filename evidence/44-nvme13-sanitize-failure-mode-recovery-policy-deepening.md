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

- `AUSE = 0` selects **restricted** completion mode;
- `AUSE = 1` selects **unrestricted** completion mode;
- `AUSE` is ignored when the requested Sanitize Action is `Exit Failure Mode`.

The bit does not select Block Erase versus Crypto Erase versus Overwrite. `SANACT` selects the sanitize action; `AUSE` selects a policy that later matters if the operation fails.

> **sanitize mechanism choice != sanitize-failure recovery policy**

## Historical record 2 — restricted and unrestricted failures have different legal exits

Revision 1.3 distinguishes two failure regimes.

If the most recent failed sanitize was started in **unrestricted** mode, failure recovery may use a subsequent Sanitize command in restricted or unrestricted completion mode, or a subsequent Sanitize command with the `Exit Failure Mode` action.

If the most recent failed sanitize was started in **restricted** mode, failure recovery requires a subsequent Sanitize command in **restricted** completion mode. Before such a new sanitize operation is started, a subsequent `Exit Failure Mode` command or a subsequent Sanitize command issued in unrestricted completion mode is aborted with **`Sanitize Failed`**.

That exact status matters: `Invalid Field in Command` is used elsewhere for an unsupported sanitize operation type; it is not the status specified for these disallowed exits from a restricted failure state.

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

Engineering reconstruction:

> **retained initiating policy can constrain future recovery authority**.

That sentence is project vocabulary, not wording used by the NVMe authors.

## Historical record 3 — command rejection is not sanitize-operation failure

Revision 1.3 separately defines what happens when the **Sanitize command itself does not complete successfully**. If the controller does not complete the command with `Successful Completion`, it shall not start the sanitize operation for that command, shall not modify the Sanitize Status log page, and shall not alter user data as a result of that rejected command.

That is materially different from an accepted command whose background sanitize later fails.

```text
command rejected before operation start
    !=
operation accepted and in progress
    !=
operation later failed
    !=
failed-state recovery completed
```

An unsuccessful command submission is therefore not evidence that a destructive sanitize ran partially or that the subsystem entered sanitize failure mode.

## Historical record 4 — the status log retains terminal state and initiating-command context

The Revision-1.3 **Sanitize Status** log is global to the NVM subsystem and is retained across power cycles and resets. Its `SSTAT` field distinguishes states including:

- no sanitize operation has ever been completed;
- the most recent sanitize completed successfully;
- a sanitize operation is in progress;
- the most recent sanitize failed.

The log also contains `SCDW10`, the command dword 10 of the Sanitize command that started the operation whose status is reported. Because command dword 10 contains `SANACT` and `AUSE`, later operation status remains associated with the launch parameters that created the operation.

> **retained terminal status + retained initiating parameters != generic “last command failed” telemetry**

The specification does not state where a controller physically stores this state. This case therefore makes no claim that `SSTAT` or `SCDW10` must exist as a byte-identical NAND record.

## Historical record 5 — failure-state exit restores admissibility, not erasure proof

`Exit Failure Mode` is a Sanitize Action used in the unrestricted recovery path; it is not Block Erase, Crypto Erase, or Overwrite.

The Sanitize Status log separately defines **Global Data Erased (`GDE`)** in relation to manufacture and the most recent **successful sanitize operation**, and tracks whether nonvolatile storage has subsequently been written.

A conservative boundary is therefore:

> **successful Exit Failure Mode != evidence that a sanitize operation successfully erased prior user data**

and:

> **restored command admissibility != erasure assurance**

This does not assert a device-specific `GDE` transition after every Exit Failure Mode implementation. It states only that service-state recovery must not be promoted into proof that a successful Block Erase, Crypto Erase, or Overwrite operation completed.

## Historical record 6 — sanitize failure changes ordinary command admissibility

After a sanitize operation fails, controllers in the NVM subsystem abort commands not allowed during a sanitize operation with status **`Sanitize Failed`** until either a subsequent sanitize operation is started or successful recovery from the failed sanitize occurs.

The failure therefore leaves behind more than a historical event record:

```text
past maintenance outcome
    -> retained control state
    -> present command-admission policy
```

The point is not that every command is blocked identically or that failure destroys payload. The point is that a past failed forgetting attempt remains operationally authoritative until an allowed recovery transition changes the state.

## Operational witness — Seagate openSeaChest keeps the distinction explicit

Seagate's current openSeaChest erase help exposes `--ause` for NVMe sanitize and describes the default as **restricted** failure-exit behavior. With `--ause`, the tool exposes the **unrestricted** path in which `Exit Failure Mode` is an additional recovery option.

The project's `openSeaChest_Erase` version history records, for **v4.6.0 (28-Aug-2024)**, a sanitize-handling refactor, addition of an option to run sanitize in unrestricted mode, and improved handling of an existing sanitize-failure condition by continuing/retrying sanitize rather than immediately exiting it.

This is an operational/tooling witness only. It does not prove that every Seagate SSD, every NVMe SSD, or any named firmware build exhibits a particular failure under test.

## Engineering reconstruction

The sourced interface can be decomposed into four distinct state classes:

| Layer | Example state | What it governs |
| --- | --- | --- |
| launch policy | `AUSE=0/1`, `SANACT` | what operation starts and what failure exits may later be legal |
| runtime maintenance | sanitize in progress | background work and ordinary-service restrictions |
| terminal outcome | success / failure | whether the intended operation completed and whether failure mode exists |
| recovery authority | retry-only vs retry-or-exit | which transitions may restore ordinary command admissibility |

The useful technical-retention relations are:

```text
operation-start policy != runtime progress != terminal outcome
terminal outcome != recovery authority
command rejection != sanitize-operation failure
failure-mode exit != successful sanitization
service recovery != sanitization verification
retained initiating policy -> constrains later recovery transitions
```

This is an analytical decomposition of interface-visible obligations, not a claim that every controller implements four literal internal objects.

## Cross-case comparison

### Case 47 — FAST '11 SSD sanitization verification

Case 47 supplies implementation/empirical evidence about whether hidden Flash state was actually sanitized. Case 44 supplies a standards-level control-state boundary.

```text
NVMe failure-state exit / service restoration
    !=
empirical evidence that hidden physical embodiments were sanitized
```

There is no genealogy claim from the FAST '11 paper to NVMe 1.3.

### Case 148 — NVMe Device Self-test reset-surviving maintenance

Case 148 shows another NVMe 1.3-era background maintenance operation whose lifecycle is not reducible to the initiating command. Both cases therefore warn against `command completion == maintenance completion`.

The mechanisms remain different: Sanitize has destructive/forgetting scope and a dedicated failure-mode admission policy; Device Self-test has its own result/resume/abort semantics. Functional similarity does not establish shared implementation lineage.

## Philosophical interpretation — downstream of the engineering record

A narrow project-level interpretation is that a system can preserve **a constraint on future action** even when the maintenance action that created the constraint has failed.

Here the retained thing of interest is not user payload. It is a relation of authority: a past launch policy plus a later failure determines which future recovery transitions are admissible.

That interpretation is not historical NVMe vocabulary and must not be used as evidence about the intentions of the standards authors.

## Explicit non-claims

This deepening does **not** establish:

1. that NVMe 1.3 invented restricted/unrestricted sanitize failure recovery;
2. that May 1, 2017 is the invention date of the mechanism;
3. that every NVMe 1.3 controller implements Sanitize or every optional sanitize action;
4. that every shipping controller correctly persists the required status across real power failures;
5. that `AUSE` selects an erase algorithm;
6. that `Exit Failure Mode` physically erases, overwrites, or cryptographically severs prior user data;
7. that exiting failure mode sets `GDE` or proves `GDE=1` on every implementation;
8. that an unsuccessful Sanitize command implies a partially executed sanitize operation;
9. that the Sanitize Status log is physically stored in ordinary NAND user blocks or in any specific medium;
10. that a retained status record is adequate sanitization verification;
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
