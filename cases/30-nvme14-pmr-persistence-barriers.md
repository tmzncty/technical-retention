# NVM Express 1.4 Persistent Memory Region: Posted Writes, Persistence Barriers, and Restore Health

## Scope

- **Bounded period:** 2019.
- **Primary specification:** **_NVM Express Base Specification Revision 1.4_**, dated 10 June 2019, especially §§3.1.18–3.1.23 and 4.8.
- **Research question:** what relations did NVMe 1.4 require a host to distinguish when a controller exposed an optional PCIe Persistent Memory Region whose contents were intended to survive power transitions and resets?

This is not a general history of persistent memory, NVDIMMs, storage-class memory, PCIe memory, NVMe, or host persistent-memory programming. It is a later interface-level companion to Case 20, which is bounded to NVMe 1.0 Flush/FUA semantics for queued namespace I/O.

The narrow problem here is different:

> **When a host can read and write a persistent region with PCIe memory transactions, what additional retained relations are needed to know that posted writes are persistent, the region is usable, and the bytes being read still belong to the expected pre-reset state?**

The official NVM Express change record identifies **Persistent Memory Region (PMR)** as a new optional feature in revision 1.4. The original ratified 1.4 specification is therefore used rather than silently projecting later NVMe terminology backward.

---

## Historical vocabulary

Revision 1.4 itself uses:

- `Persistent Memory Region (PMR)`;
- `persistent memory`;
- `Persistent Memory Region Capabilities (PMRCAP)`;
- `Persistent Memory Region Control (PMRCTL)`;
- `Persistent Memory Region Status (PMRSTS)`;
- `Persistent Memory Region Write Barrier Mechanisms (PMRWBM)`;
- `Not Ready (NRDY)`;
- `Health Status (HSTS)`;
- `Restore Error`;
- `Read Only`;
- `Unreliable`;
- `Error (ERR)`;
- `write elasticity buffer`;
- `Persistent Memory Region Sustained Write Throughput`;
- `Posted PCI Express requests`;
- `non-volatile write buffer` and `non-volatile memory`.

The following are **project engineering terms**, not claims about the historical vocabulary of NVMe 1.4:

- `persistence qualification`;
- `restore continuity`;
- `persistent-interface contract`;
- `availability gate`;
- `nonvolatile staging`;
- `persistence authority`.

This case deliberately does **not** rename PMR as an NVMe `persistence domain`. That phrase belongs to a separate terminology/revision-history question unless an exact period source establishes it for the particular mechanism being discussed.

---

## Historical record

### H/P — PMR was introduced as an optional NVMe 1.4 feature

The ratified Revision 1.4 cover identifies the specification as dated **10 June 2019**. NVM Express's companion change record classifies the **Persistent Memory Region** under `New Features`, calls it optional, and describes it as a PCIe memory region whose contents persist across power cycles, resets, and disabling of the PMR.

This grounds a version-specific claim only: PMR was a new optional feature of the NVMe 1.4 specification. It does not establish invention priority for persistent memory or PCIe-accessible nonvolatile memory.

**Primary anchors:** Revision 1.4 cover; NVM Express, `Changes in NVMe Revision 1.4`, `New Features → Persistent Memory Region`.

### H/P — the PMR is a general-purpose PCIe memory region with a separately controlled address relation

Section 4.8 defines PMR as an optional region of general-purpose PCIe read/write persistent memory. The host accesses its PCIe address range through the BAR selected by `PMRCAP.BIR`. If controller-address access is supported, the host may also configure a controller address range through `PMRMSC`; the PCIe and controller ranges may differ in base address but have equal size and one-to-one corresponding offsets.

For command data or metadata transfers using PMR, the specification requires the data/metadata for one command to reside entirely in PMR or entirely outside PMR rather than being split across both.

These are interface/addressing facts. The specification does not thereby tell us which physical memory chips embody those addresses.

**Primary anchors:** §4.8, printed p. 86; §§3.1.18 and 3.1.23, printed pp. 56 and 59–60.

### H/P — data written while PMR is ready persist across power cycles, Controller Level Resets, and PMR disable

Section 4.8 states that data written while PMR is ready persist across:

- power cycles;
- Controller Level Resets;
- disabling the PMR.

The same paragraph immediately refuses to bind this persistence guarantee to one physical mechanism. It gives at least two permitted implementation shapes:

1. the write to nonvolatile memory has completed; or
2. the write has reached a **non-volatile write buffer** and is written to nonvolatile memory later.

This is strong historical evidence that, at the PMR interface, `persistent` is a guarantee about survival across specified transitions, not a complete description of final physical placement.

**Primary anchor:** §4.8, printed p. 87.

### H/P — PMR may expose a write elasticity buffer whose drain time is distinct from PCIe burst acceptance

Revision 1.4 permits an optional **write elasticity buffer** to absorb bursts of PCIe writes when PCIe throughput exceeds the PMR's sustained write throughput. The specification exposes optional buffer-size and sustained-throughput registers and describes the time to move buffered data to nonvolatile media in terms of buffer occupancy and sustained throughput.

The interface therefore recognizes a temporal distinction between accepting a burst of PCIe traffic and draining internal buffered work toward nonvolatile media.

The specification does not say that every PMR has such a buffer, nor does it identify the buffer with the nonvolatile write buffer used in the preceding implementation example. Those relations are implementation-specific unless separately sourced.

**Primary anchors:** §4.8, printed p. 87; §§3.1.21–3.1.22, printed pp. 58–59.

### H/P — PMR write barriers qualify completion and persistence of earlier Posted PCIe writes

`PMRCAP.PMRWBM` enumerates supported PMR write-barrier mechanisms and requires at least one supported mechanism. Revision 1.4 defines two possible barrier forms:

- completion of a PCIe memory read from any PMR address can ensure that all prior writes to PMR have completed and are persistent; and/or
- completion of a read from `PMRSTS` can provide the corresponding barrier, with status additionally indicating whether the associated PMR updates completed without error and are persistent.

Section 4.8 explicitly identifies the earlier writes as **Posted PCI Express requests**.

The historical point is not that PCIe posting is unreliable. It is that NVMe 1.4 itself exposes a stronger persistence relation that the host may need to establish after posted writes.

**Primary anchors:** `PMRCAP.PMRWBM`, printed p. 56; §4.8, printed p. 87.

### H/P — enablement and readiness are separate from persistence of the contents

The host enables PMR through `PMRCTL.EN`; after enablement the controller indicates readiness by clearing `PMRSTS.NRDY`. Section 4.8 notes that restoring or saving PMR contents can take time and that enabling the NVMe controller itself is not required in order to enable PMR.

Thus a persistent set of bytes may survive while the region is temporarily not ready to service normal PCIe memory access.

**Primary anchors:** §3.1.19 `PMRCTL`, printed p. 57; §4.8, printed p. 87.

### H/P — request completion while PMR is not ready does not imply valid read data or a successful state update

Revision 1.4 gives unusually sharp negative semantics when PMR is not ready:

- PMR reads complete successfully but return an undefined value;
- PMR writes complete normally but do not update PMR contents.

This is direct period-primary evidence that successful transport/request completion is not sufficient to infer either valid recovered content or a completed state transition.

**Primary anchor:** §4.8, printed p. 87.

### H/P — a PMR can remain persistent while failing to restore the expected prior contents

`PMRSTS.HSTS` defines several health states. In `Restore Error`, the PMR is described as operating normally and persistent, but its contents may not have been restored correctly and may therefore differ from the contents before the preceding power cycle, NVM subsystem reset, Controller Level Reset, or PMR disable.

The same status register separately defines:

- `Read Only`, in which reads return correct data but writes do not update PMR;
- `Unreliable`, in which reads may be invalid/poisoned, writes may fail or write undefined data, and the PMR may have become non-persistent;
- `ERR`, which while the PMR is ready and normal qualifies whether previous writes completed without error and their values are persistent.

The specification therefore treats persistence, prior-state restoration, read validity, writeability, and error-free completion as separable interface properties.

**Primary anchor:** §3.1.20 `PMRSTS`, printed p. 58.

---

## Retained state

This bounded case requires more than one retained object or relation.

### 1. PMR payload bytes

The host observes a memory-addressed byte region whose contents are intended to survive the specified power/reset/disable transitions when written while ready.

### 2. Address-resolution state

BAR selection, the PMR PCIe address range, and—if supported—the controller address range determine which memory transactions resolve to the PMR. A persistent payload without a valid address relation is not the same thing as a usable PMR interface.

### 3. Buffered write state

The specification permits implementation-specific nonvolatile staging and separately permits a write elasticity buffer. Pending internal write work may therefore exist between host transaction acceptance and later placement/drain stages.

### 4. Barrier relation

A host may need evidence that earlier Posted PCIe writes have completed and are persistent. This relation is not reducible to the bytes themselves; the specification exposes supported barrier mechanisms and status for it.

### 5. Ready / health / error state

`NRDY`, `HSTS`, and `ERR` qualify whether the region can presently service requests, whether returned contents can be trusted, whether write updates are permitted, and whether earlier writes reached the promised persistent state.

### 6. Restore continuity

A PMR can be `persistent` after a transition while still reporting `Restore Error`. Whether the post-transition contents are the expected pre-transition contents is therefore a separate relation from the region's abstract ability to retain persistent state.

---

## Retention mechanism

### Persistence across transitions

The host-visible contract is that data written while ready survive specified transitions. The physical path is deliberately implementation-specific.

### Direct-NVM path

One permitted implementation interpretation is that persistence is reached when the write to nonvolatile memory has completed.

### Nonvolatile-buffer path

Another permitted interpretation is that the write reaches a nonvolatile write buffer and is transferred to nonvolatile memory later. The interface can therefore treat a write as persistent without exposing final internal placement as the host's completion criterion.

### Optional elasticity-buffer path

A PMR may additionally buffer burst traffic to decouple PCIe burst throughput from sustained PMR write throughput. Because the specification does not equate this optional elasticity buffer with the nonvolatile persistence buffer example, this case keeps them separate.

### Barrier path

Supported PMR barriers give the host a way to turn a sequence of earlier posted memory writes into a stronger statement: those writes have completed and are persistent, with `PMRSTS` additionally able to qualify error state.

---

## Addressing and access geometry

PMR differs from the queued namespace/LBA path emphasized in Case 20.

The host may access PMR through ordinary PCIe memory reads and writes to a BAR-backed address range. If controller-address access is supported, host-configured controller addresses map by equal offsets into the same region.

This creates several distinct questions:

```text
Which PCIe address names the PMR?
        ≠
Is PMR enabled?
        ≠
Is PMR ready?
        ≠
Did this memory request complete?
        ≠
Did prior posted writes become persistent?
        ≠
Are the returned bytes valid and continuous with the prior state?
```

The interface itself exposes separate registers/relations for these questions.

---

## Read / write / barrier semantics

### Posted writes

Ordinary PMR memory writes use PCIe memory transactions. Revision 1.4's barrier discussion explicitly treats earlier PMR writes as Posted PCIe requests and provides a persistence barrier beyond merely having issued those writes.

### Barrier through PMR read

If the corresponding `PMRWBM` capability is advertised, completion of a PCIe read from PMR acts as a barrier for earlier PMR writes.

### Barrier through `PMRSTS`

If the status-read barrier is supported, a `PMRSTS` read both orders earlier writes into a persistence point and exposes whether the updates completed without error.

### Not-ready access

When PMR is not ready, read and write requests can still complete at the interface while failing to supply the semantic result a caller might ordinarily infer from completion: reads return undefined data and writes leave memory unchanged.

### Health-qualified reads and writes

`HSTS` further qualifies whether reads are trustworthy and writes update memory. An `Unreliable` PMR may even cease to be persistent.

---

## Time and availability

This case adds several independently meaningful timescales:

- PCIe posted-write issue;
- posted-write completion as established by a supported barrier;
- persistence qualification;
- optional elasticity-buffer drain time;
- later internal transfer from nonvolatile buffering to nonvolatile memory;
- PMR enable/disable transition;
- save/restore time before `NRDY` changes;
- power/reset interval;
- health-state reporting delay and host polling interval.

The interface explicitly warns that a critical warning/asynchronous event may arrive after the PMR health condition changed. A host that depends on health therefore has an interval of uncertainty: operations since the last known-normal status may have been affected.

Persistence, availability, and knowledge of integrity are therefore not synchronized into one timestamp.

---

## Failure / forgetting modes

Distinct failures include:

- host failure to execute a supported persistence barrier before relying on prior Posted PCIe writes;
- PMR not-ready state, where request completion does not produce ordinary read/write semantics;
- `Restore Error`, where the PMR remains persistent but expected pre-transition contents may not have been restored;
- read-only transition, which preserves readable state while removing write authority;
- unreliable state, where data validity, write success, and even persistence may be compromised;
- non-zero `PMRSTS.ERR`, which creates uncertainty over one or more previous writes;
- loss/misconfiguration of the relevant address relation even while payload survives;
- implementation failure below the interface contract.

Revision 1.4 also draws a useful forgetting boundary. Ordinary PMR disable is inside the stated persistence guarantee; by contrast, after a sanitize operation, a not-ready PMR read must return an undefined value that does not permit recovery of previous user data from cache or nonvolatile media. This is a narrow interface statement, not a claim about every physical sanitization mechanism or forensic technique.

---

## Engineering reconstruction

### E — persistent interface contract ≠ fixed physical substrate

Revision 1.4 explicitly allows the PMR persistence promise to be realized either by completed nonvolatile-memory placement or by nonvolatile buffered state that is moved later. The interface promise therefore underdetermines the internal embodiment.

### E — posted-write issue/completion ≠ persistence-barrier completion

The existence of `PMRWBM` is a direct counterexample to collapsing these layers. The host may need an explicit supported read-based barrier before it can assert that previous Posted PCIe writes have completed and are persistent.

### E — persistent write ≠ final internal placement

A write can satisfy the PMR persistence contract through a nonvolatile buffer before a later transfer to nonvolatile memory. `Persistent now` and `already at its final internal location` are different relations.

### E — persistence ≠ immediate availability

PMR can retain contents across reset/disable while save/restore takes time and `NRDY` temporarily blocks ordinary service. Survival of state and current callability are separate.

### E — ready ≠ restored continuity

`Restore Error` is the strongest period-primary counterexample: a PMR can be ready enough to report a health status, still be persistent, and yet fail to contain the expected pre-transition contents.

### E — successful request completion ≠ valid recovery or state update

The not-ready semantics explicitly permit successful/normal completion without valid read data and without write mutation. Completion must therefore be typed by the interface state in which it occurred.

### E — persistence capability ≠ perpetual trust

Health and error status can later qualify or revoke assumptions about valid reads, successful writes, and persistence. Persistent state still depends on retained diagnostic/control relations that tell the host whether a particular interval remains trustworthy.

---

## Functional analogies

### A — Case 20, NVMe 1.0 Flush/FUA

Both cases concern NVMe interface-level persistence, but their access and control shapes are different.

Case 20:

```text
queued namespace/LBA command
→ optional volatile write cache
→ Flush or per-write FUA
→ command completion / media commitment
```

Case 30:

```text
PCIe memory-addressed PMR
→ Posted memory writes
→ supported read-based persistence barrier
→ readiness / health / restore qualification
```

The comparison is functional. PMR should not be described as merely `FUA for memory`, and the 2011 namespace command semantics should not be rewritten using 2019 PMR vocabulary.

### A — Case 15, Intel SSD 320 PLP

Case 15 grounds a named physical/controller implementation involving volatile staging and stored capacitor energy. Case 30's PMR text deliberately leaves the persistence implementation open. A PMR may use an internal nonvolatile buffer, but that does not license an inference that it uses Intel SSD 320-style capacitors or any other specific PLP mechanism.

### A — Case 04, mapped Flash

Case 04 separates logical identity from physical location inside mapped Flash. Case 30 adds another interface-level separation: persistent host-visible bytes can remain invariant while the controller changes where or how their durable representation is internally staged. Neither case establishes the other's exact mapping or media-management mechanism.

---

## Philosophical interpretation

### I — persistence can survive while continuity and availability fail

The most useful conceptual pressure from this case is not that `persistent memory remembers`. It is that the specification itself separates at least three stronger questions:

1. **Did a state survive a specified transition?**
2. **Is the state currently available through the interface?**
3. **Is the available state continuous with the state expected from before the transition?**

`NRDY` and `Restore Error` show that these are not synonyms. A technically persistent region can be temporarily unavailable; it can also remain persistent as a capability while the expected earlier contents fail to be restored correctly.

This does not establish a general philosophical theory of memory. It supplies a bounded engineering counterexample to any theory that equates persistence, availability, and temporal continuity without qualification.

---

## Claim ledger

| Claim | Type | Evidence / limit |
| --- | --- | --- |
| PMR is a new optional NVMe 1.4 feature | H/P | official NVM Express change record + ratified 1.4 specification; no invention-priority claim |
| PMR is a general-purpose PCIe read/write persistent-memory region | H/P | §4.8, printed p. 86 |
| data written while PMR is ready persist across power cycles, Controller Level Resets, and PMR disable | H/P | §4.8, printed p. 87 |
| the persistence mechanism may be direct NVM completion or nonvolatile buffering followed by later NVM transfer | H/P | §4.8, printed p. 87; implementation remains unspecified |
| PMR may expose an optional write elasticity buffer | H/P | §4.8 and §§3.1.21–3.1.22; do not equate it automatically with the nonvolatile persistence buffer |
| a supported PMR read-based barrier ensures earlier Posted PCIe writes have completed and are persistent | H/P | `PMRCAP.PMRWBM`, printed p. 56; §4.8 p. 87 |
| PMR enable and PMR ready are distinct | H/P | `PMRCTL.EN`, `PMRSTS.NRDY`; §§3.1.19–3.1.20 |
| not-ready reads may complete successfully with undefined data; not-ready writes may complete without updating memory | H/P | §4.8, printed p. 87 |
| Restore Error permits a persistent PMR whose expected prior contents were not restored correctly | H/P | `PMRSTS.HSTS`, printed p. 58 |
| successful request completion is not sufficient to infer valid recovery or write mutation | E | reconstructed directly from the not-ready semantics |
| persistence does not imply immediate availability | E | persistence across disable/reset + save/restore/NRDY timing |
| PMR persistence is not identical to NVMe 1.0 Flush/FUA semantics | A | bounded comparison with Case 20 |
| PMR is an NVMe `persistence domain` in the same historical sense used by later specifications | X | not established in this bounded source set; exact terminology remains future work |

---

## Evidence status

**Status: `grounded`.**

The central claims depend on the official ratified **NVM Express Revision 1.4** specification and NVM Express's official 1.4 change record. The key PMR mechanism pages were checked in both text and rendered-page form. No named-controller implementation or compliance claim is made, and no broader persistent-memory invention genealogy is inferred.

Grounding record:

- [`../evidence/30-nvme14-2019-pmr-grounding.md`](../evidence/30-nvme14-2019-pmr-grounding.md)

---

## Sources

### Primary

1. NVM Express, Inc., **_NVM Express Base Specification Revision 1.4_**, 10 June 2019, especially §§3.1.18–3.1.23 and 4.8: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>.
2. NVM Express, Inc., **`Changes in NVMe Revision 1.4`**, especially `New Features → Persistent Memory Region`: <https://nvmexpress.org/changes-in-nvme-revision-1-4/>.

### Related repository check

`tmzncty/computing-archaeology` was searched for a dedicated NVMe / PMR / persistence-barrier treatment before writing this slice. No dedicated case was found in the current repository search, so this case keeps only the retention-specific interface argument rather than constructing a general NVMe or persistent-memory history.
