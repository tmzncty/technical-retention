# Deepening Record — Intel 1975–1983 DRAM Refresh-Control Failure Boundary

## Target case

[`cases/03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md)

## Status

**`bounded deepening complete`**

This record closes one narrow debt left by the existing Case 03 controller work:

> Can period primary documentation show not only that DRAM refresh had separate timer / coverage / arbitration state, but that corruption or misuse of that control state could fail **before** the stored payload itself visibly failed?

For the bounded Intel evidence here, the answer is **yes**.

The September 1975 Intel *8080 Microcomputer Systems User's Manual* already documents the **8222 Dynamic Memory Refresh Controller** as a separate device with an adjustable refresh-request oscillator, internal address multiplexer, refresh timer, and control / I/O circuitry. Intel's 1983 *Memory Components Handbook*, through application note AP-97A, then gives a much more explicit 8202A control decomposition: an internal refresh timer, a seven-bit refresh counter, request synchronization, arbitration against ordinary memory traffic, and a TEST mode that clears the refresh counter. Intel explicitly warns that the resulting interruption of the refresh sequence **may result in data loss**.

The same AP-97A also documents the opposite control failure: an improperly generated external transparent-refresh request can leave the processor waiting indefinitely while the controller repeatedly performs refresh cycles. Thus this slice adds a two-sided boundary:

```text
insufficient / disrupted maintenance sequencing
    -> retention risk

excessive / badly coupled maintenance admission
    -> useful-service liveness risk
```

This is not a general history of DRAM controllers, not a first-invention claim, and not evidence that every 1970s or 1980s DRAM system behaved like these Intel parts.

---

## Why this slice matters

The existing Case 03 evidence already established:

```text
payload charge
    != refresh deadline / phase state
    != refresh coverage position
    != refresh/access arbitration state
```

and later showed that coverage state can migrate from a separate controller into the DRAM package without automatically internalizing refresh cadence.

What remained less directly grounded was the **failure boundary of the maintenance-control state itself**.

The 8202A evidence supplies that boundary directly:

```text
payload still presently readable
    != maintenance-control state correct
    != future deadline satisfaction guaranteed
```

A controller can lose or restart its coverage position before the array has yet crossed a physical retention threshold. The visible payload can therefore remain apparently healthy while the system has already damaged the process that is supposed to keep it healthy.

The transparent-refresh example adds the converse:

```text
many refresh cycles occurring
    != useful service remains live
    != maintenance policy is correct
```

The presence of maintenance work is not itself a correctness certificate.

---

## Historical record

### H/P — Intel documented a dedicated 8222 refresh controller in its September 1975 8080 manual

Intel's September 1975 *8080 Microcomputer Systems User's Manual* contains a product section headed:

> `Schottky Bipolar 8222 — DYNAMIC MEMORY REFRESH CONTROLLER`

The feature list includes:

- `Adjustable Refresh Request Oscillator`;
- support for 8107A / 8107B 4K RAM refresh;
- `Internal Address Multiplexer`;
- support for up to six row-address inputs for a 64 × 64 organization.

The accompanying prose describes the 8222 as a refresh controller for dynamic RAMs and says that it contains an accurate refresh timer, whose frequency is set by an external resistor and capacitor, plus the control and I/O circuitry needed to meet dynamic-RAM refresh requirements.

This is enough to establish a bounded historical point:

```text
DRAM array payload
    != dedicated external refresh-control component
```

by 1975 in Intel's documented product ecosystem.

It is **not** enough to claim that the 8222 was the first dedicated refresh controller, or that its internal control state was identical to the later 8202A.

**Primary anchor:** Intel Corporation, *8080 Microcomputer Systems User's Manual*, September 1975, 8222 section, printed p. 5-99.

Canonical archival scan: <https://www.bitsavers.org/components/intel/MCS80/98-153B_Intel_8080_Microcomputer_Systems_Users_Manual_197509.pdf>

Searchable page transcription used for this bounded text check: <https://manualsdump.com/en/manuals/intel-8080model/110758/165>

Institutional artifact-date corroboration: The Henry Ford, `Manual, "INTEL 8080 Microcomputer Systems User's Manual," 1975`, dated September 1975: <https://www.thehenryford.org/collections/explore/artifact/379548>

### H/P — a named Intel board used the 8222 as the mediator between ordinary RAM requests and refresh requests

Intel's SBC 104/108 board documentation describes an 8222-based dynamic-memory subsystem in which the controller coordinates system-bus RAM-cycle requests with internally generated refresh requests. The board text states that sixty-four refresh cycles cover the memory array and that timing control inside the 8222 keeps refresh-request frequency sufficient for data retention.

The same description distinguishes ordinary system-memory requests from refresh requests and explains that the controller accepts the next request when the memory is no longer busy.

This is useful because it places the 8222 in a real system-control relation rather than leaving it as an isolated datasheet block:

```text
ordinary memory demand
    + refresh demand
    -> shared controller / admission path
    -> one DRAM array
```

The board manual is used only as a bounded implementation witness. This record does not attempt a complete SBC 104/108 chronology.

**Period vendor-manual transcript:** <https://manualzz.com/doc/6680590/intel-sbc-104-108-boards-manual>

### H/P — Intel's 8202A explicitly contains separate refresh timer and refresh-address counter state

Intel's 1983 *Memory Components Handbook* reproduces application note AP-97A, **`Interfacing Dynamic RAMs to iAPX 86/88 Systems Using the Intel 8202A and 8203`**.

AP-97A says the 8202A can receive refresh requests externally, but if no refresh request arrives for roughly 13 microseconds it generates one internally. At the documented rate, one row is refreshed every 15.6 microseconds or sooner, covering 128 rows within 2 ms.

The detailed block description then separates two control functions:

- a **refresh timer** times the interval since the last refresh and generates an internal refresh request when necessary;
- a **seven-bit refresh counter** determines the next row to refresh and advances after each refresh cycle.

This directly grounds:

```text
maintenance cadence / due-state
    != maintenance coverage position
```

The timer is about another refresh opportunity becoming due. The counter is about where the traversal proceeds next.

**Primary anchor:** Intel Corporation, *Memory Components Handbook* (1983), AP-97A, printed pp. 3-119–3-122.

Canonical archive: <https://www.bitsavers.org/components/intel/_dataBooks/1983_Memory_Component_Handbook.pdf>

Searchable transcript used to verify the prose and page sequence: <https://www.studylib.net/doc/25790501/1983-memory-component-handbook>

### H/P — 8202A TEST mode clears the refresh counter and Intel warns that the interrupted sequence may cause data loss

AP-97A documents a TEST cycle requested by asserting the read and write inputs simultaneously. The test cycle clears the refresh-address counter and performs a write cycle.

Intel explicitly warns that TEST should not occur during normal system operation because it interferes with normal RAM refresh.

The command-decoder discussion makes the failure boundary sharper. Intel recommends pull-up resistors on one or both of the read/write inputs because the processor can three-state those signals during RESET or HOLD. The text then states that because TEST mode resets the refresh-address counter, the refresh sequence is interrupted and **data loss may result**.

This is period manufacturer documentation of a maintenance-control failure path:

```text
counter / coverage state disturbed
    -> refresh traversal interrupted or restarted
    -> some rows can receive the wrong effective revisit spacing
    -> retention deadline can be missed
    -> payload loss may follow
```

The source does **not** say that clearing the counter immediately erases DRAM contents. The danger is mediated by subsequent refresh coverage and physical retention time.

### H/P — proper arbitration bounds how long refresh can be postponed by ordinary memory traffic

AP-97A treats arbitration as necessary because a dynamic RAM cannot execute an ordinary read/write cycle and a refresh cycle simultaneously through the same control path.

The 8202A synchronizes memory and refresh requests before arbitration. Intel's description says ordinary memory cycles receive priority in the documented simultaneous-request arrangement, while the arbitration structure ensures that a refresh cycle is delayed by **at most one RAM cycle**.

This gives a concrete historical distinction:

```text
refresh request exists
    != refresh cycle has started

refresh deadline
    depends partly on
bounded admission delay
```

The timer can request maintenance, but an arbiter still determines when the shared resource admits it.

The quoted `at most one RAM cycle` is a property of the documented 8202A arbitration arrangement, not a universal DRAM rule.

### H/P — Intel documents a refresh-overadmission failure that can lock useful service out

AP-97A also warns against a particular transparent-refresh generator that derives an external refresh request from opcode-fetch activity without the correct coupling to the controller's acknowledge state.

Intel explains a failure sequence in which an internally generated refresh overlaps a processor fetch; the controller then sees the ordinary request and external refresh request together, repeatedly honors refresh first, and can enter a condition in which the processor remains in wait states while the 8202A performs refresh cycle after refresh cycle.

Intel calls this **`Refresh Lock-Out`** and supplies a corrected circuit that delays generation of the external refresh request until the opcode fetch is already in progress.

This is the converse of the counter-reset hazard:

```text
refresh work can be abundant
while
useful memory service is unavailable
```

It therefore blocks the shortcut:

```text
more maintenance activity
    = better retention system
```

The historical claim is only about the documented 8202A control interaction and Intel's example circuit.

### H/P — Intel describes the 8203 as an extension of the 8202A architecture

The same 1983 handbook says that the 8203 is an **extension of the 8202A architecture**, retains pin compatibility, and supports 64K dynamic RAMs with modifications to the earlier design.

That wording permits a bounded same-vendor technical relationship:

```text
8202A architecture
    -> extended 8203 architecture
```

This is stronger than a purely functional analogy because Intel itself states the architectural relationship.

It does **not** establish that the 1975 8222 is a direct ancestor of the 8202A. That broader controller genealogy remains open.

**Primary anchor:** Intel, *Memory Components Handbook* (1983), AP-97A, 8203 section following the 8202A discussion.

---

## Engineering reconstruction

### E — maintenance-control failure can precede visible payload failure

The 8202A warning is valuable because it separates two failure times.

At the instant the refresh counter is reset, many cells may still contain perfectly recoverable charge. What has changed first is the controller's representation of future maintenance coverage.

Thus:

```text
present payload correctness
    != future-retention process correctness
```

A system can therefore enter a **retention-at-risk** state before any payload bit is yet observably wrong.

This phrase is a project reconstruction, not Intel terminology.

### E — request generation, admission, execution, and coverage are distinct retention relations

The Intel controller evidence supports a more exact maintenance pipeline:

```text
physical retention obligation
    -> timer / external logic produces refresh request
    -> request is synchronized / retained pending
    -> arbiter admits refresh against ordinary memory traffic
    -> refresh cycle executes
    -> coverage counter advances
    -> required row set is revisited before its deadline
```

Failure can occur at multiple stages:

- no request is generated in time;
- a request is generated but never admitted;
- a refresh cycle executes on the wrong effective coverage sequence;
- refresh occurs so aggressively that useful service is starved;
- the physical cell still fails despite nominal control because its actual retention margin is inadequate.

Therefore:

```text
refresh configured
    != refresh requested
    != refresh admitted
    != refresh executed
    != correct coverage completed
    != payload still recoverable
```

### E — coverage state is not a durable checkpoint merely because losing it matters

The 8202A refresh counter matters to retention, but the documentation treats it as powered operational state. There is no claim that it survives power loss or is checkpointed to nonvolatile storage.

Its persistence horizon is appropriate to the operating regime it serves:

```text
microsecond-scale recurring obligation
    -> regime-local counter state
```

This differs from later scrub cursors, repair maps, or scan checkpoints whose purpose can include surviving restart.

The functional role may be comparable; the persistence contract is not.

### E — a maintenance subsystem has a service-liveness budget as well as a retention budget

The refresh-lockout example shows that a controller can satisfy or even overproduce refresh work while destroying useful-service liveness.

The system therefore has at least two coupled obligations:

```text
retention obligation
    keep rows restored before physical deadlines

service obligation
    allow ordinary reads/writes to make progress
```

Arbitration is not incidental plumbing. It is part of how these obligations coexist on a shared interface.

### E — the 1975→1983 record supports an earlier external-control floor, not a complete genealogy

The 8222 is a direct primary witness that Intel sold/documented a dedicated dynamic-memory refresh controller by 1975. The 8202A/AP-97A material later makes timer/counter/arbitration state and failure modes far more explicit.

A safe historical statement is therefore:

```text
1975: dedicated external refresh-controller role is directly documented
1983: Intel documents a richer 8202A control decomposition and failure boundary
```

What is **not** yet shown is a line-by-line or product-line descent from 8222 to 8202A.

---

## Controlled functional comparison

### A — relation to later durable maintenance checkpoints

Later cases in this repository contain HDFS scan cursors, SSD maintenance telemetry, persistent repair maps, and other control evidence.

The 8202A counter is comparable only at one function:

> it encodes where a recurring maintenance traversal is in its coverage space.

But:

```text
8202A refresh counter
    powered, short-horizon, regime-local control state

restart-surviving scrub cursor
    durable progress evidence across process / machine interruption
```

Calling both `maintenance-control state` is useful. Calling both `checkpoints` would erase an important persistence-horizon difference.

No genealogy is claimed.

### A — relation to Case 83 HDFS BlockScanner admission failures

Case 83 shows a later software system in which a background scanner implementation exists but configuration can disable admission of the maintenance regime. The present DRAM case instead shows a hardware controller whose timer/request/arbitration/coverage state can fail or be miscoupled.

The bounded functional comparison is:

```text
maintenance mechanism exists
    != maintenance obligation is correctly admitted and completed
```

The physical mechanism, timescale, restart semantics, and historical lineages are unrelated.

### A — relation to Case 102 patrol-read scheduling

Case 102 separates maintenance schedule, admission, execution, progress evidence, and repair. The 8202A provides an earlier hardware-level counterexample to collapsing those layers, but again only functionally:

```text
scheduled / requested
    != admitted
    != completed coverage
```

Patrol Read concerns disk defect discovery; DRAM refresh concerns restoration of volatile charge. No historical continuity is implied.

---

## Philosophical / media-theoretical boundary

### I — the present can depend on state about its future maintenance

DRAM is often used to illustrate that persistence requires repeated work. The 8202A deepening makes the temporal structure more precise.

At one instant, the payload can still be present while the controller state responsible for revisiting it later has already become wrong. The failure is first a failure of **organized futurity**: the machinery no longer correctly represents which maintenance action must occur next and when.

That supports a narrow project-level interpretation:

> technical persistence can depend on operational state whose object is not the stored value itself but the **future return** required to keep that value available.

The interpretation remains bounded by the mechanism. The refresh counter is not a cultural memory, not an archive, not Stieglerian tertiary retention by itself, and not Heideggerian `Bestand`.

### I — maintenance is not simply more activity

The refresh-lockout example prevents a romanticized reading in which recurrence itself guarantees persistence.

Too little or wrongly sequenced maintenance threatens the payload; badly coupled excess maintenance can threaten service liveness.

Persistence is therefore not just repetition. It is **timely, correctly addressed, correctly admitted repetition under competing operational constraints**.

That wording is a project interpretation, not Intel's historical vocabulary.

---

## Explicit non-claims

This deepening does **not** claim that:

1. Intel invented the dedicated DRAM refresh controller;
2. the 8222 was the first refresh controller;
3. the 8222 was the first commercial refresh controller;
4. the 1975 8222 had the same internal counter structure as the 8202A;
5. the visible 8222 material proves a nonvolatile refresh counter;
6. the 8222 directly evolved into the 8202A;
7. Intel's 8202A was the first controller with an internal refresh counter;
8. the 8202A test mode always causes payload loss;
9. clearing the refresh counter immediately erases DRAM data;
10. every refresh-counter reset necessarily violates the physical retention deadline;
11. the documented pull-up hazard occurred in every shipping system;
12. processor RESET necessarily destroys DRAM payload;
13. processor HOLD necessarily destroys DRAM payload;
14. a refresh request is identical to a completed refresh cycle;
15. a completed refresh cycle proves correct whole-array coverage;
16. the 8202A's one-RAM-cycle arbitration bound is universal across DRAM controllers;
17. Intel's phrase about memory integrity is a proof against all electrical, device, clock, power, or controller faults;
18. more refresh cycles always improve system correctness;
19. refresh lock-out is a physical DRAM-retention failure;
20. refresh lock-out proves data loss;
21. the 8202A counter is equivalent to a durable scrub checkpoint;
22. the 1975–1983 evidence supplies a complete controller genealogy;
23. the 8202A→8203 relation implies the 8222→8202A relation;
24. Intel practice was universal vendor practice;
25. later CAS-before-RAS or self-refresh designs preserve the same control split;
26. this hardware control problem is historically continuous with HDFS or disk scrubbing;
27. maintenance-control state is philosophically identical to the payload it helps preserve;
28. a controller-state fault is the only way ordinary refresh can fail.

---

## Claim ledger

| Claim | Label | Evidence |
| --- | --- | --- |
| Intel's September 1975 8080 manual documents the 8222 as a `DYNAMIC MEMORY REFRESH CONTROLLER` | H/P | Intel 8080 manual, 8222 section, p. 5-99 |
| The 8222 documentation names an adjustable refresh-request oscillator, internal address multiplexer, and refresh timer/control circuitry | H/P | same |
| Intel board documentation shows the 8222 mediating ordinary RAM requests and internally generated refresh requests | H/P | Intel SBC 104/108 board manual |
| AP-97A documents an 8202A internal refresh timer and seven-bit refresh-address counter | H/P | Intel 1983 *Memory Components Handbook*, AP-97A pp. 3-119–3-122 |
| The 8202A counter advances after refresh cycles and TEST mode clears it | H/P | same |
| Intel warns that TEST-mode counter reset interrupts the refresh sequence and may result in data loss | H/P | same |
| AP-97A recommends pull-ups to reduce inadvertent TEST entry when processor signals are three-stated during RESET/HOLD | H/P | same |
| The documented 8202A arbiter can delay refresh by at most one RAM cycle | H/P | AP-97A arbitration section |
| Intel documents an improperly coupled transparent-refresh circuit that can cause repeated refresh and indefinite processor wait states | H/P | AP-97A `Refresh Lock-Out` section |
| Intel calls the 8203 an extension of the 8202A architecture | H/P | Intel 1983 handbook, 8203 section |
| Maintenance-control failure can precede visible payload failure | E | bounded reconstruction from counter-reset warning + DRAM retention deadline |
| Maintenance request, admission, execution, and coverage are distinct relations | E | bounded reconstruction from timer/counter/arbiter behavior |
| The 8202A refresh counter is a durable restart checkpoint | X | explicitly unsupported |
| The 8222→8202A genealogy is established | X | explicitly unsupported |

---

## Source ledger

### Primary / period manufacturer documentation

1. Intel Corporation, **8080 Microcomputer Systems User's Manual**, September 1975, 8222 section, printed p. 5-99.
   - canonical archival scan: <https://www.bitsavers.org/components/intel/MCS80/98-153B_Intel_8080_Microcomputer_Systems_Users_Manual_197509.pdf>
   - searchable page transcription: <https://manualsdump.com/en/manuals/intel-8080model/110758/165>
   - bounded claims used here: product title; adjustable refresh-request oscillator; internal address multiplexer; refresh timer; dynamic-RAM refresh-control role.
2. Intel Corporation, **SBC 104/108 boards manual**.
   - public manual transcript: <https://manualzz.com/doc/6680590/intel-sbc-104-108-boards-manual>
   - bounded claims used here: 8222 coordinates system RAM requests with internally generated refresh requests; sixty-four refresh cycles cover the array; controller timing maintains refresh frequency.
3. Intel Corporation, **Memory Components Handbook** (1983), application note AP-97A, `Interfacing Dynamic RAMs to iAPX 86/88 Systems Using the Intel 8202A and 8203`, printed pp. 3-117–3-127.
   - canonical archival scan: <https://www.bitsavers.org/components/intel/_dataBooks/1983_Memory_Component_Handbook.pdf>
   - searchable transcript: <https://www.studylib.net/doc/25790501/1983-memory-component-handbook>
   - bounded claims used here: internal/external refresh request; refresh timer; seven-bit refresh counter; TEST-mode counter clear; inadvertent TEST warning; arbitration; one-RAM-cycle refresh-delay bound; refresh lock-out; 8203 as extension of 8202A architecture.

### Institutional artifact provenance

4. The Henry Ford, **Manual, `INTEL 8080 Microcomputer Systems User's Manual, 1975`**, Object ID 95.22.2.3.
   - <https://www.thehenryford.org/collections/explore/artifact/379548>
   - records Intel Corporation as creator and September 1975 as date made.
5. Smithsonian National Museum of American History, **Manuals Relating to the Intel 8080 Microprocessor and Its Applications**, ID 1991.3201.25.
   - <https://americanhistory.si.edu/collections/object/nmah_1401237>
   - collection record lists both July and September 1975 Intel 8080 manual editions.

### Source-quality note

The historical claims above come from Intel-authored period documentation, with museum records used only to corroborate edition/date provenance. During this slice, the searchable text of the relevant Intel manual/handbook sections was checked against archived-document metadata and page numbering, but the public PDF gateway available in this run did not provide a reliable page-image rendering path. This record therefore does **not** claim fresh facsimile-level inspection of every cited page or schematic.

No claim depends on reading a faint wire or logic symbol from a block diagram. The core boundary rests on explicit prose: `refresh timer`, `refresh counter`, TEST-mode clear, interrupted refresh sequence, possible data loss, arbitration behavior, and refresh lock-out.

---

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `8203 refresh controller` found no dedicated reusable packet during this slice. Earlier Case 03 work likewise found no dedicated `2164A` / `8202A` / `8203` treatment.

This repository therefore keeps only the retention-specific seam:

```text
dedicated maintenance controller
    -> request / timer state
    -> coverage-counter state
    -> arbitration / admission
    -> documented control-state failure
    -> retention or service consequence
```

The following remain better work for `computing-archaeology`:

- complete 8222 / 3222 / 8202 / 8202A / 8203 product genealogy;
- first-invention / first-shipment priority;
- Intel versus Mostek / Motorola / TI / AMD controller comparisons;
- process, package, price, board-design, and system-adoption history;
- detailed iAPX 86/88 bus-interface evolution;
- later integration of refresh control into chipsets and memory controllers.

---

## Remaining debt

This bounded slice closes:

- one primary 1975 witness for a dedicated Intel DRAM refresh-controller role;
- one source-level 8202A separation of timer, coverage counter, and arbitration;
- one explicit manufacturer warning that control-state reset can interrupt refresh and may lead to later data loss;
- one opposite control failure in which badly coupled refresh admission can starve useful service;
- the bounded Intel-stated 8202A→8203 architectural relationship.

It intentionally leaves open:

- whether an earlier Intel 3222 or another vendor supplies an earlier primary dedicated-controller floor;
- exact 8222→8202/8202A lineage and design inheritance;
- direct facsimile inspection of all AP-97A diagrams if a later argument depends on circuit topology;
- bench fault injection that intentionally clears or biases refresh coverage while monitoring row-level decay;
- controller clock/power faults and brownout behavior;
- production field-failure records for inadvertent TEST entry or refresh lock-out;
- vendor/standard genealogy for later self-refresh and chipset-integrated refresh control;
- modern TRR/RFM and adaptive-refresh control failures, which are distinct later cases.

The case should remain **`grounded`**. This evidence deepens the controller-failure seam but does not justify a maturity promotion or a claim of complete DRAM-refresh genealogy.
