# Evidence 111F — Seagate Pulsar XT.2 2011 powered-retention prior art and revision-history boundary

**Status:** `bounded deepening complete`

## Scope

This record deepens one narrow chronology and source-critical question in Case 111:

> before the directly inspected April-2012 Pulsar.2 manual, did a named enterprise SSD already document powered controller-local retention monitoring / rewrite while also requiring no routine scheduled preventive maintenance?

For the directly inspected record, the answer is **yes by June 2011**.

Seagate's **Pulsar XT.2 SAS Product Manual, publication 100647497, Rev. B, June 2011** states that the drive uses SLC NAND, gives a typical three-month powered-off retention figure at 40 °C, says that powered firmware / hardware can monitor and refresh memory cells, and states more specifically that powered cells are monitored and rewritten when their levels decay unexpectedly. The same manual says that no routine scheduled preventive maintenance is required.

The document revision table adds a second, deliberately weaker chronology relation. It records:

- Rev. A — 16 March 2011 — initial release;
- Rev. B — 1 June 2011 — only sheet 34 affected, for a 7 mm weight correction.

The retention material inspected in Rev. B is on printed pp. 14 and 16, not sheet 34. The revision record therefore supports a **revision-history inference** that these passages were already present in the March-2011 Rev. A lineage. But because a Rev. A facsimile was not directly inspected in this slice, March 2011 is not promoted to the same evidential category as the directly inspected June-2011 wording.

This packet also uses the later **Pulsar.2 Rev. C, March 2013** revision table as a source-critical counterexample. That table says Rev. B (16 April 2012) changed multiple pages including p. 14, which is where the later Pulsar.2 `Data Retention` section appears. Thus the inspected 2012/2013 Pulsar.2 wording must **not** be silently back-projected into its August-2011 Rev. A.

This slice is about:

- moving the direct named-product powered-retention-maintenance floor from April 2012 to June 2011;
- distinguishing a directly inspected wording floor from a revision-history-supported inference floor;
- showing the same broad documentation-level retention relation on an SLC enterprise SSD before the later MLC Pulsar.2 witness;
- preserving the boundary between autonomous device maintenance and operator-runbook cadence.

It is **not**:

- an invention-priority claim for SSD refresh;
- a claim that Pulsar XT.2 and Pulsar.2 share one controller, firmware, threshold, scheduler, or physical rewrite geometry;
- a claim that all SLC or MLC enterprise SSDs implement this behavior;
- a claim that March 2011 is the first commercial or public occurrence of SSD retention refresh;
- a claim that Rev. A has been directly inspected;
- a claim that an SSD must be periodically powered by an operator merely because it can perform powered retention work;
- a derivation of JESD218;
- a firmware reverse-engineering result;
- a controlled retention or power-cycle experiment.

---

## Source map

### P1 — Seagate Pulsar XT.2 SAS Product Manual, Rev. B, June 2011 — `H/P`

Seagate Technology, **_Pulsar XT.2 SAS Product Manual_**, publication `100647497`, Rev. B, June 2011:

<https://www.seagate.com/staticfiles/support/docs/manual/sas/100647497b.pdf>

The title and revision pages identify the document as `Pulsar XT.2 SAS`, publication `100647497`, Rev. B, June 2011. The revision table records Rev. A on 16 March 2011 as the initial release and Rev. B on 1 June 2011 as a change only to sheet 34 for a 7 mm weight correction.

The directly inspected Rev. B record establishes:

- the media is **Single Layer Cell (SLC) NAND Flash**;
- preventive maintenance is listed as not required;
- typical data retention with power removed at 40 °C is three months;
- while power is applied, firmware / hardware can monitor and refresh memory cells;
- §6.2.5 `Data Retention` says powered cells are monitored and rewritten if their levels decay unexpectedly;
- §6.3.2 says no routine scheduled preventive maintenance is required.

The relevant retention text is on printed pp. 14 and 16. Rev. B's revision table names only sheet 34 as changed from Rev. A.

### P2 — Seagate Pulsar.2 SAS Product Manual, Rev. C, March 2013 — `H/P-source-critical comparator`

Seagate Technology, **_Pulsar.2 SAS Product Manual_**, publication `100666271`, Rev. C, March 2013:

<https://www.seagate.com/files/www-content/product-content/pulsar-fam/pulsar/pulsar-2/en-us/docs/100666271c.pdf>

This later manual records:

- Rev. A — 11 August 2011 — initial release;
- Rev. B — 16 April 2012 — changes to a substantial page list including p. 14;
- Rev. C — 8 March 2013 — front cover and pp. 1–2.

The contents and body place `Data Retention` on printed p. 14 in this lineage. Therefore the Rev. B revision record itself blocks an unqualified inference that the inspected later wording was unchanged in Pulsar.2 Rev. A.

The same Rev. C manual identifies Pulsar.2 media as **Multi Layer Cell (MLC) NAND Flash** and retains the broad powered-monitoring / conditional-rewrite relation documented in the existing Case-111 evidence packet.

P2 is used here chiefly to discipline revision-history reasoning. It is not used to replace the already-grounded April-2012 Pulsar.2 evidence.

---

## Historical record

### H/P — June 2011 directly documents powered retention maintenance in a named enterprise SSD

The June-2011 Pulsar XT.2 manual is a direct first-party named-product witness. Its reliability material separates powered-off retention from powered controller behavior: the powered-off specification is stated under a temperature condition, while powered operation makes monitoring / refresh machinery available.

The manual's dedicated `Data Retention` subsection narrows the mechanism further. It does not merely use `refresh` as an undefined marketing word. It describes a conditional relation in which cell retention is monitored while powered and cells are rewritten when decay reaches an unexpected level.

The conservative direct historical statement is:

> **By June 2011, Seagate publicly documented a named enterprise SAS SSD whose powered controller behavior included cell-retention monitoring and conditional rewrite.**

This is a `documented-by` boundary, not an invention date.

### H/P — the same product says no routine scheduled preventive maintenance is required

Pulsar XT.2 simultaneously lists preventive maintenance as unnecessary and says no routine scheduled preventive maintenance is required.

That means the source itself places two forms of maintenance on different responsibility layers:

```text
operator-scheduled preventive maintenance
    -> not required by this manual

controller-local powered retention work
    -> explicitly documented
```

The historical counterexample is therefore earlier than the existing April-2012 Pulsar.2 witness:

```text
"no routine scheduled preventive maintenance"
    !=
"no internal maintenance"
```

### H/P — XT.2 is an SLC product witness

The same manual identifies the drive media as SLC NAND Flash. This matters only as a product descriptor and comparison guardrail.

It permits the bounded statement:

> powered controller-local retention monitoring / conditional rewrite was documented for this named SLC enterprise SSD.

It does **not** permit the statement that SLC as a class requires or implements one universal refresh algorithm.

### H/P-revision — Seagate's revision table supports a March-2011 continuity inference, not direct inspection

The Rev. B document says Rev. A was the 16-March-2011 initial release and that the 1-June-2011 Rev. B change affected only sheet 34 for a weight correction. The retention passages inspected in Rev. B are on printed pp. 14 and 16.

On the face of that vendor revision record, those pages were not listed among the Rev. B changes. It is therefore reasonable to record a **revision-history-supported inference** that the same retention passages belonged to the Rev. A document lineage.

But the evidential categories must remain separate:

```text
directly inspected Rev. B wording — June 2011
    !=
revision-history-supported Rev. A continuity — March 2011
    !=
first invention / first implementation
```

A direct Rev. A facsimile would be required to collapse the first two categories.

### H/P-source-critical — Pulsar.2 shows why revision tables cannot always justify back-projection

The later Pulsar.2 revision table is an important counterexample to casual continuity reasoning. It records an August-2011 Rev. A initial release, then says the April-2012 Rev. B changed several pages including p. 14. In the inspected later manual, `Data Retention` is on p. 14.

Therefore:

> **the April-2012/2013 Pulsar.2 retention wording cannot be treated as direct evidence for August 2011 merely because Rev. A existed.**

This is a negative source-critical result. It does not prove that Pulsar.2 Rev. A lacked powered retention monitoring; it proves only that the surviving revision history does not warrant unchanged-wording back-projection for the relevant page.

### H/P-comparison — broad wording spans SLC XT.2 and later MLC Pulsar.2 documentation

Pulsar XT.2 identifies SLC NAND; Pulsar.2 identifies MLC NAND. Both surviving first-party manuals document the broad relation:

```text
power applied
    -> cell-retention monitoring available
    -> conditional rewrite / refresh behavior
```

This broad cross-product documentation continuity is historical evidence about what Seagate publicly described. It is **not** evidence of identical controller internals or direct technical descent.

---

## Engineering reconstruction

The following terms are project reconstructions unless explicitly attributed to Seagate.

### E — passive offline survival and active powered renewal are distinct regimes

The XT.2 manual separately gives a powered-off retention characteristic and powered monitoring / rewrite behavior.

A retention model faithful to the source therefore needs at least two regimes:

```text
unpowered interval
    -> controller maintenance unavailable
    -> stored charge must remain recoverable within the product condition

powered interval
    -> controller can inspect retention condition
    -> conditional rewrite can renew vulnerable state
```

`nonvolatile` consequently does not mean `maintenance-free under every power regime`.

### E — power is an enabling condition, not completion evidence

XT.2 documents what becomes possible while powered but provides no host-visible `retention maintenance complete` bit, minimum powered dwell, whole-device coverage counter, or proof that every vulnerable cell has already been examined after a given power-on interval.

Thus:

```text
power restored
    -> retention-maintenance opportunity exists
    !=
retention maintenance proven complete
```

The later IBM/Dell/ESS evidence in Case 111 adds operator dwell times and one system-level scrub-completion witness; it must not be projected backward into XT.2.

### E — monitoring and rewrite are different stages

The XT.2 subsection describes monitoring first and rewrite only when a decay condition is met. The defensible reconstruction is:

```text
powered cell
    -> observe / qualify retention condition
    -> threshold condition?
        -> conditional rewrite
```

This rejects several shortcuts:

- powered operation does not imply continuous rewriting;
- every host read is not thereby a documented refresh trigger;
- every cell is not shown to be rewritten on every maintenance pass;
- `refresh` in the reliability footnote is not enough to infer a disclosed page-selection algorithm.

### E — revision history itself is retained evidence with a different authority level

A revision table is not the same artifact as an earlier revision. It can constrain what probably changed without reproducing every byte of the predecessor.

For XT.2:

```text
Rev. B direct text
    + vendor statement that only sheet 34 changed
    + retention passages outside sheet 34
        -> strong continuity inference
```

For Pulsar.2:

```text
Rev. B change list includes retention page 14
    -> unchanged-wording inference to Rev. A is not licensed
```

This distinction is useful beyond this case: **revision metadata can support or weaken historical continuity claims, but it is not automatically a substitute for the missing revision.**

### E — same broad behavior across SLC and MLC products does not identify one mechanism

The XT.2/Pulsar.2 pair supports a product-documentation category — powered retention monitoring plus conditional rewrite — across two media descriptions. It does not identify:

- the measured physical signal;
- ECC-margin or voltage-threshold policy;
- sampling cadence;
- rewrite placement;
- whether data is rewritten in place or remapped;
- controller family;
- firmware code lineage;
- identical failure handling.

Therefore:

```text
same vendor-level retention contract
    !=
same implementation
```

---

## Functional comparison

### Case 76 — JESD218 SSD endurance / retention qualification

XT.2 references JESD218 in its endurance material while separately describing product-local retention monitoring / rewrite. Functionally:

```text
qualification relation
    !=
autonomous maintenance mechanism
```

The standard-level retention requirement does not, by itself, identify XT.2's controller algorithm.

### Case 37 — Samsung 840 EVO old-data refresh

Case 37 documents a later client-SSD episode in which powered periodic refresh was described in relation to old-data read performance. XT.2 is an earlier enterprise-SAS product witness, but no direct genealogy or algorithm identity is established.

The bounded functional comparison is only:

```text
powered controller work can renew NAND-resident state
```

The symptom framing, NAND class, controller, thresholds, cadence, and public product context differ or remain undisclosed.

### Case 36 — Flash Correct-and-Refresh

Academic FCR uses explicit ECC/error-margin logic in a research design. XT.2's public manual does not disclose that algorithm. `monitor`, `refresh`, `rewrite`, and academic `correct-and-refresh` must remain distinct historical terms unless a source establishes implementation identity.

### Case 111 later operator runbooks

XT.2 places the documented maintenance responsibility inside the device while saying routine scheduled preventive maintenance is not required. IBM/Dell later add explicit operator-facing extended-shutdown schedules.

Functionally:

```text
device-local autonomous maintenance capability
    !=
operator maintenance cadence
```

No causal genealogy is asserted from the 2011 Seagate product to the 2020s field runbooks.

---

## Prior art and chronology boundary

This slice changes the repository's bounded chronology in one way:

> **the directly inspected named enterprise-SSD product witness for powered retention monitoring / conditional rewrite moves from April 2012 to June 2011.**

The XT.2 revision table also supplies a plausible earlier **16-March-2011 revision-lineage floor**, because Rev. B identifies only sheet 34 as changed while the relevant passages are on pp. 14 and 16. That is recorded as a revision-history inference, not direct inspection.

This slice does **not** establish:

- first invention;
- first patent disclosure;
- first shipment;
- first controller implementation;
- first use of `refresh` for SSD retention;
- a Seagate-origin genealogy for later vendor behavior.

The Pulsar.2 revision table simultaneously narrows another prior claim: the existence of an August-2011 Rev. A cannot be used by itself to move the inspected Pulsar.2 wording backward, because its April-2012 Rev. B explicitly changed the page carrying the retention section.

---

## Philosophical interpretation

The technical fact that matters conceptually is not simply that NAND is nonvolatile. The XT.2 manual documents a substrate that can retain state without power while also depending, when power is present, on hidden controller work that can inspect and renew that state.

A limited interpretation is therefore:

> **quiescent survival and active preservation can coexist in the same storage object without occupying the same time or responsibility layer.**

The `no routine scheduled preventive maintenance` wording makes that division especially visible: human-visible maintenance burden can be absent while machine-local maintenance remains active.

This is a project interpretation, not Seagate's philosophical vocabulary. It does not make every SSD background task a form of `memory`, `archive`, or `care`, and it does not imply that powered autonomy guarantees indefinite retention.

---

## Explicit non-claims

This packet does **not** claim that:

1. XT.2 invented SSD retention refresh;
2. June 2011 is the first public disclosure of such behavior;
3. March 2011 is directly inspected wording;
4. the vendor revision table is byte-for-byte proof of Rev. A;
5. Pulsar.2 Rev. A lacked retention monitoring;
6. Pulsar.2 Rev. B's later wording was necessarily absent from Rev. A;
7. XT.2 and Pulsar.2 use the same controller;
8. XT.2 and Pulsar.2 use the same firmware;
9. SLC and MLC require the same refresh thresholds;
10. every Seagate SSD implements the same policy;
11. every enterprise SSD performs powered refresh;
12. every powered period completes retention maintenance;
13. every host read triggers a rewrite;
14. every rewrite preserves the same physical page;
15. the manual discloses physical threshold sensing or ECC-margin policy;
16. the three-month figure is a deterministic failure instant;
17. `no preventive maintenance required` means no internal maintenance occurs;
18. XT.2 required an IBM/Dell-style periodic power-up runbook;
19. JESD218 prescribes XT.2's controller algorithm;
20. later Seagate, Samsung, IBM, Dell, or NetApp behavior descends directly from XT.2.

---

## Claim ledger

| Claim | Type | Evidence strength | Boundary |
| --- | --- | --- | --- |
| Pulsar XT.2 Rev. B is a June-2011 named enterprise-SAS SSD manual | H/P | strong | direct first-party document |
| XT.2 uses SLC NAND Flash | H/P | strong | named product only |
| XT.2 gives a typical three-month powered-off retention figure at 40 °C | H/P | strong | product condition, not deterministic failure time |
| XT.2 says powered firmware / hardware can monitor and refresh memory cells | H/P | strong | internal method undisclosed |
| XT.2 §6.2.5 says powered cell retention is monitored and conditionally rewritten | H/P | strong | threshold/cadence/geometry undisclosed |
| XT.2 says no routine scheduled preventive maintenance is required | H/P | strong | operator burden, not absence of internal work |
| `no scheduled PM = no internal maintenance` | X | rejected | contradicted inside the same manual |
| Rev. A is recorded as 16 March 2011; Rev. B says only sheet 34 changed | H/P | strong | revision-history fact |
| XT.2 retention passages therefore likely continue from Rev. A | H/E | medium-strong | revision-history inference; Rev. A not directly inspected |
| June-2011 direct wording = March-2011 direct wording | X | rejected | evidence categories remain distinct |
| Pulsar.2 Rev. B changed p. 14, where Data Retention resides | H/P | strong | blocks unchanged-page back-projection |
| Pulsar.2 Rev. A therefore lacked the feature | X | rejected | change list does not establish absence |
| later Pulsar.2 uses MLC NAND while retaining broad powered-monitor/rewrite wording | H/P | strong | documentation-level comparison only |
| same broad SLC/MLC wording = same firmware algorithm | X | rejected | implementation identity not established |
| power applied = maintenance complete | X | rejected | no XT.2 completion telemetry or dwell contract |
| direct product witness floor moves from April 2012 to June 2011 | H | strong | bounded inspected-source floor, not priority |
| March-2011 revision-lineage inference = invention date | X | rejected | chronology categories are different |

---

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Pulsar XT.2` found no dedicated packet to reuse.

This repository therefore keeps only the retention-specific seam:

```text
powered-off survival
    !=
powered controller maintenance opportunity
    !=
conditional renewal
    !=
operator-scheduled maintenance
    !=
maintenance completion evidence
```

A broad Seagate enterprise-SSD product genealogy, Pulsar controller history, SLC/MLC platform evolution, SAS ecosystem history, shipment chronology, firmware archaeology, and influence genealogy belong primarily in `computing-archaeology` rather than being duplicated here.

---

## Remaining evidence debt

The bounded slice is complete, but several narrower questions remain:

- obtain a direct Pulsar XT.2 Rev. A (16 March 2011) facsimile and compare the retention passages byte-for-byte or page-for-page with Rev. B;
- obtain a direct Pulsar.2 Rev. A (11 August 2011) facsimile and determine what changed on the retention-bearing p. 14 in Rev. B;
- search earlier enterprise-SSD manuals for a pre-March-2011 named-product powered-retention contract;
- identify whether Seagate published controller-level telemetry, error-threshold, or maintenance-completion evidence for XT.2;
- keep product-document chronology separate from shipment, implementation, and patent genealogy;
- validate named-device behavior experimentally only in a separate fault/retention-testing slice.

---

## Sources

- Seagate Technology, **_Pulsar XT.2 SAS Product Manual_**, publication `100647497`, Rev. B, June 2011: <https://www.seagate.com/staticfiles/support/docs/manual/sas/100647497b.pdf>.
- Seagate Technology, **_Pulsar.2 SAS Product Manual_**, publication `100666271`, Rev. C, March 2013: <https://www.seagate.com/files/www-content/product-content/pulsar-fam/pulsar/pulsar-2/en-us/docs/100666271c.pdf>.
- Internal predecessor evidence: [`111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md`](111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md).
- Internal standards context: [`../cases/76-jedec-ssd-endurance-retention-qualification.md`](../cases/76-jedec-ssd-endurance-retention-qualification.md).
- Internal commercial-refresh comparison: [`../cases/37-samsung-840-evo-old-data-performance-refresh.md`](../cases/37-samsung-840-evo-old-data-performance-refresh.md).
