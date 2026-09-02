# Case 30 grounding — NVMe 1.4 Persistent Memory Region (2019)

## Purpose

This record grounds [`../cases/30-nvme14-pmr-persistence-barriers.md`](../cases/30-nvme14-pmr-persistence-barriers.md).

The bounded question is not a general history of persistent memory. It is narrower:

> What did the first ratified NVMe specification that introduced the optional **Persistent Memory Region (PMR)** require a host to distinguish among persistent bytes, posted writes, persistence barriers, readiness, restore correctness, and health/error state?

The evidence is unusually strong because the central mechanism is defined directly by the standards organization in the ratified 2019 base specification.

---

## Source set

### P1 — NVM Express Base Specification Revision 1.4

- **Organization:** NVM Express, Inc.
- **Document:** _NVM Express Base Specification Revision 1.4_.
- **Date:** 10 June 2019.
- **Official PDF:** <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>
- **Role:** primary technical authority for PMR registers, addressing, access semantics, persistence mechanism, barriers, readiness, restore/health state, and not-ready behavior.

Directly inspected anchors:

- cover / PDF p. 1 — revision and date;
- printed p. 56 — `PMRCAP`, including `PMRWBM` write-barrier capability;
- printed p. 57 — `PMRCTL.EN`;
- printed p. 58 — `PMRSTS.HSTS`, `NRDY`, and `ERR`;
- printed pp. 58–59 — elasticity-buffer size and sustained-throughput registers;
- printed pp. 59–60 — `PMRMSC` controller-address relation;
- printed pp. 86–87 — §4.8 `Persistent Memory Region` mechanism and interface semantics.

The key §4.8 pages were inspected both through the PDF text layer and rendered page images. The status-register wording on printed p. 58 was directly checked in the PDF text layer; the same table is structurally clear from the source and does not rely on OCR.

### P2 — NVM Express, `Changes in NVMe Revision 1.4`

- **Organization:** NVM Express, Inc.
- **Official page:** <https://nvmexpress.org/changes-in-nvme-revision-1-4/>
- **Role:** version-history control.

The page classifies PMR under **New Features**, marks it optional, and summarizes it as a PCIe memory region whose contents persist across power cycles, resets, and disabling PMR. It points to Revision 1.4 §§3.1, 4.8, 5.21, and 8.15 and Technical Proposals 4000a and 4032.

This is used to establish that PMR is new in **NVMe Revision 1.4**, not to claim invention priority for persistent memory generally.

---

## Exact claim anchors

### 1. Revision/date and version boundary

**Claim:** the bounded source is NVMe Base Specification Revision 1.4 dated 10 June 2019, and NVM Express's change record treats PMR as a new optional feature of revision 1.4.

**Evidence:** P1 cover; P2 `New Features → Persistent Memory Region`.

**Strength:** high.

**Limit:** this supports a specification-version claim only. It does not show that NVMe invented persistent memory, memory-mapped NVM, NVDIMMs, storage-class memory, or PCIe-attached persistent memory.

### 2. PMR is a general-purpose PCIe read/write persistent-memory region

**Claim:** §4.8 defines PMR as an optional general-purpose PCIe read/write persistent memory region.

**Evidence:** P1 printed p. 86, §4.8.

The same section establishes a host-visible PCIe address range selected through a BAR. When controller-addressing support is used, `PMRMSC` supplies a controller address range whose offsets correspond one-to-one with the PCIe range.

**Strength:** high.

**Retention consequence:** payload survival and address-resolution state are distinct. The bytes may persist, but which transactions resolve to them is an additional control relation.

### 3. PMR persistence crosses specific power/reset/disable transitions

**Claim:** data written to PMR while PMR is ready persist across power cycles, Controller Level Resets, and disabling PMR.

**Evidence:** P1 printed p. 87, §4.8.

**Strength:** high.

**Limit:** the paragraph is an interface guarantee for the specified conditions. It does not establish survival across every possible device failure, media failure, firmware defect, sanitize operation, or removal/destruction of the underlying device.

### 4. Persistence mechanism is implementation-specific

**Claim:** Revision 1.4 explicitly permits more than one internal route to the PMR persistence guarantee.

**Evidence:** P1 printed p. 87, §4.8.

The source gives two examples:

- persistence may mean that a write to nonvolatile memory has completed; or
- persistence may mean that the write is stored in a nonvolatile write buffer and transferred to nonvolatile memory later.

**Strength:** high.

**Engineering consequence:** `persistent interface contract ≠ fixed physical substrate or final placement`.

**Limit:** the examples do not prove that any named controller used either implementation. No capacitor, battery, DRAM, SCM, NAND, firmware journal, or other concrete physical design is inferred from the standard.

### 5. Optional write elasticity buffer creates a separate throughput/drain relation

**Claim:** PMR may include an optional write elasticity buffer when PMR sustained throughput is lower than PCIe link throughput; optional registers expose buffer size and sustained throughput, enabling estimation of drain time.

**Evidence:** P1 printed p. 87 §4.8; printed pp. 58–59 §§3.1.21–3.1.22.

**Strength:** high.

**Limit:** the standard does not equate this elasticity buffer with the nonvolatile write buffer mentioned in the persistence-mechanism example. The case therefore keeps them distinct.

### 6. PMR exposes explicit persistence barriers for earlier Posted PCIe writes

**Claim:** `PMRCAP.PMRWBM` enumerates supported mechanisms that ensure previous PMR writes have completed and are persistent, with at least one mechanism required.

**Evidence:** P1 printed p. 56, `PMRCAP.PMRWBM`; §4.8 printed p. 87.

Two mechanism bits are defined:

- completion of a memory read from a PMR address; and
- completion of a read of `PMRSTS`.

Section 4.8 describes the preceding PMR writes as Posted PCIe write requests. A `PMRSTS`-based barrier can additionally expose whether the updates completed without error.

**Strength:** high.

**Engineering consequence:** `posted-write issue/completion ≠ persistence-barrier completion`.

This conclusion does not claim that a posted PCIe write was never physically received before the barrier. It says only that NVMe 1.4 exposes the barrier as the host-visible mechanism for the stronger completed-and-persistent relation.

### 7. PMR enable and readiness are separate states

**Claim:** the host sets `PMRCTL.EN`; PMR is ready for PCIe accesses only after `PMRSTS.NRDY` clears. Saving/restoring contents may take time, and PMR can be enabled without enabling the NVMe controller itself.

**Evidence:** P1 printed p. 57 §3.1.19; §4.8 printed p. 87.

**Strength:** high.

**Engineering consequence:** `persistent survival ≠ immediate service availability`.

### 8. Not-ready request completion lacks ordinary read/write semantics

**Claim:** when PMR is not ready, reads complete successfully but return an undefined value; writes complete normally but do not update PMR.

**Evidence:** P1 printed p. 87, §4.8.

**Strength:** high.

**Engineering consequence:** `successful request completion ≠ valid recovery` and `successful request completion ≠ state mutation`.

This is one of the strongest counterexamples in the case because it is stated directly by the interface specification rather than inferred from a hypothetical failure.

### 9. Restore Error separates persistence capability from continuity with prior contents

**Claim:** `PMRSTS.HSTS = Restore Error` means PMR is operating normally and is persistent, while its contents may not have been restored correctly and may not match the contents before the preceding power cycle, NVM subsystem reset, Controller Level Reset, or PMR disable.

**Evidence:** P1 printed p. 58, `PMRSTS.HSTS`.

**Strength:** high.

**Engineering consequence:** `persistent PMR ≠ correctly restored prior state`.

This does not mean the specification regards wrong contents as correct data. It means the health/status model distinguishes the continued persistent-memory capability from continuity of the particular expected pre-transition state.

### 10. Health and error state qualify read/write/persistence trust

**Claim:** `HSTS` separately defines Normal, Restore Error, Read Only, and Unreliable states; `ERR` indicates whether earlier writes completed without error and are persistent when PMR is ready and normal.

**Evidence:** P1 printed p. 58, `PMRSTS`.

In `Read Only`, reads are correct while writes do not update PMR. In `Unreliable`, reads may be invalid or poisoned, writes may fail or write undefined data, and PMR may also have become non-persistent. Non-zero `ERR` is sticky until PCI function reset.

**Strength:** high.

**Engineering consequence:** a host-visible persistent capability still requires retained status relations to know whether current operations and earlier writes remain trustworthy.

### 11. Health reporting can lag the underlying condition

**Claim:** §4.8 warns that an asynchronous event may be reported some time after PMR health changes; the host should treat operations since the last normal status report as potentially affected. It also suggests periodic `PMRSTS` reads where needed to qualify read validity.

**Evidence:** P1 printed p. 87, §4.8.

**Strength:** high.

**Engineering consequence:** knowledge of integrity/persistence has its own temporal window; it need not change at exactly the same instant as the underlying fault.

### 12. PMR disable and sanitize are not equivalent forgetting events

**Claim:** ordinary PMR disable is within the persistence promise, whereas the specified not-ready read behavior following sanitize must not permit recovery of prior user data from cache or nonvolatile media.

**Evidence:** P1 printed p. 87, §4.8.

**Strength:** high for the interface boundary.

**Limit:** this is not a full study of NVMe sanitize, secure erasure, crypto erase, raw-media forensics, or implementation compliance. Those need a separate bounded case if pursued.

---

## Cross-case controls

### Case 20 — NVMe 1.0 Flush/FUA

Case 20 and Case 30 must not be merged into a timeless NVMe persistence model.

- **Case 20 / 2011:** namespace/LBA commands, VWC, Flush, FUA, command completion, host-enforced ordering, AWUN/AWUPF.
- **Case 30 / 2019:** memory-mapped PMR, Posted PCIe writes, read-based PMR persistence barriers, ready/health/restore status.

The historical mechanisms and vocabulary differ even though both constrain persistence at an NVMe host/controller interface.

### Case 15 — Intel SSD 320 power-loss protection

The SSD 320 case names a physical product path and stored-energy mechanism. PMR is intentionally implementation-agnostic. The PMR standard cannot be used as evidence that a particular controller used capacitors or any SSD 320-like emergency-transfer design.

### Case 04 — mapped Flash

Mapped Flash shows logical currentness surviving physical relocation inside a device. PMR shows a different abstraction boundary in which host memory addresses remain stable while internal durable placement can be implementation-specific. The resemblance is functional only.

---

## Prior-art / novelty boundary

The official change record supports the claim that PMR is **new in NVMe 1.4**. It does not support a broader priority claim.

This record therefore rejects the following shortcuts:

- `NVMe 1.4 invented persistent memory`;
- `PMR invented memory-mapped NVM`;
- `PMR is identical to every NVDIMM or SCM programming model`;
- `PMR persistence proves one specific controller substrate`;
- `PMR is automatically the same thing as any later NVMe term called persistence domain`.

Broader persistent-memory history belongs in conventional technical history or `computing-archaeology` if a historical engineering treatment is needed.

---

## Related-repository check

Before writing this slice, `tmzncty/computing-archaeology` was searched for a dedicated NVMe / Persistent Memory Region / persistence-barrier treatment. No dedicated result was found in the current code search.

That absence does not prove the topic has never been discussed elsewhere in that repository. It is sufficient for the present routing decision: this contribution remains a narrow retention-specific interface case and does not attempt a general history of NVMe or persistent memory.

---

## Evidence maturity

**Recommended case status: `grounded`.**

Reasons:

1. the mechanism is bounded to one ratified specification revision;
2. the central claims are stated directly in an official primary technical source;
3. exact section and printed-page anchors are available;
4. the crucial mechanism pages were checked in both text and rendered-page form;
5. negative/interface-failure semantics are explicit rather than reconstructed from later commentary;
6. the case preserves a strict boundary between the historical terms `PMR`, `PMRWBM`, `NRDY`, `HSTS`, `Restore Error`, and project analytical terms;
7. no named implementation/compliance or invention-priority claim is made;
8. Case 20 supplies an earlier NVMe comparison without being overwritten by later PMR semantics.

Remaining future work is deliberately outside the promotion boundary:

- exact later NVMe `persistence domain` terminology and revision archaeology;
- concrete PMR controller/product implementations and compliance;
- host persistent-memory programming models and CPU cache-flush composition;
- filesystem/database persistence composition;
- sanitize/forensics as a separate forgetting case;
- broader NVDIMM/SCM genealogy.

---

## Citation-ready sources

1. NVM Express, Inc., _NVM Express Base Specification Revision 1.4_, 10 June 2019: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>.
2. NVM Express, Inc., `Changes in NVMe Revision 1.4`: <https://nvmexpress.org/changes-in-nvme-revision-1-4/>.
