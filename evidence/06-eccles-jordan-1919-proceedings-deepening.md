# Case 06 source deepening: Eccles–Jordan in the 1919 British Association record

## Status

- **Case:** [`cases/06-flip-flop-powered-working-retention.md`](../cases/06-flip-flop-powered-working-retention.md)
- **Purpose:** deepen the Eccles–Jordan side of Case 06 with directly recoverable contemporary authorial material rather than relying only on the 1918-filed patent plus later descriptions.
- **Result:** the published proceedings of the British Association's Bournemouth meeting record Eccles and Jordan's paper **“A Trigger Relay utilising Three Electrode Thermionic Vacuum Tubes”** on pp. 271–272 and directly describe the resistance-coupled cascade, back coupling, trigger action, and the absence of a restoring influence after an electrical stimulus. The proceedings themselves point to _The Electrician_, 19 September 1919, p. 298 and _Radio Review_, vol. I, p. 143.
- **Maturity consequence:** this closes the **authorial/contemporary mechanism-text** gap that previously rested mainly on the patent. It does **not** mean the exact _Electrician_ p. 298 or _Radio Review_ pp. 143–146 facsimile has been visually inspected. That page-image task is now narrow archival cleanup rather than the only primary support for the 1919 mechanism.
- **Case status:** **still `first-pass`**. The remaining promotion blocker is direct visual inspection of ENIAC PX-1-105 / immediately relevant original schematic material; exact 1919 periodical facsimile inspection remains desirable archival cleanup.
- **Related-repository check:** a fresh search of [`tmzncty/computing-archaeology`](https://github.com/tmzncty/computing-archaeology) for Eccles–Jordan / ENIAC / flip-flop / register material again found no dedicated treatment to reuse.

Claim labels used below:

- `H/P` — historical record / primary or contemporary source;
- `H/S` — archival / scholarly source-control evidence;
- `E` — engineering reconstruction;
- `A` — functional analogy;
- `X` — rejected or not established.

---

## 1. Primary-source identity

### H/P — the British Association record is a contemporary report of the 1919 meeting

The digitized volume is titled _Report of the Eighty-Seventh Meeting of the British Association for the Advancement of Science: Bournemouth: 1919, September 9–13_. The title page records the Bournemouth meeting and the London publication by John Murray in 1920.

In the Transactions of Section G, the Friday, 12 September session lists Eccles and Jordan's contribution under the title:

> `A Trigger Relay utilising Three Electrode Thermionic Vacuum Tubes.`

The printed record identifies the authors as Professor W. H. Eccles and F. W. Jordan. Its footnote points readers to:

- _The Electrician_, 19 September 1919, p. 298;
- _Radio Review_, vol. I, p. 143.

This is therefore not a later textbook recollection. It is a contemporary proceedings record of the authors' 1919 presentation, published immediately after the meeting.

**Primary source:** British Association for the Advancement of Science, _Report of the Eighty-Seventh Meeting ... Bournemouth: 1919_, Transactions of Section G, printed pp. 271–272. Internet Archive item: <https://archive.org/details/reportofbritisha20adva>. Direct OCR/text layer: <https://archive.org/stream/reportofbritisha20adva/reportofbritisha20adva_djvu.txt>.

---

## 2. H/P — the proceedings directly describe regenerative trigger action

The proceedings characterize the circuit as a **cascade amplifier with resistance coupling**. They state that an even number of valves is required and that **back coupling from the last to the first produces the required trigger action**.

The reported sequence is explicit enough to recover the mechanism without later `flip-flop` vocabulary:

1. an electrical stimulus makes the first grid more positive;
2. current through the first valve rises;
3. the second grid potential falls;
4. current through the second valve falls;
5. the resulting potential change feeds back to make the first grid still more positive;
6. because there is **no restoring influence**, the first-valve current proceeds toward its limiting value set by the tube and battery.

A retention-specific schematic of the period description is therefore:

```text
external electrical stimulus
    -> first-valve current rises
    -> second-valve current falls
    -> returned potential reinforces first-valve change
    -> no restoring influence
    -> limiting circuit condition
```

This independently confirms the patent-based reconstruction that the key mechanism is regenerative feedback whose resulting condition is not merely the instantaneous duration of the initiating stimulus.

The proceedings do **not** call the mechanism a `bit`, `memory cell`, `register`, or `flip-flop`. Its period vocabulary is `trigger relay`, `cascade amplifier`, `resistance coupling`, `back coupling`, `electric stimulus`, and the absence of a `restoring influence`.

---

## 3. Cross-check against the 1918-filed patent

### H/P — the proceedings and patent support the same bounded mechanism from different source contexts

British Patent GB148582A, filed 21 June 1918 and published 5 August 1920 as **“Improvements in ionic relays,”** describes return coupling / `retroaction` between thermionic valves and explains how a stimulus can drive the valves toward opposite limiting current conditions. It also describes restoration of the initial condition by interrupting the interaction.

The British Association record matters because it is a separate contemporary authorial presentation with its own period terminology and a concise causal description of the trigger action. The central Case-06 mechanism therefore no longer depends on reading the patent alone.

**Patent:** <https://patents.google.com/patent/GB148582A/en>.

### H/P + source-control limit — a near-contemporary reprint is consistent, but was not used as a visual facsimile anchor

A January 1920 _Radio Amateur News_ reproduction indexed on the public web prints the Eccles–Jordan article under the same title and includes the stronger wording that the triggered electrical equilibrium remains in the new condition until reset, followed by a description of how to restore the initial condition. This is fully consistent with the patent and the British Association record.

However, the available retrieval path exposed machine-extracted text while the PDF itself did not render reliably in this research pass. It is therefore a useful contemporary cross-check, **not** a substitute for claiming visual inspection of the requested _Electrician_ or _Radio Review_ facsimile.

Discovery copy: <https://electronicsandbooks.com/edt/manual/Magazine/R/Radio%20News%20US/20s/Radio-News-1920-01-R%20%5B65%5D.pdf>.

---

## 4. What this changes in Case 06

### E — regeneration, not mere electrical inertia, is the retention mechanism

The contemporary proceedings make the causal loop visible. The state continuation is not adequately described as “the voltage simply lingers.” The key relation is mutually reinforcing valve-state change through back coupling until a limiting condition is reached.

That supports the Case-06 local phrase **powered regenerative/bistable working retention** more strongly than a generic statement that the circuit “has two states.”

### E — `no restoring influence` is not the same claim as `no maintenance condition`

The period phrase concerns the circuit's immediate restoring tendency after the trigger. It must not be inflated into a claim that the circuit is independent of operating power, bias, functioning valves, or the surrounding electrical conditions.

The repository should therefore preserve:

```text
no restoring influence after the trigger
    !=
no enabling conditions for retention

powered regenerative stability
    !=
periodic refresh / rewrite
```

### A/X — later computer-memory language remains retrospective

The modern engineering literature can legitimately compare the Eccles–Jordan trigger relay to later bistable state elements. But the primary 1919 source still does not license the historical sentence “Eccles and Jordan were designing a computer register.”

The source actually strengthens the anti-anachronism boundary because its own vocabulary is now directly available.

---

## 5. Revised evidence-gap ledger

| Gap | Status after this pass | Evidence boundary |
| --- | --- | --- |
| Period primary `register` vocabulary | **closed** | Whirlwind R-221, 1954 |
| ENIAC Part-II machine-specific textual operation | **closed for the bounded p. IV-43 sequence** | direct Part-II text |
| Eccles–Jordan contemporary authorial mechanism text beyond the patent | **closed** | British Association 1919 meeting proceedings, pp. 271–272 |
| Exact _Electrician_ p. 298 / _Radio Review_ pp. 143–146 facsimile inspection | **open, archival cleanup** | exact locators known; proceedings themselves cite them; no visual page claim added |
| ENIAC PX-1-105 visual schematic inspection | **open, promotion blocker** | drawing identity/provenance known; original image/topology still unverified |

This changes the shape of the remaining work. Case 06 no longer has two equally important source gaps. Its 1919 mechanism is independently anchored by the patent and a contemporary authorial proceedings record. The unresolved ENIAC schematic is now the main evidence-maturity blocker.

---

## 6. Claim ledger

| Claim | Label | Evidence status |
| --- | --- | --- |
| Eccles and Jordan presented `A Trigger Relay utilising Three Electrode Thermionic Vacuum Tubes` at the 1919 British Association meeting | H/P | contemporary proceedings, Section G, pp. 271–272 |
| The proceedings cite _The Electrician_ 19 Sep 1919 p. 298 and _Radio Review_ vol. I p. 143 | H/P | printed footnote in the proceedings |
| The proceedings describe a resistance-coupled cascade with back coupling from last valve to first producing trigger action | H/P | directly recovered primary text |
| An external stimulus initiates mutually reinforcing current/potential changes and the text says there is no restoring influence | H/P | directly recovered primary text |
| The bounded retention mechanism is regenerative continuation rather than mere persistence of the input pulse | E | reconstruction from proceedings + GB148582A |
| The 1919 authors described the apparatus as a computer `flip-flop`, `bit`, `memory cell`, or `register` | X | not supported; those are later classifications |
| The exact _Electrician_ / _Radio Review_ page image has now been visually inspected | X | not established in this pass |
| PX-1-105 has now been visually verified | X | still open |
| Case 06 is now `grounded` | X | schematic-level promotion blocker remains |

---

## Next bounded step

Do not reopen generic Eccles–Jordan history and do not open SRAM/cache yet solely because this source gap is stronger. The next highest-value move is now singular:

> **directly render and inspect ENIAC PX-1-105 `Flip-Flop Circuit` and only the immediately relevant drawing context, then compare the observed topology against the already grounded Part-II textual operation.**

The exact _Electrician_ / _Radio Review_ facsimile can still be recovered for archival completeness, but it is no longer the only contemporary authorial support for the 1919 mechanism. If PX-1-105 confirms the current bounded reconstruction, reconsider Case 06 for `grounded`; if it conflicts, repair the case first.