# Evidence 101H — Seagate 2010 BMS zero-progress ambiguity across the current power epoch

**Status:** `bounded deepening complete`

Related canonical case: [`../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md`](../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md)

Related standards grounding: [`101-t10-2004-2007-background-medium-scan-grounding.md`](101-t10-2004-2007-background-medium-scan-grounding.md)

Related named-product packets:

- [`101-hitachi-2008-bms-policy-log-persistence-deepening.md`](101-hitachi-2008-bms-policy-log-persistence-deepening.md)
- [`101-wd-2024-bms-progress-repair-policy-deepening.md`](101-wd-2024-bms-progress-repair-policy-deepening.md)

Related retention-maintenance observability comparison:

- [`111-seagate-xt2-maintenance-observability-boundary-deepening.md`](111-seagate-xt2-maintenance-observability-boundary-deepening.md)

---

## Question

Case 101 already establishes that SCSI Background Medium Scan (BMS) exposes host-visible status, scan counts, progress, defect records, and implementation-dependent repair policy. It also already distinguishes ordinary suspend/resume behavior from proof of a crash- or power-persistent scan cursor.

This packet asks a narrower question:

> When a host reads `BACKGROUND MEDIUM SCAN PROGRESS = 0000h`, what maintenance history does that value actually prove?

The bounded answer from Seagate's December-2010 SCSI command reference is unusually useful:

```text
no BMS initiated since power on
    -> progress = 0000h

most recent BMS completed
    -> progress = 0000h
```

Therefore one host-visible value represents at least two materially different maintenance histories.

The immediate consequence is:

```text
progress = 0000h
    != unique proof that a scan completed
    != proof that a pre-power-loss scan completed
    != cross-power resume checkpoint
```

This is an interface-observability result. It is **not** a claim about what Seagate firmware privately remembers internally.

---

## Source custody

### P1 — T10/04-198 revision 5, January 2005 — `H/P-standardization`

T10, **_Background Medium Scan_**, document `T10/04-198 revision 5`, 2005:

<https://www.t10.org/ftp/t10/document.04/04-198r5.pdf>

The proposal defines host-visible Background Scan Results information, including:

- whether pre-scan or BMS is active or suspended;
- number of scans performed;
- progress of an active scan;
- defect/error entries;
- ordinary BMS suspend/resume from the suspended location when BMS is disabled and then re-enabled.

This packet uses P1 only to anchor the standards-era interface shape. It does **not** attribute the later Seagate-specific wording about `0000h` and `since power on` to this proposal unless explicitly present in the inspected text.

### P2 — Seagate SCSI Commands Reference Manual, Rev. D, December 2010 — `H/P-interface`

Seagate Technology, **_SCSI Commands Reference Manual_**, publication `100293068`, Rev. D, December 2010:

<https://www.seagate.com/staticfiles/support/disc/manuals/Interface%20manuals/100293068d.pdf>

Relevant material is the Background Scan Results log page (`15h`), especially:

- `BACKGROUND SCANNING STATUS`;
- `NUMBER OF SCANS PERFORMED`;
- `BACKGROUND MEDIUM SCAN PROGRESS`;
- Background Medium Scan defect parameters;
- generic log-parameter control / saving semantics.

P2 is the primary source for the exact dual meaning of zero progress used in this packet.

### P3 — existing Case 101 named-product packets — `repo reuse`

The Hitachi 2008 and Western Digital 2024 packets already establish two nearby but different boundaries:

- save-capable monitoring/log state does not itself prove persistence of an exact scan restart cursor;
- ordinary disable/re-enable suspend/resume behavior does not itself prove cross-power checkpoint semantics.

This packet reuses those results rather than reconstructing them again.

### Related-repository check

`tmzncty/computing-archaeology` was searched for `Background Medium Scan` and `SCSI BMS` during this pass. No dedicated technical-history packet was identified that could be reused directly, so this file remains narrowly scoped to the retention/observability seam rather than creating a second history of SCSI BMS.

---

# 1. Historical / source record

## H/P-101H.1 — T10 standardized a host-visible monitor surface for background scanning

The 2005 T10 proposal describes a Background Scan Results log page through which an application client can monitor background scanning activity.

The status parameter exposes, among other things:

```text
background scanning status
number of scans performed
medium scan progress
```

The proposal also says that if BMS is disabled while a scan is in progress, the scan is suspended, and after BMS is enabled again it resumes from the suspended location.

This is important but bounded evidence:

```text
disable -> suspend -> re-enable -> resume
```

is an ordinary control-path relation. By itself it says nothing about whether the suspended location survives loss of power, controller reset, firmware restart, or another discontinuity.

## H/P-101H.2 — Seagate defines progress as the percent complete of a scan currently in progress

Seagate's December-2010 command reference states that `BACKGROUND MEDIUM SCAN PROGRESS` reports the percent complete of a background scan operation in progress.

Its representation uses a numerator with `65,536 (1_0000h)` as denominator.

The key point is that this field is not documented as an archival record of the most recently completed scan position. It is a progress observable for current activity.

## H/P-101H.3 — Seagate explicitly assigns `0000h` to two different histories

The same definition then states that when there is no background scan operation in progress, the device server sets `BACKGROUND MEDIUM SCAN PROGRESS` to `0000h` in either of these cases:

```text
A. no background scan operation has been initiated since power on

or

B. the most recent background scan operation has completed
```

This is the central historical/source fact of the packet.

The distinction is not inferred from a missing field. The vendor's command manual explicitly assigns the same returned value to both conditions.

## H/P-101H.4 — the wording makes the current power epoch part of the observable's semantics

Condition A is not merely “no scan active.” It is explicitly qualified by **since power on**.

That wording gives the progress field a power-epoch-sensitive interpretation:

```text
current power epoch begins
    -> no BMS initiated yet
    -> progress may be 0000h
```

The source does not say that internal firmware forgets all previous scan history at power-on. It says only that this particular progress value can represent a state in which no BMS has been initiated in the current power epoch.

## H/P-101H.5 — scan counters are a different observable from progress

The same log-page description separately defines `NUMBER OF SCANS PERFORMED` and `NUMBER OF BACKGROUND MEDIUM SCAN PERFORMED`.

Therefore:

```text
progress field
    != scan-count field
```

A host may be able to combine multiple fields to learn more than it could from the progress field alone.

This packet consequently makes only the narrower claim:

```text
BACKGROUND MEDIUM SCAN PROGRESS = 0000h
alone
    != unique completion evidence
```

It does **not** claim that every possible combination of status, count, defect log, vendor data, and historical host observations is ambiguous.

## H/P-101H.6 — BMS status can distinguish active/halted states without making zero progress unique

Seagate also exposes `BACKGROUND SCANNING STATUS`, with values covering conditions such as:

- no scan active;
- BMS active;
- pre-scan active;
- halted due to fatal error;
- halted for vendor-specific causes;
- halted due to temperature;
- halted while waiting for the BMS interval timer.

That richer status surface does not change the narrower encoding fact:

```text
progress = 0000h
```

is not, by itself, a unique completed-pass token.

## H/P-101H.7 — save-capable monitoring data does not manufacture distinctions absent from an encoding

Existing Case 101 evidence already shows that BMS log parameters can participate in generic SCSI log-parameter saving semantics under the relevant control rules.

That creates an important anti-collapse:

```text
some monitoring state may be save-capable
    != exact BMS cursor persistence proved
```

The present packet adds another:

```text
field value may be retained
    != all histories that map to that value remain distinguishable
```

If two source states are intentionally encoded as the same value, preserving the encoded value cannot by itself recreate which source state produced it.

This is an interface-level statement, not an assertion about internal firmware metadata.

---

# 2. Immediate interface consequence

The documented state-to-observable relation can be summarized as follows.

| Maintenance history / current state | `BACKGROUND MEDIUM SCAN PROGRESS` consequence established here | What it proves |
| --- | --- | --- |
| No BMS initiated since current power-on | `0000h` is permitted/documented | No current progress value uniquely implies a completed prior pass |
| BMS currently in progress | Percent-complete numerator | Current run has an observable progress surface |
| Most recent BMS completed | `0000h` is permitted/documented | Completion can also map to zero |
| Prior-power-epoch BMS state | Exact restart behavior not established by this wording | Requires separate evidence |

The relation is therefore many-to-one:

```text
state A: no scan initiated since power on ----+
                                           |
                                           +--> progress = 0000h
                                           |
state B: most recent scan completed --------+
```

A host that only obtains the progress value cannot invert that mapping uniquely.

---

# 3. Engineering reconstruction

The terms in this section are repository-authored analysis language. They are **not** claimed as Seagate or T10 historical terminology.

## E-101H.1 — `power-epoch-scoped progress observable`

A useful engineering description of the Seagate field is:

> **power-epoch-scoped progress observable** — a host-visible value whose documented interpretation includes whether activity has begun since the current power-on, rather than a durable journal of a maintenance operation's complete lineage.

For this source:

```text
power on
    -> no current-epoch scan initiated
    -> progress = 0 possible

scan active
    -> progress reports current run

scan completed
    -> progress = 0 possible
```

This term describes the public interface behavior only.

## E-101H.2 — `many-to-one observability boundary`

A second useful term is:

> **many-to-one observability boundary** — a boundary at which multiple materially different internal or historical states are intentionally represented by the same external observation.

The exact grounded instance is:

```text
never initiated in this power epoch
    and
most recent run completed

both
    -> 0000h progress
```

Consequently:

```text
observable equality
    != historical-state equality
```

## E-101H.3 — activity telemetry is not automatically completion authority

The field can be useful during a live scan while still being insufficient as a stand-alone completion witness after the scan is no longer active.

So:

```text
progress telemetry exists
    != unique completion token exists
```

and:

```text
current activity observable
    != durable maintenance lineage
```

## E-101H.4 — a saved value is not equivalent to a saved distinction

Suppose, without asserting any specific implementation, that a system preserves a returned progress value across some reset boundary.

If that value is `0000h`, preservation alone still does not prove which documented source condition produced it.

Thus:

```text
persistence of representation
    != persistence of all distinctions
```

This is stronger than the generic observation that “logs may be incomplete.” Here the loss of distinction follows from the documented encoding relation itself.

## E-101H.5 — ordinary resume semantics do not establish cross-power resume semantics

The T10-era control behavior gives:

```text
BMS active
    -> EN_BMS cleared
    -> suspended
    -> EN_BMS set
    -> resumes from suspended location
```

It does not, without further evidence, give:

```text
BMS active
    -> power removed
    -> power restored
    -> resumes from same durable cursor
```

Nor does Seagate's zero-progress rule provide that missing evidence.

Therefore:

```text
control suspension cursor
    != proved crash-persistent checkpoint
```

---

# 4. Relation to existing Case 101 packets

## 4.1 T10 2004–2007 grounding

The standards packet establishes the feature family and separates:

```text
host foreground VERIFY
    != autonomous BMS
```

This packet stays one layer lower: once BMS has a progress surface, what can a particular returned value actually establish?

## 4.2 Hitachi 2008 policy/log persistence

The Hitachi packet already established:

```text
save-capable monitoring/log state
    != proved exact persistent BMS restart cursor
```

This packet adds a different reason to resist over-reading telemetry:

```text
even a preserved progress value
    may not uniquely encode maintenance history
```

The two findings are complementary, not duplicates.

## 4.3 Western Digital 2024 progress/repair policy

The WD packet establishes a current named-product manual in which BMS can be suspended and resumed from the last scanned logical block during ordinary enable/disable operation, and in which repair behavior is policy-sensitive.

It still does not prove a cross-power durable cursor.

The Seagate 2010 result here supplies an older, explicit power-epoch-sensitive host-visible semantic boundary.

---

# 5. Functional cross-case comparison

This section is functional analogy only. It makes no genealogy claim.

## 5.1 Case 111 — Seagate XT.2 maintenance observability

Case 111 uses Seagate's XT.2 product manual plus this command-reference family to show that BMS and DST have comparatively rich host-visible status/progress/result surfaces, while the separately documented retention-monitor/rewrite behavior does not expose an equivalent retention-specific completion witness in the inspected public material.

The present Case 101 packet sharpens the comparison:

```text
BMS telemetry exists
    != BMS progress value uniquely proves completion

BMS completion evidence
    != retention-refresh completion authority
```

So there are at least three distinct layers:

```text
maintenance subsystem exists
    -> subsystem exposes telemetry
        -> telemetry may or may not uniquely prove a bounded run completed
            -> even that does not prove another maintenance subsystem completed
```

## 5.2 General maintenance-state comparison

Across other cases in this repository, a recurring pattern is that a system may retain enough state to continue or reconstruct maintenance without exposing one host-visible scalar that uniquely describes the complete historical state.

This is a functional comparison only. No claim is made that SCSI BMS directly influenced later distributed or flash-maintenance designs.

---

# 6. Philosophical interpretation

This section is intentionally interpretive and must not be read as source history.

A useful retention lesson is:

> Preserving a representation is not the same as preserving every distinction that once existed before encoding.

If an interface deliberately maps two histories to one value, then the information loss occurs at the representation boundary even if that value itself is stored perfectly.

For maintenance systems this matters because operators often ask a historical question:

```text
"Has the required work actually completed?"
```

while the interface may expose only a current-state question:

```text
"Is there a scan in progress, and if so how far has it advanced?"
```

Those are related but not identical observability contracts.

---

# 7. Explicit non-claims

This packet does **not** claim any of the following:

1. that Seagate firmware erases an internal BMS cursor at power loss;
2. that Seagate firmware cannot privately preserve a BMS cursor across power cycles;
3. that all BMS log-page state is volatile;
4. that `0000h` always means “no scan has ever run”;
5. that `0000h` always means “the most recent scan completed”;
6. that `0000h` plus every other host-visible field is necessarily ambiguous;
7. that scan counters cannot disambiguate some histories;
8. that power-on clears every BMS counter, defect record, or saved log parameter;
9. that TSD/save-capability semantics prove exact progress-cursor persistence;
10. that ordinary BMS disable/re-enable resume semantics survive power loss;
11. that ordinary BMS disable/re-enable resume semantics do not survive power loss;
12. an exact Seagate cross-power BMS restart location;
13. that a halted BMS necessarily reports the same progress semantics as a completed BMS beyond what the manual explicitly documents;
14. that BMS is equivalent to retention refresh;
15. that BMS completion is evidence that SSD retention-specific maintenance completed;
16. that Seagate's generic command manual describes every private behavior of every Seagate product;
17. that every SCSI implementation uses identical counter persistence semantics;
18. that every later SCSI or SAS revision retained the exact same wording;
19. that a current progress field is useless—only that it is not a unique completion token at zero;
20. that the T10 proposal itself contains the exact later Seagate `since power on` wording unless separately verified;
21. that public observability and internal state are identical;
22. that one many-to-one field prevents a host from building stronger history by logging observations externally;
23. any direct historical lineage from SCSI BMS to NVMe, eMMC, distributed storage, or other maintenance systems;
24. any maturity promotion for Case 101.

---

# 8. What this closes

This packet closes one narrow ambiguity in Case 101:

> **Does `BACKGROUND MEDIUM SCAN PROGRESS = 0000h` uniquely prove that the latest required scan completed?**

For the inspected Seagate 2010 interface definition: **no**.

The documented encoding explicitly allows both:

```text
no scan initiated since power on
```

and:

```text
most recent scan completed
```

to produce the same progress value.

This means the progress field alone is not a cross-power completion witness.

Case 101 remains **`grounded`**. No maturity promotion is warranted by this packet.

---

# 9. Remaining high-value debt

The next useful work is now narrower.

## P1 — named-device cross-power BMS cursor semantics

Find a first-party SAS/SCSI product manual or command document that explicitly states one of:

```text
BMS resumes after power cycle from durable location X
```

or:

```text
BMS restarts after power cycle from beginning / another defined point
```

This would answer the internal-continuity question rather than merely the external-observability question.

## P1 — actual power-cycle trace

A high-value experiment would record:

```text
start BMS
    -> observe nonzero progress
    -> remove/reset power at a known point
    -> restore
    -> read BMS status
    -> read progress
    -> read scan count
    -> inspect defect/error parameters
    -> observe whether scanning resumes, restarts, or remains idle
```

The trace should keep distinct:

- process/controller reset;
- device reset;
- actual power removal;
- clean shutdown versus abrupt power loss.

## P2 — persistent private/vendor cursor evidence

A service manual, vendor diagnostic interface, firmware patent, or other primary material exposing a durable BMS location/checkpoint would be useful, but it should not be substituted for the standard host-visible semantics unless the relation is explicit.

---

## Compact result

```text
T10-era BMS
    -> host-visible status / count / progress
    -> ordinary suspend/resume control exists

Seagate 2010 progress semantics
    -> no scan initiated since power on -> 0000h
    -> most recent scan completed       -> 0000h

therefore

progress value persisted
    != maintenance-history distinction persisted

progress = 0000h
    != unique completion evidence
    != cross-power resume checkpoint
```
