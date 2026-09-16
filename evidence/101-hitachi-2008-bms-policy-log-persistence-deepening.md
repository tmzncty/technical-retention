# Evidence 101 deepening — Hitachi 2008 BMS policy persistence and log-state horizons

**Canonical case:** [`../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md`](../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md)

**Bounded question:** by the late 2000s, did a named SAS drive expose one undifferentiated `BMS state`, or did it already separate persistent maintenance policy, current traversal/progress, cumulative history, defect-event evidence, and later repair authority across reset/power boundaries?

**Status:** `bounded deepening complete` for the named Hitachi Ultrastar 15K450 SAS product contract and the contemporaneous T10 log-save semantics inspected here. This is a deepening of Case 101, **not a new BMS case** and not a general history of SCSI mode/log persistence.

---

## Source ledger

### S1 — Hitachi Global Storage Technologies, *Ultrastar 15K450 (SAS) Hard Disk Drive Specification*, Version 1.2

- **Date:** 29 October 2008.
- **Models named on title page:** HUS154545VLS300 and HUS154530VLS300.
- **Manufacturer:** Hitachi Global Storage Technologies.
- **Current archive URL:** <https://documents.westerndigital.com/content/dam/doc-library/en_us/assets/public/western-digital/product/data-center-drives/ultrastar-sas-series/product-manual-ultrastar-15k450-sas.pdf>
- **Evidence class:** `H/P` — first-party named-product specification preserved in Western Digital's document archive.
- **Primary locations inspected:** title/front matter; §18.7.11 `Log Sense Page 15`; §18.8 `MODE SELECT (15)`; §18.10 `MODE SENSE (1A)`; §18.10.15.1 `Background Control (Subpage 01h)`.

The title page identifies `Version 1.2 29 October 2008`, and the copyright/front matter identifies Hitachi Global Storage Technologies. The specification directly exposes BMS status/progress, BMS result entries, the Background Control mode subpage, MODE SELECT save behavior, and post-reset/power-up restoration of saved mode parameters.

### S2 — T10/05-242r2, *SPC-4, Combinations of bits and fields in the LOG SELECT CDB and log parameters*

- **Date on document:** revision text carries August/November 2005 editing dates.
- **Organization:** INCITS T10; author Mark Evans, Maxtor Corporation.
- **URL:** <https://www.t10.org/ftp/t10/document.05/05-242r2.pdf>
- **Evidence class:** `H/P` — contemporaneous standards-development proposal, not a claim that this proposal text alone is the final published SPC-4 wording.

This proposal is useful because it states the period meaning of `DS`, `TSD`, `SP`, volatile interim log updates, and save-to-nonvolatile behavior explicitly. T10's SPC-4 project page independently dates Revision 03 to 19 January 2006, but this evidence file does not pretend that inspecting the project ledger is equivalent to line-by-line inspection of every later normative revision.

### S3 — existing Case 101 grounding and later product deepening

- [`101-t10-2004-2007-background-medium-scan-grounding.md`](101-t10-2004-2007-background-medium-scan-grounding.md)
- [`101-wd-2024-bms-progress-repair-policy-deepening.md`](101-wd-2024-bms-progress-repair-policy-deepening.md)

These are comparison anchors only. The existing canonical record already establishes the 2004–2006 T10 BMS standardization path and a 2007 Seagate implementation. The 2024 Western Digital HC590 record already distinguishes current progress, lifetime counts, defect entries, and no in-scan reassignment, but deliberately left power/reset persistence as an open documentation question.

---

## Historical / product findings

### H1 — by October 2008, a named Hitachi SAS drive made the BMS control regime a saveable mode-page state

Hitachi's §18.10.15.1 exposes Background Control Subpage `01h`. The table contains:

- `EN_BMS`;
- `EN_PS`;
- `S_L_FULL`;
- `LOWIR`;
- Background Medium Scan Interval Time;
- Background Pre-Scan Time Limit;
- Minimum Idle Time Before Background Scan;
- Maximum Time To Suspend Background Scan.

The first byte of the subpage identifies the `PS` bit and has default byte `DCh`; with `PS` in bit 7, the page reports itself as saveable.

That matters because the same product's MODE SELECT contract explicitly distinguishes two persistence horizons:

```text
SP = 0
    -> use selected mode-page values
    -> only until power removal / reset / later MODE SELECT

SP = 1
    -> save selected values in the disk reserved area
    -> maintain them across power cycle or reset
```

This is direct product documentation, not an inference from the word `mode`.

### H2 — saved mode-page state is reconstituted after power-up rather than being identical to the first instantaneous power-up state

The MODE SENSE section gives an unusually explicit transition sequence. Immediately after power-up and before media access, defaults are current. Once the media can be accessed, saved values are read from the Reserved Area and become current. It also says current values take on the saved values after reset if the parameters were saved.

Therefore the product contract supports a three-stage distinction:

```text
persistent representation exists in reserved area
    !=
values are already current at the first instant of power-up
    !=
post-startup control regime has been reconstituted from saved state
```

The disk need not treat `persistent configuration` and `currently active configuration` as one physical state at every instant.

### H3 — a persisted maintenance policy can encode a future maintenance obligation rather than evidence that maintenance has already occurred

`EN_PS=1` does not mean a pre-scan has already completed. The Background Control text says that enabling `EN_PS` causes pre-scan to start **after the next power-on cycle**. Once that pre-scan completes, another pre-scan does not occur until `EN_PS` is toggled off/on and another power-on cycle occurs.

So the named product directly supports:

```text
persistent maintenance policy
    !=
maintenance execution
    !=
maintenance completion
```

and more specifically:

```text
retained EN_PS policy across shutdown
    -> future power-on-triggered pre-scan
```

This is a retained control relation whose operational effect is intentionally deferred into a later boot/power episode.

### H4 — disabling BMS during an execution preserves a resumable traversal relation, but the manual does not by that sentence alone make the suspended location power-loss durable

The Background Control text says that changing `EN_BMS` from one to zero during a scan suspends the scan; setting it to one again causes the scan to resume from the suspended location.

That is direct evidence for:

`execution active != execution suspended != traversal obligation retired`

But the clause does **not** state that the exact suspended LBA survives an unexpected power loss. Mode-page persistence tells us that control policy can be saved; it does not automatically prove that an implementation's latest traversal checkpoint is written atomically with every progress change.

### H5 — the BMS result page already separated current progress, lifetime summary, and per-error event evidence in 2008

Hitachi's Log Sense Page 15 exposes:

- a `BMS Status` parameter;
- `Number of Scans Performed`, explicitly over the life of the drive;
- `Medium Scan Progress`, expressed as a fraction over 65,536;
- one or more Medium Scan Parameters containing power-on minutes at error detection, error status/codes, and physical/logical location information.

The product therefore already exposes plural maintenance-state horizons:

```text
current execution state
    !=
current traversal progress
    !=
lifetime maintenance-count summary
    !=
individual defect-event evidence
```

A lifetime count remains only a summary. It does not become a complete per-LBA verification chronology.

### H6 — BMS status and medium-scan event parameters advertise `DS=0` and `TSD=0`, but those bits do not justify an exact crash-checkpoint claim

For both the BMS Status Parameter and Medium Scan Parameter, the 2008 product manual reports `DS=0` and `TSD=0`; both use list-style format/linking values rather than being ordinary scalar user payload.

The contemporaneous T10 `05-242r2` text states:

- `DS=0` means the logical unit supports saving that log parameter when the relevant LOG SELECT/LOG SENSE save mechanism is invoked;
- `TSD=0` means the logical unit has a target-defined implicit saving method at vendor-specific intervals;
- cumulative parameter values may be held in volatile memory between save events and may therefore lose the newest updates on a power cycle;
- the stated implicit-save objective is preserving statistical significance across power cycles, not guaranteeing that every most-recent update is an atomic crash-consistent checkpoint.

The safe reconstruction is therefore:

```text
save-capable log parameter
    !=
parameter definitely saved after every update

implicit periodic save
    !=
latest progress position guaranteed power-fail durable

cross-power statistical continuity
    !=
exact crash-consistent traversal checkpoint
```

Because the BMS structures here are list-style parameters, the cumulative-counter language in the T10 proposal should not be overextended into a stronger per-event or per-progress atomicity guarantee than the source states.

### H7 — Hitachi 2008 independently blocks a universal `BMS = automatic in-scan reassignment` reading

The Hitachi product manual states directly: `Reassignment during the background scan is not supported.` Its Medium Scan result instead exposes a state where reassignment is pending an initiator `REASSIGN` or later write.

This is important because the canonical Case 101's 2007 Seagate witness permits logging or reallocation according to `ARRE/AWRE`, whereas this 2008 Hitachi witness supports BMS while declining reassignment *during* BMS.

Thus, by 2008 there is already cross-vendor product evidence for:

```text
standardized BMS control/status family
    !=
identical automatic-repair policy
```

This does not establish a chronological industry trend from one policy to another. It establishes implementation-policy plurality under broadly comparable SCSI BMS vocabulary.

### H8 — the 2008 Hitachi witness changes how the 2024 Western Digital evidence should be weighted

The later Western Digital HC590 record also says that reassignment during BMS is not supported and exposes a very similar status/progress/result shape.

The 2008 Hitachi document is historically independent of the 2007 Seagate product witness, but it should not be naively counted as an entirely unrelated engineering lineage from later HGST/Western Digital products. Western Digital later acquired HGST, and the present official archive itself hosts the old Hitachi specification.

The bounded provenance rule is:

```text
2008 Hitachi product witness
    !=
2007 Seagate product lineage

2008 Hitachi + 2024 Western Digital documents
    !=
two automatically independent long-run engineering lineages
```

Corporate/document chronology can establish separate publication events without proving independent firmware ancestry.

---

## Engineering reconstruction

The evidence supports decomposing the named product's maintenance state into at least six relations.

### 1. Medium payload / physical readability

The user block is what future reads must still recover. BMS control metadata is not the payload.

### 2. Persistent maintenance policy

Saveable Background Control parameters determine whether BMS/pre-scan is enabled and how it is scheduled. With MODE SELECT `SP=1`, those policy values can cross reset/power boundaries via the drive's Reserved Area.

### 3. Reconstituted current policy

After startup reaches media access, saved values are read and become current. Persistent representation and active runtime configuration are related but distinct states.

### 4. Traversal/execution state

BMS may be active, suspended, halted, or inactive, and has a current percentage progress relation.

### 5. Cumulative maintenance summary

`Number of Scans Performed` records a lifetime total. It is not a map of verification age for every sector.

### 6. Defect-event evidence and repair status

Medium Scan Parameters retain evidence about detected errors and whether later action is pending. Detection does not itself equal reassignment.

The resulting model is:

```text
persistent BMS policy
        ↓ power-up reconstitution
current BMS policy
        ↓ scheduling / idle opportunity
scan execution + progress
        ↓ observation
result / defect evidence
        ↓ separate repair authority
rewrite / REASSIGN / later write
```

No arrow in this diagram should be read as automatic identity.

---

## Functional comparison

### Case 101 — 2007 Seagate BMS

The Seagate witness remains the earlier named product grounding for standardized device-side BMS. Hitachi 2008 adds a different repair policy and explicit mode/log persistence detail.

This is a functional/product-contract comparison, **not** evidence that Hitachi copied Seagate or that both used the same internal firmware architecture.

### Case 101 — 2024 Western Digital HC590

The HC590 later exposes current progress, lifetime scan counts, event records, and no in-scan reassignment. Hitachi 2008 shows that much of that product-visible decomposition existed at least sixteen years earlier in the Hitachi/HGST lineage.

The new historical conclusion is not `the 2024 behavior was unchanged internally since 2008`; only the documented interface relation is continuous enough to compare.

### Cases 18 / 83 — ZFS and HDFS scrub/scanner

A saved BMS policy or drive-local defect log cannot substitute for higher-layer checksum/currentness evidence. The abstraction level and validation target differ.

---

## Philosophical limit

This slice adds one narrow interpretive point: **a system can retain a maintenance intention or regime across a period in which the maintenance act itself is not occurring**.

That is useful for `technical-retention` because it separates retention of an operational obligation from retention of the protected payload and from retention of a complete history of maintenance acts.

It does **not** make a saved mode page an archive, a narrative memory, or a complete trace of what happened to the disk.

---

## Stop conditions / explicit non-claims

Do **not** infer from this evidence that:

- Hitachi invented BMS, pre-scan, SCSI mode-page persistence, or log-page persistence;
- all 2008 SAS drives implemented BMS like the Ultrastar 15K450;
- `PS=1` on Background Control proves every internal BMS runtime variable is stored in the same Reserved Area representation;
- the exact suspended LBA is atomically persisted after every movement of the scan head;
- `DS=0` means a parameter is currently saved at all times;
- `TSD=0` means zero recent updates can be lost on sudden power failure;
- statistical significance across power cycles means exact replay or crash consistency;
- a lifetime scan count is a per-sector verification history;
- BMS completion is a timeless integrity certificate;
- no in-scan reassignment means the drive cannot reassign on later write, explicit REASSIGN, or another path;
- Hitachi 2008 and Western Digital 2024 are two cleanly independent engineering lineages merely because the documents have different corporate mastheads;
- BMS log clearing securely erases the physical medium;
- drive-local BMS proves end-to-end filesystem or application integrity.

---

## Related-repository boundary

A fresh search of `tmzncty/computing-archaeology` for `C15K600` and `Background Media Scan` returned no dedicated study. The broader Hitachi/HGST/Western Digital firmware lineage, complete SPC mode/log genealogy, disk-controller implementation history, and fault-injection work should live there if developed. This file keeps only the bounded retention question: **which maintenance-control/evidence relations can outlive one execution burst or power episode, and what does that still not prove?**

---

## Remaining debt

- perform named-drive reset/power-loss experiments to determine whether the latest BMS traversal location is checkpointed, how often, and under which reset classes;
- inspect a final SPC-4 revision around the 2008 product date line-by-line for the exact normative DS/TSD/list-parameter semantics rather than relying only on the contemporaneous `05-242r2` proposal plus product behavior;
- test whether LOG SENSE/LOG SELECT save operations actually preserve each BMS list entry on a real 15K450 and what happens when the log is full;
- trace Hitachi 15K450 → later HGST → Western Digital BMS firmware/interface continuity only in `computing-archaeology`, unless a retention-specific contract change appears;
- compare another genuinely independent later SAS vendor rather than counting corporate-document multiplicity as implementation independence.