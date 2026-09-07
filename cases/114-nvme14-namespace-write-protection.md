# NVM Express 1.4 Namespace Write Protection: Mutation Authority, State Lifetime, and Transition Durability

## Status

**`grounded`** for the bounded NVMe 1.4 namespace-write-protection contract described below.

Grounding record: [`../evidence/114-nvme-1996-2019-namespace-write-protection-grounding.md`](../evidence/114-nvme-1996-2019-namespace-write-protection-grounding.md).

## Scope

- **Object / regime:** the optional `Namespace Write Protection` capability introduced in the NVM Express Base Specification revision 1.4, ratified in 2019.
- **Primary mechanism source:** NVM Express Base Specification Revision 1.4, especially `Namespace Write Protection Config` (Feature Identifier `84h`) and §8.19.
- **Public change record:** NVM Express's `Changes in NVMe Revision 1.4`, which identifies Namespace Write Protect as a new optional revision-1.4 feature and links it to Technical Proposal 4005c.
- **Prior-art floor:** X3T10/96-179r0, 10 May 1996, an SSC proposal for software-controlled associated, persistent, and permanent write protection on tape volumes.
- **Research question:** what exactly persists when an NVMe namespace becomes write protected, how does that authority state survive resets or power cycles, and why is write protection neither the same as payload nonvolatility nor the same as a physically write-once medium?

This case is **not** a complete NVMe security history, RPMB provisioning study, TCG Opal analysis, NAND-retention study, implementation audit of a named controller, or proof of SCSI-to-NVMe genealogy.

The bounded retention claim is:

> **NVMe 1.4 adds retained mutation-authority state to a namespace. Entering a protected state may itself require a durability-closing transfer of that namespace's volatile write-cache data and metadata to nonvolatile media; after the transition, the namespace remains readable while medium-modifying commands are rejected according to the selected protection state. The lifetime of the authority state is specified separately from the physical retention lifetime of the payload.**

`mutation authority`, `authority lifetime`, and `transition durability closure` are project engineering terms, not NVM Express historical vocabulary.

---

## Historical vocabulary

The inspected NVMe sources directly use:

- `Namespace Write Protection`;
- `Namespace Write Protection Config`;
- `Namespace Write Protection Capabilities (NWPC)`;
- `No Write Protect`;
- `Write Protect`;
- `Write Protect Until Power Cycle`;
- `Permanent Write Protect`;
- `Namespace Write Protection Authentication Control`;
- `Feature Not Changeable`;
- `volatile write cache`;
- `non-volatile media`.

The following are project terms used only for comparison:

- `mutation authority`;
- `authority lifetime`;
- `transition durability closure`;
- `protocol-level immutability`;
- `payload-retention physics`.

---

## Historical record

### H/P — Namespace Write Protect is a revision-1.4 optional feature

NVM Express's official `Changes in NVMe Revision 1.4` page lists `Namespace Write Protect (optional)` under new features. It describes the feature as controlling write protection on a per-namespace basis and says it may be used to prevent modification of a specified namespace. The page points to revision-1.4 §§5.14, 5.15, 5.21, 8.10, and 8.19 and to Technical Proposal 4005c.

This establishes a public revision boundary. It does **not** establish that NVMe invented software write protection, persistent protection, permanent protection, WORM storage, or any particular underlying hardware mechanism.

Primary source: NVM Express, [`Changes in NVMe Revision 1.4`](https://nvmexpress.org/changes-in-nvme-revision-1-4/).

### H/P — the namespace has four distinct write-protection states

NVMe 1.4 §8.19 defines four states:

1. `No Write Protect`;
2. `Write Protect`;
3. `Write Protect Until Power Cycle`;
4. `Permanent Write Protect`.

The initial state at namespace creation is `No Write Protect`.

The states deliberately have different lifetimes. `No Write Protect`, ordinary `Write Protect`, and `Permanent Write Protect` persist across both power cycles and NVMe Controller Level Resets. `Write Protect Until Power Cycle` survives Controller Level Reset but transitions to `No Write Protect` at the next power cycle.

Therefore:

> **controller reset ≠ power cycle for namespace-protection lifetime**.

and:

> **one write-protected state ≠ one universal persistence regime**.

Primary source: NVM Express Base Specification Revision 1.4, §8.19, Figure 488.

### H/P — `Feature not saveable` does not mean the namespace state is volatile

Feature Identifier `84h` is explicitly defined as **not saveable**. Yet the same section states that the feature value after a power cycle or Controller Level Reset is determined by the namespace's previous write-protection state, except for `Write Protect Until Power Cycle`.

The specification therefore forces a useful semantic distinction:

> **Set-Features saveability ≠ persistence of the state represented by that feature**.

A host cannot infer that the protection relation disappears merely because the Feature Identifier itself is not saveable through the generic Feature-save mechanism.

Primary source: NVM Express Base Specification Revision 1.4, §5.21.1.29.

### H/P — the stronger state transitions have separate authentication control

The transitions into `Write Protect Until Power Cycle` and `Permanent Write Protect` are subject to the `Namespace Write Protection Authentication Control` mechanism. NVMe 1.4 ties that control to the RPMB Device Configuration Block.

The specification therefore distinguishes at least three things:

- whether a protection state exists;
- whether the controller supports a given state;
- whether a requested transition into one of the stronger states is currently authorized.

This is not evidence that all NVMe write protection is cryptographic, nor that protection of the namespace payload is implemented by encrypting it.

### H/P — protection is a namespace relation shared across attached controllers

NVMe 1.4 states that if any controller in the NVM subsystem supports Namespace Write Protection, the namespace's write-protection state shall be enforced by any controller to which that namespace is attached.

Thus:

> **namespace attachment to multiple controllers ≠ independent per-controller mutation authority**.

The authoritative relation belongs to the namespace contract across the attached-controller access paths in the bounded specification.

### H/P — entering write protection closes outstanding volatile namespace state first

The strongest retention-specific mechanism in the case appears in §5.21.1.29. If Set Features changes a namespace into a write-protected state, the controller shall commit **all volatile write-cache data and metadata associated with that namespace to nonvolatile media as part of the transition**.

That means the transition is not merely a policy-bit flip over whatever happened to be durably stored already.

The specification establishes:

> **entering write protection ≠ mutation-authority change only**;

and:

> **protection-state transition can require durability work before the protected state is established**.

This requirement is especially important beside Case 20's Flush/FUA distinction. Here a future-mutation barrier and a durability boundary are composed in one transition, but they remain conceptually distinct.

### H/P — reads remain possible while modifying commands are rejected

NVMe 1.4 §8.19.1.1 defines command interactions for a write-protected namespace. Read and other nonmodifying operations remain allowed, while commands/actions that attempt to modify the namespace medium are rejected. The rule also reaches commands whose command-level namespace identifier may be broader than one namespace if the action would modify a protected namespace.

The section also says a `Flush` against a protected namespace completes successfully with no effect, because the relevant volatile cache data and metadata were already written to nonvolatile media during the transition into write protection.

Therefore:

> **write protected ≠ unreadable**;

> **write protected ≠ detached or nonexistent**;

> **successful post-transition Flush ≠ evidence of newly performed persistence work**.

### H/P — deliberate write protection is not the media-health read-only warning

NVMe 1.4 §8.19.1 says the controller shall not set the SMART/Health `Critical Warning` read-only condition merely because the read-only condition resulted from a namespace write-protection state transition or its autonomous transition at power cycle.

So:

> **administratively/protocol write protected ≠ media-health read-only failure state**.

The same host-visible inability to modify data can therefore arise from importantly different causes.

---

## Retained state decomposition

At least eight distinct state classes should remain visible.

1. **Namespace payload** — the logical blocks and metadata represented by the namespace.
2. **Physical nonvolatile embodiment** — whatever device media currently embodies those logical blocks; the specification does not require one physical layout.
3. **Volatile write-cache state** — pending data/metadata that may need to cross into nonvolatile media before write protection is established.
4. **Namespace identity / attachment relation** — which namespace the feature applies to and which controllers can access it.
5. **Write-protection state** — one of the four states defined in §8.19.
6. **Capability state** — which levels of Namespace Write Protection the controller supports.
7. **Authentication-control state** — whether transitions into the stronger states are permitted through the bounded RPMB control.
8. **Media-health state** — separately reported reliability/read-only information that must not be conflated with deliberate write protection.

The public specification exposes these relations through commands and data structures. It does not establish the exact NAND pages, firmware journals, capacitor-backed buffers, or controller-internal records used to implement them.

---

## Engineering reconstruction

### E — mutation authority can persist independently of payload retention physics

A NAND payload can be physically nonvolatile while the namespace remains writable, or the same payload can be made protocol-level read-only by retained namespace state.

Conversely, making the namespace permanently write protected through this interface does not increase cell charge-retention time, improve ECC margin, refresh weak NAND cells, or prove that physical blocks can never move internally.

Therefore:

> **payload nonvolatility ≠ mutation prohibition**;

and:

> **mutation prohibition ≠ stronger physical retention**.

### E — protection entry is a two-part state transition

A useful bounded reconstruction is:

```text
writable namespace
+ possibly pending volatile namespace data/metadata
    ↓ Set Features / permitted transition
commit namespace volatile state to nonvolatile media
    ↓
write-protected namespace
    ↓
reads remain admissible; medium-modifying commands are rejected
```

The specification does not expose whether the cache commit is implemented as one physical transaction or many. The reconstruction only preserves the normative ordering relation required by the interface.

### E — protection-state persistence and generic Feature saveability are different state machines

Feature Identifier `84h` being `not saveable` describes how the generic Set/Get Features persistence mechanism applies. Section 8.19 separately defines how the namespace's protection state behaves across reset and power-cycle events.

This is a reusable warning for controller protocols:

> **control-register persistence vocabulary ≠ lifetime of the controlled object state**.

### E — `Permanent` is scoped to the protocol state, not to every lower layer

`Permanent Write Protect` means the namespace remains in the permanent protection state under the NVMe state machine. It does not establish:

- a physically write-once NAND cell;
- a WORM optical medium;
- indefinite charge retention;
- immutable controller firmware;
- an audit/compliance regime equivalent to S3 Object Lock;
- secure sanitization after namespace retirement;
- immunity to hardware replacement, destructive laboratory intervention, or lower-layer failure.

The project therefore uses `protocol-level permanence` only as a bounded engineering description.

---

## Prior art boundary

### H/P — persistent/permanent software-controlled write-protection vocabulary predates NVMe 1.4

X3T10/96-179r0, dated **10 May 1996**, is a proposal to the X3T10 SCSI committee titled `Additional Write Protection functions for SSC`. It records discussion of three added functions named `Associated Write Protect`, `Persistent Write Protect`, and `Permanent Write Protect`.

The attached proposed SSC text describes persistent write protection of a volume across mounts and permanent write protection of a volume across mounts. It also distinguishes saving a device-server mode page from recording the persistent/permanent protection indication for a volume on the medium.

That evidence is sufficient for this bounded guardrail:

> **NVMe 1.4 Namespace Write Protection ≠ invention of persistent/permanent software-controlled write protection**.

Primary source: X3T10, [`96-179r0 — Additional Write Protection functions for SSC`](https://www.t10.org/ftp/t10/document.96/96-179r0.pdf), 10 May 1996.

### H/P/A — the 1996 SSC proposal is a prior-art floor, not proven genealogy

The mechanisms are not identical.

- The 1996 SSC proposal is tape-volume/device-server specific and proposes recording persistent/permanent volume state on the medium.
- NVMe 1.4 defines a namespace/controller capability and state machine, with stronger transition authorization tied to RPMB configuration.

Chronology plus shared vocabulary does not prove that one implementation descended from the other.

> **earlier SCSI/SSC write-protection mechanism ≠ demonstrated SCSI→NVMe implementation genealogy**.

---

## Cross-case comparisons — functional, not genealogical

### A — Case 20: NVMe 1.0 Flush / FUA

Case 20 separates command completion from media persistence and shows how Flush/FUA close particular durability relations.

Case 114 adds a different relation: entering a protected state requires namespace-associated volatile write-cache data and metadata to be committed before the future-mutation prohibition is established.

Thus:

> **durability closure ≠ future mutation prohibition**,

although NVMe 1.4 deliberately composes them at this transition boundary.

### A — Case 110: Amazon S3 Object Lock

Both cases expose retained control state that can prevent later mutation, but the scope and semantics differ sharply.

- S3 Object Lock is version-scoped and adds Governance/Compliance retention, retain-until time, legal hold, and version-currentness interactions.
- NVMe Namespace Write Protection applies at namespace scope and defines reset/power-cycle/permanent state lifetimes rather than versioned retain-until/legal-hold semantics.

Therefore:

> **version-scoped service WORM ≠ namespace-wide controller write protection**.

No AWS↔NVMe genealogy is implied.

### A — Case 84: NVMe ZNS Reset and sanitization boundary

Case 84 shows that logical reuse/deallocation does not itself prove physical sanitization. Case 114 supplies the complementary authority boundary: while a namespace is protected, medium-modifying operations are rejected, but this does not turn write protection itself into a sanitization mechanism.

> **preventing mutation ≠ performing erasure**.

---

## Failure and forgetting boundaries

Distinct failures or operator mistakes include:

- assuming Namespace Write Protection exists on a controller that does not implement the optional capability;
- treating `not saveable` as proof that protection disappears after reset;
- expecting `Write Protect Until Power Cycle` to disappear after a Controller Level Reset rather than a power cycle;
- expecting ordinary `Write Protect` to disappear on the next power cycle even though it persists;
- attempting to change an already `Permanent Write Protect` namespace through the same Feature state machine;
- assuming a broad-scope Format/Sanitize path can modify a namespace despite its protection state;
- confusing deliberate write protection with media-health read-only degradation;
- assuming a successful Flush on a protected namespace performs fresh durability work;
- equating permanent protocol write protection with physical WORM media or indefinite NAND retention;
- losing access to data for reasons unrelated to write authority: controller failure, media failure, lost mapping state, or incompatible software.

None of these should be collapsed into one generic category called `data retention failure`.

---

## Historical record / reconstruction / analogy ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| Namespace Write Protect is a new optional NVMe 1.4 feature | `H/P` | official NVM Express revision-1.4 changes page |
| NVMe 1.4 defines four namespace write-protection states with different reset/power-cycle lifetimes | `H/P` | Base Specification 1.4 §8.19 |
| Feature Identifier 84h is not saveable while most protection states still persist | `H/P` | Base Specification 1.4 §5.21.1.29 + §8.19 |
| entering write protection commits namespace volatile cache data/metadata to nonvolatile media | `H/P` | Base Specification 1.4 §5.21.1.29 |
| reads remain allowed while medium-modifying commands are rejected | `H/P` | Base Specification 1.4 §8.19.1.1 |
| deliberate namespace protection is not the SMART media-read-only warning | `H/P` | Base Specification 1.4 §8.19.1 |
| permanent namespace write protection is a physically immutable NAND medium | `X` | the interface contract does not establish this |
| the 1996 SSC proposal establishes persistent/permanent software write-protection prior art | `H/P` | X3T10/96-179r0 |
| the 1996 proposal directly evolved into NVMe 1.4 | `X` | chronology/shared vocabulary do not prove genealogy |
| S3 Object Lock and NVMe Namespace Write Protection are the same mechanism | `X/A` | functional comparison only; scope, time, version, and authority models differ |

---

## Philosophical interpretation — bounded

Case 114 adds one narrow pressure to the project's vocabulary of retention:

> **a technically retained state can determine not only what may be recovered later, but also what may no longer be deliberately changed later.**

That is a statement about retained **authority/control state**, not a claim that prohibition is itself physical preservation. A namespace can retain a prohibition on modification while its NAND cells still age, its controller can still fail, and its internal physical embodiment may still be opaque to the host.

The case therefore disciplines any philosophical use of `immutability`: before calling a technical object immutable, specify **which actor, interface, operation, time horizon, and failure model** the prohibition covers.

---

## Related repositories

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Namespace Write Protect` found no dedicated history to reuse in this round. A broader history of SCSI/ATA/NVMe write-protection mechanisms, proposal genealogy, controller implementation, and security provisioning belongs there if developed. This repository keeps the narrower retention-authority comparison.

Related cases here:

- [Case 20 — NVM Express 1.0 Volatile Write Cache and FUA](20-nvme10-fua-flush-persistence-ordering.md)
- [Case 75 — NVM Express 1.3d Reservations](75-nvme13-reservation-persistence-ptpl.md)
- [Case 84 — NVMe Zoned Namespace Zone Reset](84-nvme-zns-zone-reset-logical-reuse.md)
- [Case 110 — Amazon S3 Object Lock](110-amazon-s3-object-lock-version-worm-retention.md)

---

## Remaining uncertainty / next work

Still open:

- direct archival inspection and proposal genealogy for TP4005c;
- revision-by-revision changes after the original 1.4 state machine;
- exact RPMB provisioning/authentication workflow in named products;
- named-controller conformance and reset/power-cycle fault tests;
- firmware crash atomicity of the transition that commits volatile cache state and changes protection state;
- behavior across controller replacement, subsystem reset classes, virtualization, and NVMe-oF deployments;
- full SCSI write-protect genealogy beyond the bounded 1996 SSC proposal;
- physical-media and forensic behavior after a namespace becomes permanently write protected.

These gaps do not block the bounded conclusion that NVMe 1.4 separates payload retention, transition durability, mutation authority, and authority-state lifetime.