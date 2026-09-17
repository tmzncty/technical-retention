# Evidence 101 — 1986–1994 SCSI VERIFY as pre-BMS host-command prior art

- **Case:** [`../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md`](../cases/101-scsi-background-medium-scan-proactive-defect-discovery.md)
- **Slice:** SCSI `VERIFY` before the 2005 Background Medium Scan (BMS) standardization path
- **Status:** `bounded deepening complete`
- **Primary question:** what exactly existed before device-side BMS when a host wanted a drive to exercise a logical-block range for medium readability?

## Why this slice matters

Case 101 already grounds a different 2005–2007 relation: T10 standardized a **device-side background scan control/status regime** after explicitly acknowledging proprietary drive methods and operating-system scanning. The open debt was narrower:

> **What earlier SCSI command-level primitive let an initiator ask a direct-access device to verify a range of medium blocks, and what did that primitive not retain or schedule?**

This record closes that command/prior-art layer without turning Case 101 into a general SCSI history.

The bounded chronology is:

```text
ANSI X3.131-1986 (SCSI-1)
    -> optional direct-access VERIFY (2Fh)
    -> initiator supplies LBA + verification length
    -> medium verification can occur without byte comparison

1988 HP named-drive implementation
    -> VERIFY by ECC check only
    -> no initiator-data comparison on this product path

1994 Seagate named-drive implementation
    -> VERIFY range command
    -> BYT CHK=0 medium verification
    -> BYT CHK=1 byte-by-byte comparison

2005 T10 BMS work
    -> device-side idle/background recurrence
    -> background-control state + progress/results
    -> proactive coverage no longer requires one foreground VERIFY command per requested range
```

This is a chronology of documented interfaces and product behavior. It is **not** a demonstrated actor-to-actor genealogy.

---

## Source-control note

The original SCSI standard is **ANSI X3.131-1986**. T10's archival index identifies it as the original SCSI standard and as superseded by SCSI-2. A surviving National Bureau of Standards / NIST copy republishes the ANSI text as **FIPS PUB 131**, adopted for U.S. federal use in 1987.

Keep those dates distinct:

```text
ANSI standard designation: X3.131-1986
    !=
FIPS federal-adoption/publication wrapper: 1987
```

The federal wrapper is a convenient surviving copy of the ANSI technical text; it does not move the ANSI command's historical floor to 1987.

The current web reader could index the relevant FIPS/ANSI clause but could not render the 11.6 MB NIST/GovInfo PDF directly. Therefore the standard claim below is tied to the indexed primary text plus T10's archival designation record, while the 1994 Seagate product witness was directly inspected page-by-page in its manufacturer PDF.

---

## Historical record

### H1 — SCSI-1 already defined an optional direct-access `VERIFY` command

ANSI X3.131-1986 §8.2.6 defines `VERIFY` for **Direct Access** devices as optional operation code `2Fh`.

The command contains, among other fields:

- a logical block address;
- a verification length;
- `BytChk`;
- ordinary command-control bits.

The standard text says the target is asked to verify data on the medium. A zero `BytChk` selects **medium verification**, explicitly illustrated by CRC/ECC-style checking, while a one `BytChk` selects a byte-by-byte comparison between medium data and data transferred from the initiator. The logical block address identifies the first block and the verification length identifies a contiguous range.

Historical claim:

> **By the SCSI-1 standard, host-initiated range verification existed as a command-level interface before the later BMS control/status regime.**

This is not yet evidence of a periodic scrub daemon, whole-disk policy, or autonomous background maintenance.

### H2 — the command already separated medium checking from host-data comparison

The SCSI-1 distinction is important because the word `verify` can otherwise invite a false equivalence.

```text
BYTCHK = 0
    -> medium verification
    -> no byte-by-byte comparison against initiator payload

BYTCHK = 1
    -> byte-by-byte compare against initiator-supplied data
```

Therefore, even in the early command vocabulary:

> **media readability/error-code verification != equality comparison with a second host-provided copy.**

That distinction is historical, not a project invention.

It also blocks a modern overreading: `BYTCHK=0` medium verification is not automatically an end-to-end application checksum, cryptographic integrity proof, filesystem semantic check, or replica-currentness test.

### H3 — HP documented a named-drive VERIFY implementation in 1988

Hewlett-Packard's **_HP 9753XS/T/D SCSI Disk Drives_**, Edition 1, revision 20 December 1988, lists `VERIFY` (`2Fh`) among supported SCSI commands.

Its command description is more restrictive than the full two-way SCSI-1 option set: the drive verifies the requested logical-block range by **ECC check only** and says that a compare is not performed. The host still supplies a starting LBA and verification length.

This provides a named-product witness that is useful precisely because it is not identical to the entire standard option space:

```text
standard permits a VERIFY command family
    !=
every product exposes every comparison mode
```

and:

```text
VERIFY command present
    !=
byte-by-byte comparison necessarily implemented
```

The 1988 HP manual is product documentation, not evidence of first shipment, command invention, or the earliest SCSI implementation of VERIFY.

### H4 — Seagate documented both medium-only and byte-compare VERIFY modes in 1994

Seagate's **_ST3655 Family SCSI Drives Product Manual, Rev. A_**, Publication 36243-001, is dated **18 January 1994**.

Section 3.5.6, printed p. 67, documents `Verify command (2FH)` and states that the drive verifies data on disc. It exposes:

- `BYT CHK`;
- a logical block address;
- a verification length;
- optional disconnect while the command executes if the host adapter supports it.

The product manual says:

- `BYT CHK=0`: verify the medium without byte-by-byte comparison of stored data;
- `BYT CHK=1`: verify the medium and perform byte-by-byte comparison of stored data;
- the LBA marks where verification begins;
- verification length is the number of contiguous logical blocks to exercise.

The directly inspected manufacturer page therefore supplies a clean pre-2005 product witness for initiator-selected media verification across an address range.

### H5 — foreground command execution is not a retained background coverage regime

Neither the SCSI-1 command definition nor the inspected HP/Seagate product descriptions establish BMS-style retained maintenance control such as:

- an enable bit for recurring background scanning;
- an interval until the next pass;
- minimum idle time before scan work starts/resumes;
- current whole-medium progress;
- a retained scan count;
- a dedicated background-scan results log;
- a power-on pre-scan regime;
- autonomous continuation independent of a new host VERIFY request.

That absence must be stated narrowly. These documents describe the `VERIFY` command path; they do not prove that no firmware, operating system, RAID controller, diagnostic tool, or vendor extension maintained such state elsewhere.

The safe relation is:

> **one host-issued verification operation != a documented autonomous recurring verification regime.**

### H6 — the 2005 BMS proposal changes maintenance locus and control state, not the existence of medium verification itself

Case 101's existing T10 evidence says the 2005 proposal was standardizing a method to control and retrieve status from background medium scanning and that proprietary drive methods and operating-system scanning already existed.

Placed next to the older VERIFY evidence, the bounded historical change becomes more precise:

```text
pre-existing command-level medium verification
    + host-selected address range
    + host decides when to issue command

        !=

BMS background-maintenance regime
    + device-side scheduling/idle opportunity
    + retained background-control state
    + scan progress/results
    + optional repair/reassignment policy
```

This does **not** prove that operating-system scanners mentioned by T10 used `VERIFY`, rather than READ, vendor-specific commands, controller facilities, or some mixture.

---

## Engineering reconstruction

The following are project analytical relations, not ANSI/HP/Seagate/T10 historical vocabulary unless stated above.

### E1 — verification primitive versus coverage policy

A command that can exercise `N` contiguous blocks is a **verification primitive**. A policy that decides when every relevant block should be exercised is a **coverage regime**.

```text
VERIFY capability
    !=
whole-medium scrub policy
```

A host could in principle tile a medium with repeated VERIFY commands, but that construction is an engineering possibility. The inspected sources do not establish that a particular 1986/1988/1994 host actually did so periodically.

### E2 — maintenance locus

The older command path requires the initiator to name the range and issue the operation. BMS moves more of the recurrence/coverage decision into the device.

```text
host schedules + device verifies
    !=
device schedules background verification
```

This is a control-locus distinction, not a claim that the underlying read-channel/ECC physics became new in 2005.

### E3 — operation completion versus retained maintenance evidence

A successful VERIFY says something about the exercised range under the command's error-recovery/verification semantics at that time. It does not, by itself, retain a durable whole-medium history of what was checked when.

```text
command completed
    !=
persistent per-LBA verification ledger
    !=
permanent future-readability certificate
```

BMS later adds explicit progress/result state, but even BMS progress remains time-bounded maintenance evidence rather than timeless medium correctness.

### E4 — readable under drive ECC versus higher-layer semantic integrity

`BYTCHK=0` can exercise medium/error-code logic without a second application copy. That supports:

```text
medium readable under device verification
    !=
filesystem block checksum valid
    !=
application object semantically correct
    !=
replica version current
```

This is the same layer discipline already enforced by Case 101 versus ZFS/HDFS comparisons.

### E5 — command availability versus actual maintenance labor

A standard command can exist for years without telling us:

- which products implemented it;
- which operating systems exposed it;
- how often administrators invoked it;
- whether arrays used it for patrol operations;
- whether firmware converted it into a different internal sequence.

Therefore:

> **interface prior art != deployment-frequency evidence.**

---

## Functional analogy — bounded

A foreground VERIFY sweep and a BMS pass can be compared as two ways to **deliberately exercise medium state before ordinary application demand happens to encounter a latent problem**.

That is the useful functional overlap.

The analogy stops at the control boundary:

| Relation | Host-issued VERIFY | Device-side BMS |
|---|---|---|
| Who initiates this unit of work? | initiator / host-side command issuer | device-side background regime once enabled |
| Address/range selection | command provides LBA + length | device manages background traversal/coverage |
| Recurrence policy | outside the command | BMS control state / interval / idle rules |
| Progress state across a pass | not established by the command definition | explicit BMS status/progress |
| Dedicated result log | not established by VERIFY itself | Background Scan Results log |
| Byte comparison mode | part of VERIFY command semantics on supporting products | not the defining BMS relation |
| Historical genealogy | not established | not established |

This table is a functional comparison. It is not evidence that BMS descended directly from VERIFY or that `VERIFY` should be renamed `scrub`.

---

## Philosophical interpretation — bounded

The technical fact here is that **the same medium can be made epistemically available through different maintenance-control arrangements**.

A one-shot command creates evidence because an external initiator deliberately asks the drive to test a range. A background regime can retain enough policy/progress state to create similar evidence without a new foreground request for every range.

The bounded interpretive point is therefore about **where the obligation to renew confidence is retained**:

```text
host policy / command sequence
    versus
embedded device maintenance policy
```

This does not make `VERIFY` an archive, make BMS a form of human memory, or prove a continuous philosophical lineage from SCSI commands to later scrub systems.

---

## Prior-art consequence

This slice narrows one Case 101 novelty boundary.

Do **not** write:

> `T10 BMS introduced proactive disk verification in 2005.`

A safer formulation is:

> **T10's 2005 BMS work standardized a device-side background control/status regime for proactive medium scanning. SCSI had already exposed an initiator-issued direct-access VERIFY command by ANSI X3.131-1986, with named disk products documenting VERIFY behavior by at least 1988 and 1994.**

Even that sentence does not establish the complete pre-2005 scrub genealogy.

---

## Claims explicitly not established

Do not infer from this record that:

1. SCSI-1 invented media verification;
2. ANSI X3.131-1986 was the first interface to expose a verification operation;
3. every SCSI-1 disk implemented optional `VERIFY`;
4. every implementation supported both `BYTCHK=0` and `BYTCHK=1` behavior;
5. HP 9753 or Seagate ST3655 were the first shipping disks with VERIFY;
6. an OS performed periodic whole-disk scrub merely because VERIFY existed;
7. the OS-scanning statement in T10 `04-198r5` proves those scanners used VERIFY;
8. `BYTCHK=0` equals a filesystem checksum scrub;
9. `VERIFY` success is a permanent integrity or retention certificate;
10. command completion creates a persistent scan-progress ledger;
11. BMS is historically just `VERIFY in the background`;
12. BMS descended directly from the SCSI-1 VERIFY design;
13. foreground VERIFY and RAID-controller Patrol Read are one implementation family;
14. device ECC verification proves application data correctness;
15. reading/verifying a sector itself physically renews magnetic retention in the same sense as DRAM refresh or Flash rewrite.

---

## Related-repository boundary

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `SCSI VERIFY`, `Background Medium Scan`, and `Patrol Read` returned no dedicated packet in the current search surface.

The broader engineering history belongs there if pursued:

- SCSI-1/SCSI-2 VERIFY evolution;
- host utilities and OS scrub loops;
- controller use of VERIFY versus ordinary READ;
- RAID Patrol Read / Consistency Check genealogy;
- vendor-specific firmware behavior;
- performance and error-recovery policy.

`technical-retention` should keep only the retention-specific boundary: **verification primitive, coverage policy, retained progress/evidence, repair authority, and maintenance locus are different relations.**

---

## Remaining debt after this slice

This deepening closes only the narrow debt **`pre-2005 SCSI host-command verification primitive`**.

Still open:

- direct archival evidence for actual pre-2005 operating-system whole-disk scrub loops and which SCSI commands they issued;
- earlier pre-SCSI verify/read-check interfaces;
- SCSI-2/SBC normative evolution of VERIFY and error-recovery pages;
- named host utilities or RAID firmware that systematically tiled whole media with VERIFY before BMS;
- any direct documentary genealogy from VERIFY to T10 BMS;
- workload/performance measurements comparing host-driven VERIFY sweeps with device-local BMS;
- field tests showing what faults different VERIFY implementations actually surface.

These are broader-history questions and are not blockers for the bounded Case 101 result.

---

## Sources

### Primary / standards and archival

- T10, **X3T9.2 archives**, identifying the original SCSI standard as `X3.131:1986`: <https://www.t10.org/x3t9_2.htm>
- American National Standards Institute, **ANSI X3.131-1986, Small Computer System Interface (SCSI)**; surviving NBS/NIST federal-adoption copy as FIPS PUB 131: <https://nvlpubs.nist.gov/nistpubs/Legacy/FIPS/fipspub131.pdf>
- U.S. Government Publishing Office copy of the same FIPS/ANSI text, including indexed §8.2.6 `VERIFY Command`: <https://www.govinfo.gov/content/pkg/GOVPUB-C13-b974db668ca7572fe23cab4c248ef62b/pdf/GOVPUB-C13-b974db668ca7572fe23cab4c248ef62b.pdf>
- Hewlett-Packard, **_HP 9753XS/T/D SCSI Disk Drives_**, Edition 1, Rev. 12/20/88, §5-39 `Verify`: <https://bitsavers.org/pdf/hp/disc/scsi/5959-1412_9753XS_9753T_9753S_OEM_Dec88.pdf>
- Seagate Technology, **_ST3655 Family SCSI Drives Product Manual, Rev. A_**, Publication 36243-001, 18 January 1994, §3.5.6 / printed p. 67: <https://www.seagate.com/support/disc/manuals/scsi/3655npmb.pdf>
- T10, Gerry Houlder (Seagate), **`04-198r5 — Background Medium Scan`**, 9 March 2005: <https://www.t10.org/ftp/t10/document.04/04-198r5.pdf>
- T10, Rob Elliott (HP), **`05-340r3 — SBC-3 SPC-4 Background scan additions`**, 18 January 2006: <https://www.t10.org/ftp/t10/document.05/05-340r3.pdf>

### Internal links

- [`101-t10-2004-2007-background-medium-scan-grounding.md`](101-t10-2004-2007-background-medium-scan-grounding.md)
- [`101-dell-2005-2006-perc-patrol-read-controller-deepening.md`](101-dell-2005-2006-perc-patrol-read-controller-deepening.md)
- [`101-lsi-dell-2003-2006-patrol-read-documentation-lineage-deepening.md`](101-lsi-dell-2003-2006-patrol-read-documentation-lineage-deepening.md)
- [`../cases/14-scsi-disk-defect-reassignment-logical-identity.md`](../cases/14-scsi-disk-defect-reassignment-logical-identity.md)
- [`../cases/18-zfs-scrub-latent-error-detection.md`](../cases/18-zfs-scrub-latent-error-detection.md)
- [`../docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md`](../docs/SYNTHESIS_08_PROACTIVE_INTEGRITY_REPAIR_MARGIN.md)
- [`../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](../docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md)

---

## Result

**Bounded deepening complete.**

The source chain is strong enough to establish that SCSI exposed an initiator-driven direct-access VERIFY primitive by `X3.131-1986`; that the command already distinguished medium verification from host-data comparison; and that named HP (1988) and Seagate (1994) disk documentation shows real product-level VERIFY behavior before T10's 2005 BMS work.

The retention-specific consequence is narrow but useful:

```text
verification capability
    !=
coverage policy
    !=
retained background progress/evidence
    !=
repair authority
```

Case 101 therefore should treat 2005 BMS as a later **background-maintenance control/status regime**, not as the origin of medium verification. Actual pre-2005 host scrub policy/genealogy remains open.