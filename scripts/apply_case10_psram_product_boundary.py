from pathlib import Path

ROOT = Path('.')
EVIDENCE = ROOT / 'evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md'
if not EVIDENCE.exists():
    raise SystemExit('pre-staged evidence file missing')

case = ROOT / 'cases/10-toshiba-leakage-tracked-self-refresh.md'
text = case.read_text(encoding='utf-8')
product_link = "Named-product boundary deepening: [`../evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md`](../evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md)."
if product_link in text:
    raise SystemExit('Case 10 already contains product-boundary deepening')
lines = text.splitlines()
prior_hits = [i for i, line in enumerate(lines) if '10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md' in line]
if not prior_hits:
    raise SystemExit('Case 10 prior-art evidence link not found')
lines.insert(prior_hits[0] + 1, '')
lines.insert(prior_hits[0] + 2, product_link)
text = '\n'.join(lines) + '\n'

section = r'''## Named-product boundary deepening — Toshiba pseudo-SRAM, 1994–2001

The patent record leaves a product-identity question open. A later Toshiba product-documentation chain now answers only the broad half of that question.

A preserved Toshiba **1994 Static RAM** data-book artifact lists the `TC51832A` family under `Pseudo Static RAM`. The preserved Toshiba family text describes a 32K×8 pseudo-static RAM using a **one-transistor dynamic memory cell**, while exposing an SRAM-like interface. It says the `RFSH` input supports both `Auto Refresh` and `Self Refresh`; the feature list separately says **Self refresh is supported by an internal timer** and **Auto refresh is supported by an internal refresh-address counter**, with 256 refresh cycles / 4 ms. Because the raw Bitsavers PDF could not be directly rendered in this pass and the detailed text was corroborated through a manufacturer-datasheet mirror, these lines are treated as `H/P*` pending direct facsimile page anchors rather than overstated as fully inspected page evidence. See the [named-product evidence addendum](../evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md).

Toshiba's official **18 June 2001** launch announcement supplies a second manufacturer-primary product witness. It names the `TC51W3216XB`, describes a standard SRAM interface over a one-transistor DRAM-like cell, explicitly advertises self refresh, and says a separate DRAM controller / refresh glue logic is unnecessary. The same announcement gives planned sample and full-production timing.

These sources move the product boundary, but they do not collapse it into the patent mechanism:

> **named-product self refresh != named-product leakage-tracked self refresh**

The `TC51832A` product text says `internal timer`; it does not document the preferred US4682306A leak-current-monitor capacitor, threshold detector, or refresh-frequency dependence on measured leakage. A timer cannot be silently renamed a leakage monitor merely because both can start autonomous maintenance.

The stronger decomposition is now:

```text
one-transistor dynamic payload
    !=
SRAM-like service interface
    !=
refresh-row enumeration
    !=
autonomous refresh timing
    !=
leakage-derived/adaptive refresh trigger
```

This also supplies a bounded comparison to Case 21. Both Toshiba pseudo-SRAM and Micron SDRAM can internalize recurring refresh work, but their external interfaces and documented mode semantics differ. The comparison is functional, not a Toshiba→Micron or patent→JEDEC genealogy.

Finally, Toshiba's 2001 statement that a separate refresh controller/glue logic is unnecessary is an interface-placement result, not evidence that maintenance disappeared:

> **external refresh burden removed != refresh obligation removed**.

The physical payload remains dynamic in the named product descriptions, and `Self Refresh` does not establish unpowered nonvolatility.

'''
if '## Failure boundaries\n' not in text:
    raise SystemExit('Case 10 Failure boundaries heading missing')
text = text.replace('## Failure boundaries\n', section + '## Failure boundaries\n', 1)

lines = text.splitlines()
ledger_hits = [i for i, line in enumerate(lines) if line.startswith('| A named Toshiba commercial part is proven to use this exact circuit |')]
if len(ledger_hits) != 1:
    raise SystemExit(f'Case 10 exact-circuit ledger row count={len(ledger_hits)}')
i = ledger_hits[0]
lines[i:i+1] = [
    "| A named Toshiba pseudo-SRAM family is documented with Auto Refresh and Self Refresh | H/P* | Toshiba 1994 data-book artifact + preserved `TC51832A` family text |",
    "| `TC51832A` Self Refresh is documented as using an internal timer while Auto Refresh uses an internal refresh-address counter | H/P* | preserved Toshiba family text; direct facsimile page anchors remain open |",
    "| Toshiba publicly announced a named `TC51W3216XB` pseudo-SRAM with a one-transistor DRAM-like cell, SRAM interface, and self refresh in 2001 | H/P | Toshiba corporate release, 18-Jun-2001 |",
    "| Named-product self refresh proves deployment of the US4682306A leak-monitor threshold path | X | product evidence does not expose the patent's monitor/threshold mechanism |",
    "| A named Toshiba commercial part is proven to use this exact leakage-tracked circuit | X | still unsupported; broad self-refresh productization is now grounded, exact circuit identity is not |",
]
text = '\n'.join(lines) + '\n'

lines = text.splitlines()
source_hits = [i for i, line in enumerate(lines) if 'A 288Kb CMOS Pseudo SRAM' in line and line.lstrip().startswith('3.')]
if len(source_hits) != 1:
    raise SystemExit(f'Case 10 Kawamoto source anchor count={len(source_hits)}')
i = source_hits[0]
lines[i:i+1] = [
    "3. Toshiba, **1994 Static RAM** data book, preserved scan: <https://www.bitsavers.org/components/toshiba/_dataBook/1994_Toshiba_Static_RAM.pdf>.",
    "4. Toshiba Semiconductor, **TC51832A family / TC51832AP, 32,768 word × 8-bit CMOS Pseudo Static RAM**, preserved manufacturer-datasheet mirror: <https://www.alldatasheet.com/datasheet-pdf/pdf/1462395/TOSHIBA/TC51832AP.html>.",
    "5. Toshiba Corporation, **“Toshiba Announces its 32Mb Pseudo SRAM Solution,”** 18 June 2001: <https://www.global.toshiba/ww/news/corporate/2001/06/pr1802.html>.",
    "6. H. Kawamoto et al., “A 288Kb CMOS Pseudo SRAM,” _ISSCC Digest of Technical Papers_, 1984, pp. 276–277, DOI 10.1109/ISSCC.1984.1156683 — period context cited by the patent, not a central mechanism source in this case.",
]
case.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')

roadmap = ROOT / 'ROADMAP.md'
road_lines = roadmap.read_text(encoding='utf-8').splitlines()
if any('10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md' in line for line in road_lines):
    raise SystemExit('ROADMAP already contains Case 10 product boundary')
hits = [i for i, line in enumerate(road_lines) if line.startswith('- [ ] DRAM evolution and refresh machinery beyond the bounded case')]
if len(hits) != 1:
    raise SystemExit(f'ROADMAP broad DRAM item count={len(hits)}')
road_line = "- [x] Case 10 named-product pseudo-SRAM self-refresh boundary deepening — [`cases/10-toshiba-leakage-tracked-self-refresh.md`](cases/10-toshiba-leakage-tracked-self-refresh.md), with new [`evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md`](evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md), now separates broad productization of autonomous self refresh from deployment of the 1984-priority patent's specific leakage-derived trigger. Toshiba's 1994 static-RAM data-book record documents the named `TC51832A` pseudo-static-RAM family as one-transistor dynamic storage with SRAM-like service, internal-counter Auto Refresh, and internal-timer Self Refresh; Toshiba's official 18-Jun-2001 `TC51W3216XB` launch independently grounds a named pseudo-SRAM product with DRAM-like cell, SRAM interface, self refresh, and reduced external refresh-controller/glue-logic burden. This closes only `named Toshiba product self-refresh exists`; exact leak-monitor/comparator product identity, direct 1994 page-image anchors, first-sale chronology, patent→product genealogy, JEDEC evolution, and fault validation remain open."
road_lines.insert(hits[0], road_line)
road_lines.insert(hits[0] + 1, '')
roadmap.write_text('\n'.join(road_lines).rstrip() + '\n', encoding='utf-8')

index = ROOT / 'CASE_INDEX.md'
idx_lines = index.read_text(encoding='utf-8').splitlines()
case_rows = [i for i, line in enumerate(idx_lines) if line.startswith('| [Toshiba Leakage-Tracked Self-Refresh:')]
if len(case_rows) != 1:
    raise SystemExit(f'CASE_INDEX Case 10 row count={len(case_rows)}')
i = case_rows[0]
row = idx_lines[i]
if '10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md' in row:
    raise SystemExit('CASE_INDEX Case 10 row already updated')
if 'named-product implementation' not in row:
    raise SystemExit('CASE_INDEX Case 10 named-product phrase missing')
row = row.replace('[Hitachi 1982–1984 prior-art deepening](evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md);', '[Hitachi 1982–1984 prior-art deepening](evidence/10-hitachi-1982-1984-leakage-comparator-self-refresh-prior-art.md) + [1994–2001 named-product self-refresh boundary](evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md);', 1)
row = row.replace('pre-1982 genealogy, named-product implementation, later standards/self-refresh evolution, and modern retention-aware policy remain separate work', 'pre-1982 genealogy, exact named-product deployment of the leakage-monitor trigger, later standards/self-refresh evolution, and modern retention-aware policy remain separate work', 1)
idx_lines[i] = row
idx = '\n'.join(idx_lines).rstrip()
if '**2576 —' in idx or '**2589 —' in idx:
    raise SystemExit('CASE_INDEX finding range already exists')
findings = r'''

## Case 10 deepening — Toshiba pseudo-SRAM named-product self-refresh findings

Evidence: [`evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md`](evidence/10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md)

- **2576 — 1994 manufacturer data-book presence != first-sale or invention date.** Toshiba's static-RAM catalog gives a conservative named-product documentation floor for the `TC51832A` family; it does not establish first shipment, first Toshiba pseudo-SRAM, or private conception. (`H/P*`, `X`)
- **2577 — pseudo-static interface != static physical retention.** The `TC51832A` product text combines an SRAM-like interface with a one-transistor dynamic memory cell, so service appearance and payload-retention mechanism must remain distinct. (`H/P*`, `E`)
- **2578 — one RFSH pin != one refresh relation.** The bounded product text exposes both Auto Refresh and Self Refresh through the refresh interface while assigning different internal support mechanisms to them. (`H/P*`, `E`)
- **2579 — internal refresh-address counter != internal self-refresh timer.** Row enumeration and recurring maintenance timing are separately named product functions, independently reinforcing the Case-09/Case-10 control-locus decomposition. (`H/P*`, `E`)
- **2580 — internal timer != demonstrated leakage monitor.** The product description does not identify the timer as US4682306A's leak-current-monitor capacitor/threshold path or as a refresh-frequency sensor of actual leakage. (`H/P*`, `X`)
- **2581 — named-product self refresh != named-product leakage-tracked self refresh.** Broad autonomous-maintenance productization is now grounded, while the specific adaptive/leakage-derived trigger remains an unproven product-identity claim. (`H/P*`, `E`, `X`)
- **2582 — self refresh != nonvolatility.** A dynamic-cell device that autonomously refreshes while powered has not thereby acquired unpowered retention. (`H/P*`, `E`, `X`)
- **2583 — external refresh-controller/glue-logic removal != refresh-obligation removal.** Toshiba's 2001 announcement markets simpler system integration while simultaneously describing a DRAM-like cell and self refresh; maintenance moved behind the interface rather than disappearing. (`H/P`, `E`)
- **2584 — 2001 availability plan != field-deployment validation.** Toshiba's official launch establishes a named commercial offering and stated sample/full-production schedule, not measured retention behavior in deployed systems or the internals of shipped lots. (`H/P`, `X`)
- **2585 — TC51832A and TC51W3216XB sharing Toshiba pseudo-SRAM/self-refresh vocabulary != one proven circuit genealogy.** The two product records are continuity witnesses for the product class, not evidence that they share the same timer, monitor, array, or patent embodiment. (`H/P`, `A`, `X`)
- **2586 — Toshiba pseudo-SRAM self refresh != Micron SDRAM Case-21 mode semantics.** Both internalize recurring preservation work, but SRAM-like RFSH operation and synchronous CKE/command/tXSR handoff are different interfaces and mechanisms. (`A`, `X`)
- **2587 — interface simplification can conceal maintenance without making persistence passive.** The surrounding system can lose an explicit refresh-scheduling burden while the retained dynamic payload still depends on recurring internal work. (`E`, `I`)
- **2588 — mirrored manufacturer text != completed facsimile inspection.** Because the Bitsavers 1994 PDF could not be rendered in this pass, detailed `TC51832A` claims remain marked `H/P*` pending direct page-image/page-number anchors rather than being overstated as fully inspected evidence. (`H/P*`, `X`)
- **2589 — related-repository boundary:** fresh `computing-archaeology` searches for `TC518512`, `TC51832`, and `pseudo SRAM` returned no dedicated case to reuse; broad pseudo-SRAM product/standards history belongs there if developed, while Case 10 keeps the retention-specific productization-versus-trigger-identity distinction. (`H/P` project-state record)
'''
index.write_text(idx + findings.rstrip() + '\n', encoding='utf-8')

case2 = case.read_text(encoding='utf-8')
assert 'named-product self refresh != named-product leakage-tracked self refresh' in case2
assert 'TC51832A' in case2 and 'TC51W3216XB' in case2
road2 = roadmap.read_text(encoding='utf-8')
assert '10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md' in road2
idx2 = index.read_text(encoding='utf-8')
for n in range(2576, 2590):
    marker = f'**{n} —'
    if idx2.count(marker) != 1:
        raise SystemExit(f'finding {n} count={idx2.count(marker)}')
assert idx2.count('10-toshiba-1994-2001-pseudo-sram-product-self-refresh-deepening.md') >= 2
print('Case 10 pseudo-SRAM named-product boundary applied successfully')
