from pathlib import Path

ROOT = Path('.')
CASE = ROOT / 'cases/121-ddr5-prac-activation-counter-initialization.md'
ROADMAP = ROOT / 'ROADMAP.md'
INDEX = ROOT / 'CASE_INDEX.md'
EVIDENCE = ROOT / 'evidence/121-ddr5-prac-powerup-reset-reconstitution-deepening.md'

EVIDENCE_TEXT = r'''# Case 121 Deepening — DDR5 PRAC Power-Up / System-Reset Reconstitution

## Scope

This note deepens [`../cases/121-ddr5-prac-activation-counter-initialization.md`](../cases/121-ddr5-prac-activation-counter-initialization.md) at one narrow boundary:

> What happens to the *authority* of PRAC activation-counter state across a reset or power-up boundary, and what must be re-established before the device may rely on those counters again?

The purpose is not to write a general DDR5 reset history. It is to separate four relations that are easy to collapse:

1. physical survival of activation-counter cells;
2. host-visible PRAC enable state;
3. host-visible ACI-completion/readiness evidence;
4. the protocol authority to use the counters for activation tracking and Alert Back-Off (ABO).

The bounded result is that a reset can invalidate readiness/authority even when the inspected product text does not establish physical erasure of the counter cells, while a later Micron patent disclosure treats power-up as a condition in which counter bits may be unknown and therefore require reinitialization.

## Source custody and evidence confidence

### Micron DDR5 SDRAM Product Core Data Sheet, Rev. E (11/2024)

The manufacturer-authored Micron core data sheet is currently inspectable through an Avnet-hosted PDF mirror:

- Micron Technology, *DDR5 SDRAM Product Core Data Sheet*, Rev. E, 11/2024, section `Per Row Activation Counting` / MR70.
- Mirror: <https://www.avnet.com/wcm/connect/dacdfea7-999f-4ee0-b514-6f9e0bf68c6d/ddr5-sdram-core.pdf?MOD=AJPERES>

This pass uses the indexed PDF text rather than claiming a fresh Micron-hosted facsimile custody chain. The source is still manufacturer-authored product documentation; the hosting/provenance limitation is recorded instead of silently treating the mirror as a different source family.

### US20250316301A1, Micron Technology

- Micron Technology, Inc., `Apparatuses and methods for activation counter initialization`, US20250316301A1, filed 21 March 2025, published 9 October 2025.
- Public record: <https://patents.justia.com/patent/20250316301>

This is a patent disclosure, not a normative DDR5 product contract and not proof that every disclosed embodiment shipped. It is used only to deepen the power-up/reinitialization mechanism boundary already visible in the product documentation.

## Historical record

### November 2024 product contract: system reset clears PRAC readiness evidence

Micron Rev. E already establishes the ordinary PRAC/ACI handoff used in the main Case 121 record:

- PRAC is optional and disabled by default in the bounded product contract;
- after the host enables PRAC, a full-array ACI is required;
- activation tracking and ABO are withheld until ACI is complete;
- completion is exposed through MR70 `OP[3]`;
- entering ACI again clears that completion indication until initialization finishes.

The same product text adds the reset boundary needed here: a system reset that disables PRAC also resets MR70 `OP[3]` to zero.

This establishes a product-level fact about **control/readiness state**. It does **not** say that system reset physically erases every activation-counter cell or proves what analog values remain in those cells immediately after reset.

### October 2025 patent disclosure: power-up can make counter values unknown

Micron's later ACI patent application describes embodiments in which activation-counter bits may be in an unknown state at power-up or after DRAM refresh requirements have been violated. The disclosed response is initialization to a known state before the counters are relied upon. The application also repeats the enable → full-array ACI → completion → counting/ABO sequence and the system-reset clearing of ACI-completion status.

This provides a primary public mechanism witness for the stronger **power-up reconstitution** relation, but it must remain source-typed correctly:

> product reset semantics ≠ patent embodiment ≠ universal JEDEC rule.

The patent can support an engineering explanation of why reinitialization is useful. It cannot be silently substituted for an inspected normative JESD79-5C reset clause or for cross-vendor product behavior.

## Engineering reconstruction

### Readiness invalidation ≠ demonstrated physical erasure

The product contract clears ACI completion when system reset disables PRAC. That is enough to show that the old `ready` relation is not allowed to survive transparently across that transition.

It is not enough to establish what happened to the underlying counter-cell charge.

Therefore:

> **ACI-complete cleared ≠ activation-counter cells physically erased.**

and:

> **possible physical survival ≠ post-reset protocol authority.**

A retained embodiment can outlive the permission to trust it.

### Reconstitution is a protocol path, not recovery of old history

The bounded restart path is better represented as:

```text
pre-reset PRAC-active regime
    -> system reset disables PRAC and clears ACI-complete evidence
    -> host enables PRAC again
    -> full-array ACI establishes known counter values
    -> ACI completion becomes true
    -> activation tracking / ABO may resume
```

ACI therefore creates a new trusted starting condition. It does not reconstruct the precise pre-reset activation-count history.

> **counter reinitialization ≠ counter-history recovery.**

The previous per-row counts may have been useful while the old powered/refresh regime was current; the protocol can deliberately stop treating them as authoritative after the regime boundary.

### Power-up unknown-state handling ≠ a durable checkpoint contract

The patent disclosure is especially useful as a negative boundary. It does not describe preserving every activation count in nonvolatile storage and replaying it after power returns. Instead, it permits the counter state to be unknown and restores a known initial condition before reliance.

That supports the bounded reconstruction:

> **PRAC activation-count state has a regime-bounded authority horizon in the inspected evidence; no cross-power durable-checkpoint guarantee is established.**

This does not mean the counters are useless or transient in an arbitrary sense. Within a valid powered and refreshed regime, their accumulated values are precisely what drives future disturbance-protection decisions.

### Reset of protection state ≠ reset of payload semantics

The product statement about system reset is specifically about disabling PRAC and clearing ACI-completion state. It must not be inflated into a claim that system reset itself physically erases user payload.

Separately, the ordinary ACI contract warns that pre-existing array data need not be preserved during ACI. Those are different transitions:

- **system reset:** invalidates PRAC enable/readiness relations in the bounded product text;
- **ACI:** establishes counter state and is not promised to preserve previously written main-array data;
- **refresh violation / power-up patent scenario:** may leave counter state unknown and can trigger the need for ACI.

Keeping these transitions separate prevents `reset`, `power loss`, `refresh violation`, and `ACI` from becoming one generic forgetting event.

### Reinitialization can be safer than retaining stale authority

A system that retained arbitrary counter bits across a regime boundary but continued to treat them as trustworthy would have a worse epistemic problem than one that explicitly clears readiness and reinitializes before use.

The engineering lesson is narrow:

> **forgetting the authority of maintenance metadata can preserve the correctness of later maintenance decisions.**

This is not a claim that every reset should erase maintenance history. It is specific to a state whose intended role can be re-established before the system relies on it again.

## Functional analogy — bounded

### Case 09: refresh-row enumerator

Case 09's bounded TI refresh counter can be initialized on power-on and then cyclically enumerates rows. Case 121's PRAC counters summarize per-row activation pressure and require ACI before they become trusted.

The functional similarity is that both are DRAM maintenance-control states that can be **reconstituted by initialization rather than treated as durable historical checkpoints**.

The mechanisms and meanings remain different:

> cyclic refresh-row phase ≠ per-row accumulated disturbance-pressure summary.

No genealogy is asserted.

### Case 83: HDFS BlockScanner cursor

The contrast is more useful than the similarity. HDFS saves a scanner cursor specifically so restart can resume maintenance progress and avoid replay from the beginning when the checkpoint remains usable. The bounded PRAC reset path instead withdraws authority from prior completion/count state and establishes a new starting condition through ACI.

> **restart-progress checkpoint ≠ reset-reinitialized protection summary.**

This strengthens Synthesis 26's rule that `maintenance-control state` does not imply one universal persistence horizon.

## Philosophical interpretation — bounded

This case adds a small refinement to the repository's account of persistence and authority:

> a technical state can remain materially possible while the system deliberately ceases to count it as an admissible continuation of the control relation that once made it meaningful.

For PRAC, the decisive transition is not merely whether charge remains somewhere in counter cells. The device/host protocol also needs a valid relation among enable state, known counter initialization, completion evidence, and later counting/ABO authority.

This is an engineering-derived interpretation. It is not Micron or JEDEC philosophical vocabulary, and it should not be generalized into a claim that all memory requires semantic reauthorization after reset.

## Rejected claims / stop conditions

This slice does **not** establish any of the following:

- system reset physically erases PRAC counter cells;
- PRAC activation counts are guaranteed to survive power loss;
- Micron's patent embodiment is the normative JESD79-5C reset contract;
- every DDR5 vendor implements the same counter-cell topology or reset path;
- ACI recovers the previous activation history;
- clearing ACI-complete status proves payload corruption;
- power-up, reset, refresh violation, and ACI are one identical failure mechanism;
- reinitializable maintenance metadata is always less important than durable metadata;
- the Case 09, Case 83, and Case 121 mechanisms share a historical genealogy.

## Related-repository boundary

A repository search found no existing PRAC/ACI-focused treatment in `tmzncty/computing-archaeology` during this pass. The broader history of DDR5 PRAC proposals, JEDEC revision chronology, cross-vendor counter implementations, and memory-controller deployment should primarily be built there if pursued. `technical-retention` keeps only the bounded retention relation: **reset/power-up can terminate the authority horizon of maintenance-control state and require reconstitution before reuse.**

## Remaining evidence debt

- direct normative JESD79-5C reset/power-up clauses and revision-by-revision PRAC changes;
- cross-vendor product documentation for ACI and reset semantics;
- named-controller traces showing reset → enable → ACI → completion → ABO readiness;
- independent fault injection across reset, aborted ACI, refresh violation, and power loss;
- physical characterization of whether/how activation-counter cells retain analog state across reset/power transitions;
- PRAC + ARFM/DRFM interaction after reinitialization.
'''

CASE_HISTORICAL = r'''### Power-up / system-reset reconstitution deepening

A later bounded pass adds a reset/power-up distinction that the original grounding left open. Micron Rev. E (11/2024) states that a system reset which disables PRAC also clears ACI-completion status (`MR70:OP[3]=0`). That is a product-contract statement about readiness/control state; it does not establish that reset physically erases the activation-counter cells themselves.

Micron's later ACI patent application, US20250316301A1 (published 9 October 2025), separately describes power-up as a condition in which activation-counter bits may be unknown and therefore require initialization to a known state before reliance. Because this is a patent embodiment rather than an inspected normative JEDEC clause, it is used only as a primary mechanism witness, not as a universal DDR5 rule.

Evidence: [`../evidence/121-ddr5-prac-powerup-reset-reconstitution-deepening.md`](../evidence/121-ddr5-prac-powerup-reset-reconstitution-deepening.md).

'''

CASE_ENGINEERING = r'''### Reset can invalidate counter authority without proving physical erasure

The reset path exposes a useful distinction among embodiment, readiness, and authority. Clearing ACI-completion state means the old trusted-counter relation does not transparently survive the transition. The inspected product text does not say that the counter cells are physically erased by that reset.

Therefore:

> **ACI-complete cleared ≠ activation-counter cells physically erased.**

and:

> **possible physical survival ≠ post-reset protocol authority.**

The later patent's power-up path reinforces the reconstitution boundary: counter values may be unknown, and the safe response is to establish a known starting condition through ACI rather than to assume that old values remain trustworthy.

> **counter reinitialization ≠ recovery of previous activation history.**

This gives the PRAC maintenance-control state a bounded persistence horizon: its authority can end at a reset/power-up regime boundary even though the protection mechanism can become usable again after explicit reinitialization. It is therefore not a durable-checkpoint contract.

'''

ROADMAP_BULLET = r'''- [x] Case 121 DDR5 PRAC power-up / system-reset reconstitution deepening — [`cases/121-ddr5-prac-activation-counter-initialization.md`](cases/121-ddr5-prac-activation-counter-initialization.md), deepened by [`evidence/121-ddr5-prac-powerup-reset-reconstitution-deepening.md`](evidence/121-ddr5-prac-powerup-reset-reconstitution-deepening.md): Micron Rev. E (11/2024) clears ACI-completion status when a system reset disables PRAC, while Micron's later US20250316301A1 disclosure treats power-up as a condition in which activation-counter bits may be unknown and require initialization before use. This closes the bounded `readiness invalidation != physical counter-cell erasure` / `reinitialization != previous-count-history recovery` seam without promoting a patent embodiment into universal JEDEC or cross-vendor reset semantics. Direct normative JESD79-5C reset clauses, cross-vendor behavior, named-controller traces, and fault injection remain open; broad PRAC/DDR5 genealogy belongs primarily in `computing-archaeology`.

'''

FINDINGS = r'''- **2680 — system-reset readiness clearing ≠ physical counter-cell erasure:** Micron Rev. E clears ACI-completion status when system reset disables PRAC, but the inspected product text does not establish that the activation-counter cells are physically erased. (`H/P`, `E`, `X`)
- **2681 — ACI completion ≠ durable restart witness:** the bounded product contract deliberately clears completion evidence across the reset transition, so prior completion is not a cross-reset certificate of present counter readiness. (`H/P`, `E`)
- **2682 — possible embodiment survival ≠ post-reset authority:** even if some counter-cell charge physically survives, the protocol does not thereby authorize the old count state after readiness has been invalidated. (`E`)
- **2683 — power-up can require counter-state reconstitution:** Micron US20250316301A1 describes activation-counter bits as potentially unknown at power-up and initializes them to a known state before reliance. (`H/P`, `E`)
- **2684 — product reset contract ≠ patent power-up embodiment:** the 11/2024 data sheet and 10/2025 patent are distinct source types; the latter cannot be silently promoted into a normative JESD79-5C or cross-vendor rule. (`H/P`, `X`)
- **2685 — reset-triggered reinitialization ≠ ordinary refresh:** ACI establishes known maintenance-control values; ordinary refresh preserves existing volatile cell values. (`E`)
- **2686 — PRAC disabled after reset ≠ payload physically erased:** the bounded reset statement concerns PRAC enable/readiness and does not by itself establish user-array erasure. (`E`, `X`)
- **2687 — readiness evidence cleared ≠ initialization failure:** `ACI complete = 0` after reset can represent deliberate invalidation of prior readiness rather than evidence that an attempted ACI failed. (`E`)
- **2688 — policy re-enabled ≠ counters ready:** after a regime boundary, enabling PRAC and completing ACI remain separate steps before activation tracking/ABO may resume. (`H/P`, `E`)
- **2689 — refreshed powered-regime continuity ≠ cross-power persistence guarantee:** the inspected sources ground volatile counter maintenance within operation but do not establish nonvolatile preservation of activation counts across loss of power. (`H/P`, `E`, `X`)
- **2690 — ACI after power-up ≠ recovery of previous activation history:** initialization creates a new known starting condition rather than reconstructing the pre-power-down sequence or exact accumulated counts. (`E`, `X`)
- **2691 — maintenance-control persistence horizon can be regime-bounded:** a state may be constitutive while the regime is active yet safely lose authority at reset if the protocol reconstitutes it before future reliance. (`E/A`)
- **2692 — PRAC-count reinitialization ≠ DRAM refresh-counter phase identity:** Case 09 and Case 121 both admit initialization of maintenance-control state, but cyclic row enumeration and per-row disturbance-pressure summaries remain different retained objects and mechanisms. (`A`, `X`)
- **2693 — PRAC reset reconstitution ≠ HDFS restart-progress checkpointing:** Case 83 preserves scanner position to reduce replay; Case 121 can deliberately invalidate old count readiness and establish a new starting condition. (`A`)
- **2694 — functional similarity ≠ genealogy:** the Case 09/83/121 comparison classifies persistence horizons only; it establishes no historical descent among DRAM refresh counters, PRAC state, and HDFS scanner cursors. (`A`, `X`)
'''


def require_once(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one occurrence, found {count}')


# Create evidence record.
if EVIDENCE.exists():
    existing = EVIDENCE.read_text(encoding='utf-8')
    if existing != EVIDENCE_TEXT:
        raise RuntimeError('evidence file already exists with different content')
else:
    EVIDENCE.write_text(EVIDENCE_TEXT, encoding='utf-8')

# Deepen Case 121.
case = CASE.read_text(encoding='utf-8')
grounding_old = 'Grounding record: [`../evidence/121-ddr5-2021-2025-prac-activation-counter-grounding.md`](../evidence/121-ddr5-2021-2025-prac-activation-counter-grounding.md).'
grounding_new = grounding_old + '\n\nReset/power-up deepening: [`../evidence/121-ddr5-prac-powerup-reset-reconstitution-deepening.md`](../evidence/121-ddr5-prac-powerup-reset-reconstitution-deepening.md).'
if 'Reset/power-up deepening:' not in case:
    require_once(case, grounding_old, 'Case grounding anchor')
    case = case.replace(grounding_old, grounding_new, 1)

hist_anchor = '### Earlier prior art: per-row activation-count state predates JESD79-5C\n'
if '### Power-up / system-reset reconstitution deepening' not in case:
    require_once(case, hist_anchor, 'Case historical anchor')
    case = case.replace(hist_anchor, CASE_HISTORICAL + hist_anchor, 1)

eng_anchor = '### Maintenance metadata is itself volatile\n'
if '### Reset can invalidate counter authority without proving physical erasure' not in case:
    require_once(case, eng_anchor, 'Case engineering anchor')
    case = case.replace(eng_anchor, CASE_ENGINEERING + eng_anchor, 1)

old_debt = '- power-cycle/reset semantics beyond the bounded public product contract;'
new_debt = '- direct normative JESD79-5C reset/power-up semantics, cross-vendor behavior, and named-controller reset traces beyond the bounded Micron product + patent evidence;'
if old_debt in case:
    require_once(case, old_debt, 'Case open-debt anchor')
    case = case.replace(old_debt, new_debt, 1)
CASE.write_text(case, encoding='utf-8')

# Add a completed roadmap slice immediately before the broad DRAM-evolution item.
roadmap = ROADMAP.read_text(encoding='utf-8')
roadmap_anchor = '- [ ] DRAM evolution and refresh machinery beyond the bounded case'
if 'Case 121 DDR5 PRAC power-up / system-reset reconstitution deepening' not in roadmap:
    require_once(roadmap, roadmap_anchor, 'ROADMAP DRAM anchor')
    roadmap = roadmap.replace(roadmap_anchor, ROADMAP_BULLET + roadmap_anchor, 1)
ROADMAP.write_text(roadmap, encoding='utf-8')

# Update the Case 121 table row by adding the deepening record and narrowing the reset debt.
index = INDEX.read_text(encoding='utf-8')
lines = index.splitlines()
row_hits = [i for i, line in enumerate(lines) if '(cases/121-ddr5-prac-activation-counter-initialization.md)' in line and line.startswith('|')]
if len(row_hits) != 1:
    raise RuntimeError(f'CASE_INDEX Case 121 row: expected one hit, found {len(row_hits)}')
ri = row_hits[0]
row = lines[ri]
if '121-ddr5-prac-powerup-reset-reconstitution-deepening.md' not in row:
    if not row.rstrip().endswith('|'):
        raise RuntimeError('CASE_INDEX Case 121 row has unexpected table shape')
    row = row.rstrip()[:-1].rstrip()
    row += ' + [2024–2025 reset/power-up reconstitution deepening](evidence/121-ddr5-prac-powerup-reset-reconstitution-deepening.md); direct normative JESD79-5C reset clauses, cross-vendor behavior, controller traces, and fault injection remain open |'
    lines[ri] = row
index = '\n'.join(lines) + ('\n' if index.endswith('\n') else '')

# Insert new findings into the existing Case 121 findings section.
if '**2680 —' not in index:
    section = '## Case 121 — DDR5 PRAC activation-counter findings\n'
    require_once(index, section, 'CASE_INDEX Case 121 findings section')
    start = index.index(section) + len(section)
    next_header = index.find('\n## Case ', start)
    if next_header == -1:
        next_header = len(index)
    block = index[start:next_header]
    if '**1946 —' not in block:
        raise RuntimeError('CASE_INDEX Case 121 existing findings not found in section')
    insertion = '\n' + FINDINGS.rstrip() + '\n'
    index = index[:next_header] + insertion + index[next_header:]

INDEX.write_text(index, encoding='utf-8')

# Local assertions keep this helper one-shot and bounded.
case = CASE.read_text(encoding='utf-8')
roadmap = ROADMAP.read_text(encoding='utf-8')
index = INDEX.read_text(encoding='utf-8')
assert case.count('121-ddr5-prac-powerup-reset-reconstitution-deepening.md') >= 2
assert roadmap.count('Case 121 DDR5 PRAC power-up / system-reset reconstitution deepening') == 1
assert roadmap.count('121-ddr5-prac-powerup-reset-reconstitution-deepening.md') == 1
for n in range(2680, 2695):
    marker = f'**{n} —'
    assert index.count(marker) == 1, (n, index.count(marker))
assert index.count('121-ddr5-prac-powerup-reset-reconstitution-deepening.md') >= 1
