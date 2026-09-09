from pathlib import Path
import re

ROOT = Path('.')
EVIDENCE_PATH = ROOT / 'evidence/36-ibm-flashsystem840-2014-2015-commercial-refresh-deepening.md'
CASE_PATH = ROOT / 'cases/36-nand-flash-correct-and-refresh-maintenance.md'
ROADMAP_PATH = ROOT / 'ROADMAP.md'
INDEX_PATH = ROOT / 'CASE_INDEX.md'

EVIDENCE = r'''# Case 36 Deepening — IBM FlashSystem 840 Named Commercial Retention Maintenance

## Purpose

This addendum deepens [`../cases/36-nand-flash-correct-and-refresh-maintenance.md`](../cases/36-nand-flash-correct-and-refresh-maintenance.md) at one deliberately narrow gap left open by the 2012 FCR case:

> Is there named commercial-product evidence that an enterprise Flash system automatically performs retention maintenance on data that the host has not rewritten, without thereby claiming that the product implements Cai et al.'s exact FCR algorithm?

**Result:** yes, at the manufacturer-documented product-contract level for IBM FlashSystem 840, with an earlier IBM Redbooks FlashSystem 720/820 sweeper witness as context. The sources are strong enough to establish a shipped-product retention-maintenance contract, but not enough to identify the controller algorithm with FCR, reconstruct the exact ECC/rewrite/remap path, or prove field behavior by independent fault injection.

This is therefore a **commercial-product implementation deepening**, not an FCR deployment claim.

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

This announcement refers back to FlashSystem 840 hardware announcements dated 17 December 2013 and establishes the product-era chronology around early 2014.

**Chronology caveat:** the current IBM Support landing page for `Flash Data Retention` displays `Original Publication Date: 16 October 2013`, while the attached file name contains `External-6-6-14` and the FlashSystem 840 product announcement chronology is later than October 2013. The repository therefore does **not** use the landing-page date as a secure publication date for the 840-specific PDF. This addendum conservatively treats the attachment as a **2014 product-era IBM artifact**, with the landing-page metadata retained only as a provenance inconsistency that should not be silently normalized.

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
| IBM Support landing-page `Original Publication Date` securely dates the 840-specific PDF to 16-Oct-2013 | X | current metadata conflicts with the 840 product chronology and the attachment file name; exact publication chronology remains unresolved |
| Commercial-product maintenance contract != independent field validation | E/X | manufacturer behavior is documented; controlled independent validation remains open |

## Related-repository audit

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `FlashSystem 840` and for Flash-refresh/NAND-retention material returned no dedicated case to reuse. The division of labor therefore remains:

- broader Texas Memory Systems -> IBM FlashSystem device/controller genealogy, FPGA/data-path history, and exact refresh implementation should primarily be developed in `computing-archaeology`;
- the retention-specific relation between nonvolatile embodiment, powered maintenance opportunity, product qualification envelope, automatic refresh, and logical continuity belongs here.

This addendum does not assert that the 720/820 and 840 maintenance mechanisms form one uninterrupted engineering lineage merely because IBM documentation places them in adjacent product generations.

## Remaining open work

- exact public/provenance chronology of the 840 `Flash Data Retention` attachment;
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
4. Ilya Krutov, **`IBM FlashSystem 720 and IBM FlashSystem 820`**, IBM Redbooks Product Guide, published 11 April 2013, updated 13 October 2014: <https://www.redbooks.ibm.com/redbooks.nsf/5193609f3941e9cf85256bc300724cfc/c7d2bf380cb6304f85257b3c0051f4a3>.
5. Karen Orlando et al., **`Implementing IBM FlashSystem 840`**, IBM Redbooks SG24-8189-02, published 9 July 2015: <https://www.redbooks.ibm.com/abstracts/sg248189.html>.
'''

CASE_SECTION = r'''## Named commercial-product deepening — IBM FlashSystem 840

A new evidence addendum, [`../evidence/36-ibm-flashsystem840-2014-2015-commercial-refresh-deepening.md`](../evidence/36-ibm-flashsystem840-2014-2015-commercial-refresh-deepening.md), closes part of the case's long-standing `commercial deployment` evidence gap without claiming that FCR itself was deployed.

IBM's product-era `Flash Data Retention` guidance for FlashSystem 840 states that Flash storage systems automatically refresh data even when the host has not written or modified it. For an installed 840 powered off longer than seven days, IBM describes an automatic `deep scrub and refresh` process after power returns; the same document gives a bounded safe power-off envelope of up to 90 days at temperatures up to 40 °C and describes recovery attempts beyond that envelope.

This changes the evidence class available to the repository:

> **research refresh proposal/evaluation != named commercial-product retention-maintenance contract**.

But the boundary is equally important:

> **named commercial-product refresh != documented deployment of Cai et al.'s exact FCR algorithm**.

The IBM source does not expose FCR's specific P/E-adaptive cadence, right-shift-error threshold, in-place-versus-remap decision, or controller ECC policy. It therefore grounds **that** automatic retention maintenance existed in a named commercial system while leaving **how** the internal refresh path worked only partially visible.

The product guidance also sharpens four separations:

- **host-unchanged payload != internally unmaintained payload** — IBM explicitly allows refresh without a host write;
- **bounded power-off nonvolatility != indefinite service-level retention** — the 840 has a product-qualified off/temperature envelope while extended retention is tied to powered normal operation;
- **crossing a qualification envelope != deterministic erasure timestamp** — IBM describes recovery methods beyond the 90-day / 40 °C conditions rather than a universal day-91 cliff;
- **power restored != maintenance debt already discharged** — a sufficiently long off interval can cause post-return deep scrub/refresh work.

An IBM Redbooks FlashSystem 720/820 product guide, published 11 April 2013, provides a useful adjacent commercial witness by listing sweeper algorithms that periodically read all data to avoid `data fade`. That wording directly establishes periodic read maintenance but **not** rewrite/remap renewal. It is therefore context, not proof that the earlier systems implemented FCR-style refresh.

Chronology is source-controlled. IBM's current support landing page shows an `Original Publication Date` of 16 October 2013, but the attached file is named `External-6-6-14` and the 840 product announcement chronology falls around December 2013 / January 2014. The repository therefore treats the attachment conservatively as a **2014 product-era artifact** and does not silently convert the landing-page metadata into a secure PDF publication date.

Finally, IBM's historical phrase `deep scrub and refresh` is not normalized into Ceph/HDFS/ZFS `scrub` semantics. The comparison is functional only: background inspection/maintenance can occur outside immediate host demand. The object models, integrity evidence, repair authority, physical mechanisms, and genealogies differ.
'''

ROADMAP_BULLET = r'''- [x] Case 36 named-commercial Flash retention-maintenance deepening — [`cases/36-nand-flash-correct-and-refresh-maintenance.md`](cases/36-nand-flash-correct-and-refresh-maintenance.md), with new [`evidence/36-ibm-flashsystem840-2014-2015-commercial-refresh-deepening.md`](evidence/36-ibm-flashsystem840-2014-2015-commercial-refresh-deepening.md), now adds a manufacturer-documented shipped-product bridge beyond the 2012 FCR research proposal: IBM's product-era FlashSystem 840 guidance says unchanged data can be automatically refreshed and that a system returning after more than seven days powered off automatically starts `deep scrub and refresh`; it also gives an up-to-90-day / up-to-40 °C safe power-off envelope. IBM Redbooks' 11-Apr-2013 FlashSystem 720/820 guide supplies an adjacent periodic-read `sweeper` / `data fade` witness but is not promoted into undocumented rewrite refresh. This closes only the bounded **named commercial-product automatic retention maintenance exists** relation. It does **not** establish Cai-et-al.-FCR deployment, exact 840 controller/ECC/remap internals, deterministic loss at day 91, raw-NAND universal retention, or independent field/fault validation. The current IBM support landing-page `Original Publication Date` conflicts with the 840 product chronology and its `External-6-6-14` attachment name, so exact attachment-publication chronology remains open; broader controller/product genealogy belongs primarily in `computing-archaeology`.
'''

INDEX_SECTION = r'''## Case 36 deepening — IBM FlashSystem 840 commercial-product retention-maintenance findings

Evidence: [`evidence/36-ibm-flashsystem840-2014-2015-commercial-refresh-deepening.md`](evidence/36-ibm-flashsystem840-2014-2015-commercial-refresh-deepening.md)

- **2475 — support-page metadata date != securely dated product attachment.** IBM's current landing page displays `Original Publication Date: 16 October 2013`, but the 840-specific attachment is named `External-6-6-14` and the product announcement chronology is later than October 2013; the repository therefore treats the PDF as a 2014 product-era witness rather than silently backdating it. (`H/P`, `X`)
- **2476 — named commercial-product refresh != FCR algorithm deployment.** IBM documents automatic FlashSystem 840 retention maintenance, but the inspected product sources do not identify P/E-adaptive FCR, the in-place/remap decision, right-shift-error thresholding, or an FCR genealogy. (`H/P`, `X`)
- **2477 — host-unchanged payload != internally unmaintained payload.** IBM explicitly says Flash data can be automatically refreshed even when not written or modified by the host. (`H/P`, `E`)
- **2478 — bounded power-off nonvolatility != indefinite service-level retention.** The 840 has a documented safe-off envelope of up to 90 days at temperatures up to 40 °C while IBM still ties extended persistence to powered normal operation. (`H/P`, `E`)
- **2479 — product power-off envelope != raw NAND retention constant.** The 90-day / 40 °C relation is a named-system operating/qualification statement over controller, media, firmware, and recovery behavior, not a universal cell-physics law. (`H/P`, `E`, `X`)
- **2480 — crossing the 90-day envelope != deterministic day-91 erasure.** IBM describes recovery methods for conditions beyond the stated envelope; the source does not establish a universal cliff where every payload is lost. (`H/P`, `X`)
- **2481 — power restored != retention-maintenance debt already discharged.** After more than seven days powered off, IBM says an installed 840 automatically starts a `deep scrub and refresh` process on return. (`H/P`, `E`)
- **2482 — automatic retention maintenance != customer/application rewrite obligation.** IBM describes the post-off deep-scrub/refresh path as automatic and not requiring customer intervention. (`H/P`, `E`)
- **2483 — IBM `deep scrub and refresh` != verification-only scrub.** The vendor's own compound phrase makes renewal part of the named path, but the source still does not expose the exact scan/correction/rewrite/remap sequence. (`H/P`, `E`, `X`)
- **2484 — same word `scrub` != same mechanism or genealogy.** IBM FlashSystem, HDFS, Ceph, and ZFS background operations can be compared functionally, but their media, integrity evidence, object models, repair authority, and histories differ. (`A`, `X`)
- **2485 — manufacturer product contract != transparent controller mechanism.** The 840 evidence establishes that automatic refresh occurs and a post-off trigger exists while leaving ECC thresholds, read-reference adaptation, physical rewrite geometry, and mapping behavior opaque. (`H/P`, `E`)
- **2486 — periodic-read sweeper != demonstrated rewrite refresh.** IBM Redbooks' 11-Apr-2013 FlashSystem 720/820 guide directly documents periodic reads to avoid `data fade`, but it does not by itself establish payload rewrite/remap renewal or a direct lineage into the 840 mechanism. (`H/S`, `X`)
- **2487 — related-repository nonduplication remains explicit.** Fresh `computing-archaeology` searches found no dedicated FlashSystem 840 or Flash-refresh/NAND-retention case; broader TMS/IBM device/controller genealogy stays routed there, while the product-level retention relation is kept here. (`H/P` project-state record)
'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one anchor, found {count}')
    return text.replace(old, new, 1)


def write_if_changed(path: Path, text: str) -> None:
    normalized = text.rstrip() + '\n'
    if not path.exists() or path.read_text(encoding='utf-8') != normalized:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(normalized, encoding='utf-8')


# 1. Add the evidence record.
if EVIDENCE_PATH.exists():
    existing = EVIDENCE_PATH.read_text(encoding='utf-8')
    if existing.rstrip() != EVIDENCE.rstrip():
        raise RuntimeError(f'{EVIDENCE_PATH} already exists with different content')
else:
    write_if_changed(EVIDENCE_PATH, EVIDENCE)

# 2. Deepen the canonical Case 36 narrative and claim ledger.
case = CASE_PATH.read_text(encoding='utf-8')
prior_link = 'Prior-art deepening: [`../evidence/36-flash-refresh-1997-2009-prior-art-deepening.md`](../evidence/36-flash-refresh-1997-2009-prior-art-deepening.md).'
commercial_link = 'Commercial-product deepening: [`../evidence/36-ibm-flashsystem840-2014-2015-commercial-refresh-deepening.md`](../evidence/36-ibm-flashsystem840-2014-2015-commercial-refresh-deepening.md).'
if commercial_link not in case:
    case = replace_once(case, prior_link, prior_link + '\n\n' + commercial_link, 'Case 36 evidence link')

section_anchor = '\n## Functional analogy and philosophical limit\n'
if '## Named commercial-product deepening — IBM FlashSystem 840' not in case:
    case = replace_once(case, section_anchor, '\n' + CASE_SECTION.rstrip() + '\n\n## Functional analogy and philosophical limit\n', 'Case 36 commercial section')

claim_anchor = '| Similarity between earlier patent mechanisms and FCR proves direct design genealogy or commercial deployment | X | neither influence chain nor shipped implementation is established by this slice |'
claim_rows = '\n'.join([
    '| IBM documents automatic refresh of FlashSystem 840 data even when host data are not written or modified | H/P | IBM product-era `Flash Data Retention` attachment |',
    '| An installed 840 powered off longer than seven days can automatically enter `deep scrub and refresh` after return | H/P | IBM product-era `Flash Data Retention` attachment |',
    '| The 840 up-to-90-day / up-to-40 °C power-off envelope is a universal raw-NAND retention law | X | the source gives a named-system operating/qualification relation, not a medium-wide cell constant |',
    '| FlashSystem 840 proves commercial deployment of Cai et al.\'s exact FCR algorithm | X | product behavior is documented, but algorithm identity/genealogy is not established |',
])
if claim_rows.split('\n')[0] not in case:
    case = replace_once(case, claim_anchor, claim_anchor + '\n' + claim_rows, 'Case 36 claim ledger')

source_marker = '8. Darlene G. Hamilton, Mark W. Randolph, Don Carlos Darling, Ron Kornitz, **“Extending flash memory data retension via rewrite refresh,”** US 2009/0161466 A1, filed 20 December 2007, published 25 June 2009: <https://patents.google.com/patent/US20090161466A1/en>.'
extra_sources = '\n'.join([
    '9. IBM Support, **`Flash Data Retention`**, current landing page and FlashSystem 840 product attachment: <https://www.ibm.com/support/pages/flash-data-retention>.',
    '10. IBM, **`Flashsystem 840 Data Retention - External-6-6-14.pdf`**, product-era support attachment: <https://www.ibm.com/support/pages/system/files/support/ssg/ssgdocs.nsf/0/e02429f9c68ec7ea85257c0600743ccd/$FILE/Flashsystem%20840%20Data%20Retention%20-%20External-6-6-14.pdf>.',
    '11. Ilya Krutov, **`IBM FlashSystem 720 and IBM FlashSystem 820`**, IBM Redbooks Product Guide, published 11 April 2013, updated 13 October 2014: <https://www.redbooks.ibm.com/redbooks.nsf/5193609f3941e9cf85256bc300724cfc/c7d2bf380cb6304f85257b3c0051f4a3>.',
    '12. Karen Orlando et al., **`Implementing IBM FlashSystem 840`**, IBM Redbooks SG24-8189-02, published 9 July 2015: <https://www.redbooks.ibm.com/abstracts/sg248189.html>.',
])
if extra_sources.split('\n')[0] not in case:
    case = replace_once(case, source_marker, source_marker + '\n' + extra_sources, 'Case 36 sources')
write_if_changed(CASE_PATH, case)

# 3. Record the completed bounded slice in ROADMAP.
roadmap = ROADMAP_PATH.read_text(encoding='utf-8')
if 'Case 36 named-commercial Flash retention-maintenance deepening' not in roadmap:
    roadmap_anchor = '- [x] DRAM power-off remanence / gradual-decay boundary'
    idx = roadmap.find(roadmap_anchor)
    if idx < 0:
        raise RuntimeError('ROADMAP insertion anchor not found')
    roadmap = roadmap[:idx] + ROADMAP_BULLET + '\n' + roadmap[idx:]
write_if_changed(ROADMAP_PATH, roadmap)

# 4. Update the authoritative Case 36 row and append new controlled findings.
index = INDEX_PATH.read_text(encoding='utf-8')
lines = index.splitlines()
row_indexes = [i for i, line in enumerate(lines) if line.startswith('| [NAND Flash Correct-and-Refresh:')]
if len(row_indexes) != 1:
    raise RuntimeError(f'CASE_INDEX Case 36 row count is {len(row_indexes)}')
lines[row_indexes[0]] = '| [NAND Flash Correct-and-Refresh: ECC-Bounded Retention Through Controller Maintenance](cases/36-nand-flash-correct-and-refresh-maintenance.md) | **grounded** | nonvolatile MLC NAND + retention-error accumulation + ECC-corrected read + remap/in-place reprogram + adaptive controller scheduling + named commercial automatic maintenance witness | separate physical nonvolatility from maintenance-free reliable retention; show error-margin renewal can relocate state and consume endurance; bound FCR novelty against earlier refresh prior art; separate named-product maintenance from FCR algorithm identity | [2012 FCR grounding](evidence/36-cai-2012-flash-correct-refresh-grounding.md) + [1997–2009 refresh prior-art deepening](evidence/36-flash-refresh-1997-2009-prior-art-deepening.md) + [IBM FlashSystem 840 commercial-product deepening](evidence/36-ibm-flashsystem840-2014-2015-commercial-refresh-deepening.md); manufacturer-documented automatic retention maintenance is now grounded, while exact FCR deployment, controller internals, independent product validation, pre-1997 prior art, later 3D-NAND/read-retry interaction, and full controller genealogy remain separate work |'
index = '\n'.join(lines).rstrip() + '\n'

if '## Case 36 deepening — IBM FlashSystem 840 commercial-product retention-maintenance findings' not in index:
    ids = [int(m.group(1)) for m in re.finditer(r'\*\*(\d+)\s+—', index)]
    if not ids or max(ids) != 2474:
        raise RuntimeError(f'Expected latest finding 2474 before append; got {max(ids) if ids else None}')
    for n in range(2475, 2488):
        if re.search(rf'\*\*{n}\s+—', index):
            raise RuntimeError(f'Finding {n} already exists')
    index = index.rstrip() + '\n\n' + INDEX_SECTION.rstrip() + '\n'
write_if_changed(INDEX_PATH, index)

# 5. Canonical consistency checks.
for path in [EVIDENCE_PATH, CASE_PATH, ROADMAP_PATH, INDEX_PATH]:
    data = path.read_text(encoding='utf-8')
    if '\r' in data:
        raise RuntimeError(f'CR character found in {path}')
    if not data.endswith('\n'):
        raise RuntimeError(f'missing terminal newline: {path}')

assert 'commercial-product deepening' in CASE_PATH.read_text(encoding='utf-8')
assert '2475 — support-page metadata date' in INDEX_PATH.read_text(encoding='utf-8')
assert '2487 — related-repository nonduplication' in INDEX_PATH.read_text(encoding='utf-8')
print('Case 36 IBM FlashSystem commercial-retention deepening applied.')
