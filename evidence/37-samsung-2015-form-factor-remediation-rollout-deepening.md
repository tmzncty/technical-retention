# Case 37 Deepening — Samsung 840 EVO 2015 Form-Factor Remediation Rollout Boundary

## Status

**`bounded deepening complete`** — bounded to the 2015 rollout boundary between the 2.5-inch 840 EVO remediation path and the later mSATA path. This record does not reopen the already-grounded NAND aging / old-data performance mechanism, and it does not infer undocumented controller differences from form factor alone.

## Purpose

This record deepens [`../cases/37-samsung-840-evo-old-data-performance-refresh.md`](../cases/37-samsung-840-evo-old-data-performance-refresh.md) around one narrow historical question:

> Did the 2015 maintenance/remediation capability described for the 840 EVO become available to the 2.5-inch and mSATA variants at the same time merely because both belonged to the same product family?

The inspected evidence says **no** at the public rollout/interface level.

The April 2015 `EXT0DB6Q` update path discussed in the existing Case 37 evidence was publicly available for the ordinary 840 EVO while contemporary reporting explicitly noted that it did not then apply to the mSATA variant. By late August 2015, period release-note preservation for Samsung Magician 4.7 named **Advanced Performance Optimization support for 840 EVO mSATA** and stated that new firmware was required. On 1 October 2015, PC Perspective reported that Samsung's `EXT43B6Q` firmware had become available for the mSATA variant and demonstrated Advanced Performance Optimization on a 1 TB 840 EVO mSATA sample.

Samsung's current official firmware ledger independently preserves two distinct final 840 EVO firmware identities:

- `SATA SSD-840 EVO Firmware` — `EXT0DB6Q`;
- `SATA SSD-840 EVO mSATA Firmware` — `EXT43B6Q`.

The bounded result is therefore about **historical maintenance-capability rollout and admission**, not about claiming that the two firmware images implement different refresh algorithms internally.

## Why this slice matters

The canonical Case 37 already uses Samsung's later Magician documentation to show that Advanced Performance Optimization ultimately covered both 2.5-inch and mSATA 840 EVO models. If that later common scope is read without the 2015 rollout chronology, it is easy to collapse two different propositions:

```text
feature eventually supported across a product family
    !=
feature introduced for every variant at the same historical moment
```

That distinction matters to `technical-retention` because retention maintenance is not only a physical capability of NAND. In this episode, access to the maintenance policy is also mediated by a particular firmware lineage, host management software, and model/variant eligibility.

## Evidence classes and provenance

### A. Samsung current firmware ledger — manufacturer-primary artifact identity

Samsung Semiconductor's current **Tool & Software Download** page separately lists:

- `SATA SSD-840 EVO mSATA Firmware` — ISO `EXT43B6Q`;
- `SATA SSD-840 EVO Firmware` — ISO `EXT0DB6Q`;
- corresponding Mac firmware entries with the same revision identifiers.

Source:

- <https://semiconductor.samsung.com/consumer-storage/support/tools/>

Evidence label: **H/P-current**.

This is strong manufacturer-primary evidence that Samsung's surviving firmware distribution infrastructure distinguishes the ordinary 840 EVO and 840 EVO mSATA with different firmware revision identities. The current page does **not** by itself establish the original 2015 release dates, the exact code differences, or the reason for the staggered rollout.

### B. PC Perspective, 28 April 2015 — period exclusion witness

PC Perspective's 28 April 2015 article on the standalone ISO updater documents the `EXT0DB6Q` remediation path after Magician 4.6 and explicitly warns mSATA 840 EVO users that the update did not currently appear to apply to their drives. The author says he had asked Samsung about the omission.

Source:

- Allyn Malventano, **“Samsung 840 EVO Standalone ISO Updater Now Available,”** *PC Perspective*, 28 April 2015: <https://pcper.com/2015/04/samsung-840-evo-standalone-iso-updater-now-available/>.

Evidence label: **H/S-period** — contemporary independent technical reporting. It is not promoted into a Samsung specification, but it is direct period evidence that the publicly available April update path was not being treated as an mSATA update.

### C. Magician 4.7 release-note preservation, 31 August 2015 — capability-admission witness

Tweakers' 31 August 2015 Magician 4.7 software record reproduces the period release-note changes and attributes the source to Samsung. The relevant entry adds **Advanced Performance Optimization support for 840 EVO mSATA** and states that new firmware is required to use that function.

Source:

- Tweakers, **“Software-update: Samsung Magician 4.7,”** 31 August 2015: <https://tweakers.net/downloads/35337/samsung-magician-47.html>.

Evidence label: **H/S with vendor-release-note provenance**.

This source is useful because it separates application-level feature exposure from device-firmware eligibility:

```text
Magician 4.7 exposes/supports the mSATA feature
    +
new device firmware is required
```

The currently inspected copy is not a Samsung-hosted 2015 PDF, so this record does not silently upgrade it to direct first-party inspection.

### D. PC Perspective, 1 October 2015 — mSATA firmware availability and observed use

PC Perspective's 1 October 2015 follow-up identifies `EXT43B6Q` as the newly available mSATA firmware. It explicitly contrasts this with the earlier `EXT0DB6Q` / Magician 4.6 rollout, states that the mSATA variant had been left out of that earlier round, and reports successful application of `EXT43B6Q` to a 1 TB 840 EVO mSATA sample followed by use of Advanced Performance Optimization.

Source:

- Allyn Malventano, **“Samsung 840 EVO mSATA Gets Long Awaited EXT43B6Q Firmware, Fixes Read Speed Issue,”** *PC Perspective*, 1 October 2015: <https://pcper.com/2015/10/samsung-840-evo-msata-gets-long-awaited-ext43b6q-firmware-fixes-read-speed-issue/>.

Evidence label: **H/S-period + observed test**.

The report establishes public availability and one observed successful maintenance path. It does not prove fleet-wide success, binary identity with the 2.5-inch firmware, or the internal refresh algorithm.

### E. Samsung later Magician guide — eventual common scope

Samsung's Magician 5.2.1 Installation Guide (Revision 2.4, June 2018) states that Advanced Performance Optimization is supported on Samsung SSD 840 EVO **2.5-inch and mSATA** models, plus the 840 Series.

Source:

- Samsung Electronics, **Samsung Magician 5.2.1 Installation Guide**, Rev. 2.4, June 2018, p. 7: <https://semiconductor.samsung.com/resources/data-sheet/Samsung_Magician_5_2_1_Installation_Guide_v2.4.pdf>.

Evidence label: **H/P-later**.

This later first-party document is used only to establish eventual vendor-recognized scope. It is not used to erase the staggered 2015 rollout.

## Historical record

### April 2015: the revised 2.5-inch remediation path did not yet cover mSATA

The canonical Case 37 already grounds Samsung's April 2015 `EXT0DB6Q` remediation and the Samsung Q&A describing a `periodic refresh feature` plus Advanced Performance Optimization.

The 28 April PC Perspective follow-up adds an important historical scope boundary: the standalone update then available did not appear to apply to the mSATA 840 EVO.

Therefore, the safe historical statement is:

> In late April 2015, the public `EXT0DB6Q` remediation path discussed for the 840 EVO was not simultaneously available as the corresponding mSATA update path.

This statement is deliberately about **publicly available update scope**, not a claim that Samsung had done no internal mSATA development by that date.

### August 2015: Magician 4.7 names mSATA Advanced Performance Optimization but still requires device firmware

The preserved Magician 4.7 release-note text adds support for Advanced Performance Optimization on the 840 EVO mSATA and immediately qualifies that capability with a firmware prerequisite.

That creates two distinct admission layers:

```text
host management software knows/exposes the feature
    !=
device has the required firmware
```

The release-note evidence does not show that every mSATA drive already had the required firmware on 31 August 2015.

### October 2015: EXT43B6Q closes the public mSATA firmware gap

By 1 October, PC Perspective reports that `EXT43B6Q` had become available for mSATA and demonstrates the update plus Advanced Performance Optimization on a 1 TB sample.

The current Samsung firmware ledger independently preserves `EXT43B6Q` as the mSATA firmware identity and `EXT0DB6Q` as the ordinary 840 EVO firmware identity.

The two source classes are complementary:

- the **period report** supplies rollout timing and observed use;
- the **current manufacturer ledger** supplies surviving first-party firmware identity/provenance.

Neither should be asked to prove what only the other establishes.

## Engineering reconstruction

### Product-family identity is not simultaneous maintenance-policy availability

The most important reconstruction is simple:

```text
same marketing/product family
    !=
same firmware package
    !=
same update availability date
    !=
same maintenance-feature admission state
```

The later Samsung Magician guide can truthfully list both 2.5-inch and mSATA as supporting Advanced Performance Optimization while the historical path to that common scope remained staggered.

Therefore:

> **eventual common feature scope ≠ simultaneous historical introduction**.

### Maintenance availability can be a conjunction of software, firmware, and model eligibility

The Magician 4.7 release-note evidence is especially useful because it says the mSATA Advanced Performance Optimization function requires new firmware.

A bounded reconstruction is:

```text
host tool / feature support
    +
model eligibility
    +
required device firmware
        -> maintenance path can become admissible
```

This is a relation among documented prerequisites. It is not a claim that those three factors are the complete internal precondition set for every execution.

Thus:

> **host-side feature visibility ≠ device-side maintenance capability**.

And:

> **firmware availability ≠ maintenance execution ≠ maintenance completion**.

The existing restoration-transaction deepening already handles execution/completion separately.

### Distinct firmware identities do not prove distinct algorithms

Samsung's current firmware ledger gives two different identifiers, `EXT0DB6Q` and `EXT43B6Q`, for ordinary and mSATA 840 EVO firmware packages.

That supports:

> **firmware artifact identity is variant-specific**.

It does **not** support:

> `EXT0DB6Q algorithm != EXT43B6Q algorithm`.

Two packages can differ for many reasons: packaging, device configuration, board/form-factor integration, controller parameters, model identification, or implementation code. No inspected source exposes a binary comparison or Samsung's internal code history.

### A rollout lag is not a physical-causality proof

The mSATA variant received the public 2015 remediation later than the ordinary 840 EVO. That historical fact does not identify why.

Therefore:

```text
later mSATA release
    !=
proof that mSATA form factor physically caused the delay
```

No claim is made here about controller stepping, NAND package, thermal behavior, validation burden, firmware branch divergence, staffing, or product priority unless a future primary source documents it.

### Historical support state is versioned

The same named product family can have different maintenance possibilities at different dates:

```text
840 EVO mSATA, April 2015
    !=
840 EVO mSATA, August 2015 host-tool state
    !=
840 EVO mSATA, October 2015 EXT43B6Q state
    !=
later Magician-supported 840 EVO mSATA state
```

The physical drive model name remains recognizable across those dates, but the available maintenance relation changes because firmware/tooling/support state changes.

This is not a claim that the user's payload identity changed. It is a claim about the **apparatus available to maintain service performance**.

## Functional comparisons and limits

### To Case 104 — optional Mobile DDR capability

Useful analogy:

- Case 104 shows that a product-family or standards-era capability name does not prove that every concrete product/order supports the feature;
- this Case 37 slice shows that a product-family name does not prove simultaneous maintenance-feature availability across variants and dates.

Limit:

- LPDDR DPD is a memory power-mode capability;
- Samsung 840 EVO Advanced Performance Optimization / periodic refresh belongs to SSD firmware and host-tool remediation;
- no shared implementation or genealogy is asserted.

### To Case 150 — SSD maintenance opportunity

Useful analogy:

- both cases show that `device exists and contains readable data` is weaker than `the required maintenance path is currently available`.

Limit:

- Case 150 concerns powered-idle / sleep-state opportunity for garbage collection;
- this slice concerns model/firmware/software eligibility for a product-specific old-data performance remediation path.

The trigger, maintenance work, and historical systems are different.

## Philosophical interpretation — bounded

The technical pressure point is that a device's nominal identity does not exhaust its historically available capacities.

A thing called `Samsung 840 EVO` can remain materially and commercially the same family while the relations that make a particular maintenance operation available change through firmware, software, model variant, and date.

The bounded interpretive result is:

> Technical availability is historically configured, not simply contained in a timeless product name.

This is a project interpretation, not Samsung's historical vocabulary. It should not be inflated into a general claim that firmware defines the identity of every digital object.

## Explicit non-claims

This record does **not** claim that:

1. mSATA's physical form factor caused the later remediation rollout;
2. `EXT43B6Q` uses a fundamentally different refresh algorithm from `EXT0DB6Q`;
3. equal current ISO sizes imply binary or algorithmic identity;
4. the April 2015 public exclusion proves Samsung had no internal mSATA firmware under development;
5. Magician 4.7 alone performed the maintenance without device firmware;
6. firmware installation alone proves Advanced Performance Optimization completed successfully;
7. one PC Perspective test proves fleet-wide mSATA behavior;
8. current Samsung firmware hosting proves the original 2015 release date;
9. the later 2018 common support list means both form factors had the feature in April 2015;
10. Advanced Performance Optimization and the firmware's autonomous periodic refresh are the same operation;
11. the product incident establishes uncorrectable data loss;
12. all TLC NAND or all Samsung SSD families share this rollout pattern;
13. Samsung copied Cai et al.'s FCR mechanism;
14. the staggered rollout establishes invention priority or an actor-to-actor genealogy;
15. the surviving current firmware files remain suitable for every present-day machine or execution environment.

## Claim ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| Samsung's current official firmware ledger separately lists 840 EVO `EXT0DB6Q` and 840 EVO mSATA `EXT43B6Q` | `H/P-current` | strong manufacturer-primary artifact identity; no original-release-date inference |
| On 28 April 2015 PC Perspective reported that the then-current standalone update did not apply to mSATA 840 EVO | `H/S-period` | contemporary technical report; not a Samsung specification |
| Magician 4.7 release-note text preserved on 31 August 2015 added Advanced Performance Optimization support for 840 EVO mSATA and required new firmware | `H/S-vendor-provenance` | secondary preservation attributed to Samsung; direct 2015 Samsung PDF not yet recovered |
| On 1 October 2015 PC Perspective identified `EXT43B6Q` as available for mSATA and demonstrated Advanced Performance Optimization on a 1 TB sample | `H/S-period + test` | one observed sample; not fleet proof |
| Samsung's 2018 Magician guide lists Advanced Performance Optimization for 840 EVO 2.5-inch and mSATA | `H/P-later` | eventual feature scope only |
| Same product family implies simultaneous remediation availability | `X` | contradicted by the April→October 2015 rollout record |
| Distinct firmware identifiers prove distinct internal refresh algorithms | `X` | unsupported |
| Later common feature scope proves common introduction date | `X` | anachronistic projection rejected |
| Form factor explains the cause of the rollout delay | `X` | unsupported |
| Host-tool support alone proves the device can execute the maintenance function | `X` | release-note evidence itself says new firmware is required |

## Related-repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `840 EVO`, `Samsung 840 EVO`, and old-data refresh found no dedicated case to reuse.

A broader history of Samsung TLC NAND, controller/firmware branches, mSATA versus 2.5-inch hardware design, and product-validation organization belongs primarily there if developed. This file remains bounded to the **retention-maintenance availability relation** exposed by the staggered 2015 remediation rollout.

## Open work after this slice

The form-factor rollout boundary is now grounded at the public artifact/reporting level. Remaining work is narrower:

- recover a Samsung-hosted or archived byte-identical **Magician 4.7 Installation Guide / release notes** from 2015 so the mSATA feature-addition line can be upgraded from vendor-provenance secondary preservation to direct first-party inspection;
- recover Samsung's original dated release page or release note for `EXT43B6Q`;
- recover the April 2015 Samsung FAQ / Magician 4.6 documentation body already listed as Case 37 debt;
- compare the two firmware packages only if a source-controlled binary-analysis question is justified; package identity alone must not become algorithm speculation;
- find primary engineering evidence, if any, for why the mSATA rollout lagged;
- add independent named-drive fault/power-cut testing only as a separate experiment/evidence slice, not as a substitute for historical rollout evidence.

## Sources

1. Samsung Semiconductor, **Tool & Software Download**, current firmware ledger. Separately lists 840 EVO `EXT0DB6Q` and 840 EVO mSATA `EXT43B6Q`: <https://semiconductor.samsung.com/consumer-storage/support/tools/>.
2. Allyn Malventano, **“Samsung 840 EVO Standalone ISO Updater Now Available,”** *PC Perspective*, 28 April 2015: <https://pcper.com/2015/04/samsung-840-evo-standalone-iso-updater-now-available/>.
3. Tweakers, **“Software-update: Samsung Magician 4.7,”** 31 August 2015, preserving release-note text attributed to Samsung: <https://tweakers.net/downloads/35337/samsung-magician-47.html>.
4. Allyn Malventano, **“Samsung 840 EVO mSATA Gets Long Awaited EXT43B6Q Firmware, Fixes Read Speed Issue,”** *PC Perspective*, 1 October 2015: <https://pcper.com/2015/10/samsung-840-evo-msata-gets-long-awaited-ext43b6q-firmware-fixes-read-speed-issue/>.
5. Samsung Electronics, **Samsung Magician 5.2.1 Installation Guide**, Rev. 2.4, June 2018, p. 7: <https://semiconductor.samsung.com/resources/data-sheet/Samsung_Magician_5_2_1_Installation_Guide_v2.4.pdf>.
6. Existing canonical case and grounding record: [`../cases/37-samsung-840-evo-old-data-performance-refresh.md`](../cases/37-samsung-840-evo-old-data-performance-refresh.md) and [`37-samsung-840-evo-2014-2015-performance-refresh-grounding.md`](37-samsung-840-evo-2014-2015-performance-refresh-grounding.md).
