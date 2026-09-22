# Case 03 — DRAM refresh evidence index

Case: [`../cases/03-dram-refresh-as-scheduled-restoration.md`](../cases/03-dram-refresh-as-scheduled-restoration.md)

Current local maturity: **grounded**.

This index is a navigation aid for the retention-specific evidence chains. It is not a substitute for `CASE_INDEX.md` and does not independently promote case maturity.

---

## Evidence chains

### 1. Cell-level leakage, restoration, and periodic regeneration

- [`03-dram-1967-1982-grounding.md`](03-dram-1967-1982-grounding.md)

Grounds the central Case 03 distinction:

```text
access-triggered restoration
    !=
time-triggered periodic regeneration
```

Primary anchors include Dennard's 1967-filed / 1968-issued patent and bounded commercial DRAM documentation.

---

### 2. External refresh control as retained maintenance state

- [`03-intel-1975-1983-refresh-control-failure-boundary-deepening.md`](03-intel-1975-1983-refresh-control-failure-boundary-deepening.md)

Adds Intel's dedicated refresh-controller lineage and makes control-state failure explicit:

```text
payload still momentarily recoverable
    !=
refresh coverage state correct
```

It also preserves the opposite failure mode in which badly coupled maintenance can damage useful-service liveness.

---

### 3. Hidden refresh versus explicit controller timing/coverage state

- [`03-intel-1982-1984-hidden-refresh-controller-state-deepening.md`](03-intel-1982-1984-hidden-refresh-controller-state-deepening.md)

Separates interface-level hidden refresh from autonomous maintenance:

```text
hidden refresh
    !=
autonomous cadence
```

and distinguishes payload state from timer, counter, and arbitration state.

---

### 4. On-chip refresh-address coverage versus autonomous self-refresh cadence

- [`03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md`](03-1984-1988-cbr-onchip-refresh-counter-boundary-deepening.md)

Uses TI CAS-before-RAS documentation and NEC patent evidence to fix:

```text
on-chip refresh-address generation
    !=
on-chip refresh-cadence generation
```

This is a control-location boundary, not a claim of one universal implementation genealogy.

---

### 5. Named-product self-refresh mode handoff and coverage obligations

- [`03-hitachi-1996-1997-self-refresh-mode-handoff-deepening.md`](03-hitachi-1996-1997-self-refresh-mode-handoff-deepening.md)

Hitachi HM5118165L documentation adds the transition layer:

```text
ordinary refresh regime
    -> qualified self-refresh entry
    -> autonomous retention interval
    -> qualified exit
    -> ordinary refresh regime
```

The datasheet requires bounded refresh work around entry/exit and forbids repeated self-refresh episodes without re-establishing whole-array coverage. It therefore fixes:

```text
self-refresh support
    !=
arbitrary mode-switch safety

mode state
    !=
coverage-completion evidence

payload retention
    !=
foreground read availability
```

---

## Cross-chain model

The five evidence chains now support a more explicit Case 03 decomposition:

```text
payload charge state
    ↓
sense / restore correctness
    ↓
refresh cadence
    ↓
refresh-address coverage
    ↓
maintenance admission / arbitration
    ↓
refresh regime / mode
    ↓
mode-transition handoff obligations
    ↓
foreground service availability
```

These relations are coupled but not interchangeable.

A correct statement about one layer must not be silently promoted into a claim about the others.

---

## Historical-record boundaries

The case currently has historical evidence for:

- leakage and periodic regeneration in Dennard's patent;
- commercial dynamic memory requiring periodic refresh;
- dedicated external refresh-control components;
- timer/counter/arbitration state in external controllers;
- hidden refresh as an interface behavior;
- on-chip CBR refresh-address generation;
- patent-level timer-backed self-refresh architecture;
- named-product self-refresh with explicit entry/exit coverage rules.

The case does **not** yet establish:

- first invention of DRAM self-refresh;
- first commercial self-refresh DRAM;
- first JEDEC standardization of self-refresh;
- one continuous genealogy from early controller designs to later on-chip self-refresh;
- a universal internal architecture for self-refresh;
- a host-visible completion proof for every refresh-coverage obligation.

---

## Engineering reconstruction boundaries

Supported reconstruction:

```text
state being retained
    !=
state required to retain it
    !=
correctness of maintenance-control state
    !=
location of maintenance-control state
    !=
maintenance-regime transition correctness
```

Do not collapse these into a single claim that `DRAM requires refresh`.

The useful retention problem is how deadlines, coverage, control-state placement, admission, and mode handoff cooperate to make a stable logical address appear continuously available.

---

## Related-repository routing

Searches of `tmzncty/computing-archaeology` for `HM5118165` and `self refresh` found no dedicated reusable packet during this slice.

Keep in this repository:

- retention deadlines;
- maintenance-control-state distinctions;
- self-refresh handoff obligations;
- evidence boundaries between payload, mode, coverage, and service availability.

Route primarily to `computing-archaeology`:

- broad DRAM/EDO/SDRAM product genealogy;
- semiconductor process history;
- vendor competition and market chronology;
- exact circuit genealogy of on-chip self-refresh timers/counters;
- shipment/adoption history not needed for the retention argument.

---

## Remaining high-value work

1. Earlier named-product self-refresh witness with directly inspectable primary documentation.
2. Named-product internal timer/counter architecture rather than patent-only architecture.
3. JEDEC self-refresh revision chronology kept separate from vendor product chronology.
4. Controller/board evidence for satisfying entry/exit refresh handoff rules.
5. Fault-injection or hardware validation around missed transition-side coverage obligations.
6. Temperature-conditioned self-refresh behavior only where a source exposes the exact policy/state relation.

Case 03 remains **grounded**. The new Hitachi evidence deepens the maintenance-handoff model but does not justify a maturity promotion by itself.
