from pathlib import Path
import re

CASE = Path('cases/111-enterprise-ssd-extended-shutdown-maintenance.md')
EVIDENCE = Path('evidence/111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md')
ROADMAP = Path('ROADMAP.md')
INDEX = Path('CASE_INDEX.md')
CASE76 = Path('cases/76-jedec-ssd-endurance-retention-qualification.md')
CASE37 = Path('cases/37-samsung-840-evo-old-data-performance-refresh.md')

for p in (ROADMAP, INDEX, CASE76, CASE37):
    if not p.exists():
        raise SystemExit(f'missing required file: {p}')
if CASE.exists() or EVIDENCE.exists():
    raise SystemExit('Case 111 or Evidence 111 already exists; refuse duplicate integration')

case = r'''# Enterprise SSD Extended Shutdown: Qualification Window, Powered Maintenance, and Operator Scheduling

## Status

**`grounded`** for the bounded vendor operational-guidance relation described below.

Grounding record: [`../evidence/111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md`](../evidence/111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md).

## Scope

- **Object / system:** enterprise SSD/NVMe storage kept powered off for extended periods, as addressed by IBM storage-system support guidance and Dell PowerEdge support guidance.
- **Historical anchor:** an IBM support-content mirror records the extended-shutdown guidance as created on **16 December 2020**; the current IBM support page is marked modified **28 March 2023**.
- **Later continuity / cross-vendor witness:** Dell support article **000198930**, version 3, marked last modified **14 May 2026**.
- **Research question:** what changes when a standards-level power-off retention interval becomes an operator scheduling problem involving backup, environment, powered maintenance opportunity, recommissioning time, and sometimes an explicit read sweep?

This case is a bounded continuation of Case 76's JESD218 SSD endurance/retention qualification relation and Case 37's product-specific powered periodic refresh. It is **not**:

- a new derivation of the JESD218 qualification tables;
- a claim that every enterprise SSD fails exactly at three months;
- a claim that every SSD implements Dell's described background tasks in the same way;
- a claim that merely applying power always completes retention maintenance;
- a claim that a full-device read universally rewrites NAND;
- a controlled endurance/retention experiment;
- a firmware-internals study;
- an archival-storage recommendation for all SSD classes;
- an invention-priority claim for Flash refresh, scrubbing, or powered maintenance.

The bounded retention claim is:

> **A power-off retention qualification interval can be operationalized as a maintenance schedule without becoming the same thing as that schedule. IBM and Dell both warn about extended enterprise-SSD shutdown around the three-month / 40 °C regime, yet prescribe different powered-run intervals. Dell additionally documents powered background retention work and a full-used-NAND read as a trigger for retention tasks. The surviving vendor record therefore separates passive offline survival, maintenance opportunity, maintenance completion, operator policy, and standards qualification.**

`maintenance opportunity`, `operator scheduling`, `offline survival`, and `recommissioning window` are project engineering terms unless explicitly attributed to a source.

## Historical vocabulary

The vendor sources use terms including:

- `extended shutdown` / `prolonged power off`;
- `data retention`;
- `power off` / `powered-up`;
- `end of life`;
- `background tasks`;
- `data retention tasks`;
- `wear-leveling`;
- `read operation`;
- `used NAND cells`;
- `backup`;
- `decommissioned`.

The following are project terms rather than historical vendor vocabulary:

- `qualification window`;
- `maintenance opportunity`;
- `maintenance-completion evidence`;
- `operator retention policy`;
- `fleet-level retention infrastructure`.

## Historical record

### H/P — IBM operationalizes the three-month retention boundary as an earlier power-on schedule

IBM's support article **“Potential for SSD data loss after extended shutdown”** states that the JEDEC enterprise-SSD requirement is a minimum of three months at 40 °C and warns that after prolonged shutdown there is potential for data loss or drive failure. Its operational recommendation is deliberately earlier than that boundary: a system and its enclosed drives should be **powered up for at least two weeks after two months of system power off**. IBM separately recommends recent backups before extended shutdown, maintaining the powered-off environment below 40 °C, and avoiding extended power-off for a drive already reporting end-of-life status.

A surviving IBM support-content mirror records the article as created **16 December 2020**; the current IBM support page records a modified date of **28 March 2023**. The creation timestamp is used only as a publication floor for this support guidance, not as an invention date for the underlying retention concern.

The important historical relation is therefore:

```text
three-month / 40 °C standards background
    !=
IBM operator schedule of two months off + at least two weeks powered
```

IBM presents the latter as conservative operational guidance, not as a redefinition of the JEDEC requirement.

### H/P — Dell explicitly distinguishes powered background retention work from the unpowered interval

Dell's current PowerEdge support article **000198930**, version 3, last modified **14 May 2026**, states that enterprise SSD/NVMe devices perform data-retention tasks while powered and that extended power-off removes the opportunity for those tasks. It additionally says wear-leveling occurs while the drives are powered, whether idle or handling host I/O.

Dell then recommends, for its affected PowerEdge context and “based on current technology,” that SSD/NVMe drives containing user data be **powered up once every 2.5 months for a minimum duration of three weeks** to allow background tasks to complete. Dell adds that larger capacities can require longer powered-on duration.

This is unusually useful because it blocks a common shortcut:

```text
power restored
    !=
retention maintenance demonstrated complete
```

The documented operator action includes **time under power**, not merely a transition from off to on.

### H/P — Dell gives a second maintenance path: read all used NAND cells

The same Dell support article says that, alternatively, **a read operation on all used NAND cells triggers the data-retention tasks**, and recommends that approach for larger-capacity drives.

Within this source's bounded product-support claim, a full read is therefore not described only as passive verification. It can be an **event that triggers device retention work**.

That does not establish that:

- every physical page is rewritten;
- every controller uses the same read-reclaim algorithm;
- every vendor has the same trigger;
- a successful read proves future retention for a specific interval.

The internal implementation remains undisclosed in the inspected Dell source.

### H/P — the two vendors do not publish one universal operator cadence

IBM's surviving guidance says two months off followed by at least two weeks powered. Dell's current guidance says 2.5 months off followed by at least three weeks powered, with longer powered time as capacities increase, or a read sweep over used NAND.

The historical record therefore gives a useful negative result:

> **shared reference to a three-month enterprise retention regime ≠ one standardized operator maintenance schedule**.

The support policies are vendor/system guidance layered above the standards-level qualification relation.

## Engineering reconstruction

### E — qualification interval and maintenance schedule are different relations

Case 76 grounds JESD218's bounded SSD qualification relation at a specified endurance/workload/temperature/use condition. Case 111 adds a different relation: what an operator is told to do when a deployed storage system will remain off long enough to approach that risk window.

```text
qualification condition
    -> states what a rated device must satisfy under a test/use model

operator maintenance schedule
    -> states when to intervene conservatively in a deployed system
```

The schedule can be earlier than the qualification boundary without contradicting it. A maintenance recommendation includes safety margin, fleet uncertainty, environmental uncertainty, time needed for background work, and backup/recommissioning concerns not encoded by one headline retention interval.

### E — passive offline survival and active powered maintenance must be separated

The bounded vendor documentation supports at least three states:

1. **powered off:** NAND must retain enough recoverable state without controller background work;
2. **powered but maintenance incomplete:** the controller has an opportunity to perform work, but Dell's minimum powered-duration language warns against treating power presence as completion evidence;
3. **powered with a prescribed maintenance opportunity:** sufficient run time or a vendor-prescribed read sweep is supplied so retention tasks can execute under the documented policy.

Therefore:

> **unpowered nonvolatility ≠ unpowered maintenance availability**;

and:

> **powered state ≠ proved maintenance completion**.

The first relation is consistent with Case 37's Samsung statement that its product-specific periodic refresh did not run while the drive was powered off. The second is newly sharp at the operator-policy level because Dell assigns a minimum powered duration.

### E — a read sweep can be maintenance-triggering without becoming universal “refresh” semantics

Dell's statement that reading all used NAND cells triggers retention tasks means that, in that bounded support regime:

> **read sweep ≠ verification-only operation**.

But the evidence does not justify the stronger statement:

> `every read refreshes every NAND cell`.

The host action and the hidden device action are different layers. A host issues reads over a logical used-data set; firmware may use the resulting error/age/read evidence to schedule hidden work. The source does not disclose exact physical rewrite geometry, thresholds, or completion telemetry.

### E — maintenance time becomes capacity-sensitive operational infrastructure

Dell says larger-capacity drives require longer powered-on duration for the background tasks. That directly makes **elapsed maintenance opportunity** an operational resource.

The source does not provide a formula, so the defensible result is only:

> **larger capacity can lengthen the prescribed maintenance window**,

not a linear scaling law and not a universal per-terabyte constant.

This is a retention issue that has migrated above the NAND cell: rack power, operator scheduling, system availability, backup state, and time reserved for maintenance can all become part of whether the retained state remains safely serviceable.

### E — “three months” is a risk/qualification boundary, not a deterministic failure clock

Neither the standard-level relation grounded in Case 76 nor the vendor support wording proves that one particular drive becomes unreadable exactly when a clock reaches three months. IBM says there is **potential** for data loss/failure after extended shutdown; Dell says systems powered off for more than three months **may** exhibit errors or faults.

Therefore:

> **retention interval ≠ deterministic individual-drive failure time**.

The practical policy is conservative precisely because actual wear, active-use temperature, power-off temperature, controller state, NAND variation, and maintenance history can differ.

## Cross-case comparison

### Case 76 — JESD218 endurance/retention qualification

Case 76 answers:

> what must remain true at a rated endurance boundary under a specified SSD qualification relation?

Case 111 asks instead:

> how do system vendors turn an extended power-off risk into an operator runbook before or around that boundary?

Thus:

```text
standards qualification
    !=
field maintenance policy
```

The field policy can cite the standard while adding earlier intervention, backup, environment, powered-run duration, and recommissioning rules.

### Case 37 — Samsung 840 EVO periodic refresh

Case 37 gives a named commercial product episode in which Samsung described a powered periodic refresh feature for **old-data read performance** and explicitly said it did not operate while power was off.

Case 111 is not another 840 EVO refresh case. It moves the comparison one level outward: IBM and Dell document **operator-facing shutdown schedules** for enterprise SSD/NVMe systems. The similarity is functional — powered time can be retention infrastructure — while the product, target property, mechanism, and evidence class differ.

### Case 36 — Flash Correct-and-Refresh

Case 36 is a research algorithm/evaluation for maintaining NAND recoverability within ECC margin. Case 111 contains no evidence that IBM or Dell implemented that algorithm. `background retention task`, `read-triggered task`, and academic `FCR` are not synonyms and no genealogy is asserted.

## Prior art and anti-anachronism

No invention-priority claim is made for either support article. The standards relation predates them, and Case 37 already grounds a 2014–2015 commercial SSD maintenance episode in which powered time mattered. The 2020–2026 sources are valuable because they expose **operator-facing policy**: how a storage vendor tells administrators to manage an extended shutdown once nonvolatile media cannot simply be treated as indefinitely passive shelf storage.

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no dedicated enterprise-SSD extended-shutdown / powered-maintenance case to reuse. A generic history of SSD retention-management firmware belongs there; this case keeps only the retention-specific distinction among qualification, offline survival, powered maintenance opportunity, operator scheduling, and recommissioning.

## Failure and forgetting boundaries

For this bounded case, distinguish:

- **extended power-off:** controller background work is unavailable;
- **approaching a vendor risk window:** policy calls for backup/environment checks and a powered maintenance interval;
- **power restored:** maintenance becomes possible but is not thereby proved complete;
- **sufficient powered interval or read sweep:** a vendor-prescribed opportunity/trigger is supplied for hidden retention tasks;
- **post-maintenance service:** ordinary operation resumes, without the support article proving a new universal shelf-life guarantee;
- **drive at end of life:** IBM warns against extended power-off, further separating endurance state from calendar time alone.

None of these states proves physical sanitization, permanent archival safety, or future correctness without qualification.

## Functional analogy and philosophical limit

A limited functional analogy is useful: a supposedly “passive” nonvolatile storage system can impose **periodic human scheduling work** because the device's own maintenance machinery cannot operate while unpowered. Retention work can therefore cross an organizational boundary: from cell physics and controller firmware into power planning, backup policy, rack/system availability, and operator time.

This is a project interpretation, not IBM or Dell's historical vocabulary. It must not be generalized into the claim that every act of powering a system is “memory maintenance,” or that operational runbooks are the same mechanism as NAND refresh.

## Claim ledger

| Claim | Type | Evidence strength | Boundary |
| --- | --- | --- | --- |
| IBM support guidance recommends at least two weeks powered after two months off | H/P | strong | IBM affected-system operational guidance, not universal SSD law |
| Dell current guidance recommends every 2.5 months, minimum three weeks powered | H/P | strong | Dell PowerEdge affected-product context; version 3, 14 May 2026 |
| Dell says powered SSD/NVMe performs retention background tasks while extended power-off prevents them | H/P | strong | vendor support description; firmware internals not disclosed |
| Dell says a read over all used NAND cells triggers retention tasks | H/P | strong | bounded Dell claim; does not prove universal read-refresh semantics |
| qualification interval ≠ operator maintenance schedule | E | strong | cross-source decomposition, not source vocabulary |
| power restored ≠ maintenance completion | E | strong | Dell minimum-duration wording supports the distinction |
| same standards background ≠ same vendor cadence | H/E | strong | IBM and Dell prescriptions differ |
| powered maintenance opportunity can become fleet-level retention infrastructure | E/A | medium | useful cross-layer interpretation, not vendor terminology |
| IBM/Dell guidance demonstrates FCR or Samsung's exact refresh algorithm | X | rejected | no genealogy or implementation identity established |
| three months is a deterministic failure instant for every drive | X | rejected | vendor wording is probabilistic/risk-based and Case 76 is qualification-bounded |

## Open questions

- What was the first publication date of Dell article 000198930 before the surviving version-3 modification date?
- Which named SSD controller/firmware families under Dell's affected systems implement the described read-triggered retention behavior, and how?
- What telemetry, if any, proves that the prescribed background work has completed?
- How does required powered duration scale with capacity and amount of used NAND in the vendor implementation?
- Can independent fault/retention testing validate the IBM/Dell operational windows after rated endurance?
- How do other enterprise vendors operationalize long powered-off intervals?
- How do these runbooks change across later NAND generations and controller ECC/refresh policies?

## Sources

- IBM Support, **“Potential for SSD data loss after extended shutdown,”** current page modified 28 March 2023: <https://www.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>.
- IBM support-content mirror of the same guidance, showing creation on 16 December 2020: <https://supportcontent.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>.
- Dell Technologies Support, **“PowerEdge: Data Retention Occur with SSD or Nvme Drives Due to Prolonged Power off,”** article 000198930, version 3, last modified 14 May 2026: <https://www.dell.com/support/kbdoc/en-us/000198930/ssd-data-retention-considerations-when-powering-off-systems-for-a-prolonged-duration>.
- Internal standards context: [`Case 76 — JEDEC JESD218 SSD Endurance Qualification`](76-jedec-ssd-endurance-retention-qualification.md).
- Internal commercial-refresh comparison: [`Case 37 — Samsung 840 EVO Old-Data Performance Restoration`](37-samsung-840-evo-old-data-performance-refresh.md).
'''

EVIDENCE_TEXT = r'''# Evidence 111 — IBM / Dell Enterprise-SSD Extended-Shutdown Guidance, 2020–2026

## Scope

This record grounds a narrow operational-retention case: two infrastructure vendors publish guidance for enterprise SSD/NVMe systems that may remain powered off long enough for power-off retention to become an operator concern.

It does **not** independently reproduce JESD218; that standards relation is already grounded in Case 76. It does not infer undocumented firmware algorithms from support prose.

## Source 1 — IBM Support: “Potential for SSD data loss after extended shutdown”

**Current page:** <https://www.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>

**Support-content mirror:** <https://supportcontent.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>

**Publication metadata observed:**

- surviving support-content mirror: `Created by Richard Hopkins on Wed, 12/16/2020 - 09:26`;
- current IBM page: `Modified date: 28 March 2023`;
- UID: `ibm16382908`.

### Directly grounded record

The current IBM page states:

- JEDEC enterprise SSD retention background of a minimum **three months at 40 °C**;
- after extended power-off there is potential for data loss and/or drive failures;
- a system and its enclosed drives should be **powered up at least two weeks after two months of system power off**;
- drives reporting end-of-life status should not be powered off for extended periods;
- the powered-off environment should remain below 40 °C;
- regular/recent backup is recommended before extended shutdown.

The affected-product metadata spans IBM storage products including Storwize, SAN Volume Controller, and FlashSystem families. The present case does not claim the same physical SSD model or controller implementation across all of them.

### Evidence boundary

IBM's wording is support/runbook guidance. It does not publish:

- controller firmware source;
- a NAND-page rewrite trace;
- proof that all maintenance completes in exactly two weeks;
- raw qualification data;
- a deterministic three-month failure threshold.

The 16 December 2020 mirror timestamp is used as a public guidance floor, not an invention date for the underlying technical mechanism.

---

## Source 2 — Dell Technologies Support article 000198930

**Document:** _PowerEdge: Data Retention Occur with SSD or Nvme Drives Due to Prolonged Power off_

**URL:** <https://www.dell.com/support/kbdoc/en-us/000198930/ssd-data-retention-considerations-when-powering-off-systems-for-a-prolonged-duration>

**Article properties observed:**

- Article Number: **000198930**;
- Article Type: **Solution**;
- Version: **3**;
- Last Modified: **14 May 2026**.

### Exact semantic locations inspected

`Symptoms` / `Cause`:

- Dell says enterprise SSD/NVMe retains data via NAND voltage levels;
- it says drive firmware performs background tasks as part of data retention;
- while powered, SSD/NVMe devices carry out data-retention tasks and wear-leveling can occur while idle or under host I/O;
- extended power-off prevents those tasks from running.

`Resolution`:

- Dell invokes JESD218/JESD219 and a **three-month** power-off interval at maximum rated endurance;
- it separately lists P/E-cycle/TBW state, active-use temperature, and power-off temperature as retention-relevant conditions;
- it recommends powering SSD/NVMe with user data **once every 2.5 months for a minimum of three weeks** so background tasks can complete;
- it states larger capacities require longer powered duration;
- it gives an alternative: **read all used NAND cells** to trigger data-retention tasks, recommended for larger drives;
- it recommends decommissioning/backing up servers stored powered off longer than three months until they can return to production use.

### What this source directly grounds

**H/P:** Dell currently documents an operator-facing relation among extended power-off, background-retention opportunity, powered run time, capacity, and a read-triggered maintenance path.

**E:** the document makes `power restored` distinguishable from `background retention work given time/opportunity to complete`.

**E:** because a read sweep is described as triggering retention tasks, the host-visible read operation and the hidden maintenance action should be modeled separately.

### Evidence boundary

The inspected page does not disclose:

- whether the retention task rewrites every page, migrates selected blocks, adjusts read references, or uses some other controller policy;
- thresholds for selecting cells/blocks;
- maintenance-completion telemetry;
- a formula relating capacity to minimum powered duration;
- whether identical behavior applies outside the listed PowerEdge/Express Flash context;
- the article's original first-publication date before version 3.

Therefore `read all used NAND cells triggers retention tasks` is retained as a **vendor-specific operational claim**, not generalized into `all NAND reads refresh cells`.

---

## Cross-source comparison

| Relation | IBM | Dell | Bounded conclusion |
| --- | --- | --- | --- |
| standards background | cites enterprise 3 months / 40 °C | cites enterprise 3 months at maximum rated endurance and ≤40 °C storage | same broad risk/qualification background |
| intervention point | after 2 months off | every 2.5 months | operator schedule is earlier than/around headline boundary |
| powered duration | at least 2 weeks | minimum 3 weeks | no universal vendor cadence |
| explicit hidden task | not specified in detail | powered background/data-retention tasks | power presence and maintenance work are separable |
| read-trigger path | not stated | full read of used NAND triggers retention tasks | Dell-specific trigger, not universalized |
| capacity dependence | not stated | larger capacity requires longer powered duration | qualitative relation only; no scaling law |
| backup / long-storage policy | recent backup; avoid extended off at EOL | backup/decommission if stored off >3 months | retention runbook includes operational safety margin |

The strongest cross-source finding is negative:

```text
same three-month enterprise retention background
    !=
one standardized power-up schedule
    !=
one standardized maintenance-completion rule
```

The vendor runbooks layer operational policy above a qualification relation.

## Cross-case grounding

### Case 76

Case 76 establishes that the JESD218 number belongs to a workload/endurance/temperature/error-bounded SSD qualification relation. Evidence 111 therefore does not interpret `three months` as a free-standing physical shelf-life constant.

### Case 37

Case 37 grounds a Samsung 840 EVO product-specific periodic-refresh statement and the fact that the described background feature does not operate while powered off. That is a useful earlier product-level witness for `unpowered persistence != powered maintenance availability`, but it is not evidence for IBM/Dell implementation identity.

### computing-archaeology reuse check

Repository search for `SSD data retention extended shutdown power-off refresh` in `tmzncty/computing-archaeology` returned no dedicated case to reuse in this slice. Generic SSD/controller history remains out of scope here.

## Claim-type ledger

| Claim | Type | Strength |
| --- | --- | --- |
| IBM publication/support guidance exists by December 2020 | H/P | strong for surviving support mirror |
| IBM recommends two months off + at least two weeks powered | H/P | strong |
| Dell version 3 recommends 2.5 months + minimum three weeks powered | H/P | strong |
| Dell documents powered background retention work | H/P | strong |
| Dell documents full-used-NAND read as a retention-task trigger | H/P | strong |
| qualification boundary != vendor runbook | E | strong |
| powered state != proved maintenance completion | E | strong |
| read sweep != verification-only in Dell's bounded regime | H/E | strong |
| vendor guidance proves one universal SSD refresh algorithm | X | rejected |
| three months is deterministic device failure time | X | rejected |
| Case 37 -> IBM/Dell direct genealogy | X | rejected |

## Evidence gaps deliberately left open

1. first-publication archaeology for Dell article 000198930 before the 14 May 2026 version-3 modification;
2. named-drive/controller mapping for Dell's described hidden retention tasks;
3. telemetry or service logs proving maintenance completion;
4. independent post-endurance fault/retention tests of the recommended shutdown schedules;
5. cross-vendor operational guidance beyond IBM and Dell;
6. direct firmware or patent evidence for the read-triggered retention path;
7. capacity-to-maintenance-time scaling.
'''

CASE.parent.mkdir(parents=True, exist_ok=True)
EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
CASE.write_text(case.rstrip() + '\n', encoding='utf-8')
EVIDENCE.write_text(EVIDENCE_TEXT.rstrip() + '\n', encoding='utf-8')

# ROADMAP: add a bounded, checked operational-policy slice after the existing
# cross-vendor Case 76 product-contract bullet.
roadmap = ROADMAP.read_text(encoding='utf-8')
new_bullet = ('- [x] Enterprise SSD extended-shutdown operational maintenance — canonical '
              '[`cases/111-enterprise-ssd-extended-shutdown-maintenance.md`](cases/111-enterprise-ssd-extended-shutdown-maintenance.md), with '
              '[`evidence/111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md`](evidence/111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md), '
              'grounds a bounded 2020–2026 IBM/Dell operator-policy layer above Case 76: IBM recommends at least two weeks powered after two months off, while Dell version 3 recommends every 2.5 months with at least three weeks powered, states that powered devices perform background retention work, and documents a full-used-NAND read as a trigger for retention tasks. This closes only `qualification interval != operator schedule`, `power-on != maintenance completion`, and `read sweep != verification-only` in the named vendor guidance; firmware internals, completion telemetry, independent validation, cross-vendor generalization, and Dell first-publication archaeology remain open.')
if new_bullet not in roadmap:
    lines = roadmap.splitlines()
    idx = next((i for i, line in enumerate(lines) if line.startswith('- [x] Cross-vendor TLC/QLC manufacturer product-contract corroboration —')), None)
    if idx is None:
        raise SystemExit('ROADMAP Case 76 cross-vendor anchor not found')
    lines.insert(idx + 1, new_bullet)
    roadmap = '\n'.join(lines) + '\n'
ROADMAP.write_text(roadmap.rstrip() + '\n', encoding='utf-8')

# CASE_INDEX: insert Case 111 row after Case 110.
index = INDEX.read_text(encoding='utf-8')
row = ('| [Enterprise SSD Extended Shutdown: Qualification Window, Powered Maintenance, and Operator Scheduling]'
       '(cases/111-enterprise-ssd-extended-shutdown-maintenance.md) | **grounded** | enterprise SSD/NVMe offline NAND retention + '
       'vendor-prescribed powered maintenance opportunity + backup/environment/run-time policy + bounded read-triggered retention path | '
       'separate standards qualification from operator cadence; passive power-off survival from powered maintenance opportunity; power restoration from '
       'maintenance completion; full read from verification-only semantics; shared retention background from one universal runbook | '
       '[2020–2026 IBM/Dell extended-shutdown grounding](evidence/111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md); Dell first-publication date, '
       'firmware internals, completion telemetry, independent post-endurance validation, capacity scaling, and broader vendor comparison remain open |')
if row not in index:
    lines = index.splitlines()
    idx = next((i for i, line in enumerate(lines) if line.startswith('| [Amazon S3 Object Lock:')), None)
    if idx is None:
        raise SystemExit('CASE_INDEX Case 110 row anchor not found')
    lines.insert(idx + 1, row)
    index = '\n'.join(lines) + '\n'

# Append findings only if the expected predecessor is still the current maximum.
nums = [int(m.group(1)) for m in re.finditer(r'^([0-9]+)\. \*\*', index, flags=re.M)]
if not nums or max(nums) != 1725:
    raise SystemExit(f'unexpected CASE_INDEX finding max: {max(nums) if nums else None}; expected 1725')
findings = r'''

## Case 111 — Enterprise SSD extended-shutdown operational-retention findings

1726. **qualification interval ≠ operator maintenance schedule** — Case 76's standards relation says what a rated SSD must satisfy under bounded workload/endurance/temperature/error conditions, while IBM and Dell prescribe earlier/around-boundary intervention schedules for deployed systems; a support runbook can add safety margin without redefining the standard;
1727. **powered state ≠ maintenance completion** — Dell does not prescribe a momentary power-on event: it requires a minimum powered duration so background tasks can complete, making maintenance opportunity and completion analytically distinct;
1728. **unpowered nonvolatility ≠ unpowered maintenance availability** — Dell says retention tasks run while powered and not during extended power-off; Case 37 independently gives a product-specific earlier example of a periodic refresh feature that does not operate while off, without establishing implementation identity;
1729. **full read ≠ verification-only in the bounded Dell guidance** — Dell says reading all used NAND cells triggers retention tasks, so a host-visible read sweep can be an initiating condition for hidden maintenance rather than merely a passive proof attempt;
1730. **read-triggered retention work ≠ universal NAND read-refresh semantics** — Dell does not disclose page-selection thresholds, rewrite geometry, controller algorithm, or cross-vendor applicability; the vendor support statement cannot be inflated into `every read refreshes every cell`;
1731. **same three-month standards background ≠ one vendor cadence** — IBM recommends two months off followed by at least two weeks powered, while Dell recommends every 2.5 months with at least three weeks powered or a read sweep; the operator policy is not standardized by the shared headline retention interval;
1732. **three-month retention interval ≠ deterministic individual-drive failure clock** — IBM uses `potential` and Dell uses `may` for post-shutdown failures; qualification/risk boundaries must not be rewritten as an exact time-to-failure law;
1733. **maintenance recommendation ≠ independent standards-compliance proof** — IBM/Dell support guidance can invoke JEDEC and prescribe operations without supplying the raw sample/UBER/FFR data required to audit one drive family's qualification;
1734. **larger capacity can require longer maintenance opportunity ≠ linear scaling law** — Dell explicitly says powered duration increases with capacity but publishes no proportionality formula in the inspected article;
1735. **background-task existence ≠ disclosed physical rewrite mechanism** — the support article names retention tasks and wear-leveling but does not prove whether a specific task rewrites every page, migrates selected blocks, changes read references, or uses another controller policy;
1736. **operator scheduling ≠ device-autonomous scheduling** — deciding when a powered-off server must be re-energized is a fleet/operator control relation even if the work performed after power-on is autonomous inside the SSD;
1737. **backup/decommission policy ≠ NAND retention mechanism** — IBM and Dell include backup or decommissioning in the runbook because operational safety can add an independent copy/availability layer; those actions do not describe how charge is retained inside the original NAND;
1738. **Case 37 product refresh ≠ Case 111 fleet guidance** — Samsung 840 EVO's 2015 periodic-refresh statement concerns a named consumer-product old-data performance incident, whereas Case 111 concerns enterprise-system extended-shutdown support policy; the common role of powered time is functional comparison only;
1739. **standards-qualified offline retention ≠ archival shelf-storage recommendation** — Case 76's bounded power-off interval and Case 111's conservative runbooks do not justify treating SSDs as indefinitely passive archives or, conversely, declaring all data unreadable immediately after the nominal interval;
1740. **related-repository boundary** — current `computing-archaeology` search found no dedicated enterprise-SSD extended-shutdown/powered-maintenance case; generic SSD firmware/history should be built there if pursued, while Case 111 keeps only the retention-specific split among qualification, offline survival, powered maintenance opportunity, operator scheduling, and recommissioning.
'''
if '## Case 111 — Enterprise SSD extended-shutdown operational-retention findings' not in index:
    index = index.rstrip() + findings + '\n'
INDEX.write_text(index.rstrip() + '\n', encoding='utf-8')

# Cross-links from the two canonical predecessor cases.
for path, link_text in (
    (CASE76, 'Operational continuation: [`Case 111 — Enterprise SSD Extended Shutdown`](111-enterprise-ssd-extended-shutdown-maintenance.md) separates this qualification relation from later IBM/Dell operator power-up schedules, powered maintenance opportunity, and recommissioning policy.'),
    (CASE37, 'Operational continuation: [`Case 111 — Enterprise SSD Extended Shutdown`](111-enterprise-ssd-extended-shutdown-maintenance.md) moves the powered-maintenance comparison outward from this named-product episode to IBM/Dell operator-facing shutdown schedules; the link is functional, not genealogical.'),
):
    text = path.read_text(encoding='utf-8')
    if link_text not in text:
        marker = 'Grounding record:'
        pos = text.find(marker)
        if pos < 0:
            raise SystemExit(f'grounding-record anchor missing in {path}')
        line_end = text.find('\n', pos)
        if line_end < 0:
            raise SystemExit(f'grounding-record line end missing in {path}')
        text = text[:line_end+1] + '\n' + link_text + '\n' + text[line_end+1:]
    path.write_text(text.rstrip() + '\n', encoding='utf-8')

# Local consistency checks before the workflow performs git-level checks.
assert CASE.exists() and EVIDENCE.exists()
assert 'two weeks after two months' in CASE.read_text(encoding='utf-8')
assert '2.5 months' in CASE.read_text(encoding='utf-8')
assert 'full-used-NAND read' in ROADMAP.read_text(encoding='utf-8')
assert '**1740. **' not in INDEX.read_text(encoding='utf-8')
assert '1740. **related-repository boundary**' in INDEX.read_text(encoding='utf-8')
