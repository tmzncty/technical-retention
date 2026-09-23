# Case 149 Deepening — Micron stacked-package / target OTP authority scope (2006–2009)

## Purpose

This note deepens one narrow boundary in [Case 149](../cases/149-micron-nand-otp-data-protect-irreversible-authority.md):

> when a NAND package contains multiple selectable internal arrays or targets, what does a successful OTP protection operation actually authorize us to claim about the whole package?

The existing Case 149 package already establishes the more basic result: Micron exposed separate OTP program and irreversible OTP-protect operations, and a successful protect operation removes future programming authority while preserving read access. This note does **not** re-prove that result.

Instead, it asks a granularity question:

```text
physical package identity
    != command-selection scope
    != demonstrated OTP-protection authority scope
```

The historical record supports the first inequality directly for the 2006 stacked part. A later 2009 Micron family makes the target-level OTP scope explicit. The two records can be compared, but the later target model must not be silently back-projected into the earlier part.

**Evidence maturity:** deepening for an already `grounded` case. No maturity promotion is proposed here.

---

## Source ledger

### S1 — Micron 2Gb, 4Gb, 8Gb x8/x16 NAND Flash Memory, Rev. D 12/06

- Micron Technology, Inc.
- title: **2Gb, 4Gb, 8Gb: x8, x16 NAND Flash Memory**
- document identifiers printed in the preserved PDF: `PDF: 09005aef814b01a2 / Source: 09005aef814b01c7`
- revision: **Rev. D 12/06 EN**
- preserved third-party PDF mirrors inspected in this pass:
  - <https://www.unikeyic.com/media/datasheet/7f/f6/080e/7f/dd6508066ac9a0d8631c65de6f3f724e.pdf>
  - <https://chipsmall.ltd/uploadfiles/datasheet/pdf/2011/5/2011513163752570.pdf>

**Custody classification:** `H/P*` — primary Micron document content preserved on third-party hosts; not an origin-hosted Micron archival copy.

Relevant sections:

- organization / stacked-die configuration and CE#/R/B# structure;
- signal descriptions and CE2# behavior;
- command definitions;
- OTP DATA PROGRAM;
- OTP DATA PROTECT;
- OTP DATA READ;
- status register definitions.

### S2 — Micron high-density asynchronous/synchronous NAND, Rev. A 11/09

- Micron Technology, Inc.
- family represented by preserved 2009 material for 64Gb–512Gb asynchronous/synchronous NAND;
- revision: **Rev. A 11/09**; preserved copies carry a **Draft: 11/20/09** date;
- preserved PDF/searchable mirrors inspected in this pass include:
  - <https://datasheet4u.com/pdf/726091/29F64G08CBAAA.pdf>
  - <https://www.scribd.com/document/856599325/29F128G08CEAAA-Micron>

**Custody classification:** `H/P*` — primary Micron document content preserved on third-party hosts; no claim of origin-host custody.

Relevant sections:

- package / target organization;
- CE# / target selection;
- One-Time Programmable (OTP) Operations;
- OTP operation mode;
- PROGRAM OTP PAGE / PROTECT OTP AREA / READ OTP PAGE.

The 2009 material is used here as a **later same-vendor clarification witness**, not as evidence that the 2006 Rev. D device had identical internal protection-state topology.

### S3 — existing Case 149 evidence package

- [`149-micron-2004-2006-nand-otp-data-protect-grounding.md`](149-micron-2004-2006-nand-otp-data-protect-grounding.md)
- [`149-onfi10-20-vendor-feature-space-otp-interface-deepening.md`](149-onfi10-20-vendor-feature-space-otp-interface-deepening.md)

These already establish the irreversible-program-authority result and the later command-interface migration boundary. They are not duplicated below.

---

# 1. Historical record — the 2006 package is not one undifferentiated command-selection domain

## 1.1 The 8Gb package is a stacked multi-die device

The Rev. D 12/06 Micron family distinguishes physical density and die organization rather than treating the package as a single monolithic array.

For the 8Gb configuration, the datasheet describes a package composed from four 2Gb dies and presents it as two separate 4Gb arrays. Those two sections have independent chip-enable and ready/busy connections.

The important retention-specific point is not merely that there are four dies. It is that **the package exposes sub-package selection boundaries**.

A useful representation is:

```text
8Gb physical package
    |
    +--> 4Gb section selected by CE#
    |        +--> constituent die state
    |
    +--> 4Gb section selected by CE2#
             +--> constituent die state
```

The datasheet also states that the operations described for CE# apply to CE2# for the second section.

Therefore:

```text
same package
    != same command-selection domain
```

This conclusion is directly historical. It does not require reconstruction of undocumented internal latch topology.

---

## 1.2 CE# is part of the command acceptance boundary

The Rev. D signal description says that when CE# is asserted and the device is not busy, the selected NAND section accepts command, address, and data information. CE2# performs the corresponding function for the second section of the 8Gb configuration.

The OTP command timing diagrams likewise include CE# as part of the command interface.

Thus the historical record supports:

```text
OTP command issued to a package
    is still issued through a selected command interface
```

For the stacked 8Gb package, command traffic is not adequately described by package identity alone.

---

# 2. Historical record — OTP program and protect remain separate irreversible transitions

This section is intentionally brief because the canonical case and the original grounding note already cover the result in detail.

The Rev. D 12/06 device exposes:

```text
OTP DATA PROGRAM   A0h -> 10h
OTP DATA PROTECT   A5h -> 10h
OTP DATA READ      AFh -> 30h
```

The OTP area cannot be erased whether protected or unprotected. The protection operation has its own busy/completion interval and status check. After successful protection, no further programming of the OTP area is allowed and the area cannot be unprotected.

The same document exposes a status indication for whether OTP protection has been enabled.

So the already-grounded authority transition remains:

```text
OTP programmed
    != OTP protected

successful OTP protect
    -> future OTP programming authority removed
```

Nothing in the present slice changes that result.

---

# 3. The 2006 boundary — selection granularity is documented; protection-state topology is not

This is the central caution of the present deepening.

From S1 we can directly establish all of the following:

1. the 8Gb physical package contains multiple dies;
2. it exposes two separately selected 4Gb sections;
3. CE# and CE2# select those sections;
4. operations described for CE# also apply to CE2#;
5. OTP protection is an irreversible status-qualified command operation.

But those facts do **not** by themselves establish the exact implementation topology of the irreversible protection state.

In particular, S1 does not explicitly say:

- whether each CE-selected 4Gb section has an independently instantiated OTP-protect latch;
- whether two dies behind one CE share one protection state or have separate internal state;
- whether an OTP protect command accepted through one CE implicitly protects anything reachable through another CE;
- where the protection state is physically stored;
- how many physical nonvolatile control elements implement that state.

Therefore the strongest justified 2006 statement is:

```text
sub-package command-selection domains are documented

but

exact sub-package OTP-protection-state partitioning
    remains undocumented in the inspected Rev. D text
```

That distinction prevents a common evidence error: deriving internal authority scope solely from the package block diagram.

---

# 4. Historical record — 2009 Micron documentation makes target-scoped OTP explicit

The later 2009 high-density Micron family uses an explicit **target** model.

Its package diagrams distinguish multiple targets selected through separate CE# signals, with one or more logical units associated with a target depending on the organization.

More importantly, the OTP section states that **each target has an OTP area**.

The same OTP section expresses access and protection in target language: the target is placed in OTP operation mode, after which the relevant program/read/protect operations apply to that target's OTP area.

For that documented 2009 family, the interface-level model is therefore explicitly:

```text
physical package
    |
    +--> target 1
    |       +--> OTP area 1
    |
    +--> target 2
    |       +--> OTP area 2
    |
    +--> ...
```

and the protection operation is naturally interpreted at the selected target's OTP area.

This supports a direct 2009 distinction:

```text
package identity
    != target identity
    != target-local OTP area identity
```

---

# 5. Chronology guardrail — do not back-project 2009 target semantics into 2006

The two source families are useful together only if their temporal roles remain separate.

### What the 2006 source proves

```text
stacked package
    -> multiple internal dies
    -> separately selected CE#/CE2# sections
    -> OTP commands operate through the selected command interface
```

### What the 2009 source adds

```text
multi-target package model
    -> each target explicitly has an OTP area
    -> OTP operation mode and protection are expressed per target
```

### What the combined record does not prove

It does **not** prove that the Rev. D 12/06 8Gb product internally used exactly the same target vocabulary, target-to-die partition, OTP-state implementation, or protection-latch granularity as the 2009 family.

So the acceptable historical sentence is:

> Micron's 2006 stacked device already exposed sub-package command-selection domains; by 2009 Micron documentation explicitly described OTP storage as target-scoped.

The unacceptable stronger sentence would be:

> Every CE on the 2006 part definitely had an independently implemented OTP-protection latch identical to the later target model.

The inspected sources do not justify that claim.

---

# 6. Engineering reconstruction — package-level immutability is a stronger claim than target-level protection

The historical record yields a useful engineering rule even without reconstructing latch circuitry.

Suppose a provisioning system records only:

```text
part number
+ package serial / board location
+ "OTP protect succeeded"
```

For a package that exposes multiple selectable internal targets or sections, that record can be underspecified.

A stronger evidence record is:

```text
exact part / revision
+ package identity
+ selected CE# / target identity
+ relevant LUN or die context when documented
+ protection command result
+ protection-status observation
+ post-protect negative programming test where safe/appropriate
```

The general rule is:

```text
successful protect in one demonstrated authority domain
    != package-wide proof of immutable state
```

unless the device documentation itself defines that authority domain as package-wide.

This is an **engineering reconstruction** from the documented scope structure. It is not a quotation from the Micron manuals.

---

# 7. Retention consequence — retained authority state has a granularity

Case 149 is about more than retained payload bits. The irreversible protection state itself is retained control state: it changes which future transitions remain legal.

The present deepening adds a second axis:

```text
retained authority state
    has persistence semantics
    AND
    has a scope / granularity
```

Those are independent questions.

For example:

```text
protection state survives
    != protection state is package-global

package contains protected OTP
    != every selectable OTP domain in the package is proven protected
```

A retention analysis that records only *whether* a lock survives but not *what the lock governs* can therefore overstate the retained authority boundary.

---

# 8. Provisioning and forensic implications

## 8.1 Provisioning logs should preserve selection provenance

For stacked NAND, a package-level inventory record is useful but not always sufficient evidence for irreversible state transitions.

Where the device exposes multiple targets or chip-enable domains, tooling should preserve which selector was active when the transition was issued and verified.

At minimum:

```text
physical-package identity
+ command-selection identity
+ authority-state result
```

should remain distinguishable.

## 8.2 A status bit is evidence only for its documented observation context

The 2006 datasheet exposes an OTP-protection status indication. But the existence of a status bit does not license a reader to silently widen the scope of the observation from selected device/section to entire package.

The scope must come from the device documentation, not from the fact that the bit is easy to read.

## 8.3 Negative tests are especially valuable after irreversible transitions

For a claim such as “this package is now immutable,” a stronger test plan checks every documented authority domain that matters to the claim.

A domain that was never selected, queried, or challenged remains an evidence gap even if another domain reports protection success.

This is a validation recommendation, not a historical assertion that any specific Micron production flow performed such a test.

---

# 9. Functional analogies — bounded, not genealogical

## 9.1 Case 114 — NVMe namespace write protection

[`../cases/114-nvme14-namespace-write-protection.md`](../cases/114-nvme14-namespace-write-protection.md)

Functional analogy only:

```text
physical controller/device
    can contain lower-level mutation-authority scopes
```

A protection state attached to one namespace should not be inflated into a controller-wide claim without evidence. Likewise, a NAND package may contain narrower command/protection domains.

There is **no claim** that NVMe namespace protection derives historically from NAND OTP targeting.

## 9.2 Case 110 — S3 Object Lock

[`../cases/110-amazon-s3-object-lock-version-worm-retention.md`](../cases/110-amazon-s3-object-lock-version-worm-retention.md)

A weaker functional analogy is that retained mutation authority is attached to an identified scope. Bucket-level enablement, object-version retention, and physical storage are not interchangeable levels of identity.

Again, this is structural comparison only, not technical genealogy.

---

# 10. Philosophical interpretation — authority belongs to a relation, not merely an enclosure

A physical enclosure encourages a misleading intuition that it defines one indivisible object of authority.

The NAND evidence gives a more careful model:

```text
one enclosure
    can contain several selectable operational domains
```

and therefore:

```text
"this package is protected"
```

is not a primitive fact. It is a compressed statement whose validity depends on which internal authority domains the protection operation actually governs.

This is a philosophical interpretation of the engineering structure, not a historical claim about Micron's design intent.

---

# 11. Explicit non-claims

This deepening does **not** claim that:

1. the 2006 8Gb Rev. D part had one independent OTP-protect latch per CE#;
2. the 2006 4Gb dual-die organization necessarily had one OTP area per die;
3. the 2009 target model can be back-projected unchanged into the 2006 product;
4. CE# selection directly reveals the physical location of the protection state;
5. a CE-selected section and a physical die are always the same thing;
6. a target and a LUN are always the same thing;
7. the protection state is implemented with any particular fuse, floating-gate cell, latch, ROM, or reserved NAND page;
8. the OTP-protect operation provides package tamper resistance;
9. OTP protection is a sanitization primitive;
10. OTP protection provides confidentiality;
11. OTP protection prevents invasive physical modification;
12. the mirrored PDFs are origin-hosted archival Micron copies;
13. the current evidence proves post-protect state across every reset and full power-cycle condition on real hardware;
14. the 2009 source is the earliest Micron use of the phrase “each target has an OTP area”;
15. successful status from one selected domain proves package-wide immutable state.

---

# 12. What this slice closes

This pass closes a bounded part of the Case 149 evidence debt:

- the exact Rev. D 12/06 product organization was re-checked rather than treated as a generic “Micron NAND” abstraction;
- the 8Gb package's multi-die, dual-CE selection structure is now explicitly connected to authority-scope analysis;
- later Micron documentation provides a direct same-vendor witness that OTP areas can be explicitly target-scoped;
- package identity is therefore no longer an acceptable default proxy for protection-authority scope in the Case 149 analysis.

The key result is:

```text
retained irreversible authority
    must be analyzed at its documented control scope

physical package identity alone
    does not establish that scope
```

Case 149 remains `grounded`.

---

# 13. Remaining evidence debt

The next useful slices are now narrower.

## A. Recover an origin-hosted or archive-origin Rev. D 12/06 datasheet

The exact document has been identified and checked, but current custody remains mirrored-primary (`H/P*`).

## B. Find an explicit 2006-era statement of OTP protection-state scope

Best evidence would directly say whether protection is per CE#, per die, per array, or package-global for the exact Rev. D family.

Without that, the present note deliberately stops at documented selection scope.

## C. Hardware validation across targets and power cycles

For an exact supported stacked part:

1. identify every documented selectable domain;
2. program distinguishable OTP test state before protection where safe;
3. protect one documented domain;
4. read protection status in each domain;
5. attempt a controlled prohibited reprogram operation where appropriate;
6. reset and fully power-cycle;
7. repeat observations.

That would convert the current interface-level scope boundary into device-observed evidence.

## D. Push the explicit target-scoped wording earlier

Search earlier Micron datasheets and application notes for the first direct “each target has an OTP area” or equivalent wording.

That is a genealogy question; a broad Micron stacked-NAND / ONFI target history should live in `computing-archaeology` if developed beyond the retention-specific evidence needed here.

---

# 14. Related-repository boundary

A fresh search of `tmzncty/computing-archaeology` for Micron NAND OTP / the exact part family / OTP DATA PROTECT did not reveal an existing technical-history package to reuse.

Therefore this note keeps only the retention-specific evidence needed by Case 149. A wider history of multi-die NAND packaging, CE#/target/LUN terminology, and ONFI target standardization should be developed there rather than duplicated here.

---

# Bottom line

The 2006 Micron record establishes that one physical 8Gb NAND package can expose multiple independently selected internal sections while also supporting irreversible OTP protection. The inspected Rev. D text does not disclose enough to equate those selection domains with independently implemented protect latches.

By 2009, Micron documentation explicitly states that **each target has an OTP area**, making the lower-than-package OTP scope visible in the interface model.

The defensible cross-revision lesson is therefore not “the 2006 chip definitely had one lock per CE.” It is narrower and more useful:

```text
one physical package
    can contain multiple authority-relevant selection domains

so

package-level immutability
    requires package-level scope evidence
    rather than a single successful protect result
```
