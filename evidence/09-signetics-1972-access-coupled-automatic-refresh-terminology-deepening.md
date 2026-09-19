# Evidence 09 — Signetics 1972 access-coupled `automatic refresh` terminology deepening

**Status:** `bounded deepening complete`

**Parent case:** [`../cases/09-dram-cbr-refresh-address-internalization.md`](../cases/09-dram-cbr-refresh-address-internalization.md)

**Adjacent records:**

- [`09-1972-1975-1103-refresh-product-contract-deepening.md`](09-1972-1975-1103-refresh-product-contract-deepening.md)
- [`09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md`](09-gte-1971-1973-self-initiating-refresh-system-boundary-deepening.md)
- [`09-1973-1982-early-self-refresh-control-partitions-prior-art-deepening.md`](09-1973-1982-early-self-refresh-control-partitions-prior-art-deepening.md)
- [`09-micron-1999-sdram-auto-vs-self-refresh-deepening.md`](09-micron-1999-sdram-auto-vs-self-refresh-deepening.md)

**Bounded question:** what did `automatic refresh` mean in named 1972 Signetics dynamic-RAM product documentation, and does that wording by itself establish autonomous recurring refresh cadence or internal whole-array traversal?

This is intentionally **not** a general Signetics product history, a claim of first use of the word `automatic`, a shipment chronology, a reconstruction of transistor-level refresh circuitry, or a genealogy from Signetics to later CAS-before-RAS / self-refresh designs. It is a terminology-and-control-boundary slice for Case 09.

---

## Result in one sentence

Signetics' 1972 MOS handbook uses `AUTOMATIC REFRESH DURING READ (2 ms)` for the advance-specification 2548 and says the 2601's cell refresh is accomplished `automatically during row (A0-A4) addressing`, while the detailed 2548 operation refreshes the **addressed column** and the 2601 still exposes ordinary external row-address inputs; therefore, in these period product pages, `automatic` can describe restoration coupled to an addressed access/refresh operation and does **not by itself** prove autonomous recurrence, an internal timer, or an internal whole-array refresh walker.

The bounded decomposition is:

```text
restoration happens automatically once a qualifying access/address is exercised
    !=
qualifying accesses are generated automatically over time
    !=
all required maintenance addresses are traversed automatically
    !=
self-refresh mode / autonomous recurring cadence
```

This is a terminology correction, not a priority claim.

---

## Sources and inspection boundary

### P1 — Signetics Corporation, 1972 MOS handbook

- Corporate author: **Signetics Corporation**.
- Copyright: **1972**.
- Direct page-preserving scan: <https://archive.decromancer.ca/bitsavers.org/components/signetics/_dataBooks/1972_Signetics_MOS.pdf>.
- Alternate page-preserving mirror: <https://device.report/m/dafd5c77c72a981090c96e4a55aefea73e10f1e24d60e279806c3cf4fb8a94a5.pdf>.
- Directly inspected printed pages:
  - p. 23 — 1103 / 1103-1, already grounded in the adjacent Evidence 09 product-contract record;
  - p. 121 — `2548`, **Fully Decoded, 2048-Bit Random Access Memory**, `ADVANCE SPECIFICATION`;
  - p. 125 — `2601`, **Fully Decoded, High Speed, 1024-Bit Dynamic, Random Access Memory**, `ADVANCED SPECIFICATION`.

The handbook's front matter explicitly warns that it contains information on newly announced products and that preliminary data may change without notice. This evidence therefore treats the 2548 and 2601 pages as **manufacturer-authored 1972 product documentation / announced-product specifications**, not as proof of production volume, exact shipment date, or final silicon behavior.

A source-level anomaly is preserved rather than silently normalized: the p. 121 heading, package identification, table of contents, and device number all say **2548**, while the first sentence of the description reads `Signetics 2458`. The transposed digits are treated here as an apparent document typo. No claim depends on silently rewriting that line.

### P2 — contemporaneous Signetics advertisement, December 1972

- *Electronic Design*, vol. 20, no. 25, 7 December 1972, Signetics advertisement.
- Page-preserving scan: <https://www.worldradiohistory.com/Archive-Electronic-Design/1972/Electronic-Design-V20-N25-1972-1207.pdf>.

The advertisement invites readers to ask about Signetics' N-channel dynamic `2601`, giving a 1024 × 1 organization and fast access. It is used only as a bounded **same-year public marketing witness that the 2601 was being offered/advertised as a named device**. The ad does not repeat the handbook's refresh mechanism and does not prove a shipment date. Its explicit `in production now` language is attached to the static 2602, not automatically transferred to the 2601.

### Related-repository check

A fresh `tmzncty/computing-archaeology` search for `2548`, `2601`, `Signetics`, and refresh found no dedicated packet to reuse. Broader Signetics product history, silicon-gate/N-channel process history, commercial shipment chronology, and early DRAM vendor competition remain companion-repository work.

---

## Historical record

### H/P — the same 1972 handbook already gives a non-automatic 1103 coverage/deadline contract

The adjacent Evidence 09 record has already directly grounded the Signetics 1103 page. The 1972 handbook says that refreshing all 1,024 bits is accomplished in **32 read cycles** and is required every **two milliseconds** for the documented 0–70 °C ambient range.

That material is not re-developed here. It supplies an important same-book control:

```text
1103
    whole-array coverage obligation stated explicitly
    + deadline stated explicitly
    + read cycles named as the restorative primitive
```

The 2548 and 2601 pages use different wording and expose different coupling between ordinary address activity and restoration.

### H/P — 2548 is described as a 2048 × 1 dynamic RAM with built-in refresh amplifiers

The p. 121 `2548` advance-specification page describes a fully decoded **2048 × 1 dynamic random-access memory** implemented with P-channel devices and says that it contains **built-in refresh amplifiers**.

The feature list includes the exact period phrase:

> `AUTOMATIC REFRESH DURING READ (2 ms)`

The page also exposes ordinary address inputs and three external non-overlapping clock inputs.

Historical record stops there unless the detailed operation supplies more.

### H/P — 2548 detailed operation ties restoration to the addressed column

The same p. 121 page gives a five-period operation sequence.

During period 2, the row and column decoders select the desired bit. During period 5:

- if a write is desired, the selected bit is written and the other bits sharing the **same addressed column** are inverted and refreshed; the corresponding bit of the column inversion memory is also inverted/refreshed;
- if a refresh is desired, the bits sharing the **same addressed column** are inverted and refreshed, and the corresponding column-inversion-memory bit is also inverted/refreshed.

The block diagram on the continuation page identifies a **32-bit column inversion memory**.

The historical point is narrow but strong:

```text
marketing/feature phrase
    `automatic refresh during read`

coexists with detailed operation
    refresh work qualified by the currently addressed column
```

The page does **not** document, in the inspected material, a free-running refresh oscillator or an autonomous internal whole-array traversal counter.

Absence from this page is not proof that no undocumented circuitry existed. The supported claim is about the published interface/operation description.

### H/P — 2601 says refresh occurs automatically during row addressing

The p. 125 `2601` advanced-specification page describes a **1024 × 1 dynamic random-access memory**.

Its description says:

> cell refresh is accomplished automatically during row (`A0-A4`) addressing.

The same page gives:

- a `REFRESH TIME ... 2 ms` feature;
- a block diagram with a **32 rows × 32 columns** memory matrix;
- a `1 OF 32 ROW DECODER`;
- `SENSE AND REFRESH AMPLIFIERS`;
- ordinary address pins including `Address 0` through `Address 4` for the row-address subset named in the description.

The page therefore documents an access/address-coupled restorative action in a named dynamic RAM.

### H/P — `automatic` and `self-initiating` are not interchangeable period terms

The Signetics pages do not use GTE's 1973 patent phrase `self-initiating refresh means` for these product behaviors.

In GTE's separately grounded system, a free-running external memory-system clock, pulse generator, row counter, address gating, and `memory busy` relation cause recurring refresh without one CPU refresh command per event.

The Signetics 2548/2601 pages instead describe restoration tied to an addressed read/refresh or row-addressing event.

Thus, already in a very narrow 1972–1973 window:

```text
`automatic` restoration within an addressed operation
    !=
`self-initiating` recurring maintenance at the memory-system boundary
```

This is a historical vocabulary distinction backed by mechanisms, not a claim that all authors used the words consistently.

### H/P — both 2548 and 2601 are preliminary/advance-specification witnesses

The 2548 page is labeled `ADVANCE SPECIFICATION`; the 2601 page `ADVANCED SPECIFICATION`. The handbook front matter says newly announced product information is preliminary and may change without notice.

Therefore these pages support:

```text
public manufacturer documentation in 1972
```

but do not by themselves establish:

```text
mass production
exact shipment date
unchanged final specification
field deployment
```

The December-1972 Signetics advertisement strengthens only the public named-device witness for the 2601; it does not close those production questions.

---

## Engineering reconstruction

### E — automatic local restoration and autonomous recurrence are different control properties

The 2548 and 2601 material lets Case 09 split an overloaded word more finely.

For an addressed operation, the chip can perform restoration without an external pin saying `rewrite this row/column now`. That is one kind of automation:

```text
qualifying access/address event
    -> internal sense/refresh work follows automatically
```

But a deadline-driven array still needs the required maintenance population to be exercised in time:

```text
all required rows/columns
    -> must receive qualifying restorative events
    -> before the relevant retention deadline
```

Who guarantees that traversal is a separate question.

Therefore:

```text
automatic restoration primitive
    != automatic event cadence
    != automatic coverage traversal
```

### E — ordinary workload can contribute to maintenance without proving maintenance sufficiency

For the 2601, row addressing itself is described as accomplishing refresh. For the 2548, the feature label and detailed operation tie refresh work to read/addressed-column behavior.

It is therefore reasonable to say that useful accesses can **discharge part of the retention obligation** for the locations they touch.

It is not reasonable to infer:

```text
normal workload
    -> necessarily visits every required maintenance unit
    -> within every 2 ms interval
```

unless a source establishes such a workload or a separate refresh schedule.

The bounded relation is:

```text
access can perform maintenance
    != workload guarantees coverage
```

### E — a refresh amplifier is an executor, not necessarily a scheduler

The 2548 advertises built-in refresh amplifiers; the 2601 block diagram shows sense-and-refresh amplifiers.

These document restoration machinery close to the payload array. They do not, by their existence alone, establish:

- a timer;
- a refresh-address counter;
- autonomous mode entry;
- complete array traversal.

This sharpens the Case-09 function decomposition:

```text
refresh executor / restorer
    != cadence authority
    != enumerator / coverage state
```

### E — 2601 shows address-source authority can remain external even when restoration is automatic

The 2601 page names row inputs `A0-A4`, a 1-of-32 row decoder, and automatic refresh during row addressing.

At the documented interface, the row address still arrives through ordinary address inputs. The chip automates restoration **after row selection**, but the inspected page does not describe an internal row walker choosing later rows independently.

Thus:

```text
internal restoration
    + externally supplied maintenance-relevant row selection
```

is another control partition distinct from later CBR:

```text
externally triggered refresh
    + internally generated refresh row
```

No genealogy between the two is asserted.

### E — 2548 adds a maintenance-unit warning: row and column are not universal refresh units

Case 09 often discusses row refresh because later DRAM sources do. The 2548 detailed operation instead describes refreshing bits sharing the **addressed column**, together with column-inversion state.

Therefore the project should not silently universalize `row` into a timeless synonym for `refresh unit` across all early dynamic memories.

The bounded rule is:

> **maintenance unit must be recovered from the actual device architecture and period documentation.**

This is especially important when comparing early product pages with later RAS/CBR interfaces.

### E — same-year product vocabulary can hide different mechanism partitions

Within one manufacturer handbook and one year, the checked pages expose at least three descriptions:

```text
1103
    full coverage = 32 read cycles / 2 ms

2548
    `automatic refresh during read`
    + addressed-column/inversion-memory refresh sequence

2601
    refresh automatically during row addressing
    + 32-row matrix
    + 2 ms refresh time
```

This is not a complete taxonomy of Signetics DRAM. It is enough to reject the shortcut that one word such as `automatic` uniquely identifies scheduler locus or refresh-address authority.

---

## Functional comparison

### A — comparison to GTE 1973 is about cadence authority only

GTE's already-grounded system can initiate recurring refresh from a free-running memory-system clock and advance a row counter even when the CPU has not asked for a useful memory access.

The Signetics 2548/2601 pages instead show automatic restoration **conditioned by access/address activity** in the published product description.

Functional contrast:

```text
access-coupled automatic restoration
    vs
system-level self-initiating recurring maintenance
```

This does not prove that one influenced the other.

### A — comparison to TI CBR is about maintenance-address source only

Later TI CBR evidence says external ordinary address inputs are ignored for a CBR refresh while an internal counter supplies the refresh row.

The Signetics 2601 page instead exposes row address inputs and says refresh is automatic during row addressing.

Functional contrast:

```text
2601 documented path
    externally supplied row selection
    -> internal restorative work

later bounded CBR path
    external refresh event
    -> internal counter supplies row selection
    -> internal restorative work
```

This is not a direct historical descent claim.

### A — comparison to Micron 1999 AUTO/SELF REFRESH is about the word `automatic`

Micron's later SDRAM distinguishes a one-shot `AUTO REFRESH` command from a persistent `SELF REFRESH` regime with internal recurring clocking.

The 1972 Signetics evidence shows why a modern reader must not infer that the earlier adjective `automatic` already meant the later SELF REFRESH control partition.

The comparison is lexical/functional only:

```text
same family of autonomy words
    != same interface contract
    != same scheduler ownership
    != same historical concept
```

---

## Philosophical / media-theoretical interpretation

### I — automation can name a local relation rather than system-wide autonomy

The technical fact is simple: a device may perform restorative work automatically **once another actor has supplied the address or access event that occasions it**.

This disciplines any broader claim about technological autonomy. What disappears from one interface may survive as an obligation elsewhere:

```text
user does not explicitly command rewrite
    !=
no one/system must ensure timely coverage
```

The useful conceptual question is therefore not `is refresh automatic?` in the abstract, but:

- automatic relative to which actor or interface?
- which event is still externally caused?
- who owns recurrence?
- who owns traversal?
- who owns the deadline?

That is an engineering-grounded interpretation, not a claim that the 1972 designers were articulating a philosophy of autonomy.

### I — maintenance can be parasitic on useful access without being reducible to use

The checked product pages show useful-address activity and state-preservation work sharing an operation path.

This is conceptually useful because it separates:

```text
maintenance triggered by use
```

from:

```text
maintenance guaranteed by use
```

The first can be true while the second remains false unless coverage and deadline conditions are satisfied.

No analogy to biological memory or human recollection is required.

---

## Explicit non-claims

This evidence does **not** claim that:

1. Signetics invented automatic DRAM refresh;
2. `automatic refresh` first appeared in 1972;
3. the 2548 definitely shipped in production quantity;
4. the 2601 definitely shipped on a specific date;
5. the p. 121 `2458` body text names a different device from the heading/package's 2548;
6. the handbook's preliminary values were unchanged in final production;
7. every read to the 2548 alone guarantees whole-array refresh coverage;
8. every ordinary workload on the 2601 necessarily covers all 32 rows within 2 ms;
9. the 2548 contains a free-running refresh timer;
10. the 2601 contains an internal refresh-row counter;
11. absence of such blocks from the inspected simplified diagrams proves they did not exist physically;
12. `automatic refresh during read` is equivalent to later CAS-before-RAS refresh;
13. `automatic refresh during read` is equivalent to later SELF REFRESH;
14. the 2548's addressed-column maintenance is physically identical to later row-oriented DRAM refresh;
15. the 2548 and 2601 use the same cell design;
16. the 1103, 2548, and 2601 form a demonstrated product genealogy;
17. GTE's 1973 system controller was designed from the Signetics 2548/2601 mechanism;
18. later TI CBR or Micron SELF REFRESH descends from these Signetics products;
19. `automatic` had one stable industry-wide technical definition in 1972;
20. a 2 ms number has one universal physical meaning across the 1103, 2548, 2601, or later DRAM.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Signetics' 1972 MOS handbook is manufacturer-authored and explicitly marks newly announced product data as preliminary | H/P | direct front matter |
| The p. 121 heading identifies device 2548 as a fully decoded 2048-bit RAM and labels it an advance specification | H/P | direct page inspection |
| The first description line says `2458` although heading/package/table of contents say 2548 | H/P | direct page inspection; preserved as source anomaly |
| The 2548 page describes a 2048 × 1 dynamic RAM with built-in refresh amplifiers | H/P | direct p. 121 text |
| The 2548 feature list says `AUTOMATIC REFRESH DURING READ (2 ms)` | H/P | direct p. 121 text |
| 2548 period-5 write/refresh operation refreshes bits sharing the addressed column and corresponding column-inversion state | H/P | direct p. 121 detailed operation |
| The 2548 block diagram names a 32-bit column inversion memory | H/P | direct page-preserving inspection |
| The 2601 page describes a 1024 × 1 dynamic RAM whose cell refresh occurs automatically during row (`A0-A4`) addressing | H/P | direct p. 125 text |
| The 2601 page gives `REFRESH TIME ... 2 ms` and a 32-row × 32-column matrix | H/P | direct p. 125 text/diagram |
| A December-1972 Signetics advertisement publicly names and markets the 2601 dynamic RAM | H/P | contemporaneous corporate advertisement; shipment not inferred |
| In these pages, `automatic` restoration does not by itself establish autonomous recurrence or traversal | E | bounded reconstruction from address-coupled operation + absence of such a published contract |
| Useful access can discharge maintenance for the addressed unit without proving whole-array deadline coverage | E | bounded mechanism reconstruction |
| Refresh executor location, cadence authority, and traversal/address authority are separate properties | E | cross-source Case-09 decomposition |
| `automatic refresh` is historically identical to later SELF REFRESH | X | explicitly unsupported |
| 1972 Signetics → later CBR/SELF REFRESH is a demonstrated genealogy | X | explicitly unsupported |

---

## Related-repository routing

### `tmzncty/computing-archaeology`

A fresh search found no dedicated 2548/2601 packet to reuse. A fuller treatment should live there if pursued:

- Signetics 2500/2600-series product chronology;
- silicon-gate and N-channel process constraints;
- exact cell/refresh-amplifier circuits;
- production and shipment evidence;
- customer/system adoption;
- comparison with Intel, Mostek, TI, MOS Technology, and other early DRAM vendors;
- later quasi-static / pseudo-static memory genealogy.

This repository retains only the control/retention seam:

```text
restoration automatically follows an addressed operation
    !=
recurring maintenance cadence is autonomous
    !=
maintenance coverage traversal is autonomous
```

### `tmzncty/problem-history`

The source is a useful anti-anachronism check. Period words such as `automatic refresh`, `self-initiating refresh`, `self-refreshing memory`, `AUTO REFRESH`, and `SELF REFRESH` must be reconstructed from their actual circuits/interfaces rather than mapped onto one timeless modern category.

---

## Remaining evidence debt

This bounded slice is complete, but the following remain deliberately open:

1. locate later Signetics production datasheets or data books that show whether the 2548 and 2601 specifications changed after the 1972 advance-specification pages;
2. establish exact announcement / first-shipment / production chronology for 2548 and 2601 if that becomes historically important;
3. recover a transistor/circuit-level source for the 2548 column-inversion refresh mechanism rather than inferring beyond the manufacturer block/operation description;
4. determine whether period application notes documented an explicit external schedule for guaranteeing full 2548/2601 coverage;
5. trace broader vendor terminology only in `computing-archaeology`, unless it changes the retention-control boundary here.

None of those debts blocks the bounded conclusion that **1972 manufacturer product documentation used `automatic refresh` for access/address-coupled restoration without thereby documenting autonomous recurring cadence or autonomous whole-array traversal.**
