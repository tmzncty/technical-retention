# Samsung 840 EVO Old-Data Performance Restoration: Read Calibration, Rewrite Renewal, and Powered Periodic Refresh

## Status

**`grounded`** — bounded to Samsung's 840 EVO old-data read-performance incident and its 2014–2015 remediation sequence: the October 2014 Performance Restoration tooling and the 2015 revised firmware / Magician path that Samsung described as using a **periodic refresh feature**. The case uses Samsung's surviving product-support downloads and later Magician documentation as manufacturer-primary anchors, plus period independent technical reporting that preserves direct Samsung statements and tests the behavior.

Grounding record: [`../evidence/37-samsung-840-evo-2014-2015-performance-refresh-grounding.md`](../evidence/37-samsung-840-evo-2014-2015-performance-refresh-grounding.md).

## Scope

This case asks a narrow question left deliberately open by Case 36:

> What changes when Flash retention maintenance is no longer only a research proposal, but becomes a product-specific commercial SSD behavior whose purpose is to keep **old-data read performance** within an acceptable service regime?

The bounded sequence is:

1. **September–October 2014:** users and reviewers document markedly slower reads of old, little-modified data on Samsung 840 EVO drives;
2. **October 2014:** Samsung publishes a Performance Restoration package. A period Samsung statement attributes the behavior to an error in the flash-management software algorithm, says the drive was performing read-retry aggressively on old once-written data, and says the restoration software rewrites old data;
3. **April 2015:** after the first fix proved insufficient for some stale-data samples, Samsung tells PC Perspective that a revised firmware algorithm uses a **periodic refresh feature** to maintain read performance of older data. Samsung explicitly says this background algorithm does not operate while power is off and provides Advanced Performance Optimization as a supplementary recovery path for drives with insufficient run-time or long powered-off intervals;
4. **later vendor continuity:** Samsung's own Magician documentation continues to list Advanced Performance Optimization as a special feature for the 840 EVO / 840 family.

This is **not**:

- a claim that all 840 EVO data was at risk of loss;
- a claim that all TLC NAND, all Samsung SSDs, or all SSDs require this exact policy;
- a claim that read-performance degradation is identical to uncorrectable retention failure;
- a claim that Samsung's periodic refresh is identical to Cai et al.'s 2012 FCR algorithm;
- a claim that every performance improvement observed after the 2015 firmware came from rewriting old pages;
- a general history of Samsung TLC NAND, read-retry, ECC, voltage-reference tuning, or SSD firmware;
- an invention-priority claim for NAND refresh or age-aware read calibration.

The object is the **commercial 840 EVO maintenance contract and observed remediation behavior**, not a generic theory of TLC NAND.

## Historical vocabulary and evidence

Samsung's surviving 840 EVO support page still exposes the product-specific **Performance Restoration Software** artifacts dated 24–28 October 2014, including Windows v1.1 and DOS/ISO v1.0 packages. This directly establishes that Samsung shipped a special restoration path rather than leaving the issue as an informal workaround.

Contemporary technical reporting preserves Samsung's explanation of the 2014 failure mode. Samsung described an error in the `flash management software algorithm`; it said SSDs ordinarily calibrate changes in cell status over time, but the 840 EVO performed `read-retry` too aggressively on older once-written data, producing a large read-performance drop. The same Samsung statement said data that had been migrated or overwritten did not show the symptom and that the restoration software restored performance by **rewriting the old data**.

The first remediation did not end the historical episode. In April 2015, PC Perspective tested a revised 840 EVO firmware identified in the article as `EXT0DB6Q` and published a direct Q&A with Samsung. Samsung's answer used the historical term **`periodic refresh feature`** and said it could maintain old-data read performance in the background without Magician. Samsung also stated that this algorithm **does not operate when power is off**. If the drive had not had enough run-time, or had been powered off for an extended period, Samsung named **Advanced Performance Optimization** in Magician 4.6 as a supplementary path to recover performance.

A later Samsung Magician 5.2.1 Installation Guide (June 2018) still documents `Advanced Performance Optimization` and says the function is supported on Samsung SSD 840 EVO (2.5-inch and mSATA) and 840 Series models. That later document is used only to confirm continued vendor-recognized feature scope; it is not projected backward as the exact 2015 implementation specification.

## Retained state and constitutive control relations

The case contains several distinct states and relations:

1. **NAND cell state** — threshold-voltage states whose interpretation can become more difficult as old data ages;
2. **logical payload** — the bytes still returned correctly to the host in the bounded performance incident;
3. **read-recovery state** — controller calibration / read-retry behavior used to interpret aging cells;
4. **physical embodiment age** — how long the current NAND embodiment has remained without migration/overwrite;
5. **logical-to-physical mapping** — the FTL relation that lets rewritten or migrated data remain the same host-visible content while its physical embodiment changes;
6. **background-maintenance opportunity** — powered run-time in which firmware can execute the periodic refresh behavior;
7. **manual/supplementary maintenance authority** — host-side Magician invocation of Advanced Performance Optimization when background maintenance has not caught up.

`read-recovery state`, `physical embodiment age`, and `background-maintenance opportunity` are project reconstruction terms. Samsung's period vocabulary includes `flash management software algorithm`, `read-retry`, `Performance Restoration`, `periodic refresh feature`, and `Advanced Performance Optimization`.

## Engineering reconstruction

### Payload retention is not the same as retrieval-performance retention

The bounded incident was reported as a severe **read-performance** degradation of older data, while Samsung's 2014 public explanation said the issue did not concern data loss or reliability. Independent reviewers likewise reported stale files remaining readable even while transfer speed collapsed.

Therefore:

> **logical payload continuity ≠ retrieval-performance continuity**.

A value can remain recoverable as the same logical value while the cost of obtaining it changes drastically. `Retained` is incomplete unless the target is named: payload correctness, latency, throughput, energy, and serviceability are not one retention property.

This case must not silently upgrade Samsung's no-data-loss statement into proof that no 840 EVO ever experienced an unrelated failure. The bounded claim is narrower: the documented incident and remediation were framed as an old-data read-performance problem rather than a demonstrated uncorrectable-data-loss regime.

### Interpretation work can age even when the logical payload still survives

Samsung's 2014 explanation says SSD flash-management software normally calibrates changes in cell status over time and that the faulty 840 EVO algorithm drove excessive read-retry on old data. That makes the read path itself part of the continuation relation.

Therefore:

> **cell state survival ≠ constant-cost interpretation of cell state**.

And:

> **successful read-retry ≠ bounded read-service cost**.

A controller may still recover the intended logical state while expending more retries, latency, controller work, or thermal/service budget than the original fast-read path.

### Read-path adaptation and physical rewriting are different maintenance operations

PC Perspective's April 2015 tests provide a useful boundary. The reviewer ran a stale-data benchmark **immediately after the firmware update**, before the drive had time to perform the claimed background refresh, and saw a large improvement. The reviewer inferred that Samsung had also changed the read algorithm to adapt better to drifted cells. Advanced Optimization then produced further improvement and was described by the reviewer as refreshing data.

The exact internal read-reference algorithm is not documented by Samsung in the inspected sources, so the inference remains secondary/engineering evidence. But the temporal observation is enough to reject a stronger simplification:

> **read-path improvement ≠ rewrite-based renewal**.

The product episode contains at least two analytically distinct ways to preserve useful access to aging state:

- change how the controller **interprets / recovers** an existing physical embodiment;
- **rewrite / refresh** data so that a newer physical embodiment is easier to read.

The same logical object can benefit from either without those operations being historically or physically identical.

### One-time restoration is not the same as a continuing maintenance policy

The October 2014 Performance Restoration path rewrote old data and initially restored performance. By April 2015, PC Perspective's stale samples had again slowed toward pre-restoration behavior, and Samsung supplied a new firmware whose answer explicitly invoked a **periodic refresh feature**.

Therefore:

> **one successful restoration ≠ stable future maintenance closure**.

A one-time rewrite can renew the current physical embodiment without proving that the controller's future interpretation/maintenance policy will keep later aging inside the desired service envelope.

This is a useful product-level complement to Case 36. Cai et al.'s FCR paper proposed periodic renewal before ECC margin is exhausted; Samsung's 840 EVO episode shows a commercial product moving from a one-time restoration action toward a continuing background refresh policy for a different target — old-data read performance.

### Nonvolatile retention while powered off is not the same as maintenance availability while powered off

Samsung's 2015 answer is unusually explicit: the periodic-refresh algorithm **does not operate when power is off**. The same answer says an SSD that had insufficient run-time or remained powered off for an extended period might need Advanced Performance Optimization to recover performance.

Therefore:

> **unpowered physical persistence ≠ unpowered availability of maintenance work**.

And:

> **power-off retention interval ≠ powered maintenance opportunity**.

The NAND can continue to hold the payload while the controller has no opportunity to execute a policy intended to keep retrieval performance normal. Power is therefore not required merely for the bounded payload to remain, yet powered time becomes infrastructure for maintaining another property of the retained state: efficient service.

### Background automation does not eliminate maintenance competition

Samsung said the periodic feature could operate without Magician and claimed it would not affect normal user scenarios except possible occasional performance degradation due to SSD background work. The later Magician guide separately warns that Advanced Performance Optimization can take time and, on at least one documented platform, may make Windows respond slowly while the operation is in progress.

Therefore:

> **automatic background maintenance ≠ zero service cost**.

Automation changes who initiates the work; it does not make controller time, NAND traffic, energy, or foreground interference disappear.

### Rewrite renewal can preserve logical identity while changing physical history

Samsung's 2014 statement says migration/overwrite removes the old-data symptom, and the restoration tool rewrites old data. At the host interface the file/value remains the same, while its NAND embodiment is renewed through controller-managed write/migration behavior.

Thus:

> **performance retention ≠ physical-embodiment continuity**.

This extends Case 04's logical/physical distinction and Case 36's retention-triggered remapping, but the trigger and target differ. Case 04 concerns erase-driven FTL continuity; Case 36 concerns a research policy for ECC-bounded retention reliability; Case 37 concerns a commercial old-data **read-performance** maintenance episode.

## Failure and forgetting boundaries

The bounded 840 EVO episode exposes several ways a retained state can become worse without becoming absent:

- the payload remains logically readable while old-data throughput falls sharply;
- controller read-retry/calibration can recover state but at a higher service cost;
- a one-time rewrite can restore the immediate state yet fail to establish a sufficient future maintenance policy;
- the firmware's background maintenance cannot run while the drive is powered off;
- insufficient powered run-time can leave maintenance backlog that requires explicit optimization;
- foreground service may compete with background restoration work.

This case therefore treats **degraded availability/performance** as distinct from forgetting. Slow recovery is not automatically data loss, just as physical presence is not automatically fast orderability.

## Prior art and anti-anachronism

This repository makes **no invention-priority claim** for Samsung's refresh or calibration techniques.

Case 36 already grounds Cai et al.'s 2012 academic FCR proposal and earlier NAND-retention research. The Samsung case is valuable for a different historical reason: it is a named commercial SSD, a public vendor remediation sequence, and a documented transition from one-time rewrite restoration to a firmware policy described by the vendor as periodic refresh.

Likewise, `periodic refresh feature` is Samsung's 2015 product vocabulary. It must not be projected backward onto early Flash cases or treated as proof that Samsung implemented Cai et al.'s FCR algorithm. Similarity at the level of repeated renewal is a **functional analogy**, not a demonstrated genealogy.

Current inspection of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated Samsung 840 EVO / old-data refresh case to reuse. A broader TLC-NAND/controller reliability history belongs there; this repository keeps the retention-specific distinction among payload survival, read interpretation, rewrite renewal, powered maintenance opportunity, and service performance.

## Functional analogies and limits

### To Case 36 — Flash Correct-and-Refresh

Useful analogy:

- both cases show a nonvolatile Flash system performing controller-mediated maintenance on aging data;
- both permit logical identity to survive physical renewal;
- both make maintenance cadence/policy part of practical continuation.

Limit:

- Case 36 is a research proposal/evaluation aimed at keeping retention errors inside an ECC reliability margin;
- Case 37 is a commercial product incident and remediation aimed at old-data **read performance**;
- no inspected source establishes that Samsung implemented Cai et al.'s algorithms.

### To DRAM refresh

Useful analogy:

- repeated maintenance can preserve some desired property of later access.

Limit:

- the 840 EVO payload is nonvolatile and remains while power is off;
- the background controller policy itself stops while power is off;
- DRAM refresh is constitutive periodic restoration required to prevent volatile dynamic-cell state from disappearing.

### To ZFS/GFS scrub

Useful analogy:

- all can consume background I/O to improve future service/reliability.

Limit:

- scrub is primarily proactive **verification** with conditional repair;
- Samsung's described periodic feature is a product-specific refresh/performance-maintenance behavior for old Flash data.

## Philosophical pressure and limit

The narrow conceptual pressure is:

> A technically retained object can remain the same logical object while the **effort required to call it back** changes with age, and a system may expend hidden maintenance not to keep the payload from immediately vanishing but to keep later retrieval inside a practical service envelope.

This is an engineering/philosophical interpretation, not Samsung's historical claim. It should not be inflated into the proposition that every performance optimization is `retention` or that slow data is forgotten data.

## Cross-case result

```text
old NAND embodiment
    !=
logical payload still recoverable
    !=
read-retry / calibration cost
    !=
normal old-data read performance
    !=
firmware read-path adaptation
    !=
background periodic refresh opportunity
    !=
manual Advanced Performance Optimization
    !=
rewritten / renewed physical embodiment
    !=
restored performance envelope
```

The key new axis is therefore:

> **payload continuity → interpretation/recovery cost → service performance → powered maintenance opportunity → renewal action**

rather than treating all five as one property called `data retention`.

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Samsung shipped 840 EVO Performance Restoration packages in October 2014 | H/P | surviving Samsung product-support download records |
| Samsung attributed the old-data slowdown to a flash-management algorithm error that caused aggressive read-retry | H/S | direct Samsung statement preserved in contemporary independent technical reporting |
| Samsung said migrated/overwritten data did not show the symptom and the restoration software rewrote old data | H/S | same period Samsung statement preserved by contemporary reporting |
| Samsung's 2015 revised algorithm was described as using a `periodic refresh feature` | H/S | direct Samsung Q&A published by PC Perspective |
| Samsung said the periodic feature does not operate with power off | H/S | direct Samsung Q&A published by PC Perspective |
| Samsung identified Advanced Performance Optimization as a supplementary recovery path after insufficient powered run-time / long power-off | H/S | direct Samsung Q&A; later Samsung Magician guide independently confirms the named feature and 840-family scope |
| The 2015 firmware produced immediate stale-data performance improvement before background refresh had time to run | H/S | PC Perspective controlled before/after test |
| The immediate improvement proves the exact internal read-reference algorithm | X | reviewer inferred read-algorithm adaptation; no inspected Samsung implementation document exposes the exact algorithm |
| The 840 EVO incident proves payload data was being lost | X | Samsung framed the bounded problem as read-performance degradation, not data loss/reliability loss |
| Samsung periodic refresh is Cai et al. FCR | X | no genealogy or algorithm-identity evidence |
| Samsung's policy proves all TLC/NAND SSDs require periodic refresh | X | outside the named product/remediation scope |

## Sources

1. Samsung, **840 EVO Series SSD (1TB) support page**, surviving product-support download ledger. The page lists `Performance Restoration Software` / `Update Software` artifacts dated 24–28 October 2014 for the 840 EVO: <https://www.samsung.com/us/business/support/owners/product/840-evo-series-1tb/>.
2. Scot Strong, **“Samsung Announces Firmware Update To Resolve 840 EVO Performance Degradation,”** *The SSD Review*, 15 October 2014. Preserves Samsung's contemporaneous explanation of the flash-management algorithm / aggressive read-retry behavior and the rewrite-based restoration statement: <https://www.thessdreview.com/daily-news/latest-buzz/samsung-announces-firmware-update-resolve-840-evo-performance-degradation/>.
3. Allyn Malventano, **“Samsung Magician 4.6 and 840 EVO EXT0DB6Q Firmware Review – Finally Fixed,”** *PC Perspective*, 14 April 2015. Includes a direct Q&A with Samsung describing the periodic-refresh feature, power-off boundary, and Advanced Performance Optimization fallback, plus independent before/after testing: <https://pcper.com/2015/04/samsung-magician-4-6-and-840-evo-ext0db6q-firmware-review-finally-fixed/>.
4. Samsung Electronics, **Samsung Magician 5.2.1 Installation Guide**, Revision 2.4, June 2018, p. 7 (`Performance Optimization` limitations). Manufacturer-primary later continuity evidence that Advanced Performance Optimization is a special supported feature for Samsung SSD 840 EVO / 840 Series: <https://semiconductor.samsung.com/resources/data-sheet/Samsung_Magician_5_2_1_Installation_Guide_v2.4.pdf>.
5. Yu Cai et al., **“Flash Correct-and-Refresh: Retention-Aware Error Management for Increased Flash Memory Lifetime,”** ICCD 2012, used only for the separate research-proposal comparison in Case 36: <https://users.ece.cmu.edu/~omutlu/pub/flash-correct-and-refresh_iccd12.pdf>.
