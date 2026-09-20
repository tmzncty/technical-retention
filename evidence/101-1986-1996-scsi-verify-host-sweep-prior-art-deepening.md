# Case 101 deepening — SCSI VERIFY and host-initiated media sweeps before autonomous BMS

Status: `bounded deepening complete`

## Scope

This evidence packet deepens [`../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md`](../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md) along one narrow historical and engineering seam:

> **Before IBM ServeRAID `Data Scrubbing`, Dell/LSI `Patrol Read`, and T10 `Background Medium Scan`, what did the SCSI `VERIFY` command and host-adapter media-scan utilities already provide — and what did they still leave to the host/operator?**

The bounded answer is:

- the 1986 SCSI standard already contained an optional direct-access `VERIFY` command (`2Fh`) for checking a specified logical-block range;
- a named 1995 Seagate SCSI drive documented `VERIFY (2Fh)` as a drive-executed medium check, with ECC-based verification when byte comparison was not requested;
- a June 1996 Adaptec AHA-1520B host-adapter manual exposed `Verify Disk Media` through `SCSISelect`, letting an operator scan a selected SCSI disk for defects and choose whether discovered bad blocks should be reassigned;
- these records establish a direct pre-2001 / pre-2005 floor for **host-initiated proactive media verification**;
- they do **not** establish autonomous background scheduling, durable scan-progress state, recurring cadence, idle/preemption policy, or a retained device-side result log comparable to later T10 BMS.

The retained-state significance is therefore not `SCSI already had BMS in 1986`. It is narrower:

```text
verification primitive exists
    !=
maintenance policy exists
    !=
maintenance is autonomously scheduled
    !=
coverage progress is retained
    !=
repair is automatically authorized/completed
```

This packet makes no invention-priority claim for disk scrubbing, host diagnostics, SCSI verification, bad-block reassignment, or later background scanning.

---

## Source set and custody

### P1 — NBS FIPS 131 / ANSI X3.131-1986 SCSI record

NIST bibliographic record:

- title: *Federal Information Processing Standards Publication: for information systems - small computer system interface (SCSI)*;
- year: **1986**;
- publisher: National Bureau of Standards;
- report number: **NBS FIPS 131**;
- DOI: `10.6028/NBS.FIPS.131`;
- bibliographic record: <https://pages.nist.gov/NIST-Tech-Pubs/bib/NBS.FIPS.131.ris>.

The surviving indexed text of the FIPS publication reproduces **ANSI X3.131-1986** and includes §8.2.6 `VERIFY Command` for direct-access devices, operation code `2Fh`. The indexed clause states that the command asks the target to verify data on the medium; with `BytChk=0`, verification is a medium check such as CRC/ECC rather than an initiator-data comparison; the CDB carries a logical block address and a verification length covering contiguous logical blocks.

The same FIPS publication states an effective date of **16 December 1987** for the federal profile.

**Custody note:** the NIST bibliographic record is directly inspectable as HTML/RIS. The clause text used here is preserved by NIST/GovInfo indexed text for the historical PDF. The PDF was not re-certified page-by-page in this slice because the public gateway did not expose a usable page-image view. Therefore this packet treats the exact clause wording as a strong indexed-primary witness, while avoiding page-number/facsimile claims beyond what was inspectable.

### P2 — T10 / X3T9.2 SCSI-2 chronology

T10's historical X3T9.2 archive identifies:

- SCSI-1 as **X3.131:1986**;
- the final SCSI-2 committee draft as **Revision 10L, 7 September 1993**;
- the published SCSI-2 standard as **X3.131:1994** (later reaffirmed).

Historical archive entry:

- <https://www.t10.org/x3t9_2.htm> (or surviving mirror where the T10 guest gateway intervenes).

This packet uses the T10 chronology only to anchor standards history. It does not infer that every optional command was implemented by every SCSI target.

### P3 — Seagate Medalist 1080sl SCSI Product Manual, August 1995

A surviving text transcription of Seagate's *Medalist 1080sl SCSI Product Manual*, dated **August 1995**, documents §3.5.6 `Verify command (2FH)`:

- the drive verifies data on the disc when it receives the command;
- the logical-block-address field selects where verification begins;
- the verification-length field specifies the number of contiguous logical blocks to verify;
- with `BytChk=0`, the drive performs medium verification by checking ECC syndromes;
- with `BytChk=1`, it performs a byte-by-byte comparison of stored data.

Source transcription:

- <https://manualzilla.com/doc/7322090/seagate-medalist-1080sl-product-manual>.

**Custody note:** this is a third-party text mirror of a vendor-authored period manual, not a currently Seagate-hosted facsimile. It is used as a named-product implementation witness and is not elevated above the standard/archival chronology for invention or standards priority.

### P4 — Adaptec AHA-1520B Installation Guide, Rev. A, June 1996

A surviving page-preserving transcription of Adaptec's **AHA-1520B Installation Guide**, Part Number `511162-00`, Rev. A, identifies:

- current document date **30 May 1996**;
- copyright **1996 Adaptec, Inc.**;
- stock line `KL 6/96`;
- product description `ISA-to-Fast SCSI-2 Host Adapter`.

The guide says `SCSISelect` contains utilities to low-level format or **verify the disk media** of attached SCSI hard disks. On page 9, `Verify Disk Media` is described as a utility that scans a selected hard-disk medium for defects. If bad blocks are found, the utility prompts the operator whether to reassign them; choosing yes causes those blocks no longer to be used. The operator may abort verification with `Esc`.

Relevant transcribed pages:

- page 8: <https://adaptec.manymanuals.com/camera-accessories/1520b-aha-storage-controller-fast-scsi-10-mbps/installation-guide-42358/8>
- page 9: <https://adaptec.manymanuals.com/camera-accessories/1520b-aha-storage-controller-fast-scsi-10-mbps/installation-guide-42358/9>
- page 16 / publication metadata: <https://adaptec.manymanuals.com/camera-accessories/1520b-aha-storage-controller-fast-scsi-10-mbps/installation-guide-42358/16>.

**Custody note:** the content is vendor-authored but currently accessed through a third-party page transcription. The packet therefore treats it as a strong period-document witness with weaker custody than a currently Adaptec/Broadcom-hosted original.

### P5 — later IBM institutional corroboration of SCSISelect semantics

IBM's still-live support record for Adaptec SCSI adapters documents the same `Verify Disk Media` maintenance vocabulary and says a medium error on a hard disk can be followed by verification/formatting through SCSISelect.

Current institutional record:

- <https://www.ibm.com/support/pages/node/844896>.

This is used only as later institutional corroboration of the utility family, not to date the feature earlier than the June 1996 Adaptec manual.

---

## Historical record

### H/P — the direct-access SCSI command set already exposed a verification primitive in 1986

The indexed ANSI/NBS text for X3.131-1986 identifies direct-access `VERIFY` as an optional command with operation code `2Fh`.

At the interface level the initiator could specify:

```text
logical block address
    +
verification length
    ->
target-side verification of that logical range
```

The standard also distinguished two verification modes:

```text
BytChk = 0
    -> medium verification such as CRC/ECC
    -> no initiator-data comparison

BytChk = 1
    -> compare medium data against initiator-supplied data
```

The crucial historical point is modest but important:

> **A standardized host-initiated medium-verification primitive predates the later background-scan terminology by nearly two decades.**

This does not mean that 1986 SCSI defined recurring scrubbing, idle scheduling, autonomous patrol, coverage checkpoints, or bad-block repair policy.

### H/P — a 1995 named SCSI disk implements VERIFY as an actual media/ECC operation

The Seagate Medalist 1080sl manual gives a concrete product-level witness rather than only a command-set abstraction.

For `VERIFY (2Fh)` the drive performs the work on the disc and, when byte comparison is not requested, checks ECC syndromes. The host selects a starting LBA and a contiguous verification length.

That supports a bounded mechanism chain:

```text
initiator selects logical range
    ->
drive reads / internally checks medium state
    ->
drive reports command outcome
```

The command can therefore renew evidence about **readability / recorded-code correctness** without transferring the user payload back to the host as an ordinary READ.

It does not by itself retain a later statement such as `this whole device was successfully scanned recently`.

### H/P — by June 1996 Adaptec exposed a human-invoked whole-disk media-scan workflow

The AHA-1520B manual places `Verify Disk Media` inside the host adapter's `SCSISelect` disk utilities.

The operator:

1. enters the SCSI disk utilities;
2. selects a target SCSI ID/device;
3. chooses `Verify Disk Media`;
4. allows the utility to scan the medium for defects;
5. is prompted if bad blocks are found;
6. decides whether those blocks should be reassigned.

This is historically stronger than merely saying `VERIFY existed` because it shows an explicit maintenance **workflow** exposed to an administrator.

But it remains host/operator initiated:

```text
operator decides to run scan
    -> host-adapter utility drives verification
    -> defects may be reported
    -> operator decides whether to reassign
```

The inspected manual does not describe:

- a recurring autonomous schedule;
- idle-time admission policy;
- a device-internal next-scan timer;
- retained traversal position across reboot;
- a persistent background-scan result page;
- a lifetime completion counter;
- automatic resumption after power loss.

Those absences are not proof that no Adaptec product ever had such capabilities. They are limits of this specific 1996 witness.

### H/P — verification and reassignment were already separate operator-visible stages

Adaptec's wording matters because a discovered bad block does not silently imply that it has already been repaired or removed from service.

The utility **prompts** the operator whether to reassign it.

Thus the period interface directly supports:

```text
defect discovered
    !=
reassignment authorized
    !=
reassignment completed
```

This is an earlier host-adapter form of a distinction that later T10 BMS makes more explicitly through result/status fields and separately controlled repair behavior.

### H/P — the earlier workflow is not historically called `Background Medium Scan`

The 1986 command vocabulary is `VERIFY`.

The 1996 Adaptec utility vocabulary is `Verify Disk Media`.

T10's 2005 vocabulary is `Background Medium Scan` / `Background Pre-Scan`.

Dell/LSI's controller vocabulary is `Patrol Read`.

IBM ServeRAID used `Data Scrubbing`.

These can be compared by function, but they must not be collapsed into one historical term.

---

## Engineering reconstruction

### E/R — command primitive and maintenance scheduler are different layers

A `VERIFY` command gives an initiator a mechanism for asking a target to qualify a bounded logical range.

It does not answer:

- who decides when verification is due;
- how a full-device pass is decomposed into commands;
- how foreground I/O preempts maintenance;
- whether progress survives reset;
- how often coverage repeats;
- how errors are accumulated over time;
- whether repair is automatic, conditional, or forbidden.

Therefore:

```text
verification primitive
    !=
maintenance scheduler
```

and:

```text
ability to verify any chosen range
    !=
proof that all ranges are periodically verified
```

### E/R — range completion is not a durable coverage certificate

A successful `VERIFY` command establishes only the bounded command outcome under the device's verification criteria at that time.

A higher layer would have to retain additional state if it wanted to claim whole-device maintenance progress, for example:

```text
next range / cursor
last completed pass
last completion time
error history
policy / recurrence interval
```

The 1986 command itself does not create those higher-level obligations.

Thus:

```text
command completion
    !=
durable maintenance-history state
```

### E/R — host-driven sweep and autonomous background scan relocate control authority

The 1996 SCSISelect workflow keeps **admission authority** with the operator/host utility.

Later device-internal BMS can keep recurring timing, idle/preemption behavior, scan progress, and result logging inside the device.

The broad functional change can be represented as:

```text
host/operator era

operator policy
    -> host-adapter utility
    -> one or more target verification operations
    -> status / prompt

later device-background era

retained device policy
    -> device scheduler / admission
    -> internal scan traversal
    -> background result state
```

This is an engineering comparison, not a demonstrated source-code or standards genealogy.

### E/R — medium verification is not semantic payload comparison

The standard/product distinction between `BytChk=0` and byte comparison matters.

With medium verification, the target may validate recorded data using ECC/CRC and its own read-recovery criteria without the initiator supplying an independent expected payload.

Therefore:

```text
medium verifies against its recorded code / ECC
    !=
application proves that the bytes are semantically the intended file contents
```

A perfectly self-consistent but stale or wrong logical payload may still pass an ECC-oriented medium verification.

This is one reason Case 101 must remain separate from filesystem/distributed checksum cases.

### E/R — discovery does not consume the same authority as repair

Adaptec's prompt-to-reassign workflow makes the control split explicit:

```text
readability evidence
    -> defect diagnosis
    -> repair decision
    -> reassignment
```

The first two can occur without the latter two.

This anticipates, functionally but not genealogically, later interfaces where scan result status and repair permission are separate retained/control relations.

---

## Controlled functional comparison

### SCSI VERIFY / SCSISelect vs T10 BMS

Shared function:

> deliberately exercise medium readability before ordinary application demand happens to discover a latent defect.

Different control structure:

| Relation | SCSI VERIFY / 1996 SCSISelect | T10 BMS |
|---|---|---|
| maintenance trigger | initiator/operator command | device-side background policy after enable |
| range selection | initiator-selected LBA/length or utility sweep | device-managed traversal |
| foreground interaction | determined by host/device command execution | explicit background idle/preemption semantics |
| progress state | not established by the bounded 1986/1996 witnesses | standardized background status/progress semantics |
| recurring cadence | not established | standardized interval/control semantics |
| result retention | ordinary command/sense outcome; utility behavior | Background Scan Results log page |
| repair authority | separate utility/operator reassign decision in Adaptec witness | separately controlled/vendor-specific behavior |

The table is a project reconstruction from the inspected sources. It is not period vocabulary.

### IBM ServeRAID / Dell-LSI Patrol Read

IBM's later `Data Scrubbing` and Dell/LSI's `Patrol Read` add controller-resident recurring maintenance and, in RAID contexts, redundancy-aware repair authority.

The pre-2001 SCSI VERIFY / SCSISelect floor therefore blocks only a **generic proactive-verification novelty claim**. It does not erase the historical significance of moving maintenance scheduling, progress, and repair policy into drive/controller firmware.

### Case 14 — reassignment

Case 14 remains canonical for the mechanics and limits of SCSI defect reassignment.

This packet only needs the relation:

```text
verify discovers / reports a suspect region
    !=
reassign changes the physical embodiment behind an LBA
```

Do not treat a successful Verify Disk Media pass as evidence that every discovered defect was reassigned, or that reassignment preserved the old payload.

### Cases 27 / 83 and Synthesis 08 — higher-layer scrub

Ceph deep scrub and HDFS BlockScanner can also perform proactive verification before demand, but they operate over higher-level integrity evidence and replica authority.

The comparison is functional only:

```text
SCSI medium verification
    !=
filesystem checksum scrub
    !=
distributed replica qualification
```

No SCSI→HDFS/Ceph genealogy is claimed.

---

## Philosophical interpretation — bounded

Case 101 already treats proactive checking as one form of **epistemic maintenance**: the medium may still physically exist while confidence in future readability becomes stale because no recent operation has tested it.

The pre-BMS slice adds a useful limit.

A system may possess the **capacity to produce new evidence** without retaining an autonomous obligation to do so.

```text
ability to test
    !=
retained schedule to test
    !=
retained evidence that testing occurred
```

In the 1996 host-utility witness, maintenance still depends on an operator invoking the utility. Later BMS/controller scrubbing can move more of that obligation into retained machine state: enable bits, recurrence intervals, progress, completion summaries, or result logs.

This is a project interpretation. ANSI, Seagate, Adaptec, IBM, and T10 did not formulate the distinction in these philosophical terms.

---

## Prior-art boundary

This deepening closes one narrow historical debt in Case 101:

> **Direct evidence now exists that host-initiated SCSI medium verification and operator-invoked media sweeps predate the 1997–1998 IBM ServeRAID data-scrubbing witnesses, the 2001/2002 IBM background-scanner patent record, the 2003 Seagate BGMS filing, and the 2005 T10 BMS / Dell Patrol Read records.**

It does **not** establish:

- the first-ever disk scrub;
- the first implementation of SCSI `VERIFY`;
- the first shipping drive to support `VERIFY`;
- the first host utility to sweep an entire SCSI disk;
- that SCSISelect internally used only `VERIFY (2Fh)` rather than a vendor/tool-specific command sequence;
- that T10 BMS was directly derived from Adaptec SCSISelect;
- that IBM ServeRAID, Dell/LSI Patrol Read, or Seagate BGMS descended from this exact utility;
- that every successful command generated durable progress/history state;
- that every discovered defect was automatically repaired;
- that ECC-valid data was semantically current application data.

Broader SCSI/SASI command genealogy, early host-diagnostic software, exact SCSISelect command traces, vendor implementation chronology, and the wider history of the words `verify`, `scrub`, `patrol`, and `scan` belong primarily in `tmzncty/computing-archaeology`.

A fresh companion-repository search for `VERIFY` did not surface a dedicated SCSI VERIFY history packet to reuse in this run.

---

## Explicit non-claims

1. `VERIFY present in X3.131-1986` does not mean every SCSI-1 disk implemented it.
2. An optional command in a standard is not proof of first invention.
3. The FIPS effective date is not the SCSI command's conception date.
4. A standard publication date is not a product shipment date.
5. A 1995 Seagate manual is not evidence that Seagate originated `VERIFY`.
6. A third-party manual transcription is not the same custody class as a currently vendor-hosted facsimile.
7. `BytChk=0` medium verification is not an independent application-data comparison.
8. Passing ECC-oriented verification does not prove the logical payload is the newest/current version.
9. Passing one range does not prove the rest of the medium is readable.
10. Passing a whole-device sweep does not guarantee future readability indefinitely.
11. A scan's discovery time is not the defect's creation time.
12. A bad-block prompt is not automatic reassignment.
13. Authorization to reassign is not proof reassignment completed.
14. Reassignment is not proof the old payload was preserved.
15. `Verify Disk Media` is not historical evidence for the term `Background Medium Scan` in 1996.
16. `VERIFY` is not `Patrol Read` merely because both can expose latent defects.
17. Host-adapter execution is not drive-autonomous scheduling.
18. Ability to abort a scan is not evidence of retained resume position.
19. The inspected Adaptec manual does not establish power-loss-persistent progress.
20. It does not establish a recurring cadence.
21. It does not establish an idle-start policy.
22. It does not establish a persistent result log.
23. It does not prove SCSISelect issued one exact CDB sequence for all devices.
24. T10 BMS standardization is not made historically redundant by earlier host verification.
25. Functional continuity is not demonstrated genealogy.
26. Later IBM support corroboration does not back-date feature introduction.
27. SCSI medium verification is not filesystem checksum scrub.
28. SCSI medium verification is not distributed replica repair.
29. `verification complete` is not a secure-erasure or sanitization claim.
30. This packet does not close the full controller-patrol-read or disk-scrubbing genealogy.

---

## Claim ledger

| Claim | Type | Evidence strength | Boundary |
|---|---|---:|---|
| ANSI X3.131-1986 includes optional direct-access `VERIFY (2Fh)` | H/P | strong indexed primary | no implementation-universality claim |
| `BytChk=0` performs medium verification rather than initiator-data comparison | H/P | strong indexed primary + product witness | no semantic-payload-integrity claim |
| Seagate Medalist 1080sl documents LBA/length-bounded VERIFY with ECC checking | H/P* | strong period vendor-manual transcription | mirror custody noted |
| Adaptec AHA-1520B June-1996 SCSISelect exposes `Verify Disk Media` | H/P* | strong period vendor-manual transcription | no first-utility claim |
| Adaptec utility scans for defects and separately prompts for reassignment | H/P* | strong period vendor-manual transcription | prompt != automatic repair |
| verification primitive predates autonomous BMS | E/R constrained by H/P | strong | no direct genealogy claim |
| host-driven sweep != autonomous device-background maintenance | E/R | strong bounded comparison | implementation-specific details remain open |
| command completion != durable maintenance history | E/R | strong structural distinction | exact device logging may differ |
| ability to test != retained obligation/evidence of testing | philosophical interpretation | bounded downstream | not actor vocabulary |

---

## What this closes

Closed for Case 101:

- a direct pre-2001 / pre-2005 SCSI verification floor;
- a named mid-1990s drive implementing `VERIFY (2Fh)`;
- a named June-1996 host-adapter utility exposing an operator-invoked whole-disk defect scan and optional reassignment decision;
- the boundary `verification primitive != autonomous background maintenance policy`;
- the boundary `defect discovery != repair authorization/completion` at the host-utility layer;
- the boundary `medium verification != semantic payload comparison`.

Still open:

- SASI / pre-SCSI verification genealogy;
- first SCSI drive/product implementation of `VERIFY`;
- earlier 1980s host utilities that systematically swept disks;
- exact Adaptec SCSISelect command traces across device families;
- SCSI VERIFY → vendor `scrub` / `patrol` / `scan` terminology genealogy;
- named production incident evidence showing latent defects discovered by these 1990s host utilities;
- persistence/reset semantics for any progress state in particular host utilities;
- broader controller and drive background-maintenance history;
- independent fault injection.

---

## Related repositories

### `tmzncty/computing-archaeology`

Broad work belongs there for:

- SASI→SCSI command-set genealogy;
- SCSI-1 / SCSI-2 product adoption;
- host-adapter BIOS and diagnostic-utility history;
- CDC/Seagate/Quantum/Adaptec product chronology;
- exact `VERIFY` implementation genealogy;
- `scrub` / `verify` / `patrol` terminology migration.

Case 101 should retain only the narrow retention seam:

```text
host can request verification
    !=
host/device retains a maintenance obligation
    !=
coverage progress is checkpointed
    !=
repair authority exists
    !=
repair completes
```

### `tmzncty/problem-history`

A later problem-history episode could ask when storage operators began to formulate **latent unreadability before demand** as a distinct maintenance problem. This packet supplies one technical floor but does not claim the actors shared one stable problem vocabulary across SCSI VERIFY, Adaptec diagnostics, IBM `Data Scrubbing`, Dell/LSI `Patrol Read`, and T10 BMS.
