# Evidence 19C — Facebook f4 production correlated-failure and rebuild-window deepening

## Purpose

This note deepens Case 19 at one bounded production boundary left open by the fragment-placement pass: whether f4's failure-domain argument has a real production witness for correlated failures and an operational witness for the time/cost of restoring lost material.

It uses the same primary OSDI 2014 f4 paper, but a different part of the evidence: the authors' reported disk-failure experience and a deliberate rebuild drill. The goal is not to manufacture a reliability model from one anecdote. It is to separate four things that are easy to collapse:

1. algebraic code budget;
2. physical failure-domain isolation;
3. foreground service while repair is outstanding;
4. the duration and performance cost of background repair.

The note keeps four evidence layers distinct:

- **H — historical record:** what the 2014 f4 authors explicitly report from production or their drill;
- **E — engineering reconstruction:** bounded consequences of those reported facts;
- **F — functional comparison:** only relations already grounded in Case 19 / Synthesis 07;
- **P — philosophical interpretation:** none is needed for the technical claims below.

## Primary source

Subramanian Muralidhar et al., **“f4: Facebook's Warm BLOB Storage System,”** *11th USENIX Symposium on Operating Systems Design and Implementation (OSDI '14)*, 2014.

- USENIX paper: https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-muralidhar.pdf
- Relevant sections: §6.4 `f4 is Resilient to Failure` and §7 `Experience`, especially pp. 394–395 in the proceedings pagination.
- Accessed: 2026-09-13.

This is a primary production-system paper written by the operators/designers of the deployed system. The reported event and drill are strong evidence for **that deployment and period**, not universal failure rates for disks, Facebook datacenters, or erasure-coded stores.

## H — Historical record

### H1. The paper reports a normal disk AFR around 1%, not a claim of independent failures

In §6.4 the authors state that they generally observed an annualized failure rate of about 1% for their disks. Failed disks were normally replaced in less than three business days, so under ordinary conditions a cluster typically had only a few disks out at a time.

This is useful operational context, but it is not an independence theorem. The paper's later production experience gives a direct counterexample to reading the nominal AFR as if every drive failed independently with one stationary probability.

### H2. A bad disk cohort plus elevated temperature produced a cell-local correlated-failure episode

In §7 the authors report that a crop/batch of disks began failing at a higher-than-normal rate and that one region experienced higher-than-average temperatures, which exacerbated the bad disks' failure rate. They report that the combination raised AFR from the normal approximately 1% to **over 60% for a period of weeks**.

The high-failure-rate disks were constrained to **one f4 cell**. The authors report **no data loss** because the corresponding buddy and XOR blocks were in other cells with lower temperatures and were unaffected.

The paper's design lesson is explicit: future deployments should use greater **hardware heterogeneity** to reduce the likelihood of this kind of correlated failure.

This is a production incident witness for common-mode risk. It is not a proof that temperature alone caused the failures, that every disk in the cell failed, or that 60% is a reusable failure probability for another system.

### H3. The production witness depends on a protection relation outside the affected cell

The event did not merely demonstrate that one local Reed–Solomon stripe had four parity blocks. The authors specifically attribute the absence of data loss to the **buddy and XOR blocks being in other cells** that were not affected by the same elevated-temperature/bad-disk episode.

Thus the period record directly ties survival of this correlated event to failure-domain separation across cells and to the geo-XOR/buddy relation described elsewhere in the f4 paper.

`local coded fragments exist`

is therefore not the whole historical explanation of survival in this event.

### H4. A deliberate rebuild drill shows that restoration can remain outstanding for days

In §6.4 the authors describe their worst failure experience up to that point as a **self-inflicted drill** that rebuilt **two hosts' worth of data (240 TB)** in the background over **three days**.

The paper reports that the adverse effect observed during the drill was an increase in **p99 latency to 500 ms**.

This is not a reported accidental 240-TB loss event. It is an intentionally induced drill, and the note preserves that distinction.

### H5. The drill separates data/service continuity from normal performance

The rebuild ran in the background rather than blocking the system until all material was restored. At the same time, the reported p99 latency increase shows that continued service and normal service quality are different conditions.

The primary record therefore contains a concrete operational witness for:

`background repair in progress + continued service + degraded tail latency`.

It does not provide a complete latency distribution, user-impact study, or universal bound on rebuild overhead.

## E — Engineering reconstruction

### E1. Nominal AFR is not a safe substitute for correlated-failure geometry

The approximately 1% ordinary AFR describes the authors' general observation. The later >60%-for-weeks episode was associated with a shared bad hardware cohort and elevated temperature in one region/cell.

The bounded engineering consequence is:

`ordinary per-disk failure frequency != guarantee of independent failures`.

A reliability argument for coded storage must therefore keep **correlation domain and placement** separate from the scalar number of parity fragments.

This is exactly the seam exposed by Evidence 19B from the opposite direction: 19B shows that post-reconstruction placement can temporarily reduce future correlated-failure margin; this note shows a production episode in which a correlated physical/environmental cohort actually mattered.

### E2. Code budget and cross-cell isolation are different retained relations

During the reported event, the affected disks were confined to one cell while buddy/XOR blocks were outside it. The system survived because the relevant recovery material did not share the same failure domain.

Therefore:

`enough algebraic redundancy`

and

`that redundancy lies outside the active correlated-failure domain`

are distinct conditions.

The source does not license a stronger claim that every imaginable cell failure is survivable, or that all correlated failures align perfectly with f4's declared cells.

### E3. Data survival is not the same milestone as full repair completion

The drill provides a concrete time separation: 240 TB was rebuilt in the background over three days. Whatever foreground service remained available during that interval, the materialized repaired state was not instantaneous.

Thus:

`can continue serving`
`!=`
`repair complete`.

This is the production-scale counterpart to Case 19's already-grounded distinction between online requested-BLOB reconstruction and background full-block rebuild.

### E4. No data loss is not the same milestone as unaffected service quality

The drill's p99 latency rose to 500 ms while background reconstruction proceeded. Accordingly:

`no reported data loss`
`!=`
`no foreground performance cost`.

The same principle should not be inflated into a claim that every rebuild necessarily has that latency impact. The 500-ms figure belongs to this reported drill.

### E5. Repair duration is itself part of the reduced-margin interval

The code/failure-domain state after a fault and the eventual repaired state are separated by maintenance time. A three-day background rebuild witness makes that interval concrete at f4 scale.

For retention analysis this means future-failure margin is not just a static property of `10+4`; it also depends on how long missing material and any placement debt remain outstanding, and on whether other failure domains stay independent during that interval.

This is an engineering interpretation of the reported drill, not a source claim that f4 exposed one scalar `repair-margin clock`.

## F — Functional comparison within the repository

Synthesis 07 already separates algebraic reconstructability, degraded-service admissibility, materialized repair, restored redundancy margin, and later integrity confidence. This f4 production witness adds another bounded coordinate:

- **correlation / placement geometry** determines how many coded contributions one physical event can remove;
- **repair duration** determines how long the system remains dependent on the reduced relation;
- **foreground service quality** may degrade even when data remains available.

The comparison is functional only. It does not claim that f4, RAID, ZFS, or Azure LRC share one implementation or genealogy.

## Explicit non-claims

This evidence does **not** establish that:

- 60% AFR is a general f4, Facebook, or disk-drive failure rate;
- every drive in the affected cell failed;
- high temperature alone caused the incident;
- the bad manufacturing cohort and temperature contributions can be quantitatively separated from the paper;
- the incident exhausted f4's local Reed–Solomon `(10,4)` budget stripe by stripe;
- absence of reported data loss proves every BLOB remained continuously available at every instant;
- a three-day two-host drill is equivalent to a natural cell outage;
- 500-ms p99 latency is a universal rebuild penalty;
- adding hardware heterogeneity has a source-supported numerical risk-reduction factor;
- geo-XOR/buddy placement makes every correlated datacenter or region failure survivable;
- the event proves fragment currentness, checksum validity, or repair atomicity beyond what the f4 paper actually reports.

## Retention consequence

Case 19 can now pair its placement-invariant negative control with an actual production correlated-failure witness and a quantitative repair-window drill.

The strongest bounded relation is:

```text
coded information sufficient
+ recovery material outside the active correlated-failure domain
+ foreground service path
+ background repair capacity over a nonzero time window
-> survival/continuity for the reported f4 episode and drill
```

while preserving the negative controls:

`nominal AFR != independence guarantee`

`no data loss != no service degradation`

`service continuity != repair completion`

`code budget != failure-domain isolation`.

This closes the narrow **production incident / operational rebuild witness** debt for Case 19. It does **not** close the separate open question of direct per-fragment currentness evidence during an incomplete rebuild, nor does it supply a general probabilistic reliability model.
