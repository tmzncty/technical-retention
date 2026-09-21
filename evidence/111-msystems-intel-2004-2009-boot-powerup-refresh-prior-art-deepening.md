# Evidence — Case 111: 2004–2009 boot / power-up Flash-refresh prior art before the 2010 named-product floor

## Status

**`bounded deepening complete`** for the narrow pre-2010 mechanism-prior-art question addressed here.

This packet does **not** move Case 111's directly inspected **named enterprise-SSD product-manual** floor earlier than the first-generation Seagate Pulsar manual dated 5 April 2010. Instead, it answers a different question:

> Before that product-manual floor, was there already public technical disclosure of nonvolatile-Flash retention maintenance that could be triggered at boot / power-up, including an SSD-specific design that re-observed data and rewrote only locations whose observed error evidence crossed a threshold?

Yes, but the surviving evidence has to be separated into at least two layers:

1. **M-Systems / Amir Ronen, 2004-filed / 2005-published:** generic nonvolatile-memory / Flash refresh according to a predetermined condition, explicitly including data age, periodic refresh, system boot, and system dismount, with in-place or out-of-place renewal.
2. **Richard L. Coulson / Intel assignment, 2008-filed / 2009-published:** an SSD-specific power-up design that starts a background scan, reads locations during idle periods, uses pre-correction error count as a retention-margin signal, and rewrites / relocates only locations that cross a threshold, while also describing optional whole-drive renewal when many weak locations are found.

The bounded contribution is therefore not an invention-priority claim. It is a source-controlled distinction among:

```text
boot-triggered refresh as a generic Flash-management condition
    !=
SSD-specific power-up re-observation + error-threshold admission
    !=
named shipping-product implementation
    !=
later operator-facing extended-shutdown policy
```

## Why this slice

Case 111 already has strong evidence at several later layers:

- the first-generation Seagate Pulsar product manual, Rev. A, 5 April 2010, directly documents powered firmware / hardware monitoring and cell refresh while separately specifying power-off retention;
- later Pulsar XT.2 and Pulsar.2 manuals make conditional rewrite more explicit;
- IBM, Lenovo, Dell, and NetApp later expose operator scheduling, wear-state admission, and system-layer completion evidence for extended shutdown.

What remained weak was the earlier mechanism-prior-art boundary. Without that boundary, the 2010 Seagate product wording can be misread as if it were also the earliest public technical conception of powered Flash retention renewal.

This packet prevents that overclaim while preserving the stronger historical value of the Seagate source as a **named-product manual**.

## Source custody and chronology

### H/P — M-Systems / Ronen patent family

Primary / near-primary patent records inspected for this packet:

- Amir Ronen, **“Refreshing data stored in a flash memory,”** US application `US10/973,272`, published as `US20050243626A1` on **3 November 2005**;
- PCT family publication `WO2005106886A2`, published **10 November 2005**;
- priority is recorded as **29 April 2004**;
- the U.S. application was filed **27 October 2004**;
- the application record names **M-Systems Flash Disk Pioneers Ltd.** as assignee.

Useful public records:

- <https://uspto.report/patent/app/20050243626>
- <https://patents.google.com/patent/WO2005106886A3/en>
- family / later grant reference: `US7325090B2`.

The chronology is handled conservatively:

```text
2004 priority / filing lineage
    !=
2004 public availability proved by this packet

3 Nov 2005 US publication
10 Nov 2005 PCT A2 publication
    -> public technical-disclosure floor used here
```

This packet does not treat priority date, filing date, publication date, grant date, product implementation date, or invention priority as interchangeable.

### H/P — Coulson / Intel-assigned U.S. patent application

Primary patent record:

- Richard L. Coulson, **“Nand memory,”** `US20090327581A1`, application `US12/165,319`;
- filing date: **30 June 2008**;
- publication date: **31 December 2009**;
- the Google Patents event record shows assignment to **Intel Corporation** on **16 September 2008**;
- the publication is currently displayed as `Abandoned`, with Google's standard warning that legal-status metadata is not itself a legal conclusion.

Primary record:

- <https://patents.google.com/patent/US20090327581A1/en>

The source rule is again explicit:

```text
30 Jun 2008 filing
    !=
31 Dec 2009 public publication
    !=
proof of implementation in an Intel shipping SSD
```

The `A1` publication is historically useful even though the U.S. application did not become the kind of product witness supplied by a manual, and its current legal-status field is not evidence that the disclosed engineering mechanism was technically invalid.

## Historical record — M-Systems / Ronen

### H/P — refresh is defined as restoring the stored state, in place or out of place

The 2005 U.S. publication describes management of nominally nonvolatile memory whose data-retention time is finite. It defines refresh broadly enough to include either restoring cells to a state corresponding to the currently stored data or reprogramming the data elsewhere.

That establishes an early public distinction important to this repository:

```text
logical data identity retained
    !=
physical storage location necessarily retained
```

Refresh can preserve the logical payload while changing its physical embodiment.

### H/P — the maintenance trigger may be retained age state

One preferred embodiment records a timestamp associated with when data were programmed and compares that retained timestamp with a system clock. When the age exceeds a chosen interval, the data are refreshed.

For NAND page-level organization, the publication describes storing the timestamp in page spare / extra area, alongside other Flash-management information such as ECC data; refreshing the data also renews the associated storage date.

This directly supplies a retention-control-state example:

```text
payload state
    + retained write/refresh-age evidence
    + clock comparison
    -> maintenance admission
```

The age metadata is not the payload itself, yet it changes whether the payload is selected for renewal.

### H/P — boot and dismount are also explicit trigger classes

The abstract and family publication explicitly name several possible predetermined refresh conditions:

- data age;
- periodic refresh;
- system boot;
- system dismount;
- data type.

Therefore a public Flash-maintenance disclosure tied to **boot** exists by 2005.

This is important because it blocks the stronger claim that a 2008/2009 power-up-triggered SSD scan was the first public idea of associating nonvolatile-memory refresh with a startup event.

### H/P — the source is broader than an SSD extended-shutdown runbook

The M-Systems source is a patent-level Flash / nonvolatile-memory management disclosure. It does not establish:

- one named enterprise SSD product;
- one operator power-off interval;
- a minimum powered dwell time;
- a whole-device scan-completion marker;
- a specific long-offline field incident;
- IBM/Dell-style recommissioning policy.

Its evidentiary value here is mechanism prior art, not product-support chronology.

## Historical record — Coulson / Intel-assigned publication

### H/P — the design starts from uncertainty at power-up rather than a required per-location age log

The 2009 publication describes a NAND SSD that, after power-up and initialization, assumes that some data may not have been written for a long time. It initializes a scan-location pointer and starts a background pass through stored data.

The publication later makes the design choice sharper: the example can operate **without needing a stored concept of time since the last rewrite**. Instead of consulting a retained age for every location, it re-observes the media after startup.

The historical mechanism is therefore distinct from the timestamp-oriented M-Systems embodiment:

```text
M-Systems preferred age path:
retained storage date + clock
    -> infer age
    -> refresh when age condition is satisfied

Coulson example:
power-up uncertainty
    -> re-observe media
    -> infer marginal retention from present error evidence
    -> refresh selected locations
```

This is a functional contrast, not proof that one design was created in response to the other.

### H/P — foreground I/O and the retention scan are interleaved

The SSD performs ordinary functions when busy. During idle opportunity, the location selected by the scan pointer is read.

The scan therefore has at least three operational states:

```text
startup admits background maintenance
    -> ordinary host work can take priority
    -> idle periods are used to advance observation / renewal
```

This differs from a simple instruction to “power the drive on.” Power establishes opportunity; background scheduling determines whether the scan actually advances.

### H/P — ECC/error evidence is used before the data become unrecoverable

For a scanned location, the design counts erroneous bits and compares that count with a threshold selected below the correction capability. If the observed error burden indicates marginal retention, the data are error-corrected and rewritten.

The source's logic is proactive:

```text
still correctable now
    + elevated error evidence
    -> treat retention margin as inadequate
    -> renew before ECC capacity is exhausted
```

Thus present readability and future retention confidence are not the same state.

### H/P — the rewrite can preserve the logical data while changing physical embodiment

The publication describes multiple possible renewal paths:

- rewriting corrected data in the same location;
- reading an erase block, erasing it, and rewriting the pages;
- relocating data to another location.

It does not force one universal primitive.

Accordingly:

```text
refresh obligation
    !=
one fixed physical rewrite geometry
```

and, where relocation is used:

```text
logical payload continuity
    !=
physical-location continuity
```

### H/P — scanning need not mean rewriting the whole device

The stated motivation includes avoiding the write-cycle and power cost of indiscriminately renewing the entire SSD every time it powers up. Locations without the relevant error evidence can be skipped.

The publication separately describes an optional inference: if many locations exceed the threshold, the controller may conclude that the drive has been off for a long period and refresh the whole drive, including locations that did not individually exceed the error threshold.

The source therefore contains two distinct control policies:

```text
selective path:
local observed error evidence
    -> local refresh admission

escalation path:
many weak locations
    -> infer broader retention risk
    -> admit whole-drive refresh
```

The second path must not be silently merged with the first.

### H/P — scan cadence is deliberately not one fixed universal schedule

The publication describes a once-at-power-up scan as one example and also contemplates another pass after elapsed powered time or continuous scanning, while noting power-consumption concerns.

So the disclosed design space already separates:

```text
startup admission
    !=
one-time scan policy
    !=
periodic powered re-scan
    !=
continuous scan policy
```

No one cadence should be retroactively imposed on all implementations.

## Engineering reconstruction

### E — exact event history can be replaced by present-state re-observation for one maintenance decision

The strongest retention-specific result in this slice is not merely that Flash may be refreshed. It is the contrast between two ways to decide **when** renewal is owed.

One path retains historical control evidence:

```text
last-program / last-refresh age state
    + clock
    -> maintenance decision
```

The Coulson path can instead discard that exact history and reconstruct urgency from present media evidence:

```text
startup event
    + fresh read
    + observed error burden
    -> maintenance decision
```

Therefore, for this bounded maintenance decision:

```text
retaining exact age history
    !=
retaining the capability to recover a safe maintenance decision
```

This does **not** mean history is generally unnecessary. It means one design can substitute re-observation of the current physical state for a per-location record of how old that state is.

### E — re-observation authority depends on the remaining correction margin

The method works only while the data remain sufficiently recoverable to be read and corrected.

That creates an ordering relation:

```text
physical degradation progresses
    -> read still succeeds with correctable errors
    -> threshold evidence appears
    -> rewrite obligation is admitted
    -> corrected data are renewed
```

If degradation has already exceeded the available recovery mechanism, the same observation cannot magically reconstruct the lost payload.

Thus:

```text
re-observation can replace some retained history
    !=
re-observation can replace lost recoverability
```

### E — maintenance opportunity, maintenance progress, and maintenance completion are separate states

The power-up event admits the background scan, but the design explicitly interleaves scanning with ordinary I/O and advances a scan pointer over time.

Therefore:

```text
power restored
    !=
scan started
    !=
scan advanced over all intended locations
    !=
all admitted rewrites completed
```

This provides a mechanism-level predecessor to Case 111's later operator-facing distinction between a powered maintenance window and maintenance-completion evidence.

### E — the publication does not establish restart-surviving scan progress

A scan-location pointer exists in the described method, but the inspected publication does not establish that this pointer is itself durably checkpointed across sudden power loss.

That missing detail matters. If power is removed during the background scan, several implementation choices are possible:

- restart scanning from the beginning at the next boot;
- persist a checkpoint and resume;
- reconstruct progress by some other metadata;
- use a different scheduler entirely.

The source inspected here does not resolve which is used in a product.

Therefore:

```text
background scan has a progress variable
    !=
scan progress is proven persistent across restart
```

and:

```text
maintenance algorithm specified
    !=
maintenance restart semantics specified
```

### E — observed error burden is maintenance evidence, not unique causal diagnosis

The publication associates elevated correctable error count with long-unwritten locations losing charge, but it also acknowledges that errors can have other causes.

For the controller decision, exact physical root cause need not be proven before the location is renewed.

Thus:

```text
maintenance-admission evidence
    !=
unique failure-cause diagnosis
```

A conservative policy can act on evidence of reduced margin without proving one exclusive microscopic cause.

### E — “still readable” and “safe to leave untouched” are distinct predicates

The threshold is intentionally set before error count reaches ECC capacity.

That means a location may satisfy:

```text
payload currently recoverable = true
```

while simultaneously satisfying:

```text
retention margin acceptable for continued inaction = false
```

This is one of the clearest technical-retention boundaries in the packet:

> **current serviceability does not imply adequate future retention margin.**

### E — relocation makes maintenance depend on currentness / mapping authority

When corrected data are moved to another location, the renewal operation is no longer only a cell-physics action. The system must also ensure that future reads resolve to the renewed embodiment rather than the stale source.

The patent does not fully specify an SSD FTL crash-consistency protocol, so the safe reconstruction is limited:

```text
rewrite / relocation primitive
    -> may change physical embodiment
    -> requires some correct resolution/currentness relation
```

It does not prove how that relation is checkpointed, ordered, or recovered after interruption.

## Controlled prior-art comparison

### F/A — M-Systems 2004/2005 vs Coulson 2008/2009

The two disclosures solve overlapping retention-maintenance problems through different control evidence.

M-Systems explicitly allows:

```text
retained age / timestamp
periodic schedule
boot event
dismount event
data type
    -> refresh admission
```

Coulson's SSD example emphasizes:

```text
power-up
    -> background media re-observation
    -> current error-count threshold
    -> selective corrected rewrite / relocation
```

The valid comparison is functional:

> Both disclose powered renewal of nonvolatile Flash state, but one foregrounds predetermined conditions including retained age and boot/dismount, while the later SSD-specific example foregrounds present error evidence gathered by a background scan.

This packet does **not** establish a direct M-Systems → Coulson genealogy, licensing relationship, copied design, or inventor influence.

### F/A — earlier Texas Instruments flash-refresh art blocks a generic invention-priority claim

Texas Instruments / John F. Schreck filed `US5365486` in **December 1992** and received the patent in **November 1994** for flash-EEPROM refresh that detects disturbed programmed state using altered read conditions and applies a restoration pulse. Its stated problem includes bitline/wordline stress rather than the SSD long-power-off scenario used by Coulson.

This older evidence is enough to enforce the boundary:

```text
Coulson 2008/2009 SSD power-up scan
    !=
first invention of Flash refresh generally
```

The physical trigger, media organization, and system context differ.

### F/A — Atmel 1998/2000 internal-refresh art supplies another earlier architecture class

Atmel's `US6088268`, filed **17 September 1998** and issued **11 July 2000**, describes a Flash array with an internal refresh pointer and several trigger modes, including automatic refresh associated with erase/program activity and user-triggered refresh.

Again, this is a prior-art guardrail rather than a genealogy claim:

```text
internal refresh pointer / row traversal
    !=
Coulson's SSD startup error-threshold scan
```

The existence of earlier traversal machinery makes it especially important not to promote the later SSD design into a universal origin story.

## Controlled comparison with Case 111's named-product and operator layers

### F/A — 2009 public mechanism disclosure vs 2010 named Seagate product documentation

The first-generation Seagate Pulsar manual remains historically stronger for one specific proposition:

> By 5 April 2010, a named shipping enterprise-SSD family had a surviving first-party product manual that directly said powered firmware / hardware could monitor and refresh memory cells.

The Coulson publication answers a different question:

> By 31 December 2009, an SSD-specific power-up/background-scan/error-threshold refresh mechanism was publicly disclosed in a U.S. patent application associated by assignment record with Intel.

Therefore:

```text
public mechanism disclosure
    !=
named-product implementation witness
```

The earlier patent does not displace the Seagate product-manual floor; it changes the **prior-art boundary around that floor**.

### F/A — do not silently map the patent onto Intel X25-M or X25-E

Intel was publicly shipping SSD products in the same broad historical period, but the inspected Coulson publication does not identify X25-M, X25-E, or another named Intel shipping SSD as implementing the disclosed algorithm.

Consequently:

```text
assignee chronology + contemporaneous products
    !=
product-level implementation proof
```

A separate firmware, manual, qualification, source-code, patent-assignment, or engineering record would be required to bridge that gap.

### F/A — later IBM/Dell runbooks move the problem to another responsibility layer

Case 111's IBM/Dell evidence gives operators instructions about how long a system may remain off, how long it should be powered again, and in Dell's case how a read sweep can trigger hidden data-retention work.

The Coulson design stays inside the device/controller mechanism layer:

```text
power-up / idle scan / threshold / rewrite
```

The later operator layer is:

```text
calendar / shutdown history / power planning / dwell time / read sweep
    -> create enough opportunity for hidden device work
```

The functional bridge is legitimate: both make powered time and re-observation relevant to retention renewal.

The historical identity claim is not legitimate: the packet does not establish that IBM or Dell policies descend from Coulson's implementation.

## Controlled terminology boundary

Several sources use the word `refresh`, but they do not thereby describe one mechanism.

Keep at least the following distinct:

```text
TI 1992/1994
    disturbed-cell detection + restoration pulse

Atmel 1998/2000
    internal Flash refresh traversal / pointer

M-Systems 2004/2005
    predetermined-condition renewal
    including age / periodic / boot / dismount

Coulson 2008/2009
    SSD power-up background scan
    + present error evidence
    + selective corrected rewrite / relocation

Seagate 2010+
    named-product powered monitor / refresh wording

IBM / Dell 2020+
    operator-facing extended-shutdown maintenance policy
```

The same English label does not establish common trigger, unit of work, persistence horizon, scheduler, error model, physical rewrite primitive, or genealogy.

## Philosophical / media-theoretical interpretation

The following is a project-level interpretation, not period vocabulary from M-Systems, Intel, Seagate, IBM, or Dell.

A nonvolatile state can remain apparently passive while the **conditions of trustworthy future availability** depend on a later opportunity to re-observe and renew it.

The contrast between retained-age control and present-state re-observation sharpens that point:

```text
one system remembers when the state was made
another can inspect how the state is doing now
both can use that evidence to decide whether to recreate the state
```

This suggests a bounded retention distinction:

> **Persistence can depend not on preserving the complete history of a state, but on preserving enough recoverability and enough future observation/maintenance capability to reconstruct the next safe action.**

The limit is equally important. If the medium has already degraded beyond recoverability, no later act of observation recreates the lost payload merely because a maintenance algorithm exists.

The interpretation therefore must not become:

```text
all history is replaceable by observation
```

or:

```text
nonvolatile storage is actually volatile memory
```

Neither follows from the mechanism.

## Explicit non-claims

This packet does **not** establish that:

1. M-Systems invented Flash refresh in 2004.
2. Coulson invented Flash refresh in 2008.
3. Coulson invented boot-triggered Flash refresh.
4. Intel invented SSD retention maintenance.
5. 30 June 2008 was the public-disclosure date of `US20090327581A1`.
6. A patent filing date is interchangeable with a publication date.
7. A patent publication is proof of a shipping implementation.
8. Intel X25-M implemented the Coulson design.
9. Intel X25-E implemented the Coulson design.
10. Any other named Intel SSD implemented the Coulson design.
11. Assignment to Intel proves product deployment.
12. The application's later abandoned status makes the technical disclosure historically irrelevant.
13. Google Patents legal-status metadata is a definitive legal opinion.
14. The M-Systems and Coulson designs are historically one lineage.
15. Coulson copied M-Systems.
16. A citation relationship by itself proves inventor influence.
17. M-Systems boot-triggered refresh is identical to Coulson's power-up background scan.
18. The M-Systems timestamp embodiment is required by every claim or implementation in that family.
19. The Coulson design permanently stores time-since-last-write state for every location.
20. The Coulson scan pointer is proven persistent across reset or power loss.
21. Power-up proves a full scan completed.
22. Scan completion proves all admitted rewrites completed under every interruption.
23. A read with correctable errors proves only retention loss as root cause.
24. Error threshold is the same as ECC exhaustion.
25. Present readability implies adequate future retention margin.
26. “Refresh” implies in-place rewriting.
27. “Refresh” implies relocation.
28. “Refresh” implies one fixed NAND page/block geometry.
29. Relocation proves a particular FTL crash-consistency protocol.
30. Seagate's 2010 product wording is derived from Coulson's patent.
31. IBM/Dell extended-shutdown policy is derived from Coulson's patent.
32. Later Dell read-triggered retention tasks are the same algorithm as the 2009 disclosure.
33. TI's 1992/1994 disturb-refresh mechanism is identical to long-offline SSD retention maintenance.
34. Atmel's internal refresh pointer is the same architecture as an SSD background scan.
35. The existence of earlier patent art closes the question of first commercial adoption.
36. The existence of earlier patent art closes the question of first named-product documentation.
37. The existence of a maintenance algorithm proves an infinite retention lifetime.
38. Re-observation can recover payload that has already become uncorrectable.
39. A current-state signal always substitutes safely for retained history.
40. One source's `refresh` terminology may be projected backward or forward onto all Flash products.

## Claim ledger

| Claim | Type | Strength | Boundary |
| --- | --- | --- | --- |
| M-Systems / Ronen U.S. application was filed 27 Oct 2004 and published 3 Nov 2005 | H/P | strong | public patent record; filing != publication |
| M-Systems family has a 29 Apr 2004 priority lineage | H/P | strong | priority metadata; not used as public-disclosure date |
| M-Systems describes refresh triggered by age, periodic schedule, boot, dismount, or data type | H/P | strong | generic NVM/Flash management disclosure, not named enterprise SSD runbook |
| M-Systems describes in-place or out-of-place renewal | H/P | strong | exact product implementation not established |
| One M-Systems embodiment retains timestamps / storage dates | H/P | strong | preferred embodiment; not universal requirement |
| Coulson application was filed 30 Jun 2008 and published 31 Dec 2009 | H/P | strong | public patent record |
| record shows assignment to Intel on 16 Sep 2008 | H/P | strong | assignment chronology != product implementation |
| Coulson describes SSD power-up initiation of a background all-data scan | H/P | strong | scan scheduling can be interleaved with host work |
| Coulson uses observed error count below ECC exhaustion to admit renewal | H/P | strong | threshold selection described; exact product threshold not established |
| Coulson allows corrected rewrite in place or relocation | H/P | strong | multiple physical implementations contemplated |
| Coulson explicitly allows a design without time-since-last-rewrite tracking | H/P | strong | example design; not every implementation |
| Coulson scan pointer is restart-persistent | X | rejected / unproved | no durable-checkpoint semantics established in inspected disclosure |
| 2009 publication proves Intel X25 implementation | X | rejected | no named-product bridge |
| M-Systems 2005 blocks a claim that Coulson first conceived boot-triggered Flash refresh | H/E | strong | earlier public patent disclosure; no genealogy inferred |
| TI 1992/1994 blocks a claim that these later sources invented Flash refresh generally | H/E | strong | different disturb problem / circuitry |
| exact age history can sometimes be replaced by present-state re-observation for maintenance admission | E | strong | bounded to this control relation; requires remaining recoverability |
| power applied != scan complete != maintenance complete | E | strong | scan is background/interleaved and completion semantics are separate |
| currently correctable != adequate future retention margin | E | strong | proactive threshold is below ECC exhaustion |
| public mechanism disclosure != named-product implementation witness | H/E | strong | patent vs 2010 Seagate product manual distinction |

## Related-repository routing

A fresh GitHub code search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for the exact Coulson publication number `US20090327581A1` returned no dedicated packet to reuse at the time of this slice.

That search result is treated conservatively: absence from one code-search result is not proof that the companion repository contains no adjacent SSD / Flash history.

The division of labor remains:

### Keep here

- boot / power-up as a retention-maintenance admission event;
- retained-age policy state versus present-state re-observation;
- ECC-margin evidence as a proactive maintenance signal;
- maintenance opportunity versus progress versus completion;
- restart-persistence question for scan/control state;
- patent disclosure versus named-product evidence;
- controlled connection to Case 111's operator-runbook layer.

### Prefer `computing-archaeology` for later broadening

- M-Systems / SanDisk corporate and controller genealogy;
- Intel NAND/SSD controller genealogy;
- X25-M / X25-E implementation archaeology;
- Flash-refresh patent-network history as a whole;
- exact silicon / firmware adoption;
- manufacturing, controller, NAND-generation, and product-market context.

## Remaining debt after this slice

This packet closes only the bounded question **“did public pre-2010 boot/power-up Flash-retention refresh prior art exist?”** It leaves several higher-value debts open:

1. **named-product adoption:** find a pre-5-April-2010 product manual, firmware note, qualification report, or service document that directly attributes comparable powered retention maintenance to a named shipping SSD;
2. **Intel implementation bridge:** determine whether any X25-family or other Intel product can be tied directly to Coulson's disclosed mechanism;
3. **scan-progress lifetime:** find evidence for whether a shipping implementation retained, discarded, or reconstructed background-scan progress across reset / power loss;
4. **M-Systems implementation bridge:** identify a named product/manual that used the boot/dismount or timestamp policy;
5. **independent validation:** seek controlled experiments that compare pre-maintenance error margin with post-refresh state rather than relying only on algorithm description;
6. **operator-policy bridge:** keep later IBM/Dell scheduling separate unless a source actually links field runbooks to one controller implementation.

Case 111 should remain **`grounded`**. This prior-art deepening changes the mechanism chronology and novelty boundary, not the canonical case's maturity classification.

## Sources

Primary / technical sources:

- Amir Ronen / M-Systems Flash Disk Pioneers Ltd., **“Refreshing data stored in a flash memory,”** U.S. patent application `US20050243626A1`, published 3 November 2005: <https://uspto.report/patent/app/20050243626>.
- Patent family record, `WO2005106886A2/A3`: <https://patents.google.com/patent/WO2005106886A3/en>.
- Richard L. Coulson, **“Nand memory,”** `US20090327581A1`, published 31 December 2009: <https://patents.google.com/patent/US20090327581A1/en>.
- John F. Schreck / Texas Instruments, **“Method and circuitry for refreshing a flash electrically erasable, programmable read only memory,”** `US5365486`, filed 16 December 1992, granted 15 November 1994: <https://patents.justia.com/patent/5365486>.
- Atmel Corporation, **“Flash memory array with internal refresh,”** `US6088268`, filed 17 September 1998, issued 11 July 2000: <https://www.freepatentsonline.com/6088268.html>.

Internal repository context:

- [`../cases/111-enterprise-ssd-extended-shutdown-maintenance.md`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md)
- [`111-seagate-pulsar-2010-powered-retention-refresh-prior-art-deepening.md`](111-seagate-pulsar-2010-powered-retention-refresh-prior-art-deepening.md)
- [`111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md`](111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md)
- [`111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md`](111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md)
- [`111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md`](111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md)
- [`111-ibm-ess-post-offline-scrub-completion-deepening.md`](111-ibm-ess-post-offline-scrub-completion-deepening.md)
- [`111-netapp-rated-life-offline-retention-telemetry-deepening.md`](111-netapp-rated-life-offline-retention-telemetry-deepening.md)
