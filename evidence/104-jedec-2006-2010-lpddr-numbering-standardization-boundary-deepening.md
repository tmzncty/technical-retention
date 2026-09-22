# Evidence 104D — 2006–2010 LPDDR Standards-Number Provenance and the DPD Standardization Boundary

**Status:** `bounded deepening complete`

**Canonical case:** [`../cases/104-micron-lpddr-selective-adaptive-self-refresh.md`](../cases/104-micron-lpddr-selective-adaptive-self-refresh.md)

**Evidence index:** [`104-lpddr-retention-evidence-index.md`](104-lpddr-retention-evidence-index.md)

## Research question

Case 104 already has a strong product-document chain for low-power retention semantics:

- Micron's May-2002 `ADVANCE` Mobile SDRAM document already distinguishes ordinary Power-Down, SELF REFRESH, and Deep Power-Down (DPD);
- later Micron and Hynix documents show continuity, optionality, and configuration-state loss;
- the 2009–2014 Micron LPDDR family grounds TCSR and PASR as separate maintenance-rate and maintenance-scope controls.

The canonical case deliberately left **JEDEC introduction / revision chronology** open. This slice asks a narrower provenance question:

> When can the first-generation LPDDR standard be identified under the names `JESD79-4` and `JESD209`, and what can that chronology establish without pretending that a standards identifier proves the date on which DPD itself was invented, introduced, or made mandatory?

The bounded result is:

1. **May 2006** is independently attested as the date of the LPDDR specification under the designation `JESD79-4`;
2. standards-catalog metadata says the document was **originally numbered `JESD79-4` from May 2006 to August 2007** and was corrected to **`JESD209` on 17 September 2007**;
3. catalog and legal-reference records then expose a bounded revision sequence through **`JESD209A` / `JESD209A-1` in 2009** and **`JESD209B` in February 2010**;
4. the inspected source set does **not** include the full May-2006 `JESD79-4` or August-2007 `JESD209` normative body, so this slice does **not** claim a clause-level first-standardization date for DPD, PASR, or TCSR.

That last limit is central. The new evidence closes a **document identity / revision-provenance** debt, not the still-open **feature-introduction** debt.

---

## Source custody and evidence classes

### S1 — NXP/Freescale product documentation preserving the old standard designation

NXP's hosted `MPC5675K` data sheet identifies the LPDDR standard in its memory-controller requirements as:

> `JEDEC STANDARD, Low Power Double Data Rate (LPDDR) SDRAM Specification, JESD79-4, May 2006`

The same wording is preserved in NXP's `PXS30` data sheet.

Sources:

- <https://www.nxp.com/docs/en/data-sheet/MPC5675K.pdf>
- <https://www.nxp.com.cn/docs/en/data-sheet/PXS30.pdf>

Evidence class here: **H/P** for the later manufacturer document's own compatibility/reference statement. It is not treated as a May-2006 publication witness; it is a later primary manufacturer source independently preserving the identity and date of the standard it references.

### S2 — standards-catalog metadata for `JESD209`

GlobalSpec's JEDEC standards record for `JESD209` gives the LPDDR scope and records the note:

> `JESD209 was originally numbered as JESD79-4 May 2006 to August 2007, corrected to JESD209 09/17/2007`.

Its document-history panel also exposes LPDDR entries for August 2007, February/March 2009, and February 2010.

Sources:

- <https://standards.globalspec.com/std/1236521/jedec-jesd-209>
- historical record page: <https://standards.globalspec.com/std/1161171/jedec-jesd-209>

Evidence class: **H/S** — a specialist standards-catalog record representing JEDEC metadata, not an origin-host full standard facsimile.

### S3 — legal bibliographic reference identifying `JESD209A`

The prior-art/reference list preserved in `US9218860B2` identifies:

- `Low Power Double Data Rate (LPDDR) SDRAM Standard`;
- `JESD209A`;
- as a **revision of `JESD209, Aug. 2007`**;
- dated **February 2009**.

Source: <https://patents.google.com/patent/US9218860B2/en>

Evidence class: **H/P*** for a formal legal record reproducing bibliographic identity, not the normative standard text itself.

### S4 — standards-catalog records for the 2009 addendum and 2010 revision

NSAI / Intertek Inform identify `JESD209A-1 : 2009` as **Addendum No. 1 to JESD209A**, titled for **LPDDR SDRAM, 1.2 V I/O**, and record `JESD209B : 2010` as its superseding revision. Their `JESD209B` record gives a February-2010 publication date and 76 pages.

Sources:

- <https://shop.standards.ie/en-ie/standards/jedec-jesd-209a-1-2009-1137199_saig_jedec_jedec_2616241/>
- <https://www.intertekinform.com/en-gb/standards/jedec-jesd-209b-2010-1137199_saig_jedec_jedec_2690420/>

Evidence class: **H/S** — standards-distribution metadata. These records are sufficient for revision identity and supersession, but not for uninspected normative clause semantics.

---

## Historical record

### H/P + H/S — `JESD79-4, May 2006` is a defensible first-generation LPDDR standards-document floor

The NXP/Freescale memory-controller documentation explicitly cites `JESD79-4, May 2006` as the `Low Power Double Data Rate (LPDDR) SDRAM Specification`. GlobalSpec independently states that the LPDDR document was originally numbered `JESD79-4` beginning in May 2006.

The bounded documentary floor is therefore:

```text
May 2006
    LPDDR standards document identifiable as JESD79-4
```

This is a **standards-document floor**, not a DPD feature floor and not a product floor.

Case 104 already has a different, earlier product-document floor:

```text
May 2002
    Micron ADVANCE Mobile SDRAM document
    documents Deep Power-Down semantics

May 2006
    LPDDR standards document
    identifiable as JESD79-4
```

The four-year ordering is useful precisely because it blocks a tempting but unsupported inference:

```text
JEDEC LPDDR standard appeared in 2006
    therefore
DPD first appeared in 2006
```

The sources do not support that inference.

### H/S — the standard's identifier changed from `JESD79-4` to `JESD209`

The standards-catalog record says the LPDDR specification was originally numbered `JESD79-4` from May 2006 through August 2007 and was corrected to `JESD209` on 17 September 2007.

The same catalog's history exposes an August-2007 LPDDR specification under the `JESD209` family.

A conservative documentary chain is therefore:

```text
JESD79-4
    May 2006 designation
        ↓
JESD209
    August/September 2007 renumbered/corrected designation
```

This is evidence about **document identity and numbering**. It is not by itself evidence that a circuit, command, or low-power state changed on the day the identifier changed.

### H/S — the cataloged LPDDR revision family continues through `JESD209A`, `JESD209A-1`, and `JESD209B`

A legal bibliographic record identifies `JESD209A` as a February-2009 revision of the August-2007 `JESD209`. Standards-distribution records identify a 2009 `JESD209A-1` 1.2-V-I/O addendum and record `JESD209B` as the superseding February-2010 revision.

The bounded revision-provenance chain is therefore:

```text
JESD79-4              May 2006
    ↓ numbering correction / family transition
JESD209               Aug/Sep 2007
    ↓ revision
JESD209A              Feb 2009
    ↓ addendum
JESD209A-1            2009
    ↓ superseded by
JESD209B              Feb 2010
```

The exact day/month formatting shown by different standards distributors for the 2009 addendum is locale-sensitive. This slice therefore uses the unambiguous year/title relation and does not manufacture a day-level chronology from ambiguous date formatting.

### H/S — the LPDDR specification itself is described as a derivative standards work, not an isolated invention event

The historical GlobalSpec record reproduces the LPDDR specification's scope language saying the specification was created from the DDR-I specification and aspects of DDR2 where shared technology made commonality useful, with low-power changes considered and balloted.

That is useful historical vocabulary for the standards process:

- `created based on`;
- `shared technology`;
- changes `considered and balloted`;
- changes incorporated into the LPDDR specification.

It does **not** establish a single inventor, a single implementation lineage, or the origin date of every low-power feature.

---

## The negative result: DPD's exact JEDEC introduction revision is still open

The strongest result of this slice is partly a refusal to overclaim.

The inspected source set gives document identity, revision dates, scope, supersession, and later references. It does **not** give a directly inspected normative clause from:

- May-2006 `JESD79-4`;
- the August-2007 `JESD209` body;
- February-2009 `JESD209A`;
- or the 2009 addendum

showing exactly when `Deep Power-Down` entered the standard, whether it was mandatory or optional in each revision, what command encoding applied, or how its exit/reinitialization contract changed.

Current third-party LPDDR verification/controller-IP pages commonly pair `JESD209A-1` / `JESD209B` compliance with `Deep Power Down` support. Those pages are useful discovery aids, but they are current implementation/vendor claims and are **not** promoted here into period standards evidence.

Accordingly:

```text
standards-family chronology established
    !=
DPD clause genealogy established
```

and:

```text
later implementation claims compliance with JESD209B
    !=
proof of the exact wording or optionality in JESD79-4 (2006)
```

---

## Engineering reconstruction

### E — a standards identifier is retained documentary state, not the mechanism itself

The same standards lineage can be referred to under different identifiers. For this slice, the important engineering/history distinction is:

```text
document family / requirements lineage
    !=
document number string
```

The 2007 renumbering demonstrates that a designation can change while the documentary object is represented as a continuation/correction of the same LPDDR standards family.

This is a provenance observation. It does not license assuming byte-for-byte clause identity across revisions.

### E — standardization chronology and product chronology answer different questions

Case 104 now has at least three separate temporal axes:

```text
product-document semantics
    May 2002 Micron ADVANCE Mobile SDRAM DPD witness

standards-document identity
    May 2006 JESD79-4 LPDDR specification

standards-family revision / renumbering
    2007 JESD209 → 2009 A/A-1 → 2010 B
```

None can substitute for the others.

The first tells us that a named manufacturer had already documented a DPD contract. The second tells us when a JEDEC LPDDR standards document can be identified. The third tells us how the standards artifact was renamed and revised.

### E — standards inheritance does not establish feature invention genealogy

The specification's own description of being based on DDR-I plus aspects of DDR2 shows documentary/technical inheritance at the standards level. It still does not answer:

- who first devised DPD;
- which vendor proposal or ballot introduced it;
- whether Micron's 2002 implementation directly influenced JEDEC wording;
- whether the 2006 standard copied a particular vendor command/state machine;
- when each vendor shipped conforming silicon.

Those require proposal, ballot, patent, product, and/or archival evidence.

### E — renumbering is not a retention-mechanism transition

The repository studies changes in retention relations. A standards-number change matters only as provenance unless a source shows that the technical contract changed with it.

Therefore:

```text
JESD79-4 → JESD209
    !=
Power-Down → SELF REFRESH → DPD
```

The left relation is a documentary designation transition. The right relation is a device-state / retention-contract distinction.

---

## Functional analogy

A limited functional analogy can be drawn to Case 04's separation of logical identity and physical location:

```text
standards-family identity can survive an identifier change
```

just as another technical object may preserve a logical designation while changing an embodiment.

This is **only a functional analogy** about identity-through-renaming. It is not evidence that standards documents use FTL-like identity machinery, and it is not a historical genealogy between document control and storage address translation.

---

## Philosophical interpretation

No new philosophical claim is required to justify this slice.

The retention-relevant lesson is methodological: historical interpretation depends on retaining enough provenance to know which document, revision, identifier, and evidence class authorize a claim. That observation remains subordinate to the source chronology and should not be inflated into a general philosophy of archival identity.

---

## Relation to Case 105 / LPDDR2

Case 105 separately establishes a standards-level public floor for LPDDR2 Per-Bank Refresh through the April-2009 `JESD209-2` announcement and directly inspected February-2010 `JESD209-2B` text.

Do not merge the two chains:

```text
first-generation LPDDR
    JESD79-4 / JESD209 / JESD209A / JESD209B

LPDDR2
    JESD209-2 / -2A / -2B ...
```

The shared `JESD209` stem is standards-family naming. It does not make an LPDDR2 normative clause valid evidence for first-generation LPDDR DPD semantics.

---

## Related-repository routing

Fresh exact-topic code searches in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `JESD209` and `LPDDR` did not surface a dedicated reusable standards-genealogy packet during this slice.

Keep `technical-retention` focused on:

- which retention/power-state relation a standards revision actually authorizes;
- product-document floor versus standardization floor;
- optionality, control state, exit/reinitialization, and retention-contract boundaries;
- provenance needed to avoid silently projecting later revision semantics backward.

Prefer `computing-archaeology` for a broad mobile-DRAM standards history, committee/ballot history, market adoption, controller-IP history, packaging evolution, vendor competition, and product-family genealogy not needed to establish a retention boundary.

---

## Explicit non-claims

This evidence packet does **not** claim that:

1. JEDEC invented LPDDR in May 2006;
2. DPD was invented in May 2006;
3. DPD first became public in May 2006;
4. Micron's May-2002 document proves commercial shipment in 2002;
5. Micron's 2002 DPD mechanism was copied into JESD79-4;
6. every clause survived the `JESD79-4` → `JESD209` renumbering unchanged;
7. every `JESD209`-family device had to implement DPD;
8. `JESD209A-1` changed DPD merely because it changed I/O-voltage requirements;
9. `JESD209B`'s 2010 publication proves a 2010 product-adoption date;
10. a standards-catalog record is equivalent to a directly inspected origin-host facsimile;
11. a later controller/verification-IP page can establish 2006 normative wording;
12. the document-number transition is itself a change in retention mechanism;
13. LPDDR2 clauses can be back-projected into first-generation LPDDR;
14. a standard revision date is an invention-priority date;
15. standardization chronology is the same as silicon, shipment, or deployment chronology.

---

## Remaining evidence debt

The next high-value work is now sharply bounded:

1. obtain and directly inspect a full **May-2006 `JESD79-4`** facsimile;
2. obtain and inspect **`JESD79-4A` / August-2007 `JESD209`** revision-difference material;
3. locate the exact **DPD** clause, command table, optionality language, and exit/reinitialization wording in each first-generation LPDDR revision;
4. determine whether DPD appears in the initial 2006 text or enters/changes later;
5. separately trace PASR/TCSR standardization rather than assuming they share DPD's revision history;
6. if available, recover JEDEC ballot/proposal metadata that identifies the change request without turning proposal authorship into invention priority;
7. find period named controllers/products that explicitly cite the then-current revision, while keeping compliance claims separate from shipment evidence.

This slice does not justify a maturity promotion. **Case 104 remains `grounded`.**
