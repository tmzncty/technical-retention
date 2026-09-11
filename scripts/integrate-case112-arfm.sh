#!/usr/bin/env bash
set -euo pipefail

git pull --ff-only origin main

EVIDENCE='evidence/112-jedec-hbm3-2022-2023-arfm-deepening.md'
if [[ -e "$EVIDENCE" ]]; then
  echo "refusing to overwrite existing $EVIDENCE" >&2
  exit 1
fi

cat > "$EVIDENCE" <<'EOF'
# Case 112 deepening evidence — HBM3 Adaptive Refresh Management policy levels, 2022–2023

## Scope

This record deepens Case 112 with one bounded correction and one bounded retention relation:

> **Adaptive Refresh Management (`ARFM`) is already present in the January-2022 JESD238 HBM3 standard, not merely a later-HBM extension. ARFM lets the controller select among vendor-published RFM threshold/decrement profiles, but changing that policy is itself constrained: outstanding RAA pressure must first be reduced to zero and one RFM level applies across all channels of the HBM3 DRAM.**

The record does not claim that HBM3 invented ARFM, reconstruct hidden victim-row selection, establish commercial controller policy, or treat an RFM level as a measured corruption threshold.

Historical/source vocabulary includes `Adaptive Refresh Management`, `ARFM`, `RFM Level`, `RAAIMT`, `RAAMMT`, `RAADEC`, `DEVICE_ID WDR`, `MR8 OP[5:4]`, `RFM required`, and `RFM not required`.

Project engineering vocabulary includes `policy level`, `maintenance-debt normalization`, `capability state`, and `selected maintenance policy`; those phrases are not attributed to JEDEC.

## Source 1 — JESD238, January 2022

**Document:** JEDEC, _High Bandwidth Memory DRAM (HBM3)_, JESD238, January 2022.  
**Public text mirror inspected:** <https://studylib.net/doc/28350036/jesd238-hbm3>

**Provenance:** the inspected document is a public mirror of JEDEC's copyrighted standard rather than the canonical JEDEC distribution endpoint. The mirror reproduces the JEDEC title page identifying `JESD238`, HBM3, and **January 2022**. This provenance limit is retained explicitly.

### H/P — ARFM is part of the January-2022 HBM3 standard

The table of contents places **Adaptive Refresh Management (ARFM)** in §6.3.2.8 immediately after ordinary Refresh Management. The inspected §6.3.2.8 states that HBM3 DRAMs may optionally support ARFM and advertise that support in the `ARFM` bit of the IEEE1500 `DEVICE_ID` WDR.

This corrects the previous Case-112 open-work wording that could be read as placing ARFM only in later HBM evolution:

```text
ARFM in JESD238 (Jan 2022)
    !=
later-HBM-only feature
```

The date is a public-standard floor, not an invention date.

### H/P — ARFM capability and default RFM requirement are distinct device fields

`DEVICE_ID` exposes separate read-only bits:

- `ARFM`: whether Adaptive Refresh Management is supported;
- `RFM`: whether Refresh Management is required under the default setting.

The same register exposes default `RAAIMT`, `RAAMMT`, and `RAADEC` fields plus alternate A/B/C versions of those fields when ARFM is supported.

Thus the public interface separates:

```text
ability to select adaptive RFM levels
    !=
default requirement to perform RFM
```

A capability bit is not itself the currently selected operating policy.

### H/P — the vendor publishes threshold profiles; the controller selects one

The standard describes the default profile plus Levels A, B, and C. `MR8 OP[5:4]` selects among them. For A/B/C the RFM requirement is `RFM is required`, and the corresponding `RAAIMT_*`, `RAAMMT_*`, and `RAADEC_*` values come from read-only `DEVICE_ID` fields set by the DRAM vendor.

The standard says increasing the RFM level increases the need for RFM commands and identifies Level C as the highest RFM level.

Bounded decomposition:

```text
vendor-provided admissible parameter profiles
    +
controller-selected RFM level
    ->
active RAA threshold/decrement policy
```

This is split authority, not evidence that the controller invents arbitrary thresholds or sees the hidden in-DRAM mitigation algorithm.

### H/P — changing the policy requires clearing existing RAA pressure

Before changing the ARFM level, the host must decrement the Rolling Accumulated ACT (`RAA`) count to **0**, using RFM or pending REF commands. The standard also requires the same RFM level on all channels of the HBM3 DRAM.

This is unusually useful retention evidence because the policy transition cannot simply reinterpret already accumulated activity history under a new threshold profile.

Engineering reconstruction:

```text
old selected RFM level
    + outstanding per-bank RAA pressure
    -> maintenance / REF until RAA = 0
    -> change level
    -> new threshold/decrement profile
```

Therefore:

> **policy change != arbitrary reclassification of outstanding maintenance debt**.

`maintenance debt` is project vocabulary for the still-accounted activation pressure; JEDEC uses RAA/RFM terminology.

### H/P — a default `RFM = 0` device can still enter an RFM-required adaptive mode

JESD238 explicitly allows an ARFM-capable HBM3 DRAM shipped with `RFM = 0` (`RFM not required`) to override that initial/default setting when the controller programs a non-default ARFM level. In that special case the DRAM treats `RFMab` / `RFMpb` as RFM commands.

This establishes a sharp boundary:

```text
RFM bit = 0 at the default level
    !=
RFM can never become required for this device
```

and:

```text
initial/default requirement state
    !=
immutable lifetime requirement state
```

The conclusion is protocol-level only. It says nothing about why a platform would choose a non-default level.

### H/P — unsupported ARFM combinations are not silently accepted

Where ARFM is not supported, non-default ARFM level selection is marked illegal/RFU rather than being a generic controller knob. This blocks another overgeneralization:

> **standard defines an ARFM level field != every HBM3 device supports adaptive-level selection**.

## Source 2 — JESD238A, January 2023

**Document:** JEDEC, _High Bandwidth Memory DRAM (HBM3)_, JESD238A, January 2023.  
**Public text mirror inspected:** <https://studylib.net/doc/27298996/jesd238a>

The inspected 2023 revision preserves the bounded ARFM relations above:

- optional ARFM capability advertised by `DEVICE_ID`;
- default plus A/B/C RFM levels;
- vendor-set read-only alternate `RAAIMT`, `RAAMMT`, and `RAADEC` values;
- controller selection through `MR8 OP[5:4]`;
- higher selected level means increased need for RFM commands;
- RAA must be reduced to zero before a level change;
- all channels of the HBM3 DRAM use the same selected level;
- an ARFM-capable device with default `RFM = 0` can make RFM operative by selecting a non-default level.

This is revision continuity across two inspected standards, not proof about every later HBM revision or product.

## Engineering reconstruction

### E — policy state sits above per-bank activity state

Case 112 already grounds per-bank RAA accounting. ARFM adds a separate policy dimension: one stack-wide selected level determines which vendor-provided threshold/decrement tuple interprets those bank-local RAA counters.

```text
per-bank retained activity summary
    !=
stack-wide selected RFM level
```

The two states compose. A local counter can determine when one bank needs management while a global policy choice determines how aggressively those counters are interpreted.

### E — “adaptive” does not mean autonomous self-tuning in the public interface

The inspected standard gives the **controller** flexibility to choose among predefined vendor profiles. It does not establish that the DRAM autonomously chooses Level A/B/C from workload observations, temperature, or observed faults.

Therefore:

> **ARFM != demonstrated autonomous DRAM policy selection**.

The hidden internal management remains opaque.

### E — changing a threshold regime has a state-conversion boundary

Because the standard requires RAA to reach zero before level change, the protocol avoids carrying a nonzero accumulated count directly across two threshold regimes. The bounded engineering interpretation is that policy migration has an explicit normalization boundary.

This does not prove that zero RAA means “no physical risk,” nor that all internal DRAM history has been erased. It proves only that the externally/accounted RAA state is normalized as required before the policy field changes.

> **RAA = 0 for level transition != proof of zero physical disturbance history**.

## Cross-case boundary

### Case 54 — DDR5 RFM split authority

Case 54 already owns the broad pattern in which DRAM exposes refresh-management requirements/thresholds while the controller retains activity accounting and schedules RFM opportunity. HBM3 ARFM refines that split: the device supplies multiple read-only threshold/decrement profiles and the controller selects one of the allowed levels.

This is a functional comparison, not an identity claim about DDR5 and HBM3 command geometry, parameter encoding, controller policy, or genealogy.

### Case 112 ordinary RFM relation

The existing Case-112 result remains intact:

```text
periodic REF obligation
    !=
activity-triggered RFM obligation
```

ARFM changes the selected RFM threshold/decrement policy; it does not turn RFM into periodic refresh or advance ordinary internal refresh counters.

## Anti-anachronism / priority boundary

The strongest dated claim here is only:

> **the public January-2022 JESD238 HBM3 standard already specifies ARFM.**

This does not establish:

- first invention or first proposal of ARFM;
- pre-publication JEDEC committee chronology;
- patent priority;
- first shipping HBM3 implementation;
- which GPUs/accelerators/controllers selected which level;
- any vendor's hidden row-selection or repair algorithm;
- a direct causal path from RowHammer research to this interface.

A fresh search of `tmzncty/computing-archaeology` found no dedicated `Adaptive Refresh Management` topic to reuse. Broader standards genealogy and controller/product adoption history remain better suited there.

## Claim ledger

| Claim | Type | Strength |
| --- | --- | --- |
| January-2022 JESD238 already contains §6.3.2.8 ARFM | H/P | strong for inspected standard mirror |
| ARFM support bit is distinct from default RFM-required bit | H/P | strong |
| vendor supplies read-only default/A/B/C threshold-decrement profiles | H/P | strong |
| controller selects an RFM level via MR8 OP[5:4] | H/P | strong |
| Levels A/B/C require RFM; higher level increases RFM need | H/P | strong |
| RAA must be reduced to zero before changing ARFM level | H/P | strong |
| one selected level applies across all channels of the HBM3 DRAM | H/P | strong |
| ARFM-capable `RFM=0` device can enable RFM at a non-default level | H/P | strong |
| policy-level selection and per-bank RAA are distinct retained states | E | strong |
| `adaptive` proves autonomous DRAM selection of A/B/C | X | rejected |
| RAA=0 proves no physical disturbance history remains | X | rejected |
| January 2022 establishes ARFM invention priority | X | rejected |

## Open evidence

Pre-2022 committee drafts/patents; commercial-controller level-selection policy; named HBM3 device parameter values; command traces showing level transitions; performance/energy impact; missed-RFM fault injection; later HBM revisions beyond the inspected 2022–2023 contract.

## Status

**`grounded`** as a bounded Case-112 correction/deepening for ARFM chronology, capability-vs-policy state, vendor/controller split authority, and maintenance-state normalization before policy transition.
EOF

python3 - <<'PY'
from pathlib import Path

# --- Case 112 ---
case_path = Path('cases/112-hbm3-rfm-bonus-maintenance-vs-periodic-refresh.md')
text = case_path.read_text()
if '112-jedec-hbm3-2022-2023-arfm-deepening.md' in text:
    raise SystemExit('Case112 ARFM deepening already integrated')

text = text.replace(
    "**`grounded`** — bounded to the public HBM3 `JESD238` / `JESD238A` Refresh Management (`RFM`) contract, especially the separation between periodic `REF` coverage and activity-triggered `RFM`, and the HBM3-specific difference between rolling `REFpb` coverage and targeted `RFMpb`.",
    "**`grounded`** — bounded to the public HBM3 `JESD238` / `JESD238A` Refresh Management (`RFM`) contract, especially the separation between periodic `REF` coverage and activity-triggered `RFM`, the HBM3-specific difference between rolling `REFpb` coverage and targeted `RFMpb`, and the optional Adaptive Refresh Management (`ARFM`) policy-level contract already present in the January-2022 standard."
)
text = text.replace(
    "Grounding record: [`../evidence/112-jedec-hbm3-2022-2023-rfm-grounding.md`](../evidence/112-jedec-hbm3-2022-2023-rfm-grounding.md).",
    "Grounding record: [`../evidence/112-jedec-hbm3-2022-2023-rfm-grounding.md`](../evidence/112-jedec-hbm3-2022-2023-rfm-grounding.md).\n\nARFM chronology/policy deepening: [`../evidence/112-jedec-hbm3-2022-2023-arfm-deepening.md`](../evidence/112-jedec-hbm3-2022-2023-arfm-deepening.md)."
)
anchor = "\n## Cross-case comparison\n"
insert = r'''

## 8. Adaptive RFM adds policy-level state above per-bank RAA

The original Case-112 pass left `ARFM/later HBM evolution` in open work. Direct reinspection of the same January-2022 JESD238 source shows that this wording was too loose: **Adaptive Refresh Management is already specified in HBM3 §6.3.2.8.** The correction is chronological and semantic; it is not a new invention-priority claim.

### H/P — capability, default requirement, and selected level are distinct

HBM3 exposes separate `ARFM` and `RFM` bits in the IEEE1500 `DEVICE_ID` WDR. `ARFM` says whether adaptive-level selection is supported; the default `RFM` bit says whether refresh management is required at the default level. The same device record supplies read-only default and A/B/C `RAAIMT`, `RAAMMT`, and `RAADEC` profiles, while `MR8 OP[5:4]` selects the active RFM level.

Therefore:

```text
ARFM capability
    != default RFM requirement
    != selected RFM level
    != per-bank RAA value
```

The device publishes an allowed policy menu; the controller selects among those vendor-defined profiles. This is a more precise split-authority relation than treating “the threshold” as one immutable constant.

### H/P — a level transition must retire outstanding accounted pressure first

JESD238 requires the host to decrement RAA to **0** using RFM or pending REF commands before changing the ARFM level, and requires the same RFM level on all channels of the HBM3 DRAM.

Engineering reconstruction:

```text
old policy level
    + outstanding bank-local RAA pressure
    -> maintenance / REF until accounted RAA = 0
    -> level transition
    -> new vendor-defined threshold/decrement profile
```

So:

> **policy change != arbitrary reinterpretation of an outstanding RAA balance under new thresholds**.

The standard gives a transition rule for the accounted state. It does **not** say that RAA=0 erases physical disturbance history or reveals the hidden mitigation state.

### H/P — default “RFM not required” is not an immutable lifetime property

ARFM can also make RFM operative on an ARFM-capable HBM3 DRAM whose default `RFM` bit says `RFM not required`: selecting a non-default level makes the device treat RFM commands as RFM rather than RNOP.

Thus:

> **default RFM requirement != immutable lifetime RFM requirement**.

Conversely, a device without ARFM support cannot treat the non-default level field as a generic tuning knob; those combinations are illegal/RFU.

### E — “adaptive” does not prove autonomous DRAM policy selection

The public contract gives the **controller** flexibility to choose Levels A/B/C. The inspected standard does not demonstrate that the DRAM autonomously chooses a level from workload, temperature, or observed faults.

> **ARFM != demonstrated autonomous self-tuning of the selected level**.

This distinction matters because Case 112 already separates public controller-side RAA bookkeeping from opaque in-DRAM management. ARFM adds a policy-selection layer; it does not disclose the hidden victim-selection algorithm.

Full source mapping and limits are recorded in [`../evidence/112-jedec-hbm3-2022-2023-arfm-deepening.md`](../evidence/112-jedec-hbm3-2022-2023-arfm-deepening.md).
'''
if anchor not in text:
    raise SystemExit('Case112 cross-case anchor missing')
text = text.replace(anchor, insert + anchor, 1)
text = text.replace(
    "Pre-2022 committee/patent genealogy; named HBM3 stack and controller behavior; independent HBM3 command traces; hidden victim selection; ARFM and later HBM evolution; threshold/fault injection; performance/energy validation.",
    "Pre-2022 committee/patent genealogy; named HBM3 stack and controller behavior; independent HBM3 command traces; hidden victim selection; commercial ARFM level-selection policy and later HBM evolution beyond the inspected 2022–2023 contract; threshold/fault injection; performance/energy validation."
)
case_path.write_text(text)

# --- Existing Evidence 112 navigation / debt correction ---
ev_path = Path('evidence/112-jedec-hbm3-2022-2023-rfm-grounding.md')
ev = ev_path.read_text()
if 'ARFM chronology/policy deepening' not in ev:
    marker = "It does not reconstruct hidden in-DRAM mitigation, establish commercial-controller behavior, or claim invention priority.\n"
    if marker not in ev:
        raise SystemExit('Evidence112 scope marker missing')
    ev = ev.replace(marker, marker + "\nARFM chronology/policy deepening: [`112-jedec-hbm3-2022-2023-arfm-deepening.md`](112-jedec-hbm3-2022-2023-arfm-deepening.md). Direct reinspection shows that ARFM is already part of JESD238 (January 2022), so it is no longer left as a generic later-HBM evidence item.\n", 1)
ev = ev.replace(
    "Pre-2022 committee drafts/patents; named HBM3 RFM parameter values; controller bookkeeping/scheduling; independent command traces; hidden internal mitigation; ARFM/later HBM revisions; threshold and missed-RFM fault injection.",
    "Pre-2022 committee drafts/patents; named HBM3 RFM parameter values; controller bookkeeping/scheduling; independent command traces; hidden internal mitigation; commercial ARFM policy and later HBM revisions beyond the inspected 2022–2023 contract; threshold and missed-RFM fault injection."
)
ev_path.write_text(ev)

# --- CASE_INDEX findings ---
idx_path = Path('CASE_INDEX.md')
idx = idx_path.read_text()
if '3378. **Historical correction:** January-2022 JESD238 already contains Adaptive Refresh Management' in idx:
    raise SystemExit('CASE_INDEX ARFM findings already integrated')
idx_anchor = "\n## Comparison matrix — provisional\n"
findings = r'''

3378. **Historical correction:** January-2022 JESD238 already contains Adaptive Refresh Management (`ARFM`) in §6.3.2.8; Case 112 no longer leaves ARFM ambiguously as a later-HBM-only item.
3379. **Historical record:** HBM3 exposes separate read-only `ARFM` capability and default `RFM`-required bits in the IEEE1500 `DEVICE_ID` WDR; support for adaptive level selection and the default requirement for RFM are different properties.
3380. **Historical record:** An ARFM-capable device exposes vendor-set default plus Level A/B/C `RAAIMT`, `RAAMMT`, and `RAADEC` parameter profiles, while the controller selects the active level through `MR8 OP[5:4]`.
3381. **Historical record:** JESD238 states that Levels A/B/C require RFM and that increasing the RFM level increases the need for RFM commands, with Level C the highest level.
3382. **Historical record:** Before changing ARFM level, the host must decrement the Rolling Accumulated ACT count to zero with RFM or pending REF commands.
3383. **Historical record:** JESD238 requires the same selected RFM level on all channels of one HBM3 DRAM even though RAA accounting remains per bank.
3384. **Historical record:** An ARFM-capable HBM3 DRAM whose default `RFM` bit is 0 can make RFM operative by programming a non-default adaptive level; default `RFM not required` is therefore not an immutable lifetime requirement state.
3385. **Historical record:** HBM3 devices without ARFM support treat non-default ARFM level selections as unsupported/illegal rather than exposing a universal controller tuning knob.
3386. **Engineering reconstruction:** `ARFM capability != default RFM requirement != selected RFM level != per-bank RAA`; these are distinct pieces of retained/control state that compose in the maintenance protocol.
3387. **Engineering reconstruction:** Vendor-published read-only threshold/decrement profiles plus controller level selection constitute split authority; the controller chooses among allowed profiles rather than supplying arbitrary hidden-DRAM thresholds.
3388. **Engineering reconstruction:** Requiring RAA=0 before a level transition creates an explicit maintenance-state normalization boundary: policy change does not arbitrarily reinterpret a nonzero accounted activation balance under a new threshold regime.
3389. **Engineering boundary:** `RAA = 0` for an ARFM transition does not prove that physical disturbance history is absent or that hidden victim-selection state has been erased.
3390. **Engineering boundary / terminology:** `Adaptive Refresh Management` in the public HBM3 interface does not demonstrate autonomous DRAM choice of Level A/B/C; the inspected contract gives the controller the level-selection action.
3391. **Functional analogy / security boundary:** Case 54 DDR5 RFM and Case 112 HBM3 ARFM both expose device/controller split maintenance authority, but command geometry, encodings, policies, and genealogy remain distinct; selecting or completing RFM likewise does not establish sanitization of stored payload.
'''
if idx_anchor not in idx:
    raise SystemExit('CASE_INDEX comparison anchor missing')
idx = idx.replace(idx_anchor, findings + idx_anchor, 1)
idx_path.write_text(idx)

# --- ROADMAP ---
road_path = Path('ROADMAP.md')
road = road_path.read_text()
road_item = "- [x] **Case 112 HBM3 ARFM chronology/policy deepening (JESD238 / JESD238A):** direct reinspection of the same 2022–2023 JEDEC standard text closes an evidence-debt error in the earlier pass: Adaptive Refresh Management is already present in January-2022 HBM3. The deepening separates ARFM capability, default RFM requirement, controller-selected RFM level, vendor-set threshold/decrement profiles, and per-bank RAA; records the required RAA-to-zero transition before level changes and the all-channel level-consistency rule; and shows that an ARFM-capable device with default `RFM=0` can make RFM operative at a non-default level. It keeps ARFM policy selection distinct from autonomous DRAM self-tuning, hidden victim selection, corruption thresholds, invention priority, and sanitization; broader genealogy/product adoption remains for `computing-archaeology`."
if road_item not in road:
    road_anchor = "## Phase 2 — Build missing technical bridges\n\n"
    if road_anchor not in road:
        raise SystemExit('ROADMAP Phase2 anchor missing')
    road = road.replace(road_anchor, road_anchor + road_item + "\n\n", 1)
road_path.write_text(road)
PY

# Remove temporary integration machinery in the research commit.
git rm -f .github/workflows/integrate-case112-arfm.yml scripts/integrate-case112-arfm.sh

git add CASE_INDEX.md ROADMAP.md \
  cases/112-hbm3-rfm-bonus-maintenance-vs-periodic-refresh.md \
  evidence/112-jedec-hbm3-2022-2023-rfm-grounding.md \
  "$EVIDENCE"

git commit -m "case112: deepen HBM3 adaptive RFM policy"
git push origin main
