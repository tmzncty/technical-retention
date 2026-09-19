# Evidence 111E — Seagate Pulsar.2 2012 powered retention-refresh prior-art deepening

**Status:** `bounded deepening complete`

## Scope

This record deepens one narrow part of Case 111:

> before the surviving 2020–2026 IBM / Dell extended-shutdown runbooks turned enterprise-SSD retention into an explicit operator scheduling problem, did a named enterprise SSD already document controller-local retention maintenance that exists only while power is applied?

For the inspected Seagate record, the answer is **yes by April 2012**.

The primary anchor is Seagate's **Pulsar.2 SAS Product Manual, Rev. B, April 2012**. The manual gives a typical powered-off retention figure, explicitly says firmware / hardware can monitor and refresh memory cells while power is applied, and then states more specifically that powered cells are monitored and rewritten if their levels decay unexpectedly. The same manual says both `Preventive maintenance: None required` and `No routine scheduled preventive maintenance is required`.

That combination is useful because it makes a distinction that later field runbooks can easily obscure:

```text
no routine operator-scheduled preventive maintenance
    !=
no controller-local retention maintenance
```

A later Seagate **1200.2 SAS SSD Product Manual, Rev. D, October 2016** repeats the same broad product contract. It is used only as a continuity witness, not as proof of identical firmware or algorithm.

This slice is about:

- power-state dependence of controller-local retention work;
- product-level autonomous monitoring / rewrite;
- the difference between hidden device maintenance and operator scheduling;
- the historical floor of a named enterprise-SSD product witness inside Case 111.

It is **not**:

- an invention-priority claim for SSD refresh;
- a history of the Pulsar product family;
- a claim that every enterprise SSD behaves this way;
- a derivation of JESD218;
- a claim that the Seagate product required IBM/Dell-style periodic power-up scheduling;
- a firmware reverse-engineering result;
- a fault-injection or long-duration retention experiment.

---

## Source map

### P1 — Seagate Pulsar.2 SAS Product Manual, Rev. B, April 2012 — `H/P`

Seagate Technology, **_Pulsar.2 SAS Product Manual_**, publication `100666271`, Rev. B, April 2012:

<https://www.seagate.com/files/www-content/product-content/pulsar-fam/pulsar/pulsar-2/en-us/docs/100666271b.pdf>

The title page identifies:

- `Pulsar.2 SAS`;
- publication number `100666271`;
- `Rev. B`;
- `April 2012`.

The revision history records Rev. A as an August 2011 initial release and Rev. B as `04/16/12`. This evidence packet uses **April 2012** as the direct wording floor because the Rev. B text was inspected. It does not back-project the inspected retention wording into Rev. A.

In the reliability section the manual states, in substance:

- NAND retention degrades with program/erase use;
- storage temperature affects powered-off retention;
- while power is applied, the SSD contains firmware and hardware features able to monitor and refresh memory cells;
- `Preventive maintenance: None required`;
- typical data retention with power removed at 40 °C: `3 months`.

Section `6.2.5 Data Retention` is more specific: while powered, retention of SSD cells is monitored and cells are rewritten if their levels decay to an unexpected level; powered-off retention depends on P/E cycles and storage temperature.

Section `6.3.2 Preventive maintenance` separately states:

> `No routine scheduled preventive maintenance is required.`

The wording is important because it places **internal autonomous work** and **operator maintenance burden** on different axes.

### P2 — Seagate 1200.2 SAS SSD Product Manual, Rev. D, October 2016 — `H/P-continuity`

Seagate Technology, **_1200.2 SAS SSD Product Manual_**, Rev. D, October 2016:

<https://www.seagate.com/content/dam/seagate/migrated-assets/www-content/product-content/ssd-fam/1200-ssd/en-us/docs/1200-2-sas-ssd-product-manual-100773817d.pdf>

The manual again records:

- `Preventive maintenance: None required`;
- typical powered-off retention of three months at 40 °C up to the specified endurance condition;
- firmware / hardware monitoring and refreshing of cells while power is applied;
- a Data Retention section in which powered cell state is monitored and rewritten when decay reaches an unexpected level;
- no routine scheduled preventive maintenance requirement.

This is a later first-party continuity witness for the broad **powered autonomous retention-maintenance** relation. It does not prove that Pulsar.2 and 1200.2 share firmware, thresholds, data structures, NAND generation, or exact scheduling policy.

---

## Historical record

### H/P — by April 2012 a named enterprise SSD documented powered autonomous retention work

The April 2012 Pulsar.2 manual is explicit that the drive has firmware and hardware able to monitor and refresh memory cells when power is applied.

That is already stronger than the generic statement `NAND is nonvolatile`: the product documentation makes power availability part of the device's active retention-management capability.

A conservative historical statement is therefore:

> **By April 2012, Seagate publicly documented a named enterprise SAS SSD whose firmware / hardware could monitor and refresh NAND cells while the SSD was powered.**

This is a `documented-by` boundary, not an invention date.

### H/P — the same manual distinguishes powered-off retention from powered maintenance

The same reliability table gives a typical powered-off retention value of **three months at 40 °C** while its footnote says that powered operation enables monitoring / refreshing.

The source itself therefore separates two regimes:

```text
power removed
    -> passive retention interval under stated product conditions

power applied
    -> controller-local monitoring / refresh capability available
```

The manual does not say that the powered-off interval is a deterministic failure instant for an individual drive.

### H/P — `Data Retention` is an explicit controller algorithm concern

The Pulsar.2 manual's Endurance Management section lists `Data Retention` alongside Wear Leveling, Garbage Collection, Write Amplification, UNMAP, and Lifetime Endurance Management.

Section `6.2.5` then states that while the drive is powered, SSD-cell retention is monitored and cells are rewritten if levels decay unexpectedly.

This supports a narrower mechanism statement than `the drive refreshes continuously`:

> **the documented controller behavior is conditional monitoring plus rewrite when a decay condition is reached.**

The threshold, cadence, measurement method, physical-page selection rule, and rewrite placement are not disclosed in the inspected manual.

### H/P — `no preventive maintenance required` does not mean `no maintenance occurs`

The reliability table says `Preventive maintenance: None required`, and section `6.3.2` says no routine scheduled preventive maintenance is required. In the same manual, however, retention monitoring / rewrite, wear leveling, and garbage collection are explicitly described as internal drive functions.

The only source-consistent reading is that the preventive-maintenance statement concerns **routine scheduled operator intervention**, not the absence of internal controller maintenance.

Therefore:

```text
no scheduled user maintenance
    !=
no maintenance state machine inside the SSD
```

This is a particularly useful historical counterexample to treating `maintenance-free` product language as evidence of passive media behavior.

### H/P-continuity — the broad contract survives in Seagate documentation by 2016

The October 2016 Seagate 1200.2 manual repeats the same broad pairing: a powered-off retention specification, controller-side powered monitoring / refresh, and no routine scheduled preventive maintenance.

That later record supports continuity of the **documentation-level distinction** within Seagate's enterprise SSD literature. It does not establish one unbroken firmware lineage.

---

## Engineering reconstruction

The following terms are project reconstruction unless explicitly attributed to Seagate.

### E — product retention qualification and powered maintenance are different relations

The Pulsar.2 documentation can be reconstructed as two related but non-identical relations:

```text
powered-off retention characteristic
    -> how long programmed state is expected to remain recoverable
       under stated product / temperature / endurance conditions

powered controller-local maintenance
    -> monitoring and conditional rewrite while the SSD has power
```

One cannot be substituted for the other.

The powered-off figure does not describe a refresh schedule, and the existence of powered refresh does not erase the need for a powered-off retention specification.

### E — power availability is an enabling condition, not completion evidence

The manual says the relevant firmware / hardware features operate when power is applied. It does **not** give a completion bit, host-visible progress counter, minimum dwell time, or proof that every vulnerable cell has already been examined after an arbitrary power-on interval.

Therefore:

```text
power applied
    -> maintenance machinery can operate
    !=
all retention maintenance completed
```

This becomes important when compared with later IBM/Dell runbooks, which explicitly allocate powered dwell time or system-level scrub completion evidence.

### E — monitoring and rewriting should remain distinct

Section 6.2.5 says powered cell retention is monitored and cells are rewritten **if** levels decay unexpectedly.

The safe reconstruction is:

```text
powered cell state
    -> monitor / qualify
    -> decay condition reached?
        -> if yes, rewrite / refresh action
        -> if no, no rewrite implied by this source
```

Thus:

- `monitoring != rewriting every cell`;
- `power applied != continuous rewrite`;
- `one read != documented refresh trigger`;
- `refresh capability != disclosed algorithm`.

### E — operator maintenance and autonomous maintenance are different responsibility loci

Case 111's later IBM/Dell documents move part of the retention problem into an operator runbook: keep the system within environmental constraints, restore power on a schedule, allow sufficient powered time, perform a read sweep, or observe a system-level scrub completion message.

Pulsar.2 exposes an earlier product-level locus:

```text
device firmware / hardware
    owns monitoring + conditional rewrite while powered

operator
    has no routine scheduled preventive-maintenance task in this manual
```

That is not a contradiction. It is a division of maintenance responsibility.

### E — hidden autonomy can later become an infrastructure dependency

A device can be marketed/documented as requiring no routine scheduled preventive maintenance while still depending on powered controller work. Once a deployment keeps the device powered off for long periods, that hidden assumption can become operationally visible.

This is a functional reconstruction, not evidence that Seagate's 2012 manual caused IBM or Dell's later field policies.

---

## Cross-case comparison

### Case 76 — JESD218 SSD retention qualification

Case 76 grounds a standards-level endurance / retention qualification relation. Pulsar.2 cites JESD218 in its endurance discussion and separately exposes a product implementation-level distinction between powered-off retention and powered controller maintenance.

Functional relation:

```text
standards qualification relation
    !=
named-product autonomous maintenance mechanism
```

No claim is made that the Pulsar.2 manual fully discloses its JESD218 test setup or that its controller algorithm is prescribed by JESD218.

### Case 37 — Samsung 840 EVO old-data refresh

Case 37 is a 2014–2015 named client-SSD episode in which Samsung addressed old-data read-performance degradation with a powered periodic refresh feature.

Pulsar.2 gives an earlier enterprise-SSD product witness for powered monitoring / conditional rewrite, but the two cases must not be collapsed:

- different vendors and product classes;
- different disclosed motivation / symptom framing;
- different documentation;
- no demonstrated genealogy;
- no proof of the same threshold or scheduler.

The bounded common function is only:

> **power can enable controller-local work that renews or protects the recoverability of NAND-resident state.**

### Case 36 — Flash Correct-and-Refresh

Case 36 studies an academic mechanism that uses ECC-related evidence to drive correction/refresh. The Pulsar.2 manual does not disclose its monitoring metric or prove FCR adoption.

`monitor and refresh memory cells` is therefore **not** translated into `implements FCR`.

### Case 111 — later IBM / Dell operator runbooks

The historical value of the Seagate witness is not that it pushes the IBM/Dell **operator-cadence** chronology back to 2012. It does not.

Instead it inserts an earlier layer:

```text
by Apr 2012
    named enterprise SSD:
    controller-local powered monitor + conditional rewrite
    no routine scheduled preventive maintenance required

by Dec 2020 and later
    system/vendor runbooks:
    extended power-off -> explicit operator intervention schedule,
    powered dwell / scrub / read-triggered maintenance guidance
```

Thus:

> **device-local autonomous maintenance predates the currently grounded operator-runbook layer, but autonomous maintenance is not the same historical object as an operator cadence.**

---

## Functional analogy

A bounded analogy is possible with other systems where a lower layer performs maintenance without ordinary user intervention. What appears `maintenance-free` at one interface can contain automatic maintenance work below that interface.

The analogy stops there. This evidence does not make SSD retention refresh equivalent to DRAM refresh, RAID scrub, filesystem garbage collection, or distributed repair.

---

## Philosophical interpretation — bounded

`I` — `nonvolatile` does not imply `maintenance-free`. A medium can preserve state without power for a bounded interval while the product also uses powered observation and rewrite to renew that state when energy and controller execution are available.

`I` — maintenance can be hidden by an interface. `No routine scheduled preventive maintenance` is compatible with substantial autonomous retention work below the user-visible maintenance boundary.

`I` — later operator runbooks make that hidden dependency organizationally visible when long shutdown removes the device's opportunity to perform the same broad class of retention work.

These are project interpretations. Seagate does not present them as philosophical claims, and no genealogy from Seagate to IBM/Dell is asserted.

---

## Explicit non-claims

This evidence does **not** establish that:

1. Seagate invented SSD refresh or data-retention maintenance.
2. the August 2011 Rev. A manual contained the exact Rev. B retention wording inspected here.
3. every Pulsar.2 cell is continuously scanned while powered.
4. every monitoring event causes a rewrite.
5. the manual discloses the decay threshold, cadence, sampling policy, ECC metric, or data structure used for monitoring.
6. `refresh` necessarily means an in-place NAND reprogram rather than relocation / rewritten physical embodiment.
7. the host can observe individual refresh operations or their completion.
8. simply applying power proves maintenance completion.
9. Pulsar.2 requires periodic operator power-up at an IBM/Dell-style cadence.
10. three months at 40 °C is a deterministic failure instant for each unit.
11. no routine scheduled preventive maintenance means no internal maintenance occurs.
12. powered refresh continues unchanged through every SAS low-power state.
13. Seagate's internal monitoring is triggered by a host full-device read.
14. Pulsar.2 implements the academic Flash Correct-and-Refresh algorithm.
15. Pulsar.2 and Samsung 840 EVO use the same mechanism.
16. Pulsar.2 and Seagate 1200.2 use identical firmware, NAND, thresholds, or scheduler.
17. the 2016 continuity witness establishes uninterrupted implementation genealogy from 2012.
18. Seagate's 2012 product documentation caused or directly influenced IBM/Dell's 2020–2026 runbooks.
19. a retention refresh is equivalent to RAID/system scrub completion.
20. retention maintenance is a sanitization mechanism.

---

## Claim ledger

| Claim | Type | Evidence strength | Boundary |
| --- | --- | --- | --- |
| Pulsar.2 Rev. B is a Seagate product manual dated April 2012 | `H/P` | strong | publication/document floor, not invention date |
| Pulsar.2 documents a typical three-month powered-off retention value at 40 °C | `H/P` | strong | bounded product specification; not deterministic failure clock |
| Pulsar.2 says firmware / hardware can monitor and refresh memory cells while power is applied | `H/P` | strong | exact algorithm / cadence undisclosed |
| Pulsar.2 says powered cell retention is monitored and cells are rewritten if levels decay unexpectedly | `H/P` | strong | conditional behavior; not continuous whole-drive rewrite |
| Pulsar.2 says no routine scheduled preventive maintenance is required | `H/P` | strong | operator-facing requirement; does not negate internal maintenance |
| no scheduled preventive maintenance = no retention maintenance | `X` | rejected | contradicted by the same manual's internal monitoring / rewrite description |
| power applied = all retention maintenance complete | `X` | rejected | no completion telemetry or minimum dwell contract in inspected source |
| Seagate 1200.2 Rev. D repeats the broad powered-monitor/rewrite contract by Oct 2016 | `H/P-continuity` | strong | documentation continuity, not common firmware proof |
| device-local autonomous maintenance = later operator shutdown cadence | `X` | rejected | different responsibility and evidence layers |
| 2012 Seagate witness proves direct genealogy to Samsung/IBM/Dell | `X` | rejected | chronology / functional similarity only |

---

## Prior-art and chronology boundary

The conservative chronology for this slice is:

```text
April 2012
    Seagate Pulsar.2 Rev. B:
    powered controller-local monitoring / conditional refresh-rewrite
    + no routine scheduled preventive maintenance requirement

2014–2015
    Case 37 Samsung 840 EVO:
    named product episode around powered periodic refresh / old-data performance

October 2016
    Seagate 1200.2 Rev. D:
    later continuity witness for powered monitoring / rewrite wording

December 2020 onward
    Case 111 IBM / Lenovo / Dell / NetApp records:
    operator cadence, system scrub, wear-state admission, powered dwell,
    and read-triggered field-maintenance guidance
```

This chronology shows different evidence layers. It does not establish ancestry among them.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Pulsar.2` and `Seagate data retention SSD` found no dedicated packet to reuse. Broad Pulsar / Seagate enterprise-SSD product genealogy, controller architecture, NAND generation, firmware history, adoption, and standards implementation belong primarily there if pursued. This evidence keeps only the retention-specific seam:

```text
powered-off survival
    !=
powered controller-local monitor / conditional rewrite
    !=
operator maintenance cadence
    !=
maintenance-completion evidence
```

---

## Remaining evidence debt

This slice closes the narrow question whether a named enterprise SSD exposed powered autonomous retention work before the 2020 operator-runbook layer. It leaves open:

- the first Seagate product/manual to use this exact powered-retention wording;
- whether Rev. A (August 2011) already contained the same text;
- the internal metric and threshold used by Pulsar.2 for decay detection;
- whether maintenance progress / completion was externally observable;
- how the behavior interacted with SAS power-management states;
- independent experimental validation under long powered-off intervals;
- additional vendors with dated product-level powered retention-refresh disclosures before 2012;
- the first first-party operator runbook that turns autonomous enterprise-SSD retention work into an explicit periodic long-shutdown power-up schedule.
