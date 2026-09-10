# Evidence 114 Deepening — NVMe Multi-Domain Power-Cycle Scope and ECN119, 2021–2024

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
