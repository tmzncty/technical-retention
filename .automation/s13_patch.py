from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text()
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{path}: expected one anchor, found {n}")
    p.write_text(text.replace(old, new))


readme_anchor = "A bounded integrity-qualified-coded-recovery comparison is now available in [`docs/SYNTHESIS_12_INTEGRITY_QUALIFIED_CODED_RECOVERY.md`](docs/SYNTHESIS_12_INTEGRITY_QUALIFIED_CODED_RECOVERY.md). Across grounded RAID-6, Swift EC, Ceph EC, and OpenZFS dRAID cases it separates coded contribution presence, version/currentness qualification, checksum/integrity evidence, integrity-metadata authority, verification coverage, diagnostic fault-location evidence, repair-source admissibility, algebraic decode sufficiency, repaired redundancy margin, and later revalidation. It also fixes the counterexamples `more parity ≠ stronger corruption diagnosis`, `checksum mismatch ≠ fault localization`, and `restored coded margin ≠ restored integrity confidence`.\n"
readme_new = readme_anchor + "\nA bounded durability-handoff comparison is now available in [`docs/SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md`](docs/SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md). Across grounded SCSI, NVMe, Intel SSD power-loss-protection, SNIA persistent-memory, ADR/eADR, and PLI-validation cases it separates ordinary completion/store execution, intermediate cache or buffer residence, persistence-control scope, cross-update ordering, persistence-boundary arrival, covered failure model, failure-triggered transfer capability, retention-infrastructure readiness, power-fail atomicity, post-failure recoverability, and higher-layer crash-consistency closure. It fixes the counterexamples `completion ≠ durability`, `FUA persistence ≠ global ordering`, `sync ≠ atomicity`, `persistence-domain arrival ≠ unconditional recovery`, and `power-fail protected ≠ already in final media`.\n"
replace_once("README.md", readme_anchor, readme_new)

phase3_a = "- [ ] How should `command completion`, `volatile-cache residence`, `nonvolatile-media commitment`, `cross-command ordering`, and `power-fail atomicity` be separated at storage interfaces?"
phase3_a_new = "- [x] At storage interfaces, separate `command completion`, `current/cache residence`, `explicit persistence-control scope`, `nonvolatile-media or persistence-boundary commitment`, `cross-command ordering`, `normal atomicity`, and `power-fail atomicity` — closed at the bounded cross-case relation level by [`docs/SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md`](docs/SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md), using grounded Cases 15, 20, 38, and 87. SCSI/NVMe command genealogy, named-controller conformance/fault injection, firmware internals, and end-to-end filesystem/database composition remain separate work."
replace_once("ROADMAP.md", phase3_a, phase3_a_new)

phase3_b = "- [ ] How should `store execution`, processor/controller-buffer residence, persistence-domain arrival, synchronization completion, failure-qualified recoverability, atomicity, and ordering be separated in persistent-memory programming models?"
phase3_b_new = "- [x] In persistent-memory programming models, separate `store execution`, processor/controller-buffer residence, persistence-domain arrival, synchronization completion, failure-qualified recoverability, atomicity, ordering, and power-fail-protected future transfer — closed at the bounded cross-case relation level by [`docs/SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md`](docs/SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md), using grounded Cases 31 and 32 with Cases 15/38 as named failure-transfer/readiness controls. Broader PMDK/DAX/ACPI/NVDIMM/platform genealogy, domain-volume-filesystem deployment validation, and fault injection remain open."
replace_once("ROADMAP.md", phase3_b, phase3_b_new)

replacements = [
    (
        "- [ ] loss of volatile controller/buffer state before a durability handoff;",
        "- [ ] loss of volatile controller/buffer state before a durability handoff — **relation structure advanced by Synthesis 13**: ordinary completion/currentness, intermediate residence, and persistence-boundary arrival are now separated; named-device loss rates, controller internals, and fault injection remain open;",
    ),
    (
        "- [ ] failed flush, shutdown transfer, or power-loss emergency transfer;",
        "- [ ] failed flush, shutdown transfer, or power-loss emergency transfer — **relation structure advanced by Synthesis 13**: host-requested flush, orderly-shutdown transfer, and device-triggered emergency handoff are distinct triggers/paths; implementation failure progression and independent validation remain open;",
    ),
    (
        "- [ ] FUA/Flush misuse, missing host-enforced ordering, or power-fail atomicity assumptions that exceed the interface contract;",
        "- [ ] FUA/Flush misuse, missing host-enforced ordering, or power-fail atomicity assumptions that exceed the interface contract — **relation structure advanced by Synthesis 13**: per-command persistence, cross-command ordering, normal atomicity, and power-fail atomicity are now explicitly separated; misuse incidence, later-revision semantics, and application-stack validation remain open;",
    ),
    (
        "- [ ] treating a mapped store or cache/controller-buffer residence as persistence-domain arrival; assuming sync supplies atomicity/order; failure patterns outside the configured domain; or domain/volume/filesystem misalignment;",
        "- [ ] treating a mapped store or cache/controller-buffer residence as persistence-domain arrival; assuming sync supplies atomicity/order; failure patterns outside the configured domain; or domain/volume/filesystem misalignment — **relation structure advanced by Synthesis 13**: SNIA persistence-domain arrival, failure-qualified recoverability, ADR/eADR domain expansion, and retained ordering obligations are now composed at the bounded relation level; empirical deployment misconfiguration, platform-specific domains, and failure injection remain open;",
    ),
]
for old, new in replacements:
    replace_once("ROADMAP.md", old, new)

idx = Path("CASE_INDEX.md")
text = idx.read_text().rstrip()
expected_tail = "1477. **finite spare reserve = possible continuation resource, not ordinary user capacity** — as an engineering reconstruction across Cases 14, 55, and 78, reserved physical locations can support future re-embodiment while remaining distinct from user-addressable payload capacity; the comparison is functional, not genealogical."
if not text.endswith(expected_tail):
    raise SystemExit("CASE_INDEX.md: unexpected findings tail")
findings = r'''

1478. **command completion ≠ durable media commitment** — SCSI-2 write-back `GOOD` can precede physical-medium write, and NVMe 1.0 preserves stronger Flush/FUA controls; completion must be interpreted under the applicable cache/command contract.
1479. **newest/current cached state ≠ lower-medium currentness** — a write-back cache can temporarily hold the authoritative newest logical value while the lower physical medium still contains an older embodiment.
1480. **FUA per-command persistence ≠ global ordering** — NVMe 1.0 can require one FUA write to reach nonvolatile media before that command completes while explicitly leaving ordering with independent commands to host/application software.
1481. **Flush / synchronization completion ≠ atomicity** — SNIA persistence synchronization can establish boundary arrival without write atomicity; NVMe's separate AWUPF capability independently prevents durability from being treated as interruption atomicity.
1482. **normal atomicity ≠ power-fail atomicity** — NVMe 1.0 reports AWUN and AWUPF separately, so normal-operation atomic-write capability cannot be silently projected across power loss.
1483. **nonvolatile interface classification ≠ final physical-medium residency** — SBC-2 nonvolatile cache and NVMe's power-loss-guaranteed cache show that survival/transfer contracts can qualify intermediate state even when it remains controller-dependent or not yet in its final medium.
1484. **persistence-domain arrival ≠ unconditional recoverability** — SNIA conditions post-restart recovery on the actual failure pattern being tolerated by the domain's design/configuration; `durable` is failure-envelope qualified.
1485. **persistence-domain expansion ≠ elimination of ordering obligations** — Intel eADR can remove ADR-era cache-flush work while retaining `SFENCE`; a larger protected domain does not automatically supply multi-update crash consistency.
1486. **power-fail-protected state ≠ already-final nonvolatile embodiment** — Intel SSD 320 PLI and ADR/eADR provide bounded examples where protection can rest on a guaranteed future transfer funded by stored energy/control after failure begins.
1487. **emergency-transfer path existence ≠ verified readiness** — Intel PLI health/test telemetry makes the future protection apparatus itself maintained state whose condition and recency can be inspected separately from payload durability.
1488. **passing component self-test ≠ whole-device fault-survival proof** — Intel distinguishes partial capacitor self-test from broader repeated power-loss validation; component readiness evidence cannot be promoted into universal implementation compliance.
1489. **failure-triggered handoff ≠ host-requested flush ≠ orderly shutdown transfer** — Case 15 shows three routes that may converge on NAND while differing in trigger, authority, available time, energy, and observability.
1490. **power-cycle survival ≠ controller/media independence** — SBC-2's nonvolatile-cache boundary permits controller-resident state to survive power while still requiring medium synchronization before controller/media separation or beyond a bounded retention interval.
1491. **lower-layer persistence ≠ higher-layer crash consistency** — individually durable writes can still violate filesystem/database dependency ordering; device/persistence-domain guarantees must compose with a higher-level closure protocol.
1492. **durability-handoff synthesis ≠ one universal pipeline or historical genealogy** — SCSI cache commands, NVMe namespace semantics, Intel SSD PLI, SNIA mapped persistent memory, ADR/eADR, and PLI validation are compared only at the relation level; their command sets, physical mechanisms, failure envelopes, and historical lineages remain distinct.
'''
idx.write_text(text + findings)

assert "SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md" in Path("README.md").read_text()
assert Path("ROADMAP.md").read_text().count("SYNTHESIS_13_DURABILITY_HANDOFF_PERSISTENCE_DOMAIN.md") >= 2
assert "1492. **durability-handoff synthesis ≠ one universal pipeline or historical genealogy**" in idx.read_text()
