# Synthesis 13 — Durability Handoff: Cache Residence, Persistence Domains, Power-Fail Transfer, and Recovery Qualification

## Scope

This is a **bounded cross-case engineering synthesis**, not a new historical case and not a genealogy of SCSI, ATA, NVMe, persistent memory, SSD power-loss protection, or filesystem durability.

It closes two relation-decomposition questions already present in the roadmap:

> How should `command completion`, `volatile-cache residence`, `nonvolatile-media commitment`, `cross-command ordering`, and `power-fail atomicity` be separated at storage interfaces?

and:

> How should `store execution`, processor/controller-buffer residence, `persistence-domain` arrival, synchronization completion, failure-qualified recoverability, atomicity, and ordering be separated in persistent-memory programming models?

The comparison is built from already-grounded repository cases:

- [Case 15 — Intel SSD 320 power-loss protection](../cases/15-intel-ssd320-power-loss-durability.md);
- [Case 20 — NVMe 1.0 VWC / Flush / FUA / AWUPF](../cases/20-nvme10-fua-flush-persistence-ordering.md);
- [Case 31 — SNIA NVM Programming Model v1 persistence domain](../cases/31-snia-nvm-persistence-domain-boundary.md);
- [Case 32 — Intel ADR/eADR power-fail domain](../cases/32-intel-adr-eadr-power-fail-domain.md);
- [Case 38 — Intel DC S3700/S3500 PLI self-test and validation](../cases/38-intel-dc-s3700-pli-self-test-validation.md);
- [Case 87 — SCSI-2 write-back cache / FUA / SYNCHRONIZE CACHE](../cases/87-scsi2-writeback-cache-fua-synchronize-cache.md).

Historical claims remain owned by those case/evidence records. The relation names introduced below are **project engineering vocabulary (`E`)** unless explicitly identified as period/product vocabulary. Similarity across interfaces is functional comparison, not evidence of common descent.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `write cache`, SCSI, Flush/FUA, persistence-domain, ADR/eADR, and power-loss-handoff combinations found no dedicated overlapping case in the current search surface. A broader technical history of storage-cache architecture, SCSI/ATA/NVMe command evolution, battery-backed controllers, persistent-memory platforms, or power-fail circuitry should therefore remain routed there if later developed; this synthesis keeps only the retention-specific relation decomposition.

---

## Why this synthesis is needed despite the individual cases

The individual cases already establish strong local boundaries:

- Case 87 shows that SCSI write-back `GOOD` can precede physical-medium write, while FUA and SYNCHRONIZE CACHE strengthen different scopes;
- Case 20 shows that NVMe 1.0 FUA can require one write to reach nonvolatile media before completion while explicitly supplying no implied ordering with other commands, and separately reports normal versus power-fail atomicity;
- Case 15 shows a named SSD whose recoverable state can depend on volatile temporary buffers plus a failure-triggered capacitor-backed transfer to NAND;
- Case 31 defines the historical SNIA `persistence domain` and states directly that synchronization to that domain does not itself supply atomicity or ordering and that recoverability remains failure-pattern qualified;
- Case 32 shows ADR/eADR moving a power-fail-protected boundary upstream without making ordering/fencing obligations disappear;
- Case 38 shows that the emergency-retention apparatus itself has health, recency, self-test, validation, and power-transition-envelope state.

What remained missing was a single relation map showing **where the word `durable` is still too coarse**. A request can be current, completed, cached, power-cycle-survivable, inside a persistence domain, ordered, atomic under one failure model, or later recoverable — and those predicates are neither synonyms nor guaranteed to close at the same instant.

---

## Historical records kept separate

### SCSI-2 / SBC-2 — completion, cache class, and physical medium were already distinct interface predicates

Case 87 grounds the 1994 SCSI-2 write-back rule: a device can return `GOOD` after the newest logical-block value has entered cache but before the physical medium has received it. A later medium-write failure can therefore surface as a deferred error after the original command has already completed.

The same standard supplies two stronger but differently scoped controls:

- `FUA=1` requires the addressed write to reach the physical medium before command completion;
- `SYNCHRONIZE CACHE` acts on already-pending cached state and forces the requested logical-block set to the physical medium.

The 2004 SBC-2 material then adds another historical distinction. A `non-volatile cache` may survive a power cycle while remaining weaker than the physical medium when disks are removed from the controller or when unpowered retention exceeds the cache's finite guarantee. Thus even `non-volatile` did not collapse controller dependence, physical-medium residency, and indefinite retention into one property.

This is **prior-art evidence for typed durability relations**, not proof of a direct SCSI-to-NVMe genealogy.

### NVMe 1.0 — per-command persistence, ordering, and power-fail atomicity are independent controls

Case 20 grounds the official 2011 NVMe 1.0 interface. The controller reports whether a `Volatile Write Cache (VWC)` is present; `Flush` requests a volatile-storage-to-nonvolatile-memory transition; and Write `FUA` requires the addressed data to reach nonvolatile media before that write's completion.

The specification immediately blocks a common overreading: FUA carries **no implied ordering with other commands**. Section 6.3 separately requires host software or the application to enforce ordering when independent commands need it.

The same controller-identification structure reports `AWUN` and `AWUPF` separately. Normal-operation atomicity and power-fail atomicity are therefore distinct advertised capabilities rather than one property inferred from successful writes.

NVMe 1.0 also supplies a useful interface-classification counterexample: if a controller guarantees cached data will be written to nonvolatile media when power is lost, that cache is considered nonvolatile for the VWC feature. The historical claim is about the **contract class**, not about the intrinsic material volatility of whatever cells implement the cache.

### Intel SSD 320 — a durability guarantee can depend on future work performed after power begins to fail

Case 15 supplies the named-implementation witness that the interface cases deliberately do not. Intel documents temporary user/system buffers in front of NAND, a power-fail detector, supply isolation, stored capacitance, firmware reprioritization, and transfer of temporary state into NAND after input power begins to disappear.

This means a state can be protected by a **guaranteed transition path** rather than only by already occupying the final nonvolatile medium. The capacitors are not payload. They are finite retention infrastructure that buys time for a later state transition.

The same case keeps three routes distinct:

```text
host-requested FLUSH
    !=
orderly shutdown transfer
    !=
device-triggered emergency transfer after power-fail detection
```

FAST '13 remains the independent boundary against equating an interface/manufacturer claim with measured correctness under every fault timing. The anonymized experiments cannot be projected onto the SSD 320 specifically.

### SNIA 2013 — persistence-domain arrival is a durability boundary, not atomicity, ordering, or unconditional recovery

Case 31 grounds `persistence domain` as historical SNIA vocabulary in the 2013 NVM Programming Model v1. SNIA defines `durable` through commitment to a persistence domain, while separately allowing mapped stores to remain first in processor-resident caches or memory-controller buffers.

`NVM.PM.FILE.SYNC` can close the requested range's durability relation by forcing it to the persistence domain. Yet the same source explicitly says synchronization does not itself guarantee write atomicity; optimized flush similarly supplies neither atomicity nor ordering. If interrupted, some ranges can have crossed the boundary while others have not, without a per-range completion map.

SNIA further says that data which reached a persistence domain **may** be recoverable after restart depending on whether the actual failure pattern is tolerated by the domain's design/configuration. It also permits multiple persistence domains and treats alignment with volumes/filesystems as an administrative act.

Therefore:

```text
reached the persistence domain
    !=
unconditionally recoverable under any failure
```

and:

```text
successful synchronization
    !=
atomic transaction
    !=
cross-update ordering protocol
```

### Intel ADR/eADR — expanding the protected domain changes flush obligations without erasing ordering obligations

Case 32 provides a platform implementation of persistence-domain placement. Under the sourced ADR regime, processor caches remain outside the power-fail-protected domain while memory-controller write-pending queues participate in a failure-triggered drain to persistent memory. Software therefore needs cache writeback plus the required ordering before it can rely on that protected path.

With eADR, Intel extends the power-fail-protection relation upstream into processor caches. PMDK can then omit cache-flush operations that were needed under ADR, yet Intel explicitly retains `SFENCE`. The platform also requires additional stored energy to perform the emergency drain.

This gives two useful counterexamples:

```text
larger persistence domain
    !=
no remaining software ordering obligation
```

and:

```text
power-fail protected now
    !=
already physically placed in the final persistent DIMM now
```

The second statement is an engineering reconstruction of the documented future-transfer guarantee, not Intel's historical wording.

### Intel PLI self-test — a promised emergency path and evidence that the path remains healthy are different retained states

Case 38 moves one level above the handoff mechanism. Intel's S3700/S3500 documentation records PLI self-test result, time since last test, lifetime test count, and unexpected-power-loss history as separate management state. Intel also distinguishes a partial capacitor self-test from a wider repeated hot-unplug validation campaign and gives a supply-fall-time envelope for the documented protection behavior.

The important boundary is:

```text
protection mechanism exists
    !=
recent evidence that one component/path remains ready
    !=
whole-device proof under every future fault
```

A passing capacitor test does not establish correct firmware, NAND programming, host ordering, filesystem invariants, every power waveform, or every future component state. Conversely, a failed readiness test is not identical to present user-data loss.

---

## Engineering reconstruction: twelve typed relations

The following decomposition is analytical. It is **not** asserted as one universal pipeline implemented by all block devices and persistent-memory systems.

### 1. Logical update / current value

What value is currently intended to count for the addressed object or range?

A write-back cache can already hold the newest logical value while the lower medium remains older. Currentness and lower-layer durability therefore diverge.

### 2. Operation acceptance / command or store execution

Has the host-issued write completed under its ordinary interface contract, or has a CPU store executed into the coherent memory hierarchy?

This is an operational milestone. It is not automatically a durability statement.

### 3. Intermediate residence

Where can the newest state still reside before a stronger handoff closes?

Depending on the regime this may include volatile controller cache, a nonvolatile controller cache, processor caches, memory-controller buffers, or product-specific temporary buffers. The physical substrate and the interface's durability classification must not be silently equated.

### 4. Persistence-control scope

Which explicit mechanism asks for a stronger boundary?

Examples include SCSI/NVMe FUA, SCSI SYNCHRONIZE CACHE, NVMe Flush, SNIA synchronization/optimized flush, cache-line writeback, or a clean-shutdown command. They have different target scopes and cannot be treated as interchangeable spellings of `make durable`.

### 5. Ordering relation

What relative order among several updates must be established for the higher-level state to be crash-admissible?

NVMe 1.0 directly states that FUA does not imply ordering with other commands. SNIA directly states that persistence synchronization does not supply a general ordering guarantee. Intel eADR retains `SFENCE` even after expanding the protected domain.

Ordering is therefore its own retained/control relation.

### 6. Persistence-boundary arrival / qualification

Has the update reached the boundary that the selected interface/platform is willing to call persistent or durable for the stated purpose?

For SCSI FUA the historical destination is the physical medium. For NVMe 1.0 FUA it is nonvolatile media. For SNIA it is a persistence domain. For ADR/eADR the protected domain can include state that still awaits a future failure-triggered drain.

The noun naming the boundary is regime-specific.

### 7. Failure model / protected envelope

Which interruption is the durability claim meant to survive?

Power cycle, sudden input-power loss, ordinary reset, controller replacement, medium removal, extended shutdown, system restart, corruption, and complete device failure are different events. SCSI nonvolatile cache, SNIA persistence domains, ADR/eADR, and Intel PLI all show that a guarantee must be read against a specific failure envelope.

### 8. Failure-triggered transfer capability

If the protected state has not yet reached its final medium, what mechanism guarantees that it will cross during the failure event?

Intel SSD 320 PLI and ADR/eADR supply concrete examples: detection, energy reserve, queue/cache drain, firmware/hardware transfer, and eventual nonvolatile placement.

This relation can make physically volatile intermediate state count as power-fail protected without changing the cells' intrinsic material volatility.

### 9. Retention-infrastructure readiness

Is there current evidence that the future-transfer apparatus is still capable of doing its job?

Case 38 shows why this deserves a separate type. Capacitor-test result, recency, event history, power-transition envelope, and whole-device validation are different evidence layers.

### 10. Atomicity under the relevant interruption

If interruption occurs during an update, what granularity is guaranteed to be all-old or all-new rather than torn/intermediate?

NVMe's distinct AWUN/AWUPF and SNIA's separate interrupted-store-atomicity capability demonstrate that durability-boundary arrival and power-fail atomicity are not synonyms.

### 11. Post-failure recoverability / admissibility

After restart, can the intended state actually be reconstructed and admitted as current under the failure that occurred?

SNIA makes recoverability conditional on the domain's tolerated failure pattern. SSD/controller cases also require coherent payload plus necessary mapping/system state. Durable bits without recoverable interpretation/currentness are insufficient.

### 12. Higher-layer crash consistency / closure

Do the set of individually persistent updates satisfy the filesystem/database/application invariant that motivated durability in the first place?

This synthesis deliberately stops short of claiming that Flush/FUA/SYNC provide filesystem atomicity or transaction semantics. Case 16 already demonstrates a higher layer where dependency ordering and explicit `fsync` closure must compose with lower-layer persistence controls rather than be replaced by them.

---

## Compact relation map

```text
logical update / newest intended value
        ↓
ordinary command completion or store execution
        ↓
possibly remains in cache / processor / controller buffer
        ↓
explicit persistence control with a defined scope
        +
required cross-update ordering relation
        ↓
reaches or is qualified inside the relevant persistence boundary
        +
covered failure model is specified
        ↓
if needed: failure-triggered transfer path remains ready
        ↓
power-fail / restart atomicity conditions apply
        ↓
post-failure recovery establishes an admissible current state
        ↓
higher layer decides whether its multi-write invariant is closed
```

This is a diagnostic checklist, not one historical architecture. A SCSI disk, NVMe controller, mapped persistent-memory platform, and capacitor-backed SSD do not traverse identical components, command sets, or failure semantics.

---

## Cross-case matrix

| Relation | SCSI Case 87 | NVMe 1.0 Case 20 | SSD 320 Case 15 | SNIA Case 31 | ADR/eADR Case 32 | PLI validation Case 38 |
| --- | --- | --- | --- | --- | --- | --- |
| ordinary completion weaker than final medium | explicit under write-back | generic completion not silently media persistence | temporary buffers exist before NAND handoff | store execution can precede domain arrival | CPU store can remain in cache/WPQ | not main slice |
| stronger persistence control | FUA / SYNCHRONIZE CACHE | FUA / Flush | Flush, clean shutdown, emergency transfer | SYNC / optimized flush | cache writeback + fence; domain-specific | test/management controls, not payload flush |
| interface boundary | physical medium; later nonvolatile-cache option | nonvolatile media; VWC classification | NAND target plus product transfer path | `persistence domain` | ADR/eADR protected domain | PLI readiness/validation envelope |
| cross-operation ordering | not generalized here | explicitly host/application responsibility | outside product brief's full contract | sync does not guarantee order | SFENCE remains under eADR | outside main slice |
| power-fail atomicity | separate historical issue | AWUN vs AWUPF | implementation must preserve coherent state; not an AWUPF definition | interrupted-store atomicity separately discoverable | not reduced to domain inclusion | validation checks shorn/unserialized writes separately |
| failure-triggered future transfer | possible controller-specific NVC semantics, not one mechanism | cache may be interface-nonvolatile if guaranteed drain | explicit capacitor-backed NAND transfer | abstract domain; implementation open | explicit ADR/eADR drain relation | readiness evidence for such a path |
| guarantee qualification | controller/media dependency and finite NVC retention | interface contract + advertised capabilities | manufacturer path claim vs independent fault evidence | failure pattern + domain configuration | covered platform power-fail regime + stored energy | self-test ≠ whole-device proof |

The matrix is `A/E`: it compares separately grounded mechanisms at the relation level and does not imply one lineage.

---

## Findings

### E — command completion ≠ durable media commitment

SCSI-2 gives the direct historical counterexample, and NVMe 1.0 preserves the need for stronger Flush/FUA semantics. `Completed` must be read under the applicable cache and command contract.

### E — newest/current cached state ≠ lower-medium currentness

A write-back cache can hold the newest logical value while the physical medium still contains the predecessor. Currentness can temporarily live above the durable destination.

### E — FUA per-command persistence ≠ global ordering

NVMe 1.0 makes the separation explicit. One write can be required to reach nonvolatile media before its own completion while relative ordering with other independent commands remains the host/application's responsibility.

### E — Flush / synchronization completion ≠ atomicity

SNIA's mapped-persistence model says successful synchronization can establish persistence-domain arrival without supplying write atomicity. NVMe's separate AWUPF capability independently shows why durability and interruption atomicity need different evidence.

### E — normal atomicity ≠ power-fail atomicity

AWUN and AWUPF are separately reported in NVMe 1.0. A system cannot infer the failure-time atomic unit from the normal-operation unit merely because both refer to the same namespace/controller.

### E — nonvolatile interface classification ≠ final physical-medium residency

SBC-2's nonvolatile cache and NVMe 1.0's power-loss-guaranteed cache show that an interface can classify intermediate state by survival/transfer contract rather than by already occupying the final medium. Such state can still depend on controller infrastructure or a bounded retention interval.

### E — persistence-domain arrival ≠ unconditional recoverability

SNIA directly conditions later recovery on whether the actual failure pattern falls inside the domain's tolerated design/configuration. `Durable` therefore needs a named failure boundary.

### E — persistence-domain expansion ≠ disappearance of software ordering obligations

Intel eADR can remove cache-flush work needed under ADR while retaining `SFENCE`. Moving the hardware-protected boundary changes one obligation without turning multi-update crash consistency into an automatic property.

### E — power-fail-protected state ≠ state already in its final nonvolatile embodiment

SSD 320 PLI and ADR/eADR both permit protection to depend on a future transfer performed when power begins to fail. The guarantee is relational: protected intermediate state plus a qualified transition path plus enough energy/control to complete it.

### E — emergency-transfer path existence ≠ verified readiness

Case 38's PLI self-test state makes readiness itself maintained evidence. Installing capacitors and firmware once is weaker than having current evidence that the protection path remains within its intended capability.

### E — passing component self-test ≠ whole-device fault-survival proof

Intel separately documents partial capacitor self-test and broader repeated power-loss validation. The former cannot be promoted into proof of every controller, NAND, firmware, host-ordering, or power-waveform failure.

### E — failure-triggered handoff ≠ host-requested flush ≠ orderly shutdown transfer

Case 15 keeps all three routes distinct. They may converge on the same nonvolatile destination while differing in trigger, available time, energy source, control authority, and error observability.

### E — power-cycle survival ≠ controller/media independence

SBC-2's nonvolatile-cache discussion supplies the counterexample: state can survive a power cycle in controller cache yet still need migration to the physical medium before disks are detached or controller-local support disappears.

### E — lower-layer persistence ≠ higher-layer crash consistency

Individually persistent writes can still violate a filesystem/database dependency if ordering or grouping is wrong. Device persistence controls must compose with the higher layer's own closure protocol.

### E — durability-handoff synthesis ≠ one universal pipeline or historical genealogy

SCSI cache commands, NVMe namespace commands, Intel SSD PLI, SNIA mapped persistent memory, ADR/eADR, and PLI health telemetry are historically and mechanically distinct. The synthesis contributes a controlled vocabulary for comparison, not a claim that one mechanism evolved directly into the next.

---

## Relationship to nearby cases and syntheses

### Case 16 — filesystem crash-admissibility remains above this boundary

BSD FFS soft updates demonstrates that lower-layer durability is not the same problem as making a multi-object metadata state crash-admissible. `fsync` closure, dependency ordering, and later reclamation remain filesystem-level relations that must be composed with the persistence interface.

### Synthesis 07 / 08 / 12 — repair/integrity begin after a different failure surface

The coded-recovery and integrity syntheses ask what happens once retained state is missing, suspect, or being rebuilt. Synthesis 13 asks an earlier durability question: **did the intended update cross the relevant persistence/failure boundary correctly before the interruption happened?** A later repair mechanism cannot retroactively create an update that was never durably admitted.

### Case 30 — PMR remains a different interface embodiment

NVMe PMR uses memory-mapped persistent-region and barrier semantics rather than the namespace Flush/FUA path. Its existing case remains the right place for PMR-specific details. This synthesis does not normalize all NVMe persistence into one command model.

---

## What must not be inferred

This bounded synthesis does **not** establish that:

- every command-completion model permits volatile write-back;
- FUA has identical scope/semantics across SCSI, ATA, NVMe, or later revisions;
- every Flush/SYNC primitive drains every cache in an end-to-end software stack;
- `nonvolatile cache` means one physical memory technology;
- every persistence domain is implemented by ADR/eADR;
- eADR protects registers, arbitrary CPU state, or every failure class;
- capacitors/PLI make a device immune to firmware, mapping, NAND, ordering, or integrity failures;
- successful synchronization supplies atomicity or transaction semantics;
- a manufacturer self-test is independent conformance certification;
- SCSI → NVMe → SNIA → ADR/eADR forms a direct historical genealogy.

---

## Evidence and prior-art boundary

No new invention-priority claim is made here. The historical record remains anchored in the primary/period materials already preserved by the six grounded cases and their evidence files: ANSI/T10 SCSI material, the official NVMe 1.0 specification, Intel product/design documentation, SNIA NVM Programming Model v1, and Intel ADR/eADR/PLI documentation, with FAST '13 retained only as the independent implementation-compliance boundary already scoped by Case 15.

The cross-case contribution is narrower:

> **Treat durability as a typed handoff relation whose validity depends on operation scope, intermediate residence, ordering, persistence boundary, covered failure model, transition-path readiness, interruption atomicity, and post-failure recovery — rather than as a Boolean property inferred from command completion or from the word `nonvolatile`.**

Broader command-set genealogy, controller architecture, filesystem/barrier history, named-product fault injection, battery/capacitor aging studies, power-waveform qualification, and platform-wide persistence-domain history remain open and should be coordinated with `computing-archaeology` where they become technical-history projects rather than retention-specific comparison.
