# Evidence 111 — Hitachi / HGST FlashMAX Periodic Power-On Guidance, 2014–2016

## Status

**`bounded deepening complete`** for one narrow question:

> Can Case 111 ground a genuinely separate pre-IBM/Dell vendor witness in which enterprise Flash storage is given an explicit periodic power-on instruction during storage, while keeping the retention specification, the operator cadence, the power-on duration, and actual maintenance completion separate?

The answer is **yes, with an important limit**. Surviving Hitachi Data Systems / Hitachi user-guide revisions for HGST PCIe Flash Drive FlashMAX2&3 tell operators to turn on the server once every three months even when the device is stored. The same guide gives a wear-dependent maximum-power-off table whose shortest row is three months at zero remaining write capacity. A contemporaneous HGST product datasheet separately states three-month retention at 40 °C at end of life.

However, the inspected documentation does **not** state how long the server must remain powered, does not identify a retention-refresh algorithm, and does not expose a completion signal for whatever device-local work may or may not occur after power-on.

This closes the prior Case 111 gap for an independent **periodic-power-up instruction**, but it does **not** close the narrower gap for an independent IBM/Dell-like **minimum powered-duration + completion semantics** witness.

---

## Scope

### Object

The bounded object is the **HGST PCIe Flash Drive / FlashMAX2&3** product family as documented in Hitachi Data Systems / Hitachi user guides and an HGST manufacturer datasheet.

The surviving product guide covers 1.1 TB, 2.2 TB, and 4.8 TB PCIe Flash Drive variants and identifies them as SSDs installed in a server PCIe slot.

### Time boundary

Three surviving manufacturer/vendor records are useful here:

1. Hitachi document **MK-99COM145-00**, _PCIe Flash Drive FlashMAX2&3 User's Guide_, copyright line ending **2014**;
2. HGST datasheet **DS24-EN-US-0815-05**, produced **May 2015** and revised **August 2015**;
3. Hitachi document **MK-99COM145-03**, _PCIe Flash Drive FlashMAX2&3 User's Guide_, copyright line ending **2016**.

The copyright endpoint on the Hitachi manuals is used only as a bounded document-era marker. It is **not** treated as an exact first-publication date unless a revision ledger or release record is recovered later.

### Research question

The narrow question is not “how does FlashMAX firmware refresh NAND?” The sources inspected here do not answer that.

The question is instead:

> What does the surviving product documentation require the operator to do about long unpowered storage, and which conclusions about maintenance can and cannot be inferred from that instruction?

---

## Source 1 — Hitachi MK-99COM145-00

**Document:** _PCIe Flash Drive FlashMAX2&3 User's Guide_

**Document number:** `MK-99COM145-00`

**Current surviving vendor-hosted PDF:**
<https://download.hitachivantara.com/download/epcra/com1450.pdf>

### Provenance observed

The PDF identifies Hitachi, Ltd. copyright through 2014 and says the document applies to the PCIe Flash Drive Series. It is hosted today on Hitachi Vantara infrastructure. The guide's product overview identifies 1.1 TB, 2.2 TB, and 4.8 TB PCIe Flash Drive models and describes the device as an SSD installed in a server PCIe slot.

This is therefore treated as **vendor product documentation**, not a third-party summary.

### Historical record — endurance state is separately operator-visible

The guide gives maximum rewrite capacities for the three listed capacities and says remaining rewrite capacity should be monitored so data can be migrated and the device replaced before the maximum is reached.

It further says that, when maximum rewrite capacity is reached, the Flash Drive enters a rewrite-suppression / read-only mode.

The same guide exposes a `Remaining Life` value through `vgc-monitor`.

For this case, the important point is only that **wear/endurance state is a separately represented operational quantity**. It is not collapsed into calendar age.

### Historical record — retention is explicitly wear-conditioned

Under `Retention (maximum power-off duration) specification`, the guide provides this relation:

| Remaining write capacity | 90% | 67% | 50% | 0% |
| --- | ---: | ---: | ---: | ---: |
| Maximum power-off duration | 5 years | 18 months | 9 months | 3 months |

The guide explains that the duration for which data can be kept without power becomes shorter as remaining write capacity decreases.

This is a direct product-level statement that:

```text
power-off retention allowance
    is conditioned by wear / remaining rewrite capacity
```

It does **not** mean every individual card will fail exactly at one table boundary.

### Historical record — one operator cadence is prescribed across storage

Immediately after the wear-conditioned table, the guide tells the operator, in substance, to **turn on the server once every three months even while the device is stored**.

That is the key witness for this deepening.

The manual therefore places side by side:

```text
wear-dependent maximum-power-off table
    90% remaining -> 5 years
    67% remaining -> 18 months
    50% remaining -> 9 months
    0% remaining  -> 3 months

operator storage instruction
    -> power on server once every 3 months
```

The historical record supports the coexistence of those two relations. The source does not explain the engineering derivation of the cadence.

### Historical record — backup remains a separate protection relation

The same page separately advises regular backup to auxiliary storage because all data may be lost if the Flash Drive is damaged.

That blocks another shortcut:

```text
periodic power-on policy
    != backup policy
    != proof against all device-failure modes
```

### Historical record — restart integrity checking is separately scoped

The guide also describes an integrity check after an **unanticipated shutdown**, with data access unavailable until that check completes.

That mechanism is textually separate from the stored-device periodic power-on instruction.

The page does **not** say that the periodic three-month storage power-on is performed in order to trigger that unanticipated-shutdown integrity check.

Therefore:

```text
periodic storage power-on
    != automatically the documented unexpected-shutdown integrity check
```

---

## Source 2 — HGST DS24-EN-US-0815-05

**Document:** _FlashMAX PCIe — Enterprise Solid-State Drives_ datasheet

**Document identifier:** `DS24-EN-US-0815-05`

**Manufacturer-hosted surviving PDF:**
<https://documents.westerndigital.com/content/dam/doc-library/en_us/assets/public/western-digital/product/hgst/general-docs/data-sheet-flashmax-pcie.pdf>

### Publication metadata observed

The datasheet states:

- © 2015 HGST, Inc.;
- produced `5/15`;
- revised `8/15`.

It lists FlashMAX III and FlashMAX II Capacity model/part numbers, capacities, endurance, operating temperatures, and reliability properties.

### Historical record — product-level EOL retention contract

For both FlashMAX III and FlashMAX II Capacity, the environmental/specification table gives:

```text
JEDEC compliance
    -> 3-month retention at 40 °C at EOL
```

This independently corroborates that the three-month end-of-life retention condition belonged to the FlashMAX product contract around the same product era.

The datasheet does **not** itself state the every-three-month server power-on instruction. That instruction is grounded in the Hitachi user guide.

This source separation matters:

```text
product retention specification
    != operator storage runbook
```

Even when the two use the same three-month number, they are not the same kind of statement.

### Historical record — wear leveling exists, but its relation to storage power-on is undisclosed

The HGST datasheet says FlashMAX with vFAS performs global and local wear leveling and may relocate data to less-used Flash locations.

That is useful product context but **not** evidence that the periodic stored-device power-on triggers a particular wear-leveling or refresh pass.

No causal bridge is supplied in the inspected source.

---

## Source 3 — Hitachi MK-99COM145-03

**Document:** _PCIe Flash Drive FlashMAX2&3 User's Guide_

**Document number:** `MK-99COM145-03`

**Current surviving vendor-hosted PDF:**
<https://download.hitachivantara.com/download/epcra/com1453.pdf>

### Provenance observed

The surviving revision identifies copyright through 2016 and extends the supported host environment to include VMware vSphere ESXi in addition to Windows Server and RHEL.

### Historical record — the retention table and power-on cadence survive a later revision

Revision `-03` preserves the same four-row retention relation:

- 90% remaining write capacity -> 5 years;
- 67% -> 18 months;
- 50% -> 9 months;
- 0% -> 3 months.

It also preserves the instruction to turn on the server once every three months while the device is stored.

This provides revision continuity for the **documented operational rule**. It does not prove that firmware behavior was unchanged between all intermediate revisions or that every FlashMAX SKU shared byte-identical controller code.

---

## Engineering reconstruction

### E — one operator cadence can sit above a wear-dependent retention table

The most useful relation in the source is not merely “three months.” It is the mismatch in dimensionality between the table and the runbook:

```text
physical/product condition:
    remaining write capacity varies

specified maximum-power-off duration:
    varies from years to months

operator storage cadence:
    one recurring three-month power-on instruction
```

Therefore:

> **wear-conditioned retention allowance != a maintenance schedule that must vary one-for-one with wear state**.

The guide's one cadence coexists with four retention rows. That is a directly observable documentation relation.

A plausible engineering reading is that a single conservative runbook is easier to operate than a schedule continuously recomputed from wear state, but the manual does not say this. That rationale remains **reconstruction**, not historical vocabulary.

### E — numerical equality does not collapse qualification and runbook semantics

The user guide's shortest retention row is three months, and the operator instruction is also once every three months. The HGST datasheet separately gives three-month retention at 40 °C at EOL.

The equality of the number does not justify:

```text
3-month product retention specification
    ==
3-month operator power-on cadence
```

The first is a retention property under a stated product/endurance condition. The second is an action schedule given to an operator storing the device.

The source does not expose the margin, derivation, or exact causality connecting the two.

### E — periodic power-on instruction does not establish powered-duration sufficiency

This is the main negative control against IBM and Dell.

Hitachi says **when** to restore power, but the inspected text does not say **how long** the server must remain powered for retention purposes.

Therefore:

```text
periodic power-on instruction
    != minimum powered duration
    != maintenance-completion evidence
```

This matters because later Case 111 evidence has stronger completion semantics:

- IBM gives a minimum powered interval in its general extended-shutdown guidance;
- Dell gives a minimum powered interval and describes background retention tasks;
- IBM ESS further exposes a named scrub and a per-vdisk completion message.

The FlashMAX witness is valuable precisely because it shows a **shallower runbook semantics**: cadence exists even when duration/completion remains unstated.

### E — power-on opportunity does not identify the hidden maintenance mechanism

The sources establish that the device should not remain indefinitely unpowered and that server power should periodically be restored.

They do not establish what happens inside FlashMAX during that powered interval.

The evidence does not resolve whether the relevant effect depends on:

- ordinary reads;
- background media scan;
- selective rewrite/reallocation;
- wear-leveling;
- ECC margin inspection;
- metadata maintenance;
- controller initialization alone;
- some combination of the above;
- or another implementation not exposed by the documentation.

So:

```text
powered maintenance opportunity
    != identified firmware algorithm
```

### E — startup integrity checking and retention maintenance remain separate state machines

The user guide's unexpected-shutdown integrity check has an explicit trigger and an operator-visible access restriction while it runs.

The stored-device power-on instruction does not name such a trigger/completion relation.

This supplies a same-document negative control:

```text
named post-crash integrity check
    != unnamed retention-related consequence of periodic power-on
```

Nearby placement in one manual is not evidence of mechanism identity.

---

## Cross-case comparison

### Case 76 — JESD218 SSD endurance / retention qualification

Case 76 owns the standards-level relation among SSD endurance rating, workload, power-off retention, UBER, and application class.

The HGST 2015 datasheet's `3-month retention at 40 °C at EOL` is a **commercial product contract / compliance statement**, not a re-derivation of JESD218.

The Hitachi user guide adds an operator layer:

```text
qualification / product retention contract
    != operator cadence
```

No normative JEDEC clause inspected in this slice requires the specific FlashMAX instruction to turn the server on every three months.

### Case 55 — endurance telemetry

The FlashMAX guide exposes `Remaining Life` through `vgc-monitor` and separately maps remaining write capacity to maximum power-off duration.

Functionally, this resembles Case 55's broader distinction between **model-derived wear state** and immediate device failure.

No claim is made that FlashMAX `Remaining Life` is literally the NVMe `Percentage Used` field or shares its exact calculation.

### Case 37 — Samsung 840 EVO powered periodic refresh

Both cases make powered time relevant to a Flash-storage maintenance problem, but the mechanism/evidence classes differ.

Case 37 has Samsung statements about a product-specific periodic refresh feature addressing old-data read performance and not operating while powered off.

This FlashMAX evidence gives an **operator storage instruction** plus a retention table, but no named internal `refresh` feature.

Therefore:

```text
power periodically restored in both cases
    != same firmware mechanism
    != direct genealogy
```

### Case 111 — IBM / Dell / NetApp later operator policies

FlashMAX materially strengthens Case 111 because it supplies a separate manufacturer/product-family witness before the surviving 2020–2026 IBM/Dell support pages.

The operator policies now span at least these documented forms:

| Witness | Long-offline intervention visible to operator | Duration/completion semantics in inspected source |
| --- | --- | --- |
| Hitachi / HGST FlashMAX | turn on server once every 3 months while stored | no retention-specific minimum on-duration or completion signal stated |
| IBM general storage guidance | power up after 2 months off | at least 2 weeks powered |
| Dell PowerEdge guidance | power up every 2.5 months or read all used NAND | minimum 3 weeks; background retention tasks described |
| IBM ESS follow-up | restore power and allow scrub to complete | named scrub + per-vdisk completion message |
| NetApp long-offline preparation | remove payload before prolonged unpowered storage | changes intervention topology instead of periodic powered retention |

This is a functional/operator-policy comparison only. It does not establish common firmware ancestry.

---

## Functional analogy

A bounded functional analogy is useful:

> A storage medium can be nonvolatile at the payload layer while still requiring **calendar-level infrastructure work** to keep its future recoverability within the vendor's operational envelope.

In FlashMAX, that work is expressed simply as periodically turning on the server. In later IBM/Dell evidence, the operational obligation acquires minimum run time, background-task language, and in IBM ESS a visible scrub-completion event.

This analogy concerns the **distribution of retention work across device and operator**. It is not a claim that all power-on events are refresh operations.

---

## Philosophical interpretation — bounded

The FlashMAX record sharpens one project-wide point without replacing the engineering description:

A nonvolatile object can remain physically present yet still depend on a **future schedule of reactivation**. The retained payload is not thereby converted into volatile memory; rather, the conditions under which its persistence remains trusted include an organizational/calendar relation external to the NAND cells themselves.

This is a project interpretation. `reactivation`, `calendar infrastructure`, and `maintenance opportunity` are not Hitachi/HGST historical terms.

---

## Explicit non-claims

This deepening does **not** claim that:

1. `MK-99COM145-00` was first published on 1 January 2014 or on any other exact date not shown by a recovered revision ledger;
2. FlashMAX invented periodic SSD power-on maintenance;
3. the three-month operator cadence is mandated by JEDEC;
4. every FlashMAX card loses data exactly after the table interval;
5. the table is a deterministic per-device failure clock;
6. one server power-on instant is sufficient maintenance;
7. the server must remain powered for any unstated number of hours/days;
8. periodic power-on necessarily rewrites every NAND cell;
9. periodic power-on necessarily invokes wear leveling;
10. the unanticipated-shutdown integrity check is the retention-maintenance mechanism;
11. the 2015 HGST datasheet proves the internal origin of the Hitachi user-guide cadence;
12. the same controller firmware is used across every listed FlashMAX II/III capacity and revision;
13. the surviving Hitachi/HGST publications establish component-supply-chain independence from all other vendors;
14. similar three-month numbers prove direct genealogy among Hitachi/HGST, IBM, Dell, NetApp, Samsung, or JEDEC;
15. powering the card periodically substitutes for backup;
16. a product-level EOL retention statement is the same evidence class as a system-vendor field runbook;
17. `Remaining Life` is identical to NVMe `Percentage Used`;
18. the later IBM/Dell minimum-duration rules can be projected backward onto FlashMAX.

---

## Claim ledger

| Claim | Type | Strength | Boundary |
| --- | --- | --- | --- |
| Hitachi FlashMAX2&3 guide exposes a wear-dependent maximum-power-off table | H/P | strong | vendor product guide |
| table ranges from 5 years at 90% remaining write capacity to 3 months at 0% | H/P | strong | product-guide relation; not deterministic individual failure time |
| guide says to turn on the server once every 3 months while the device is stored | H/P | strong | operator cadence; duration/completion unstated |
| later `-03` guide preserves the same table and cadence | H/P | strong | revision continuity only; no firmware-identity claim |
| HGST 2015 datasheet gives 3-month retention at 40 °C at EOL | H/P | strong | product contract/compliance statement |
| one operator cadence can coexist with multiple wear-conditioned retention rows | E | strong | directly follows from one guide's table + instruction |
| three-month product retention spec != three-month operator cadence | E | strong | same number, different relation/evidence semantics |
| periodic power-on != minimum powered duration != completion evidence | E | strong | source omits latter two |
| periodic power-on proves a particular hidden refresh/wear-leveling algorithm | X | rejected | no causal implementation evidence |
| unexpected-shutdown integrity check is the periodic retention mechanism | X | rejected | source scopes it to unanticipated shutdown |
| FlashMAX closes Case 111's independent periodic-power-up witness gap | E | strong at vendor/product-document level | does not close independent duration/completion gap |

---

## Source ledger

### Primary/vendor technical sources

1. Hitachi, Ltd., _PCIe Flash Drive FlashMAX2&3 User's Guide_, `MK-99COM145-00`, surviving Hitachi Vantara-hosted PDF: <https://download.hitachivantara.com/download/epcra/com1450.pdf>.
2. HGST, _FlashMAX PCIe — Enterprise Solid-State Drives_, `DS24-EN-US-0815-05`, produced 5/15, revised 8/15, surviving manufacturer document hosted by Western Digital: <https://documents.westerndigital.com/content/dam/doc-library/en_us/assets/public/western-digital/product/hgst/general-docs/data-sheet-flashmax-pcie.pdf>.
3. Hitachi, Ltd., _PCIe Flash Drive FlashMAX2&3 User's Guide_, `MK-99COM145-03`, surviving Hitachi Vantara-hosted PDF: <https://download.hitachivantara.com/download/epcra/com1453.pdf>.

### Internal project links

- [`Case 111 — Enterprise SSD Extended Shutdown`](../cases/111-enterprise-ssd-extended-shutdown-maintenance.md)
- [`Evidence 111 — IBM / Dell Extended Shutdown`](111-ibm-dell-2020-2026-ssd-extended-shutdown-grounding.md)
- [`Case 76 — JESD218 SSD Endurance Qualification`](../cases/76-jedec-ssd-endurance-retention-qualification.md)
- [`Case 55 — NVMe SMART / Health`](../cases/55-nvme-smart-health-endurance-telemetry.md)
- [`Case 37 — Samsung 840 EVO Old-Data Performance`](../cases/37-samsung-840-evo-old-data-performance-refresh.md)

### Related-repository reuse check

A current search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `SSD power off retention shutdown refresh` returned no dedicated FlashMAX / long-offline-retention case to reuse. A broad history of Virident/HGST PCIe Flash accelerators would belong there if developed later; this evidence file keeps only the retention/runbook boundary.

---

## Remaining evidence debt

This slice deliberately leaves open:

1. an exact revision/publication ledger for `MK-99COM145-00` through `-03` rather than copyright-year endpoints;
2. original HGST/Virident engineering rationale for selecting the three-month storage cadence;
3. firmware/service documentation identifying what maintenance, if any, is guaranteed to execute after a stored card is powered;
4. a retention-specific minimum powered duration for FlashMAX;
5. an operator-visible completion signal tied specifically to long-offline retention rather than unanticipated-shutdown integrity checking;
6. controller/firmware mapping across the 1.1 TB, 2.2 TB, and 4.8 TB variants;
7. field logs or controlled tests showing retention behavior at several `Remaining Life` levels;
8. whether any earlier Virident manual contained the same periodic power-on instruction;
9. whether later HGST/Western Digital enterprise Flash products retained, modified, or removed the instruction;
10. a second independent vendor witness that combines **periodic power-up + explicit minimum powered duration + completion semantics** outside IBM/Dell lineage.
