from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {count}")
    return text.replace(old, new, 1)


case_path = "cases/55-nvme-smart-health-endurance-telemetry.md"
case = read(case_path)
case = replace_once(
    case,
    "**`grounded`** — bounded to the NVMe 1.0e/1.3 SMART / Health Information interface and a 2014 Intel DC P3700 product witness.",
    "**`grounded`** — bounded to the NVMe 1.0/1.0e/1.3 SMART / Health Information interface and a 2014 Intel DC P3700 product witness. The latest deepening uses the original 2011 Gold specification to separate spare-threshold warning, reserve exhaustion, and actual command failure without inferring a hidden SSD remapping algorithm.",
    "case status",
)

historical_anchor = "### NVMe 1.0e already defines retained health history\n"
historical_add = """### NVMe 1.0 already separates spare threshold, spare exhaustion, and command failure

The original **NVM Express Revision 1.0 Gold**, ratified **1 March 2011**, already contains the spare-capacity and failure boundary needed for this case; 1.0e is therefore not treated as the first appearance of the mechanism.

In §5.10.1.2 and Figure 59, Revision 1.0 says SMART / Health information is provided over the life of the controller and retained across power cycles. `Available Spare` is a normalized 0–100% measure of remaining spare capacity, while `Available Spare Threshold` may generate an asynchronous event once that reserve falls below the configured threshold. The asynchronous-event table separately names `Spare Below Threshold`.

A different table, the generic command-status definitions, gives `Write Fault` a stronger service consequence: the write data could not be committed to the media, and the specification says this **may** be due to lack of available spare locations. The immediately following `Unrecovered Read Error` is defined separately as read data that could not be recovered from the media.

The historical interface therefore does **not** expose one binary `healthy/dead` transition. It exposes at least three different relations:

```text
remaining spare capacity
        -> threshold crossing / warning
        -> possible exhaustion-related write failure
```

The arrows are an engineering ordering of interface relations, not a claim that every device must traverse a deterministic state machine. In particular, the specification says spare exhaustion **may** cause a Write Fault; it does not say every Write Fault proves spare exhaustion, nor that crossing the warning threshold means the reserve is already exhausted.

This direct 2011 evidence sharpens the ROADMAP failure slice while keeping the implementation boundary intact: NVMe exposes reserve and failure semantics to the host, but does not thereby specify a particular controller's bad-block table, FTL, replacement-pool allocator, NAND defect-growth process, or automatic reassignment algorithm.

"""
case = replace_once(case, historical_anchor, historical_add + historical_anchor, "case historical insertion")

engineering_anchor = "### Spare capacity is maintenance reserve, not ordinary free user space\n"
engineering_add = """### Spare threshold, reserve exhaustion, and service failure are different states

The 2011 command-status wording makes the spare-reserve distinction operational rather than merely descriptive. A controller can report remaining spare capacity; the remaining capacity can fall below a warning threshold; and lack of spare locations can become severe enough that a write cannot be committed. These are different claims.

Therefore:

> **spare below threshold ≠ spare exhausted**.

and:

> **spare exhaustion as a possible Write Fault cause ≠ proof that every Write Fault is a spare-exhaustion event**.

and:

> **Write Fault ≠ Unrecovered Read Error**.

The retention consequence is that **present payload correctness and future repair/continuation margin can diverge**. A device may still serve current data while its hidden reserve for replacing or bypassing future failed locations is shrinking. Conversely, a low-spare warning is not itself evidence that current user payload has already been lost.

This is where Cases 14 and 78 become useful functional comparisons. SCSI grown-defect reassignment and Micron NAND bad-block management directly ground finite replacement pools at lower layers; NVMe 1.0 shows a later host-visible interface that reports remaining spare capacity and can surface a write failure when spare locations are unavailable. The comparison is **not** genealogy, and the NVMe source cannot be used to infer that an SSD implements either earlier mechanism internally.

"""
case = replace_once(case, engineering_anchor, engineering_add + engineering_anchor, "case engineering insertion")

ledger_anchor = "| NVMe 1.0e SMART/Health information is described as lifetime information retained across power cycles | `H/P` | strong, official specification |"
ledger_add = """| NVMe 1.0 Gold already exposes Available Spare, a spare threshold, and a Spare Below Threshold asynchronous-event condition | `H/P` | strong, official 2011 specification |
| NVMe 1.0 `Write Fault` says data could not be committed and lack of spare locations is one possible cause | `H/P` | strong, official 2011 specification |
| `Spare Below Threshold` is not equivalent to reserve exhaustion, and `Write Fault` is not equivalent to `Unrecovered Read Error` | `H/P/E` | strong bounded reconstruction from distinct normative fields/status codes |
"""
case = replace_once(case, ledger_anchor, ledger_add + ledger_anchor, "case claim ledger")

source_anchor = """1. NVM Express, **NVM Express 1.0e**, official specification PDF, especially §5.10.1.2 and Figure 60, printed pp. 67–69: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0e.pdf>
2. NVM Express, **NVM Express Revision 1.3**, official specification PDF, especially §5.14.1.2 and Figure 93, printed pp. 98–100: <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>
3. NVM Express, **Specification Archives**, historical revision index: <https://nvmexpress.org/nvm-express-specification-archives/>
4. Intel, **Intel Solid-State Drive DC P3700 Series Product Specification**, Order Number 330566-002US, July 2014; surviving transcript/mirror used for product-specific tables: <https://manualzilla.com/doc/7195133/intel-dcp3700-1.6tb>
5. NVM Express, **Features for Error Reporting, SMART, Log Pages, Failures and management capabilities in NVMe Architectures**, later institutional explanation used only as operational corroboration, not historical priority evidence: <https://nvmexpress.org/resource/features-for-error-reporting-smart-log-pages-failures-and-management-capabilities-in-nvme-architectures/>"""
source_repl = """1. NVM Express, **NVM Express Revision 1.0 Gold**, ratified 1 March 2011, especially the generic command-status definitions, asynchronous-event status table, §5.10.1.2, and Figure 59: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0-Gold.pdf>
2. NVM Express, **NVM Express 1.0e**, official specification PDF, especially §5.10.1.2 and Figure 60, printed pp. 67–69: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0e.pdf>
3. NVM Express, **NVM Express Revision 1.3**, official specification PDF, especially §5.14.1.2 and Figure 93, printed pp. 98–100: <https://nvmexpress.org/wp-content/uploads/NVM_Express_Revision_1.3.pdf>
4. NVM Express, **Specification Archives**, historical revision index: <https://nvmexpress.org/nvm-express-specification-archives/>
5. Intel, **Intel Solid-State Drive DC P3700 Series Product Specification**, Order Number 330566-002US, July 2014; surviving transcript/mirror used for product-specific tables: <https://manualzilla.com/doc/7195133/intel-dcp3700-1.6tb>
6. NVM Express, **Features for Error Reporting, SMART, Log Pages, Failures and management capabilities in NVMe Architectures**, later institutional explanation used only as operational corroboration, not historical priority evidence: <https://nvmexpress.org/resource/features-for-error-reporting-smart-log-pages-failures-and-management-capabilities-in-nvme-architectures/>"""
case = replace_once(case, source_anchor, source_repl, "case sources")
write(case_path, case)


ev_path = "evidence/55-nvme10-13-smart-health-endurance-grounding.md"
ev = read(ev_path)
ev = replace_once(
    ev,
    "The answer is yes for the bounded NVMe 1.0e–1.3 record.",
    "The answer is yes for the bounded NVMe 1.0–1.3 record. The original 2011 Gold revision additionally grounds the boundary between spare-threshold warning, lack of spare locations, and command failure.",
    "evidence scope",
)

ev_anchor = "## Source A — official NVM Express 1.0e\n"
ev_add = """## Source 0 — official NVM Express Revision 1.0 Gold

**Document:** `NVM Express Revision 1.0`, ratified **1 March 2011**.

Official PDF: <https://nvmexpress.org/wp-content/uploads/NVM-Express-1_0-Gold.pdf>

The official PDF was directly inspected in this slice, including facsimile inspection of the structured SMART/Health table.

### 0.1. The original 1.0 log already retains lifetime health information

**§5.10.1.2, printed p. 64; Figure 59, printed p. 65.**

Revision 1.0 says SMART/general health information is provided over the life of the controller and retained across power cycles. Figure 59 already defines `Available Spare`, `Available Spare Threshold`, `Percentage Used`, and the separate critical-warning bits for spare threshold, reliability degradation, and read-only media.

`Percentage Used` already carries the explicit boundary that 100 means estimated endurance consumed but **may not indicate device failure** and may exceed 100.

This prevents a false chronology in which those relations first appear in 1.0e or 1.3.

### 0.2. Spare-threshold notification is not spare exhaustion

**Asynchronous Event Request status table, printed p. 55.**

Revision 1.0 defines a `Spare Below Threshold` condition: available spare space has fallen below the threshold. The condition describes a threshold crossing, not zero remaining reserve.

Therefore the primary source itself supports keeping:

`spare below threshold ≠ spare exhausted`.

### 0.3. Lack of spare locations is a possible cause of Write Fault

**Generic Command Status, printed p. 49.**

Status `80h Write Fault` says the write data could not be committed to the media and that this **may** be due to lack of available spare locations reported as an asynchronous event. Status `81h Unrecovered Read Error` is separately defined as read data that could not be recovered from the media.

This grounds a bounded failure bridge:

```text
remaining reserve / threshold evidence
        ≠
actual inability to commit a write
        ≠
unrecovered read failure
```

The word `may` is important. It allows `lack of spare locations -> possible Write Fault cause`; it does **not** allow the converse claim `every Write Fault -> proven spare exhaustion`.

### 0.4. Interface evidence does not expose the internal replacement mechanism

Revision 1.0 reports reserve and failure semantics but does not, in these clauses, define a particular NAND bad-block table, FTL allocation algorithm, physical replacement-pool geometry, or automatic reassignment sequence. Those mechanisms must be grounded from lower-layer/product evidence such as Case 78 rather than inferred from host telemetry.

"""
ev = replace_once(ev, ev_anchor, ev_add + ev_anchor, "evidence source0 insertion")

ev_ledger_anchor = "| SMART/Health includes information retained across power cycles | `H/P` | NVMe 1.0e §5.10.1.2; NVMe 1.3 §5.14.1.2 | strong official primary |"
ev_ledger_add = """| Original NVMe 1.0 already exposes Available Spare and Spare Below Threshold | `H/P` | NVMe 1.0 Fig. 59 + asynchronous-event status | strong official 2011 primary |
| Lack of spare locations is one possible cause of `Write Fault` | `H/P` | NVMe 1.0 Generic Command Status 80h | strong official 2011 primary |
| `Write Fault` and `Unrecovered Read Error` are separate statuses | `H/P/E` | NVMe 1.0 status 80h vs 81h | strong official primary; relation-level reconstruction |
| A spare-threshold event proves reserve exhaustion or current payload loss | `X` | threshold wording does not say this | rejected |
| Every `Write Fault` proves spare exhaustion | `X` | contradicted by normative `may be due` wording | rejected |
"""
ev = replace_once(ev, ev_ledger_anchor, ev_ledger_add + ev_ledger_anchor, "evidence ledger")

cross_anchor = "- **Case 36:** physical NAND error/refresh mechanism ≠ host-visible health estimate.\n"
cross_add = """- **Case 14:** SCSI grown-defect reassignment directly grounds finite spare-location consumption and a `NO DEFECT SPARE LOCATION AVAILABLE` failure; NVMe 1.0 is compared only as a later host-interface reserve/failure relation, not as genealogy.
- **Case 78:** Micron NAND bad-block management directly grounds reserved replacement blocks and BBT-controlled exclusion. NVMe `Available Spare` does not prove that a conforming SSD uses that exact internal mechanism.
- **Case 76:** JEDEC workload-qualified endurance and NVMe `Percentage Used` concern life/endurance qualification; they must not be collapsed into the separate `Available Spare` reserve relation.
"""
ev = replace_once(ev, cross_anchor, cross_add + cross_anchor, "evidence cross-case")
write(ev_path, ev)


road_path = "ROADMAP.md"
road = read(road_path)
road = replace_once(
    road,
    "- [ ] defect growth, failed reassignment, or spare exhaustion;",
    "- [ ] defect growth, failed reassignment, or spare exhaustion — **partially advanced by grounded Cases 14, 55, and 78**: Case 14 grounds finite SCSI replacement locations and explicit no-spare failure; Case 78 grounds NAND factory/lifetime bad-block exclusion plus reserved replacement blocks; the latest Case-55 deepening adds the 2011 NVMe host-interface bridge from remaining `Available Spare` and `Spare Below Threshold` warning to a `Write Fault` that may result from lack of spare locations. This does not yet ground named-controller automatic reassignment, empirical spare-exhaustion behavior, post-threshold fault progression, or a full HDD/NAND/SSD defect-management genealogy;",
    "ROADMAP failure item",
)
write(road_path, road)


idx_path = "CASE_INDEX.md"
idx = read(idx_path).rstrip("\n")
idx_anchor = "1467. **integrity-qualified coded-recovery synthesis ≠ one universal pipeline or historical genealogy** — RAID-6, Swift, Ceph, and OpenZFS are compared only at the relation level; differences in fault model, versioning, checksum authority, code geometry, and repair policy remain historically and technically distinct."
idx_add = """
1468. **remaining spare capacity ≠ present payload correctness** — NVMe 1.0 can expose declining `Available Spare` while the interface still distinguishes this reserve state from actual read/write failure; continuation margin can shrink before current payload service fails.
1469. **spare below threshold ≠ spare exhausted** — `Spare Below Threshold` is a threshold condition, not a statement that no replacement locations remain.
1470. **spare-threshold warning ≠ reliability-degraded warning** — NVMe 1.0 assigns separate Critical Warning bits to low spare space and device-reliability degradation; one cannot be substituted for the other.
1471. **spare-threshold warning ≠ read-only state** — low spare reserve and media read-only mode are separate host-visible warning relations.
1472. **Percentage Used ≠ Available Spare** — the former is a vendor-specific estimate of consumed device life, while the latter reports normalized remaining spare capacity; endurance model and replacement reserve are distinct state variables.
1473. **100% Percentage Used ≠ device failure** — the original NVMe 1.0 field definition already says estimated endurance may be consumed without implying device failure and permits values above 100.
1474. **spare exhaustion as a possible Write Fault cause ≠ proof that every Write Fault is spare exhaustion** — the 2011 standard says write failure `may` be due to lack of available spare locations, so the causal implication cannot be reversed.
1475. **Write Fault ≠ Unrecovered Read Error** — inability to commit write data and inability to recover read data are separate generic command statuses even when both can arise in a degrading storage device.
1476. **host-visible spare telemetry ≠ internal defect-remap mechanism** — NVMe exposes reserve/warning/failure semantics but does not thereby prove a particular bad-block table, FTL allocator, replacement-pool geometry, or reassignment algorithm.
1477. **finite spare reserve = possible continuation resource, not ordinary user capacity** — as an engineering reconstruction across Cases 14, 55, and 78, reserved physical locations can support future re-embodiment while remaining distinct from user-addressable payload capacity; the comparison is functional, not genealogical."""
if idx.count(idx_anchor) != 1:
    raise SystemExit(f"CASE_INDEX anchor count {idx.count(idx_anchor)}")
idx = idx.replace(idx_anchor, idx_anchor + idx_add, 1) + "\n"
write(idx_path, idx)
