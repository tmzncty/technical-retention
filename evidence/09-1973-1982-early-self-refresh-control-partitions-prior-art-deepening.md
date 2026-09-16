# Evidence 09 — 1973–1982 early self-refresh control partitions prior-art deepening

**Status:** `bounded deepening complete`

**Parent case:** [`../cases/09-dram-cbr-refresh-address-internalization.md`](../cases/09-dram-cbr-refresh-address-internalization.md)

**Earlier adjacent record:** [`09-1981-1983-autonomous-self-refresh-prior-art-deepening.md`](09-1981-1983-autonomous-self-refresh-prior-art-deepening.md)

**Bounded question:** how far before the already-grounded 1981–1983 DRAM self-refresh literature can public technical evidence establish internal refresh scheduling, internal row selection, and access/refresh arbitration—and what does that do to Case 09's chronology without turning a patent chain into an invention-priority genealogy?

This record is intentionally narrow. It does **not** attempt a complete history of dynamic-memory refresh, a first-invention claim, a shipment chronology, a JEDEC genealogy, or a direct descent argument from 1970s patents to later commodity DRAM. It deepens only the prior-art boundary relevant to retention-control authority.

---

## Result in one sentence

By public patent publication, **1973** already supplies a MOS-memory self-refresh design in which row-specific deadline state can force refresh and block access, while **1980** and **1982** Texas Instruments patents cleanly separate two other partitions—external refresh cadence with on-chip row enumeration, and internally timed on-chip refresh whose occasional overlap is absorbed into access latency.

Therefore the Case-09 history can no longer use `1981` as even a conservative public-document floor for the existence of internally initiated refresh logic. The safer statement is:

```text
1973 public patent witness
    self-refresh / deadline-tracked mandatory refresh already exists

1980 public TI patent witness
    external refresh command cadence
    + internal row enumeration

1982 public TI patent witness
    internal refresh cadence
    + internal row enumeration
    + refresh/access arbitration
```

The 1981 Reese paper remains valuable as a peer-reviewed DRAM publication witness; it is no longer the earliest public witness in this repository for the broader control partition.

---

## Sources and evidence boundary

### 1. MOS Technology, US 3,737,879, `Self-refreshing memory`

- Inventors: Richard M. Greene, Donald L. McLaughlin, John O. Paivinen.
- Assignee: MOS Technology, Inc.
- Filed: **5 January 1972**.
- Granted / public patent date: **5 June 1973**.
- Application: `05/215,506`.
- Public transcript used for direct text inspection: <https://uspto.report/patent/grant/3737879>
- Patent corpus mirror: <https://patents.google.com/patent/US3737879A/en>

The public transcript preserves the patent abstract and detailed description. The abstract states that a different counter is associated with each row; an ordinary read-and-restore or write resets that row's counter; if a row goes without such service for the permitted maximum interval, the counter initiates a **mandatory refresh** and temporarily inhibits access. An optional program-sensing path can also use otherwise idle intervals for **voluntary refresh** of rows nearest to needing mandatory service.

The detailed description explains the physical reason: MOS storage units retain charge on capacitors, that charge leaks, and rows not read/restored, written, or otherwise refreshed within the allowed interval must be refreshed. It explicitly contrasts the proposal with prior systems that periodically halted normal operation and refreshed every row.

This is public patent evidence. It is **not** a demonstrated commercial MOS Technology DRAM product and does not establish how widely the architecture was implemented.

### 2. Texas Instruments, US 4,207,618, `On-chip refresh for dynamic memory`

- Inventors: Lionel S. White, Jr.; G. R. Mohan Rao.
- Assignee: Texas Instruments Inc.
- Filed / priority: **26 June 1978**.
- Published / granted: **10 June 1980**.
- Public text: <https://patents.google.com/patent/US4207618A/en>

The patent places a refresh-address counter and address multiplexing on the dynamic-memory chip. Its summary says the only external signal needed is a **refresh command**; that command makes the on-chip mechanism select the row defined by the internal counter and then advance the counter.

The detailed embodiment states that the row address for refresh is internally generated and that the sequential counter advances for each externally supplied `RF` refresh signal. The rows still must be traversed within the maximum refresh interval.

This is a particularly clean witness for:

```text
refresh-address authority on chip
    != recurring refresh-cadence authority on chip
```

The same patent cites an earlier GTE `US3729722A`, titled `Dynamic mode integrated circuit memory with self-initiating refresh means` (priority 1971-09-17; publication 1973-04-24). That citation is recorded below as a **future direct-inspection lead**, not as a mechanism claim in this record because its full primary text was not directly inspected here.

### 3. Texas Instruments, US 4,333,167, `Dynamic memory with on-chip refresh invisible to CPU`

- Inventor: David J. McElroy.
- Assignee: Texas Instruments Incorporated.
- Filed: **5 October 1979**.
- Granted / public patent date: **1 June 1982**.
- Public transcript: <https://patents.justia.com/patent/4333167>

This patent moves the recurring trigger itself on chip. Its claims describe a refresh address counter and a refresh-signal generator within the semiconductor body, with refresh signals produced at **regular internally defined intervals**.

The implementation uses an on-chip refresh clock generator, an internal sequential row counter, address multiplexing, sense/refresh amplifiers, and control logic. It also specifies the collision rule:

- if a read begins after a refresh has started, the refresh completes and the read then executes;
- if a write begins after a refresh has started, address/data are latched, refresh completes, and the write then proceeds;
- the published access/write timing budget includes the possible refresh wait.

For the illustrative 256-row / 4 ms case, the patent gives an internal-refresh interval of roughly 15 microseconds and an example refresh/access duration around 0.3 microseconds. Those example numbers are not promoted here into universal DRAM constants.

Again, this is patent disclosure, not a named shipped DRAM-product specification.

---

## Historical record

### H/P — public self-refresh evidence reaches 1973, not merely 1981

US 3,737,879 is publicly dated June 1973 and explicitly calls itself a `self-refreshing memory` system. Its logic is not merely a free-running global sweep. It associates refresh-age state with rows and lets an expired row counter trigger mandatory refresh.

The bounded historical correction is:

```text
public technical self-refresh disclosure
    by 1973
        includes deadline-tracked row refresh
        + forced refresh admission
        + access inhibition during mandatory refresh
```

This does **not** establish the first self-refresh invention. The patent itself sits within a broader early-1970s dynamic-memory refresh field, and the current slice did not audit all earlier patents, conference papers, or products.

### H/P — ordinary accesses can discharge a later refresh obligation in the 1973 design

In US 3,737,879, a row's counter is reset when that row is accessed for writing or for reading followed by restore. Thus an ordinary service operation and a maintenance operation can both satisfy the same underlying retention need.

The period design therefore already distinguishes:

```text
maintenance obligation exists
    != a dedicated refresh command must necessarily perform the next restoration
```

A recent ordinary access may make a separate refresh unnecessary for that row until its timer ages again.

### H/P — the 1973 design contains both mandatory and opportunistic refresh

The patent's `mandatory` path waits until a row reaches its maximum permitted no-refresh interval, then inhibits access and refreshes the row.

Its optional `voluntary` path instead detects a sufficiently long pause in memory demand and refreshes one or more rows closest to requiring mandatory refresh.

This establishes, in period vocabulary, a distinction between:

```text
deadline-forced maintenance
    and
opportunistic early maintenance
```

without importing modern scheduler terminology into the historical layer.

### H/P — TI's 1980 patent internalizes enumeration but keeps cadence external

US 4,207,618 places the row counter and row-address source inside the memory chip, while requiring an externally supplied refresh signal for each refresh event.

The key product-independent patent relation is:

```text
external system
    decides that a refresh event occurs now

memory device
    chooses the refresh row internally
    executes refresh
    advances the internal row counter
```

This is directly relevant to the later Case-09 CBR/AUTO REFRESH comparison, but the 1980 patent is not itself a claim about the later JEDEC command vocabulary.

### H/P — TI's 1982 patent internalizes cadence and arbitrates collisions

US 4,333,167 adds an internal refresh clock generator. Its row counter advances from internally generated refresh timing rather than from one external refresh request per cycle.

The patent does not make refresh physically disappear. Instead, it specifies what happens when maintenance and service contend for the same array:

```text
refresh begins
    -> refresh completes
    -> queued/latching normal access proceeds
```

The title's `invisible to CPU` language therefore must be read with the patent's own timing contract. Visibility is reduced at the control-interface level; occasional access latency can still include the maintenance interval.

### H/P — `static-like` service does not mean static-cell physics

Both TI patents explicitly motivate their designs by the cost/board-space burden of conventional external dynamic-memory refresh and compare the interface objective with static RAM convenience.

The retained data nevertheless remain dynamic cell charge requiring periodic restoration. The architectural goal is to move or hide refresh-control work, not to turn a one-transistor dynamic cell into a six-transistor static latch.

---

## Retained-state decomposition

The early patents make it possible to distinguish several state classes without relying on later SDRAM terminology.

### 1. Payload state

The user-visible bit value is embodied in dynamic MOS cell charge and is subject to leakage.

### 2. Refresh-age / deadline evidence

In US 3,737,879, row counters encode whether a row is approaching or has reached the maximum allowed interval without a restorative event.

This is maintenance-control state, not application payload.

### 3. Refresh-coverage position

In US 4,207,618 and US 4,333,167, a sequential counter identifies which row will be refreshed next.

This is not the same relation as the 1973 per-row age counters. Both can influence which row receives maintenance, but they encode different facts.

### 4. Cadence authority

The 1980 TI design expects a repeated external refresh signal. The 1982 TI design includes an internal refresh clock generator.

### 5. Address-source authority

During refresh, internal refresh addressing takes authority over the row decoder instead of the ordinary external row address.

### 6. Access/maintenance arbitration state

The 1973 patent can inhibit access during mandatory refresh. The 1982 patent latches or delays a normal request when refresh is already underway.

These are all control relations layered around the same underlying dynamic-retention problem.

---

## Engineering reconstruction

### E — `when`, `which row`, and `who waits` are independently movable control functions

The three patents expose at least three separable questions:

```text
when must maintenance occur?
which row should receive it?
what happens if service arrives at the same time?
```

US 3,737,879 uses row-age/deadline state to decide when a particular row has become mandatory and can exploit idle periods for earlier work.

US 4,207,618 moves row enumeration on chip while leaving repeated event timing outside.

US 4,333,167 moves recurring event timing on chip as well and defines a collision/latency policy.

Therefore:

```text
internal row enumeration
    != internal deadline/cadence authority
    != access arbitration policy
```

### E — refresh can be hidden by changing the observer's contract, not by eliminating maintenance

`Invisible to CPU` in the 1982 patent is best reconstructed as interface abstraction. A request can be accepted under a timing contract that already budgets for the possibility that refresh must finish first.

So:

```text
host does not issue refresh commands
    != refresh does no work

host sees ordinary read/write interface
    != internal array is continuously available

maintenance latency included in service contract
    != maintenance latency is physically zero
```

This is a retention-specific example of hidden infrastructure.

### E — event-triggered restoration and deadline-triggered restoration can coexist

The 1973 design treats read-and-restore, writes, mandatory refresh, and voluntary refresh as different events that can all affect a row's future refresh need.

A useful reconstruction is:

```text
row restored by ordinary access
    -> age evidence resets
    -> dedicated refresh can be deferred

row not otherwise restored
    -> age evidence advances
    -> mandatory refresh eventually becomes necessary
```

This sharpens the repository's distinction between access-triggered restoration and deadline-driven maintenance: the two are different trigger classes but can interact in one system.

### E — selective deadline state is not the same thing as a cyclic refresh pointer

US 3,737,879's per-row counters represent how recently each row has been serviced. A sequential refresh counter represents a traversal position.

Thus:

```text
row-age evidence
    != next-row pointer

proof that row X is due
    != proof that traversal pointer currently names X
```

Both are maintenance-control state, but with different semantics and failure consequences.

### E — internalization relocates responsibility, not the retention deadline itself

Across the TI contrast, the physical requirement remains that every required row be restored within its allowed interval. What changes is the control boundary responsible for satisfying that requirement.

Therefore:

> **a retention obligation may remain constant while the authority that schedules, enumerates, and arbitrates its maintenance migrates across a package or system boundary.**

---

## Functional comparisons

The following comparisons are **functional analogies only**. They do not assert direct historical descent.

### A — 1980 TI patent vs later AUTO/CBR-style control partition

US 4,207,618 functionally resembles the later Case-09 partition in which the device owns refresh-row enumeration but the outside system still supplies recurring refresh events.

```text
external recurrence
    + internal row enumeration
```

The electrical interface, command encoding, device generation, and standards context differ. `Functional resemblance != JEDEC genealogy`.

### A — 1982 TI patent vs later SELF REFRESH

US 4,333,167 functionally resembles later self-refresh in one narrow respect: recurring refresh timing and row enumeration are both internal.

But the patent describes a memory designed to admit ordinary requests around internal refresh events, whereas later SDRAM SELF REFRESH is a mode with its own entry/exit and service restrictions.

Thus:

```text
internal recurrence + internal enumeration
    != identical self-refresh mode semantics
```

### A — 1973 deadline-tracked rows vs modern retention-aware refresh research

US 3,737,879 is a useful historical counterexample to any broad novelty statement that `refresh only what appears to need refresh` is intrinsically a twenty-first-century idea.

However, its evidence variable is **elapsed time since restorative service**, not measured per-cell retention time, temperature-conditioned retention, error telemetry, or learned weak-row classification.

Therefore:

```text
row-age/deadline tracking
    != retention-time profiling
    != weak-row classification
    != modern retention-aware refresh algorithm
```

---

## Philosophical interpretation

### I — apparent quiescence can be an achievement of relocated timing work

The exact technical fact is that an external processor can cease participating in individual refresh events while internal counters, clocks, address selection, sense/restore circuits, and arbitration continue operating.

A bounded interpretation is:

> what looks like `the memory simply remains there` at one interface can be an achieved service condition produced by maintenance work hidden below that interface.

This does not imply that every form of retention is active or continuously maintained; magnetic remanence, Flash charge storage, and mechanical position remain counterexamples elsewhere in the repository.

### I — a retained value and retained evidence about how to keep it are different technical objects

The 1973 row-age counters are not user data, yet losing or corrupting their relation could change whether the system knows a row has become due for restoration.

That supports a narrow conceptual distinction:

```text
state being preserved
    != state used to decide preservation work
```

The second can be constitutive of continued availability without being the cultural/logical payload itself.

---

## Chronology discipline

Dates in this record are intentionally separated by evidentiary role.

```text
US 3,737,879
    filed 1972-01-05
    public patent 1973-06-05

US 4,207,618
    filed / priority 1978-06-26
    public patent 1980-06-10

US 4,333,167
    filed 1979-10-05
    public patent 1982-06-01
```

The filing dates matter for patent chronology, but they are **not** treated as public-disclosure dates. The public-document floors used for the repository are 1973, 1980, and 1982 respectively unless a separate earlier public source is directly established.

The 1981 Reese JSSC article therefore remains an important peer-reviewed public source even though the broader self-refresh/control ideas have earlier patent-publication witnesses.

---

## Explicit non-claims

This record does **not** claim that:

1. US 3,737,879 invented self-refresh;
2. 1973 is the earliest dynamic-memory self-refresh publication;
3. a patent filing date is the same thing as a public disclosure date;
4. MOS Technology shipped a commercial product implementing US 3,737,879;
5. Texas Instruments shipped a product implementing the exact circuits of US 4,207,618 or US 4,333,167;
6. US 4,207,618 is a historical predecessor of JEDEC `AUTO REFRESH` in a demonstrated standardization lineage;
7. US 4,333,167 is a historical predecessor of JEDEC `SELF REFRESH` in a demonstrated standardization lineage;
8. `invisible to CPU` means physically zero refresh latency;
9. dynamic cells become static cells when refresh control moves on chip;
10. all refresh state is durable across power loss;
11. the per-row age counters of US 3,737,879 are equivalent to later refresh-address counters;
12. an ordinary read always refreshes every DRAM design in the same way;
13. `voluntary refresh` in the 1973 patent is the same historical concept as modern background maintenance;
14. row-age tracking is equivalent to measured retention-time profiling;
15. the earlier GTE US 3,729,722 mechanism has been directly verified here merely because later patents cite it;
16. patent citation proves implementation inheritance;
17. similar control partitions prove a single technical lineage;
18. the inspected patents define later commodity-DRAM standards.

---

## Source-strength ledger

| Claim | Source | Strength | Boundary |
|---|---|---|---|
| MOS self-refresh design with per-row counters and mandatory refresh | US 3,737,879 direct patent transcript | H/P* | patent disclosure, not product deployment |
| ordinary read/restore or write resets row refresh-age counter | US 3,737,879 direct patent transcript | H/P* | bounded to disclosed architecture |
| voluntary refresh can use an idle interval before mandatory deadline | US 3,737,879 direct patent transcript | H/P* | period patent term; not modern scheduler identity |
| TI 1980 design puts refresh counter/address mux on chip | US 4,207,618 patent text | H/P | patent disclosure |
| TI 1980 design still needs one external refresh signal per event | US 4,207,618 patent text | H/P | no claim about later CBR/JEDEC descent |
| TI 1982 design has internally defined refresh timing | US 4,333,167 claims/text | H/P* | patent disclosure, not named shipped product |
| read/write arriving after refresh start can be delayed until refresh completes | US 4,333,167 detailed description | H/P* | bounded to disclosed implementation |
| refresh authority has separable cadence/enumeration/arbitration functions | cross-source mechanism comparison | E | engineering reconstruction |
| AUTO/SELF comparisons | Case-09 later product evidence + these patents | A | functional only, not genealogy |

`H/P*` marks primary patent text inspected through a reliable public transcript/mirror rather than an origin-hosted page-stable USPTO facsimile in this slice.

---

## Related-repository check

`tmzncty/computing-archaeology` was searched for the exact patent number `3737879` and for the earlier self-refresh topic. No dedicated module matching this bounded slice was found.

Accordingly this record keeps only the **retention-specific control boundary** here. A broader history of early MOS/DRAM refresh circuits, vendor competition, silicon implementation, cost, board-space tradeoffs, product shipment, and influence genealogy belongs primarily in `computing-archaeology` if developed later.

---

## Remaining evidence debt

The next useful work is now much narrower:

1. directly inspect the full primary text/facsimile of **GTE US 3,729,722**, `Dynamic mode integrated circuit memory with self-initiating refresh means` (priority 1971-09-17; publication 1973-04-24), before using it for mechanism claims;
2. locate contemporary product/data-book evidence showing which, if any, named commercial devices implemented the 1973 MOS Technology architecture;
3. locate named products tied to the TI 1980/1982 patent control partitions rather than inferring implementation from shared corporate authorship;
4. directly page-inspect the 1981 Reese JSSC paper if a future claim depends on its exact arbiter or `ready` timing;
5. keep JEDEC standardization genealogy separate from the earlier patent prior-art chronology.

None of these debts blocks the bounded conclusion of this record.
