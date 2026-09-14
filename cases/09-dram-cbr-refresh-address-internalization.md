# CAS-before-RAS DRAM Refresh: Moving Refresh Addressing On-Chip

## Status

**`grounded`** — bounded to Texas Instruments' TMS4164 contrast, TMS4256/TMS4257 refresh behavior, TI's 1984-filed on-chip refresh-counter design, and a late-1999 Micron SDRAM successor comparison separating externally repeated AUTO REFRESH from device-clocked SELF REFRESH.

Grounding record: [`../evidence/09-ti-cbr-refresh-address-grounding.md`](../evidence/09-ti-cbr-refresh-address-grounding.md).

Deepening record: [`../evidence/09-dram-refresh-counter-initialization-test-deepening.md`](../evidence/09-dram-refresh-counter-initialization-test-deepening.md).

SDRAM control-boundary deepening: [`../evidence/09-micron-1999-sdram-auto-vs-self-refresh-deepening.md`](../evidence/09-micron-1999-sdram-auto-vs-self-refresh-deepening.md).

---

## Scope

- **Object / system:** a bounded transition from externally enumerated DRAM refresh rows toward CAS-before-RAS refresh with an on-chip refresh-address counter, followed by a bounded late-1999 SDRAM comparison in which AUTO REFRESH and SELF REFRESH place recurring refresh cadence under different authorities.
- **Date range:** 1983–1986 for the central commercial/device evidence; a 1984-filed TI patent supplies the mechanism-level design account. A January 1988 revision of the TMS4256/TMS4257 sheet was directly inspected only as a page-stable facsimile witness to the same documented device-family behavior. Micron's November-1999 64 Mb SDRAM documentation is used only as a later product-level successor witness for AUTO REFRESH versus SELF REFRESH control partition.
- **Primary comparison:** TMS4164 as an explicitly named commercial device lacking the patented refresh counter versus the TMS4256/TMS4257 family's documented CAS-before-RAS and hidden-refresh behavior; the later Micron SDRAM comparison asks what changes when recurring refresh clocking, not only refresh-row enumeration, can move on-chip after an explicit mode transition.
- **Question:** what changes when the DRAM still has a periodic retention deadline but parts of the work required to cover all rows move from system logic onto the memory chip?

This is **not** a general history of DRAM evolution. The SDRAM material is a bounded AUTO REFRESH / SELF REFRESH control comparison, not a JEDEC genealogy or a full SDRAM history. DDR per-bank refresh, temperature-compensated refresh, retention-aware refresh research, and broad controller/test-mode history remain outside this case unless needed for a later retention comparison.

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

That account is correct but leaves `refresh machinery` too monolithic. The TI evidence lets us decompose it:

```text
refresh deadline
refresh-cycle scheduling
refresh trigger / command sequence
next-row enumeration
row selection
sense / restoration
```

The Micron SDRAM successor evidence adds another distinction:

```text
maintenance mode entry / exit
    != recurring refresh-cadence authority
```

The case matters because these functions need not live at the same layer or under the same authority.

---

## Historical vocabulary

The period sources use:

- `refresh`;
- `RAS-only refresh`;
- `CAS-before-RAS refresh`;
- `hidden refresh`;
- `refresh address`;
- `refresh counter`;
- `self refresh circuitry` in the title and description of TI's US4653030A;
- `AUTO REFRESH` and `SELF REFRESH` in Micron's 1999 SDRAM documentation.

### Terminology warning

`Self refresh` in the 1984-filed TI patent must be read from its disclosed mechanism, not from later DRAM expectations. The patent's refresh counter is activated by a CAS-before-RAS sequence and explicitly says the processor or memory controller external to the memory device controls how often that sequence occurs.

Micron's 1999 `SELF REFRESH`, by contrast, documents a mode in which the SDRAM supplies internal clocking and performs recurring refresh cycles after externally requested entry.

Therefore:

> **same historical phrase `self refresh` ≠ same distribution of retention work.**

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

This is the key historical fact for the case. The physical refresh obligation did not disappear; the chip acquired machinery that can choose the row to refresh without the system presenting that row through the ordinary address pins.

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

### H/P — the bounded counter does not schedule itself

The most important limit is explicit in the patent. For a 4 ms maximum refresh period and 256 rows, it says the CAS-before-RAS sequence should occur on average every 15.6 µs and that this is controlled by the processor or memory controller external to the memory device.

So the period primary source itself blocks the shortcut:

```text
on-chip refresh counter
    !=
fully autonomous refresh scheduler
```

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

The existing Case 09 split between external scheduling and internal row enumeration now has an operational witness: Motorola supplies a procedure specifically for checking the counter's traversal behavior.

Thus:

```text
enough refresh requests
    !=
verified traversal of all required rows
```

and conversely a correctly progressing counter does not prove that external logic met the refresh deadline.

The counter-test result is also event-bounded evidence, not a permanent certificate of future refresh correctness.

---

## 1999 SDRAM AUTO REFRESH vs SELF REFRESH control-boundary deepening

Detailed record: [`../evidence/09-micron-1999-sdram-auto-vs-self-refresh-deepening.md`](../evidence/09-micron-1999-sdram-auto-vs-self-refresh-deepening.md).

### H/P — AUTO REFRESH internalizes addressing without internalizing repeated-command cadence

Micron's November-1999 64 Mb SDRAM datasheet (`MT48LC16M4A2 / MT48LC8M8A2 / MT48LC4M16A2`, `Rev. 11/99`) explicitly calls `AUTO REFRESH` analogous to conventional CAS-before-RAS refresh.

The same paragraph says the command is **nonpersistent** and must be issued each time refresh is required. The refresh address is generated internally; ordinary address bits are `Don't Care` during the command. For the documented family, 4,096 AUTO REFRESH cycles are required within 64 ms.

So this later product preserves the core Case-09 split:

```text
internal refresh-row enumeration
    !=
internal recurring refresh-cadence authority
```

### H/P — SELF REFRESH additionally internalizes recurring clocking after entry

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

This is product-level evidence for internal scheduling within the entered self-refresh regime. It is not a claim that the DRAM is globally independent of system power, mode control, or exit timing.

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

There are two different retained-state layers in this case.

### Payload state

As in the grounded DRAM case, the memory array holds volatile dynamic state that must be periodically reconstructed.

### Maintenance-control state

The refresh counter has a current count that determines which row will be selected on a later refresh request. This count is not application payload and does not preserve user history. It is nevertheless retained control state that helps ensure maintenance is distributed across the row set.

In the Micron SDRAM successor comparison, the entered SELF REFRESH mode is another control condition: it changes the source of recurring refresh clocking without turning that condition into application history.

This gives the repository a recursive retention relation:

> **a mechanism for preserving payload can itself depend on smaller retained states or modes that organize preservation work.**

That is an engineering reconstruction from the documented counter/mode roles, not a philosophical claim that the counter or mode is an archive or memory in the cultural sense.

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

CAS-before-RAS and later SDRAM AUTO/SELF REFRESH therefore create bounded cases in which:

> **service addressing and maintenance addressing share row-selection infrastructure but can have different address sources and different scheduling authorities.**

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

### SDRAM AUTO REFRESH

A command explicitly requests one refresh operation while the DRAM supplies the internal refresh address. The command's nonpersistent nature keeps recurrence as an external responsibility.

### SDRAM SELF REFRESH

A mode-entry command establishes a regime in which recurring refresh clocking proceeds internally until exit. The product documentation therefore distinguishes a one-shot externally repeated request from a retained maintenance regime.

---

## Maintenance and labor

The case should not be narrated as `refresh became automatic`.

A more accurate decomposition is:

| Function | TI bounded CBR locus | Micron 1999 AUTO REFRESH | Micron 1999 SELF REFRESH steady state |
| --- | --- | --- | --- |
| physical need to refresh before deadline | array/device physics | array/device physics | array/device physics |
| recurring cadence authority | external processor/controller | external system/controller | internal clocking after external mode entry |
| request / mode establishment | CAS-before-RAS timing sequence | AUTO REFRESH command each time | SELF REFRESH entry + maintained CKE condition |
| next refresh-row enumeration | on-chip refresh counter | on-chip refresh controller/counter | on-chip refresh controller/counter |
| row sensing / restoration | on-chip memory circuitry | on-chip memory circuitry | on-chip memory circuitry |
| transition back to ordinary operation | not this mode distinction | ordinary command regime | external clock stabilization + `tXSR` handoff |

The relevant historical changes are **redistributions of retention work and authority**, not disappearance of work.

This is closely related to the repository's maintenance-visibility audit: automation can remove a responsibility from one interface or board-level circuit while making another internal state/path or mode more important.

---

## Failure / forgetting modes

The mechanism distinguishes several failures that would all look like `refresh failure` at too high a level.

### Missed deadline

External logic causes too few refresh cycles before the retention interval expires in a regime where cadence remains external.

### Wrong operation selection

The control sequence fails to invoke the intended refresh path or maintenance mode.

### Enumeration failure

The internal counter/address path fails to cover the required rows correctly.

### Internal cadence failure

Within a documented self-refresh regime, internal recurring clocking fails to cause the required refresh work.

### Reconstruction-path failure

The correct row is selected, but sensing/restoration does not correctly reconstruct its logical state.

### Handoff failure

A system violates entry/exit timing or assumes normal service before the documented transition has completed.

These are not asserted as specific measured silicon failure rates. They are architecture-level failure classes implied by the sourced partition of functions.

---

## Engineering reconstruction

### E — refresh obligation ≠ refresh-address-generation locus

Case 03 links the deadline to physical charge leakage. Case 09 shows that the place where the next row number is generated is a separate design choice.

The retention requirement can remain stable while maintenance responsibility moves.

### E — internalized refresh addressing ≠ autonomous refresh scheduling

The TI patent directly says the processor or memory controller controls the frequency of the CAS-before-RAS sequence. Micron's 1999 AUTO REFRESH similarly uses internal addressing while requiring each refresh command externally; only SELF REFRESH adds internal recurring clocking after entry.

Therefore `internal refresh address` and `internal refresh schedule` are demonstrably different properties even within closely related refresh regimes.

This gives a cleaner vocabulary for future cases:

```text
refresh deadline
refresh scheduler / cadence authority
refresh trigger or mode-entry mechanism
refresh enumerator
refresh executor / restorer
transition / handoff semantics
```

Do not collapse them back into one word, `refresh`.

### E — hidden maintenance is observer-relative

Hidden refresh can maintain an output while refresh cycles proceed. The operation is hidden only relative to a particular observation at the interface. It remains visible to timing, power, control, and device-level analysis.

### E — maintenance machinery can have retention state

The refresh counter itself must carry enough sequential state between refresh requests to choose successive rows. This is not payload retention, but it is constitutive control state for the bounded maintenance scheme.

The earlier deepening record adds a horizon boundary: the TI disclosed phase is initialized at power-on rather than preserved as a durable cross-power checkpoint. The Micron evidence adds an authority boundary: the same row refresh counter participates in both AUTO REFRESH and SELF REFRESH even though cadence authority differs by mode.

> **maintenance-control-state location != maintenance-authority location.**

### E — autonomy is regime-scoped

Micron's SELF REFRESH evidence supports autonomous refresh recurrence only after explicit entry and only while the required mode condition is maintained. Entry and exit still belong to a system/device handoff.

Thus:

```text
internal recurring refresh
    != globally autonomous memory system
```

---

## Philosophical / media-theoretical interpretation

### I — persistence can involve relocation of responsibility

This case sharpens the project's maintenance thesis without turning it into a metaphor. The relevant technical fact is not merely that `DRAM needs refresh`; that was already established. The new fact is that the functions making refresh possible can migrate across an interface or switch authority by mode while the underlying physical obligation remains.

This makes `where is the maintenance?` and `who currently initiates it?` as important as `is there maintenance?`

### I — invisibility is a relation between mechanism and observer

Hidden refresh is a concrete engineering example in which continued output availability can coexist with ongoing reconstruction beneath that interface. SELF REFRESH adds a second bounded example: recurring maintenance may continue without external clocking even though the system still controls entry and exit conditions.

These observations do not by themselves establish Heideggerian `Bestand`, Stieglerian tertiary retention, or a general philosophy of technological autonomy.

---

## Functional analogies and limits

### A/H/P — bounded later comparison to SDRAM SELF REFRESH

Micron's November-1999 product documentation provides the later comparison that the earlier Case-09 text had intentionally left open.

It does **not** create a genealogy. The bounded comparison is:

```text
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

The useful conclusion is a control-locus distinction, not a claim that one implementation descends directly from the other.

### A — analogy to controller offload

Moving row enumeration or recurring cadence from board/controller logic into the DRAM can be described functionally as an offload of maintenance-control functions.

`Offload` is a modern analytical term here, not a recovered 1984 or 1999 actor category.

### A — analogy to HDFS scanner progress state

Case 83's HDFS scanner cursor is also retained control state that distributes maintenance work across a payload population. The analogy stops at that function. HDFS checkpoints traversal position so a process/restart can resume without replaying the entire scan; the TI DRAM embodiment initializes the cyclic refresh phase at power-on, and the Micron SDRAM evidence shows a mode-local handoff of cadence authority. Their persistence horizons and authority semantics are therefore different.

> **maintenance-control state != one universal checkpoint contract.**

This is a functional comparison, not a DRAM-to-HDFS genealogy.

### Limit — patent mechanism ≠ exact TMS4256 implementation

US4653030A and the TMS4256/TMS4257 datasheet are complementary evidence classes. The patent provides manufacturer-primary mechanism detail; the commercial datasheet provides product-family behavior. The patent does not identify its preferred embodiment as the exact TMS4256/TMS4257 circuit.

### Limit — Micron product documentation ≠ JEDEC genealogy

The 1999 Micron datasheet establishes a named-product control boundary. It does not establish when JEDEC first standardized SELF REFRESH, which vendor invented the feature, the first commercial shipment, or the exact internal oscillator topology.

### Limit — no general DRAM generation history

Density, process, package, page/nibble modes, broad controller IC history, DDR per-bank refresh, ECC, and later retention-aware refresh policy are outside this slice unless they alter a future retention comparison.

---

## Cross-case result

Case 03 established:

> **time can create a retention obligation even without useful access.**

Case 09 adds:

> **the obligation and the machinery that discharges it must be analyzed separately.**

A compact comparison is:

```text
Case 03
    why refresh is required
    deadline-driven reconstruction

Case 09 — 1980s CBR
    who supplies the maintenance address
    who triggers the maintenance cycle
    which part of refresh moves across the interface

Case 09 — 1999 SDRAM successor
    whether recurring cadence remains an external repeated obligation
    or becomes internal within an entered maintenance regime
```

This produces four particularly useful controls:

1. **refresh obligation ≠ refresh-address-generation locus**;
2. **internalized refresh addressing ≠ autonomous refresh scheduling**;
3. **hidden refresh ≠ absence of retention work**;
4. **shared maintenance-control state ≠ shared scheduling authority**.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| TMS4256/TMS4257 documentation specifies a 4 ms refresh period | H/P | TI period data book; later revision facsimile directly inspected |
| TMS4256/TMS4257 supports RAS-only, CAS-before-RAS, and hidden refresh | H/P | TI period data book + direct later-revision facsimile |
| CBR refresh ignores the external address and generates the refresh address internally | H/P | TI manufacturer documentation |
| TI patented an on-chip refresh counter activated by CAS-before-RAS | H/P | US4653030A abstract/summary/figures |
| TI explicitly named TMS4164 as a commercial device lacking the patent's refresh counter | H/P | US4653030A description |
| The bounded patent still leaves refresh-trigger cadence with an external processor/controller | H/P | US4653030A refresh-cycle discussion |
| TI's disclosed refresh counter starts at zero at power-on and increments on CBR refresh cycles | H/P | US4653030A counter-stage description |
| Motorola documents a product-level CBR refresh-counter test using internal row selection and controlled data writes | H/P | 1989 *Motorola Memory Data* product section |
| The Motorola counter test requires initialization cycles and uses 512 cycles to exercise the documented row set | H/P | Motorola counter-test procedure |
| Micron Rev. 11/99 calls SDRAM AUTO REFRESH analogous to conventional CBR refresh | H/P | manufacturer-authored 64 Mb SDRAM datasheet, printed p. 13 via page-preserving mirror |
| Micron AUTO REFRESH is nonpersistent and uses internally generated refresh addressing | H/P | same 1999 page |
| Micron SELF REFRESH retains data without external clocking and uses internal clocking for recurring refresh | H/P | same 1999 page |
| AUTO REFRESH and SELF REFRESH share the row refresh counter in the bounded Micron product | H/P | same 1999 page |
| SELF REFRESH exit includes a `tXSR` handoff because internal refresh may still be in progress | H/P | same 1999 page |
| Internal row enumeration proves internal recurring scheduling | X | directly rejected by AUTO REFRESH control partition |
| Sharing one row refresh counter proves identical maintenance authority | X | directly rejected by AUTO vs SELF REFRESH mode distinction |
| Motorola's product counter is proven to use TI's power-on-zero circuit | X | unsupported cross-vendor implementation identity |
| A successful counter test permanently certifies future refresh correctness | X | bounded diagnostic event ≠ continuing scheduler/coverage correctness |
| Maintenance-control state must persist across power loss whenever it helps retain payload | X/E | TI's disclosed counter is intentionally initialized at power-on; persistence horizon is regime-specific |
| Moving refresh enumeration on-chip removes the periodic retention obligation | X | contradicted by the same source set |
| `self refresh circuitry` in the TI patent automatically means later autonomous self-refresh | X | rejected by TI's external-trigger statement and Micron's distinct later product semantics |
| The TI patent is proven to be the exact TMS4256 circuit | X | unsupported product-identity leap |
| Micron's 1999 datasheet proves JEDEC invention/standardization chronology | X | product evidence ≠ normative genealogy |
| Retention infrastructure can itself contain retained control state | E | bounded reconstruction from refresh-counter and mode roles |

---

## Related repositories

### `tmzncty/computing-archaeology`

Fresh related-repository searches for `TMS4256`, `CAS-before-RAS`, and `SDRAM self refresh` found no dedicated case to reuse. A broad DRAM refresh-counter, SDRAM-standardization, test-mode, oscillator, and product-history account still belongs there:

<https://github.com/tmzncty/computing-archaeology>

This repository should keep only the retention-specific comparison about the **locus, authority, and visibility of maintenance work**.

### `tmzncty/problem-history`

Use its anti-anachronism discipline for the phrase `self refresh`. The TI patent's period phrase and Micron's 1999 mode name must each be interpreted through the mechanism actually described rather than treated as timelessly identical vocabulary.

---

## Sources

1. Texas Instruments, *MOS Memory Data Book 1986*, TMS4256/TMS4257 device section, revision header `MAY 1983—REVISED NOVEMBER 1985`: <https://bitsavers.org/components/ti/_dataBooks/1986_SMYD006_TI_MOS_Memory_Data_Book.pdf>.
2. Texas Instruments, `TMS4256, TMS4257 — 262,144-BIT DYNAMIC RANDOM-ACCESS MEMORIES`, standalone page-preserving copy, revision header `MAY 1983—REVISED JANUARY 1988`, directly inspected printed pp. 4-3 and 4-5: <https://www.ardent-tool.com/datasheets/TI_TMS4256_7.pdf>.
3. Tadashi Tachibana, Chitranjan N. Reddy, Ngai H. Hong, `Self refresh circuitry for dynamic memory`, US4653030A, filed 31 August 1984, assigned to Texas Instruments: <https://patents.google.com/patent/US4653030A/en>.
4. Texas Instruments, *MOS Memory Data Book 1984*, TMS4164 family documentation: <https://vintage-computer-books.netlify.app/Texas%20Instruments%20-%20MOS%20Memory%20Data%20Book%20-%201984.pdf>.
5. Motorola, *Memory Data*, 1989, MCM514256A / MCM51L4256A product section, especially `REFRESH CYCLES` and `CAS BEFORE RAS REFRESH COUNTER TEST`: <https://www.bitsavers.org/components/motorola/_dataBooks/1989_DL113r6_Motorola_Memory_Data.pdf>.
6. Micron Technology, `MT48LC16M4A2 / MT48LC8M8A2 / MT48LC4M16A2` 64 Mb SDRAM, `Rev. 11/99`, printed p. 13, manufacturer-authored content preserved by a page-stable mirror: <https://www.alldatasheet.fr/html-pdf/228369/MICRON/MT48LC4M16A2/2945/13/MT48LC4M16A2.html>.
7. Micron Technology, same 64 Mb SDRAM family, `Rev. V 09/14`, later manufacturer-authored continuity witness preserved as PDF by Mouser, especially p. 33 and SELF REFRESH timing material: <https://www.mouser.com/datasheet/2/671/micts06234_1-2290735.pdf>.
