from pathlib import Path
import re

roadmap_path = Path('ROADMAP.md')
roadmap = roadmap_path.read_text(encoding='utf-8')
roadmap_lines = roadmap.splitlines()
new_decay = "- [ ] decay and leakage — **substantially advanced at the DRAM physical-state layer by grounded Cases 03 and 127, and now partially advanced at the environmental Flash-retention layer by grounded Case 132**: Case 03 grounds leakage as the reason ordinary powered DRAM requires periodic restoration before a service deadline; Case 127 crosses the maintenance boundary and shows that after refresh/power withdrawal the tested SDRAM/DDR/DDR2 modules decayed gradually rather than instantaneously, with strong temperature dependence and structured cell-specific ground states. Case 132 adds a bounded 2015 commercial serial-Flash experiment that separates storage survival from active operation: four warm verification checks across 24 months of approximately -130 °C to -195 °C storage found no bit errors in the tested pattern, while cryogenic program/erase timing and pass rates degraded sharply and recovered after warm-up. This grounds `refresh deadline ≠ physical decay timestamp`, `volatile service loss ≠ immediate physical erasure`, `retention-valid environment ≠ full-operation-valid environment`, and `same temperature intervention ≠ same DRAM/Flash mechanism`. Direct Link/May 1979 facsimile inspection, later DDR generations, Flash/EEPROM charge-loss kinetics beyond this device-level cryogenic result, elevated-temperature acceleration, longer independent replication, and controlled fault injection remain open;"
matched = False
for i, line in enumerate(roadmap_lines):
    if line.startswith('- [ ] decay and leakage —'):
        roadmap_lines[i] = new_decay
        matched = True
        break
if not matched:
    if 'environmental Flash-retention layer by grounded Case 132' not in roadmap:
        raise AssertionError('ROADMAP decay/leakage line not found')
else:
    roadmap_path.write_text('\n'.join(roadmap_lines) + '\n', encoding='utf-8')

index_path = Path('CASE_INDEX.md')
index = index_path.read_text(encoding='utf-8')
case_path = 'cases/132-cryogenic-serial-flash-retention-operability.md'
if case_path not in index:
    lines = index.splitlines()
    insertion = None
    for i, line in enumerate(lines):
        if 'cases/131-dell-perc-foreign-configuration-controller-replacement.md' in line:
            insertion = i + 1
            break
    assert insertion is not None, 'Case 131 table row not found'
    row = "| [Cryogenic Serial Flash: Retention Without Full Cryogenic Operability](cases/132-cryogenic-serial-flash-retention-operability.md) | **grounded** | nonvolatile serial Flash + cryogenic storage + periodic warm verification + temperature-dependent command envelope | separate stored-state survival from active operation; show environmental conditions can preserve a written pattern while program/erase service degrades; bound reversible low-temperature failure and zero-error observations | [2015 cryogenic serial-Flash grounding](evidence/132-2015-cryogenic-serial-flash-grounding.md); longer-duration replication, elevated-temperature comparison, raw-cell charge-loss kinetics, named modern products, and independent fault testing remain open |"
    lines.insert(insertion, row)
    index = '\n'.join(lines) + '\n'

heading = '## Case 132 — cryogenic serial-Flash environmental-retention findings'
if heading not in index:
    assert '**2374 —' in index, 'expected previous finding 2374 missing'
    findings = '''
## Case 132 — cryogenic serial-Flash environmental-retention findings

- **2375 — bounded cryogenic storage survival is directly observed, not inferred from device nonvolatility.** Ihmig, Shirley, and Zimmermann's 2015 experiment used a separate 100-IC-per-batch retention group and reported four checks over 24 months with no observed bit errors in the stored `ALL55` pattern under approximately -130 °C to -195 °C storage. (`H/P`)
- **2376 — retention-valid environment ≠ full-operation-valid environment.** The same study found strong low-temperature program/erase slowdown and batch-dependent functional failures even though the separately stored retention group remained recoverable at scheduled checks. (`H/P`, `E`)
- **2377 — stored-state survival ≠ successful write/erase service.** A written Flash pattern can remain recoverable while page program or sector erase becomes too slow or fails at the current temperature. (`E`)
- **2378 — reversible cryogenic operation failure ≠ permanent device failure.** Group-1 devices that failed at low temperature generally returned to proper room-temperature operation after warm-up, so current environmental unavailability is weaker than irreversible technical loss. (`H/P`, `E`)
- **2379 — periodic verification ≠ continuous service.** The long-duration retention group was periodically warmed and checked rather than demonstrated as continuously online at cryogenic temperature. (`H/P`, `E`)
- **2380 — successful warm verification ≠ demonstrated in-situ cryogenic read/write availability.** The experimental procedure establishes recoverability through a cold-store-to-warm-read path, not a universal command guarantee inside the storage environment. (`H/P`, `X`)
- **2381 — zero observed bit errors ≠ universal archival retention law.** A finite batch set, test pattern, 24-month window, and verification procedure cannot be promoted into a technology-wide lifetime or zero-failure guarantee. (`E`, `X`)
- **2382 — batch/process sensitivity ≠ one universal serial-Flash temperature threshold.** Six batches manufactured from 2007 to 2012 showed materially different low-temperature pass behavior under a common commercial-device framing. (`H/P`, `X`)
- **2383 — low-temperature program/erase slowdown ≠ evidence of payload loss.** Increased command latency is an operational-margin result and must not be redescribed as retention failure without bit-error evidence. (`H/P`, `E`)
- **2384 — environmental preservation can create mode-switching maintenance without DRAM-like refresh.** Cryogenic storage, temperature/liquid monitoring, scheduled warm verification, and possible warm-time rewriting form a retention workflow around a nonvolatile device; this is different from periodically restoring the Flash payload merely to keep it alive. (`E`)
- **2385 — the same cooling intervention ≠ the same DRAM/Flash retention mechanism.** Case 127 concerns a volatile residual-charge window after DRAM maintenance withdrawal; Case 132 concerns already-written nonvolatile Flash plus an environmentally narrowed command envelope. The comparison is functional/environmental only. (`A`, `X`)
- **2386 — component cryogenic experiment ≠ JESD218 SSD retention contract.** Case 76 composes workload, host TBW, error criteria, temperatures, and power-off retention at the SSD service level; Case 132 is a device-level experiment outside ordinary operating conditions. (`A`, `X`)
- **2387 — the 2015 experimental floor ≠ invention priority for cryogenic Flash or low-temperature memory.** The paper directly grounds this bounded batch study but does not establish origin of the broader practice or phenomenon. (`H/P`, `X`)
- **2388 — related-repository boundary remains explicit.** Fresh `tmzncty/computing-archaeology` searches for `cryogenic` and `serial flash` found no dedicated case to reuse; broader cryogenic-electronics, Flash product/process, packaging, and instrumentation history belongs there, while Case 132 retains the environmental retention/operability relation. (`H/P` project-state record)
'''
    index = index.rstrip() + '\n\n' + findings.lstrip('\n')

index_path.write_text(index.rstrip() + '\n', encoding='utf-8')

index_now = index_path.read_text(encoding='utf-8')
for n in range(2375, 2389):
    count = len(re.findall(rf'\*\*{n} —', index_now))
    assert count == 1, f'finding {n} count={count}'
assert case_path in index_now
assert 'evidence/132-2015-cryogenic-serial-flash-grounding.md' in index_now
assert 'environmental Flash-retention layer by grounded Case 132' in roadmap_path.read_text(encoding='utf-8')
