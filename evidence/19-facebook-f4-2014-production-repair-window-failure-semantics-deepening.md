# Case 19 evidence deepening — f4 production repair window and failure semantics

**Status:** bounded deepening complete  
**Case:** [`../cases/19-facebook-f4-erasure-coded-failure-domains.md`](../cases/19-facebook-f4-erasure-coded-failure-domains.md)  
**Bounded period:** production experience reported in October 2014  
**Primary source:** Subramanian Muralidhar et al., “f4: Facebook’s Warm BLOB Storage System,” OSDI ’14

---

## 1. Why this slice exists

The canonical Case 19 already establishes that f4 separates:

- direct normal reads;
- online requested-BLOB reconstruction;
- offline full-block rebuilding;
- post-rebuild placement balancing;
- local Reed–Solomon protection from geo-XOR protection.

A previous deepening also established that reconstructing a block does not by itself restore ideal failure-domain placement.

What remained underdeveloped was a different retention relation visible in the paper’s **production failure experience**:

> a storage component can be unavailable without its stored embodiment being destroyed, and foreground service can continue while a much longer background repair interval remains open.

The same paper reports a concrete controlled failure drill in which **two hosts’ worth of data, 240 TB, were rebuilt in the background over three days**, while the paper identifies the observed adverse effect as an increase in p99 latency to 500 ms.

This slice therefore does **not** reopen the general history of f4 or erasure coding. It isolates four boundaries:

```text
component unavailable
    != stored embodiment destroyed

read/service availability
    != full redundancy restored

repair started
    != repair completed

long background repair interval
    != equivalent period of total service outage
```

The last relation is bounded to the reported drill and must not be universalized into a guarantee for every f4 failure episode.

---

## 2. Source discipline

### 2.1 Directly inspected primary source

Subramanian Muralidhar, Wyatt Lloyd, Sabyasachi Roy, Cory Hill, Ernest Lin, Weiwen Liu, Satadru Pan, Shiva Shankar, Viswanath Sivakumar, Linpeng Tang, and Sanjeev Kumar, **“f4: Facebook’s Warm BLOB Storage System,”** *11th USENIX Symposium on Operating Systems Design and Implementation (OSDI ’14)*, 6–8 October 2014, pp. 383–398.

USENIX publication page:

<https://www.usenix.org/conference/osdi14/technical-sessions/presentation/muralidhar>

USENIX open-access PDF:

<https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-muralidhar.pdf>

Relevant locations directly checked:

- paper pp. 389–390 / PDF pp. 7–8: backoff reconstruction, rebuilder nodes, coordinator scheduling, throttling;
- paper pp. 393–394 / PDF pp. 11–12: production methodology, failure analysis, disk AFR, host-return behavior, and the 240 TB / three-day drill;
- paper p. 390 / PDF p. 8: placement balancing after failure/reconstruction/replacement.

### 2.2 Visual inspection

The USENIX PDF pages containing the relevant paragraphs and Figure 14 were visually inspected, not only consumed through search snippets.

### 2.3 Companion-repository check

`tmzncty/computing-archaeology` was searched for dedicated `f4` / Facebook warm-BLOB / rebuild material before writing this slice. No dedicated case was found.

Accordingly this record keeps only the retention-specific production-failure boundary. It does not attempt to build a general Facebook storage history.

---

## 3. Historical record

### H/P — the evaluation distinguishes production measurements from analytic failure modeling

Section 6 says that most evaluation results come from production-system measurements, while §6.4’s broad failure-tolerance curves are analytic. The paper separately describes how request traces and sampled stored content were measured in production.

This distinction matters because Figure 14 is **not** itself a trace of thousands of simultaneous failed disks or racks. The authors use a modeled/analytic failure exercise to estimate unavailable-BLOB fractions under increasing numbers of failures, then separately report their actual failure experience.

Historical boundary:

```text
Figure 14 modeled resilience curve
    != observed production incident trace
```

The production experience paragraphs must therefore be read separately from the analytic stress curves.

**Primary anchors:** Muralidhar et al. 2014, §6.1 and §6.4, paper pp. 393–394.

---

### H/P — f4 continually monitors and rebalances placement while evaluating failure resilience

At the start of §6.4 the paper says the implementation places blocks on different racks initially and **continually monitors and rebalances** them so that failures do not leave the intended rack separation permanently degraded. It says blocks are consequently almost always in different failure domains and uses that as an assumption for the rest of the Figure 14 analysis.

This is important negative evidence against a purely static reading of the erasure-code layout. The fault model used by the evaluation depends on continuing maintenance of placement geometry.

It does **not** prove that every stripe is always perfectly distributed, and the design section explicitly allows rare placement violations.

**Primary anchor:** Muralidhar et al. 2014, §6.4, paper p. 393.

---

### H/P — disk failures and replacement introduce a nonzero degraded interval

In the production `Failure Experience` paragraph, the authors report an approximate disk Annualized Failure Rate of **~1%**. Failed disks are replaced in **less than three business days**, and the paper says a cluster therefore typically has at most a few disks out at a time.

The paper also reports that one cluster had recently received a batch of bad disks and consequently had a higher failure rate. Even with that batch, the authors characterize their observed state as remaining on the far-left region of Figure 14 where the modeled best/worst/expected curves had not yet materially diverged.

Historical record:

```text
ordinary production
    -> disk failures occur
    -> failed disks may remain out for a nonzero replacement window
    -> background redundancy/placement machinery carries the system through that interval
```

The source does not say that every failed disk waits for physical replacement before missing blocks can be rebuilt; it says failed disks are replaced within that operational window and separately describes background reconstruction machinery.

**Primary anchor:** Muralidhar et al. 2014, `Failure Experience`, paper p. 394.

---

### H/P — a host failure need not mean loss of the host’s disk-resident data

The paper says host failures occur less often than disk failures and that host failures **typically do not lose data**. Its concrete example is replacement of a faulty component such as DRAM, after which the host returns with the data still on its disks.

This is a particularly useful historical witness because `host unavailable` can otherwise be silently treated as equivalent to `all embodiments on that host destroyed`.

The source instead supplies at least two possible meanings of a host-level failure episode:

```text
host unavailable because a non-disk component failed
    -> disks may remain intact
    -> repair of host component
    -> host can return with prior disk data

versus

failure that actually removes disk-resident block embodiment
    -> coded reconstruction may be required
```

The paper does not enumerate every host-failure mode, so this is not a claim that host failures never lose data.

**Primary anchor:** Muralidhar et al. 2014, `Failure Experience`, paper p. 394.

---

### H/P — the paper reports a controlled 240 TB, three-day background rebuild

The strongest production-like bounded repair-window evidence in the paper is a **self-inflicted drill** that the authors call their worst failure so far.

The drill rebuilt **two hosts’ worth of data, 240 TB**, **in the background over three days**. The authors state that the only adverse effect of the drill was an increase in **p99 latency to 500 ms**.

This is not an uncontrolled natural failure incident; it is explicitly described as a drill. That distinction must be preserved.

What the report does establish is that in this exercised production system:

```text
large repair work existed for ~3 days
    + repair ran in the background
    + foreground requests still had a measured latency distribution
```

Therefore the existence of an open repair obligation did not equate to a three-day complete service outage.

**Primary anchor:** Muralidhar et al. 2014, `Failure Experience`, paper p. 394.

---

### H/P — rebuild is intentionally throttled against foreground demand

The design section says rebuilder nodes reconstruct missing blocks by fetching `n` companion/parity blocks, and that rebuilding creates significant disk and network load. Rebuilders **throttle themselves** to avoid adversely impacting online user requests. Coordinators are responsible for scheduling rebuilds to minimize the likelihood of data loss.

Rebalancing is likewise described as expensive and throttled.

This means the three-day repair duration cannot safely be interpreted as a raw coding-throughput limit. The documented mechanism intentionally trades repair speed against foreground service impact.

Historical relation:

```text
repair duration
    = result of missing work
    + available disk/network resources
    + scheduling / throttling policy
    + concurrent foreground demand
    + other system conditions
```

The equation is an engineering decomposition, not a literal formula from the paper.

**Primary anchor:** Muralidhar et al. 2014, `Rebuilder Nodes` / `Coordinator Nodes`, paper p. 390.

---

## 4. Engineering reconstruction

### E — failure episode ≠ embodiment loss

The host-return example gives a direct counterexample to an easy abstraction error:

```text
component not serving requests right now
    !=
data previously stored behind that component has ceased to exist
```

A failed DRAM or other replaceable host component can make a host unavailable while its disks still preserve their block embodiments.

This distinction matters because the correct retention response can differ:

- temporary rerouting / online reconstruction may bridge service;
- hardware repair may return the original disk-resident embodiment;
- durable coded rebuild may be necessary only when an embodiment is actually lost or considered unavailable long enough to justify replacement.

The paper does not specify the exact threshold at which f4 chooses to rebuild a transiently unavailable host’s blocks, so that policy must remain unstated.

---

### E — service availability ≠ restored redundancy margin

The 240 TB drill is useful precisely because repair took three days while the source still reports foreground latency rather than a multi-day outage.

That supports:

```text
client-visible service can continue
    while
background redundancy repair is incomplete
```

It does **not** follow that every affected stripe retained its full pre-drill margin at every instant during those three days. On the contrary, the point of background rebuild is to restore missing encoded contributions.

Thus:

> `can still serve reads` ≠ `all intended redundant embodiments are already restored`.

This is stronger than the purely architectural distinction between backoff reads and rebuilder work because the drill demonstrates a long-lived exercised interval in which repair work and foreground service coexist.

---

### E — repair completion is a temporal risk boundary, not merely a performance statistic

For an `(10,4)` stripe, four unavailable blocks are within the paper’s stated Reed–Solomon erasure budget and more than four exceed the simple implemented recovery model used in §6.4.

When one or more fragments are absent, the system has less remaining tolerance for additional failures until repair completes. Therefore a three-day repair interval is not only `time consumed by maintenance`; it is also a period during which some affected redundancy relations can be weaker than after repair.

Bounded reconstruction:

```text
failure
    -> reduced redundancy margin for affected stripes
    -> background rebuild interval
    -> rebuilt contribution restored
    -> separate placement balancing may still remain
```

The paper does not publish a stripe-by-stripe timeline for the drill, so it would be too strong to claim that every affected stripe remained degraded for the full three days.

---

### E — foreground latency and redundancy state are different observables

The paper reports `p99 latency = 500 ms` as the drill’s adverse service effect. This is an externally visible performance measure.

It is not a direct measure of:

- how many stripes were degraded at each time;
- how many blocks had already been rebuilt;
- whether placement balancing had converged;
- how close any stripe was to exhausting its remaining erasure budget.

So:

```text
latency telemetry
    != repair-progress ledger
    != redundancy-margin ledger
```

A system can expose acceptable service latency while internal maintenance debt remains significant.

---

### E — physical replacement time and logical repair time need not be the same clock

The paper mentions disk replacement in less than three business days and separately describes automated background block reconstruction. Those are different operations.

A disk being physically replaced does not by itself tell us whether:

- all blocks formerly on it have already been reconstructed elsewhere;
- reconstruction waits for replacement;
- a replacement target receives repaired blocks before/after installation;
- placement balancing has completed.

Therefore:

```text
hardware replacement complete
    != proved logical repair complete

logical block reconstructed
    != proved ideal placement restored
```

The exact orchestration is outside what this paper documents.

---

## 5. Functional comparisons

### A — Case 17 RAID degraded service

Both Case 17 and this f4 slice distinguish continued service from completed redundancy repair.

The analogy is functional only:

- RAID may continue serving through degraded mode and later rebuild a device/stripe set;
- f4 can reconstruct requested BLOB ranges online while coordinator/rebuilder work restores full missing blocks across distributed failure domains.

f4 additionally separates block reconstruction from rack/failure-domain placement repair, and the paper reports a multi-day background repair drill in production.

Do not infer direct implementation lineage from this comparison.

---

### A — Case 24 Windows Azure LRC representation handoff

Case 24’s transition debt is a **representation-change** problem: full replicas coexist with newly produced coded fragments until validation/completion metadata permits source-replica retirement.

This f4 slice is a **failure-repair** problem after a coded representation is already in service.

Both cases show that background maintenance can remain open while foreground service or an older representation continues to carry availability, but the state transitions differ:

```text
WAS LRC
old redundancy regime -> validated new regime -> old replicas retire

f4 rebuild
coded regime degraded -> missing contribution reconstructed -> margin restored
```

That is a functional comparison, not evidence of shared code or genealogy.

---

### A — Case 136 rebuild-rate control

Case 136 shows explicitly configurable array-controller rebuild priority/rate. f4 instead documents rebuilder throttling and coordinator scheduling in a distributed erasure-coded system.

The shared function is bounded:

> repair speed is a policy/resource trade-off against foreground work.

The specific controls, state geometry, failure domains, and completion criteria are different.

---

## 6. Philosophical interpretation

The technically grounded philosophical trigger here is **persistence during an unfinished repair**.

A simplistic picture says an object either survives a failure or it does not. The f4 drill makes a more graded technical sequence visible:

```text
object remains answerable
    while
some redundancy relation is under repair
    while
repair itself competes with ordinary use
```

The retained object is therefore not adequately described by asking only whether bytes can presently be returned. Future fault margin is also a maintained relation, and it can be temporarily weaker even while ordinary access remains available.

This does **not** justify calling `degraded mode` a philosophical category in its own right. The conceptual use is narrower: maintenance can be constitutive of continued availability without needing to be complete at every moment.

---

## 7. Explicit non-claims

This slice does **not** claim that:

1. the 240 TB drill was an accidental production outage;
2. every f4 repair of 240 TB takes three days;
3. the drill’s three-day duration is an intrinsic Reed–Solomon coding limit;
4. all affected stripes were degraded for exactly three days;
5. p99 latency of 500 ms proves zero failed requests or zero unavailable BLOBs;
6. the paper provides a durable per-stripe rebuild-progress log;
7. a host failure never destroys data;
8. a disk failure always requires waiting for physical disk replacement before reconstruction;
9. physical disk replacement completion equals logical block-repair completion;
10. block reconstruction completion equals placement-balancer convergence;
11. the bad-disk batch caused data loss;
12. Figure 14 is an observed trace of thousands of simultaneous failures;
13. f4 invented background rebuilding, degraded service, or erasure-coded repair;
14. later Facebook/Meta storage systems preserve the same repair policy or topology.

---

## 8. Claim ledger

| Claim | Type | Strength |
|---|---|---|
| f4 production paper reports ~1% disk AFR | H/P | direct primary text |
| failed disks were replaced in less than three business days | H/P | direct primary text |
| hosts often returned with disk data intact after non-disk component repair | H/P | direct primary text |
| a self-inflicted drill rebuilt two hosts / 240 TB in background over three days | H/P | direct primary text + visually inspected page |
| paper reports the drill’s adverse effect as p99 latency reaching 500 ms | H/P | direct primary text + visually inspected page |
| rebuilders throttle to protect foreground requests | H/P | direct design description |
| coordinators schedule rebuilds to reduce data-loss likelihood | H/P | direct design description |
| placement is continually monitored/rebalanced | H/P | direct primary text |
| component unavailability ≠ embodiment destruction | E | bounded inference anchored by host-return example |
| service availability ≠ full redundancy restored | E | bounded inference anchored by online reads + multi-day rebuild |
| repair interval is also a reduced-margin exposure interval | E | mechanism reconstruction; stripe-specific duration not claimed |
| latency telemetry ≠ repair-progress state | E | bounded measurement-state distinction |
| f4 drill proves zero request failure | X | unsupported |
| three days is an intrinsic coding limit | X | contradicted by documented throttling/scheduling context |

---

## 9. What this closes, and what remains open

### Closed by this bounded slice

- Case 19 now has a separately identified **production repair-window witness**, rather than only architectural repair descriptions and analytic placement/failure reasoning.
- The repository now has direct period evidence for `host unavailable != host disk data destroyed` in this system.
- The case now has a concrete exercised example in which substantial background repair coexisted with foreground service for days.
- The relation `foreground service restored/continued != redundancy repair complete` is no longer only a schematic architecture inference.

### Still open

- exact persisted representation, if any, of per-block/per-stripe rebuild progress;
- restart/crash behavior of rebuilder/coordinator state during an incomplete rebuild;
- exact policy threshold for rebuilding a temporarily unavailable host versus waiting for return;
- stripe-by-stripe timing and margin telemetry during the 240 TB drill;
- a naturally occurring production data-loss/unavailability incident with sufficient technical detail;
- later f4 evolution and whether repair state became more explicitly durable/observable.

Those should be separate slices. They must not be inferred from the 2014 paper’s drill.

---

## 10. Navigation consequence

The canonical Case 19 should now distinguish three different completion boundaries:

```text
requested BLOB reconstructed for this read
    !=
missing full block reconstructed durably
    !=
preferred failure-domain placement restored
```

and one orthogonal failure boundary:

```text
host unavailable
    !=
host-resident disk embodiment destroyed
```

The 240 TB drill adds a concrete production-time relation:

```text
foreground service continues
    while
large background repair remains unfinished
```

This evidence should be linked from the canonical case as a production repair-window deepening, without changing Case 19’s existing `grounded` maturity.