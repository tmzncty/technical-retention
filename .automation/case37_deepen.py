from pathlib import Path

EVIDENCE_PATH = Path('evidence/37-samsung-2014-restoration-transaction-deepening.md')

EVIDENCE = r'''# Case 37 Deepening — Samsung 840 EVO 2014 Restoration Transaction, Admission, and Interruption Boundary

## Purpose

This record deepens [`../cases/37-samsung-840-evo-old-data-performance-refresh.md`](../cases/37-samsung-840-evo-old-data-performance-refresh.md) without reopening the already-grounded 2014–2015 old-data-performance chronology.

The bounded question is narrower:

> When Samsung's October 2014 Performance Restoration package was used, what had to be true for the maintenance path to be available, what stages did the operation expose, and what did Samsung say could happen if that maintenance transaction was interrupted?

The answer adds a maintenance-admission and transaction-safety layer to Case 37. It does **not** expose Samsung's internal NAND rewrite algorithm, prove a particular crash-atomic implementation, or establish that every 840 EVO restoration attempt succeeded.

## Evidence classes and provenance

### A. Manufacturer-primary support ledgers — surviving artifact identity

Samsung's current US Business support page for the 1 TB 840 EVO still lists October 2014 Performance Restoration downloads. The ledger records:

- 28 October 2014 — DOS `Update Software` v1.0 artifacts;
- 24 October 2014 — Windows `Update Software` v1.1 artifacts;
- a current note that users who already restored performance with `Samsung Performance Restoration v.1.0` do not need to use v1.1.

Source: <https://www.samsung.com/us/business/support/owners/product/840-evo-series-1tb/>.

Samsung Australia's current support page for model `MZ-7TE500` preserves a more specific first-party artifact ledger. It identifies, among other files:

- `Samsung_Performance_Restoration.iso`, v1.0, 28 October 2014, file ID `5880447`;
- `Samsung_Performance_Restoration_USB_Bootable.zip`, v1.0, 28 October 2014, file ID `5880448`;
- `Samsung_Performance_Restoration_DOS_v10.pdf`, v1.0, 28 October 2014, file ID `5880449`;
- `Samsung_Performance_Restoration_V11.zip`, v1.1, 24 October 2014, file ID `5870447`;
- `Samsung_Performance_Restoration_v11.pdf`, v1.1, 24 October 2014, file ID `5870448`.

Source: <https://www.samsung.com/au/support/model/MZ-7TE500BW/>.

These current manufacturer pages establish artifact identity, product scope, dates, versions, and surviving support metadata. They do **not** by themselves establish every instruction inside the historical PDF body.

A present-day support-page annotation that the old tool `does not work` is treated only as a **current access/support-state observation**. It must not be projected backward as evidence that the tool did not work in October 2014.

### B. Manufacturer-authored October 2014 guide body preserved through secondary document mirrors

The exact historical guide filenames above are independently anchored by Samsung's surviving first-party ledger, but the currently inspected body text is available through third-party document mirrors rather than a directly rendered Samsung-hosted PDF. That provenance distinction is retained explicitly.

A mirrored copy of the Samsung-authored Windows **Performance Restoration Version 1.0** guide, marked `2014.10 (Rev 1.0)`, describes two separate features:

- `Firmware Update`;
- `SSD Performance Restoration`.

It gives a staged workflow in which firmware update precedes a restoration-in-progress stage and a restoration-completed stage. The same guide warns that:

- removing/disconnecting the SSD while restoration is in progress can corrupt data;
- abnormal termination while restoration is active can corrupt data;
- firmware update itself carries data-loss risk and Samsung recommends backup;
- unplugging the SSD during firmware update may permanently damage the SSD.

It also imposes maintenance-path constraints. In the inspected Windows guide text, the tool is specific to the 840 EVO family, does not work through SCSI-controller or USB-to-SATA paths, supports specified partition/filesystem arrangements, does not work on a user-password-locked SSD, does not support RAID mode for this path, and has additional driver/platform restrictions.

Mirrored Samsung-authored guide body:

- <https://abcdocz.com/doc/355108/sa-amsu-ung>
- corroborating mirror: <https://www.scribd.com/doc/273995952/Samsung-Performance-Restoration-v-1-0-Installation-Guide>

A mirrored DOS guide independently preserves the same high-level split between firmware update and SSD restoration, the interruption warnings, and the SCSI/USB-to-SATA/password/RAID limitations:

- <https://manualzz.com/doc/1884796/samsung-ssd-user-manual>

Evidence label: **H/P\*** — manufacturer-authored historical document content through secondary mirrors, with artifact identity/date/version independently anchored by Samsung's current first-party support ledger. The asterisk prevents the mirror from being silently upgraded to direct inspection of a current Samsung-hosted body.

### C. Contemporary independent publication preserving Samsung's staged remediation context

The SSD Review's 15 October 2014 article preserves Samsung's period explanation that the old-data slowdown was associated with flash-management/read-retry behavior and that the restoration utility rewrote old data. Its walkthrough also presents the restoration as a sequence rather than one indivisible event: start restoration, update firmware, restoration in progress, restoration complete.

Source: <https://www.thessdreview.com/daily-news/latest-buzz/samsung-announces-firmware-update-resolve-840-evo-performance-degradation/>.

This source remains **H/S with direct-vendor-statement provenance**. It corroborates the transaction structure but does not supersede the provenance distinction above.

## Engineering reconstruction

### Firmware installation is not the same state as restoration completion

The historical guide itself separates `Firmware Update` and `SSD Performance Restoration`, and the staged workflow exposes an intermediate `Restoration is in Progress` state before completion.

Therefore:

> **firmware update ≠ performance-restoration completion**.

And:

> **maintenance started ≠ maintenance safely completed**.

This is not a claim about the exact internal firmware transaction protocol. It is a host-visible maintenance-state distinction supported by the documented workflow.

### A maintenance operation can create its own failure window

The original old-data incident is a retention/performance problem: aging physical embodiments become more expensive to read under the flawed management policy. The restoration guide documents a different failure class introduced by the act of remediation itself: interruption during firmware update or restoration can cause corruption or device damage.

Therefore:

> **maintenance-path interruption hazard ≠ original old-data aging hazard**.

And:

> **a procedure intended to improve later retention/serviceability can itself require temporary continuity conditions while it runs**.

This does not establish the probability of corruption, a particular atomicity protocol, or that normal power-off storage outside the maintenance transaction is unsafe.

### Unplugging during firmware update is not the same event as ordinary powered-off retention

Case 37 already establishes from the April 2015 Samsung Q&A that the later periodic refresh algorithm does not run with power off. The October 2014 guide adds a separate rule: unplugging **during the update/restoration transaction** is hazardous.

Those must remain separate:

> **ordinary power-off retention interval ≠ interruption of an active maintenance/update transaction**.

The first concerns what the nonvolatile payload and maintenance policy do while the device is quiescent. The second concerns loss of continuity during an operation that is actively changing firmware and/or data embodiments.

### Maintenance-path eligibility is not the same as payload readability

The official restoration route depends on more than the NAND payload existing. Samsung's guide places constraints on attachment path, partition/filesystem state, password/security state, RAID mode, and some host/controller/driver conditions.

Thus:

> **payload remains host-readable ≠ official restoration path is currently admissible**.

And:

> **maintenance-interface compatibility ≠ NAND-cell condition**.

A drive can possess readable old data while the particular Samsung utility cannot reach or service it through a given enclosure/controller/software arrangement. The guide does not imply that these interface restrictions are physical NAND-retention laws.

### Admission to the tool is not proof of maintenance outcome

Conversely, satisfying the documented platform and attachment prerequisites only establishes that the supported maintenance path may be attempted. It does not prove that a particular run reaches the documented completed state without error.

> **maintenance admissibility ≠ maintenance completion ≠ verified post-maintenance outcome**.

The October 2014 guide is a procedure/contract document, not an independent fault-injection study or fleet-level success-rate measurement.

### Backup advice is a risk boundary, not a measured failure rate

Samsung's guide tells users to back up important data before firmware update and warns of possible data loss/corruption under interruption.

This supports:

> **vendor-declared operation risk ≠ evidence that data loss normally occurs**.

No failure probability, corruption frequency, or complete crash matrix is inferred from the warning language.

### v1.0/v1.1 packaging does not create a recurring maintenance cadence

Samsung's current first-party support note says users who already restored performance with v1.0 do not need to use v1.1. In this bounded context, v1.1 is therefore a later package/revision of the one-time restoration route, not evidence of a recurring refresh schedule.

> **restoration package revision ≠ periodic maintenance cadence**.

The continuing periodic-refresh policy remains a separate April 2015 historical layer already grounded in the main Case 37 evidence record.

### Artifact metadata can outlive practical execution support

Samsung's current support pages still preserve filenames, versions, dates, sizes, and download records for the 2014 maintenance artifacts while at least one current US page also marks the old v1.1 tool as not working.

A narrow archival/access observation follows:

> **surviving maintenance-artifact metadata ≠ currently executable maintenance path**.

This is a present-day repository/source-preservation observation, not a historical claim about 2014 functionality. It is useful to the project's longer-term access layer because a technical procedure can remain documentable after the supported execution environment has decayed or disappeared.

## Historical record / reconstruction / analogy / interpretation boundary

### Historical record

- Samsung's current support ledgers preserve exact October 2014 restoration artifacts and version/date metadata.
- Samsung-authored October 2014 guides, inspected through mirrors whose artifact identity is independently anchored by Samsung, separate firmware update from restoration and document interruption hazards and platform/interface limitations.
- Contemporary reporting preserves the old-data remediation context and staged workflow.

### Engineering reconstruction

From those records the repository can safely distinguish:

```text
old-data performance problem
    !=
maintenance-path eligibility
    !=
firmware-update stage
    !=
restoration-in-progress stage
    !=
restoration-completed state
    !=
verified post-maintenance service outcome
    !=
later recurring refresh policy
```

### Functional analogies

- **Case 15 — Intel SSD 320 PLP:** both make interruption/power continuity relevant to data state, but Case 15 concerns device-internal emergency durability under unexpected power loss; Case 37 concerns a host-invoked firmware/restoration procedure. No implementation or genealogy is shared by inference.
- **Case 36 — Flash Correct-and-Refresh:** both involve Flash maintenance/renewal, but FCR is a research policy for ECC-bounded retention while this slice concerns the safety and admissibility of one commercial restoration transaction.
- **Case 135 — Micron eMMC self-refresh:** both show that maintenance availability can depend on operational preconditions; Micron's reset/time/idle policy and Samsung's host-tool/platform path are different mechanisms and historical objects.

### Philosophical interpretation — bounded

The technical pressure point is modest: retention work itself can have a **continuation requirement**. A system may need a stable power/interface/execution relation long enough to transform one retained embodiment into another safely.

This does not justify saying that maintenance is universally `memory remembering itself`, nor does it turn every software compatibility problem into a physical retention mechanism. The mechanism-first claim is only that an operation intended to preserve future service can possess its own admission conditions and interruption hazards.

## Claim ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| Samsung's current support infrastructure preserves named 840 EVO Performance Restoration v1.0/v1.1 artifacts dated October 2014 | `H/P` | strong current manufacturer artifact/provenance ledger |
| The Samsung-authored October 2014 guide separates firmware update from SSD performance restoration | `H/P*` | guide body inspected through secondary mirrors; artifact identity/date/version first-party anchored |
| The guide warns that disconnect/abnormal termination during restoration can corrupt data | `H/P*` | strong document-content evidence with mirror-provenance qualification |
| The guide warns that unplugging during firmware update may permanently damage the SSD and recommends backup | `H/P*` | risk warning; not a measured failure-rate claim |
| The supported restoration path has attachment/security/filesystem/controller restrictions | `H/P*` | bounded to documented tool path, not NAND physics |
| Firmware update completion is identical to restoration completion | `X` | contradicted by documented staged workflow |
| Tool eligibility proves successful restoration | `X` | unsupported |
| Restoration interruption hazard is the same failure mode as the original old-data slowdown | `X` | different documented event class |
| A firmware-update warning proves ordinary powered-off data retention is unsafe | `X` | unsupported |
| Current `Tool does not work` annotation proves the tool failed in 2014 | `X` | anachronistic projection rejected |
| Surviving support metadata proves the old tool remains executable today | `X` | current support metadata and execution availability are distinct |

## Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Samsung 840 EVO` returned no dedicated case to reuse. Broader Samsung controller history, firmware architecture, TLC process history, and archival recovery of historical execution environments belong there if developed. This file remains bounded to the retention-specific maintenance-transaction relation.

## Open work after this slice

Still open:

- recover and directly inspect a Samsung-hosted or independently archived byte-identical October 2014 guide body if one becomes accessible;
- recover Samsung-hosted April 2015 FAQ / Magician 4.6 guide artifacts;
- exact firmware-update/restoration crash-consistency protocol and rollback behavior;
- exact internal read-reference and rewrite/relocation algorithm;
- independent named-drive power-cut/fault-injection testing during the restoration transaction;
- endurance/write-amplification cost of restoration and later periodic refresh;
- broader 840 EVO firmware/controller genealogy.

## Sources

1. Samsung US Business, **840 EVO Series SSD (1TB) support/download page**, current support ledger with October 2014 v1.0/v1.1 entries: <https://www.samsung.com/us/business/support/owners/product/840-evo-series-1tb/>.
2. Samsung Australia, **Samsung SSD 840 EVO 500GB (`MZ-7TE500`) support page**, current first-party ledger retaining exact Performance Restoration filenames, versions, dates, and file IDs: <https://www.samsung.com/au/support/model/MZ-7TE500BW/>.
3. Samsung Electronics, **Samsung Performance Restoration Version 1.0**, `2014.10 (Rev 1.0)`, manufacturer-authored Windows guide body inspected through mirror: <https://abcdocz.com/doc/355108/sa-amsu-ung>; corroborating mirror: <https://www.scribd.com/doc/273995952/Samsung-Performance-Restoration-v-1-0-Installation-Guide>.
4. Samsung Electronics, **Samsung Performance Restoration DOS v1.0 Introduction and Installation Guide**, `2014.10 (Rev 1.0)`, manufacturer-authored guide body inspected through mirror: <https://manualzz.com/doc/1884796/samsung-ssd-user-manual>.
5. Scot Strong, **“Samsung Announces Firmware Update To Resolve 840 EVO Performance Degradation,”** *The SSD Review*, 15 October 2014: <https://www.thessdreview.com/daily-news/latest-buzz/samsung-announces-firmware-update-resolve-840-evo-performance-degradation/>.
6. Existing Case 37 grounding record for the broader 2014–2015 chronology: [`37-samsung-840-evo-2014-2015-performance-refresh-grounding.md`](37-samsung-840-evo-2014-2015-performance-refresh-grounding.md).
'''


def once_replace(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one anchor, found {count}')
    return text.replace(old, new, 1)


if EVIDENCE_PATH.exists():
    raise SystemExit('evidence file already exists; refusing duplicate slice')
EVIDENCE_PATH.write_text(EVIDENCE, encoding='utf-8')

case_path = Path('cases/37-samsung-840-evo-old-data-performance-refresh.md')
case = case_path.read_text(encoding='utf-8')
grounding = "Grounding record: [`../evidence/37-samsung-840-evo-2014-2015-performance-refresh-grounding.md`](../evidence/37-samsung-840-evo-2014-2015-performance-refresh-grounding.md).\n"
case = once_replace(
    case,
    grounding,
    grounding + "\nRestoration-transaction deepening: [`../evidence/37-samsung-2014-restoration-transaction-deepening.md`](../evidence/37-samsung-2014-restoration-transaction-deepening.md).\n",
    'Case 37 grounding link',
)
insert_anchor = "### One-time restoration is not the same as a continuing maintenance policy\n"
insert = r'''### Restoration is a staged maintenance transaction, not an atomic “fix”

The October 2014 Samsung-authored Performance Restoration guide, whose exact artifact identity is preserved in Samsung's current support ledgers and whose body survives through document mirrors, separates `Firmware Update` from `SSD Performance Restoration`. Its documented workflow passes through firmware update and `Restoration is in Progress` before a completed state. The same guide warns that disconnecting or abnormally terminating restoration can corrupt data, and that unplugging during firmware update may damage the device.

Therefore:

> **firmware update ≠ restoration completion**,

> **maintenance started ≠ maintenance safely completed**,

and

> **maintenance-path interruption hazard ≠ the original old-data aging hazard**.

The warnings establish an operation boundary, not a measured failure probability or the exact internal crash-consistency protocol.

The guide also limits the supported maintenance path by attachment/interface, partition/filesystem, password/security, RAID, and some controller/driver conditions. Those constraints make maintenance availability relational at a different layer from NAND readability:

> **payload remains readable ≠ official restoration path is admissible**,

> **maintenance-interface compatibility ≠ NAND-cell condition**,

and

> **maintenance admissibility ≠ maintenance completion ≠ verified outcome**.

A current Samsung support page still preserves the 2014 artifact ledger while marking the old v1.1 tool as not working. That present-day state is used only to distinguish **artifact/procedure metadata survival from current executability**; it is not projected backward as evidence that the utility failed historically.

'''
case = once_replace(case, insert_anchor, insert + insert_anchor, 'Case 37 engineering section')
case_path.write_text(case, encoding='utf-8')

roadmap_path = Path('ROADMAP.md')
roadmap = roadmap_path.read_text(encoding='utf-8')
if '37-samsung-2014-restoration-transaction-deepening.md' in roadmap:
    raise SystemExit('ROADMAP already contains Case 37 deepening')
roadmap_anchor = "## Phase 2 — Build missing technical bridges\n\n"
roadmap_entry = "- [x] Case 37 Samsung 840 EVO restoration-transaction / maintenance-admission deepening — [`cases/37-samsung-840-evo-old-data-performance-refresh.md`](cases/37-samsung-840-evo-old-data-performance-refresh.md), deepened by [`evidence/37-samsung-2014-restoration-transaction-deepening.md`](evidence/37-samsung-2014-restoration-transaction-deepening.md): current Samsung support ledgers preserve exact October-2014 v1.0/v1.1 restoration artifacts, while the manufacturer-authored guide body surviving through qualified secondary mirrors separates firmware update from restoration completion, warns about corruption/device risk under interruption, and exposes attachment/security/filesystem/controller admission limits. This closes the bounded `firmware update != restoration complete`, `maintenance admission != payload readability`, and `maintenance interruption hazard != original aging hazard` seams without claiming crash-atomic internals, failure rates, or that a current `Tool does not work` label describes 2014 behavior. Direct Samsung-hosted/byte-identical guide recovery, the April-2015 FAQ/Magician-4.6 body, exact controller algorithms, and power-cut fault injection remain open; broader firmware/controller genealogy belongs primarily in `computing-archaeology`.\n\n"
roadmap = once_replace(roadmap, roadmap_anchor, roadmap_anchor + roadmap_entry, 'ROADMAP Phase 2')
roadmap_path.write_text(roadmap, encoding='utf-8')

index_path = Path('CASE_INDEX.md')
index = index_path.read_text(encoding='utf-8')
old_tail = "[2014–2018 Samsung 840 EVO grounding](evidence/37-samsung-840-evo-2014-2015-performance-refresh-grounding.md); Samsung-hosted 2014/2015 FAQ/Magician-4.6 archival recovery, exact internal read-reference algorithm, other TLC/3D-NAND products, and endurance/compliance measurements remain separate work"
new_tail = "[2014–2018 Samsung 840 EVO grounding](evidence/37-samsung-840-evo-2014-2015-performance-refresh-grounding.md) + [2014 restoration-transaction deepening](evidence/37-samsung-2014-restoration-transaction-deepening.md); direct Samsung-hosted/byte-identical 2014 guide recovery, Samsung-hosted 2015 FAQ/Magician-4.6 archival recovery, exact internal read-reference algorithm, other TLC/3D-NAND products, and endurance/compliance measurements remain separate work"
index = once_replace(index, old_tail, new_tail, 'CASE_INDEX Case 37 row')
if '## Case 37 deepening — 2014 restoration-transaction findings' in index:
    raise SystemExit('CASE_INDEX findings already present')
findings = r'''

## Case 37 deepening — 2014 restoration-transaction findings

Evidence: [`evidence/37-samsung-2014-restoration-transaction-deepening.md`](evidence/37-samsung-2014-restoration-transaction-deepening.md)

- **2864 — first-party artifact identity != directly inspected historical guide body:** current Samsung support ledgers preserve October-2014 filenames, versions, dates, and file IDs, while the guide body used here is inspected through qualified third-party mirrors rather than silently promoted to a current Samsung-hosted facsimile. (`H/P`, `H/P*`, `X`)
- **2865 — maintenance-path eligibility != payload readability:** Samsung's tool depends on supported attachment/interface, partition/filesystem, password/security, RAID, and controller/driver conditions; readable payload does not by itself make the official restoration route admissible. (`H/P*`, `E`)
- **2866 — firmware update != performance-restoration completion:** the Samsung guide exposes firmware update and SSD restoration as separate features/stages, with an explicit restoration-in-progress state before completion. (`H/P*`, `E`)
- **2867 — maintenance started != maintenance safely completed:** entering the restoration workflow leaves a documented intermediate state whose abnormal termination can corrupt data. (`H/P*`, `E`)
- **2868 — maintenance interruption hazard != original aging failure:** the original episode concerns old-data read-performance degradation, while the guide's corruption warning concerns interruption of the remediation transaction itself. (`H/P*`, `E`, `X`)
- **2869 — unplugging during firmware update != ordinary power-off retention:** a hazardous loss of continuity during active update/restoration must not be confused with passive unpowered retention or the later fact that periodic refresh cannot run while power is off. (`H/P*`, `E`, `X`)
- **2870 — backup recommendation != measured loss rate:** Samsung's firmware-update warning establishes declared risk and a precaution, not a probability that ordinary restoration attempts lose data. (`H/P*`, `X`)
- **2871 — maintenance admissibility != maintenance outcome:** satisfying tool prerequisites authorizes/permits an attempt; it does not prove that a particular run reached the completed state or that post-run performance was independently verified. (`E`, `X`)
- **2872 — v1.0 completion != obligation to rerun v1.1:** Samsung's current support note says users who already restored with v1.0 do not need v1.1, making package revision and one-time restoration history distinct. (`H/P`, `E`)
- **2873 — one-time restoration package != 2015 periodic-refresh cadence:** the October-2014 utility revision sequence is not evidence of recurring maintenance; Samsung's later periodic-refresh statement remains a separate April-2015 historical layer. (`H/P`, `H/S`, `E`, `X`)
- **2874 — product/interface gate != NAND physics:** SCSI, USB-to-SATA, RAID, filesystem, password, or driver restrictions describe the supported host maintenance path and cannot be generalized into cell-retention laws. (`H/P*`, `E`, `X`)
- **2875 — current `Tool does not work` label != 2014 historical behavior:** a present-day Samsung support annotation describes the current support/access state and cannot be projected backward as evidence that the October-2014 utility was nonfunctional. (`H/P`, `X`)
- **2876 — surviving artifact metadata != executable maintenance availability:** filenames, dates, versions, and support records can remain recoverable even when the old tool is no longer a practically supported execution path. (`H/P`, `E`)
- **2877 — restoration/update risk != sanitization:** corruption/device-damage warnings during firmware/restoration say nothing about secure erase, forensic disappearance, or an NVMe/ATA sanitization guarantee. (`E`, `X`)
- **2878 — related-repository boundary:** a fresh `tmzncty/computing-archaeology` search for `Samsung 840 EVO` returned no dedicated overlapping case; broader Samsung firmware/controller/TLC genealogy belongs there if developed, while this slice remains bounded to maintenance transaction/admission semantics. (`H/P` project-state record)
'''
index = index.rstrip() + findings + '\n'
index_path.write_text(index, encoding='utf-8')

assert EVIDENCE_PATH.exists()
assert case.count('37-samsung-2014-restoration-transaction-deepening.md') >= 1
assert roadmap.count('37-samsung-2014-restoration-transaction-deepening.md') >= 1
assert index.count('37-samsung-2014-restoration-transaction-deepening.md') >= 2
assert '**2864 —' in index and '**2878 —' in index
