# CAS-before-RAS DRAM Refresh: Moving Refresh Addressing On-Chip

## Status

**`grounded`** — bounded to Texas Instruments' TMS4164 contrast, TMS4256/TMS4257 refresh behavior, and TI's 1984-filed on-chip refresh-counter design.

Grounding record: [`../evidence/09-ti-cbr-refresh-address-grounding.md`](../evidence/09-ti-cbr-refresh-address-grounding.md).

---

## Scope

- **Object / system:** a bounded transition from externally enumerated DRAM refresh rows toward CAS-before-RAS refresh with an on-chip refresh-address counter.
- **Date range:** 1983–1986 for the central commercial/device evidence; a 1984-filed TI patent supplies the mechanism-level design account. A January 1988 revision of the TMS4256/TMS4257 sheet was directly inspected only as a page-stable facsimile witness to the same documented device-family behavior.
- **Primary comparison:** TMS4164 as an explicitly named commercial device lacking the patented refresh counter versus the TMS4256/TMS4257 family's documented CAS-before-RAS and hidden-refresh behavior.
- **Question:** what changes when the DRAM still has a periodic retention deadline but part of the work required to cover all rows moves from system logic onto the memory chip?

This is **not** a general history of DRAM evolution. It does not cover SDRAM auto-refresh commands, DDR per-bank refresh, temperature-compensated refresh, retention-aware refresh research, or all meanings of `self refresh`.

Case 03 already grounds the physical reason dynamic semiconductor state needs periodic reconstruction. This case starts one layer higher:

> **Does moving refresh-row enumeration on-chip change the retention mechanism, the maintenance obligation, or merely the location of some maintenance control?**

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

The case matters because these functions need not live at the same layer.

---

## Historical vocabulary

The period sources use:

- `refresh`;
- `RAS-only refresh`;
- `CAS-before-RAS refresh`;
- `hidden refresh`;
- `refresh address`;
- `refresh counter`;
- `self refresh circuitry` in the title and description of TI's US4653030A.

### Terminology warning

`Self refresh` in the 1984-filed patent must be read from its disclosed mechanism, not from later DRAM expectations. The patent's refresh counter is activated by a CAS-before-RAS sequence and explicitly says the processor or memory controller external to the memory device controls how often that sequence occurs.

Therefore:

> **historical `self refresh circuitry` in this source ≠ automatically autonomous oscillator/timer-driven self-refresh in later DRAM generations.**

The period term is historical record. Any later taxonomy is functional comparison only.

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

## Retained state

There are two different retained-state layers in this case.

### Payload state

As in the grounded DRAM case, the memory array holds volatile dynamic state that must be periodically reconstructed.

### Maintenance-control state

The refresh counter has a current count that determines which row will be selected on a later refresh request. This count is not application payload and does not preserve user history. It is nevertheless retained control state that helps ensure maintenance is distributed across the row set.

This gives the repository a recursive retention relation:

> **a mechanism for preserving payload can itself depend on a smaller retained state that organizes preservation work.**

That is an engineering reconstruction from the documented counter role, not a philosophical claim that the counter is an archive or memory in the cultural sense.

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

---

## Addressing and access geometry

This case shows that `addressing` itself has more than one role.

### Ordinary access address

The normal row/column address designates payload for read/write service.

### Maintenance address

The refresh row designates payload for reconstruction, not because software requested that data, but because the array must revisit it before a retention deadline.

CAS-before-RAS therefore creates a bounded case in which:

> **service addressing and maintenance addressing share row-selection infrastructure but can have different address sources.**

The same physical row can be selected for an application access using an external address or selected for retention work using an internally generated refresh address.

---

## Read / write / refresh semantics

This case does not redefine DRAM read/write physics. Its contribution is the additional operation class.

### RAS-only refresh

External row selection can be strobed without an ordinary data-return transaction.

### CAS-before-RAS refresh

The strobe ordering requests refresh behavior and selects the internal refresh-address path rather than the ordinary external row-address path.

### Hidden refresh

A refresh sequence can occur while an already produced output value remains valid under the specified timing conditions.

This means:

> **visible output continuity does not prove internal quiescence.**

The system can be actively maintaining retained state while one interface appears unchanged.

---

## Maintenance and labor

The case should not be narrated as `refresh became automatic`.

A more accurate decomposition is:

| Function | Bounded locus |
| --- | --- |
| physical need to refresh before the deadline | array/device physics |
| decision that refresh cycles must occur often enough | external processor/controller in the bounded patent |
| request encoding | CAS-before-RAS timing sequence |
| next refresh-row enumeration | on-chip refresh counter |
| row selection / sensing / restoration | on-chip memory circuitry |

The relevant historical change is **redistribution of retention work**, not disappearance of work.

This is closely related to the repository's maintenance-visibility audit: automation can remove a responsibility from one interface or board-level circuit while making another internal state/path more important.

---

## Failure / forgetting modes

The mechanism distinguishes several failures that would all look like `refresh failure` at too high a level.

### Missed deadline

External logic causes too few refresh cycles before the retention interval expires.

### Wrong operation selection

The control sequence fails to invoke the intended refresh path.

### Enumeration failure

The internal counter/address path fails to cover the required rows correctly.

### Reconstruction-path failure

The correct row is selected, but sensing/restoration does not correctly reconstruct its logical state.

These are not asserted as specific measured silicon failure rates. They are architecture-level failure classes implied by the sourced partition of functions.

---

## Engineering reconstruction

### E — refresh obligation ≠ refresh-address-generation locus

Case 03 links the deadline to physical charge leakage. Case 09 shows that the place where the next row number is generated is a separate design choice.

The retention requirement can remain stable while maintenance responsibility moves.

### E — internalized refresh addressing ≠ autonomous refresh scheduling

The TI patent directly says the processor or memory controller controls the frequency of the CAS-before-RAS sequence. Therefore `internal refresh address` and `internal refresh schedule` are different properties.

This gives a cleaner vocabulary for future cases:

```text
refresh deadline
refresh scheduler
refresh trigger
refresh enumerator
refresh executor / restorer
```

Do not collapse them back into one word, `refresh`.

### E — hidden maintenance is observer-relative

Hidden refresh can maintain an output while refresh cycles proceed. The operation is hidden only relative to a particular observation at the interface. It remains visible to timing, power, control, and device-level analysis.

### E — maintenance machinery can have retention state

The refresh counter itself must carry enough sequential state between refresh requests to choose successive rows. This is not payload retention, but it is constitutive control state for the bounded maintenance scheme.

---

## Philosophical / media-theoretical interpretation

### I — persistence can involve relocation of responsibility

This case sharpens the project's maintenance thesis without turning it into a metaphor. The relevant technical fact is not merely that `DRAM needs refresh`; that was already established. The new fact is that the functions making refresh possible can migrate across an interface while the underlying physical obligation remains.

This makes `where is the maintenance?` as important as `is there maintenance?`

### I — invisibility is a relation between mechanism and observer

Hidden refresh is a concrete engineering example in which continued output availability can coexist with ongoing reconstruction beneath that interface. It supports the project's bounded claim that invisible work must always be specified relative to an observer/layer.

This does not by itself establish Heideggerian `Bestand`, Stieglerian tertiary retention, or a general philosophy of technological invisibility.

---

## Functional analogies and limits

### A — analogy to later autonomous self-refresh

Later DRAM can internalize more of the scheduling/timing needed for self-refresh. That makes it useful as a future comparison.

But this bounded case does **not** establish that mechanism. The historical TI patent explicitly leaves refresh-request cadence with external processor/controller logic.

### A — analogy to controller offload

Moving row enumeration from board/controller logic into the DRAM can be described functionally as an offload of one maintenance-control function.

`Offload` is a modern analytical term here, not a recovered 1984 actor category.

### Limit — patent mechanism ≠ exact TMS4256 implementation

US4653030A and the TMS4256/TMS4257 datasheet are complementary evidence classes. The patent provides manufacturer-primary mechanism detail; the commercial datasheet provides product-family behavior. The patent does not identify its preferred embodiment as the exact TMS4256/TMS4257 circuit.

### Limit — no general DRAM generation history

Density, process, package, page/nibble modes, controller IC history, SDRAM command protocols, ECC, and later DDR refresh policy are outside this slice unless they alter a future retention comparison.

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

Case 09
    who supplies the maintenance address
    who triggers the maintenance cycle
    which part of refresh moves across the interface
```

This produces three particularly useful controls:

1. **refresh obligation ≠ refresh-address-generation locus**;
2. **internalized refresh addressing ≠ autonomous refresh scheduling**;
3. **hidden refresh ≠ absence of retention work**.

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
| Moving refresh enumeration on-chip removes the periodic retention obligation | X | contradicted by the same source set |
| `self refresh circuitry` in this patent automatically means later autonomous self-refresh | X | rejected by the patent's external-trigger statement |
| The patent is proven to be the exact TMS4256 circuit | X | unsupported product-identity leap |
| Retention infrastructure can itself contain retained control state | E | bounded reconstruction from refresh-counter role |

---

## Related repositories

### `tmzncty/computing-archaeology`

A dedicated TMS4256 / CAS-before-RAS refresh case was not found in the related-repository check for this pass. A broad DRAM technical history still belongs there:

<https://github.com/tmzncty/computing-archaeology>

This repository should keep only the retention-specific comparison about the **locus and visibility of maintenance work**.

### `tmzncty/problem-history`

Use its anti-anachronism discipline for the word `self refresh`. The patent's period phrase must be interpreted through the mechanism it actually describes rather than through later DRAM vocabulary.

---

## Sources

1. Texas Instruments, *MOS Memory Data Book 1986*, TMS4256/TMS4257 device section, revision header `MAY 1983—REVISED NOVEMBER 1985`: <https://bitsavers.org/components/ti/_dataBooks/1986_SMYD006_TI_MOS_Memory_Data_Book.pdf>.
2. Texas Instruments, `TMS4256, TMS4257 — 262,144-BIT DYNAMIC RANDOM-ACCESS MEMORIES`, standalone page-preserving copy, revision header `MAY 1983—REVISED JANUARY 1988`, directly inspected printed pp. 4-3 and 4-5: <https://www.ardent-tool.com/datasheets/TI_TMS4256_7.pdf>.
3. Tadashi Tachibana, Chitranjan N. Reddy, Ngai H. Hong, `Self refresh circuitry for dynamic memory`, US4653030A, filed 31 August 1984, assigned to Texas Instruments: <https://patents.google.com/patent/US4653030A/en>.
4. Texas Instruments, *MOS Memory Data Book 1984*, TMS4164 family documentation: <https://vintage-computer-books.netlify.app/Texas%20Instruments%20-%20MOS%20Memory%20Data%20Book%20-%201984.pdf>.
