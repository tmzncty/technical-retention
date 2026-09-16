# Case 11 deepening — Intel 1976 1702A datasheet qualification boundary

## Status

**`bounded deepening complete`**

This note deepens [`../cases/11-intel-frohman-floating-gate-eprom-erasure.md`](../cases/11-intel-frohman-floating-gate-eprom-erasure.md) at the product-datasheet layer.

The previous Case 11 deepening established a period Intel development workflow in which a 1702A is exposed to ultraviolet light and then checked across its address space for the erased state. Its remaining archival debt asked for a period 1702A datasheet/data-book page so that product qualification could be separated from programmer/manual procedure.

The directly inspected 1976 Intel Data Catalog material closes that narrower document-class gap, but it also produces a useful negative result:

> the checked 1702A datasheet specifies operating/storage temperature limits, read/program electrical limits, access time, programming time, and factory programmability, but does **not** itself state a quantified data-retention duration or erase/program endurance count in the checked product entry.

That distinction matters because a product can be explicitly nonvolatile and tightly electrically qualified without the same datasheet entry turning that property into a `N years at T` retention warranty.

---

## Research question

The bounded question is:

> Once a period manufacturer datasheet is inspected, which limits are actually product qualifications, and which stronger retention/endurance claims remain absent?

A second, deliberately later Intel source is used only as a bounded successor comparison:

> What does Intel's 1977 2716 engineering handbook say about a device that reads as a logical value while its programmed/erased cell characteristic is too close to the sense threshold?

The latter is not projected backward as a 1702A specification. It is used to sharpen the difference between a readable logical postcondition and physical margin.

---

## Source set and provenance control

### P1 — Intel, _1976 Intel Data Catalog_, 1702A product entry

Primary manufacturer catalog, mirrored at:

- <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/1976_Intel_Data_Catalog.pdf>
- alternate 1702A-only extract: <https://www.cpu-galaxy.at/CPU/Ram%20Rom%20Eprom/ROM/Intel%201702%20section-Dateien/1702_Datasheet.pdf>

The catalog entry is headed:

- `1702A`
- `2K (256 x 8) UV ERASABLE PROM`

The surviving catalog scan is a period manufacturer source. This note uses the **1976 catalog appearance** as its document date and does not infer that every limit first appeared in 1976 or that this is the earliest 1702A datasheet revision.

### P2 — Intel, _Memory Design Handbook_, May 1977, 2716 application section

Primary manufacturer engineering handbook, mirrored at:

- <https://www.bitsavers.org/components/intel/_dataBooks/1977_C-160_memDesignHb_May77.pdf>
- alternate mirror: <https://www.hartetechnologies.com/manuals/Intel/C-160%20mem%20Design%20Hndbk_May77.pdf>

The relevant section is the 2716 discussion titled `Under Programming And Under Erasing`, followed by the 2716 Mini Programmer discussion.

This source is **not** treated as a 1702A specification. It is a later Intel engineering comparison that exposes the distinction between digital readback and analog cell margin.

### P3 — Smithsonian National Museum of American History, Intel 1702A object record

Institutional artifact/context record:

- <https://americanhistory.si.edu/collections/object/nmah_713501>

The museum records an Intel 1702A EPROM object, credits Intel, dates the object to 1972, and identifies it as nonvolatile, electrically programmable, and UV erasable. It is used only as object/context evidence, not for electrical qualification.

---

## Historical record — 1976 1702A product entry

### H/P — the product is explicitly a 2K UV-erasable PROM

Intel's 1976 catalog labels the 1702A a `2K (256 x 8) UV ERASABLE PROM`.

The entry lists three access-time grades:

- 1702A-2 — 0.65 µs maximum;
- 1702A — 1.0 µs maximum;
- 1702A-6 — 1.5 µs maximum.

The datasheet also advertises:

- `Fast Programming: 2 Minutes for all 2048 Bits`;
- `All 2048 Bits Guaranteed Programmable: 100% Factory Tested`;
- `Static MOS: No Clocks Required`.

The prose explains that the device is a 256-word × 8-bit electrically programmable ROM, that all 2048 bits are initially in the `0` state, and that information is introduced by selectively programming `1`s. The transparent package lid allows ultraviolet exposure to erase the bit pattern.

These are direct product statements. They are not, by themselves, quantified lifetime/endurance statements.

### H/P — Intel separately specifies operating and storage temperature limits

The product entry gives an absolute-maximum ambient temperature under bias of approximately **-10°C to +80°C** and a **storage temperature of -65°C to +125°C**.

The normal read-operation tables use a commercial operating-temperature range of **0°C to +70°C**.

This is valuable because the datasheet now grounds a period, product-specific environmental envelope that the earlier MCS-4 workflow did not provide.

But the source labels these as electrical/absolute-maximum and operating conditions. It does not say that data is guaranteed to remain valid for a specified number of years throughout the storage-temperature range.

### H/P — electrical stress limits are product qualifications, not retention-time statements

The same entry specifies read- and program-operation voltage/stress limits and timing. That makes the 1976 catalog a materially different source class from the MCS-4 development manual:

```text
MCS-4 development manual
    -> operator/programmer procedure
    -> erase exposure + read/list verification

1976 product datasheet
    -> device ratings
    -> operating/storage temperature
    -> access/program timing
    -> voltage/stress limits
```

The documents overlap in product family but answer different engineering questions.

### H/P — `100% factory tested` is explicitly attached to programmability

Intel's headline says all 2048 bits are guaranteed programmable and `100% Factory Tested`; the prose says complete programming and functional testing is performed before shipment to insure programmability.

The bounded historical claim is therefore about **shipment-time programmability testing**.

The source does not turn this statement into:

- an erase/program cycle-count guarantee;
- a retention-duration guarantee;
- a guarantee that repeated UV/program cycles leave the same analog margin indefinitely.

### H/P/N — no quantified retention-years statement appears in the checked product entry

The directly inspected four-page 1702A datasheet extract and the indexed 1976 catalog text do not expose a `retention`, `years`, or erase/program `cycles` specification for stored-data lifetime/endurance.

This is **bounded negative evidence about this checked document**, not a historical claim that Intel never published such a qualification elsewhere.

Safe wording:

> In the checked 1976 Intel 1702A product entry, product/environment/electrical limits are explicit, while a quantified data-retention duration and erase/program endurance count are not stated.

Unsafe wording:

> Intel had no retention/endurance qualification for the 1702A.

The latter would require a much broader archival search of reliability reports, qualification documents, data books, application notes, and revision history.

---

## Engineering reconstruction

The following are project-level interpretations, not period Intel terminology.

### E/R — storage-temperature rating is not a retention-duration warranty

The 1976 datasheet gives a storage-temperature range. That establishes a device stress/environment boundary, not automatically a data-retention claim.

Therefore:

```text
specified storage-temperature range
    !=
quantified data-retention duration at that temperature
```

A datasheet can tell us that the packaged device may be stored within a temperature range without thereby telling us how many years a programmed bit is guaranteed to remain within read margin under every point in that range.

This distinction prevents a common evidence error: taking any number in a `storage` row as if it were a retention-time specification.

### E/R — `Static MOS: No Clocks Required` is not a lifetime claim

The headline establishes that the 1702A does not need a DRAM-style clock/refresh mechanism for ordinary stored-state retention/read service.

It supports:

```text
no recurring clock required for retained state
    !=
no physical leakage / aging process exists
    !=
infinite retention duration
```

`Static` here helps classify the operating regime. It does not quantify how long the floating-gate charge remains safely separated from the sense threshold.

### E/R — factory programmability is not reprogramming endurance

A shipment-time guarantee that all 2048 bits are programmable answers a different question from how many erase/program repetitions a device can tolerate.

```text
all locations programmable at factory test
    !=
N guaranteed erase/program cycles
```

The earlier MCS-4 manual demonstrates intended erase-and-reprogram reuse. The 1976 datasheet demonstrates factory-tested programmability. Neither source, in the checked passages, supplies an endurance-cycle distribution.

### E/R — product qualification is multidimensional

The new source allows Case 11 to separate at least these fields:

```text
physical retention mechanism
    trapped floating-gate charge

operational erase procedure
    UV exposure under period guidance

erase-completion observation
    read/list erased state across addresses

product electrical qualification
    voltage / timing / temperature limits

shipment-time functional qualification
    all locations factory-tested programmable

retention-duration qualification
    not quantified in checked 1976 product entry

reprogramming-endurance qualification
    not quantified in checked 1976 product entry
```

The absence of the last two numbers from this product entry does not negate the first five fields.

---

## Bounded 2716 successor comparison — logical state versus cell margin

### H/P — Intel explicitly describes under-programmed / under-erased cells near the sense threshold

Intel's May 1977 _Memory Design Handbook_ says that the 2716 can be `under program[med]` or `under erasing` such that the cell characteristic crosses or sits near the sense threshold.

The handbook explains that small changes in voltage or temperature can then cause a `1` or `0` to be sensed. It attributes this state to insufficient erasing or programming.

Its prescribed cures are to:

1. erase adequately with the required UV exposure for the 2716 discussion; or
2. program according to specification.

The same handbook's programmer section provides manual verification and a duplicate mode in which each location is programmed and verified before the next location is processed, ending in PASS/FAIL indication.

### F/A — a readable digital value is not identical to generous analog margin

This later 2716 source gives a useful functional comparison for Case 11:

```text
logical state observed at one condition
    !=
large physical margin from the sense threshold
```

The source itself shows why: a partially programmed/erased cell can lie close enough to the threshold that temperature or voltage changes alter the sensed result.

This comparison is deliberately bounded:

- it does **not** prove the 1702A had identical cell distributions or thresholds;
- it does **not** retroactively add the 2716's UV-dose number to the 1702A;
- it does **not** show that every successful 1702A verify had a hidden marginal cell;
- it does show, within Intel's later EPROM engineering literature, why `readable postcondition` and `physical state margin` are analytically distinct.

### E/R — verification has a scope

The 1973 MCS-4 workflow verifies the readable logical postcondition after erase/program operations.

The 1977 2716 handbook makes clear that EPROM cell state also has an analog relation to a sense threshold.

Accordingly the project can now state more precisely:

```text
logical verification
    = evidence about the observed digital state under the verification conditions

logical verification
    !=
direct measurement of floating-gate charge
    !=
complete characterization of margin over all voltage / temperature / time
```

This is a scope statement about evidence, not a criticism of the historical programmer.

---

## Historical-record / reconstruction boundary

### Historical record established here

- Intel's 1976 catalog identifies the 1702A as a 2K UV-erasable PROM.
- The entry gives access grades, approximately two-minute programming for all bits, and 100% factory-tested programmability.
- The entry calls the device static MOS with no clocks required.
- The entry supplies absolute-maximum and operating temperature/electrical limits.
- The checked entry does not itself state a quantified retention duration or erase/program cycle count.
- Intel's 1977 2716 handbook explicitly discusses under-program/under-erase states near the sense threshold and sensitivity to voltage/temperature changes.

### Engineering reconstruction added here

- storage-temperature rating is not the same evidence object as a data-retention-duration guarantee;
- shipment-time programmability is not endurance;
- no recurring clock requirement is not infinite retention;
- readable digital verification does not directly measure analog charge/margin;
- product qualification should be represented as a vector of separate limits rather than one generic `reliability` field.

### Functional analogy only

The 2716 threshold-margin discussion is a **later same-vendor/same-broad-technology comparison**, not evidence that every 1702A internal behavior was identical.

### Philosophical interpretation only

The case can support the conceptual observation that technical persistence is not one number: the ability to retain a readable distinction, the environmental envelope, the confidence produced by verification, and the margin against future drift are different relations.

Intel's datasheets and handbook do not formulate that as a philosophy of memory or time.

---

## Claim ledger

| Claim | Label | Evidence |
| --- | --- | --- |
| Intel's 1976 catalog calls the 1702A a 2K (256 × 8) UV-erasable PROM | H/P | Intel _1976 Data Catalog_, 1702A entry |
| The 1702A product entry gives 0.65/1.0/1.5 µs access grades | H/P | same |
| The entry advertises approximately two-minute programming for all 2048 bits | H/P | same |
| Intel says all 2048 bits are guaranteed programmable / 100% factory tested | H/P | same |
| The device is described as static MOS with no clocks required | H/P | same |
| The entry gives -10°C to +80°C ambient-under-bias absolute maximum and -65°C to +125°C storage temperature | H/P | same |
| Normal read tables use a 0°C to +70°C operating range | H/P | same |
| The checked 1702A entry states a quantified data-retention duration | X | not found in the checked entry |
| The checked 1702A entry states a quantified erase/program endurance count | X | not found in the checked entry |
| Storage-temperature rating can be read as a retention-years guarantee | X | unsupported category substitution |
| `100% factory tested programmable` is an endurance-cycle guarantee | X | unsupported |
| `Static MOS: No Clocks Required` means infinite retention | X | unsupported |
| Intel's 1977 2716 handbook describes under-programmed/under-erased cell characteristics near the sense threshold | H/P | Intel _Memory Design Handbook_, May 1977 |
| The 2716 discussion says voltage/temperature changes can alter the sensed value when margin is insufficient | H/P | same |
| The 2716 threshold discussion proves identical 1702A cell behavior | X | unsupported backward projection |
| Logical readback verification directly measures floating-gate charge/margin | X | unsupported; it observes device output |

---

## Explicit non-claims

This note does **not** claim:

1. that the 1976 catalog is the first Intel 1702A datasheet;
2. that every 1702A revision shares exactly the same qualification envelope;
3. that no Intel reliability/qualification document ever specified 1702A retention duration;
4. that the 1702A had no endurance limit;
5. that the absence of an endurance number means unlimited endurance;
6. that -65°C to +125°C is a guaranteed data-retention-temperature range for a specified duration;
7. that `Static MOS` means physically immutable or indefinitely stable;
8. that two-minute programming time is a retention or erase-completion metric;
9. that 100% factory programmability proves every device remains programmable after arbitrary reuse;
10. that the 1977 2716 cell/threshold geometry is identical to the 1702A;
11. that the 2716 UV-dose value should be substituted for the 1702A's earlier MCS-4 erase guidance;
12. that a logical verify operation is a forensic remanence test;
13. that a successful read at one voltage/temperature proves margin at all allowed conditions;
14. that later EPROM qualification vocabulary can be silently backdated into Frohman's 1970–1971 patents;
15. that this product-document comparison establishes a genealogy toward EEPROM, Flash, SSD scrub, or sanitize.

---

## Related-repository check

Searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `1702A` and `EPROM` still return no dedicated technical-history module to reuse.

Accordingly this note keeps only the retention-specific evidence distinction:

```text
mechanism evidence
    !=
operator procedure
    !=
product electrical/environmental qualification
    !=
retention-duration/endurance qualification
```

A broader 1702/1702A/2708/2716 product genealogy, process history, programmer history, or Intel qualification-program history belongs primarily in `computing-archaeology` if developed later.

---

## What this closes

The previous deepening said that a dedicated 1702A datasheet/data-book page was still desirable.

That document-class debt is now closed in bounded form:

- a period Intel 1702A product entry has been directly inspected;
- it contributes product-specific environmental/electrical and functional limits;
- it does **not** provide the hoped-for retention-years/endurance-cycle numbers in the checked entry.

The research question therefore becomes more precise rather than simply remaining `find a datasheet`.

---

## Remaining bounded debt

The next archival step is now specifically **qualification/reliability evidence**, not another generic datasheet search:

1. locate an Intel 1702A reliability report, qualification report, earlier/later data-book revision, application note, or production document that explicitly states a data-retention duration and its temperature/test assumptions;
2. locate period evidence for erase/program endurance or reuse-cycle qualification for a named 1702A revision;
3. if such numbers first become explicit only in later EPROM generations, document that chronology without silently transferring them backward;
4. keep analog threshold/margin measurements distinct from logical readback verification;
5. keep electrical EEPROM erasure as a separate mechanism case rather than treating it as merely a better-qualified 1702A.

None of these items blocks the current `grounded` maturity of Case 11.

---

## Sources

1. Intel, _1976 Intel Data Catalog_, 1702A product entry, period manufacturer catalog mirror: <https://deramp.com/downloads/mfe_archive/050-Component%20Specifications/Intel/Memory%20Components/1976_Intel_Data_Catalog.pdf>.
2. Intel, 1702A-only datasheet extract mirror: <https://www.cpu-galaxy.at/CPU/Ram%20Rom%20Eprom/ROM/Intel%201702%20section-Dateien/1702_Datasheet.pdf>.
3. Intel, _Memory Design Handbook_, May 1977, 2716 `Under Programming And Under Erasing` and programmer sections: <https://www.bitsavers.org/components/intel/_dataBooks/1977_C-160_memDesignHb_May77.pdf>.
4. Alternate mirror of the same Intel 1977 handbook: <https://www.hartetechnologies.com/manuals/Intel/C-160%20mem%20Design%20Hndbk_May77.pdf>.
5. National Museum of American History, `Intel 1702A Electrically Programmable Read Only Memory (EPROM)`: <https://americanhistory.si.edu/collections/object/nmah_713501>.

## Retrieval note

The 1976 Intel catalog text was available through web indexing, and the compact four-page 1702A PDF extract was opened as a PDF in this research pass. Page-image rendering of that compact mirror timed out in the current reader; an earlier catalog render/index and the independently indexed catalog text agree on the product headline and qualification fields used here. The 1977 Intel handbook is independently indexed at both the Bitsavers and Harter mirrors. Claims above are limited to text that is directly exposed by those period manufacturer sources; missing retention/endurance quantities are treated as document-bounded negative evidence, not as proof of historical absence.