# Case 15 Deepening — Intel SSD 320 Unsafe-Shutdown Telemetry Is Event History, Not a Durability Verdict

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

