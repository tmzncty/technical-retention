# CAS-before-RAS DRAM Refresh: Moving Refresh Addressing On-Chip

## Status

**`grounded`** — bounded to Texas Instruments' TMS4164 contrast, TMS4256/TMS4257 refresh behavior, TI's 1984-filed on-chip refresh-counter design, an early-1980s autonomous-self-refresh prior-art deepening, and a late-1999 Micron SDRAM product comparison separating externally repeated AUTO REFRESH from device-clocked SELF REFRESH.

Grounding record: [`../evidence/09-ti-cbr-refresh-address-grounding.md`](../evidence/09-ti-cbr-refresh-address-grounding.md).

Deepening record: [`../evidence/09-dram-refresh-counter-initialization-test-deepening.md`](../evidence/09-dram-refresh-counter-initialization-test-deepening.md).

Early autonomous-self-refresh prior-art deepening: [`../evidence/09-1981-1983-autonomous-self-refresh-prior-art-deepening.md`](../evidence/09-1981-1983-autonomous-self-refresh-prior-art-deepening.md).

SDRAM control-boundary deepening: [`../evidence/09-micron-1999-sdram-auto-vs-self-refresh-deepening.md`](../evidence/09-micron-1999-sdram-auto-vs-self-refresh-deepening.md).

---

## Scope

- **Object / system:** a bounded comparison of early-1980s DRAM refresh-control partitions: externally enumerated refresh, CAS-before-RAS refresh with an on-chip refresh-address counter, and contemporaneous self-refresh designs that also placed recurring refresh timing on-chip; a late-1999 SDRAM product is retained as a later clean AUTO REFRESH / SELF REFRESH interface comparison.
- **Date range:** 1981–1986 for the central early control-partition evidence; a 1984-filed TI patent supplies mechanism-level CBR design detail. A January 1988 revision of the TMS4256/TMS4257 sheet was directly inspected only as a page-stable facsimile witness to the same documented device-family behavior. Micron's November-1999 64 Mb SDRAM documentation is used only as a later product-level successor witness for AUTO REFRESH versus SELF REFRESH control partition.
- **Primary comparison:** TMS4164 as an explicitly named commercial device lacking TI's patented refresh counter versus TMS4256/TMS4257-family CAS-before-RAS behavior; Reese et al. 1981 and Yamada et al. 1983 provide bounded prior art showing that internal timer + counter self-refresh was already an early-1980s alternative; the later Micron SDRAM comparison supplies a directly documented synchronous-interface contrast between repeated AUTO REFRESH commands and SELF REFRESH recurrence after mode entry.
- **Question:** what changes when the DRAM still has a periodic retention deadline but row enumeration, recurrence timing, mode control, and access arbitration can be placed under different authorities?

This is **not** a general history of DRAM evolution. The early self-refresh material is a bounded prior-art correction, not an invention-priority or product-shipment genealogy. The SDRAM material is a bounded AUTO REFRESH / SELF REFRESH control comparison, not a JEDEC genealogy or a full SDRAM history. DDR per-bank refresh, temperature-compensated refresh, retention-aware refresh research, and broad controller/test-mode history remain outside this case unless needed for a later retention comparison.

Case 03 already grounds the physical reason dynamic semiconductor state needs periodic reconstruction. This case starts one layer higher:

> **Does moving refresh-row enumeration or recurring refresh cadence on-chip change the retention mechanism, the maintenance obligation, or the location and authority of maintenance control?**

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
refresh-cycle scheduling / cadence authority
refresh trigger / mode entry
next-row enumeration
row selection / address-source authority
access-vs-refresh arbitration
sense / restoration
```

The early-self-refresh evidence adds an important historical correction: the functions did not migrate on-chip in one simple linear order. By 1981–1983, published self-refresh designs already combined an internal timer with an internal refresh counter, while other early-1980s DRAMs used internal row enumeration but still relied on external refresh cadence.

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

`Self refresh` cannot be treated as a timeless circuit category whose mechanism follows automatically from the phrase.

Reese et al. 1981 is indexed as describing self-refresh with an on-chip timer, arbiter, and refresh counter. Yamada et al. 1983 concerns a DRAM with auto/self-refresh functions, and later Mitsubishi prior-art reconstructions attribute an internal timer + refresh-counter architecture to that work.

By contrast, `self refresh circuitry` in TI's 1984-filed patent title does **not** mean that the disclosed CBR counter supplies recurring cadence: the patent explicitly says the processor or memory controller external to the memory device controls how often the CAS-before-RAS sequence occurs.

Micron's 1999 `SELF REFRESH` documents yet another concrete interface contract: after explicit mode entry, the SDRAM supplies internal clocking and performs recurring refresh cycles while the required mode condition remains active.

Therefore:

> **same historical phrase `self refresh` ≠ same command semantics, interface contract, or distribution of retention work.**

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

## 1981–1983 autonomous self-refresh prior-art deepening

Detailed record: [`../evidence/09-1981-1983-autonomous-self-refresh-prior-art-deepening.md`](../evidence/09-1981-1983-autonomous-self-refresh-prior-art-deepening.md).

### H/P — self-refresh with timer + counter is already present in 1981 literature

E. A. Reese and colleagues published a self-refresh DRAM paper in *IEEE Journal of Solid-State Circuits* 16(5), 1981, pp. 479–487, DOI `10.1109/JSSC.1981.1051626`.

Modern scholarly indexes preserve an abstract description in which self-refresh is implemented with an on-chip timer, arbiter, and refresh counter, with a `ready` relation exposed to the processor. The full IEEE paper was not directly page-inspected in this slice, so those mechanism claims remain abstract-level rather than figure/page-level grounding.

This is nevertheless enough to correct a chronological shortcut:

```text
by 1981
    internal recurring refresh timing
    + internal row enumeration
    + refresh/access arbitration
were already part of published DRAM self-refresh design
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

The early source set therefore supports at least these contemporaneous design classes:

```text
external cadence + external row enumeration

external cadence + internal row enumeration
    (for example, CBR/internal-counter designs)

internal cadence during a self-refresh regime + internal row enumeration
    (documented in early self-refresh literature)
```

The historical correction is important: **internal cadence is not a late-1990s invention merely because the 1999 Micron device gives Case 09 a particularly clean product-level AUTO/SELF comparison.**

### E — autonomous recurrence remains a powered, regime-scoped property

The early self-refresh evidence does not turn DRAM into a nonvolatile medium. Internal timer and counter logic still require sufficient electrical power, valid mode/control conditions, and functioning restoration circuitry.

Thus:

```text
main system relinquishes recurring refresh control
    != DRAM becomes unpowered
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

### Refresh-coverage state

The refresh counter has a current count that determines which row will be selected on a later refresh request. This count is not application payload and does not preserve user history. It is nevertheless retained control state that helps ensure maintenance is distributed across the row set.

### Cadence / timer state

In an internally timed self-refresh regime, an on-chip timer or clocking mechanism supplies the recurrence relation that an external controller otherwise has to supply.

Timer state and counter phase are distinct: one answers approximately **when** maintenance is due; the other answers **which row** is next.

### Maintenance-mode state

An entered self-refresh mode is another control condition: it changes the source of recurring refresh timing without turning that condition into application history.

### Arbitration / service state

The 1981 self-refresh publication's abstract-level arbiter/`ready` relation makes another distinction visible: deciding that refresh is due does not by itself determine how a simultaneous service request is handled.

This gives the repository a recursive retention relation:

> **a mechanism for preserving payload can itself depend on smaller retained states or modes that organize preservation work.**

That is an engineering reconstruction from documented counter/timer/mode roles, not a philosophical claim that those control states are an archive or memory in the cultural sense.

---

## Retention mechanism

The physical payload-retention regime remains deadline-driven reconstruction. What changes is the control partition.

### External-row-address regime

A system that must present each refresh row externally needs external machinery to:

1. know which row is next;
2. place that row on the multiplexed address pins;
3. issue the refresh timing sequence often enough;
4. repeat until all rows have been covered inside the retention deadline.

### CAS-before-RAS internal-address regime

In the bounded TI design:

1. external logic still causes the CAS-before-RAS refresh request;
2. ordinary external address inputs are ignored for that refresh;
3. the on-chip counter supplies the refresh row;
4. the DRAM performs the row-level sense/restoration operation;
5. successive refresh requests progress the internal count.

The maintenance obligation survives while one part of its control path migrates across the package boundary.

### Early autonomous-self-refresh regime

In the bounded 1981–1983 prior-art slice:

1. external logic establishes a self-refresh condition/regime;
2. an on-chip timer determines later refresh recurrence;
3. an on-chip refresh counter supplies successive maintenance addresses;
4. refresh-control/arbitration logic coordinates the maintenance operation;
5. ordinary service may be delayed, blocked, or arbitrated depending on the design.

This is a historical alternative control partition, not a claim about every early DRAM.

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

CBR, early self-refresh, and later SDRAM AUTO/SELF REFRESH create bounded cases in which:

> **service addressing and maintenance addressing share row-selection infrastructure but can have different address sources, scheduling authorities, and arbitration rules.**

The same physical row can be selected for an application access using an external address or selected for retention work using internally generated refresh addressing.

---

## Read / write / refresh semantics

This case does not redefine DRAM read/write physics. Its contribution is the additional operation classes and control regimes.

### RAS-only refresh

External row selection can be strobed without an ordinary data-return transaction.

### CAS-before-RAS refresh

The strobe ordering requests refresh behavior and selects the internal refresh-address path rather than the ordinary external row-address path.

### Hidden refresh

A refresh sequence can occur while an already produced output value remains valid under the specified timing conditions.

This means:

> **visible output continuity does not prove internal quiescence.**

The system can be actively maintaining retained state while one interface appears unchanged.

### Early self-refresh

A self-refresh condition delegates repeated refresh timing and row progression to internal machinery. Depending on the implementation, normal access may be blocked or explicitly arbitrated while maintenance is active.

This means:

> **internal recurrence != transparent concurrent service.**

### SDRAM AUTO REFRESH

A command explicitly requests one refresh operation while the DRAM supplies the internal refresh address. The command's nonpersistent nature keeps recurrence as an external responsibility.

### SDRAM SELF REFRESH

A mode-entry command establishes a regime in which recurring refresh clocking proceeds internally until exit. The product documentation therefore distinguishes a one-shot externally repeated request from a retained maintenance regime.

---

## Maintenance and labor

The case should not be narrated as `refresh became automatic`.

A more accurate decomposition is:

| Function | TI bounded CBR locus | Early self-refresh literature | Micron 1999 AUTO REFRESH | Micron 1999 SELF REFRESH steady state |
| --- | --- | --- | --- | --- |
| physical need to refresh before deadline | array/device physics | array/device physics | array/device physics | array/device physics |
| recurring cadence authority | external processor/controller | internal timer within entered self-refresh regime | external system/controller | internal clocking after external mode entry |
| request / mode establishment | CAS-before-RAS timing sequence | external establishment of self-refresh condition; exact interface design-specific | AUTO REFRESH command each time | SELF REFRESH entry + maintained CKE condition |
| next refresh-row enumeration | on-chip refresh counter | on-chip refresh counter in bounded examples | on-chip refresh controller/counter | on-chip refresh controller/counter |
| access conflict policy | ordinary controller/device timing | explicit arbitration / possible access lockout in bounded evidence | command/timing rules | normal access unavailable until exit/handoff |
| row sensing / restoration | on-chip memory circuitry | on-chip memory circuitry | on-chip memory circuitry | on-chip memory circuitry |
| transition back to ordinary operation | not this mode distinction | implementation-specific | ordinary command regime | external clock stabilization + `tXSR` handoff |

The relevant historical differences are **alternative distributions of retention work and authority**, not disappearance of work and not necessarily one linear sequence of offload.

This is closely related to the repository's maintenance-visibility audit: automation can remove a responsibility from one interface or board-level circuit while making another internal state/path or mode more important.

---

## Failure / forgetting modes

The mechanism distinguishes several failures that would all look like `refresh failure` at too high a level.

### Missed deadline

The responsible scheduler causes too few refresh cycles before the retention interval expires. Depending on mode, that scheduler may be external or internal.

### Wrong operation selection / wrong mode

The control sequence fails to invoke the intended refresh path or maintenance mode.

### Enumeration failure

The internal counter/address path fails to cover the required rows correctly.

### Internal cadence failure

Within a documented self-refresh regime, internal recurring timing fails to cause the required refresh work.

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

### E — internalized refresh addressing ≠ autonomous refresh scheduling

The TI patent directly says the processor or memory controller controls the frequency of the CAS-before-RAS sequence. Micron's 1999 AUTO REFRESH similarly uses internal addressing while requiring each refresh command externally.

The early-prior-art deepening adds the complementary witness: by 1981–1983, self-refresh designs also existed in which an internal timer and counter supplied recurring refresh work inside an entered regime.

Therefore `internal refresh address` and `internal refresh schedule` are demonstrably different properties, but the historical design space already included both combinations in the early 1980s.

This gives a cleaner vocabulary for future cases:

```text
refresh deadline
refresh scheduler / cadence authority
refresh trigger or mode-entry mechanism
refresh enumerator / coverage state
address-source authority
access/maintenance arbitration
refresh executor / restorer
transition / handoff semantics
```

Do not collapse them back into one word, `refresh`.

### E — no single linear offload chronology

The source set blocks a tempting teleology:

```text
external everything
    -> internal row counter
    -> much later internal timer
```

A better historical reconstruction is that different designs explored different control partitions, some with external cadence and internal addressing and some already with internally timed self-refresh.

Historical coexistence does not itself establish influence or descent among those designs.

### E — hidden maintenance is observer-relative

Hidden refresh can maintain an output while refresh cycles proceed. Self-refresh can remove recurring host command traffic while internal cycles continue. In both cases the operation is hidden only relative to particular interfaces or observers. It remains visible to timing, power, control, or device-level analysis.

### E — maintenance machinery can have retention state

The refresh counter itself must carry enough sequential state between refresh requests to choose successive rows. In internally timed self-refresh, timer/mode/arbitration state additionally organizes when that counter is exercised and when normal access may proceed.

The earlier counter-initialization deepening adds a horizon boundary: the TI disclosed phase is initialized at power-on rather than preserved as a durable cross-power checkpoint. The early self-refresh evidence adds a control decomposition, while the Micron evidence adds a clean later authority boundary: the same row refresh counter participates in both AUTO REFRESH and SELF REFRESH even though cadence authority differs by mode.

> **maintenance-control-state location != maintenance-authority location != maintenance-control-state persistence horizon.**

### E — autonomy is regime-scoped and power-dependent

Early self-refresh and Micron's later SELF REFRESH support autonomous refresh recurrence only within an established maintenance regime and while the device remains sufficiently powered.

Thus:

```text
internal recurring refresh
    != globally autonomous memory system
    != unpowered nonvolatile retention
```

---

## Philosophical / media-theoretical interpretation

### I — persistence can involve relocation of responsibility

This case sharpens the project's maintenance thesis without turning it into a metaphor. The relevant technical fact is not merely that `DRAM needs refresh`; that was already established. The new fact is that the functions making refresh possible can migrate across an interface, coexist in alternative partitions, or switch authority by mode while the underlying physical obligation remains.

This makes `where is the maintenance?`, `who currently initiates it?`, and `what infrastructure remains powered?` as important as `is there maintenance?`

### I — invisibility is a relation between mechanism and observer

Hidden refresh is a concrete engineering example in which continued output availability can coexist with ongoing reconstruction beneath that interface. Self-refresh adds another: recurring maintenance may continue without recurring host commands or external refresh clocks even though power and mode conditions still sustain the device.

These observations do not by themselves establish Heideggerian `Bestand`, Stieglerian tertiary retention, or a general philosophy of technological autonomy.

---

## Functional analogies and limits

### A/H/P — bounded early-1980s comparison

The early prior art gives a controlled counterexample to one-period/one-architecture storytelling:

```text
1981 self-refresh literature
    internal timer + internal counter + arbitration

TI 1984-filed CBR-counter design
    internal row enumeration + external request cadence
```

The useful conclusion is **coexisting control partitions**, not a genealogy and not a claim that either architecture universally characterized its period.

### A/H/P — bounded later comparison to SDRAM SELF REFRESH

Micron's November-1999 product documentation remains valuable because it places AUTO REFRESH and SELF REFRESH side by side under one synchronous product interface.

The bounded comparison is:

```text
early self-refresh literature
    internal recurrence within a self-refresh regime
    internal row enumeration
    historical interface design-specific

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

Moving row enumeration or recurring cadence from board/controller logic into the DRAM can be described functionally as an offload of maintenance-control functions.

`Offload` is a modern analytical term here, not a recovered early-1980s or 1999 actor category.

### A — analogy to HDFS scanner progress state

Case 83's HDFS scanner cursor is also retained control state that distributes maintenance work across a payload population. The analogy stops at that function. HDFS checkpoints traversal position so a process/restart can resume without replaying the entire scan; the TI DRAM embodiment initializes the cyclic refresh phase at power-on, and DRAM self-refresh keeps regime-local timing/coverage state only while the powered retention episode exists. Their persistence horizons and authority semantics are therefore different.

> **maintenance-control state != one universal checkpoint contract.**

This is a functional comparison, not a DRAM-to-HDFS genealogy.

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

> **the obligation and the machinery that discharges it must be analyzed separately, and the machinery historically had multiple competing control partitions rather than one simple migration path.**

A compact comparison is:

```text
Case 03
    why refresh is required
    deadline-driven reconstruction

Case 09 — early self-refresh literature
    internal timer can own recurring cadence
    internal counter can own row enumeration
    arbitration/service semantics remain a separate problem

Case 09 — TI CBR
    internal counter supplies maintenance address
    external controller still supplies recurring request cadence

Case 09 — 1999 SDRAM successor
    AUTO REFRESH: external repeated cadence + internal addressing
    SELF REFRESH: internal recurrence after explicit mode entry
    same product exposes both authority regimes
```

This produces six particularly useful controls:

1. **refresh obligation ≠ refresh-address-generation locus**;
2. **internalized refresh addressing ≠ autonomous refresh scheduling**;
3. **internal cadence authority ≠ transparent concurrent access**;
4. **hidden refresh ≠ absence of retention work**;
5. **shared maintenance-control state ≠ shared scheduling authority**;
6. **self-refresh ≠ nonvolatility or absence of power dependence**.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| TMS4256/TMS4257 documentation specifies a 4 ms refresh period | H/P | TI period data book; later revision facsimile directly inspected |
| TMS4256/TMS4257 supports RAS-only, CAS-before-RAS, and hidden refresh | H/P | TI period data book + direct later-revision facsimile |
| CBR refresh ignores the external address and generates the refresh address internally | H/P | TI manufacturer documentation |
| TI patented an on-chip refresh counter activated by CAS-before-RAS | H/P | US4653030A abstract/summary/figures |
| TI explicitly named TMS4164 as a commercial device lacking the patent's refresh counter | H/P | US4653030A description |
| The bounded TI patent leaves refresh-trigger cadence with an external processor/controller | H/P | US4653030A refresh-cycle discussion |
| A Reese et al. DRAM self-refresh paper appeared in IEEE JSSC in 1981, vol. 16 no. 5, pp. 479–487, DOI `10.1109/JSSC.1981.1051626` | H/P | strong bibliographic record; full paper not directly page-inspected in this slice |
| The indexed Reese abstract describes an on-chip timer, arbiter, and refresh counter | H/P | abstract-level evidence; detailed circuit claims intentionally bounded |
| Yamada et al. published a 64-Kbit DRAM `auto/self refresh` paper in January 1983, DOI `10.1002/ECJA.4400660114` | H/P | strong bibliographic record; full article not directly page-inspected here |
| Later Mitsubishi patents explicitly attribute a timer + refresh-counter + address-multiplexer architecture to the 1983 Yamada paper | H/P | later manufacturer prior-art reconstruction |
| Internally timed self-refresh therefore existed in early-1980s DRAM technical literature before the 1999 SDRAM witness | H/P | strong at publication/mechanism-class level; no priority or genealogy claim |
| TI's disclosed refresh counter starts at zero at power-on and increments on CBR refresh cycles | H/P | US4653030A counter-stage description |
| Motorola documents a product-level CBR refresh-counter test using internal row selection and controlled data writes | H/P | 1989 *Motorola Memory Data* product section |
| The Motorola counter test requires initialization cycles and uses 512 cycles to exercise the documented row set | H/P | Motorola counter-test procedure |
| Micron Rev. 11/99 calls SDRAM AUTO REFRESH analogous to conventional CBR refresh | H/P | manufacturer-authored 64 Mb SDRAM datasheet, printed p. 13 via page-preserving mirror |
| Micron AUTO REFRESH is nonpersistent and uses internally generated refresh addressing | H/P | same 1999 page |
| Micron SELF REFRESH retains data without external clocking and uses internal clocking for recurring refresh | H/P | same 1999 page |
| AUTO REFRESH and SELF REFRESH share the row refresh counter in the bounded Micron product | H/P | same 1999 page |
| SELF REFRESH exit includes a `tXSR` handoff because internal refresh may still be in progress | H/P | same 1999 page |
| Internal row enumeration proves internal recurring scheduling | X | directly rejected by TI CBR and Micron AUTO REFRESH control partitions |
| Internal recurring scheduling proves transparent concurrent normal access | X | rejected by early self-refresh arbitration/access-lockout evidence |
| Self-refresh proves unpowered retention / nonvolatility | X | rejected: dynamic payload still depends on powered periodic restoration |
| Sharing one row refresh counter proves identical maintenance authority | X | directly rejected by AUTO vs SELF REFRESH mode distinction |
| Motorola's product counter is proven to use TI's power-on-zero circuit | X | unsupported cross-vendor implementation identity |
| A successful counter test permanently certifies future refresh correctness | X | bounded diagnostic event ≠ continuing scheduler/coverage correctness |
| Maintenance-control state must persist across power loss whenever it helps retain payload | X/E | TI's disclosed counter is intentionally initialized at power-on; persistence horizon is regime-specific |
| Moving refresh enumeration on-chip removes the periodic retention obligation | X | contradicted by the same source set |
| `self refresh circuitry` in the TI patent automatically means autonomous self-refresh | X | rejected by TI's external-trigger statement and early/later distinct self-refresh mechanisms |
| 1999 Micron SELF REFRESH is the first autonomous DRAM self-refresh | X | contradicted by 1981–1983 publication evidence |
| The early publications, TI CBR patent, and Micron SDRAM form a demonstrated direct genealogy | X | unsupported historical continuity |
| The TI patent is proven to be the exact TMS4256 circuit | X | unsupported product-identity leap |
| Micron's 1999 datasheet proves JEDEC invention/standardization chronology | X | product evidence ≠ normative genealogy |
| Retention infrastructure can itself contain retained control state | E | bounded reconstruction from refresh-counter, timer, arbitration, and mode roles |

---

## Related repositories

### `tmzncty/computing-archaeology`

Fresh related-repository searches for `CAS-before-RAS` found no dedicated case to reuse. A broad history of quasi-static RAM, early self-refresh prototypes/products, ISSCC/JSSC publication genealogy, DRAM refresh counters/timers, SDRAM standardization, test modes, oscillators, and controller integration still belongs there:

<https://github.com/tmzncty/computing-archaeology>

This repository should keep only the retention-specific comparison about the **locus, authority, persistence horizon, and visibility of maintenance work**.

### `tmzncty/problem-history`

Use its anti-anachronism discipline for the phrase `self refresh`. Reese/Yamada early self-refresh, TI's patent title phrase, and Micron's 1999 mode name must each be interpreted through the mechanism actually described rather than treated as timelessly identical vocabulary.

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
