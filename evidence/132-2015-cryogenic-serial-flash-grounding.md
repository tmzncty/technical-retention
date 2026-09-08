# 2015 cryogenic serial-Flash retention / operability grounding record

This evidence record grounds [`cases/132-cryogenic-serial-flash-retention-operability.md`](../cases/132-cryogenic-serial-flash-retention-operability.md).

**Canonical maturity status is tracked in [`CASE_INDEX.md`](../CASE_INDEX.md).** This slice is deliberately bounded to a 2015 commercial serial-Flash batch experiment. It does not substitute for a general Flash-device history, raw-cell retention physics, SSD qualification, or a cryogenic-electronics genealogy.

## Grounding question

The roadmap already contains strong DRAM evidence that temperature changes residual physical retention after refresh/power withdrawal (Case 127) and SSD evidence that temperature is part of standardized endurance/retention qualification (Case 76). A separate question remained open:

> Can an environmental condition be favorable enough for keeping an already-written nonvolatile state while simultaneously making active read/write/erase service weaker, slower, or temporarily unavailable?

The 2015 Ihmig/Shirley/Zimmermann experiment supplies a bounded Flash example because it deliberately separates functional/performance screening from long-duration retention screening.

---

## Source A — Ihmig, Shirley, Zimmermann 2015

**Document:** Frank R. Ihmig, Stephen G. Shirley, Heiko Zimmermann, “Batch screening of commercial serial flash-memory integrated circuits for low-temperature applications,” *Cryogenics* 71 (2015), DOI `10.1016/j.cryogenics.2015.05.005`.

**Institutional bibliographic record:** <https://publica.fraunhofer.de/entities/publication/bec6d545-e1b1-4a6c-a3cc-ca9d1043ad60>

**Accepted-manuscript access:** <https://www.researchgate.net/publication/277338221_Batch_screening_of_commercial_serial_flash-memory_integrated_circuits_for_low-temperature_applications>

**Evidence class:** `H/P` — peer-reviewed contemporary experimental paper; the accepted manuscript is author-uploaded primary text. Fraunhofer's institutional record independently anchors bibliographic identity and DOI.

**Access/provenance caution:** this slice text-inspected the accepted-manuscript content indexed from the author upload, not a publisher-typeset final PDF facsimile. The record therefore uses section/figure/table identities and reported values without claiming verification of final printed pagination or typography.

### A1. Scope: six batches / 3,600 ICs

The paper reports six production batches of commercial serial Flash-memory ICs manufactured from **2007 to 2012**, with **600 devices per batch** and **3,600 ICs total**.

The authors divide each batch into two experimental groups:

- **Group 1:** 500 ICs per batch for functional/performance characterization across a temperature sequence;
- **Group 2:** 100 ICs per batch for data-retention testing during long-duration cryogenic storage.

This split is evidence that `low-temperature functionality` and `retained-data survival` were experimentally treated as different questions.

**Grounded boundary:** `functional screening != retention screening`.

### A2. Temperature sequence and functional pass boundary

Group 1 was exercised at room temperature and successively colder conditions, including liquid-nitrogen temperature and intermediate test points. The results reported in the manuscript show:

- no observed failures down to **188 K (-85 °C)**;
- some batch-dependent failures beginning at colder points such as **138 K** or **108 K**;
- substantial additional failures near **88 K** and liquid-nitrogen temperature;
- strong batch-to-batch variation rather than one sharp universal device-family threshold.

The article's abstract summarizes the performance change by reporting that page-programming times typically increased by a factor of **4–6 at -196 °C**. Experimental plots/tables additionally show strong low-temperature sector-erase slowdown.

**Grounded boundary:** `same nominal serial-Flash family != one universal cryogenic operating envelope`.

### A3. Low-temperature functional failure was generally reversible

The manuscript states that generally no irreversible functional damage was found and that, after warm-up, all ICs operated properly again at room temperature.

This establishes a bounded counterexample:

```text
failed active operation at cryogenic temperature
    !=
irreversible device failure
```

It does not establish that every stored bit necessarily survives every possible failed command, thermal excursion, or device generation.

### A4. Retention test procedure used written pattern + cryogenic storage + warm verification

For Group 2, the test procedure was distinct from Group 1. The ICs were written with the test pattern **`ALL55`**, the write was verified, and the assemblies were stored in the cryotank gas phase. Temperature and cryogenic-liquid conditions were monitored.

At approximately **six-month intervals**, the retention group was removed, warmed to room temperature, checked for the stored pattern, and returned to cryogenic storage.

That procedure matters because the experimental claim is:

```text
cold storage
    -> warm verification point
    -> recover stored pattern
```

not:

```text
continuous in-situ cryogenic online service
```

**Grounded boundary:** `periodic warm-read verification != continuous cryogenic service`.

### A5. 24-month observed retention result

The manuscript reports **four retention checks over 24 months**. Across those checks it reports **no bit errors** in the stored test pattern. The cryogenic-storage temperature was monitored in a range of approximately **-130 °C to -195 °C**.

This is a strong bounded experimental observation, but its scope is finite:

- tested devices/batches;
- one stated test pattern/procedure;
- 24-month observation window;
- periodic room-temperature verification;
- monitored cryogenic-storage range.

It does not establish a universal Flash-retention rating or zero failure probability.

### A6. Batch/process evolution is part of the observed relation

The paper emphasizes batch-to-batch variation and discusses manufacturing tolerances / product evolution as relevant to the low-temperature behavior. Devices that present the same broad commercial interface can therefore have materially different low-temperature operating margins.

This prevents a timeless abstraction such as `serial Flash works down to temperature X` from being projected onto every manufacturing batch.

---

## Evidence decomposition

The experiment supplies two different retained-state questions.

### Storage relation

```text
already-written bit pattern
    + cryogenic environment
    + elapsed time
    + later warm verification
    -> observed recoverability
```

### Active-operation relation

```text
device
    + current temperature
    + command type
    + timing / electrical margins
    -> program / erase / functional pass or failure
```

The paper's value for `technical-retention` is precisely that those relations can diverge.

---

## Evidence ledger

| Claim | Type | Evidence | Status |
| --- | --- | --- | --- |
| six batches manufactured 2007–2012 were compared | `H/P` | abstract + experimental-design section | strong |
| 3,600 ICs were tested, 600 per batch | `H/P` | experimental-design section | strong |
| Group 1 used 500 ICs/batch for functional/performance tests | `H/P` | experimental-design section | strong |
| Group 2 used 100 ICs/batch for retention tests | `H/P` | experimental-design section | strong |
| no Group-1 failures were observed down to 188 K | `H/P` | functional-results table/discussion | strong bounded result |
| colder failures were batch-dependent | `H/P` | functional-results table / batch comparison | strong |
| page-program time typically increased 4–6x at -196 °C | `H/P` | abstract + performance results | strong |
| low-temperature Group-1 failures were generally reversible after warm-up | `H/P` | results/discussion | strong bounded result |
| retention Group 2 used `ALL55`, cryogenic storage, and periodic warm verification | `H/P` | data-retention procedure | strong |
| four checks over 24 months found no bit errors in the stored pattern | `H/P` | data-retention results | strong bounded result |
| storage temperature was monitored at approximately -130 °C to -195 °C | `H/P` | data-retention results | strong |
| zero errors for 24 months establishes a universal archival lifetime | `X` | sample/duration/procedure do not justify it | rejected |
| successful warm verification proves continuous cryogenic read/write service | `X` | experiment used environmental mode change | rejected |
| cryogenic functional failure proves payload erasure | `X` | warm-up recovery blocks this inference | rejected |
| same temperature effect means same mechanism as DRAM remanence | `A/X` | comparison is functional/environmental only | rejected as mechanism identity |

---

## Engineering reconstruction

### E1. Retention-valid environment and operation-valid environment can differ

The retention group demonstrates recoverability after long cold storage, while the functional group shows severe low-temperature timing/pass-rate degradation. The defensible synthesis is:

```text
state can remain recoverable
while
some active operations are temporarily inadmissible or impractical
```

`Admissible` here is project vocabulary, not the paper's term.

### E2. `environmental suitability` is operation-typed

A single label such as `safe temperature` is too coarse for retention analysis. At minimum, this case requires separate questions for:

- store/hold;
- read/verify;
- page program;
- sector erase;
- warm-up recovery.

### E3. Zero observed errors is an observation, not a universal law

The test can establish `no observed bit errors under the tested procedure for 24 months`. It cannot establish an infinite lower error rate, all-pattern guarantee, all-vendor guarantee, or raw-cell retention model.

### E4. Verification itself has an environmental path

The stored state was periodically brought back to a room-temperature verification condition. Hence future recoverability depends not only on physical bit survival but on the ability to transition from storage environment to a usable access environment without destroying the relevant state.

### E5. Environmental retention can create maintenance through mode switching

The storage regime did not need DRAM-like refresh, but it did require environmental monitoring and scheduled verification. In the intended application, rare writes could be deferred until warmer conditions. That is a bounded example of retention work moving into **temperature management + verification scheduling**, not evidence that Flash requires periodic rewrite to remain nonvolatile.

---

## Cross-case controls

### Case 127 — DRAM power-off remanence

Shared comparison variable: **temperature**.

Different mechanism:

- Case 127: volatile capacitor state after its ordinary refresh/power guarantee has stopped;
- Case 132: an already-written nonvolatile Flash pattern kept in cryogenic storage while active command behavior changes.

Safe analogy:

> temperature is part of a retention relation in both cases.

Rejected identity:

> cooling acts through one historically/mechanically identical retention regime.

### Case 76 — JESD218 SSD endurance / retention qualification

Case 76 composes host-visible TBW, workload, error limits, active-use temperature, and later power-off retention into an SSD-level qualification contract. Case 132 is a component-level experimental excursion far outside ordinary commercial temperature specifications.

Safe boundary:

`experimental cryogenic component result != standardized SSD retention contract`.

### Cases 12–13 — EEPROM / early Flash

Those cases ground electrical erase/program mechanisms and erase geometry. Case 132 should not back-project its 2015 environmental behavior into their earlier devices or infer a shared product genealogy.

---

## Related-repository check

A fresh search of `tmzncty/computing-archaeology` for **`cryogenic`** and **`serial flash`** returned no dedicated case to reuse. Broad low-temperature electronics history, Flash product/process genealogy, packaging, test instrumentation, and cryobiological-electronics history should be built there rather than duplicated here.

The bounded contribution retained in this repository is:

> **a physical environment can preserve an already-written nonvolatile state over the tested interval while narrowing the active command envelope; therefore retention availability, verification availability, and full operational availability must remain separate.**

---

## Historical / provenance cautions

### Do not turn 2015 into an invention date

This source is a direct experimental/documentation floor for the bounded batch study. It is not evidence that cryogenic Flash testing, cold nonvolatile storage, or low-temperature memory electronics originated in 2015.

### Do not infer raw-cell kinetics from the device-level result

The paper reports device-level bit errors, pass rates, and timings. Without a dedicated physical study, this slice does not assert an exact floating-gate threshold-decay mechanism or Arrhenius lifetime model at these temperatures.

### Do not treat the accepted manuscript as a publisher facsimile

The article identity and DOI are institutionally anchored by Fraunhofer; the experimental text was inspected through the author-uploaded accepted manuscript. Exact final-pagination or typesetting claims remain outside this slice.

---

## Readiness assessment

Case 132 meets the repository's `grounded` threshold for its **bounded environmental-retention / operability question**:

- peer-reviewed primary experimental evidence;
- explicit sample/batch scope;
- distinct functional and retention test groups;
- exact experimental-result boundaries;
- counterexamples against universalization;
- cross-case controls against DRAM and JESD218 SSD retention;
- fresh related-repository duplication check;
- no invention-priority or raw-cell-physics overclaim.

Future work should be narrow rather than generic: longer-duration replication, elevated-temperature comparison, direct raw-cell threshold/charge-loss studies, named modern serial-Flash products, independent laboratories, or controlled thermal-cycling fault experiments.