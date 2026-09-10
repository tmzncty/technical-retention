from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SYNTHESIS = r'''# Synthesis 27 — Retention-Policy Evidence: Representativeness, Freshness, Authority, and Revalidation

> **Question:** when preservation work is conditioned on a sensor, proxy, profile, status field, or runtime error observation, what makes that evidence safe to use *now* as an input to maintenance policy?

**Status:** bounded cross-case synthesis over already-grounded DRAM evidence. This document does not add a new invention-priority claim, does not assert one genealogy among the mechanisms, and does not treat every environmental or health signal as the same kind of state.

Grounded witnesses used here:

- [`Case 10 — Toshiba leakage-tracked self refresh`](../cases/10-toshiba-leakage-tracked-self-refresh.md): a deliberately decaying leak-monitor state can trigger maintenance before protected payload cells are expected to cross their loss boundary;
- [`Case 34 — Micron temperature-dependent refresh`](../cases/34-micron-temperature-dependent-dram-refresh.md): sensed environment can be discretized into a cadence policy, while later DDR3 `SRT` / `ASR` product semantics separate declared envelope from automatic measurement-driven policy;
- [`Case 35 — Micron Mobile DDR automatic TCSR`](../cases/35-micron-mobile-ddr-automatic-tcsr.md): an on-die temperature sensor can automatically control self-refresh cadence while host-visible `TCSR` bits are ineffective on the bounded product and `PASR` independently controls retention coverage;
- [`Case 40 — RAIDR retention-aware refresh`](../cases/40-raidr-retention-aware-dram-refresh.md): a measured row-retention profile can be retained as controller state, while DPD/VRT evidence shows that representation persistence does not guarantee future validity;
- [`Case 43 — AVATAR VRT-aware feedback`](../cases/43-avatar-vrt-aware-dram-refresh-feedback.md): ECC and proactive scrub can provide runtime evidence that revises a row's refresh class, with later retention testing required for less-conservative reclassification;
- [`Case 93 — DRAM VRT profile staleness`](../cases/93-dram-variable-retention-time-profile-staleness.md): a profile may survive across boots while the physical relation it represents changes or was incompletely observed;
- [`Case 133 — LPDDR4 MR4 thermal offset`](../cases/133-micron-lpddr4-mr4-thermal-offset-refresh-authority.md): sensor placement, status-update latency, host polling, controller response, and a writable thermal offset become explicit parts of the retention-control relation.

The historical claims remain in those case/evidence records. The phrase **`maintenance-policy evidence`** is used here only as an engineering umbrella for an observation, proxy, classification, retained profile, status field, or error signal that is consumed when deciding how much preservation work is due, where it should apply, or whether a prior policy remains admissible. It is not historical DRAM vocabulary and it does not imply a correctness certificate.

---

## 1. Verdict

The cases support a distinction that is not captured by either `metadata persisted` or `sensor available`:

> **The persistence of a maintenance-policy input, the current validity of what it represents, and the authority granted to it are separate relations.**

A useful comparison therefore needs at least this chain:

```text
physical retention constraint / environment
    !=
observation or proxy
    !=
spatial / temporal / contextual representativeness
    !=
retained representation or status
    !=
policy interpretation / guardband
    !=
authority to select maintenance
    !=
maintenance execution
    !=
future payload outcome
```

The same bit pattern can remain perfectly intact in a profile table while becoming unsafe to trust. Conversely, a short-lived or repeatedly sampled signal can remain operationally useful without being a durable historical record. A conservative approximation can be less precise yet safer than a more exact-looking stale value. And a field can exist in an interface without having effective software authority over the bounded product.

This synthesis therefore adds one cross-case audit question to the repository:

> **What proposition does the evidence support, under what spatial, temporal, contextual, and failure assumptions, and what revalidation path exists when those assumptions may no longer hold?**

---

## 2. Claim discipline

Following [`METHOD.md`](METHOD.md) and [`../AGENTS.md`](../AGENTS.md):

- **H/P — historical / primary:** source vocabulary, dates, measured behavior, product contracts, and implementation claims stay in the individual cases and evidence records;
- **E — engineering reconstruction:** `maintenance-policy evidence`, `representativeness`, and the validity/authority decomposition below are project analytical tools;
- **A — functional analogy:** comparing a leak monitor, a temperature sensor, a retained row profile, and an ECC event by their policy role does not make them the same physical mechanism or establish descent;
- **I — philosophical interpretation:** the final interpretation is limited to the fact that persistence can depend on fallible technical representations of preservation conditions.

The synthesis deliberately does **not** claim that the historical actors shared a concept of `evidence validity`, that all adaptive refresh descends from one invention, or that DRAM retention control is a general model of knowledge.

---

## 3. Why this is not Synthesis 24 or Synthesis 26 again

[`SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md`](SYNTHESIS_24_RETENTION_MAINTENANCE_TRIGGER_REGIMES.md) asks **what makes preservation work due**: elapsed time, access, capacity pressure, wear, failure, and so on. It already notes that evidence-conditioned and environment-conditioned policies can modify those regimes.

[`SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md) asks **how long auxiliary preservation state must survive and how it is reconstituted**: reinitialize, replay, reload, compare copies, re-observe, or accumulate.

The present synthesis asks a third question:

> **Even if the policy input exists and is available, why should the system trust it as a sufficiently conservative representation of the condition that matters now?**

These axes are orthogonal:

```text
trigger regime
    = what makes work due?

persistence horizon
    = how long must the control state survive?

policy-evidence validity
    = under what conditions is that state/observation safe to use?
```

Therefore:

> **same trigger != same evidence-validity problem**

and

> **same persistence horizon != same representativeness or authority**.

---

## 4. Comparison axes

For a maintenance-policy input, audit at least these axes:

| Axis | Question |
| --- | --- |
| **protected relation** | What payload or retention margin is being protected? |
| **physical condition** | What actually constrains retention: leakage, temperature, VRT state, disturbance exposure, or another mechanism? |
| **observation / proxy** | What is actually measured or retained? Sensor value, proxy decay, status class, profile, error event? |
| **spatial representativeness** | Does the observation stand for one cell, row, die, sensor location, package, or external hot spot? |
| **temporal freshness** | How old can the observation/profile be before policy may be unsafe? |
| **context qualification** | Does validity depend on data pattern, temperature, lifecycle stage, operating mode, or another condition? |
| **representation granularity** | Is a continuous condition reduced to bands, bins, flags, or one row-level minimum? |
| **approximation direction** | If the representation is wrong, does it cause extra maintenance or unsafe under-maintenance? |
| **policy authority** | Is the state advisory, automatically controlling, host-programmable, ignored, or merely reported? |
| **revalidation path** | Poll again, observe an error, scrub, retention-test, fall back conservatively, or do something else? |
| **execution closure** | Does selecting the policy prove the required refresh/repair actually occurred? |

No case should fill an unknown entry by analogy with another mechanism.

---

## 5. A proxy can be useful without being the protected state

Case 10 is the cleanest early counterexample to `measurement = payload condition`. Toshiba's disclosed preferred embodiment uses a monitor capacitor whose controlled decay is observed to start a refresh pass. The monitor may be designed to leak slightly faster than ordinary memory cells so that the control boundary is reached conservatively.

The monitor therefore has value precisely because it is **not** the payload. It is a different physical state engineered to stand in a safety relation to the protected array.

Case 34 similarly uses a temperature sensor near the DRAM array, then maps the sensed value into discrete bands and an oscillator/refresh cadence. The sensor observes an environmental variable; it does not directly measure every cell's remaining charge or future retention time.

Therefore:

> **policy-relevant proxy != protected physical state**

and

> **proxy usefulness != proxy identity with the thing protected**.

The engineering question is not whether the proxy is `really the same` as retention. It is whether the documented relation is conservative enough for the policy that consumes it.

---

## 6. Representativeness has spatial, temporal, and contextual dimensions

### Spatial representativeness

Case 133 makes the spatial problem explicit. Micron warns that a tightly coupled SoC can create a hot spot that is not near the memory's thermal sensor. The reported condition can therefore understate the retention-relevant temperature elsewhere in the coupled system. A controller thermal offset is provided to compensate the TCSR policy for a bounded sensor-to-hot-spot gradient.

This is not merely numerical sensor `accuracy`:

> **sensor accuracy != spatial representativeness**.

A perfectly calibrated sensor at one location can still be the wrong observation for another physically hotter location.

### Temporal representativeness

The same case gives a bounded freshness chain: internal sensor update delay (`tTSI`), host MR4 polling interval, and system response delay all contribute to how old the effective environmental knowledge can become under a changing thermal condition. The status may be valid when produced yet unsafe if acted on too late.

Thus:

> **observation timestamp/freshness problem != payload refresh deadline**, even when both ultimately constrain preservation.

### Contextual representativeness

Cases 40 and 93 show a different problem. A row-retention profile can depend on data pattern (`DPD`), can miss a later variable-retention-time (`VRT`) transition, and can be qualified by the duration and lifecycle stage of the profiling experiment. The same row address does not guarantee that one measured retention number remains a context-free truth.

Therefore:

> **address identity != retention-behavior identity**

and

> **measurement under one context != universal future validity**.

These three forms of representativeness should not be collapsed into a generic statement that `the sensor/profile may be inaccurate`.

---

## 7. Retaining a representation can preserve the wrong answer

Case 40 supplies a decisive counterexample to treating durability of control metadata as sufficient. RAIDR explicitly discusses saving retention-profile results for later boots. The 2013 DPD/VRT measurements then show that the represented physical relation can change or can have been incompletely observed.

Case 93 makes this second-order problem explicit:

```text
profile bits survive
    +
row identity survives
    +
controller successfully reloads the profile
    !=
profile remains conservative for the current physical state
```

So:

> **representation persistence != represented-relation validity**.

This is not ordinary metadata corruption. The stored profile can be byte-for-byte correct relative to an earlier measurement and still become unsafe to use later.

The distinction matters because `more durable metadata` can actually preserve a stale policy input more effectively. Durability is not itself a guarantee of epistemic or engineering currentness.

---

## 8. Policy configuration, observation, and authority are different states

Case 34's later DDR3 product witness separates manual `SRT` from automatic `ASR`. `SRT` can conservatively force a higher self-refresh rate for an extended-temperature envelope without claiming a current temperature measurement; `ASR` instead allows the device to select between rates automatically.

Therefore:

> **declared operating envelope != measured environmental condition**.

Case 35 adds an even sharper interface warning: `TCSR`-labelled bits are present in the bounded product's register definition, but programming them has no effect because an on-die sensor automatically controls the self-refresh oscillator. At the same time `PASR` remains separately programmable and controls which parts of the array are retained.

Therefore:

> **field presence != effective software authority**

and

> **cadence authority != retention-coverage authority**.

Case 133 then adds a controller-writable thermal offset adjacent to read-only status. The host can observe one state and write another state that changes TCSR behavior. The offset is a policy correction, not a recalibration of the physical sensor.

So the policy path must keep at least these distinct:

```text
observation
    !=
configuration
    !=
interpretation/guardband
    !=
authority
    !=
actuation
```

---

## 9. Fresh status is not history

Case 133's `TUF` is deliberately compressed. It records whether the reported refresh-rate class changed since the previous MR4 read and is cleared by that read. It does not preserve each sensor sample, timestamp, intermediate class, or physical temperature trajectory.

Therefore:

> **change-since-last-observation evidence != event history**.

This matters because a maintenance controller may need only enough evidence to decide the next action, not a durable historical account of everything the environment did.

Case 40's retention bin is similarly not a history of the profiling process. A current class can be operationally useful while omitting the measurements and transitions that produced it.

Thus:

> **policy-input state != provenance-complete history**.

When provenance matters for later audit or revalidation, it must be established separately rather than inferred from the current policy value.

---

## 10. Approximation direction can matter more than precision

RAIDR's Bloom-filter use provides a precise engineering example. A false positive can classify an ordinary row as needing more frequent refresh, wasting maintenance work but remaining conservative under the model. A dangerous omission would instead under-refresh a genuinely weak row.

AVATAR uses a similar asymmetry at the policy level. A correctable ECC event may have a cause other than VRT, yet the design can conservatively upgrade the affected row to `Fast Refresh`. The evidence is not perfectly specific, but the chosen error direction spends more maintenance rather than risking under-maintenance.

Therefore:

> **less specific evidence can be safer than stale precise-looking evidence**

and

> **approximation error must be evaluated by direction and consequence, not only magnitude**.

This also explains why downgrade authority is different from upgrade authority. Moving to more maintenance can often be justified by weak evidence; moving back to less maintenance may require a stronger retention test or other revalidation.

> **conservative upgrade authority != downgrade authority**.

---

## 11. Observation coverage is part of evidence validity

Case 43 shows why a correct detection mechanism can still be insufficient. ECC on ordinary accesses can expose and correct errors only in data that are actually accessed. Cold memory can remain unobserved, so AVATAR adds proactive scrub to extend coverage.

Therefore:

> **correction capability != observation coverage**.

And because a scrub traversal is distinct from charge refresh:

> **verification/revalidation work != preservation actuation**.

Case 133's polling interval gives the same structural lesson at a different mechanism boundary: a status interface can be correct when read, yet the system can observe it too infrequently for the permitted environmental rate of change.

Coverage is therefore not only spatial. It can be temporal, workload-dependent, or mode-dependent.

---

## 12. Revalidation is itself a maintenance relation

Cases 40/93 show the problem of a profile that can become stale. Case 43 supplies one bounded response: runtime ECC evidence and proactive scrub can cause conservative row upgrades, while a separate retention test can later authorize downgrade.

Case 133 supplies another response class: re-read current MR4 status within the documented timing relation and update the controller's thermal offset when the bounded sensor-to-hot-spot relation requires it.

These are not the same mechanism, but both show:

```text
policy state at t0
    -> environment/substrate may change
    -> new observation
    -> qualification / interpretation
    -> policy revision or conservative fallback
```

Therefore:

> **maintenance-policy state may itself require maintenance**.

But that sentence must not be inflated into recursive metaphor. The concrete operations are polling, testing, scrubbing, correction, comparison, and reclassification.

Revalidation also has a cost. More frequent polling, scrubbing, retention testing, finer sensors, or finer classification consumes energy, bandwidth, time, or implementation complexity. Case 34 already makes that tradeoff explicit at the comparator/control-circuit level; Case 43 makes it explicit in scrub/retest overhead.

> **adaptive maintenance != free maintenance**.

---

## 13. Selecting a policy does not prove preservation occurred

The final boundary is operational. A valid policy input can select the correct cadence, but the required refresh still has to execute correctly. Conversely, an executed refresh schedule can be unsafe if the policy that chose it was based on stale or unrepresentative evidence.

The full chain is therefore:

```text
condition / constraint
    -> evidence
    -> qualification
    -> policy selection
    -> authority/admission
    -> command generation
    -> physical restoration
    -> later recoverability
```

No single edge certifies all later edges.

Hence:

> **valid evidence != executed maintenance**

> **executed maintenance != future-safety proof under an invalid policy model**

> **successful present read != future retention margin**.

The last rule also connects functionally to the repository's NAND/SSD cases, but no cross-technology genealogy is asserted here.

---

## 14. Cross-case matrix

| Case | Evidence / representation | Main validity question | Policy authority | Revalidation / fallback |
| --- | --- | --- | --- | --- |
| **10** | decaying leak-monitor capacitor / detector threshold | is the proxy conservatively related to protected cells? | disclosed on-chip trigger starts refresh sequence | recharge/restart monitor cycle after refresh; product fault behavior not established |
| **34** | nearby temperature sensor + bands; later SRT/ASR controls | is environment represented conservatively and at useful granularity? | system/device policy selects cadence depending on bounded embodiment | conservative fixed SRT or automatic ASR in later product witness; no universal genealogy |
| **35** | on-die sensor + product register semantics | which interface state actually controls cadence, and what region remains entitled to retention? | automatic TCSR path controls cadence; PASR separately controls coverage | product contract only; sensor-fault requalification remains open |
| **40 / 93** | profiled row-retention bins / saved profile | does measured behavior remain conservative across DPD, VRT, time, pattern, and lifecycle? | controller profile selects row-specific cadence | re-profiling/guardbanding required in principle; 2013 evidence exposes static-profile limits |
| **43** | ECC events + scrub observations + RRT class | are enough locations observed, and is an error specific enough to justify class change? | runtime event can conservatively upgrade row policy | proactive scrub + later retention test; downgrade uses stronger evidence |
| **133** | MR4 refresh-rate class, TUF, sensor location, controller offset | is status fresh and spatially representative of the retention-relevant hot spot? | device status + controller offset jointly shape TCSR behavior | timed polling/response and offset adjustment within documented gradient envelope |

The matrix compares **relations**, not historical descent.

---

## 15. Counterexamples fixed by the comparison

The grounded cases reject the following shortcuts:

- **`sensor exists -> condition is known` — rejected.** Sensor placement and update timing can limit what is known for the retention decision.
- **`profile persisted -> profile remains valid` — rejected.** DPD/VRT can invalidate a perfectly preserved profile relation.
- **`field exists -> software controls the function` — rejected.** Case 35's TCSR bits are a direct product counterexample.
- **`current status -> complete history` — rejected.** TUF is a read-to-clear change indicator, not a temperature log.
- **`more precise representation -> safer policy` — rejected as a universal rule.** Conservative approximation direction matters.
- **`ECC can correct -> all vulnerable memory is observed` — rejected.** Demand visibility and proactive coverage are separate.
- **`error observed -> cause uniquely diagnosed` — rejected.** AVATAR explicitly allows conservative over-classification.
- **`policy selected -> maintenance executed` — rejected.** Selection, command authority, and physical restoration remain distinct.
- **`adaptive policy -> no guardband` — rejected.** Case 34 explicitly retains guardband/control tradeoffs.
- **`revalidation -> proof of permanent future safety` — rejected.** Revalidation has its own coverage, timing, model, and lifecycle limits.

---

## 16. Prior-art and genealogy stop conditions

This synthesis makes no invention-priority claim. The individual cases already preserve the important historical boundaries:

- Case 10 independently grounds earlier Hitachi leakage-comparator self-refresh prior art rather than treating Toshiba as origin;
- Case 34 preserves a 1987-priority temperature-conditioned DRAM-refresh floor before Micron's 1991 filing;
- Case 35 is a commercial product-contract witness, not a JEDEC revision chronology;
- RAIDR and AVATAR are research mechanisms with their own cited predecessors and are not presented as commercial deployment;
- Case 133 uses Micron and SK hynix product documentation to bound one LPDDR4-era relation while explicitly withholding a complete standards genealogy.

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for the combined `MR4 / TCSR / thermal offset / VRT / retention profile` relation found no dedicated cross-technology treatment to reuse. Broader DRAM-generation history, JEDEC revision chronology, sensor circuitry, controller implementations, and invention genealogy should still be developed there rather than duplicated here.

The present document keeps only the retention-specific relation:

> **what qualifies a representation of preservation conditions to control preservation work?**

---

## 17. Philosophical interpretation — bounded

The exact technical fact is modest: some retention systems do not act directly from the protected state alone. They act from **representations of the conditions under which that state is expected to remain recoverable** — a proxy capacitor, temperature status, retained row profile, or error observation.

Those representations can be:

- conservative or non-conservative;
- fresh or stale;
- spatially representative or misplaced;
- context-qualified or overgeneralized;
- authoritative, advisory, ignored, or only one input among several;
- revalidated through later observation and maintenance work.

The narrow conceptual payoff is:

> **technical persistence can depend on maintaining not only a state, but a sufficiently valid operational relation between that state, its changing conditions, and the policy that decides what preservation work is owed.**

That does not mean the machine `knows` its condition in a human sense, nor that a sensor/profile is memory of memory. It means only that the engineering architecture contains fallible representational links whose validity affects whether preservation work is adequate.

---

## 18. Research consequences

Future retention cases that use environmental, health, wear, integrity, or profile evidence should answer explicitly:

1. What physical condition actually constrains the retained target?
2. What does the system measure or retain instead of that condition directly?
3. What spatial region does the observation represent?
4. How fresh must it be?
5. What context qualifies the observation or model?
6. What approximation/quantization occurs, and which error direction is safe?
7. What authority does the resulting state actually have in the bounded implementation?
8. What maintenance action follows, and how is execution distinguished from selection?
9. What observation coverage is required before the evidence can be trusted?
10. How can the state be revalidated, conservatively upgraded, downgraded, or discarded?
11. What happens if the representation survives but becomes stale?
12. Which historical vocabulary is source-native, and which comparison terms are project reconstruction?

This is a comparison discipline, not an exhaustive taxonomy.
'''

README_INSERT = r'''

A bounded retention-policy-evidence synthesis is now available in [`docs/SYNTHESIS_27_RETENTION_POLICY_EVIDENCE_VALIDITY.md`](docs/SYNTHESIS_27_RETENTION_POLICY_EVIDENCE_VALIDITY.md). Across grounded DRAM leak-monitor, temperature-conditioned refresh, TCSR/PASR, RAIDR/VRT, AVATAR, and LPDDR4 MR4 cases it separates the protected physical condition, observation/proxy, spatial and temporal representativeness, context qualification, retained representation, approximation direction, policy authority, revalidation coverage, maintenance execution, and future payload outcome. It fixes the counterexamples `representation persisted != represented relation remains valid`, `sensor exists != condition is sufficiently known`, `field exists != software authority`, `current status != history`, `correction capability != observation coverage`, and `policy selected != maintenance executed`.
'''

ROADMAP_INSERT = r'''
- [x] Distinguish maintenance-policy evidence from the protected state and audit its representativeness, freshness, context qualification, approximation direction, authority, observation coverage, and revalidation path — bounded by [`docs/SYNTHESIS_27_RETENTION_POLICY_EVIDENCE_VALIDITY.md`](docs/SYNTHESIS_27_RETENTION_POLICY_EVIDENCE_VALIDITY.md): grounded Cases 10, 34, 35, 40, 43, 93, and 133 show that a proxy/profile/status can remain available while becoming non-conservative, that sensor placement and polling latency are separate validity dimensions, that interface-field presence need not imply effective control authority, and that conservative upgrade can require weaker evidence than downgrade. This closes only the cross-case relation `policy-input persistence != policy-input validity != policy authority`; complete JEDEC genealogy, commercial adaptive-refresh deployment, sensor fault characterization, and broad DRAM controller history remain companion-repository work.
'''

INDEX_APPEND = r'''

## Synthesis 27 — retention-policy evidence validity findings

Evidence: [`docs/SYNTHESIS_27_RETENTION_POLICY_EVIDENCE_VALIDITY.md`](docs/SYNTHESIS_27_RETENTION_POLICY_EVIDENCE_VALIDITY.md), synthesized only from already-grounded Cases 10, 34, 35, 40, 43, 93, and 133.

- **2785 — maintenance-policy evidence != protected payload/condition:** a leak monitor, temperature status, row profile, or ECC event can influence preservation without being the state it protects. (`E`)
- **2786 — useful proxy != physical identity with the protected condition:** Case 10's deliberately conservative leak monitor and Case 34's environmental sensor are separate physical states whose value lies in a bounded relation to payload retention. (`H/P`, `E`)
- **2787 — sensor availability != sufficient representativeness:** an observation can exist and be numerically valid while failing to represent the retention-relevant location or condition. (`H/P`, `E`)
- **2788 — spatial representativeness != sensor accuracy:** Case 133's sensor-to-hot-spot gradient shows that calibration/accuracy at one location does not prove knowledge of a hotter coupled location. (`H/P`, `E`)
- **2789 — policy-evidence freshness deadline != payload refresh deadline:** `tTSI`, host polling, and response latency constrain how current the control observation is, while physical refresh remains a separate preservation obligation. (`H/P`, `E`)
- **2790 — representation persistence != represented-relation validity:** a saved retention profile can survive correctly while VRT/DPD or later lifecycle conditions make it non-conservative. (`H/P`, `E`)
- **2791 — context-qualified measurement != universal future minimum:** data pattern, profiling duration, temperature, lifecycle stage, and operating mode can qualify what a retention measurement means. (`H/P`, `E`, `X`)
- **2792 — declared operating envelope != measured environmental condition:** Case 34's later `SRT` / `ASR` split shows that a conservative configured policy and automatic measurement-driven policy are distinct ways to cover a retention envelope. (`H/P`, `E`)
- **2793 — interface-field presence != effective software authority:** Case 35's documented but ineffective TCSR programming bits block inference from register names to actual control locus. (`H/P`, `X`)
- **2794 — current/change status != history:** LPDDR TUF and row-policy classes can support current decisions without preserving the full sequence of environmental samples, transitions, or profiling events. (`H/P`, `E`)
- **2795 — approximation safety depends on error direction:** RAIDR Bloom-filter false positives can cause conservative over-refresh, while unsafe omissions/underclassification are categorically different. (`H/P`, `E`)
- **2796 — conservative upgrade authority != downgrade authority:** AVATAR can react to a correctable error by spending more refresh work, while later reduction of that work requires separate retention testing/revalidation. (`H/P`, `E`)
- **2797 — correction capability != observation coverage:** demand-time ECC can correct an observed error without covering cold memory; proactive scrub extends observation but remains distinct from refresh. (`H/P`, `E`)
- **2798 — valid policy input != maintenance execution != future-safety proof:** evidence qualification, policy selection, refresh command generation/restoration, and later recoverability are separate stages. (`E`, `X`)
- **2799 — cross-case comparison is relational, not genealogical:** leak-monitor, temperature-sensor, retention-profile, ECC/scrub, and MR4/thermal-offset mechanisms are compared by evidence/authority roles only; broader DRAM/JEDEC/controller history remains routed to `computing-archaeology`. (`A`, `X`, `H/P` project-state record)
'''

README_MARKER = "A bounded maintenance-control-state persistence-horizon synthesis is now available in [`docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md). Across grounded DRAM, raw-NAND, SSD telemetry, and HDFS cases it separates regime-local phase, restart-progress checkpoint, qualification/currentness map, retained policy, re-observed runtime evidence, and cumulative event-history summary. It fixes the counterexamples `maintenance-control state != durable checkpoint`, `persistence horizon != authority`, `checkpoint != correctness certificate`, `reconstructable != consequence-free`, and `policy retention != effective implementation behavior`."

ROADMAP_MARKER = "- [x] Distinguish maintenance-control-state role, authority, reconstitution path, and persistence horizon — bounded by [`docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md`](docs/SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md): grounded Cases 09, 15, 78, 83, and 116 separate regime-local cyclic phase, restart-progress checkpoint, restart-persistent qualification/currentness state, retained policy, re-observed runtime embodiment evidence, and cumulative event-history summary. This closes only the cross-case decomposition `maintenance-control state != one universal durable-checkpoint contract`; mechanism genealogy, implementation-specific fault atomicity, and broader DRAM/NAND/SMART/HDFS history remain routed to `computing-archaeology`."


def insert_after(path: Path, marker: str, insertion: str, unique_token: str) -> None:
    text = path.read_text(encoding="utf-8")
    if unique_token in text:
        return
    if marker not in text:
        raise SystemExit(f"marker missing in {path}")
    text = text.replace(marker, marker + insertion, 1)
    path.write_text(text, encoding="utf-8")


synth_path = ROOT / "docs/SYNTHESIS_27_RETENTION_POLICY_EVIDENCE_VALIDITY.md"
if synth_path.exists():
    current = synth_path.read_text(encoding="utf-8")
    if current != SYNTHESIS.strip() + "\n":
        raise SystemExit("Synthesis 27 already exists with different content")
else:
    synth_path.write_text(SYNTHESIS.strip() + "\n", encoding="utf-8")

insert_after(
    ROOT / "README.md",
    README_MARKER,
    README_INSERT,
    "SYNTHESIS_27_RETENTION_POLICY_EVIDENCE_VALIDITY.md",
)
insert_after(
    ROOT / "ROADMAP.md",
    ROADMAP_MARKER,
    "\n" + ROADMAP_INSERT,
    "policy-input persistence != policy-input validity != policy authority",
)

index_path = ROOT / "CASE_INDEX.md"
index_text = index_path.read_text(encoding="utf-8")
if "## Synthesis 27 — retention-policy evidence validity findings" not in index_text:
    if "**2784 —" not in index_text:
        raise SystemExit("expected current CASE_INDEX tail finding 2784 not found")
    index_path.write_text(index_text.rstrip() + INDEX_APPEND + "\n", encoding="utf-8")

# Bounded local assertions: fail rather than silently duplicate or mis-anchor.
checks = {
    ROOT / "README.md": ["SYNTHESIS_26_MAINTENANCE_CONTROL_STATE_PERSISTENCE_HORIZONS.md", "SYNTHESIS_27_RETENTION_POLICY_EVIDENCE_VALIDITY.md"],
    ROOT / "ROADMAP.md": ["policy-input persistence != policy-input validity != policy authority"],
    ROOT / "CASE_INDEX.md": ["**2785 —", "**2799 —", "Synthesis 27 — retention-policy evidence validity findings"],
    synth_path: ["representation persistence != represented-relation validity", "sensor accuracy != spatial representativeness", "conservative upgrade authority != downgrade authority"],
}
for path, needles in checks.items():
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"missing assertion {needle!r} in {path}")

print("Synthesis 27 staged successfully")
