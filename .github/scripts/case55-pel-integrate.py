from pathlib import Path

case_path = Path("cases/55-nvme-smart-health-endurance-telemetry.md")
roadmap_path = Path("ROADMAP.md")
index_path = Path("CASE_INDEX.md")


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one marker, found {count}")
    return text.replace(old, new, 1)


case = case_path.read_text(encoding="utf-8")

old = """The case establishes that an SSD can retain cumulative health/endurance evidence across power cycles and expose it to host software without that evidence being the user payload or a complete physical wear history.

Grounding record: [`../evidence/55-nvme10-13-smart-health-endurance-grounding.md`](../evidence/55-nvme10-13-smart-health-endurance-grounding.md).
"""
new = """The case establishes that an SSD can retain cumulative health/endurance evidence across power cycles and expose it to host software without that evidence being the user payload or a complete physical wear history. A further NVMe 1.4 deepening adds Persistent Event Log as a later, explicitly selective event-history layer and separates log persistence from completeness, immutability, lossless abrupt-power-failure capture, and sanitization verification.

Grounding record: [`../evidence/55-nvme10-13-smart-health-endurance-grounding.md`](../evidence/55-nvme10-13-smart-health-endurance-grounding.md).

Persistent-event-log deepening: [`../evidence/55-nvme14-2019-persistent-event-log-deepening.md`](../evidence/55-nvme14-2019-persistent-event-log-deepening.md).
"""
case = replace_once(case, old, new, "status")

old = """- the distinction between cumulative/lifetime information and the current `Critical Warning` state.

This is not a general history of SMART, NAND endurance, wear leveling, SSD failure prediction, or enterprise fleet management."""
new = """- the distinction between cumulative/lifetime information and the current `Critical Warning` state;
- NVMe 1.4 `Persistent Event Log` as selected typed history, including persistence, suppression/deletion, reporting-context, periodic SMART-snapshot, and sanitize-modification boundaries.

This is not a general history of SMART, NAND endurance, wear leveling, SSD failure prediction, persistent logging, or enterprise fleet management."""
case = replace_once(case, old, new, "scope")

historical = """### NVMe 1.4 adds a persistent but explicitly selective event-history layer

The **NVM Express Base Specification Revision 1.4, 10 June 2019** adds a distinct historical interface to the health/endurance state already covered above. NVM Express's own `Changes in NVMe Revision 1.4` page lists **Persistent Event Log (PEL)** as a new optional feature, and normative §5.14.1.13 defines Log Identifier `0Dh`. This is a revision boundary, not an invention claim: Case 55 already grounds a bounded ATA/ATAPI-5 self-test history in 1999.

PEL significant-event information is required to persist across **power cycles and resets**, and the log is global to the NVM subsystem. The immediately following power-failure wording is weaker: implementations **should** be designed for minimal event-information loss upon power failure. The source therefore supports `reset/power-cycle persistence != guaranteed lossless abrupt-power-failure capture`.

The history is explicitly selective. Event count and maximum size are vendor-specific; repeated same events may be suppressed above a vendor-specific frequency threshold; and deletion policy is vendor-specific when size/count/category bounds are reached. The specification even permits an older important event to be retained while a newer event is deleted. PEL is therefore persistent history under retention policy, not a complete FIFO archive.

Revision 1.4 defines heterogeneous events including SMART/Health snapshots, firmware commits, timestamp changes, power-on/reset, subsystem hardware errors, namespace changes, separate Format NVM and Sanitize **start/completion** events, feature changes, telemetry creation, thermal excursions, and vendor/TCG events. When PEL is supported, SMART/Health snapshot events are created at least once every **24 power-on hours** for the controller scope specified by the virtualization rules. A historical SMART snapshot still remains an interface/model snapshot rather than a raw NAND/FTL event history.

PEL retrieval has its own read-consistency boundary. A host may establish a reporting context, read the data associated with it, and release it. Events occurring while that context exists are still logged but are not reported in the existing context. Thus `reporting context != frozen underlying log`.

Finally, Revision 1.4 explicitly permits **sanitize** to remove or modify PEL events to prevent derivation of user data, with removed events unspecified. Persistence therefore does not mean immutability. Conversely, a PEL `Sanitize Completion` event records an interface-visible episode; it is not independent forensic verification that every stale physical embodiment became unrecoverable.

Deepening record: [`../evidence/55-nvme14-2019-persistent-event-log-deepening.md`](../evidence/55-nvme14-2019-persistent-event-log-deepening.md).

"""
case = replace_once(case, "## Retained states and their different meanings\n", historical + "## Retained states and their different meanings\n", "historical insert")

retained = """### 7. Selected persistent event history

NVMe 1.4 PEL retains typed evidence about selected device/subsystem events across resets and power cycles. Unlike a cumulative counter, an entry can retain an event category, timestamp, and event-specific data; unlike a complete audit archive, the log remains subject to vendor-specific capacity, repeated-event suppression, and deletion policy. Periodic SMART/Health snapshot events add a historical form of the health interface without exposing a complete physical-media history.

"""
case = replace_once(case, "## Engineering reconstruction\n", retained + "## Engineering reconstruction\n", "retained-state insert")

engineering = """### Persistent event history is not complete or immutable event history

PEL is persistent across named reset/power-cycle boundaries, but the same specification permits repeated-event suppression, vendor-specific deletion under bounds, and sanitize-driven removal/modification. Therefore **`persistent event history != complete event history`** and **`persistent != immutable`**. A reporting context stabilizes a selected read view while newer events continue to be logged, so retrieval-view stability and ongoing history accumulation are separate relations.

The periodic SMART/Health snapshot is also not a raw-media ledger. It does not disclose every ECC correction, FTL move, NAND program/erase, garbage-collection copy, read-reclaim decision, or per-cell threshold state. Therefore **`historical SMART snapshot != complete physical-media history`** and **`snapshot cadence != media-maintenance cadence`**.

The separate Sanitize Start and Sanitize Completion event types fix another boundary: **`operation start != operation completion != independent verification of physical forgetting`**. The event record documents interface state; it does not become a forensic audit of every physical embodiment.

"""
case = replace_once(case, "## Relation to existing cases\n", engineering + "## Relation to existing cases\n", "engineering insert")

old = """- a healthy-looking interface report does not independently verify hidden physical wear distribution or future failure time.

The repository should therefore reject `SMART says healthy` as a synonym for `all retained payload is safe indefinitely`."""
new = """- a healthy-looking interface report does not independently verify hidden physical wear distribution or future failure time;
- PEL persistence does not imply every event survives every abrupt power failure;
- repeated-event suppression and bounded-log deletion mean retained event history may be intentionally incomplete;
- sanitize may deliberately remove or modify some persistent-event history.

The repository should therefore reject `SMART says healthy` as a synonym for `all retained payload is safe indefinitely`, and reject `persistent log` as a synonym for `complete immutable archive`."""
case = replace_once(case, old, new, "failure boundaries")

prior = """NVMe 1.4 adds a later standards-history boundary: NVM Express's own revision ledger identifies Persistent Event Log as a new optional NVMe feature by June 2019. That does not make NVMe 1.4 the invention of retained drive history. The already-grounded 1999 ATA/ATAPI-5 21-entry circular self-test log is an explicit earlier counterexample. The useful comparison is narrower: ATA retains bounded self-test diagnostic records, whereas NVMe 1.4 standardizes a heterogeneous event-history interface with explicit suppression/deletion, reporting-context, periodic SMART-snapshot, and sanitize-modification rules. No direct ATA→NVMe genealogy is asserted, and TP4007a/4042a proposal chronology remains open until those proposals are independently inspected.

"""
case = replace_once(case, "## Philosophical interpretation — bounded\n", prior + "## Philosophical interpretation — bounded\n", "prior-art insert")

old = """The case therefore sharpens a distinction between **retaining the thing** and **retaining evidence about the remaining conditions of retention**.

That is a project-level interpretation. It is not terminology attributed to NVM Express or Intel."""
new = """NVMe 1.4 adds a second bounded conceptual problem: retained history itself is governed by admission, suppression, finite capacity, retrieval context, priority/deletion, and sanitization rules. A device can preserve a history of its operation while also being authorized to forget selected parts of that history.

The case therefore sharpens a distinction between **retaining the thing**, **retaining evidence about the remaining conditions of retention**, and **retaining a selected history of operations/events**.

That is a project-level interpretation. It is not terminology attributed to NVM Express or Intel."""
case = replace_once(case, old, new, "philosophy insert")

old = """| NVMe health telemetry is historically/technically identical to Cassandra repair state or DDR5 RAA | `X` | rejected; functional analogy only |

## Sources
"""
new = """| NVMe health telemetry is historically/technically identical to Cassandra repair state or DDR5 RAA | `X` | rejected; functional analogy only |
| NVMe 1.4 adds Persistent Event Log as a new optional NVMe feature | `H/P` | first-party revision/spec boundary; not invention proof |
| PEL persists across power cycles/resets while power-failure language only recommends minimizing event-information loss | `H/P/E` | modal distinction; not a lossless-abrupt-failure guarantee |
| PEL may suppress repeated events and delete entries under vendor-specific bounded-history policy | `H/P/E` | `persistent event history != complete event history` |
| PEL reporting context excludes newly occurring events from its existing view while those events continue to be logged | `H/P/E` | `reporting context != frozen underlying log` |
| sanitize may remove/modify PEL events to prevent user-data derivation | `H/P/E` | `persistent != immutable` |
| a PEL Sanitize Completion event independently verifies physical media sanitization | `X` | rejected; event history is not forensic verification |

## Sources
"""
case = replace_once(case, old, new, "claim rows")

old = """10. T13, **AT Attachment with Packet Interface - 5 (ATA/ATAPI-5), Working Draft T13/1321D Revision 2**, 13 December 1999; period draft transcription/mirror used for revision history and §§8.41.4–8.41.6: <https://studylib.net/doc/25730948/ata-atapi-5>

## Related repositories
"""
new = """10. T13, **AT Attachment with Packet Interface - 5 (ATA/ATAPI-5), Working Draft T13/1321D Revision 2**, 13 December 1999; period draft transcription/mirror used for revision history and §§8.41.4–8.41.6: <https://studylib.net/doc/25730948/ata-atapi-5>
11. NVM Express, **NVM Express Base Specification, Revision 1.4**, 10 June 2019, especially §5.14.1.13 and §5.14.1.13.1: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf>
12. NVM Express, **Changes in NVMe Revision 1.4**, first-party revision summary: <https://nvmexpress.org/changes-in-nvme-revision-1-4/>

## Related repositories
"""
case = replace_once(case, old, new, "source append")

old = """A fresh repository search found no dedicated NVMe SMART/endurance or ATA SMART/SFF-8035i/ATA5 self-test case in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). Broader SMART/ATA/NVMe health-monitoring genealogy and disk/SSD engineering chronology should remain there if developed; this case keeps only the retention-specific state/history, diagnostic-history, and interface-boundary distinctions."""
new = """A fresh repository search found no dedicated NVMe SMART/endurance, Persistent Event Log, or ATA SMART/SFF-8035i/ATA5 self-test case in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). Broader SMART/ATA/NVMe health-monitoring and event-log genealogy, proposal history, product adoption, and disk/SSD engineering chronology should remain there if developed; this case keeps only the retention-specific state/history, diagnostic-history, and interface-boundary distinctions."""
case = replace_once(case, old, new, "related-repo update")

case_path.write_text(case, encoding="utf-8")

roadmap = roadmap_path.read_text(encoding="utf-8")
marker = "## Phase 2 — Build missing technical bridges\n\n"
bullet = """- [x] **Case 55 NVMe 1.4 Persistent Event Log deepening:** [`cases/55-nvme-smart-health-endurance-telemetry.md`](cases/55-nvme-smart-health-endurance-telemetry.md) + [`evidence/55-nvme14-2019-persistent-event-log-deepening.md`](evidence/55-nvme14-2019-persistent-event-log-deepening.md) add the official 10-June-2019 Revision-1.4 PEL boundary above the existing SMART/Health and ATA self-test-history evidence. The slice separates reset/power-cycle persistence from lossless abrupt-power-failure capture, typed event history from cumulative counters, finite/suppressed/deletion-governed history from a complete archive, an established reporting context from the still-growing underlying log, and periodic SMART snapshots from raw physical-media history. It also records the normative rule that sanitize may remove/modify PEL events, fixing `persistent != immutable` and `sanitize-completion event != independently verified physical erasure`. ATA/ATAPI-5's 1999 circular self-test log remains the earlier bounded diagnostic-history prior-art floor; direct ATA→NVMe genealogy, TP4007a/4042a proposal chronology, named-product PEL behavior, controller internals, and abrupt-power-loss compliance testing remain open and should be coordinated with `computing-archaeology`.

"""
if "Case 55 NVMe 1.4 Persistent Event Log deepening" in roadmap:
    raise SystemExit("roadmap bullet already present")
roadmap = replace_once(roadmap, marker, marker + bullet, "roadmap")
roadmap_path.write_text(roadmap, encoding="utf-8")

index = index_path.read_text(encoding="utf-8")
if "## Case 55 deepening — NVMe 1.4 Persistent Event Log / selected device history" in index:
    raise SystemExit("CASE_INDEX section already present")
if "**3420 — X:**" not in index:
    raise SystemExit("expected latest finding 3420 not found")
section = """

## Case 55 deepening — NVMe 1.4 Persistent Event Log / selected device history

Grounding: [`cases/55-nvme-smart-health-endurance-telemetry.md`](cases/55-nvme-smart-health-endurance-telemetry.md) and [`evidence/55-nvme14-2019-persistent-event-log-deepening.md`](evidence/55-nvme14-2019-persistent-event-log-deepening.md).

- **3421 — H/P:** NVM Express Base Specification Revision 1.4 is dated 10 June 2019, and NVM Express's first-party Revision-1.4 change ledger identifies Persistent Event Log as a new optional feature in that revision; this is a revision boundary, not an invention date.
- **3422 — H/P:** PEL significant-event information is retained across power cycles and resets and the log is global to the NVM subsystem.
- **3423 — H/P/E:** Revision 1.4 separately says subsystems `should` be designed for minimal event-information loss upon power failure, so `retained across reset/power cycle != guaranteed lossless abrupt-power-failure capture`.
- **3424 — H/P:** PEL event count and maximum supported size are vendor-specific.
- **3425 — H/P:** Repeated occurrences of the same supported event may be suppressed after a vendor-specific frequency threshold is exceeded.
- **3426 — H/P:** When size/count/category bounds are reached, deletion policy is vendor-specific; an older important event may be retained while a newer event is deleted.
- **3427 — E:** `persistent event history != complete event history`; persistence does not remove admission, suppression, capacity, and deletion policy.
- **3428 — H/P:** Standard PEL categories include SMART/Health snapshot, firmware commit, timestamp change, power-on/reset, subsystem hardware error, namespace change, separate Format/Sanitize start and completion, Set Features, telemetry creation, thermal excursion, and vendor/TCG events.
- **3429 — H/P:** When PEL is supported, Revision 1.4 requires SMART/Health snapshot events at least once every 24 power-on hours under the specified controller/virtualization scope.
- **3430 — E:** `periodic SMART snapshot != complete raw-media history != media-maintenance cadence`; a historical snapshot retains the standardized health abstraction rather than hidden NAND/FTL events.
- **3431 — H/P:** A host can establish/read/release a PEL reporting context; events occurring while that context exists continue to be logged but are excluded from the existing context.
- **3432 — E:** `reporting context != frozen underlying log`; retrieval-view stability and ongoing event accumulation are separate relations.
- **3433 — H/P:** Sanitize may remove or modify PEL events to prevent derivation of user data, and which events are removed is unspecified.
- **3434 — E:** `persistent != immutable`; ordinary diagnostic-history retention may yield to a stronger sanitization/forgetting policy.
- **3435 — H/P/A:** ATA/ATAPI-5's grounded 1999 21-entry circular self-test log is earlier prior art for bounded retained device diagnostic history; PEL is a later heterogeneous standardized event-history interface, with no direct ATA→NVMe genealogy asserted.
- **3436 — X:** PEL does not by itself prove complete/lossless device history, hidden NAND/FTL algorithm, proposal-level invention priority, direct ATA→NVMe lineage, or independent verification that a recorded sanitize completion made every prior embodiment unrecoverable.
"""
index = index.rstrip() + section + "\n"
index_path.write_text(index, encoding="utf-8")

for path in (case_path, roadmap_path, index_path):
    text = path.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        path.write_text(text + "\n", encoding="utf-8")
