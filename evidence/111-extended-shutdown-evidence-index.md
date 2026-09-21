# Case 111 Evidence Index — Enterprise SSD Extended Shutdown, Powered Maintenance, and Operator Scheduling

## Canonical case

- [`../cases/111-enterprise-ssd-extended-shutdown-maintenance.md`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md)
- Current maturity: **`grounded`**.

This index is navigation and scope control. It does not promote the case beyond `grounded` and does not replace the claim ledgers inside the canonical case and evidence packets.

## What Case 111 is actually about

Case 111 should not be reduced to the slogan “SSDs need refresh.” Its useful research object is the migration of a retention problem across responsibility layers:

```text
finite nonvolatile-media retention
    ↓
device-local monitoring / renewal
    ↓
powered maintenance opportunity
    ↓
background-work scheduling
    ↓
operator shutdown / recommissioning policy
    ↓
completion evidence and future-offline admission
```

The repository keeps these layers distinct because one source rarely establishes all of them.

## Evidence chain

### 1. Pre-2010 mechanism prior art — boot / power-up admission and policy-state alternatives

- [`111-msystems-intel-2004-2009-boot-powerup-refresh-prior-art-deepening.md`](111-msystems-intel-2004-2009-boot-powerup-refresh-prior-art-deepening.md)

Bounded role:

- M-Systems / Ronen, 2004-filed / 2005-published, publicly discloses Flash / nonvolatile-memory renewal according to predetermined conditions including age, periodic schedule, boot, dismount, and data type;
- one embodiment stores a timestamp / storage date, making maintenance admission depend on retained historical control state;
- Coulson, 2008-filed / 2009-published and assigned to Intel in the surviving event record, discloses an SSD-specific power-up background scan;
- that scan uses present correctable-error burden as a proactive retention-margin signal and can rewrite or relocate selected data;
- the example explicitly need not retain time-since-last-rewrite for every location;
- the scan has a progress pointer, but the inspected disclosure does not prove that scan progress survives reset or power loss.

Critical boundary:

```text
public mechanism prior art
    !=
named-product implementation
```

This packet **does not** move the direct named-enterprise-SSD product-manual floor earlier than 5 April 2010.

### 2. First-generation Seagate Pulsar — direct named-product floor, 2010

- [`111-seagate-pulsar-2010-powered-retention-refresh-prior-art-deepening.md`](111-seagate-pulsar-2010-powered-retention-refresh-prior-art-deepening.md)

Bounded role:

- Seagate Pulsar Product Manual `100596473`, Rev. A;
- revision record dates initial release to **5 April 2010**;
- named SLC enterprise SSD family;
- typical one-year power-off retention at 25 °C in that product context;
- powered firmware / hardware can monitor and refresh memory cells;
- operator-facing table simultaneously says preventive maintenance is not required.

Critical boundary:

```text
no routine operator preventive maintenance
    !=
no controller-local retention work
```

and:

```text
commercial shipment chronology
    !=
directly inspected documentation chronology
```

### 3. Seagate Pulsar XT.2 — stronger conditional-rewrite wording, 2011

- [`111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md`](111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md)

Bounded role:

- direct Rev. B product-manual witness in June 2011;
- SLC NAND;
- powered monitoring / refresh plus more explicit conditional rewrite when cell levels decay unexpectedly;
- no routine scheduled preventive maintenance required;
- revision history supports a bounded continuity inference toward the March-2011 Rev. A lineage, but direct Rev. A text remains uninspected.

Critical boundary:

```text
revision-history continuity inference
    !=
direct wording evidence
    !=
implementation / invention date
```

### 4. Seagate Pulsar.2 — later MLC continuity and page-change caution, 2012

- [`111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md`](111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md)

Bounded role:

- later MLC enterprise-SSD product-manual witness;
- powered monitoring / refresh and conditional rewrite;
- three-month-at-40 °C product context;
- revision history records a change to the retention-bearing page between Rev. A and the inspected Rev. B.

Critical boundary:

```text
later similar wording
    !=
automatic back-projection into an earlier revision
```

and:

```text
1 year @ 25 °C on one product
    !=
3 months @ 40 °C on another product
```

### 5. IBM / Dell operator-runbook grounding, 2020–2026

- [`111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md`](111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md)

Bounded role:

- turns long power-off retention into an operator scheduling problem;
- separates standards / qualification background from earlier intervention policy;
- IBM guidance includes a powered interval after a bounded offline interval;
- Dell guidance explicitly describes powered data-retention tasks and a minimum powered duration;
- Dell also describes a read over used NAND as a trigger for retention tasks.

Critical boundary:

```text
qualification horizon
    !=
operator intervention schedule
    !=
minimum powered maintenance opportunity
```

and:

```text
host read sweep
    !=
proof that every physical NAND location is rewritten
```

### 6. IBM / Lenovo cadence and documentation-lineage deepening, 2020–2022

- [`111-ibm-lenovo-2020-2022-shutdown-cadence-lineage-deepening.md`](111-ibm-lenovo-2020-2022-shutdown-cadence-lineage-deepening.md)

Bounded role:

- demonstrates that one standards-level background does not generate one universal field cadence;
- separates generic IBM, TS7770, ESS 5000, later ESS-alert, and Lenovo/Storwize contexts;
- identifies an automatic ESS scrub-admission rule after a shorter offline interval;
- treats Lenovo wording as documentation/platform-lineage evidence rather than automatically double-counting it as independent engineering validation.

Critical boundary:

```text
same standards background
    !=
one universal vendor cadence
```

and:

```text
second corporate masthead
    !=
independent technical witness by default
```

### 7. IBM ESS post-offline scrub completion

- [`111-ibm-ess-post-offline-scrub-completion-deepening.md`](111-ibm-ess-post-offline-scrub-completion-deepening.md)

Bounded role:

- adds a named system-level scrub process after a long-offline interval;
- adds operator-visible per-vdisk completion evidence;
- distinguishes time under power from observed completion of the named system-layer scrub.

Critical boundary:

```text
powered maintenance opportunity
    !=
scrub admitted
    !=
per-vdisk scrub completion observed
```

and:

```text
system scrub complete
    !=
proof that every hidden SSD-firmware maintenance task is complete
```

### 8. NetApp rated-life / future-offline-retention admission

- [`111-netapp-rated-life-offline-retention-telemetry-deepening.md`](111-netapp-rated-life-offline-retention-telemetry-deepening.md)

Bounded role:

- uses rated-life evidence to change warning / replacement policy;
- preserves the distinction between current serviceability and future long-offline retention confidence;
- keeps model-derived wear state separate from a deterministic immediate-failure verdict.

Critical boundary:

```text
currently readable / serviceable
    !=
trusted for future long powered-off retention
```

## Cross-layer state model

The evidence now supports a deliberately layered model:

```text
A. media condition
    retained charge / error margin / wear history

B. device-local policy evidence
    retained age / schedule
    OR newly observed error burden

C. device-local maintenance admission
    boot / power-up / idle / threshold / periodic policy

D. device-local maintenance execution
    monitor / scan / correct / rewrite / relocate

E. device-local progress / completion
    may or may not be exposed or persisted

F. system-level maintenance admission
    long-offline trigger / scrub scheduling

G. operator policy
    calendar intervention / powered dwell / read sweep / backup / environment

H. operator-visible completion evidence
    e.g. named system scrub completion

I. future-offline admission
    wear / rated-life / policy judgment
```

The repository should not replace this with one boolean `healthy` or `refreshed` flag.

## Current source-critical distinctions

### Filing / priority is not publication

The new prior-art packet makes chronology explicit:

```text
priority date
    !=
filing date
    !=
public publication date
    !=
product implementation date
```

A 2008 filing published at the end of 2009 is not described here as “public in 2008.”

### Patent disclosure is not product implementation

The Coulson publication is an SSD-specific mechanism witness, but no inspected source currently ties it directly to X25-M, X25-E, or another named Intel shipping SSD.

```text
assignee + contemporaneous product family
    !=
implementation proof
```

### Product documentation is not invention priority

The 5-April-2010 Pulsar manual remains the earliest directly inspected **named enterprise-SSD product-manual** witness currently used by Case 111.

That does not make Seagate the inventor of Flash refresh or boot/power-up retention maintenance.

### Power is an opportunity, not a completion certificate

Across the mechanism and runbook layers:

```text
power restored
    !=
background scan / scrub complete
```

The Coulson design explicitly advances a background scan during idle opportunity; Dell assigns a minimum powered interval; IBM ESS provides a distinct system-layer completion witness.

### Readability is not future-retention confidence

The Coulson threshold design renews data while errors remain correctable; NetApp later distinguishes high rated-life use from immediate device failure while changing future-offline policy.

```text
recoverable now
    !=
sufficient future retention margin
```

### “Refresh” is not one universal primitive

Across Case 111 and adjacent prior art, `refresh` can refer to:

- restoration pulses for disturbed Flash cells;
- internal Flash traversal;
- timestamp / age / boot-triggered renewal;
- SSD error-threshold rewrite or relocation;
- product-manual monitor / refresh behavior;
- later operator-level retention tasks.

The shared word does not establish a shared trigger, geometry, scheduler, mapping semantics, or genealogy.

## Controlled comparison targets

Useful internal comparisons, without asserting historical continuity:

- **Case 36** — Flash Correct-and-Refresh: academic algorithm / ECC-margin maintenance, not proven to be the vendor implementations here;
- **Case 37** — Samsung 840 EVO old-data performance restoration: powered periodic product episode with different symptom framing and product class;
- **Case 52** — NAND read disturb: another case where present observation / retained policy can generate future maintenance obligations;
- **Case 55** — NVMe SMART / Health endurance telemetry: model-derived endurance state can alter operator judgment without being an immediate-failure bit;
- **Case 67** — OCP `Refresh Counts`: telemetry/accounting vocabulary must not be merged with product-manual `refresh memory cells` wording;
- **Case 76** — JESD218 SSD endurance/retention qualification: qualification relation is not the same as autonomous maintenance or a field runbook.

## Related-repository routing

Fresh exact-number code search in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) did not surface a dedicated `US20090327581A1` packet during the current slice.

Keep `technical-retention` focused on:

- retained policy state versus re-observed evidence;
- maintenance admission / opportunity / progress / completion;
- future-offline admissibility;
- chronology and evidence-layer distinctions.

Prefer `computing-archaeology` for broad histories of:

- M-Systems / SanDisk controller and product genealogy;
- Intel X25 controller / firmware genealogy;
- the larger Flash-refresh patent network;
- SSD market chronology;
- exact commercial adoption and silicon/firmware implementation.

## Remaining high-value debt

The current evidence chain is broad enough that further Case 111 work should be narrower, not another generic SSD-retention overview.

Highest-value unresolved slices are:

1. **pre-5-April-2010 named-product evidence** — direct product manual / firmware note / qualification material showing powered retention renewal;
2. **Intel implementation bridge** — evidence connecting Coulson's 2009-public mechanism to a named shipping SSD, or evidence showing that no such attribution can safely be made;
3. **maintenance-progress restart semantics** — whether a real product persists, reconstructs, or discards scan/scrub progress after reset or interrupted power;
4. **independent validation** — controlled tests of error margin before and after retention renewal;
5. **controller-specific Dell behavior** — a named controller/firmware family for the read-triggered retention task;
6. **completion telemetry below the storage-system layer** — device-local evidence, if any, that a retention-maintenance pass finished;
7. **capacity / used-data scaling** — direct evidence for how maintenance duration scales rather than inferring a formula from operator guidance;
8. **later NAND-generation drift** — how the operator schedule changes as ECC, NAND generation, and controller policy change.

## Status decision

**No maturity promotion.**

Case 111 remains `grounded` because the new packet improves mechanism chronology and the evidence graph, but it does not close the product-implementation and independent-validation gaps strongly enough to justify a stronger status.
