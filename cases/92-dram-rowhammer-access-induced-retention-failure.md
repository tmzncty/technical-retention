# DRAM RowHammer: Access-Induced Retention Failure and Targeted Refresh

## Scope

- **Bounded system:** commodity DDR3-era DRAM as experimentally characterized by Kim et al. at ISCA 2014, plus Intel's 2012-filed `row hammer` targeted-refresh patent family as an earlier industry witness.
- **Bounded mechanism:** repeated activation of an aggressor row, accelerated charge leakage in physically nearby victim rows, ordinary periodic refresh, access-count / threshold-based targeted refresh, and the 2014 PARA proposal.
- **Research question:** what changes in the meaning of DRAM retention when a cell can lose charge before the ordinary refresh deadline because *another row is being accessed too often*?

This is **not** a general history of DRAM disturbance, RowHammer exploits, TRR, DDR4/DDR5 mitigations, Half-Double, refresh-management standards, memory-controller security, or DRAM process scaling. The case isolates one retention relation: **ordinary time-based refresh can remain correctly scheduled while access activity elsewhere shortens the effective retention interval of a victim row.**

The bounded retention claim is:

> **Classic DRAM refresh treats retention as a deadline-driven restoration problem: every row must be restored before charge leakage crosses a failure threshold. RowHammer adds a second variable. Repeated activation of one row can accelerate leakage in physically nearby rows enough that they fail inside the ordinary refresh window. In that regime, preservation cannot be described by elapsed time alone; it can require maintenance conditioned on access activity and physical topology.**

`workload-conditioned retention interval`, `maintenance trigger state`, `topology-qualified preservation`, and `interference-shaped retention` below are **project engineering terms**, not historical DRAM vocabulary.

---

## Historical vocabulary

The bounded 2012–2014 sources use:

- `disturbance error`;
- `row hammer` / `row hammer event` / `row hammer condition`;
- `aggressor row`;
- `victim row` / `victim cell`;
- `refresh interval` (`RI` in Kim et al.);
- `threshold number of activations` (`Nth` in Kim et al.);
- `targeted refresh`;
- `hot rows`;
- `PARA` / `probabilistic adjacent row activation`.

Do not silently rename these as cache-coherence faults, ordinary weak-cell retention failures, magnetic half-select, NAND read disturb, or a generic security exploit.

---

## Historical record

### H/P — ordinary DDR3 retention is already a scheduled restoration relation

Kim et al. summarize the DDR3 baseline as a finite charge-retention problem. Cell charge leaks; before the charge level leaves the usable noise margin it must be restored. They describe the then-standard 64 ms refresh window and note that opening a row reads through the sense amplifiers and restores the row's cell charge. A rank receives enough refresh operations within the window to cover all rows.

This is the ordinary relation already grounded more deeply in Case 03:

```text
elapsed time
    -> charge leakage
    -> refresh before deadline
    -> logical value remains recoverable
```

Case 92 does not replace that account. It adds an access-induced failure path inside the same volatile substrate.

**Primary research anchor:** Kim et al., ISCA 2014, §2.4.

### H/P — repeated activation of one row can corrupt data in nearby rows

Kim et al. report disturbance errors in 110 of 129 tested DRAM modules from three manufacturers. Their experimental characterization identifies repeated wordline toggling as the operative access pattern: many activations to one row produce disturbance effects in nearby rows, accelerating charge leakage in some victim cells. They observed errors after as few as 139,000 activations in the tested modules.

The paper's mechanism-level claim is intentionally bounded. It argues that wordline-voltage fluctuations and inter-cell coupling accelerate nearby-cell leakage; it does **not** claim to have resolved every microscopic coupling pathway in every device.

**Primary research anchor:** Kim et al., ISCA 2014, Abstract, §1, §§3–7.

### H/P — the aggressor can be repeatedly restored while victims are being endangered

Opening a DRAM row is also a restoration operation for that row. RowHammer therefore has an asymmetric retention structure:

```text
aggressor row repeatedly ACTIVATEd
    -> aggressor charge repeatedly sensed/restored
    -> nearby victim charge leaks faster
    -> victim may fail before its next ordinary refresh
```

The access that keeps one row operational can contribute to accelerated loss in another row. `activity = maintenance` for the aggressor and `activity = disturbance` for the victim can coexist in the same interval.

**Primary research anchors:** Kim et al., §2.2–2.4, §6.3.

### H/P — victim cells are not merely the ordinary weakest-retention cells

Kim et al. explicitly compare disturbance-vulnerable victim cells with `weak cells`, defined by short ordinary retention time under a long no-access/no-refresh test. They found little overlap in the tested modules and concluded that the coupling pathway responsible for disturbance errors may be independent of the process variation responsible for ordinary weak cells.

This blocks an easy but misleading reduction:

```text
RowHammer victim = ordinary leaky/weak cell
```

The bounded evidence instead supports treating passive/time-driven retention weakness and access-induced disturbance susceptibility as related but distinct failure relations.

**Primary research anchor:** Kim et al., §7, `Victim Cells ≠ Weak Cells`.

### H/P — ordinary SECDED ECC is not a complete RowHammer safety boundary

The 2014 measurements found some 64-bit words containing multiple victim cells. The paper notes that ordinary SECDED can correct one bit and detect two, but does not provide a failsafe boundary against the measured multi-bit disturbance patterns; three or more victim errors can exceed even the detection guarantee discussed there.

Therefore `ECC exists` cannot be treated as an unconditional claim that the retained logical value remains recoverable under disturbance.

**Primary research anchor:** Kim et al., §6.3.

### H/P — shortening the global refresh interval can mitigate disturbance, at a cost

Kim et al. found that sufficiently short refresh intervals eliminated disturbance errors in their tested conditions, but estimated substantial performance and energy overhead for globally refreshing all rows that frequently. Their example for an 8.2 ms interval raised refresh-time overhead far above the baseline they cited.

This matters because it exposes two different maintenance policies:

```text
periodic/global policy:
    refresh everybody more often

activity/topology-conditioned policy:
    identify risky access activity
    refresh rows threatened by that activity
```

Both restore charge, but their trigger, scope, state requirements, and cost structure differ.

**Primary research anchor:** Kim et al., §8.1.

### H/P — Intel had a row-hammer-specific targeted-refresh design filed in 2012

Intel's patent family titled `Row hammer refresh command` has a U.S. priority and filing date of 30 June 2012; the application publication appeared on 2 January 2014. The patent describes a controller receiving an indication that a row has exceeded a threshold number of accesses within a time period, identifying the hammered row, and causing a targeted refresh of physically adjacent victim rows. It also states that logical labels do not necessarily reveal physical adjacency and allows the memory device itself to resolve the victim rows.

This is an earlier industry witness that `row hammer` and targeted victim-row refresh were already active engineering concepts by 2012. It is **not** evidence that Intel invented all DRAM disturbance, nor that the patent was the first RowHammer mitigation.

**Primary patent anchor:** Bains et al., US9236110B2 / US20140006703A1, filed 2012-06-30.

### H/P — the 2014 paper proposes both tracked and stateless activity-conditioned mitigation

Kim et al. discuss identifying frequently opened (`hot`) rows and refreshing neighbors. A direct implementation could retain per-row counters or approximate hot-row state, but the storage/search cost is substantial. Their own proposal, PARA, deliberately avoids such retained per-row history: whenever a row is closed, the controller probabilistically opens an adjacent row. PARA is therefore `stateless` in the paper's explicit terminology with respect to per-row activation counters / aggressor-victim address tables.

The retention lesson is not that RowHammer always requires access-history metadata. It is that **the maintenance policy must somehow couple preservation work to access activity**; implementations can embody that coupling through retained counters/threshold state or through a stateless probabilistic rule.

**Primary research anchor:** Kim et al., §§8.1–8.2.

### H/P — targeted maintenance depends on physical-topology knowledge

Kim et al. emphasize that selective neighbor refresh requires knowledge of physical adjacency, while logical row addresses may not directly expose it and manufacturer remapping can change the relevant neighbors. Intel's patent makes the same boundary operationally useful by allowing the DRAM device, which knows its internal mapping, to resolve victim rows from information about the hammered row.

Thus a host-visible or controller-visible row identifier is not by itself a complete description of the physical interference neighborhood.

**Primary anchors:** Kim et al., §8.2 `Adjacency Information`; Bains et al., targeted-refresh patent.

---

## Retained state

### 1. Victim-cell payload charge

The user-visible logical bit remains embodied in volatile charge. RowHammer changes the rate at which some victim cells lose the charge margin needed for correct sensing.

### 2. Ordinary refresh schedule / progress

The device/controller still performs the normal recurring refresh relation. A RowHammer failure can happen **without** simply omitting that ordinary schedule.

### 3. Aggressor-activity state in tracked mitigations

Counter/threshold-based designs retain some representation that a row has been activated often enough within a refresh-period window to require extra action. This can be exact or approximate; it is not the user payload.

### 4. Physical adjacency / mapping knowledge

Targeted refresh requires some authority to translate `hammered row` into the physical victim neighborhood. Logical address identity and physical interference topology are distinct state relations.

### 5. PARA policy state

PARA does not retain per-row access history, but the controller still embodies a policy parameter and random/probabilistic decision mechanism that changes maintenance behavior on row close. `Stateless` here means no per-row history table/counter of the type the paper contrasts with PARA, not literally no technical state anywhere in the controller.

---

## Physical / logical substrate

The substrate remains ordinary DRAM cells and their wordlines, bitlines, sense amplifiers, row buffers, refresh controls, and address/mapping machinery. The important addition is **coupling between nominally distinct rows**: the logical organization presents separately addressed rows, but the physical array does not guarantee that electrical activity in one row is irrelevant to retention in neighboring rows.

---

## Retention mechanism

A simplified ordinary path is:

```text
victim bit encoded as cell charge
    -> passive leakage
    -> periodic refresh before ordinary retention deadline
    -> charge restored
```

The disturbance path is:

```text
aggressor row repeatedly opened/closed
    -> wordline repeatedly toggles
    -> nearby victim-cell leakage accelerates
    -> ordinary refresh deadline may become too late
    -> bit may cross sensing margin and flip
```

Tracked targeted-refresh mitigation adds:

```text
retain / derive access count or hot-row indication
    -> threshold reached inside refresh window
    -> resolve physical victim neighborhood
    -> targeted refresh victim row(s)
```

PARA instead adds:

```text
row close event
    -> probabilistic maintenance decision
    -> occasionally open/refresh adjacent row
    -> higher aggressor activity increases cumulative chance of victim refresh
```

The same physical operation — opening a row and restoring its charge — can therefore participate in different temporal policies: ordinary periodic refresh, access-driven targeted refresh, or probabilistic access-coupled neighbor refresh.

---

## Addressing and access geometry

RowHammer makes three address relations non-equivalent:

1. **logical row identity** — what software/controller addressing refers to;
2. **physical row identity** — the actual wordline and cell row selected inside the DRAM organization;
3. **interference neighborhood** — which physical rows/cells can be disturbed by repeated activity on another row.

A targeted mitigation that knows only the logical identifier may be insufficient if remapping obscures physical adjacency. The 2012 patent and 2014 paper both make this mismatch part of the mitigation problem.

---

## Read semantics

Ordinary DRAM row activation is not a passive observation: sensing is followed by restoration of the opened row. In the RowHammer regime, repeated activation also has a **nonlocal side effect** on retention. An access to one row can influence charge survival in a row that was not requested.

Therefore:

> **nondestructive logical service to the requested address does not imply physically side-effect-free retention for neighboring addresses.**

This is an engineering reconstruction from the measured disturbance relation, not historical vocabulary.

---

## Write and erasure semantics

The bounded case is not about deliberate write or erasure. A victim bit flip is an **unauthorized physical state transition** caused by disturbance. It should not be described as normal overwrite, delete, invalidate, or secure forgetting.

A refresh performed *before* the victim crosses the sensing margin can restore the existing correct value. Once the victim has already been mis-sensed/corrupted, refresh by itself is not evidence that the original logical value can be reconstructed; recovery may require ECC, redundancy, or a known-good copy.

---

## Time

The case contains at least four relevant timescales:

- ordinary DRAM cell retention time / refresh interval;
- row-cycle / activation cadence that bounds how quickly an aggressor can be toggled;
- access-count threshold accumulated within a refresh-period window in tracked mitigations;
- extra targeted or probabilistic refresh timing triggered by access events rather than the ordinary global schedule alone.

The central temporal point is that the safe interval before restoration is **not invariant under workload**. A nominal 64 ms ordinary refresh window does not mean a disturbed victim cell necessarily retains adequate charge for 64 ms under arbitrary neighboring activation patterns.

---

## Maintenance and labor

Retention work is distributed across:

- DRAM cell/circuit design and isolation;
- manufacturing screening for disturbance susceptibility;
- ordinary refresh circuitry and memory-controller scheduling;
- optional hot-row detection / counters / thresholds;
- physical-row mapping knowledge;
- targeted-refresh command/interface design;
- controller policy such as PARA;
- ECC and higher-level recovery where corruption has already occurred;
- validation and characterization work needed to establish safe thresholds for real devices.

RowHammer therefore does not abolish the classic DRAM refresh obligation. It adds **interference-aware maintenance** on top of it.

---

## Failure / forgetting modes

Keep the following distinct:

- ordinary passive charge leakage beyond the refresh deadline;
- disturbance-accelerated leakage caused by repeated neighboring activation;
- missing or incorrect hot-row detection;
- threshold chosen too high for the actual device;
- targeted refresh issued to the wrong physical neighborhood because mapping/adjacency knowledge is wrong;
- probabilistic mitigation failing on a rare event path;
- multi-bit corruption exceeding the assumed ECC capability;
- already-corrupted data being refreshed without independent correction;
- process/device variation outside the tested characterization envelope.

Do not reduce all of these to `DRAM lost a bit`.

---

## Engineering reconstruction

### E — ordinary refresh compliance ≠ disturbance immunity

A controller can satisfy the recurring refresh schedule and still lose victim data if another row is activated often enough to accelerate victim leakage inside that schedule.

### E — time-driven leakage ≠ access-induced accelerated leakage

Both end in charge-margin loss, but the causal/time relation differs. Ordinary weak retention is dominated by how long charge is left without restoration; RowHammer adds activity elsewhere as a rate-changing variable.

### E — own-row access ≠ only-own-row physical effect

The requested logical operation targets one row, but repeated wordline activity can have measurable retention consequences in other rows.

### E — logical address isolation ≠ physical electrical isolation

Separate addressability does not guarantee that the underlying cells are physically independent. Reliability isolation is a stronger relation than address-space separation.

### E — victim cell ≠ ordinary weak-retention cell

The 2014 measurements found little overlap between cells failing the long-retention weak-cell test and RowHammer victim cells in the characterized modules.

### E — repeated activation can refresh the aggressor while degrading victims

The opened row is restored by its own accesses while nearby rows can lose charge faster. Preservation work and disturbance can be two sides of the same physical access event depending on which row is considered.

### E — retention interval can be workload- and topology-conditioned

For a victim row, the useful interval before restoration depends not only on elapsed time and temperature/device characteristics but also on activity in its physical neighborhood.

### E — global faster refresh ≠ targeted refresh

Both can reduce disturbance risk, but one increases periodic maintenance for all rows while the other conditions extra work on a detected or inferred local risk.

### E — targeted refresh ≠ payload correction after corruption

Refreshing a still-correct victim cell renews its charge margin. It does not by itself prove recovery of an original value after that value has already flipped.

### E — ECC presence ≠ failsafe against multi-bit disturbance

The measured multi-victim patterns exceed the single-error-correction assumptions of ordinary SECDED in some words.

### E — logical row adjacency ≠ guaranteed physical adjacency

Targeted preservation can depend on hidden/remapped physical topology rather than the obvious logical row numbering.

### E — topology knowledge can become retention infrastructure

If preservation policy must refresh threatened neighbors, the mapping from an aggressor identifier to its physical victim neighborhood participates in the ability to retain payload correctly.

### E — access-history tracking ≠ complete access-history retention

Counter/threshold schemes can retain a bounded statistic sufficient to trigger maintenance without keeping every memory access as a history.

### E — PARA statelessness ≠ absence of maintenance policy

PARA removes the per-row history structure discussed by the paper, but still embodies an access-coupled probabilistic rule. `Stateless` is therefore relative to the tracked-history alternatives, not a statement that the controller has no state or parameters.

---

## Functional analogies and limits

### A — Case 03 DRAM scheduled refresh

Case 03 establishes deadline-driven restoration under ordinary leakage. Case 92 shows that the same substrate can acquire an additional **workload-triggered** maintenance obligation because neighboring access shortens a victim's safe interval. This is the strongest internal comparison because the substrate is continuous while the maintenance semantics change.

### A — Case 70 magnetic-core half-select disturbance

Both cases show that `not logically selected` does not mean `physically untouched`: an operation aimed at one selected state can partially stress another state. The materials, circuits, timescales, and historical lineages are different; no descent is claimed.

### A — NAND read disturb

Repeated access in Flash/NAND can also impose stress on non-target cells/pages and eventually require relocation or recovery. The analogy is limited to **access-induced neighbor disturbance**. DRAM RowHammer acts through volatile-charge/wordline coupling and refresh; NAND read disturb involves different cell physics, voltage regimes, ECC margins, and maintenance strategies.

### A — Case 83 HDFS block scanning

Both cases expose maintenance that is not identical to ordinary foreground service. HDFS scanning verifies retained media and reports corruption; RowHammer mitigation must renew volatile charge quickly enough to prevent access-induced corruption. Verification and restoration are not the same operation.

---

## Prior-art and genealogy boundary

Do **not** claim:

- the 2014 ISCA paper discovered the first disturbance error in DRAM history;
- Intel invented all DRAM disturbance or all RowHammer mitigation because it filed a targeted-refresh patent in 2012;
- every DRAM module, generation, manufacturer, or modern DDR device has the same thresholds as the 129 modules studied in 2014;
- PARA was a historical industry standard or a deployed mechanism merely because the paper proposed and evaluated it;
- `targeted refresh`, later TRR-family mitigations, and modern refresh-management commands are one timeless mechanism;
- RowHammer victim cells are simply the same set as ordinary weak-retention cells;
- logical row-number adjacency reveals physical adjacency;
- refreshing an already-corrupted victim necessarily reconstructs the original payload.

Kim et al. themselves note older disturbance history and identify industry awareness of the RowHammer problem by at least 2012. The broader DRAM disturbance / TRR / RFM / security-exploit genealogy belongs in `computing-archaeology` if developed later. This case retains only the bounded 2012–2014 evidence needed for the retention argument.

---

## Philosophical / media-theoretical interpretation — bounded

### I — retention is not always a property of an isolated bearer

The classic shorthand `this cell retains for N milliseconds` invites an isolated-object picture. RowHammer shows why that description is conditional. A cell's recoverable future can depend on what the system does to nearby physical structures during the interval. The retained state is local, but the conditions of its continued retention are relational.

### I — technical isolation is maintained, not merely addressed

A memory architecture can give two rows distinct addresses while still requiring extra maintenance to prevent activity in one from altering the other. Addressability therefore supplies a logical distinction, not a complete guarantee of independent persistence. In this case, preserving the distinction can require knowledge of hidden topology and additional restoration work.

These are project interpretations, not claims that Intel or the ISCA authors used this philosophical vocabulary.

---

## What would falsify or narrow this case

- evidence that the 2014 experiments did not maintain ordinary refresh while producing the reported disturbance errors would narrow the `ordinary refresh compliance ≠ immunity` conclusion;
- evidence that the victim/weak-cell comparison was an artifact of the three modules tested in that section would require limiting that distinction more sharply to those samples;
- a device whose internal mapping exposes physical adjacency directly would weaken the mapping-opacity problem for that device, not the general logical/physical distinction;
- a mitigation with stronger correction or redundancy may preserve application-visible data after disturbance, but that would add another recovery layer rather than make the physical disturbance disappear;
- later standards or proprietary mitigations may change triggers and thresholds and must be analyzed in their own versions rather than projected backward into 2012–2014.

---

## Remaining work deliberately left open

- exact pre-2012 disturbance-error genealogy from early DRAM through 2010s devices;
- JEDEC DDR3/DDR4/DDR5 refresh and disturbance-mitigation chronology;
- vendor-specific Target Row Refresh / TRR implementations and reverse engineering;
- later RowHammer bypasses, Half-Double, many-sided hammering, and refresh-management commands;
- exact modern ECC-on-die interactions;
- RowHammer exploit/security history;
- named-device fault injection under controlled refresh and temperature conditions;
- process-physics reconstruction beyond the cautious mechanism boundary in the 2014 paper.

---

## Related repositories

A search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) found no existing RowHammer / DRAM-disturbance case at the time of this slice. If a broader disturbance genealogy is added there later, this file should reuse/link it rather than grow into a DRAM history.

---

## Sources

See [`../evidence/92-dram-2012-2014-rowhammer-grounding.md`](../evidence/92-dram-2012-2014-rowhammer-grounding.md).
