# Case 01 grounding record — mercury delay-line recirculation, timing, and temperature control (1947–1958)

**Case:** [`cases/01-mercury-delay-line-circulation.md`](../cases/01-mercury-delay-line-circulation.md)  
**Grounding decision:** `grounded`  
**Evidence scope:** exact patent locations for circulation / erasure / retiming / indexing / temperature compensation; direct 1949 *Proceedings of the I.R.E.* page evidence; machine-specific UNIVAC I maintenance evidence for temperature-controlled mercury memory.  
**Historical range of the evidence used here:** 1947–1958.

This record does **not** attempt to write a general history of acoustic delay lines. That work already exists in [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-memory-was-a-tube-of-sound.md). The purpose here is narrower: close the source-location gaps that kept Case 01 at `first-pass`, while preserving the difference between period technical vocabulary and this repository's later retention analysis.

---

## 1. Promotion criteria

The previous Case-01 evidence ledger left three practical blockers:

1. exact patent column / figure anchors for recirculation, retiming, erasure, indexing, and environmental correction;
2. direct inspection of the 1949 IRE paper with page-level anchoring;
3. machine-specific primary evidence that temperature control was not merely a generic museum-summary observation but part of an operational mercury-memory implementation.

This slice closes those blockers strongly enough for `grounded` status. One archival nicety remains: a convenient directly renderable facsimile of every page of the 1949 IRE paper was not available in this run. No Case-01 claim depends solely on an uninspected interior page of that article; exact mechanism claims are carried by the directly inspected patent and the UNIVAC I maintenance manual.

---

## 2. Primary source A — Eckert and Mauchly, US2629827A, filed 1947-10-31

**Source:** J. Presper Eckert Jr. and John W. Mauchly, *Memory system*, US2629827A, filed 31 October 1947, published 24 February 1953.  
Patent HTML: <https://patents.google.com/patent/US2629827A/en>  
Patent PDF: <https://patentimages.storage.googleapis.com/f7/97/cd/c2e4049f574d4d/US2629827.pdf>

The patent facsimile was directly inspected. The following printed-column anchors should be preferred over unlocated paraphrase.

### 2.1 Printed cols. 3–4 — circulation, disturbance, correction, indexing, and control

Printed **col. 3** states that information may remain recirculating, be taken out while still recirculating, be taken out and erased, or be replaced / modified. The same column immediately identifies cumulative-error sources including dimensional inaccuracies, **temperature changes**, and frequency deviation, then describes automatic frequency control together with **reforming and retiming** of pulses so that pulse form and timing do not accumulate error.

The same passage says the timing system provides an **index** into the stored information so that a particular portion of the pulse pattern can be identified and controlled.

Printed **cols. 3–4** also enumerate the figures that bind those claims to concrete apparatus:

- **Fig. 1** — recirculation plus pulse erase, pulse input, external output, pulse forming, and retiming;
- **Fig. 10** — master oscillator and temperature-correction system;
- **Fig. 11** — complete memory system with input/output and erasure controls;
- **Fig. 12** — control of the master oscillator used in Fig. 10;
- **Fig. 13** — identification and individual control of memory spaces in the circulating system;
- **Figs. 14–15** — preferred mercury-tank construction.

This is the strongest direct anchor for the Case-01 historical claims that the system was not merely a passive acoustic path: the period design explicitly included circulation, selective modification / erasure, retiming, indexing, and correction for environmental / timing disturbance.

### 2.2 Printed cols. 5–6 — temperature is part of tank construction

Printed **col. 5** describes insulation around the mercury tank and a **heating coil 78** surrounding it. It says that, although electrical compensation for temperature changes is provided elsewhere, the mercury tank should nevertheless be held as nearly as convenient to a constant temperature; the tank is enclosed and insulated for that reason.

This passage is important because it blocks a weak reading in which `temperature control` is treated as a later explanatory metaphor. The patent's preferred physical construction itself allocates components and enclosure design to thermal stability.

### 2.3 Printed cols. 15–18 — temperature-dependent acoustic delay and closed-loop correction

Printed **col. 15** explicitly notes that acoustic velocity in mercury **decreases as temperature rises** and says the temperature is desirably maintained quite closely constant, with a heating coil under thermostat control.

Printed **cols. 17–18** explain the frequency / temperature correction relation in more operational detail. A temperature change shifts the phase coincidence used by the control system; the oscillator frequency correspondingly changes so that the tank continues to contain the intended number of digit pulses during the transit interval. The patent then discusses an equivalent arrangement in which changing acoustic velocity can instead drive tank-temperature adjustment through a heating coil.

This gives Case 01 an exact period-primary basis for the engineering statement:

> retention correctness depends on keeping **propagation delay, pulse phase, and the machine's timing reference mutually aligned**.

That sentence is an engineering reconstruction, not patent vocabulary. The historical record underneath it is the patent's explicit coupling among mercury acoustic velocity, temperature, oscillator frequency, phase coincidence, and pulse timing.

---

## 3. Primary source B — Auerbach, Eckert, Shaw, Sheppard, *Proceedings of the I.R.E.*, 1949

**Source:** Isaac L. Auerbach, J. Presper Eckert Jr., Robert F. Shaw, and C. Bradford Sheppard, **“Mercury Delay Line Memory Using a Pulse Rate of Several Megacycles,”** *Proceedings of the I.R.E.* **37**(8), August 1949, pp. **855–861**, DOI `10.1109/JRPROC.1949.229683`.

Bibliographic record: <https://ieeexplore.ieee.org/document/1698100/>  
Directly inspected scan containing printed p. 855: <https://capmimo.ece.wisc.edu/capmimo_papers/Path%20Length%20Microwave%20Lenses.pdf>

### 3.1 Printed p. 855 — directly inspected

Printed **p. 855** was directly inspected in facsimile. The paper's summary states that:

- a mercury delay-line memory system for electronic computers had been developed for pulse repetition rates of several megacycles per second;
- the higher repetition rate reduced space and access time;
- pulse-envelope representation and crystal gating supported the higher pulse rate;
- a **multichannel memory using a single pool of mercury** simplified mechanical construction, reduced size, and made **temperature control much easier**.

This page is enough to anchor several points that had previously been cited only through later summaries: the authors themselves present temperature control as a design consequence of the memory's physical organization, and they explicitly connect pulse rate with access-time engineering.

### 3.2 Interior-page retrieval boundary

Search indexing of the full August 1949 issue exposes additional text on printed p. 859 concerning a dedicated temperature-control channel in the multichannel tank, but that archive's full-issue PDF could not be rendered directly in this run. Accordingly:

- the repository may record **p. 855** as directly inspected facsimile evidence;
- the paper's full page range **855–861** and DOI are secure bibliographic facts;
- no detailed mechanism claim in the grounded case is made to depend solely on the unrendered p. 859 text.

The same temperature-control mechanism is independently and much more precisely grounded below in a manufacturer maintenance manual.

---

## 4. Primary source C — *UNIVAC I Maintenance Manual*, January 1958

**Source:** Remington Rand UNIVAC Division of Sperry Rand Corporation, **UNIVAC I Maintenance Manual for Univac I Central Computer Group**, January 1958.  
Archive copy: <https://bitsavers.computerhistory.org/pdf/univac/univac1/UNIVAC1_Maintenance_Manual_Jan58.pdf>  
Archive index: <https://bitsavers.computerhistory.org/pdf/univac/univac1/>

The archive's indexed text was checked at paragraph level. This source is later than the 1947 patent / 1949 paper but is **machine-specific manufacturer maintenance documentation**, not retrospective museum explanation.

### 4.1 §§1-76 to 1-79 — the temperature-control channel is part of the memory system

- **§1-76** describes the UNIVAC I principal internal store as a 1000-word acoustic delay-line memory of 100 ten-word mercury registers and says seven additional channels control the temperature of the seven mercury tanks.
- **§1-77** places the total 126 mercury channels in seven tanks, each divided into 18 channels.
- **§1-78** decomposes a ten-word register into the acoustic delay, an intermediate-frequency chassis with amplifiers / detector / compensating delay, and a recirculation chassis containing a cathode follower, pulse former and retimer, modulator, and gates.
- **§1-79** explains that a temperature-control signal enters the mercury column each word time and is used to adjust current through the heating coil to maintain tank temperature.

This is direct machine-level evidence that the operational memory was not adequately described as `mercury + transducers`; timing, pulse re-formation, electronics, and temperature-control circuitry were constitutive infrastructure.

### 4.2 §§1-88 to 1-90 — transit-time measurement controls heater power

- **§1-88** identifies a 3500-ohm d-c fine temperature-control coil and states that its current is adjusted by the temperature-control channel, which **measures the transit time of a pulse through the mercury**.
- **§1-89** describes comparison of the delayed pulse with a standard timing pulse; the delayed pulse's position determines whether heating should be on or off, and heater power is adjusted to balance tank heat loss.
- **§1-90** identifies **channel 18** as the temperature-control channel; the other relevant chassis participate in information-channel recirculation.

The retention-specific significance is unusually clear:

> the system uses **propagation delay itself as a sensed control variable** in order to maintain the physical environment that keeps future propagation delay usable.

That formulation is this repository's engineering reconstruction. The historical facts are the manual's transit-time measurement, timing comparison, temperature-control channel, and heating-coil actuation.

### 4.3 Machine boundary

UNIVAC I evidence must **not** be silently generalized into EDSAC hardware claims. It establishes that a named production mercury-delay-line computer implemented temperature control as an explicit memory subsystem. It does not prove that EDSAC used the same channel count, heater topology, temperature, timing comparator, or maintenance procedure.

---

## 5. Cross-repository reuse check

`tmzncty/computing-archaeology` already contains a substantial engineering-history treatment:

- [`docs/memory/why-memory-was-a-tube-of-sound.md`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-memory-was-a-tube-of-sound.md)

That article covers radar inheritance, serial access, EDSAC / SEAC context, temperature sensitivity, and the architectural trade in sharing expensive circuitry across many bits. This grounding slice therefore does **not** duplicate that narrative.

`technical-retention` keeps only the comparison-specific result:

- stored-state identity survives repeated regenerated physical tokens;
- retained existence and immediate availability differ because access is phase-dependent;
- environmental control is part of the maintenance relation, not an incidental building-service footnote;
- state retention remains distinct from history retention.

---

## 6. Claim-type boundary

### Historical record

The sources directly support:

- coded pulse information is recirculated through a delay path;
- pulse sequences can be extracted, erased, replaced, or modified;
- pulse reforming / retiming and indexed control are explicit parts of the design;
- temperature changes and oscillator/frequency deviations are explicit disturbance sources;
- the preferred patent apparatus includes heating / insulation and temperature/frequency correction;
- the 1949 paper presents multichannel single-pool mercury construction as easing temperature control;
- UNIVAC I maintenance documentation assigns dedicated channels and heater-control circuitry to keeping mercury transit timing within operating conditions.

### Engineering reconstruction

The repository may infer, while labeling the inference:

- `retention = closed-loop recurrence + correction` is a useful system model;
- the immediate acoustic/electrical token is repeatedly replaced while logical equivalence is maintained;
- **environmental control can be constitutive retention infrastructure** when environmental drift changes the timing relation that defines usable stored positions;
- a sensing channel that measures propagation delay is retained/operational state used to protect other retained state.

These are not period terms.

### Functional analogy

Comparisons to DRAM refresh, destructive core restore, Flash remapping, RAID reconstruction, or distributed repair concern the function `maintain a logical relation across physical change`. They do **not** establish a common historical lineage or identical mechanism.

### Philosophical interpretation

`retention as recurrence`, `persistence as maintained relation`, and the link to technical microtemporality are interpretive claims. The engineering evidence constrains them; it does not turn them into historical actors' vocabulary.

---

## 7. Prior-art / priority controls

This slice does **not** make an invention-priority claim such as `Eckert invented all delay-line memory` or `the 1949 paper invented acoustic storage`. The 1947 patent is used because it provides a precise manufacturer/designer-primary disclosure of the mechanism and its controls. The 1949 paper is used as a period engineering publication by the development team. Priority history belongs in a dedicated technical-history treatment if needed.

Likewise, a later UNIVAC I manual is evidence for the machine it documents, not evidence that every mercury-delay-line computer used the same temperature-control topology.

---

## 8. Grounding decision

**Decision: promote Case 01 from `first-pass` to `grounded`.**

Why promotion is now justified:

1. the 1947-filed primary patent has exact printed-column and figure anchors for circulation, erasure / modification, retiming, indexing, mercury-tank construction, and temperature/frequency correction;
2. printed p. 855 of the 1949 IRE paper has been directly inspected and anchors the development team's own high-rate / access-time / multichannel / temperature-control description;
3. a manufacturer maintenance manual for a named production machine gives paragraph-level machine-specific evidence for recirculation electronics, a dedicated temperature-control channel, transit-time measurement, and heater actuation;
4. the case already links to `computing-archaeology`, so the promotion deepens evidence rather than duplicating the general engineering history.

Remaining work is **archival cleanup or optional extension**, not a grounding blocker:

- obtain a conveniently renderable full facsimile of IRE pp. 856–861 and record additional exact figure/page anchors if a later argument needs them;
- add EDSAC-specific temperature-control primary evidence only if making an EDSAC-specific thermal-control claim;
- decide separately whether `recurrence` deserves a controlled-vocabulary entry distinct from `refresh`;
- deepen the Ernst comparison only in a bounded philosophical test, not inside the historical mechanism record.
