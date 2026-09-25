# Case 111 — Linux NVMe HIR host-tooling adoption and wait-policy boundary

**Case:** 111 — Enterprise SSD extended-shutdown maintenance  
**Maturity effect:** none; Case 111 remains `grounded`  
**Slice:** standards capability -> open-source host tooling -> device-adoption boundary  
**Inspected:** 25 September 2026

## Question

NVMe 2.1 gives Host-Initiated Refresh (HIR) a public capability bit, recommended interval, nominal duration, live percentage, and terminal Device Self-test result.

A separate question is whether ordinary host tooling actually exposes and consumes those fields in a way that should be treated as evidence of a shipping device implementation or of HIR-specific completion semantics.

This packet tests only that boundary.

## Sources

### Primary standard

1. NVM Express, **NVM Express Base Specification, Revision 2.1**, ratified 5 August 2024, especially Host-Initiated Refresh / TP4058:
   - https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.1-2024.08.05-Ratified.pdf

### Primary open-source implementation history

2. linux-nvme/libnvme commit `5011a3f8d92e8d9a558ceea39d42f4f9c15e3883`, committed 6 December 2024, **"types: Update id-ctrl field based on NVMe 2.1 spec"**:
   - https://github.com/linux-nvme/libnvme/commit/5011a3f8d92e8d9a558ceea39d42f4f9c15e3883

   The commit adds Identify Controller fields `rhiri` and `hirt` and documents them as Recommended Host-Initiated Refresh Interval and Host-Initiated Refresh Time.

3. linux-nvme/libnvme commit `4ef59f47ea2afec249984e192a1ff6a9046af0b9`, committed 20 December 2024, **"types: add enum for the fields added in TP4058"**:
   - https://github.com/linux-nvme/libnvme/commit/4ef59f47ea2afec249984e192a1ff6a9046af0b9

   The commit adds the `HIRS` support bit to Device Self-test Options and adds self-test code `3h` for Host-Initiated Refresh.

4. linux-nvme/nvme-cli commit `5f3a369c9c8bca3fc1737c5c4d43ac7d3a83269b`, committed 9 January 2025, **"nvme: add the new Self-test Code of Device Self-test command"**:
   - https://github.com/linux-nvme/nvme-cli/commit/5f3a369c9c8bca3fc1737c5c4d43ac7d3a83269b

   The commit adds command/result presentation for HIR and explicitly names TP4058 / Environmental Extremes Management.

### Current source inspected on 25 September 2026

5. libnvme current `types.h` at inspected commit `01ede320a30ef2094ab4d3fb072cea64f6bf6ecc`:
   - https://github.com/linux-nvme/libnvme/blob/01ede320a30ef2094ab4d3fb072cea64f6bf6ecc/src/nvme/types.h

6. nvme-cli current `src/nvme-cmds-sanitize.c` at inspected commit `c32e0fbffcb38638574de685d5f987f8179dd67c`:
   - https://github.com/linux-nvme/nvme-cli/blob/c32e0fbffcb38638574de685d5f987f8179dd67c/src/nvme-cmds-sanitize.c

7. nvme-cli current stdout / JSON presentation at the same inspected commit:
   - https://github.com/linux-nvme/nvme-cli/blob/c32e0fbffcb38638574de685d5f987f8179dd67c/src/nvme-print-stdout.c
   - https://github.com/linux-nvme/nvme-cli/blob/c32e0fbffcb38638574de685d5f987f8179dd67c/src/nvme-print-json.c

## Historical record

### 1. Host-visible HIR support landed in stages after NVMe 2.1 ratification

The public implementation history is not one atomic event.

On 6 December 2024, libnvme added the NVMe-2.1 Identify Controller fields:

```text
RHIRI
    Recommended Host-Initiated Refresh Interval

HIRT
    Host-Initiated Refresh Time
```

On 20 December 2024, libnvme added the TP4058 Device Self-test Options support bit and operation code:

```text
HIRS
    Host-Initiated Refresh Support

STC = 3h
    Host-Initiated Refresh
```

On 9 January 2025, nvme-cli added HIR to its Device Self-test command/result presentation.

This establishes a bounded public host-tooling adoption sequence after the 5-August-2024 NVMe-2.1 ratification date.

It does **not** establish when any SSD vendor first shipped HIR-capable firmware.

### 2. Current nvme-cli can expose capability-adjacent HIR fields

At the inspected 2026 source state, nvme-cli prints:

- the HIRS capability in verbose Device Self-test Options decoding;
- `rhiri`;
- `hirt`;
- HIR as Device Self-test code `3h`;
- HIR in Device Self-test result presentation.

The CLI also accepts `--self-test-code=3` and reports `Host-Initiated Refresh started` after successful submission.

Therefore ordinary host tooling can represent the standard's HIR control/observability vocabulary.

### 3. The generic wait loop was not rewritten into a HIR-specific policy

The current nvme-cli `wait_self_test()` path is shared with Device Self-test generally.

It:

1. reads Identify Controller;
2. derives its no-progress wait threshold from `edstt` (Extended Device Self-test Time);
3. polls the Device Self-test log once per second;
4. watches the generic `completion` percentage;
5. treats the return to zero after prior observed progress as the end of the running episode.

In the inspected source, the wait loop does **not** use `hirt` when choosing its threshold, and it does not inspect the newest terminal result in order to decide success/abort semantics before returning from the wait loop.

This is a source-level observation about the current host tool, not a claim about controller firmware.

### 4. libnvme's current-operation enum remains less HIR-specific than its command/result enums

Current libnvme has:

```text
NVME_ST_CODE_HOST_INIT = 0x3
NVME_DST_STC_HOST_INIT = 0x3
```

but the inspected `enum nvme_st_curr_op` lists `NOT_RUNNING`, `SHORT`, `EXTENDED`, `VS`, and `RESERVED` without a named HIR current-operation constant.

The raw `current_operation` byte remains available, so this omission does not prevent software from observing a numeric `3h` value. It does, however, show that public host-library taxonomy can lag or differ across adjacent parts of one standard feature.

Do not inflate this into a controller-level interoperability claim.

## Engineering reconstruction

The implementation history supports a useful separation:

```text
standard defines HIR
    != host library has typed fields
    != command-line tool can invoke HIR
    != tool has HIR-specific waiting policy
    != a named device advertises HIR
    != that device successfully completes HIR
```

The host side itself therefore has several distinct evidence layers:

```text
schema adoption
    -> capability decoding
    -> operation submission
    -> live progress polling
    -> terminal-result interpretation
    -> product-specific trace
```

A tool can reach the middle of this chain without supplying evidence for the last step.

### HIRT exposure versus HIRT use

The current implementation yields another narrow anti-collapse:

```text
HIRT is visible to host software
    != generic wait policy is parameterized by HIRT
```

This matters because field availability and policy use are separate retained relations. A value may be carried through a public interface yet remain unused by one consumer's control loop.

No claim is made here that `edstt` is necessarily unsafe for every HIR device. The source proves only that the inspected wait path is generic and does not consume `hirt`.

### Progress observation versus terminal authority

The generic wait loop primarily watches the current percentage.

The standard-level Case-111 evidence already distinguishes live percentage from terminal Self-test Result Data Structures. Combining the two gives:

```text
progress became observable
    != terminal outcome was interpreted by the waiting helper

wait helper returned
    != future offline-retention guarantee
```

This is an implementation-boundary observation, not a finding that nvme-cli violates the NVMe specification.

## Functional analogy

A limited analogy to eMMC BKOPS is useful only at the host-observability layer:

```text
public maintenance control exists
    -> host tooling can expose some controls/status
    -> consumer policy may still be more generic than the maintenance class
```

No protocol genealogy or firmware-mechanism identity is implied.

## Philosophical interpretation

A narrow retention point survives the technical inspection:

> Public observability is itself layered. Making a maintenance state nameable in a standard, representable in a library, printable by a tool, and actionable in an operator workflow are separate acts.

This does **not** imply that technical state becomes real only when software names it. The controller operation may exist independently of host tooling; the point is only that practical authority depends on which relations the host can actually identify and consume.

## Anti-collapse rules added by this slice

```text
standard feature
    != host-tool support

host-tool support
    != named-device adoption

RHIRI/HIRT printed
    != HIR supported by the attached device unless capability evidence agrees

HIR command accepted
    != HIR operation completed

live percentage polled
    != terminal result interpreted

HIRT exposed
    != HIRT used by the generic wait policy

typed command/result enum
    != every adjacent library enum is equally HIR-specific
```

## What this closes

Boundedly closed:

- whether mainstream Linux NVMe userspace acquired explicit HIR vocabulary after NVMe 2.1: **yes**;
- whether nvme-cli can submit HIR and display HIR-related Identify/result fields: **yes**;
- whether this host-tool adoption by itself proves a shipping SSD implements HIR: **no**;
- whether the inspected generic wait path is visibly parameterized by HIRT: **no**.

## What remains open

This slice does **not** close Case-111 P1.

Highest-value remaining evidence:

1. a first-party named shipping NVMe SSD that explicitly advertises HIR or exposes `HIRS=1`;
2. its exact `RHIRI` and `HIRT`;
3. a real successful HIR trace with current percentage and terminal result;
4. a reset/abort trace on that same device;
5. preferably a vendor statement tying the operation to the product's offline-retention maintenance contract.

A lower-priority host-tooling follow-up would be to determine whether later libnvme/nvme-cli commits add a named HIR current-operation enum or HIRT-aware wait behavior.

## Related-repository boundary

Fresh searches in `tmzncty/computing-archaeology` for `Host-Initiated Refresh`, `RHIRI HIRT`, and `NVMe extended self-test reset` found no dedicated packet.

Broad libnvme/nvme-cli evolution, NVMe feature-adoption history, distro packaging, and command-line UX belong primarily in `computing-archaeology` if expanded. Case 111 retains only the retention-specific observability and authority boundary.
