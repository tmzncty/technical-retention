# NAND Flash Correct-and-Refresh: ECC-Bounded Retention Through Controller Maintenance

## Status

**`grounded`** — bounded to Yu Cai et al.'s peer-reviewed 2012 ICCD proposal and evaluation of **Flash Correct-and-Refresh (FCR)** for 3x-nm MLC NAND Flash, with later 2015 retention-characterization work used only as a boundary check on retention-age/read-recovery semantics. The historical novelty boundary is additionally deepened by pre-2012 nonvolatile-memory refresh patent records from 1978–2009; those records narrow what can safely be attributed to FCR without changing the case's bounded 2012 object.

Grounding record: [`../evidence/36-cai-2012-flash-correct-refresh-grounding.md`](../evidence/36-cai-2012-flash-correct-refresh-grounding.md).

Earlier prior-art deepening: [`../evidence/36-1978-1994-nonvolatile-flash-refresh-prior-art-deepening.md`](../evidence/36-1978-1994-nonvolatile-flash-refresh-prior-art-deepening.md).

Prior-art deepening: [`../evidence/36-flash-refresh-1997-2009-prior-art-deepening.md`](../evidence/36-flash-refresh-1997-2009-prior-art-deepening.md).

Commercial-product deepening: [`../evidence/36-ibm-flashsystem840-2014-2015-commercial-refresh-deepening.md`](../evidence/36-ibm-flashsystem840-2014-2015-commercial-refresh-deepening.md).

## Scope

This case asks a narrow question left open by Cases 04, 13, and 15:

> What changes when a physically nonvolatile Flash medium is treated as requiring periodic controller/software maintenance in order to keep accumulated retention errors inside an ECC-qualified reliability margin?

The 2012 FCR paper proposes three related controller/software policies:

- **remapping-based FCR** — read a valid block, correct accumulated errors with ECC, program corrected data to a free block, and remap the logical address;
- **hybrid reprogramming/remapping FCR** — usually restore charge in place, but remap when accumulated right-shift/program errors become too large;
- **adaptive-rate FCR** — change refresh cadence as block wear / P/E-cycle count changes rather than assuming one fixed interval for the entire device lifetime.

This is **not**:

- evidence that all NAND Flash or all SSDs require the same refresh policy;
- evidence that the proposed FCR algorithms were commercially deployed exactly as simulated;
- a claim that Flash is physically volatile in the DRAM sense;
- a claim that Flash `refresh` and DRAM refresh are the same historical mechanism;
- a general history of NAND reliability, ECC, read-retry, LDPC, 3D NAND, or SSD firmware;
- an invention-priority claim for Flash refresh.

The bounded object is the **2012 FCR proposal/evaluation as an explicit retention-maintenance regime**.

## Historical vocabulary and record

The primary paper is Yu Cai, Gulay Yalcin, Onur Mutlu, Erich F. Haratsch, Adrian Cristal, Osman S. Unsal, and Ken Mai, **“Flash Correct-and-Refresh: Retention-Aware Error Management for Increased Flash Memory Lifetime,”** presented at the 30th IEEE International Conference on Computer Design (ICCD), Montreal, September 2012, pp. 94–101, DOI `10.1109/ICCD.2012.6378623`.

Its own vocabulary includes:

- `retention errors`;
- `Flash Correct-and-Refresh (FCR)`;
- `remapping-based FCR`;
- `in-place reprogramming`;
- `hybrid FCR`;
- `adaptive-rate FCR`;
- `program/erase (P/E) cycles`;
- `raw BER (RBER)` / `uncorrectable BER (UBER)`;
- `error correcting codes (ECC)`;
- `flash translation layer (FTL)`;
- `wear leveling` and `garbage collection`.

The authors characterize retention errors as errors caused when an already-programmed floating-gate cell gradually loses charge and its threshold-voltage state can cross a read-reference boundary. In their measured 3x-nm MLC population, retention error rate increases with retention time and P/E wear, and the paper treats retention errors as the dominant error class in that bounded experimental regime.

The central proposal is explicit: periodically **read, correct, and refresh** stored data before accumulated retention errors exceed the correction capability of the selected ECC. `Refresh` in this paper means either reprogramming or remapping, not a DRAM row-restore command.

## Retained state and constitutive control state

The bounded FCR regime contains several separable states:

1. **cell state** — threshold-voltage / charge distributions encoding MLC values;
2. **logical payload** — the error-corrected page/block value presented by the SSD;
3. **ECC margin** — how many raw errors can still be corrected before UBER violates the target;
4. **mapping / validity state** — which physical block currently embodies the logical address and which blocks contain valid data;
5. **wear state** — per-block P/E-cycle counts used by adaptive-rate FCR and already maintained for wear leveling;
6. **maintenance policy state** — which blocks need refresh and at what rate.

`ECC margin`, `maintenance policy state`, and `retention qualification` are project reconstruction terms. They are not presented as period vocabulary.

## Engineering reconstruction

### Nonvolatility does not guarantee maintenance-free reliable retention

The Flash cell remains physically nonvolatile: power is not required merely to prevent immediate disappearance of the programmed state. Yet the paper's mechanism begins from a different requirement — keeping raw retention errors below an ECC-bounded reliability threshold over a desired service interval.

Therefore:

> **nonvolatile medium ≠ maintenance-free reliable retention at a specified error target**.

This does not redefine Flash as volatile. It separates **unpowered physical persistence** from **continued system-level recoverability with a bounded error budget**.

### Raw-state degradation can precede logical data loss

The paper explicitly places ECC between raw Flash reads and host-visible corrected data. Retention errors can accumulate in the physical readout while the controller still reconstructs the correct logical page.

Therefore:

> **raw physical error accumulation ≠ immediate logical payload loss**.

But the same relation creates a deadline of another kind: once accumulated errors outrun ECC capability, the page may no longer be recoverable by that path.

Thus:

> **ECC-correctability margin ≠ indefinite retention margin**.

FCR acts before that margin is exhausted.

### Long logical retention can be composed from shorter physical-retention intervals

The paper gives a deliberately concrete model result: with its examined 3x-nm MLC data and a fixed 512-bit BCH code, a much shorter guaranteed storage interval permits many more P/E cycles than a three-year interval. It uses the example of refreshing every three days to synthesize a much longer logical storage requirement.

The numerical values are **experiment/model specific**, not universal NAND laws. The retention relation is more general:

> **long logical retention interval ≠ one uninterrupted physical-embodiment interval**.

Repeated correction and rewriting can make the later logical state depend on a sequence of shorter, renewed physical embodiments.

### Flash refresh can preserve identity by changing location

In remapping-based FCR the controller:

1. selects valid data needing refresh;
2. reads it page by page;
3. corrects accumulated errors with ECC;
4. programs the corrected data into a new free block;
5. remaps the logical address.

Therefore:

> **retention maintenance ≠ location stability**.

This directly extends Case 04. Case 04 grounds relocation under rewrite/reclamation pressure; Case 36 adds a different trigger — **retention-error margin** — for deliberately replacing the physical embodiment while preserving logical identity.

### `Refresh` is not one physical operation

The paper itself contrasts NAND with DRAM. Its remapping path rewrites corrected payload into another erased block. Its in-place path instead uses ISPP to add charge back to cells whose retention error came from charge loss.

Therefore:

> **Flash FCR `refresh` ≠ DRAM refresh**.

The shared word names a functional goal — restore usable state before loss — while the substrate constraints, granularity, controller role, rewrite geometry, and side effects differ.

### Maintenance can consume the lifetime it is trying to extend

Periodic remapping creates additional erase cycles because old blocks eventually become reclaimable. The paper explicitly observes an inflection point for some workloads where increasing remap frequency can reduce lifetime.

Therefore:

> **more maintenance ≠ more lifetime**.

A retention operation can spend endurance in order to preserve error margin.

The in-place path exposes a second counterexample. Reprogramming can correct left-shift retention errors by adding charge, but it can also create program-interference errors and cannot repair right-shift errors requiring charge removal. Hybrid FCR therefore monitors right-shift error count and falls back to remapping when the threshold is exceeded.

Hence:

> **maintenance operation ≠ error-neutral repair**.

Retention work can create a different failure mechanism while suppressing the original one.

### Refresh cadence can depend on retained wear history

Adaptive-rate FCR starts with no refresh while retention errors remain inside the selected ECC margin, then increases refresh frequency as P/E cycles accumulate. The paper notes that per-block P/E-cycle information is already maintained for wear leveling.

Therefore:

> **refresh cadence ≠ one fixed medium constant**.

And:

> **payload retention can depend on retained maintenance metadata**.

The system needs a remembered wear relation in order to decide how much future retention work to perform.

### Maintenance competes with ordinary service and requires power

The paper says FCR requires powered Flash, can run with lower priority or during idle periods, and can be interrupted to reduce response-time impact.

Thus the proposed persistence is not a free background property. It consumes controller time, Flash operations, energy, and a service window.

## Failure and forgetting boundaries

Within this bounded regime, loss can occur through several distinct paths:

- charge leakage and threshold-voltage drift increase raw retention errors;
- ECC can mask/correct those errors until its capability is exceeded;
- remap-based refresh can consume additional erase/endurance budget;
- in-place reprogramming can introduce program-interference errors;
- a refresh policy that is too slow can allow correctability margin to expire;
- a refresh policy that is too aggressive can spend endurance or create new errors;
- powered-controller maintenance cannot execute while the device remains unpowered;
- losing mapping/validity/wear metadata would undermine the policy even if payload charge still exists.

Forgetting is therefore not one event. In this case it can be **physical drift beyond a recoverable threshold**, **loss of the logical-currentness relation**, or **failure of the maintenance regime to renew error margin in time**.

## Prior art and anti-anachronism

The 2012 paper includes a bounded authorial priority statement (“to our knowledge”) about its combination of retention-error characteristics. A dedicated prior-art deepening now makes the repository's boundary much firmer: [`../evidence/36-flash-refresh-1997-2009-prior-art-deepening.md`](../evidence/36-flash-refresh-1997-2009-prior-art-deepening.md) documents public pre-2012 records for several mechanisms that must **not** be treated as FCR inventions.

A 1997-filed / 1999-public U.S. patent already describes multilevel nonvolatile-memory refresh in response to threshold-voltage drift/error evidence, including ECC participation, deferred/idle-time refresh, periodic timer-driven refresh, retained last-refresh time, power-up refresh, and sector buffer→erase→rewrite. A separate 2000-filed / 2002-public Flash patent family describes dynamic refresh that can move data to a different physical location while an address-mapping circuit changes the logical/virtual→physical mapping. A 2005-public record describes age/timestamp-triggered in-place or out-of-place Flash refresh, and a 2007-filed / 2009-public record describes erase-free reprogram refresh triggered by elapsed time, level drift, or read-error evidence.

Therefore the repository rejects all of the following as FCR novelty claims:

- `generic nonvolatile-memory refresh first appears in FCR`;
- `periodic / idle-time / power-up Flash refresh first appears in FCR`;
- `ECC/error-assisted refresh first appears in FCR`;
- `refresh-time relocation/remapping first appears in FCR`;
- `retention-age/timestamp-triggered Flash refresh first appears in FCR`;
- `erase-free reprogram refresh first appears in FCR`.

The surviving bounded distinction is narrower: Cai et al. combine measured 3x-nm MLC retention-error characterization with explicit storage-time / P/E-wear / ECC trade-offs, remapping and in-place paths, hybrid fallback for the opposite/right-shift error population, per-block P/E-cycle-driven adaptive refresh rate, and SSD/workload simulation that makes the maintenance/endurance trade-off quantitative.

This is a **combination/evaluation boundary**, not an invention-priority judgment. Patent filing/priority date is also kept separate from public publication date. Patent disclosure does not prove commercial deployment, and functional similarity does not prove a patent-family → FCR design genealogy.

Nor does this project project the FCR term backward onto the earlier records. Their own terms — `refresh`, `dynamic refresh`, `refresh timer`, `address mapping`, `storage date`, and `rewrite refresh` — remain historical vocabulary. `FCR` is used historically only for the 2012 proposal and its later descendants/citations where explicitly sourced.

### Earlier public refresh floor — 1978–1994

A separate earlier-prior-art addendum, [`../evidence/36-1978-1994-nonvolatile-flash-refresh-prior-art-deepening.md`](../evidence/36-1978-1994-nonvolatile-flash-refresh-prior-art-deepening.md), closes the bounded `pre-1997 nonvolatile-memory refresh` debt. A 1978-filed / 1980-public Matsushita patent describes natural-decay warning plus capture/erase/rewrite for a specific MNOS nonvolatile-memory embodiment; it is **not** treated as Flash. A 1990-filed / 1993-public Intel patent then explicitly describes blocked Flash EPROM refresh after program/erase disturbance, including a margin-sensitive scan and same-location reprogramming. A 1992-filed / 1994-public Texas Instruments patent independently describes flash EEPROM refresh through two-level margin tests, restorative program pulses, optional sector capture/erase/rewrite, and erase-cycle/time triggers.

This moves the conservative inspected public floor backward while adding counterexamples that matter more than the date itself:

- **nonvolatile != drift-free**;
- **Flash refresh != necessarily retention-age-triggered**;
- **Flash refresh != necessarily relocation/remapping**;
- **one word `refresh` != one physical rewrite geometry**;
- **maintenance trigger state != payload state**;
- **on-chip/interface-invisible maintenance != maintenance-free**.

The earlier records do not establish commercial deployment, NAND/SSD identity, direct influence on FCR, or invention priority. FCR remains distinct as a 2012 measured/evaluated 3x-nm MLC NAND policy combination coupling storage time, P/E wear, ECC capability, hybrid renewal choices, and workload simulation.

A 2015 follow-up by Cai et al. characterizes retention age in real 2y-nm MLC NAND and shows that optimal read-reference voltage changes with retention age. That later evidence deepens the general point that retained charge, readable interpretation, and controller recovery parameters can diverge over time. It is not used to rewrite either the pre-2012 patent mechanisms or the 2012 FCR mechanism, and it does not establish deployment.
## Named commercial-product deepening — IBM FlashSystem 840

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

## Functional analogy and philosophical limit

A bounded analogy to DRAM is useful only at this level:

> both systems can make later recoverability depend on maintenance before an error/decay boundary is crossed.

The analogy stops immediately after that functional relation. DRAM refresh is constitutive periodic restoration of volatile dynamic-cell state; FCR is a proposed controller/software reliability policy over a nonvolatile, erase/endurance-constrained medium with ECC and remapping.

The case creates one narrow conceptual pressure:

> A substrate may be called nonvolatile while a particular **reliability-qualified continuation relation** over that substrate becomes operational and maintenance-dependent.

That is an engineering/philosophical interpretation. It is not evidence that the 2012 authors were making a philosophical claim about persistence.

## Cross-case result

Case 36 extends the Flash/SSD comparison as follows:

```text
floating-gate charge state
    !=
raw readout / retention-error population
    !=
ECC-correctable logical payload
    !=
remaining correction margin
    !=
refresh-cadence decision
    !=
read + correction
    !=
in-place charge restoration OR remap to new embodiment
    !=
updated mapping / wear state
    !=
restored future correction margin
```

It also separates proactive retention renewal from integrity scrubbing. ZFS/GFS cases use verification to discover whether retained copies are already inconsistent/corrupt; FCR is triggered by a model/policy aimed at **preventing time/wear-dependent raw error accumulation from outrunning ECC**. The operations can both be background scans, but their failure models and repair semantics are not identical.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Cai et al. presented FCR at ICCD 2012 | H/P | peer-reviewed primary paper + institutional bibliographic records |
| FCR periodically reads, ECC-corrects, then reprograms in place or remaps before retention errors exceed ECC capability | H/P | abstract + §§I, IV |
| Remapping FCR programs corrected data to a new free block and changes the logical mapping | H/P | §IV.A / Fig. 3 |
| In-place reprogramming restores charge without erase for the bounded retention-error direction | H/P | §IV.B / Fig. 4 |
| In-place reprogramming can create program-interference errors and cannot repair the opposite/right-shift error direction | H/P | §IV.B / Fig. 5 |
| Hybrid FCR uses error evidence to decide when to remap instead of continuing in-place reprogramming | H/P | §IV.B / Fig. 6 |
| Adaptive-rate FCR changes refresh frequency with P/E cycles and reuses per-block wear information | H/P | §IV.C–D |
| More frequent remapping can reduce lifetime because it adds erase cycles | H/P/E | §IV.A + evaluation discussion |
| FCR requires power and can be scheduled as background/idle work | H/P | §IV.D |
| A 1978-filed / 1980-public record already describes natural-decay-triggered nonvolatile-memory renewal through warning, temporary capture, erase, and rewrite | H/P | US4218764A; specific embodiment is MNOS, not asserted as Flash |
| A 1990-filed / 1993-public Intel record explicitly describes Flash EPROM refresh after high-voltage operation disturbance and can reprogram the same location | H/P | US5239505A |
| A 1992-filed / 1994-public TI record independently describes flash EEPROM refresh, margin-sensitive restoration, sector reconstruction, and erase-cycle/time triggers | H/P | US5365486A |
| Pre-2012 public records already describe periodic/deferred/power-up nonvolatile-memory refresh with error/ECC participation | H/P | US5909449A (1999 public record; 1997 filing) |
| Pre-2012 public records already describe refresh that relocates data and changes logical-to-physical mapping | H/P | US6396744B1 / 2000 priority family |
| Pre-2012 public records already describe age/timestamp-triggered in-place or out-of-place Flash refresh | H/P | US20050243626A1 / US7325090B2 |
| Pre-2012 public records already describe erase-free reprogram refresh triggered by time, drift, or read-error evidence | H/P | US20090161466A1 |
| Generic Flash refresh, refresh-time remapping, or erase-free rewrite refresh is an invention unique to FCR | X | contradicted by inspected pre-2012 patent records |
| Similarity between earlier patent mechanisms and FCR proves direct design genealogy or commercial deployment | X | neither influence chain nor shipped implementation is established by this slice |
| IBM documents automatic refresh of FlashSystem 840 data even when host data are not written or modified | H/P | IBM product-era `Flash Data Retention` attachment |
| An installed 840 powered off longer than seven days can automatically enter `deep scrub and refresh` after return | H/P | IBM product-era `Flash Data Retention` attachment |
| The 840 up-to-90-day / up-to-40 °C power-off envelope is a universal raw-NAND retention law | X | the source gives a named-system operating/qualification relation, not a medium-wide cell constant |
| FlashSystem 840 proves commercial deployment of Cai et al.'s exact FCR algorithm | X | product behavior is documented, but algorithm identity/genealogy is not established |
| The reported 46× average lifetime improvement proves a production SSD achieved 46× measured field life | X | the paper reports simulation driven by measured characterization/workload data, not a multi-year production deployment |
| FCR proves all NAND Flash requires periodic refresh | X | outside the bounded 3x-nm MLC proposal/evaluation |
| NAND FCR refresh is historically or physically identical to DRAM refresh | X | paper itself distinguishes the mechanisms |

## Related repositories

Current inspection of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) finds broad Flash/controller history still listed as an area to deepen, not a dedicated FCR retention case to reuse. A general NAND-controller reliability history belongs there; this repository keeps the retention-specific comparison among nonvolatility, ECC margin, refresh trigger, remapping, and endurance.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the anti-anachronism rule: the 2012 authors' `Flash Correct-and-Refresh` vocabulary is historical; `reliability-qualified continuation` and `maintenance metadata` remain modern analytical terms.

## Sources

1. Yu Cai, Gulay Yalcin, Onur Mutlu, Erich F. Haratsch, Adrian Cristal, Osman S. Unsal, Ken Mai, **“Flash Correct-and-Refresh: Retention-Aware Error Management for Increased Flash Memory Lifetime,”** *30th IEEE International Conference on Computer Design (ICCD)*, Montreal, September 2012, pp. 94–101, DOI `10.1109/ICCD.2012.6378623`. Author-hosted paper: <https://users.ece.cmu.edu/~omutlu/pub/flash-correct-and-refresh_iccd12.pdf>.
2. ETH Zurich Systems Group publication record for the same ICCD 2012 paper: <https://publications.systems.ethz.ch/publication/791>.
3. Carnegie Mellon KiltHub record, posted 1 October 2012, preserving the abstract and evaluation boundary: <https://kilthub.cmu.edu/articles/journal_contribution/Flash_Correct-and-Refresh_Retention-Aware_Error_Management_for_Increased_Flash_Memory_Lifetime/6468821>.
4. Yu Cai, Yixin Luo, Erich F. Haratsch, Ken Mai, Onur Mutlu, **“Data Retention in MLC NAND Flash Memory: Characterization, Optimization, and Recovery,”** *HPCA 2015*, pp. 551–563, DOI `10.1109/HPCA.2015.7056062`; used only as later retention-age/read-recovery boundary evidence: <https://www.istc-cc.cmu.edu/publications/papers/2015/flash-memory-data-retention_hpca15_abs.shtml>.
5. Hock C. So and Sau C. Wong, **“Multibit-per-cell non-volatile memory with error detection and correction,”** US 5,909,449 A, filed 8 September 1997, public patent 1 June 1999: <https://patents.google.com/patent/US5909449A/en>.
6. **“Flash memory with dynamic refresh,”** US 6,396,744 B1, filed 25 April 2000, public patent 28 May 2002; same family includes relocation/address-mapping refresh records: <https://patents.google.com/patent/US6396744B1/en>.
7. **“Refreshing data stored in a flash memory,”** US 2005/0243626 A1 / US 7,325,090 B2, priority 29 April 2004, application publication 3 November 2005: <https://patents.google.com/patent/US7325090B2/en>.
8. Darlene G. Hamilton, Mark W. Randolph, Don Carlos Darling, Ron Kornitz, **“Extending flash memory data retension via rewrite refresh,”** US 2009/0161466 A1, filed 20 December 2007, published 25 June 2009: <https://patents.google.com/patent/US20090161466A1/en>.
9. IBM Support, **`Flash Data Retention`**, current landing page and FlashSystem 840 product attachment: <https://www.ibm.com/support/pages/flash-data-retention>.
10. IBM, **`Flashsystem 840 Data Retention - External-6-6-14.pdf`**, product-era support attachment: <https://www.ibm.com/support/pages/system/files/support/ssg/ssgdocs.nsf/0/e02429f9c68ec7ea85257c0600743ccd/$FILE/Flashsystem%20840%20Data%20Retention%20-%20External-6-6-14.pdf>.
11. Ilya Krutov, **`IBM FlashSystem 720 and IBM FlashSystem 820`**, IBM Redbooks Product Guide, published 11 April 2013, updated 13 October 2014: <https://www.redbooks.ibm.com/redbooks.nsf/5193609f3941e9cf85256bc300724cfc/c7d2bf380cb6304f85257b3c0051f4a3>.
12. Karen Orlando et al., **`Implementing IBM FlashSystem 840`**, IBM Redbooks SG24-8189-02, published 9 July 2015: <https://www.redbooks.ibm.com/abstracts/sg248189.html>.
13. Yukio Furuta and Tomisaburo Okumura, **“Non-volatile memory refresh control circuit,”** US 4,218,764 A, filed 3 October 1978, published/granted 19 August 1980, Matsushita Electric Industrial Co., Ltd.: <https://patents.google.com/patent/US4218764A/en>.
14. Albert Fazio, Gregory E. Atwood, and Neal R. Mielke, **“Floating gate non-volatile memory with blocks and memory refresh,”** US 5,239,505 A, filed 28 December 1990, published/granted 24 August 1993, Intel Corporation: <https://patents.google.com/patent/US5239505A/en>.
15. John F. Schreck, **“Method and circuitry for refreshing a flash electrically erasable, programmable read only memory,”** US 5,365,486 A, filed 16 December 1992, published/granted 15 November 1994, Texas Instruments Incorporated: <https://patents.google.com/patent/US5365486A/en>.
