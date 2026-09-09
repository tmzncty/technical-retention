from pathlib import Path

CASE = Path("cases/15-intel-ssd320-power-loss-durability.md")
GROUNDING = Path("evidence/15-intel-ssd320-power-loss-durability-grounding.md")
EVIDENCE = Path("evidence/15-intel320-2011-unsafe-shutdown-telemetry-deepening.md")
ROADMAP = Path("ROADMAP.md")
INDEX = Path("CASE_INDEX.md")

EVIDENCE_TEXT = r"""# Case 15 Deepening — Intel SSD 320 Unsafe-Shutdown Telemetry Is Event History, Not a Durability Verdict

## Scope

This deepening asks one bounded question inside the already-grounded Intel SSD 320 power-loss case:

> **What does the drive retain when it counts an `unsafe shutdown`, and what does that retained evidence not prove about payload durability or the success of power-loss protection?**

The source boundary is deliberately narrow. It uses two Intel manufacturer-primary documents for the same named 2011 product family:

1. Intel, *Intel Solid-State Drive 320 Series Product Specification*, order **325152-002US**, September 2011, especially §5.4.1, printed pp. 18–19, Tables 12–13.
2. Intel, *Enhanced power-loss data protection in the Intel Solid-State Drive 320 Series*, order **325207-001US**, March 2011, especially printed p. 1.

The first document exposes a retained SMART event count. The second describes the product's intended emergency protection path during the same class of unsafe power event. Read together, they make it possible to separate **event-history retention** from **durability outcome** without assuming a hidden controller mechanism.

This is not a general SMART history, not independent post-fix power-cut validation, and not a claim about the exact internal cause of the SSD 320 `BAD_CTX 13x` / 8 MB defect already discussed in Case 15.

---

## Source custody and exact anchors

### Source A — Intel SSD 320 Product Specification, September 2011

**Document:** Intel Corporation, *Intel Solid-State Drive 320 Series Product Specification*, order 325152-002US, September 2011.

**Custody:** directly inspected from Intel's regional content host:

<https://www.intel.com.br/content/dam/www/public/us/en/documents/product-specifications/ssd-320-specification.pdf>

**Relevant anchors:**

- printed p. 18, §5.4.1 / Table 12: SMART attribute `C0h`, `Power-Off Retract Count (Unsafe Shutdown Count)`;
- printed p. 18: the raw value is the cumulative number of unsafe/unclean shutdown events over the life of the device;
- printed p. 18: Intel defines the counted event by power-off without `STANDBY IMMEDIATE` being the last command;
- printed p. 18: C0h flags are `SP=1`, `EC=1`, `ER=0`, `PE=0`, `OC=1`, `PW=0`, with threshold `0 (none)`;
- printed p. 19 / Table 13: Intel defines `SP` as `Self-preserving attribute`, `EC` as `Event count attribute`, `OC=1` as collected during offline and online activity, and `PW=0` as `Advisory` rather than `Pre-fail`.

### Source B — Intel SSD 320 Power-Loss Data Protection brief, March 2011

**Document:** Intel Corporation, *Enhanced power-loss data protection in the Intel Solid-State Drive 320 Series*, order 325207-001US, March 2011.

**Custody:** directly inspected from Intel's content host:

<https://www.intel.com/content/dam/www/public/us/en/documents/technology-briefs/ssd-320-series-power-loss-data-protection-brief.pdf>

**Relevant anchors, printed p. 1:**

- a clean shutdown uses `STANDBY IMMEDIATE` so data in temporary buffers can be saved to NAND;
- an unsafe shutdown is described as power disappearing before that command can be issued;
- the SSD 320 is claimed to protect user and system data during unexpected power loss;
- a power-fail detector, firmware, isolation, and onboard capacitance provide a path to transfer temporary-buffer state to NAND.

Source B is a manufacturer design/product claim, not independent validation that every fault timing or every firmware version completed the path correctly.

---

## Historical record

### H/P — Intel exposes a cumulative unsafe-shutdown event count in the named SSD 320

The September 2011 product specification lists SMART attribute `C0h` as `Power-Off Retract Count (Unsafe Shutdown Count)`. Intel says its raw value reports the **cumulative number of unsafe (unclean) shutdown events over the life of the device**.

This is direct named-product evidence that the SSD retains a summary of a class of past power-transition events rather than exposing only current payload and current error state.

The same row gives an operational criterion: the event is counted when the device is powered off without `STANDBY IMMEDIATE` being the last command.

The historical vocabulary should be preserved exactly enough to avoid two different anachronisms:

- the period product document really does use the inherited-looking label `Power-Off Retract Count`;
- the document itself parenthetically identifies the SSD meaning as `Unsafe Shutdown Count`.

Nothing in this source establishes a mechanical retract operation inside the SSD.

### H/P — Intel classifies C0h as a self-preserving event-count attribute, not a thresholded pre-fail verdict

Table 12 sets C0h flags to `SP=1`, `EC=1`, `OC=1`, and `PW=0`, with no threshold. Table 13 defines those flag names.

The safe historical statement is therefore:

> Intel classified this field as a self-preserving event count collected online/offline and did not classify it as a pre-fail warranty attribute or give it a threshold in this product table.

This does **not** establish the internal nonvolatile data structure, exact counter-update transaction, wear policy, or power-fail atomicity of the counter itself.

### H/P — Intel's power-loss brief treats the same unsafe-event class as an occasion for protection work

The March 2011 brief uses the same `STANDBY IMMEDIATE` boundary to distinguish clean from unsafe shutdown. Yet the purpose of the advertised SSD 320 protection path is precisely to act when an unsafe/unexpected power-loss event occurs.

Intel describes a power-fail detector, controller firmware, supply isolation, stored capacitor energy, and transfer of temporary user/system data to NAND.

Thus the manufacturer's own documents do not support reading `unsafe shutdown` as synonymous with `data was lost`. In one document it is an **event classification**; in the other it is the **triggering circumstance for a protective response**.

---

## Engineering reconstruction

### E — unsafe-shutdown event evidence != power-loss-protection failure evidence

The C0h counting rule is defined by the shutdown/control sequence, not by the outcome of the emergency transfer.

Therefore:

```text
unsafe power-transition event observed/classified
        !=
power-loss-protection path failed
        !=
payload corruption demonstrated
```

A counted event can identify exposure to an abnormal shutdown condition without encoding whether every affected payload and controller state ultimately survived.

### E — the same event class can coexist with successful protection

Source B claims that the SSD 320 responds to unsafe shutdown by transferring temporary user/system state to NAND using stored energy. Source A counts unsafe shutdowns according to the absence of the normal `STANDBY IMMEDIATE` handoff.

The two relations are compatible:

```text
normal shutdown protocol absent
        -> event qualifies as unsafe
        -> emergency protection may run
        -> outcome must be established separately
```

The evidence does not let the project turn the last arrow into a guarantee. It only blocks the opposite shortcut that the first condition is itself proof of loss.

### E — cumulative count != per-event history

C0h is a scalar lifetime count. The inspected table does not attach to each event:

- a wall-clock timestamp;
- affected LBAs;
- commands outstanding at failure;
- whether a FLUSH had completed;
- capacitor/PLI health;
- firmware-path completion;
- post-restart recovery result;
- amount of data lost or preserved.

Thus the device retains **compressed event history**, not an event-by-event audit log.

### E — event-history retention != payload retention

The retained C0h value is about the device's own past exposure. It is not the user payload whose durability Case 15 originally analyzes.

That distinction matters because a storage system may preserve a small amount of diagnostic history even when a particular payload is lost, or preserve all payload across an event while still incrementing the event counter.

### E/X — documented cumulative counter semantics != demonstrated power-fail-atomic counter update

The product specification tells the host what C0h is meant to report. It does not reveal when the increment is materialized, what persistence primitive protects the update, or what happens if power collapses during the counter update itself.

Therefore this slice does **not** claim that the counter can never miss, duplicate, tear, reset, or otherwise mis-record an event under any fault.

That is an implementation/fault-injection question.

### E/X — no threshold / advisory classification != no retention risk

`PW=0` and threshold `0 (none)` establish how Intel classified this SMART field. They do not mean that unsafe shutdowns are harmless, nor that any number of such events is safe.

The threshold relation and the physical/durability outcome are different.

---

## Functional analogy

### A/X — later NVMe unsafe-shutdown telemetry is a bounded analogy, not genealogy

Case 55 already grounds a later NVMe SMART / Health interface in which `Unsafe Shutdowns` is cumulative retained device-history state, distinct from current warning state and user payload.

That later interface is useful only as a relation-level comparison:

```text
past abnormal power-transition count
        !=
payload
        !=
complete failure history
```

This deepening does **not** claim that NVMe copied Intel SSD 320 C0h, that ATA SMART and NVMe share an internal implementation, or that the label establishes a direct standards genealogy.

---

## Philosophical interpretation

### I — retention can preserve evidence of a threat without preserving a verdict about its consequence

The narrow conceptual point is not that the SSD has a metaphorical memory of trauma. It is simpler:

> A technical system can retain evidence that a preservation-threatening event occurred while leaving the event's actual effect on the retained object to other evidence.

This is useful for the repository because it separates at least three temporal relations:

1. the payload intended to persist;
2. the abnormal event that threatened or triggered preservation work;
3. a retained summary that the event occurred.

The third relation can outlive the event without becoming a complete history of either the payload or the protection outcome.

The interpretation stops there.

---

## Rejected / unsupported claims

### X — “C0h is a count of failed PLP events”

Rejected. Intel defines the counted event by the shutdown sequence, not by PLP outcome.

### X — “every counted unsafe shutdown caused data loss”

Rejected. Intel's separate power-loss brief presents unsafe shutdown as exactly the circumstance in which the protection mechanism is intended to preserve user/system data.

### X — “zero unsafe shutdowns proves all writes were durable”

Rejected. C0h is only one event count. It says nothing complete about flush correctness, firmware defects, media errors, host ordering, or other durability failures.

### X — “Power-Off Retract Count proves an SSD has a mechanical retract mechanism”

Rejected. The Intel table itself parenthetically names the SSD relation `Unsafe Shutdown Count`. No mechanical retract mechanism is established by this label.

### X — “the SMART count is a complete chronology”

Rejected. The inspected field is a cumulative scalar, not a per-event log.

### X — “Intel's PLP claim is independent conformance evidence”

Rejected. It is manufacturer-primary evidence for the documented design/claim. Independent named-product fault injection remains separate.

---

## What this changes in Case 15

This slice adds a second retained-state layer to the existing power-loss case:

```text
payload + controller state
    -> durability handoff / emergency transfer
    -> recoverable logical state

power-transition event
    -> cumulative SMART event evidence
    -> later host-visible diagnostic history
```

The two paths intersect at the same physical episode but have different sameness rules, evidence content, and failure modes.

The strongest new boundary is:

> **retaining evidence that a durability-threatening event occurred is not the same operation as retaining the payload through that event, and neither relation by itself proves the other succeeded.**

---

## Open work after this slice

- exact C0h update timing and whether its increment is power-fail atomic;
- independent fault injection on a named SSD 320, ideally before/after firmware `4PC10362`;
- exact `BAD_CTX 13x` internal cause and relationship, if any, to event telemetry;
- ATA/SFF genealogy of the `Power-Off Retract Count` / unsafe-shutdown attribute name;
- controller-internal representation of SMART persistence;
- broader SSD telemetry history, which belongs primarily in `computing-archaeology`.

A fresh search of `tmzncty/computing-archaeology` for `Intel SSD 320` found no dedicated overlapping study. The present file therefore keeps only this retention-specific evidence boundary.

"""

def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one anchor, got {count}")
    return text.replace(old, new, 1)

if EVIDENCE.exists():
    if EVIDENCE.read_text() != EVIDENCE_TEXT:
        raise RuntimeError(f"{EVIDENCE} already exists with different content")
else:
    EVIDENCE.write_text(EVIDENCE_TEXT)

case = CASE.read_text()

deepening_anchor = "This is **not** a general history of SSDs, NAND, FTL algorithms, SATA, filesystems, `fsync`, NVMe persistence domains, or every form of power-loss protection."
if "15-intel320-2011-unsafe-shutdown-telemetry-deepening.md" not in case:
    case = replace_once(
        case,
        deepening_anchor,
        "Deepening record: [`../evidence/15-intel320-2011-unsafe-shutdown-telemetry-deepening.md`](../evidence/15-intel320-2011-unsafe-shutdown-telemetry-deepening.md) adds the bounded retained-event-history boundary `unsafe shutdown event != PLP failure verdict`.\n\n" + deepening_anchor,
        "case deepening link",
    )

old_prov = "The full September product specification currently survives in the research path through a non-Intel mirror; its Intel order number, revision/date, and document content are preserved, but the repository does not describe that mirror as current Intel hosting. The April addendum and March power-loss brief are currently available from Intel's own document host."
new_prov = "The September product specification is now directly inspectable from Intel's regional content host (`intel.com.br`), including the SMART tables used in the later telemetry deepening. The April addendum and March power-loss brief are likewise available from Intel-hosted document paths."
if old_prov in case:
    case = replace_once(case, old_prov, new_prov, "case product-spec provenance")

hist_anchor = "### H/P + H/S — August 2011 firmware history adds a named-product unsafe-power-loss recovery defect"
hist_insert = r"""### H/P — Unsafe-shutdown telemetry: event history is not a durability verdict

Intel's September 2011 SSD 320 Product Specification adds a second retained-state layer to the power-loss case. SMART attribute `C0h`, `Power-Off Retract Count (Unsafe Shutdown Count)`, reports the **cumulative number of unsafe/unclean shutdown events over the life of the device**. Intel defines the counted event operationally: the device was powered off without `STANDBY IMMEDIATE` being the last command.

The same row is marked `SP=1`, `EC=1`, `OC=1`, `PW=0`, with threshold `0 (none)`; Table 13 identifies these as self-preserving, event-count, online-collection, and advisory rather than pre-fail classifications.

This does not turn C0h into a payload-durability verdict. Intel's March power-loss brief uses the same clean/unsafe boundary while claiming that, during an unsafe shutdown, power-fail detection plus firmware and onboard capacitance transfer temporary user/system data to NAND. The same physical episode can therefore be:

```text
classified and counted as an unsafe shutdown
        +
handled by the emergency protection path
```

Whether the protection actually succeeded is a separate evidence question.

The cumulative field is also not a complete event log: the inspected specification gives no per-event timestamp, affected LBA set, outstanding-command list, flush state, PLP-health result, or recovery verdict. Nor does it disclose the power-fail atomicity of the counter update itself.

**Primary anchors:** Intel 325152-002US (September 2011), printed pp. 18–19, Tables 12–13; Intel 325207-001US (March 2011), printed p. 1.

"""
if "Unsafe-shutdown telemetry: event history is not a durability verdict" not in case:
    case = replace_once(case, hist_anchor, hist_insert + hist_anchor, "case historical insertion")

eng_anchor = "### E — explicit durability contract ≠ empirical implementation compliance"
eng_insert = r"""### E — unsafe-shutdown event evidence ≠ PLP failure / payload-loss evidence

C0h's classification rule depends on the shutdown/control sequence, not on the outcome of the emergency transfer. A lifetime unsafe-shutdown count therefore records exposure to a class of abnormal power transitions without saying which events caused corruption, which were fully protected, or which payloads were affected.

This yields:

```text
event counted
    !=
protection failed
    !=
payload lost
```

It also yields the converse caution: `C0h == 0` would not prove that every write was properly ordered, flushed, mapped, or otherwise durable.

### E — cumulative event telemetry ≠ per-event audit history

A scalar lifetime count compresses history. It preserves that events have accumulated, but not the sequence-specific evidence needed to reconstruct each event's cause and consequence.

The source also does not reveal the transaction used to preserve C0h itself. Therefore **documented cumulative counter semantics ≠ demonstrated power-fail-atomic counter update**.

"""
if "cumulative event telemetry ≠ per-event audit history" not in case:
    case = replace_once(case, eng_anchor, eng_insert + eng_anchor, "case engineering insertion")

fun_anchor = "### A — comparison with RADOS, Case 05"
fun_insert = r"""### A — comparison with NVMe SMART / Health, Case 55

Case 55 later grounds NVMe SMART / Health fields including cumulative unsafe-shutdown history as non-payload retained device evidence. The useful analogy is only relational: both interfaces can retain a summary of abnormal power-transition exposure without turning that summary into the user payload or a complete failure history.

This does **not** establish an ATA/Intel-320 → NVMe genealogy, shared internal counter implementation, or unchanged semantics.

"""
if "comparison with NVMe SMART / Health, Case 55" not in case:
    case = replace_once(case, fun_anchor, fun_insert + fun_anchor, "case analogy insertion")

rej_anchor = "### X — “this case establishes filesystem `fsync` or NVMe persistence semantics”"
rej_insert = r"""### X — “the unsafe-shutdown SMART count is a count of failed power-loss-protection events”

Rejected. Intel defines C0h by the shutdown sequence. Its separate power-loss brief describes protection work intended to run during that event class.

### X — “Power-Off Retract Count proves an SSD mechanical retract mechanism”

Rejected. The Intel SSD table itself parenthetically identifies the field as `Unsafe Shutdown Count`; the label alone is not mechanism evidence or genealogy.

"""
if "unsafe-shutdown SMART count is a count of failed power-loss-protection events" not in case:
    case = replace_once(case, rej_anchor, rej_insert + rej_anchor, "case rejected insertion")

ledger_anchor = "| FAST ’13 identifies Intel SSD 320 as a failing device | X | explicitly rejected |"
ledger_rows = r"""| Intel SSD 320 C0h retains a cumulative lifetime unsafe/unclean-shutdown event count | H/P | strong: Intel 325152-002US, Tables 12–13 |
| C0h is event classification rather than a PLP-success/failure verdict | E | strongly bounded by Intel's C0h definition plus separate PLP brief |
| a cumulative unsafe-shutdown count is not a per-event payload/recovery log | E | strongly bounded by field structure; no per-event details in inspected table |
| documented cumulative C0h semantics prove power-fail-atomic counter update | X | explicitly rejected; update transaction/fault behavior not disclosed |
| `Power-Off Retract Count` proves a mechanical SSD retract operation | X | explicitly rejected |
"""
if "Intel SSD 320 C0h retains a cumulative lifetime unsafe/unclean-shutdown event count" not in case:
    case = replace_once(case, ledger_anchor, ledger_anchor + "\n" + ledger_rows.rstrip(), "case claim ledger")

case = case.replace(
    "Directly inspected the surviving mirrored PDF at printed pp. 16, 21–22 for command support and cache-control surfaces. The current research path is a third-party mirror; this source is not represented as presently Intel-hosted.  \n   <https://www.ssdwiki.com/media/ssd-320-specification.pdf>",
    "Directly inspected the Intel-hosted PDF at printed pp. 16, 18–19, 21–22 for command support, SMART telemetry, and cache-control surfaces.  \n   <https://www.intel.com.br/content/dam/www/public/us/en/documents/product-specifications/ssd-320-specification.pdf>",
)
CASE.write_text(case)

grounding = GROUNDING.read_text()
grounding = grounding.replace(
    "**Inspection:** directly rendered surviving mirrored PDF, especially printed pp. 16, 21, and 22.",
    "**Inspection:** directly rendered Intel-hosted PDF, especially printed pp. 16, 18–19, 21, and 22.",
)
grounding = grounding.replace(
    "**Evidence class:** `H/P` for the identifiable Intel document; source-host provenance is separately qualified.",
    "**Evidence class:** `H/P` — manufacturer-primary named-product specification.",
)
old_direct = "- `FLUSH CACHE EXT` appears in the 48-bit Address command set."
new_direct = """- `FLUSH CACHE EXT` appears in the 48-bit Address command set;
- SMART attribute `C0h`, `Power-Off Retract Count (Unsafe Shutdown Count)`, reports a cumulative lifetime unsafe/unclean-shutdown event count;
- Intel defines the counted unsafe event by power-off without `STANDBY IMMEDIATE` being the last command;
- C0h is marked self-preserving/event-count/online-collection, advisory rather than pre-fail, with no threshold in Tables 12–13."""
if "SMART attribute `C0h`" not in grounding:
    grounding = replace_once(grounding, old_direct, new_direct, "grounding source D details")

old_bound = "**Boundary:** the inspected PDF is currently reached through a third-party mirror (`ssdwiki.com`). The document itself carries Intel's title/order/date, but this record does not represent the mirror as official Intel hosting.\n\nSurviving copy inspected: <https://www.ssdwiki.com/media/ssd-320-specification.pdf>"
new_bound = "**Boundary:** the product specification is directly inspectable from Intel's regional content host. The SMART table documents host-visible semantics and classifications; it does not disclose the internal counter representation, update transaction, or fault atomicity.\n\nIntel-hosted copy inspected: <https://www.intel.com.br/content/dam/www/public/us/en/documents/product-specifications/ssd-320-specification.pdf>"
if old_bound in grounding:
    grounding = replace_once(grounding, old_bound, new_bound, "grounding provenance boundary")

promo_old = "- the Intel product specification supplies actual named-product FLUSH / write-cache command support, with the mirror provenance explicitly qualified;"
promo_new = "- the Intel product specification supplies actual named-product FLUSH / write-cache command support and directly inspected C0h unsafe-shutdown telemetry semantics;"
if promo_old in grounding:
    grounding = replace_once(grounding, promo_old, promo_new, "grounding promotion source")
GROUNDING.write_text(grounding)

roadmap = ROADMAP.read_text()
roadmap_heading = "## Phase 2 — Build missing technical bridges\n\n"
roadmap_bullet = r"""- [x] Case 15 Intel SSD 320 retained unsafe-shutdown telemetry deepening — [`cases/15-intel-ssd320-power-loss-durability.md`](cases/15-intel-ssd320-power-loss-durability.md), deepened by [`evidence/15-intel320-2011-unsafe-shutdown-telemetry-deepening.md`](evidence/15-intel320-2011-unsafe-shutdown-telemetry-deepening.md): Intel's September 2011 product specification exposes SMART `C0h` as a cumulative lifetime `Power-Off Retract Count (Unsafe Shutdown Count)`, defines the event by absence of `STANDBY IMMEDIATE`, labels it a self-preserving event count with no threshold and advisory rather than pre-fail status, while Intel's March 2011 power-loss brief describes emergency protection work intended to run during that same unsafe-event class. This closes the bounded `unsafe-shutdown event evidence != PLP failure/data-loss verdict` and `cumulative count != per-event audit history` seam. Exact C0h update atomicity, named-device post-fix power-cut validation, `BAD_CTX 13x` internals, and attribute-name genealogy remain open; Case 55's later NVMe counter is used only as a functional analogy, while broader SMART/SSD telemetry history belongs primarily in `computing-archaeology`.

"""
if "Case 15 Intel SSD 320 retained unsafe-shutdown telemetry deepening" not in roadmap:
    roadmap = replace_once(roadmap, roadmap_heading, roadmap_heading + roadmap_bullet, "roadmap insertion")
ROADMAP.write_text(roadmap)

idx = INDEX.read_text()
lines = idx.splitlines()
old_prefix = "| [Intel SSD 320 Power-Loss Protection: Volatile Staging, Flush, and Emergency Retention Work]"
matching = [i for i, line in enumerate(lines) if line.startswith(old_prefix)]
if len(matching) != 1:
    raise RuntimeError(f"Case 15 row: expected one row, got {len(matching)}")
i = matching[0]
lines[i] = "| [Intel SSD 320 Power-Loss Protection: Volatile Staging, Flush, and Emergency Retention Work](cases/15-intel-ssd320-power-loss-durability.md) | **grounded** | nonvolatile NAND behind volatile controller/buffer state + explicit flush-to-media boundary + clean-shutdown handoff + capacitor-backed failure-triggered transfer + retained cumulative unsafe-shutdown event telemetry + named unsafe-power-loss firmware recovery defect/fix | separate medium nonvolatility from end-to-end durability; explicit flush from shutdown paths; fault-event history from protection outcome/data loss; protection architecture from recovery correctness; host-visible capacity from physical media population; contract from measured compliance | [2007–2013 grounding](evidence/15-intel-ssd320-power-loss-durability-grounding.md) + [2011 unsafe-shutdown telemetry deepening](evidence/15-intel320-2011-unsafe-shutdown-telemetry-deepening.md); exact C0h update atomicity, independent named-product post-fix fault injection, exact BAD_CTX internal cause, filesystem `fsync`, NVMe persistence composition, and generic SSD history remain separate work |"
idx = "\n".join(lines) + "\n"

findings = r"""
- **2650 — Intel SSD 320 C0h is a cumulative lifetime unsafe/unclean-shutdown event count.** The September 2011 product specification names `Power-Off Retract Count (Unsafe Shutdown Count)` and defines the raw value as accumulated unsafe shutdown events over the device's life. (`H/P`)
- **2651 — the counted Intel unsafe-shutdown event is protocol/control-sequence qualified.** The product specification defines it by power-off without `STANDBY IMMEDIATE` being the last command, not by a detected payload-corruption outcome. (`H/P`)
- **2652 — C0h is classified as self-preserving + event-count + online-collection, with no threshold and advisory rather than pre-fail status.** Tables 12–13 expose those flags directly; the flags are interface classification, not an internal implementation disclosure. (`H/P`)
- **2653 — unsafe-shutdown event evidence != PLP failure evidence.** The event criterion says what kind of shutdown occurred; it does not say whether the emergency transfer succeeded. (`E`)
- **2654 — unsafe shutdown != demonstrated data corruption.** Intel's separate March 2011 brief describes unsafe shutdown as the circumstance in which the named SSD's power-fail detector, firmware, capacitance, and NAND transfer are intended to protect state. (`H/P`, `E`)
- **2655 — a counted abnormal event can coexist with successful protection.** `normal shutdown protocol absent` and `emergency protection succeeds` are logically compatible relations; outcome requires separate evidence. (`E`)
- **2656 — cumulative event count != per-event audit history.** C0h does not supply per-event timestamps, affected LBAs, outstanding commands, flush state, PLP health, or recovery verdict in the inspected table. (`E`)
- **2657 — event-history retention != payload retention.** C0h retains a diagnostic summary about past power transitions, not the user payload whose durability is at issue. (`E`)
- **2658 — documented cumulative counter semantics != demonstrated power-fail-atomic counter update.** Intel specifies what C0h reports but does not expose increment timing, persistence transaction, or arbitrary-fault behavior. (`E`, `X`)
- **2659 — no threshold / advisory classification != no retention risk.** Intel's SMART classification does not establish that unsafe shutdowns are harmless or that any event count is safe. (`X`)
- **2660 — `Power-Off Retract Count` != evidence of an SSD mechanical retract mechanism.** The same Intel row parenthetically names the SSD field `Unsafe Shutdown Count`; label inheritance alone cannot establish mechanism or genealogy. (`H/P`, `X`)
- **2661 — manufacturer PLP design claim != independent named-product conformance.** Intel's March 2011 brief is strong primary evidence for the documented protection path, but not post-fix fault-injection validation. (`H/P`, `X`)
- **2662 — Case 55 NVMe unsafe-shutdown history ~= Case 15 C0h only as a bounded functional analogy.** Both can retain abnormal-power-event summaries distinct from payload/current warnings; no ATA/Intel→NVMe genealogy or shared implementation is asserted. (`A`, `X`)
- **2663 — retained event evidence can outlive the threatening event without becoming a verdict about its consequence.** This is the narrow philosophical payoff: event trace, retained object, and preservation outcome remain distinct relations. (`I`)
- **2664 — related-repository boundary:** a fresh `tmzncty/computing-archaeology` search for `Intel SSD 320` found no dedicated overlapping study; broader SMART/SSD telemetry and attribute-name genealogy belong there if developed, while Case 15 keeps the retention-specific event-evidence boundary. (`H/P` project-state record)
"""
if "**2650 —" not in idx:
    idx = idx.rstrip() + "\n" + findings.lstrip()
INDEX.write_text(idx)
