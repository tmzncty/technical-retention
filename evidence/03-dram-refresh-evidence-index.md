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

### 6. Earlier named-product self-refresh primary witness and vendor-specific handoff

- [`03-micron-1993-self-refresh-handoff-primary-witness-deepening.md`](03-micron-1993-self-refresh-handoff-primary-witness-deepening.md)

Micron's *1993 Specialty DRAM Data Book* moves the named-product manufacturer-document floor earlier with the `MT4C8512/3 S`, Rev. 3/93.

The data sheet is explicitly marked `ADVANCE`, so this is **not** promoted into a production/shipment claim.

The source adds three useful distinctions:

```text
external CBR cadence
    + internal refresh counter/controller
    !=
SELF REFRESH internal clocking + row progression
```

```text
self-refresh exit
    !=
maintenance obligation erased
```

and:

```text
same SELF REFRESH capability class
    !=
one universal cross-vendor exit protocol
```

Micron permits immediate post-exit access when the system resumes distributed CBR refresh, while still constraining the next refresh action; another external refresh strategy requires whole-array refresh work before ordinary use. Micron also warns that other manufacturers may require a full post-exit burst regardless of the normal refresh strategy.

This closes the **earlier named-product manufacturer-document witness** debt while leaving an earlier **production-status / shipment** witness open.

---

## Cross-chain model

The six evidence chains now support a more explicit Case 03 decomposition:

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
controller/device compatibility contract
    ↓
foreground service availability
```

These relations are coupled but not interchangeable.

A correct statement about one layer must not be silently promoted into a claim about the others.

The newest Micron witness also makes the authority transfer more explicit:

```text
ordinary CBR:
external cadence authority
    + internal row-address progression

SELF REFRESH:
internal cadence authority
    + internal row-address progression

exit:
external cadence authority must be re-established
    under vendor-specific coverage/deadline rules
```

This is an engineering reconstruction of the documented behavior, not Micron's own taxonomy.

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
- a March-1993 named Micron product document with internal self-refresh clocking, internal refresh counter/controller behavior, and explicit exit-side handoff rules;
- a later 1996–1997 named Hitachi product witness with explicit self-refresh entry/exit coverage obligations.

The case does **not** yet establish:

- first invention of DRAM self-refresh;
- first commercial self-refresh DRAM;
- production shipment of the March-1993 `MT4C8512/3 S` source, because Micron marks it `ADVANCE`;
- first JEDEC standardization of self-refresh;
- that Micron's 1993 `industry standard` wording maps to a particular JEDEC ballot/revision date;
- one continuous genealogy from early controller designs to later on-chip self-refresh;
- a universal internal architecture for self-refresh;
- a universal cross-vendor exit protocol;
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
    !=
controller/device transition-contract compatibility
```

The Micron source adds a useful control-location/authority decomposition:

```text
refresh-address progression can be internal
while cadence remains external
```

and later:

```text
SELF REFRESH can temporarily move cadence authority internal
without making post-exit external maintenance irrelevant
```

Do not collapse these into a single claim that `DRAM requires refresh`.

The useful retention problem is how deadlines, coverage, control-state placement, admission, authority transfer, and mode handoff cooperate to make a stable logical address appear continuously available.

---

## Functional-comparison boundaries

The Micron and Hitachi self-refresh witnesses may be compared functionally because both expose transition-side retention obligations.

But:

```text
similar handoff function
    !=
identical controller-facing protocol
    !=
shared circuit implementation
    !=
direct historical genealogy
```

Micron's own cross-vendor warning is positive evidence that the repository should preserve vendor-specific transition contracts rather than synthesize one timeless `self-refresh exit` rule.

---

## Related-repository routing

Fresh searches of `tmzncty/computing-archaeology` for `MT4C8512` and `self refresh DRAM` found no dedicated reusable packet for this slice. Earlier Case 03 searches for `HM5118165` likewise found no dedicated packet.

Keep in this repository:

- retention deadlines;
- maintenance-control-state distinctions;
- self-refresh handoff obligations;
- cadence-authority transfer;
- evidence boundaries between payload, mode, coverage, and service availability;
- distinction between manufacturer documentation status and production/shipment evidence.

Route primarily to `computing-archaeology`:

- broad DRAM/EDO/SDRAM product genealogy;
- semiconductor process history;
- vendor competition and market chronology;
- exact circuit genealogy of on-chip self-refresh timers/counters;
- shipment/adoption history not needed for the retention argument.

---

## Remaining high-value work

1. **Earlier or contemporary production-status / shipping self-refresh DRAM primary witness.** The March-1993 Micron `MT4C8512/3 S` closes the named-product documentation floor but is marked `ADVANCE`.
2. **Named-product internal timer/oscillator + row-counter architecture.** The Micron source directly establishes internal clocking and refresh counter/controller behavior, but not enough circuit detail to reconstruct the exact oscillator/timer architecture.
3. **JEDEC self-refresh revision chronology**, kept separate from vendor product chronology and from Micron's own `industry standard` wording.
4. **Controller/board evidence** for satisfying entry/exit refresh handoff rules against a named DRAM.
5. **Fault-injection or hardware validation** around malformed entry, interrupted self-refresh, and missed transition-side coverage obligations.
6. **Temperature-conditioned self-refresh behavior** only where a source exposes the exact policy/state relation.

Case 03 remains **grounded**. The new Micron evidence deepens the maintenance-authority / handoff model and closes one earlier-document witness debt, but it does not justify a maturity promotion by itself.
