# Case 100 Grounding — Dirty-Region Prior Art, ZFS DTL Patent Family, and Selective Resilver

**Case:** [`../cases/100-zfs-dirty-time-log-selective-resilver.md`](../cases/100-zfs-dirty-time-log-selective-resilver.md)

**Status:** `grounded`

## Purpose

This record grounds a narrow retention relation:

> a ZFS dirty time log can preserve transaction-time / birth-time evidence about incomplete replication, allowing later resilver logic to focus on blocks exposed during those intervals instead of treating all surviving state as equally in need of repair.

It also preserves an explicit prior-art boundary: spatial dirty-region logs provided selective mirrored-volume recovery before the ZFS DTL family. The record does not claim invention priority, universal release behavior, or integrity proof from DTL membership.

---

## Source A — Sun Cluster 2.2 Dirty Region Logging

Oracle-preserved Sun documentation:

<https://docs.oracle.com/cd/E19957-01/806-2329/ch2admin-39382/index.html>

Title: **Sun Cluster 2.2 Cluster Volume Manager Guide**, §2.1.4 `Dirty Region Logging and CVM`.

### A1. Historical record

The guide describes DRL as an optional mirrored-volume feature for faster recovery after system failure. It says DRL:

- divides a volume into consecutive regions;
- keeps a status bit for each region;
- marks regions dirty before the corresponding data write proceeds;
- synchronously writes a newly dirty log entry before the data write;
- on restart recovers only regions marked dirty rather than the entire mirror.

### A2. Grounded use

This is a manufacturer/platform-primary prior-art witness for selective recovery via retained **spatial dirty-state metadata**.

### A3. Limit

Do not rename DRL as DTL. Do not infer direct genealogy merely because both reduce resynchronization work. Exact DRL product genealogy belongs in `computing-archaeology`.

---

## Source B — Sun/Oracle ZFS DTL patent family chronology

Family overview / related applications:

<https://patents.google.com/patent/US8938594B2/en>

The application records benefit of provisional application **60/734,023**, filed **2005-11-04**, titled `Dirty Time Logging and Resilvering`, in the names of William H. Moore and Jeffrey S. Bonwick. It identifies related applications for dirty time logging, DTL-directed resilvering, and pruned resilvering. The corresponding U.S. application publications appeared **2007-05-10**.

### B1. Grounded use

Use **2005-11-04** as a bounded priority/documentary floor for this Sun design family and **2007-05-10** as the public application witness.

### B2. Limit

Patent priority is not a `first shipping` date and does not establish that every described embodiment appeared in the same product release.

---

## Source C — `Method and system for dirty time logging`

<https://patents.google.com/patent/US7925827B2/en>

Publication lineage includes application `US20070106869A1`, published **2007-05-10**.

### C1. Historical record

The application describes attempting to store a data/indirect block associated with a birth time and updating a DTL with that birth time if storage on a disk is unsuccessful.

Related family description explains that DTL entries can represent time with transaction-group numbers and can retain the interval during which a disk was offline / did not successfully receive I/O.

### C2. Grounded use

DTL is evidence of **incomplete replication over transaction time**, not simply a region bitmap and not a complete operation log.

### C3. Limit

The patent describes embodiments and claimed methods. It is not independent product-compliance evidence.

---

## Source D — DTL-directed and pruned resilver

- DTL-directed resilver: <https://patents.google.com/patent/US7930495B2/en>
- pruned resilver: <https://patents.google.com/patent/US8635190B2/en>

### D1. Historical record

The pruned-resilver application describes a hierarchical block tree in which block pointers contain birth time. It traverses a branch only when the parent birth-time relation means descendants could still intersect the DTL and resilvers a child when the DTL contains that child's birth time.

The worked example assigns DTL transaction groups / birth times 32–37 to an offline interval and treats blocks outside that interval as not requiring resilvering in the described model.

### D2. Grounded use

This directly supports:

- temporal repair selection;
- block birth time as repair-membership metadata;
- subtree pruning as a consequence of retained temporal bounds;
- `repair scope history ≠ complete write history`.

### D3. Prior-art language inside the patent

The pruned-resilver description explicitly discusses conventional dirty region logging, including the tradeoff between fine regions/logging overhead and coarse regions/excess recovery work.

Therefore the source itself blocks a naïve `DTL invented selective recovery` story.

---

## Source E — Oracle Solaris ZFS Administration Guide: operational resilver witness

Oracle documentation:

<https://docs.oracle.com/cd/E26505_01/html/E37384/gbbba.html>

### E1. Historical / product record

The guide states that ZFS resilvers only the minimum amount of necessary data. It contrasts a short outage with full device replacement and says the latter takes time proportional to used data.

### E2. Grounded use

This supplies a product-level behavioral witness that selective catch-up is not confined to patent prose.

### E3. Limits

The guide does not expose every internal DTL data structure and does not license a universal performance multiplier. `minutes or seconds` is an example/context statement, not a service guarantee for arbitrary pools.

---

## Source F — OpenZFS 2.1.11 `vdev.c`: later implementation continuity

Debian source view of OpenZFS 2.1.11:

<https://sources.debian.org/src/zfs-linux/2.1.11-1%2Bdeb12u1/module/zfs/vdev.c>

Around the DTL comment in `vdev.c`, the source says:

- a vdev DTL is the set of transaction groups for which it has less than perfect replication;
- `DTL_MISSING`: no valid copies on the vdev for those txgs;
- `DTL_PARTIAL`: data available but not fully replicated;
- `DTL_SCRUB`: txgs the last scrub could not repair;
- `DTL_OUTAGE`: txgs that cannot currently be read and generally computed only when needed;
- leaf `DTL_MISSING` maps are sufficient to derive parent/other DTL state;
- only that sufficient leaf missing-state basis is kept on disk, with other DTLs regenerated after load/configuration changes.

### F1. Grounded use

This later implementation witness sharpens two distinctions:

1. **repair-history state has types** — missing, partial, scrub and current outage are not one boolean;
2. **persistent basis ≠ every derived maintenance classification** — a smaller durable basis can regenerate higher-level state.

### F2. Limit

This is release/source-specific continuity. It must not be used to assert that the 2005 provisional or every Solaris release had the exact 2.1.11 class set and persistence implementation.

---

## Related-repository duplication check

A GitHub code search during this slice found no dedicated `DTL` / `resilver` match in `tmzncty/computing-archaeology`.

Use that narrowly. It is not proof that no adjacent mirror/RAID history exists there.

Division of labor:

- broad DRL → dirty-log → ZFS implementation genealogy, controller history, and rebuild algorithms: `computing-archaeology`;
- bounded retention relation among transaction-time exposure evidence, block birth time, repair selection, and later metadata retirement: Case 100 here.

---

## Claim ledger

| Claim | Type | Evidence | Status / limit |
| --- | --- | --- | --- |
| pre-ZFS Sun DRL records dirty spatial regions and limits mirror recovery to them | `H/P` | Source A | grounded prior-art floor |
| Sun ZFS DTL/resilver family claims 2005-11-04 provisional priority | `H/P` | Source B | chronology only; not first deployment |
| a block birth time can be retained in DTL when storage on one disk is unsuccessful | `H/P` | Source C | patent/design witness |
| DTL time may be represented by transaction-group number | `H/P` | Sources C–D | bounded to described embodiments |
| pruned resilver uses DTL/birth relations to select blocks and skip irrelevant branches | `H/P` | Source D | grounded design relation; not universal release implementation |
| Solaris ZFS product docs expose minimum-necessary-data resilver after short outage | `H/P` | Source E | qualitative product witness |
| modern OpenZFS 2.1.11 calls DTL txgs of less-than-perfect replication | `H/P` | Source F | later continuity only |
| modern OpenZFS persists only a sufficient leaf missing-state basis and derives other DTL state | `H/P/E` | Source F | implementation/version-specific |
| DTL is a complete write-history archive | `X` | mechanism/source boundary | rejected |
| DTL membership is checksum/corruption proof | `X` | Sources D, F + Case 18 comparison | rejected |
| ZFS invented selective mirror resynchronization | `X` | Source A + D prior-art discussion | rejected |
| DRL chronology proves direct DRL→DTL genealogy | `X` | none | unsupported |

---

## Controlled conclusions

1. **repair-scope history can remain after the failure event itself has ended**;
2. **failure-exposure history ≠ complete payload/mutation history**;
3. **spatial dirty-region evidence ≠ transaction-time DTL evidence**;
4. **block birth metadata + retained DTL interval can authorize exclusion from repair work**;
5. **selective resilver ≠ scrub/integrity verification**;
6. **temporary-outage catch-up ≠ blank replacement-device reconstruction**;
7. **temporal pruning of repair scope ≠ dRAID sequential reconstruction geometry**;
8. **small retained maintenance metadata can eliminate large amounts of unnecessary future I/O**;
9. **payload survival ≠ survival of the evidence required for efficient repair**;
10. **a persistent minimal basis may regenerate derived maintenance state** in the bounded later OpenZFS implementation;
11. **earlier DRL blocks an invention claim without proving direct genealogy**.
