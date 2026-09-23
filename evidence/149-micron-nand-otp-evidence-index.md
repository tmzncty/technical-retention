# Case 149 Evidence Index — Micron NAND OTP irreversible authority

This file is the evidence navigation for [`../cases/149-micron-nand-otp-data-protect-irreversible-authority.md`](../cases/149-micron-nand-otp-data-protect-irreversible-authority.md).

**Case maturity:** `grounded`

No evidence item below independently justifies a promotion. The index exists to keep three different questions from collapsing into one:

```text
what irreversible authority transition exists?
    != how the command interface representing it evolved
    != what physical / target scope that authority governs
```

---

## Canonical case

[`../cases/149-micron-nand-otp-data-protect-irreversible-authority.md`](../cases/149-micron-nand-otp-data-protect-irreversible-authority.md)

Use the canonical case for the overall claim:

- Micron NAND exposes a dedicated OTP area;
- OTP programming and OTP protection are distinct transitions;
- unprotected OTP is already non-erasable;
- successful OTP protection removes future program authority;
- protection is irreversible in the documented interface;
- read access remains available;
- command completion/status matters;
- mechanism speculation, security properties, and later interface forms must remain separate from the historical record.

---

# Evidence chain 1 — irreversible OTP authority transition

## E149-1 — Micron 2004–2006 OTP DATA PROTECT grounding

[`149-micron-2004-2006-nand-otp-data-protect-grounding.md`](149-micron-2004-2006-nand-otp-data-protect-grounding.md)

**Question:** what exactly changes when Micron's OTP DATA PROTECT operation succeeds?

**Pinned result:**

```text
OTP erased
    -> OTP programmed
    -> OTP protection succeeds
    -> further programming disallowed

read access remains
```

The important distinctions are:

```text
programmed
    != protected

non-erasable payload
    != future programming authority removed

command issued
    != operation successfully completed
```

The grounding package also keeps the 2004-filed / 2006-published Micron patent in its proper role: mechanism evidence and chronology context, not proof that a particular datasheet product instantiated every patented structure exactly as drawn.

It likewise preserves earlier AMD/Fujitsu prior art so Case 149 does not overclaim invention priority.

**Do not infer:** exact latch topology, tamper resistance, confidentiality, sanitization, or post-protect behavior under every undocumented reset/power condition.

---

# Evidence chain 2 — vendor command interface versus standardized feature space

## E149-2 — ONFI 1.0/2.0 and later Micron OTP interface migration

[`149-onfi10-20-vendor-feature-space-otp-interface-deepening.md`](149-onfi10-20-vendor-feature-space-otp-interface-deepening.md)

**Question:** does the later ONFI-era control surface mean that the earlier dedicated Micron OTP command sequence did not exist or was not real?

**Pinned result:** no. The evidence needs a chronology, not a flattened “NAND OTP command” abstraction.

The older Micron family uses dedicated OTP command opcodes. Later ONFI-era Micron devices use a feature-controlled OTP operation mode and ordinary read/program operations against the OTP area.

Therefore:

```text
same broad capability
    can survive interface migration

older vendor-specific command encoding
    != later standardized / feature-space control encoding
```

This chain is about **representation and interface genealogy**, not about the physical location of the retained protection state.

**Do not infer:** that ONFI standardized every earlier Micron vendor command, that the later feature address existed in the 2006 device, or that all vendors converged at the same date.

---

# Evidence chain 3 — stacked package, target selection, and protection-authority scope

## E149-3 — Micron 2006–2009 stacked-target OTP authority-scope boundary

[`149-micron-2006-2009-stacked-target-otp-authority-scope-deepening.md`](149-micron-2006-2009-stacked-target-otp-authority-scope-deepening.md)

**Question:** if a physical NAND package contains multiple selectable internal sections or targets, is one successful OTP protect result enough to prove a package-wide immutable state?

**2006 historical floor:** the exact Rev. D 12/06 8Gb Micron package is a stacked multi-die device with two separately selected 4Gb sections. CE# and CE2# are distinct sub-package command-selection interfaces, and the document states that the operations described for CE# also apply to CE2#.

Thus:

```text
physical package identity
    != command-selection scope
```

But the 2006 text inspected in this pass does not explicitly document whether the irreversible OTP-protection state is independently instantiated per CE#, per die, per array, or in some other topology.

**2009 later same-vendor witness:** a later Micron high-density NAND family uses an explicit target model and states that each target has an OTP area. OTP operation mode and protection are expressed at the selected target.

That supports a direct later distinction:

```text
package identity
    != target identity
    != target-local OTP area identity
```

The chronology guardrail is essential:

```text
2009 explicit target-scoped OTP
    != proof that the 2006 product used identical internal lock topology
```

The engineering consequence is nevertheless clear:

```text
package-wide "locked" claim
    requires evidence covering the documented protection / selection scope
```

A single successful protection result must not silently be widened from a selected operational domain to the whole package unless the datasheet defines the protection scope that way.

**Do not infer:** one lock latch per CE#, one OTP area per die in the 2006 part, or package-global protection from an undocumented topology.

---

# Unified state model

The Case 149 package now distinguishes at least five state classes or boundaries:

```text
OTP payload state
    |
    +--> erased / partially programmed / programmed bits
    |
    +--> non-erasability of the OTP medium

OTP mutation-authority state
    |
    +--> further programming still legal
    +--> further programming irreversibly disabled

command completion state
    |
    +--> issued / busy / success / failure

interface representation
    |
    +--> dedicated vendor OTP commands
    +--> later feature-controlled OTP mode

scope identity
    |
    +--> package
    +--> CE-selected section
    +--> target
    +--> LUN/die where explicitly documented
```

These axes interact, but they are not synonyms.

In particular:

```text
payload retained
    != mutation authority retained

mutation authority removed
    != package-global removal proved

same capability
    != same command encoding

same physical package
    != one indivisible authority domain
```

---

# Historical record versus engineering reconstruction

The index should be read with the repository's standard evidence discipline.

## Historical record

Historical claims require direct source support, including:

- Rev. D 12/06 Micron OTP commands and their documented irreversibility;
- the 8Gb package's multi-die / dual-CE organization;
- later Micron target organization and target-scoped OTP wording;
- ONFI/vendor feature-space chronology where directly sourced.

## Engineering reconstruction

The following are repository analyses, not quotations from Micron:

- provisioning logs should preserve selector/target provenance where authority scope can be narrower than package identity;
- package-wide immutability is a stronger claim than one successful target/section protect result;
- validation should test every documented authority domain relevant to a package-level claim;
- retained control state must be described by both persistence and scope.

## Functional analogy

Comparisons to NVMe namespace write protection, S3 Object Lock, flash mapping, or other cases are structural comparisons only unless a source establishes genealogy.

## Philosophical interpretation

Statements such as “authority belongs to a relation rather than merely an enclosure” are interpretive abstractions from the engineering structure. They are not claims about Micron's historical design intent.

---

# Cross-case navigation

## Case 114 — NVMe namespace write protection

[`../cases/114-nvme14-namespace-write-protection.md`](../cases/114-nvme14-namespace-write-protection.md)

Useful functional comparison:

```text
whole device identity
    != lower-level mutation-authority scope
```

No genealogy claim.

## Case 110 — Amazon S3 Object Lock

[`../cases/110-amazon-s3-object-lock-version-worm-retention.md`](../cases/110-amazon-s3-object-lock-version-worm-retention.md)

Useful weaker comparison: retained mutation authority and retention policy attach to identified logical scopes rather than to an undifferentiated physical storage object.

No genealogy claim.

## Case 78 — Micron NAND bad-block marker management

[`../cases/78-micron-nand-bad-block-marker-management.md`](../cases/78-micron-nand-bad-block-marker-management.md)

Related technology family but a different control-state problem. Bad-block markers are retained evidence about media usability; OTP protection is retained mutation authority. Do not merge the two merely because both reside in NAND.

---

# What is now grounded strongly enough to reuse

Within the limits of mirrored-primary custody and the explicit non-claims in each evidence note, downstream synthesis may safely reuse these propositions:

1. Micron's documented OTP area is non-erasable even before protection.
2. OTP programming and irreversible OTP protection are separate operations.
3. A successful protection operation removes further programming authority while read access remains.
4. Completion/status is part of the protection claim; command issue alone is insufficient.
5. The older dedicated-command interface and later feature-controlled interface should not be collapsed into one timeless encoding.
6. A physical NAND package can contain multiple separately selected internal sections/targets.
7. Later Micron documentation explicitly gives each target an OTP area.
8. Package identity alone is therefore not a defensible universal proxy for OTP authority scope.
9. The exact 2006 per-CE/per-die protection-state topology remains open and must not be invented.

Case 149 remains `grounded`.

---

# Priority evidence debt

## 1. Origin-hosted/archive-origin Rev. D 12/06 datasheet

The exact document identity is known, but the currently inspected copies are third-party mirrors. Recover a Micron-origin or strong archival-origin copy if possible.

## 2. Explicit 2006 protection-scope statement

Find a period datasheet, application note, erratum, characterization document, or other primary Micron source that directly states whether OTP protection on the Rev. D family is scoped per CE#, per die, per array, or package-wide.

This is the highest-value documentary follow-up to E149-3.

## 3. Hardware protect/reset/power-cycle validation

On an exact supported stacked part, observe status and prohibited-program behavior across every documented selector before and after reset/full power-cycle.

Target distinction:

```text
interface says protection is irreversible
    != hardware behavior across every reset/power event empirically observed
```

## 4. Earlier target-scoped wording

Push the explicit “each target has an OTP area” chronology earlier than the preserved 2009 witness if primary material permits.

If this expands into a general history of CE#, targets, LUNs, stacked NAND packaging, and ONFI terminology, move that broad genealogy to `tmzncty/computing-archaeology` and link back rather than duplicating it here.

## 5. Part-number / die-generation revision matrix

Track which exact Micron part numbers, package stacks, die revisions, and datasheet revisions carry each OTP control model. Do not assume one family page applies identically across every suffix and generation.

---

# Related-repository boundary

A fresh search in `tmzncty/computing-archaeology` did not find an existing Micron NAND OTP / exact-part technical-history module suitable for reuse in this pass.

`technical-retention` should therefore keep the narrow retention evidence above. A future broad history of multi-die NAND target terminology belongs in `computing-archaeology`, with this index linking to it once such a module exists.

---

# Bottom line

Case 149 now has three distinct evidence chains:

```text
irreversible OTP authority transition
    +
command-interface migration
    +
physical-package / target authority scope
```

Together they support a more precise retention statement:

> an irreversible control state is not adequately characterized only by how long it survives; its command representation and the exact object over which it governs future mutation must also be identified.
