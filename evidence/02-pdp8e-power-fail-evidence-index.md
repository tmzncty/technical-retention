# Case 02 — PDP-8/E power-fail evidence navigation

**Canonical case:** [`../cases/02-magnetic-core-destructive-read.md`](../cases/02-magnetic-core-destructive-read.md)  
**Parent Case-02 navigation:** [`02-core-retention-evidence-index.md`](02-core-retention-evidence-index.md)  
**Current maturity:** `grounded`  
**Status effect of this index:** navigation only; no maturity promotion

This focused index keeps the PDP-8/E power-transition evidence split into separate source questions instead of repeatedly reopening the same 1973 manual.

---

## Evidence chain

| Slice | Evidence | What it establishes | Boundary |
| --- | --- | --- | --- |
| **Current-cycle closure after power-fail detection** | [`02-dec-pdp8e-1973-power-fail-current-cycle-closure-deepening.md`](02-dec-pdp8e-1973-power-fail-current-cycle-closure-deepening.md) | `POWER OK` loss halts normal timing while memory-side X/Y current withdrawal is delayed sufficiently to complete the active WRITE; DEC describes a fast-on/slow-off power-fail path | stopping normal timing != truncating already-admitted destructive-read/restore work; quiescent nonvolatility != in-flight closure |
| **Electrical trigger and supply hold-up envelope** | [`02-dec-pdp8e-1973-power-ok-threshold-holdup-budget-deepening.md`](02-dec-pdp8e-1973-power-ok-threshold-holdup-budget-deepening.md) | explicit regulated-rail limits that withdraw `POWER OK`, plus a >=2 ms supply-level hold-up specification after line-voltage loss under maximum load | rail threshold != magnetic payload failure; line-loss hold-up != post-`POWER OK` residual time != memory slow-off delay != measured restore margin |

---

## Combined historical record

The September-1973 DEC maintenance manual now supports the following bounded sequence without importing modern crash-consistency vocabulary into the historical layer:

```text
line-power / regulated-rail condition degrades
    -> voltage monitor withdraws POWER OK at documented rail limits
    -> normal timing chain is stopped
    -> current core-memory cycle is nevertheless completed
    -> X/Y current-source removal is delayed sufficiently to complete WRITE
    -> current source is then withdrawn
```

The supply documentation separately gives a minimum **2 ms regulated-output hold-up after loss of line voltage under maximum load**.

That number is not a documented memory slow-off timer.

---

## Engineering reconstruction

Project terminology can now distinguish four boundaries:

```text
upstream power-loss event
    !=
control threshold crossing
    !=
withdrawal of new-work authority
    !=
withdrawal of completion capability
```

For this named implementation, `POWER OK` functions as a transition-control boundary rather than a direct measurement that core remanence has already failed.

The combined evidence also supports a bounded **drain-before-withdraw** reconstruction:

```text
stop normal progression
    -> preserve enough electrical / drive capability to close current WRITE
    -> withdraw memory current afterward
```

`drain-before-withdraw` and `transition-authority signal` are repository engineering terms, not DEC's 1973 vocabulary.

---

## Quantitative boundary

The new electrical packet closes the earlier source-level question `what rail conditions cause POWER OK to be withdrawn?` and adds a supply-level hold-up figure.

It does **not** justify this arithmetic:

```text
2 ms supply hold-up
- some software / memory interval
= exact safety margin
```

The reference events are not established as identical. In particular:

```text
line-voltage loss time
    != documented POWER OK crossing time

POWER OK crossing time
    != numeric X/Y slow-off completion time
```

A real margin calculation still needs aligned trigger points and timing measurements or engineering-drawing values.

---

## Historical / analogy / interpretation discipline

### Historical record

Keep DEC's own terms attached to the source: `POWER OK`, timing chain, READ, WRITE, X/Y current source, regulated rail limits, and hold-up time.

### Engineering reconstruction

Use project terms such as `transition-authority signal`, `drain-before-withdraw`, and `completion capability` only as mechanism descriptions derived from the documented behavior.

### Functional analogy

Later DRAM, Flash, storage-controller, or distributed-maintenance systems may share the relation:

```text
failure detected
    -> stop admitting new work
    -> still permit bounded completion of already-admitted work
```

That is a functional comparison, not a genealogy.

### Philosophical interpretation

The bounded project interpretation is that a power transition can contain several ordered technical boundaries rather than one instantaneous `power gone` event. This is not a historical claim about DEC's conceptual language.

---

## Related-repository routing

The broader magnetic-core / computer-architecture history remains routed to:

- [`tmzncty/computing-archaeology/docs/memory/why-core-memory-was-worth-weaving.md`](https://github.com/tmzncty/computing-archaeology/blob/main/docs/memory/why-core-memory-was-worth-weaving.md)

A fresh search for `H724` in `tmzncty/computing-archaeology` found no dedicated packet to reuse. A general PDP-8/E power-supply history should be developed there rather than expanded inside this retention sub-index.

---

## Remaining debt

Highest-value next steps are now narrower:

1. find the numeric `POWER OK`-to-X/Y-current-off delay, if exposed in engineering drawings or component timing;
2. produce a phase-specific fault trace for READ / sense-register capture / WRITE-restoration interruption;
3. find a named core-memory controller with a materially different power-fail policy;
4. compare nominal maintenance-manual timing with field/service measurements on aged hardware.

Case 02 remains **`grounded`**. `CASE_INDEX.md` remains the authoritative maturity ledger; this focused index does not replace or reconstruct it.
