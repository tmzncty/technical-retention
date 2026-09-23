# Evidence 111H — Seagate Pulsar XT.2 maintenance observability: BMS/DST status versus retention-refresh completion

**Status:** `bounded deepening complete`

Related canonical case: [`../cases/111-enterprise-ssd-extended-shutdown-maintenance.md`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md)

Related XT.2 chronology / powered-retention packet: [`111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md`](111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md)

Related OCP maintenance-accounting boundary: [`67-2020-2025-ocp-refresh-count-semantics-deepening.md`](67-2020-2025-ocp-refresh-count-semantics-deepening.md)

---

## Question

Case 111 already establishes that Seagate's June-2011 Pulsar XT.2 manual documents powered cell-retention monitoring and conditional rewrite, while later IBM/Dell guidance turns long shutdown into an operator scheduling problem.

The canonical case still has a narrower observability question:

> What telemetry, if any, can prove that prescribed background retention work has completed outside the already-grounded IBM ESS system-level scrub witness?

This packet does **not** claim to recover a retention-refresh completion indicator. Instead, it uses the same named SSD and its referenced Seagate command manual to establish a sharper interface boundary:

```text
Pulsar XT.2 exposes host-visible status / progress / result surfaces
for some maintenance and diagnostic subsystems

but the inspected XT.2 retention-refresh description
identifies no analogous host-visible retention-refresh completion surface
```

The result is a bounded negative finding, not an argument from generic silence:

```text
maintenance telemetry exists
    !=
retention-maintenance completion is observable
```

and:

```text
one background subsystem's status/progress/result interface
    !=
another background subsystem's completion contract
```

---

## Source custody

### P1 — Seagate Pulsar XT.2 SAS Product Manual, Rev. B, June 2011 — `H/P`

Seagate Technology, **_Pulsar XT.2 SAS Product Manual_**, publication `100647497`, Rev. B, June 2011:

<https://www.seagate.com/staticfiles/support/docs/manual/sas/100647497b.pdf>

The cover identifies:

- product family: `Pulsar XT.2 SAS`;
- publication: `100647497`;
- revision: `Rev. B`;
- date: `June 2011`;
- standard models: `ST400FX0002`, `ST200FX0002`, `ST100FX0002`;
- SED model: `ST400FX0012`.

The manual explicitly lists Seagate **SCSI Commands Reference Manual part number `100293068`** and SAS Interface Manual part number `100293071` as reference documents. It also says that more information about SCSI commands used by Seagate SAS drives is in part number `100293068`.

Relevant inspected sections are:

- reliability / retention material around printed pp. 14–16;
- §6.2.5 `Data Retention`;
- §6.3.6 `Drive Self Test (DST)`;
- §9.4 `Background Media Scan`;
- the supported-command table entries for LOG SENSE, Background Scan Results log page, Self-test Results page, and Background Scan mode subpage.

### P2 — Seagate SCSI Commands Reference Manual, Rev. D, December 2010 — `H/P-interface`

Seagate Technology, **_SCSI Commands Reference Manual_**, publication `100293068`, Rev. D, December 2010:

<https://www.seagate.com/staticfiles/support/disc/manuals/Interface%20manuals/100293068d.pdf>

This is not treated as a product-specific hidden-firmware disclosure. It is used because P1 explicitly references part number `100293068` for SCSI command behavior and P1 separately states that XT.2 supports the relevant Background Scan Results log page.

Relevant inspected material is §4.2.3 `Background Scan Results log page (15h)`, including:

- Background Scanning Status;
- Number of Scans Performed;
- Background Medium Scan Progress;
- Background Medium Scan error parameters;
- parameter-saving semantics.

### P3 — existing Case 67 OCP packet — `cross-case reuse`

[`67-2020-2025-ocp-refresh-count-semantics-deepening.md`](67-2020-2025-ocp-refresh-count-semantics-deepening.md) already inspected OCP primary specifications and established that OCP SMART-10 `Refresh Counts` is integrity-maintenance block-reallocation accounting, while OCP background refresh is a separate whole-device coverage obligation.

This packet reuses that result rather than duplicating the OCP history.

### Source-rendering note

The official Seagate-hosted PDFs were inspected through their indexed text. Page-image rendering was attempted in this research pass but the remote PDF screenshot path returned cache-miss errors. No graphical/layout inference beyond the indexed text, section numbering, and page anchors is made here.

---

## Historical / source record

### H/P-111H.1 — XT.2 retention maintenance is documented as powered monitoring plus conditional rewrite

The XT.2 reliability material states that power-off retention degrades with use and temperature, then distinguishes the powered regime: while power is applied, firmware/hardware can monitor and refresh memory cells.

Its dedicated §6.2.5 narrows the relation further:

```text
while powered
    -> cell retention is monitored
    -> if cell levels decay unexpectedly
       -> cells are rewritten
```

The manual does not name a host-visible retention-refresh status bit, progress field, completed-pass counter, or per-run result log in this section.

That absence is recorded only at the level of the inspected public XT.2 interface documentation. It is not proof that no vendor-private diagnostic or factory interface ever existed.

### H/P-111H.2 — the same named drive separately exposes Background Media Scan

XT.2 §9.4 describes **Background Media Scan (BMS)** as a self-initiated scan that reads across the entire addressable media while the drive is idle.

The manual says BMS can:

- find unreadable or recovered-error sites;
- log those sites;
- reallocate them;
- allow a host using the BMS Log Page to check **BMS status and results** rather than performing its own full media scan.

The scheduling contract is also explicit:

- BMS starts after 500 ms of idle time;
- it operates in 500 ms bursts;
- it suspends for 100 ms to permit other background functions to run;
- host commands interrupt BMS promptly;
- BMS-initiated error recovery is completed before returning to host-command service.

This is a different documented subsystem from §6.2.5 retention monitoring/rewrite.

### H/P-111H.3 — XT.2 advertises the BMS control/telemetry surfaces in its command table

The XT.2 supported-command table explicitly marks as supported:

```text
LOG SENSE (4Dh)
Background Scan Results log page (15h)
Self-test Results page (10h)
Background Scan mode subpage (1Ch/01h)
```

This matters because it prevents a weak argument of the form:

> perhaps the manual simply never documents host-visible maintenance state at all.

It does document such surfaces for specific subsystems.

### H/P-111H.4 — Seagate's referenced command manual defines concrete BMS state, progress, and scan-count fields

The December-2010 Seagate SCSI Commands Reference Manual defines Background Scan Results log page `15h`.

Its Background Scanning Status parameter includes at least:

```text
ACCUMULATED POWER ON MINUTES
BACKGROUND SCANNING STATUS
NUMBER OF BACKGROUND SCANS PERFORMED
BACKGROUND MEDIUM SCAN PROGRESS
NUMBER OF BACKGROUND MEDIUM SCANS PERFORMED
```

The status codes distinguish states including:

```text
00h  no background scans active
01h  background medium scan active
02h  background pre-scan active
03h  background medium scan halted due to fatal error
04h  halted due to vendor-specific pattern of errors
05h  halted due to medium formatted without P-list
06h  halted for vendor-specific cause
07h  halted due to temperature outside allowed range
08h  halted waiting for interval-timer expiration
```

Thus the host-observable surface is not merely a lifetime counter. It includes current activity/halt state.

### H/P-111H.5 — BMS progress is explicitly quantified

The same command manual defines `BACKGROUND MEDIUM SCAN PROGRESS` as the percentage complete of a background scan in progress, encoded as a numerator with `65,536` as denominator.

When no background scan is in progress — including the case where the most recent scan has completed — the field is set to zero.

This creates an important source-critical guardrail:

```text
progress == 0
    != by itself proof that one complete scan just finished
```

because zero can also mean no scan has been initiated since power-on.

The `NUMBER OF SCANS PERFORMED` / `NUMBER OF BACKGROUND MEDIUM SCANS PERFORMED` fields provide a distinct historical count of completed scan operations.

### H/P-111H.6 — some BMS status state is saveable, but persistence timing is not a transactional checkpoint contract

For the Background Scanning Status log parameter, the command manual says that when `TSD` is zero the device server saves the log parameter to its medium at **vendor-specific intervals**; when `TSD` is one implicit saving is disabled by the application client.

This is useful, but bounded:

```text
saveable status parameter
    != every progress update durably checkpointed
    != crash-atomic scan cursor
    != exact restart semantics
```

The source does not give a universal persistence interval or guarantee that the last host-observed progress value will be recovered after arbitrary power loss.

### H/P-111H.7 — XT.2 gives an even stronger explicit result surface for Drive Self Test

XT.2's DST section provides a second within-product comparison.

When DST begins, the drive creates a Self-test Results Log entry and stores the log page in nonvolatile memory. After the self-test completes or is aborted, it updates the result value in nonvolatile memory. A result value of zero means the drive passed with no errors detected; nonzero values encode failure/abort conditions.

Thus the same manual can document an operation with an explicit lifecycle:

```text
start
    -> persistent in-progress/result record
    -> completion or abort
    -> persistent terminal result
```

No equivalent retention-refresh result lifecycle is identified in the inspected §6.2.5 material or supported-log-page descriptions.

---

## Engineering reconstruction

The following terminology is project reconstruction, not Seagate's historical vocabulary.

### E-111H.1 — maintenance opportunity, maintenance activity, maintenance progress, and maintenance completion are different evidence classes

The XT.2 record supports at least four distinct evidence classes:

```text
maintenance opportunity
    = device is powered and relevant controller machinery can run

maintenance activity evidence
    = a maintenance subsystem reports that it is active / counts work

maintenance progress evidence
    = a subsystem reports position or percent complete

maintenance completion evidence
    = a subsystem exposes a terminal/result condition for a bounded run
```

They are not interchangeable.

For retention monitoring/rewrite, P1 establishes opportunity and mechanism description. It does not identify a host-visible bounded-run completion witness.

For BMS, P1/P2 establish current status, progress, scan counts, and error-result surfaces.

For DST, P1 establishes persistent terminal result reporting.

### E-111H.2 — same physical device does not imply one unified maintenance state machine

XT.2 places these functions in different documentation contexts:

```text
Data Retention
    -> endurance / retention management
    -> powered monitoring + conditional rewrite

Background Media Scan
    -> defect / error management
    -> idle-time whole-address-space reads
    -> status/results log

Drive Self Test
    -> diagnostic validation
    -> explicit terminal result log
```

The controller may share lower-level read, ECC, copy, and reallocation primitives, but the public interface contracts are different.

Therefore:

```text
same SSD controller
    != same trigger
    != same coverage rule
    != same progress semantics
    != same completion authority
```

### E-111H.3 — BMS completion cannot be substituted for retention-refresh completion

BMS reads the addressable space while idle and exposes scan-specific telemetry.

Retention maintenance is documented separately as monitoring cell levels and rewriting when decay is unexpected.

Nothing inspected says:

```text
one BMS pass complete
    -> all retention-refresh obligations complete
```

or:

```text
BMS progress
    == retention-refresh progress
```

or:

```text
BMS error reallocation
    == retention conditional rewrite
```

A BMS completion witness is authority for a BMS claim only.

### E-111H.4 — a host-visible status field can be weaker than a completion proof

Even for BMS, the interface must be read carefully.

A single observation of:

```text
BACKGROUND SCANNING STATUS = no scan active
BACKGROUND MEDIUM SCAN PROGRESS = 0
```

is ambiguous between at least:

- no scan has started since power-on;
- the most recent scan completed;
- another documented non-active state relation depending on surrounding history.

A stronger run-level inference requires surrounding state such as scan-count change and absence of a halted status.

So:

```text
observable state
    != self-interpreting completion proof
```

### E-111H.5 — persistent diagnostic results show that completion observability is an interface design choice

DST demonstrates that Seagate could expose persistent terminal state when the interface contract called for it.

That makes the retention-refresh boundary more meaningful:

```text
device performs internal work
    != host is given a terminal result for that work
```

The gap is not simply `old SSDs had no telemetry`.

It is subsystem-specific observability.

### E-111H.6 — this narrows, but does not close, Case 111's operator-completion problem

Later IBM/Dell runbooks prescribe powered dwell or read sweeps because operator policy needs a practical intervention rule.

XT.2 shows a device may simultaneously contain:

- hidden/autonomous retention maintenance;
- explicitly observable BMS maintenance;
- explicitly result-bearing DST diagnostics.

The operator therefore cannot infer:

```text
"some maintenance log looks complete"
    -> "all retention work needed for future offline storage is complete"
```

A valid completion criterion must be tied to the exact maintenance subsystem and vendor/system contract.

---

## Cross-case comparison

### Case 111 — IBM ESS system-level scrub completion

The IBM ESS evidence provides an operator-visible system message indicating completion of a scrub run for each vdisk.

Functionally:

```text
ESS scrub completion message
    -> completion evidence for that named system scrub

XT.2 BMS status / progress / counts
    -> observability for that named drive scan

XT.2 powered retention monitoring/rewrite
    -> no comparable completion surface identified in inspected public manual
```

None of the three should be used as authority for the others.

### Case 67 — OCP `Refresh Counts`

Case 67 already establishes:

```text
OCP SMART-10 Refresh Counts
    -> cumulative integrity-maintenance block-reallocation accounting

OCP BKGND-1..3
    -> whole-device background-refresh obligation
```

and that an increasing cumulative counter does not prove whole-device coverage completion.

XT.2 supplies an earlier named-product complement:

```text
maintenance accounting/status can be visible
    while retention-maintenance completion remains unexposed
```

No genealogy is asserted between 2011 Seagate interfaces and later OCP telemetry.

### Case 36 — Flash Correct-and-Refresh

Case 36 gives a research mechanism with explicit error-margin logic. XT.2 does not expose enough internals to identify its retention rewrite with FCR.

The observability lesson is independent of mechanism identity:

```text
internal maintenance mechanism
    != management-plane completion contract
```

### Case 37 — Samsung 840 EVO old-data refresh

The functional resemblance is powered renewal of NAND-resident state. The user-visible products, symptom, media, triggers, cadence, and exposed completion semantics differ or remain unknown.

No technical ancestry is claimed.

---

## Prior-art / chronology boundary

This packet does **not** move Case 111's earliest named-product powered-retention witness. The existing first-generation Pulsar packet remains the earlier direct 5-April-2010 documentation floor.

The new historical object is different:

> **By June 2011, a named enterprise SSD public manual simultaneously documented powered retention rewrite and explicit host-observable progress/result machinery for other background/diagnostic subsystems.**

That supports a bounded interface-history statement:

```text
public maintenance observability existed on the device
    != retention-refresh completion observability was documented
```

It is not an invention-priority claim for BMS, SCSI log pages, SSD telemetry, or maintenance completion reporting.

---

## Philosophical interpretation

A narrow project interpretation follows from the technical boundary:

> **Maintenance can be real without being fully legible to the layer that depends on its outcome.**

The important distinction is not `visible` versus `invisible` in the abstract. XT.2 shows multiple visibility regimes inside one product: one subsystem exposes progress and scan history, another exposes persistent terminal diagnostic results, while the public retention section describes autonomous conditional rewrite without an equivalent host completion token.

This is project vocabulary, not Seagate's philosophy. It does not imply that hidden work is unreliable, that visible counters are sufficient authority, or that every storage system should expose every controller state.

---

## Explicit non-claims

This packet does **not** claim that:

1. XT.2's BMS is the same process as its cell-retention monitoring/rewrite;
2. a completed BMS pass proves retention maintenance complete;
3. BMS scans every physical NAND page rather than the documented addressable space;
4. every BMS read causes a rewrite;
5. every BMS error causes the same reallocation path as retention maintenance;
6. XT.2 exposes a public retention-refresh progress counter;
7. XT.2 exposes a public retention-refresh completion bit;
8. no vendor-private XT.2 retention diagnostic ever existed;
9. every command/log page implemented by firmware is exhaustively described in the public product manual;
10. `BACKGROUND MEDIUM SCAN PROGRESS = 0` alone proves a completed scan;
11. `no background scans active` alone proves a completed scan;
12. `NUMBER OF SCANS PERFORMED` identifies what every scan examined internally;
13. BMS status is checkpointed after every progress update;
14. vendor-specific log-save intervals imply crash-atomic persistence;
15. DST completion proves media retention readiness;
16. a DST pass proves future long-offline retention;
17. Seagate's 2010 SCSI command manual is a firmware source-code disclosure;
18. OCP `Refresh Counts` descends from Seagate BMS or XT.2 retention refresh;
19. later Dell read-triggered retention tasks are XT.2 BMS;
20. IBM ESS scrub and XT.2 BMS share one implementation;
21. public absence of a retention-completion field proves physical impossibility of detecting completion;
22. June 2011 is the first historical occurrence of maintenance telemetry;
23. June 2011 is the first SSD with BMS;
24. host-visible completion is always necessary for safe retention policy.

---

## Claim ledger

| ID | Layer | Claim | Strength | Boundary |
| --- | --- | --- | --- | --- |
| H-111H.1 | historical/product | XT.2 Rev. B is a Seagate product manual dated June 2011 | strong | direct first-party PDF |
| H-111H.2 | historical/product | XT.2 documents powered retention monitoring and conditional rewrite | strong | direct product wording |
| H-111H.3 | historical/product | XT.2 documents BMS as a self-initiated idle-time scan across addressable media | strong | direct product wording |
| H-111H.4 | historical/product | XT.2 says hosts may check BMS status/results | strong | direct product wording |
| H-111H.5 | historical/interface | XT.2 supports Background Scan Results log page 15h and Background Scan mode subpage | strong | product command table |
| H-111H.6 | historical/interface | referenced Seagate command manual exposes BMS status, progress, and scan counts | strong | first-party interface manual referenced by product |
| H-111H.7 | historical/interface | BMS status parameter may be saved at vendor-specific intervals | strong | does not define crash-atomic checkpointing |
| H-111H.8 | historical/product | DST writes/updates Self-test Results in nonvolatile memory | strong | diagnostic result, not retention result |
| E-111H.1 | engineering | maintenance opportunity/activity/progress/completion are distinct evidence classes | strong reconstruction | constrained by named interfaces |
| E-111H.2 | engineering | BMS completion evidence cannot authorize a retention-refresh completion claim | strong | no source identity between subsystems |
| E-111H.3 | engineering | maintenance telemetry can exist without target-maintenance completion observability | strong | public-interface boundary only |
| A-111H.1 | analogy | ESS scrub, XT.2 BMS, and OCP counters are different observability surfaces | useful | no mechanism/genealogy identity |
| P-111H.1 | interpretation | preservation work can be real while only partially legible upward | bounded | project interpretation |

---

## What this closes

This packet closes a narrow part of Case 111's telemetry question:

```text
Does a named enterprise SSD expose host-visible maintenance state at all?
    -> yes, XT.2 exposes BMS status/results and DST results.

Does that fact provide a documented XT.2 retention-refresh completion witness?
    -> no, not in the inspected public retention/interface material.
```

The bounded result is stronger than either extreme:

```text
"there is no telemetry"
    -> false for the named device

"there is maintenance telemetry, therefore retention work is complete"
    -> unsupported
```

---

## Remaining debts

### P1 — find a named drive with a retention-specific completion surface

Highest-value next evidence would be a first-party SSD/NVMe/SAS source that explicitly ties a host-visible field to completion of retention refresh / data-retention maintenance, not merely to generic scan, patrol, reclaim, or cumulative relocation counts.

### P2 — identify Dell-affected controller/firmware families

Dell article 000198930 says a full read of used NAND triggers data-retention tasks. A named drive/firmware mapping plus first-party telemetry or command documentation could connect the operator procedure to an actual device completion surface.

### P3 — controlled XT.2 observation if hardware becomes available

A useful experiment would record, across a long powered interval:

- Background Scan Results log page;
- Self-test Results log page;
- any vendor-unique SMART/log fields;
- host read sweep behavior;
- power-cycle persistence of observed state.

This would still not identify retention-refresh completion unless a field is independently tied to that process.

### P4 — separate BMS completion from future offline-retention qualification

Even a fully completed BMS run is a statement about the BMS maintenance contract. Future power-off retention remains conditioned by media wear, temperature, and the product/system retention contract.

---

## Research reuse boundary

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Background Media Scan` and `Pulsar XT.2` found no dedicated packet to reuse in this pass.

A broad history of SCSI Background Media Scan, LOG SENSE telemetry, or Seagate SAS interface evolution belongs there. This packet retains only the Case-111-specific distinction among:

```text
retention maintenance
maintenance observability
scan progress
terminal diagnostic result
operator completion authority
```

---

## Bottom line

The June-2011 Pulsar XT.2 is a useful counterexample to a simplistic `old SSD = opaque maintenance` story.

The same first-party product documentation that describes hidden powered retention monitoring / conditional rewrite also exposes rich host-visible machinery for other operations: BMS has status, progress, scan counts, and error results; DST has nonvolatile terminal results.

Therefore the correct retention conclusion is not that the device lacks maintenance telemetry. It is narrower:

> **maintenance observability is subsystem-specific. A host-visible BMS or diagnostic completion surface does not become a retention-refresh completion witness merely because all of the work occurs inside the same SSD.**

For Case 111, this turns the next search target from generic `SSD telemetry` into a much sharper object: **a named, first-party retention-specific completion or coverage authority.**