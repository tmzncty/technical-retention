# Case 104 Evidence Index — LPDDR Selective / Adaptive Self-Refresh and Low-Power Retention Boundaries

**Case 104: `grounded`.**

**Canonical case:** [`../cases/104-micron-lpddr-selective-adaptive-self-refresh.md`](../cases/104-micron-lpddr-selective-adaptive-self-refresh.md)

This index keeps five evidence layers separate. They answer different questions and must not be collapsed into a single claim that “LPDDR keeps data in low power.”

```text
refresh-rate control
    !=
refresh-coverage control
    !=
low-power retention mode
    !=
deep-power retention withdrawal
    !=
standards-document identity / revision provenance
```

---

## 1. 2009–2014 Micron TCSR / PASR grounding

[`104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md`](104-micron-2009-2014-lpddr-tcsr-pasr-grounding.md)

**Bounded question:** how can a named LPDDR product vary both the rate and scope of retention maintenance?

**Established:**

- Temperature-Compensated Self Refresh (TCSR) changes refresh-rate policy;
- Partial-Array Self Refresh (PASR) changes which array region remains under self-refresh maintenance;
- the full array may remain ordinarily addressable even though only a selected subset is promised retention during PASR self refresh;
- control metadata can therefore determine future payload survivability without being payload itself.

**Boundary:** `addressable capacity != maintained-retention set`; `maintenance-rate policy != maintenance-scope policy`.

---

## 2. 2014 low-power-state retention boundary

[`104-micron-2014-lpddr-low-power-retention-boundary-deepening.md`](104-micron-2014-lpddr-low-power-retention-boundary-deepening.md)

**Bounded question:** what is the retention difference among Power-Down, SELF REFRESH, and Deep Power-Down in a named Micron LPDDR contract?

**Established:**

- ordinary Power-Down reduces interface activity but does not perform refresh, so residence remains bounded by the refresh requirement;
- SELF REFRESH keeps recurring maintenance inside the device;
- Deep Power-Down removes the documented array-retention condition and requires reinitialization after exit;
- documented data loss is not a sanitization guarantee.

**Boundary:** `Power-Down != powered off`; `SELF REFRESH != passive nonvolatility`; `DPD exit != payload resume`.

---

## 3. 2008–2009 named-product DPD availability / optionality

[`104-micron-hynix-2008-2009-dpd-product-availability-deepening.md`](104-micron-hynix-2008-2009-dpd-product-availability-deepening.md)

**Bounded question:** how early can DPD be tied to named Mobile-DDR product documents, and is feature vocabulary automatically universal across the family?

**Established:**

- Micron June-2008 documentation preserves DPD semantics;
- Hynix May-2009 documentation independently documents DPD but marks it optional;
- the Hynix witness also explicitly states that memory data and MR/EMR information are lost in DPD.

**Boundary:** `documented feature != universal ordering/configuration`; `payload-state loss can coexist with control/configuration-state loss`.

---

## 4. May-2002 pre-LPDDR / Mobile-SDRAM DPD floor

[`104-micron-2002-mobile-sdram-dpd-command-repurposing-deepening.md`](104-micron-2002-mobile-sdram-dpd-command-repurposing-deepening.md)

**Bounded question:** can DPD semantics be found before the later LPDDR standards identity and later named Mobile-DDR documents?

**Established:**

- Micron's May-2002 `ADVANCE` Mobile SDRAM / BAT-RAM document already separates Power-Down, SELF REFRESH, and Deep Power-Down;
- DPD removes the documented payload-retention condition;
- DPD exit requires waiting, PRECHARGE, multiple AUTO REFRESH commands, and MR/EMR initialization before ordinary service;
- the same command pattern is explicitly identified as Burst Terminate on traditional SDRAM but Deep Power-Down on the mobile/BAT-RAM family.

**Boundary:** `electrical exit != service restored != prior payload recovered`; `same command encoding != same operation across device contracts`.

This is a **development-document floor**, not shipment or invention evidence.

---

## 5. 2006–2010 LPDDR standards-number provenance

[`104-jedec-2006-2010-lpddr-numbering-standardization-boundary-deepening.md`](104-jedec-2006-2010-lpddr-numbering-standardization-boundary-deepening.md)

**Bounded question:** when can the first-generation LPDDR JEDEC specification be identified as `JESD79-4` / `JESD209`, and what does that chronology not prove about DPD itself?

**Established:**

- later NXP/Freescale primary documentation independently references `JESD79-4, May 2006` as the LPDDR specification;
- standards-catalog metadata records that `JESD209` was originally numbered `JESD79-4` from May 2006 to August 2007 and was corrected to `JESD209` in September 2007;
- bibliographic/catalog records expose the later `JESD209A`, `JESD209A-1`, and `JESD209B` revision chain through February 2010;
- the full 2006/2007 normative bodies were not directly inspected in this slice, so the exact DPD clause-introduction revision remains open.

**Boundary:** `standards-document chronology != feature-invention chronology`; `renumbering != retention-mechanism transition`; `vendor product floor != standardization floor != shipment floor`.

---

## State taxonomy

Keep at least these Case 104 state classes separate:

| State / relation | Role | Evidence / transition |
| --- | --- | --- |
| DRAM payload charge | user-visible data | refresh / decay / DPD retention withdrawal |
| refresh-rate policy | determines maintenance cadence | TCSR / sensor-oscillator relation |
| refresh-scope policy | determines maintained region | PASR selection |
| ordinary Power-Down state | reduced-activity state with refresh deadline still aging | exit before retention deadline |
| SELF REFRESH state | internal recurring-maintenance authority | device self-refresh machinery |
| DPD state | low-power state outside prior payload-retention promise | power-state exit + reinitialization |
| mode-register / configuration state | determines device behavior | may require reconstruction; Hynix explicitly documents loss in DPD |
| standards-document designation | identifies a normative artifact/revision | `JESD79-4` → `JESD209` → revisions |
| product-document provenance | identifies what one vendor documented at a date | Micron/Hynix revision records |

These states and records have different persistence horizons and different authority.

---

## Cross-layer boundaries

```text
payload presently readable
    !=
payload guaranteed through a selected low-power mode
```

```text
array ordinarily addressable
    !=
array region selected for self-refresh maintenance
```

```text
policy/configuration retained
    !=
payload retained
```

```text
DPD command/state documented by a vendor
    !=
JEDEC feature introduction established
    !=
commercial shipment established
    !=
invention priority established
```

```text
same standards family
    !=
same identifier
    !=
same complete normative wording across revisions
```

---

## Historical vocabulary vs project vocabulary

Historical/source vocabulary includes:

- `Power-Down`;
- `SELF REFRESH`;
- `Deep Power-Down`;
- `temperature-compensated self refresh (TCSR)`;
- `partial-array self refresh (PASR)`;
- `MODE REGISTER` / `EXTENDED MODE REGISTER`;
- `JESD79-4`;
- `JESD209`, `JESD209A`, `JESD209A-1`, `JESD209B`.

Project engineering terms include:

- `retention-scope policy`;
- `maintenance-rate control`;
- `retention withdrawal`;
- `service restoration`;
- `standards-document floor`;
- `product-document floor`;
- `document identity / revision provenance`.

Do not rewrite the project terms as if they were period JEDEC or vendor vocabulary.

---

## Functional comparisons only

Useful bounded comparisons include:

- Case 21: ordinary AUTO REFRESH vs SELF REFRESH authority handoff;
- Case 105: LPDDR2 Per-Bank Refresh standards-level target/coverage accounting;
- Case 135: eMMC retained maintenance-policy configuration;
- Synthesis 26: maintenance-control-state persistence horizons.

These comparisons isolate control-state and maintenance relations. They do not assert shared circuitry, shared standards genealogy, or historical conceptual continuity.

---

## Related-repository routing

Fresh exact-topic searches in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `JESD209` and `LPDDR` returned no dedicated packet to reuse during the standards-provenance slice.

Keep here:

- retention-mode contracts;
- maintenance rate/scope control;
- retained/lost policy and configuration state;
- standards-version provenance where it changes what retention claim is authorized;
- product-vs-standard-vs-shipment evidence boundaries.

Route broad mobile-DRAM standards history, committee process, market adoption, packaging, product competition, and controller evolution to `computing-archaeology` if developed later.

---

## Current evidence debt

The highest-value remaining Case 104 work is narrower than before:

1. directly inspect May-2006 `JESD79-4` and the 2007 `JESD209` body/revision material;
2. establish the exact revision in which DPD appears and its mandatory/optional status;
3. trace PASR and TCSR standardization separately instead of assuming a shared chronology;
4. recover JEDEC ballot/proposal metadata if available, without turning proposal authorship into invention priority;
5. add a period named controller/product explicitly citing the then-current standard revision;
6. separate compliance documentation from sample availability, ordering, volume shipment, and field deployment;
7. pursue remanence/fault-injection only as a separate experimental layer, not as a substitute for interface history.

No maturity promotion follows from the standards-number provenance packet. **Case 104 remains `grounded`.**
