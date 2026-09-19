# Case 101 evidence deepening — IBM 2001 / Seagate 2003 background-media-scan prior art

## Status

`bounded deepening complete`

## Question

Before T10 approved `04-198r5 — Background Medium Scan` in March 2005, what direct primary evidence already described proactive background media scanning, retained scan/error evidence, and repair/reallocation behavior?

This packet does not attempt a complete history of disk scrubbing, SCSI VERIFY, RAID patrol read, or drive firmware.

## Primary records

### IBM — US09/872,386 / US20020184580A1 / US6922801B2

- title: _Storage media scanner apparatus and method providing media predictive failure analysis and proactive media surface defect management_;
- inventors: John Edward Archibald, Jr.; Brian Dennis McKean;
- original assignee: International Business Machines Corporation;
- filed / priority: **1 June 2001**;
- published application: **5 December 2002**;
- grant: 26 July 2005;
- source: <https://patents.google.com/patent/US6922801B2/en>.

### Seagate — US10/740,886 / US20050188238A1 / US7490261B2

- title: _Background media scan for recovery of data errors_;
- inventors: Mark Gaertner; Xiaoying Li; David A. Anderson;
- assignee: Seagate Technology LLC;
- filed / priority: **18 December 2003**;
- published application: **25 August 2005**;
- grant: 10 February 2009;
- source: <https://patents.google.com/patent/US7490261B2/en>.

The IBM application was public by December 2002. The Seagate filing predates T10 approval as an engineering record, but its published application postdates the March 2005 standards vote. Filing, publication, grant, and shipment must not be collapsed.

T10 comparison sources:

- Gerry Houlder (Seagate), `04-198r5 — Background Medium Scan`, 9 March 2005: <https://www.t10.org/ftp/t10/document.04/04-198r5.pdf>
- T10 plenary minutes `05-097r0`, 10 March 2005: <https://www.t10.org/ftp/t10/document.05/05-097r0.htm>

---

## Historical record

### H/P — IBM publicly disclosed proactive background media scanning before T10 BMS

IBM's 2001-filed / 2002-published disclosure explicitly describes a background storage-media surface scanner for predictive media-failure analysis and proactive defect management. It seeks recoverable and unrecoverable read/write failures before normal host access reaches the affected region.

Bounded historical relation:

```text
background maintenance access
    -> media weakness discovered before demand
    -> defect evidence retained/reported
    -> optional reconstruction / reallocation
```

This independently supports T10 `04-198r5`'s later statement that proprietary and host-side scanning already existed. It does not establish earliest invention.

### H/P — the IBM mechanism can live at controller, RAID-controller, or host locus

The IBM text allows execution in an internal/external controller, an array controller in a RAID system, or another processor such as a host CPU.

Therefore:

```text
background media scanning
    != necessarily drive-internal scanning
```

A similar retention function can be placed at different system boundaries with different traffic, redundancy knowledge, and repair authority.

### H/P — IBM makes background admission workload-dependent

The disclosure says scanning can run as a background task and can begin when controller workload falls below a threshold. The threshold may be fixed, programmable, or dynamically adjusted.

Thus:

```text
maintenance obligation
    != immediate maintenance execution
```

The threshold is functionally comparable to later idle/background scheduling, but it is not silently renamed as T10's later BMS timing fields.

### H/P — IBM does not require one fixed full-medium traversal

The scanner may traverse all sectors, but may also scan selected portions, skip regions, or scan some regions more frequently than others.

This supplies an early primary counterexample to the assumption that proactive coverage implies one universal LBA-linear physical traversal.

### H/P — IBM retains maintenance metadata distinct from user payload

IBM describes sector-, sector-stripe-, and stripe-written indicators. These can be stored in reserved disk areas, extended-sector information, or controller nonvolatile memory. The scanner also tracks errors encountered and reallocations performed.

The relevant state classes are distinct:

```text
user payload
    != written/allocation metadata
    != scan schedule
    != defect evidence
    != repair history
```

The disclosure does not prove that every runtime scan position or error field survives every power-loss mode.

### H/P — IBM can expose weakness before ordinary reads fail

One embodiment reduces or disables ordinary drive error recovery during maintenance so that normally correctable errors become visible as early signs of media degradation. If a sector is unreadable in a RAID setting, the controller may reconstruct data from redundancy before replacing the defective location.

Therefore:

```text
ordinary read still recoverable
    != medium has no maintenance concern

maintenance-visible weakness
    != host-visible hard failure
```

### H/P — Seagate recorded a drive-side BGMS/pre-scan design by December 2003

Seagate's 18 December 2003 filing describes a disc-drive `background media scan (BGMS)` over LBAs without host intervention. The design scans for read errors, runs recovery actions, logs recovered/unrecovered errors, and gates execution on idle time and interval since the prior BGMS.

The first post-power-up scan is called a `pre-scan`. BGMS and pre-scan may be enabled or disabled by host control.

Because publication occurred in August 2005, this is evidence of pre-standardization engineering work, not evidence that the patent text was publicly available to T10 in 2003.

### H/P — incomplete pre-scan coverage changes write semantics

In the Seagate filing, a WRITE to an LBA range not yet covered by the power-up pre-scan is converted to WRITE AND VERIFY. After the full available LBA range is covered, pre-scan is disabled.

Bounded observation:

> a Seagate design record dated December 2003 already combines power-up pre-scan coverage with temporary write-and-verify semantics before T10's March 2005 approval.

Chronology alone does not prove one-to-one textual descent into the standard.

### H/P — Seagate separates traversal progress from error-log retention

The design tracks the current LBA scanned and exposes logged BGMS/pre-scan/write information through `LOG SENSE`; `LOG SELECT` can clear the log. The log has finite capacity and may wrap.

Therefore:

```text
current traversal frontier
    != retained error log

retained error log
    != complete lifetime history

log clear / overwrite
    != physical medium repair
```

This is a useful early example of maintenance evidence having its own retention and forgetting policy.

### H/P — T10 2005 is better read as standardization over an older mechanism family

T10 `04-198r5` explicitly says multiple vendors already had proprietary methods and customers wanted a standard control/status method. The IBM public disclosure confirms a pre-2005 controller/host-side mechanism floor; the Seagate filing confirms a pre-approval drive-side BGMS/pre-scan design record.

Conservative relation:

```text
pre-existing proactive-scan mechanisms
    -> later interoperable control/status standardization
```

This is not proof of IBM→Seagate or patent→T10 clause genealogy.

---

## Engineering reconstruction

The new evidence sharpens four independent dimensions.

1. **Maintenance locus:** host/software, controller/RAID-controller, or drive-internal.
2. **Maintenance evidence:** traversal progress, written-region metadata, recovered/unrecovered errors, counts, and repair records are different retained objects.
3. **Maintenance scope:** all sectors, selected regions, metadata-conditioned regions, and not-yet-pre-scanned regions need not have the same coverage semantics.
4. **Repair authority:** observing a bad sector, recovering it with drive ECC, reconstructing from RAID redundancy, and reallocating a sector are distinct operations.

Useful boundaries:

```text
verification coverage
    != repair authority
    != repair completion

maintenance enabled
    != every address recently qualified

controller-side scan
    != device-side BMS
```

---

## Functional comparison — not genealogy

### IBM 2001/2002 vs T10 2005

Shared broad function: pre-demand media exercise, error discovery, maintenance evidence, optional relocation.

Different documented locus: IBM explicitly permits controller/host implementations; T10 standardizes device-server BMS controls/status.

> **functional prior art != identical interface architecture.**

### Seagate 2003 filing vs T10 2005

Shared vocabulary/functions include BGMS/background scanning, pre-scan, idle scheduling, error logging, host control, and write-and-verify while pre-scan coverage is incomplete.

> **pre-standardization Seagate design record != demonstrated one-to-one source for the later standard.**

### IBM controller scan vs Dell/LSI Patrol Read

IBM supplies an earlier generic controller/RAID-controller proactive scan mechanism floor than the currently inspected April 2005 named PERC `Patrol Read` documentation.

> **earlier controller-level scan mechanism != earlier `Patrol Read` terminology.**

---

## Philosophical interpretation — bounded

These records strengthen only a narrow claim: a system may retain user data while separately maintaining evidence about whether the current embodiment remains trustworthy enough for future retrieval.

Verification can create evidence without relocating data; repair can later depend on that evidence. Therefore:

```text
verification
    != repair
```

The records do not justify a general claim that unscanned data cease to exist or that observation itself constitutes storage.

---

## Explicit non-claims

This packet does not claim that:

1. IBM invented disk scrubbing in 2001;
2. IBM invented `Patrol Read`;
3. IBM's patent embodiments shipped as described;
4. IBM directly influenced T10 `04-198r5`;
5. Seagate invented background media scanning;
6. the 2003 Seagate filing was public in 2003;
7. the Seagate patent and T10 proposal are identical;
8. acronym similarity proves genealogy;
9. T10 BMS and Dell/LSI Patrol Read share one implementation lineage;
10. a successful scan is a permanent integrity certificate;
11. retained error evidence proves remediation;
12. clearing an error log erases old media embodiments;
13. controller NVRAM necessarily retains an exact scan frontier;
14. patent priority date equals publication date;
15. patent publication equals product shipment;
16. patent grant equals first implementation;
17. absence of an earlier inspected document proves absence of earlier practice.

---

## Claim ledger

| Claim | Type | Strength | Boundary |
|---|---|---|---|
| IBM filed 2001-06-01 and published 2002-12-05 | historical record | high | filing/publication distinct |
| IBM directly described controller-side background media scanning before host demand | historical record | high | patent disclosure, not shipment proof |
| IBM allowed controller/RAID/host loci and workload-gated execution | historical record | high | not equated with T10 fields |
| Seagate filed a drive-side BGMS/pre-scan design on 2003-12-18 | historical record | high | public only in 2005 |
| Seagate linked incomplete pre-scan coverage to WRITE AND VERIFY | historical record | high | not clause-genealogy proof |
| public proactive-scan prior art predates T10 approval | historical synthesis | high via IBM publication | not earliest-ever claim |
| locus/evidence/scope/repair authority are separate dimensions | engineering reconstruction | strong | project ontology |
| cross-source similarity is functional, not genealogical | functional comparison | strong | explicit non-genealogy |

---

## Remaining debt

Still open:

- earlier host-initiated SCSI VERIFY sweep history;
- pre-2001 controller/vendor implementation records;
- named IBM product/firmware evidence practicing this patent family;
- Seagate product/release evidence between the December 2003 filing and T10 standardization;
- direct T10 contribution/prosecution evidence proving or refuting patent→standard genealogy;
- pre-April-2005 PERC/LSI firmware chronology;
- independent vendors' `Patrol Read` terminology history;
- fault injection and lower-layer persistence after repair/reassignment.

A repository search found no dedicated `US6922801` packet in `tmzncty/computing-archaeology` during this slice. Broader IBM/Seagate product history, SCSI VERIFY genealogy, patent lineage, and vendor competition belong there if developed later.

## Result

**Bounded deepening complete.** Case 101 now has direct earlier primary evidence rather than relying only on T10's retrospective statement that proprietary/host scanning existed: a publicly published IBM controller-level scanner by **5 December 2002**, plus a Seagate **18 December 2003** filing already describing drive-side BGMS, power-up pre-scan, idle scheduling, error logs, and write-and-verify for uncovered LBAs. The result preserves `standardization != invention`, `functional similarity != genealogy`, `filing != publication != shipment`, and `verification != repair`.