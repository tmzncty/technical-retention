# Case 21 — refresh-handoff evidence navigation

## Canonical status

Case 21 remains **`grounded`**.

Canonical case:

- [`../cases/21-micron-sdram-refresh-mode-handoff.md`](../cases/21-micron-sdram-refresh-mode-handoff.md)

This index is navigation only. It does not replace the canonical case or `ROADMAP.md`, and adding a deepening packet does not by itself promote maturity.

## Evidence chain

### 1. 1999 Micron SDR SDRAM grounding

[`21-micron-1999-sdram-refresh-mode-grounding.md`](21-micron-1999-sdram-refresh-mode-grounding.md)

Primary role:

- named Micron 64Mb SDR SDRAM family;
- `AUTO REFRESH` is nonpersistent and externally repeated;
- refresh row address generation is internal;
- `SELF REFRESH` internalizes recurring refresh clocking/work;
- exit requires stable external clocking and `tXSR` before ordinary service;
- grounds the base distinction `refresh obligation != recurring command-generation responsibility`.

### 2. 2014–2015 Micron mobile-memory handoff-gap deepening

[`21-micron-2014-2015-self-refresh-handoff-gap-deepening.md`](21-micron-2014-2015-self-refresh-handoff-gap-deepening.md)

Primary role:

- named Micron LPDDR2 MCP plus corroborating Micron LPDDR3 product document;
- explicit all-banks-idle entry precondition;
- explicit possibility of an internally timed refresh event being missed at self-refresh exit;
- mandatory compensating external REFRESH before a subsequent self-refresh entry;
- manufacturer-authored unsupported transition with insufficient REFRESH commands inside the governing refresh window;
- deepens the distinction `mode transition completed != maintenance-accounting closure` and `refresh activity != refresh-window coverage`.

## Current bounded result

The current evidence chain supports the following decomposition without asserting a universal DRAM genealogy:

```text
physical refresh obligation
    !=
refresh-row enumeration
    !=
recurring refresh-event source
    !=
self-refresh entry admission
    !=
mode-transition completion
    !=
refresh-window coverage
    !=
transition-specific compensating maintenance
    !=
ordinary service admission
```

The 1999 source grounds a reversible handoff between external and internal recurrence. The 2014–2015 source shows that a later Micron mobile-memory interface treats the handoff boundary itself as capable of leaving a specific maintenance obligation outstanding.

## Roadmap relation

This evidence materially advances the open DRAM failure-mode seam around missed externally issued refresh cadence and refresh-mode transitions:

- a Micron LPDDR2 timing example explicitly rejects a transition that supplies only about 2,048 REFRESH commands in a window requiring the full minimum count;
- Micron LPDDR2/LPDDR3 explicitly warn that an internally timed refresh event can be missed on self-refresh exit and require an extra REFRESH before re-entry.

The roadmap gap should nevertheless **not** be treated as empirically closed. Still open are actual payload-loss thresholds under violated timing, controller reset/power sequencing, loss of the powered self-refresh regime, standards-wide genealogy, and controlled hardware fault injection.

## Related repository routing

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `self refresh`, `SDRAM`, `CKE`, `LPDDR`, and missed-refresh wording found no dedicated technical-history packet to reuse.

Broader DRAM-generation history, JEDEC revision genealogy, controller evolution, and first-introduction priority belong there if pursued comprehensively. Case 21 should remain bounded to retention/maintenance relations.

## Next narrow evidence targets

1. Directly inspect the relevant normative JEDEC LPDDR2/LPDDR3 clauses and revision chronology.
2. Find a named memory-controller implementation that schedules the required post-exit compensating refresh and inspect its reset/error path.
3. Separate violation of the all-banks-idle entry precondition from violation of the post-exit compensation rule.
4. Add controlled hardware timing/fault evidence if a suitable platform is available.
5. Keep temperature-dependent refresh rate and PASR coverage in their dedicated cases unless a source establishes a direct relation.
