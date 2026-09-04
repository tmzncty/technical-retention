# Case 62 Grounding Record — Bell/IBM Transformer Read-Only Storage, 1950–1970

## Status

**`grounded`** for the bounded claim that IBM System/360 Model 40 TROS retained microinstructions in a fixed control-tape conductor/transformer coupling pattern, exposed that state only for runtime readout, and moved deliberate program change into **physical control-tape replacement**.

This record does **not** claim that IBM or System/360 invented transformer read-only storage, inductive translation, microprogramming, firmware, or read-only memory.

---

## Research question

What exactly is retained in the Model 40 TROS, what changes during an ordinary read, and where does update authority go when the running machine has no ordinary electrical write path to the control store?

The bounded answer is:

```text
retained bit:
    fixed drive-line / transformer link-or-bypass relation

ordinary read:
    address one drive line
    induce sense output where linked
    leave encoded control-tape routing unchanged

program change:
    physically change / replace encoded control tape(s)
```

This makes TROS a useful post-Case-60 bridge from wired fixed program topology to **service-replaceable fixed control media**.

---

## Related-repository duplication check

A GitHub search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `TROS`, `transformer read-only`, `Dimond ring`, and `System/360` transformer storage found no dedicated TROS case during this slice.

Therefore the present contribution remains in `technical-retention`, while a broader genealogy of Bell translators, IBM Hursley SCAMP, System/360 control-store engineering, cost/performance constraints, and later semiconductor ROM should be routed to `computing-archaeology` if developed.

Absence of a search hit is not evidence that the companion repository contains no relevant general magnetic-memory or System/360 context.

---

## Source ledger

| Source | Type | Exact use | What it does not prove |
| --- | --- | --- | --- |
| IBM, *System/360 Model 40 Functional Units: Field Engineering Manual of Instruction*, Fifth Edition, March 1970, SY22-2843-1, `Transformer Read Only Storage (TROS)` section | `H/P`, manufacturer field-engineering manual | TROS terminology; 56-bit / 18-field control word; fixed predetermined information; read-only runtime semantics; ROAR/ROSCAR addressing; 4K/6K/8K addressing; transformer link/bypass read principle; microinstruction/microprogram vocabulary; explicit statement that changing TROS information requires physically changing control tapes | the indexed scan does not by itself provide field-failure statistics, service labor time, or invention priority; direct PDF rendering was blocked by the archive in this run, so no claim depends on uninspected diagrams |
| P. Fagg, J. L. Brown, J. A. Hipp, D. T. Doody, J. W. Fairclough, J. Greene, `IBM System/360 Engineering`, AFIPS Fall Joint Computer Conference, 1964, pp. 205–231 | `H/P`, contemporary IBM engineering paper | standard Model 40 TROS organization; 16 modules × 256 ROS words; 128 two-word tapes per module; printed ladder networks; punched routing through/bypass transformer; TROS diagnostic-routine use | does not establish transformer-ROM priority; does not make every later Model 40 option identical to the standard 4K organization |
| D. M. Taub and B. W. Kington, `The Design of Transformer (Dimond Ring) Read-Only Stores`, *IBM Journal of Research and Development* 8(4), 1964, pp. 443–459 | `H/P`, contemporary IBM research paper | period `Transformer (Dimond Ring) Read-Only Stores` terminology and a direct IBM engineering link to the Dimond-ring class; mechanism/design context | paper title/bibliographic record alone is not enough for exact figure-level claims; this slice does not claim a full genealogy from the paper |
| Thomas L. Dimond, U.S. Patent 2,614,176, filed 1950-05-06, issued 1952-10-14 | `H/P`, primary Bell patent / prior-art anchor | inductive translator using jumpers threaded through selected coils; current through jumper energizes output windings; shows documented Bell inductive-translation practice predating System/360; references a related 1948-filed Cahill/Carpenter/Dimond application | is not an IBM control-store document; telephone-number translation is not microprogram control; does not prove component-for-component identity with Model 40 TROS |
| Bell System engineering history, *Switching Technology (1925–1975)*, bibliography to No. 5 Crossbar | `H/S`, institutional technical history | bibliographically anchors T. L. Dimond, `No. 5 Crossbar AMA Translator`, *Bell Laboratories Record* 29 (February 1951), pp. 62–68 | secondary historical compilation; not used as sole evidence for the Model 40 mechanism |
| Computer History Museum, `Memory & Storage` timeline, `Transformer Read Only Storage (TROS)` | `H/S`, museum/institutional artifact context | confirms System/360-era TROS artifact/product context and Mylar punched-strip through/around-transformer description | its wording `IBM introduces TROS` is product-history wording, not proof that IBM invented transformer ROM |

---

## Primary-source anchors

### 1. IBM March 1970 field-engineering manual — runtime authority and physical revision

The indexed text of IBM SY22-2843-1 establishes the bounded operational contract particularly cleanly.

It states that:

- TROS contains **fixed, predetermined information**;
- it **can only be read out**;
- the control word contains **56 bits grouped into 18 fields**;
- TROS can be addressed by **ROAR, ROSCAR 1, or ROSCAR 2**;
- the 4K model uses a 12-bit address while 6K/8K configurations use a 13th address bit;
- the output is called a **micro-instruction** or **TROS control word**;
- a chain of microinstructions is a **microprogram**;
- and the method of changing TROS information is to **physically change the TROS control tapes**.

The mechanism text then says that an addressed drive line is the transformer primary and the sense winding is the secondary. Where the drive line links the transformer, a pulse induces a pulse in the sense winding; where it bypasses the transformer, that sense output is absent.

This source alone is sufficient to reject two shortcuts:

```text
addressable -> writable        [false]
read-only -> never changeable  [false]
```

Model 40 TROS is finely addressable during execution yet deliberately updated outside the ordinary runtime write interface.

### Provenance limit

The Bitsavers PDF is an archival scan of the IBM manual. Search indexing exposed the relevant primary text, but direct PDF open returned HTTP 403 during this run. The case therefore does not pretend to have inspected Figure 33 visually and does not make geometry claims that require image interpretation.

---

### 2. `IBM System/360 Engineering` (1964) — carrier construction

The contemporary AFIPS paper says the finally debugged Model 40 microprogram is translated into microinstructions held in TROS.

For the standard 4096-word organization described there:

```text
16 modules
× 256 ROS words per module
= 4096 microinstructions
```

Each module contains 128 tapes with two words per tape. Each word tape carries two printed ladder networks. Punched breaks alter the current path so that the line passes through the transformer for one value or bypasses it for the other.

This grounds the case's material statement:

> **the fixed microinstruction is embodied in a prepared conductor path on a replaceable carrier.**

It also provides a useful diagnostic boundary: one TROS module stores test routines used at system reset to validate CPU/local/main storage operation. Those diagnostics are retained executable state; their existence does not prove that the TROS medium itself has undergone an exhaustive independent physical integrity check.

---

### 3. Taub/Kington (1964) — `Dimond Ring` terminology

The IBM Journal title itself is historically important:

> `The Design of Transformer (Dimond Ring) Read-Only Stores`

The use of `Dimond Ring` is sufficient here to block an isolated-System/360 narrative. The full paper is useful future archival work for exact signal-margin and construction-method analysis, but this case does not need to mine those details to establish the retention boundary.

---

### 4. Dimond patent (1950 filing / 1952 issue) — prior-art guardrail

Dimond's Bell patent describes a number-group translator using an inductive translating device. A jumper is threaded through a combination of coils identified with a desired translation. When current flows in the jumper, the output windings of the threaded coils are energized.

The patent also says a related Cahill/Carpenter/Dimond inductive-translator application had been filed on 29 October 1948.

Therefore the safe chronological statement is:

> **inductive information translation by wire/coil threading was documented at Bell before the 1964 System/360 TROS.**

This is deliberately narrower than `Dimond invented all transformer ROM in year X`.

---

### 5. CHM timeline — artifact/product witness, not invention priority

The Computer History Museum's memory/storage timeline describes System/360-era TROS and says punched Mylar strips control whether current flows through or around each transformer to represent the two binary values.

Its sentence that IBM `introduces` TROS with the IBM 360 is read here as museum product-history language. In light of the Bell prior art above, it is **not** used to assign invention priority.

That provenance distinction is important enough to retain in the case because an unsafely compressed timeline can otherwise generate a false claim:

```text
System/360 product introduction
        ≠
first invention of transformer read-only storage
```

---

## Mechanism reconstruction

### Retained state

```text
prepared control tape
    + printed drive-line route
    + link / bypass relation at transformer position
        ↓
fixed microinstruction pattern
```

### Runtime read

```text
ROAR / ROSCAR address
        ↓
select drive line
        ↓
current pulse
        ↓
linked transformer -> induced sense pulse
bypassed transformer -> no corresponding pulse
        ↓
TROS control word / microinstruction
```

The state-bearing conductor route is not consumed by this operation.

### Deliberate revision

```text
new desired microinstruction pattern
        ↓
new / changed encoded control tape
        ↓
physical service replacement
        ↓
new TROS information becomes current
```

The old carrier can remain physically legible after supersession. This is not secure erasure.

---

## Retention semantics

### Retained payload (`E` from primary mechanism)

The bounded payload is the microinstruction bit pattern embodied in conductor routing/coupling geometry.

### Volatility (`E`)

The state-bearing route survives loss of operating current as physical geometry. Ordinary electronic read service still requires powered drivers, transformers/sense circuits, addressing, latching, and downstream control logic.

Therefore:

> **power-independent payload embodiment ≠ power-independent machine availability.**

### Maintenance (`H/E`)

No periodic refresh of the control-tape pattern is established. Retention still depends on physical carrier integrity, correct installation/configuration, working sensing/addressing circuitry, and deliberate service procedures when revision is required.

### Read (`H/P`)

Read is inductive and logically nondestructive with respect to the fixed route.

### Write / erase (`H/P`)

No ordinary runtime electronic write/erase path is established. IBM explicitly relocates information change to physical control-tape change.

### Currentness (`E`)

A removed older tape can survive physically after a replacement becomes authoritative for the machine. Thus **physical survival and current configured program are distinct relations**.

---

## Claim classification

### Historical record (`H/P`)

Established:

- Model 40 TROS is read-only control storage;
- its output is microinstruction/control-word state used to control machine operation;
- link/bypass drive-line geometry determines sensed values;
- control tapes physically carry the word pattern;
- changing TROS information requires physical control-tape change;
- Bell inductive translators using thread-through-coil relations predate System/360.

### Engineering reconstruction (`E`)

Supported:

- magnetic transduction is not the same as magnetic-state payload retention;
- runtime read-only is an authority/interface property rather than absolute physical immutability;
- retained payload and sensing recoverability are separate;
- quiescent retention can shift maintenance burden toward manufacture/configuration/service rather than refresh;
- replacement can change currentness before destroying prior physical state.

### Functional analogy (`A`)

Allowed only with limits:

- **Apollo core rope:** useful for state-bearing topology vs magnetic transduction; not identical construction or direct causal genealogy;
- **mask ROM / firmware image:** useful for runtime read-only/currentness comparison; not physical identity;
- **hot-swappable immutable image:** useful only as a modern service-authority analogy.

### Philosophical interpretation (`I`)

Bounded interpretation:

- `read-only` is relational to an operational layer and authority;
- stability can be produced by moving mutation out of the fast operational path and into a slower material replacement path.

Rejected:

- TROS proves a universal philosophy of memory;
- read-only means metaphysically unchangeable;
- magnetic transformer means magnetic-remanent payload;
- replaceable carrier means erasable memory in the EEPROM/Flash sense.

---

## Prior-art / novelty boundary

### Established no later than the bounded record

- **1948:** the Dimond 1950-filed patent references a related Cahill/Carpenter/Dimond inductive-translator filing from 1948;
- **1950:** Dimond files U.S. 2,614,176 for an electronic induction number-group translator;
- **1951:** Bell Laboratories Record publishes `No. 5 Crossbar AMA Translator`;
- **1952:** Dimond patent issues;
- **1964:** Taub/Kington publish `Transformer (Dimond Ring) Read-Only Stores`; Fagg et al. document Model 40 TROS carrier construction in the System/360 engineering paper;
- **1970:** IBM field-engineering manual directly specifies the Model 40 read-only/change-control-tape semantics used here.

### Explicitly not claimed

- first read-only memory;
- first microprogram control store;
- first transformer memory;
- first wired ROM;
- first inductive translator;
- direct Bell → IBM component continuity without additional genealogy work;
- direct IBM TROS → semiconductor ROM descent.

The contribution is **retention-specific comparison**, not priority reassignment.

---

## Cross-case consequences

### Case 02 — classic magnetic-core RAM

```text
Case 02:
    bit = remanent magnetic state
    destructive read may create rewrite obligation

Case 62:
    bit = fixed conductor / transformer coupling relation
    read energizes transformer path without rewriting carrier
```

Finding:

> **magnetic component family ≠ magnetic-state payload family.**

### Case 60 — Apollo core rope

```text
Case 60:
    fixed program in sense-wire/core topology
    new program moves through rope manufacture/module replacement

Case 62:
    fixed microinstruction in printed control-tape/transformer topology
    IBM explicitly permits physical control-tape replacement
```

Finding:

> **topology-coupled sensing ≠ one update/service geometry.**

The Model 40 case is valuable precisely because it prevents Case 60 from being over-generalized into `wired fixed memory means whole-module remanufacture`.

### Cases 11–13 — floating-gate ROM/EEPROM/Flash bridge

The relevant axis is update authority:

```text
TROS        -> physical tape replacement
EPROM       -> electrical program + external radiation erase
EEPROM      -> electrical erase/program
Flash       -> electrical coarse erase + finer program/read
```

No teleological sequence is claimed. The comparison shows that `nonvolatile` or `read-only` alone does not determine how deliberate forgetting/revision occurs.

---

## Findings promoted to CASE_INDEX

The following relations are strong enough for the cross-case ledger:

1. **runtime read-only ≠ lifecycle immutable**;
2. **magnetic transduction ≠ magnetic-state payload retention**;
3. **fine runtime addressability ≠ fine runtime update authority**;
4. **state-bearing control-tape route ≠ sensing-transformer state**;
5. **read-only ≠ physically inactive**;
6. **physical control-tape replacement ≠ in-place electronic write**;
7. **superseded carrier survival ≠ current configured program**;
8. **fixed microprogram ≠ hardwired combinational logic**;
9. **retained executable diagnostic code ≠ automatic proof of medium integrity**;
10. **power-independent payload geometry ≠ power-independent service availability**;
11. **shared topology-coupled readout ≠ same carrier/revision regime**;
12. **System/360 product introduction ≠ transformer-ROM invention priority**;
13. **control-store role identity ≠ physical ROS mechanism identity**;
14. **quiescent retention ≠ zero lifecycle retention labor**;
15. **configuration forgetting ≠ physical sanitization**;
16. **Model 40 TROS ≠ Apollo core rope ≠ classic writable core RAM**.

---

## Evidence limits / future work

- Direct rendering of the Bitsavers IBM manual failed with HTTP 403 in this run; exact textual claims are grounded in indexed primary text, not image interpretation.
- A directly inspected Taub/Kington facsimile should precede any future argument about exact transformer turns ratio, `ZERO` current, worst-case bit pattern, or signal margins.
- A broader Bell Model VI / No. 5 Crossbar → IBM Hursley SCAMP → System/360 genealogy belongs in `computing-archaeology` unless a retention-specific question requires it here.
- Field-engineer replacement procedures, configuration records, error rates, and repair times remain ungrounded.
- CCROS/BCROS are neighboring counterexamples, not silently absorbed into TROS.

---

## Source references

- IBM, *System/360 Model 40 Functional Units: Field Engineering Manual of Instruction*, Fifth Edition, March 1970, SY22-2843-1: <https://bitsavers.org/pdf/ibm/360/fe/2040/SY22-2843-1_Model_40_Functional_Units_Mar70.pdf>.
- P. Fagg et al., `IBM System/360 Engineering`, *Proceedings of the 1964 Fall Joint Computer Conference*, pp. 205–231: <https://researchr.org/publication/FaggBHDFG64>; text mirror of CHM collection scan: <https://paperzz.com/doc/9212284/ibm-system-360-engineering>.
- Daniel M. Taub and Brian W. Kington, `The Design of Transformer (Dimond Ring) Read-Only Stores`, *IBM Journal of Research and Development* 8(4), 1964, pp. 443–459, DOI 10.1147/rd.84.0443: <https://dblp.org/rec/journals/ibmrd/TaubK64>.
- Thomas L. Dimond, U.S. Patent 2,614,176, `Electronic Induction Number Group Translator`, filed 6 May 1950: <https://patents.google.com/patent/US2614176A/en>.
- Bell System, *A History of Engineering and Science in the Bell System: Switching Technology (1925–1975)*, bibliography citing T. L. Dimond, `No. 5 Crossbar AMA Translator`, *Bell Laboratories Record* 29 (February 1951), pp. 62–68: <https://www.telephonecollectors.info/index.php/browse/document-repository/catalogs-manuals/bell-system-we/history-books-1/11365-btl-history-switching-technology-1982-opt-r/file>.
- Computer History Museum, `Memory & Storage` timeline, `Transformer Read Only Storage (TROS)`: <https://www.computerhistory.org/timeline/memory-storage/>.