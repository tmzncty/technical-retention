# Case 15 Grounding Record — Intel SSD 320 Power-Loss Durability Boundary

## Purpose

This record supports [`cases/15-intel-ssd320-power-loss-durability.md`](../cases/15-intel-ssd320-power-loss-durability.md).

The bounded promotion question is:

> Can the repository directly establish a controller-mediated retention regime in which a nonvolatile Flash medium coexists with volatile staging/system state, an explicit volatile-cache → nonvolatile-media flush contract, and a power-failure-triggered emergency transfer backed by stored energy?

**Result:** yes. The case is `grounded` for that mechanism. It does not establish all SSD durability semantics, filesystem persistence, NVMe persistence domains, or the empirical fault behavior of every Intel SSD 320 unit.

---

## Source set and evidence classes

### Source A — T13 ATA8-ACS working draft, 2007

**Document:** T13/1699-D Revision 4a, _AT Attachment 8 - ATA/ATAPI Command Set (ATA8-ACS)_, 21 May 2007.

**Inspection:** direct PDF text + rendered page inspection, §7.14 printed p. 108 / PDF p. 147; adjacent §7.15 printed p. 109 / PDF p. 148.

**Evidence class:** `H/P` — period standards-development primary evidence.

**Directly establishes:**

- the period term `volatile write cache`;
- the period term `non-volatile media`;
- `FLUSH CACHE` as a host request to move cache data to nonvolatile media;
- command completion is not to be indicated until the data have been flushed to nonvolatile media or an error occurs;
- `FLUSH CACHE EXT` repeats the same core relation for the 48-bit feature set.

**Boundary:** the title page says Revision 4a is a **working draft** and not a completed standard. Do not cite it as the final ANSI publication.

Surviving copy inspected: <https://tc.gts3.org/cs3210/2016/spring/r/hardware/ATA8-ACS.pdf>

---

### Source B — Intel SSD 320 power-loss technical brief, March 2011

**Document:** Intel Corporation, _Intel Solid-State Drive 320 Series: Power Loss Data Protection_, order 325207-001US, March 2011.

**Inspection:** direct Intel-hosted two-page PDF; both pages visually inspected.

**Evidence class:** `H/P` — manufacturer-primary product/design disclosure.

**Directly establishes:**

- user and system data may reside for brief periods in `temporary buffers` as well as NAND;
- normal shutdown is described through `STANDBY IMMEDIATE`, permitting temporary-buffer state to be saved to nonvolatile NAND;
- an `unsafe shutdown` can interrupt that normal saving path;
- a power-fail detector signals the controller ASIC as input power drops;
- firmware disconnects the input-power path and uses onboard power-loss-protection capacitance;
- stored capacitor energy is described as sufficient for firmware to move transfer-buffer / other temporary-buffer data to NAND;
- the unsafe-shutdown path prioritizes user and system data over nonessential controller activity;
- the block diagram exposes `Power Fail Detect`, `Power Good`, `Power FET`, `Hold-up Circuit`, and `Power Loss Protection Capacitance` as distinct parts of the mechanism.

**Boundary:** this is Intel's own product/design account. It is strong historical evidence for the mechanism Intel documented, but it is not independent fault-injection validation or a guarantee for every possible power transient.

<https://www.intel.com/content/dam/www/public/us/en/documents/technology-briefs/ssd-320-series-power-loss-data-protection-brief.pdf>

---

### Source C — Intel SSD 320 enterprise addendum, April 2011

**Document:** Intel Corporation, _Intel Solid-State Drive 320 Series Enterprise Server/Storage Application Product Specification Addendum_, order 325170-002US, April 2011.

**Inspection:** direct Intel-hosted PDF, first page and printed p. 5 inspected.

**Evidence class:** `H/P` — manufacturer-primary named-product specification.

**Directly establishes:**

- Intel presents the SSD 320 as ATA8-ACS compatible;
- `Enhanced power-loss data protection` is a named product feature;
- the enterprise random-write performance method is documented with `SSD write-cache enabled`.

**Boundary:** performance-test cache enablement does not by itself define every host-write completion or durability semantic. It is used only to establish that a write-cache facility is real in the named product context.

<https://www.intel.com/content/dam/www/public/us/en/documents/product-specifications/ssd-320-enterprise-server-storage-application-specification-addendum.pdf>

---

### Source D — Intel SSD 320 Product Specification, September 2011

**Document:** Intel Corporation, _Intel Solid-State Drive 320 Series Product Specification_, order 325152-002US, September 2011.

**Inspection:** directly rendered surviving mirrored PDF, especially printed pp. 16, 21, and 22.

**Evidence class:** `H/P` for the identifiable Intel document; source-host provenance is separately qualified.

**Directly establishes:**

- the SSD 320 supports mandatory ATA8-ACS commands in the documented set;
- `FLUSH CACHE` appears in the ATA General Feature command set;
- `STANDBY IMMEDIATE` appears in the Power Management command set;
- SCT Feature Control exposes `write cache` and `write cache reordering` feature codes;
- `FLUSH CACHE EXT` appears in the 48-bit Address command set.

**Boundary:** the inspected PDF is currently reached through a third-party mirror (`ssdwiki.com`). The document itself carries Intel's title/order/date, but this record does not represent the mirror as official Intel hosting.

Surviving copy inspected: <https://www.ssdwiki.com/media/ssd-320-specification.pdf>

---

### Source E — Zheng et al., FAST ’13

**Document:** Mai Zheng, Joseph Tucek, Feng Qin, Mark Lillibridge, “Understanding the Robustness of SSDs under Power Fault,” _FAST ’13_, pp. 271–284.

**Inspection:** direct USENIX paper inspection, especially printed pp. 273, 279, and 281.

**Evidence class:** `S` plus experimental evidence reported by the authors; used here as a high-quality independent boundary/counterexample, not product identity evidence.

**Directly supports:**

- SSD controller/FTL state can include mapping relations whose power-fault consistency matters in addition to payload programming;
- the authors' synchronous-write test path included cache flushes and they verified that flush commands were issued;
- some anonymized tested SSDs nevertheless exhibited unexpected failure/serialization behavior under power fault;
- the paper discusses a failure ordering in which a page may be programmed while the controller's validity/mapping state does not become consistently current.

**Boundary:** the fifteen tested SSDs are anonymized. This paper cannot establish that the Intel SSD 320 was tested or failed. Its role is to reject a universal inference from interface contract to empirical compliance.

<https://www.usenix.org/conference/fast13/technical-sessions/presentation/zheng>

---

## Grounded mechanism

The combined primary evidence supports the following bounded model:

```text
                    host persistence/shutdown control
                    ┌───────────────┴────────────────┐
                    │                                │
              FLUSH CACHE                   STANDBY IMMEDIATE
                    │                                │
                    └───────────────┬────────────────┘
                                    ↓
                        temporary / volatile state
                                    ↓
                           controller / firmware
                                    ↓
                           nonvolatile NAND

unexpected external power loss
          ↓
   power-fail detection
          ↓
firmware emergency path + input isolation
          ↓
 stored capacitor energy
          ↓
finish temporary user/system-state transfer to NAND
```

The first branch is command/interface controlled. The second branch is device-triggered failure handling. They converge on a nonvolatile NAND target but are not the same retention event.

---

## Claims strengthened by this slice

### G-15.1 — `nonvolatile medium ≠ every necessary current device state is already nonvolatile`

**Evidence:** Intel directly describes temporary user/system buffers plus NAND.

**Status:** grounded engineering reconstruction from manufacturer-primary mechanism evidence.

### G-15.2 — an explicit flush can define a volatile → nonvolatile completion boundary

**Evidence:** ATA8-ACS Rev. 4a §7.14–7.15; Intel SSD 320 command support.

**Status:** grounded for the cited draft/interface/product context.

### G-15.3 — persistence can require event-triggered work after external power begins to disappear

**Evidence:** Intel power-fail detector, firmware path, isolation, stored capacitance, NAND transfer.

**Status:** grounded for the SSD 320 design disclosure.

### G-15.4 — `stored energy ≠ stored payload`, while stored energy can still be retention infrastructure

**Evidence:** capacitor charge supplies hold-up energy for transfer; NAND is the nonvolatile payload target.

**Status:** grounded engineering reconstruction.

### G-15.5 — payload programming and mapping/currentness durability are separable

**Evidence:** Case 04 already establishes mapping as retained state; Zheng et al. provide later experimental/controller discussion where programmed data and validity/mapping ordering can diverge under power fault.

**Status:** grounded as a cross-case/controller-level distinction; **not** an Intel-320-specific failure claim.

### G-15.6 — `interface contract ≠ empirical implementation compliance`

**Evidence:** ATA draft defines flush completion semantics; FAST ’13 shows that fault-injection behavior must be tested as a separate evidence layer.

**Status:** grounded methodological control.

---

## Claims deliberately not made

### X-15.1 — “Intel invented SSD power-loss protection”

Not established or needed.

### X-15.2 — “the SSD 320 has no volatile state”

Contradicted by Intel's temporary-buffer description and write-cache interface.

### X-15.3 — “FLUSH CACHE support alone proves every power-fault outcome is correct”

Rejected. Contract/support and empirical compliance are separate evidence classes.

### X-15.4 — “FAST ’13 proves the Intel SSD 320 failed under injected power cuts”

Rejected. Device identities are anonymized.

### X-15.5 — “the hold-up capacitors are the persistent data medium”

Rejected. They are an energy reserve enabling transfer to NAND.

### X-15.6 — “this case establishes `fsync`, filesystem crash consistency, or NVMe persistence domains”

Rejected. Those semantics live above or in different interfaces and require separate evidence.

---

## Related-repository duplication check

Before writing, `tmzncty/computing-archaeology` was searched for combinations of:

- SSD power loss;
- flush / volatile write cache;
- controller cache;
- FTL durability;
- capacitor / power-loss protection.

No dedicated existing case was found in that repository by those searches. The present slice therefore adds only the retention-specific boundary and links conceptually back to Case 04 rather than duplicating generic SSD/Flash history.

---

## Promotion judgment

**Case 15 status: `grounded`.**

Why promotion is justified:

- direct period standards-development text supplies the volatile-cache / nonvolatile-media and flush-completion vocabulary;
- direct Intel-hosted product/design material supplies the named SSD 320 power-fail mechanism and clean/unsafe-shutdown distinction;
- the Intel product specification supplies actual named-product FLUSH / write-cache command support, with the mirror provenance explicitly qualified;
- independent high-quality FAST ’13 research supplies a counterexample boundary that prevents manufacturer/interface evidence from being overgeneralized;
- historical record, engineering reconstruction, functional analogy, and philosophical interpretation remain separated;
- the source set yields concrete failure modes and does not depend on a single loose analogy.

Future work should **not** turn this into a generic SSD chapter. Distinct later cases may examine filesystem crash consistency, NVMe volatile-write-cache / FUA / persistence-domain semantics, enterprise PLP qualification, or controller-metadata recovery, but they are not hidden promotion blockers for this bounded case.
