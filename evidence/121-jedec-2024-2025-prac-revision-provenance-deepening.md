# Evidence 121 — JESD79-5C → 5C.01 → 5D PRAC Revision Provenance Deepening

## Scope

This record closes one narrow part of Case 121's standards-version debt:

> What can public evidence establish about the **document lineage** of DDR5 PRAC from JESD79-5C through JESD79-5C.01 to JESD79-5D, without silently projecting one revision's normative text into another?

The bounded result is deliberately narrower than a clause-by-clause standards diff.

It establishes:

- the April 2024 public introduction of named DDR5 `Per-Row Activation Counting (PRAC)` in JESD79-5C;
- the July 2024 `JESD79-5C.01_v1.31` document identity and its explicit label as an **Editorial Revision** of `JESD79-5C_v1.30`;
- persistence of the named PRAC section architecture across publicly inspectable tables of contents for 5C, 5C.01, and 5D;
- the November 2025 `JESD79-5D_v1.41` document identity, its historical-edition relation to 5C.01/5C, and the presence of an informative annex specifically titled `Differences between JESD79-5D and JESD79-5C.01`;
- why those facts are enough to improve provenance discipline but **not** enough to claim line-by-line semantic identity or to enumerate every PRAC change in 5D.

This record does **not**:

- reproduce copyrighted JEDEC standard text beyond short identifying/TOC phrases;
- claim access to the complete licensed JESD79-5D text;
- claim that `Editorial Revision` means every normative sentence is byte-for-byte identical;
- claim that unchanged section titles imply unchanged timing values, mode-register encodings, thresholds, error behavior, or reset semantics;
- claim that the existence of a newer whole-standard revision proves PRAC itself changed;
- replace manufacturer product documentation with a standards inference;
- establish committee proposal genealogy before the 2024 publication;
- establish implementation genealogy from JEDEC text to any named DRAM die or memory controller.

The purpose is version provenance: **which document is being used for which historical claim**.

---

## Source 1 — JEDEC publication announcement, 17 April 2024

**Type:** standards-organization primary announcement redistributed by Business Wire (`H/P`)

- title: `JEDEC Updates JESD79-5C DDR5 SDRAM Standard: Elevating Performance and Security for Next-Gen Technologies`;
- source attribution: JEDEC via Business Wire;
- date: 17 April 2024;
- redistributed copy used here: https://markets.financialcontent.com/bpas/article/bizwire-2024-4-17-jedec-updates-jesd79-5c-ddr5-sdram-standard-elevating-performance-and-security-for-next-gen-technologies
- original JEDEC destination named in the release: https://www.jedec.org/news/pressreleases/jedec-updates-jesd79-5c-ddr5-sdram-standard-elevating-performance-and-security

### Claims supported

The release says JEDEC had published `JESD79-5C DDR5 SDRAM` and names **Per-Row Activation Counting (PRAC)** as a new data-integrity feature. It describes wordline-granular activation counting and a DRAM-to-system alert / mitigation-time coordination path.

The same release also identifies other whole-standard changes, including extension of defined timing parameters through 8800 Mbps, Self-Refresh Exit Clock Sync, DDP timing, and PASR deprecation.

**Safe historical claim:**

> By 17 April 2024, JEDEC publicly identified PRAC as part of JESD79-5C and described its high-level DRAM/system coordination role.

### Claims not supported

The announcement does not provide a complete normative PRAC clause set. In particular, it is not sufficient evidence for exact:

- ACI sequencing;
- mode-register bit encodings;
- alert/back-off timing values;
- activation-counter error semantics;
- reset/power-up behavior;
- later-revision changes.

Those require the standard itself or bounded manufacturer/product documentation.

---

## Source 2 — JESD79-5C_v1.30 public preview metadata / table of contents

**Type:** standards-document preview from an engineering-standards distributor (`H/P`, document-identity / structure witness)

- document: `JEDEC Standard No. 79-5C_v1.30`;
- title: `DDR5 SDRAM`;
- distributor preview: https://store.accuristech.com/products/preview/2901296
- release family: April 2024, independently anchored by the JEDEC 17 April announcement above.

The publicly indexed preview exposes the table of contents for the PRAC portion. It identifies:

- Clause 16, `DDR5 Per Row Activation Counting`;
- 16.1 `Introduction`;
- 16.2 `Activation Counter Initialization`;
- 16.3 `Per Row Activation Counting Core Timing Parameters`;
- 16.3.1 `Refresh Operation Scheduling Flexibility`;
- 16.3.2 `Precharge Timing`;
- 16.4 `Per Row Activation Counting Response`;
- 16.4.1 `Targeted Refresh`;
- 16.4.2 `Targeted RFM`;
- 16.5 `Back-off Protocol` and Alert Back-Off subclauses;
- 16.6 `ALERT_n Priorities`;
- 16.7 `Activation Counter Errors`;
- 16.8 `Per Row Activation Counting Testing`;
- 16.9 `ALERT_n Verification`;
- 16.10 `PRAC and ABO Mode Register Definition`.

This is useful because it places several terms already used in Case 121 inside the **5C document structure itself**, rather than deriving them only from a later Micron product document.

It does **not** expose enough clause text to substitute for the full standard.

### Safe bounded conclusion

```text
5C public announcement
    -> proves PRAC publication milestone / high-level role

5C document preview
    -> proves named PRAC clause architecture exists in 5C

announcement-level description
    !=
full normative clause semantics
```

---

## Source 3 — JESD79-5C.01_v1.31, July 2024

**Type:** standards-document preview + standards-catalog metadata (`H/P`, document-version witness)

### Document identity

Accuris' JEDEC preview identifies:

- `JESD79-5C.01_v1.31`;
- `DDR5 SDRAM`;
- `July 2024`;
- and, critically, the parenthetical document label:

`Editorial Revision of JESD79-5C_v1.30, April 2024`.

Preview:
https://store.accuristech.com/asa/products/preview/2909094

A second Accuris/ECIA preview exposes the 5C.01 table of contents:
https://store.accuristech.com/ecia/products/preview/2909094

NSAI and Intertek catalog records independently identify `JESD79-5C.01_v1.31:2024` as a July 2024 JEDEC publication, later superseded by JESD79-5D:

- https://shop.standards.ie/en-ie/standards/jedec-jesd79-5c-01-v1-31-2024-1376174_saig_jedec_jedec_3438787/
- https://www.intertekinform.com/en-gb/standards/jedec-jesd79-5c-01-v1-31-2024-1376174_saig_jedec_jedec_3438787/

### PRAC section continuity visible at TOC level

The 5C.01 preview again exposes Clause 16 `DDR5 Per Row Activation Counting`, including:

- 16.2 `Activation Counter Initialization`;
- 16.3 `Per Row Activation Counting Core Timing Parameters`;
- 16.4 `Per Row Activation Counting Response`;
- targeted refresh / targeted RFM;
- back-off protocol;
- `Activation Counter Errors`;
- PRAC testing;
- ALERT verification;
- `PRAC and ABO Mode Register Definition`.

The public TOC therefore supports **section-architecture continuity** between 5C and 5C.01.

The document header's own phrase `Editorial Revision` is also important provenance evidence. It tells us how this edition is classified by the document itself.

### What `Editorial Revision` safely means here

The strongest safe claim is:

> JESD79-5C.01_v1.31 identifies itself as an editorial revision of JESD79-5C_v1.30, and the publicly visible PRAC clause headings remain structurally continuous.

That is stronger than saying only “another revision exists.”

It is still weaker than:

> every PRAC normative sentence, numeric parameter, table entry, note, cross-reference, and mode-register definition is identical.

Without a licensed redline or direct inspection of the relevant clauses / Annex D, the latter remains unsupported.

Therefore:

```text
editorial-revision label
    !=
proof of byte-identical normative text

same PRAC section titles
    !=
proof of unchanged values / requirements
```

---

## Source 4 — JESD79-5D_v1.41, November 2025

**Type:** standards-document preview + standards-catalog metadata (`H/P`, later-edition witness)

### Document identity and publication lineage

Accuris' current-document search identifies:

- `JESD79-5D_v1.41`;
- `DDR5 SDRAM`;
- publication date `11/01/2025` in the U.S.-formatted storefront;
- historical editions `JESD79-5C.01_v1.31` and `JESD79-5C_v1.30`.

Search/catalog result:
https://store.accuristech.com/searches/62400105

The public preview identifies the document as `JEDEC Standard No. 79-5D`, states that it came from JEDEC Board Ballot `JCB-25-78`, and names JC-42.3 as the cognizant subcommittee:
https://store.accuristech.com/products/preview/3062398

NSAI / Intertek records identify the edition as current and show it superseding `JESD79-5C.01_v1.31:2024`:

- https://shop.standards.ie/en-ie/standards/jedec-jesd79-5d-2025-1450100_saig_jedec_jedec_3780502/
- https://www.intertekinform.com/en-gb/standards/jedec-jesd79-5d-2025-1450100_saig_jedec_jedec_3780502/

The locale-specific storefronts render the numeric date differently (`01-11-2025` in a UK/EU view; `11-01-2025` in a U.S. view). Taken together with the explicit month/year catalog context, this record uses **November 2025**, not an ambiguous day/month interpretation.

### PRAC remains a named Clause 16 architecture

The 5D preview still contains:

- Clause 16 `DDR5 Per Row Activation Counting`;
- `Activation Counter Initialization`;
- PRAC core timing parameters;
- refresh-operation scheduling flexibility;
- precharge timing;
- PRAC response;
- targeted refresh / targeted RFM;
- back-off protocol;
- `Activation Counter Errors`;
- PRAC testing;
- ALERT verification;
- `PRAC and ABO Mode Register Definition`.

This establishes a useful but bounded continuity claim:

> PRAC/ACI remains a named standards structure in JESD79-5D.

It does **not** establish that every clause remained semantically unchanged from 5C.01.

### The standard itself exposes the correct delta locus

Most importantly, the 5D table of contents includes:

- `ANNEX D - (Informative) Differences between JESD79-5C.01 and JESD79-5C`;
- `ANNEX E - (Informative) Differences between JESD79-5D and JESD79-5C.01`.

That gives the next research pass a much sharper target. Instead of inferring changes from product documents, press releases, page counts, or changed page numbers, the standards lineage itself names an informative revision-difference annex.

The public search preview used in this round exposes the existence/title of Annex E but not enough of its contents to enumerate its PRAC deltas safely.

### Whole-standard change ≠ PRAC-specific change

The 5D TOC also includes an added DDR5-9200 timing-parameter entry that is absent from the visible 5C/5C.01 timing-grade list. That is direct evidence that the **whole standard** evolved beyond 5C.01.

But this relation must remain explicit:

```text
5D contains substantive whole-standard changes
    !=
PRAC necessarily changed in the same way

PRAC section headings persist
    !=
PRAC normative semantics necessarily stayed identical
```

The revision itself is not evidence for either side of that stronger question.

---

## Revision-provenance chronology

The public evidence now supports this bounded chain:

```text
April 2024
JESD79-5C_v1.30
    -> JEDEC publicly announces PRAC as part of DDR5
    -> Clause 16 PRAC architecture visible in document preview

July 2024
JESD79-5C.01_v1.31
    -> self-identifies as an Editorial Revision of 5C_v1.30
    -> PRAC section architecture remains visible

November 2025
JESD79-5D_v1.41
    -> later JEDEC DDR5 edition
    -> supersedes / follows 5C.01 in standards catalogs
    -> PRAC Clause 16 remains present
    -> Annex E explicitly exists for 5D-vs-5C.01 differences
```

This is a **document chronology**, not yet a complete semantic-change chronology.

---

## Historical record vs engineering reconstruction

### Historical record (`H/P`)

Directly supported by the sources above:

1. JEDEC publicly announced JESD79-5C and PRAC on 17 April 2024.
2. The 5C preview contains a dedicated PRAC Clause 16 with ACI, timing, response, error, testing, verification, and PRAC/ABO register-definition headings.
3. `JESD79-5C.01_v1.31` is dated July 2024 and explicitly labels itself an `Editorial Revision` of `JESD79-5C_v1.30, April 2024`.
4. The 5C.01 preview retains the same named PRAC clause architecture at TOC level.
5. `JESD79-5D_v1.41` is a November 2025 JEDEC DDR5 edition; standards catalogs identify 5C.01 as a superseded/historical predecessor.
6. The 5D preview still contains the named PRAC Clause 16 architecture.
7. The 5D TOC contains an informative Annex E specifically for differences between 5D and 5C.01.

### Engineering reconstruction (`E`)

The project-level inference is about evidence handling:

> a technical claim about a standards-defined maintenance mechanism should carry a **revision identity**, not merely the family name `DDR5`.

For Case 121, that means:

```text
claim observed in 5C
    !=
automatically normative in 5D

claim observed in Micron Rev. E
    !=
automatically a clause-level JEDEC requirement

same named PRAC mechanism across revisions
    !=
same exact timing / encoding / reset semantics
```

The revision identity is part of the provenance of the retention contract.

---

## Product documentation and standard revision are different evidence axes

Case 121 already uses Micron's Rev. E (11/2024) DDR5 core document for the concrete ACI/counter-refresh contract. The standards chronology here does not convert that product evidence into a JEDEC-wide universal rule.

The safe model is two-dimensional:

```text
standards axis
5C -> 5C.01 -> 5D

manufacturer-document axis
Micron core-doc revision -> later Micron revisions / named parts
```

A product document may expose behavior consistent with one standards generation without proving exact conformance to every later edition.

Conversely, a later standard may retain a named feature without proving that an older product implements every later detail.

Therefore:

> **standard edition continuity ≠ product implementation continuity**.

And:

> **product revision continuity ≠ standards-clause identity**.

This mirrors the repository's Case 111 discipline around firmware implementation epochs, but the comparison is functional only. A JEDEC standard revision and an SSD firmware revision are not the same historical or technical object.

---

## Why this matters for retention analysis

PRAC is second-order retention infrastructure: activation-count state helps determine when disturbance mitigation should happen. Case 121 already shows that this state itself can require initialization, refresh, integrity handling, and re-establishment.

Standards revision provenance adds another layer:

```text
retained state
    -> governed by a protocol contract

protocol contract
    -> belongs to a particular document revision

same feature name in later revision
    !=
proof that every governing condition is unchanged
```

This is not merely bibliographic housekeeping. If a later edition changes initialization, timing, error, alert, or mode-register semantics, then the conditions under which activation-count state is considered trustworthy could also change.

This round does **not** claim that such a PRAC change occurred in 5D. It establishes why that question must be answered from the revision-difference evidence rather than assumption.

---

## Functional analogy — bounded

A limited analogy to software/schema versioning is useful:

```text
same field / feature name across versions
    !=
same complete contract
```

But this is only a methodological analogy. JEDEC DDR5 revisions are not database schema migrations, and no software genealogy is implied.

The more relevant cross-case comparison is Case 111:

```text
Case 111:
same SSD family + different firmware revision
    -> implementation epoch may alter maintenance behavior

Case 121:
same DDR5 feature family + different standards revision
    -> normative-contract epoch may alter what can safely be asserted
```

The common function is **version-bounded evidence**. The mechanisms and institutions differ.

---

## Philosophical interpretation — bounded

A retention claim is not only about whether some physical bits persist. It also depends on whether the rules that make those bits meaningful and trustworthy are being cited from the correct technical epoch.

That supports one narrow interpretation:

> technical continuity requires continuity of both state and justified interpretation of the state under the applicable contract.

This is a project-level philosophical interpretation. It is not JEDEC vocabulary and should not be back-projected onto the standards committee.

---

## Explicit non-claims / guardrails

This evidence record does **not** establish any of the following:

1. `JESD79-5C.01 is byte-identical to JESD79-5C`.
2. `Editorial Revision` guarantees no normative effect whatsoever.
3. identical PRAC section titles imply identical paragraph text.
4. page-number shifts imply semantic changes.
5. a new 5D speed grade implies PRAC changed.
6. a new whole-standard revision implies PRAC changed.
7. persistence of Clause 16 implies PRAC is mandatory in every DDR5 part.
8. presence of PRAC in a standard implies the feature is enabled by default in every product.
9. JEDEC's high-level PRAC announcement specifies ACI completely.
10. Micron's ACI behavior is universal solely because 5C/5D have an ACI section.
11. 5D Annex E contains a PRAC change merely because Annex E exists.
12. lack of a publicly visible PRAC delta means no delta exists.
13. later standards catalog metadata is equivalent to the full normative standard.
14. a standards distributor is the standards authority; it is used here as a document-preview / metadata witness.
15. the 2024/2025 public chronology proves committee proposal priority or invention priority.
16. a named standards feature proves a named shipping die implements it.
17. a named shipping implementation proves every JEDEC-permitted behavior.
18. `superseded` means older documents cease to matter historically.
19. `current` standard status rewrites what engineers could have known in 2024.
20. 5D can be quoted as authority for a 5C historical claim without explicitly saying it is later evidence.

---

## Claim ledger

| Claim | Type | Strength | Evidence |
| --- | --- | --- | --- |
| JEDEC publicly announced PRAC as part of JESD79-5C on 17 Apr 2024 | `H/P` | high | JEDEC-via-Business-Wire release |
| 5C has a dedicated PRAC Clause 16 with ACI, timing, response, error/testing, alert, and MR-definition structure | `H/P` | high for document structure | Accuris 5C preview |
| 5C.01_v1.31 is a July 2024 document | `H/P` | high | document preview + catalog metadata |
| 5C.01 explicitly labels itself an Editorial Revision of 5C_v1.30 | `H/P` | high | JEDEC document header visible in Accuris preview |
| 5C.01 retains the named PRAC Clause 16 architecture at TOC level | `H/P` | high for structure | Accuris/ECIA preview |
| 5D_v1.41 is a November 2025 DDR5 edition and follows 5C.01 in the documented edition chain | `H/P` | high for document metadata | Accuris + NSAI/Intertek |
| 5D still contains named PRAC/ACI Clause 16 architecture | `H/P` | high for structure | Accuris 5D preview |
| 5D contains an informative annex explicitly for 5D vs 5C.01 differences | `H/P` | high for existence/title | 5D TOC preview |
| PRAC normative semantics are byte-identical in 5C, 5C.01, and 5D | `X` | unsupported | no line-level diff inspected |
| PRAC definitely changed in 5D | `X` | unsupported | whole-standard revision alone is insufficient |
| Standards claims should be revision-bounded | `E` | strong methodological reconstruction | version chain above |
| Product docs can be silently promoted to universal JEDEC clauses | `X` | rejected | evidence-class boundary |

---

## Related-repository check

A current GitHub search of `tmzncty/computing-archaeology` for `JESD79-5C PRAC Per-Row Activation Counting` returned no dedicated reusable packet.

Division of labor remains:

- `technical-retention`: revision-bounded retention contract, initialization/readiness, counter validity, evidence provenance, cross-case comparison;
- `computing-archaeology`: broader JEDEC committee genealogy, ballot/proposal history, vendor adoption chronology, controller/platform evolution if developed later.

No duplicate standards-history narrative is created here beyond what is needed to bound Case 121's claims.

---

## Remaining evidence debt after this round

This round narrows the previous broad item `revision-by-revision PRAC changes through JESD79-5D` into concrete next targets:

1. inspect **JESD79-5D Annex E** (`Differences between JESD79-5D and JESD79-5C.01`) and record only PRAC-relevant deltas;
2. inspect **JESD79-5C.01 Annex D** (`Differences between JESD79-5C.01 and JESD79-5C`) to determine whether the editorial revision touched PRAC wording/tables at all;
3. compare the relevant Clause 16 / MR / timing tables across 5C.01 and 5D under a lawful full-text source or licensed redline;
4. keep ACI/reset/counter-error claims revision-scoped until those deltas are directly checked;
5. map named manufacturer product-document revisions to the standards editions they explicitly claim to support, where such statements are public;
6. retain committee/proposal genealogy as a separate prior-art/history problem rather than inferring it from publication order.

The key improvement is that the open problem is no longer “what happened after 5C?” in general. The next standards task has a named source locus: **Annex D / Annex E plus the PRAC Clause 16 tables they identify as changed or unchanged**.

---

## Sources

1. JEDEC via Business Wire, `JEDEC Updates JESD79-5C DDR5 SDRAM Standard: Elevating Performance and Security for Next-Gen Technologies`, 17 April 2024: https://markets.financialcontent.com/bpas/article/bizwire-2024-4-17-jedec-updates-jesd79-5c-ddr5-sdram-standard-elevating-performance-and-security-for-next-gen-technologies
2. Accuris preview, `JEDEC Standard No. 79-5C_v1.30 — DDR5 SDRAM`: https://store.accuristech.com/products/preview/2901296
3. Accuris preview, `JESD79-5C.01_v1.31 — DDR5 SDRAM` (`Editorial Revision of JESD79-5C_v1.30, April 2024`): https://store.accuristech.com/asa/products/preview/2909094
4. Accuris/ECIA preview, `JESD79-5C.01_v1.31 — DDR5 SDRAM` table of contents: https://store.accuristech.com/ecia/products/preview/2909094
5. NSAI catalog, `JEDEC JESD79-5C.01_v1.31:2024`: https://shop.standards.ie/en-ie/standards/jedec-jesd79-5c-01-v1-31-2024-1376174_saig_jedec_jedec_3438787/
6. Accuris search/catalog, `JEDEC JESD79-5D_v1.41 — DDR5 SDRAM`: https://store.accuristech.com/searches/62400105
7. Accuris preview, `JEDEC Standard No. 79-5D — DDR5 SDRAM`: https://store.accuristech.com/products/preview/3062398
8. NSAI catalog, `JEDEC JESD79-5D:2025`: https://shop.standards.ie/en-ie/standards/jedec-jesd79-5d-2025-1450100_saig_jedec_jedec_3780502/
9. Intertek Inform catalog, `JEDEC JESD79-5D:2025`: https://www.intertekinform.com/en-gb/standards/jedec-jesd79-5d-2025-1450100_saig_jedec_jedec_3780502/

## Status effect

This deepening strengthens Case 121's **revision provenance** and narrows its open standards-delta debt, but it does not justify a maturity promotion. Case 121 remains `grounded` until the actual 5C.01→5D PRAC deltas are inspected directly and cross-vendor / named-platform evidence improves.