# Evidence — Case 111: Seagate Pulsar Rev. A moves the powered-retention-maintenance documentation floor to April 2010

## Status

**`bounded deepening complete`** for the narrow documentation-prior-art question addressed here.

This packet does **not** claim invention priority for SSD retention maintenance. It asks a smaller question:

> How early can Case 111 directly document, in a named enterprise SSD product manual, the coexistence of an unpowered retention specification, powered firmware/hardware retention work, and no routine operator preventive-maintenance requirement?

The answer moves the directly inspected floor from Seagate Pulsar XT.2 Rev. B (June 2011) to the first-generation Seagate Pulsar SATA Product Manual Rev. A, dated **5 April 2010**.

## Why this slice

Case 111 already grounded two later layers:

1. 2011–2012 Seagate enterprise SSD manuals in which powered controller-local retention maintenance is explicit; and
2. 2020–2026 IBM/Dell operator runbooks that turn long power-off intervals into field scheduling problems.

The remaining historical debt was whether the named-product documentation floor could be moved earlier without relying on revision-history inference. The first-generation Pulsar manual closes that bounded debt directly.

This is useful precisely because the result is **not** the same as the later XT.2/Pulsar.2 wording. The 2010 manual says the SSD contains firmware and hardware features that can monitor and refresh memory cells while powered, but it does not expose the later manuals' more specific conditional-rewrite wording.

## Source custody and evidence quality

### H/P — Seagate Pulsar Product Manual Rev. A

Primary source:

- Seagate Technology LLC, **_Pulsar Product Manual_**, publication `100596473`, Rev. A, April 2010.
- First-party Seagate-hosted PDF: <https://www.seagate.com/content/dam/seagate/migrated-assets/staticfiles/support/disc/manuals/ssd/100596473a.pdf>
- Models named on the cover: `ST9200011FS`, `ST9100011FS`, `ST950011FS`.
- Media: SLC NAND Flash.

The cover identifies `100596473`, `Rev. A`, and `April 2010`. The revision-history page records:

```text
Rev. A    04/05/10    Initial release.
```

That makes **5 April 2010** the direct documentation date used in this packet.

### H/P — Seagate commercialization chronology

Primary corporate source:

- Seagate investor/news release, **“Seagate introduces its First Solid State Drive: Pulsar,”** 7 December 2009: <https://investors.seagate.com/news/news-details/2009/Seagate-introduces-its-First-Solid-State-Drive-Pulsar/default.aspx>

The release says Pulsar was Seagate's first product in a new enterprise SSD family and that Seagate began shipping Pulsar units to selected OEMs for revenue in **September 2009**.

That chronology is retained only as a commercialization anchor. It does **not** license back-projection of the April-2010 manual's retention wording into September or December 2009.

The source rule is therefore:

```text
commercial shipment date
    !=
public documentation date
    !=
implementation date
    !=
invention date
```

## Historical record

### H/P — the April-2010 manual is a named enterprise SSD product document

The manual describes the first-generation Pulsar SATA SSD family. Its introduction identifies SLC NAND Flash storage and its specification tables identify the three named models.

This matters because the evidence is not a later generic Flash-maintenance explanation, patent abstraction, or retrospective history. It is a product manual for a shipping enterprise SSD family.

### H/P — unpowered retention is specified separately

The manual's specification material states a typical data-retention value with power removed of **1 year at 25 °C**.

The reliability table repeats:

```text
Typical Data Retention with Power removed (at 25C): 1 year
```

The accompanying note says that NAND retention capability deteriorates with use/program-erase history and that higher temperature reduces the length of time the Flash component can retain its programmed value with power removed.

This is a bounded product specification. It is not a universal SLC constant and is not directly numerically comparable with later products tested or specified under different temperatures, wear states, NAND generations, or qualification assumptions.

### H/P — powered retention maintenance is explicit

The same reliability note then states that retention is not an issue with power applied because the SSD contains firmware and hardware features able to **monitor and refresh memory cells when power is applied**.

This directly documents a powered/unpowered regime distinction by April 2010:

```text
power removed
    -> retention must be carried by the NAND state under the stated product condition

power applied
    -> firmware / hardware monitoring and refresh capability is available
```

The manual does not disclose the metric being monitored, the threshold that admits maintenance, the coverage policy, the scheduler, the unit of work, or the exact physical rewrite primitive.

### H/P — no operator preventive maintenance is required

The same reliability table says:

```text
Preventive maintenance: None required.
```

This is historically important because it appears in the same product document as powered internal retention work.

The directly supported boundary is therefore:

```text
no operator preventive-maintenance requirement
    !=
no controller-local retention maintenance
```

The product can present itself as requiring no routine preventive maintenance from the operator while still depending on powered firmware/hardware work to sustain the retention regime described by the vendor.

### H/P — commercialization predates the inspected manual, but maintenance wording cannot be back-projected

Seagate's 7 December 2009 announcement says revenue shipments to selected OEMs began in September 2009. The first directly inspected manual in this packet is dated 5 April 2010.

The only safe chronology is:

```text
September 2009
    revenue shipments to selected OEMs

7 December 2009
    public Pulsar announcement

5 April 2010
    directly inspected Rev. A product manual with powered monitor/refresh wording
```

Nothing in the inspected announcement itself establishes the same monitor/refresh wording. This packet therefore does not move the **direct documentation floor** into 2009.

## Engineering reconstruction

### E — passive shelf retention and powered retention support are different operating regimes

The manual provides enough evidence for a bounded reconstruction:

```text
offline regime
    NAND physical state
    + wear history
    + storage temperature
    -> bounded unpowered retention capability

powered regime
    NAND physical state
    + controller firmware/hardware
    + monitor/refresh capability
    -> additional retention-maintenance path available
```

The second regime does not erase the first. A drive that can maintain cells while powered still has a finite unpowered retention specification.

Likewise, nonvolatility does not imply that every useful retention guarantee is passive:

```text
nonvolatile media
    !=
maintenance-free media under all operating histories
```

### E — maintenance capability is not maintenance-completion evidence

The 2010 manual says powered firmware/hardware **can** monitor and refresh cells. It does not publish a completion marker, full-device scan cursor, maintenance counter, dwell-time contract, or operator-visible completion event.

Therefore:

```text
power applied
    -> maintenance capability available
    !=
maintenance completed
```

This distinction remains important when Case 111 later reaches Dell's minimum powered durations and IBM ESS scrub-completion evidence.

### E — “refresh memory cells” does not reveal the unit of work

The 2010 wording is intentionally left at its documented granularity. `refresh memory cells` could involve controller operations whose exact physical organization is hidden by the product interface.

The source does **not** establish:

- one-cell-at-a-time refresh;
- page rewrite;
- block relocation;
- read reclaim;
- whole-device periodic sweep;
- a fixed cadence;
- a retained per-cell age map;
- one particular ECC threshold;
- host-read-triggered maintenance.

Those are separate engineering questions.

### E — operator responsibility and device responsibility are separable

The coexistence of `Preventive maintenance: None required` and powered monitor/refresh capability supports a responsibility decomposition:

```text
operator responsibility
    !=
controller responsibility

no scheduled human maintenance
    !=
no ongoing machine maintenance
```

This is a useful predecessor to the later Case 111 field runbooks, where long shutdown removes the device's maintenance opportunity and therefore pushes some retention responsibility back outward into operator scheduling.

## Controlled comparison with later Seagate manuals

### F/A — 2010 Pulsar vs 2011 Pulsar XT.2

The 2010 first-generation Pulsar Rev. A directly says powered firmware/hardware can monitor and refresh memory cells.

The June-2011 Pulsar XT.2 Rev. B adds a stronger product-level wording in its dedicated retention section: powered cell state is monitored and cells are conditionally rewritten when levels decay unexpectedly.

Safe comparison:

```text
2010 Pulsar
    direct powered monitor / refresh wording

2011 XT.2
    direct powered monitor / refresh wording
    + more explicit conditional-rewrite description
```

Unsafe inference:

```text
2010 “refresh memory cells”
    ==
2011 exact conditional-new-location rewrite mechanism
```

The earlier manual moves the documentation floor but does not inherit every later implementation detail.

### F/A — 2010 Pulsar vs 2012 Pulsar.2

Pulsar.2 is a later MLC enterprise SSD family and carries the more explicit conditional-rewrite wording. The first-generation Pulsar in this packet is SLC.

The similar broad retention vocabulary supports documentation-level continuity only. It does not prove one controller lineage, identical thresholds, one scheduler, or one physical maintenance primitive.

### F/A — the numerical retention specifications are not directly comparable

The 2010 first-generation Pulsar manual states a typical **1 year at 25 °C** with power removed. The later XT.2/Pulsar.2 manuals used in Case 111 give a typical **3 months at 40 °C** relation.

Those numbers must not be ordered as if they measured the same condition:

```text
1 year @ 25 °C on first-generation Pulsar
    !=
3 months @ 40 °C on later XT.2 / Pulsar.2
```

Different temperature, media generation, product design, wear assumptions, test conditions, and documentation conventions prevent a simple “2010 retained longer” conclusion.

## Controlled terminology comparison with Case 67

Case 67 grounds an OCP telemetry field named `Refresh Counts` as an integrity-maintenance block-reallocation accounting category. The 2010 Pulsar manual uses the ordinary product phrase `refresh memory cells`.

The shared word **refresh** is not enough to merge the mechanisms:

```text
same label “refresh”
    !=
same unit of work
    !=
same trigger
    !=
same controller primitive
    !=
same telemetry semantics
```

Case 111's source describes a powered retention-maintenance capability. Case 67's OCP field describes an accounting interface. No historical or implementation genealogy is asserted between them.

## Controlled comparison with DRAM refresh

The manual's use of `refresh` does not make NAND maintenance equivalent to DRAM refresh.

DRAM refresh is deadline-driven restoration of volatile charge state as part of ordinary correct operation. The Pulsar evidence concerns a nonvolatile Flash product whose controller can monitor and refresh cells while powered and which separately publishes a finite unpowered retention specification.

Functional similarity is limited to the fact that persistence can depend on renewal work. Physical mechanism, timing model, addressing, failure modes, and historical vocabulary differ.

## Philosophical / media-theoretical interpretation

The following is a project-level interpretation, not Seagate's vocabulary:

> **Persistence can be partly produced by ongoing powered maintenance while the product still presents itself externally as nonvolatile storage requiring no routine preventive maintenance from the operator.**

The useful distinction is not `persistent` versus `maintained` as mutually exclusive categories. Instead, a system can combine:

- passive physical persistence during an unpowered interval;
- autonomous maintenance while powered;
- an interface that hides that maintenance from ordinary operators;
- later institutional policies that become necessary when power is absent long enough to suppress the hidden work.

This interpretation must remain downstream of the engineering record. The 2010 manual itself does not theorize “maintenance-produced persistence.”

## Explicit non-claims

This packet does **not** establish that:

1. Seagate invented SSD retention refresh in 2010.
2. April 2010 is the first ever use of powered Flash retention maintenance.
3. September 2009 revenue shipment proves the April-2010 retention wording was already present then.
4. December 2009 public announcement documents powered cell refresh.
5. Rev. A publication date equals firmware implementation date.
6. The first-generation Pulsar used the same controller as Pulsar XT.2.
7. The first-generation Pulsar used the same controller as Pulsar.2.
8. `refresh memory cells` means one physical NAND cell is individually rewritten.
9. `refresh memory cells` means page rewrite.
10. `refresh memory cells` means block relocation.
11. `refresh memory cells` means read reclaim.
12. `refresh memory cells` means an OCP `Refresh Counts` event.
13. The drive periodically rewrites every block.
14. A host read sweep triggers the 2010 maintenance path.
15. Applying power proves any maintenance pass completed.
16. `Preventive maintenance: None required` means no internal maintenance occurs.
17. One year at 25 °C is a universal SLC retention constant.
18. One year at 25 °C can be directly ranked against three months at 40 °C from later products.
19. The 2010 product had infinite powered retention.
20. The vendor's phrase that retention is not an issue when powered is a mathematical guarantee under every failure mode.
21. Monitoring implies a specific retained age counter or threshold table.
22. Monitoring proves controller telemetry exposed maintenance state to the host.
23. The 2010 manual establishes an IBM/Dell-style operator power-up cadence.
24. The 2010 maintenance path is DRAM refresh.
25. The 2010 maintenance path is Samsung 840 EVO periodic refresh.
26. The 2010 maintenance path is Case 36's Flash Correct-and-Refresh algorithm.
27. Similar terminology proves genealogy among Seagate product generations.
28. Product shipping date, documentation date, implementation date, and invention date are interchangeable.
29. The 2009 investor release is evidence for the internal retention mechanism.
30. A current surviving PDF proves no earlier manual or engineering document existed.

## Claim ledger

| Claim | Type | Strength | Boundary |
| --- | --- | --- | --- |
| Pulsar manual `100596473`, Rev. A, is dated April 2010 | H/P | strong | first-party Seagate PDF |
| Revision history records `04/05/10` as the initial release | H/P | strong | direct facsimile/text; documentation date only |
| Manual covers ST9200011FS / ST9100011FS / ST950011FS | H/P | strong | named product family |
| Product uses SLC NAND Flash | H/P | strong | first-generation Pulsar only |
| Manual specifies typical 1-year power-off retention at 25 °C | H/P | strong | bounded product/condition; not universal constant |
| Manual says retention degrades with use and higher temperature | H/P | strong | qualitative source statement |
| Manual says powered firmware/hardware can monitor and refresh memory cells | H/P | strong | exact trigger, geometry and primitive undisclosed |
| Manual says preventive maintenance is not required | H/P | strong | operator-facing statement; does not negate internal work |
| Named enterprise SSD powered-retention-maintenance documentation therefore exists by 5 April 2010 | H/E | strong | documented-by floor, not invention priority |
| Seagate announced Pulsar publicly on 7 December 2009 | H/P | strong | first-party corporate chronology |
| Seagate says revenue shipments to selected OEMs began in September 2009 | H/P | strong | commercialization chronology only |
| April-2010 maintenance wording was already present in September 2009 | X | rejected | no inspected 2009 source establishes it |
| 2010 monitor/refresh wording proves XT.2's exact later conditional-rewrite behavior | X | rejected | later wording is more specific |
| first-generation Pulsar 1y@25°C is directly better than XT.2/Pulsar.2 3mo@40°C | X | rejected | conditions are not comparable |
| no routine preventive maintenance != no controller-local maintenance | E | strong | both statements coexist in one product manual |
| power applied != maintenance completion | E | strong | capability wording lacks completion evidence |
| commercial shipment date != documentation date != implementation/invention date | E/H | strong | source-chronology boundary |
| `refresh` in Case 111 == OCP `Refresh Counts` in Case 67 | X | rejected | product-maintenance wording vs telemetry/accounting semantics |

## Related-repository routing

A repository search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `Pulsar` and publication number `100596473` found no dedicated packet to reuse.

This repository therefore keeps only the retention-specific seam:

```text
unpowered product retention
    -> powered controller-local monitoring / refresh
    -> later explicit conditional-rewrite wording
    -> still later operator scheduling around long shutdown
```

A broader history of Seagate's first enterprise SSD program, controller genealogy, OEM qualification, SLC-to-MLC product evolution, SATA/SAS product strategy, or the precise engineering history from 2009 shipment to 2010 documentation belongs in `computing-archaeology`.

## Remaining evidence debt

The bounded April-2010 documentation floor is closed. Remaining useful work is narrower:

- find a directly inspectable pre-April-2010 enterprise SSD manual with comparable powered retention-maintenance wording;
- recover any September–December 2009 Pulsar engineering/product documentation that directly states the maintenance behavior rather than inferring it from the 2010 manual;
- recover a direct Pulsar XT.2 Rev. A facsimile to verify the existing March-2011 revision-lineage inference;
- determine, only from appropriately strong sources, what the first-generation Pulsar controller actually counted, sensed, or rewrote during `refresh`;
- preserve the distinction between product-local maintenance and later operator-runbook cadence.

## Sources

- Seagate Technology LLC, **_Pulsar Product Manual_**, publication `100596473`, Rev. A, April 2010: <https://www.seagate.com/content/dam/seagate/migrated-assets/staticfiles/support/disc/manuals/ssd/100596473a.pdf>.
- Seagate, **“Seagate introduces its First Solid State Drive: Pulsar,”** 7 December 2009: <https://investors.seagate.com/news/news-details/2009/Seagate-introduces-its-First-Solid-State-Drive-Pulsar/default.aspx>.
- Internal comparison: [`111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md`](111-seagate-xt2-2011-powered-retention-refresh-prior-art-deepening.md).
- Internal comparison: [`111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md`](111-seagate-pulsar2-2012-powered-retention-refresh-prior-art-deepening.md).
- Terminology comparison: [`../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md`](../cases/67-sk-hynix-3d-nand-read-disturb-adaptive-reclaim.md).
- DRAM comparison: [`../cases/03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md).
