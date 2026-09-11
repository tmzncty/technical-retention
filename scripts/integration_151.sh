#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

git fetch origin main
git pull --rebase origin main

case_path="cases/151-ddr5-same-bank-refresh-partitioned-maintenance.md"
evidence_path="evidence/151-ddr5-2014-2020-bank-scoped-refresh-grounding.md"

if [[ -e "$case_path" || -e "$evidence_path" ]]; then
  echo "Case 151 canonical files already exist; refusing to duplicate." >&2
  exit 1
fi

python3 - <<'PY'
from pathlib import Path

index = Path('CASE_INDEX.md').read_text(encoding='utf-8')
if '3253' not in index:
    raise SystemExit('Expected Case 150 finding 3253 is absent; CASE_INDEX baseline changed.')
if '3254.' in index or 'Case 151 — DDR5 Same Bank Refresh' in index:
    raise SystemExit('Finding 3254 or Case 151 already exists; refusing to collide.')
PY

cat > "$case_path" <<'EOF'
# Case 151 — DDR5 Same Bank Refresh: Partitioned Refresh Scope, Concurrent Service, and Retention Scheduling

Status: grounded

## 0. Research Status Snapshot

- **Historical record:** grounded at a conservative public boundary. JEDEC announced publication of JESD79-5 DDR5 on 2020-07-14; current Micron DDR5 documentation describes SAME BANK REFRESH (`REFsb`). A Micron-origin 2014 LPDDR2 product manual preserved on a third-party mirror provides an earlier, product-specific per-bank-refresh prior-art floor.
- **Engineering reconstruction:** grounded only at the public command/interface level. `REFsb` partitions a refresh episode to the same bank number across bank groups while non-targeted banks remain eligible for other commands subject to DDR5 timing rules. No hidden controller scheduler, cell circuit, or product firmware is inferred.
- **Functional analogy:** bounded. Cases 03, 09, and 10 study other dimensions of DRAM refresh; LPDDR2 `REFpb` provides earlier bank-scoped refresh chronology. Similarity does not establish an identical state machine or direct genealogy.
- **Philosophical interpretation:** interpretation only. A persistence obligation may be spatially scoped: some state can be under compulsory maintenance while other state remains available for foreground use.

## 1. Problem Statement

DRAM refresh is compulsory restorative maintenance, but the existence of a refresh obligation does not by itself determine how much of a memory device must become unavailable during each maintenance episode.

DDR5 `REFsb` is a useful retention case because it makes that distinction explicit. Micron describes the command as refreshing a bank in each bank group while keeping the other banks available for access. The preservation obligation therefore remains device-wide over time, but a particular refresh operation can have a narrower spatial scope.

The bounded question is:

> What must remain true for DDR5 data retention when the maintenance that restores charge is partitioned across banks rather than expressed only as whole-array blocking work?

## 2. Boundary and Stop Conditions

### In scope

- the public DDR5 `REFsb` command relation;
- bank-group/bank maintenance scope and foreground-access consequences;
- a conservative 2020 public DDR5-standard boundary;
- Micron LPDDR2 `REFpb` as an earlier bank-scoped-refresh prior-art floor;
- comparison with Cases 03, 09, 10, and 150;
- retention-specific interpretation of spatially partitioned maintenance.

### Out of scope

- exact JEDEC timing tables not reproduced in the public sources used here;
- hidden memory-controller scheduling algorithms;
- DRAM cell-circuit implementation of refresh;
- RowHammer/TRR policy;
- per-row individualized retention profiling;
- claims that DDR5 invented bank-scoped refresh;
- claims of direct LPDDR2-to-DDR5 genealogy;
- ECC scrub, data-integrity proof, or media sanitization.

## 3. Evidence Matrix

| ID | Evidence | Type | Supports | Does not support |
|---|---|---|---|---|
| E151.1 | JEDEC publication announcement mirrored by Design-Reuse, 2020-07-14 | institutional historical record, mirrored | public publication boundary for JESD79-5 DDR5 | invention date; exact normative `REFsb` wording |
| E151.2 | Micron DDR5 SDRAM product documentation | first-party technical | DDR5 exposes all-bank and same-bank refresh; `REFsb` refreshes a bank in each bank group | controller microarchitecture; implementation genealogy |
| E151.3 | Micron DDR5 feature explanation | first-party technical | targeted banks must be idle; untargeted banks can remain available subject to timing restrictions | universal performance gain; no stalls of any kind |
| E151.4 | Micron-origin 2014 LPDDR2 manual mirrored by Doczz | historical vendor manual mirror (`H/P*`) | `REFpb` existed on a named LPDDR2 product family; target bank inaccessible while other banks can be read/written | origin-hosted archival provenance; DDR5 equivalence or lineage |
| E151.5 | Micron current legacy-part catalog for EDB4432BBPA | first-party product identity | the mirrored manual corresponds to a real Micron/Elpida LPDDR2 part family | the detailed refresh text by itself |

## 4. Historical Record

### 4.1 DDR5 public boundary: 2020, not an invention claim

JEDEC's publication announcement for JESD79-5 is dated **2020-07-14**. This is used only as a conservative public standard boundary. It is not treated as the date on which bank-scoped refresh was invented, nor as proof that every DDR5 implementation immediately shipped with the same controller policy.

Micron's current DDR5 product material contrasts earlier DDR refresh support with DDR5's addition of `REFsb`: the command refreshes a bank in each bank group rather than requiring an all-bank refresh episode.

### 4.2 What `REFsb` changes

Micron's DDR5 feature explanation is more precise than the label “same bank” alone. The command targets **the same bank number across bank groups**. On the cited 16Gb x4/x8 organization, only one bank in each bank group needs to be idle for the command; the remaining banks need not all be idle and remain available subject to the specified timing restrictions.

Therefore:

- `same-bank wording != exactly one physical bank total`;
- `some bank scope under refresh != all banks unavailable`;
- `foreground service continuity != absence of retention maintenance`.

The data in the targeted banks still depends on periodic restorative work. What changes is the service-blocking scope of a particular maintenance episode.

### 4.3 Earlier bank-scoped prior art: LPDDR2 in 2014

A Micron-origin LPDDR2 product manual, Rev. A 07/14, preserved by a third-party documentation mirror, describes a per-bank refresh command (`REFpb`). It states that the target bank is inaccessible during its per-bank refresh cycle while other banks remain accessible and may receive reads or writes. Micron's current legacy catalog independently identifies the `EDB4432BBPA` family as LPDDR2.

This establishes a bounded prior-art floor: **bank-scoped DRAM refresh was publicly documented on a named Micron/Elpida LPDDR2 product family by 2014**, before JESD79-5 DDR5 was published in 2020.

It does **not** establish that LPDDR2 `REFpb` and DDR5 `REFsb` are the same state machine. In the LPDDR2 document, a device-internal bank counter schedules the target bank in a round-robin sequence; Micron's DDR5 description instead says `REFsb` targets the same bank number across bank groups. Earlier chronology therefore blocks a novelty overclaim but does not prove direct genealogy.

## 5. Engineering Reconstruction

At the public-interface level, a bounded reconstruction is:

1. DRAM cells remain subject to a periodic refresh obligation.
2. The controller reaches a point at which a bank-scoped refresh episode is due and legal under the command/timing contract.
3. A DDR5 `REFsb` command selects a bank number across the bank groups.
4. The targeted banks are unavailable for the refresh interval.
5. Non-targeted banks remain eligible for foreground commands, subject to the command/timing restrictions that still apply.
6. After the refresh interval, the targeted banks return to ordinary access eligibility.
7. Repeating such scoped episodes over time satisfies the broader retention schedule.

This is an **interface-level reconstruction**, not a claim about silicon micro-operations or a particular memory-controller scheduler.

The relevant retained state categories are also distinct:

- **payload state:** charge patterns representing user/system data in DRAM cells;
- **maintenance obligation:** the requirement that restorative refresh continue within timing limits;
- **maintenance scope/control state:** which bank set a given refresh episode targets and which commands are legal while it is in progress.

The refresh-control relation is not another payload replica and not a full history of prior refresh events.

## 6. What This Case Does Not Mean

### 6.1 Bank-scoped refresh is not individualized retention profiling

`REFsb` exposes a spatial command granularity. It does not, from the evidence used here, say that each row has its own measured leakage rate or individualized retention deadline. Case 10 addresses adaptive cadence/leakage ideas; Case 151 addresses spatial maintenance scope.

### 6.2 Interface capability is not deployed scheduling policy

The existence of `REFsb` does not prove how often a real CPU memory controller uses it, how it trades it against all-bank refresh, or how workloads affect its policy. Those claims require controller-specific documentation or traces.

### 6.3 Refresh is not ECC scrub or sanitization

Refresh restores volatile charge so valid data remains readable. It is not, by itself, an error-correction scrub that proves integrity, and it is not a deletion/sanitization procedure intended to make prior data irrecoverable.

## 7. Cross-Case Comparison

| Case | Maintenance / retained relation | Main variable | Key distinction from Case 151 |
|---|---|---|---|
| Case 03 — DRAM scheduled restoration | periodic charge restoration | cadence | Case 151 asks how one mandatory refresh episode is spatially partitioned |
| Case 09 — CBR refresh address internalization | device-managed refresh sequencing | address/control ownership | internalizing refresh address generation is different from limiting service-blocking scope |
| Case 10 — leakage-tracked self-refresh | adaptive maintenance cadence | time / sensed retention need | Case 151 does not infer per-row leakage profiling |
| Case 150 — managed-SSD garbage collection | background relocation + erase | reclamation scope/opportunity | only a functional analogy: foreground service can coexist with maintenance; medium, mechanism, and persistence problem differ |

## 8. Related Repository Boundary

`tmzncty/computing-archaeology` was searched for a dedicated `per-bank refresh` / `REFsb` topic before this case was opened; no dedicated treatment was found.

The broad historical genealogy of LPDDR/DDR refresh commands, memory-controller policy evolution, DRAM-bank organizations, and platform adoption belongs primarily in `computing-archaeology`. This case keeps only the bounded retention relation: **mandatory restorative maintenance can be spatially partitioned without turning the rest of the memory device into “not under retention.”**

## 9. Philosophical Interpretation

**Interpretation only:** persistence is not equivalent to global quiescence. A technical system can preserve a whole by rotating a maintenance relation across parts, temporarily withdrawing one scope from foreground use while leaving other scopes current and serviceable.

This is a useful abstraction for `technical-retention`, but it must not be mistaken for historical actor language or proof that unrelated maintenance systems share a common implementation lineage.

## 10. Open Questions

- obtain an archival/origin-hosted copy of the 2014 Micron LPDDR2 manual rather than relying on the preserved vendor-document mirror;
- recover and quote the exact normative JESD79-5 `REFsb` wording from a lawfully accessible standards copy;
- identify a named shipped DDR5 memory controller and document when/how it selects `REFsb` versus all-bank refresh;
- quantify workload-visible effects with product/platform measurements without confusing performance results with retention semantics;
- trace LPDDR2 `REFpb`, later LPDDR generations, and DDR5 `REFsb` historically in `computing-archaeology` before asserting genealogy.

## Sources

1. Micron Technology, **DDR5 DRAM** product page, current first-party comparison table: https://www.micron.com/products/memory/dram-components/ddr5-sdram
2. Micron Technology, **Micron DDR5 SDRAM: New Features**, current first-party technical material: https://assets.micron.com/adobe/assets/urn%3Aaaid%3Aaem%3A5ea148c8-e3fe-489e-8489-99b1b9cdcd3c/renditions/original/as/ddr5-new-features-white-paper.pdf
3. JEDEC press-release text mirrored by Design-Reuse, **JEDEC Publishes New DDR5 Standard for Advancing Next-Generation High Performance Computing Systems**, 2020-07-14: https://www.design-reuse.com/news/8558-jedec-publishes-new-ddr5-standard-for-advancing-next-generation-high-performance-computing-systems/
4. Micron Technology, current legacy LPDDR catalog entry for `EDB4432BBPA-1D-F`: https://www.micron.com/products/memory/dram-components/lpddr-components/part-catalog/part-detail/edb4432bbpa-1d-f
5. Micron-origin **168-Ball, Single-channel Mobile LPDDR2 SDRAM**, Rev. A 07/14, preserved vendor-document mirror: https://doczz.net/doc/8137024/168-ball--single-channel-mobile-lpddr2-sdram
EOF

cat > "$evidence_path" <<'EOF'
# Evidence 151 — DDR5 Same-Bank Refresh and Earlier Bank-Scoped DRAM Refresh (2014–2020)

Status: grounded evidence record

## Research Question

What public evidence is sufficient to establish that DDR5 exposes a bank-partitioned refresh mechanism that can preserve foreground access to untargeted banks, while also preventing the overclaim that DDR5 invented bank-scoped DRAM refresh?

## Evidence Classification

### E151.1 — JESD79-5 public publication boundary

- **Source:** JEDEC press-release text mirrored by Design-Reuse, 2020-07-14.
- **Class:** institutional historical record, preserved mirror (`I/H*`).
- **Claim supported:** JEDEC publicly announced publication of JESD79-5 DDR5 SDRAM on 2020-07-14.
- **Strength:** strong for public chronology.
- **Stop condition:** does not establish invention date, implementation date for every product, or exact normative `REFsb` language.

### E151.2 — Micron DDR5 command comparison

- **Source:** Micron first-party DDR5 SDRAM product documentation.
- **Class:** primary technical (`P`).
- **Claim supported:** DDR5 supports all-bank and same-bank refresh; Micron describes `REFsb` as refreshing a bank in each bank group.
- **Strength:** strong for public product/interface semantics.
- **Stop condition:** no inference about hidden controller scheduling or direct genealogy.

### E151.3 — Micron `REFsb` access-scope explanation

- **Source:** Micron first-party **DDR5 SDRAM: New Features** technical material.
- **Class:** primary technical (`P`).
- **Claim supported:** `REFsb` targets the same bank number across bank groups; targeted banks must be idle before refresh; non-targeted banks need not all be idle and remain available subject to refresh timing restrictions.
- **Strength:** strong for command-scope engineering reconstruction.
- **Stop condition:** does not mean every bank is always accessible or that `REFsb` creates zero workload stalls.

### E151.4 — 2014 Micron-origin LPDDR2 `REFpb` manual

- **Source:** **168-Ball, Single-channel Mobile LPDDR2 SDRAM**, Rev. A 07/14, Micron Technology copyright 2014, preserved by Doczz.
- **Class:** historical vendor-document mirror (`H/P*`).
- **Claim supported:** a named Micron/Elpida LPDDR2 family documented per-bank refresh (`REFpb`) by 2014; target bank is inaccessible during `tRFCpb`, while other banks remain accessible and may receive READ/WRITE commands; target bank selection follows a device bank counter.
- **Strength:** good prior-art floor, downgraded for non-origin hosting.
- **Stop condition:** do not call it an origin-hosted primary copy; do not infer that DDR5 `REFsb` is the same state machine.

### E151.5 — Current Micron legacy-part identity

- **Source:** Micron current catalog for `EDB4432BBPA-1D-F` / obsolete LPDDR family.
- **Class:** primary product identity (`P`).
- **Claim supported:** the part family represented in the preserved 2014 manual is a real Micron/Elpida LPDDR2 product family.
- **Strength:** corroborates provenance/product identity, not detailed command semantics.

## Claim Matrix

| Claim | Classification | Evidence | Confidence |
|---|---|---|---|
| JESD79-5 was publicly announced as published on 2020-07-14 | historical record | E151.1 | high |
| DDR5 `REFsb` refreshes a bank in each bank group | historical/technical record | E151.2–E151.3 | high |
| Untargeted banks can remain available while the selected same-bank set is refreshing, subject to timing rules | technical record | E151.3 | high |
| `same bank` does not mean exactly one physical bank in the entire device | engineering interpretation of public command scope | E151.3 | high |
| LPDDR2 `REFpb` already provided product-documented bank-scoped refresh by 2014 | prior-art historical record | E151.4–E151.5 | medium-high |
| DDR5 invented bank-scoped refresh | rejected claim | E151.4 | high confidence rejection |
| LPDDR2 `REFpb` directly caused or evolved into DDR5 `REFsb` | genealogy claim | not established | unsupported |
| `REFsb` implies per-row individualized retention profiling | implementation claim | not established | unsupported |
| a real DDR5 controller necessarily uses `REFsb` whenever possible | product policy claim | not established | unsupported |

## Engineering Reconstruction Boundary

The strongest safe reconstruction is interface-level:

`periodic refresh obligation -> legal REFsb opportunity -> selected bank number across bank groups enters refresh interval -> untargeted banks remain command-eligible subject to timing -> selected banks return to ordinary access -> repeated scoped episodes satisfy broader refresh schedule`

This reconstruction does **not** specify:

- how a CPU memory controller chooses between `REFab` and `REFsb`;
- exact silicon refresh micro-operations;
- row-remap/ECC/TRR interaction;
- workload-dependent scheduling heuristics;
- any undisclosed queue, timer, or persistent controller state.

## Prior-Art and Anti-Anachronism Notes

1. **2020 is a public DDR5 standard boundary, not an invention date.**
2. **2014 LPDDR2 is an earlier named-product bank-scoped-refresh floor, not proof of the first such implementation.**
3. `LPDDR2 REFpb != DDR5 REFsb`: the public targeting contracts differ.
4. Earlier chronology does not establish genealogy.
5. Current Micron DDR5 explanations are used to describe the public feature; they are not silently projected backward into the 2014 LPDDR2 state machine.
6. The 2014 manual is a vendor-origin document on a third-party mirror and is therefore explicitly downgraded to `H/P*` pending a better archival/origin copy.

## Cross-Case Limits

- **Case 03:** periodic restorative maintenance; Case 151 adds spatial partitioning of a refresh episode.
- **Case 09:** CBR/internal refresh address ownership; Case 151 is about service/maintenance scope rather than who advances the refresh address.
- **Case 10:** adaptive self-refresh cadence; Case 151 does not imply individualized leakage sensing.
- **Case 150:** managed-SSD GC can coexist with foreground service, but this is only a functional analogy. SSD reclamation, DRAM charge restoration, and their persistence states are unrelated mechanisms.

## Related-Repository Check

A repository search of `tmzncty/computing-archaeology` for `per-bank refresh` / `REFsb` found no dedicated case before this slice was opened. Broader DDR/LPDDR command genealogy, controller adoption, and DRAM organization history should be developed there rather than duplicated here.

## Sources

- Micron DDR5 SDRAM: https://www.micron.com/products/memory/dram-components/ddr5-sdram
- Micron DDR5 feature material: https://assets.micron.com/adobe/assets/urn%3Aaaid%3Aaem%3A5ea148c8-e3fe-489e-8489-99b1b9cdcd3c/renditions/original/as/ddr5-new-features-white-paper.pdf
- JEDEC publication announcement mirror, 2020-07-14: https://www.design-reuse.com/news/8558-jedec-publishes-new-ddr5-standard-for-advancing-next-generation-high-performance-computing-systems/
- Micron legacy LPDDR part identity: https://www.micron.com/products/memory/dram-components/lpddr-components/part-catalog/part-detail/edb4432bbpa-1d-f
- Micron-origin 2014 LPDDR2 manual mirror: https://doczz.net/doc/8137024/168-ball--single-channel-mobile-lpddr2-sdram
EOF

python3 - <<'PY'
from pathlib import Path

idx_path = Path('CASE_INDEX.md')
idx = idx_path.read_text(encoding='utf-8').rstrip() + '\n'
section = r'''

### Case 151 — DDR5 Same Bank Refresh: Partitioned Refresh Scope

3254. **[H]** JEDEC publicly announced publication of JESD79-5 DDR5 SDRAM on 2020-07-14; this is a public-standard boundary, not an invention date.
3255. **[H]** Micron documents DDR5 `REFsb` as refreshing a bank in each bank group rather than requiring an all-bank refresh episode.
3256. **[E]** `same-bank wording != exactly one physical bank total`; the public DDR5 command scope is the same bank number across bank groups.
3257. **[H]** Micron states that non-targeted banks need not all be idle during `REFsb` and remain available subject to the applicable timing restrictions.
3258. **[E]** `refresh obligation != whole-array unavailability`; mandatory retention maintenance does not require every bank to be blocked by every refresh episode.
3259. **[E]** `maintenance scope != retention scope`; a bank-partitioned operation can contribute to a device-wide periodic retention obligation.
3260. **[E]** `some bank scope under maintenance != all banks unavailable`; accessibility is scoped by the refresh command and timing contract.
3261. **[E]** `foreground service continuity != absence of refresh maintenance`; useful accesses can coexist with restorative work on another bank scope.
3262. **[H]** A Micron-origin 2014 LPDDR2 manual documents `REFpb` per-bank refresh on a named product family, with other banks accessible during the target bank's refresh cycle.
3263. **[E]** DDR5 `REFsb` must not be described as the global invention of bank-scoped DRAM refresh given the earlier LPDDR2 product record.
3264. **[E]** `LPDDR2 REFpb != DDR5 REFsb`; similar bank-scoped goals do not establish an identical targeting/state machine.
3265. **[E]** `earlier chronology != direct genealogy`; the 2014 prior-art floor blocks novelty overclaim without proving LPDDR2-to-DDR5 descent.
3266. **[E]** `controller-visible refresh granularity != per-row individualized retention profiling`; bank-scoped commands do not prove row-specific leakage measurement.
3267. **[E]** `interface capability != shipped controller scheduling policy`; the existence of `REFsb` does not establish when a concrete CPU/controller chooses to issue it.
3268. **[E]** refresh command/timing state is control/maintenance state, not a payload replica and not a complete history of previous refresh events.
3269. **[E]** bank-scoped refresh is not by itself ECC scrub or an integrity proof; those operations answer different failure/authority questions.
3270. **[E]** DRAM refresh is restorative retention maintenance, not sanitization or evidence that prior data has become irrecoverable.
3271. **[A]** Interpretation only: persistence obligations can be spatially decomposed so that one scope is temporarily withdrawn for maintenance while other scopes remain serviceable.
3272. **[E]** Related-repository boundary: broad DDR/LPDDR refresh genealogy and controller adoption belong in `computing-archaeology`; Case 151 retains only the bounded retention relation.
'''
idx_path.write_text(idx + section.lstrip('\n'), encoding='utf-8')

road_path = Path('ROADMAP.md')
road = road_path.read_text(encoding='utf-8')
entry = '- [x] Ground DDR5 same-bank refresh as a partitioned-maintenance case: JESD79-5 public boundary (2020), Micron `REFsb` one-bank-per-bank-group scope, untargeted-bank service continuity, LPDDR2 per-bank prior-art floor, and strict no-genealogy/no-controller-policy/no-sanitization boundaries (Case 151).'
if 'Case 151' not in road:
    lines = road.splitlines()
    inserted = False
    for i, line in enumerate(lines):
        if 'Case 150' in line and line.lstrip().startswith('- [x]'):
            lines.insert(i + 1, entry)
            inserted = True
            break
    if not inserted:
        if lines and lines[-1].strip():
            lines.append('')
        lines.append(entry)
    road_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
PY

# Integration-first validation occurs here, in the GitHub runner after canonical files are written.
git diff --check

grep -q '^Status: grounded' "$case_path"
grep -q 'LPDDR2 REFpb != DDR5 REFsb' "$case_path"
grep -q '3254\.' CASE_INDEX.md
grep -q '3272\.' CASE_INDEX.md
grep -q 'Case 151' ROADMAP.md

# Ensure only the intended canonical research files survive the integration commit.
git add CASE_INDEX.md ROADMAP.md "$case_path" "$evidence_path"
git rm -f scripts/integration_151.sh .github/workflows/integrate-case151.yml

changed="$(git diff --cached --name-only)"
for expected in CASE_INDEX.md ROADMAP.md "$case_path" "$evidence_path"; do
  grep -Fxq "$expected" <<<"$changed" || { echo "Missing staged file: $expected" >&2; exit 1; }
done
if grep -Eq '(^|/)integration_151\.sh$|integrate-case151\.yml$' <<<"$changed"; then
  echo "Temporary integration scaffolding is still staged as a surviving file change." >&2
  exit 1
fi

git commit -m "case151: ground DDR5 partitioned refresh scope"
git push origin HEAD:main
