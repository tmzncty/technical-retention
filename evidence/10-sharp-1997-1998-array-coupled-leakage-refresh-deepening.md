# Evidence 10 Addendum — Sharp 1997–1998 Array-Coupled Leakage Self-Refresh

## Status

**`bounded deepening complete`** — cross-vendor mechanism evidence for a later DRAM / pseudo-SRAM self-refresh design that derives refresh timing from leakage coupled to existing array infrastructure rather than from a standalone leakage-simulation element alone.

This addendum does **not** identify a named shipping Sharp memory product with the exact circuit, does not establish first invention, and does not turn a patent embodiment into a universal model of adaptive refresh.

---

## Purpose

Case 10 already has two manufacturer-primary mechanism witnesses:

- Hitachi JPS5956291A, publicly disclosed in 1984, uses two precharged leakage-simulation capacitors and a comparator to decide when an automatic refresh pass begins;
- Toshiba US4682306A, Japanese priority 1984 and US publication in 1987, uses a preferred monitor-capacitor / threshold path and explicitly permits a conservative monitor element that reaches the maintenance boundary before ordinary payload cells.

Those records establish that refresh timing can be derived from a deliberately decaying proxy state. They do **not** imply that later leakage-tracked refresh had to use the same proxy geometry.

Sharp's later patent family provides a useful negative control. It describes self-refresh timing coupled to leakage occurring through existing bit-line / substrate structures, and also gives an alternative embodiment that derives refresh timing from the operating cycle of a substrate back-bias generator.

The narrow research question is therefore:

> **Does leakage-derived refresh imply one stable sensor topology, or can the same preservation objective be implemented by materially different physical proxies and aggregation boundaries?**

The Sharp record supports the latter.

---

## Source identity and chronology

Primary family used here:

**Makoto Ihara / Sharp Corp., US6075739A, _Semiconductor storage device performing self-refresh operation in an optimal cycle_.**

- earliest family priority shown in the record: **17 February 1997**;
- Japanese application: **29 October 1997**;
- Japanese laid-open publication JPH10289573A: **27 October 1998**;
- US filing: **12 February 1998**;
- US publication / grant: **13 June 2000**;
- original assignee: **Sharp Corp.**;
- inventor: **Makoto Ihara**;
- directly inspected English family text: <https://patents.google.com/patent/US6075739A/en>;
- Japanese family publication: <https://patents.google.com/patent/JPH10289573A/en>.

Chronology guardrail:

```text
17 Feb 1997 priority
    !=
27 Oct 1998 Japanese public disclosure
    !=
13 Jun 2000 US publication
```

For a public-document floor, this repository uses the 1998 Japanese laid-open publication rather than silently treating the priority date as public disclosure.

---

## Direct historical record

### H/P — Sharp explicitly contrasts fixed worst-case timers with leakage-dependent timing

The description says that DRAMs and pseudo-SRAMs with built-in refresh timers conventionally set self-refresh to a fixed interval based on memory-cell leakage evaluated beforehand. It characterizes that interval as being chosen for worst-case temperature dependence and process variation, which can make refresh more frequent than actually required under less severe conditions.

The source then links refresh current to refresh frequency and argues that a refresh interval following actual leakage can reduce self-refresh current, particularly at lower temperature.

This is period design vocabulary about `refresh cycle`, `leak current`, and `self-refresh`; the project need not rename it `adaptive refresh` to establish the engineering relation.

### H/P — the first embodiment couples the timer to bit-line-precharge leakage

The first embodiment contains:

- a one-transistor / one-capacitor dynamic memory-cell array;
- bit-line pairs and bit-line precharge circuits;
- a bit-line precharge potential line;
- a bit-line precharge potential generator;
- a refresh timer circuit;
- a capacitor in the timer path;
- an oscillator and binary counter stages that produce a refresh clock.

The key relation is that the refresh-timer capacitor is connected to the pull-up path that maintains the bit-line precharge potential. Charge drawn from the timer capacitor therefore follows the current required to compensate leakage on the bit-line-precharge network.

The patent says the bit lines are connected through many diffusion contacts / PN junctions whose leakage has a temperature characteristic similar to memory-cell leakage. It therefore treats leakage observed through the existing bit-line-precharge network as an indirect measurement of the array's leakage condition.

A bounded reconstruction of the first embodiment is:

```text
many array-connected junction leakage sources
    -> demand on bit-line-precharge potential generator
    -> discharge of timer / leak-monitoring capacitor
    -> oscillator rate follows discharge rate
    -> counter divides oscillator activity
    -> refresh clock generation
    -> row refresh work
```

This is not a claim that payload-cell charge itself is read out to schedule refresh. The historical mechanism is indirect.

### H/P — the source explicitly values aggregation across many leakage sources

Sharp states that leakage variation can be large when only a small number of PN junctions are used as leakage sources. Its design instead monitors leakage appearing on a bit-line-precharge potential line connected to a very large number of junctions and argues that the resulting current is sufficiently averaged to reduce the influence of individual variation.

That gives a retention-relevant distinction not explicit in the earlier Case-10 witnesses:

```text
proxy similarity
    !=
proxy population / aggregation boundary
```

A sensor can be physically related to the payload problem yet still differ in whether it represents one deliberately designed sentinel element or an aggregate signature from many array-connected structures.

### H/P — refresh timing remains a derived clock, not a direct analog maintenance action

The patent does not make analog leakage itself refresh a row. In the first embodiment, the leakage-related capacitor discharge affects oscillator behavior; binary counters then count oscillations and emit the refresh clock after a specified count.

Therefore:

```text
physical leakage condition
    !=
refresh-clock event
    !=
row selection / restoration
```

The condition is transformed through control circuitry before maintenance work occurs.

### H/P — the same patent family gives a different leakage proxy topology

A later embodiment uses substrate back-bias behavior rather than the bit-line-precharge leakage path as the tracked condition. A substrate-potential detector and charge-pump path restore substrate potential when it leaves a specified range. The refresh timer derives its output from the cycle of substrate-potential change / charge-pump activity, with an oscillator and counter producing refresh clocks.

The description says that greater substrate leakage leads to more frequent refresh-clock output and presents the substrate leakage source as chip-wide enough to provide an averaged condition.

This is especially useful as a negative control because it appears within the **same** patent family:

> **same self-refresh objective != one unique leakage-sensing embodiment.**

The project should therefore avoid speaking of `the` Sharp leakage sensor as though the family disclosed only one topology.

---

## Cross-vendor mechanism comparison — not genealogy

| Record | Public-document floor used here | Condition / proxy state | Detection / transformation | Aggregation boundary exposed by source |
| --- | --- | --- | --- | --- |
| Hitachi JPS5956291A | 31 Mar 1984 | two precharged leakage-simulation capacitors | differential voltage comparison | deliberately constructed local simulation elements |
| Toshiba US4682306A preferred embodiment | 21 Jul 1987 US publication; Japanese priority 20 Aug 1984 | monitor capacitor, optionally biased toward greater leakage than ordinary cells | threshold / inverter starts intermittent refresh sequence | deliberately constructed conservative monitor element |
| Sharp JPH10289573A / US6075739A first embodiment | 27 Oct 1998 Japanese publication | timer capacitor discharged according to current needed to compensate bit-line-precharge-network leakage | oscillator rate + binary count -> refresh clock | many array-connected diffusion / PN-junction leakage sources |
| Sharp alternative substrate embodiment | same family | substrate-potential / back-bias restoration cycle | detector + charge pump + oscillator / counter -> refresh clock | chip/substrate-level leakage behavior |

The defensible comparison is functional and architectural:

```text
same broad preservation objective
    !=
same monitored physical state
    !=
same aggregation boundary
    !=
same threshold / comparison logic
    !=
same refresh-clock generation path
```

Nothing in this table proves direct Hitachi -> Toshiba -> Sharp design descent.

---

## Prior-art boundary

US6075739A's patent record lists several earlier Toshiba leakage / refresh documents, including the Japanese family corresponding to the Case-10 Toshiba automatic-refresh work. That is evidence that the later Sharp patent record sits in a documented field of earlier leakage-aware refresh inventions.

It is **not** enough, by itself, to claim:

- that Makoto Ihara personally read or copied a particular Toshiba document before designing the circuit;
- that an examiner citation proves implementation lineage;
- that Sharp's aggregate bit-line or substrate proxy is descended transistor-for-transistor from Toshiba's monitor-capacitor embodiment;
- that the patent citation list is a complete map of relevant prior art.

The safe historical statement is narrower:

> by the late 1990s, a Sharp patent family publicly disclosed materially different ways to couple self-refresh timing to leakage, while its patent record also sat among earlier manufacturer disclosures of leakage-aware refresh.

---

## Engineering reconstruction

### E — preservation may depend on a proxy that is neither payload nor a replica of one payload cell

In the Sharp first embodiment, the relevant maintenance signal is derived from current associated with maintaining the bit-line-precharge network and its many leakage sources. That makes the proxy more infrastructural than a single-cell surrogate.

A useful decomposition is:

```text
payload charge state
    !=
array-associated leakage signature
    !=
timer-capacitor state
    !=
oscillator / counter state
    !=
refresh-clock state
```

All of these may participate in preservation, but they are not interchangeable forms of retained state.

### E — averaging can improve representativeness while hiding local extremes

Sharp explicitly motivates the many-junction measurement as reducing variation by aggregation. From a systems perspective, averaging and worst-case protection are different objectives.

The source supports the first relation:

```text
many leakage sources -> less sensitivity to one source's variation
```

It does **not** establish the second:

```text
averaged leakage -> guaranteed coverage of the worst-retention cell
```

That latter implication would require product characterization or validation evidence that this patent does not provide.

### E — sensor fidelity has multiple dimensions

The Hitachi/Toshiba/Sharp comparison suggests at least three independent design questions:

1. **physical similarity** — does the monitored state have leakage physics similar to the protected cells?
2. **conservatism** — is the monitor intentionally arranged to cross its maintenance boundary before payload loss?
3. **population coverage** — does the monitor represent one designed proxy, a sample, or an aggregate over many physical structures?

These are project-level analytical categories, not historical vendor terminology.

### E — a maintenance trigger can be derived through another maintenance subsystem

The substrate-back-bias embodiment is conceptually distinct from a dedicated leak-sensor path. A subsystem already tasked with keeping substrate potential in range can expose its own operating rhythm, and that rhythm can then inform refresh timing.

This supports a broader retention pattern:

> **one maintenance loop can become evidence for scheduling another maintenance loop.**

The statement is an engineering reconstruction of the disclosed coupling, not a claim that Sharp used that phrase.

---

## Functional analogy — bounded only

The Sharp design can be compared functionally with later temperature-compensated self-refresh, retention-aware refresh, SSD wear telemetry, or other condition-derived maintenance systems because all transform some observed state into maintenance timing or intensity.

But the comparison stops at function:

```text
condition-derived maintenance
    !=
shared sensor physics
    !=
shared control algorithm
    !=
shared implementation lineage
```

Case 55's SSD spare telemetry, for example, is digitally reported controller state around finite reserve consumption; it is not evidence for a historical or implementation connection to analog DRAM leakage monitors.

---

## Philosophical interpretation

A narrow interpretation follows from the engineering record: preservation need not rely on observing the payload directly. A system can preserve one state by retaining and interpreting another state whose evolution is expected to remain meaningfully related to the payload's risk.

The Sharp evidence adds a qualification to the earlier Case-10 formulation:

> the useful maintenance proxy need not be a miniature copy of the threatened state; it may instead be an aggregate signature emitted by the infrastructure surrounding that state.

That is a present-day interpretation. Sharp's patent makes engineering claims about leakage, averaging, refresh timing, and power; it does not present a philosophy of representation or memory.

---

## Explicit non-claims

This addendum does **not** claim that:

- 17 February 1997 is the public-disclosure date;
- Sharp invented leakage-aware, adaptive, variable, or temperature-aware refresh;
- US6075739A is earlier than the Hitachi or Toshiba Case-10 records;
- a named Sharp DRAM or pseudo-SRAM shipped with either disclosed embodiment;
- the patent's first embodiment directly measures charge remaining in payload cells;
- bit-line-precharge leakage and memory-cell storage-node leakage are physically identical;
- averaging many PN-junction leakage sources proves coverage of the worst-retention cell;
- one oscillator/counter implementation is universal across the patent family or across Sharp memories;
- the substrate-back-bias embodiment and bit-line-precharge embodiment are the same circuit;
- the patent's statements about temperature scaling are universal quantitative laws for all DRAM processes;
- a patent citation to Toshiba proves inventor-to-inventor transmission or copying;
- `self-refresh` in this late-1990s patent can be silently equated with every later JEDEC self-refresh mode semantic;
- condition-derived refresh makes dynamic memory nonvolatile;
- reduced refresh frequency eliminates the refresh obligation;
- aggregate sensing is intrinsically safer than a conservative local sentinel.

---

## Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Sharp publicly disclosed this patent family by the Japanese laid-open publication of 27 Oct 1998 | H/P | JPH10289573A / US6075739A family chronology |
| The family criticizes fixed worst-case self-refresh intervals as potentially over-refreshing under easier conditions | H/P | US6075739A description |
| The first embodiment couples a refresh-timer capacitor to leakage demand on the bit-line-precharge network | H/P | US6075739A first embodiment and claims |
| The source treats many array-connected PN-junction leakage sources as an averaging mechanism | H/P | US6075739A description |
| Oscillator behavior and binary counting transform the leakage-related state into a refresh clock | H/P | US6075739A first embodiment |
| The family also discloses a substrate/back-bias-cycle-derived refresh-timing embodiment | H/P | US6075739A later embodiment / claims |
| Sharp's two disclosed proxy topologies are one identical physical mechanism | X | source presents distinct embodiments |
| Aggregate leakage proves protection of the worst-retention payload cell | X | no such validation is supplied |
| A named commercial Sharp part used either exact embodiment | X | not established here |
| The 1997 priority date is public disclosure | X | public-document floor is the 1998 Japanese publication |
| A patent citation to Toshiba proves direct design genealogy | X | citation relation is insufficient |
| Leakage-derived self-refresh can use materially different proxy and aggregation topologies | E | bounded cross-vendor reconstruction from Hitachi, Toshiba, and Sharp records |
| A maintenance subsystem's activity can become evidence for scheduling another maintenance subsystem | E | bounded reconstruction from the substrate/back-bias embodiment |

---

## Related-repository boundary

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `US6075739`, `self refresh leakage`, and related terms found no dedicated Sharp / DRAM leakage-monitor history to reuse.

This repository therefore keeps the narrow cross-vendor mechanism comparison because it changes the retention-specific model of what counts as a maintenance proxy. A broader history of DRAM process leakage, back-bias generators, pseudo-SRAM product families, manufacturer competition, and standards belongs in `computing-archaeology` if developed later.

---

## Remaining evidence debt

The following questions remain open:

- a named Sharp shipping DRAM or pseudo-SRAM tied by manufacturer documentation to one of these exact embodiments;
- die-level or circuit-level validation showing the disclosed coupling in commercial silicon;
- characterization data for how well the aggregate bit-line / substrate leakage proxies bound worst-cell retention across process and temperature;
- a complete 1980s–2000s genealogy of variable-refresh patents and publications, including applicant-vs-examiner citation provenance;
- direct historical evidence of inventor-to-inventor influence rather than functional similarity;
- comparison with later standardized temperature-compensated self-refresh using normative JEDEC/vendor documents;
- independent fault-injection or measurement work that separates proxy failure, oscillator/counter failure, row-enumeration failure, and payload-restoration failure.

These are deliberately left open rather than inferred from the patent.

---

## Grounding decision

**Status: bounded cross-vendor mechanism deepening accepted.**

Sharp's 1998 public patent-family record shows that leakage-derived self-refresh did not converge on one unique `sentinel capacitor` architecture. The disclosed alternatives couple refresh timing to aggregate bit-line-precharge leakage or to substrate/back-bias behavior, with oscillation and counting converting those conditions into refresh clocks.

The strongest retention conclusion is therefore:

```text
preservation objective shared
    !=
proxy topology shared
    !=
aggregation boundary shared
    !=
control path shared
```

That conclusion deepens Case 10 without turning a patent embodiment into a shipping-product claim or a functional comparison into genealogy.

## Sources

1. Makoto Ihara / Sharp Corp., US6075739A, _Semiconductor storage device performing self-refresh operation in an optimal cycle_: <https://patents.google.com/patent/US6075739A/en>.
2. Sharp Corp., JPH10289573A, Japanese family publication, published 27 October 1998: <https://patents.google.com/patent/JPH10289573A/en>.
3. Hitachi Ltd., JPS5956291A, _MOS storage device_, published 31 March 1984: <https://patents.google.com/patent/JPS5956291A/en>.
4. Takayasu Sakurai and Tetsuya Iizuka / Toshiba Corp., US4682306A, _Self-refresh control circuit for dynamic semiconductor memory device_: <https://patents.google.com/patent/US4682306A/en>.