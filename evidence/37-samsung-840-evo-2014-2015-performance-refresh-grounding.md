# Case 37 Grounding — Samsung 840 EVO Old-Data Performance Restoration, 2014–2015

## Purpose

This record grounds [`../cases/37-samsung-840-evo-old-data-performance-refresh.md`](../cases/37-samsung-840-evo-old-data-performance-refresh.md) as a bounded commercial Flash/SSD retention-maintenance case.

The evidence target is intentionally narrower than a NAND-retention history:

> establish that Samsung shipped a product-specific old-data performance-restoration path in 2014, then publicly described a 2015 840 EVO firmware algorithm as using periodic refresh; separate payload correctness, read-recovery cost, physical rewrite, powered maintenance opportunity, and read-performance continuity.

## Evidence classes

### A. Manufacturer-primary surviving artifacts

#### Samsung 840 EVO support page — October 2014 restoration packages

Current Samsung support for the 840 EVO 1TB (`MZ-7TE1T0`) retains a download ledger that includes:

- 28 October 2014 — Update Software v1.0, DOS, including Performance Restoration ISO/USB artifacts;
- 24 October 2014 — Update Software v1.1 for Windows, with the note that users who already restored performance with v1.0 do not need to run v1.1.

The exact current page is:

<https://www.samsung.com/us/business/support/owners/product/840-evo-series-1tb/>

What this proves:

- Samsung shipped a named, product-specific **Performance Restoration** path in October 2014;
- it was not merely a community workaround or later recollection;
- Samsung treated restoration as a special firmware/software service event for the 840 EVO.

What it does **not** prove by itself:

- the detailed internal algorithm;
- that every 840 EVO unit suffered the issue;
- that the 2014 action provided a lasting future maintenance policy;
- a general Samsung/TLC genealogy.

#### Samsung Magician 5.2.1 Installation Guide — June 2018

Directly inspected manufacturer PDF:

<https://semiconductor.samsung.com/resources/data-sheet/Samsung_Magician_5_2_1_Installation_Guide_v2.4.pdf>

Revision 2.4, June 2018, printed page 7 / PDF page 7, `General Limitations → Performance Optimization` states:

- Advanced Performance Optimization takes more time to complete;
- performance improvement may depend on the user's system environment;
- Advanced Performance Optimization is supported only on Samsung SSD 840 EVO (2.5-inch, mSATA) and 840 Series models;
- Windows may experience slow response while Advanced Performance Optimization is in progress on one specifically named controller/driver environment.

What this proves:

- the named Advanced Performance Optimization function remained a vendor-recognized special function for the 840 EVO / 840 family;
- the operation consumes visible service time and can have foreground-response cost.

Boundary:

- this 2018 guide is **later continuity evidence**, not the exact April 2015 Magician 4.6 implementation specification;
- it cannot be used to infer the 2015 firmware's internal data-placement or read-reference algorithm.

### B. Contemporary direct-vendor statements preserved by independent technical reporting

No currently accessible Samsung-hosted 2014/2015 FAQ with the full explanation was found in this round. The historical explanation is therefore preserved through period independent technical publications that explicitly attribute the statements to Samsung.

#### October 2014 Samsung explanation, preserved by The SSD Review

Scot Strong, `Samsung Announces Firmware Update To Resolve 840 EVO Performance Degradation`, 15 October 2014:

<https://www.thessdreview.com/daily-news/latest-buzz/samsung-announces-firmware-update-resolve-840-evo-performance-degradation/>

The article reproduces Samsung's contemporaneous account. The attributable propositions are:

1. the old-data performance drop was associated with an error in the 840 EVO `flash management software algorithm`;
2. SSDs normally calibrate changes in cell status over time through flash-management software;
3. the faulty algorithm caused the 840 EVO to perform read-retry aggressively, lowering overall read performance;
4. the symptom was associated with data left in its initial cells rather than subsequently migrated/overwritten data;
5. Samsung's restoration software restored read performance by rewriting old data;
6. Samsung framed the issue as read-performance degradation rather than data loss or drive-reliability loss.

Evidence label: **H/S with direct-vendor quotation provenance**. These are Samsung-attributed historical statements, but the surviving page is an independent publication rather than a Samsung primary document.

The same article shows the named `SAMSUNG SSD 840 EVO PERFORMANCE RESTORATION v.1.0` workflow and links to Samsung's download site as it existed at the time, strengthening continuity with the surviving Samsung support artifacts above.

### C. April 2015 direct Samsung Q&A and independent behavior tests

Allyn Malventano, `Samsung Magician 4.6 and 840 EVO EXT0DB6Q Firmware Review – Finally Fixed`, *PC Perspective*, 14 April 2015:

<https://pcper.com/2015/04/samsung-magician-4-6-and-840-evo-ext0db6q-firmware-review-finally-fixed/>

#### Samsung Q&A propositions

PC Perspective states that the Q&A was conducted with Samsung while the new firmware and beta Magician 4.6 were being tested. Samsung's published answers establish:

1. Samsung revised the firmware algorithm to maintain performance consistency for old data under exceptional circumstances;
2. the algorithm was **based on a periodic refresh feature** intended to maintain the read performance of older data;
3. Samsung said the algorithm could operate without Magician;
4. Samsung explicitly said the algorithm **does not operate when power is off**;
5. if the SSD had insufficient run-time for the firmware algorithm, or had been powered off for an extended time, **Advanced Performance Optimization** in Magician 4.6 could recover performance;
6. Samsung described Advanced Performance Optimization as a supplementary feature for those exceptional circumstances;
7. users who had never run the earlier Performance Restoration tool could upgrade directly to the new firmware through Magician 4.6;
8. in that Q&A Samsung said the issue had been reported for the 840 EVO SSD only.

Evidence label: **H/S with direct-vendor Q&A provenance**.

Important wording boundary:

- `periodic refresh feature` is Samsung's own product-era term as preserved in the Q&A;
- `maintenance opportunity`, `retrieval-performance retention`, and `powered maintenance backlog` are project reconstruction terms.

#### PC Perspective empirical boundary

On the test-results page, PC Perspective reports that a stale-data benchmark run **immediately after the firmware update** — before the drive had time to perform background refresh — already showed a large improvement. The reviewer then says it *appears* Samsung also changed the read algorithm to adapt better to drifted cells. After Advanced Optimization, performance improved further.

Evidence label:

- immediate performance improvement before background refresh: **H/S, empirical review observation**;
- exact interpretation that Samsung changed the read-reference algorithm: **S/E inference**, not manufacturer-confirmed implementation detail.

This distinction is central. The experiment blocks the shortcut:

> `all 2015 improvement = background rewriting`.

But it does **not** provide source-level proof of the exact read-threshold/calibration algorithm.

The same review notes a methodological problem: writing test data itself refreshes/renews data and therefore changes the state being measured. That is useful bounded evidence that measurement and maintenance can interact in Flash-retention experiments.

## Chronology

### September 2014 — public old-data slowdown investigation

PC Perspective documents old-data read slowdown and publishes Samsung's acknowledgement that a firmware fix is being qualified. Community/reviewer observations are discovery evidence, not used here as a substitute for Samsung's later mechanism statements.

### 15–28 October 2014 — one-time restoration regime

Samsung's public explanation attributes the problem to flash-management/read-retry behavior and says rewriting old data restores performance. Samsung publishes Performance Restoration v1.0/v1.1 artifacts. The surviving support page still carries those October 2014 files.

This phase supports:

> **rewrite renewal can restore service performance while preserving the same logical data**.

It does not establish a durable future maintenance policy.

### By April 2015 — recurrence and revised maintenance regime

PC Perspective reports stale samples slowing again after the first attempted fix. Samsung's new Q&A describes a revised firmware algorithm based on periodic refresh and explicitly introduces a power-off boundary plus Advanced Performance Optimization fallback.

This supports:

> **one-time restoration ≠ continuing maintenance closure**.

### June 2018 — vendor documentation continuity

Samsung's Magician 5.2.1 guide still gives Advanced Performance Optimization special 840 EVO/840 scope. This confirms that the named maintenance operation remained in Samsung's own product software documentation after the incident.

## Mechanism claims and evidence strength

| Claim | Evidence class | Strength / boundary |
| --- | --- | --- |
| Samsung shipped product-specific Performance Restoration software in October 2014 | manufacturer-primary support/download ledger | strong |
| 2014 cause was described by Samsung as flash-management algorithm / aggressive read-retry on old once-written data | direct Samsung statement preserved in period independent publication | strong historical attribution; surviving document is secondary host |
| 2014 restoration rewrote old data | direct Samsung statement preserved in period independent publication | strong historical attribution |
| 2015 revised algorithm used a `periodic refresh feature` | direct Samsung Q&A published by PC Perspective | strong historical attribution |
| periodic feature did not operate with power off | direct Samsung Q&A | strong historical attribution |
| insufficient run-time / long power-off could require Advanced Performance Optimization | direct Samsung Q&A | strong historical attribution |
| Advanced Performance Optimization remained a special 840-family feature | manufacturer-primary 2018 Magician guide | strong later continuity evidence |
| immediate post-firmware performance improved before refresh time elapsed | independent period test | strong observation |
| exact 2015 read-reference threshold algorithm | reviewer inference only | **not grounded as internal implementation fact** |
| periodic refresh guarantees data integrity/lifetime | not established | **rejected** |
| Samsung implemented Cai et al. 2012 FCR | no genealogy evidence | **rejected** |

## Retention-specific findings supported

The case supports the following project-level distinctions:

1. **logical payload continuity ≠ retrieval-performance continuity**;
2. **cell state survival ≠ constant-cost interpretation of cell state**;
3. **successful read-retry ≠ bounded read-service cost**;
4. **read-path improvement ≠ rewrite-based renewal**;
5. **one successful restoration ≠ stable future maintenance closure**;
6. **unpowered physical persistence ≠ unpowered availability of maintenance work**;
7. **power-off retention interval ≠ powered maintenance opportunity**;
8. **automatic background maintenance ≠ zero service cost**;
9. **performance retention ≠ physical-embodiment continuity**;
10. **commercial refresh deployment ≠ generic NAND requirement or academic-algorithm identity**.

These are engineering comparison claims derived from the bounded evidence, not Samsung's terminology unless explicitly noted.

## Prior art / genealogy control

Case 36 already grounds Cai et al., ICCD 2012, as a research proposal for periodic Flash Correct-and-Refresh under an ECC-bounded retention-error model. It predates the 840 EVO remediation episode, but this case makes **no claim of causal lineage** from FCR to Samsung firmware.

The two cases deliberately target different historical objects and different maintenance targets:

- **Case 36:** research proposal; keep raw retention errors inside ECC reliability margin; remap/in-place reprogram policies; simulated SSD lifetime evaluation using measured chip characterization;
- **Case 37:** commercial named product; maintain/recover old-data read performance; one-time rewriting followed by vendor-described periodic refresh plus a supplementary optimization path.

Shared `refresh` language licenses a functional comparison only.

## Related-repository check

A current GitHub search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for Samsung 840 EVO, old-data refresh, read-retry/read-reference, and NAND retention refresh returned no dedicated case. The broader Flash/controller reliability history should remain there if later developed. This repository contributes only the retention-specific decomposition of a commercial remediation regime.

## Why `grounded`

Promotion is justified because the bounded case has:

- a named product and date range;
- surviving manufacturer download artifacts proving the 2014 restoration program existed;
- manufacturer vocabulary and mechanism claims preserved in period direct-vendor statements;
- a 2015 direct Samsung Q&A establishing periodic refresh, power-off limitation, and supplementary optimization;
- independent period testing that separates immediate read-path improvement from later optimization effects;
- later manufacturer documentation independently confirming the special Advanced Performance Optimization feature scope;
- explicit rejection of unsupported internal-algorithm, data-loss, universal-TLC, and FCR-genealogy claims;
- a checked related-repository boundary.

The remaining archival improvement would be recovery of Samsung-hosted 2014/2015 FAQ or Magician 4.6 guide artifacts with the full historical statements. Their absence does not leave the central commercial behavior dependent on an unsourced retrospective, because the period direct-vendor Q&A, surviving Samsung download ledger, later Samsung guide, and independent contemporaneous tests triangulate the bounded claims.

## Sources

1. Samsung 840 EVO Series SSD support/download page: <https://www.samsung.com/us/business/support/owners/product/840-evo-series-1tb/>.
2. Scot Strong, `Samsung Announces Firmware Update To Resolve 840 EVO Performance Degradation`, *The SSD Review*, 15 October 2014: <https://www.thessdreview.com/daily-news/latest-buzz/samsung-announces-firmware-update-resolve-840-evo-performance-degradation/>.
3. Allyn Malventano, `Samsung Magician 4.6 and 840 EVO EXT0DB6Q Firmware Review – Finally Fixed`, *PC Perspective*, 14 April 2015, including Samsung Q&A and test-results pages: <https://pcper.com/2015/04/samsung-magician-4-6-and-840-evo-ext0db6q-firmware-review-finally-fixed/>.
4. Samsung Electronics, `Samsung Magician 5.2.1 Installation Guide`, Rev. 2.4, June 2018, p. 7: <https://semiconductor.samsung.com/resources/data-sheet/Samsung_Magician_5_2_1_Installation_Guide_v2.4.pdf>.
5. Yu Cai et al., `Flash Correct-and-Refresh: Retention-Aware Error Management for Increased Flash Memory Lifetime`, ICCD 2012, comparison/prior-art boundary only: <https://users.ece.cmu.edu/~omutlu/pub/flash-correct-and-refresh_iccd12.pdf>.
