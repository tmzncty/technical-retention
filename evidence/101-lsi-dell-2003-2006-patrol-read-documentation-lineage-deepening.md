# Case 101 deepening — LSI/Dell 2003–2006 Patrol Read documentation chronology and source-lineage boundary

- **Status:** `bounded deepening complete`
- **Canonical case:** [`../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md`](../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md)
- **Slice:** public MegaRAID / PERC controller documentation from February 2003 through March 2006, focused on when `Patrol Read` becomes visible in the inspected documentation and on how Dell/LSI source lineage should be weighted.
- **Question:** how far can the public documentation floor for controller-level Patrol Read be moved earlier, and when do two corporate mastheads represent independent engineering evidence versus documentation from one controller ecosystem?

This slice does **not** establish invention priority, first firmware implementation, first shipment, or a T10 Background Medium Scan → MegaRAID Patrol Read genealogy. It also does not attempt a general LSI/MegaRAID history.

---

## 1. Why this slice was selected

Case 101 already grounds T10 device-side Background Medium Scan and a Dell PERC controller-level Patrol Read witness. Its remaining work explicitly leaves open:

- pre-June-2005 Dell/LSI Patrol Read chronology;
- LSI/MegaRAID material independent of Dell branding;
- cross-vendor terminology and genealogy;
- evidence for or against treating T10 BMS and controller Patrol Read as one lineage.

The existing Dell slice used the 7 June 2005 MegaPR utility release as the earliest named-controller public witness. The new material improves that boundary in two directions:

1. a Dell PERC 4/Di/Si and 4e/Di/Si user guide dated **April 2005** already documents Patrol Read mode/status/control;
2. LSI's generic MegaRAID Configuration Software User's Guide Version 2.0 documents Patrol Read by its 2006 edition, but period Dell records explicitly identify the relevant PERC family with LSI Logic / MegaRAID branding, so Dell and LSI should not be counted naively as two independent engineering witnesses.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated `Patrol Read` history to reuse. Broader controller genealogy still belongs primarily there.

---

## 2. Source chronology and evidence quality

### 2.1 February 2003 — LSI MegaRAID Configuration Software User's Guide Version 1.0 — mirrored period manual

The inspected First Edition is:

- LSI Logic, **MegaRAID Configuration Software User's Guide**, DB15-000269-00, Version 1.0 / First Edition, February 2003.
- Surviving page-preserving PDF mirror: <https://www.manuallib.com/download/pdf0/LSILOGIC-MEGARAID-CONFIGURATION-SOFTWARE-USER-GUIDE.PDF>

The document's title/front matter identifies it as LSI Logic's official reference for MegaRAID software tools and utilities. The inspected searchable copy contains explicit `Check Consistency` menu and operation descriptions, including verification of RAID redundancy data and automatic parity correction where differences are found.

A full-text search of this inspected 116-page copy returns **no match for `Patrol Read`**.

Because this copy is obtained from a third-party mirror rather than the current Broadcom archive, the negative claim is deliberately weak:

> **The inspected February 2003 Version 1.0 documentation does not expose the term/control surface `Patrol Read`.**

It does **not** establish:

- that no MegaRAID firmware in 2003 had an equivalent internal function;
- that Patrol Read was invented after February 2003;
- that every 2003-era MegaRAID product had the same feature set;
- that absence from one manual proves absence from every contemporaneous manual or firmware branch.

The 2003 document is useful chiefly as a documentation baseline because it already exposes a separate `Check Consistency` operation while the inspected text does not expose `Patrol Read`.

### 2.2 April 2005 — Dell PERC 4/Di/Si and 4e/Di/Si User's Guide — earlier named-controller public witness

A surviving copy of Dell's **PowerEdge Expandable RAID Controller 4/Di/Si and 4e/Di/Si User's Guide** identifies:

- models `PERC 4/Di/Si` and `PERC 4e/Di/Si`;
- **Release: April 2005**;
- Dell copyright 2003–2005;
- `MegaRAID` as a registered trademark of **LSI Logic Corporation**.

Surviving page-preserving web copy:

- <https://dell.manymanuals.com/computer-hardware/perc-4-si/user-manual-31973>

The manual's contents and configuration sections explicitly include `Patrol Read`. The controller BIOS exposes:

- `Patrol Read Mode`;
- `Patrol Read Status`;
- `Patrol Read Control`;
- `Manual`;
- `Auto`;
- `Manual Halt`;
- `Disabled`.

The status surface reports at least the number of completed iterations, whether the operation is active/stopped, and the next execution schedule. The guide separately contains `Consistency Check` and Patrol Read sections.

This moves the bounded public-document floor for the already-known Dell PERC controller witness from **7 June 2005** to **April 2005**.

It does **not** establish first firmware availability, first shipment, invention date, or the date at which every PERC 3/4 controller gained the feature.

### 2.3 7 June 2005 — Dell MegaPR for Linux A02 — utility release, not feature-origin date

Dell's still-live support record is:

- **LSI Logic PERC3/DCL, PERC3/DC, PERC3/QC, PERC3/SC, PERC 4/Di, PERC 4/SC, PERC 4/DC, PERC 4e/DC, PERC 4e/Di, PERC 4e/Si, v.1.03, A02**;
- release date **7 June 2005**;
- category `SCSI RAID`;
- MegaPR for Linux described as a utility that starts/stops Patrol Read and displays current Patrol Read status.

Source:

- <https://www.dell.com/support/home/en-us/drivers/driversdetails?driverid=nfpxp>

The record labels this package `Initial Release of MegaPR for Linux`, but its own prerequisites show why that phrase must not be converted into `initial release of Patrol Read`:

- MegaPR requires a minimum controller firmware level;
- Patrol Read mode must already be `Auto` or `Manual` for MegaPR to start/stop an iteration;
- the mode itself is changed through the PERC BIOS configuration utility (`CTRL+M` → Adapter → Patrol Read Options).

Thus:

```text
initial release of host utility
    !=
initial firmware implementation of Patrol Read
```

The same Dell page's title explicitly prefixes the named PERC controller list with **`LSI Logic`**, which is source-lineage evidence relevant below.

### 2.4 February/March 2006 — LSI MegaRAID Configuration Software User's Guide Version 2.0 — generic MegaRAID witness

The current Broadcom archive exposes:

- LSI Logic, **MegaRAID Configuration Software User's Guide**, DB15-000269-01, Version 2.0;
- current archive URL: <https://docs.broadcom.com/doc/12353347>.

The surviving PDF has two adjacent date signals that should not be silently collapsed:

- its revision-history table gives **Version 2.0 — February 2006**;
- its front matter identifies **Second Edition (March 2006)** and the title page says March 2006.

For this slice, the safe wording is therefore `the February/March 2006 Version 2.0 / Second Edition`, rather than pretending the two document dates are identical.

Its revision history also records:

- DB15-000269-00 — Version 1.0 — February 2003 — `Initial release of document`;
- DB15-000269-01 — Version 2.0 — February 2006 — multiple revisions including BIOS menu changes.

The Version 2.0 manual contains a dedicated §2.4.7 `Patrol Read`. It says Patrol Read reviews the system for possible hard-drive errors that may lead to drive failure, with corrective action depending on array configuration and error type. It exposes `Manual`, `Auto`, `Manual Halt`, and `Disable`; Auto causes firmware to initiate Patrol Read on a scheduled basis.

The status surface reports:

- number of completed iterations;
- current state, active/stopped;
- schedule for the next execution.

A later BIOS-menu description in the same manual says Auto mode runs continuously and schedules a new Patrol Read within four hours after the last iteration completes.

The manual separately defines `Consistency Check` as verification of RAID redundancy correctness for supported RAID levels. Therefore, within generic LSI documentation itself:

```text
Patrol Read
    !=
Consistency Check
```

This is not only a Dell marketing distinction.

---

## 3. Historical record

### H/P* — the inspected 2003 LSI manual exposes Consistency Check but not Patrol Read

The First Edition contains `Check Consistency` in the BIOS/WebBIOS/MegaRAID Manager control surfaces and gives it explicit RAID-redundancy semantics. No `Patrol Read` text match was found in the inspected searchable copy.

The correct historical statement is documentation-specific:

> **In the inspected February 2003 Version 1.0 manual, Consistency Check is documented while Patrol Read is not.**

This is a negative-document witness, not proof of feature nonexistence.

### H/P* — April 2005 Dell documentation moves the named-controller public floor earlier than MegaPR

The April 2005 PERC 4/Di/Si / 4e/Di/Si guide exposes Patrol Read configuration and status before Dell's June 2005 MegaPR Linux release record.

Therefore the earlier Case 101 phrasing can be tightened from:

```text
named Dell PERC Patrol Read public by 7 June 2005
```

to:

```text
named Dell PERC 4/Di/Si family Patrol Read documented by April 2005
MegaPR Linux host-control utility publicly released 7 June 2005
```

The two dates refer to different artifacts and should remain separate.

### H/P — the June 2005 Dell utility record presupposes controller firmware support

MegaPR's minimum-firmware requirement and BIOS-mode prerequisite show that the utility is layered above an existing controller feature.

Thus the utility release is strong evidence of a public control surface, but weak evidence for the controller feature's origin date.

### H/P — generic LSI documentation exposes the same Patrol Read control vocabulary by early 2006

The LSI Version 2.0 manual documents `Patrol Read Mode`, `Status`, and `Control` with Manual/Auto/Manual Halt/Disable semantics. It also separately documents `Consistency Check`.

This closes one bounded debt in Case 101: **period LSI/MegaRAID material independent of a Dell-authored manual is now available.**

But this does not make LSI and Dell independent engineering lineages.

### H/P — Dell and LSI documentation are lineage-related evidence, not two clean independent vendor witnesses

The April 2005 Dell manual explicitly identifies `MegaRAID` as an LSI Logic trademark. Dell's official June 2005 utility record titles the supported family as `LSI Logic PERC3/... PERC 4/...`.

LSI's own manual says its MegaRAID tools apply to systems using MegaRAID controllers, including controllers designed into systems by other manufacturers.

Together these records justify a bounded provenance statement:

> **The Dell PERC Patrol Read witness and the LSI MegaRAID Patrol Read witness belong to an overlapping controller/documentation ecosystem and should not be counted mechanically as two independent corporate confirmations of the mechanism.**

This is stronger than merely noticing that two manuals use the same words, but weaker than claiming:

- every PERC model uses firmware identical to one retail LSI MegaRAID adapter;
- Dell merely copied LSI documentation;
- all Patrol Read implementation details are shared;
- LSI invented the feature.

The source-lineage conclusion is about evidence weighting, not undocumented binary identity.

---

## 4. Engineering reconstruction

The following are project reconstructions from the documented behavior, not historical vocabulary of Dell or LSI.

### E/R — documentation appearance, software release, firmware availability, and invention are different dates

At least four chronological layers must be kept separate:

```text
feature conception / invention
    !=
firmware implementation
    !=
product documentation
    !=
host-management utility release
```

The inspected sources currently establish public documentation by April 2005 for a named Dell PERC family and a Linux host utility release on 7 June 2005. They do not close the first two layers.

### E/R — a copyright range is not a clause date

The 2006 LSI manual repeatedly prints `Copyright © 2003–2006`. Its own revision history, however, distinguishes the 2003 Version 1.0 from the 2006 Version 2.0, while the inspected 2003 manual has no Patrol Read match.

Therefore:

```text
copyright 2003–2006 on Version 2.0
    !=
Patrol Read documented in 2003
```

This is an important date-hygiene rule for reused vendor manuals.

### E/R — a second corporate masthead is not automatically an independent engineering witness

Evidence independence depends on provenance, not URL count or company-name count.

Here, Dell's own records expose LSI Logic / MegaRAID lineage around the relevant PERC families. Therefore a cross-source claim should distinguish:

1. **document independence** — two separately published artifacts can corroborate wording/behavior;
2. **organizational masthead independence** — Dell and LSI are distinct companies;
3. **engineering-lineage independence** — not demonstrated here and in fact partially undercut by the documented PERC/LSI relationship.

Thus:

```text
second publisher
    !=
independent implementation lineage
```

### E/R — Patrol Read recurrence state is not an exact verification ledger

The LSI manual exposes number of completed iterations, active/stopped state, and next-execution schedule. Auto mode schedules another pass after the prior iteration completes.

Those fields describe recurrence and coarse execution status. They do not prove a persistent per-LBA verification history or a power-loss-persistent exact scan frontier.

```text
iteration count + schedule
    !=
per-block verification certificate
```

The existing Dell deepening remains the stronger witness for the distinction between NVRAM-held maintenance summary/policy and an exact in-flight restart checkpoint.

### E/R — completion-relative scheduling is a different clock from fixed wall-clock scheduling

The LSI Version 2.0 BIOS description says a new Auto Patrol Read is scheduled within four hours **after the last iteration is completed**.

That creates a completion-relative recurrence clock:

```text
next due time
    =
prior completion time + bounded delay
```

It should not be silently rewritten as `runs every four hours`, because one iteration's duration can vary and the source does not define a fixed four-hour start-to-start period.

---

## 5. Functional comparisons

### 5.1 T10 Background Medium Scan

Case 101's T10 BMS evidence remains device-side. Dell/LSI Patrol Read is controller-orchestrated array maintenance.

The new chronology does not establish historical descent between them.

```text
device-side BMS
    ~= functional proactive medium verification
controller Patrol Read

but

functional similarity
    !=
T10 → LSI/Dell genealogy
```

### 5.2 Dell versus LSI

This is a provenance comparison, not a technology comparison.

Dell and LSI documents can be used to corroborate the existence and exposed semantics of Patrol Read. They should not be multiplied into two independent implementation families merely because the documents have different publishers.

### 5.3 Case 111 IBM/Lenovo source-lineage lesson

Case 111 separately shows that a second corporate masthead can inherit or republish closely related operational guidance. Case 101 now supplies a different storage-controller example of the same **methodological** warning:

> **source multiplicity ≠ engineering-lineage multiplicity.**

This is a functional/methodological analogy only. It does not assert any IBM/Lenovo ↔ Dell/LSI historical connection.

---

## 6. Philosophical interpretation — bounded

Case 101 already treats proactive verification as a form of epistemic maintenance: the medium may remain physically present while justified confidence in future readability becomes stale until a scan exercises it.

This slice adds a narrower historiographic counterpart. What survives in documentation is also not self-authenticating evidence of independent origins. Provenance relations determine how many genuinely independent witnesses a historian has.

That observation should remain methodological. It does **not** turn vendor-document genealogy into a philosophical theory of storage, and it does not change the physical mechanism of Patrol Read.

---

## 7. Negative controls

This slice does **not** support any of the following claims:

- `LSI invented Patrol Read`;
- `Dell invented Patrol Read`;
- `Patrol Read first appeared in April 2005`;
- `Patrol Read did not exist in firmware in 2003`;
- `the 2003 manual proves a universal absence across all MegaRAID products`;
- `copyright 2003–2006 proves Patrol Read existed in 2003`;
- `MegaPR initial release = Patrol Read initial release`;
- `Dell PERC firmware is bit-for-bit identical to generic LSI MegaRAID firmware`;
- `Dell + LSI = two fully independent engineering witnesses`;
- `T10 BMS directly caused or standardized PERC/MegaRAID Patrol Read`;
- `Patrol Read = Consistency Check`;
- `iteration completed = every block permanently certified readable`.

---

## 8. What this slice closes

This bounded deepening closes four narrow debts:

1. moves the named Dell PERC public-document Patrol Read floor from June 2005 to **April 2005**;
2. adds a **generic LSI MegaRAID** Patrol Read witness by the February/March 2006 Version 2.0 documentation;
3. adds a 2003 documentation baseline in which `Check Consistency` is visible but `Patrol Read` is not found, without turning absence into an implementation claim;
4. records a source-lineage rule: Dell and LSI Patrol Read documents are overlapping ecosystem evidence and should not be counted as cleanly independent vendor implementations.

---

## 9. Remaining work

Still open after this slice:

- earlier-than-April-2005 Patrol Read firmware, manuals, release notes, or controller shipment evidence;
- exact LSI/Dell engineering and firmware lineage for individual PERC 3/4 versus MegaRAID controller models;
- archived LSI release notes that might date the first Patrol Read-capable firmware more precisely;
- IBM ServeRAID and genuinely independent controller-vendor period evidence;
- host-initiated SCSI VERIFY scrub history before controller/device autonomous scanning;
- direct evidence for or against a T10 BMS → controller Patrol Read genealogy;
- terminology migration: when `patrol read` becomes generic across vendors rather than one controller-family term;
- exact restart/persistence semantics of early LSI Patrol Read across power loss and firmware update;
- field validation on period hardware.

These do not block the bounded result.

---

## 10. Related repositories

### `tmzncty/computing-archaeology`

No dedicated `Patrol Read` entry was found in a fresh repository search. The broader historical engineering genealogy — LSI/MegaRAID model families, PERC OEM lineage, ServeRAID, firmware chronology, and SCSI VERIFY ancestry — should be developed there if pursued. `technical-retention` should retain only the provenance-sensitive maintenance relations needed for Case 101.

### `tmzncty/problem-history`

The anti-anachronism rule applies both to technology and sources. `readability qualification`, `maintenance evidence`, `source-lineage independence`, and `documentation floor` are project terms. Dell/LSI historical vocabulary includes `Patrol Read`, `Patrol Read Mode`, `Patrol Read Status`, `Patrol Read Control`, `Manual`, `Auto`, `Manual Halt`, `Disable`, `Consistency Check`, and `MegaPR`.

---

## 11. Sources

### Primary / period vendor documentation

- LSI Logic, **MegaRAID Configuration Software User's Guide**, DB15-000269-00, Version 1.0 / First Edition, February 2003. Surviving searchable PDF mirror: <https://www.manuallib.com/download/pdf0/LSILOGIC-MEGARAID-CONFIGURATION-SOFTWARE-USER-GUIDE.PDF>
- Dell, **PowerEdge Expandable RAID Controller 4/Di/Si and 4e/Di/Si User's Guide**, Release April 2005, Rev. A07. Surviving page-preserving copy: <https://dell.manymanuals.com/computer-hardware/perc-4-si/user-manual-31973>
- Dell, **MegaPR for Linux v.1.03, A02**, release date 7 June 2005: <https://www.dell.com/support/home/en-us/drivers/driversdetails?driverid=nfpxp>
- LSI Logic, **MegaRAID Configuration Software User's Guide**, DB15-000269-01, Version 2.0 / Second Edition, February/March 2006. Current Broadcom archive: <https://docs.broadcom.com/doc/12353347>

### Internal comparisons

- [`../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md`](../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md)
- [`101-dell-2005-2006-perc-patrol-read-controller-deepening.md`](101-dell-2005-2006-perc-patrol-read-controller-deepening.md)
- [`../cases/111-enterprise-ssd-extended-shutdown-maintenance.md`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md)

---

## 12. Status

**Bounded deepening complete.**

The public-document chronology is now tighter: the inspected LSI Version 1.0 (February 2003) documents Consistency Check but not Patrol Read; Dell PERC 4/Di/Si family documentation exposes Patrol Read by April 2005; Dell's MegaPR Linux host utility follows on 7 June 2005 and explicitly requires supporting firmware; LSI's generic MegaRAID Version 2.0 documentation exposes Patrol Read by its February/March 2006 edition. The main retention-method result is provenance-sensitive: multiple documents and corporate mastheads may corroborate an interface while still belonging to an overlapping controller lineage, so source count must not be mistaken for independent engineering-lineage count.