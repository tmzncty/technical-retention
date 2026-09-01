# Case 06 source-deepening addendum: flip-flop / register boundary

## Status

- **Case:** [`cases/06-flip-flop-powered-working-retention.md`](../cases/06-flip-flop-powered-working-retention.md)
- **Purpose:** close one of the three explicit `first-pass` gaps without pretending the whole case is grounded.
- **Result:** the period `register` boundary has a primary early-computer anchor. A second evidence pass has now directly recovered an ENIAC Part-II textual timing sequence at p. IV-43; see [`06-eniac-timing-retention-deepening.md`](06-eniac-timing-retention-deepening.md). The 1919 Eccles–Jordan authorial page/reprint and the original ENIAC PX-1-105 schematic image still have not been directly inspected. **Case 06 therefore remains `first-pass`.**
- **Related-repository check:** a fresh search of `tmzncty/computing-archaeology` for Eccles–Jordan / ENIAC / flip-flop / register material found no dedicated treatment to reuse.

This note keeps four layers separate:

- `H/P` — period record / primary source;
- `H/S` — archival or scholarly source-location evidence;
- `E` — engineering reconstruction;
- `A` — functional comparison.

---

## 1. Period primary evidence for `register`

### H/P — Whirlwind I uses `register` as a machine-level organization/role, not as a synonym for one bistable element

M. F. Mann, R. R. Rathbone, and J. B. Bennett's MIT Digital Computer Laboratory Report R-221, **_Whirlwind I Operation Logic_**, dated **1 May 1954**, provides a useful period boundary witness.

The report's introduction says that Whirlwind I has a **basic register length of sixteen binary digits**, and describes parallel-digit transmission over a bus with one channel for each digit of the sixteen-digit register. That is already architecture-level language: `register` identifies an organized machine quantity and interface, not merely the existence of a bistable electrical degree of freedom.

More decisively, §2.231 describes the A-register (`AR`) as a **“simple flip-flop register”** and then defines its functions. In the indexed report text, AR is required to:

1. receive a number coming from storage through read-in gates;
2. transmit a number to the accumulator for addition/subtraction;
3. hold the multiplicand and divisor;
4. expose/sign-sense the number for arithmetic control;
5. support complement/sign-changing operations;
6. hold information for later transfer/use.

The historically safe conclusion is therefore narrower than a modern textbook equation:

> In at least one 1954 computer report, `flip-flop` names the implementation family while `A-register` names a grouped, connected, functionally specified machine component.

This directly supports the Case-06 warning **`flip-flop mechanism ≠ register architecture`**. It also prevents an equally bad opposite claim: period engineers certainly *could* call a collection implemented with flip-flops a `flip-flop register`.

**Primary source:** M. F. Mann, R. R. Rathbone, J. B. Bennett, _Whirlwind I Operation Logic_, Project Whirlwind Report R-221, MIT Digital Computer Laboratory, 1 May 1954, especially introduction p. 1-1 and §2.231 / p. 2-12. Digitized copy indexed by Bitsavers: <https://www.bitsavers.org/pdf/mit/whirlwind/R-series/R-221_Whirlwind_I_Operational_Logic_May54.pdf>.

### H/P + limit — Whirlwind's own `register` vocabulary is broader than a modern CPU-register shortcut

R-221's introduction also describes magnetic-core storage in terms of **storage registers**: each digit of a storage register is a particular magnetic core, and a storage access can read/rewrite the old information or insert new information.

That matters methodologically. A period source solves the anachronism problem only if we preserve the period source's *own* semantic range. Whirlwind's `register` cannot simply be translated into today's narrow “small CPU register file” category.

So the new boundary is:

```text
one bistable / flip-flop
    != automatically a register

register
    != one universal physical substrate

period use of register
    != automatically the modern CPU-register category
```

This is stronger than the earlier first-pass wording because it is supported by period architecture vocabulary rather than only by a modern functional distinction.

### H/S — bibliographic identity of R-221 is independently corroborated

MIT's 1954 publication record lists **“Whirlwind I Operation Logic”**, Report R-221, dated 1 May 1954, by M. F. Mann, R. R. Rathbone, and J. B. Bennett. A Computer History Museum finding aid for MIT Computing Projects likewise records `Project Whirlwind Report R-221 Whirlwind Operation Logic`, dated 1954-05-01.

These records corroborate title/date/authorship and keep the source from depending only on a third-party filename.

- MIT, _Report to the President and Chancellor 1954_, Digital Computer Laboratory publication list: <https://web.mit.edu/src/pres-rep/49-58__Killian/1954.pdf>.
- Computer History Museum, _Guide to the Collection of MIT Computing Projects_, hardware/manuals folder list: <https://archive.computerhistory.org/resources/access/text/finding-aids/102634702-MIT/102634702-MIT.pdf>.

---

## 2. What this changes in the retention comparison

### E — a register adds organization and use semantics around retained elements

The Whirlwind evidence makes it unsafe to define a register merely as “a thing that retains bits.” The A-register is situated in a bus, has read-in gates, transmits to an accumulator, holds operands, participates in sign sensing, and has explicitly named machine functions.

The retention-specific reconstruction is:

```text
bistable retained condition
    + grouping
    + connectivity / gating
    + machine-defined role
    + later state-sensitive use
        -> register-level working retention
```

Not every historical register must have exactly these features, and the formula is not offered as a universal definition. It is a bounded explanation of why `register` adds architecture above the elementary retention mechanism in this source.

### E — substrate and architectural role are orthogonal enough to require separate axes

Within the same Whirlwind report, `register` language spans a flip-flop A-register and magnetic-core storage registers. This is a useful counterexample to a substrate-first taxonomy.

For `technical-retention`, future semiconductor/cache work should therefore record separately:

- **state element / substrate:** what physical distinction persists;
- **organization:** how many elements are grouped and selected;
- **architectural role:** what the machine treats the group as doing;
- **interface/use semantics:** how the retained value conditions later operations.

This is an engineering comparison, not a claim that all historical uses of `register` share one invariant definition.

---

## 3. Eccles–Jordan 1919: exact locator recovered, direct inspection still open

### H/S — publication and scan locations are now precise

The 1919 paper can now be located much more exactly than in the first pass:

- W. H. Eccles and F. W. Jordan, **“A trigger relay utilizing three-electrode thermionic vacuum tubes,”** _The Electrician_ 83, **19 September 1919**, p. 298.
- Reprinted in _The Radio Review_ 1(3), **December 1919**, pp. 143–146.
- A digitized _Electrician_ volume is catalogued at Internet Archive with the relevant page at p. 298: <https://archive.org/details/electricaljourna83lond/page/298>.
- The _Radio Review_ reprint is catalogued in HathiTrust at the corresponding sequence: <https://babel.hathitrust.org/cgi/pt?id=mdp.39015021318277&seq=165>.

Later scholarly/technical discussions reproduce the characteristic formulation that the one-stroke relay remains in its new condition until reset, which is consistent with the 1918 patent and with the first-pass engineering reading. But this pass did **not** obtain a directly inspectable page image through the available retrieval path, so the repository should not mark the 1919-paper gap complete on the strength of secondary quotation alone.

Useful locator/corroboration:

- IEEE Spectrum, “Re-creating the First Flip-Flop,” 2018: <https://spectrum.ieee.org/recreating-the-first-flipflop>.
- Michaela Gabrillo and Benjamin Zetter, _Articulating Media_, Open Humanities Press, 2023, discussion citing Eccles & Jordan 1919 p. 298.

---

## 4. ENIAC circuit provenance and Part-II timing evidence

### H/S — original drawing numbers are recoverable

Brian Stuart's Drexel ENIAC drawing index states that most images were processed from scans of the ENIAC patent-trial microfilm, with some higher-quality Smithsonian replacements. The index explicitly lists:

- **PX-1-105 — `Flip-Flop Circuit`**;
- **PX-1-106 — `Gate Tube Circuits`**;
- **PX-1-109 — `Binary Ring Circuit`**.

Its “Other Drawing References” section also records earlier drawing references including:

- **PX-1-3 — `Vacuum Trigger-Circuit (Flip-Flop)`**;
- **PX-1-8 — `Flip-flop Circuit with a Time Constant (Gate Form)`**.

- Drexel ENIAC Drawings index: <https://www.cs.drexel.edu/~bls96/eniac/drawings/>.
- ENIAC Part-II scan: <https://www.cs.drexel.edu/~bls96/eniac/reports/prog2.pdf>.

### H/P — Part II p. IV-43 now supplies a directly recovered machine-specific timing sequence

A second evidence pass directly recovered the primary text at Part II p. **IV-43**. It describes an incoming switch pulse setting an `unsynchronized flip-flop`; that state enables a synchronizing gate so the next central programming pulse can set a `synchronized flip-flop`; the second state enables a transmitter gate; a later central program pulse is transmitted and resets both flip-flops. The report explains the second stage in terms of avoiding unreliable reduced-magnitude pulses when an unsynchronized switch event overlaps a central program pulse.

This materially deepens the ENIAC evidence because the period report itself now supplies the state-transition/timing role. The detailed retention analysis and claim ledger are in [`06-eniac-timing-retention-deepening.md`](06-eniac-timing-retention-deepening.md).

However, **PX-1-105 itself has still not been visually rendered and inspected**. No new drawing-specific resistor values, tube topology, bias conditions, or component-level timing claims are promoted from the textual sequence.

The updated evidence boundary is therefore:

```text
Part-II textual operation directly inspected
    !=
PX-1-105 schematic visually inspected
```

---

## 5. Revised evidence-gap ledger

| Gap from Case 06 first pass | Current evidence | Status after this note |
| --- | --- | --- |
| Directly inspect Eccles–Jordan 1919 paper or page-preserving reprint | exact _Electrician_ and _Radio Review_ scan locators recovered; secondary quotation cross-check found | **open — direct page inspection still required** |
| Recover machine-specific ENIAC Part-II textual operation | Part II p. IV-43 directly supplies a two-flip-flop synchronizing sequence and reliability rationale | **closed for this bounded textual sequence** |
| Inspect original ENIAC PX-1-105 flip-flop schematic | drawing identity/provenance known | **open — schematic image itself still needs direct inspection** |
| Add period primary source for architectural `register` boundary | Whirlwind R-221 (1954), p. 1-1 and §2.231 / p. 2-12 | **closed** |

Because two direct visual/source-inspection gaps remain open, this note does **not** recommend promotion of Case 06 to `grounded`.

---

## 6. Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| R-221 is _Whirlwind I Operation Logic_, dated 1 May 1954, by Mann, Rathbone, Bennett | H/P + H/S | report + MIT publication list + CHM finding aid |
| R-221 calls AR a `simple flip-flop register` | H/P | §2.231 / p. 2-12 indexed primary text |
| R-221 gives AR machine-level functions including receive, transmit, hold, and sign-related use | H/P | §2.231 / p. 2-12 indexed primary text |
| Period `register` vocabulary can name a grouped/functionally situated component implemented with flip-flops | H/P + E | bounded Whirlwind inference |
| `register` in Whirlwind is restricted to the modern CPU-register sense | X | contradicted by R-221's `storage register` vocabulary for core storage |
| Every flip-flop is historically a register | X | not supported by ENIAC/Whirlwind source layers |
| Register role and physical retention substrate should be separate comparison axes | E | bounded cross-mechanism reconstruction |
| PX-1-105 is catalogued as an ENIAC `Flip-Flop Circuit` drawing | H/S | Drexel patent-trial-microfilm drawing index |
| Part II p. IV-43 directly documents an unsynchronized flip-flop -> synchronizing gate -> synchronized flip-flop -> transmitter/reset sequence | H/P | directly recovered primary report text |
| The exact PX-1-105 circuit topology has now been directly verified | X | not established; schematic image remains uninspected |
| The 1919 paper has now been directly page-inspected | X | locator recovered, direct page inspection still open |

---

## Next bounded step

Do **not** open SRAM/cache yet solely because the `register` vocabulary gap and one ENIAC textual-operation gap are closed. The highest-value next move remains to finish the two direct inspections:

1. inspect _The Electrician_ p. 298 or _Radio Review_ pp. 143–146 directly;
2. render and inspect PX-1-105 / immediately relevant ENIAC Part-II drawing material and record exact circuit/topology anchors.

If those confirm the current reconstruction, Case 06 can be reconsidered for `grounded`. If they conflict with it, the case should be corrected rather than promoted.