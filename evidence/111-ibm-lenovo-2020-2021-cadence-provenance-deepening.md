# Evidence 111 — IBM / Lenovo Extended-Shutdown Cadence and Source-Provenance Deepening, 2020–2021

## Status

**`bounded deepening complete`** for one narrow question:

> When several support pages repeat the same enterprise-SSD retention background, do they constitute independent evidence for one universal operator cadence?

This record adds two controls to Case 111:

1. **same vendor, same broad three-month / 40 °C background, different product-specific powered-run cadence** — IBM's general Storwize/FlashSystem guidance says at least two weeks powered after two months off, while a TS7770 notice published the next day says at least one week powered after two months off;
2. **different vendor domain, strongly related product/support lineage, nearly identical runbook wording** — Lenovo's January 2021 article repeats the two-month / two-week guidance for Lenovo Storage V-series and `Storwize V7000 for Lenovo`, so it should not be counted naively as an independent cross-vendor replication of the policy.

The bounded result is:

```text
shared qualification/risk background
    != uniquely determined operator cadence

and

separate vendor support page
    != automatically independent evidence lineage
```

This is an evidence-provenance and operator-policy deepening. It is **not** a NAND-controller-internals study and does not close Case 111's need for additional genuinely independent enterprise-vendor evidence.

---

## Sources inspected

### Source A — IBM general extended-shutdown support guidance

IBM Support, **“Potential for SSD data loss after extended shutdown”**:

- current page: <https://www.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>
- surviving support-content mirror: <https://supportcontent.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>

Observed publication metadata:

- support-content mirror: created **16 December 2020**;
- current page: modified **28 March 2023**;
- UID: `ibm16382908`.

The current page lists affected IBM storage families including Storwize V7000, SAN Volume Controller, Storwize V5000, and several FlashSystem families.

### Source B — IBM TS7770-specific notice

IBM Support, **“TS7770 with FC 8081 may experience issues when being powered off for more than three months”**:

- <https://www.ibm.com/support/pages/node/6382550>
- surviving search/index metadata records **Date first published: 17 December 2020**.

This notice is product-specific to **TS7770 with FC 8081**.

### Source C — Lenovo extended-shutdown support guidance

Lenovo Support, document **HT511702**, **“Potential for SSD data loss after extended shutdown”**:

- example current product-scoped page: <https://datacentersupport.lenovo.com/kw/en/products/storage/lenovo-storage/v3700v2/6535/solutions/ht511702>
- document metadata: **Original Publish Date: 24 January 2021**; **Last Modified Date: 25 January 2021**.

Affected platforms listed by Lenovo include:

- Lenovo Storage V3700 V2/XP;
- Lenovo Storage V5030;
- Lenovo Storage V7000 for PRC;
- Lenovo Storage V3500;
- Lenovo Storage V3700;
- Lenovo Storage V5000;
- **Storwize V7000 for Lenovo**.

### Source D — Lenovo product-family / firmware-lineage context

Lenovo Support, document **HT505889**, **“IBM Storwize for Lenovo and Lenovo Storage V-series Upgrade Planning”**:

- <https://support.lenovo.com/kw/en/solutions/ht505889-ibm-storwize-for-lenovo-and-lenovo-storage-v-series-upgrade-planning>
- original publish date **22 January 2018**;
- last modified **14 February 2018**.

The document explicitly plans firmware upgrades across an **IBM Storwize for Lenovo family** and a **Lenovo Storage V-series family**, with shared release-level planning for Storwize V5000/V7000 and Lenovo Storage V3700 V2/V5030.

This source is used only to establish that the Lenovo support surface in Source C is not safely treated as a wholly unrelated product lineage merely because it appears under a different vendor domain.

---

## Historical record

### H/P — IBM's general guidance uses a two-month / two-week operator schedule

IBM's general support article uses the familiar enterprise-SSD retention background of **three months at 40 °C** and warns that extended power-off can lead to data loss and/or drive failures.

Its runbook then moves intervention earlier than that headline interval:

- after **two months** of system power-off;
- power the system and enclosed drives for **at least two weeks**;
- maintain the powered-off environment below 40 °C;
- avoid extended shutdown for a drive already reporting end-of-life status;
- keep recent backups before extended shutdown.

The page's affected-product metadata spans several IBM storage families. The present deepening does not infer that all those families contain the same SSD model, controller, firmware, or background-maintenance algorithm.

### H/P — IBM's TS7770 notice uses the same broad risk background but only a one-week powered interval

The TS7770 notice was first published **17 December 2020**, one day after the surviving creation date of the general IBM support guidance.

It again states the enterprise-SSD background as **three months at 40 °C** and gives the same broad warnings about gradual Flash charge loss, data loss/drive-failure risk, backups, end-of-life drives, and environmental control.

But its product-specific operational recommendation is different:

- after **two months** of system power-off;
- power the system and enclosed drives for **at least one week**.

That one-week recommendation is the important negative control. Within IBM's own surviving December 2020 support record:

```text
same broad three-month / 40 °C background
    + same two-month intervention point
    != same minimum powered-run duration
```

The evidence therefore does not support deriving `two weeks` mechanically from the JEDEC retention interval itself.

### H/P — Lenovo HT511702 repeats the IBM-style two-month / two-week runbook

Lenovo's HT511702, originally published **24 January 2021**, presents the same broad three-month / 40 °C enterprise-SSD background and recommends:

- recent backups before extended shutdown;
- power-up after **two months** off for **at least two weeks**;
- continued environmental control below 40 °C while powered down;
- avoiding prolonged power-off for drives indicating end of life;
- formatting a drive in candidate state with `chdrive -task format` when a retired system will later be reused.

The affected-platform list includes both Lenovo Storage V-series names and **Storwize V7000 for Lenovo**.

At the level needed here, the semantic structure and operator cadence substantially match IBM's general December 2020 guidance.

### H/P — Lenovo already documented the Storwize-for-Lenovo / Lenovo V-series relation before HT511702

Lenovo HT505889 predates the shutdown article by three years. Its title and firmware-planning table explicitly place **IBM Storwize for Lenovo** and **Lenovo Storage V-series** in one support/upgrade context.

This matters methodologically because the January 2021 Lenovo shutdown article is not a clean sample from a storage family with no visible relationship to the IBM Storwize ecosystem.

The defensible historical claim is limited:

> **There is documented product/support lineage overlap sufficient to reject a naive assumption of source independence.**

The inspected sources do **not** establish the exact editorial workflow by which the Lenovo article was produced, nor do they prove that every Lenovo-listed platform ran byte-identical IBM firmware.

---

## Engineering reconstruction

### E — qualification background underdetermines field cadence

The IBM comparison provides a useful decomposition:

```text
standards / qualification background
    -> constrains a retention-risk envelope

product/system runbook
    -> chooses an intervention point and maintenance opportunity
```

If the headline three-month / 40 °C relation uniquely determined the operator cadence, the two December 2020 IBM notices would not be expected to prescribe different powered durations while invoking the same broad background.

The safer model is:

```text
operator cadence = qualification context
                 + product/system assumptions
                 + operational safety margin
                 + maintenance/recommissioning requirements
```

The sources do not expose enough internal engineering detail to solve those terms quantitatively. The equation is therefore a project decomposition, not IBM vocabulary.

### E — same intervention point does not imply same completion criterion

Both IBM notices use **two months powered off** as the intervention point, but one asks for at least one week powered and the other at least two weeks.

Therefore:

```text
same calendar trigger
    != same powered-maintenance window
```

and more generally:

```text
maintenance trigger
    != maintenance duration
    != maintenance-completion evidence
```

This complements the existing ESS deepening, where IBM exposes an observable scrub-completion message rather than relying only on elapsed powered time.

### E — duplicated support wording should not inflate cross-vendor evidence count

Suppose two support pages repeat the same retention warning and cadence. There are at least two explanations:

1. independent vendors converged on the same policy from independent engineering evidence;
2. the pages share product lineage, support content, inherited operational knowledge, or another dependence relation.

The Lenovo evidence makes explanation (2) sufficiently plausible and historically grounded that HT511702 should **not** be counted as an independent new vendor witness for a universal two-month / two-week rule.

Thus:

```text
number of webpages
    != number of independent engineering observations
```

For this repository, evidence provenance is part of claim strength whenever cross-vendor agreement is used to generalize a retention mechanism or runbook.

### E — CLI vocabulary can expose support-lineage continuity without proving implementation identity

Both IBM's general guidance and Lenovo HT511702 use the Storwize-family administrative vocabulary around a candidate drive and `chdrive -task format`.

That is useful evidence of a shared operational surface. It does **not** prove:

- the same physical Flash modules;
- the same FTL;
- the same NAND generation;
- the same format implementation in every product or firmware release;
- the same hidden retention-maintenance algorithm.

Interface continuity is weaker than implementation identity.

---

## Functional comparison

### Case 76 — JESD218 qualification

Case 76 supplies the bounded standards-level relation. This deepening shows why a qualification interval cannot be silently promoted into one field-maintenance schedule:

```text
qualification requirement
    != IBM general runbook
    != IBM TS7770 runbook
```

The comparison is functional and policy-level. It does not claim JEDEC specified either IBM cadence.

### Case 111 — IBM ESS scrub-completion deepening

The ESS follow-up gives an even stronger operator-state decomposition:

```text
calendar threshold
    -> power restored
    -> scrub executes
    -> per-vdisk completion is observed
```

The TS7770/general-IBM cadence split reinforces why **elapsed powered time** is not itself a universal physical definition of maintenance completion.

### Case 37 — Samsung 840 EVO periodic refresh

Case 37 remains useful only as a product-level comparison showing that a described background maintenance feature can depend on powered operation. Nothing in the IBM/Lenovo support pages proves Samsung's exact refresh mechanism or genealogy.

---

## Philosophical interpretation — bounded

A limited project interpretation survives this evidence:

> Retention policy can acquire an institutional history of its own. A physical risk envelope becomes a support runbook; the runbook can then be specialized by product context or propagated across related product/support families.

That does **not** make documentation itself the NAND retention mechanism. The retained payload still depends on Flash physics, controller behavior, redundancy, and maintenance. Documentation matters at another layer: it can preserve the operator procedure that makes a future maintenance opportunity happen at all.

The useful distinction is therefore:

```text
physical retention mechanism
    != operator maintenance policy
    != documentary transmission of that policy
```

This is a philosophical/organizational interpretation, not IBM or Lenovo historical vocabulary.

---

## Prior-art and source-independence boundary

This deepening makes **no invention-priority claim**. IBM's December 2020 dates and Lenovo's January 2021 date are publication chronology for the surviving support documents only.

The Lenovo page is also deliberately **not** used as an independent fourth-vendor witness alongside IBM, Dell, and NetApp. Its value is the opposite: it demonstrates why apparent cross-vendor repetition must be checked for product/support lineage before it is counted as independent corroboration.

A fresh search of `tmzncty/computing-archaeology` for enterprise-SSD extended-shutdown / powered-maintenance material found no dedicated technical-history case to reuse. Generic Storwize/SSD history is not reconstructed here.

---

## Explicit non-claims

This evidence does **not** claim that:

1. the JEDEC three-month / 40 °C relation mathematically implies IBM's one-week or two-week powered interval;
2. one week is sufficient for every TS7770 configuration under every wear state and temperature;
3. two weeks is sufficient for every Storwize/FlashSystem configuration under every wear state and temperature;
4. either interval is a measured NAND rewrite time;
5. applying power proves hidden drive-local maintenance completed;
6. every IBM product listed on the general page uses one SSD model or one controller implementation;
7. every Lenovo V-series product uses byte-identical IBM firmware;
8. Lenovo copied IBM through a particular editorial workflow;
9. publication chronology proves invention chronology;
10. identical support wording proves independent experimental confirmation;
11. `chdrive -task format` has one invariant media-level implementation across all products and generations;
12. formatting is equivalent to refresh, scrub, sanitize, or retention maintenance;
13. the TS7770 one-week cadence supersedes the general IBM two-week cadence;
14. Lenovo closes Case 111's open debt for independent vendors beyond IBM/Dell/NetApp;
15. support-policy propagation is the same mechanism as data retention in NAND.

---

## Claim ledger

| Claim | Type | Strength | Boundary |
| --- | --- | --- | --- |
| IBM general guidance exists by 16 Dec 2020 | Historical record | strong | surviving support-content publication floor, not invention date |
| IBM general guidance uses two months off + at least two weeks powered | Historical record | strong | affected IBM storage-system support context |
| IBM TS7770 notice was first published 17 Dec 2020 | Historical record | strong | product-specific support notice |
| IBM TS7770 guidance uses two months off + at least one week powered | Historical record | strong | TS7770 with FC 8081 only |
| same broad retention background can coexist with different IBM powered-run durations | Historical record / engineering reconstruction | strong | does not identify the undisclosed cause of the difference |
| Lenovo HT511702 was originally published 24 Jan 2021 and uses two months + two weeks | Historical record | strong | listed Lenovo/Storwize-for-Lenovo platforms |
| Lenovo HT505889 documents an IBM-Storwize-for-Lenovo / Lenovo-V-series support relation | Historical record | strong | establishes lineage overlap, not implementation identity |
| Lenovo HT511702 should not be counted naively as independent cross-vendor confirmation of IBM cadence | Engineering reconstruction / source criticism | strong | exact editorial transfer path remains unknown |
| qualification boundary uniquely determines operator cadence | Rejected | strong negative control | contradicted by differing IBM product guidance |
| separate vendor domain automatically means independent engineering evidence | Rejected | strong negative control | product/support lineage must be checked |

---

## Remaining evidence debt

This bounded deepening closes only the provenance/cadence question above. Still open:

1. identify genuinely independent enterprise vendors with explicit long-power-off operator guidance;
2. recover engineering rationale for the TS7770 **one-week** versus general IBM **two-week** powered duration, if any public primary source exposes it;
3. determine whether later TS7770 documentation retained, changed, or removed the December 2020 cadence;
4. find firmware/service telemetry that distinguishes `power applied` from actual device-local retention-task completion;
5. trace the exact support-content editorial/provenance path between IBM's December 2020 guidance and Lenovo HT511702 only if archival evidence makes that path demonstrable;
6. map specific drive/controller families only where primary product documentation supports the mapping;
7. preserve the existing Case 111 distinction between standards qualification, operator policy, powered-maintenance opportunity, and observed scrub completion.

---

## Sources

- IBM Support, **“Potential for SSD data loss after extended shutdown”**, current page modified 28 March 2023: <https://www.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>.
- IBM support-content mirror of the same article, recording creation on 16 December 2020: <https://supportcontent.ibm.com/support/pages/potential-ssd-data-loss-after-extended-shutdown>.
- IBM Support, **“TS7770 with FC 8081 may experience issues when being powered off for more than three months”**, date first published 17 December 2020: <https://www.ibm.com/support/pages/node/6382550>.
- Lenovo Support, **“Potential for SSD data loss after extended shutdown”**, document HT511702, original publish date 24 January 2021, last modified 25 January 2021: <https://datacentersupport.lenovo.com/kw/en/products/storage/lenovo-storage/v3700v2/6535/solutions/ht511702>.
- Lenovo Support, **“IBM Storwize for Lenovo and Lenovo Storage V-series Upgrade Planning”**, document HT505889, original publish date 22 January 2018, last modified 14 February 2018: <https://support.lenovo.com/kw/en/solutions/ht505889-ibm-storwize-for-lenovo-and-lenovo-storage-v-series-upgrade-planning>.

## Completion note

`bounded deepening complete`: this slice establishes **cadence underdetermination** inside IBM's own December 2020 support record and **source-dependence caution** for the later Lenovo page. It intentionally leaves truly independent cross-vendor expansion and controller-level causal explanation open.