# 3D NAND Early Retention Loss: Front-Loaded Charge Loss, Retention Age, and Read-Reference Adaptation

## Status

**`grounded`** — bounded to the retention-specific transition from earlier charge-trapping NAND fast-initial-charge-loss evidence (2010), through a 2016 tube-type 3D NAND early-retention study, to Luo et al.'s 2018 experimental characterization of real 3D NAND MLC chips and their **Retention Model Aware Reading (ReMAR)** proposal. A follow-on deepening isolates the same 2018 paper's **retention interference** measurements and **Retention Interference Aware Neighbor-Cell Assisted Correction (ReNAC)** proposal. A manufacturer-design deepening adds Toshiba / Toshiba Memory patent evidence for adaptive and elapsed-time-conditioned NAND read-voltage tracking, including nonvolatile reference-time/control records loaded into volatile controller working state after power-on. A 2022–2024 TLC deepening adds direct peer-reviewed TLC retention/read-voltage evidence rather than carrying the 2018 MLC result forward by projection. A 2019–2024 QLC deepening now closes the minimal **direct QLC measurement** gap for retention-conditioned threshold/error/read-voltage behavior while keeping cross-generation quantitative portability and commercial-controller deployment open.

The manufacturer material closes only a **patent/design-witness** portion of the open deployment question. It does not establish that a named retail SSD shipped ReMAR, ReNAC, or the exact Toshiba disclosed mechanism. The later TLC and QLC evidence closes generation-specific measurement gaps only; named-controller deployment, directly comparable cross-generation curves, and device-specific long-horizon QLC behavior remain open.

Evidence navigation:

- grounding: [`../evidence/65-3d-nand-2010-2018-early-retention-grounding.md`](../evidence/65-3d-nand-2010-2018-early-retention-grounding.md)
- retention-interference / ReNAC deepening: [`../evidence/65-luo-2018-retention-interference-renac-deepening.md`](../evidence/65-luo-2018-retention-interference-renac-deepening.md)
- Toshiba / Toshiba Memory age-aware read-tracking and metadata deepening: [`../evidence/65-toshiba-2014-2018-age-aware-read-tracking-metadata-deepening.md`](../evidence/65-toshiba-2014-2018-age-aware-read-tracking-metadata-deepening.md)
- direct TLC retention/read-voltage deepening: [`../evidence/65-2022-2024-tlc-retention-read-voltage-deepening.md`](../evidence/65-2022-2024-tlc-retention-read-voltage-deepening.md)
- direct QLC retention/read-threshold deepening: [`../evidence/65-2019-2024-qlc-retention-read-threshold-deepening.md`](../evidence/65-2019-2024-qlc-retention-read-threshold-deepening.md)

## Scope

This case asks a narrow question left open by Cases 36, 52, and 59:

> What changes when a nonvolatile 3D charge-trap NAND cell loses a disproportionate amount of retention margin soon after programming, so that the age of the data can become an input to later read interpretation — and when the retained state of a vertically adjacent cell can further condition that aging trajectory?

The bounded object is **early retention loss / fast initial charge loss** in charge-trapping NAND, with special attention to:

1. the 2018 extended-duration characterization of real 3D NAND MLC chips;
2. its age-aware ReMAR proposal;
3. its separately measured neighbor-conditioned **retention interference** phenomenon and ReNAC proposal;
4. Toshiba / Toshiba Memory manufacturer design records showing that adaptive read-voltage tracking and later elapsed-time-conditioned tracking can depend on retained controller metadata whose durable and runtime representations have different persistence horizons;
5. direct 2022–2024 3D-TLC evidence showing retention-after-cycling read-voltage adaptation and history-conditioned later retention results without assuming quantitative portability from the 2018 MLC population; and
6. direct 2019–2024 3D-QLC evidence showing measured retention-conditioned threshold/error/read-voltage behavior without treating TLC as a substitute for QLC measurement.

This is **not**:

- a complete history of 3D NAND or charge-trap Flash;
- evidence that every 3D NAND generation, TLC/QLC product, or vendor has the same early-retention curve or retention-interference magnitude;
- a claim that 2018 invented fast initial charge loss or first observed early retention in 3D NAND;
- evidence that ReMAR or ReNAC shipped in a named commercial SSD/controller;
- evidence that the Toshiba patent embodiments shipped unchanged in a named retail SSD;
- a claim that Toshiba's elapsed-time-conditioned tracking is ReMAR or that either design derives from the other;
- a claim that a 2017 patent-priority filing was already a 2017 public disclosure;
- a modern device-specific `read reclaim` case;
- the same mechanism as Case 36's planar-NAND Flash Correct-and-Refresh (FCR), Case 52's read disturb, or Case 59's program interference;
- a claim that retention interference, layer-to-layer process variation, early retention loss, and read disturb are one phenomenon;
- a claim that the 2018 paper demonstrated a meaningful ReNAC lifetime improvement on its tested generation; the paper explicitly says it did not;
- a claim that direct QLC measurement makes the 2018 MLC or 2022–2024 TLC curves quantitatively portable to QLC.

The 2018 authors characterize chips from a major vendor but do not identify the vendor/product. Numerical results remain bounded to their test population and model assumptions. The Toshiba material is used as manufacturer-primary **design disclosure**, not as measured product deployment evidence. The 2022/2024 TLC and 2019/2024 QLC sources are research-device evidence, not proof of a named shipping controller policy.

## Historical vocabulary and chronology

### `fast initial charge loss` before the 2018 3D-NAND characterization

C.-P. Chen and colleagues' IEDM 2010 paper is titled **“Study of fast initial charge loss and its impact on the programmed states Vt distribution of charge-trapping NAND flash.”** Its published record places `fast initial charge loss` explicitly in charge-trapping NAND well before the 2018 ReMAR work.

This matters for priority:

> **2018 extended 3D-NAND characterization ≠ invention of fast initial charge loss in charge-trapping NAND.**

The 2010 result is used as prior art only. This repository does not project later 3D device organization, ReMAR policy, or the 2018 24-day experimental curve backward onto it.

### `early retention` in tube-type 3D NAND by 2016

Bongsik Choi and colleagues' 2016 VLSI Technology paper uses **`early retention`** for fast charge loss within seconds in tube-type, word-line-stacked 3D NAND. Its abstract reports measurements from microseconds to seconds and attributes the bounded behavior mainly to lateral charge loss through shared charge-trap layers, with sensitivity to program/erase levels.

The authors frame this as the first observation of early retention in their tube-type 3D NAND regime. The present repository keeps that claim source-bounded rather than upgrading it into a universal invention claim.

Therefore:

> **2018 24-day study ≠ first 3D-NAND early-retention observation.**

### Toshiba adaptive-read tracking before ReMAR's public record

Toshiba's US9251892B1, with a 2014 priority date and public grant/publication on **2 February 2016**, describes controller-side tracking used to determine an appropriate NAND read voltage from observed threshold behavior.

Its value here is a bounded prior-art correction:

> **fixed read voltage ≠ all manufacturer read-control practice before 2018.**

The inspected 2016 patent is not relabeled as ReMAR and is not used to claim that elapsed retention time was already its defining input.

### Toshiba Memory elapsed-time-conditioned tracking: priority chronology is not publication chronology

Toshiba Memory's later **US20180277227A1, _Semiconductor memory device and read control method thereof_**, claims priority from Japanese Patent Application 2017-058897 filed **24 March 2017**, but the US application became public on **27 September 2018**.

Its claims make a tracking parameter depend on both the target **word line** and an **elapsed time from a previous access** to a group of cells. The tracking parameter may control the starting read voltage, number of read voltages, and spacing among them; variants also select among parameter tables based on access count.

The chronology must therefore be expressed in two layers:

```text
2014-09-11   Toshiba adaptive-tracking priority
2016-02-02   Toshiba adaptive-tracking public grant
2017-03-24   Toshiba Memory age-aware Japanese priority filing
2018-06/07   Luo et al. ReMAR public presentation / author-posted record
2018-09-27   Toshiba Memory US age-aware application becomes public
```

Therefore:

> **earlier priority filing ≠ earlier public disclosure.**

The record supports parallel manufacturer/academic design evidence, not an invention-priority or technology-transfer claim.

Dedicated record: [`../evidence/65-toshiba-2014-2018-age-aware-read-tracking-metadata-deepening.md`](../evidence/65-toshiba-2014-2018-age-aware-read-tracking-metadata-deepening.md).

### Extended-duration characterization in 2018

Yixin Luo, Saugata Ghose, Yu Cai, Erich F. Haratsch, and Onur Mutlu experimentally characterize real, then-state-of-the-art 3D NAND MLC chips in 2018. Their paper explicitly distinguishes its contribution from earlier short-duration work and follows retention behavior out to **24 days**.

In the tested population, the raw bit error rate (`RBER`) rises by about an order of magnitude within roughly **three hours** after programming and then increases much more slowly; another approximately order-of-magnitude increase takes on the order of **eleven days**. The important retention result is the *shape* of this curve, not universalization of those exact numbers.

The paper uses historical/technical vocabulary including:

- `early retention loss`;
- `retention time` / `retention age`;
- `charge trap`;
- `threshold voltage (Vth)`;
- `raw bit error rate (RBER)`;
- `read reference voltage` / `optimal read reference voltage`;
- `Retention Model Aware Reading (ReMAR)`;
- `retention interference`;
- `Retention Interference Aware Neighbor-Cell Assisted Correction (ReNAC)`;
- `layer-to-layer process variation`.

The Toshiba source vocabulary adds `tracking parameter`, `write reference time`, `reference time data`, and read/write/access-count management. `front-loaded retention hazard`, `read-interpretation state`, `controller time continuity`, `relational retention trajectory`, and `persistence horizon` remain project analytical terms.

### Direct TLC evidence in 2022–2024

Hongzhe Lin and colleagues' 2022 IEEE SNW paper directly characterizes **TLC 3D NAND** threshold-voltage distributions and optimal read voltages under `retention-after-cycling`, then proposes a mathematical model for predicting optimal-read-voltage shift (`ORVS`) rather than relying only on search-based read retry. Its abstract reports 96.6% prediction accuracy for one bounded condition: blocks at 8k P/E cycles after 335 hours at 55 °C.

Xuesong Zheng and colleagues' 2024 *Micromachines* paper supplies a more inspectable raw-device witness: a 128-Gbit, 64-layer charge-trap TLC NAND device tested with an FPGA raw-NAND platform from 25 °C to 85 °C. The study follows fresh blocks through 10k P/E cycles and includes a 24-hour data-retention path after deliberately different preceding P/E timing and temperature histories. The later retention fail-bit counts depend on those prior histories in the bounded experiment.

These sources close only the former **direct TLC measurement** debt. They do not prove that the 2018 MLC curve is quantitatively portable and do not prove commercial-controller deployment of any one adaptive-read policy.

Dedicated record: [`../evidence/65-2022-2024-tlc-retention-read-voltage-deepening.md`](../evidence/65-2022-2024-tlc-retention-read-voltage-deepening.md).

### Direct QLC evidence in 2019–2024

Kunliang Wang, Gang Du, Zhiyuan Lun, and Xiaoyan Liu's 2019 IEEE IMW record explicitly covers **3-D TLC and QLC NAND flash memories**. Its abstract states that threshold-voltage distributions after different data-retention times and P/E-cycle counts are measured, that a back-propagation neural-network model predicts those distributions with good agreement to measurement, and that the result can be used for read-voltage optimization. This is enough to establish a direct QLC retention/read-threshold measurement witness without inventing full-paper details that were not directly inspected.

M. Dean Sciacca, Trinadhachari Kosuru, and Nikolaos Papandreou's 2024 IEEE EDTM paper supplies a second direct QLC witness. IBM Research's institutional record says the study evaluates data retention using **state-of-the-art 3D charge-trap QLC NAND**, characterizing RBER and optimal-read-voltage offsets under different P/E counts, dwell times, and cycling temperatures.

These records close the former minimal **direct QLC measurement** debt only. They do not show that Luo et al.'s 2018 MLC early-retention curve, ReNAC effect, or the TLC results are quantitatively portable into QLC; nor do they establish a named shipped controller policy.

Dedicated record: [`../evidence/65-2019-2024-qlc-retention-read-threshold-deepening.md`](../evidence/65-2019-2024-qlc-retention-read-threshold-deepening.md).

## Retained state and constitutive control state

The bounded regime contains several separable relations:

1. **cell charge / threshold-voltage state** — charge retained in a 3D charge-trap transistor and expressed through its threshold voltage;
2. **logical MLC/TLC/QLC value** — the bit value inferred from which voltage interval the cell is classified into;
3. **retention age** — elapsed time since the current data embodiment was programmed or since another controller-defined reference event;
4. **P/E-cycle history** — wear state that changes error behavior/model parameters;
5. **read-reference policy** — voltage boundaries or tracking-search parameters used to interpret the current threshold distribution;
6. **ECC margin / error evidence** — remaining raw-error budget and current correction evidence that can trigger a more expensive read path;
7. **program-time metadata** — in ReMAR, controller-retained timing state used to estimate current retention age;
8. **reference-time management record** — in the Toshiba Memory design, nonvolatile time-reference/control metadata that can be associated with a block/page or access/write reference event;
9. **volatile controller working copy** — runtime representation loaded after power-on from nonvolatile management state in the Toshiba disclosure;
10. **time source / reboot continuity** — a meaningful clock relation needed before retained timestamps can become elapsed-time estimates;
11. **word-line / process-location context** — Toshiba's design conditions tracking on target word-line identity in addition to elapsed time;
12. **read/write/access-count state** — further context used by some disclosed tracking variants;
13. **vertically adjacent neighbor state** — in the measured retention-interference relation, a conditioning variable for the victim's threshold-voltage evolution;
14. **neighbor-aware recovery policy** — in ReNAC, an additional read-offset selection relation used after the ordinary read path fails;
15. **preceding operation/temperature history** — in the 2024 TLC experiment, controlled P/E timing and temperature conditions that change the later observed error population;
16. **model-predicted optimal-read-voltage shift** — in the 2022 TLC work, an interpretation/control result rather than payload or physical renewal;
17. **QLC retention/cycling condition** — in the 2019/2024 QLC records, retention time, P/E count, dwell, and cycling temperature condition measured threshold/error distributions and optimal-read-voltage offsets without themselves constituting user payload.

The timestamps, counters, word-line identity, neighbor value, prior-history conditions, and read-voltage models are not user payload. They are different kinds of control/context state or experimental conditioning that can change how an existing physical embodiment is interpreted.

## Engineering reconstruction

### Nonvolatile does not mean temporally stationary

The cell does not require continuous operating power merely to keep its programmed charge distinction. Yet the 2018 measurements show that the physical distribution changes rapidly soon after programming.

Therefore:

> **nonvolatile retention ≠ time-invariant read margin.**

And:

> **equal elapsed-time increments ≠ equal marginal retention loss.**

A one-hour interval immediately after program can matter differently from an equal interval much later. This is not a redefinition of Flash as volatile; it separates **power-independent survival** from **time evolution of the error/read margin** of that surviving state.

### Retention age is not one linear maintenance clock

Case 36 shows that NAND retention can motivate proactive controller work. Early retention loss adds a different temporal shape: the risk/margin change is concentrated near the beginning of the embodiment's life rather than progressing at one constant rate.

Thus:

> **retention age ≠ one linear maintenance clock.**

A policy assuming one fixed periodic interval can be a poor match to a mechanism whose error growth is steep immediately after program and flatter later.

Luo et al. explicitly evaluate the earlier planar-oriented FCR policy and report that, under their 3D NAND model/measurements, its lifetime benefit is much smaller than the large planar result cited from earlier work. This is evidence of transfer mismatch, not proof that every physical rewriting policy is wrong for 3D NAND.

### The same surviving cell state can require a different later read criterion

As charge leaks and threshold-voltage distributions shift, the read-reference voltage that minimizes raw errors also changes. The 2018 study observes that the optimal reference changes quickly when data is young and much more slowly after the early-retention period.

Therefore:

> **surviving cell charge ≠ fixed read-reference interpretation.**

And:

> **retained logical identity can depend on an age-sensitive interpretation rule.**

The bits need not be rewritten merely for a reader to change how the existing physical state is classified.

### ReMAR makes retained age metadata part of reading

ReMAR proposes to model retention loss and choose read-reference voltages using estimated data age. The controller keeps block program time together with P/E-cycle state, computes retention age on reads, and applies the model to select a better reference voltage.

This produces a particularly clear retention relation:

> **program-time metadata can become read-interpretation state.**

The timestamp does not carry user payload and does not preserve every program/read event. It is a compact control relation that helps decide how the payload should later be recovered.

Therefore:

> **retained program timestamp ≠ retained payload ≠ complete access history.**

The 2018 evaluation is research-system/model evidence, not evidence of a shipped commercial controller.

### Manufacturer design evidence adds two persistence horizons for interpretation metadata

Toshiba Memory's detailed embodiment describes reference-time and other management information retained in nonvolatile memory and loaded into controller memory after power-on.

That exposes an implementation-level distinction not available from ReMAR's research description alone:

```text
nonvolatile reference-time/control record
    !=
volatile runtime working copy
```

Therefore:

> **persistent read-interpretation metadata ≠ continuously resident read-interpretation state.**

A restart can destroy the active working copy without necessarily destroying the retained relation from which the working copy can be reconstructed.

The reverse caution is equally important:

> **boot-time reconstruction path ≠ proof of crash-atomic metadata update.**

The patent does not prove that every timestamp update is atomically coordinated with FTL remapping, that torn records are impossible, or that the latest reference time survives every sudden power cut.

### Age-aware interpretation can be multi-dimensional

The Toshiba Memory design combines elapsed time with word-line identity and, in variants, access/read/write count state. Therefore:

> **retention age ≠ complete controller interpretation context.**

This complements Case 65's existing neighbor-conditioned result: future legibility can depend on temporal, spatial/process, use-history, and relational context without those variables becoming one physical failure mechanism.

The 2024 TLC experiment strengthens the same boundary from a different evidence class. Its later retention result depends on deliberately controlled preceding P/E timing and temperature history. The 2024 QLC record independently makes P/E count, dwell time, and cycling temperature part of its retention/RBER/read-offset characterization. These results do **not** prove that a shipping controller stores a literal history log, but they do show that equal elapsed retention time need not imply equal physical/read margin.

### Direct QLC evidence closes a measurement-layer gap, not a portability gap

The 2019 and 2024 QLC records add direct generation-specific evidence for the same broad read-interpretation problem already observed in MLC/TLC:

```text
retention / cycling condition
    -> measured QLC threshold or error state
    -> changed optimal read boundary / offset
```

Therefore:

> **QLC retention-conditioned read behavior is directly measured ≠ MLC/TLC numerical results are portable to QLC.**

This distinction is the point of the deepening. A generation-specific witness removes the need for analogy at the minimal measurement layer while preserving all quantitative and deployment stop conditions.

### Trigger evidence is not tracking context or recovery verdict

In Toshiba's disclosed flows, ECC failure or a high correctable-error count can cause the tracking path to be entered. Retained reference-time, word-line, and count context then bound the tracking search.

Thus:

```text
error / ECC trigger evidence
    !=
tracking context
    !=
tracking result
    !=
logical recovery verdict
```

### Clock continuity can become retention infrastructure

A timestamp helps only if its later interpretation remains meaningful. Luo et al. discuss using a real-time clock and, where necessary, synchronizing time with the host after boot. Toshiba's power-on management-state load supplies a separate manufacturer design witness for the fact that temporal control information can cross a restart boundary in a stored representation.

Therefore:

> **controller time continuity can become retention infrastructure.**

Yet:

> **controller time continuity ≠ medium charge continuity.**

Losing a clock relation and losing charge state are different failures. The former can disable an age-aware optimization while the payload remains physically present and perhaps recoverable by other read/ECC paths.

### Read-reference adaptation is not physical refresh

ReMAR changes the voltage boundary used to interpret an aged distribution. Toshiba's tracking design changes the read-voltage search/selection process. The 2022 TLC work adds another read-side form: predicting an optimal-read-voltage shift under retention-after-cycling. The 2019 and 2024 QLC records add threshold-distribution prediction/measurement and optimal-read-voltage-offset characterization in QLC. None of these operations, by itself, puts leaked charge back into the cell.

Therefore:

> **read-reference adaptation / tracking / prediction ≠ physical refresh or restoration.**

This is the central boundary against Case 36. A later system could compose read adaptation with a rewrite/remap path, but functional composability does not make them one operation.

### Logical recoverability can outlast pristine physical margin

As in Cases 36, 52, and 59, raw error growth can occur while ECC and read-retry/reference adaptation still recover the intended page.

Therefore:

> **correct logical read ≠ unchanged physical retention margin.**

And:

> **RBER/FBC growth ≠ immediate logical forgetting.**

Forgetting occurs only when available interpretation/correction/recovery resources can no longer recover an admissible logical value under the relevant service contract.

## Retention interference deepening: age plus neighbor state

The 2018 Luo et al. paper also measures **retention interference**: the speed of victim-cell retention loss depends on the threshold-voltage state of a vertically adjacent neighbor sharing the charge-trap structure along the bitline.

The authors describe charge movement between higher- and lower-threshold-voltage neighbors through the shared charge-trap layer. They deliberately control the experiment against **program interference** by using neighbors programmed before victims and excluding an erased-state victim regime with separate interference sensitivity. Grouping cells by victim and neighbor state over 24 days, they observe smaller victim threshold shifts when the neighboring cell is in a higher-voltage state.

Thus:

```text
retention age
    !=
complete measured retention trajectory

retention age + neighbor stored state
    ->
more specific estimate of victim threshold-voltage evolution
```

Therefore:

> **same retention age ≠ necessarily the same physical retention trajectory.**

And:

> **victim logical identity ≠ physically self-contained victim state.**

The neighbor does not become part of the victim payload. It becomes physical context that can help explain and recover the victim.

### ReNAC adapts a recovery form without merging failure mechanisms

Luo et al. adapt the earlier Neighbor-Cell Assisted Correction (`NAC`) recovery pattern to retention interference and name the result **ReNAC**:

```text
retention time + vertically adjacent neighbor state
    -> online retention-interference model
    -> neighbor-dependent read offset
    -> reread after ordinary read/ECC failure
```

This is a read-path recovery proposal, not a physical rewrite.

Therefore:

> **neighbor-assisted logical recovery ≠ physical restoration of the victim cell.**

And:

> **reuse of NAC's recovery form ≠ program interference and retention interference are the same physics.**

### The negative result is part of the evidence

The paper states that ReNAC does **not** show meaningful flash-lifetime improvement for the current generation of 3D NAND it tested. The measured retention-interference shift is smaller than voltage movement from process variation and early retention loss in that population.

The authors expect retention interference to matter more as geometries shrink and in TLC/QLC devices with narrower margins, but leave quantitative future-device evaluation open.

Therefore:

> **ReNAC proposed ≠ demonstrated current-generation lifetime benefit.**

And:

> **projected future TLC/QLC importance ≠ measured TLC/QLC result in the 2018 paper.**

Dedicated record: [`../evidence/65-luo-2018-retention-interference-renac-deepening.md`](../evidence/65-luo-2018-retention-interference-renac-deepening.md).

## Functional comparison: Toshiba age-aware tracking and ReMAR

The shared high-level relation is:

```text
retained time reference + current time
    -> elapsed-time estimate
    -> better-bounded read-reference selection/search
```

But the evidence types and mechanisms differ.

- **ReMAR** is a scholarly proposal motivated by measured 3D-NAND early-retention behavior and explicitly models retention-age-dependent optimal read reference.
- **Toshiba Memory's design** is a manufacturer patent disclosure in which elapsed time, word-line identity, and other state can select a tracking search pattern.
- **2022 TLC ORVS work** is a later scholarly measurement/model record for retention-after-cycling in TLC; it does not establish either ReMAR or Toshiba genealogy.
- **2019/2024 QLC work** is generation-specific scholarly measurement/model evidence for retention-conditioned threshold/error/read-voltage behavior; it likewise does not establish ReMAR, Toshiba, or commercial-controller genealogy.

Therefore:

> **same broad function ≠ same algorithm.**

> **same broad function ≠ historical genealogy.**

> **patent embodiment or research model ≠ shipped controller.**

The Toshiba age-aware patent's earlier 2017 priority filing also cannot be used as if it were an earlier public disclosure than ReMAR.

## Cross-case boundaries

### Versus Case 36 — Flash Correct-and-Refresh

Case 36:

```text
elapsed retention age / wear
    -> accumulating raw errors
    -> ECC correction
    -> in-place reprogram OR remap/rewrite
    -> renewed physical margin
```

Case 65 ReMAR:

```text
program time + P/E state
    -> strongly front-loaded 3D retention aging
    -> model-estimated current distribution
    -> age-aware read-reference selection
    -> lower-error interpretation of existing embodiment
```

Case 65 Toshiba design witness:

```text
reference-time record + current time
    + word-line / count context
    + error evidence
    -> tracking-parameter selection
    -> bounded read-voltage search
```

Case 65 ReNAC:

```text
retention time + neighbor state
    -> neighbor-conditioned retention estimate
    -> failure-path read-offset selection
    -> reread of existing embodiment
```

Case 65 later TLC/QLC evidence:

```text
retention + cycling / prior-history condition
    -> changed threshold/error regime
    -> measured or predicted optimal read-voltage condition
```

Safe functional analogy: all can preserve or characterize logical availability against retention-related error growth.

Stop condition: **physical renewal is not read-boundary adaptation**, and these sources do not establish one common implementation lineage.

### Versus Case 52 — NAND read disturb

Case 52 is **access-induced**: repeated reads apply pass-through stress to other cells, so read count can become a maintenance clock.

Case 65 early retention is **post-program time dependent**. Toshiba's disclosed controller may also use read/access count as an input, which is useful precisely because it shows that one controller can carry multiple distinct degradation clocks. The 2024 TLC experiment studies read-disturb and retention in the same research program but keeps them as separate processes. The 2024 QLC record varies cycling conditions for retention characterization; it is not evidence that retention and read disturb are one mechanism.

Therefore:

> **elapsed-time context ≠ read-count context.**

And:

> **early retention loss / retention interference ≠ read disturb.**

### Versus Case 59 — NAND program interference / NAC

Case 59 is **write-event-induced neighbor coupling**. A neighboring program event shifts a previously programmed victim, and program order matters.

Case 65 retention interference is **retention-time evolution conditioned by neighbor stored state** in a 3D charge-trap structure. ReNAC reuses a neighbor-aware recovery form but the physical mechanism remains different. The 2024 TLC experiment's prior operation timing and the 2024 QLC study's cycling-condition variables are history variables and do not collapse into Case 59's program-interference mechanism.

Therefore:

> **retention interference ≠ program interference.**

### Versus Case 04 — Flash virtual mapping

Case 04's mapping/currentness metadata answers:

> which physical embodiment currently counts?

Case 65's time/reference/tracking metadata answers:

> how should the current embodiment be interpreted now?

Both can be constitutive controller state, but:

> **mapping/currentness state ≠ read-interpretation state.**

The Toshiba boot-load evidence also does not prove that reference-time metadata and FTL mapping are updated atomically together.

### Versus DRAM refresh

A narrow analogy is allowed: both DRAM and NAND cases can make later readability depend on time-sensitive policy.

The analogy stops there. DRAM refresh is constitutive periodic restoration of volatile dynamic-cell state; early-retention-aware 3D NAND reading concerns a nonvolatile medium whose aged physical distribution may be interpreted using changed read references and retained context.

## Failure and forgetting boundaries

Distinct failure modes include:

- fast post-program charge loss shifts threshold distributions;
- P/E wear changes applicable error behavior;
- prior operation interval / temperature history can condition a later TLC error population;
- QLC P/E count, dwell, and cycling temperature can condition measured retention/RBER/read-voltage behavior in the bounded 2024 study;
- a fixed read-reference voltage becomes increasingly mismatched to the aged distribution;
- ECC margin can be consumed even while reads still succeed;
- program/reference-time metadata can be missing, stale, or associated with the wrong current physical embodiment;
- a durable reference-time record can survive while its volatile working copy must be rebuilt after restart;
- a working copy can exist while the underlying persistent record is stale or inconsistent;
- clock continuity/time synchronization can be unavailable after restart;
- word-line/process-location or count-conditioned policy can be wrong for a different generation;
- an analytical model can be inaccurate for a different chip generation or vendor;
- a victim's threshold evolution can differ because a vertically adjacent neighbor occupies a different state;
- neighbor-state metadata/reads can be unavailable or a neighbor-conditioned model can be wrong;
- age-aware or neighbor-aware reading can reduce errors without physically renewing the cell, leaving later physical aging active;
- a controller can eventually exhaust ECC/read-retry/tracking/recovery options even though some physical charge remains.

Forgetting here is neither “power was removed” nor “a certain wall-clock duration elapsed.” It is loss of a sufficiently distinguishable and recoverable logical state under the available read-reference, ECC, metadata, context, and policy resources.

## Historical record / engineering reconstruction / interpretation ledger

| Claim | Layer | Evidence boundary |
| --- | --- | --- |
| fast initial charge loss is documented in charge-trapping NAND by 2010 | `H/P` | IEDM 2010 bibliographic/abstract record; prior art only |
| tube-type 3D NAND `early retention` within seconds is documented by 2016 | `H/P` | VLSI Technology 2016 paper metadata/abstract |
| Toshiba publicly disclosed adaptive NAND read-voltage tracking by 2016 | `H/P` | US9251892B1 manufacturer-primary design record |
| Toshiba Memory's later design selects tracking parameters using word-line identity + elapsed time | `H/P` | US20180277227A1 claims; patent design, not shipped product |
| Toshiba management/reference-time state can have nonvolatile-at-rest and volatile-runtime representations | `H/P` | detailed manufacturer design disclosure; no crash-atomicity claim |
| Luo et al. extend observation of real 3D NAND early retention to 24 days and report strongly front-loaded RBER growth | `H/P` | directly inspected 2018 paper |
| optimal read-reference voltage changes with retention age in the bounded 3D NAND population | `H/P` | 2018 characterization/modeling |
| ReMAR tracks data age and adapts the read reference using program-time/P-E information | `H/P` | 2018 ReMAR proposal |
| Luo et al. measure victim retention shift correlated with vertically adjacent neighbor state | `H/P` | 2018 retention-interference experiment |
| ReNAC models retention interference using retention time and neighbor state | `H/P` | 2018 ReNAC proposal |
| ReNAC shows meaningful lifetime improvement on the tested current generation | `X` | 2018 explicitly reports that it does not |
| 2022 peer-reviewed work directly characterizes retention-after-cycling threshold distributions / optimal read voltages in TLC 3D NAND | `H/P` | IEEE SNW publisher record/abstract |
| 2022 work reports 96.6% ORVS prediction accuracy for 8k-P/E blocks after 335 h at 55 °C | `H/P` | bounded abstract-level result; not a retention success probability |
| 2024 raw-device work tests 128-Gbit 64-layer charge-trap TLC through a 24 h retention path after controlled P/E timing/temperature histories | `H/P` | directly inspectable methods/results |
| later TLC retention FBC can differ with prior operation/temperature history in the bounded 2024 experiment | `H/P` | source-bounded experiment; not universal product law |
| 2019 IMW work directly includes 3-D QLC measured retention-conditioned Vth distributions and read-voltage optimization | `H/P` | institutional/publisher abstract; no invented full-paper details |
| 2024 EDTM work directly evaluates retention in 3D charge-trap QLC and characterizes RBER/read-voltage offsets under cycling conditions | `H/P` | IBM Research institutional abstract |
| a retained timestamp/reference-time record can become constitutive read-interpretation state | `E` | reconstruction from ReMAR + Toshiba mechanism |
| persistent control record and runtime working copy can have different persistence horizons | `E` | reconstruction from Toshiba power-on load path |
| boot reconstruction proves atomic metadata updates | `X` | not established by patent disclosure |
| time continuity can be retention infrastructure without being payload | `E` | reconstruction from RTC/reference-time requirements |
| neighbor state can become recovery side information without becoming victim payload | `E` | reconstruction from retention-interference/ReNAC mechanism |
| same elapsed retention time fully determines TLC/QLC recovery margin | `X` | controlled-history/cycling-condition evidence blocks this shortcut |
| age-aware, neighbor-aware, or model-predicted reference selection physically restores lost charge | `X` | read-boundary adaptation is not charge rewrite |
| Toshiba age-aware tracking, 2022 TLC ORVS prediction, or 2019 QLC BpNN modeling is ReMAR | `X/A` | functional similarity only; algorithm/genealogy identity not established |
| 2017 Toshiba priority filing is proof of public disclosure before ReMAR | `X` | filing chronology != public-publication chronology |
| ReMAR, ReNAC, Toshiba's exact patent embodiment, or the later TLC/QLC models are proven deployed in a named commercial controller | `X` | deployment remains open |
| direct QLC measurement makes MLC/TLC quantitative curves portable to QLC | `X` | generation-specific measurement closes only the minimal evidence gap |
| every later 3D NAND/TLC/QLC generation has the same early-retention curve/interference magnitude | `X` | outside bounded population |
| early retention / retention interference is identical to read disturb or program interference | `X/A` | only higher-level comparison is allowed |
| nonvolatile media can require time-sensitive and relational interpretation policy | `I` | bounded philosophical pressure; not historical actor vocabulary |

## Philosophical interpretation — bounded

This case supplies two narrow conceptual corrections:

> **A retained state can remain materially present while the rule for making it reliably available to a future operation changes with the age of that state.**

And:

> **A retained state can remain materially local while its future legibility is partly relational to other retained state and controller context.**

The Toshiba deepening adds a third bounded pressure:

> **The metadata that makes persistent matter legible can itself require persistence across one interval and reconstruction into a different working representation across another.**

The TLC/QLC deepening adds a fourth:

> **The same elapsed retention age does not exhaust technical history: prior wear, operation timing, dwell, and temperature can condition the later recovery margin.**

These are useful to a philosophy of technical retention because they separate `remaining` from `remaining equally legible under one fixed interpretation`, and persistent control relations from their runtime embodiments. They do not imply that the engineers were making philosophical claims about memory, nor do they make every controller timestamp, model, or neighbor read a form of cultural or tertiary retention.

The engineering result comes first: a nonvolatile charge-trap state can age nonlinearly, and a controller can use retained temporal, spatial/process, count, neighbor, and model/context evidence to adapt how it reads the state.

## Cross-case result

Case 65 now adds this chain:

```text
3D charge-trap programmed state
    !=
retention/reference age
    !=
front-loaded threshold/RBER evolution
    !=
P/E / operation / dwell / temperature history
    !=
nonvolatile reference-time/control record
    !=
volatile runtime working copy
    !=
word-line / access-count context
    !=
vertically adjacent neighbor state
    !=
MLC/TLC/QLC threshold/error distribution
    !=
optimal / recovery read-reference or tracking search
    !=
model-predicted read-voltage shift
    !=
ECC-correctable logical payload
    !=
age-aware / neighbor-aware controller interpretation
    !=
physical refresh or rewrite
```

The strongest result remains that **retention policy can move from “renew the physical state on a schedule” toward “retain or infer enough temporal and contextual evidence to reinterpret the same aged physical state more accurately.”** The manufacturer-design evidence shows one concrete way such context can itself cross a power-cycle boundary through persistent metadata and runtime reconstruction; the TLC/QLC evidence shows that later measured read/error conditions can also depend on wear and preceding operating history. This remains a functional/engineering comparison, not a claim of universal SSD practice or one historical lineage.

## Related repositories

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `early retention`, `TLC 3D NAND`, `QLC NAND retention`, and the exact later paper titles found no dedicated reusable case. A broader history of BiCS/V-NAND/charge-trap process architecture, TLC/QLC product generations, Toshiba/Kioxia controller genealogy, QLC vendor/process genealogy, and patent-family evolution belongs there. This repository keeps only the retention-specific relation among front-loaded aging, read tracking, persistent reference-time state, runtime reconstruction, history-conditioned TLC/QLC evidence, neighbor-conditioned drift, ECC margin, and physical renewal.

Case 59 remains the local home for the earlier program-interference/NAC genealogy; this case links that work instead of duplicating it.

[`tmzncty/problem-history`](https://github.com/tmzncty/problem-history) supplies the anti-anachronism discipline. `fast initial charge loss`, `early retention`, `ReMAR`, `retention interference`, `ReNAC`, `tracking parameter`, `reference time`, `retention-after-cycling`, `optimal read voltage shift`, `retention threshold voltage distribution`, and `optimal read voltage offset` are source vocabulary where cited; `front-loaded retention hazard`, `read-interpretation state`, `relational retention trajectory`, and `persistence horizon` are modern analytical terms.

## Remaining work

The early-retention/ReMAR case, retention-interference/ReNAC slice, manufacturer patent/design witness, and direct TLC/QLC measurement slices are grounded, but stronger evidence remains open:

- independent replication of retention interference in later **named** 3D NAND generations/vendors;
- full-text and quantitative QLC inspection beyond the current abstract/institutional-record layer, including exact device/test conditions and longer retention horizons;
- directly comparable MLC/TLC/QLC experiments using the same platform/protocol rather than carrying curves across generations;
- direct later-generation TLC/QLC measurements specifically testing whether the 2018 front-loaded early-retention curve shape and neighbor-conditioned effect recur quantitatively;
- **named shipped controller/product** evidence for ReMAR-like age-aware tracking — the patent/design level is now partially closed, deployment is not;
- named shipped controller/product evidence for ReNAC-like neighbor-state recovery;
- firmware/command traces showing when a real controller reads neighbor state after ECC failure;
- interaction with modern LDPC soft decoding, multi-step read retry, and read reclaim;
- fault-injection experiments separating age/neighbor-aware benefit from generic read-retry heuristics;
- sudden-power-loss tests of reference-time/tracking-metadata update consistency;
- evidence for how reference-time state follows or is reset by FTL relocation / garbage collection;
- later architecture evidence showing whether shared-charge-trap leakage geometry changes materially;
- broader BiCS/V-NAND/process and Toshiba/Kioxia/QLC controller genealogy in `computing-archaeology`, linked back here rather than duplicated.

## Sources

1. Yixin Luo, Saugata Ghose, Yu Cai, Erich F. Haratsch, Onur Mutlu, **“Improving 3D NAND Flash Memory Lifetime by Tolerating Early Retention Loss and Process Variation,”** *Proceedings of the ACM on Measurement and Analysis of Computing Systems* 2(3), Article 37, 2018, DOI `10.1145/3224432`; author-accessible full text: <https://arxiv.org/abs/1807.05140>.
2. Bongsik Choi et al., **“Comprehensive evaluation of early retention (fast charge loss within a few seconds) characteristics in tube-type 3-D NAND Flash Memory,”** *2016 IEEE Symposium on VLSI Technology*, Honolulu, 14–16 June 2016, DOI `10.1109/VLSIT.2016.7573385`.
3. C.-P. Chen, H.-T. Lue, C.-C. Hsieh, K.-P. Chang, K.-Y. Hsieh, C.-Y. Lu, **“Study of fast initial charge loss and its impact on the programmed states Vt distribution of charge-trapping NAND flash,”** *2010 IEEE International Electron Devices Meeting (IEDM)*, San Francisco, 6–8 December 2010, pp. 5.6.1–5.6.4 / 118–121, DOI `10.1109/IEDM.2010.5703304`.
4. Yu Cai, Gulay Yalcin, Onur Mutlu, Erich F. Haratsch, Osman Unsal, Adrian Cristal, Ken Mai, **“Neighbor-Cell Assisted Error Correction for MLC NAND Flash Memories,”** *ACM SIGMETRICS*, June 2014, pp. 491–504; institutional abstract: <https://istc-cc.cmu.edu/publications/papers/2014/neighbor-assisted-error-correction-in-flash_sigmetrics14_abs.shtml>.
5. **“Reliability of NAND Flash Memories: Planar Cells and Emerging Issues in 3D Devices,”** *Computers* 6(2):16, 2017, DOI `10.3390/computers6020016`, used as scholarly chronology/cross-check rather than as a substitute for primary evidence where mechanism claims are decisive.
6. Toshiba Corp, Shohei Asami, Toshikatsu Hida, Tokumasa Hara, Riki Suzuki, **_Memory system and method of controlling nonvolatile memory_**, US9251892B1, priority 11 September 2014, published/granted 2 February 2016. <https://patents.google.com/patent/US9251892B1/en>.
7. Toshiba Memory Corporation, **_Semiconductor memory device and read control method thereof_**, US20180277227A1, claiming priority to Japanese Patent Application 2017-058897 filed 24 March 2017, US publication 27 September 2018; later US10586601B2 granted 10 March 2020. <https://patents.justia.com/patent/20180277227>.
8. Hongzhe Lin, Yifan Guo, Yifang Xi, Yachen Kong, Xuepeng Zhan, Jiezhi Chen, **“Optimal Read Voltages of Retention-after-Cycling in Triple-level-cell (TLC) 3D NAND Flash Memory and its High-precision Modeling Method,”** 2022 IEEE Silicon Nanoelectronics Workshop (SNW), 11–12 June 2022, DOI `10.1109/SNW56633.2022.9889070`; publisher record: <https://ieeexplore.ieee.org/document/9889070/>.
9. Xuesong Zheng, Yifan Wu, Haitao Dong, Yizhi Liu, Pengpeng Sang, Liyi Xiao, Xuepeng Zhan, **“Impact of Program–Erase Operation Intervals at Different Temperatures on 3D Charge-Trapping Triple-Level-Cell NAND Flash Memory Reliability,”** *Micromachines* 15(9):1060, 23 August 2024, DOI `10.3390/mi15091060`; <https://www.mdpi.com/2072-666X/15/9/1060>.
10. Kunliang Wang, Gang Du, Zhiyuan Lun, Xiaoyan Liu, **“The Method of Predicting Retention Threshold Voltage Distribution for NAND Flash Memory Based on Back-Propagation Neural Network,”** *2019 IEEE 11th International Memory Workshop (IMW)*, DOI `10.1109/IMW.2019.8739277`; Peking University institutional record: <https://ir.pku.edu.cn/handle/20.500.11897/544481>.
11. M. Dean Sciacca, Trinadhachari Kosuru, Nikolaos Papandreou, **“Cycling Condition Impacts on 3D QLC NAND Reliability,”** *2024 8th IEEE Electron Devices Technology & Manufacturing Conference (EDTM)*, 3 March 2024, DOI `10.1109/EDTM58488.2024.10511536`; IBM Research record: <https://research.ibm.com/publications/cycling-condition-impacts-on-3d-qlc-nand-reliability>.
