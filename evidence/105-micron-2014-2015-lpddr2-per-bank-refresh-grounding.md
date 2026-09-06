# Micron 2014–2015 LPDDR2 per-bank REFRESH grounding record

This record grounds [`../cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md`](../cases/105-micron-lpddr2-per-bank-refresh-maintenance-granularity.md).

The question is deliberately narrow: can a DRAM refresh transaction be localized to one bank while the retention obligation still covers the full bank set over time, and how does that differ from Case 104's PASR reduction of the retained set?

## Source A — Micron 168-ball single-channel Mobile LPDDR2, Rev. A 07/14

Micron Technology, Inc., _168-Ball, Single-channel Mobile LPDDR2 SDRAM_, PDF ID `09005aef85c99ac2`, filename `168b_12x12_4-16gb_2e0e_lpddr2.pdf`, Rev. A, July 2014.

Manufacturer PDF mirror:
<https://www.mouser.com/datasheet/2/671/168b_12x12_4%2016gb_2e0e_mobile%20lpddr2-1283387.pdf>

The direct PDF text and exact printed-page locations were inspected. Page-image rendering was also attempted in the research environment but the remote cache did not return the page images, so this record does not claim figure-level visual inspection.

### A1. Feature-level scope

**Printed p. 1.**

The feature list gives `8 internal banks for concurrent operation` and `Per-bank refresh for concurrent operation`, while ATCSR, PASR, and DPD are listed as separate features.

This immediately blocks a vocabulary collapse:

> per-bank refresh ≠ PASR ≠ self refresh ≠ DPD.

### A2. REFpb target selection and controller tracking

**Printed p. 81.**

Micron says REFpb performs a per-bank refresh on the bank scheduled by an internal bank counter. For this eight-bank device family, the sequence is fixed round-robin `0-1-2-3-4-5-6-7-...`.

The bank count can be synchronized between controller and SDRAM by resetting it to zero, including through RESET or exit from self refresh. Micron explicitly requires the controller to track the bank being refreshed.

This supports a bounded maintenance-control relation:

> maintenance target tracking state ≠ payload state.

It does not expose the physical implementation of the counter or controller bookkeeping.

### A3. Target-bank unavailability and non-target concurrency

**Printed p. 82.**

Micron states that the target bank is inaccessible during `tRFCpb`, while other banks remain accessible/addressable. Non-target banks may remain active or receive READ/WRITE commands. After the REFpb cycle, the affected bank is idle.

This directly grounds:

- bank-local maintenance ≠ whole-device service blackout;
- target-bank maintenance interval ≠ target-bank ordinary-service interval;
- service availability of non-target banks ≠ completion of target-bank maintenance.

The idle precondition is a command-admission rule, not evidence that the target bank contains no data.

### A4. REFab and bank-count synchronization

**Printed p. 82.**

REFab applies refresh to all banks, requires all banks idle, and synchronizes the bank count between controller and SDRAM to zero.

This establishes that REFab and REFpb differ in service/admission geometry even when later refresh accounting can substitute a complete REFpb cycle for one REFab.

### A5. Rolling-window refresh obligation and full REFpb cycle

**Printed p. 83.**

Micron defines a minimum number `R` of REFab commands within any rolling refresh window `tREFW`. For devices supporting per-bank refresh, it states that one REFab may be replaced by a **full cycle of eight REFpb commands**.

That sentence is the central evidence for Case 105:

> per-bank maintenance-event granularity ≠ partial retained-set policy.

A single REFpb covers one target maintenance event; the refresh obligation composes a sequence of such events across banks and time.

The same section also permits burst/distributed refresh scheduling under window constraints. This supports scheduling elasticity but not unlimited postponement.

## Source B — Micron 1Gb Automotive Mobile LPDDR2, Rev. B 12/14

Micron Technology, Inc., _1Gb: x16, x32 Automotive Mobile LPDDR2 SDRAM_, PDF ID `09005aef85d5f0c6`, filename `1gb_mobile_lpddr2_u88m_ait_aat.pdf`, Rev. B, December 2014.

Text-preserving mirror:
<https://dtsheet.com/doc/1384685/1gb--x16--x32-automotive-lpddr2-sdram>

The refresh-command section repeats the controller-tracking requirement: the controller must track the bank being refreshed by REFpb; the bank count can be synchronized to zero through RESET or exit from self refresh. The document also retains bank-idle and `tRFCpb`/`tRFCab` separation constraints.

Use of Source B is conservative. It is a same-manufacturer product-family continuity check, not an independent lab validation and not evidence of invention priority.

## Source C — Micron 512Mb Automotive Mobile LPDDR2, Rev. A 07/15

Micron Technology, Inc., _512Mb: x32 Automotive Mobile LPDDR2 SDRAM_, PDF ID `09005aef86573be0`, filename `512mb_mobile_lpddr2_u97m_ait_aat_aut.pdf`, Rev. A, July 2015.

Text-preserving mirror:
<https://dtsheet.com/doc/1384686/512mb--x32-automotive-mobile-lpddr2-sdram>

This later manufacturer document again requires the controller to track the bank being refreshed by REFpb, repeats the bank-idle precondition, and preserves distinct `tRFCpb`/`tRFCab` timing constraints. It is used only as a 2015 continuity witness for the bounded interface relation, not as independent validation and not as an origin claim.

## Relation to Case 104

Case 104 grounds PASR in a later Micron LPDDR family as a **retention coverage** policy: in self refresh, excluded regions are not refreshed and their data are not promised survival.

Source A grounds REFpb as a **maintenance transaction** policy: one bank is refreshed per transaction, but a complete eight-bank cycle substitutes for one all-bank refresh in the rolling refresh accounting.

Therefore:

```text
PASR
    selected maintained set can shrink

REFpb
    one maintenance transaction can shrink in spatial scope
    while aggregate bank coverage remains required
```

The words `partial` and `per-bank` are not interchangeable descriptions of one retention mechanism.

## Source hierarchy and limitations

| Claim | Label | Locator | Strength |
| --- | --- | --- | --- |
| Micron markets per-bank refresh as supporting concurrent operation | H/P | Source A, printed p. 1 | strong manufacturer-primary |
| REFpb follows a fixed eight-bank round-robin target sequence | H/P | Source A, printed p. 81 | strong manufacturer-primary |
| controller tracks the bank being refreshed | H/P | Source A, p. 81; Sources B/C continuity | strong manufacturer-primary, same-vendor corroboration |
| target bank unavailable while other banks may be READ/WRITE-accessed | H/P | Source A, printed p. 82 | strong manufacturer-primary |
| REFab refreshes all banks and resynchronizes bank count | H/P | Source A, printed p. 82 | strong manufacturer-primary |
| one REFab can be replaced by a full cycle of eight REFpb commands | H/P | Source A, printed p. 83 | strong manufacturer-primary |
| transaction scope and retained-set scope are different relations | E | bounded reconstruction from A3/A5 + Case 104 | strong mechanism inference |
| Micron/2014 originated per-bank refresh | X | not established | rejected |
| REFpb and PASR are historically/mechanically identical | X | contradicted by source semantics | rejected |

## Historical cautions

- The main source is a genuine Micron manufacturer PDF preserved by Mouser; the mirror is not independent validation.
- Sources B and C are same-vendor continuity witnesses, not independent corroboration.
- A precise July 2014 product-document witness is not an origin date.
- No complete JEDEC revision chronology is reconstructed here.
- `REFpb cycle completion` must be scoped to one maintenance transaction, not promoted to a whole-array correctness certificate.
- Bank-count synchronization is maintenance bookkeeping, not proof that every payload bit is correct or newly restored.
- The controller-tracking obligation does not tell us how every shipping controller represented or persisted that state.
- Functional similarity to later DDR/LPDDR per-bank/same-bank refresh does not establish direct genealogy.

## Related-repository check

A current GitHub search of `tmzncty/computing-archaeology` for LPDDR2 `REFpb` / `per-bank refresh` did not expose a dedicated case. A full standards genealogy, earlier vendor prior art, controller scheduling implementation, power/performance modeling, and later per-bank/same-bank-refresh evolution belong there if developed comprehensively.
