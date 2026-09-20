# Case 21 evidence deepening: Micron 2014–2015 self-refresh handoff gap and compensating refresh

## Status

**Bounded deepening complete.**

This packet adds a later Micron product-document witness to Case 21. It does not replace the 1999 SDR SDRAM grounding record. Its purpose is narrower: document a refresh-maintenance discontinuity that Micron itself exposes at self-refresh exit, plus a concrete externally scheduled refresh-window failure around a mode transition.

The bounded conclusion is:

```text
self-refresh mode active
    !=
all refresh accounting around mode exit is automatically closed

mode exit registered
    !=
no maintenance event can fall into the handoff seam

refresh feature exists
    !=
required refresh coverage was actually supplied in the relevant window
```

The later Micron LPDDR2/LPDDR3 documents explicitly require a compensating REFRESH after self-refresh exit before a subsequent self-refresh entry because an internally timed refresh event can be missed at exit. The LPDDR2 document also gives an unsupported refresh-pattern transition whose refresh window contains only about half the required number of refresh commands.

Case 21 remains **`grounded`**. This packet deepens one failure/control boundary; it does not promote the case to a stronger maturity state.

---

## Research question

Case 21 already established a mode-mediated transfer of recurring refresh responsibility:

```text
normal operation
    host/controller supplies recurring refresh commands

self refresh
    DRAM supplies internal recurring refresh work

exit
    external responsibility resumes
```

The question here is more specific:

> Does crossing the boundary between internally generated self-refresh work and externally supplied refresh work automatically preserve a continuous maintenance accounting relation, or can the transition itself require explicit compensation?

A second, related question is:

> Can an externally generated refresh pattern look active while still failing the required coverage window?

These are engineering questions about a named command contract, not a claim about generic DRAM philosophy.

---

## Source custody and scope

### Primary authored document used for the main reconstruction

Micron Technology, Inc., _8GB: eMMC and 8Gb: 2 x 4Gb Single-Channel LPDDR2 MCP_, PDF identifier `09005aef8562a3ca`, file `162ball_j95l_451_2e0e.pdf`, Rev. F, May 2015.

The inspected copy is hosted as an attachment on NXP Community:

<https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/imx-processors/80733/1/MT29PZZZ8D5BKFTF-18%2520W%2520.pdf>

The PDF identifies Micron as author/copyright holder and gives the document identifier, revision, date, part family, contents, figure numbers, and revision history. Hosting by NXP is a custody fact; it is not treated as evidence that NXP authored the memory semantics.

Relevant printed pages/sections:

- printed p. 83: regular distributed refresh example;
- printed pp. 85–86: unsupported/supported transition examples around repetitive refresh bursts and self refresh;
- printed pp. 88–89: `SELF REFRESH Operation` and Figure 50;
- printed p. 89 notes: all-banks-idle entry precondition and `tXSR` restrictions.

### Corroborating later-family document

Micron Technology, Inc., _178-Ball, Single-Channel Mobile LPDDR3 SDRAM_, PDF identifier `09005aef858e9dd3`, file `178b_8-16gb_2c0f_mobile_lpddr3.pdf`, Rev. D, September 2014.

Public searchable copy:

<https://dtsheet.com/doc/1384705/178-ball--single-channel-mobile-lpddr3-sdram>

The corroborating document repeats the missed-internal-refresh-at-exit warning and the requirement for an extra refresh before returning to self refresh. It is used only as an independent Micron product-family continuity witness, not as proof that LPDDR2 and LPDDR3 share identical internal implementation.

### What was not inspected

This packet does **not** claim direct inspection of the complete JEDEC LPDDR2/LPDDR3 standard genealogy, silicon RTL, analog refresh timer implementation, or fault-injection traces. It does not establish the first historical appearance of this rule.

---

# Historical record

## 1. The 2015 Micron LPDDR2 MCP exposes a refresh-window obligation, not merely an average activity indication

The Micron LPDDR2 portion describes REFRESH in terms of a bounded refresh window and required number of refresh operations. Its examples distinguish a regular distributed pattern, repetitive burst refresh, supported transitions, and an explicitly unsupported transition.

The regular distributed example shows refresh commands spread across the refresh window. Micron also allows a burst/pause style pattern under defined constraints.

The important counterexample is Figure 46, `Nonsupported Transition from Repetitive REFRESH Burst`. Micron marks a refresh window with **insufficient REFRESH commands** and explains that only about 2,048 commands appear in a window requiring the specified minimum count `R`.

Therefore, the historical document itself distinguishes:

```text
some REFRESH commands occurred
    !=
required refresh-window coverage was satisfied
```

This is stronger evidence than a generic statement that DRAM needs periodic refresh: it gives a manufacturer-authored transition pattern that is rejected because the required window accounting is not met.

## 2. Micron provides a recommended self-refresh entry/exit placement relative to burst/pause refresh

Figure 47 is titled `Recommended Self Refresh Entry and Exit` and places self refresh inside the surrounding refresh-window accounting of a burst/pause regime.

That figure matters because self refresh is not documented as a timeless escape hatch from the external refresh contract. Entry and exit occur within a larger temporal maintenance relation.

The document does not say that every entry/exit at any arbitrary point is equivalent. It shows a recommended transition in conjunction with the surrounding refresh pattern.

## 3. Entry has a state precondition

The LPDDR2 self-refresh timing notes state that the device must be in the **all banks idle** state before entering self refresh.

The entry command is registered with the documented CKE/command encoding, after which CKE must remain LOW to keep the device in self-refresh mode.

After entry, the device performs at least one all-bank refresh internally during `tCKESR`; the device must remain in self refresh for at least `tCKESR`.

Thus the historical interface exposes at least three distinct conditions:

```text
entry command encoding
    !=
entry-state precondition
    !=
minimum residence / internal-maintenance interval
```

## 4. Exit has a service-restoration delay

For exit, Micron requires the external clock to be stable before CKE returns HIGH. After self-refresh exit is registered, the device must remain in the `tXSR` interval before a valid command is issued. CKE remains HIGH and NOPs are issued during that interval so any internal refresh already in progress can complete.

This preserves the Case 21 distinction:

```text
exit requested/registered
    !=
ordinary command service admissible
```

## 5. The exit boundary can miss an internally timed refresh event

The key historical statement is explicit: Micron says self-refresh use creates the possibility that an internally timed refresh event is missed when CKE is driven HIGH for self-refresh exit.

Micron then requires, after exit, at least one REFRESH before a subsequent SELF REFRESH command:

- one all-bank REFRESH; or
- eight per-bank REFRESH commands.

This is not inferred from generic DRAM theory. It is a named manufacturer requirement in the product document.

The 2014 Micron LPDDR3 document independently repeats the same control boundary: an internally timed refresh event can be missed as CKE rises for exit, and at least one extra REFRESH is required before the device returns to self refresh.

## 6. The compensating refresh is not described as ordinary payload restoration after known corruption

Neither inspected Micron passage says that data has already been lost at every self-refresh exit. The wording is preventive: a refresh event **can** be missed, and an extra refresh is therefore required before a later self-refresh transition.

Accordingly, the correct historical claim is about a protocol maintenance obligation, not a measured corruption event.

---

# Engineering reconstruction

## 7. Maintenance-authority transfer is not automatically maintenance-accounting closure

Case 21's earlier model separated who causes recurring refresh work:

```text
external recurrence
    -> self-refresh internal recurrence
    -> external recurrence
```

The later Micron evidence adds a missing layer:

```text
who currently owns recurrence
    !=
whether all maintenance debt at the handoff boundary is already closed
```

An internal refresh timer can be approaching an event when CKE rises. The mode transition changes the source of future refresh work, yet the device contract still requires explicit compensation before the next self-refresh entry.

A useful bounded reconstruction is:

```text
internal maintenance regime
    -> exit boundary
    -> possible unperformed internal event
    -> external compensating REFRESH
    -> later self-refresh re-entry admitted
```

`Maintenance debt` and `handoff seam` are project vocabulary, not Micron's period terms.

## 8. A mode boundary can preserve payload while leaving a maintenance obligation outstanding

The device can exit self refresh without the documentation claiming immediate data loss, while still imposing a mandatory extra refresh before another self-refresh entry.

Therefore:

```text
payload presently readable/retained
    !=
maintenance obligation fully discharged
```

This distinction matters across the repository because many retained systems expose a usable state before every preventive-maintenance relation has necessarily been renewed.

## 9. Transition completion is not coverage completion

`tXSR` answers one question: when may ordinary commands resume after exit while an internal refresh may be finishing?

The mandatory extra REFRESH answers another question: what must be done because an internally timed refresh could have been missed at the transition?

So:

```text
tXSR satisfied
    !=
all refresh accounting around the transition is closed
```

and:

```text
ordinary service admissible
    !=
future self-refresh re-entry admissible without compensating maintenance
```

The two constraints should not be collapsed into one generic `self refresh exit completed` state.

## 10. Maintenance existence is not maintenance coverage

The unsupported LPDDR2 transition gives a particularly clean negative witness.

A trace may contain many refresh commands and still fail the required refresh window. The problem is not absence of the mechanism. It is insufficient coverage in the governing interval.

This yields:

```text
refresh command exists
    !=
refresh cadence is sufficient
    !=
refresh-window coverage is sufficient
```

That directly connects Case 21 to the repository's maintenance-observability work without turning a timing diagram into telemetry.

## 11. Entry encoding is not entry admission

The all-banks-idle requirement means that a host/controller cannot reason only from the command opcode/CKE encoding.

A stronger decomposition is:

```text
entry requested
    !=
entry preconditions satisfied
    !=
self-refresh regime established
    !=
minimum self-refresh residence completed
```

The document does not supply a field-failure probability for violating these rules, so the repository should not invent one.

## 12. The compensating refresh is a closure action, not proof of a known lost row

The required post-exit refresh is best reconstructed as closure of a possible maintenance gap. It is not evidence that the device identifies a specific missed row or exposes the internal timer phase to the host.

Nothing in the inspected text demonstrates that the host knows which internal event was missed, whether one was actually missed on a particular exit, or which exact row would otherwise become most vulnerable.

Therefore:

```text
mandatory compensation
    !=
positive diagnosis of a specific failed refresh event
```

## 13. Refresh-window arithmetic is relational retained evidence

The unsupported-transition diagram also shows why the relevant object is not merely a counter value.

For retention reasoning, the relation includes:

```text
number of refresh operations
    + their placement in the required window
    + transition timing
    + mode state
```

A raw count outside its time window is insufficient to prove compliance.

This is an engineering reconstruction from Micron's timing diagrams, not a claim that the device stores a literal host-visible `maintenance ledger`.

---

# Controlled functional comparisons

## 14. Comparison to the 1999 Micron SDR SDRAM witness

The 1999 Case 21 source establishes external AUTO REFRESH versus internal SELF REFRESH recurrence and `tXSR` on exit.

The 2014–2015 mobile-memory evidence adds a later, more explicit transition obligation: an internal refresh event may be missed at exit and the next self-refresh entry is gated by compensating external refresh.

This is a **later functional deepening**, not evidence that the exact LPDDR2/LPDDR3 rule existed unchanged in the 1999 parts.

## 15. Comparison to Case 03

Case 03 separates dynamic-cell retention, refresh requests, arbitration, enumeration, and maintenance execution in earlier controller architectures.

The present packet is complementary: it shows a mode-transition boundary where maintenance recurrence changes regime and the interface explicitly requires compensation.

No hardware genealogy between those controllers and Micron LPDDR2 is claimed.

## 16. Comparison to Case 45 / later DDR maintenance-state work

Later DDR5 cases distinguish self-refresh transition lifetime, maintenance counters, diagnostic state, and coverage validity.

Case 21's new evidence is narrower and earlier: it does not concern DDR5 ECS or REFsb counter reset. The functional similarity is only that a mode transition can affect maintenance-state interpretation or obligations without being equivalent to payload loss.

## 17. Comparison to Synthesis 29

Synthesis 29 distinguishes maintenance schedule, admission, execution, coverage, accounting, and closure.

The LPDDR2 timing diagrams provide a concrete DRAM witness for the same analytical separation:

```text
REFRESH commands visible in a trace
    !=
coverage of the required refresh window

self-refresh exit complete enough for service
    !=
maintenance closure sufficient for immediate re-entry
```

This is a functional comparison. Micron did not use the synthesis vocabulary.

---

# Philosophical interpretation boundary

A limited conceptual observation is permissible: preserving a state can depend on continuity of maintenance relations across a change in who performs the maintenance. A system may preserve the payload while still owing a transition-specific maintenance action.

That observation must remain downstream of the technical evidence.

This packet does **not** claim that Micron described self refresh in terms of memory, remembrance, institutional responsibility, care, archive, or forgetting. It does not transform a timing requirement into a philosophy of continuity.

---

# Explicit non-claims

This packet does **not** establish that:

1. Micron invented self refresh;
2. Micron invented the post-exit extra-refresh rule;
3. the inspected 2015 LPDDR2 document is the first standard or product to contain the rule;
4. the LPDDR2 and LPDDR3 devices have identical internal circuits;
5. the 1999 SDR SDRAM family already had the same missed-event mechanism;
6. one refresh event is always missed at every self-refresh exit;
7. a missed internally timed event necessarily causes immediate payload corruption;
8. the mandatory compensating REFRESH proves that corruption already occurred;
9. `tXSR` itself performs the compensating refresh;
10. satisfying `tXSR` removes the post-exit refresh requirement;
11. one all-bank refresh and eight per-bank refreshes are universally interchangeable across all DRAM standards;
12. an all-banks-idle precondition proves an implementation-specific internal state machine;
13. a REFRESH command proves every row met its physical retention margin;
14. a large number of refresh commands proves the governing refresh window was satisfied;
15. an average refresh rate alone proves the placement constraints in every window;
16. the unsupported transition diagram is a measured field-failure trace;
17. the unsupported transition diagram reports a measured bit-error rate;
18. the host can observe which specific internal refresh event was missed;
19. the host can observe the internal refresh timer phase from the cited interface;
20. the post-exit refresh requirement is a form of ECC repair;
21. self refresh provides nonvolatile retention without device power;
22. CKE alone proves safe surrounding-system power removal;
23. controller status in another product family proves physical cell health;
24. LPDDR2/LPDDR3 timing semantics define the complete JEDEC genealogy;
25. a document hosted by NXP was authored by NXP;
26. a mirrored searchable LPDDR3 copy is stronger provenance than the Micron-authored document identity it reproduces;
27. this packet closes empirical fault-injection or brownout behavior;
28. this packet measures retention margin at temperature extremes;
29. this packet establishes controller-software correctness in any shipping platform;
30. this packet establishes a philosophical theory of maintenance responsibility.

---

# Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Micron Rev. F 05/15 LPDDR2 MCP documents distributed/burst refresh patterns and refresh-window requirements | H/P | Micron-authored product PDF, pp. 83–86 |
| Micron marks one repetitive-burst transition as unsupported because the indicated refresh window contains only about 2,048 REFRESH commands rather than the required minimum | H/P | Figure 46 and note, printed p. 86 |
| Micron documents a recommended self-refresh entry/exit placement in the surrounding burst/pause refresh pattern | H/P | Figure 47, printed p. 87 |
| LPDDR2 self-refresh entry requires all banks idle | H/P | Figure 50 notes, printed p. 89 |
| LPDDR2 self refresh performs internal refresh and requires minimum `tCKESR` residence | H/P | `SELF REFRESH Operation`, printed pp. 88–89 |
| Exit requires stable clock, CKE HIGH, NOPs, and `tXSR` before valid commands | H/P | `SELF REFRESH Operation`, printed p. 89 |
| An internally timed refresh event can be missed when CKE rises for exit | H/P | Micron Rev. F 05/15, printed p. 89 |
| Before subsequent self refresh, the host must issue one all-bank REFRESH or eight per-bank REFRESH commands | H/P | same passage |
| Micron Rev. D 09/14 LPDDR3 independently repeats the missed-event and extra-refresh rule | H/P | Micron-authored LPDDR3 product document, printed pp. 69–71 |
| Maintenance-authority transfer is distinct from maintenance-accounting closure | E | bounded reconstruction from the documented post-exit compensation |
| Service-admission timing is distinct from transition-specific maintenance closure | E | `tXSR` versus mandatory extra REFRESH |
| Refresh activity is distinct from required refresh-window coverage | E | Figure 46 negative witness |
| The mandatory extra REFRESH proves a specific row was already corrupted | X | source states possibility/rule, not diagnosed corruption |
| The 2015 mobile-memory behavior can be projected unchanged into the 1999 SDR SDRAM | X | later-family deepening only |

---

# Remaining debt

The most useful next checks are narrow:

- inspect the normative JEDEC LPDDR2/LPDDR3 clauses and revision chronology for the same exit-compensation rule;
- determine the first public revision/product family in which Micron exposed this exact wording;
- find a named memory-controller implementation that explicitly schedules the required post-exit compensating refresh and inspect its reset/error path;
- perform controlled timing/fault experiments around self-refresh exit and immediate re-entry on real hardware;
- distinguish the consequences of violating the all-banks-idle entry precondition from violating the post-exit extra-refresh rule;
- keep temperature-dependent retention margin, PASR coverage, and later DDR5 maintenance-state transitions in their own cases unless a source establishes a direct relation.

Broader DRAM-generation and standards history should be developed in `tmzncty/computing-archaeology` rather than duplicated here.

---

# Related repository check

A fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for `self refresh`, `SDRAM`, `CKE`, `LPDDR`, and missed-refresh wording found no dedicated packet suitable for reuse in this slice.

Accordingly, this evidence file retains only the bounded retention/control reconstruction. A full standards and product-line history belongs in the archaeology repository if undertaken later.

---

# Sources

1. Micron Technology, Inc., _8GB: eMMC and 8Gb: 2 x 4Gb Single-Channel LPDDR2 MCP_, `09005aef8562a3ca`, `162ball_j95l_451_2e0e.pdf`, Rev. F, May 2015, especially printed pp. 83–89. NXP-hosted preserved copy: <https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/imx-processors/80733/1/MT29PZZZ8D5BKFTF-18%2520W%2520.pdf>.
2. Micron Technology, Inc., _178-Ball, Single-Channel Mobile LPDDR3 SDRAM_, `09005aef858e9dd3`, `178b_8-16gb_2c0f_mobile_lpddr3.pdf`, Rev. D, September 2014, especially self-refresh / refresh-requirement material around printed pp. 69–71. Searchable preserved copy: <https://dtsheet.com/doc/1384705/178-ball--single-channel-mobile-lpddr3-sdram>.
3. Existing Case 21 grounding for the earlier SDR SDRAM mode-handoff witness: [`21-micron-1999-sdram-refresh-mode-grounding.md`](21-micron-1999-sdram-refresh-mode-grounding.md).
4. Canonical case: [`../cases/21-micron-sdram-refresh-mode-handoff.md`](../cases/21-micron-sdram-refresh-mode-handoff.md).
