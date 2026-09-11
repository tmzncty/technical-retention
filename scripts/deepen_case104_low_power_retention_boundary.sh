#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
git pull --ff-only origin main

python3 - <<'PY'
from pathlib import Path

case = Path('cases/104-micron-lpddr-selective-adaptive-self-refresh.md')
evidence = Path('evidence/104-micron-2014-lpddr-low-power-retention-boundary-deepening.md')
index = Path('CASE_INDEX.md')
roadmap = Path('ROADMAP.md')
workflow = Path('.github/workflows/deepen-case104-low-power-retention.yml')
script = Path('scripts/deepen_case104_low_power_retention_boundary.sh')

for p in [case, index, roadmap, Path('README.md'), Path('AGENTS.md'), Path('docs/METHOD.md'), Path('docs/PRIOR_ART.md'), Path('docs/TECHNICAL_SPINE.md')]:
    if not p.exists():
        raise SystemExit(f'missing prerequisite: {p}')
if evidence.exists():
    raise SystemExit(f'refusing to overwrite existing evidence file: {evidence}')

evidence_text = r'''# Case 104 Deepening — Micron Mobile LPDDR Low-Power Retention Boundaries (2014)

## Purpose

This record deepens [`../cases/104-micron-lpddr-selective-adaptive-self-refresh.md`](../cases/104-micron-lpddr-selective-adaptive-self-refresh.md) around one bounded question:

> when one named LPDDR device offers ordinary Power-Down, SELF REFRESH, and Deep Power-Down, which of those low-power states actually retains payload, by what maintenance relation, and what happens on exit?

The answer is deliberately narrower than a history of LPDDR power management. A Micron 512Mb Mobile LPDDR datasheet, Rev. I (January 2014), exposes three different contracts inside one product family:

```text
ordinary Power-Down
    refresh temporarily stops
    -> retention remains deadline-bounded

SELF REFRESH
    device performs refresh internally
    -> payload is retained while powered and within specified conditions

Deep Power-Down
    array power / refresh support is withdrawn
    -> payload retention is not promised
    -> full DRAM initialization is required on exit
```

The document is a manufacturer-origin technical publication preserved on a Texas Instruments support site rather than a current Micron origin host, so historical claims from this copy are tagged `H/P*` under repository policy.

## Primary source inspected

Micron Technology, Inc., _512Mb: x16, x32 Mobile LPDDR SDRAM_, document `t67m_512mb_mobile_lpddr.pdf`, Rev. I, January 2014, especially printed pp. 90–94 (PDF pp. 89–93), preserved by Texas Instruments:

<https://e2e.ti.com/cfs-file/__key/telligent-evolution-components-attachments/00-791-00-00-00-38-27-14/T67M_5F00_512Mb_5F00_mobile_5F00_lpddr_5F00_sdram.pdf>

The same 2009–2014 Micron family is already the bounded object of Case 104. This record does not introduce a new product lineage or priority claim; it tightens one power-state seam in the existing case.

## Historical record — ordinary Power-Down is retentive only inside the refresh deadline

The datasheet says that entering Power-Down disables input/output buffers other than CKE. It then states that Power-Down duration is **limited by the refresh requirements of the device**. The timing figure reinforces the point with `Must not exceed refresh device limits`, and exit requires the normal `tXP` delay before another valid command.

The bounded historical result is therefore:

```text
Power-Down
    !=
power removed from the DRAM array

Power-Down
    !=
self-refresh maintenance
```

Ordinary Power-Down is a lower-activity interval during which the existing charge state may survive, but the device is not performing the recurring refresh work needed for an arbitrarily long stay in that state. The allowed interval is bounded by the same retention deadline that makes refresh necessary.

This blocks the shorthand `power-down = powered off`.

## Historical record — SELF REFRESH retains payload by continuing internal maintenance

The same datasheet says SELF REFRESH can retain data while the rest of the system is powered down and that external clocking is not needed. The device nevertheless continues refresh internally. Refresh intervals are scheduled inside the device and may vary; temperature sensing and PASR/TCSR policy discussed in the main Case 104 determine cadence and scope.

Thus the low external activity is not passive retention:

```text
external clock absent
    !=
refresh absent
```

SELF REFRESH is a maintenance-bearing state. The payload survives because the device continues the constitutive work that dynamic charge requires.

## Historical record — Deep Power-Down intentionally crosses the retention boundary

Micron describes Deep Power-Down (DPD) as the maximum-power-reduction mode obtained by eliminating power to the memory array. The datasheet states that data **will not be retained** after entering DPD.

The exit contract is equally important. After CKE is raised to leave DPD, Micron requires a **full DRAM initialization sequence** before normal operation resumes. The timing figure repeats that requirement.

This produces a stronger distinction than merely saying “DPD uses less power”:

```text
exit ordinary Power-Down
    -> wait tXP, continue service with retained payload

exit SELF REFRESH
    -> wait tXSR / complete internal refresh, continue with retained payload

exit DPD
    -> full DRAM initialization required; prior payload is outside the retention contract
```

The required initialization is evidence that DPD exit is not a resume path for retained array contents.

## Engineering reconstruction — low-power depth is not one retention axis

The three modes are useful precisely because energy state and retention state do not collapse into one scalar ordering.

A bounded engineering reconstruction is:

| Mode | Refresh work while resident | Payload contract | Exit relation |
| --- | --- | --- | --- |
| ordinary Power-Down | no recurring refresh in the mode | retained only within refresh timing limits | `tXP`, then ordinary command service |
| SELF REFRESH | internal device refresh continues | retained under the documented powered/operating conditions and selected PASR scope | `tXSR`, then ordinary service |
| Deep Power-Down | retention support withdrawn | data not retained | full DRAM initialization |

The table is a present engineering comparison of manufacturer-defined states, not historical vocabulary supplied by Micron.

Therefore:

> **lower power != stronger retention**

and

> **low-power state != one retention class**.

## Engineering reconstruction — retention can fail by deadline expiry or by policy withdrawal

The same part exposes two different paths out of the retention guarantee:

1. remain too long in ordinary Power-Down without performing the refresh work required by the device; or
2. enter DPD, which intentionally withdraws array-power / refresh support and declares data non-retained.

Those paths should not be flattened into the same event. One is a **deadline-bounded maintenance omission**; the other is a **mode transition that explicitly retires the retention contract**.

This complements Case 104's PASR result. PASR can withdraw maintenance from selected regions while keeping others alive; DPD withdraws the whole-array retention promise.

## Engineering reconstruction — reinitialization is not restoration

The DPD exit sequence requires the DRAM to be initialized again. That requirement restores the device to an operationally admissible state; it does not reconstruct the pre-DPD payload.

Therefore:

```text
service reinitialization
    !=
payload restoration
```

The distinction matters because “the device is usable again” and “the previous data remain current” are different relations.

## Negative evidence / security boundary

The datasheet gives a host-visible retention contract, not a sanitization proof.

It establishes that prior payload is **not promised to remain valid after DPD**. It does not establish:

- the exact time at which every capacitor's residual charge becomes physically unrecoverable;
- whether specialized laboratory techniques can recover any remanent information over some interval;
- a media-sanitization assurance level;
- a verified erase pass;
- cryptographic erasure;
- an overwrite or readback-verification procedure.

Accordingly:

> **`data not retained` != `verified sanitization`**.

DPD is a power-management / retention boundary, not evidence of a security-erasure mechanism.

## Functional comparison — magnetic core and dynamic RAM cross the power boundary differently

Case 02 now has named IBM/DEC evidence that magnetic-core payload can remain during an unpowered interval even though power transitions still need protection and surrounding control state may be reset. This LPDDR witness exposes the opposite bounded relation: dynamic payload in SELF REFRESH still depends on powered internal maintenance, while DPD intentionally removes the condition under which payload survival is promised.

The comparison is functional only:

```text
magnetic core: quiescent payload may remain without sustaining power
LPDDR self refresh: payload remains through powered periodic reconstruction
LPDDR DPD: deepest power-saving mode abandons payload retention
```

No common mechanism, invention genealogy, or historical vocabulary is inferred.

## Philosophical interpretation — retention is a mode contract, not a synonym for “still powered a little”

A bounded project-level interpretation is that apparent persistence depends on which relations a mode continues to support. The three modes use different combinations of power, maintenance, timing, and re-entry procedure; none can be understood from the word “low-power” alone.

This is a philosophical interpretation of the engineering contrast, not wording attributed to Micron or JEDEC.

## Prior-art and anti-anachronism boundaries

This deepening does **not** claim:

- that Micron invented Power-Down, SELF REFRESH, DPD, or LPDDR low-power modes;
- that Rev. I January 2014 is the first public appearance of these functions;
- a JEDEC ballot chronology or direct genealogy between earlier SDRAM and this implementation;
- that Power-Down internally refreshes the array;
- that SELF REFRESH means the array is unpowered;
- that DPD is secure erase or sanitization;
- that the datasheet reveals exact cell-level remanence after DPD;
- that all LPDDR generations use identical entry, exit, or retention semantics.

A broader standards / low-power-memory genealogy belongs primarily in `tmzncty/computing-archaeology`. A repository search found no dedicated Deep Power-Down history there at the time of this deepening, so this record keeps only the bounded product semantics needed by `technical-retention`.

## Resulting bounded distinctions

```text
Power-Down != powered off
Power-Down != SELF REFRESH
SELF REFRESH != no maintenance
SELF REFRESH != passive nonvolatility
DPD != PASR
DPD exit != retained-state resume
full DRAM initialization != payload restoration
data not retained != verified sanitization
low-power state != one retention class
```

## Open work deliberately left outside this slice

- JEDEC normative introduction and revision history of LPDDR DPD / self-refresh modes;
- earlier vendor products implementing DPD;
- cross-vendor differences in entry/exit timing and supply behavior;
- hardware measurement of payload decay or remanence after DPD;
- controller policy deciding among ordinary Power-Down, SELF REFRESH, and DPD;
- broader mobile-memory power-management genealogy.
'''
evidence.write_text(evidence_text, encoding='utf-8')

s = case.read_text(encoding='utf-8')
link = 'Low-power-state retention-boundary deepening: [`../evidence/104-micron-2014-lpddr-low-power-retention-boundary-deepening.md`](../evidence/104-micron-2014-lpddr-low-power-retention-boundary-deepening.md). This product-level slice separates ordinary Power-Down, SELF REFRESH, and DPD without turning DPD content loss into a sanitization claim.'
if '104-micron-2014-lpddr-low-power-retention-boundary-deepening.md' not in s:
    anchor = 'Grounding record: [`../evidence/104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md`](../evidence/104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md).'
    if anchor not in s:
        raise SystemExit('Case104 grounding-record anchor missing')
    s = s.replace(anchor, anchor + '\n\n' + link, 1)

heading = '### H/P* — Power-Down, SELF REFRESH, and DPD expose different retention contracts'
if heading not in s:
    anchor = '## Retained state and control state'
    if anchor not in s:
        raise SystemExit('Case104 retained-state anchor missing')
    section = r'''### H/P* — Power-Down, SELF REFRESH, and DPD expose different retention contracts

A second January-2014 Micron Mobile LPDDR datasheet tightens the low-power boundary. Ordinary **Power-Down** disables most interface activity, but the manufacturer explicitly limits its duration by the device refresh requirement; it is therefore not an indefinite retention mode and it is not equivalent to removing power. **SELF REFRESH** instead keeps the dynamic payload current by scheduling refresh internally without an external clock. **Deep Power-Down** crosses a different boundary: Micron says memory-array power is eliminated, prior data are not retained, and exit requires a full DRAM initialization sequence.

The bounded state relation is therefore:

```text
ordinary Power-Down
    -> no refresh while resident; duration bounded by refresh deadline

SELF REFRESH
    -> internal refresh continues; selected payload remains under the documented conditions

Deep Power-Down
    -> retention support withdrawn; data not retained; full reinitialization on exit
```

This supports `Power-Down != powered off`, `SELF REFRESH != passive nonvolatility`, and `DPD exit != retained-state resume`. The source is a vendor-origin Micron datasheet preserved on a Texas Instruments site, so these claims are recorded as `H/P*` rather than current-origin `H/P`.

The content-loss statement is still not a sanitization guarantee. The datasheet does not establish the cell-level remanence horizon, laboratory recoverability, or verified physical erasure after DPD.

'''
    s = s.replace(anchor, section + anchor, 1)

claim_anchor = '| DPD eliminates array power and does not retain payload | H/P | Micron command/general-description text |'
if claim_anchor in s and 'ordinary Power-Down duration is bounded by refresh requirements' not in s:
    extra = '''\n| ordinary Power-Down duration is bounded by refresh requirements rather than providing indefinite retention | H/P* | Micron Mobile LPDDR Rev. I 01/14 pp. 90–93 |\n| SELF REFRESH retains payload through internally scheduled refresh without external clocking | H/P* | Micron Mobile LPDDR Rev. I 01/14 pp. 89–90 |\n| exit from DPD requires a full DRAM initialization sequence | H/P* | Micron Mobile LPDDR Rev. I 01/14 pp. 93–94 |\n| DPD content loss is equivalent to verified sanitization | X | not established; no remanence / recovery / erase-assurance evidence |'''
    s = s.replace(claim_anchor, claim_anchor + extra, 1)

source_anchor = '3. Takayasu Sakurai and Tetsuya Iizuka, Toshiba Corp., US4682306A, _Self-refresh control circuit for dynamic semiconductor memory device_, Japanese priority 20 August 1984, US publication 21 July 1987: <https://patents.google.com/patent/US4682306A/en>.'
if source_anchor in s and 'T67M_5F00_512Mb_5F00_mobile' not in s:
    s = s.replace(source_anchor, source_anchor + '\n4. Micron Technology, Inc., _512Mb: x16, x32 Mobile LPDDR SDRAM_, `t67m_512mb_mobile_lpddr.pdf`, Rev. I, January 2014, especially pp. 90–94; vendor-origin datasheet preserved via Texas Instruments: <https://e2e.ti.com/cfs-file/__key/telligent-evolution-components-attachments/00-791-00-00-00-38-27-14/T67M_5F00_512Mb_5F00_mobile_5F00_lpddr_5F00_sdram.pdf>.', 1)
case.write_text(s, encoding='utf-8')

idx = index.read_text(encoding='utf-8')
old_evidence = '[2009–2014 Micron LPDDR TCSR/PASR grounding](evidence/104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md); full JEDEC/LPDDR feature genealogy'
new_evidence = '[2009–2014 Micron LPDDR TCSR/PASR grounding](evidence/104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md) + [2014 low-power-state retention-boundary deepening](evidence/104-micron-2014-lpddr-low-power-retention-boundary-deepening.md); full JEDEC/LPDDR feature genealogy'
if old_evidence not in idx:
    raise SystemExit('CASE_INDEX Case104 row anchor missing')
idx = idx.replace(old_evidence, new_evidence, 1)

finding_heading = '## Case 104 deepening — Micron LPDDR low-power-state retention-boundary findings'
if finding_heading in idx:
    raise SystemExit('CASE_INDEX deepening findings already present')
marker = '## Comparison matrix — provisional'
if marker not in idx:
    raise SystemExit('CASE_INDEX comparison-matrix anchor missing')
findings = r'''## Case 104 deepening — Micron LPDDR low-power-state retention-boundary findings

3338. **Power-Down != powered off.** Micron's January-2014 Mobile LPDDR contract keeps the device in a powered low-activity state and explicitly limits residence time by the refresh requirement; the name must not be read as array power removal. (`H/P*`, `E`)
3339. **ordinary Power-Down != SELF REFRESH.** In ordinary Power-Down, refresh does not continue indefinitely and the residence time is refresh-deadline-bounded; SELF REFRESH instead schedules recurring refresh internally. (`H/P*`)
3340. **no external clocking != no retention work.** Micron's SELF REFRESH retains data without external clocking precisely while device-local refresh continues. (`H/P*`, `E`)
3341. **SELF REFRESH != passive nonvolatility.** The payload remains conditional on powered internal reconstruction rather than a substrate that simply holds state with all retention power removed. (`E`)
3342. **Deep Power-Down != ordinary Power-Down.** DPD is the manufacturer's maximum-power-reduction mode, eliminates memory-array power, and carries no payload-retention promise. (`H/P*`)
3343. **DPD exit != retained-state resume.** Micron requires a full DRAM initialization sequence after DPD exit; re-establishing an operational device does not restore the pre-DPD payload. (`H/P*`, `E`)
3344. **full initialization != payload restoration.** Initialization re-establishes admissible device control/configuration state, while the prior array contents remain outside the DPD retention contract. (`E`)
3345. **low-power state != one retention class.** The same named product family exposes deadline-bounded Power-Down, maintenance-bearing SELF REFRESH, and retention-abandoning DPD; energy reduction and payload-retention semantics are separate comparison axes. (`E`)
3346. **deadline expiry != explicit retention-policy withdrawal.** Ordinary Power-Down can exceed a refresh deadline if held too long, whereas DPD explicitly enters a mode that withdraws the whole-array retention promise. (`E`)
3347. **`data not retained` != verified sanitization.** The datasheet does not establish exact capacitor discharge, forensic recoverability, overwrite, readback verification, or a security-erasure assurance level after DPD. (`X`, `E`)
3348. **magnetic-core power-off retention and LPDDR low-power retention are only functional counterpoints.** Case 02 supplies named-machine evidence for unpowered core payload survival plus transition hazards; Case 104 instead shows powered refresh-dependent survival and deliberate DPD retention withdrawal. No shared mechanism or genealogy follows. (`A`, `X`)
3349. **2014 named-product semantics != invention chronology.** This deepening fixes a product-level contract and does not claim that Micron invented Power-Down, SELF REFRESH, or DPD; broader standards and low-power-memory genealogy remain outside this repository slice. (`X`)

'''
idx = idx.replace(marker, findings + marker, 1)
index.write_text(idx, encoding='utf-8')

r = roadmap.read_text(encoding='utf-8')
roadmap_item = '- [x] Case 104 Mobile LPDDR low-power retention-boundary deepening — [`cases/104-micron-lpddr-selective-adaptive-self-refresh.md`](cases/104-micron-lpddr-selective-adaptive-self-refresh.md) + [`evidence/104-micron-2014-lpddr-low-power-retention-boundary-deepening.md`](evidence/104-micron-2014-lpddr-low-power-retention-boundary-deepening.md): Micron Rev. I January-2014 product documentation now separates ordinary Power-Down (no ongoing refresh; residence time bounded by refresh requirements), SELF REFRESH (internal maintenance continues without external clocking), and Deep Power-Down (array-power/retention withdrawal, data not retained, full DRAM initialization required on exit). This closes the bounded `Power-Down != powered off`, `SELF REFRESH != passive nonvolatility`, `DPD exit != retained-state resume`, and `data-not-retained != sanitization` seams. JEDEC introduction chronology, earlier vendor DPD implementations, controller selection policy, remanence experiments, and broader mobile-memory power-management history remain open and belong primarily in `computing-archaeology`.'
if roadmap_item not in r:
    anchor = '## Phase 2 — Build missing technical bridges\n\n'
    if anchor not in r:
        raise SystemExit('ROADMAP Phase2 anchor missing')
    r = r.replace(anchor, anchor + roadmap_item + '\n', 1)
roadmap.write_text(r, encoding='utf-8')
PY

# Keep the final research commit canonical: remove the temporary automation scaffolding.
git rm -f scripts/deepen_case104_low_power_retention_boundary.sh .github/workflows/deepen-case104-low-power-retention.yml

git add cases/104-micron-lpddr-selective-adaptive-self-refresh.md \
        evidence/104-micron-2014-lpddr-low-power-retention-boundary-deepening.md \
        CASE_INDEX.md ROADMAP.md

if git diff --cached --quiet; then
  echo 'No staged research changes; refusing empty integration commit.' >&2
  exit 1
fi

git commit -m 'case104: deepen LPDDR low-power retention boundary'
git push origin main
