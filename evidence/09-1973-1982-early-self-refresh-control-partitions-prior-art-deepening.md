# Evidence 09 — 1973–1982 early self-refresh control partitions prior-art deepening

**Status:** `bounded deepening complete`

**Parent case:** [`../cases/09-dram-cbr-refresh-address-internalization.md`](../cases/09-dram-cbr-refresh-address-internalization.md)

**Earlier adjacent record:** [`09-1981-1983-autonomous-self-refresh-prior-art-deepening.md`](09-1981-1983-autonomous-self-refresh-prior-art-deepening.md)

**Direct-inspection follow-up:** [`09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md`](09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md)

**Bounded question:** how far before the already-grounded 1981–1983 DRAM self-refresh literature can public technical evidence establish internal refresh scheduling, internal row selection, and access/refresh arbitration—and what does that do to Case 09's chronology without turning a patent chain into an invention-priority genealogy?

This record is intentionally narrow. It does **not** attempt a complete history of dynamic-memory refresh, a first-invention claim, a shipment chronology, a JEDEC genealogy, or a direct descent argument from 1970s patents to later commodity DRAM. It deepens only the prior-art boundary relevant to retention-control authority.

A later direct-inspection follow-up closes the GTE lead that was originally left open here. The result is important precisely because it does **not** merely move the on-chip chronology earlier: GTE's April-1973 `self-initiating refresh` patent describes an automatically recurring **memory-system-level** refresh controller around commercial Intel 1103 chips. It therefore adds a distinct control partition and a terminology warning rather than an earlier witness for chip-local self-refresh.

---

## Result in one sentence

By public patent publication, **April 1973** already supplies a self-initiating recurring refresh controller at the memory-system boundary; **June 1973** supplies a MOS-memory self-refresh design in which row-specific deadline state can force refresh and block access; and **1980** and **1982** Texas Instruments patents cleanly separate two other partitions—external refresh cadence with on-chip row enumeration, and internally timed on-chip refresh whose occasional overlap is absorbed into access latency.

The conservative chronology is therefore:

```text
1973-04-24 GTE public patent
    automatic recurring refresh at memory-system boundary
    + system-level row counter / address gating
    + memory-busy service deferral
    != on-chip self-refresh

1973-06-05 MOS Technology public patent
    self-refresh / deadline-tracked mandatory refresh
    + row-specific refresh-age evidence
    + optional opportunistic early refresh

1980 public TI patent
    external refresh command cadence
    + internal row enumeration

1982 public TI patent
    internal refresh cadence
    + internal row enumeration
    + refresh/access arbitration
```

The 1981 Reese paper remains valuable as a peer-reviewed DRAM publication witness; it is not the earliest public witness in this repository for the broader refresh-control problem.

---

## Sources and evidence boundary

### 1. GTE Automatic Electric Laboratories, US 3,729,722, `Dynamic mode integrated circuit memory with self-initiating refresh means`

- Inventor: Joseph Patrick Shuba.
- Original assignee: GTE Automatic Electric Laboratories Incorporated.
- Filed / priority: **17 September 1971**.
- Granted / public patent date: **24 April 1973**.
- Direct text inspected in follow-up: <https://patents.google.com/patent/US3729722A/en>
- Detailed record: [`09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md`](09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md).

The preferred embodiment uses commercial Intel 1103 MOS dynamic-memory chips and places the free-running refresh clock, pulse generator, row-address counter, address gating, and `memory busy` relation around the memory chips at the system level. A refresh counter sequentially supplies maintenance row addresses; ordinary accesses attempted during refresh are deferred.

This is direct primary evidence for **automatic recurring system-level refresh**. It is not evidence that the Intel 1103 itself contained the refresh controller or that the patent discloses on-chip self-refresh.

### 2. MOS Technology, US 3,737,879, `Self-refreshing memory`

- Inventors: Richard M. Greene, Donald L. McLaughlin, John O. Paivinen.
- Assignee: MOS Technology, Inc.
- Filed: **5 January 1972**.
- Granted / public patent date: **5 June 1973**.
- Application: `05/215,506`.
- Public transcript used for direct text inspection: <https://uspto.report/patent/grant/3737879>
- Patent corpus mirror: <https://patents.google.com/patent/US3737879A/en>

The public transcript states that a different counter is associated with each row; an ordinary read-and-restore or write resets that row's counter; if a row goes without such service for the permitted maximum interval, the counter initiates a **mandatory refresh** and temporarily inhibits access. An optional path can use otherwise idle intervals for **voluntary refresh** of rows nearest to needing mandatory service.

This is public patent evidence. It is **not** a demonstrated commercial MOS Technology DRAM product and does not establish how widely the architecture was implemented.

### 3. Texas Instruments, US 4,207,618, `On-chip refresh for dynamic memory`

- Inventors: Lionel S. White, Jr.; G. R. Mohan Rao.
- Assignee: Texas Instruments Inc.
- Filed / priority: **26 June 1978**.
- Published / granted: **10 June 1980**.
- Public text: <https://patents.google.com/patent/US4207618A/en>

The patent places a refresh-address counter and address multiplexing on the dynamic-memory chip. Its summary says the only external signal needed is a **refresh command**; that command makes the on-chip mechanism select the row defined by the internal counter and then advance the counter.

The detailed embodiment says the row address for refresh is internally generated and the sequential counter advances for each externally supplied `RF` refresh signal. The rows still must be traversed within the maximum refresh interval.

This is a particularly clean witness for:

```text
refresh-address authority on chip
    != recurring refresh-cadence authority on chip
```

The TI patent cites GTE US3729722A as prior art. The GTE text has now been directly inspected in the follow-up record. That citation is retained only as a formal patent-document relation; it is not treated as proof of implementation inheritance or direct engineering influence.

### 4. Texas Instruments, US 4,333,167, `Dynamic memory with on-chip refresh invisible to CPU`

- Inventor: David J. McElroy.
- Assignee: Texas Instruments Incorporated.
- Filed: **5 October 1979**.
- Granted / public patent date: **1 June 1982**.
- Public transcript: <https://patents.justia.com/patent/4333167>

This patent moves the recurring trigger itself on chip. Its claims describe a refresh address counter and a refresh-signal generator within the semiconductor body, with refresh signals produced at **regular internally defined intervals**.

The implementation uses an on-chip refresh clock generator, an internal sequential row counter, address multiplexing, sense/refresh amplifiers, and control logic. It also specifies the collision rule: if a read or write begins after refresh has started, refresh finishes first and the normal access proceeds afterward. The published timing budget includes that possible wait.

Again, this is patent disclosure, not a named shipped DRAM-product specification.

---

## Historical record

### H/P — self-initiating recurring refresh is public in April 1973, but at a system boundary

The GTE patent is publicly dated 24 April 1973 and explicitly uses `self-initiating refresh` language. Direct inspection shows that the preferred embodiment is a refresh controller around commercial Intel 1103 chips rather than a chip-local refresh engine.

Its checked control partition is:

```text
free-running system refresh clock
    -> refresh pulse generator
    -> system-level row counter
    -> address gating selects maintenance row
    -> dynamic-memory chips execute refresh cycle
```

The patent also maintains a `memory busy` relation while refresh occupies the array interface, so an external access can be deferred.

Therefore:

```text
self-initiating at memory-system boundary
    != self-initiating at DRAM-package boundary
```

This is the central correction supplied by the follow-up.

### H/P — public row-deadline self-refresh evidence reaches June 1973

US 3,737,879 is publicly dated 5 June 1973 and explicitly calls itself a `self-refreshing memory` system. Its logic is not merely a free-running global sweep. It associates refresh-age state with rows and lets an expired row counter trigger mandatory refresh.

The bounded historical relation is:

```text
public technical self-refresh disclosure
    by June 1973
        includes deadline-tracked row refresh
        + forced refresh admission
        + access inhibition during mandatory refresh
```

This does **not** establish the first self-refresh invention.

### H/P — ordinary accesses can discharge a later refresh obligation in the MOS design

In US 3,737,879, a row's counter is reset when that row is accessed for writing or for reading followed by restore. Thus an ordinary service operation and a maintenance operation can both satisfy the same underlying retention need.

```text
maintenance obligation exists
    != a dedicated refresh command must necessarily perform the next restoration
```

### H/P — the MOS design contains mandatory and opportunistic refresh

The patent's `mandatory` path waits until a row reaches its maximum permitted no-refresh interval, then inhibits access and refreshes the row. Its optional `voluntary` path instead detects a sufficiently long pause in memory demand and refreshes one or more rows closest to requiring mandatory refresh.

This establishes, in period vocabulary, a distinction between deadline-forced and opportunistic early maintenance without importing modern scheduler identity.

### H/P — TI's 1980 patent internalizes enumeration but keeps cadence external

US 4,207,618 places the row counter and row-address source inside the memory chip, while requiring an externally supplied refresh signal for each refresh event.

```text
external system
    decides that a refresh event occurs now

memory device
    chooses the refresh row internally
    executes refresh
    advances the internal row counter
```

This is directly relevant to later CBR/AUTO-REFRESH comparisons, but it is not itself a claim about later JEDEC command vocabulary.

### H/P — TI's 1982 patent internalizes cadence and arbitrates collisions

US 4,333,167 adds an internal refresh clock generator. Its row counter advances from internally generated refresh timing rather than from one external refresh request per cycle.

If an ordinary access arrives after refresh begins, the disclosed design finishes maintenance first and then services the request. The title's `invisible to CPU` language therefore cannot safely be read as `refresh takes no time`.

```text
host need not schedule each refresh
    != physical refresh disappears

maintenance wait absorbed into service timing contract
    != zero maintenance latency
```

### H/P — `static-like` service does not mean static-cell physics

The TI patents motivate their designs partly by the cost/board-space burden of conventional external dynamic-memory refresh and by the desire for static-like interface convenience. The retained data nevertheless remain dynamic cell charge requiring periodic restoration.

---

## Retained-state decomposition

The early patents make several state classes distinguishable without relying on later SDRAM terminology.

### 1. Payload state

The user-visible bit value is embodied in dynamic MOS cell charge and is subject to leakage.

### 2. Refresh-age / deadline evidence

In US 3,737,879, row counters encode whether a row is approaching or has reached the maximum allowed interval without a restorative event.

This is maintenance-control state, not application payload.

### 3. Refresh-coverage position

In the GTE system-level controller and the TI 1980/1982 designs, a sequential counter identifies which row will be refreshed next.

This is not the same relation as the MOS Technology per-row age counters. Both influence maintenance selection, but they encode different facts.

### 4. Cadence authority

- GTE 1973: a free-running **system-level** clock automatically supplies recurrence.
- TI 1980: a repeated **external refresh command** supplies recurrence while the device owns row enumeration.
- TI 1982: an **on-chip refresh clock** supplies recurrence.

### 5. Address-source authority

During refresh, maintenance address state takes authority over the row decoder/address drivers instead of the ordinary service address path. The physical location of that maintenance-address source differs across designs.

### 6. Access/maintenance arbitration state

The GTE patent exposes a `memory busy`/defer relation; the MOS patent can inhibit access during mandatory refresh; the TI 1982 patent latches or delays a request when refresh is already underway.

These are control relations layered around the same underlying dynamic-retention problem.

---

## Engineering reconstruction

### E — `automatic`, `on-chip`, and `self-refresh` are not one axis

The direct GTE inspection adds a control dimension that was previously only a lead.

At least three questions must be separated:

```text
who supplies recurring maintenance cadence?
where is the cadence machinery physically located?
where is row-enumeration / due-state evidence located?
```

GTE 1973 shows automatic recurrence can exist at the memory-system boundary while row enumeration remains outside the DRAM chip. TI 1980 shows the opposite partial partition: enumeration moves on-chip while recurring event timing remains external. TI 1982 moves both recurrence and enumeration on-chip.

Therefore:

> **refresh autonomy != refresh-control integration.**

### E — `when`, `which row`, and `who waits` are independently movable control functions

The source set exposes at least these separable questions:

```text
when must maintenance occur?
which row should receive it?
where is that decision represented?
what happens if service arrives at the same time?
```

US 3,737,879 uses row-age/deadline state to decide when a particular row has become mandatory and can exploit idle periods for earlier work.

GTE US3729722A automates recurrence with a system-level free-running clock and system-level traversal counter.

US 4,207,618 moves row enumeration on chip while leaving repeated event timing outside.

US 4,333,167 moves recurring event timing on chip as well and defines a collision/latency policy.

Thus:

```text
internal row enumeration
    != internal deadline/cadence authority
    != automatic system-level recurrence
    != access arbitration policy
```

### E — refresh can be hidden by changing the observer's contract, not by eliminating maintenance

The GTE controller can remove the need for a CPU/requester to issue each refresh event while still exposing `memory busy` and access deferral. TI's 1982 patent can hide recurring refresh commands from the CPU while occasional collisions still affect access latency.

So:

```text
refresh initiation hidden from requester
    != refresh occupancy hidden from requester
    != refresh does no work
```

### E — event-triggered restoration and deadline-triggered restoration can coexist

The MOS design treats read-and-restore, writes, mandatory refresh, and voluntary refresh as different events that can all affect a row's future refresh need.

```text
row restored by ordinary access
    -> age evidence resets
    -> dedicated refresh can be deferred

row not otherwise restored
    -> age evidence advances
    -> mandatory refresh eventually becomes necessary
```

This sharpens the repository's distinction between access-triggered restoration and deadline-driven maintenance: the trigger classes differ but can interact in one system.

### E — selective deadline state is not the same thing as a cyclic refresh pointer

US 3,737,879's per-row counters represent how recently each row has been serviced. The GTE/TI sequential refresh counters represent traversal position.

```text
row-age evidence
    != next-row pointer

proof that row X is due
    != proof that a cyclic enumerator currently names X
```

### E — internalization relocates responsibility, not the retention deadline itself

Across the source set, the physical requirement remains that every required dynamic row be restored within its allowed interval. What changes is the boundary responsible for satisfying and organizing that requirement.

> **a retention obligation may remain constant while the authority that schedules, enumerates, and arbitrates its maintenance migrates across a board, package, or system boundary.**

---

## Functional comparisons

The following comparisons are **functional analogies only** unless a formal patent citation is explicitly identified. They do not assert direct historical descent.

### A — GTE 1973 vs TI 1980

The pair isolates opposite partial internalizations:

```text
GTE 1973 preferred embodiment
    automatic system-level cadence
    + system-level row enumeration

TI 1980
    external refresh command cadence
    + on-chip row enumeration
```

This is a strong counterexample to a one-dimensional `more automatic = more integrated` narrative.

TI's patent corpus formally cites the GTE patent. That proves a document-level prior-art relation, not a product genealogy.

### A — GTE 1973 vs MOS Technology 1973

Both patents use autonomy-like refresh vocabulary, but their control evidence differs:

```text
GTE
    global free-running cadence
    + cyclic traversal counter

MOS Technology
    row-specific age/deadline evidence
    + mandatory / opportunistic refresh
```

Similar vocabulary does not establish identical scheduler geometry or shared implementation lineage.

### A — TI 1980 vs later AUTO/CBR-style control partition

US 4,207,618 functionally resembles the later partition in which the device owns refresh-row enumeration but the outside system still supplies recurring refresh events.

```text
external recurrence
    + internal row enumeration
```

The electrical interface, command encoding, device generation, and standards context differ. `Functional resemblance != JEDEC genealogy`.

### A — TI 1982 vs later SELF REFRESH

US 4,333,167 functionally resembles later self-refresh in one narrow respect: recurring refresh timing and row enumeration are both internal.

But the patent describes a memory designed to admit ordinary requests around internal refresh events, whereas later SDRAM SELF REFRESH is a mode with its own entry/exit and service restrictions.

```text
internal recurrence + internal enumeration
    != identical self-refresh mode semantics
```

### A — 1973 deadline-tracked rows vs modern retention-aware refresh research

US 3,737,879 is a useful historical counterexample to any broad novelty statement that `refresh only what appears to need refresh` is intrinsically a twenty-first-century idea.

However, its evidence variable is elapsed time since restorative service, not measured per-cell retention time, temperature-conditioned retention, error telemetry, or learned weak-row classification.

```text
row-age/deadline tracking
    != retention-time profiling
    != weak-row classification
    != modern retention-aware refresh algorithm
```

---

## Philosophical interpretation

### I — apparent quiescence can be an achievement of relocated timing work

The exact technical fact is that an external processor/requester can cease participating in individual refresh events while dedicated timing, counters, address selection, sense/restore circuits, and arbitration continue operating elsewhere.

A bounded interpretation is:

> what looks like `the memory simply remains there` at one interface can be an achieved service condition produced by maintenance work hidden below or beside that interface.

This does not imply that every form of retention is active or continuously maintained; magnetic remanence, Flash charge storage, and mechanical position remain counterexamples elsewhere in the repository.

### I — the system boundary changes the description of autonomy

GTE's patent is the strictest example in this slice. At the CPU/requester boundary, the memory subsystem can initiate refresh without one command per event. At the DRAM-chip boundary, those same devices are externally refreshed by surrounding circuitry.

Thus:

> **before using `automatic`, `self-refresh`, or `autonomous` philosophically, identify the system boundary at which the description is true.**

### I — a retained value and retained evidence about how to keep it are different technical objects

Row-age counters and traversal counters are not user data, yet they organize the work by which user data remain available.

```text
state being preserved
    != state used to decide / distribute preservation work
```

The second can be constitutive of continued availability without being a cultural/logical archive.

---

## Chronology discipline

Dates are intentionally separated by evidentiary role:

```text
GTE US 3,729,722
    filed / priority 1971-09-17
    public patent 1973-04-24
    directly inspected in follow-up
    preferred embodiment: system-level automatic refresh controller

MOS Technology US 3,737,879
    filed 1972-01-05
    public patent 1973-06-05

TI US 4,207,618
    filed / priority 1978-06-26
    public patent 1980-06-10

TI US 4,333,167
    filed 1979-10-05
    public patent 1982-06-01
```

The filing dates matter for patent chronology, but they are **not** treated as public-disclosure dates. The GTE lead now moves the checked public-document floor for automatic recurring dynamic-memory refresh control to April 1973 in this repository, but it does **not** move the floor for verified on-chip recurring refresh control.

---

## Explicit non-claims

This record does **not** claim that:

1. GTE invented dynamic-memory refresh or automatic refresh;
2. `self-initiating refresh` first appeared in April 1973;
3. a patent filing date is the same thing as a public-disclosure date;
4. the Intel 1103 itself contained GTE's refresh clock or row counter;
5. GTE's preferred embodiment is an on-chip self-refresh DRAM;
6. US 3,737,879 invented self-refresh;
7. MOS Technology shipped a commercial product implementing US 3,737,879;
8. Texas Instruments shipped a product implementing the exact circuits of US 4,207,618 or US 4,333,167;
9. US 4,207,618 is a historical predecessor of JEDEC `AUTO REFRESH` in a demonstrated standardization lineage;
10. US 4,333,167 is a historical predecessor of JEDEC `SELF REFRESH` in a demonstrated standardization lineage;
11. `invisible to CPU` means physically zero refresh latency;
12. dynamic cells become static cells when refresh control moves on chip or into dedicated system logic;
13. all refresh state is durable across power loss;
14. the per-row age counters of US 3,737,879 are equivalent to cyclic refresh-address counters;
15. an ordinary read always refreshes every DRAM design in the same way;
16. `voluntary refresh` in the MOS patent is the same historical concept as modern background maintenance;
17. row-age tracking is equivalent to measured retention-time profiling;
18. TI's formal citation of the GTE patent proves implementation inheritance or direct engineering influence;
19. similar control partitions prove a single technical lineage;
20. the inspected patents define later commodity-DRAM standards.

---

## Source-strength ledger

| Claim | Source | Strength | Boundary |
|---|---|---|---|
| GTE self-initiating refresh uses a free-running system-level controller around commercial Intel 1103 chips | US 3,729,722 direct patent transcript | H/P* | patent embodiment, not named GTE product shipment |
| GTE system-level row counter/address gating supplies sequential maintenance rows | US 3,729,722 description/claims | H/P* | disclosed apparatus; not on-chip counter evidence |
| GTE `memory busy` can defer ordinary access during refresh | US 3,729,722 description | H/P* | disclosed service boundary |
| MOS self-refresh design with per-row counters and mandatory refresh | US 3,737,879 direct patent transcript | H/P* | patent disclosure, not product deployment |
| ordinary read/restore or write resets row refresh-age counter | US 3,737,879 direct patent transcript | H/P* | bounded to disclosed architecture |
| voluntary refresh can use an idle interval before mandatory deadline | US 3,737,879 direct patent transcript | H/P* | period patent term; not modern scheduler identity |
| TI 1980 design puts refresh counter/address mux on chip | US 4,207,618 patent text | H/P | patent disclosure |
| TI 1980 design still needs one external refresh signal per event | US 4,207,618 patent text | H/P | no claim about later CBR/JEDEC descent |
| TI 1982 design has internally defined refresh timing | US 4,333,167 claims/text | H/P* | patent disclosure, not named shipped product |
| read/write arriving after refresh start can be delayed until refresh completes | US 4,333,167 detailed description | H/P* | bounded to disclosed implementation |
| refresh authority has separable cadence/enumeration/location/arbitration functions | cross-source mechanism comparison | E | engineering reconstruction |
| GTE vs TI control-location comparison | cross-source comparison | E/A | functional comparison; TI citation only proves document relation |
| AUTO/SELF comparisons | Case-09 later product evidence + these patents | A | functional only, not genealogy |

`H/P*` marks primary patent text inspected through a reliable public transcript/mirror rather than an origin-hosted page-stable USPTO facsimile in this slice.

---

## Related-repository check

`tmzncty/computing-archaeology` was checked again. Its semiconductor-memory overview, [`docs/memory/why-semiconductor-ram-became-a-hierarchy.md`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-semiconductor-ram-became-a-hierarchy.md), already supplies the broad constraint-first account of dynamic cells, density, sensing/restoration, and controller refresh work.

No dedicated GTE-US3729722 control-boundary module was found. Accordingly this record keeps only the **retention-specific control boundary** here. A broader history of early refresh-controller boards, Intel 1103 system design, vendor competition, silicon implementation, cost, product shipment, and influence genealogy belongs primarily in `computing-archaeology` if developed later.

---

## Remaining evidence debt

1. **Closed in the direct-inspection follow-up:** GTE US 3,729,722 has now been inspected. Its preferred embodiment establishes automatic recurring **system-level** refresh around commercial Intel 1103 chips, not earlier on-chip self-refresh. If future work depends on the exact `32 rows / 2 ms` Intel-1103 product contract, contemporaneous Intel manufacturer documentation should be checked separately.
2. locate contemporary product/data-book evidence showing which, if any, named commercial devices implemented the MOS Technology 1973 row-age/deadline architecture;
3. locate named products tied to the TI 1980/1982 patent control partitions rather than inferring implementation from shared corporate authorship;
4. directly page-inspect the 1981 Reese JSSC paper if a future claim depends on its exact arbiter or `ready` timing;
5. keep JEDEC standardization genealogy separate from the earlier patent prior-art chronology.

None of these debts blocks the bounded conclusion of this record.