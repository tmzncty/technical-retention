# Case 07 source deepening — Fairchild static-MOS cell regime, 1968–1970

## Purpose

This note deepens [`cases/07-static-mos-ram-powered-quiescence.md`](../cases/07-static-mos-ram-powered-quiescence.md) without expanding it into a general SRAM history.

The bounded question is:

> What period-primary evidence shows that an early MOS memory cell could be a cross-coupled, bistable storage element embedded in an array, while still having distinct standby/address/read/write conditions and engineering margins?

It also records one negative control: a nearby Intel/Vadasz MOS-memory patent is explicitly dynamic and therefore must **not** be used as evidence for the Intel 1101/2102 static bit-cell topology.

Case 07 remains `first-pass`. This note strengthens the generic period mechanism and failure/margin evidence; it does **not** close the still-open Intel-product-specific bit-cell schematic gap.

---

## Source 1 — Fairchild US3530443A, filed 27 November 1968, published 22 September 1970

### Bibliographic record — H/P

- Harold S. Crafts, Wendell B. Sander, James B. Angell, **“MOS gated resistor memory cell,”** US Patent 3,530,443.
- Original assignee: Fairchild Camera and Instrument Corporation.
- Filed: 27 November 1968.
- Published / granted: 22 September 1970.
- Primary-text access: <https://patents.google.com/patent/US3530443A/en>.

The patent is close enough in date to the 1969–1971 static-MOS bridge to serve as period evidence, but it is a **Fairchild design**, not an Intel 1101/1101A/2102 product disclosure.

### Flip-flop storage is period vocabulary — H/P

The patent describes the then-typical semiconductor memory cell as a flip-flop plus gating elements. For MOS implementation it describes the flip-flop as two MOS transistors with cross-coupled gates, with the cross-coupling identified as the stability relation. The invention then reduces the separate-component burden by making two additional MOS devices serve as voltage-variable loads and gating elements.

Its summary describes a complete four-active-device MOS memory cell in which the two cross-coupled devices store the logic condition and the other two devices also serve load/gating functions.

This is a stronger period mechanism witness than a later textbook statement that early SRAM was “flip-flop based”: the flip-flop / cross-coupling language is in the 1968-filed technical disclosure itself.

### Stable holding and array service are separate questions — H/P

The patent does not stop at a cell diagram. It explicitly treats the cell as operating in an array with word and bit lines and separates four package/array-level conditions:

1. standby;
2. address;
3. read;
4. write.

The same basic circuit is then discussed under multiple operating regimes, including `static storage` and `dynamic storage`.

For the static-storage mode, the patent gives a powered standby bias, an address change on the selected word line, differential-current sensing for read, and a bit-line bias change sufficient to switch the retained state for write.

### E — mechanism reconstruction

For the bounded static mode the source supports this reconstruction:

```text
cross-coupled MOS state relation
        +
powered standby bias
        ↓
quiescent logical condition
        ↓
word-line address operation
        ↓
differential read or state-switching write
```

The retained target is not simply “charge somewhere.” It is which cross-coupled logical condition remains stable under the stated powered bias relation.

This is consistent with Case 07's existing comparison to powered thermionic bistability while remaining a distinct semiconductor implementation.

---

## A particularly useful boundary: `static` is a regime, not a sufficient topology description

### H/P

The Fairchild patent describes the same basic cell family as capable of several operating modes. Its text explicitly contrasts `static storage` with `dynamic storage` rather than presenting the words as names of two immutable transistor-count categories.

In the dynamic mode, the document states that word lines must be addressed periodically to prevent loss of information and describes periodic restoring pulses because the dynamic storage interval cannot exceed the natural storage time.

### E

This yields a useful discipline for the repository:

> **A cross-coupled MOS topology does not, by its name alone, settle the complete retention regime. Biasing, array operation, and maintenance protocol matter.**

For the bounded Intel 1101A/2102 claims, the manufacturer documentation is still the authority for “fully DC stable,” “no clocks,” and “no refreshing.” The Fairchild patent is a period mechanism witness showing why static/dynamic behavior must be source-controlled rather than inferred from a modern schematic stereotype.

### X — prohibited inference

Do **not** infer:

- `US3530443A = Intel 1101 cell`;
- `US3530443A = Intel 2102 cell`;
- every early static MOS cell used the same four-device circuit;
- every cross-coupled MOS cell was necessarily operated statically;
- “static” by itself means no supply power, no access timing, or no peripheral circuitry.

---

## Engineering margins: bistability is not an ideal Boolean abstraction

### H/P

The patent compares alternative array/operating arrangements in terms of threshold sensitivity, current transients, write speed, power dissipation, and noise margin. One discussed dynamic arrangement has roughly one-volt noise immunity, while an alternative has much smaller immunity; the text also notes a threshold-voltage-sensitive half-select mode as a yield problem.

The exact numerical values belong to the disclosed Fairchild circuits and modes only. They must not be generalized to Intel 1101A, 2102, 5101, or to later SRAM.

### E

The important cross-case result is narrower:

> **bistability ≠ unlimited state-holding margin.**

A cell can have two intended logical conditions while its ability to remain, be selected, be sensed, and be rewritten correctly depends on finite voltage/noise/process margins and on the array bias conditions around it.

This deepens Case 07 finding 101 (`cell bistability ≠ array-memory semantics`) without replacing it. The new point is that the retained distinction itself is **margin-bounded**, not an abstract Boolean fact independent of the electrical environment.

---

## Source 2 negative control — Intel US3706079A is dynamic, not static-cell evidence

### Bibliographic record — H/P

- Leslie L. Vadasz and Joel A. Karp, **“Three-line cell for random-access integrated circuit memory,”** US Patent 3,706,079.
- Assignee: Intel Corporation.
- Priority / filing: 16 September 1971.
- Published: 12 December 1972.
- Primary-text access: <https://patents.google.com/patent/US3706079A/en>.

### H/P

This Intel patent explicitly describes a **three-line dynamic storage cell**. Its retained electrical charge resides on parasitic capacitance and the document states that the charge is transient and must be refreshed periodically.

### Methodological use

The patent is useful here chiefly as a control against source-by-proximity reasoning:

> the fact that a document is an early Intel MOS-memory patent by Vadasz does not make it evidence for the Intel 1101/2102 static bit-cell topology.

It belongs with dynamic-memory history unless used as a deliberately labeled contrast.

This matters because the open Case 07 promotion gap is **cell-specific evidence for an Intel static product**, not merely “find an Intel patent from the same years.”

---

## Vadasz–Chua–Grove 1971 page status

Search-indexed text for the May 1971 *IEEE Spectrum* issue continues to support the already-recorded page locations:

- p. 43: MOS flip-flops for storage and discussion of a static MOS memory cell;
- p. 47: fully decoded static MOS memory and the Intel 1101 system-expansion example.

However, this run did **not** obtain a reliably renderable facsimile of those exact pages. Under the repository's source rule, indexed page text is not the same as direct visual inspection of the page image.

Therefore the roadmap item “directly inspect Vadasz 1971 pp. 43/47” remains open.

---

## What this changes in Case 07

### Newly strengthened

1. **Period cross-coupled MOS mechanism:** directly inspectable patent text from a 1968-filed Fairchild design describes MOS flip-flop storage and cross-coupled stability.
2. **Static mode as an operating regime:** period primary text explicitly separates static storage, standby/address/read/write conditions, and a contrasting dynamic mode.
3. **Margin-bound retention:** the period disclosure ties usable operation to threshold, noise, power/current, and array-bias tradeoffs rather than an idealized binary state alone.
4. **Negative source control:** the 1971-filed Intel/Vadasz/Karp patent is explicitly dynamic and cannot close the Intel-static-cell gap.

### Still open before promotion

1. direct visual inspection of Vadasz–Chua–Grove 1971 pp. 43 and 47;
2. a cell-specific primary schematic/design source for Intel 1101/1101A or 2102-class **static** memory;
3. device-specific hold/failure/noise-margin evidence for one of the bounded Intel static products, rather than transferring Fairchild margins to Intel;
4. later cache semantics remain deferred.

---

## Claim ledger

| Claim | Type | Status |
| --- | --- | --- |
| Fairchild US3530443A was filed in 1968 and published in 1970 | H/P | supported |
| the patent describes MOS flip-flop storage with cross-coupled devices | H/P | supported |
| the disclosed cell family includes a static-storage operating mode | H/P | supported |
| static mode is discussed with separate standby/address/read/write conditions in an array | H/P | supported |
| the same disclosed family also has dynamic operation requiring periodic restoration | H/P | supported |
| finite threshold/noise/power margins matter to usable state retention and access | H/P + E | supported, circuit-specific values remain bounded |
| Fairchild US3530443A is the Intel 1101 or 2102 bit cell | X | rejected / unsupported |
| Intel US3706079A closes the static-cell topology gap | X | rejected; the patent is explicitly dynamic |
| Case 07 is ready to promote to `grounded` | X | not yet |

---

## Sources

1. Harold S. Crafts, Wendell B. Sander, James B. Angell, **“MOS gated resistor memory cell,”** US Patent 3,530,443, filed 27 November 1968, published 22 September 1970. <https://patents.google.com/patent/US3530443A/en>
2. Leslie L. Vadasz, Joel A. Karp, **“Three-line cell for random-access integrated circuit memory,”** US Patent 3,706,079, filed 16 September 1971, published 12 December 1972. <https://patents.google.com/patent/US3706079A/en>
3. L. L. Vadasz, H. T. Chua, A. S. Grove, **“Semiconductor random-access memories,”** *IEEE Spectrum* 8(5), May 1971, pp. 40–48. Exact p. 43 / p. 47 facsimile inspection remains open in this repository.
