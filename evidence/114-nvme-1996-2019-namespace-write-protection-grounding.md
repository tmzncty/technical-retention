# Evidence 114 — NVMe Namespace Write Protection, 1996–2019 Prior-Art and Contract Grounding

## Purpose

This record grounds the bounded claims in [`../cases/114-nvme14-namespace-write-protection.md`](../cases/114-nvme14-namespace-write-protection.md).

The source question is deliberately narrow:

> When NVMe 1.4 makes a namespace write protected, what state persists, what durability work is required at the transition, what operations remain allowed, and what earlier write-protection evidence prevents an NVMe-first novelty claim?

This record does **not** establish named-controller implementation, physical NAND immutability, WORM compliance, RPMB provisioning practice, or a direct SCSI→NVMe genealogy.

---

## Source ledger

| Source | Date / revision | Type | Exact use | Limit |
| --- | --- | --- | --- | --- |
| NVM Express, [`Changes in NVMe Revision 1.4`](https://nvmexpress.org/changes-in-nvme-revision-1-4/) | revision-1.4 change record | official standards-organization web record | identifies `Namespace Write Protect (optional)` as a new revision-1.4 feature, per-namespace scope, references §§5.14/5.15/5.21/8.10/8.19 and TP4005c | summary, not full normative state machine |
| NVM Express, [`NVM Express Base Specification Revision 1.4`](https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf) | ratified 10 June 2019 | primary standard | Feature Identifier 84h; four protection states; persistence across power/reset; authentication control; cross-controller enforcement; command interactions; volatile-cache commit on transition | interface contract, not implementation disclosure |
| NVM Express, [`NVM Express Base Specification Revision 1.4c`](https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4c-2021.06.28-Ratified.pdf) | header revision date 9 March 2021 | later primary standard | later searchable continuity check for the same feature/state-machine family | later revision is not silently substituted for exact 2019 wording where historical wording matters |
| NVM Express, [`NVMe Namespaces`](https://nvmexpress.org/resource/nvme-namespaces/) | current official educational page | institutional explanatory source | corroborates namespace as host-accessible LBA collection and per-namespace write-protection concept | current educational wording, not a 2019 historical source |
| X3T10, [`96-179r0 — Additional Write Protection functions for SSC`](https://www.t10.org/ftp/t10/document.96/96-179r0.pdf) | 10 May 1996 | primary committee proposal | earlier `Persistent Write Protect` / `Permanent Write Protect` vocabulary and proposed volume-persistent semantics | proposal status; tape/SSC-specific; no direct genealogy established |

---

## Evidence A — revision-1.4 novelty boundary

### A1. Official NVM Express change record

NVM Express's `Changes in NVMe Revision 1.4` page places `Namespace Write Protect (optional)` in its **New Features** section. It describes the feature as controlling write protection on a **per namespace** basis and says it may be used to prevent modification of a specified namespace.

The page points readers to:

- §5.14;
- §5.15;
- §5.21;
- §8.10;
- §8.19;
- Technical Proposal `4005c`.

### Supported claim

```text
Namespace Write Protection is a new optional capability of NVMe revision 1.4.
```

### Not supported

```text
NVMe 1.4 invented software write protection.
NVMe 1.4 invented persistent/permanent write protection.
TP4005c is the first conception of the mechanism.
```

The 1996 T10 evidence below independently blocks the broader novelty claims.

---

## Evidence B — exact 2019 state lifetime

### B1. Base Specification 1.4 §8.19 / Figure 488

The ratified 2019 specification defines four namespace write-protection states:

| State | Across power cycle | Across NVMe Controller Level Reset |
| --- | --- | --- |
| `No Write Protect` | persists | persists |
| `Write Protect` | persists | persists |
| `Write Protect Until Power Cycle` | does **not** persist; transitions to `No Write Protect` | persists |
| `Permanent Write Protect` | persists | persists |

The initial namespace state at creation is `No Write Protect`.

### Supported boundaries

```text
controller-level reset != power cycle for protection-state lifetime
```

```text
ordinary Write Protect != Write Protect Until Power Cycle
```

```text
Permanent Write Protect != the only state that survives a power cycle
```

The ordinary `Write Protect` state also survives power cycles in the bounded standard.

### Page-image check

The ratified PDF's page containing §5.21.1.29 / Figure 321 was visually inspected in this research pass and confirms the four named values and the statement that the Feature is not saveable while post-reset/power-cycle value is determined by prior namespace write-protection state except for `Write Protect Until Power Cycle`.

Screenshot retrieval for the later §8.19 pages was unreliable in the browser cache, so no claim in this record depends on figure layout or graphics that were not also available in parsed normative text.

---

## Evidence C — Feature saveability is not authority-state persistence

### C1. Base Specification 1.4 §5.21.1.29

`Namespace Write Protection Config` is Feature Identifier `84h`.

The section says the Feature is **not saveable**. It immediately states, however, that after a power cycle or Controller Level Reset the Feature value is determined by the namespace's protection state before that event, except for `Write Protect Until Power Cycle`.

This makes an unusually clean terminology trap visible.

### Supported boundary

```text
Feature Identifier not saveable != namespace write-protection state volatile
```

A generic controller-feature persistence attribute and the lifetime of the controlled namespace state are different relations.

---

## Evidence D — transition into protection includes durability closure

### D1. Base Specification 1.4 §5.21.1.29

The standard requires that when Set Features changes the namespace into a write-protected state, the controller commit **all volatile write-cache data and metadata associated with the specified namespace to nonvolatile media as part of transitioning**.

### Supported claims

```text
write-protection transition != policy-bit change only
```

```text
future mutation prohibition can be composed with a volatile-to-nonvolatile durability closure
```

### Important limit

The standard does not disclose:

- the number of internal NAND programs;
- firmware-journal format;
- capacitor use;
- physical cache topology;
- crash-atomic implementation sequence;
- whether internal media relocation later occurs.

Therefore the evidence supports an **interface ordering/closure relation**, not a controller microarchitecture reconstruction.

---

## Evidence E — command interactions after protection

### E1. Base Specification 1.4 §8.19.1.1

The command-interaction table permits reads and specified nonmodifying operations and requires commands to fail if the specified action attempts to modify the medium of a write-protected namespace.

The rule is not confined to commands whose NSID literally equals the protected namespace. A broader-scope command must still fail when its action would modify the protected namespace.

The section also states that `Flush` completes successfully with **no effect** on a write-protected namespace because the relevant volatile write-cache data and metadata were written to nonvolatile media during the transition into write protection.

### Supported boundaries

```text
write protected != unreadable
```

```text
write protected != nonexistent / detached
```

```text
successful Flush after protection != newly performed cache drain
```

```text
write protection != sanitization
```

Format/Sanitize-style medium-modifying authority is constrained rather than performed by the write-protection state.

---

## Evidence F — protection state and media-health state are different

### F1. Base Specification 1.4 §8.19.1

The standard states that the controller shall not set the Critical Warning read-only condition merely because the media became read-only as a result of a namespace write-protection state transition or autonomous protection-state transition such as power cycle.

### Supported boundary

```text
intentional/protocol write protection != media-health read-only warning
```

This matters for retention analysis because an identical high-level observation — writes rejected — can arise from policy/authority state or from device health failure. Those failure meanings must not be merged.

---

## Evidence G — capability, authentication, and attachment

### G1. Capability reporting

§8.19 ties support to the Namespace Write Protection Capabilities (`NWPC`) field in Identify Controller.

The optional feature therefore has a capability layer distinct from the state itself.

### G2. Authentication control for stronger transitions

The `Write Protect Until Power Cycle` and `Permanent Write Protect` transitions are subject to `Namespace Write Protection Authentication Control` in the RPMB Device Configuration Block.

This supports:

```text
state exists != every transition into that state is presently authorized
```

It does not establish that ordinary data reads/writes are encrypted or authenticated by this mechanism.

### G3. Enforcement across attached controllers

§8.19.1 requires the namespace's write-protection state to be enforced by every controller to which that namespace is attached if the subsystem exposes the capability.

Supported boundary:

```text
multi-controller namespace attachment != independent write-protection state per access path
```

---

## Evidence H — 1996 SCSI/SSC prior-art floor

### H1. X3T10/96-179r0 identity

The document is dated **10 May 1996**, addressed to the X3T10 Committee (SCSI), and titled `Additional Write Protection functions for SSC`.

Its opening says the SSC working group discussed three additional functions:

- `Associated Write Protect`;
- `Persistent Write Protect`;
- `Permanent Write Protect`.

It also proposes distinct write-protect-related ASC/ASCQ values.

### H2. Persistence across volume mounts

The attached text describes:

- associated write protection for the currently mounted volume;
- persistent write protection of a volume across mounts;
- permanent write protection of a volume across mounts.

For `Persistent Write Protect`, the draft text distinguishes saving device-server mode pages from retaining the persistent write-protection indication for a volume on the **medium**.

For `Permanent Write Protect`, the draft says the volume is permanently write protected while recorded information remains and defines a one-way protection relation in the proposed command behavior.

### Supported novelty guardrail

```text
2019 NVMe Namespace Write Protection
    !=
invention of persistent/permanent software-controlled write protection
```

### Status limit

`96-179r0` is a **committee proposal**, not evidence that every proposed clause became a final SSC standard or was deployed in a named tape product exactly as written.

The proposal is used only as an earlier public mechanism/vocabulary floor.

---

## Evidence I — prior art is not genealogy

The 1996 SSC and 2019 NVMe mechanisms differ materially.

### 1996 bounded SSC proposal

- tape-volume/device-server setting;
- persistent/permanent protection across mounts;
- proposed indication recorded on the medium;
- SCSI mode-page / sense-code environment.

### NVMe 1.4

- namespace/controller capability;
- four reset/power-cycle-defined states;
- Set/Get Features interface;
- stronger-transition authorization through RPMB configuration;
- cross-controller enforcement for shared namespace attachment;
- mandatory volatile-cache-to-nonvolatile closure on transition.

### Supported conclusion

```text
earlier related mechanism + shared words
    !=
proven SSC -> NVMe implementation genealogy
```

A full standards genealogy belongs in `computing-archaeology` if later evidence establishes it.

---

## Cross-case evidence discipline

### Case 20 — NVMe Flush/FUA

Historical identity: same protocol family, but different feature question.

Functional comparison:

```text
media-persistence closure != future mutation authority
```

Case 114 is useful because the write-protection transition deliberately composes those relations: volatile namespace state is first committed, then later medium modification is prohibited.

No claim is made that write protection is a new kind of Flush.

### Case 110 — S3 Object Lock

Functional analogy only.

S3 Object Lock exposes version-scoped Governance/Compliance retention, retain-until timestamps, legal holds, and delete-marker/version-currentness interactions. NVMe 1.4 exposes namespace-scoped protection states whose lifetime is specified across power cycles/resets.

```text
version-scoped timed/held service WORM
    !=
namespace-scoped controller write-protection state
```

The comparison is about retained mutation authority, not historical descent or implementation identity.

### Case 84 — ZNS Reset / sanitization boundary

Functional comparison:

```text
preventing mutation != performing logical deallocation != physical sanitization
```

Write protection blocks modifying authority; it does not itself erase or sanitize existing data.

---

## Claim ledger

| Claim | Label | Strength | Evidence |
| --- | --- | --- | --- |
| Namespace Write Protect is new in NVMe 1.4 | `H/P` | strong | official revision-1.4 changes page |
| feature is per namespace | `H/P` | strong | changes page + 1.4 §8.19 |
| four protection states have different reset/power-cycle lifetimes | `H/P` | strong | 1.4 §8.19 / Figure 488 |
| Feature 84h is not saveable while namespace protection may persist | `H/P` | strong | 1.4 §5.21.1.29 |
| entering a protected state commits namespace volatile cache state to NVM | `H/P` | strong | 1.4 §5.21.1.29 |
| reads remain allowed; modifying actions are blocked | `H/P` | strong | 1.4 §8.19.1.1 |
| write-protected Flush performs no new work | `H/P` | strong | 1.4 §8.19.1.1 |
| deliberate write protection is distinct from media-health read-only warning | `H/P` | strong | 1.4 §8.19.1 |
| all attached controllers enforce one namespace protection state | `H/P` | strong | 1.4 §8.19.1 |
| 1996 T10 proposal provides persistent/permanent software write-protect prior art | `H/P` | strong as proposal-history floor | X3T10/96-179r0 |
| 1996 SSC directly caused NVMe 1.4 design | `X` | unsupported | no genealogy source inspected |
| `Permanent Write Protect` means physical NAND cannot change | `X` | unsupported | protocol contract does not expose physical medium invariance |
| namespace write protection improves NAND charge-retention time | `X` | unsupported | no physical-retention mechanism in inspected feature contract |
| write protection is equivalent to S3 Object Lock | `X/A` | rejected as identity; useful analogy only | unlike scope/time/version/authority semantics |

---

## Evidence-quality notes

1. **Primary standards evidence dominates.** NVM Express and X3T10/T10 materials carry the mechanism claims; current explanatory pages are only corroborative.
2. **Original 2019 wording is preferred.** Revision 1.4c is useful as a later continuity/search aid but is not silently substituted where exact 2019 historical wording is at issue.
3. **PDF visual inspection is bounded.** The Feature-84h page of the 2019 ratified PDF was visually checked. Some other screenshot retrievals failed at the browser-cache layer, so this record makes no diagram-layout claim dependent on those unavailable page images.
4. **Proposal status remains proposal status.** X3T10/96-179r0 is not upgraded into a final-standard/deployment claim.
5. **No hidden implementation is invented.** The standards establish host/controller-visible obligations, not the firmware journal, NAND layout, or crash-atomic implementation.

---

## Remaining evidence gaps

- retrieve and inspect TP4005c directly and establish its dates/authorship/revision history;
- identify whether and how the write-protection proposal moved through pre-ratification NVMe 1.4 drafts;
- trace final SSC standard adoption of the 1996 persistent/permanent proposal without assuming it;
- find named NVMe controller/device support and conformance evidence;
- test reset vs power-cycle state persistence on hardware;
- test crash/power-loss behavior during the transition that drains volatile namespace state;
- inspect RPMB authentication-control provisioning and recovery in named products;
- establish whether virtualization or NVMe-oF deployments alter any host-visible authority boundary;
- investigate physical/forensic behavior under `Permanent Write Protect` without conflating host command refusal with immutable media.

These gaps leave the bounded 2019 contract conclusion intact.