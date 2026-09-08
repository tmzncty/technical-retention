from pathlib import Path

CASE_PATH = Path("cases/15-intel-ssd320-power-loss-durability.md")
EVIDENCE_PATH = Path("evidence/15-intel-ssd320-power-loss-durability-grounding.md")
ROADMAP_PATH = Path("ROADMAP.md")
INDEX_PATH = Path("CASE_INDEX.md")

CASE_MARKER = "### H/P + H/S — August 2011 firmware history adds a named-product unsafe-power-loss recovery defect"
EVIDENCE_MARKER = "### Source F — Intel SSD Firmware Update Tool release-history compilation, preserving the August 2011 SSD 320 entry"
FINDINGS_MARKER = "## Case 15 deepening — named SSD 320 unsafe-power-loss recovery findings"

CASE_BLOCK = r'''### H/P + H/S — August 2011 firmware history adds a named-product unsafe-power-loss recovery defect

A later Intel-authored Firmware Update Tool release-note compilation preserves the SSD 320 revision history and records firmware `4PC10362` in **August 2011** as fixing issues related to `BAD_CTX 13x`, an **8 MB capacity** failure associated with unsafe power-loss situations. The surviving copy inspected is a mirror of Intel document **328292-030US** (April 2019), not current Intel hosting. Contemporary reporting from 17–18 August 2011 independently records the same firmware revision and public symptom description.

This changes the evidence boundary of the case. The March 2011 Intel brief remains strong primary evidence for the documented power-fail detector / hold-up-capacitance / emergency-transfer architecture, but the August revision history shows that **having that architecture did not make unsafe-shutdown recovery bug-free**. A named product with explicit enhanced power-loss protection still required a firmware repair for a power-loss-associated recovery/context failure severe enough to collapse the host-visible capacity surface to 8 MB.

The release history does **not** disclose the internal structure represented by `BAD_CTX`, does not say that NAND payload was physically erased, and does not identify whether the fault lay in FTL mapping, capacity metadata, startup recovery state, another controller structure, or an interaction among them. The correct historical claim is therefore narrower than many later retellings:

> **Intel documented an SSD 320 firmware defect associated with unsafe power loss and an 8 MB capacity symptom, then documented firmware 4PC10362 as fixing issues related to that defect.**

Primary release-history anchor (Intel-authored document on a surviving non-Intel mirror): <https://downloads.bl4ckb0x.de/downloadcenter.intel.com/28749/eng/Intel_SSD_Firmware_Update_Tool_3_0_7_Release_Notes-328292-030US.pdf>

Contemporary secondary corroboration: Tom's Hardware, 18 August 2011, <https://www.tomshardware.com/news/intel-320-ssd-bug-8mb-firmware%2C13250.html>.

### E — protection architecture ≠ recovery correctness

The named-product history supplies a sharper counterexample than the anonymized FAST '13 population alone:

```text
documented power-loss protection path
        ≠
proof that every unsafe-shutdown recovery transition is correct
```

Protection hardware can preserve energy and permit emergency transfer while firmware/recovery logic still contains a defect in the state needed to re-present the device correctly after restart.

### E — host-visible capacity ≠ physical media population

The 8 MB symptom is an observation at the controller/interface surface. It therefore demonstrates a failure of **presented capacity/addressability**, not by itself destruction of all NAND beyond 8 MB. This is a mechanism-sensitive negative claim: the source set does not reveal how much user payload physically survived, whether it remained internally reachable, or which controller relation failed.

### E/A — recovery-context failure may be compared with mapping/currentness loss, but not identified with it

Case 39 shows directly that Flash payload can survive while runtime mapping/currentness state must be reconstructed after power failure. That is a useful **functional analogy** for understanding why a controller can lose logical reachability without proving physical erasure. It is not evidence that `BAD_CTX 13x` was specifically an FTL-map failure.

Cases 122–123 similarly show, under intentional ATA HPA/DCO control, that host-visible capacity can differ from a broader native/selectable population. Their use here is only relational: **presented capacity is controller-mediated state**. An involuntary `BAD_CTX` recovery failure is not historically or technically the same mechanism as SET MAX or DCO.

'''

EVIDENCE_SOURCE = r'''### Source F — Intel SSD Firmware Update Tool release-history compilation, preserving the August 2011 SSD 320 entry

**Document:** Intel Corporation, _Intel Solid State Drive Firmware Update Tool Release Notes_, Revision 3.0.7, April 2019, document 328292-030US; SSD 320 Series Revision History on printed p. 18.

**Inspection:** searchable PDF text plus direct source inspection. The surviving copy is hosted on a non-Intel mirror whose path preserves the former Intel Download Center filename; this record treats the document as identifiable Intel-authored release notes, not as current Intel hosting.

**Evidence class:** `H/P` for the Intel-authored firmware revision record, with source-host provenance explicitly qualified.

**Directly establishes:**

- the SSD 320 revision-history entry dates firmware `4PC10362` to **August 2011**;
- Intel's revision description ties that firmware to fixes for `BAD_CTX 13x` / **8 MB capacity** problems associated with unsafe power-loss situations;
- a named SSD 320 product family with documented enhanced power-loss protection still had a later firmware-level unsafe-shutdown recovery problem requiring remediation.

**Does not establish:**

- the internal representation or root cause of `BAD_CTX`;
- that the protection capacitors, power-fail detector, or NAND-transfer path themselves were defective;
- how much user payload physically survived when the 8 MB symptom occurred;
- whether post-fix firmware eliminates every possible unsafe-power-loss failure.

Surviving copy inspected: <https://downloads.bl4ckb0x.de/downloadcenter.intel.com/28749/eng/Intel_SSD_Firmware_Update_Tool_3_0_7_Release_Notes-328292-030US.pdf>

### Source G — contemporary public reporting of the Intel 320 8 MB firmware fix, August 2011

**Document:** Marcus Yam, “Intel Releases New SSD Firmware to Fix 8 MB Bug,” _Tom's Hardware_, 18 August 2011.

**Evidence class:** `S` — contemporary secondary corroboration of the public release and symptom description.

**Directly supports:** firmware 4PC10362 was publicly released in August 2011 for the SSD 320 `BAD_CTX 13x` / 8 MB problem, with the problem described as occurring after unexpected power loss under specific conditions.

**Boundary:** use this source to corroborate public chronology/symptoms, not to reverse-engineer the controller. The Intel-authored release history remains the stronger anchor for the firmware revision itself.

<https://www.tomshardware.com/news/intel-320-ssd-bug-8mb-firmware%2C13250.html>

'''

EVIDENCE_CLAIMS = r'''### G-15.7 — documented PLP architecture ≠ bug-free unsafe-shutdown recovery

**Evidence:** Intel's March 2011 design brief documents the power-fail/hold-up/emergency-transfer path; Intel's preserved August 2011 revision history documents firmware 4PC10362 as fixing `BAD_CTX 13x` / 8 MB issues associated with unsafe power loss.

**Status:** grounded named-product historical boundary. It does not identify which internal submechanism failed.

### G-15.8 — host-visible capacity collapse ≠ proof of physical NAND population collapse

**Evidence:** the documented symptom is an 8 MB capacity presentation. Neither Intel release history nor the contemporary public report establishes that NAND beyond that boundary was physically erased.

**Status:** engineering reconstruction / negative boundary.

### G-15.9 — firmware remediation ≠ retroactive data-recovery proof

**Evidence:** 4PC10362 is documented as fixing issues related to the failure mode. The source does not say that installing the firmware after a drive has already entered the bad state restores all user data or proves its prior physical survival.

**Status:** evidence-boundary claim.

### G-15.10 — named-product failure history ≠ independent post-fix conformance testing

**Evidence:** Source F identifies the SSD 320 family and its fix; Zheng et al. independently inject power faults but anonymize device identities.

**Status:** grounded methodological separation. Independent fault-injection validation of a named SSD 320 before/after 4PC10362 remains open.

'''

OLD_POWER_LOSS = "- [ ] power loss — **partially advanced at the access-authority layer by grounded Case 126**: NVMe 1.1 makes reservation/registration state survive ordinary controller/subsystem resets while namespace-specific `PTPL` separately decides whether that coordination state survives a reset due to power loss. This grounds `controller-reset persistence ≠ power-loss persistence` and `payload survival ≠ access-authority survival` for one shared-storage protocol; physical-state loss, volatile-payload loss, controller-internal implementation, named-device fault behavior, and broader power-failure mechanisms remain open;"
NEW_POWER_LOSS = "- [ ] power loss — **substantially advanced at the SSD-device and access-authority layers by grounded Cases 15 and 126**: Case 15 separates volatile staging, explicit flush, orderly shutdown, and capacitor-backed unsafe-power-loss transfer, and its August-2011 firmware-history deepening now adds a named Intel SSD 320 recovery defect/fix (`BAD_CTX 13x`, 8 MB capacity) without guessing the hidden controller root cause; Case 126 separately shows that NVMe reservation/registration coordination state can survive ordinary resets while namespace-specific `PTPL` controls survival across power-loss reset. Together these ground `documented protection architecture ≠ bug-free recovery`, `host-visible capacity ≠ physical media population`, `controller-reset persistence ≠ power-loss persistence`, and `payload durability ≠ access-authority durability`. Independent named-device post-fix fault injection, exact BAD_CTX internal cause, physical-cell loss, other controller families/media, and broader power-failure genealogies remain open;"

OLD_CASE_ROW = "| [Intel SSD 320 Power-Loss Protection: Volatile Staging, Flush, and Emergency Retention Work](cases/15-intel-ssd320-power-loss-durability.md) | **grounded** | nonvolatile NAND behind volatile controller/buffer state + explicit flush-to-media boundary + clean-shutdown handoff + power-failure-triggered emergency transfer using stored capacitor energy | separate medium nonvolatility from end-to-end durability; distinguish explicit flush, orderly shutdown, and unsafe-power-loss paths; treat stored energy as retention infrastructure rather than payload; separate interface contract from measured fault behavior | [2007–2013 SSD power-loss durability grounding](evidence/15-intel-ssd320-power-loss-durability-grounding.md); manufacturer-primary enterprise PLI health/validation is now handled separately in Case 38, while independent named-product PLP compliance, filesystem `fsync`, NVMe persistence composition, and generic SSD history remain separate work |"
NEW_CASE_ROW = "| [Intel SSD 320 Power-Loss Protection: Volatile Staging, Flush, and Emergency Retention Work](cases/15-intel-ssd320-power-loss-durability.md) | **grounded** | nonvolatile NAND behind volatile controller/buffer state + explicit flush-to-media boundary + clean-shutdown handoff + capacitor-backed failure-triggered transfer + named unsafe-power-loss firmware recovery defect/fix | separate medium nonvolatility from end-to-end durability; explicit flush from shutdown paths; protection architecture from recovery correctness; host-visible capacity from physical media population; contract from measured compliance | [2007–2013 grounding](evidence/15-intel-ssd320-power-loss-durability-grounding.md), now deepened with Intel's preserved August-2011 `4PC10362` / `BAD_CTX 13x` revision history; independent named-product post-fix fault injection, exact BAD_CTX internal cause, filesystem `fsync`, NVMe persistence composition, and generic SSD history remain separate work |"

FINDINGS = r'''## Case 15 deepening — named SSD 320 unsafe-power-loss recovery findings

- **2195 — documented PLP architecture ≠ bug-free unsafe-shutdown recovery:** Intel's March 2011 SSD 320 brief documents detector/firmware/hold-up-capacitance emergency retention work, while Intel's preserved August 2011 revision history records 4PC10362 fixes for `BAD_CTX 13x` / 8 MB problems associated with unsafe power loss. (`H/P`, `E`)
- **2196 — August 2011 firmware fix ≠ invention or mechanism-origin claim:** the revision history dates one named remediation event; it does not establish when the underlying recovery design originated or whether similar faults existed in other SSD families. (`H/P`, `X`)
- **2197 — 8 MB host-visible capacity ≠ 8 MB physical NAND population:** the failure symptom is controller-presented capacity; the inspected sources do not establish physical erasure or destruction of NAND beyond that range. (`E`, `X`)
- **2198 — BAD_CTX symptom ≠ established FTL-map root cause:** Case 39 makes mapping-recovery loss a useful functional analogy, but Intel's release history does not disclose whether `BAD_CTX` was mapping, capacity, startup-context, or another controller-state failure. (`A`, `X`)
- **2199 — firmware fix ≠ retroactive proof of payload recoverability:** documenting 4PC10362 as a fix does not prove that data on a drive already in the bad state remain physically intact or become recoverable merely by applying the update. (`H/P`, `E`, `X`)
- **2200 — named-product firmware history ≠ independent power-cut conformance test:** Intel identifies the SSD 320 revision; FAST '13 independently tests power faults but anonymizes device identities, so the two evidence classes must remain separate. (`H/P`, `S`, `X`)
- **2201 — unsafe-power-loss recovery ≠ FLUSH CACHE closure:** the firmware defect is associated with unsafe power-loss situations; it does not repeal ATA's explicit host-triggered flush boundary or prove that a completed flush itself caused the failure. (`H/P`, `E`)
- **2202 — capacity/addressability failure ≠ retention-medium failure:** the named symptom reinforces that post-restart usefulness depends on controller-mediated designation/resolution state as well as nonvolatile cells. (`E`)
- **2203 — Case 39 mapping recovery ≠ BAD_CTX mechanism identity:** both can exhibit surviving Flash plus damaged logical reachability, but no source currently proves that GeckoFTL-style or generic FTL mapping reconstruction describes the Intel 320 defect. (`A`, `X`)
- **2204 — HPA/DCO capacity indirection ≠ BAD_CTX failure:** Cases 122–123 intentionally retain control/configuration state that changes the host-visible capacity surface; Case 15's involuntary unsafe-shutdown symptom is only a relational comparison, not the same mechanism or genealogy. (`A`, `X`)
- **2205 — more protection infrastructure ≠ monotonically complete protection:** stored energy, detection hardware, firmware, and NAND handoff can reduce one failure window while leaving recovery/context correctness as an independent obligation. (`E`)
- **2206 — related-repository boundary:** a fresh `tmzncty/computing-archaeology` search found no dedicated SSD power-fault / Intel 320 `BAD_CTX` case to reuse; broad SSD/FTL implementation genealogy belongs there if developed, while this deepening remains focused on retention and recovery boundaries. (`H/P` project-state record)
'''


def insert_before(text: str, anchor: str, block: str, marker: str) -> str:
    if marker in text:
        return text
    if anchor not in text:
        raise RuntimeError(f"missing anchor: {anchor!r}")
    return text.replace(anchor, "\n" + block.rstrip() + "\n\n---\n\n" + anchor.split("---\n\n", 1)[1], 1) if anchor.startswith("\n---\n\n") else text.replace(anchor, block + anchor, 1)


def update_case():
    text = CASE_PATH.read_text(encoding="utf-8")
    if CASE_MARKER not in text:
        anchor = "\n---\n\n## Retained state\n"
        if anchor not in text:
            raise RuntimeError("Case 15 retained-state anchor missing")
        text = text.replace(anchor, "\n" + CASE_BLOCK.rstrip() + "\n\n---\n\n## Retained state\n", 1)
    CASE_PATH.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_evidence():
    text = EVIDENCE_PATH.read_text(encoding="utf-8")
    if EVIDENCE_MARKER not in text:
        anchor = "\n---\n\n## Grounded mechanism\n"
        if anchor not in text:
            raise RuntimeError("Evidence 15 grounded-mechanism anchor missing")
        text = text.replace(anchor, "\n" + EVIDENCE_SOURCE.rstrip() + "\n\n---\n\n## Grounded mechanism\n", 1)
    if "### G-15.7" not in text:
        anchor = "\n---\n\n## Claims deliberately not made\n"
        if anchor not in text:
            raise RuntimeError("Evidence 15 claim-boundary anchor missing")
        text = text.replace(anchor, "\n" + EVIDENCE_CLAIMS.rstrip() + "\n\n---\n\n## Claims deliberately not made\n", 1)
    EVIDENCE_PATH.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_roadmap():
    text = ROADMAP_PATH.read_text(encoding="utf-8")
    if NEW_POWER_LOSS not in text:
        if OLD_POWER_LOSS not in text:
            raise RuntimeError("ROADMAP power-loss boundary changed")
        text = text.replace(OLD_POWER_LOSS, NEW_POWER_LOSS, 1)
    ROADMAP_PATH.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_index():
    text = INDEX_PATH.read_text(encoding="utf-8")
    if NEW_CASE_ROW not in text:
        if OLD_CASE_ROW not in text:
            raise RuntimeError("CASE_INDEX Case 15 row changed")
        text = text.replace(OLD_CASE_ROW, NEW_CASE_ROW, 1)
    if FINDINGS_MARKER not in text:
        if "**2194" not in text:
            raise RuntimeError("CASE_INDEX expected tail 2194 missing")
        text = text.rstrip() + "\n\n" + FINDINGS.rstrip() + "\n"
    INDEX_PATH.write_text(text.rstrip() + "\n", encoding="utf-8")


update_case()
update_evidence()
update_roadmap()
update_index()
