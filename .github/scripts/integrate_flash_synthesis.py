from pathlib import Path

ROOT = Path('.')


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one match, found {count}: {old[:120]!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8')


synthesis = r'''# Flash Retention Synthesis — Read-Path Adaptation, Recovery Cost, and Representation Renewal

**Status:** `grounded cross-case synthesis`

**Cases compared:**

- [`../cases/36-nand-flash-correct-and-refresh-maintenance.md`](../cases/36-nand-flash-correct-and-refresh-maintenance.md) — research proposal for ECC-bounded Correct-and-Refresh (`FCR`);
- [`../cases/37-samsung-840-evo-old-data-performance-refresh.md`](../cases/37-samsung-840-evo-old-data-performance-refresh.md) — named commercial old-data performance incident, one-time restoration, and later periodic refresh policy;
- [`../cases/65-3d-nand-early-retention-loss-age-aware-reading.md`](../cases/65-3d-nand-early-retention-loss-age-aware-reading.md) — early retention loss plus age-aware read-reference selection (`ReMAR`);
- [`../cases/85-toshiba-nand-shift-read-retry-recoverability.md`](../cases/85-toshiba-nand-shift-read-retry-recoverability.md) — shifted / retry reads that change interpretation before any physical rewrite.

This document closes one narrow roadmap question:

> In controller-managed Flash, how should **physical embodiment age**, **read-retry/calibration cost**, **logical payload recoverability**, **read-performance envelope**, **powered maintenance opportunity**, **read-path adaptation**, and **rewrite renewal** be separated?

It does **not** claim one universal NAND firmware architecture. It is a comparison of several historically distinct mechanisms that happen to expose the same analytical mistake: treating every successful later read, every refresh, every retry, and every retained payload as one property called `data retention`.

---

## 1. Claim discipline

This synthesis follows [`METHOD.md`](METHOD.md).

- **H/P — historical / primary:** vocabulary and mechanism directly documented by period patents, vendor statements, manuals, or original papers.
- **S/E — scholarly / empirical:** peer-reviewed characterization of measured devices or evaluated research techniques.
- **E — engineering reconstruction:** relations inferred across the grounded mechanisms.
- **F — functional analogy:** comparison across unlike products/techniques without claiming genealogy.
- **P — philosophical interpretation:** only after the technical relations are kept separate.

Terms such as `physical embodiment age`, `read-performance envelope`, `reader-side recovery`, and `representation renewal` are project reconstruction terms unless a source explicitly uses them.

---

## 2. Historical evidence that forces the separation

### 2.1 Cai et al. 2012 — correction plus physical renewal

Case 36 is bounded to Yu Cai et al., **“Flash Correct-and-Refresh: Retention-Aware Error Management for Increased Flash Memory Lifetime,”** ICCD 2012. Their `FCR` proposal periodically reads Flash, corrects accumulated errors with ECC, and then renews the stored representation by either reprogramming in place or remapping corrected data to another block. Adaptive-rate FCR makes cadence depend on wear history.

The historical object is therefore not merely a better reader. Its maintenance path can deliberately **change the physical embodiment** of the logical payload and can consume endurance while doing so.

**E:** `logical continuation through FCR ≠ physical-location continuity`.

**E:** `representation renewal can spend program/erase lifetime in order to restore future error margin`.

### 2.2 Cai et al. 2015 — retention age can change the best read boundary

Cai et al., **“Data Retention in MLC NAND Flash Memory: Characterization, Optimization, and Recovery,”** HPCA 2015, characterize real 2y-nm MLC NAND and report that the optimal read-reference voltage changes systematically with retention age. Their proposed **Retention Optimized Reading (ROR)** learns and applies a block-appropriate read-reference voltage online.

The paper is especially useful because it explicitly contrasts this read-side route with FCR. In its introduction, FCR is described as periodically reading, correcting, and reprogramming data; the authors identify two limitations for that bounded regime: use of one fixed reference voltage across different retention ages, and the need for the controller to remain consistently powered so refresh work can occur. Their ROR evaluation reports a 10.1% reduction in average error-correction latency and 768 KB of stored overhead for the evaluated 512 GB SSD model; those numbers are **evaluation-specific**, not universal device constants.

This adds a clean historical bridge:

> changing the reader's discrimination boundary can improve reliability/performance **without that read operation itself renewing the cells**.

It also blocks a false equation between `retention age` and one global device age. Different blocks can carry different program times and therefore different useful read-reference settings.

### 2.3 Samsung 840 EVO 2014–2015 — payload continuity can coexist with a degraded service envelope

Case 37 documents a different target. Samsung's 840 EVO episode was publicly framed around severe old-data **read-performance** degradation rather than demonstrated payload loss. Samsung's 2014 explanation, preserved in contemporary reporting, attributed the behavior to flash-management/read-retry behavior and said the restoration path rewrote old data. In 2015 Samsung described a revised firmware path with a `periodic refresh feature` and explicitly said that background feature did not operate while the SSD was powered off.

The product therefore separates at least three things:

1. the logical bytes can still be recovered;
2. recovering them can become expensive enough to violate the expected performance envelope;
3. later background rewrite/refresh can renew the physical representation and restore easier service.

**E:** `logical payload continuity ≠ retrieval-performance continuity`.

**E:** `unpowered payload persistence ≠ unpowered availability of controller maintenance`.

### 2.4 Luo et al. 2018 — early retention loss makes age evidence part of interpretation

Case 65 grounds 3D charge-trap NAND **early retention loss** and Luo et al.'s `Retention Model Aware Reading (ReMAR)`. The measured retention curve is strongly front-loaded in the bounded population, and the proposed controller uses program-time / wear information to choose a better read-reference voltage.

This creates a second-order relation: controller metadata can preserve information about **how old the current physical embodiment is**, and that evidence can influence how the same cells are interpreted later.

**E:** `program-time metadata ≠ user payload`.

**E:** `retained age evidence ≠ refreshed cell charge`.

**E:** `a stale or lost age model can degrade an optimization while the NAND payload remains physically present`.

### 2.5 Toshiba/Nagashima 2009-priority family and Park et al. 2021 — retry can recover state while adding service cost

Case 85 uses Toshiba's 2009-priority `Memory system` family to keep the historical operations distinct: `default read`, shifted read / `retry read`, ECC evaluation, and a later `refresh operation` that copies data to an erased block. The patent family therefore directly blocks the shortcut `retry read = refresh`.

Park et al., ASPLOS 2021, provide a later independent empirical witness using **160 real 3D TLC NAND chips**. Their paper describes read-retry as repeated page sensing with adjusted `VREF` values until raw errors fall within ECC capability or the retry path gives up. It also makes the service cost explicit: additional retry steps add read latency. In their sampled devices, at three months retention age and zero P/E cycles, every read in the reported experiment required more than three retry steps. The paper treats longer retention age and higher P/E wear as conditions that can increase retry work; the exact counts remain bounded to the measured population and experiment.

The same paper finds that the final successful retry can retain positive ECC-capability margin and uses that margin in a research proposal to shorten sensing time. That is another useful separation:

> **remaining correction margin can be traded against read-service cost without becoming a physical rewrite.**

---

## 3. Cross-case state decomposition

| Dimension | Case 36 — FCR | Case 37 — 840 EVO | Case 65 — ReMAR | Case 85 — shifted/read-retry |
| --- | --- | --- | --- | --- |
| physical embodiment age | elapsed retention time + wear motivate maintenance | old, little-modified data is the problematic population | program time is explicit controller input | standing time / operating condition can inform read condition |
| raw physical state | retention errors accumulate | aged-cell interpretation becomes costly | early retention loss shifts distributions quickly | threshold distributions drift relative to read levels |
| reader-side adaptation | not the defining operation; fixed-reference limitation motivates later work | period evidence supports read-path changes but exact proprietary algorithm is not fully exposed | model chooses age-aware read reference | default → shifted / retry read changes read levels |
| ECC / recovery boundary | correct before errors exceed capability | successful recovery can still be slow | lower RBER preserves correction margin | retry seeks a read whose error count is ECC-correctable |
| performance envelope | background work competes with service | central historical target is old-data read performance | better reference choice avoids unnecessary error-correction work | retry steps directly add latency in later empirical evidence |
| powered maintenance opportunity | proactive FCR requires controller power to run | periodic refresh does not run while powered off | access-side policy runs when controller reads; age evidence must remain interpretable | retries occur on powered read path |
| physical renewal | reprogram / remap corrected data | restoration / periodic refresh can rewrite old data | not inherent in ReMAR read adaptation | Toshiba refresh/copy is distinct from retry read |
| principal bounded target | keep retention errors inside ECC reliability margin | keep old-data read service inside practical performance envelope | reduce age-induced read errors via better interpretation | recover a presently readable logical value before/without rewrite |

The table is an **engineering comparison**, not a historical claim that these designs form one direct lineage.

---

## 4. Engineering reconstruction

### 4.1 Physical embodiment age ≠ logical payload age

A logical object can keep the same host-visible identity while its physical NAND embodiment is rewritten or remapped. Conversely, an old physical embodiment can continue returning the same logical bytes.

Therefore:

> `logical object lifetime ≠ uninterrupted lifetime of one NAND cell population`.

This is already visible in Case 36's remapping and Case 37's restoration path.

### 4.2 Physical survival ≠ fixed-cost recovery

An aged page may still contain enough information for ECC plus read-retry to recover the correct logical value, yet require more sensing attempts, more ECC work, and more latency.

Therefore:

> `recoverable now ≠ recoverable at the original service cost`.

Case 37 supplies the named commercial performance boundary; Park et al. supply a later measured mechanism-level witness for retry-step cost.

### 4.3 Read-path adaptation ≠ representation renewal

Changing `VREF`, selecting a different retry condition, or using an age-aware model changes the **interpretation path**. Reprogramming/remapping/copying corrected data changes the **stored representation**.

They can be composed, but they have different costs and different effects:

- read adaptation spends sensing/controller/ECC effort and can leave the aged physical distribution untouched;
- rewrite renewal spends write/erase bandwidth, free-block/mapping work, energy, and endurance but can create a newer physical embodiment with more future margin.

Hence:

> `current reader-side recovery ≠ renewed future physical margin`.

### 4.4 Read-retry cost is not itself data loss

Retry count and read latency can rise while the returned value remains correct. This matters because a storage system can violate a performance expectation before it violates a correctness expectation.

Therefore:

> `retention-quality degradation can appear first as service degradation rather than forgetting`.

This does **not** justify calling every latency regression a retention failure. The relation is retention-specific only where the extra work is causally tied to preserving/recovering aged stored state.

### 4.5 Powered maintenance opportunity ≠ power-off retention interval

NAND's programmed state can persist while the SSD is off, but background firmware cannot perform refresh/rewrite work without power. Cai et al. 2015 explicitly identify continuously powered operation as a limitation of their FCR comparison, while Samsung's 2015 840 EVO statement independently says its periodic-refresh algorithm does not operate when the drive is powered off.

Therefore:

> `medium can retain payload while system accumulates maintenance debt`.

The debt may later manifest as extra retry latency, a need for foreground recovery, or a need to renew the representation after power returns.

### 4.6 Maintenance targets must be named

The cases do not all preserve the same quantity:

- Case 36 targets **ECC-bounded reliability / lifetime**;
- Case 37 targets **old-data read performance** in a named product episode;
- Case 65 targets **lower read error rate through age-aware interpretation**;
- Case 85 isolates **present recoverability through adjusted sensing**.

Therefore the word `refresh` is insufficient unless the target, operation, and substrate are stated.

---

## 5. Rejected collapses

1. **`old Flash = unreadable Flash`** — rejected. Age can increase raw errors or recovery cost before logical failure.
2. **`ECC-correctable = healthy/new physical representation`** — rejected. Correctability says the current path still has enough margin.
3. **`read retry = refresh`** — rejected by Toshiba's explicit separation and by the different physical operations.
4. **`better VREF = restored charge`** — rejected. A reader can change its decision boundary while the cell population remains aged.
5. **`rewrite = mere read optimization`** — rejected. Rewriting creates a new/renewed physical embodiment and consumes storage-management resources.
6. **`powered-off retention = powered-off maintenance`** — rejected. The medium may retain while background maintenance is unavailable.
7. **`slow read = forgotten data`** — rejected. Service degradation and logical forgetting are different states.
8. **`one vendor/product result = universal NAND law`** — rejected. Numerical retention curves, retry counts, and firmware behavior remain device/population specific.

---

## 6. Prior-art and terminology boundary

No new invention-priority claim is made here.

- Case 85 already grounds a 2000-priority MLC reference-voltage-adjustment patent family before Toshiba's 2009-priority design, while refusing to infer direct genealogy.
- Case 36 treats `Flash Correct-and-Refresh` as Cai et al.'s 2012 research vocabulary, not as a generic retroactive name for every earlier rewrite policy.
- Case 37 keeps Samsung's historical product terms — `Performance Restoration`, `read-retry`, `periodic refresh feature`, and `Advanced Performance Optimization` — local to the product episode.
- Cases 65 and 85 preserve `ReMAR`, `read-retry`, `VREF`, and related paper/patent vocabulary without projecting those labels onto earlier Flash generations.

A complete sense-amplifier, retry-command, vendor-table, LDPC/soft-decision, TLC/QLC, and commercial-controller genealogy belongs primarily in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology). A fresh repository search for `read retry` and `NAND flash` found no dedicated matching technical-history module there, so this synthesis keeps only the retention-specific relation and leaves the broader device genealogy open.

---

## 7. Bounded roadmap closure

For the current repository, the controller-managed Flash comparison can now be treated as closed at the **relation-decomposition level**:

```text
physical embodiment age / wear
        !=
raw threshold-distribution state
        !=
chosen read/reference condition
        !=
raw error population
        !=
ECC-bounded logical recoverability
        !=
retry / calibration work
        !=
read-performance envelope
        !=
powered opportunity for proactive maintenance
        !=
rewrite / remap / reprogram renewal
        !=
future physical-error margin
```

The following remain valid future work without reopening this exact synthesis question:

- vendor-specific retry-command and calibration-table genealogy;
- QLC and newer 3D-NAND read-threshold behavior;
- named-product telemetry linking retry counts to long power-off intervals;
- exact firmware scheduling/energy costs for background refresh/reclaim;
- cross-vendor fault injection and aged-device validation;
- how on-die ECC and hidden controller recovery alter host-visible evidence.

---

## Sources used for this synthesis

1. Yu Cai et al., **“Flash Correct-and-Refresh: Retention-Aware Error Management for Increased Flash Memory Lifetime,”** ICCD 2012, DOI `10.1109/ICCD.2012.6378623`: <https://users.ece.cmu.edu/~omutlu/pub/flash-correct-and-refresh_iccd12.pdf>.
2. Yu Cai et al., **“Data Retention in MLC NAND Flash Memory: Characterization, Optimization, and Recovery,”** HPCA 2015, DOI `10.1109/HPCA.2015.7056062`: <https://www.istc-cc.cmu.edu/publications/papers/2015/flash-memory-data-retention_hpca15.pdf>.
3. Jisung Park et al., **“Reducing Solid-State Drive Read Latency by Optimizing Read-Retry,”** ASPLOS 2021, DOI `10.1145/3445814.3446719`: <https://arxiv.org/abs/2104.09611>.
4. Toshiba/Nagashima 2009-priority **“Memory system”** family, representative US publication: <https://patents.google.com/patent/US20120268994A1/en>.
5. The Samsung 840 EVO and 3D-NAND ReMAR source chains remain fully enumerated in the grounded records for [Case 37](../evidence/37-samsung-840-evo-2014-2015-performance-refresh-grounding.md) and [Case 65](../evidence/65-3d-nand-2010-2018-early-retention-grounding.md); this synthesis does not duplicate those source ledgers.
'''

out = ROOT / 'docs/SYNTHESIS_06_FLASH_READ_PATH_VS_RENEWAL.md'
if out.exists():
    raise SystemExit(f'{out}: already exists; refusing to overwrite')
out.write_text(synthesis, encoding='utf-8')

roadmap_old = "- [ ] In controller-managed Flash, how should physical embodiment age, read-retry/calibration cost, logical payload recoverability, read-performance envelope, powered maintenance opportunity, read-path adaptation, and rewrite renewal be separated?"
roadmap_new = "- [x] In controller-managed Flash, separate `physical embodiment age`, `read-retry/calibration cost`, `logical payload recoverability`, `read-performance envelope`, `powered maintenance opportunity`, `read-path adaptation`, and `rewrite renewal` — closed at the bounded relation-decomposition level by [`docs/SYNTHESIS_06_FLASH_READ_PATH_VS_RENEWAL.md`](docs/SYNTHESIS_06_FLASH_READ_PATH_VS_RENEWAL.md), synthesizing grounded Cases 36, 37, 65, and 85 and adding the Cai et al. 2015 / Park et al. 2021 empirical latency-and-reference-voltage bridge. Vendor retry-command genealogy, QLC/newer 3D-NAND behavior, named-product telemetry, exact maintenance energy/scheduling, on-die-ECC visibility, and cross-vendor fault injection remain separate work."
replace_once('ROADMAP.md', roadmap_old, roadmap_new)

readme_anchor = "This chain is a **research heuristic**, not a claim that all of these mechanisms are historically or philosophically identical."
readme_insert = "A focused Flash/SSD comparison is now available in [`docs/SYNTHESIS_06_FLASH_READ_PATH_VS_RENEWAL.md`](docs/SYNTHESIS_06_FLASH_READ_PATH_VS_RENEWAL.md). It separates physical embodiment age, reader-side adaptation, ECC/retry cost, logical recoverability, service performance, powered maintenance opportunity, and physical rewrite/renewal across grounded Cases 36, 37, 65, and 85."
replace_once('README.md', readme_anchor, readme_insert + "\n\n" + readme_anchor)

index = ROOT / 'CASE_INDEX.md'
index_text = index.read_text(encoding='utf-8')
if '### Cross-case Flash retention synthesis — Cases 36, 37, 65, and 85' in index_text:
    raise SystemExit('CASE_INDEX.md: Flash synthesis findings already present')
expected_tail = "1280. **element nonvolatility ≠ uniform state-class nonvolatility** — Case 02 grounds remanent core state at the memory-element/access-cycle level, while Case 86 and the IBM counterexample show that processor, protection, I/O, and main-storage state can cross the same power lifecycle under different preservation rules."
if not index_text.rstrip().endswith(expected_tail):
    raise SystemExit('CASE_INDEX.md: unexpected findings tail; repository advanced concurrently')
findings = r'''

### Cross-case Flash retention synthesis — Cases 36, 37, 65, and 85

1281. **physical embodiment age ≠ logical-object lifetime** — a host-visible object can outlive one NAND cell population through rewrite/remap, while an old physical embodiment can also remain logically readable without being physically renewed.

1282. **logical recoverability ≠ original read-performance envelope** — aged Flash can remain ECC/retry-recoverable while sensing attempts, decoding work, and latency increase enough to become a service problem.

1283. **read-retry/calibration work can grow before logical forgetting** — Park et al.'s measured 3D-TLC retry behavior supplies an empirical witness that added recovery steps are an intermediate state, not proof that the payload is already absent.

1284. **read-path adaptation ≠ representation renewal** — changed `VREF`, shifted read, ROR, or age-aware reading changes interpretation of surviving cells; reprogram/remap/rewrite creates a renewed physical embodiment.

1285. **successful reader-side recovery ≠ restored future physical margin** — a page can be decoded now under a better reference/ECC path while its aged threshold distribution and wear history remain.

1286. **powered maintenance opportunity ≠ power-off payload retention** — NAND can preserve data without operating power while proactive controller rewrite/refresh policies remain unable to execute and maintenance debt can accumulate.

1287. **retained age/read-condition metadata ≠ refreshed cell state** — controller evidence about program time, wear, or a useful read condition can improve future interpretation without putting leaked charge back into the cell.

1288. **ECC margin can be a service-performance resource without becoming free reliability** — Park et al. use remaining final-retry correction margin to motivate shorter sensing latency; spending margin on latency does not make the physical error population disappear.

1289. **one Flash maintenance target ≠ another** — Case 36 targets ECC-bounded reliability/lifetime, Case 37 old-data read performance, Case 65 age-aware error reduction, and Case 85 present retry recoverability; shared controller work does not erase those different contracts.

1290. **controller-managed Flash retention is a staged relation rather than one `nonvolatile` Boolean** — physical charge survival, read interpretation, raw-error population, ECC recovery, retry cost, service performance, powered maintenance, physical renewal, and renewed future margin can change at different times.
'''
index.write_text(index_text.rstrip() + findings + '\n', encoding='utf-8')

# Lightweight integrity checks for this bounded integration.
for path in ['README.md', 'ROADMAP.md', 'CASE_INDEX.md', 'docs/SYNTHESIS_06_FLASH_READ_PATH_VS_RENEWAL.md']:
    text = (ROOT / path).read_text(encoding='utf-8')
    if '\r' in text:
        raise SystemExit(f'{path}: unexpected CR character')

print('Integrated Flash read-path-vs-renewal synthesis.')
