# Case 60 Grounding Record — Apollo Core Rope, 1964–1972

## Status

**`grounded`** for the bounded claim that the Apollo Guidance Computer's Block II fixed memory retained program bits primarily in **wired sense-line/core topology**, while ferrite-core switching served the readout mechanism rather than constituting the enduring payload bit in the same way as classic read/write magnetic-core memory.

This record does **not** claim that Apollo invented wired-in fixed memory, read-only magnetic memory, transformer ROM, or the general idea of encoding data in wiring geometry.

---

## Research question

What exactly remains between reads in an AGC core-rope module, and how does that retained state differ from the remanent bit state of classic coincident-current magnetic-core RAM?

The bounded answer supported here is:

```text
classic writable core RAM:
    magnetic remanence is payload state
    ordinary destructive read may erase that state
    rewrite restores it

AGC core rope:
    thread / bypass wiring geometry is payload state
    selected ferrite core switches and resets during access
    read transduces the wiring relation
    ordinary program execution cannot rewrite the fixed topology
```

The case therefore tests a retention regime in which the **state-bearing structure and the state-changing read transducer are not the same thing**.

---

## Source ledger

| Source | Type | Exact use | What it does not prove |
| --- | --- | --- | --- |
| MIT Instrumentation Laboratory / Charles Stark Draper Laboratory, _MIT's Role in Project Apollo, Volume III — Computer Subsystem_, R-700 (1972), especially §2.3.6 and §3.5.2, pp. 46 and 90–92, plus fixed-memory construction discussion around Figs. 3-33/3-34 | P/H, primary institutional final report | identifies AGC fixed memory as nondestructive transformer-type core rope with information wired in; distinguishes erasable and fixed memory; gives the sense-wire thread/bypass encoding; describes set/reset, inhibit selection, selected-core switching/reset, sense-line induction, six-module organization, and tape-guided operator threading | does not establish priority for wired-core ROM; does not imply every rope version had identical organization; does not make wiring labor itself a philosophical category |
| NASA, _Spaceborne Digital Computer Systems — Space Vehicle Design Criteria_, NASA SP-8070 (March 1971), §2.2.2 `Memory` | P/H, contemporary government design-criteria report | defines fixed/read-only memory as manufactured contents requiring physical modification for change; names core-rope program memory; treats retention through power loss/electrical malfunction as a fixed-memory advantage; reports an approximately four-week Apollo production cycle for program changes/new modules | does not establish a universal core-rope manufacturing time; does not show that all fixed memories are physically indestructible; does not specify every Block II electrical detail |
| Ramon L. Alonso, Robert E. Oleksiak, William B. Turner, MIT, U.S. Patent 3,451,129, filed 1966-01-05 | P/H, contemporary patent | uses `wired-in memories`; states that data are stored according to wiring geometry; describes conductor thread/bypass choices for logic values and a tape/program-controlled Jacquard-derived manufacturing workflow | does not by itself prove that every claim in the patent was used unchanged in each flight rope; does not establish MIT as inventor of wired-in memory because the patent itself discusses existing wired-in-memory practice |
| Hayden A. Nelson, U.S. Patent 3,419,855, filed 1964-12-24 | P/H, contemporary patent and prior-art boundary | describes a read-only wired-core fixed-information memory in which storage is provided by the physical configuration of drive windings; explicitly discusses existing linear-select wired-core and `core rope type` arrangements | is not an Apollo implementation document; its different wired-core organization must not be silently substituted for AGC circuit details |
| `tmzncty/computing-archaeology` code/document search for `core rope` | repository-duplication check | no dedicated core-rope case found during this slice, so a retention-specific case here does not duplicate an existing related-repository treatment | absence of a search hit is not proof that no magnetic-memory context exists elsewhere in that repository |

---

## Primary-source anchors

### 1. MIT R-700 — fixed program state and readout

R-700's bounded claims are unusually useful because the report names both the retained-program organization and the read cycle.

The report describes the AGC program memory as a **nondestructive-read core-rope memory of the transformer type with information wired in**. It then explains the bit relation in the fixed-memory organization:

```text
sense line threads selected core  -> logical one
sense line bypasses selected core -> logical zero
```

For the Block II organization described there, six modules each contain 512 cores and 192 sense lines. The selected core is chosen by set/reset and inhibit currents. When it switches, voltage is induced in the sense lines that thread it; later reset returns the core to the starting magnetic condition.

This supports two distinct historical facts:

1. **the program bit is defined by a manufactured wire/core relation**;
2. **the magnetic core intentionally changes state during ordinary readout**.

The engineering conclusion `state-bearing structure ≠ state-changing transducer` follows from their conjunction; it is not historical actor terminology.

R-700 also describes tape-controlled guidance for operators who physically route the sense wires. That grounds the claim that software/program specification was translated into manufacturing instructions whose correctness directly determined the stored bit pattern.

### 2. NASA SP-8070 — fixed-memory lifecycle semantics

NASA SP-8070 provides a system-level boundary that the circuit description alone cannot supply. Its fixed/read-only-memory discussion says that the contents are manufactured into the memory and content change therefore requires **physical modification**. In the Apollo core-rope context it reports a roughly **four-week production cycle** for program changes requiring new modules.

The number is used only as a bounded historical witness for revision latency. It is **not** normalized against later retrospective reports that may include additional software-freeze, spacecraft-integration, checkout, or mission-readiness intervals.

### 3. MIT U.S. 3,451,129 — wiring geometry as memory state

The 1966-filed MIT patent directly uses the general `wired-in memory` category and says data are stored according to **the geometry of the wiring configuration**. Its manufacturing process sorts/routes wires according to logical values and then mounts the harness through magnetic cores.

This strengthens the case's vocabulary without requiring the retrospective phrase `software woven into hardware`.

### 4. Nelson U.S. 3,419,855 — novelty guardrail

Nelson's 1964-filed patent describes a coincident-current **read-only wired-core fixed-information memory** with storage in the physical configuration of drive windings. Its background also discusses earlier wired-core/core-rope arrangements.

Therefore:

> **Apollo core rope ≠ invention of wired-in fixed memory.**

The historically supportable claim is narrower: Apollo used a particular transformer/core-rope organization, documented by MIT and NASA, in which fixed program state and magnetic readout were sharply separated.

---

## Mechanism reconstruction

### Retained payload

```text
physical conductor routing
        +
thread / bypass relation to selected ferrite cores
        =
fixed program bit pattern
```

### Read transduction

```text
address + inhibit network
        ↓
select one core
        ↓
core changes magnetic state
        ↓
threading sense conductors receive induced voltage
        ↓
selected word is classified
        ↓
core reset
```

### Program replacement

```text
new verified program image
        ↓
new routing/manufacturing instructions
        ↓
new or physically modified rope module
        ↓
verification + installation
        ↓
new current fixed program
```

The old module can remain physically readable after supersession. Consequently, **currentness and physical survival are separate relations** even in a nominally read-only medium.

---

## Claim classification

### Historical record (`H/P`)

Supported:

- AGC Block II used separate erasable core and fixed core-rope memories;
- the fixed memory was transformer-type, nondestructive-read, and wired in;
- thread/bypass sense-line geometry encoded fixed bits;
- selected cores switched and reset during read;
- inhibit/set/reset and sense-line circuitry participated in selection/recovery;
- ordinary program steps could not rewrite the rope contents;
- manufacture translated bit specifications into wire routing;
- fixed-memory program change could require a new physical module and, in the NASA 1971 witness, roughly a four-week production cycle;
- wired-in/wired-core read-only memory was already an established technical category by the mid-1960s.

### Engineering reconstruction (`E`)

Supported inferences:

- the durable program state is better described as **wiring topology** than as per-bit remanent core polarity;
- logical nondestructiveness can coexist with repeated physical switching in the read transducer;
- manufacturing correctness becomes part of write correctness when runtime write authority is absent;
- retention work can migrate from runtime maintenance into production, verification, configuration control, and module replacement;
- physical survival of an old module does not make its program image current after replacement.

### Functional analogy (`A`)

Permitted only with guardrails:

- **mask ROM:** both can expose a manufactured, ordinary-runtime read-only bit pattern; physical mechanisms and genealogy are different;
- **classic magnetic-core RAM:** useful mainly as a contrast, because shared ferrite material does not imply shared state-bearing semantics;
- **configuration artifacts / immutable images:** useful for currentness-vs-survival comparison only, not as historical descent.

### Philosophical interpretation (`I`)

Permitted bounded interpretation:

- a technical state can persist in a **relation among components** rather than the instantaneous state of one component;
- material inscription can shift update authority into fabrication and replacement.

Rejected overreach:

- core rope `proves` Stieglerian tertiary retention;
- hand threading alone makes the artifact philosophically privileged;
- read-only means metaphysical immutability;
- ferrite use makes rope memory equivalent to classic magnetic-core RAM.

---

## Prior-art / novelty boundary

### Established no later than the bounded record

- 1964: Nelson files a read-only wired-core memory whose stored information is in physical winding configuration;
- 1966: MIT files a manufacturing patent explicitly describing `wired-in memories` and wiring geometry as stored data;
- 1971: NASA treats core-rope as an established fixed-program space-computer memory and discusses physical-modification/program-change consequences;
- 1972: MIT's final Apollo report gives the detailed AGC fixed-memory organization and manufacturing/readout account used here.

### Explicitly not claimed

- invention of ROM;
- invention of transformer memory;
- invention of wired-in memory;
- invention of magnetic-core memory;
- first use of a core rope;
- first manufactured software artifact;
- direct genealogy to later semiconductor mask ROM.

The contribution of Case 60 is therefore **comparative and retention-specific**, not a priority claim.

---

## Cross-case consequences

### Case 02 — classic magnetic core

Case 02 establishes:

```text
remanent core state carries bit
read may destroy state
rewrite restores logical bit
```

Case 60 establishes:

```text
wire/core geometry carries fixed bit
core switching is access transduction
reset restores transducer condition, not payload
```

Therefore:

> **shared ferrite material ≠ shared retention semantics.**

### Case 11 / 12 / 13 — EPROM / EEPROM / Flash

All can preserve state without ordinary runtime power, but their update authority differs sharply:

- EPROM: exceptional radiation erase;
- EEPROM: electrical erase/write;
- early Flash: coarse electrical erase + finer program/read;
- core rope: fixed program rewrite requires physical artifact modification/manufacture.

Thus `nonvolatile` alone says little about **who can revise state, at what granularity, through what service path, and on what timescale**.

### Case 42 / 56 / 58 — currentness and surviving history

A superseded rope module may remain perfectly readable after a new module becomes authoritative. This is functionally comparable to other cases where physical survival does not determine currentness, but no distributed-consensus or log-authority semantics are imported into Apollo.

---

## Evidence-strength assessment

| Claim family | Strength | Reason |
| --- | --- | --- |
| thread/bypass encoding | **strong** | direct MIT institutional description |
| selected-core switching/reset during read | **strong** | direct MIT circuit/operation description |
| fixed program not electrically rewritten by program steps | **strong** | MIT + NASA institutional evidence |
| manufacture as the update path | **strong** | MIT manufacturing description + NASA fixed-memory lifecycle semantics + MIT patent |
| ~four-week Apollo program-change production cycle | **strong but bounded** | contemporary NASA design-criteria witness; not universalized |
| topology rather than remanent polarity as payload | **strong engineering reconstruction** | follows directly from encoding and access evidence |
| Apollo priority/invention claim | **rejected** | contemporary 1964/1966 wired-memory prior art |
| full pre-Apollo genealogy | **not attempted** | unnecessary for bounded case; future prior-art deepening only |

---

## Grounding decision

Promote directly to **`grounded`** because the central claims no longer depend on a single fragile secondary description:

1. MIT R-700 provides system-specific payload/read/manufacturing evidence;
2. NASA SP-8070 provides contemporary fixed-memory lifecycle and revision-latency evidence;
3. the MIT manufacturing patent provides contemporary wiring-geometry terminology and workflow detail;
4. the Nelson patent independently prevents a false Apollo novelty claim;
5. related-repository duplication was checked;
6. the case explicitly separates historical record, engineering reconstruction, functional analogy, and philosophical interpretation.

Remaining work is targeted genealogy or artifact-specific production archaeology, not a blocker for the bounded retention claim.

---

## Source links

- MIT Instrumentation Laboratory / Charles Stark Draper Laboratory, _MIT's Role in Project Apollo, Volume III — Computer Subsystem_, R-700 (1972): https://www.ibiblio.org/apollo/Documents/R-700.pdf
- NASA, _Spaceborne Digital Computer Systems — Space Vehicle Design Criteria_, NASA SP-8070 (1971), NTRS record: https://ntrs.nasa.gov/citations/19710024203
- NASA SP-8070 historical HTML transcription, §2.2.2: https://klabs.org/history/history_docs/sp-8070/ch2/2p2/2p2p2_memory.htm
- Alonso, Oleksiak, Turner, U.S. Patent 3,451,129: https://patents.google.com/patent/US3451129A/en
- Hayden A. Nelson, U.S. Patent 3,419,855: https://patents.google.com/patent/US3419855
