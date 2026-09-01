# Case 06 grounding: Burks 1947 ENIAC flip-flop circuit

## Status

- **Case:** [`cases/06-flip-flop-powered-working-retention.md`](../cases/06-flip-flop-powered-working-retention.md)
- **Purpose:** close the remaining mechanism-level grounding gap for the ENIAC side of Case 06 without pretending that a published simplified schematic is identical to the still-uninspected original PX-1-105 production drawing.
- **Result:** Arthur W. Burks's 1947 primary paper supplies a directly inspected, period-published ENIAC flip-flop schematic together with explicit descriptions of steady-state stability, triggering/recovery dynamics, component choices, and machine timing margins. In combination with the 1946 ENIAC report, the Eccles–Jordan patent and 1919 proceedings record, and the Whirlwind register witness, this is sufficient to promote Case 06 from `first-pass` to **`grounded`** for the bounded claims made in the case.
- **Remaining archival cleanup:** direct visual inspection of PX-1-105 and the exact 1919 _Electrician_ / _Radio Review_ facsimiles. These remain useful for drawing/page-specific claims but are no longer sole mechanism blockers.
- **Related-repository check:** a fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for PX-1-105 / ENIAC / Eccles–Jordan / flip-flop / register material found no dedicated treatment to reuse. A broad electronic-memory history still belongs there rather than here.

Claim labels below follow repository convention:

- `H/P` — historical record / primary contemporary source;
- `H/S` — source-control or archival evidence;
- `E` — engineering reconstruction;
- `A` — functional analogy;
- `X` — rejected / not established.

---

## 1. Primary-source identity

### H/P — Burks published a machine-specific circuit account in 1947

Arthur W. Burks, who had worked on the ENIAC project at the Moore School, published **“Electronic Computing Circuits of the ENIAC”** in the _Proceedings of the Institute of Radio Engineers_, vol. 35, no. 8, August 1947, pp. 756–767. The inspected Computer History Museum scan is a period reprint from that issue.

The article is particularly valuable for this repository because it does not merely say that ENIAC contained flip-flops. It explicitly explains the circuit's stable states and its transition/recovery design and prints a simplified ENIAC circuit schematic.

**Primary source:** Arthur W. Burks, “Electronic Computing Circuits of the ENIAC,” _Proceedings of the I.R.E._ 35(8), August 1947, pp. 756–767. Computer History Museum scan: <https://archive.computerhistory.org/resources/text/Knuth_Don_X4100/PDF_index/k-8-pdf/k-8-r5367-1-ENIAC-circuits.pdf>.

---

## 2. Directly inspected mechanism evidence

### H/P — p. 757 classifies the flip-flop as a remembering circuit

On p. 757 Burks introduces the general types of computing circuits used in ENIAC and says that the first general circuit type is one capable of **remembering**. He states that both digital and programmatic information must be stored and identifies the Eccles–Jordan trigger circuit, or flip-flop, as the first of ENIAC's remembering-circuit types.

This is useful historical vocabulary: the retention interpretation is not being imposed solely by a modern analyst. Burks himself places the flip-flop inside an explicit period discussion of remembering and storing information.

### H/P — p. 758 separates steady-state stability from triggering dynamics

Section IV, “Flip-Flop and Counter Design,” says that the flip-flop circuit used in ENIAC is shown in **Fig. 3, tubes 1, 2, 3, and 4**. The printed figure is titled **“Accumulator program control circuit (simplified).”**

Burks then separates two design problems:

1. **steady-state stability**, depending on the direct-current connections;
2. **flipping or triggering action**, depending on the alternating-current connections as well.

For the first problem he states that a flip-flop has **two stable states** because direct-current connections run from the plate of each tube to the grid of the opposite tube. In his explanation, the conducting tube biases the nonconducting tube negatively and the nonconducting tube biases the conducting tube positively. He then discusses resistor ratios, tube variation, plate resistance, and power-supply regulation as design variables that determine whether those two stable conditions remain reliable.

This is the missing circuit-level primary anchor for the bounded retention mechanism. It directly supports a regenerative, powered bistable state without requiring us to infer the mechanism from the later word `flip-flop` alone.

### H/P — p. 758 also treats transition and recovery as a separate dynamic design problem

Burks describes the dynamic design as a compromise between rapid flipping and the circuit's recovery so that it will be ready for a later resetting operation. Increasing the relevant resistance/capacitance can speed one aspect of the triggering path while delaying return to the quiescent condition needed for the next operation.

The important retention lesson is therefore not just “feedback holds a bit.” The period source distinguishes:

```text
state-holding stability
    !=
transition / trigger dynamics
    !=
recovery-to-ready timing
```

Those are different engineering obligations even inside one short-lived retained-state element.

### H/P — p. 759 gives explicit microsecond-scale timing margins

Burks reports that the actual value selected for C1 and C2 was **25 micromicrofarads**. He then states that the Fig. 3 flip-flop can be set in about **one microsecond** and is ready to reset in about **four microseconds**. In ENIAC operation it has at least **2.5 microseconds** in which to be set and is **never reset sooner than ten microseconds after being set**.

These figures are historically useful because they show that extremely short working retention still has a nontrivial engineering time structure. The state need not last seconds, hours, or years for the distinction between “remained long enough” and “failed to remain or recover in time” to matter to machine operation.

---

## 3. Engineering reconstruction

### E — powered quiescent retention is supported more precisely

The earlier Case 06 phrase `powered quiescent working retention` can now be stated more carefully. The stable state is produced by the direct-current cross-coupled relation of the valves under operating power. The primary evidence does **not** describe a periodic refresh deadline analogous to DRAM or recirculation analogous to a delay line merely to keep the selected stable state present.

So the safe bounded comparison remains:

> **continuous enabling power is not the same operation as periodic reconstruction of the retained state.**

That is not a claim that the circuit is maintenance-free. Tube condition, bias, power regulation, component tolerances, and timing all matter.

### E — holding and changing state should be separate comparison axes

Burks's own two-part design discussion supplies a strong counterexample to treating “retention mechanism” as a single undifferentiated property. A later SRAM/cache bridge should therefore record separately:

- what makes a state stable while no intentional transition occurs;
- what operation changes the state;
- how long the circuit requires to settle/recover before another transition;
- what power and circuit conditions are prerequisites for all of the above.

### E — short retention has engineering margins, not an arbitrary duration threshold

The explicit 1 / 4 / 2.5 / 10 microsecond timing relations make the repository's earlier “no justified minimum duration” finding less abstract. The correct test is not whether a state survives for some arbitrary number of milliseconds. It is whether a past event/state remains admissibly effective across the interval required by a later operation, including the mechanism's own settling and recovery constraints.

---

## 4. Strict artifact boundary

### H/P — the Burks figure was directly inspected

The 1947 paper's Fig. 3 and accompanying pp. 758–759 mechanism/timing discussion were directly inspected in the page-preserving CHM scan.

### H/S + X — PX-1-105 itself is still not directly inspected here

Brian Stuart's Drexel ENIAC drawing index identifies **PX-1-105 — `Flip-Flop Circuit`**, with most drawing images described as processed from ENIAC patent-trial microfilm and some replacements from Smithsonian material:

<https://www.cs.drexel.edu/~bls96/eniac/drawings/>.

The exact PX-1-105 image was not reliably rendered in this pass. Therefore this note does **not** claim:

- that Burks Fig. 3 is a facsimile of PX-1-105;
- drawing-specific dimensions, drafting annotations, revisions, or component placement;
- any topology detail visible only on PX-1-105 and absent from the inspected published paper.

The evidence relation is:

```text
period-published simplified ENIAC schematic + explicit mechanism text
    = sufficient for the bounded mechanism claims

period-published simplified schematic
    != original production/patent-trial drawing facsimile
```

This is a claim-specific maturity rule, not permission to stop caring about original drawings when a later question depends on drawing-specific detail.

---

## 5. Why Case 06 can now be `grounded`

The repository's `grounded` gate asks for strong primary evidence, precise locations, historical vocabulary, mechanism/failure modes, limits, and a related-repository duplication check. Case 06 now has independent coverage of those requirements:

- Eccles–Jordan GB148582A plus the 1919 British Association proceedings anchor the regenerative trigger principle and contemporary vocabulary;
- the 1946 _Report on the ENIAC_ anchors machine-specific `flip-flop`, set/reset/clear, `stores` / `remembers`, initialization, static output, carry, and staged event/timing use;
- Burks 1947 pp. 757–759 directly anchor ENIAC remembering-circuit vocabulary, a visible simplified circuit, two stable states, DC cross-coupling, trigger/recovery separation, tolerances, and timing margins;
- Whirlwind R-221 (1954) anchors the period architectural `register` boundary without equating every flip-flop with a register;
- modern synchronization and modern register-file language remain explicitly labeled as analogy rather than historical vocabulary;
- fresh related-repository search found no dedicated treatment to reuse.

Accordingly, **Case 06 is promoted to `grounded` for this bounded 1918–1946 mechanism/working-retention question plus the explicitly bounded 1954 register witness.**

The promotion does not make every ENIAC drawing claim grounded and does not turn this case into a general history of latches, SRAM, registers, or sequential logic.

---

## 6. Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Burks 1947 identifies the Eccles–Jordan trigger / flip-flop as an ENIAC remembering-circuit type | H/P | directly inspected p. 757 |
| Burks Fig. 3 is a period-published simplified ENIAC accumulator program-control circuit containing the discussed flip-flop | H/P | directly inspected p. 758 |
| Burks separates steady-state stability from triggering/action and recovery | H/P | directly inspected p. 758 |
| Burks explains the two stable states through direct-current plate-to-opposite-grid cross-coupling | H/P | directly inspected p. 758 |
| The inspected paper gives about 1 µs set, about 4 µs ready-to-reset, at least 2.5 µs set allowance, and no reset sooner than 10 µs after set | H/P | directly inspected p. 759 |
| Continuous power is equivalent to DRAM-style periodic refresh | X | not supported; different retention operation |
| State-holding stability and transition/recovery timing are the same engineering property | X | directly contradicted by Burks's design decomposition |
| Burks Fig. 3 is identical to PX-1-105 | X | not established |
| PX-1-105 has now been visually inspected | X | not established; archival cleanup remains |
| Case 06's bounded mechanism claims can be promoted without PX drawing-specific claims | H/P + E | supported by independent primary mechanism/schematic corpus plus explicit artifact boundary |

---

## 7. Cross-case consequences and next bounded step

This grounding pass supports three additions to the cross-case ledger:

1. **state-holding feedback ≠ transition/recovery path** — Burks explicitly separates the DC stability problem from triggering and readiness for reset;
2. **short retention still has internal timing structure** — the ENIAC flip-flop's microsecond-scale set/recovery/use margins are operational constraints, not a trivial interval;
3. **published primary schematic ≠ original production drawing** — a directly inspected period-published circuit can ground mechanism-level claims while an uninspected original drawing remains necessary for drawing-specific claims.

The next technical bridge should now move forward rather than continue chasing PX-1-105 as a generic blocker. A bounded **SRAM / static semiconductor cell** case is the highest-value next step: it can test whether the powered-quiescent distinction survives the transition from thermionic feedback to semiconductor static memory, while `register` organization and later `cache` semantics remain separate axes. Broad semiconductor-memory history should be reused from or contributed to `computing-archaeology` instead of duplicated here.