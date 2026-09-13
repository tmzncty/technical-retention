# Case 55 deepening — OCP 2024 Available-Spare EOL and Read-Only transition

## Status

**Bounded deepening complete.** This record adds a later datacenter-profile witness to Case 55's existing NVMe SMART / Health spare-capacity analysis. It closes one narrow ROADMAP gap at the interface-policy level: a standards profile can bind host-visible spare telemetry to an explicit service-mode transition while still keeping warning, nominal endurance consumption, host-write continuation, and residual read-preservation reserve distinct.

It does **not** establish a universal NVMe controller algorithm, a named shipping drive's fault-injection behavior, the physical topology of an FTL replacement pool, or the first historical appearance of this policy.

Parent case: [`../cases/55-nvme-smart-health-endurance-telemetry.md`](../cases/55-nvme-smart-health-endurance-telemetry.md).

Earlier grounding: [`55-nvme10-13-smart-health-endurance-grounding.md`](55-nvme10-13-smart-health-endurance-grounding.md).

## Research question

Case 55 already grounds a 2011 NVMe interface distinction:

```text
remaining spare capacity
        -> threshold warning
        -> possible exhaustion-related write failure
```

The base specification does not require every controller to traverse one deterministic end-of-life state machine. This deepening asks a narrower later question:

> Can a datacenter SSD profile make `Available Spare` an explicit control boundary for continued host writes, and if so, does `0%` mean literal physical exhaustion of every spare block?

## Source and provenance

The primary source is the Open Compute Project **Datacenter NVMe SSD Specification, Version 2.6 (`09252024`)**, whose cover identifies the version as **25 September 2024** and lists contributors from Meta, Microsoft, HPE, Dell Technologies, and Google.

The directly inspected official PDF is used chiefly at:

- §8.4 `End-of-Life (EOL)`, especially requirements `EOL-1`, `EOL-4`, `EOL-5`, `EOL-6`, `EOL-7`, and `EOL-8`, printed/PDF pp. 160–161;
- the existing Case 55 NVMe 1.0 primary record supplies the earlier generic-interface counterpoint rather than being silently rewritten by the later OCP profile.

This source establishes a **2024 public profile contract**. It is not used to claim that the policy was invented in 2024, first shipped in 2024, or absent from earlier OCP/cloud-SSD revisions or vendor firmware.

## Historical record

### OCP separates endurance EOL from the later write-service cutoff

`EOL-1` defines the profile's endurance end-of-life boundary as the earlier of two conditions: the specified Total Bytes Written has been surpassed, or the nonvolatile-media endurance limit has been reached, with NAND cycling making a block unwritable given as an example.

That definition is not itself the same as an immediate read-only transition. `EOL-4` separately requires the device to continue operating in read/write mode until the condition in `EOL-5` is reached, unless another error independently prevents continued read/write operation.

The profile therefore keeps at least these relations distinct:

```text
endurance qualification / EOL condition
        !=
current ability to continue host writes
        !=
read-only service transition
```

### `Available Spare = 0%` is a policy/reporting boundary, not literal zero physical spares

`EOL-5` requires the device to switch to **Read Only Mode (ROM)** when the SMART / Health Information `Available Spare` field reaches `0%`. The requirement defines that `0%` as the condition in which there are insufficient spare blocks to support **Host writes**.

Crucially, the same requirement says the field shall report `0%` **before** all available spare blocks have actually been exhausted. The reason is explicit: enough spare blocks must remain to handle blocks that go bad during read operations.

This is a strong negative control against a superficially obvious interpretation:

> **reported `Available Spare = 0%` != literally no physical spare blocks remain**.

The interface value is therefore a service-policy boundary tied to the adequacy of reserve for continued writes, while some reserve may intentionally remain for preserving read service under later defects.

### Warning, read-only transition, and critical-warning bits are separate states

`EOL-5` also requires different SMART / Health warning behavior around the transition:

- when `Available Spare` falls below `Available Spare Threshold`, Critical Warning bit 0 is set and a SMART / Health Status event is generated when the event is enabled and an Asynchronous Event Request is outstanding;
- when the device enters ROM because `Available Spare` reaches `0%`, Critical Warning bits 2 and 3 are set.

The profile therefore does not collapse the low-spare warning into the final host-write cutoff:

```text
Available Spare < threshold
        -> warning / event
        !=
Available Spare = 0%
        -> Read Only Mode
```

### OCP requires a bounded warning-to-cutoff runway

`EOL-8` requires the `Available Spare Threshold` to be chosen so that, under a **worst-case write workload**, `Available Spare` does not reach `0%` for at least **three days after crossing the threshold**.

This is not a universal SSD lifetime or replacement SLA. It is a profile-level lower bound on the warning-to-ROM runway under the stated workload assumption.

The retained telemetry thus participates in a timed operational relation:

```text
threshold crossing
        -> host-visible warning state
        -> at least three-day specified runway under worst-case write workload
        -> 0% policy boundary / ROM
```

The arrows are an **engineering reconstruction of the profile requirements**, not a claim that wear consumption is linear, that every field update occurs continuously, or that field-service replacement always happens inside this interval.

### `Percentage Used = 100%` and low-spare warning are deliberately ordered but not equated

`EOL-6` requires enough spare blocks that `Percentage Used` reaches **100% before** `Available Spare` falls below its threshold. `EOL-7` requires 1% update granularity for both `Percentage Used` and `Available Spare`.

This strengthens Case 55's earlier rejection of `Percentage Used = 100%` as a deterministic death instant. In this profile, the nominal endurance-use milestone must occur **before** the low-spare warning, which itself must precede the `Available Spare = 0%` ROM boundary by the `EOL-8` runway.

A useful bounded ordering is therefore:

```text
Percentage Used reaches 100%
        -> later low-spare threshold crossing
        -> warning runway
        -> Available Spare reports 0%
        -> Read Only Mode
```

The source does not authorize turning this into an exact physical-wear trajectory for every device.

## Engineering reconstruction

### Host-write reserve and read-preservation reserve are not the same capacity relation

The most important retention-specific result is the source's deliberate reservation of some physical spares **after** the host-visible `0%` point. Those residual spares are not sufficient, under the profile, to justify continued host writes, but they can remain useful for blocks going bad during reads.

Therefore:

> **reserve sufficient for continued host writes != reserve retained to preserve later read service**.

This is a better model than treating spare capacity as one scalar whose physical exhaustion and service exhaustion are necessarily simultaneous.

### A health field can become a normative service-control boundary without becoming the physical state itself

`Available Spare` remains a host-visible representation of reserve condition. The OCP profile gives that representation operational authority by specifying a service transition at `0%`, but it simultaneously proves that the field is **not** a literal count of physical spares because `0%` must occur before complete physical exhaustion.

Thus:

> **telemetry/control state can govern service while still being an abstraction over hidden physical state**.

and:

> **service-control authority != physical-state identity**.

### Base NVMe semantics and OCP profile policy must not be merged

The earlier Case 55 record uses the 2011 NVMe Gold specification to establish `Available Spare`, a threshold warning, and a `Write Fault` for which lack of spare locations is one possible cause. That generic interface does **not** by itself require the OCP sequence above.

The 2024 OCP source adds a profile contract:

```text
base NVMe field/status semantics
        + datacenter profile policy
        -> required warning runway and ROM transition
```

Therefore:

> **NVMe-defined field != universal NVMe end-of-life policy**.

This distinction is especially important because the OCP document is intentionally stricter than the generic interface it builds on.

## Functional comparisons

### Case 14 — SCSI defect reassignment

Case 14 grounds finite replacement capacity for disk defect reassignment. The functional comparison is that both cases make future continuation depend on finite replacement reserve.

The difference is decisive: Case 14 concerns a command/path for substituting physical sectors behind a stable LBA, while this OCP slice concerns a later host-visible SSD health field and profile-level service-mode policy. No SCSI→OCP/NVMe genealogy is asserted.

### Case 78 — raw NAND bad-block reserve

Case 78 grounds reserve blocks and bad-block exclusion at a raw-NAND/product-management layer. OCP `Available Spare` may reflect reserve pressure in an SSD, but this deepening does **not** infer that the profile exposes Case 78's exact reserve-block table, replacement granularity, or algorithm.

The comparison is only relational:

> finite physical replacement opportunity can be summarized by a higher-level service-qualification signal.

### Case 55 — retained device-health state

This deepening strengthens the parent case's central distinction. A device can retain/report evidence about the remaining conditions under which it can continue preserving and serving payload. In the OCP profile, that evidence is not merely descriptive: specific values are tied to warning and service-mode transitions.

## Explicit non-claims and stop conditions

This record does **not** establish any of the following:

1. **2024 invention priority.** Version 2.6 is a bounded public witness, not proof of first proposal, first profile revision, first firmware implementation, or first shipment.
2. **Universal NVMe behavior.** The ROM sequence is an OCP datacenter-profile requirement, not a rule inferred for every NVMe SSD.
3. **Named-device implementation compliance.** No shipping controller was power-cycled, worn to EOL, fault-injected, or independently observed traversing the sequence in this slice.
4. **Exact FTL topology.** `Available Spare` does not expose the number, location, type, or allocation algorithm of physical replacement blocks.
5. **Literal zero-spare semantics.** The source explicitly rejects that reading by requiring the reported value to reach zero before all physical spares are exhausted.
6. **Three-day device lifetime.** The three-day value is a minimum threshold-to-zero runway under a worst-case write workload, not a retention specification, warranty, field-replacement SLA, or forecast of time-to-failure under ordinary use.
7. **ROM means perfect readability.** Entering Read Only Mode does not prove every LBA remains readable, that no later read error can occur, or that all residual spares suffice under arbitrary fault growth.
8. **ROM means sanitization or immutability.** Read-only service policy is not a secure-erasure guarantee, WORM property, forensic statement, or proof that internal firmware never writes metadata.
9. **`Percentage Used = 100%` means physical media exhaustion.** The profile deliberately places the 100% milestone before low-spare warning and ROM.
10. **Direct genealogy from SCSI/raw-NAND reserve mechanisms.** Those cases are functional comparisons only.

## Roadmap effect

This slice closes the narrow **post-threshold service-progression** question at the **standards-profile contract** layer:

```text
low-spare warning
        !=
write-service cutoff
        !=
literal exhaustion of all physical spares
```

The still-open work is narrower and more empirical:

- named-controller / named-product conformance or fault-injection evidence for low-spare → ROM progression;
- earlier OCP revision/proposal chronology if first-publication history becomes important;
- implementation-specific FTL spare-pool topology and reassignment behavior;
- post-ROM read-error growth and residual-repair behavior;
- independent validation of the three-day warning runway under controlled endurance stress.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Available Spare`, OCP NVMe EOL, and the read-only spare-exhaustion boundary found no dedicated study to reuse. Broad SSD/NVMe/OCP engineering genealogy should remain there if developed; this file keeps only the retention/service-boundary relation.

## Sources

1. Open Compute Project, **Datacenter NVMe SSD Specification, Version 2.6 (`09252024`)**, 25 September 2024, cover and §8.4 `End-of-Life (EOL)`, especially `EOL-1`, `EOL-4`–`EOL-8`, pp. 160–161: <https://www.opencompute.org/documents/datacenter-nvme-ssd-specification-v2-6-2-pdf>
2. NVM Express, **NVM Express Revision 1.0 Gold**, ratified 1 March 2011, as already directly grounded in Case 55 and [`55-nvme10-13-smart-health-endurance-grounding.md`](55-nvme10-13-smart-health-endurance-grounding.md); used here only as the earlier generic-interface counterpoint.

## Evidence classification

- **Historical record (`H/P`)** — the OCP 2.6 requirements, dates, field names, warning bits, ROM transition, ordering constraints, and three-day profile requirement.
- **Engineering reconstruction (`E`)** — the decomposition of warning, host-write reserve, residual read-preservation reserve, service authority, and hidden physical capacity.
- **Functional analogy (`A`)** — bounded comparison to SCSI reassignment and raw-NAND spare capacity.
- **Philosophical interpretation (`I`)** — none required for this slice; the result is intentionally mechanism/interface focused.
