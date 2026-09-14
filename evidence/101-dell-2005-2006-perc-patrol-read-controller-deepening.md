# Case 101 deepening — Dell PERC Background Patrol Read as controller-level proactive maintenance, 2005–2006

- **Status:** `bounded deepening complete`
- **Canonical case:** [`../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md`](../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md)
- **Slice:** named hardware-RAID-controller `Patrol Read` evidence, bounded to Dell PERC 3/4/4e public material from 2005–2006 plus one later Dell support document that preserves legacy implementation details.
- **Question:** when proactive medium verification moves above an individual drive into a RAID controller, which maintenance relations become controller state, which repair paths depend on array redundancy, and which apparently persistent maintenance records are **not** exact restart checkpoints?

This record closes one narrow debt in Case 101. It does **not** attempt a full genealogy of `patrol read`, LSI/MegaRAID, IBM ServeRAID, SCSI VERIFY tooling, RAID consistency checking, or disk scrubbing.

---

## 1. Why this slice was selected

Case 101 already grounds T10 `Background Medium Scan` as a device-side SCSI maintenance interface and explicitly leaves **named hardware RAID-controller Patrol Read genealogy** open. The missing bounded witness was therefore not another disk-internal scan, but a controller that:

1. publicly calls the operation `Patrol Read`;
2. schedules it across member drives;
3. can use RAID redundancy when a medium defect is found;
4. distinguishes this work from parity/mirror `Consistency Check` and from SMART prediction; and
5. retains some maintenance-control/evidence state outside user payload.

Dell PERC 3/4/4e material satisfies that bounded need without requiring a claim that Dell or LSI invented the term or mechanism.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated `patrol read` history to reuse. Broader controller genealogy should still be routed there if developed later.

---

## 2. Source chronology and evidence quality

### 2.1 7 June 2005 — Dell MegaPR utility release record — period vendor record

Dell's still-live driver record for **MegaPR for Linux**, version `1.03, A02`, gives a release date of **7 June 2005** and categorizes the package as `SCSI RAID`. Dell states that MegaPR can start and stop Patrol Read and display its current status on specified PERC controllers, including PERC 3/DCL, 3/DC, 3/QC, 3/SC, PERC 4/Di, 4/SC, 4/DC, and PERC 4e/DC, 4e/Di, 4e/Si.

This is a strong period product/software witness for a named controller-side `Patrol Read` control surface by June 2005.

Source:

- Dell, **MegaPR for Linux, v.1.03, A02**, release date 7 June 2005: <https://www.dell.com/support/home/en-us/drivers/driversdetails?driverid=nfpxp>

A parallel Windows package survives in Dell support as well. The bounded claim here does not depend on choosing one host OS.

### 2.2 February 2006 — Dell Power Solutions article — period vendor publication

Drew Habas and John Sieber, **“Background Patrol Read for Dell PowerEdge RAID Controllers,”** was reprinted from *Dell Power Solutions*, February 2006, pp. 73–75. The inspected surviving PDF copy visibly carries `www.dell.com/powersolutions`, the Dell Power Solutions page furniture, and `Copyright © 2006 Dell Inc.`. Habas is identified as a Dell RAID product marketing manager and Sieber as lead engineer for Dell's SCSI RAID development group.

The historical Dell URL was:

- <http://www.dell.com/downloads/global/power/ps1q06-20050212-Habas.pdf>

The original URL is no longer conveniently retrievable in this research environment. A page-preserving surviving copy inspected for this slice is:

- <https://device.report/m/6f19713c57627fcded037f379ce7f40935f82e64231047790be0b44ae2498823.pdf>

Because the surviving host is not Dell, claims from the article are limited to what is directly visible in the PDF artifact and its Dell imprint. The mirror is not treated as independent corroboration.

### 2.3 Dell support document 000129145 — later vendor documentation of legacy PERC behavior

Dell currently publishes **“Patrol ReadによるRAIDアレイのメンテナンス”**, document `000129145`, version 7, last updated **24 February 2026**. The page describes legacy PERC 3/4/4e firmware families, MegaPR control, controller error handling, NVRAM-maintained Patrol Read state, completion bitmaps, scheduling, and error logs.

Source:

- Dell, document `000129145`, **Patrol ReadによるRAIDアレイのメンテナンス**, current version 7: <https://www.dell.com/support/kbdoc/ja-jp/000129145/patrol-read%E3%81%AB%E3%82%88%E3%82%8Braid%E3%82%A2%E3%83%AC%E3%82%A4%E3%81%AE%E3%83%A1%E3%83%B3%E3%83%86%E3%83%8A%E3%83%B3%E3%82%B9>

This is **not** used to back-date every sentence to 2005. It is a later Dell support record describing the legacy implementation family. The June 2005 utility record and February 2006 article carry the period-publication burden.

---

## 3. Historical record

### H/P — a named RAID-controller Patrol Read control surface was public by June 2005

Dell's 7 June 2005 MegaPR package is not generic documentation about disk scanning. It is software specifically for the PERC controller families listed above, with start, stop, and status functions for `Patrol Read`.

Therefore the bounded historical statement is:

```text
by 7 June 2005:
Dell publicly distributed host software
    -> controls named PERC Patrol Read state
```

This is stronger than a later recollection that such a feature once existed, but weaker than a claim about invention date, first firmware availability, or internal development chronology.

### H/P — Dell's 2006 article places proactive verification at the RAID-controller layer

The February 2006 Dell article describes Background Patrol Read as a PERC feature that issues commands to each drive in the array to test sectors. When a bad sector is found, the article says the PERC instructs the drive to reassign it and reconstructs the data using the other drives; the affected drive then writes the reconstructed data to the replacement sector.

The article also says configured drives, including hot spares, are checked, while its footnote excludes drives that are neither array members nor hot spares because they do not yet contain array data.

The historically bounded structure is therefore:

```text
controller-level maintenance policy
    -> issue drive commands across configured members
    -> discover bad sector
    -> use RAID peers when reconstructable
    -> instruct reassignment / rewrite on affected drive
```

This is not equivalent to a drive autonomously scanning itself.

### H/P — Auto and Manual are different maintenance policies

Dell's 2006 article distinguishes:

- **Auto mode** — after checking the array, Patrol Read repeats indefinitely;
- **Manual mode** — one pass, then stop until an administrator starts another pass.

The article further says ordinary data I/O remains the RAID subsystem's highest priority, Patrol Read uses spare bandwidth, and the controller adjusts command frequency and size according to outstanding I/O.

Thus the controller retained not only a maintenance capability but a policy about recurrence and foreground priority.

Historical terms here are Dell's `Auto mode`, `Manual mode`, `Background Patrol Read`, and workload-sensitive command behavior. `maintenance policy` is the project reconstruction.

### H/P — Patrol Read, Consistency Check, and SMART were explicitly separate functions

Dell's 2006 article places three functions in the PERC Fault Management Suite:

1. **Background Patrol Read** — proactive disk-media-error discovery/recovery in redundant arrays;
2. **Consistency Check** — checking/correcting inconsistency between RAID data and parity, or between mirror copies;
3. **SMART alerts** — predictive warning about deteriorating drive behavior.

The article acknowledges overlap: Consistency Check can encounter media errors and trigger recovery. But it explicitly calls Consistency Check a **data-level check**, says it requires more controller resources to read and compare data, and presents Patrol Read as the more efficient operation for the medium-error problem.

Therefore:

```text
Patrol Read
    != Consistency Check
    != SMART prediction
```

The distinction is historical, not merely a later project taxonomy.

### H/L — the later Dell support record exposes RAID-state-dependent repair behavior

Dell document `000129145` says MegaRAID firmware retries `Verify` to the affected LBA up to five times before stopping Patrol Read, performing recovery, and resuming from the stopping point. It then describes different responses by array state:

- RAID 0: log / continue without redundant reconstruction;
- non-optimal RAID state: do not perform the same repair path;
- RAID 1: read data from the mirror and write-verify;
- RAID 5: initiate recovery logic using peer drives and write-verify;
- hot spare: write-verify behavior is available.

This later vendor record makes an important controller-level distinction explicit:

```text
medium defect detected
    != payload reconstructable from the present array state
    != repair completed
```

The exact implementation language is from the later support record; it is not silently attributed to the 2005 T10 committee or to every PERC generation.

### H/L — some Patrol Read control/evidence state is stored in controller NVRAM

Dell document `000129145` explicitly says firmware stores Patrol Read data in **NVRAM**. It identifies purposes including:

1. tracking physical-drive progress;
2. scheduling Patrol Read start times; and
3. logging error information.

The page then describes:

- a configurable frequency for clearing the PR-complete bitmap;
- `PR completed Bitmap`;
- `Last complete Bitmap`;
- a bitmap-clear timestamp;
- frequency between Patrol Read iterations;
- next desired start time, including storage of a next start time in NVRAM;
- error information with physical drive and LBA;
- logs for both recovered and unrecovered errors.

The evidence therefore supports durable controller-side **maintenance metadata** beyond user payload and beyond the disk sector being tested.

### H/L — persistent maintenance metadata is not an exact execution checkpoint

The same Dell support document gives the counterexample that makes the NVRAM evidence useful rather than merely descriptive. It says that if the server reboots while Patrol Read is running in **Auto** mode, Patrol Read starts the operation again **from the beginning**. In **Manual** mode it does not restart automatically.

Therefore, despite NVRAM-maintained scheduling, completion summaries, and error records:

```text
persistent maintenance metadata
    != persistent exact scan-position checkpoint
```

and:

```text
reboot after Auto-mode interruption
    -> restart work from beginning

reboot after Manual-mode interruption
    -> no automatic restart
```

This is a strong negative boundary. NVRAM persistence does not imply that all in-flight maintenance state is checkpointed for exact continuation.

### H/L — completion bitmaps are bounded summaries, not per-LBA certificates

Dell's later support document says the firmware periodically clears a PR-completion bitmap, saves the prior bitmap as `Last complete Bitmap`, and retains the bitmap-clear timestamp. Its example says these values let a user know which drives completed Patrol Read at least once within the recent two clear cycles; with a 30-day clear period, that gives a roughly 30–60-day window depending on position in the cycle.

That is useful retained evidence, but its granularity is **per physical drive / completion cycle**, not one durable verification record per logical sector.

Therefore:

```text
recent drive-level completion evidence
    != per-LBA verification history
    != timeless proof of readability
```

---

## 4. Engineering reconstruction

The following relations are project reconstructions from the documented behavior, not Dell's historical ontology.

### E/R — moving the maintenance locus changes the available repair context

A drive-internal scan can know its own medium and defect-management mechanisms. A RAID controller can additionally know which drives belong to the same redundancy relation and can coordinate reconstruction across them.

Thus:

```text
drive-local readability test
    != controller-level redundancy-aware maintenance
```

The difference is not merely where code happens to run. It changes which other embodiments can serve as repair sources.

### E/R — coverage, reconstructability, and remediation are distinct relations

A controller may successfully exercise an LBA and discover a defect while still lacking enough admissible peer data to reconstruct the payload. Dell's RAID-0 and non-optimal-array branches make this concrete.

A more precise chain is:

```text
maintenance coverage
    -> defect evidence
    -> repair-source qualification
    -> reconstructability
    -> reassignment / rewrite attempt
    -> restored redundancy/readability state
```

No arrow is logically guaranteed merely by the preceding one.

### E/R — policy persistence, summary persistence, and execution persistence have different horizons

Dell's later NVRAM documentation plus reboot behavior supports at least four maintenance-state classes:

1. **policy / mode state** — whether recurrence is automatic, manual, halted, or disabled;
2. **schedule state** — when another pass is intended;
3. **summary / evidence state** — recent per-drive completion and error records;
4. **in-flight execution position** — where the current pass was when interrupted.

The first three can have longer persistence than the fourth.

Therefore:

```text
maintenance-control persistence horizon
    != maintenance-execution persistence horizon
```

This directly complements the repository's maintenance-control-state synthesis without implying that every controller partitions state in the same way.

### E/R — repeated full scans can be correct behavior after losing an exact checkpoint

Restarting from the beginning after reboot performs redundant maintenance work. It does not by itself mean the policy or prior evidence was forgotten.

```text
lost exact progress
    -> possible repeated verification work
    != loss of all maintenance policy/history
```

Conversely, retaining a recent completion bitmap does not reconstruct the exact place from which an interrupted pass could safely continue.

---

## 5. Functional comparison with T10 Background Medium Scan

This comparison is deliberately **functional**, not genealogical.

| Relation | T10 / drive-side BMS in canonical Case 101 | Dell PERC Patrol Read, 2005–2006 bounded slice |
| --- | --- | --- |
| Maintenance locus | SCSI device server / drive-side function | RAID controller orchestrating member drives |
| Main evidence target | difficult/unreadable logical blocks and scan results | drive-media defects across configured RAID members/hot spares |
| Redundancy knowledge | not inherently an array-level relation | controller can use mirror/parity peers when array state permits |
| Repair control | ARRE/AWRE and vendor-specific device action | controller can coordinate reconstruction plus drive reassignment/rewrite |
| Recurrence policy | BMS interval / background controls | Dell Auto vs Manual modes |
| Workload interaction | background operation with idle/suspend controls | foreground I/O priority; command rate/size adjusted with workload |
| Exposed retained evidence | scan count/progress/result log | controller status plus later-documented NVRAM schedule/completion/error state |

The comparison supports:

```text
similar proactive-medium-verification function
    != same maintenance locus
    != same repair authority
    != same control-state representation
    != demonstrated historical descent
```

No inspected source says Dell PERC Patrol Read was an implementation of T10 `04-198r5`, used the standardized BMS operation internally, or descended from Seagate's proposal. The two records are chronologically close, but chronology is not genealogy.

---

## 6. Cross-case links

### Case 14 — SCSI defect reassignment

Case 14 owns the lower-level distinction between stable logical address and replacement physical sector. Dell PERC adds a controller above that relation which can reconstruct payload before asking the affected drive to reassign/rewrite.

Therefore:

```text
replacement sector availability
    != recoverable old payload

RAID reconstruction source
    + drive reassignment
    -> one possible controller-level recovery path
```

The second line is bounded to the documented Dell redundant-array behavior, not a universal SCSI rule.

### Case 18 — ZFS scrub

Both can proactively find latent problems before demand, but ZFS has filesystem/pool checksum identity and end-to-end redundancy semantics. PERC Patrol Read is a controller-level media-defect operation and does not thereby establish application-level or filesystem-level content correctness.

```text
PERC media verification
    != end-to-end checksum verification
```

### Case 55 — SMART telemetry

Dell itself separates SMART predictive warning from active Patrol Read coverage. This gives a period vendor counterexample to collapsing telemetry into verification:

```text
health prediction
    != active medium coverage
    != repaired payload
```

### Synthesis 26 — maintenance-control-state persistence horizons

Dell PERC supplies a useful controller case where schedule/completion/error metadata can be retained in NVRAM while an interrupted Auto scan starts again at the beginning. Functionally this is a direct example of:

```text
retained policy/evidence
    != retained exact execution frontier
```

This is a cross-case relation, not evidence that PERC shares an implementation with DRAM, HDFS, NAND, or other synthesis cases.

---

## 7. Philosophical interpretation — bounded

The PERC case sharpens a narrow form of **retained obligation**. The controller may preserve evidence that verification has been completed recently, evidence that errors were seen, and a schedule saying work is due again. Those records do not contain the user payload, yet they change what future maintenance actions are warranted.

The conceptual point stops there. NVRAM bitmaps and schedules are not `memory` in a human sense, and periodic verification is not what physically keeps magnetic domains magnetized. The maintenance records preserve a relation between **what has been checked, what remains due, and what defects have already been observed**; they do not become the stored object itself.

The reboot counterexample also blocks an overly strong equation between memory and continuity: a system can remember enough to know that recurring maintenance exists while forgetting the exact execution point of the interrupted pass.

---

## 8. Explicit non-claims

This slice does **not** claim that:

1. Dell or LSI invented background disk scanning;
2. Dell coined `Patrol Read`;
3. June 2005 is the first firmware date for the feature;
4. every PERC model supported the same Patrol Read semantics;
5. every MegaRAID controller used Dell's exact policy;
6. Dell Patrol Read was derived from T10 Background Medium Scan;
7. Dell Patrol Read invoked the standardized T10 BMS command internally;
8. controller `VERIFY` behavior proves one universal SCSI command sequence across firmware versions;
9. a successful Patrol Read proves higher-layer data integrity;
10. a completed pass proves future readability indefinitely;
11. the NVRAM completion bitmap is a per-LBA ledger;
12. NVRAM schedule/error persistence proves exact in-flight progress persistence;
13. restarting Auto mode from the beginning proves all prior maintenance evidence was discarded;
14. discovering a bad sector proves the payload is reconstructable;
15. reassignment proves that the old payload was recovered;
16. Consistency Check and Patrol Read are interchangeable because both may encounter media errors;
17. SMART prediction is equivalent to proactive coverage;
18. RAID redundancy always supplies enough good peer data for repair;
19. the current 2026 support-page wording was published verbatim in 2005; or
20. this bounded Dell witness closes the broader cross-vendor controller patrol-read genealogy.

---

## 9. Claim ledger

| Claim | Type | Evidence strength | Boundary |
| --- | --- | --- | --- |
| Dell distributed MegaPR control/status software for Patrol Read on named PERC 3/4/4e controllers by 7 Jun 2005 | Historical record | strong period vendor record | no first-invention claim |
| Dell described PERC Patrol Read as controller-orchestrated proactive media-defect detection/recovery in Feb 2006 | Historical record | strong period vendor publication, surviving mirrored artifact | mirror is provenance carrier, not independent source |
| PERC could reconstruct from peer drives and coordinate reassignment/rewrite when redundancy allowed | Historical record | strong period vendor publication | not guaranteed in degraded/nonredundant state |
| Dell explicitly separated Patrol Read, Consistency Check, and SMART | Historical record | strong period vendor publication | overlap in media-error discovery does not erase semantic difference |
| Later Dell documentation says Patrol Read state, schedule, completion summary, and errors can be kept in NVRAM | Historical record, later vendor continuity | strong later vendor support record | do not back-date exact wording automatically |
| Auto-mode reboot restarts from the beginning while Manual does not auto-restart | Historical record, later vendor continuity | strong later vendor support record | exact behavior bounded to described legacy implementation |
| Persistent maintenance metadata need not be an exact execution checkpoint | Engineering reconstruction | strong inference from NVRAM + reboot behavior | not universal to all controllers |
| Controller-level maintenance has redundancy-aware repair context unavailable to a single-drive scan as such | Engineering reconstruction | strong bounded inference | drive may have other recovery mechanisms; no universal superiority claim |
| PERC Patrol Read and T10 BMS are functionally comparable proactive verification regimes | Functional analogy | useful bounded comparison | no genealogy or command identity |
| Retained maintenance evidence can preserve obligation without preserving exact execution continuity | Philosophical interpretation | bounded to documented mechanism | not a definition of memory in general |

---

## 10. What this closes and what remains open

### Closed by this slice

- one **named hardware RAID-controller** public Patrol Read witness by June 2005;
- one period Dell explanation of controller-level proactive media-defect discovery and redundancy-assisted repair;
- one period vendor distinction between `Patrol Read`, `Consistency Check`, and `SMART`;
- one bounded later-vendor record of PERC NVRAM maintenance state;
- the relation `persistent maintenance metadata != persistent exact execution checkpoint` for the described PERC behavior.

### Still open

- pre-June-2005 Dell/LSI firmware-development chronology and first shipment;
- LSI/MegaRAID documentation independent of Dell branding;
- IBM ServeRAID and other controller vendors' period terminology;
- when and where `patrol read` terminology first appears publicly;
- whether any direct genealogy links Dell/LSI Patrol Read to T10 BMS, earlier SCSI VERIFY sweeps, or another implementation family;
- cross-vendor Patrol Read versus parity/consistency-check behavior;
- fault injection against period PERC hardware;
- exact persistence behavior of every documented NVRAM field across reboot, controller replacement, firmware update, battery loss, and NVRAM corruption;
- whether the older PERC completion bitmaps survived every reset/power-loss path or only specified controller lifecycle events;
- broader controller-history synthesis, which belongs primarily in `computing-archaeology`.

---

## 11. Source list

### Period vendor sources

- Dell, **MegaPR for Linux, v.1.03, A02**, 7 June 2005, SCSI RAID utility: <https://www.dell.com/support/home/en-us/drivers/driversdetails?driverid=nfpxp>
- Drew Habas and John Sieber, **“Background Patrol Read for Dell PowerEdge RAID Controllers,”** *Dell Power Solutions*, February 2006, pp. 73–75. Historical Dell URL: <http://www.dell.com/downloads/global/power/ps1q06-20050212-Habas.pdf>. Inspected surviving PDF: <https://device.report/m/6f19713c57627fcded037f379ce7f40935f82e64231047790be0b44ae2498823.pdf>

### Later vendor continuity / implementation detail

- Dell, **Patrol ReadによるRAIDアレイのメンテナンス**, document `000129145`, version 7, last updated 24 February 2026: <https://www.dell.com/support/kbdoc/ja-jp/000129145/patrol-read%E3%81%AB%E3%82%88%E3%82%8Braid%E3%82%A2%E3%83%AC%E3%82%A4%E3%81%AE%E3%83%A1%E3%83%B3%E3%83%86%E3%83%8A%E3%83%B3%E3%82%B9>

### Canonical internal comparisons

- [`../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md`](../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md)
- [`../cases/14-scsi-disk-defect-reassignment-logical-identity.md`](../cases/14-scsi-disk-defect-reassignment-logical-identity.md)
- [`../cases/18-zfs-scrub-latent-error-detection.md`](../cases/18-zfs-scrub-latent-error-detection.md)
- [`../cases/55-nvme-smart-health-endurance-telemetry.md`](../cases/55-nvme-smart-health-endurance-telemetry.md)
- [`../docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md`](../docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md)
- [`../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md)

---

## Final bounded result

Dell PERC supplies a period, named **controller-level** proactive verification witness that complements but does not collapse into T10's drive-side Background Medium Scan. The controller can coordinate media testing across array members, use redundancy when repair is possible, and distinguish media scanning from parity/mirror consistency checking and SMART prediction. Later Dell documentation adds a particularly useful retention boundary: schedule/completion/error state can live in NVRAM while an interrupted Auto Patrol Read still restarts from the beginning.

The resulting controlled relation is:

```text
retained maintenance policy / summary / error evidence
    !=
retained exact execution frontier
```

That is the bounded contribution of this slice. It is not a claim of invention, direct T10 genealogy, universal controller semantics, or complete controller patrol-read history.