# IBM System/360 Model 40 TROS: Runtime Read-Only State in Replaceable Transformer Control Tapes

## Scope

- **Object / system:** IBM System/360 Model 40 Transformer Read Only Storage (TROS), bounded to the control-store organization documented for the 2040 Processing Unit;
- **Date range:** 1964–1970 for the principal IBM evidence, with a Bell System inductive-translator prior-art anchor from 1950–1952;
- **Why this case matters for technical retention:** the Model 40 stores microinstructions in a physically fixed conductor/transformer relation that is read-only during ordinary machine operation, yet IBM explicitly makes the retained information service-replaceable by physically changing the TROS control tapes.

This case does **not** attempt a general history of microprogramming, System/360, ROM, firmware, Bell translators, or magnetic memory. It isolates a narrower question:

> What kind of retention is produced when ordinary electrical execution can only read a fixed control store, but a technician can change the current program by replacing the encoded physical carrier?

It follows [`Case 60`](60-apollo-core-rope-wired-topology.md) without collapsing the two systems. Both use transformer coupling and manufactured conductor geometry, but they organize bits, carriers, access, and revision differently.

A repository search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for TROS / Dimond-ring / System/360 transformer-ROM material found no dedicated case during this slice, so this file keeps the history bounded to the retention argument rather than duplicating a parallel technical survey.

---

## Historical vocabulary

IBM's March 1970 Model 40 field-engineering manual uses the explicit period term **`Transformer Read Only Storage (TROS)`**. It describes the TROS control word as 56 bits divided into 18 fields, calls its information **fixed** and **predetermined**, says it **can only be read out**, and calls the output word a `micro-instruction` or `TROS control word`. A chain of such words is a `microprogram`.[^ibm-fe]

The same manual is unusually useful for update semantics. It states that the way to change the TROS information is to **physically change the TROS control tapes**.[^ibm-fe]

The 1964 AFIPS paper *IBM System/360 Engineering* independently describes the Model 40 implementation as sixteen TROS modules, each containing 256 read-only-store words. Each module contains 128 tapes, each tape two words; its printed ladder networks are modified according to the desired microinstruction pattern.[^fagg]

The modern project phrase `replaceable fixed state` below is therefore an engineering reconstruction. IBM's own vocabulary is stronger and more precise: `read only storage`, `control tape`, `micro-instruction`, and `microprogram`.

---

## Retained state: coupling geometry, not one ferrite remanence per bit

IBM's Model 40 manual gives the operating principle directly:

```text
addressed drive line links transformer  -> sense pulse -> 1
addressed drive line bypasses transformer -> no sense pulse -> 0
```

The drive line acts as the transformer primary and the sense winding as the secondary. A selected current pulse induces output where the drive line links the transformer; bypass positions do not produce the corresponding induced pulse.[^ibm-fe]

The 1964 engineering paper describes the physical carrier in more detail. Each word tape carries printed ladder networks. A punched break routes current so that the line passes through the transformer for one value or bypasses it for the other.[^fagg]

The retained logical distinction is therefore not best described as a binary remanent magnetic polarity left behind in a ferrite element. It is a **manufactured conductor-routing / mutual-inductance relation** that the transformer read path transduces when addressed.

That gives the first central distinction:

> **magnetic transduction ≠ magnetic-state payload retention.**

Ferrite/transformer material participates in reading the program, but the current microinstruction pattern is encoded by the physical routing of the control-tape conductors.

This sharply limits any analogy with classic read/write magnetic-core memory from Case 02. Shared use of magnetic material is not enough to establish shared retention semantics.

---

## Addressability: selecting a fixed word does not make the word writable

The field-engineering manual separates addressability from mutability. It says TROS can be addressed through the Read Only Address Register (ROAR) or ROSCAR registers and uses a 12-bit address for a 4K TROS and a 13th bit on 6K/8K configurations.[^ibm-fe]

That supports a useful relation:

```text
fine runtime addressability
        does not imply
fine runtime update authority
```

A specific microinstruction can be electrically selected and repeatedly recovered, yet ordinary execution has no corresponding electrical write path that changes the punched control-tape routing.

The output is operational rather than archival: the microinstruction directly controls data flow, special circuitry, selection of the next TROS address, and parity checking.[^ibm-fe]

So the retained state is not merely a document read by an operator. It is executable machine-control state whose **read path is runtime-active while its update path is service/physical**.

---

## Read semantics: logical nondestructiveness without zero physical activity

An ordinary TROS read sends a current pulse through the selected drive line. The transformer coupling produces or does not produce a sense pulse according to the fixed route.[^ibm-fe]

Nothing in that read operation punches or re-routes the control tape. The bit-defining physical relation survives the sensing event.

Accordingly:

> **read-only ≠ physically inactive.**

Current changes and transformer induction are required to recover a word, while the encoded conductor geometry remains unchanged.

This is another reason not to use `read-only` as a synonym for `nothing physical happens`. What is invariant is the **state-bearing relation**, not every instantaneous electrical or magnetic condition in the read path.

The correct comparison with Case 60 is functional, not genealogical identity:

```text
Apollo core rope:
    sense-wire thread/bypass relation carries program bit
    selected core switches/reset during read

IBM Model 40 TROS:
    printed drive-line routing through/bypass transformer carries bit
    addressed current pulse is inductively sensed
```

Both show that a state-bearing topology can be read through magnetic transduction. They do not use the same organization, bit density, carrier construction, or maintenance workflow.

---

## Write / revision semantics: read-only at runtime, replaceable in service

The most important Model 40 retention fact is IBM's explicit separation between runtime access and lifecycle modification.

The manual says TROS contains fixed, predetermined information that can only be read out, while changing that information requires physically changing the TROS control tapes.[^ibm-fe]

The 1964 engineering paper explains why that statement is physically meaningful: the microinstruction bit pattern is prepared in the printed ladder network on the word tape. Changing the encoded program therefore means changing the physical carrier pattern rather than issuing an ordinary machine write.[^fagg]

This yields a stronger distinction than the generic phrase `ROM is immutable`:

> **runtime read-only ≠ lifecycle immutable.**

A service action can replace the carrier and thereby change which microprogram is current without converting TROS into a writable memory during normal execution.

The transition is approximately:

```text
new microprogram / corrected microinstruction pattern
        ↓
newly encoded control tape(s)
        ↓
physical service replacement
        ↓
new fixed TROS state becomes current
```

The old tape may still physically embody the previous bit pattern after removal. Thus:

> **program supersession ≠ physical disappearance of the superseded carrier.**

This is a currentness relation, not secure erasure.

---

## Retention work: little runtime renewal, nontrivial lifecycle organization

The control-tape bit pattern does not require periodic electrical refresh analogous to DRAM merely to remain encoded. The conductor geometry survives idle intervals and loss of operating current as a physical arrangement.

That statement is an **engineering reconstruction** from the mechanism, not an IBM guarantee of indefinite archival life.

The case therefore separates two kinds of retention work:

1. **runtime retention work:** no periodic reconstruction of the encoded tape pattern is established for the bounded TROS;
2. **lifecycle retention work:** manufacture, configuration control, physical protection, diagnosis, service replacement, and verification are necessary if the intended microprogram is to remain the one the machine executes.

The 1964 engineering paper also notes that one TROS module provided diagnostic routines used on system reset to validate CPU and storage operation.[^fagg] That is not a refresh mechanism for TROS bits; it is evidence that **retained control state can participate in validating the rest of the machine**.

So:

> **retained diagnostic program ≠ proof that the retained program itself has been revalidated at the physical-bit level.**

The repository should keep diagnostic use, physical carrier integrity, and logical microprogram correctness distinct.

---

## Failure and forgetting

### Loss or damage of the encoded control tape

If the printed route, punched pattern, connector, or mechanical carrier is damaged so that the intended current path changes or cannot be selected, the retained microinstruction may become unreadable or incorrect even though the transformer assembly remains present.

This is an engineering failure mode implied by the mechanism; the bounded sources do not provide a statistical field-failure distribution.

### Sense / transformer path failure

A control tape can remain correctly encoded while the transformer/sense electronics no longer recover the intended value. Therefore:

> **payload-bearing geometry ≠ recoverability infrastructure.**

Physical survival of the tape pattern does not by itself prove successful executable recovery.

### Service replacement

Replacing control tapes can make the previous program non-current without erasing the removed tapes. This is **configuration forgetting**, not physical sanitization.

### Mis-encoding

Because the physical tape pattern directly determines the fixed word, fabrication or preparation error can become logical microinstruction error. In this regime, carrier correctness is information correctness.

---

## Prior art: IBM System/360 is not the origin of inductive wired translation

The title of Taub and Kington's 1964 IBM Journal paper — *The Design of Transformer (Dimond Ring) Read-Only Stores* — already places the IBM work in a `Dimond Ring` technical category rather than presenting transformer read-only storage as an invention without antecedents.[^taub]

A stronger primary prior-art anchor is Thomas L. Dimond's Bell Telephone Laboratories patent, U.S. 2,614,176, filed 6 May 1950. It describes an **electronic induction number group translator** in which a jumper is threaded through selected coils; a current surge energizes the output windings of the coils through which the jumper passes. The patent also cites a related Cahill/Carpenter/Dimond application filed in 1948.[^dimond]

Bell's later engineering history bibliographically identifies Dimond's contemporary article `No. 5 Crossbar AMA Translator`, *Bell Laboratories Record* 29 (February 1951), pp. 62–68.[^bell-history]

The safe historical claim is therefore:

> **By 1950–1952, Bell had documented inductive translation based on jumper/coil threading; IBM's 1964 Model 40 TROS is a later, machine-specific control-store implementation in the broader Dimond-ring / transformer-read-only family.**

This case does **not** claim that Dimond's telephone translator and IBM's TROS are component-for-component identical, nor that the Bell patent alone proves the complete genealogy of every transformer ROM.

Likewise, the Computer History Museum's timeline statement that IBM introduced TROS with System/360 is useful product-history wording, but it must not be expanded into an invention-priority claim for transformer read-only storage.[^chm]

---

## Cross-case comparison

### Case 02 — classic writable magnetic core

Case 02:

```text
remanent magnetization carries payload
read may destroy that state
rewrite restores it
```

Case 62:

```text
control-tape conductor routing carries fixed microinstruction
transformer induction reads the relation
ordinary machine execution has no write-back path
```

Therefore:

> **magnetic core / transformer presence ≠ remanent-state memory.**

### Case 60 — Apollo core rope

The functional similarity is genuine but bounded:

- both preserve a program through a manufactured conductor/core coupling relation;
- both use magnetic/transformer behavior for sensing rather than treating every stored bit as a stable core polarity;
- neither supplies ordinary runtime electronic rewrite of the fixed program.

The difference is equally important:

- AGC rope organizes many sense lines through each selected core and moves program revision through rope-module production;
- Model 40 TROS uses printed control tapes/word lines and explicitly permits physical tape replacement as the way to change TROS information.

Thus:

> **shared topology-coupled readout ≠ same carrier or same revision regime.**

### Cases 11–13 — EPROM / EEPROM / Flash

All can be called `nonvolatile` or `read-mostly` in broad modern language, but their update authority differs:

- EPROM: radiation erase + electrical programming;
- EEPROM: electrical erase/program;
- early Flash: coarse electrical erase + finer program/read;
- TROS: physical carrier replacement, not an in-system electrical rewrite.

The useful comparison is about **where update authority resides**, not about treating all ROM/nonvolatile media as one lineage.

### Case 55 — retained health telemetry

TROS demonstrates a fixed executable control program; NVMe SMART/Health demonstrates cumulative device-history/control information. Both are retained technical state, but `fixed microprogram` and `retained lifetime telemetry` have different purposes, update mechanisms, and temporal semantics.

---

## Claim classification

### Historical record (`H/P`)

Supported:

- IBM Model 40 used TROS as read-only control storage;
- the bounded TROS control word is 56 bits / 18 fields in the field-engineering manual;
- TROS information is fixed/predetermined and only read out during ordinary operation;
- drive-line linking versus bypassing a transformer controls the sensed bit;
- TROS output is a microinstruction/control word, and sequences form a microprogram;
- Model 40 TROS control tapes physically encode the word pattern;
- IBM says changing TROS information requires physically changing the control tapes;
- the 1964 engineering account describes 16 modules × 256 words for the standard 4096-word store and 128 two-word tapes per module;
- Bell inductive translator prior art predates System/360.

### Engineering reconstruction (`E`)

Supported inferences:

- the retained payload is better described as conductor-routing / coupling geometry than as per-bit ferrite remanence;
- ordinary read transduction changes electrical/magnetic conditions without changing the encoded tape route;
- quiescent physical retention can coexist with substantial configuration/service labor;
- field replacement can change logical currentness while old carriers continue to survive physically;
- payload geometry and sensing/recoverability infrastructure are distinct retained conditions.

### Functional analogy (`A`)

Permitted with explicit limits:

- Apollo core rope: topology-coupled fixed-program sensing, but different organization and revision workflow;
- mask ROM / later firmware ROM: runtime read-only control-store role only, not physical identity or direct genealogy;
- immutable software image: currentness-by-replacement analogy only.

### Philosophical interpretation (`I`)

A bounded interpretation is permitted:

- `read-only` is a relation between an artifact and a particular operational authority, not a metaphysical property of never being changeable;
- a retained state can be stable precisely because its update path has been displaced into a slower service/fabrication layer.

Rejected overreach:

- TROS is literally Stieglerian tertiary retention merely because it stores microcode;
- runtime read-only implies absolute immutability;
- transformer use makes TROS the same technical object as core rope or classic core RAM;
- System/360 invented transformer read-only storage.

---

## Retention summary

| Dimension | Model 40 TROS |
| --- | --- |
| retained state | fixed microinstruction bit pattern |
| substrate | printed control-tape drive-line routing through/bypass transformer positions |
| volatility | state-bearing routing does not depend on operating power; recoverability electronics do |
| maintenance | no periodic bit refresh established; carrier integrity, configuration, diagnostics, and service replacement remain |
| addressability | ROAR/ROSCAR-selected fixed control words |
| read semantics | current-transformer sensing; logically nondestructive with respect to the encoded route |
| write semantics | no ordinary runtime write; change by physical control-tape replacement |
| erase semantics | no ordinary electrical erase; supersession by replacement does not imply old-carrier destruction |
| failure | carrier/route damage, connection/sense-path failure, mis-encoding, wrong configuration |
| identity | microprogram identity can persist across repeated reads; a revised current program can move to replacement tapes |
| labor | control-tape preparation/manufacture, installation, configuration control, maintenance, diagnostics |
| prior-art boundary | Dimond/Bell inductive translation predates System/360; IBM case is a bounded later implementation |

---

## What this case establishes

> **IBM System/360 Model 40 TROS is a grounded counterexample to both `magnetic component = magnetic-state payload` and `read-only = immutable`. Its microinstructions are retained in fixed conductor/transformer coupling geometry, ordinary operation reads rather than rewrites that geometry, and IBM explicitly places program change in a physical control-tape replacement path.**

The strongest cross-case consequence is:

> **update authority can be displaced from runtime commands into replaceable material configuration without making the retained state either purely hardwired logic or absolutely unchangeable.**

---

## Evidence limits and next work

- The Bitsavers copy of the IBM March 1970 field-engineering manual was text-indexed successfully in this run, but direct PDF rendering returned HTTP 403; claims here therefore use the indexed primary text and do not depend on uninspected diagram geometry.
- A dedicated archive-quality inspection of the Taub/Kington pp. 443–459 facsimile would improve exact figure/signal-margin anchoring but is not needed for the bounded retention claim.
- A full Bell/IBM transformer-ROM genealogy, IBM Hursley SCAMP development, and TROS manufacturing economics belong primarily in `computing-archaeology` if pursued.
- Model 30 CCROS and Model 50 BCROS should remain separate cases if their distinct carrier/revision semantics become analytically useful.
- No named-field-failure statistics or independent fault-injection evidence is claimed here.

---

## Sources

[^ibm-fe]: IBM, *System/360 Model 40 Functional Units: Field Engineering Manual of Instruction*, Fifth Edition, March 1970, order SY22-2843-1, especially the `Transformer Read Only Storage (TROS)` section around printed p. 52. Archived scan: <https://bitsavers.org/pdf/ibm/360/fe/2040/SY22-2843-1_Model_40_Functional_Units_Mar70.pdf>.

[^fagg]: P. Fagg, J. L. Brown, J. A. Hipp, D. T. Doody, J. W. Fairclough, and J. Greene, `IBM System/360 Engineering`, *Proceedings of the 1964 Fall Joint Computer Conference*, pp. 205–231; TROS discussion around pp. 216–219. Bibliographic record: <https://researchr.org/publication/FaggBHDFG64>. Text mirror of the Computer History Museum collection scan: <https://paperzz.com/doc/9212284/ibm-system-360-engineering>.

[^taub]: Daniel M. Taub and Brian W. Kington, `The Design of Transformer (Dimond Ring) Read-Only Stores`, *IBM Journal of Research and Development* 8(4), 1964, pp. 443–459, DOI 10.1147/rd.84.0443. Bibliographic record: <https://dblp.org/rec/journals/ibmrd/TaubK64>.

[^dimond]: Thomas L. Dimond, `Electronic Induction Number Group Translator`, U.S. Patent 2,614,176, filed 1950-05-06, issued 1952-10-14: <https://patents.google.com/patent/US2614176A/en>.

[^bell-history]: A. E. Joel et al., *A History of Engineering and Science in the Bell System: Switching Technology (1925–1975)*, bibliography for No. 5 Crossbar, citing T. L. Dimond, `No. 5 Crossbar AMA Translator`, *Bell Laboratories Record* 29 (February 1951), pp. 62–68. Archived text/searchable scan: <https://www.telephonecollectors.info/index.php/browse/document-repository/catalogs-manuals/bell-system-we/history-books-1/11365-btl-history-switching-technology-1982-opt-r/file>.

[^chm]: Computer History Museum, `Memory & Storage` timeline, entry `Transformer Read Only Storage (TROS)`: <https://www.computerhistory.org/timeline/memory-storage/>. The CHM wording is used as an artifact/product-introduction witness, not an invention-priority claim.