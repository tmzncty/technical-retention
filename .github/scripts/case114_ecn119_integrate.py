from pathlib import Path

EVIDENCE_PATH = Path('evidence/114-nvme-2021-2024-multidomain-power-cycle-deepening.md')
CASE_PATH = Path('cases/114-nvme14-namespace-write-protection.md')
ROADMAP_PATH = Path('ROADMAP.md')
INDEX_PATH = Path('CASE_INDEX.md')

EVIDENCE = r'''# Evidence 114 Deepening — NVMe Multi-Domain Power-Cycle Scope and ECN119, 2021–2024

## Purpose

This record deepens [`../cases/114-nvme14-namespace-write-protection.md`](../cases/114-nvme14-namespace-write-protection.md) at one narrow standards-evolution boundary:

> What happens to a namespace protection state whose lifetime is defined by a `power cycle` once one namespace and its attached controllers may occupy different power domains?

The answer is not a new Flash-retention mechanism. It is a control-state lifetime problem: the event that clears `Write Protect Until Power Cycle` is only useful if its scope is operationally well defined across every access path that must enforce the same namespace state.

This file distinguishes historical / standards record (`H/P`), engineering reconstruction (`E`), functional analogy (`A`), philosophical interpretation (`I`), and unsupported extensions (`X`). It does **not** establish a named controller implementation, a hardware field failure, physical NAND immutability, or a direct genealogy from the 2019 feature proposal to ECN119.

---

## Source ledger

| Source | Date / revision | Type | Exact use | Limit |
| --- | --- | --- | --- | --- |
| NVM Express, [Base Specification Revision 1.4](https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf) | ratified 10 June 2019 | primary standard | original namespace-write-protection state machine; `Write Protect Until Power Cycle` survives controller reset but clears on power cycle; shared namespace state is enforced by every attached controller | predates the later multi-domain rule |
| NVM Express, [Base Specification Revision 2.0](https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-2_0-2021.06.02-Ratified-4.pdf) | ratified 2 June 2021 | primary standard | continuity of the four-state write-protection model after the 2.0 restructuring; preserves the simple power-cycle lifetime statement | not evidence that ECN119 already existed |
| NVM Express, [Specification Archives](https://nvmexpress.org/nvm-express-specification-archives/) — Base Specification Revision 2.0c | ratified 4 October 2022 | official archive + primary standard inspected in this pass | establishes a pre-ECN119 2.0-series boundary; the inspected write-protection clauses still use the prior state/lifetime form without the later multi-domain prohibition | absence is bounded to the inspected write-protection clauses, not every possible committee discussion |
| NVM Express, [Base Specification Revision 2.0d](https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-2.0d-2024.01.11-Ratified.pdf) | ratified 11 January 2024 | primary standard | adds the multi-domain `Write Protect Until Power Cycle` restriction and its simultaneous-power-cycle rationale; Set Features rejects the stated transition context | interface contract, not implementation trace |
| NVM Express, [Revision 2.1 Changes](https://nvmexpress.org/wp-content/uploads/NVM-Express-Revision-2.1-Changes-08_07.pdf) | 2024 change record | official standards-organization change record | identifies `ECN119 (mandatory)` as a new requirement / incompatible change and summarizes the different-domain prohibition | summary of standards evolution, not the ECN119 proposal body |
| NVM Express, [Base Specification Revision 2.1](https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.1-2024.08.05-Ratified.pdf) | ratified 5 August 2024 | primary standard | later normative continuity: `Write Protect Until Power Cycle` shall not be used in multi-domain NVM subsystems | later than the 2.0d incorporation point |

---

## Evidence A — the original lifetime was already namespace-wide, not controller-local

### A1. NVMe 1.4

Revision 1.4 defines `Write Protect Until Power Cycle` as a namespace state that does **not** persist across the relevant power-cycle transition, **does** persist across an NVMe Controller Level Reset, belongs to one namespace write-protection state machine, and is enforced by every controller to which the protected namespace is attached when the capability is exposed by the subsystem.

The important historical point is therefore not merely that a state is “temporary.” Its lifetime is keyed to a particular event class, while its authority is namespace-scoped across attached access paths.

Supported boundaries:

```text
controller reset != the power-cycle event that expires Write Protect Until Power Cycle
one namespace protection state != one independent controller-local protection state
```

These are 2019 contract claims. No later multi-domain wording is projected backward into Revision 1.4.

---

## Evidence B — NVMe 2.0 preserves the simple lifetime rule

Revision 2.0 retains the same four namespace write-protection states and again defines `Write Protect Until Power Cycle` as surviving Controller Level Reset but not the next power cycle.

The official archive places Revision 2.0c in October 2022. In the inspected 2.0c Namespace Write Protection state and Set-Features clauses, the later multi-domain prohibition is not yet present.

Supported chronology boundary:

```text
later multi-domain restriction != original 2019/2021 feature text
```

This is an absence claim only about the inspected normative write-protection clauses, not a claim that no engineer or workgroup had identified the issue before publication.

---

## Evidence C — Revision 2.0d makes event scope a topology problem

Revision 2.0d adds two linked rules. The Namespace Write Protection state section says `Write Protect Until Power Cycle` **should not be used** in a multi-domain NVM subsystem because clearing the state requires a simultaneous power cycle of the namespace and all controllers to which that namespace is attached. The Set Features rule says that if a command attempts to change a namespace into `Write Protect Until Power Cycle` in a multi-domain NVM subsystem (`MDS = 1`), the controller should abort the command with `Feature Not Changeable`.

The standard is not saying that NAND data cannot survive independently, nor that a controller reset clears the state. It is saying that the **expiry event for an authority relation becomes problematic when the entities participating in that relation can occupy separately power-cyclable domains**.

Supported boundaries:

```text
power-cycle-scoped authority lifetime != controller-local reset lifetime
named lifetime event != automatically local event scope
capability support != context-admissible state transition
```

---

## Evidence D — the standards body explicitly attributes the change to ECN119

NVM Express's Revision 2.1 change record labels **ECN119 mandatory** and places it under **New requirement / incompatible change**. Its summary says Namespace Write Protect Until Power Cycle is prohibited when the controller and namespace are in different domains because the namespace and controller must be simultaneously power cycled to clear the state.

This is stronger evidence than merely observing textual differences between two PDFs: the standards body itself classifies the change and names ECN119.

Supported historical claim:

```text
ECN119 is the official change attribution for the multi-domain WPUC restriction.
```

Not supported:

```text
ECN119 invented the general idea that distributed state lifetimes need coordinated reset events.
ECN119 proves a field failure in a named SSD or storage array.
```

The ECN119 proposal/body and committee deliberation were not separately inspected in this slice, so author, drafting chronology, motivation beyond the published rationale, and influence genealogy remain open.

---

## Evidence E — Revision 2.1 makes the topology restriction explicitly normative

Revision 2.1 states that `Write Protect Until Power Cycle` **shall not be used** in multi-domain NVM subsystems, again because clearing it requires simultaneous power cycling of the namespace and all controllers to which it is attached.

Supported boundary:

```text
ratified feature capability != permission to use every optional state in every subsystem topology
```

The optional WPUC state may be generally supported while a particular multi-domain context makes the transition inadmissible. Revision 2.1 is a later continuity witness; it is not silently substituted for 2.0d's exact `should` wording or for 1.4's 2019 contract.

---

## Engineering reconstruction

### E1. `temporary` needs an operationally realizable expiry event

A useful bounded model is:

```text
namespace state = Write Protect Until Power Cycle
        +
controllers A, B, ... enforce that same namespace state
        +
namespace/controller power domains may differ
        ↓
clearing event must cover the namespace and every attached controller
        ↓
partial/local power cycling is not sufficient evidence that the namespace-wide state has coherently expired
```

This is a reconstruction of the interface relation documented by ECN119-era text. It does not describe hidden firmware replication or the physical storage of the protection bit.

### E2. state lifetime is relational to topology

The same named state can have an easy-to-realize expiry condition in a simple subsystem and a coordination problem in a multi-domain subsystem.

> **Authority-state lifetime is not fully characterized by naming a duration/event; the event's scope relative to all entities that must agree on the state can also matter.**

`authority-state lifetime` and `event scope` are project terms, not NVM Express historical vocabulary.

### E3. capability, transition authority, and context admissibility remain different

At least three questions remain separate:

1. does the controller advertise Namespace Write Protection / WPUC capability?
2. is a requested stronger transition authorized by the feature's protection-control mechanism?
3. is that state admissible in the current subsystem topology?

ECN119 adds the third dimension. A positive answer to (1) is not sufficient for (3).

### E4. none of this strengthens payload retention physics

The rule says nothing about floating-gate or charge-trap retention time, ECC margin, read disturb, refresh/rewrite maintenance, FTL relocation, or physical sanitization.

```text
more carefully scoped write-protection lifetime != stronger physical data retention
```

---

## Functional comparisons — not genealogy

### A — Case 116 HDFS maintenance expiry

Case 116 has a retained administrative maintenance state with a time-based expiry that can change how long the system may rely on a temporarily unavailable DataNode. Case 114's WPUC deepening is different: its exit condition is a **power-topology event**, not a wall-clock deadline.

```text
policy/authority state can have an expiry condition distinct from payload lifetime
```

No HDFS-to-NVMe or distributed-system genealogy is implied.

### A — Case 120 Endurance Groups

Case 120 already warns that namespace scope, NVM-Set scope, and group-level history scope are not interchangeable. ECN119 adds another orthogonal scope distinction: **the entities that enforce a namespace state and the power domains through which its clearing event must propagate**.

This is a functional scope comparison only; Endurance Groups do not implement Namespace Write Protection.

---

## Philosophical interpretation — bounded

### I — a lifetime predicate can hide infrastructure assumptions

Calling a state `Until Power Cycle` sounds like a simple temporal qualification. The multi-domain change shows that such a label may also presuppose an infrastructure in which the relevant event can be applied coherently to every component that must share the state.

> **Technical temporariness can depend on the topology and coordination of the event that ends a state, not only on how long the state can physically survive.**

Stop condition: this is not a general theory of social or human memory, and the standard does not use the project's philosophical vocabulary.

---

## Claim ledger

| Claim | Layer | Strength / limit |
| --- | --- | --- |
| 1.4 WPUC survives Controller Level Reset but clears on power cycle | `H/P` | strong; original standard |
| shared namespace write-protection state is enforced across attached controllers | `H/P` | strong; original standard |
| 2.0 preserves the simple WPUC lifetime model | `H/P` | strong; primary standard |
| inspected 2.0c write-protection clauses lack the later multi-domain prohibition | `H/P` | bounded negative chronology claim only |
| 2.0d says WPUC should not be used in multi-domain subsystems and ties clearing to simultaneous power cycle of namespace + attached controllers | `H/P` | strong; primary standard |
| 2.0d Set Features should reject the multi-domain transition with `Feature Not Changeable` | `H/P` | strong; primary standard |
| NVM Express identifies ECN119 as mandatory / new requirement / incompatible change | `H/P` | strong; official change record |
| 2.1 says WPUC shall not be used in multi-domain subsystems | `H/P` | strong; later primary standard |
| `power cycle` in this state machine is equivalent to one controller reset | `X` | explicitly contradicted by state lifetime and ECN119 rationale |
| supporting WPUC means it is admissible in every topology | `X` | contradicted by multi-domain rule |
| ECN119 proves a named device bug/failure | `X` | no implementation/fault evidence inspected |
| multi-domain prohibition changes NAND charge-retention physics | `X` | no physical-retention mechanism established |
| Case 116 / Case 120 are genealogical ancestors of this rule | `X/A` | functional comparison only |

---

## Remaining evidence gaps

- retrieve and inspect the ECN119 proposal/body directly, including author/date/revision history and any stated interoperability motivation beyond the published change summary;
- identify the exact pre-2.0d draft/working-group point at which the new language entered the Base Specification;
- test a named multi-domain implementation or conformance environment and observe the exact `Feature Not Changeable` path;
- establish how specific controllers expose domain membership and namespace placement in real systems;
- keep the broader NVMe-oF and virtualization question open: multi-domain topology is not synonymous with either transport or virtualization;
- retain the existing Case-114 gaps around TP4005c, final SSC lineage, RPMB provisioning, transition-time power loss, and physical/forensic behavior.

These gaps do not weaken the bounded standards-evolution conclusion: **by the ECN119 / 2.0d–2.1 period, the NVMe specification explicitly treats WPUC expiry as a topology-sensitive coordinated power-cycle problem rather than a controller-local lifetime event.**
'''

if EVIDENCE_PATH.exists():
    raise SystemExit(f'{EVIDENCE_PATH} already exists')
EVIDENCE_PATH.write_text(EVIDENCE, encoding='utf-8')

case = CASE_PATH.read_text(encoding='utf-8')
ground = "Grounding record: [`../evidence/114-nvme-1996-2019-namespace-write-protection-grounding.md`](../evidence/114-nvme-1996-2019-namespace-write-protection-grounding.md)."
deep = "Later standards deepening: [`../evidence/114-nvme-2021-2024-multidomain-power-cycle-deepening.md`](../evidence/114-nvme-2021-2024-multidomain-power-cycle-deepening.md)."
if ground not in case:
    raise SystemExit('Case 114 grounding marker not found')
if deep not in case:
    case = case.replace(ground, ground + '\n\n' + deep, 1)

section_marker = '## Retained state decomposition'
if section_marker not in case:
    raise SystemExit('Case 114 retained-state marker not found')
deep_section = r'''## Later standards deepening — ECN119 and multi-domain power-cycle scope

The 2019 bounded case defines `Write Protect Until Power Cycle` as surviving an NVMe Controller Level Reset but clearing on a power cycle, while one namespace protection state is enforced by every controller attached to the namespace. Later standards evolution exposes a topology assumption hidden inside that apparently simple lifetime rule.

Revision 2.0 preserves the original four-state model. The inspected Revision 2.0c write-protection clauses likewise do not yet contain the later multi-domain prohibition. Revision 2.0d (11 January 2024), however, says `Write Protect Until Power Cycle` should not be used in a **multi-domain NVM subsystem** because clearing it requires a simultaneous power cycle of the namespace and all controllers to which that namespace is attached; its Set Features rule correspondingly says an attempt to enter that state in a multi-domain subsystem should be aborted with `Feature Not Changeable`.

NVM Express's own Revision-2.1 change record attributes this change to **ECN119 (mandatory)** and classifies it as a **new requirement / incompatible change**. Revision 2.1 then uses the stronger normative formulation that the state **shall not be used** in multi-domain NVM subsystems.

Historical/standards boundary (`H/P`):

> **the multi-domain restriction is a later ECN119-era standards change; it must not be projected backward as if it were already explicit in NVMe 1.4.**

Engineering reconstruction (`E`):

> **a state whose expiry is named by an event such as `power cycle` can still need a topology-scoped definition of that event when the authority relation spans independently powerable entities.**

The useful decomposition is now:

```text
feature capability
!= transition authorization
!= topology/context admissibility
!= shared namespace authority state
!= event scope needed to expire that state
!= payload-retention physics
```

In particular, `power cycle` here is not equivalent to an NVMe Controller Level Reset; power-cycling one attached controller is not established as sufficient to expire the shared namespace state in a multi-domain topology; advertising support for WPUC does not make that state admissible in every topology; and the standards change says nothing about NAND charge lifetime, ECC margin, internal relocation, or sanitization.

Functional comparison (`A`): Case 116's HDFS maintenance expiry also shows that control-state expiry and payload lifetime are distinct, but HDFS uses a time/policy expiry while ECN119 concerns a coordinated power-topology event. Case 120 separately demonstrates that namespace, NVM-Set, and Endurance-Group scopes differ; ECN119 adds an orthogonal power-domain/event-scope distinction. Neither comparison is a genealogy claim.

Philosophical interpretation (`I`, bounded): `Until Power Cycle` illustrates how an apparently temporal label can hide infrastructure assumptions about **which components must participate in the event that ends the state**. The interpretation stops at that engineering relation; it is not a theory of memory in general.

Primary deepening record: [`../evidence/114-nvme-2021-2024-multidomain-power-cycle-deepening.md`](../evidence/114-nvme-2021-2024-multidomain-power-cycle-deepening.md).

---

'''
if '## Later standards deepening — ECN119 and multi-domain power-cycle scope' not in case:
    case = case.replace(section_marker, deep_section + section_marker, 1)

old_gap = '- establish whether virtualization or NVMe-oF deployments alter any host-visible authority boundary;'
new_gap = '- validate ECN119/Revision-2.1 multi-domain rejection on a named controller, emulator, or conformance environment, including real domain-membership exposure;\n- establish whether NVMe-oF or virtualization deployments outside the bounded multi-domain rule alter any other host-visible authority boundary;'
if old_gap in case:
    case = case.replace(old_gap, new_gap, 1)
CASE_PATH.write_text(case, encoding='utf-8')

roadmap = ROADMAP_PATH.read_text(encoding='utf-8')
rm_prefix = '- [x] NVMe 1.4 Namespace Write Protection / mutation-authority persistence boundary —'
rm_lines = roadmap.splitlines()
hits = [i for i, line in enumerate(rm_lines) if line.startswith(rm_prefix)]
if len(hits) != 1:
    raise SystemExit(f'Expected one Case 114 roadmap line, found {len(hits)}')
sub = "  - [x] ECN119 multi-domain power-cycle deepening — [`evidence/114-nvme-2021-2024-multidomain-power-cycle-deepening.md`](evidence/114-nvme-2021-2024-multidomain-power-cycle-deepening.md): NVMe 2.0 preserves the original `Write Protect Until Power Cycle` lifetime while Revision 2.0d adds the multi-domain restriction and NVM Express attributes it to mandatory ECN119; Revision 2.1 makes the topology rule explicitly normative. This closes only the bounded `power-cycle lifetime event != controller-local reset`, `feature capability != topology-admissible transition`, and `shared authority lifetime can require coordinated event scope` seam. Direct ECN119 proposal-body archaeology, named-device/conformance traces, transition-time fault injection, and broader NVMe-oF/virtualization behavior remain open; generic NVMe power-domain history belongs primarily in `computing-archaeology`."
if sub not in rm_lines:
    rm_lines.insert(hits[0] + 1, sub)
ROADMAP_PATH.write_text('\n'.join(rm_lines) + '\n', encoding='utf-8')

index = INDEX_PATH.read_text(encoding='utf-8')
idx_prefix = '| [NVM Express 1.4 Namespace Write Protection: Mutation Authority, State Lifetime, and Transition Durability]'
idx_lines = index.splitlines()
ihits = [i for i, line in enumerate(idx_lines) if line.startswith(idx_prefix)]
if len(ihits) != 1:
    raise SystemExit(f'Expected one Case 114 index row, found {len(ihits)}')
row = idx_lines[ihits[0]]
old_ev = '[1996–2019 grounding record](evidence/114-nvme-1996-2019-namespace-write-protection-grounding.md);'
new_ev = '[1996–2019 grounding record](evidence/114-nvme-1996-2019-namespace-write-protection-grounding.md) + [2021–2024 multi-domain power-cycle deepening](evidence/114-nvme-2021-2024-multidomain-power-cycle-deepening.md);'
if old_ev not in row:
    raise SystemExit('Case 114 index evidence marker not found')
row = row.replace(old_ev, new_ev, 1)
row = row.replace('NVMe-oF/virtualization behavior', 'named multi-domain conformance/fault validation and remaining NVMe-oF/virtualization behavior', 1)
idx_lines[ihits[0]] = row
index = '\n'.join(idx_lines) + '\n'

findings_heading = '## Case 114 — ECN119 multi-domain power-cycle deepening findings'
findings = r'''

## Case 114 — ECN119 multi-domain power-cycle deepening findings

- **2849 — WPUC lifetime event != Controller Level Reset:** the original state contract already makes `Write Protect Until Power Cycle` survive Controller Level Reset while clearing on the specified power-cycle event. (`H/P`)
- **2850 — shared namespace authority != independent controller-local authority:** the write-protection state is namespace-scoped and enforced by every attached controller when the capability is present. (`H/P`)
- **2851 — later multi-domain restriction != original 2019 rule:** Revision 2.0 preserves the simple state lifetime; the inspected 2.0c write-protection clauses do not yet contain the later multi-domain prohibition. (`H/P`, bounded chronology)
- **2852 — multi-domain topology != automatically admissible WPUC:** Revision 2.0d says WPUC should not be used in a multi-domain NVM subsystem. (`H/P`)
- **2853 — expiry event name != local event scope:** 2.0d explains that clearing WPUC requires simultaneous power cycling of the namespace and all attached controllers. (`H/P`, `E`)
- **2854 — capability support != context-admissible transition:** a controller may advertise WPUC support while the multi-domain context makes a Set Features transition into that state inadmissible. (`H/P`, `E`)
- **2855 — inadmissible transition != silent state divergence:** 2.0d specifies `Feature Not Changeable` for the attempted multi-domain transition instead of permitting a state whose clearing event is ambiguous across domains. (`H/P`, `E`)
- **2856 — ECN119 attribution != inferred diff archaeology:** NVM Express's own change record labels ECN119 mandatory and classifies the rule as a new requirement / incompatible change. (`H/P`)
- **2857 — ECN119 official attribution != proposal-body genealogy:** the change record identifies the ECN, but this slice does not establish its author, committee deliberation, first draft, or design influence beyond the published rationale. (`H/P`, `X`)
- **2858 — 2.0d `should` wording != 2.1 `shall` wording:** Revision 2.1 supplies the later explicit normative prohibition; its wording must not be silently substituted for the exact 2.0d text. (`H/P`)
- **2859 — coordinated expiry scope != payload-retention mechanism:** the rule governs namespace mutation-authority state and says nothing about NAND charge retention, ECC margin, refresh, FTL relocation, or sanitization. (`H/P`, `E`, `X`)
- **2860 — `simultaneous power cycle` != measured nanosecond-level timing requirement:** the standards phrase establishes participating-entity/event scope, not an implementation timing tolerance or physical synchronization experiment. (`H/P`, `E`, `X`)
- **2861 — multi-domain != NVMe-oF or virtualization by definition:** ECN119's topology rule cannot be generalized into claims about every remote, virtualized, or fabric-attached deployment without additional evidence. (`H/P`, `X`)
- **2862 — Case 116 expiry comparison != genealogy:** HDFS maintenance expiry and NVMe WPUC both separate control-state expiry from payload lifetime, but one is a time/policy boundary and the other a power-topology event. (`A`)
- **2863 — related-repository boundary:** fresh `computing-archaeology` searches for `Namespace Write Protect`, `TP4005c`, and `ECN119` found no dedicated overlapping study; broader NVMe power-domain/standards genealogy belongs there, while Case 114 keeps the retention-specific authority-lifetime relation. (`H/P` project-state record)
'''
if findings_heading not in index:
    index = index.rstrip() + findings + '\n'
INDEX_PATH.write_text(index, encoding='utf-8')
