# Case 55 Evidence Deepening: Samsung PM9A3 Vendor SMART Layout and the OCP Cloud-Log Boundary

## Status

**`grounded`** for a bounded named-product telemetry-layout claim. The product-layout witness is Samsung's January 2021 **PM9A3 M.2 Datasheet, Rev. 1.0**, a Samsung-authored document preserved through a distributor/document mirror. Samsung's official **DC Toolkit 3.0 User Guide, Rev. 1.0 (October 2023)** independently names PM9A3 as a supported NVMe SSD and shows the tool's extended-SMART retrieval path. The standards/profile comparison uses the Open Compute Project **NVMe Cloud SSD Specification, Version 1.0 (03182020)**.

This record does **not** claim that every PM9A3 form factor, firmware revision, OEM customization, or later product exposes byte-for-byte identical logs. It also does not treat a vendor log-page definition as proof of the controller's hidden NAND policy, FTL implementation, read-disturb thresholds, or reset behavior beyond what the inspected field definitions explicitly state.

## Research question

Case 55 already establishes that standardized NVMe SMART/Health state can retain cumulative device history while mixing it with current/nonpersistent state. This deepening asks a narrower product question:

> When a named data-center SSD exposes several different health/telemetry log namespaces at once, what can the log-page layout itself establish about retained maintenance history, and what persistence semantics must **not** be imported from an adjacent standard or from a differently named product field?

The answer is useful because `SMART`, `extended SMART`, and `cloud health` are easy to collapse into one conceptual object even when the actual interface separates them by log identifier, accounting boundary, and persistence contract.

## Sources inspected

1. **Samsung Electronics, _PM9A3 NVMe M.2 Datasheet_, Rev. 1.0, January 2021.** Models listed on the cover include `MZ1L21T9HCLS-00A07`, `MZ1L2960HCJR-00A07`, and `MZ1L23T8HBLA-00A07`. The surviving copy inspected here is Samsung-authored but mirror-hosted: <https://www.stesz.com/Upload/SAMSUNG/PM9A3/PM9A3-M.2-Datasheet.pdf>.
2. **Samsung Electronics, _Samsung DC Toolkit 3.0 User Guide_, Rev. 1.0, October 2023.** Official Samsung-hosted PDF: <https://download.semiconductor.samsung.com/resources/user-manual/Samsung_DCToolkit_V3.0_User_Guide.pdf>.
3. **Open Compute Project, _NVMe Cloud SSD Specification_, Version 1.0 (03182020).** First-party OCP PDF: <https://www.opencompute.org/documents/nvme-cloud-ssd-specification-v1-0-3-pdf>.

The OCP source is a profile/specification witness, not evidence that OCP invented SSD health telemetry. Case 55 already carries earlier ATA and NVMe floors.

---

## Historical record

### H/P* — PM9A3 exposes a vendor-specific OEM Extended SMART page at LID `0xCA`

The January-2021 PM9A3 datasheet identifies the device as NVMe 1.4 compliant and documents the standard NVMe SMART/Health information elsewhere in the interface tables. In Identify Controller vendor-specific space, byte 3092 is described as `OEM Extended SMART Supported`, with value `1h` indicating support.

Section 6.4 then defines **Extended SMART Information Log (LID `0xCA`)**. The page contains a mixture of normalized/raw attribute groups and fixed-offset counters/state. Examples include:

- lifetime program-fail and erase-fail counts;
- lifetime wear-level information, including minimum, maximum, and average erase cycles;
- lifetime end-to-end and CRC error counts;
- media-wear percentage, host-read percentage, and workload timer;
- lifetime thermal-throttle status and event count;
- lifetime user writes, lifetime NAND writes, and lifetime user reads;
- retired/unused/used reserved-block counts;
- `Read Reclaim count`;
- lifetime UECC count;
- power-on hours and clean/unclean shutdown counts;
- SRAM/DRAM CECC/UECC-related fields;
- firmware-update success/failure counts;
- read-recovery attempts;
- reset count, trimmed-sector count, temperature excursion counts, and recovery-reset count.

The document is Samsung-authored primary product content, but because the inspected PDF is mirror-hosted this record marks provenance as `H/P*` rather than silently claiming current Samsung custody of that 2021 datasheet copy.

### H/P* — one field explicitly states power-cycle persistence, but the page does not give one blanket persistence sentence for every field

Within the `0xCA` table, Samsung explicitly says the thermal-throttling event count is **preserved over power cycles**. That wording is direct evidence for that named field.

It does not follow that every adjacent field has exactly the same update, reset, saturation, or persistence semantics. Many are labelled `Lifetime`, some are not, and the table does not state one universal `all bytes in 0xCA persist identically` rule.

The bounded historical claim is therefore deliberately asymmetric:

> **explicit power-cycle persistence for one field is strong evidence for that field; adjacency on the same page is not a substitute for a persistence contract for every other field.**

### H/P* — PM9A3 also defines a distinct Enhanced SMART page at LID `0xC4`

Immediately after the OEM `0xCA` layout, the same datasheet defines a separate **Enhanced SMART Log (LID `0xC4`)**. Its fields include throughput/timed-workload measures, read/write error measures, temperature statistics, and physical-media-unit read/write accounting.

Thus the named product does not expose one monolithic `SMART` record. At minimum, the inspected interface distinguishes:

```text
standard NVMe SMART / Health (0x02)
        !=
Samsung OEM Extended SMART (0xCA)
        !=
Samsung Enhanced SMART (0xC4)
```

The distinction is an interface fact, not a claim that the three pages are backed by three physically separate stores inside the controller.

### H/P — Samsung's official DC Toolkit names PM9A3 and provides a separate extended-SMART retrieval path

Samsung's October-2023 DC Toolkit 3.0 guide lists **Samsung SSD PM9A3** among the supported drives. For NVMe devices, `-NG / --nvme-get-log-page` has separate selectors for standard SMART/Health (`--smart`) and extended SMART (`--smart-extended`).

The guide's reference-output page shows a named `SAMSUNG NVMe SSD PM9A3` with firmware `GDC7502Q` under `Get Extended SMART data`, and separately shows temperature, firmware, and estimated-lifetime output.

This is useful named-product corroboration that the vendor-facing telemetry vocabulary reached Samsung's public management tooling. It still does not prove that every PM9A3 firmware uses one immutable byte layout, or that DC Toolkit's presentation exposes every raw field from the 2021 datasheet.

### H/P — OCP Cloud SSD defines yet another telemetry namespace: Cloud Health `0xC0`

The Open Compute Project's 18-March-2020 NVMe Cloud SSD specification defines a vendor-specific **SMART Cloud Health Log at `0xC0`** and a 512-byte Cloud Attribute Log layout.

The profile gives explicit retention rules that are stronger and more general than the single-field PM9A3 wording inspected above. `SLOG-1` says values in the vendor log pages are persistent across power cycles unless otherwise specified. `SLOG-10` says the device shall not lose SMART Health `0x02` or Cloud Health `0xC0` data more than ten minutes old across power cycles/resets; `SLOG-11` separately preserves backup-energy-source failure information and critical warnings across those boundaries.

The same profile defines `Physical Media Units Written` as bytes written to media including user and metadata traffic to user and system areas, explicitly so the attribute can be used to calculate write amplification. `Physical Media Units Read` similarly covers reads from user and system areas.

This is a valuable accounting-boundary contrast with base NVMe `Data Units Written`, which Case 55 already grounds as host/controller-interface traffic rather than a normative count of internal NAND work.

---

## Engineering reconstruction

### E — telemetry namespace is part of the evidence boundary

A useful reconstruction for the named-product/profile combination is:

```text
host-visible health concept
        -> selected log namespace / LID
        -> field-specific accounting rule
        -> field-specific update/persistence rule
        -> host/tool interpretation
```

The log identifier is not cosmetic. It tells the researcher which contract is being read. Therefore:

> **same device + same word `SMART` != one homogeneous telemetry schema.**

and:

> **same semantic theme (`writes`, `wear`, `reset`, `reclaim`) != same accounting or persistence horizon.**

### E — OCP `0xC0` persistence cannot be silently projected onto Samsung `0xCA`

The OCP specification explicitly scopes its persistence requirements to its SMART/Cloud-health contract. The PM9A3 datasheet separately assigns `0xCA` to Samsung OEM Extended SMART and `0xC4` to Enhanced SMART.

The numerical similarity of vendor log identifiers does not create inheritance. In particular:

> **OCP Cloud Health persistence rule != proof that every Samsung `0xCA` byte persists by the same rule.**

If a future source establishes PM9A3 conformance to a particular OCP revision, that still must be tied to the exact required log/page and firmware/profile scope rather than used as a blanket statement about all vendor telemetry.

### E — an internal-media counter and a host-write counter answer different questions

The PM9A3 OEM page distinguishes `Lifetime user writes` from `Lifetime NAND writes`; its enhanced page exposes physical-media-oriented quantities. OCP likewise defines physical-media units as including user and metadata traffic in user/system areas.

This supplies a product/profile-level counterexample to treating a generic `bytes written` number as self-explanatory:

> **host-visible write traffic != physical-media write traffic.**

That difference is precisely what makes write amplification an additional relation rather than a synonym for host write volume.

### E/A — PM963 `Lifetime read Reclaim count` and PM9A3 `Read Reclaim count` should not be normalized into one persistence claim

Case 67 already records Samsung DC Toolkit evidence for a PM963 field named `Lifetime read Reclaim count`. The PM9A3 2021 `0xCA` table instead labels the field **`Read Reclaim count`** while explicitly applying `Lifetime` to many neighboring fields.

The safe cross-case comparison is functional: both products expose a read-reclaim-related counter vocabulary. It is **not** safe to infer from the PM963 label that the PM9A3 field is lifetime-persistent, nor to infer shared trigger logic, counter width, reset behavior, firmware lineage, or physical read-disturb policy.

Therefore:

> **similar vendor field name across products != identical persistence horizon or implementation.**

### E — a counter named `Reset Count` is telemetry about resets, not evidence for a telemetry-reset command

The PM9A3 table includes `Reset Count` and `Recovery Reset Count` as attributes. In this evidence slice they are treated as reported state. Their names do not establish an interface that clears other counters, nor do they establish what exact reset classes are accumulated beyond the vendor's field naming.

This blocks a common lexical overreach:

> **`Reset Count` field != counter-reset semantics.**

---

## Functional comparisons

### Versus Case 55's base NVMe SMART/Health

Base NVMe standardizes a cross-vendor set of health fields. PM9A3 adds vendor pages that expose more implementation/product-specific summaries. The useful relation is **layering**, not replacement: standard telemetry can coexist with vendor-specific telemetry.

### Versus Case 67 read reclaim

Case 67 studies maintenance evidence and relocation policy around read disturb and also carries a PM963 telemetry witness. PM9A3 contributes another named product's reclaim-related counter but does not reveal the trigger algorithm. Telemetry existence is therefore weaker than mechanism identity.

### Versus Case 38 power-loss protection

PM9A3's vendor telemetry includes shutdown/error/reset-related fields, while Case 38 studies PLI apparatus health and independent power-cut validation. A counter or log entry about an event is not itself proof that the underlying protection path worked correctly.

### Versus OCP Cloud SSD

The OCP profile is a normative cloud-device contract with explicit persistence, saturation, update, and accounting requirements for its pages. PM9A3's datasheet is a product interface witness. Similar operational goals do not erase the difference between a profile requirement and a particular vendor page definition.

---

## Rejected / unsupported claims

- **X — `PM9A3 0xCA is the OCP 0xC0 Cloud Health log`.** Rejected: the inspected documents assign different LIDs and layouts.
- **X — `all PM9A3 0xCA fields are lifetime-persistent because nearby fields say Lifetime`.** Rejected: field-specific wording is not a blanket contract.
- **X — `OCP SLOG-10 proves PM9A3 0xCA persistence`.** Rejected unless a source explicitly maps that product/firmware/page to the OCP requirement.
- **X — `Read Reclaim count proves the PM9A3 controller uses Case 67's patented SK hynix algorithm`.** Rejected: telemetry vocabulary does not identify trigger logic or implementation genealogy.
- **X — `Reset Count means the host can reset PM9A3 SMART counters`.** Rejected: the field is evidence of reported reset history, not a documented clearing command.
- **X — `Lifetime NAND writes is a raw count of NAND page-program commands`.** Rejected: the datasheet gives an aggregate vendor field, not a complete physical command trace.
- **X — `OCP 2020 or Samsung 2021 establishes invention priority for vendor SMART telemetry`.** Rejected: Case 55 already carries substantially earlier ATA/NVMe health-history evidence.
- **X — `a vendor telemetry page is a sanitization witness`.** Rejected: health/history reporting does not prove old physical payload embodiments became unrecoverable.

---

## Claim ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| PM9A3 2021 datasheet defines OEM Extended SMART at `0xCA` | `H/P*` | Samsung-authored, mirror-hosted product datasheet |
| PM9A3 2021 datasheet separately defines Enhanced SMART at `0xC4` | `H/P*` | same product datasheet |
| PM9A3 `0xCA` includes lifetime user/NAND writes, reserve/error/shutdown fields, read-reclaim count, reset count, and related telemetry | `H/P*` | field-layout evidence; not hidden-algorithm evidence |
| PM9A3 thermal-throttle event count is explicitly preserved over power cycles | `H/P*` | explicit field wording |
| every adjacent `0xCA` field therefore has identical persistence/reset semantics | `X` | no blanket product statement inspected |
| Samsung DC Toolkit 3.0 supports PM9A3 and distinguishes SMART from extended-SMART retrieval | `H/P` | official Samsung 2023 guide |
| OCP Cloud SSD 2020 defines a separate `0xC0` Cloud Health log with explicit persistence rules | `H/P` | first-party OCP specification |
| OCP `0xC0` persistence rules automatically govern Samsung `0xCA` | `X` | different namespace/contract; mapping not established |
| OCP Physical Media Units Written includes user+metadata and user+system-area media traffic | `H/P` | explicit OCP field definition |
| host-write and physical-media-write counters have different accounting boundaries | `E` | bounded reconstruction from base NVMe + PM9A3/OCP definitions |
| PM963 and PM9A3 read-reclaim counters prove identical persistence or firmware lineage | `X` | similar vocabulary only |
| one product can expose several telemetry surfaces whose fields must be interpreted under their own contracts | `E` | product/profile interface reconstruction |

## Open work after this slice

The bounded named-product layout debt is partially closed, not exhausted. Still open:

- firmware-specific PM9A3 validation of counter reset/saturation/update behavior;
- controlled power-cycle and abrupt-power-loss tests against named fields;
- exact OCP conformance scope for particular PM9A3 form factors/OEM firmware revisions;
- cross-generation comparison with later Samsung PM9D3/PM1743 telemetry without assuming lineage;
- fleet-tool handling of field rollover, unsupported values, and firmware revisions;
- controller-internal mapping from telemetry counters to NAND/FTL maintenance state.

Broader OCP/NVMe telemetry genealogy belongs primarily in `tmzncty/computing-archaeology`; a fresh repository search found no dedicated existing module to reuse in this round.
