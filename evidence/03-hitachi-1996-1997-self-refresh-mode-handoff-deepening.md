# Case 03 deepening — Hitachi HM5118165L self-refresh mode handoff, 1996–1997

## Scope

This packet deepens one narrow retention question inside Case 03:

> When a DRAM can maintain its payload in a named `Self Refresh` mode, what does the product documentation require at the **boundary between ordinary externally serviced refresh and autonomous self-refresh**?

The object is Hitachi's `HM5118165 Series`, a 16 Mbit EDO DRAM documented in the inspected vendor datasheet as `ADE-203-636D (Z), Rev. 4.0, Nov. 1997`. The revision record states that the initial issue was Rev. 1.0 on 30 September 1996.

This is **not** a general history of self-refresh DRAM and does not attempt to establish first invention, first shipment, or first standardization. It is a product-level retention-contract deepening.

Status: **grounded evidence deepening; no case maturity promotion**.

---

## Why this slice matters

Case 03 already distinguishes:

- payload state from refresh-control state;
- externally generated cadence from on-chip refresh-address coverage;
- CAS-before-RAS refresh from timer-backed self-refresh;
- useful access from the maintenance work required to keep data recoverable.

The Hitachi HM5118165L adds a different boundary:

```text
ordinary refresh regime
    -> self-refresh entry
    -> autonomous retention interval
    -> self-refresh exit
    -> ordinary refresh regime resumes
```

The transition itself is constrained. A device may support self-refresh and still require explicit coverage discipline before and after the autonomous interval.

That gives a retention-specific counterexample to:

```text
self-refresh supported
    = arbitrary safe mode switching
```

---

## Source inspected

### Primary technical source

Hitachi, `HM5118165 Series — 16 M EDO DRAM (1-Mword × 16-bit), 1 k Refresh`, `ADE-203-636D (Z)`, Rev. 4.0, Nov. 1997.

Mirror used for direct page inspection:

<https://www.manuallib.com/download/pdf10/HITACHI-HM5118165-SERIES-16-M-EDO-DRAM-(1-MWORD--TIMES--16-BIT)-1-K-REFRESH.PDF>

Relevant document locations:

- printed p. 1 / PDF p. 1: feature summary;
- printed p. 5 / PDF p. 5: truth table, including `Self refresh cycle (L-version)`;
- printed pp. 11–13 / PDF pp. 11–13: refresh period, self-refresh timing, and notes 28–31;
- printed p. 29 / PDF p. 29: self-refresh waveform;
- printed p. 33 / PDF p. 33: revision record.

The repository should treat the mirror only as a delivery location. The document itself is a Hitachi-originated datasheet.

---

# Historical record

## H1 — The L-version exposes a distinct self-refresh product mode

The feature list names four refresh modes:

- RAS-only refresh;
- CAS-before-RAS refresh;
- Hidden refresh;
- Self refresh, specifically for the `L-version`.

The same page also advertises `Battery backup operation (L-version)`.

The truth table gives self-refresh its own input condition rather than folding it into ordinary CBR refresh.

This establishes a named product-level interface distinction:

```text
RAS-only refresh
    !=
CAS-before-RAS refresh
    !=
Hidden refresh
    !=
Self refresh
```

It does **not** establish that all four modes use unrelated internal circuits.

---

## H2 — The L-version has a longer specified refresh period

The feature summary gives:

```text
1024 refresh cycles / 16 ms
```

for the ordinary device family and:

```text
1024 refresh cycles / 128 ms
```

for the L-version.

The AC table repeats the distinction as `tREF = 16 ms` and `tREF = 128 ms (L-version)`.

This is a product contract about the allowed refresh-coverage period. It is not a direct measurement of the weakest-cell physical retention time.

Therefore:

```text
specified refresh period
    !=
measured intrinsic cell-retention distribution
```

---

## H3 — Self-refresh is a powered maintenance mode, not nonvolatile retention

The datasheet specifies self-refresh current for the L-version (`ICC11`, maximum 300 µA under the listed CMOS-interface conditions).

The device therefore still requires powered operation during self-refresh.

The correct historical statement is:

```text
low-power autonomous maintenance
    !=
unpowered data retention
```

The feature phrase `battery backup operation` should not be rewritten as `nonvolatile memory`.

---

## H4 — Entry to self-refresh includes a defined transition interval

Note 28 states that a `tRASS` interval from 10 µs through 100 µs must not be used; during that interval the device is in a transition state from normal operation to self-refresh. For a sufficiently long RAS pulse (`tRASS >= 100 µs`), the self-refresh timing rules apply.

This establishes a product-level state-transition boundary:

```text
ordinary operation
    -> transition state
    -> self-refresh state
```

The existence of the final state does not erase the protocol needed to enter it.

---

## H5 — Distributed CBR users have an explicit before/after handoff deadline

Note 29 states that, when ordinary operation uses distributed CBR refresh at a 15.6 µs interval, CBR refresh should be executed within 15.6 µs immediately:

- after exiting self-refresh; and
- before entering self-refresh.

The retention obligation therefore crosses the mode boundary.

A useful reconstruction is:

```text
ordinary-mode coverage schedule
    -> bounded handoff to self-refresh
    -> self-refresh maintains array
    -> bounded handoff back to ordinary schedule
```

This is stronger than merely saying `the device has self-refresh`.

---

## H6 — Burst/RAS-only users must establish whole-array coverage around the handoff

Note 30 gives a different rule for systems using RAS-only refresh or burst CBR in normal operation: 1024 distributed CBR refresh cycles at 15.6 µs intervals should be executed within 16 ms immediately after exiting and before entering self-refresh.

The source therefore distinguishes at least two ordinary-regime histories at the self-refresh boundary.

The required handoff work depends on how refresh coverage was being supplied outside self-refresh.

Thus:

```text
same self-refresh mode
    !=
same transition obligation for every external refresh regime
```

---

## H7 — Repetitive self-refresh entry is not unconstrained

Note 31 states that repetitive self-refresh without refreshing all memory is not allowed. Once self-refresh has been exited, all memory cells need to be refreshed before self-refresh is entered again.

This is a particularly useful retention boundary.

The product documentation does not model self-refresh as a timeless binary switch that can be toggled arbitrarily. It imposes a coverage obligation between self-refresh episodes.

A safe summary is:

```text
self-refresh exit
    !=
immediate permission to begin another self-refresh episode

self-refresh exit
    -> re-establish whole-array refresh coverage
    -> next self-refresh entry becomes admissible
```

---

## H8 — Output service is intentionally unavailable during self-refresh

The self-refresh waveform holds data output at High-Z while the mode is active.

This supports another important distinction:

```text
payload retention
    !=
foreground read availability
```

Self-refresh is a retention regime in which the device is maintaining stored state while ordinary service is suspended.

---

## H9 — The inspected revision chain begins in 1996

The revision record on printed p. 33 states:

- Rev. 1.0 — 30 Sep. 1996 — Initial issue;
- Rev. 2.0 — 26 Nov. 1996;
- Rev. 3.0 — 24 Feb. 1997;
- Rev. 4.0 — Nov. 1997.

This supports a conservative document-availability statement:

> Hitachi documentation for this named device family existed by 30 September 1996, and the directly inspected revision is from November 1997.

It does **not** establish first shipment, first customer use, or the first commercial self-refresh DRAM.

---

# Engineering reconstruction

## E1 — Self-refresh moves cadence/coverage work behind the device interface, but only inside a bounded regime

The external interface enters a state in which ordinary refresh commands are no longer being issued while the payload is expected to remain recoverable.

That supports the bounded reconstruction:

```text
external refresh scheduling responsibility
    -> suspended during the self-refresh interval
```

But the same datasheet makes the transition obligations explicit. Therefore it is too strong to write:

```text
self-refresh means the host no longer participates in retention correctness
```

A more precise model is:

```text
host/controller establishes admissible entry
    ↓
device maintains payload during self-refresh
    ↓
host/controller satisfies exit-side coverage obligation
```

The maintenance authority is redistributed, not abolished.

---

## E2 — A mode boundary can itself be part of the retention mechanism

Case 03 often speaks of a deadline such as `all rows must be refreshed within T`.

The HM5118165L adds a second type of deadline:

```text
maintenance-regime transition deadline
```

The stored data can remain physically present while the protocol approaches or violates a transition-side coverage requirement.

So retention correctness depends not only on what happens **inside** a mode but also on whether the system crosses between modes with a valid maintenance history.

---

## E3 — Maintenance history matters even when payload addresses do not change

Nothing in this mode switch requires the logical address of user data to change.

Yet admissible transition behavior depends on recent refresh history:

- whether ordinary refresh was distributed or burst-style;
- whether the required rows have been covered;
- how recently the last qualifying refresh occurred;
- whether full-array coverage has been re-established after exit.

Therefore:

```text
stable logical address
    !=
maintenance-history irrelevance
```

The payload can have a stable address while its continued recoverability depends on hidden temporal history.

---

## E4 — Coverage completion is different from mode indication

The external signal pattern can indicate that self-refresh was entered or exited. That does not itself prove that the preceding/following whole-array coverage obligation has been satisfied.

This yields a useful general distinction:

```text
mode state
    !=
coverage-completion evidence
```

The datasheet gives rules for the latter but does not expose a host-readable progress register proving that every required row has been covered.

---

# Functional analogy

The following comparison is functional only.

The handoff resembles other systems in this repository where authority moves between maintenance regimes:

```text
old maintenance regime
    -> transition qualification
    -> new maintenance regime
    -> requalification before returning
```

This is comparable at the relation level to redundancy-mode conversion, log/snapshot handoff, or persistence-domain transfer.

It is **not** evidence of shared historical genealogy, common implementation, or identical failure semantics.

---

# Philosophical interpretation

The technical fact that matters is narrow: the apparent continuity of the stored value depends on a controlled transition between maintenance regimes.

A value may look continuously `there` to a higher layer even though, below that interface, the system changes who is responsible for renewing it and imposes temporal conditions on that handoff.

The useful conceptual point is therefore not that `memory is process` in a generic sense. It is more exact:

> continuity of availability can depend on a retained and correctly completed relation between successive maintenance regimes.

This interpretation stops at the documented mode-transition mechanism. It should not be projected backward as Hitachi's own philosophical vocabulary.

---

# Explicit non-claims

This packet does **not** claim:

1. that HM5118165 was the first DRAM with self-refresh;
2. that the initial 1996 datasheet date equals first shipment;
3. that `battery backup` means nonvolatile retention;
4. that the 128 ms specification equals intrinsic cell-retention lifetime;
5. that every self-refresh implementation uses the same internal timer/counter design;
6. that the datasheet exposes the exact internal refresh oscillator or counter architecture;
7. that the self-refresh transition rules are identical across vendors or generations;
8. that the device exposes a host-readable proof of whole-array refresh completion;
9. that mode entry itself proves the pre-entry refresh obligation was satisfied;
10. that mode exit itself proves the post-exit refresh obligation was satisfied;
11. that self-refresh guarantees useful read service while active;
12. that this product establishes JEDEC standard chronology or invention priority.

---

# What this changes in Case 03

This deepening adds one product-level retention seam not previously explicit in the case:

```text
refresh mechanism exists
    !=
refresh regime is currently active
    !=
transition into that regime is admissible
    !=
whole-array coverage obligation is complete
    !=
foreground service is available
```

It also strengthens the case's existing claim that refresh control has multiple separable dimensions:

```text
cadence
coverage
admission
mode
handoff
service availability
```

These dimensions can move between controller and device without collapsing into one generic `refresh state`.

---

# Remaining evidence debt

Useful next slices are now narrower:

1. obtain an earlier named DRAM product with directly inspectable self-refresh documentation to move the public product-document floor earlier than 1996;
2. inspect a vendor document that explicitly exposes the internal self-refresh timer/counter implementation for a named product rather than only a patent architecture;
3. find contemporaneous controller documentation showing exactly how firmware/hardware satisfied the HM5118165L entry/exit coverage rules;
4. test whether later Hitachi revisions changed notes 28–31 or only timing/product parameters;
5. obtain board/BOM or shipment evidence before making adoption claims;
6. keep JEDEC self-refresh standard chronology separate from this vendor-product witness.

Broader SDRAM/EDO-DRAM product genealogy belongs primarily in `tmzncty/computing-archaeology`; this repository should retain only the maintenance-handoff analysis.
