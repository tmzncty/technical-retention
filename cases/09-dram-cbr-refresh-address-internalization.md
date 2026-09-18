# CAS-before-RAS DRAM Refresh: Moving Refresh Addressing On-Chip

## Status

**`grounded`** — bounded to an early-1970s system-level automatic-refresh witness around commercial 1103 DRAMs, period 1103 product refresh contracts, Texas Instruments' TMS4164 contrast, TMS4256/TMS4257 refresh behavior, TI's 1984-filed on-chip refresh-counter design, a 1973–1982 public-patent prior-art deepening, an early-1980s autonomous-self-refresh publication deepening, and a late-1999 Micron SDRAM product comparison separating externally repeated AUTO REFRESH from device-clocked SELF REFRESH.

Grounding record: [`../evidence/09-ti-cbr-refresh-address-grounding.md`](../evidence/09-ti-cbr-refresh-address-grounding.md).

Deepening record: [`../evidence/09-dram-refresh-counter-initialization-test-deepening.md`](../evidence/09-dram-refresh-counter-initialization-test-deepening.md).

Early public-patent prior-art deepening: [`../evidence/09-1973-1982-early-self-refresh-control-partitions-prior-art-deepening.md`](../evidence/09-1973-1982-early-self-refresh-control-partitions-prior-art-deepening.md).

GTE system-boundary deepening: [`../evidence/09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md`](../evidence/09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md).

1103 product-contract deepening: [`../evidence/09-1972-1975-1103-refresh-product-contract-deepening.md`](../evidence/09-1972-1975-1103-refresh-product-contract-deepening.md).

Early autonomous-self-refresh publication deepening: [`../evidence/09-1981-1983-autonomous-self-refresh-prior-art-deepening.md`](../evidence/09-1981-1983-autonomous-self-refresh-prior-art-deepening.md).

SDRAM control-boundary deepening: [`../evidence/09-micron-1999-sdram-auto-vs-self-refresh-deepening.md`](../evidence/09-micron-1999-sdram-auto-vs-self-refresh-deepening.md).

---

## Scope

- **Object / system:** a bounded comparison of DRAM refresh-control partitions: externally enumerated refresh, a memory-system-level self-initiating refresh controller around commercial 1103 devices, internally tracked/self-initiated refresh in early public patent literature, externally triggered refresh with an on-chip refresh-address counter, internally clocked refresh with on-chip row enumeration and access arbitration, CAS-before-RAS refresh, and later SELF REFRESH; a late-1999 SDRAM product is retained as a clean AUTO REFRESH / SELF REFRESH interface comparison.
- **Date range:** 1972–1986 for the central early product/control evidence, while preserving the distinction between the GTE patent's 1971 filing date and its April-1973 public patent date; a 1984-filed TI patent supplies mechanism-level CBR design detail. A January 1988 revision of the TMS4256/TMS4257 sheet was directly inspected only as a page-stable facsimile witness to the same documented device-family behavior. Micron's November-1999 64 Mb SDRAM documentation is used only as a later product-level successor witness for AUTO REFRESH versus SELF REFRESH control partition.
- **Primary comparison:** GTE's April-1973 public patent supplies automatic recurring refresh at the memory-system boundary around commercial Intel 1103 chips; Signetics 1972 and Intel 1975 product documents independently ground the 1103-family coverage/deadline contract; MOS Technology's June-1973 public self-refresh patent supplies row-age/deadline-triggered mandatory and opportunistic refresh; TI's 1980 public patent supplies external cadence plus internal row enumeration; TI's 1982 public patent supplies internal cadence plus internal row enumeration and access arbitration; TMS4164/TMS4256/TMS4257 and the 1984-filed TI CBR patent supply the named commercial/product-family contrast; Reese et al. 1981 and Yamada et al. 1983 remain peer-reviewed/publication witnesses for early autonomous self-refresh; the later Micron SDRAM comparison supplies a directly documented synchronous-interface contrast between repeated AUTO REFRESH commands and SELF REFRESH recurrence after mode entry.
- **Question:** what changes when the DRAM still has a periodic retention deadline but row enumeration, recurrence timing, deadline evidence, mode control, access arbitration, and the system boundary that owns them can be placed under different authorities?

This is **not** a general history of DRAM evolution. The early patent and publication material is a bounded prior-art correction, not an invention-priority, product-shipment, or direct-influence genealogy. The 1103 material is a bounded product-contract comparison, not a second-source genealogy. The SDRAM material is a bounded AUTO REFRESH / SELF REFRESH control comparison, not a JEDEC genealogy or a full SDRAM history. DDR per-bank refresh, temperature-compensated refresh, retention-aware refresh research, and broad controller/test-mode history remain outside this case unless needed for a later retention comparison.

Case 03 already grounds the physical reason dynamic semiconductor state needs periodic reconstruction. This case starts one layer higher:

> **Does moving refresh-row enumeration, deadline tracking, or recurring refresh cadence across system/package boundaries change the retention mechanism, the maintenance obligation, or the location and authority of maintenance control?**

---

## Why this is a separate retention case

The simplest summary of Case 03 is:

```text
leaky electrical state
    -> finite retention interval
    -> periodic reconstruction before a deadline
```

That account is correct but leaves `refresh machinery` too monolithic. The source set lets us decompose it:

```text
refresh deadline
refresh-age / deadline evidence
refresh-cycle scheduling / cadence authority
refresh trigger / mode entry
next-row enumeration
row selection / address-source authority
access-vs-refresh arbitration
sense / restoration
system/package boundary that owns each function
```

The early prior-art evidence adds an important historical correction: these functions did not migrate on-chip in one simple linear order. GTE's April-1973 public patent already describes self-initiating recurring refresh at the **memory-system** boundary while keeping the free-running clock, pulse generator, row counter, address gating, and `memory busy` relation outside the commercial Intel 1103 chips in its preferred embodiment. MOS Technology's June-1973 public patent instead tracks row-specific time-to-refresh and can force maintenance. Public TI patents in 1980 and 1982 then provide a clean contrast between external cadence with internal row enumeration and internally timed refresh with internal enumeration plus access arbitration. The 1981–1983 publication evidence remains important as a peer-reviewed/contemporary DRAM witness rather than the earliest public-document floor for the broader idea.

The 1103 product evidence adds another separation: a device can specify **how much restorative coverage must occur by when** without thereby specifying one unique scheduler, counter placement, or arbitration design. GTE's 16 kHz worked cadence is one system implementation derived from the 1103's 32-row / 2 ms requirement, not the device contract itself.

The Micron SDRAM successor evidence then provides a later same-product distinction:

```text
maintenance mode entry / exit
    != recurring refresh-cadence authority
```

The case matters because these functions need not live at the same layer or under the same authority, and historically more than one partition coexisted.

---

## Historical vocabulary

The period sources use:

- `refresh`;
- `self-initiating refresh` in GTE US3729722A;
- `self-refreshing memory`;
- `mandatory refresh` and `voluntary refresh` in US3737879;
- `on-chip refresh` in US4207618;
- refresh `invisible to CPU` in US4333167;
- `RAS-only refresh`;
- `CAS-before-RAS refresh`;
- `hidden refresh`;
- `refresh address`;
- `refresh counter`;
- `self-refresh` in early-1980s IEEE/Japanese DRAM work;
- `auto/self refresh` in the 1983 Yamada et al. publication;
- `self refresh circuitry` in the title and description of TI's US4653030A;
- `AUTO REFRESH` and `SELF REFRESH` in Micron's 1999 SDRAM documentation.

### Terminology warning

`Self refresh` and adjacent autonomy language cannot be treated as timeless circuit categories whose mechanism follows automatically from the phrase.

GTE's 1973 `self-initiating refresh` is automatic relative to the processor/requester, but the preferred embodiment places its free-running clock, pulse generator, row counter, gating, and busy logic at the memory-system boundary around commercial DRAM chips. It is therefore **not** evidence that the Intel 1103 itself contains chip-local self-refresh machinery.

US3737879's June-1973 public patent uses `self-refreshing memory` for a row-age/deadline-driven design with mandatory refresh and optional opportunistic/voluntary refresh. Reese et al. 1981 is indexed as describing self-refresh with an on-chip timer, arbiter, and refresh counter. Yamada et al. 1983 concerns a DRAM with auto/self-refresh functions, and later Mitsubishi prior-art reconstructions attribute an internal timer + refresh-counter architecture to that work.

By contrast, `self refresh circuitry` in TI's 1984-filed patent title does **not** mean that the disclosed CBR counter supplies recurring cadence: the patent explicitly says the processor or memory controller external to the memory device controls how often the CAS-before-RAS sequence occurs.

Micron's 1999 `SELF REFRESH` documents yet another concrete interface contract: after explicit mode entry, the SDRAM supplies internal clocking and performs recurring refresh cycles while the required mode condition remains active.

Therefore:

> **same or similar historical autonomy vocabulary ≠ same command semantics, physical integration boundary, interface contract, deadline representation, or distribution of retention work.**

The period terms are historical record. Any cross-period taxonomy is functional comparison only.

---

## Historical record

### H/P — TMS4256/TMS4257 keep the ordinary DRAM deadline

Texas Instruments' 1986 *MOS Memory Data Book* carries a TMS4256/TMS4257 sheet with the revision header `MAY 1983—REVISED NOVEMBER 1985`. The devices are 262,144 × 1 dynamic RAMs and specify a maximum refresh period of 4 ms.

The refresh section states that refresh can be accomplished by stroking each of 256 rows. Ordinary access refreshes the selected row, and RAS-only refresh is also available.

This keeps the core Case-03 relation intact:

```text
state still decays
    -> rows still need reconstruction
    -> a deadline still exists
```

### H/P — CAS-before-RAS changes where the refresh row comes from

The same manufacturer documentation defines CAS-before-RAS refresh by bringing CAS low before RAS. During that mode:

- the external address is ignored;
- the refresh address is generated internally.

This is the key historical fact for the central CBR slice. The physical refresh obligation did not disappear; the chip acquired machinery that can choose the row to refresh without the system presenting that row through the ordinary address pins.

### H/P — Hidden refresh changes interface visibility

The TMS4256/TMS4257 sheet also defines `hidden refresh`. After a read, CAS can remain low while RAS is cycled through refresh behavior, allowing valid output data to remain at the output pin for the documented interval. External address inputs are again ignored during the hidden-refresh cycles.

Thus a refresh operation may occur while one visible interface condition — the output value — remains stable.

### H/P — TI's patent exposes the counter/address-path mechanism

US4653030A, filed by TI inventors Tadashi Tachibana, Chitranjan N. Reddy, and Ngai H. Hong on 31 August 1984, describes a multiplexed-address dynamic memory with an on-chip refresh counter activated by CAS-before-RAS sequencing.

The patent describes:

- ordinary row-address input buffers;
- a set of refresh-counter stages;
- selection between the external-address path and the refresh-counter path;
- use of the internally generated row address during a refresh-only cycle;
- progression of the counter across successive refresh requests.

The patent also supplies a rare named commercial contrast: a `64K × 1` device of the same general type, **without the refresh counter of the invention**, was commercially available as the `TMS4164`.

This does not prove a simple genealogy `TMS4164 -> patent -> TMS4256`. It does establish, in TI's own period design vocabulary, the exact architectural distinction needed for the retention comparison: **external row-address supply versus on-chip refresh-row generation**.

### H/P — the bounded TI counter does not schedule itself

The most important limit is explicit in the patent. For a 4 ms maximum refresh period and 256 rows, it says the CAS-before-RAS sequence should occur on average every 15.6 µs and that this is controlled by the processor or memory controller external to the memory device.

So the period primary source itself blocks the shortcut:

```text
on-chip refresh counter
    !=
fully autonomous refresh scheduler
```

---

## 1971–1982 early refresh-control prior-art deepening

Detailed prior-art record: [`../evidence/09-1973-1982-early-self-refresh-control-partitions-prior-art-deepening.md`](../evidence/09-1973-1982-early-self-refresh-control-partitions-prior-art-deepening.md).

GTE direct-inspection record: [`../evidence/09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md`](../evidence/09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md).

1103 product-contract record: [`../evidence/09-1972-1975-1103-refresh-product-contract-deepening.md`](../evidence/09-1972-1975-1103-refresh-product-contract-deepening.md).

### H/P — GTE's April-1973 `self-initiating refresh` is automatic at the memory-system boundary

GTE Automatic Electric Laboratories' US3729722A, filed 17 September 1971 and granted/published 24 April 1973, describes a dynamic-memory system whose refresh circuitry contains a free-running clock, refresh pulse generator, row-address counter, address gating, and a `memory busy` relation.

Its preferred embodiment explicitly uses commercially available Intel 1103 MOS memory chips and describes the refresh apparatus around those chips. For the worked 1103 geometry it uses 32 rows, a stated two-millisecond refresh requirement, and a 16 kHz clock so one row is selected every 62.5 microseconds. An external memory access attempted during refresh is deferred until the refresh cycle completes.

The historical boundary is therefore:

```text
self-initiating at memory-system boundary
    !=
self-initiating at DRAM-package boundary
```

This closes the earlier discovery-only status of US3729722A. It does not establish invention priority, shipment of GTE's controller, or a direct implementation genealogy to later on-chip refresh.

### H/P — period 1103 product documents independently ground the coverage/deadline contract

Signetics' 1972 MOS handbook documents its 1103 as a 1024-word × 1-bit dynamic memory in which refreshing all 1,024 bits is accomplished in 32 read cycles and is required every two milliseconds for the documented 0–70 °C ambient range. Intel's own 1975 data catalog independently gives the same 32-read-cycle / two-millisecond relation for the Intel 1103.

The same Intel catalog supplies a useful anti-generalization: the faster 1103A-1 still uses 32 read cycles for full coverage but specifies a one-millisecond refresh period. Thus:

```text
same coverage geometry
    !=
one invariant refresh deadline across related variants
```

The product contract says how much coverage is required by when. GTE's free-running clock, counter, gating, and service deferral are one specific system implementation for meeting that obligation.

### H/P* — MOS Technology's June-1973 public patent describes row-age/deadline-driven self-refresh

MOS Technology's US3737879, filed 5 January 1972 and granted/published 5 June 1973, is titled `Self-refreshing memory`.

Its disclosed architecture associates refresh-age state with each row. A read-and-restore or write resets the corresponding row counter; if a row reaches the permitted maximum interval without being restored, its counter causes a mandatory refresh and temporarily inhibits access. An optional program-sensing path can instead use an idle interval to refresh rows approaching the mandatory deadline.

This supplies a different early control partition:

```text
by public patent in June 1973
    row-specific maintenance-age evidence
    + mandatory deadline-triggered refresh
    + optional opportunistic early refresh
    + access admission changes during forced maintenance
```

It does not establish invention priority or product deployment.

### H/P — TI's 1980 public patent cleanly separates cadence from enumeration

US4207618A, filed 26 June 1978 and published/granted 10 June 1980, puts the refresh-address counter and address multiplexing on the dynamic-memory chip. Its own summary says the only external signal needed is a refresh command; that request selects the row defined by the internal counter and advances the counter.

So:

```text
external refresh-event cadence
    + internal refresh-row enumeration
```

was already directly described in public TI patent text before the later CBR patent used elsewhere in this case.

### H/P* — TI's 1982 public patent internalizes cadence and defines collision handling

US4333167, filed 5 October 1979 and granted/published 1 June 1982, describes an internal refresh clock generator, internal refresh address counter, and address-selection logic. Its claims specify refresh signals at regular internally defined intervals.

The detailed description also makes the service boundary explicit: if a read or write begins after refresh has started, the refresh finishes first and the normal access then proceeds; the published access/write timing budget includes that possible wait.

Therefore the title phrase `refresh invisible to CPU` cannot safely be read as `refresh takes no time`. The bounded relation is:

```text
host need not schedule each refresh
    != physical refresh disappears

maintenance wait absorbed into the service timing contract
    != zero maintenance latency
```

### E — the 1973 counters and TI traversal counters are not the same retained control state

US3737879's per-row counters represent how long a row has gone without a restorative event. The TI sequential refresh counter represents which row is next in a traversal.

Thus:

```text
row-age / deadline evidence
    != traversal position

proof a row is due
    != proof a cyclic enumerator currently names that row
```

Both are maintenance-control state, but their semantics and failure consequences differ.

### Chronology boundary

Patent filing dates are not silently treated as public dates:

```text
US3729722A
    filed / priority 1971-09-17
    public patent 1973-04-24
    automatic recurrence at memory-system boundary

US3737879
    filed 1972-01-05
    public patent 1973-06-05

US4207618
    filed / priority 1978-06-26
    public patent 1980-06-10

US4333167
    filed 1979-10-05
    public patent 1982-06-01
```

This chronology is a checked public-document/control-partition chronology. It is **not** a first-invention or direct-influence genealogy.

---

## 1981–1983 autonomous self-refresh prior-art deepening

Detailed record: [`../evidence/09-1981-1983-autonomous-self-refresh-prior-art-deepening.md`](../evidence/09-1981-1983-autonomous-self-refresh-prior-art-deepening.md).

### H/P — self-refresh with timer + counter is present in 1981 literature

E. A. Reese and colleagues published a self-refresh DRAM paper in *IEEE Journal of Solid-State Circuits* 16(5), 1981, pp. 479–487, DOI `10.1109/JSSC.1981.1051626`.

Modern scholarly indexes preserve an abstract description in which self-refresh is implemented with an on-chip timer, arbiter, and refresh counter, with a `ready` relation exposed to the processor. The full IEEE paper was not directly page-inspected in this slice, so those mechanism claims remain abstract-level rather than figure/page-level grounding.

The peer-reviewed publication remains an important historical witness even though the broader self-refresh/control problem now has earlier public patent evidence:

```text
by 1981
    peer-reviewed DRAM self-refresh literature includes
        internal recurring refresh timing
        + internal row enumeration
        + refresh/access arbitration
```

It does not establish invention priority.

### H/P — Yamada et al. 1983 places AUTO and SELF refresh in one DRAM architecture

Michihiro Yamada and colleagues' January-1983 publication `Auto/Self Refresh機能内蔵64Kbit MOSダイナミックRAM`, translated/indexed as `A 64Kbit MOS dynamic RAM with auto/self refresh functions`, DOI `10.1002/ECJA.4400660114`, provides a second early publication anchor.

Later Mitsubishi patents explicitly attribute a conventional refresh circuit to that 1983 article and describe separate functional blocks for:

- refresh control;
- an internal timer producing later refresh requests;
- a refresh-address counter;
- a multiplexer selecting external or refresh-counter addresses.

The later patents are manufacturer-authored prior-art reconstructions, not substitutes for direct page-level inspection of the 1983 paper. They are used conservatively to establish the attributed control partition.

### H/P/E — early DRAM already occupied more than one refresh-control partition

The early source set therefore supports at least these design classes:

```text
system-level automatic cadence + system-level row enumeration
    (GTE April-1973 preferred embodiment around commercial Intel 1103 chips)

row-age/deadline-triggered selective refresh
    (MOS Technology June-1973 public patent)

external cadence + internal row enumeration
    (for example, TI's 1980 public on-chip-refresh patent and later CBR/internal-counter designs)

internal cadence + internal row enumeration + access arbitration
    (for example, TI's 1982 public patent and early self-refresh publication evidence)
```

The historical correction is important: **automatic recurrence does not imply on-chip integration, and internal cadence is not a late-1990s invention merely because the 1999 Micron device gives Case 09 a particularly clean product-level AUTO/SELF comparison. Nor is 1981 now treated as the earliest public-document floor for the broader self-refresh control problem.**

### E — autonomous recurrence remains a powered, regime-scoped property

The early self-refresh evidence does not turn DRAM into a nonvolatile medium. External memory-system automatic controllers and internal timer/counter logic alike require sufficient electrical power, valid mode/control conditions where applicable, and functioning restoration circuitry.

Thus:

```text
main requester relinquishes recurring refresh control
    != memory subsystem becomes unpowered
    != refresh obligation disappears
```

Battery-backed or standby discussions are changes in retention infrastructure and authority, not evidence of quiescent nonvolatile payload storage.

---

## Refresh-counter initialization and testability deepening

### H/P — the TI disclosed counter has a power-on phase

US4653030A states that the disclosed refresh-counter latch is forced to zero at power-on and that the counter starts at zero, then increments through its carry path on successive CAS-before-RAS refresh cycles.

This is a narrower claim than `CBR counters start at zero` in general. It establishes the initialization semantics of **this disclosed TI embodiment**, not a universal DRAM-interface guarantee and not the exact hidden circuit of TMS4256/TMS4257.

### H/P — Motorola exposes a commercial refresh-counter test

Motorola's 1989 *Memory Data* section for MCM514256A / MCM51L4256A documents `CAS BEFORE RAS REFRESH COUNTER TEST`. During that test the internal counter generates the row address while the external address supplies the column address; the prescribed read-write sequence repeats for 512 cycles and later normal reads check the pattern. The product text also requires at least eight CAS-before-RAS initialization cycles before performing the test.

This makes a normally hidden maintenance enumerator operationally testable through controlled payload observations. It does **not** mean that ordinary refresh writes counter history into application data, and the Motorola product implementation is not identified with TI's patent circuit.

### E — the retention infrastructure has its own lifetime boundary

The power-on initialization detail sharpens the earlier `maintenance-control state` claim. The refresh count must persist long enough to distribute refresh work correctly during a powered retention episode, but the TI embodiment does not preserve that phase as a durable cross-power record.

> **maintenance-control state lifetime != application-state lifetime under every failure model.**

For volatile DRAM, losing power ends the ordinary powered retention regime itself. A counter that organizes that regime can therefore be intentionally reinitialized at the next power-up without constituting a rollback of persistent application history.

### E — cadence and coverage are independent maintenance obligations

The existing Case 09 split between scheduling and row enumeration has an operational witness: Motorola supplies a procedure specifically for checking the counter's traversal behavior.

Thus:

```text
enough refresh requests
    !=
verified traversal of all required rows
```

and conversely a correctly progressing counter does not prove that the responsible scheduler — external in CBR/AUTO regimes or internal in SELF REFRESH — met the refresh deadline.

The counter-test result is also event-bounded evidence, not a permanent certificate of future refresh correctness.

---

## 1999 SDRAM AUTO REFRESH vs SELF REFRESH control-boundary deepening

Detailed record: [`../evidence/09-micron-1999-sdram-auto-vs-self-refresh-deepening.md`](../evidence/09-micron-1999-sdram-auto-vs-self-refresh-deepening.md).

### H/P — AUTO REFRESH internalizes addressing without internalizing repeated-command cadence

Micron's November-1999 64 Mb SDRAM datasheet (`MT48LC16M4A2 / MT48LC8M8A2 / MT48LC4M16A2`, `Rev. 11/99`) explicitly calls `AUTO REFRESH` analogous to CAS-before-RAS refresh in conventional DRAM.

The same paragraph says the command is **nonpersistent** and must be issued each time refresh is required. The refresh address is generated internally; ordinary address bits are `Don't Care` during the command. For the documented family, 4,096 AUTO REFRESH cycles are required within 64 ms.

So this later product preserves the core Case-09 split:

```text
internal refresh-row enumeration
    !=
internal recurring refresh-cadence authority
```

### H/P — SELF REFRESH internalizes recurring clocking after entry

The adjacent `SELF REFRESH` description says the SDRAM can retain data without external clocking. Entry resembles AUTO REFRESH except CKE is held low; once the command is registered, the SDRAM provides its own internal clocking and performs its own AUTO REFRESH cycles while the mode remains active.

The bounded control partition is therefore:

```text
AUTO REFRESH
    external system/controller: repeated refresh commands / cadence
    DRAM: row enumeration + refresh execution

SELF REFRESH steady state
    external system/controller: establishes/maintains the mode condition
    DRAM: internal clocking + recurring refresh + row enumeration + execution
```

This is product-level evidence for internal scheduling within the entered self-refresh regime. After the early-prior-art deepening, it is **not** treated as the first historical appearance of internally timed self-refresh.

### H/P — both modes share the row refresh counter but not the same authority relation

Micron states that AUTO REFRESH and SELF REFRESH both use the row refresh counter.

That directly supplies a useful negative control:

> **shared maintenance-control state != shared scheduling authority.**

The current counter phase may be common infrastructure even while the authority that advances recurring maintenance differs by mode.

### H/P — SELF REFRESH exit is a maintenance handoff, not an instantaneous semantic flip

Micron requires the external clock to be stable before CKE returns high and requires NOP commands during `tXSR` because an internal refresh may still be in progress.

Thus:

```text
exit requested
    != internal refresh necessarily already complete
    != normal command service immediately available
```

After the exit interval, ordinary AUTO REFRESH cadence again becomes an external obligation.

### E — a maintenance mode can retain a control regime rather than a history

AUTO REFRESH is explicitly nonpersistent: the request must recur. SELF REFRESH instead establishes a mode in which refresh recurrence continues internally until exit.

This makes a bounded distinction between:

```text
repeated maintenance request
    vs
retained maintenance regime
```

The mode is not application history. It is retained control state that changes who must initiate the recurring work needed to preserve payload.

---

## Retained state

There are several different retained-state/control-state layers in this case.

### Payload state

As in the grounded DRAM case, the memory array holds volatile dynamic state that must be periodically reconstructed.

### Refresh-age / deadline state

The 1973 MOS Technology patent exposes one form of maintenance evidence that tracks how long individual rows have gone without a restorative event. It is control state about the preservation obligation, not user payload and not the same thing as a cyclic traversal pointer.

### Refresh-coverage state

A refresh counter has a current count that determines which row will be selected on a later refresh request. The GTE preferred embodiment places such traversal state in surrounding system circuitry; TI's later on-chip designs provide examples with the counter inside the memory device. The count is not application payload and does not preserve user history. It is nevertheless retained control state that helps ensure maintenance is distributed across the row set.

### Cadence / timer state

Recurring cadence can likewise live at different boundaries. GTE's preferred embodiment uses a free-running system-level clock; an internally timed self-refresh regime can instead use on-chip timing or clocking machinery.

Timer/oscillator state and counter phase are distinct: one answers approximately **when** maintenance is due; the other answers **which row** is next.

### Maintenance-mode state

An entered self-refresh mode is another control condition: it changes the source of recurring refresh timing without turning that condition into application history.

### Arbitration / service state

GTE's `memory busy` relation can defer external service, the 1973 MOS Technology mandatory-refresh path can inhibit access, TI's 1982 patent can delay/latch service around an internal refresh, and the 1981 self-refresh publication's abstract-level arbiter/`ready` relation makes the same general distinction visible: deciding that refresh is due does not by itself determine how a simultaneous service request is handled.

This gives the repository a recursive retention relation:

> **a mechanism for preserving payload can itself depend on smaller retained states or modes that organize preservation work.**

That is an engineering reconstruction from documented counter/timer/mode roles, not a philosophical claim that those control states are an archive or memory in the cultural sense.

---

## Retention mechanism

The physical payload-retention regime remains deadline-driven reconstruction. What changes is the control partition.

### Externally controlled / system-level automatic regime

In GTE's bounded preferred embodiment:

1. the commercial DRAM chips expose a finite refresh obligation;
2. a free-running clock in the memory-system apparatus produces recurring cadence;
3. a system-level row counter supplies successive maintenance row addresses;
4. gating selects the refresh address rather than the ordinary external row address during maintenance;
5. a `memory busy` relation defers ordinary access while refresh occupies the memory cycle.

This is automatic recurrence relative to the CPU/requester without being chip-local self-refresh.

### Row-age/deadline-tracked self-refresh regime

In the bounded MOS Technology 1973 patent:

1. a row's ordinary access/restoration can reset its maintenance-age state;
2. rows that age to the permitted limit can force mandatory refresh;
3. forced maintenance can change access admission;
4. idle periods can optionally be used for earlier voluntary refresh.

This is not a claim about later DRAM implementation or a modern retention-aware scheduler; it is a period patent control partition.

### Externally triggered internal-address regime

In the bounded 1980 TI patent and later CBR family evidence:

1. external logic causes each refresh event;
2. ordinary external address inputs are not used for the refresh row;
3. the on-chip counter supplies the refresh row;
4. the DRAM performs the row-level sense/restoration operation;
5. successive refresh requests progress the internal count.

The maintenance obligation survives while one part of its control path migrates across the package boundary.

### Internally clocked refresh regime

In the bounded 1982 TI patent:

1. an on-chip refresh clock supplies recurring cadence;
2. an on-chip counter supplies successive row addresses;
3. device control logic arbitrates refresh against ordinary reads/writes;
4. an ordinary request that collides with an already-started refresh may wait until maintenance completes.

This supplies an earlier public-patent witness for internal cadence and row enumeration without claiming a named shipped product.

### Early autonomous-self-refresh publication regime

In the bounded 1981–1983 prior-art slice:

1. external logic establishes a self-refresh condition/regime;
2. an on-chip timer determines later refresh recurrence;
3. an on-chip refresh counter supplies successive maintenance addresses;
4. refresh-control/arbitration logic coordinates the maintenance operation;
5. ordinary service may be delayed, blocked, or arbitrated depending on the design.

This is a historical publication-level control partition, not a claim about every early DRAM.

### SDRAM AUTO REFRESH regime

In the bounded Micron 1999 product:

1. external logic issues each AUTO REFRESH command;
2. the command is nonpersistent;
3. refresh addressing is internal;
4. the DRAM performs refresh work;
5. enough commands must still be supplied within the documented refresh window.

### SDRAM SELF REFRESH regime

After explicit mode entry in the bounded Micron product:

1. external logic establishes the required entry/mode condition;
2. the DRAM supplies internal clocking;
3. recurring refresh proceeds internally;
4. the shared row refresh counter continues to organize row coverage;
5. exit requires a handoff interval before normal command service resumes.

Thus retention-work locus is mode-dependent rather than a single permanent property of the device.

---

## Addressing and access geometry

This case shows that `addressing` itself has more than one role.

### Ordinary access address

The normal row/column address designates payload for read/write service.

### Maintenance address

The refresh row designates payload for reconstruction, not because software requested that data, but because the array must revisit it before a retention deadline.

GTE's preferred embodiment switches between the external row-address register and a system-level refresh counter; later CBR/self-refresh examples can generate the maintenance address inside the memory device. The source set therefore creates bounded cases in which:

> **service addressing and maintenance addressing can have different address sources, scheduling authorities, physical locations, deadline evidence, and arbitration rules while reaching the same payload array.**

The same physical row can be selected for an application access using an ordinary service address or selected for retention work using a separately generated maintenance address.

---

## Read / write / refresh semantics

This case does not redefine DRAM read/write physics. Its contribution is the additional operation classes and control regimes.

### Ordinary access as maintenance input

The MOS Technology 1973 patent makes one interaction especially explicit: a read-and-restore or write can reset a row's refresh-age state. A service operation can therefore change the timing of a later dedicated maintenance obligation without becoming identical to a refresh command.

The 1103 product documents add a separate historical witness: they describe whole-array refresh as accomplished in 32 read cycles while describing stored information as non-destructively read. This is a product-interface contract, not proof that all DRAM generations refresh through identical read semantics.

### RAS-only refresh

External row selection can be strobed without an ordinary data-return transaction.

### CAS-before-RAS refresh

The strobe ordering requests refresh behavior and selects the internal refresh-address path rather than the ordinary external row-address path.

### Hidden refresh

A refresh sequence can occur while an already produced output value remains valid under the specified timing conditions.

This means:

> **visible output continuity does not prove internal quiescence.**

The system can be actively maintaining retained state while one interface appears unchanged.

### System-level automatic recurrence

GTE's free-running refresh apparatus can initiate a maintenance cycle without a CPU/requester issuing one refresh command per event, yet the patent explicitly maintains `memory busy` and defers an ordinary access that collides with refresh.

This means:

> **automatic initiation != zero service occupancy.**

### Internally clocked / early self-refresh

An internal refresh clock or self-refresh condition can delegate repeated refresh timing and row progression to internal machinery. Depending on the implementation, normal access may be blocked, delayed, or explicitly arbitrated while maintenance is active.

This means:

> **internal recurrence != transparent concurrent service.**

### SDRAM AUTO REFRESH

A command explicitly requests one refresh operation while the DRAM supplies the internal refresh address. The command's nonpersistent nature keeps recurrence as an external responsibility.

### SDRAM SELF REFRESH

A mode-entry command establishes a regime in which recurring refresh clocking proceeds internally until exit. The product documentation therefore distinguishes a one-shot externally repeated request from a retained maintenance regime.

---

## Maintenance and labor

The case should not be narrated as `refresh became automatic` or as one monotonic migration into the chip.

A more accurate decomposition is:

| Function | GTE 1973 system-level controller | MOS Technology 1973 deadline-tracked patent | TI 1980 / bounded CBR locus | TI 1982 internally clocked patent | Early self-refresh literature | Micron 1999 AUTO REFRESH | Micron 1999 SELF REFRESH steady state |
| --- | --- | --- | --- | --- | --- | --- | --- |
| physical need to refresh before deadline | DRAM/device physics | array/device physics | array/device physics | array/device physics | array/device physics | array/device physics | array/device physics |
| recurring cadence / due-state authority | free-running memory-system clock | per-row age/deadline logic | external processor/controller | internal refresh clock | internal timer within entered self-refresh regime | external system/controller | internal clocking after external mode entry |
| request / mode establishment | controller self-initiates while powered | deadline-triggered mandatory path; optional idle-period voluntary path | external refresh command / CBR timing | internal periodic signal | external establishment of self-refresh condition; exact interface design-specific | AUTO REFRESH command each time | SELF REFRESH entry + maintained CKE condition |
| next refresh-row selection | system-level row counter | due row selected from deadline evidence | on-chip refresh counter | on-chip refresh counter | on-chip refresh counter in bounded examples | on-chip refresh controller/counter | on-chip refresh controller/counter |
| access conflict policy | `memory busy`; colliding access deferred | mandatory refresh can inhibit access | ordinary controller/device timing | colliding read/write waits for refresh already underway | explicit arbitration / possible access lockout in bounded evidence | command/timing rules | normal access unavailable until exit/handoff |
| row sensing / restoration | DRAM circuitry | memory circuitry | on-chip memory circuitry | on-chip memory circuitry | on-chip memory circuitry | on-chip memory circuitry | on-chip memory circuitry |
| transition back to ordinary operation | after refresh cycle / busy clears | after mandatory refresh | not this mode distinction | after internal refresh completes | implementation-specific | ordinary command regime | external clock stabilization + `tXSR` handoff |

The relevant historical differences are **alternative distributions of retention work and authority**, not disappearance of work and not necessarily one linear sequence of offload.

The 1103 product contract sits orthogonally to this table: `32 read cycles / 2 ms` states a coverage/deadline obligation, while the GTE controller shows one concrete way surrounding infrastructure can generate cadence, traversal, address-source selection, and service arbitration to satisfy it.

This is closely related to the repository's maintenance-visibility audit: automation can remove a responsibility from one interface or board-level circuit while making another internal state/path or mode more important.

---

## Failure / forgetting modes

The mechanism distinguishes several failures that would all look like `refresh failure` at too high a level.

### Lost / wrong deadline evidence

In a deadline-tracked design, control state about how long a row has gone without restorative service can be wrong even before payload decay becomes externally visible.

### Missed deadline

The responsible scheduler causes too few refresh cycles before the retention interval expires. Depending on architecture/mode, that scheduler may be system-level, controller-local, or internal to the memory device.

### Wrong operation selection / wrong mode

The control sequence fails to invoke the intended refresh path or maintenance mode.

### Enumeration failure

The active refresh counter/address path — whether system-level or on-chip in the bounded examples — fails to cover the required rows correctly.

### Internal cadence failure

Within an internally clocked or documented self-refresh regime, internal recurring timing fails to cause the required refresh work.

### External/system cadence failure

Within a system-level automatic or externally commanded regime, the surrounding oscillator/controller fails to produce sufficient refresh events despite a still-valid DRAM payload/coverage contract.

### Arbitration / service-handoff failure

A design or host mishandles a conflict between refresh and access, or assumes normal service before a documented mode transition has completed.

### Reconstruction-path failure

The correct row is selected, but sensing/restoration does not correctly reconstruct its logical state.

These are not asserted as specific measured silicon failure rates. They are architecture-level failure classes implied by the sourced partition of functions.

---

## Engineering reconstruction

### E — refresh obligation ≠ refresh-address-generation locus

Case 03 links the deadline to physical charge leakage. Case 09 shows that the place where the next row number is generated is a separate design choice.

The retention requirement can remain stable while maintenance responsibility moves.

### E — automatic recurrence ≠ on-chip integration

The GTE source provides a particularly clean counterexample to a one-axis automation story. Its memory subsystem can self-initiate recurring refresh relative to the processor while the worked Intel 1103 chips remain externally maintained by a free-running clock, counter, gating, and busy logic outside the DRAM package.

Therefore:

```text
who initiates recurring maintenance
    !=
where refresh-control machinery is physically integrated
```

GTE 1973 and TI 1980 even occupy complementary partitions: the former automates cadence while keeping enumeration outside the DRAM; the latter places refresh enumeration on-chip while still requiring an external refresh request for each event.

### E — product coverage/deadline contract ≠ one scheduler implementation

The 1103 product evidence constrains **coverage** and **deadline**. It does not logically require GTE's uniform 16 kHz phase, a particular counter package, or one arbitration policy. GTE's worked controller is one system realization of the product obligation.

The Intel 1103A-1 comparison further blocks an easy geometry shortcut: the same 32-cycle coverage count can coexist with a different one-millisecond refresh deadline.

Thus:

```text
row/coverage geometry
    != retention deadline

retention deadline + coverage requirement
    != one unique maintenance scheduler
```

### E — internalized refresh addressing ≠ autonomous refresh scheduling

The TI CBR patent directly says the processor or memory controller controls the frequency of the CAS-before-RAS sequence. Micron's 1999 AUTO REFRESH similarly uses internal addressing while requiring each refresh command externally.

The earlier prior-art deepening adds complementary witnesses: GTE automates cadence at the memory-system level while keeping enumeration outside the DRAM; the 1980 TI patent isolates external cadence + internal enumeration; the 1982 TI patent puts cadence and enumeration on chip; the 1973 MOS Technology patent instead tracks row-specific due state; the 1981–1983 publication record adds peer-reviewed/self-refresh examples with timer, counter, and arbitration.

Therefore `internal refresh address`, `internal refresh schedule`, `automatic refresh relative to requester`, and `internal deadline evidence` are demonstrably different properties, and multiple combinations existed well before the late SDRAM era.

This gives a cleaner vocabulary for future cases:

```text
refresh deadline
refresh-age / due-state evidence
refresh scheduler / cadence authority
refresh trigger or mode-entry mechanism
refresh enumerator / coverage state
address-source authority
access/maintenance arbitration
refresh executor / restorer
transition / handoff semantics
physical/system boundary for each function
```

Do not collapse them back into one word, `refresh`.

### E — no single linear offload chronology

The source set blocks a tempting teleology:

```text
external everything
    -> internal row counter
    -> much later internal timer
```

A better historical reconstruction is that different designs explored different control partitions: automatic system-level recurrence, deadline-tracked selective refresh, external cadence with internal addressing, internally timed refresh, and self-refresh modes were all part of the early design space.

Historical coexistence does not itself establish influence or descent among those designs.

### E — hidden maintenance is observer-relative

GTE's controller can hide one-refresh-command-per-event labor from the processor while still exposing `memory busy` and access deferral. The 1982 TI patent can hide recurring refresh commands from the CPU while occasional collisions still affect access latency. Hidden refresh can maintain an output while refresh cycles proceed. Self-refresh can remove recurring host command traffic while internal cycles continue. In each case the operation is hidden only relative to particular interfaces or observers. It remains visible to timing, power, control, or device-level analysis.

### E — maintenance machinery can have retention state

A refresh traversal counter must carry enough sequential state between refresh requests to choose successive rows. GTE places that coverage state in surrounding system circuitry; later TI examples place it inside the memory device. A deadline-tracked design can instead retain due-state/age evidence for rows. In internally timed self-refresh, timer/mode/arbitration state additionally organizes when maintenance happens and when normal access may proceed.

The earlier counter-initialization deepening adds a horizon boundary: the TI disclosed CBR phase is initialized at power-on rather than preserved as a durable cross-power checkpoint. The early patent/publication evidence adds a control decomposition, while the Micron evidence adds a clean later authority boundary: the same row refresh counter participates in both AUTO REFRESH and SELF REFRESH even though cadence authority differs by mode.

> **maintenance-control-state meaning != maintenance-control-state location != maintenance-authority location != maintenance-control-state persistence horizon.**

### E — autonomy is regime-scoped and power-dependent

System-level automatic recurrence, internally clocked refresh, early self-refresh, and Micron's later SELF REFRESH support autonomous recurrence only within their documented powered operating conditions/regimes.

Thus:

```text
automatic recurring refresh
    != globally autonomous memory system
    != unpowered nonvolatile retention
```

---

## Philosophical / media-theoretical interpretation

### I — persistence can involve relocation of responsibility

This case sharpens the project's maintenance thesis without turning it into a metaphor. The relevant technical fact is not merely that `DRAM needs refresh`; that was already established. The new fact is that the functions making refresh possible can migrate across an interface, coexist in alternative partitions, or switch authority by mode while the underlying physical obligation remains.

GTE adds a particularly useful limit: responsibility can move away from the CPU/requester into dedicated infrastructure **without** moving into the DRAM chip itself.

This makes `where is the maintenance?`, `who currently initiates it?`, `what evidence says maintenance is due?`, `what system boundary is being described?`, and `what infrastructure remains powered?` as important as `is there maintenance?`

### I — invisibility and autonomy are relations between mechanism and observer

At the CPU boundary, GTE's memory subsystem can appear to initiate its own refresh; at the DRAM-package boundary, the same chips are externally refreshed. The 1982 `invisible to CPU` patent is another strict technical example: the CPU can be relieved of recurring refresh control even though a colliding request may still wait for internal maintenance. Hidden refresh is another case in which continued output availability can coexist with ongoing reconstruction beneath that interface. Self-refresh adds another: recurring maintenance may continue without recurring host commands or external refresh clocks even though power and mode conditions still sustain the device.

These observations do not by themselves establish Heideggerian `Bestand`, Stieglerian tertiary retention, or a general philosophy of technological autonomy.

---

## Functional analogies and limits

### A/H/P — bounded early comparison

The early prior art gives a controlled counterexample to one-period/one-architecture storytelling:

```text
GTE April-1973 patent
    system-level automatic cadence
    + system-level row enumeration / address gating
    + memory-busy service deferral
    != on-chip self-refresh

MOS Technology June-1973 patent
    row-age/deadline evidence + mandatory/opportunistic refresh

TI 1980 patent
    external cadence + internal enumeration

Reese et al. 1981 self-refresh publication
    on-chip timer + internal counter + arbitration

TI 1982 patent
    internal cadence + internal enumeration + access-delay arbitration

TI 1984-filed CBR-counter design
    internal row enumeration + external request cadence
```

The useful conclusion is **coexisting control partitions**, not a genealogy and not a claim that any one architecture universally characterized its period.

### A/H/P — bounded later comparison to SDRAM SELF REFRESH

Micron's November-1999 product documentation remains valuable because it places AUTO REFRESH and SELF REFRESH side by side under one synchronous product interface.

The bounded comparison is:

```text
early patent/publication designs
    multiple internal/external control partitions
    historical interfaces design-specific

TI 1984-filed CBR-counter design
    internal row enumeration
    external request cadence

Micron 1999 AUTO REFRESH
    internal row enumeration
    external repeated-command cadence

Micron 1999 SELF REFRESH
    internal row enumeration
    internal recurring clocking after external mode entry
```

The useful conclusion is a control-locus distinction and a historical correction, not a claim that one implementation descends directly from another or that 1999 marks the invention of self-refresh.

### A — analogy to controller offload

Moving row enumeration or recurring cadence from requester logic into dedicated memory-system circuitry or into the DRAM can be described functionally as an offload of maintenance-control functions.

`Offload` is a modern analytical term here, not a recovered 1970s/1980s or 1999 actor category.

### A — analogy to HDFS scanner progress state

Case 83's HDFS scanner cursor is also retained control state that distributes maintenance work across a payload population. The analogy stops at that function. HDFS checkpoints traversal position so a process/restart can resume without replaying the entire scan; GTE's and TI's DRAM refresh counters organize a powered recurrence regime rather than a durable process-restart history, and the TI CBR embodiment initializes the cyclic refresh phase at power-on. Their persistence horizons and authority semantics are therefore different.

> **maintenance-control state != one universal checkpoint contract.**

This is a functional comparison, not a DRAM-to-HDFS genealogy.

### Limit — patent disclosure ≠ product implementation

US3729722A, US3737879, US4207618, and US4333167 are strong public technical documents for prior-art control partitions. They are not, in this slice, proof that a particular commercial product shipped with every disclosed mechanism. GTE's preferred embodiment names a commercial Intel 1103 as the maintained device, but that does not prove commercial deployment of the surrounding GTE controller. Shared corporate authorship and later citation do not prove which commercial die implemented which disclosed circuit.

### Limit — product contract ≠ system-controller genealogy

The Signetics 1972 and Intel 1975 1103 documents ground a coverage/deadline product contract. They do not prove that Signetics and Intel implementations were electrically identical, that GTE's exact controller shipped with either product, or that one product contract dictates one controller topology.

### Limit — patent mechanism ≠ exact TMS4256 implementation

US4653030A and the TMS4256/TMS4257 datasheet are complementary evidence classes. The patent provides manufacturer-primary mechanism detail; the commercial datasheet provides product-family behavior. The patent does not identify its preferred embodiment as the exact TMS4256/TMS4257 circuit.

### Limit — abstract/patent prior-art reconstruction ≠ direct early-paper facsimile

The 1981 JSSC and 1983 Yamada publication anchors are strong enough to establish early self-refresh literature and its broad mechanism class, but this slice did not directly inspect their full page images. Detailed circuit claims are therefore bounded to abstract-level metadata and later manufacturer patent reconstructions that explicitly cite the publications.

### Limit — Micron product documentation ≠ JEDEC genealogy

The 1999 Micron datasheet establishes a named-product control boundary. It does not establish when JEDEC first standardized SELF REFRESH, which vendor invented the feature, the first commercial shipment, or the exact internal oscillator topology.

### Limit — no general DRAM generation history

Density, process, package, page/nibble modes, broad controller IC history, DDR per-bank refresh, ECC, and later retention-aware refresh policy are outside this slice unless they alter a future retention comparison.

---

## Cross-case result

Case 03 established:

> **time can create a retention obligation even without useful access.**

Case 09 adds:

> **the obligation, evidence that maintenance is due, the machinery that discharges it, and the boundary at which that machinery appears automatic must be analyzed separately; those functions historically had multiple control partitions rather than one simple migration path.**

A compact comparison is:

```text
Case 03
    why refresh is required
    deadline-driven reconstruction

Case 09 — GTE 1973 system-level automatic refresh
    free-running cadence + row traversal live outside commercial DRAM chips
    colliding service can be deferred

Case 09 — 1103 product contract
    coverage count + retention deadline
    does not itself choose scheduler topology

Case 09 — MOS Technology 1973 deadline-tracked patent
    retained row-age evidence can force selective maintenance
    ordinary access can reset that due-state relation

Case 09 — TI 1980 patent / later CBR
    internal counter supplies maintenance address
    external controller still supplies recurring request cadence

Case 09 — TI 1982 internally clocked patent
    internal timer + internal counter
    colliding service may wait for refresh completion

Case 09 — 1981–1983 self-refresh literature
    internal timer can own recurring cadence
    internal counter can own row enumeration
    arbitration/service semantics remain a separate problem

Case 09 — 1999 SDRAM successor
    AUTO REFRESH: external repeated cadence + internal addressing
    SELF REFRESH: internal recurrence after explicit mode entry
    same product exposes both authority regimes
```

This produces ten particularly useful controls:

1. **refresh obligation ≠ refresh-address-generation locus**;
2. **refresh-age/deadline evidence ≠ traversal position**;
3. **automatic recurring refresh ≠ on-chip refresh integration**;
4. **coverage geometry ≠ retention deadline ≠ one unique scheduler**;
5. **internalized refresh addressing ≠ autonomous refresh scheduling**;
6. **internal cadence authority ≠ transparent concurrent access**;
7. **hidden refresh ≠ absence of retention work**;
8. **shared maintenance-control state ≠ shared scheduling authority**;
9. **self-refresh ≠ nonvolatility or absence of power dependence**;
10. **public patent prior art / product chronology ≠ demonstrated implementation genealogy**.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| US3729722A publicly documents `self-initiating refresh` by 24 April 1973 | H/P | direct public patent transcript; filing/public dates kept distinct |
| GTE's preferred embodiment uses commercial Intel 1103 chips with a separate free-running clock, refresh pulse generator, row-address counter, gating, and `memory busy` relation | H/P | direct US3729722A description; system-level apparatus, not chip-local self-refresh |
| In the GTE embodiment, colliding external access is deferred until refresh completes | H/P | direct US3729722A description |
| GTE's `self-initiating refresh` establishes automatic recurrence at the memory-system boundary, not proof of on-chip self-refresh | H/P/E | direct mechanism + bounded boundary reconstruction |
| Signetics 1972 and Intel 1975 1103 product documents specify full-array refresh in 32 read cycles every two milliseconds | H/P | manufacturer-authored product documentation; exact early Intel stepping chronology not claimed |
| Intel 1103A-1 keeps the 32-cycle coverage count while specifying a one-millisecond refresh period | H/P | Intel 1975 catalog product comparison |
| US3737879 publicly documents a `self-refreshing memory` by June 1973 | H/P* | direct public patent transcript/mirror; filing/public dates kept distinct |
| US3737879 uses row-specific counters so ordinary access can reset refresh-age state and an expired row can force mandatory refresh | H/P* | direct public patent transcript; patent disclosure, not product deployment |
| US3737879 also describes voluntary refresh during otherwise idle periods | H/P* | direct public patent transcript; not equated with modern background scheduling |
| US4207618 publicly documents external refresh requests with internal row enumeration by June 1980 | H/P | Google Patents primary patent text |
| US4333167 publicly documents internally timed refresh plus internal row enumeration and read/write collision handling by June 1982 | H/P* | Justia public patent transcript; patent disclosure, not named product |
| TMS4256/TMS4257 documentation specifies a 4 ms refresh period | H/P | TI period data book; later revision facsimile directly inspected |
| TMS4256/TMS4257 supports RAS-only, CAS-before-RAS, and hidden refresh | H/P | TI period data book + direct later-revision facsimile |
| CBR refresh ignores the external address and generates the refresh address internally | H/P | TI manufacturer documentation |
| TI patented an on-chip refresh counter activated by CAS-before-RAS | H/P | US4653030A abstract/summary/figures |
| TI explicitly named TMS4164 as a commercial device lacking the patent's refresh counter | H/P | US4653030A description |
| The bounded TI CBR patent leaves refresh-trigger cadence with an external processor/controller | H/P | US4653030A refresh-cycle discussion |
| A Reese et al. DRAM self-refresh paper appeared in IEEE JSSC in 1981, vol. 16 no. 5, pp. 479–487, DOI `10.1109/JSSC.1981.1051626` | H/P | strong bibliographic record; full paper not directly page-inspected in this slice |
| The indexed Reese abstract describes an on-chip timer, arbiter, and refresh counter | H/P | abstract-level evidence; detailed circuit claims intentionally bounded |
| Yamada et al. published a 64-Kbit DRAM `auto/self refresh` paper in January 1983, DOI `10.1002/ECJA.4400660114` | H/P | strong bibliographic record; full article not directly page-inspected here |
| Later Mitsubishi patents explicitly attribute a timer + refresh-counter + address-multiplexer architecture to the 1983 Yamada paper | H/P | later manufacturer prior-art reconstruction |
| Internally timed self-refresh/control therefore has public evidence before the 1999 SDRAM witness and before the 1981 peer-reviewed paper | H/P | strong at patent/publication mechanism-class level; no priority or genealogy claim |
| TI's disclosed CBR refresh counter starts at zero at power-on and increments on CBR refresh cycles | H/P | US4653030A counter-stage description |
| Motorola documents a product-level CBR refresh-counter test using internal row selection and controlled data writes | H/P | 1989 *Motorola Memory Data* product section |
| The Motorola counter test requires initialization cycles and uses 512 cycles to exercise the documented row set | H/P | Motorola counter-test procedure |
| Micron Rev. 11/99 calls SDRAM AUTO REFRESH analogous to conventional CBR refresh | H/P | manufacturer-authored 64 Mb SDRAM datasheet, printed p. 13 via page-preserving mirror |
| Micron AUTO REFRESH is nonpersistent and uses internally generated refresh addressing | H/P | same 1999 page |
| Micron SELF REFRESH retains data without external clocking and uses internal clocking for recurring refresh | H/P | same 1999 page |
| AUTO REFRESH and SELF REFRESH share the row refresh counter in the bounded Micron product | H/P | same 1999 page |
| SELF REFRESH exit includes a `tXSR` handoff because internal refresh may still be in progress | H/P | same 1999 page |
| `self-initiating refresh` in GTE proves Intel 1103 contained on-chip self-refresh | X | directly rejected by the preferred embodiment's separate system-level clock/counter/gating apparatus |
| A 32-cycle / 2 ms product contract proves one required scheduler phase/topology | X | product coverage/deadline obligation does not dictate GTE's specific controller implementation |
| Internal row enumeration proves internal recurring scheduling | X | directly rejected by TI 1980/CBR and Micron AUTO REFRESH control partitions |
| Internal recurring scheduling proves transparent concurrent normal access | X | rejected by TI 1982 wait semantics and early self-refresh arbitration/access-lockout evidence |
| Self-refresh proves unpowered retention / nonvolatility | X | rejected: dynamic payload still depends on powered periodic restoration |
| Sharing one row refresh counter proves identical maintenance authority | X | directly rejected by AUTO vs SELF REFRESH mode distinction |
| The 1973 per-row age counters are equivalent to later cyclic refresh counters | X | different retained-control semantics: due-state evidence vs traversal position |
| Motorola's product counter is proven to use TI's power-on-zero circuit | X | unsupported cross-vendor implementation identity |
| A successful counter test permanently certifies future refresh correctness | X | bounded diagnostic event ≠ continuing scheduler/coverage correctness |
| Maintenance-control state must persist across power loss whenever it helps retain payload | X/E | TI's disclosed CBR counter is intentionally initialized at power-on; persistence horizon is regime-specific |
| Moving refresh enumeration on-chip removes the periodic retention obligation | X | contradicted by the same source set |
| `self refresh circuitry` in the TI CBR patent automatically means autonomous self-refresh | X | rejected by TI's external-trigger statement and early/later distinct self-refresh mechanisms |
| 1981 Reese or 1999 Micron marks invention priority for autonomous DRAM self-refresh | X | contradicted by earlier public patent evidence; first-invention question remains out of scope |
| The early patents/publications, GTE controller, TI CBR patent, and Micron SDRAM form a demonstrated direct genealogy | X | unsupported historical continuity |
| Patent filing date is interchangeable with public disclosure date | X | explicitly rejected by chronology discipline |
| The TI CBR patent is proven to be the exact TMS4256 circuit | X | unsupported product-identity leap |
| Micron's 1999 datasheet proves JEDEC invention/standardization chronology | X | product evidence ≠ normative genealogy |
| Retention infrastructure can itself contain retained control state | E | bounded reconstruction from deadline evidence, refresh counters, timers, arbitration, and mode roles |

---

## Related repositories

### `tmzncty/computing-archaeology`

Fresh related-repository searches for the exact GTE patent number `US3729722`, `1103`, `Intel 1103 refresh`, and the earlier Case-09 terms found no dedicated case to reuse. A broad history of early dynamic-memory refresh patents/products, Intel/Signetics second-source genealogy, exact 1103 stepping history, board-level refresh-controller development, quasi-static RAM, ISSCC/JSSC publication genealogy, DRAM refresh counters/timers, silicon implementation, vendor competition, SDRAM standardization, test modes, oscillators, and controller integration still belongs there:

<https://github.com/tmzncty/computing-archaeology>

This repository should keep only the retention-specific comparison about **device coverage/deadline contract, cadence authority, traversal state, system/package locus, retained due-state/coverage state, persistence horizon, arbitration, and visibility of maintenance work**.

### `tmzncty/problem-history`

Use its anti-anachronism discipline for `self-initiating refresh`, `self-refreshing memory`, and later `self refresh`. GTE's 1973 system-boundary wording, the June-1973 MOS Technology patent term, Reese/Yamada early self-refresh, TI's later patent title phrase, and Micron's 1999 mode name must each be interpreted through the mechanism and system boundary actually described rather than treated as timelessly identical vocabulary.

---

## Sources

1. Texas Instruments, *MOS Memory Data Book 1986*, TMS4256/TMS4257 device section, revision header `MAY 1983—REVISED NOVEMBER 1985`: <https://bitsavers.org/components/ti/_dataBooks/1986_SMYD006_TI_MOS_Memory_Data_Book.pdf>.
2. Texas Instruments, `TMS4256, TMS4257 — 262,144-BIT DYNAMIC RANDOM-ACCESS MEMORIES`, standalone page-preserving copy, revision header `MAY 1983—REVISED JANUARY 1988`, directly inspected printed pp. 4-3 and 4-5: <https://www.ardent-tool.com/datasheets/TI_TMS4256_7.pdf>.
3. Tadashi Tachibana, Chitranjan N. Reddy, Ngai H. Hong, `Self refresh circuitry for dynamic memory`, US4653030A, filed 31 August 1984, assigned to Texas Instruments: <https://patents.google.com/patent/US4653030A/en>.
4. Texas Instruments, *MOS Memory Data Book 1984*, TMS4164 family documentation: <https://vintage-computer-books.netlify.app/Texas%20Instruments%20-%20MOS%20Memory%20Data%20Book%20-%201984.pdf>.
5. Motorola, *Memory Data*, 1989, MCM514256A / MCM51L4256A product section, especially `REFRESH CYCLES` and `CAS BEFORE RAS REFRESH COUNTER TEST`: <https://www.bitsavers.org/components/motorola/_dataBooks/1989_DL113r6_Motorola_Memory_Data.pdf>.
6. Micron Technology, `MT48LC16M4A2 / MT48LC8M8A2 / MT48LC4M16A2` 64 Mb SDRAM, `Rev. 11/99`, printed p. 13, manufacturer-authored content preserved by a page-stable mirror: <https://www.alldatasheet.fr/html-pdf/228369/MICRON/MT48LC4M16A2/2945/13/MT48LC4M16A2.html>.
7. Micron Technology, same 64 Mb SDRAM family, `Rev. V 09/14`, later manufacturer-authored continuity witness preserved as PDF by Mouser, especially p. 33 and SELF REFRESH timing material: <https://www.mouser.com/datasheet/2/671/micts06234_1-2290735.pdf>.
8. E. A. Reese, D. W. Spaderna, S. T. Flannagan, F. Tsang, self-refresh DRAM paper, *IEEE Journal of Solid-State Circuits* 16(5), 1981, pp. 479–487, DOI `10.1109/JSSC.1981.1051626`: <https://doi.org/10.1109/JSSC.1981.1051626>.
9. Bibliographic record preserving the `A 4Kx8 dynamic RAM with self-refresh` title, authors, volume/issue/pages and DOI: <https://eurekamag.com/research/080/945/080945698.php>.
10. Michihiro Yamada et al., `A 64Kbit MOS dynamic RAM with auto/self refresh functions`, *Electronics and Communications in Japan*, vol. 66, no. 1, January 1983, DOI `10.1002/ECJA.4400660114`: <https://doi.org/10.1002/ECJA.4400660114>.
11. Takahiro Komatsu, `Dynamic type semiconductor memory device with a refresh function and method for refreshing the same`, US 5,251,176, Mitsubishi Electric, filed 27 August 1991; prior-art discussion explicitly attributes timer/counter/multiplexer architecture to Yamada et al. 1983: <https://patents.google.com/patent/US5251176A/en>.
12. Masaki Kumanoya et al., `Self-refreshing of dynamic random access memory device and operating method therefor`, US 4,943,960, Mitsubishi Electric, granted 24 July 1990; background describes timer + address-counter self-refresh without external refresh clocks and cites Yamada et al. 1983: <https://patents.google.com/patent/US4943960A/en>.
13. Gerald Lee Frenkil and Steven E. Golson, `Hidden refresh of a dynamic random access memory`, US 5,193,072, VLSI Technology, filed 21 December 1990; background distinguishes external refresh, internal-counter refresh, Reese self-refresh, and quasi-static RAM: <https://patents.google.com/patent/US5193072A/en>.
14. Richard M. Greene, Donald L. McLaughlin, John O. Paivinen, `Self-refreshing memory`, US3737879, filed 5 January 1972, granted/published 5 June 1973, assigned to MOS Technology: <https://uspto.report/patent/grant/3737879>; patent-corpus mirror: <https://patents.google.com/patent/US3737879A/en>.
15. Lionel S. White, Jr. and G. R. Mohan Rao, `On-chip refresh for dynamic memory`, US4207618A, filed/priority 26 June 1978, granted/published 10 June 1980, Texas Instruments: <https://patents.google.com/patent/US4207618A/en>.
16. David J. McElroy, `Dynamic memory with on-chip refresh invisible to CPU`, US4333167, filed 5 October 1979, granted/published 1 June 1982, Texas Instruments: <https://patents.justia.com/patent/4333167>.
17. Joseph Patrick Shuba, `Dynamic mode integrated circuit memory with self-initiating refresh means`, US3729722A, filed 17 September 1971, granted/published 24 April 1973, GTE Automatic Electric Laboratories: <https://patents.google.com/patent/US3729722A/en>; full public transcript mirror: <https://uspto.report/patent/grant/3729722>.
18. Signetics Corporation, 1972 MOS handbook, `1103 / 1103-1 — Fully Decoded Random Access 1024 Bit Dynamic Memory`, printed p. 23, directly inspected in the dedicated product-contract evidence: <https://device.report/m/dafd5c77c72a981090c96e4a55aefea73e10f1e24d60e279806c3cf4fb8a94a5.pdf>.
19. Intel Corporation, *1975 Intel Data Catalog*, `Silicon Gate MOS 1103 — Fully Decoded Random Access 1024 Bit Dynamic Memory`, catalog p. 2-7; same catalog supplies the bounded 1103A/1103A-1 comparison: <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/1975_Intel_Data_Catalog.pdf>.
