# Deepening Record — 1984–1988 CAS-before-RAS Refresh, On-Chip Coverage State, and the Self-Refresh Boundary

## Target case

[`cases/03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md)

## Status

**`bounded deepening complete`**

This record closes one narrow debt left by the earlier Intel 2164A / 8203 deepening:

> What changes when a later DRAM moves the **refresh-address / coverage counter** onto the DRAM itself, and does that move make the device self-refreshing or otherwise autonomous?

The bounded answer is **no**. Texas Instruments documentation for the TMS4256/TMS4257 family shows a CAS-before-RAS (`CAS-before-RAS`) mode in which the external address is ignored and the refresh address is generated internally. TI applications material makes the internal state explicit as an **on-chip refresh counter** that removes the need for an external refresh counter. But the device still depends on externally applied CAS/RAS timing to invoke each refresh opportunity.

A contemporaneous NEC patent, filed in 1984 and published in 1986, is especially useful as a terminology/control counterexample: it describes conventional CAS-before-RAS refresh with an internal refresh/address counter, then adds a timer and refresh-timing generator so the device can transition into a distinct **self-refresh mode**. Thus, in the period sources used here:

```text
on-chip refresh-address generation
    != autonomous refresh cadence

CAS-before-RAS refresh
    != self-refresh
```

This is not a general history of asynchronous DRAM refresh, an invention-priority claim, or proof of which vendor first shipped any particular mode.

---

## Why this slice matters

The previous Case 03 deepening established an Intel 1982–1984 arrangement in which:

```text
DRAM payload state
    != external refresh-deadline / timer state
    != external next-row / coverage state
    != refresh/access arbitration state
```

That result still left an important architectural question open. Once the next-row state moves **inside** the DRAM package, a loose account can easily collapse several kinds of autonomy into one:

```text
internal row selection
    -> "automatic refresh"
    -> "self-refresh"
```

The period sources here block that collapse.

A more accurate decomposition is:

```text
restore execution
    = perform the internal sensing/restoration work

coverage authority
    = determine which refresh row/address comes next

cadence / trigger authority
    = determine when another refresh operation must occur

service arbitration
    = determine when maintenance may occupy the shared interface
```

Different generations and products can place these functions in different locations.

---

## Historical record

### H/P — TI's TMS4256/TMS4257 production datasheet requires recurrent refresh over 256 rows

A Texas Instruments TMS4256/TMS4257 datasheet preserved as a 23-page manufacturer scan identifies the parts as `262,144-BIT DYNAMIC RANDOM-ACCESS MEMORIES`. The copy inspected here is marked:

- `MAY 1983 — REVISED JANUARY 1988`;
- `Copyright © 1983, Texas Instruments Incorporated`;
- `PRODUCTION DATA`.

Its feature page lists:

- a `Long Refresh Period ... 4 ms (Max)`;
- `RAS-Only Refresh Mode`;
- `Hidden Refresh Mode`;
- `CAS-Before-RAS Refresh Mode`.

The operating-text page then states that refresh must be performed at least once every four milliseconds to retain data and describes the requirement as strobing each of 256 refresh rows.

This establishes the continuing **array-wide deadline and coverage obligation** for this product family. It does not by itself say where all timing or coverage state lives.

**Primary anchors:** Texas Instruments, `TMS4256, TMS4257 — 262,144-BIT DYNAMIC RANDOM-ACCESS MEMORIES`, inspected scan pp. 4-3 and 4-5; copy marked May 1983, revised January 1988.

Public scan: <https://www.ardent-tool.com/datasheets/TI_TMS4256_7.pdf>

### H/P — CAS-before-RAS makes the external row address irrelevant for refresh

The same TI datasheet gives a specific CAS-before-RAS sequence: CAS is brought low before RAS, and successive cycles can keep CAS low while RAS is cycled.

The key sentence for this case is that, during CAS-before-RAS refresh:

- the **external address is ignored**;
- the **refresh address is generated internally**.

That is a historical product-level change in the locus of coverage state.

Compare the earlier Intel 2164A evidence in the existing Case 03 deepening, where hidden refresh still acted on the row addressed at the second RAS and an external controller could own the next-row counter.

This TI source therefore supports the bounded transition:

```text
external refresh address supplied by controller
    -> internal refresh address supplied by DRAM
```

It does **not** by itself prove a timer, autonomous recurrence, or self-refresh.

**Primary anchor:** TI TMS4256/TMS4257 datasheet, inspected printed p. 4-5, `CAS-before-RAS refresh`.

### H/P — TI's 1986 applications material explicitly names an on-chip refresh counter

Texas Instruments' 1986 *MOS Memory Data Book* applications material explains the same feature at system level. In its `CAS-BEFORE-RAS REFRESH` discussion, TI says the feature on the TMS4256/TMS4257 includes an **on-chip refresh counter** that eliminates the requirement for an external refresh counter.

The same passage says:

- CAS must be low for the specified setup interval before RAS goes low to enable CAS-before-RAS refresh;
- successive refreshes can keep CAS low while RAS is cycled;
- the on-chip counter enables the present refresh address when the CAS-before-RAS preconditions are met;
- from the system point of view, some external refresh-address multiplexing and counter circuitry can be eliminated.

The immediately adjacent `RAS-ONLY REFRESH` discussion describes the older organization explicitly: an external timer enables an external counter at the refresh period, and that external counter outputs the row to be refreshed.

This is unusually clean historical evidence for a control-state relocation:

```text
RAS-only organization described by TI
    external timer
    + external refresh counter
    + externally supplied row address

CAS-before-RAS organization described by TI
    external CAS/RAS invocation
    + on-chip refresh counter
    + internally generated refresh address
```

The TI text does not say that the TMS4256/TMS4257 independently decides when enough time has passed to issue a refresh while the interface is otherwise idle.

**Primary manufacturer source:** Texas Instruments, *MOS Memory Data Book* (1986), Applications Information, `CAS-BEFORE-RAS REFRESH`, printed p. 9-52 in the archived section.

Archive locator: <https://garyopa.hopto.org/WHTech/ftp.whtech.com/datasheets%20and%20manuals/Datasheets%20-%20TI/MOSMemory-1986/MOSMemory-1986-09-Applications%20Information.pdf>

Canonical data-book archive: <https://bitsavers.org/components/ti/_dataBooks/1986_SMYD006_TI_MOS_Memory_Data_Book.pdf>

### H/P — `hidden refresh` can reuse the internal address path without becoming self-refresh

The inspected TI production datasheet also says the external address is ignored during hidden-refresh cycles on this implementation.

This matters because the same term `hidden refresh` described a different row-address situation in the earlier Intel 2164A material used elsewhere in Case 03.

The safe historical conclusion is therefore:

```text
same label: "hidden refresh"
    != guaranteed same refresh-address locus
```

In the TI implementation inspected here, the hidden-refresh path can use internally generated refresh addressing. In the earlier Intel 2164A evidence, the refreshed row remained tied to an externally supplied row address.

This is a terminology warning, not proof of a clean industry-wide generation boundary.

### H/P — NEC's 1984-filed patent treats CAS-before-RAS and self-refresh as distinct modes

NEC's Japanese patent application JP59177905A was filed on 27 August 1984 and published as JPS6157097A on 22 March 1986. Google Patents identifies Kazuo Nakaizumi as inventor and NEC Corporation as original assignee.

The patent's translated abstract and description distinguish two modes:

1. a **CAS-before-RAS refresh mode** that already uses a refresh/address counter;
2. a later **self-refresh mode** entered after a timing condition is met.

The description of the conventional CAS-before-RAS arrangement says refresh/address counter 23 supplies the refresh address when the CAS/RAS condition invokes refresh. It explicitly observes that putting the refresh-address counter inside the DRAM removes the need for an external refresh address.

The invention then adds:

- timer 24;
- refresh timing generation circuit 25;
- control logic that transitions from CAS-before-RAS refresh into self-refresh after RAS remains active for a predetermined period.

During the self-refresh mode, the timer/timing-generation circuitry causes repeated refresh using the refresh/address counter until the mode is released.

This patent is not product-shipment evidence, but it is strong primary evidence that period designers treated these as **different control layers**.

**Primary anchor:** NEC / Kazuo Nakaizumi, JPS6157097A, `Dynamic semiconductor memory`, filed 1984-08-27, published 1986-03-22, especially translated abstract and description of refresh/address counter 23, timer 24, and refresh timing generator 25.

Transcription: <https://patents.google.com/patent/JPS6157097A/en>

### H/P — NEC's distinction exposes what on-chip CBR still leaves external

The NEC description says the conventional CAS-before-RAS arrangement can retain cell data with an internal refresh-address counter and CAS/RAS clocks, yet it still characterizes external refresh control as burdensome enough to motivate the added self-refresh control.

That yields a period-authored distinction that is very useful for Case 03:

```text
internal coverage state
    != internal cadence generation
```

A DRAM can know **which row is next** without autonomously deciding **when the next refresh is due**.

This does not imply that every CBR implementation had the exact NEC block diagram or that every later self-refresh implementation descended from this patent.

### H/P — Samsung's 1988 data book independently exposes the counter increment step

Samsung's 1988 *MOS Memory Data Book* documents the KM41256A/KM41257A family with CAS-before-RAS on-chip refreshing. The converted manufacturer text states that:

- CAS-before-RAS enables on-chip refresh circuitry;
- an internal refresh operation occurs;
- the on-chip refresh-address counter is incremented in preparation for the next CAS-before-RAS refresh cycle;
- hidden refresh uses that on-chip counter as well;
- a special CAS-before-RAS counter-test cycle exists to verify the counter-related circuitry.

This is an independent product-family witness that the internal coverage state is not merely an abstract inference from `address generated internally`; the vendor exposed behavior explicitly in terms of a counter and its progression.

**Primary manufacturer source:** Samsung Semiconductor, *1988 MOS Memory Data Book*, KM41256A/KM41257A device-operation pages, publicly converted transcript at <https://manuals.plus/m/85b83593adbc036de4142423dbf452ec188a6445ad476820abc659b82e7f2ade>.

Because the accessible copy is a converted text presentation rather than the directly inspected original page image, this source is used only for the explicit counter/increment/test statements and not for fine-grained diagram interpretation.

---

## Engineering reconstruction

### E — refresh control has at least three separable authorities

The combined Intel/TI/NEC evidence supports a stronger decomposition than the earlier Case 03 packet alone:

```text
1. restoration authority
   perform a refresh operation on the selected row

2. coverage authority
   determine which row/address comes next

3. cadence authority
   determine when another refresh operation must be invoked
```

A fourth system-level layer often exists as well:

```text
4. arbitration authority
   decide when maintenance may use the shared memory interface
```

These can migrate independently between controller and DRAM.

### E — on-chip coverage state is not self-refresh

The TI device removes the external refresh address from CAS-before-RAS refresh and TI applications material names the internal state as an on-chip counter. But externally supplied CAS/RAS sequencing still invokes the operation.

Thus:

```text
coverage counter inside DRAM
    != refresh timer inside DRAM
    != autonomous recurrence
```

The NEC patent makes that distinction explicit by adding a timer/timing generator to a design that already has the internal counter.

### E — integration can reduce external state without eliminating the maintenance obligation

Moving the refresh counter on-chip can eliminate some board-level logic and address multiplexing. It does not eliminate:

- the cell leakage deadline;
- the need to cover all required rows;
- the need to create refresh opportunities;
- the power/time cost of restoration;
- the need for a defined entry/exit/control protocol.

So integration changes **where maintenance state lives**, not whether the retention relation requires maintenance.

### E — the same logical obligation can survive a change of control-state embodiment

The 8203-style external counter and the TMS4256/TMS4257 on-chip counter can both satisfy the same functional need:

```text
remember next refresh address
```

The retained user payload need not know which embodiment supplied that coverage state.

This provides another project-level boundary:

```text
maintenance obligation
    != one fixed physical embodiment of maintenance-control state
```

### E — terminology must be decomposed by mechanism, not normalized by later vocabulary

The sources show at least four period-visible terms or mode labels:

- `RAS-only refresh`;
- `CAS-before-RAS refresh`;
- `hidden refresh`;
- `self-refresh`.

They should not be collapsed into a single timeless category called `automatic refresh`.

The engineering questions are more precise:

```text
Who supplies the refresh address?
Who remembers next-row coverage?
Who creates the timing trigger?
Who arbitrates refresh against useful service?
What remains externally clocked or commanded?
```

---

## Controlled functional comparison

### A — relation to Case 09's 1972 `automatic refresh` terminology

Case 09's Signetics 2548/2601 evidence shows that a period document can use `automatic refresh` for access/address-coupled restoration without implying autonomous recurring cadence or whole-array traversal.

The CBR evidence here adds a different decomposition:

```text
1972 access-coupled "automatic" restoration
    automatic internal action after a qualifying access/address event

1980s CAS-before-RAS with on-chip counter
    internal coverage/address progression
    but externally invoked refresh opportunities

self-refresh design
    internal timing generation added to internal coverage state
```

This is a **functional/terminological comparison**, not a genealogy.

### A — relation to later mobile-DRAM refresh cases

Later LPDDR cases in this repository expose per-bank refresh, self-refresh, temperature-conditioned policy, and other richer control splits. The present slice should be used only as an earlier bounded example of **control-state relocation**.

It does not establish a direct line from the TMS4256/TMS4257 or NEC patent to later JEDEC mobile-memory mechanisms.

---

## Philosophical / media-theoretical boundary

### I — hidden maintenance can move inward without becoming independent

This slice sharpens one conceptual point already present in Case 03: apparent continuity depends on a temporal organization that can be displaced across system boundaries.

Here, the displacement is literal:

```text
next-row memory
    moves from external controller logic
    into the DRAM package
```

But the maintenance relation remains dependent on external timing signals until cadence generation also moves inward.

The narrow philosophical lesson is therefore not `integration = autonomy` but:

> the boundary of a technical object can move while the dependency structure that sustains retention remains distributed.

That observation should not be inflated into a claim about agency, organismic memory, tertiary retention, or `Bestand`.

---

## Explicit non-claims

This deepening does **not** claim that:

1. Texas Instruments invented CAS-before-RAS refresh;
2. TMS4256/TMS4257 were the first DRAMs with an internal refresh-address counter;
3. the inspected January-1988 revision proves every listed feature was already present in the original May-1983 revision;
4. the 1986 TI applications note proves first shipment or first commercial availability;
5. every TMS4256/TMS4257 stepping implemented CAS-before-RAS identically;
6. every asynchronous DRAM used an on-chip refresh counter;
7. RAS-only refresh always requires an external counter in every later architecture;
8. CAS-before-RAS refresh is the same thing as self-refresh;
9. hidden refresh is the same thing as self-refresh;
10. `refresh address generated internally` proves an internal refresh timer;
11. an on-chip counter proves autonomous maintenance cadence;
12. an on-chip counter proves that refresh/access arbitration is also on-chip;
13. an internal refresh counter is nonvolatile;
14. the refresh counter survives power loss or reset;
15. losing the counter necessarily destroys payload immediately;
16. internal refresh-address generation removes the refresh deadline;
17. internal refresh-address generation removes refresh bandwidth or power cost;
18. NEC's 1984 filing proves a shipped NEC product had the claimed self-refresh implementation in 1984;
19. the translated NEC patent text should be treated as perfectly idiomatic English engineering terminology;
20. the NEC patent establishes invention priority for self-refresh;
21. Samsung's converted transcript substitutes for page-image verification of every diagram or timing value;
22. Intel 2164A hidden refresh and TI TMS4256 hidden refresh have identical address-generation semantics;
23. a shared mode label proves a shared circuit implementation;
24. CBR-to-self-refresh control in the NEC patent is genealogically ancestral to later JEDEC self-refresh;
25. integration of coverage state makes DRAM a maintenance-free medium;
26. functional similarity to later scrub/checkpoint state proves historical continuity;
27. this slice is a complete history of 256K DRAMs;
28. this slice is a complete history of refresh terminology;
29. the 1980s documents define modern DDR refresh semantics;
30. `automatic`, `hidden`, `CBR`, and `self-refresh` are interchangeable project synonyms.

---

## Claim ledger

| Claim | Label | Evidence |
| --- | --- | --- |
| TI's inspected TMS4256/TMS4257 production datasheet is marked May 1983, revised January 1988 | H/P | TI datasheet p. 4-3 |
| The inspected TI revision requires refresh over 256 rows within 4 ms | H/P | TI datasheet p. 4-5 |
| During TI CAS-before-RAS refresh, the external address is ignored and the refresh address is generated internally | H/P | TI datasheet p. 4-5 |
| TI applications material describes the feature as using an on-chip refresh counter that eliminates the external refresh counter | H/P | TI 1986 *MOS Memory Data Book*, Applications Information p. 9-52 |
| TI contrasts older RAS-only organization using an external timer/counter with CBR using the on-chip counter | H/P | same TI applications section |
| NEC filed JP59177905A on 1984-08-27 and publication JPS6157097A appeared on 1986-03-22 | H/P | patent metadata |
| NEC's patent distinguishes CAS-before-RAS refresh from a self-refresh mode entered by added timer/timing-generation control | H/P | JPS6157097A abstract and description |
| Samsung 1988 product documentation describes an on-chip refresh counter that increments for the next CBR cycle | H/P | Samsung 1988 *MOS Memory Data Book* converted device-operation text |
| Coverage authority can move on-chip while cadence authority remains external | E | bounded reconstruction from TI + NEC sources |
| An internal refresh-address counter is not evidence of nonvolatile maintenance state | E/X boundary | source does not claim persistence across reset/power loss |
| CAS-before-RAS refresh is historically identical to self-refresh | X | directly contradicted by NEC mode distinction |
| The 1980s CBR evidence proves genealogy to later JEDEC self-refresh | X | unsupported |

---

## Source ledger

### Primary manufacturer documentation

1. Texas Instruments, **`TMS4256, TMS4257 — 262,144-BIT DYNAMIC RANDOM-ACCESS MEMORIES`**, inspected manufacturer scan; title page of the device section marked `MAY 1983 — REVISED JANUARY 1988`.
   - public scan: <https://www.ardent-tool.com/datasheets/TI_TMS4256_7.pdf>
   - printed p. 4-3: revision line and feature list;
   - printed p. 4-5: 4 ms / 256-row refresh statement; CAS-before-RAS mode; external address ignored; refresh address generated internally; hidden-refresh address boundary.
2. Texas Instruments, **MOS Memory Data Book** (1986), Applications Information.
   - canonical archive: <https://bitsavers.org/components/ti/_dataBooks/1986_SMYD006_TI_MOS_Memory_Data_Book.pdf>
   - section mirror: <https://garyopa.hopto.org/WHTech/ftp.whtech.com/datasheets%20and%20manuals/Datasheets%20-%20TI/MOSMemory-1986/MOSMemory-1986-09-Applications%20Information.pdf>
   - printed p. 9-52: external timer/counter description for RAS-only refresh; on-chip refresh counter description for CAS-before-RAS; system-logic reduction.
3. Samsung Semiconductor, **1988 MOS Memory Data Book**, KM41256A/KM41257A device-operation section.
   - public converted transcript: <https://manuals.plus/m/85b83593adbc036de4142423dbf452ec188a6445ad476820abc659b82e7f2ade>
   - relevant text: CAS-before-RAS on-chip refresh circuitry; internal counter increment; hidden-refresh use of counter; CBR counter-test cycle.

### Primary patent record

4. Kazuo Nakaizumi / NEC Corporation, **`Dynamic semiconductor memory`**, JP59177905A / JPS6157097A.
   - filed: 1984-08-27;
   - published: 1986-03-22;
   - transcription and metadata: <https://patents.google.com/patent/JPS6157097A/en>;
   - abstract and description: conventional CAS-before-RAS refresh/address counter; added timer 24; refresh timing generator 25; transition into distinct self-refresh mode.

### Bibliographic cross-check

5. Google Books catalog record, Texas Instruments, *MOS Memory Data Book*, Texas Instruments, 1986: <https://books.google.com/books/about/MOS_Memory_Data_Book.html?id=-iouAQAAIAAJ>.

---

## Source-quality note

The 23-page TI TMS4256/TMS4257 production datasheet was directly inspected as page images in this research slice, including printed pp. 4-3 and 4-5. The inspected copy is explicitly a **January 1988 revision**, so this record does not back-project every visible feature into May 1983 merely because the revision line names that earlier origin date.

The 1986 TI applications section is period manufacturer documentation and is bibliographically cross-checked against the 1986 TI data book. Its relevant text is publicly indexed, but the archive hosts did not provide a renderable page image through the current retrieval path. Accordingly, this record uses only the explicit prose about external versus on-chip counters and does not infer from unreadable schematics.

The NEC patent is a primary filing but its accessible English text is machine-translated from Japanese. It is used for the structural mode distinction and identified block relationships, not for fine semantic claims about exact English wording.

The Samsung source is a converted public transcript of manufacturer documentation. It is included as corroboration, not as the sole basis for the core conclusion.

---

## Related-repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `CAS-before-RAS refresh TMS4256` found no dedicated packet to reuse.

This repository should therefore keep only the retention-specific seam:

```text
external coverage counter
    -> on-chip coverage counter
    -> separate addition of cadence/timing generation for self-refresh
```

Broader work belongs primarily in `computing-archaeology`, including:

- first-invention and first-shipment priority for CAS-before-RAS refresh;
- vendor-by-vendor 64K/256K/1M DRAM feature chronology;
- controller/chipset adoption history;
- JEDEC ballot/standard chronology;
- circuit genealogy from asynchronous CBR to later self-refresh;
- pricing, packaging, process, and manufacturing history.

---

## Remaining debt

This slice closes the bounded debt `compare a later DRAM with an on-device refresh-address counter to the externally controlled 2164A arrangement`.

It also partially closes the terminology debt by establishing, no later than the 1984-filed / 1986-published NEC record, a primary-source distinction between `CAS-before-RAS refresh` and `self-refresh`.

Still open:

- identify the earliest **directly page-inspected** manufacturer product documentation for an on-chip CBR refresh counter rather than relying on later revision plus 1986 applications prose;
- determine first public/shipping use of the terms `CAS-before-RAS refresh`, `hidden refresh`, and `self-refresh` without assuming the oldest source found is the invention;
- recover JEDEC committee/standard chronology for these asynchronous-DRAM modes;
- inspect a named shipping self-refresh DRAM whose internal timing generator is documented at product level;
- verify reset/power behavior of internal refresh counters on named devices;
- test experimentally what happens when externally supplied CBR cadence is too slow while the on-chip coverage counter itself remains correct;
- keep broad semiconductor-memory genealogy in `computing-archaeology` rather than expanding Case 03 into a device-history survey.
