# Case 06 source-deepening addendum: flip-flop / register boundary

## Status

- **Case:** [`cases/06-flip-flop-powered-working-retention.md`](../cases/06-flip-flop-powered-working-retention.md)
- **Purpose:** close explicit source gaps while preserving claim-specific evidence boundaries.
- **Result:** the period `register` boundary has a primary early-computer anchor. ENIAC Part II p. IV-43 directly supplies a machine-specific timing sequence; see [`06-eniac-timing-retention-deepening.md`](06-eniac-timing-retention-deepening.md). The British Association's contemporary proceedings independently anchor Eccles and Jordan's 1919 regenerative mechanism beyond the patent; see [`06-eccles-jordan-1919-proceedings-deepening.md`](06-eccles-jordan-1919-proceedings-deepening.md). A later grounding pass directly inspected Arthur W. Burks's 1947 period-published simplified ENIAC flip-flop schematic and mechanism/timing discussion; see [`06-burks-1947-eniac-flip-flop-grounding.md`](06-burks-1947-eniac-flip-flop-grounding.md). **Case 06 is now `grounded`.** Exact _Electrician_ / _Radio Review_ facsimiles and PX-1-105 remain archival cleanup for artifact-specific claims, not generic mechanism blockers.
- **Related-repository check:** fresh searches of `tmzncty/computing-archaeology` for Eccles–Jordan / ENIAC / flip-flop / register material found no dedicated treatment to reuse.

This note keeps four layers separate:

- `H/P` — period record / primary source;
- `H/S` — archival or scholarly source-location evidence;
- `E` — engineering reconstruction;
- `A` — functional comparison.

---

## 1. Period primary evidence for `register`

### H/P — Whirlwind I uses `register` as a machine-level organization/role, not as a synonym for one bistable element

M. F. Mann, R. R. Rathbone, and J. B. Bennett's MIT Project Whirlwind Report R-221, **_Whirlwind I Operation Logic_**, dated **1 May 1954**, provides a useful period boundary witness.

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

So the boundary is:

```text
one bistable / flip-flop
    != automatically a register

register
    != one universal physical substrate

period use of register
    != automatically the modern CPU-register category
```

### H/S — bibliographic identity of R-221 is independently corroborated

MIT's 1954 publication record lists **“Whirlwind I Operation Logic”**, Report R-221, dated 1 May 1954, by M. F. Mann, R. R. Rathbone, and J. B. Bennett. A Computer History Museum finding aid for MIT Computing Projects likewise records `Project Whirlwind Report R-221 Whirlwind Operation Logic`, dated 1954-05-01.

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

Within the same Whirlwind report, `register` language spans a flip-flop A-register and magnetic-core storage registers. Future semiconductor/cache work should therefore record separately:

- **state element / substrate:** what physical distinction persists;
- **organization:** how many elements are grouped and selected;
- **architectural role:** what the machine treats the group as doing;
- **interface/use semantics:** how the retained value conditions later operations.

This is an engineering comparison, not a claim that all historical uses of `register` share one invariant definition.

---

## 3. Eccles–Jordan 1919: contemporary authorial mechanism text recovered; exact periodical facsimile remains cleanup

### H/P — British Association proceedings directly record the trigger-relay mechanism

The published _Report of the Eighty-Seventh Meeting of the British Association for the Advancement of Science: Bournemouth: 1919, September 9–13_ records Eccles and Jordan's paper **“A Trigger Relay utilising Three Electrode Thermionic Vacuum Tubes”** in the Transactions of Section G, printed pp. 271–272.

The report directly describes a cascade amplifier with resistance coupling, an even number of valves, back coupling from the last valve to the first producing the trigger action, an external electrical stimulus, mutually reinforcing current/potential changes, and `no restoring influence` while the first-valve current proceeds toward its limiting condition.

The printed footnote points to _The Electrician_, 19 September 1919, p. 298 and _Radio Review_, vol. I, p. 143. This closes the substantive contemporary authorial mechanism-text gap beyond GB148582A while preserving period vocabulary (`trigger relay`, coupling, stimulus, restoring influence) rather than rewriting it as `bit`, `memory cell`, or `register`.

Full notes: [`06-eccles-jordan-1919-proceedings-deepening.md`](06-eccles-jordan-1919-proceedings-deepening.md). Primary scan/text host: <https://archive.org/details/reportofbritisha20adva>.

### H/S + limit — exact _Electrician_ / _Radio Review_ page-image inspection remains open

The exact locators remain:

- W. H. Eccles and F. W. Jordan, **“A trigger relay utilizing three-electrode thermionic vacuum tubes,”** _The Electrician_ 83, **19 September 1919**, p. 298;
- reprinted in _The Radio Review_ 1(3), **December 1919**, pp. 143–146;
- Internet Archive locator: <https://archive.org/details/electricaljourna83lond/page/298>;
- HathiTrust locator: <https://babel.hathitrust.org/cgi/pt?id=mdp.39015021318277&seq=165>.

Those exact page images still have not been reliably rendered here, so the repository does not claim their figures, typography, or exact page wording. Their status is archival cleanup because the mechanism has independent contemporary primary support.

---

## 4. ENIAC circuit provenance, report timing evidence, and Burks 1947 grounding

### H/S — original drawing numbers are recoverable

Brian Stuart's Drexel ENIAC drawing index states that most images were processed from scans of the ENIAC patent-trial microfilm, with some higher-quality Smithsonian replacements. The index lists:

- **PX-1-105 — `Flip-Flop Circuit`**;
- **PX-1-106 — `Gate Tube Circuits`**;
- **PX-1-109 — `Binary Ring Circuit`**;
- earlier references PX-1-3 — `Vacuum Trigger-Circuit (Flip-Flop)` and PX-1-8 — `Flip-flop Circuit with a Time Constant (Gate Form)`.

- Drexel ENIAC Drawings index: <https://www.cs.drexel.edu/~bls96/eniac/drawings/>.
- ENIAC Part-II scan: <https://www.cs.drexel.edu/~bls96/eniac/reports/prog2.pdf>.

### H/P — Part II p. IV-43 supplies a directly recovered machine-specific timing sequence

Part II p. **IV-43** describes an incoming switch pulse setting an `unsynchronized flip-flop`; that state enables a synchronizing gate so the next central programming pulse can set a `synchronized flip-flop`; the second state enables a transmitter gate; a later central program pulse is transmitted and resets both flip-flops. The report explains the second stage in terms of avoiding unreliable reduced-magnitude pulses when an unsynchronized switch event overlaps a central program pulse.

Detailed analysis: [`06-eniac-timing-retention-deepening.md`](06-eniac-timing-retention-deepening.md).

### H/P — Burks 1947 closes the bounded circuit-mechanism gap with a directly inspected published schematic

Arthur W. Burks's **“Electronic Computing Circuits of the ENIAC,”** _Proceedings of the I.R.E._ 35(8), August 1947, pp. 756–767, supplies a directly inspectable period-published ENIAC circuit account. On p. 757 Burks explicitly classifies the flip-flop among remembering circuits. On p. 758, Section IV and Fig. 3 directly show a simplified accumulator program-control circuit and explain that the ENIAC flip-flop has two stable states because of direct-current plate-to-opposite-grid cross-coupling. Burks separately treats steady-state stability and triggering/recovery dynamics. On p. 759 he gives the microsecond-scale set, recovery, and machine timing margins.

Full grounding record: [`06-burks-1947-eniac-flip-flop-grounding.md`](06-burks-1947-eniac-flip-flop-grounding.md).

The exact PX-1-105 drawing itself still has not been visually inspected, so drawing-specific claims remain prohibited. The evidence boundary is now:

```text
Burks 1947 period-published simplified schematic directly inspected
    = bounded ENIAC bistability mechanism grounded

Burks published schematic
    !=
PX-1-105 original drawing facsimile
```

---

## 5. Revised evidence-gap ledger

| Gap from Case 06 first pass | Current evidence | Status now |
| --- | --- | --- |
| Contemporary Eccles–Jordan authorial mechanism text beyond the patent | British Association 1919 meeting proceedings, pp. 271–272, directly recovered | **closed for mechanism evidence** |
| Exact _Electrician_ / _Radio Review_ facsimile inspection | exact locators recovered; independent contemporary evidence supports mechanism | **open — archival cleanup** |
| Recover machine-specific ENIAC Part-II textual operation | Part II p. IV-43 directly supplies a two-flip-flop synchronizing sequence and reliability rationale | **closed for bounded textual sequence** |
| Ground the ENIAC flip-flop circuit mechanism below the name/interface | Burks 1947 pp. 757–759: directly inspected published schematic + stable-state/cross-coupling + trigger/recovery + timing account | **closed for bounded mechanism claims** |
| Inspect original ENIAC PX-1-105 flip-flop drawing | drawing identity/provenance known | **open — archival cleanup / drawing-specific verification, not promotion blocker** |
| Add period primary source for architectural `register` boundary | Whirlwind R-221 (1954), p. 1-1 and §2.231 / p. 2-12 | **closed** |

Case 06 is therefore **`grounded`** for its bounded mechanism/working-retention claims. The uninspected original drawing still constrains any claim that depends specifically on that artifact.

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
| British Association proceedings directly record Eccles and Jordan's 1919 trigger-relay mechanism and period vocabulary | H/P | Transactions of Section G, pp. 271–272 |
| The exact _Electrician_ / _Radio Review_ facsimile has now been visually inspected | X | not established; archival cleanup |
| PX-1-105 is catalogued as an ENIAC `Flip-Flop Circuit` drawing | H/S | Drexel drawing index |
| Part II p. IV-43 directly documents an unsynchronized flip-flop -> synchronizing gate -> synchronized flip-flop -> transmitter/reset sequence | H/P | directly recovered primary report text |
| Burks 1947 directly shows/explains the bounded ENIAC two-stable-state circuit mechanism and timing | H/P | directly inspected pp. 757–759 |
| Burks Fig. 3 is identical to PX-1-105 | X | not established |
| The exact PX-1-105 drawing has now been directly verified | X | not established; archival cleanup remains |
| Case 06 is grounded for its bounded mechanism/working-retention claims | H/P + E | independent primary source corpus + exact mechanism locations + explicit limits |

---

## Next bounded step

Do **not** keep PX-1-105 as a generic blocker now that Burks 1947 directly grounds the period ENIAC circuit mechanism. Return to the original drawing only for a drawing-specific question or archival cleanup.

The next high-value bridge is a bounded **SRAM / static semiconductor cell** case. It should test whether the powered-quiescent distinction survives the substrate transition while keeping state element, array organization, architectural register role, and later cache semantics separate. Broad semiconductor-memory history belongs primarily in `computing-archaeology` and should be linked/reused rather than rewritten here.
