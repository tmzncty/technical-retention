# Case 09 grounding — TI CAS-before-RAS refresh-address internalization

## Purpose

This record grounds one deliberately narrow DRAM-evolution claim:

> By the mid-1980s, a DRAM could keep the same deadline-driven retention obligation while moving **refresh-row address generation** from external system logic into the memory chip itself.

The bounded comparison is Texas Instruments' TMS4164 baseline versus the TMS4256/TMS4257 family and a TI-assigned 1984-filed refresh-counter patent. It is **not** a general history of DRAM refresh, SDRAM, DDR, autonomous self-refresh, or memory controllers.

The source set is chosen because it changes the retention comparison established by Case 03. Case 03 already grounds why dynamic state requires periodic reconstruction. This record asks a different question: **where does the machinery that enumerates the rows live, and who still has to cause refresh to happen on time?**

---

## Source set and inspection status

### P1 — Texas Instruments, *MOS Memory Data Book 1986*, TMS4256/TMS4257

**Document:** Texas Instruments, *MOS Memory Data Book 1986*, device section `TMS4256, TMS4257 — 262,144-BIT DYNAMIC RANDOM-ACCESS MEMORIES`, revision header `MAY 1983—REVISED NOVEMBER 1985`.

**Archive:**
<https://bitsavers.org/components/ti/_dataBooks/1986_SMYD006_TI_MOS_Memory_Data_Book.pdf>

**Period evidence recovered from the searchable primary scan:**

- `262,144 × 1` organization;
- maximum refresh period of 4 ms;
- `RAS-Only Refresh Mode`;
- `CAS-Before-RAS Refresh Mode`;
- `Hidden Refresh Mode`;
- the refresh description states that each of 256 rows must be refreshed within the interval;
- in CAS-before-RAS refresh, the external address is ignored and the refresh address is generated internally;
- hidden refresh likewise ignores the external address while allowing valid output data to remain at the output pin under the documented sequence.

The device section begins at printed p. 4-75 in the 1986 data book.

**Inspection boundary:** the Bitsavers PDF is searchable/indexed and yields the period 1985-revision text, but its exact facsimile page was not freshly renderable in this run. A page-preserving standalone TI datasheet copy with revision header `MAY 1983—REVISED JANUARY 1988` was directly inspected instead:

<https://www.ardent-tool.com/datasheets/TI_TMS4256_7.pdf>

Directly inspected printed p. 4-3 confirms the family, revision, 4 ms refresh period, RAS-only, hidden-refresh, and CAS-before-RAS feature list. Directly inspected printed p. 4-5 contains the refresh prose, including internal generation of the refresh address and the hidden-refresh sequence. The later facsimile is used only as a direct visual witness to this device-family mechanism; it is **not** used to pretend that every word on the January 1988 revision had already appeared unchanged in May 1983.

### P2 — Texas Instruments, US4653030A, *Self refresh circuitry for dynamic memory*

**Inventors:** Tadashi Tachibana, Chitranjan N. Reddy, Ngai H. Hong.

**Assignee:** Texas Instruments Incorporated.

**Filed:** 31 August 1984.

**Patent:**
<https://patents.google.com/patent/US4653030A/en>

**Primary anchors:** abstract; Summary of the Invention; description of FIG. 1, FIG. 2h, FIG. 3, and FIG. 5.

The patent states that a multiplexed-address dynamic memory uses an **on-chip refresh counter activated by a CAS-before-RAS sequence**. Either the ordinary address-input buffers or the refresh-counter stages are selected into the row-address path. It further states that a commercially available `64K × 1` device of this general type, **without the refresh counter of the invention**, was the `TMS4164`.

For the refresh-only cycle, CAS falls before RAS, the external address is ignored, eight refresh-counter stages provide the row address, and the ordinary column path is not needed. The patent then gives an especially useful system boundary: with a 4 ms maximum refresh period and 256 rows, the CAS-before-RAS sequence should be applied on average every 15.6 µs, and **this is controlled by the processor or memory controller external to the memory device**.

That sentence prevents a major overclaim: the on-chip counter internalizes row enumeration, but the bounded design does not thereby internalize the deadline scheduler that causes refresh cycles to occur.

### P3 — Texas Instruments TMS4164 period documentation

The 1984 TI MOS Memory Data Book and later TI device documentation describe the TMS4164 as a 65,536 × 1 dynamic RAM with a 4 ms refresh period in which all 256 row addresses must be strobed with RAS.

Period data-book route:
<https://vintage-computer-books.netlify.app/Texas%20Instruments%20-%20MOS%20Memory%20Data%20Book%20-%201984.pdf>

This source is useful as device-level context, while P2 supplies the stronger manufacturer-primary contrast by explicitly naming the TMS4164 as a commercial part lacking the patent's refresh counter.

---

## Claim ledger

| Claim | Label | Evidence | Status |
| --- | --- | --- | --- |
| TMS4256/TMS4257 require periodic refresh on a 4 ms maximum interval | H/P | P1, refresh section | direct period manufacturer evidence |
| The family supports RAS-only, CAS-before-RAS, and hidden-refresh modes | H/P | P1 feature list + refresh section | direct period manufacturer evidence |
| During CAS-before-RAS refresh, the external address is ignored and a refresh address is generated internally | H/P | P1 refresh section | direct manufacturer evidence; later revision also visually inspected |
| TI disclosed an on-chip refresh counter selected by CAS-before-RAS sequencing | H/P | P2 abstract + summary + FIG. 2h/3/5 description | direct manufacturer-primary design evidence |
| TI explicitly contrasted the disclosed counter design with a commercially available TMS4164 lacking that counter | H/P | P2 FIG. 1 description | direct manufacturer-primary comparison |
| Even with the counter on chip, the bounded design still requires an external processor/controller to issue refresh-trigger sequences often enough to meet the 4 ms / 256-row obligation | H/P/E | P2 refresh-cycle discussion | directly sourced architecture + bounded reconstruction |
| Refresh-row enumeration can move on-chip without eliminating the physical refresh deadline | E | P1 + P2 + Case 03 | strongly grounded reconstruction |
| Hidden refresh makes retention work disappear | X | P1 directly documents refresh activity while output remains valid | rejected |
| CAS-before-RAS internal refresh counter is equivalent to later autonomous oscillator-based DRAM self-refresh | X | P2 explicitly leaves trigger cadence external | rejected |
| US4653030A is the exact internal circuit of the commercial TMS4256/TMS4257 | X | patent does not make this product identity claim; datasheet and patent are used as separate evidence layers | rejected |

---

## What changes relative to Case 03

Case 03 already established:

```text
charge leakage
    -> finite retention interval
    -> periodic restoration obligation
```

The present source set adds a second axis:

```text
retention deadline
    stays

refresh trigger cadence
    remains externally imposed in the bounded patent

row-address enumeration
    external in the TMS4164 contrast
    -> can move on-chip in the disclosed CBR-counter design

normal address pins during CBR refresh
    ignored

row reconstruction
    still performed inside the DRAM array/sense path
```

The key result is therefore not `DRAM became self-maintaining`. It is:

> **one component of retention work — deciding which row is next — can migrate across an interface while the deadline and the need to trigger maintenance remain.**

---

## Historical vocabulary boundary

The period sources themselves use:

- `refresh`;
- `RAS-only refresh`;
- `CAS-before-RAS refresh`;
- `hidden refresh`;
- `refresh address`;
- `refresh counter`;
- the patent title phrase `self refresh circuitry`.

The last phrase requires care. In this 1984-filed TI patent, the disclosed counter is activated by an externally caused CAS-before-RAS sequence, and the patent explicitly says the processor or memory controller controls how often that sequence is applied. Therefore:

> **period use of `self refresh` here must not be silently normalized into the later stronger meaning of a DRAM autonomously scheduling its own refresh from an internal timer/oscillator while the external system need not issue refresh cycles.**

Later DRAM self-refresh is a separate future case if needed.

---

## Engineering implications

### E — Refresh obligation ≠ refresh-address-generation locus

Leakage determines that rows must be reconstructed before a deadline. It does not determine whether the next-row identifier must be supplied by motherboard/controller logic or generated by a counter on the DRAM die.

### E — Internalized addressing ≠ autonomous scheduling

The bounded TI design internalizes row enumeration but still depends on external CAS/RAS timing to request refresh. It therefore decomposes what can otherwise be vaguely called `the refresh controller` into at least:

1. deadline/scheduling responsibility;
2. refresh-cycle triggering;
3. row enumeration;
4. row selection;
5. sensing/restoration.

Those functions can move independently.

### E — Retention infrastructure retains control state of its own

A refresh counter has a current count between successive refresh requests. That count is not application payload and does not constitute a history of user data. It is nevertheless machine state required so successive maintenance cycles cover the row set rather than repeatedly revisiting an arbitrary row.

This adds a useful recursive case for the project:

> machinery that preserves payload can itself depend on retained control state.

The claim is bounded to the architectural role documented by P2; it does not imply that the counter survives power loss or has archival significance.

### E — Hidden refresh ≠ absent refresh

P1's hidden-refresh mode allows valid output data to remain while RAS is cycled in a refresh sequence. The work becomes less visible at one interface, but the row-refresh operation still happens and still consumes timing/power resources.

This directly strengthens the repository's existing rule:

> interface invisibility is observer-relative and must not be mistaken for maintenance disappearance.

---

## Failure / forgetting boundaries

The source-grounded mechanism supports several distinct failure classes:

- **missed deadline:** too few refresh cycles occur within the specified period;
- **trigger/path failure:** the CAS/RAS sequence does not request the intended refresh path;
- **enumeration failure:** the internal refresh-address mechanism fails to progress through the row set correctly;
- **shared reconstruction failure:** row selection/sensing/restoration fails even if the trigger and row identifier are correct.

The evidence does **not** support inventing transistor-specific failure probabilities or asserting which physical subcircuit would fail first. Those require a different source set.

---

## Related-repository check

`tmzncty/computing-archaeology` was searched for a dedicated TMS4256 / CAS-before-RAS refresh treatment and no directly reusable case was found in this pass.

That repository remains the correct home for a broader history of DRAM generations, controller ICs, packaging, density, process technology, and later SDRAM/DDR refresh standards. `technical-retention` should retain only the bounded comparison about **migration of retention responsibility across the chip/system interface**.

---

## Grounding decision

**Status: `grounded` for the bounded refresh-address-internalization claim.**

Promotion is justified because the central claims have:

- a period TI device datasheet establishing the commercial refresh modes and internal refresh-address behavior;
- a TI-assigned primary design patent that exposes the counter/address-path mechanism and explicitly names the TMS4164 comparison;
- an explicit primary statement that external system logic still controls refresh-trigger cadence;
- direct facsimile inspection of the later revision's relevant TMS4256/TMS4257 pages, with the 1985-revision period text separately anchored in the 1986 TI data book;
- explicit negative controls against product-identity and later-self-refresh anachronism;
- a related-repository duplication check.

Remaining work is optional deepening, not a blocker for this bounded result: exact direct rendering of the November 1985 TMS4256/TMS4257 data-book pages, a dedicated period controller-IC case, or a later autonomous-self-refresh case.
