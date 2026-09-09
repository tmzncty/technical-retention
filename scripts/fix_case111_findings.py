from pathlib import Path
import re

p = Path('CASE_INDEX.md')
s = p.read_text(encoding='utf-8')
start = '1713. **rated-life estimate ≠ immediate device-failure verdict**'
pos = s.find(start)
if pos < 0:
    raise SystemExit('staged Case 111 finding block not found')
# The mistaken block is at EOF and contains 13 lines, 1713..1725.
prefix = s[:pos].rstrip()
block = '''## Case 111 deepening — NetApp rated-life / offline-retention telemetry findings

Evidence: [`evidence/111-netapp-rated-life-offline-retention-telemetry-deepening.md`](evidence/111-netapp-rated-life-offline-retention-telemetry-deepening.md)

- **2488 — rated-life estimate ≠ immediate device-failure verdict.** NetApp says `Rated Life Used >99` means estimated endurance has been consumed but does not necessarily indicate device failure. (`H/P`, `E`)
- **2489 — current readable service ≠ qualification for long powered-off retention.** NetApp warns that an SSD at 100% rated life might not retain data through long power-off even though the threshold is not defined as immediate online failure. (`H/P`, `E`)
- **2490 — 90%/95% warning thresholds ≠ 100% replacement action.** ONTAP escalates NOTICE→ERROR→ALERT and changes the operator action at end of rated life; the thresholds are an operational policy ladder, not one physical state. (`H/P`, `E`)
- **2491 — threshold crossing ≠ deterministic bit-loss instant.** The vendor wording is `might not be able to retain`; it does not define a day, temperature-independent cliff, or one cell-level failure event. (`H/P`, `X`)
- **2492 — past-usage forecast ≠ wall-clock guarantee.** The remaining-weeks field is described as an estimate based on past usage; the internal model and future workload assumptions are not exposed. (`H/P`, `E`, `X`)
- **2493 — retained health telemetry can qualify future payload retention without being payload.** Rated-life state participates in replacement/offline-retention decisions while remaining device-health/control evidence. (`H/P`, `E`)
- **2494 — rated-life estimate ≠ spare-block consumption.** `storage disk show -ssd-wear` exposes Rated Life Used separately from Spare Blocks Consumed and its limit; one host-visible wear scalar cannot stand in for the other. (`H/P`, `E`)
- **2495 — wear-state admission policy ≠ periodic power-up maintenance schedule.** NetApp gates long-offline trust by rated life, whereas the bounded IBM/Dell sources prescribe powered intervals/maintenance opportunity. (`H/P`, `A`, `X`)
- **2496 — operator replacement ≠ proof of present physical unreadability.** A service policy can retire a drive conservatively before the historical record proves current payload loss. (`H/P`, `E`, `X`)
- **2497 — JESD218 rated-endurance relation ≠ current field estimate of remaining margin.** Case 76 supplies the qualification relation; NetApp supplies an operational estimate and action after deployment. (`A`, `E`)
- **2498 — NVMe `Percentage Used` analogy ≠ proven NetApp field genealogy.** Case 55 provides a functionally similar model-derived endurance state, but the inspected NetApp docs do not prove a one-field implementation identity across attached drive families. (`A`, `X`)
- **2499 — May 2021 vendor-documentation floor ≠ invention priority.** The ONTAP 9.9.1 catalog directly grounds the event semantics by that publication, not their first implementation or origin. (`H/P`, `X`)
- **2500 — future-retention authority can be withdrawn while physical embodiment survives.** The system may still possess and read the SSD while retained wear evidence causes long-offline retention to be treated as inadmissible. (`E`)
'''
p.write_text(prefix + '\n\n' + block.rstrip() + '\n', encoding='utf-8')

# Catch both this run's bug and accidental duplicate canonical finding IDs.
for n in range(2488, 2501):
    token = f'- **{n} —'
    if p.read_text(encoding='utf-8').count(token) != 1:
        raise SystemExit(f'finding {n} not unique')
if re.search(r'(?m)^17(?:1[3-9]|2[0-5])\. \*\*(?:rated-life|current readable|90%|threshold|past-usage|retained health|wear-state|operator replacement|JESD218|NVMe|May 2021|future-retention)', p.read_text(encoding='utf-8')):
    raise SystemExit('mistaken finding-number block remains')
