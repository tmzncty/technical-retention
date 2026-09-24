# Case 02 — magnetic-core power / restart evidence index

## Status

**Case maturity: `grounded`.**

This index is navigation for the power-transition / restart subproblem inside [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md). It does not replace the main Case 02 grounding record or promote the authoritative maturity ledger.

## Evidence chain

1. [`02-magnetic-core-1951-1954-grounding.md`](02-magnetic-core-1951-1954-grounding.md) — main remanence, destructive-read and rewrite grounding.
2. [`02-ibm-705-1954-1955-indefinite-retention-vocabulary-deepening.md`](02-ibm-705-1954-1955-indefinite-retention-vocabulary-deepening.md) — early commercial retention vocabulary; not a quantified lifetime or restart contract.
3. [`02-mtc-1956-1957-nonvolatile-system-power-removal-boundary-deepening.md`](02-mtc-1956-1957-nonvolatile-system-power-removal-boundary-deepening.md) — IRE 1956 medium/system distinction plus MTC 1957 power, environmental and restart-context evidence.
4. [`02-ibm-7090-1960-1962-power-on-clear-retention-policy-deepening.md`](02-ibm-7090-1960-1962-power-on-clear-retention-policy-deepening.md) — startup policy can deliberately clear a remanent medium.
5. [`02-1965-1966-core-power-transition-retention-deepening.md`](02-1965-1966-core-power-transition-retention-deepening.md) — IBM 1401 controlled retention and PDP-7 explicit transition protection / control-state reset.
6. [`02-dec-1966-1969-pdp8-memory-power-cycle-diagnostic-deepening.md`](02-dec-1966-1969-pdp8-memory-power-cycle-diagnostic-deepening.md) — machine-level power-cycle retention diagnostic and later restoration evidence.

## Current anti-collapse

```text
magnetic remanence
    != system power-removal retention contract
    != safe transition
    != powered operating qualification
    != startup policy
    != restart-context completeness
    != exact execution resume
```

The new MTC/IRE packet strengthens the first boundary with period vocabulary: the 1956 IRE definition itself warns that nonvolatile media do not determine whether the enclosing device/system retains information through power removal.

## Open work

Highest-value remaining debts are now narrower:

- direct **Whirlwind** startup/shutdown primary evidence;
- pre-1956 `volatile` / `nonvolatile` terminology genealogy;
- uncontrolled brownout / partial-rail behavior on a named core-memory machine;
- exact restart-software reconstruction where retained core payload is combined with separately retained/re-entered control state;
- broader power-control genealogy, which belongs primarily in `tmzncty/computing-archaeology`.

Fresh searches in `computing-archaeology` for MTC power, the 1957 MTC Service Manual, and the IRE nonvolatile-power-removal distinction found no dedicated packet to reuse.

## Claim-layer boundary

- **Historical record:** IRE definitions, MTC/IBM/DEC manuals and diagnostics.
- **Engineering reconstruction:** separation of medium retention, transition integrity, powered qualification and restart context.
- **Functional analogy:** later persistence-domain / restart systems only at the relation level.
- **Philosophical interpretation:** material endurance is not automatically operational availability.

No functional analogy in this index is a genealogy claim.
