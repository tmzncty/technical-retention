# Case 06 source deepening: ENIAC timing-retention in the synchronizing path

## Status

- **Case:** [`cases/06-flip-flop-powered-working-retention.md`](../cases/06-flip-flop-powered-working-retention.md)
- **Purpose:** deepen the ENIAC side of Case 06 with directly recoverable Part-II primary text rather than infer circuit behavior from a drawing locator alone.
- **Result:** Part II, p. IV-43 directly documents a two-flip-flop synchronizing path in which an incoming switch pulse establishes a condition that survives until later central-programming pulses act on it. This closes a **textual-operation** gap for one ENIAC circuit sequence, but it does **not** close the separate visual-schematic gap for PX-1-105. The Eccles–Jordan 1919 page/reprint also remains uninspected. **Case 06 therefore remains `first-pass`.**
- **Related-repository check:** a fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for Eccles–Jordan / ENIAC / flip-flop / register material found no dedicated treatment to reuse.

Claim labels used below:

- `H/P` — period historical record / primary source;
- `H/S` — archival or institutional source-control evidence;
- `E` — engineering reconstruction;
- `A` — functional analogy;
- `X` — rejected or not established.

---

## 1. Primary-source identity and scope

### H/P — Part II is the circuit-detail volume of the 1 June 1946 ENIAC report

The U.S. Army / University of Pennsylvania report landing page identifies **_A Report on the ENIAC_**, dated **1 June 1946**, as work under Contract W-670-ORD-4926 between the U.S. Army Ordnance Department and the University of Pennsylvania Moore School of Electrical Engineering. Its preface separates the report into five bound parts and states that **Part II, Technical Description of the ENIAC** is intended for readers who require a detailed understanding of the circuits.

This matters for evidence maturity: the sequence below is not a later textbook reconstruction but a machine-specific primary technical description.

**Primary report portal:** U.S. Army / Moore School, _A Report on the ENIAC_, 1 June 1946: <https://ftp.arl.army.mil/~mike/comphist/46eniac-report/>.

**Part-II scan used for the page anchor:** <https://www.cs.drexel.edu/~bls96/eniac/reports/prog2.pdf>.

**Institutional archival corroboration:** University of Pennsylvania Archives, Moore School Office of the Director Records, listing `ENIAC Technical Report II`, 1 June 1946: <https://archives.upenn.edu/collections/finding-aid/upd8_4/>.

---

## 2. H/P — p. IV-43 documents staged retention of an unsynchronized switch event

Part II p. **IV-43** describes a path beginning with a pulse received from a switch. The report states that the received pulse sets an **`unsynchronized flip-flop`**. That flip-flop operates a **`synchronizing gate`**, through which the next **central programming pulse** can set a **`synchronized flip-flop`**. The second flip-flop then operates a **`transmitter gate`**; a later central program pulse passes to the transmitter and resets both flip-flops.

The sequence can be represented, without adding modern vocabulary, as:

```text
switch pulse
    -> unsynchronized flip-flop set
    -> synchronizing gate enabled
    -> next central programming pulse
    -> synchronized flip-flop set
    -> transmitter gate enabled
    -> central program pulse transmitted
    -> both flip-flops reset
```

The report also explains why the second stage is present. The switch pulse is not synchronized with the ENIAC. If the first gate begins to conduct while a central program pulse is already present, the resulting pulse can be reduced in magnitude and reliable operation cannot be expected. The synchronized flip-flop forces the transmitter gate into a fully established on/off condition before the next central program pulse is used for output.

This is stronger evidence than the drawing-index locator alone because the period report itself gives the **temporal function** of the two retained states.

**Primary anchor:** _A Report on the ENIAC_, Part II, p. IV-43, paragraph beginning `When the pulse is received the unsynchronized flip-flop is set`, scan at <https://www.cs.drexel.edu/~bls96/eniac/reports/prog2.pdf>.

---

## 3. Engineering reconstruction — the retained target can be a pending event condition

### E — the first flip-flop holds more than a numeric value

For the bounded sequence on p. IV-43, the retained target is usefully reconstructed as a **pending control/event condition**:

```text
t0: an external pulse occurs
    -> FF1 records that the event has occurred

intervening time / machine pulse boundary
    -> FF1 remains in the condition needed to enable the synchronizing gate

t1: a central programming pulse acts on that retained condition
    -> FF2 enters the synchronized condition

later machine pulse
    -> transmitter action occurs
    -> reset ends the retained condition
```

If the first condition did not survive from the switch event to the relevant central-programming pulse, the later operation would differ. That satisfies the repository's bounded retention test without requiring a long duration or a storage-style `read` transaction.

This adds a distinct role alongside the numerical and carry examples already documented in Case 06:

- a flip-flop can retain a digit-related or carry-related condition;
- a flip-flop can also retain that **an event has occurred and awaits a machine-timed consequence**.

### E — timing qualification can itself depend on staged retained state

The second flip-flop is not described merely as another place to hold the same value. In the report's own operational explanation, it makes the transmitter gate reliably fully on or fully off when a central program pulse arrives.

The retention-specific lesson is therefore:

> **timing alignment can require staged retention: one retained state preserves an event across an uncertain arrival relation, and another retained state establishes a machine-timed condition for later use.**

This is not a universal definition of synchronization, and it does not imply that all reliability problems reduce to retained-state staging.

---

## 4. Historical-language boundary

### H/P — use the ENIAC report's own terms

The safe period vocabulary here is:

- `unsynchronized flip-flop`;
- `synchronizing gate`;
- `synchronized flip-flop`;
- `central programming pulse` / `central program pulse`;
- `transmitter gate`;
- reliable operation / output pulse synchronized with the rest of the ENIAC.

### A — modern synchronizer / clock-domain language is analogy only

A modern engineer may notice a functional resemblance to later event-latching or synchronization problems. That can be useful as a **functional analogy**, but Case 06 must not rewrite the 1946 report as if its authors were using later `clock-domain crossing`, setup/hold, or metastability theory.

The primary source gives a concrete period problem: an incoming switch pulse can be out of phase with ENIAC's central programming pulse, producing a weak gate output unless the event is staged through retained flip-flop state. That is enough for the retention analysis.

---

## 5. What remains unverified

### H/S — PX-1-105 remains a locator, not a visually inspected schematic

Brian Stuart's Drexel ENIAC drawing index identifies:

- **PX-1-105 — `Flip-Flop Circuit`**;
- PX-1-106 — `Gate Tube Circuits`;
- PX-1-109 — `Binary Ring Circuit`.

The index explains that most drawing images were processed from ENIAC patent-trial microfilm, with some higher-quality Smithsonian replacements.

**Drawing index:** <https://www.cs.drexel.edu/~bls96/eniac/drawings/>.

This pass did not obtain a reliable rendered view of PX-1-105 itself. Therefore the repository still does **not** promote claims about its resistor values, tube-by-tube topology, exact bias points, or drawing-specific timing paths.

The source-control distinction is now:

```text
Part-II textual operation directly inspected
    !=
PX-1-105 schematic visually inspected
```

### H/S — Eccles–Jordan 1919 direct-page inspection remains open

The exact _Electrician_ p. 298 and _Radio Review_ pp. 143–146 locators remain useful, but this pass still did not obtain a directly inspectable authorial page image. Same-year reporting is consistent with the existing patent-based reconstruction, but it does not substitute for the requested direct page/reprint inspection.

---

## 6. Revised Case-06 gap ledger

| Gap | Status after this pass | Evidence boundary |
| --- | --- | --- |
| Period primary `register` vocabulary | **closed** | Whirlwind R-221, 1954 |
| ENIAC Part-II machine-specific textual operation | **partly closed** | p. IV-43 directly supplies a two-flip-flop timing sequence and its reliability rationale |
| ENIAC PX-1-105 visual schematic inspection | **open** | drawing identity known; image/topology not directly verified |
| Eccles–Jordan 1919 authorial page/reprint inspection | **open** | exact locators known; direct page image still required |

This is enough to deepen Case 06, but not enough to promote it to `grounded` under the repository's own quality gate.

---

## 7. Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| _A Report on the ENIAC_ is dated 1 June 1946 and Part II is the circuit-detail technical description | H/P + H/S | Army/Moore School report portal + UPenn archival record |
| Part II p. IV-43 says an incoming switch pulse sets an `unsynchronized flip-flop` | H/P | directly recoverable primary text |
| FF1 enables a synchronizing gate through which a later central programming pulse sets a `synchronized flip-flop` | H/P | directly recoverable primary text |
| FF2 controls a transmitter gate and the later output/reset sequence | H/P | directly recoverable primary text |
| The second stage is justified because an unsynchronized arrival can otherwise produce a reduced-magnitude pulse and unreliable operation | H/P | directly recoverable primary text |
| The retained target can be reconstructed as a pending event/control condition rather than only a number | E | bounded reconstruction from the documented temporal sequence |
| This is historically a modern `clock-domain crossing synchronizer` | X/A only | modern analogy may be useful, but the 1946 source does not establish that later concept/vocabulary |
| PX-1-105 topology/component values are directly verified | X | schematic image still not inspected |
| Case 06 is ready for `grounded` promotion | X | two direct-inspection gaps remain |

---

## Next bounded step

Do not open SRAM/cache merely because the ENIAC textual mechanism is now stronger. The remaining highest-value work is narrower:

1. directly inspect the Eccles–Jordan 1919 authorial page/reprint;
2. directly render and inspect PX-1-105 (and only the immediately relevant ENIAC Part-II drawing context), recording exact circuit/topology anchors.

If those inspections confirm the present mechanism boundaries, reconsider Case 06 for `grounded`. If they conflict, correct the case rather than promote it.