# DRAM Variable Retention Time: Profile Staleness and Unstable Preservation Deadlines

## Scope

- **Bounded system:** DRAM retention-time profiling as represented by the 2012 RAIDR proposal, stressed against variable-retention-time (VRT) and data-pattern-dependence (DPD) evidence from period device research, especially IBM's 1992 VRT study and Liu et al.'s 2013 characterization of 248 commodity DDR3 chips.
- **Bounded mechanism:** measure a cell/row retention time, retain a classification or `retention time bin`, use that retained control state to choose a future refresh interval, and confront the fact that the physical retention behavior being represented may change with time or stored-data context.
- **Research question:** what happens to technical retention when the system retains not only payload, but also a *model of how long the payload can safely be left unrefreshed*, and that model can itself become stale?

This is **not** a general history of DRAM refresh reduction, self-refresh, weak-cell testing, RowHammer, ECC, JEDEC refresh standards, or semiconductor defect physics. It isolates one retention relation:

> **A retention-aware controller can preserve a profile that says how frequently a row should be refreshed, yet preservation of the profile does not guarantee preservation of the truth it represents. Variable retention time and data-pattern dependence can make a previously measured deadline unsafe. The metadata that reduces maintenance work can therefore become another object that itself requires qualification, guardbanding, remeasurement, or error tolerance.**

`profile staleness`, `maintenance-deadline metadata`, `preservation policy state`, `context-qualified retention`, and `profile revalidation` below are **project engineering terms**, not historical DRAM vocabulary.

---

## Historical vocabulary

The bounded sources use:

- `retention time` / `refresh interval`;
- `retention time profiling`;
- `retention time bins`;
- `weak cells` / `leaky cells`;
- `variable retention time` (`VRT`);
- the earlier `variable hold time` (`VHT`) vocabulary in the cited 1987 work;
- `data pattern dependence` (`DPD`);
- `high retention time state` / `low retention time state`;
- `guard band`;
- `trap-assisted gate-induced drain leakage` (`TA-GIDL`) in the physical explanation summarized by the 2013 study.

Do not silently rename these as `RowHammer`, cache metadata, wear-leveling state, or generic `bit rot`. Those may be useful comparisons at the level of relations, not period vocabulary or genealogy.

---

## Historical record

### H/P — retention-aware refresh can make a stored profile part of the controller's correctness path

Liu et al.'s 2012 RAIDR proposal groups DRAM rows into `retention time bins`. A profiling step measures row retention time; the memory controller records rows in bins; later refresh decisions consult those bins and use a bin-specific or default refresh interval. The paper's correctness statement is explicitly conditional on each row being refreshed at an interval no longer than its **measured retention time**.

The profile is therefore not descriptive paperwork outside the machine. It participates directly in deciding how long payload charge may be left without restoration.

**Primary research anchor:** Liu et al., ISCA 2012, §3.1.

### H/P — RAIDR explicitly proposed retaining the profile across boots

RAIDR's straightforward profiling method writes static patterns, disables refresh, and observes when a first bit changes. After profiling, the measured results may be saved by the operating system and restored into the memory controller on later boots without repeating the profile. For permanently attached 3D-stacked/eDRAM configurations, the paper even discusses storing the one-time profile permanently in controller ROM/fuses.

This is a particularly clean retention-within-retention relation:

```text
payload state
    depends on future refresh timing
        which depends on retained profile state
```

The 2012 paper notes circuit-level crosstalk as a complication and leaves deeper analysis of that issue to future work. Its reuse-across-boot proposal is therefore historical evidence for the *architecture and assumption being stressed*, not evidence that every retention profile is in fact immutable.

**Primary research anchors:** Liu et al., ISCA 2012, §3.2 and §3.7.

### H/P — VRT was established before retention-aware controller proposals

IBM Research records Restle, Park, and Lloyd's 1992 IEDM paper `DRAM variable retention time`. Its abstract defines VRT as time-varying cell leakage that changes how long a bit retains information, reports VRT cells in all examined 4 Mbit and 16 Mbit chips across multiple manufacturers and both trench- and stacked-capacitor technologies, and distinguishes two-state and multi-state VRT cells.

The 2013 characterization's related-work section places the genealogy still earlier: it says VRT was first observed by Yaney et al. in the 1987 `variable hold time` work and then confirmed/investigated in more detail by Restle et al. This case uses that chronology conservatively. It does **not** claim that RAIDR, IBM 1992, or the 2013 paper invented VRT.

**Primary/institutional anchors:** Restle et al., IEDM 1992; Liu et al., ISCA 2013, §7.3.

### H/P — manufacturer evidence shows a cell can pass an early retention condition and later require faster refresh

Micron's 2002-filed patent `Method of reducing variable retention characteristics in DRAM cells` describes retention time changing over time even at constant temperature. One illustrative cell remains near 120 ms for an initial period and then falls to about 48 ms; the patent uses this to show how a cell could pass a 64 ms-oriented test and later lose data in a system whose chosen refresh interval was longer than the changed requirement.

The exact numbers are an illustrative embodiment, not universal DRAM thresholds. The important historical point is the engineering problem already being stated by a DRAM manufacturer: **qualification at one moment need not establish the future minimum retention time of the cell.**

**Primary patent anchor:** US6898138B2 / US20040042306A1, filed 2002-08-29.

### H/P — the 2013 study directly measured profile instability across modern commodity DDR3 parts

Liu et al. tested 248 commodity DDR3 chips from five major vendors on a temperature-controlled FPGA platform. They identify two phenomena that complicate retention-time profiling:

1. **data pattern dependence (DPD):** the measured retention time of a cell is affected by values stored in other cells;
2. **variable retention time (VRT):** some cells move unpredictably among multiple retention-time states over time.

The paper explicitly says prior retention-aware mechanisms depend on an accurate profile and that these two effects challenge the assumption that a profile can simply be measured once and treated as a conservative description of future behavior.

**Primary research anchor:** Liu et al., ISCA 2013, Abstract and §§1–2.3.

### H/P — a 2× safety margin was not a universal cure in the measured VRT population

The 2013 paper reports that VRT can make retention time fall substantially below a previously measured value and states that even a 2× safety margin may not suffice. In the detailed VRT analysis, some tested cells exhibited minimum versus maximum measured retention times differing by more than a factor of four; the authors therefore note that handling VRT only with a fixed guard band could require a guard band greater than four in those observations.

This evidence blocks a simple equation:

```text
profile + ordinary fixed margin = permanently qualified deadline
```

It does **not** prove that every DRAM device requires a 4× margin, or that a sufficiently conservative architecture cannot handle VRT.

**Primary research anchors:** Liu et al., ISCA 2013, Introduction and §6.1.

### H/P — profiling duration can be shorter than the time needed to observe the dangerous state

The same study reports many VRT cells remaining in a high-retention state for about 15,000 seconds (roughly four hours), with some observed for nearly the entire approximately one-day experiment before leaving that state. The authors conclude that reliable observation of the lowest retention states may require continuous profiling on the order of days, and that at the architectural level a VRT cell cannot simply be identified without observing a VRT transition.

Thus an apparently exhaustive test over addresses can still be temporally incomplete: every row may have been tested, yet the relevant low-retention state may not have occurred during the test window.

**Primary research anchor:** Liu et al., ISCA 2013, §§6.2–6.3.

### H/P — profile validity is also dependent on the stored data pattern

The 2013 paper reports strong DPD. In some tested devices, profiling with only simple all-1 and all-0 patterns identified less than 15% of the weak cells exposed by a broader set of patterns. The authors attribute the observed dependency to data-dependent circuit coupling/noise and show that the relevant worst-case pattern differs across device organizations.

This adds a second way a retained profile can be insufficient:

```text
measured deadline
    is qualified by the measurement data pattern
```

A profile is therefore not necessarily a context-free scalar attached permanently to one physical cell.

**Primary research anchors:** Liu et al., ISCA 2013, Introduction and §§2.3, 5.

### H/P — manufacturing-time profiling need not survive assembly unchanged

Liu et al. further note that very high temperatures such as those used in soldering can induce VRT in cells not previously susceptible, citing earlier device literature. They therefore warn that a manufacturer profile made before module assembly may not accurately describe the final assembled module.

This is not evidence that every soldering cycle creates VRT. It is a bounded historical argument that the system boundary and lifecycle stage at which profiling occurs can matter to the validity of the retained classification.

**Primary research anchor:** Liu et al., ISCA 2013, §6.3.

---

## Retained state

### 1. Payload charge

The application-visible bit remains embodied as charge in a DRAM cell capacitor and must be restored before sensing margin is lost.

### 2. Retention-time profile / bin membership

A retention-aware mechanism may retain a row's measured class: for example, whether that row must remain in a faster-refresh bin or may use a longer default interval. This is **control metadata**, not user payload.

### 3. Refresh progress and policy state

The controller still retains or derives which rows are due for refresh and applies a schedule. Case 93 is not about a controller simply forgetting to execute refresh; it is about the possibility that the schedule is faithful to a **stale or incomplete profile**.

### 4. Measurement context

Temperature, test pattern, profiling duration, assembly state, and other conditions qualify what a measured retention time means. They need not all be stored literally in a particular historical implementation, but engineering reconstruction must not pretend the measured number is independent of them.

### 5. Hidden VRT physical state

A cell can occupy a high- or low-retention state that is not represented merely by its stable logical address or by an old profile entry. This physical state is not the user payload and, according to the 2013 architectural discussion, cannot simply be predicted before observing the state change.

---

## Physical / logical substrate

The physical substrate remains the DRAM cell capacitor/access transistor and the leakage/coupling mechanisms that determine how fast usable charge margin decays. The logical/control substrate adds:

- row identity;
- measured retention-time class;
- controller data structures such as RAIDR bins/Bloom filters;
- refresh counters/scheduling logic;
- optional OS persistence of profile information.

The crucial point is that the **represented thing and the representation have different failure modes**. The profile can remain bit-for-bit intact while the cell's actual retention behavior changes.

---

## Retention mechanism

A simplified baseline is:

```text
cell stores payload charge
    -> charge leaks
    -> refresh before safe deadline
    -> payload remains recoverable
```

Retention-aware refresh adds a learned relation:

```text
measure row/cell retention behavior
    -> store profile / retention-time bin
    -> choose longer or shorter future refresh interval
    -> reduce unnecessary refresh work
```

VRT creates a profile-invalidating path:

```text
profile says row is safe for interval T
    -> cell later transitions to lower-retention state
    -> profile bits remain unchanged
    -> controller faithfully waits T
    -> actual safe interval is now < T
    -> payload may fail before scheduled restoration
```

DPD creates a context-invalidating path:

```text
profile measured under pattern P1
    -> later payload/neighborhood has pattern P2
    -> sensing/leakage margin differs
    -> old measured deadline may not be conservative for P2
```

The retention-aware mechanism therefore turns **knowledge about retention** into retention infrastructure.

---

## Addressing and access geometry

The row address can remain perfectly stable across all of these events. The difficulty is not loss of designation but loss of validity in the relation:

```text
row identity -> safe refresh class
```

RAIDR's Bloom filters are a compressed membership structure for this relation. VRT shows that correct membership is temporally contingent; DPD shows that it can also be context contingent.

This is distinct from Case 04 Flash mapping, where a stable logical address is resolved to changing physical locations. Here the physical row can stay put while the **maintenance classification** attached to it becomes wrong.

---

## Read semantics

Ordinary DRAM activation/sensing still restores the selected row as described in Cases 03 and 92. Case 93 does not introduce a new read mechanism. Its new problem lies before the next access: whether the controller's stored model lets the row wait too long before restoration.

A successful read during profiling is therefore evidence about a row under a particular elapsed time, temperature, data pattern, and VRT state. It is not proof that the same row has one timeless intrinsic retention deadline.

---

## Write and erasure semantics

Writing payload changes cell charge and may change the data pattern that affects DPD. Updating a retention profile changes control state about how the payload will be maintained. These are distinct writes.

No deliberate erasure mechanism is central to this case. A retention failure caused by a stale profile is unintended corruption/forgetting, not an authorized delete or secure erase.

---

## Time

At least five temporal layers matter:

- ordinary refresh interval;
- measured retention time for a cell/row under a particular test;
- duration of the profiling experiment;
- residence time in high- or low-retention VRT states;
- lifecycle time between manufacturing test, module assembly, boot-time restoration of a profile, and later operation.

The key temporal result is that **measurement time and future use time are not interchangeable**. A four-hour or one-day high-retention episode can make a short profiling interval appear safe while the future low-retention state remains unobserved.

---

## Maintenance and labor

Retention work in this regime includes:

- ordinary DRAM refresh circuitry and scheduling;
- characterization of cell/row retention behavior;
- generation and storage of retention profiles;
- choosing conservative bin boundaries and guard bands;
- temperature-aware policy;
- selecting data patterns adequate to expose weak cells;
- deciding how long profiling must run;
- re-profiling or online profiling when static qualification is insufficient;
- ECC/error tolerance for previously undiscovered weak/VRT states;
- manufacturing and assembly qualification.

A mechanism designed to **reduce maintenance** can therefore create new maintenance work around the correctness of the metadata that decides which maintenance may safely be skipped.

---

## Failure / forgetting modes

Keep these distinct:

- ordinary cell leakage beyond a genuinely correct refresh deadline;
- a VRT transition lowering the actual safe interval below a retained profile value;
- profiling that ends before the lowest-retention state appears;
- a data pattern that fails to expose the worst-case weak-cell behavior;
- a profile generated before assembly becoming invalid for the final module;
- temperature policy that is wrong or insufficiently conservative;
- profile storage corruption;
- correct profile storage but stale profile semantics;
- bin-membership omission/false classification;
- ECC/error-tolerance assumptions that do not cover an unprofiled failure.

The central new distinction is:

> **profile loss and profile staleness are different faults.**

The former loses the control record. The latter retains the control record while losing the truth relation that made it safe to use.

---

## Engineering reconstruction

### E — measured retention time ≠ immutable cell property

A measured value is an observation under a particular physical VRT state and measurement context. The same addressed cell can later exhibit a lower safe interval.

### E — profile persistence ≠ profile correctness

Saving and perfectly restoring a profile across boot protects the profile's bits. It does not prove that its row-to-deadline relation still matches the physical device.

### E — static retention profile ≠ guaranteed future safe refresh schedule

A controller can execute exactly the schedule authorized by its profile and still fail if the profile ceased to be conservative.

### E — retention metadata ≠ user payload

The profile is not application data. Yet loss or staleness of this secondary state can determine whether application data remains recoverable.

### E — longer remembered deadline can be more dangerous than a shorter conservative deadline

A stale classification that incorrectly grants a long interval is not harmless metadata drift. It can cause the controller to omit restoration that the cell now requires.

### E — profiling duration ≠ proof that the lowest retention state was observed

Address coverage can be complete while temporal-state coverage remains incomplete. A VRT cell may not enter its dangerous state during the profiling window.

### E — guard band ≠ proof against state changes

A margin reduces risk only within the variation envelope it covers. The measured >4× changes and the paper's explicit 2× warning show why a fixed small guard band cannot be treated as a universal proof.

### E — test / assembly qualification ≠ final-system retention profile

A device can pass an earlier measurement regime yet later encounter a physical lifecycle transition that changes VRT behavior. Qualification has a lifecycle boundary.

### E — profiling data pattern ≠ neutral context

If neighboring stored values affect observed retention, a profile produced under one small set of patterns is evidence about that test context, not automatically a worst-case certificate.

### E — cell-local retention ≠ neighbor-value-independent retention

DPD makes a cell's safe interval relational to stored values elsewhere in its array even without the repeated-access disturbance central to RowHammer.

### E — VRT ≠ ordinary temperature scaling

Temperature is a major retention variable and can be handled with explicit scaling/policy. VRT adds state transitions over time that cannot be reduced to one deterministic temperature-to-retention curve.

### E — profile reuse across boot ≠ physical-state continuity

The reboot boundary can leave a persisted profile intact while the represented DRAM has passed through time, temperature, assembly, or VRT-state transitions.

### E — retention-aware refresh trades maintenance work for retained classification knowledge

The optimization skips some periodic refresh operations by trusting additional knowledge about which rows require them. Saving energy/time therefore depends on another maintained correctness relation.

### E — stale preservation metadata can actively cause failure

Metadata can be wrong in a direction that suppresses needed work. In that case, retaining the stale metadata is not neutral; its authority is part of the failure path.

### E — maintenance policy may itself require maintenance / revalidation

Once preservation depends on a learned profile, continued correctness may require remeasurement, online profiling, error detection, or a conservative fallback. The maintenance mechanism acquires its own maintenance obligation.

---

## Functional analogies and limits

### A — Cases 03, 09, and 10 DRAM refresh authority

Case 03 establishes ordinary deadline-driven restoration; Case 09 moves refresh-address enumeration on-chip; Case 10 internalizes refresh scheduling through a leakage-tracked mechanism. Case 93 asks a different question: **what if the controller stores a learned per-row deadline and that learned relation later becomes false?** It does not replace those earlier refresh regimes.

### A — Case 53 RowHammer

Both Case 53 and Case 93 show that `retention time` cannot always be treated as a simple fixed scalar. The causal regimes differ sharply:

- RowHammer: repeated activity in an aggressor row accelerates a victim row's loss;
- VRT: the cell itself changes among leakage/retention states over time;
- DPD: stored values elsewhere change the observed retention margin.

No historical genealogy between these failure modes is implied.

### A — stale mapping/currentness/recovery metadata in later storage systems

Mapped Flash, caches, and distributed systems also contain metadata whose bits can survive while its authority or correspondence becomes stale. The analogy is only relational: **preserving a representation is not enough if the represented relation has changed.** DRAM retention bins are neither address maps nor consensus epochs.

---

## Prior-art and genealogy boundary

Do **not** claim:

- RAIDR invented retention-aware refresh or per-row retention profiling;
- the 2013 paper discovered VRT;
- IBM's 1992 paper was necessarily the first VRT observation;
- `variable hold time` and every later `VRT` implementation form one fully established engineering lineage merely because later authors cite earlier work;
- a 2× or 4× guard band is a universal DRAM requirement;
- every DRAM chip requires days of profiling;
- every soldering operation induces VRT;
- DPD is RowHammer;
- a stale profile is the same failure as corrupt profile bits;
- persisted profile metadata constitutes complete retention history.

The broad history of VRT physics, manufacturing test, adaptive refresh, JEDEC standards, and modern in-DRAM mitigation belongs in `computing-archaeology` if developed. Case 93 retains only the evidence needed to show that **preservation metadata can outlive its validity**.

---

## Philosophical / media-theoretical interpretation — bounded

### I — a retained prescription can outlive the condition that made it true

Technical retention often appears to ask only whether a state remains. This case forces a second question: **does a retained control statement remain valid?** A profile entry can persist exactly while the cell it describes moves into another retention state. The survival of the inscription and the survival of its truth relation are therefore separable.

### I — optimization produces a second-order retention problem

The universal conservative refresh policy performs extra work in exchange for needing little knowledge about individual rows. Retention-aware refresh tries to remove that excess work by preserving more differentiated knowledge. The optimization therefore moves some of the burden from repeated restoration into measurement, classification, guardbanding, and revalidation.

These are project interpretations, not claims that the DRAM authors used this philosophical vocabulary.

---

## What would falsify or narrow this case

- if a concrete retention-aware implementation always re-profiled before any profile could become stale, the persisted-profile failure path would not apply to that implementation;
- a device technology with no measurable VRT in the relevant operating envelope would narrow the VRT part of the argument for that device;
- a profiling procedure proven to enumerate worst-case DPD patterns would narrow the DPD uncertainty for that organization;
- sufficiently conservative fixed refresh plus ECC can avoid depending on fine-grained profile correctness, but at the cost of returning to a different retention regime;
- later devices may move classification, correction, or adaptive policy on-die; they require version-specific evidence rather than projection from 2012–2013 controller proposals.

---

## Remaining work deliberately left open

- exact 1987 Yaney et al. full-paper inspection and pre-1987 metastable-leakage genealogy;
- transistor/device-physics history of VRT, traps, TA-GIDL, and process scaling;
- JEDEC and vendor refresh-profile standards or proprietary mechanisms;
- production deployment evidence for online/adaptive retention profiling;
- interaction with on-die ECC in later DDR generations;
- field failure data under long-lived profiles and real workload/data-pattern transitions;
- modern retention-aware refresh schemes that explicitly model VRT and DPD;
- controlled experiments on named hardware.

---

## Related repositories

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no existing dedicated `variable retention time` / VRT case at the time of this slice. Broader semiconductor-device and refresh-policy genealogy should be developed there and linked back rather than duplicated here.

---

## Sources

See [`../evidence/93-dram-1987-2013-vrt-profiling-grounding.md`](../evidence/93-dram-1987-2013-vrt-profiling-grounding.md).
