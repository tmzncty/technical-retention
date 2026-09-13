# Case 36 Deepening — IBM FlashSystem 840 Named Commercial Retention Maintenance

## Purpose

This addendum deepens [`../cases/36-nand-flash-correct-and-refresh-maintenance.md`](../cases/36-nand-flash-correct-and-refresh-maintenance.md) at one deliberately narrow gap left open by the 2012 FCR case:

> Is there named commercial-product evidence that an enterprise Flash system automatically performs retention maintenance on data that the host has not rewritten, without thereby claiming that the product implements Cai et al.'s exact FCR algorithm?

**Result:** yes, at the manufacturer-documented product-contract level for IBM FlashSystem 840, with an earlier IBM Redbooks FlashSystem 720/820 sweeper witness as context. The sources are strong enough to establish a shipped-product retention-maintenance contract, but not enough to identify the controller algorithm with FCR, reconstruct the exact ECC/rewrite/remap path, or prove field behavior by independent fault injection.

This is therefore a **commercial-product implementation deepening**, not an FCR deployment claim.

Chronology/provenance deepening: [`36-ibm-flashsystem840-support-record-provenance-chronology-deepening.md`](36-ibm-flashsystem840-support-record-provenance-chronology-deepening.md) now separates the IBM Support record's `Original Publication Date` from the current page revision, current attachment, product-announcement, and GA dates. It closes the bounded interpretation of the page's `16 October 2013` field without inventing an exact first-publication date for the current PDF.

## Sources inspected

### A. IBM Support — `Flash Data Retention`

Current support landing page:

<https://www.ibm.com/support/pages/flash-data-retention>

Attached IBM PDF:

<https://www.ibm.com/support/pages/system/files/support/ssg/ssgdocs.nsf/0/e02429f9c68ec7ea85257c0600743ccd/$FILE/Flashsystem%20840%20Data%20Retention%20-%20External-6-6-14.pdf>

The landing page identifies the document as guidance about FlashSystem 840 / V840 retention behavior. The attached one-page IBM document directly states that extended persistence requires the storage system to be powered and operating normally, says Flash storage systems automatically refresh data even when the data have not been written or modified, gives a bounded FlashSystem 840 power-off envelope of up to 90 days at temperatures up to 40 °C, and says that after more than seven days powered off the installed 840 automatically starts a `deep scrub and refresh` process on return.

**Evidence class:** `H/P` for IBM's named-product contract and vocabulary; `E` only for the project-level separations derived below.

### B. IBM FlashSystem 840 product chronology

IBM hardware announcement record, dated 16 January 2014:

<https://www.ibm.com/docs/en/announcement_archive/ENUS114-032/ENUS114-032.PDF>

This announcement refers back to FlashSystem 840 hardware announcements dated 17 December 2013 and establishes the product-era chronology around early 2014. Current IBM lifecycle records independently give 24 January 2014 General Availability for 9840-AE1 and 9843-AE1.

**Chronology correction:** the current IBM Support record exposes `Original Publication Date: 16 October 2013`, while the current abstract names both FlashSystem 840 and V840 and the current attachment is named `External-6-6-14.pdf`. The dedicated provenance deepening shows that these are different chronological objects. The 16-October-2013 value is safe as IBM's current metadata for the **support record identity**, but it is not a secure publication date for the **current 840-specific PDF** or the current 840/V840 wording. IBM's 840 public-announcement references begin on 17 December 2013, the 840 lifecycle records give 24 January 2014 GA, and IBM publicly introduced V840 in February 2014. The attachment's `6-6-14` string is retained only as a date-coded filename/title because no inspected formal revision field defines it.

Therefore this addendum treats the attachment as a **2014 product-era IBM artifact** while leaving the exact first-publication date of the current PDF open. This is no longer described merely as a metadata `conflict`; it is a support-record-versus-current-revision provenance distinction.

### C. IBM Redbooks — FlashSystem 720 / 820 context

IBM Redbooks Product Guide, published 11 April 2013 and updated 13 October 2014:

<https://www.redbooks.ibm.com/redbooks.nsf/5193609f3941e9cf85256bc300724cfc/c7d2bf380cb6304f85257b3c0051f4a3>

The guide lists, among the Flash-module protection technologies, `Sweeper algorithms` that periodically read all data to avoid `data fade` issues. It separately lists ECC, checksums, overprovisioning, wear leveling, RAID protection, and battery-backed destaging of RAM buffers.

This is useful as an earlier named-commercial-system maintenance witness, but its wording directly establishes **periodic reading**, not a rewrite/remap refresh. It must not be promoted into an undocumented FlashSystem 720/820 FCR-style renewal mechanism.

**Evidence class:** `H/S` / institutional technical product guide; useful for commercial context and a negative boundary on what the wording does not establish.

### D. IBM Redbooks — `Implementing IBM FlashSystem 840`

IBM Redbooks, SG24-8189-02, published 9 July 2015:

<https://www.redbooks.ibm.com/abstracts/sg248189.html>

PDF:

<https://www.redbooks.ibm.com/redbooks/pdfs/sg248189.pdf>

The implementation guide repeats the operator-level relation that the enclosure should remain powered or be powered periodically to retain array consistency, gives the same up-to-90-day / up-to-40 °C safe power-off envelope, and warns that data might be lost after a longer power-off interval.

**Evidence class:** `H/S` as a later IBM institutional continuity / operating-guidance witness. It is not used to infer undocumented controller internals.

## Historical record

### Named product behavior, not a research-only mechanism

The strongest change to Case 36 is not a new physical model. It is the evidence class.

Cai et al. 2012 grounds an explicit research proposal/evaluation for retention-aware correction and renewal. IBM's FlashSystem 840 document instead names a commercial storage system and describes automatic retention maintenance as an operating property of that system. In IBM's own wording, host inactivity does not imply retention inactivity: data can be automatically refreshed despite not being written or modified by the host.

This is sufficient to establish:

> **named commercial Flash system != maintenance-free merely because the payload is host-unchanged**.

It is not sufficient to establish:

> **FlashSystem 840 implements Cai et al.'s FCR algorithm**.

The IBM document does not expose the FCR-specific combination of P/E-adaptive cadence, ECC threshold policy, in-place reprogramming, right-shift-error fallback, and remapping policy described in the 2012 paper.

### Power-off interval is a product contract, not a raw-cell constant

The IBM 840 document gives a system-level power-off envelope: up to 90 days at temperatures up to 40 °C. That is a product/operational qualification statement over the whole storage system, not a universal NAND-cell retention law.

Therefore:

> **system power-off envelope != raw NAND intrinsic-retention constant**.

The same document says the system has recovery methods for conditions beyond that envelope. That blocks a second overclaim:

> **crossing 90 days != a sourced deterministic timestamp at which every payload bit is lost**.

The documentation changes the risk/qualification relation; it does not define a universal cliff at day 91.

### Restart can begin retention work before ordinary steady state

For an installed FlashSystem 840 that has been powered off longer than seven days, IBM says startup automatically initiates a `deep scrub and refresh` process. This establishes a machine-defined off-duration threshold that changes what maintenance work is owed after power returns.

The useful decomposition is:

```text
payload physically survives power-off
    !=
power is restored
    !=
retention-maintenance debt is zero
    !=
deep scrub / refresh begins
    !=
maintenance completes / system returns to optimal condition
```

The source does not provide enough detail here to reconstruct exact block selection, ECC thresholds, rewrite geometry, or completion telemetry.

### `deep scrub and refresh` must retain IBM's own scope

IBM's phrase should not be normalized into Ceph, HDFS, ZFS, or another storage system's `scrub` semantics. The 840 document itself couples `deep scrub` with `refresh`, which is already enough to show that its named operation is not safely reducible to `verification only`; however, the internal relation between scanning, correction, rewriting, remapping, and controller metadata is not exposed by this source.

Therefore:

> **same word `scrub` != same historical mechanism**.

And:

> **IBM `deep scrub and refresh` != fully reconstructed refresh algorithm**.

## Engineering reconstruction

### Host quiescence and retention work are independent dimensions

A host can leave a logical payload untouched while the storage system performs internal maintenance on its physical embodiment. This adds a named-product witness to a relation already visible in Case 36's research regime:

> **host write history != complete physical-renewal history**.

The logical value may stay unchanged while controller activity renews or requalifies the embodiment that continues to serve it.

### Nonvolatility and maintenance opportunity remain separate

The 840 can retain data during a bounded period without input power, yet IBM still recommends powered normal operation for extended retention and automatically performs refresh after sufficiently long power-off intervals.

Thus:

> **power-off survivability != indefinite maintenance-free reliable retention**.

This does not turn NAND into DRAM. It means a nonvolatile medium can participate in a system whose long-horizon reliability contract depends on later powered maintenance opportunity.

### Automatic maintenance is not customer rewrite

The 840 document explicitly removes customer intervention from the post-power-off deep-scrub/refresh path. The relevant retention work is controller/system activity, not an application rewrite requirement.

Therefore:

> **automatic retention maintenance != host/application rewrite obligation**.

### Commercial evidence does not reveal physical algorithm identity

A manufacturer can expose an operational retention contract while hiding the exact physical/control mechanism. The 840 source tells us **that** automatic refresh occurs and **when** one post-power-off path is triggered, but not exactly **how** the Flash cells, ECC engine, FTL mappings, spare blocks, or read references are manipulated.

This makes the evidence boundary itself useful:

> **named-product feature contract != transparent controller mechanism**.

The mechanism remains partially opaque even when the maintenance policy is no longer a research-only proposal.

## Prior-art / chronology consequence

This addendum does not change the pre-2012 prior-art conclusions already grounded in [`36-flash-refresh-1997-2009-prior-art-deepening.md`](36-flash-refresh-1997-2009-prior-art-deepening.md). Patent records still establish that generic nonvolatile refresh, age/timer/error triggers, relocation/remapping, and erase-free rewrite refresh predate FCR.

The new contribution is instead an **evidence-class bridge**:

```text
pre-2012 public refresh disclosures
    !=
2012 FCR research proposal/evaluation
    !=
2013 FlashSystem 720/820 periodic-read sweeper product documentation
    !=
2014-era FlashSystem 840 automatic refresh + post-off deep-scrub/refresh product documentation
```

No arrow in that chain is asserted as a direct design genealogy.

The FlashSystem 720/820 Redbook is especially useful as a stop condition: it directly documents periodic reads to avoid data fade, but not enough to infer rewrite renewal. The later 840 document uses stronger `refresh` language, but still does not identify the algorithm with FCR.

The chronology/provenance deepening adds a separate methodological rule:

> **support-record original-publication metadata != exact publication date of every current attachment/revision**.

That rule protects the prior-art boundary from accidentally moving the commercial-product evidence floor backward to October 2013 on the basis of an untyped support-page metadata field.

## Functional analogies and limits

### FCR comparison

Functional analogy:

- both the 2012 FCR proposal and the 840 product guidance treat long-horizon recoverability as something that can depend on powered background maintenance rather than host mutation;
- both make `nonvolatile` compatible with an active reliability-maintenance regime.

Stop condition:

- FCR exposes ECC/error thresholds, in-place reprogram/remap alternatives, P/E-adaptive scheduling, and evaluated endurance trade-offs;
- the IBM 840 guidance exposes a product-level operational policy and trigger but not those internals;
- no direct FCR -> FlashSystem 840 genealogy is established.

### Distributed/file-system scrub comparison

Functional analogy:

- a background operation can examine retained state outside immediate host demand.

Stop condition:

- HDFS, Ceph, ZFS, and IBM FlashSystem use different object models, integrity evidence, repair authority, physical media, and implementation histories;
- `deep scrub` is not one universal storage operation.

### Philosophical limit

The technical fact creates a modest conceptual pressure: a state can be materially nonvolatile while the **continued institutional/service promise that it remain reliably recoverable** depends on later maintenance windows, controller policy, and product operating conditions.

That is a project-level interpretation. IBM's support document is not evidence that IBM engineers were making a philosophical claim about memory, temporality, or technical retention.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| IBM documents automatic refresh of Flash data even when host data are not written or modified | H/P | IBM `Flash Data Retention` attachment |
| FlashSystem 840 has a documented safe power-off envelope of up to 90 days at up to 40 °C | H/P | IBM `Flash Data Retention` attachment; later Redbooks continuity |
| After more than seven days powered off, an installed FlashSystem 840 automatically starts a `deep scrub and refresh` process | H/P | IBM `Flash Data Retention` attachment |
| The 840 process requires no customer intervention according to IBM | H/P | same attachment |
| FlashSystem 720/820 documentation lists periodic-read sweeper algorithms intended to avoid data fade | H/S | IBM Redbooks Product Guide, 11-Apr-2013 / updated 13-Oct-2014 |
| FlashSystem 720/820 sweeper wording proves a rewrite/remap refresh algorithm | X | source establishes periodic reading, not rewrite renewal |
| FlashSystem 840 implements Cai et al.'s exact FCR algorithm | X | no algorithm-identity or genealogy evidence in inspected product sources |
| 90 days at 40 °C is a universal raw-NAND retention constant | X | IBM statement is a named-system operating/qualification envelope |
| Day 91 implies deterministic total data loss | X | IBM instead describes recovery methods beyond the stated envelope |
| IBM currently reports `Original Publication Date: 16-Oct-2013` for support record `ssg1S7004533` | H/P | current IBM Support record |
| `16-Oct-2013` securely dates the current 840-specific PDF or current 840/V840 abstract | X | dedicated provenance deepening shows record metadata and current revision/attachment are different chronological objects |
| `External-6-6-14` is independently authenticated as the PDF's formal publication date | X | it is a date-coded artifact filename/title; exact formal publication chronology remains unresolved |
| Commercial-product maintenance contract != independent field validation | E/X | manufacturer behavior is documented; controlled independent validation remains open |

## Related-repository audit

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `FlashSystem 840` and for Flash-refresh/NAND-retention material returned no dedicated case to reuse. The division of labor therefore remains:

- broader Texas Memory Systems -> IBM FlashSystem device/controller genealogy, FPGA/data-path history, and exact refresh implementation should primarily be developed in `computing-archaeology`;
- the retention-specific relation between nonvolatile embodiment, powered maintenance opportunity, product qualification envelope, automatic refresh, logical continuity, and source-controlled evidence dating belongs here.

This addendum does not assert that the 720/820 and 840 maintenance mechanisms form one uninterrupted engineering lineage merely because IBM documentation places them in adjacent product generations.

## Remaining open work

- **bounded chronology interpretation closed:** `16-Oct-2013` is support-record original-publication metadata, not a secure date for the current PDF/current abstract; see [`36-ibm-flashsystem840-support-record-provenance-chronology-deepening.md`](36-ibm-flashsystem840-support-record-provenance-chronology-deepening.md);
- exact first-publication date / formal document-control history of the current `External-6-6-14` attachment remains open;
- an archived 2013 snapshot of support UID `ssg1S7004533` would be needed to recover its original title/body/attachment with confidence;
- firmware/source-level reconstruction of `deep scrub and refresh`;
- whether the 840 path used in-place reprogramming, remapping, read-reference adaptation, ECC-threshold policy, or some combination;
- independent named-product observation/fault validation of the refresh path;
- broader commercial-controller refresh comparison outside the IBM/TMS family;
- later 3-D NAND / QLC commercial refresh behavior and telemetry;
- direct genealogy, if any, between pre-2012 refresh disclosures, FCR, TMS/IBM product mechanisms, and later commercial controllers.

## Sources

1. IBM Support, **`Flash Data Retention`**, current landing page and attached FlashSystem 840 product document: <https://www.ibm.com/support/pages/flash-data-retention>.
2. IBM, **`Flashsystem 840 Data Retention - External-6-6-14.pdf`**, one-page product-era support attachment: <https://www.ibm.com/support/pages/system/files/support/ssg/ssgdocs.nsf/0/e02429f9c68ec7ea85257c0600743ccd/$FILE/Flashsystem%20840%20Data%20Retention%20-%20External-6-6-14.pdf>.
3. IBM United States Hardware Announcement 114-032, 16 January 2014, with references to the 17-December-2013 FlashSystem 840 product announcements: <https://www.ibm.com/docs/en/announcement_archive/ENUS114-032/ENUS114-032.PDF>.
4. IBM product lifecycle, FlashSystem 840 9840-AE1: <https://www.ibm.com/support/pages/node/7094794>.
5. IBM product lifecycle, FlashSystem 840 9843-AE1: <https://www.ibm.com/support/pages/node/7092436>.
6. Ilya Krutov, **`IBM FlashSystem 720 and IBM FlashSystem 820`**, IBM Redbooks Product Guide, published 11 April 2013, updated 13 October 2014: <https://www.redbooks.ibm.com/redbooks.nsf/5193609f3941e9cf85256bc300724cfc/c7d2bf380cb6304f85257b3c0051f4a3>.
7. Karen Orlando et al., **`Implementing IBM FlashSystem 840`**, IBM Redbooks SG24-8189-02, published 9 July 2015: <https://www.redbooks.ibm.com/abstracts/sg248189.html>.
8. IBM Storage announcement/blog, **`Fall In Love with IBM FlashSystem V840 Enterprise Performance Solution`**, 11 February 2014: <https://community.ibm.com/community/user/blogs/tony-pearson1/2014/02/11/fall-in-love-with-ibm-flashsystem-v840-enterprise-performance-solution>.
