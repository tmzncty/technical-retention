# Evidence 10 Addendum — Hitachi 1982–1984 Leakage-Comparator Self-Refresh Prior Art

## Purpose

Independently inspect the Hitachi record that Toshiba US4682306A cited as prior art, so Case 10 no longer depends on Toshiba's retrospective description for the earlier leakage-aware self-refresh boundary.

This addendum is deliberately narrow. It establishes a **manufacturer-primary public mechanism floor by 31 March 1984** for a DRAM automatic/self-refresh design whose trigger is derived from leakage-simulation capacitor state. It does not establish the first invention of leakage-aware refresh, a named commercial implementation, or a direct Hitachi-to-Toshiba implementation genealogy.

---

## Source identity and chronology

**Hitachi Ltd., JPS5956291A, _MOS storage device_** (Japanese publication; Google Patents supplies a machine-translated transcription of the period document).

- application / priority: **JP57164829A, 24 September 1982**;
- publication: **JPS5956291A, 31 March 1984**;
- inventors listed in the record: Kiyobumi Uchibori, Norimasa Yasui, Yoshiaki Onishi, Hiroshi Kawamoto;
- assignee: Hitachi Ltd.;
- directly inspected transcription: <https://patents.google.com/patent/JPS5956291A/en>.

Chronology guardrail:

> **24 September 1982 filing/priority ≠ 31 March 1984 public disclosure.**

The earlier date is relevant to the family chronology. The directly inspectable public-document floor used by this repository is the publication date.

---

## Direct historical record

### H/P — the source distinguishes externally requested refresh from a fully automatic objective

The description begins from dynamic-memory charge leakage and the need to read, amplify, and rewrite information before it is lost. It then discusses an earlier `automatic refresh` arrangement driven through an external refresh-control terminal and says that requiring the external control signal means that arrangement cannot be regarded as fully automatic refresh.

The Hitachi invention's stated objective is therefore not merely `DRAM needs refresh`; it is to internalize more of the decision/control path while reducing unnecessary refresh power.

### H/P — fixed conservative self-refresh is treated as an energy problem

The source says actual cell leakage varies, including with temperature, and argues that a fixed refresh period sized with margin for the worst condition performs refresh more frequently than necessary in less demanding conditions. The exact quantitative/process relations in the document remain period- and design-specific rather than universal DRAM laws.

### H/P — automatic refresh includes address, oscillation, and leakage-simulation blocks

The disclosed automatic-refresh circuit contains a refresh-address counter, a leakage-current simulation circuit, and an oscillation circuit. The oscillator produces pulses for address stepping during self-refresh, while the refresh-address counter forms internal refresh addresses.

This independently confirms that the design combines two relations that must not be collapsed:

```text
when maintenance should start
    !=
which row maintenance should address next
```

### H/P — two retained analog control states are compared

The principal embodiment uses two precharged capacitors, C1 and C2, in the leakage-current simulation circuit. Their initial levels, capacitances, and/or leakage are deliberately arranged so that the held voltage of C2 falls faster than that of C1 in relation to the desired memory-cell refresh period.

A voltage-comparison circuit receives the two held voltages. The important historical relation is therefore comparative rather than a single fixed timer value:

```text
held state Va on C1
    compared with
held state Vb on C2
    -> relation reverses as leakage proceeds
```

The patent also discusses alternative ways to obtain the required relation, including equal capacitance with different leakage and structures whose capacitor/leakage characteristics can be engineered to track the memory-cell problem.

### H/P — comparison reversal activates self-refresh work

When the C1/C2 voltage relation reverses, the comparator-derived self-refresh control signal changes state. That state admits oscillator pulses to the refresh counter, selects the counter's internally formed address path, and marks self-refresh as in progress. The described interface blocks outside writes/reads during this interval.

The counter then supplies refresh addresses so that the full memory-cell set is refreshed. Counter overflow precharges C1/C2 again and ends the self-refresh pass, beginning another monitoring interval.

A bounded state-machine reconstruction is:

```text
C1/C2 precharged
    -> leakage changes their held voltages at intentionally different rates
    -> comparator relation reverses
    -> self-refresh control state asserted
    -> oscillator pulses reach refresh-address counter
    -> internal refresh addresses traverse the array
    -> counter overflow
    -> C1/C2 re-precharged
    -> monitoring interval restarts
```

### H/P — the claims preserve the same relation

Claim 1 names first and second precharged capacitors, a voltage-comparison circuit receiving their held voltages, and an automatic-refresh control circuit activated by the comparator's inverted output to self-refresh dynamic memory cells according to an internally generated address signal. Claim 4 separately allows the automatic-refresh circuit also to be activated by an external control signal.

This claim structure keeps **autonomous condition-derived triggering** separate from the continued possibility of an externally requested refresh path.

---

## Prior-art effect on Case 10

Before this direct inspection, Case 10 knew JPS5956291A only through Toshiba US4682306A's explicit prior-art discussion. That was enough to block a Toshiba priority claim, but not enough to ground Hitachi's circuit details independently.

Direct inspection changes the evidence status:

```text
before:
Toshiba says earlier Hitachi work used two leakage-monitor capacitors + comparator

now:
Hitachi's own 1984 public document directly shows
    two precharged leakage-simulation capacitors
    + voltage comparison
    + comparator-derived self-refresh control
    + internal oscillator/counter/address path
    + full-pass completion/re-precharge cycle
```

The defensible novelty boundary for Toshiba therefore becomes narrower. Toshiba US4682306A remains a strong later mechanism witness for its own preferred **single monitor-capacitor + threshold/inverter + intermittent refresh-pass** design, but it is not the repository's earliest directly inspected leakage-derived self-refresh mechanism.

---

## Engineering reconstruction

### E — payload retention state ≠ maintenance-proxy state

The user payload is the dynamic-cell information being preserved. C1/C2 hold different state: intentionally decaying analog control evidence used to decide when preservation work should begin.

The project may call these `proxy` or `sentinel` states, but those are reconstruction terms, not Hitachi's recovered vocabulary. The source itself uses leakage-current simulation / comparison language.

### E — trigger authority ≠ enumeration authority ≠ completion evidence

The comparator decides when the condition is met; the oscillator provides pulses; the counter enumerates refresh addresses; overflow marks the end of the pass and reinitializes the monitoring state. Correctness of one relation does not automatically prove correctness of the others.

### E — a preservation mechanism can retain a deliberately unstable control relation

The leakage-simulation capacitors are useful precisely because their stored voltages change. Their controlled decay is not a failure of the retention system; it is the measurement process that schedules work on the payload.

### E — self-refresh availability ≠ ordinary read/write availability

The source's self-refresh-in-progress handling blocks normal external read/write service during the pass. Preserving state can therefore temporarily reduce foreground availability without implying payload loss.

---

## Functional comparison with Toshiba — not genealogy

| Relation | Hitachi JPS5956291A | Toshiba US4682306A |
| --- | --- | --- |
| Public document | 31 Mar 1984 | 21 Jul 1987 (Japanese priority 20 Aug 1984) |
| Condition state | two precharged leakage-simulation capacitors | preferred monitor capacitor |
| Detection | voltage relation/comparator | monitor threshold/inverter/control path |
| Active refresh work | oscillator + refresh-address counter + internally selected addresses | oscillator + refresh-address counter + row decoder |
| Completion/reset | counter overflow re-precharges monitor capacitors | pass completion resets/recharges monitor state |

This is a **functional/mechanism comparison**, not proof that Toshiba copied Hitachi, that the circuits are transistor-for-transistor descendants, or that one patent family exhausts the historical genealogy.

---

## Anti-anachronism and evidence limits

- `adaptive refresh`, `closed-loop refresh`, `proxy`, and `sentinel` remain modern analytical vocabulary unless a period source uses them.
- `self-refresh` / `automatic refresh` are used here only where supported by the period documents; their exact distinction is source-specific and must not be projected into later JEDEC command semantics.
- one directly inspected 1984 publication does **not** establish first invention or complete prior art;
- patent disclosure does **not** establish a named shipping DRAM or pseudo-SRAM implementation;
- a shared objective and similar block roles do **not** prove direct Hitachi→Toshiba genealogy;
- machine translation is adequate here for mechanism discovery/cross-checking against circuit labels and claims, but a later priority dispute or wording-sensitive historiographic claim should consult the Japanese facsimile or a specialist translation.

---

## Related-repository boundary

Fresh searches of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `JPS5956291A` and `self-refresh` found no dedicated treatment to reuse.

`technical-retention` therefore keeps this narrow correction because it changes the retention-specific novelty boundary. A broader history of Hitachi/Toshiba DRAM families, pseudo-SRAM, leakage monitors, oscillator design, process scaling, standards, and commercial deployment belongs primarily in `computing-archaeology` if developed.

---

## Grounding decision

**Status: direct primary prior-art deepening accepted.**

The source independently grounds a public 1984 leakage-comparator self-refresh mechanism and converts what had been an indirect Toshiba citation into direct manufacturer-primary evidence. It narrows Toshiba's novelty boundary without creating a new invention-priority claim.
